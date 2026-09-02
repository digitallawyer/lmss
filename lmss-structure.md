---
layout: page
title: Using LMSS on a matter
description: How a tag attaches to a matter, and how systems exchange them.
---
The [specification](/specification/) covers how the standard is built. This page
covers the part you actually implement: getting tags onto a matter and moving them
between systems.

## A matter is a set of tags

There is no single "matter record" in the LMSS. A matter is described by attaching
tags from different branches, each answering a different question:

| Question | Branch |
| --- | --- |
| What kind of law is this? | Area of Law |
| What is the client's industry? | Industry and Market |
| Who is involved, and in what role? | Actor / Player |
| Where is it? | Location |
| Which court or tribunal? | Forums and Venues |
| Which agency or authority? | Governmental Body |
| What documents are involved? | Document / Artifact |
| What is being produced or sought? | Objectives, Service |
| What state is it in? | Status |

You use as many or as few as your system needs. A matter tagged only with an Area of
Law is still validly described; the standard has no required-field rule of the kind
LMSS 1.0 had.

## Store IRIs

The one implementation rule that matters:

> Store the IRI. Render the label.

Labels change between releases; IRIs do not. A system that stores
`http://lmss.sali.org/R8AC0Iq3zua7VGgBd0jCBtz` keeps working when SALI renames that
tag. A system that stored "Business Organizations Law" as a string quietly breaks.

Keep a local copy of the tag's label for display and search, refresh it when you
update your snapshot of the standard, but always treat the IRI as the key.

## Specificity and the hierarchy

Tag as **deeply** as the facts support, and let consumers walk up.

Because tags are arranged hierarchically, a matter tagged with a leaf is implicitly
also described by every ancestor of that leaf. A matter tagged *Business
Organizations Law* is a *Corporate Law* matter and an *Area of Law* matter without
anyone storing those separately. This is why SALI's API standard specifies that a
response returns the lowest descendant — the leaf — and leaves the caller to map
ancestry on their own side.

The practical consequence: your query layer needs the hierarchy, not just the tags.
When someone asks for all Corporate Law matters, you must expand that to every
descendant IRI before matching. The [full JSON dump](/api/) includes each tag's
parents and children so you can build that expansion locally.

## Exchanging matters between systems

SALI publishes a draft API standard, an OpenAPI description at
[`sali-legal/api`](https://github.com/sali-legal/api/blob/main/SALI_API.yml), which
defines how two systems exchange LMSS-tagged matters and documents. Its shape:

- `/supported/tags` — an implementer declares which tags and custom fields it
  understands, so a caller knows what it can ask for.
- Matter and document endpoints carry LMSS IRIs as identifiers throughout, in both
  requests and responses.
- Responses return leaf tags; parent-child expansion is the caller's job.

It is explicitly a draft, and worth reading before you design your own interchange
format rather than after.

## A worked example

A wage and hour class action in Georgia, expressed as tags rather than as a
document:

```json
{
  "matter": "Wage and hour class action against XYZ Corp.",
  "tags": [
    "http://lmss.sali.org/<area-of-law:-wage-and-hour>",
    "http://lmss.sali.org/<forum:-n.d.-georgia>",
    "http://lmss.sali.org/<location:-georgia>",
    "http://lmss.sali.org/<player-role:-plaintiff>",
    "http://lmss.sali.org/<legal-entity:-class>"
  ]
}
```

Each placeholder is a real IRI you can look up here — start from
[the branch browser](/branch/) or [search](/search/). Compare this with the nested
Header/Matter document that LMSS 1.0 required, and the shift is clear: the structure
moved out of the payload and into the identifiers.
