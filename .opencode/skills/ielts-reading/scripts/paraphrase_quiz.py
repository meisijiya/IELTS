#!/usr/bin/env python3
"""
IELTS Reading 同义替换词族速查与练习工具（2026 版）

基于 references/reading-paraphrase.md 中的 6 大类型 + AWL 570 词族（Coxhead 2000）+ 8 大话题分组。
**初稿「近 500 组同义替换高频词」无官方依据，已删除**。本工具仅基于 AWL 词族。

Usage:
    python3 paraphrase_quiz.py --word important
    python3 paraphrase_quiz.py --topic education
    python3 paraphrase_quiz.py --random 5
    python3 paraphrase_quiz.py --quiz 10
    python3 paraphrase_quiz.py --negation
    python3 paraphrase_quiz.py --all
"""

import argparse
import random
import sys
from typing import Dict, List


# AWL 570 词族（Coxhead 2000）按 8 大话题分组（精简版，每组取 8-12 个核心词族）
# 完整词表：https://www.wgtn.ac.nz/lals/resources/academicwordlist
AWL_FAMILIES: Dict[str, Dict[str, List[str]]] = {
    "education": {
        "achieve": ["accomplish", "attain", "reach"],
        "acquire": ["obtain", "gain", "secure"],
        "comprehend": ["understand", "grasp", "fathom"],
        "educate": ["teach", "instruct", "train"],
        "establish": ["found", "create", "set up"],
        "evaluate": ["assess", "appraise", "judge"],
        "facilitate": ["enable", "assist", "ease"],
        "instruction": ["teaching", "training", "direction"],
        "perception": ["awareness", "understanding", "view"],
        "qualify": ["certify", "license", "entitle"],
        "research": ["study", "investigation", "inquiry"],
        "theory": ["hypothesis", "concept", "notion"],
    },
    "research": {
        "analyse": ["examine", "study", "break down"],
        "data": ["information", "statistics", "findings"],
        "demonstrate": ["show", "prove", "indicate"],
        "examine": ["inspect", "investigate", "analyse"],
        "experiment": ["trial", "test", "investigation"],
        "hypothesis": ["theory", "assumption", "proposition"],
        "interpret": ["explain", "clarify", "understand"],
        "investigate": ["explore", "study", "examine"],
        "method": ["approach", "technique", "procedure"],
        "observe": ["watch", "monitor", "notice"],
        "conclude": ["determine", "decide", "deduce"],
        "indicate": ["suggest", "show", "point to"],
    },
    "environment": {
        "climate": ["weather", "atmospheric conditions"],
        "conserve": ["preserve", "protect", "safeguard"],
        "contaminate": ["pollute", "taint", "poison"],
        "degrade": ["deteriorate", "erode", "worsen"],
        "ecology": ["environment", "ecosystem"],
        "emit": ["release", "discharge", "give off"],
        "environment": ["surroundings", "habitat", "setting"],
        "fluctuate": ["vary", "oscillate", "shift"],
        "inhabit": ["reside", "live in", "populate"],
        "sustain": ["maintain", "support", "preserve"],
        "diverse": ["varied", "different", "multiple"],
        "extinct": ["gone", "disappeared", "vanished"],
    },
    "technology": {
        "accurate": ["precise", "exact", "correct"],
        "automate": ["mechanize", "computerize", "robotize"],
        "compute": ["calculate", "process", "reckon"],
        "device": ["apparatus", "instrument", "tool"],
        "generate": ["produce", "create", "make"],
        "implement": ["execute", "carry out", "apply"],
        "industrial": ["manufacturing", "business", "commercial"],
        "manufacture": ["produce", "make", "fabricate"],
        "mechanism": ["process", "system", "operation"],
        "function": ["work", "operate", "perform"],
        "innovative": ["novel", "creative", "new"],
        "integrate": ["combine", "merge", "unite"],
    },
    "society": {
        "alter": ["change", "modify", "transform"],
        "aspect": ["facet", "dimension", "feature"],
        "attribute": ["character", "trait", "quality"],
        "compensate": ["offset", "make up for", "reimburse"],
        "concept": ["idea", "notion", "thought"],
        "consequent": ["resulting", "following", "ensuing"],
        "constitute": ["comprise", "form", "make up"],
        "context": ["setting", "environment", "background"],
        "individual": ["person", "specific", "single"],
        "interaction": ["communication", "exchange", "contact"],
        "perceive": ["notice", "observe", "see"],
        "significant": ["important", "notable", "considerable"],
    },
    "health": {
        "adequate": ["sufficient", "enough", "satisfactory"],
        "affect": ["influence", "impact", "concern"],
        "chronic": ["persistent", "ongoing", "long-term"],
        "clinical": ["medical", "hospital", "healthcare"],
        "competent": ["capable", "skilled", "proficient"],
        "contract": ["acquire", "develop", "catch"],
        "immune": ["resistant", "protected", "invulnerable"],
        "recover": ["heal", "recuperate", "get better"],
        "access": ["availability", "entry", "approach"],
        "exposure": ["contact", "encounter", "experience"],
        "prevent": ["stop", "avert", "preclude"],
        "treat": ["cure", "heal", "manage"],
    },
    "business": {
        "benefit": ["advantage", "profit", "gain"],
        "consume": ["use", "purchase", "buy"],
        "contract": ["agreement", "deal", "arrangement"],
        "decline": ["decrease", "reduce", "drop"],
        "dominate": ["control", "prevail", "rule"],
        "economic": ["financial", "fiscal", "monetary"],
        "employ": ["hire", "use", "engage"],
        "finance": ["fund", "capital", "money"],
        "purchase": ["buy", "acquire", "obtain"],
        "revenue": ["income", "earnings", "receipts"],
        "compete": ["contend", "rival", "vie"],
        "profit": ["gain", "earnings", "return"],
    },
    "government": {
        "authority": ["power", "control", "official"],
        "commission": ["committee", "body", "panel"],
        "designate": ["appoint", "specify", "name"],
        "enforce": ["implement", "compel", "apply"],
        "govern": ["rule", "manage", "administer"],
        "illegal": ["unlawful", "illicit", "prohibited"],
        "legitimate": ["legal", "lawful", "valid"],
        "policy": ["principle", "rule", "guideline"],
        "regulate": ["control", "supervise", "govern"],
        "institution": ["establishment", "organization", "body"],
        "legislation": ["law", "statute", "act"],
        "reform": ["revise", "improve", "transform"],
    },
}


