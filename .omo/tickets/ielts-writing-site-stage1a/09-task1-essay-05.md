---
id: T-009
goal: Task 1 essay 05 (Mixed graph) renders with 三件套 + embedded chart.
files:
  - docs/writing/task1/05-mixed-graph.html
  - docs/assets/images/task1-charts/05-mixed-graph.png
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

Pick the mixed-graph sample from `Task 1 冲刺(1).docx` (the题库 has 1 mixed-graph entry — see `.omo/plans/stage1a.md` P4 row #05). Attributes `data-task="task1"`, `data-difficulty="medium"`, `data-type="mixed-graph"`.

If the题库 has 0 mixed-graph questions, mark BLOCKED with reason and pick the closest substitute (a Dynamic bar that includes a secondary metric) while keeping `data-type="mixed-graph"` only if the source clearly combines two chart types.

## Acceptance criteria

- [ ] File `docs/writing/task1/05-mixed-graph.html` exists with correct attributes and 三件套.
- [ ] Word count 170–190.
- [ ] Chart image extracted.
- [ ] Numbers in essay match chart image.

## Verification

- Same as T-005.

## Files in scope

- `docs/writing/task1/05-mixed-graph.html`.
- `docs/assets/images/task1-charts/05-mixed-graph.png`.

## Files out of scope

- Other Task 1 essays (T-005..T-008).

## BLOCKED condition

Same as T-005. Plus: BLOCKED if题库 has no mixed-graph chart AND no Dynamic bar with a secondary metric.