---
layout: page
title: Getting started
description: Find a tag, store it, query it back.
---
## 1. Find the tag

Start from [the branch browser](/branch/) if you know roughly where a concept sits,
or [search](/search/) if you have a phrase. Search covers labels first and synonyms
on request, which matters because much of the standard's usefulness is in its {{ site.data.lmss_stats.synonyms_fmt }}
alternative names — *Motion to Dismiss* also being *Demurrer* and *MTD*.

Every tag has a permanent page. The one you want looks like:

```
https://lmss.io/tag/R8AC0Iq3zua7VGgBd0jCBtz/
```

That page shows the definition, every synonym, every ancestry path, the children,
and the IRI to store.

## 2. Pull it into your system

Each tag page has a JSON twin:

```
https://lmss.io/api/v2/tag/R8AC0Iq3zua7VGgBd0jCBtz.json
```

For anything beyond a lookup, take the branch or the full dump instead of fetching
tags one at a time — see [the API](/api/). A typical first integration loads one
branch, usually Area of Law, into a local table with `iri`, `label`, `parent` and
`definition` columns.

## 3. Store the IRI

Add a column for the IRI on your matter table, or a join table if a matter can carry
several tags from the same branch, which it usually can. Keep the label alongside
it for display, and treat that copy as a cache you refresh, not as the key.

## 4. Query it back

**Expand the hierarchy before you match.** This is the step that gets missed. Someone
asking for Corporate Law matters expects everything underneath it too. Build a descendant
lookup from the `children` arrays in the JSON, then match against the expanded set.

Without that expansion, a matter tagged *Business Organizations Law* will not appear
in a search for *Corporate Law*, and the tagging will look broken when it is not.

## 5. Keep it current

The standard moves. Pin a version, record which one you loaded, and refresh
deliberately — every JSON response here carries the exact upstream commit it was
generated from, so you can tell what you are running against.

If you are migrating data tagged under LMSS 1.0, start at the
[crosswalk](/crosswalk/).
