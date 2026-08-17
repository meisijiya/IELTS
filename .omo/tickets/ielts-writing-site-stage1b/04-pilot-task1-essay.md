---
id: T-018
goal: First end-to-end Task 1 essay using the full protocol — chart extraction → multimodal read → essay → HTML → verify PASS → push → Actions deploy green.
files:
  - docs/writing/task1/06-process-rain-shadow-desert.html
  - docs/assets/images/task1-charts/06-process-rain-shadow-desert.png
deps: [T-016, T-016b, T-017]
ac:
  - REQ-task1-batch-coverage-scenario-task1-process-diagrams-shipped
  - REQ-template-invariants-scenario-word-count-band
  - REQ-template-invariants-scenario-single-h1-single-main
  - REQ-chart-data-not-fabricated-scenario-figures-traceable
  - REQ-chart-data-not-fabricated-scenario-blocked-not-guessed
evidence: `docs/writing/task1/06-process-rain-shadow-desert.html` exists; `bash scripts/verify-stage1b.sh docs/writing/task1/06-process-rain-shadow-desert.html` exits 0; chart PNG extracted to `docs/assets/images/task1-charts/`; Actions deploy run `conclusion: success`.
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

This is the **pilot** essay — validates the entire per-ticket pipeline before fanning out 7 more Task 1 subagents in parallel.

Subagent steps:

1. **Extract chart from docx**: Use `python-docx` to read `Task 1 冲刺(1).docx`; find the image relationship attached to the rain-shadow desert paragraph (line ~237). Extract the PNG via `zipfile` to `docs/assets/images/task1-charts/06-process-rain-shadow-desert.png`.
2. **Read chart numbers**: Use `look_at` tool on the extracted PNG. Goal: every step number, arrow direction, every word in every label.
3. **Document Chart data**: In ticket's `## Chart data` section, list every numeric / word fact used in the essay with a line ref to the PNG.
4. **Draft essay**: 170–190 words, 6-band-clean voice, 4 paragraphs (intro paraphrase → overview → body 1 → body 2 trend + anomaly).
5. **Write rubric**: 1–2 paragraphs Chinese TA/CC/LR/GRA note.
6. **Write keywords**: 5–10 `<code>` items in `<ul><li>` (each `<li><code>phrase</code> — 中文释义</li>`).
7. **Compose HTML**: Copy `docs/writing/task1/05-mixed-graph.html` (or any 1a Task 1 essay) as skeleton; swap content. Preserve template structure exactly.
8. **Self-run verify**: `bash scripts/verify-stage1b.sh docs/writing/task1/06-process-rain-shadow-desert.html` MUST exit 0.
9. **Commit + push**: `git add` the 2 files; commit `stage 1b(T-018): Task 1 pilot essay — process rain-shadow desert (first end-to-end)`; `git push origin main`.
10. **Wait for Actions deploy**: poll `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` until `conclusion: success` or 10 min timeout.

## Acceptance criteria

- [ ] File `docs/writing/task1/06-process-rain-shadow-desert.html` exists.
- [ ] File `docs/assets/images/task1-charts/06-process-rain-shadow-desert.png` exists and is non-zero size.
- [ ] Verify script exits 0 for this file.
- [ ] Actions deploy run `conclusion: success`.
- [ ] No `<figure>` content drift from Stage 1a template.
- [ ] No word-count band violation.

## Verification

- [ ] `ls -la docs/writing/task1/06-process-rain-shadow-desert.html docs/assets/images/task1-charts/06-process-rain-shadow-desert.png` shows both files.
- [ ] `bash scripts/verify-stage1b.sh docs/writing/task1/06-process-rain-shadow-desert.html` exits 0.
- [ ] `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` shows latest run `conclusion: success`.

## Files in scope

- `docs/writing/task1/06-process-rain-shadow-desert.html` (create).
- `docs/assets/images/task1-charts/06-process-rain-shadow-desert.png` (create).

## Files out of scope

- Other Task 1 essay pages (T-019..T-026).
- The bulk-verify script (T-017).
- The Writing index (T-016b).
- The workflow YAML (T-016).

## BLOCKED condition

If `look_at` returns "unable to read" for the rain-shadow chart (it's a complex multi-step diagram with arrows), mark this ticket `blocked` and **escalate to dispatcher** via `.omo/tickets/ielts-writing-site-stage1b/_dispatch.md`. Do NOT commit a fabricated essay. The dispatcher will either retry with a different multimodal prompt or swap this pilot for one of the chart-types T-019..T-026 (e.g., the simpler Caribbean line chart at T-023).