NEGATION_TRIGGERS: Dict[str, List[str]] = {
    "否定前缀": ["un-", "in-", "im-", "ir-", "il-", "dis-", "non-", "anti-", "mis-"],
    "否定动词": ["fail", "lack", "miss", "deny", "refuse", "reject", "ignore", "negate"],
    "半否定词": ["hardly", "scarcely", "barely", "rarely", "seldom", "few", "little", "only"],
    "否定形容词": ["unlikely", "impossible", "unaware", "doubtful", "reluctant"],
    "转折连词": ["but", "however", "although", "though", "whereas", "while", "yet"],
    "否定代词": ["nothing", "nobody", "none", "neither", "nor"],
}


# 6 大替换类型（学术分类，非官方）
SUBSTITUTION_TYPES: Dict[str, str] = {
    "1. 词义替换 Lexical": "同义词 / 近义词替换（最常见，约 60% 考点）",
    "2. 词性转换 Grammatical": "动词 ↔ 名词 / 形容词等（约 25% 考点）",
    "3. 上下义 Hypernymy/Hyponymy": "概括 ↔ 具体（animal ↔ dog）",
    "4. 解释说明 Explanation": "用一句解释替代原词（最隐蔽）",
    "5. 否定 + 反义 Negation": "正话反说（difficult → not easy）",
    "6. 句式结构 Structural": "主动 ↔ 被动 / 简单 ↔ 复合 / 倒装",
}


def lookup(word: str) -> List:
    """查找单词的同义替换"""
    word = word.lower().strip()
    results = []
    for topic, families in AWL_FAMILIES.items():
        # 直接匹配
        if word in families:
            results.append((topic, word, families[word], "原词"))
        # 反向匹配：word 是某个原词的同义
        for key, values in families.items():
            if word in [v.lower() for v in values]:
                results.append((topic, key, [word] + [v for v in values if v.lower() != word], "同义"))
    return results


def list_topic(topic: str) -> None:
    """列出某话题所有词族"""
    if topic not in AWL_FAMILIES:
        print(f"\n未知话题：{topic}")
        print(f"可用话题：{', '.join(AWL_FAMILIES.keys())}")
        return
    print(f"\n【{topic}】AWL 词族（共 {len(AWL_FAMILIES[topic])} 族）：\n")
    for word, synonyms in AWL_FAMILIES[topic].items():
        print(f"  • {word}: {', '.join(synonyms)}")
    print()


