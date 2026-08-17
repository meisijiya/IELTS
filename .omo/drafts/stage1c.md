---
slug: stage1c
status: drafting
intent: clear
review_required: false
pending-action: write .omo/plans/stage1c.md
approach: <fill: the approach you intend to plan>
---

# Draft: stage1c

## Components (topology ledger)
<!-- Lock the SHAPE before depth. One row per top-level component that can succeed or fail independently. -->
<!-- id | outcome (one line) | status: active|deferred | evidence path -->

| id | outcome (one line) | status | evidence path |
|---|---|---|---|
| C1 | **Essay corpus**: 191 new Task 2 essay HTML files in `docs/writing/task2/<NN>-<slug>.html` (NN from 43..233), one per unused prompt in 作文真题储备 docx, excluding `7.1 音乐` (1 prompt) | active | spec:essay-coverage-191 |
| C2 | **Index extension**: `docs/writing/index.html` extended from 55 → 246 `<article>` cards; chip filter logic preserved | active | spec:index-extended-to-246 |
| C3 | **Verify script**: `scripts/verify-stage1b.sh` exit 0 on 246 essay corpus (likely no-op; 9 invariants + 8-chip whitelist + 270-290 band already cover Task 2) | active | spec:template-invariants-9 |
| C4 | **Handoff cleanup**: delete `HANDOFF-stage1a.md`, `HANDOFF-stage1b.md`, `.opencode/handoffs/2026-08-15T154136.md` (spec approved → run before plan review) | active | spec:handoff-cleanup |

## Open assumptions (announced defaults)
<!-- Record any default you adopt instead of asking, so the user can veto it at the gate. -->
<!-- assumption | adopted default | rationale | reversible? -->

| assumption | adopted default | rationale | reversible? |
|---|---|---|---|
| Wave size | **32 essays/wave** (8 SA × 4 essay, matching Stage 1b SA-2a..SA-2h pattern) | Stage 1b precedent: 8 parallel subagents × 4 essay = 32; works at this scale without context exhaustion (Stage 1b R3 risk) | yes — wave size is internal |
| Wave count | **6 waves** (191 ÷ 32 ≈ 6) | 191 essays / 32 per wave = ~6 waves; Wave 6 will have ~7 essays if some sub-cats are full | yes |
| Per-essay atomic commit | 1 commit / essay, format `stage 1c(T-NNN): <slug> — <one-line what>` (T-065..T-255) | Stage 1a/1b 9 invariants require atomic commits; T-NNN continues from Stage 1b's T-064 | yes (squash at end if needed) |
| Chip selection | Prompt's question word → chip (e.g., "To what extent do you agree" → `agree-disagree`; "Discuss both views" → `discuss-both-views`) | Stage 1a/1b mapping: each prompt's question word determines chip deterministically | yes (single chip per essay) |
| Wave parallelism | Max 8 subagents per wave | Stage 1b peak fan-out was 8; OMO harness supports this | yes |
| Subagent work-per-essay | 4 essay / SA (Task 2 only, text-only, no chart data) | Stage 1b SA-2a..SA-2h SA model | yes |
| Sub-cats with >4 prompts | Split across multiple SA (e.g., 8.2 with 23 prompts → 6 SA in one wave); sub-cats with 1 prompt get grouped | 8.2=23, 3.5=17, 6.1=17, 3.2=17, 5.1=14, 8.1=13 are large sub-cats; need weighted assignment | yes |
| Index card generation | Python script reads each new essay's `<article data-task data-difficulty data-type>` + `<h1>` title and emits `<article>` cards (Stage 1b T-064a precedent) | Already proven at Stage 1b T-064a (extended 10 → 55 cards) | yes |
| 8-chip whitelist | UNCHANGED from Stage 1b T-016b (agree-disagree / discuss-both-views / positive-negative / opinion / two-questions / problem-solution / advantage-disadvantage / single-question) | Stage 1b 已 ship; no need to extend | yes (but constrained by Stage 1b) |
| `7.1 音乐` sub-cat | SKIP (1 prompt) — Stage 1b dropped; user choice "完整 OMO + 191 篇" also excludes 7.1 | User chose option 1: 完整 OMO + 191 篇分 wave (不含 7.1) | yes (can add later) |
| Handoff delete order | Run after spec EXPLORED, before plan review | User said "spec 写完再删"; delete is low-risk, gitignored/rm-able | yes |
| Verify script patch | NO patches needed unless a new essay triggers a previously-unseen invariant | Existing 9 invariants + 8-chip whitelist + 270-290 band fully cover Stage 1c | yes |
| Visual-qa dual-oracle gate | **REQUIRED in Wave 7 final** (user selected "全量必做") — visual-qa skill dual-oracle pass over 246 essay corpus to catch design system / accessibility issues | User explicitly chose full visual-qa coverage | yes (1 final-verifier ticket added) |
| Wave count (revised) | 6 essay waves + 1 final wave (Wave 7 = bulk verify + visual-qa dual-oracle + ship-evidence-gate + HANDOFF-stage1c.md) | Wave 7 added for visual-qa dual-oracle pass | yes |

