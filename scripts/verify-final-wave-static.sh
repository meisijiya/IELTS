#!/usr/bin/env bash
# verify-final-wave-static.sh — Final wave STATIC verifiers (F1, F2, F3, F5, F6).
# F4 / F7 / F8 are runtime (jsdom) and covered by a separate script.
# Exit 0 iff all 5 checks PASS.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOG="$ROOT/.omo/evidence/final-wave-static.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "### $(date -u +%FT%TZ) ###"
  echo "Final wave STATIC verification: F1, F2, F3, F5, F6"
  echo ""
} > "$LOG"

emit() { tee -a "$LOG"; }
say()  { echo "$@" | tee -a "$LOG"; }

PASS=0
FAIL=0
FAILED=""

# --- python check helper: id, desc, code; prints result, sets PASS/FAIL ---
pycheck() {
  local id="$1" desc="$2" code="$3" out rc
  out=$(python3 -c "$code" 2>&1) && rc=0 || rc=$?
  if [ "$rc" -eq 0 ]; then
    say "[$id] $desc ... PASS ($out)"
    PASS=$((PASS+1))
  else
    say "[$id] $desc ... FAIL: $out"
    FAIL=$((FAIL+1))
    FAILED="$FAILED $id"
  fi
}

# ---------------- F1: 主页 HTML 结构 ----------------
pycheck F1 "主页 HTML 结构" '
import re, sys
html = open("docs/index.html").read()
cards = re.findall(r"<article class=\"card\">", html)
n = len(cards)
required = {"speaking/", "writing/", "reading/", "listening/", "vocab/"}
hrefs = set(re.findall(r"<article class=\"card\">\s*<a href=\"([^\"]+)\"", html))
errs = []
if n != 5: errs.append(f"cards={n}")
miss = required - hrefs
if miss: errs.append(f"missing {sorted(miss)}")
extra = hrefs - required
if extra: errs.append(f"unexpected {sorted(extra)}")
if "aria-disabled" in html: errs.append("aria-disabled present")
if "Coming soon" in html: errs.append("Coming soon present")
if errs:
    print("; ".join(errs)); sys.exit(1)
print(f"{n} cards, no aria-disabled, no Coming soon")
'

# ---------------- F2: listening/reading 题型清单 ----------------
pycheck F2 "题型清单" '
import sys
rh = open("docs/reading/index.html").read()
rtypes = {i for i in range(1, 12) if f"Type {i}." in rh}

lh = open("docs/listening/index.html").read().lower()
l_checks = [
    ("Multiple choice",          "multiple choice" in lh),
    ("Matching",                 "matching" in lh),
    ("Plan/Map/Diagram labeling",
        ("plan" in lh and "map" in lh and "diagram" in lh and ("labeling" in lh or "labelling" in lh))),
    ("Form/Note/Table/Flow-Chart/Summary completion",
        any(s in lh for s in ["form completion","note completion","table completion","flow-chart","flow chart","summary completion"])),
    ("Sentence completion",      "sentence completion" in lh),
    ("Short-answer",             "short-answer" in lh or "short answer" in lh),
]
l_hits = [name for name, ok in l_checks if ok]
errs = []
if len(rtypes) != 11:
    miss = sorted(set(range(1,12)) - rtypes)
    errs.append(f"reading {len(rtypes)}/11 (missing {miss})")
if len(l_hits) != 6:
    miss = [n for n,o in l_checks if not o]
    errs.append(f"listening {len(l_hits)}/6 (missing {miss})")
if errs:
    print("; ".join(errs)); sys.exit(1)
print(f"reading {len(rtypes)}/11, listening {len(l_hits)}/6")
'

# ---------------- F3: 5 JSON 词条数 ----------------
pycheck F3 "JSON 词条数" '
import json, sys

def J(p): return json.load(open(p))

def chk(name, items, lo, hi, need_eq_cats=None):
    s = f"{name}={items}"
    ok = lo <= items <= hi
    if need_eq_cats is not None:
        cats = J(f"docs/vocab/data/{name}.json").get("categories", [])
        c = len(cats)
        s = f"{s}/{c}"
        ok = ok and c == need_eq_cats
    return s, ok

n_speaking = len(J("docs/vocab/data/speaking-p1.json").get("items", []))

parts = [f"speaking-p1={n_speaking}"]
errs = []
if n_speaking != 64:
    errs.append(f"speaking-p1={n_speaking} (expected 64)")

p, ok = chk("listening",  len(J("docs/vocab/data/listening.json").get("items", [])),  800, 1200)
parts.append(p)
if not ok: errs.append("listening out of [800,1200]")

