---
slug: writing-read-tracking-and-features
status: awaiting-approval
intent: clear
review_required: false
pending-action: hand off to worker session via $start-work; plan written at .omo/plans/writing-read-tracking-and-features.md
approach: Add JS-only client-side features (read-tracking, typing boxes, sticky prompt, clear-cache) to the existing static HTML site. All paths are already relative → GitHub Pages compatible with no JS/CSS/HTTP-path changes. New files: 3 small vanilla JS modules under `docs/assets/js/` + 1 batch injection script under `scripts/` + 2 GitHub Pages deployment files (`.nojekyll`, `CNAME`). Edit existing files via the injection script — never hand-edit 292 + 71 article pages. Single component topology: all features share the `ielts-*` localStorage namespace so the homepage clear-cache button can wipe everything atomically. localStorage is per-origin (scheme + host + port), NOT per-path, so the same key works at `meisijiya.site/IELTS/...` and `meisijiya.github.io/IELTS/...` without any code change. The visual design and per-feature behavior are pre-validated in `.omo/drafts/design-preview.html` (4 interactive demos) — implementation MUST mirror its CSS classes, colors, and interactions.
plan_path: .omo/plans/writing-read-tracking-and-features.md
plan_sha256: null
approval_round_id: round-1
approval_decision: user-said-可以写plan
approval_timestamp: 2026-08-18
---

# Draft: writing-read-tracking-and-features

## Components (topology ledger)

| id | outcome (one line) | status | evidence path |
|----|--------------------|--------|---------------|
| C1. read-tracker.js | One vanilla JS module that paints red/green dots on list cards and marks a visited article on load. Used by both writing list + speaking list + every article page. | active | `docs/assets/js/read-tracker.js` |
| C2. essay-typing.js | One vanilla JS module that adds input boxes under each `<p>` of `<section class="essay">`, makes `.prompt` sticky with a collapse toggle, and persists drafts to `ielts-writing:draft:<slug>:<i>`. Used only by writing article pages. | active | `docs/assets/js/essay-typing.js` |
| C3. clear-cache.js | One vanilla JS module that wires the homepage button: on click, iterate `localStorage`, remove keys with prefix `ielts-`, then refresh the page. | active | `docs/assets/js/clear-cache.js` |
| C4. inject-features.py | One Python script (stdlib only, mirrors `extend-index.py` and `generate-speaking-pages.py` patterns) that injects `<script>` tags + homepage button into the existing files. Idempotent: re-running is a no-op. | active | `scripts/inject-features.py` |
| C5. writing task1/task2 edits | After C4 runs, every file in `docs/writing/task1/*.html` and `docs/writing/task2/*.html` (292 files) gets `<script defer src="../../assets/js/read-tracker.js">` + `<script defer src="../../assets/js/essay-typing.js">` before `</body>`. | active | `docs/writing/task1/*.html`, `docs/writing/task2/*.html` |
| C6. speaking topics edits | Every file in `docs/speaking/topics/*.html` (71 files) gets `<script defer src="../assets/js/read-tracker.js">` before `</body>`. | active | `docs/speaking/topics/*.html` |
| C7. writing index edits | `docs/writing/index.html` gets `<script defer src="../assets/js/read-tracker.js">` before `</body>`. The existing inline script at the bottom stays untouched. | active | `docs/writing/index.html` |
| C8. speaking index edits | `docs/speaking/index.html` gets `<script defer src="../assets/js/read-tracker.js">` before `</body>`. The existing inline script at the bottom stays untouched. | active | `docs/speaking/index.html` |
| C9. homepage edits | `docs/index.html` gets a `<button class="clear-cache-btn">清除缓存</button>` + `<script defer src="assets/js/clear-cache.js">` before `</body>`. | active | `docs/index.html` |
| C10. CSS additions | Append ~60 lines to `docs/assets/css/style.css` — `.dot-read`, `.dot-unread`, `.typing-input`, `.typing-row`, `.prompt-sticky`, `.prompt-sticky.collapsed`, `.clear-cache-btn`. No rewriting of existing rules. **CSS MUST exactly mirror the proven styles in `.omo/drafts/design-preview.html` lines 91-330** (dot, sticky, typing, clear-cache classes). | active | `docs/assets/css/style.css` |
| C11. GitHub Pages `.nojekyll` | Empty file at `docs/.nojekyll`. Disables GitHub Pages' default Jekyll processing. Defensive — no current `_`-prefixed files, but shields against future ones. | active | `docs/.nojekyll` |
| C12. GitHub Pages `CNAME` | Single-line file `docs/CNAME` containing `meisijiya.site`. Preserves the existing custom domain (the live site URL `meisijiya.site/IELTS/...` already uses it). GitHub Pages reads this file and serves TLS for that domain. | active | `docs/CNAME` |
| C13. Sticky prompt robust solution | The design preview still showed text bleed-through after 3 rounds of CSS attempts. Production implementation MUST use the **container-isolation pattern**: wrap body in `<div class="essay-body">` with `position: relative; z-index: 1; isolation: isolate`, then `.prompt-sticky` gets `position: sticky; top: 0; z-index: 10; isolation: isolate; background: #fff`. Two separate stacking contexts → prompt always wins. Plus `background-image: linear-gradient(#fff, #fff)` as belt-and-suspenders. | active | `docs/assets/css/style.css` + `docs/assets/js/essay-typing.js` |
| C14. Open-state persistence | Preview added `ielts-writing:open:<slug>:<paragraph-index>` keys to remember the textarea's expanded/collapsed state. Production MUST persist this — opening/closing the box per paragraph should survive page reloads. | active | `docs/assets/js/essay-typing.js` |

