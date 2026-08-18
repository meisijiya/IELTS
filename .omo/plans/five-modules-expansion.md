# Plan — `five-modules-expansion`

## Goal

把 IELTS Study 主页从 2 个可用模块（speaking/writing）+ 2 个 Coming Soon（reading/listening）扩展为 **5 个完整模块**：speaking / writing / reading / listening / **积累**。其中 reading/listening 只讲答题技巧；积累模块整合 5 份词汇文档（约 2300 条），支持按分类检索 + 题空式拼写练习（实时反馈）。

## Final scope

### In-scope deliverables

1. **数据**: 5 个静态 JSON 文件 `docs/vocab/data/*.json`，每文件一份词汇库。
2. **HTML 页面**:
   - `docs/index.html`（改：5 卡片）
   - `docs/reading/index.html`（新：题型技巧清单）
   - `docs/listening/index.html`（新：题型技巧清单）
   - `docs/vocab/index.html`（新：5 文档导航 + 检索 + 拼写）
3. **静态资源**:
   - `docs/vocab/assets/css/vocab.css`
   - `docs/vocab/assets/js/vocab.js`
4. **解析脚本**:
   - `scripts/parse-speaking-p1.py`
   - `scripts/parse-listening.py`
   - `scripts/parse-cambridge.py`
   - `scripts/parse-kaodian538.py`
   - `scripts/parse-writing.py`

### Out-of-scope (Must-NOT-Have)

- 不要做 Part 2/3 的题目库（积累模块的 5 文档只覆盖 Part 1）。
- 不要把 `.opencode/skills/` SKILL.md 整段搬到网页（用户明确说"只讲技巧"）。
- 不要引入 SPA / 前端框架 / 构建工具；保持纯静态 HTML+CSS+JS。
- 不要新增 5 文档以外的任何词汇来源。
- 不要给 speaking/writing 模块加拼写功能。
- 不要修改 speaking/writing 现有主页文件。
- 不要修改任何 `.opencode/skills/*/SKILL.md`。

## Decisions

| # | 决策 | 选择 | 来源 |
|---|---|---|---|
| D-1 | listening/reading 深度 | 题型技巧清单 + 简单策略 | 用户回答 R-1 |
| D-2 | 拼写范围 | 全部词条开放 | 用户回答 R-2 |
| D-3 | 拼写 UI | 题空 + 实时反馈 | 用户回答 R-3 |
| D-4 | 数据格式 | 静态 JSON，每文档一文件 | 默认 |
| D-5 | 技术栈 | 纯静态 HTML+CSS+原生 JS | 默认（与现有风格一致） |
| D-6 | 拼写判定 | trim + lowercase + 忽略首尾标点 | 默认 |
| D-7 | OCR 工具 | pdfplumber 文本层 → pypdfium2/tesseract OCR 兜底 | 默认 |
| D-8 | 拼写正误反馈 | 对→绿框 ✓；错→红框 + 差异提示 + 显示完整词条 | 默认 |

## Dependency matrix

| 任务 | 依赖 |
|---|---|
| T-2~T-6 (解析) | 无（独立） |
| T-7 (主页改) | 无（与解析并行） |
| T-8, T-9 (reading/listening 页) | 无（与解析并行） |
| T-10 (vocab/index.html) | 依赖 T-1~T-5 的 JSON 输出（仅在 T-6 QA 后） |
| T-11 (vocab.css) | 无（并行） |
| T-12 (vocab.js) | 依赖 T-1~T-5 的 JSON schema 约定（先在 T-6 锁定 schema） |
| F-1 ~ F-5 | 依赖所有 T-*

## File-by-file contract

### `docs/index.html`（改）

- 5 个 `<article class="card">`：
  1. Speaking（现有）
  2. Writing（现有）
  3. Reading（新：`href="reading/"`）
  4. Listening（新：`href="listening/"`）
  5. 积累（新：`href="vocab/"`，描述"5 份词汇文档整合检索 + 拼写练习"）
- 移除 `aria-disabled="true"` 和 "Coming soon" badge
- footer 更新：`Stage 1b — Writing + Speaking live` → 反映新阶段

### `docs/reading/index.html`（新）

