# Upgrade guide: urirun 0.3 → 0.4

urirun 0.4 is **backward compatible**: the public API is unchanged and old import
paths still work through shims. For most downstreams the upgrade is a one-line pin
bump; the rest of this page is optional new capability.

## 1. Bump the pin

```diff
- pip install "git+https://github.com/if-uri/urirun.git@v0.3.14#subdirectory=adapters/python"
+ pip install "git+https://github.com/if-uri/urirun.git@v0.4.0#subdirectory=adapters/python"
```

The same `@v0.3.14 → @v0.4.0` change applies to connector `pyproject.toml` pins,
`get.urirun.com` (`URIRUN_REF`) and the ifURI app. Across this repo set it is one
command — `apply-release-pins.sh v0.4.0` (see the [release checklist](release-checklist.html)).

## 2. What stays the same

- **Public API**: `urirun.command`, `urirun.shell`, `urirun.connector`, `urirun.run`
  and `urirun.compile_registry` are unchanged. Connectors built with the decorators
  need only the pin bump.
- **The contract**: `urirun.bindings.v2` → registry → adapter → executor is stable.
- **Old import paths**: `import urirun.errors`, `urirun._runtime` etc. still resolve
  via back-compat shims.

## 3. What moved (IFURI-007)

The runtime was split into `urirun.runtime.*` with `host` and `connector`
subpackages. New code should import from the canonical location:

```diff
- from urirun import errors
+ from urirun.runtime import errors
```

Shims keep the old paths working, but they are the migration target, not the
destination. Check what your project still imports from the legacy layout:

```bash
urirun compat check        # which modules moved to runtime/host/connector or to a connector package
```

## 4. New capabilities (opt in)

- **[Adopt any package as URI](adopt-as-uri.html)** — `urirun adopt-pack <manifest|dir|package>`
  gives an existing package a URI surface with zero-to-minimal change
  (`[tool.urirun]` in pyproject, a `"urirun"` key in package.json, or CLI entry points).
- **[`error://` diagnostics](errors.html)** — standardized error codes, a `@capture`
  decorator and an `/errors` route on nodes.
- **Param-aware routing** — concrete URIs resolve templated mid-path `{param}`
  segments and bind the value to the handler.
- **`secret://` by reference** and **`urirun add-openapi`** — credentials resolved
  lazily at the executor boundary; import an OpenAPI doc into declarative `fetch`
  routes.
- **Connector SDKs in 9 more languages** (Go, PHP, Ruby, Perl, Bash, Rust,
  TypeScript, Java, C#) beside Python/JS.

See the [0.4 work summary](work-summary-2026-06-21.html) for the full surface.
