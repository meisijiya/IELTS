---
id: T-010
goal: Task 2 essay 01 (agree-disagree — history vs business) renders with 三件套.
files:
  - docs/writing/task2/01-agree-disagree-history-vs-business.html
deps: [T-002, T-004]
ac:
  - REQ-essay-content-scenario-task2-essay-coverage
evidence: data-task/difficulty/type correct; wc -w 270–290; rubric + keywords present.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

A single Task 2 essay HTML page for sub-category 1.1 (education content), source: `.omo/plans/stage1a.md` P5 row #01. Attributes `data-task="task2"`, `data-difficulty="easy"`, `data-type="agree-disagree"`. Essay in 6-band-clean voice (basic topic vocab + occasional synonym swap, simple/complex mix without contrived errors, mechanical but coherent transitions). Word count 270–290.

Prompt text (from 题库): "Some people think that there could be more benefit to society if more people studied business than history. To what extent do you agree or disagree? (2025.1.18 / 2022.12.17)"

## Acceptance criteria

- [ ] File exists at `docs/writing/task2/01-agree-disagree-history-vs-business.html`.
- [ ] Root `<article>` carries `data-task="task2"`, `data-difficulty="easy"`, `data-type="agree-disagree"`.
- [ ] English essay body 270–290 words.
- [ ] Chinese TA/CC/LR/GRA note (1–2 paragraphs).
- [ ] Keyword list 5–10 items.
- [ ] Prompt text quoted near the top of the page.

## Verification

- `grep -E 'data-task="task2"|data-difficulty="easy"|data-type="agree-disagree"' docs/writing/task2/01-agree-disagree-history-vs-business.html` returns 3 hits.
- `python3` snippet counts essay body words → 270..290.
- `grep -c '<code>' docs/writing/task2/01-agree-disagree-history-vs-business.html` returns 5..10.

## Files in scope

- `docs/writing/task2/01-agree-disagree-history-vs-business.html` (create).

## Files out of scope

- `作文真题储备（近五年）_可修改.docx` (read-only).
- Other Task 2 essays (T-011..T-014).

## BLOCKED condition

If the prompt text is ambiguous (e.g. conflicting题目 between 2025.1.18 and 2022.12.17), mark BLOCKED with both versions quoted.