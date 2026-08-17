#!/usr/bin/env python3
"""
IELTS Reading 个性化学习计划生成器（2026 版）

根据目标分数、当前水平、可用天数、每日可用小时数生成冲刺计划。
基于 references/reading-overview.md / reading-strategies.md 中的"4 周 / 8 周 / 12 周"框架 + SOP-F 目标设定现实主义。

Usage:
    python3 study_plan.py --target 7 --days 28 --level 5.5 --hours 1.5
    python3 study_plan.py --target 8 --days 56 --level 6.5 --hours 2
    python3 study_plan.py --target 7 --days 7   --level 6   # OSR 7 天冲刺
    python3 study_plan.py --target 7.5 --days 84 --level 6  # 12 周系统
"""

import argparse
from datetime import datetime, timedelta


PLANS = {
    # 7 天 OSR 冲刺（阅读单科重考）
    "7day": {
        "name": "7 天 OSR 阅读冲刺计划",
        "applicable": "阅读单科重考强化（A 类或 G 类）",
        "day1": {
            "title": "Day 1：定位 + 错题分析",
            "tasks": [
                "1 套完整真题模考（IELTS 21 Test 1/2/3/4 任选 1 套，60 分钟计时）",
                "评分 + 错题分析（按 10 大陷阱分类：对齐 reading-traps.md）",
                "识别最弱 Passage + 最弱题型",
                "下载 BC 官方 IELTS Ready Premium 做 1 次机考模拟（熟悉 Highlight / Notes）",
            ],
        },
        "day2": {
            "title": "Day 2：弱项 Passage 强化",
            "tasks": [
                "P1 隔离练习 5 套（IELTS 20-21 Test 1-4 P1 全部）",
                "词性预判训练（the / a 后接名词；to 后接动词原形）",
                "字数限制训练（NO MORE THAN TWO WORDS = 算冠词）",
                "AWL 词族 1-3 频段复习（约 200 词族）",
            ],
        },
        "day3": {
            "title": "Day 3：TFNG / YNNG 专项",
            "tasks": [
                "P2 TFNG 练习 5 套（IELTS 20-21 Test 1-4 P2 全部）",
                "F vs NG 关键测试：能否找到对立表述？",
                "否定触发器训练（hardly / scarcely / only / few）",
                "YNNG 区分：事实 vs 作者观点",
            ],
        },
        "day4": {
            "title": "Day 4：Heading 专项",
            "tasks": [
                "P3 Heading 练习 5 套（IELTS 20-21 Test 1-4 P3 全部）",
                "四步法：预判段落结构 → 划核心话题词 → 选项匹配 → 反向验证",
                "段落主旨偏差识别（选项匹配过宽 / 过窄）",
                "AWL 词族 4-5 频段复习（约 400 词族）",
            ],
        },
        "day5": {
            "title": "Day 5：复杂匹配 + 填空综合",
            "tasks": [
                "Matching information / features / sentence endings 各 5 套",
                "6 大替换类型训练（词义 / 词性 / 上下义 / 解释 / 否定 / 句式）",
                "填空题字数 + 词性预判 + 同义替换识别",
                "逻辑信号词 10 大类清单复习",
            ],
        },
        "day6": {
            "title": "Day 6：完整真题 + 机考 UI 适应",
            "tasks": [
                "2 套完整真题模考（60 分钟计时；A 类或 G 类按考试类型）",
                "机考 UI 模拟（BC IELTS Ready Premium）",
                "错题回顾 + 10 大陷阱对照",
                "顺序阅读法 vs 平行阅读法实验（按学员特点选）",
            ],
        },
        "day7": {
            "title": "Day 7：考前冲刺 + 心理调适",
            "tasks": [
                "1 次全真模拟（60 分钟，60 分钟计时，按 OSR 考试类型）",
                "AWL 词族最后一次默写",
                "考前 30 秒动作清单演练（P1/P2/P3 各 20 分钟硬上限）",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 4 周冲刺
    "4week": {
        "name": "4 周强化计划",
        "applicable": "基础 5.0-5.5，目标 6.0-6.5",
        "week1": {
            "title": "Week 1：词汇基础 + 顺序阅读法训练",
            "tasks": [
                "1 套完整真题模考（IELTS 21 Test 1，60 分钟）",
                "评分 + 错题分析（按 10 大陷阱分类）",
                "识别最弱 Passage + 题型",
                "AWL 词族 1-3 频段（前 200 词族，每天 10 词族）",
                "顺序阅读法训练：每 Passage 20 分钟，先看题再读文章",
                "下载 BC IELTS Ready Premium 做机考 UI 熟悉",
            ],
        },
        "week2": {
            "title": "Week 2：填空 + TFNG 专项",
            "tasks": [
                "每天 1 个最弱 Passage 隔离练习（20 分钟）",
                "填空题专项（Type 8/9）：词性预判 + 字数限制 + 严格用原词",
                "TFNG 专项（Type 2）：6 大考点（绝对词 / 模糊词 / 比较 / 因果 / 时态 / 数量）",
                "AWL 词族 4-5 频段（每天 10 词族）",
                "周末 1 套完整真题模拟",
            ],
        },
        "week3": {
            "title": "Week 3：Heading + 复杂匹配",
            "tasks": [
                "Heading 专项（P3 主导）：四步法 + 反向验证",
                "Matching information / features / sentence endings 综合",
                "平阅读法实验（仅实验，IDP 官方推顺序阅读法）",
                "周末 2 套完整真题模考（间隔 3 天）",
            ],
        },
        "week4": {
            "title": "Week 4：考前冲刺 + 心理准备",
            "tasks": [
                "1 套全真模拟（60 分钟计时，机考 UI）",
                "错题回顾 + 10 大陷阱对照",
                "考前 30 秒动作清单演练",
                "AWL 词族最后一次默写",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 8 周系统计划
    "8week": {
        "name": "8 周系统计划",
        "applicable": "基础 5.5-6.0，目标 6.5-7.0",
        "week1": {
            "title": "Week 1：基础定位 + 词汇基础",
            "tasks": [
                "1 套完整真题模考（IELTS 21 Test 1）",
                "评分 + 错题分析（按 10 大陷阱分类）",
                "识别最弱 Passage + 题型",
                "AWL 词族 1-3 频段（前 200 词族）",
                "8 大话题核心词全部过一遍（education/research/environment/technology/society/health/business/government）",
            ],
        },
        "week2": {
            "title": "Week 2：词汇 + P1 强化",
            "tasks": [
                "8 大话题核心词精背（每天 1 个话题 20 词）",
                "P1 隔离练习 5 套（IELTS 20-21 Test 1-4 P1）",
                "填空类陷阱（reading-traps.md §1-2）",
                "熟词僻义 20 词（每次 5 词，4 天一轮）",
            ],
        },
        "week3": {
            "title": "Week 3：P2 + TFNG 强化",
            "tasks": [
                "P2 隔离练习 5 套（IELTS 20-21 Test 1-4 P2）",
                "TFNG 专项 50 题",
                "否定触发器训练 + 替换识别",
                "YNNG 区分（事实 vs 观点）",
            ],
        },
        "week4": {
            "title": "Week 4：TFNG + 顺序题综合",
            "tasks": [
                "P2 隔离练习 5 套（加深）",
                "TFNG 6 大考点 + 替换识别 综合",
                "句子完成匹配（Type 7）",
                "周末 1 套完整真题模拟",
            ],
        },
        "week5": {
            "title": "Week 5：P3 + Heading 专项",
            "tasks": [
                "P3 隔离练习 5 套（IELTS 20-21 Test 1-4 P3）",
                "Heading 四步法 + 反向验证",
                "AWL 词族 6-7 频段（高级）",
                "逻辑信号词 10 大类清单复习",
            ],
        },
        "week6": {
            "title": "Week 6：复杂匹配 + 学术拓展",
            "tasks": [
                "Matching information / features 综合",
                "Matching sentence endings 专项",
                "学术阅读拓展（The Economist / Nature / Science 短文，每天 30 分钟）",
                "6 大替换类型清单复习",
            ],
        },
        "week7": {
            "title": "Week 7：机考 UI + 冲刺",
            "tasks": [
                "机考 UI 模拟 2 次（BC IELTS Ready Premium）",
                "2 套完整真题模考（60 分钟计时）",
                "错题回顾 + 弱项 Passage 二次强化",
                "平行阅读法实验（可选）",
            ],
        },
        "week8": {
            "title": "Week 8：考前冲刺",
            "tasks": [
                "1 套全真模拟（A 类或 G 类按考试类型）",
                "错题回顾 + 10 大陷阱对照",
                "考前 30 秒动作清单演练",
                "AWL 词族最后一次默写",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 12 周系统计划
    "12week": {
        "name": "12 周系统计划",
        "applicable": "基础 6.0-6.5，目标 7.0-8.0（需强语言环境输入）",
        "weeks_summary": "12 周详细任务可调用 scripts/study_plan.py --target 7.5 --days 84 --level 6.5 生成完整 8 周 + 4 周冲刺合并版",
    },
}


def generate_plan(target: float, days: int, level: float, hours: float) -> None:
    """根据参数生成学习计划"""

    # 选择计划模板
    if days <= 10:
        template_key = "7day"
    elif days <= 35:
        template_key = "4week"
    elif days <= 70:
        template_key = "8week"
    else:
        template_key = "12week"

    template = PLANS[template_key]

    # 输出
    print(f"\n{'='*70}")
    print(f"雅思阅读学习计划 - {template['name']}")
    print(f"{'='*70}")
    print(f"目标分数：{target}    当前水平：{level}    可用天数：{days}    每日：{hours}h")
    print(f"目标差距：+{target - level:.1f} 分")
    print(f"适用场景：{template['applicable']}")
    print(f"{'='*70}\n")

    # 现实性提示（基于 SOP-F 目标设定现实主义）
    gap = target - level
    if gap >= 2.0:
        print("⚠️ 现实性提示：")
        print(f"   从 {level} 提升到 {target}（+{gap:.1f} 分）通常需要 {int(gap*8)}-{int(gap*12)} 周。")
        print(f"   {days} 天冲刺风险较高，建议拉长至 {int(gap*8)*7}-{int(gap*12)*7} 天。\n")
    elif gap >= 1.0:
        print(f"ℹ️ 提示：从 {level} 到 {target}（+{gap:.1f} 分）通常需要 8-12 周强化。\n")

    # 输出任务清单
    if template_key == "12week":
        print(template["weeks_summary"])
        print("\n详细任务请参考 references/reading-strategies.md 中 12 周路径。\n")
    else:
        start_date = datetime.now().date()
        day_counter = 0

        for key in template:
            if key in ("name", "applicable"):
                continue
            week = template[key]
            day_counter += 1

            print(f"## {week['title']}\n")
            for task in week["tasks"]:
                print(f"- {task}")
            print()

            # 如果是按天的计划，显示日期
            if template_key == "7day":
                task_date = start_date + timedelta(days=day_counter - 1)
                print(f"📅 日期：{task_date.strftime('%Y-%m-%d')} (Day {day_counter}/7)\n")

    # 资源指引
    print("="*70)
    print("📚 配套资源指引")
    print("="*70)
    print("- 真题：IELTS 21 Academic（首选 2026-07）/ IELTS 20（次选 2025-07）/ IELTS 19（2024-06）")
    print("- 机考 UI 模拟：British Council IELTS Ready Premium（报名 BC 考试免费）")
    print("- 学术词族：references/reading-paraphrase.md（AWL 570 词族）")
    print("- 词汇清单：references/reading-vocabulary.md（8 大话题 + 熟词僻义 + 10 类信号词）")
    print("- 题型策略：references/reading-question-types.md（11 大官方题型）")
    print("- 错题陷阱：references/reading-traps.md（10 大陷阱 + 4 步复盘法）")
    print("- 做题策略：references/reading-strategies.md（顺序阅读法 + 平行阅读法）")
    print("- 计分对照：references/reading-band-descriptors.md（A vs G 双表）")
    print("- 2026 政策：references/2026-updates.md（机考 / OSR / IELTS 21）\n")
    print("脚本调用：")
    print("  python3 scripts/paraphrase_quiz.py --topic education")
    print("  python3 scripts/vocab_quiz.py --topic environment --n 15")
    print("  python3 scripts/vocab_quiz.py --false-friend 20")
    print("  python3 scripts/vocab_quiz.py --signal\n")

    # 进度跟踪
    print("="*70)
    print("✅ 进度跟踪模板")
    print("="*70)
    print("每周末自检：")
    print("1. 本周完成率（任务清单完成 / 总数 × 100%）")
    print("2. 最弱 Passage 是否改善（错题数对比上周）")
    print("3. AWL 词族 quiz 正确率（应 > 80%）")
    print("4. 机考 UI 适应度（Highlight / Notes 使用熟练度）")
    print("5. 做题顺序：顺序阅读法 vs 平行阅读法（按学员特点决策）")
    print("6. A vs G 类（如 G 类考生：填空题权重高 + 训练应加重）\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思阅读个性化学习计划生成器（2026 版）")
    parser.add_argument("--target", type=float, required=True, help="目标分数（如 7）")
    parser.add_argument("--days", type=int, required=True, help="可用天数")
    parser.add_argument("--level", type=float, required=True, help="当前水平（如 5.5）")
    parser.add_argument("--hours", type=float, default=1.5, help="每日可用小时数（默认 1.5）")

    args = parser.parse_args()

    # 参数验证
    if not (0 <= args.target <= 9):
        print("目标分数应在 0-9 之间")
        return
    if not (0 <= args.level <= 9):
        print("当前水平应在 0-9 之间")
        return
    if args.days < 1:
        print("可用天数应 ≥ 1")
        return

    generate_plan(args.target, args.days, args.level, args.hours)


if __name__ == "__main__":
    main()
