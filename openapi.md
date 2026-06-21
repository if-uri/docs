# Import an OpenAPI spec (`add-openapi`)

Turn an existing REST API into URI-addressed routes with no handler code.
`urirun add-openapi` reads an OpenAPI document and emits declarative `fetch`
bindings — one route per path × method — that flow through the normal
compile / validate / run / MCP pipeline.

## Usage

```bash
urirun add-openapi <openapi.json|url> --scheme <scheme> [--target <name>] [--base-url <url>]
```

| Flag | Meaning |
| --- | --- |
| `spec` | path or URL to an `openapi.json` |
| `--scheme` | URI scheme for the generated routes, e.g. `ksef` |
| `--target` | URI target / environment name (default: `api`) |
| `--base-url` | override the base URL (else `servers[0]` from the spec) |

## What it generates

Each `path` × `method` becomes a route:

```
ksef://api/invoices/{id}/query/get      ->  GET  {base}/invoices/{id}
ksef://api/invoices/command/post        ->  POST {base}/invoices
```

- the base URL is resolved from `environments[<target>]` (or `--base-url`), so the
  same routes point at staging or production by switching the target;
- `{param}` placeholders in the path are templated from the payload at run time and
  validated by an `inputSchema` derived from the path parameters;
- auth and crypto stay as the one referenced helper — pair this with
  [`secret://`](secrets.html) so credentials resolve lazily at the executor boundary.

## Related

`add-openapi` is the OpenAPI front end to urirun's declarative HTTP connectors.
For a hand-written spec, `urirun connectors from-spec <spec.toml|json>` turns an
`environments` + `routes` table into the same `fetch` bindings — config, not code.
See [generating connectors](generating-connectors.html) and
[transports](transports.html).
