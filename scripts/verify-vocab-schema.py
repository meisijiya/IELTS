#!/usr/bin/env python3
"""Verify the 5 vocab JSON files share a consistent core schema. Read-only."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "vocab" / "data"
FILES = ["speaking-p1", "listening", "cambridge", "kaodian538", "writing"]
REQUIRED = ("id", "category_id", "english")
TOP = {"source_doc", "source_label", "categories", "items"}


def has_core(it, source_doc):
    miss = [k for k in REQUIRED if not it.get(k)]
    if "chinese" not in it:
        # kaodian538 synonym entries: no chinese, no rank, no paraphrase
        if source_doc == "kaodian538" and not it.get("rank"):
            pass
        else:
            miss.append("chinese")
    return miss


def validate(name, path, strict, verbose):
    r = {"items": 0, "categories": 0, "optional": set()}
    try:
        d = json.loads(path.read_text())
    except Exception as e:
        return False, {"error": f"json load: {e}"}
    if not TOP.issubset(d):
        return False, {"error": f"missing top-level: {TOP - set(d)}"}
    if strict and (not d.get("source_doc") or not d.get("source_label")):
        return False, {"error": "empty source_doc/source_label"}
    cats, items = d["categories"], d["items"]
    if strict and (not cats or not items):
        return False, {"error": "empty categories/items"}
    r["categories"] = len(cats)
    r["items"] = len(items)
    cat_ids = {c.get("id") for c in cats if isinstance(c, dict)}
    cat_counts = Counter()
    for it in items:
        if not isinstance(it, dict):
            continue
        miss = has_core(it, d.get("source_doc", ""))
        if miss:
            return False, {"error": f"item missing core: {miss}"}
        if it["category_id"] not in cat_ids:
            return False, {"error": f"item {it['id']} bad category_id {it['category_id']!r}"}
        r["optional"].update(set(it) - set(REQUIRED) - {"chinese"})
        cat_counts[it["category_id"]] += 1
    if verbose:
        r["cat_counts"] = dict(cat_counts)
    return True, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    failed, total_i, total_c = False, 0, 0
    for name in FILES:
        path = DATA / f"{name}.json"
        if not path.exists():
            print(f"[FAIL] {name}: missing ({path})"); failed = True; continue
        ok, r = validate(name, path, args.strict, args.verbose)
        opt = ",".join(sorted(r.get("optional", []))) or "-"
        tag = "OK  " if ok else "FAIL"
        line = f"[{tag}] {name}: items={r.get('items', '?')} cats={r.get('categories', '?')} optional=[{opt}]"
        if "error" in r:
            line += f"  ERR={r['error']}"
        print(line)
        if ok:
            total_i += r["items"]; total_c += r["categories"]
            if args.verbose and "cat_counts" in r:
                print(f"  {name}:")
                for cid, n in sorted(r["cat_counts"].items()):
                    print(f"    {cid}: {n}")
        else:
            failed = True
    print(f"TOTAL items={total_i} categories={total_c} files={len(FILES)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())