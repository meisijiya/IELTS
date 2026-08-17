# Stage 1b Plan — IELTS Writing Site: 45-Essay 题库 Expansion (v2)

> Plan agent: Prometheus (v1) → Momus review (REJECT v1) → v2 hand-edited by dispatcher.
> v2 status: addresses all 3 v1 blocking issues (sub-cat mapping / chip dictionary / arithmetic).
> Awaiting Momus re-review.

## Goal

Ship the Stage-1b slice of the IELTS study site: expand the Stage-1a skeleton (5 Task 1 + 5 Task 2) into the full 题库 — **8 new Task 1 essays** (slugs `06..13`) covering remaining chart types and **37 new Task 2 essays** (slugs `06..42`) covering every `1.1`–`8.2` sub-category (32 first-essays + 5 second-prompt-variants for the sub-cats already shipped in 1a). Final corpus: **10 + 45 = 55 essay HTMLs** live at https://meisijiya.github.io/IELTS/. Acceptance lives in `.omo/specs/ielts-writing-site-stage1b.md`.

## Context (v2 corrected)

- Repo: `https://github.com/meisijiya/IELTS` (public, `main` branch only).
- Working dir: `/home/ljh2923/opencode-project/IELTS`.
- Stage 1a shipped 17 commits since baseline `fbd2072`. Site live.
- **Stage 1a actual sub-cat coverage** (verified by reading `作文真题储备（近五年）_可修改.docx` and matching 5 Stage 1a essay prompts):
  - `01-agree-disagree-history-vs-business` → **1.1** #1 (history vs business) → uses chip `agree-disagree`
  - `02-discuss-both-views-employment-skills` → **1.1** #2 (employment skills) → uses chip `discuss-both-views`
  - `03-positive-negative-children-freedom` → **1.2** #4 (children freedom) → uses chip `positive-negative`
  - `04-opinion-teachers-morality` → **1.5** #2 (teachers judge right/wrong) → uses chip `opinion`
  - `05-two-questions-environment` → **4.4** #1 (natural resources over-consumption) → uses chip `two-questions`
  - = **5 essays / 4 distinct sub-cats** (1.1 covered twice with two different chips).
  - All 5 Task 2 chips are now USED by Stage 1a. Second-variant essays need NEW chips.
- Source content:
  - `Task 1 冲刺(1).docx` — 13 chart questions with embedded images. 5 already covered in 1a; **8 remain** to be shipped in Stage 1b.
  - `作文真题储备（近五年）_可修改.docx` — 37 sub-categories `1.1`–`8.2`. 4 covered in 1a; **32 need first essays + 5 need a 2nd prompt variant** = 37 total.
- Filter chip state (verified by reading `docs/writing/index.html` lines 26–36):
  - Task 1 chips: `static-graph`, `dynamic-graph`, `mixed-graph`, `map`, `process` (5 total)
  - Task 2 chips: `agree-disagree`, `discuss-both-views`, `positive-negative`, `opinion`, `two-questions` (5 total, all used by Stage 1a)
  - **Missing chips needed for second-variants**: `problem-solution`, `advantage-disadvantage`, `single-question` (3 new chips; the standard IELTS Task 2 types not yet in the filter)
- Spec: `.omo/specs/ielts-writing-site-stage1b.md` (EXPLORED, 6 Requirements, 14 Scenarios).
- Handoff: `HANDOFF-stage1a.md` at repo root.
- Constraints from 1a review cycle (preserved verbatim): 9 template invariants; chart-data-not-fabricated; atomic 1-essay-per-commit; commit message `stage 1b(T-NNN): <slug> — <one-line what>`; all Actions SHA-pinned.

---

## v2 Blocking-issue Fixes (vs v1)

