# Documentation source of truth

This page separates authoritative docs from generated snapshots and historical
notes. Use it before changing architecture, package boundaries, connector
contracts, or autonomous host/node behavior.

## Authoritative Docs

These files describe current behavior and should be kept in sync with code:

- `docs/index.md`, `docs/README.md` and `docs/architecture.md` - public
  documentation entry points and current ecosystem architecture.
- `docs/quality-and-docs-audit-2026-06-29.md` - current cross-repository
  quality, stale-documentation and semcod-tooling audit.
- `docs/getting-started.md`, `docs/commands.md`,
  `docs/registry-and-bindings.md` - runtime and registry basics.
- `docs/connectors.md`, `docs/connector-authoring.md`,
  `docs/generating-connectors.md` - connector package shape and discovery.
- `urirun/README.md` - current local CLI and host/node operator guide.
- `urirun/docs/ARCHITECTURE.md` - current implementation architecture for the
  runtime hub, contracts, router, flow, services, widgets, artifacts,
  connectors and nodes.
- `urirun/docs/ACTIVE_REFACTOR_PLAN.md` - execution order for the current
  slimming and extraction work.
- `urirun/docs/HOST_DASHBOARD_CHAT.md` - chat dashboard request lifecycle,
  target resolution, deterministic intents, recovery and service behavior.
- `urirun/docs/URIRUN_PACKAGE_SPLIT_PLAN.md` - the current target is slim-core:
  `urirun` owns only the minimal URI kernel and CLI, while contracts,
  connectors, services, flow, node, widgets and artifacts own their code outside
  core. The current part includes the "Docelowy Model Slim-Core" and
  "Reguły Ekstrakcji" sections; sections beginning with "Cel (historyczny)" are
  historical context.
- `urirun-contract/ARCHITECTURE.md` - contract kernel architecture, fleet
  coverage, compatibility gates and contract roadmap.
- `URI_ECOSYSTEM_ATOMIZATION_AUDIT.md` - 2026-06-28 atomization snapshot. Use
  it as predecessor context; the 2026-06-29 quality audit supersedes it for
  documentation freshness and semcod-tooling status.
- `docs/autonomous-work-unblock-status-2026-07-08.md` - `/work` repeated-unblock
  issue status and fix plan.
- `docs/signal-kvm-llm-proxy-refactor-2026-07-09.md` - Signal composer focus
  (IFURI-237), `llm-urirun-com` proxy, API adapters, E2E results and refactor
  plan (operational status until modules are extracted per that plan).
- `HUMAN-ACTIONS.md` - the current human action checklist for the autonomy
  frontier (secrets, node enrollment, policy grants); kept in sync with open
  `waiting:*` tickets.
- `todo.md` - the current if-uri hub TODO; connector/SDK backlog items are
  checked off against repo state, not left as aspirational.

## Generated Snapshots

These files are useful evidence, not source documentation. Regenerate them
before using them for decisions:

- `*/project/map.toon.yaml`, `*/project/context.md`,
  `*/project/analysis.toon.yaml`, `*/project/planfile-tickets.yaml`.
- `SUMD.md`, `SUMR.md`, `code2llm_output/`.
- `.nlp2dsl/registry/environment.yaml`.
- generated Mermaid/PNG files under `project/`.

Do not treat generated README files under `project/` as current architecture.
They can contain empty headings, old tasks, or stale symbol references.

## Historical Docs

These files can explain why a decision was made, but they are not the current
operational contract:

- `docs/work-summary-*`.
- `docs/project-structure-audit-*`.
- `docs/todo-consolidation-audit-2026-07-08.md` - point-in-time review of
  every `TODO.md` in the hub (IFURI-208); the `repo-standards.md` TODO.md row
  is the current rule it produced.
- `URIRUN_CONTRACT_REFACTORING_REPORT.md`.
- `CAMERA-KSEF-PIPELINE-REPORT.md` - 2026-06-24 session index for the
  camera/USB/OCR to KSeF invoice pipeline; the connectors and examples it
  lists are current, the report itself is a point-in-time index, not living
  documentation.
- `RETROSPECTIVE.md` - 2026-06-24 lessons-learned pass; several of its "top 5"
  items are already marked done in the file itself and should be checked
  against current code before being cited as open work.
- `urirun/docs/RELEASE-extracted-packages.md`.
- old `CHANGELOG.md` sections and generated release fragments.
- lower historical sections of `urirun/docs/URIRUN_PACKAGE_SPLIT_PLAN.md`.

When a historical doc contradicts an authoritative doc, the authoritative doc
wins.

## Validation Rules

- Run `docval` against source docs, excluding generated snapshots:
  `project/`, `SUMD.md`, `SUMR.md`, `code2llm_output/`, generated images and
  generated ticket files.
- Run `code2llm` to refresh maps before using hotspot or package-boundary
  claims.
- Run `env2llm` before autonomy tests so the planner sees live CDP/KVM/LLM/node
  availability.
- Run `urirun-contract` fleet coverage before accepting connector changes:
  mutating routes need contracts unless they are explicitly classified.
- Keep service docs (`urirun-service-chat`, `urirun-service-scanner`) aligned
  with service manifests and `/api/uri/invoke` restart behavior.

## Update Policy

If a package changes from a meta-package to a real extracted package, update the
package README, `urirun/docs/URIRUN_PACKAGE_SPLIT_PLAN.md`, and this page in the
same change. If code moves out of `urirun`, add an import-boundary test so core
does not import the extracted implementation back. If a connector starts
exposing URI routes, add or update its `contracts.json` and test it with
`urirun_contract.gate.conform`.
