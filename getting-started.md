# Getting started

Install directly from GitHub:

```bash
pip install "git+https://github.com/if-uri/urirun.git@v0.3.14#subdirectory=adapters/python"
```

The installed CLI and Python import namespace are both `urirun`.

## Install a ready connector

The connector hub can install `urirun` plus selected connector packages:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check,time-tools' | bash
```

For a virtualenv:

```bash
python3 -m venv .venv
PYTHON_BIN="$PWD/.venv/bin/python" \
  bash -c "curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash"
PATH="$PWD/.venv/bin:$PATH" urirun-http-check status https://ifuri.com --expect-status 200
```

More connector details: [Connectors](connectors.md).

## Generate a registry

Scan a project and compile a runtime registry in one command:

```bash
urirun scan ./project \
  --out generated/bindings.v2.json \
  --registry-out generated/registry.json
```

The scanner can read explicit binding files, Dockerfile labels, package scripts,
Python entry points, Makefile targets, and shell scripts.

## Inspect routes

```bash
urirun validate generated/bindings.v2.json
urirun list generated/registry.json
```

## Run a URI

Dry-run is the default for command-like routes:

```bash
urirun run 'cli://local/git/status' --registry generated/registry.json
```

For real execution, use a policy file and the `--execute` flag:

```bash
urirun run 'cli://local/git/status' \
  --registry generated/registry.json \
  --policy policy.json \
  --allow 'cli://local/**' \
  --execute
```

Keep shell templates behind an explicit policy with `allowShellTemplates: true`.

## Run the HTTP Check connector

After installing `http-check`, build its bindings and execute the URI:

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

## Run the Time Tools connector

After installing `time-tools`, build its bindings and execute the URI:

```bash
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
