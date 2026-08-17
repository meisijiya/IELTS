# Spec — Stage 1c: Task 2 题库全量补齐 (191 篇)

> Spec 路径: `.omo/specs/ielts-writing-site-stage1c.md`
> 状态: **EXPLORED**（7 段 non-empty，全部 Requirement 含 Scenario）
> 上游约束: Stage 1a/1b 已 ship 55 essay，9 项模板不变量 + 8-chip whitelist + 270-290 词 band 全部保留不变。

---

## Objectives

1. **题库 100% 覆盖**：`作文真题储备（近五年）_可修改.docx` 内 234 道 Task 2 prompt 全部出 1 篇范文（除 `7.1 音乐` 不写），共新增 **191 篇** Task 2 essay；连同 Stage 1a/1b 已 ship 的 42 篇 Task 2，总计 233 篇。
2. **Stage 1a/1b 既有 55 篇**保持不动（不重写、不修改模板、不删卡），spec 仅约束新增 191 篇的产出规范。
3. **索引页 246 essay 卡片**：`docs/writing/index.html` 同步扩展（55 → 246），所有 card 含 `<article data-task data-difficulty data-type>` 与 `<h1>` 标题，filter chip 行为保留（8 个 chip 全部 ≥1 篇可见）。

## Commands / API surface

- `bash scripts/verify-stage1b.sh docs/writing/` — 验证脚本，期望对 246 essay exit 0（9 项不变量 + word-count band + chip whitelist）。
- `.github/workflows/deploy.yml` — push to `main` 时自动 build & deploy 到 GitHub Pages。

（N/A: 本 spec 不引入新的 HTTP endpoint、CLI 子命令或 event 名。）

## Structure

- **Essay corpus**: `docs/writing/task2/<NN>-<slug>.html` 新增 191 个文件（NN 从 43 起递增，覆盖 Stage 1b 已用编号 01..42 + Stage 1c 新增 43..233；slug 与 `作文真题储备` docx 的 sub-cat × prompt 编号绑定）。
- **Index**: `docs/writing/index.html` 新增 191 个 `<article>` cards（每 card 含 `<h3>` + `<p class="meta">` + 链接），filter chip 逻辑（lines 26-36 + JS）保持不变。
- **Verify script**: `scripts/verify-stage1b.sh` 现有实现覆盖 Task 2 已 ship 范围；如发现某新 essay 因 chip/word-count 触发新类型不变量，需先 patch 脚本再写 essay，但 9 项主不变量与 8-chip whitelist 不变。
- **Deployment**: 现有 `.github/workflows/deploy.yml`（4 SHA-pin + `cancel-in-progress: true`），无需修改。

## Code style

- **HTML 模板与 Stage 1a/1b 完全一致**：单 `<h1>`、单 `<main>`、`<article data-task data-difficulty data-type>`、5–10 `<code>` 关键词列表。
- **Task 2 essay body 270–290 词**（不超出 band）。
- **中文评分 1–2 段**：覆盖 TA / CC / LR / GRA 四项，每项一句话。
- **atomic commit**：每篇 essay 一个 commit（不批量）；commit message 格式 `stage 1c(T-NNN): <slug> — <one-line what>`，NNN 从 T-065 起递增（接续 Stage 1b 的 T-016..T-064）。
- **不复用 Stage 1a/1b 已写 55 篇的 prompt**：新增 191 篇必须映射到 `作文真题储备` docx 中 Stage 1a/1b 未覆盖的 prompt（防重复覆盖）。
- **不引入新依赖**：纯静态 HTML + 现有 CSS + 现有 verify bash 脚本。

## Testing

