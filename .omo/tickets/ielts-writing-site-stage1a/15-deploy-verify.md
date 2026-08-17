---
id: T-015
goal: All Stage 1a acceptance scenarios are exercised end-to-end on the deployed site.
files:
  - docs/screenshots/01-homepage.png
  - docs/screenshots/02-writing-index-default.png
  - docs/screenshots/03-writing-index-filtered.png
  - docs/screenshots/04-essay-page.png
deps: [T-003, T-004, T-005, T-006, T-007, T-008, T-009, T-010, T-011, T-012, T-013, T-014]
ac:
  - REQ-pages-site-live-scenario-homepage-renders
  - REQ-pages-site-live-scenario-essay-routes-200
  - REQ-essay-filter-scenario-single-chip-filter
  - REQ-essay-filter-scenario-combined-chip-filter
  - REQ-essay-filter-scenario-hash-restore-on-reload
  - REQ-essay-content-scenario-task1-essay-coverage
  - REQ-essay-content-scenario-task2-essay-coverage
  - REQ-deploy-automation-scenario-auto-deploy-on-push
evidence: 4 screenshots under docs/screenshots/ + curl 200 log + Playwright assertions log + gh api build status.
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

Commit all Stage 1a deliverables, push to `main`, and verify the deploy + each spec scenario end-to-end.

Steps:

1. `git add .github docs .gitignore` (only those paths; nothing else).
2. Commit with a clear message (`stage 1a: site skeleton + 5 sample essays`).
3. Push to `main` (default behaviour).
4. Wait for Actions run to complete (poll `gh api repos/meisijiya/IELTS/pages/builds/latest` until `status: built` or timeout 5 min).
5. `curl -I` the homepage, writing index, and each of the 5 essay URLs — all must be HTTP 200. Log the output.
6. Use Playwright (Python or Node) to:
   - Open `https://meisijiya.github.io/IELTS/`, screenshot to `docs/screenshots/01-homepage.png`.
   - Open `https://meisijiya.github.io/IELTS/writing/`, screenshot to `docs/screenshots/02-writing-index-default.png` (5 cards visible).
   - Click `[易]` chip, assert URL hash equals `#diff=easy` and only `data-difficulty="easy"` cards remain visible (others have `display:none`), screenshot to `docs/screenshots/03-writing-index-filtered.png`.
   - Click `[All]` for difficulty + `[易]` + `[static-graph]` chips to set up a combined filter; assert URL hash equals `#diff=easy&type=static-graph`; reload the page and assert the same filter state is restored from the hash.
   - Open any one essay page, screenshot to `docs/screenshots/04-essay-page.png`.
7. Save Playwright assertions to `docs/screenshots/_assertions.log` for audit.

## Acceptance criteria

- [ ] All 4 screenshots exist and have non-zero size.
- [ ] `gh api repos/meisijiya/IELTS/pages/builds/latest` returns `status: built`.
- [ ] `curl -I` log shows HTTP 200 for `/`, `/writing/`, `/writing/task1/01-table-universities-ranked.html`, … (one line per URL, status code 200).
- [ ] Playwright assertion log confirms all 3 filter scenarios.
- [ ] No unrelated files were committed (`git diff --name-only HEAD~1 HEAD` lists only docs/ and .github/).

## Verification

- [ ] `ls -la docs/screenshots/` shows 4 PNGs + `_assertions.log`.
- [ ] `git log --oneline -1` shows the Stage 1a commit.
- [ ] `git diff --name-only HEAD~1 HEAD` shows only `.github/`, `docs/`, possibly `.gitignore`.

## Files in scope

- `docs/screenshots/*` (create via Playwright + curl output).
- One commit touching `.github/` + `docs/`.

## Files out of scope

- The two source docx files (never touched).
- `.gitignore` change is allowed only if a build artefact (e.g. `docs/screenshots/_assertions.log`) needs ignoring — preferable: don't add build artefacts at all.

## BLOCKED condition

If Actions deploy fails twice in a row: stop, surface the failed run URL and last build log to user, leave commits in place (so user can inspect). If any Playwright assertion fails: re-run once after a short delay; if still failing, surface to user.