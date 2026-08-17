#!/usr/bin/env python3
"""extend-index.py — append 237 new Task 2 <article> cards to docs/writing/index.html.

Reads the prompt-bank table `.omo/drafts/prompts-by-section.md` to get the
237 filenames (column 10 after `|` split), parses each essay HTML in
`docs/writing/task2/` for `<article data-task data-difficulty data-type>` and
the `<h1>` text, emits one card per essay, inserts them in ascending filename
order before the closing `</main>` of the essay-list section, AFTER the 55
existing cards. Preserves every byte of existing content.

Usage: python3 extend-index.py  (paths below resolve relative to repo root)
"""
from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
MD_PATH = REPO / ".omo/drafts/prompts-by-section.md"
TASK2_DIR = REPO / "docs/writing/task2"
INDEX_PATH = REPO / "docs/writing/index.html"
LOG_PATH = REPO / ".omo/drafts/extend-index.log"

WHITELIST_CHIPS = {
    "agree-disagree",
    "discuss-both-views",
    "positive-negative",
    "opinion",
    "two-questions",
    "problem-solution",
    "advantage-disadvantage",
    "single-question",
}
WHITELIST_DIFF = {"easy", "medium", "hard"}


def log(msg: str) -> None:
    print(msg)
    LOG_PATH.write_text((LOG_PATH.read_text() if LOG_PATH.exists() else "") + msg + "\n", encoding="utf-8")


def collect_slugs(md_text: str) -> list[str]:
    """Extract 237 Filename-slug values from the markdown table."""
    slugs: list[str] = []
    for line in md_text.splitlines():
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Layout after split: ['', '#', Section, Sub, Sub#, prompt, year, 题型, chip, diff, slug, notes, '']
        if len(cells) < 11 or not cells[1].isdigit():
            continue
        slug = cells[10]
        if slug.endswith(".html"):
            slugs.append(slug)
    return slugs


ARTICLE_RE = re.compile(r"<article\s+([^>]+)>")
ATTR_RE = re.compile(r'data-([a-z]+)="([^"]*)"')
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)


def parse_essay(slug: str) -> tuple[str, str, str]:
    """Parse one essay file; return (difficulty, chip, title)."""
    path = TASK2_DIR / slug
    text = path.read_text(encoding="utf-8")
    article_match = ARTICLE_RE.search(text)
    if not article_match:
        raise ValueError(f"{slug}: no <article> element")
    attrs = dict(ATTR_RE.findall(article_match.group(1)))
    task = attrs.get("task", "")
    diff = attrs.get("difficulty", "")
    chip = attrs.get("type", "")
    if task != "task2":
        raise ValueError(f"{slug}: data-task={task!r} (expected 'task2')")
    if diff not in WHITELIST_DIFF:
        raise ValueError(f"{slug}: data-difficulty={diff!r} not in {WHITELIST_DIFF}")
    if chip not in WHITELIST_CHIPS:
        raise ValueError(f"{slug}: data-type={chip!r} not in whitelist")
    h1_match = H1_RE.search(text)
    if not h1_match:
        raise ValueError(f"{slug}: no <h1>")
    title = h1_match.group(1).strip()
    return diff, chip, title


def card(slug: str, diff: str, chip: str, title: str) -> str:
    safe_title = html.escape(title, quote=False)
    return (
        f'    <article data-task="task2" data-difficulty="{diff}" data-type="{chip}">\n'
        f'      <h3><a href="task2/{slug}">{safe_title}</a></h3>\n'
        f'      <p class="meta">Task 2 · {diff} · {chip}</p>\n'
        f'    </article>'
    )


def main() -> int:
    LOG_PATH.write_text("", encoding="utf-8")
    log(f"extend-index.py started — repo={REPO}")
    log(f"  md: {MD_PATH}")
    log(f"  task2 dir: {TASK2_DIR}")
    log(f"  index: {INDEX_PATH}")

    md_text = MD_PATH.read_text(encoding="utf-8")
    slugs = collect_slugs(md_text)
    log(f"  slugs from md: {len(slugs)}")
    if len(slugs) != 237:
        log(f"ERROR: expected 237 slugs, got {len(slugs)}", )
        return 1

    # Parse each essay, preserving md order; we'll sort by slug at the end.
    parsed: list[tuple[str, str, str, str]] = []
    errors: list[str] = []
    for slug in slugs:
        try:
            diff, chip, title = parse_essay(slug)
        except ValueError as e:
            errors.append(str(e))
            continue
        parsed.append((slug, diff, chip, title))
    log(f"  parsed OK: {len(parsed)}")
    if errors:
        for e in errors:
            log(f"  PARSE ERROR: {e}")
        if len(errors) > 0:
            # spec says no errors; fail loud
            return 2

    # Sort by filename ascending (e.g., 043-... < 044-...)
    parsed.sort(key=lambda r: r[0])
    log(f"  sorted first: {parsed[0][0]}")
    log(f"  sorted last:  {parsed[-1][0]}")

    # Build card block.
    new_cards = "\n".join(card(*p) for p in parsed) + "\n"

    # Read index and insert before </main>. Use one regex split.
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    n_articles_before = index_text.count("<article ")
    log(f"  <article> count before: {n_articles_before}")
    if n_articles_before != 55:
        log(f"ERROR: expected 55 existing articles, got {n_articles_before}")
        return 3

    # Insert directly before the closing </main>. Must be unique.
    marker = "  </main>\n"
    if index_text.count(marker) != 1:
        log("ERROR: could not find exactly one </main> closing marker in expected form")
        return 4
    new_index = index_text.replace(marker, new_cards + marker, 1)

    n_articles_after = new_index.count("<article ")
    log(f"  <article> count after:  {n_articles_after}")
    if n_articles_after != 292:
        log(f"ERROR: expected 292 articles after insertion, got {n_articles_after}")
        return 5

    # Sanity: existing 55 byte-identical. Confirm first 55 article substrings
    # extracted from new_index equal those from old index.
    def article_substrings(s: str) -> list[str]:
        return re.findall(r"<article [^>]+>.*?</article>", s, re.S)

    old_arts = article_substrings(index_text)
    new_arts = article_substrings(new_index)
    for i in range(55):
        if old_arts[i] != new_arts[i]:
            log(f"ERROR: article #{i} modified:\n  old: {old_arts[i][:200]}\n  new: {new_arts[i][:200]}")
            return 6
    log("  first 55 articles: byte-identical ✓")

    INDEX_PATH.write_text(new_index, encoding="utf-8")
    log(f"  wrote {INDEX_PATH} ({len(new_index)} bytes)")
    log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
