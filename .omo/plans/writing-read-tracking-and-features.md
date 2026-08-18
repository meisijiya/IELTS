# writing-read-tracking-and-features - Work Plan

## TL;DR (For humans)

**What you'll get:** IELTS Study 站加上 4 个零依赖客户端功能 — 写作/口语文章页的已读 dot（绿/红）、写作文章每段 `<p>` 下方可收起的打字练习输入框（500ms debounce 持久化草稿）、写作题目 prompt 滚动时吸顶 + 可折叠、主页一键清除本地缓存按钮。所有功能走浏览器 localStorage，GitHub Pages 直发零修改。

**Why this approach:** 纯 vanilla JS 模块 + 1 个 Python 注入脚本批量改 364 个 HTML 文件，**零手改 essay/topic 源 HTML**。设计已在 `.omo/drafts/design-preview.html`（654 行）可视验证。Sticky prompt 用容器隔离（`<div class="essay-body">` 双 stacking context）解决预览页残留的文字穿透问题。

**What it will NOT do:** 不改阅读 / 听力 / 词汇模块（无 per-article 列表）、不做对错检查、不引入第三方依赖、不弹 alert、清除只清 `ielts-*` 前缀、不动现有 inline 脚本和 CSS 既有 182 行。

**Effort:** Short  
**Risk:** Low — 改动限于 4 个手改文件 + 1 段 CSS 追加 + 6 个新文件 + 363 个程序化注入；任一步可 `git checkout` + `python scripts/inject-features.py --undo` 回滚

**Decisions to sanity-check:**
- 红色 dot 用 `#c33`（用户可改）
- 已读触发时机 = DOMContentLoaded（不收集停留时间）
- 输入框展开状态也持久化（`ielts-writing:open:<slug>:<i>`）
- 清除缓存后 2 秒刷新（不弹 alert）

Your next move: 启动 `$start-work` worker 执行 Implementation waves → Final verification wave。

---

> TL;DR (machine): Short / Low — 4 vanilla JS + 1 CSS append + 1 Python script + 2 GH-Pages files + 363 script-tag injections, zero source-HTML edits.

## Scope

### Must have

1. **3 个 vanilla JS 模块** — `docs/assets/js/read-tracker.js`（≤ 50 行）、`docs/assets/js/essay-typing.js`（≤ 100 行）、`docs/assets/js/clear-cache.js`（≤ 20 行）
2. **CSS 追加** — `docs/assets/css/style.css` 末尾追加 ~60 行（dot / sticky / typing / clear-cache 类），不改已有 182 行
3. **2 个 GitHub Pages 部署文件** — `docs/.nojekyll`（空）+ `docs/CNAME`（`meisijiya.site`）
4. **1 个 Python 注入脚本** — `scripts/inject-features.py`（≤ 200 行，幂等）
5. **3 个手改 HTML** — `docs/index.html`（加按钮 + script）、`docs/writing/index.html`（加 script）、`docs/speaking/index.html`（加 script）
6. **363 个 HTML 的程序化注入** — 292 写作 essay + 71 口语 topic（每个加 1-2 行 `<script defer>` 在 `</body>` 前）
7. **行为落地** — DOMContentLoaded 标记已读（绿圆点）、点击 toggle dot → 红/绿切换、点 prompt 折叠按钮 → 高度 40px / 全展开、点输入框 `▸ 练习` → 展开 textarea + 500ms debounce 写草稿、点主页 `清除缓存` → 删 `ielts-*` 键 + 按钮变 `已清除 ✓` 2 秒后刷新
8. **Sticky prompt 容器隔离** — `<div class="essay-body">` 包正文段落 + `isolation: isolate; z-index: 1`，与 `.prompt-sticky`（`isolation: isolate; z-index: 10; background-image: linear-gradient(#fff, #fff)`）形成两个独立 stacking context

### Must NOT have (guardrails, anti-slop, scope boundaries)

