# Generating connectors

A connector is anything that produces a `urirun.bindings.v2` document. That
contract is **language-agnostic**: the bindings are JSON, the runtime validates
and dispatches them, and the thing a binding runs (a command, an HTTP call, a
container) can be written in anything. This page shows how to generate
connectors from a command, a service and a Docker artifact, and how to emit the
same contract from Python, JavaScript, Go or PHP.

For the Python authoring API specifically, see
[Connector authoring](connector-authoring.md).

## The contract

Every connector emits one document:

```json
{
  "version": "urirun.bindings.v2",
  "bindings": {
    "<scheme>://<target>/<resource>/<operation>": {
      "kind": "command",
      "adapter": "argv-template",
      "inputSchema": { "type": "object", "properties": {}, "additionalProperties": false },
      "argv": ["my-cli", "sub", "{param}"],
      "meta": { "label": "..." }
    }
  }
}
```

Whatever produces this JSON, the runtime treats it the same:

```bash
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun run '<uri>' registry.json --payload '{...}' --execute --allow '<scheme>://*'
```

## From a command

The most common adapter is `argv-template`: the binding is an argv list with
`{placeholder}` slots filled from the validated payload.

```json
"hash://host/sha256/command/file": {
  "kind": "command",
  "adapter": "argv-template",
  "inputSchema": {
    "type": "object", "required": ["path"],
    "properties": { "path": { "type": "string" } },
    "additionalProperties": false
  },
  "argv": ["sha256sum", "{path}"],
  "policy": { "allowExecute": true }
}
```

You can also let the runtime adopt commands from a project:

```bash
urirun scan ./project --registry-out generated/registry.json
```

## From a service

Point a route at an HTTP (or gRPC) service with the `fetch` adapter instead of a
local command — the connector wraps a remote capability as a URI:

```json
"weather://host/forecast/query/today": {
  "kind": "fetch",
  "adapter": "fetch",
  "inputSchema": {
    "type": "object", "required": ["city"],
    "properties": { "city": { "type": "string" } },
    "additionalProperties": false
  },
  "request": { "method": "GET", "url": "https://api.example.com/forecast?city={city}" }
}
```

The same registry then projects to MCP tools and an A2A card, so the service is
callable by an agent without extra glue.

## From a Docker artifact

A binding can run a container, so any Dockerized tool becomes a URI route. Use
`argv-template` with `docker run`:

```json
"convert://host/image/command/resize": {
  "kind": "command",
  "adapter": "argv-template",
  "inputSchema": {
    "type": "object", "required": ["input", "width"],
    "properties": {
      "input": { "type": "string" },
      "width": { "type": "integer", "minimum": 1 }
    },
    "additionalProperties": false
  },
  "argv": [
    "docker", "run", "--rm", "-v", "{input}:/in",
    "dpokidov/imagemagick", "convert", "/in", "-resize", "{width}", "/in"
  ],
  "policy": { "allowExecute": true }
}
```

This keeps the connector itself tiny — the capability ships as an image, and the
binding is the stable URI address in front of it.

## Standardized generation across languages

Because the output is just the `urirun.bindings.v2` JSON, a urirun SDK can build
it in any language and ship as a normal library inside your project. The same
three calls — declare a connector, declare commands, emit bindings — produce an
identical document.

**Python** (`urirun`):

```python
import urirun
c = urirun.connector("hash", scheme="hash")

@c.command("sha256/command/file")
def sha256(path: str) -> list[str]:
    return ["sha256sum", "{path}"]

print(urirun.dump(c.bindings()))
```

**JavaScript** (`urirun-js`):

```js
import { connector } from "urirun-js";
const c = connector("hash", { scheme: "hash" });
c.command("sha256/command/file", {
  input: { required: ["path"], properties: { path: { type: "string" } } },
  argv: ["sha256sum", "{path}"],
});
console.log(JSON.stringify(c.bindings(), null, 2));
```

**Go** (`urirun-go`):

```go
c := urirun.NewConnector("hash", "hash")
c.Command("sha256/command/file", urirun.Schema{Required: []string{"path"},
    Properties: map[string]any{"path": map[string]any{"type": "string"}}},
    []string{"sha256sum", "{path}"})
fmt.Println(c.BindingsJSON())
```

**PHP** (`urirun-php`):

```php
$c = new Urirun\Connector('hash', 'hash');
$c->command('sha256/command/file',
    ['required' => ['path'], 'properties' => ['path' => ['type' => 'string']]],
    ['sha256sum', '{path}']);
echo $c->bindingsJson();
```

Each prints the same document, and the runtime validates and runs any of them:

```bash
node connector.js > bindings.json   # or: python connector.py / go run . / php connector.php
urirun validate bindings.json
urirun compile bindings.json --out registry.json
urirun list registry.json
```

The SDKs live next to the runtime under `adapters/<language>/` in
[if-uri/urirun](https://github.com/if-uri/urirun): Python, JavaScript, Go, PHP,
Ruby, Perl, Rust, Bash and C. They are kept in lockstep by a conformance check —
`python3 adapters/conformance.py` builds the same `hash` connector with every
SDK and asserts the documents are identical and valid — so a connector behaves
the same no matter which language authored it. The canonical SDK surface is
defined in `adapters/SPEC.md`.

## Related

- [Connector authoring](connector-authoring.md) - the full Python authoring API.
- [Registry and bindings](registry-and-bindings.md) - how a binding becomes a
  dispatchable, policy-gated registry.
- [Transports](transports.md) - the adapter kinds a binding can target.
- [Connectors](connectors.md) - install from the hub and the package shape.
