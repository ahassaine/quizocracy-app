# dev/app/logic/y6_gen_c.py — Year 6 generators: levels 6.5 and 6.6
#
# 6.5 Decimals (place value to three places, rounding, comparing and ordering,
#     adding and subtracting, x/÷ by 10, 100 and 1,000, multiplying by a whole
#     number, multiplying one-digit decimals, dividing by a whole number, and
#     multi-step problems where the answer has to be rounded in context)
# 6.6 Fractions, decimals and percentages (converting each way, the common
#     equivalences, comparing and ordering across the three forms, finding a
#     percentage of an amount and percentage problems)
#
# Every generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and chooses at random between 8+ genuinely different framings.
#
# All decimal arithmetic is done with Decimal or Fraction on exact integer
# inputs and converted to float only at the very end, so no answer can ever be
# 0.30000000000000004.
#
# Visual components used here:
#   area_grid (parts: 100) . the hundredths / percentage square
#   number_line ............ decimals in steps of 0.1, 0.01 and 0.001
#   data_table ............. price lists, conversion tables, results tables
#   fraction_bar ........... fraction/decimal equivalence
#   strip_model ............ sharing a decimal amount, percentage bars
#   pie_chart .............. percentages of a whole
#   bar_chart .............. percentage comparisons
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from .maths_engine import skill, pick, NAMES, n_words

S5 = "6.5 Decimals"
S6 = "6.6 Fractions, decimals & percentages"


# ---------------------------------------------------------------- helpers ----
def _tier(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_tier(d)]


def _pick_t(weights):
    """Choose a framing index; visual framings carry more weight."""
    total = float(sum(weights))
    r = random.random() * total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r < acc:
            return i
    return len(weights) - 1


def _D(x):
    """Anything -> an exact Decimal (never via binary float)."""
    if isinstance(x, Decimal):
        return x
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def _txt(x):
    """Exact Decimal -> tidy UK text: 3.400 -> '3.4', 100 -> '100', 0.375 -> '0.375'."""
    v = _D(x)
    if v == v.to_integral_value():
        return format(v.quantize(Decimal(1)), "f")
    v = v.normalize()
    return format(v, "f")


def _fl(x):
    """Exact Decimal -> the float stored as the answer."""
    return float(_D(x))


def _rnd(x, places=0):
    """Round half up to `places` decimal places, exactly."""
    q = Decimal(1).scaleb(-int(places))
    return _D(x).quantize(q, rounding=ROUND_HALF_UP)


def _dp(x):
    """Number of decimal places actually written."""
    s = _txt(x)
    return len(s.split(".")[1]) if "." in s else 0


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _places(k):
    """10 -> 'one place', 100 -> 'two places', 1000 -> 'three places'."""
    n = len(str(int(k))) - 1
    return "%s place%s" % (n_words(n), "" if n == 1 else "s")


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _lb(pence):
    """Pence -> '£12.30' (always two decimal places)."""
    pence = int(pence)
    return "£%d.%02d" % (pence // 100, pence % 100)


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _names(k):
    return random.sample(NAMES, k)


def _nq(prompt, value, unit=None, text=False, placeholder=None, solution=None):
    """A typed numeric answer (decimal) with a tiny tolerance."""
    spec = {}
    if unit:
        spec["unit"] = unit
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": _fl(value), "answer_type": "num",
            "tolerance": 1e-6, "solution": solution or []}


def _iq(prompt, value, unit=None, solution=None):
    spec = {}
    if unit:
        spec["unit"] = unit
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
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": "%d/%d" % (int(num), int(den)), "answer_type": "frac",
            "tolerance": 0, "solution": solution or []}


def _setq(prompt, values, solution, placeholder="e.g. 1.2, 3.4"):
    """An order-insensitive list of decimals, typed with commas between them."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(_txt(v) for v in values), "answer_type": "set",
            "tolerance": 0, "solution": solution}


def _lineq(prompt, value, lo, hi, step, major, solution):
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": _fl(lo), "max": _fl(hi), "step": _fl(step),
                     "major": _fl(major)},
            "answer": _fl(value), "answer_type": "num",
            "tolerance": _fl(step) / 2.0, "solution": solution}


def _tableq(prompt, headers, rows, answer, answer_type, solution,
            missing=None, tolerance=0, unit=None):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _gridshade(prompt, hundredths, solution):
    """Shade the hundredths square; the pupil's value comes back as n/100."""
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "fraction", "parts": 100},
            "answer": "%d/100" % int(hundredths), "answer_type": "frac",
            "tolerance": 0, "solution": solution}


def _gridread(prompt, hundredths, answer, answer_type, solution,
              tolerance=0, unit=None):
    spec = {"mode": "fraction_read", "parts": 100, "shaded": int(hundredths)}
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _barshade(prompt, parts, num, solution):
    return {"prompt": prompt, "component": "fraction_bar",
            "spec": {"parts": int(parts), "mode": "shade"},
            "answer": "%d/%d" % (int(num), int(parts)), "answer_type": "frac",
            "tolerance": 0, "solution": solution}


