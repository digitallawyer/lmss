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

OWL_URL = "https://raw.githubusercontent.com/{repo}/{ref}/LMSS.owl"
SITE = "https://lmss.io"
CACHE = Path(".cache")


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
<header class="site">
  <a class="brand" href="/"><strong>LMSS</strong><span>IO</span></a>
  <nav><a href="/branch/">Tags</a> <a href="/specification">Specification</a>
       <a href="/api">API</a> <a href="/search">Search</a></nav>
</header>
<main>
{crumbs}
{body}
</main>
<footer class="site">
  <p>Generated from the <a href="https://sali.org" rel="noopener">SALI Alliance</a>
     LMSS ontology. lmss.io is not affiliated with SALI.</p>
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
    rows = "".join(
        f'<li><a href="/branch/{e(L.slug(label_of(tags, b)))}/">'
        f'{e(label_of(tags, b))}</a><span class="n">{counts[b]:,}</span></li>'
        for b in sorted(branches, key=lambda x: -counts[x]))
    body = (f"<h1>LMSS tags</h1><p class='lede'>The complete standard: "
            f"<strong>{total:,}</strong> tags across <strong>{len(branches)}</strong> "
            f"top-level branches.</p><ul class='grid'>{rows}</ul>")
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

    write_sitemaps(out, tags, branches)
    write_css(out)

    files = sum(1 for _ in out.rglob("*") if _.is_file())
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"done: {len(tags):,} tags, {len(branches)} branches, "
          f"{files:,} files, {size / 1e6:.0f} MB")


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


def write_css(out):
    write(out / "assets" / "css" / "lmss.css", """
:root{--paper:#fbfbfa;--surface:#fff;--rule:#e2e4e8;--ink:#1a1d23;--soft:#5a6270;
--faint:#8a919e;--accent:#0f5c63;--accent-dim:#eaf3f3}
@media(prefers-color-scheme:dark){:root{--paper:#15181d;--surface:#1c2026;--rule:#2f353f;
--ink:#e8ebef;--soft:#a5adba;--faint:#79818f;--accent:#5fb6bc;--accent-dim:#173235}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);line-height:1.6;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header.site,footer.site{border-bottom:1px solid var(--rule);background:var(--surface)}
footer.site{border:0;border-top:1px solid var(--rule);margin-top:48px}
header.site{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:center;
padding:14px 24px;position:sticky;top:0;z-index:5}
.brand{text-decoration:none;color:var(--ink);font-weight:700;letter-spacing:.02em}
.brand span{color:var(--accent);margin-left:4px;font-weight:500}
header.site nav{display:flex;gap:18px;font-size:14px}
main{max-width:860px;margin:0 auto;padding:28px 24px 64px}
footer.site p{max-width:860px;margin:0 auto;padding:16px 24px;font-size:13px;color:var(--faint)}
h1{font-size:clamp(24px,4vw,34px);line-height:1.15;margin:.2em 0 .4em}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:var(--soft);
margin:34px 0 10px}
h2 .count{color:var(--faint);font-weight:400;text-transform:none;letter-spacing:0}
.lede{font-size:18px;color:var(--soft);max-width:66ch}
.count-line{color:var(--soft)}
.crumbs{font-size:13px;color:var(--faint);margin-bottom:8px}
.crumbs a{color:var(--soft)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
background:var(--accent-dim);padding:.12em .38em;border-radius:3px;word-break:break-all}
dl.meta{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:18px 0;
font-size:14px;border-top:1px solid var(--rule);padding-top:14px}
dl.meta dt{color:var(--faint);text-transform:uppercase;font-size:11px;letter-spacing:.07em;
padding-top:.35em}
dl.meta dd{margin:0}
ul.tags,ul.grid,ul.paths,ul.rels,ul.plain{list-style:none;padding:0;margin:0}
ul.tags,ul.grid{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
border-radius:4px;overflow:hidden}
@media(min-width:620px){ul.tags,ul.grid{grid-template-columns:1fr 1fr}}
ul.tags li,ul.grid li{background:var(--surface);padding:9px 14px;display:flex;
justify-content:space-between;gap:12px;font-size:15px}
ul.grid .n,ul.tags .n{color:var(--faint);font-size:13px;font-variant-numeric:tabular-nums}
li.more{color:var(--faint);font-style:italic}
ul.paths li,ul.rels li,ul.plain li{padding:5px 0;border-bottom:1px solid var(--rule);
font-size:15px}
.rel{color:var(--faint);font-size:12px;text-transform:uppercase;letter-spacing:.06em;
margin-right:8px}
.syn{color:var(--soft);max-width:70ch}
.provenance{margin-top:40px;padding-top:14px;border-top:1px solid var(--rule);
font-size:13px;color:var(--faint)}
""".strip())


if __name__ == "__main__":
    main()
