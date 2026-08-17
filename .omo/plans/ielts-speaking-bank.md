# ielts-speaking-bank - Work Plan

## TL;DR (For humans)

**What you'll get:**
- 71 个口语话题（Part 1 + Part 2 + Part 3）的全套贴合您真实经历的英文答案，目标分数 6-7 分（默认 6.5）。
- 一个独立的 GitHub Pages 站点模块 `docs/speaking/`，与现有 `docs/writing/` 平级，含首页（话题分类 + 筛选 + 搜索）+ 每个话题的详情页（问题列表 + 答案 + 学习模式）。
- 上线后可通过 GitHub Pages 直接访问，支持手机/电脑。

**Why this approach:**
- 用 JSON 中间数据层把"答案数据"和"页面渲染"分离 → HTML 模板只写一次，71 个话题页由数据生成，避免每页手写 71 次。
- 复用现有 `docs/assets/css/style.css` 的视觉风格 → 与写作模块视觉一致。
- 按"必考 + 高频 + Part2&3 四大类"分波次生成答案 → 每波独立完成、独立可验证、可中途暂停。

**What it will NOT do:**
- 不会生成范文用于考试提交（合规边界 — 仅供学习参考）。
- 不会做 Part 1 的"音频 / 跟读"功能（v1 只做文本 + 折叠答案）。
- 不会做 AI 教练陪练对话（仅是静态答案库）。

**Effort:** Large
**Risk:** Medium - 71 话题 × 多答案，工作量主要在内容生成，HTML 是模板化批量产出。

**Decisions to sanity-check:**
- 目标分数 6.5（您说 6-7，取中间；可微调到 6.0 或 7.0）。
- 答案语言：英文为主，每题后附 1 行中文要点提示。
- 缺失经历（您说"没有"的 6 个人物 + 4 个事件 + 8+ 个观点）由 AI 按您的人设（深圳 / 计算机专业 / 跟 AI 交流 / 喜欢海）合理编造，并标注"AI 补全经历"。

Your next move: 确认此计划 → 启动 worker 执行。

---

> TL;DR (machine): Large effort, Medium risk. Deliverable: 71 话题答案 JSON + 71 HTML 页面 + 首页 + GitHub Pages 自动部署。

## Scope

### Must have
1. 补全用户在问卷中标记"没有"的 6 个 Part 2 人物（老师 / 种植物 / 自学者 / 名人 / 帮人者 / 自然保护者）+ 4 个事件（重大决定 / 给建议 / 不好音乐活动 / 超预算购物）+ Part 3 缺失观点
2. 生成 71 个话题的全套答案：
   - Part 1 必考 5 个话题 × ~12 问题 = ~60 答案
   - Part 1 高频 27 个话题 × ~6 问题 = ~162 答案
   - Part 2 & 3 39 个话题 × (1 cue card 答案 + 3-6 Part 3 问题) = ~234 答案
3. JSON 数据文件 `docs/speaking/data/answers.json` 集中存放全部答案
4. HTML 模板（1 套）：
   - 首页 `docs/speaking/index.html`：话题列表 + 按 Part / Category / new+old 筛选 + 搜索框
   - 话题详情页模板：折叠式 Q-A 列表 + Part 2 cue card + 长答案 + Part 3 讨论
5. 71 个话题详情页 `docs/speaking/topics/*.html`（由数据 + 模板批量生成）
6. 学习模式交互（纯 JS）：点击问题 → 折叠/展开答案；"隐藏全部答案"按钮用于先看问题自测
7. 复用 `docs/assets/css/style.css`，新增少量口语模块专属样式
8. 部署：复用现有 `.github/workflows/deploy.yml`，无需修改 workflow