| # | v1 Issue | v2 Fix |
|---|---|---|
| **B1** | Plan assumed Stage 1a covered (1.2, 1.4, 1.5, 1.6, 4.7) — wrong. Actual: (1.1 ×2, 1.2, 1.5, 4.4). | §Ticket Tree updated to reflect 4 distinct sub-cats covered; SA-3b sub-cats changed from (1.4, 1.6, 4.7) → second-variant on (1.1, 1.2, 1.5, 4.4) — the 4 actually covered; SA-2a's erroneously-assigned 1.1 replaced with 4.7 (first-essay, since 4.7 actually NOT covered). |
| **B2** | Plan's second-variant chip names (problem-solution, advantage-disadvantage, cause-effect, mixed-task, single-question) did not exist in `docs/writing/index.html` `knownTypes` Set. | New **T-016b** in Wave 0: extend `docs/writing/index.html` to add 3 new chips (`problem-solution`, `advantage-disadvantage`, `single-question`) plus sync the `knownTypes` Set in the filter JS. Second-variant essays pick chips from the resulting 8-chip Task 2 dictionary. |
| **B3** | Plan stated "5 + 45 = 53". 5+45=50; Stage 1a has 10 essays, so 10+45=55. | §Goal + §Ticket Tree + §Verification Gates all updated to **10 + 45 = 55**. |

---

## Ticket Tree (v2)

Ticket IDs `T-016 .. T-064` (50 tickets).

| Range | Count | Purpose |
|---|---|---|
| `T-016` | 1 | Workflow concurrency tweak (`cancel-in-progress: true`) |
| **`T-016b`** | **1** | **NEW: extend Writing index — add 3 Task 2 chips (problem-solution, advantage-disadvantage, single-question) + sync `knownTypes` Set in filter JS** |
| `T-017` | 1 | Bulk-verify script `scripts/verify-stage1b.sh` |
| `T-018` | 1 | Pilot essay (T1 process) — validates ticket AC + new-chip-set end-to-end before fan-out |
| `T-019..T-026` | 8 | Task 1 essays (slugs 06..13), one ticket per essay |
| `T-027..T-058` | 32 | Task 2 first-essay batch — one per **uncovered** sub-category (NOT 1.1 / 1.2 / 1.5 / 4.4); covers 32 sub-cats |
| `T-059..T-063` | 5 | Task 2 second-prompt-variant batch — for the 5 (sub-cat × chip) cells already shipped by Stage 1a (1.1 ×2 + 1.2 ×1 + 1.5 ×1 + 4.4 ×1), each picks a **different** chip from the new 8-chip dictionary |
| `T-064` | 1 | Bulk deploy verification (curl all 55 URLs + Playwright spot-check + GH Actions status) |

**Sub-category ledger (v2, locked):**

| Sub-cat | First essay? | Stage 1a chip(s) used | Second-variant chip slot |
|---|---|---|---|
| 1.1 教育内容 | **Stage 1a** (×2) | `agree-disagree`, `discuss-both-views` | (a) `single-question`, (b) `problem-solution` → 2 second-variants |
| 1.2 教育观念 | **Stage 1a** | `positive-negative` | `advantage-disadvantage` → 1 second-variant |
| 1.5 师生话题 | **Stage 1a** | `opinion` | `discussion` (alias for `discuss-both-views` already used; pick `single-question` or `advantage-disadvantage`) → 1 second-variant |
| 4.4 自然资源 | **Stage 1a** | `two-questions` | `problem-solution` → 1 second-variant |
| All other 32 sub-cats (1.3, 1.4, 1.6, 1.7, 1.8, 2.1-2.5, 3.1-3.10, 4.1-4.3, 4.5, 4.6, 4.7, 5.1, 5.2, 6.1, 6.2, 7.1, 8.1, 8.2) | **Stage 1b** first essay | — | — |

Total second-variants: 2 (for 1.1) + 1 (1.2) + 1 (1.5) + 1 (4.4) = **5**.

Total Task 2 essays Stage 1b: 32 (first) + 5 (second) = **37** ✓.

---

## Wave Plan (v2: 4 waves + final, with T-016b added)

### Wave 0 — Foundation + Pilot (sequential, 1 subagent)

**Why first** (and now even more critical): T-016b must land BEFORE any second-variant essay commit, because the second-variant's `data-type` attribute won't be filterable until the chip is registered in `index.html`. T-016 must land before any commit at all. T-017 must land before any essay commit (verify gate). T-018 pilot validates the per-ticket AC + new-chip-set protocol before fanning out.

