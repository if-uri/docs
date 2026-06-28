# Current architecture

Status: 2026-06-28.

This page is the public map of the ifURI / urirun system. The detailed
implementation architecture lives in
[if-uri/urirun docs/ARCHITECTURE.md](https://github.com/if-uri/urirun/blob/main/docs/ARCHITECTURE.md).

## System shape

`urirun` is the small URI runtime. It accepts a URI, a registry-backed command,
or a natural-language flow, diagnoses where every step can run, executes through
the correct transport, and returns a portable JSON result.

The current architecture is split into installable owners:

| Owner | Responsibility |
| --- | --- |
| `urirun` | lightweight hub runtime, CLI, policy, registry discovery and compatibility shims |
| `urirun-contract` | route contracts, effect class, reversibility, JSON Schema, TypeScript and conformance gates |
| `urirun-connector-router` | pre-dispatch routing diagnosis for host, node and service targets |
| `urirun-flow` | flow model, planner normalization, thin driver, verification, rollback and recovery |
| `urirun-connector-*` | domain capabilities such as `kvm://`, `fs://`, `ocr://`, `llm://`, `github://` |
| `urirun-service-*` | long-running applications such as chat/dashboard, scanner and android/webpage node |
| `urirun-widgets` | live widget render helpers, service views and HTML/SVG/JS widget surfaces |
| `urirun-artifacts` | artifact URI surface and descriptors for final files/results |
| `urirun-node` | node/mesh package boundary; currently a meta-package while the real source is still being split |

The rule is one source of truth per kernel. Old import paths can remain as
compatibility shims, but they should re-export the owning package instead of
shipping a second implementation.

## Execution path

```text
prompt / CLI / API
  -> route registry and target selection
  -> flow planning or loaded flow
  -> router diagnosis
  -> node, service or connector execution
  -> contract-shaped result
  -> verification, artifact/widget/log
  -> recovery nextIntent on failure
```

Before an autonomous action runs, `urirun-connector-router` should know whether
the route runs on the host, a selected `node:*`, a `service:*`, or is blocked by
a missing connector, unreachable transport or unsafe command.

## Object model

- **Host** - local coordination center: registry, dashboard, chat, dispatch,
  object registry, logs and artifact registration.
- **Node** - controlled runtime such as a PC, server, browser, phone, API or
  device. Classic nodes expose `/health`, `/routes`, `/run`, `/events` and
  service metadata.
- **Service** - long-running application with lifecycle and state, for example
  `urirun-service-chat` or `urirun-service-scanner`.
- **Connector** - small package that owns one URI capability domain and exposes
  routes through `urirun.bindings`.
- **Contract** - declared route behavior: input/output shape, effect,
  reversibility and examples. Mutating autonomous routes should ship contracts.
- **Widget** - live view/control surface. Widgets are not files.
- **Artifact** - finished immutable output such as a PDF, screenshot, OCR JSON,
  CSV or report.

## Current refactor direction

The hub is being reduced to the minimal runtime and compatibility layer. New
work should move domain behavior into connector packages, long-running UI/process
behavior into service packages, live rendering into `urirun-widgets`, and route
behavior into `urirun-contract`.

Immediate architectural risks:

- publish `urirun-connector-router` and `urirun-widgets` before the next hub
  release, because the hub now depends on them;
- continue extracting service-chat/node code without moving all of `urirun.host`
  into a new monolith;
- keep examples as acceptance tests through the same router and contract path as
  production.

## More detail

- Runtime architecture:
  [if-uri/urirun docs/ARCHITECTURE.md](https://github.com/if-uri/urirun/blob/main/docs/ARCHITECTURE.md)
- Component boundaries:
  [if-uri/urirun docs/COMPONENTS.md](https://github.com/if-uri/urirun/blob/main/docs/COMPONENTS.md)
- URI object model:
  [if-uri/urirun docs/URI_OBJECTS.md](https://github.com/if-uri/urirun/blob/main/docs/URI_OBJECTS.md)
- Active refactor plan:
  [if-uri/urirun docs/ACTIVE_REFACTOR_PLAN.md](https://github.com/if-uri/urirun/blob/main/docs/ACTIVE_REFACTOR_PLAN.md)
