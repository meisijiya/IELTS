# Reading Paraphrase：6 大类型 + AWL 词族 + 学术边界标注

> 2026 版。**初稿「近 500 组同义替换高频词」无任何官方依据，已删除**。本文件改用学术权威词表（AWL 570 词族 / Oxford 3000-5000）+ 6 大类型 + 否定触发器 + 训练方法。所有「民间合并数字」均标注来源。

---

## ⚠️ 重要修正（必读）

### 初稿「近 500 组同义替换高频词」核验

**官方依据缺失**：

- 雅思 / Cambridge / British Council / IDP 任何官方资料均**未出现「近 500 组同义替换」**这一数字
- 最大可信词表是 **AWL（Academic Word List, Coxhead 2000）570 词族**
- 学术相关词表：BNC/COCA 词族（Nation）、Oxford 3000/5000、General Service List（West 1953）

**修正方案**：

- **不再引用「近 500 组」**
- 改用 **AWL 570 词族**作为底层学术词汇
- 6 大类型保留（这是学术上对替换方式的合理分类）
- 高频替换词清单按 **话题**分类（不引用总数字）

⚠️ **类似民间数字也应警惕**：「90% 替换」「80% 考点涉及替换」等表述均无官方依据。本文件用「绝大多数 P2/P3 考点涉及替换」作为更严谨表述。

---

## 一、6 大类型总览（学术分类）

> 6 大类型（词义/词性/上下义/解释/否定/句式）属于学术上对替换方式的合理分类，**不是雅思官方分类**。Cambridge IELTS 19/20/21 前言未提及此分类，但是英语学术写作常用的替换分析框架。

| 类型 | 定义 | 真题示例 |
|---|---|---|
| **1. 词义替换 Lexical** | 用同义词 / 近义词替换 | 题目 "important" → 原文 "significant" |
| **2. 词性转换 Grammatical** | 动词 ↔ 名词 / 形容词 等 | 原文 "vary" → 题目 "variation" |
| **3. 上下义替换 Hypernymy/Hyponymy** | 概括 ↔ 具体 | 原文 "animal" → 题目 "dog" |
| **4. 解释说明替换 Explanation** | 用一句解释替代原词 | 原文 "abandoned" → 题目 "stopped completely and never resumed" |
| **5. 否定 + 反义替换 Negation** | 正话反说 | 题目 "difficult" → 原文 "not easy" |
| **6. 句式结构替换 Structural** | 主动 ↔ 被动 / 简单 ↔ 复合 / 倒装 | 原文 "The result is X" → 题目 "X results from Y" |

**核心**：A 类 P2/P3 几乎**所有考点**都涉及替换——填空题答案词几乎从不在原文中原词出现；判断题题干与原文是同义替换关系；Heading 选项与段落主旨是同义替换。

---

## 二、AWL 570 词族（学术最权威词表）

### 简介

**AWL（Academic Word List, Coxhead 2000）** 是英语学术写作最权威的词表，覆盖学术文本中 10% 词频但不包含最常用 2000 词的非学科通用词族。

