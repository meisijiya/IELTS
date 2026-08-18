# Task 2 — essay-typing.js

## File
`docs/assets/js/essay-typing.js`

## Line count
100 (acceptance: ≤ 100) — `wc -l docs/assets/js/essay-typing.js` → `100`

## Acceptance grep counts
| pattern | count | required |
|---|---|---|
| `ielts-writing:draft:` | 2 | ≥ 1 ✓ |
| `ielts-writing:open:` | 2 | ≥ 1 ✓ |
| `prompt-sticky` | 2 | ≥ 1 ✓ |
| `data-task` | 2 | ≥ 1 ✓ |

## Behavior summary
- IIFE + `'use strict'`, early return if `!article[data-task]` (skips reading/listening/speaking pages even with `.prompt`).
- `slug` = `location.pathname.split('/').pop().replace(/\.html$/, '')` → e.g. `01-table-universities-ranked`.
- All `localStorage` access funneled through `safeGet` / `safeSet` helpers wrapping `try/catch`.
- **Sticky prompt**: add `prompt-sticky` class; prepend `<div class="prompt-title"><span>题目</span><button class="prompt-toggle">▾</button></div>`; move all existing children into `<div class="prompt-body">` (text content untouched). Toggle click flips `.collapsed` on the prompt and swaps button to `▴`.
- **Essay-body wrapper**: if `<section class="essay">` has no direct `.essay-body` child, move all children into a new `<div class="essay-body">`. Establishes the isolated stacking context the CSS relies on.
- **Typing rows**: for each `.essay-body > p`, append (zero-indexed) `<div class="typing-row">` containing `<button>▸ 练习</button> <span class="draft-status"></span> <textarea rows=3>` immediately after `p`. Idempotent: skips if the next sibling is already `.typing-row`.
  - toggle click → flips `.visible` on textarea, updates button text, persists `ielts-writing:open:<slug>:<i>` = `'1'` / `'0'`.
  - input → 500ms debounce (per-index `timers` map), writes to `ielts-writing:draft:<slug>:<i>`, status `保存中…` → `已保存 ✓` + `.saved` class.
  - load → restores draft value + `已恢复 ✓` if non-empty, restores open state + `▾ 收起` + `.visible` if persisted.
- Row layout matches demo: button is first child, status second, textarea third (`btn.nextElementSibling.nextElementSibling` reaches the textarea).

## Source reference
- Demo JS: `.omo/drafts/design-preview.html:543-605`
- Real essay HTML: `docs/writing/task1/01-table-universities-ranked.html:14-52` (prompt + essay + rubric + keywords structure)
- IIFE pattern: `docs/speaking/assets/js/learning-mode.js`
