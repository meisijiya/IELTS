---
id: T-016b
goal: Add 3 new Task 2 chips (problem-solution, advantage-disadvantage, single-question) to docs/writing/index.html so second-variant essays have a filterable data-type value.
files:
  - docs/writing/index.html
deps: [T-016]
ac:
  - REQ-task2-batch-coverage-scenario-task2-5-repeat-subcat-prompts-shipped
  - REQ-deploy-and-bulk-verify-scenario-filter-chips-populated
evidence: `grep -c 'data-value="problem-solution"' docs/writing/index.html` returns 1; same for `advantage-disadvantage`, `single-question`; knownTypes Set (line ~92) derives its values from `Array.prototype.map.call(typeRow.querySelectorAll('.chip'), ...)`, so adding the 3 buttons auto-syncs the Set.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1b
---

## What to build

Extend `docs/writing/index.html` to add 3 new Task 2 chips (`problem-solution`, `advantage-disadvantage`, `single-question`) to the type chip-row (lines 26-36). The `knownTypes` Set (line 92) is auto-derived from the chip buttons via `Array.prototype.map.call(typeRow.querySelectorAll('.chip'), function(c){return c.dataset.value;})` — so adding the 3 chip buttons automatically registers them in the Set. No JS edit needed.

The 5 existing chips (agree-disagree, discuss-both-views, positive-negative, opinion, two-questions) must remain unchanged.

## Acceptance criteria

- [ ] 3 new `<button>` elements added between line 36 and the closing `</div>` of the type chip-row (line 37).
- [ ] Each new chip uses `data-value="problem-solution"`, `data-value="advantage-disadvantage"`, `data-value="single-question"` (matching the kebab-case convention).
- [ ] Existing 5 chips untouched.
- [ ] Commit message: `stage 1b(T-016b): add 3 new Task 2 chips (problem-solution, advantage-disadvantage, single-question) for second-variants`.

## Verification

- [ ] `grep -c 'data-value="problem-solution"' docs/writing/index.html` returns 1.
- [ ] `grep -c 'data-value="advantage-disadvantage"' docs/writing/index.html` returns 1.
- [ ] `grep -c 'data-value="single-question"' docs/writing/index.html` returns 1.
- [ ] `grep -c '<button type="button" class="chip"' docs/writing/index.html` returns 11 (8 type + 4 difficulty - 1 "All" type = 11 chip buttons total; double-check by counting).
- [ ] After deploy: `curl -sL https://meisijiya.github.io/IELTS/writing/ | grep -c 'data-value="single-question"'` returns 1 (live verification).

## Files in scope

- `docs/writing/index.html` (edit lines 36-37, add 3 button lines).

## Files out of scope

- The 10 existing essay HTMLs (untouched).
- The deploy.yml (untouched, T-016).
- Any CSS file (chip styles already generic via `.chip` class).

## BLOCKED condition

None expected. If the existing `knownTypes` Set derivation is changed during a future edit to not derive from chip buttons, this ticket must extend the JS Set manually.
