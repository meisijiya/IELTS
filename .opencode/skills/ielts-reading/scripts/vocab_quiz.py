#!/usr/bin/env python3
"""
IELTS Reading 8 大话题词汇 + 熟词僻义 + 逻辑信号词 学习工具（2026 版）

基于 references/reading-vocabulary.md 中的 8 大话题 + 熟词僻义 + 逻辑信号词。

Usage:
    python3 vocab_quiz.py --list
    python3 vocab_quiz.py --topic education --n 15
    python3 vocab_quiz.py --false-friend 20
    python3 vocab_quiz.py --signal
    python3 vocab_quiz.py --all 20
"""

import argparse
import random
from typing import Dict, List


# 8 大话题核心词族（精简版，约 100 词族，每族 3-5 个词）
TOPIC_VOCAB: dict = {
    "education": [
        "achieve", "accomplish", "attain", "comprehend", "grasp",
        "educate", "instruct", "train", "establish", "found",
        "evaluate", "assess", "appraise", "facilitate", "enable",
        "instruction", "teaching", "training", "perception", "awareness",
        "qualify", "certify", "license", "research", "investigation",
    ],
    "research": [
        "analyse", "examine", "investigate", "data", "statistics",
        "demonstrate", "show", "prove", "hypothesis", "theory",
        "interpret", "explain", "method", "approach", "technique",
        "observe", "monitor", "conclude", "determine", "indicate",
        "suggest", "sample", "subject", "variable", "control group",
    ],
    "environment": [
        "climate", "weather", "conserve", "preserve", "protect",
        "contaminate", "pollute", "degrade", "deteriorate", "ecology",
        "ecosystem", "emit", "release", "fluctuate", "vary",
        "inhabit", "reside", "sustain", "maintain", "diverse",
        "extinct", "endangered", "renewable", "fossil fuel", "carbon",
    ],
    "technology": [
        "accurate", "precise", "automate", "mechanize", "compute",
        "calculate", "device", "apparatus", "generate", "produce",
        "implement", "execute", "industrial", "manufacturing", "mechanism",
        "function", "operate", "innovative", "novel", "integrate",
        "combine", "digital", "automated", "algorithm", "software",
    ],
    "society": [
        "alter", "change", "modify", "aspect", "facet",
        "attribute", "trait", "compensate", "offset", "concept",
        "notion", "consequent", "resulting", "constitute", "comprise",
        "context", "setting", "individual", "person", "interaction",
        "communication", "perceive", "notice", "significant", "considerable",
    ],
    "health": [
        "adequate", "sufficient", "affect", "influence", "chronic",
        "persistent", "clinical", "medical", "competent", "capable",
        "contract", "acquire", "immune", "resistant", "recover",
        "heal", "access", "exposure", "prevent", "treat",
        "symptom", "diagnosis", "patient", "treatment", "therapy",
    ],
    "business": [
        "benefit", "advantage", "consume", "purchase", "contract",
        "agreement", "decline", "decrease", "dominate", "control",
        "economic", "financial", "employ", "hire", "finance",
        "fund", "purchase", "buy", "revenue", "income",
        "compete", "rival", "profit", "gain", "market",
    ],
    "government": [
        "authority", "power", "commission", "committee", "designate",
        "appoint", "enforce", "implement", "govern", "rule",
        "illegal", "unlawful", "legitimate", "legal", "policy",
        "principle", "regulate", "control", "institution", "establishment",
        "legislation", "law", "reform", "revise", "administration",
    ],
}