### Must NOT have (guardrails, anti-slop, scope boundaries)
- ❌ 不要为考试代写并伪装成考生作品 — 所有答案明确标注"AI 范例，仅供学习"
- ❌ 不要添加音频 / 录音功能 — v1 只做文本
- ❌ 不要把写作模块的范文也搬过来 — 只做口语
- ❌ 不要硬编码 71 个 HTML 文件 — 必须由 JSON + 模板批量生成
- ❌ 不要做 AI 陪练对话 — 静态答案库即可
- ❌ 不要添加 SSR / 后端 — 纯静态 HTML + JSON

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- **Test decision:** TDD-light - 每个 Wave 后做一次结构验证 + 内容检查
- **Evidence:** `.omo/evidence/ulw/ses_<session>/ielts-speaking-bank/a<N>/`
- **自动化验证**：
  - 答案完整性：每个话题的 JSON 包含的 Q-A 数量 = PDF 中的题目数
  - HTML 完整性：71 个话题页全部生成，无 404
  - 链接完整性：从首页可点击进入所有话题页
  - 语言分数自检：抽样 5 个话题，对照 6.5 分 band descriptors 检查 LR / FC / GRA 特征
- **本地预览**：用 `python -m http.server` 在 docs/ 目录起静态服务，访问首页和至少 5 个话题页验证

## Execution strategy

### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.

| Wave | 主题 | 并行 todo 数 |
|---|---|---|
| Wave 1 | 经历补全 + JSON 数据结构设计 | 2 |
| Wave 2 | Part 1 必考 5 话题答案生成 | 5 |
| Wave 3 | Part 1 高频 27 话题答案生成（分 5 批） | 5 |
| Wave 4 | Part 2 & 3 PLACE 6 话题答案生成 | 6 |
| Wave 5 | Part 2 & 3 PEOPLE 11 话题答案生成 | 11 |
| Wave 6 | Part 2 & 3 OBJECTS 10 话题答案生成 | 10 |
| Wave 7 | Part 2 & 3 EVENTS 12 话题答案生成 | 12 |
| Wave 8 | HTML 模板 + 首页 + 批量生成 71 话题页 | 5 |
| Wave 9 | 学习功能 JS + 样式调整 | 2 |
| Wave 10 | 部署验证 | 3 |

总 todo 数：~70 个，分 10 个波次执行。

### Dependency matrix

| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 补全缺失经历 | (none) | Wave 2-7 全部 | 设计 JSON 数据结构 |
| 设计 JSON 数据结构 | (none) | Wave 2-7 全部 | 补全缺失经历 |
| Part 1 必考 5 答案 | 经历补全 + JSON 结构 | Wave 8 | 无（每个话题内串行，但 5 话题可并行） |
| Part 1 高频 27 答案 | 经历补全 + JSON 结构 | Wave 8 | 必考波次（不同子代理） |
| Part 2&3 PLACE 6 | 经历补全 + JSON 结构 | Wave 8 | Part 2&3 其他大类 |
| Part 2&3 PEOPLE 11 | 经历补全 + JSON 结构 | Wave 8 | Part 2&3 其他大类 |
| Part 2&3 OBJECTS 10 | 经历补全 + JSON 结构 | Wave 8 | Part 2&3 其他大类 |
| Part 2&3 EVENTS 12 | 经历补全 + JSON 结构 | Wave 8 | Part 2&3 其他大类 |
| HTML 模板 | JSON 数据结构 | 批量生成 | 与答案生成并行（按模板雏形先做） |
| 批量生成 71 页 | HTML 模板 + 全部答案 JSON | 部署 | 无 |
| 学习功能 JS | 71 页生成完成 | 部署 | 样式调整 |
| 部署验证 | 全部完成 | (none) | 无 |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->

### Wave 1 - 基础准备

