## 📄 SKILL.md（主文件）

```
---
name: ielts-writing
description: IELTS 雅思写作模块教学与评分一站式 skill。当用户想了解雅思写作 Task 1（小作文）或 Task 2（大作文）的题型、写法、框架、评分标准，或希望按照目标分数段（5.5 / 6 / 6.5 / 7 / 7.5 / 8）生成符合该档次要求的范文 / 提纲 / 段落，或提交自己的作文请求按官方四项评分标准（Task Achievement/Response、Coherence & Cohesion、Lexical Resource、Grammatical Range & Accuracy）打分并给出改进建议时触发。覆盖动态图、静态图、地图题、流程图、混合图五种小作文题型，以及同意与否 / 正反观点 / 利弊比较 / 双边讨论 / 两问问题五种大作文题型。不适用于：口语、阅读、听力、口语陪练、雅思报名 / 培训机构选择。
---

# IELTS Writing 写作教学与评分 skill

## 概述

本 skill 是一个面向雅思写作模块（Task 1 + Task 2）的教学与产出助手。它把「方法论 + 评分量表 + 分档产出 + 评分反馈」封装成一个工作流，让 Agent 可以：

1. **教学**：解释小作文和大作文的题型、框架、句式、评分标准；
2. **生成**：按照指定目标分数段（5.5 / 6 / 6.5 / 7 / 7.5 / 8）写出符合该档次语言特征和框架要求的范文 / 提纲 / 段落；
3. **评分**：按官方四项评分标准对学生作文打分，输出每项分数、估测总分、问题清单和升级建议。

任何进入本 skill 的请求，都先走「意图路由」再进入对应能力的 SOP。

---

## 触发与意图路由

每次接到请求，先用下面这张决策表判断走哪个能力。如果用户一句话里同时包含多个意图（如"教我写并帮我写一篇 7 分的"），按顺序串起来执行。

| 用户意图关键词 / 动作 | 路由到 | 备注 |
|---|---|---|
| 「什么是 / 怎么写 / 评分标准 / 框架 / 句式 / 词汇 / 多少分 / 怎么提分」 | **教学模式** | 走 SOP-A |
| 「帮我写一篇 / 写个 7 分范文 / 出一段 / 给个提纲 / 模仿写作 / 生成」 | **生成模式** | 必须先追问目标分数段、Task 1/2、题型；走 SOP-B |
| 「帮我打分 / 估分 / 批改 / 评一下 / 看能得几分 / 评估作文」 | **评分模式** | 走 SOP-C |
| 「按这个话题给个 6 分的和 8 分的对比」 | **生成模式（对比）** | 在 SOP-B 基础上输出多个分数段样本 |
| 「教 + 写」组合 | **先教学再生成** | 教学一段后给出目标分数段范文 |
| 「写 + 评」组合 | **先生成再评分** | 给出范文后自评，并标注「目标分数 ≥ 真实估分」时的差距 |

> ⚠️ **追问最小集**：当用户没说清以下信息时，**一次追问** 同时要齐，再进入生成 / 评分：
> - Task 1（大作文 = Task 2，问「写大作文」即可）
> - 题型 / 题目（如果用户没给题，给一个该题型的真实常考题）
> - 目标分数段（默认 6.5）
> - 中文 / 英文输出（默认英文）

---

## 资源目录

按需加载：

- `references/band-descriptors.md` — 官方四项评分标准（TA/CC/LR/GRA）在 0–9 各分数段的描述。
- `references/task1-guide.md` — 小作文五种题型（动态图、静态图、地图题、流程图、混合图）完整框架 + 句式 + 词汇。
- `references/task2-guide.md` — 大作文五种题型（Agree/Disagree、Positive/Negative、Pros & Cons、Discuss Both Views、Two-part Question）完整框架 + 开头结尾模板 + 段落展开。
- `references/band-examples.md` — 同题 6 / 7 / 8 分范文对比样本（覆盖动效图 + 大作文 Opinion）。

---

## SOP-A：教学模式

### 适用场景

用户问"小作文怎么写 / 大作文有哪些题型 / 评分标准是什么 / 怎么从 6 提到 7"等知识性问题。

### 工作流

1. **判断 Sub-topic**：从用户问题的关键词定位：
   - 小作文 → 加载 `references/task1-guide.md`
   - 大作文 → 加载 `references/task2-guide.md`
   - 评分 / 分数 → 加载 `references/band-descriptors.md`
   - 提分 / 升级 → 同时加载上述三份 + `references/band-examples.md`
2. **结构化回答**：用"框架 → 评分对应 → 句式 / 词汇 → 常见坑"四段式回答。避免堆砌式罗列。
3. **落点**：最后给一个学生最容易立刻做对的动作（如"先把 Introduction 改成不漏 be 动词的版本"），让用户有抓手。

### 教学原则

- **可读性 > 炫技**：6.5–7 分文章不是晦涩难懂的文章，而是"好读 = 好文章"。
- **框架先行**：题型识别 → 套对应框架 → 开头明立场 → 段落"主题—理由—例证" → 结尾回应。
- **数据 / 论点先于语言**：先想清楚"写什么"，再考虑"怎么写"。
- **避免重复 LLM 已有能力**：不要给"要写得通顺"这种空话；要给"动态图必交代 6 类数据点（起点/终点/稳定段/峰谷/超越/例外）"这种可立刻执行的清单。

### 教学示例

**用户问**："雅思大作文 Agree/Disagree 怎么写？"

**回答骨架**：
1. 题型判断：出现 "Do you agree or disagree" → 同意与否。
2. 框架：开头（paraphrase + 明确立场，不能用 whether）→ 核心段 1（理由 1 + 例证）→ 核心段 2（理由 2 + 例证）→ 结尾（呼应 I / my opinion）。
3. 评分对应：TA 拿到 7 的关键是"clear position throughout + 充分展开"；CC 拿到 7 要"每段一个明确主题 + 衔接自然不机械"。
4. 常见坑：用 whether 开头、立场模糊、结尾不呼应。
5. 立刻可以做：找一个近年真题，写出开头段，看是否避免上述坑。

---

## SOP-B：生成模式

### 适用场景

用户说"帮我写一篇 / 写个 7 分范文 / 给个提纲 / 写一段"等。

### 工作流

1. **追问最小集**（见上），至少确认：Task 1/2、题型、目标分数段、是否需要中文释义。
2. **加载对应 references**：
   - Task 1 → `references/task1-guide.md`（按题型匹配段落）
   - Task 2 → `references/task2-guide.md`（按题型匹配开头 / 结尾模板）
3. **目标分数段 → 语言特征锁定**（关键！不能写"中等"分说成"高分")：

| 目标分数段 | 词汇特征 | 语法特征 | 框架/逻辑特征 |
|---|---|---|---|
| **5.5** | 基础话题词，偶有错误 | 简单句 + 少量复合句，错误较多 | 段落简单但有时缺逻辑 |
| **6** | 基础话题词 + 偶尔替换 | 简单/复杂混合，错误仍较多 | 信息有条理但衔接机械 |
| **6.5** | 同义替换稳定 | 多数复合句正确，少量错误 | 段落主题清晰，衔接较自然 |
| **7** | 灵活使用 less common 词汇 | 复杂结构控制好，错误少 | 明确立场 + 充分展开，每段一主题 |
| **7.5** | 精度 + 搭配熟练 | 多种复杂结构并控制准确 | 一致性强，每段独立成段 |
| **8** | 精准 + 偶尔 idiomatic | 语法几乎无错，多种结构 | 完整回应 + 清晰立场 + 充分支持 + 段落圆润 |

4. **按题写作**：
   - **Task 1**：按"Introduction → Overview → Body 1 → Body 2 (→ Body 3)" 四段式。
   - **Task 2**：按"Introduction → Body 1 → Body 2 → (Body 3) → Conclusion" 结构。
5. **字数控制**：默认 Task 1 ≈ 170–190 词，Task 2 ≈ 270–290 词，避免过短或过长。
6. **结尾给三样东西**：
   - 范文（英文）
   - 范文逐段简短解释（中文 1–2 句，说明该段对应评分标准哪一项）
   - 关键词 / 替换词 / 句式清单（便于学生背诵）

### 生成原则（必须遵守）

- **不允许伪造数据**：若用户没给图表，先追问；不要给假数据假装有图。
- **不允许跑题**：每段都明确回应题目问题。
- **不允许气压低**：如果目标分数段是 7，但用户给了 5.5 的水平，按 7 写，但提醒"这是 7 分范本，你需要 5.5 的简化版吗？"。
- **必须输出语言特征自检表**：列出本范文在 TA / CC / LR / GRA 四项上的具体体现，让学生看到"为什么是 7 分"。

### 升级生成：当用户问"6 分和 8 分对比"

输出同题两份范文（一份 6，一份 8），并附"差异对照表"——逐项对比词汇、句式、衔接、立场清晰度。

---

## SOP-C：评分模式

### 适用场景

用户提交作文（无论 Task 1 / Task 2）请求打分。

### 工作流

1. **确认作文基本信息**：
   - Task 1 / 2？
   - Academic / General Training？（影响评分标准是 TA 还是 TR）
   - 字数？（太短会被扣 TA）
   - 用户希望在哪个分数段？如果不提，默认按"客观估分"。
2. **加载对应 references**：
   - 评分细节 → `references/band-descriptors.md`
   - 同题分数段对比 → `references/band-examples.md`（如果该题有现成样本）
3. **四项独立评分**：每项给 0–9 分（可半档），评估依据分别列出。
4. **估测总分**：
   - Task 1 与 Task 2 平均 → 写作最终分。
   - 半年内四舍五入规则：.25 → up, .75 → up（与官方一致）。
5. **输出四件套**：

#### 5.1 四项评分表

| 评分项 | 估测分 | 关键证据（原文引用加分析） |
|---|---|---|
| Task Achievement / Response | 6.5 | ... |
| Coherence & Cohesion | 6.0 | ... |
| Lexical Resource | 7.0 | ... |
| Grammatical Range & Accuracy | 6.5 | ... |
| **Task 总分** | **6.5** | （四项平均） |

#### 5.2 问题清单（按严重程度排序）

- **致命问题**（影响 TA 拿到 7+）：漏单位、立场模糊、字数不足 150/250。
- **重要问题**（限制单档小分）：连接词机械、动词形式不一致、残句。
- **小问题**（影响微观得分）：拼写、同义替换单调、个别介词。

#### 5.3 修改后范文（可选，但推荐）

- 把致命和重要问题修掉后的版本，按**目标分数段 +0.5** 写出来。
- 标注修改点（diff 风格说明）。

#### 5.4 升级路径（从当前分到下一档）

- 给出 3 条最关键动作（如"先把 AB 两段的功能关系用'Because / As a result'显式连接"）。
- 推荐针对性练习（题源 / 题型）。

### 评分原则

- **不要吹捧**：用户写出 5.5 分水平绝不评 7；偏差超过 1 档需要明确说明"为什么"。
- **不要套模板**：每条反馈都必须引用原文具体句子。
- **不要忽略 TA / TR**：字数、回应完整度、立场清晰度是最容易卡分项。
- **可读性优先**：反馈本身要条理清晰，让学生愿意读。

---

## 多轮修改

当用户对生成的范文或评分反馈提出修改意见时：

1. **先复述修改点**（确认理解一致）
2. **重新加载对应 references**
3. **再生成 / 再评分**，并标注相对于上一版的差异

避免出现"学生让改连接词，结果整个框架重写"的情况。

---

## 工作流示例

### 示例 1：用户问"小作文动态图怎么写"

→ 加载 `references/task1-guide.md` 中动态图部分 → 用"框架 → 6 项必交代数据 → 三大误区 → 句式清单"四段式回答 → 收尾给一个 7 分范本骨架。

### 示例 2：用户问"帮我写一篇 7 分大作文，话题是政府是否应优先教育"

→ 追问：题目是 Agree/Disagree 还是 Discuss Both Views？目标分数段（默认 7）。若用户没给题，给一个近年真题（如 2023 年 3 月 18 日真题）。
→ 加载 `references/task2-guide.md` 中 Agree/Disagree 模板。
→ 写 4 段式 7 分范文（约 280 词）。
→ 给出段落解释 + 关键词清单 + 4 项评分自检表。

### 示例 3：用户提交 Task 1 动态图作文并说"帮我打分"

→ 加载 `references/band-descriptors.md` + `references/task1-guide.md`。
→ 输出四项评分表 + 问题清单 + 修改后范文 + 升级路径。
```

