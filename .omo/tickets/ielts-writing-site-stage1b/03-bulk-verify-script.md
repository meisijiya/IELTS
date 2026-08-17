---
id: T-017
goal: Write scripts/verify-stage1b.sh enforcing 9 template invariants + 8-chip whitelist + RED/GREEN self-test for Stage 1b essay verification.
files:
  - scripts/verify-stage1b.sh
deps: [T-016, T-016b]
ac:
  - REQ-template-invariants-scenario-single-h1-single-main
  - REQ-template-invariants-scenario-article-data-attrs-present
  - REQ-template-invariants-scenario-keyword-list-5-to-10
  - REQ-template-invariants-scenario-word-count-band
  - REQ-task2-batch-coverage-scenario-task2-5-repeat-subcat-prompts-shipped
evidence: `bash scripts/verify-stage1b.sh docs/writing/` exits 0 on Stage 1a corpus; exits non-zero when run against a deliberately violated copy of a 1a essay (e.g., word count changed to 250).
size: M
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

A bash script that walks every HTML file under `docs/writing/task1/` and `docs/writing/task2/` and asserts:

1. **A2** Exactly one `<h1>` (`grep -c '<h1>'` returns 1).
2. **A3** Exactly one `<main>` (`grep -c '<main>'` returns 1).
3. **A4** `<article data-task="..." data-difficulty="..." data-type="...">` on a single line (regex).
4. **A7** Between 5 and 10 `<code>` inside the `<section class="keywords">…</section>` block.
5. **A-T1** For Task 1 essays only: `<img loading="lazy" decoding="async" alt="..." width=... height=...>` present + `<figcaption>` + `<img src>` resolves to existing PNG.
6. **A-T2** For Task 2 essays only: `data-type` value is one of the 8 valid chips (5 Stage 1a + 3 new from T-016b).
7. **Word count band**: tokenize the `<section class="essay">…</section>` body; Task 1 must be 170-190, Task 2 must be 270-290.

Script header documents the protocol. Script uses `bash` + `python3 -c '...'` blocks for regex assertions. Script exits 0 if all pass, non-zero with per-file error messages otherwise.

**RED/GREEN self-test**: Script also contains a self-test mode (`scripts/verify-stage1b.sh --self-test`) that copies a Stage 1a essay to a temp dir, injects a deliberate violation, asserts the script exits non-zero. Then removes violation, asserts exit 0. Documented in header.

## Acceptance criteria

- [ ] Script exists at `scripts/verify-stage1b.sh`.
- [ ] Script is executable (`chmod +x`).
- [ ] `bash scripts/verify-stage1b.sh docs/writing/` exits 0 on Stage 1a corpus.
- [ ] `bash scripts/verify-stage1b.sh --self-test` exits 0 (proves RED/GREEN cycle works).
- [ ] Commit message: `stage 1b(T-017): add bulk-verify script for Stage 1b essay invariants`.

## Verification

- [ ] All 5 AC above pass.
- [ ] Output: per-file PASS line, total summary at end, exit code 0.
- [ ] Self-test output shows RED (script detects violation) then GREEN (script passes clean copy).

## Files in scope

- `scripts/verify-stage1b.sh` (create).
- `scripts/` directory (create if absent).

## Files out of scope

- The 10 existing essay HTMLs (verified, not modified).
- The Writing index HTML (T-016b's domain).
- Workflow YAML (T-016's domain).

## BLOCKED condition

If `python3` is missing or `bash` is not GNU bash on the runner: surface to user; do not silently fallback.
