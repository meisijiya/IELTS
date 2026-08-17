---
id: T-007
goal: Task 1 essay 03 (Static bar — top ten countries for electricity) renders with 三件套 + embedded chart.
files:
  - docs/writing/task1/03-bar-electricity.html
  - docs/assets/images/task1-charts/03-bar-electricity.png
deps: [T-002, T-004]
ac:
  - REQ-essay-content-scenario-task1-essay-coverage
  - REQ-essay-content-scenario-chart-data-not-fabricated
evidence: data-task/difficulty/type correct; wc -w 170–190; chart extracted.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

Same structure as T-005. Source: `.omo/plans/stage1a.md` P4 row #03. Attributes `data-task="task1"`, `data-difficulty="easy"`, `data-type="static-graph"`.

## Acceptance criteria

- [ ] File `docs/writing/task1/03-bar-electricity.html` exists with correct attributes and 三件套.
- [ ] Word count 170–190.
- [ ] Chart image extracted to `docs/assets/images/task1-charts/03-bar-electricity.png`.
- [ ] Numbers in essay match chart image.

## Verification

- Same as T-005 against the new file.

## Files in scope

- `docs/writing/task1/03-bar-electricity.html`.
- `docs/assets/images/task1-charts/03-bar-electricity.png`.

## Files out of scope

- Other Task 1 essays (T-005, T-006, T-008, T-009).

## BLOCKED condition

Same as T-005.