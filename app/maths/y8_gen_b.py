# dev/app/logic/y8_gen_b.py — Year 8 generators: strands 8.2 and 8.3
#
# 8.2  Calculating with decimals & directed numbers   (Y8.2.a .. Y8.2.i)
# 8.3  Fractions                                       (Y8.3.a .. Y8.3.j)
#
# Every generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and chooses at random between 8+ genuinely different framings (bare
# calculation, word problem, missing value, inverse, visual model, comparison,
# reasoning, multi-step).
#
# All decimal arithmetic is done with Decimal / Fraction on exact integer inputs
# and converted to float only at the very end, so no answer is ever
# 0.30000000000000004. Ordinary subtraction is guarded so nothing turns
# unintentionally negative — the EXCEPTIONS are the directed-number skills
# (Y8.2.f, Y8.2.g) and the rational-number skill (Y8.2.h), which are MEANT to
# produce negative results.
#
# NOTE on `frac` answers: check_answer accepts any equivalent fraction, so a
# question whose objective is "in its lowest terms / simplest form" asks for the
# numerator or the denominator as an int, or for a mixed number as a str.
#
# Visual components used here:
#   number_line ......... decimals, and directed numbers (min may be negative)
#   fraction_bar ........ fraction equivalence / shading
#   area_grid ........... fraction and hundredths models
#   strip_model ......... fraction-of-a-quantity bar models
#   data_table .......... price lists, rate tables, conversion tables
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from .maths_engine import skill, pick, NAMES, n_words

S2 = "8.2 Calculating with decimals & directed numbers"
S3 = "8.3 Fractions"


# ================================================================ helpers ====
def _t(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_t(d)]


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


# ---- exact decimals ---------------------------------------------------------
def _D(x):
    if isinstance(x, Decimal):
        return x
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def _txt(x):
    """Exact Decimal -> tidy UK text: 3.400 -> '3.4', 5 -> '5', -0.50 -> '-0.5'."""
    v = _D(x)
    if v == v.to_integral_value():
        return format(v.quantize(Decimal(1)), "f")
    return format(v.normalize(), "f")


def _fl(x):
    return float(_D(x))


def _rnd(x, places=0):
    q = Decimal(1).scaleb(-int(places))
    return _D(x).quantize(q, rounding=ROUND_HALF_UP)


def _mk(dp, lo, hi):
    """A Decimal with `dp` decimal places, from an integer in [lo, hi] counted
    in units of 10**-dp; when dp >= 1 it always keeps a decimal digit."""
    dp = int(dp)
    for _try in range(40):
        n = random.randint(int(lo), int(hi))
        if dp == 0 or n % (10 ** dp):
            return _D(n).scaleb(-dp)
    return _D(random.randint(int(lo), int(hi)) | 1).scaleb(-dp)


def _lb(pence):
    pence = int(pence)
    sign = "-" if pence < 0 else ""
    pence = abs(pence)
    return "%s£%d.%02d" % (sign, pence // 100, pence % 100)


# ---- exact fractions --------------------------------------------------------
def _hcf(a, b):
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a or 1


def _lcm(a, b):
    a, b = abs(int(a)), abs(int(b))
    if a == 0 or b == 0:
        return 0
    return a * b // _hcf(a, b)


def _simp(n, d):
    g = _hcf(n, d)
    return n // g, d // g


def _mixed_str(w, n, d):
    """(2, 3, 4) -> '2 3/4';  (2, 0, 4) -> '2';  (0, 3, 4) -> '3/4'."""
    w, n, d = int(w), int(n), int(d)
    sign = ""
    if w < 0 or (w == 0 and n < 0):
        sign = "-"
        w, n = abs(w), abs(n)
    if n == 0:
        return "%s%d" % (sign, w)
    if w == 0:
        return "%s%d/%d" % (sign, n, d)
    return "%s%d %d/%d" % (sign, w, n, d)


def _improper_to_mixed(n, d):
    """(11, 4) -> (2, 3, 4) with the fraction part in lowest terms."""
    w = n // d
    rn, rd = n % d, d
    if rn:
        rn, rd = _simp(rn, rd)
    return w, rn, rd


_FRAC_WORDS = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth",
               7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
               12: "twelfth", 20: "twentieth", 100: "hundredth"}
_FRAC_PLURAL = {2: "halves"}


def _frac_words(n, d):
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%d/%d" % (n, d)
    if n == 1:
        return "one " + w
    return "%s %s" % (n_words(n), _FRAC_PLURAL.get(d, w + "s"))


def _ths(d):
    """Plural denominator word: 2 -> 'halves', 4 -> 'quarters', 7 -> 'sevenths'."""
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%dths" % d
    return _FRAC_PLURAL.get(d, w + "s")


# terminating-decimal denominators (all of form 2^a * 5^b)
_TERM_DEN = [2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 100]


def _frac_to_dec(n, d):
    """Exact Decimal for a terminating fraction n/d."""
    return (_D(n) / _D(d))


# ---- question builders ------------------------------------------------------
def _nq(prompt, value, solution=None, unit=None, text=False, placeholder=None,
        tol=1e-6):
    spec = {}
    if unit:
        spec["unit"] = unit
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": _fl(value), "answer_type": "num",
            "tolerance": tol, "solution": solution or []}


def _iq(prompt, value, solution=None, unit=None, placeholder=None):
    spec = {}
    if unit:
        spec["unit"] = unit
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": int(value), "answer_type": "int",
            "tolerance": 0, "solution": solution or []}


def _sq(prompt, value, placeholder=None, solution=None):
    spec = {"text": True}
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": str(value), "answer_type": "str",
            "tolerance": 0, "solution": solution or []}


def _fq(prompt, num, den, placeholder="e.g. 3/8", solution=None):
    """A typed fraction answer (equivalent fractions are accepted)."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": "%d/%d" % (int(num), int(den)), "answer_type": "frac",
            "tolerance": 0, "solution": solution or []}


def _mixq(prompt, w, n, den, placeholder="e.g. 2 3/4", solution=None):
    """A typed mixed-number answer, e.g. '2 3/4' or '-1 1/2'."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": _mixed_str(w, n, den), "answer_type": "str",
            "tolerance": 0, "solution": solution or []}


