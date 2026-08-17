---
id: T-014
goal: Task 2 essay 05 (two-questions — environment) renders with 三件套.
files:
  - docs/writing/task2/05-two-questions-environment.html
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

Same structure as T-010. Source: `.omo/plans/stage1a.md` P5 row #05. Attributes `data-task="task2"`, `data-difficulty="hard"`, `data-type="two-questions"`.

Pick a two-question prompt from the 4.x 环境子类别 (e.g. energy/water/noise/plastic). Confirm the prompt actually asks **two questions** ("What … and how …?") before tagging `data-type="two-questions"`; if no such prompt exists, mark BLOCKED.

## Acceptance criteria / Verification / Files / BLOCKED

Identical to T-010 with attributes and filename adjusted. BLOCKED additionally if题库 4.x has no two-question variant.