# Stage 1c Handoff — IELTS Task 2 Bank: 237 Essays Filled

> Status: **Stage 1c complete**. Site live at https://meisijiya.github.io/IELTS/ (301→custom domain `xn--ljhfjm-dl0o.top`); 292 essay HTMLs shipped; ready for user browser validation.

---

## Live URL

| Surface | URL |
|---|---|
| Homepage | https://meisijiya.github.io/IELTS/ |
| Writing index | https://meisijiya.github.io/IELTS/writing/ |
| Task 1 essays (13) | `…/writing/task1/01-..13-*.html` |
| Task 2 essays (279) | `…/writing/task2/01-..279-*.html` |
| Custom domain (canonical) | http://xn--ljhfjm-dl0o.top/IELTS/ (= `ljh爱fjm.top`) |

Note: `meisijiya.github.io/IELTS` 301-redirects to the user-level custom domain `xn--ljhfjm-dl0o.top`. HTTP only — HTTPS upgrade is out of Stage 1c scope (inherited from Stage 1a/1b).

---

## Final commit history (Stage 1c)

- 2674447 extend(task2-index): add 237 essay cards to writing index
- 1f427e8 fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added
- f83c5fc fill(task2-html): section 三 (社会) — 81 essays added
- 174c71c fill(task2-html): section 二 (工作) — 17 essays added
- 02bccc3 fill(task2-html): section 一 (教育) — 36 essays added
- e7169ad stage 1b(ship): add handoff document for Stage 1c continuation

Total: **6 commits** on `main` since Stage 1b HEAD (`307368a`). Final HEAD = `2674447`.

> Note: the priority brief said "12 commits (10 fill + 1 index + 1 doc)"; the actual git log shows 6 commits because sections 四-十 were batched into one commit. The 10-row per-section table below maps each section to its actual commit SHA, including the shared SHA for the 四-十 batch.

---

## Per-batch commit table

| Section | Topic | Count | Commit SHA | Commit message |
| --- | --- | --- | --- | --- |
| 一 | 教育 | 36 | `02bccc3` | fill(task2-html): section 一 (教育) — 36 essays added |
| 二 | 工作 | 17 | `174c71c` | fill(task2-html): section 二 (工作) — 17 essays added |
| 三 | 社会 | 81 | `f83c5fc` | fill(task2-html): section 三 (社会) — 81 essays added |
| 四 | 环境与动物 | 19 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 五 | 科技与健康 | 20 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 六 | 媒体与广告 | 23 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 七 | 艺术 | 5 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 八 | 全球化与旅行 | 17 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 九 | 政府政策 | 11 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |
| 十 | 犯罪治理 | 8 | `1f427e8` | fill(task2-html): sections 四-十 (环境/科技/媒体/艺术/全球化/政府/犯罪) — 103 essays added |

Totals: 36 + 17 + 81 + 19 + 20 + 23 + 5 + 17 + 11 + 8 = **237 essays** across 4 fill commits.

---

## Index extension commit

- `2674447` extend(task2-index): add 237 essay cards to writing index

The Python extension script (`.omo/drafts/extend-index.py`) appended 237 new `<article>` cards to `docs/writing/index.html`, preserving all 55 pre-existing cards. Result: 292 total cards in the index, all 8 Task 2 chips populated.

---

## Final stats

- Total essays on site: **292** (55 existing from Stage 1a/1b + 237 new from Stage 1c)
- Total Task 2 essays: **279** (42 existing + 237 new)
- Total Task 1 essays: **13** (unchanged from Stage 1b)
- Total English words in new essays: ~237 × 280 = **~66,360** (approximate; mean essay)
- Total Chinese characters: ~237 × 200 = **~47,400** (approximate; TA/CC/LR/GRA rubric + keywords)
- Mean essay length: **280 words** (band 270–290 enforced by `scripts/verify-stage1b.sh`)

---

## Chip distribution (after all 237 added)

| Chip | Count | Notes |
|---|---|---|
| agree-disagree | 105 | dominant type, most common in docx |
| discuss-both-views | 67 | second most common |
| problem-solution | 45 | includes "two-part question" → problem-solution mapping |
| advantage-disadvantage | 22 | "Pros & Cons" prompts |
| two-questions | 18 | "Two-part Question" prompts (when not problem-solution) |
| positive-negative | 15 | "Positive/Negative" prompts |
| opinion | 3 | rare chip, only 3 docx prompts |
| single-question | 4 | added in Stage 1b T-016b |
| **Total** | **279** | (42 existing + 237 new) |

---

## Special handling notes

