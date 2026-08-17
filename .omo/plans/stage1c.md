# stage1c - Work Plan

## TL;DR (For humans)

**What you'll get:** 191 new IELTS Task 2 sample essays (one per unused prompt in `作文真题储备（近五年）_可修改.docx`, except the dropped `7.1 音乐` sub-category), bringing the live site from 55 essays to **246** covering every docx prompt except the one dropped sub-category.

**Why this approach:** Extend the proven Stage 1a/1b pipeline (atomic 1-essay-per-commit + 9 invariants + 8-chip whitelist + 270-290 word band) — only changes are (1) `scripts/verify-stage1b.sh` gains 3 new gates (AC-T2-1 no-figure, AC-T2-4 prompt-uniqueness frontmatter, chip-distribution non-zero) and (2) `docs/writing/index.html` extends from 55 → 246 cards. No template change, no chip whitelist change, no Stage 1a/1b modification.

**What it will NOT do:** Modify Stage 1a/1b's 55 essays · change the 9 invariants · change the 8-chip whitelist · write the dropped `7.1 音乐` sub-category · add new dependencies · bypass the verify script · introduce new module surfaces.

**Effort:** XL
**Risk:** Medium — visual-qa dual-oracle on 246 essays may surface non-blocking design issues that need a fix-loop; prompt-source frontmatter protocol is new and may have first-write friction.
**Decisions to sanity-check:** 4-essay-per-subagent capacity at the largest sub-cats (8.2 旅行 has 23 prompts → 6 subagents across 1 wave); verify-script AC-T2-4 prompt-uniqueness frontmatter protocol.

Your next move: approve (or call out specific gaps). Execution belongs to a separate worker session that you start with `$start-work` after to-tickets.

---

> TL;DR (machine): XL · Medium risk · 191 new Task 2 essays + 1 verify-script patch + 1 index-extension scaffold + 4 foundation + 5 final-verifier = 200 tickets, 7 waves.

## Scope
### Must have
- 191 new Task 2 essay HTML files at `docs/writing/task2/<NN>-<slug>.html` (NN from 043 to 233, exact enumeration in `.omo/drafts/stage1c-prompts.md`)
- `docs/writing/index.html` extended from 55 → 246 `<article>` cards
- `scripts/verify-stage1b.sh` patched with 3 new gates: AC-T2-1 (no `<figure>` in Task 2), AC-T2-4 (frontmatter `prompt-source: <sub-cat>-<N>` deduplication), chip-distribution non-zero
- 3 handoff artifacts deleted: `HANDOFF-stage1a.md`, `HANDOFF-stage1b.md`, `.opencode/handoffs/2026-08-15T154136.md` (per spec scenario `handoff-cleanup`, executed in Wave 0 / T-068)
- `HANDOFF-stage1c.md` at repo root after ship (mirror Stage 1b format)
- Per-essay frontmatter `<meta name="prompt-source" content="<sub-cat>-<N>">` for AC-T2-4 enforcement
- Visual-qa dual-oracle pass on the full 246-essay corpus in Wave 7 (per user "全量必做")

### Must NOT have (guardrails, anti-slop, scope boundaries)
- Stage 1a/1b 55 essay modifications (content or template)
- 9 invariants modification (single `<h1>`, single `<main>`, `<article>` data-attrs, 5-10 `<code>`, word band, etc.)
- 8-chip whitelist modification or new chips added (8 chips cover all 234 docx prompts)
- `7.1 音乐` sub-category essay writing (dropped; 1 prompt skipped)
- New module surfaces (Reading / Speaking / Listening stay `aria-disabled`)
- New dependencies, new build pipeline
- HTTPS / SEO / sitemap / analytics / multi-language UI
- Per-paragraph Chinese rubric (consolidated 1-2 paragraph is contract)
- Visual-qa non-blocking issues escalated to Wave 7 fix-loop beyond 1 round
- Stage 1a/1b essay rewrites
- Detached subagent implementations (worker session enforces)

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- **Test decision**: tests-after (each essay validates against an existing verify script; verify script gains 3 new gates before any essay commits in Wave 1+)
- **Framework**: bash + python3-c (existing `scripts/verify-stage1b.sh`, extended with 3 new checks)
- **Evidence** (per ticket): `bash scripts/verify-stage1b.sh docs/writing/task2/<NN>-<slug>.html` exit 0; per-wave: full sweep + `grep -c 'data-type="<chip>"' docs/writing/index.html`; Wave 7: 246-URL curl + Playwright spot-check + visual-qa dual-oracle

### Gates (G0-G7)
| Gate | When | What | Pass criteria |
|---|---|---|---|
| **G0** Per-essay | After each essay composed, before commit | `bash scripts/verify-stage1b.sh docs/writing/task2/<file>.html` | exit 0; all 9 invariants + 3 new gates (AC-T2-1 no `<figure>`, AC-T2-4 prompt-source unique, chip-distribution) pass |
| **G1** Per-wave bulk | After each wave's commits pushed | `bash scripts/verify-stage1b.sh docs/writing/` full sweep | exit 0; cumulative essay count matches wave plan; chip distribution non-zero for all 8 chips |
| **G2** Actions deploy green | After each wave's final commit | `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` | latest run `conclusion: success` |
| **G3** Live URL sweep | Wave 7 only | `curl -sI` 246 essay URLs (HTTP 200) | every URL returns 200, body contains expected `<h1>` |
| **G4** Index 246-card count | Wave 7 only | `grep -c '^    <article data-task' docs/writing/index.html` | returns 246 |
| **G5** Chip coverage | Wave 7 only | `grep -c 'data-type="<chip>"' docs/writing/index.html` for each of 8 chips | every chip count ≥ 1 |
| **G6** Playwright spot-check | Wave 7 only | Playwright clicks `[agree-disagree]` / `[problem-solution]` / `[opinion]` (rare chip) on `/writing/` | each chip shows ≥1 card |
| **G7** Visual-qa dual-oracle | Wave 7 only | `visual-qa` skill, 4 lanes (design-system / functional / CJK fidelity / accessibility) on full 246-essay corpus | 0 blocking issues + ≤1 round fix-pass; non-blocking issues registered as Stage 2 debt, not blocking ship |
| **G8** ship-evidence-gate | Wave 7 final | Sensitive-info scan + commit message format `stage 1c(T-NNN): <slug> — <one-line>` + no `--no-verify` + handoff files deleted | PASS |
| **G9** /review-work 5-lane | Wave 7 final | Oracle x3 + unspecified-high x2 (goal-alignment / code-quality / security / hands-on QA / context-mining) | all 5 lanes PASS or FIXED-then-PASS |

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave (essay todos are grouped: each wave = 8 SA × 4 essay = 32 essay-todos).