- 不可修改 `docs/writing/task1/*.html` / `task2/*.html` / `docs/speaking/topics/*.html` 现有内容或 attribute
- 不可在阅读 / 听力 / 词汇模块加已读标记
- 不可调用 `localStorage.clear()` —— 仅删 `ielts-*` 前缀
- 不可重写 `docs/assets/css/style.css` 已有 182 行
- 不可重写 `docs/writing/index.html` 已有 1216-1288 行的 filter 脚本
- 不可重写 `docs/speaking/index.html` 已有 624-693 行的搜索脚本
- 不可引入第三方 JS / CSS 库（CDN / npm）
- 不可改 `<article data-task data-difficulty data-type>` 或 `<article data-topic-id>` 已有属性
- 不可在输入框上做对错检查
- 不可使用 alert() / confirm() 弹窗
- 不可让 dot indicator 阻挡标题点击（`pointer-events: none`）
- 不可新增 `<script>` 同步加载（必须 `defer`）
- 不可引入需要构建步骤的资产
- 不可使用 `file://` 协议特性
- 不可改 `.omo/drafts/design-preview.html`（仅作 source of truth，不导入生产）

## Verification strategy

> Zero human intervention - all verification is agent-executed.

- **Test decision**: tests-after（静态 HTML 无单元测试框架；用结构化脚本 + grep + curl / Python HTML 解析 + 视觉自检替代）
- **Evidence**: `.omo/evidence/task-<N>-writing-read-tracking-and-features.<ext>`
- **Agent-executed QA 工具**：
  - `python3 -c "..."` — HTML 解析 + script tag 计数
  - `grep -c '<script defer src="...read-tracker.js">' docs/writing/task1/*.html` — 注入验证
  - `python3 -c "import json; ..."` — 验证 inject-features.py 是幂等的
  - 若 Chromium 可用：`agent-browser` / `playwright` 跑 smoke test（stale 检查 sticky prompt cover）
  - 用户视觉验证（worker 产出浏览器截图路径：`repo/screenshots/`）

## Execution strategy

### Parallel execution waves

> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.

- **Wave 1**（基础层，5 todos 全并行）：3 JS + CSS 追加 + 2 GH-Pages 文件
- **Wave 2**（集成层，4 todos 全并行）：1 Python 脚本 + 3 手改 HTML
- **Wave 3**（批量执行，1 todo）：跑 inject-features.py 注入 363 文件
- **Wave 4**（验证层，1 todo）：结构化 grep + 注入幂等 + 视觉截图（若 Chromium 可用）
- **Final verification wave**（F1-F4）：plan compliance / code quality / real manual QA / scope fidelity

### Dependency matrix

| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1. read-tracker.js | none | 7, 8, 9, 10 | 2, 3, 4, 5 |
| 2. essay-typing.js | none | 10, 14 | 1, 3, 4, 5 |
| 3. clear-cache.js | none | 7, 10 | 1, 2, 4, 5 |
| 4. CSS append | none | 10, 14 | 1, 2, 3, 5 |
| 5. .nojekyll + CNAME | none | 10 | 1, 2, 3, 4 |
| 6. inject-features.py | none | 10 | 7, 8, 9 |
| 7. docs/index.html (homepage) | 1, 3 | 10 | 6, 8, 9 |
| 8. docs/writing/index.html | 1 | 10 | 6, 7, 9 |
| 9. docs/speaking/index.html | 1 | 10 | 6, 7, 8 |
| 10. Run inject-features.py | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 11 | none |
| 11. Verify all + evidence | 10 | F1-F4 | none |

## Todos

> Implementation + Test = ONE todo. Never separate.

### Wave 1 — Foundation (5 parallel)

