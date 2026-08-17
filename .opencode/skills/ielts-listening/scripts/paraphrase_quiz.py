#!/usr/bin/env python3
"""
IELTS Listening 同义替换词族速查与练习工具（2026 版）

基于 references/listening-paraphrase.md 中的 60 个高频词族。

Usage:
    python3 paraphrase_quiz.py --word important
    python3 paraphrase_quiz.py --category opinion
    python3 paraphrase_quiz.py --random 5
    python3 paraphrase_quiz.py --quiz 10
    python3 paraphrase_quiz.py --negation
    python3 paraphrase_quiz.py --signal
    python3 paraphrase_quiz.py --all
"""

import argparse
import random
import sys
from typing import Dict, List


# 60 个高频同义替换词族（精简版，去除 80+ 中的低频词）
WORD_FAMILIES: Dict[str, Dict[str, List[str]]] = {
    "opinion": {
        "important": ["significant", "crucial", "vital", "essential", "key"],
        "useful": ["helpful", "beneficial", "valuable", "practical"],
        "difficult": ["hard", "challenging", "demanding", "tough"],
        "interesting": ["fascinating", "intriguing", "appealing", "engaging"],
        "agree": ["concur", "share the view", "be of the same opinion"],
        "disagree": ["contradict", "oppose", "be against", "differ"],
        "worried": ["concerned", "anxious", "troubled", "uneasy"],
    },
    "change": {
        "increase": ["rise", "grow", "expand", "climb", "escalate", "soar"],
        "decrease": ["fall", "drop", "decline", "reduce", "diminish", "plunge"],
        "change": ["alter", "modify", "transform", "shift", "convert"],
        "improve": ["enhance", "upgrade", "refine", "ameliorate"],
        "remain": ["stay", "persist", "continue", "maintain"],
        "expand": ["extend", "enlarge", "broaden", "widen"],
    },
    "frequency": {
        "always": ["constantly", "continuously", "all the time", "every time"],
        "often": ["frequently", "regularly", "commonly", "repeatedly"],
        "sometimes": ["occasionally", "periodically", "from time to time", "now and then"],
        "rarely": ["seldom", "hardly ever", "scarcely ever", "infrequently"],
        "never": ["not ever", "at no time", "under no circumstances"],
    },
    "abstract": {
        "opportunity": ["chance", "prospect", "possibility", "opening"],
        "challenge": ["difficulty", "problem", "obstacle", "hurdle"],
        "benefit": ["advantage", "merit", "profit", "gain"],
        "problem": ["issue", "trouble", "difficulty", "complication"],
        "solution": ["answer", "resolution", "remedy", "key"],
        "impact": ["effect", "influence", "consequence"],
        "evidence": ["proof", "indication", "sign", "data", "findings"],
        "method": ["way", "approach", "technique", "procedure", "means"],
        "purpose": ["aim", "goal", "objective", "intention"],
    },
    "action": {
        "need": ["require", "demand", "call for", "be in need of"],
        "give": ["provide", "supply", "offer", "donate", "distribute"],
        "take": ["receive", "accept", "obtain", "acquire"],
        "help": ["assist", "aid", "support", "facilitate"],
        "prevent": ["stop", "halt", "inhibit", "restrain", "curb"],
        "protect": ["safeguard", "shield", "guard", "preserve"],
        "damage": ["harm", "hurt", "impair", "destroy", "ruin"],
    },
    "academic": {
        "research": ["study", "investigation", "inquiry", "exploration"],
        "theory": ["hypothesis", "concept", "notion", "assumption"],
        "experiment": ["trial", "test", "investigation", "examination"],
        "discover": ["find", "identify", "detect", "uncover", "reveal"],
        "conclude": ["determine", "decide", "deduce", "infer"],
        "analyse": ["examine", "study", "investigate", "break down"],
    },
    "environment": {
        "environment": ["surroundings", "setting", "ecosystem", "habitat"],
        "climate": ["weather patterns", "atmospheric conditions"],
        "sustainable": ["eco-friendly", "renewable", "long-lasting"],
        "pollution": ["contamination", "emissions", "waste"],
        "conservation": ["preservation", "protection", "safeguarding"],
        "biodiversity": ["variety of life", "ecological diversity"],
    },
    "spatial": {
        "near": ["close by", "nearby", "adjacent to", "within walking distance"],
        "far": ["a long way from", "distant from", "remote from"],
        "opposite": ["across from", "facing", "on the other side of"],
        "next_to": ["beside", "by", "alongside"],
        "between": ["in the middle of", "among"],
    },
    "direction": {
        "left": ["on the left", "to the left of", "on your left"],
        "right": ["on the right", "to the right of", "on your right"],
        "north": ["northern", "in the north of"],
        "south": ["southern", "in the south of"],
        "straight": ["straight ahead", "straight forward", "keep going"],
    },
    "verb_noun": {
        "decide/decision": ["make a decision", "determination", "conclusive"],
        "arrive/arrival": ["get to", "reaching", "incoming"],
        "analyse/analysis": ["examine", "breakdown", "methodical"],
        "grow/growth": ["expand", "increase", "mature"],
        "succeed/success": ["achieve", "accomplishment", "triumphant"],
        "create/creation": ["produce", "innovation", "inventive"],
        "develop/development": ["evolve", "advancement", "emerging"],
        "perform/performance": ["execute", "execution", "active"],
        "signify/significance": ["mean", "importance", "significant"],
    },
}


