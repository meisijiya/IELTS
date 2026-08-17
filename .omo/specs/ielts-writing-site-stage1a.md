# IELTS Writing Site — Stage 1a Spec

Stage 1a of the IELTS 学习站点: ship a GitHub Pages skeleton + 5 sample essays (covering all Task 1/Task 2 question types) with difficulty/type filtering, so the user can verify the design on https://meisijiya.github.io/IELTS/ before Stage 1b (the remaining 59 essays).

## Objectives

- GitHub Pages skeleton is live at https://meisijiya.github.io/IELTS/ with a 4-module homepage (Speaking / Writing / Reading / Listening, only Writing enabled) and an academic-minimal + reading-optimised CSS theme.
- 5 essay HTML pages ship under `docs/writing/task1/` and `docs/writing/task2/`, covering every Task 1 type (static-graph / dynamic-graph / mixed-graph) and every Task 2 type (agree-disagree / discuss-both-views / positive-negative / opinion / two-questions) present in the source 题库.
- The Writing module index page exposes difficulty (`easy` / `medium` / `hard`) and type chips that filter the essay list, sync to URL hash, and survive page reload.

## Commands / API surface

- N/A

## Structure

- Homepage entry layer (4 cards, only Writing clickable).
- Writing module index (题库 description + difficulty/type filter bar + essay list).
- Essay detail pages (Task 1 + Task 2, each with题号, 三件套 content).
- Static assets layer (CSS, image assets, screenshot evidence).
- Deployment layer (GitHub Actions workflow publishing `docs/` to Pages).

## Code style

- Pure HTML + vanilla JS; no framework, no third-party CDN, no build step.
- Academic-minimal palette: white background, deep ink (`#1a1a1a`) body text, deep green accent (`#2d5a3d`) for links / chip-active / emphasis.
- Serif typography for titles and body (`Source Serif` / `Noto Serif SC` with `Georgia` / 思源宋体 fallback); monospace for meta tags and code.
- Single-column reading layout: `max-width: 720px`, line-height `1.75`, font-size `18px`, generous paragraph spacing.
- Responsive: mobile single-column, tablet/desktop 2×2 card grid.
- 6-band-clean essay voice: basic topic vocabulary with occasional synonym swaps, simple/complex sentence mix without contrived errors, mechanical but coherent transitions.

## Testing

- Every Pages URL returns HTTP 200 (homepage, writing index, 5 essay pages); verified by `curl -I`.
- GitHub Actions deploy log shows a successful run; verified by `gh api repos/meisijiya/IELTS/pages/builds/latest`.
- 4 visual screenshots saved under `docs/screenshots/`: homepage, writing index default, writing index after clicking a chip, any one essay page.
- Filter interaction validated: URL hash updates on chip click, non-matching `<article>` cards become `display:none`, reload restores the filter from `location.hash`.
- Word counts of all 5 essays verified in the `170–190` (Task 1) and `270–290` (Task 2) bands.

## Boundaries

In scope:

- Site skeleton + 5 essay HTML pages.
- Difficulty (3 levels) + type label schema.
- GitHub Actions deploy to Pages.
- Visual and interaction evidence.

Out of scope:

- Remaining 59 essays (Stage 1b).
- Non-Writing module content (still disabled).
- Custom domain / CNAME configuration.
- Comments, search backend, SEO, sitemap, RSS.

## Acceptance criteria

### Requirement: pages-site-live

The system SHALL ship the site live on GitHub Pages with all expected routes accessible.

#### Scenario: homepage-renders

- [ ] **WHEN** an unauthenticated browser visits `https://meisijiya.github.io/IELTS/`
- [ ] **THEN** the response is HTTP 200 and the HTML contains exactly 4 module cards, of which only the Writing card has a working anchor; the other three are visibly disabled with a "Coming soon" indicator.

#### Scenario: essay-routes-200

- [ ] **WHEN** the same browser visits `https://meisijiya.github.io/IELTS/writing/`, `…/writing/task1/<any>.html`, and `…/writing/task2/<any>.html`
- [ ] **THEN** every request returns HTTP 200 and renders its full content (no broken images, no console errors, no missing CSS).

### Requirement: essay-filter

The system SHALL provide working difficulty and type filters on the Writing index page.

#### Scenario: single-chip-filter

- [ ] **WHEN** the user clicks the `[易]` difficulty chip
- [ ] **THEN** the URL hash updates to `#diff=easy` and only essay cards whose `data-difficulty="easy"` remain visible; the rest get `display:none`.

#### Scenario: combined-chip-filter

- [ ] **WHEN** the user has `[易]` active and then clicks the `[static-graph]` type chip
- [ ] **THEN** only cards with both `data-difficulty="easy"` and `data-type="static-graph"` remain visible, and the URL hash equals `#diff=easy&type=static-graph`.

#### Scenario: hash-restore-on-reload

- [ ] **WHEN** the user reloads the page with `#diff=easy&type=static-graph` in the URL
- [ ] **THEN** after load, the matching chips show the active state and the same cards remain visible without the user clicking anything.

### Requirement: essay-content

The system SHALL produce 5 essays with full content, correct metadata, and on-band word counts.

#### Scenario: task1-essay-coverage

- [ ] **WHEN** the user opens any of the 5 Task 1 essay HTML pages under `docs/writing/task1/`
- [ ] **THEN** the `<article>` root carries `data-task="task1"`, `data-difficulty` and `data-type` attributes matching the planned mapping; the page contains the English essay (170–190 words), a Chinese 1–2 paragraph TA/CC/LR/GRA note, and a 5–10 item keyword list.

#### Scenario: task2-essay-coverage

- [ ] **WHEN** the user opens any of the 5 Task 2 essay HTML pages under `docs/writing/task2/`
- [ ] **THEN** the `<article>` root carries `data-task="task2"`, `data-difficulty` and `data-type` attributes matching the planned mapping; the page contains the English essay (270–290 words), a Chinese 1–2 paragraph TA/CC/LR/GRA note, and a 5–10 item keyword list.

#### Scenario: chart-data-not-fabricated

- [ ] **WHEN** the writing agent writes a Task 1 essay
- [ ] **THEN** every numeric figure referenced must be readable from the source chart image extracted from `Task 1 冲刺(1).docx`; if any required number is unreadable the essay is marked BLOCKED and skipped rather than guessed.

### Requirement: deploy-automation

The system SHALL deploy automatically on every push to `main` via GitHub Actions.

#### Scenario: auto-deploy-on-push

- [ ] **WHEN** any file under `docs/` is committed and pushed to `main`
- [ ] **THEN** within 5 minutes the GitHub Actions workflow `Deploy to GitHub Pages` succeeds and `gh api repos/meisijiya/IELTS/pages/builds/latest` returns `status: success`.

#### Scenario: failure-visible

- [ ] **WHEN** the workflow fails for any reason
- [ ] **THEN** the Actions run page shows a non-empty error log and the site keeps the previous successful deploy unchanged.