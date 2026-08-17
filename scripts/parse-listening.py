#!/usr/bin/env python3
"""Parse `听力高频词汇.pdf` (45 pages, image-only) into `docs/vocab/data/listening.json`.

Source layout per category block (e.g. ``1. Accommodation 食宿篇``):
    N. <English Name> <Chinese Label>           <- category header
    <intro paragraph in Chinese>                 <- skipped
    <sub-section header in Chinese>             <- skipped
    > word [ipa] n. 中文                          <- primary word entry
    ※ TIPS line(s)                                <- attached to previous word
    sub-word 中文                                  <- sub-item, no IPA, no >
    ※ TIPS line(s)                                <- attached to previous word
    > word [...] ...

Plan reference: ``.omo/plans/five-modules-expansion.md`` §lines 133–185, 167–170
(11 expected categories, ~1015 items, items carry optional ipa + tips).
"""
from __future__ import annotations

import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pypdfium2 as pdfium
import pytesseract

# ---- paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SOURCE_PDF = ROOT / "听力高频词汇.pdf"
OUT_JSON = ROOT / "docs" / "vocab" / "data" / "listening.json"
LOG_FILE = ROOT / ".omo" / "evidence" / "parse-listening.log"
CACHE_FILE = ROOT / ".omo" / "cache" / "listening-ocr.txt"
ISSUES_FILE = ROOT / ".omo" / "notepads" / "five-modules-expansion" / "issues.md"

SOURCE_DOC = "listening"
SOURCE_LABEL = "听力高频词汇"

# ---- expected categories ---------------------------------------------------
EXPECTED_CATEGORIES: list[tuple[int, str, str]] = [
    (1, "accommodation",      "食宿篇"),
    (2, "travelling",         "休闲旅行"),
    (3, "banking",            "银行交易"),
    (4, "freshman",           "新生入学"),
    (5, "school-life",        "学校生活"),
    (6, "library",            "图书馆场景"),
    (7, "medical",            "医疗场景"),
    (8, "interview",          "面试就职"),
    (9, "dining",             "休闲娱乐"),
    (10, "science",           "科普类场景"),
    (11, "society-economy",   "社会经济类场景"),
]

# ---- regex & helpers -------------------------------------------------------
LATIN_RE = re.compile(r"[A-Za-z]")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")

# Category header: number + . or space + (English|Chinese) + space + (Chinese)
RE_CATEGORY = re.compile(
    r"^\s*(\d{1,2})\s*[\.\s、,]+\s*"
    r"([A-Za-z\u4e00-\u9fff][\w\u4e00-\u9fff\s&\-]+?)\s*$"
)

# TIPS markers — these prefixes (or their OCR-mangled variants) denote a note
RE_TIPS_PREFIX = re.compile(r"^[※KXT*]\s*[\u4e00-\u9fff]|^TIPS\s*[:：]")

# Sub-section header inside a category: short Chinese-only line, 2-10 chars
RE_SUBSECTION = re.compile(r"^[\u4e00-\u9fff\s]{2,10}$")

# POS tags OCR'd adjacent to words (`house n`, `en-suite n/adj`, `subject n`)
RE_TRAILING_POS = re.compile(
    r"\s+(?:n|v|adj|adv|vt|vi|prep|conj|art|pron|num|int|aux)"
    r"(?:\s*/\s*(?:n|v|adj|adv|vt|vi|prep|conj|art|pron|num|int|aux))*"
    r"\.?[,，、；;]?\s*$",
    re.IGNORECASE,
)
RE_RESIDUAL_IPA = re.compile(r"[\[\]]|\b[a-zA-Z]+\s*[\]\[]")
RE_LEADING_GARBAGE = re.compile(r"^[a-zA-ZxyIXAa]\s+(?=[A-Za-z])")
RE_BAD_ENGLISH = re.compile(r"[()\[\]<>|]|,\s*,|\(\s*\)|^\s*[.,;]|^\s*'")


def _strip_trailing_pos(eng: str) -> str:
    prev = None
    while prev != eng:
        prev = eng
        eng = RE_TRAILING_POS.sub("", eng).rstrip(" ,.;。:，．、；;")
    eng = re.sub(
        r"\s+(?:n|v|m|adj|adv|vt|vi|prep|conj|pron|num|int|aux)"
        r"(?:[./,，][^a-zA-Z\s]*[a-zA-Z]+)*\s*$",
        "",
        eng,
        flags=re.IGNORECASE,
    ).rstrip(" ,.;。:，．、；;")
    eng = re.sub(r"\s*[|/][a-z]+\s*$", "", eng, flags=re.IGNORECASE)
    eng = re.sub(r"[a-z]+\|\s*$", "", eng, flags=re.IGNORECASE)
    eng = re.sub(r"\s+[a-z]{1,3}$", "", eng).rstrip(" ,.;。:，．、；;")
    return eng