- [x] 1. Create `docs/assets/js/read-tracker.js` — read-tracking module
  What to do / Must NOT do: Create a new file `docs/assets/js/read-tracker.js` (≤ 50 lines vanilla JS, IIFE + `'use strict'`). On `DOMContentLoaded`: (a) if `<article data-task>` or `<article data-topic-id>` exists, derive module+slug and write `ielts-read:<module>:<slug>` = `'1'` to `localStorage` (try/catch); (b) for every `<article>` in the same page (list page case), look up the corresponding read key and add class `dot-read` / `dot-unread` to a `<span class="dot">` element that the script also injects if not present (use `card.querySelector('h3 a').getAttribute('href')` to extract slug). Module = `'writing'` if `<article data-task>` exists, `'speaking'` if `<article data-topic-id>` exists. Slug = URL-basename without `.html` for index pages, or the article's `data-task`+`-`+index path. **Must NOT** use any third-party lib; **must NOT** use `localStorage.clear()`; **must NOT** block rendering; **must NOT** fail if `localStorage` is disabled.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 7, 8, 9, 10
  References (executor has NO interview context - be exhaustive): `docs/speaking/assets/js/learning-mode.js:1-51` (existing IIFE + try/catch pattern), `.omo/drafts/design-preview.html:500-541` (read-tracker demo JS), `.omo/drafts/design-preview.html:91-114` (dot CSS classes), `docs/writing/index.html:1216-1288` (existing inline filter script — DO NOT touch), `docs/speaking/index.html:624-693` (existing inline search script — DO NOT touch)
  Acceptance criteria (agent-executable): `test -f docs/assets/js/read-tracker.js && wc -l docs/assets/js/read-tracker.js | awk '$1 <= 50'` returns 0; `grep -c "DOMContentLoaded" docs/assets/js/read-tracker.js` ≥ 1; `grep -c "ielts-read:" docs/assets/js/read-tracker.js` ≥ 1
  QA scenarios (name the exact tool + invocation): happy: open `docs/writing/index.html` in browser, click any card → page load shows `.dot-read` on that card; failure: open with localStorage disabled → no console error, no unhandled promise. Evidence `.omo/evidence/task-1-writing-read-tracking-and-features.js`
  Commit: Y | feat(js): add read-tracker.js — dot indicator + visited tracking

- [x] 2. Create `docs/assets/js/essay-typing.js` — typing box + sticky prompt module
  What to do / Must NOT do: Create `docs/assets/js/essay-typing.js` (≤ 100 lines vanilla JS, IIFE). On `DOMContentLoaded` for writing essay pages only (detect via `<article data-task>`): (a) for each `<p>` inside `<section class="essay">` (zero-indexed), inject a `<div class="typing-row"><button class="typing-toggle">▸ 练习</button><span class="draft-status"></span><textarea class="typing-input" rows="3" placeholder="在这里写你的第 N 段…"></textarea></div>` immediately after the `<p>`; (b) wire click on toggle to show/hide textarea (toggle `.visible` class) and persist state to `ielts-writing:open:<slug>:<i>`; (c) wire `input` event with 500ms debounce to persist textarea value to `ielts-writing:draft:<slug>:<i>`; (d) restore open state + draft value on load; (e) detect `<section class="prompt">` (only the first one in the article), add `class="prompt-sticky"` to it, inject a `<div class="prompt-title"><span>题目</span><button class="prompt-toggle">▾</button></div>` prepend, wrap the existing prompt `<p>` in `<div class="prompt-body">`, wire click on toggle to add `.collapsed` class. Slug = URL basename without `.html`. **Must NOT** add check-in / right-wrong feedback; **must NOT** alter the prompt's `<p>` text content; **must NOT** apply to any `<article>` without `data-task` (i.e., reading/listening — they have `<section class="prompt">` but no `data-task`); **must NOT** add context-insensitive overlapping.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 10, 14
  References (executor has NO interview context - be exhaustive): `docs/speaking/assets/js/learning-mode.js:1-51` (localStorage try/catch pattern), `.omo/drafts/design-preview.html:543-605` (essay-typing demo JS), `.omo/drafts/design-preview.html:190-241` (typing CSS), `.omo/drafts/design-preview.html:116-188` (sticky prompt CSS), `docs/writing/task1/01-table-universities-ranked.html:14-52` (article structure)
  Acceptance criteria (agent-executable): `test -f docs/assets/js/essay-typing.js && wc -l docs/assets/js/essay-typing.js | awk '$1 <= 100'`; `grep -c "ielts-writing:draft:" docs/assets/js/essay-typing.js` ≥ 1; `grep -c "ielts-writing:open:" docs/assets/js/essay-typing.js` ≥ 1; `grep -c "prompt-sticky" docs/assets/js/essay-typing.js` ≥ 1; `grep -c "data-task" docs/assets/js/essay-typing.js` ≥ 1
  QA scenarios (name the exact tool + invocation): happy: open `docs/writing/task1/01-table-universities-ranked.html`, click `▸ 练习` → textarea visible; type → 500ms later `已保存 ✓` shows; refresh → draft restored; failure: open `docs/reading/index.html` (no `data-task`) → no `.typing-row` injected. Evidence `.omo/evidence/task-2-writing-read-tracking-and-features.js`
  Commit: Y | feat(js): add essay-typing.js — paragraph typing boxes + sticky prompt