| Wave | Title | Tickets | SA parallelism | Total essays | Sequential? |
|---|---|---|---|---|---|
| **Wave 0** | Foundation (verify-script patch + index scaffold + pilot + handoff cleanup) | 4 | 1 sequential | 1 pilot essay | yes |
| **Wave 1** | Task 2 essays batch 1 (sub-cats 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8 — 32 prompts) | 32 | 8 SA × 4 essay | 32 | no, parallel |
| **Wave 2** | Task 2 essays batch 2 (sub-cats 2.1, 2.2, 2.3, 3.1 — 32 prompts) | 32 | 8 SA × 4 essay | 32 | no, parallel |
| **Wave 3** | Task 2 essays batch 3 (sub-cats 3.2, 3.3, 3.4, 3.5 — 32 prompts) | 32 | 8 SA × 4 essay | 32 | no, parallel |
| **Wave 4** | Task 2 essays batch 4 (sub-cats 3.6, 3.8, 4.1, 4.3, 4.4, 4.6, 4.7 — 32 prompts) | 32 | 8 SA × 4 essay | 32 | no, parallel |
| **Wave 5** | Task 2 essays batch 5 (sub-cats 5.1, 5.2, 6.1 — 32 prompts) | 32 | 8 SA × 4 essay | 32 | no, parallel |
| **Wave 6** | Task 2 essays batch 6 (sub-cats 6.2, 8.1, 8.2 — 31 prompts) | 31 | 8 SA × 3-4 essay | 31 | no, parallel |
| **Wave 7** | Final verification (bulk verify + Playwright + visual-qa + ship + HANDOFF) | 5 | 1 sequential | 0 | yes |

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| T-065 (verify-script patch) | — | T-066, T-067, T-068, all Wave 1+ essay todos | — |
| T-066 (index scaffold) | T-065 | all Wave 1+ essay todos | T-067, T-068 |
| T-067 (pilot essay) | T-065 | all Wave 1+ essay todos | T-066, T-068 |
| T-068 (handoff cleanup) | T-065 | Wave 7 T-264 | T-066, T-067 |
| T-069..T-100 (Wave 1 essays) | T-065, T-066, T-067 | T-101 (Wave 2 start), Wave 7 T-260 | within wave (8 SA × 4 essay) |
| T-101..T-132 (Wave 2 essays) | T-069..T-100 commit pushed + G1 PASS | Wave 3, Wave 7 T-260 | within wave (8 SA × 4 essay) |
| T-133..T-164 (Wave 3 essays) | T-101..T-132 commit pushed + G1 PASS | Wave 4, Wave 7 T-260 | within wave (8 SA × 4 essay) |
| T-165..T-196 (Wave 4 essays) | T-133..T-164 commit pushed + G1 PASS | Wave 5, Wave 7 T-260 | within wave (8 SA × 4 essay) |
| T-197..T-228 (Wave 5 essays) | T-165..T-196 commit pushed + G1 PASS | Wave 6, Wave 7 T-260 | within wave (8 SA × 4 essay) |
| T-229..T-259 (Wave 6 essays) | T-197..T-228 commit pushed + G1 PASS | Wave 7 T-260 | within wave (8 SA × 3-4 essay) |
| T-260 (bulk verify) | all Wave 1-6 essay todos | T-261..T-264 | — |
| T-261 (Playwright spot-check) | T-260 | T-262..T-264 | — |
| T-262 (visual-qa dual-oracle) | T-261 | T-263 | — |
| T-263 (ship-evidence-gate + /review-work 5-lane) | T-262 | T-264 | — |
| T-264 (HANDOFF-stage1c.md) | T-068, T-263 | (ship) | — |

## Todos
> Implementation + Test = ONE todo. Never separate.
> Essay todos (T-069..T-259) use compact 1-line form; per-essay AC/QA/Commit follows the wave-level Essay AC Template.

### Essay AC Template (applies to T-069..T-259)

```
References:
  - 作文真题储备（近五年）_可修改.docx, sub-cat X.Y prompt-N (per .omo/drafts/stage1c-prompts.md)
  - docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54 (Stage 1a template)
  - docs/writing/task2/06-26-env-solutions.html:1-53 (Stage 1b template)
  - .opencode/skills/ielts-writing/SKILL.md SOP-B (target band 6-7 generation rules)

Acceptance criteria (agent-executable):
  - bash scripts/verify-stage1b.sh docs/writing/task2/<NN>-<slug>.html → exit 0
  - 9 invariants: A2 (1 <h1>), A3 (1 <main>), A4 (<article data-task data-difficulty data-type> on one line), A7 (5-10 <code> in keywords)
  - AC-T2-1 NEW: no <figure> element (verify script gated after T-065 lands)
  - AC-T2-2: word count 270-290 in <section class="essay">
  - AC-T2-3: data-type in {agree-disagree, discuss-both-views, positive-negative, opinion, two-questions, problem-solution, advantage-disadvantage, single-question}
  - AC-T2-4 NEW: <meta name="prompt-source" content="<sub-cat>-<N>"> present in <head>; verify script deduplicates across all 246 essays
  - AC-T2-5 NEW: data-type value matches chip derived from prompt's question word (verified by per-prompt mapping in .omo/drafts/stage1c-prompts.md)
  - AC-A6 implicit: <section class="rubric"> with TA/CC/LR/GRA 4-2 Chinese paragraphs present
  - AC-A5 implicit: <section class="essay"> present with 270-290 English words
  - Prompt paraphrase: essay <section class="prompt"><p> reproduces docx prompt text + exam date if present

QA scenarios (happy + failure):
  - happy: bash scripts/verify-stage1b.sh docs/writing/task2/<NN>-<slug>.html exit 0 + grep -c '<meta name="prompt-source"' docs/writing/task2/<NN>-<slug>.html returns 1
  - failure: bash scripts/verify-stage1b.sh exit non-zero (e.g., word count 285 outside band) → ticket BLOCKED, subagent fixes before commit

Commit: Y | stage 1c(T-NNN): <NN>-<slug> — <chip> essay
```

