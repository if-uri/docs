# TODO

## Documentation roadmap

- [ ] Keep `project-structure-audit-2026-06-20.md` aligned with
      roadmap IFURI-015..IFURI-019 and released tooling fixes.
- [ ] Add a public guide for the full connector Docker matrix once IFURI-016 has
      a stable `make` target and captured logs/results.
- [ ] Add app GUI operator screenshots after IFURI-017 lands.
- [x] Document released IFURI-008 connector entry-point discovery for installed
      connector packages.
- [x] Document built-in `error://` diagnostics, CLI shortcuts, URI bindings and
      planfile ticket conversion. (`errors.md`, `commands.md`)
- [x] Document `urirun compat list/check` for IFURI-015 core-to-connector/app
      migration checks. (`commands.md`)
- [x] Publish the 2026-06-20 work summary on the generated docs site.
      (`work-summary-2026-06-20.md`, built into the site and linked from index)
- [x] Add architecture diagrams for `URI -> binding -> registry -> adapter -> executor`.
      (Architecture section in `registry-and-bindings.md`)
- [x] Add a connector authoring tutorial based on `urirun.connector(...)`.
      (`connector-authoring.md`)
- [x] Add an operator guide for host/node communication across a LAN.
      (`host-node-lan.md`)
- [x] Add a noVNC demo guide that links to `if-uri/examples/11-novnc_lan_flow`.
      (`novnc-demo.md`)
- [x] Keep active runtime install snippets aligned with the latest tested
      `urirun` release. Active docs use `urirun>=0.4.190`; historical upgrade
      and work-summary pages may still mention older tags as migration context.

## Cross-repository hygiene

- [ ] Review active install snippets for `github.com/if-uri/urirun` before each
      runtime or connector release.
- [x] Link every connector README back to the hub page and docs.
      (Related-projects section with hub page + docs.ifuri.com links across all
      published `urirun-connector-*` repos)
- [x] Record the Planfile, Domain Monitor and SQLite Context connector split in
      the cross-repository work summary.
- [x] Keep `connect.ifuri.com/llms.txt` and docs connector pages in sync.
      (`connectors.md` catalog status now mirrors the 13 hub manifests, 8
      available / 5 planned, and points to connectors.json/llms.txt as canonical)
- [x] Add a release checklist for runtime, connector packages, examples and
      app docs. (`release-checklist.md`)
