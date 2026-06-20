#!/usr/bin/env python3
"""Build the docs site and validate it: pages build and internal links resolve.

- runs build_site.py into a temp dir,
- every source *.md (minus README/LICENSE/TODO/CHANGELOG) produced an .html,
- every internal href="<slug>.html" points to a file that exists.

Exit 0 when clean, 1 on any problem. Used by CI (make test) and locally.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"README", "LICENSE", "TODO", "CHANGELOG"}
HREF = re.compile(r'href="([a-z0-9-]+)\.html"')


def main() -> int:
    out = tempfile.mkdtemp(prefix="docs-check-")
    res = subprocess.run([sys.executable, os.path.join(ROOT, "scripts/build_site.py"), out],
                         capture_output=True, text=True)
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        print("FAIL: build_site.py crashed")
        return 1

    errors = 0
    built = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(out, "*.html"))}

    # Every source page must have produced an .html.
    for md in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
        slug = os.path.basename(md)[:-3]
        if slug in SKIP:
            continue
        if slug not in built:
            print(f"FAIL: {slug}.md did not produce {slug}.html")
            errors += 1

    # Every internal link must resolve to a built page.
    for page in sorted(glob.glob(os.path.join(out, "*.html"))):
        text = open(page, encoding="utf-8").read()
        for target in sorted(set(HREF.findall(text))):
            if target not in built:
                print(f"FAIL: {os.path.basename(page)} links {target}.html which was not built")
                errors += 1

    print(f"{len(built)} page(s) built, {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
