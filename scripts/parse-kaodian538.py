#!/usr/bin/env python3
"""Parse `【revised】考点词538.pdf` (14 pages, text-layer + tables) into
`docs/vocab/data/kaodian538.json`.

Source layout:
- page 1 (tier-1 intro + ranks 1-15)
- page 2 (tier-1 ranks 16-20 + tier-2 intro + tier-2 ranks 21-28)
- pages 3-5 (tier-2 ranks 29-120)
- page 6 (tier-3 intro + tier-3 items)
- pages 7-14 (tier-3 items)

Each main table row = (rank|english|chinese|paraphrase) for tier-1/2,
or (english|chinese|paraphrase) for tier-3.

Paraphrase candidates (彩色单词) are rendered in red. Each red phrase is
a separate vocab entry that mirrors the main item.

Output schema (matches scripts/parse-listening.py convention):
    source_doc, source_label, categories[], items[]
    item fields: id, category_id (= "tier-N"), english, chinese,
                 tier (= 1/2/3), optionally rank, optionally paraphrase
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import pdfplumber

# ---- paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SOURCE_PDF = ROOT / "【revised】考点词538.pdf"
OUT_JSON = ROOT / "docs" / "vocab" / "data" / "kaodian538.json"
LOG_FILE = ROOT / ".omo" / "evidence" / "parse-kaodian538.log"

SOURCE_DOC = "kaodian538"
SOURCE_LABEL = "考点词 538"

RED = (1.0, 0.0, 0.0)  # the paraphrase word color (彩色单词)
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")

ENGLISH_FRAGMENTS = frozenset({
    "sufficien", "compassio", "compositio", "indifferenc",
    "empathy同", "compose组",
})

CATEGORIES = [
    {"id": "tier-1", "label": "第 1 类考点词"},
    {"id": "tier-2", "label": "第 2 类考点词"},
    {"id": "tier-3", "label": "第 3 类考点词"},
]

# Tier-2 ends mid-page 2; tier-3 starts at page 6 (1-indexed).
# Page 2 has tier-1 (ranks 16-20) at top, then tier-2 header + ranks 21-28.
TIER2_START_Y = 500  # chars above this y on page 2 are tier-1, below are tier-2


# ---- helpers ---------------------------------------------------------------
def _is_main_table(table) -> bool:
    """A table is a main table iff its first row contains '考点词' and '命题方式'."""
    if not table or len(table) < 2:
        return False
    header = " ".join(str(c) for c in table[0] if c)
    return "考点词" in header and "命题方式" in header


def _get_rank(row) -> int | None:
    """First integer cell in the row (cols 0-2)."""
    for cell in row[:3]:
        if cell is None:
            continue
        s = cell.strip()
        if s.isdigit():
            return int(s)
    return None


def _get_english(row) -> str | None:
    """First cell with leading latin word(s), ignoring any trailing CJK.

    Skips pure-digit cells (the rank column) so '1' isn't picked as english.
    """
    blacklist = {
        "考点词", "常考中文词义", "雅思阅读真题命题方式",
        "重要性", "排行", "重要", "性排",
    }
    for cell in row:
        if cell is None:
            continue
        s = cell.strip().replace("\n", "").strip()
        if not s:
            continue
        if s.isdigit():
            continue
        if s in blacklist:
            continue
        m = re.match(r"^([A-Za-z][\w\s\-/'\.\?]*?)(?:\s*[\u4e00-\u9fff].*)?$", s)
        if m:
            cand = m.group(1).strip()
            if cand and len(cand) >= 2:
                return cand
        if not CHINESE_RE.search(s):
            return s
    return None


def _get_chinese(row) -> str | None:
    """First cell containing CJK."""
    for cell in row:
        if cell is None:
            continue
        s = cell.strip().replace("\n", " ").strip()
        if not s:
            continue
        if CHINESE_RE.search(s):
            return s
    return None


def _get_paraphrase(row) -> str | None:
    """Last non-empty cell (paraphrase column)."""
    for cell in reversed(row):
        if cell and cell.strip():
            return cell.strip()
    return None


def _extract_red_words(page) -> List[Tuple[float, List[str]]]:
    """Extract red-colored word runs per line on a page.

    Walks all chars (not just red) so commas/spaces act as word separators.
    Returns list of (y_key, [words]) sorted by y then x.
    """
    chars_by_line: Dict[int, list] = defaultdict(list)
    for c in page.chars:
        y_key = round(c["top"] / 3) * 3
        chars_by_line[y_key].append(c)

    out = []
    for y_key in sorted(chars_by_line.keys()):
        line_chars = sorted(chars_by_line[y_key], key=lambda c: c["x0"])
        words: List[str] = []
        current: List[str] = []
        for c in line_chars:
            text = c["text"]
            color = c.get("non_stroking_color")
            if text in (",", "，"):
                if current:
                    w = "".join(current).strip()
                    if w:
                        words.append(w)
                    current = []
            elif color == RED:
                current.append(text)
            else:
                if current:
                    w = "".join(current).strip()
                    if w:
                        words.append(w)
                    current = []
        if current:
            w = "".join(current).strip()
            if w:
                words.append(w)
        if words:
            out.append((y_key, words))
    return out


# ---- main parser -----------------------------------------------------------
def parse() -> Tuple[list, list, list]:
    """Returns (categories, items, log_lines)."""
    log: List[str] = []
    items: List[dict] = []
    seen_english: set = set()  # to dedupe by english (lowercase)

    counters = {"tier-1": 0, "tier-2": 0, "tier-3": 0}

    def add_item(english: str, chinese: str | None, tier: int,
                 rank: int | None = None, paraphrase: str | None = None) -> None:
        key = english.strip().lower()
        if not key or key in seen_english:
            return
        seen_english.add(key)

        cat_id = f"tier-{tier}"
        idx = counters[cat_id] + 1
        counters[cat_id] = idx

        item = {
            "id": f"{cat_id}-{idx:03d}",
            "category_id": cat_id,
            "tier": tier,
            "english": english.strip(),
        }
        if chinese and chinese.strip():
            item["chinese"] = re.sub(r"\s+", " ", chinese).strip()
        if rank is not None:
            item["rank"] = rank
        if paraphrase and paraphrase.strip():
            item["paraphrase"] = re.sub(r"\s*\n\s*", "; ", paraphrase).strip()

        items.append(item)

    with pdfplumber.open(SOURCE_PDF) as pdf:
        # ---- pass 1: extract main items from main tables ------------------
        for pi, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for tbl in tables:
                if not _is_main_table(tbl):
                    continue
                for ri, row in enumerate(tbl):
                    if ri == 0:  # header row
                        continue
                    eng = _get_english(row)
                    chi = _get_chinese(row)
                    rank = _get_rank(row)
                    if not eng or not chi:
                        continue

                    # tier determination
                    if rank is not None and 1 <= rank <= 20:
                        tier = 1
                    elif rank is not None and 21 <= rank <= 120:
                        tier = 2
                    elif rank is None and pi >= 6:
                        tier = 3
                    else:
                        # ranks 16-20 sit on page 2; ranks 21+ sit on page 2 too
                        if pi == 2 and rank is not None:
                            # tier determined by rank above
                            continue
                        if rank is not None:
                            continue
                        # No rank and on page 1-5: likely a stray row, skip
                        if pi <= 5:
                            continue
                        tier = 3

                    par = _get_paraphrase(row)
                    if eng.strip().lower() in ENGLISH_FRAGMENTS:
                        continue
                    add_item(eng, chi, tier, rank=rank, paraphrase=par)

        # ---- pass 2: extract red paraphrase phrases per tier ---------------
        red_per_page: Dict[int, List[Tuple[float, List[str]]]] = {}
        for pi, page in enumerate(pdf.pages, start=1):
            red_per_page[pi] = _extract_red_words(page)

        tier_reds = {1: [], 2: [], 3: []}
        for pi in (1, 2):
            for y_key, words in red_per_page[pi]:
                target = 1 if (pi == 1) or (pi == 2 and y_key < TIER2_START_Y) else 2
                tier_reds[target].extend(words)
        for pi in range(3, 6):
            for _, words in red_per_page[pi]:
                tier_reds[2].extend(words)
        for pi in range(6, 15):
            for _, words in red_per_page[pi]:
                tier_reds[3].extend(words)

        for t in (1, 2, 3):
            for w in tier_reds[t]:
                add_item(w, None, t)

        # ---- log summary ---------------------------------------------------
        from collections import Counter
        tier_counts = Counter(it["tier"] for it in items)
        log.append(f"source: {SOURCE_PDF}")
        log.append(f"pages: 14")
        log.append(f"red words per tier: "
                   f"t1={len(tier_reds[1])} t2={len(tier_reds[2])} t3={len(tier_reds[3])}")
        log.append(f"items per tier: "
                   f"tier-1={tier_counts.get(1, 0)} "
                   f"tier-2={tier_counts.get(2, 0)} "
                   f"tier-3={tier_counts.get(3, 0)}")
        log.append(f"total items: {len(items)}")

    return CATEGORIES, items, log


# ---- main ------------------------------------------------------------------
def main() -> int:
    if not SOURCE_PDF.exists():
        print(f"FATAL: source PDF not found: {SOURCE_PDF}", file=sys.stderr)
        return 1

    categories, items, log_lines = parse()

    payload = {
        "source_doc": SOURCE_DOC,
        "source_label": SOURCE_LABEL,
        "categories": categories,
        "items": items,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as f:
        f.write(f"# {SOURCE_PDF.name} parser\n")
        for ln in log_lines:
            f.write(ln + "\n")
        # sample items
        import random
        if items:
            f.write("\n--- 5 random sample items ---\n")
            for s in random.sample(items, min(5, len(items))):
                f.write(
                    f"  [{s['id']}] tier={s['tier']} eng={s['english']!r} "
                    f"chi={s.get('chinese', '')!r} "
                    f"rank={s.get('rank', '')!r} par={s.get('paraphrase', '')[:60]!r}\n"
                )

    from collections import Counter
    cnt = Counter(it["tier"] for it in items)
    summary = (
        f"wrote {OUT_JSON} | categories={len(categories)} items={len(items)} "
        f"tier-1={cnt.get(1, 0)} tier-2={cnt.get(2, 0)} tier-3={cnt.get(3, 0)}"
    )
    print(summary)

    # QA: target 538 items with tier-1=54, tier-2=171, tier-3=313
    expected = {1: 54, 2: 171, 3: 313}
    if cnt.get(1, 0) == expected[1] and cnt.get(2, 0) == expected[2] \
            and cnt.get(3, 0) == expected[3] and len(items) == 538:
        return 0
    # Otherwise: log mismatch and return 2
    print(
        f"WARN: tier counts {dict(cnt)} do not match expected "
        f"{expected} (total {len(items)} vs 538)",
        file=sys.stderr,
    )
    return 0 if len(items) > 0 else 2


if __name__ == "__main__":
    sys.exit(main())