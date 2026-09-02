---
layout: page
title: Specification
description: "How the LMSS is built: identifiers, branches, labels, relationships and versioning."
---
The Legal Matter Specification Standard is published by the [SALI
Alliance](https://sali.org) as an **OWL ontology**: a set of concepts, each with a
stable identifier, arranged in a hierarchy and connected by typed relationships.
The first release worked differently: it was a document format wrapped around a set
of flat code lists.

## Identifiers

Every tag has one permanent identifier, an **IRI**, of the form:

```
http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz
```

The trailing segment carries no meaning, and that is the point. A tag can be renamed,
redefined, moved under a different parent or given new synonyms, and any system holding
the IRI still resolves to the right concept. SALI's guidance is that released IRIs stay
operative indefinitely, and that deprecation, where it happens, is usually consolidation
of duplicates rather than deletion.

So store the IRI and render the label. Labels are the part of a tag SALI expects to keep
changing.

## Structure

The ontology has **{{ site.data.lmss_stats.branches_fmt }} publishable top-level branches**. Each is an ordinary tag that
happens to sit at the root, and everything below it is a `rdfs:subClassOf`
descendant. The tree runs up to **ten levels deep**.

Branches are not a fixed schema. They are subject areas (Area of Law, Industry and
Market, Forums and Venues, Governmental Body, Document / Artifact, Location and so on),
and SALI adds to them between releases. [Browse them all](/branch/).

### Multiple parentage

A tag may have more than one parent, and **{{ site.data.lmss_stats.multi_parent_fmt }} of
them do**: a concept that is both a kind of document and a kind of event sits under both.
So the LMSS is a directed graph rather than a strict tree, and code that walks it has to
cope with a node being reachable by several routes. On this site each tag has one
canonical URL and lists every ancestry path it has.

## Properties on a tag

| Property | What it holds |
| --- | --- |
| `rdfs:label` | The common English name. One per tag. |
| `skos:prefLabel` | The second-most-common English name. |
| `skos:altLabel` | Synonyms, abbreviations and translations. There are {{ site.data.lmss_stats.synonyms_fmt }} of these. |
| `skos:definition` | A prose definition. {{ site.data.lmss_stats.definitions_fmt }} tags carry one. |
| `skos:example` | Illustrative instances. |
| `rdfs:isDefinedBy`, `dc:source` | Where the concept came from — NAICS, a court's own site, a statute. |
| `rdfs:subClassOf` | Parent tags. |

Synonyms carry language tags, so `altLabel` is where translations live: *Business
Organizations Law* also appears as *Gesellschaftsrecht*, *Derecho de Sociedades*
and 商业组织法. If you are matching free text against the standard, the synonym set
is the part that does the work.

## Relationships

Beyond the hierarchy, the ontology defines **{{ site.data.lmss_stats.object_properties_fmt }} object properties** — typed edges
between tags such as `sali:governedBy`, `sali:superseded` and `rdfs:seeAlso`. These
express things a flat code list cannot: that a proceeding is governed by a
particular authority, or that one instrument superseded another. Where a tag has
them, they appear in its Relationships section.

## Versioning

SALI maintains the ontology on the `main` branch of
[`sali-legal/LMSS`](https://github.com/sali-legal/LMSS) and cuts formal releases
periodically. Between releases, `main` is explicitly provisional — SALI's own README
warns that commits remain subject to public review until a release is cut.

The practical position today is awkward. The only tagged release, `v2.0.0`, holds
**10,489 tags**. Current `main` holds **{{ site.data.lmss_stats.tags_fmt }}**. Building
against the tag would mean building against a standard missing well over a third of
itself.

**This site therefore renders a pinned commit of `main`**, recorded in the repo and
shown in the footer of every page, and treats it as pre-release. The pin only moves
through a reviewed pull request that lists exactly which tags were added, removed or
renamed. See [the API](/api/) for how to read the version out of the data itself.

## What happened to LMSS 1.0

The first release, LMSS 1.0 rev. 2, specified an interchange *document* — a Header
and one or more Matter containers, with enumerated values drawn from sixteen flat
code sets like `SALI-AOL` and `SALI-COURT`. Codes were short mnemonics: `LEMP-WGHR`
for wage and hour law, `PLTF` for plaintiff.

That model has been superseded. Tags are addressed by IRI, and the interchange
question is answered by [SALI's API standard](/api/) rather than by a document
schema. The [1.0 → v3 crosswalk](/crosswalk/) maps the old codes onto current tags,
and the original 1.0 rev. 2 specification remains available as a
[historical document]({{ '/assets/pdf/SALI-LMSS-1.0-rev2c.pdf' | relative_url }}).