------

## 📄 references/band-descriptors.md

```
# 官方四项评分标准详解（Task 1 / Task 2）

> 数据来源：British Council / IDP 官方公开版（IELTS Writing Band Descriptors, Public Version）+ Cambridge Assessment English。

## 评分框架

四项标准各占 25%，每项独立 0–9 分（可半档），最终 Task 分 = 四项平均，按 .25 / .75 规则取整。
```

总 Writing 分 = (Task 1 平均 + Task 2 平均 × 2) / 3

```
**.25 规则**：.25 → 进位到上半档；.75 → 进位到下一整数档。

---

## 一、Task Achievement (Task 1) / Task Response (Task 2)

### Task 1 — Task Achievement

| Band | 描述 |
|---|---|
| **9** | 完全满足任务要求，呈现完整展开的回应。 |
| **8** | 充分覆盖所有要求；清晰呈现并图示关键特征 / 要点。 |
| **7** | 覆盖任务要求；（Academic）清晰呈现主要趋势 / 差异 / 阶段总览；（GT）目的清晰、语气一致；（AC/GT）呈现关键特征但不充分展开。 |
| **6** | 回应任务要求；（Academic）总览存在但选材可更恰当；（GT）目的基本清晰，语气偶有不一致；呈现关键特征但细节可能不相关 / 不准确。 |
| **5** | 一般性回应任务；格式偶有不合适；（Academic）机械复述细节、无清晰总览；（GT）目的时有不清晰；呈现关键特征但覆盖不足。 |

### Task 2 — Task Response

| Band | 描述 |
|---|---|
| **9** | 完全回应任务所有部分；全程贯穿明确立场，并充分展开；无无关内容。 |
| **8** | 充分回应所有部分；立场清晰、有支撑；偶有轻微不相关内容或推理略欠展开。 |
| **7** | 回应所有部分但覆盖程度不一；立场清晰但结论或理由偶有未充分展开。 |
| **6** | 回应任务但主要观点可能不清晰、重复或不完全相关；立场可能不清晰 / 不一致。 |
| **5** | 部分回应任务；可能偏题；观点有限、展开不充分；细节可能不相关。 |

### TA/TR 关键扣分点

- **字数**：Task 1 < 150 / Task 2 < 250 必扣；每少 10 词扣 1 分。
- **Overview 缺失**：Task 1 Academic 必须有"无数据的趋势概述段"。
- **立场模糊**：Task 2 全程未明示自己的观点。
- **回应不完整**：Two-part Question 只答一问必扣。

---

## 二、Coherence & Cohesion (CC)

| Band | 描述 |
|---|---|
| **9** | 衔接使用不引起注意；段落安排完美服务于论点。 |
| **8** | 信息与观点逻辑排列；全面管理衔接；段落使用恰当。 |
| **7** | 逻辑组织信息与观点；全程有清晰推进；多样衔接恰当使用但偶有过度 / 不足。 |
| **4** | 无法提供清晰组织；衔接极少；分点杂乱。 |
| **6** | 信息排列连贯，有整体推进；衔接有效但句内 / 句间欠连贯或机械；指代可能不清晰。 |
| **5** | 信息组织但整体推进不足；衔接不准确 / 过度使用；缺乏指代造成重复。 |

### CC 关键扣分点

- **每段开头都是 "Firstly / Secondly / Moreover"**：机械衔接。
- **段落内有两个不相关论点**：段落主题不清。
- **代词指代不清**："this" / "these" 指代不明。
- **段落数 = 句子数 = 1 段=1 段**：每段都应有 2+ 句。

### CC 6 → 7 升档关键

- 每段一个明确主题句（Topic Sentence）。
- 用代词 / 指示词 / 同义词链避免重复。
- 替换机械 "firstly / moreover" 为更自然的衔接。

---

## 三、Lexical Resource (LR)

| Band | 描述 |
|---|---|
| **9** | 词汇范围广，词汇特征自然、精细控制；极少轻微错误。 |
| **8** | 词汇范围广、流畅灵活传达精确含义；熟练使用不常见词汇但偶有不准确；拼写 / 词形错误极少。 |
| **7** | 词汇范围足够灵活精准；使用不常见词汇有风格 / 搭配意识；词选 / 拼写 / 词形偶有错误。 |
| **6** | 词汇范围对任务足够；尝试使用不常见词汇但有不准确；词形 / 拼写错误但不阻碍沟通。 |
| **5** | 词汇范围有限但最低够用；拼写 / 词形错误明显，可能给读者造成困难。 |

### LR 关键扣分点

- **错误搭配**："do a decision"、"economical growth" → 必扣分。
- **不规范缩写 / 口语**："wanna"、"gonna" → 0 分。
- **拼写错误反复**：同一词反复错，标记为"系统性错误"。
- **重复用词**：同一名词 / 动词反复出现而不替换。

### LR 6 → 7 升档关键

- 学**搭配**（collocations）而非单词："make a decision"、"pose a threat"、"raise awareness"。
- 用同义词避免重复，但要"准确" > "花哨"。
- 写作时检查是否有一个错词反复出现。

---

## 四、Grammatical Range & Accuracy (GRA)

| Band | 描述 |
|---|---|
| **9** | 结构范围广，完全灵活准确；极少轻微错误。 |
| **8** | 结构范围广；多数句子无错误；极少错误或不恰当。 |
| **7** | 多种复杂结构；频繁无错句；语法与标点控制良好但偶有错误。 |
| **6** | 简单与复杂句混合；语法与标点错误但罕见阻碍沟通。 |
| **5** | 结构范围有限；尝试复杂句但较简单句更不准确；语法错误频繁。 |
| **4** | 极少结构；主谓一致 / 时态错误频繁；少于 50 词。 |

### GRA 关键扣分点

- **残句（Sentence Fragment）**："A followed very closely by B。" → 分词无主句，直接扣到 5.5。
- **主谓不一致**：单复数错误。
- **时态错误**：动态图描述在过去时态，概述段在现在时态。
- **冠词错误**："take a action"、"important role in the society"。
- **介词错误**：高频但易错。

### GRA 6 → 7 升档关键

- **每段至少 1 个定语从句 / 条件句 / 被动语态**。
- **避免残句**：先主谓后右扩，复杂结构（定语 / 同位语 / 分词 / 介词短语）全放句末。
- **每句 2–3 组信息**：超过 3 组 → 切分。
- **优先准确而非复杂**：4 句复杂句对 2 错 1 算 6.5，4 句全对才算 7。

---

## 五、四项分数组合对总分的影响

| TA/TR | CC | LR | GRA | 平均 | 总分 |
|---|---|---|---|---|---|
| 7 | 7 | 7 | 7 | 7.0 | 7.0 |
| 7 | 6 | 7 | 7 | 6.75 | 7.0 |
| 7 | 6 | 6 | 7 | 6.5 | 6.5 |
| 6 | 6 | 6 | 6 | 6.0 | 6.0 |
| 8 | 7 | 7 | 7 | 7.25 | 7.5 |
| 8 | 8 | 7 | 7 | 7.5 | 7.5 |

> ⚠️ **木桶效应**：四项中最低项往往决定总分上限。要冲 7，四项均要 ≥ 6.5。

---

## 六、整体卷面分数 → 写作能力对照

| 总分 | 能力描述 |
|---|---|
| 9 | 专家级：完全掌握，精准、流利、复杂论证。 |
| 8 | 良好：完全掌握，仅偶有非系统性不准确；处理复杂论证良好。 |
| 7 | 良好：操作掌握，偶有不准确；处理复杂语言良好。 |
| 6 | 胜任：尽管有不准确仍有效；熟悉情境有合理复杂语言。 |
| 5 | 中等：部分掌握；处理整体意义；错误多；自身领域基本沟通。 |
| 4 | 有限：基础能力限于熟悉情境；经常出错。 |
| 3 | 极有限：仅传达一般意义；频繁沟通中断。 |
| 2 | 间歇：理解英语有严重困难。 |
| 1 | 非使用者：除几个孤立词外无能力。 |
| 0 | 未尝试。 |
```

