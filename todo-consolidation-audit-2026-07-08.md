# TODO.md consolidation audit — 2026-07-08 (IFURI-208)

Review of every `TODO.md` in the `if-uri` hub, prompted by the recurring
`[NXDO] Review and Consolidate TODO.md Files` housekeeping ticket. Answers one
question: is `TODO.md` being used consistently across the ecosystem, and if
not, what should change.

## Inputs

Commands run from `/home/tom/github/if-uri`:

```bash
find . -maxdepth 2 -iname "TODO.md" -not -path "*/node_modules/*" \
  -not -path "*/.claude/*" -not -path "*/.work/*"

# per-file open/done checkbox counts
grep -c '^\s*- \[ \]' <file>; grep -c '^\s*- \[x\]' <file>

# ecosystem-wide conformance, from if-uri/ifuri-com
STRICT=1 bash scripts/docs-lint.sh
```

## Finding: two unrelated things share the filename `TODO.md`

**Hand-curated backlog TODO.md** (31 repos, e.g. `todo.md`, `docs/TODO.md`,
`roadmap/TODO.md`, `get-ifuri-com/TODO.md`, most `urirun-connector-*`
repos with a TODO.md) — short, prose, `[x]` items carry evidence
(commit/file reference), matches the `repo-standards.md` definition of
"the live backlog." `todo.md` and `roadmap/TODO.md` already carry dated
review headers (IFURI-157, IFURI-217) and are current.

**`prefact`-generated lint-issue dumps** — machine-written, unrelated to
backlog planning:

| Repo | Generated | Header claims | Checkbox lines in file |
| --- | --- | --- | --- |
| `urirun/TODO.md` | 2026-07-05 | 711 active, 56 completed | 256 (200 open + 56 done) |
| `examples/TODO.md` | 2026-06-21 | 320 active, 0 completed | 200 |
| `app/TODO.md` | 2026-06-21 | 269 active, 128 completed | 200 open + 100 done shown |
| `urivision/TODO.md` | 2026-07-05 | 223 active, 6 completed | 200 + 6 |
| `urirun-connector-kvm/TODO.md` | 2026-06-27 | 170 active, 6 completed | 170 + 6 |
| `urirun-connector-twin/TODO.md` | 2026-06-27 | 88 active, 0 completed | 88 |
| `urirun-contract-windowpair/TODO.md` | 2026-06-27 | — | 34 + 9 |
| `relcom/TODO.md` | 2026-07-08 | 0 active, 0 completed | 0 |

Two problems follow from treating these as the backlog:

- **Truncation is silent.** `urirun/TODO.md` header says 711 active issues
  exist, but the file only lists 200 — someone reading the file (not the
  header) undercounts open work by 511 items with no "...and N more" marker.
- **Staleness is invisible.** `examples/TODO.md` and `app/TODO.md` are
  regenerated snapshots from 2026-06-21 (17 days stale as of this audit) with
  no dated review note the way the hand-curated files have; a reader can't
  tell whether it reflects current code without re-running `prefact`.

These are linter output, not planning documents — useful for
`prefact -a --execute-todos`, not for "what should this repo work on next."

## Finding: `docs-lint --strict` TODO.md gap is large and pre-existing

`STRICT=1 bash scripts/docs-lint.sh` (ifuri-com) reports **31/132 repos
conform**, **101 need work**, of which **92/132 lack a `TODO.md` at all**.
This gap predates this audit and spans the whole `urirun-connector-*` and
`urirun-*` fleet (most connectors extracted since the ~60-repo split have no
`TODO.md`). Bulk-creating 92 placeholder files is out of scope for a single
consolidation pass — it would produce empty boilerplate, not a live backlog,
which is the opposite of what `repo-standards.md` asks for. Tracked as
follow-up, not fixed here.

## Action taken

- `docs/repo-standards.md`: the `TODO.md` row now distinguishes the live
  backlog from `prefact`-generated lint dumps, so `docs-lint --strict`
  passing on a repo doesn't get read as "has a maintained backlog."
- `docs/source-of-truth.md`: this audit added under Historical Docs, as a
  point-in-time snapshot (same pattern as the 2026-06-29 quality audit).
- No content changes to the 31 hand-curated `TODO.md` files: the hub-level
  `todo.md` and `docs/TODO.md`/`roadmap/TODO.md` were already reviewed
  against repo state (IFURI-157, IFURI-217) and are current; the rest are
  short and per-repo-scoped, not duplicated across files.

## Not done in this pass

- Regenerating the 8 `prefact` snapshots (owned by `prefact`, not by hand).
- Creating `TODO.md` for the 92 repos that lack one — needs a decision on
  whether every extracted connector should carry a backlog file, not a
  mechanical fix.
