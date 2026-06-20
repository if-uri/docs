# Host and node on a LAN

This operator guide explains how two ifURI machines talk to each other on a
local network: one **host** that drives a flow and one or more **nodes** that
advertise services. Every call uses the same `ifuri://` contract, so a workflow
step runs locally or on a peer without changing addresses.

## Roles

- **Host** - starts a local HTTP runtime and UDP discovery, then routes flow
  steps either locally or to a peer.
- **Node** - publishes its service list and sharing scope, and answers
  `ifuri://<node>/services/...` calls.

A single machine can be both: hosts can also expose services, and nodes can run
their own flows.

## 1. Install a node

The fastest path is the installer from `get.ifuri.com`, which creates a local
`urirun` node and prepares it to register on the network:

```bash
curl -fsSL https://get.ifuri.com/node.sh | bash -s -- --name laptop --port 8765 --background
```

For the desktop operator experience, use the ifURI app instead:

```bash
ifuri-app app
```

## 2. Advertise services

A node turns local artifacts into URI routes and serves them over HTTP:

```bash
urirun scan ./project --registry-out generated/registry.json
ifuri-app urirun-serve --registry generated/registry.json   # /health /routes /run
```

The node publishes a service list and a sharing scope so hosts only see what the
operator chose to expose.

## 3. Discover peers

From the host, list the nodes that announced themselves on the LAN:

```bash
ifuri-app discover
```

Discovery is UDP-based, so it works without central configuration as long as the
machines share a broadcast domain.

## 4. Route a flow across the LAN

A flow step can run locally or call a peer with the same URI shape. Only the
target segment changes:

```text
flow:
  id: local-review-and-share
  group: dev-ops

do:
  - urirun://local/registry/query/health
  - mcp://filesystem/list:
      path: ./project
  - ifuri://office-node.lan/services/browser/open:
      url: https://ifuri.com
```

`urirun://local/...` and `mcp://...` run on the host; `ifuri://office-node.lan/...`
is dispatched to the peer over HTTP.

## 5. Audit every call

Every call - local or remote - is recorded with its envelope, payload, status,
time and source. Use the log to confirm which machine executed each step and to
review cross-node activity after a flow runs.

## Troubleshooting

- **No peers in `discover`** - the machines are not in the same broadcast
  domain, or a firewall blocks the UDP discovery port. Put both on the same
  subnet or add an explicit node address.
- **A route returns 403 / not shared** - the node's sharing scope does not
  expose that route. Re-scan and serve with the route included.
- **`urirun` cannot find a console script** - add the connector's bin directory
  to `PATH`; see [Connectors](connectors.md).

## Related

- [noVNC LAN demo](novnc-demo.md) - a four-computer LAN scenario driven by URI
  commands.
- [Transports](transports.md) - the adapter kinds behind each route.
- [Getting started](getting-started.md) - install and run a first URI.
