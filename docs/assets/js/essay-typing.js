/* Writing essay detail — typing rows + sticky prompt + essay-body isolation.
 * Only runs on <article data-task> pages (writing only). localStorage guarded.
 * Keys: ielts-writing:open:<slug>:<i>, ielts-writing:draft:<slug>:<i>
 * Row layout: button → status → textarea (toggle reads nextElementSibling.nextElementSibling).
 */
(function () {
  'use strict';

  const article = document.querySelector('article[data-task]');
  if (!article) return;

  const slug = location.pathname.split('/').pop().replace(/\.html$/, '') || 'default';
  const safeGet = (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const safeSet = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const draftKey = (i) => `ielts-writing:draft:${slug}:${i}`;
  const openKey  = (i) => `ielts-writing:open:${slug}:${i}`;

  // --- Sticky prompt: add class, inject title bar, wrap inner content ---
  const prompt = article.querySelector('section.prompt');
  if (prompt && !prompt.classList.contains('prompt-sticky')) {
    prompt.classList.add('prompt-sticky');
    const title = document.createElement('div');
    title.className = 'prompt-title';
    const label = document.createElement('span');
    label.textContent = '题目';
    const btn = document.createElement('button');
    btn.className = 'prompt-toggle';
    btn.type = 'button';
    btn.textContent = '▾';
    title.append(label, btn);
    const body = document.createElement('div');
    body.className = 'prompt-body';
    while (prompt.firstChild) body.appendChild(prompt.firstChild);
    prompt.append(title, body);
    btn.addEventListener('click', () => {
      const c = prompt.classList.toggle('collapsed');
      btn.textContent = c ? '▴' : '▾';
    });
  }

  // --- Essay body isolation wrapper (creates stacking context for sticky) ---
  const essay = article.querySelector('section.essay');
  if (essay && !essay.querySelector(':scope > .essay-body')) {
    const wrap = document.createElement('div');
    wrap.className = 'essay-body';
    while (essay.firstChild) wrap.appendChild(essay.firstChild);
    essay.appendChild(wrap);
  }
  if (!essay) return;

  // --- Inject typing rows after each <p> (idempotent) ---
  essay.querySelectorAll('.essay-body > p').forEach((p, i) => {
    if (p.nextElementSibling && p.nextElementSibling.classList.contains('typing-row')) return;
    const row = document.createElement('div');
    row.className = 'typing-row';
    const b = document.createElement('button');
    b.className = 'typing-toggle';
    b.type = 'button';
    b.dataset.para = String(i);
    b.textContent = '▸ 练习';
    const st = document.createElement('span');
    st.className = 'draft-status';
    const ta = document.createElement('textarea');
    ta.className = 'typing-input';
    ta.rows = 3;
    ta.placeholder = `在这里写你的第 ${i + 1} 段…`;
    row.append(b, st, ta);
    p.after(row);

    const saved = safeGet(draftKey(i));
    if (saved) { ta.value = saved; st.textContent = '已恢复 ✓'; st.classList.add('saved'); }
    if (safeGet(openKey(i)) === '1') { ta.classList.add('visible'); b.textContent = '▾ 收起'; }
  });

  // --- Toggle open/close + persist ---
  essay.querySelectorAll('.typing-toggle').forEach((b) => {
    b.addEventListener('click', () => {
      const ta = b.nextElementSibling.nextElementSibling;
      const open = ta.classList.toggle('visible');
      b.textContent = open ? '▾ 收起' : '▸ 练习';
      safeSet(openKey(b.dataset.para), open ? '1' : '0');
    });
  });

  // --- Debounced draft save (500ms per index) ---
  const timers = {};
  essay.querySelectorAll('.typing-input').forEach((ta, i) => {
    ta.addEventListener('input', () => {
      const st = ta.previousElementSibling;
      st.textContent = '保存中…';
      st.classList.remove('saved');
      clearTimeout(timers[i]);
      timers[i] = setTimeout(() => {
        safeSet(draftKey(i), ta.value);
        st.textContent = '已保存 ✓';
        st.classList.add('saved');
      }, 500);
    });
  });
})();
