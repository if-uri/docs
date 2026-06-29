# Node types and connection configuration

Every node exposes `URI` routes, but node types differ in **transport** and in **what
they can do**. Each type needs different knowledge, so each has its own connection
configuration. Pick the type that matches the machine or device.

The dashboard surfaces all of these under **Nodes → ➕ Dodaj node (wybierz typ
połączenia)**, and a live copy of this guide is served at `/docs/nodes`.

Originally this page documented six broad types. The current host registry uses
ten canonical node types and keeps the older names as aliases:

- `server`, `pc`, `rdp`, `smartphone`
- `browser-debug`, `browser-chrome-plugin`, `browser-firefox-plugin`
- `webpage`, `api`, `device`

Compatibility aliases include `browser` → `browser-debug` and `web` /
`webnode` → `webpage`.

| Type | Transport | Knowledge needed | Connector |
|------|-----------|------------------|-----------|
| 🖥️ server | shell / SSH | SSH, remote install | get-node + shell |
| 💻 pc | app + shell | desktop, terminal | get-node + kvm |
| 🪟 rdp | remote desktop (RDP) | RDP, Windows login | kvm / rdp |
| 📱 smartphone | web → APK/Termux | app install, LAN | android-node + adb |
| 🌐 browser-debug | DevTools (CDP) | launch with debug port | webnode / browser-control |
| 🧩 browser-chrome-plugin | Chrome extension | extension id, node URL | chrome-plugin |
| 🧩 browser-firefox-plugin | Firefox extension | extension id, node URL | firefox-plugin |
| 📄 webpage | HTML/JS page relay | android-node page or page bridge | webpage / webnode page scope |
| 🔌 api | HTTP/API endpoint | base URL, auth, optional OpenAPI | http-api / fetch / openapi |
| 🧩 device | multi-interface device | APIs/protocols, auth, capabilities | camera / rtsp / ssh / smb / mqtt |

---

## 🖥️ server — shell / SSH

Headless machine (VPS, server). Controlled over a shell; the urirun node is installed
remotely over SSH.

**You need:** SSH access (`user@host`), permission to install.

```bash
ssh user@HOST "curl -fsSL https://get.ifuri.com/node.sh | bash -s -- --name HOST --port 8765 --background"
```

Then save the node with URL `http://HOST:8765`. Test: `http://HOST:8765/health`.

## 💻 pc — application + shell

A machine with a GUI (laptop, desktop). You run the node locally (or via the ifURI
app), and add desktop control (the `kvm` connector: screenshot, keyboard, mouse).

```bash
curl -fsSL https://get.ifuri.com/node.sh | bash -s -- --name pc --port 8765 --background
```

Save the node with URL `http://PC-IP:8765`.

## 🪟 rdp — remote desktop

Windows/xrdp over RDP (port 3389). You connect to the desktop and control it; a urirun
node with the KVM connector runs on the desktop side.

**You need:** RDP host, login, an RDP client (e.g. `xfreerdp`).

```bash
xfreerdp /v:HOST:3389 /u:USER /p:PASS /cert:ignore
```

On the desktop, start the node (like a PC) and save the node with URL `http://HOST:8765`.

## 📱 smartphone — web node → mobile node

Two enrollment stages:

1. **Webpage node (immediately):** start the android-node service and open its URL in the
   phone's browser. The phone is **automatically** added as a `webpage` node — controlled
   via JS on the open page (navigate, eval). Nothing to install.
2. **Mobile node (full):** from that page you download the APK or run the Termux script.
   The phone becomes a full node (port 8765): files, system, input — via the `adb`
   connector.

```bash
urirun-android-node serve     # distribution + relay service (port 8195)
```

The service on port 8195 is the distribution hub for every browser-based client:

| Path | Serves |
|------|--------|
| `GET /` | webpage control client (no install — auto-registers on open) |
| `GET /plugins` | JSON list of available clients (chrome, firefox, webpage) |
| `GET /plugins/chrome.zip` | Chrome extension (load unpacked in `chrome://extensions`) |
| `GET /plugins/firefox.zip` | Firefox extension (load in `about:debugging`) |
| `GET /qr.png` `GET /bootstrap.sh` `GET /apk/` | QR, Termux bootstrap, APK download |

In the dashboard: **Smartphone → Uruchom serwis android-node → Pokaż QR**. Scan with the
phone. Connected phones appear in the "web node" list; after installing the APK, save them
as a "mobile node".

See also [Android Nexus 7 example](../examples/47-android-nexus7-node/README.md).

