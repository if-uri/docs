# Commands

## v2 CLI

`urirun` defaults to the v2 schema-first runtime.

```bash
urirun scan PATH --out generated/bindings.v2.json --registry-out generated/registry.json
urirun validate generated/bindings.v2.json
urirun compile generated/bindings.v2.json --out generated/registry.json
urirun list generated/registry.json
urirun run URI --registry generated/registry.json --payload '{"name":"Ada"}'
```

## Generate bindings in one line

Expose a package command:

```bash
urirun add-pypi sampleproject --out urirun.bindings.v2.json
```

Expose a command template:

```bash
urirun add-command 'util://local/echo/message' \
  --argv 'python3 -c "import sys; print(sys.argv[1])" {text}' \
  --param text:string:required \
  --out urirun.bindings.v2.json
```

## Install connectors from the hub

Install a verified connector package:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash
```

Dry-run the same install through the runtime catalog:

```bash
urirun connectors list --available
urirun connectors show http-check
urirun connectors install http-check
```

Inspect the connector directly:

```bash
urirun-http-check manifest
urirun-http-check bindings
urirun-http-check status https://ifuri.com --expect-status 200
```

Compile and run its URI:

```bash
python - <<'PY' > bindings.json
import json
from urirun_connector_http_check import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun compile bindings.json --out registry.json
urirun run 'httpcheck://host/http/query/status' registry.json \
  --payload '{"url":"https://ifuri.com","expectStatus":200}' \
  --execute \
  --allow 'httpcheck://host/*'
```

## Inspect runtime errors

Failed runs are stamped with stable `error://` addresses and persisted to
`~/.urirun/errors.jsonl` by default:

```bash
urirun errors recent
urirun errors search policy
urirun errors info E-ce9b1dd4
urirun errors bindings > error-bindings.json
urirun compile error-bindings.json --out error-registry.json
urirun run 'error://local/errors/query/recent' error-registry.json
```

Use `urirun errors ticket <code> <project>` to turn a recurring error into a
planfile ticket.

## Check compatibility migration

Legacy host/domain modules are moving out of `urirun` core into connector
packages and the ifURI app. Use the compatibility report before removing old
imports from a downstream project:

```bash
urirun compat list
urirun compat list --json
urirun compat check --json
```

`compat check` returns non-zero until every replacement package or app-layer
replacement is installed.

## Versioned commands

```bash
urirun-v1 compile v1/examples/json/bindings.v1.example.json --out /tmp/registry.json
urirun-v1 run 'media://local/video/transcode' /tmp/registry.json --payload '{"input":"a.mp4","output":"b.mp4"}'
urirun-v2 --help
```

Use these versioned commands when a script must stay pinned to a major registry
contract.

## Module commands

The module namespace is `urirun`, so these are also valid:

```bash
python -m urirun.v2 --help
python -m urirun.v2_mcp tools generated/registry.json
python -m urirun.v2_mcp card generated/registry.json
```
