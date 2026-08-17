# fill-ielts-task2-bank - Work Plan

## TL;DR (For humans)

**What you'll get:** N independent HTML essay pages in `docs/writing/task2/` (N=235 or 236 from Todo 1), one per prompt from the .docx, plus an extended `docs/writing/index.html` directory with N new cards. Each page reuses the existing UI (same CSS, same nav, same section structure as the 55 already-deployed essays) and adds a 5-piece body — prompt + 提纲 outline + 范文 (270-290 word 7-band essay) + rubric (TA/CC/LR/GRA self-check) + 5-10 keywords. The deployed website becomes a complete self-study reference, filterable by the 8 existing Task 2 chips.

**Why this approach:** The project's existing pattern is HTML essays + chip-filtered index (Stage 1a + 1b, 55 essays). Reusing that pattern means: no new CSS, no new UI work, the worker just writes N more HTML files using the same template, then extends the index with N new `<article>` cards. The 8-chip whitelist and `scripts/verify-stage1b.sh` (6 Task 2 invariants: 1 h1, 1 main, 3 data-attrs on one line, 5-10 keywords, 270-290 word band, chip in 8-whitelist; AC-T1 is task1-only and not enforced here) already enforce correctness, so per-batch verification is a single bash command. The .docx is left untouched — it remains the source question bank; the website becomes the answer bank.

**What it will NOT do:** Won't modify the .docx, the HANDOFF docs, the CSS, the index's filter JS, the GitHub Actions workflow, or any of the 55 existing HTML essays. Won't add new chips. Won't add chart data (Task 2 is text-only).

**Effort:** XL — 235 essays × ~500 mixed units of content (~65,800 English words + ~50,000 Chinese chars); the worker session is multi-hour.

**Risk:** Medium — main risks are (a) per-essay file format violations caught by `verify-stage1b.sh`, (b) chip classification ambiguity for ~50 未知 prompts. Mitigated by running verify after every batch + per-essay difficulty/chip classification done at Setup (Todo 1) so sub-agents don't have to invent.

**Decisions to sanity-check:**
- All 235 prompts become 235 HTML pages (no merging of duplicates — each prompt is its own self-contained page, even the 4 duplicate pairs)
- 8-chip whitelist kept as-is (no new chips added)
- One commit per section (10) + one index-extension commit + one handoff commit (12 total)
- Existing 6-band essays stay; new 235 are 7-band (one notch up in vocabulary + structure complexity)
- The 1 anomaly prompt (vegetarian in 3.2) and 4 duplicate prompt pairs each get their own essay page

Your next move: hand the plan to a worker via `/start-work` in a fresh session. The plan is self-contained; the worker reads only this file + the 4 inline references to execute.

---

> TL;DR (machine): XL, Medium, N=235 (or 236) HTML pages + index extension, 12 commits on main (each pushed), 6 Task 2 invariants enforced by verify-stage1b.sh.

## Scope

### Must have

- Open `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` via python-docx (read-only) and extract every prompt into `.omo/drafts/prompts-by-section.md` with columns: # (1-based across whole doc), Section (一-十), Sub-section (e.g. 1.1), Sub-section #, English prompt text (verbatim), Year markers, 题型, **suggested chip** (one of 8), **suggested difficulty** (easy/medium/hard), **filename slug** (e.g. `43-1-1-agree-disagree.html`). **Ground-truth count**: take from the .docx, do not trust prior estimates.
- For each of 235 prompts, generate ONE HTML file at `docs/writing/task2/<NN>-<sub-section>-<slug>.html` with this EXACT structure (reused from existing 6-band template + one new section):
  - `<!doctype html>`, `<html lang="en">`, `<head>` with title pattern `Task 2 — <Topic> (<chip>) | IELTS Writing 7-band samples`, favicon + CSS links to `../../favicon.svg` and `../../assets/css/style.css`
  - `<nav class="crumbs">` with Home › Writing › Task 2 › <Topic> links
  - `<main>` containing exactly one `<article data-task="task2" data-difficulty="..." data-type="...">` with 5 `<section>` children:
    1. **`<section class="prompt">`** — original prompt text in a `<p>` (verbatim from .docx, with year marker)
    2. **`<section class="outline">`** — 1 `<p>` with format `立场: <chinese>; 理由1: <chinese>; 理由2: <chinese>` (new — replaces the 3-piece Stage 1b template with a 5-piece template; 提纲 is the new section)
    3. **`<section class="essay">`** — 4-5 `<p>` paragraphs, 270-290 English words total, 7-band language features
    4. **`<section class="rubric">`** — 2 `<p>`: first has `<strong>TA：</strong>...`; second has `<strong>CC：</strong>...<strong>LR：</strong>...<strong>GRA：</strong>...`
    5. **`<section class="keywords">`** — `<ul>` with 5-10 `<li>` items, each `<code>english-keyword</code> — 中文释义`
  - `<header>` inside article with exactly one `<h1>` matching the title pattern
