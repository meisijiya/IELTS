#!/usr/bin/env python3
"""Generate 71 speaking topic HTML pages from answers.json + template.html.

Reads:
  - docs/speaking/template.html
  - docs/speaking/data/answers.json

Writes:
  - docs/speaking/topics/<topic-id>.html  (71 files)
  - .omo/evidence/generation.log

Stdlib only. No Jinja2. html.escape() for safety.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "docs" / "speaking" / "template.html"
DATA = ROOT / "docs" / "speaking" / "data" / "answers.json"
OUT_DIR = ROOT / "docs" / "speaking" / "topics"
LOG_PATH = ROOT / ".omo" / "evidence" / "generation.log"

PART_LABEL = {
    "p1-required": "Part 1 必考",
    "p1-high-freq": "Part 1 高频",
    "p23": "Part 2&3",
}
CATEGORY_LABEL = {
    "place": "地点 PLACE", "place-p23": "地点 PLACE",
    "object": "物品 OBJECTS", "object-p23": "物品 OBJECTS",
    "event": "事件 EVENTS", "event-p23": "事件 EVENTS",
    "abstract": "抽象 ABSTRACT",
    "people": "人物 PEOPLE",
}
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")
EMPTY_SENTINEL = "（待补充）"


def _esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_cue_card(topic: dict) -> str:
    cue = topic.get("cue_card")
    if not cue:
        return ""
    bullets_en = cue.get("bullets_en") or []
    bullets_zh = cue.get("bullets_zh") or []
    prompt_en = _esc(cue.get("prompt_en") or topic.get("questions", [{}])[0].get("question_en", ""))
    lines = [f'  <p class="prompt-en">{prompt_en}</p>']
    if bullets_en or bullets_zh:
        lines.append('  <ul class="cue-bullets">')
        for i in range(max(len(bullets_en), len(bullets_zh))):
            en = _esc(bullets_en[i]) if i < len(bullets_en) else ""
            zh = _esc(bullets_zh[i]) if i < len(bullets_zh) else ""
            text = en if en else zh
            if not text:
                continue
            if zh and zh != en:
                lines.append(f'    <li>{text} <span class="bullet-zh">({zh})</span></li>')
            else:
                lines.append(f'    <li>{text}</li>')
        lines.append("  </ul>")
    return "\n".join(lines)


def render_questions(topic: dict, warnings: list[str]) -> str:
    out = []
    for idx, q in enumerate(topic.get("questions") or [], start=1):
        qid = q.get("id", f"q{idx}")
        q_en = _esc(q.get("question_en", ""))
        a_en_raw = (q.get("answer_en") or "").strip()
        hint_zh_raw = (q.get("answer_hint_zh") or "").strip()
        if not a_en_raw:
            warnings.append(f"{topic['id']}/{qid}: empty answer_en -> placeholder")
        if not hint_zh_raw:
            warnings.append(f"{topic['id']}/{qid}: empty answer_hint_zh -> placeholder")
        a_en = _esc(a_en_raw) if a_en_raw else EMPTY_SENTINEL
        hint = _esc(hint_zh_raw) if hint_zh_raw else EMPTY_SENTINEL
        label = "Cue Card" if qid == "cue" else f"Q{idx}"
        out.append(
            f'    <details class="qa-item" open>\n'
            f'      <summary><span class="q-num">{label}</span>'
            f'<span class="q-text">{q_en}</span></summary>\n'
            f'      <div class="answer">\n'
            f'        <p class="answer-en">{a_en}</p>\n'
            f'        <p class="answer-hint">{hint}</p>\n'
            f'      </div>\n'
            f'    </details>'
        )
    return "\n".join(out)


def render_template(template: str, topic: dict, warnings: list[str]) -> str:
    cue_html = render_cue_card(topic)
    q_html = render_questions(topic, warnings)
    has_cue = bool(topic.get("cue_card"))
    part_label = PART_LABEL.get(topic["part"], topic["part"])
    cat_label = CATEGORY_LABEL.get(topic["category"], topic["category"])
    ai_flag = (
        '<span class="ai-flag">AI 补全经历</span>'
        if topic.get("is_ai_supplemented")
        else ""
    )
    values = {
        "topic_id": _esc(topic["id"]),
        "part": _esc(topic["part"]),
        "part_label": _esc(part_label),
        "category_label": _esc(cat_label),
        "title_en": _esc(topic.get("title_en", "")),
        "title_zh": _esc(topic.get("title_zh", "")),
        "ai_flag": ai_flag,
        "cue_card_html": cue_html,
        "questions_html": q_html,
    }

    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            warnings.append(f"{topic['id']}: unknown placeholder {{{{{key}}}}}")
            return match.group(0)
        return values[key]

    rendered = PLACEHOLDER_RE.sub(repl, template)
    if has_cue:
        rendered = rendered.replace(
            '<section class="cue-card">\n        <h2>Part 2 话题卡片</h2>',
            '<section class="cue-card">\n        <h2>Part 2 话题卡片</h2>',
        )
    else:
        rendered = re.sub(
            r'<section class="cue-card">.*?</section>',
            "",
            rendered,
            count=1,
            flags=re.DOTALL,
        )
    return rendered


def main() -> int:
    started = datetime.now(timezone.utc)
    log_lines: list[str] = [
        f"=== generate-speaking-pages.py run at {started.isoformat(timespec='seconds')} ==="
    ]

    if not TEMPLATE.exists():
        print(f"ERROR: template missing: {TEMPLATE}", file=sys.stderr)
        return 1
    if not DATA.exists():
        print(f"ERROR: data missing: {DATA}", file=sys.stderr)
        return 1

    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    topics = payload.get("topics") or []

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_warnings: list[str] = []
    written = 0
    for topic in topics:
        tid = topic.get("id")
        if not tid:
            all_warnings.append("topic missing id -> skipped")
            continue
        topic_warnings: list[str] = []
        body = render_template(template, topic, topic_warnings)
        header = (
            f"<!-- Generated by generate-speaking-pages.py at "
            f"{started.isoformat(timespec='seconds')} -->\n"
        )
        out_path = OUT_DIR / f"{tid}.html"
        out_path.write_text(header + body, encoding="utf-8")
        written += 1
        all_warnings.extend(topic_warnings)

    finished = datetime.now(timezone.utc)
    elapsed = (finished - started).total_seconds()
    log_lines.extend([
        f"topics_in_json: {len(topics)}",
        f"files_written:  {written}",
        f"elapsed_sec:    {elapsed:.3f}",
        f"warnings:       {len(all_warnings)}",
    ])
    if all_warnings:
        log_lines.append("--- warnings ---")
        log_lines.extend(all_warnings)
    log_lines.append("=== done ===")
    LOG_PATH.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"generated {written} topic pages in {OUT_DIR}")
    print(f"warnings: {len(all_warnings)}  (full list in {LOG_PATH})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
