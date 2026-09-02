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
python3 scripts/build_lmss.py --out _generated
bundle exec jekyll serve
```

`scripts/build_lmss.py` downloads the pinned `LMSS.owl` (cached in `.cache/`), parses it,
and writes the generated tree. Jekyll then builds the hand-written pages around it.

## Updating the standard

The pinned ref is bumped by the `update-lmss` workflow, which opens a pull request with a
diff of added, changed and removed tags. The site never follows upstream `main` automatically.

## Licence

Site code is MIT (see `LICENSE.md`). The LMSS itself is published by the SALI Alliance
under [its own licence](https://github.com/sali-legal/LMSS/blob/main/LICENSE); lmss.io is
not affiliated with SALI.