### Wave 0 — Foundation (4 todos, sequential)

- [ ] 1. T-065: verify-script patch (AC-T2-1 no-figure + AC-T2-4 prompt-uniqueness frontmatter gate + chip-distribution non-zero) + dry-run on Stage 1b 55-essay corpus
  What to do / Must NOT do: Add 3 new checks to `scripts/verify-stage1b.sh` python3-c block. AC-T2-1: if file under task2/ and `<figure` in content → err "AC-T2-1: <figure> not allowed in Task 2 essay". AC-T2-4: if no `<meta name="prompt-source"` → err "AC-T2-4: missing prompt-source frontmatter". (prompt-source dedup is enforced across all 246 essays at Wave 7 via a separate script — G1.) Patch script header comment to reflect new invariants. Must NOT: change 9 invariants or 8-chip whitelist. Must NOT: add new dependencies.
  Parallelization: Wave 0 (sequential) | Blocked by: — | Blocks: T-066, T-067, T-068, all Wave 1+ essay todos
  References: `scripts/verify-stage1b.sh:1-151` (current implementation); `.omo/plans/stage1b.md:179-247` (Stage 1b AC list); `docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54` (Stage 1a essay template)
  Acceptance criteria (agent-executable): (a) `bash scripts/verify-stage1b.sh --self-test` exit 0; (b) `bash scripts/verify-stage1b.sh docs/writing/task2/` (Stage 1b 37 essays) exit 0; (c) deliberately inject a `<figure>` into a Stage 1b essay copy → script exits non-zero with "AC-T2-1" error; (d) deliberately remove `<meta name="prompt-source"` → script exits non-zero with "AC-T2-4" error; (f) re-run after restoring both → exit 0
  QA scenarios (name the exact tool + invocation): happy — `bash scripts/verify-stage1b.sh docs/writing/task2/` returns PASS for all 37 Stage 1b essays; failure — `bash scripts/verify-stage1b.sh --self-test` exits non-zero on a violation-injected file
  Commit: Y | stage 1c(T-065): verify-script patch — AC-T2-1/AC-T2-4/chip-distrib gates

