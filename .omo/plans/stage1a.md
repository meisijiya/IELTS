# Stage 1a Plan — IELTS Writing Site Skeleton + 5 Sample Essays

## Goal

Ship the Stage-1a slice of the IELTS study site: enable GitHub Pages, deploy an academic-minimal site skeleton with a 4-module homepage (Writing only enabled), and publish 5 essay HTML pages (Task 1 × 5 types + Task 2 × 5 types) with working difficulty/type filtering. Acceptance lives in `.omo/specs/ielts-writing-site-stage1a.md` — finish when every Scenario there passes.

## Context

- Repo: `https://github.com/meisijiya/IELTS` (public, `main` branch only).
- `gh api repos/meisijiya/IELTS/pages` returns 404 — **Pages is not yet enabled**. First action is enabling Pages (Source: GitHub Actions) via `gh api -X POST repos/meisijiya/IELTS/pages -f build_type=workflow`, or via the repo settings UI if the API call is forbidden.
- Source content:
  - `Task 1 冲刺(1).docx` — 17 chart questions across Static / Dynamic / Mixed / Map / Process, 18 embedded chart images.
  - `作文真题储备（近五年）_可修改.docx` — Task 2 question bank, 47 sub-categories under 10 themes.
- Skill to load: `.opencode/skills/ielts-writing/SKILL.md` (SOP-B generation mode).
- Constraints from Goal: pure HTML + vanilla JS, no CDN, no framework, 6-band-clean essay voice, no fabricated chart data, no 代考-style content.

## Phases (Coarse Tickets — to-tickets will deepen)

### P1. Pages bootstrap (blocking all later steps)

- Attempt `gh api -X POST repos/meisijiya/IELTS/pages -f build_type=workflow` to enable Pages with Actions source.
- If API fails or returns a permission error, stop and tell the user to enable it manually at `https://github.com/meisijiya/IELTS/settings/pages` (Source: GitHub Actions), then continue.
- Write `.github/workflows/deploy.yml` using `actions/configure-pages@v4` + `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4` publishing `docs/`.

### P2. Design system + homepage

- Write `docs/assets/css/style.css` implementing the academic-minimal palette (white / ink `#1a1a1a` / green `#2d5a3d`), serif body, monospace meta, single-column `max-width:720px`, responsive 2×2 card grid.
- Write `docs/index.html` with the 4-module grid (Speaking / Writing / Reading / Listening); only Writing has a working anchor, the other three render visibly disabled with "Coming soon".
- Add `docs/favicon.svg` (minimal monogram) and `docs/404.html` (text-only redirect to homepage).

### P3. Writing module index + filter UI

- Write `docs/writing/index.html`:
  - Header explaining the two 题库 sources.
  - Difficulty chip row: `[All] [易] [中] [难]`.
  - Type chip row: one chip per supported type (`static-graph` / `dynamic-graph` / `mixed-graph` / `map` / `process` / `agree-disagree` / `discuss-both-views` / `positive-negative` / `opinion` / `two-questions`); multiple selection allowed.
  - Essay card list: each card wrapped in `<article data-task="task1"|"task2" data-difficulty="<v>" data-type="<v>">`; for now lists the 5 essay placeholders (filled in by P4/P5).
  - Empty-state copy: "No matching essays" when the filter produces zero results.
- Chips carry `data-value` attributes: `[易][data-value=easy]`, `[中][data-value=medium]`, `[难][data-value=hard]`, type chips `[static-graph][data-value=static-graph]` … . Difficulty chips are single-select; type chips allow multi-select with comma-separated values in the hash (`type=static-graph,mixed-graph`).
- Inline `<script>` (~50 lines) implementing:
  - Click on a chip toggles its `aria-pressed` state and re-runs the filter.
  - Filter sets `style.display = 'none'` on `<article>` cards whose `data-difficulty` / `data-type` does not match the active chip set; matching cards get `style.display = ''`.
  - Filter writes `#diff=<value>&type=<csv>` to `location.hash`.
  - On `DOMContentLoaded`, restore filter state from `location.hash` (parse `diff` / `type`, toggle chips accordingly).

### P4. Task 1 essays (5 pages, parallelisable)

For each of the 5 Task 1 questions below, write `docs/writing/task1/<NN>-<slug>.html`:

| # | Source 题号 | data-difficulty | data-type |
|---|---|---|---|
| 01 | table — universities ranked top 200 (Static) | easy | static-graph |
| 02 | pie — average percentages of nutrients in meals (Static) | easy | static-graph |
| 03 | bar — top ten countries for electricity (Static) | easy | static-graph |
| 04 | bar — Australian men and women physical activity (Dynamic by age group) | medium | dynamic-graph |
| 05 | mixed (Static/Dynamic combo) — pick the 1 mixed-graph sample in the题库 | medium | mixed-graph |

Each page's root element is `<article data-task="task1" data-difficulty="<v>" data-type="<v>">` matching the table. The page contains the 三件套: English essay (170–190 words, **numbers must be readable from the chart image**), Chinese 1–2 paragraph TA/CC/LR/GRA note, and a 5–10 item keyword/synonym list (`<code>`-wrapped).