- **happy path**: `bash scripts/verify-stage1b.sh docs/writing/` exit 0（246 essay 全 PASS）。
- **filter chip visibility**: 浏览器或 Playwright 验证 8 个 Task 2 chip 都有 ≥1 essay 可见（counts: agree-disagree ≥ 1, discuss-both-views ≥ 1, positive-negative ≥ 1, opinion ≥ 1, two-questions ≥ 1, problem-solution ≥ 1, advantage-disadvantage ≥ 1, single-question ≥ 1）。
- **deploy**: `.github/workflows/deploy.yml` 跑过后，curl `https://meisijiya.github.io/IELTS/writing/task2/<新 slug>.html` 对 191 URL 返回 200（允许 0–10 个 404/30x 重定向，由 GitHub Pages 301 行为决定）。
- **content quality spot-check**: 抽样 ≥3 篇 stage1c essay，逐篇人工 verify：(a) prompt 被正确 paraphrase 进 intro；(b) 两个 body 段有明确立场 + 充分展开；(c) 270–290 词；(d) 5–10 关键词覆盖 TA/CC/LR/GRA 各项。
- **index correctness**: `docs/writing/index.html` 含 246 个 `<article>` 卡 + 55 (Stage 1a/1b) 与 191 (Stage 1c) 不重叠；filter JS 在 8 个 chip 上行为不变。

## Boundaries

In scope:

- 新增 191 篇 Task 2 essay (HTML + index cards)
- 删除 3 个 handoff 文档 (spec 写完后执行)
- 必要时微调 `scripts/verify-stage1b.sh` (新增 chip 校验或 band 校验)
- `HANDOFF-stage1c.md` 在 ship 后写 (跟 Stage 1a/1b 同样格式)

Out of scope:

- `7.1 音乐` sub-cat (1 题) — Stage 1b 已 dropped，本次同样 dropped
- 修改 Stage 1a/1b 已 ship 的 55 篇 essay
- 修改 9 项模板不变量或 8-chip whitelist (agree-disagree / discuss-both-views / positive-negative / opinion / two-questions / problem-solution / advantage-disadvantage / single-question)
- 引入新依赖 / 新模块 / 新建 build pipeline
- 修改 `.opencode/skills/ielts-writing/SKILL.md` 内容 (spec 范围内不变)
- Stage 1a/1b 文档 / 截图 / verify log 等历史产物
- `.omo/` 路径下产物 (gitignored，本次依然不提交)
- 用户已经做出的 Stage 1c 范围决策: 完整 OMO 流程 + 191 篇分 wave + 不含 7.1 + handoff 在 spec 后删

## Acceptance criteria

### Requirement: essay-coverage-191

The system SHALL produce 191 new Task 2 essay HTML files, each mapping to a distinct unused prompt in `作文真题储备（近五年）_可修改.docx`, with no overlap to the 42 Stage 1a/1b Task 2 prompts.

#### Scenario: all-191-prompts-mapped

- [ ] **WHEN** the build phase completes
- [ ] **THEN** `docs/writing/task2/` contains exactly 191 new `.html` files (filename prefix `43-` to `233-`); each filename maps to a `(sub-cat, prompt-N)` pair in `作文真题储备` docx that is not covered by Stage 1a (5 essays) or Stage 1b first-batch (32 sub-cats × 1 essay) or Stage 1b second-variants (5 essays).

#### Scenario: no-prompt-overlap

- [ ] **WHEN** new 191 essays are written
- [ ] **THEN** no two essays (across Stage 1a/1b + Stage 1c) paraphrase the same source prompt. Verifiable by reading each essay's intro and confirming unique prompt paraphrase.

#### Scenario: 7-1-music-skipped

- [ ] **WHEN** enumerating sub-cats in the source docx
- [ ] **THEN** `7.1 音乐` (1 prompt) is not written. Total docx prompts = 234; stage1c = 234 − 42 (existing) − 1 (7.1) = 191.

### Requirement: template-invariants-9

The system SHALL preserve the 9 Stage 1a/1b template invariants across all 191 new Task 2 essays.

#### Scenario: h1-and-main-singletons

- [ ] **WHEN** parsing any new essay
- [ ] **THEN** the file contains exactly one `<h1>` element and exactly one `<main>` element.

#### Scenario: article-data-attrs

- [ ] **WHEN** parsing any new essay
- [ ] **THEN** a single `<article data-task="task2" data-difficulty="<easy|medium|hard>" data-type="<one of 8 chips>">` element is present.