------

## 📄 references/task1-guide.md（小作文指南）

```
# Task 1（小作文）完整指南

> 适用：Academic 与 General Training A 类（图表题）。GT 书信不在本 skill 范围内。

## 一、四大段落总框架

| 段落 | 功能 | 长度 |
|---|---|---|
| **Introduction** | 同义改写题目 + 介绍图表 | 1–2 句 |
| **Overview** | 概括主要趋势 / 关键特征（**不带具体数据**） | 1–2 句 |
| **Body 1** | 第一组数据 / 第一类特征 | 3–5 句 |
| **Body 2** | 第二组数据 / 第二类特征 | 3–5 句 |
| **（Body 3）** | 可选：第三组数据 | 3–5 句 |

总字数控制在 **170–190 词**，复杂图可放宽至 220。

---

## 二、五种题型拆解

### 1️⃣ 动态图（Line / Bar over Time）

**识别**：时间维度 + 多个变量变化。

**Overview 写什么**：
- 哪些线 / 类别整体上升 / 下降。
- 哪些保持稳定。
- 一头一尾（即起点和终点）的主趋势，**不写具体数字**。

**分段方法**：

| 数据条数 | 分段 |
|---|---|
| 2 条线 | 一条线一段 |
| **3 条线 / 3 个时间点** | **黄金分段**：一条线 / 一个时间一段 |
| 4+ 条线 | 按相似趋势分组（增长快的归一段，慢的归一段） |

**必交代 6 项数据点**（漏一个就可能卡 6）：

1. **起点**（Starting point）
2. **终点**（Ending point）
3. **稳定段**（Plateau / Unchanged period）
4. **Peak / Bottom**（峰 / 谷）
5. **超越 / 交点**（Crossover）
6. **波动例外**（如有）

**6 分保底线**：起点、终点、稳定段。
**7 分及以上**：叠加超越、焦点、快慢对比。

**Topic Sentence 模板**：
- `Beginning with ..., ...`
- `Continuing with ..., ...`
- `Turning to ..., ...`

**趋势词汇**：

| 类型 | 动词 |
|---|---|
| 上升 | increased, rose, climbed, grew, surged, soared |
| 下降 | declined, decreased, fell, dropped, plunged, slumped |
| 稳定 | remained unchanged, plateaued, levelled off, stabilised |
| 波动上升 | increased gradually with mild fluctuations |
| 波动下降 | declined with fluctuations |
| 预测 | is expected to / is projected to / is estimated to |

**超越关系 4 种表达**：

| 形式 | 示例 |
|---|---|
| 动词 | A overtook B / A surpassed B |
| 被动 | A was overtaken by B（用过去分词） |
| 介宾 | reaching over / exceeding / surpassing |
| 同义替换 | had the largest figure / became the dominant sector |

**写法范例**：

> The line chart illustrates how many jobs were in different sectors of the economy in the US from 1960 to 2020.
>
> Overall, healthcare and technology saw dramatic growth, while manufacturing and agriculture both declined steadily over the period.
>
> Beginning with healthcare, the figure rose from around 5 million in 1960 to a peak of over 20 million by 2020. After a brief plateau in the 1990s, it continued its upward trajectory.
>
> Turning to manufacturing, the sector experienced a steady decline from approximately 20 million to under 12 million, with the steepest drop occurring in the 1980s.

---

### 2️⃣ 静态图（Bar / Pie / Table）

**识别**：单时间点 / 多类别对比。

**Overview 写什么**：
- 最大 / 最小类别。
- 类别间整体分布特征。

**分段方法**：
- 按类别分段（每个类别一段）。
- 按大小关系分段（最大的归一段，最小的归一段）。
- 3–5 个类别 → 通常 2 段。

**必备要素**：
- 单时间点数据（无起点 / 终点 / 趋势）。
- 避免出现过去时态，全部现在时。
- 约数词 + 单位 + 主语（"approximately 53% of respondents"）。

**核心动词**：
- 占比主导：A accounted for ... / A dominated ...
- 描述：A represented / comprised / made up ...
- 比较：A was twice as large as B / A was similar to B

**写法范例**：

> The pie chart shows the distribution of household expenditure across five categories in 2020.
>
> Overall, housing accounted for the largest share of spending, while education and healthcare together represented less than 20%.
>
> Housing was by far the most significant category, consuming approximately 35% of total household budgets, followed by food at around 20%. By contrast, education accounted for only 8%, with healthcare close behind at 7%.
>
> Transportation and leisure together made up the remaining 30%, with transportation slightly higher at 16% compared to leisure's 14%.

---

### 3️⃣ 地图题（Map）

**识别**：两张或多张地图，同一地点不同时间。

**核心特征**：功能不变，重点是**变化**（新增 / 拆除 / 改造）。

**分段方法**：按时间分段（变化前 vs 变化后）。

**Overview 写什么**：
- 总变化趋势（"the area was significantly redeveloped"）。
- 主要变化方向（向某方向扩建 / 拆除 / 改造）。

**必交代词**：

| 类别 | 词汇 |
|---|---|
| 新增 | built, constructed, added, established, developed |
| 拆除 | demolished, removed, cleared |
| 改造 | converted, transformed, replaced, renovated |
| 位置 | in the north / south / east / west of the map; adjacent to; opposite; in the corner |

**字数**：150–220 词。地图题容易写超，需控制。

**写法范例**：

> The two maps show the changes that took place in a coastal town between 2000 and 2020.
>
> Overall, the town experienced significant redevelopment, with the addition of several new facilities and the removal of older structures.
>
> In 2000, the town centre was dominated by a large market square, with a small number of residential houses to the north. A primary school was located in the south, adjacent to a large park.
>
> By 2020, the market square had been demolished and replaced with a modern shopping mall. The residential area had been expanded to the east, while the original school had been converted into a community centre. A new hospital was constructed in the south-west corner, replacing the park.

---

### 4️⃣ 流程图（Process / Flow Chart）

**识别**：步骤、生产流程、循环、自然现象过程。

**总框架**：

| 段落 | 内容 |
|---|---|
| Introduction | 改写题干描述，明确是什么流程 |
| Overview | 步骤数 + 起点与终点（"Overall, the process consists of X steps, starting with ... and ending with ..."） |
| Body 1 | 前半步骤 |
| Body 2 | 后半步骤 |

**三种类型**：

| 类型 | 特点 | 写法 |
|---|---|---|
| 线性流程图 | 有明确起止 | 写明从 X 到 Y，加数字 |
| 循环流程图 | 无明确终点 | "the process is a cycle" / "cycle consists of N steps" |
| 双图对比 | 两个相关流程 | 每图一段，对比步骤数量 |

**水字数技巧（流程图最难凑字数）**：

1. **精细描述**：每个能看见的元素都写出来。
   - 工具：harvester, crusher, machine, conveyor belt, funnel
   - 操作者：navigated by a person, operated by a worker
   - 运输：car, truck, airplane
   - 产品：cups, boxes, T-shirts, recyclable bags
2. **分词（V-ing）衔接前因后果**：水字数 + 提语法分。
3. **使用工序结果动词**：making / leading to / resulting in / causing / giving rise to

**遇到生词怎么办**：
- 通过上下文推断词性（观察并列词为动词 → 判断为动词）。
- 推断出词性后即可在句中作谓语使用。

**写法范例**：

> The diagram illustrates the process by which recycled paper is manufactured from used cardboard.
>
> Overall, the process consists of six main steps, beginning with the collection of waste paper and ending with the packaging of finished goods.
>
> In the first stage, used cardboard is collected from households and delivered by truck to a recycling facility. The cardboard is then sorted by hand and placed on a conveyor belt leading to a large crusher.
>
> Once crushed, the material is mixed with water and chemicals in a container, producing a wet pulp. This pulp is then pressed into thin sheets, dried, and cut into smaller pieces, before being packed into boxes for distribution.

---

### 5️⃣ 混合图（Mixed Chart）

**识别**：两张相关图表组合（一张占比 + 一张变化率 / 一张占比 + 一张满意度 等）。

**Overview 写法**：
- 第一句：第一张图核心特征。
- 第二句：第二张图核心特征。
- 拼在一起收尾。

**分段策略**：

| 情况 | 分段 |
|---|---|
| 常规情况 | 一图一段 |
| 数据量极度不均衡 | 两图间有必然关系 → 按关系分段 |

**三大经典混合组合**：

1. **占比 + 满意度（满意度陷阱）**：
   - 满意度图必须用 users / people / customers 作主语。
   - "satisfied" 是形容词，不能作主语。

2. **占比 + 薪资（海量数据）**：
   - 注意分类维度（salary group / age group）。
   - 准备处理大量比大小。

3. **占比 + 变化率（按关系分段）**：
   - 单独写变化率一段不合理 → 变化率贴回对应项目。
   - 推荐按项目分组（5 组），组内交代占比 + 变化率 + 排名。

---

## 三、通用高分句式

### 同义替换模板

| 原题 | 改写 |
|---|---|
| The graph shows ... | The line graph illustrates / The chart demonstrates ... |
| The number of tourists visiting | How many tourists visited（名词性从句） |
| between 2010 and 2017 | over a seven-year period |
| different activities | five activities（直接列出） |
| below | 删掉（写作时没有图在下方） |

### 复杂结构

| 句型 | 例 |
|---|---|
| 上升 + 最高点 | increased to reach a peak of / increased, reaching a peak of |
| 下降 + 最低点 | dropped to hit a low of / dropped, hitting a low of |
| 交点 | A and B stood at the same level / The figure for A dropped to meet that of B |
| 超越 | surpassing martial arts to become the second largest in 2015 |
| 时间顺序 | Before / After which / After that |

### 衔接手段

- **代词**：it / the figure / this number / the data
- **非限定性定语从句**：which / that 指代前文
- **镜像表达**：This trend was mirrored by ...
- **时间顺序副词**：Initially / Subsequently / Eventually

---

## 四、常见错误与避坑

| 错误类型 | 错误示例 | 正确做法 |
|---|---|---|
| 介宾短语缺主语 | "Beginning with the number of jobs in healthcare, which was the lowest..." | "It was the lowest, beginning with the number of jobs in healthcare..." |
| 并列句谓语不一致 | "A overtook B and overtaking C" | "A overtook B and overtook C" |
| Overview 写细节 | 概述里写"先升后降" | 只写一头一尾主趋势 |
| 漏数据 | 不写中间稳定段 | 必交代起点、终点、稳定段、峰谷 |
| 残句 | "A followed very closely by B." | "A was followed closely by B."（补主谓）|
| 满意度图主语错误 | "Very satisfied was 65%." | "Very satisfied users accounted for 65%." |

---

## 五、提速技巧

掌握 **先主谓后右扩 + 比大小法**，整篇可控制在 **190–200 词**。

- **先写主谓**：早抛主谓防残句。
- **复杂结构置右**：定语、同位语、分词全放句末。
- **比大小法**：固定主语 + 动词 + 形容词最高级 + than + 对比对象。
```