- [x] 1. 补全用户缺失经历到 `.omo/drafts/ielts-speaking-supplemented.md`
  What to do / Must NOT do:
  - 读取 `.omo/drafts/experience-questionnaire.md` 中所有"没有"项
  - 为 6 个 Part 2 人物（F2 老师、F4 种植物、F7 画画小孩、F8 自学者、F9 名人、F10 帮人者、F11 聪明者、F12 自然保护者）各编造合理人物（贴合深圳大学生背景）
  - 为 4 个事件（G1 重大决定、G9 给建议、G10 不好音乐、G16 超预算）编造合理事件
  - 为 8+ 个 Part 3 "不知道"项补充合理观点（按用户已有立场延伸）
  - 输出 markdown，结构与原问卷一致，每个补全项标 `[AI补全]` 标签
  - 不要修改原问卷，只追加补充
  Parallelization: Wave 1 | Blocked by: (none) | Blocks: Wave 2-7 全部
  References: `.omo/drafts/experience-questionnaire.md:1-466`、`.opencode/skills/ielts-speaking/SKILL.md:114-200`（SOP-B 经历确认步骤）
  Acceptance criteria: 文件存在、覆盖所有"没有"项、每项有 `[AI补全]` 标签、内容与用户人设一致
  QA scenarios:
  - happy: 文件生成 → 检查 `wc -l` ≥ 50 行
  - failure: 用户画像矛盾检查 → 人工 spot-check 5 个补全项
  Evidence `.omo/evidence/ulw/<session>/task-1-ielts-speaking-supplemented.md`
  Commit: N

- [x] 2. 设计 JSON 数据结构 + 创建数据文件骨架
  What to do / Must NOT do:
  - 在 `.omo/drafts/` 创建 `answers-schema.md` 描述 JSON 结构
  - 创建 `docs/speaking/data/answers.json` 空骨架，包含 topics 数组与每个 topic 的 slots（part1 / part2 / part3）
  - 每个 slot 含问题文本（来自 PDF）、答案（待填）、分类标签
  - 不要现在就填答案，只搭框架
  Parallelization: Wave 1 | Blocked by: (none) | Blocks: Wave 2-7 全部 + Wave 8
  References: `.opencode/skills/ielts-speaking/SKILL.md:114-200`、`docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54`（参考 HTML 结构）
  Acceptance criteria: JSON 文件 schema 完整、可用 `python -m json.tool` 验证合法、所有 71 个 topic 占位 slot 已建好
  QA scenarios:
  - happy: JSON 解析通过 → `python -m json.tool docs/speaking/data/answers.json`
  - failure: topic 数量检查 → 解析后断言 `len(topics) == 71`
  Evidence `.omo/evidence/ulw/<session>/task-2-answers-schema.md`
  Commit: Y | chore(speaking): add answers data skeleton

### Wave 2 - Part 1 必考 5 话题答案生成

- [x] 3. Part 1 Hometown 答案生成（深圳 / 一线城市 / 适合年轻人）
  What to do / Must NOT do: 按 6.5 分语言特征生成 12 个 Q-A 答案；不要照抄 PDF 题目，要 paraphrase；不要超过 30 秒/题；必须用用户实际经历（深圳、年轻人多、湿热天气等）
  Parallelization: Wave 2 | Blocked by: todo 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:14-21`、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance criteria: 12 个 Q-A 全部填入 JSON 对应 slot、每答 25-40 词、用 SEER 公式
  QA scenarios: happy → JSON 解析通过、assert topic "hometown" 的 part1 数组有 12 项
  Evidence `.omo/evidence/ulw/<session>/task-3-hometown.md`
  Commit: N

- [x] 4. Part 1 Work or Studies 答案生成（计算机专业学生 / 喜欢玩计算机 / 女朋友帮忙）
  Parallelization: Wave 2 | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:23-28`、ielts-speaking band-descriptors 6.5 段
  Acceptance: 10 个 Q-A（含 Work 和 Study 两支）
  QA: JSON 解析通过、计数对
  Evidence `.omo/evidence/ulw/<session>/task-4-work.md`
  Commit: N

- [x] 5. Part 1 Home/Accommodation 答案生成（三室一厅 / 跟爸妈爷爷弟妹住 / 上下床）
  Parallelization: Wave 2 | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:30-34`
  Acceptance: 12 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-5-home.md`
  Commit: N

