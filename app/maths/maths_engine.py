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
import math
from fractions import Fraction
from ..db import db
from ..drills import typos

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
        s = str(x).strip().lower().replace(",", "").replace(" ", "").replace("−", "-").replace("–", "-")
        s = re.sub(r"[£$€]", "", s)              # "£148.50", "$218.96", "5€"
        s = _UNIT.sub("", s)                     # "98m²", "-5°C", "40%", "2 litres": the unit is shown beside the box
        return float(s)
    except Exception:
        return None

_UNIT = re.compile(r"[a-z°%/²³]+(?:\^?[23])?$")   # any unit after the number: "98m²", "-5°c", "40%", "30pupils", "12m/s"


def _std_form(x):
    """'3x10^5', '3 × 10⁵', '3*10^5' -> 300000.0 (a number typed in standard form)."""
    s = re.sub(r"[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+", lambda m: "^" + m.group(0).translate(_SUP), str(x))
    s = s.lower().replace(" ", "").replace(",", "").replace("−", "-")
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)[x×*]10\^\(?(-?\d+)\)?", s)
    return float(m.group(1)) * 10 ** int(m.group(2)) if m else None


_VULGAR = {"½": "1/2", "⅓": "1/3", "⅔": "2/3", "¼": "1/4", "¾": "3/4", "⅕": "1/5", "⅖": "2/5", "⅗": "3/5",
           "⅘": "4/5", "⅙": "1/6", "⅚": "5/6", "⅛": "1/8", "⅜": "3/8", "⅝": "5/8", "⅞": "7/8"}


def _frac_text(x):
    """A fraction as typed, tidied: '−1/2' -> '-1/2', '2½' -> '2 1/2', '2 1/2 pizzas' -> '2 1/2'."""
    s = str(x).strip().replace("−", "-").replace("–", "-").replace("⁄", "/")
    s = re.sub("[%s]" % "".join(_VULGAR), lambda m: " " + _VULGAR[m.group(0)], s).strip()
    s = re.sub(r"(?<=\d)\s+[a-zA-Z][a-zA-Z ]*$", "", s)     # a unit word after the number
    return " ".join(s.split())


def _frac(x):
    s = _frac_text(x)
    m = re.fullmatch(r"(-?)(\d+)\s+(\d+)\s*/\s*(\d+)", s)     # mixed number "2 1/3"
    if m and int(m.group(4)):
        v = int(m.group(2)) + Fraction(int(m.group(3)), int(m.group(4)))
        return -v if m.group(1) else v
    s = s.replace(" ", "")
    try:
        if "/" in s:
            n, d = s.split("/"); return Fraction(int(n), int(d))
        return Fraction(s)
    except Exception:
        return None


def _frac_shape(x):
    """How a fraction answer is written: ('whole', n) | ('mixed', w, r, d) | ('simple', n, d) | ('decimal',)."""
    s = _frac_text(x).lstrip("-")
    m = re.fullmatch(r"(\d+)", s)
    if m:
        return ("whole", int(m.group(1)))
    m = re.fullmatch(r"(\d+)\s+(\d+)\s*/\s*(\d+)", s)
    if m:
        return ("mixed",) + tuple(int(g) for g in m.groups())
    m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", s)
    if m:
        return ("simple", int(m.group(1)), int(m.group(2)))
    return ("decimal",)


def _lowest(sh):
    """Is the written fraction in its simplest form? (a whole number is)"""
    if sh[0] == "whole":
        return True
    if sh[0] == "mixed":
        return 0 < sh[2] < sh[3] and math.gcd(sh[2], sh[3]) == 1
    if sh[0] == "simple":
        return sh[2] > 1 and math.gcd(sh[1], sh[2]) == 1
    return False


# What a fraction question asks for. Each rule applies only when the stored answer is itself in that form.
_SIMPLEST = re.compile(r"simplest|lowest terms|simplif", re.I)
_AS_MIXED = re.compile(r"(?:\bas a|\(|\bgive (?:it|your answer|the answer) as a)\s*mixed number(?! or)", re.I)
_AS_IMPROPER = re.compile(r"\bas an improper fraction", re.I)
_A_FRACTION = re.compile(r"fraction|mixed number", re.I)
_DECIMAL_OK = re.compile(r"\bor (?:a |as a )?decimal|\bdecimal or\b", re.I)


