#!/usr/bin/env python3
"""Generate the LMSS tag tree, JSON API and search index for lmss.io.

Writes finished HTML straight to the output directory rather than emitting Jekyll
pages: 18k files through Liquid is impractically slow, and none of these pages
need Liquid. Run it against a built _site.

    python3 scripts/build_lmss.py --out _site
"""

import argparse
import gzip
import hashlib
import html
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lmss_parse as L
import build_crosswalk as C

# The 24 branches grouped by what they describe about a matter. This grouping is
# ours, not SALI's: the ontology has no notion of families, and the homepage says
# so. It exists so 24 tiles read as a structure rather than a list.
FAMILIES = [
    ("subject", "What the work is"),
    ("parties", "Who is involved"),
    ("place", "Where and under what authority"),
    ("things", "What is involved"),
    ("process", "How it runs"),
    ("interop", "Technical"),
]
BRANCH_FAMILY = {
    "Area of Law": "subject",
    "Legal Use Cases": "subject",
    "Service": "subject",
    "Objectives": "subject",
    "Matter Narrative": "subject",

    "Actor / Player": "parties",
    "Legal Entity": "parties",
    "Governmental Body": "parties",
    "Industry and Market": "parties",

    "Location": "place",
    "Forums and Venues": "place",
    "Legal Authorities": "place",
    "Language": "place",

    "Document / Artifact": "things",
    "Asset Type": "things",
    "Currency": "things",
    "Financial Concepts and Metrics": "things",

    "Event": "process",
    "Status": "process",
    "Engagement Attributes": "process",
    "Communication Modality": "process",

    "Standards Compatibility": "interop",
    "Data Format": "interop",
    "System Identifiers": "interop",
}

OWL_URL = "https://raw.githubusercontent.com/{repo}/{ref}/LMSS.owl"
SITE = "https://lmss.io"
CACHE = Path(".cache")

# LMSS 1.0 rev. 2 pages that no longer exist, and where their readers should go.
# GitHub Pages cannot issue a real 301, so these become meta-refresh stubs.
REDIRECTS = {
    "SALI-areas-of-law": "/branch/area-of-law/",
    "SALI-court": "/branch/forums-and-venues/",
    "SALI-currency": "/branch/currency/",
    "SALI-format": "/branch/data-format/",
    "SALI-governmental-body": "/branch/governmental-body/",
    "SALI-industry": "/branch/industry-and-market/",
    "SALI-legal-entity": "/branch/legal-entity/",
    "SALI-locations": "/branch/location/",
    "SALI-matter-narrative": "/branch/matter-narrative/",
    "SALI-player-role": "/branch/actor-player/",
    "SALI-process": "/branch/event/",
    "SALI-process-status": "/branch/status/",
    "SALI-representation-role": "/branch/actor-player/",
    "SALI-trial-type": "/branch/event/",
    "SALI-LMSS-type": "/specification/",
    "SALI-LMSS-version": "/specification/",
    "lmss-codes": "/branch/",
    "lmss-ux-api": "/api/",
    "matter-api": "/api/",
}


# --------------------------------------------------------------------------- data

def fetch_owl(repo, ref):
    CACHE.mkdir(exist_ok=True)
    dest = CACHE / f"LMSS-{ref[:12]}.owl"
    if dest.exists():
        print(f"  using cached {dest}")
        return dest
    url = OWL_URL.format(repo=repo, ref=ref)
    print(f"  downloading {url}")
    with urllib.request.urlopen(url, timeout=180) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    print(f"  {dest.stat().st_size / 1e6:.1f} MB")
    return dest


def read_pin(config_path="_config.yml"):
    """Read the pinned upstream ref without needing a YAML parser."""
    pin, inside = {}, False
    for line in Path(config_path).read_text().splitlines():
        if line.startswith("lmss:"):
            inside = True
            continue
        if inside:
            if line[:1] not in (" ", "\t"):
                break
            if ":" in line:
                k, v = line.strip().split(":", 1)
                pin[k.strip()] = v.strip().split("#")[0].strip().strip('"')
    missing = {"repo", "ref"} - set(pin)
    if missing:
        sys.exit(f"_config.yml lmss: block is missing {', '.join(sorted(missing))}")
    return pin


