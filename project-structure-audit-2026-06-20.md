# Project structure audit

This page summarizes the 2026-06-20 repository audit for the ifURI ecosystem.
The planning source is the roadmap page:
[Project structure audit](https://roadmap.ifuri.com/?doc=06-structure-audit-2026-06-20).

## Current shape

- `urirun` is the URI runtime core: command decorators, bindings, registry,
  policy and execution adapters.
- `urirun-connector-*` repositories are installable capability packages.
- `app` is the host/operator application with GUI, mesh, node discovery and
  execution views.
- `get` is the one-line installer for host and node machines.
- `connect.ifuri.com` is the connector hub and machine-readable catalog.
- `examples` proves networked URI flows in Docker/noVNC.

## What still needs work

1. Finish the runtime boundary: move compatibility modules out of `urirun` once
   downstream code no longer imports them.
2. Prove every connector in one Docker matrix with host, pc1 and pc2.
3. Add connector install, route discovery and payload forms to the app GUI.
4. Publish richer per-connector contract pages with schemas, policy notes and
   tested version badges.
5. Add `get.ifuri.com` install bundles and `doctor` checks for LAN/service
   readiness.

## Planfile tickets

- `IFURI-015` - remove remaining compatibility modules from `urirun` core.
- `IFURI-016` - prove connector installs through a host-node Docker matrix.
- `IFURI-017` - add connector install and route discovery to the app GUI.
- `IFURI-018` - publish per-connector contract pages and compatibility badges.
- `IFURI-019` - add installer bundles and doctor checks for host/node setup.
- `IFURI-020` - released: local sprint YAML validation uses `--file-type
  sprint`, and `planfile health check` handles generated ticket buckets without
  crashing.

## Validated planfile commands

```bash
planfile validate schema .planfile/sprints/current.yaml --file-type sprint
planfile validate schema .planfile/sprints/backlog.yaml --file-type sprint
planfile health check get
```

Use [roadmap.ifuri.com](https://roadmap.ifuri.com/) for current status.
