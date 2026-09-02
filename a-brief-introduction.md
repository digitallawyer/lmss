---
layout: page
title: A brief introduction
description: What the LMSS is, why it exists, and what changed when it became an ontology.
---
## What is the LMSS?

The Legal Matter Specification Standard is a standard way to describe a legal matter:
a piece of legal work, or a grouping of work around a legal issue. It is published by
the [SALI Alliance](https://sali.org), it is open, and anyone can use it for free.

The idea is borrowed from manufacturing. Physical goods have product codes; legal work
has never had an equivalent. The LMSS supplies one. It gives you a shared way to say
what a piece of legal work actually is: its area of law, the client's industry, the
forum, the parties and their roles, the documents involved.

## Why it matters

Matter coding makes buying, staffing, pricing and delivering legal services more
efficient, because it makes work comparable.

Take a wage and hour class action in Georgia. If the client can state the kind of
matter in tags, the firm can search its own history against those same tags. Which
comparable matters has it handled? Which lawyers worked on them? If the client wants a
fixed fee, what did those matters actually cost to run?

None of that is possible when every organisation describes the same case in its own
words. Two firms will call it a "wage and hour class action", an "FLSA collective
action" and a "employment class claim", and no database can tell they mean the same
thing. Tags fix that, but only when both sides use the same ones.

<p><iframe width="560" height="315" style="max-width:100%;border:1px solid var(--rule);border-radius:6px"
  src="https://www.youtube.com/embed/XdcMBHTNE6M" title="SALI LMSS: An introduction"
  loading="lazy" frameborder="0" allowfullscreen></iframe></p>

<p class="hint">Recorded in 2019, so it covers the standard's first release. The
reasoning still holds; the mechanics have moved on, as below.</p>

## From code lists to an ontology

The first release was a document format wrapped around sixteen flat code lists. Codes
were short mnemonics: `LEMP-WGHR` for wage and hour law, `PLTF` for plaintiff. A matter
was a nested JSON document with a required Header and Matter structure.

SALI has since rebuilt the standard as an ontology. Three things changed in practice.

**It got much bigger.** Roughly 117 areas of law became 152. The 458 courts became
1,880 forums and venues. The 45 industry codes became 2,184, aligned to NAICS. The
standard now holds {{ site.data.lmss_stats.tags_fmt }} tags across
{{ site.data.lmss_stats.branches }} branches, and whole subject areas that had no
equivalent before: documents, matter phases, objectives.

**Tags got permanent identifiers.** Instead of `LEMP-WGHR`, each tag is identified by
an IRI like `http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz`. Harder to read, far safer
to build on. SALI can rename a tag whenever the profession's language shifts, and every
system that stored the IRI keeps working.

**It records relationships.** Tags carry definitions, synonyms in a dozen languages,
and typed links to other tags. A flat list can only say what exists. An ontology can
say that one thing is governed by another, or supersedes it.

## Where to go next

[Browse the tags](/branch/) to see the whole thing. The
[specification](/specification/) covers how it is built, and
[using LMSS on a matter](/lmss-structure/) covers how to implement it.
[Getting started](/getting-started/) is the short version of both.

If you hold data coded under LMSS 1.0, start at the [crosswalk](/crosswalk/).