# --------------------------------------------------------------------------- html

NAV_INCLUDE = Path("_includes/nav.html")


def site_nav():
    """The header markup, read from the include Jekyll uses.

    Deliberately plain HTML with no Liquid, so generated pages and Jekyll pages
    cannot drift apart. check_build.py asserts they match.
    """
    return NAV_INCLUDE.read_text(encoding="utf-8").strip()


def e(s):
    return html.escape(s or "", quote=True)


def label_of(tags, iri):
    t = tags.get(iri)
    if t is None:
        return iri
    return t.label or t.id


def page(title, description, body, canonical, breadcrumbs=None):
    crumbs = ""
    if breadcrumbs:
        links = " <span aria-hidden=\"true\">›</span> ".join(
            f'<a href="{e(h)}">{e(t)}</a>' if h else f"<span>{e(t)}</span>"
            for t, h in breadcrumbs)
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{links}</nav>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — LMSS</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<link rel="stylesheet" href="/assets/css/lmss.css">
<link rel="icon" href="/favicon.ico">
</head>
<body>
{site_nav()}
<main id="main">
{crumbs}
{body}
</main>
<footer class="site">
  <p>The LMSS is published by the <a href="https://sali.org" rel="noopener">SALI Alliance</a>
  under the <a href="https://github.com/sali-legal/LMSS/blob/main/LICENSE" rel="noopener">MIT licence</a>.
  This site is built and maintained by
  <a href="https://www.linkedin.com/in/pietergunst/" rel="noopener">Pieter Gunst</a>,
  and is not affiliated with SALI.
  <a href="/talk-to-us/">Contact</a> &middot;
  <a href="https://github.com/digitallawyer/lmss" rel="noopener">Source</a></p>
