---
layout: page
title: Search
description: Search every tag in the standard by name, synonym or identifier.
---
<p class="hint">Searching all {{ site.data.lmss_stats.tags_fmt }} tags.</p>
<input type="search" id="q" placeholder="Search the standard — try “demurrer”, “NAICS”, or an IRI"
       autocomplete="off" autofocus aria-label="Search LMSS tags">
<p class="hint" id="status">Loading the index…</p>
<ul id="results"></ul>

<script>
(function () {
  var q = document.getElementById('q'),
      status = document.getElementById('status'),
      out = document.getElementById('results'),
      tags = null, syn = null, synLoading = false;

  // Accept ?q= so the homepage search box can hand off to this page.
  var initial = new URLSearchParams(location.search).get('q');
  if (initial) q.value = initial;

  fetch('/search/index.json')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      tags = d;
      status.textContent = d.length.toLocaleString() + ' tags indexed. Synonyms load when you search.';
      if (q.value) run();
    })
    .catch(function () { status.textContent = 'Could not load the search index.'; });

  // 3.9 MB of synonyms is worth fetching, but not before someone actually searches.
  function loadSynonyms() {
    if (syn || synLoading) return;
    synLoading = true;
    fetch('/search/synonyms.json')
      .then(function (r) { return r.json(); })
      .then(function (d) { syn = d; run(); })
      .catch(function () { synLoading = false; });
  }

  function run() {
    var term = q.value.trim().toLowerCase();
    out.innerHTML = '';
    if (!tags || term.length < 2) {
      status.textContent = tags
        ? tags.length.toLocaleString() + ' tags indexed. Type at least two characters.'
        : 'Loading the index…';
      return;
    }
    loadSynonyms();

    var hits = [], seen = {};
    for (var i = 0; i < tags.length && hits.length < 400; i++) {
      var t = tags[i], l = t[1].toLowerCase();
      var rank = l === term ? 0 : l.indexOf(term) === 0 ? 1 : l.indexOf(term) > -1 ? 2 : -1;
      if (t[0].toLowerCase() === term) rank = 0;
      if (rank > -1 && !seen[t[0]]) { seen[t[0]] = 1; hits.push([rank, t, null]); }
    }
    if (syn) {
      for (var j = 0; j < syn.length && hits.length < 400; j++) {
        var s = syn[j];
        if (seen[s[0]]) continue;
        if (s[1].toLowerCase().indexOf(term) > -1) { seen[s[0]] = 1; hits.push([3, null, s]); }
      }
    }
    hits.sort(function (a, b) { return a[0] - b[0]; });

    var byId = {};
    for (var k = 0; k < tags.length; k++) byId[tags[k][0]] = tags[k];

    out.innerHTML = hits.slice(0, 100).map(function (h) {
      var t = h[1] || byId[h[2][0]];
      if (!t) return '';
      var via = h[2] ? '<span class="syn">matched synonym: ' + esc(h[2][1]) + '</span>' : '';
      return '<li><a href="/tag/' + encodeURIComponent(t[0]) + '/">' + esc(t[1]) + '</a>' +
             '<span class="b">' + esc(t[2]) + '</span>' + via + '</li>';
    }).join('');

    status.textContent = hits.length
      ? hits.length + (hits.length > 100 ? ' matches, showing the first 100' : ' matches')
        + (syn ? '' : ' — still loading synonyms')
      : 'No match for “' + q.value + '”.';
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var timer;
  q.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      run();
      var url = q.value ? '?q=' + encodeURIComponent(q.value) : location.pathname;
      history.replaceState(null, '', url);
    }, 120);
  });
})();
</script>
