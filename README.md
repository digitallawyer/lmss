# lmss.io

A browsable, machine-readable rendering of the [SALI](https://sali.org) **Legal Matter
Specification Standard (LMSS)**, published at [lmss.io](https://lmss.io) by
[Legal.io](https://www.legal.io).

The site is generated from SALI's own ontology — [`sali-legal/LMSS`](https://github.com/sali-legal/LMSS)
`LMSS.owl` — at a pinned commit recorded in `_config.yml` under `lmss.ref`. Nothing in the
tag tree is hand-maintained.

## What's here

| Path | What it is |
| --- | --- |
| `/tag/<iri>` | One page per LMSS tag: definition, synonyms, ancestry, children, relationships |
| `/branch/<slug>` | Index for each top-level branch of the ontology |
| `/api/v2/` | JSON for every tag and branch, plus a full dump |
| `/specification`, `/lmss-structure` | How the standard works, written out |
| `/api/v1/` | **Deprecated.** Frozen LMSS 1.0 rev. 2 code sets, kept so old integrations don't break |

## Building

```
bundle install
python3 scripts/build_lmss.py --stats-only   # writes _data/lmss_stats.json
bundle exec jekyll build
python3 scripts/build_lmss.py --out _site    # writes the tag tree into _site
python3 scripts/check_build.py _site
```

`scripts/build_lmss.py` downloads the pinned `LMSS.owl` (cached in `.cache/`) and parses
it. The order matters: the stats pass must run first so Jekyll can quote real counts,
and the tree is written into `_site` *after* Jekyll, because ~18k pages through Liquid
would take hours where writing them directly takes seconds.

Serve the result with any static server, e.g. `python3 -m http.server -d _site`.
Use `--only-branch "Area of Law"` to iterate on a small subset.

## Updating the standard

The pinned ref is bumped by the `update-lmss` workflow, which opens a pull request with a
diff of added, changed and removed tags. The site never follows upstream `main` automatically.

## Licence

Site code is MIT (see `LICENSE.md`). lmss.io is not affiliated with SALI.

The LMSS itself is © SALI Alliance. **Its licensing is genuinely ambiguous and worth
knowing about before reusing anything here:**

- [sali.org](https://sali.org/explore-the-standard/) states **CC BY-ND 4.0**, with a
  reasoned rationale: SALI-licensed material "cannot be used to create competing
  standards or distributed derivatives", though stakeholders may "freely incorporate
  SALI into their systems and adapt it for their internal use".
- The [`sali-legal/LMSS`](https://github.com/sali-legal/LMSS/blob/main/LICENSE) repo
  ships **MIT**, as do `sali-legal/api` and `sali-legal/tools`. MIT has been there since
  the initial commit in 2022; the file has been edited three times since, but only ever
  on the copyright line.
- `LMSS.owl` carries no licence statement of its own.

This site follows the more restrictive of the two, CC BY-ND, since it is the
rights-holder's own published policy. It reproduces SALI's labels and definitions with
attribution and points at SALI as canonical, rather than presenting an altered version
of the standard. The branch families on the homepage and the 1.0 crosswalk are our own
additions and are labelled as such.
