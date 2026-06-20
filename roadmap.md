# Roadmap

The current roadmap is maintained in the public planning site:
[roadmap.ifuri.com](https://roadmap.ifuri.com/).

## P0 - trust installs and execution

- Keep active install commands and package dependencies on
  `github.com/if-uri/urirun`.
- Prove every available connector in Docker with host, pc1 and pc2.
- Remove compatibility modules from `urirun` core after downstream migration.
- Keep hub manifests, docs snippets and tested release tags synchronized.

## P1 - make connectors easy to use

- Use `urirun connectors list/show/install/check` for the public hub catalog
  and `urirun discover` / `urirun compile --entry-points` for installed
  connector route discovery.
- Add connector install, registry refresh, payload forms and result panels to
  the ifURI app GUI.
- Publish per-connector contract pages with route lists, JSON schemas, policy
  notes and tested version badges.
- Add install bundles and a `doctor` check to `get.ifuri.com`.

## P2 - improve adoption

- Generate blog/tutorial content from connector metadata.
- Keep SEO, social and LLM metadata synchronized across docs, hub and examples.
- Finish brand exports and use the same assets across public sites.

## Current planfile tickets

- `IFURI-008` - released: installed connectors expose `urirun.bindings`
  entry-points and can generate a registry without manual JSON merging.
- `IFURI-015` - remove remaining compatibility modules from `urirun` core.
- `IFURI-016` - prove connector installs through a host-node Docker matrix.
- `IFURI-017` - add connector install and route discovery to the app GUI.
- `IFURI-018` - publish per-connector contract pages and compatibility badges.
- `IFURI-019` - add installer bundles and doctor checks for host/node setup.

Released tooling fix:

- `IFURI-020` - local sprint YAML validation works with `--file-type sprint`;
  `planfile health check` no longer crashes on generated ticket buckets.
