"""Check the grammar and science question banks against app/bank/SPEC.md.

    python scripts/bank_lint.py                 # every file in app/bank/content
    python scripts/bank_lint.py grammar_y3      # one file (module name)

Prints one line per problem and a summary per file; exits 1 if anything is wrong.
"""
import importlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TYPES = {"mcq", "tap", "text", "write", "num"}
KEY_RE = re.compile(r"^(GP|SC)([1-9])\.(\d{2})$")
BANNED = re.compile(r"\b(all|none) of (the )?(above|these)\b|\b(god|gods|magic|wizard|witch|ghost|zombie|vampire)\b", re.I)
AMERICAN = re.compile(r"\b(color|colors|favorite|center|(?<!light )(?<!parking )meter|meters|liter|liters|gray|mom|math|neighbor|behavior|"
                      r"flavor|harbor|honor|vapor|odor|fiber|aluminum|sulfur dioxide)\b")
ID_RE = re.compile(r"^[0-9a-f]{12}$")
MIN_QS, MIN_TYPES = 20, 3


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


def check_q(q, where, out):
    t = q.get("t")
    if t not in TYPES:
        return out.append(f"{where}: unknown type {t!r}")
    for f in ("q", "why"):
        if not isinstance(q.get(f), str) or len(q[f].strip()) < 3:
            out.append(f"{where}: missing {f}")
    if not isinstance(q.get("id"), str) or not ID_RE.match(q["id"]):
        out.append(f"{where}: missing or malformed id (run scripts/bank_ids.py)")
    extra = set(q) - {"id", "t", "q", "why", "why2", "no", "opts", "s", "a", "tol", "unit"}
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
    if BANNED.search(text):
        out.append(f"{where}: banned wording ({BANNED.search(text).group(0)})")
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
    elif t == "num":
        if not isinstance(q.get("a"), (int, float)) or isinstance(q.get("a"), bool):
            out.append(f"{where}: num needs a numeric answer")
        if "tol" in q and (not isinstance(q["tol"], (int, float)) or q["tol"] < 0):
            out.append(f"{where}: bad tol")


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
        if "after" in s and s["after"] not in {x.get("key") for x in skills if x is not s}:
            out.append(f"{k}: 'after' names {s['after']!r}, not a skill of this file")
        qs = s.get("qs") or []
        nq += len(qs)
        if len(qs) < MIN_QS:
            out.append(f"{k}: only {len(qs)} questions (min {MIN_QS})")
        if len({q.get("t") for q in qs}) < MIN_TYPES:
            out.append(f"{k}: only one question type")
        prompts = {}
        for i, q in enumerate(qs):
            check_q(q, f"{k}#{i}", out)
            if q.get("id") in seen_ids:                 # ids are unique across the whole bank, not only the skill
                out.append(f"{k}#{i}: duplicate id {q['id']} (also {seen_ids[q['id']]})")
            elif q.get("id"):
                seen_ids[q["id"]] = f"{k}#{i}"
            sig = norm(q.get("q", "") + "|" + q.get("s", "") + "|" + "|".join(sorted(map(str, q.get("opts", [])))))
            if sig in prompts:
                out.append(f"{k}#{i}: same question as #{prompts[sig]}")
            prompts[sig] = i
    return out, len(skills), nq


def main(argv):
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