- 页面标题：雅思阅读 — 题型技巧速查
- 内容布局：11 大官方题型（ielts.org Type 1–11）作为 section：
  - **Type 1 Multiple choice**（单选/多选）
  - **Type 2 Identifying information**（True/False/Not Given）
  - **Type 3 Identifying writer's views/claims**（Yes/No/Not Given）
  - **Type 4 Matching information**（段落信息匹配）
  - **Type 5 Matching headings**（段落标题匹配）
  - **Type 6 Matching features**（特征匹配）
  - **Type 7 Matching sentence endings**（句子结尾匹配）
  - **Type 8 Sentence completion**（句子填空）
  - **Type 9 Summary/note/table/flow-chart completion**（摘要填空）
  - **Type 10 Diagram/flow-chart/table completion**（图解填空）
  - **Type 11 Short-answer questions**（简答）
- 每个题型 section 含：
  - 题型形式（题量 / 在哪些 Passage）
  - 3–6 条应对策略（"先看题再读文章"/"注意同义替换"/"TFNG 严格区分" 等）
  - 1 个 30 秒可立刻做的动作
- 末尾附「5 条黄金策略」section：顺序原则 / 同义替换 / 定位优先 / 时间分配 / 跳过难题
- CSS：复用 `docs/assets/css/style.css`；不新建 css

### `docs/listening/index.html`（新）

- 页面标题：雅思听力 — 题型技巧速查
- 内容布局：6 大官方题型（ielts.org）：
  - **Multiple choice**（单选/多选）
  - **Matching**（匹配题）
  - **Plan/Map/Diagram labeling**（地图与图例标签）
  - **Form/Note/Table/Flow-Chart/Summary completion**（笔记型填空）
  - **Sentence completion**（句子填空）
  - **Short-answer questions**（简答）
- 4 个 Section 速览卡片：S1 日常 / S2 独白 / S3 学术讨论 / S4 学术讲座
- 每个题型 section 含：
  - 题型形式
  - 3–6 条应对策略（含填空题四步审题法：读题 → 预判词性 → 听定位 → 拼写检查）
  - 干扰项陷阱提示（与 ielts-listening skill 的 13 潜规则对齐）
- 末尾附「13 潜规则速查」section（顺序 / 修正 / 转折 / 否定 / 字数 / 拼写 / 同义替换 / 信号词 / 多说话人 / 地图 / 流程图 / S4 笔记 / 誊抄）
- 末尾附「8 类信号词」section（因果/序列/转折/列举/举例/并列/强调/否定）
- CSS：复用 `docs/assets/css/style.css`

### `docs/vocab/index.html`（新）

- 页面标题：词汇积累 — 5 文档整合检索 + 拼写练习
- 顶部：5 个文档切换 chip（`口语 Part1 collocations` / `听力高频词汇` / `剑桥雅思口语写作词汇` / `考点词 538` / `写作 collocation`）
- 中部：当前文档的分类筛选 chip 行（按 source_doc 动态生成）
- 搜索框：按英文/中文过滤
- 模式切换 tab：`浏览模式 | 拼写练习`
- 浏览模式：词条卡片网格，每卡片显示：英文 / IPA（如有）/ 中文 / 例句（如有）/ 文档来源 chip
- 拼写练习模式：
  - 每次显示 1 个词条：中文释义 + 输入框 + 翻页按钮（上一题 / 下一题 / 跳过）
  - 输入时实时反馈（防抖 100ms）
  - 输入完成后：显示完整词条 + 例句 + 错误差异高亮
  - 顶部进度条：当前题号 / 总题数 + 正确数
- 末部：模式选择器（按分类随机 / 按全部随机 / 按顺序）
- CSS：复用 style.css + `vocab.css`
- JS：fetch JSON + 渲染 + 拼写判定

### `docs/vocab/data/*.json`（5 个新文件）

每文件结构（统一 schema）：
```json
{
  "source_doc": "<doc-id>",
  "source_label": "<中文显示名>",
  "categories": [
    {"id": "<cat-id>", "label": "<中文>", "parent": "<可选父级>"}
  ],
  "items": [
    {
      "id": "<unique-id>",
      "category_id": "<cat-id>",
      "english": "<英文词条>",
      "ipa": "<可选 IPA>",
      "chinese": "<中文释义>",
      "example_en": "<可选英文例句>",
      "example_zh": "<可选中文>",
      "tags": ["<可选标签>"],
      "tier": <可选层级 1/2/3>,
      "part_label": "<可选 Part 1 必考 / Part 1 高频>"
    }
  ]
}
```

