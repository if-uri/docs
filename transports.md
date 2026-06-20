# Transports

`urirun` keeps the URI contract separate from the transport. The same URI can be
called locally, through a service endpoint, or by a flow orchestrator.

## Local and shell

- `local-function` calls an in-process function registered by code.
- `argv-template` renders an argv list and executes it without a shell.
- `shell-template` renders a shell string and requires explicit policy approval.

## Docker

Docker examples use URI targets as service names:

```text
python://python-worker/text/normalize
node://node-worker/text/slugify
shell://shell-worker/report/write
```

See `v2/examples/docker_uri_flow` for a Compose flow where services publish
bindings and an orchestrator runs a multi-step URI flow.

## HTTP and browser

The HTML example in `v2/examples/html_uri_app` loads a binding document, renders
URI forms, and calls a Python backend through `POST /api/run`.

The backend can expose logs, recent calls, MCP tools, and A2A cards from the same
registry, so frontend actions use the same URI names as backend actions.

The connector hub also has HTTP-oriented packages. The verified HTTP Check
connector installs from [connect.ifuri.com/connectors/http-check](https://connect.ifuri.com/connectors/http-check)
and exposes:

```text
httpcheck://host/http/query/status
```

That route can be called from shell, an ifuri host process, an MCP client or a
flow orchestrator because the transport-specific implementation remains behind
the registry adapter.

## gRPC

`urirun.v2_grpc` provides a small RPC surface for route listing, unary calls,
and stream-style calls. Install the optional dependency set when using it:

```bash
pip install "urirun[grpc] @ git+https://github.com/tellmesh/urirun.git@v0.3.14#subdirectory=adapters/python"
```

## MCP and A2A

Because v2 bindings include JSON Schema, the registry can be projected into:

- MCP `tools/list`
- MCP `tools/call`
- A2A agent card skills

Execution still goes through the same `urirun` policy gate.

See [MCP and A2A](mcp.md) for the LLM-facing projection.
