# Changelog

This changelog records source documentation changes for the public docs site.
Historical implementation reports are linked from the index and source-of-truth
pages instead of being duplicated here.

## [Unreleased] - 2026-07-14

### Fixed
- Fix ast-print-statements issues (ticket-08ad3628)
- Fix ruff-print-statements issues (ticket-fbb930d0)
- Fix ai-boilerplate issues (ticket-3503d95b)
- Fix import-optimization issues (ticket-a510713e)
- Fix ast-unused-imports issues (ticket-63a4630f)
- Fix ast-print-statements issues (ticket-5a399263)
- Fix ruff-print-statements issues (ticket-3509b2b6)
- Fix ruff-sorted-imports issues (ticket-a5e3cc28)
- Fix ai-boilerplate issues (ticket-6b4d42f3)
- Fix import-optimization issues (ticket-a43228ab)
- Fix ast-unused-imports issues (ticket-a05af845)
- Fix ast-string-concat issues (ticket-0a2df3da)
- Fix ast-print-statements issues (ticket-72011ab4)
- Fix ast-missing-return-type issues (ticket-b4ea7a1c)
- Fix ruff-unused-imports issues (ticket-2aeccd44)
- Fix ruff-print-statements issues (ticket-d0c121bb)
- Fix ruff-sorted-imports issues (ticket-5b988792)
- Fix smart-return-type issues (ticket-1ec01c6e)
- Fix string-concat-fstring issues (ticket-a9705ec8)
- Fix unused-imports issues (ticket-edc668f9)
- Fix string-formatting issues (ticket-293a1472)
- Fix import-optimization issues (ticket-e7ad6bdb)

## [Unreleased]

Current unreleased documentation updates are grouped below.

### Added
- Add a current architecture page covering the split between the `urirun` hub,
  contracts, connector router, flow, services, widgets, artifacts, connectors
  and nodes.
- Add the 2026-06-20 project-structure audit page and link it into the generated
  docs navigation.
- Add the 2026-06-20 cross-repository work summary.
- Add a documentation TODO focused on connector authoring, LAN host/node usage
  and noVNC demos.
- Record follow-up documentation updates in `get`, `ifuri-com` and connector
  repositories.
- Record follow-up documentation updates in `roadmap`, `marketing` and `logo`.
- Record the published Planfile, Domain Monitor and SQLite Context connector
  packages in the cross-repository summary and README.
- Expand the connector guide with tested Planfile, Domain Monitor and SQLite
  Context usage examples and Docker smoke commands.
- Split Domain Monitor DNS reads from provider-specific Namecheap DNS mutation
  routes in the connector guide.
- Update Domain Monitor install snippets to `v0.2.1`, the self-contained
  connector runtime release.
- Update SQLite Context install snippets to `v0.1.1`, the self-contained
  host data store release.

### Changed
- Link the documentation index and README to the work summary and related
  implementation repositories.
- Update runtime references to the current `if-uri/urirun` project namespace.
- Replace the old single-connector roadmap with the current P0/P1/P2 plan and
  planfile tickets IFURI-015..IFURI-020.
- Add checked `urirun connectors ...` dry-run commands next to public
  `curl | bash` connector install snippets.
- Mark IFURI-008 as released and document entry-point connector discovery via
  `urirun discover` and `urirun compile --entry-points`.
- Add `urirun.bindings` entry-point examples to the connector guide and
  connector-authoring tutorial.
- Mark IFURI-020 as released and document validated planfile sprint/health
  commands.
- Document built-in `error://` diagnostics, including `urirun errors ...`,
  registry-ready error bindings, URI flow examples and planfile ticket creation.
- Document `urirun compat list/check` as the migration report for modules moving
  from `urirun` core to connector packages or the ifURI app.