- [x] 3. Create `docs/assets/js/clear-cache.js` — homepage clear-cache module
  What to do / Must NOT do: Create `docs/assets/js/clear-cache.js` (≤ 20 lines vanilla JS, IIFE). On `DOMContentLoaded`: find `<button class="clear-cache-btn">`. On click: iterate `localStorage` (try/catch), collect keys with `key.startsWith('ielts-')`, remove them, then set `btn.textContent = '已清除 ✓'` + add class `cleared`, then `setTimeout(() => { btn.textContent = '清除缓存'; btn.classList.remove('cleared'); location.reload(); }, 2000)`. **Must NOT** call `localStorage.clear()`; **must NOT** use alert/confirm; **must NOT** touch keys without `ielts-` prefix.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 7, 10
  References (executor has NO interview context - be exhaustive): `.omo/drafts/design-preview.html:243-291` (clear-cache-btn CSS), `.omo/drafts/design-preview.html:607-630` (clear-cache demo JS), `docs/speaking/assets/js/learning-mode.js:1-51` (try/catch pattern)
  Acceptance criteria (agent-executable): `test -f docs/assets/js/clear-cache.js && wc -l docs/assets/js/clear-cache.js | awk '$1 <= 20'`; `grep -c "startsWith('ielts-')" docs/assets/js/clear-cache.js` ≥ 1; `grep -c "location.reload" docs/assets/js/clear-cache.js` ≥ 1
  QA scenarios (name the exact tool + invocation): happy: open index.html, click button → localStorage ielts-* keys gone, page reloads after 2s; failure: localStorage disabled → no unhandled error. Evidence `.omo/evidence/task-3-writing-read-tracking-and-features.js`
  Commit: Y | feat(js): add clear-cache.js — homepage ielts-* cache wipe