NEGATION_TRIGGERS: Dict[str, List[str]] = {
    "否定前缀": ["un-", "in-", "im-", "ir-", "il-", "dis-", "non-", "anti-", "mis-"],
    "否定动词": ["fail", "lack", "miss", "deny", "refuse", "reject", "ignore"],
    "半否定词": ["hardly", "scarcely", "barely", "rarely", "seldom", "few", "little", "only"],
    "否定形容词": ["unlikely", "impossible", "unaware", "doubtful"],
}


SIGNAL_WORDS: Dict[str, List[str]] = {
    "因果": ["because", "since", "as", "so", "therefore", "thus", "hence", "consequently", "due to"],
    "序列": ["first", "second", "third", "next", "then", "finally", "subsequently", "meanwhile"],
    "转折": ["but", "however", "although", "though", "yet", "while", "whereas", "despite", "instead"],
    "列举": ["and", "also", "as well as", "in addition", "moreover", "besides", "apart from"],
    "举例": ["for example", "for instance", "such as", "like", "including", "namely"],
    "强调": ["very", "really", "extremely", "particularly", "especially", "definitely", "absolutely"],
    "总结": ["in conclusion", "to sum up", "overall", "in summary"],
    "否定": ["no", "not", "never", "none", "nobody", "nothing", "hardly", "rarely", "only"],
}


def lookup(word: str) -> List:
    """查找单词的同义替换"""
    word = word.lower().strip()
    results = []
    for category, families in WORD_FAMILIES.items():
        # 直接匹配
        if word in families:
            results.append((category, word, families[word], "原词"))
        # 反向匹配：word 是某个原词的同义
        for key, values in families.items():
            if word in [v.lower() for v in values]:
                results.append((category, key, [word] + [v for v in values if v.lower() != word], "同义"))
    return results


def list_category(category: str) -> None:
    """列出某类别所有词族"""
    if category not in WORD_FAMILIES:
        print(f"\n未知类别：{category}")
        print(f"可用类别：{', '.join(WORD_FAMILIES.keys())}")
        return
    print(f"\n【{category}】类别同义替换词族（共 {len(WORD_FAMILIES[category])} 族）：\n")
    for word, synonyms in WORD_FAMILIES[category].items():
        print(f"  • {word}: {', '.join(synonyms)}")
    print()


def random_quiz(n: int = 5) -> None:
    """随机出 N 道同义替换练习题"""
    all_words = []
    for category, families in WORD_FAMILIES.items():
        for word, synonyms in families.items():
            all_words.append((word, synonyms, category))

    selected = random.sample(all_words, min(n, len(all_words)))
    print(f"\n同义替换练习题（共 {len(selected)} 道）：\n")

    for i, (word, synonyms, category) in enumerate(selected, 1):
        # 选 3 个同义 + 3 个干扰项
        correct = random.sample(synonyms, min(3, len(synonyms)))
        all_synonyms = []
        for _, syns, _ in all_words:
            all_synonyms.extend(syns)
        all_synonyms = list(set(all_synonyms))
        distractors = random.sample([s for s in all_synonyms if s not in synonyms], 3)
        options = correct + distractors
        random.shuffle(options)

        print(f"题目 {i}（{category}）：选出【{word}】的同义词")
        for j, opt in enumerate(options, 1):
            marker = "✓" if opt in correct else " "
            print(f"  [{marker}] {chr(64+j)}. {opt}")
        print(f"  答案：{correct}")
        print()


def show_negation() -> None:
    """显示否定替换触发器"""
    print("\n否定替换触发器（听到这些 → 反义替换警报）：\n")
    for category, words in NEGATION_TRIGGERS.items():
        print(f"  • {category}：{', '.join(words)}")
    print("\n听到否定/半否定词时，答案通常与音频意思相反！\n")


def show_signal() -> None:
    """显示信号词分类"""
    print("\n雅思听力 8 类信号词：\n")
    for category, words in SIGNAL_WORDS.items():
        print(f"  • {category}：{', '.join(words)}")
    print("\n信号词后往往跟着考点答案！\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="雅思听力同义替换词族速查与练习工具（2026 版）")
    parser.add_argument("--word", type=str, help="查找单词的同义替换")
    parser.add_argument("--category", type=str, help="列出某类别所有词族")
    parser.add_argument("--random", type=int, help="随机展示 N 个词族")
    parser.add_argument("--quiz", type=int, help="生成 N 道同义替换练习题")
    parser.add_argument("--negation", action="store_true", help="显示否定替换触发器")
    parser.add_argument("--signal", action="store_true", help="显示 8 类信号词")
    parser.add_argument("--all", action="store_true", help="显示全部词族")

    args = parser.parse_args()

    if args.word:
        results = lookup(args.word)
        if results:
            print(f"\n【{args.word}】的同义替换：\n")
            for category, key, syns, kind in results:
                print(f"  {category} ({kind}): {key} ↔ {', '.join(syns)}")
            print()
        else:
            print(f"\n未找到【{args.word}】的同义替换")
            print("试试 --category 查看所有类别")
    elif args.category:
        list_category(args.category)
    elif args.random:
        all_families = []
        for category, families in WORD_FAMILIES.items():
            for word, syns in families.items():
                all_families.append((category, word, syns))
        selected = random.sample(all_families, min(args.random, len(all_families)))
        print(f"\n随机 {args.random} 个同义替换词族：\n")
        for category, word, syns in selected:
            print(f"  • [{category}] {word}: {', '.join(syns)}")
    elif args.quiz:
        random_quiz(args.quiz)
    elif args.negation:
        show_negation()
    elif args.signal:
        show_signal()
    elif args.all:
        for category in WORD_FAMILIES:
            list_category(category)
        show_negation()
        show_signal()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()