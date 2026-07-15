# ifURI docs

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Call Graph](#call-graph)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `docs`
- **version**: `0.0.0`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: Makefile, app.doql.less, project/(5 analysis files)

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 9f 788L | python:3,shell:2,yaml:2,txt:1 | 2026-07-14
# generated in 0.00s
# CC̅=8.3 | critical:1/6 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    md CC=27 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[3]:
  [1] Src [page]: page → md_to_html_links
      PURITY: 100% pure
  [2] Src [main]: main
      PURITY: 100% pure
  [3] Src [main]: main → _load_registry_ids
      PURITY: 100% pure

LAYERS:
  scripts/                        CC̄=8.3    ←in:0  →out:0
  │ !! build_site                 103L  0C    3m  CC=27     ←0
  │ check_site                  57L  0C    1m  CC=10     ←0
  │ check_node_types            47L  0C    2m  CC=9      ←0
  │ deploy-plesk.sh             14L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ planfile.yaml              305L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ tree.txt                    92L  0C    0m  CC=0.0    ←0
  │ project.sh                  66L  0C    0m  CC=0.0    ←0
  │ Makefile                    10L  0C    0m  CC=0.0    ←0
  │

COUPLING: no cross-package imports detected

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 4f 86L | 2026-07-14

SUMMARY:
  files_scanned: 4
  total_lines:   86
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       18
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 0 func | 1f | 2026-07-14
# generated in 0.00s

NEXT[0]: no refactoring needed

RISKS[0]: none

METRICS-TARGET:
  CC̄:          0.0 → ≤0.0
  max-CC:      0 → ≤0
  god-modules: 0 → 0
  high-CC(≥15): 0 → ≤0
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=0.0 → now CC̄=0.0
```

## Intent

ifURI docs