## Open assumptions (announced defaults)

| assumption | adopted default | rationale | reversible? |
|------------|-----------------|-----------|-------------|
| "已读" 触发时机 | 页面 `DOMContentLoaded` 后立即标记为已读 | 最小代价；用户已点击进入即视为"看过"；不收集滚动/停留时间 | 是；改 JS 一行 |
| 红/绿圆圈渲染位置 | 卡片左上角（绝对定位 8px），与标题并排不阻挡 | 大屏幕小屏通用；不破坏现有 `<h3>` 流式布局 | 是；改 CSS |
| 输入框 UI | 每段 `<p>` 下方一个 `<textarea rows="3" placeholder="…">` + 一个展开/收起按钮（`▸ 练习` / `▾ 收起`），默认收起 | 与用户"默认收起"指令一致；textarea 而非 input 支持多行 | 是；改 CSS/JS |
| 输入框展开状态持久化 | 写入 `ielts-writing:open:<slug>:<i>`，刷新后保留展开/收起状态 | 用户在预览页要求的行为；避免每次打开都点一遍 | 是；改 JS |
| 草稿持久化粒度 | 输入时 `input` 事件 debounce 500ms 写 localStorage | 平衡磁盘写入频率与防丢 | 是 |
| 草稿键命名 | `ielts-writing:draft:<slug>:<paragraph-index>` | 与用户一致答："持久化"；含 slug 避免跨文章串数据 | 是 |
| 已读键命名 | `ielts-read:<module>:<slug>`，`module ∈ {writing, speaking}` | 单一前缀方便一键清；`<slug>` 从页面 URL 末段（去 `.html`）+ `<article data-task>` 或 `data-topic-id` 派生 | 是 |
| Sticky 行为 | `position: sticky; top: 0;` 配合 `z-index: 10` | 用户最简；移动端 `viewport` 滚动不影响 | 是；改 CSS |
| Sticky prompt 兜底 | 用**容器隔离**模式：`<div class="essay-body">` 包正文段落并 `isolation: isolate; z-index: 1`；`.prompt-sticky` 同样 `isolation: isolate; z-index: 10`；加 `background-image: linear-gradient(#fff, #fff)` 强制绘制 | 预览页 3 轮加固仍漏底 → 必须在生产实现时用上更稳的方案；两道独立 stacking context + 强制绘制 | 是；改 CSS |
| 收起触发 | prompt 标题右侧加 `<button class="prompt-toggle">▾</button>`；点击切换 `.collapsed` 类，把 prompt 高度压到 40px 看一行概要 | 单击切换；用户自选 | 是 |
| 清除缓存反馈 | 按钮点击后短暂变文字"已清除 ✓"(2 秒) 再刷新页面 | 无 alert；最小干扰 | 是 |
| 注入的可逆性 | inject-features.py 是 idempotent：若 `<script>` tag 已存在则跳过；可再跑一次不会重复注入 | 匹配现有 `extend-index.py` 的幂等模式（看 WRITTEN_BYTES 校验） | 是 |
| 阅读/听力/词汇 | 已读追踪只覆盖 writing + speaking（用户已答） | 该三模块无 per-article 列表页；不强行修 | 是 |
| JS 加载位置 | 全部 `defer` 后置于 `</body>` 前 | 已有说话模块 `learning-mode.js` 用的同一模式 | 是 |
| 不动现有 inline 脚本 | 写作 index.html 的 filter 脚本、口语 index.html 的搜索脚本原位不动 | 不破坏现有功能 | 是 |
| 不动 CSS 已有规则 | 所有新样式 append 到 style.css 末尾 | 已有 `style.css` 182 行被多个页面共享；最小风险 | 是 |
| 设计预览 = source of truth | 生产 CSS 类名、颜色、间距、行为完全 mirror `.omo/drafts/design-preview.html` 的 4 个 demo（dot grid、sticky 折叠、typing 持久化、清除缓存） | 预览已可视验证；避免凭空设计回退 | 是；改 CSS 偏移 1-2 行无影响 |

