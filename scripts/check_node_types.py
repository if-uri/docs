#!/usr/bin/env python3
"""Validate docs/node-types.md against the host node type registry."""
from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
MONOREPO = ROOT.parent
NODE_TYPES_MD = ROOT / "node-types.md"


def _load_registry_ids() -> tuple[list[str], dict[str, str]]:
    sys.path.insert(0, str(MONOREPO / "urirun" / "adapters" / "python"))
    from urirun.host.node_types import NODE_TYPE_ALIASES, NODE_TYPE_PROFILES  # noqa: PLC0415

    ids = [str(item["id"]) for item in NODE_TYPE_PROFILES]
    aliases = {
        "browser": NODE_TYPE_ALIASES["browser"],
        "web": NODE_TYPE_ALIASES["web"],
        "webnode": NODE_TYPE_ALIASES["webnode"],
    }
    return ids, aliases


def main() -> int:
    ids, aliases = _load_registry_ids()
    text = NODE_TYPES_MD.read_text(encoding="utf-8")
    errors = 0
    for node_type in ids:
        if f"`{node_type}`" not in text and f"| {node_type} " not in text:
            print(f"FAIL: node-types.md does not mention canonical node type {node_type!r}")
            errors += 1
    for alias, target in aliases.items():
        if f"`{alias}`" not in text or f"`{target}`" not in text:
            print(f"FAIL: node-types.md does not document alias {alias!r} -> {target!r}")
            errors += 1
    if len(ids) != 10:
        print(f"FAIL: expected 10 canonical node types, registry has {len(ids)}: {ids}")
        errors += 1
    print(f"checked {len(ids)} node type(s), {len(aliases)} alias(es), {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
