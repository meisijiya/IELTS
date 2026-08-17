#!/usr/bin/env python3
"""
IELTS Listening 场景 + S4 学术话题词汇听写测试工具（2026 版）

基于 references/listening-scenario-vocabulary.md。
S1-S2 场景 9 大 + S4 学术话题 6 大。

Usage:
    python3 vocab_quiz.py --list
    python3 vocab_quiz.py --scenario accommodation --n 15
    python3 vocab_quiz.py --topic environment --n 10
    python3 vocab_quiz.py --all 20
"""

import argparse
import random


# S1-S2 场景词汇（精简版，约 250 词）
SCENARIO_VOCAB: dict = {
    "accommodation": [
        "single room", "double room", "twin room", "studio", "shared flat", "dormitory",
        "kitchen", "bathroom", "balcony", "garage", "garden", "central heating",
        "bed", "wardrobe", "desk", "chair", "sofa", "shelf", "lamp", "curtain", "carpet",
        "fridge", "washing machine", "microwave", "oven", "dishwasher",
        "rent", "deposit", "utility bills", "monthly fee", "inclusive of bills",
        "lease", "contract", "landlord", "tenant", "notice period", "reference",
    ],
    "travel": [
        "flight", "train", "bus", "coach", "ferry", "platform", "departure gate", "terminal",
        "ticket", "single", "return", "one-way", "timetable", "schedule", "reservation",
        "hotel", "hostel", "guesthouse", "check-in", "check-out", "reception",
        "luggage", "suitcase", "backpack", "hand luggage", "baggage allowance",
        "attraction", "landmark", "monument", "museum", "cathedral", "gallery",
        "sightseeing", "excursion", "guided tour", "day trip", "package tour",
    ],
    "medical": [
        "appointment", "GP", "specialist", "prescription", "consultation",
        "headache", "fever", "cough", "dizziness", "nausea", "fatigue",
        "tablets", "capsules", "syrup", "dosage", "side effects",
        "insurance", "claim", "policy", "coverage", "premium",
        "A&E", "ward", "clinic", "pharmacy",
    ],
    "job": [
        "CV", "resume", "cover letter", "application", "reference",
        "interview", "employer", "position", "vacancy", "salary", "wage",
        "duties", "responsibilities", "shift", "overtime", "full-time", "part-time",
        "manager", "engineer", "teacher", "nurse", "accountant", "consultant",
    ],
    "education": [
        "full-time", "part-time", "intensive", "crash course", "online course",
        "module", "lecture", "tutorial", "seminar", "workshop", "assignment",
        "exam", "test", "essay", "dissertation", "thesis", "grade",
        "undergraduate", "postgraduate", "master", "PhD", "diploma",
    ],
    "banking": [
        "account", "current account", "savings account", "joint account",
        "deposit", "withdraw", "transfer", "balance", "overdraft",
        "interest rate", "annual fee", "commission", "exchange rate",
        "credit card", "debit card", "cheque", "loan", "mortgage",
    ],
    "shopping": [
        "goods", "item", "product", "brand", "size", "colour", "material",
        "purchase", "order", "refund", "exchange", "receipt", "warranty",
        "cash", "card", "contactless", "voucher", "coupon", "discount",
        "department store", "supermarket", "market", "boutique",
    ],
    "leisure": [
        "concert", "performance", "exhibition", "festival", "carnival",
        "swimming", "cycling", "hiking", "climbing", "skiing", "yoga",
        "stadium", "arena", "theatre", "cinema", "gallery", "park",
        "membership", "subscription", "season ticket", "registration",
    ],
    "facility": [
        "library", "museum", "post office", "police station", "hospital",
        "car park", "bus stop", "railway station", "roundabout", "pedestrian crossing",
        "park", "square", "fountain", "monument", "playground", "sports centre",
        "north", "south", "east", "west", "opposite", "next to", "adjacent to", "behind",
    ],
}


# S4 学术话题词汇（2024-2026 真实考情）
TOPIC_VOCAB: dict = {
    "environment": [
        "habitat", "ecosystem", "biodiversity", "species", "extinction", "conservation",
        "climate change", "global warming", "carbon emissions", "greenhouse effect",
        "renewable energy", "solar power", "wind farm", "fossil fuel", "sustainability",
        "pollution", "contamination", "waste disposal", "recycling", "carbon footprint",
        "preservation", "protection", "restoration", "sustainable development",
    ],
    "psychology": [
        "participants", "subjects", "volunteers", "sample group", "control group",
        "cognitive", "perception", "memory", "emotion", "motivation", "behaviour",
        "experiment", "observation", "interview", "survey", "questionnaire",
        "findings", "results", "data analysis", "correlation", "hypothesis",
        "conclusion", "implication", "limitation", "significance",
    ],
    "history": [
        "excavation", "dig site", "artefact", "fossil", "remains", "ruins",
        "civilisation", "settlement", "dynasty", "empire", "colony",
        "era", "century", "decade", "prehistoric", "ancient", "medieval",
        "historian", "archaeologist", "scholar", "manuscript", "chronicle",
    ],
    "technology": [
        "technology", "innovation", "invention", "prototype", "mechanism",
        "data", "algorithm", "software", "digital", "virtual", "automated",
        "procedure", "process", "system", "function", "operation",
        "efficient", "effective", "accurate", "reliable", "limitation",
    ],
    "business": [
        "company", "corporation", "enterprise", "business", "organisation",
        "management", "strategy", "operation", "marketing", "finance",
        "economy", "market", "demand", "supply", "revenue", "profit",
        "employee", "workforce", "manager", "executive", "stakeholder",
    ],
    "education": [
        "teaching method", "curriculum", "syllabus", "assessment", "feedback",
        "learning style", "motivation", "engagement", "achievement",
        "study", "research", "survey", "case study", "longitudinal study",
    ],
}


