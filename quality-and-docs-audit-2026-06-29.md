# Quality and docs audit - 2026-06-29

This audit answers two questions:

- which docs no longer reflect the current application state;
- how to use the local `~/github/semcod/*` Python packages to improve quality
  in `if-uri` without adding another manual review process.

## Inputs

Commands run from `/home/tom/github/if-uri`:

```bash
PYTHONPATH=/home/tom/github/semcod/env2llm/src \
  python3 -m env2llm.cli . --project-id if-uri --format yaml --no-merge

PYTHONPATH=/home/tom/github/semcod/docval/src \
  python3 -m docval.cli scan docs --project .

PYTHONPATH=/home/tom/github/semcod/docval/src \
  python3 -m docval.cli scan urirun/docs --project .

PYTHONPATH=/home/tom/github/semcod/redup/src \
  python3 -m redup.cli_app.main compare \
    urirun/adapters/python/urirun_scanner urirun-connector-scanner \
    --no-community --min-lines 8

python3 codebase_audit.py --root . --list --json
```

## Current state

The core architecture is mostly aligned with the current refactor direction:

- `urirun/docs/ARCHITECTURE.md`, `COMPONENTS.md`,
  `AUTONOMY_ARCHITECTURE.md`, `EXPERIENCE_RETRIEVAL.md` and
  `ACTIVE_REFACTOR_PLAN.md` are the strongest current architecture docs.
- `urirun-flow` is the real-source owner of `urirun_flow`; hub paths under
  `urirun.node.flow*` are compatibility shims.
- `urirun-connector-router` owns URI routing and target diagnosis, including
  `router://host/target/query/diagnose`.
- `urirun-connector-twin` owns inventory, experience retrieval and flow recall
  surfaces; chat consumes those typed routes instead of owning the retrieval
  kernel.
- `urirun_runtime.v2` is now mostly runtime core, with CLI command handlers
  split into `urirun_runtime.v2_cmds`.

Measured health:

- `docval docs`: 33 files, 97% valid (214/221 chunks). Remaining issues are
  task markers and two orphaned marker sections, not semantic invalidity.
- `docval urirun/docs`: 18 files, 99% valid (258/260 chunks). Remaining issues
  are the intentional task markers in `REFACTOR_ROADMAP.md`.
- `env2llm` generated `.nlp2dsl/registry/environment.yaml` with live host
  capability facts. It reports host `nvidia`, Linux kernel `6.17.0-40`,
  desktop tools including `ydotool`, `grim` and `scrot`, TestQL scenarios, ports
  and runtime capability flags.
- `codebase_audit`: 17 findings total, grouped as `hardcoded: 7` and
  `orchestration: 10`; severities are `{5: 5, 6: 7, 7: 5}`. No current
  top-level findings for contract gaps, layering or duplicate kernels.
- `redup` comparison between adapter scanner fallback and
  `urirun-connector-scanner`: 203 cross matches and 3626 potential shared LOC.
  This is the largest remaining single-source risk.

## Docs that need correction or reclassification

| File or area | Problem | Action |
| --- | --- | --- |
| `docs/index.md`, `docs/README.md` | still call 2026-06-20 work summary and structure audit "current" | point readers to this audit and call old summaries historical |
| `URI_ECOSYSTEM_ATOMIZATION_AUDIT.md` | good 2026-06-28 snapshot, but several numbers are now older than the current split | keep as historical predecessor; this file supersedes it for quality/doc status |
| `URIRUN_CONTRACT_REFACTORING_REPORT.md` | dated report with live-run assertions and old coverage numbers | keep as historical evidence; current AS-IS lives in the newer architecture and refactor-plan docs |
| `human-connector/memory/ifuri-contract-layer-state.md` | says production twin still uses a hard-coded reversibility table and fleet coverage is only about 3/40; current docs and tests show later state | mark as historical memory or refresh from `ACTIVE_REFACTOR_PLAN.md` |
| `urirun/docs/URIRUN_PACKAGE_SPLIT_PLAN.md` | top status block still contains historical details such as `runtime/v2.py 2593 -> ~1970` and handlers staying in v2, while current code uses `v2_cmds` and `v2.py` is about 1658 lines | rewrite the dated decomposition block or move it under an explicit "historical 2026-06-23" section |
| `project/*`, `urirun/project/*`, `*/project/*`, `code2llm_output/*` | generated maps are useful evidence but contain stale symbol references after refactors | never cite them without rerunning `code2llm`; exclude from doc source-of-truth |
| docs/examples with `192.168.188.*`, `lenovo`, fixed ports | many are lab fixtures, but they read like operational defaults | convert production docs to placeholders/env vars; keep concrete LAN values only in clearly named fixture examples |
| connector/service READMEs generated from templates | several still describe package shape rather than current ownership, contracts and service manifests | regenerate or patch per package after ownership changes |