def _frac_form(expected, value, prompt):
    """'' when the fraction is written the way the question asks, otherwise a hint for the child.
    The value is already known to be right."""
    p = str(prompt or "")
    vs, es = _frac_shape(value), _frac_shape(expected)
    if vs[0] == "decimal" and _A_FRACTION.search(p) and not _DECIMAL_OK.search(p):
        return "Right value — now write it as a fraction."       # "Write 0.04 as a fraction": 0.04 is a copy
    if es[0] == "mixed" and vs[0] not in ("mixed", "whole") and _AS_MIXED.search(p):
        return "Right value — now write it as a mixed number."
    if es[0] == "simple" and vs[0] != "simple" and _AS_IMPROPER.search(p):
        return "Right value — now write it as an improper fraction."
    if _SIMPLEST.search(p) and _lowest(es) and not _lowest(vs):
        return "Right value — now simplify it."
    return ""


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


_DEC_ASKED = re.compile(r"decimal|d\.\s?p\b|\bround|significant|s\.f\b|nearest", re.I)


def _drop_var(value, prompt):
    """'x = -13' -> '-13' when x is a letter of the question ("Solve 8x = -104", "What is y?")."""
    m = re.fullmatch(r"\s*([a-zA-Z])\s*=\s*(.+)", str(value))
    if not m or (prompt and not re.search(r"(?<![a-zA-Z])%s(?![a-zA-Z])" % m.group(1), str(prompt))):
        return value
    return m.group(2)


# Units a typed answer is checked against: (kind, size in the smallest unit). Others ("°", "pupils") pass.
_SIZES = {}
for _kind, _rows in (
        ("length", [(1, "mm millimetre millimetres millimeter millimeters"), (10, "cm centimetre centimetres centimeter centimeters"),
                    (1000, "m metre metres meter meters"), (10 ** 6, "km kilometre kilometres kilometer kilometers")]),
        ("mass", [(1, "g gram grams gramme grammes"), (1000, "kg kilogram kilograms kilo kilos"),
                  (10 ** 6, "tonne tonnes")]),
        ("capacity", [(1, "ml millilitre millilitres milliliter milliliters cm³ cm^3"), (10, "cl centilitre centilitres"),
                      (1000, "l litre litres liter liters"), (10 ** 6, "m³ m^3")]),
        ("area", [(1, "mm² mm^2"), (100, "cm² cm^2"), (10 ** 6, "m² m^2"), (10 ** 12, "km² km^2")]),
        ("time", [(1, "s sec secs second seconds"), (60, "min mins minute minutes"), (3600, "h hr hrs hour hours"),
                  (86400, "day days"), (604800, "week weeks")]),
        ("money", [(1, "p pence penny"), (100, "£ pound pounds")])):
    for _size, _names in _rows:
        _SIZES.update({n: (_kind, _size) for n in _names.split()})
_ASKED_UNIT = re.compile(r"\b(?:in|into|how many|how much|number of)\s+(%s)(?![\w²³^])"
                         % "|".join(sorted((re.escape(n) for n in _SIZES if n != "£"), key=len, reverse=True)), re.I)


def _typed_unit(value):
    """The unit a child typed after (or "£" before) the number: "8000 kg" -> ('mass', 1000); None if none or unknown."""
    s = str(value).strip().lower()
    if re.match(r"^-?\s*£", s) or re.match(r"^-?[\d.,\s]+£$", s):
        return _SIZES["£"]
    m = re.fullmatch(r"[-−+]?\s*[£$€]?\s*[\d.,\s]*\d\s*([^\d\s].*?)\.?", s)
    return _SIZES.get(m.group(1).strip()) if m else None


def _wanted_units(unit, prompt):
    """The units the answer may be in: the box's unit and any unit the question asks for ("in millimetres")."""
    out = [_SIZES[str(unit).strip().lower()]] if unit and str(unit).strip().lower() in _SIZES else []
    return out + [_SIZES[m.lower()] for m in _ASKED_UNIT.findall(str(prompt or ""))]


def _a_number(value, prompt):
    """A typed number: plain, with a unit or currency, in standard form, or as a fraction ("3/20" for 0.15)
    unless the question asks for a decimal."""
    s = _drop_var(value, prompt)
    if re.search(r"\d\s*/\s*\d", str(s)):            # a fraction, never "6" with a unit "/7"
        f = None if _DEC_ASKED.search(str(prompt or "")) else _frac(s)
        return float(f) if f is not None else None
    v = _num(s)
    return _std_form(s) if v is None else v


