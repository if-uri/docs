# Connectors

Connectors are installable packages that add URI-addressed capabilities to
`urirun` and the ifuri app. A connector can expose one or more URI schemes,
bindings, registry entries, CLI commands, service endpoints or flow examples.

The public catalog is:

- [connect.ifuri.com](https://connect.ifuri.com) - human connector hub,
- [connectors.json](https://connect.ifuri.com/connectors.json) - full catalog,
- [registry.json](https://connect.ifuri.com/registry.json) - registry projection,
- [search.json](https://connect.ifuri.com/search.json) - search index for users,
  crawlers and LLMs,
- [llms.txt](https://connect.ifuri.com/llms.txt) - compact LLM-readable index.

## Install from the hub

Install one connector:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash
```

Install multiple connectors:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=planfile,http-check,namecheap-dns' | bash
```

When using a virtualenv, run the installer with that Python binary:

```bash
python3 -m venv .venv
PYTHON_BIN="$PWD/.venv/bin/python" \
  bash -c "curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash"
PATH="$PWD/.venv/bin:$PATH" urirun-http-check status https://ifuri.com --expect-status 200
```

The `PATH` line matters for command bindings such as `argv-template`, because
`urirun` must be able to find console scripts installed by connector packages.

## Tested HTTP Check connector

The first external connector package is:

- package repo: [if-uri/urirun-connector-http-check](https://github.com/if-uri/urirun-connector-http-check),
- hub page: [connect.ifuri.com/connectors/http-check](https://connect.ifuri.com/connectors/http-check),
- manifest: [connect.ifuri.com/connectors/http-check.json](https://connect.ifuri.com/connectors/http-check.json).

It exposes:

```text
httpcheck://host/http/query/status
```

Run it through `urirun`:

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

The connector was verified from a clean virtualenv by installing through the
public hub and executing the URI through `urirun run`.

## Connector package shape

A Python connector should normally include:

- `pyproject.toml` with a console script or importable package,
- `connector.manifest.json` with catalog metadata,
- `urirun.bindings.v2.json` or a function that returns equivalent bindings,
- a small CLI for direct shell use,
- tests that prove the package works without the hub.

Example functions exposed by a package:

```python
from urirun_connector_http_check import connector_manifest, urirun_bindings

manifest = connector_manifest()
bindings = urirun_bindings()
```

The hub manifest and the package manifest should describe the same URI routes.
The package remains the executable source; the hub is the discovery and install
surface.

## Add a connector to the catalog

Create:

```text
data/connectors/<id>/manifest.json
```

Then rebuild and test the hub:

```bash
python3 tools/build_catalog.py
bash tests/smoke.sh
```

Validate a manifest against the public endpoint before opening or merging a
catalog change:

```bash
curl -fsS https://connect.ifuri.com/validate-connector \
  -H 'Content-Type: application/json' \
  --data @data/connectors/<id>/manifest.json
```

Detailed maintainer docs live in the hub repository:

- [Connector architecture](https://github.com/if-uri/connect.ifuri.com/blob/main/docs/CONNECTORS-ARCHITECTURE.md),
- [Submit a connector](https://github.com/if-uri/connect.ifuri.com/blob/main/docs/SUBMIT-CONNECTOR.md),
- [Plesk deploy](https://github.com/if-uri/connect.ifuri.com/blob/main/docs/PLESK.md).

## Trust model

The public catalog distinguishes verified and community connectors:

- `verified` connectors are maintained or reviewed by if-uri,
- `community` connectors must declare a publisher,
- community manifests must declare adapter kinds explicitly,
- executable adapters such as `argv-template` and `shell-template` are reserved
  for verified connectors unless a separate trust review approves them.

This keeps connector discovery easy while keeping arbitrary command execution
behind review and runtime policy.