# 熟词僻义（高频陷阱词，精简版 50 词）
FALSE_FRIENDS: dict = {
    "address": ["n. 地址", "v. 处理 / 对付（address a problem）"],
    "adopt": ["v. 收养", "v. 采纳（adopt a policy）"],
    "allege": ["v. 声称", "adj. 据称的（alleged）"],
    "assume": ["v. 假设", "v. 承担 / 担任（assume a role）"],
    "bar": ["n. 酒吧", "v. 阻止 / n. 障碍（barriers）"],
    "bear": ["n. 熊", "v. 承受 / 携带（bear responsibility）"],
    "claim": ["v. 声称", "v. 要求 / 索赔（claim compensation）"],
    "commit": ["v. 承诺", "v. 犯罪 / 致力于（commit a crime）"],
    "compound": ["n. 化合物", "v. 加重 / adj. 复合（compound interest）"],
    "conceive": ["v. 想象", "v. 构思 / 怀孕（conceive an idea）"],
    "contemplate": ["v. 凝视", "v. 考虑 / 打算（contemplate doing）"],
    "court": ["n. 法院", "n. 球场 / 献殷勤（pay court to）"],
    "credit": ["n. 信用", "n. 荣誉 / 学分（take credit for）"],
    "deliver": ["v. 递送", "v. 演讲 / 接生（deliver a speech）"],
    "develop": ["v. 发展", "v. 患 / 显现（develop a disease）"],
    "dispose": ["v. 处理", "v. 处置 / 丢弃（dispose of waste）"],
    "engage": ["v. 订婚", "v. 从事 / 参与（engage in）"],
    "estimate": ["v. 估计", "v. 估价 / 评估（estimate the cost）"],
    "evident": ["adj. 明显", "adv. 显然（it is evident that）"],
    "exhibit": ["v. 展览", "v. 展现 / 表现（exhibit symptoms）"],
    "figure": ["n. 数字", "n. 人物 / 身材（a public figure）"],
    "fine": ["n. 罚款", "adj. 好的 / 精细（fine detail）"],
    "grant": ["v. 授予", "v. 同意 / 承认（grant a request）"],
    "host": ["n. 主人", "n. 大量 / 主办（a host of issues）"],
    "incidence": ["n. 发生率", "n. 影响 / 发生（incidence of disease）"],
    "intimate": ["v. 亲密", "adj. 暗示 / 详尽（intimate knowledge）"],
    "issue": ["n. 问题", "v. 发行 / n. 子女（issue a statement）"],
    "launch": ["v. 发射", "v. 启动 / 推出（launch a product）"],
    "margin": ["n. 边缘", "n. 利润 / 余地（profit margin）"],
    "matter": ["n. 物质", "v. 重要 / n. 事情（it matters）"],
    "mean": ["v. 刻薄", "v. 意味着 / 平均（mean to do）"],
    "monitor": ["n. 监视器", "v. 监测 / 班长（monitor progress）"],
    "negotiate": ["v. 谈判", "v. 转让 / 越过（negotiate a turn）"],
    "notice": ["n. 注意", "v. 通知 / n. 公示（notice a change）"],
    "panel": ["n. 面板", "n. 小组 / 陪审团（panel discussion）"],
    "perform": ["v. 表演", "v. 执行 / 表现（perform well）"],
    "period": ["n. 时期", "n. 周期 / 句号（period of time）"],
    "post": ["v. 邮寄", "n. 职位 / 柱子（post a job）"],
    "premium": ["n. 溢价", "n. 保险费 / adj. 优质（premium quality）"],
    "project": ["n. 项目", "v. 投射 / 凸出（project onto）"],
    "prompt": ["adj. 迅速", "v. 提示 / 推动（prompt discussion）"],
    "proportion": ["n. 比例", "n. 部分 / 均衡（in proportion to）"],
    "rate": ["n. 速度", "n. 比率 / 评估（rate highly）"],
    "recover": ["v. 恢复", "v. 重新获得 / 康复（recover from）"],
    "register": ["v. 注册", "v. 登记 / 表明（register a complaint）"],
    "regulate": ["v. 调节", "v. 监管 / 校准（regulated by law）"],
    "resort": ["n. 度假地", "v. 诉诸 / 采取（resort to）"],
    "schedule": ["n. 时间表", "v. 安排 / 计划（schedule a meeting）"],
    "suspect": ["v. 怀疑", "n. 嫌疑人"],
    "sustain": ["v. 维持", "v. 承受 / 支撑（sustain damage）"],
    "tap": ["n. 龙头", "v. 开发 / 利用（tap resources）"],
    "transfer": ["v. 转移", "v. 调任 / 转账（transfer money）"],
    "treat": ["v. 请客", "v. 治疗 / 对待（treat a disease）"],
    "undertake": ["v. 承担", "v. 承诺 / 着手（undertake a task）"],
    "vary": ["v. 变化", "v. 不同于 / 改变（vary from）"],
    "yield": ["n. 产量", "v. 屈服 / 产生（yield results）"],
}


# 逻辑信号词（10 大类，精简版）
SIGNAL_WORDS: Dict[str, List[str]] = {
    "转折": ["but", "however", "although", "though", "whereas", "while", "yet", "nevertheless", "nonetheless", "on the contrary", "in contrast"],
    "因果": ["because", "since", "as", "so", "therefore", "thus", "hence", "consequently", "due to", "owing to", "cause", "result in", "lead to", "give rise to", "bring about", "result from", "stem from", "accordingly"],
    "对比": ["similarly", "likewise", "in the same way", "by contrast", "on the other hand", "conversely", "compared with", "unlike", "instead", "rather than", "in comparison"],
    "举例": ["for example", "for instance", "such as", "like", "namely", "including", "particularly", "in particular", "especially", "notably"],
    "总结": ["in conclusion", "in summary", "to summarize", "in short", "in brief", "overall", "altogether", "in all", "to sum up", "on the whole"],
    "递进": ["furthermore", "moreover", "in addition", "besides", "additionally", "what's more", "also", "then", "next", "finally"],
    "时间": ["when", "while", "as", "before", "after", "since", "until", "during", "meanwhile", "subsequently", "previously", "formerly", "later", "eventually", "ultimately", "finally", "immediately"],
    "条件": ["if", "unless", "provided that", "as long as", "in case", "on condition that", "supposing"],
    "强调": ["importantly", "significantly", "indeed", "in fact", "actually", "as a matter of fact", "certainly", "surely", "above all"],
    "否定": ["not", "no", "never", "none", "nothing", "hardly", "scarcely", "rarely", "only", "fail", "lack", "miss", "deny", "refuse", "reject", "ignore", "without", "instead of", "rather than"],
}


