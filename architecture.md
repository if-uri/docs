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
  -> router diagnosis and plan acceptance
  -> node, service or connector execution
  -> contract-shaped result
  -> verification, artifact/widget/log
  -> recovery nextIntent on failure
```

Before an autonomous action runs, `urirun-connector-router` should know whether
the route runs on the host, a selected `node:*`, a `service:*`, or is blocked by
a missing connector, unreachable transport or unsafe command. The router exposes
both `plan/query/diagnose` and `plan/query/accept`: LLM, recall or heuristics may
propose candidate flows, but the same deterministic acceptance gate decides
whether a plan can execute.

Desktop environment analysis is part of the pre-action path. For screenshot and
UI prompts the system grounds the plan in `display/query/info`,
`env/query/profile`, `twin://*/env/query/inventory`, route ownership and Digital
Twin memory. Contracts can declare env-enum domains such as
`monitor -> env:monitors.id`; the flow selection gate resolves explicit values,
single-option defaults, fingerprint-keyed preferences, or emits typed
`needs-selection`. On GNOME/Wayland multi-monitor hosts, KVM captures all
monitors through Mutter `RecordArea` and returns monitor metadata plus the
captured image dimensions, so the chat artifact describes the actual surface.

## URI as the stable contract boundary

ifURI has two translations around the same URI:

- **contract -> code**: `contracts.json` and bindings generate handler
  signatures, JSON Schema, SDK/MCP/A2A surfaces and lint gates;
- **query/command -> runtime -> JSON**: a flow step is routed to `runsOn`,
  executed through an adapter, and returned as a portable JSON envelope.

The contract is the shared invariant across both translations. A URI such as
`kvm://host/cdp/page/command/navigate` is not only an RPC name: the same contract
guards generated code, effect class (`query` vs `command`), optional inverse and
the wire envelope returned by host, node or service execution.

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
- Autonomy architecture:
  [if-uri/urirun docs/AUTONOMY_ARCHITECTURE.md](https://github.com/if-uri/urirun/blob/main/docs/AUTONOMY_ARCHITECTURE.md)
- Component boundaries:
  [if-uri/urirun docs/COMPONENTS.md](https://github.com/if-uri/urirun/blob/main/docs/COMPONENTS.md)
- URI object model:
  [if-uri/urirun docs/URI_OBJECTS.md](https://github.com/if-uri/urirun/blob/main/docs/URI_OBJECTS.md)
- Active refactor plan:
  [if-uri/urirun docs/ACTIVE_REFACTOR_PLAN.md](https://github.com/if-uri/urirun/blob/main/docs/ACTIVE_REFACTOR_PLAN.md)