def _fracstr(fr):
    """A signed Fraction as tidy text: Fraction(-3,8) -> '-3/8', Fraction(4,1)
    -> '4'.  The sign always sits in the numerator."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    return "%d/%d" % (fr.numerator, fr.denominator)


def _frac_result_q(base_prompt, res, solution):
    """Route a (possibly negative) Fraction result to the right answer shape:
    whole number -> int, proper fraction -> frac, otherwise a mixed-number str.
    `base_prompt` carries the calculation WITHOUT a 'give your answer' clause;
    the matching clause is appended here so wording and answer_type agree."""
    res = Fraction(res)
    if res.denominator == 1:
        return _iq(base_prompt + " Give your answer as a whole number.",
                   res.numerator, solution)
    if -1 < res < 1:
        return _fq(base_prompt + " Give your answer as a fraction.",
                   res.numerator, res.denominator, solution=solution)
    sign = -1 if res < 0 else 1
    a = -res if res < 0 else res
    w = a.numerator // a.denominator
    rn = a.numerator % a.denominator
    return _mixq(base_prompt + " Give your answer as a mixed number "
                 "in its simplest form.",
                 sign * w, rn, a.denominator, solution=solution)


def _setq(prompt, values, solution, placeholder="e.g. 1.2, 3.4"):
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(_txt(v) for v in values), "answer_type": "set",
            "tolerance": 0, "solution": solution}


def _nlq(prompt, value, lo, hi, step, major, solution, tol=None):
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": _fl(lo), "max": _fl(hi), "step": _fl(step),
                     "major": _fl(major)},
            "answer": _fl(value), "answer_type": "num",
            "tolerance": (_fl(step) / 2.0) if tol is None else tol,
            "solution": solution}


def _fbq(prompt, parts, shaded, solution):
    return {"prompt": prompt, "component": "fraction_bar",
            "spec": {"parts": int(parts), "mode": "shade"},
            "answer": "%d/%d" % (int(shaded), int(parts)),
            "answer_type": "frac", "tolerance": 0, "solution": solution}


def _agread(prompt, parts, shaded, answer, answer_type, solution,
            placeholder=None, tol=0):
    spec = {"mode": "fraction_read", "parts": int(parts), "shaded": int(shaded)}
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tol, "solution": solution}


def _stripq(prompt, parts, part_label, total_label, unknown, answer,
            answer_type, solution, tol=0):
    return {"prompt": prompt, "component": "strip_model",
            "spec": {"mode": "equal_parts", "parts": int(parts),
                     "partLabel": str(part_label),
                     "totalLabel": str(total_label), "unknown": unknown},
            "answer": answer, "answer_type": answer_type,
            "tolerance": tol, "solution": solution}


def _dtq(prompt, headers, rows, answer, answer_type, solution, missing=None,
         placeholder=None, tol=0):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tol, "solution": solution}


_SHOP = ["notebook", "pen", "water bottle", "lunch box", "poster", "badge",
         "keyring", "pencil case", "sticker sheet", "ruler"]
_UNITS = ["kg", "m", "litres", "cm"]


def _plural(word):
    if word.endswith(("ch", "sh", "s", "x")):
        return word + "es"
    return word + "s"


def _pick_opts(opts_by_tier, d, weighted_tail=None):
    d = _t(d)
    opts = list(opts_by_tier[d])
    if weighted_tail:
        opts += weighted_tail
    return pick(opts)()


# ============================================================== 8.2.a ========
@skill("Y8.2.a", "Add and subtract decimals", S2)
def _(d=1):
    d = _t(d)
    dp = _by_d(d, 1, 2, 2)
    lo, hi = _by_d(d, (5, 95), (105, 950), (1005, 9950))

    def _pair():
        a = _mk(dp, lo, hi)
        b = _mk(dp, lo, hi)
        return a, b

    def add_bare():
        a, b = _pair()
        s = a + b
        return _nq("Work out %s + %s" % (_txt(a), _txt(b)), s,
                   ["Line up the decimal points.",
                    "%s + %s = %s." % (_txt(a), _txt(b), _txt(s))])

    def sub_bare():
        a, b = _pair()
        big, small = (a, b) if a >= b else (b, a)
        if big == small:
            big = big + _mk(dp, 10, hi)
        r = big - small
        return _nq("Work out %s − %s" % (_txt(big), _txt(small)), r,
                   ["Line up the decimal points.",
                    "%s − %s = %s." % (_txt(big), _txt(small), _txt(r))])

    def missing_add():
        a, b = _pair()
        s = a + b
        return _nq("%s + ___ = %s . What is the missing number?"
                   % (_txt(a), _txt(s)), b,
                   ["Subtract to reverse the addition.",
                    "%s − %s = %s." % (_txt(s), _txt(a), _txt(b))])

    def inverse_sub():
        a, b = _pair()
        s = a + b
        return _nq("___ − %s = %s . What is the missing number?"
                   % (_txt(a), _txt(b)), s,
                   ["Add to reverse the subtraction.",
                    "%s + %s = %s." % (_txt(a), _txt(b), _txt(s))])

    def money_total():
        who = pick(NAMES)
        pa = random.randint(120, 990)
        pb = random.randint(80, 720)
        item_a, item_b = random.sample(_SHOP, 2)
        return _nq("%s buys a %s for %s and a %s for %s. How much does %s spend "
                   "altogether? Give your answer in pounds."
                   % (who, item_a, _lb(pa), item_b, _lb(pb), who),
                   _D(pa + pb) / 100, unit="£",
                   solution=["%s + %s = %s." % (_lb(pa), _lb(pb), _lb(pa + pb))])

    def money_change():
        pa = random.randint(120, 480)
        pb = random.randint(120, 480)
        total = pa + pb
        paid = ((total // 100) + 1 + random.randint(0, 4)) * 100
        change = paid - total
        return _nq("A %s costs %s and a %s costs %s. They are paid for with "
                   "%s. How much change is given? Give your answer in pounds."
                   % (pick(_SHOP), _lb(pa), pick(_SHOP), _lb(pb), _lb(paid)),
                   _D(change) / 100, unit="£",
                   solution=["Total cost = %s." % _lb(total),
                    "%s − %s = %s." % (_lb(paid), _lb(total), _lb(change))])

    def measure_word():
        who = pick(NAMES)
        a = _mk(2, 150, 480)
        b = _mk(2, 60, 140)
        r = a - b
        return _nq("A plank of wood is %s m long. %s cuts %s m off the end. "
                   "How long is the plank now? Give your answer in metres."
                   % (_txt(a), who, _txt(b)), r, unit="m",
                   solution=["%s − %s = %s." % (_txt(a), _txt(b), _txt(r))])

    def three_add():
        a = _mk(dp, lo, hi)
        b = _mk(dp, lo, hi)
        c = _mk(dp, lo, hi)
        s = a + b + c
        return _nq("Work out %s + %s + %s" % (_txt(a), _txt(b), _txt(c)), s,
                   ["Add in any order, keeping the points lined up.",
                    "The total is %s." % _txt(s)])

    def line_mark():
        a = _mk(1, 3, 27) / 10 + 0  # tenths on 0..3
        a = _mk(1, 2, 28)
        b = _mk(1, 2, 20)
        a = a / 10
        b = b / 10
        s = a + b
        return _nlq("The number line is marked in tenths. Mark the answer to "
                    "%s + %s." % (_txt(a), _txt(b)), s, 0, 6, Decimal("0.1"),
                    Decimal("1"),
                    ["%s + %s = %s." % (_txt(a), _txt(b), _txt(s))])

    def table_receipt():
        items = random.sample(_SHOP, 3)
        ps = [random.randint(80, 640) for _ in range(3)]
        rows = [[it, _lb(p)] for it, p in zip(items, ps)]
        tot = sum(ps)
        return _dtq("The receipt shows three items. What is the total cost? "
                    "Give your answer in pounds.",
                    ["Item", "Price"], rows, _fl(_D(tot) / 100), "num",
                    ["%s = %s." % (" + ".join(_lb(p) for p in ps), _lb(tot))],
                    tol=1e-6, placeholder="£")

    def compare_sums():
        a, b = _pair()
        c, e = _pair()
        s1, s2 = a + b, c + e
        while s1 == s2:
            c, e = _pair()
            s2 = c + e
        bigger = "first" if s1 > s2 else "second"
        return _sq("Which total is larger: the first, %s + %s, or the second, "
                   "%s + %s? Type first or second."
                   % (_txt(a), _txt(b), _txt(c), _txt(e)), bigger,
                   placeholder="first or second",
                   solution=["First total = %s, second total = %s."
                             % (_txt(s1), _txt(s2)),
                             "The %s total is larger." % bigger])

    common = [add_bare, sub_bare, missing_add, money_total, measure_word,
              line_mark, table_receipt, three_add]
    return _pick_opts({
        0: [add_bare, sub_bare, missing_add, money_total, line_mark,
            table_receipt, measure_word],
        1: common + [money_change, compare_sums],
        2: [sub_bare, missing_add, inverse_sub, money_change, three_add,
            measure_word, compare_sums, table_receipt, add_bare],
    }, d, weighted_tail=[line_mark, table_receipt, line_mark])


# ============================================================== 8.2.b ========
@skill("Y8.2.b", "Multiply decimals", S2)
def _(d=1):
    d = _t(d)

    def dec_by_whole():
        a = _mk(_by_d(d, 1, 1, 2), *_by_d(d, (2, 9), (11, 89), (105, 895)))
        w = random.randint(*_by_d(d, (2, 6), (3, 9), (4, 12)))
        p = a * w
        return _nq("Work out %s × %d" % (_txt(a), w), p,
                   ["%s × %d = %s (multiply, then place the point)."
                    % (_txt(a), w, _txt(p))])

    def dec_by_dec():
        a = _mk(1, *_by_d(d, (2, 9), (11, 49), (11, 89)))
        b = _mk(1, *_by_d(d, (2, 9), (2, 9), (11, 49)))
        a, b = a / 1, b / 1
        # single-place decimals
        a = _mk(1, *_by_d(d, (2, 9), (11, 49), (11, 89)))
        b = _mk(1, 2, 9)
        p = a * b
        return _nq("Work out %s × %s" % (_txt(a), _txt(b)), p,
                   ["Ignore the points: %s × %s = %s."
                    % (_txt(a * 10), _txt(b * 10), _txt(a * b * 100)),
                    "There are 2 decimal places in the question, so %s × %s = "
                    "%s." % (_txt(a), _txt(b), _txt(p))])

    def missing_factor():
        a = _mk(1, 2, 9)
        w = random.randint(*_by_d(d, (2, 6), (3, 9), (4, 12)))
        p = a * w
        return _nq("%s × ___ = %s . What is the missing whole number?"
                   % (_txt(a), _txt(p)), w,
                   ["%s ÷ %s = %d." % (_txt(p), _txt(a), w)])

    def rectangle_area():
        L = _mk(1, *_by_d(d, (15, 45), (21, 89), (105, 245)))
        W = _mk(1, 2, 9)
        area = L * W
        return _nq("A rectangle is %s cm long and %s cm wide. What is its area, "
                   "in cm²?" % (_txt(L), _txt(W)), area, unit="cm²",
                   solution=["Area = length × width = %s × %s = %s cm²."
                    % (_txt(L), _txt(W), _txt(area))])

    def cost_of_many():
        who = pick(NAMES)
        price = random.randint(115, 450)
        n = random.randint(*_by_d(d, (2, 5), (3, 8), (4, 12)))
        item = pick(_SHOP)
        total = price * n
        return _nq("One %s costs %s. %s buys %d of them. What is the total "
                   "cost? Give your answer in pounds."
                   % (item, _lb(price), who, n), _D(total) / 100, unit="£",
                   solution=["%s × %d = %s." % (_lb(price), n, _lb(total))])

    def dec_square():
        a = _mk(1, 2, 9)
        p = a * a
        return _nq("Work out %s²  (that is %s × %s)." % (_txt(a), _txt(a),
                                                         _txt(a)), p,
                   ["%s × %s = %s." % (_txt(a), _txt(a), _txt(p))])

    def dp_reasoning():
        a = _mk(1, 2, 9)
        b = _mk(2, 3, 89)
        p = a * b
        # avoid trailing-zero products so "add the decimal places" (1+2=3)
        # matches the written answer exactly
        for _try in range(40):
            if "." in _txt(p) and len(_txt(p).split(".")[1]) == 3:
                break
            b = _mk(2, 3, 89)
            p = a * b
        n = len(_txt(p).split(".")[1]) if "." in _txt(p) else 0
        return _iq("When you work out %s × %s, how many decimal places does "
                   "the answer have? (Count the decimal places in each number "
                   "and add them.)" % (_txt(a), _txt(b)), n,
                   ["%s has 1 place and %s has 2 places." % (_txt(a), _txt(b)),
                    "The product %s has %d decimal places." % (_txt(p), n)])

    def rate_table():
        price = random.randint(120, 380)
        ns = [2, 3, 5]
        rows = [[str(nn), _lb(price * nn)] for nn in ns[:2]]
        rows.append([str(ns[2]), ""])
        ans = _D(price * ns[2]) / 100
        return _dtq("Each ticket costs the same. Complete the table: what does "
                    "%d tickets cost? Give your answer in pounds." % ns[2],
                    ["Tickets", "Cost"], rows, _fl(ans), "num",
                    ["One ticket costs %s." % _lb(price),
                     "%d × %s = %s." % (ns[2], _lb(price), _lb(price * ns[2]))],
                    missing=(2, 1), tol=1e-6, placeholder="£")

    def fill_petrol():
        litres = _mk(1, 21, 89)
        ppl = random.randint(140, 175)
        cost = _D(litres) * _D(ppl) / 100
        cost = _rnd(cost, 2)
        return _nq("Fuel costs %s per litre. What does %s litres cost? Give "
                   "your answer in pounds, to the nearest penny."
                   % (_lb(ppl), _txt(litres)), cost, unit="£",
                   solution=["%s × %s = about %s." % (_txt(litres), _lb(ppl),
                                             _lb(int(cost * 100)))], tol=1e-6)

    return _pick_opts({
        0: [dec_by_whole, missing_factor, cost_of_many, rectangle_area,
            rate_table, dec_square],
        1: [dec_by_whole, dec_by_dec, missing_factor, rectangle_area,
            cost_of_many, dec_square, rate_table, dp_reasoning],
        2: [dec_by_dec, missing_factor, rectangle_area, dec_square,
            dp_reasoning, rate_table, fill_petrol, cost_of_many],
    }, d, weighted_tail=[rate_table, rate_table])


# ============================================================== 8.2.c ========
@skill("Y8.2.c", "Divide decimals", S2)
def _(d=1):
    d = _t(d)

    def dec_by_whole():
        w = random.randint(*_by_d(d, (2, 5), (3, 8), (4, 12)))
        q = _mk(_by_d(d, 1, 1, 2), *_by_d(d, (12, 48), (21, 89), (105, 445)))
        div = q * w
        return _nq("Work out %s ÷ %d" % (_txt(div), w), q,
                   ["%s ÷ %d = %s." % (_txt(div), w, _txt(q))])

    def dec_by_dec():
        # scale so it becomes whole ÷ whole
        b = _mk(1, 2, 9)
        q = random.randint(*_by_d(d, (2, 8), (3, 12), (4, 24)))
        a = b * q
        return _nq("Work out %s ÷ %s" % (_txt(a), _txt(b)), q,
                   ["Multiply both numbers by 10: %s ÷ %d."
                    % (_txt(a * 10), int(b * 10)),
                    "%s ÷ %d = %d." % (_txt(a * 10), int(b * 10), q)])

    def missing_dividend():
        w = random.randint(*_by_d(d, (2, 5), (3, 8), (3, 9)))
        q = _mk(1, 12, 89)
        div = q * w
        return _nq("___ ÷ %d = %s . What is the missing number?" % (w, _txt(q)),
                   div, ["Reverse it: %s × %d = %s." % (_txt(q), w, _txt(div))])

    def missing_divisor():
        w = random.randint(*_by_d(d, (2, 5), (3, 8), (3, 9)))
        q = _mk(1, 12, 89)
        div = q * w
        return _iq("%s ÷ ___ = %s . What is the missing whole number?"
                   % (_txt(div), _txt(q)), w,
                   ["%s ÷ %s = %d." % (_txt(div), _txt(q), w)])

    def sharing_money():
        n = random.randint(*_by_d(d, (2, 5), (3, 8), (4, 12)))
        each = random.randint(115, 480)
        total = each * n
        return _nq("%s is shared equally between %d people. How much does each "
                   "person get? Give your answer in pounds."
                   % (_lb(total), n), _D(each) / 100, unit="£",
                   solution=["%s ÷ %d = %s." % (_lb(total), n, _lb(each))])

    def rate_per_item():
        n = random.randint(*_by_d(d, (3, 6), (4, 9), (5, 12)))
        each = random.randint(60, 240)
        total = each * n
        return _nq("%d identical pens cost %s in total. What does one pen cost? "
                   "Give your answer in pounds." % (n, _lb(total)),
                   _D(each) / 100, unit="£",
                   solution=["%s ÷ %d = %s." % (_lb(total), n, _lb(each))])

    def scaling_equiv():
        b = _mk(1, 2, 8)
        q = random.randint(4, 9)
        a = b * q
        return _iq("%s ÷ %s gives the same answer as %d ÷ %d. What is that "
                   "answer?" % (_txt(a), _txt(b), int(a * 10), int(b * 10)), q,
                   ["Multiplying both numbers by 10 does not change the "
                    "answer.",
                    "%d ÷ %d = %d." % (int(a * 10), int(b * 10), q)])

    def length_pieces():
        piece = _mk(1, 12, 45)
        n = random.randint(*_by_d(d, (3, 6), (4, 8), (5, 12)))
        total = piece * n
        return _iq("A ribbon %s cm long is cut into equal pieces each %s cm "
                   "long. How many pieces are there?" % (_txt(total),
                                                         _txt(piece)), n,
                   ["%s ÷ %s = %d pieces." % (_txt(total), _txt(piece), n)])

    def table_unit_cost():
        n = random.randint(4, 8)
        each = random.randint(90, 320)
        total = each * n
        rows = [["Number of items", str(n)], ["Total cost", _lb(total)],
                ["Cost of one", ""]]
        return _dtq("Complete the table to find the cost of one item. Give your "
                    "answer in pounds.", ["", ""], rows, _fl(_D(each) / 100),
                    "num", ["%s ÷ %d = %s." % (_lb(total), n, _lb(each))],
                    missing=(2, 1), tol=1e-6, placeholder="£")

    return _pick_opts({
        0: [dec_by_whole, missing_dividend, sharing_money, rate_per_item,
            length_pieces, table_unit_cost],
        1: [dec_by_whole, dec_by_dec, missing_dividend, missing_divisor,
            sharing_money, rate_per_item, length_pieces, table_unit_cost],
        2: [dec_by_dec, missing_divisor, scaling_equiv, sharing_money,
            length_pieces, table_unit_cost, dec_by_whole, rate_per_item],
    }, d, weighted_tail=[table_unit_cost, table_unit_cost])


# ============================================================== 8.2.d ========
@skill("Y8.2.d", "Multiply and divide decimals by powers of ten", S2)
def _(d=1):
    d = _t(d)
    pows = _by_d(d, [10, 100], [10, 100, 1000], [10, 100, 1000])

    def mul():
        k = pick(pows)
        a = _mk(_by_d(d, 1, 2, 3), *_by_d(d, (12, 98), (105, 985), (1005, 9985)))
        r = a * k
        return _nq("Work out %s × %d" % (_txt(a), k), r,
                   ["Multiplying by %d moves every digit %d place(s) to the "
                    "left." % (k, len(str(k)) - 1),
                    "%s × %d = %s." % (_txt(a), k, _txt(r))])

    def div():
        k = pick(pows)
        r = _mk(_by_d(d, 1, 2, 2), *_by_d(d, (12, 98), (105, 985), (105, 985)))
        a = r * k
        return _nq("Work out %s ÷ %d" % (_txt(a), k), r,
                   ["Dividing by %d moves every digit %d place(s) to the "
                    "right." % (k, len(str(k)) - 1),
                    "%s ÷ %d = %s." % (_txt(a), k, _txt(r))])

    def missing_power():
        a = _mk(_by_d(d, 1, 2, 2), 12, 98)
        k = pick(pows)
        r = a * k
        return _iq("%s × ___ = %s . The missing number is 10, 100 or 1000. "
                   "What is it?" % (_txt(a), _txt(r)), k,
                   ["The digits move %d place(s) to the left."
                    % (len(str(k)) - 1),
                    "So the multiplier is %d." % k])

    def missing_power_div():
        r = _mk(_by_d(d, 1, 2, 2), 12, 98)
        k = pick(pows)
        a = r * k
        return _iq("%s ÷ ___ = %s . The missing number is 10, 100 or 1000. "
                   "What is it?" % (_txt(a), _txt(r)), k,
                   ["The digits move %d place(s) to the right."
                    % (len(str(k)) - 1),
                    "So the divisor is %d." % k])

    def two_step():
        a = _mk(1, 12, 98)
        r = a * 100
        return _nq("Work out %s × 10 × 10" % _txt(a), r,
                   ["× 10 × 10 is the same as × 100.",
                    "%s × 100 = %s." % (_txt(a), _txt(r))])

    def measure_convert():
        m = _mk(_by_d(d, 1, 2, 2), 12, 95)
        cm = m * 100
        return _nq("There are 100 cm in a metre. Convert %s m into "
                   "centimetres." % _txt(m), cm, unit="cm",
                   solution=["%s × 100 = %s cm." % (_txt(m), _txt(cm))])

    def money_convert():
        p = random.randint(*_by_d(d, (30, 90), (120, 980), (1050, 8950)))
        pounds = _D(p) / 100
        return _nq("There are 100 pence in a pound. Convert %dp into pounds "
                   "by dividing by 100." % p, pounds, unit="£",
                   solution=["%d ÷ 100 = %s." % (p, _txt(pounds))])

    def io_x10():
        a = _mk(1, 12, 89)
        rows = [[_txt(a), _txt(a * 10)], [_txt(a * 10), _txt(a * 100)],
                [_txt(a * 100), ""]]
        return _dtq("Each 'Out' is the 'In' multiplied by 10. Complete the "
                    "last row.", ["In", "Out"], rows, _fl(a * 1000), "num",
                    ["%s × 10 = %s." % (_txt(a * 100), _txt(a * 1000))],
                    missing=(2, 1), tol=1e-6)

    def digit_move():
        k = pick([10, 100, 1000])
        a = _mk(2, 105, 985)
        r = a / k
        return _nq("Work out %s ÷ %d" % (_txt(a), k), r,
                   ["Move each digit %d place(s) right."
                    % (len(str(k)) - 1),
                    "%s ÷ %d = %s." % (_txt(a), k, _txt(r))])

    return _pick_opts({
        0: [mul, div, missing_power, measure_convert, money_convert, io_x10],
        1: [mul, div, missing_power, missing_power_div, measure_convert,
            money_convert, io_x10, two_step],
        2: [mul, div, missing_power, missing_power_div, two_step, digit_move,
            money_convert, io_x10],
    }, d, weighted_tail=[io_x10, io_x10])


# ============================================================== 8.2.e ========
@skill("Y8.2.e", "Multi-step decimal calculations", S2)
def _(d=1):
    d = _t(d)

    def add_then_mul():
        a = _mk(1, 12, 45)
        b = _mk(1, 11, 40)
        k = random.randint(*_by_d(d, (2, 4), (2, 5), (3, 6)))
        r = (a + b) * k
        return _nq("Work out (%s + %s) × %d" % (_txt(a), _txt(b), k), r,
                   ["Brackets first: %s + %s = %s."
                    % (_txt(a), _txt(b), _txt(a + b)),
                    "%s × %d = %s." % (_txt(a + b), k, _txt(r))])

    def mul_then_add():
        a = _mk(1, 12, 45)
        k = random.randint(2, 5)
        b = _mk(1, 11, 60)
        r = a * k + b
        return _nq("Using BIDMAS, work out %s × %d + %s" % (_txt(a), k,
                                                            _txt(b)), r,
                   ["Multiply first: %s × %d = %s."
                    % (_txt(a), k, _txt(a * k)),
                    "%s + %s = %s." % (_txt(a * k), _txt(b), _txt(r))])

    def sub_then_div():
        q = _mk(1, 12, 45)
        k = random.randint(2, 5)
        b = _mk(1, 11, 40)
        a = q * k + b
        r = (a - b) / k
        return _nq("Work out (%s − %s) ÷ %d" % (_txt(a), _txt(b), k), r,
                   ["Brackets first: %s − %s = %s."
                    % (_txt(a), _txt(b), _txt(a - b)),
                    "%s ÷ %d = %s." % (_txt(a - b), k, _txt(r))])

    def shopping_change():
        item = pick(_SHOP)
        price = random.randint(115, 320)
        n = random.randint(2, 4)
        paid = ((price * n) // 100 + 1 + random.randint(1, 5)) * 100
        change = paid - price * n
        return _nq("%d %s cost %s each. They are paid for with %s. How much "
                   "change is given? Give your answer in pounds."
                   % (n, _plural(item), _lb(price), _lb(paid)),
                   _D(change) / 100, unit="£",
                   solution=["Cost = %d × %s = %s." % (n, _lb(price), _lb(price * n)),
                    "%s − %s = %s." % (_lb(paid), _lb(price * n),
                                       _lb(change))])

    def mean_of():
        n = _by_d(d, 3, 4, 5)
        vals = [_mk(1, 12, 88) for _ in range(n)]
        while len(set(vals)) < n:               # repeated values make the mean trivial
            vals = [_mk(1, 12, 88) for _ in range(n)]
        # ensure exact mean at 1-2 dp
        n = len(vals)
        tot = sum(vals)
        exact = _D(tot) / n
        m = _rnd(exact, 2)
        return _nq("Find the mean of %s. Give your answer to 2 decimal places."
                   % ", ".join(_txt(v) for v in vals), m,
                   ["Total = %s." % _txt(tot),
                    "%s ÷ %d %s %s." % (_txt(tot), n,
                                        "=" if exact == m else "≈", _txt(m))],
                   tol=1e-6)

    def perimeter():
        L = _mk(1, 21, 85)
        W = _mk(1, 12, 45)
        p = (L + W) * 2
        return _nq("A rectangle is %s cm by %s cm. What is its perimeter, in "
                   "cm?" % (_txt(L), _txt(W)), p, unit="cm",
                   solution=["Perimeter = 2 × (%s + %s) = 2 × %s."
                    % (_txt(L), _txt(W), _txt(L + W)),
                    "= %s cm." % _txt(p)])

    def two_products():
        a = _mk(1, 12, 40)
        j = random.randint(2, 5)
        b = _mk(1, 11, 40)
        k = random.randint(2, 5)
        r = a * j + b * k
        return _nq("Work out %s × %d + %s × %d" % (_txt(a), j, _txt(b), k), r,
                   ["%s × %d = %s and %s × %d = %s."
                    % (_txt(a), j, _txt(a * j), _txt(b), k, _txt(b * k)),
                    "%s + %s = %s." % (_txt(a * j), _txt(b * k), _txt(r))])

    def recipe_scale():
        per = _mk(2, 12, 45)            # 0.12-0.45 kg per person
        base = random.randint(2, 4)
        want = base * random.randint(2, 3)
        one = per
        r = one * want
        return _nq("A recipe for %d people uses %s kg of flour per person. How "
                   "much flour is needed for %d people, in kg?"
                   % (base, _txt(per), want), r, unit="kg",
                   solution=["Each person needs %s kg." % _txt(per),
                    "%s × %d = %s kg." % (_txt(per), want, _txt(r))])

    def bracket_div_add():
        a = _mk(1, 24, 96)
        k = random.choice([2, 3, 4])
        while (a / k) != _rnd(a / k, 1):
            a = _mk(1, 24, 96)
        b = _mk(1, 11, 40)
        r = a / k + b
        return _nq("Work out %s ÷ %d + %s" % (_txt(a), k, _txt(b)), r,
                   ["Divide first: %s ÷ %d = %s."
                    % (_txt(a), k, _txt(a / k)),
                    "%s + %s = %s." % (_txt(a / k), _txt(b), _txt(r))])

    def menu_table():
        items = random.sample(_SHOP, 2)
        p1 = random.randint(90, 320)
        p2 = random.randint(90, 320)
        q1 = random.randint(2, 4)
        q2 = random.randint(2, 4)
        rows = [[items[0], _lb(p1), str(q1)], [items[1], _lb(p2), str(q2)]]
        tot = p1 * q1 + p2 * q2
        return _dtq("The table shows two items with their prices and how many "
                    "are bought. What is the total cost? Give your answer in "
                    "pounds.", ["Item", "Price", "Quantity"], rows,
                    _fl(_D(tot) / 100), "num",
                    ["%d × %s + %d × %s = %s."
                     % (q1, _lb(p1), q2, _lb(p2), _lb(tot))],
                    tol=1e-6, placeholder="£")

    return _pick_opts({
        0: [add_then_mul, mul_then_add, shopping_change, perimeter, mean_of,
            recipe_scale, menu_table],
        1: [add_then_mul, mul_then_add, sub_then_div, shopping_change,
            mean_of, perimeter, two_products, recipe_scale, menu_table],
        2: [mul_then_add, sub_then_div, two_products, mean_of, perimeter,
            bracket_div_add, shopping_change, menu_table],
    }, d, weighted_tail=[menu_table, menu_table])


# ============================================================== 8.2.f ========
# DIRECTED NUMBERS — negative answers are EXPECTED here.
@skill("Y8.2.f", "Add and subtract directed numbers", S2)
def _(d=1):
    d = _t(d)
    R = _by_d(d, 9, 15, 20)

    def add_neg():
        a = pick([x for x in range(-R, R + 1) if x])
        b = -random.randint(1, R)
        s = a + b
        return _iq("Work out %d + (%d)" % (a, b), s,
                   ["Adding %d means moving %d to the left."
                    % (b, abs(b)),
                    "%d + (%d) = %d." % (a, b, s)])

    def sub_to_neg():
        a = pick([x for x in range(-R, R + 1) if x])
        b = random.randint(1, R)        # a − b may be negative or positive
        r = a - b
        return _iq("Work out %d − %d" % (a, b), r,
                   ["Start at %d and count back %d." % (a, b),
                    "%d − %d = %d." % (a, b, r)])

    def sub_neg():
        a = random.randint(-R, R)
        b = -random.randint(1, R)
        r = a - b
        return _iq("Work out %d − (%d)" % (a, b), r,
                   ["Subtracting a negative is the same as adding: %d + %d."
                    % (a, abs(b)),
                    "%d − (%d) = %d." % (a, b, r)])

    def two_neg():
        a = -random.randint(1, R)
        b = -random.randint(1, R)
        s = a + b
        return _iq("Work out (%d) + (%d)" % (a, b), s,
                   ["Both are negative, so combine and keep the sign.",
                    "(%d) + (%d) = %d." % (a, b, s)])

    def missing_add():
        a = random.randint(-R, R)
        s = random.randint(-R, R)
        b = s - a
        return _iq("%d + ___ = %d . What is the missing number?" % (a, s), b,
                   ["Reverse it: %d − %d = %d." % (s, a, b)])

    def temp_change():
        who = pick(NAMES)
        start = random.randint(-8, 5)
        drop = random.randint(3, 12)
        end = start - drop
        return _iq("At dawn the temperature is %d°C. By night it has fallen by "
                   "%d°C. What is the temperature at night, in °C?"
                   % (start, drop), end,
                   ["%d − %d = %d." % (start, drop, end)], unit="°C")

    def temp_rise():
        start = random.randint(-12, -2)
        rise = random.randint(2, 10)
        end = start + rise
        return _iq("The temperature is %d°C, then rises by %d°C. What is the "
                   "new temperature, in °C?" % (start, rise), end,
                   ["%d + %d = %d." % (start, rise, end)], unit="°C")

    def line_add():
        a = random.randint(-8, 8)
        b = random.randint(max(-8, -12 - a), min(8, 12 - a))   # answer stays on the line
        s = a + b
        op = "%d + (%d)" % (a, b) if b < 0 else "%d + %d" % (a, b)
        return _nlq("The number line runs from −12 to 12. Mark the answer to "
                    "%s." % op, s, -12, 12, 1, 4,
                    ["%s = %d." % (op.replace("+ (", "+ ").replace(")", ""), s)])

    def difference():
        a = random.randint(-R, R)
        b = random.randint(-R, R)
        while a == b:
            b = random.randint(-R, R)
        diff = abs(a - b)
        return _iq("How many degrees apart are a temperature of %d°C and a "
                   "temperature of %d°C?" % (a, b), diff,
                   ["The difference is %d − (%d) = %d." % (max(a, b), min(a, b),
                                                           diff)], unit="°C")

    def three_terms():
        a = random.randint(-R, R)
        b = -random.randint(1, R)
        c = random.randint(1, R)
        s = a + b + c
        return _iq("Work out %d + (%d) + %d" % (a, b, c), s,
                   ["Work left to right: %d + (%d) = %d." % (a, b, a + b),
                    "%d + %d = %d." % (a + b, c, s)])

    return _pick_opts({
        0: [add_neg, sub_to_neg, two_neg, temp_change, temp_rise, line_add,
            missing_add],
        1: [add_neg, sub_to_neg, sub_neg, two_neg, missing_add, temp_change,
            temp_rise, line_add, difference],
        2: [sub_neg, two_neg, missing_add, three_terms, temp_rise, difference,
            line_add, add_neg],
    }, d, weighted_tail=[line_add, line_add])


# ============================================================== 8.2.g ========
# DIRECTED NUMBERS — negative answers are EXPECTED here.
@skill("Y8.2.g", "Multiply and divide directed numbers", S2)
def _(d=1):
    d = _t(d)
    R = _by_d(d, 6, 9, 12)

    def neg_times_pos():
        a = -random.randint(2, R)
        b = random.randint(2, R)
        return _iq("Work out (%d) × %d" % (a, b), a * b,
                   ["A negative times a positive is negative.",
                    "(%d) × %d = %d." % (a, b, a * b)])

    def neg_times_neg():
        a = -random.randint(2, R)
        b = -random.randint(2, R)
        return _iq("Work out (%d) × (%d)" % (a, b), a * b,
                   ["A negative times a negative is positive.",
                    "(%d) × (%d) = %d." % (a, b, a * b)])

    def div_neg():
        q = random.randint(2, R)
        b = -random.randint(2, R)
        a = q * b
        return _iq("Work out %d ÷ (%d)" % (a, b), q,
                   ["A negative divided by a negative is positive."
                    if a < 0 else "Divide and apply the sign rule.",
                    "%d ÷ (%d) = %d." % (a, b, q)])

    def pos_div_neg():
        q = -random.randint(2, R)
        b = -random.randint(2, R)
        a = q * b
        return _iq("Work out %d ÷ (%d)" % (a, b), q,
                   ["A positive divided by a negative is negative.",
                    "%d ÷ (%d) = %d." % (a, b, q)])

    def square_neg():
        a = -random.randint(2, R)
        return _iq("Work out (%d)²  (that is (%d) × (%d))." % (a, a, a), a * a,
                   ["A negative squared is positive.",
                    "(%d) × (%d) = %d." % (a, a, a * a)])

    def missing_factor():
        a = -random.randint(2, R)
        b = random.choice([-1, 1]) * random.randint(2, R)
        p = a * b
        return _iq("(%d) × ___ = %d . What is the missing number?" % (a, p), b,
                   ["%d ÷ (%d) = %d." % (p, a, b)])

    def cube_reason():
        a = -random.randint(2, _by_d(d, 3, 4, 5))
        return _iq("Work out (%d)³  (that is (%d) × (%d) × (%d))."
                   % (a, a, a, a), a ** 3,
                   ["(%d) × (%d) = %d." % (a, a, a * a),
                    "%d × (%d) = %d." % (a * a, a, a ** 3)])

    def debt_word():
        who = pick(NAMES)
        each = random.randint(2, 8)
        n = random.randint(3, 6)
        total = -each * n
        return _iq("%s owes £%d to each of %d friends. Written as a directed "
                   "number, what is %s's total balance, in pounds?"
                   % (who, each, n, who), total,
                   ["%d debts of £%d each: %d × (−%d) = %d."
                    % (n, each, n, each, total)], unit="£")

    def two_step():
        a = -random.randint(2, R)
        b = -random.randint(2, R)
        c = random.randint(2, R)
        r = a * b * (-1 if random.random() < 0.5 else 1)
        # keep simple: (a*b)/c exact
        prod = a * b
        c = random.choice([x for x in range(2, R + 1) if prod % x == 0] or [1])
        r = prod // c
        return _iq("Work out (%d) × (%d) ÷ %d" % (a, b, c), r,
                   ["(%d) × (%d) = %d." % (a, b, prod),
                    "%d ÷ %d = %d." % (prod, c, r)])

    def sign_table():
        rows = [["(−1) × (−1)", "1"], ["(−1) × (+1)", "−1"],
                ["(−1) × (−1) × (−1)", ""]]
        return _dtq("The table shows what happens to the sign. Complete the "
                    "last row: what is (−1) × (−1) × (−1)?",
                    ["Product", "Result"], rows, -1, "int",
                    ["Three negative factors give a negative result.",
                     "(−1) × (−1) × (−1) = −1."], missing=(2, 1))

    def neg_mult_number_line():
        # Understand multiplying by a negative integer using a number line.
        a = random.randint(2, _by_d(d, 4, 5, 6))   # size of each jump
        w = random.randint(2, _by_d(d, 3, 4, 5))    # number of jumps
        prod = -(a * w)
        lo = prod - a                               # multiple of a, room below
        hi = a
        return _nlq(
            "Multiplying by a negative integer: on the number line, start at 0 "
            "and make %d equal jumps of −%d (each jump goes to the left). Mark "
            "the answer to %d × (−%d)." % (w, a, w, a),
            prod, lo, hi, 1, a,
            ["%d jumps of −%d from 0 land on %d." % (w, a, prod),
             "So %d × (−%d) = %d." % (w, a, prod)])

    return _pick_opts({
        0: [neg_times_pos, neg_times_neg, div_neg, square_neg, missing_factor,
            debt_word, neg_mult_number_line],
        1: [neg_times_pos, neg_times_neg, div_neg, pos_div_neg, square_neg,
            missing_factor, debt_word, sign_table, neg_mult_number_line],
        2: [neg_times_neg, pos_div_neg, square_neg, cube_reason, missing_factor,
            two_step, sign_table, div_neg, neg_mult_number_line],
    }, d, weighted_tail=[sign_table, neg_mult_number_line])


# ============================================================== 8.2.h ========
# RATIONAL NUMBERS — positive/negative fractions and decimals; negatives OK.
@skill("Y8.2.h", "Four operations with rational numbers", S2)
def _(d=1):
    d = _t(d)

    def dec_add_neg():
        a = _mk(1, 12, 85)
        b = _mk(1, 12, 85)
        # a + (-b) -> may be negative
        r = a - b
        return _nq("Work out %s + (−%s)" % (_txt(a), _txt(b)), r,
                   ["Adding a negative means subtracting: %s − %s."
                    % (_txt(a), _txt(b)),
                    "= %s." % _txt(r)])

    def dec_sub_bigger():
        a = _mk(1, 12, 40)
        b = _mk(1, 45, 85)
        r = a - b
        return _nq("Work out %s − %s" % (_txt(a), _txt(b)), r,
                   ["The result is below zero.",
                    "%s − %s = %s." % (_txt(a), _txt(b), _txt(r))])

    def neg_dec_times():
        a = _mk(1, 2, 9)
        k = random.randint(2, 6)
        r = -a * k
        return _nq("Work out (−%s) × %d" % (_txt(a), k), r,
                   ["Negative × positive = negative.",
                    "(−%s) × %d = %s." % (_txt(a), k, _txt(r))])

    def frac_add_neg():
        den = pick([3, 4, 5, 6, 8])
        a, b = random.sample(range(1, den), 2)  # a != b, so num != 0
        # a/den + (-b/den) = (a-b)/den, may be negative
        num = a - b
        sn, sd = _simp(abs(num), den)
        sn = sn if num > 0 else -sn
        return _fq("Work out %d/%d + (−%d/%d). Give your answer as a fraction."
                   % (a, den, b, den), sn, sd,
                   ["Same denominator: (%d − %d)/%d = %d/%d."
                    % (a, b, den, num, den),
                    "In simplest form that is %s." % _mixed_str(0, sn, sd)])

    def frac_times_neg():
        n1, dd1 = 1, pick([2, 3, 4, 5])
        n2, dd2 = 1, pick([2, 3, 4, 5])
        num = -(n1 * n2)
        den = dd1 * dd2
        sn, sd = _simp(abs(num), den)
        return _fq("Work out (−1/%d) × 1/%d. Give your answer as a fraction."
                   % (dd1, dd2), -sn, sd,
                   ["Multiply tops and bottoms: −1/%d." % den,
                    "In simplest form: −%s." % _mixed_str(0, sn, sd)])

    def neg_frac_of():
        den = pick([2, 4, 5, 10])
        num = 1
        whole = pick([20, 40, 60, 80, 100])
        val = -(whole // den) * num
        return _iq("Work out (−1/%d) × %d" % (den, whole), val,
                   ["%d ÷ %d = %d, then apply the negative sign."
                    % (whole, den, whole // den),
                    "= %d." % val])

    def dec_div_neg():
        b = -random.randint(2, 6)
        q = _mk(1, 12, 45)
        a = -q * b                      # positive dividend, negative divisor
        return _nq("Work out %s ÷ (%d)" % (_txt(a), b), -q,
                   ["Positive ÷ negative = negative.",
                    "%s ÷ (%d) = %s." % (_txt(a), b, _txt(-q))])

    def compare_rational():
        a = _mk(1, -40, 40)
        # ensure negative sometimes
        a = _D(random.randint(-40, 40)).scaleb(-1)
        b = _D(random.randint(-40, 40)).scaleb(-1)
        while a == b:
            b = _D(random.randint(-40, 40)).scaleb(-1)
        big = a if a > b else b
        bigger = _txt(big)
        return _nq("Which is larger: %s or %s? Type the number."
                   % (_txt(a), _txt(b)), big,
                   ["On a number line, %s is further right." % bigger],
                   text=True, placeholder="a number")

    def mixed_two_step():
        a = _mk(1, 12, 45)
        b = _mk(1, 12, 45)
        k = random.randint(2, 4)
        r = (a - b) * k  # a<b sometimes -> negative
        # force a<b for a negative bracket often
        if random.random() < 0.5 and a > b:
            a, b = b, a
        r = (a - b) * k
        return _nq("Work out (%s − %s) × %d" % (_txt(a), _txt(b), k), r,
                   ["Brackets first: %s − %s = %s."
                    % (_txt(a), _txt(b), _txt(a - b)),
                    "× %d = %s." % (k, _txt(r))])

    def line_neg():
        a = _D(random.randint(-70, 70)).scaleb(-1)
        b = _D(random.randint(10, min(70, int(a * 10) + 80))).scaleb(-1)
        r = a - b  # a + (-b), may be negative; stays on the −8..8 line
        return _nlq("The number line runs from −8 to 8 in tenths. Mark the "
                    "answer to %s + (−%s)." % (_txt(a), _txt(b)), r, -8, 8,
                    Decimal("0.1"), Decimal("1"),
                    ["%s − %s = %s." % (_txt(a), _txt(b), _txt(r))],
                    tol=0.05)

    def eval_expr_integers():
        # Evaluate numerical expressions involving integers (BIDMAS; negatives OK).
        a = random.randint(-9, 9)
        b = random.randint(2, 8)
        c = random.randint(-8, -2)
        form = random.randint(0, 2)
        if form == 0:
            res = a + b * c
            expr = "%d + %d × (%d)" % (a, b, c)
            sol = ["Multiply first (BIDMAS): %d × (%d) = %d." % (b, c, b * c),
                   "%d + (%d) = %d." % (a, b * c, res)]
        elif form == 1:
            res = a - b * c
            expr = "%d − %d × (%d)" % (a, b, c)
            sol = ["Multiply first: %d × (%d) = %d." % (b, c, b * c),
                   "%d − (%d) = %d." % (a, b * c, res)]
        else:
            res = (a + c) * b
            expr = "(%d + (%d)) × %d" % (a, c, b)
            sol = ["Brackets first: %d + (%d) = %d." % (a, c, a + c),
                   "%d × %d = %d." % (a + c, b, res)]
        return _iq("Evaluate this numerical expression involving integers: %s ."
                   % expr, res, sol)

    def mul_div_signed_fractions():
        # Multiply and divide positive and negative fractions.
        d1 = pick([2, 3, 4, 5])
        n1 = random.randint(1, d1 - 1)
        d2 = pick([2, 3, 4, 5])
        n2 = random.randint(1, d2 - 1)
        s1 = random.choice([1, -1])
        s2 = random.choice([1, -1])
        A = Fraction(s1 * n1, d1)
        B = Fraction(s2 * n2, d2)
        if random.random() < 0.5:
            res, op = A * B, "×"
        else:
            res, op = A / B, "÷"
        f1 = _fracstr(A)
        f2 = "(%s)" % _fracstr(B)
        base = ("Multiply and divide positive and negative fractions. Work out "
                "%s %s %s." % (f1, op, f2))
        sol = ["Apply the sign rule, then %s the fractions."
               % ("multiply" if op == "×" else "divide"),
               "%s %s %s = %s." % (f1, op, f2, _fracstr(res))]
        return _frac_result_q(base, res, sol)

    def rational_four_ops():
        # Add, subtract, multiply and divide rational numbers (signed fractions).
        d1 = pick([2, 3, 4, 5])
        n1 = random.randint(1, d1 - 1)
        d2 = pick([2, 3, 4, 5])
        n2 = random.randint(1, d2 - 1)
        A = Fraction(random.choice([1, -1]) * n1, d1)
        B = Fraction(random.choice([1, -1]) * n2, d2)
        op = pick(["+", "−", "×", "÷"])
        res = {"+": A + B, "−": A - B, "×": A * B, "÷": A / B}[op]
        fa = _fracstr(A)
        fb = "(%s)" % _fracstr(B)
        base = ("Add, subtract, multiply and divide rational numbers. These are "
                "rational numbers: work out %s %s %s." % (fa, op, fb))
        sol = ["Work with the signed rational numbers carefully.",
               "%s %s %s = %s." % (fa, op, fb, _fracstr(res))]
        return _frac_result_q(base, res, sol)

    def evaluate_rational_expr():
        # Evaluate numerical expressions involving rational numbers (BIDMAS).
        d1 = pick([2, 3, 4])
        n1 = random.randint(1, d1 - 1)
        d2 = pick([2, 3, 4])
        n2 = random.randint(1, d2 - 1)
        d3 = pick([2, 3, 4])
        n3 = random.randint(1, d3 - 1)
        A = Fraction(random.choice([1, -1]) * n1, d1)
        B = Fraction(n2, d2)
        C = Fraction(random.choice([1, -1]) * n3, d3)
        res = A + B * C
        expr = "%s + %s × (%s)" % (_fracstr(A), _fracstr(B), _fracstr(C))
        base = ("Evaluate this numerical expression involving rational numbers: "
                "%s ." % expr)
        sol = ["Multiply before adding (BIDMAS): %s × %s = %s."
               % (_fracstr(B), _fracstr(C), _fracstr(B * C)),
               "Then %s + %s = %s."
               % (_fracstr(A), _fracstr(B * C), _fracstr(res))]
        return _frac_result_q(base, res, sol)

    return _pick_opts({
        0: [dec_add_neg, dec_sub_bigger, neg_dec_times, neg_frac_of,
            compare_rational, frac_add_neg, line_neg, eval_expr_integers,
            mul_div_signed_fractions, rational_four_ops, evaluate_rational_expr],
        1: [dec_add_neg, dec_sub_bigger, neg_dec_times, frac_add_neg,
            neg_frac_of, dec_div_neg, compare_rational, frac_times_neg,
            line_neg, eval_expr_integers, mul_div_signed_fractions,
            rational_four_ops, evaluate_rational_expr],
        2: [dec_sub_bigger, neg_dec_times, frac_add_neg, frac_times_neg,
            dec_div_neg, mixed_two_step, compare_rational, line_neg,
            eval_expr_integers, mul_div_signed_fractions, rational_four_ops,
            evaluate_rational_expr],
    }, d, weighted_tail=[eval_expr_integers, mul_div_signed_fractions,
                         rational_four_ops, evaluate_rational_expr])


# ============================================================== 8.2.i ========
@skill("Y8.2.i", "Decimal and multi-step number problems", S2)
def _(d=1):
    d = _t(d)

    def best_buy():
        # two pack sizes, find cheaper per unit (whole-penny unit prices)
        u1 = random.randint(20, 60)
        u2 = random.randint(20, 60)
        while u2 == u1:
            u2 = random.randint(20, 60)
        n1 = random.choice([4, 5, 6])
        n2 = random.choice([4, 5, 6])
        p1, p2 = u1 * n1, u2 * n2
        cheaper = "A" if u1 < u2 else "B"
        return _sq("Pack A has %d items for %s. Pack B has %d items for %s. "
                   "Which pack is better value per item? Type A or B."
                   % (n1, _lb(p1), n2, _lb(p2)), cheaper,
                   placeholder="A or B",
                   solution=["Pack A: %s each. Pack B: %s each."
                             % (_lb(u1), _lb(u2)),
                             "Pack %s is cheaper per item." % cheaper])

    def total_and_change():
        items = random.sample(_SHOP, 3)
        ps = [random.randint(90, 420) for _ in range(3)]
        tot = sum(ps)
        paid = (tot // 100 + 1 + random.randint(1, 6)) * 100
        change = paid - tot
        return _nq("A shopper buys a %s (%s), a %s (%s) and a %s (%s), paying "
                   "with %s. How much change is given? Give your answer in "
                   "pounds." % (items[0], _lb(ps[0]), items[1], _lb(ps[1]),
                                items[2], _lb(ps[2]), _lb(paid)),
                   _D(change) / 100, unit="£",
                   solution=["Total = %s." % _lb(tot),
                    "%s − %s = %s." % (_lb(paid), _lb(tot), _lb(change))])

    def petrol_cost():
        litres = _mk(1, 201, 480)
        ppl = random.randint(140, 175)
        cost = _rnd(_D(litres) * _D(ppl) / 100, 2)
        return _nq("Fuel costs %s per litre. What does %s litres cost, to the "
                   "nearest penny? Give your answer in pounds."
                   % (_lb(ppl), _txt(litres)), cost, unit="£",
                   solution=["%s × %s ≈ %s." % (_txt(litres), _lb(ppl),
                                       _lb(int(cost * 100)))])

    def perimeter_two():
        L = _mk(1, 25, 85)
        W = _mk(1, 12, 40)
        p = (L + W) * 2
        return _nq("A rectangular garden is %s m long and %s m wide. A fence "
                   "runs all the way round it. How long is the fence, in "
                   "metres?" % (_txt(L), _txt(W)), p, unit="m",
                   solution=["Perimeter = 2 × (%s + %s) = %s m."
                    % (_txt(L), _txt(W), _txt(p))])

    def how_many_fit():
        cash = random.randint(15, 40)
        price = random.randint(120, 380)
        n = (cash * 100) // price
        return _iq("A %s costs %s. What is the greatest number that can be "
                   "bought with £%d?" % (pick(_SHOP), _lb(price), cash), n,
                   ["£%d = %dp." % (cash, cash * 100),
                    "%d ÷ %d = %d (whole items)."
                    % (cash * 100, price, n)], unit="items")

    def split_bill():
        n = random.randint(3, 6)
        each = random.randint(150, 480)
        total = each * n
        return _nq("A bill of %s is split equally between %d people. How much "
                   "does each pay? Give your answer in pounds."
                   % (_lb(total), n), _D(each) / 100, unit="£",
                   solution=["%s ÷ %d = %s." % (_lb(total), n, _lb(each))])

    def mass_leftover():
        bag = _mk(1, 45, 95)
        used = _mk(1, 12, 40)
        while used * 2 == bag:                        # half used would leave the shown number
            used = _mk(1, 12, 40)
        left = bag - used
        return _nq("A bag holds %s kg of flour. %s kg is used. How much is "
                   "left, in kg?" % (_txt(bag), _txt(used)), left, unit="kg",
                   solution=["%s − %s = %s kg." % (_txt(bag), _txt(used), _txt(left))])

    def rate_table():
        each = random.randint(120, 320)
        ns = [1, 3, 5]
        rows = [[str(nn), _lb(each * nn)] for nn in ns]
        k = random.randint(1, 2)
        ans = _D(each * ns[k]) / 100
        rows[k][1] = ""
        return _dtq("The tickets all cost the same. Complete the missing cost, "
                    "in pounds.", ["Tickets", "Cost"], rows, _fl(ans), "num",
                    ["One ticket costs %s." % _lb(each),
                     "%d × %s = %s." % (ns[k], _lb(each), _lb(each * ns[k]))],
                    missing=(k, 1), tol=1e-6, placeholder="£")

    def double_discount():
        price = random.randint(20, 40) * 100
        off = random.choice([2, 3, 5]) * 100
        n = random.randint(2, 3)
        pay = (price - off) * n
        return _nq("A jacket normally costs %s but has %s off. How much do %d "
                   "jackets cost at the reduced price? Give your answer in "
                   "pounds." % (_lb(price), _lb(off), n), _D(pay) / 100,
                   unit="£",
                   solution=["Reduced price = %s − %s = %s."
                    % (_lb(price), _lb(off), _lb(price - off)),
                    "%d × %s = %s." % (n, _lb(price - off), _lb(pay))])

    return _pick_opts({
        0: [total_and_change, perimeter_two, split_bill, mass_leftover,
            rate_table, how_many_fit],
        1: [best_buy, total_and_change, perimeter_two, how_many_fit,
            split_bill, mass_leftover, rate_table, double_discount],
        2: [best_buy, total_and_change, petrol_cost, how_many_fit,
            double_discount, perimeter_two, rate_table, split_bill],
    }, d, weighted_tail=[rate_table, rate_table])


# ============================================================== 8.3.a ========
@skill("Y8.3.a", "Simplify and find equivalent fractions", S3)
def _(d=1):
    d = _t(d)

    def _unsimplified():
        base_d = pick([2, 3, 4, 5, 6, 8])
        base_n = random.randint(1, base_d - 1)
        while _hcf(base_n, base_d) != 1:        # 2/6 is not in simplest form
            base_n = random.randint(1, base_d - 1)
        k = random.randint(*_by_d(d, (2, 4), (2, 6), (3, 9)))
        return base_n, base_d, base_n * k, base_d * k

    def simp_num():
        bn, bd, n, dd = _unsimplified()
        return _iq("Write %d/%d in its simplest form. Type the NUMERATOR of the "
                   "simplified fraction." % (n, dd), bn,
                   ["The HCF of %d and %d is %d." % (n, dd, _hcf(n, dd)),
                    "%d ÷ %d = %d, so the numerator is %d."
                    % (n, _hcf(n, dd), bn, bn)])

    def simp_den():
        bn, bd, n, dd = _unsimplified()
        return _iq("Write %d/%d in its simplest form. Type the DENOMINATOR of "
                   "the simplified fraction." % (n, dd), bd,
                   ["Divide both by the HCF, %d." % _hcf(n, dd),
                    "%d ÷ %d = %d." % (dd, _hcf(n, dd), bd)])

    def equiv_num():
        bn, bd = random.randint(1, 4), pick([2, 3, 4, 5])
        while bn >= bd:
            bn = random.randint(1, bd - 1)
        k = random.randint(2, _by_d(d, 4, 6, 9))
        return _iq("Fill in the missing number:  %d/%d = ___/%d"
                   % (bn, bd, bd * k), bn * k,
                   ["The denominator was multiplied by %d." % k,
                    "So the numerator is %d × %d = %d." % (bn, k, bn * k)])

    def equiv_den():
        bn, bd = random.randint(1, 4), pick([2, 3, 4, 5])
        while bn >= bd:
            bn = random.randint(1, bd - 1)
        k = random.randint(2, _by_d(d, 4, 6, 9))
        return _iq("Fill in the missing number:  %d/%d = %d/___"
                   % (bn, bd, bn * k), bd * k,
                   ["The numerator was multiplied by %d." % k,
                    "So the denominator is %d × %d = %d." % (bd, k, bd * k)])

    def is_simplest():
        if random.random() < 0.5:
            n, dd = random.randint(1, 6), pick([7, 9, 11, 13])
            while _hcf(n, dd) != 1 or n >= dd:
                n = random.randint(1, dd - 1)
            return _sq("Is %d/%d already in its simplest form? Type yes or no."
                       % (n, dd), "yes", placeholder="yes or no",
                       solution=["%d and %d share no common factor above 1."
                                 % (n, dd),
                                 "So %d/%d is already simplest." % (n, dd)])
        bn, bd, n, dd = _unsimplified()
        return _sq("Is %d/%d already in its simplest form? Type yes or no."
                   % (n, dd), "no", placeholder="yes or no",
                   solution=["%d and %d share the common factor %d."
                             % (n, dd, _hcf(n, dd)),
                             "It simplifies to %d/%d, so no." % (bn, bd)])

    def bar_equiv():
        parts = pick([4, 6, 8])
        shaded = random.randint(1, parts - 1)
        sn, sd = _simp(shaded, parts)
        return _fbq("Shade %d of the %d equal parts, then read off the shaded "
                    "fraction." % (shaded, parts), parts, shaded,
                    ["%d out of %d parts is shaded." % (shaded, parts),
                     "That is %d/%d, or %d/%d in simplest form."
                     % (shaded, parts, sn, sd)])

    def grid_read():
        bn, bd, n, dd = _unsimplified()
        # use area grid with parts <= 100 to read the simplified numerator
        parts = pick([8, 10, 12])
        shaded = random.randint(1, parts - 1)
        sn, sd = _simp(shaded, parts)
        return _agread("The grid shows %d of %d squares shaded. In simplest "
                       "form, what is the shaded fraction? Type the numerator."
                       % (shaded, parts), parts, shaded, sn, "int",
                       ["%d/%d = %d/%d." % (shaded, parts, sn, sd),
                        "The simplest numerator is %d." % sn])

    def which_equiv():
        bn, bd = 3, 4
        bn, bd = random.choice([(2, 3), (3, 4), (2, 5), (3, 5), (5, 6)])
        good = (bn * 2, bd * 2)
        bads = [(bn + 1, bd + 1), (bn, bd + 2), (bn + 2, bd)]
        rows = [["%d/%d" % good], ["%d/%d" % bads[0]], ["%d/%d" % bads[1]]]
        random.shuffle(rows)
        return _dtq("Which fraction in the table is equivalent to %d/%d? Type "
                    "it exactly as it appears in the table." % (bn, bd),
                    ["Fraction"], rows, "%d/%d" % good, "str",
                    ["%d/%d = %d/%d (both parts doubled)."
                     % (bn, bd, good[0], good[1])],
                    placeholder="e.g. 1/2")

    def word_simplify():
        who = pick(NAMES)
        bd = pick([2, 4, 5])
        bn = 1
        k = random.choice([4, 5, 6])
        n, dd = bn * k, bd * k
        return _iq("In a class of %d pupils, %d walk to school. Write the "
                   "fraction who walk in its simplest form and type the "
                   "denominator." % (dd, n), bd,
                   ["%d/%d simplifies by dividing by %d."
                    % (n, dd, _hcf(n, dd)),
                    "It becomes %d/%d." % (bn, bd)])

    return _pick_opts({
        0: [simp_num, equiv_num, equiv_den, is_simplest, bar_equiv, grid_read],
        1: [simp_num, simp_den, equiv_num, equiv_den, is_simplest, bar_equiv,
            which_equiv, word_simplify],
        2: [simp_num, simp_den, equiv_num, equiv_den, is_simplest, which_equiv,
            grid_read, word_simplify],
    }, d, weighted_tail=[bar_equiv, grid_read, which_equiv])


# ============================================================== 8.3.b ========
@skill("Y8.3.b", "Mixed numbers and improper fractions", S3)
def _(d=1):
    d = _t(d)

    def _mixed():
        w = random.randint(*_by_d(d, (1, 3), (2, 5), (3, 8)))
        dd = pick([2, 3, 4, 5, 6, 8])
        n = random.randint(1, dd - 1)
        while _hcf(n, dd) != 1:         # keep the fraction part in lowest terms
            n = random.randint(1, dd - 1)
        return w, n, dd

    def imp_to_mixed():
        w, n, dd = _mixed()
        imp = w * dd + n
        return _mixq("Write %d/%d as a mixed number." % (imp, dd), w, n, dd,
                     solution=["%d ÷ %d = %d remainder %d."
                               % (imp, dd, w, n),
                               "So %d/%d = %s." % (imp, dd, _mixed_str(w, n,
                                                                       dd))])

    def mixed_to_imp_num():
        w, n, dd = _mixed()
        imp = w * dd + n
        return _iq("Write %s as an improper fraction over %d. Type the "
                   "NUMERATOR." % (_mixed_str(w, n, dd), dd), imp,
                   ["%d × %d + %d = %d." % (w, dd, n, imp),
                    "So %s = %d/%d." % (_mixed_str(w, n, dd), imp, dd)])

    def mixed_to_imp_frac():
        w, n, dd = _mixed()
        imp = w * dd + n
        return _fq("Write %s as an improper fraction." % _mixed_str(w, n, dd),
                   imp, dd,
                   ["%d × %d + %d = %d." % (w, dd, n, imp),
                    "So %s = %d/%d." % (_mixed_str(w, n, dd), imp, dd)])

    def whole_part():
        w, n, dd = _mixed()
        imp = w * dd + n
        return _iq("What is the whole-number part of %d/%d when it is written "
                   "as a mixed number?" % (imp, dd), w,
                   ["%d ÷ %d = %d remainder %d." % (imp, dd, w, n),
                    "The whole-number part is %d." % w])

    def is_improper():
        if random.random() < 0.5:
            top = random.randint(6, 15)
            bot = random.randint(2, top - 1)
            ans = "yes"
        else:
            bot = random.randint(4, 9)
            top = random.randint(1, bot - 1)
            ans = "no"
        return _sq("Is %d/%d an improper fraction (top heavier than bottom)? "
                   "Type yes or no." % (top, bot), ans,
                   placeholder="yes or no",
                   solution=["An improper fraction has numerator ≥ "
                             "denominator.",
                             "%d %s %d, so the answer is %s."
                             % (top, "≥" if ans == "yes" else "<", bot, ans)])

    def line_mark():
        w, n, dd = _mixed()
        dd = pick([2, 3, 4])
        n = random.randint(1, dd - 1)
        w = random.randint(1, 3)
        val = w + Fraction(n, dd)
        top = 4
        return _nlq("The number line is marked in %s. Mark %s on it."
                    % (_ths(dd), _mixed_str(w, n, dd)), _fl(val), 0, top,
                    Fraction(1, dd), 1,
                    ["%s is %d whole and %d/%d more." % (_mixed_str(w, n, dd),
                                                         w, n, dd)])

    def simplify_mixed():
        w = random.randint(1, 4)
        dd = pick([4, 6, 8])
        n = random.choice([x for x in range(2, dd) if _hcf(x, dd) > 1])
        sn, sd = _simp(n, dd)
        return _mixq("Write %s with its fraction part in simplest form."
                     % _mixed_str(w, n, dd), w, sn, sd,
                     solution=["%d/%d = %d/%d." % (n, dd, sn, sd),
                               "So %s = %s." % (_mixed_str(w, n, dd),
                                                _mixed_str(w, sn, sd))])

    def add_to_whole():
        w, n, dd = _mixed()
        need = dd - n
        return _fq("What must be added to %s to make the next whole number, "
                   "%d? Give your answer as a fraction."
                   % (_mixed_str(w, n, dd), w + 1), need, dd,
                   ["%d/%d + %d/%d = %d/%d = 1." % (n, dd, need, dd, dd, dd),
                    "So add %d/%d." % (need, dd)])

    def count_halves():
        dd = pick([2, 3, 4])
        w = random.randint(1, 4)
        n = random.randint(1, dd - 1)
        imp = w * dd + n
        return _iq("How many %s are there in %s altogether?"
                   % (_ths(dd), _mixed_str(w, n, dd)), imp,
                   ["Each whole is %d %s, so %d %s %d."
                    % (dd, _ths(dd), w, "whole is" if w == 1 else "wholes are", w * dd),
                    "%d + %d = %d %s." % (w * dd, n, imp, _ths(dd))])

    return _pick_opts({
        0: [imp_to_mixed, mixed_to_imp_num, whole_part, is_improper, line_mark,
            count_halves],
        1: [imp_to_mixed, mixed_to_imp_num, mixed_to_imp_frac, whole_part,
            is_improper, line_mark, add_to_whole, count_halves],
        2: [imp_to_mixed, mixed_to_imp_frac, whole_part, simplify_mixed,
            add_to_whole, count_halves, line_mark, mixed_to_imp_num],
    }, d, weighted_tail=[line_mark, line_mark])


# ============================================================== 8.3.c ========
@skill("Y8.3.c", "Compare and order fractions and mixed numbers", S3)
def _(d=1):
    d = _t(d)

    def compare_two():
        dens = pick([(3, 4), (2, 5), (4, 6), (3, 8), (5, 6), (2, 3)])
        d1, d2 = dens
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        while f1 == f2:
            n2 = random.randint(1, d2 - 1)
            f2 = Fraction(n2, d2)
        bigger = "%d/%d" % (n1, d1) if f1 > f2 else "%d/%d" % (n2, d2)
        L = _lcm(d1, d2)
        return _sq("Which is larger: %d/%d or %d/%d? Type the larger fraction."
                   % (n1, d1, n2, d2), bigger,
                   placeholder="e.g. %d/%d" % (n1, d1),
                   solution=["Common denominator %d: %d/%d and %d/%d."
                             % (L, n1 * (L // d1), L, n2 * (L // d2), L),
                             "The larger is %s." % bigger])

    def insert_symbol():
        d1, d2 = pick([(3, 4), (2, 5), (5, 6), (3, 8), (2, 3)])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        if f1 == f2:
            sym = "="
        else:
            sym = "<" if f1 < f2 else ">"
        return _sq("Put the correct symbol between the fractions:  %d/%d ___ "
                   "%d/%d . Type <, > or =." % (n1, d1, n2, d2), sym,
                   placeholder="< , > or =",
                   solution=["Compare using a common denominator.",
                             "%d/%d %s %d/%d." % (n1, d1, sym, n2, d2)])

    def order_set():
        dens = [2, 3, 4, 6]
        fr = []
        seen = set()
        while len(fr) < _by_d(d, 3, 4, 4):
            dd = pick(dens)
            n = random.randint(1, dd - 1)
            f = Fraction(n, dd)
            if f in seen:
                continue
            seen.add(f)
            fr.append((n, dd, f))
        fr_sorted = sorted(fr, key=lambda x: x[2])
        vals = ["%d/%d" % (n, dd) for n, dd, _ in fr_sorted]
        shown = ["%d/%d" % (n, dd) for n, dd, _ in fr]
        return {"prompt": "Write these fractions in order from smallest to "
                          "largest, separated by commas:  %s"
                          % ", ".join(shown),
                "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 1/4, 1/2, 3/4"},
                "answer": ", ".join(vals), "answer_type": "str", "tolerance": 0,
                "solution": ["Use a common denominator to compare.",
                             "In order: %s." % ", ".join(vals)]}

    def compare_mixed():
        w = random.randint(2, 5)
        d1, d2 = pick([(3, 4), (2, 5), (5, 6), (3, 8)])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        f1 = w + Fraction(n1, d1)
        f2 = w + Fraction(n2, d2)
        while f1 == f2:
            n2 = random.randint(1, d2 - 1)
            f2 = w + Fraction(n2, d2)
        bigger = _mixed_str(w, n1, d1) if f1 > f2 else _mixed_str(w, n2, d2)
        return _sq("Which mixed number is larger: %s or %s? Type it."
                   % (_mixed_str(w, n1, d1), _mixed_str(w, n2, d2)), bigger,
                   placeholder="e.g. 2 3/4",
                   solution=["The whole parts are equal, so compare the "
                             "fractions %d/%d and %d/%d." % (n1, d1, n2, d2),
                             "The larger number is %s." % bigger])

    def between():
        dd = pick([4, 6, 8])
        return _fq("Write a fraction that lies exactly halfway between 0 and "
                   "1/%d. Give it as a fraction." % dd, 1, dd * 2,
                   ["Halfway is 1/%d ÷ 2 = 1/%d." % (dd, dd * 2)])

    def compare_to_half():
        dd = pick([5, 6, 8, 10])
        n = random.randint(1, dd - 1)
        f = Fraction(n, dd)
        if f == Fraction(1, 2):
            n = 1
            f = Fraction(1, dd)
        sym = "less than" if f < Fraction(1, 2) else "more than"
        return _sq("Is %d/%d less than or more than one half? Type 'less than' "
                   "or 'more than'." % (n, dd), sym,
                   placeholder="less than / more than",
                   solution=["Half of %d is %.1f; the numerator is %d."
                             % (dd, dd / 2, n),
                             "So %d/%d is %s one half." % (n, dd, sym)])

    def line_place():
        dd = pick([4, 5, 6, 8])
        n = random.randint(1, dd - 1)
        return _nlq("The number line runs from 0 to 1 in %s. Mark %d/%d."
                    % (_ths(dd), n, dd), _fl(Fraction(n, dd)), 0, 1,
                    Fraction(1, dd), 1,
                    ["%d/%d is %d step(s) of 1/%d from 0." % (n, dd, n, dd)])

    def largest_of_three():
        items = []
        seen = set()
        while len(items) < 3:
            dd = pick([2, 3, 4, 5, 6])
            n = random.randint(1, dd - 1)
            f = Fraction(n, dd)
            if f in seen:
                continue
            seen.add(f)
            items.append((n, dd, f))
        big = max(items, key=lambda x: x[2])
        return _sq("Which of these is the largest:  %s? Type it as a fraction."
                   % ", ".join("%d/%d" % (n, dd) for n, dd, _ in items),
                   "%d/%d" % (big[0], big[1]),
                   placeholder="e.g. 3/4",
                   solution=["Compare with a common denominator.",
                             "The largest is %d/%d." % (big[0], big[1])])

    return _pick_opts({
        0: [compare_two, insert_symbol, compare_to_half, line_place,
            largest_of_three, between],
        1: [compare_two, insert_symbol, order_set, compare_mixed,
            compare_to_half, line_place, largest_of_three, between],
        2: [insert_symbol, order_set, compare_mixed, between, compare_to_half,
            largest_of_three, line_place, compare_two],
    }, d, weighted_tail=[line_place, line_place])


# ============================================================== 8.3.d ========
@skill("Y8.3.d", "Convert between fractions and decimals", S3)
def _(d=1):
    d = _t(d)

    def frac_to_dec():
        dd = pick(_by_d(d, [2, 4, 5, 10], [2, 4, 5, 8, 10, 20],
                        [8, 16, 20, 25, 40, 50]))
        n = random.randint(1, dd - 1)
        dec = _frac_to_dec(n, dd)
        return _nq("Write %d/%d as a decimal." % (n, dd), dec,
                   ["%d ÷ %d = %s." % (n, dd, _txt(dec))])

    def dec_to_frac_num():
        dd = pick([2, 4, 5, 8, 10, 20, 25])
        bn = random.randint(1, dd - 1)
        while _hcf(bn, dd) != 1:
            bn = random.randint(1, dd - 1)
        dec = _frac_to_dec(bn, dd)
        return _iq("Write %s as a fraction in its simplest form. Type the "
                   "NUMERATOR." % _txt(dec), bn,
                   ["%s = %d/%d in simplest form." % (_txt(dec), bn, dd),
                    "The numerator is %d." % bn])

    def dec_to_frac_den():
        dd = pick([2, 4, 5, 8, 20, 25])
        bn = random.randint(1, dd - 1)
        while _hcf(bn, dd) != 1:
            bn = random.randint(1, dd - 1)
        dec = _frac_to_dec(bn, dd)
        return _iq("Write %s as a fraction in its simplest form. Type the "
                   "DENOMINATOR." % _txt(dec), dd,
                   ["%s = %d/%d in simplest form." % (_txt(dec), bn, dd),
                    "The denominator is %d." % dd])

    def tenths_hundredths():
        dd = pick([10, 100])
        n = random.randint(1, dd - 1)
        dec = _frac_to_dec(n, dd)
        return _nq("Write %d/%d as a decimal." % (n, dd), dec,
                   ["%d out of %d = %s." % (n, dd, _txt(dec))])

    def common_equiv():
        pairs = [(1, 2, "0.5"), (1, 4, "0.25"), (3, 4, "0.75"), (1, 5, "0.2"),
                 (2, 5, "0.4"), (1, 10, "0.1"), (1, 8, "0.125"), (3, 5, "0.6")]
        n, dd, dec = pick(pairs)
        return _nq("Recall the common equivalent: what is %d/%d as a decimal?"
                   % (n, dd), Decimal(dec),
                   ["%d/%d = %s." % (n, dd, dec)])

    def mixed_to_dec():
        w = random.randint(1, 5)
        dd = pick([2, 4, 5, 10])
        n = random.randint(1, dd - 1)
        while _hcf(n, dd) != 1:
            n = random.randint(1, dd - 1)
        dec = _D(w) + _frac_to_dec(n, dd)
        return _nq("Write the mixed number %s as a decimal."
                   % _mixed_str(w, n, dd), dec,
                   ["%d/%d = %s." % (n, dd, _txt(_frac_to_dec(n, dd))),
                    "So %s = %s." % (_mixed_str(w, n, dd), _txt(dec))])

    def grid_convert():
        n = random.randint(1, 99)
        dec = _frac_to_dec(n, 100)
        return _agread("The hundredths grid shows %d of 100 squares shaded. "
                       "Write the shaded amount as a decimal." % n, 100, n,
                       _fl(dec), "num", ["%d/100 = %s." % (n, _txt(dec))],
                       placeholder="e.g. 0.37", tol=1e-6)

    def which_bigger():
        dd = pick([4, 5, 8, 20])
        n = random.randint(1, dd - 1)
        while _hcf(n, dd) != 1:
            n = random.randint(1, dd - 1)
        f = _frac_to_dec(n, dd)
        dec = _mk(2, 5, 95)
        while dec == f:
            dec = _mk(2, 5, 95)
        bigger = "%d/%d" % (n, dd) if f > dec else _txt(dec)
        return _sq("Which is larger, the fraction %d/%d or the decimal %s? Type "
                   "the larger one." % (n, dd, _txt(dec)), bigger,
                   placeholder="a fraction or a decimal",
                   solution=["%d/%d = %s as a decimal." % (n, dd, _txt(f)),
                             "The larger value is %s." % bigger])

    def table_fill():
        rows_data = [(1, 2), (1, 4), (3, 4), (1, 5)]
        pick_row = random.randrange(len(rows_data))
        rows = []
        for i, (n, dd) in enumerate(rows_data):
            dec = _txt(_frac_to_dec(n, dd))
            rows.append(["%d/%d" % (n, dd),
                         "" if i == pick_row else dec])
        n, dd = rows_data[pick_row]
        ans = _frac_to_dec(n, dd)
        return _dtq("Complete the conversion table: write %d/%d as a decimal."
                    % (n, dd), ["Fraction", "Decimal"], rows, _fl(ans), "num",
                    ["%d ÷ %d = %s." % (n, dd, _txt(ans))],
                    missing=(pick_row, 1), tol=1e-6, placeholder="a decimal")

    return _pick_opts({
        0: [frac_to_dec, tenths_hundredths, common_equiv, grid_convert,
            table_fill, dec_to_frac_num],
        1: [frac_to_dec, dec_to_frac_num, dec_to_frac_den, common_equiv,
            mixed_to_dec, grid_convert, table_fill, which_bigger],
        2: [frac_to_dec, dec_to_frac_num, dec_to_frac_den, mixed_to_dec,
            which_bigger, table_fill, grid_convert, common_equiv],
    }, d, weighted_tail=[grid_convert, table_fill])


# ============================================================== 8.3.e ========
@skill("Y8.3.e", "Add and subtract fractions and mixed numbers", S3)
def _(d=1):
    d = _t(d)

    def same_den_add():
        dd = pick([5, 6, 7, 8, 9, 10])
        a = random.randint(1, dd - 2)
        b = random.randint(1, dd - a - 1) if dd - a - 1 >= 1 else 1
        s = a + b
        sn, sd = _simp(s, dd)
        return _fq("Work out %d/%d + %d/%d. Give your answer as a fraction in "
                   "its simplest form." % (a, dd, b, dd), sn, sd,
                   ["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, s, dd),
                    "In simplest form that is %d/%d." % (sn, sd)])

    def same_den_sub():
        dd = pick([5, 6, 7, 8, 9, 10])
        a = random.randint(2, dd - 1)
        b = random.randint(1, a - 1)
        r = a - b
        sn, sd = _simp(r, dd)
        return _fq("Work out %d/%d − %d/%d. Give your answer as a fraction in "
                   "its simplest form." % (a, dd, b, dd), sn, sd,
                   ["%d/%d − %d/%d = %d/%d." % (a, dd, b, dd, r, dd),
                    "= %d/%d." % (sn, sd)])

    def diff_den_add():
        d1, d2 = pick([(2, 3), (3, 4), (2, 5), (4, 6), (2, 6), (3, 6),
                       (4, 8), (3, 8)])
        L = _lcm(d1, d2)
        while True:                     # keep the sum proper (below 1)
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            num = n1 * (L // d1) + n2 * (L // d2)
            if num < L:
                break
        sn, sd = _simp(num, L)
        return _fq("Work out %d/%d + %d/%d. Give your answer as a fraction in "
                   "its simplest form." % (n1, d1, n2, d2), sn, sd,
                   ["Common denominator %d: %d/%d + %d/%d = %d/%d."
                    % (L, n1 * (L // d1), L, n2 * (L // d2), L, num, L),
                    "= %d/%d." % (sn, sd)])

    def diff_den_sub():
        d1, d2 = pick([(2, 3), (3, 4), (2, 5), (5, 6), (3, 8), (4, 6)])
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        v1 = n1 * (L // d1)
        v2 = n2 * (L // d2)
        while v1 == v2:                 # 3/6 − 2/4 would be 0
            n2 = random.randint(1, d2 - 1)
            v2 = n2 * (L // d2)
        if v1 <= v2:
            v1, v2, d1, d2, n1, n2 = v2, v1, d2, d1, n2, n1
        num = v1 - v2
        sn, sd = _simp(num, L)
        return _fq("Work out %d/%d − %d/%d. Give your answer as a fraction in "
                   "its simplest form." % (n1, d1, n2, d2), sn, sd,
                   ["Common denominator %d: %d/%d − %d/%d = %d/%d."
                    % (L, v1, L, v2, L, num, L),
                    "= %d/%d." % (sn, sd)])

    def mixed_add():
        w1 = random.randint(1, 3)
        w2 = random.randint(1, 3)
        dd = pick([3, 4, 5, 6])
        n1 = random.randint(1, dd - 1)
        n2 = random.randint(1, dd - 1)
        total = Fraction(w1 * dd + n1, dd) + Fraction(w2 * dd + n2, dd)
        w, rn, rd = _improper_to_mixed(total.numerator, total.denominator)
        return _mixq("Work out %s + %s. Give your answer as a mixed number in "
                     "its simplest form."
                     % (_mixed_str(w1, n1, dd), _mixed_str(w2, n2, dd)),
                     w, rn, rd,
                     solution=["Add wholes and fractions: %d + %d = %d."
                               % (w1, w2, w1 + w2),
                               "The total is %s." % _mixed_str(w, rn, rd)])

    def mixed_sub():
        dd = pick([3, 4, 5, 6])
        w1 = random.randint(3, 6)
        w2 = random.randint(1, w1 - 2)  # result stays above 1
        n1 = random.randint(1, dd - 1)
        n2 = random.randint(1, dd - 1)
        f1 = Fraction(w1 * dd + n1, dd)
        f2 = Fraction(w2 * dd + n2, dd)
        r = f1 - f2
        w, rn, rd = _improper_to_mixed(r.numerator, r.denominator)
        return _mixq("Work out %s − %s. Give your answer as a mixed number "
                     "in its simplest form."
                     % (_mixed_str(w1, n1, dd), _mixed_str(w2, n2, dd)),
                     w, rn, rd,
                     solution=["Write both over %d and subtract." % dd,
                               "The answer is %s." % _mixed_str(w, rn, rd)])

    def missing_add():
        dd = pick([4, 5, 6, 8])
        a = random.randint(1, dd - 2)
        s = random.randint(a + 1, dd - 1)
        b = s - a
        sn, sd = _simp(b, dd)
        return _fq("%d/%d + ___ = %d/%d . What is the missing fraction? Give it "
                   "in simplest form." % (a, dd, s, dd), sn, sd,
                   ["%d/%d − %d/%d = %d/%d." % (s, dd, a, dd, b, dd),
                    "= %d/%d." % (sn, sd)])

    def word_pizza():
        who1, who2 = _two_names()
        dd = pick([4, 6, 8])
        a = random.randint(1, dd // 2)
        b = random.randint(1, dd - a - 1) if dd - a - 1 >= 1 else 1
        s = a + b
        sn, sd = _simp(s, dd)
        return _fq("%s eats %d/%d of a pizza and %s eats %d/%d of it. What "
                   "fraction of the pizza do they eat altogether? Give it in "
                   "simplest form." % (who1, a, dd, who2, b, dd), sn, sd,
                   ["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, s, dd),
                    "= %d/%d." % (sn, sd)])

    def bar_add():
        dd = pick([6, 8, 10])
        a = random.randint(1, dd - 2)
        b = random.randint(1, dd - a - 1) if dd - a - 1 >= 1 else 1
        s = a + b
        return _fbq("Shade %d/%d, then a further %d/%d, of the bar. Read off "
                    "the total shaded fraction." % (a, dd, b, dd), dd, s,
                    ["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, s, dd)])

    return _pick_opts({
        0: [same_den_add, same_den_sub, missing_add, word_pizza, bar_add,
            diff_den_add],
        1: [same_den_add, same_den_sub, diff_den_add, diff_den_sub,
            missing_add, word_pizza, bar_add, mixed_add],
        2: [diff_den_add, diff_den_sub, mixed_add, mixed_sub, missing_add,
            word_pizza, same_den_sub, bar_add],
    }, d, weighted_tail=[bar_add, bar_add])


# ============================================================== 8.3.f ========
@skill("Y8.3.f", "Multiply fractions and mixed numbers", S3)
def _(d=1):
    d = _t(d)

    def frac_times_frac():
        d1 = pick([2, 3, 4, 5])
        d2 = pick([2, 3, 4, 5])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        num, den = n1 * n2, d1 * d2
        sn, sd = _simp(num, den)
        return _fq("Work out %d/%d × %d/%d. Give your answer as a fraction in "
                   "its simplest form." % (n1, d1, n2, d2), sn, sd,
                   ["Multiply tops and bottoms: %d/%d." % (num, den),
                    "= %d/%d." % (sn, sd)])

    def frac_times_whole():
        dd = pick([2, 3, 4, 5, 6, 8])
        n = random.randint(1, dd - 1)
        w = random.randint(*_by_d(d, (2, 6), (3, 12), (4, 20)))
        num, den = n * w, dd
        sn, sd = _simp(num, den)
        if sd == 1:
            return _iq("Work out %d/%d × %d." % (n, dd, w), sn,
                       ["%d × %d = %d, then ÷ %d = %d."
                        % (n, w, n * w, dd, sn)])
        w2, rn, rd = _improper_to_mixed(sn, sd)
        if w2 > 0:
            return _mixq("Work out %d/%d × %d. Give your answer as a mixed "
                         "number in simplest form." % (n, dd, w), w2, rn, rd,
                         solution=["%d × %d = %d/%d." % (n, w, n * w, dd),
                                   "= %s." % _mixed_str(w2, rn, rd)])
        return _fq("Work out %d/%d × %d. Give your answer as a fraction in "
                   "simplest form." % (n, dd, w), sn, sd,
                   ["%d/%d × %d = %d/%d = %d/%d."
                    % (n, dd, w, num, den, sn, sd)])

    def unit_frac_of():
        dd = pick([2, 3, 4, 5])
        whole = dd * random.randint(*_by_d(d, (2, 6), (3, 10), (4, 15)))
        val = whole // dd
        return _iq("Work out 1/%d of %d." % (dd, whole), val,
                   ["%d ÷ %d = %d." % (whole, dd, val)])

    def mixed_times_whole():
        w = random.randint(1, 3)
        dd = pick([2, 3, 4])
        n = random.randint(1, dd - 1)
        k = random.randint(2, _by_d(d, 3, 4, 6))
        imp = w * dd + n
        prod = Fraction(imp * k, dd)
        w2, rn, rd = _improper_to_mixed(prod.numerator, prod.denominator)
        if rn == 0:
            return _iq("Work out %s × %d." % (_mixed_str(w, n, dd), k), w2,
                       ["%s = %d/%d." % (_mixed_str(w, n, dd), imp, dd),
                        "%d/%d × %d = %d." % (imp, dd, k, w2)])
        return _mixq("Work out %s × %d. Give your answer as a mixed number "
                     "in simplest form."
                     % (_mixed_str(w, n, dd), k), w2, rn, rd,
                     solution=["%s = %d/%d." % (_mixed_str(w, n, dd), imp, dd),
                               "%d/%d × %d = %s."
                               % (imp, dd, k, _mixed_str(w2, rn, rd))])

    def square_frac():
        dd = pick([2, 3, 4, 5])
        n = random.randint(1, dd - 1)
        num, den = n * n, dd * dd
        sn, sd = _simp(num, den)
        return _fq("Work out (%d/%d)²  (that is %d/%d × %d/%d). Give it in "
                   "simplest form." % (n, dd, n, dd, n, dd), sn, sd,
                   ["%d/%d × %d/%d = %d/%d." % (n, dd, n, dd, num, den),
                    "= %d/%d." % (sn, sd)])

    def missing_factor():
        d1 = pick([2, 3, 4])
        n1 = random.randint(1, d1 - 1)
        d2 = pick([2, 3, 4])
        n2 = random.randint(1, d2 - 1)
        pnum, pden = n1 * n2, d1 * d2
        return _fq("%d/%d × ___ = %d/%d . What is the missing fraction?"
                   % (n1, d1, pnum, pden), n2, d2,
                   ["Divide: (%d/%d) ÷ (%d/%d) = %d/%d."
                    % (pnum, pden, n1, d1, n2, d2)])

    def word_recipe():
        who = pick(NAMES)
        dd = pick([2, 3, 4])
        n = 1
        whole = dd * random.randint(2, 6)
        val = whole // dd
        return _iq("A recipe uses %d g of sugar. %s makes 1/%d of the recipe. "
                   "How many grams of sugar does %s use?"
                   % (whole, who, dd, who), val, unit="g",
                   solution=["%d ÷ %d = %d g." % (whole, dd, val)])

    def bar_of_bar():
        d1 = pick([2, 3, 4])
        d2 = pick([2, 3])
        n1 = 1
        num, den = 1, d1 * d2
        return _fbq("A bar is split into %d equal parts and 1 part is taken. "
                    "That part is then split into %d and 1 piece taken. Shade "
                    "the final fraction of the whole bar."
                    % (d1, d2), den, 1,
                    ["1/%d of 1/%d = 1/%d." % (d2, d1, den),
                     "So 1 of %d equal parts is shaded." % den])

    def mult_choose_model():
        # Multiply fractions by whole numbers: choose the model.
        dd = pick([4, 5, 6, 8, 10])
        w = random.randint(2, min(dd - 1, _by_d(d, 3, 4, 5)))
        return _agread(
            "Multiply the fraction by the whole number. The area model shows "
            "1/%d shaded %d times; read off the product. What "
            "is 1/%d × %d? Give your answer as a fraction."
            % (dd, w, dd, w), dd, w, "%d/%d" % (w, dd), "frac",
            ["1/%d added %d times fills %d of the %d equal parts."
             % (dd, w, w, dd),
             "So 1/%d × %d = %d/%d." % (dd, w, w, dd)],
            placeholder="e.g. 3/8")

    def mult_complete_equation():
        # Multiply fractions by whole numbers using models: complete the equation.
        for _try in range(40):
            dd = pick([6, 8, 10, 12])
            n = random.randint(1, 3)
            w = random.randint(2, 5)
            if 2 <= n * w < dd:
                break
        else:
            dd, n, w = 12, 1, 2
        prod = n * w
        return _agread(
            "Use the area model to complete the equation. The model shows %d/%d "
            "added %d times, so %d parts of %d are shaded. Complete: "
            "%d/%d × %d = ___/%d. Type the missing numerator."
            % (n, dd, w, prod, dd, n, dd, w, dd), dd, prod, prod, "int",
            ["%d/%d added %d times shades %d of the %d equal parts."
             % (n, dd, w, prod, dd),
             "So %d/%d × %d = %d/%d and the missing numerator is %d."
             % (n, dd, w, prod, dd, prod)],
            placeholder="a whole number")

    return _pick_opts({
        0: [frac_times_frac, frac_times_whole, unit_frac_of, word_recipe,
            bar_of_bar, missing_factor, mult_choose_model,
            mult_complete_equation],
        1: [frac_times_frac, frac_times_whole, unit_frac_of, square_frac,
            missing_factor, word_recipe, bar_of_bar, mixed_times_whole,
            mult_choose_model, mult_complete_equation],
        2: [frac_times_frac, mixed_times_whole, square_frac, missing_factor,
            frac_times_whole, word_recipe, unit_frac_of, bar_of_bar,
            mult_choose_model, mult_complete_equation],
    }, d, weighted_tail=[bar_of_bar, mult_choose_model, mult_complete_equation])


# ============================================================== 8.3.g ========
@skill("Y8.3.g", "Fraction of a quantity; scale by a fraction", S3)
def _(d=1):
    d = _t(d)

    def unit_of():
        dd = pick([2, 3, 4, 5, 6, 8])
        whole = dd * random.randint(*_by_d(d, (2, 8), (4, 15), (6, 25)))
        val = whole // dd
        return _iq("Work out 1/%d of %d." % (dd, whole), val,
                   ["%d ÷ %d = %d." % (whole, dd, val)])

    def nonunit_of():
        dd = pick([3, 4, 5, 6, 8])
        n = random.randint(2, dd - 1)
        whole = dd * random.randint(*_by_d(d, (2, 6), (3, 12), (4, 20)))
        val = whole // dd * n
        return _iq("Work out %d/%d of %d." % (n, dd, whole), val,
                   ["%d ÷ %d = %d." % (whole, dd, whole // dd),
                    "%d × %d = %d." % (whole // dd, n, val)])

    def money_of():
        dd = pick([2, 4, 5])
        n = random.randint(1, dd - 1)
        pounds = dd * random.randint(4, 20)
        val = pounds // dd * n
        return _iq("Work out %d/%d of £%d." % (n, dd, pounds), val, unit="£",
                   solution=["£%d ÷ %d = £%d." % (pounds, dd, pounds // dd),
                    "× %d = £%d." % (n, val)])

    def strip_of():
        dd = pick([3, 4, 5, 6])
        n = random.randint(2, dd - 1)  # >=2 so it is not trivially one part
        each = random.randint(*_by_d(d, (4, 12), (6, 20), (10, 40)))
        whole = each * dd
        val = each * n
        return _stripq("Use the strip model. A ribbon %d cm long is split into "
                       "%d equal parts. What is the total length of %d parts, "
                       "in cm?" % (whole, dd, n), dd, "%d cm" % each,
                       "%d cm" % whole, n, val, "int",
                       ["Each part is %d ÷ %d = %d cm." % (whole, dd, each),
                        "%d × %d = %d cm." % (each, n, val)])

    def find_whole():
        dd = pick([2, 3, 4, 5])
        part = random.randint(*_by_d(d, (2, 8), (4, 15), (6, 25)))
        whole = part * dd
        return _iq("1/%d of a number is %d. What is the number?" % (dd, part),
                   whole, ["%d × %d = %d." % (part, dd, whole)])

    def scale_up():
        dd = pick([2, 3, 4, 5])
        n = dd + random.randint(1, 4)  # improper -> enlarges
        base = dd * random.randint(4, 12)
        val = base // dd * n
        return _iq("A length of %d cm is scaled by %d/%d. What is the new "
                   "length, in cm?" % (base, n, dd), val, unit="cm",
                   solution=["%d ÷ %d = %d." % (base, dd, base // dd),
                    "× %d = %d cm." % (n, val)])

    def scale_down():
        dd = pick([3, 4, 5])
        n = random.randint(1, dd - 1)
        base = dd * random.randint(4, 15)
        val = base // dd * n
        return _iq("A recipe for %d g is scaled by %d/%d. What is the new "
                   "amount, in grams?" % (base, n, dd), val, unit="g",
                   solution=["%d × %d/%d = %d g." % (base, n, dd, val)])

    def compare_of():
        (n1, d1), (n2, d2) = random.sample(pick([
            [(3, 4), (3, 5)], [(2, 3), (3, 4)], [(4, 5), (3, 4)],
            [(2, 5), (1, 3)], [(3, 5), (2, 3)], [(5, 6), (4, 5)]]), 2)
        whole = _lcm(d1, d2) * random.randint(2, 6)
        a = whole // d1 * n1
        b = whole // d2 * n2
        f1, f2 = "%d/%d" % (n1, d1), "%d/%d" % (n2, d2)
        bigger = f1 if a > b else f2
        return _sq("Which is more: %s of %d or %s of %d? Type %s or %s."
                   % (f1, whole, f2, whole, f1, f2), bigger,
                   placeholder="%s or %s" % (f1, f2),
                   solution=["%s of %d = %d; %s of %d = %d."
                             % (f1, whole, a, f2, whole, b),
                             "So %s of %d is more." % (bigger, whole)])

    def word_class():
        dd = pick([3, 4, 5])
        n = random.randint(1, dd - 1)
        total = dd * random.randint(5, 9)
        val = total // dd * n
        return _iq("A school has %d pupils in Year 8. %d/%d of them walk to "
                   "school. How many pupils walk to school?" % (total, n, dd),
                   val, ["%d ÷ %d = %d." % (total, dd, total // dd),
                         "× %d = %d." % (n, val)], unit="pupils")

    return _pick_opts({
        0: [unit_of, nonunit_of, money_of, strip_of, word_class, find_whole],
        1: [unit_of, nonunit_of, money_of, strip_of, find_whole, scale_down,
            word_class, compare_of],
        2: [nonunit_of, money_of, find_whole, scale_up, scale_down, compare_of,
            strip_of, word_class],
    }, d, weighted_tail=[strip_of, strip_of])


# ============================================================== 8.3.h ========
@skill("Y8.3.h", "Reciprocals; divide fractions and mixed numbers", S3)
def _(d=1):
    d = _t(d)

    def reciprocal_frac():
        dd = pick([2, 3, 4, 5, 6, 8])
        n = random.randint(1, dd - 1)
        return _fq("What is the reciprocal of %d/%d? (Turn the fraction upside "
                   "down.)" % (n, dd), dd, n,
                   ["The reciprocal of %d/%d is %d/%d." % (n, dd, dd, n)])

    def reciprocal_whole():
        w = random.randint(2, 9)
        return _fq("What is the reciprocal of %d? Give your answer as a "
                   "fraction." % w, 1, w,
                   ["%d = %d/1, so its reciprocal is 1/%d." % (w, w, w)])

    def frac_div_frac():
        d1 = pick([2, 3, 4, 5])
        n1 = random.randint(1, d1 - 1)
        d2 = pick([2, 3, 4, 5])
        n2 = random.randint(1, d2 - 1)
        num, den = n1 * d2, d1 * n2
        sn, sd = _simp(num, den)
        w2, rn, rd = _improper_to_mixed(sn, sd)
        if sd == 1:
            return _iq("Work out %d/%d ÷ %d/%d." % (n1, d1, n2, d2), sn,
                       ["Multiply by the reciprocal: %d/%d × %d/%d."
                        % (n1, d1, d2, n2),
                        "= %d." % sn])
        if w2 > 0:
            return _mixq("Work out %d/%d ÷ %d/%d. Give your answer as a mixed "
                         "number in simplest form." % (n1, d1, n2, d2),
                         w2, rn, rd,
                         solution=["Multiply by the reciprocal: %d/%d × %d/%d "
                                   "= %d/%d." % (n1, d1, d2, n2, num, den),
                                   "= %s." % _mixed_str(w2, rn, rd)])
        return _fq("Work out %d/%d ÷ %d/%d. Give your answer as a fraction in "
                   "simplest form." % (n1, d1, n2, d2), sn, sd,
                   ["Multiply by the reciprocal: %d/%d × %d/%d = %d/%d."
                    % (n1, d1, d2, n2, num, den),
                    "= %d/%d." % (sn, sd)])

    def frac_div_whole():
        dd = pick([2, 3, 4, 5, 6])
        n = random.randint(1, dd - 1)
        w = random.randint(2, _by_d(d, 3, 5, 8))
        num, den = n, dd * w
        sn, sd = _simp(num, den)
        return _fq("Work out %d/%d ÷ %d. Give your answer as a fraction in "
                   "simplest form." % (n, dd, w), sn, sd,
                   ["Dividing by %d multiplies the denominator: %d/%d."
                    % (w, num, den),
                    "= %d/%d." % (sn, sd)])

    def whole_div_frac():
        w = random.randint(2, _by_d(d, 4, 6, 9))
        dd = pick([2, 3, 4])
        n = 1
        val = w * dd  # w ÷ (1/dd) = w*dd
        return _iq("Work out %d ÷ 1/%d." % (w, dd), val,
                   ["Dividing by 1/%d is the same as multiplying by %d."
                    % (dd, dd),
                    "%d × %d = %d." % (w, dd, val)])

    def how_many_fit():
        dd = pick([2, 3, 4])
        wholes = random.randint(2, 6)
        val = wholes * dd
        return _iq("How many 1/%d-litre cups can be filled from %d litres of "
                   "juice?" % (dd, wholes), val,
                   ["%d ÷ 1/%d = %d × %d = %d." % (wholes, dd, wholes, dd,
                                                   val)], unit="cups")

    def mixed_div_whole():
        w = random.randint(1, 3)
        dd = pick([2, 3, 4])
        n = random.randint(1, dd - 1)
        imp = w * dd + n
        k = random.randint(2, 4)
        num, den = imp, dd * k
        sn, sd = _simp(num, den)
        w2, rn, rd = _improper_to_mixed(sn, sd)
        if w2 > 0 and rn > 0:
            return _mixq("Work out %s ÷ %d. Give your answer as a mixed "
                         "number in simplest form." % (_mixed_str(w, n, dd), k), w2, rn, rd,
                         solution=["%s = %d/%d." % (_mixed_str(w, n, dd), imp,
                                                    dd),
                                   "%d/%d ÷ %d = %s." % (imp, dd, k,
                                                         _mixed_str(w2, rn,
                                                                    rd))])
        return _fq("Work out %s ÷ %d. Give your answer as a fraction in "
                   "simplest form." % (_mixed_str(w, n, dd), k), sn, sd,
                   ["%s = %d/%d, then ÷ %d = %d/%d."
                    % (_mixed_str(w, n, dd), imp, dd, k, sn, sd)])

    def is_reciprocal():
        dd = pick([2, 3, 4, 5])
        n = random.randint(1, dd - 1)
        if random.random() < 0.5:
            return _sq("Two numbers are reciprocals if they multiply to make "
                       "1. Do %d/%d and %d/%d multiply to make 1? Type yes or "
                       "no." % (n, dd, dd, n), "yes", placeholder="yes or no",
                       solution=["%d/%d × %d/%d = %d/%d = 1."
                                 % (n, dd, dd, n, n * dd, n * dd)])
        return _sq("Two numbers are reciprocals if they multiply to make 1. Do "
                   "%d/%d and %d/%d multiply to make 1? Type yes or no."
                   % (n, dd, n, dd), "no", placeholder="yes or no",
                   solution=["%d/%d × %d/%d = %d/%d, which is not 1."
                             % (n, dd, n, dd, n * n, dd * dd)])

    def line_recip():
        dd = pick([2, 3, 4, 5, 6, 8])
        return _nlq("The reciprocal of %d is 1/%d. The number line runs from 0 "
                    "to 1 in %s. Mark 1/%d on it." % (dd, dd, _ths(dd), dd),
                    _fl(Fraction(1, dd)), 0, 1, Fraction(1, dd), 1,
                    ["The reciprocal of %d is 1/%d." % (dd, dd),
                     "It is one step of 1/%d from 0." % dd])

    def strip_fit():
        dd = pick([2, 3, 4])
        wholes = random.randint(2, 5)
        val = wholes * dd
        return _stripq("Use the strip model. A ribbon %d m long is cut into "
                       "pieces each 1/%d m long. How many pieces are there?"
                       % (wholes, dd), wholes, "1 m", "%d m" % wholes, None,
                       val, "int",
                       ["Each metre gives %d pieces, so %d × %d = %d."
                        % (dd, wholes, dd, val)])

    def div_unit_by_whole_model():
        # Divide unit fractions by whole numbers using models.
        dd = pick([2, 3, 4, 5])
        w = random.randint(2, _by_d(d, 3, 4, 5))
        parts = dd * w
        return _agread(
            "Use an area model to divide the unit fraction by a whole number. "
            "The model splits 1/%d into %d equal parts. Work out 1/%d ÷ %d and "
            "give your answer as a fraction." % (dd, w, dd, w),
            parts, 1, "1/%d" % parts, "frac",
            ["Splitting 1/%d into %d makes %d equal parts in the whole."
             % (dd, w, parts),
             "So 1/%d ÷ %d = 1/%d." % (dd, w, parts)],
            placeholder="e.g. 1/12")

    def div_whole_by_unit_model():
        # Divide whole numbers by unit fractions using models.
        dd = pick([2, 3, 4, 5])
        w = random.randint(2, _by_d(d, 4, 6, 8))
        val = w * dd
        return _agread(
            "Use a model to divide a whole number by a unit fraction. The area "
            "model shows one 1/%d piece. How many 1/%d pieces fit into %d "
            "wholes? Work out %d ÷ 1/%d." % (dd, dd, w, w, dd),
            dd, 1, val, "int",
            ["Each whole contains %d pieces of size 1/%d." % (dd, dd),
             "%d ÷ 1/%d = %d × %d = %d." % (w, dd, w, dd, val)],
            placeholder="a whole number")

    def div_area_model():
        # Divide unit fractions and whole numbers using area models.
        dd = pick([2, 3, 4, 5])
        if random.random() < 0.5:
            w = random.randint(2, _by_d(d, 3, 4, 5))
            parts = dd * w
            return _agread(
                "Use an area model. The model splits the unit fraction 1/%d "
                "into %d equal parts. Work out 1/%d ÷ %d and give your answer "
                "as a fraction." % (dd, w, dd, w), parts, 1, "1/%d" % parts,
                "frac", ["1/%d ÷ %d = 1/%d." % (dd, w, parts)],
                placeholder="e.g. 1/12")
        w = random.randint(2, _by_d(d, 4, 6, 8))
        val = w * dd
        return _agread(
            "Use an area model. The model shows one 1/%d piece. How many 1/%d "
            "pieces make %d wholes? Work out %d ÷ 1/%d." % (dd, dd, w, w, dd),
            dd, 1, val, "int",
            ["%d ÷ 1/%d = %d × %d = %d." % (w, dd, w, dd, val)],
            placeholder="a whole number")

    return _pick_opts({
        0: [reciprocal_frac, reciprocal_whole, whole_div_frac, how_many_fit,
            frac_div_whole, is_reciprocal, line_recip, div_unit_by_whole_model,
            div_whole_by_unit_model, div_area_model],
        1: [reciprocal_frac, reciprocal_whole, frac_div_frac, frac_div_whole,
            whole_div_frac, how_many_fit, is_reciprocal, mixed_div_whole,
            line_recip, div_unit_by_whole_model, div_whole_by_unit_model,
            div_area_model],
        2: [reciprocal_frac, frac_div_frac, frac_div_whole, whole_div_frac,
            mixed_div_whole, how_many_fit, is_reciprocal, line_recip,
            div_unit_by_whole_model, div_whole_by_unit_model, div_area_model],
    }, d, weighted_tail=[div_unit_by_whole_model, div_whole_by_unit_model,
                         div_area_model])


# ============================================================== 8.3.i ========
@skill("Y8.3.i", "Mixed four-operation fraction calculations", S3)
def _(d=1):
    d = _t(d)

    def add_then_mult():
        dd = pick([3, 4, 6])
        a = random.randint(1, dd - 2)
        b = random.randint(1, dd - a - 1) if dd - a - 1 >= 1 else 1
        k = random.randint(2, 4)
        # (a/dd + b/dd) × k
        s = a + b
        res = Fraction(s * k, dd)
        sn, sd = res.numerator, res.denominator
        w2, rn, rd = _improper_to_mixed(sn, sd)
        if sd == 1:
            return _iq("Work out (%d/%d + %d/%d) × %d." % (a, dd, b, dd, k),
                       sn, ["Brackets: %d/%d + %d/%d = %d/%d."
                            % (a, dd, b, dd, s, dd),
                            "× %d = %d." % (k, sn)])
        if w2 > 0:
            return _mixq("Work out (%d/%d + %d/%d) × %d. Give a mixed number in "
                         "simplest form."
                         % (a, dd, b, dd, k), w2, rn, rd,
                         solution=["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, s,
                                                               dd),
                                   "× %d = %s." % (k, _mixed_str(w2, rn, rd))])
        return _fq("Work out (%d/%d + %d/%d) × %d. Give it in simplest form."
                   % (a, dd, b, dd, k), sn, sd,
                   ["%d/%d + %d/%d = %d/%d, × %d = %d/%d."
                    % (a, dd, b, dd, s, dd, k, sn, sd)])

    def mult_then_add():
        d1 = pick([2, 3, 4])
        d2 = pick([2, 3, 4])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        dd = pick([2, 4])
        n3 = 1
        res = Fraction(n1 * n2, d1 * d2) + Fraction(n3, dd)
        sn, sd = res.numerator, res.denominator
        w2, rn, rd = _improper_to_mixed(sn, sd)
        if sd == 1:
            return _iq("Work out %d/%d × %d/%d + %d/%d."
                       % (n1, d1, n2, d2, n3, dd), sn,
                       ["Multiply first: %d/%d × %d/%d = %d/%d."
                        % (n1, d1, n2, d2, n1 * n2, d1 * d2),
                        "+ %d/%d = %d." % (n3, dd, sn)])
        if w2 > 0:
            return _mixq("Work out %d/%d × %d/%d + %d/%d. Give a mixed number "
                         "in simplest form." % (n1, d1, n2, d2, n3, dd),
                         w2, rn, rd,
                         solution=["Multiply first, then add %d/%d." % (n3, dd),
                                   "The result is %s."
                                   % _mixed_str(w2, rn, rd)])
        return _fq("Work out %d/%d × %d/%d + %d/%d. Give it in simplest form."
                   % (n1, d1, n2, d2, n3, dd), sn, sd,
                   ["%d/%d × %d/%d = %d/%d." % (n1, d1, n2, d2, n1 * n2,
                                                d1 * d2),
                    "+ %d/%d = %d/%d." % (n3, dd, sn, sd)])

    def sub_then_div():
        dd = pick([4, 6, 8])
        a = random.randint(3, dd - 1)
        b = random.randint(1, a - 1)
        k = random.randint(2, 3)
        res = Fraction(a - b, dd) / k
        sn, sd = res.numerator, res.denominator
        return _fq("Work out (%d/%d − %d/%d) ÷ %d. Give it in simplest form."
                   % (a, dd, b, dd, k), sn, sd,
                   ["Brackets: %d/%d − %d/%d = %d/%d."
                    % (a, dd, b, dd, a - b, dd),
                    "÷ %d = %d/%d." % (k, sn, sd)])

    def div_then_sub():
        d1 = pick([2, 3, 4])
        n1 = random.randint(1, d1 - 1)
        w = random.randint(2, 4)
        dd = pick([4, 6, 8])
        n3 = 1
        res = Fraction(n1, d1 * w) - Fraction(n3, dd)
        if res <= 0:  # keep positive for this framing
            res = Fraction(n1, d1 * w)
            n3 = 0
            prompt = "Work out %d/%d ÷ %d." % (n1, d1, w)
        else:
            prompt = ("Work out %d/%d ÷ %d − %d/%d."
                      % (n1, d1, w, n3, dd))
        sn, sd = res.numerator, res.denominator
        return _fq(prompt + " Give it in simplest form.", sn, sd,
                   ["Divide first: %d/%d ÷ %d = %d/%d."
                    % (n1, d1, w, n1, d1 * w),
                    "The result is %d/%d." % (sn, sd)])

    def three_add():
        dd = pick([6, 8, 12])
        a = random.randint(1, dd - 3)
        b = random.randint(1, dd - a - 2)
        c = random.randint(1, dd - a - b - 1) if dd - a - b - 1 >= 1 else 1
        s = a + b + c
        sn, sd = _simp(s, dd)
        return _fq("Work out %d/%d + %d/%d + %d/%d. Give it in simplest form."
                   % (a, dd, b, dd, c, dd), sn, sd,
                   ["%d/%d + %d/%d + %d/%d = %d/%d."
                    % (a, dd, b, dd, c, dd, s, dd),
                    "= %d/%d." % (sn, sd)])

    def word_multi():
        who = pick(NAMES)
        dd = pick([4, 6, 8])
        used1 = random.randint(1, dd // 2)
        used2 = random.randint(1, dd - used1 - 1) if dd - used1 - 1 >= 1 else 1
        left = dd - used1 - used2
        sn, sd = _simp(left, dd)
        return _fq("%s starts with a full jug. %s pours out %d/%d, then a "
                   "further %d/%d. What fraction of the jug is left? Give it in "
                   "simplest form." % (who, who, used1, dd, used2, dd), sn, sd,
                   ["Poured out: %d/%d + %d/%d = %d/%d."
                    % (used1, dd, used2, dd, used1 + used2, dd),
                    "Left: 1 − %d/%d = %d/%d = %d/%d."
                    % (used1 + used2, dd, left, dd, sn, sd)])

    def bracket_bar():
        dd = pick([8, 10, 12])
        a = random.randint(2, dd - 2)
        b = random.randint(1, a - 1)
        return _fbq("Shade %d/%d of the bar, then rub out %d/%d. Read off the "
                    "fraction that stays shaded." % (a, dd, b, dd), dd, a - b,
                    ["%d/%d − %d/%d = %d/%d." % (a, dd, b, dd, a - b, dd)])

    def missing_in_chain():
        dd = pick([4, 6, 8])
        a = random.randint(1, dd - 2)
        r = random.randint(a + 1, dd - 1)
        b = r - a
        sn, sd = _simp(b, dd)
        return _fq("%d/%d + ___ = %d/%d . Find the missing fraction, in "
                   "simplest form." % (a, dd, r, dd), sn, sd,
                   ["%d/%d − %d/%d = %d/%d = %d/%d."
                    % (r, dd, a, dd, b, dd, sn, sd)])

    def evaluate_fraction_expr():
        # Evaluate numerical expressions involving fractions (BIDMAS).
        for _try in range(40):
            dd = pick([2, 3, 4, 6])
            a = random.randint(1, dd - 1)
            d2 = pick([2, 3, 4])
            b = random.randint(1, d2 - 1)
            d3 = pick([2, 3, 4])
            c = random.randint(1, d3 - 1)
            res = Fraction(a, dd) + Fraction(b, d2) * Fraction(c, d3)
            if res.denominator == 1 or res < 1:
                break
        else:
            dd, a, d2, b, d3, c = 4, 1, 2, 1, 2, 1
            res = Fraction(a, dd) + Fraction(b, d2) * Fraction(c, d3)
        prod = Fraction(b, d2) * Fraction(c, d3)
        expr = "%d/%d + %d/%d × %d/%d" % (a, dd, b, d2, c, d3)
        base = ("Evaluate this numerical expression involving fractions: %s ."
                % expr)
        sol = ["Multiply before adding (BIDMAS): %d/%d × %d/%d = %s."
               % (b, d2, c, d3, _fracstr(prod)),
               "Then %d/%d + %s = %s." % (a, dd, _fracstr(prod), _fracstr(res))]
        return _frac_result_q(base, res, sol)

    return _pick_opts({
        0: [add_then_mult, three_add, word_multi, bracket_bar, missing_in_chain,
            mult_then_add, evaluate_fraction_expr],
        1: [add_then_mult, mult_then_add, sub_then_div, three_add, word_multi,
            bracket_bar, missing_in_chain, div_then_sub, evaluate_fraction_expr],
        2: [add_then_mult, mult_then_add, sub_then_div, div_then_sub,
            three_add, word_multi, missing_in_chain, bracket_bar,
            evaluate_fraction_expr],
    }, d, weighted_tail=[bracket_bar, evaluate_fraction_expr])


# ============================================================== 8.3.j ========
@skill("Y8.3.j", "Fraction word problems and estimation", S3)
def _(d=1):
    d = _t(d)

    def estimate_sum():
        # round each to nearest whole and add
        pairs = []
        for _ in range(2):
            dd = pick([3, 4, 5, 6, 8])
            n = random.choice([1, dd - 1])  # near 0 or near 1
            pairs.append((n, dd))
        est = sum(round(n / dd) for n, dd in pairs)
        return _iq("Estimate %d/%d + %d/%d by rounding each fraction to the "
                   "nearest whole number (0 or 1). What is the estimate?"
                   % (pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]), est,
                   ["%d/%d rounds to %d and %d/%d rounds to %d."
                    % (pairs[0][0], pairs[0][1], round(pairs[0][0] /
                                                       pairs[0][1]),
                       pairs[1][0], pairs[1][1], round(pairs[1][0] /
                                                       pairs[1][1])),
                    "Estimate = %d." % est])

    def estimate_mixed_sum():
        a = random.randint(1, 4) + Fraction(random.choice([1, 3]),
                                            pick([4, 8]))
        b = random.randint(1, 4) + Fraction(random.choice([1, 3]),
                                            pick([4, 8]))
        est = round(a) + round(b)
        return _iq("Estimate %s + %s by rounding each mixed number to the "
                   "nearest whole number. What is the estimate?"
                   % (_mixed_str(*_improper_to_mixed(a.numerator,
                                                     a.denominator)),
                      _mixed_str(*_improper_to_mixed(b.numerator,
                                                     b.denominator))), est,
                   ["Round each to the nearest whole number and add.",
                    "Estimate = %d." % est])

    def word_of_quantity():
        dd = pick([3, 4, 5, 6])
        n = random.randint(1, dd - 1)
        total = dd * random.randint(*_by_d(d, (4, 8), (6, 15), (8, 25)))
        val = total // dd * n
        item = pick(["books", "apples", "pens", "toy cars", "mugs", "tickets"])
        return _iq("A shop has %d %s. %d/%d of them are sold. How many are "
                   "sold?" % (total, item, n, dd), val,
                   ["%d ÷ %d = %d, × %d = %d." % (total, dd, total // dd, n,
                                                  val)], unit=item)

    def remaining():
        dd = pick([3, 4, 5, 6, 8])
        n = random.randint(1, dd - 1)
        total = dd * random.randint(3, 12)
        left = total - total // dd * n
        return _iq("A tank holds %d litres. %d/%d of it is used. How many "
                   "litres are left?" % (total, n, dd), left, unit="litres",
                   solution=["Used: %d/%d of %d = %d." % (n, dd, total, total // dd * n),
                    "Left: %d − %d = %d." % (total, total // dd * n, left)])

    def find_whole_word():
        dd = pick([2, 3, 4, 5])
        n = random.randint(1, dd - 1)
        each = random.randint(*_by_d(d, (3, 9), (5, 15), (8, 25)))
        part = each * n
        whole = each * dd
        return _iq("%d/%d of a number is %d. What is the whole number?"
                   % (n, dd, part), whole,
                   ["One part (1/%d) is %d ÷ %d = %d." % (dd, part, n, each),
                    "The whole is %d × %d = %d." % (each, dd, whole)])

    def two_fractions_left():
        who = pick(NAMES)
        dd = pick([6, 8, 10, 12])
        a = random.randint(1, dd // 2)
        b = random.randint(1, dd - a - 1) if dd - a - 1 >= 1 else 1
        left = dd - a - b
        sn, sd = _simp(left, dd)
        return _fq("%s spends %d/%d of the money on food and %d/%d on travel. "
                   "What fraction is left? Give it in simplest form."
                   % (who, a, dd, b, dd), sn, sd,
                   ["Spent: %d/%d + %d/%d = %d/%d." % (a, dd, b, dd, a + b, dd),
                    "Left: %d/%d = %d/%d." % (left, dd, sn, sd)])

    def strip_word():
        dd = pick([4, 5, 6])
        n = random.randint(2, dd - 1)  # >=2 so more than one stage
        each = random.randint(6, 20)
        whole = each * dd
        val = each * n
        return _stripq("Use the strip model. A journey of %d km is split into "
                       "%d equal stages. How far are %d stages, in km?"
                       % (whole, dd, n), dd, "%d km" % each, "%d km" % whole,
                       n, val, "int",
                       ["Each stage is %d km." % each,
                        "%d × %d = %d km." % (each, n, val)])

    def better_estimate():
        # is a/b closer to 0, 1/2 or 1?
        dd = pick([5, 6, 7, 8, 9, 10])
        n = random.randint(1, dd - 1)
        while n * 4 in (dd, 3 * dd):    # 1/4 and 3/4 are equally close to two targets
            n = random.randint(1, dd - 1)
        f = n / dd
        target = min([0, 0.5, 1], key=lambda t: abs(f - t))
        label = {0: "0", 0.5: "1/2", 1: "1"}[target]
        return _sq("Is %d/%d closest to 0, 1/2 or 1? Type 0, 1/2 or 1."
                   % (n, dd), label, placeholder="0, 1/2 or 1",
                   solution=["%d/%d ≈ %s." % (n, dd, format(_rnd(Decimal(n) / dd, 2), "f")),
                             "That is closest to %s." % label])

    return _pick_opts({
        0: [word_of_quantity, remaining, find_whole_word, strip_word,
            better_estimate, estimate_sum],
        1: [estimate_sum, word_of_quantity, remaining, find_whole_word,
            two_fractions_left, strip_word, better_estimate, estimate_mixed_sum],
        2: [estimate_sum, estimate_mixed_sum, word_of_quantity, find_whole_word,
            two_fractions_left, better_estimate, remaining, strip_word],
    }, d, weighted_tail=[strip_word, strip_word])
