# Naming

The public runtime name is `urirun`. The current GitHub repository URL is
`if-uri/urirun`.

## Use `urirun` for runtime surfaces

Use `urirun` for:

- Python distribution name
- Python import namespace
- JS package name and imports
- primary CLI command
- versioned CLI commands
- JSON document versions
- Docker/OCI labels
- C firmware adapter files
- documentation title
- logo and website branding

Recommended commands:

```bash
urirun --help
urirun scan ./project
urirun validate generated/bindings.v2.json
urirun list generated/registry.json
urirun run 'tool://local/report/render' --registry generated/registry.json
```

Version-specific CLIs are also available:

```bash
urirun-v1 --help
urirun-v2 --help
```

Examples:

```python
import urirun

@urirun.command("demo://host/example/query/run")
def run_example(target: str):
    return ["demo", "{target}"]
```

```js
import { parseUri } from "urirun";
```

```json
{ "version": "urirun.bindings.v2" }
```

```dockerfile
LABEL io.tellmesh.urirun.manifest="/app/bindings.json"
```

## Earlier names are historical

The runtime moved through earlier tellmesh repository names before the current
ifURI organization namespace. Everything user-facing is now `urirun`, including
the remote and install commands:

```txt
git@github.com:if-uri/urirun.git
```

```bash
pip install "urirun>=0.4.190"
npm install github:if-uri/urirun
```

Historical changelog entries can still mention older names, but new docs,
scripts, manifests and examples should point at `if-uri/urirun`.