## Findings (cited - path:lines)

- 主页结构 — `docs/index.html:10-42` — 5 module `<article class="card">` + footer；无 JS
- 写作列表页结构 — `docs/writing/index.html:43-1212` — 292 `<article data-task data-difficulty data-type>` 卡片 + 行 1216-1288 已有的 filter 脚本
- 写作 Task 1 文章结构 — `docs/writing/task1/01-table-universities-ranked.html:14-52` — `<article data-task data-difficulty data-type><header><section class="prompt"><figure><section class="essay"><section class="rubric"><section class="keywords">`
- 写作 Task 2 文章结构 — `docs/writing/task2/01-agree-disagree-history-vs-business.html:14-52` — 与 Task 1 共同结构
- 口语列表页结构 — `docs/speaking/index.html:50-619` — 71 `<a class="topic-card" href="topics/..." data-part data-category data-title-en data-title-zh>` 卡片
- 口语 topic 页结构 — `docs/speaking/topics/p1-hometown.html:17-148` — `<article data-topic-id data-part>` + `<details class="qa-item">` 模式
- 已有 JS 范式 — `docs/speaking/assets/js/learning-mode.js:1-51` — IIFE + try/catch 包 localStorage + 事件委托；本计划沿用
- 现有 CSS 变量 — `docs/assets/css/style.css:1-6` — `:root { --ink, --green, --bg, --muted }`；新样式用 `var(--green)` 保持一致
- 现有 prompt 样式 — `docs/assets/css/style.css:141-147` — `.prompt { background: var(--muted); border-left: 4px solid var(--green); font-style: italic }`；新 sticky 行为需在该规则上叠加
- 已有 batch 脚本范式 — `scripts/extend-index.py:1-178` — stdlib only + log file + 字节校验；`scripts/generate-speaking-pages.py:1-100` — 模板渲染 + 替换 + log
- 站点规模 — `docs/writing/task1/` 13 个 .html + `docs/writing/task2/` 279 个 .html = 292 写作文章；`docs/speaking/topics/` 71 个 = 71 口语 topic
- 设计预览（粗略设计参考） — `.omo/drafts/design-preview.html` — 654 行，4 个 demo（dot 网格、sticky 折叠、typing 持久化、清除缓存）+ 决策一览；CSS 行 91-330（dot / sticky / typing / clear-cache 类）+ JS 行 500-650（交互）+ 储物 inspector
- Sticky prompt 预览页遗留问题 — `.omo/drafts/design-preview.html:127-147` — 3 轮加固（`background: #fff !important` + `z-index: 100` + `isolation: isolate` + `box-shadow`）后用户仍报告正文段落穿透显示；生产实现必须用 `essay-body` 容器隔离加固