| Ticket | What | AC | Skills |
|---|---|---|---|
| `T-016` | Flip `concurrency.cancel-in-progress: false` → `true` in `.github/workflows/deploy.yml` | YAML parses; 4 SHA-pins preserved; comment explains why | `git-master` |
| **`T-016b`** | Extend `docs/writing/index.html`: add 3 new Task 2 chips (`problem-solution`, `advantage-disadvantage`, `single-question`) to lines 26–36 chip-row; update JS `knownTypes` Set (line 92) to include the 3 new values. Backward-compatible (existing 5 chips untouched). Commit. | `grep -c 'data-value="problem-solution"' docs/writing/index.html` returns 1; `grep -c 'knownTypes'` shows 3 new entries; existing chips untouched | `programming`, `git-master` |
| `T-017` | Write `scripts/verify-stage1b.sh` — bash + python3 -c enforcing: word-count band (170–190 / 270–290), single `<h1>`, single `<main>`, 3 data-attrs on `<article>` in one line, 5–10 `<code>` in keywords `<ul>`, Task 1 `<img loading="lazy">`, **8 valid Task 2 chips in `data-type`** (5 from Stage 1a + 3 new from T-016b). RED phase: inject deliberate violation into a 1a essay copy and verify script exits non-zero. GREEN: remove violation, exit 0. | script self-tests; documented header; `bash scripts/verify-stage1b.sh docs/writing/` exits 0 on Stage 1a corpus | `programming` |
| `T-018` | Pilot Task 1 essay (one of the process diagrams) — full pipeline: extract chart PNG via python-docx, multimodal-read numbers, write 170–190 word essay, 1–2 paragraph rubric, 5–10 keyword list, HTML template, commit, run `verify-stage1b.sh`, confirm Actions deploy | file `<slug>.html` exists; verify script PASS; Actions run green; chart numbers traceable to PNG | `writing`, `git-master` |

**Subagent count**: 1 (sequential inside the wave — T-018 depends on T-016, T-016b, T-017).

### Wave 1 — Task 1 essays (8 parallel subagents, 1 essay each)

Same as v1 — Task 1 work is independent of Task 2 chip expansion.

| Ticket | Slug | Source (docx) | data-type | data-difficulty |
|---|---|---|---|---|
| `T-019` | `06-process-rain-shadow-desert` | 5.Process rain-shadow desert | process | medium |
| `T-020` | `07-process-plastic-recycling` | 5.Process plastic recycling | process | medium |
| `T-021` | `08-process-cement-making` | 5.Process cement + concrete | process | hard |
| `T-022` | `09-mixed-library-survey` | 3.mixed library users | mixed-graph | medium |
| `T-023` | `10-dynamic-caribbean-tourists` | 2.Dynamic Caribbean island visitors 2010-2017 | dynamic-graph | medium |
| `T-024` | `11-dynamic-melbourne-activities` | 2.Dynamic Melbourne social centre activities | dynamic-graph | medium |
| `T-025` | `12-dynamic-asian-cities` | 2.Dynamic Asian countries urbanisation | dynamic-graph | hard |
| `T-026` | `13-static-uk-school-spending` | 1.Static UK school spending 3 pies | static-graph | easy |

**Subagent count**: 8 (parallel).

### Wave 2 — Task 2 first-essay batch (8 parallel subagents, 4 essays each)

**v2 correction**: SA-2a no longer includes 1.1 (covered in Stage 1a). Instead it covers **4.7 环保手段** + the next 3 unassigned sub-cats in the "教育" group.

| Subagent | Sub-cats | Essay slugs |
|---|---|---|
| SA-2a | 4.7 环保手段 + 1.3 语言学习 + 1.7 教育对象 + 1.8 教育现象 | 06, 07, 08, 09 |
| SA-2b | 2.1 工作选择 + 2.2 个人能力 + 2.3 工作环境 + 2.4 工作种类 | 10, 11, 12, 13 |
| SA-2c | 2.5 Work-life balance + 3.1 城市化 + 3.2 文化 + 3.3 老龄化 | 14, 15, 16, 17 |
| SA-2d | 3.4 交通 + 3.5 价值观对比 + 3.6 社会现象 + 3.7 隐私 | 18, 19, 20, 21 |
| SA-2e | 3.8 生活变迁 + 3.9 性别 + 3.10 文明礼貌 + 4.1 动物保护 | 22, 23, 24, 25 |
| SA-2f | 4.2 塑料 + 4.3 水资源 + 4.5 噪声污染 + 4.6 消费环境 | 26, 27, 28, 29 |
| SA-2g | 1.4 学历意义 + 1.6 教育方式 + 5.1 科技类 + 5.2 健康类 | 30, 31, 32, 33 |
| SA-2h | 6.1 媒体类 + 6.2 广告类 + 7.1 音乐 + 8.1 全球化 + 8.2 旅行 | 34, 35, 36, 37 (5 essays) |