- [x] 4. Append CSS rules to `docs/assets/css/style.css`
  What to do / Must NOT do: Append to `docs/assets/css/style.css` (after existing 182 lines, no edits to existing rules). Add classes: `.dot`, `.dot-unread`, `.dot-read`, `.dot--legend`, `.typing-row`, `.typing-toggle`, `.typing-input`, `.typing-input.visible`, `.draft-status`, `.draft-status.saved`, `.scroll-hint`, `.prompt-sticky`, `.prompt-sticky.collapsed`, `.prompt-sticky.collapsed .prompt-body`, `.prompt-sticky .prompt-title`, `.prompt-sticky.collapsed .prompt-title`, `.prompt-toggle`, `.essay-body`, `.clear-cache-btn`, `.clear-cache-btn.cleared`, `.clear-cache-btn:hover`. **CRITICAL — for `.prompt-sticky`** include BOTH `isolation: isolate; z-index: 10; background: #fff; background-image: linear-gradient(#fff, #fff);` and `box-shadow: 0 2px 8px rgba(0,0,0,.12)`. For `.essay-body` include `isolation: isolate; z-index: 1; position: relative`. **Must NOT** rewrite any of the existing 182 lines; **must NOT** reorder `:root` variables; **must NOT** change selectors that already exist.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 10, 14
  References (executor has NO interview context - be exhaustive): `.omo/drafts/design-preview.html:91-330` (CSS to mirror — copy exactly the proven styles), `docs/assets/css/style.css:1-182` (existing `:root` vars + base styles — DO NOT touch)
  Acceptance criteria (agent-executable): `tail -c +1 docs/assets/css/style.css | head -182 | diff - <(git show HEAD:docs/assets/css/style.css | head -182)` returns no diff; `grep -c "\.essay-body" docs/assets/css/style.css` ≥ 1; `grep -c "isolation: isolate" docs/assets/css/style.css` ≥ 2; `grep -c "linear-gradient(#fff" docs/assets/css/style.css` ≥ 1
  QA scenarios (name the exact tool + invocation): happy: write diff to `.omo/evidence/task-4-css-diff.txt` showing first 182 lines unchanged; failure: any byte difference in lines 1-182 → fail. Evidence `.omo/evidence/task-4-writing-read-tracking-and-features.css`
  Commit: Y | feat(css): append dot/typing/sticky/clear-cache classes

- [x] 5. Create `docs/.nojekyll` and `docs/CNAME`
  What to do / Must NOT do: Create `docs/.nojekyll` as empty file (just `touch`). Create `docs/CNAME` with single line content `meisijiya.site` (no trailing newline beyond what `printf '%s\n' 'meisijiya.site'` produces).
  Parallelization: Wave 1 | Blocked by: none | Blocks: 10
  References (executor has NO interview context - be exhaustive): GitHub Pages docs on `.nojekyll` (disables Jekyll processing); `docs/CNAME` (binds custom domain)
  Acceptance criteria (agent-executable): `test -f docs/.nojekyll && wc -c docs/.nojekyll | awk '$1 == 0'`; `test -f docs/CNAME && cat docs/CNAME` outputs `meisijiya.site`
  QA scenarios (name the exact tool + invocation): happy: file existence + content check; failure: missing file → fail. Evidence `.omo/evidence/task-5-cname.txt`
  Commit: Y | chore(gh-pages): add .nojekyll + CNAME for meisijiya.site

### Wave 2 — Integration (4 parallel)

- [x] 6. Create `scripts/inject-features.py` — batch injection script
  What to do / Must NOT do: Create `scripts/inject-features.py` (≤ 200 lines, stdlib only, mirrors `scripts/extend-index.py:1-178` pattern). Subcommands: `inject` (default), `drift-check` (verify N files have correct tags), `undo` (remove all injected tags). Targets: (a) every `docs/writing/task1/*.html` and `docs/writing/task2/*.html` → inject two `<script defer src="../../assets/js/{read-tracker,essay-typing}.js">` lines before `</body>`; (b) every `docs/speaking/topics/*.html` → inject `<script defer src="../assets/js/read-tracker.js">` before `</body>`; (c) `docs/writing/index.html` → inject `<script defer src="../assets/js/read-tracker.js">` before `</body>`; (d) `docs/speaking/index.html` → inject `<script defer src="../assets/js/read-tracker.js">` before `</body>`. **Idempotency**: if `<script defer src="...read-tracker.js"` already exists in the file, skip. Detect by exact substring match. Use `pathlib.Path` and `re` (no shell). Write log to `.omo/evidence/inject-features.log`. Exit code 0 on success, 1 on file read/write error, 2 on idempotency violation. **Must NOT** modify any non-target file; **must NOT** open files for writing if no script tag is missing (no-op); **must NOT** re-order existing content; **must NOT** skip files silently.
  Parallelization: Wave 2 | Blocked by: none | Blocks: 10
  References (executor has NO interview context - be exhaustive): `scripts/extend-index.py:1-178` (stdlib + log + byte-check pattern), `scripts/generate-speaking-pages.py:1-100` (template pattern), `.omo/drafts/design-preview.html:500-630` (script tag reference paths)
  Acceptance criteria (agent-executable): `test -f scripts/inject-features.py && wc -l scripts/inject-features.py | awk '$1 <= 200'`; `python3 scripts/inject-features.py --help` exits 0; `python3 scripts/inject-features.py drift-check` after inject walk returns 0 (or prints expected counts)
  QA scenarios (name the exact tool + invocation): happy: run `python3 scripts/inject-features.py drift-check` → reports 292 writing + 71 speaking + 2 index files expected; failure: missing required tag → exit 1. Evidence `.omo/evidence/task-6-inject-features.log`
  Commit: Y | feat(scripts): add inject-features.py — batch script-tag injection

