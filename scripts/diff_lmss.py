#!/usr/bin/env python3
"""Compare two LMSS.owl revisions and summarise what changed.

Used by the update-lmss workflow to write a pull-request body, so a version bump
arrives as a reviewable list of tag changes rather than an opaque SHA.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lmss_parse as L


def snapshot(path):
    tags, _ = L.parse(path)
    return {t.id: (t.label, t.definition) for t in tags.values()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    args = ap.parse_args()

    old, new = snapshot(args.old), snapshot(args.new)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    relabelled = sorted(i for i in set(old) & set(new) if old[i][0] != new[i][0])
    redefined = sorted(i for i in set(old) & set(new)
                       if old[i][0] == new[i][0] and old[i][1] != new[i][1])

    print(f"**{len(new):,} tags** (was {len(old):,}, "
          f"{len(new) - len(old):+,})\n")
    print(f"| Change | Count |\n| --- | ---: |")
    print(f"| Added | {len(added):,} |")
    print(f"| Removed | {len(removed):,} |")
    print(f"| Label changed | {len(relabelled):,} |")
    print(f"| Definition changed | {len(redefined):,} |")

    def section(title, ids, fmt):
        if not ids:
            return
        print(f"\n<details><summary>{title} ({len(ids):,})</summary>\n")
        for i in ids[:200]:
            print(f"- {fmt(i)}")
        if len(ids) > 200:
            print(f"- …and {len(ids) - 200:,} more")
        print("\n</details>")

    section("Removed", removed, lambda i: f"`{i}` — {old[i][0]}")
    section("Added", added, lambda i: f"`{i}` — {new[i][0]}")
    section("Renamed", relabelled, lambda i: f"`{i}` — {old[i][0]} → {new[i][0]}")

    # Removals are the only genuinely breaking change for downstream consumers.
    if removed:
        print(f"\n> **{len(removed):,} tags disappeared.** Check whether they were "
              f"deprecated upstream or consolidated before merging.")


if __name__ == "__main__":
    main()
