---
id: T-001
goal: GitHub Pages is enabled on the repo and a deploy workflow is committed.
files:
  - .github/workflows/deploy.yml
deps: []
ac:
  - REQ-deploy-automation-scenario-auto-deploy-on-push
evidence: gh api repos/meisijiya/IELTS/pages returns a JSON object (not 404), and .github/workflows/deploy.yml is committed.
size: S
status: done
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

Enable GitHub Pages on `meisijiya/IELTS` with Source = GitHub Actions, then commit `.github/workflows/deploy.yml` so that any push to `main` auto-deploys the `docs/` directory.

## Acceptance criteria

- [ ] `gh api repos/meisijiya/IELTS/pages` returns a non-404 JSON object containing `build_type: workflow`.
- [ ] `.github/workflows/deploy.yml` exists, uses `actions/configure-pages@v4` + `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`, and the artifact path is `docs/`.
- [ ] A test commit triggering the workflow either succeeds (preferred) or fails with a clear "permission / Pages not enabled" error pointing at the Settings URL.

## Verification

- [ ] `gh api repos/meisijiya/IELTS/pages` (expect non-404).
- [ ] `gh workflow list` shows the deploy workflow.
- [ ] Push a no-op commit; `gh api repos/meisijiya/IELTS/pages/builds/latest` shows a `built` or `building` status.

## Files in scope

- `.github/workflows/deploy.yml` (create).

## Files out of scope

- Anything under `docs/` (T-002 onward).
- The two source docx files (read-only).

## Notes

- If `gh api -X POST repos/meisijiya/IELTS/pages -f build_type=workflow` returns 403 or 404, stop and hand off to user: open https://github.com/meisijiya/IELTS/settings/pages → Source = "GitHub Actions" → Save. Do not retry indefinitely.