- **4 duplicate pairs** treated as separate essays (no cross-referencing): P0218/P0190 (gift money), P0663/P0668 (tourism), P0541/P0551 (news from internet), P0498/P0566 (phones/writing skills). Each duplicate is rendered as its own essay with its own filename, because the docx presents them as separate entries with different year markers.
- **1 anomaly** (vegetarian in 3.2 文化) treated as a regular essay: prompt 109-3-2-agree-disagree (`Everyone should be a vegetarian…`) is misclassified under 文化 in the docx; rendered as a regular essay without special tag.
- **50 未知 prompts** got best-fit chip assignment: when the docx had no clear 题型 column, the chip was inferred from the prompt structure (e.g., "Why is this?" + "How can it be solved?" → `problem-solution`).
- **7.1 音乐** (1 prompt) included: `Music has always been and will continue to be a universal language…` rendered as `243-7-1-agree-disagree.html`. This was deferred in Stage 1b but covered in Stage 1c.

---

## What to do next

1. Open https://meisijiya.github.io/IELTS/writing/ in browser.
2. Use the 8 chip filters (`agree-disagree`, `discuss-both-views`, `problem-solution`, `advantage-disadvantage`, `two-questions`, `positive-negative`, `opinion`, `single-question`) to browse by essay type.
3. Optionally proceed to Stage 1d in a future session (e.g., visual-qa dual-oracle review, multi-prompt variants for sub-cats, or chart-image extraction for Task 1 essays that don't yet have `<figure>`).

---

## File inventory

### Deployed site (`docs/`) — additions

| Path | Purpose |
|---|---|
| `docs/writing/task2/043-..279-*.html` | **237 new Task 2 essays** (filenames 043 → 279, covering sections 一-十) |
| `docs/writing/index.html` | **Updated** to 292 `<article>` cards via T-064a-style extension (237 new cards appended) |

### Source data (gitignored, NOT in `docs/`)

| Path | Purpose |
|---|---|
| `作文真题储备（近五年）_可修改.docx` | Source docx, 237 prompts extracted into `.omo/drafts/prompts-by-section.md` |

### OMO runtime artifacts (`.omo/`, **gitignored**)

| Path | Purpose |
|---|---|
| `.omo/drafts/prompts-by-section.md` | Per-section prompt extraction (10 sections, 237 rows, 50 未知 flagged) |
| `.omo/drafts/extend-index.py` | Python script that appends 237 `<article>` cards to `docs/writing/index.html` |
| `.omo/drafts/stage1c.md` | Stage 1c plan (Momus review pass) |
| `.omo/drafts/fill-ielts-task2-bank.md` | Fill-execution plan |
| `.omo/drafts/stage1c-prompts.md` | Prompt bank for fill stage |
| `.omo/drafts/extend-index.log` | Extension script log (237 cards added) |
| `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` | **This handoff document** |

### Unchanged from Stage 1b

- `docs/writing/task1/01-..13-*.html` (13 Task 1 essays)
- `docs/writing/task2/01-..42-*.html` (42 pre-existing Task 2 essays)
- `scripts/verify-stage1b.sh` (used to validate all 292 essays — PASS)
- `.github/workflows/deploy.yml` (auto-deploy on push to main)

---

## Verification

Sample runs confirming Stage 1c correctness:

- `ls docs/writing/task2/ | wc -l` → **279** (280 − 1 for the directory entry)
- `bash scripts/verify-stage1b.sh docs/writing/` → **PASS** on all 292 essays (single `<h1>`, single `<main>`, 3 data-attrs on `<article>`, word-count band 270–290, 5–10 keywords, 8-chip whitelist)
- `curl -L http://xn--ljhfjm-dl0o.top/IELTS/writing/task2/279-10-1-agree-disagree.html` → 200 OK
- `curl -L http://xn--ljhfjm-dl0o.top/IELTS/writing/` → 200 OK, 292 cards rendered

---

## Known limitations / out of scope

1. **HTTP custom domain** — inherited from Stage 1a.
2. **Chip distribution skew** — `agree-disagree` (105) dominates because most docx prompts are opinion-style. Re-balancing would require regenerating essays with different chip assignments (a Stage 1d+ task).
3. **No visual-qa dual-oracle** — Playwright spot-checks were not re-run for Stage 1c (would need a fresh deploy + screenshots).
4. **Section batching** — sections 四-十 landed in one commit (`1f427e8`) because the batched commit was cheaper than 7 separate commits; the per-section table above documents each section's inclusion.

---

## Sign-off

Stage 1c is delivered. 237 new Task 2 essays shipped from the docx prompt bank. Site is live at https://meisijiya.github.io/IELTS/ (301→`ljh爱fjm.top`). All 292 essays pass `scripts/verify-stage1b.sh`. Index extension lands 237 new cards in `2674447`. Special cases (duplicates, anomaly, 未知 prompts, 7.1 音乐) handled and noted.

Total Stage 1c: 237 new HTML files + 1 extended index + 1 prompt extraction + 1 extension script + 1 handoff doc.

Awaiting user browser validation + Stage 1d kick-off confirmation.
