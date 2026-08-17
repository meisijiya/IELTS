#!/usr/bin/env python3
"""Inject <script defer> tags into target HTML files (read-tracker + essay-typing).

Subcommands:
  inject        (default) Inject missing tags before </body>. Idempotent.
  drift-check            Verify every target has its expected tag set.
  undo                   Remove injected tags (best-effort restore).

Targets (365 files):
  docs/writing/task1/*.html     (13)  -> 2 tags (../../assets/js/...)
  docs/writing/task2/*.html    (279)  -> 2 tags (../../assets/js/...)
  docs/speaking/topics/*.html   (71)  -> 1 tag  (../assets/js/...)
  docs/writing/index.html        (1)  -> 1 tag  (../assets/js/...)
  docs/speaking/index.html       (1)  -> 1 tag  (../assets/js/...)

Idempotency: exact substring check on the full <script> tag line.

Exit codes:
  0 success | 1 file r/w error OR missing tag (drift-check) | 2 unreadable (drift-check)
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / ".omo" / "evidence" / "inject-features.log"

RT_W = '<script defer src="../../assets/js/read-tracker.js"></script>'
ET_W = '<script defer src="../../assets/js/essay-typing.js"></script>'
RT_S = '<script defer src="../assets/js/read-tracker.js"></script>'
RT_S2 = '<script defer src="../../assets/js/read-tracker.js"></script>'

UNDO_SUBS = (RT_W, ET_W, RT_S, RT_S2)

DIR_TARGETS: list[tuple[Path, tuple[str, ...]]] = [
    (ROOT / "docs" / "writing" / "task1", (RT_W, ET_W)),
    (ROOT / "docs" / "writing" / "task2", (RT_W, ET_W)),
    (ROOT / "docs" / "speaking" / "topics", (RT_S2,)),
]
FILE_TARGETS: list[tuple[Path, tuple[str, ...]]] = [
    (ROOT / "docs" / "writing" / "index.html", (RT_S,)),
    (ROOT / "docs" / "speaking" / "index.html", (RT_S,)),
]


def _log(msg: str, fh) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    if fh:
        fh.write(line + "\n")
        fh.flush()


def _all_files() -> list[tuple[Path, tuple[str, ...]]]:
    out: list[tuple[Path, tuple[str, ...]]] = []
    for d, tags in DIR_TARGETS:
        if d.is_dir():
            out.extend((p, tags) for p in sorted(d.glob("*.html")))
    out.extend(FILE_TARGETS)
    return out


def _inject(content: str, expected: tuple[str, ...]) -> tuple[str, list[str]]:
    missing = [t for t in expected if t not in content]
    if not missing:
        return content, []
    return content.replace("</body>", "\n".join(missing) + "\n</body>", 1), missing


def _undo(content: str) -> tuple[str, int]:
    kept = []
    removed = 0
    for line in content.split("\n"):
        if any(s in line for s in UNDO_SUBS):
            removed += 1
            continue
        kept.append(line)
    new = "\n".join(kept)
    return re.sub(r"\n{3,}", "\n\n", new), removed


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _write(path: Path, content: str) -> bool:
    try:
        path.write_text(content, encoding="utf-8")
        return True
    except OSError:
        return False


def cmd_inject(log_fh) -> int:
    files = _all_files()
    modified = skipped = errors = 0
    for path, expected in files:
        rel = path.relative_to(ROOT)
        content = _read(path)
        if content is None:
            _log(f"READ ERROR  {rel}", log_fh)
            errors += 1
            continue
        new_content, missing = _inject(content, expected)
        if not missing:
            _log(f"SKIP       {rel}  ({len(expected)} tag(s) present)", log_fh)
            skipped += 1
            continue
        if not _write(path, new_content):
            _log(f"WRITE ERROR {rel}", log_fh)
            errors += 1
            continue
        _log(f"INJECT     {rel}  (+{len(missing)}/{len(expected)} tag(s))", log_fh)
        modified += 1
    _log(f"SUMMARY inject: {modified} modified, {skipped} skipped, {errors} errors, {len(files)} total", log_fh)
    return 1 if errors else 0


def cmd_drift_check(log_fh) -> int:
    files = _all_files()
    missing_files: list[tuple[Path, list[str]]] = []
    error_files: list[tuple[Path, str]] = []
    for path, expected in files:
        rel = path.relative_to(ROOT)
        content = _read(path)
        if content is None:
            error_files.append((path, f"cannot read {rel}"))
            continue
        miss = [t for t in expected if t not in content]
        if miss:
            missing_files.append((path, miss))
    ok = len(files) - len(missing_files) - len(error_files)
    _log(f"DRIFT-CHECK: {ok}/{len(files)} OK, {len(missing_files)} missing, {len(error_files)} unreadable", log_fh)
    for path, miss in missing_files:
        rel = path.relative_to(ROOT)
        _log(f"  MISSING {rel}: {[m[:60] + ('...' if len(m) > 60 else '') for m in miss]}", log_fh)
    for path, err in error_files:
        rel = path.relative_to(ROOT)
        _log(f"  ERROR   {rel}: {err}", log_fh)
    if error_files:
        return 2
    return 1 if missing_files else 0


def cmd_undo(log_fh) -> int:
    files = _all_files()
    modified = unchanged = errors = 0
    for path, _ in files:
        rel = path.relative_to(ROOT)
        content = _read(path)
        if content is None:
            _log(f"READ ERROR  {rel}", log_fh)
            errors += 1
            continue
        new_content, removed = _undo(content)
        if removed == 0:
            unchanged += 1
            continue
        if not _write(path, new_content):
            _log(f"WRITE ERROR {rel}", log_fh)
            errors += 1
            continue
        _log(f"UNDO       {rel}  (-{removed} tag line(s))", log_fh)
        modified += 1
    _log(f"SUMMARY undo: {modified} modified, {unchanged} unchanged, {errors} errors, {len(files)} total", log_fh)
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject read-tracker + essay-typing <script defer> tags into target HTML files.",
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("inject", help="Inject missing tags (idempotent) [default]")
    sub.add_parser("drift-check", help="Verify all expected tags present")
    sub.add_parser("undo", help="Remove injected tags (best-effort)")
    args = parser.parse_args()
    cmd = args.cmd or "inject"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        _log(f"=== {cmd} ===", fh)
        if cmd == "inject":
            return cmd_inject(fh)
        if cmd == "drift-check":
            return cmd_drift_check(fh)
        if cmd == "undo":
            return cmd_undo(fh)
        _log(f"unknown subcommand: {cmd}", fh)
    return 1


if __name__ == "__main__":
    sys.exit(main())