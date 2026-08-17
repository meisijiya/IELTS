---
id: T-004
goal: The Writing module index renders 题库 description + working difficulty/type filter + 5 essay placeholder cards.
files:
  - docs/writing/index.html
deps: [T-002]
ac:
  - REQ-essay-filter-scenario-single-chip-filter
  - REQ-essay-filter-scenario-combined-chip-filter
  - REQ-essay-filter-scenario-hash-restore-on-reload
evidence: curl + Playwright (T-015) verifies URL hash updates, display:none on non-matching cards, and reload restoration.
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

`docs/writing/index.html` is the Writing module landing page. Sections:

1. Header: explains the two 题库 sources.
2. Filter bar:
   - Difficulty chip row: `[All][data-value=all][aria-pressed=true]` (default), `[易][data-value=easy]`, `[中][data-value=medium]`, `[难][data-value=hard]`. Single-select.
   - Type chip row: one chip per supported type (`static-graph`, `dynamic-graph`, `mixed-graph`, `map`, `process`, `agree-disagree`, `discuss-both-views`, `positive-negative`, `opinion`, `two-questions`) plus `[All][data-value=all]`. Multi-select; hash value is comma-separated (`type=static-graph,mixed-graph`).
3. Essay list: 5 `<article>` cards, each `data-task="task1"|"task2"`, `data-difficulty="<v>"`, `data-type="<v>"`, linking to the essay page (real `href` once T-005..T-014 land; placeholder anchor otherwise).
4. Empty-state `<p class="empty" hidden>No matching essays</p>`.

Inline `<script>` (~50 lines) implementing:

- Click on a chip toggles `aria-pressed` and re-runs the filter.
- Filter sets `style.display = 'none'` on `<article>` cards whose `data-difficulty` does not match the active difficulty chip AND whose `data-type` is not in the active type set; matching cards get `style.display = ''`. When `[All]` is active for difficulty, every `data-difficulty` matches; same for type.
- Filter writes `#diff=<value>&type=<csv>` (or `#type=<csv>` / `#diff=<value>` alone when the other dimension is `[All]`).
- On `DOMContentLoaded`, parse `location.hash`, restore the active chip states and re-run the filter.

## Acceptance criteria

- [ ] `docs/writing/index.html` exists and links `../assets/css/style.css`.
- [ ] Contains the difficulty chip row (`[易]`, `[中]`, `[难]` plus `[All]`).
- [ ] Contains all 10 type chips with `data-value` attributes matching their slugs.
- [ ] Contains 5 `<article>` cards with `data-task`, `data-difficulty`, `data-type` set.
- [ ] Inline script (no external file) implements filter + hash sync + reload restore.
- [ ] Empty-state element exists with text `No matching essays` (hidden by default).
- [ ] When user clicks `[易]`, URL hash becomes `#diff=easy` and only `data-difficulty="easy"` cards are visible (the rest get `style.display:none`).

## Verification

- [ ] `grep -c 'data-value="easy"' docs/writing/index.html` returns `≥1`.
- [ ] `grep -c 'data-value="static-graph"' docs/writing/index.html` returns `≥1`.
- [ ] `grep -c '<article ' docs/writing/index.html` returns `5`.
- [ ] `grep -c "style.display" docs/writing/index.html` returns `≥1`.
- [ ] `grep -c 'location.hash' docs/writing/index.html` returns `≥1`.
- [ ] Playwright e2e (T-015) confirms all 3 filter scenarios.

## Files in scope

- `docs/writing/index.html` (create).

## Files out of scope

- The 5 essay HTML files (T-005..T-014).