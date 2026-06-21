# Adopt any package as URI

Give an existing application a URI surface with the **least possible change** —
ideally none. urirun reads what a package already ships and emits a validated
`urirun.bindings.v2` registry, so every capability becomes an addressable URI that
flows through the normal compile / validate / run / MCP pipeline.

There are three paths, ordered from zero change to one small config block.

## 1. Zero change — automatic CLI → URI

Any pip or npm package that ships a command becomes URI-addressable with no edit:

```bash
urirun add-pypi <package>            # or: python -m urirun.runtime.v2_adopt add-python-package <package>
urirun compile urirun.bindings.v2.json --out registry.json
urirun run 'cli://<package>/<script>/run' registry.json --payload '{"args":["--version"]}' --execute --allow 'cli://*'
```

urirun reads the package's `console_scripts` / `bin` entry points and generates one
`cli://…/run` binding per command. The argument vector stays a JSON Schema, so callers
pass arbitrary args while the contract is explicit.

## 2. Wrapper — adopt a capability manifest

A package that already describes its URI surface in a manifest (`scheme` +
`uri_patterns` + handlers) is mapped **1:1**, with no change to the package:

```bash
urirun adopt-pack ./path/to/manifest.yaml --out pack.bindings.v2.json   # a file
urirun adopt-pack <installed-package-name> --out pack.bindings.v2.json  # discovered, no import
```

Installed packages are located through a `urirun.packs` entry point or a recorded
`manifest.yaml`, using `importlib.metadata` — **the package is never imported**, so its
own dependencies need not be present to adopt its URI surface. The mapping:

| manifest | bindings.v2 |
| --- | --- |
| `pattern: kvm://{host}/task/command/type-text` | binding URI |
| `kind: query` / `command` | `meta.uriKind` |
| `operation` + `handlers.python: python://mod:func` | `local-function` `ref` |
| `side_effects: true` / `approval: required` | `policy.sideEffects` / `policy.approval` |

Unhydrated `local-function` refs dispatch in simulated mode (so the registry validates
and routes immediately); hydrate the ref with the package's callable to execute for real.

## 3. One small config block — declare the URI in project metadata

A package without a manifest can opt in with a single table — no code:

```toml
# pyproject.toml  (Python / PyPI)
[tool.urirun]
scheme = "kvm"
manifest = "urikvm/manifest.yaml"     # or inline uri_patterns = [ … ]
```

```json
// package.json  (node / npm)
"urirun": { "scheme": "browser", "manifest": "manifest.json" }
```

Then `urirun adopt-pack <dir-or-name>` reads `[tool.urirun]` and emits the registry —
the URI is configured directly from the project's own metadata, from PyPI or locally.

## What this proves

Pointed at the [tellmesh](https://github.com/) capability packs unchanged, urirun adopted
**18 packs into one registry — 95 URI routes** across 21 schemes (`browser`, `kvm`, `llm`,
`ocr`, `rdp`, `stepper`, `stt`, `him`, `screen`, `vql`, …), all passing `urirun validate`.

One pack was skipped: a `shell://{command}` pattern carries only an authority, while
bindings.v2 requires `scheme://host/resource/kind/operation`. Such a URI must add resource
and operation segments to be adopted — the grammar is the contract.
