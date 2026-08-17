---
id: T-003
goal: The homepage renders 4 module cards with only Writing enabled.
files:
  - docs/index.html
  - docs/favicon.svg
  - docs/404.html
deps: [T-002]
ac:
  - REQ-pages-site-live-scenario-homepage-renders
evidence: curl https://meisijiya.github.io/IELTS/ returns 200 with HTML containing 4 cards; Playwright screenshot saved at docs/screenshots/01-homepage.png by T-015.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

`docs/index.html` is the site root. It links the shared CSS, shows the brand title `IELTS Study` and a short motto, then renders a 2×2 responsive grid of 4 cards: Speaking, Writing, Reading, Listening. Only Writing has a working `<a href="writing/">`; the other three render visibly disabled with `aria-disabled="true"` and a `Coming soon` badge.

Also add `docs/favicon.svg` (minimal monogram, single colour) and `docs/404.html` (text-only redirect message + link back to `/`).

## Acceptance criteria

- [ ] `docs/index.html` exists and links `assets/css/style.css`.
- [ ] The `<main>` (or equivalent) contains exactly 4 `.card` elements whose text content matches `Speaking`, `Writing`, `Reading`, `Listening` in order.
- [ ] Only the Writing card contains an `<a href="writing/">` with non-empty text; the other three have `aria-disabled="true"` and a `Coming soon` badge.
- [ ] `docs/favicon.svg` is a valid SVG (single file, no external refs).
- [ ] `docs/404.html` exists and links back to `/`.

## Verification

- [ ] `grep -c '<a href="writing/">' docs/index.html` returns `1` (only one).
- [ ] `grep -c 'aria-disabled="true"' docs/index.html` returns `3`.
- [ ] `grep -c 'Coming soon' docs/index.html` returns `≥3`.
- [ ] Final HTTP 200 check happens at T-015.

## Files in scope

- `docs/index.html` (create).
- `docs/favicon.svg` (create).
- `docs/404.html` (create).

## Files out of scope

- `docs/assets/css/style.css` (T-002).
- `docs/writing/**` (T-004 onward).