## Findings (cited - path:lines)

- `.omo/specs/ielts-writing-site-stage1c.md:1` — Spec EXPLORED, 5 Requirements × 16 Scenarios, machine assertion PASS
- `.omo/specs/ielts-writing-site-stage1b.md:1-157` — Stage 1b spec precedent (6 Requirements, 14 Scenarios, 9 invariants, atomic commit, wave model)
- `.omo/plans/stage1b.md:1-401` — Stage 1b plan v2: 50 tickets, 4 waves + final, 8 SA × 4 essay Task 2 model, 32 essays/wave
- `Task 1 冲刺(1).docx` → 13 Task 1 prompts (Stage 1c OUT OF SCOPE, all already covered)
- `作文真题储备（近五年）_可修改.docx` → **234 Task 2 prompts across 37 sub-cats**
- `作文真题储备（近五年）_可修改.docx` sub-cat prompt distribution (count):
  - 1.1=7, 1.2=10, 1.3=1, 1.4=3, 1.5=2, 1.6=7, 1.7=3, 1.8=3
  - 2.1=6, 2.2=5, 2.3=4, 2.4=1, 2.5=1
  - 3.1=9, 3.2=17, 3.3=6, 3.4=8, 3.5=17, 3.6=15, 3.7=1, 3.8=4, 3.9=1, 3.10=1
  - 4.1=4, 4.2=1, 4.3=2, 4.4=6, 4.5=1, 4.6=2, 4.7=3
  - 5.1=14, 5.2=6
  - 6.1=17, 6.2=9
  - 7.1=1 (SKIP)
  - 8.1=13, 8.2=23
- Stage 1a: 5 Task 2 essays (sub-cats 1.1×2, 1.2, 1.5, 4.4 — covers 4 distinct sub-cats)
- Stage 1b: 37 Task 2 essays (32 first-essay covering 32 sub-cats incl. 1.3, 1.4, 1.6, 1.7, 1.8, 2.1-2.5, 3.1-3.10, 4.1-4.6, 5.1, 5.2, 6.1, 6.2, 8.1, 8.2; 5 second-variants for 1.1/1.2/1.5/4.4)
- Stage 1c: 234 − 42 (existing) − 1 (7.1 音乐) = **191 prompts**
- `docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54` — Stage 1a essay template (single article / single main / single h1 / prompt section / essay section / rubric section / keywords section with `<code>` items)
- `docs/writing/task2/06-26-env-solutions.html:1-53` — Stage 1b first-essay template (same as Stage 1a, uses `data-type="single-question"` chip)
- `scripts/verify-stage1b.sh:1-151` — 9 invariants + 8-chip whitelist + 270-290 band; **already covers Stage 1c without modification**
- `docs/writing/index.html:1-342` — Index with 55 `<article>` cards; chip filter JS (lines 92+); needs extension to 246
- `.github/workflows/deploy.yml` — Existing 4 SHA-pinned + cancel-in-progress: true; no change needed

## Decisions (with rationale)

- **Wave 0 foundation scope**: T-065 (verify script dry-run on Stage 1b corpus as RED → GREEN confirm). T-066 (index extension scaffold — generate 191 placeholder cards from docx prompt enumeration). NO chip whitelist extension needed.
- **Pilot (Wave 0 final ticket)**: T-067 — write 1 stage1c essay end-to-end, run bulk verify, run Actions deploy, confirm all 8 chips + 246 cards visible. Validates sub-agent protocol before fan-out.
- **Wave 1-6 Task 2 fan-out**: 6 waves × 32 essays (Wave 6 has 7 essays); each wave = 8 SA × 4 essay.
- **Sub-cats with >4 prompts**: split across SA (e.g., 3.2 文化 with 17 prompts → 4 SA + 1 SA picks up overflow; 8.2 旅行 with 23 → 6 SA). Largest sub-cats drive multiple waves.
- **Sub-cats with 1 prompt**: grouped together (e.g., 1.3, 2.4, 2.5, 3.7, 3.9, 3.10, 4.2, 4.5 = 8 sub-cats × 1 prompt = 8 essays → 2 SA × 4 essay).
- **Final verification wave (Wave 7)**: bulk verify all 246 essays + Playwright spot-check + chip distribution check + ship-evidence-gate + HANDOFF-stage1c.md.

## Scope IN

