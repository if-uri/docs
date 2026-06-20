# TODO

## Documentation roadmap

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
- [x] Keep runtime versions in docs aligned with the latest tested `urirun`
      GitHub tag. (pinned to `v0.3.14` across all install snippets)

## Cross-repository hygiene

- [ ] Link every connector README back to the hub page and docs.
- [ ] Keep `connect.ifuri.com/llms.txt` and docs connector pages in sync.
- [ ] Add a release checklist for runtime, connector packages, examples and
      app docs.