def _clock(t):
    """'3:45', '15.45', '3:45 pm', '10am', '7.30 p.m.' -> (h, m, 'am' | 'pm' | None)."""
    t = str(t).strip().lower().replace(" ", "")
    ap = re.search(r"([ap])\.?m\.?$", t)
    if ap:
        t = t[:ap.start()]
    t = t.replace(".", ":")
    if re.fullmatch(r"\d{1,2}", t):          # "1 pm", "10am": a whole hour
        t += ":00"
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", t)
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        return None
    return int(m.group(1)), int(m.group(2)), ap and ap.group(1) + "m"


_H12 = re.compile(r"12-hour|12 hour", re.I)
_H24 = re.compile(r"24-hour|24 hour", re.I)
_DURATION = re.compile(r"hours and minutes", re.I)


def _same_time(expected, value, prompt):
    """Times of day. A 24-hour answer (13:15, 08:20) needs the 24-hour hour; a question that converts TO the
    12-hour clock refuses the 24-hour time copied back and checks a.m./p.m. when typed; on a clock face
    3:45 and 15:45 are the same; a duration (h:mm hours and minutes) is exact."""
    v, e = _clock(value), _clock(expected)
    if not v or not e or v[1] != e[1]:
        return False
    (vh, _, ap), (eh, em, _) = v, e
    p = str(prompt or "")
    if ap:
        if not 1 <= vh <= 12:
            return False
        vh = vh % 12 + (12 if ap == "pm" else 0)
    if _DURATION.search(p):
        return not ap and vh == eh
    if eh >= 13 or eh == 0 or str(expected).strip().startswith("0"):
        if ap and _H24.search(p):            # "Write it as a 24-hour time": 3:45 pm is not that form
            return False
        return vh == eh
    if _H12.search(p):
        if not ap and (vh >= 13 or vh == 0):  # "Write 13:15 as a 12-hour time": 13:15 is the question
            return False
        if ap:                               # the 24-hour time in the question says which half of the day
            src = [int(h) for h, mm in re.findall(r"\b(\d{1,2}):(\d{2})\b", p)
                   if int(mm) == em and int(h) % 12 == eh % 12]
            if len(set(src)) == 1:
                return vh == src[0]
    return vh % 12 == eh % 12


_ORD_FIGURES = re.compile(r"in figures|(?:like|e\.g\.)\s+\d+(?:st|nd|rd|th)\b", re.I)


def _same_set(expected, value):
    """Order-insensitive list of numbers: "90, 92, 94", "2, 3, 5 and 7", "6,184,930, 7,518,249" (a comma
    between digit groups belongs to the number) or "6184930; 7518249"."""
    def norm(s, groups):
        s = str(s)
        if groups:
            s = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s)
        parts = [p for p in re.sub(r"\band\b|[;,]", " ", s).split() if p.strip()]
        out = []
        for p in parts:
            n = _num(p)
            if n is None:
                return None
            out.append(n)
        return sorted(out)
    ne = norm(expected, True)
    return ne is not None and ne in (norm(value, True), norm(value, False))