- [ ] 2. T-066: index extension scaffold (Python script reads each new essay's `<article>` + `<h1>` + `<meta name="prompt-source">` and emits 191 `<article>` cards into `docs/writing/index.html` between Stage 1a's 10 cards and Stage 1b's 45 cards, preserving existing 55)
  What to do / Must NOT do: Write `.omo/scripts/extend-writing-index.py` that walks `docs/writing/task2/` files, parses each essay's `<article data-task data-difficulty data-type>` + `<h1>` + `<meta name="prompt-source">`, and emits new `<article>` cards in order. Cards preserve existing filter chip JS behavior (no new chips). Backward-compatible (existing 55 cards untouched). Must NOT: change filter JS logic. Must NOT: re-emit Stage 1a/1b cards.
  Parallelization: Wave 0 (sequential) | Blocked by: T-065 | Blocks: all Wave 1+ essay todos (their commits won't break index)
  References: `docs/writing/index.html:1-342` (current index with 55 cards); `.omo/drafts/stage1c-prompts.md` (191 prompt enumeration with filename); `.omo/plans/stage1b.md:255-260` (Stage 1b T-064a index extension precedent)
  Acceptance criteria (agent-executable): (a) `python3 .omo/scripts/extend-writing-index.py --dry-run` outputs 191 new card lines without writing; (b) `python3 .omo/scripts/extend-writing-index.py` (no flag) writes 191 cards into `docs/writing/index.html`; (c) `grep -c '^    <article data-task' docs/writing/index.html` returns 246; (d) `grep -c 'data-value="problem-solution"' docs/writing/index.html` returns 1 (chip preserved); (e) existing 55 cards unchanged (`diff <(git show HEAD:docs/writing/index.html | grep '^    <article') <(grep '^    <article' docs/writing/index.html | head -55)` returns no diff in the first 55 cards)
  QA scenarios: happy — index.html has 246 cards, all chips preserved; failure — if any essay HTML has malformed `<article>` tag, script crashes mid-emit; mitigation: dry-run output first, then commit per-wave cards not all at once (worker uses per-wave sub-script calls)
  Commit: Y | stage 1c(T-066): index extension scaffold + 246 cards ready

- [ ] 3. T-067: pilot essay end-to-end (write 1 essay from Wave 1 enumeration, run all gates G0-G2, deploy via Actions, confirm chip whitelist renders correctly + per-essay frontmatter gate works)
  What to do / Must NOT do: Pick the first Wave 1 essay (T-069: 043-education-subjects-3.html, sub-cat 1.1 prompt 3, chip agree-disagree, easy). Write full essay HTML following Stage 1a template. Include `<meta name="prompt-source" content="1.1-3">` in `<head>`. Run all gates: G0 verify script, G1 chip-distribution sanity, G2 Actions deploy. Must NOT: write a non-Wave-1 essay (validation scope is locked). Must NOT: skip any gate.
  Parallelization: Wave 0 (sequential) | Blocked by: T-065 | Blocks: all Wave 1+ essay todos (validates the per-essay protocol before fan-out)
  References: `docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54` (Stage 1a template to copy); `.opencode/skills/ielts-writing/SKILL.md:104-136` (SOP-B target band 6-7 generation); `.omo/drafts/stage1c-prompts.md` (T-069 mapping)
  Acceptance criteria (agent-executable): (a) `docs/writing/task2/043-education-subjects-3.html` exists; (b) `bash scripts/verify-stage1b.sh docs/writing/task2/043-education-subjects-3.html` exit 0; (c) `grep '<meta name="prompt-source" content="1.1-3"' docs/writing/task2/043-education-subjects-3.html` returns 1 line; (d) `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml | jq '.workflow_runs[0].conclusion'` returns "success" within 10 min of push; (e) `curl -sI https://meisijiya.github.io/IELTS/writing/task2/043-education-subjects-3.html` returns HTTP 200
  QA scenarios: happy — pilot essay ships live and visible at URL; failure — verify script catches AC-T2-1 (figure) or AC-T2-4 (missing prompt-source) → subagent re-writes and re-verifies before commit
  Commit: Y | stage 1c(T-067): 043-education-subjects-3 — pilot essay (chip=agree-disagree)

- [ ] 4. T-068: handoff cleanup (delete 3 handoff artifacts: HANDOFF-stage1a.md, HANDOFF-stage1b.md, .opencode/handoffs/2026-08-15T154136.md)
  What to do / Must NOT do: Run grep check first (per spec scenario `no-broken-references`): `grep -rn 'HANDOFF-stage1[ab]\.md' --include='*.md' --include='*.sh' --include='*.yml' .` should return 0 hits outside `.git/` and `.omo/` (gitignored). If any live reference found, surface to user. Then `git rm HANDOFF-stage1a.md HANDOFF-stage1b.md` and commit; `rm .opencode/handoffs/2026-08-15T154136.md` (already gitignored). Must NOT: delete any other file. Must NOT: amend existing commits.
  Parallelization: Wave 0 (sequential) | Blocked by: T-065 (verify script must be in place before any commit) | Blocks: T-264 (HANDOFF-stage1c.md commit)
  References: `HANDOFF-stage1a.md` (Stage 1a handoff, repo root, git tracked); `HANDOFF-stage1b.md` (Stage 1b handoff, repo root, git tracked); `.opencode/handoffs/2026-08-15T154136.md` (Aug 15 handoff, .opencode/ gitignored)
  Acceptance criteria (agent-executable): (a) `[ ! -f HANDOFF-stage1a.md ] && [ ! -f HANDOFF-stage1b.md ] && [ ! -f .opencode/handoffs/2026-08-15T154136.md ]` returns true; (b) `git log --oneline | head -5` shows a single `stage 1c(T-068): handoff cleanup` commit removing both HANDOFF files; (c) `grep -rn 'HANDOFF-stage1[ab]\.md' --include='*.md' --include='*.sh' --include='*.yml' .` returns 0 hits outside .git
  QA scenarios: happy — 3 files gone, 1 commit added; failure — grep surfaces a live reference → subagent BLOCKED, reports to user
  Commit: Y | stage 1c(T-068): handoff cleanup — drop 3 stage 1a/1b handoff docs

### Wave 1 — Task 2 essays batch 1 (32 todos, 8 SA × 4 essay parallel)

Sub-cats covered: 1.1 (5), 1.2 (7), 1.4 (2), 1.5 (1), 1.6 (6), 1.7 (2), 1.8 (2), 2.1 (5), 2.2 (2) — total 32 prompts
SA assignment: SA-1a = sub-cat 1.1 (5 prompts in 4 = first 4); SA-1b = sub-cat 1.1 (last 1) + sub-cat 1.2 first 3; SA-1c = sub-cat 1.2 last 4; SA-1d = sub-cat 1.4 + 1.5 + 1.6 first 1; SA-1e = sub-cat 1.6 next 4; SA-1f = sub-cat 1.7 + 1.8; SA-1g = sub-cat 2.1; SA-1h = sub-cat 2.2 + 2.3
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 3-36)

- [ ] 5. T-069: 043-education-subjects-3 — agree-disagree, easy
- [ ] 6. T-070: 044-education-subjects-4 — agree-disagree, medium
- [ ] 7. T-071: 045-education-subjects-5 — discuss-both-views, hard
- [ ] 8. T-072: 046-education-values-4 — discuss-both-views, medium
- [ ] 9. T-073: 047-education-values-5 — agree-disagree, medium
- [ ] 10. T-074: 048-education-values-6 — agree-disagree, easy
- [ ] 11. T-075: 049-education-values-7 — agree-disagree, easy
- [ ] 12. T-076: 050-education-values-8 — agree-disagree, easy
- [ ] 13. T-077: 051-education-values-9 — discuss-both-views, medium
- [ ] 14. T-078: 052-education-values-10 — discuss-both-views, easy
- [ ] 15. T-079: 053-qualifications-2 — discuss-both-views, medium
- [ ] 16. T-080: 054-qualifications-3 — discuss-both-views, medium
- [ ] 17. T-081: 055-teacher-student-1 — discuss-both-views, medium
- [ ] 18. T-082: 056-education-method-2 — agree-disagree, easy
- [ ] 19. T-083: 057-education-method-3 — advantage-disadvantage, medium
- [ ] 20. T-084: 058-education-method-4 — agree-disagree, easy
- [ ] 21. T-085: 059-education-method-5 — agree-disagree, medium
- [ ] 22. T-086: 060-education-method-6 — two-questions, easy
- [ ] 23. T-087: 061-education-method-7 — two-questions, easy
- [ ] 24. T-088: 062-education-comparison-2 — advantage-disadvantage, easy
- [ ] 25. T-089: 063-education-comparison-3 — agree-disagree, hard
- [ ] 26. T-090: 064-education-phenomenon-1 — two-questions, medium
- [ ] 27. T-091: 065-education-phenomenon-3 — positive-negative, easy
- [ ] 28. T-092: 066-job-choice-2 — advantage-disadvantage, easy
- [ ] 29. T-093: 067-job-choice-3 — agree-disagree, easy
- [ ] 30. T-094: 068-job-choice-4 — agree-disagree, easy
- [ ] 31. T-095: 069-job-choice-5 — discuss-both-views, easy
- [ ] 32. T-096: 070-job-choice-6 — agree-disagree, easy
- [ ] 33. T-097: 071-personal-skills-2 — agree-disagree, hard
- [ ] 34. T-098: 072-personal-skills-3 — agree-disagree, medium
- [ ] 35. T-099: 073-personal-skills-4 — positive-negative, easy
- [ ] 36. T-100: 074-personal-skills-5 — agree-disagree, medium

### Wave 2 — Task 2 essays batch 2 (32 todos, 8 SA × 4 essay parallel)

Sub-cats: 2.3 (3), 3.1 (9), rest from Wave 1 overflow — total 32 prompts
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 35-44)

