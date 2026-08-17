#!/usr/bin/env python3
"""Parse `口语 Part1 5-8月collocations.docx` into `docs/vocab/data/speaking-p1.json`.

Source layout (per topic block):
    N. <Topic Title>
    ① <english collocation>
    <chinese translation>
    <example sentence>
    适用：                (optional — appears in topics 1–5 and 11–32)
    * ...                 (optional bullet prompts)
    ② <english collocation>
    <chinese translation>
    <example sentence>
    适用：                (optional)
    * ...                 (optional)

There are 32 topics × 2 collocations = 64 items.

Output schema (locked by .omo/plans/five-modules-expansion.md §lines 133–185):
    source_doc, source_label, categories[], items[]
    item fields: id, category_id, english, chinese, example_en
                 + optional ipa, example_zh, tags, tier, part_label
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import List

from docx import Document  # python-docx

# ---- paths ---------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent  # repo root
SOURCE_DOCX = ROOT / "口语 Part1 5-8月collocations.docx"
OUT_JSON = ROOT / "docs" / "vocab" / "data" / "speaking-p1.json"
LOG_FILE = ROOT / ".omo" / "evidence" / "parse-speaking-p1.log"

SOURCE_DOC = "speaking-p1"
SOURCE_LABEL = "口语 Part1 5-8月 collocations"

# Topics 1–5 are the official Part 1 "anchor" topics (Hometown, Work or Studies,
# Home / Accommodation, The Area You Live In, The City You Live In); the rest
# belong to the rotating question pool. This split is purely a naming convention
# for category_id and matches the example ids in the plan.
ANCHOR_TOPIC_COUNT = 5


# ---- logging helpers ------------------------------------------------------
def _log_lines(lines: List[str]) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- slug / id helpers ----------------------------------------------------
def slugify(label: str) -> str:
    """Lowercase + collapse non-alnum to single hyphens, strip leading/trailing."""
    s = label.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def make_category_id(topic_num: int, title: str) -> str:
    prefix = "p1" if topic_num <= ANCHOR_TOPIC_COUNT else "p1f"
    return f"{prefix}-{slugify(title)}"


def make_item_id(category_id: str, slot: int) -> str:
    return f"{category_id}-{slot}"


# ---- parsing --------------------------------------------------------------
TOPIC_RE = re.compile(r"^(\d+)\.\s+(.+)$")
ITEM_RE = re.compile(r"^[①②]\s+(.+)$")


def parse_docx(path: Path) -> tuple[list[dict], list[dict], list[str]]:
    """Return (categories, items, log_lines)."""
    doc = Document(str(path))
    paras = [p.text.strip() for p in doc.paragraphs]

    log: List[str] = [f"source: {path}", f"paragraphs: {len(paras)}"]

    # 1. locate topic headers
    topic_positions: list[tuple[int, int, str]] = []  # (para_idx, num, title)
    for i, t in enumerate(paras):
        m = TOPIC_RE.match(t)
        if m:
            topic_positions.append((i, int(m.group(1)), m.group(2).strip()))
    log.append(f"topics detected: {len(topic_positions)}")
    if len(topic_positions) != 32:
        log.append(f"WARNING: expected 32 topics, got {len(topic_positions)}")

    # 2. iterate topic blocks
    categories: list[dict] = []
    items: list[dict] = []
    topic_blocks = topic_positions + [(len(paras), 0, "")]

    for idx in range(len(topic_positions)):
        start, num, title = topic_positions[idx]
        end = topic_blocks[idx + 1][0]
        block = paras[start:end]

        category_id = make_category_id(num, title)
        categories.append({"id": category_id, "label": title})

        # find ① and ② markers within this block
        slots: list[tuple[int, int, str]] = []  # (para_offset, marker_num, english)
        for off, line in enumerate(block):
            m = ITEM_RE.match(line)
            if m:
                marker_num = 1 if line.startswith("①") else 2
                slots.append((off, marker_num, m.group(1).strip()))

        if len(slots) != 2:
            log.append(f"WARNING: topic {num} '{title}' has {len(slots)} items (expected 2)")

        for off, marker_num, english in slots:
            chinese = ""
            example_en = ""
            # scan forward from the marker to collect chinese + example_en
            j = off + 1
            collected = []
            while j < len(block):
                line = block[j]
                if not line:
                    j += 1
                    continue
                if line.startswith("①") or line.startswith("②"):
                    break  # next item starts
                if line == "适用：" or line.startswith("*"):
                    j += 1
                    continue  # skip applicability hints
                if line == "�":
                    j += 1
                    continue  # skip separator
                collected.append(line)
                if len(collected) >= 2:
                    break
                j += 1
            if len(collected) >= 1:
                chinese = collected[0]
            if len(collected) >= 2:
                example_en = collected[1]

            item = {
                "id": make_item_id(category_id, marker_num),
                "category_id": category_id,
                "english": english,
                "chinese": chinese,
                "example_en": example_en,
            }
            items.append(item)
            log.append(f"  item {len(items):02d} [{category_id}#{marker_num}] {english!r} -> {chinese!r}")

    return categories, items, log


# ---- main -----------------------------------------------------------------
def main() -> int:
    if not SOURCE_DOCX.exists():
        print(f"FATAL: source not found: {SOURCE_DOCX}", file=sys.stderr)
        return 1

    categories, items, log = parse_docx(SOURCE_DOCX)

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

    summary = (
        f"wrote {OUT_JSON} | categories={len(categories)} items={len(items)}"
    )
    print(summary)
    log.append("---")
    log.append(summary)
    _log_lines(log)

    # hard invariant: this script's contract is 64 items across 32 topics
    if len(items) != 64:
        print(
            f"FATAL: items count {len(items)} != 64 (see {LOG_FILE})",
            file=sys.stderr,
        )
        return 1
    if len(categories) != 32:
        print(
            f"FATAL: categories count {len(categories)} != 32 (see {LOG_FILE})",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