来源：[Victoria University of Wellington AWL](https://www.wgtn.ac.nz/lals/resources/academicwordlist)

### 6 大话题分类（AWL 子集）

AWL 570 词族按话题分为 28 个子类（参考 Coxhead 2000 论文）。以下是 **8 大话题**（按 IELTS 阅读高频话题整合）：

#### 话题 1：教育 / 学习（Education）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| achieve | achievement / achievable | accomplish / attain |
| assess | assessment / assessable | evaluate / appraise |
| comprehend | comprehension / comprehensive | understand / grasp |
| confer | conference / conferred | consult / discuss |
| define | definition / definite | specify / clarify |
| educate | education / educational | instruct / teach |
| establish | establishment / established | found / create |
| instruct | instruction / instructive | direct / teach |
| perceive | perception / perceptible | notice / observe |
| presume | presumption / presumably | assume / suppose |

#### 话题 2：研究 / 方法（Research）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| analyse | analysis / analytical | examine / study |
| data | datum / database | information / statistics |
| demonstrate | demonstration / demonstrable | show / prove |
| evaluate | evaluation / evaluative | assess / appraise |
| examine | examination / examined | inspect / analyze |
| experiment | experimental / experimentation | test / trial |
| hypothesis | hypothetical / hypothesize | theory / assumption |
| interpret | interpretation / interpretive | explain / clarify |
| investigate | investigation / investigator | explore / study |
| method | methodology / methodical | approach / procedure |

#### 话题 3：环境 / 自然（Environment）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| climate | climatic | weather / atmospheric |
| conserve | conservation / conservative | preserve / protect |
| contaminate | contamination / contaminant | pollute / taint |
| degrade | degradation / degraded | deteriorate / erode |
| ecology | ecological / ecologically | environment / ecosystem |
| emit | emission / emitted | release / discharge |
| environment | environmental / environmentally | surroundings / habitat |
| fluctuate | fluctuation / fluctuating | vary / oscillate |
| inhabit | inhabitant / inhabitation | reside / live |
| sustain | sustainable / sustainability | maintain / support |

#### 话题 4：技术 / 工业（Technology）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| accurate | accuracy / inaccurately | precise / exact |
| automate | automation / automatic | mechanize / computerize |
| compute | computation / computer | calculate / process |
| device | —— | apparatus / instrument |
| generate | generation / generator | produce / create |
| implement | implementation / implemented | execute / carry out |
| industrial | industry / industrialize | manufacturing / business |
| manufacture | manufacturer / manufactured | produce / make |
| mechanize | mechanism / mechanical | automate / engine |
| technical | technique / technically | technological / specialized |

#### 话题 5：社会 / 心理（Society & Psychology）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| alter | alteration / alterable | change / modify |
| aspect | —— | facet / dimension |
| attribute | attribution / attributable | character / trait |
| compensate | compensation / compensatory | offset / make up |
| concept | conception / conceptual | idea / notion |
| consequent | consequence / consequently | result / outcome |
| constitute | constitution / constituent | comprise / form |
| context | contextual / contextualize | setting / environment |
| individual | individuality / individualize | person / specific |
| interact | interaction / interactive | engage / communicate |

#### 话题 6：健康 / 医学（Health）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| adequate | adequacy / inadequate | sufficient / enough |
| affect | affection / affected | influence / impact |
| chronic | chronically | persistent / ongoing |
| clinical | clinically | medical / hospital |
| competent | competence / competency | capable / skilled |
| contract | contraction / contracted | acquire / develop |
| deprive | deprivation / deprived | deny / strip |
| immune | immunity / immunize | resistant / protected |
| medical | medicine / medicate | healthcare / clinical |
| recover | recovery / recovered | heal / recuperate |

#### 话题 7：商业 / 经济（Business）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| benefit | beneficial / beneficiary | advantage / profit |
| compensate | compensation / compensatory | offset / reimburse |
| consume | consumption / consumer | use / purchase |
| contract | contractual / contractor | agreement / deal |
| decline | declined / declining | decrease / reduce |
| dominate | dominance / dominant | control / prevail |
| economic | economy / economics | financial / fiscal |
| employ | employment / employer | hire / use |
| finance | financial / financing | fund / capital |
| purchase | purchaser / purchasing | buy / acquire |

#### 话题 8：政府 / 法律（Government & Law）

| 词族 | 词性转换 | 同义替换 |
|---|---|---|
| authority | authorize / authoritative | power / official |
| commission | commissioner / commissioned | committee / body |
| compromise | compromising / compromised | settle / negotiate |
| designate | designation / designated | appoint / specify |
| enforce | enforcement / enforced | implement / compel |
| govern | government / governmental | rule / manage |
| illegal | legality / legalize | unlawful / illicit |
| legitimate | legitimacy / legitimize | legal / lawful |
| policy | —— | principle / rule |
| regulate | regulation / regulator | control / supervise |

**覆盖**：AWL 570 词族**覆盖学术文本 10% 词频**（Coxhead 2000 论文原文），是 A 类阅读高频学术词族的主要来源（但不等于"覆盖 80%+ 文章"——此为 skill 之前版本夸大表述，已修正）。**建议**：

- 0 → 6.5：背 AWL 1–3 频段（前 200 词族）
- 6.5 → 7.5：背 AWL 1–5 频段（前 400 词族）
- 7.5 → 8.0+：背 AWL 1–7 频段（全部 570 词族）

---

## 三、6 大类型详解

### 类型 1：词义替换 Lexical Substitution

**最常见的替换类型**。要求**听懂意思不听话面**。

**真题示例**：

> 题目：The museum focuses on ___ history.
> 原文：「We are particularly interested in the **industrial** past of this region.」
> 答案：**industrial**

**训练方法**：

- 背词族时背**完整词族**（如 important → significance / significantly / significant）而非单个词
- 听到近义词时反应「这是 X 的同义」
- P2/P3 训练重点

### 类型 2：词性转换 Grammatical Substitution

**第二常见**。动词 ↔ 名词 / 形容词 / 副词。

**真题示例**：

> 题目：The ___ of the project took several years.
> 原文：「The project **varied** considerably over time.」
> 选项：A. variation ✓（名词） B. variety C. various D. variable
> 答案：**variation**

**训练方法**：

- 背词族时**重点记词性变化**（如 analyse v. → analysis n. → analytical adj.）
- 写笔记时**用名词**，填空时识别**目标词性**

### 类型 3：上下义替换 Hypernymy / Hyponymy

**概括 ↔ 具体**。

**真题示例**：

> 题目：The article mentions various ___ that thrive in the region.
> 原文：「The area is home to numerous species, including **deer, foxes, and rabbits**.」
> 答案：animals 或 mammals（**概括词**）

**反向示例**：

> 题目：Which animal is mentioned in the article?
> 原文：「The area is home to numerous **animals**, including deer, foxes, and rabbits.」
> 答案：deer / foxes / rabbits（**具体词**）

**训练方法**：

- 背词族时**同时记上位词和下位词**（如 animal 是 deer / fox / rabbit 的上位词）
- 题目问「动物」类 → 文中通常给具体动物，答案用 animal 概括

### 类型 4：解释说明替换 Explanation Substitution

**最考验理解能力**。用一句解释替代原词。

**真题示例**：

> 题目：The study was ___.
> 原文：「The research was **halted indefinitely** due to lack of funding.」
> 答案：**halted indefinitely** / **stopped permanently**（解释替换）

**训练方法**：

- 遇到不熟悉的词 → 立即看上下文 → 推断意思
- 用「这意味着什么」问自己
- 重点训练 P3 抽象词（如「sustainability」「implementation」）

### 类型 5：否定 + 反义替换 Negation Substitution

**最易失分**。用反义词 + 否定触发，答案与原文意思相反。

**关键否定触发器清单**（在原文出现立即标记 ⭐）：

| 类别 | 词 |
|---|---|
| **否定前缀** | un-, in-, im-, ir-, il-, dis-, non-, anti-, mis- |
| **否定动词** | fail, lack, miss, deny, refuse, reject, ignore |
| **半否定词** ⭐ | hardly, scarcely, barely, rarely, seldom, few, little, only |
| **否定形容词** | unlikely, impossible, unaware, doubtful |
| **转折词** | but, however, although, though, whereas, while |

**真题示例**：

> 题目：The hotel was ___.
> 原文：「The hotel was **hardly** impressive.」
> 答案：**disappointing** / **unimpressive**（反义）

**训练方法**：

- 听到/看到否定/半否定词 → 在题目旁画「×」提醒
- 答案取反义
- 重点训练 TFNG/YNNG 中的否定题

### 类型 6：句式结构替换 Structural Substitution

**主动 ↔ 被动 / 简单 ↔ 复合 / 倒装**。

**真题示例**：

> 题目：The experiment was conducted by researchers.
> 原文：「Researchers **conducted** the experiment.」
> 答案：**conducted**（主被动替换）

**复杂示例**：

> 题目：The decline in biodiversity is caused by human activity.
> 原文：「Human activity **has led to** a decline in biodiversity.」
> 答案：**has led to**（因果倒转）

**训练方法**：

- 识别**主语和宾语**的位置变化
- 识别**因果断句**和**转承句**
- 重点训练 P3 复杂学术句

---

## 四、否定触发器专项训练

### 否定触发器清单（必背）

| 类别 | 触发器 | 听到立即标记 |
|---|---|---|
| **否定前缀** | un- / in- / im- / ir- / il- / dis- / non- / anti- / mis- | ⭐⭐⭐⭐ |
| **否定动词** | fail / lack / miss / deny / refuse / reject / ignore / negate | ⭐⭐⭐⭐⭐ |
| **半否定词** | hardly / scarcely / barely / rarely / seldom / few / little / only | ⭐⭐⭐⭐⭐ |
| **否定形容词** | unlikely / impossible / unaware / doubtful / reluctant | ⭐⭐⭐⭐ |
| **转折连词** | but / however / although / though / whereas / while / yet | ⭐⭐⭐⭐⭐ |
| **条件否定** | unless / without / instead of / rather than | ⭐⭐⭐ |
| **否定代词** | nothing / nobody / none / neither / nor | ⭐⭐⭐⭐ |

### 实战应用

**应用 1：TFNG 判定**

> 原文：「Hardly any students opted for the course.」
> 题干：Most students opted for the course.
> 判定：原文半否定 → 题干取反义 → **FALSE**

**应用 2：填空题**

> 题目：The hotel was ___.
> 原文：「The hotel was hardly impressive.」
> 答案：**disappointing**（反义）

**应用 3：YNNG 判定**

> 原文：「The author rarely agrees with the new theory.」
> 题干：The author supports the new theory.
> 判定：原文否定 → 题干取反义 → **NO**

---

## 五、训练方法（按学员水平）

### 0 → 6.0 起步（4 周）

- 每天 15 分钟背 AWL 1–3 频段（前 200 词族，**完整词族**）
- 每天 10 分钟做同义替换配对练习（30 题）
- 重点训练「类型 1 词义替换」+「类型 5 否定替换」

### 6.0 → 7.0 强化（4–8 周）

- 每天 15 分钟背 AWL 1–5 频段（前 400 词族）
- 每天 15 分钟做填空 + TFNG 同义替换训练（30 题）
- 加入「类型 2 词性转换」+「类型 6 句式结构」

### 7.0 → 8.0+ 进阶（8–12 周）

- 每天 20 分钟背 AWL 1–7 频段（全 570 词族）
- 每天 20 分钟做「句子完成匹配」+「复杂 Heading」+「学术阅读拓展」
- 加入「类型 3 上下义」+「类型 4 解释说明」

---

## 六、立刻可做的 3 个动作

1. **下载 AWL 词表**（[Victoria University of Wellington AWL](https://www.wgtn.ac.nz/lals/resources/academicwordlist)）→ 每天背 10 个词族（完整词族）
2. **打印否定触发器清单** → 贴在书桌前 → 每次模考时强制检查
3. **拿 IELTS 21 Test 1 P3** → 找出所有「同义替换」对应（题目词 → 原文词）→ 标注 + 分类（6 大类型）→ 练习 3 套

---

## 七、参考来源

- **AWL（Academic Word List）Coxhead 2000**：[Victoria University of Wellington](https://www.wgtn.ac.nz/lals/resources/academicwordlist)
- **Oxford 3000 / 5000**：[Oxford Learners Dictionaries](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford3000-5000)
- **General Service List (West 1953)**：[HK EDB reference](https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Wordlists_preamble.html)
- **Nation BNC/COCA Word Family Lists**：[eapfoundation.com](https://www.eapfoundation.com/vocab/general/bnccoca/)
- **IELTS 官方 Reading 格式**：[ielts.org Academic Reading Format](https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-reading)