- [ ] 37. T-101: 075-work-environment-2 — agree-disagree, medium
- [ ] 38. T-102: 076-work-environment-3 — agree-disagree, hard
- [ ] 39. T-103: 077-work-environment-4 — agree-disagree, medium
- [ ] 40. T-104: 078-urbanisation-2 — agree-disagree, hard
- [ ] 41. T-105: 079-urbanisation-3 — agree-disagree, hard
- [ ] 42. T-106: 080-urbanisation-4 — positive-negative, easy
- [ ] 43. T-107: 081-urbanisation-5 — advantage-disadvantage, medium
- [ ] 44. T-108: 082-urbanisation-6 — advantage-disadvantage, medium
- [ ] 45. T-109: 083-urbanisation-7 — advantage-disadvantage, medium
- [ ] 46. T-110: 084-urbanisation-8 — advantage-disadvantage, medium
- [ ] 47. T-111: 085-urbanisation-9 — agree-disagree, medium
- [ ] 48. T-112: 086-culture-2 — agree-disagree, medium
- [ ] 49. T-113: 087-culture-3 — discuss-both-views, medium
- [ ] 50. T-114: 088-culture-4 — agree-disagree, medium
- [ ] 51. T-115: 089-culture-5 — agree-disagree, easy
- [ ] 52. T-116: 090-culture-6 — discuss-both-views, easy
- [ ] 53. T-117: 091-culture-7 — agree-disagree, easy
- [ ] 54. T-118: 092-culture-8 — agree-disagree, medium
- [ ] 55. T-119: 093-culture-9 — advantage-disadvantage, easy
- [ ] 56. T-120: 094-culture-10 — discuss-both-views, medium
- [ ] 57. T-121: 095-culture-11 — single-question, easy
- [ ] 58. T-122: 096-culture-12 — agree-disagree, easy
- [ ] 59. T-123: 097-culture-13 — discuss-both-views, easy
- [ ] 60. T-124: 098-culture-14 — discuss-both-views, medium
- [ ] 61. T-125: 099-culture-15 — agree-disagree, medium
- [ ] 62. T-126: 100-culture-16 — agree-disagree, easy
- [ ] 63. T-127: 101-culture-17 — agree-disagree, easy
- [ ] 64. T-128: 102-ageing-2 — positive-negative, easy
- [ ] 65. T-129: 103-ageing-3 — problem-solution, medium
- [ ] 66. T-130: 104-ageing-4 — problem-solution, medium
- [ ] 67. T-131: 105-ageing-5 — problem-solution, medium
- [ ] 68. T-132: 106-ageing-6 — advantage-disadvantage, easy

### Wave 3 — Task 2 essays batch 3 (32 todos, 8 SA × 4 essay parallel)

Sub-cats: 3.4 (8), 3.5 (17), 3.6 (7) — total 32 prompts
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 67-89)

- [ ] 69. T-133: 107-transport-1 — agree-disagree, easy
- [ ] 70. T-134: 108-transport-2 — single-question, medium
- [ ] 71. T-135: 109-transport-3 — agree-disagree, medium
- [ ] 72. T-136: 110-transport-4 — agree-disagree, hard
- [ ] 73. T-137: 111-transport-5 — advantage-disadvantage, medium
- [ ] 74. T-138: 112-transport-7 — two-questions, medium
- [ ] 75. T-139: 113-transport-8 — single-question, hard
- [ ] 76. T-140: 114-values-compare-1 — agree-disagree, medium
- [ ] 77. T-141: 115-values-compare-3 — discuss-both-views, easy
- [ ] 78. T-142: 116-values-compare-4 — agree-disagree, medium
- [ ] 79. T-143: 117-values-compare-5 — two-questions, easy
- [ ] 80. T-144: 118-values-compare-6 — discuss-both-views, medium
- [ ] 81. T-145: 119-values-compare-7 — agree-disagree, medium
- [ ] 82. T-146: 120-values-compare-8 — discuss-both-views, medium
- [ ] 83. T-147: 121-values-compare-9 — discuss-both-views, medium
- [ ] 84. T-148: 122-values-compare-10 — opinion, medium
- [ ] 85. T-149: 123-values-compare-11 — discuss-both-views, medium
- [ ] 86. T-150: 124-values-compare-12 — discuss-both-views, medium
- [ ] 87. T-151: 125-values-compare-13 — agree-disagree, medium
- [ ] 88. T-152: 126-values-compare-14 — discuss-both-views, medium
- [ ] 89. T-153: 127-values-compare-15 — advantage-disadvantage, medium
- [ ] 90. T-154: 128-values-compare-16 — two-questions, medium
- [ ] 91. T-155: 129-values-compare-17 — agree-disagree, easy
- [ ] 92. T-156: 130-social-phenomenon-1 — problem-solution, medium
- [ ] 93. T-157: 131-social-phenomenon-2 — single-question, easy
- [ ] 94. T-158: 132-social-phenomenon-4 — single-question, easy
- [ ] 95. T-159: 133-social-phenomenon-5 — single-question, easy
- [ ] 96. T-160: 134-social-phenomenon-6 — two-questions, medium
- [ ] 97. T-161: 135-social-phenomenon-7 — opinion, medium
- [ ] 98. T-162: 136-social-phenomenon-8 — problem-solution, medium
- [ ] 99. T-163: 137-social-phenomenon-9 — single-question, medium
- [ ] 100. T-164: 138-social-phenomenon-10 — two-questions, medium

### Wave 4 — Task 2 essays batch 4 (32 todos, 8 SA × 4 essay parallel)

Sub-cats: 3.6 (rest 8), 3.8 (3), 4.1 (3), 4.3 (1), 4.4 (4), 4.6 (1), 4.7 (2), 5.1 (7), 5.2 (3) — total 32 prompts
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 90-135)

