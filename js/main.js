/* China Robotics Insider - minimal interactions */
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
  }

  // Current year in footer
  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();

  // Article like buttons (per-article localStorage counter)
  document.querySelectorAll('.like-btn').forEach(function (btn) {
    var slug = btn.getAttribute('data-slug') || 'article';
    var key = 'cri_like_' + slug;
    var n = parseInt(localStorage.getItem(key) || '0', 10);
    var badge = btn.querySelector('.like-count');
    if (badge) badge.textContent = n;
    if (n > 0) btn.classList.add('liked');
    btn.addEventListener('click', function () {
      var cur = parseInt(localStorage.getItem(key) || '0', 10);
      var next = cur > 0 ? 0 : 1; // toggle
      localStorage.setItem(key, String(next));
      if (badge) badge.textContent = next;
      btn.classList.toggle('liked', next === 1);
    });
  });

  // Copy link buttons
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-url') || location.href;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = 'Copied \u2713';
        setTimeout(function () { btn.textContent = old; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done)['catch'](done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });
})();
