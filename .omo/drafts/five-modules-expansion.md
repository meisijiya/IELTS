# Draft — `five-modules-expansion`

> Single resume point. Read this before any later turn.

## Intent

- `intent: clear`
- `review_required: false` (user did not request high-accuracy review)

## Outcome (user-stated)

1. **Listening + Reading 模块**: 在主页从 `Coming soon` 升级为真实可点击模块，内容**只讲解答题技巧**（不涉及 2026 政策、A vs G、AWL 元信息、备考路径）。
2. **新增第五个模块「积累」**: 整合这 5 个文档：
   - `/home/ljh2923/opencode-project/IELTS/口语 Part1 5-8月collocations.docx`
   - `/home/ljh2923/opencode-project/IELTS/听力高频词汇.pdf`
   - `/home/ljh2923/opencode-project/IELTS/剑桥雅思口语写作词汇.pdf`
   - `/home/ljh2923/opencode-project/IELTS/【revised】考点词538.pdf`
   - `/home/ljh2923/opencode-project/IELTS/写作 collocation.pdf`
3. 词条按各文档原始分类/标签组织，方便检索 + 复习。
4. 提供拼写输入框练习（**题空 + 实时反馈** 风格，**5 文档全部词条开放拼写**）。

## Owner-decisions resolved by user (recorded)

- **R-1** Listening/Reading 深度 → `题型技巧清单 + 简单策略`（题型 → 应对 → 速查表；不含元信息）
- **R-2** 拼写范围 → `全部词条开放拼写`（5 文档 ~2300 条全进拼写池，按分类筛选）
- **R-3** 拼写 UI → `题空 + 实时反馈`（显示中文 → 输入英文 → 即时对/错 + 显示完整词条）
- **R-4** 浏览器缓存 → **加 localStorage 增强**：进度持久化（key=`vocab-progress`）+ 学习统计 chip（累计练习 / 总正确率 / 重置按钮）+ 「未掌握」tab（拼错过的词，按 wrongCount 排序）+ 拼写卡片底部历史正确率小字

## Defaults adopted (no user input needed)

- **数据存储**: 静态 JSON 文件 `docs/vocab/data/*.json`，每文档一个；运行时 fetch + 内存缓存（同会话不重复 fetch）。
- **页面技术栈**: 纯静态 HTML + CSS + 原生 JavaScript（与现有 `docs/speaking/` / `docs/writing/` 风格一致，不引入新框架）。
- **现有模块**: `docs/speaking/` 与 `docs/writing/` 不动；不动任何 `.opencode/skills/*` 文件。
- **拼写判定规则**: 去除两端空白、不区分大小写、忽略首尾标点（如 `.` `,`）；同义/变形算错（坚持"拼对就给对"）。
- **OCR 处理**: 3 个图像型 PDF（听力高频、剑桥口语写作、写作 collocation）用 pdfplumber/PyMuPDF 渲染 + tesseract OCR；OCR 中文字段允许小误差，英文/IPA/数字必须 100% 准确。
- **题空模式**: 显示中文/释义 → 单词框输入 → 输入时即时判定（防抖 100ms）。
- **正误标记**: 对→绿色边框 + ✓；错→红色边框 + 拼写差异提示 + 显示完整词条；空→中性。
- **localStorage 容量**: 5 文档全量 ~2300 词条进度 JSON 上限 ~230 KB，localStorage 5 MB 限制内绰绰有余。

## Scope OUT (Must-NOT-Have)

- 不要做 `口语 Part 2/3` 的题目库（已有 `speaking/` 内 Part 2&3，5 文档只覆盖 Part 1）。
- 不要把 `.opencode/skills/` 的 SKILL.md 整段搬到网页（用户明确说"只讲技巧"，元信息已在 skill 中可见，不重复）。
- 不要引入 SPA/前端框架/构建工具；保持纯静态。
- 不要新增第 6 个文档以外的任何词汇来源。
- 不要给「写作/口语」模块加拼写功能（用户原话"积累模块"才要拼写）。
- 不要修改 speaking/writing 现有主页。

## Approval gate

- `status: awaiting-approval`
- Approach: see plan at `.omo/plans/five-modules-expansion.md` (will be written after OK).
- Next workflow action: present brief, wait for OK, then write plan.

## Backlog (open questions for plan writer)

None — all surviving forks resolved.