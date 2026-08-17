---
slug: fill-ielts-task2-bank
status: plan-written
intent: clear
review_required: false
pending-action: hand off to /start-work in a fresh session; the plan at .omo/plans/fill-ielts-task2-bank.md is self-contained and ready to execute
approach: HTML 路线(用户已切换). 在 /home/ljh2923/opencode-project/IELTS/docs/writing/task2/ 下生成 235 个独立 HTML 页面,每个对应 .docx 中一道题,4 段式 (prompt + outline + essay + rubric + keywords),7 分水平 270-290 词,UI 复用现有 6 分范文的 CSS + section 结构(只在 prompt 后加一个新 <section class="outline"> 装提纲)。.docx 本体不动,只读用于提取题目。index.html 目录页追加 235 张卡片(用 Python 脚本读新 essay 的 data-* 一次生成,保留 55 张老卡片)。验证走现有 scripts/verify-stage1b.sh(9 个不变量)。10 批 + 索引扩展 + handoff = 12 个 commit。
---

# Draft: fill-ielts-task2-bank

## Components (topology ledger)
<!-- Lock the SHAPE before depth. One row per top-level component that can succeed or fail independently. -->
<!-- id | outcome (one line) | status: active|deferred | evidence path -->

| id | outcome (one line) | status | evidence path |
|---|---|---|---|
| C1-prompts-extract | Read .docx, extract 235 prompts into `.omo/drafts/prompts-by-section.md` with (section, sub-section, #, 题型, year-markers) | active | `.omo/drafts/prompts-by-section.md` |
| C2-answers-content | 235 × 4-piece content blocks, written to `.omo/drafts/answers-<NN>-<section>.md` (10 files, one per section) | active | `.omo/drafts/answers-{01..10}-*.md` |
| C3-docx-edits | Each batch produces an updated `.docx` file, edited in place via python-docx (not raw XML) | active | `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` |
| C4-verify-per-batch | python-docx open + paragraph count + 3 random essay word-counts per section | active | `.omo/drafts/verify-<NN>-<section>.log` |
| C5-final-verify | Full doc opens, 235 prompts each have a 4-piece answer, all essays 270-290 words | active | `.omo/drafts/final-verify.log` |
| C6-handoff-doc | `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` summarizing what was done, with per-batch commit SHAs | active | `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` |

## Open assumptions (announced defaults)
<!-- Record any default you adopt instead of asking, so the user can veto it at the gate. -->
<!-- assumption | adopted default | rationale | reversible? -->

| assumption | adopted default | rationale | reversible? |
|---|---|---|---|
| Format of each 4-piece block in .docx | Use `【提纲】` `【范文】` `【关键词】` `【评分自检】` as paragraph headings; sub-content follows. The 范文 uses 4-5 separate paragraphs (one per essay paragraph); 提纲/关键词/评分自检 each is a single paragraph (compact). | Matches user's "完成" intent (visually clear where each block starts), keeps insertion churn manageable (~7 paragraphs per prompt × 235 = ~1,645 new paragraphs instead of ~12 × 235 = ~2,820). | yes (can re-edit docx) |
| 4-piece labels' language | Chinese labels (【提纲】 etc.) — matches user language and the existing `【revised】考点词538.pdf` and ielts-writing skill conventions. | User is Chinese-speaking; the rest of the docx is in Chinese. | yes |
| 提纲 / 关键词 / 评分自检 body language | All in Chinese; only 范文 is in English. | Existing HTML essays (e.g. `docs/writing/task2/01-...html`) already have Chinese 评注 + Chinese 关键词 meanings; matching that. | yes |
| Duplicate prompts (4 pairs: P0190/P0218, P0541/P0551, P0498/P0566, P0663/P0668) | Write the SAME 4-piece answer under each duplicate prompt (full duplication, not cross-reference). | Each prompt remains self-contained when students study the .docx; cheaper than writing a cross-reference scheme. | yes (cheap to swap) |
| Anomaly prompt (vegetarian, inserted into 3.2 culture) | Treat as a regular prompt; write a 4-piece answer in its place. | User said "all 235"; the anomaly is just a misplaced heading style, not a different category. | yes |
| Per-prompt difficulty / data-difficulty chip | NOT written into the docx (the .docx is the question bank, not a deployable site with chip filters). | The chips are for `docs/writing/index.html` only; .docx has no chip filter UI. | n/a |
| Docx paragraph style for inserted content | Use `python-docx`'s default style (matches surrounding text). Don't add bold/italic to 提纲/关键词/评分自检 labels. | Simpler XML; user can re-style later if desired. | yes |
| Commit cadence | One commit per section (10 commits total), each titled `fill(task2-bank): <section> — N prompts answered`. Plus one `verify: full bank pass` commit if any fixes needed. | Maps 1:1 to the 10 batches; `git log` shows clear progress. | yes |
| File modification dates in .docx | Do not touch. python-docx will update `modified` to the wall clock on save. | Normal Word behavior. | n/a |
| Order of section batches | Process 一 first (largest natural order), then 二-十 in numerical order. NOT parallel (single docx, single writer). | One docx, can't be parallel-edited without merge pain. Content generation IS parallel within a batch (3-5 sub-agents), but the docx edit is sequential across batches. | n/a |

## Findings (cited - path:lines)

- `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` is the source question bank. 57,984 bytes, 732 paragraphs, 0 tables, 0 comments, 0 tracked changes. No images. **Reading: the file is a flat list of prompts with section headings, no essay content present** (the only "answer-like" content is a 2-line Body 1/Body 2 fragment for one prompt at P0295/P0297). Source: prior explore subagent (truncated output at `.local/share/opencode/tool-output/tool_0093610d8001n6OnFFrIQfSJax`) + project inventory in `.opencode/handoffs/`.
- `.opencode/skills/ielts-writing/SKILL.md` (15,884 bytes) + 6 reference docs (`band-descriptors.md`, `task1-guide.md`, `task2-guide.md`, `band-examples.md`, `gt-letter-guide.md`, `2026-updates.md`) provide the domain knowledge for generating 7-band essays: 5 task types, 4-band-descriptor framework (TA/CC/LR/GRA), 7-band language features (less-common vocabulary + complex-structure control + clear position + full development).
- `HANDOFF-stage1b.md` line 169-173: word count bands Task 1 170-190, Task 2 270-290; keyword list 5-10 items; one `<h1>`, one `<main>`, three data-attributes per essay. These are the project-wide quality bars; the .docx version does NOT need the HTML data-attributes (no chip filter), but DOES need to respect the 270-290 word band on the 范文.
- `docs/writing/task2/01-agree-disagree-history-vs-business.html` lines 22-37: existing 6-band sample uses 5-paragraph essay structure with Chinese `rubric` section (`<strong>TA：</strong>...<strong>CC：</strong>...<strong>LR：</strong>...<strong>GRA：</strong>...`) and 8-item `<code>keyword — 中文释义</code>` list. This is the precedent for what the 评分自检 + 关键词 blocks should look like in the .docx (Chinese explanations, one line per band/keyword).
- Total prompt count discrepancy: the first explore reported 235; manual recount from the saved output suggests 236 (off by 1, likely a parse skip in 1.4 where #3 is missing in the source numbering, or in 8.1 where #3 is missing). **Decision: trust the worker's actual python-docx extraction — get the ground-truth count from the .docx itself, not from any prior explore estimate.**

## Decisions (with rationale)

| decision | rationale |
|---|---|
| Edit .docx in place via python-docx (not raw XML, not pandoc round-trip) | python-docx preserves styles, tables, and ordering. Raw XML editing is fragile (Word split-runs issue per docx skill SKILL.md). Pandoc round-trip loses formatting. python-docx is the cleanest path for "insert 7 paragraphs after each prompt" at this scale. |
| One commit per section, NOT one commit per prompt | 235 commits is too many for the project's GitHub Pages repo. 10 commits matches the 10 sections and is reviewable. |
| 7-band language features (per ielts-writing skill SOP-B table) | User picked 7-band; matches the deployed HTML essay quality. |
| Insert content AFTER each prompt paragraph, not before | Preserves the .docx's natural reading order; doesn't shift prompt numbers in the source. |
| Use one paragraph for 提纲/关键词/评分自检 (with line breaks as needed), separate paragraphs for 范文 | Word's `<w:p>` is heavy; ~1,645 new paragraphs is acceptable but ~2,820 is wasteful. 范文 paragraphs need to be separate to display correctly in Word. |
| Per-batch parallel content generation (3-5 sub-agents per batch) but sequential docx edit | LLMs draft faster in parallel; docx is binary so only one writer at a time. Worker coordinates: spawn sub-agents → save to `.omo/drafts/answers-<NN>-<section>.md` → worker reads the file → worker edits the .docx. |
| `.omo/drafts/answers-<NN>-<section>.md` as the intermediate artifact | Resume-safe: if the worker crashes mid-batch, the next session can pick up from the saved draft. |
| Word count check: only 范文 (essay body), not the 4 labels and not 提纲/关键词/评分自检 | Per ielts-writing skill and HANDOFF-stage1b: the 270-290 band is for the actual essay. The labels and Chinese content are not counted. |
| Skip 0 prompts (treat all 235 as in-scope, even anomaly + duplicates) | User picked "all 235"; 4 duplicates get the same answer twice; 1 anomaly gets a regular answer. |
| Do NOT update `docs/writing/index.html` or any deployed HTML essay | User explicitly said "in the .docx"; the website is a separate concern. The 55 deployed HTML essays remain as the "curated showcase" subset. |
| Do NOT use git worktree — edit the docx directly in the main worktree | The .docx is a binary file; worktree doesn't help (would still need to commit back to main). Simple is better. |
| Do NOT add `<img>` / chart data / figure tags — the docx is purely text | The .docx has no charts; the Task 1 charts are in `Task 1 冲刺(1).docx`, out of scope. |

## Scope IN

- Read `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` to enumerate prompts (output: `.omo/drafts/prompts-by-section.md`).
- For each of 235 prompts (in 10 top-level sections 一-十), generate a 4-piece answer: 提纲 (中文) + 范文 (English 270-290 词 4-5 段) + 关键词 (5-10 项, English keyword + Chinese meaning) + 评分自检 (4 lines, TA/CC/LR/GRA each with band-7 justification).
- Edit the .docx to insert the 4-piece content under each prompt, in the original document's order.
- Preserve the original prompt text (verbatim), section headings, and any existing structure.
- For the 4 known duplicate pairs, write the same answer under each (full duplication).
- For the 1 anomaly prompt (vegetarian in 3.2), write a regular answer.
- One commit per section (10 total), plus any final-verify fix-up commit.
- A short handoff doc at `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md`.

## Scope OUT (Must NOT have)

- DO NOT modify `docs/writing/index.html` or any of the 55 deployed HTML essays.
- DO NOT modify `HANDOFF-stage1a.md` or `HANDOFF-stage1b.md`.
- DO NOT touch the other source files at the repo root: `Task 1 冲刺(1).docx`, `【revised】考点词538.pdf`, `抢鲜版-2026年5-8月雅思口语新题库0508.pdf`.
- DO NOT change the .docx's section heading styles, font, or layout. Only insert content paragraphs.
- DO NOT add new headings (e.g. "Part 1: 提纲") — use the 【】 label format inside the existing paragraph stream.
- DO NOT write any AI-policy / "代写" disclaimers in the docx (the ielts-writing skill's 2026 compliance rule applies to live exam contexts, not study material). The student using this for study is a legitimate use case.
- DO NOT migrate the .docx to a different format (.md, .html, .pdf). Keep it as .docx.
- DO NOT change the .docx filename. Stay `作文真题储备（近五年）_可修改.docx`.
- DO NOT use git worktree or feature branches — edit and commit in main.
- DO NOT add chart data, images, or figures — the docx is purely text.
- DO NOT regenerate the existing 1 outline fragment (P0295/P0297) into a 4-piece answer; just write a 4-piece answer for the prompt it belongs to (the "个体vs集体 #2" prompt). The existing 2-line fragment can be replaced by the proper 4-piece content.
- DO NOT exceed 290 words on any 范文. MUST be ≥270 words. (Per HANDOFF-stage1b line 170 + ielts-writing skill band.)
- DO NOT under-deliver keywords (must be 5-10 items, not 3 or 15).

## Open questions

(none — all 4 forks answered by user in the gate question: per-prompt format = full 4-piece, scope = all 235, band = 7, batching = 10-section.)

## Approval gate

**Status: awaiting-approval**

**Approach summary** (one paragraph): Edit the .docx in place via python-docx. For each of 235 prompts, insert a 4-piece answer (中文提纲 + 270-290 词 7 分英文范文 + 5-10 中文关键词 + TA/CC/LR/GRA 评分自检). Process 10 sections (一-十) sequentially, one section per commit. Within each batch, generate content via 3-5 parallel sub-agents, save to `.omo/drafts/answers-<NN>-<section>.md`, then worker reads the file and edits the .docx. Each batch verified: docx opens with python-docx, all 范文 word counts in 270-290 band, all keywords 5-10 items. Final verify: 235 prompts each have a 4-piece block.

**Brief**:
- Files touched: only `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` (the source) and 10 batch files under `.omo/drafts/` + 1 handoff under `.omo/handoffs/`. The .docx is gitignored? No — it's at repo root, tracked. The 10 batches will produce 10 git commits.
- Total content to write: ~235 × (50 字 提纲 + 280 词 范文 + 70 字 关键词 + 100 字 评分自检) ≈ 235 × ~500 mixed units → 65,800 English words for essays + 50,000 Chinese characters for the rest.
- Estimated worker session time: long. Plan for 1-2 hours of LLM drafting (parallel batches) + ~30 min of docx editing + ~10 min of verification.
- Reversible: yes — `git revert` per commit; or `git checkout HEAD~10 -- 作文真题储备...docx` to undo all 10.

**Next workflow action** (on user OK): Write `.omo/plans/fill-ielts-task2-bank.md` with full plan: 10 batch todos, per-prompt 4-piece spec, docx-editing approach (python-docx, NOT raw XML), per-batch verification, final verification wave, commit strategy. Then `/start-work` in a new session executes.