def check_answer(answer_type, expected, value, tolerance=0, unit=None, prompt=""):
    """Is the pupil's value right? `prompt` (the question) decides the form where the form is the skill:
    "as a decimal", "in its simplest form", "as a 12-hour time", "in figures, e.g. 4th"."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return False
    at = answer_type
    if at in ("num", "int"):
        v, e = _a_number(value, prompt), _num(expected)
        if v is None and not _IN_DIGITS.search(str(prompt or "")):
            v = _WORD_NUM.get(str(value).strip().lower())        # "two" for 2, unless the task is writing it in digits
        if v is None or e is None:
            return False
        near = lambda a, b: abs(a - b) <= (tolerance or 0) + 1e-9 * max(abs(b), 1e-6)   # noqa: E731 float noise only
        typed, want = _typed_unit(_drop_var(value, prompt)), _wanted_units(unit, prompt)
        same = [w for w in want if typed and w[0] == typed[0]]
        if same and all(w[1] != typed[1] for w in same):
            # a unit of the same kind but another size: "8000 kg" for grams, "£38" for 38p, "40 m" for mm.
            # Only money converts ("£1.86" for 186p, "1200p" for £12); "8 kg" for "how many grams in 8 kg"
            # would be the question copied back.
            return typed[0] == "money" and any(near(v * typed[1], e * w[1]) for w in same)
        if near(v, e):
            return True
        # an answer asked in pence typed in pounds: "£1.86" for 186p (only where the box says "p")
        return unit == "p" and "£" in str(value) and abs(v * 100 - e) <= (tolerance or 0) + 1e-6
    if at == "frac":
        v, e = _frac(value), _frac(expected)
        return v is not None and e is not None and v == e and not _frac_form(expected, value, prompt)
    if at == "time":
        return _same_time(expected, value, prompt)
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
        return _same_set(expected, value)
    # a 24-hour time kept as text ("09:45", "13:20"): "9:45", "9.45" and "09 45" count; hours are not mod 12
    m = re.fullmatch(r"\s*(\d{1,2})[:.](\d{2})\s*", str(expected))
    if m:
        v = re.fullmatch(r"\s*(\d{1,2})\s*[:. h]\s*(\d{2})\s*", str(value))
        return bool(v) and (int(v.group(1)), int(v.group(2))) == (int(m.group(1)), int(m.group(2)))
    # a position ("3rd"): "3" and "third" count too, unless the question asks for the ordinal in figures;
    # a suffix that is typed must be the right one ("71th" is wrong)
    m = re.fullmatch(r"\s*(\d+)(?:st|nd|rd|th)\s*", str(expected).lower())
    if m:
        v = str(value).strip().lower()
        t = re.fullmatch(r"(\d+)\s*(st|nd|rd|th)", v)
        if t:
            return t.group(1) == m.group(1) and ordinal(t.group(1)) == t.group(1) + t.group(2)
        if _ORD_FIGURES.search(str(prompt or "")):
            return False
        return _ORD_WORDS.get(v, v) == m.group(1)
    # str — accept UK 'and' being present or absent, and 'seven hundred four'
    sv, se = _sn(value), _sn(expected)
    if sv == se or sv.replace(" and ", " ") == se.replace(" and ", " "):
        return True
    if _RULE.fullmatch(se):                          # a sequence rule: "+10" for "add 10", "×3" for "multiply by 3"
        return _rule(sv) == se
    pe = _poly(se)                                   # algebra in another order: "30+5x" for "5x+30"
    if pe is not None:
        return _poly(sv) == pe
    wv, we = _words(sv), _words(se)                  # "a half turn" for "half", "Wednesday" for "Wed"
    return bool(wv) and (wv == we or wv.replace(" and ", " ") == we.replace(" and ", " "))


# "two" typed for 2 (a word answer to "How many …?"); never where writing the number in digits is the task
_WORD_NUM = {w: float(i) for i, w in enumerate(_ONES)} | {w: float(10 * i) for i, w in enumerate(_TENS) if w}
_IN_DIGITS = re.compile(r"digit|numeral|figures|in numbers", re.I)

# A term-to-term rule as words: "add 10", "subtract 3", "multiply by 2", "divide by 4", "multiply by 2 then add 1"
_RULE_STEP = r"(?:add|subtract|multiply by|divide by) \d+(?:\.\d+)?"
_RULE = re.compile(r"%s(?: (?:then|and) %s)?" % (_RULE_STEP, _RULE_STEP))
_RULE_SAID = [(re.compile(p), r) for p, r in (
    (r"(?:^|(?<=\s))\+(?=\d)|\bplus |\badd on |\bincrease by ", "add "),
    (r"(?:^|(?<=\s))-(?=\d)|\bminus |\btake away |\btake |\bsubtract by |\bdecrease by ", "subtract "),
    (r"(?:^|(?<=\s))(?:x|×|\*)(?=\d)|\btimes (?:by )?|\bmultiply (?!by)|\bmultiplied by ", "multiply by "),
    (r"(?:^|(?<=\s))(?:÷|/)(?=\d)|\bdivide (?!by)|\bdivided by |\bshare by ", "divide by "))]


def _rule(sv):
    """A typed rule in the words the question uses: "+10" -> "add 10", "x2 then +1" -> "multiply by 2 then add 1".
    "each time" and "every time" are dropped."""
    s = re.sub(r"\s*\b(?:each|every) (?:time|term)\b", "", sv)
    s = re.sub(r"(?<=\d)\s*(?=[+×x*÷/-]\d)", " then ", s)                # "x2+1" -> "x2 then +1"
    s = re.sub(r"(?<=[+×x*÷/-])\s+(?=\d)", "", s)                       # "+ 10" -> "+10"
    s = re.sub(r"(?<=[a-z])(?=[+×*÷/-]\d)", " ", s)                      # "then+1" -> "then +1"
    for pat, rep in _RULE_SAID:
        s = pat.sub(rep, s)
    s = re.sub(r"(multiply by|divide by|add|subtract)\s+(?=\d)", r"\1 ", s)
    return " ".join(s.split())


def slipped_words(answer_type, expected, value, prompt=""):
    """A word answer that is right but for a slip of the keyboard ("yse", "eigth thousand"): [(typed, wanted)].
    Never a word the question offers as a choice, a number word for another ("eighty" for "eight") or yes/no."""
    if answer_type != "str":
        return []
    se, sv = _sn(expected).replace(" and ", " "), _sn(value).replace(" and ", " ")
    if not re.fullmatch(r"[a-z ]+", se) or not re.fullmatch(r"[a-z ]+", sv):
        return []
    never = typos.NUMBER_WORDS | {"yes", "no"} | set(re.findall(r"[a-z]+", str(prompt or "").lower()))
    return typos.slips(sv.split(), se.split(), never)


def slip_hint(expected, pairs):
    """What the child is told before the free retry."""
    if all(w in typos.NUMBER_WORDS for w in _sn(expected).split()):
        return typos.number_hint(pairs)
    return typos.RETRY


def form_hint(answer_type, expected, value, prompt=""):
    """For a refused fraction of the right value: what to change ("Right value — now simplify it.")."""
    if answer_type != "frac":
        return ""
    v, e = _frac(value), _frac(expected)
    return _frac_form(expected, value, prompt) if v is not None and v == e else ""


def _poly(s):
    """A linear or polynomial expression, optionally with "C=" in front, as {lhs, term: coefficient}:
    "11a+11b" and "11b+11a" give the same. None when it is not one (brackets, ratios, words, numbers
    alone), so those keep the text match."""
    s = s.replace("×", "").replace("*", "").replace("·", "")
    if not re.search(r"[\d+^=-]", s):               # a word ("kite") is not k × i × t × e
        return None
    lhs = ""
    if s.count("=") == 1:
        lhs, s = s.split("=")
        if not re.fullmatch(r"[a-z]", lhs):
            return None
    if not re.fullmatch(r"[+-]?[0-9a-z.^]+(?:[+-][0-9a-z.^]+)*", s):
        return None
    terms, letters = {}, False
    for sign, body in re.findall(r"([+-]?)([^+-]+)", s):
        m = re.fullmatch(r"(\d*\.?\d+)?((?:[a-z](?:\^\d+)?){0,4})", body)
        if not m or not (m.group(1) or m.group(2)):
            return None
        powers = {}
        for v, n in re.findall(r"([a-z])(?:\^(\d+))?", m.group(2)):
            powers[v] = powers.get(v, 0) + int(n or 1)
        letters = letters or bool(powers)
        k = tuple(sorted(powers.items()))
        c = Fraction(m.group(1)) if m.group(1) else Fraction(1)
        terms[k] = terms.get(k, 0) + (-c if sign == "-" else c)
    if not letters:
        return None
    return {"=": lhs, **{k: c for k, c in terms.items() if c}}


# Word answers: a fair extra word, a short or long name, a common synonym.
_LEAD = re.compile(r"^(?:it is|it's|it was|its|it|they are|they|a|an|the)\s+")
_TAIL = {"turn", "angle", "angled", "triangle", "quadrilateral", "shape", "place", "column", "number",
         "pound", "pounds"}                          # "acute angle", "equilateral triangle", "... pounds" on a cheque
_SAME = {
    "oblong": "rectangle", "rectangular prism": "cuboid", "square pyramid": "square based pyramid",
    "triangular pyramid": "triangular based pyramid", "compass": "compasses", "pair of compass": "compasses",
    "full": "whole", "3/4": "three quarter", "1/2": "half",
    "1/4": "quarter", "one half": "half", "one quarter": "quarter",
    "millimetre": "mm", "millimeter": "mm", "centimetre": "cm", "centimeter": "cm", "metre": "m", "meter": "m",
    "kilometre": "km", "kilometer": "km", "gram": "g", "gramme": "g", "kilogram": "kg", "kilo": "kg",
    "millilitre": "ml", "milliliter": "ml", "litre": "l", "liter": "l", "pence": "p", "penny": "p",
    "monday": "mon", "tuesday": "tue", "tues": "tue", "wednesday": "wed", "weds": "wed", "thursday": "thu",
    "thur": "thu", "thurs": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun",
    "january": "jan", "february": "feb", "march": "mar", "april": "apr", "june": "jun", "july": "jul",
    "august": "aug", "september": "sep", "sept": "sep", "october": "oct", "november": "nov", "december": "dec",
}
_NUMBER_WORDS = set(_ONES) | set(_TENS) | {"hundred", "thousand", "million"}


def _one(w):
    """'grapes' -> 'grape', 'boxes' -> 'box', 'potatoes' -> 'potato'; not 'less', 'tens' (ten is a number)."""
    if len(w) < 4 or not w.isalpha() or w.endswith(("ss", "us", "is")):
        return w
    one = w[:-2] if re.search(r"(?:[sxz]|ch|sh|o)es$", w) else w[:-1] if w.endswith("s") else w
    return w if one in _NUMBER_WORDS else one


def _words(s):
    s = _LEAD.sub("", _LEAD.sub("", s))
    ws = s.split()
    while len(ws) > 1 and ws[-1] in _TAIL:
        ws.pop()
    if ws:
        ws[-1] = _one(ws[-1])
    s = " ".join(ws)
    return _SAME.get(s, s)

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


_DP_WORDS = {"one": 1, "two": 2, "three": 3}
_DP_ASKED = re.compile(r"\bto (\d|one|two|three) (?:decimal place|d\.?p\b)", re.I)


def _set_text(a):
    """A list of big numbers is shown as the question writes them: "6,184,930; 7,518,249"."""
    parts = [p for p in re.sub(r"\band\b|[;,]", " ", str(a)).split()]
    nums = [_num(p) for p in parts]
    if not parts or None in nums or max(abs(n) for n in nums) < 1000:
        return a
    return "; ".join(f"{int(n):,}" if n.is_integer() else f"{n:,}" for n in nums)


def _grouped(n):
    """6300000 -> "6,300,000" as the questions write it; under 10,000 stays a plain number (years, 4-digit sums)."""
    return f"{n:,}" if abs(n) >= 10000 else n


def answer_text(q):
    """The answer as it is shown after a wrong try. Generators compute with floats, so a whole number
    comes out as 26.0 and a third as 0.3333333333333333: show 26, 1/3 or 2 1/3 instead. When the prompt
    asks for decimal places, show that many (6.0, 21.90)."""
    a = q.get("answer")
    if q.get("answer_type") == "set":
        return _set_text(a)
    if q.get("answer_type", "num") not in ("num", "int"):
        return a
    if isinstance(a, int) and not isinstance(a, bool):
        return _grouped(a)
    if not isinstance(a, float):
        return a
    m = _DP_ASKED.search(q.get("prompt", ""))
    n = m and (_DP_WORDS.get(m.group(1).lower()) or int(m.group(1)))
    if n and abs(round(a, n) - a) < 1e-9:      # not a bound such as 2.85 for "rounds to 2.9 to 1 d.p."
        return f"{a:.{n}f}"
    if a.is_integer():
        return _grouped(int(a))
    f = Fraction(a).limit_denominator(24)
    if f.denominator > 1 and abs(float(f) - a) < 1e-6 and len(f"{a:.10g}".split(".")[-1]) >= 5:
        w, r = divmod(abs(f.numerator), f.denominator)
        return ("-" if a < 0 else "") + (f"{w} {r}/{f.denominator}" if w else f"{r}/{f.denominator}")
    return float(f"{a:.10g}")


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


_FRAC_NAMED = re.compile(r"\b\d+\s*/\s*\d+\b|\b(?:halves|half|thirds?|quarters?|fifths?|sixths?|sevenths?|eighths?|"
                         r"ninths?|twelfths?)\b", re.I)
_TYPE_IT = re.compile(r"\b(?:write|type|give|what are)\b", re.I)
_PLOT_IT = re.compile(r"\b(?:plot|mark|graph|draw)\b", re.I)


def _keypad(q):
    """The phone keyboard a typed answer needs. iOS 'numeric' has no '.' or '−' and 'decimal' has no '−',
    so only a whole, non-negative number gets the digit pad."""
    if q.get("answer_type", "num") not in ("num", "int"):
        return "text"
    v = _num(q.get("answer"))
    if v is None or v < 0:
        return "text"
    return "numeric" if float(v).is_integer() and float(q.get("tolerance") or 0).is_integer() else "decimal"


def present(q, skill_key):
    """Shape how a generated question is shown, from its own structure (component, spec, answer)."""
    comp, spec, prompt = q.get("component"), dict(q.get("spec") or {}), q.get("prompt", "")
    spec.setdefault("keypad", _keypad(q))
    a = _num(q.get("answer")) if q.get("answer_type", "num") in ("num", "int") else None
    if comp == "clock" and "snap" not in spec:
        # the minute hand snaps to what the question needs: quarters in Year 1, 5 minutes after that
        # (1 minute only when the time is not on a 5)
        try:
            mins = int(str(q.get("answer")).split(":")[1])
        except (IndexError, ValueError):
            mins = 1
        spec["snap"] = 15 if skill_key.startswith("Y1.") and mins % 15 == 0 else 5 if mins % 5 == 0 else 1
    elif comp == "number_line" and a is not None:
        # a fraction line (steps of 1/n, a fraction in the prompt, no decimals) is labelled in whole numbers only
        # and answered as a fraction, so neither the ticks nor the "Answer:" line turns it into decimals
        st = float(spec.get("step") or 1)
        n = round(1 / st) if st > 0 else 0
        k = round(a * n)
        if (2 <= n <= 24 and abs(n * st - 1) < 1e-6 and abs(a * n - k) < 1e-3 and _FRAC_NAMED.search(prompt)
                and not re.search(r"\d\.\d|%|√|decimal", prompt, re.I)
                and abs(float(spec.get("min") or 0) * n - round(float(spec.get("min") or 0) * n)) < 1e-6):
            spec["fractions"] = n
            # shown as the prompt writes it ("2/5" on a line in tenths), else in the line's own steps ("4/8")
            said = [m.group(0) for m in re.finditer(r"(?<![\d/])(?:\d+ )?\d+/\d+(?![\d/])", prompt)
                    if _frac(m.group(0)) == Fraction(k, n)]
            w, r = divmod(abs(k), n)
            q["answer"] = said[0] if said else ("-" if k < 0 else "") + (f"{w} {r}/{n}" if w and r else str(w) if not r
                                                                            else f"{r}/{n}")
            q["answer_type"] = "frac"
    elif comp == "coordinate_grid" and q.get("answer_type") == "coord" and not spec.get("typed") \
            and _TYPE_IT.search(prompt) and not _PLOT_IT.search(prompt):
        spec["typed"] = True                            # "Write the coordinates of A": a box to write in
        spec.setdefault("placeholder", "(x, y)")
    elif comp == "equal_groups" and spec.get("mode", "read") == "read" and a is not None:
        g, p = int(spec.get("groups") or 0), int(spec.get("per") or 0)
        if g and p and a != g * p and a in (g, p) and re.search(r"(?<![\d.])%d(?![\d.])" % (g * p), prompt):
            # "how many groups / how many in each group": show the counters before they are grouped
            # (and, for sharing, the empty groups), not the finished picture
            spec = {k: v for k, v in spec.items() if k not in ("groups", "per")}
            spec["loose"] = g * p
            if a == p and a != g:
                spec["rings"] = g
    elif comp == "equal_groups" and spec.get("mode") == "build" and spec.get("targetGroups") and a is not None \
            and a == spec["targetGroups"] * spec.get("targetPer", 0):
        # build the groups asked for AND type the total: both are marked
        spec["typed"] = True
        q["answer"] = f"{spec['targetGroups']} groups of {spec['targetPer']} = {int(a)}"
        q["answer_type"] = "str"
    elif comp == "array" and spec.get("mode", "build") == "build" and spec.get("targetRows") and a is not None \
            and a == spec["targetRows"] * spec.get("targetCols", 0):
        # build the array asked for AND type the total; "3 rows of 2" must be 3 rows, "show 3 × 2" either way round
        spec["typed"] = True
        spec["eitherWay"] = not re.search(r"\brows?\b", prompt, re.I)
        q["answer"] = f"{spec['targetRows']} rows of {spec['targetCols']} = {int(a)}"
        q["answer_type"] = "str"
    elif comp == "angle" and spec.get("mode", "classify") == "classify" and spec.get("degrees") is not None:
        d = float(spec["degrees"])
        if "shown" in prompt and re.search(r"(?<![\d.])%s\s*°" % re.escape(f"{d:g}"), prompt):
            # the prompt gives the drawn angle: label it with its value, and put the "?" on the angle asked for
            spec["given"] = True
            if a is not None and "straight line" in prompt.lower() and abs(a + d - 180) < 1e-9:
                spec["unknown"] = "straight"
            elif a is not None and "straight line" in prompt.lower() and abs(2 * a + d - 180) < 1e-9:
                spec["unknown"] = "straight2"
            elif a is not None and abs(a + d - 360) < 1e-9:
                spec["unknown"] = "full"
            elif a is not None and abs(a + d - 90) < 1e-9 and re.search(r"complement|right angle", prompt, re.I):
                spec["unknown"] = "right"
    q["spec"] = spec
    return neutral_examples(q)


_EX_DIGITS = re.compile(r"\d+")
_EX_TOKEN = re.compile(r"-?\d+(?:[./:]\d+)*")


def _ex_tokens(text):
    return set(_EX_TOKEN.findall(str(text).replace(",", " ")))


def _ex_plain(text):
    return re.sub(r"[\s.…]+$|\s+|\.\.\.|…", "", str(text).lower())


def _ex_shift(text, k):
    """Every digit moved on by k, keeping the shape ("3/4" -> "4/5", "x^2+6x+9" -> "x^3+7x+0"); a number never
    gains a leading 0 and never becomes 0, so no "x/0" and no "07"."""
    def one(m):
        o = m.group(0)
        s = "".join(str((int(c) + k) % 10) for c in o)
        return str(k) + s[1:] if s[0] == "0" and o[0] != "0" else s
    return _EX_DIGITS.sub(one, text)


def neutral_examples(q):
    """A format example must never be the answer or a part of it: "e.g. 665, 675, ..." in the box for "Count on
    in 10s from 655", or "e.g. 3/4" (a fixed example) when the answer happens to be 3/4, or a question saying
    "Write it like 2:3" whose answer is 2:3. Such an example gets the same shape with other digits; numbers the
    question itself shows may stay."""
    ans, prompt = str(q.get("answer", "")), q.get("prompt", "")
    atoks = _ex_tokens(ans)
    if _EX_DIGITS.search(ans):
        k = next((k for k in range(1, 10) if not (_ex_tokens(_ex_shift(ans, k)) & atoks)), 1)
        prompt = re.sub(r"\b(like|for example|e\.g\.) %s(?![\w/:^]|\.\d)" % re.escape(ans),
                        lambda m: "%s %s" % (m.group(1), _ex_shift(ans, k)), prompt)
        q["prompt"] = prompt
    ptoks = _ex_tokens(prompt)

    def leaks(ex):
        return _ex_plain(ex) == _ex_plain(ans) or bool((_ex_tokens(ex) & atoks) - ptoks)
    spec = q.get("spec") or {}
    ph = spec.get("placeholder")
    if isinstance(ph, str) and ph[:4].lower() == "e.g." and leaks(ph[4:]):
        # a list says only how to write it: shifted digits would show numbers that break the question's rule
        spec["placeholder"] = "numbers, with commas" if "," in ph and "(" not in ph else next(
            (p for p in (_ex_shift(ph, k) for k in range(1, 10)) if not leaks(p[4:])), "type your answer")
    return q


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
    q = present(q, skill_key)                           # keypad, clock snap, fraction lines, typed boxes, start pictures
    token = secrets.token_urlsafe(16)
    await db.maths_lab_q.update_one(
        {"_id": token},
        {"$set": {
            "skill": skill_key,
            "prompt": q["prompt"],
            "answer": q["answer"],
            "display": answer_text(q),
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
    prompt = doc.get("prompt", "")
    correct = check_answer(doc["answer_type"], doc["answer"], value, doc.get("tolerance", 0), doc.get("unit"), prompt)
    solution = list(doc.get("solution", []))
    if not correct:
        slipped = slipped_words(doc["answer_type"], doc["answer"], value, prompt)
        if slipped and not doc.get("retried"):
            # a spelling slip where spelling is not the skill: one free retry, the question stays open
            await db.maths_lab_q.update_one({"_id": doc["_id"]}, {"$set": {"done": False, "retried": True}})
            return {"ok": True, "correct": False, "retry": True, "hint": slip_hint(doc["answer"], slipped),
                    "skill": doc.get("skill")}
        if slipped:                              # after the retry: name the misspelt word
            right = "Your number was right. " if slip_hint(doc["answer"], slipped) != typos.RETRY else ""
            solution.insert(0, right + typos.corrections(slipped))
        hint = form_hint(doc["answer_type"], doc["answer"], value, prompt)
        if hint:                                 # the right value in the wrong form: say so first
            solution.insert(0, hint)
    return {"ok": True, "correct": bool(correct),
            "expected": doc.get("display", doc["answer"]), "solution": solution,
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