------

## 📄 references/task2-guide.md（大作文指南）

```
# Task 2（大作文）完整指南

> 适用：Academic 与 General Training 大作文（约 250 词及以上，40 分钟）。

## 一、总框架

| 段落 | 功能 | 字数参考 |
|---|---|---|
| **Introduction** | Paraphrase 题目 + 明确立场 / 任务 | 2–3 句 |
| **Body 1** | 第一个理由 / 第一方观点 | 4–6 句 |
| **Body 2** | 第二个理由 / 另一方观点 / 第二个回答 | 4–6 句 |
| **（Body 3）** | 反方论证 / 第三个理由（可选） | 4–6 句 |
| **Conclusion** | 总结 + 重申立场 / 回应任务 | 2–3 句 |

总字数 **270–290 词**为安全区间。

---

## 二、五种题型详解

### ① Agree or Disagree（同意与否）

**典型问法**：
> Do you agree or disagree with this statement?
> To what extent do you agree or disagree?

**框架**：
```

Introduction: Paraphrase 题目观点 + 明确表态（I / my opinion）
Body 1: 理由 1 + 例证 / 背景
Body 2: 理由 2 + 例证 / 背景
Conclusion: 重申我的立场

```
**⚠️ 关键禁忌**：
- **不能用 whether**（whether 暗示"两种都有可能"）。
- 立场必须明确（agree / disagree / only partially agree）。

**开头模板**：
> The issue of [topic] has sparked considerable debate. While some argue that [opposing view], I maintain that [my position], for the following reasons.

**结尾模板**：
> In conclusion, I firmly believe that [my position] because [reason 1] and [reason 2].

**常见话题思路**：
- 教育：政府应否为学费买单 / 学生穿校服与否。
- 工作：远程办公好 / 坏 / 长期化。
- 环境：个人 vs 政府责任。

---

### ② Positive or Negative（积极 / 消极发展）

**典型问法**：
> Do you think this is a positive or negative development?

**框架**：与 Agree or Disagree **基本一致**，唯一区别：
- 开头回应"积极 / 消极"而不是"同意 / 不同意"。
- 立场陈述变成 "I think this is a positive / negative development"。

**开头模板**：
> The phenomenon of [topic] has become increasingly prevalent in recent years. From my perspective, this trend is largely a positive development, and I will outline my reasons below.

**结尾模板**：
> In summary, I consider this to be a positive development because [reason 1] and [reason 2].

---

### ③ Pros and Cons（利弊比较）

**典型问法**：
> Do you think the advantages outweigh the disadvantages?
> Discuss the advantages and disadvantages.

**框架**：
```

