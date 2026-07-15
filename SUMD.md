# ifURI docs

ifURI docs

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Intent](#intent)

## Metadata

- **name**: `docs`
- **version**: `0.0.0`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: Makefile, app.doql.less, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: docs;
  version: 0.1.0;
}

workflow[name="site"] {
  trigger: manual;
  step-1: run cmd=python3 scripts/build_site.py _site;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=python3 scripts/check_site.py;
  step-2: run cmd=python3 scripts/check_node_types.py;
}

workflow[name="deploy"] {
  trigger: manual;
  step-1: run cmd=bash scripts/deploy-plesk.sh;
}

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: python;
}
```

## Workflows

## Configuration

```yaml
project:
  name: docs
  version: 0.0.0
  env: local
```

## Deployment

```bash markpact:run
pip install docs

# development install
pip install -e .[dev]
```

## Makefile Targets

- `help`
- `site`
- `test`
- `deploy`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# docs | 9f 788L | txt:1,shell:2,python:3,yaml:2 | 2026-07-14
# generated in 0.00s
# stats: 6 func | 0 cls | 9 mod | CC̄=8.3 | critical:1 | cycles:0
# alerts[3]: CC md=27; fan-out md=20; fan-out main=14
# hotspots[4]: md fan=20; main fan=14; page fan=5; main fan=5
# evolution: CC̄ 0.0→8.3 (regressed +8.3)
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[9]:
  Makefile,10
  planfile.yaml,305
  prefact.yaml,94
  project.sh,66
  scripts/build_site.py,103
  scripts/check_node_types.py,47
  scripts/check_site.py,57
  scripts/deploy-plesk.sh,14
  tree.txt,92
D:
  scripts/build_site.py:
    e: md,md_to_html_links,page
    md(text)
    md_to_html_links(s)
    page(slug)
  scripts/check_site.py:
    e: main
    main()
  scripts/check_node_types.py:
    e: _load_registry_ids,main
    _load_registry_ids()
    main()
  Makefile:
  tree.txt:
  project.sh:
  scripts/deploy-plesk.sh:
  planfile.yaml:
  prefact.yaml:
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
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
```

## Call Graph

*5 nodes · 3 edges · 2 modules · CC̄=8.3*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `md` *(in scripts.build_site)* | 27 ⚠ | 1 | 60 | **61** |
| `main` *(in scripts.check_node_types)* | 9 | 0 | 11 | **11** |
| `page` *(in scripts.build_site)* | 1 | 0 | 8 | **8** |
| `_load_registry_ids` *(in scripts.check_node_types)* | 2 | 1 | 3 | **4** |
| `md_to_html_links` *(in scripts.build_site)* | 1 | 1 | 1 | **2** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/if-uri/docs
# generated in 0.00s
# nodes: 5 | edges: 3 | modules: 2
# CC̄=8.3

HUBS[20]:
  scripts.build_site.md
    CC=27  in:1  out:60  total:61
  scripts.check_node_types.main
    CC=9  in:0  out:11  total:11
  scripts.build_site.page
    CC=1  in:0  out:8  total:8
  scripts.check_node_types._load_registry_ids
    CC=2  in:1  out:3  total:4
  scripts.build_site.md_to_html_links
    CC=1  in:1  out:1  total:2

MODULES:
  scripts.build_site  [3 funcs]
    md  CC=27  out:60
    md_to_html_links  CC=1  out:1
    page  CC=1  out:8
  scripts.check_node_types  [2 funcs]
    _load_registry_ids  CC=2  out:3
    main  CC=9  out:11

EDGES:
  scripts.build_site.page → scripts.build_site.md_to_html_links
  scripts.build_site.page → scripts.build_site.md
  scripts.check_node_types.main → scripts.check_node_types._load_registry_ids
```

## Intent

ifURI docs
