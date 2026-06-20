# Error reference (error://)

`urirun` turns failures into **standardized, addressable, searchable resources**.
Every failed execution is classified against established standards (not a bespoke
taxonomy), gets a stable code and an `error://` address, is recorded to a store,
and links back to this page.

## Standards used

ifURI does not invent its own error taxonomy. It reuses:

- **gRPC canonical status codes** ([grpc/grpc statuscodes.md](https://github.com/grpc/grpc/blob/master/doc/statuscodes.md))
  as the error **category** - `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED`, etc.
- **POSIX `errno`** names (`ENOENT`, `EACCES`, `ETIMEDOUT` …) to classify system errors.
- **RFC 5424 (syslog)** severities - `error`, `critical`, `warning`, `notice`.
- **RFC 9110** HTTP status codes, and the **RFC 9457 (Problem Details for HTTP APIs)**
  response shape via the `problem` projection.

## The error envelope

A failed result carries standardized fields:

```json
{
  "uri": "shell://host/echo/run",
  "ok": false,
  "error": {
    "type": "policy",
    "message": "no allow rule matched (default deny)",
    "code": "E-ce9b1dd4",
    "category": "PERMISSION_DENIED",
    "severity": "warning",
    "status": 403,
    "uri": "error://local/E-ce9b1dd4/query/info",
    "help": "https://docs.ifuri.com/errors.html?code=E-ce9b1dd4&category=PERMISSION_DENIED#permission-denied"
  }
}
```

- **code** - stable id; the same *class* of error always hashes to the same code
  (paths, numbers and hex are normalized out), so occurrences aggregate.
- **category** - the gRPC canonical code (the standardized type).
- **severity** / **status** - RFC 5424 severity and RFC 9110 HTTP status.
- **uri** - the `error://` address you can query.
- **help** - this page, deep-linked to the category, with the code as a query param.

`urirun.errors.problem(envelope)` projects this to RFC 9457
`application/problem+json` (`type` = the help URL, `instance` = the `error://`
address, `title` = category, `status`, `detail`).

## Categories

Every error maps to one canonical category.

| Category | HTTP | Severity | Meaning | First fix |
| --- | --- | --- | --- | --- |
| INVALID_ARGUMENT | 400 | error | Malformed or invalid input, regardless of state | Check the binding `inputSchema` and the payload |
| FAILED_PRECONDITION | 400 | error | System not in the required state | Satisfy the precondition / pass `confirm=True` |
| OUT_OF_RANGE | 400 | error | Attempted past the valid range | Use a value inside the documented range |
| UNAUTHENTICATED | 401 | warning | No valid credentials | Provide auth before calling the route |
| PERMISSION_DENIED | 403 | warning | Not allowed by the policy gate | Add an `--allow` rule matching the URI scope |
| NOT_FOUND | 404 | error | File, route or binary not found | Verify the path, install the dep, or scan the binding |
| ALREADY_EXISTS | 409 | warning | Entity to create already exists | Use the existing entity or a new id |
| ABORTED | 409 | error | Aborted, e.g. a concurrency conflict | Retry with fresh state |
| RESOURCE_EXHAUSTED | 429 | warning | Quota or resource limit hit | Free resources or raise the limit |
| CANCELLED | 499 | notice | Cancelled by the caller | Usually expected; re-run if needed |
| DATA_LOSS | 500 | critical | Unrecoverable data loss/corruption | Restore from backup; investigate |
| UNKNOWN | 500 | error | Unmapped exception | Inspect the message; file a ticket |
| INTERNAL | 500 | error | Internal invariant broken (a bug) | File a ticket with the code |
| UNIMPLEMENTED | 501 | error | No adapter/executor for the route | Check the binding `adapter`/`kind` |
| UNAVAILABLE | 503 | error | Dependency/transport down | Retry; check the node/service is reachable |
| DEADLINE_EXCEEDED | 504 | error | Timed out before completing | Raise the timeout or check the target |

### How classification works

In order: an explicit `errno`, an `errno` name in the message, high-signal
message patterns (more specific than a generic exception type), then the Python
exception type, then weaker keywords. Examples of the type/errno mapping:

| Source | Category |
| --- | --- |
| `policy` (policy gate denial) | PERMISSION_DENIED |
| `confirm` (needs confirmation) | FAILED_PRECONDITION |
| `schema`, `ValueError`, `KeyError`, `TypeError` | INVALID_ARGUMENT |
| `FileNotFoundError`, `ENOENT` | NOT_FOUND |
| `PermissionError`, `EACCES`, `EPERM` | PERMISSION_DENIED |
| `TimeoutError`, `ETIMEDOUT` | DEADLINE_EXCEEDED |
| `ConnectionError`, `ECONNREFUSED` | UNAVAILABLE |
| `NotImplementedError`, "executor not found" | UNIMPLEMENTED |
| `FileExistsError`, `EEXIST` | ALREADY_EXISTS |
| `ENOSPC`, `EMFILE` | RESOURCE_EXHAUSTED |

## Where errors are stored

Errors are appended to `~/.urirun/errors.jsonl`.

- `URIRUN_ERROR_LOG` - override the store path.
- `URIRUN_ERRORS=0` - stamp the `error://` address without persisting.
- `URIRUN_ERROR_DOCS` - override the docs base URL used in `help` links.

## Command line

```bash
urirun errors recent                  # same CLI, shorter operational form
urirun errors info E-ce9b1dd4
urirun errors search policy
urirun errors ticket E-ce9b1dd4 .
urirun errors bindings > error-bindings.json

python -m urirun.errors recent          # recent errors, aggregated by code
python -m urirun.errors info E-ce9b1dd4  # category, count, severity and fix hints
python -m urirun.errors search policy    # search by code, type, category, message, scheme
python -m urirun.errors ticket E-ce9b1dd4  # turn an error into a planfile ticket
python -m urirun.errors categories       # print the full category table
```

## As URI flow resources

`error://` is also a built-in URI resource. Add its bindings to any registry:

```bash
urirun errors bindings > error-bindings.json
urirun compile error-bindings.json --out error-registry.json
```

Then call it like any other URI route:

```bash
urirun run 'error://local/errors/query/recent' error-registry.json
urirun run 'error://local/errors/query/search' error-registry.json \
  --payload '{"query":"policy"}'
urirun run 'error://local/errors/query/info' error-registry.json \
  --payload '{"code":"E-ce9b1dd4"}'
urirun run 'error://local/errors/command/ticket' error-registry.json \
  --payload '{"code":"E-ce9b1dd4","project":"."}' \
  --execute --allow 'error://local/errors/command*'
```

The per-error address in each envelope is also executable:

```bash
urirun run 'error://local/E-ce9b1dd4/query/info' error-registry.json
```

In a YAML/JSON flow this gives you a normal diagnostic step:

```yaml
- error://local/errors/query/search:
    query: policy
- error://local/errors/command/ticket:
    code: E-ce9b1dd4
    project: .
```

## On a node

A running node records the errors it serves and exposes them over HTTP:

```text
GET /errors                 # recent errors, aggregated by code
GET /errors/search?q=shell  # search the node's errors
GET /errors/<code>          # info + fix hints for one code
```

Every failed `POST /run` response carries the `error://` address and `help` URL.

## Capturing errors from selected functions

Route any function's exceptions into `error://` with the `@capture` decorator -
classification, code, address and recording happen automatically, and the
exception still propagates (with `exc.uri_error` attached):

```python
from urirun.errors import capture

@capture(scheme="dns")
def resolve(domain: str) -> list[str]:
    ...  # an exception here is classified, recorded and re-raised

# inspect after a failure:
try:
    resolve("example.com")
except Exception as exc:
    print(exc.uri_error["code"], exc.uri_error["category"], exc.uri_error["help"])
```

Use `@capture(reraise=False)` to return the standardized error envelope instead
of raising.

## From error to ticket

`urirun.errors.to_ticket(code)` (or `python -m urirun.errors ticket <code>`)
creates a [planfile](https://github.com/if-uri/urirun) ticket from a recorded
error: it copies the category, severity, message, failing URIs, fix hints and the
docs link into the ticket body, labels it `error` / `urirun` / `<category>` /
`<scheme>`, and raises the priority to `high` once the error recurs five or more
times (or its severity is `critical`+). This closes the loop from a runtime
failure to tracked, fixable work.

## Related

- [Registry and bindings](registry-and-bindings.md) - how a URI becomes an
  executable, policy-gated route.
- [Host and node on a LAN](host-node-lan.md) - running a node that serves `/errors`.
- [Commands](commands.md) - the `urirun` CLI.
