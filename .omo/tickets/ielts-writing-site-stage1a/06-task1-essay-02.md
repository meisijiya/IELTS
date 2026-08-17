---
id: T-006
goal: Task 1 essay 02 (Static pie — average percentages of nutrients in meals) renders with 三件套 + embedded chart.
files:
  - docs/writing/task1/02-pie-meal-nutrients.html
  - docs/assets/images/task1-charts/02-pie-meal-nutrients.png
deps: [T-002, T-004]
ac:
  - REQ-essay-content-scenario-task1-essay-coverage
  - REQ-essay-content-scenario-chart-data-not-fabricated
evidence: essay page committed; data-task/difficulty/type attributes correct; wc -w 170–190; chart image extracted.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

Same structure as T-005, source question from `.omo/plans/stage1a.md` P4 row #02. Attributes `data-task="task1"`, `data-difficulty="easy"`, `data-type="static-graph"`.

## Acceptance criteria

- [ ] File `docs/writing/task1/02-pie-meal-nutrients.html` exists with correct attributes and 三件套.
- [ ] Word count 170–190.
- [ ] Chart image at `docs/assets/images/task1-charts/02-pie-meal-nutrients.png` exists.
- [ ] Numbers in essay match chart image.

## Verification

- Same grep / `wc -w` checks as T-005 against the new file.
- `test -f docs/assets/images/task1-charts/02-pie-meal-nutrients.png`.

## Files in scope

- `docs/writing/task1/02-pie-meal-nutrients.html`.
- `docs/assets/images/task1-charts/02-pie-meal-nutrients.png`.

## Files out of scope

- Other Task 1 essays (T-005, T-007, T-008, T-009).

## BLOCKED condition

Same as T-005.