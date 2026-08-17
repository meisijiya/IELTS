#!/usr/bin/env python3
"""Parse `写作 collocation.pdf` (pure-image PDF, 18 pages) into `docs/vocab/data/writing.json`.

Layout per page (OCR'd at 200 DPI, lang='eng+chi_sim'):
    N. <Topic>类                  ← Chinese topic header (may be OCR-missed)
    english phrase  中文 翻译
    english phrase  中文 翻译 (parenthetical example)   ← example may span lines

5 of 9 topic headers are OCR-recoverable; 4 are inferred from content boundaries
(二、四、六、七). Inferred labels are logged as warnings.

Output schema (matches scripts/parse-speaking-p1.py convention):
    source_doc, source_label, categories[], items[]
    item fields: id, category_id, english, chinese, example_en
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Tesseract binary was extracted into /tmp/opencode/tess_root (no sudo available,
# so we point pytesseract at the local binary and prepend its lib dir).
TESS_ROOT = Path("/tmp/opencode/tess_root")
os.environ.setdefault("LD_LIBRARY_PATH", str(TESS_ROOT / "usr/lib/x86_64-linux-gnu"))
os.environ.setdefault("TESSDATA_PREFIX", str(TESS_ROOT / "usr/share/tesseract-ocr/5/tessdata/"))

import pytesseract  # noqa: E402  (must come after env-var setup)
pytesseract.pytesseract.tesseract_cmd = str(TESS_ROOT / "usr/bin/tesseract")

import pypdfium2 as pdfium  # noqa: E402
from PIL import Image  # noqa: E402

# ---- paths ---------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SOURCE_PDF = ROOT / "写作 collocation.pdf"
OUT_JSON = ROOT / "docs" / "vocab" / "data" / "writing.json"
LOG_FILE = ROOT / ".omo" / "evidence" / "parse-writing.log"
ISSUES_FILE = ROOT / ".omo" / "notepads" / "five-modules-expansion" / "issues.md"

SOURCE_DOC = "writing"
SOURCE_LABEL = "写作 collocation"

# ---- topic map (Chinese ordinal → inferred slug + label) ---------------
# 五 and 八 and 九 are confirmed by OCR; the rest are inferred from content boundaries.
# Slugs are kept lowercase-english, dashes-as-separators (per task spec).
TOPIC_MAP: Dict[str, Dict[str, str]] = {
    "一": {"slug": "education",       "label": "教育"},
    "二": {"slug": "language",        "label": "语言"},            # inferred: linguistic terms
    "三": {"slug": "culture",         "label": "文化"},
    "四": {"slug": "government",      "label": "政府社会"},        # inferred: politics/media/society
    "五": {"slug": "work",            "label": "工作"},
    "六": {"slug": "environment",     "label": "环境"},            # inferred: pollution/urban
    "七": {"slug": "society",         "label": "社会"},            # inferred: family/class
    "八": {"slug": "animal-protection", "label": "动物保护"},
    "九": {"slug": "technology",      "label": "科技"},
}
INFERRED_TOPICS = {"二", "四", "六", "七"}

NUM = "一二三四五六七八九十"
HEADER_RE = re.compile(rf"^\s*([{NUM}])\s*[、,\.]\s*(.+?)\s*$")

CJK_RE = re.compile(r"[一-鿿]")
PAGE_HEADER_RE = re.compile(rf"^\s*[{NUM}]\s*[、,\.]\s*.{{0,15}}\s*类\s*$")
GARBAGE_LINE_RE = re.compile(r"^[\W_]+$")


# ---- logging -------------------------------------------------------------
def log(msg: str) -> None:
    print(msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(msg + "\n")


def reset_log() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("", encoding="utf-8")


# ---- OCR -----------------------------------------------------------------
def ocr_pages(pdf: "pdfium.PdfDocument") -> List[str]:
    """Render all pages and return OCR text per page."""
    out: List[str] = []
    for i in range(len(pdf)):
        img: Image.Image = pdf[i].render(scale=200 / 72).to_pil()
        text = pytesseract.image_to_string(img, lang="eng+chi_sim")
        out.append(text)
    return out


# ---- topic segmentation --------------------------------------------------
def detect_topic_at_line(line: str) -> str | None:
    """Return Chinese ordinal ('一'..'九') if line looks like a topic header."""
    s = line.strip()
    if not s or len(s) > 30:
        return None
    if not PAGE_HEADER_RE.match(s):
        return None
    m = HEADER_RE.match(s)
    return m.group(1) if m else None


def segment_by_topic(pages: List[str]) -> List[Tuple[str, List[str]]]:
    """Walk pages sequentially; for each detected topic header, start a new bucket.

    Lines before the first header go to bucket '一'. If a page straddles two
    topics, split at the header line. Inferred topic headers (二/四/六/七) are
    injected when no explicit header is found but content boundaries suggest
    a new topic — heuristic by page index (see _maybe_inject).
    """
    # page → first ordinal seen on it, or None
    page_first: Dict[int, str] = {}
    for i, txt in enumerate(pages):
        for ln in txt.split("\n"):
            o = detect_topic_at_line(ln)
            if o:
                page_first[i] = o
                break

    detected = sorted(set(page_first.values()))
    log(f"OCR-detected topic headers: {detected}")
    log(f"Inferred topic headers:     {sorted(INFERRED_TOPICS)}")

    # Inject missing ordinals in numerical order. For each detected header, infer
    # the missing ones that lie strictly between the previous detected ordinal
    # and this one (or between last detected and end).
    full_ord: List[str] = list("一二三四五六七八九")
    topic_starts: Dict[str, int] = {o: pg for pg, o in page_first.items()}
    last_det = ""
    for o in full_ord:
        if o in topic_starts:
            last_det = o
            continue
        if not last_det:
            continue
        # find next detected ordinal after `o`
        nxt = next((x for x in full_ord if x in topic_starts and full_ord.index(x) > full_ord.index(o)), None)
        if not nxt:
            continue
        # inject midpoint between last_det and nxt
        a, b = full_ord.index(last_det), full_ord.index(nxt)
        i = full_ord.index(o)
        topic_starts[o] = int(round(
            topic_starts[last_det] + (topic_starts[nxt] - topic_starts[last_det]) * (i - a) / (b - a)
        ))
        last_det = o

    log(f"Topic start pages: {dict(sorted(topic_starts.items()))}")

    # Assign each page to one topic bucket based on greatest start ≤ page idx.
    sorted_ord = sorted(topic_starts.keys(), key=lambda x: full_ord.index(x))
    buckets: Dict[str, List[str]] = {o: [] for o in full_ord}
    for pg_idx, txt in enumerate(pages):
        owner = sorted_ord[0]
        for o in sorted_ord:
            if topic_starts[o] <= pg_idx:
                owner = o
        buckets[owner].append(txt)

    return [(o, buckets[o]) for o in full_ord]


# ---- collocation parsing -------------------------------------------------
def split_english_chinese(line: str) -> Tuple[str, str]:
    """Return (english, chinese) for a single collocation line.

    Strategy: english is the longest ASCII-leading run; chinese is the rest
    (Chinese chars + any English/numbers interleaved as pinyin/gloss).
    """
    s = line.strip()
    # find first CJK char
    m = CJK_RE.search(s)
    if not m:
        return (s, "")
    eng = s[: m.start()].strip()
    chi = s[m.start():].strip()
    # strip a leading '*' / 'x' marker from english (OCR noise flag)
    eng = re.sub(r"^[x*]+\s*", "", eng)
    return (eng, chi)


def extract_example(line: str) -> Tuple[str, str | None]:
    """If line ends with a balanced (...) example, return (stripped_line, example)."""
    # only consider parenthetical that starts after the english+chinese portion
    # i.e. an open '(' that isn't inside the chinese portion's brackets
    if "(" not in line and "（" not in line:
        return (line, None)
    # find the LAST '(' that has matching ')' at end of line
    opens = [i for i, c in enumerate(line) if c in "(（"]
    for i in reversed(opens):
        close = ")" if line[i] == "(" else "）"
        if line.rstrip().endswith(close):
            inner = line[i + 1: line.rstrip().rfind(close)]
            stripped = (line[:i] + line[line.rstrip().rfind(close) + 1:]).strip()
            return (stripped, inner.strip())
    return (line, None)


def parse_items(buckets: List[Tuple[str, List[str]]]) -> Tuple[List[dict], List[dict], List[str]]:
    """Return (categories, items, log_lines)."""
    categories: List[dict] = []
    items: List[dict] = []
    log_lines: List[str] = []
    per_topic_counts: Dict[str, int] = {}

    for ordinal, page_texts in buckets:
        info = TOPIC_MAP[ordinal]
        cat_id = info["slug"]
        categories.append({
            "id": cat_id,
            "ordinal": ordinal,
            "label": info["label"],
            "label_zh": f"{ordinal}、{info['label']}类",
            "inferred": ordinal in INFERRED_TOPICS,
        })
        if ordinal in INFERRED_TOPICS:
            log_lines.append(f"WARN: topic '{ordinal}' label '{info['label']}' inferred from content (no OCR header)")
        slot = 0
        current: Dict | None = None

        for page_text in page_texts:
            for raw in page_text.split("\n"):
                line = raw.strip()
                if not line:
                    if current and current.get("_open_paren"):
                        # blank line inside paren — keep buffer
                        continue
                    continue
                # skip detected topic headers
                if detect_topic_at_line(line):
                    current = None
                    continue
                # skip very short / garbage
                if len(line) < 3:
                    continue
                # skip pure instruction page header (pg 0)
                if line.startswith("Instruction"):
                    continue
                if line.startswith("打印"):
                    continue
                if line.startswith("平常"):
                    continue
                if line.startswith("Collocation 对"):
                    continue

                # continuation of previous entry's parenthetical?
                if current and current.get("_open_paren") and not CJK_RE.search(line):
                    current["_example_buf"].append(line)
                    joined = " ".join(current["_example_buf"])
                    # try to close on first matching ')'
                    close_i = joined.find(")")
                    if close_i != -1:
                        current["example_en"] = joined[:close_i].strip(" (")
                        # remainder after ')' is a fresh entry, reprocess
                        remainder = joined[close_i + 1:].strip()
                        current.pop("_open_paren", None)
                        current.pop("_example_buf", None)
                        current = None
                        if remainder and CJK_RE.search(remainder):
                            line = remainder
                        else:
                            continue
                    else:
                        continue

                # detect an unclosed paren (multi-line example)
                has_open = False
                if "(" in line or "（" in line:
                    opens = line.count("(") + line.count("（")
                    closes = line.count(")") + line.count("）")
                    if opens > closes:
                        has_open = True

                stripped, example = extract_example(line)
                eng, chi = split_english_chinese(stripped)
                if not eng or not chi:
                    continue
                # filter entries with too few Chinese chars (likely OCR garbage)
                if len(CJK_RE.findall(chi)) < 2:
                    continue

                slot += 1
                item = {
                    "id": f"{cat_id}-{slot}",
                    "category_id": cat_id,
                    "english": eng,
                    "chinese": chi,
                }
                if example:
                    item["example_en"] = example
                if has_open:
                    item["_open_paren"] = True
                    item["_example_buf"] = [example] if example else []
                items.append(item)
                current = item

        per_topic_counts[ordinal] = slot
        log_lines.append(f"topic {ordinal} ({cat_id}): {slot} items")

    log_lines.append(f"TOTAL items: {sum(per_topic_counts.values())}")
    return categories, items, log_lines


# ---- main ----------------------------------------------------------------
def main() -> int:
    reset_log()
    log(f"source: {SOURCE_PDF}")
    log(f"output: {OUT_JSON}")

    pdf = pdfium.PdfDocument(str(SOURCE_PDF))
    log(f"pages: {len(pdf)}")

    pages = ocr_pages(pdf)
    for i, t in enumerate(pages):
        log(f"  page {i:02d}: {len(t):5d} chars OCR'd")

    buckets = segment_by_topic(pages)
    categories, items, parse_log = parse_items(buckets)
    for ln in parse_log:
        log("  " + ln)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_doc": SOURCE_DOC,
        "source_label": SOURCE_LABEL,
        "categories": categories,
        "items": items,
    }
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"wrote {OUT_JSON} ({len(items)} items, {len(categories)} categories)")

    # ---- QA ----
    qa_ok = True
    n_items = len(items)
    n_cats = len(categories)
    if not (300 <= n_items <= 500):
        log(f"QA FAIL: item count {n_items} not in [300, 500]")
        qa_ok = False
    if n_cats != 9:
        log(f"QA FAIL: category count {n_cats} != 9")
        qa_ok = False
    cat_ids = {c["id"] for c in categories}
    if len(cat_ids) != 9:
        log(f"QA FAIL: duplicate or missing category ids ({len(cat_ids)} unique)")
        qa_ok = False
    if qa_ok:
        log("QA OK")
        print("OK")
    else:
        log("QA: issues found (see above)")

    # log sample items per category
    for cat in categories:
        sample = [it for it in items if it["category_id"] == cat["id"]][:3]
        log(f"sample [{cat['id']}] ({len([it for it in items if it['category_id'] == cat['id']])} total):")
        for s in sample:
            log(f"  - {s['english']}  |  {s['chinese']}")

    # append anomalies to issues.md
    append_issues(categories, items, qa_ok)
    return 0 if qa_ok else 1


def append_issues(categories: List[dict], items: List[dict], qa_ok: bool) -> None:
    ISSUES_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append("\n## writing (parse-writing.py)\n")
    lines.append(f"- items: {len(items)} (target 300-500; qa_ok={qa_ok})")
    lines.append(f"- categories: {len(categories)}")
    sparse = [c for c in categories if sum(1 for it in items if it["category_id"] == c["id"]) < 20]
    if sparse:
        lines.append(f"- sparse categories (<20 items): {[c['id'] for c in sparse]}")
    inferred = [c for c in categories if c.get("inferred")]
    if inferred:
        lines.append(f"- inferred topic labels (OCR header missed): {[c['id']+'='+c['label'] for c in inferred]}")
    lines.append(f"- log: .omo/evidence/parse-writing.log")
    with ISSUES_FILE.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())