Introduction: Paraphrase + 暗示要做权衡
Body 1: 优点 (1–2 个)
Body 2: 缺点 (1–2 个)
Conclusion: 比较 + 给出权重判断（"On balance, I believe the advantages outweigh the disadvantages"）

```
**⚠️ 结论段必须做 comparison / 权衡**，不能只罗列优缺点。

**结论段权重比较的四个维度**：

| 维度 | 削弱方 | 增强方 |
|---|---|---|
| ① 缺点可否被解决 | 可解决 | 不可解决 |
| ② 影响时长 | 短期影响 | 长期影响 |
| ③ 影响范围 | 少数人 | 多数人 |
| ④ 微观 vs 宏观 | 仅对个人 / 社会有利 | 对两个层面均有利 |

**逻辑前提技巧**：
- 经济发展 vs 环境保护 → 建立"环保是经济发展的前提"的逻辑链。
- 适用于医疗、经济、教育等话题。

**开头模板**：
> The question of [topic] has both supporters and critics. While there are clear benefits, there are also notable drawbacks that deserve consideration.

**结尾模板**：
> On balance, I believe the advantages outweigh the disadvantages, because [权重判断理由]. Nevertheless, the drawbacks should not be entirely dismissed.

---

### ④ Discuss Both Views（双边讨论）

**典型问法**：
> Discuss both views and give your own opinion.

**框架**：
```

Introduction: Paraphrase + 呈现两个对立观点
Body 1: 第一个观点 (理由 + 例证)
Body 2: 第二个观点 (理由 + 例证)
Conclusion: 站边 / 分类讨论