def setup_tesseract() -> str:
    """Return path to a working tesseract binary.

    Tries PATH; falls back to the portable install at /tmp/tess-full; raises
    FileNotFoundError with a clear message if neither works.
    """
    system_tess = shutil.which("tesseract")
    if system_tess:
        env = os.environ.copy()
        for v in ("LD_LIBRARY_PATH", "TESSDATA_PREFIX"):
            env.pop(v, None)
        try:
            r = subprocess.run(
                [system_tess, "--list-langs"],
                capture_output=True, text=True, env=env, timeout=10,
            )
            if "eng" in r.stdout and "chi_sim" in r.stdout:
                return system_tess
        except Exception:
            pass

    portable = Path("/tmp/tess-full/usr/bin/tesseract")
    if portable.exists():
        os.environ["LD_LIBRARY_PATH"] = (
            "/tmp/tess-full/usr/lib/x86_64-linux-gnu:"
            + os.environ.get("LD_LIBRARY_PATH", "")
        )
        os.environ["TESSDATA_PREFIX"] = (
            "/tmp/tess-full/usr/share/tesseract-ocr/5/tessdata/"
        )
        return str(portable)

    raise FileNotFoundError(
        "tesseract binary not found in PATH and no portable install at "
        "/tmp/tess-full/usr/bin/tesseract."
    )


def _ocr_config() -> str:
    if os.environ.get("TESSDATA_PREFIX"):
        return f"--tessdata-dir {os.environ['TESSDATA_PREFIX']} --oem 1 --psm 6"
    return "--oem 1 --psm 6"


# ---- OCR -------------------------------------------------------------------
def ocr_page(pdf_doc, page_idx: int) -> str:
    page = pdf_doc[page_idx]
    pil_image = page.render(scale=100 / 72).to_pil()
    return pytesseract.image_to_string(
        pil_image, lang="eng+chi_sim", config=_ocr_config()
    )


