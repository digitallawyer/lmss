"""Parse SALI's LMSS.owl into plain Python records.

Stdlib only, deliberately: the build runs on a bare GitHub Actions runner with no
pip install step. The ontology is RDF/XML but regular enough that ElementTree is
sufficient -- we only need classes, their labels/annotations, and subClassOf edges.
"""

import re
import xml.etree.ElementTree as ET
from collections import defaultdict

OWL_THING = "http://www.w3.org/2002/07/owl#Thing"
LMSS_BASE = "http://lmss.sali.org/"

RDF = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
RDFS = "{http://www.w3.org/2000/01/rdf-schema#}"
SKOS = "{http://www.w3.org/2004/02/skos/core#}"
DC = "{http://purl.org/dc/elements/1.1/}"

# Branches SALI ships but that should not be published.
EXCLUDED_BRANCHES = {"ZZZ - SANDBOX: UNDER CONSTRUCTION"}

# Annotations we surface on a tag page, keyed by the local tag name we give them.
SIMPLE_ANNOTATIONS = {
    RDFS + "comment": "comment",
    RDFS + "isDefinedBy": "defined_by",
    RDFS + "seeAlso": "see_also",
    SKOS + "definition": "definition",
    SKOS + "example": "examples",
    SKOS + "note": "notes",
    SKOS + "prefLabel": "pref_labels",
    SKOS + "altLabel": "alt_labels",
    DC + "description": "description",
    DC + "source": "sources",
    DC + "identifier": "identifiers",
}
MULTI = {"examples", "notes", "pref_labels", "alt_labels", "sources",
         "identifiers", "see_also", "defined_by"}


class Tag:
    __slots__ = ("iri", "id", "label", "definition", "comment", "description",
                 "pref_labels", "alt_labels", "examples", "notes", "sources",
                 "identifiers", "see_also", "defined_by", "parents", "children",
                 "relations", "branch")

    def __init__(self, iri):
        self.iri = iri
        self.id = iri.rsplit("/", 1)[-1].lstrip("#")
        self.label = None
        self.definition = self.comment = self.description = None
        for f in MULTI:
            setattr(self, f, [])
        self.parents, self.children, self.relations = [], [], []
        self.branch = None

    def __repr__(self):
        return f"<Tag {self.id} {self.label!r}>"


def _text(el):
    """Literal value of an annotation element, or its rdf:resource if it's a link."""
    if el.text and el.text.strip():
        return el.text.strip()
    res = el.get(RDF + "resource")
    return res.strip() if res else None


def parse(path):
    """Return (tags_by_iri, branch_iris) for the publishable part of the ontology."""
    root = ET.parse(path).getroot()

    tags, object_props = {}, {}
    for el in root:
        if el.tag.endswith("ObjectProperty"):
            iri = el.get(RDF + "about")
            lab = el.find(RDFS + "label")
            if iri:
                object_props[iri] = lab.text if lab is not None else iri.rsplit("/", 1)[-1]

    for el in root:
        if not el.tag.endswith("Class"):
            continue
        iri = el.get(RDF + "about")
        if not iri:
            continue  # anonymous class expression; not a published tag
        tag = tags.get(iri) or Tag(iri)
        tags[iri] = tag

        for child in el:
            ctag = child.tag
            if ctag == RDFS + "label":
                tag.label = (child.text or "").strip() or tag.label
            elif ctag == RDFS + "subClassOf":
                parent = child.get(RDF + "resource")
                if parent:
                    tag.parents.append(parent)
            elif ctag in SIMPLE_ANNOTATIONS:
                field = SIMPLE_ANNOTATIONS[ctag]
                val = _text(child)
                if not val:
                    continue
                if field in MULTI:
                    getattr(tag, field).append(val)
                elif getattr(tag, field) is None:
                    setattr(tag, field, val)
            elif ctag.startswith("{" + LMSS_BASE):
                # A typed relationship (sali:governedBy, sali:superseded, ...).
                target = child.get(RDF + "resource")
                if target:
                    prop = "{" + LMSS_BASE + "}"
                    name = object_props.get(LMSS_BASE + ctag[len(prop):], ctag[len(prop):])
                    tag.relations.append((name, target))

    _link_children(tags)
    branches = _find_branches(tags)
    _assign_branches(tags, branches)
    _drop_excluded(tags, branches)
    return tags, branches


def _link_children(tags):
    for iri, tag in tags.items():
        for parent in tag.parents:
            if parent in tags:
                tags[parent].children.append(iri)
    for tag in tags.values():
        tag.children.sort(key=lambda i: (tags[i].label or "").lower())


def _find_branches(tags):
    """Top-level branches are the direct subclasses of owl:Thing."""
    return [iri for iri, t in tags.items() if OWL_THING in t.parents]


def _assign_branches(tags, branches):
    """Label every tag with its branch. Multi-parent tags take their first path."""
    for root_iri in branches:
        stack, seen = [root_iri], set()
        while stack:
            iri = stack.pop()
            if iri in seen:
                continue
            seen.add(iri)
            if tags[iri].branch is None:
                tags[iri].branch = root_iri
            stack.extend(tags[iri].children)


def _drop_excluded(tags, branches):
    excluded = {i for i in branches if (tags[i].label or "") in EXCLUDED_BRANCHES}
    for iri in excluded:
        branches.remove(iri)
    for iri in [i for i, t in tags.items() if t.branch in excluded]:
        del tags[iri]
    # Scrub dangling edges left behind by the removal.
    live = set(tags)
    for tag in tags.values():
        tag.parents = [p for p in tag.parents if p in live or p == OWL_THING]
        tag.children = [c for c in tag.children if c in live]
        tag.relations = [(n, t) for n, t in tag.relations if t in live]


def ancestry(tags, iri):
    """All root-to-tag paths, since 832 tags have more than one parent."""
    tag = tags.get(iri)
    if tag is None:
        return []
    real = [p for p in tag.parents if p in tags]
    if not real:
        return [[iri]]
    paths = []
    for parent in real:
        for path in ancestry(tags, parent):
            if iri not in path:            # defensive: the graph should be acyclic
                paths.append(path + [iri])
    return paths or [[iri]]


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "untitled"
