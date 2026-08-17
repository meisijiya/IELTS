---
id: T-013
goal: Task 2 essay 04 (opinion — teachers teaching morality) renders with 三件套.
files:
  - docs/writing/task2/04-opinion-teachers-morality.html
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

Same structure as T-010. Source: `.omo/plans/stage1a.md` P5 row #04. Attributes `data-task="task2"`, `data-difficulty="hard"`, `data-type="opinion"`.

Prompt: "Some people believe teachers should teach students to judge what is right or wrong and to behave well. Others say teachers should only teach students academic subjects. Discuss both views and give your opinion. (2025.4.26)"

(Despite the prompt wording starting with "Discuss both views", the题库 marks this as sub-category 1.5 师生话题 with opinion倾向; we tag `data-type="opinion"` per the plan mapping. If the prompt wording feels ambiguous after re-reading, mark BLOCKED.)

## Acceptance criteria / Verification / Files / BLOCKED

Identical to T-010 with attributes and filename adjusted.