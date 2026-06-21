# ifURI / urirun work summary — 2026-06-21 (urirun 0.4)

What shipped to `main` since the v0.3.14 tag — the surface of the upcoming
**urirun 0.4** release. This continues the [2026-06-20 summary](work-summary-2026-06-20.html).

## Runtime (`urirun`)

- **`error://` engine** on nodes: standardized error codes mapped to established
  standards (gRPC status, POSIX errno, HTTP, RFC 9457 Problem Details), a
  `@capture` decorator, an `/errors` route and deep links to
  [docs.ifuri.com/errors](errors.html). Errors become searchable, ticketable URIs.
- **Param-aware routing**: templated mid-path segments like
  `kvm://{host}/monitor/{monitor}/query/screenshot` now resolve from a concrete URI
  and bind the value to the handler; exact matches still take priority.
- **`adopt-pack`** — the adoption moat (see below), a first-class `urirun adopt-pack`
  command.
- **Connector SDKs in 9 more languages** (Go, PHP, Ruby, Perl, Bash, Rust,
  TypeScript, Java, C#) beside Python/JS, kept in lockstep by a conformance check
  that compares each language's emitted `bindings.v2` and runs a functional pass.
- **IFURI-007**: the runtime was split into `urirun.runtime.*` with `host` and
  `connector` subpackages and back-compat shims.
- **Release tooling**: `make release-bump V=X.Y.Z` unifies all five version files;
  versions reconciled and locked at **0.4.0**.

## Adopt any package as URI (the moat)

> Give an existing application a URI surface with the least possible change — see
> [docs.ifuri.com/adopt-as-uri](adopt-as-uri.html).

Three paths, zero-to-minimal change: (1) **zero change** — `console_scripts`/`bin`
become `cli://` routes; (2) **manifest bridge** — a capability manifest maps 1:1 to
`bindings.v2`; (3) **one config block** — `[tool.urirun]` in `pyproject.toml` or a
`"urirun"` key in `package.json`. Installed packs are discovered *without importing
them*, so a pack's own dependencies need not be present to adopt its URI surface.

Proven against the tellmesh capability packs unchanged: **18 packs adopted into one
registry, 113 of 116 routes dispatch** through the runtime, **20+ packs fully green**.
A runnable cross-pack flow (screen → OCR/VQL → LLM → alert) ships as
[examples 11](https://examples.ifuri.com/), and **14 packs are listed on
[connect.ifuri.com](https://connect.ifuri.com)**.

## Ecosystem & process

- **Documentation standard** ([repo-standards](repo-standards.html)) enforced by
  `make docs-lint` and a per-repo CI workflow — 31/31 repos conform.
- **One-command deploy**: `make deploy-all` ships every web property sequentially;
  `get-*`/site repos run post-deploy download-and-run tests.
- **Property split**: `urirun.com` (runtime site) and `get.urirun.com` (node/host
  installer) were extracted; `get.ifuri.com` became the **app** download and
  301-redirects `/node.sh` to get.urirun.com. The shared ecobar links `urirun.com`.
- **Licensing**: Apache-2.0 ecosystem-wide with a canonical `NOTICE`
  (`Copyright 2026 ifuri.com / Tom Sapletta`); visible copyright footers on all sites.

## Gating the release

- `make test` must be green. The one red test (`test_compat::…compat_report`) is a
  setup issue in the IFURI-007/008 compat tracking — `compat_report["ok"]` should
  distinguish "extracted connector not installed" (expected) from "incompatible"
  (a real fail), so the suite is green without each extracted connector installed.
- Then: tag `v0.4.0` → `apply-release-pins.sh v0.4.0` (27 pins) → redeploy
  get.urirun.com + docs. Until the pins move, this work stays dark to installed
  nodes and the app, which still pin v0.3.14.
