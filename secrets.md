# Secrets by reference (`secret://`)

A URI should carry a *reference* to a credential, never the credential itself.
`secret://` resolves the value **lazily, only in `--execute`**, behind a
deny-by-default policy, and injects it at the executor boundary (env / header /
stdin). Resolved values are wrapped in `SecretStr`, so every serialized surface —
the registry, route table, error store, logs, MCP tools and A2A cards — prints
`****` instead of the secret.

## Referencing a secret

A route's config carries a `{secret:…}` or `{getv:…}` placeholder, or a route URI
references a provider:

```
secret://keyring/ksef/{nip}        # OS credential store, keyed per NIP
getv://OPENROUTER_API_KEY          # process environment variable
```

The reference lives in the registry in plain sight; the value never does.

## Providers

| Provider | Source |
| --- | --- |
| `env` / `getv` | process environment |
| `dotenv` | a `.env` file |
| `keyring` | the OS credential store |
| `vault` | HashiCorp Vault KV v2 (`VAULT_ADDR` / `VAULT_TOKEN`) |
| `oauth` | a cached access token with in-place refresh |
| `browser` | **refuses by design** — auto-scraping a browser's saved logins is the
  infostealer pattern the OS blocks; export the one credential you need to your
  keyring instead |

## Policy: deny by default

A `secret://` reference resolves only when explicitly allowed, and only in
`--execute`:

```bash
urirun run 'fetch://api/invoice/command/send' registry.json --execute \
  --allow 'fetch://*' --secret-allow 'secret://keyring/ksef/*'
```

Without a matching `--secret-allow` glob the reference stays unresolved and the
call is refused — the same default-deny discipline as route execution.

## On a node

`urirun node serve` resolves **no** `secret://` references by default: a remote
`/run` must not read the host's local secrets. Opt in per host:

```bash
urirun node serve --allow-secrets
```

## Why this matters

The secret is addressable and policy-gated like any other capability, but it is
injected at the last moment and never serialized. A leaked registry, a captured
error envelope or an MCP transcript carries `****`, not the key.
