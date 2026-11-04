"""Generate many questions per skill and flag text and data slips: "1 apples", "a 8", "an cube",
leftover %d / {}, None/nan in text, doubled words, unbalanced brackets, non-JSON diagram data,
integer answers that are not whole.

    python3 scripts/maths_lint.py [Y5 ...] [--n 200]
"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e

N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 200
only = [a for a in sys.argv[1:] if a.startswith("Y")]

SINGULAR_OK = ("ss", "us", "is", "ics", "ous", "news", "series", "species", "lens", "gas", "has", "was", "its",
               "this", "plus", "minus", "times", "less", "always", "yes", "pass", "class", "glass", "dress", "cross",
               "bus", "chess", "grass", "access", "process", "address", "boss", "loss", "moss", "kiss", "miss",
               "bonus", "focus", "virus", "census", "corpus", "radius", "cactus", "campus", "circus", "octopus",
               "walrus", "hippopotamus", "rhinoceros", "canvas", "atlas", "iris", "basis", "axis", "chassis",
               "appears", "measures", "means", "equals", "remains", "goes", "makes", "gets", "leaves",
               "needs", "buys", "gives", "works", "includes", "satisfies", "stands", "rounds", "costs", "weighs",
               "holds", "takes", "lies", "represents", "shows", "fails", "comes", "changes")
A_AN_OK = re.compile(r"\ba (one|once|unit|uni|eu|use|usu|uk\b|u-|ewe|ufo|ur[aio])", re.I)
CHECKS = [
    ("format code left", re.compile(r"%[sdfr]|\{\}|\{[a-z_]+\}")),
    ("None/nan in text", re.compile(r"\bNone\b(?! (of|are|is|was|were|have|has)\b)|\b(nan|NaN|inf)\b")),
    ("doubled word", re.compile(r"\b(?!(one|two|three|four|five|six|seven|eight|nine|zero)\b)([a-z]{2,}) \2\b", re.I)),   # "point six six" is fine
    ("a before vowel sound", re.compile(r"(?<![\w'])a (?=[aeiou]\w)(?!(is|and|or|in|as|equals)\b)")),
    ("an before consonant", re.compile(r"(?<![\w'])an (?=[bcdfgjklmnpqrstvwxyz])(?![a-z][-\s])(?!h(our|onest|onour|eir))")),
    ("a before 8/11/18/80s", re.compile(r"\ba (8|11|18|8\d|8\d\d|8,\d{3}|11,\d{3}|18,\d{3})\b")),
    ("an before other number", re.compile(r"\ban (?!(8|11|18)\b|8\d|8,|11,|18,)\d")),
    ("negative zero", re.compile(r"(?<![\d.])-0(?![.\d])")),
    ("space before full stop or comma", re.compile(r"[A-Za-z] [.,](\s|$)")),
]
PLURAL_ONE = re.compile(r"(?<![\d.,/−£$€-])\b1 ([a-z]+)\b")


def texts(q):
    yield "prompt", str(q.get("prompt") or "")
    for s in q.get("solution") or []:
        yield "solution", str(s)
    sp = q.get("spec") or {}
    for k in ("choices", "options"):
        for c in sp.get(k) or []:
            yield "choice", str(c)


def lint(q):
    out = []
    for where, t in texts(q):
        for name, rx in CHECKS:
            m = rx.search(t)
            if m and not (name == "a before vowel sound" and A_AN_OK.search(t[m.start():m.start() + 8])):
                out.append("%s in %s: …%s…" % (name, where, t[max(0, m.start() - 25):m.end() + 25]))
        for m in PLURAL_ONE.finditer(t):
            w = m.group(1)
            if re.search(r"[A-Z][a-z]* $", t[:m.start()]):          # a label: "Rectangle 1 measures"
                continue
            if w.endswith("s") and not w.endswith(SINGULAR_OK) and len(w) > 3:
                out.append("'1 %s' in %s: …%s…" % (w, where, t[max(0, m.start() - 25):m.end() + 25]))
        if where == "prompt" and t.count("(") != t.count(")"):
            out.append("unbalanced brackets in prompt: %s" % t[:90])
    try:
        json.dumps(q.get("spec") or {}, allow_nan=False)
    except (TypeError, ValueError) as ex:
        out.append("spec is not plain JSON: %s" % ex)
    a = q.get("answer")
    if q.get("answer_type") == "int" and not re.fullmatch(r"-?\d+", str(a).replace(",", "")):
        out.append("int answer %r is not a whole number" % a)
    return out


found = collections.defaultdict(collections.Counter)
for s in e.SKILLS:
    if only and not s["key"].startswith(tuple(o + "." for o in only)):
        continue
    for d in (0, 1, 2):
        for _ in range(N):
            for msg in lint(e.call_generator(e.GENERATORS[s["key"]], d)):
                found[s["key"]][msg] += 1
for key in found:
    print(key)
    for msg, n in found[key].most_common(6):
        print("   %4d× %s" % (n, msg))
print("\n%d skills flagged" % len(found))