## Decisions (with rationale)

- **D1. JS-only，纯 vanilla，无依赖** — 保持站点零依赖；与已有 `learning-mode.js` 一致
- **D2. 单一 inject-features.py 脚本** — 避免分散多个脚本注入碎片；与现有 one-off script 风格一致
- **D3. CSS 全部 append，不修改已存在规则** — 最小破坏面；任何回滚都可 `--reset` 风格撤销
- **D4. 主页按钮位置** — 放在 `<footer>` 上方、主卡片下方；理由：破坏性操作不应出现在首屏显眼位置
- **D5. 红/绿圈颜色** — 沿用 `var(--green)` 绿；红色用 `#c33`（与现有 ink 同色系但不冲撞）
- **D6. 输入框不检查** — 仅占位符 + 可保存草稿；用户已答 "不需要检查"
- **D7. 已读键含模块前缀** — 单一前缀 `ielts-read:*` 便于清除；`<module>` 字段保留避免 writing 与 speaking slug 撞名
- **D8. 清除缓存 = `ielts-*` 前缀** — 用户已答 "仅清本应用键"
- **D9. Sticky 实现选 CSS 而非 JS** — `position: sticky` 比 JS 监听轻量；移动端表现一致
- **D10. prompt 收起 fold 行为** — 收起时整个 `.prompt` 元素塌缩到约 40px 高（露出一行 + toggle 按钮），不要直接 `display: none` —— 用户可能随时想看
- **D11. Sticky prompt 容器隔离** — 用 `<div class="essay-body">` 包正文段落（`isolation: isolate; z-index: 1`），与 `.prompt-sticky`（`isolation: isolate; z-index: 10`）形成两个独立 stacking context；必修预览页残留的 text 穿透问题
- **D12. 输入框展开状态持久化** — 增 `ielts-writing:open:<slug>:<i>` 键，与草稿键对称；按键 switching 状态也写 localStorage
- **D13. 设计预览作 source of truth** — 生产 CSS 必须 mirror `.omo/drafts/design-preview.html`，避免凭空设计回退到不兼容的样式

## Scope IN

1. 新建 `docs/assets/js/read-tracker.js`（≤ 50 行）
2. 新建 `docs/assets/js/essay-typing.js`（≤ 100 行）
3. 新建 `docs/assets/js/clear-cache.js`（≤ 20 行）
4. 新建 `scripts/inject-features.py`（≤ 200 行）
5. 追加 CSS 规则到 `docs/assets/css/style.css`（≤ 80 行；CSS 内容对齐 `.omo/drafts/design-preview.html` 行 91-330）
6. 在 `docs/index.html` 加清除缓存按钮 + 引 `<script>`
7. 在 `docs/writing/index.html`、所有 292 篇写作文章、71 个口语 topic、`docs/speaking/index.html` 引 `<script>` 标签
8. 写作 292 篇文章的每段 `<p>` 下方 JS-injected 输入框（运行时注入，不改 HTML 源；opener-state + content 双重持久化）
9. 写作 292 篇文章的 `.prompt` 改为 sticky + collapse；用 `essay-body` 容器隔离 + `background-image` 兜底；selector 一次只匹配第一个 `.prompt`（即写作题目的 prompt，不影响 reading/listening 的 `.prompt`）
10. **GitHub Pages 兼容**：新建 `docs/.nojekyll`（空文件，禁用 Jekyll）
11. **GitHub Pages 兼容**：新建 `docs/CNAME`（单行 `meisijiya.site`，保留自定义域名）
12. **设计预览同步**：实现完毕后将 `.omo/drafts/design-preview.html` 标记为 obsolete（保留作参考，不删）

## Scope OUT (Must NOT have)