- [x] 7. Manual edit `docs/index.html` — add clear-cache button + script tag
  What to do / Must NOT do: Edit `docs/index.html` (currently 42 lines). Add a `<div class="cache-actions"><button class="clear-cache-btn" id="clearBtn">清除缓存</button></div>` block right before the `<footer>` tag. Add `<script defer src="assets/js/clear-cache.js"></script>` right before `</body>`. Use `edit` tool with exact-match oldString. **Must NOT** rewrite any existing line; **must NOT** add any other content; **must NOT** change the `<title>` or `<meta>` tags.
  Parallelization: Wave 2 | Blocked by: 1, 3 | Blocks: 10
  References (executor has NO interview context - be exhaustive): `docs/index.html:10-42` (current structure), `.omo/drafts/design-preview.html:448-460` (clear-cache demo markup)
  Acceptance criteria (agent-executable): `grep -c '<button class="clear-cache-btn"' docs/index.html` ≥ 1; `grep -c '<script defer src="assets/js/clear-cache.js"' docs/index.html` ≥ 1; `diff <(head -41 docs/index.html) <(git show HEAD:docs/index.html | head -41)` returns no diff
  QA scenarios (name the exact tool + invocation): happy: open `docs/index.html` in browser → button visible above footer; failure: missing tag → fail. Evidence `.omo/evidence/task-7-index.html`
  Commit: Y | feat(homepage): add clear-cache button + script tag

- [x] 8. Manual edit `docs/writing/index.html` — add read-tracker script tag
  What to do / Must NOT do: Edit `docs/writing/index.html`. Add `<script defer src="../assets/js/read-tracker.js"></script>` right before `</body>` (after the existing inline script at lines 1216-1288). **Must NOT** touch the existing inline filter script; **must NOT** reorder any `<article>`; **Must NOT** modify any `<article data-task>` / card content.
  Parallelization: Wave 2 | Blocked by: 1 | Blocks: 10
  References (executor has NO interview context - be exhaustive): `docs/writing/index.html:1216-1288` (existing inline script — DO NOT touch), `docs/writing/index.html:1289` (`</body>` location)
  Acceptance criteria (agent-executable): `grep -c '<script defer src="../assets/js/read-tracker.js"' docs/writing/index.html` ≥ 1; `head -1216 docs/writing/index.html | diff - <(git show HEAD:docs/writing/index.html | head -1216)` returns no diff
  QA scenarios (name the exact tool + invocation): happy: open `docs/writing/index.html` → dots visible on all cards (initially red); failure: missing tag → fail. Evidence `.omo/evidence/task-8-writing-index.html`
  Commit: Y | feat(writing-index): add read-tracker script tag

