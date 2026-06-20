# Release checklist

A repeatable checklist for shipping a coordinated ifURI release across the
runtime, connector packages, examples and app docs. The goal is that every
public install snippet, manifest and catalog entry points at the same tested
versions.

## 1. Runtime (`urirun`)

- [ ] Tests green on the target commit (`make test` in `if-uri/urirun`).
- [ ] Tag the release (for example `v0.3.14`) and push the tag.
- [ ] Update install snippets to the new tag across docs, the website and
      connector READMEs:
      `pip install "git+https://github.com/if-uri/urirun.git@<tag>#subdirectory=adapters/python"`.
- [ ] CHANGELOG and VERSION updated.

## 2. Connector packages

For each `urirun-connector-*` package:

- [ ] Package version bumped; `connector.manifest.json` and `urirun_bindings()`
      describe the same routes.
- [ ] `make docker-test` passes (CLI, registry compile, `urirun run`, MCP tools,
      A2A card).
- [ ] README links back to the connect.ifuri.com hub page and docs.ifuri.com.
- [ ] Hub catalog entry (`connect.ifuri.com/data/connectors/<id>/manifest.json`)
      updated and validated:
      `curl -fsS https://connect.ifuri.com/validate-connector --data @manifest.json`.

## 3. Connector hub (`connect.ifuri.com`)

- [ ] `python3 tools/build_catalog.py` regenerates `connectors.json`,
      `registry.json`, `search.json`, `llms.txt` and `sitemap.xml`.
- [ ] `bash tests/smoke.sh` passes.
- [ ] `docs.ifuri.com/connectors.html` status list matches the catalog
      (available vs planned).

## 4. Examples

- [ ] Numbered examples build and pass (`make test`, plus `make test-full`
      for `11-novnc_lan_flow`).
- [ ] Heavy Docker examples pin image tags for reproducible CI.
- [ ] Example install/run commands reference the released runtime tag.

## 5. App and host docs

- [ ] `if-uri/app` README, CHANGELOG and VERSION reflect the release.
- [ ] `ifuri.com` download copy aligned: app version is live from GitHub
      Releases; the urirun runtime tag is current.
- [ ] `get.ifuri.com` default `URIRUN_REF` points at the released tag.

## 6. Cross-repository sync

- [ ] Work summary in `if-uri/docs` updated for the release.
- [ ] Roadmap entries reflect shipped vs planned work.
- [ ] All `TODO.md` / `CHANGELOG.md` files touched by the release updated.

## Related

- [Connectors](connectors.md) - catalog, package shape and trust model.
- [Connector authoring](connector-authoring.md) - build a connector package.
- [Getting started](getting-started.md) - install and run a URI.