- [x] 6. Part 1 The area you live in 答案生成（新安街道 / 前海 / 看海）
  Parallelization: Wave 2 | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:36-39`
  Acceptance: 7 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-6-area.md`
  Commit: N

- [x] 7. Part 1 The city you live in 答案生成（深圳 / 永久地 / 湿热 / 繁华）
  Parallelization: Wave 2 | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:41-45`
  Acceptance: 11 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-7-city.md`
  Commit: N

### Wave 3 - Part 1 高频话题答案生成（29 个，分 5 批）

- [x] 8. Part 1 高频 PLACE 批（Parks / Outer space / Building）
  Parallelization: Wave 3 batch A | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:169-183`
  Acceptance: 3 话题 × ~4 Q-A = 12 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-8-place-p1.md`
  Commit: N

- [x] 9. Part 1 高频 OBJECT 批 1（Science / Cars / Teachers / Social media）
  Parallelization: Wave 3 batch B | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:148-158`
  Acceptance: 4 话题 × ~6 Q-A = ~24 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-9-object1.md`
  Commit: N

- [x] 10. Part 1 高频 OBJECT 批 2（Watch / Websites / Mirrors / Gifts）
  Parallelization: Wave 3 batch C | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:117-144`
  Acceptance: 4 话题 × ~5 Q-A = ~20 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-10-object2.md`
  Commit: N

- [x] 11. Part 1 高频 OBJECT 批 3（Pets / Food / Sports team / Scenery / Views / Childhood）
  Parallelization: Wave 3 batch D | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:55-72, 145-166`
  Acceptance: 6 话题 × ~5 Q-A = ~30 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-11-object3.md`
  Commit: N

- [x] 12. Part 1 高频 EVENT + ABSTRACT 批（Shopping / Singing / Life stages / Morning / Reading / Walking / Typing / Tidiness / Music / Hobby）
  Parallelization: Wave 3 batch E | Blocked by: 1, 2 | Blocks: Wave 8
  References: `.omo/drafts/experience-questionnaire.md:79-111`
  Acceptance: 10 话题 × ~5 Q-A = ~50 个 Q-A
  Evidence `.omo/evidence/ulw/<session>/task-12-event-abs.md`
  Commit: N

### Wave 4 - Part 2 & 3 PLACE 6 话题（每个 = 1 cue card + Part 3 答案）

- [x] 13. Describe your favorite city (深圳 / 繁华)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.16、`.omo/drafts/experience-questionnaire.md:185`
  Acceptance: cue card 4 个 bullet 全覆盖 + 150-200 词答案 + 5 个 Part 3 答案
  Evidence `.omo/evidence/ulw/<session>/task-13-fav-city.md`
  Commit: N

- [x] 14. Describe a boring place (AI 补全：等公交车 / 排队时)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.17、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-14-boring.md`
  Commit: N

- [x] 15. Describe a tall building (平安金融中心 / 不喜欢 / 怕高)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.17、`.omo/drafts/experience-questionnaire.md:189`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-15-tall.md`
  Commit: N

- [x] 16. Describe an interesting building (深圳湾体育中心 / 春茧)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.18
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-16-interest-bldg.md`
  Commit: N

- [x] 17. Describe a famous city (深圳 / 繁华)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.18、`.omo/drafts/experience-questionnaire.md:189`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-17-famous-city.md`
  Commit: N

- [x] 18. Describe a city enjoyed visiting (广西南宁 / 和女朋友)
  Parallelization: Wave 4 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.19、`.omo/drafts/experience-questionnaire.md:188`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-18-nanning.md`
  Commit: N

### Wave 5 - Part 2 & 3 PEOPLE 11 话题

- [x] 19. Describe a friend from childhood (zeng / 小学同学 / 没联系)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.21、`.omo/drafts/experience-questionnaire.md:198-200`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-19-child-friend.md`
  Commit: N

