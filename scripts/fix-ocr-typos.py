#!/usr/bin/env python3
"""Fix obvious OCR typos in vocab JSON files (english + chinese fields only).

Stdlib only. Run:  python3 scripts/fix-ocr-typos.py [--dry-run]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs/vocab/data"
LOG = ROOT / ".omo/evidence/ocr-typo-fix.log"
FILES = ["listening.json", "writing.json", "kaodian538.json"]

# ---------------------------------------------------------------------------
# English wordlist: hardcoded common words + high-frequency tokens from data
# ---------------------------------------------------------------------------
COMMON = set("""
a about above accept account across act action active activity add address
admit adult advance advantage adventure advice affect afford after afternoon
again against age agency agent agree agreement air airline airport all allow
almost alone along already also although always among amount an and animal
another answer any anyone anything appear apple application apply approach
area argue argument arm army around arrange arrive art article artist as ask
assist assistant assume attack attempt attention attitude attract audience
author authority available average avoid award aware away baby back bad bag
balance ball bank bar base basic basis battle be beach bear beat beautiful
because become bed before begin behavior behind believe benefit best better
between beyond big bill bird birth bit black blood board boat body book
border born borrow both bottle bottom box boy brain branch brand break
breakfast bridge brief bright bring British broad brother budget build
building burn business busy but buy by call camera campaign can cancel
capital car card care career carry case cash catch cause cell centre century
certain chair challenge chance change character charge cheap check chemical
child choice choose church cigarette city civil claim class clean clear
climate climb close club coach cold collect college colour come commercial
committee common communicate community company compare competition complain
complete computer concern condition conference consider contain continue
control conversation cook cool copy corner correct cost could council
country course court cover create crime criminal crisis critical culture
cup current customer cut damage dance danger dark data date daughter day
dead deal death debate decide decision deep degree deliver demand department
depend describe design desk detail develop development die difference
different difficult digital dinner direct direction director discover
discuss discussion disease dish distance distribute district divide doctor
document dog door double down draw dream dress drink drive drop drug during
each early earn earth east easy eat economic economy edge education effect
effort eight either election electric electronic element else employ employee
employer employment end energy engine engineer enjoy enough enter entire
environment environmental equal equipment especially establish even evening
event ever every everybody everyone everything evidence exact exam example
exchange executive exercise exist expect experience expert explain express
eye face fact factor fail fair fall family far farm fast father fear feature
feed feel few field fight figure fill film final financial find fine finger
finish fire firm first fish fit five flight floor focus follow food foot
football for force foreign forest forget form formal former forward four
free freedom fresh friend from front fruit full fund future gain game garden
gas general generation gentle get girl give glass global go goal good
government great green ground group grow growth guarantee guess guest guide
gun hair half hall hand handle hang happen happy hard harm hate have he head
health hear heart heat heavy help her here herself high hill him himself
history hit hold home hope hospital host hot hotel hour house how however
huge human hundred husband idea identify if image imagine impact important
improve in include income increase indeed individual industry influence
information inside instead institution interest international interview into
introduce investment involve issue it item its itself job join joke journey
joy judge jump just keep key kid kill kind king kitchen know knowledge land
language large last late later laugh law lawyer lay lead leader learn least
leave left leg legal less let letter level lie life light like likely limit
link line list listen little live local long look lose loss lot love low
main maintain major majority make man manage management manager many map
market marriage material matter may maybe me meal mean measure media medical
meet meeting member memory mention message method middle might military
million mind mine minister minute miss mission model modern moment money
month more morning most mother move movement movie much music must my myself
name nation national natural nature near nearly necessary need network never
new news next nice night no nobody none nor north not note nothing notice
now number nurse object occur of off offer office officer often oil ok old
on once one only open operation opinion opportunity or order organization
other our ourselves out outside over own owner page pain paint paper parent
park part particular party pass past patient pattern pay peace people per
percent perfect perform perhaps period person personal phone photograph
physical pick picture piece place plan plant play player point police policy
political politics poor popular population position positive possible
postgraduate power practice prepare present president press pressure pretty
prevent price primary print private probably problem process produce product
professor program project promise protect provide public pull purpose push
put quality question quickly quiet quite race radio raise range rate rather
reach read ready real realize really reason receive recent record red reduce
reflect region relate relationship religious remain remember remove report
represent republic require research resource respect respond response rest
result return reveal rich right rise risk road rock role room rule run
safety same save say school science scientific scientist sea season seat
second secret section secure see seek seem select sell send senior sense
series serious serve service set seven several shake share she shoot shop
short should show side sign significant similar simple since sing single
sister sit site situation six size skill skin small smile so social society
software soldier some somebody someone something sometimes son song soon
sort sound source south space speak special specific speech spend sport
spring staff stage stand standard star start state statement station stay
step still stock stop store story straight strategy street strength strike
strong structure student study stuff style subject succeed success such
sudden suffer suggest summer support sure surface system table take talk
task tax teach teacher team technology television tell ten tend term test
than thank that the their them themselves then theory there these they thing
think third this those though thought thousand threat three through throw
thus time to today together too top total touch toward town trade tradition
traffic train travel treat treatment tree trip trouble true trust truth try
turn two type under understand unit university unless until up upon us use
usually value various very victim view village violence visit voice vote
wait walk wall want war warm watch water way we weak wealth wear week
weight welcome well west what whatever when where whether which while white
who whole whom whose why wide wife will win wind window wine wing winner
winter wish with within without woman wonder word work worker world worry
would write writer wrong year yes yesterday yet you young your yourself
""".split())

# Correct words that OCR errors map to (not in the common list above)
EXTRA_WORDS = set("""
abstain aim archaeology arts buildings civilization commercials conditioner
coexist economy education extinction fit foreign gas government highly
horizon illnesses misleading paid point prospect radical realize recycle
relationship restaurant sandwich scenic science select society species
subject theoretical tourism vandalism vegetarian vision yellow year
interview interviewee refund cough recruit bargain boom import export
review display checklist report return studio keep-fit
""".split())
COMMON |= EXTRA_WORDS

# ---------------------------------------------------------------------------
# OCR-confusable letter pairs (a->b means b is the correct letter)
# ---------------------------------------------------------------------------
OCR_PAIRS = {
    ("l", "i"), ("i", "l"), ("l", "c"), ("c", "l"), ("c", "e"), ("e", "c"),
    ("j", "i"), ("i", "j"), ("o", "c"), ("c", "o"), ("m", "n"), ("n", "m"),
    ("t", "f"), ("f", "t"),
}

VOWELS = set("aeiouy")


def clearly_broken(tok):
    """Heuristic: token looks like OCR garbage, not a real word."""
    if not re.search(r"[aeiou]", tok):          # no vowel
        return True
    if re.search(r"[bcdfghjklmnpqrstvwxz]{3,}", tok):  # 3+ consonants in a row
        return True
    if re.search(r"(.)\1", tok):                # any double letter
        return True
    # single 'l' sitting next to a consonant (classic l/i OCR swap)
    for m in re.finditer(r"l", tok):
        i = m.start()
        left = tok[i - 1] if i > 0 else ""
        right = tok[i + 1] if i + 1 < len(tok) else ""
        if (left and left not in VOWELS) or (right and right not in VOWELS):
            return True
    return False


def edit_ops(a, b):
    """Return list of (op, a_char, b_char) for a->b, or None if distance > 2."""
    m, n = len(a), len(b)
    if abs(m - n) > 2:
        return None
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + cost)
    if dp[m][n] > 2:
        return None
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("replace", a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("delete", a[i - 1], ""))
            i -= 1
        else:
            ops.append(("insert", "", b[j - 1]))
            j -= 1
    return ops


def ocr_plausible(ops, tok):
    """All ops must be OCR-plausible; insert/delete needs clearly_broken."""
    broken = clearly_broken(tok)
    for op, a, b in ops:
        if op == "replace":
            if (a, b) not in OCR_PAIRS:
                return False
        else:  # delete / insert
            if not broken:
                return False
    return True


def find_candidate(tok, wordlist):
    """Return the single best OCR-plausible candidate, or None."""
    cands = []
    for w in wordlist:
        if w == tok:
            continue
        ops = edit_ops(tok, w)
        if ops is None:
            continue
        if not ocr_plausible(ops, tok):
            continue
        cands.append((w, ops))
    if not cands:
        return None
    # prefer pure substitutions (no insert/delete)
    min_insdel = min(sum(1 for op, _, _ in ops if op != "replace")
                     for _, ops in cands)
    cands = [c for c in cands
             if sum(1 for op, _, _ in c[1] if op != "replace") == min_insdel]
    # prefer candidate matching the token's plural/singular form
    pm = [c for c in cands if c[0].endswith("s") == tok.endswith("s")]
    if pm:
        cands = pm
    if len(cands) == 1:
        return cands[0][0]
    return None


# ---------------------------------------------------------------------------
# Manual overrides: unambiguous cases the generic algorithm cannot reach
# ---------------------------------------------------------------------------
EN_OVERRIDE = {
    "subjecit": "subject",                    # 科目 (transposition)
    "eimjn": "aim",                           # 目的
    "ri'ta:njn": "return",                    # 归还 (garbled IPA)
    "ri po:t": "report",                      # 报告 (garbled IPA)
    "ri saikoll": "recycle",                  # 回收 (garbled IPA)
    "sandwit": "sandwich",                    # 三明治
    "vcgctarian rcstaurant": "vegetarian restaurant",  # 素食餐厅
    "cjyillzatlon": "civilization",           # 精神文明
    "CO--6Xxlst/coexistence": "coexist/coexistence",  # 共存
    "school ofAns": "school of Arts",         # 文学院
    "eyesight aisait": "eyesight",            # 视力 (aisait = noise)
    "interviewee intorvju:'i": "interviewee",  # 被面试者 (garbled IPA)
    "checklist pek": "checklist",             # 清单 (pek = noise)
    "keep-tit stutio": "keep-fit studio",     # 健身房
    "ges": "gas",                             # 气
    "mljsleading": "misleading",              # example_en: 误导性报道
}

# Items too garbled to repair -> leave untouched, log as skipped
SKIP_IDS = {
    "school-life-97",   # 'Mecthodology DRE. ik ial EH method' garbage
    "environment-28",   # 'perfeat the construation of urban Infraatrue ture' garbage
    "freshman-76",      # 'Xno Mlow' garbage
    "dining-53",        # 'se' -> 让促销，出售 (unclear)
    "dining-69",        # 'fo:ln' -> 毛皮 (unclear)
}

# Broken tokens that appear in the data -> excluded from the wordlist so the
# algorithm flags them (their correct forms are in COMMON/EXTRA_WORDS)
BROKEN = {
    "agalnst", "blrth", "bulldings", "cconomy", "clty", "commerclals",
    "educatlon", "forelgn", "knowlecdge", "reallze", "relatlonshlp",
    "scjentific", "sclect", "sclence", "soclety", "vandallsm", "polnt",
    "radlcal", "extinctlon", "theoretloal", "ycar", "prospeot", "specjes",
    "pald", "govemment", "vislon", "horlzon", "abstaln", "tourlsm", "hlghly",
    "mjsleading", "ycllow", "sccnic", "conditioncr", "archacology",
    "mercilessg", "iiinesses", "mljsleading",
}

# ---------------------------------------------------------------------------
# Chinese: OCR confusion table (char -> correct char) + known target words
# ---------------------------------------------------------------------------
ZH_CONF = {
    "四": "园", "佑": "估", "料": "科", "马": "鸟", "成": "咸", "两": "商",
    "东": "车", "简": "筒", "出": "厕", "笨": "宿", "中": "申", "汗": "汁",
}
ZH_KNOWN = {
    "校园", "评估", "挂科", "候鸟", "咸味", "商店", "停车场", "手电筒",
    "公共厕所", "寄宿学校", "申请表", "苹果汁",
}
ZH_OVERRIDE = {  # stray OCR noise chars to drop
    "六太阳镜": "太阳镜",
    "由六三明治": "三明治",
}

NOISE_TOKEN = re.compile(r"^(?:[nN][aA]|[mM][aA]|[iI][mM])$")
DROP_TOKENS = {"fy"}  # stray OCR noise tokens to drop


def fix_english(en, wordlist):
    if en in EN_OVERRIDE:
        return EN_OVERRIDE[en], True
    parts = re.split(r"([^A-Za-z])", en)
    out, changed = [], False
    for tok in parts:
        if not tok or not tok.isalpha():
            out.append(tok)
            continue
        low = tok.lower()
        if NOISE_TOKEN.match(tok) or low in DROP_TOKENS:  # OCR noise
            changed = True
            continue
        if low in wordlist:
            out.append(tok)
            continue
        cand = find_candidate(low, wordlist)
        if cand:
            out.append(cand.capitalize() if tok[0].isupper() else cand)
            changed = True
        else:
            out.append(tok)
    return "".join(out).strip(), changed


def fix_chinese(zh):
    if zh in ZH_OVERRIDE:
        return ZH_OVERRIDE[zh], True
    for i, ch in enumerate(zh):
        if ch in ZH_CONF:
            cand = zh[:i] + ZH_CONF[ch] + zh[i + 1:]
            if cand in ZH_KNOWN:
                return cand, True
    return zh, False


def main():
    dry = "--dry-run" in sys.argv

    # build wordlist: hardcoded + data tokens (freq>=1) minus known-broken
    freq = Counter()
    for fn in FILES:
        data = json.load(open(DATA / fn, encoding="utf-8"))
        for it in data["items"]:
            for tok in re.findall(r"[A-Za-z]+", it.get("english", "")):
                freq[tok.lower()] += 1
            for tok in re.findall(r"[A-Za-z]+", it.get("example_en", "")):
                freq[tok.lower()] += 1
    wordlist = COMMON | {t for t in freq if t not in BROKEN}

    log_lines = [f"# OCR typo fix run ({'DRY-RUN' if dry else 'APPLIED'})"]
    total = 0
    for fn in FILES:
        path = DATA / fn
        raw = path.read_bytes()
        data = json.loads(raw)
        changed_items = []
        for it in data["items"]:
            iid = it["id"]
            if iid in SKIP_IDS:
                log_lines.append(f"SKIP {fn} {iid}: too garbled to repair")
                continue
            en_new, en_ch = fix_english(it.get("english", ""), wordlist)
            zh_new, zh_ch = fix_chinese(it.get("chinese", ""))
            ex_new, ex_ch = "", False
            if "example_en" in it:
                ex_new, ex_ch = fix_english(it["example_en"], wordlist)
            if en_ch or zh_ch or ex_ch:
                changed_items.append((iid, it.get("english", ""), en_new,
                                      it.get("chinese", ""), zh_new,
                                      it.get("example_en", ""), ex_new))
                it["english"] = en_new
                it["chinese"] = zh_new
                if ex_ch:
                    it["example_en"] = ex_new
        for iid, eo, en, zo, zn, xo, xn in changed_items:
            msg = f"FIX {fn} {iid}: english {eo!r} -> {en!r}"
            if zo != zn:
                msg += f" | chinese {zo!r} -> {zn!r}"
            if xo != xn:
                msg += f" | example_en {xo!r} -> {xn!r}"
            log_lines.append(msg)
        total += len(changed_items)
        if not dry:
            new_raw = json.dumps(data, ensure_ascii=False, indent=2)
            if raw.endswith(b"\n"):
                new_raw += "\n"
            path.write_text(new_raw, encoding="utf-8")
        print(f"{fn}: {len(changed_items)} items changed")

    log_lines.append(f"TOTAL: {total} items corrected")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"log -> {LOG}")
    if dry:
        print("DRY-RUN: no files written")


if __name__ == "__main__":
    main()