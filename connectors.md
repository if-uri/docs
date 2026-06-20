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
curl -fsSL 'https://connect.ifuri.com/install?connectors=planfile,domain-monitor,sqlite-context,http-check,time-tools' | bash
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

## Tested external connectors

The currently tested external connector packages are:

| Connector | Package repo | Main URI examples |
| --- | --- | --- |
| HTTP Check | [if-uri/urirun-connector-http-check](https://github.com/if-uri/urirun-connector-http-check) | `httpcheck://host/http/query/status` |
| Time Tools | [if-uri/urirun-connector-time-tools](https://github.com/if-uri/urirun-connector-time-tools) | `time://host/clock/query/now` |
| Planfile | [if-uri/urirun-connector-planfile](https://github.com/if-uri/urirun-connector-planfile) | `task://host/ticket/command/create`, `planfile://host/dsl/command/run` |
| Domain Monitor | [if-uri/urirun-connector-domain-monitor](https://github.com/if-uri/urirun-connector-domain-monitor) | `monitor://host/http/query/status`, `monitor://host/dns/query/current`, `flow://host/domain/command/check` |
| Namecheap DNS | [if-uri/urirun-connector-namecheap-dns](https://github.com/if-uri/urirun-connector-namecheap-dns) | `dns://host/records/command/plan`, `dns://host/records/command/backup`, `dns://host/records/command/apply` |
| SQLite Context | [if-uri/urirun-connector-sqlite-context](https://github.com/if-uri/urirun-connector-sqlite-context) | `data://host/record/command/upsert`, `log://host/logs/query/recent` |

Each package exposes a hub page and a machine-readable manifest:

- [connect.ifuri.com/connectors/http-check](https://connect.ifuri.com/connectors/http-check),
- [connect.ifuri.com/connectors/time-tools](https://connect.ifuri.com/connectors/time-tools),
- [connect.ifuri.com/connectors/planfile](https://connect.ifuri.com/connectors/planfile),
- [connect.ifuri.com/connectors/domain-monitor](https://connect.ifuri.com/connectors/domain-monitor),
- [connect.ifuri.com/connectors/namecheap-dns](https://connect.ifuri.com/connectors/namecheap-dns),
- [connect.ifuri.com/connectors/sqlite-context](https://connect.ifuri.com/connectors/sqlite-context).

### HTTP Check

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

### Time Tools

- package repo: [if-uri/urirun-connector-time-tools](https://github.com/if-uri/urirun-connector-time-tools),
- hub page: [connect.ifuri.com/connectors/time-tools](https://connect.ifuri.com/connectors/time-tools),
- manifest: [connect.ifuri.com/connectors/time-tools.json](https://connect.ifuri.com/connectors/time-tools.json).

It exposes:

```text
time://host/clock/query/now
```

Install and run it:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=time-tools' | bash

python - <<'PY' > bindings.json
import json
from urirun_connector_time_tools import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'time://host/clock/query/now' registry.json \
  --payload '{"timezone":"UTC","output":"iso"}' \
  --execute \
  --allow 'time://host/*'
```

### Planfile

Planfile exposes ticket queues and DSL commands as URI routes:

```text
task://host/tickets/query/list
task://host/ticket/command/create
task://host/ticket/command/start
task://host/ticket/command/complete
planfile://host/dsl/command/run
```

Run it through `urirun`:

```bash
pip install 'git+https://github.com/if-uri/urirun-connector-planfile.git@v0.1.1'

urirun-planfile bindings > bindings.json
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'task://host/ticket/command/create' registry.json \
  --payload '{"project":".","name":"Daily domain check","queue":"daily"}' \
  --execute \
  --allow 'task://host/*'
```

### Domain Monitor

Domain Monitor moves HTTP status checks, DNS reads, screenshot artifacts and
daily domain-check flows out of the `urirun` core:

```text
monitor://host/http/query/status
monitor://host/dns/query/current
monitor://host/dns/query/expected
browser://host/page/command/screenshot
flow://host/domain/command/check
flow://host/daily/command/run
```

Mock DNS read example:

```bash
pip install 'git+https://github.com/if-uri/urirun-connector-domain-monitor.git@v0.2.1'

urirun-domain-monitor bindings > bindings.json
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'monitor://host/dns/query/current' registry.json \
  --payload '{"domain":"example.com","current_records":"[{\"Name\":\"@\",\"Type\":\"A\",\"Address\":\"203.0.113.10\"}]"}' \
  --execute \
  --allow 'monitor://host/*'
```

Provider-specific DNS changes are intentionally separate. Use Namecheap DNS for
host-record planning, backup and apply routes.

### Namecheap DNS

Namecheap DNS owns the provider-specific `dns://` routes:

```text
dns://host/records/query/current
dns://host/records/query/expected
dns://host/records/command/plan
dns://host/records/command/backup
dns://host/records/command/apply
```

Safe mock DNS planning example:

```bash
pip install 'git+https://github.com/if-uri/urirun-connector-namecheap-dns.git@v0.1.0'

urirun-namecheap-dns bindings > bindings.json
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'dns://host/records/command/plan' registry.json \
  --payload '{"domain":"example.com","current_records":"[{\"Name\":\"@\",\"Type\":\"A\",\"Address\":\"203.0.113.10\"}]","desired_records":"[{\"Name\":\"@\",\"Type\":\"A\",\"Address\":\"203.0.113.11\"}]"}' \
  --execute \
  --allow 'dns://host/*'
```

### SQLite Context

SQLite Context gives the host a local memory layer for datasets, records,
artifacts, checks and logs:

```text
data://host/dataset/command/create
data://host/record/command/upsert
data://host/records/query/search
artifact://host/artifact/command/register
check://host/check/command/add
log://host/logs/query/recent
```

Run it through `urirun`:

```bash
pip install 'git+https://github.com/if-uri/urirun-connector-sqlite-context.git@v0.1.0'

urirun-sqlite-context bindings > bindings.json
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run 'data://host/dataset/command/create' registry.json \
  --payload '{"name":"domains","dataset_schema":"{\"type\":\"object\"}"}' \
  --execute \
  --allow 'data://host/*'
```

## Docker verification

Every executable connector should have a Docker smoke test that proves it works
inside a real network, not only on the developer host. The current pattern is:

- one target service that exposes a resource, for example nginx,
- one tester service that installs `urirun` and the connector,
- URI execution through `urirun run`,
- MCP tools projection,
- A2A card projection.

For the HTTP Check connector:

```bash
git clone https://github.com/if-uri/urirun-connector-http-check.git
cd urirun-connector-http-check
make docker-test
```

For the Time Tools connector:

```bash
git clone https://github.com/if-uri/urirun-connector-time-tools.git
cd urirun-connector-time-tools
make docker-test
```

For Planfile:

```bash
git clone https://github.com/if-uri/urirun-connector-planfile.git
cd urirun-connector-planfile
make docker-test
```

For Domain Monitor:

```bash
git clone https://github.com/if-uri/urirun-connector-domain-monitor.git
cd urirun-connector-domain-monitor
make docker-test
```

For Namecheap DNS:

```bash
git clone https://github.com/if-uri/urirun-connector-namecheap-dns.git
cd urirun-connector-namecheap-dns
make docker-test
```

For SQLite Context:

```bash
git clone https://github.com/if-uri/urirun-connector-sqlite-context.git
cd urirun-connector-sqlite-context
make docker-test
```

For the full host/node connector scenario:

```bash
git clone https://github.com/if-uri/examples.git
cd examples/12-full_e2e_connect_lab
make test
```

The full scenario starts `host`, `pc1`, `pc2`, `ifuri-site` and
`registry-runtime` containers. It installs available connectors from
`connect.ifuri.com`, executes URI routes, checks host-node communication, serves
the same registry over gRPC, and verifies MCP tools plus A2A skills.

Catalog status (mirrors the hub manifests; the live
[connectors.json](https://connect.ifuri.com/connectors.json) and
[llms.txt](https://connect.ifuri.com/llms.txt) are the source of truth):

- available: `http-check`, `time-tools`, `browser-control`, `domain-monitor`,
  `planfile`, `sqlite-context`, `namecheap-dns`, `grpc-transport`,
- planned (manifest listed, package pending): `get-node`, `kvm`, `llm`,
  `mcp-filesystem`, `mqtt`.

## Connector package shape

A Python connector should normally include:

- `pyproject.toml` with a console script or importable package,
- `connector.manifest.json` with catalog metadata,
- `urirun.bindings.v2.json` or a function that returns equivalent bindings,
- a small CLI for direct shell use,
- tests that prove the package works without the hub.
- a Docker smoke environment that proves network execution and MCP/A2A
  projection.

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
