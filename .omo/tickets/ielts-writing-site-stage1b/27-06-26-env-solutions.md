---
id: T-027
goal: Task 2 essay — sub-category 4.7 (slug 06-26-env-solutions) — first essay covering this previously-uncovered sub-category from 作文真题储备.
files:
  - docs/writing/task2/06-26-env-solutions.html
deps: [T-018]
ac:
  - REQ-task2-batch-coverage-scenario-task2-32-new-subcats-shipped
  - REQ-template-invariants-scenario-word-count-band
  - REQ-template-invariants-scenario-single-h1-single-main
  - REQ-template-invariants-scenario-article-data-attrs-present
  - REQ-template-invariants-scenario-keyword-list-5-to-10
evidence: file exists at docs/writing/task2/06-26-env-solutions.html; bash scripts/verify-stage1b.sh docs/writing/task2/06-26-env-solutions.html exits 0; word count in [270, 290]; `<article>` carries valid `data-type` from the 8-chip whitelist; theme = environment.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

Task 2 essay HTML page covering sub-category **4.7** (theme: environment) from `作文真题储备（近五年）_可修改.docx`. This is the **first** essay for this sub-category (not covered by Stage 1a).

Subagent steps:

1. Locate the sub-category in `作文真题储备（近五年）_可修改.docx` paragraphs.
2. Pick the most representative question prompt under this sub-category (numbered `#N`). The writer may add a 1-line rationale for the choice in the ticket's `## Prompt source` section.
3. Determine `data-type`: pick the best-matching chip from the **8-chip whitelist**: `{agree-disagree, discuss-both-views, positive-negative, opinion, two-questions, problem-solution, advantage-disadvantage, single-question}`. Chip choice driven by prompt structure (e.g., "do you agree" → `agree-disagree`; "discuss both views" → `discuss-both-views`; "advantages and disadvantages" → `advantage-disadvantage`; "what problems…how to solve" → `problem-solution`).
4. Draft 270–290 word 6-band-clean essay (intro → body 1 → body 2 → conclusion).
5. Write Chinese 1–2 paragraph rubric (TA/CC/LR/GRA).
6. Write 5–10 `<code>` keyword list.
7. Compose HTML copying `docs/writing/task2/01-agree-disagree-history-vs-business.html` skeleton; swap content.
8. Self-run `bash scripts/verify-stage1b.sh docs/writing/task2/06-26-env-solutions.html` → must exit 0.
9. Commit + push.

## Acceptance criteria

- [ ] File `docs/writing/task2/06-26-env-solutions.html` exists.
- [ ] `<article>` carries `data-task="task2"`, `data-difficulty` (writer's choice: easy/medium/hard), `data-type` (one of 8 valid chips) on same line.
- [ ] Word count of `<section class="essay">` body in [270, 290].
- [ ] 5–10 `<code>` items in keywords section.
- [ ] Verify script exits 0.

## Verification

- [ ] `bash scripts/verify-stage1b.sh docs/writing/task2/06-26-env-solutions.html` exits 0.
- [ ] `grep -E 'data-task="task2"' docs/writing/task2/06-26-env-solutions.html` returns 1.

## Files in scope

- `docs/writing/task2/06-26-env-solutions.html` (create).

## Files out of scope

- Other Task 2 essay pages (siblings).
- Task 2 docx (read-only).
- The bulk-verify script (T-017).
- The Writing index (T-016b).

## BLOCKED condition

If the prompt under sub-category 4.7 is genuinely ambiguous (no clear question structure), mark `blocked`, write reason, escalate. Do NOT fabricate a prompt.
