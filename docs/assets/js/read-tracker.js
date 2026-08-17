/* Read-tracker: marks <article> cards as read/unread via localStorage.
 * Works on detail pages (single article with data-task / data-topic-id)
 * and list pages (many article cards with h3 > a).
 * Keys: ielts-read:writing:<slug>, ielts-read:speaking:<slug>.
 */
(function () {
  'use strict';
  if (!document.querySelector('article[data-task], article[data-topic-id]')) return;
  const P = 'ielts-read:';
  const get = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const del = (k) => { try { localStorage.removeItem(k); } catch (e) {} };
  const pageSlug = () => location.pathname.split('/').pop().replace(/\.html$/, '');
  const cardSlug = (art) => {
    const a = art.querySelector('h3 a');
    return a ? new URL(a.getAttribute('href'), location.href).pathname.split('/').pop().replace(/\.html$/, '') : pageSlug();
  };
  const modOf = (art) => art.hasAttribute('data-task') ? 'writing' : art.hasAttribute('data-topic-id') ? 'speaking' : null;

  document.addEventListener('DOMContentLoaded', () => {
    const detail = document.querySelector('article[data-task], article[data-topic-id]');
    if (detail) { const m = modOf(detail); if (m) set(P + m + ':' + pageSlug(), '1'); }
    document.querySelectorAll('article').forEach((art) => {
      const m = modOf(art); if (!m) return;
      let dot = art.querySelector('.dot');
      if (!dot) { dot = document.createElement('span'); dot.className = 'dot'; art.insertBefore(dot, art.firstChild); }
      const read = get(P + m + ':' + cardSlug(art)) === '1';
      dot.classList.toggle('dot-read', read);
      dot.classList.toggle('dot-unread', !read);
    });
  });

  document.addEventListener('click', (e) => {
    const art = e.target.closest('article'); if (!art) return;
    if (e.target.closest('button, a, input, textarea, select, details, summary, [data-no-toggle-read]')) return;
    const m = modOf(art); if (!m) return;
    const dot = art.querySelector('.dot'); if (!dot) return;
    const slug = cardSlug(art);
    if (dot.classList.contains('dot-read')) {
      dot.classList.remove('dot-read'); dot.classList.add('dot-unread'); del(P + m + ':' + slug);
    } else {
      dot.classList.remove('dot-unread'); dot.classList.add('dot-read'); set(P + m + ':' + slug, '1');
    }
  });
})();