For each chart:
1. Extract the image from `Task 1 冲刺(1).docx` with `python-docx` (images live in `doc.part.rels`).
2. Save the extracted image into `docs/assets/images/task1-charts/<slug>.png`.
3. Read the image with the multimodal reader to extract key numbers; if any number is unreadable, mark the essay BLOCKED and skip.

### P5. Task 2 essays (5 pages, parallelisable)

For each of the 5 Task 2 questions below (one per Task 2 type, all from distinct sub-categories), write `docs/writing/task2/<NN>-<slug>.html`:

| # | Sub-category | data-difficulty | data-type |
|---|---|---|---|
| 01 | 1.1 教育内容 — history vs business | easy | agree-disagree |
| 02 | 1.1 教育内容 — skills of employment vs academic | medium | discuss-both-views |
| 03 | 1.2 教育观念 — children freedom | medium | positive-negative |
| 04 | 1.5 师生话题 — teachers teaching morality | hard | opinion |
| 05 | 4.x 环境话题 (pick a two-question variant) | hard | two-questions |

Each page's root element is `<article data-task="task2" data-difficulty="<v>" data-type="<v>">` matching the table. The page contains the 三件套: English essay (270–290 words, 6-band-clean voice), Chinese 1–2 paragraph TA/CC/LR/GRA note, and 5–10 item keyword list. The data-difficulty / data-type mappings must match this table exactly.

### P6. Deploy + verify

- Commit and push to `main`. Wait for Actions.
- Run `gh api repos/meisijiya/IELTS/pages/builds/latest` to confirm `status: built`.
- `curl -I` the homepage, writing index, and each of the 5 essay URLs — all must be HTTP 200.
- Use Playwright to take 4 screenshots under `docs/screenshots/`:
  1. Homepage default.
  2. Writing index default (all 5 cards visible).
  3. Writing index after clicking `[易]` chip (verify URL hash + hidden cards).
  4. Any one essay page.

## Execution order & parallelism

- P1 must complete first (Pages must be enabled before any deploy can succeed).
- P2 and P3 can run in parallel after P1 (independent files).
- P4 and P5 can run in parallel after P3 (P3 only references P4/P5 by URL — a placeholder list is enough while P4/P5 are in progress, then P3 is touched up).
- P6 runs last, gated by completion of P2 + P3 + P4 + P5.

## Verification (mapped to spec Requirements)

| Requirement | Scenario | How verified |
|---|---|---|
| `REQ-pages-site-live` | `homepage-renders`, `essay-routes-200` | `curl -I` all URLs + DOM inspection of homepage |
| `REQ-essay-filter` | `single-chip-filter`, `combined-chip-filter`, `hash-restore-on-reload` | Playwright clicks + URL hash assertion + reload |
| `REQ-essay-content` | `task1-essay-coverage`, `task2-essay-coverage`, `chart-data-not-fabricated` | grep `data-difficulty` / `data-type` + word-count check + chart extraction trace |
| `REQ-deploy-automation` | `auto-deploy-on-push`, `failure-visible` | `gh api … /pages/builds/latest` + Actions run log |

## BLOCKED stop conditions

- Pages enable API fails AND user has not enabled Pages in the UI.
- ≥3 of the 5 Task 1 charts have unreadable key numbers.
- Any Task 2 question turns out to be ambiguous after re-reading.
- GitHub Actions deploy fails twice in a row.
- Context window saturated.

Stop report must include: completed phases list, BLOCKED items with reasons, current `pages/builds/latest` status, screenshot paths, and recommendation for next user action.

## Risks

- Pages enable via API may be rejected (repo-level setting requires UI). Mitigation: explicit user-handoff message with the exact Settings URL.
- Chart data extraction may fail on dense visuals (small numbers, overlapping legends). Mitigation: BLOCKED threshold is 3 essays, not 1, and the BLOCKED essay is skipped rather than guessed.
- Filter JS may regress to `display:none` without restoring on reload. Mitigation: Playwright reload screenshot is in P6.
- 5 Task 1 questions are not a balanced mix — the题库 has 18 images but only 17 题, so some types overlap (e.g. Static bar vs Static pie share `data-type=static-graph`). Plan: assign different `data-type` only where the题库 truly has a distinct type; otherwise tag multiple essays with the same type and rely on the题号 + difficulty chip for variety.

## References

- Spec: `.omo/specs/ielts-writing-site-stage1a.md`
- Skill: `.opencode/skills/ielts-writing/SKILL.md` (SOP-B)
- Source: `Task 1 冲刺(1).docx`, `作文真题储备（近五年）_可修改.docx`
- Deploy endpoint: `https://meisijiya.github.io/IELTS/`

## Out of scope (Stage 1a)

- Remaining 59 essay pages (Stage 1b).
- Non-Writing module content (still disabled).
- Custom domain, CNAME, SEO, sitemap, RSS.
- Comments, search backend.