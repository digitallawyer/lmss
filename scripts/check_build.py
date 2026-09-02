#!/usr/bin/env python3
"""Post-build checks. Fails CI rather than shipping a broken tree.

The generated site is far too large to eyeball, so the invariants that matter --
valid JSON, no dangling internal links, no slug collisions -- are asserted here.
"""

import json
import re
import sys
from pathlib import Path

MIN_TAGS = 15000   # a parse that silently half-fails should not deploy


def main(out):
    root = Path(out)
    if not (root / "tag").is_dir():
        sys.exit(f"{out}/tag/ missing -- did the generator run?")

    problems = []
    ids = {p.name for p in (root / "tag").iterdir() if p.is_dir()}
    slugs = {p.name for p in (root / "branch").iterdir() if p.is_dir()}

    if len(ids) < MIN_TAGS:
        problems.append(f"only {len(ids):,} tag pages (expected >= {MIN_TAGS:,})")

    for path in root.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            problems.append(f"invalid JSON: {path} ({exc})")

    dangling_tags, dangling_branches = set(), set()
    for path in (root / "tag").rglob("index.html"):
        page = path.read_text(encoding="utf-8")
        dangling_tags |= {m for m in re.findall(r'href="/tag/([^/"]+)/"', page)
                          if m not in ids}
        dangling_branches |= {m for m in re.findall(r'href="/branch/([^/"]+)/"', page)
                              if m not in slugs}
    if dangling_tags:
        problems.append(f"{len(dangling_tags)} dangling /tag/ links, "
                        f"e.g. {sorted(dangling_tags)[:3]}")
    if dangling_branches:
        problems.append(f"{len(dangling_branches)} dangling /branch/ links, "
                        f"e.g. {sorted(dangling_branches)[:3]}")

    # Hand-written pages link into the generated tree, so check those too.
    # Skip hrefs containing quotes/plus signs: those are JS-built strings.
    def resolves(href):
        href = href.split("#")[0].split("?")[0]
        target = root / href.lstrip("/")
        return (target.is_file() or (target / "index.html").is_file()
                or (root / (href.lstrip("/") + ".html")).is_file())

    for path in list(root.glob("*.html")) + [root / "branch/index.html",
                                             root / "crosswalk/index.html"]:
        if not path.is_file():
            continue
        for href in re.findall(r'href="(/[^"\'+]*)"', path.read_text(errors="ignore")):
            if not resolves(href):
                problems.append(f"broken link in {path.name}: {href}")

    labels = [json.loads((root / "api/v2/branch" / f"{s}.json").read_text())["label"]
              for s in slugs]
    if len(set(labels)) != len(labels):
        problems.append("branch slug collision -- two branches share a URL")

    size = sum(f.stat().st_size for f in root.rglob("*") if f.is_file())
    if size > 900e6:
        problems.append(f"site is {size/1e6:.0f} MB, near the 1 GB Pages limit")

    if problems:
        print("BUILD CHECK FAILED", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    print(f"build check passed: {len(ids):,} tags, {len(slugs)} branches, "
          f"{size/1e6:.0f} MB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_site")
