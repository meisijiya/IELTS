# Feature: ielts-writing-site-stage1a

Stage 1a of the IELTS 学习站点: ship a GitHub Pages skeleton + 5 sample essays (covering every Task 1/Task 2 type present in the题库) with a working difficulty/type filter, so the user can validate the design on https://meisijiya.github.io/IELTS/ before Stage 1b (the remaining 59 essays).

References:

- Spec: `.omo/specs/ielts-writing-site-stage1a.md` (EXPLORED)
- Plan: `.omo/plans/stage1a.md` (Momus PASS, 3 spec-asserted behaviors made explicit)
- Skill: `.opencode/skills/ielts-writing/SKILL.md` (SOP-B)
- Source: `Task 1 冲刺(1).docx`, `作文真题储备（近五年）_可修改.docx`

## Tickets

| NN | Title | id | deps | size | ac (REQ IDs) |
|----|-------|----|------|------|--------------|
| 01 | pages-bootstrap | T-001 | — | S | REQ-deploy-automation-scenario-auto-deploy-on-push |
| 02 | design-system | T-002 | — | S | REQ-pages-site-live (CSS supports both scenarios) |
| 03 | homepage | T-003 | T-002 | S | REQ-pages-site-live-scenario-homepage-renders |
| 04 | writing-index | T-004 | T-002 | M | REQ-essay-filter (all 3 scenarios) |
| 05 | task1-essay-01 | T-005 | T-002, T-004 | S | REQ-essay-content-scenario-task1-essay-coverage, REQ-essay-content-scenario-chart-data-not-fabricated |
| 06 | task1-essay-02 | T-006 | T-002, T-004 | S | same as 05 |
| 07 | task1-essay-03 | T-007 | T-002, T-004 | S | same as 05 |
| 08 | task1-essay-04 | T-008 | T-002, T-004 | S | same as 05 |
| 09 | task1-essay-05 | T-009 | T-002, T-004 | S | same as 05 |
| 10 | task2-essay-01 | T-010 | T-002, T-004 | S | REQ-essay-content-scenario-task2-essay-coverage |
| 11 | task2-essay-02 | T-011 | T-002, T-004 | S | same as 10 |
| 12 | task2-essay-03 | T-012 | T-002, T-004 | S | same as 10 |
| 13 | task2-essay-04 | T-013 | T-002, T-004 | S | same as 10 |
| 14 | task2-essay-05 | T-014 | T-002, T-004 | S | same as 10 |
| 15 | deploy-verify | T-015 | T-003, T-004, T-005..T-014 | M | REQ-pages-site-live (both), REQ-essay-filter (all 3), REQ-essay-content (all 3), REQ-deploy-automation (both) |

## Cross-feature edges

None — single feature. Internal `deps:` edges only.

## Status

`TICKETS_READY` — proceed to `/start-work`.

## Block / retry policy

If a Task 1 essay ticket hits BLOCKED on chart data extraction: mark that ticket `blocked`, do not block other Task 1 tickets. Re-enter planning only if ≥3 of the 5 Task 1 tickets are blocked.

If a Task 2 essay ticket hits BLOCKED on question ambiguity: mark that ticket `blocked`, do not block siblings. Re-enter planning only if ≥3 of the 5 Task 2 tickets are blocked.

If T-001 (Pages enable) fails via `gh api`: stop the whole feature, hand off to user with the Settings URL.