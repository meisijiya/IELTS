/* Vocab — browse-only. Loads 5 JSON files; renders doc/category chips and a
 * browse grid with debounced text search. No spell / unmastered / progress.
 * Pure vanilla, no deps.
 */
(function () {
  'use strict';

  const SOURCE_IDS = ['speaking-p1', 'listening', 'cambridge', 'kaodian538', 'writing'];
  const DEBOUNCE_SEARCH_MS = 150;

  const VocabApp = {
    STATE: {
      activeDoc: null,
      activeCategory: null,
      searchQuery: '',
      vocabData: {},
    },

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
      this.wireEvents();
      this.renderDocChips();
      this.renderCategoryChips();
      this.applyFilter();
    },

    cacheEls() {
      const id = (s) => document.getElementById(s);
      this.$ = {
        error:    id('vocab-error'),
        docChips: id('doc-chips'),
        catChips: id('category-chips'),
        search:   id('vocab-search'),
        cardGrid: id('vocab-card-grid'),
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

    setDoc(docId) {
      if (this.STATE.activeDoc === docId) return;
      this.STATE.activeDoc = docId;
      this.STATE.activeCategory = null;
      this.renderDocChips();
      this.renderCategoryChips();
      this.applyFilter();
    },

    setCategory(catId) {
      this.STATE.activeCategory = catId || null;
      this.renderCategoryChips();
      this.applyFilter();
    },

    setSearch(q) {
      this.STATE.searchQuery = (q || '').trim().toLowerCase();
      this.applyFilter();
    },

    applyFilter() {
      const { activeDoc, activeCategory, searchQuery } = this.STATE;
      let items;

      if (activeDoc === 'all') {
        items = [];
        for (const id of SOURCE_IDS) {
          const doc = this.STATE.vocabData[id];
          if (!doc) continue;
          for (const it of doc.items) items.push(Object.assign({}, it, { sourceDoc: id }));
        }
        if (searchQuery) {
          items = items.filter((it) => {
            const en = (it.english || '').toLowerCase();
            const zh = (it.chinese || '').toLowerCase();
            return en.includes(searchQuery) || zh.includes(searchQuery);
          });
        }
      } else {
        const doc = this.STATE.vocabData[activeDoc];
        items = doc ? doc.items.filter((it) => {
          if (activeCategory && it.category_id !== activeCategory) return false;
          if (searchQuery) {
            const en = (it.english || '').toLowerCase();
            const zh = (it.chinese || '').toLowerCase();
            if (!en.includes(searchQuery) && !zh.includes(searchQuery)) return false;
          }
          return true;
        }) : [];
      }

      this.renderBrowse(items);
    },

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

    renderBrowse(items) {
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

    showError(msg) {
      if (!this.$.error) {
        console.error('[VocabApp]', msg);
        return;
      }
      this.$.error.hidden = false;
      this.$.error.textContent = msg;
    },

    esc(s) {
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    },

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

      let searchTimer = null;
      this.$.search.addEventListener('input', (e) => {
        if (searchTimer) clearTimeout(searchTimer);
        const v = e.target.value;
        searchTimer = setTimeout(() => this.setSearch(v), DEBOUNCE_SEARCH_MS);
      });
    },
  };

  document.addEventListener('DOMContentLoaded', () => VocabApp.init());
  window.VocabApp = VocabApp;
})();