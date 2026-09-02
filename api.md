---
layout: page
title: API
description: JSON for every tag and branch, plus a full dump of the standard.
---
Static JSON, served from the same build as the pages. No key, no rate limit, no
sign-up. Every response records the exact upstream commit it was generated from, so
you can always tell which revision of the standard you are holding.

## Endpoints

| Endpoint | Returns |
| --- | --- |
| `/api/v2/index.json` | Version metadata and the endpoint list |
| `/api/v2/tag/{id}.json` | One tag: labels, synonyms, definition, parents, children, relationships |
| `/api/v2/branch/{slug}.json` | A branch and its top-level tags |
| `/api/v2/lmss.json` | **Every tag in the standard**, ~19 MB |
| `/api/v2/crosswalk.json` | LMSS 1.0 codes mapped to current IRIs |
| `/search/index.json` | `[id, label, branch]` for every tag, ~1.3 MB |
| `/search/synonyms.json` | `[id, synonym]` for all {{ site.data.lmss_stats.synonyms_fmt }} synonyms, ~3.9 MB |

The `{id}` is the trailing segment of the IRI: for
`http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz`, the id is `R8AC0Iq3zua7VGgBd0jCBtz`.

## Example

```
curl https://lmss.io/api/v2/tag/R8AC0Iq3zua7VGgBd0jCBtz.json
```

```json
{
  "iri": "http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz",
  "id": "R8AC0Iq3zua7VGgBd0jCBtz",
  "label": "Business Organizations Law",
  "definition": "Law governing the creation and operation of businesses.",
  "altLabels": ["Business Organisations Law", "Gesellschaftsrecht", "商业组织法", "..."],
  "branch": { "label": "Area of Law", "iri": "http://lmss.sali.org/RSYBzf149Mi5KE0YtmpUmr" },
  "parents": [{ "id": "RF0Bb0267149dFC8b5e349a1", "label": "Corporate Law" }],
  "children": [],
  "relations": [],
  "source": { "repo": "sali-legal/LMSS", "ref": "3f9ac0c9...", "channel": "pre-release" }
}
```

**Take the full dump, not 18,000 requests.** If you need more than a handful of
tags, fetch `/api/v2/lmss.json` once and work locally. It is a single file
containing the entire standard with all parent and child links intact, which is what
you need anyway to expand the hierarchy at query time.

## SALI's own API standard

This API serves the *contents* of the standard. How two systems exchange LMSS-tagged
matters with each other is a different question, covered by SALI's draft API standard
at [`sali-legal/api`](https://github.com/sali-legal/api/blob/main/SALI_API.yml).
If you are designing an integration between legal systems rather than loading the
taxonomy, read that one.

## Version 1 is deprecated

The previous API published LMSS 1.0 rev. 2 code sets at `/api/v1/`. Those files are
**still served** so existing integrations don't break, but they describe a
superseded version of the standard and are not maintained. Every v1 response now
carries a `deprecated` flag and a pointer here.

If you are on v1, the [crosswalk](/crosswalk/) maps your codes to current IRIs.
