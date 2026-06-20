# Working with errors (error://)

`urirun` turns failures into addressable, searchable resources. Every failed
execution gets a stable error code and an `error://` address, so an error is
something you can look up, search, fix and turn into a ticket - not a one-off
log line.

## Stable codes and addresses

When a route fails, the result envelope gains a code and an address:

```json
{
  "uri": "shell://host/echo/run",
  "ok": false,
  "error": {
    "type": "policy",
    "message": "no allow rule matched (default deny)",
    "code": "E-ce9b1dd4",
    "uri": "error://local/E-ce9b1dd4/query/info"
  }
}
```

The same *class* of error always hashes to the same code: volatile bits
(file paths, numbers, hex addresses) are normalized out before hashing, so
repeated failures aggregate under one code with an occurrence count.

## Where errors are stored

Errors are appended to `~/.urirun/errors.jsonl`.

- `URIRUN_ERROR_LOG` - override the store path.
- `URIRUN_ERRORS=0` - stamp the `error://` address but do not persist (useful
  for ephemeral or read-only environments). Stamping the envelope is always
  side-effect free.

## Command line

```bash
python -m urirun.errors recent          # most recent errors, aggregated by code
python -m urirun.errors info E-ce9b1dd4  # details, occurrence count and fix hints
python -m urirun.errors search policy    # search by code, type, message or scheme
python -m urirun.errors ticket E-ce9b1dd4  # turn an error into a planfile ticket
```

`info` returns occurrence counts, the failing URIs, and type-aware fix hints,
for example a policy denial suggests adding an `--allow` rule.

## On a node

A running node (`get.ifuri.com/node.sh`) records the errors it serves and
exposes them over HTTP:

```text
GET /errors                 # recent errors, aggregated by code
GET /errors/search?q=shell  # search the node's errors
GET /errors/<code>          # info + fix hints for one code
```

Every failed `POST /run` response also carries the `error://` address, so a
caller can look the error up immediately.

## From error to ticket

`ticket` (CLI) or `urirun.errors.to_ticket(code)` creates a
[planfile](https://github.com/if-uri/urirun) ticket from a recorded error: it
copies the type, message, failing URIs and fix hints into the ticket body,
labels it `error` / `urirun` / `<scheme>`, and raises the priority to `high`
once the error has recurred five or more times. This closes the loop from a
runtime failure to tracked, fixable work.

## Related

- [Registry and bindings](registry-and-bindings.md) - how a URI becomes an
  executable, policy-gated route.
- [Commands](commands.md) - the `urirun` CLI.
- [Host and node on a LAN](host-node-lan.md) - running a node that serves
  `/errors`.
