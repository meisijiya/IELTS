# IELTS Writing Site — Stage 1b Spec

Stage 1b of the IELTS 学习站点: expand the Stage 1a skeleton (5 sample essays) into the full 题库 by writing the remaining 8 Task 1 essays + 37 Task 2 essays (one per sub-category × 37 sub-categories; 5 already covered in Stage 1a get a second prompt variant to fill the type-chip empty state), total **~45 new essays**, deploy via existing GitHub Pages workflow, so the user has the complete 53-essay corpus (5 + 45) live at https://meisijiya.github.io/IELTS/.

## Objectives

- 8 Task 1 essays ship under `docs/writing/task1/`, covering the remaining question types in `Task 1 冲刺(1).docx` (3 process / diagram + 5 non-static-graph charts already classified). All 8 follow the same template / word band / data-attribute convention as Stage 1a.
- 37 Task 2 essays ship under `docs/writing/task2/`, one per `1.1`–`8.2` sub-category from `作文真题储备（近五年）_可修改.docx`. Stage 1a already covers **4 distinct sub-categories** (`1.1` ×2, `1.2`, `1.5`, `4.4`) using **5 essays** (since `1.1` is covered twice with two different chips). The 5 (sub-cat × chip) cells already shipped by Stage 1a each receive a **second prompt variant** as a different `data-type` chip drawn from **3 new Task 2 chips** added to the Writing index in `T-016b` (`problem-solution`, `advantage-disadvantage`, `single-question`); the other 32 sub-categories receive their first essay.
- Total Stage 1b: **~45 new essays** (8 + 32 + 5). After Stage 1b the site hosts **10 (Stage 1a) + 45 (Stage 1b) = 55 essay HTMLs** covering every Task 1 chart-type in the docx and every Task 2 sub-category in the docx.
- The Writing index filter chips (`process`, `map`, all 10 Task 2 types) populate with real essay cards (no more "No matching essays" empty states).
- One final bulk-verification pass: all 53 essay URLs return HTTP 200, word counts fall in band, Actions deploy succeeds.

## Commands / API surface

- N/A

## Structure

- New essay HTML pages under `docs/writing/task1/` (8 files, slugs `06-..13-<kebab>.html`) and `docs/writing/task2/` (37 files, slugs `06-..42-<kebab>.html`).
- New chart images for the 3 process diagrams under `docs/assets/images/task1-charts/` (extracted from docx with `python-docx` + `zipfile`).
- Bulk-verification script (small `scripts/verify-stage1b.sh` or inline `python3`) that scans every essay HTML and asserts: word-count band, single `<h1>`, single `<main>`, three `data-*` attributes on the `<article>` root, chart `<img>` present for Task 1.
- GitHub Actions workflow `.github/workflows/deploy.yml` flips `concurrency.cancel-in-progress` to `true` to absorb the high commit rate (Stage 1a had `false`).
- `docs/writing/index.html` extended with 3 new Task 2 chips (`problem-solution`, `advantage-disadvantage`, `single-question`) so second-variant essays have a filterable `data-type` value (T-016b).
- No new structural components beyond Stage 1a — every essay is a sibling to the existing 10.

## Code style

- Every essay HTML follows the **Stage 1a template exactly**: same `<nav>` / `<main>` / `<article data-task data-difficulty data-type>` / `<header><h1>` / section order. No drift.
- Task 1: English essay **170–190 words** (`<section class="essay">`), 1–2-paragraph Chinese TA/CC/LR/GRA rubric (`<section class="rubric">`), 5–10 `<code>` keyword items in `<ul><li>` (`<section class="keywords">`), `<figure>` with `<img loading="lazy" decoding="async" alt="..." width=... height=...>` and `<figcaption>`.
- Task 2: English essay **270–290 words**, same rubric + keyword structure, no `<figure>` (no chart to embed).
- One `<h1>` per page; `<h2>` only inside `<section class="essay">` for "Essay" / "Rubric" / "Keywords" headings if the section lacks an implicit title. No other `<h2>`-level narrative headings.
- Essay voice stays 6-band-clean — basic topic vocabulary with occasional synonym swaps, simple/complex sentence mix, mechanical transitions; no contrived errors meant to look "imperfect".
- Keyword `<code>` items: prefer low-frequency collocations, topic-specific phrasal verbs, and IELTS-band-7 vocabulary the candidate is unlikely to know by default. **Never** keyword-stuffing; 5–10 not 15+.
- Commit message format: `stage 1b(T-NNN): <slug> — <one-line what>`. One ticket per essay.