</footer>
</body>
</html>
"""


def definition_list(pairs):
    rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in pairs if v)
    return f"<dl class='meta'>{rows}</dl>" if rows else ""


def link_list(tags, iris, limit=None):
    shown = iris[:limit] if limit else iris
    items = "".join(
        f'<li><a href="/tag/{e(tags[i].id)}/">{e(label_of(tags, i))}</a></li>'
        for i in shown if i in tags)
    more = ""
    if limit and len(iris) > limit:
        more = f"<li class='more'>+{len(iris) - limit:,} more</li>"
    return f"<ul class='tags'>{items}{more}</ul>" if items else ""


def render_tag(tags, tag, pin):
    paths = L.ancestry(tags, tag.iri)
    trail = ""
    if paths:
        rendered = []
        for path in paths[:4]:
            steps = " <span aria-hidden='true'>›</span> ".join(
                f'<a href="/tag/{e(tags[i].id)}/">{e(label_of(tags, i))}</a>'
                for i in path[:-1])
            rendered.append(f"<li>{steps or '<span>Top level</span>'}</li>")
        extra = (f"<li class='more'>+{len(paths) - 4:,} more paths</li>"
                 if len(paths) > 4 else "")
        plural = "s" if len(paths) > 1 else ""
        trail = (f"<section><h2>Ancestry path{plural}</h2>"
                 f"<ul class='paths'>{''.join(rendered)}{extra}</ul></section>")

    body = [f"<h1>{e(tag.label or tag.id)}</h1>"]
    if tag.definition or tag.description:
        body.append(f"<p class='lede'>{e(tag.definition or tag.description)}</p>")

    body.append(definition_list([
        ("IRI", f"<code>{e(tag.iri)}</code>"),
        ("Branch", f'<a href="/branch/{e(L.slug(label_of(tags, tag.branch)))}/">'
                   f'{e(label_of(tags, tag.branch))}</a>' if tag.branch else ""),
        ("Children", f"{len(tag.children):,}" if tag.children else ""),
        ("Source", " ".join(f'<a href="{e(s)}" rel="noopener nofollow">{e(s[:60])}</a>'
                            for s in (tag.defined_by + tag.sources)[:3])),
    ]))

    if tag.alt_labels or tag.pref_labels:
        syn = tag.pref_labels + tag.alt_labels
        body.append("<section><h2>Also known as</h2><p class='syn'>"
                    + ", ".join(e(s) for s in syn[:60])
                    + (f" <span class='more'>+{len(syn) - 60:,} more</span>"
                       if len(syn) > 60 else "")
                    + "</p></section>")

    if tag.examples:
        body.append("<section><h2>Examples</h2><ul class='plain'>"
                    + "".join(f"<li>{e(x)}</li>" for x in tag.examples[:20])
                    + "</ul></section>")

    body.append(trail)

    if tag.children:
        body.append(f"<section><h2>Children <span class='count'>{len(tag.children):,}"
                    f"</span></h2>{link_list(tags, tag.children, 300)}</section>")

    if tag.relations:
        rows = "".join(
            f'<li><span class="rel">{e(n)}</span> '
            f'<a href="/tag/{e(tags[t].id)}/">{e(label_of(tags, t))}</a></li>'
            for n, t in tag.relations[:40] if t in tags)
        if rows:
            body.append(f"<section><h2>Relationships</h2><ul class='rels'>{rows}</ul></section>")

    if tag.notes or tag.comment:
        notes = (tag.notes or []) + ([tag.comment] if tag.comment else [])
        body.append("<section><h2>Notes</h2>"
                    + "".join(f"<p>{e(n)}</p>" for n in notes[:6]) + "</section>")

    body.append(
        f"<p class='provenance'>Generated from <code>{e(pin['repo'])}</code> at "
        f"<code>{e(pin['ref'][:12])}</code>"
        + (f" ({e(pin.get('ref_date',''))})" if pin.get("ref_date") else "")
        + f". <a href='/api/v2/tag/{e(tag.id)}.json'>JSON</a></p>")

    crumbs = [("Tags", "/branch/")]
    if tag.branch and tag.branch != tag.iri:
        crumbs.append((label_of(tags, tag.branch),
                       f"/branch/{L.slug(label_of(tags, tag.branch))}/"))
    crumbs.append((tag.label or tag.id, None))

    desc = (tag.definition or tag.description
            or f"{tag.label or tag.id} in the SALI LMSS legal matter standard.")
    return page(tag.label or tag.id, desc[:300], "\n".join(body),
                f"{SITE}/tag/{tag.id}/", crumbs)


def render_branch(tags, branch_iri, members, pin):
    tag = tags[branch_iri]
    name = tag.label or tag.id
    top = tag.children
    body = [f"<h1>{e(name)}</h1>"]
    if tag.definition:
        body.append(f"<p class='lede'>{e(tag.definition)}</p>")
    body.append(f"<p class='count-line'><strong>{len(members):,}</strong> tags in this "
                f"branch, <strong>{len(top):,}</strong> at the top level.</p>")
    body.append(definition_list([
        ("IRI", f"<code>{e(tag.iri)}</code>"),
        ("JSON", f"<a href='/api/v2/branch/{e(L.slug(name))}.json'>"
                 f"/api/v2/branch/{e(L.slug(name))}.json</a>"),
    ]))
    rows = "".join(
        f'<li><a href="/tag/{e(tags[i].id)}/">{e(label_of(tags, i))}</a>'
        f'{f"<span class=n>{len(tags[i].children):,}</span>" if tags[i].children else ""}</li>'
        for i in top)
    body.append(f"<section><h2>Top-level tags</h2><ul class='grid'>{rows}</ul></section>")
    return page(name, tag.definition or f"The {name} branch of the SALI LMSS standard.",
                "\n".join(body), f"{SITE}/branch/{L.slug(name)}/",
                [("Tags", "/branch/"), (name, None)])


def render_branch_index(tags, branches, counts, total):
    ordered = sorted(branches, key=lambda x: -counts[x])
    biggest = counts[ordered[0]] if ordered else 1
    rows = "".join(
        f'<li><a href="/branch/{e(L.slug(label_of(tags, b)))}/" '
        f'data-fam="{e(BRANCH_FAMILY.get(label_of(tags, b), "other"))}">'
        f'<span class="bn">{e(label_of(tags, b))}</span>'
        f'<span class="bbar"><span style="width:{max(1.5, counts[b] / biggest * 100):.1f}%">'
        f'</span></span>'
        f'<span class="n">{counts[b]:,}</span></a></li>'
        for b in ordered)
    body = (f"<h1>LMSS tags</h1><p class='lede'>The complete standard: "
            f"<strong>{total:,}</strong> tags across <strong>{len(branches)}</strong> "
            f"top-level branches, nested up to ten levels deep.</p>"
            f"<ul class='branchlist'>{rows}</ul>")
    return page("LMSS tags", f"All {total:,} tags in the SALI LMSS standard.",
                body, f"{SITE}/branch/", [("Tags", None)])


# --------------------------------------------------------------------------- json

def tag_json(tags, tag, pin):
    return {
        "iri": tag.iri,
        "id": tag.id,
        "label": tag.label,
        "definition": tag.definition or tag.description,
        "prefLabels": tag.pref_labels,
        "altLabels": tag.alt_labels,
        "examples": tag.examples,
        "notes": tag.notes,
        "sources": tag.defined_by + tag.sources,
        "branch": {"iri": tag.branch, "label": label_of(tags, tag.branch)} if tag.branch else None,
        "parents": [{"iri": p, "id": tags[p].id, "label": label_of(tags, p)}
                    for p in tag.parents if p in tags],
        "children": [{"iri": c, "id": tags[c].id, "label": label_of(tags, c)}
                     for c in tag.children],
        "relations": [{"property": n, "iri": t, "label": label_of(tags, t)}
                      for n, t in tag.relations if t in tags],
        "url": f"{SITE}/tag/{tag.id}/",
        "source": {"repo": pin["repo"], "ref": pin["ref"], "channel": pin.get("channel")},
    }


# --------------------------------------------------------------------------- write

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, (dict, list)):
        content = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
    path.write_text(content, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site", help="output directory (a built _site)")
    ap.add_argument("--only-branch", help="generate one branch only, by label")
    ap.add_argument("--owl", help="use a local LMSS.owl instead of downloading")
    ap.add_argument("--stats-only", action="store_true",
                    help="write _data/lmss_stats.json and exit, so Jekyll pages "
                         "can quote real counts instead of hardcoded ones")
    args = ap.parse_args()

    pin = read_pin()
    print(f"pinned: {pin['repo']} @ {pin['ref'][:12]} ({pin.get('ref_date','?')})")
    owl = Path(args.owl) if args.owl else fetch_owl(pin["repo"], pin["ref"])

    print("parsing ontology...")
    tags, branches = L.parse(owl)
    counts = {b: 0 for b in branches}
    for t in tags.values():
        if t.branch in counts:
            counts[t.branch] += 1

    if args.stats_only:
        write_stats(tags, branches, counts, pin, owl)
        return

    if args.only_branch:
        keep = [b for b in branches if (tags[b].label or "") == args.only_branch]
        if not keep:
            sys.exit(f"no branch labelled {args.only_branch!r}. "
                     f"Options: {sorted(tags[b].label for b in branches)}")
        branches = keep
        tags = {i: t for i, t in tags.items() if t.branch in keep}
        print(f"  restricted to {args.only_branch}: {len(tags):,} tags")

    out = Path(args.out)
    print(f"writing to {out}/ ...")

    for tag in tags.values():
        write(out / "tag" / tag.id / "index.html", render_tag(tags, tag, pin))
        write(out / "api" / "v2" / "tag" / f"{tag.id}.json", tag_json(tags, tag, pin))

    for b in branches:
        members = [t for t in tags.values() if t.branch == b]
        name = label_of(tags, b)
        write(out / "branch" / L.slug(name) / "index.html",
              render_branch(tags, b, members, pin))
        write(out / "api" / "v2" / "branch" / f"{L.slug(name)}.json", {
            "iri": b, "label": name, "slug": L.slug(name), "count": len(members),
            "url": f"{SITE}/branch/{L.slug(name)}/",
            "topLevel": [{"iri": c, "id": tags[c].id, "label": label_of(tags, c),
                          "children": len(tags[c].children)} for c in tags[b].children],
        })

    write(out / "branch" / "index.html",
          render_branch_index(tags, branches, counts, len(tags)))

    # Search: labels are small enough to ship eagerly; synonyms load on demand.
    write(out / "search" / "index.json",
          [[t.id, t.label or t.id, L.slug(label_of(tags, t.branch))] for t in tags.values()])
    write(out / "search" / "synonyms.json",
          [[t.id, s] for t in tags.values() for s in (t.pref_labels + t.alt_labels)])

    write(out / "api" / "v2" / "lmss.json", {
        "source": {"repo": pin["repo"], "ref": pin["ref"],
                   "channel": pin.get("channel"), "date": pin.get("ref_date")},
        "count": len(tags),
        "branches": [{"iri": b, "label": label_of(tags, b),
                      "slug": L.slug(label_of(tags, b)), "count": counts.get(b, 0)}
                     for b in branches],
        "tags": [tag_json(tags, t, pin) for t in tags.values()],
    })
    write(out / "api" / "v2" / "index.json", {
        "version": "2", "generated_from": pin,
        "endpoints": {
            "tag": f"{SITE}/api/v2/tag/{{id}}.json",
            "branch": f"{SITE}/api/v2/branch/{{slug}}.json",
            "full": f"{SITE}/api/v2/lmss.json",
            "search": f"{SITE}/search/index.json",
        },
        "deprecated": {"v1": f"{SITE}/api/v1/ — LMSS 1.0 rev. 2, frozen"},
    })

    if not args.only_branch:
        rows, stats = C.build("api/v1", tags, branches)
        write(out / "crosswalk" / "index.html", render_crosswalk(rows, stats, pin))
        write(out / "api" / "v2" / "crosswalk.json",
              {"source": {"repo": pin["repo"], "ref": pin["ref"]},
               "note": "Derived by label matching; review before relying on it.",
               "stats": stats, "codes": rows})
        n_redirects = write_redirects(out)
        n_v1 = stamp_v1_deprecation(out)
        print(f"  crosswalk: {len(rows):,} codes "
              f"({stats.get('high', 0):,} high confidence)")
        print(f"  {n_redirects} redirect stubs, {n_v1} v1 files stamped deprecated")

    write_sitemaps(out, tags, branches)

    files = sum(1 for _ in out.rglob("*") if _.is_file())
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"done: {len(tags):,} tags, {len(branches)} branches, "
          f"{files:,} files, {size / 1e6:.0f} MB")


def write_redirects(out):
    """Meta-refresh stubs. Not a 301 -- Pages has no server config -- so each
    carries a canonical link, which is what search engines actually act on."""
    for old, new in REDIRECTS.items():
        write(out / f"{old}.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved — LMSS</title>
<link rel="canonical" href="{SITE}{new}">
<meta http-equiv="refresh" content="0; url={new}">
<meta name="robots" content="noindex">
</head><body>
<p>This page covered LMSS 1.0 rev. 2 and has been replaced.
<a href="{new}">Continue to its replacement</a>.</p>
</body></html>
""")
    return len(REDIRECTS)


