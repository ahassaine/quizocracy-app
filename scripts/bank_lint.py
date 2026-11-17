"""Check the question banks (grammar, science, phonics, reading) against app/bank/SPEC*.md.

    python scripts/bank_lint.py                 # every file in app/bank/content
    python scripts/bank_lint.py grammar_y3      # one file (module name)
    python scripts/bank_lint.py --no-ids reading_y3   # while writing, before scripts/bank_ids.py gives ids

Prints one line per problem and a summary per file; exits 1 if anything is wrong.
"""
import importlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TYPES = {"mcq", "tap", "text", "write", "num", "seg", "order"}
KEY_RE = re.compile(r"^(GP|SC|PH|RD)([1-9])\.(\d{2})$")
BANNED = re.compile(r"\b(all|none) of (the )?(above|these)\b|\b(god|gods|goddess|magic|magical|wizard|witch|ghost|zombie|vampire|fairy|fairies|"
                    r"dragon|dragons|unicorn|monster|monsters|demon|devil|angel|angels|heaven|hell|spirit|spirits|myth|myths|"
                    r"legend|legends|church|mosque|temple|prayer|pray|christmas|easter|diwali|halloween|hanukkah|wine|beer|"
                    r"alcohol|pork|bacon|ham|sausage|gambling|casino|lottery|boyfriend|girlfriend|kiss|kissed|curse)\b", re.I)
BANNED_GP_SC = re.compile(r"\b(all|none) of (the )?(above|these)\b|\b(god|gods|magic|wizard|witch|ghost|zombie|vampire)\b", re.I)
AMERICAN = re.compile(r"\b(color|colors|favorite|center|(?<!light )(?<!parking )meter|meters|liter|liters|gray|mom|math|neighbor|behavior|"
                      r"flavor|harbor|honor|vapor|odor|fiber|aluminum|sulfur dioxide)\b")
ID_RE = re.compile(r"^[0-9a-f]{12}$")
MIN_QS, MIN_TYPES = 20, 3
DOMAINS = {"vocab", "retrieve", "sequence", "summarise", "infer", "predict", "structure", "language", "compare", "purpose"}
KS1_DOMAINS = {"vocab", "retrieve", "sequence", "infer", "predict"}
KINDS = {"Stories", "Information", "Instructions", "Poems", "Letters and diaries", "Biography", "News reports",
         "Persuasive writing", "Play scripts", "Explanations"}
# words per passage and questions per passage, by year (SPEC_READING.md)
READ_WORDS = {1: (30, 80), 2: (80, 160), 3: (150, 250), 4: (200, 300), 5: (250, 380), 6: (300, 450), 7: (350, 550),
              8: (350, 550), 9: (350, 550)}
READ_QS = {1: 4, 2: 5, 3: 6, 4: 6, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7}
SPEC_PH = ROOT / "app/bank/SPEC_PHONICS.md"
EMOJI = {}
if SPEC_PH.exists():
    _sec = SPEC_PH.read_text().split("## EMOJI", 1)[-1].split("##", 1)[0]
    for _pair in _sec.split("\n", 2)[-1].split("\n\n")[0].split(" · "):
        _e, _, _w = _pair.strip().partition(" ")
        if _e and _w:
            EMOJI[_e] = _w
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u231A-\u23FF\u2190-\u21FF]")


