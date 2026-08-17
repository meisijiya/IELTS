---
id: T-002
goal: The site's CSS implements the academic-minimal + reading-optimised theme that all pages share.
files:
  - docs/assets/css/style.css
deps: []
ac:
  - REQ-pages-site-live-scenario-homepage-renders (CSS makes the homepage render correctly)
  - REQ-pages-site-live-scenario-essay-routes-200 (CSS makes essay pages readable)
evidence: docs/assets/css/style.css committed; visual inspection via T-015 screenshots.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

A single hand-written CSS file implementing the design system described in `.omo/plans/stage1a.md` P2: academic-minimal palette (white / ink `#1a1a1a` / green `#2d5a3d`), serif typography for titles and body with `Georgia` / 思源宋体 fallback, monospace meta, single-column reading layout (`max-width: 720px`, line-height `1.75`, font-size `18px`), responsive 2×2 → 1-column card grid, chip styles for the filter UI.

## Acceptance criteria

- [ ] File committed at `docs/assets/css/style.css`.
- [ ] Defines CSS custom properties for `--ink: #1a1a1a` and `--green: #2d5a3d`.
- [ ] `.essay` / `article` selector sets `max-width: 720px`, `line-height: 1.75`, `font-size: 18px`.
- [ ] `.card-grid` provides a 2×2 grid on `min-width: 720px` and 1 column below.
- [ ] `.chip` styles cover default / hover / `[aria-pressed="true"]` (active) / disabled states.
- [ ] No `@import` of any external URL (offline-safe).

## Verification

- [ ] No external CDN references: `grep -E "@import|fonts.googleapis|cdn\." docs/assets/css/style.css` returns nothing.
- [ ] Custom properties present: `grep -E "(--ink|--green)" docs/assets/css/style.css`.
- [ ] Final visual check happens at T-015 (Playwright screenshots).

## Files in scope

- `docs/assets/css/style.css` (create).

## Files out of scope

- Any HTML file (T-003, T-004, T-005..T-014).

## Notes

- Keep it small (target ≤250 lines). No preprocessor, no PostCSS, no Tailwind, no build step.
- Use system fonts only; do not embed webfonts.