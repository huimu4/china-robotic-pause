/* China Robotics Insider - site search */
(function () {
  'use strict';
  var box = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var countEl = document.getElementById('search-count');
  if (!box || !results) return;

  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function render() {
    var q = (box.value || '').trim().toLowerCase();
    if (!q) {
      countEl.textContent = '';
      results.innerHTML = '<p class="search-empty">Type a keyword \u2014 a company, a founder, a product \u2014 to search the site.</p>';
      return;
    }
    var index = window.SEARCH_INDEX || [];
    var hits = index.filter(function (p) {
      return (p.t + ' ' + p.k + ' ' + p.d + ' ' + p.cat).toLowerCase().indexOf(q) !== -1;
    });
    if (!hits.length) {
      countEl.textContent = '0 results';
      results.innerHTML = '<p class="search-empty">No results for \u201c' + esc(box.value.trim()) + '\u201d. Try \u201cUnitree\u201d, \u201chumanoid\u201d or \u201cDJI\u201d.</p>';
      return;
    }
    countEl.textContent = hits.length + (hits.length > 1 ? ' results' : ' result');
    results.innerHTML = hits.map(function (p) {
      return '<article class="card search-hit">' +
        '<h3><a href="' + esc(p.u) + '">' + esc(p.t) + '</a></h3>' +
        '<p>' + esc(p.d) + '</p>' +
        '<div class="tag-row"><span class="tag teal">' + esc(p.cat) + '</span></div>' +
        '</article>';
    }).join('');
  }

  var params = new URLSearchParams(window.location.search);
  var q0 = params.get('q');
  if (q0) {
    box.value = q0;
    render();
  }

  box.addEventListener('input', render);
  box.addEventListener('search', render);
})();
