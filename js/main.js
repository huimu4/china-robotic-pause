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
})();