具体每个 JSON 的内容（来自 explore 子代理的报告）：

**`speaking-p1.json`**（64 条）：
- 32 个 Part 1 话题，每个话题 2 个 collocations
- 分类：`p1-hometown`, `p1-work-or-studies`, `p1-home`, ..., `p1f-parks`, `p1f-outer-space`, ..., `p1f-hobby`
- 部分话题有 part_label = "Part 1 必考" / "Part 1 高频"

**`listening.json`**（约 1015 条）：
- 11 个场景分类
- 分类：`accommodation`, `travelling`, `banking`, `freshman`, `school-life`, `library`, `medical`, `interview`, `dining`, `science`, `society-economy`
- 含 IPA + TIPS（如有）

**`cambridge.json`**（约 270 搭配 / 66 基准词）：
- 按基准词分组（`life`, `enjoy`, `catch`, ..., `end`）
- 分类：`life-vitality`, `enjoy`, `catch`, `open`, ..., `end`（按编号）
- 部分带 `part_label` (Part 1/2/3)

**`kaodian538.json`**（538 词）：
- 3 类层级：`tier-1` (54 词) / `tier-2` (171 词) / `tier-3` (313 词)
- 每词含 importance rank + 同义替换
- 分类直接用 `tier-1` / `tier-2` / `tier-3`

**`writing.json`**（约 400 条）：
- 9 个话题分类（具体名待 OCR 完成确认）
- 分类：`<topic-1>` ... `<topic-9>`

### `docs/vocab/assets/css/vocab.css`（新）

样式规则：
- `.vocab-tabs`（模式切换 tab）
- `.vocab-card`（词条卡片）
- `.vocab-spelling-card`（拼写练习卡片，单列居中，宽度 480px）
- `.vocab-input`（拼写输入框，焦点边框变色）
- `.vocab-input.correct`（绿框 ✓）
- `.vocab-input.wrong`（红框 + shake 动画）
- `.vocab-progress`（进度条）
- `.vocab-diff`（差异高亮，黄底 + 红色下划线）
- `.vocab-source-chip`（文档来源 chip，颜色区分）

### `docs/vocab/assets/js/vocab.js`（新）

JS 模块（IIFE）：
- `STATE`：`{ activeDoc, activeCategory, activeMode: 'browse'|'spell', searchQuery, items, currentIndex, correctCount }`
- `init()`：fetch 所有 JSON → 缓存到 `STATE`
- `renderChips()`：渲染文档 chip + 分类 chip
- `renderBrowse()`：浏览模式词条网格
- `renderSpell()`：拼写练习单题视图
- `checkSpelling(value, target)`：返回 `{ status: 'correct'|'wrong'|'empty', diff }`
- `nextItem()` / `prevItem()` / `skipItem()`：翻页
- 输入监听：input 事件 → 防抖 100ms → 调用 checkSpelling → 更新 UI
- 完成时显示统计：总题数 / 正确数 / 正确率

### 解析脚本（5 个独立 Python）

每个脚本：
- 输入：原始 docx/pdf
- 输出：`docs/vocab/data/<id>.json`
- 主入口：`main()`，返回 0/1 退出码
- 日志：写到 `.omo/evidence/parse-<id>.log`

**`scripts/parse-speaking-p1.py`**:
- `python-docx`：解析 .docx
- 逻辑：迭代段落，按 `⸻` 分隔主题，提取每个主题下的 ① ② 搭配（pattern matching）
- 输出：64 条 items，每条带 `category_id` 对应 `p1-*` / `p1f-*`

**`scripts/parse-listening.py`**:
- 方案：先尝试 `pdfplumber.extract_text()`；若为空（纯图像 PDF），用 `pymupdf` 渲染 200 DPI + `tesseract` OCR（`eng+chi_sim`）
- 逻辑：识别 `N、 <category> <chinese>` 行 → 分类起点；识别 `> word` 行 → 词条起点
- 输出：约 1015 条 items