## Testing

- For each Task 1 essay: the writer subagent extracts the chart image, **runs `python3 -m ...` or reads with multimodal** to confirm every numeric figure in the essay is verifiable from the chart; if any figure is not readable, the ticket is marked **BLOCKED** and surfaced to the dispatcher — never guessed.
- Bulk-verification script (`scripts/verify-stage1b.sh`) sweeps all 53 essay HTMLs after Stage 1b push: asserts word count in band for each, asserts exactly one `<h1>` and one `<main>`, asserts `<article data-task data-difficulty data-type>` present in that order, asserts `<img>` present with `loading="lazy"` for Task 1, asserts 5–10 `<code>` inside the keywords section.
- Final deploy check: `gh api repos/meisijiya/IELTS/actions/runs?workflow=deploy.yml` shows the post-Stage-1b-push run succeeded.
- Spot-check by hand (manual QA via Playwright screenshot of one Stage 1b essay + one Task 1 diagram essay) to confirm visual parity with Stage 1a.

## Boundaries

In scope:

- 8 Task 1 essays + 37 Task 2 essays under `docs/writing/`.
- 3 new chart PNGs for the process diagrams in Task 1 docx.
- `concurrency.cancel-in-progress: true` in deploy workflow.
- A small bulk-verify shell script (no framework, just `grep`/`python3 -c`).
- Cosmetic Stage 1a cleanups if trivially cheap during a re-touch (redundant `<h2>Essay</h2>`, missing `<img width height>`, `<h2>` rubric header collapse); otherwise deferred.

Out of scope:

- Stage 1a essay rewrites (kept verbatim).
- New module surfaces (Reading / Speaking / Listening still `aria-disabled`).
- Visual-qa dual-oracle gate (deferred to Stage 1c).
- HTTPS upgrade / per-repo CNAME / SEO / sitemap / analytics.
- Multi-language UI (English-only).
- SOP-B per-paragraph Chinese explanation (Stage 1a's consolidated 1–2 paragraph rubric is the contract).
- Per-prompt-variant coverage for every Task 2 sub-category that already has one essay (1 essay per sub-category is the contract; a second variant is only added for the 5 sub-categories already shipped in Stage 1a, to fill the chip filter's empty-type state).

## Acceptance criteria

### Requirement: task1-batch-coverage

The system SHALL ship 8 new Task 1 essays covering the remaining chart types in `Task 1 冲刺(1).docx`.

#### Scenario: task1-process-diagrams-shipped

- [ ] **WHEN** the user opens any of `06-..08-<kebab>.html` (the 3 process / diagram essays)
- [ ] **THEN** the page renders with the Stage 1a template; word count is 170–190; `<figure>` contains `<img loading="lazy" decoding="async" alt width height>` and `<figcaption>`; the rubric + keywords sections are present; numeric figures in the essay are traceable to the extracted chart PNG.

#### Scenario: task1-remaining-chart-types-shipped

- [ ] **WHEN** the user opens any of `09-..13-<kebab>.html` (the 5 remaining chart-type essays: line chart / Asian countries / library survey / exports / mixed non-Stage-1a)
- [ ] **THEN** the page renders with the Stage 1a template; word count is 170–190; the rubric + keywords sections are present; numeric figures are traceable to the chart PNG.

### Requirement: task2-batch-coverage

The system SHALL ship 37 new Task 2 essays, one per sub-category `1.1`–`8.2`.

#### Scenario: task2-32-new-subcats-shipped

- [ ] **WHEN** the user opens any of the 32 Task 2 essay HTMLs covering sub-categories not in Stage 1a (1.1 / 1.3 / 1.7 / 1.8 / 2.1-2.5 / 3.1-3.10 / 4.1-4.6 / 5.1-5.2 / 6.1-6.2 / 7.1 / 8.1-8.2 etc.)
- [ ] **THEN** the page renders with the Stage 1a template; word count is 270–290; the rubric + keywords sections are present; `<article data-task="task2" data-difficulty="..." data-type="...">` attributes are present on the same line.

#### Scenario: task2-5-repeat-subcat-prompts-shipped

- [ ] **WHEN** the user opens any of the 5 Task 2 essay HTMLs covering sub-categories that already have a Stage 1a essay (1.2 / 1.4 / 1.5 / 1.6 / 4.7)
- [ ] **THEN** the page is a second prompt variant of that sub-category, with a different `data-type` chip than its Stage 1a sibling (filling the chip filter's empty-type state); word count is 270–290; template invariants hold.

### Requirement: template-invariants

The system SHALL enforce the Stage 1a 9-template-invariant contract on every new essay.

#### Scenario: single-h1-single-main

- [ ] **WHEN** `scripts/verify-stage1b.sh` scans all 45 new essay HTMLs
- [ ] **THEN** each file contains exactly one `<h1>` and exactly one `<main>`, otherwise the script exits non-zero.

#### Scenario: article-data-attrs-present

- [ ] **WHEN** the same script scans the `<article>` root of each essay
- [ ] **THEN** each `<article>` has all three attributes (`data-task`, `data-difficulty`, `data-type`) on the same opening tag line, otherwise the script exits non-zero.

#### Scenario: keyword-list-5-to-10

- [ ] **WHEN** the same script counts `<code>` elements inside the keywords section of each essay
- [ ] **THEN** each essay has between 5 and 10 `<code>` items, otherwise the script exits non-zero.

#### Scenario: word-count-band

- [ ] **WHEN** the same script tokenises the essay `<section>` body of each essay
- [ ] **THEN** Task 1 essays have 170–190 words, Task 2 essays have 270–290 words, otherwise the script exits non-zero.

### Requirement: chart-data-not-fabricated

The system SHALL NOT fabricate numeric figures for Task 1 essays.

#### Scenario: blocked-not-guessed

- [ ] **WHEN** a writer subagent cannot read a required number from the source chart image
- [ ] **THEN** the essay ticket is marked **BLOCKED** in the ticket file (`status: blocked` in frontmatter) and the dispatcher is notified; the essay is NOT committed.

#### Scenario: figures-traceable

- [ ] **WHEN** a writer subagent commits a Task 1 essay
- [ ] **THEN** every numeric figure in the essay body is documented in the ticket's `## Chart data` section with a line-number reference to the chart PNG; no figure is invented.

### Requirement: deploy-and-bulk-verify

The system SHALL deploy all Stage 1b essays via the existing GitHub Actions workflow and verify the result end-to-end.

#### Scenario: all-55-essay-urls-200

- [ ] **WHEN** the dispatcher curls `https://meisijiya.github.io/IELTS/writing/task1/<each>.html` (13 paths) and `…/writing/task2/<each>.html` (42 paths)
- [ ] **THEN** every request returns HTTP 200 and the body contains the expected `<h1>` title.

#### Scenario: filter-chips-populated

- [ ] **WHEN** the user clicks the `[process]` chip on `…/writing/` (and every other previously-empty chip)
- [ ] **THEN** at least one essay card remains visible; "No matching essays" empty state no longer appears for any chip that has coverage in the docx.

#### Scenario: final-deploy-success

- [ ] **WHEN** the last Stage 1b commit is pushed to `main`
- [ ] **THEN** within 10 minutes the `Deploy to GitHub Pages` Actions run completes successfully; the live site reflects all 53 essays; no failure log is shown.

### Requirement: workflow-concurrency-tuned

The system SHALL tune the GitHub Actions workflow for the high Stage 1b commit rate.

#### Scenario: cancel-in-progress-true

- [ ] **WHEN** the dispatcher inspects `.github/workflows/deploy.yml`
- [ ] **THEN** the `concurrency` block has `cancel-in-progress: true` (Stage 1a had `false`); this absorbs bursts of commit pushes without queueing stale runs.