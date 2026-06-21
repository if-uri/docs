# Repository & documentation standard

Every repository in the ifURI / urirun ecosystem follows one documentation
standard so that any project is predictable to pick up, and drift is caught
automatically by `make docs-lint`.

## Required files

| File | Purpose |
| --- | --- |
| `README.md` | What the project is, how to install/run it, links, license. ≥ 20 lines. |
| `CHANGELOG.md` | [Keep a Changelog](https://keepachangelog.com) format — a `## [version]` heading per release. |
| `VERSION` | A single [SemVer](https://semver.org) line (e.g. `0.1.0`). |
| `LICENSE` | The project licence — **Apache-2.0** across the ecosystem. Pure website repos may omit it (a site is content, not a licensed library). |
| `NOTICE` | Attribution required by Apache-2.0. Canonical line: `Copyright 2026 ifuri.com / Tom Sapletta - tom.sapletta.com`. |
| `CONTRIBUTING.md` | How to contribute; points back to this standard. |
| `TODO.md` | Recommended — the live backlog. |

The `LICENSE` text stays verbatim Apache-2.0; the copyright owner lives in `NOTICE`
(and in source headers as `# Author: Tom Sapletta · https://tom.sapletta.com`).

## README sections

A README should cover, in order: a `#` title, a one-paragraph description, an
**Install / Usage** block, a **Development** block (`make` targets), **Links** to
the rest of the ecosystem, and a **License** line.

## Connector repos

`urirun-connector-*` repos additionally:

- document their `scheme://` URI routes in the README (a table of URI → operation);
- link their hub page `connect.ifuri.com/connectors/<id>`;
- emit the `urirun.bindings.v2` contract (validated with `urirun validate`).

Scaffold a new one with `make new-connector ID=…` in `if-uri/connect.ifuri.com`.

## Enforcement

From `if-uri/ifuri-com`:

```bash
make docs-lint                 # lint every sibling repo
bash scripts/docs-lint.sh urirun-connector-hash docs   # specific repos
STRICT=1 make docs-lint        # also flag a missing TODO.md
```

`docs-lint` reports `N/M repo(s) conform` and exits non-zero on any gap, so it can
gate CI. It is the executable form of this page — if the two disagree, fix both.