def _stripq(prompt, parts, part_label, total_label, unknown, answer,
            answer_type, solution, tolerance=0):
    return {"prompt": prompt, "component": "strip_model",
            "spec": {"mode": "equal_parts", "parts": int(parts),
                     "partLabel": str(part_label), "totalLabel": str(total_label),
                     "unknown": unknown},
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _pieq(prompt, slices, answer, answer_type, solution, highlight=None,
          tolerance=0):
    spec = {"slices": [[str(a), int(b)] for a, b in slices], "mode": "read"}
    if highlight is not None:
        spec["highlight"] = int(highlight)
    return {"prompt": prompt, "component": "pie_chart", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _barq(prompt, cats, vals, answer, answer_type, solution, tolerance=0):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "mode": "read"},
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


# ------------------------------------------------------- decimal builders ----
def _mk(dp, lo, hi):
    """A Decimal with at most `dp` decimal places, from an integer in [lo, hi]
    counted in units of 10**-dp. _mk(2, 105, 990) -> 1.05 ... 9.9. When dp >= 1
    the value always has at least one decimal place, so it never turns into a
    whole number in the prompt."""
    dp = int(dp)
    for _try in range(40):
        n = random.randint(int(lo), int(hi))
        if dp == 0 or n % (10 ** dp):
            return _D(n).scaleb(-dp)
    return _D(random.randint(int(lo), int(hi)) | 1).scaleb(-dp)


def _digit_words(s):
    return " ".join(n_words(int(ch)) for ch in s)


def _point_words(v):
    """Decimal -> 'four point two seven five'."""
    s = _txt(v)
    if "." not in s:
        return n_words(int(s))
    w, f = s.split(".")
    return "%s point %s" % (n_words(int(w)), _digit_words(f))


def _in_words(v):
    """Decimal -> UK words: 3.42 -> 'three and forty-two hundredths'."""
    s = _txt(v)
    if "." not in s:
        return n_words(int(s))
    w, f = s.split(".")
    return "%s and %s %s" % (n_words(int(w)), n_words(int(f)),
                             _PLACE_NAME[len(f) - 1])


_PLACE_NAME = ["tenths", "hundredths", "thousandths"]
_PLACE_VAL = [Decimal("0.1"), Decimal("0.01"), Decimal("0.001")]


def _pv3(d):
    """A number with three decimal places whose digits are all different, so
    'the digit 7' is never ambiguous."""
    nw = _by_d(d, 1, 2, 3)
    ds = random.sample(range(1, 10), nw + 3)
    whole = int("".join(str(x) for x in ds[:nw]))
    return whole, ds[nw], ds[nw + 1], ds[nw + 2]


_SHOP = ["notebook", "pen", "water bottle", "lunch box", "poster", "keyring",
         "badge", "pencil case"]
_FOOD = ["apple", "bread roll", "carton of juice", "banana", "muffin", "yoghurt"]
_DRINK = ["orange juice", "lemonade", "apple juice", "milk", "water"]


def _plural(word):
    if " of " in word:
        head, rest = word.split(" of ", 1)
        return _plural(head) + " of " + rest
    if word.endswith(("ch", "sh", "s", "x")):
        return word + "es"
    return word + "s"


# =============================================================== 6.5 =========
@skill("Y6.5.a", "Place value in decimals to three places", S5)
def _(d=1):
    d = _tier(d)
    whole, t1, h1, th1 = _pv3(d)
    val = _D("%d.%d%d%d" % (whole, t1, h1, th1))
    txt = _txt(val)
    digits = [t1, h1, th1]
    t = _pick_t([2, 2, 2, 1, 1, 1, 3, 1, 1, 3, 1, 2, 2])

    if t == 0:                       # value of a named digit, as a decimal
        i = random.randrange(3)
        return _nq("What is the value of the digit %d in %s? "
                   "Write the value as a decimal." % (digits[i], txt),
                   _PLACE_VAL[i] * digits[i],
                   solution=["The %d is in the %s place."
                             % (digits[i], _PLACE_NAME[i]),
                             "Its value is %s, which is %s."
                             % (_pl(digits[i], _PLACE_NAME[i][:-1]),
                                _txt(_PLACE_VAL[i] * digits[i]))])

    if t == 1:                       # which digit sits in a named place
        i = random.randrange(3)
        return _iq("Which digit is in the %s place in %s?"
                   % (_PLACE_NAME[i], txt), digits[i],
                   solution=["After the decimal point the places run tenths, "
                             "hundredths, thousandths.",
                             "The %s digit of %s is %d."
                             % (_PLACE_NAME[i], txt, digits[i])])

    if t == 2:                       # expanded form with one part missing
        parts = [_D(whole)] + [_PLACE_VAL[i] * digits[i] for i in range(3)]
        k = random.randrange(1, 4) if d else random.randrange(1, 4)
        shown = ["___" if i == k else _txt(p) for i, p in enumerate(parts)]
        return _nq("Complete the expanded form: %s = %s"
                   % (txt, " + ".join(shown)), parts[k],
                   solution=["%s is %s, %s, %s and %s." % (txt, _pl(whole, "one"), _pl(t1, "tenth"), _pl(h1, "hundredth"),
                                                     _pl(th1, "thousandth")),
                             "The missing part is %s." % _txt(parts[k])])

    if t == 3:                       # build the number from its parts
        return _nq("Write the number that is %s, %s, %s and %s."
                   % (_pl(whole, "one"), _pl(t1, "tenth"), _pl(h1, "hundredth"),
                      _pl(th1, "thousandth")), val,
                   solution=["Put each digit in its own place: ones, tenths, "
                             "hundredths, thousandths.",
                             "The number is %s." % txt])

    if t == 4:                       # how many thousandths altogether
        return _iq("How many thousandths are there altogether in %s?" % txt,
                   int(val * 1000), unit="thousandths",
                   solution=["1 whole is 1,000 thousandths.",
                             "%s is %d thousandths." % (txt, int(val * 1000))])

    if t == 5:                       # words -> figures
        return _nq("A decimal is read out as '%s'. Write that decimal in figures."
                   % _point_words(val), val,
                   solution=["The words after 'point' give the tenths, "
                             "hundredths and thousandths digits in order.",
                             "In figures that is %s." % txt])

    if t == 6:                       # place a three-place decimal on a line
        w = random.randint(0, _by_d(d, 1, 4, 8))
        tenth = random.randrange(0, 10)
        lo = _D(w) + _D(tenth) / 10
        v = lo + _D(random.randint(1, 99)) / 1000
        return _lineq("Place %s on the number line." % _txt(v), v,
                      lo, lo + _D("0.1"), _D("0.001"), _D("0.01"),
                      ["Each small step on the line is one thousandth, 0.001.",
                       "%s lies between %s and %s."
                       % (_txt(v), _txt(lo), _txt(lo + _D("0.1")))])

    if t == 7:                       # same digit, different value
        dig = random.randint(1, 9)
        others = [x for x in range(1, 10) if x != dig]
        i, j = random.sample(range(3), 2)
        a = ["0"] * 3
        a[i] = str(dig)
        for k in range(3):
            if k != i:
                a[k] = str(random.choice(others))
        b = ["0"] * 3
        b[j] = str(dig)
        for k in range(3):
            if k != j:
                b[k] = str(random.choice(others))
        a_txt = "%d.%s" % (random.choice(others), "".join(a))
        b_txt = "%d.%s" % (random.choice(others), "".join(b))
        bigger = a_txt if i < j else b_txt
        big_i, small_i = (i, j) if i < j else (j, i)
        return _nq("The digit %d appears in %s and in %s. In which of the two "
                   "numbers is the %d worth more? Write that number."
                   % (dig, a_txt, b_txt, dig), _D(bigger),
                   solution=["In %s the %d is in the %s place, worth %s."
                             % (bigger, dig, _PLACE_NAME[big_i],
                                _txt(_PLACE_VAL[big_i] * dig)),
                             "In the other number it is only worth %s, so %s."
                             % (_txt(_PLACE_VAL[small_i] * dig), bigger)])

    if t == 8:                       # add the parts back together
        return _nq("What is %s + %s + %s?"
                   % (_txt(_PLACE_VAL[0] * t1), _txt(_PLACE_VAL[1] * h1),
                      _txt(_PLACE_VAL[2] * th1)),
                   _PLACE_VAL[0] * t1 + _PLACE_VAL[1] * h1 + _PLACE_VAL[2] * th1,
                   solution=["%s, %s and %s."
                             % (_pl(t1, "tenth"), _pl(h1, "hundredth"),
                                _pl(th1, "thousandth")),
                             "Together that is 0.%d%d%d." % (t1, h1, th1)])

    if t == 9:                       # place-value chart (visual)
        w1 = random.randint(1, 9)
        v = _D("%d.%d%d%d" % (w1, t1, h1, th1))
        return _tableq("The place-value chart shows one number. "
                       "Write that number as a decimal.",
                       ["Ones", "Tenths", "Hundredths", "Thousandths"],
                       [[w1, t1, h1, th1]], _fl(v), "num",
                       ["Read the digits in order and put the decimal point "
                        "after the ones digit.",
                        "The number is %s." % _txt(v)], tolerance=1e-6)

    if t == 11:                      # decimals expressed in words -> figures
        w = random.randint(1, _by_d(d, 9, 40, 400))
        dpn = _by_d(d, 1, 2, random.choice([2, 3]))
        f = random.randint(1, 10 ** dpn - 1)
        v = _D("%d.%s" % (w, str(f).zfill(dpn)))
        return _nq("A decimal is written in words as '%s'. Write that decimal "
                   "in figures." % _in_words(v), v,
                   solution=["The whole-number part is %s." % n_words(w),
                             "In figures the decimal is %s." % _txt(v)])

    if t == 12:                      # figures -> the words for the decimal part
        w = random.randint(1, _by_d(d, 9, 40, 400))
        dpn = _by_d(d, 1, 2, random.choice([2, 3]))
        f = random.randint(1, 10 ** dpn - 1)
        v = _D("%d.%s" % (w, str(f).zfill(dpn)))
        s = _txt(v)
        wh, fr = s.split(".")
        return _iq("Written in words, the decimal %s is expressed as "
                   "'%s and ___ %s'. Type the missing number."
                   % (s, n_words(int(wh)), _PLACE_NAME[len(fr) - 1]), int(fr),
                   solution=["The digits after the decimal point are %s."
                             % " ".join(fr),
                             "%s is %s and %s %s."
                             % (s, n_words(int(wh)), n_words(int(fr)),
                                _PLACE_NAME[len(fr) - 1])])

    # value of the thousandths digit written as a fraction
    return _fq("What is the value of the digit %d in %s? "
               "Write the value as a fraction." % (th1, txt), th1, 1000,
               placeholder="e.g. 7/1000",
               solution=["The %d is in the thousandths place." % th1,
                         "Its value is %s, which is %d/1000."
                         % (_pl(th1, "thousandth"), th1)])


@skill("Y6.5.b", "Round decimals to a given number of places", S5)
def _(d=1):
    d = _tier(d)

    def _v(dp=None, more_than=0):
        """A value with `dp` decimal places, always written with more than
        `more_than` of them so the rounding is never already done."""
        dp = dp or _by_d(d, 2, random.choice([2, 3]), 3)
        w = random.randint(1, _by_d(d, 9, 40, 200))
        for _try in range(60):
            f = random.randint(1, 10 ** dp - 1)
            v = _D("%d.%s" % (w, str(f).zfill(dp)))
            if _dp(v) > more_than:
                return v
        return _D("%d.%s" % (w, "1".zfill(dp)))

    t = _pick_t([1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1])

    if t == 11:                      # round a calculator answer
        a = random.randint(_by_d(d, 2, 5, 10), _by_d(d, 30, 80, 200))
        b = pick([3, 6, 7, 9, 11])
        while a % b == 0:
            a += 1
        places = pick([1, 2]) if d else 1
        exact = _D(a) / _D(b)
        shown = exact.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
        r = _rnd(exact, places)
        return _nq("A calculator shows %d ÷ %d = %s. Round this to %s." % (a, b, _txt(shown), ["", "one decimal place",
                                                                                          "two decimal places"][places]),
                   r, solution=["Look at the digit in the next place after the %s." % ["", "tenths", "hundredths"][places],
                                "%s rounds to %s." % (_txt(shown), _txt(r))])

    if t == 12:                      # how much the rounding changes the number
        v = _v(3 if d else 2, more_than=1)
        places = 1
        r = _rnd(v, places)
        return _nq("%s is rounded to one decimal place. By how much does the number change?" % _txt(v), abs(r - v),
                   solution=["%s rounds to %s." % (_txt(v), _txt(r)),
                             "The difference is %s − %s = %s." % (_txt(max(r, v)), _txt(min(r, v)), _txt(abs(r - v)))])

    if t == 13:                      # estimate a product by rounding
        whole = random.randint(2, 9)
        a = _D(random.randint(11, 99)) / 10
        while _D(a * 10) % 10 in (0, 5):
            a = _D(random.randint(11, 99)) / 10
        ra = _rnd(a, 0)
        return _iq("Estimate %s × %d by first rounding %s to the nearest whole number." % (_txt(a), whole, _txt(a)),
                   int(ra) * whole, solution=["%s rounds to %s." % (_txt(a), _txt(ra)),
                                              "%s × %d = %d." % (_txt(ra), whole, int(ra) * whole)])

    if t == 0:                       # to the nearest whole number
        v = _v()
        return _iq("Round %s to the nearest whole number." % _txt(v), _rnd(v, 0),
                   solution=["Look at the tenths digit of %s." % _txt(v),
                             "%s rounds to %s." % (_txt(v), _txt(_rnd(v, 0)))])

    if t == 1:                       # to one decimal place
        v = _v(more_than=1)
        return _nq("Round %s to one decimal place." % _txt(v), _rnd(v, 1),
                   solution=["Look at the hundredths digit to decide.",
                             "%s rounds to %s." % (_txt(v), format(_rnd(v, 1), "f"))])

    if t == 2:                       # to two decimal places
        v = _v(3, more_than=2)
        return _nq("Round %s to two decimal places." % _txt(v), _rnd(v, 2),
                   solution=["Look at the thousandths digit to decide.",
                             "%s rounds to %s." % (_txt(v), format(_rnd(v, 2), "f"))])

    if t == 3:                       # exactly halfway
        places = pick([0, 1, 2])
        w = random.randint(1, 30)
        if places == 0:
            v = _D(w) + _D("0.5")
        elif places == 1:
            v = _D("%d.%d5" % (w, random.randrange(0, 10)))
        else:
            v = _D("%d.%d%d5" % (w, random.randrange(0, 10), random.randrange(0, 10)))
        r = _rnd(v, places)
        return _nq("Round %s to %s." % (_txt(v), ["the nearest whole number",
                                                  "one decimal place",
                                                  "two decimal places"][places]),
                   r,
                   solution=["%s is exactly halfway between the two rounded "
                             "values." % _txt(v),
                             "A half always rounds up, so the answer is %s."
                             % _txt(r)])

    if t == 4:                       # measures word problem
        who = pick(NAMES)
        v = _mk(3, 1200, 9800)
        while _dp(v) < 2:
            v = _mk(3, 1200, 9800)
        return _nq("%s measures a plank as %s metres long. Rounded to one "
                   "decimal place, how long is the plank in metres?"
                   % (who, _txt(v)), _rnd(v, 1), unit="m",
                   solution=["The hundredths digit decides which tenth is nearest.",
                             "%s m rounds to %s m." % (_txt(v), format(_rnd(v, 1), "f"))])

    if t == 5:                       # round then place on a number line
        v = _mk(2, 101, 899)
        while _dp(v) < 2:
            v = _mk(2, 101, 899)
        r = _rnd(v, 1)
        lo = _D(int(v))
        return _lineq("Round %s to one decimal place, then place your answer "
                      "on the number line." % _txt(v), r, lo, lo + 1,
                      _D("0.1"), _D("0.5"),
                      ["The hundredths digit of %s decides." % _txt(v),
                       "%s rounds to %s." % (_txt(v), format(r, "f"))])

    if t == 6:                       # inverse: largest / smallest
        target = _mk(1, 11, 89)
        largest = random.random() < 0.5
        if largest:
            ans = target + _D("0.04")
            return _nq("A number with two decimal places rounds to %s when it "
                       "is rounded to one decimal place. What is the largest "
                       "such number?" % _txt(target), ans,
                       solution=["Anything from %s up to %s rounds to %s."
                                 % (_txt(target - _D("0.05")), _txt(ans),
                                    _txt(target)),
                                 "The largest with two decimal places is %s."
                                 % _txt(ans)])
        ans = target - _D("0.05")
        return _nq("A number with two decimal places rounds to %s when it is "
                   "rounded to one decimal place. What is the smallest such "
                   "number?" % _txt(target), ans,
                   solution=["%s is exactly halfway and a half rounds up to %s."
                             % (_txt(ans), _txt(target)),
                             "So the smallest such number is %s." % _txt(ans)])

    if t == 7:                       # which of two rounds to the target
        w = random.randint(2, 20)
        a = _D(w) - _D(random.randint(1, 49)) / 100
        b = _D(w) - _D(random.randint(51, 99)) / 100
        first, second = (a, b) if random.random() < 0.5 else (b, a)
        return _nq("Which of these rounds to %d when rounded to the nearest "
                   "whole number: %s or %s? Write that number."
                   % (w, _txt(first), _txt(second)), a,
                   solution=["%s rounds to %d." % (_txt(a), w),
                             "%s rounds to %d instead, so the answer is %s."
                             % (_txt(b), w - 1, _txt(a))])

    if t == 8:                       # table of measurements
        who = _names(3)
        vals = []
        while len(vals) < 3:
            v3 = _mk(3, 1050, 1950)
            if _dp(v3) >= 2:
                vals.append(v3)
        i = random.randrange(3)
        rows = [[who[k], _txt(vals[k]) + " s"] for k in range(3)]
        return _tableq("The table shows three reaction times. Round %s's time to "
                       "one decimal place. Write the answer in seconds."
                       % who[i], ["Name", "Reaction time"], rows,
                       _fl(_rnd(vals[i], 1)), "num",
                       ["%s took %s s." % (who[i], _txt(vals[i])),
                        "Rounded to one decimal place that is %s s."
                        % _txt(_rnd(vals[i], 1))], tolerance=1e-6)

    if t == 9:                       # money to the nearest penny / pound
        if random.random() < 0.5:
            v = _mk(3, 1005, 9995)
            while _dp(v) < 3:        # the third place must be there to round
                v = _mk(3, 1005, 9995)
            return _nq("A price works out at £%s. Rounded to the nearest penny, "
                       "how much is that in pounds?" % _txt(v), _rnd(v, 2),
                       unit="£",
                       solution=["The thousandths digit decides the nearest penny.",
                                 "£%s rounds to £%s."
                                 % (_txt(v), format(_rnd(v, 2), "f"))])
        p = random.randint(150, 4990)
        return _iq("A jacket costs %s. Rounded to the nearest pound, how much "
                   "is that?" % _lb(p), _rnd(_D(p) / 100, 0), unit="£",
                   solution=["There are %d pence on top of the pounds." % (p % 100),
                             "%s rounds to £%s."
                             % (_lb(p), _txt(_rnd(_D(p) / 100, 0)))])

    # how many of these round to a given whole number
    w = random.randint(2, 20)
    vals = []
    n_hit = random.randint(1, 3)
    for k in range(4):
        if k < n_hit:
            vals.append(_D(w) + _D(random.randint(-49, 49)) / 100)
        else:
            vals.append(_D(w) + _D(random.choice([1, -1]) * random.randint(55, 145)) / 100)
    random.shuffle(vals)
    hits = len([v for v in vals if _rnd(v, 0) == w])
    return _iq("How many of these numbers round to %d when rounded to the "
               "nearest whole number? %s"
               % (w, ", ".join(_txt(v) for v in vals)), hits,
               solution=["Round each number in turn.",
                         "%d of them %s to %d." % (hits, "rounds" if hits == 1 else "round", w)])


@skill("Y6.5.c", "Compare and order decimals to three places", S5)
def _(d=1):
    d = _tier(d)

    def _vals(k):
        """k distinct decimals; at higher tiers they share a leading prefix and
        have different numbers of decimal places, which is the real test."""
        out = []
        w = random.randint(0, _by_d(d, 4, 9, 9))
        tries = 0
        while len(out) < k and tries < 400:
            tries += 1
            if d == 0:
                v = _D(w) + _D(random.randrange(1, 10)) / 10
            elif d == 1:
                v = _D(w) + _D(random.randrange(1, 100)) / 100
            else:
                tenth = random.randrange(0, 10)
                extra = random.choice([0, 0, random.randrange(1, 100)])
                v = _D(w) + _D(tenth) / 10 + _D(extra) / 1000
            if v > 0 and all(v != o for o in out):
                out.append(v)
        while len(out) < k:
            out.append(max(out) + _D("0.001"))
        return out

    t = _pick_t([1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 3])

    if t == 0:                       # which is larger
        a, b = _vals(2)
        return _nq("Which is larger, %s or %s? Write the larger number."
                   % (_txt(a), _txt(b)), max(a, b),
                   solution=["Line up the decimal points and compare the ones, "
                             "then the tenths, then the hundredths.",
                             "%s is larger than %s."
                             % (_txt(max(a, b)), _txt(min(a, b)))])

    if t == 1:                       # which is smaller
        a, b = _vals(2)
        return _nq("Which is smaller, %s or %s? Write the smaller number."
                   % (_txt(a), _txt(b)), min(a, b),
                   solution=["Compare place by place from the left.",
                             "%s is smaller than %s."
                             % (_txt(min(a, b)), _txt(max(a, b)))])

    if t == 2:                       # largest of four
        vs = _vals(4)
        return _nq("Write the largest of these numbers: %s"
                   % ", ".join(_txt(v) for v in vs), max(vs),
                   solution=["Line up the decimal points and compare place by "
                             "place.", "The largest is %s." % _txt(max(vs))])

    if t == 3:                       # smallest of four
        vs = _vals(4)
        return _nq("Write the smallest of these numbers: %s"
                   % ", ".join(_txt(v) for v in vs), min(vs),
                   solution=["A shorter decimal is not always the smaller one.",
                             "The smallest is %s." % _txt(min(vs))])

    if t == 4:                       # nth largest / nth smallest
        vs = _vals(4)
        k = random.choice([2, 3])
        if random.random() < 0.5:
            ans = sorted(vs, reverse=True)[k - 1]
            return _nq("Write the %s largest of these numbers: %s"
                       % (_ord(k), ", ".join(_txt(v) for v in vs)), ans,
                       solution=["In order, largest first: %s."
                                 % ", ".join(_txt(v) for v in sorted(vs, reverse=True)),
                                 "The %s largest is %s." % (_ord(k), _txt(ans))])
        ans = sorted(vs)[k - 1]
        return _nq("Write the %s smallest of these numbers: %s"
                   % (_ord(k), ", ".join(_txt(v) for v in vs)), ans,
                   solution=["In order, smallest first: %s."
                             % ", ".join(_txt(v) for v in sorted(vs)),
                             "The %s smallest is %s." % (_ord(k), _txt(ans))])

    if t == 5:                       # place the greater one on a number line
        w = random.randint(0, 8)
        a = _D(w) + _D(random.randrange(1, 100)) / 100
        b = _D(w) + _D(random.randrange(1, 100)) / 100
        while b == a:
            b = _D(w) + _D(random.randrange(1, 100)) / 100
        return _lineq("Which is greater, %s or %s? Place the greater number on "
                      "the number line." % (_txt(a), _txt(b)), max(a, b),
                      _D(w), _D(w + 1), _D("0.01"), _D("0.1"),
                      ["Both numbers lie between %d and %d." % (w, w + 1),
                       "%s is greater than %s."
                       % (_txt(max(a, b)), _txt(min(a, b)))])

    if t == 6:                       # true or false
        a, b = _vals(2)
        sign = pick([">", "<"])
        truth = (a > b) if sign == ">" else (a < b)
        return _sq("Is this comparison true or false? %s %s %s. "
                   "Type true or false." % (_txt(a), sign, _txt(b)),
                   "true" if truth else "false", placeholder="true / false",
                   solution=["%s is %s %s."
                             % (_txt(a), "greater than" if a > b else "less than",
                                _txt(b)),
                             "So the comparison is %s."
                             % ("true" if truth else "false")])

    if t == 7:                       # type the symbol
        a, b = _vals(2)
        return _sq("Which symbol makes this true: %s ___ %s? "
                   "Type < or >." % (_txt(a), _txt(b)),
                   ">" if a > b else "<", placeholder="< or >",
                   solution=["Compare the ones, then the tenths, hundredths and "
                             "thousandths.",
                             "%s %s %s." % (_txt(a), ">" if a > b else "<", _txt(b))])

    if t == 8:                       # race times: smallest wins
        p, q = _two_names()
        a, b = _vals(2)
        a = _D(random.randint(9500, 12500)) / 1000
        b = _D(random.randint(9500, 12500)) / 1000
        while b == a:
            b = _D(random.randint(9500, 12500)) / 1000
        return _sq("%s ran 100 m in %s seconds and %s ran it in %s seconds. "
                   "Who was faster? Type the name."
                   % (p, _txt(a), q, _txt(b)), p if a < b else q,
                   placeholder="a name",
                   solution=["The faster runner has the smaller time.",
                             "%s is less than %s, so %s was faster."
                             % (_txt(min(a, b)), _txt(max(a, b)),
                                p if a < b else q)])

    if t == 9:                       # table of measurements
        who = _names(4)
        vs = _vals(4)
        rows = [[who[k], _txt(vs[k])] for k in range(4)]
        want_max = random.random() < 0.5
        target = max(vs) if want_max else min(vs)
        name = who[vs.index(target)]
        return _tableq("The table shows how far each pupil threw a ball, in "
                       "metres. Who threw the %s distance? Type the name."
                       % ("greatest" if want_max else "shortest"),
                       ["Pupil", "Distance (m)"], rows, name, "str",
                       ["Compare the distances place by place.",
                        "%s threw %s m, the %s distance."
                        % (name, _txt(target),
                           "greatest" if want_max else "shortest")])

    if t == 10:                      # how many are greater than a boundary
        vs = _vals(5)
        cut = sorted(vs)[random.randint(0, 3)]
        n_more = len([v for v in vs if v > cut])
        return _iq("How many of these numbers are greater than %s? %s"
                   % (_txt(cut), ", ".join(_txt(v) for v in vs)), n_more,
                   solution=["Compare each number with %s." % _txt(cut),
                             "%d of them %s greater." % (n_more, "is" if n_more == 1 else "are")])

    # place the number exactly halfway between two decimals
    w = random.randint(0, 8)
    a = _D(w) + _D(random.randrange(10, 45)) / 100
    b = a + _D(random.randrange(1, 25)) * 2 / 100
    mid = (a + b) / 2
    return _lineq("What number is exactly halfway between %s and %s? "
                  "Place it on the number line." % (_txt(a), _txt(b)), mid,
                  _D(w), _D(w + 1), _D("0.01"), _D("0.1"),
                  ["The gap from %s to %s is %s."
                   % (_txt(a), _txt(b), _txt(b - a)),
                   "Half of that gap is %s, so halfway is %s."
                   % (_txt((b - a) / 2), _txt(mid))])


@skill("Y6.5.d", "Add and subtract decimals", S5)
def _(d=1):
    d = _tier(d)

    def _pairv():
        """Two decimals, usually with different numbers of decimal places."""
        combos = _by_d(d, [(1, 1), (1, 2), (2, 1)],
                       [(1, 2), (2, 1), (2, 2), (2, 3), (1, 3)],
                       [(1, 3), (3, 1), (2, 3), (3, 2), (3, 3), (1, 2)])
        p, q = pick(combos)
        hi = _by_d(d, 9, 40, 90)
        a = _mk(p, 10 ** p + 1, hi * 10 ** p)
        while _dp(a) == 0:           # never a whole number in disguise
            a = _mk(p, 10 ** p + 1, hi * 10 ** p)
        b = _mk(q, 10 ** q + 1, max(hi // 2, 2) * 10 ** q)
        while _dp(b) == 0:
            b = _mk(q, 10 ** q + 1, max(hi // 2, 2) * 10 ** q)
        return a, b

    t = _pick_t([1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 2])

    if t == 0:                       # bare addition
        a, b = _pairv()
        return _nq("Work out %s + %s." % (_txt(a), _txt(b)), a + b,
                   solution=["Line up the decimal points and fill the gaps with "
                             "zeros: %s + %s." % (_txt(a), _txt(b)),
                             "%s + %s = %s." % (_txt(a), _txt(b), _txt(a + b))])

    if t == 1:                       # bare subtraction (guarded positive)
        a, b = _pairv()
        big, small = max(a, b), min(a, b)
        if big == small:
            big = small + _D("0.5")
        return _nq("Work out %s − %s." % (_txt(big), _txt(small)), big - small,
                   solution=["Line up the decimal points, writing %s with the "
                             "same number of decimal places." % _txt(small),
                             "%s − %s = %s."
                             % (_txt(big), _txt(small), _txt(big - small))])

    if t == 2:                       # missing addend
        a, b = _pairv()
        return _nq("Complete: %s + ___ = %s" % (_txt(a), _txt(a + b)), b,
                   solution=["Subtract to undo the addition.",
                             "%s − %s = %s."
                             % (_txt(a + b), _txt(a), _txt(b))])

    if t == 3:                       # missing start of a subtraction
        a, b = _pairv()
        return _nq("Complete: ___ − %s = %s" % (_txt(b), _txt(a)), a + b,
                   solution=["Add to undo the subtraction.",
                             "%s + %s = %s." % (_txt(a), _txt(b), _txt(a + b))])

    if t == 4:                       # money and change
        who = pick(NAMES)
        item = pick(_SHOP)
        cost = random.randint(120, 1850)
        paid = random.choice([500, 1000, 2000])
        while paid <= cost:
            paid = random.choice([1000, 2000, 5000])
        change = paid - cost
        return _nq("%s pays with a %s note for %s costing %s. How much change "
                   "does %s get, in pounds?"
                   % (who, _lb(paid).replace(".00", ""), _a_word(item),
                      _lb(cost), who),
                   _D(change) / 100, unit="£",
                   solution=["%s − %s = %s."
                             % (_lb(paid), _lb(cost), _lb(change)),
                             "The change is %s." % _lb(change)])

    if t == 5:                       # three decimals added
        a = _mk(1, 11, 89)
        b = _mk(2, 105, 899)
        c = _mk(3, 1005, 8995)
        return _nq("Work out %s + %s + %s." % (_txt(a), _txt(b), _txt(c)),
                   a + b + c,
                   solution=["Add the first two: %s + %s = %s."
                             % (_txt(a), _txt(b), _txt(a + b)),
                             "Then %s + %s = %s."
                             % (_txt(a + b), _txt(c), _txt(a + b + c))])

    if t == 6:                       # place the total on a number line
        a = _mk(2, 105, 380)
        b = _mk(1, 11, 45)
        total = a + b
        lo = _D(int(total))
        return _lineq("Work out %s + %s, then place the total on the number "
                      "line." % (_txt(a), _txt(b)), total, lo, lo + 1,
                      _D("0.01"), _D("0.1"),
                      ["Write %s as %s so the places line up."
                       % (_txt(b), format(b.quantize(Decimal("0.01")), "f")),
                       "%s + %s = %s." % (_txt(a), _txt(b), _txt(total))])

    if t == 7:                       # receipt table
        who = pick(NAMES)
        items = random.sample(_FOOD, 3)
        prices = [random.randint(40, 195) for _ in range(3)]
        rows = [[items[k].capitalize(), _lb(prices[k])] for k in range(3)]
        total = sum(prices)
        return _tableq("The table shows what %s bought. What is the total cost, "
                       "in pounds?" % who, ["Item", "Price"], rows,
                       _fl(_D(total) / 100), "num",
                       ["Add the three prices: %s."
                        % " + ".join(_lb(p) for p in prices),
                        "The total is %s." % _lb(total)], tolerance=1e-6)

    if t == 8:                       # difference between two measures
        p, q = _two_names()
        a = _mk(2, 125, 185)
        b = _mk(3, 1250, 1850)
        while a == b:
            b = _mk(3, 1250, 1850)
        return _nq("%s is %s m tall and %s is %s m tall. What is the difference "
                   "in their heights, in metres?"
                   % (p, _txt(a), q, _txt(b)), abs(a - b), unit="m",
                   solution=["Write both heights with three decimal places.",
                             "%s − %s = %s m."
                             % (_txt(max(a, b)), _txt(min(a, b)),
                                _txt(abs(a - b)))])

    if t == 9:                       # capacity word problem, two steps
        who = pick(NAMES)
        a = _mk(2, 105, 285)
        b = _mk(1, 5, 18)
        c = _mk(2, 30, 95)
        left = a + b - c
        return _nq("A jug holds %s litres of juice. %s pours in %s litres more, "
                   "then pours out %s litres. How much juice is left in the "
                   "jug, in litres?" % (_txt(a), who, _txt(b), _txt(c)),
                   left, unit="l",
                   solution=["%s + %s = %s litres."
                             % (_txt(a), _txt(b), _txt(a + b)),
                             "%s − %s = %s litres."
                             % (_txt(a + b), _txt(c), _txt(left))])

    if t == 11:                      # choose the two decimals with a given
        #                              sum or difference (exactly one pair works)
        scale = _by_d(d, 10, 10, 100)
        lo, hi = (11, 98) if scale == 10 else (105, 985)
        xs = [11, 22, 34, 47, 61] if scale == 10 else [105, 218, 341, 472, 615]
        pool = [x for x in range(lo, hi + 1) if x % scale]   # never a whole number
        for _try in range(40):
            cand = random.sample(pool, 5)
            sums = [cand[i] + cand[j] for i in range(5) for j in range(i + 1, 5)]
            diffs = [abs(cand[i] - cand[j]) for i in range(5)
                     for j in range(i + 1, 5)]
            if len(set(sums)) == 10 and len(set(diffs)) == 10 and 0 not in diffs:
                xs = cand
                break
        i, j = random.sample(range(5), 2)
        a, b = _D(xs[i]) / scale, _D(xs[j]) / scale
        listed = ", ".join(_txt(_D(x) / scale) for x in sorted(xs))
        if random.random() < 0.5:
            target = a + b
            return _setq("Here is a list of decimals:  %s.  Choose the two "
                         "decimals from the list that have a sum of %s. Type "
                         "both decimals, separated by a comma."
                         % (listed, _txt(target)), [a, b],
                         ["Only one pair from the list adds to %s."
                          % _txt(target),
                          "%s + %s = %s." % (_txt(a), _txt(b), _txt(target))])
        big, small = max(a, b), min(a, b)
        target = big - small
        return _setq("Here is a list of decimals:  %s.  Choose the two decimals "
                     "from the list that have a difference of %s. Type both "
                     "decimals, separated by a comma."
                     % (listed, _txt(target)), [big, small],
                     ["Only one pair from the list has a difference of %s."
                      % _txt(target),
                      "%s − %s = %s." % (_txt(big), _txt(small), _txt(target))])

    # missing entry in a distance table
    who = _names(3)
    legs = [_mk(random.choice([1, 2]), 12, 480) for _ in range(3)]
    total = sum(legs, _D(0))
    k = random.randrange(3)
    rows = [[who[i] , _txt(legs[i])] for i in range(3)]
    rows[k][1] = "?"
    return _tableq("The table shows how far each pupil walked, in kilometres. "
                   "Altogether they walked %s km. How far did %s walk, in "
                   "kilometres?" % (_txt(total), who[k]),
                   ["Pupil", "Distance (km)"], rows, _fl(legs[k]), "num",
                   ["The two known distances add to %s km."
                    % _txt(total - legs[k]),
                    "%s − %s = %s km."
                    % (_txt(total), _txt(total - legs[k]), _txt(legs[k]))],
                   missing=(k, 1), tolerance=1e-6)


def _a_word(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


@skill("Y6.5.e", "Multiply and divide by 10, 100 and 1,000", S5)
def _(d=1):
    d = _tier(d)
    powers = _by_d(d, [10, 100], [10, 100, 1000], [10, 100, 1000])
    t = _pick_t([1, 1, 1, 1, 1, 1, 3, 1, 3, 3, 3, 2])

    if t == 0:                       # multiply
        k = pick(powers)
        v = _mk(_by_d(d, 1, 2, 3), 105, 9995)
        return _nq("Work out %s × %s." % (_txt(v), "{:,}".format(k)), v * k,
                   solution=["Multiplying by %s moves every digit %s to the "
                             "left." % ("{:,}".format(k), _places(k)),
                             "%s × %s = %s."
                             % (_txt(v), "{:,}".format(k), _txt(v * k))])

    if t == 1:                       # divide
        k = pick(powers)
        v = _mk(_by_d(d, 0, 1, 2), 105, 9995)
        return _nq("Work out %s ÷ %s." % (_txt(v), "{:,}".format(k)),
                   _D(v) / k,
                   solution=["Dividing by %s moves every digit %s to the "
                             "right." % ("{:,}".format(k), _places(k)),
                             "%s ÷ %s = %s."
                             % (_txt(v), "{:,}".format(k), _txt(_D(v) / k))])

    if t == 2:                       # missing power (multiplication)
        k = pick(powers)
        v = _mk(_by_d(d, 1, 2, 3), 105, 995)
        return _iq("Complete: %s × ___ = %s" % (_txt(v), _txt(v * k)), k,
                   solution=["The digits have moved %s to the left."
                             % _places(k),
                             "%s × %s = %s."
                             % (_txt(v), "{:,}".format(k), _txt(v * k))])

    if t == 3:                       # missing start (division)
        k = pick(powers)
        v = _mk(_by_d(d, 1, 2, 2), 105, 995)
        return _nq("Complete: ___ ÷ %s = %s" % ("{:,}".format(k), _txt(v)),
                   v * k,
                   solution=["Undo the division by multiplying.",
                             "%s × %s = %s."
                             % (_txt(v), "{:,}".format(k), _txt(v * k))])

    if t == 4:                       # metric conversion
        who = pick(NAMES)
        # (small unit, big unit, factor, sentence about the small unit,
        #  sentence about the big unit)
        small, big, k, s_up, s_down = pick([
            ("cm", "m", 100,
             "A rope measures %s cm. How long is the rope in m?",
             "A rope measures %s m. How long is the rope in cm?"),
            ("m", "km", 1000,
             "%s walks %s m. How far is that in km?",
             "%s walks %s km. How far is that in m?"),
            ("g", "kg", 1000,
             "A parcel has a mass of %s g. What is that mass in kg?",
             "A parcel has a mass of %s kg. What is that mass in g?"),
            ("ml", "l", 1000,
             "A bottle holds %s ml of water. How much is that in l?",
             "A bottle holds %s l of water. How much is that in ml?"),
            ("mm", "cm", 10,
             "A nail is %s mm long. How long is the nail in cm?",
             "A nail is %s cm long. How long is the nail in mm?"),
        ])
        if random.random() < 0.5:                    # small -> big (divide)
            n = random.randint(105, 9950) if k > 10 else random.randint(11, 199)
            text = s_up % ((who, "{:,}".format(n)) if "%s walks" in s_up
                           else "{:,}".format(n))
            return _nq(text, _D(n) / k, unit=big,
                       solution=["There are %s %s in 1 %s."
                                 % ("{:,}".format(k), small, big),
                                 "%s ÷ %s = %s %s."
                                 % ("{:,}".format(n), "{:,}".format(k),
                                    _txt(_D(n) / k), big)])
        v = _mk(_by_d(d, 1, 2, 3), _by_d(d, 11, 105, 105), _by_d(d, 99, 995, 995))   # big -> small (multiply)
        text = s_down % ((who, _txt(v)) if "%s walks" in s_down else _txt(v))
        return _nq(text, v * k, unit=small,
                   solution=["1 %s is %s %s." % (big, "{:,}".format(k), small),
                             "%s × %s = %s %s."
                             % (_txt(v), "{:,}".format(k), _txt(v * k), small)])

    if t == 5:                       # two-step chain
        k1 = pick(powers)
        k2 = pick([k for k in powers if k != k1])
        v = _mk(_by_d(d, 1, 2, 3), 105, 995)
        res = _D(v) * k1 / k2
        return _nq("Work out %s × %s ÷ %s."
                   % (_txt(v), "{:,}".format(k1), "{:,}".format(k2)), res,
                   solution=["%s × %s = %s."
                             % (_txt(v), "{:,}".format(k1), _txt(v * k1)),
                             "%s ÷ %s = %s."
                             % (_txt(v * k1), "{:,}".format(k2), _txt(res))])

    if t == 6:                       # conversion table with a missing cell
        k = pick([10, 100, 1000])
        ins = [_mk(_by_d(d, 1, 2, 2), 105, 995) for _ in range(4)]
        rows = [[_txt(v), _txt(v * k)] for v in ins]
        i = random.randrange(4)
        rows[i][1] = "?"
        return _tableq("Every number in the table has been multiplied by %s. "
                       "What number belongs in the empty cell?"
                       % "{:,}".format(k),
                       ["Number", "× %s" % "{:,}".format(k)], rows,
                       _fl(ins[i] * k), "num",
                       ["Each output is the input multiplied by %s."
                        % "{:,}".format(k),
                        "%s × %s = %s."
                        % (_txt(ins[i]), "{:,}".format(k), _txt(ins[i] * k))],
                       missing=(i, 1), tolerance=1e-6)

    if t == 7:                       # word problem: many identical items
        who = pick(NAMES)
        k = pick([10, 100, 1000])
        mass = _mk(_by_d(d, 1, 2, 3), 105, 950)
        return _nq("One bead has a mass of %s grams. What is the mass of %s "
                   "identical beads, in grams?" % (_txt(mass), "{:,}".format(k)),
                   mass * k, unit="g",
                   solution=["%s beads means %s × %s."
                             % ("{:,}".format(k), _txt(mass), "{:,}".format(k)),
                             "The mass is %s g." % _txt(mass * k)])

    if t == 8:                       # place the result on a number line
        if random.random() < 0.5:
            v = _mk(2, 5, 95)                       # 0.05 ... 0.95
            res = v * 10                            # 0.5 ... 9.5, a multiple of 0.1
            return _lineq("Work out %s × 10, then place your answer on the "
                          "number line." % _txt(v), res, 0, 10,
                          _D("0.1"), _D("1"),
                          ["Multiplying by 10 moves every digit one place to "
                           "the left.",
                           "%s × 10 = %s." % (_txt(v), _txt(res))])
        v = _mk(1, 5, 95)                           # 0.5 ... 9.5
        res = _D(v) / 10                            # 0.05 ... 0.95
        return _lineq("Work out %s ÷ 10, then place your answer on the number "
                      "line." % _txt(v), res, 0, 1, _D("0.01"), _D("0.1"),
                      ["Dividing by 10 moves every digit one place to the "
                       "right.",
                       "%s ÷ 10 = %s." % (_txt(v), _txt(res))])

    if t == 10:                      # decimal division patterns over
        #                              increasing place values
        n = pick([2, 3, 4, 5, 6, 8])
        q = 11
        for _try in range(40):
            cand = random.randint(11, 49)
            if (cand * n) % 10:
                q = cand
                break
        quot = _D(q) / 10                       # e.g. 1.2
        div = quot * n                          # e.g. 4.8

        def _c(v):
            """Tidy UK number text, with a comma in the thousands."""
            return ("{:,}".format(int(v)) if _D(v) == int(_D(v)) else _txt(v))

        rows = [[("%s ÷ %d" % (_c(div * (10 ** i)), n)),
                 _c(quot * (10 ** i))] for i in range(4)]
        rows[3][1] = "?"
        ans = quot * 1000
        return _tableq("This pattern of decimal divisions runs over increasing "
                       "place values. What answer belongs in the empty cell?",
                       ["Division", "Answer"], rows, _fl(ans), "num",
                       ["Each dividend is ten times the one above it, so each "
                        "answer is ten times the answer above it.",
                        "%s ÷ %d = %s."
                        % (_c(div * 1000), n, _c(ans))],
                       missing=(3, 1), tolerance=1e-6)

    if t == 11:                      # divide a decimal by a power of ten:
        #                              find the missing number
        k = pick(powers)
        v = _mk(_by_d(d, 1, 2, 2), 105, 995)
        return _iq("This decimal is divided by a power of ten. Find the missing "
                   "number:  %s ÷ ___ = %s" % (_txt(v), _txt(_D(v) / k)), k,
                   solution=["Every digit has moved %s to the right."
                             % _places(k),
                             "%s ÷ %s = %s."
                             % (_txt(v), "{:,}".format(k), _txt(_D(v) / k))])

    # compare two expressions
    k1, k2 = pick([10, 100, 1000]), pick([10, 100, 1000])
    a = _mk(_by_d(d, 1, 2, 2), 105, 995)
    b = _mk(_by_d(d, 1, 2, 2), 105, 995)
    va, vb = a * k1, _D(b) / k2
    while va == vb:
        b = _mk(2, 105, 995)
        vb = _D(b) / k2
    bigger = max(va, vb)
    return _nq("Which is greater, %s × %s or %s ÷ %s? Write the greater value."
               % (_txt(a), "{:,}".format(k1), _txt(b), "{:,}".format(k2)),
               bigger,
               solution=["%s × %s = %s and %s ÷ %s = %s."
                         % (_txt(a), "{:,}".format(k1), _txt(va),
                            _txt(b), "{:,}".format(k2), _txt(vb)),
                         "The greater value is %s." % _txt(bigger)])


@skill("Y6.5.f", "Multiply a decimal by a whole number", S5)
def _(d=1):
    d = _tier(d)

    def _fac():
        dp = _by_d(d, 1, random.choice([1, 2]), random.choice([1, 2, 2]))
        a = _mk(dp, 11 if dp == 1 else 105, 95 if dp == 1 else 995)
        n = random.randint(*_by_d(d, (2, 6), (3, 12), (4, 24)))
        return a, n

    t = _pick_t([1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 2])

    if t == 0:                       # bare multiplication
        a, n = _fac()
        return _nq("Work out %s × %d." % (_txt(a), n), a * n,
                   solution=["Ignore the point: %s × %d = %s."
                             % (_txt(a * (10 ** _dp(a))), n,
                                _txt(a * n * (10 ** _dp(a)))),
                             "Put the point back %s from the right: %s."
                             % (_places(10 ** _dp(a)), _txt(a * n))])

    if t == 1:                       # cost of several items
        who = pick(NAMES)
        item = pick(_SHOP)
        p = random.randint(45, 395)
        n = random.randint(*_by_d(d, (2, 5), (3, 9), (4, 15)))
        return _nq("%s buys %d %s at %s each. What is the total cost, in "
                   "pounds?" % (who, n, _plural(item), _lb(p)),
                   _D(p * n) / 100, unit="£",
                   solution=["%s × %d = %s."
                             % (_lb(p), n, _lb(p * n)),
                             "The total cost is %s." % _lb(p * n)])

    if t == 2:                       # measures
        a, n = _fac()
        return _nq("A shelf is %s metres long. What is the total length of %d "
                   "such shelves, in metres?" % (_txt(a), n), a * n, unit="m",
                   solution=["%d lots of %s m." % (n, _txt(a)),
                             "%s × %d = %s m." % (_txt(a), n, _txt(a * n))])

    if t == 3:                       # missing factor
        a, n = _fac()
        if random.random() < 0.5:
            return _nq("Complete: ___ × %d = %s" % (n, _txt(a * n)), a,
                       solution=["Divide to undo the multiplication.",
                                 "%s ÷ %d = %s." % (_txt(a * n), n, _txt(a))])
        return _iq("Complete: %s × ___ = %s" % (_txt(a), _txt(a * n)), n,
                   solution=["Divide to undo the multiplication.",
                             "%s ÷ %s = %d." % (_txt(a * n), _txt(a), n)])

    if t == 4:                       # strip model
        a, n = _fac()
        n = min(n, 10)
        return _stripq("The strip model shows %d equal parts, each of %s. "
                       "What is the total?" % (n, _txt(a)),
                       n, _txt(a), "?", "total", _fl(a * n), "num",
                       ["%d equal parts of %s." % (n, _txt(a)),
                        "%d × %s = %s." % (n, _txt(a), _txt(a * n))],
                       tolerance=1e-6)

    if t == 5:                       # price list table
        items = random.sample(_FOOD, 3)
        prices = [random.randint(40, 165) for _ in range(3)]
        i = random.randrange(3)
        n = random.randint(3, 9)
        rows = [[items[k].capitalize(), _lb(prices[k])] for k in range(3)]
        return _tableq("Use the price list. What is the cost of %d %s, in "
                       "pounds?" % (n, _plural(items[i])),
                       ["Item", "Price"], rows,
                       _fl(_D(prices[i] * n) / 100), "num",
                       ["One %s costs %s." % (items[i], _lb(prices[i])),
                        "%s × %d = %s." % (_lb(prices[i]), n, _lb(prices[i] * n))],
                       tolerance=1e-6)

    if t == 6:                       # two-step
        a = _mk(1, 11, 49)
        b = _mk(1, 11, 49)
        m = random.randint(2, 6)
        n = random.randint(2, 6)
        return _nq("Work out %s × %d + %s × %d."
                   % (_txt(a), m, _txt(b), n), a * m + b * n,
                   solution=["%s × %d = %s and %s × %d = %s."
                             % (_txt(a), m, _txt(a * m), _txt(b), n, _txt(b * n)),
                             "%s + %s = %s."
                             % (_txt(a * m), _txt(b * n), _txt(a * m + b * n))])

    if t == 7:                       # use a known fact
        a, n = _fac()
        return _nq("%s × %d = %s. Use this fact to work out %s × %d."
                   % (_txt(a), n, _txt(a * n), _txt(a), n * 2), a * n * 2,
                   solution=["%d is double %d." % (n * 2, n),
                             "Double %s to get %s."
                             % (_txt(a * n), _txt(a * n * 2))])

    if t == 8:                       # compare two products
        a = _mk(1, 15, 49)
        b = _mk(1, 15, 49)
        m = random.randint(3, 8)
        n = random.randint(3, 8)
        while a * m == b * n:
            n = random.randint(3, 8)
        return _nq("Which is greater, %s × %d or %s × %d? Write the greater "
                   "value." % (_txt(a), m, _txt(b), n), max(a * m, b * n),
                   solution=["%s × %d = %s and %s × %d = %s."
                             % (_txt(a), m, _txt(a * m), _txt(b), n, _txt(b * n)),
                             "The greater value is %s."
                             % _txt(max(a * m, b * n))])

    if t == 10:                      # estimate the product of a two-digit
        #                              whole number and a decimal
        a = _mk(2, 105, 995)
        for _try in range(40):
            if a - int(a) != _D("0.5"):
                break
            a = _mk(2, 105, 995)
        n = random.randint(11, 89)
        for _try in range(40):
            if n % 10 != 5:
                break
            n = random.randint(11, 89)
        ra = int(_rnd(a, 0))
        rn = int(_rnd(_D(n) / 10, 0)) * 10
        return _iq("Estimate the product %s × %d by rounding %s to the nearest "
                   "whole number and %d to the nearest ten."
                   % (_txt(a), n, _txt(a), n), ra * rn,
                   solution=["%s rounds to %d and %d rounds to %d."
                             % (_txt(a), ra, n, rn),
                             "The estimate is %d × %d = %s."
                             % (ra, rn, "{:,}".format(ra * rn))])

    # place the product on a number line
    a = _mk(2, 105, 240)
    n = random.randint(2, 4)
    prod = a * n
    lo = _D(int(prod))
    return _lineq("Work out %s × %d, then place your answer on the number line."
                  % (_txt(a), n), prod, lo, lo + 1, _D("0.01"), _D("0.1"),
                  ["%s × %d = %s." % (_txt(a), n, _txt(prod)),
                   "That lies between %s and %s." % (_txt(lo), _txt(lo + 1))])


@skill("Y6.5.g", "Multiply decimals by whole numbers", S5)
def _(d=1):
    # NC Year 6: multiply one-digit numbers with up to two decimal places by whole numbers.
    # (Decimal x decimal is KS3 and lives in the Year 7 bank.)
    d = _tier(d)
    t = _pick_t([1, 1, 3, 1, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1])

    def _one():
        """A one-digit number with one or two decimal places: 0.7, 3.4, 0.06, 2.35."""
        dp = 1 if d == 0 else pick([1, 2])
        while True:
            a = _D(random.randint(1, 9 * 10 ** dp + 9)) / 10 ** dp
            if a != a.to_integral_value() and a < 10:
                return a

    def _k():
        return random.randint(2, _by_d(d, 5, 9, 12))

    if t == 0:                       # bare decimal × whole number
        a, k = _one(), _k()
        n = int(a * 10 ** _dp(a))
        return _nq("Work out %s × %d." % (_txt(a), k), a * k,
                   solution=["%d × %d = %d." % (n, k, n * k),
                             "%s has %s, so divide by %d: %d ÷ %d = %s."
                             % (_txt(a), _pl(_dp(a), "decimal place"), 10 ** _dp(a), n * k, 10 ** _dp(a), _txt(a * k))])

    if t == 1:                       # hundredths × whole number
        a = _D(random.randint(1, 9)) / 100
        k = _k()
        return _nq("Work out %s × %d." % (_txt(a), k), a * k,
                   solution=["%s × %d = %s." % (_pl(int(a * 100), "hundredth"), k, _pl(int(a * 100) * k, "hundredth")),
                             "That is %s." % _txt(a * k)])

    if t == 2:                       # hundredths square model
        a = _D(random.randint(1, 9)) / 100
        k = random.randint(2, min(9, 100 // int(a * 100)))
        c = int(a * k * 100)
        return _gridshade("The square is one whole split into 100 equal parts. "
                          "Shade it to show %s × %d." % (_txt(a), k),
                          c, ["%s × %d = %s." % (_txt(a), k, _txt(a * k)),
                              "%s is %d hundredths, so shade %d small squares."
                              % (_txt(a * k), c, c)])

    if t == 3:                       # missing whole-number factor
        a, k = _one(), _k()
        return _iq("Complete: %s × ___ = %s" % (_txt(a), _txt(a * k)), k,
                   solution=["Divide to undo the multiplication.",
                             "%s ÷ %s = %d." % (_txt(a * k), _txt(a), k)])

    if t == 4:                       # perimeter / length in context
        a, k = _one(), _k()
        while a >= 3:
            a = _one()
        thing = pick(["fence panel", "shelf", "plank", "piece of track"])
        return _nq("Each %s is %s m long. %d of them are laid end to end. How long is the row, "
                   "in metres?" % (thing, _txt(a), k), a * k, unit="m",
                   solution=["%s × %d = %s." % (_txt(a), k, _txt(a * k)),
                             "The row is %s m long." % _txt(a * k)])

    if t == 5:                       # compare two products
        a, k = _one(), _k()
        c, m = _one(), _k()
        while a * k == c * m:
            c, m = _one(), _k()
        return _nq("Which is greater, %s × %d or %s × %d? Write the greater "
                   "value." % (_txt(a), k, _txt(c), m), max(a * k, c * m),
                   solution=["%s × %d = %s and %s × %d = %s."
                             % (_txt(a), k, _txt(a * k), _txt(c), m, _txt(c * m)),
                             "The greater value is %s." % _txt(max(a * k, c * m))])

    if t == 6:                       # reasoning: bigger or smaller than the whole number
        a, k = _one(), _k()
        big = a > 1
        return _sq("Is %s × %d greater than or less than %d? Type greater or less." % (_txt(a), k, k),
                   "greater" if big else "less", placeholder="greater / less",
                   solution=["%s is %s than 1, so %d lots of it is %s than %d."
                             % (_txt(a), "more" if big else "less", k, "more" if big else "less", k),
                             "%s × %d = %s." % (_txt(a), k, _txt(a * k))])

    if t == 7:                       # use a known whole-number fact
        a, k = _one(), _k()
        n = int(a * 10 ** _dp(a))
        return _nq("%d × %d = %d. Use this fact to work out %s × %d." % (n, k, n * k, _txt(a), k), a * k,
                   solution=["%s is %d ÷ %d." % (_txt(a), n, 10 ** _dp(a)),
                             "So the product is %d ÷ %d = %s." % (n * k, 10 ** _dp(a), _txt(a * k))])

    if t == 8:                       # a chain with two whole numbers
        a = _one()
        k, m = random.randint(2, 5), random.randint(2, 5)
        return _nq("Work out %s × %d × %d." % (_txt(a), k, m), a * k * m,
                   solution=["%s × %d = %s." % (_txt(a), k, _txt(a * k)),
                             "%s × %d = %s." % (_txt(a * k), m, _txt(a * k * m))])

    if t == 10:                      # estimate first
        whole = random.randint(1, 9)
        a = _D("%d.%d" % (whole, pick([1, 2, 3, 4, 6, 7, 8, 9])))     # never a 5, so no tie
        k = _k()
        ra = int(_rnd(a, 0))
        return _iq("Estimate %s × %d by rounding %s to the nearest whole number." % (_txt(a), k, _txt(a)), ra * k,
                   solution=["%s rounds to %d." % (_txt(a), ra), "The estimate is %d × %d = %d." % (ra, k, ra * k)])

    if t == 11:                      # measures: mass of several items
        a, k = _one(), _k()
        item = pick(["bag of flour", "parcel", "tin of paint", "box of tiles"])
        return _nq("One %s weighs %s kg. What do %d of them weigh altogether, in kg?" % (item, _txt(a), k), a * k,
                   unit="kg", solution=["%s × %d = %s kg." % (_txt(a), k, _txt(a * k))])

    if t == 12:                      # money: price × quantity
        p = _D(random.randint(15, 99)) / 100
        k = random.randint(3, 9)
        item = pick(["pen", "apple", "stamp", "notebook", "rubber"])
        return _nq("One %s costs £%s. How much do %d of them cost, in pounds?" % (item, "%.2f" % p, k), p * k, unit="£",
                   solution=["%d × %dp = %dp." % (k, int(p * 100), int(p * 100) * k),
                             "That is %s." % _lb(int(p * k * 100))])

    if t == 13:                      # spot the place-value mistake
        a, k = _one(), _k()
        n = int(a * 10 ** _dp(a))
        who = pick(NAMES)
        return _nq("%s says %s × %d = %d. That is wrong. What is the correct answer?" % (who, _txt(a), k, n * k),
                   a * k, solution=["%s forgot to put the decimal point back." % who,
                                    "%d × %d = %d, and %s has %s, so %s × %d = %s."
                                    % (n, k, n * k, _txt(a), _pl(_dp(a), "decimal place"), _txt(a), k, _txt(a * k))])

    # read the shaded square as a product
    a = _D(random.randint(1, 9)) / 100
    k = random.randint(2, min(9, 100 // int(a * 100)))
    c = int(a * k * 100)
    return _gridread("The shaded part of this hundredths square shows the "
                     "answer to %s × %d. Write that answer as a decimal."
                     % (_txt(a), k), c, _fl(a * k), "num",
                     ["%d of the 100 small squares are shaded, which is %d/100." % (c, c),
                      "%s × %d = %s." % (_txt(a), k, _txt(a * k))],
                     tolerance=1e-6)


@skill("Y6.5.h", "Divide decimals by whole numbers", S5)
def _(d=1):
    d = _tier(d)

    def _exact():
        """A division that comes out exactly."""
        n = random.randint(*_by_d(d, (2, 5), (2, 9), (3, 12)))
        dp = _by_d(d, 1, random.choice([1, 2]), random.choice([2, 2, 3]))
        q = _mk(dp, 11 if dp == 1 else (105 if dp == 2 else 1005),
                95 if dp == 1 else (995 if dp == 2 else 9995))
        return q * n, n, q

    t = _pick_t([1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3])

    if t == 0:                       # bare exact division
        a, n, q = _exact()
        return _nq("Work out %s ÷ %d." % (_txt(a), n), q,
                   solution=["Divide as usual, keeping the decimal point in "
                             "line.", "%s ÷ %d = %s." % (_txt(a), n, _txt(q))])

    if t == 1:                       # money shared
        who = pick(NAMES)
        n = random.randint(3, 8)
        each = random.randint(65, 480)
        total = each * n
        return _nq("%s shares %s equally between %d friends. How much does "
                   "each friend get, in pounds?" % (who, _lb(total), n),
                   _D(each) / 100, unit="£",
                   solution=["%s ÷ %d." % (_lb(total), n),
                             "Each friend gets %s." % _lb(each)])

    if t == 2:                       # measures shared
        a, n, q = _exact()
        return _nq("A ribbon %s metres long is cut into %d equal pieces. How "
                   "long is each piece, in metres?" % (_txt(a), n), q, unit="m",
                   solution=["%s ÷ %d." % (_txt(a), n),
                             "Each piece is %s m long." % _txt(q)])

    if t == 3:                       # inexact -> round the quotient
        n = random.randint(3, 9)
        a = _mk(1, 25, 480)
        while _dp(a) == 0:           # keep a genuine decimal dividend
            a = _mk(1, 25, 480)
        exact = _D(a) / n
        places = pick([1, 2])
        r = _rnd(exact, places)
        return _nq("Work out %s ÷ %d. Give your answer to %s."
                   % (_txt(a), n, "one decimal place" if places == 1
                      else "two decimal places"), r,
                   solution=["%s ÷ %d = %s (to 4 decimal places)."
                             % (_txt(a), n, _txt(_rnd(exact, 4))),
                             "Rounded to %s that is %s."
                             % ("one decimal place" if places == 1
                                else "two decimal places", format(r, "f"))])

    if t == 4:                       # missing divisor / dividend
        a, n, q = _exact()
        if random.random() < 0.5:
            return _iq("Complete: %s ÷ ___ = %s" % (_txt(a), _txt(q)), n,
                       solution=["Divide the total by the quotient.",
                                 "%s ÷ %s = %d." % (_txt(a), _txt(q), n)])
        return _nq("Complete: ___ ÷ %d = %s" % (n, _txt(q)), a,
                   solution=["Multiply to undo the division.",
                             "%s × %d = %s." % (_txt(q), n, _txt(a))])

    if t == 5:                       # strip model
        a, n, q = _exact()
        n = min(n, 10)
        a = q * n
        return _stripq("The strip model shows %s split into %d equal parts. "
                       "How much is one part?" % (_txt(a), n),
                       n, "?", _txt(a), "part", _fl(q), "num",
                       ["%s ÷ %d." % (_txt(a), n),
                        "One part is %s." % _txt(q)], tolerance=1e-6)

    if t == 6:                       # bill split table
        who = _names(3)
        items = random.sample(_FOOD, 3)
        prices = [random.randint(45, 185) for _ in range(3)]
        total = sum(prices)
        n = 3
        while total % n:
            prices[0] += 1
            total = sum(prices)
        rows = [[items[k].capitalize(), _lb(prices[k])] for k in range(3)]
        return _tableq("%s, %s and %s share the cost of everything in the table "
                       "equally. How much does each pupil pay, in pounds?"
                       % (who[0], who[1], who[2]), ["Item", "Price"], rows,
                       _fl(_D(total // n) / 100), "num",
                       ["The total is %s." % _lb(total),
                        "%s ÷ 3 = %s each." % (_lb(total), _lb(total // n))],
                       tolerance=1e-6)

    if t == 7:                       # two-step: add then divide
        a = _mk(1, 15, 95)
        b = _mk(1, 15, 95)
        n = pick([2, 4, 5])
        tot = a + b
        while (tot * 100) % n:
            b = _mk(1, 15, 95)
            tot = a + b
        return _nq("Work out (%s + %s) ÷ %d." % (_txt(a), _txt(b), n),
                   _D(tot) / n,
                   solution=["%s + %s = %s." % (_txt(a), _txt(b), _txt(tot)),
                             "%s ÷ %d = %s." % (_txt(tot), n, _txt(_D(tot) / n))])

    if t == 8:                       # mean of decimals
        n = pick([4, 5])
        vals = [_mk(1, 15, 95) for _ in range(n)]
        tot = sum(vals, _D(0))
        mean = _D(tot) / n
        if _dp(mean) > 2:
            mean = _rnd(mean, 2)
            return _nq("Work out the mean of these masses, in kilograms, giving "
                       "your answer to two decimal places: %s"
                       % ", ".join(_txt(v) for v in vals), mean, unit="kg",
                       solution=["The total is %s kg." % _txt(tot),
                                 "%s ÷ %d = %s kg to two decimal places."
                                 % (_txt(tot), n, _txt(mean))])
        return _nq("Work out the mean of these masses, in kilograms: %s"
                   % ", ".join(_txt(v) for v in vals), mean, unit="kg",
                   solution=["The total is %s kg." % _txt(tot),
                             "%s ÷ %d = %s kg." % (_txt(tot), n, _txt(mean))])

    if t == 10:                      # divide decimals using area models:
        #                              complete the equation
        n = pick([2, 4, 5])
        q_h = random.randint(1, 100 // n)
        shaded = q_h * n
        return _gridread("This area model is one whole split into 100 equal "
                         "squares, and %s of it is shaded. Use the area model "
                         "to complete the equation:  %s ÷ %d = ___"
                         % (_txt(_D(shaded) / 100), _txt(_D(shaded) / 100), n),
                         shaded, _fl(_D(q_h) / 100), "num",
                         ["Split the %d shaded squares into %d equal groups."
                          % (shaded, n),
                          "%d ÷ %d = %s, so the answer is %s."
                          % (shaded, n, _pl(q_h, "square"), _txt(_D(q_h) / 100))],
                         tolerance=1e-6)

    if t == 11:                      # divide decimals using area models: shade
        #                              the answer
        n = pick([2, 4, 5])
        q_h = random.randint(1, 100 // n)
        shaded = q_h * n
        return _gridshade("This area model is one whole split into 100 equal "
                          "squares. Work out %s ÷ %d, then shade the area model "
                          "to show the answer."
                          % (_txt(_D(shaded) / 100), n), q_h,
                          ["%s is %d of the 100 small squares."
                           % (_txt(_D(shaded) / 100), shaded),
                           "%d ÷ %d = %d, so shade %s, which is %s."
                           % (shaded, n, q_h, _pl(q_h, "square"), _txt(_D(q_h) / 100))])

    # cost per item to the nearest penny
    n = random.randint(3, 9)
    total = random.randint(250, 3500)
    while total % n == 0:
        total = random.randint(250, 3500)
    each = int(_rnd(_D(total) / n, 0))
    item = pick(_SHOP)
    return _iq("A pack of %d %s costs %s. To the nearest penny, how much does "
               "one %s cost? Give your answer in pence."
               % (n, _plural(item), _lb(total), item), each, unit="p",
               solution=["%d ÷ %d = %s pence." % (total, n, _txt(_rnd(_D(total) / n, 3))),
                         "To the nearest penny that is %dp." % each])


@skill("Y6.5.i", "Decimal problems with rounding in context", S5)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 3, 1, 1, 3])

    if t == 0:                       # how many can be bought (round down)
        who = pick(NAMES)
        item = pick(_SHOP)
        if d == 0:                   # easy: prices in 50p steps
            price = pick([50, 100, 150, 200, 250])
        else:
            price = random.randint(85, 445) if d == 1 else random.randint(185, 999)
        budget = random.randint(price * 3, price * _by_d(d, 8, 12, 20))
        while budget % price == 0:
            budget += 7
        n = budget // price
        return _iq("%s has %s to spend on %s costing %s each. What is the "
                   "greatest number of %s that %s can buy?"
                   % (who, _lb(budget), _plural(item), _lb(price),
                      _plural(item), who), n,
                   solution=["%s ÷ %s = %s."
                             % (_lb(budget), _lb(price),
                                _txt(_rnd(_D(budget) / price, 2))),
                             "Only whole %s can be bought, so the answer is %d."
                             % (_plural(item), n)])

    if t == 1:                       # how many containers (round up)
        cap = _by_d(d, _D(pick(["1.5", "2.5", "0.5", "2", "3"])), _mk(1, 15, 45), _mk(2, 105, 495))
        total = _by_d(d, _D(random.randint(10, 60)), _mk(1, 200, 900), _mk(2, 2005, 9995))
        n = -((-total) // cap)
        n = int(n)
        while _D(n - 1) * cap >= total:
            n -= 1
        while _D(n) * cap < total:
            n += 1
        return _iq("A tank holds %s litres of water. It is emptied into jugs "
                   "that each hold %s litres. What is the smallest number of "
                   "jugs needed to hold all the water?"
                   % (_txt(total), _txt(cap)), n,
                   solution=["%s ÷ %s = %s."
                             % (_txt(total), _txt(cap),
                                _txt(_rnd(_D(total) / cap, 2))),
                             "%d jugs hold only %s litres, so %d jugs are needed."
                             % (n - 1, _txt(cap * (n - 1)), n)])

    if t == 2:                       # cost per unit, nearest penny
        n = pick(_by_d(d, [2, 4, 5], list(range(3, 13)), list(range(7, 20))))
        lo, hi = _by_d(d, (200, 1500), (200, 4500), (1000, 9999))
        total = random.randint(lo, hi)
        while total % n == 0:
            total = random.randint(lo, hi)
        each = int(_rnd(_D(total) / n, 0))
        return _iq("%d identical tickets cost %s altogether. To the nearest "
                   "penny, how much does one ticket cost? Give your answer in "
                   "pence." % (n, _lb(total)), each, unit="p",
                   solution=["%s ÷ %d = %s pence."
                             % (_lb(total), n, _txt(_rnd(_D(total) / n, 3))),
                             "To the nearest penny that is %dp." % each])

    if t == 3:                       # total cost, nearest pound
        n = random.randint(*_by_d(d, (2, 5), (4, 14), (12, 29)))
        price = random.randint(*_by_d(d, (23, 137), (115, 685), (115, 985))) * (5 if d == 0 else 1)
        total = n * price
        return _iq("A shop sells notebooks at %s each. What is the cost of %d "
                   "notebooks, rounded to the nearest pound?" % (_lb(price), n),
                   _rnd(_D(total) / 100, 0), unit="£",
                   solution=["%s × %d = %s." % (_lb(price), n, _lb(total)),
                             "Rounded to the nearest pound that is £%s."
                             % _txt(_rnd(_D(total) / 100, 0))])

    if t == 4:                       # mean rounded to one decimal place
        n = pick(_by_d(d, [4], [4, 6, 7], [7, 8, 9]))
        # easy: whole-number heights; stretch: two decimal places
        vals = [_by_d(d, _D(random.randint(10, 30)), _mk(1, 105, 195), _mk(2, 1005, 1995))
                for _ in range(n)]
        tot = sum(vals, _D(0))
        mean = _rnd(_D(tot) / n, 1)
        return _nq("The heights of %d plants, in centimetres, are %s. What is "
                   "the mean height, to one decimal place?"
                   % (n, ", ".join(_txt(v) for v in vals)), mean, unit="cm",
                   solution=["The total height is %s cm." % _txt(tot),
                             "%s ÷ %d = %s cm to one decimal place."
                             % (_txt(tot), n, format(mean, "f"))])

    if t == 5:                       # cutting lengths (round down) or leftover
        # easy: tenths, leaving out 0.2 and 0.5, which always fit whole metres exactly
        piece = _by_d(d, _D(pick(["0.3", "0.4", "0.6", "0.7", "0.8", "0.9"])), _mk(2, 25, 95),
                      _mk(2, 105, 295))
        total = random.randint(*_by_d(d, (3, 9), (3, 9), (10, 25)))
        n = int(_D(total) / piece)
        while _D(n + 1) * piece <= total:
            n += 1
        left = _D(total) - piece * n
        if random.random() < 0.5:
            return _iq("A rope %d metres long is cut into pieces %s metres "
                       "long. How many whole pieces can be cut?"
                       % (total, _txt(piece)), n,
                       solution=["%d ÷ %s = %s."
                                 % (total, _txt(piece),
                                    _txt(_rnd(_D(total) / piece, 2))),
                                 "Only whole pieces count, so %d pieces." % n])
        return _nq("A rope %d metres long is cut into as many %s metre pieces "
                   "as possible. How much rope is left over, in metres?"
                   % (total, _txt(piece)), left, unit="m",
                   solution=["%d whole pieces use %s m."
                             % (n, _txt(piece * n)),
                             "%d − %s = %s m left over."
                             % (total, _txt(piece * n), _txt(left))])

    if t == 6:                       # data table, round the total
        k_items = _by_d(d, 3, 4, 5)
        items = random.sample(_FOOD, k_items)
        prices = [_by_d(d, random.randint(9, 45) * 5, random.randint(45, 225), random.randint(45, 995))
                  for _ in range(k_items)]
        rows = [[items[k].capitalize(), _lb(prices[k])] for k in range(k_items)]
        total = sum(prices)
        return _tableq("Use the table. What is the total cost, rounded to the "
                       "nearest pound?", ["Item", "Price"], rows,
                       int(_rnd(_D(total) / 100, 0)), "int",
                       ["The exact total is %s." % _lb(total),
                        "Rounded to the nearest pound that is £%s."
                        % _txt(_rnd(_D(total) / 100, 0))])

    if t == 7:                       # rate rounded to one decimal place
        who = pick(NAMES)
        km = random.randint(*_by_d(d, (45, 160), (85, 480), (300, 900)))
        litres = pick(_by_d(d, [4, 5, 8], list(range(7, 40)), list(range(23, 60))))
        while km % litres == 0:
            km += 1
        rate = _rnd(_D(km) / litres, 1)
        return _nq("A car travels %d km on %d litres of fuel. How many "
                   "kilometres does the car travel per litre, to one decimal "
                   "place?" % (km, litres), rate, unit="km",
                   solution=["%d ÷ %d = %s." % (km, litres,
                                                _txt(_rnd(_D(km) / litres, 3))),
                             "To one decimal place that is %s km per litre."
                             % format(rate, "f")])

    if t == 8:                       # estimate by rounding, then the real value
        a = _by_d(d, _mk(1, 25, 95), _mk(2, 205, 895), _mk(2, 1005, 9995))
        n = random.randint(*_by_d(d, (2, 5), (3, 9), (6, 12)))
        est = int(_rnd(a, 0)) * n
        return _iq("Estimate %s × %d by first rounding %s to the nearest whole "
                   "number. What is your estimate?" % (_txt(a), n, _txt(a)),
                   est,
                   solution=["%s rounds to %s." % (_txt(a), _txt(_rnd(a, 0))),
                             "%s × %d = %d." % (_txt(_rnd(a, 0)), n, est)])

    # journey table: total distance rounded
    k_legs = _by_d(d, 2, 3, 4)
    who = _names(k_legs)
    legs = [_by_d(d, _mk(2, 105, 495), _mk(2, 105, 895), _mk(2, 105, 1995)) for _ in range(k_legs)]
    rows = [[who[k], _txt(legs[k])] for k in range(k_legs)]
    tot = sum(legs, _D(0))
    return _tableq("The table shows how far each pupil cycled, in kilometres. "
                   "What is the total distance, rounded to one decimal place?",
                   ["Pupil", "Distance (km)"], rows,
                   _fl(_rnd(tot, 1)), "num",
                   ["The exact total is %s km." % _txt(tot),
                    "Rounded to one decimal place that is %s km."
                    % format(_rnd(tot, 1), "f")], tolerance=1e-6)


# =============================================================== 6.6 =========
# fractions whose decimal form terminates within three places
_TERM = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
         (1, 8), (3, 8), (5, 8), (7, 8), (1, 10), (3, 10), (7, 10), (9, 10),
         (1, 20), (3, 20), (7, 20), (9, 20), (11, 20), (13, 20), (17, 20),
         (1, 25), (2, 25), (3, 25), (4, 25), (6, 25), (7, 25), (9, 25),
         (11, 25), (13, 25), (1, 40), (3, 40), (7, 40), (1, 50), (3, 50),
         (7, 50), (9, 50), (11, 50), (13, 50), (17, 50), (21, 50), (23, 50),
         (1, 100), (7, 100), (9, 100), (11, 100), (13, 100), (17, 100),
         (19, 100), (23, 100), (29, 100), (31, 100), (37, 100), (41, 100),
         (43, 100), (47, 100), (53, 100), (59, 100), (61, 100), (67, 100),
         (71, 100), (73, 100), (79, 100), (83, 100), (89, 100), (97, 100),
         (1, 125), (3, 125), (7, 125), (1, 200), (3, 200), (7, 200),
         (9, 200), (1, 250), (3, 250), (7, 250), (1, 500), (3, 500),
         (7, 500), (9, 500), (11, 500)]

_EASY_TERM = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
              (1, 10), (3, 10), (7, 10), (9, 10)]
_CORE_TERM = _EASY_TERM + [(1, 8), (3, 8), (5, 8), (7, 8), (1, 20), (3, 20),
                           (7, 20), (9, 20), (1, 25), (3, 25), (7, 25),
                           (9, 25), (1, 50), (7, 50), (1, 100), (7, 100),
                           (23, 100), (37, 100), (43, 100)]


def _term_pair(d):
    return pick(_by_d(d, _EASY_TERM, _CORE_TERM, _TERM))


def _fdec(num, den):
    """Exact Decimal for a terminating fraction."""
    return (_D(num) / _D(den)).quantize(Decimal("0.000001")).normalize()


@skill("Y6.6.a", "Convert a fraction to a decimal", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 1, 1, 1])
    num, den = _term_pair(d)
    val = _fdec(num, den)

    if t == 10:                      # compare a fraction with a decimal
        other = _rnd(val + _D(pick([-15, -10, -5, 5, 10, 15])) / 100, 2)
        if other <= 0 or other >= 1:
            other = _D("0.5") if val != _D("0.5") else _D("0.45")
        return _nq("Which is greater, %d/%d or %s? Write the greater one as a decimal." % (num, den, _txt(other)),
                   max(val, other), solution=["%d/%d = %s." % (num, den, _txt(val)),
                                              "%s is greater than %s." % (_txt(max(val, other)), _txt(min(val, other)))])

    if t == 11:                      # smallest of three, mixed forms
        pairs = random.sample(_CORE_TERM, 2)
        vals = [_fdec(a, b) for a, b in pairs]
        extra = _rnd(_D(random.randint(5, 95)) / 100, 2)
        while extra in vals or vals[0] == vals[1]:
            extra = _rnd(_D(random.randint(5, 95)) / 100, 2)
            pairs = random.sample(_CORE_TERM, 2)
            vals = [_fdec(a, b) for a, b in pairs]
        shown = ["%d/%d" % pairs[0], "%d/%d" % pairs[1], _txt(extra)]
        random.shuffle(shown)
        allv = vals + [extra]
        return _nq("Which is the smallest:  %s ?  Write it as a decimal." % ",  ".join(shown), min(allv),
                   solution=["As decimals: %s." % ", ".join(_txt(v) for v in sorted(allv)),
                             "The smallest is %s." % _txt(min(allv))])

    if t == 12:                      # measures
        f_num, f_den = pick([(1, 4), (3, 4), (1, 8), (3, 8), (5, 8), (7, 8), (2, 5), (3, 20), (7, 20)])
        unit = pick(["kilometre", "kilogram", "litre"])
        return _nq("Write %d/%d of a %s as a decimal number of %ss." % (f_num, f_den, unit, unit), _fdec(f_num, f_den),
                   solution=["%d ÷ %d = %s." % (f_num, f_den, _txt(_fdec(f_num, f_den))),
                             "So it is %s %ss." % (_txt(_fdec(f_num, f_den)), unit)])

    if t == 13:                      # thousandths
        m = random.choice([x for x in range(1, 1000) if x % 10])
        return _nq("Write %d/1000 as a decimal." % m, _D(m) / 1000,
                   solution=["Thousandths have three decimal places.", "%d/1000 = %s." % (m, _txt(_D(m) / 1000))])

    if t == 0:                       # bare conversion
        return _nq("Write %d/%d as a decimal." % (num, den), val,
                   solution=["%d/%d means %d ÷ %d." % (num, den, num, den),
                             "%d ÷ %d = %s." % (num, den, _txt(val))])

    if t == 1:                       # by division, explicitly
        return _nq("Convert %d/%d to a decimal by dividing %d by %d."
                   % (num, den, num, den), val,
                   solution=["Set out %d ÷ %d as a short division." % (num, den),
                             "The answer is %s." % _txt(val)])

    if t == 2:                       # equivalent fraction route
        k = 100 // den if 100 % den == 0 else 1000 // den if 1000 % den == 0 else None
        if k:
            base = 100 if 100 % den == 0 else 1000
            return _nq("Change %d/%d into an equivalent fraction with a "
                       "denominator of %d, then write it as a decimal."
                       % (num, den, base), val,
                       solution=["%d/%d = %d/%d." % (num, den, num * k, base),
                                 "%d/%d = %s." % (num * k, base, _txt(val))])
        return _nq("Write %d/%d as a decimal." % (num, den), val,
                   solution=["%d/%d means %d ÷ %d." % (num, den, num, den),
                             "%d ÷ %d = %s." % (num, den, _txt(val))])

    if t == 3:                       # place on a number line
        f_num, f_den = pick([(1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
                             (1, 8), (3, 8), (5, 8), (7, 8), (1, 10), (3, 10),
                             (7, 10), (9, 10), (1, 20), (7, 20), (9, 20)])
        v = _fdec(f_num, f_den)
        step = _D(1) / _D(f_den)
        return _lineq("Place %d/%d on the number line." % (f_num, f_den), v,
                      0, 1, step, _D("0.5") if f_den % 2 == 0 else step,
                      ["%d/%d = %s as a decimal."
                       % (f_num, f_den, _txt(v)),
                       "Count %s along from 0." % _pl(f_num, "step")])

    if t == 4:                       # hundredths square
        f_num, f_den = pick([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5),
                             (4, 5), (1, 20), (3, 20), (7, 20), (9, 20),
                             (1, 25), (3, 25), (7, 25), (1, 50), (7, 50)])
        c = int(_fdec(f_num, f_den) * 100)
        return _gridshade("The square is one whole split into 100 equal parts. "
                          "Shade it to show %d/%d." % (f_num, f_den), c,
                          ["%d/%d = %d/100." % (f_num, f_den, c),
                           "Shade %d of the 100 small squares." % c])

    if t == 5:                       # mixed number
        w = random.randint(1, 9)
        return _nq("Write %d and %d/%d as a decimal." % (w, num, den),
                   _D(w) + val,
                   solution=["%d/%d = %s." % (num, den, _txt(val)),
                             "%d + %s = %s." % (w, _txt(val), _txt(_D(w) + val))])

    if t == 6:                       # word problem
        who = pick(NAMES)
        return _nq("%s finished %d/%d of a jigsaw. Write the amount %s finished "
                   "as a decimal." % (who, num, den, who), val,
                   solution=["%d/%d means %d ÷ %d." % (num, den, num, den),
                             "That is %s." % _txt(val)])

    if t == 7:                       # conversion table with a missing cell
        pairs = random.sample(_by_d(d, _EASY_TERM, _CORE_TERM, _CORE_TERM), 4)
        rows = [["%d/%d" % (a, b), _txt(_fdec(a, b))] for a, b in pairs]
        i = random.randrange(4)
        rows[i][1] = "?"
        a, b = pairs[i]
        return _tableq("The table matches fractions to decimals. What decimal "
                       "belongs in the empty cell?", ["Fraction", "Decimal"],
                       rows, _fl(_fdec(a, b)), "num",
                       ["%d/%d means %d ÷ %d." % (a, b, a, b),
                        "%d/%d = %s." % (a, b, _txt(_fdec(a, b)))],
                       missing=(i, 1), tolerance=1e-6)

    if t == 8:                       # fraction bar
        f_den = pick([4, 5, 8, 10])
        f_num = random.randint(1, f_den - 1)
        v = _fdec(f_num, f_den)
        return _barshade("The bar has %d equal parts. Shade it to show %s."
                         % (f_den, _txt(v)), f_den,
                         f_num, ["%s = %d/%d." % (_txt(v), f_num, f_den),
                                 "Shade %s." % _pl(f_num, "part")])

    if d == 0:                       # keep the easy tier on terminating ones
        return _nq("Write %d/%d as a decimal." % (num, den), val,
                   solution=["%d/%d means %d ÷ %d." % (num, den, num, den),
                             "%d ÷ %d = %s." % (num, den, _txt(val))])

    # a fraction that does not terminate: give the answer to 2 dp
    n2, d2 = pick([(1, 3), (2, 3), (1, 6), (5, 6), (1, 9),
                   (2, 9), (4, 9), (5, 12), (7, 12)])
    v = _rnd(_D(n2) / _D(d2), 2)
    return _nq("Write %d/%d as a decimal, giving your answer to two decimal "
               "places." % (n2, d2), v,
               solution=["%d ÷ %d = %s..." % (n2, d2, _txt(_rnd(_D(n2) / _D(d2), 4))),
                         "To two decimal places that is %s." % _txt(v)])


@skill("Y6.6.b", "Convert a decimal to a fraction in lowest terms", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 3, 1, 1, 3, 1, 3, 2, 1, 1])

    def _dv():
        if d == 0:
            c = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
            return _D(c) / 100, Fraction(c, 100)
        if d == 1:
            c = random.randint(1, 99)
            return _D(c) / 100, Fraction(c, 100)
        m = random.choice([random.randint(1, 99) * 10, random.randint(1, 999)])
        return _D(m) / 1000, Fraction(m, 1000)

    if t == 0:                       # numerator in lowest terms
        v, fr = _dv()
        return _iq("Write %s as a fraction in its lowest terms. "
                   "What is the numerator of that fraction?" % _txt(v),
                   fr.numerator,
                   solution=["%s = %d/%d." % (_txt(v), int(v * (10 ** _dp(v))),
                                              10 ** _dp(v)),
                             "In its lowest terms that is %d/%d, so the "
                             "numerator is %d."
                             % (fr.numerator, fr.denominator, fr.numerator)])

    if t == 1:                       # denominator in lowest terms
        v, fr = _dv()
        return _iq("Write %s as a fraction in its lowest terms. "
                   "What is the denominator of that fraction?" % _txt(v),
                   fr.denominator,
                   solution=["%s = %d/%d." % (_txt(v), int(v * (10 ** _dp(v))),
                                              10 ** _dp(v)),
                             "In its lowest terms that is %d/%d, so the "
                             "denominator is %d."
                             % (fr.numerator, fr.denominator, fr.denominator)])

    if t == 2:                       # fraction with a stated denominator
        v, fr = _dv()
        base = 10 ** _dp(v)
        return _fq("Write %s as a fraction with a denominator of %d."
                   % (_txt(v), base), int(v * base), base,
                   placeholder="e.g. 37/100",
                   solution=["%s has %s." % (_txt(v), _pl(_dp(v), "decimal place")),
                             "So %s = %d/%d."
                             % (_txt(v), int(v * base), base)])

    if t == 3:                       # word problem
        who = pick(NAMES)
        v, fr = _dv()
        return _iq("%s scored %s of the marks in a test. Written as a fraction "
                   "in its lowest terms, what is the denominator of that "
                   "fraction?" % (who, _txt(v)), fr.denominator,
                   solution=["%s = %d/%d." % (_txt(v), int(v * (10 ** _dp(v))),
                                              10 ** _dp(v)),
                             "Cancelled down that is %d/%d."
                             % (fr.numerator, fr.denominator)])

    if t == 4:                       # hundredths square -> lowest terms
        c = random.choice([4, 5, 8, 10, 12, 15, 16, 20, 24, 25, 30, 35, 36, 40,
                           45, 48, 50, 55, 60, 64, 65, 70, 75, 80, 85, 90, 95])
        fr = Fraction(c, 100)
        ask_num = random.random() < 0.5
        return _gridread("The hundredths square has %d of its 100 small squares "
                         "shaded. Write the shaded amount as a fraction in its "
                         "lowest terms. What is the %s of that fraction?"
                         % (c, "numerator" if ask_num else "denominator"), c,
                         fr.numerator if ask_num else fr.denominator, "int",
                         ["%d/100 cancels down to %d/%d."
                          % (c, fr.numerator, fr.denominator),
                          "The %s is %d."
                          % ("numerator" if ask_num else "denominator",
                             fr.numerator if ask_num else fr.denominator)])

    if t == 5:                       # decimal greater than 1 -> mixed number
        w = random.randint(1, 9)
        v, fr = _dv()
        while fr == 0:
            v, fr = _dv()
        return _iq("Write %s as a mixed number with the fraction part in its "
                   "lowest terms. What is the denominator of the fraction part?"
                   % _txt(_D(w) + v), fr.denominator,
                   solution=["The whole-number part is %d and the decimal part "
                             "is %s." % (w, _txt(v)),
                             "%s = %d/%d, so the denominator is %d."
                             % (_txt(v), fr.numerator, fr.denominator,
                                fr.denominator)])

    if t == 6:                       # sum of numerator and denominator
        v, fr = _dv()
        return _iq("Write %s as a fraction in its lowest terms. What is the "
                   "sum of the numerator and the denominator?" % _txt(v),
                   fr.numerator + fr.denominator,
                   solution=["%s in its lowest terms is %d/%d."
                             % (_txt(v), fr.numerator, fr.denominator),
                             "%d + %d = %d." % (fr.numerator, fr.denominator,
                                                fr.numerator + fr.denominator)])

    if t == 7:                       # table with a missing cell
        cs = random.sample([5, 15, 20, 25, 35, 40, 45, 55, 60, 65, 75, 80, 85,
                            90, 95, 12, 24, 36, 44, 48, 52, 64, 72, 88], 4)
        rows = [[_txt(_D(c) / 100),
                 "%d/%d" % (Fraction(c, 100).numerator,
                            Fraction(c, 100).denominator)] for c in cs]
        i = random.randrange(4)
        rows[i][1] = "?"
        fr = Fraction(cs[i], 100)
        return _tableq("The table matches decimals to fractions in their lowest "
                       "terms. What is the denominator of the fraction that "
                       "belongs in the empty cell?",
                       ["Decimal", "Fraction"], rows, fr.denominator, "int",
                       ["%s = %d/100." % (_txt(_D(cs[i]) / 100), cs[i]),
                        "That cancels down to %d/%d."
                        % (fr.numerator, fr.denominator)],
                       missing=(i, 1))

    if t == 8:                       # three-place decimal
        m = random.choice([125, 375, 625, 875, 250, 750, 200, 400, 600, 800,
                           25, 75, 150, 350, 450, 550, 650, 850, 950])
        fr = Fraction(m, 1000)
        v = _D(m) / 1000
        ask_num = random.random() < 0.5
        return _iq("Write %s as a fraction in its lowest terms. What is the %s "
                   "of that fraction?"
                   % (_txt(v), "numerator" if ask_num else "denominator"),
                   fr.numerator if ask_num else fr.denominator,
                   solution=["%s = %d/1000." % (_txt(v), m),
                             "%d/1000 cancels down to %d/%d."
                             % (m, fr.numerator, fr.denominator)])

    if t == 10:                      # the whole fraction, in lowest terms
        v, fr = _dv()
        while fr.denominator == 1 or fr == 0:
            v, fr = _dv()
        return _sq("Write %s as a fraction in its lowest terms." % _txt(v), "%d/%d" % (fr.numerator, fr.denominator),
                   placeholder="e.g. 3/20",
                   solution=["%s = %d/%d." % (_txt(v), int(v * 10 ** _dp(v)), 10 ** _dp(v)),
                             "Divide top and bottom by %d: %d/%d."
                             % (int(v * 10 ** _dp(v)) // fr.numerator, fr.numerator, fr.denominator)])

    if t == 11:                      # context, lowest terms
        c = random.choice([5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 20, 40, 60, 80, 12, 24, 36, 48, 64, 72, 88])
        fr = Fraction(c, 100)
        what = pick(["A water tank is %s full.", "A phone battery is %s charged.", "%s of a field is planted with wheat."])
        return _sq((what % _txt(_D(c) / 100)) + " Write that amount as a fraction in its lowest terms.",
                   "%d/%d" % (fr.numerator, fr.denominator), placeholder="e.g. 3/4",
                   solution=["%s = %d/100." % (_txt(_D(c) / 100), c), "%d/100 = %d/%d." % (c, fr.numerator, fr.denominator)])

    if t == 12:                      # thousandths to eighths
        m = random.choice([125, 375, 625, 875])
        fr = Fraction(m, 1000)
        return _sq("Write %s as a fraction in its lowest terms." % _txt(_D(m) / 1000), "%d/%d" % (fr.numerator, fr.denominator),
                   placeholder="e.g. 1/8",
                   solution=["%s = %d/1000." % (_txt(_D(m) / 1000), m),
                             "Divide top and bottom by 125: %d/%d." % (fr.numerator, fr.denominator)])

    # fraction bar: shade a decimal, then the lowest-terms denominator
    parts = pick([4, 5, 8, 10])
    n = random.randint(1, parts - 1)
    v = _fdec(n, parts)
    return _barshade("The bar has %d equal parts. Shade it to show %s."
                     % (parts, _txt(v)), parts, n,
                     ["%s = %d/%d." % (_txt(v), n, parts),
                      "Shade %s of the bar." % _pl(n, "part")])


_COMMON = [(1, 2, "0.5", 50), (1, 4, "0.25", 25), (3, 4, "0.75", 75),
           (1, 5, "0.2", 20), (2, 5, "0.4", 40), (3, 5, "0.6", 60),
           (4, 5, "0.8", 80), (1, 10, "0.1", 10), (3, 10, "0.3", 30),
           (7, 10, "0.7", 70), (9, 10, "0.9", 90), (1, 20, "0.05", 5),
           (3, 20, "0.15", 15), (7, 20, "0.35", 35), (9, 20, "0.45", 45),
           (1, 25, "0.04", 4), (1, 50, "0.02", 2), (1, 100, "0.01", 1),
           (3, 25, "0.12", 12), (7, 50, "0.14", 14)]

_COMMON_EASY = [(1, 2, "0.5", 50), (1, 4, "0.25", 25), (3, 4, "0.75", 75),
                (1, 5, "0.2", 20), (1, 10, "0.1", 10), (3, 10, "0.3", 30),
                (7, 10, "0.7", 70)]


@skill("Y6.6.c", "Common fraction, decimal and percentage equivalences", S6)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, _COMMON_EASY, _COMMON[:16], _COMMON)
    num, den, dec, pct = pick(pool)
    val = _D(dec)
    t = _pick_t([1, 1, 1, 1, 3, 3, 3, 1, 3, 1])

    if t == 0:                       # fraction -> percentage
        return _iq("Write %d/%d as a percentage." % (num, den), pct, unit="%",
                   solution=["%d/%d = %s." % (num, den, dec),
                             "%s × 100 = %d, so %d/%d = %d%%."
                             % (dec, pct, num, den, pct)])

    if t == 1:                       # percentage -> decimal
        return _nq("Write %d%% as a decimal." % pct, val,
                   solution=["Per cent means out of 100, so %d%% = %d/100."
                             % (pct, pct),
                             "%d/100 = %s." % (pct, dec)])

    if t == 2:                       # decimal -> percentage
        return _iq("Write %s as a percentage." % dec, pct, unit="%",
                   solution=["Multiply by 100 to change a decimal into a "
                             "percentage.", "%s × 100 = %d%%." % (dec, pct)])

    if t == 3:                       # percentage -> fraction (lowest terms)
        fr = Fraction(pct, 100)
        return _iq("Write %d%% as a fraction in its lowest terms. What is the "
                   "denominator of that fraction?" % pct, fr.denominator,
                   solution=["%d%% = %d/100." % (pct, pct),
                             "That cancels down to %d/%d."
                             % (fr.numerator, fr.denominator)])

    if t == 4:                       # shade the percentage square
        p = pick([5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        return _gridshade("The square is one whole split into 100 equal parts. "
                          "Shade it to show %d%%." % p, p,
                          ["Per cent means out of 100.",
                           "Shade %d of the 100 small squares." % p])

    if t == 5:                       # read the percentage square
        c = random.randint(1, 99)
        if random.random() < 0.5:
            return _gridread("The square is one whole split into 100 equal "
                             "parts, with %d shaded. What percentage is "
                             "shaded?" % c, c, c, "int",
                             ["%d out of 100 is %d/100." % (c, c),
                              "That is %d%%." % c], unit="%")
        return _gridread("The square is one whole split into 100 equal parts, "
                         "with %d shaded. Write the shaded amount as a decimal."
                         % c, c, _fl(_D(c) / 100), "num",
                         ["%d/100 is %s." % (c, _pl(c, "hundredth")),
                          "As a decimal that is %s." % _txt(_D(c) / 100)],
                         tolerance=1e-6)

    if t == 6:                       # triple table with a missing cell
        rows_src = random.sample(pool, min(4, len(pool)))
        rows = [["%d/%d" % (a, b), c, "%d%%" % p] for a, b, c, p in rows_src]
        i = random.randrange(len(rows))
        col = random.choice([1, 2])
        rows[i][col] = "?"
        a, b, c, p = rows_src[i]
        if col == 1:
            return _tableq("The table matches fractions, decimals and "
                           "percentages. What decimal belongs in the empty "
                           "cell?", ["Fraction", "Decimal", "Percentage"],
                           rows, _fl(_D(c)), "num",
                           ["%d/%d = %d%%." % (a, b, p),
                            "%d%% as a decimal is %s." % (p, c)],
                           missing=(i, col), tolerance=1e-6)
        return _tableq("The table matches fractions, decimals and percentages. "
                       "What percentage belongs in the empty cell? Give the "
                       "number only.", ["Fraction", "Decimal", "Percentage"],
                       rows, p, "int",
                       ["%s × 100 = %d." % (c, p),
                        "So %d/%d = %s = %d%%." % (a, b, c, p)],
                       missing=(i, col))

    if t == 7:                       # word problem
        who = pick(NAMES)
        return _iq("%s got %d/%d of the questions right in a quiz. What "
                   "percentage did %s get right?" % (who, num, den, who), pct,
                   unit="%",
                   solution=["%d/%d = %s." % (num, den, dec),
                             "%s = %d%%." % (dec, pct)])

    if t == 8:                       # pie chart
        p = pick([10, 20, 25, 40, 50, 60, 75, 80])
        a, b = random.sample(["Football", "Netball", "Cricket", "Hockey"], 2)
        return _pieq("The pie chart shows how a class voted for a sport. What "
                     "percentage of the class voted for %s? Give the number "
                     "only." % a,
                     [[a, p], [b, 100 - p]], p, "int",
                     ["The %s sector is %d out of every 100." % (a, p),
                      "That is %d%%." % p], highlight=0)

    # true or false equivalence
    other = pick([x for x in pool if x[3] != pct])
    same = random.random() < 0.5
    shown_pct = pct if same else other[3]
    return _sq("Is this statement true or false? %d/%d is the same as %d%%. "
               "Type true or false." % (num, den, shown_pct),
               "true" if same else "false", placeholder="true / false",
               solution=["%d/%d = %s = %d%%." % (num, den, dec, pct),
                         "The statement is %s." % ("true" if same else "false")])


@skill("Y6.6.d", "Convert between percentages, fractions and decimals", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 3, 1, 1, 1])

    def _pct():
        if d == 0:
            return random.randrange(5, 100, 5)
        if d == 1:
            return random.randint(1, 99)
        return random.choice([random.randint(1, 99), random.randrange(105, 300, 5),
                              random.randrange(5, 100, 5)])

    if t == 0:                       # percentage -> decimal
        p = _pct()
        return _nq("Write %d%% as a decimal." % p, _D(p) / 100,
                   solution=["%d%% means %d out of 100." % (p, p),
                             "%d ÷ 100 = %s." % (p, _txt(_D(p) / 100))])

    if t == 1:                       # decimal -> percentage
        p = _pct()
        v = _D(p) / 100
        return _iq("Write %s as a percentage. Give the number only." % _txt(v),
                   p, unit="%",
                   solution=["Multiply by 100: %s × 100 = %d." % (_txt(v), p),
                             "So %s = %d%%." % (_txt(v), p)])

    if t == 2:                       # percentage -> fraction over 100
        p = _pct()
        return _fq("Write %d%% as a fraction with a denominator of 100." % p,
                   p, 100, placeholder="e.g. 43/100",
                   solution=["Per cent means 'out of 100'.",
                             "%d%% = %d/100." % (p, p)])

    if t == 3:                       # fraction -> percentage
        num, den = pick(_by_d(d, _EASY_TERM, _CORE_TERM, _CORE_TERM))
        v = _fdec(num, den)
        p = v * 100
        if _dp(p) == 0:
            return _iq("Write %d/%d as a percentage. Give the number only."
                       % (num, den), int(p), unit="%",
                       solution=["%d/%d = %s." % (num, den, _txt(v)),
                                 "%s × 100 = %d%%." % (_txt(v), int(p))])
        return _nq("Write %d/%d as a percentage. Give the number only."
                   % (num, den), p, unit="%",
                   solution=["%d/%d = %s." % (num, den, _txt(v)),
                             "%s × 100 = %s%%." % (_txt(v), _txt(p))])

    if t == 4:                       # scale up to a denominator of 100
        den = pick([2, 4, 5, 10, 20, 25, 50])
        num = random.randint(1, den - 1)
        k = 100 // den
        p = num * k
        return _iq("Change %d/%d into an equivalent fraction with a "
                   "denominator of 100, then write it as a percentage. "
                   "Give the number only." % (num, den), p, unit="%",
                   solution=["Multiply top and bottom by %d: %d/%d = %d/100."
                             % (k, num, den, p),
                             "%d/100 = %d%%." % (p, p)])

    if t == 5:                       # decimal with three places -> percentage
        m = random.randint(5, 995)
        v = _D(m) / 1000
        p = v * 100
        return _nq("Write %s as a percentage. Give the number only." % _txt(v),
                   p, unit="%",
                   solution=["Multiply by 100 to change a decimal into a "
                             "percentage.",
                             "%s × 100 = %s." % (_txt(v), _txt(p))])

    if t == 6:                       # conversion table
        picks = random.sample(_by_d(d, _EASY_TERM, _CORE_TERM, _CORE_TERM), 4)
        rows = []
        for a, b in picks:
            v = _fdec(a, b)
            rows.append(["%d/%d" % (a, b), _txt(v), "%s%%" % _txt(v * 100)])
        i = random.randrange(4)
        col = random.choice([1, 2])
        rows[i][col] = "?"
        a, b = picks[i]
        v = _fdec(a, b)
        if col == 1:
            return _tableq("The table matches fractions, decimals and "
                           "percentages. What decimal belongs in the empty "
                           "cell?", ["Fraction", "Decimal", "Percentage"],
                           rows, _fl(v), "num",
                           ["%d/%d means %d ÷ %d." % (a, b, a, b),
                            "%d/%d = %s." % (a, b, _txt(v))],
                           missing=(i, col), tolerance=1e-6)
        return _tableq("The table matches fractions, decimals and percentages. "
                       "What percentage belongs in the empty cell? Give the "
                       "number only.", ["Fraction", "Decimal", "Percentage"],
                       rows, _fl(v * 100), "num",
                       ["%d/%d = %s." % (a, b, _txt(v)),
                        "%s × 100 = %s%%." % (_txt(v), _txt(v * 100))],
                       missing=(i, col), tolerance=1e-6)

    if t == 7:                       # shade the percentage square
        p = random.randint(1, 99)
        return _gridshade("The square is one whole split into 100 equal parts. "
                          "Shade it to show %d%%." % p, p,
                          ["%d%% means %d out of 100." % (p, p),
                           "Shade %d of the 100 small squares." % p])

    if t == 8:                       # word problem across the forms
        who = pick(NAMES)
        p = random.randrange(5, 100, 5)
        return _nq("In a survey, %d%% of the pupils in a school walk to school. "
                   "Write %d%% as a decimal." % (p, p), _D(p) / 100,
                   solution=["%d%% = %d/100." % (p, p),
                             "%d/100 = %s." % (p, _txt(_D(p) / 100))])

    if t == 10:                      # convert a fraction to a percent using a
        #                              grid model
        den = pick(_by_d(d, [2, 4, 5, 10], [2, 4, 5, 10, 20, 25],
                         [4, 5, 10, 20, 25, 50, 100]))
        num = random.randint(1, den - 1)
        p = num * (100 // den)
        return _gridread("This grid model is one whole split into 100 equal "
                         "squares, and %d/%d of it is shaded. Convert %d/%d to "
                         "a percent. Give the number only."
                         % (num, den, num, den), p, p, "int",
                         ["%d/%d of the grid model is %d of the 100 squares."
                          % (num, den, p),
                          "%d out of 100 is %d%%." % (p, p)], unit="%")

    if t == 11:                      # largest of three forms, as a percentage
        while True:
            p1 = random.randrange(10, 95, 5)
            num, den = pick([(1, 4), (3, 4), (2, 5), (3, 5), (1, 8), (3, 8), (7, 20), (9, 20), (1, 2)])
            dv = _D(random.randint(5, 95)) / 100
            vals = {"%d%%" % p1: _D(p1) / 100, "%d/%d" % (num, den): _D(num) / _D(den), _txt(dv): dv}
            if len(set(vals.values())) == 3:
                break
        keys = list(vals)
        random.shuffle(keys)
        big = max(vals.values())
        ask = _iq if big * 100 == (big * 100).to_integral_value() else _nq
        return ask("Which is the largest:  %s ?  Write it as a percentage. Give the number only." % ",  ".join(keys),
                   big * 100, unit="%",
                   solution=["As percentages: %s." % ", ".join("%s = %s%%" % (k, _txt(vals[k] * 100)) for k in keys),
                             "The largest is %s%%." % _txt(big * 100)])

    if t == 12:                      # percentage -> fraction in lowest terms
        p = random.choice([x for x in range(2, 100) if Fraction(x, 100).denominator != 100])
        fr = Fraction(p, 100)
        return _sq("Write %d%% as a fraction in its lowest terms." % p, "%d/%d" % (fr.numerator, fr.denominator),
                   placeholder="e.g. 3/20",
                   solution=["%d%% = %d/100." % (p, p), "That cancels down to %d/%d." % (fr.numerator, fr.denominator)])

    if t == 13:                      # the rest, as a percentage
        num, den = pick([(1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (3, 10), (7, 10), (7, 20), (11, 25), (1, 2)])
        p = num * 100 // den
        what = pick(["have a pet", "walk to school", "play an instrument"])
        return _iq("%d/%d of the children in a school %s. What percentage of the children do not? Give the number only."
                   % (num, den, what), 100 - p, unit="%",
                   solution=["%d/%d = %d%%." % (num, den, p), "100%% − %d%% = %d%%." % (p, 100 - p)])

    # place a percentage on a 0-1 number line
    p = random.randrange(1, 100)
    return _lineq("Place %d%% on this number line, which runs from 0 to 1."
                  % p, _D(p) / 100, 0, 1, _D("0.01"), _D("0.1"),
                  ["%d%% = %s as a decimal." % (p, _txt(_D(p) / 100)),
                   "Count %d small steps on from 0." % p])


@skill("Y6.6.e", "Compare and order fractions, decimals and percentages", S6)
def _(d=1):
    d = _tier(d)

    def _items(k, hundredths=False):
        """k items in mixed forms, all with different values."""
        out = []
        used = set()
        tries = 0
        while len(out) < k and tries < 400:
            tries += 1
            if hundredths:
                m = random.randrange(10, 1000, 10)
            elif d == 2:
                m = random.choice([random.randrange(50, 1000, 25),
                                   random.randrange(50, 1000, 10)])
            else:
                m = random.randrange(50, 1000, 50) if d == 0 else \
                    random.randrange(10, 1000, 10)
            if m in used:
                continue
            used.add(m)
            v = _D(m) / 1000
            kind = pick(["frac", "dec", "pct"])
            if kind == "frac":
                fr = Fraction(m, 1000)
                text = "%d/%d" % (fr.numerator, fr.denominator)
            elif kind == "dec":
                text = _txt(v)
            else:
                text = "%s%%" % _txt(v * 100)
            out.append((text, v))
        while len(out) < k:
            m = max(used) + 1
            used.add(m)
            out.append((_txt(_D(m) / 1000), _D(m) / 1000))
        return out

    t = _pick_t([1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3])

    if t == 0:                       # which is greater, two forms
        items = _items(2)
        (ta, va), (tb, vb) = items
        big = max(va, vb)
        return _nq("Which is greater, %s or %s? Write the greater amount as a "
                   "decimal." % (ta, tb), big,
                   solution=["%s = %s and %s = %s."
                             % (ta, _txt(va), tb, _txt(vb)),
                             "The greater amount is %s." % _txt(big)])

    if t == 1:                       # largest of three
        items = _items(3)
        big = max(v for _t, v in items)
        return _nq("Write the largest of these amounts as a decimal: %s"
                   % ", ".join(t_ for t_, _v in items), big,
                   solution=["As decimals: %s."
                             % ", ".join("%s = %s" % (t_, _txt(v))
                                         for t_, v in items),
                             "The largest is %s." % _txt(big)])

    if t == 2:                       # smallest of three
        items = _items(3)
        small = min(v for _t, v in items)
        return _nq("Write the smallest of these amounts as a decimal: %s"
                   % ", ".join(t_ for t_, _v in items), small,
                   solution=["Change them all into decimals first: %s."
                             % ", ".join("%s = %s" % (t_, _txt(v))
                                         for t_, v in items),
                             "The smallest is %s." % _txt(small)])

    if t == 3:                       # second largest of four
        items = _items(4)
        vals = sorted((v for _t, v in items), reverse=True)
        return _nq("Write the second largest of these amounts as a decimal: %s"
                   % ", ".join(t_ for t_, _v in items), vals[1],
                   solution=["In order, largest first: %s."
                             % ", ".join(_txt(v) for v in vals),
                             "The second largest is %s." % _txt(vals[1])])

    if t == 4:                       # true or false
        items = _items(2)
        (ta, va), (tb, vb) = items
        sign = pick([">", "<"])
        truth = (va > vb) if sign == ">" else (va < vb)
        return _sq("Is this statement true or false? %s %s %s. "
                   "Type true or false." % (ta, sign, tb),
                   "true" if truth else "false", placeholder="true / false",
                   solution=["%s = %s and %s = %s."
                             % (ta, _txt(va), tb, _txt(vb)),
                             "So the statement is %s."
                             % ("true" if truth else "false")])

    if t == 5:                       # who did best
        items = _items(3)
        who = _names(3)
        best = max(range(3), key=lambda i: items[i][1])
        return _sq("In a test %s scored %s of the marks, %s scored %s and %s "
                   "scored %s. Who scored the most? Type the name."
                   % (who[0], items[0][0], who[1], items[1][0], who[2],
                      items[2][0]), who[best], placeholder="a name",
                   solution=["As decimals: %s."
                             % ", ".join("%s = %s" % (who[i], _txt(items[i][1]))
                                         for i in range(3)),
                             "%s scored the most." % who[best]])

    if t == 6:                       # table of mixed forms
        items = _items(4)
        who = _names(4)
        rows = [[who[i], items[i][0]] for i in range(4)]
        want_max = random.random() < 0.5
        idx = (max if want_max else min)(range(4), key=lambda i: items[i][1])
        return _tableq("The table shows the share of a pizza each pupil ate. "
                       "Who ate the %s share? Type the name."
                       % ("largest" if want_max else "smallest"),
                       ["Pupil", "Share"], rows, who[idx], "str",
                       ["Change every share into a decimal: %s."
                        % ", ".join("%s = %s" % (items[i][0], _txt(items[i][1]))
                                    for i in range(4)),
                        "%s ate the %s share."
                        % (who[idx], "largest" if want_max else "smallest")])

    if t == 7:                       # place the greater on a number line
        items = _items(2, hundredths=True)
        (ta, va), (tb, vb) = items
        big = max(va, vb)
        return _lineq("Which is greater, %s or %s? Place the greater amount on "
                      "this number line, which runs from 0 to 1."
                      % (ta, tb), big, 0, 1, _D("0.01"), _D("0.1"),
                      ["%s = %s and %s = %s."
                       % (ta, _txt(va), tb, _txt(vb)),
                       "The greater amount is %s." % _txt(max(va, vb))])

    if t == 8:                       # how many are greater than a half
        items = _items(5)
        cut = _D("0.5")
        n_more = len([v for _t, v in items if v > cut])
        return _iq("How many of these amounts are greater than 0.5? %s"
                   % ", ".join(t_ for t_, _v in items), n_more,
                   solution=["Change each amount into a decimal and compare "
                             "with 0.5.",
                             "%d of them are greater than 0.5." % n_more])

    if t == 9:                       # equal or not
        m = random.randrange(50, 1000, 50)
        v = _D(m) / 1000
        fr = Fraction(m, 1000)
        same = random.random() < 0.5
        shown = _txt(v) if same else _txt(v + _D("0.05"))
        return _sq("Are %d/%d and %s equal? Type yes or no."
                   % (fr.numerator, fr.denominator, shown),
                   "yes" if same else "no", placeholder="yes / no",
                   solution=["%d/%d = %s as a decimal."
                             % (fr.numerator, fr.denominator, _txt(v)),
                             "So the answer is %s." % ("yes" if same else "no")])

    # bar chart of percentages (the four percentages make a whole survey)
    cats = random.sample(["Football", "Netball", "Cricket", "Hockey", "Tennis"], 4)
    while True:
        cuts = sorted(random.sample(range(1, 20), 3))
        parts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 20 - cuts[2]]
        if min(parts) >= 1:
            break
    pcts = [x * 5 for x in parts]
    i = random.randrange(4)
    frac_form = Fraction(pcts[i], 100)
    return _barq("The bar chart shows the percentage of pupils choosing each "
                 "sport. What fraction of the pupils chose %s? Write the "
                 "denominator of that fraction in its lowest terms."
                 % cats[i].lower(), cats, pcts, frac_form.denominator, "int",
                 ["%s was chosen by %d%% of pupils." % (cats[i], pcts[i]),
                  "%d%% = %d/100 = %d/%d." % (pcts[i], pcts[i],
                                              frac_form.numerator,
                                              frac_form.denominator)])


def _pct_amount(d):
    """A percentage and an amount whose percentage is a whole number."""
    p = pick(_by_d(d, [10, 20, 25, 50, 75],
                   [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90],
                   [4, 5, 8, 12, 15, 18, 22, 24, 25, 35, 45, 55, 65, 85, 95]))
    step = 100 // _gcd(p, 100)
    base = random.randint(*_by_d(d, (2, 12), (2, 30), (3, 60)))
    amount = base * step
    return p, amount, amount * p // 100


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


@skill("Y6.6.f", "Find a percentage of an amount", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 3, 3, 3, 1, 1, 3, 2, 2])

    if t == 0:                       # bare percentage of a number
        p, amount, ans = _pct_amount(d)
        return _iq("What is %d%% of %s?" % (p, "{:,}".format(amount)), ans,
                   solution=["1%% of %s is %s."
                             % ("{:,}".format(amount), _txt(_D(amount) / 100)),
                             "%d × %s = %s."
                             % (p, _txt(_D(amount) / 100), "{:,}".format(ans))])

    if t == 1:                       # percentage of money
        p = pick([5, 10, 15, 20, 25, 40, 50, 60, 75])
        pounds = random.randint(2, 90) * (100 // _gcd(p, 100)) // 5 * 5
        if pounds < 5:
            pounds = 20
        pence = pounds * 100
        while (pence * p) % 100:
            pence += 100
        ans = pence * p // 100
        return _nq("What is %d%% of %s? Give your answer in pounds."
                   % (p, _lb(pence)), _D(ans) / 100, unit="£",
                   solution=["1%% of %s is %s."
                             % (_lb(pence), _lb(pence // 100)),
                             "%d × %s = %s, so %d%% of %s is %s."
                             % (p, _lb(pence // 100), _lb(ans), p,
                                _lb(pence), _lb(ans))])

    if t == 2:                       # measures
        p, amount, ans = _pct_amount(d)
        return _iq("A bag of flour has a mass of %s grams. What is %d%% of "
                   "that mass, in grams?" % ("{:,}".format(amount), p), ans,
                   unit="g",
                   solution=["%d%% means %d out of every 100." % (p, p),
                             "%d%% of %s g = %s g."
                             % (p, "{:,}".format(amount), "{:,}".format(ans))])

    if t == 3:                       # discount: price after a reduction
        p = pick([10, 20, 25, 50, 15, 30, 40])
        pence = random.randint(4, 60) * 500
        while (pence * p) % 100:
            pence += 500
        cut = pence * p // 100
        return _nq("A coat costs %s. In a sale the price is reduced by %d%%. "
                   "What is the sale price, in pounds?" % (_lb(pence), p),
                   _D(pence - cut) / 100, unit="£",
                   solution=["%d%% of %s is %s." % (p, _lb(pence), _lb(cut)),
                             "%s − %s = %s."
                             % (_lb(pence), _lb(cut), _lb(pence - cut))])

    if t == 4:                       # percentage square model
        p = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75,
                           80, 90])
        return _gridshade("The whole square stands for 100%%. "
                          "Shade it to show %d%%." % p, p,
                          ["The square has 100 equal small squares.",
                           "Shade %d of them to show %d%%." % (p, p)])

    if t == 5:                       # strip model: 10% of a total
        total = random.randint(2, 60) * 10
        return _stripq("The strip model shows %s split into 10 equal parts. "
                       "What is 10%% of %s?"
                       % ("{:,}".format(total), "{:,}".format(total)),
                       10, "?", "{:,}".format(total), "part", total // 10, "int",
                       ["10%% is one tenth, so divide %s by 10."
                        % "{:,}".format(total),
                        "10%% of %s is %s."
                        % ("{:,}".format(total), "{:,}".format(total // 10))])

    if t == 6:                       # table of percentages of amounts
        p = pick([5, 10, 20, 25, 50])
        step = 100 // _gcd(p, 100)
        amounts = [random.randint(2, 40) * step for _ in range(4)]
        while len(set(amounts)) < 4:
            amounts = [random.randint(2, 40) * step for _ in range(4)]
        rows = [["{:,}".format(a), "{:,}".format(a * p // 100)] for a in amounts]
        i = random.randrange(4)
        rows[i][1] = "?"
        return _tableq("Every number in the second column is %d%% of the number "
                       "beside it. What number belongs in the empty cell?" % p,
                       ["Amount", "%d%% of it" % p], rows,
                       amounts[i] * p // 100, "int",
                       ["%d%% of %s." % (p, "{:,}".format(amounts[i])),
                        "The answer is %s."
                        % "{:,}".format(amounts[i] * p // 100)],
                       missing=(i, 1))

    if t == 7:                       # build from 10% and 5%
        p = pick([15, 35, 45, 55, 65, 85, 95])
        amount = random.randint(2, 40) * 20
        ans = amount * p // 100
        return _iq("Work out %d%% of %s by first finding 10%% and 5%%."
                   % (p, "{:,}".format(amount)), ans,
                   solution=["10%% of %s is %s and 5%% is %s."
                             % ("{:,}".format(amount),
                                _txt(_D(amount) / 10), _txt(_D(amount) / 20)),
                             "%d%% of %s = %s."
                             % (p, "{:,}".format(amount), "{:,}".format(ans))])

    if t == 8:                       # compare two percentages of amounts
        p1, a1, r1 = _pct_amount(d)
        p2, a2, r2 = _pct_amount(d)
        while r1 == r2:
            p2, a2, r2 = _pct_amount(d)
        return _iq("Which is greater, %d%% of %s or %d%% of %s? Write the "
                   "greater value." % (p1, "{:,}".format(a1), p2,
                                       "{:,}".format(a2)), max(r1, r2),
                   solution=["%d%% of %s = %s and %d%% of %s = %s."
                             % (p1, "{:,}".format(a1), "{:,}".format(r1),
                                p2, "{:,}".format(a2), "{:,}".format(r2)),
                             "The greater value is %s." % "{:,}".format(max(r1, r2))])

    if t == 10:                      # percent of a number, stated in words
        p, amount, ans = _pct_amount(d)
        return _iq("What is %d percent of the number %s?"
                   % (p, "{:,}".format(amount)), ans,
                   solution=["1 percent of %s is %s."
                             % ("{:,}".format(amount), _txt(_D(amount) / 100)),
                             "%d × %s = %s."
                             % (p, _txt(_D(amount) / 100),
                                "{:,}".format(ans))])

    if t == 11:                      # percent of a number: word problem
        p, amount, ans = _pct_amount(d)
        for _grow in range(5):       # keep the context sensible, e.g. not 4 books
            if amount >= 20:
                break
            amount *= 2
            ans *= 2
        who = pick(NAMES)
        kind = random.randrange(4)
        if kind == 0:
            prompt = ("A library has %s books. %d percent of the books are "
                      "about science. How many of the books are about science?"
                      % ("{:,}".format(amount), p))
            unit = "books"
        elif kind == 1:
            prompt = ("A school has %s pupils. %d percent of the pupils walk "
                      "to school. How many of the pupils walk to school?"
                      % ("{:,}".format(amount), p))
            unit = "pupils"
        elif kind == 2:
            prompt = ("%s has %s stickers and gives away %d percent of them. "
                      "How many stickers does %s give away?"
                      % (who, "{:,}".format(amount), p, who))
            unit = "stickers"
        else:
            prompt = ("A farm has %s trees. %d percent of the trees are apple "
                      "trees. How many of the trees are apple trees?"
                      % ("{:,}".format(amount), p))
            unit = "trees"
        return _iq(prompt, ans, unit=unit,
                   solution=["%d percent means %d out of every 100." % (p, p),
                             "%d percent of %s is %s."
                             % (p, "{:,}".format(amount), "{:,}".format(ans))])

    # pie chart: percentage of a known total
    p = pick([10, 20, 25, 40, 50, 60, 75, 80])
    total = random.randint(2, 12) * 20
    a = pick(["Walk", "Cycle", "Bus", "Car"])
    return _pieq("%d pupils were asked how they travel to school. The pie chart "
                 "shows that %d%% chose '%s'. How many pupils chose '%s'?"
                 % (total, p, a, a),
                 [[a, p], ["Other", 100 - p]], total * p // 100, "int",
                 ["%d%% of %d pupils." % (p, total),
                  "%d%% of %d = %d." % (p, total, total * p // 100)],
                 highlight=0)


@skill("Y6.6.g", "Percentage problems", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 1, 1, 1, 1])

    if t == 10:                      # percentage of an amount of money
        p = pick([5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75, 80, 90])
        amt = random.randint(2, _by_d(d, 10, 30, 80)) * 20
        return _iq("Find %d%% of £%d." % (p, amt), amt * p // 100, unit="£",
                   solution=["10%% of £%d is £%s." % (amt, _txt(_D(amt) / 10)),
                             "%d%% of £%d = £%d." % (p, amt, amt * p // 100)])

    if t == 11:                      # which percentage of an amount is larger
        p1, p2 = random.sample([10, 20, 25, 30, 40, 50, 60, 75], 2)
        a1, a2 = random.randint(2, 20) * 20, random.randint(2, 20) * 20
        v1, v2 = a1 * p1 // 100, a2 * p2 // 100
        while v1 == v2:
            a2 += 20
            v2 = a2 * p2 // 100
        return _iq("Which is larger: %d%% of %d or %d%% of %d? Write the larger value." % (p1, a1, p2, a2), max(v1, v2),
                   solution=["%d%% of %d = %d." % (p1, a1, v1), "%d%% of %d = %d." % (p2, a2, v2),
                             "The larger is %d." % max(v1, v2)])

    if t == 12:                      # compare two test scores
        who1, who2 = _two_names()
        while True:
            m1, t1 = pick([(18, 25), (17, 20), (36, 50), (7, 10), (13, 20), (21, 25), (42, 50), (9, 10), (16, 25)])
            m2, t2 = pick([(18, 25), (17, 20), (36, 50), (7, 10), (13, 20), (21, 25), (42, 50), (9, 10), (16, 25)])
            if m1 * 100 // t1 != m2 * 100 // t2:
                break
        p1, p2 = m1 * 100 // t1, m2 * 100 // t2
        return _iq("%s scored %d out of %d. %s scored %d out of %d. What is the higher percentage score? Give the number only."
                   % (who1, m1, t1, who2, m2, t2), max(p1, p2), unit="%",
                   solution=["%d/%d = %d%% and %d/%d = %d%%." % (m1, t1, p1, m2, t2, p2),
                             "The higher score is %d%%." % max(p1, p2)])

    if t == 13:                      # two steps: how many are NOT
        tot = random.randint(2, 9) * 100
        p = pick([4, 5, 6, 8, 12, 15, 20, 35])
        return _iq("A box holds %d apples and %d%% of them are bruised. How many apples are not bruised?" % (tot, p),
                   tot - tot * p // 100, unit="apples",
                   solution=["%d%% of %d = %d bruised." % (p, tot, tot * p // 100),
                             "%d − %d = %d are not bruised." % (tot, tot * p // 100, tot - tot * p // 100)])

    if t == 0:                       # what percentage is x of y
        den = pick([10, 20, 25, 40, 50, 200])
        total = den
        num = random.randint(1, den - 1)
        while (num * 100) % den:
            num = random.randint(1, den - 1)
        p = num * 100 // den
        who = pick(NAMES)
        return _iq("%s scored %s out of %d in a test. What percentage is "
                   "that? Give the number only." % (who, _pl(num, "mark"), total), p, unit="%",
                   solution=["%d out of %d = %d/%d." % (num, total, num, total),
                             "As a percentage that is %d%%." % p])

    if t == 1:                       # find the whole from a percentage
        p = pick([5, 10, 20, 25, 40, 50, 60, 75, 80])
        whole = random.randint(2, 40) * (100 // _gcd(p, 100))
        part = whole * p // 100
        return _iq("%d%% of a number is %s. What is the number?"
                   % (p, "{:,}".format(part)), whole,
                   solution=["1%% of the number is %s ÷ %d = %s."
                             % ("{:,}".format(part), p,
                                _txt(_D(part) / p)),
                             "100%% of it is %s × 100 = %s."
                             % (_txt(_D(part) / p), "{:,}".format(whole))])

    if t == 2:                       # percentage of a measure (NC: "such as 15% of 360")
        p = pick([5, 15, 35, 45, 65, 85])
        unit, word = pick([("m", "metres"), ("kg", "kilograms"), ("ml", "millilitres"), ("g", "grams")])
        amt = random.randint(1, _by_d(d, 10, 30, 90)) * 20
        return _iq("Find %d%% of %s %s." % (p, "{:,}".format(amt), word), amt * p // 100, unit=unit,
                   solution=["10%% of %s is %s and 5%% is half of that, %s."
                             % ("{:,}".format(amt), _txt(_D(amt) / 10), _txt(_D(amt) / 20)),
                             "%d%% of %s = %s %s." % (p, "{:,}".format(amt), "{:,}".format(amt * p // 100), unit)])

    if t == 3:                       # sale price after a percentage off
        p = pick([10, 20, 25, 30, 40, 50])
        a = random.randint(2, 30) * 10
        while (a * p) % 100:
            a += 10
        off = a * p // 100
        item = pick(["jacket", "bike helmet", "pair of trainers", "lamp", "board game"])
        return _iq("A %s costs £%d. In a sale it has %d%% off. What is the sale price, in pounds?" % (item, a, p),
                   a - off, unit="£",
                   solution=["%d%% of £%d = £%d." % (p, a, off), "£%d − £%d = £%d." % (a, off, a - off)])

    if t == 4:                       # difference between two percentages
        p1 = pick([10, 20, 25, 50])
        p2 = pick([x for x in [10, 20, 25, 50, 40, 75] if x != p1])
        a1 = random.randint(2, 30) * (100 // _gcd(p1, 100))
        a2 = random.randint(2, 30) * (100 // _gcd(p2, 100))
        r1, r2 = a1 * p1 // 100, a2 * p2 // 100
        while r1 == r2:
            a2 = random.randint(2, 30) * (100 // _gcd(p2, 100))
            r2 = a2 * p2 // 100
        return _iq("Work out the difference between %d%% of %s and %d%% of %s."
                   % (p1, "{:,}".format(a1), p2, "{:,}".format(a2)),
                   abs(r1 - r2),
                   solution=["%d%% of %s = %s and %d%% of %s = %s."
                             % (p1, "{:,}".format(a1), "{:,}".format(r1),
                                p2, "{:,}".format(a2), "{:,}".format(r2)),
                             "The difference is %s." % "{:,}".format(abs(r1 - r2))])

    if t == 5:                       # results table
        who = _names(4)
        totals = [pick([20, 25, 40, 50]) for _ in range(4)]
        marks = []
        pcts = []
        for tot in totals:
            m = random.randint(1, tot - 1)
            while (m * 100) % tot:
                m = random.randint(1, tot - 1)
            marks.append(m)
            pcts.append(m * 100 // tot)
        i = random.randrange(4)
        rows = [[who[k], "%d out of %d" % (marks[k], totals[k])] for k in range(4)]
        return _tableq("The table shows four test results. What percentage did "
                       "%s score? Give the number only." % who[i],
                       ["Pupil", "Score"], rows, pcts[i], "int",
                       ["%s scored %d out of %d."
                        % (who[i], marks[i], totals[i]),
                        "%d ÷ %d × 100 = %d%%."
                        % (marks[i], totals[i], pcts[i])])

    if t == 6:                       # pie chart with a total
        total = random.randint(3, 15) * 20
        p = pick([10, 15, 20, 25, 30, 40, 50, 60])
        labels = ["Red", "Blue", "Green", "Yellow"]
        a, b = random.sample(labels, 2)
        n = total * p // 100
        return _pieq("%d counters are sorted by colour. The pie chart shows "
                     "that %d%% of them are %s. How many counters are not %s?"
                     % (total, p, a.lower(), a.lower()),
                     [[a, p], [b, 100 - p]], total - n, "int",
                     ["%d%% of %d = %d counters are %s."
                      % (p, total, n, a.lower()),
                      "%d − %d = %d are not %s." % (total, n, total - n,
                                                    a.lower())],
                     highlight=0)

    if t == 7:                       # find another percentage of the same number
        p1 = pick([10, 20, 25, 30, 40])
        p2 = pick([x for x in [15, 45, 60, 75, 80, 90] if x != p1])
        whole = random.randint(2, 30) * 20
        while (whole * p1) % 100 or (whole * p2) % 100:
            whole += 20
        part = whole * p1 // 100
        return _iq("%d%% of a number is %s. What is %d%% of the same number?"
                   % (p1, "{:,}".format(part), p2),
                   whole * p2 // 100,
                   solution=["The whole number is %s ÷ %d × 100 = %s."
                             % ("{:,}".format(part), p1, "{:,}".format(whole)),
                             "%d%% of %s = %s."
                             % (p2, "{:,}".format(whole),
                                "{:,}".format(whole * p2 // 100))])

    if t == 8:                       # compare a fraction of an amount with a percentage of it
        amt = random.randint(2, 12) * 20
        while True:
            num, den = pick([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (3, 10), (7, 10)])
            p = pick([15, 30, 35, 45, 55, 65, 70, 85])
            if num * 100 != p * den:
                break
        f, q = amt * num // den, amt * p // 100
        return _iq("Which is more: %d/%d of %d or %d%% of %d? Write the larger value." % (num, den, amt, p, amt), max(f, q),
                   solution=["%d/%d = %d%%, so %d/%d of %d = %d." % (num, den, num * 100 // den, num, den, amt, f),
                             "%d%% of %d = %d." % (p, amt, q), "The larger value is %d." % max(f, q)])

    # bar chart: percentage of a whole (the four bars total 200 pupils)
    cats = random.sample(["Maths", "Science", "History", "Art", "Music"], 4)
    while True:
        cuts = sorted(random.sample(range(1, 20), 3))
        parts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 20 - cuts[2]]
        if min(parts) >= 1:
            break
    vals = [x * 10 for x in parts]
    total = sum(vals)
    i = random.randrange(4)
    return _barq("The bar chart shows how many pupils chose each club. What "
                 "percentage of the pupils chose %s? Give the number only."
                 % cats[i].lower(), cats, vals, vals[i] * 100 // total, "int",
                 ["Altogether %d pupils chose a club." % total,
                  "%d out of %d is %d%%." % (vals[i], total,
                                             vals[i] * 100 // total)])
