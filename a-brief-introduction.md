---
layout: page
title: A brief introduction
description: What the LMSS is, why it exists, and what changed when it became an ontology.
---
## What is the LMSS?

The **Legal Matter Specification Standard** is a standard way to describe a legal
matter — a piece of legal work, or a grouping of work around a legal issue. It is
published by the [SALI Alliance](https://sali.org), it is open, and anyone can use
it for free.

The idea is simple. Manufactured goods have product codes; legal work does not. The
LMSS is a shared vocabulary for saying what a piece of legal work actually *is* — its
area of law, the client's industry, the forum, the parties and their roles, the
documents involved — in terms that every system in the industry can read the same way.

## Why it matters

Matter coding makes buying, staffing, pricing and delivering legal services more
tractable, because it makes comparison possible.

Take a wage and hour class action. If the client can state the kind of matter in
codes, the firm can search its own history by those same codes: which comparable
matters it has handled, which lawyers have the most relevant experience, and — if
the client wants a fixed fee — what those comparable matters actually cost. None of
that works when every organisation describes the same matter in its own words.

The value is not in any single tag. It is in two systems using the *same* tag.

<p><iframe width="560" height="315" style="max-width:100%;border:1px solid var(--rule);border-radius:4px"
  src="https://www.youtube.com/embed/XdcMBHTNE6M" title="SALI LMSS: An introduction"
  loading="lazy" frameborder="0" allowfullscreen></iframe></p>

<p class="hint">Recorded in 2019, so it describes the standard's first release. The
fundamentals still hold; the mechanics have moved on, as below.</p>

## What changed: from code lists to an ontology

The first release of the LMSS was a document format with sixteen flat code lists.
Codes were short mnemonics — `LEMP-WGHR` for wage and hour law, `PLTF` for
plaintiff — and a matter was expressed as a nested JSON document with a required
Header and Matter structure.

SALI has since rebuilt the standard as an **ontology**. Three practical differences:

**It is much larger.** Roughly 117 areas of law became 161; 458 courts became 2,172
forums and venues; 45 industry codes became 2,183 aligned to NAICS. The standard now
holds **{{ site.data.lmss_stats.tags_fmt }} tags** across {{ site.data.lmss_stats.branches_fmt }} branches, including whole areas — documents, matter
phases, objectives — that had no equivalent before.

**Tags have opaque permanent identifiers.** Instead of `LEMP-WGHR`, a tag is
identified by an IRI like `http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz`. That looks
worse to read and is much better to build on: the label can change without breaking
every system that stored it.

**It records relationships, not just membership.** Tags carry definitions, synonyms
across languages, and typed links to other tags. The standard can now express that
one thing is governed by another, or supersedes it — which a flat list of codes
never could.

## Where to go next

- [Browse the tags](/branch/) — all {{ site.data.lmss_stats.branches_fmt }} branches, down to the leaf
- [Specification](/specification/) — how the standard is built
- [Using LMSS on a matter](/lmss-structure/) — the implementation view
- [Getting started](/getting-started/) — find a tag, store it, query it back
- [1.0 → v3 crosswalk](/crosswalk/) — if you hold data coded under the old release