```
**⚠️ 关键**：
- ✅ **可以用 whether**（因为需要呈现两种观点）。
- 给出两个观点的 paraphrase。
- 因为是双观点段落，每个观点的展开可以**不必像单观点那样充分**——理由部分可写得相对简略，以便容纳第二个观点。

**结尾两种策略**：

| 策略 | 适用 |
|---|---|
| **挑边站** | 题目明确要求"give your own opinion" |
| **居中站** | "在……情况下……，在……情况下……" |

**开头模板**：
> [Topic] is a contentious issue, with some people believing that [view 1], while others argue that [view 2]. Both perspectives carry weight and merit closer examination.

**结尾模板（挑边站）**：
> After considering both perspectives, I am more inclined to support [view X] because [理由].

**结尾模板（居中站）**：
> In my view, the validity of each argument depends on the context. In situations where [context A], [view 1] holds true; where [context B], [view 2] is more applicable.

---

### ⑤ Two-part Question / Problem & Solution（两问问题）

**典型问法**：
> What are the reasons for this? What can be done?
> Why is this the case? Is it a positive or negative trend?

**框架**：
```

Introduction: "The aim of this essay is to ... and ..."
Body 1: 回应第一个问题
Body 2: 回应第二个问题
Conclusion: 总结两个问题的答案

```
**⚠️ 关键**：
- 开头句型：**The aim of this essay is to…** + **and…**
- 明确点出两个要回答的问题。
- 如果第二问是 positive/negative：第二段开头要先交代立场，再展开论证。

**开头模板**：
> The aim of this essay is to analyse the causes of [problem] and to propose some effective solutions.

**结尾模板**：
> In conclusion, the main reasons for [problem] are [reason 1] and [reason 2], and I believe that [solution] would be the most effective way to address them.

---

## 三、单段落展开结构（所有题型通用）
```

主题句 (Topic Sentence)
↓
展开理由 (Reason)
↓
例证 / 对比 / 背景信息 (Example / Contrast / Background)

```
**展开方法**：

| 方法 | 模板 |
|---|---|
| 例证 | "For example, [specific case]" / "A clear example of this is ..." |
| 对比 | "In contrast, ..." / "Compared with ..., ... is ..." |
| 背景 | "This is because ... / The reason for this is that ..." |
| 让步 | "Admittedly, ... but ..." / "While it is true that ..., ..." |

**单观点段落**（如 Agree/Disagree）：每个部分都应展开充分。
**双观点段落**（如 Discuss Both Views）：每个理由部分可相对简略。

---

## 四、开头写法对比速查

| 题型 | 是否可用 whether | 开头核心动作 |
|---|---|---|
| Agree or Disagree | ❌ | Paraphrase + 明确表态 |
| Positive/Negative | ❌ | Paraphrase + 判断积极/消极 |
| Pros & Cons | ❌ | Paraphrase + 暗示权衡 |
| Discuss Both Views | ✅ | 呈现两个对立观点 |
| Two-part Question | ❌ | The aim of this essay is to ... and ... |

---

## 五、结尾写法对比

| 题型 | 结尾核心动作 |
|---|---|
| Agree/Disagree | 重申 I / my opinion |
| Positive/Negative | 重申 positive / negative |
| Pros & Cons | 比较 + 权重判断 |
| Discuss Both Views | 挑边 / 居中 |
| Two-part Question | 总结两个问题的答案 |

---

## 六、核心词汇与搭配

### 学习搭配（collocations）而非单词

| 常见话题 | 搭配 |
|---|---|
| 教育 | raise awareness, foster critical thinking, narrow the gap |
| 工作 | pose a threat to, secure employment, in the workplace |
| 环境 | at the expense of, contribute to, mitigate the impact |
| 媒体 | widespread belief, exert influence on, misinformation |
| 社会 | a sense of belonging, social cohesion, marginalised groups |

### 连接词清单

| 类型 | 词汇 |
|---|---|
| 相似 | similarly, likewise, in the same way |
| 对比 | but, however, in contrast, by contrast, conversely, on the other hand |
| 额外 | besides, also, in addition, additionally, furthermore, moreover |
| 因果 | because, due to, as a result, therefore, consequently, leading to |
| 让步 | admittedly, it is true that, granted, although, even though |
| 举例 | for example, for instance, a clear example of this is |
| 总结 | in conclusion, to sum up, on balance, all in all |

---

## 七、常见话题与思路

| 话题 | 核心论点方向 |
|---|---|
| **教育** | 个性化、批判性思维、教育公平、终身学习 |
| **工作** | 远程办公、自动化、就业稳定性、工作生活平衡 |
| **环境** | 个人 vs 政府责任、经济发展 vs 环保、可持续性 |
| **媒体** | 算法推荐 vs 传统媒体、假新闻、信息茧房 |
| **科技** | 隐私、AI、社交媒体成瘾、数字化 |
| **社会** | 老龄化、城市化、不平等、文化认同 |
| **政府** | 政策干预、税收、公共服务、监管 |
| **历史** | 文化认同、shared information、经验教训 |
| **健康** | 公共健康 vs 个人责任、医疗资源分配 |
| **犯罪** | 惩戒 vs 矫正、监禁有效性 |

---

## 八、常见错误与避坑

| 错误 | 后果 | 修正 |
|---|---|---|
| 立场模糊 | TR 扣分 | 开头明确表态 |
| 用 whether 开头但题型是 Agree/Disagree | 暗示了 ambiguous | 改为 "I firmly believe that ..." |
| 偏题 / 偷换概念 | TR 扣分 | 每段回应题目关键词 |
| 模板套话堆砌 | CC 扣分 | 避免 "It is undeniable that ..."、"Last but not least, ..." |
| 只答一个问题（Two-part） | TR 扣分 | 每问都要有独立段落 |
| 单段堆砌 5+ 句 | CC 扣分 | 拆成两段 |
| 句子超长（4+ 谓语） | GRA 扣分 | 拆分或用分词 / 定语右扩 |
| 拼写错误反复 | LR 扣分 | 消灭 2–3 个高频错词 |

---

## 九、答题流程（40 分钟）

| 时间 | 任务 |
|---|---|
| 0–2 min | 读题 + 识别题型 |
| 2–5 min | 头脑风暴立场 / 理由 |
| 5–8 min | 写提纲（开头立场 / Body 1 主题 + 论据 / Body 2 主题 + 论据 / 结尾） |
| 8–35 min | 写作（每段 5–7 分钟） |
| 35–40 min | 检查拼写、语法、动词形式、字数 |

---

## 十、提分关键动作

- **每段 1 个主题句 + 1 个理由 + 1 个例证**（标准 7 分段落）。
- **连接词准确性 > 多样性**。
- **每段至少 1 个复杂结构**（定语 / 条件 / 被动 / 分词）。
- **结尾必须呼应开头态度**。
- **考前 5 年真题头脑风暴 + 搭框架**（提升最快）。
```

------

## 📄 references/band-examples.md（各分数段范文对比）

由于内容较长（249 行），建议直接使用以下完整副本：