- [x] 20. Describe a person with successful business (姨丈)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.21、`.omo/drafts/experience-questionnaire.md:207`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-20-business.md`
  Commit: N

- [x] 21. Describe a person who grows plants (AI 补全：邻居阿姨)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.22、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-21-plants.md`
  Commit: N

- [x] 22. Describe a person wanting medical career (妹妹 / 做护士)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.22、`.omo/drafts/experience-questionnaire.md:213`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-22-medical.md`
  Commit: N

- [x] 23. Describe a person good at planning (女朋友 / 学习计划 / 拿奖学金)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.23、`.omo/drafts/experience-questionnaire.md:216`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-23-planning.md`
  Commit: N

- [x] 24. Describe a child who loves drawing (AI 补全：表妹的小孩)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.23、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-24-child-art.md`
  Commit: N

- [x] 25. Describe a friend who self-learned (AI 补全：朋友学剪辑)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.24、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-25-self-learn.md`
  Commit: N

- [x] 26. Describe a famous person to meet (AI 补全：马斯克 / 钢铁侠原型)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.24、`.omo/drafts/ielts-speaking-supplemented.md`、`.omo/drafts/experience-questionnaire.md:177`（钢铁侠关联）
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-26-famous.md`
  Commit: N

- [x] 27. Describe a person who helps others (AI 补全：爷爷)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.25、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-27-helper.md`
  Commit: N

- [x] 28. Describe a smart problem solver (AI 补全：表姐)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.25、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-28-smart.md`
  Commit: N

- [x] 29. Describe a person who protects nature (AI 补全：环保志愿者同学)
  Parallelization: Wave 5 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.26、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-29-nature.md`
  Commit: N

### Wave 6 - Part 2 & 3 OBJECTS 10 话题

- [x] 30. Describe a new law (保障双休落地)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.28、`.omo/drafts/experience-questionnaire.md:293`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-30-law.md`
  Commit: N

- [x] 31. Describe a plan that changed (难受 / 安排被打乱)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.28、`.omo/drafts/experience-questionnaire.md:281`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-31-changed-plan.md`
  Commit: N

- [x] 32. Describe an interesting video (会笑、收藏 / B 站)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.29、`.omo/drafts/experience-questionnaire.md:284`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-32-video.md`
  Commit: N

- [x] 33. Describe a movie (蜘蛛侠 / 跟女朋友 / 布吉)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.29、`.omo/drafts/experience-questionnaire.md:287`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-33-movie.md`
  Commit: N

- [x] 34. Describe a piece of technology (3D 打印机)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.30、`.omo/drafts/experience-questionnaire.md:302`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-34-tech.md`
  Commit: N

- [x] 35. Describe a family heirloom (老照片 / 承载儿时回忆)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.30、`.omo/drafts/experience-questionnaire.md:305`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-35-heirloom.md`
  Commit: N

- [x] 36. Describe a perfect job (图书管理员 / 轻松)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.31、`.omo/drafts/experience-questionnaire.md:296`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-36-perfect-job.md`
  Commit: N

- [x] 37. Describe a short-term foreign job (教中文)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.31、`.omo/drafts/experience-questionnaire.md:299`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-37-foreign-job.md`
  Commit: N

- [x] 38. Describe a program or app (微信)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.32、`.omo/drafts/experience-questionnaire.md:308`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-38-app.md`
  Commit: N

- [x] 39. Describe an overspent item (AI 补全：买手机)
  Parallelization: Wave 6 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.32、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-39-overspent.md`
  Commit: N

### Wave 7 - Part 2 & 3 EVENTS 12 话题

- [x] 40. Describe an important decision (AI 补全：选计算机专业)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.35、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-40-decision.md`
  Commit: N

- [x] 41. Describe a time you got up early (太阳没起来就醒)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.35、`.omo/drafts/experience-questionnaire.md:246`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-41-early.md`
  Commit: N