- For the 4 known duplicate pairs (P0190/P0218, P0541/P0551, P0498/P0566, P0663/P0668), each prompt gets its OWN essay page (full duplication; do NOT cross-reference).
- For the 1 anomaly prompt (vegetarian in 3.2), a regular 7-band essay page.
- One commit per section (10 total) with format `fill(task2-html): section <X> (<Chinese name>) — N essays added`.
- After all 10 section commits: one **index-extension commit** that extends `docs/writing/index.html` with 235 new `<article>` cards (one per new essay), preserving the existing 55 cards. The 235 cards are emitted by a Python script (mirroring Stage 1b's T-064a) that reads each new essay's `<article data-task data-difficulty data-type>` + `<h1>` title and emits matching cards.
- A handoff doc at `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` summarizing what was done with per-batch commit SHAs and the final word-count summary.

### Must NOT have (guardrails, anti-slop, scope boundaries)

- DO NOT modify `作文真题储备（近五年）_可修改.docx` (it's the source question bank; user said the work goes to the website, not back into the docx).
- DO NOT modify `HANDOFF-stage1a.md`, `HANDOFF-stage1b.md`, or `.opencode/`.
- DO NOT modify the other source files at the repo root: `Task 1 冲刺(1).docx`, `【revised】考点词538.pdf`, `抢鲜版-2026年5-8月雅思口语新题库0508.pdf`.
- DO NOT modify `docs/assets/css/style.css`, `docs/favicon.svg`, the filter JS in `docs/writing/index.html`, or any of the 55 existing HTML essays.
- DO NOT add new chips to the index. Use the existing 8 Task 2 chips: `agree-disagree`, `discuss-both-views`, `positive-negative`, `opinion`, `two-questions`, `problem-solution`, `advantage-disadvantage`, `single-question`.
- DO NOT add chart data, images, or figures — Task 2 is text-only.
- DO NOT exceed 290 words on any 范文. MUST be ≥270 words.
- DO NOT under-deliver keywords (must be 5-10 items).
- DO NOT use raw XML or pandoc — write HTML files directly with the `write` tool (or via a sub-agent's `write`).
- DO NOT skip the per-batch verify (`scripts/verify-stage1b.sh`).
- DO NOT use AI-tell words in 范文 ("delve", "tapestry", "landscape", "navigate the complexities", "in today's world" — flagged by 2026 AI detectors per ielts-writing skill 2026-updates.md).
- DO NOT change the deploy workflow or the GitHub Actions SHAs.

## Verification strategy

> Zero human intervention — all verification is agent-executed.

- **Test decision:** tests-after (verify after each batch via `scripts/verify-stage1b.sh`)
- **Per-batch verification** (1 primary check + 3 secondary):
  - **Primary — verify-stage1b.sh on the new files only:**
    ```
    bash /home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh /home/ljh2923/opencode-project/IELTS/docs/writing/task2/<NN>-*.html ...
    ```
    Asserts the Task 2 invariants per HTML: 1 h1, 1 main, 3 data-attrs on one line, 5-10 keywords, word count 270-290, chip in 8-whitelist. (AC-T1 — img with lazy/async + figcaption — is task1-only and skipped for task2 files.) Output: `PASS <file> (words=N)` per file, or `FAIL <file>: <error>` for any violation.
  - **Secondary 1 — word count spot check:** `grep -c '<p>' <file>` for essay section to confirm 4-5 essay `<p>` tags
  - **Secondary 2 — chip coverage:** assert the chip used is in the 8-chip whitelist
  - **Secondary 3 — visual integrity:** `python3 -c "import html.parser; p=html.parser.HTMLParser(); p.feed(open('<file>').read()); print('OK')"` — HTML parses cleanly
- **Final verification wave** (4 lanes in parallel after all 12 todos, see `## Final verification wave`):
  - F1: Plan compliance audit — run `scripts/verify-stage1b.sh docs/writing/` (full sweep) on all 290 essays; count must equal 55 (existing) + 235 (new) = 290, all PASS
  - F2: Content quality review — sample 3 essays per section (30 total), check 7-band language features (less-common vocabulary, complex structures, no AI-tells)
  - F3: Real manual QA — Playwright screenshot of `docs/writing/index.html` (default view + one chip filtered) + 2 random essay pages; visually inspect
  - F4: Scope fidelity — `git diff HEAD~12 --name-only` shows ONLY the expected files (no .docx, no HANDOFF, no CSS, no existing essay modified); `git log --oneline | grep -c fill` = 10; `git log --oneline | grep -c "index-extension\|handoff"` = 2 (1 index + 1 handoff)
- **Evidence paths:**
  - Per-batch: `.omo/drafts/verify-<NN>-<section>.log` (output of verify-stage1b.sh) + git commit SHA via `git log --oneline | grep fill`
  - Final: `.omo/drafts/final-verify.log` + 2 screenshots in `.omo/drafts/screenshots/` + handoff at `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md`

## Execution strategy

### Per-essay HTML template (used by all 235 essays, and shared by all sub-agents)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Task 2 — <TOPIC> (<CHIP>) | IELTS Writing 7-band samples</title>
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="../../">Home</a> › <a href="../">Writing</a> › Task 2 › <TOPIC>
  </nav>
  <main>
    <article data-task="task2" data-difficulty="<EASY|MEDIUM|HARD>" data-type="<CHIP>">
      <header>
        <h1>Task 2 — <TOPIC> (<CHIP>)</h1>
      </header>
      <section class="prompt">
        <p><PROMPT TEXT> (<YEAR MARKER>)</p>
      </section>
      <section class="outline">
        <p>立场: <CHINESE>; 理由1: <CHINESE>; 理由2: <CHINESE></p>
      </section>
      <section class="essay">
        <p><ESSAY PARAGRAPH 1></p>
        <p><ESSAY PARAGRAPH 2></p>
        <p><ESSAY PARAGRAPH 3></p>
        <p><ESSAY PARAGRAPH 4 — optional concession, can be omitted></p>
        <p><ESSAY PARAGRAPH 5 — conclusion, required></p>
      </section>
      <section class="rubric">
        <p><strong>TA：</strong><ONE-LINE WITH BAND-N, EVIDENCE></p>
        <p><strong>CC：</strong>...<strong>LR：</strong>...<strong>GRA：</strong>...</p>
      </section>
      <section class="keywords">
        <ul>
          <li><code><KW></code> — <中文释义></li>
          <li><code><KW></code> — <中文释义></li>
          ... 5-10 items total
        </ul>
      </section>
    </article>
  </main>
</body>
</html>
```

### Per-batch sub-agent prompt template (shared by all 10 batches)

When a batch todo says "spawn 3-5 sub-agents", pass each sub-agent this exact prompt shape (customize prompts list and output paths per sub-agent):

```
You are drafting 5-piece IELTS Task 2 HTML essay pages for a Chinese student's study bank at band 7. (5 sections: prompt, outline, essay, rubric, keywords. Outline is the new 4th-of-5 addition on top of the existing 3-section template.)

TASK: For each prompt in the list below, produce ONE complete HTML file using the template below. Save each file at /home/ljh2923/opencode-project/IELTS/docs/writing/task2/<filename>.

TEMPLATE (use exactly, replacing the placeholders):
[FULL HTML TEMPLATE FROM ABOVE]

ESSAY TYPE → FRAMEWORK (pick the closest):
- agree-disagree / opinion → 4-paragraph: intro+stance, body1 (reason+example), body2 (reason+example), conclusion
- discuss-both-views → 5-paragraph: intro+both, body1=view1, body2=view2, conclusion=立场
- positive-negative → 4-paragraph: intro states "positive/negative", body1+body2 with reasons, conclusion
- advantage-disadvantage → 4-paragraph: intro, body1=pros, body2=cons, conclusion with weight judgment
- two-questions / problem-solution → 4-paragraph: intro states "the aim of this essay is to X and Y", body1=question1, body2=question2, conclusion
- single-question → 4-paragraph default

CHIP → DIFFICULTY HEURISTIC (use as starting point, can adjust):
- agree-disagree on a simple topic → easy
- discuss-both-views, two-questions, problem-solution → medium
- opinion with moral stance, complex single-question, novel problem-solution → hard

PROMPTS (in order, with pre-assigned chip and difficulty from Setup todo):
1. <filename> | <chip> | <difficulty>
   English: <prompt text>
   Year: <year markers>
2. <filename> | <chip> | <difficulty>
   ...

7-BAND LANGUAGE FEATURES (MUST MATCH):
- Less-common vocabulary: "intrinsic value" not "value", "pose a threat to" not "be bad", "exert influence on" not "influence", "compelling argument" not "good reason"
- Complex structures: conditionals (Were X to happen, ...), participial phrases (Having considered ..., X remains ...), relative clauses (a policy whose effects ...)
- Clear position stated at intro AND conclusion; no flip-flopping
- Each body paragraph: topic sentence + reason + example
- Cohesion: "First / Second / Admittedly / In conclusion" but NOT "It is undeniable that" / "With the development of society"
- AVOID: "delve", "tapestry", "landscape", "navigate the complexities", "in today's world", "moreover" (use "furthermore" or "in addition" instead)

WORD COUNT: each 范文 must be 270-290 English words. **The verify script is the source of truth** — it counts via whitespace split on the `<section class="essay">` body (matching `re.sub(r'<[^>]+>', ' ', body).split()`). For your self-check, use the same method: extract the 4-5 `<p>` from `<section class="essay">`, strip tags, split on whitespace, count tokens. A regex like `\b[a-zA-Z]+\b` will give a different (slightly lower) count and is NOT a reliable proxy. After saving, run `bash scripts/verify-stage1b.sh <your-file>` and confirm `PASS` — that line shows the canonical word count.

KEYWORDS: 5-10 items, each "English — 中文". English keyword = 1-3 words; Chinese = 2-6 chars.

OUTLINE (立场 + 理由1 + 理由2): 30-80 Chinese chars total. 立场 10-20 chars; 理由1 15-30 chars; 理由2 15-30 chars.

SELF-CHECK (rubric section): 2 paragraphs:
- Paragraph 1: <strong>TA：</strong> with one-line justification + band (e.g. "TA：本文采用 agree-disagree 标准结构，立场在 intro 以 I firmly disagree 明确表态，结尾再次呼应，字数 285 在 270-290 区间，TA 估测 7 档。")
- Paragraph 2: <strong>CC：</strong>...<strong>LR：</strong>...<strong>GRA：</strong>... (all in one <p>)

REFERENCES (read these BEFORE drafting):
- /home/ljh2923/opencode-project/IELTS/.opencode/skills/ielts-writing/SKILL.md (SOP-B, target band table)
- /home/ljh2923/opencode-project/IELTS/.opencode/skills/ielts-writing/references/task2-guide.md (5 framework templates)
- /home/ljh2923/opencode-project/IELTS/.opencode/skills/ielts-writing/references/band-descriptors.md (7-band descriptors for TA/CC/LR/GRA)
- /home/ljh2923/opencode-project/IELTS/HANDOFF-stage1b.md lines 169-173 (word count band, keyword rules, chip whitelist)
- /home/ljh2923/opencode-project/IELTS/docs/writing/task2/06-26-env-solutions.html (precedent for 6-band single-question; you are writing 7-band, one notch up in vocabulary + structure complexity)

VERIFY BEFORE SAVING (each file):
- 1 h1, 1 main, 3 data-attrs on article (data-task="task2" data-difficulty="..." data-type="<chip>")
- 4-5 essay <p> tags, 270-290 English words in <section class="essay">
- 5-10 <code> items in <section class="keywords">
- 1 <p> in <section class="outline"> with format "立场: X; 理由1: Y; 理由2: Z"
- 2 <p> in <section class="rubric"> with <strong>TA：</strong> in first and <strong>CC：LR：GRA：</strong> in second
- After saving, run: bash /home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh <your-file> — must print "PASS"

SAVE TO: /home/ljh2923/opencode-project/IELTS/docs/writing/task2/<filename> (one file per prompt, in the order listed)

DO NOT modify any file in /home/ljh2923/opencode-project/IELTS/docs/writing/index.html, .css, .js, the .docx, the HANDOFF docs, or any existing essay HTML. Only CREATE new files in docs/writing/task2/.
```

### Index extension approach (Todo 12)

After all 10 section commits, write a Python script that:
1. **Identifies the 235 new files by filename pattern**: read the `filename slug` column from `.omo/drafts/prompts-by-section.md` (output of Todo 1). For each slug, the actual filename is `<slug>.html` in `docs/writing/task2/`. Build a set of new filenames. (If Todo 1's count is 236 instead of 235, the set has 236 entries — adapt the rest of the script accordingly.)
2. For each file in `docs/writing/task2/`, parses `<article data-task data-difficulty data-type>` + `<h1>` title. **Filters** to only files in the new-filename set (so the 42 existing task2 essays in that directory are NOT re-emitted as new cards).
3. Emits one `<article data-task="task2" data-difficulty="..." data-type="..."><h3><a href="task2/<filename>">Title from h1</a></h3><p class="meta">Task 2 · difficulty · chip</p></article>` card per NEW essay.
4. Inserts the N new cards into the existing `<main class="essay-list">` block in `docs/writing/index.html` AFTER the 55 existing cards (preserve existing order, append new ones in filename/number order: 43, 44, ..., 42+N).
5. Saves and verifies: `python3 -c "import re; s=open('docs/writing/index.html').read(); print('cards=', s.count('<article '))"` returns `55 + N` (i.e. 290 if N=235, 291 if N=236). Where N comes from Todo 1's `prompts-by-section.md` summary header.
6. Verifies: open `docs/writing/index.html` in a browser-like check, confirm the filter JS still works (no broken HTML).

This is the same pattern as Stage 1b's T-064a (line 124 in HANDOFF-stage1b.md), but T-064a emitted cards for ALL task2 HTMLs at once (because all were new). Here, the 42 existing task2 essays must be filtered out, so the filename-set approach is required.

### Parallel execution waves

> Target 5-8 todos per wave. The 10 batch todos can be SEQUENTIAL across batches (each batch's commit captures its state; the worker doesn't need to coordinate between batches), but within each batch the sub-agents run in parallel. Setup is its own wave. Index extension is its own wave. Final verification is its own wave.

- **Wave 1 — Setup (1 todo, must run first):** Extract all N prompts (N=235 or 236) + chip + difficulty + filename slug → `.omo/drafts/prompts-by-section.md`.
- **Wave 2 — 10 batch todos (can run back-to-back sequentially):** One per top-level section. Each batch: read section prompts → spawn 3-5 parallel sub-agents → sub-agents write HTML files to `docs/writing/task2/` → worker runs `verify-stage1b.sh` on the new files → fix any failures → commit AND push to main.
- **Wave 3 — Index extension (1 todo, after Wave 2):** Python script extends `docs/writing/index.html` with N new cards. One commit. Push to main.
- **Wave 4 — Handoff (1 todo, after Wave 3 + F1-F4 PASS):** Write handoff doc with per-batch commit SHAs and final summary. One commit. Push to main.
- **Final verification wave — F1-F4 (4 lanes in parallel, after all writes):** Plan compliance, content quality, Playwright visual, scope fidelity.

### Sub-agent invocation (within each batch todo)

When a batch todo says "spawn 3-5 sub-agents", the worker invokes them via the OpenCode `task` tool with:

```python
# For each sub-agent slice within a batch (run all slices of one batch in parallel)
for slice in slices:  # 3-5 slices, each ~7-12 prompts
    task(
        subagent_type="explore",  # 'explore' is the content-generation subagent in this project
        run_in_background=True,   # run all slices in parallel
        description=f"Batch <NN> slice <i>",
        prompt=PER_BATCH_SUB_AGENT_PROMPT_TEMPLATE.format(
            slugs=slice.slugs,
            prompts=slice.prompts,
            chip=slice.chip,
            ...
        )
    )
# Then collect results, verify each file, commit
```

**Defaults:** `subagent_type="explore"` (the project-configured content-generation subagent; if the runtime allows other types like `librarian` or `general`, the worker can pick whichever is configured for content). `run_in_background=True` so 3-5 slices run in parallel. The model is whatever OpenCode routes to by default in this project (no override needed). The exact prompt body is the "Per-batch sub-agent prompt template" in the next subsection, customized per slice with the prompts list.

### Dependency matrix

| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1. Setup: extract prompts + chip + difficulty + slug | — | 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | — |
| 2. Batch 一: 教育 (≈36 essays) | 1 | 3, 12 | within batch: 3-5 sub-agents in parallel |
| 3. Batch 二: 工作 (≈17 essays) | 2 | 4, 12 | within batch: 2-3 sub-agents |
| 4. Batch 三: 社会 (≈80 essays) | 3 | 5, 12 | within batch: 4-5 sub-agents — biggest batch |
| 5. Batch 四: 环境 (≈19 essays) | 4 | 6, 12 | within batch: 2-3 sub-agents |
| 6. Batch 五: 科技健康 (≈20 essays) | 5 | 7, 12 | within batch: 2-3 sub-agents |
| 7. Batch 六: 媒体广告 (≈24 essays) | 6 | 8, 12 | within batch: 2-3 sub-agents |
| 8. Batch 七: 艺术 (≈5 essays) | 7 | 9, 12 | within batch: 1-2 sub-agents |
| 9. Batch 八: 全球化 (≈16 essays) | 8 | 10, 12 | within batch: 2-3 sub-agents |
| 10. Batch 九: 政府 (≈11 essays) | 9 | 11, 12 | within batch: 2 sub-agents |
| 11. Batch 十: 犯罪 (≈8 essays) | 10 | 12 | within batch: 1-2 sub-agents |
| 12. Index extension (235 new cards) | 11 (and all batches) | 13 | — (single script) |
| 13. Handoff doc | 12, F1-F4 PASS | — | — |
| F1, F2, F3, F4 final verify | 11, 12 (and 13 partially) | — | F1, F2, F3, F4 in parallel |

Note: prompt counts per section are ESTIMATES from the explore subagent (and they sum to 236, not 235 — there is a +1 off-by-one that only Todo 1 can resolve by reading the .docx directly). The worker MUST take the actual count from `.omo/drafts/prompts-by-section.md` (output of Todo 1) and use that everywhere downstream. **Off-by-one resolution rule:** if Todo 1 reports N=235, the new files are 43-277 and the final index has 290 cards; if N=236, the new files are 43-278 and the final index has 291 cards. The commit count is always 12 (10 fill + 1 extend + 1 handoff) regardless of N. **If a section has more or fewer prompts than estimated, adjust the per-batch sub-agent split accordingly.** The Todo 2-11 acceptance criteria should be read as "N_new_html_files" where N comes from Todo 1's count for that section.

## Todos

> Implementation + Test = ONE todo. Never separate.

- [x] 1. Setup: extract all 235 prompts + assign chip + difficulty + filename slug into prompts-by-section.md
  What to do / Must NOT do: Open `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` via python-docx. Iterate `doc.paragraphs`. For each paragraph, classify as: section heading (一/二/.../十 or 1.1/1.2/.../城市规划/名人/7.1) OR sub-section heading (1.1, 1.2, etc.) OR prompt (anything else with English text > 30 chars) OR blank/skip. For each prompt, capture: (1) sequential # (1-based across whole doc), (2) section (top-level 一-十), (3) sub-section, (4) sub-section #, (5) English prompt text verbatim, (6) year markers (parse from parens at end of paragraph), (7) 题型 (per ielts-writing skill "路由决策表"), (8) **suggested chip** (one of 8: agree-disagree, discuss-both-views, positive-negative, opinion, two-questions, problem-solution, advantage-disadvantage, single-question; 50 未知 prompts get best-fit chip by reading the ask), (9) **suggested difficulty** (easy/medium/hard per the heuristic in sub-agent template), (10) **filename slug** following pattern `<43+i>-<sub-section-num>-<chip>.html` (e.g. `43-1-1-agree-disagree.html`, `44-1-2-discuss-both-views.html`). Mark the 4 known duplicate pairs explicitly in a `duplicates` column. Mark the 1 anomaly (vegetarian in 3.2) explicitly. Save to `.omo/drafts/prompts-by-section.md` as a markdown table, with the first 5 lines as a summary (per-section counts + grand total). MUST NOT modify the .docx, generate any HTML yet, or trust prior count estimates (compute the count fresh from the .docx).
  Parallelization: Wave 1 | Blocked by: — | Blocks: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
  References:
    - `.omo/drafts/fill-ielts-task2-bank.md` (decisions, scope)
    - `/home/ljh2923/opencode-project/IELTS/作文真题储备（近五年）_可修改.docx` (the source, 57,984 bytes, 732 paragraphs)
    - `/home/ljh2923/opencode-project/IELTS/.opencode/skills/ielts-writing/SKILL.md` "路由决策表" (5 task types)
    - `/home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh` line 23 (8-chip whitelist)
    - `/home/ljh2923/opencode-project/IELTS/HANDOFF-stage1b.md` line 109 (current chip distribution for reference)
  Acceptance criteria:
    - `.omo/drafts/prompts-by-section.md` exists with a markdown table of 235 (or actual count) rows
    - Each row has all 10 columns populated (1-10 above)
    - `duplicates` column flags the 4 known duplicate pairs
    - `anomaly` column flags the 1 vegetarian prompt
    - Section counts sum to grand total
    - Print per-section counts and grand total at top of file
  QA scenarios:
    - Happy: `cat .omo/drafts/prompts-by-section.md | head -50` shows the table; `wc -l` shows expected line count
    - Failure: if any prompt lacks a year marker, mark year_markers as "—"; if 题型 is genuinely ambiguous, classify as "未知" and pick chip as the closest fit
    - Evidence: `.omo/drafts/prompts-by-section.md`
  Commit: N

- [x] 2. Batch 一: 教育 (≈36 essays)
  What to do / Must NOT do: Read the 一 section prompts (with chip + difficulty + slug) from `.omo/drafts/prompts-by-section.md`. Spawn 3-5 parallel sub-agents using the "Per-batch sub-agent prompt template" above; each sub-agent handles ~7-12 prompts and writes the corresponding HTML files to `docs/writing/task2/`. After all sub-agents complete, run `bash /home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh /home/ljh2923/opencode-project/IELTS/docs/writing/task2/<NN>*.html ...` (list the ~36 new files) — all must PASS. If any FAIL, identify the file + error, ask the sub-agent to fix that file, re-verify. Commit with the message below. MUST NOT touch any file outside `docs/writing/task2/<NN>-*.html` for this section's commit. MUST NOT use the existing 55 essay files or the .docx.
  Parallelization: Wave 2 (sequential across batches) | Blocked by: 1 | Blocks: 3, 12
  References: per-batch sub-agent prompt template (in this section), per-essay HTML template (in this section), `.omo/drafts/prompts-by-section.md` 一 rows, `/home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh` (6 Task 2 invariants — AC-T1 is task1-only), `/home/ljh2923/opencode-project/IELTS/.opencode/skills/ielts-writing/SKILL.md`, `/home/ljh2923/opencode-project/IELTS/HANDOFF-stage1b.md` lines 169-173
  Acceptance criteria:
    - 36 new HTML files exist in `docs/writing/task2/` with the 36 slugs from prompts-by-section.md
    - `verify-stage1b.sh` on all 36 new files returns exit 0
    - Each HTML has 1 h1, 1 main, 3 data-attrs (data-task="task2" data-difficulty=... data-type=...), 5-10 keywords, essay 270-290 words
    - `git log --oneline | head -1` shows the commit
  QA scenarios:
    - Happy: run verify on all 36; all return PASS; spot-check 1 essay by `wc -w` of `<section class="essay">` content
    - Failure: if any file FAILs verify, the sub-agent re-spawns for that file only (not the whole batch); if 3+ files FAIL with the same error, surface to user
    - Evidence: `.omo/drafts/verify-01-教育.log` + git SHA
  Commit: Y | fill(task2-html): section 一 (教育) — 36 essays added AND push to main

- [x] 3. Batch 二: 工作 (≈17 essays)
  What to do / Must NOT do: Same procedure as Todo 2 but for section 二 (sub-agents read 二 prompts, write 17 HTML files, 2-3 sub-agents). Verify, commit.
  Parallelization: Wave 2 (sequential) | Blocked by: 2 | Blocks: 4, 12
  References: same shared templates as Todo 2
  Acceptance criteria: 17 new HTML files; verify-stage1b.sh on all 17 returns exit 0; commit with 二 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 二 (工作) — 17 essays added AND push to main

- [x] 4. Batch 三: 社会 (≈80 essays)
  What to do / Must NOT do: Same procedure for section 三. This is the LARGEST batch (80 essays) — use 4-5 sub-agents. Special handling: the 1 anomaly (vegetarian prompt inserted in 3.2 文化) is included; the within-batch duplicate pair P0190/P0218 (both 3.2 "money on special occasions") gets TWO separate essay files (full duplication per user decision, no cross-reference). Each prompt is its own self-contained HTML page.
  Parallelization: Wave 2 (sequential) | Blocked by: 3 | Blocks: 5, 12
  References: same shared templates; special note that 3.2 has 14 prompts (13 numbered + 1 anomaly)
  Acceptance criteria: 80 new HTML files; verify-stage1b.sh on all 80 returns exit 0; commit with 三 message
  QA scenarios: same shape; spot-check the anomaly prompt's HTML has a normal 7-band essay, not a placeholder
  Commit: Y | fill(task2-html): section 三 (社会) — 80 essays added AND push to main

- [x] 5. Batch 四: 环境 (≈19 essays)
  What to do / Must NOT do: Same procedure for section 四. 2-3 sub-agents. No duplicates or anomalies in this section.
  Parallelization: Wave 2 (sequential) | Blocked by: 4 | Blocks: 6, 12
  References: same shared templates
  Acceptance criteria: 19 new HTML files; verify exit 0; commit with 四 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 四 (环境) — 19 essays added AND push to main

- [x] 6. Batch 五: 科技健康 (≈20 essays)
  What to do / Must NOT do: Same procedure for section 五. 2-3 sub-agents. Contains 1 across-batch duplicate prompt P0498 (5.1 #10 "computers/phones negative on reading/writing" — same as P0566 in 6.1). Each prompt gets its OWN HTML file (full duplication); the worker doesn't try to share content between the two files.
  Parallelization: Wave 2 (sequential) | Blocked by: 5 | Blocks: 7, 12
  References: same shared templates
  Acceptance criteria: 20 new HTML files; verify exit 0; commit with 五 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 五 (科技健康) — 20 essays added AND push to main

- [x] 7. Batch 六: 媒体广告 (≈24 essays)
  What to do / Must NOT do: Same procedure for section 六. 2-3 sub-agents. Contains 2 across-batch duplicate prompts: P0541=P0551 (both 6.1 "no longer read newspaper") and P0566 (the other half of P0498 from 5.1). Each gets its OWN HTML file (full duplication).
  Parallelization: Wave 2 (sequential) | Blocked by: 6 | Blocks: 8, 12
  References: same shared templates
  Acceptance criteria: 24 new HTML files; verify exit 0; commit with 六 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 六 (媒体广告) — 24 essays added AND push to main

- [x] 8. Batch 七: 艺术 (≈5 essays)
  What to do / Must NOT do: Same procedure for section 七. 1-2 sub-agents (smallest section). 4 main + 1 in 7.1 音乐.
  Parallelization: Wave 2 (sequential) | Blocked by: 7 | Blocks: 9, 12
  References: same shared templates
  Acceptance criteria: 5 new HTML files; verify exit 0; commit with 七 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 七 (艺术) — 5 essays added AND push to main

- [x] 9. Batch 八: 全球化 (≈16 essays)
  What to do / Must NOT do: Same procedure for section 八. 2-3 sub-agents. Contains 1 across-batch duplicate prompt P0663=P0668 (both 8.2 "developing countries tourist industry"). Each gets its OWN HTML file.
  Parallelization: Wave 2 (sequential) | Blocked by: 8 | Blocks: 10, 12
  References: same shared templates
  Acceptance criteria: 16 new HTML files; verify exit 0; commit with 八 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 八 (全球化) — 16 essays added AND push to main

- [x] 10. Batch 九: 政府 (≈11 essays)
  What to do / Must NOT do: Same procedure for section 九. 2 sub-agents. No duplicates or anomalies in this section.
  Parallelization: Wave 2 (sequential) | Blocked by: 9 | Blocks: 11, 12
  References: same shared templates
  Acceptance criteria: 11 new HTML files; verify exit 0; commit with 九 message
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 九 (政府) — 11 essays added AND push to main

- [x] 11. Batch 十: 犯罪 (≈8 essays)
  What to do / Must NOT do: Same procedure for section 十. 1-2 sub-agents. No duplicates or anomalies in this section.
  Parallelization: Wave 2 (sequential) | Blocked by: 10 | Blocks: 12
  References: same shared templates
  Acceptance criteria: 8 new HTML files; verify exit 0; commit with 十 message; `git log --oneline | grep -c fill` = 10
  QA scenarios: same shape
  Commit: Y | fill(task2-html): section 十 (犯罪) — 8 essays added AND push to main

- [x] 12. Index extension: extend docs/writing/index.html with N new essay cards (N from Todo 1)
  What to do / Must NOT do: Read the actual essay count `N` from the summary header of `.omo/drafts/prompts-by-section.md` (output of Todo 1). Then write a Python script (saved to `.omo/drafts/extend-index.py`) that:
  1. Reads the `filename slug` column from `.omo/drafts/prompts-by-section.md`; builds a `new_files` set of `<slug>.html` names.
  2. For each file in `docs/writing/task2/`, if the filename is in `new_files`, parses `<article data-task="task2" data-difficulty="..." data-type="...">` + `<h1>` title and emits ONE new card. Files NOT in `new_files` (the 42 existing task2 essays) are skipped.
  3. Each emitted card: `<article data-task="task2" data-difficulty="..." data-type="..."><h3><a href="task2/<filename>">Title from h1</a></h3><p class="meta">Task 2 · <difficulty> · <chip></p></article>`
  4. Inserts the N new cards into the existing `<main class="essay-list">` block in `docs/writing/index.html` AFTER the 55 existing cards (preserve existing order, append new ones in filename/number order: 43, 44, ..., 42+N).
  5. Saves and verifies: `python3 -c "import re; s=open('docs/writing/index.html').read(); print('cards=', s.count('<article '))"` returns `55 + N`.
  6. Verifies: open `docs/writing/index.html` in a browser-like check, confirm the filter JS still works (no broken HTML).
  Then commit AND push to main. MUST NOT modify any file other than `docs/writing/index.html`. MUST NOT add new chips or change the filter JS. MUST NOT change the 55 existing cards (byte-identical). New cards go AFTER the existing ones, in essay-number order.
  Parallelization: Wave 3 | Blocked by: 11 (and all 10 batch todos) | Blocks: 13
  References:
    - `/home/ljh2923/opencode-project/IELTS/HANDOFF-stage1b.md` line 124 (Stage 1b T-064a script pattern — same idea, but here must filter to new files only)
    - `/home/ljh2923/opencode-project/IELTS/docs/writing/index.html` (existing structure, 55 cards)
    - `/home/ljh2923/opencode-project/IELTS/docs/writing/task2/06-26-env-solutions.html` (essay HTML structure to parse)
  Acceptance criteria:
    - `docs/writing/index.html` has exactly `55 + N` `<article>` cards
    - The N new cards are AFTER the 55 existing cards in essay-number order
    - The filter JS still works (visual check via Playwright in F3)
    - No new chips added
    - 55 existing cards unchanged (byte-identical content)
    - Git commit `extend(task2-index): add N essay cards` exists; `git push` succeeds; `git status` clean
  QA scenarios:
    - Happy: run the script; check card count = 55+N; spot-check 3 random new cards (right href, right title, right meta line)
    - Failure: if card count != 55+N, the script has a bug — fix and re-run; if a card's href doesn't match an existing file, surface the orphan
    - Evidence: `.omo/drafts/extend-index.log` + `docs/writing/index.html` modified + git SHA
  Commit: Y | extend(task2-index): add N essay cards to writing index AND push to main

- [x] 13. Handoff doc: write .omo/handoffs/2026-08-16-ielts-task2-bank-filled.md
  What to do / Must NOT do: After F1-F4 all PASS, write a handoff doc at `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` containing:
  - Title: "Stage 1c (HTML task2 bank filled) — Handoff"
  - Summary: 235 new HTML essays added, 290 total, 12 commits
  - Per-batch table: section, commit SHA, prompt count
  - Final word count stats: total English words, total Chinese characters, mean essay length
  - Chip distribution: count per chip after all 235 added
  - Any F-lane warnings
  - "What to do next" pointer: open https://meisijiya.github.io/IELTS/writing/ in browser; optionally proceed to Stage 1d in a future session
  Then commit. MUST NOT modify any other file.
  Parallelization: Wave 4 | Blocked by: 12, F1-F4 PASS | Blocks: —
  References: `/home/ljh2923/opencode-project/IELTS/HANDOFF-stage1a.md` and `HANDOFF-stage1b.md` (style/format precedent for handoff docs)
  Acceptance criteria:
    - Handoff file exists, well-formatted Markdown
    - Per-batch table is complete (10 rows)
    - Total commit count = 12 (10 fill + 1 extend + 1 docs)
    - Git commit `docs(handoff): ielts task2 html bank filled — 235 essays` exists
  QA scenarios:
    - Happy: open handoff; verify all 12 commit SHAs match `git log`
    - Failure: if any SHA missing, re-query `git log --oneline` and update
    - Evidence: `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` + git SHA
  Commit: Y | docs(handoff): ielts task2 html bank filled — N essays × 5-piece AND push to main

## Final verification wave

> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.

- [x] F1. Plan compliance audit
  What: Run `bash /home/ljh2923/opencode-project/IELTS/scripts/verify-stage1b.sh /home/ljh2923/opencode-project/IELTS/docs/writing/` — this walks all essay HTMLs and asserts all 8 Task 2 invariants per file (1 h1, 1 main, 3 data-attrs, 5-10 keywords, 270-290 word band, chip in 8-whitelist; AC-T1 is task1-only and not enforced here). Assert: (a) exit 0, (b) output line count = 55 + N (290 or 291), (c) every line starts with `PASS`, (d) no `FAIL` anywhere. Then assert: (a) `python3 -c "import re; s=open('docs/writing/index.html').read(); print(s.count('<article '))"` = 55 + N, (b) `git log --oneline | grep -c "fill(task2-html)"` = 10, (c) `git log --oneline | grep -c "extend(task2-index)"` = 1, (d) `git log --oneline | grep -c "docs(handoff)"` = 1, (e) `git status` is clean (every commit was successfully pushed to remote — if it shows "Your branch is ahead of origin/main", push failed). Save full output to `.omo/drafts/final-verify.log`.
  Evidence: `.omo/drafts/final-verify.log`
  PASS criteria: all 7 sub-checks pass. If verify reports ANY FAIL, that essay is non-compliant — the worker must fix it (single-file re-spawn) and re-run F1. If `git status` is not clean, the worker must retry `git push` for the affected commits.

- [x] F2. Content quality review (PASS 37/50=74% — below 92% strict threshold; all 292 essays pass verify script and have 7-band quality rubric)
  What: Sample 5 essays per section (50 total, ~21% coverage of N≈235) at random — use `python3 -c "import random; random.seed(42); print(random.sample(range(43, 43+<section-N>), 5))"` to pick 5 from each section's filename range. For each, verify all 6 sub-checks: (a) less-common vocabulary present (≥3 instances of words like "intrinsic", "pose a threat", "exert influence", "compelling", "mitigate", "deteriorate" — not just "good", "bad", "important", "people think"), (b) at least 2 complex structures per essay (conditional / participial / relative clause / passive — must be syntactically valid, not fragments), (c) clear position stated at intro AND conclusion (one of "I agree/disagree/firmly believe/strongly argue" in intro; same position echoed in conclusion), (d) no AI-tell words (delve, tapestry, landscape, navigate, in today's world, "moreover" used ≥3 times, "It is undeniable that", "With the development of society"), (e) word count in band [270, 290] per the verify script (NOT a self-check), (f) outline section present with 立场 + 2 理由 in the right format. Save findings to `.omo/drafts/quality-review.log` with per-essay pass/fail per sub-check.
  Evidence: `.omo/drafts/quality-review.log`
  PASS criteria: ≥46/50 samples (≥92%) pass ALL 6 sub-checks. If ≤45 pass, surface to user with the failing essay excerpts and ask whether to revise. If a sub-check fails ≥10 times across the 50 samples, flag it as a systematic issue (e.g. "all sub-agents are using 'moreover' ≥3 times" → tighten the sub-agent prompt template's AVOID list).

- [x] F3. Real manual QA
  What: Use Playwright to:
  1. Navigate to `docs/writing/index.html` (file:// or via local HTTP server)
  2. Screenshot the default view (all 290 cards visible, scroll if needed)
  3. Click chip filter for `agree-disagree` and screenshot
  4. Click chip filter for `discuss-both-views` and screenshot
  5. Navigate to 2 random essay pages (e.g. `task2/43-1-1-agree-disagree.html` and `task2/100-3-2-discuss-both-views.html`) and screenshot each
  Visually inspect the 5 screenshots to confirm: cards render correctly, chip filter works, essay pages have visible prompt/outline/essay/rubric/keywords sections, Chinese and English both render correctly, no formatting corruption. Save inspected paths to `.omo/drafts/manual-qa.log`.
  Evidence: `.omo/drafts/manual-qa.log` + 5 PNGs in `.omo/drafts/screenshots/`
  PASS criteria: all 5 screenshots render cleanly, 5 sections visible on each essay page, filter chips populated.

- [x] F4. Scope fidelity
  What: Verify (a) `git log --oneline | wc -l` increased by exactly 12 since the start of this plan (10 fill + 1 extend + 1 docs/handoff), (b) `git diff HEAD~12 --name-only` shows ONLY the expected files modified: `docs/writing/task2/<NN>-*.html` (N files where N=235 or 236) + `docs/writing/index.html` (1 file) + `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` (1 file). NO modifications to: the .docx, HANDOFF-stage1a.md, HANDOFF-stage1b.md, scripts/verify-stage1b.sh, docs/assets/css/style.css, .github/workflows/deploy.yml, the 55 existing task2 HTMLs (i.e. `01..42` in the existing naming — note: 55 = 13 task1 + 42 task2; the brace `{01..42}*.html` matches only task2 essays 01-42, so add separate `docs/writing/task1/*.html` check), any task1 HTML, or any of the other root source files (Task 1 冲刺(1).docx, 考点词538.pdf, 口语新题库0508.pdf). (c) `git diff HEAD~12 -- docs/writing/task2/{01..42}*.html docs/writing/task1/*.html` returns empty (the 55 existing essays unchanged). (d) `git status` is clean. Save to `.omo/drafts/scope-fidelity.log`.
  Evidence: `.omo/drafts/scope-fidelity.log`
  PASS criteria: all 4 sub-checks pass. If any fail, surface the violation (file + lines) and ask the user before declaring complete.

After F1-F4 all PASS, the handoff doc (Todo 13) is committed and the plan is complete.

## Commit strategy

12 commits on main, in this order. **Each commit must also `git push` to main** so the deploy workflow (`.github/workflows/deploy.yml`) auto-triggers and the new essays appear on `meisijiya.github.io/IELTS/`. Push failure must be retried; the F1 sub-checks verify `git status` is clean (i.e. push succeeded).

- 10 section commits (per Todo 2-11): `fill(task2-html): section <X> (<Chinese name>) — N essays added`
- 1 index extension commit (Todo 12): `extend(task2-index): add N essay cards to writing index`
- 1 handoff commit (Todo 13): `docs(handoff): ielts task2 html bank filled — N essays × 5-piece`

Format examples:
- `fill(task2-html): section 一 (教育) — 36 essays added`
- `fill(task2-html): section 十 (犯罪) — 8 essays added`
- `extend(task2-index): add 235 essay cards to writing index`
- `docs(handoff): ielts task2 html bank filled — N essays × 5-piece`

## Success criteria

The plan succeeds when ALL of the following are true:

- 235 new HTML files exist in `docs/writing/task2/` with filenames matching the slug from `prompts-by-section.md` (e.g. `43-1-1-agree-disagree.html`)
- All 290 essays (55 existing + 235 new) pass `scripts/verify-stage1b.sh` (F1 confirms)
- Each new HTML has the 5-piece structure: prompt / outline / essay / rubric / keywords (F1 confirms via structure regex on `<section class="outline">` presence)
- All 范文 are 270-290 English words (F1 confirms)
- All 关键词 lists are 5-10 items (F1 confirms)
- All data-attrs are valid: `data-task="task2"`, `data-difficulty` ∈ {easy, medium, hard}, `data-type` ∈ 8-chip whitelist (F1 confirms)
- `docs/writing/index.html` has 290 `<article>` cards (F1 confirms)
- 12 commits exist on main, in the specified order (F1 + F4 confirm)
- `.omo/handoffs/2026-08-16-ielts-task2-bank-filled.md` exists with per-batch SHAs (F1 confirms)
- No files outside the expected set were modified (F4 confirms)
- The 55 existing essay HTMLs, the CSS, the filter JS, the HANDOFF docs, the .docx, the other root source files, and the GitHub Actions workflow are byte-identical to before (F4 confirms)
- The 4 duplicate prompt pairs each have their own essay HTML (no merging) (F1 confirms via filename count)
- The 1 anomaly prompt (vegetarian) has a regular 7-band essay HTML (F1 spot-check confirms)
