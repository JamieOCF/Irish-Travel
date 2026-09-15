document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  var root = document.documentElement;

  function syncPressedState() {
    toggle.setAttribute('aria-pressed', String(root.getAttribute('data-theme') === 'dark'));
  }

  syncPressedState();

  toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    syncPressedState();
  });
});