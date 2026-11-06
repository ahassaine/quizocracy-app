# dev/app/logic/maths_engine.py
"""Server-authoritative interactive maths engine (framework).

Generators live in the y3_gen_* modules and register themselves with @skill.
A generator returns:
  { "prompt", "component", "spec", "answer", "answer_type", "tolerance", "solution" }
The client renders `component` from `spec`, captures the pupil's value, and posts it
back; the server validates against the stored answer. Answers never reach the client
until the pupil has committed one.

answer_type: num | int | frac | time | coord | str | set
component:   number | number_line | base_ten | array | fraction_bar | clock |
             bar_chart | coordinate_grid
"""
import random
import inspect
import secrets
import datetime
import re
from fractions import Fraction
from ..db import db

# ---------------------------------------------------------------- registry ----
GENERATORS = {}
SKILLS = []

def skill(key, title, strand):
    def deco(fn):
        GENERATORS[key] = fn
        SKILLS.append({"key": key, "title": title, "strand": strand})
        return fn
    return deco

def skill_list():
    return SKILLS

# ----------------------------------------------------------------- helpers ----
_ONES = ["zero","one","two","three","four","five","six","seven","eight","nine","ten",
         "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
         "eighteen","nineteen"]
_TENS = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]

def n_words(n):
    """UK style: 342 -> 'three hundred and forty-two'."""
    n = int(n)
    if n < 20: return _ONES[n]
    if n < 100:
        return _TENS[n//10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    h = _ONES[n//100] + " hundred"
    r = n % 100
    if r == 0: return h
    return h + " and " + (_ONES[r] if r < 20 else _TENS[r//10] + ("" if r % 10 == 0 else "-" + _ONES[r % 10]))

_ROMAN = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX",10:"X",11:"XI",12:"XII"}
def roman(n): return _ROMAN[int(n)]

def money(p):
    """pence -> '£3.45' or '45p'."""
    p = int(p)
    return ("£%d.%02d" % (p // 100, p % 100)) if p >= 100 else ("%dp" % p)

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20: suf = "th"
    else: suf = {1:"st",2:"nd",3:"rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)

def pick(seq): return random.choice(seq)
NAMES = ["Sara","Tom","Amina","Leo","Priya","Zara","Omar","Ella","Noah","Maya"]

# ------------------------------------------------------------ answer check ----
def _num(x):
    try:
        s = str(x).strip().lower().replace(",", "").replace("£", "").replace(" ", "").replace("−", "-").replace("–", "-")
        s = _UNIT.sub("", s)                     # "98m²", "-5°C", "40%", "2 litres": the unit is shown beside the box
        return float(s)
    except Exception:
        return None

_UNIT = re.compile(r"[a-z°%/²³]+(?:\^?[23])?$")   # any unit after the number: "98m²", "-5°c", "40%", "30pupils", "12m/s"


def _frac(x):
    m = re.fullmatch(r"\s*(-?)(\d+)\s+(\d+)\s*/\s*(\d+)\s*", str(x))     # mixed number "2 1/3"
    if m and int(m.group(4)):
        v = int(m.group(2)) + Fraction(int(m.group(3)), int(m.group(4)))
        return -v if m.group(1) else v
    s = str(x).strip().replace(" ", "")
    try:
        if "/" in s:
            n, d = s.split("/"); return Fraction(int(n), int(d))
        return Fraction(s)
    except Exception:
        return None

_SUP = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")


def _sn(s):
    """normalise free text: case, punctuation, UK 'and', hyphens.

    Also makes ALGEBRAIC whitespace insensitive: a pupil who types "6x + 8" must match
    a stored "6x+8". A hyphen between two words ("forty-two", "north-east") counts as a
    space; any other '-' is a minus sign and is kept, so "x>=2" never matches "x>=-2".
    """
    s = str(s).strip().lower().replace("−", "-").replace("–", "-").replace("≤", "<=").replace("≥", ">=").replace("°", "")
    s = re.sub(r"(?<=\d)\s*(am|pm)\b", r" \1", s)                  # 10am = 10 am
    s = re.sub(r"(?<=\d)\s*(?:r|rem|remainder)\s*(?=\d)", " r ", s)  # 25r3 = 25 remainder 3 = 25 r 3
    s = re.sub(r"^(?:a|an|the)\s+(?=[a-z])", "", s)                     # "an elephant" = "elephant"
    s = re.sub(r"[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+", lambda m: "^" + m.group(0).translate(_SUP), s)
    s = re.sub(r"(?<=[\d)])\s*[x×*]\s*(?=[\d(])", "x", s)   # 3.2 × 10^-4 = 3.2x10^-4
    s = s.replace(")x(", ")(")
    s = re.sub(r"(?<=\d)\s+(?=[a-z]\b)", "", s)            # 2 x = 2x
    s = re.sub(r"\b([ap])\.\s*m\b\.?", r"\1m", s)          # a.m. = am, p.m. = pm
    for ch in ".,!?":
        s = s.replace(ch, " ")
    s = re.sub(r"(?<=[a-z])\s*-\s*(?=[a-z])", " ", s)   # word hyphens
    s = " ".join(s.split())
    s = re.sub(r"\s*([-+*/=^<>():])\s*", r"\1", s)  # drop spaces around algebra operators, brackets, ratio colons
    return s

_ORD_WORDS = {w: str(i) for i, w in enumerate(
    "zeroth first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth "
    "fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth".split())}


def check_answer(answer_type, expected, value, tolerance=0, unit=None):
    if value is None or (isinstance(value, str) and not value.strip()):
        return False
    at = answer_type
    if at in ("num", "int"):
        v, e = _num(value), _num(expected)
        if v is None or e is None:
            return False
        if abs(v - e) <= (tolerance or 0) + 1e-9:
            return True
        # an answer asked in pence typed in pounds: "£1.86" for 186p (only where the box says "p")
        return unit == "p" and "£" in str(value) and abs(v * 100 - e) <= (tolerance or 0) + 1e-6
    if at == "frac":
        v, e = _frac(value), _frac(expected)
        return v is not None and e is not None and v == e
    if at == "time":
        def norm(t):
            t = str(t).strip().lower().replace(".", ":").replace(" ", "")
            t = t.replace("am", "").replace("pm", "")
            if re.fullmatch(r"\d{1,2}", t):          # "1 pm", "10am": a whole hour
                t += ":00"
            if ":" not in t: return None
            try:
                hh, mm = t.split(":")[:2]
                return (int(hh) % 12, int(mm))
            except Exception:
                return None
        nv, ne = norm(value), norm(expected)
        return nv is not None and nv == ne
    if at == "coord":
        def norm(c):
            c = str(c).strip().strip("()").replace(" ", "").replace("−", "-")
            try:
                a, b = c.split(","); return (int(a), int(b))
            except Exception:
                return None
        nv, ne = norm(value), norm(expected)
        return nv is not None and nv == ne
    if at == "set":
        # order-insensitive list of numbers, e.g. "90, 92, 94"
        def norm(s):
            parts = [p for p in re.sub(r"\band\b", " ", str(s)).replace(",", " ").split() if p.strip()]
            out = []
            for p in parts:
                n = _num(p)
                if n is None: return None
                out.append(n)
            return sorted(out)
        nv, ne = norm(value), norm(expected)
        return nv is not None and nv == ne
    # a 24-hour time kept as text ("09:45", "13:20"): "9:45", "9.45" and "09 45" count; hours are not mod 12
    m = re.fullmatch(r"\s*(\d{1,2})[:.](\d{2})\s*", str(expected))
    if m:
        v = re.fullmatch(r"\s*(\d{1,2})\s*[:. h]\s*(\d{2})\s*", str(value))
        return bool(v) and (int(v.group(1)), int(v.group(2))) == (int(m.group(1)), int(m.group(2)))
    # a position ("3rd"): "3" and "third" count too
    m = re.fullmatch(r"\s*(\d+)(?:st|nd|rd|th)\s*", str(expected).lower())
    if m:
        v = str(value).strip().lower()
        v = _ORD_WORDS.get(v, re.sub(r"(?<=\d)(?:st|nd|rd|th)$", "", v))
        return v == m.group(1)
    # str — accept UK 'and' being present or absent, and 'seven hundred four'
    sv, se = _sn(value), _sn(expected)
    if sv == se: return True
    return sv.replace(" and ", " ") == se.replace(" and ", " ")

# ----------------------------------------------------------- question store ----
def difficulty_for(score):
    """Mastery score -> difficulty tier. Questions harden as the pupil approaches 100."""
    try:
        score = int(score or 0)
    except Exception:
        score = 0
    if score < 40:
        return 0
    if score < 80:
        return 1
    return 2


def call_generator(fn, difficulty=1):
    """Generators may take a difficulty argument; older zero-arg ones still work."""
    try:
        if len(inspect.signature(fn).parameters) >= 1:
            return fn(difficulty)
    except (TypeError, ValueError):
        pass
    return fn()


def hide_missing_cell(component, spec):
    """Tables mark the cell the pupil must fill with `missing`, but generators leave its true
    value in `rows`. Blank it here so the answer never travels to the browser."""
    m, rows = spec.get("missing"), spec.get("rows")
    if not isinstance(rows, list):
        return spec
    if component == "data_table" and isinstance(m, (list, tuple)) and len(m) == 2:
        r, c = m
    elif component == "io_table" and isinstance(m, int):
        r, c = m, 1
    else:
        return spec
    if not (0 <= r < len(rows) and isinstance(rows[r], (list, tuple)) and 0 <= c < len(rows[r])):
        return spec
    rows = [list(x) if isinstance(x, (list, tuple)) else x for x in rows]
    rows[r][c] = ""
    return {**spec, "rows": rows}


def hide_pie_answer(spec, answer):
    """The pie legend lists every slice's value; when the question asks for the outlined slice's value,
    that slice's value is shown as '?' instead."""
    i, sl = spec.get("highlight"), spec.get("slices")
    if not isinstance(i, int) or not isinstance(sl, list) or not (0 <= i < len(sl)):
        return spec
    try:
        hit = abs(float(sl[i][1]) - float(answer)) < 1e-9
    except (TypeError, ValueError, IndexError):
        return spec
    return {**spec, "hideValue": True} if hit else spec


async def new_question(skill_key, difficulty=1, pupil=None):
    fn = GENERATORS.get(skill_key)
    if not fn:
        return None
    q = call_generator(fn, difficulty)
    # A coordinate_grid whose answer is NOT a coordinate is being used as a drawn
    # stimulus (read the gradient / y-value / intercept). The grid can only PLOT a
    # point, so such a question is unanswerable unless it also shows a typed box —
    # flip it into the grid's typed-stimulus mode automatically.
    if q.get("component") == "coordinate_grid" and q.get("answer_type", "num") != "coord":
        spec = dict(q.get("spec") or {})
        spec["typed"] = True
        q["spec"] = spec
    # The answer is stored in Mongo (BSON), which cannot encode Fraction/Decimal/etc.
    # Coerce anything that is not a plain JSON scalar to str — check_answer re-parses
    # strings for every type, so a stored "9/4" or "0.375" still matches correctly.
    _ans = q.get("answer")
    if not isinstance(_ans, (str, int, float, bool, type(None))):
        q["answer"] = str(_ans)
    q["spec"] = hide_missing_cell(q.get("component"), q.get("spec") or {})
    if q.get("component") == "pie_chart":
        q["spec"] = hide_pie_answer(q["spec"], q.get("answer"))
    if q.get("component") == "angle" and q.get("answer_type", "num") in ("int", "num"):
        q["spec"] = {**q["spec"], "numeric": True}     # a number answer gets a "degrees" box, not "acute / ..."
    token = secrets.token_urlsafe(16)
    await db.maths_lab_q.update_one(
        {"_id": token},
        {"$set": {
            "skill": skill_key,
            "prompt": q["prompt"],
            "answer": q["answer"],
            "answer_type": q.get("answer_type", "num"),
            "tolerance": q.get("tolerance", 0),
            "unit": (q.get("spec") or {}).get("unit"),
            "solution": q.get("solution", []),
            "difficulty": difficulty,
            "pupil": pupil,
            "created": datetime.datetime.utcnow(),
        }},
        upsert=True,
    )
    return {"token": token, "prompt": q["prompt"],
            "component": q.get("component", "number"), "spec": q.get("spec", {})}

async def check(token, value, pupil):
    """One answer per question, and only by the child it was served to."""
    doc = await db.maths_lab_q.find_one_and_update(
        {"_id": str(token or ""), "pupil": pupil, "done": {"$ne": True}}, {"$set": {"done": True}})
    if not doc:
        return {"ok": False, "error": "expired"}
    correct = check_answer(doc["answer_type"], doc["answer"], value, doc.get("tolerance", 0), doc.get("unit"))
    return {"ok": True, "correct": bool(correct),
            "expected": doc["answer"], "solution": doc.get("solution", []),
            "skill": doc.get("skill"), "prompt": doc.get("prompt", "")}

# ------------------------------------------------ register Y3 generators ------
from . import y1_gen_a, y1_gen_b, y2_gen_a, y2_gen_b   # noqa: E402,F401
from . import y3_gen_a, y3_gen_b, y3_gen_c, y3_gen_d, y3_gen_e   # noqa: E402,F401
from . import y4_gen_a, y4_gen_b, y4_gen_c, y4_gen_d, y4_gen_e   # noqa: E402,F401
from . import y5_gen_a, y5_gen_b, y5_gen_c, y5_gen_d, y5_gen_e   # noqa: E402,F401
from . import y6_gen_a, y6_gen_b, y6_gen_c, y6_gen_d, y6_gen_e, y6_gen_f   # noqa: E402,F401
from . import y7_gen_a, y7_gen_b, y7_gen_c, y7_gen_d, y7_gen_e, y7_gen_f, y7_gen_g, y7_gen_h   # noqa: E402,F401
from . import y8_gen_a, y8_gen_b, y8_gen_c, y8_gen_d, y8_gen_e, y8_gen_f   # noqa: E402,F401
from . import y9_gen_a, y9_gen_b, y9_gen_c, y9_gen_d, y9_gen_e, y9_gen_f, y9_gen_g   # noqa: E402,F401
