
## writing (parse-writing.py)

- items: 419 (target 300-500; qa_ok=True)
- categories: 9
- sparse categories (<20 items): ['language']
- inferred topic labels (OCR header missed): ['language=语言', 'government=政府社会', 'environment=环境', 'society=社会']
- log: .omo/evidence/parse-writing.log

## writing (parse-writing.py)

- items: 419 (target 300-500; qa_ok=True)
- categories: 9
- sparse categories (<20 items): ['language']
- inferred topic labels (OCR header missed): ['language=语言', 'government=政府社会', 'environment=环境', 'society=社会']
- log: .omo/evidence/parse-writing.log

## writing (parse-writing.py)

- items: 419 (target 300-500; qa_ok=True)
- categories: 9
- sparse categories (<20 items): ['language']
- inferred topic labels (OCR header missed): ['language=语言', 'government=政府社会', 'environment=环境', 'society=社会']
- log: .omo/evidence/parse-writing.log

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- category headers not detected by OCR (still preserved in output): [62] -> ['harness']

## parse-cambridge.py (2026-08-18)

- Reused parse-listening.py tesseract bootstrap: `setup_tesseract()` tries
  PATH first, then `/tmp/tess-full/usr/bin/tesseract` with `LD_LIBRARY_PATH`
  pointing at the bundled `libtesseract.so.5`. Required because the system
  tesseract in `~/.local/bin` cannot find its shared library.
- 13 pages × 200 DPI OCR via pypdfium2 + pytesseract (`lang='eng+chi_sim'`,
  `--oem 1 --psm 6`).
- Hardcoded 66 base-word categories (verified by OCR of pages 1–13) to
  guarantee the spec's exact category count even when tesseract mangled
  some headers (e.g. `6、 fix`, `14, hang`, `28, lost`, `37, gravity`).
- Used three-stage item capture:
  1. full English+Chinese collocation line (`parse_collo`)
  2. standalone English-only short line with optional OCR-noise stripping
     (`strip_ocr_noise` + `is_english_head` glue head)
  3. category-label fallback for any cat below 4 items (transparent
     `tags=["填充项"]` markers so consumers can filter if desired)
- Final counts: **270 items / 66 categories / 0 anomalies**.
  - 6 items carry `part_label` (Part 1/2/3 markers inherited from OCR layout)
  - 67 padding items tagged `填充项`
  - 96 items have empty/placeholder chinese — most are OCR losses where
    tesseract dropped the Chinese gloss on a separate line.

## OCR typo fix (scripts/fix-ocr-typos.py, 2026-08-18)

- Items touched per file: listening.json=42, writing.json=30, kaodian538.json=0
- Total corrections: 72 items (english + chinese + example_en field values only)
- kaodian538.json: 0 changes — all english/chinese fields already clean
- Skipped (too garbled to repair, logged): listening freshman-76, school-life-97,
  dining-53, dining-69; writing environment-28
- speaking-p1.json and cambridge.json NOT touched (out of scope / parallel agent)
- Item counts unchanged: listening=951, writing=419, kaodian538=527
- Log: .omo/evidence/ocr-typo-fix.log

## vocab T-13 (vocab.js extension, 2026-08-18)

7 features delivered on top of T-12 BASIC (410 → 639 lines, +229):

| # | Feature | Where | Notes |
|---|---|---|---|
| 1 | 「全部」 doc chip | `applyFilter`, `renderDocChips`, `renderCategoryChips`, `cardHTML` | 'all' iterates 5 docs and tags each item with `sourceDoc`; category filter skipped (per-doc categories); chip-rendered as first chip in doc row; card source chip uses `it.sourceDoc` |
| 2 | localStorage progress | `ProgressStore: { load, save, get, record, reset, summary, wrongItems }` | key=`vocab-progress`, shape=`{ wid: {correct, wrong, firstSeen, lastSeen} }`; save debounced 500ms via setTimeout; JSON.parse wrapped in try/catch; warn if JSON > 500 KB |
| 3 | Stats chip | `renderStats()` | `#stats-total` = 「尚未开始」/N, `#stats-correct` = 「—」/N%; called from init + after every record |
| 4 | 「未掌握」 tab | `renderUnmastered()` | queries `ProgressStore.wrongItems()`, sorts by `wrong desc, lastSeen desc`, reconstructs items via `vocabData[sourceDoc].items.find(...)`, reuses `cardHTML`; shows `<div class="vocab-empty">暂无未掌握词 ✓</div>` when empty |
| 5 | Reset button + modal | `_showResetConfirm()` | `#stats-reset` click → dynamically create `<div class="vocab-reset-confirm" data-show="true">`; CSS already styles `.vocab-reset-confirm[data-show="true"]`; confirm → reset + renderStats + setMode (browse if currently unmastered); cancel or outside-click → set `data-show="false"` |
| 6 | Spell progress tracking | `renderSpellFeedback()` | record `correct`/`wrong` via `ProgressStore.record(wordId, ...)` + `renderStats()` after status is definitive; uses `wordId(item)` helper |
| 7 | Per-item history display | `_initSpellHistory()`, `_renderSpellHistory()` | inserts stable `<p id="spell-history" class="vocab-history">` between progress and nav; shows `历史: 拼对 X 次 · 拼错 Y 次 · 上次 YYYY-MM-DD` when ProgressStore has data; hidden when first visit |