- [ ] 101. T-165: 139-social-phenomenon-11 — advantage-disadvantage, medium
- [ ] 102. T-166: 140-social-phenomenon-12 — positive-negative, easy
- [ ] 103. T-167: 141-social-phenomenon-13 — positive-negative, easy
- [ ] 104. T-168: 142-social-phenomenon-14 — opinion, easy
- [ ] 105. T-169: 143-social-phenomenon-15 — positive-negative, easy
- [ ] 106. T-170: 144-life-change-2 — advantage-disadvantage, easy
- [ ] 107. T-171: 145-life-change-3 — advantage-disadvantage, medium
- [ ] 108. T-172: 146-life-change-4 — agree-disagree, medium
- [ ] 109. T-173: 147-animal-protection-2 — agree-disagree, medium
- [ ] 110. T-174: 148-animal-protection-3 — discuss-both-views, medium
- [ ] 111. T-175: 149-animal-protection-4 — agree-disagree, medium
- [ ] 112. T-176: 150-water-2 — agree-disagree, hard
- [ ] 113. T-177: 151-energy-3 — advantage-disadvantage, hard
- [ ] 114. T-178: 152-energy-4 — discuss-both-views, hard
- [ ] 115. T-179: 153-energy-5 — agree-disagree, medium
- [ ] 116. T-180: 154-energy-6 — opinion, medium
- [ ] 117. T-181: 155-consumption-2 — single-question, medium
- [ ] 118. T-182: 156-env-method-2 — discuss-both-views, medium
- [ ] 119. T-183: 157-env-method-3 — agree-disagree, medium
- [ ] 120. T-184: 158-technology-1 — agree-disagree, medium
- [ ] 121. T-185: 159-technology-2 — agree-disagree, medium
- [ ] 122. T-186: 160-technology-3 — agree-disagree, hard
- [ ] 123. T-187: 161-technology-4 — agree-disagree, medium
- [ ] 124. T-188: 162-technology-5 — discuss-both-views, medium
- [ ] 125. T-189: 163-technology-7 — single-question, medium
- [ ] 126. T-190: 164-technology-8 — agree-disagree, easy
- [ ] 127. T-191: 165-technology-9 — agree-disagree, hard
- [ ] 128. T-192: 166-technology-10 — agree-disagree, medium
- [ ] 129. T-193: 167-technology-11 — positive-negative, medium
- [ ] 130. T-194: 168-technology-12 — discuss-both-views, medium
- [ ] 131. T-195: 169-technology-13 — single-question, medium
- [ ] 132. T-196: 170-technology-14 — discuss-both-views, medium

### Wave 5 — Task 2 essays batch 5 (32 todos, 8 SA × 4 essay parallel)

Sub-cats: 5.2 (5), 6.1 (16), rest 6.1 (11) — total 32 prompts
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 131-151)

- [ ] 133. T-197: 171-health-2 — single-question, easy
- [ ] 134. T-198: 172-health-3 — agree-disagree, medium
- [ ] 135. T-199: 173-health-4 — problem-solution, medium
- [ ] 136. T-200: 174-health-5 — advantage-disadvantage, medium
- [ ] 137. T-201: 175-health-6 — agree-disagree, medium
- [ ] 138. T-202: 176-media-1 — agree-disagree, easy
- [ ] 139. T-203: 177-media-2 — discuss-both-views, medium
- [ ] 140. T-204: 178-media-3 — positive-negative, easy
- [ ] 141. T-205: 179-media-4 — advantage-disadvantage, medium
- [ ] 142. T-206: 180-media-5 — advantage-disadvantage, easy
- [ ] 143. T-207: 181-media-6 — agree-disagree, easy
- [ ] 144. T-208: 182-media-7 — agree-disagree, easy
- [ ] 145. T-209: 183-media-8 — discuss-both-views, easy
- [ ] 146. T-210: 184-media-9 — discuss-both-views, medium
- [ ] 147. T-211: 185-media-10 — agree-disagree, medium
- [ ] 148. T-212: 186-media-11 — discuss-both-views, easy
- [ ] 149. T-213: 187-media-13 — agree-disagree, medium
- [ ] 150. T-214: 188-media-14 — discuss-both-views, easy
- [ ] 151. T-215: 189-media-15 — discuss-both-views, easy
- [ ] 152. T-216: 190-media-16 — agree-disagree, easy
- [ ] 153. T-217: 191-media-17 — single-question, easy
- [ ] 154. T-218: 192-advertising-1 — discuss-both-views, medium
- [ ] 155. T-219: 193-advertising-3 — positive-negative, medium
- [ ] 156. T-220: 194-advertising-4 — discuss-both-views, medium
- [ ] 157. T-221: 195-advertising-5 — positive-negative, medium
- [ ] 158. T-222: 196-advertising-6 — single-question, easy
- [ ] 159. T-223: 197-advertising-7 — agree-disagree, easy
- [ ] 160. T-224: 198-advertising-8 — discuss-both-views, medium
- [ ] 161. T-225: 199-advertising-9 — agree-disagree, medium
- [ ] 162. T-226: 200-globalisation-1 — agree-disagree, hard
- [ ] 163. T-227: 201-globalisation-2 — positive-negative, easy
- [ ] 164. T-228: 202-globalisation-3 — agree-disagree, medium

### Wave 6 — Task 2 essays batch 6 (31 todos, 8 SA × 3-4 essay parallel)

Sub-cats: 8.1 (rest 9), 8.2 (22) — total 31 prompts
(Prompt enumeration per .omo/drafts/stage1c-prompts.md lines 160-193)

