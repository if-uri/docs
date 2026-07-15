% ── Project Metadata ─────────────────────────────────────
project_metadata('docs', '0.0.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 31, 'less').
project_file('project.sh', 66, 'shell').
project_file('scripts/build_site.py', 104, 'python').
project_file('scripts/check_node_types.py', 48, 'python').
project_file('scripts/check_site.py', 58, 'python').
project_file('scripts/deploy-plesk.sh', 15, 'shell').
project_file('tree.sh', 5, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('scripts/build_site.py', 'md', 1, 27, 12).
python_function('scripts/build_site.py', 'md_to_html_links', 1, 1, 1).
python_function('scripts/build_site.py', 'page', 1, 1, 5).
python_function('scripts/check_node_types.py', '_load_registry_ids', 0, 2, 2).
python_function('scripts/check_node_types.py', 'main', 0, 9, 5).
python_function('scripts/check_site.py', 'main', 0, 10, 13).

% ── Python Classes ───────────────────────────────────────

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('help', '').
makefile_target('site', '').
makefile_target('test', '').
makefile_target('deploy', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────

% ── TestQL Scenarios ─────────────────────────────────────

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_workflow('site', 'manual').
sumd_workflow_step('site', 1, 'python3 scripts/build_site.py _site').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'python3 scripts/check_site.py').
sumd_workflow_step('test', 2, 'python3 scripts/check_node_types.py').
sumd_workflow('deploy', 'manual').
sumd_workflow_step('deploy', 1, 'bash scripts/deploy-plesk.sh').