#### Scenario: word-count-band

- [ ] **WHEN** tokenizing any new Task 2 essay body
- [ ] **THEN** total word count ∈ [270, 290]. Verifiable via `wc -w` on essay body (excluding `<code>` keywords and Chinese rubric).

#### Scenario: code-keywords-count

- [ ] **WHEN** parsing any new essay
- [ ] **THEN** the keywords `<ul>` block contains between 5 and 10 `<code>` elements.

#### Scenario: no-figure-for-task2

- [ ] **WHEN** parsing any new Task 2 essay
- [ ] **THEN** the file contains zero `<figure>` elements (Task 2 has no chart data).

#### Scenario: chinese-rubric-present

- [ ] **WHEN** parsing any new essay
- [ ] **THEN** a 1–2 paragraph Chinese rubric section is present, covering TA / CC / LR / GRA four band descriptors.

### Requirement: index-extended-to-246

The system SHALL extend `docs/writing/index.html` to contain 246 `<article>` cards (55 existing + 191 new), preserving the existing filter chip logic.

#### Scenario: article-count

- [ ] **WHEN** parsing `docs/writing/index.html`
- [ ] **THEN** `grep -c '^    <article data-task' docs/writing/index.html` returns 246 (55 old + 191 new), no duplicates, no missing.

#### Scenario: card-links-resolve

- [ ] **WHEN** extracting all `<a href="...">` from the 191 new cards
- [ ] **THEN** each href corresponds to an existing file under `docs/writing/task2/`; `bash scripts/verify-stage1b.sh docs/writing/` reports zero broken-link or 404 invariants.

#### Scenario: chip-filter-unchanged

- [ ] **WHEN** reviewing `docs/writing/index.html` lines 26-36 (chip row) and the JS `knownTypes` Set
- [ ] **THEN** the 8 chip values are unchanged from Stage 1b T-016b: `agree-disagree`, `discuss-both-views`, `positive-negative`, `opinion`, `two-questions`, `problem-solution`, `advantage-disadvantage`, `single-question`.

### Requirement: verify-script-pass-246

The system SHALL keep `bash scripts/verify-stage1b.sh docs/writing/` exit 0 after Stage 1c ships 191 new essays.

#### Scenario: bulk-verify-exit-zero

- [ ] **WHEN** running `bash scripts/verify-stage1b.sh docs/writing/`
- [ ] **THEN** exit code is 0, all 246 essays pass all 9 invariants (h1, main, data-attrs, code-keywords, word-count band, chip whitelist, no figure for task2, chinese rubric presence).

#### Scenario: chip-distribution-non-zero

- [ ] **WHEN** reading `docs/writing/index.html` and counting cards per `data-type`
- [ ] **THEN** every one of the 8 Task 2 chips has at least 1 essay card. (May require Stage 1c to write at least 1 essay in chip types that Stage 1a/1b left under-populated; e.g., `opinion` had only 1 card in Stage 1b — Stage 1c should not reduce this.)

### Requirement: handoff-cleanup

The system SHALL delete 3 handoff artifacts once the spec is approved by Momus (i.e., immediately after this spec becomes `EXPLORED` and accepted by user), to declutter Stage 1a/1b historical session context per user request.

#### Scenario: handoff-files-deleted

- [ ] **WHEN** the delete operation runs
- [ ] **THEN** the following 3 files no longer exist on disk:
  - `HANDOFF-stage1a.md` (was repo root, git tracked → must `git rm` + commit)
  - `HANDOFF-stage1b.md` (was repo root, git tracked → must `git rm` + commit)
  - `.opencode/handoffs/2026-08-15T154136.md` (was `.opencode/handoffs/`, gitignored → plain `rm`)

#### Scenario: no-broken-references

- [ ] **WHEN** grepping the repo for `HANDOFF-stage1a.md` or `HANDOFF-stage1b.md` references
- [ ] **THEN** no live source file (script, workflow, docs, spec, plan) references them. (Acceptable if dead references remain in `.omo/` gitignored artifacts, which are not shipped.)