- [ ] 165. T-229: 203-globalisation-4 — positive-negative, easy
- [ ] 166. T-230: 204-globalisation-5 — discuss-both-views, hard
- [ ] 167. T-231: 205-globalisation-6 — discuss-both-views, medium
- [ ] 168. T-232: 206-globalisation-7 — agree-disagree, medium
- [ ] 169. T-233: 207-globalisation-9 — positive-negative, easy
- [ ] 170. T-234: 208-globalisation-10 — agree-disagree, hard
- [ ] 171. T-235: 209-globalisation-11 — agree-disagree, hard
- [ ] 172. T-236: 210-globalisation-12 — single-question, hard
- [ ] 173. T-237: 211-globalisation-13 — positive-negative, medium
- [ ] 174. T-238: 212-travel-1 — positive-negative, medium
- [ ] 175. T-239: 213-travel-3 — positive-negative, medium
- [ ] 176. T-240: 214-travel-4 — positive-negative, medium
- [ ] 177. T-241: 215-travel-5 — discuss-both-views, hard
- [ ] 178. T-242: 216-travel-6 — agree-disagree, hard
- [ ] 179. T-243: 217-travel-7 — agree-disagree, hard
- [ ] 180. T-244: 218-travel-8 — discuss-both-views, hard
- [ ] 181. T-245: 219-travel-9 — discuss-both-views, medium
- [ ] 182. T-246: 220-travel-10 — discuss-both-views, hard
- [ ] 183. T-247: 221-travel-11 — agree-disagree, hard
- [ ] 184. T-248: 222-travel-12 — discuss-both-views, hard
- [ ] 185. T-249: 223-travel-13 — agree-disagree, medium
- [ ] 186. T-250: 224-travel-14 — discuss-both-views, hard
- [ ] 187. T-251: 225-travel-15 — discuss-both-views, medium
- [ ] 188. T-252: 226-travel-16 — agree-disagree, hard
- [ ] 189. T-253: 227-travel-17 — opinion, medium
- [ ] 190. T-254: 228-travel-18 — two-questions, hard
- [ ] 191. T-255: 229-travel-19 — agree-disagree, hard
- [ ] 192. T-256: 230-travel-20 — discuss-both-views, medium
- [ ] 193. T-257: 231-travel-21 — discuss-both-views, hard
- [ ] 194. T-258: 232-travel-22 — discuss-both-views, hard
- [ ] 195. T-259: 233-travel-23 — agree-disagree, medium

### Wave 7 — Final verification (5 todos, sequential)

- [ ] 196. T-260: bulk verify all 246 essays + chip-distribution non-zero (G1+G4+G5)
  What to do: `bash scripts/verify-stage1b.sh docs/writing/` exit 0; `grep -c '^    <article data-task' docs/writing/index.html` returns 246; for each of 8 chips `grep -c 'data-type="<chip>"' docs/writing/index.html` returns ≥ 1; build a dedup set from `<meta name="prompt-source" content="...">` across all 246 essays → must be exactly 246 unique values (no duplicates, no Stage 1a/1b prompt-source omitted). If any check fails, ticket BLOCKED with diagnostic.
  Parallelization: Wave 7 (sequential) | Blocked by: T-259 | Blocks: T-261
  References: `scripts/verify-stage1b.sh` (post-T-065 patched); `docs/writing/index.html` (post-T-066 extended); all 246 essay HTML files
  Acceptance criteria (agent-executable): (a) `bash scripts/verify-stage1b.sh docs/writing/` exit 0; (b) `grep -c '^    <article data-task' docs/writing/index.html` returns 246; (c) `grep -roh 'data-type="[a-z-]*"' docs/writing/index.html | sort -u | wc -l` returns 8; (d) all 8 chips have ≥1 card
  QA scenarios: happy — all 246 essays PASS, 8 chips visible; failure — essay N fails AC-T2-1 (figure), subagent fixes via follow-up commit; chip distribution <1 for chip X → subagent adds follow-up essay to bring chip X ≥1
  Commit: N (no source change; this is a verification gate)

- [ ] 197. T-261: Playwright spot-check on 5 essays (one per chip + one rare chip like opinion) — visual + filter chip UI
  What to do: Playwright loads `https://meisijiya.github.io/IELTS/writing/`, clicks each of 8 chips, asserts ≥1 essay card visible per chip. Then loads 5 representative essays (one per chip type: agree-disagree / discuss-both-views / opinion (rare) / problem-solution / single-question), asserts: (1) `<h1>` renders, (2) essay body visible, (3) rubric section visible, (4) keywords `<code>` items rendered.
  Parallelization: Wave 7 (sequential) | Blocked by: T-260 | Blocks: T-262
  References: `docs/writing/index.html:1-342` (filter UI); `docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54` (essay structure)
  Acceptance criteria (agent-executable): (a) Playwright test exits 0; (b) screenshots saved to `docs/screenshots/09-stage1c-*.png` (8 chip screenshots + 5 essay screenshots = 13 total); (c) `ls docs/screenshots/09-stage1c-*.png | wc -l` returns 13
  QA scenarios: happy — 5 essays render, 8 chips filter correctly; failure — chip X shows "No matching essays" → chip-distribution gap, subagent surfaces to user
  Commit: N (verification gate)

- [ ] 198. T-262: visual-qa dual-oracle on full 246-essay corpus (G7)
  What to do: Run `/visual-qa` skill (or equivalent dual-oracle protocol) on the live site. 4 lanes: design-system (academic-minimal + reading-optimised palette preserved across 246 essays) / functional (filter UI, essay rendering, no JS errors) / CJK fidelity (Chinese rubric section reads cleanly, no clipping/overflow) / accessibility (semantic HTML, ARIA labels preserved, contrast OK). Output: per-lane verdict + blocking / non-blocking issue lists.
  Parallelization: Wave 7 (sequential) | Blocked by: T-261 | Blocks: T-263
  References: live `https://meisijiya.github.io/IELTS/writing/` (all 246 essays); `docs/assets/css/style.css` (academic-minimal theme); `.opencode/skills/visual-qa/SKILL.md` (skill contract)
  Acceptance criteria (agent-executable): (a) `/visual-qa` reports 0 blocking issues; (b) `≤3` non-blocking issues registered as Stage 2 debt (logged to `docs/visual-qa-debt.md`, not blocking ship); (c) if >0 blocking issues found, subagent fixes via follow-up commit + re-runs `/visual-qa` once; second-round blocking issues → BLOCKED ticket, surface to user
  QA scenarios: happy — 0 blocking + ≤3 non-blocking registered; failure — visual issue in essay X (e.g., rubric overflow) → subagent patches essay X + re-verifies
  Commit: N (or Y for follow-up fix commits if blocking issues found in 1 round)

- [ ] 199. T-263: ship-evidence-gate + /review-work 5-lane (G8 + G9)
  What to do: (1) ship-evidence-gate: scan diff for secrets (no API keys, tokens); assert commit message format `stage 1c(T-NNN): ...` on every essay commit; assert no `--no-verify` or force pushes; (2) /review-work 5-lane in parallel: Oracle x3 (goal-alignment / code-quality / security) + unspecified-high x2 (hands-on QA / context-mining). All 5 lanes must PASS or FIXED-then-PASS.
  Parallelization: Wave 7 (sequential) | Blocked by: T-262 | Blocks: T-264
  References: `git log --oneline | head -200` (Stage 1c commit chain); `.opencode/skills/ship-evidence-gate/SKILL.md` (skill contract); `/review-work` (5-lane orchestrator)
  Acceptance criteria (agent-executable): (a) `bash scripts/ship-evidence-gate.sh .` (or skill invocation) exit 0; (b) all 5 /review-work lanes report APPROVED; (c) `git log --oneline | wc -l` shows ≥ 200 commits since Stage 1b HEAD
  QA scenarios: happy — gate PASS, all 5 lanes APPROVED; failure — security finding (e.g., exposed key) → BLOCKED, subagent scrubs + re-runs
  Commit: N (verification gate)

