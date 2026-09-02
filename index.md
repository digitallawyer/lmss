---
layout: home
title: The legal matter standard
description: Every tag in SALI's Legal Matter Specification Standard. Browsable, searchable, and in JSON.
---
<section class="hero">
  <h1>LMSS</h1>
  <p class="hero-sub">SALI's standard vocabulary for describing legal work.</p>

  <form class="hero-search" action="/search/" method="get" role="search">
    <label class="sr-only" for="hq">Search the standard</label>
    <input type="search" id="hq" name="q" autocomplete="off"
           placeholder="Search {{ site.data.lmss_stats.tags_fmt }} tags">
    <button type="submit">Search</button>
  </form>
  <p class="hero-eg">Try
    <a href="/search/?q=wage+and+hour">wage and hour</a>,
    <a href="/search/?q=demurrer">demurrer</a>,
    <a href="/search/?q=arbitration">arbitration</a>.</p>
</section>

<section class="map-section">
  <div class="map-head">
    <h2>{{ site.data.lmss_stats.branches }} branches <span>sized by tag count</span></h2>
    <a href="/branch/">All tags &rarr;</a>
  </div>
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
      <h3>Introduction</h3>
      <p>What the LMSS is and why it's useful.</p>
    </a>
    <a class="card" href="/getting-started/">
      <h3>Getting started</h3>
      <p>Find a tag, store it, query it back.</p>
    </a>
    <a class="card" href="/api/">
      <h3>API</h3>
      <p>JSON for every tag. No key needed.</p>
    </a>
    <a class="card" href="/crosswalk/">
      <h3>Crosswalk</h3>
      <p>LMSS 1.0 codes mapped to current IRIs.</p>
    </a>
  </div>
</section>
