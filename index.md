# urirun docs

`urirun` is the user-facing CLI for URI-addressed command packages. A project can
declare a URI once and call it from a shell, backend, frontend, service flow, or
agent tool projection.

## Start here

- [Getting started](getting-started.md) - install from GitHub, scan artifacts,
  compile a registry, and run a URI.
- [Current architecture](architecture.md) - current system shape: hub,
  contracts, connector router, flow, services, widgets, artifacts and nodes.
- [Documentation source of truth](source-of-truth.md) - current docs,
  generated snapshots and historical notes.
- [Active refactor plan](https://github.com/if-uri/urirun/blob/main/docs/ACTIVE_REFACTOR_PLAN.md) -
  authoritative implementation refactor order for slim-core, connectors,
  services, flow and host/node autonomy.
- [Quality and docs audit 2026-06-29](quality-and-docs-audit-2026-06-29.md) -
  current quality, stale-docs and semcod-tooling audit.
- [Work summary 2026-06-20](work-summary-2026-06-20.md) - historical
  cross-repository status for `urirun`, connectors, ifURI App and examples.
- [Naming](naming.md) - what uses `urirun` and how the repository namespace
  migrated.
- [Commands](commands.md) - CLI commands and versioned entry points.
- [Registry and bindings](registry-and-bindings.md) - how bindings become a
  dispatchable registry.
- [Connectors](connectors.md) - installable URI packages, the public hub,
  catalog manifests, package shape and trust model.
- [Connector authoring](connector-authoring.md) - build a connector with
  `urirun.connector(...)` and export registry-ready bindings.
- [Generating connectors](generating-connectors.md) - from a command, a service
  or a Docker artifact, and the same contract in Python, JS, Go and PHP.
- [Transports](transports.md) - local functions, shell, Docker, HTTP, gRPC,
  browser, MCP, and A2A.
- [MCP and A2A](mcp.md) - how the same registry becomes LLM-callable tools and
  agent cards.
- [Error reference](errors.md) - standardized error categories (gRPC/RFC),
  `error://` addresses, fix hints and error-to-ticket.
- [Host and node on a LAN](host-node-lan.md) - operator guide for host/node
  communication and flow routing across a local network.
- [Node types and connections](node-types.md) - current node types from the
  host registry (`server`, `pc`, `rdp`, `smartphone`, browser plugin/debug
  modes, `webpage`, `api`, `device`) and their aliases.
- [Security and policy](security-and-policy.md) - default-deny execution, where
  restrictions are set, and how to read a node's live policy.
- [noVNC LAN demo](novnc-demo.md) - URI commands drive real Chromium browsers
  inside noVNC desktops across the LAN.
- [Project structure audit](project-structure-audit-2026-06-20.md) -
  historical repository map, runtime boundary and refactor/test priorities.
- [Logo](logo.md) - generated SVG logo assets and usage notes.
- [Roadmap](roadmap.md) - user-facing usability TODOs; implementation
  refactors live in the active refactor plan above.
- [Release checklist](release-checklist.md) - coordinated release steps across
  runtime, connectors, examples and app docs.

## Current recommendation

Use v2 for new projects:

```bash
pip install "urirun>=0.4.190"
urirun scan ./project --out generated/bindings.v2.json --registry-out generated/registry.json
urirun list generated/registry.json
```

Keep v1 only for older examples that depend on the first parameter-binding
contract.

For ready-made capabilities, install connector packages from the public hub:

```bash
curl -fsSL 'https://connect.ifuri.com/install?connectors=http-check' | bash
```

Or preview the generated install command without changing the environment:

```bash
urirun connectors install http-check
```
