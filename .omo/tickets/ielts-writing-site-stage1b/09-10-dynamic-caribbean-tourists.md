---
id: T-023
goal: Task 1 essay — Dynamic line — Caribbean island visitors 2010-17 (slug 10-dynamic-caribbean-tourists) renders with full template + embedded chart extracted from docx.
files:
  - docs/writing/task1/10-dynamic-caribbean-tourists.html
  - docs/assets/images/task1-charts/10-dynamic-caribbean-tourists.png
deps: [T-018]
ac:
  - REQ-task1-batch-coverage-scenario-task1-remaining-chart-types-shipped
  - REQ-template-invariants-scenario-word-count-band
  - REQ-template-invariants-scenario-single-h1-single-main
  - REQ-chart-data-not-fabricated-scenario-figures-traceable
evidence: file exists at docs/writing/task1/10-dynamic-caribbean-tourists.html; chart PNG at docs/assets/images/task1-charts/10-dynamic-caribbean-tourists.png; bash scripts/verify-stage1b.sh docs/writing/task1/10-dynamic-caribbean-tourists.html exits 0; word count in [170, 190]; Actions deploy green.
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

Task 1 essay HTML page covering the chart question from `Task 1 冲刺(1).docx`:

- **Title**: Dynamic line — Caribbean island visitors 2010-17
- **Slug**: `10-dynamic-caribbean-tourists`
- **data-task**: task1
- **data-difficulty**: medium
- **data-type**: dynamic-graph

Subagent steps:

1. Extract chart PNG from `Task 1 冲刺(1).docx` via `python-docx` + `zipfile`.
2. Read numbers with `look_at` tool; document every fact in `## Chart data` section.
3. Draft 170–190 word 6-band-clean essay (4 paragraphs).
4. Write Chinese 1–2 paragraph rubric (TA/CC/LR/GRA).
5. Write 5–10 `<code>` keyword list.
6. Compose HTML copying `docs/writing/task1/05-mixed-graph.html` skeleton; swap content.
7. Save PNG to `docs/assets/images/task1-charts/10-dynamic-caribbean-tourists.png`.
8. Self-run `bash scripts/verify-stage1b.sh docs/writing/task1/10-dynamic-caribbean-tourists.html` → must exit 0.
9. Commit + push.

## Acceptance criteria

- [ ] File `docs/writing/task1/10-dynamic-caribbean-tourists.html` exists.
- [ ] File `docs/assets/images/task1-charts/10-dynamic-caribbean-tourists.png` exists.
- [ ] `<article>` carries `data-task="task1"`, `data-difficulty="medium"`, `data-type="dynamic-graph"` on same line.
- [ ] `<figure>` contains `<img loading="lazy" decoding="async" alt width height>` + `<figcaption>`.
- [ ] Word count of `<section class="essay">` body in [170, 190].
- [ ] Verify script exits 0 for this file.

## Verification

- [ ] `bash scripts/verify-stage1b.sh docs/writing/task1/10-dynamic-caribbean-tourists.html` exits 0.
- [ ] `git log --oneline | head -3` shows the new commit.
- [ ] `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` shows latest run success.

## Files in scope

- `docs/writing/task1/10-dynamic-caribbean-tourists.html` (create).
- `docs/assets/images/task1-charts/10-dynamic-caribbean-tourists.png` (create).

## Files out of scope

- Other Task 1 essay pages (siblings).
- The bulk-verify script (T-017).
- The Writing index (T-016b).
- Task 1 docx (read-only).

## BLOCKED condition

If `look_at` returns "unable to read" for any required chart number: mark `blocked`, write reason to `## Chart data` section, escalate to dispatcher. Do NOT fabricate.
