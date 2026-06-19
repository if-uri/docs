# Roadmap

The most useful next work for making `urirun` easier:

- Add `urirun connectors list/install` so the CLI can consume
  `https://connect.ifuri.com/registry.json` directly instead of relying only on
  shell one-liners.
- Add connector entry-point discovery so installed packages can expose
  `connector_manifest()` and `urirun_bindings()` without custom import glue.
- Add `urirun init` as a guided command that writes `.urirun/`
  defaults, sample policy, and an example binding.
- Add `urirun doctor` to check Python version, optional dependencies, Docker,
  PHP, Node, generated registry freshness, and duplicate route conflicts.
- Add `urirun serve` as a single HTTP console command for logs, route listing,
  dry-runs, and real execution behind policy.
- Add a canonical `.env` loader shared by examples so ports and registry paths
  have one source of truth.
- Add first-class `log://` routes for frontend, backend, shell, firmware, and
  Docker services.
- Add a registry diff command: `urirun diff old-registry.json new-registry.json`.
- Add scanner explanations: every generated binding should include source file,
  source standard, and reason.
- Expand installer smoke tests for GitHub installs, hub installs and GitHub
  Release wheels. The `http-check` connector is the first proven external
  connector package.
- Keep public docs focused on v1 and v2; older experiment folders should remain
  removed or archived outside the main project.