p, ok = chk("cambridge",  len(J("docs/vocab/data/cambridge.json").get("items", [])),  240, 300, need_eq_cats=65)
parts.append(p)
if not ok: errs.append("cambridge out of [240,300] or categories!=65")

p, ok = chk("kaodian538", len(J("docs/vocab/data/kaodian538.json").get("items", [])), 400, 540)
parts.append(p)
if not ok: errs.append("kaodian538 out of [400,540]")

p, ok = chk("writing",    len(J("docs/vocab/data/writing.json").get("items", [])),    300, 500, need_eq_cats=9)
parts.append(p)
if not ok: errs.append("writing out of [300,500] or categories!=9")

if errs:
    print("FAIL: " + "; ".join(errs)); sys.exit(1)
print(", ".join(parts))
'

# ---------------- F5: 分类筛选每个分类桶 ≥1 条 ----------------
pycheck F5 "分类筛选" '
import json, sys
files = ["speaking-p1","listening","cambridge","kaodian538","writing"]
fails = []
for f in files:
    d = json.load(open(f"docs/vocab/data/{f}.json"))
    cat_ids = {c.get("id") for c in d.get("categories", [])}
    item_cats = {it.get("category_id") for it in d.get("items", [])}
    unused = cat_ids - item_cats
    if unused:
        fails.append(f"{f}:{len(unused)} empty buckets")
if fails:
    print("; ".join(fails)); sys.exit(1)
print("5/5 docs")
'

# ---------------- F6: 静态 HTTP 加载 + node 语法 ----------------
SERVER_PID=""
cleanup() {
  if [ -n "$SERVER_PID" ]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  # Verify no listener remains on 8765
  if command -v ss >/dev/null 2>&1 && ss -tln 2>/dev/null | grep -q ":8765 "; then
    pkill -f "http.server 8765" 2>/dev/null || true
    sleep 0.3
  elif command -v lsof >/dev/null 2>&1 && lsof -i :8765 >/dev/null 2>&1; then
    pkill -f "http.server 8765" 2>/dev/null || true
    sleep 0.3
  fi
}
trap cleanup EXIT

python3 -m http.server 8765 --directory . >/dev/null 2>&1 &
SERVER_PID=$!
sleep 1

f6_ok=1
f6_err=""

is200() { curl -sf -o /dev/null -w "%{http_code}" --max-time 5 "$1" | grep -q "^200$"; }

if ! is200 "http://localhost:8765/docs/vocab/index.html"; then
  f6_err+="html non-200; "; f6_ok=0
fi

JS_BODY=$(curl -sf --max-time 5 "http://localhost:8765/docs/vocab/assets/js/vocab.js" || true)
if [ -z "$JS_BODY" ]; then
  f6_err+="js fetch failed; "; f6_ok=0
else
  if ! printf "%s" "$JS_BODY" | grep -q "VocabApp"; then
    f6_err+="js missing VocabApp; "; f6_ok=0
  fi
  if ! printf "%s" "$JS_BODY" | grep -q "checkSpelling"; then
    f6_err+="js missing checkSpelling; "; f6_ok=0
  fi
fi

if ! is200 "http://localhost:8765/docs/vocab/assets/css/vocab.css"; then
  f6_err+="css non-200; "; f6_ok=0
fi

for jf in speaking-p1 listening cambridge kaodian538 writing; do
  if ! is200 "http://localhost:8765/docs/vocab/data/${jf}.json"; then
    f6_err+="${jf}.json non-200; "; f6_ok=0
  fi
done

if ! command -v node >/dev/null 2>&1; then
  f6_err+="node missing; "; f6_ok=0
elif ! node --check docs/vocab/assets/js/vocab.js >/dev/null 2>&1; then
  f6_err+="node --check failed; "; f6_ok=0
fi

# Cleanup server now (trap will run on EXIT too, but we want it gone before summary)
cleanup
SERVER_PID=""

if [ "$f6_ok" -eq 1 ]; then
  say "[F6] 静态无错 ... PASS (200s + syntax OK)"
  PASS=$((PASS+1))
else
  say "[F6] 静态无错 ... FAIL: $f6_err"
  FAIL=$((FAIL+1))
  FAILED="$FAILED F6"
fi

# ---------------- Summary ----------------
say ""
if [ "$FAIL" -eq 0 ]; then
  say "OVERALL: PASS ($PASS/5)"
  exit 0
else
  say "OVERALL: FAIL ($PASS pass, $FAIL fail:$FAILED)"
  exit 1
fi