- [x] 9. Manual edit `docs/speaking/index.html` — add read-tracker script tag
  What to do / Must NOT do: Edit `docs/speaking/index.html`. Add `<script defer src="../assets/js/read-tracker.js"></script>` right before `</body>` (after the existing inline search script at lines 624-693). **Must NOT** touch the existing inline search script; **must NOT** reorder any `<a class="topic-card">`.
  Parallelization: Wave 2 | Blocked by: 1 | Blocks: 10
  References (executor has NO interview context - be exhaustive): `docs/speaking/index.html:624-693` (existing inline script — DO NOT touch), `docs/speaking/index.html:695` (`</body>` location)
  Acceptance criteria (agent-executable): `grep -c '<script defer src="../assets/js/read-tracker.js"' docs/speaking/index.html` ≥ 1; `head -624 docs/speaking/index.html | diff - <(git show HEAD:docs/speaking/index.html | head -624)` returns no diff
  QA scenarios (name the exact tool + invocation): happy: open `docs/speaking/index.html` → dots visible on all topic cards; failure: missing tag → fail. Evidence `.omo/evidence/task-9-speaking-index.html`
  Commit: Y | feat(speaking-index): add read-tracker script tag

### Wave 3 — Batch execution (1 todo)

- [x] 10. Run `scripts/inject-features.py` — inject 363 HTML files
  What to do / Must NOT do: Execute `python3 scripts/inject-features.py` (no flags = default `inject`). Verify: 13 task1 files + 279 task2 files = 292 writing essays each get 2 script tags; 71 speaking topic files each get 1 script tag; 2 index files each get 1 script tag. Log file at `.omo/evidence/inject-features.log`. Then run `python3 scripts/inject-features.py drift-check` to verify idempotency / completeness. **Must NOT** run any other script; **must NOT** skip files; **must NOT** modify non-target files.
  Parallelization: Wave 3 | Blocked by: 1, 2, 3, 4, 5, 6, 7, 8, 9 | Blocks: 11
  References (executor has NO interview context - be exhaustive): `docs/writing/task1/*.html` (13 files), `docs/writing/task2/*.html` (279 files), `docs/speaking/topics/*.html` (71 files), `scripts/inject-features.py` (just-created)
  Acceptance criteria (agent-executable): `(find docs/writing/task1 docs/writing/task2 -name '*.html' | xargs grep -l 'read-tracker.js' | wc -l)` = 292; `(find docs/writing/task1 docs/writing/task2 -name '*.html' | xargs grep -l 'essay-typing.js' | wc -l)` = 292; `(find docs/speaking/topics -name '*.html' | xargs grep -l 'read-tracker.js' | wc -l)` = 71; `python3 scripts/inject-features.py drift-check` exits 0
  QA scenarios (name the exact tool + invocation): happy: `python3 scripts/inject-features.py drift-check` reports all 363 files OK; failure: count mismatch → fail. Evidence `.omo/evidence/task-10-inject.log`
  Commit: Y | feat(inject): script-tag 363 writing articles + speaking topics

### Wave 4 — Verification (1 todo)

- [x] 11. End-to-end verification + smoke tests
  What to do / Must NOT do: Run a battery of structural checks + (if Chromium available) visual smoke tests. Structural: (a) idempotency — re-run `python3 scripts/inject-features.py` reports no changes; (b) file counts match expectation; (c) `git status` shows exactly the 4 manual edits + 6 new files + 363 modified articles + 2 deployment files; (d) `python3 -c "import html.parser; ..."` parses one modified essay to confirm no malformed HTML; (e) check `<script>` tag ordering (read-tracker before essay-typing for writing pages; reading/listening pages untouched). Visual (if Chromium): open `docs/writing/task1/01-table-universities-ranked.html`, scroll, screenshot to `.omo/evidence/task-11-sticky-prompt.png`; verify prompt background covers body text. If Chromium unavailable, document the limitation and rely on the structural CSS check. **Must NOT** modify any file except possibly writing evidence; **must NOT** skip the idempotency check.
  Parallelization: Wave 4 | Blocked by: 10 | Blocks: F1-F4
  References (executor has NO interview context - be exhaustive): `.omo/drafts/design-preview.html:127-147` (sticky prompt CSS to verify mirrors), `docs/assets/css/style.css` (CSS modifications to verify), `scripts/inject-features.py` (drift-check command)
  Acceptance criteria (agent-executable): `python3 scripts/inject-features.py drift-check` exits 0 twice in a row; `git diff --stat | grep -E "^\s+[0-9]+\s+docs/" | wc -l` ≥ 363; if Chromium available, screenshot file exists at `.omo/evidence/task-11-sticky-prompt.png`
  QA scenarios (name the exact tool + invocation): happy: all checks pass + screenshot shows prompt covering body; failure: any count mismatch or missing script tag → fail. Evidence `.omo/evidence/task-11-verify.log`
  Commit: N | (verification only)