def ocr_all_pages(pdf_path: Path) -> list[tuple[int, str, str]]:
    """Return list of (page_num, text, mode). Uses cache when available."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if CACHE_FILE.exists() and CACHE_FILE.stat().st_mtime >= pdf_path.stat().st_mtime:
        raw = CACHE_FILE.read_text(encoding="utf-8")
        chunks = re.split(r"\n={5}PAGE (\d+)={5}\n", raw)
        pages: list[tuple[int, str, str]] = []
        i = 1
        while i < len(chunks):
            page_num = int(chunks[i])
            text = chunks[i + 1]
            pages.append((page_num, text, "cached"))
            i += 2
        return pages

    setup_tesseract()
    pdf_doc = pdfium.PdfDocument(str(pdf_path))
    n_pages = len(pdf_doc)
    pages = []
    mode_lines: list[str] = []
    t0 = time.time()
    for pidx in range(n_pages):
        text = ocr_page(pdf_doc, pidx)
        pages.append((pidx + 1, text, "ocr"))
        mode_lines.append(f"P{pidx+1}: ocr {len(text)}c {time.time()-t0:.1f}s")
    CACHE_FILE.write_text(
        "".join(f"\n=====PAGE {n}=====\n{t}" for n, t, _ in pages),
        encoding="utf-8",
    )
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        for line in mode_lines:
            f.write(line + "\n")
    return pages


# ---- english/chinese splitter ----------------------------------------------
def split_tokens(line: str) -> tuple[str, str]:
    """Split a token-stream line into (english, chinese).

    The transition happens at the first token containing CJK characters.
    """
    s = re.sub(r"^[>\s•●]+", "", line)
    tokens = s.split()
    eng_tokens: list[str] = []
    chi_tokens: list[str] = []
    state = "eng"
    for tok in tokens:
        has_lat = bool(LATIN_RE.search(tok))
        has_chi = bool(CHINESE_RE.search(tok))
        if state == "eng":
            if has_lat and not has_chi:
                eng_tokens.append(tok)
            elif has_chi:
                chi_tokens.append(tok)
                state = "chi"
            else:
                continue
        else:
            chi_tokens.append(tok)
    eng = " ".join(eng_tokens).strip()
    chi = "".join(chi_tokens).strip()  # OCR injects spaces between CJK chars
    return eng, chi


def find_ipa(line: str) -> tuple[str | None, str]:
    """Extract IPA from a line, return (ipa_or_None, line_without_ipa)."""
    m = re.search(r"\[([^\]\n]{1,40})\]", line)
    if m:
        ipa = m.group(1).strip().strip("'").strip()
        return ipa, line.replace(m.group(0), " ", 1)
    return None, line


def clean_english(eng: str) -> str:
    eng = re.sub(r"\s+", " ", eng).strip()
    eng = RE_RESIDUAL_IPA.sub(" ", eng)
    eng = re.sub(r"\s+", " ", eng).strip()
    eng = _strip_trailing_pos(eng)
    eng = RE_LEADING_GARBAGE.sub("", eng)
    eng = re.sub(r"\s+", " ", eng).strip()
    return eng


def clean_chinese(chi: str) -> str:
    """Strip whitespace, punctuation noise; collapse spaces between CJK chars."""
    chi = re.sub(r"\s+", "", chi)
    chi = chi.strip(" ,.;。;:、，．()（）[]【】<>《》")
    return chi


def parse_word_entry(line: str) -> tuple[str, str | None, str] | None:
    """Extract (english, ipa_or_None, chinese) from a word line, or None."""
    if len(line) > 100 or not line.strip():
        return None
    if not LATIN_RE.search(line) or not CHINESE_RE.search(line):
        return None

    ipa, stripped = find_ipa(line)
    eng, chi = split_tokens(stripped)
    eng = clean_english(eng)
    chi = clean_chinese(chi)

    if not eng or not chi:
        return None
    if len(eng) < 2 or len(eng) > 60:
        return None
    if len(chi) < 1 or len(chi) > 25:
        return None
    if not re.search(r"[A-Za-z]{2,}", eng):
        return None
    if CHINESE_RE.search(eng):
        return None
    if re.search(r"[A-Za-z]", chi):
        return None
    if re.search(r"[A-Za-z][./][A-Za-z]", chi):
        return None
    if RE_BAD_ENGLISH.search(eng):
        return None
    if re.match(r"^[A-Z]{2,}\s+", eng) or re.match(r"^[A-Z]{3,}$", eng):
        if eng in ("CV", "DVD", "TV", "ATM", "GPS"):
            pass
        else:
            return None
    # filter image-OCR noise: multi-token english with single-char chinese
    if len(chi) <= 1 and len(eng.split()) >= 2 and len(eng) > 12:
        return None
    # filter all-caps multi-word english (OCR text from embedded images)
    if re.match(r"^[A-Z][A-Z\-]+\s+[A-Z]", eng) or re.match(r"^[A-Z]{4,}\s+[A-Z]{4,}", eng):
        return None
    # filter chinese that's just 一 (OCR lost real chars; misleading entry)
    if chi == "一":
        return None

    return eng, ipa, chi


# ---- main parser -----------------------------------------------------------
def parse_pages(
    pages: list[tuple[int, str, str]],
) -> tuple[list[dict], list[dict], list[str], list[str]]:
    categories: list[dict] = []
    items: list[dict] = []
    log: list[str] = []
    anomalies: list[str] = []

    current_cat_id: str | None = None
    seen_categories: set[int] = set()
    tip_buffer: list[str] = []
    sub_counter: dict[str, int] = {}

    cat_label_for_num = {n: lbl for n, _, lbl in EXPECTED_CATEGORIES}
    cat_id_for_num = {n: cid for n, cid, _ in EXPECTED_CATEGORIES}

    log.append(f"pages: {len(pages)}")

    for page_num, text, mode in pages:
        log.append(f"--- page {page_num} (mode={mode}, {len(text)} chars) ---")
        lines = text.split("\n")

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            # ---- category header ----
            m = RE_CATEGORY.match(line)
            if m:
                num = int(m.group(1))
                rest = m.group(2).strip()
                if 1 <= num <= 11 and num not in seen_categories:
                    has_latin = bool(LATIN_RE.search(rest))
                    has_chinese = bool(CHINESE_RE.search(rest))
                    if has_chinese and (has_latin or len(rest) <= 12):
                        current_cat_id = cat_id_for_num[num]
                        current_cat_label = cat_label_for_num[num]
                        seen_categories.add(num)
                        if not any(c["id"] == current_cat_id for c in categories):
                            categories.append(
                                {"id": current_cat_id, "label": current_cat_label}
                            )
                        log.append(
                            f"  P{page_num}: cat#{num} -> {current_cat_id} "
                            f"({current_cat_label}) | {line[:60]!r}"
                        )
                        tip_buffer = []
                        sub_counter[current_cat_id] = 0
                        continue
                    else:
                        anomalies.append(
                            f"P{page_num}: rejected fake cat header {line[:60]!r}"
                        )

            # ---- if no category yet, skip ----
            if current_cat_id is None:
                continue

            # ---- TIPS marker ----
            if RE_TIPS_PREFIX.match(line):
                tip_buffer.append(line)
                continue

            # ---- sub-section header (short Chinese only) ----
            if RE_SUBSECTION.match(line) and not LATIN_RE.search(line):
                continue

            # ---- word entry ----
            parsed = parse_word_entry(line)
            if parsed is None:
                if (
                    len(line) > 15
                    and CHINESE_RE.search(line)
                    and "[" not in line
                    and items
                    and items[-1]["category_id"] == current_cat_id
                ):
                    tip_buffer.append(line)
                continue

            eng, ipa, chi = parsed
            sub_counter[current_cat_id] = sub_counter.get(current_cat_id, 0) + 1
            idx = sub_counter[current_cat_id]
            item = {
                "id": f"{current_cat_id}-{idx}",
                "category_id": current_cat_id,
                "english": eng,
                "chinese": chi,
            }
            if ipa:
                item["ipa"] = ipa
            if tip_buffer:
                joined = " ".join(tip_buffer)
                joined = re.sub(r"\s+", " ", joined).strip()
                joined = re.sub(r"^[※KXT*]+\s*", "", joined)
                if joined and len(joined) <= 500:
                    item["tips"] = joined
                tip_buffer = []
            items.append(item)
            log.append(
                f"  item {len(items):04d} [{current_cat_id}#{idx}] "
                f"{eng!r:30s} -> {chi!r:20s}"
                + (f" | ipa={ipa!r}" if ipa else "")
            )

    expected_nums = set(n for n, _, _ in EXPECTED_CATEGORIES)
    missing = expected_nums - seen_categories
    if missing:
        anomalies.append(
            f"missing categories: {sorted(missing)} -> "
            f"{[cat_id_for_num[n] for n in sorted(missing)]}"
        )
    log.append(f"categories detected: {sorted(seen_categories)}")
    log.append(f"items extracted: {len(items)}")
    log.append(f"anomalies: {len(anomalies)}")

    return categories, items, log, anomalies


# ---- main ------------------------------------------------------------------
def main() -> int:
    if not SOURCE_PDF.exists():
        print(f"FATAL: source PDF not found: {SOURCE_PDF}", file=sys.stderr)
        return 1

    try:
        tess_cmd = setup_tesseract()
    except FileNotFoundError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    print(f"tesseract: {tess_cmd}")

    pages = ocr_all_pages(SOURCE_PDF)
    print(f"OCR done: {len(pages)} pages")

    categories, items, log_lines, anomalies = parse_pages(pages)

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
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"source: {SOURCE_PDF}\n")
        for ln in log_lines:
            f.write(ln + "\n")
        f.write("\n--- summary ---\n")
        f.write(
            f"categories: {len(categories)} (ids="
            f"{','.join(c['id'] for c in categories)})\n"
        )
        f.write(f"items: {len(items)}\n")
        if anomalies:
            f.write("\n--- anomalies ---\n")
            for a in anomalies:
                f.write(a + "\n")
        if items:
            f.write("\n--- 5 random sample items ---\n")
            for s in random.sample(items, min(5, len(items))):
                f.write(
                    f"  [{s['id']}] eng={s['english']!r} chi={s['chinese']!r}"
                    + (f" ipa={s['ipa']!r}" if 'ipa' in s else "")
                    + (f" tips={s.get('tips','')[:80]!r}" if 'tips' in s else "")
                    + "\n"
                )

    if anomalies:
        ISSUES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ISSUES_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n## parse-listening.py ({time.strftime('%Y-%m-%d')})\n\n")
            for a in anomalies:
                f.write(f"- {a}\n")

    summary = (
        f"wrote {OUT_JSON} | categories={len(categories)} items={len(items)} "
        f"anomalies={len(anomalies)}"
    )
    print(summary)
    return 0 if (800 <= len(items) <= 1200 and len(categories) == 11) else 2


if __name__ == "__main__":
    sys.exit(main())