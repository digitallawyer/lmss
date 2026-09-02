---
layout: home
title: The legal matter standard, in full
description: Every tag in the SALI Legal Matter Specification Standard — browsable, searchable, and available as JSON.
---
<section class="hero">
  <h1>The legal matter standard, in full</h1>
  <p class="hero-sub">The LMSS is the legal industry's shared vocabulary for describing
  legal work. This site publishes all {{ site.data.lmss_stats.tags_fmt }} tags of it:
  every definition, every synonym, every relationship — as pages you can link to and
  JSON you can build on.</p>

  <form class="hero-search" action="/search/" method="get" role="search">
    <label class="sr-only" for="hq">Search the standard</label>
    <input type="search" id="hq" name="q" autocomplete="off"
           placeholder="Search {{ site.data.lmss_stats.tags_fmt }} tags — “wage and hour”, “demurrer”, “NAICS”">
    <button type="submit">Search</button>
  </form>
  <p class="hero-eg">Or start from
    <a href="/branch/area-of-law/">Area of Law</a>,
    <a href="/branch/industry-and-market/">Industry</a>,
    <a href="/branch/forums-and-venues/">Forums and Venues</a>.</p>
</section>

<section class="map-section">
  <h2 class="map-head">
    <span>The {{ site.data.lmss_stats.branches }} branches</span>
    <a href="/branch/">Browse all &rarr;</a>
  </h2>
  <p class="map-note">Sized by how many tags each one holds.</p>
  <div class="mosaic">
    {% for b in site.data.lmss_stats.branch_list %}
    <a class="tile" href="/branch/{{ b.slug }}/" style="--span:{{ b.span }}">
      <span class="tile-name">{{ b.label }}</span>
      <span class="tile-n">{{ b.count_fmt }}</span>
    </a>
    {% endfor %}
  </div>
</section>

<section>
  <div class="cards">
    <a class="card" href="/a-brief-introduction/">
      <h3>New to the LMSS?</h3>
      <p>What it is, why matter coding pays off, and what changed when the standard
      became an ontology.</p>
    </a>
    <a class="card" href="/getting-started/">
      <h3>Putting it to work</h3>
      <p>Find the right tag, store it against a matter, and query it back without
      losing the hierarchy.</p>
    </a>
    <a class="card" href="/api/">
      <h3>API</h3>
      <p>JSON for every tag and branch, plus a single-file dump of the whole standard.
      No key, no rate limit.</p>
    </a>
    <a class="card" href="/crosswalk/">
      <h3>Migrating from LMSS 1.0?</h3>
      <p>SALI publishes no mapping from the old mnemonic codes to current IRIs.
      This one covers {{ site.data.lmss_stats.crosswalk_high_fmt }} of them.</p>
    </a>
  </div>
</section>
