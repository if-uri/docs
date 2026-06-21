# Connector authoring

This tutorial builds a small connector with `urirun.connector(...)`, exports
registry-ready bindings, and runs a URI through `urirun`. It mirrors the real
[if-uri/urirun-connector-http-check](https://github.com/if-uri/urirun-connector-http-check)
package. For installing and cataloguing existing connectors, see
[Connectors](connectors.md).

## The idea

A connector declares each URI route **once**, next to the function that knows
how to run it. `urirun.connector(...)` returns a connector object; its
`@connector.command(...)` decorator turns a Python function into a URI binding,
using the function signature as the payload schema. The function returns an
argv template, so the same declaration drives CLI, registry, MCP and A2A.

## 1. Create the connector object

```python
import urirun

CONNECTOR_ID = "http-check"
CONNECTOR = urirun.connector(CONNECTOR_ID, scheme="httpcheck")
```

The `scheme` becomes the first segment of every route this connector exposes:
`httpcheck://...`.

## 2. Declare a command

Decorate a function with `@CONNECTOR.command("resource/operation", ...)`. The
path after the scheme and host is taken from the decorator; the payload schema
is inferred from the function parameters and their defaults.

```python
@CONNECTOR.command("http/query/status", meta={"label": "Check HTTP status"})
def status_command(url: str, expectStatus: int = 200, timeout: float = 10.0) -> list[str]:
    """Declare the URI binding once; the signature is the schema."""
    return [
        "urirun-http-check",
        "status",
        "{url}",
        "--expect-status",
        "{expectStatus}",
        "--timeout",
        "{timeout}",
    ]
```

This declares the route:

```text
httpcheck://host/http/query/status
```

The returned list is an **argv template**. Placeholders such as `{url}` and
`{expectStatus}` are filled from the validated payload at run time, so the
console script never parses URIs itself.

## 3. Export bindings and a manifest

Expose two functions so the hub, `urirun` and tests can read the same package:

```python
from typing import Any
from importlib import resources
import json


def urirun_bindings() -> dict[str, Any]:
    return CONNECTOR.bindings()


def connector_manifest() -> dict[str, Any]:
    text = resources.files(__package__).joinpath("connector.manifest.json").read_text("utf-8")
    return json.loads(text)
```

`CONNECTOR.bindings()` returns the registry-ready bindings built from every
declared command. The manifest is catalog metadata (id, title, routes,
publisher) and should describe the same routes as the bindings.

## 4. Run the route through urirun

Generate bindings, compile a registry, then execute the URI:

```bash
python - <<'PY' > bindings.json
import json
from urirun_connector_http_check import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'httpcheck://host/http/query/status' registry.json \
  --payload '{"url":"https://ifuri.com","expectStatus":200,"timeout":10}' \
  --execute \
  --allow 'httpcheck://host/*'
```

The `--allow` policy gate is required for executable adapters: `urirun` only
runs routes that match an explicit allow pattern.

## 5. Package shape

A publishable connector normally ships:

- `pyproject.toml` with a console script (here `urirun-http-check`) and a
  `urirun.bindings` entry point,
- `connector.manifest.json` with catalog metadata,
- the connector module that calls `urirun.connector(...)` and declares commands,
- `urirun_bindings()` / `connector_manifest()` accessors,
- tests that prove the package works without the hub,
- a Docker smoke test that proves network execution and MCP/A2A projection.

Minimal `pyproject.toml` entry:

```toml
[project.scripts]
urirun-http-check = "urirun_connector_http_check.cli:main"

[project.entry-points."urirun.bindings"]
http-check = "urirun_connector_http_check:urirun_bindings"
```

With that in place, installed connectors are visible to the runtime:

```bash
urirun discover --registry-out .urirun/connectors.registry.json
urirun list --entry-points
```

## 6. Verify in Docker

Prove the connector works inside a real network, not only on your host:

```bash
git clone https://github.com/if-uri/urirun-connector-http-check.git
cd urirun-connector-http-check
make docker-test
```

The smoke environment starts a target service, installs `urirun` and the
connector in a separate tester, executes the URI, and checks the MCP tools and
A2A card projections.

## 7. Reuse the urirun host backend (don't duplicate it)

`urirun` is a self-contained backend: storage and operational logic live once in
its `host/` layer (`urirun.host.host_db`, `urirun.host.domain_monitor`,
`urirun.host.planfile_adapter`). A connector that needs that behaviour should
**reuse the backend**, not copy it — the connector then owns only the URI route
declarations, the CLI and the JSON envelope.

```python
import urirun
from urirun.host import host_db          # the backend, single source of truth

DATA = urirun.connector("sqlite-context", scheme="data")

@DATA.command("datasets/query/list", meta={"label": "List datasets"})
def datasets_list_command(db: str = "") -> list[str]:
    return ["urirun-sqlite-context", "datasets-list", "--db", "{db}"]

def list_datasets(db: str = "") -> dict:
    # delegate to the backend; add only the connector envelope
    return {"ok": True, "connector": "sqlite-context", "datasets": host_db.list_datasets(db or None)}
```

The official `sqlite-context`, `domain-monitor` and `planfile` connectors are
built exactly this way — each shrank by ~300–400 lines once it stopped copying
the backend. Use this when your connector mirrors an existing host capability;
write standalone logic only when there is no backend equivalent (e.g.
`time-tools`, `uuid`). The boundary is tracked by `urirun compat list`.

## Next steps

- [Connectors](connectors.md) - install from the hub, package shape, catalog
  and trust model.
- [Registry and bindings](registry-and-bindings.md) - how bindings become a
  dispatchable registry.
- [MCP and A2A](mcp.md) - how the same registry becomes LLM tools and agent
  cards.
- [Transports](transports.md) - the adapter kinds a command can target.
