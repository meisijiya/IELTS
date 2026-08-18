/* Vocab — BASIC mode (T-12). T-13 extends with localStorage + stats + 未掌握.
 * IIFE wraps a single VocabApp; window.VocabApp is exposed so T-13 can patch.
 * Pure vanilla, no deps. Loads 5 JSON files; renders doc/category chips, browse
 * grid, and one-at-a-time spell view with debounced char-level diff feedback.
 */
(function () {
  'use strict';

  const SOURCE_IDS = ['speaking-p1', 'listening', 'cambridge', 'kaodian538', 'writing'];
  const PUNCT_RE = /^[.,;:!?]+|[.,;:!?]+$/g;
  const DEBOUNCE_SEARCH_MS = 150;
  const DEBOUNCE_SPELL_MS = 100;

  // ---- VocabApp ----
  const VocabApp = {
    STATE: {
      activeDoc: null,
      activeCategory: null,
      searchQuery: '',
      mode: 'browse',
      items: [],        // filtered pool — shared by browse & spell
      currentIndex: 0,
      correctCount: 0,
      vocabData: {},    // { [docId]: { source_doc, source_label, categories, items } }
    },

    // ============== init ==============
    async init() {
      this.cacheEls();
      try {
        await this.loadAllData();
      } catch (err) {
        this.showError('词表加载失败: ' + (err && err.message ? err.message : err));
        return;
      }
      this.STATE.activeDoc = SOURCE_IDS[0];
      this.STATE.activeCategory = null;
      this._initSpellHistory();
      this.ProgressStore.load();
      this.wireEvents();
      this.renderDocChips();
      this.renderCategoryChips();
      this.setMode('browse');
      this.applyFilter();
      this.renderStats();
    },

    _initSpellHistory() {
      const el = document.createElement('p');
      el.id = 'spell-history';
      el.className = 'vocab-history';
      el.hidden = true;
      // ponytail: CSS lacks .vocab-history; inline minimum until stylesheet ships.
      el.style.cssText = 'font-size:0.85em;color:#666;margin:0.25em 0;';
      this.$.spellNav.parentNode.insertBefore(el, this.$.spellNav);
      this._spellHistoryEl = el;
    },

    _renderSpellHistory(item) {
      const el = this._spellHistoryEl;
      if (!el) return;
      const wid = this.wordId(item);
      const h = this.ProgressStore.get(wid);
      if (!h || ((h.correct || 0) + (h.wrong || 0)) === 0) {
        el.hidden = true;
        el.textContent = '';
        return;
      }
      const last = (h.lastSeen || '').slice(0, 10);
      el.hidden = false;
      el.textContent = '历史: 拼对 ' + (h.correct || 0)
        + ' 次 · 拼错 ' + (h.wrong || 0)
        + ' 次 · 上次 ' + last;
    },

    wordId(item) {
      const docId = this.STATE.activeDoc === 'all'
        ? (item.sourceDoc || this.STATE.activeDoc)
        : this.STATE.activeDoc;
      return docId + '::' + item.category_id + '::' + item.id;
    },

    renderStats() {
      const sum = this.ProgressStore.summary();
      if (this.$.statsTotal)   this.$.statsTotal.textContent = sum.totalText;
      if (this.$.statsCorrect) this.$.statsCorrect.textContent = sum.accuracyText;
    },

    _showResetConfirm() {
      const existing = this._resetModal;
      if (existing) {
        existing.setAttribute('data-show', 'true');
        return;
      }
      const modal = document.createElement('div');
      modal.className = 'vocab-reset-confirm';
      modal.setAttribute('data-show', 'true');
      modal.innerHTML = '<div class="vocab-reset-card" style="background:#fff;padding:1.25em 1.5em;border-radius:6px;min-width:240px;text-align:center;">'
        + '<p style="margin:0 0 1em;">确定重置所有学习数据？</p>'
        + '<div class="vocab-reset-actions" style="display:flex;gap:0.5em;justify-content:center;">'
        +   '<button type="button" class="chip" data-reset="cancel">取消</button>'
        +   '<button type="button" class="chip" data-reset="ok">确认</button>'
        + '</div>'
        + '</div>';
      modal.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-reset]');
        if (btn) {
          if (btn.dataset.reset === 'ok') {
            this.ProgressStore.reset();
            this.renderStats();
            const m = this.STATE.mode;
            this.setMode(m === 'unmastered' ? 'browse' : m);
          }
          modal.setAttribute('data-show', 'false');
          return;
        }
        if (e.target === modal) modal.setAttribute('data-show', 'false');
      });
      document.body.appendChild(modal);
      this._resetModal = modal;
    },

    ProgressStore: {
      _key: 'ielts-vocab:progress',
      _legacyKey: 'vocab-progress',
      _cache: null,
      _saveTimer: null,
      _WARN_BYTES: 500000,

      load() {
        this._cache = {};
        try {
          let raw = localStorage.getItem(this._key);
          if (!raw) {
            raw = localStorage.getItem(this._legacyKey);
            if (raw) {
              try { localStorage.setItem(this._key, raw); } catch (e) {}
              try { localStorage.removeItem(this._legacyKey); } catch (e) {}
            }
          }
          if (!raw) return;
          if (raw.length > this._WARN_BYTES) {
            console.warn('[VocabApp] localStorage "' + this._key
              + '" exceeds 500KB (' + raw.length + ' bytes).');
          }
          const parsed = JSON.parse(raw);
          this._cache = (parsed && typeof parsed === 'object') ? parsed : {};
        } catch (e) {
          console.warn('[VocabApp] failed to parse localStorage', e);
          this._cache = {};
        }
      },

      save() {
        if (this._saveTimer) clearTimeout(this._saveTimer);
        this._saveTimer = setTimeout(() => {
          try {
            const json = JSON.stringify(this._cache);
            if (json.length > this._WARN_BYTES) {
              console.warn('[VocabApp] ProgressStore JSON exceeds 500KB ('
                + json.length + ' bytes).');
            }
            localStorage.setItem(this._key, json);
          } catch (e) {
            console.warn('[VocabApp] failed to save localStorage', e);
          }
        }, 500);
      },

      get(wordId) {
        return this._cache[wordId] || null;
      },

      record(wordId, correct) {
        const now = new Date().toISOString();
        const cur = this._cache[wordId];
        if (cur) {
          cur.correct = (cur.correct || 0) + (correct ? 1 : 0);
          cur.wrong = (cur.wrong || 0) + (correct ? 0 : 1);
          cur.lastSeen = now;
        } else {
          this._cache[wordId] = { correct: correct ? 1 : 0, wrong: correct ? 0 : 1, firstSeen: now, lastSeen: now };
        }
        this.save();
      },

      reset() {
        this._cache = {};
        this.save();
      },

      summary() {
        const entries = Object.values(this._cache);
        const total = entries.length;
        if (total === 0) {
          return { totalText: '尚未开始', accuracyText: '—', total: 0, attempts: 0, correct: 0 };
        }
        let attempts = 0, correct = 0;
        for (const e of entries) {
          attempts += (e.correct || 0) + (e.wrong || 0);
          correct += (e.correct || 0);
        }
        const accuracy = attempts > 0 ? Math.round((correct / attempts) * 100) + '%' : '—';
        return { totalText: String(total), accuracyText: accuracy, total: total, attempts: attempts, correct: correct };
      },

      wrongItems() {
        const out = [];
        for (const wordId in this._cache) {
          const e = this._cache[wordId];
          const wrong = e.wrong || 0;
          if (wrong <= 0) continue;
          const parts = wordId.split('::');
          out.push({
            wordId: wordId,
            item: parts[2] || '',
            sourceDoc: parts[0] || '',
            wrong: wrong,
            lastSeen: e.lastSeen || '',
          });
        }
        out.sort((a, b) => {
          if (b.wrong !== a.wrong) return b.wrong - a.wrong;
          return (b.lastSeen || '').localeCompare(a.lastSeen || '');
        });
        return out;
      },
    },

    cacheEls() {
      const id = (s) => document.getElementById(s);
      this.$ = {
        error:          id('vocab-error'),
        docChips:       id('doc-chips'),
        catChips:       id('category-chips'),
        search:         id('vocab-search'),
        modeTabs:       id('mode-tabs'),
        viewBrowse:     id('view-browse'),
        viewSpell:      id('view-spell'),
        viewUnmastered: id('view-unmastered'),
        cardGrid:       id('vocab-card-grid'),
        spellPrompt:    id('spell-prompt'),
        spellInput:     id('spell-input'),
        spellFeedback:  id('spell-feedback'),
        spellProgress:  id('spell-progress'),
        spellNav:       id('spell-nav'),
        unmasteredList: id('unmastered-list'),
        statsTotal:     id('stats-total'),
        statsCorrect:   id('stats-correct'),
        statsReset:     id('stats-reset'),
      };
    },

    async loadAllData() {
      const results = await Promise.all(
        SOURCE_IDS.map((id) =>
          fetch('./data/' + id + '.json')
            .then((r) => {
              if (!r.ok) throw new Error(id + '.json HTTP ' + r.status);
              return r.json();
            })
            .then((json) => [id, json])
        )
      );
      const data = {};
      for (const [docId, json] of results) data[docId] = json;
      this.STATE.vocabData = data;
    },

    // ============== spell helpers (public for T-13/tests) ==============
    norm(s) {
      if (s == null) return '';
      return String(s).trim().toLowerCase().replace(PUNCT_RE, '');
    },

    checkSpelling(value, target) {
      const nv = this.norm(value);
      const nt = this.norm(target);
      if (nv.length === 0) {
        return { status: 'empty', target, value, diff: '' };
      }
      if (nv === nt) {
        return { status: 'correct', target, value, diff: this.spanAll(nv, 'char-right') };
      }
      return { status: 'wrong', target, value, diff: this.diffChars(nv, nt) };
    },

    spanAll(s, cls) {
      let out = '';
      for (const ch of s) out += '<span class="' + cls + '">' + this.esc(ch) + '</span>';
      return out;
    },

    diffChars(value, target) {
      const n = Math.max(value.length, target.length);
      let out = '';
      for (let i = 0; i < n; i++) {
        const v = value[i];
        const t = target[i];
        if (i < value.length && i < target.length && v === t) {
          out += '<span class="char-right">' + this.esc(v) + '</span>';
        } else if (i < value.length) {
          out += '<span class="char-wrong">' + this.esc(v) + '</span>';
        } else {
          // missing — show the target's char as hint
          out += '<span class="char-wrong">' + this.esc(t) + '</span>';
        }
      }
      return out;
    },

    esc(s) {
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    },

    // ============== state setters ==============
    setDoc(docId) {
      if (this.STATE.activeDoc === docId) return;
      this.STATE.activeDoc = docId;
      this.STATE.activeCategory = null;
      this.STATE.currentIndex = 0;
      this.renderDocChips();
      this.renderCategoryChips();
      this.applyFilter();
    },

    setCategory(catId) {
      // null/undefined/''  → all categories
      this.STATE.activeCategory = catId || null;
      this.STATE.currentIndex = 0;
      this.renderCategoryChips();
      this.applyFilter();
    },

    setMode(mode) {
      this.STATE.mode = mode;
      const map = {
        browse:     this.$.viewBrowse,
        spell:      this.$.viewSpell,
        unmastered: this.$.viewUnmastered,
      };
      for (const k in map) if (map[k]) map[k].hidden = (k !== mode);

      if (this.$.modeTabs) {
        this.$.modeTabs.querySelectorAll('[data-mode]').forEach((el) => {
          if (el.dataset.mode === mode) el.setAttribute('aria-pressed', 'true');
          else el.removeAttribute('aria-pressed');
        });
      }

      if (mode === 'browse')      this.renderBrowse();
      else if (mode === 'spell')  this.renderSpell();
      else if (mode === 'unmastered') this.renderUnmastered();
    },

    setSearch(q) {
      this.STATE.searchQuery = (q || '').trim().toLowerCase();
      this.applyFilter();
    },

    // ============== filter pipeline ==============
    applyFilter() {
      const { activeDoc, activeCategory, searchQuery } = this.STATE;

      if (activeDoc === 'all') {
        let all = [];
        for (const id of SOURCE_IDS) {
          const doc = this.STATE.vocabData[id];
          if (!doc) continue;
          for (const it of doc.items) all.push(Object.assign({}, it, { sourceDoc: id }));
        }
        if (searchQuery) {
          all = all.filter((it) => {
            const en = (it.english || '').toLowerCase();
            const zh = (it.chinese || '').toLowerCase();
            return en.includes(searchQuery) || zh.includes(searchQuery);
          });
        }
        this.STATE.items = all;
      } else {
        const doc = this.STATE.vocabData[activeDoc];
        if (!doc) {
          this.STATE.items = [];
        } else {
          this.STATE.items = doc.items.filter((it) => {
            if (activeCategory && it.category_id !== activeCategory) return false;
            if (searchQuery) {
              const en = (it.english || '').toLowerCase();
              const zh = (it.chinese || '').toLowerCase();
              if (!en.includes(searchQuery) && !zh.includes(searchQuery)) return false;
            }
            return true;
          });
        }
      }

      if (this.STATE.mode === 'browse') {
        this.renderBrowse();
      } else if (this.STATE.mode === 'spell') {
        if (this.STATE.currentIndex >= this.STATE.items.length) {
          this.STATE.currentIndex = 0;
        }
        this.renderSpell();
      } else if (this.STATE.mode === 'unmastered') {
        this.renderUnmastered();
      }
    },

    // ============== render: doc chips ==============
    renderDocChips() {
      const data = this.STATE.vocabData;
      const isAll = this.STATE.activeDoc === 'all';
      const allChip = '<button type="button" class="chip vocab-tab doc-chip" data-doc="all"'
        + (isAll ? ' aria-pressed="true"' : '')
        + '>全部</button>';
      const rest = SOURCE_IDS.map((id) => {
        const doc = data[id];
        const label = doc ? doc.source_label : id;
        const active = id === this.STATE.activeDoc;
        return '<button type="button" class="chip vocab-tab doc-chip" data-doc="' + this.esc(id) + '"'
          + (active ? ' aria-pressed="true"' : '')
          + '>' + this.esc(label) + '</button>';
      }).join('');
      this.$.docChips.innerHTML = allChip + rest;
    },

    // ============== render: category chips ==============
    renderCategoryChips() {
      if (this.STATE.activeDoc === 'all') {
        this.$.catChips.innerHTML =
          '<button type="button" class="chip vocab-tab cat-chip" data-cat="" aria-pressed="true">全部</button>';
        return;
      }
      const doc = this.STATE.vocabData[this.STATE.activeDoc];
      const cats = doc ? doc.categories : [];
      const parts = [
        '<button type="button" class="chip vocab-tab cat-chip" data-cat=""'
          + (this.STATE.activeCategory == null ? ' aria-pressed="true"' : '')
          + '>全部</button>',
      ];
      for (const c of cats) {
        parts.push(
          '<button type="button" class="chip vocab-tab cat-chip" data-cat="' + this.esc(c.id) + '"'
            + (this.STATE.activeCategory === c.id ? ' aria-pressed="true"' : '')
            + '>' + this.esc(c.label) + '</button>'
        );
      }
      this.$.catChips.innerHTML = parts.join('');
    },

    // ============== render: browse ==============
    renderBrowse() {
      const items = this.STATE.items;
      if (items.length === 0) {
        this.$.cardGrid.innerHTML = '<div class="vocab-empty">当前条件下没有词条。</div>';
        return;
      }
      this.$.cardGrid.innerHTML = items.map((it) => this.cardHTML(it)).join('');
    },

    cardHTML(it) {
      const docId = it.sourceDoc || this.STATE.activeDoc;
      const sourceLabel = this._sourceLabel(docId);
      const ipa = it.ipa
        ? '<span class="card-ipa">[' + this.esc(it.ipa) + ']</span>'
        : '';
      const example = it.example_en
        ? '<p class="card-example">' + this.esc(it.example_en) + '</p>'
        : '';
      return '<article class="vocab-card" data-id="' + this.esc(it.id) + '">'
        + '<header class="card-head">'
        +   '<span class="vocab-source-chip" data-source="' + this.esc(docId) + '">'
        +     this.esc(sourceLabel)
        +   '</span>'
        + '</header>'
        + '<h3 class="card-en">' + this.esc(it.english) + ' ' + ipa + '</h3>'
        + '<p class="card-zh">' + this.esc(it.chinese || '') + '</p>'
        + example
        + '</article>';
    },

    _sourceLabel(docId) {
      const d = this.STATE.vocabData[docId];
      return d ? d.source_label : docId;
    },

    // ============== render: spell ==============
    renderSpell() {
      const items = this.STATE.items;
      this.$.spellInput.classList.remove('correct', 'wrong');
      this._spellDebounce = null;

      if (items.length === 0) {
        this.$.spellPrompt.innerHTML = '';
        this.$.spellFeedback.innerHTML = '<div class="vocab-empty">当前条件下没有可拼写的词条。</div>';
        this.$.spellInput.value = '';
        this.$.spellInput.disabled = true;
        this._setProgress(0, 0);
        if (this._spellHistoryEl) { this._spellHistoryEl.hidden = true; this._spellHistoryEl.textContent = ''; }
        return;
      }
      this.$.spellInput.disabled = false;
      const item = items[this.STATE.currentIndex];
      this.$.spellPrompt.innerHTML = '<div class="spell-zh">' + this.esc(item.chinese || '(no translation)') + '</div>';
      this.$.spellInput.value = '';
      this.$.spellFeedback.innerHTML = '';
      this._setProgress(this.STATE.currentIndex + 1, items.length);
      this._renderSpellHistory(item);
    },

    _setProgress(value, max) {
      if (!this.$.spellProgress) return;
      if (this.$.spellProgress.tagName === 'PROGRESS') {
        this.$.spellProgress.value = value;
        this.$.spellProgress.max = max;
      } else {
        this.$.spellProgress.textContent = value + ' / ' + max;
      }
    },

    _spellDebounce: null,

    onSpellInput(raw) {
      if (this._spellDebounce) clearTimeout(this._spellDebounce);
      this._spellDebounce = setTimeout(() => this.renderSpellFeedback(raw), DEBOUNCE_SPELL_MS);
    },

    renderSpellFeedback(raw) {
      const items = this.STATE.items;
      if (items.length === 0) return;
      const item = items[this.STATE.currentIndex];
      const r = this.checkSpelling(raw, item.english);

      this.$.spellInput.classList.remove('correct', 'wrong');
      if (r.status === 'empty') {
        this.$.spellFeedback.innerHTML = '';
        return;
      }
      if (r.status === 'correct') {
        this.$.spellInput.classList.add('correct');
        this.$.spellFeedback.innerHTML = '<span class="spell-ok">拼写正确 ✓</span>';
        this.ProgressStore.record(this.wordId(item), true);
        this.renderStats();
      } else {
        this.$.spellInput.classList.add('wrong');
        this.$.spellFeedback.innerHTML =
          '<div class="vocab-diff">' + r.diff + '</div>'
          + '<div class="spell-hint">正确答案: <code>' + this.esc(r.target) + '</code></div>';
        this.ProgressStore.record(this.wordId(item), false);
        this.renderStats();
      }
    },

    // ============== nav: next / prev / skip ==============
    nextItem() {
      if (this.STATE.items.length === 0) return;
      this.STATE.currentIndex = (this.STATE.currentIndex + 1) % this.STATE.items.length;
      this.renderSpell();
    },
    prevItem() {
      if (this.STATE.items.length === 0) return;
      const n = this.STATE.items.length;
      this.STATE.currentIndex = (this.STATE.currentIndex - 1 + n) % n;
      this.renderSpell();
    },
    skipItem() {
      // BASIC mode: skip == move on. T-13 will mark "未掌握" without progressing stats.
      this.nextItem();
    },

    // ============== render: unmastered ==============
    renderUnmastered() {
      let wrong = this.ProgressStore.wrongItems();
      if (this.STATE.activeDoc !== 'all') {
        wrong = wrong.filter((w) => w.sourceDoc === this.STATE.activeDoc);
      }
      if (!wrong || wrong.length === 0) {
        this.$.unmasteredList.innerHTML =
          '<div class="vocab-empty">暂无未掌握词 ✓</div>';
        return;
      }
      const html = wrong.map((w) => {
        const doc = this.STATE.vocabData[w.sourceDoc];
        if (!doc) return '';
        const item = doc.items.find((i) => i.id === w.item);
        if (!item) return '';
        return this.cardHTML(Object.assign({}, item, { sourceDoc: w.sourceDoc }));
      }).join('');
      this.$.unmasteredList.innerHTML = html || '<div class="vocab-empty">暂无未掌握词 ✓</div>';
    },

    // ============== error display ==============
    showError(msg) {
      if (!this.$.error) {
        console.error('[VocabApp]', msg);
        return;
      }
      this.$.error.hidden = false;
      this.$.error.textContent = msg;
    },

    // ============== events ==============
    wireEvents() {
      this.$.docChips.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-doc]');
        if (btn) this.setDoc(btn.dataset.doc);
      });

      this.$.catChips.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-cat]');
        if (!btn) return;
        this.setCategory(btn.dataset.cat || null);
      });

      this.$.modeTabs.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-mode]');
        if (btn) this.setMode(btn.dataset.mode);
      });

      // search — debounced 150ms
      let searchTimer = null;
      this.$.search.addEventListener('input', (e) => {
        if (searchTimer) clearTimeout(searchTimer);
        const v = e.target.value;
        searchTimer = setTimeout(() => this.setSearch(v), DEBOUNCE_SEARCH_MS);
      });

      // spell input — debounced 100ms (inside onSpellInput)
      this.$.spellInput.addEventListener('input', (e) => this.onSpellInput(e.target.value));

      this.$.spellNav.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-nav]');
        if (!btn) return;
        const a = btn.dataset.nav;
        if (a === 'next')      this.nextItem();
        else if (a === 'prev') this.prevItem();
        else if (a === 'skip') this.skipItem();
      });

      if (this.$.statsReset) {
        this.$.statsReset.addEventListener('click', () => this._showResetConfirm());
      }
    },
  };

  document.addEventListener('DOMContentLoaded', () => VocabApp.init());
  window.VocabApp = VocabApp;
})();