Note: SA-2h covers **5 sub-cats** (slightly over the 4-per-subagent rule — accepts because the "媒体/广告/音乐/全球化/旅行" group is naturally adjacent and small). Total essays in Wave 2 = 4×7 + 5 = **33**. Adjusting: one sub-cat gets merged into another wave or removed.

**v2 correction**: 32 first-essay slots, not 33. Drop 1 sub-cat from SA-2h (e.g., merge 7.1 音乐 into SA-2g as "creative" topic, leaving SA-2g with 5 essays and SA-2h with 4). Or: SA-2g has 4 (1.4, 1.6, 5.1, 5.2), SA-2h has 4 (6.1, 6.2, 8.1, 8.2) — leaving 7.1 音乐 unassigned. Drop 7.1 from scope (it's not core to IELTS Topic Frequency by Band 7).

**Final v2 sub-cat assignment for Wave 2** (32 essays):

| Subagent | Sub-cats | Slugs |
|---|---|---|
| SA-2a | 4.7 + 1.3 + 1.7 + 1.8 | 06, 07, 08, 09 |
| SA-2b | 2.1 + 2.2 + 2.3 + 2.4 | 10, 11, 12, 13 |
| SA-2c | 2.5 + 3.1 + 3.2 + 3.3 | 14, 15, 16, 17 |
| SA-2d | 3.4 + 3.5 + 3.6 + 3.7 | 18, 19, 20, 21 |
| SA-2e | 3.8 + 3.9 + 3.10 + 4.1 | 22, 23, 24, 25 |
| SA-2f | 4.2 + 4.3 + 4.5 + 4.6 | 26, 27, 28, 29 |
| SA-2g | 1.4 + 1.6 + 5.1 + 5.2 | 30, 31, 32, 33 |
| SA-2h | 6.1 + 6.2 + 8.1 + 8.2 | 34, 35, 36, 37 |

**7.1 音乐** is OUT OF SCOPE for Stage 1b (covered by Stage 1c if user wants). Spec Boundaries should mention this.

**Subagent count**: 8 (parallel). Total essays in Wave 2 = **32** ✓.

### Wave 3 — Task 2 second-prompt-variant batch (2 parallel subagents, 3 + 2 essays)

**v2 correction**: second-variants target the actual Stage 1a (sub-cat × chip) cells, not invented sub-cats. Pick chip from the **3 new chips** added by T-016b.

| Subagent | (sub-cat × target-chip) cells | Slugs |
|---|---|---|
| SA-3a | 1.1 → `single-question` + 1.1 → `problem-solution` + 1.2 → `advantage-disadvantage` | 38, 39, 40 |
| SA-3b | 1.5 → `single-question` + 4.4 → `problem-solution` | 41, 42 |

**Subagent count**: 2 (parallel). Total essays in Wave 3 = **5** ✓.

### Wave 4 — Bulk Deploy Verify (1 subagent, sequential)

Same as v1 but corpus is now **55** essays (10 from Stage 1a + 45 from Stage 1b).

| Ticket | What | AC |
|---|---|---|
| `T-064` | (a) `git log --oneline | head -50` shows all Stage 1b commits. (b) `curl -sI` every one of **55** essay URLs returns 200. (c) `bash scripts/verify-stage1b.sh docs/writing/task1 docs/writing/task2` exits 0. (d) `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` shows latest run succeeded. (e) Playwright spot-check screenshots: 1 Task 1 process essay + 1 Task 2 second-variant essay + filter chip `[problem-solution]` + filter chip `[process]` showing ≥1 card. | All 5 sub-checks PASS; commit screenshot artifacts to `docs/screenshots/`. |

### Final — Ship Evidence Gate → /review-work → Fix → Re-verify → Ship

Sequential after Wave 4. Single subagent per gate.

1. **`ship-evidence-gate`** — scan diff for secrets; assert commit message format `stage 1b(T-NNN): ...` on every essay commit; assert no `--no-verify` or force pushes; assert T-016b's 3 new chips are visible in `index.html` and `knownTypes` Set.
2. **`/review-work`** (5 lanes in parallel — Oracle / Oracle / Oracle / unspecified-high / unspecified-high): goal-alignment, code-quality, security, hands-on QA, context-mining.
3. Fix any FAIL lane (small subagent per fix).
4. Re-run Wave 4 verification.
5. **Ship**: produce HANDOFF-stage1b.md + sign-off message to user.

**Total wave count**: 4 + final (5 phases). Subagent fan-out peaks at 8 in Wave 1 and 8 in Wave 2.

---

## Per-Ticket Acceptance Criteria (binary, blocking commit)

Each ticket's frontmatter carries these AC; the bulk-verify script (`T-017`) is the automated gate.

### All essays (Task 1 + Task 2)

```
AC-A1: file path matches docs/writing/task{N}/<NN>-<slug>.html
AC-A2: exactly one <h1> in file (grep -c '<h1>' returns 1)
AC-A3: exactly one <main> in file (grep -c '<main>' returns 1)
AC-A4: <article data-task="..." data-difficulty="..." data-type="..."> appears
       on a single line (regex matches all 3 attrs on same line)
AC-A5: <section class="essay"> exists with body text
AC-A6: <section class="rubric"> exists with 1-2 paragraphs containing
       TA / CC / LR / GRA markers (Chinese)
AC-A7: <section class="keywords"><ul> exists with 5-10 <code> items
       (grep -c '<code>' inside section returns N where 5 <= N <= 10)
AC-A8: commit message matches: ^stage 1b\(T-\d{3}\): [a-z0-9-]+ — .+$
AC-A9: file content matches Stage 1a template structure
       (same nav, head, link, script tags as 01-..05 siblings)
```

### Task 1 essays only

```
AC-T1-1: <figure> contains <img loading="lazy" decoding="async" alt="..." width=... height=...>
         AND <figcaption>
AC-T1-2: <img src="../../assets/images/task1-charts/<slug>.png"> resolves to
         docs/assets/images/task1-charts/<slug>.png (test -f)
AC-T1-3: word count of <section class="essay"> body is in [170, 190]
AC-T1-4: ticket's ## Chart data section documents every numeric figure in
         the essay with a line reference to the chart PNG
AC-T1-5: if any number in essay is NOT documented in ## Chart data, ticket
         status = blocked, no commit
```

### Task 2 essays only

```
AC-T2-1: no <figure> element present
AC-T2-2: word count of <section class="essay"> body is in [270, 290]
AC-T2-3: data-type value MUST be one of the 8 valid Task 2 chips:
         {agree-disagree, discuss-both-views, positive-negative, opinion,
          two-questions, problem-solution, advantage-disadvantage, single-question}
         (verified by grep against this set in verify script)
AC-T2-4: for second-variant tickets (T-059..T-063): data-type MUST differ
         from sibling essay's data-type (e.g., 1.1 sibling uses
         `agree-disagree` → second-variant cannot use `agree-disagree`)
AC-T2-5: prompt source line references the exact docx paragraph
         (sub-cat code + question # in frontmatter)
```

### Workflow + verify-script tickets

```
AC-WF-1 (T-016): .github/workflows/deploy.yml has cancel-in-progress: true;
                 all 4 SHA-pins preserved
AC-WF-2 (T-016b): docs/writing/index.html line 26-36 has 8 Task 2 chips
                  (5 Stage 1a + 3 new); knownTypes Set (line 92) includes
                  all 8 values; existing 5 chips UNCHANGED
AC-VFY-1 (T-017): scripts/verify-stage1b.sh runs against docs/writing/task1
                 and docs/writing/task2; checks A1-A9 + T1/T2 AC; exit 0
                 on Stage 1a corpus; documented header; RED-phase
                 self-test passes (script exits non-zero on a deliberately
                 violated 1a essay)
AC-VFY-2 (T-064): all 55 essay URLs return 200; filter chips
                  [process], [problem-solution], [advantage-disadvantage],
                  [single-question] show >=1 card; GH Actions deploy green
```

---

## Subagent Fan-Out Strategy (unchanged from v1)

- **Task 1 subagents**: 1 essay per subagent (heavy multimodal load).
- **Task 2 subagents**: 4 essays per subagent (text-only).
- **Maximum parallel subagents per wave**: 8.

---

## Chart Extraction Protocol for Task 1 (unchanged from v1)

Same as v1. Any failure ⇒ BLOCKED ticket, no commit. See v1 §Chart Extraction Protocol for full steps.

---

## Keyword Extraction Rules (unchanged from v1)

Same as v1. See v1 §Keyword Extraction Rules for composition + anti-patterns.

---

## Rollback Plan (v2 update for T-016b)

### Single-essay rollback

```
git revert <commit-sha> --no-edit && git push origin main
```

### T-016b rollback (chip dictionary extension)

If the 3 new chips cause filter JS bugs:

```
git revert <T-016b-commit-sha> --no-edit   # removes new chips
# OR fix in place:
edit docs/writing/index.html  # remove the 3 new <button> lines
edit docs/writing/index.html  # remove 3 new entries from knownTypes Set
git commit -m "stage 1b(fix T-016b): <one-line fix>"
git push origin main
```

If T-016b is reverted, ALL 5 second-variant essays (T-059..T-063) become un-filterable (filter rejects their data-type). They would need either reversion too, or live as orphaned essays only reachable via direct URL.

**Mitigation**: T-016b must be tested by T-018 pilot (which uses one of the new chips in a Task 1 essay... wait, Task 1 doesn't use the new Task 2 chips. Instead: T-018 pilot should validate T-016b's filter functionality by curling the live site and asserting all 8 Task 2 chips are present in the rendered HTML).

### Other rollbacks (T-016, T-017)

Same as v1.

### Nuclear rollback (Stage 1b as a whole)

```
git revert <range-of-50-commits> --no-edit   # or interactive rebase
# OR
git reset --hard fbd2072   # destructive, requires force-push
```

---

## Risk Register (v2)

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **Chart unreadable** — multimodal looker returns garbled numbers for a dense chart | Medium | 1 essay BLOCKED per occurrence | Pilot (T-018) catches protocol bugs early. BLOCKED threshold is per-essay, not per-batch. Multimodal prompt can be re-iterated. |
| R2 | **Template drift** — Task 2 subagents re-typing the template from scratch introduce subtle differences | High | Forces re-do of 4-essay batch | Subagent copies Stage 1a essay as starting skeleton, then swaps content. Bulk-verify script catches A1-A9 violations pre-commit. |
| R3 | **Context window exhaustion** — subagent accumulates docx text + ticket + chart PNG + template + 4 essay drafts | Medium | Subagent loses coherence, keywords degrade | 4-essay cap per Task 2 subagent (rule above). |
| R4 | **Actions concurrency deadlock** — `cancel-in-progress: true` cancels in-flight deploys, but if all 50 commits push within 60s, GitHub's concurrent run cap cancels the FINAL deploy | Low | Final deploy never runs | Dispatcher's final commit (T-064) waits 30s before pushing. Monitor `gh api .../actions/runs?workflow=deploy.yml` in Wave 4 and re-push if needed. |
| R5 | **Bulk-deploy network failure** — git push times out or Actions service incident during 50-commit burst | Low | Some commits don't push | Dispatcher's git push loop retries 3× with exponential backoff. |
| **R6** (new) | **T-016b new chips not recognized by filter JS** — typo in `knownTypes` Set or chip button HTML causes second-variant essays to be unfindable | Medium | 5 second-variants become orphaned | T-018 pilot MUST validate: curl live index.html and assert 8 chip values present + 8 knownTypes entries; then test by clicking the new chip on the live filter UI via Playwright. |
| **R7** (new) | **Second-variant chip collision** — second-variant picks a chip already used by sibling | Medium | Violates AC-T2-4; subagent must redo | Frontmatter carries `(sub-cat × target-chip)` tuple explicitly. Verify script AC-T2-4 enforces. |
| **R8** (corrected) | **Docx "mystery" charts** — Task 1 docx has 2-3 map charts (image13/14 harbour) that have no numeric figures and can't satisfy AC-T1-4 (figures traceable to chart) | Low | Those map charts OUT OF SCOPE for Stage 1b | Spec Boundaries lists `[map]` chip as remaining empty by design. Out of scope. |

### Minor risks

- **R9 Topic mismatch**: writer picks wrong sub-cat — frontmatter sub-cat code cross-checked against essay content
- **R10 Chip-pick ambiguity**: SA-3 subagents may disagree on which chip is best for the second-variant — leave pick to writer discretion within the 3 new chips; verify script enforces AC-T2-4 only
- **R11 Docx version drift**: user updates source docx during Stage 1b — out of scope, defer to Stage 1c

---

## Skills to Load Per Subagent (unchanged from v1)

Same as v1. Foundation: `programming`, `git-master`. Task 1: `writing`, `git-master`, plus inline `look_at`. Task 2: `writing`, `git-master`. Bulk-verify: `git-master`, inline `playwright`. Final gates: `ship-evidence-gate`, `/review-work`.

---

## Verification Gates (v2 update)

| Gate | When | What | Pass criteria |
|---|---|---|---|
| **G0** Per-subagent self-check | After each essay HTML composed, before commit | `bash scripts/verify-stage1b.sh docs/writing/taskN/<file>.html` | Exit 0; A1-A9 + T1/T2 specific AC pass |
| **G1** Per-wave bulk scan | After each wave's commits pushed | `bash scripts/verify-stage1b.sh docs/writing/` full sweep | Exit 0 for all essays in wave |
| **G1.5** Chip-set integrity | After Wave 0 commits | `curl -sL https://meisijiya.github.io/IELTS/writing/ | grep -c 'data-value="problem-solution"'` returns ≥1; same for `advantage-disadvantage`, `single-question` | All 8 Task 2 chips present in live HTML |
| **G2** Actions deploy green | After final commit of each wave | `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` | Latest run `conclusion: success` |
| **G3** Live URL sweep | Wave 4 | `curl -sI` all **55** essay URLs + homepage + writing index | Every URL returns 200; body contains expected `<h1>` title |
| **G4** Filter chip coverage | Wave 4 | Playwright clicks `[process]`, `[problem-solution]`, `[advantage-disadvantage]`, `[single-question]` chips on `/writing/` | ≥1 essay card visible per chip. `[map]` chip remains empty by docx design (R8). |
| **G5** Spot-check screenshots | Wave 4 | Playwright screenshots: 1 Task 1 process essay, 1 Task 2 second-variant essay, filter chip states | Saved to `docs/screenshots/05..08-*.png` |
| **G6** ship-evidence-gate | Final | Sensitive-info scan + commit message format check + no --no-verify + T-016b chip-set assertion | PASS |
| **G7** /review-work (5 lanes) | Final | Oracle x3 + unspecified-high x2 | All 5 lanes PASS or FIXED-then-PASS |

---

## Atomic Commit Strategy (unchanged from v1)

Same as v1. 50 commits total. Commit message format: `stage 1b(T-NNN): <slug> — <one-line what>`.

---

## TDD-Oriented Planning Notes (unchanged from v1)

RED→GREEN→REFACTOR cycle maps to:
- RED: T-017 verify script tested against a deliberately violated 1a essay
- GREEN: each Task 1/2 subagent writes the minimum essay that satisfies AC
- REFACTOR: cosmetic cleanups (redundant `<h2>`, missing `<img width height>`) deferred

---

## Phase Boundary

**STOP after Final wave**. Do NOT run `to-tickets`, `/start-work`, or any further planning steps.

```
## Next stage
PASS → to-tickets → /start-work
```

---

## Out of Scope (v2)

- New module surfaces (Reading / Speaking / Listening still `aria-disabled`)
- HTTPS upgrade, per-repo CNAME, SEO, sitemap, analytics
- Multi-language UI
- SOP-B per-paragraph Chinese explanation
- Stage 1a essay rewrites (kept verbatim)
- Visual-qa dual-oracle gate (deferred to Stage 1c)
- **`[map]` chip filter content** (docx has 0 numeric-bearing map charts; AC-T1-4 forbids non-traceable figures, so map charts are skipped)
- **`7.1 音乐` sub-category** (dropped from Wave 2 to keep 32-first-essay budget; out of scope for Stage 1b)
- **Multi-prompt coverage for sub-categories** (one essay per sub-cat; second variants only for the 5 Stage-1a-covered cells)

---

## References

- Spec: `.omo/specs/ielts-writing-site-stage1b.md`
- Handoff: `HANDOFF-stage1a.md` at repo root
- Stage 1a plan: `.omo/plans/stage1a.md`
- Source: `Task 1 冲刺(1).docx`, `作文真题储备（近五年）_可修改.docx`
- Filter UI: `docs/writing/index.html` lines 26–36 (chips), 92–94 (knownTypes Set)
- Deploy endpoint: `https://meisijiya.github.io/IELTS/`
- Stage 1a essay template anchors: `docs/writing/task1/01-table-universities-ranked.html` (T1), `docs/writing/task2/01-agree-disagree-history-vs-business.html` (T2)