- [x] 42. Describe working in a group (小组作业 / 电影社团 / 队友迟到)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.36、`.omo/drafts/experience-questionnaire.md:249-250`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-42-group.md`
  Commit: N

- [x] 43. Describe a live sports event (电竞 / 在家)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.36、`.omo/drafts/experience-questionnaire.md:253`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-43-sports.md`
  Commit: N

- [x] 44. Describe being proud of family member (弟弟考试分数高)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.37、`.omo/drafts/experience-questionnaire.md:256-257`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-44-proud.md`
  Commit: N

- [x] 45. Describe using imagination (无聊时脑里异想天开)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.37、`.omo/drafts/experience-questionnaire.md:260`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-45-imagination.md`
  Commit: N

- [x] 46. Describe an occasion many smiling (学校运动会晚上表演)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.38、`.omo/drafts/experience-questionnaire.md:263`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-46-smiling.md`
  Commit: N

- [x] 47. Describe no mobile phone occasion (高中学校)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.38、`.omo/drafts/experience-questionnaire.md:266`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-47-no-phone.md`
  Commit: N

- [x] 48. Describe giving advice (AI 补全：建议弟弟选专业)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.39、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-48-advice.md`
  Commit: N

- [x] 49. Describe a bad music event (AI 补全：公司年会)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.39、`.omo/drafts/ielts-speaking-supplemented.md`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-49-bad-music.md`
  Commit: N

