/* Speaking topic — learning mode toggle.
 * Buttons: [data-action="hide-all"], [data-action="show-all"] close/open all <details class="qa-item">.
 * Keyboard: 'h' hides all, 's' shows all (ignored inside form fields).
 * Per-topic localStorage key derived from <article data-topic-id>.
 */
(function () {
  'use strict';

  var article = document.querySelector('article[data-topic-id]');
  var items = document.querySelectorAll('details.qa-item');
  var hideBtn = document.querySelector('[data-action="hide-all"]');
  var showBtn = document.querySelector('[data-action="show-all"]');
  if (!items.length) return;

  var topicId = article ? article.getAttribute('data-topic-id') : 'default';
  var storageKey = 'ielts-speaking:learning-mode:' + topicId;

  function setAll(open) {
    items.forEach(function (item) {
      item.open = open;
    });
    try {
      localStorage.setItem(storageKey, open ? 'shown' : 'hidden');
    } catch (e) {
      // ponytail: localStorage may be disabled (private mode, quota) — ignore silently.
    }
  }

  function restore() {
    var saved;
    try {
      saved = localStorage.getItem(storageKey);
    } catch (e) { return; }
    if (saved !== 'shown' && saved !== 'hidden') return;
    var open = saved === 'shown';
    items.forEach(function (item) { item.open = open; });
  }

  if (hideBtn) hideBtn.addEventListener('click', function () { setAll(false); });
  if (showBtn) showBtn.addEventListener('click', function () { setAll(true); });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (e.key === 'h' || e.key === 'H') { setAll(false); }
    else if (e.key === 's' || e.key === 'S') { setAll(true); }
  });

  restore();
})();