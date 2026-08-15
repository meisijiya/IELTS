#!/usr/bin/env bash
# verify-stage1b.sh — Stage 1b essay invariant bulk-verify (AC-A2..A9, AC-T1, AC-T2)
#
# Protocol (per *.html under docs/writing/task1/ and docs/writing/task2/):
#   AC-A2  exactly one <h1>
#   AC-A3  exactly one <main>
#   AC-A4  <article data-task=".." data-difficulty=".." data-type=".."> on one line
#   AC-A7  5-10 <code> items inside <section class="keywords">…</section>
#   AC-T1  (task1 only) <img loading="lazy" decoding="async" alt=".."> + <figcaption>
#          + img src PNG exists on disk (width/height optional)
#   AC-T2  (task2 only) data-type ∈ {agree-disagree, discuss-both-views,
#          positive-negative, opinion, two-questions, problem-solution,
#          advantage-disadvantage, single-question}
#   AC-A8/9  word count of <section class="essay"> body: task1 ∈ [170,190],
#          task2 ∈ [270,290]
#
# Usage: verify-stage1b.sh <file-or-dir>...   (exit 0 iff all PASS)
#        verify-stage1b.sh --self-test        (copy corpus essay, inject
#                                              violation, assert non-zero,
#                                              restore, assert zero)

set -u
TASK2_TYPES="agree-disagree discuss-both-views positive-negative opinion two-questions problem-solution advantage-disadvantage single-question"
failures=0

check_file() {
    local f="$1"
    python3 - "$f" "$TASK2_TYPES" <<'PYEOF'
import re, sys, os

f = sys.argv[1]
valid_t2 = sys.argv[2].split()
s = open(f, encoding='utf-8').read()
name = os.path.basename(f)
is_t1 = 'task1' in f
errs = []

# AC-A2 / AC-A3
if len(re.findall(r'<h1>', s)) != 1:
    errs.append('AC-A2: expected exactly 1 <h1>')
if len(re.findall(r'<main>', s)) != 1:
    errs.append('AC-A3: expected exactly 1 <main>')

# AC-A4: article tag with all three data attrs on a single line
art = re.search(r'<article\s+data-task="([a-z0-9-]+)"\s+data-difficulty="([a-z]+)"\s+data-type="([a-z0-9-]+)"\s*>', s)
if not art:
    errs.append('AC-A4: <article data-task data-difficulty data-type> single-line tag missing')
else:
    dtype = art.group(3)

# AC-A7: 5-10 <code> in keywords section
kw = re.search(r'<section class="keywords">(.*?)</section>', s, re.S)
if not kw:
    errs.append('AC-A7: no <section class="keywords">')
else:
    ncode = kw.group(1).count('<code>')
    if not (5 <= ncode <= 10):
        errs.append(f'AC-A7: {ncode} <code> in keywords (need 5-10)')

if is_t1:
    # AC-T1: img with lazy/async/alt + figcaption + PNG exists
    img = re.search(r'<img\s+([^>]*?)src="([^"]+\.png)"([^>]*?)\s*>', s)
    if not img:
        errs.append('AC-T1: <img src="*.png"> missing')
    else:
        attrs = img.group(1) + img.group(3)
        for need in ('loading="lazy"', 'decoding="async"', 'alt="'):
            if need not in attrs:
                errs.append(f'AC-T1: img missing {need}')
        png = os.path.normpath(os.path.join(os.path.dirname(f), img.group(2)))
        if not os.path.exists(png):
            errs.append(f'AC-T1: img src not found on disk: {png}')
    if '<figcaption>' not in s:
        errs.append('AC-T1: <figcaption> missing')
    lo, hi = 170, 190
else:
    if 'task2' not in f:
        errs.append(f'UNKNOWN: file neither under task1/ nor task2/: {f}')
    if art and dtype not in valid_t2:
        errs.append(f'AC-T2: data-type "{dtype}" not in valid set')
    lo, hi = 270, 290

# essay word count
m = re.search(r'<section class="essay">(.*?)</section>', s, re.S)
if not m:
    errs.append('essay: no <section class="essay">')
else:
    wc = len(re.sub(r'<[^>]+>', ' ', m.group(1)).split())
    if not (lo <= wc <= hi):
        errs.append(f'word count {wc} outside [{lo},{hi}]')

if errs:
    print(f'FAIL {name}: ' + '; '.join(errs))
    sys.exit(1)
print(f'PASS {name} (words={wc})')
sys.exit(0)
PYEOF
    local rc=$?
    if [ $rc -ne 0 ]; then failures=1; fi
}

if [ "${1:-}" = "--self-test" ]; then
    tmp=$(mktemp -d)
    mkdir -p "$tmp/docs/writing/task1"
    cp "docs/writing/task1/05-mixed-graph.html" "$tmp/docs/writing/task1/"
    # resolve img src ../../assets/... relative to the temp copy
    mkdir -p "$tmp/docs/assets/images/task1-charts"
    cp "docs/assets/images/task1-charts/05-mixed-graph.png" "$tmp/docs/assets/images/task1-charts/"
    python3 - "$tmp/docs/writing/task1/05-mixed-graph.html" <<'PYEOF'
import re, sys
f = sys.argv[1]
s = open(f, encoding='utf-8').read()
s = re.sub(r'<section class="essay">.*?</section>',
           '<section class="essay"><p>Too short.</p></section>', s, flags=re.S)
open(f, 'w', encoding='utf-8').write(s)
PYEOF
    bash "$0" "$tmp/docs/writing/task1/05-mixed-graph.html" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "FAIL self-test: injected violation did not fail"
        rm -rf "$tmp"; exit 1
    fi
    cp "docs/writing/task1/05-mixed-graph.html" "$tmp/docs/writing/task1/"
    bash "$0" "$tmp/docs/writing/task1/05-mixed-graph.html" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "FAIL self-test: restored file did not pass"
        rm -rf "$tmp"; exit 1
    fi
    rm -rf "$tmp"
    echo "PASS self-test"
    exit 0
fi

if [ $# -eq 0 ]; then
    echo "usage: $0 <file-or-dir>... | --self-test" >&2
    exit 2
fi

for arg in "$@"; do
    if [ -d "$arg" ]; then
        for f in "$arg"/task1/*.html "$arg"/task2/*.html; do
            [ -f "$f" ] && check_file "$f"
        done
    elif [ -f "$arg" ]; then
        check_file "$arg"
    else
        echo "FAIL: not found: $arg"
        failures=1
    fi
done

exit $failures
