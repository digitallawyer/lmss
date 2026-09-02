---
layout: home
title: The legal matter standard, in full
description: Every tag in the SALI Legal Matter Specification Standard, browsable and machine-readable.
---
<div class="hero">
<h1>The legal matter standard, in full</h1>
<p>The LMSS is the legal industry's shared vocabulary for describing legal work —
what kind of matter it is, who is involved, where it sits, and what is being done.
This site publishes the whole thing: every tag, with its definition, synonyms and
relationships, as pages you can link to and JSON you can build on.</p>
</div>

<div class="stat-row">
  <div class="stat"><b>{{ site.data.lmss_stats.tags_fmt }}</b><span>Tags</span></div>
  <div class="stat"><b>24</b><span>Branches</span></div>
  <div class="stat"><b>{{ site.data.lmss_stats.definitions_fmt }}</b><span>Definitions</span></div>
  <div class="stat"><b>{{ site.data.lmss_stats.synonyms_fmt }}</b><span>Synonyms</span></div>
</div>

<div class="cards">
  <a class="card" href="/a-brief-introduction/">
    <h3>A brief introduction</h3>
    <p>What the LMSS is, why matter coding matters, and what changed when the standard became an ontology.</p>
  </a>
  <a class="card" href="/branch/">
    <h3>Browse the tags</h3>
    <p>All {{ site.data.lmss_stats.branches_fmt }} branches, from Area of Law to Governmental Body, down to the leaf.</p>
  </a>
  <a class="card" href="/specification/">
    <h3>Specification</h3>
    <p>How the standard is built: IRIs, branches, labels, relationships, versioning.</p>
  </a>
  <a class="card" href="/getting-started/">
    <h3>Getting started</h3>
    <p>Find the right tag, store it against a matter, and query it back.</p>
  </a>
  <a class="card" href="/api/">
    <h3>API</h3>
    <p>JSON for every tag and branch, plus a full dump of the standard.</p>
  </a>
  <a class="card" href="/crosswalk/">
    <h3>1.0 → v3 crosswalk</h3>
    <p>Mapping the old mnemonic codes onto current IRIs. Nobody else publishes this.</p>
  </a>
</div>
