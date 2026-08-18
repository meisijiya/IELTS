/* Read-tracker: marks writing <article> cards and speaking <a.topic-card> as read/unread.
 * Works on detail pages (single article) and list pages (many cards).
 * Keys: ielts-read:writing:<slug>, ielts-read:speaking:<slug>.
 */
(function () {
  'use strict';
  const hasDetail = !!document.querySelector('article[data-task], article[data-topic-id]');
  const hasList = !!document.querySelector('a.topic-card[href*="topics/"]');
  if (!hasDetail && !hasList) return;

  const P = 'ielts-read:';
  const get = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const del = (k) => { try { localStorage.removeItem(k); } catch (e) {} };
  const pageSlug = () => location.pathname.split('/').pop().replace(/\.html$/, '');

  // Resolve a card's slug. For <a.topic-card>, slug is the .html filename in href.
  // For <article>, slug is the h3 > a href, or the current page slug.
  const cardSlug = (el) => {
    if (el.tagName === 'A' && el.classList.contains('topic-card')) {
      return (el.getAttribute('href') || '').split('/').pop().replace(/\.html$/, '') || pageSlug();
    }
    const a = el.querySelector('h3 a');
    return a ? new URL(a.getAttribute('href'), location.href).pathname.split('/').pop().replace(/\.html$/, '') : pageSlug();
  };

  // module key for a card: writing or speaking
  const modOf = (el) => {
    if (el.tagName === 'A' && el.classList.contains('topic-card')) return 'speaking';
    if (el.hasAttribute('data-task')) return 'writing';
    if (el.hasAttribute('data-topic-id')) return 'speaking';
    return null;
  };

  const ensureDot = (el) => {
    let dot = el.querySelector(':scope > .dot');
    if (!dot) { dot = document.createElement('span'); dot.className = 'dot'; el.appendChild(dot); }
    return dot;
  };

  const paint = (el) => {
    const m = modOf(el); if (!m) return;
    const slug = cardSlug(el);
    const read = get(P + m + ':' + slug) === '1';
    const dot = ensureDot(el);
    dot.classList.toggle('dot-read', read);
    dot.classList.toggle('dot-unread', !read);
  };

  document.addEventListener('DOMContentLoaded', () => {
    // Detail page: mark this page as read
    const detail = document.querySelector('article[data-task], article[data-topic-id]');
    if (detail) { const m = modOf(detail); if (m) set(P + m + ':' + pageSlug(), '1'); }
    // List pages: paint all cards
    document.querySelectorAll('article, a.topic-card').forEach(paint);
  });

  document.addEventListener('click', (e) => {
    const el = e.target.closest('article, a.topic-card');
    if (!el) return;
    if (e.target.closest('button, a, input, textarea, select, details, summary, [data-no-toggle-read]')) return;
    const m = modOf(el); if (!m) return;
    const dot = el.querySelector(':scope > .dot'); if (!dot) return;
    const slug = cardSlug(el);
    if (dot.classList.contains('dot-read')) {
      dot.classList.remove('dot-read'); dot.classList.add('dot-unread'); del(P + m + ':' + slug);
    } else {
      dot.classList.remove('dot-unread'); dot.classList.add('dot-read'); set(P + m + ':' + slug, '1');
    }
  });
})();