## Final verification wave

> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.

- [x] F1. Plan compliance audit
  Run a final audit: every component in `.omo/drafts/writing-read-tracking-and-features.md` (C1-C14) has a corresponding change in `git diff --stat`. Every "Must NOT" rule still holds (no third-party lib introduced, no `localStorage.clear()`, no rewrite of `style.css` first 182 lines, no rewrite of `index.html` inline scripts, no edit to reading/listening/vocab).
  Evidence: `.omo/evidence/f1-compliance.log`
- [x] F2. Code quality review
  Static review: (a) all 3 JS files have `'use strict'` + try/catch on localStorage; (b) no `console.log` left in production; (c) CSS selector specificity sanity (no `!important` except in `.prompt-sticky`'s background fallback); (d) inject-features.py has zero `shell=True` subprocess calls.
  Evidence: `.omo/evidence/f2-quality.log`
- [x] F3. Real manual QA
  Use `agent-browser` (or fallback: `curl + grep`) to fetch `docs/index.html` + `docs/writing/index.html` + `docs/writing/task1/01-table-universities-ranked.html` + `docs/speaking/index.html` + `docs/speaking/topics/p1-hometown.html` and verify: (a) homepage button text is `清除缓存`; (b) writing index has ≥ 1 `<script>` for read-tracker; (c) writing essay has 2 `<script>` tags (read-tracker + essay-typing); (d) speaking topic has 1 `<script>` tag; (e) sticky prompt CSS class is present. If Chromium available: open writing essay, scroll, verify prompt stays visible.
  Evidence: `.omo/evidence/f3-manual-qa.log`
- [x] F4. Scope fidelity
  Re-read `.omo/drafts/writing-read-tracking-and-features.md` "Scope OUT" list. Verify each rule has not been violated. Verify all 4 user requirements are met: (1) ✅ paragraph typing box on writing essays; (2) ✅ green/red dot on writing + speaking list pages; (3) ✅ clear-cache button on homepage; (4) ✅ sticky prompt on writing essays with collapsible.
  Evidence: `.omo/evidence/f4-scope.log`

## Commit strategy

- Each Wave 1/2/3 todo creates a focused commit (10 commits total)
- Wave 1 commits: `feat(js):`, `feat(js):`, `feat(js):`, `feat(css):`, `chore(gh-pages):`
- Wave 2 commits: `feat(scripts):`, `feat(homepage):`, `feat(writing-index):`, `feat(speaking-index):`
- Wave 3 commit: `feat(inject):`
- Wave 4 (verify): no commit
- All commits use conventional-commits format; commit messages ≤ 72 chars
- Squash / rebase is acceptable before final handoff if user requests

## Success criteria

The implementation is complete when ALL of:

1. ✅ `python3 scripts/inject-features.py drift-check` exits 0
2. ✅ Exactly 363 article HTML files have new `<script>` tags + 2 index files have new `<script>` tags + 1 homepage has new button + script
3. ✅ `docs/.nojekyll` exists and is empty
4. ✅ `docs/CNAME` contains exactly `meisijiya.site`
5. ✅ `docs/assets/css/style.css` first 182 lines are byte-identical to base; appended lines include `.essay-body`, `.prompt-sticky`, `.dot`, `.typing-input`, `.clear-cache-btn`
6. ✅ All 3 JS files exist and are ≤ their line budgets
7. ✅ Reading / Listening / Vocab pages have ZERO modifications
8. ✅ `git status` shows the expected 4 + 363 + 6 = 373 file changes (4 manual + 363 injected + 6 new)
9. ✅ Final verification wave F1-F4 all APPROVE