def list_scenarios() -> None:
    """列出所有场景"""
    print("\nS1-S2 场景词汇：\n")
    for i, (scenario, words) in enumerate(SCENARIO_VOCAB.items(), 1):
        print(f"  {i:2d}. {scenario:20s} ({len(words)} 词)")
    print(f"\n共 {sum(len(v) for v in SCENARIO_VOCAB.values())} 词\n")


def list_topics() -> None:
    """列出所有 S4 学术话题"""
    print("\nS4 学术话题词汇：\n")
    for i, (topic, words) in enumerate(TOPIC_VOCAB.items(), 1):
        print(f"  {i:2d}. {topic:20s} ({len(words)} 词)")
    print(f"\n共 {sum(len(v) for v in TOPIC_VOCAB.values())} 词\n")


def quiz_scenario(scenario: str, n: int = 10) -> None:
    """某场景的听写测试"""
    if scenario not in SCENARIO_VOCAB:
        print(f"\n未知场景：{scenario}")
        list_scenarios()
        return

    words = SCENARIO_VOCAB[scenario]
    selected = random.sample(words, min(n, len(words)))

    print(f"\n场景【{scenario}】听写测试（{len(selected)} 词）：\n")
    print("提示：听音频后写下单词/词组，然后对照答案")
    print("─" * 50)
    for i, word in enumerate(selected, 1):
        print(f"  {i:2d}. [__________]    答案：{word}")
    print(f"\n总词数：{len(words)} | 本次抽取：{len(selected)}\n")
    print("训练法：")
    print("  1. 让朋友读或用 TTS 读单词/词组")
    print("  2. 你写下英文拼写")
    print("  3. 对照答案，错的标记为高频错词")
    print("  4. 错的 2 天后重新听写\n")


def quiz_topic(topic: str, n: int = 10) -> None:
    """某 S4 学术话题的听写测试"""
    if topic not in TOPIC_VOCAB:
        print(f"\n未知话题：{topic}")
        list_topics()
        return

    words = TOPIC_VOCAB[topic]
    selected = random.sample(words, min(n, len(words)))

    print(f"\nS4 学术话题【{topic}】听写测试（{len(selected)} 词）：\n")
    print("提示：听音频后写下单词/词组，然后对照答案")
    print("─" * 50)
    for i, word in enumerate(selected, 1):
        print(f"  {i:2d}. [__________]    答案：{word}")
    print(f"\n总词数：{len(words)} | 本次抽取：{len(selected)}\n")


def quiz_all(n: int = 20) -> None:
    """所有场景 + 话题混合出题"""
    all_vocab = []
    for scenario, words in SCENARIO_VOCAB.items():
        for word in words:
            all_vocab.append(("场景", scenario, word))
    for topic, words in TOPIC_VOCAB.items():
        for word in words:
            all_vocab.append(("话题", topic, word))

    selected = random.sample(all_vocab, min(n, len(all_vocab)))

    print(f"\n全场景 + S4 话题混合听写测试（{len(selected)} 词）：\n")
    print("─" * 60)
    for i, (kind, name, word) in enumerate(selected, 1):
        print(f"  {i:2d}. [__________]    答案：{word}    [{kind}/{name}]")
    print(f"\n总词数：{len(all_vocab)} | 本次抽取：{len(selected)}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思听力场景 + S4 学术话题词汇听写测试（2026 版）")
    parser.add_argument("--scenario", type=str, help="场景名（如 accommodation）")
    parser.add_argument("--topic", type=str, help="S4 学术话题（如 environment）")
    parser.add_argument("--n", type=int, default=10, help="出题数量（默认 10）")
    parser.add_argument("--all", type=int, help="混合所有场景 + 话题出题")
    parser.add_argument("--list", action="store_true", help="列出所有场景和话题")

    args = parser.parse_args()

    if args.list:
        list_scenarios()
        list_topics()
    elif args.scenario:
        quiz_scenario(args.scenario, args.n)
    elif args.topic:
        quiz_topic(args.topic, args.n)
    elif args.all:
        quiz_all(args.all)
    else:
        list_scenarios()
        list_topics()
        print("用法示例：")
        print("  python3 vocab_quiz.py --scenario accommodation --n 15")
        print("  python3 vocab_quiz.py --topic environment --n 10")
        print("  python3 vocab_quiz.py --all 20")
        print("  python3 vocab_quiz.py --list  (列出所有场景和话题)")


if __name__ == "__main__":
    main()