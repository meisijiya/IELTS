# Feature: ielts-writing-site-stage1b

Stage 1b: expand the Stage-1a skeleton (5 Task 1 + 5 Task 2 = 10 essays) into the full 题库 — **8 new Task 1 essays** + **37 new Task 2 essays** (32 first-essays + 5 second-prompt-variants for the 4 sub-cats Stage 1a already covered, expanded to 5 (sub-cat × chip) cells since 1.1 is covered twice). Total Stage 1b = **45 new essays**; final corpus = **10 + 45 = 55 essay HTMLs** live at https://meisijiya.github.io/IELTS/.

References:

- Spec: `.omo/specs/ielts-writing-site-stage1b.md` (EXPLORED, 6 Requirements / 14 Scenarios)
- Plan: `.omo/plans/stage1b.md` (Momus v2 PASS)
- Source: `Task 1 冲刺(1).docx`, `作文真题储备（近五年）_可修改.docx`
- Stage 1a corpus: `docs/writing/task1/01..05*.html`, `docs/writing/task2/01..05*.html`

## Tickets

| NN | Title | id | deps | size | ac (REQ IDs) |
|----|-------|----|------|------|--------------|
| 01 | workflow-concurrency-flip | T-016 | [] | XS | 1 REQ refs |
| 02 | extend-writing-index-new-chips | T-016b | [T-016] | S | 2 REQ refs |
| 03 | bulk-verify-script | T-017 | [T-016, T-016b] | M | 5 REQ refs |
| 04 | pilot-task1-essay | T-018 | [T-016, T-016b, T-017] | M | 5 REQ refs |
| 05 | 06-process-rain-shadow-desert | T-019 | [T-018] | M | 4 REQ refs |
| 06 | 07-process-plastic-recycling | T-020 | [T-018] | M | 4 REQ refs |
| 07 | 08-process-cement-making | T-021 | [T-018] | M | 4 REQ refs |
| 08 | 09-mixed-library-survey | T-022 | [T-018] | M | 4 REQ refs |
| 09 | 10-dynamic-caribbean-tourists | T-023 | [T-018] | M | 4 REQ refs |
| 10 | 11-dynamic-melbourne-activities | T-024 | [T-018] | M | 4 REQ refs |
| 11 | 12-dynamic-asian-cities | T-025 | [T-018] | M | 4 REQ refs |
| 12 | 13-static-uk-school-spending | T-026 | [T-018] | M | 4 REQ refs |
| 27 | 06-26-env-solutions | T-027 | [T-018] | S | 5 REQ refs |
| 28 | 07-01-lang-learning | T-028 | [T-018] | S | 5 REQ refs |
| 29 | 08-04-education-target | T-029 | [T-018] | S | 5 REQ refs |
| 30 | 09-05-education-phenomenon | T-030 | [T-018] | S | 5 REQ refs |
| 31 | 10-06-job-choice | T-031 | [T-018] | S | 5 REQ refs |
| 32 | 11-07-personal-skill | T-032 | [T-018] | S | 5 REQ refs |
| 33 | 12-08-work-env | T-033 | [T-018] | S | 5 REQ refs |
| 34 | 13-09-job-types | T-034 | [T-018] | S | 5 REQ refs |
| 35 | 14-10-work-life-balance | T-035 | [T-018] | S | 5 REQ refs |
| 36 | 15-11-urbanisation | T-036 | [T-018] | S | 5 REQ refs |
| 37 | 16-12-culture | T-037 | [T-018] | S | 5 REQ refs |
| 38 | 17-13-ageing | T-038 | [T-018] | S | 5 REQ refs |
| 39 | 18-14-transport | T-039 | [T-018] | S | 5 REQ refs |
| 40 | 19-15-values-compare | T-040 | [T-018] | S | 5 REQ refs |
| 41 | 20-16-social-phenomenon | T-041 | [T-018] | S | 5 REQ refs |
| 42 | 21-17-privacy | T-042 | [T-018] | S | 5 REQ refs |
| 43 | 22-18-life-change | T-043 | [T-018] | S | 5 REQ refs |
| 44 | 23-19-gender | T-044 | [T-018] | S | 5 REQ refs |
| 45 | 24-20-civility | T-045 | [T-018] | S | 5 REQ refs |
| 46 | 25-21-animal-protection | T-046 | [T-018] | S | 5 REQ refs |
| 47 | 26-22-plastic | T-047 | [T-018] | S | 5 REQ refs |
| 48 | 27-23-water | T-048 | [T-018] | S | 5 REQ refs |
| 49 | 28-24-noise-pollution | T-049 | [T-018] | S | 5 REQ refs |
| 50 | 29-25-consumption-env | T-050 | [T-018] | S | 5 REQ refs |
| 51 | 30-02-qual-meaning | T-051 | [T-018] | S | 5 REQ refs |
| 52 | 31-03-education-method | T-052 | [T-018] | S | 5 REQ refs |
| 53 | 32-27-technology | T-053 | [T-018] | S | 5 REQ refs |
| 54 | 33-28-health | T-054 | [T-018] | S | 5 REQ refs |
| 55 | 34-29-media | T-055 | [T-018] | S | 5 REQ refs |
| 56 | 35-30-advertising | T-056 | [T-018] | S | 5 REQ refs |
| 57 | 36-31-globalisation | T-057 | [T-018] | S | 5 REQ refs |
| 58 | 37-32-travel | T-058 | [T-018] | S | 5 REQ refs |
| 13 | 1.1-single-question | T-059 | [T-018] | S | 5 REQ refs |
| 14 | 1.1-problem-solution | T-060 | [T-018] | S | 5 REQ refs |
| 15 | 1.2-advantage-disadvantage | T-061 | [T-018] | S | 5 REQ refs |
| 16 | 1.5-single-question | T-062 | [T-018] | S | 5 REQ refs |
| 17 | 4.4-problem-solution | T-063 | [T-018] | S | 5 REQ refs |
| 18 | bulk-deploy-verify | T-064 | [T-016, T-016b, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-027, T-028, T-029, T-030, T-031, T-032, T-033, T-034, T-035, T-036, T-037, T-038, T-039, T-040, T-041, T-042, T-043, T-044, T-045, T-046, T-047, T-048, T-049, T-050, T-051, T-052, T-053, T-054, T-055, T-056, T-057, T-058, T-059, T-060, T-061, T-062, T-063] | M | 3 REQ refs |

## Cross-feature edges

None — single feature. Internal `deps:` edges only.

## Status

`TICKETS_READY` — proceed to `/start-work`.

## Block / retry policy

If a Task 1 essay ticket hits BLOCKED on chart data extraction (multimodal returns "unable to read"): mark that ticket `blocked`, do not block other Task 1 tickets. Re-enter planning only if ≥3 of the 8 Task 1 tickets are blocked.

If a Task 2 essay ticket hits BLOCKED on prompt ambiguity: mark that ticket `blocked`, do not block siblings. Re-enter planning only if ≥3 of the 37 Task 2 tickets are blocked.

If T-016b (chip extension) is reverted, all 5 second-variant essays (T-059..T-063) become un-filterable; they need either reversion too or live as orphaned essays only reachable via direct URL.

If T-017 (verify script) is buggy and rejects all 45 essays, Wave 1–3 will halt; use `VERIFY_SKIP=1 bash scripts/verify-stage1b.sh ...` as emergency escape (mitigation per plan §Risk R10).
