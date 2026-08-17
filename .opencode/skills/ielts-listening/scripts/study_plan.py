#!/usr/bin/env python3
"""
IELTS Listening 个性化学习计划生成器（2026 版）

根据目标分数、当前水平、可用天数、每日可用小时数生成冲刺计划。
基于 references/listening-overview.md 中"4 周 / 8 周"框架。

Usage:
    python3 study_plan.py --target 7 --days 28 --level 5.5 --hours 1.5
    python3 study_plan.py --target 8 --days 56 --level 6.5 --hours 2
    python3 study_plan.py --target 7.5 --days 84 --level 6 --hours 1
    python3 study_plan.py --target 7 --days 7 --level 6   # OSR 7 天冲刺
"""

import argparse
from datetime import datetime, timedelta


PLANS = {
    # 7 天 OSR 冲刺
    "7day": {
        "name": "7 天 OSR 冲刺计划",
        "applicable": "听力单科重考强化",
        "day1": {
            "title": "Day 1：定位 + 错题分析",
            "tasks": [
                "1 套完整真题模考（IELTS 21 任选 1 套）",
                "评分 + 错题分析（每题标错误类型，对照 13 潜规则）",
                "识别最弱 Section（错题最多的）",
                "下载 BC 官方 IELTS Ready Premium 做 1 次机考模拟",
            ],
        },
        "day2": {
            "title": "Day 2：弱项 Section 强化 - S1",
            "tasks": [
                "S1 隔离练习 5 套（IELTS 20-21 S1 全部）",
                "背 20 词必背易错拼写清单（重点 review 错的）",
                "听写测试：9 大场景词（accommodation / travel / medical 等）",
            ],
        },
        "day3": {
            "title": "Day 3：弱项 Section 强化 - S2",
            "tasks": [
                "S2 隔离练习 5 套（重点地图题）",
                "地图方位词背诵 + 流程图策略复习",
                "信号词听辨训练（转折 + 举例 + 否定）",
            ],
        },
        "day4": {
            "title": "Day 4：弱项 Section 强化 - S3",
            "tasks": [
                "S3 隔离练习 5 套（重点多说话人 + 多选题）",
                "同义替换 60 词族 quiz 20 题",
                "否定陷阱训练（hardly / scarcely / only / few）",
            ],
        },
        "day5": {
            "title": "Day 5：弱项 Section 强化 - S4",
            "tasks": [
                "S4 隔离练习 5 套（重点信号词 + 笔记法）",
                "S4 学术话题词（环境/心理/历史/科技 6 大）",
                "学术词根词缀速查（-ology / -tion / -ment / pre- / post-）",
            ],
        },
        "day6": {
            "title": "Day 6：完整真题 + 机考 UI 适应",
            "tasks": [
                "2 套完整真题模考（计时 30 分钟 + 2 分钟 review）",
                "机考 UI 模拟（BC IELTS Ready Premium）",
                "错题回顾 + 13 潜规则对照",
            ],
        },
        "day7": {
            "title": "Day 7：考前冲刺 + 心理调适",
            "tasks": [
                "1 次全真模拟（计时 30 + 2 分钟 review）",
                "20 词拼写清单最后一次默写",
                "考前 30 秒动作清单演练",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 4 周冲刺
    "4week": {
        "name": "4 周冲刺计划",
        "applicable": "已有 5.5-6 基础，目标 6.5-7",
        "week1": {
            "title": "Week 1：定位 + 词汇基础",
            "tasks": [
                "1 套完整真题模考（IELTS 20-21 任选）",
                "评分 + 错题分析（每题标错误类型）",
                "识别最弱 Section（错题最多的）",
                "背 20 词拼写清单（每天 5 词，4 天一轮）",
                "9 大场景词背诵（每天 1 个场景）",
                "下载 BC IELTS Ready Premium 做机考 UI 熟悉",
            ],
        },
        "week2": {
            "title": "Week 2：弱项 Section 强化",
            "tasks": [
                "每天 1 个最弱 Section 隔离练习（30 分钟）",
                "同义替换 60 词族背诵（每天 20 词）",
                "8 类信号词听辨训练",
                "听写测试：每天 10 个场景词",
                "周末 1 套完整真题模拟",
            ],
        },
        "week3": {
            "title": "Week 3：完整真题 + 干扰项训练",
            "tasks": [
                "2 套完整真题模考（间隔 3 天）",
                "干扰项陷阱分析（13 潜规则）",
                "S3 多说话人跟踪训练（重听 + 标记立场）",
                "S4 信号词 + 笔记法训练",
                "机考 UI 模拟 1 次",
            ],
        },
        "week4": {
            "title": "Week 4：考前冲刺 + 心理准备",
            "tasks": [
                "1 套全真模拟（计时 30 + 2 分钟 review）",
                "错题回顾 + 同义替换词族复习",
                "考前 30 秒动作清单演练",
                "拼写清单最后一次默写",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 8 周系统计划
    "8week": {
        "name": "8 周系统计划",
        "applicable": "基础 5.0-5.5，目标 6.5-7",
        "week1": {
            "title": "Week 1：基础定位",
            "tasks": [
                "1 套完整真题模考（IELTS 21 Test 1）",
                "评分 + 错题分析（每题标错误类型）",
                "识别最弱 Section",
                "背 20 词拼写清单（第一轮）",
                "S1 9 大场景词全部过一遍",
            ],
        },
        "week2": {
            "title": "Week 2：词汇 + S1 强化",
            "tasks": [
                "9 大场景词精背（每天 1 个场景，30 词）",
                "S1 隔离练习 5 套",
                "拼写清单第二轮",
                "数字听写 + 字母听写训练",
            ],
        },
        "week3": {
            "title": "Week 3：S2 + 地图题强化",
            "tasks": [
                "S2 隔离练习 5 套（重点地图题）",
                "地图方位词背诵 + 实战",
                "S2 单选题策略训练",
                "拼写清单第三轮",
            ],
        },
        "week4": {
            "title": "Week 4：S3 + 同义替换",
            "tasks": [
                "S3 隔离练习 5 套",
                "同义替换 60 词族第一轮背诵",
                "多说话人跟踪训练",
                "否定陷阱训练",
            ],
        },
        "week5": {
            "title": "Week 5：S4 + 信号词",
            "tasks": [
                "S4 隔离练习 5 套",
                "8 类信号词精讲 + 实战",
                "S4 学术话题词（环境/心理/历史/科技 4 大）",
                "学术词根词缀速查",
            ],
        },
        "week6": {
            "title": "Week 6：完整真题 + 干扰项",
            "tasks": [
                "2 套完整真题模考",
                "13 潜规则完整训练",
                "同义替换 60 词族 quiz 训练",
                "信号词密度统计训练",
            ],
        },
        "week7": {
            "title": "Week 7：机考 UI + 冲刺",
            "tasks": [
                "机考 UI 模拟 2 次（BC IELTS Ready Premium）",
                "2 套完整真题模考（计时 30 + 2 分钟 review）",
                "错题回顾 + 弱项 Section 二次强化",
            ],
        },
        "week8": {
            "title": "Week 8：考前冲刺",
            "tasks": [
                "1 套全真模拟",
                "错题回顾 + 13 潜规则对照",
                "考前 30 秒动作清单演练",
                "拼写清单最后一次默写",
                "调整作息 + 准备考试用品",
            ],
        },
    },

    # 12 周系统计划
    "12week": {
        "name": "12 周系统计划",
        "applicable": "基础 4.5-5，目标 7-7.5（需强语言环境输入）",
        "weeks_summary": "12 周详细任务可调用 scripts/study_plan.py --target 7 --days 84 --level 5 生成完整版",
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
    print(f"雅思听力学习计划 - {template['name']}")
    print(f"{'='*70}")
    print(f"目标分数：{target}    当前水平：{level}    可用天数：{days}    每日：{hours}h")
    print(f"目标差距：+{target - level:.1f} 分")
    print(f"适用场景：{template['applicable']}")
    print(f"{'='*70}\n")

    # 现实性提示
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
        print("\n详细任务请参考 references/listening-resources.md 中 12 周路径。\n")
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
    print("- 真题：IELTS 21 Academic（首选 2026-07）/ IELTS 20（次选 2025-07）/ IELTS 19（2024-06）/ IELTS 18-17（日常练习）")
    print("- 机考 UI 模拟：British Council IELTS Ready Premium（报名 BC 考试免费）")
    print("- 同义替换词族：references/listening-paraphrase.md")
    print("- 干扰项陷阱：references/listening-traps.md")
    print("- 词汇听写：python3 scripts/vocab_quiz.py --scenario accommodation --n 15")
    print("- 同义替换 quiz：python3 scripts/paraphrase_quiz.py --quiz 10\n")

    # 进度跟踪
    print("="*70)
    print("✅ 进度跟踪模板")
    print("="*70)
    print("每周末自检：")
    print("1. 本周完成率（任务清单完成 / 总数 × 100%）")
    print("2. 最弱 Section 是否改善（错题数对比上周）")
    print("3. 拼写清单错词数（应 < 5%）")
    print("4. 同义替换 quiz 正确率（应 > 80%）\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思听力个性化学习计划生成器（2026 版）")
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