- [x] 50. Describe encouraging someone (鼓励考研 / 对方听听而已)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.40、`.omo/drafts/experience-questionnaire.md:275`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-50-encourage.md`
  Commit: N

- [x] 51. Describe a vehicle trip (和女朋友 / 没体验过)
  Parallelization: Wave 7 | Blocked by: 1, 2 | Blocks: Wave 8
  References: PDF p.40、`.omo/drafts/experience-questionnaire.md:278`
  Acceptance: cue card + 答案 + Part 3
  Evidence `.omo/evidence/ulw/<session>/task-51-vehicle.md`
  Commit: N

### Wave 8 - HTML 模板 + 首页 + 批量生成 71 话题页

- [x] 52. 创建 HTML 话题页模板（template.html）
  What to do / Must NOT do:
  - 写一份完整的 `docs/speaking/template.html`，含占位符（{{topic_id}}、{{topic_name}}、{{part1_qa}}、{{part2_cue_card}}、{{part2_answer}}、{{part3_qa}}）
  - 复用 `docs/assets/css/style.css`
  - 加折叠答案的 JS（每个 Q-A 是 `<details>` 或点击 toggle）
  - 不要在模板里硬编码任何具体答案
  Parallelization: Wave 8 | Blocked by: 2（数据结构）| Blocks: 53
  References: `docs/writing/task2/01-agree-disagree-history-vs-business.html:1-54`、`docs/assets/css/style.css:1-182`
  Acceptance: HTML 文件存在、占位符格式清晰、用浏览器打开渲染正常
  QA scenarios: happy → 打开 template.html 显示骨架；failure → 占位符缺失检测
  Evidence `.omo/evidence/ulw/<session>/task-52-template.html`
  Commit: Y | feat(speaking): add topic page template

- [x] 53. 创建首页 docs/speaking/index.html
  What to do / Must NOT do:
  - 含话题列表（按 Part 分类：Part 1 必考 / Part 1 高频 / Part 2&3 PLACE / PEOPLE / OBJECTS / EVENTS）
  - 筛选器：按 Part 筛选、按 new/old 筛选、按 category 筛选
  - 搜索框（按话题名搜索）
  - 链接到 71 个话题详情页
  - 不要在首页展示答案，只列话题
  Parallelization: Wave 8 | Blocked by: 52 | Blocks: 54
  References: `docs/writing/index.html:1-100`
  Acceptance: 首页存在、含 71 个话题卡片、筛选按钮可点击、链接全部可达
  QA scenarios: happy → 打开首页显示全部话题；failure → 检查链接 404 数 = 0
  Evidence `.omo/evidence/ulw/<session>/task-53-index.html`
  Commit: Y | feat(speaking): add index page with filters

- [x] 54. 写批量生成脚本 generate_pages.py
  What to do / Must NOT do:
  - 读取 `docs/speaking/data/answers.json`
  - 用 Jinja2 或纯字符串替换渲染 `template.html` 为 71 个 HTML 文件
  - 输出到 `docs/speaking/topics/<topic-slug>.html`
  - 记录生成日志到 `.omo/evidence/generation.log`
  - 不要修改原 JSON 或 template
  Parallelization: Wave 8 | Blocked by: 52 | Blocks: 55
  References: 上述两个文件
  Acceptance: 脚本可执行、生成 71 个 HTML、每个 HTML 含对应话题的 Q-A 数据
  QA scenarios: happy → `python generate_pages.py` 成功；failure → 数量检查 `ls docs/speaking/topics/*.html | wc -l == 71`
  Evidence `.omo/evidence/ulw/<session>/task-54-generator.py`
  Commit: Y | feat(speaking): add batch HTML generator

- [x] 55. 运行生成脚本，产出 71 个话题页
  What to do / Must NOT do: 执行 `python generate_pages.py`、验证输出文件齐全；不要手动调整生成的 HTML（除非发现 bug）
  Parallelization: Wave 8 | Blocked by: 53, 54, Wave 2-7 全部 | Blocks: 56
  References: todo 54
  Acceptance: 71 个 HTML 文件存在、首页链接全部可达
  QA scenarios: happy → 文件计数 == 71、首页点击 5 个抽样话题无 404
  Evidence `.omo/evidence/ulw/<session>/task-55-generated-pages.md`
  Commit: Y | feat(speaking): generate 71 topic pages

- [x] 56. 验证 JSON 答案数据完整性
  What to do / Must NOT do: 写脚本检查 answers.json 每个 topic 的 Q-A 数量 = PDF 题目数；不要修改答案
  Parallelization: Wave 8 | Blocked by: Wave 2-7 全部 | Blocks: F1
  References: todo 2 schema
  Acceptance: 全部 71 topic 通过数量验证、JSON 合法
  QA scenarios: happy → `python verify_completeness.py` 退出码 0；failure → 列出缺失 topic
  Evidence `.omo/evidence/ulw/<session>/task-56-verified.md`
  Commit: N

### Wave 9 - 学习功能 JS + 样式调整

- [x] 57. 添加学习模式交互（隐藏答案 / 全部显示）
  What to do / Must NOT do:
  - 在所有 HTML 页面加 JS：默认折叠所有答案；点击 "显示答案" 按钮展开；点击 "背诵模式" 隐藏答案后只显示问题
  - 加按钮到话题页顶部
  - 不要修改答案内容
  Parallelization: Wave 9 | Blocked by: 55 | Blocks: F1
  References: 当前 topic page 模板
  Acceptance: 点击按钮可切换显示/隐藏
  QA scenarios: happy → 浏览器测试；failure → JS 控制台无错误
  Evidence `.omo/evidence/ulw/<session>/task-57-learning-mode.md`
  Commit: Y | feat(speaking): add learning mode toggle

- [x] 58. 视觉一致性检查 + 微调样式
  What to do / Must NOT do: 与 docs/writing 视觉风格统一；检查移动端响应；不加新颜色/字体
  Parallelization: Wave 9 | Blocked by: 55 | Blocks: F1
  References: `docs/assets/css/style.css:1-182`
  Acceptance: 桌面和移动端渲染正常、与写作模块视觉一致
  QA scenarios: happy → Playwright 截图对比；failure → 修复 CSS
  Evidence `.omo/evidence/ulw/<session>/task-58-style.md`
  Commit: N

### Wave 10 - 部署验证

- [x] 59. 本地静态服务器测试
  What to do / Must NOT do: 用 `python -m http.server` 起 docs/ 目录；访问首页 + 5 个抽样话题；不要修改服务器配置
  Parallelization: Wave 10 | Blocked by: 55 | Blocks: 60
  References: 整个 docs/speaking/ 目录
  Acceptance: 全部页面 200、无 JS 错误
  QA scenarios: happy → curl 抽样 5 页返回 200；failure → curl 找 404/500
  Evidence `.omo/evidence/ulw/<session>/task-59-local-test.md`
  Commit: N

- [x] 60. 写 deploy verification log
  What to do / Must NOT do: 记录 `.github/workflows/deploy.yml` 会自动捡起 docs/speaking/、验证 workflow 文件存在；不要修改 workflow
  Parallelization: Wave 10 | Blocked by: 59 | Blocks: 61
  References: `.github/workflows/deploy.yml:1-39`
  Acceptance: 部署 log 记录完整
  Evidence `.omo/evidence/ulw/<session>/task-60-deploy-log.md`
  Commit: N

- [x] 61. 提交所有文档文件并 push 到 main
  What to do / Must NOT do: git add + commit + push；commit message 格式遵循已有风格；不要 force push
  Parallelization: Wave 10 | Blocked by: 60 | Blocks: F1
  References: 现有 git log
  Acceptance: 提交成功、GitHub Actions 触发
  QA scenarios: happy → push 成功；failure → 解决冲突
  Evidence `.omo/evidence/ulw/<session>/task-61-pushed.md`
  Commit: Y | feat(speaking): deploy ielts speaking module

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [x] F1. Plan compliance audit - 71 个话题答案全部生成、JSON 结构完整、HTML 渲染正常
- [x] F2. Code quality review - 答案语言特征自检（抽样 5 个话题对照 6.5 分 band descriptors）、HTML 无样式错误
- [x] F3. Real manual QA - Playwright 打开首页 + 5 个话题页 + 学习模式交互测试
- [x] F4. Scope fidelity - Must NOT have 项未越界：无音频、无陪练、无 SSR、无硬编码 HTML

## Commit strategy

- Wave 1 / 2 / 3 / 4 / 5 / 6 / 7：只更新数据文件和 drafts，不提交（数据有缺失时回滚成本低）
- Wave 8：每个 HTML 模板 / 生成脚本 / 数据完整性验证后单次提交
- Wave 9：每个 JS / 样式调整后单次提交
- Wave 10：推送触发 GitHub Pages 部署后单次提交
- 总 commit 数：~6-8 个，每个原子

## Success criteria

1. ✅ 71 个口语话题的答案全部生成，存于 `docs/speaking/data/answers.json`
2. ✅ `docs/speaking/index.html` 含完整话题列表 + 筛选 + 搜索
3. ✅ `docs/speaking/topics/*.html` 共 71 个文件
4. ✅ 学习模式可切换（默认隐藏答案 → 点击展开）
5. ✅ 抽样 5 个话题的答案对照 6.5 分 band descriptors 通过（FC / LR / GRA 特征符合）
6. ✅ GitHub Actions 部署成功，页面可在 GitHub Pages 上访问
7. ✅ 与 docs/writing 视觉风格一致（同样字体、同样面包屑、同样绿色主题）
8. ✅ 移动端可读、无横向滚动条
9. ✅ 所有补全的经历标注 `[AI补全]`，与用户真实经历区分

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 答案生成量极大（~470 答案） | 分 10 波次执行，每波独立可暂停 |
| 用户人设可能前后矛盾 | Wave 1 经历补全后抽样 spot-check |
| HTML 生成脚本可能格式错误 | 生成后用浏览器测试 + Playwright 截图 |
| GitHub Pages 部署失败 | 复用现有 workflow + 部署前本地验证 |
| 用户填写问卷时表达简短，部分经历需要大量补全 | 已在 Wave 1 标注 `[AI补全]`，所有补全内容贴合用户人设 |