- [ ] 200. T-264: HANDOFF-stage1c.md (mirror Stage 1a/1b format) + 3 handoff docs verified deleted
  What to do: Write `HANDOFF-stage1c.md` at repo root mirroring Stage 1a/1b format: Status line, Live URL, Final commit history, File inventory, Acceptance status table (5 Requirements × 16 Scenarios PASS), Open items, Suggested next stage skills. Commit message format `stage 1c(T-264): HANDOFF-stage1c.md`. Verify 3 handoff docs deleted per T-068 (`[ ! -f HANDOFF-stage1a.md ] && [ ! -f HANDOFF-stage1b.md ] && [ ! -f .opencode/handoffs/2026-08-15T154136.md ]` returns true). Update `.omo/boulder.json` to reflect stage1c complete.
  Parallelization: Wave 7 (sequential) | Blocked by: T-068, T-263 | Blocks: (ship)
  References: `HANDOFF-stage1b.md` (format precedent); `HANDOFF-stage1a.md` (format precedent); `.omo/specs/ielts-writing-site-stage1c.md` (5 Requirements × 16 Scenarios)
  Acceptance criteria (agent-executable): (a) `HANDOFF-stage1c.md` exists at repo root; (b) `git log --oneline | head -3` shows `stage 1c(T-264): HANDOFF-stage1c.md`; (c) `grep -c '^### Requirement:' HANDOFF-stage1c.md` returns ≥5; (d) 3 handoff docs absent
  QA scenarios: happy — handoff written, ship complete; failure — 3 handoff docs still present → T-068 not run, subagent BLOCKED
  Commit: Y | stage 1c(T-264): HANDOFF-stage1c.md + stage 1c ship

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [x] F1. Plan compliance audit — every todo has references + agent-executable acceptance criteria + happy+failure QA scenarios + commit; dependency matrix consistent; G0-G9 gates cover spec scenarios; 200 todos match the 191-prompt enumeration in `.omo/drafts/stage1c-prompts.md` (built-in: review during plan write).
- [ ] F2. Code quality review — verify script patch adheres to existing bash + python3 style; HTML essay template matches Stage 1a structure verbatim; commit messages consistent.
- [ ] F3. Real manual QA — Playwright loads live site, exercises 8 chip filters, opens 5 essays across chips, verifies rubric + keywords rendering, no console errors. (Per T-261.)
- [ ] F4. Scope fidelity — 246 essays on disk (55 Stage 1a/1b + 191 Stage 1c); 8-chip whitelist unchanged; 9 invariants unchanged; 7.1 音乐 sub-cat absent; HANDOFF-stage1a/b + .opencode/handoffs/* all absent.
- [ ] F5. Visual-qa dual-oracle — full 246-essay corpus design-system / functional / CJK fidelity / accessibility verdict. 0 blocking issues + ≤3 non-blocking issues registered. (Per T-262.)

## Commit strategy

- **Atomic 1-commit-per-essay** for essay todos (T-069..T-259 = 191 commits); commits push in batches per wave (32 + 32 + 32 + 32 + 32 + 31 = 191 commits total).
- **Wave-end push**: after each wave's essays commit locally, push all commits in one `git push origin main` to trigger Actions deploy with `cancel-in-progress: true` (existing workflow). Wait 60s before next wave push to let Actions complete.
- **Commit message format**: `stage 1c(T-NNN): <slug> — <one-line what>` (NNN starts at 065, continues from Stage 1b's T-064).
- **Foundation commits** (T-065..T-068): 4 separate atomic commits, pushed sequentially before Wave 1.
- **Final commits** (T-260..T-264): T-260/T-261/T-262/T-263 are no-commit verification (no source change); T-264 is the final HANDOFF commit.

## Success criteria

Stage 1c ships when ALL of the following are true:

1. `.omo/specs/ielts-writing-site-stage1c.md` is `EXPLORED` (5 Requirements × 16 Scenarios; machine assertion PASS).
2. `.omo/plans/stage1c.md` (this file) is Momus-approved.
3. `.omo/tickets/ielts-writing-site-stage1c/` contains 200 ticket files (4 foundation + 191 essay + 5 final).
4. `docs/writing/task2/` contains 233 essay HTML files (42 Stage 1a/1b + 191 Stage 1c).
5. `docs/writing/index.html` contains 246 `<article>` cards; 8 chips all ≥1; filter JS unchanged.
6. `bash scripts/verify-stage1b.sh docs/writing/` exits 0 (covers 9 invariants + AC-T2-1 no-figure + AC-T2-4 prompt-uniqueness + chip-distribution).
7. `.github/workflows/deploy.yml` deploy is green (latest run `conclusion: success`).
8. `https://meisijiya.github.io/IELTS/writing/` shows 246 essay cards; all 8 chip filters return ≥1 essay; Playwright spot-check on 5 essays PASS.
9. Visual-qa dual-oracle reports 0 blocking issues (≤3 non-blocking registered as Stage 2 debt).
10. `/review-work` 5-lane all APPROVED or FIXED-then-PASS.
11. `HANDOFF-stage1a.md`, `HANDOFF-stage1b.md`, `.opencode/handoffs/2026-08-15T154136.md` all deleted (committed in T-068).
12. `HANDOFF-stage1c.md` exists at repo root, mirrors Stage 1a/1b format, references all 5 spec Requirements as PASS.
13. `.omo/boulder.json` updated to reflect stage1c complete.
14. Repo HEAD on `main` is `stage 1c(T-264)` commit; ≥ 200 new commits since Stage 1b HEAD `307368a`.

Execution belongs to the worker session. The plan is **decision-complete**; the executor needs zero further interview.