- 不可修改 `docs/writing/task1/*.html` / `task2/*.html` / `docs/speaking/topics/*.html` 的现有 essay/prompt 内容或 attribute
- 不可在阅读 / 听力 / 词汇模块加已读标记（用户已确认仅写作 + 口语）
- 不可调用 `localStorage.clear()` 全清 —— 仅删 `ielts-*` 前缀
- 不可重写 `docs/assets/css/style.css` 已有 182 行
- 不可重写 `docs/writing/index.html` 已有 1216-1288 行的 filter 脚本
- 不可重写 `docs/speaking/index.html` 已有 624-693 行的搜索脚本
- 不可引入第三方 JS / CSS 库（CDN / npm）；只用浏览器原生 API
- 不可改 `<article data-task data-difficulty data-type>` 或 `<article data-topic-id>` 已有属性
- 不可在输入框上做"对错检查"功能（用户已答"不需要检查"）
- 不可使用 alert() / confirm() 弹窗；改用文字反馈
- 不可把"已读"完全清空时弹 toast —— 直接刷新页面即可
- 不可新增 `<script>` 同步加载（必须 `defer`）
- 不可让 dot indicator 阻挡标题点击（pointer-events: none / 鼠标穿透）
- **GitHub Pages 兼容**：不可引入需要构建步骤的资产（保留纯静态）
- **GitHub Pages 兼容**：不可使用 `file://` 协议相关的特性（必须能 HTTPS 跑）
- **GitHub Pages 兼容**：不可把 localStorage 键绑死到绝对路径（保持 origin-scoped，`ielts-*` 前缀足够）

## Open questions

无；用户已答完 3 个 owner-decision fork。

## Approval gate
status: awaiting-approval

**Approach summary:** 6 个新文件（3 个 vanilla JS 模块 + 1 个 Python 注入脚本 + 2 个 GitHub Pages 部署文件 `.nojekyll` / `CNAME`）+ 1 个 CSS 追加 + 364 个 HTML 文件的程序化注入。零手改 essay/topic HTML。

**Files in / out:**
- New: `docs/assets/js/read-tracker.js`, `docs/assets/js/essay-typing.js`, `docs/assets/js/clear-cache.js`, `scripts/inject-features.py`, `docs/.nojekyll`, `docs/CNAME`
- Modified: `docs/assets/css/style.css` (append), `docs/index.html` (add button + 1 script), `docs/writing/index.html` (add 1 script), `docs/speaking/index.html` (add 1 script)
- Modified by script: 292 writing essays + 71 speaking topics (each gets 1-2 script tag lines)

**GitHub Pages 适配要点（您新增的约束）：**
- 现有代码零修改：所有路径 relative，localStorage 是 origin-scoped（与 path 无关），HTTPS/HTTP 都行
- `docs/.nojekyll` 阻止 GitHub Pages 默认的 Jekyll 处理（防止未来 `_` 开头文件被吃掉）
- `docs/CNAME` 写 `meisijiya.site` 保留自定义域名
- GitHub Pages 启用步骤（一次性 UI 操作，不在本计划代码改动范围）：Settings → Pages → Build and deployment → Source = "Deploy from a branch" → Branch = `main`、Folder = `/docs`

**设计预览锚定（您刚提到的"粗略设计参考"）：**
- 生产实现以 `.omo/drafts/design-preview.html` 为准——CSS 类名、颜色、间距、行为必须与该预览页的 4 个 demo section 对齐
- 预览页中 sticky prompt 仍漏底的问题，将在生产实现时用 `essay-body` 容器隔离 + `background-image` 兜底彻底解决
- 预览页本身不删，保留作为参考；实现完成后由 worker 在 README 注明"参考预览"

**Decisions to sanity-check:** 用户确认的 3 个 fork = 已读范围 = 写作+口语、清除范围 = `ielts-*` 前缀、输入草稿 = 持久化；GitHub Pages 适配 = 加 `.nojekyll` + CNAME 保 `meisijiya.site`。任何变化 → 重启。

**Next workflow action:** 等待用户明确"OK"。批准后——运行 scaffold 写 `.omo/plans/writing-read-tracking-and-features.md`，APPEND task batches 到 `## Todos`。**执行本身**留给独立 worker session（`$start-work`）—— 我不会自己改任何产品代码。