def stamp_v1_deprecation(out):
    """Mark the frozen 1.0 JSON in place. Deliberately not redirected: an HTML
    stub at a .json path hands machine clients HTML and breaks their parser."""
    v1 = out / "api" / "v1"
    if not v1.is_dir():
        return 0
    notice = {
        "deprecated": True,
        "standard": "LMSS 1.0 rev. 2",
        "note": "Frozen 2019 snapshot of a superseded version of the LMSS.",
        "supersededBy": f"{SITE}/api/v2/",
        "crosswalk": f"{SITE}/api/v2/crosswalk.json",
    }
    n = 0
    for path in v1.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        write(path, {**notice, "codes": data} if isinstance(data, list) else
                    {**notice, **data})
        n += 1
    return n


def render_crosswalk(rows, stats, pin):
    order = {"high": 0, "medium": 1, "low": 2, "none": 3, "retired": 4}
    rows = sorted(rows, key=lambda r: (order.get(r["confidence"], 9),
                                       r["codeSet"], r["code"]))
    body = [
        "<h1>LMSS 1.0 → v3 crosswalk</h1>",
        "<p class='lede'>SALI publishes no mapping from the 1.0 rev. 2 mnemonic "
        "codes to current IRIs — the ontology defines a <code>sali:code</code> "
        "annotation, but no tag uses it. This one is derived by matching labels, "
        "so treat it as a starting point for review rather than an authority.</p>",
        definition_list([
            ("Codes", f"{len(rows):,}"),
            ("High confidence", f"{stats.get('high', 0):,} — exact name match "
                                f"inside the successor branch"),
            ("Medium / low", f"{stats.get('medium', 0) + stats.get('low', 0):,} — "
                             f"matched outside the branch, or ambiguous"),
            ("No match", f"{stats.get('none', 0):,}"),
            ("JSON", f"<a href='/api/v2/crosswalk.json'>/api/v2/crosswalk.json</a>"),
        ]),
        "<section><h2>Mapping</h2><div class='tbl'><table>",
        "<thead><tr><th>Code</th><th>1.0 name</th><th>Current tag</th>"
        "<th>Confidence</th></tr></thead><tbody>",
    ]
    for r in rows:
        m = r["match"]
        target = (f"<a href='/tag/{e(m['id'])}/'>{e(m['label'])}</a>" if m
                  else "<span class='none'>—</span>")
        body.append(f"<tr><td><code>{e(r['code'])}</code></td><td>{e(r['name'])}</td>"
                    f"<td>{target}</td>"
                    f"<td><span class='conf {r['confidence']}'>"
                    f"{r['confidence']}</span></td></tr>")
    body.append("</tbody></table></div></section>")
    body.append(f"<p class='provenance'>Derived from the 1.0 rev. 2 code sets "
                f"archived at <code>/api/v1/</code> against "
                f"<code>{e(pin['repo'])}</code> @ <code>{e(pin['ref'][:12])}</code>.</p>")
    return page("LMSS 1.0 to v3 crosswalk",
                "Mapping LMSS 1.0 rev. 2 codes onto current SALI LMSS IRIs.",
                "\n".join(body), f"{SITE}/crosswalk/",
                [("Crosswalk", None)])