def list_topics() -> None:
    """列出所有 8 大话题"""
    print("\n【雅思阅读 8 大话题核心词】\n")
    for i, (topic, words) in enumerate(TOPIC_VOCAB.items(), 1):
        print(f"  {i}. {topic:15s} ({len(words)} 词)")
    print(f"\n共 {sum(len(v) for v in TOPIC_VOCAB.values())} 词\n")
    print("提示：")
    print("  - 完整词族见 references/reading-paraphrase.md（AWL 570 词族）")
    print("  - 完整熟词僻义见 references/reading-vocabulary.md 第三章\n")


def quiz_topic(topic: str, n: int = 15) -> None:
    """某话题的词汇练习"""
    if topic not in TOPIC_VOCAB:
        print(f"\n未知话题：{topic}")
        list_topics()
        return

    words = TOPIC_VOCAB[topic]
    selected = random.sample(words, min(n, len(words)))

    print(f"\n话题【{topic}】词汇测试（{len(selected)} 词）：\n")
    print("─" * 60)
    print("提示：写下英文拼写 + 自己造的同义替换词（AWL 词族）")
    print("─" * 60)
    for i, word in enumerate(selected, 1):
        print(f"  {i:2d}. [__________]    答案：{word}")
    print(f"\n总词数：{len(words)} | 本次抽取：{len(selected)}\n")


def quiz_false_friends(n: int = 20) -> None:
    """熟词僻义测试"""
    items = list(FALSE_FRIENDS.items())
    selected = random.sample(items, min(n, len(items)))

    print(f"\n【熟词僻义测试】（{len(selected)} 词）\n")
    print("找出每个词在雅思阅读中的僻义（非常用释义）\n")
    print("─" * 60)
    for i, (word, meanings) in enumerate(selected, 1):
        print(f"  {i:2d}. {word}")
        print(f"      ├─ 常用义：{meanings[0]}")
        print(f"      └─ 雅思僻义：{meanings[1]}")
    print(f"\n总词数：{len(FALSE_FRIENDS)} | 本次抽取：{len(selected)}\n")
    print("训练法：")
    print("  1. 整理 3-5 个最易错的僻义词")
    print("  2. 用僻义造 3 个句子")
    print("  3. 错的 2 天后重新测试\n")


def show_signal() -> None:
    """显示 10 大类逻辑信号词"""
    print("\n【雅思阅读 10 大类逻辑信号词】\n")
    print("提示：每段至少识别 1 个转折词（but / however / although），不跳读")
    print("─" * 60)
    for category, words in SIGNAL_WORDS.items():
        print(f"\n  【{category}】({len(words)} 词)")
        # 每行打印 5 个
        for j in range(0, len(words), 5):
            print(f"    {', '.join(words[j:j+5])}")
    print()


def quiz_all(n: int = 20) -> None:
    """所有话题混合"""
    all_vocab = []
    for topic, words in TOPIC_VOCAB.items():
        for word in words:
            all_vocab.append(("话题", topic, word))
    selected = random.sample(all_vocab, min(n, len(all_vocab)))

    print(f"\n【混合测试】8 大话题随机共 {len(selected)} 词\n")
    print("─" * 60)
    for i, (kind, topic, word) in enumerate(selected, 1):
        print(f"  {i:2d}. [__________]    答案：{word}    [{topic}]")
    print(f"\n总词数：{len(all_vocab)} | 本次抽取：{len(selected)}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思阅读 8 大话题词汇 + 熟词僻义 + 逻辑信号词 学习工具（2026 版）")
    parser.add_argument("--list", action="store_true", help="列出所有 8 大话题")
    parser.add_argument("--topic", type=str, help="话题名（education/research/environment/technology/society/health/business/government）")
    parser.add_argument("--n", type=int, default=15, help="出题数量（默认 15）")
    parser.add_argument("--false-friend", type=int, help="熟词僻义测试 N 词")
    parser.add_argument("--signal", action="store_true", help="显示 10 大类逻辑信号词")
    parser.add_argument("--all", type=int, help="混合所有话题出 N 题")

    args = parser.parse_args()

    if args.list:
        list_topics()
    elif args.topic:
        quiz_topic(args.topic, args.n)
    elif args.false_friend:
        quiz_false_friends(args.false_friend)
    elif args.signal:
        show_signal()
    elif args.all:
        quiz_all(args.all)
    else:
        list_topics()
        print("用法示例：")
        print("  python3 vocab_quiz.py --topic education --n 15")
        print("  python3 vocab_quiz.py --false-friend 20")
        print("  python3 vocab_quiz.py --signal")
        print("  python3 vocab_quiz.py --all 20")
        print("  python3 vocab_quiz.py --list  (列出所有 8 大话题)")


if __name__ == "__main__":
    main()
