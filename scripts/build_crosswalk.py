#!/usr/bin/env python3
"""Map LMSS 1.0 rev. 2 mnemonic codes onto current v3 IRIs.

SALI publishes no crosswalk -- the ontology defines a `sali:code` annotation but
no class uses it -- so anyone holding data coded under 1.0 has no upgrade path.
This derives one by matching labels, and is explicit about how confident each
match is. Matches are a starting point for review, not an authority.
"""

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lmss_parse as L

# Which 1.0 code set corresponds to which v3 branch. Sets with no successor
# branch are listed so the output can say so explicitly rather than stay silent.
CODESET_BRANCH = {
    "SALI-AOL": "Area of Law",
    "SALI-COURT": "Forums and Venues",
    "ISO-4257": "Currency",
    "SALI-FMT": "Data Format",
    "SALI-GOVT": "Governmental Body",
    "SALI-IND": "Industry and Market",
    "SALI-ISO31662": "Location",
    "SALI-LEGENT": "Legal Entity",
    "SALI-MATNAR": "Matter Narrative",
    "SALI-PROC": "Event",
    "SALI-PROCSTAT": "Status",
    "SALI-PROLE": "Actor / Player",
    "SALI-RROLE": "Actor / Player",
    "SALI-TRITYP": "Event",
    "SALI-process-status-type": "Status",
    "SALI-LMST": None,   # document-format metadata; no v3 successor
    "SALI-VERS": None,   # ditto
}


def norm(s):
    s = (s or "").replace("\ufffd", "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\b(law|codes?|the)\b", " ", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def index_tags(tags, branches):
    """label -> [iri], both globally and per branch."""
    by_branch = defaultdict(lambda: defaultdict(list))
    globally = defaultdict(list)
    branch_name = {b: (tags[b].label or "") for b in branches}
    for tag in tags.values():
        names = [tag.label] + tag.pref_labels + tag.alt_labels
        bname = branch_name.get(tag.branch, "")
        for n in names:
            key = norm(n)
            if not key:
                continue
            if tag.iri not in by_branch[bname][key]:
                by_branch[bname][key].append(tag.iri)
            if tag.iri not in globally[key]:
                globally[key].append(tag.iri)
    return by_branch, globally


def build(api_v1_dir, tags, branches):
    by_branch, globally = index_tags(tags, branches)
    rows, stats = [], defaultdict(int)

    for path in sorted(Path(api_v1_dir).glob("*.json")):
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(records, list):
            continue
        for rec in records:
            if not isinstance(rec, dict):
                continue
            code = (rec.get("Full Code") or rec.get("Code") or "").strip()
            name = (rec.get("Name") or rec.get("Short Name") or "").strip()
            if not code or not name:
                continue
            codeset = (rec.get("Code Set") or path.stem).strip()
            branch = CODESET_BRANCH.get(path.stem, "")

            key = norm(name)
            match, confidence = None, "none"
            if branch and key in by_branch[branch]:
                hits = by_branch[branch][key]
                match, confidence = hits[0], "high" if len(hits) == 1 else "medium"
            elif key in globally:
                hits = globally[key]
                match, confidence = hits[0], "medium" if len(hits) == 1 else "low"
            elif norm(code) in globally:
                # Names in some 1.0 files are corrupted; the code may still hit.
                hits = globally[norm(code)]
                match, confidence = hits[0], "medium" if len(hits) == 1 else "low"
            elif branch is None:
                confidence = "retired"

            stats[confidence] += 1
            rows.append({
                "code": code, "name": name, "codeSet": codeset,
                "sourceFile": path.name, "confidence": confidence,
                "match": ({"iri": match, "id": tags[match].id,
                           "label": tags[match].label,
                           "url": f"https://lmss.io/tag/{tags[match].id}/"}
                          if match else None),
            })
    return rows, dict(stats)