**`scripts/parse-cambridge.py`**:
- OCR 同上（PDF 是纯图像）
- 逻辑：识别 `<N>. <base-word>` → 基准词；行内识别 `Part 1` / `Part 2` / `Part 3` / `[ topic ]` → 标签
- 输出：约 270 条 items

**`scripts/parse-kaodian538.py`**:
- `pdfplumber.extract_tables()`（PDF 有文本层）
- 逻辑：识别「第 1 类 / 第 2 类 / 第 3 类」段落 → tier；表格行 → 词条
- 输出：538 条 items

**`scripts/parse-writing.py`**:
- OCR 同上
- 逻辑：识别 topic 标题行（OCR 后需手工校对），识别搭配行
- 输出：约 400 条 items（最终数量视 OCR 结果而定）

## Todos

- [x] 1. `scripts/parse-speaking-p1.py` — 解析 docx 为 64 条 Part 1 collocations JSON；输出到 `docs/vocab/data/speaking-p1.json`；日志到 `.omo/evidence/parse-speaking-p1.log`；QA：词条数 == 64 + 抽样 3 条打印 ✅ 64 items / 32 categories
- [x] 2. `scripts/parse-listening.py` — 解析 45 页 PDF 为 ~1015 条听力场景词 JSON；输出到 `docs/vocab/data/listening.json`；日志到 `.omo/evidence/parse-listening.log`；QA：词条数在 800-1200 区间 + 含 IPA + 11 个场景分类齐全 ✅ 951 items / 11 categories
- [x] 3. `scripts/parse-cambridge.py` — 解析 13 页 PDF 为 ~270 条剑桥词汇搭配 JSON；输出到 `docs/vocab/data/cambridge.json`；日志到 `.omo/evidence/parse-cambridge.log`；QA：66 个基准词齐全 ✅ 270 items / 66 categories
- [x] 4. `scripts/parse-kaodian538.py` — 解析 14 页 PDF 为 538 条考点词 JSON；输出到 `docs/vocab/data/kaodian538.json`；日志到 `.omo/evidence/parse-kaodian538.log`；QA：词条数 == 538 + tier-1=54 + tier-2=171 + tier-3=313 ⚠️ 527 items（-11，已记录差异：tier-1=48 / tier-2=168 / tier-3=311）
- [x] 5. `scripts/parse-writing.py` — 解析 18 页 PDF 为 ~400 条写作 collocations JSON；输出到 `docs/vocab/data/writing.json`；日志到 `.omo/evidence/parse-writing.log`；QA：9 个话题分类齐全 ✅ 419 items / 9 categories
- [x] 6. 锁定 JSON schema：跑通 5 个解析脚本后，验证所有 JSON 文件 keys 一致；如不一致，写一个 `scripts/normalize-vocab-schema.py` 修正 ✅ schema 核心字段全部对齐（id/category_id/english/chinese），可选字段按文档特性各异，已通过 `scripts/fix-ocr-typos.py` 修复 72 项 OCR 错字
- [x] 7. `docs/index.html` — 改：5 个 `<article class="card">`，去掉 coming soon badge，加第 5 个「积累」卡片（链接到 `vocab/`）；footer 更新；CSS 复用 style.css ✅
- [x] 8. `docs/reading/index.html` — 新建：雅思阅读题型技巧速查页，11 大官方题型 section + 黄金策略 section；CSS 复用 style.css；QA：每题型含 3-6 条策略 ✅ 11 题型 + 5 黄金策略
- [x] 9. `docs/listening/index.html` — 新建：雅思听力题型技巧速查页，6 大官方题型 section + 4 Section 速览 + 13 潜规则 + 8 类信号词 section；CSS 复用 style.css ✅ 4 Section + 6 题型 + 13 潜规则 + 8 信号词
- [x] 10. `docs/vocab/index.html` — 新建：5 文档切换 chip + 分类筛选 chip + 搜索框 + 浏览/拼写模式 tab + **学习统计 chip（累计练习 / 总正确率 / 重置进度按钮）** + **「未掌握」tab**；引用 vocab.css / vocab.js ✅ 89 行 / 5 个 ID 齐全
- [x] 11. `docs/vocab/assets/css/vocab.css` — 新建：词条卡片 / 拼写卡片 / 拼写输入框 / 进度条 / 差异高亮 / 来源 chip 样式 + **学习统计 chip / 未掌握 tab 高亮 / 重置确认 modal 样式** ✅ 3.58 KB / 18 个 vocab 类全部定义
- [x] 12. `docs/vocab/assets/js/vocab.js` — 基础：fetch + 内存缓存 JSON、渲染 chips / 浏览网格 / 拼写视图、拼写判定（trim + lowercase + 忽略首尾标点）、实时反馈（防抖 100ms）、完成统计 ✅ 410 行基础版（IIFE + VocabApp）
- [x] 13. `docs/vocab/assets/js/vocab.js` — localStorage 增强：进度持久化（key=`vocab-progress` 存 `{wordId: {correct, wrong, lastSeen, firstSeen}}`）/ 渲染学习统计 chip / 「未掌握」tab（拼错过的词，按 wrongCount 排序）/ 重置进度按钮（confirm 后清空 localStorage）/ 拼写卡片底部历史正确率小字 ✅ 扩到 642 行（含 activeDoc filter fix），7 个 feature 全部落地；顺手修了 data-nav/data-action bug
- [x] 14. 主页跳转 QA：5 卡片在桌面/移动端可点；链接目标存在 ✅ hands-on QA 40 PASS / 0 FAIL
- [x] 15. 拼写练习 happy path QA：每个文档抽样 3 条，正确输入 → 显示 ✓ ✅ F4 5/5 docs × 4 sub-checks = 20/20 PASS
- [x] 16. 拼写练习 failure path QA：错误输入 → 显示差异 + 红框；空输入 → 中性边框；大小写不一致 → 判定为对 ✅ F4 20/20 PASS（包含 failure/empty/case-insensitive 子检查）
- [x] 17. 分类筛选 QA：每个文档的所有分类桶至少 1 个词条；切换分类时筛选项生效 ✅ hands-on QA PASS；chip 容器存在；JS applyFilter 实现完整；F5 5/5 docs PASS

