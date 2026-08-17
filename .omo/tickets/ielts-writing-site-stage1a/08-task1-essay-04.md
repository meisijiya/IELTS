---
id: T-008
goal: Task 1 essay 04 (Dynamic bar — Australian men and women physical activity) renders with 三件套 + embedded chart.
files:
  - docs/writing/task1/04-bar-physical-activity.html
  - docs/assets/images/task1-charts/04-bar-physical-activity.png
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

Same structure as T-005. Source: `.omo/plans/stage1a.md` P4 row #04. Attributes `data-task="task1"`, `data-difficulty="medium"`, `data-type="dynamic-graph"`.

## Acceptance criteria

- [ ] File `docs/writing/task1/04-bar-physical-activity.html` exists with correct attributes and 三件套.
- [ ] Word count 170–190.
- [ ] Chart image extracted.
- [ ] Numbers in essay match chart image.

## Verification

- Same as T-005.

## Files in scope

- `docs/writing/task1/04-bar-physical-activity.html`.
- `docs/assets/images/task1-charts/04-bar-physical-activity.png`.

## Files out of scope

- Other Task 1 essays (T-005..T-007, T-009).

## BLOCKED condition

Same as T-005.