def random_quiz(n: int = 5) -> None:
    """随机展示 N 个词族"""
    all_families = []
    for topic, families in AWL_FAMILIES.items():
        for word, synonyms in families.items():
            all_families.append((topic, word, synonyms))
    selected = random.sample(all_families, min(n, len(all_families)))
    print(f"\n随机 {n} 个 AWL 词族：\n")
    for topic, word, synonyms in selected:
        print(f"  • [{topic}] {word}: {', '.join(synonyms)}")


def quiz(n: int = 10) -> None:
    """生成 N 道同义替换练习题"""
    all_words = []
    for topic, families in AWL_FAMILIES.items():
        for word, synonyms in families.items():
            all_words.append((topic, word, synonyms))

    selected = random.sample(all_words, min(n, len(all_words)))
    print(f"\n【同义替换练习题】共 {len(selected)} 道\n")

    for i, (topic, word, synonyms) in enumerate(selected, 1):
        # 选 3 个同义 + 3 个干扰项
        correct = random.sample(synonyms, min(3, len(synonyms)))
        all_synonyms = []
        for _, syns in all_words:
            all_synonyms.extend(syns)
        all_synonyms = list(set(all_synonyms))
        distractors = random.sample([s for s in all_synonyms if s not in synonyms], 3)
        options = correct + distractors
        random.shuffle(options)

        print(f"题目 {i}（{topic}）：选出【{word}】的同义词")
        for j, opt in enumerate(options, 1):
            marker = "✓" if opt in correct else " "
            print(f"  [{marker}] {chr(64+j)}. {opt}")
        print(f"  答案：{correct}")
        print()


def show_negation() -> None:
    """显示否定替换触发器"""
    print("\n【否定替换触发器】（在原文出现立即标记 → 答案取反义）\n")
    for category, words in NEGATION_TRIGGERS.items():
        print(f"  • {category}：{', '.join(words)}")
    print("\n⚠️ 关键：做完 TFNG 题时，听到否定/半否定词 → 答案与原文相反！\n")


def show_types() -> None:
    """显示 6 大替换类型"""
    print("\n【阅读 6 大同义替换类型】（学术分类，非官方）\n")
    for type_name, desc in SUBSTITUTION_TYPES.items():
        print(f"  • {type_name}：{desc}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思阅读同义替换词族速查与练习工具（2026 版）")
    parser.add_argument("--word", type=str, help="查找单词的同义替换")
    parser.add_argument("--topic", type=str, help="列出某话题所有词族（education/research/environment/technology/society/health/business/government）")
    parser.add_argument("--random", type=int, help="随机展示 N 个词族")
    parser.add_argument("--quiz", type=int, help="生成 N 道同义替换练习题")
    parser.add_argument("--negation", action="store_true", help="显示否定替换触发器")
    parser.add_argument("--types", action="store_true", help="显示 6 大替换类型")
    parser.add_argument("--all", action="store_true", help="显示全部词族 + 否定 + 6 大类型")

    args = parser.parse_args()

    if args.word:
        results = lookup(args.word)
        if results:
            print(f"\n【{args.word}】的同义替换（AWL 词族）：\n")
            for topic, key, syns, kind in results:
                print(f"  {topic} ({kind}): {key} ↔ {', '.join(syns)}")
            print()
        else:
            print(f"\n未找到【{args.word}】在 AWL 词族中的同义替换")
            print("提示：AWL 仅覆盖学术文本 10% 词频（Coxhead 2000）。")
            print("试试 --topic 查看所有话题")
    elif args.topic:
        list_topic(args.topic)
    elif args.random:
        random_quiz(args.random)
    elif args.quiz:
        quiz(args.quiz)
    elif args.negation:
        show_negation()
    elif args.types:
        show_types()
    elif args.all:
        for topic in AWL_FAMILIES:
            list_topic(topic)
        show_negation()
        show_types()
    else:
        parser.print_help()
        print("\n用法示例：")
        print("  python3 paraphrase_quiz.py --word important")
        print("  python3 paraphrase_quiz.py --topic education")
        print("  python3 paraphrase_quiz.py --random 5")
        print("  python3 paraphrase_quiz.py --quiz 10")
        print("  python3 paraphrase_quiz.py --negation")
        print("  python3 paraphrase_quiz.py --all")


if __name__ == "__main__":
    main()
