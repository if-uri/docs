# noVNC LAN demo

A Docker demo where URI commands control **real Chromium browsers** running
inside virtual noVNC desktops. The browser opens inside the container, not on
the host, and a single URI flow drives several computers on the LAN through one
shared contract.

Source: [if-uri/examples/11-novnc_lan_flow](https://github.com/if-uri/examples/tree/main/11-novnc_lan_flow)

## What runs

- `pc1-browser`..`pc4-browser` - Selenium Chromium desktops with noVNC.
- `pc1-api`..`pc4-api` - small URI node APIs exposing `browser://`, `app://`
  and `log://`.
- `dashboard` - a browser view with noVNC iframes, logs and the last flow
  result.
- `orchestrator/run_flow.py` - sends a multi-step URI flow to the computers.

Optional `pc3` and `pc4` services start behind the Compose profile `full`.

## Run it

```bash
make up
```

Open the dashboard and the noVNC desktops:

```text
Dashboard: http://127.0.0.1:8192/?pc1NovncPort=7901&pc2NovncPort=7902&pc1ApiPort=9001&pc2ApiPort=9002
pc1 noVNC: http://127.0.0.1:7901/?autoconnect=1&resize=scale
pc2 noVNC: http://127.0.0.1:7902/?autoconnect=1&resize=scale
```

If those ports are busy, run the same demo on another set - the dashboard
accepts port overrides in the query string:

```bash
DASHBOARD_PORT=18192 \
PC1_NOVNC_PORT=17901 PC2_NOVNC_PORT=17902 \
PC1_API_PORT=19001 PC2_API_PORT=19002 \
make up
```

## The URI flow

```bash
make flow
```

The basic flow opens pages and captures screenshots through these URI commands:

```text
browser://pc1/page/command/open
browser://pc1/page/command/screenshot
browser://pc2/page/command/open
browser://pc2/page/command/screenshot
log://pc1/session/command/write
log://pc2/session/query/recent
```

Every computer is just another node on the `ifuri://` network: the same action
address works locally and remotely, and the audit log records the envelope,
payload, status, time and source of every call.

## Four-computer scenario

The full scenario starts four noVNC computers and gives each one a small local
service - `pc1` notes, `pc2` orders, `pc3` reports, `pc4` monitor - while every
machine also exposes `browser://` and `log://` routes. Run it with the `full`
Compose profile and verify with:

```bash
make test-full
```

A successful run reports `ok: true`, the step and route counts, and a screenshot
per computer.

## Related

- [Transports](transports.md) - how `browser://`, `shell://`, HTTP, gRPC, MCP
  and A2A map to the same registry.
- [Getting started](getting-started.md) - install `urirun`, scan a project and
  run a URI.
- Live web version: [ifuri.com/docs/novnc-demo.html](https://ifuri.com/docs/novnc-demo.html)