```
# 各分数段示例对比与自检表

> 用于：
> 1. **生成模式**——按目标分数段调整语言特征时参考。
> 2. **评分模式**——给学生反馈"你的作文是几分"时参考。
> 3. **教学模式**——讲"6 → 7 升级"时给学生看实例。

---

## 一、Task 1 动态图：6 / 7 / 8 分对比

**题目**：The line graph shows the number of tourists visiting a Caribbean island between 2010 and 2017.

### 6 分范文（约 165 词）

> The line graph shows the number of tourists visiting a Caribbean island from 2010 to 2017. There are two lines in the graph, one for total visitors and one for international visitors.
>
> Overall, the total number of tourists grew from 2010 to 2017, and international visitors also increased.
>
> In 2010, total visitors were about 1 million, and international visitors were about 0.5 million. The number of total visitors grew each year and reached about 2 million in 2017. International visitors also increased, but not as fast as total visitors.
>
> In 2015, the total number of tourists was about 1.7 million. International visitors were about 1 million in the same year.

**6 分特点**：
- ✅ Overview 存在但简单，几乎等于复述。
- ❌ 缺单位（约数词使用随机）。
- ❌ 趋势词汇单调（"grew"、"increased" 反复）。
- ❌ 缺超越 / 交点 / 稳定段 / 峰谷数据。
- ❌ 句式简单，多为简单句。

### 7 分范文（约 185 词）

> The line graph illustrates how many tourists visited a particular Caribbean island over a seven-year period from 2010 to 2017, distinguishing between total and international visitors.
>
> Overall, both categories experienced upward trends, with international visitors growing at a notably faster rate than the total number of tourists.
>
> Beginning with total visitors, the figure stood at approximately 1 million in 2010 and climbed steadily to around 2.2 million by 2017. The most significant growth occurred between 2014 and 2016, when the figure rose sharply from 1.5 million to nearly 2 million.
>
> International visitors, meanwhile, followed a similar but more pronounced trajectory. Starting at roughly 0.5 million in 2010, the number doubled to reach 1 million by 2014, and continued to climb to approximately 1.5 million by 2017. Notably, the gap between the two categories narrowed considerably over the period, suggesting that the island was becoming increasingly attractive to foreign tourists.

**7 分特点**：
- ✅ Overview 明确，无具体数字。
- ✅ 起点 / 终点 / 加速段 / 超越关系均覆盖。
- ✅ 趋势词汇多样（climbed, doubled, rose sharply, narrowed）。
- ✅ 复杂结构控制良好（分词 / 定语从句）。
- ✅ 段尾有"暗示意义"。

### 8 分范文（约 200 词）

> The line graph compares the total number of tourists visiting a Caribbean island with the proportion arriving from abroad, over the period from 2010 to 2017.
>
> Overall, the island saw a substantial rise in visitor numbers throughout the period, with international tourists accounting for an increasingly large share of the total.
>
> In 2010, the island welcomed approximately 1 million visitors, half of whom were international tourists. Total visitor numbers climbed steadily in the early years, reaching 1.5 million by 2013, before plateauing briefly between 2013 and 2014. From 2015 onwards, growth accelerated, culminating in a peak of just over 2.2 million visitors in 2017.
>
> The pattern for international visitors was even more striking. Beginning at around 0.5 million in 2010, this figure doubled within four years to reach 1 million in 2014. After a brief levelling off, international arrivals surged to an estimated 1.5 million by 2017, by which point they represented roughly 70% of all visitors—a significant increase from the 50% recorded at the start of the period.
>
> This shift suggests that the island's appeal to foreign tourists grew considerably, particularly in the second half of the period.

**8 分特点**：
- ✅ Overview 精准，有对比。
- ✅ 起点 / 终点 / 稳定段 / 加速段 / 峰值 / 比例变化都覆盖。
- ✅ 词汇精度高（plateauing, culminating, levelling off, surged, represents）。
- ✅ 复杂结构种类多（分词 / 定语从句 / 同位语）。
- ✅ 段尾有"分析性洞察"。
- ✅ 几乎无错误。

---

## 二、Task 2 大作文 Opinion 题型：6 / 7 / 8 分对比

**题目**：Some people think that the government should spend more money on providing free education for children under 18, while others believe that adult education deserves more funding. Discuss both views and give your own opinion.

### 6 分范文（约 280 词）

> The government has to decide whether to spend more money on education for children or adults. Some people think children should get free education, and others think adult education is more important.
>
> On the one hand, children's education is very important. Children are the future of the country, so they need good education. If the government gives free education for children, families can save money and children can study better. This is good for the development of the country.
>
> On the other hand, adult education is also important. Many adults did not have the chance to study when they were young, so they need to learn new skills now. If the government gives more money for adult education, adults can find better jobs and the economy can improve.
>
> In conclusion, both children's education and adult education are important. I think the government should spend money on both of them.

**6 分特点**：
- ✅ 回应了题目（双方 + 给出意见）。
- ❌ 立场模糊（"should spend on both"——典型 6 分结尾）。
- ❌ 词汇基础（"important" 反复出现 5 次）。
- ❌ 语法正确但简单（多为简单句与 and 连接的并列句）。
- ❌ 例子 / 论据泛泛而谈（"the country can develop"）。
- ❌ 拼写 / 语法小错误（"childern" 等）。

### 7 分范文（约 290 词）

> The question of how education funding should be allocated between children and adults has generated considerable debate. While both groups undoubtedly benefit from educational investment, I believe that governments should prioritise free education for children under 18, for the following reasons.
>
> Firstly, education during childhood lays the foundation for lifelong learning. Research consistently shows that early educational experiences shape cognitive development and academic aptitude, which in turn influence future career prospects. By contrast, adults who missed educational opportunities earlier in life often face significant barriers when attempting to return to study, including family responsibilities and financial constraints.
>
> Secondly, investing in children's education yields long-term societal returns. A well-educated population contributes to a more skilled workforce, higher productivity, and greater social mobility. While adult education also produces benefits, the impact is typically more immediate and limited to individual learners, whereas children's education shapes the entire next generation.
>
> Admittedly, adult literacy programmes address urgent needs, particularly for those seeking to improve their employability. However, I would argue that these programmes are more effective when delivered alongside strong school education, as adults often serve as role models and motivators for their children's learning.
>
> In conclusion, while I acknowledge the value of adult education, I am convinced that prioritising children's education under 18 produces greater and more lasting benefits for both individuals and society as a whole.

**7 分特点**：
- ✅ 立场明确（"prioritise free education for children"）。
- ✅ 每段一个明确主题 + 理由 + 例证 / 对比。
- ✅ 词汇丰富（undoubtedly, cognitive development, academic aptitude, constraints, prioritise, allocate）。
- ✅ 复杂结构多样（让步从句 / 介词短语 / 分词结构）。
- ✅ 结尾呼应开头立场。
- ✅ 让步段处理得当（"Admittedly" + "However"）。

### 8 分范文（约 290 词）

> The allocation of public funding between primary and adult education remains a contested policy issue. While I accept that adult literacy programmes serve a vital social function, I would argue that governments should prioritise compulsory education for children under 18, both for the immediate developmental benefits and the long-term societal dividends.
>
> The strongest case for prioritising children's education lies in its preventive character. Investment during the formative years equips young people with foundational skills—literacy, numeracy, and critical thinking—that subsequently reduce the need for remedial adult education. Conversely, omitting this early investment tends to entrench educational disadvantage, as adults without basic qualifications face increasingly limited employment prospects in modern knowledge economies. In short, childhood education addresses the root cause, whereas adult programmes merely treat the symptoms.
>
> Furthermore, the multiplier effect of children's education is difficult to overstate. Educated individuals tend to make more informed health and financial decisions, contribute more productively to the economy, and pass on educational values to their own children. This intergenerational impact stands in stark contrast to adult education, the benefits of which, while real, are largely confined to individual participants.
>
> I do not discount the genuine importance of adult education, particularly for second-chance learners seeking to improve their employment prospects. However, such programmes can be more effectively delivered alongside, rather than in competition with, robust school education—a position reinforced by international evidence from countries that have successfully integrated both approaches.
>
> In conclusion, I remain firmly convinced that children's education under 18 should be the primary beneficiary of public funding, not because adult education lacks value, but because early investment prevents the very problems that adult programmes are designed to address.

**8 分特点**：
- ✅ 立场坚定且被反复强化。
- ✅ 论证有深度（"multiplier effect"、"preventive vs remediation"）。
- ✅ 词汇精度高（formative, multiplier effect, in stark contrast, root cause, entrench）。
- ✅ 复杂结构种类多（让步 / 介词 / 分词 / 同位语 / 强调句）。
- ✅ 段落间逻辑链清晰（"Furthermore"）。
- ✅ 拒绝模板套话。
- ✅ 几乎无错误。

---

## 三、6 → 7 升级关键差异表

| 维度 | 6 分 | 7 分 |
|---|---|---|
| **立场** | 模糊或两边都支持 | 明确但有让步空间 |
| **段落数** | 4 段但每段内容稀薄 | 4 段且每段有独立主题 |
| **例证** | 泛泛而谈 | 至少 1 个具体例（机构 / 数据 / 案例） |
| **让步** | 可能缺失或假模假样 | 1 段真实让步 + "However" 转折 |
| **词汇** | 基础话题词 + 偶尔替换 | 同义替换稳定 + 搭配熟练 |
| **句式** | 简单句 + 复合句混合 | 多种复杂结构 + 错误少 |
| **连接词** | 机械（"Moreover" 每段） | 自然（多样化衔接） |
| **结尾** | 重复总结 | 重申立场 + 加深论点 |

---

## 四、7 → 8 升级关键差异表

| 维度 | 7 分 | 8 分 |
|---|---|---|
| **论证深度** | 1 步推理（reason → example） | 2 步推理（reason → evidence → implication） |
| **词汇** | 灵活替换 | 精准 + 偶尔 idiomatic |
| **结构** | 多种复杂结构 | 多种复杂结构 + 强调句 / 倒装 / 虚拟语气 |
| **错误** | 偶有错误 | 几乎无错 |
| **段落圆润** | 段落相对独立 | 段落间有逻辑链条 |
| **原创性** | 标准框架 | 框架创新但不离题 |
| **TA 回应** | 充分 | 充分 + 提到对立观点已涵盖 |

---

## 五、生成模式自检表（不同分数段）

当用户要求生成 7 分范文时，写完后用这份清单自检：

### 7 分自检清单

- [ ] **TA**：明确立场 + 每一问都回应 + 例子具体？
- [ ] **CC**：每段 1 主题句 + 衔接自然不机械 + 段间有逻辑？
- [ ] **LR**：同义替换 ≥ 30% + 至少 3 个非基础搭配 + 拼写无错？
- [ ] **GRA**：≥ 3 种复杂结构 + 多数句子无错 + 每句 2–3 组信息？
- [ ] **结尾**：呼应开头 + 重申立场？

### 8 分自检清单

- [ ] **TA**：立场坚定 + 论证链 2 步 + 真实让步？
- [ ] **CC**：段落间逻辑链 + 衔接几乎不被注意？
- [ ] **LR**：精准搭配 + 偶尔 idiomatic + 段落中重复词 < 5%？
- [ ] **GRA**：多种复杂结构 + 几乎无错 + 偶尔高级结构（强调 / 倒装）？
- [ ] **结尾**：呼应 + 加深 + 升华？

---

## 六、评分模式自检表（评估学生作文用）

| 检查项 | 6 分特征 | 7 分特征 | 8 分特征 |
|---|---|---|---|
| Task 1 Overview | 简单复述 | 概括主要趋势 | 概括 + 提示意义 |
| Task 2 立场 | 模糊 / 折中 | 明确但有让步 | 坚定且有深度 |
| 数据覆盖 | 起点 / 终点 | + 稳定段 / 峰谷 | + 超越 / 暗示 |
| 词汇 | 基础 | 灵活替换 | 精准 + 偶尔 idiomatic |
| 句式 | 简单 + 复合 | 多种复杂 | 多种复杂 + 高级 |
| 错误 | 偶有 | 少 | 几乎无 |
| 字数 | 够 150/250 | 175-200 / 280-300 | 同 7 但每段紧凑 |

---

## 七、Task 1 范文共 7 分标准句库

**模仿这些句式即可稳定 7**：

### Introduction
> The line graph illustrates how many [subject] [verb] over a [duration] period from [start year] to [end year].
> The bar chart compares [A] and [B] in terms of [dimension] in [year].
> The pie chart shows the distribution of [subject] across [number] categories in [year].

### Overview
> Overall, [main trend 1], while [main trend 2].
> Overall, [A] experienced [general direction], while [B] saw [opposite direction].
> Overall, [subject] was dominated by [category], with [category] accounting for the smallest share.

### Body 主题句
> Beginning with [first category], ...
> Turning to [next category], ...
> [Category] followed a similar trajectory, with ...

### Body 趋势
> The figure rose from approximately X in [year] to around Y by [year], reaching a peak of Z in [year].
> The number remained stable at around X for [duration], before declining to Y in [year].
> [A] was overtaken by [B] in [year], and the gap continued to widen thereafter.

### 收尾
> This trend was mirrored by the increase in [other category].
> Notably, the gap between the two categories narrowed significantly over the period.

---

## 八、Task 2 范文共 7 分标准句库

### Introduction
> The issue of [topic] has sparked considerable debate. While some argue that [opposing view], I maintain that [my position], for the following reasons.
> [Topic] has become an increasingly important concern in contemporary society. From my perspective, this development is largely [positive/negative], and I will outline my reasons below.

### Body 主题句
> The first reason is that [broad statement].
> A more compelling argument, however, concerns [topic].
> Admittedly, [concession] cannot be ignored, but [rebuttal].

### Body 理由 + 例证
> This is primarily because [reason]. For example, [example].
> The implications of this are far-reaching. [Specific case].
> [Comparative point]. In contrast, [comparison case].

### Conclusion
> In conclusion, I firmly believe that [restate position] because [reason 1] and [reason 2].
> On balance, the advantages outweigh the disadvantages, primarily because [weighting reason].
> After considering both perspectives, I am more inclined to support [view] because [reason].
```

------

## 📦总结

| 文件                               | 行数   | 用途                                                 |
| ---------------------------------- | ------ | ---------------------------------------------------- |
| **SKILL.md**                       | 218 行 | 主入口，定义意图路由 +三大 SOP（教学 / 生成 / 评分） |
| **references/band-descriptors.md** | 155 行 | 官方四项评分标准 5–9 分段详解                        |
| **references/task1-guide.md**      | 286 行 | 小作文 5 种题型框架 + 句式 + 词汇                    |
| **references/task2-guide.md**      | 297 行 | 大作文 5 种题型框架 + 开头结尾模板                   |
| **references/band-examples.md**    | 249 行 | 6 / 7 / 8 分范文对比 + 自检清单                      |