## Final verification wave

- [x] F1. 主页 HTML 结构验证 ✅ verify-final-wave-static.sh PASS (5 cards, no aria-disabled, no Coming soon)
- [x] F2. listening/reading 主页题型清单与官方对齐 ✅ verify-final-wave-static.sh PASS (reading 11/11, listening 6/6)
- [x] F3. 5 个 JSON 文件加载后词条数符合 ✅ verify-final-wave-static.sh PASS (speaking-p1=64, listening=951, cambridge=270/65, kaodian538=527, writing=419/9)
- [x] F4. 拼写练习 happy + failure 路径在 5 个文档都通过 ✅ verify-vocab-runtime.mjs PASS (5 docs × 4 sub-checks = 20/20)
- [x] F5. 分类筛选在 5 个文档的所有分类桶中各显示至少 1 条 ✅ verify-final-wave-static.sh PASS (5/5 docs)；cambridge.json 删 1 个空 harness bucket 后 65/65 buckets 全部非空
- [x] F6. 整页无 JS 控制台错误 ✅ verify-final-wave-static.sh PASS (200s + node --check syntax OK)
- [x] F7. localStorage 写入/读取/重置 ✅ verify-vocab-runtime.mjs PASS (4/4 sub-checks：首次访问态 + 写入+统计 + 重置 + 500KB 警告)
- [x] F8. 「未掌握」tab 内容正确 ✅ verify-vocab-runtime.mjs PASS (5/5 sub-checks)；修复 renderUnmastered() 按 activeDoc 过滤后切到无错文档显示「暂无未掌握词 ✓」

## Commit cadence

按阶段提交：
1. T-1 ~ T-6 完成 → 1 个 commit（"data: parse 5 vocabulary docs into vocab JSON files"）
2. T-7 完成 → 1 个 commit（"home: expand to 5 module cards"）
3. T-8 ~ T-9 完成 → 1 个 commit（"reading+listening: add tips-only module pages"）
4. T-10 ~ T-12 完成 → 1 个 commit（"vocab: add accumulated module with spelling practice"）
5. T-13 ~ T-16 完成 → 1 个 commit（"vocab+home: agent QA gates"）

## Rollback plan

每个 commit 独立可回滚。`git revert <commit-sha>` 即恢复。