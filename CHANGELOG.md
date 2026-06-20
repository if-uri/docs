# Changelog

## [Unreleased]

### Added
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