- 191 new Task 2 essay HTML files in `docs/writing/task2/<NN>-<slug>.html` (NN from 43..233)
- `docs/writing/index.html` extended from 55 → 246 `<article>` cards
- 6-7 parallel subagents per wave (peak 8), 4 essay / subagent
- Atomic 1-essay-per-commit (191 commits + foundation commits + final commit)
- Commit message format: `stage 1c(T-NNN): <slug> — <one-line what>`
- Each essay: 270-290 words, single `<h1>`, single `<main>`, `<article data-task data-difficulty data-type>`, 5-10 `<code>` in keywords section, 1-2 paragraph Chinese rubric (TA/CC/LR/GRA)
- Per-essay AC (binary, blocking commit):
  - AC-A1: file path matches `docs/writing/task2/<NN>-<slug>.html`
  - AC-A2: exactly one `<h1>` (verify script)
  - AC-A3: exactly one `<main>` (verify script)
  - AC-A4: `<article>` with all 3 data-attrs on same line (verify script)
  - AC-A7: 5-10 `<code>` in keywords section (verify script)
  - AC-T2-1: no `<figure>` element (verify script)
  - AC-T2-2: word count 270-290 (verify script)
  - AC-T2-3: `data-type` in 8-chip whitelist (verify script)
  - AC-T2-4 (NEW for Stage 1c): prompt source line — frontmatter references docx `(sub-cat, prompt-N)` and essay intro paraphrases a prompt NOT covered by Stage 1a/1b (prevents re-writes)
  - AC-T2-5 (NEW for Stage 1c): chip selection matches prompt's question word
- Bulk verify (`bash scripts/verify-stage1b.sh docs/writing/`) exit 0 on 246 essays after each wave
- Index extension script (Python, 1-time use)
- Handoff cleanup: 3 files deleted after spec EXPLORED (already done? No — spec EXPLORED but handoff still present. Run before plan review.)
- HANDOFF-stage1c.md at ship time (mirror Stage 1a/1b format)

## Scope OUT (Must NOT have)

- 7.1 音乐 sub-cat (1 prompt) — explicitly dropped
- Stage 1a/1b 55 essays modification
- 9 invariants change (single `<h1>`, single `<main>`, etc.)
- 8-chip whitelist extension (no new chips needed for Stage 1c prompts; existing 8 chips cover all 234 prompts)
- verify-stage1b.sh modifications (existing 9 invariants + 8 chips + 270-290 band fully cover Stage 1c)
- New dependencies / new modules
- Index filter JS behavior changes
- Visual-qa dual-oracle gate — **REQUIRED in Wave 7 final** (full 246 corpus, user selected "全量必做")
- Stage 1a/1b handoff documents (already gitignored or about to be deleted by C4)
- Reading / Speaking / Listening module surfaces (still aria-disabled)
- HTTPS upgrade, SEO, sitemap, analytics, multi-language UI
- Per-paragraph Chinese rubric (consolidated 1-2 paragraph is the contract)
- New chip whitelist beyond 8 (no new chips needed)

## Open questions

(None — user resolved visual-qa gate by selecting "全量必做" — Wave 7 final-verifier.)

## Approval gate
status: awaiting-approval
<!-- Set status to awaiting-approval once exploration is exhausted and unknowns are answered. -->
<!-- This durable record is the loop guard: on a later turn read it and resume at the gate instead of re-running exploration. -->

**Brief for user:**

Stage 1c intent: **CLEAR** (user selected "完整 OMO + 191 篇分 wave (推荐)"). `review_required: false`.

**Plan approach**: 4 components (essay corpus C1, index C2, verify script C3 no-op, handoff cleanup C4). 7 waves:
- **Wave 0 — Foundation**: verify script dry-run (T-065), index extension scaffold (T-066), pilot essay end-to-end (T-067), handoff cleanup (T-068: git rm HANDOFF-stage1a.md / HANDOFF-stage1b.md / rm .opencode/handoffs/2026-08-15T154136.md).
- **Wave 1-6 — Task 2 essay fan-out**: each wave = 8 parallel SA × 4 essay = 32 essay; Wave 6 = ~7 essay (191 total).
- **Wave 7 — Final verification**: bulk verify all 246 essays; Playwright spot-check on 5+ essays; visual-qa dual-oracle (user selected "全量必做"); ship-evidence-gate; /review-work 5-lane; HANDOFF-stage1c.md.

**Defaults adopted (reversible, no need to ask)**:
- Wave size: 32 essays/wave (Stage 1b SA-2 model)
- Atomic 1-essay-per-commit, format `stage 1c(T-NNN): <slug> — <one-line what>`
- Per-essay AC: 9 invariants (verify script) + AC-T2-4 (prompt uniqueness) + AC-T2-5 (chip matches prompt's question word)
- Sub-cats >4 prompts split across multiple SA; 1-prompt sub-cats grouped
- No verify script modification; no chip whitelist extension
- 8 chip whitelist UNCHANGED

**Out of scope (must NOT have)**: Stage 1a/1b modification, 9-invariant change, 8-chip whitelist change, new dependencies, 7.1 音乐 sub-cat, visual-qa deferred (we now include it).

**Ticket count**: 1 verify-script + 1 index-script + 1 pilot + 1 handoff-cleanup + 191 essay + 5 final-wave = ~200 tickets.

**Owner-decisions resolved**:
- Visual-qa gate: required in Wave 7 (user selected 全量必做)

**Plan deliverable**: `.omo/plans/stage1c.md` (decision-complete; 7 waves; 200 tickets; verification gates G0-G7).
