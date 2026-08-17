---
id: T-016
goal: Flip deploy.yml concurrency.cancel-in-progress to true so the 50-commit Stage 1b burst doesn't queue stale deploy runs.
files:
  - .github/workflows/deploy.yml
deps: []
ac:
  - REQ-workflow-concurrency-tuned-scenario-cancel-in-progress-true
evidence: `grep 'cancel-in-progress: true' .github/workflows/deploy.yml` returns 1; all 4 SHA-pinned action versions unchanged from Stage 1a commit 421546e.
size: XS
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

Edit `.github/workflows/deploy.yml` to set `concurrency.cancel-in-progress: true` (currently `false` in Stage 1a). Preserve all 4 SHA-pinned action versions. Add a one-line comment explaining the rationale.

## Acceptance criteria

- [ ] `concurrency.cancel-in-progress: true` in the YAML.
- [ ] All 4 SHA-pins preserved (checkout, configure-pages, upload-pages-artifact, deploy-pages).
- [ ] YAML parses (`gh workflow view deploy.yml` or `yamllint` succeeds).
- [ ] Commit message: `stage 1b(T-016): enable concurrency cancel-in-progress for burst deploys`.

## Verification

- [ ] `grep -n cancel-in-progress .github/workflows/deploy.yml` shows `true`.
- [ ] `grep -E 'uses: actions/[a-z-]+@[0-9a-f]{40}' .github/workflows/deploy.yml` shows 4 hits (SHAs).
- [ ] `git push origin main` triggers Actions run that succeeds (one-off verify).

## Files in scope

- `.github/workflows/deploy.yml` (edit).

## Files out of scope

- Any other file. Other Stage 1b commits are separate.

## BLOCKED condition

None expected; YAML edit is mechanical. If SHA verification reveals a pin was missed, fix in place and re-commit.