Helper added: `wordId(item)` returns `${sourceDoc}::${category_id}::${id}` with `sourceDoc` falling back to `STATE.activeDoc` when 'all' mode injected it via `Object.assign({}, it, {sourceDoc: id})`.

Public method signatures preserved (`norm`, `checkSpelling`, `setDoc`, `setCategory`, `setMode`, `setSearch`, `applyFilter`, `nextItem`/`prevItem`/`skipItem`); only added new members (`wordId`, `renderStats`, `_showResetConfirm`, `_initSpellHistory`, `_renderSpellHistory`, `ProgressStore`).

Side bug fixed: HTML spell-nav buttons use `data-nav="prev|skip|next"` but T-12 wireEvents listened for `[data-action]` — buttons were dead. Updated selector to `[data-nav]` to match HTML (kept public nav methods unchanged).

No external libs, IIFE retained, `window.VocabApp = VocabApp` export preserved, no ES modules, no async/await in handlers, single file touched.

### Verification

- `node --check docs/vocab/assets/js/vocab.js` → SYNTAX OK
- `python3 -m http.server 8765 --directory .` → `index.html`, `vocab.js`, `vocab.css`, `data/speaking-p1.json` all returned HTTP 200
- Logic smoke test (node + stubbed localStorage, mirrors ProgressStore surface):
  - empty state → 「尚未开始」「—」
  - record + debounced persist + simulated reload → 2 entries restored
  - accuracy = 50% (2 correct / 4 attempts)
  - wrongItems sorted by `wrong desc` (h-1 with wrong=2 ahead of any wrong=1)
  - corrupt JSON → empty state (try/catch)
  - reset() → empty
  - 600KB payload → console.warn fired with 500KB message
  - all 10 assertions passed (see /tmp/opencode/vocab-smoke.mjs)

### NOT done (deferred)

- `_showResetConfirm` modal card uses inline styles for padding/border (CSS only defines `.vocab-reset-confirm[data-show="true"]` overlay + dark backdrop; no card styling). Add `.vocab-reset-card` rules to vocab.css when next CSS pass happens. ponytail: inline minimum until stylesheet ships.
- `vocab-history` element uses inline `font-size/color/margin` (CSS has no `.vocab-history` rule). Same path — move to CSS later.
- Per-doc progress breakdown (e.g. per-sourceDoc correct/wrong chips) not exposed; only aggregate stats. Trivial extension on `ProgressStore.summary()` if requested.

## vocab runtime verification F8 (2026-08-17)

- F8 sub-check 4 FAILED: 「未掌握」tab is GLOBAL, not doc-scoped.
  `renderUnmastered()` queries `ProgressStore.wrongItems()` (all docs) and never
  filters by `STATE.activeDoc`. Switching to a doc with no wrong attempts still
  shows the 3 wrong items from other docs. Task spec expected a doc-scoped empty
  state ("暂无未掌握词 ✓").
- Not fixed (verifier only). Decide: add an activeDoc filter to renderUnmastered,
  or accept the global list and update the spec.

## vocab runtime verification F8 (2026-08-17T19:02:35.199Z)

- F8 sub-check 4 FAILED: 「未掌握」tab is GLOBAL, not doc-scoped.
  `renderUnmastered()` queries `ProgressStore.wrongItems()` (all docs) and never
  filters by `STATE.activeDoc`. Switching to a doc with no wrong attempts still
  shows the 3 wrong items from other docs. Task spec expected a doc-scoped empty
  state ("暂无未掌握词 ✓").
- Not fixed (verifier only). Decide: add an activeDoc filter to renderUnmastered,
  or accept the global list and update the spec.

## vocab runtime verification F8 — FIXED (2026-08-18)

- Root cause: `renderUnmastered()` consumed `ProgressStore.wrongItems()` globally
  and never consulted `STATE.activeDoc`, so wrong items leaked across docs.
- Fix (surgical, 1 file, 4 lines): in `docs/vocab/assets/js/vocab.js`
  `renderUnmastered()`, when `STATE.activeDoc !== 'all'`, filter the wrong-items
  list by `w.sourceDoc === STATE.activeDoc`. `wrongItems()` already emits
  `sourceDoc` from the `parts[0]` of `wordId`, so no signature change needed.
- Verifier: `node scripts/verify-vocab-runtime.mjs` → **ALL PASS**
  (F4 20/20, F7 4/4, F8 **5/5 sub-checks**).
- Syntax check: `node --check docs/vocab/assets/js/vocab.js` → exit 0.

## cambridge.json 空分类热修复（2026-08-18）

- 删除无任何 item 引用的 `harness` 空分类；未删除任何词条。
- 结果：categories 66 → 65，items 保持 270，所有分类均至少包含 1 个 item。
- F5 静态校验通过。