def norm(s):
    return " ".join(str(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').split())


def tap_tokens(s):
    """Words of a tap sentence and the indices of the bracketed ones; None if the brackets are malformed."""
    words, hits = [], []
    for i, tok in enumerate(s.split()):
        n = tok.count("[")
        if n != tok.count("]") or n > 1:
            return None
        if n:
            m = re.fullmatch(r"([^\[\]]*)\[([^\[\]]+)\]([^\[\]]*)", tok)
            if not m or not re.search(r"\w", m.group(2)) or re.search(r"\w", m.group(1) + m.group(3)):
                return None
            hits.append(i)
            tok = m.group(1) + m.group(2) + m.group(3)
        words.append(tok)
    return words, hits


def check_q(q, where, out, kind="GP", sk=None):
    """kind: the key prefix (GP, SC, PH, RD); sk: the skill (a reading passage's text is checked against)."""
    t = q.get("t")
    banned = BANNED if kind in ("PH", "RD") else BANNED_GP_SC
    if t not in TYPES:
        return out.append(f"{where}: unknown type {t!r}")
    for f in ("q", "why"):
        if not isinstance(q.get(f), str) or len(q[f].strip()) < 3:
            out.append(f"{where}: missing {f}")
    if not NO_IDS and (not isinstance(q.get("id"), str) or not ID_RE.match(q["id"])):
        out.append(f"{where}: missing or malformed id (run scripts/bank_ids.py)")
    extra = set(q) - {"id", "t", "q", "why", "why2", "no", "opts", "s", "a", "tol", "unit"} \
        - ({"w", "say"} if kind == "PH" else {"d", "items"} if kind == "RD" else set())
    if extra:
        out.append(f"{where}: unknown fields {sorted(extra)}")
    if "why2" in q and (not isinstance(q["why2"], str) or len(q["why2"].strip()) < 3 or norm(q["why2"]) == norm(q.get("why", ""))):
        out.append(f"{where}: why2 must be a different explanation")
    if "no" in q:
        no = q["no"]
        wrong = {norm(x) for x in (q.get("opts") or [])[1:]}
        right = {norm(x) for x in (q.get("a") if isinstance(q.get("a"), list) else [])}
        if t not in ("mcq", "text") or not isinstance(no, dict) or not no:
            out.append(f"{where}: 'no' is a dict of wrong mcq options (or typed text answers) and why each is wrong")
        else:
            for o, line in no.items():
                if t == "mcq" and norm(o) not in wrong:
                    out.append(f"{where}: 'no' names {o!r}, which is not a wrong option")
                if t == "text" and norm(o) in right:
                    out.append(f"{where}: 'no' names {o!r}, which is an accepted answer")
                if not isinstance(line, str) or len(line.strip()) < 3:
                    out.append(f"{where}: 'no' line for {o!r} is empty")
    text = " ".join(str(q.get(k, "")) for k in ("q", "s", "why", "why2")) + " " + " ".join(map(str, q.get("opts", [])))
    text += " " + " ".join(map(str, (q.get("no") or {}).values())) if isinstance(q.get("no"), dict) else ""
    text += " " + " ".join(str(q.get(k, "")) for k in ("w", "say")) + " " + " ".join(map(str, q.get("items", [])))
    if banned.search(text):
        out.append(f"{where}: banned wording ({banned.search(text).group(0)})")
    if kind == "RD":
        check_reading_q(q, where, out, sk or {})
    if kind == "PH":
        check_phonics_q(q, where, out)
    if kind in ("PH", "RD") and t in ("write", "num"):
        out.append(f"{where}: {t} is not used in this bank")
    if kind not in ("PH", "RD") and t in ("seg", "order"):
        out.append(f"{where}: {t} is only used in phonics and reading")
    if AMERICAN.search(text):
        out.append(f"{where}: American spelling ({AMERICAN.search(text).group(0)})")
    if re.search(r"\b(diagram|picture|graph|image|table) (below|above|shows)\b|\blook at the (diagram|picture|graph)\b", text, re.I):
        out.append(f"{where}: refers to a picture that is not there")
    if t == "mcq":
        o = q.get("opts")
        if not isinstance(o, list) or not 2 <= len(o) <= 4 or not all(isinstance(x, str) and x.strip() for x in o):
            return out.append(f"{where}: mcq needs 2-4 non-empty options")
        if len({norm(x).lower() for x in o}) != len(o):
            out.append(f"{where}: mcq options repeat")
        if len(o) >= 3 and len(o[0]) > 1.6 * max(len(x) for x in o[1:]) and len(o[0]) > 25:
            out.append(f"{where}: right option much longer than the others (leak)")
    elif t == "tap":
        r = tap_tokens(q.get("s", ""))
        if r is None or not r[1]:
            return out.append(f"{where}: tap sentence needs [word] brackets around whole words")
        words, hits = r
        targets = [re.sub(r"^\W+|\W+$", "", words[i]).lower() for i in hits]
        for w in targets:
            if sum(1 for x in words if re.sub(r"^\W+|\W+$", "", x).lower() == w) > 1:
                out.append(f"{where}: tap target {w!r} appears more than once")
        if len(hits) > 1 and not re.search(r"\b(two|three|four|five|all|each|every|both)\b|\b(the|all) \w+s\b", q["q"], re.I):
            out.append(f"{where}: several targets but the question does not say how many")
    elif t in ("text", "write"):
        a = q.get("a")
        if not isinstance(a, list) or not a or not all(isinstance(x, str) and x.strip() for x in a):
            return out.append(f"{where}: {t} needs a list of accepted answers")
        if t == "text" and len(a[0].split()) > 4:                 # the shown answer; other accepted forms may be longer
            out.append(f"{where}: text answers should be 1-4 words")
        if t == "write":
            if not q.get("s"):
                out.append(f"{where}: write needs the sentence to fix in s")
            elif norm(q["s"]) in {norm(x) for x in a}:
                out.append(f"{where}: the sentence to fix is already an accepted answer")
    elif t == "seg":
        w, a = q.get("w"), q.get("a")
        if not isinstance(w, str) or not isinstance(a, str) or "|" not in a:
            return out.append(f"{where}: seg needs w (the word) and a (the word split with |)")
        parts = a.split("|")
        if "".join(parts) != w or any(not p for p in parts):
            out.append(f"{where}: seg answer {a!r} does not spell {w!r}")
        if not re.fullmatch(r"[a-z]+", w):
            out.append(f"{where}: seg word must be lower-case letters only")
    elif t == "order":
        it = q.get("items")
        if not isinstance(it, list) or not 3 <= len(it) <= 5 or not all(isinstance(x, str) and x.strip() for x in it):
            return out.append(f"{where}: order needs 3-5 items, in the right order")
        if len({norm(x).lower() for x in it}) != len(it):
            out.append(f"{where}: order items repeat")
    elif t == "num":
        if not isinstance(q.get("a"), (int, float)) or isinstance(q.get("a"), bool):
            out.append(f"{where}: num needs a numeric answer")
        if "tol" in q and (not isinstance(q["tol"], (int, float)) or q["tol"] < 0):
            out.append(f"{where}: bad tol")


def _plain(s):
    return re.sub(r"\s+", " ", norm(s)).strip()


def check_reading_q(q, where, out, sk):
    t, year = q.get("t"), sk.get("year") or 0
    d = q.get("d")
    if d not in DOMAINS:
        out.append(f"{where}: reading question needs d, one of {sorted(DOMAINS)}")
    elif year <= 2 and d not in KS1_DOMAINS:
        out.append(f"{where}: d={d!r} is not a Year 1-2 domain")
    if t == "tap" and isinstance(q.get("s"), str):
        bare = _plain(q["s"].replace("[", "").replace("]", ""))
        if bare not in _plain(sk.get("text", "")):
            out.append(f"{where}: tap sentence is not copied exactly from the passage")
    if t == "text" and year <= 1:
        out.append(f"{where}: no typed answers in Year 1")
    if t == "mcq" and isinstance(q.get("opts"), list):
        want = 3 if year <= 2 else 4
        if len(q["opts"]) != want:
            out.append(f"{where}: Year {year} mcq needs {want} options")


def check_phonics_q(q, where, out):
    t = q.get("t")
    if "w" in q and "say" in q:
        out.append(f"{where}: a question has w or say, not both")
    for f in ("w", "say"):
        if f in q and (not isinstance(q[f], str) or not q[f].strip()):
            out.append(f"{where}: empty {f}")
    say = q.get("say")
    if isinstance(say, str) and say.strip():
        if not re.fullmatch(r"[a-z]+", say):
            out.append(f"{where}: say must be one lower-case word")
        if re.search(r"\b%s\b" % re.escape(say), q.get("q", ""), re.I):
            out.append(f"{where}: the spoken word {say!r} is written in q")
    w = q.get("w")
    if isinstance(w, str) and re.search(r"\b%s\b" % re.escape(w), q.get("q", ""), re.I):
        out.append(f"{where}: the word to read {w!r} is also in q")
    for x in [q.get("q", "")] + list(q.get("opts") or []):
        for e in EMOJI_RE.findall(str(x)):
            if e not in "".join(EMOJI) and EMOJI:
                out.append(f"{where}: emoji {e!r} is not in the SPEC_PHONICS list")
    opts = q.get("opts") or []
    if t == "mcq" and opts and all(EMOJI_RE.search(str(o)) for o in opts):
        names = [EMOJI.get(str(o).strip()) for o in opts]
        if None in names:
            out.append(f"{where}: picture options must each be one emoji from the list")
        elif len(set(names)) != len(names):
            out.append(f"{where}: two pictures mean the same word")
        elif isinstance(w, str) and names[0] != w:
            out.append(f"{where}: the right picture means {names[0]!r}, not the word {w!r}")


def check_module(name, seen_keys, seen_ids=None):
    out = []
    seen_ids = {} if seen_ids is None else seen_ids
    try:
        mod = importlib.import_module(f"app.bank.content.{name}")
    except Exception as e:  # noqa: BLE001 - report anything that stops the file loading
        return [f"{name}: does not import: {e!r}"], 0, 0
    skills = getattr(mod, "SKILLS", None)
    if not isinstance(skills, list) or not skills:
        return [f"{name}: no SKILLS list"], 0, 0
    nq = 0
    for s in skills:
        k = s.get("key", "?")
        m = KEY_RE.match(str(k))
        if not m:
            out.append(f"{k}: bad key")
        elif int(m.group(2)) != s.get("year"):
            out.append(f"{k}: key year does not match year {s.get('year')}")
        if k in seen_keys:
            out.append(f"{k}: duplicate key (also in {seen_keys[k]})")
        seen_keys[k] = name
        for f in ("strand", "title", "nc"):
            if not isinstance(s.get(f), str) or not s[f].strip():
                out.append(f"{k}: missing {f}")
        kind = m.group(1) if m else "GP"
        if kind == "RD":
            check_passage(s, k, out)
        if "after" in s and s["after"] not in {x.get("key") for x in skills if x is not s}:
            out.append(f"{k}: 'after' names {s['after']!r}, not a skill of this file")
        qs = s.get("qs") or []
        nq += len(qs)
        if kind == "RD":
            want = READ_QS.get(s.get("year"), 6)
            if not want <= len(qs) <= want + 1:
                out.append(f"{k}: {len(qs)} questions (Year {s.get('year')} passages have {want})")
        else:
            if len(qs) < MIN_QS:
                out.append(f"{k}: only {len(qs)} questions (min {MIN_QS})")
            if len({q.get("t") for q in qs}) < MIN_TYPES:
                out.append(f"{k}: fewer than {MIN_TYPES} question types")
        prompts = {}
        for i, q in enumerate(qs):
            check_q(q, f"{k}#{i}", out, kind, s)
            if q.get("id") in seen_ids:                 # ids are unique across the whole bank, not only the skill
                out.append(f"{k}#{i}: duplicate id {q['id']} (also {seen_ids[q['id']]})")
            elif q.get("id"):
                seen_ids[q["id"]] = f"{k}#{i}"
            sig = norm(q.get("q", "") + "|" + q.get("s", "") + "|" + "|".join(sorted(map(str, q.get("opts", [])))))
            if sig in prompts:
                out.append(f"{k}#{i}: same question as #{prompts[sig]}")
            prompts[sig] = i
    return out, len(skills), nq


def check_passage(s, k, out):
    text, year = s.get("text"), s.get("year")
    if s.get("strand") not in KINDS:
        out.append(f"{k}: strand must be one of {sorted(KINDS)}")
    if not isinstance(text, str) or not text.strip():
        return out.append(f"{k}: missing text")
    n = len(re.findall(r"[A-Za-z0-9'’-]+", text))
    lo, hi = READ_WORDS.get(year, (0, 10 ** 6))
    if not lo <= n <= hi * 1.1:
        out.append(f"{k}: {n} words (Year {year}: {lo}-{hi})")
    if BANNED.search(text + " " + s.get("title", "")):
        out.append(f"{k}: banned wording in the passage ({BANNED.search(text + ' ' + s.get('title', '')).group(0)})")
    if AMERICAN.search(text):
        out.append(f"{k}: American spelling in the passage ({AMERICAN.search(text).group(0)})")
    if re.search(r"^#|\*\*", text, re.M):
        out.append(f"{k}: no markdown in the passage")


NO_IDS = False


def main(argv):
    global NO_IDS
    NO_IDS = "--no-ids" in argv          # while writing: ids are added at the end by scripts/bank_ids.py
    argv = [a for a in argv if a != "--no-ids"]
    names = argv or sorted(p.stem for p in (ROOT / "app/bank/content").glob("*.py") if p.stem != "__init__")
    seen, ids, bad, tot_s, tot_q = {}, {}, 0, 0, 0
    for n in names:
        probs, ns, nq = check_module(n, seen, ids)
        tot_s += ns; tot_q += nq
        for p in probs:
            print(p)
        bad += len(probs)
        print(f"== {n}: {ns} skills, {nq} questions, {len(probs)} problems")
    print(f"TOTAL {tot_s} skills, {tot_q} questions, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