## 📄 webpage relay — page registers itself (no install)

The simplest browser node: **opening the android-node page (port 8195) in any browser**
makes that browser/tab a controllable node — it appears in the dashboard nodes list
**automatically**, with no "save" step. It is transient (present while the page is open,
gone when closed) and tagged `webpage`.

How it works: the page runs a small JS client that registers itself
(`POST /api/webpage-node/register`), then long-polls for actions
(`/api/webpage-node/poll/<id>`) and posts results. The host controls it by running a
`webpage://<id>/...` URI through the relay (`POST /api/webpage-node/relay/<id>/run`), which
queues the action for the page to execute. Routes include `page/query/info`,
`page/command/navigate`, `page/command/eval`, `camera/command/start`, `sensor/...`,
`iframe/command/open`.

The dashboard `summary()` merges these live webpage nodes into the nodes list (so they show
up the moment a device opens the page), and the **✕ Usuń** button forgets a transient node
in the service (`/api/webpage-node/forget`) or deletes a persistent node from host config.

This is distinct from **Browser Debug** below — webpage relay needs no debug port and works
on phones; CDP (Browser Debug) gives full whole-browser control but needs a desktop browser
launched with `--remote-debugging-port`.

## 🌐 browser-debug — whole browser (CDP)

Control an entire browser through the Chrome DevTools Protocol: every tab (open / close /
navigate), status, screenshots. Connector `webnode`, scope `browser`.

```bash
google-chrome --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1
```

```bash
urirun run "webnode://browser/tabs/query/list" --entry-points --execute --allow 'webnode://*'
```

Save the node with endpoint `http://127.0.0.1:9222`. The dashboard form also shows a QR by
default — scanning it on another device opens that browser as a webpage node (auto-registered).

## 🧩 browser-chrome-plugin — Chrome extension node

Chrome plugin nodes control the active browser tab through an installed extension
and relay URI calls back to a urirun node. Use this when a full CDP debug port is
not available or when you want an extension-scoped browser capability.

```bash
urirun host add-node chrome-plugin http://127.0.0.1:8765 --kind browser-chrome-plugin
```

## 🧩 browser-firefox-plugin — Firefox extension node

Firefox plugin nodes follow the same pattern as Chrome plugin nodes, but use a
temporary or installed Firefox add-on as the browser-side bridge.

```bash
urirun host add-node firefox-plugin http://127.0.0.1:8765 --kind browser-firefox-plugin
```

## 📄 webpage — a single page (HTML/JS)

Control **one page/tab**: navigate, eval JS, click by selector, type, screenshot.
Connector `webnode`, scope `page`. Choose the tab with `WEBNODE_TARGET` (an id from the
tab list) — otherwise it acts on the active tab.

```bash
# list tabs and their ids:
urirun run "webnode://browser/tabs/query/list" --entry-points --execute --allow 'webnode://*'
# drive one page:
WEBNODE_TARGET=<id> urirun run "webnode://page/command/navigate" \
  --entry-points --execute --allow 'webnode://*' --payload '{"url":"https://example.com"}'
```

Save the node with the CDP endpoint and (optionally) the tab id. The dashboard form shows a
QR by default for the page-as-webpage-node flow.

## 🔌 api — configured HTTP/API endpoint

API nodes represent external HTTP/REST/OpenAPI services, SaaS endpoints or local
HTTP services. The host stores API metadata and credentials by reference, then
projects URI calls such as `api://crm-api/main/command/request` onto the
configured endpoint.

```bash
urirun host add-node crm-api https://api.example.test/v1 \
  --kind api \
  --api-id main \
  --api-kind rest \
  --auth-type bearer \
  --auth-token TOKEN
```

Secrets are stored through `secret://keyring/urirun-node-api/<node>/<api>#credential`.

## 🧩 device — multi-interface physical device

Device nodes group several interfaces on one physical or embedded device: web UI,
RTSP stream, SSH, SMB/NAS, GPIO, MQTT or vendor APIs. HTTP-like interfaces can be
called through host-configured API routes; non-HTTP protocols return
`connector_required` until the matching connector is installed.

```bash
urirun host add-node rpi-camera http://rpi.local \
  --kind device \
  --api '{"id":"panel","kind":"web","url":"http://rpi.local"}' \
  --api '{"id":"stream","kind":"rtsp","role":"camera","url":"rtsp://rpi.local/live"}' \
  --api '{"id":"ssh","kind":"ssh","url":"ssh://pi@rpi.local"}'
```
