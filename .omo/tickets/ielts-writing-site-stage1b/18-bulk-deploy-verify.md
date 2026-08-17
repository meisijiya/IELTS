---
id: T-064
goal: All Stage 1b acceptance scenarios exercised end-to-end on the deployed site — curl all 55 essay URLs return 200, filter chips populate, Actions deploy green, Playwright spot-check screenshots saved.
files:
  - docs/screenshots/05-task1-process-essay.png
  - docs/screenshots/06-task2-second-variant.png
  - docs/screenshots/07-filter-chip-process.png
  - docs/screenshots/08-filter-chip-problem-solution.png
  - docs/screenshots/_assertions-stage1b.log
deps: [T-016, T-016b, T-017, T-018, T-019, T-020, T-021, T-022, T-023, T-024, T-025, T-026, T-027, T-028, T-029, T-030, T-031, T-032, T-033, T-034, T-035, T-036, T-037, T-038, T-039, T-040, T-041, T-042, T-043, T-044, T-045, T-046, T-047, T-048, T-049, T-050, T-051, T-052, T-053, T-054, T-055, T-056, T-057, T-058, T-059, T-060, T-061, T-062, T-063]
ac:
  - REQ-deploy-and-bulk-verify-scenario-all-55-essay-urls-200
  - REQ-deploy-and-bulk-verify-scenario-filter-chips-populated
  - REQ-deploy-and-bulk-verify-scenario-final-deploy-success
evidence: 4 Playwright screenshots + assertions log + curl 200 log for 55 URLs + gh api run success.
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

End-to-end verification of Stage 1b deploy. The dispatcher (or this subagent) runs after all 50 prior tickets are pushed.

Steps:

1. **git log inspection**: `git log --oneline | head -50` — confirm ~50 Stage 1b commits present.
2. **curl all 55 essay URLs** (10 from Stage 1a + 45 new):
   - 5 Stage 1a Task 1 + 8 Stage 1b Task 1 = 13 Task 1 URLs
   - 5 Stage 1a Task 2 + 37 Stage 1b Task 2 = 42 Task 2 URLs
   - Plus homepage `/` and writing index `/writing/`
   - Each must return HTTP 200; body contains expected `<h1>` title.
3. **Bulk verify**: `bash scripts/verify-stage1b.sh docs/writing/` exits 0 (validates all 55 essays).
4. **Actions status**: `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` shows latest run `conclusion: success`.
5. **Playwright spot-check** (save 4 screenshots):
   - Open `https://meisijiya.github.io/IELTS/writing/task1/06-process-rain-shadow-desert.html` → screenshot `docs/screenshots/05-task1-process-essay.png`.
   - Open `https://meisijiya.github.io/IELTS/writing/task2/38-1-1-second-variant.html` (or whichever second-variant slug) → screenshot `docs/screenshots/06-task2-second-variant.png`.
   - On `/writing/`, click `[process]` chip → assert ≥1 essay card visible, screenshot `docs/screenshots/07-filter-chip-process.png`.
   - On `/writing/`, click `[problem-solution]` chip → assert ≥1 essay card visible, screenshot `docs/screenshots/08-filter-chip-problem-solution.png`.
6. **Save assertions log**: `docs/screenshots/_assertions-stage1b.log` containing all curl status codes + Playwright assertions.
7. **Commit + push**: the screenshots + log; final deploy is canonical.

## Acceptance criteria

- [ ] All 4 screenshots exist and have non-zero size.
- [ ] Curl log shows 55 HTTP 200 + 1 homepage 200 + 1 writing index 200 = 57 total 200 responses.
- [ ] `bash scripts/verify-stage1b.sh docs/writing/` exits 0.
- [ ] `gh api .../actions/runs?workflow=deploy.yml` shows latest run `conclusion: success`.
- [ ] Playwright assertion log confirms filter chips `[process]`, `[problem-solution]`, `[advantage-disadvantage]`, `[single-question]` each show ≥1 essay card.
- [ ] No unrelated files committed.

## Verification

- [ ] `ls -la docs/screenshots/` shows 8 PNGs (4 from Stage 1a + 4 new) + 2 log files.
- [ ] `git log --oneline | head -50` shows ~50 Stage 1b commits.
- [ ] Final Actions deploy success.

## Files in scope

- `docs/screenshots/05..08-*.png` (create via Playwright).
- `docs/screenshots/_assertions-stage1b.log` (create).
- One final commit touching `docs/screenshots/`.

## Files out of scope

- The 50 Stage 1b essay files (already committed).
- The source docx files (read-only).
- Any Stage 1a file.

## BLOCKED condition

If Actions deploy fails twice in a row: stop, surface failed run URL + log to user, leave commits in place. If any Playwright assertion fails: re-run once after 30s delay; if still failing, surface to user. If verify script exits non-zero: identify the offending file(s), attempt fix, re-run; if not fixable in 2 attempts, surface.
