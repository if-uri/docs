# ifURI / urirun work summary - 2026-06-20

This note summarizes the current cross-repository state after the latest
`urirun`, connector, app and examples work.

## Completed

- Standardized the public runtime name around `urirun`, while keeping historical
  GitHub references to `tellmesh/urirun`.
- Added the preferred Python authoring style with `@urirun.command(...)`,
  `@urirun.shell(...)` and `urirun.connector(...)`, so connector packages can
  declare routes once and export registry-ready bindings.
- Split the ecosystem direction into a small runtime core plus installable
  connector packages, a public connector hub and the ifURI host/app layer.
- Built the PHP connector hub at `connect.ifuri.com` with connector pages,
  machine-readable manifests, search index, sitemap, `llms.txt` and one-line
  installers.
- Added and verified connector packages for HTTP checks, time tools and browser
  control, including registry generation and MCP/A2A projection checks.
- Documented the user bootstrap path across `get.ifuri.com`, `ifuri.com`,
  `connect.ifuri.com`, `if-uri/examples` and the individual connector
  repositories.
- Integrated `urirun` concepts into the ifURI app through CLI/API runtime
  commands, task planning documentation and desktop GUI work.
- Improved the ifURI desktop service table layout so long URI routes stay
  readable in the GUI.
- Expanded `if-uri/examples` into numbered examples from JSON bindings through
  decorators, artifact scanning, transports, Docker flows, device mesh, full E2E
  and simple defaults.
- Rebuilt `11-novnc_lan_flow` as a full Docker/noVNC demo where URI commands
  execute inside virtual desktops rather than on the host machine.
- Added a four-computer noVNC URI scenario:
  - `pc1` exposes notes routes,
  - `pc2` exposes orders routes,
  - `pc3` exposes reports routes,
  - `pc4` exposes monitor routes,
  - all machines expose `browser://` screenshot/open routes and `log://` routes.
- Added CI coverage in `if-uri/examples` for the four-computer noVNC flow.

## Verified

The latest noVNC example was verified with:

```bash
python3 -m py_compile computer/browser_node.py orchestrator/run_flow.py
make test
make test-full
docker compose config
python3 -m json.tool generated/registry.json
```

`make test-full` produced:

```json
{
  "ok": true,
  "mode": "full",
  "steps": 16,
  "routes": 24,
  "screenshots": [
    "pc1-example.png",
    "pc2-ifuri.png",
    "pc3-example-org.png",
    "pc4-example-net.png"
  ]
}
```

The ifURI desktop GUI work was verified earlier with focused GUI smoke tests and
the full non-e2e pytest suite in `if-uri/app`.

## Important repositories

- Runtime core: [tellmesh/urirun](https://github.com/tellmesh/urirun)
- App/host UI: [if-uri/app](https://github.com/if-uri/app)
- Public docs: [if-uri/docs](https://github.com/if-uri/docs)
- Examples: [if-uri/examples](https://github.com/if-uri/examples)
- Connector hub: [if-uri/connect.ifuri.com](https://github.com/if-uri/connect.ifuri.com)
- Installer site: [if-uri/get](https://github.com/if-uri/get)
- Project website: [if-uri/ifuri-com](https://github.com/if-uri/ifuri-com)
- Roadmap site: [if-uri/roadmap](https://github.com/if-uri/roadmap)
- Marketing operations: [if-uri/marketing](https://github.com/if-uri/marketing)
- Brand assets: [if-uri/logo](https://github.com/if-uri/logo)
- HTTP connector: [if-uri/urirun-connector-http-check](https://github.com/if-uri/urirun-connector-http-check)
- Time connector: [if-uri/urirun-connector-time-tools](https://github.com/if-uri/urirun-connector-time-tools)
- Browser connector: [if-uri/urirun-connector-browser-control](https://github.com/if-uri/urirun-connector-browser-control)

## Documentation files updated

- `if-uri/docs`: summary, index, README, TODO and changelog.
- `if-uri/examples`: README, TODO and changelog plus the `11-novnc_lan_flow`
  Docker/noVNC documentation.
- `if-uri/app`: README, TODO and changelog for app/host follow-up work.
- `tellmesh/urirun`: README, TODO and changelog with current `v0.3.14` install
  examples and runtime/core boundary tasks.
- `if-uri/connect.ifuri.com`: README, TODO and changelog for connector hub work.
- `if-uri/get`: README, TODO and changelog for node bootstrap work.
- `if-uri/ifuri-com`: README, TODO and changelog for public website work.
- `if-uri/roadmap`: README, TODO and changelog for roadmap site work.
- `if-uri/marketing`: README, TODO and changelog for outreach operations.
- `if-uri/logo`: README, TODO and changelog for brand package work.
- Connector packages: README/TODO/CHANGELOG links for HTTP check, time tools and
  browser control.

## Remaining work

- Move host/app-specific modules out of the runtime core when the package split
  is ready.
- Add stable connector discovery/list/install commands to `urirun` itself.
- Make the noVNC scenario launchable from ifURI App, not only from Make/Docker.
- Add browser-level UI tests for the noVNC dashboard once Playwright browsers
  are installed in CI.
- Pin Docker image tags in heavy examples for reproducible CI runs.
- Keep connector manifests, hub catalog entries and package versions synchronized
  through CI.
