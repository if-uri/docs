# Security and policy

urirun is **default-deny**: a route only runs if an explicit policy allows it. This
page is where execution restrictions live, how to read them in real time, and how to
manage them.

> **Note on assistant guardrails.** If you drive a node through an AI assistant, the
> assistant keeps its own safety rules (it will not type passwords, enter payment
> details, etc.). Those are the assistant's operating rules, **not** a urirun setting —
> they are not configured here and cannot be toggled off. This page covers urirun's
> own execution policy, which *is* configurable.

## Where restrictions are set

| restriction | where you set it |
|-------------|------------------|
| **Which URIs may execute** | `urirun node serve --allow '<glob>'` (repeatable) — the node's allow-list. Without a match a call is denied (`no allow rule matched (default deny)`). |
| **Allow for pushed routes** | `urirun host deploy <node> --allow '<glob>'` — the policy for a deployed surface. |
| **Programmatic policy** | `urirun.policy(allow=[...], deny=[...], secret_allow=[...], policy_file=...)` → pass as `policy=` to `urirun.run(...)`. |
| **Per-route gate** | a binding's `policy.allowExecute: true` lets that one route run without a glob. |
| **Who may call `/run`** | `urirun node serve --require-run-auth` → `/run` and `/events` require an admin token or an enrolled SSH key (403 otherwise). |
| **Node admin (deploy / node://)** | `--key-auth` (enrolled `~/.ssh/id_ed25519`, `authorized_keys`) or `--admin-token`; `/deploy` and `node://` are always admin-gated. |
| **Secrets** | `secret://` / `getv://` are execute-only and deny-by-default; widen with `secret_allow` globs. |
| **Surface integrity** | `host deploy --merge` (add, don't replace) and the registry **etag** (a hot-swap is detectable, see [host & node](host-node-lan.md)). |

Globs match the URI: `env://*` allows any `env` route, `browser://laptop/**` any browser
route on `laptop`, `**` everything (don't, on an open `/run`).

## Read the restrictions in real time

- **`GET /health` → `policy`** shows the live allow-list and the auth flags:

  ```bash
  curl -s http://node:8765/health | jq .policy
  # { "allow": ["env://*","proc://*"], "requireRunAuth": false, "allowSecrets": false }
  ```

- **Every `/run` envelope carries a `decision`** — the policy verdict for that exact call:

  ```json
  { "uri": "shell://laptop/command/rm", "ok": false,
    "decision": { "allowed": false, "reason": "no allow rule matched (default deny)" } }
  ```

- **`urirun host probe <node>`** snapshots the surface and dry-runs every route pinned to
  the registry etag, so you can see what a node will and won't run right now (and whether
  the surface is being hot-swapped under you). See [Commands](commands.md).

- **Capability discovery over URIs** — a connector can expose what a machine offers
  without `shell://`. Example: `browser://<node>/system/query/browsers` lists the
  installed browsers and their paths, so a caller picks a browser from the contract
  rather than probing the shell.

## Manage it

- **Tighten** (recommended for anything reachable on a LAN): narrow the `--allow` globs to
  the exact schemes a node should serve, add `--require-run-auth`, enroll keys with
  `urirun host copy-id`. An open `/run` with `--allow '**'` is unauthenticated remote
  execution — only for a throwaway local node.
- **Loosen** deliberately and visibly: widen a glob, and confirm it with
  `curl /health | jq .policy` and a dry-run (`urirun host probe`). The change is in one
  place (the node's allow-list), readable at any time.
- **Audit**: every call is logged with its envelope, `decision`, status, time and source;
  the SSE stream (`/events`) emits `error://` for denials as they happen.

## Related

- [Host and node on a LAN](host-node-lan.md) — deploy, merge, probe, churn detection.
- [Secrets](secrets.md) — `secret://` / `getv://` by reference, execute-only.
- [Commands](commands.md) — `host probe`, `host deploy --merge`, `connectors verify`.