## Code quality front

The next refactors should not target line count alone. The active risks are:

1. **Scanner real-source drift.** `redup` found heavy overlap between
   `urirun/adapters/python/urirun_scanner` and `urirun-connector-scanner`.
   Decide whether the connector package is the real source and turn the adapter
   copy into a shim/fallback import, then add a single-source gate.
2. **Hardcoded environment facts.** The remaining `codebase_audit` findings are
   mostly absolute home paths, private LAN IPs, node aliases, model literals and
   service ports. Production decisions should use inventory/config/memory or an
   explicit payload; examples should label fixtures.
3. **Large orchestration modules.** Highest current modules:
   `urirun-connector-smart-crop/core.py`, `urirun-flow/flow_planner.py`,
   `host/host_dashboard.py`, `camera/core.py`, `kvm/backends.py`,
   scanner document/bridge modules, `chat_orchestrator.py` and
   `urirun_runtime/v2.py`. The right extraction unit is a typed URI capability,
   contract, service or twin query, not a prettier helper split.
4. **Documentation freshness.** `docval` is green enough for a gate, but only if
   generated snapshots are excluded and historical docs are labeled.

## Semcod tools to adopt

| Tool | Use in `if-uri` | Gate shape |
| --- | --- | --- |
| `env2llm` | generate live environment facts before autonomy tests and route/twin diagnosis | write `.nlp2dsl/registry/environment.yaml`; compare key facts with Twin inventory |
| `docval` | scan Markdown source docs for empty/orphan/task-marker sections | run on `docs` and `urirun/docs`; exclude generated folders |
| `redup` | detect cross-package real-source drift | compare known risky pairs: scanner fallback vs connector, widget renderers, router shims, flow shims |
| `code2llm` | regenerate code maps before using hotspot claims | update generated `project/map.toon.yaml` only as evidence, never hand-edit |
| `pyqual` | orchestrate repeated audit/test/report loops | add `pyqual.yaml` later, after docval/redup/env2llm commands are stable |
| `nlp2uri` | convert NL examples into URI-plan golden corpora | feed `testing/` and `examples/44-chat-prompt-sweep` |
| `prefact` | catch import and refactor hazards before/after large code moves | run on touched Python packages in extraction PRs |
| `planfile` | turn audit output into tracked tasks | sync this audit into refactor tickets once priorities are accepted |

## Proposed next refactor order

1. **Docs source-of-truth patch.** Update `docs/index.md`, `docs/README.md` and
   `docs/source-of-truth.md` so 2026-06-20/28 reports are no longer labeled
   "current" when this audit supersedes them.
2. **Scanner single-source decision.** Make `urirun-connector-scanner` the
   source of truth or explicitly document why the adapter fallback remains a
   second implementation. If it remains, add a `redup` ratchet.
3. **Hardcoded environment burn-down.** Split audit findings into fixtures vs
   production. Production occurrences move to config/inventory/env-domain
   resolution; fixture occurrences get comments or example-local env defaults.
4. **Package docs refresh.** For packages already extracted
   (`urirun-flow`, `urirun-connector-router`, `urirun-connector-twin`,
   services, widgets, artifacts), update README/architecture docs after each
   ownership change.
5. **CI quality target.** Add a lightweight `make docs-quality` or
   `scripts/docs_quality_audit.sh` that runs `docval`, `env2llm`, selected
   `redup` comparisons and `codebase_audit --list --json`.

## Acceptance criteria

- `docval docs` and `docval urirun/docs` stay above 95% after excluding
  generated snapshots and archiving empty task-heavy fragments.
- `codebase_audit` has no severity 7 production hardcoded findings.
- scanner fallback/connector drift is either removed or guarded by a failing
  single-source/redup ratchet.
- all docs that mention concrete LAN nodes explain whether they are examples,
  fixtures or live operator configuration.
- every generated code map used in a review includes the command and timestamp
  that produced it.