def pack_rows(spans, width=12):
    """Grow spans so every row of the mosaic fills the grid exactly.

    sqrt-scaled spans rarely sum to a multiple of the grid width, which leaves
    ragged gaps at the right edge. This greedily packs them into rows in the
    given order, then distributes each row's shortfall across its tiles,
    widest first. Order and relative size survive; the right edge comes out
    flush.
    """
    rows, current = [], []
    for index, span in enumerate(spans):
        if current and sum(s for _, s in current) + span > width:
            rows.append(current)
            current = []
        current.append([index, span])
    if current:
        rows.append(current)

    packed = list(spans)
    for row in rows:
        shortfall = width - sum(s for _, s in row)
        order = sorted(range(len(row)), key=lambda i: -row[i][1])
        while shortfall > 0:
            for i in order:
                if shortfall == 0:
                    break
                row[i][1] += 1
                shortfall -= 1
        for index, span in row:
            packed[index] = span
    return packed


def write_stats(tags, branches, counts, pin, owl):
    """Figures quoted in hand-written prose, so they cannot silently drift."""
    depth, stack = {}, [(b, 1) for b in branches]
    while stack:
        iri, d = stack.pop()
        if iri in depth and depth[iri] <= d:
            continue
        depth[iri] = d
        stack.extend((c, d + 1) for c in tags[iri].children)

    stats = {
        "tags": len(tags),
        "branches": len(branches),
        "definitions": sum(1 for t in tags.values() if t.definition or t.description),
        "synonyms": sum(len(t.pref_labels) + len(t.alt_labels) for t in tags.values()),
        "multi_parent": sum(1 for t in tags.values()
                            if len([p for p in t.parents if p in tags]) > 1),
        "max_depth": max(depth.values()) if depth else 0,
        "object_properties": L.count_object_properties(owl),
        "ref": pin["ref"],
        "ref_date": pin.get("ref_date"),
        # Every branch, largest first. `weight` is sqrt-scaled so the homepage
        # mosaic stays readable: raw counts span 12 to 3,783, which would make
        # the small branches invisible slivers.
        "branch_list": [
            {"label": label_of(tags, b), "slug": L.slug(label_of(tags, b)),
             "count": counts.get(b, 0),
             "count_fmt": f"{counts.get(b, 0):,}",
             "weight": max(4, round(counts.get(b, 0) ** 0.5)),
             # Columns on the homepage's 12-wide grid. sqrt-scaled: raw counts
             # span 12 to 3,783, which would leave most branches as slivers.
             "span": max(2, min(6, round((counts.get(b, 0) ** 0.5) / 9))),
             "family": BRANCH_FAMILY.get(label_of(tags, b), "other")}
            for b in sorted(branches, key=lambda x: -counts.get(x, 0))],
    }
    # Liquid has no thousands-separator filter, so ship pre-formatted strings
    # alongside the raw integers.
    for key in ("tags", "branches", "definitions", "synonyms", "multi_parent",
                "object_properties"):
        stats[f"{key}_fmt"] = f"{stats[key]:,}"

    packed = pack_rows([b["span"] for b in stats["branch_list"]])
    for entry, span in zip(stats["branch_list"], packed):
        entry["span"] = span

    stats["families"] = [{"key": k, "label": v} for k, v in FAMILIES]

    unclassified = sorted(b["label"] for b in stats["branch_list"]
                          if b["family"] == "other")
    if unclassified:
        # A new upstream branch should be classified by a person, not silently
        # rendered grey. The weekly update PR fails here rather than on master.
        print("  WARNING unclassified branches: " + ", ".join(unclassified))
    stats["unclassified"] = unclassified

    # The crosswalk headline number, so the homepage can quote it.
    try:
        rows, cw = C.build("api/v1", tags, branches)
        stats["crosswalk_total"] = len(rows)
        stats["crosswalk_high"] = cw.get("high", 0)
        stats["crosswalk_high_fmt"] = f"{cw.get('high', 0):,}"
    except Exception as exc:                       # archive absent in some checkouts
        print(f"  crosswalk stats skipped: {exc}")

    write(Path("_data") / "lmss_stats.json", stats)
    print(f"  wrote _data/lmss_stats.json ({stats['tags']:,} tags)")
    return stats


def write_sitemaps(out, tags, branches):
    """Split sitemaps: one URL set per 20k is the spec limit, but keep them small."""
    urls = ([f"{SITE}/branch/"]
            + [f"{SITE}/branch/{L.slug(label_of(tags, b))}/" for b in branches]
            + [f"{SITE}/tag/{t.id}/" for t in tags.values()])
    chunks = [urls[i:i + 10000] for i in range(0, len(urls), 10000)]
    for n, chunk in enumerate(chunks, 1):
        body = "".join(f"<url><loc>{html.escape(u)}</loc></url>" for u in chunk)
        write(out / f"sitemap-tags-{n}.xml",
              '<?xml version="1.0" encoding="UTF-8"?>'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
              f"{body}</urlset>")
    idx = "".join(f"<sitemap><loc>{SITE}/sitemap-tags-{n}.xml</loc></sitemap>"
                  for n in range(1, len(chunks) + 1))
    write(out / "sitemap-tags.xml",
          '<?xml version="1.0" encoding="UTF-8"?>'
          '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          f"{idx}</sitemapindex>")




if __name__ == "__main__":
    main()
