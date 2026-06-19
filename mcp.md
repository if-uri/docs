# MCP & A2A — how an LLM client calls ifURI URI routes as tools

> **In one sentence:** ifURI turns your project's actions into URI routes, the
> [urirun](https://github.com/tellmesh/urirun) runtime compiles them into a registry,
> and `ifuri-app urirun-mcp` *projects* that registry as **[MCP](https://modelcontextprotocol.io)
> tools** (and an **A2A agent card**) — so a client like **Claude** can discover and call
> them, while every call still passes the urirun policy gate.

Sites: [ifuri.com](https://ifuri.com) · [docs.ifuri.com](https://docs.ifuri.com) ·
[examples.ifuri.com](https://examples.ifuri.com) · [get.ifuri.com](https://get.ifuri.com) ·
[connect.ifuri.com](https://connect.ifuri.com) · [logo.ifuri.com](https://logo.ifuri.com)
Repos: [if-uri/app](https://github.com/if-uri/app) · [tellmesh/urirun](https://github.com/tellmesh/urirun)

## The contract

A route is a stable address `scheme://target/resource/operation`. A **binding** describes
how to run it (adapter + JSON-Schema input). Many bindings compile into one **registry**.
The same registry is what the CLI runs, what the HTTP/MCP server serves, and what flows call.
See [docs: registry-and-bindings](registry-and-bindings.md) and [transports](transports.md).

## Pipeline (what happens, step by step)

```text
project artifacts ──scan──▶ bindings.v2.json ──compile──▶ registry.json
                                                              │
                                   ┌──────────────────────────┼───────────────────────────┐
                                   ▼                          ▼                            ▼
                          MCP tools/list             A2A agent card                 tools/call
                       (to_mcp_tools)              (to_a2a_card)                   (call_tool)
                                   │                                                     │
                                   ▼                                                     ▼
                        Claude / MCP client  ───── JSON-RPC over stdio ─────▶  urirun.v2.run
                                                                                         │
                                                                       resolve_route → validate_input
                                                                       → adapter + policy gate → result
```

### 1. Declare / scan → bindings
You write bindings by hand, generate them with decorators, or scan a project.
- CLI: `ifuri-app urirun-scan ./project --registry-out generated/registry.json`
- App code: [`scan_project()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L327)
  → [`cmd_urirun_scan()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/cli.py#L380)
- urirun does the scanning in [`urirun._scan`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/_scan.py)
  (Dockerfile labels, package scripts, Python entry points, Makefile, shell, explicit binding files).

### 2. Compile → registry
- [`urirun.v2.compile_registry()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2.py#L794)
  produces `{version, routes, index, routeCount, …}`.
- The app finds the active registry via
  [`default_urirun_registry()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L152)
  (env `IFURI_URIRUN_REGISTRY` or `workspace.urirun.registry`).

### 3. Project → MCP tools / A2A card
This is the bridge from "URI registry" to "agent tools".
- `ifuri-app urirun-mcp tools` → MCP `tools/list`
  ([`mcp_tools()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L363)
  → [`urirun.v2_mcp.to_mcp_tools()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L45)).
  Each route becomes a tool whose name is sanitised by
  [`tool_name()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L32)
  and whose `inputSchema` is the binding's JSON Schema.
- `ifuri-app urirun-mcp card` → A2A (Agent2Agent) agent card
  ([`a2a_card()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L378)
  → [`urirun.v2_mcp.to_a2a_card()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L65)) —
  every route is published as an agent **skill**.
- CLI wiring: [`cmd_urirun_mcp()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/cli.py#L408).

Example:

```bash
ifuri-app urirun-mcp tools --registry generated/registry.json
# -> {"ok": true, "tools": [{"name": "sys_local_echo_hello", "inputSchema": {...}}, ...]}
```

### 4. Serve over stdio → a client connects
- `ifuri-app urirun-mcp serve --registry generated/registry.json` starts an **MCP stdio server**
  ([`serve_mcp()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L401)
  → [`urirun.v2_mcp.serve_mcp()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L104)),
  speaking [JSON-RPC 2.0](https://www.jsonrpc.org/specification) over stdin/stdout — the transport MCP clients expect.
- Add `--execute` to allow real runs (otherwise it stays dry-run). A standalone
  equivalent is `python -m urirun.v2_mcp serve registry.json`
  ([`main()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L145)).

Register it in an MCP client (e.g. Claude Desktop / Claude Code) as a command server:

```json
{
  "mcpServers": {
    "ifuri": {
      "command": "ifuri-app",
      "args": ["urirun-mcp", "serve", "--registry", "/path/generated/registry.json"]
    }
  }
}
```

### 5. The client discovers → calls
1. Client sends `tools/list` → server returns the projected tools.
2. Client sends `tools/call {name, arguments}` →
   [`urirun.v2_mcp.call_tool()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L96)
   maps the tool name back to a URI (via
   [`build_tool_index()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py#L92))
   and runs it.

### 6. Run → resolve, validate, gate, execute
`call_tool` (and the in-process path
[`dispatch_local()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L173)) both end in
[`urirun.v2.run()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2.py#L644):
- [`resolve_route()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/_registry.py#L445)
  finds the binding (URI parsed by
  [`translate()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/_registry.py#L43));
- [`validate_input()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2.py#L187)
  checks the payload against the JSON Schema with
  [`jsonschema` Draft 2020-12](https://python-jsonschema.readthedocs.io/);
- the **policy gate** decides allow/deny (default-deny in execute mode); an approved run uses an
  allow policy (see [`_load_urirun_policy()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/runtime.py#L124));
- an adapter runs it — e.g.
  [`run_argv_template()`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2.py#L246)
  (safe argv, no shell) — and a result envelope `{ok, decision, result}` comes back.

## The same registry, other surfaces

Because the contract is constant, the registry feeds more than MCP:
- **CLI** `ifuri-app urirun-call URI --registry … [--execute]`
  ([`cmd_urirun_call()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/cli.py#L340)).
- **HTTP** `ifuri-app urirun-serve` → `/health`, `/routes`, `POST /run`
  ([`serve_http()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/urirun_bridge.py#L232)).
- **Flows** route URIs (local packs → urirun → remote node) in
  [`RuntimeState.run_flow()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/runtime.py#L231)
  and [`call_uri()`](https://github.com/if-uri/app/blob/main/src/ifuri_app/runtime.py#L173).

## Libraries used
- [urirun](https://github.com/tellmesh/urirun) — the URI runtime: `v2` (run/compile),
  [`v2_mcp`](https://github.com/tellmesh/urirun/blob/main/adapters/python/urirun/v2_mcp.py) (MCP/A2A),
  `_registry`, `_scan`, `_runtime`.
- [Model Context Protocol](https://modelcontextprotocol.io) — tool discovery/call for LLM clients.
- A2A (Agent2Agent) — agent capability card (one skill per route).
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification) — the stdio wire format.
- [jsonschema](https://python-jsonschema.readthedocs.io/) — input validation (Draft 2020-12).
- [pydantic](https://docs.pydantic.dev/) — optional schema generation from decorated functions.

## Try it
```bash
pip install "git+https://github.com/tellmesh/urirun.git@main#subdirectory=adapters/python"
ifuri-app urirun-scan ./project --registry-out generated/registry.json
ifuri-app urirun-mcp tools --registry generated/registry.json   # what a client sees
ifuri-app urirun-mcp serve --registry generated/registry.json   # connect Claude here
```

More: [commands](commands.md) · [getting-started](getting-started.md) ·
runnable [examples.ifuri.com](https://examples.ifuri.com).
