# dev/app/logic/y8_gen_a.py — Year 8 generators: strands 8.0 and 8.1
#
# 8.0  Number, place value & directed numbers (compare/order integers incl.
#      negatives, decimal place value, rounding to dp and significant figures,
#      number lines, rational numbers, <, > and =, BIDMAS, estimation).
# 8.1  Factors, powers, roots & standard form (divisibility, factors/multiples,
#      prime factorisation in index form, HCF, LCM, index laws, powers, roots,
#      standard form).
#
# Difficulty `d`: 0 = easy, 1 = core (year-expected), 2 = stretch.
# One generator per skill; each offers 8+ genuinely different framings and
# routes a good share through the interactive components.
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from .maths_engine import skill, ordinal, pick, NAMES

S0 = "8.0 Number, place value & directed numbers"
S1 = "8.1 Factors, powers, roots & standard form"

_TOWNS = ["Redhill", "Oakfield", "Larkmoor", "Westbury", "Fenton", "Millbrook",
          "Ashgrove", "Northolt", "Stanton", "Hartley"]
_CITIES = ["Oslo", "Moscow", "Helsinki", "Toronto", "Reykjavik", "Prague",
           "Warsaw", "Tallinn", "Vienna", "Berlin"]


# ================================================================ helpers ====
def _d(d):
    """Clamp difficulty to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _lst(xs):
    return ", ".join(str(x) for x in xs)


def _fmt(x):
    """Clean decimal string: 3.0 -> '3', 3.40 -> '3.4', 300 -> '300'."""
    d = x if isinstance(x, Decimal) else Decimal(str(x))
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s


def _dround(x, dp):
    """Round to `dp` decimal places, half up, as a Decimal."""
    d = x if isinstance(x, Decimal) else Decimal(str(x))
    q = Decimal(1).scaleb(-int(dp))
    return d.quantize(q, rounding=ROUND_HALF_UP)


def _sfround(x, sig):
    """Round to `sig` significant figures, half up, as a Decimal."""
    d = x if isinstance(x, Decimal) else Decimal(str(x))
    if d == 0:
        return Decimal(0)
    exp = d.adjusted()                       # power of ten of the leading digit
    q = Decimal(1).scaleb(exp - (int(sig) - 1))
    return d.quantize(q, rounding=ROUND_HALF_UP)


def _r1sf(n):
    """Round an integer to 1 significant figure (half up)."""
    n = int(n)
    if n == 0:
        return 0
    sign = -1 if n < 0 else 1
    n = abs(n)
    base = 10 ** (len(str(n)) - 1)
    return sign * ((n + base // 2) // base) * base


def _near_1sf(A):
    """A random integer that rounds to the 1-sf value A (A a multiple of its place)."""
    A = int(A)
    if A < 10:
        return A
    base = 10 ** (len(str(A)) - 1)
    delta = random.randint(-(base // 2 - 1), base // 2 - 1)
    n = A + delta
    return n if _r1sf(n) == A else A


_PLACE_AFTER = {0: "tenths", 1: "hundredths", 2: "thousandths", 3: "ten-thousandths", 4: "hundred-thousandths"}


def _why_dp(x, dp):
    """Why x rounds as it does to dp decimal places, from the digit that decides it."""
    frac = format(x if isinstance(x, Decimal) else Decimal(str(x)), "f").partition(".")[2]
    nxt = int((frac + "0" * (dp + 1))[dp])
    return "The %s digit is %d, %s, so %s rounds %s to %s." % (
        _PLACE_AFTER[dp], nxt, "5 or more" if nxt >= 5 else "less than 5", _fmt(x),
        "up" if nxt >= 5 else "down", format(_dround(x, dp), "f"))


def _why_sf(x, sig):
    """Why x rounds as it does to sig significant figures."""
    d = abs(x if isinstance(x, Decimal) else Decimal(str(x)))
    nxt = int(d.scaleb(sig - 1 - d.adjusted() + 1) % 10)
    return "The next digit after %d significant figure%s is %d, %s, so round %s." % (
        sig, "" if sig == 1 else "s", nxt, "5 or more" if nxt >= 5 else "less than 5", "up" if nxt >= 5 else "down")


def _why_bigger(a, b):
    """Why one decimal is bigger: the first place, from the left, where the digits differ."""
    if (a < 0) != (b < 0):
        return "A negative number is always less than a positive one."
    if a < 0:
        return "Both are negative, so the one further from zero (%s) is smaller." % _fmt(min(a, b))
    if int(a) != int(b):
        return "The whole numbers differ: %d and %d." % (int(a), int(b))
    fa, fb = (format(Decimal(str(v)), "f").partition(".")[2] for v in (a, b))
    n = max(len(fa), len(fb))
    fa, fb = fa.ljust(n, "0"), fb.ljust(n, "0")
    i = next(i for i in range(n) if fa[i] != fb[i])
    return "Line up the decimal points: the first different digit is in the %s place, %s and %s." % (
        _PLACE_AFTER[i], fa[i], fb[i])


# ---- component question builders --------------------------------------------
def _tb(prompt, ans, atype="int", spec=None, solution=None, tol=0):
    """A typed-answer question on the plain `number` component."""
    return {"prompt": prompt, "component": "number", "spec": spec or {},
            "answer": ans, "answer_type": atype, "tolerance": tol,
            "solution": solution or []}


def _wq(prompt, ans, solution, placeholder="type your answer"):
    return _tb(prompt, ans, "str", {"text": True, "placeholder": placeholder},
               solution)


def _yn(prompt, ans, solution):
    return _wq(prompt, ans, solution, "yes / no")


def _numq(prompt, ans, solution, tol=0, unit=None, placeholder=None):
    spec = {}
    if unit:
        spec["unit"] = unit
    if placeholder:
        spec["placeholder"] = placeholder
    return _tb(prompt, ans, "num", spec, solution, tol)


def _setq(prompt, values, solution, placeholder="e.g. 2, 3, 6"):
    vals = sorted(int(v) for v in values)
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in vals),
            "answer_type": "set", "tolerance": 0, "solution": solution}


def _dt(prompt, headers, rows, answer, solution, missing=None, atype="int"):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": atype, "tolerance": 0,
            "solution": solution}


def _nl(prompt, ans, lo, hi, step, major, solution):
    """Place-the-marker on a number line (supports decimal step); ans = lo + k*step."""
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": float(lo), "max": float(hi), "step": float(step),
                     "major": float(major)},
            "answer": _fmt(ans), "answer_type": "num",
            "tolerance": abs(float(step)) / 2.0, "solution": solution}


def _ineq(prompt, op, value, lo, hi, ans, solution):
    """An inequality drawn on a number line; typed yes/no or value answer."""
    return {"prompt": prompt, "component": "inequality_line",
            "spec": {"op": op, "value": value, "min": lo, "max": hi},
            "answer": ans, "answer_type": "str", "tolerance": 0,
            "solution": solution}


def _pick_t(plain, visual):
    """Choose a framing; visual framings are twice as likely as typed ones."""
    return random.choice(list(plain) + list(visual) + list(visual))()


# ---- number helpers ---------------------------------------------------------
def _pf(n):
    """Prime factorisation of n>1 as an ordered list of (prime, exponent)."""
    n = int(n)
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def _pf_str(pairs):
    """[(2,3),(3,1),(5,2)] -> '2^3x3x5^2' (exponent 1 omitted, 'x' between)."""
    bits = []
    for p, e in pairs:
        bits.append("%d^%d" % (p, e) if e > 1 else "%d" % p)
    return "x".join(bits)


def _make_composite(d):
    """A composite number with a tidy prime factorisation for this difficulty."""
    if d == 0:
        primes = [2, 3, 5]
        cap = 200
    elif d == 1:
        primes = [2, 3, 5, 7]
        cap = 1200
    else:
        primes = [2, 3, 5, 7, 11]
        cap = 6000
    for _ in range(40):
        chosen = random.sample(primes, random.randint(2, 3 if d else 2))
        n = 1
        for p in chosen:
            n *= p ** random.randint(1, 3 if p <= 3 else 2)
        if 12 <= n <= cap:
            return n
    return 360


def _lcm(a, b):
    return a * b // math.gcd(a, b)


def _terminates(fr):
    """Does the fraction (in lowest terms) give a terminating decimal?"""
    den = fr.denominator
    for p in (2, 5):
        while den % p == 0:
            den //= p
    return den == 1


# ---- standard-form helpers --------------------------------------------------
def _sf_from_digits(digits, exp):
    """digits='325', exp=6 -> ('3.25x10^6', Decimal value)."""
    mant = digits[0] + ("." + digits[1:] if len(digits) > 1 else "")
    value = Decimal(int(digits)).scaleb(exp - (len(digits) - 1))
    return "%sx10^%d" % (mant, exp), value


def _rand_digits(d):
    """A 2-3 digit significant string, no trailing zero (clean mantissa)."""
    k = 2 if d == 0 else random.choice([2, 3])
    s = str(random.randint(1, 9))
    for _ in range(k - 1):
        s += str(random.randint(0, 9))
    return s.rstrip("0") or s[0]


# ==================================================================== 8.0 ====
@skill("Y8.0.a", "Compare and order integers, including negatives", S0)
def _(d=1):
    d = _d(d)
    hi = {0: 20, 1: 60, 2: 200}[d]

    def _n():
        return random.randint(-hi, hi)

    def _neg():
        return -random.randint(1, hi)

    def _pair():
        # every pair has a negative; harder tiers make both negative and close, so the
        # child must see that -179 < -143 although 179 > 143
        if d == 0 or random.random() < 0.3:
            a, b = _neg(), random.randint(-hi, hi)
        else:
            a = -random.randint(hi // 4, hi)
            b = a + random.choice([-1, 1]) * random.randint(1, max(3, hi // 5))
            b = min(-1, b)
        while a == b:
            b = _neg()
        return (a, b) if random.random() < 0.5 else (b, a)

    def _many(k):
        # at least half the list negative; at hard, several close negatives
        s = set()
        while len(s) < (k + 1) // 2:
            s.add(_neg() if d < 2 or not s else min(-1, min(s) + random.randint(-hi // 5, hi // 5)))
        while len(s) < k:
            s.add(_n())
        xs = list(s)
        random.shuffle(xs)
        return xs

    def _minus(a, b):
        """'6 − 2', '6 − (-2)': brackets only round a negative."""
        return "%d − %s" % (a, ("(%d)" % b) if b < 0 else "%d" % b)

    def t_greater():
        a, b = _pair()
        return _tb("Which is greater, %d or %d? Type the greater number." % (a, b),
                   max(a, b), "int", {},
                   ["On a number line, %d is to the right of %d." % (max(a, b), min(a, b)),
                    "%d is greater." % max(a, b)])

    def t_smaller():
        a, b = _pair()
        return _tb("Which is smaller, %d or %d? Type the smaller number." % (a, b),
                   min(a, b), "int", {},
                   ["The further left on a number line, the smaller.",
                    "%d is smaller." % min(a, b)])

    def t_symbol():
        a, b = _pair()
        sym = "<" if a < b else ">"
        return _wq("Type the correct symbol, < or >, to complete:   %d ___ %d" % (a, b),
                   sym, ["%d is further %s on the number line than %d." % (a, "left" if a < b else "right", b),
                         "%d %s %d." % (a, sym, b)], "< or >")

    def _winter():
        # real winter-dawn readings for these northern cities (about -30 to 8 °C);
        # harder tiers pick two close negatives rather than bigger numbers
        if d == 0:
            return random.randint(-10, -1), random.randint(-5, 8)
        lo = -20 if d == 1 else -30
        a = random.randint(lo, -2)
        b = a + random.choice([-1, 1]) * random.randint(1, 6 if d == 1 else 4)
        b = max(lo, min(-1, b))
        return a, (b if b != a else a - 1)

    def t_temp():
        ca, cb = random.sample(_CITIES, 2)
        ta, tb = _winter()
        if random.random() < 0.5:
            ta, tb = tb, ta
        return _tb("On a winter morning it was %d°C in %s and %d°C in %s. Which "
                   "temperature is colder? Type it." % (ta, ca, tb, cb),
                   min(ta, tb), "int", {},
                   ["Colder means lower on the scale.",
                    "%d°C is colder than %d°C." % (min(ta, tb), max(ta, tb))])

    def t_warmer_diff():
        # a day's rise in a UK-like climate: start -12..4 °C, finish below 20 °C
        lo = {0: random.randint(-5, -1), 1: random.randint(-9, 4), 2: random.randint(-12, -3)}[d]
        rise = random.randint(*{0: (3, 9), 1: (4, 14), 2: (9, 22)}[d])
        top = lo + rise
        return _tb("The temperature rose from %d°C to %d°C. By how many degrees did "
                   "it rise?" % (lo, top), rise, "int", {},
                   ["%s = %d." % (_minus(top, lo), rise)])

    def t_greatest():
        xs = _many({0: 4, 1: 5, 2: 5}[d])
        return _tb("Which of these is the greatest?   %s" % _lst(xs), max(xs), "int", {},
                   ["In order: %s." % _lst(sorted(xs)),
                    "The greatest is the one furthest right on the number line: %d." % max(xs)])

    def t_least():
        xs = _many({0: 4, 1: 5, 2: 5}[d])
        return _tb("Which of these is the least?   %s" % _lst(xs), min(xs), "int", {},
                   ["In order: %s." % _lst(sorted(xs)),
                    "The least is the one furthest left on the number line: %d." % min(xs)])

    def t_nth():
        xs = _many(5)
        i = random.randint(2, 4)
        ans = sorted(xs)[i - 1]
        return _tb("Put these in order, smallest first. Which number is %s?   %s"
                   % (ordinal(i), _lst(xs)), ans, "int", {},
                   ["In order: %s." % _lst(sorted(xs)),
                    "The %s number is %d." % (ordinal(i), ans)])

    def t_set_greater():
        xs = _many(5)
        lim = sorted(xs)[1]
        big = [x for x in xs if x > lim]
        return _setq("Type all of these that are greater than %d:   %s" % (lim, _lst(xs)),
                     big, ["Greater than %d: %s." % (lim, _lst(sorted(big)))],
                     "e.g. -3, 4, 7")

    def t_line():
        a = _neg()
        lo = ((a - 4) // 2) * 2 - 2
        return _nl("Place %d on the number line." % a, a, lo, lo + 20, 1, 5,
                   ["%d sits %d steps from %d." % (a, a - lo, lo)])

    def t_line_least():
        # three integers within about 20 of each other, so the line stays in 1s at a readable size
        base = _neg()
        xs = set([base])
        while len(xs) < 3:
            xs.add(base + random.randint(-8, 12) if d else base + random.randint(-6, 20))
        xs = sorted(xs)
        target = xs[0]
        lo = ((target - 3) // 5) * 5
        hi = lo + 25
        while hi < xs[-1] + 1:
            hi += 5
        return _nl("Here are three integers: %s. Place the SMALLEST one on the line."
                   % _lst(sorted(xs, key=lambda _z: random.random())),
                   target, lo, hi, 1, 5,
                   ["In order: %s." % _lst(xs),
                    "%d is furthest left on the number line, so it is the smallest%s." % (
                        target, " (the negative furthest from zero)" if target < 0 else "")])

    return _pick_t([t_greater, t_smaller, t_symbol, t_temp, t_warmer_diff,
                    t_greatest, t_least, t_nth, t_set_greater],
                   [t_line, t_line_least])


@skill("Y8.0.b", "Place value; compare and order decimals", S0)
def _(d=1):
    d = _d(d)
    dp = {0: 2, 1: 3, 2: 4}[d]
    _PLACES = [("tenths", 1), ("hundredths", 2), ("thousandths", 3),
               ("ten-thousandths", 4)]

    def _dec():
        whole = random.randint(0, 9 if d == 0 else 99)
        frac = "".join(str(random.randint(0, 9)) for _ in range(dp))
        return Decimal("%d.%s" % (whole, frac))

    def _pair():
        a, b = _dec(), _dec()
        if random.random() < 0.5:                # close pair: share the whole part
            b = (Decimal(int(a)) + Decimal("0." + "".join(
                str(random.randint(0, 9)) for _ in range(dp))))
        while a == b:
            b = _dec()
        return a, b

    def t_digit_value():
        x = _dec()
        place, pos = pick(_PLACES[:dp])
        digit = int((x * (10 ** pos)) % 10)
        return _tb("In the number %s, which digit is in the %s place?" % (_fmt(x), place),
                   digit, "int", {},
                   ["The %s is the %s digit after the point." % (place, ordinal(pos)),
                    "That digit is %d." % digit])

    def t_place_of():
        x = _dec()
        place, pos = pick(_PLACES[:dp])
        digit = int((x * (10 ** pos)) % 10)
        while digit == 0 or _fmt(x).count(str(digit)) > 1:   # the digit must be unique
            x = _dec()
            digit = int((x * (10 ** pos)) % 10)
        opts = " / ".join(p for p, q in _PLACES[:dp])
        return _wq("In %s, which place is the digit %d in? (%s)" % (_fmt(x), digit, opts),
                   place, ["The %d is in the %s place." % (digit, place)], opts)

    def t_value_worth():
        x = _dec()
        place, pos = pick(_PLACES[:dp])
        digit = int((x * (10 ** pos)) % 10)
        while digit == 0:
            x = _dec()
            digit = int((x * (10 ** pos)) % 10)
        val = _fmt(Decimal(digit).scaleb(-pos))
        return _tb("In %s, what is the VALUE of the digit in the %s place? (as a decimal)"
                   % (_fmt(x), place), val, "num", {},
                   ["The %s digit is %d, worth %s." % (place, digit, val)])

    def t_greater():
        a, b = _pair()
        return _numq("Which is greater, %s or %s? Type the greater number."
                     % (_fmt(a), _fmt(b)), _fmt(max(a, b)),
                     [_why_bigger(a, b), "%s is greater." % _fmt(max(a, b))])

    def t_smaller():
        a, b = _pair()
        return _numq("Which is smaller, %s or %s? Type the smaller number."
                     % (_fmt(a), _fmt(b)), _fmt(min(a, b)),
                     [_why_bigger(a, b), "%s is smaller." % _fmt(min(a, b))])

    def t_symbol():
        a, b = _pair()
        sym = "<" if a < b else ">"
        return _wq("Type < or > to complete:   %s ___ %s" % (_fmt(a), _fmt(b)),
                   sym, [_why_bigger(a, b), "%s %s %s." % (_fmt(a), sym, _fmt(b))], "< or >")

    def t_order_smallest():
        xs = [_dec() for _ in range(4)]
        while len(set(xs)) < 4:
            xs = [_dec() for _ in range(4)]
        return _numq("Type the SMALLEST of these decimals:   %s"
                     % _lst(_fmt(v) for v in xs), _fmt(min(xs)),
                     ["In order: %s." % _lst(_fmt(v) for v in sorted(xs)),
                      "The smallest is %s." % _fmt(min(xs))])

    def t_order_largest():
        xs = [_dec() for _ in range(4)]
        while len(set(xs)) < 4:
            xs = [_dec() for _ in range(4)]
        return _numq("Type the LARGEST of these decimals:   %s"
                     % _lst(_fmt(v) for v in xs), _fmt(max(xs)),
                     ["In order: %s." % _lst(_fmt(v) for v in sorted(xs)),
                      "The largest is %s." % _fmt(max(xs))])

    def t_nth():
        xs = [_dec() for _ in range(4)]
        while len(set(xs)) < 4:
            xs = [_dec() for _ in range(4)]
        i = random.randint(2, 3)
        ans = sorted(xs)[i - 1]
        return _numq("Put these decimals in order, smallest first. Which is %s?   %s"
                     % (ordinal(i), _lst(_fmt(v) for v in xs)), _fmt(ans),
                     ["In order: %s." % _lst(_fmt(v) for v in sorted(xs)),
                      "The %s is %s." % (ordinal(i), _fmt(ans))])

    def t_table():
        towns = random.sample(_TOWNS, 4)
        # one race: times of a similar size, so the decimals decide the order
        base = random.randint(11, 15) if d == 0 else random.randint(48, 62)
        vals = set()
        while len(vals) < 4:
            vals.add(Decimal(base + random.randint(0, 1)) + Decimal("0." + "".join(
                str(random.randint(0, 9)) for _ in range(min(dp, 3)))))
        vals = list(vals)
        rows = [[t, _fmt(v)] for t, v in zip(towns, vals)]
        big = random.random() < 0.5
        want = max(vals) if big else min(vals)
        return _dt("The table shows race times (seconds). What is the %s time in "
                   "the table?" % ("longest" if big else "shortest"),
                   ["Runner", "Time (s)"], rows, _fmt(want),
                   ["In order: %s." % _lst(_fmt(v) for v in sorted(vals)),
                    "The %s time is %s." % ("longest" if big else "shortest",
                                            _fmt(want))], atype="num")

    def t_line():
        whole = random.randint(1, 6)
        k = random.randint(1, 9)
        if d == 0:
            ans = Decimal(whole) + Decimal(k) / 10
            return _nl("Place %s on the number line." % _fmt(ans), ans,
                       whole, whole + 1, Decimal("0.1"), Decimal("0.5"),
                       ["%s is %d %s past %d." % (_fmt(ans), k, "tenth" if k == 1 else "tenths", whole)])
        # core/stretch: zoom in on one tenth (or hundredth), marked in the next place
        unit = Decimal("0.01") if d == 1 else Decimal("0.001")
        start = Decimal(whole) + Decimal(random.randint(0, 9)) / (10 if d == 1 else 100)
        ans = start + k * unit
        return _nl("Place %s on the number line." % _fmt(ans), ans,
                   start, start + 10 * unit, unit, 5 * unit,
                   ["The line runs from %s to %s in steps of %s." % (_fmt(start), _fmt(start + 10 * unit), _fmt(unit)),
                    "%s is %d %s past %s." % (_fmt(ans), k, "step" if k == 1 else "steps", _fmt(start))])

    return _pick_t([t_digit_value, t_place_of, t_value_worth, t_greater, t_smaller,
                    t_symbol, t_order_smallest, t_order_largest, t_nth],
                   [t_table, t_line])


@skill("Y8.0.c", "Round to decimal places and significant figures", S0)
def _(d=1):
    d = _d(d)

    def _dec():
        whole = random.randint(0, 9 if d == 0 else 999)
        frac = "".join(str(random.randint(0, 9)) for _ in range(random.randint(3, 5)))
        return Decimal("%d.%s" % (whole, frac))

    def t_dp():
        dp = random.randint(1, 3 if d else 2)
        x = _dec()
        while _dround(x, dp) == x:                    # the number must need rounding
            x = _dec()
        ans = _dround(x, dp)
        return _numq("Round %s to %d decimal place%s." % (_fmt(x), dp, "" if dp == 1 else "s"),
                     format(ans, "f"),
                     ["Look at the digit in the next place along.", _why_dp(x, dp)])

    def t_nearest():
        x = _dec()
        ans = _dround(x, 0)
        return _numq("Round %s to the nearest whole number." % _fmt(x), _fmt(ans),
                     ["The first decimal digit decides.", _why_dp(x, 0)])

    def t_sf_small():
        sig = random.randint(1, 3 if d else 2)
        while True:                                   # the number must need rounding
            whole = random.randint(0, 0 if d == 0 else 9)
            frac = "".join(str(random.randint(0, 9)) for _ in range(5))
            x = Decimal("%d.%s" % (whole, frac))
            if x != 0 and _sfround(x, sig) != x:
                break
        ans = _sfround(x, sig)
        return _numq("Round %s to %d significant figure%s."
                     % (_fmt(x), sig, "" if sig == 1 else "s"), format(ans, "f"),   # 5.90, not 5.9, to 3 s.f.
                     ["Count significant figures from the first non-zero digit.", _why_sf(x, sig),
                      "%s to %d s.f. is %s." % (_fmt(x), sig, format(ans, "f"))])

    def t_sf_big():
        while True:                                   # the number must need rounding
            n = random.randint(1000, 999999) if d else random.randint(100, 9999)
            sig = random.randint(1, 3)
            ans = _sfround(Decimal(n), sig)
            if ans != n:
                break
        return _numq("Round %d to %d significant figure%s."
                     % (n, sig, "" if sig == 1 else "s"), _fmt(ans),
                     ["Keep %d significant figure%s, the rest become zeros."
                      % (sig, "" if sig == 1 else "s"), _why_sf(n, sig),
                      "%d to %d s.f. is %s." % (n, sig, _fmt(ans))])

    def t_money():
        p = random.randint(101, [999, 9999, 99999][d])
        raw = Decimal(p) / 100 + Decimal(random.randint(1, 9)) / 1000
        if d == 2:                                    # stretch: 4 d.p. on the calculator
            raw += Decimal(random.randint(1, 9)) / 10000
        ans = _dround(raw, 2)
        return _numq("A bill is shared, and the calculator shows each share as £%s. Round "
                     "this to 2 decimal places (the nearest penny)." % _fmt(raw), format(ans, "f"),
                     ["2 d.p. gives an exact number of pence.", _why_dp(raw, 2)], unit="£")

    def t_measure():
        if d == 2:                                    # stretch: 3 d.p., the thousandths can mislead
            x = Decimal(pick([n for n in range(1000, 100000) if n % 100])) / 1000
        else:                                         # always 2 d.p. to round
            x = Decimal(pick([n for n in range(100, 1000 if d == 0 else 10000) if n % 10])) / 100
        who = pick(NAMES)
        ans = _dround(x, 1)
        return _numq("%s measures a plank as %s m. Round this length to 1 decimal "
                     "place." % (who, _fmt(x)), format(ans, "f"),
                     [_why_dp(x, 1)], unit="m")

    def t_which_rounds():
        base = Decimal(random.randint(1, 8) if d < 2 else random.randint(10, 99)) \
            + Decimal(random.randint(1, 8)) / 10
        if d == 2:                                    # stretch: the right one is just BELOW, decoys close by
            good = base - Decimal(random.randint(1, 4)) / 100
            opts = [good, base - Decimal("0.06"), base + Decimal("0.05"),
                    base - Decimal("0.1")]
        else:
            good = base + Decimal(random.randint(1, 4)) / 100
            opts = [good, base - Decimal("0.07"), base + Decimal("0.09"),
                    base + Decimal("0.13")]
        opts = [o for o in opts if _dround(o, 1) == base] + \
               [o for o in opts if _dround(o, 1) != base]
        want = opts[0]
        show = opts[:]
        random.shuffle(show)
        return _numq("Which of these rounds to %s when rounded to 1 decimal place?"
                     "   %s" % (_fmt(base), _lst(_fmt(o) for o in show)), _fmt(want),
                     [_why_dp(want, 1),
                      "The others round to something else: %s." % "; ".join(
                          "%s → %s" % (_fmt(o), format(_dround(o, 1), "f")) for o in show if o != want)])

    def t_yes_no():
        x = _dec()
        dp = random.randint(1, 2)
        real = _dround(x, dp)
        claim = real if random.random() < 0.5 else real + Decimal(1).scaleb(-dp)
        said, right = _fmt(claim), format(real, "f")        # 356.0 to 1 d.p. keeps its zero: "356" is not it
        sol = ["%s to %d d.p. is %s." % (_fmt(x), dp, right)]
        if claim == real and said != right:
            sol.append("To %d d.p. it must show %d decimal place%s, so %s is not correct."
                       % (dp, dp, "" if dp == 1 else "s", said))
        return _yn("%s says %s rounded to %d d.p. is %s. Is that correct? (yes/no)"
                   % (pick(NAMES), _fmt(x), dp, said),
                   "yes" if said == right else "no", sol)

    def t_table():
        xs = sorted({_dec() for _ in range(4)})
        while len(xs) < 4:
            xs = sorted({_dec() for _ in range(4)})
        rows = [[_fmt(v), format(_dround(v, 1), "f")] for v in xs]     # 537.0, not 537: 1 d.p. shows one place
        r = random.randint(0, 3)
        return _dt("Complete the rounding table. What belongs in the empty cell "
                   "(rounded to 1 d.p.)?", ["Number", "To 1 d.p."], rows,
                   format(_dround(xs[r], 1), "f"),
                   [_why_dp(xs[r], 1)],
                   missing=[r, 1], atype="num")

    return _pick_t([t_dp, t_nearest, t_sf_small, t_sf_big, t_money, t_measure,
                    t_which_rounds, t_yes_no],
                   [t_table])


@skill("Y8.0.d", "Integers and decimals on number lines", S0)
def _(d=1):
    d = _d(d)

    def t_int_pos():
        lo = random.randint(0, [20, 40, 40][d]) * (5 if d == 2 else 1)
        step = pick([[1], [1, 2], [5, 10, 25]][d])
        if d == 2:
            lo -= lo % step
        ans = lo + step * random.randint(1, 9)
        return _nl("Place %d on the number line." % ans, ans, lo, lo + step * 10,
                   step, step * 5, ["%d is %d %s of %d past %d."
                                    % (ans, (ans - lo) // step,
                                       "step" if ans - lo == step else "steps", step, lo)])

    def t_int_neg():
        span = pick([[10], [10, 20], [40, 60]][d])
        step = 2 if d == 2 else 1                     # stretch: the line counts in 2s
        ans = step * random.randint(-span // step, span // step)
        while ans == 0:
            ans = step * random.randint(-span // step, span // step)
        return _nl("Place %d on the number line." % ans, ans, -span, span, step,
                   step * 5, ["Count %s from zero%s." % ("left" if ans < 0 else "right",
                                                         " in steps of 2" if step == 2 else "")])

    def t_dec_tenths():
        whole = random.randint(0, 5)
        k = random.randint(1, 9)
        if d == 2:                                    # stretch: hundredths on a zoomed-in line
            lo = Decimal(whole) + Decimal(k - 1) / 10
            j = random.randint(1, 9)
            ans = lo + Decimal(j) / 100
            return _nl("Place %s on the number line." % _fmt(ans), ans, lo, lo + Decimal("0.1"),
                       Decimal("0.01"), Decimal("0.05"),
                       ["Each small step is one hundredth.",
                        "%s is %d %s past %s." % (_fmt(ans), j, "hundredth" if j == 1 else "hundredths",
                                                  _fmt(lo))])
        ans = Decimal(whole) + Decimal(k) / 10
        return _nl("Place %s on the number line." % _fmt(ans), ans, whole, whole + 1,
                   Decimal("0.1"), Decimal("0.5"),
                   ["%s is %d %s past %d." % (_fmt(ans), k, "tenth" if k == 1 else "tenths", whole)])

    def t_dec_neg():
        whole = -random.randint(*[(0, 0), (1, 4), (5, 19)][d])     # easy: between -1 and 0
        k = random.randint(1, 9)
        ans = Decimal(whole) - Decimal(k) / 10
        return _nl("Place %s on the number line." % _fmt(ans), ans, whole - 1, whole + 1,
                   Decimal("0.1"), Decimal("0.5"),
                   ["%s is between %d and %d." % (_fmt(ans), whole - 1, whole)])

    def t_between():
        lo = random.randint(*[(0, 5), (-5, 5), (-9, 2)][d])
        a = lo + 2 + random.randint(0, 1)
        b = a + 2
        ans = a + 1
        if d == 2:                                    # stretch: decimal bounds, often negative
            a = Decimal(ans) - Decimal(random.randint(1, 9)) / 10
            b = Decimal(ans) + Decimal(random.randint(1, 9)) / 10
            return _nl("Place the whole number on the line that is greater than %s and less "
                       "than %s." % (_fmt(a), _fmt(b)), ans, lo, lo + 8, 1, 4,
                       ["The only whole number between %s and %s is %d." % (_fmt(a), _fmt(b), ans)])
        return _nl("Place the whole number on the line that is greater than %d and less "
                   "than %d." % (a, b), ans, lo, lo + 8, 1, 4,
                   ["The only whole number between %d and %d is %d." % (a, b, ans)])

    def t_rounded():
        x = Decimal(random.randint(1, 8)) + Decimal(random.randint(1, 9)) / 10
        if d == 0:
            x = Decimal(random.randint(1, 8)) + Decimal(pick([1, 2, 3, 7, 8, 9])) / 10   # never near .5
        elif d == 2:                                  # stretch: 2 d.p., and negative half the time
            x = Decimal(random.randint(1, 8)) + Decimal(pick([n for n in range(1, 100) if n != 50])) / 100
            if random.random() < 0.5:
                x = -x
        ans = _dround(x, 0)
        lo = math.floor(x) - 1
        return _nl("Round %s to the nearest whole number, then place your answer on "
                   "the line." % _fmt(x), ans, lo, lo + 4, 1, 1,
                   [_why_dp(x, 0) if x > 0 else "%s is nearer to %s than to %s, so it rounds to %s."
                    % (_fmt(x), _fmt(ans), _fmt(ans + (1 if ans <= x else -1)), _fmt(ans))])

    def t_midpoint():
        step = pick([[2, 10], [2, 4, 10], [Decimal("0.2"), Decimal("0.6"), 20]][d])
        lo = random.randint(*[(0, 4), (-2, 4), (-6, 0)][d]) * step
        a = lo + step
        b = lo + 3 * step
        ans = (a + b) / 2 if d == 2 else (a + b) // 2
        return _nl("Place the number that is exactly halfway between %s and %s."
                   % (_fmt(a), _fmt(b)), ans, lo, lo + 4 * step, step / 2 if d == 2 else step // 2, step,
                   ["Add them and halve: (%s + %s) ÷ 2 = %s." % (_fmt(a), _fmt(b), _fmt(ans)),
                    "Halfway between %s and %s is %s." % (_fmt(a), _fmt(b), _fmt(ans))])

    def t_count_on():
        start = random.randint(*[(0, 6), (-6, 6), (-6, 6)][d])
        step = pick([[1, 2], [1, 2, 3], [3, 4, 5]][d])
        jumps = random.randint(2, 4 if d < 2 else 3)
        if d == 2 and random.random() < 0.6:          # stretch: count BACK, often past zero
            ans = start - step * jumps
            return _nl("Start at %d and count back %d jumps of %d. Place where you land."
                       % (start, jumps, step), ans, min(start, ans) - 2,
                       min(start, ans) - 2 + 20, 1, 5,
                       ["%d − %d × %d = %d." % (start, jumps, step, ans)])
        ans = start + step * jumps
        return _nl("Start at %d and count on %d jumps of %d. Place where you land."
                   % (start, jumps, step), ans, min(start, ans) - 2,
                   min(start, ans) - 2 + 20, 1, 5,
                   ["%d + %d × %d = %d." % (start, jumps, step, ans)])

    def t_temp_line():
        if d == 2:                                    # stretch: work out the reading first
            start = random.randint(-4, 9)
            ans = start - random.randint(max(3, start + 2), start + 14)
            return _nl("A thermometer reads %d°C. The temperature falls by %d degrees. Place the new "
                       "temperature on the line." % (start, start - ans), ans, -20, 20, 1, 5,
                       ["%d − %d = %d, so the new temperature is %d°C." % (start, start - ans, ans, ans)])
        ans = random.randint(-5 if d == 0 else -8, 8)
        while ans == 0:
            ans = random.randint(-5 if d == 0 else -8, 8)
        return _nl("A thermometer reads %d°C. Place that temperature on the line."
                   % ans, ans, -10, 10, 1, 5,
                   ["%d°C is %d below zero." % (ans, -ans) if ans < 0
                    else "%d°C is above zero." % ans])

    def t_graph_h():
        span = {0: 5, 1: 10, 2: 12}[d]
        ans = random.randint(-span + 1, span - 1)
        while ans == 0:
            ans = random.randint(-span + 1, span - 1)
        return _nl("Graph the integer %d on the horizontal number line." % ans,
                   ans, -span, span, 1, 5,
                   ["%d is %d step%s to the %s of zero."
                    % (ans, abs(ans), "" if abs(ans) == 1 else "s",
                       "right" if ans > 0 else "left")])

    def t_graph_v():
        if d == 2:
            step, span = 2, 20
        else:
            step, span = 1, {0: 5, 1: 10}[d]
        k = random.randint(1, span // step)
        ans = step * k * (1 if random.random() < 0.5 else -1)
        # the line is drawn across the page, so the question talks about right and left, not up and down
        return _nl("Graph the integer %d on the number line. Positive integers are to the right of "
                   "zero and negative integers are to the left." % ans,
                   ans, -span, span, step, step * 5,
                   ["%d is %d step%s of %d to the %s of zero."
                    % (ans, k, "" if k == 1 else "s", step,
                       "right" if ans > 0 else "left")])

    if d == 0:          # still Year 8: no "place 7 on a 0-10 line" or "count on 3 jumps of 2"
        return _pick_t([], [t_int_neg, t_dec_tenths, t_dec_neg, t_rounded, t_midpoint, t_temp_line, t_graph_v])
    return _pick_t([t_int_pos], [t_int_neg, t_dec_tenths, t_dec_neg, t_between,
                                 t_rounded, t_midpoint, t_count_on, t_temp_line,
                                 t_graph_h, t_graph_v])


@skill("Y8.0.e", "Order and classify rational numbers", S0)
def _(d=1):
    d = _d(d)

    def _frac():
        den = pick({0: [2, 4, 5, 10], 1: [2, 4, 5, 8, 10, 20, 25], 2: [8, 20, 25, 40, 50]}[d])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        if random.random() < {0: 0.2, 1: 0.4, 2: 0.5}[d]:
            f = -f
        return f

    def t_frac_to_dec():
        f = _frac()
        return _numq("Write the fraction %s as a decimal." % _fmt_frac(f),
                     _fmt(Decimal(f.numerator) / Decimal(f.denominator)),
                     ["%s = %s ÷ %s = %s." % (_fmt_frac(f), f.numerator, f.denominator,
                                              _fmt(Decimal(f.numerator) / Decimal(f.denominator)))])

    def t_compare():
        f = _frac()
        dv = Decimal(f.numerator) / Decimal(f.denominator)
        other = dv + pick({0: [Decimal("0.2"), Decimal("-0.2"), Decimal("0.3")],
                           1: [Decimal("0.1"), Decimal("-0.1"), Decimal("0.15"), Decimal("-0.2")],
                           2: [Decimal("0.01"), Decimal("-0.02"), Decimal("0.05"), Decimal("-0.05")]}[d])
        vals = [(dv, _fmt_frac(f)), (other, _fmt(other))]
        smaller = min(vals, key=lambda z: z[0])
        return _numq("Which is smaller, %s or %s? Type your answer as a decimal."
                     % (vals[0][1], vals[1][1]), _fmt(smaller[0]),
                     ["%s = %s." % (_fmt_frac(f), _fmt(dv)), _why_bigger(dv, other),
                      "The smaller value is %s." % _fmt(smaller[0])])

    def t_order_smallest():
        vals = set()
        while len(vals) < 3:
            f = _frac()
            vals.add(Decimal(f.numerator) / Decimal(f.denominator))
        vals = list(vals)
        toks = [_fmt(v) for v in vals]
        random.shuffle(toks)
        return _numq("Order these from smallest to largest, and type the smallest:"
                     "   %s" % _lst(toks), _fmt(min(vals)),
                     ["In order: %s." % _lst(_fmt(v) for v in sorted(vals)),
                      "The smallest is %s: %s" % (_fmt(min(vals)), "the negative furthest from zero."
                                                  if min(vals) < 0 else "it is furthest left on the number line.")])

    def t_between():
        target = pick({0: [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)],
                       1: [Fraction(1, 4), Fraction(3, 8), Fraction(3, 5), Fraction(7, 10)],
                       2: [Fraction(5, 8), Fraction(7, 20), Fraction(9, 25), Fraction(-3, 8), Fraction(-11, 20)]}[d])
        dv = Decimal(target.numerator) / Decimal(target.denominator)
        gap = Decimal("0.05") if d == 2 else Decimal("0.15")      # stretch: a narrow interval
        lo = dv - gap
        hi = dv + gap
        others = [dv - 2 * gap, dv + 2 * gap]
        toks = [(_fmt_frac(target), dv)] + [("%s" % _fmt(o), o) for o in others]
        random.shuffle(toks)
        shown = _lst(t for t, _v in toks)
        return _numq("Which of these lies between %s and %s? Type it as a decimal."
                     "   %s" % (_fmt(lo), _fmt(hi), shown), _fmt(dv),
                     ["%s = %s, which is between %s and %s."
                      % (_fmt_frac(target), _fmt(dv), _fmt(lo), _fmt(hi))])

    def t_is_integer():
        num = random.randint(2, {0: 9, 1: 9, 2: 20}[d]) * pick({0: [2, 5, 10], 1: [2, 3, 4], 2: [3, 4, 6, 7]}[d])
        den = pick({0: [2, 5, 10], 1: [2, 3, 4], 2: [3, 4, 6, 7, 8]}[d])
        f = Fraction(num, den)
        return _yn("Is %d/%d an integer? (yes/no)" % (num, den),
                   "yes" if f.denominator == 1 else "no",
                   ["%d ÷ %d leaves a remainder of %d, so it is not a whole number."
                    % (num, den, num % den) if f.denominator != 1
                    else "%d/%d = %d, a whole number." % (num, den, num // den)])

    def t_terminating():
        den = pick({0: [2, 3, 4, 5, 9, 10], 1: [2, 3, 4, 5, 6, 8, 9, 11],
                    2: [6, 12, 14, 15, 24, 30, 35, 40]}[d])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        # stretch shows the fraction unsimplified (3/12): cancel first, then look at the denominator
        shown = "%d/%d" % (num, den) if d == 2 else _fmt_frac(f)
        return _yn("Does the fraction %s give a terminating decimal? (yes/no)"
                   % shown, "yes" if _terminates(f) else "no",
                   ["A fraction terminates only if its denominator (in lowest terms) "
                    "has just 2s and 5s as prime factors.",
                    "%s is %s." % (shown if shown == _fmt_frac(f) else "%s = %s, which" % (shown, _fmt_frac(f)),
                                   "terminating" if _terminates(f) else "recurring")])

    def t_count_neg():
        vals = []
        while len(vals) < 5:
            f = _frac()
            v = Decimal(f.numerator) / Decimal(f.denominator)
            if v not in [z[1] for z in vals]:
                vals.append((_fmt_frac(f) if random.random() < 0.5 else _fmt(v), v))
        neg = sum(1 for _t, v in vals if v < 0)
        return _tb("How many of these numbers are negative?   %s"
                   % _lst(t for t, _v in vals), neg, "int", {},
                   ["Count the ones less than zero.", "There are %d." % neg])

    def t_nth_dec():
        vals = set()
        while len(vals) < 4:
            f = _frac()
            vals.add(Decimal(f.numerator) / Decimal(f.denominator))
        vals = list(vals)
        toks = [_fmt(v) for v in vals]
        random.shuffle(toks)
        i = random.randint(2, 3)
        ans = sorted(vals)[i - 1]
        return _numq("Order these smallest first. Which is %s? Type it.   %s"
                     % (ordinal(i), _lst(toks)), _fmt(ans),
                     ["In order: %s." % _lst(_fmt(v) for v in sorted(vals)),
                      "The %s is %s." % (ordinal(i), _fmt(ans))])

    def t_reciprocal():
        # Multiplicative inverse (reciprocal) of a rational number.
        if random.random() < {0: 1.0, 1: 0.5, 2: 0.0}[d]:
            n = random.randint(2, 12)
            return {"prompt": "The reciprocal (also called the multiplicative "
                    "inverse) of %d is a fraction. Write it, like 1/7." % n,
                    "component": "number",
                    "spec": {"text": True, "placeholder": "e.g. 1/7"},
                    "answer": "1/%d" % n, "answer_type": "frac", "tolerance": 0,
                    "solution": ["The reciprocal of a whole number %d is 1/%d "
                                 "(their product is 1)." % (n, n)]}
        pairs = [(2, 3), (2, 5), (2, 7), (2, 9), (3, 4), (3, 5), (3, 7), (3, 8),
                 (4, 5), (4, 7), (5, 6), (5, 8), (4, 9), (5, 9), (3, 10), (7, 10)]
        a, b = pick(pairs)
        sg = "-" if d == 2 and random.random() < 0.5 else ""      # stretch: a negative keeps its sign
        return {"prompt": "Find the multiplicative inverse (the reciprocal) of the "
                "fraction %s%d/%d. Give your answer as a fraction, like 5/2." % (sg, a, b),
                "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 5/2"},
                "answer": "%s%d/%d" % (sg, b, a), "answer_type": "frac", "tolerance": 0,
                "solution": ["To find the reciprocal, swap the numerator and "
                             "denominator%s." % (" and keep the sign" if sg else ""),
                             "The multiplicative inverse of %s%d/%d is %s%d/%d."
                             % (sg, a, b, sg, b, a)]}

    return _pick_t({0: [t_frac_to_dec, t_compare, t_order_smallest, t_is_integer,
                        t_count_neg, t_reciprocal],
                    1: [t_frac_to_dec, t_compare, t_order_smallest, t_between,
                        t_is_integer, t_terminating, t_count_neg, t_nth_dec,
                        t_reciprocal],
                    2: [t_frac_to_dec, t_compare, t_between, t_terminating, t_nth_dec,
                        t_reciprocal]}[d], [])


def _fmt_frac(f):
    """Fraction -> display like '-3/4' or '5'."""
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f < 0 else ""
    return "%s%d/%d" % (sign, abs(f.numerator), f.denominator)


@skill("Y8.0.f", "Compare numbers with <, > and =", S0)
def _(d=1):
    d = _d(d)

    def _int():
        hi = {0: 20, 1: 60, 2: 150}[d]
        return random.randint(-hi, hi)

    def _dec():
        if d == 0:                                    # easy: positive, 1 d.p.
            return Decimal(random.randint(0, 20)) + Decimal(random.randint(0, 9)) / 10
        return Decimal(random.randint(-50, 50)) + Decimal(random.randint(0, 99)) / 100

    def _dec_pair():
        a = _dec()
        if d < 2:
            return a, _dec()
        # stretch: two numbers very close together, often negative, with different numbers of d.p.
        b = a + Decimal(pick([n for n in range(-90, 91) if n])) / 1000
        return (a, b) if random.random() < 0.5 else (b, a)

    def _sym(a, b):
        return "<" if a < b else (">" if a > b else "=")

    def t_int_sym():
        a, b = _int(), _int()
        return _wq("Type <, > or = to compare:   %d ___ %d" % (a, b), _sym(a, b),
                   (["%d is further %s on the number line than %d." % (a, "left" if a < b else "right", b)]
                    if a != b else []) + ["%d %s %d." % (a, _sym(a, b), b)], "< > or =")

    def t_dec_sym():
        a, b = _dec_pair()
        return _wq("Type <, > or = to compare:   %s ___ %s" % (_fmt(a), _fmt(b)),
                   _sym(a, b), ([_why_bigger(a, b)] if a != b else [])
                   + ["%s %s %s." % (_fmt(a), _sym(a, b), _fmt(b))], "< > or =")

    def t_equal_case():
        f = Fraction(random.randint(1, [3, 5, 9][d]), pick([[2, 4, 10], [2, 4, 5, 10], [8, 20, 25, 40]][d]))
        if d == 2 and random.random() < 0.5:          # stretch: negative fractions too
            f = -f
        dv = Decimal(f.numerator) / Decimal(f.denominator)
        if random.random() < 0.5:
            b = dv
        else:
            gap = Decimal("0.01") if d == 2 else Decimal("0.1")
            b = dv + pick([gap, -gap])
        return _wq("Type <, > or = to compare:   %s ___ %s" % (_fmt_frac(f), _fmt(b)),
                   _sym(dv, b),
                   ["%s = %s." % (_fmt_frac(f), _fmt(dv)),
                    "%s %s %s." % (_fmt(dv), _sym(dv, b), _fmt(b))], "< > or =")

    def t_neg_vs_pos():
        top = [10, 30, 99][d]
        a = -random.randint(1, top)
        b = random.randint(1, top)
        if d == 2 and random.random() < 0.6:          # stretch: two negatives
            while -b == a:
                b = random.randint(1, top)
            b = -b
            return _wq("Type <, > or = to compare:   %d ___ %d" % (a, b), _sym(a, b),
                       ["For negative numbers, the one further from zero is the smaller.",
                        "%d %s %d." % (a, _sym(a, b), b)], "< > or =")
        if random.random() < 0.5:
            a, b = b, a
        return _wq("Type <, > or = to compare:   %d ___ %d" % (a, b), _sym(a, b),
                   ["A negative number is always less than a positive one.",
                    "%d %s %d." % (a, _sym(a, b), b)], "< > or =")

    def t_expr():
        a = random.randint(*[(1, 10), (-8, 8), (-15, 15)][d])
        b = random.randint(*[(-5, -1), (-8, 8), (-15, 15)][d])
        if d == 2:                                    # stretch: subtract a directed number
            left = a - b
            right = left + pick([-2, -1, 0, 1, 2])
            return _wq("Type <, > or = to compare:   %d − (%d) ___ %d" % (a, b, right),
                       _sym(left, right),
                       ["%d − (%d) = %d." % (a, b, left),
                        "%d %s %d." % (left, _sym(left, right), right)], "< > or =")
        left = a + b
        right = random.randint(-16, 16)
        return _wq("Type <, > or = to compare:   %d + (%d) ___ %d" % (a, b, right),
                   _sym(left, right),
                   ["%d + (%d) = %d." % (a, b, left),
                    "%d %s %d." % (left, _sym(left, right), right)], "< > or =")

    def t_ineq_yes():
        op = pick(["<", ">"] if d < 2 else ["<", ">", "<=", ">="])
        value = random.randint(-4, 6)
        test = value + pick([[-3, -2, 2, 3], [-2, -1, 1, 2], [-1, 0, 0, 1]][d])   # stretch: on the boundary
        sat = {"<": test < value, ">": test > value, "<=": test <= value, ">=": test >= value}[op]
        return _ineq("The number line shows an inequality in x. Does x = %d satisfy "
                     "it? (yes/no)" % test, op, value, value - 6, value + 6,
                     "yes" if sat else "no",
                     ["The arrow shows x %s %d." % (op, value),
                      "%d %s %d is %s." % (test, op, value,
                                           "true" if sat else "false")])

    def t_ineq_read():
        op = pick(["<", ">"] if d == 0 else ["<", ">", "<=", ">="])
        value = random.randint(*[(0, 6), (-4, 6), (-12, 12)][d])
        disp = {"<": "<", ">": ">", "<=": "<=", ">=": ">="}[op]
        return _ineq("Read the inequality shown on the number line and type it (use x, "
                     "like x>3; type ≤ as <= and ≥ as >=).", op, value, value - 6, value + 6,
                     "x%s%d" % (disp, value),
                     ["The circle is %s and the arrow points %s."
                      % ("open" if op in ("<", ">") else "filled",
                         "left" if "<" in op else "right"),
                      "So x %s %d." % (op, value)])

    def t_true_false():
        a, b = _int(), _int()
        sym = pick(["<", ">"])
        truth = (a < b) if sym == "<" else (a > b)
        return _yn("Is this true?   %d %s %d   (yes/no)" % (a, sym, b),
                   "yes" if truth else "no",
                   ["%d %s %d, so the statement is %s."
                    % (a, _sym(a, b), b, "true" if truth else "false")])

    def t_table_sym():
        a, b = _dec_pair()
        return _dt("Type <, > or = for the empty cell to compare the two numbers.",
                   ["First", "Symbol", "Second"], [[_fmt(a), "?", _fmt(b)]],
                   _sym(a, b), ([_why_bigger(a, b)] if a != b else [])
                   + ["%s %s %s." % (_fmt(a), _sym(a, b), _fmt(b))],
                   missing=[0, 1], atype="str")

    return _pick_t([t_int_sym, t_dec_sym, t_equal_case, t_neg_vs_pos, t_expr,
                    t_true_false],
                   [t_ineq_yes, t_ineq_read, t_table_sym])


@skill("Y8.0.g", "Priority of operations (BIDMAS)", S0)
def _(d=1):
    d = _d(d)
    hi = {0: 6, 1: 9, 2: 12}[d]                    # the largest single number in most framings

    def t_bracket_add():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(2, hi)
        ans = a * (b + c)
        return _tb("Work out:   %d × (%d + %d)" % (a, b, c), ans, "int", {},
                   ["Brackets first: %d + %d = %d." % (b, c, b + c),
                    "%d × %d = %d." % (a, b + c, ans)])

    def t_mul_before_add():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(2, 20)
        ans = c + a * b
        return _tb("Work out:   %d + %d × %d" % (c, a, b), ans, "int", {},
                   ["Multiply first: %d × %d = %d." % (a, b, a * b),
                    "%d + %d = %d." % (c, a * b, ans)])

    def t_index():
        a = random.randint(2, 3 if d == 0 else 5)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        if d == 2:                                 # stretch: index, then multiply, then subtract
            ans = b * a ** 2 - c
            return _tb("Work out (use BIDMAS):   %d × %d^2 − %d" % (b, a, c), ans, "int", {},
                       ["Index first: %d^2 = %d." % (a, a * a),
                        "%d × %d = %d, then − %d = %d." % (b, a * a, b * a * a, c, ans)])
        ans = c + a ** 2
        return _tb("Work out (use BIDMAS):   %d + %d^2" % (c, a), ans, "int", {},
                   ["Index first: %d^2 = %d." % (a, a * a),
                    "%d + %d = %d." % (c, a * a, ans)])

    def t_full():
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        c = random.randint(2, 5)
        e = random.randint(2, 9)
        ans = a * (b + c) - e
        return _tb("Work out:   %d × (%d + %d) − %d" % (a, b, c, e), ans, "int", {},
                   ["Brackets: %d + %d = %d." % (b, c, b + c),
                    "%d × %d = %d, then − %d = %d." % (a, b + c, a * (b + c), e, ans)])

    def t_div_mix():
        q = random.randint(2, hi)
        b = random.randint(2, hi)
        a = q * b
        c = random.randint(2, 20)
        ans = c + a // b
        return _tb("Work out:   %d + %d ÷ %d" % (c, a, b), ans, "int", {},
                   ["Divide first: %d ÷ %d = %d." % (a, b, a // b),
                    "%d + %d = %d." % (c, a // b, ans)])

    def t_two_bracket():
        a = random.randint(6, 12)
        b = random.randint(1, 5)
        c = random.randint(6, 12)
        e = random.randint(1, 5)
        while a - b == 0:
            b = random.randint(1, 5)
        ans = (a - b) * (c - e)
        return _tb("Work out:   (%d − %d) × (%d − %d)" % (a, b, c, e), ans, "int", {},
                   ["First bracket: %d. Second bracket: %d." % (a - b, c - e),
                    "%d × %d = %d." % (a - b, c - e, ans)])

    def t_decimal():
        a = Decimal(random.randint(2, 9))
        b = Decimal(random.randint(2, 9)) / 10
        c = random.randint(2, 6)
        ans = a + b * c
        return _numq("Work out:   %s + %s × %d" % (_fmt(a), _fmt(b), c), _fmt(ans),
                     ["Multiply first: %s × %d = %s." % (_fmt(b), c, _fmt(b * c)),
                      "%s + %s = %s." % (_fmt(a), _fmt(b * c), _fmt(ans))])

    def t_missing_val():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(3, 20)
        total = a * b + c
        if d == 2:                                 # stretch: the gap is inside the product
            return _tb("Fill the missing number:   %d × ___ + %d = %d" % (a, c, total),
                       b, "int", {},
                       ["%d − %d = %d." % (total, c, a * b),
                        "%d ÷ %d = %d." % (a * b, a, b)])
        return _tb("Fill the missing number:   %d × %d + ___ = %d" % (a, b, total),
                   c, "int", {},
                   ["%d × %d = %d." % (a, b, a * b),
                    "%d − %d = %d." % (total, a * b, c)])

    def t_insert_bracket():
        a = random.randint(2, 5)
        b = random.randint(2, 6)
        c = random.randint(2, 6)
        ans = a * (b + c)
        return _tb("Sam writes %d × %d + %d and puts brackets round %d + %d to do that "
                   "part first. What does the calculation equal now?"
                   % (a, b, c, b, c), ans, "int", {},
                   ["With brackets: %d + %d = %d first." % (b, c, b + c),
                    "%d × %d = %d." % (a, b + c, ans)])

    def t_compare():
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        c = random.randint(2, 6)
        left = a + b * c
        right = (a + b) * c
        big = max(left, right)
        return _tb("Which is larger, %d + %d × %d or (%d + %d) × %d? Type the larger "
                   "value." % (a, b, c, a, b, c), big, "int", {},
                   ["%d + %d × %d = %d." % (a, b, c, left),
                    "(%d + %d) × %d = %d." % (a, b, c, right),
                    "The larger is %d." % big])

    def t_word():
        who = pick(NAMES)
        pack = random.randint(4, 8)
        boxes = random.randint(3, 6)
        extra = random.randint(2, 9)
        ans = boxes * pack + extra
        return _tb("%s has %d boxes of %d pencils and %d loose pencils. Write the "
                   "total as %d × %d + %d and work it out." % (who, boxes, pack, extra,
                                                               boxes, pack, extra),
                   ans, "int", {},
                   ["%d × %d = %d." % (boxes, pack, boxes * pack),
                    "%d + %d = %d." % (boxes * pack, extra, ans)])

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            a = random.randint(2, hi)
            b = random.randint(2, hi)
            c = random.randint(2, 12)
            rows.append(["%d + %d × %d" % (c, a, b), str(c + a * b)])
            if i == r_i:
                a0, b0, c0, want = a, b, c, c + a * b
        return _dt("Complete the table using BIDMAS. What value belongs in the empty "
                   "cell?", ["Calculation", "Answer"], rows, want,
                   ["Multiply before adding: %d × %d = %d." % (a0, b0, a0 * b0),
                    "%d + %d = %d." % (c0, a0 * b0, want)], missing=[r_i, 1])

    def t_square_bracket():                        # stretch: brackets, then the index, then the rest
        a = random.randint(3, 6)
        b = random.randint(1, 4)
        c = random.randint(2, 6)
        e = random.randint(2, min(9, ((a + b) ** 2 - 1) // c))     # keeps the answer positive
        ans = (a + b) ** 2 - c * e
        return _tb("Work out:   (%d + %d)^2 − %d × %d" % (a, b, c, e), ans, "int", {},
                   ["Brackets: %d + %d = %d." % (a, b, a + b),
                    "Index: %d^2 = %d." % (a + b, (a + b) ** 2),
                    "Multiply: %d × %d = %d." % (c, e, c * e),
                    "%d − %d = %d." % ((a + b) ** 2, c * e, ans)])

    def t_eval_dec():
        a = Decimal(random.randint(2, 9))
        b = Decimal(random.randint(1, 9)) / 10
        c = random.randint(2, 6)
        forms = []
        v1 = (a + b) * c
        forms.append(("(%s + %s) × %d" % (_fmt(a), _fmt(b), c), v1,
                      "Brackets first: %s + %s = %s, then × %d = %s."
                      % (_fmt(a), _fmt(b), _fmt(a + b), c, _fmt(v1))))
        v2 = a + b * c
        forms.append(("%s + %s × %d" % (_fmt(a), _fmt(b), c), v2,
                      "Multiply first: %s × %d = %s, then + %s = %s."
                      % (_fmt(b), c, _fmt(b * c), _fmt(a), _fmt(v2))))
        expr, val, sol = pick(forms)
        return _numq("Evaluate this numerical expression involving decimals (use "
                     "BIDMAS):   %s" % expr, _fmt(val), [sol])

    return _pick_t({0: [t_bracket_add, t_mul_before_add, t_index, t_div_mix,
                        t_missing_val, t_insert_bracket, t_word],
                    1: [t_bracket_add, t_mul_before_add, t_index, t_full, t_div_mix,
                        t_two_bracket, t_decimal, t_missing_val, t_insert_bracket,
                        t_compare, t_word, t_eval_dec],
                    2: [t_index, t_full, t_two_bracket, t_decimal, t_missing_val,
                        t_compare, t_eval_dec, t_square_bracket]}[d], [t_table])


@skill("Y8.0.h", "Estimate to check a calculation", S0)
def _(d=1):
    d = _d(d)

    def t_product():
        a = random.randint(11, 89) * [1, 10, 100][d] + random.randint(0, 9)
        b = random.randint(11, 89)
        A, B = _r1sf(a), _r1sf(b)
        return _tb("Estimate %d × %d by rounding each number to 1 significant figure."
                   % (a, b), A * B, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d × %d = %d." % (A, B, A * B)])

    def t_sum():
        lo, hi = [(11, 89), (110, 890), (1100, 8900)][d]
        xs = [random.randint(lo, hi) for _ in range([2, 3, 4][d])]
        est = sum(_r1sf(x) for x in xs)
        return _tb("Estimate %s by rounding each number to 1 significant figure."
                   % " + ".join(str(x) for x in xs), est, "int", {},
                   ["Rounded: %s." % " + ".join(str(_r1sf(x)) for x in xs),
                    "Estimate = %d." % est])

    def t_diff():
        if d == 0:                                    # easy: 2-digit numbers
            a, b = random.randint(40, 90), random.randint(10, 34)
        elif d == 1:
            a, b = random.randint(400, 900), random.randint(100, 349)   # 350 would round to 400: 400 − 400 = 0
        else:                                         # stretch: 4-digit numbers
            a, b = random.randint(4000, 9000), random.randint(1000, 3400)
        A, B = _r1sf(a), _r1sf(b)
        return _tb("Estimate %d − %d by rounding each number to 1 significant figure."
                   % (a, b), A - B, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d − %d = %d." % (A, B, A - B)])

    def t_quotient():
        for _ in range(30 if d < 2 else 300):
            B = pick([[2, 3, 4, 5], [2, 3, 4, 5, 6, 8], [3, 4, 6, 7, 8, 9]][d]) \
                * pick([[1], [1, 10], [10, 100]][d])
            q = random.randint(2, [20, 40, 90][d])
            A = B * q
            if len(str(A)) <= [3, 4, 5][d] and _r1sf(A) == A:
                a = _near_1sf(A)
                b = _near_1sf(B)
                if _r1sf(a) == A and _r1sf(b) == B:
                    return _tb("Estimate %d ÷ %d by rounding each number to 1 "
                               "significant figure." % (a, b), A // B, "int", {},
                               ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                                "%d ÷ %d = %d." % (A, B, A // B)])
        return _tb("Estimate 592 ÷ 21 by rounding each number to 1 significant figure.",
                   30, "int", {}, ["600 ÷ 20 = 30."])

    def t_reasonable():
        a = random.randint(*[(11, 49), (21, 89), (210, 890)][d])     # stretch: 3-digit × 2-digit
        b = random.randint(*[(11, 49), (21, 89), (21, 89)][d])
        real = a * b
        A, B = _r1sf(a), _r1sf(b)
        est = A * B
        claim = real if random.random() < 0.5 else pick([real * 10, real // 10])   # a place-value slip
        return _yn("%s worked out %d × %d and got %d. Rounding each number to 1 s.f. "
                   "gives an estimate of %d. Is %d a reasonable answer? (yes/no)"
                   % (pick(NAMES), a, b, claim, est, claim),
                   "yes" if claim == real else "no",
                   ["Estimate: %d × %d = %d." % (A, B, est),
                    "The exact answer is %d, so %d is %s." % (real, claim,
                        "reasonable" if claim == real else "not reasonable")])

    def t_money():
        items = random.randint(*[(2, 3), (3, 5), (4, 6)][d])
        prices = [random.randint(*[(110, 490), (180, 690), (180, 1890)][d]) for _ in range(items)]
        est = sum(_r1sf(p) for p in prices)
        show = ", ".join("£%s" % _fmt(Decimal(p) / 100) for p in prices)
        return _tb("A shopper buys items priced %s (in pence: %s). Estimate the total "
                   "in PENCE by rounding each price to 1 significant figure."
                   % (show, ", ".join(str(p) for p in prices)), est, "int", {},
                   ["Rounded pence: %s." % " + ".join(str(_r1sf(p)) for p in prices),
                    "Estimate = %dp." % est])

    def t_which_est():
        a = random.randint(*[(18, 62), (180, 620), (1800, 6200)][d])
        b = random.randint(18, 62)
        A, B = _r1sf(a), _r1sf(b)
        good = A * B
        # decoys are real slips: rounding only one number, a place-value slip, or rounding the wrong way
        sa, sb = 10 ** (len(str(A)) - 1), 10 ** (len(str(B)) - 1)
        slips = [_r1sf(a) * b, a * B, good * 10, good // 10, (A + sa) * B, A * (B + sb),
                 (A - sa) * B, A * (B - sb)]
        opts = [good]
        for v in random.sample(slips, len(slips)):
            if v > 0 and v not in opts and len(opts) < 4:
                opts.append(v)
        show = opts[:]
        random.shuffle(show)
        return _tb("Round each number to 1 significant figure to estimate %d × %d. "
                   "Which of these is that estimate?   %s" % (a, b, _lst(show)),
                   good, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d × %d = %d." % (A, B, good)])

    def t_check_div():
        for _ in range(200):                          # the rounded division must be exact
            b = pick([[19, 21, 29, 31], [19, 21, 29, 31, 39, 41], [39, 41, 59, 61, 79, 81]][d])
            q = random.randint(*[(5, 15), (15, 45), (30, 90)][d])
            a = b * q + random.randint(0, b - 1)
            A, B = _r1sf(a), _r1sf(b)
            if A % B == 0:
                break
        est = A // B if B else 0
        return _tb("Estimate %d ÷ %d by rounding each number to 1 significant figure "
                   "(give a whole-number estimate)." % (a, b), est, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d ÷ %d ≈ %d." % (A, B, est)])

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            a = random.randint(*[(11, 49), (21, 89), (210, 890)][d])
            b = random.randint(*[(11, 49), (21, 89), (21, 89)][d])
            A, B = _r1sf(a), _r1sf(b)
            rows.append(["%d × %d" % (a, b), str(A * B)])
            if i == r_i:
                a0, b0, want = a, b, A * B
        return _dt("Each estimate rounds both numbers to 1 significant figure. What "
                   "estimate belongs in the empty cell?", ["Calculation", "Estimate"],
                   rows, want,
                   ["%d ≈ %d and %d ≈ %d." % (a0, _r1sf(a0), b0, _r1sf(b0)),
                    "%d × %d = %d." % (_r1sf(a0), _r1sf(b0), want)], missing=[r_i, 1])

    def t_dec_estimate():
        def dec(lo, hi):
            if d == 2:                                # stretch: 2 d.p.
                return Decimal(random.randint(lo, hi)) + Decimal(random.randint(1, 99)) / 100
            return Decimal(random.randint(lo, hi)) + Decimal(random.randint(0, 9)) / 10

        op = pick(["sum", "difference"] if d == 0 else ["sum", "difference", "product"])
        if d == 2 and op == "product":
            a, b = dec(2, 19), dec(2, 9)
            ra, rb = _dround(a, 0), _dround(b, 0)
            est = ra * rb
            expr = "%s × %s" % (_fmt(a), _fmt(b))
        elif op == "sum":
            a, b = dec(3, 29), dec(3, 29)
            ra, rb = _dround(a, 0), _dround(b, 0)
            est = ra + rb
            expr = "%s + %s" % (_fmt(a), _fmt(b))
        elif op == "difference":
            a, b = dec(20, 49), dec(3, 18)      # a always rounds above b
            ra, rb = _dround(a, 0), _dround(b, 0)
            est = ra - rb
            expr = "%s − %s" % (_fmt(a), _fmt(b))
        else:
            a, b = dec(2, 9), dec(2, 9)
            ra, rb = _dround(a, 0), _dround(b, 0)
            est = ra * rb
            expr = "%s × %s" % (_fmt(a), _fmt(b))
        return _numq("Estimate the %s   %s   by first rounding each decimal to the "
                     "nearest whole number." % (op, expr), _fmt(est),
                     ["%s ≈ %s and %s ≈ %s." % (_fmt(a), _fmt(ra), _fmt(b), _fmt(rb)),
                      "Estimated %s: %s." % (op, _fmt(est))])

    return _pick_t([t_product, t_sum, t_diff, t_quotient, t_reasonable, t_money,
                    t_which_est, t_check_div, t_dec_estimate], [t_table])


# ==================================================================== 8.1 ====
@skill("Y8.1.a", "Divisibility rules", S1)
def _(d=1):
    d = _d(d)
    RULES = {2: "even (ends in 0, 2, 4, 6 or 8)",
             3: "its digit sum is a multiple of 3",
             4: "its last two digits form a multiple of 4",
             5: "it ends in 0 or 5",
             6: "it is divisible by both 2 and 3",
             9: "its digit sum is a multiple of 9",
             10: "it ends in 0"}
    DIVS = {0: [2, 5, 10], 1: [2, 3, 4, 5, 6, 9, 10], 2: [3, 4, 6, 9]}[d]

    def _n():
        return random.randint(100, 999 if d == 0 else 9999)

    def t_yesno():
        k = pick(DIVS)
        if random.random() < 0.5:
            n = random.randint(20, 300) * k              # a true multiple
        else:
            n = _n()
        return _yn("Is %d divisible by %d? (yes/no)" % (n, k),
                   "yes" if n % k == 0 else "no",
                   ["A number is divisible by %d when %s." % (k, RULES[k]),
                    "%d ÷ %d %s exact." % (n, k, "is" if n % k == 0 else "is not")])

    def t_which_set():
        k = pick(DIVS)
        xs = random.sample(range(50, 400), 5)
        good = [x for x in xs if x % k == 0]
        if not good:
            cand = random.randint(20, 60) * k
            xs[0] = cand if cand not in xs[1:] else random.randint(20, 60) * k
            good = [x for x in xs if x % k == 0]
        return _setq("Type all of these that are divisible by %d:   %s" % (k, _lst(xs)),
                     good, ["Divisible by %d when %s." % (k, RULES[k]),
                            "Those are %s." % _lst(sorted(good))])

    def t_missing_digit():
        k = pick([3, 9] if d else [3])
        a = random.randint(1, 9)
        b = random.randint(0, 9)
        base = a * 100 + b * 10
        need = (-(a + b)) % k
        n = base + need
        if d == 2:                                    # stretch: 4 digits, and the LARGEST digit
            c = random.randint(0, 9)
            need = (-(a + b + c)) % k
            big = need + k * ((9 - need) // k)
            return _tb("What is the LARGEST single digit that can go in the box to make %d%d%d_ "
                       "divisible by %d?" % (a, b, c, k), big, "int", {},
                       ["The digit sum must be a multiple of %d." % k,
                        "%d + %d + %d + %d = %d, a multiple of %d, and no bigger digit works."
                        % (a, b, c, big, a + b + c + big, k)])
        return _tb("What single digit goes in the box to make %d%d_ divisible by %d? "
                   "(smallest such digit)" % (a, b, k), need, "int", {},
                   ["The digit sum must be a multiple of %d." % k,
                    "%d + %d + %d = %d, a multiple of %d." % (a, b, need, a + b + need, k)])

    def t_rule_word():
        k = pick([[2, 5, 10], [2, 3, 4, 5, 9, 10], [3, 4, 6, 9]][d])
        n = random.randint(*[(100, 999), (100, 999), (1000, 99999)][d])
        return _yn("You can test divisibility by %d using the rule: %s. Using this, is "
                   "%d divisible by %d? (yes/no)" % (k, RULES[k], n, k),
                   "yes" if n % k == 0 else "no",
                   ["%d ÷ %d %s exact." % (n, k, "is" if n % k == 0 else "is not")])

    def t_digit_sum():
        n = random.randint(*[(100, 999), (100, 9999), (10000, 999999)][d])
        ds = sum(int(c) for c in str(n))
        return _tb("What is the digit sum of %d? (This tests divisibility by 3 and 9.)"
                   % n, ds, "int", {},
                   ["Add the digits: %s = %d." % (" + ".join(str(n)), ds)])

    def t_by_six():
        n = random.randint(*[(30, 200), (100, 999), (1000, 99999)][d])
        return _yn("A number is divisible by 6 if it is divisible by both 2 and 3. Is "
                   "%d divisible by 6? (yes/no)" % n, "yes" if n % 6 == 0 else "no",
                   ["%d is %s and %s." % (n, "even" if n % 2 == 0 else "odd",
                                          "a multiple of 3" if n % 3 == 0
                                          else "not a multiple of 3"),
                    "So it %s divisible by 6." % ("is" if n % 6 == 0 else "is not")])

    def t_count():
        k = pick([[2, 5, 10], [2, 3, 5], [3, 4, 6, 9]][d])
        xs = random.sample(range(*[(20, 100), (20, 200), (100, 1000)][d]), 6)
        c = sum(1 for x in xs if x % k == 0)
        return _tb("How many of these numbers are divisible by %d?   %s" % (k, _lst(xs)),
                   c, "int", {},
                   ["The multiples of %d are %s." % (k, _lst([x for x in xs if x % k == 0]))
                    if c else "No number in the list is a multiple of %d." % k,
                    "That is %d of them." % c])

    def t_not_div():
        k = pick(DIVS)
        xs = [m * k for m in random.sample(range(20, 60), 3)]
        bad = random.randint(20, 60) * k + random.randint(1, k - 1)
        while bad in xs:
            bad = random.randint(20, 60) * k + random.randint(1, k - 1)
        xs.append(bad)
        random.shuffle(xs)
        return _tb("One of these is NOT divisible by %d. Which one?   %s" % (k, _lst(xs)),
                   bad, "int", {},
                   ["%d ÷ %d leaves a remainder." % (bad, k),
                    "%d is not divisible by %d." % (bad, k)])

    return _pick_t([t_yesno, t_which_set, t_missing_digit, t_rule_word, t_digit_sum,
                    t_by_six, t_count, t_not_div], [])


@skill("Y8.1.b", "Factors, multiples, prime or composite", S1)
def _(d=1):
    d = _d(d)

    def _factors(n):
        fs = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                fs.add(i)
                fs.add(n // i)
            i += 1
        return sorted(fs)

    def t_all_factors():
        n = random.randint(12, 40 if d == 0 else 90)
        return _setq("Type all the factors of %d." % n, _factors(n),
                     ["The factors of %d are %s." % (n, _lst(_factors(n)))],
                     "e.g. 1, 2, 3, 6")

    def t_prime_composite():
        n = random.randint(2, 40 if d == 0 else 99)
        is_p = len(_factors(n)) == 2
        return _wq("Is %d prime or composite? (type 'prime' or 'composite')" % n,
                   "prime" if is_p else "composite",
                   ["%d has factors %s." % (n, _lst(_factors(n))),
                    "%d is %s." % (n, "prime" if is_p else "composite")])

    def t_nth_multiple():
        k = random.randint(*[(2, 10), (3, 12), (11, 25)][d])
        i = random.randint(*[(2, 6), (3, 9), (6, 15)][d])
        return _tb("What is the %s multiple of %d?" % (ordinal(i), k), k * i, "int", {},
                   ["%d × %d = %d." % (k, i, k * i)])

    def t_is_factor():
        b = random.randint(*[(2, 10), (2, 12), (6, 19)][d])
        n = b * random.randint(2, [9, 9, 30][d]) if random.random() < 0.5 \
            else random.randint(*[(10, 60), (20, 90), (100, 400)][d])
        return _yn("Is %d a factor of %d? (yes/no)" % (b, n),
                   "yes" if n % b == 0 else "no",
                   ["%d ÷ %d %s exact." % (n, b, "is" if n % b == 0 else "is not")])

    def t_is_multiple():
        k = random.randint(*[(2, 10), (3, 12), (7, 25)][d])
        n = k * random.randint(2, [10, 12, 30][d]) if random.random() < 0.5 \
            else random.randint(*[(20, 100), (20, 140), (100, 500)][d])
        return _yn("Is %d a multiple of %d? (yes/no)" % (n, k),
                   "yes" if n % k == 0 else "no",
                   ["%d %s in the %d times table." % (n, "is" if n % k == 0 else "is not", k)])

    def t_common_factors():
        lo, hi = [(6, 24), (12, 40), (30, 99)][d]
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        while b == a:
            b = random.randint(lo, hi)
        common = sorted(set(_factors(a)) & set(_factors(b)))
        return _setq("Type all the common factors of %d and %d." % (a, b), common,
                     ["Common factors of %d and %d: %s." % (a, b, _lst(common))],
                     "e.g. 1, 2, 4")

    def t_count_factors():
        n = random.randint(*[(6, 30), (12, 60), (60, 200)][d])
        c = len(_factors(n))
        return _tb("How many factors does %d have?" % n, c, "int", {},
                   ["Factors of %d: %s." % (n, _lst(_factors(n))),
                    "That is %d factors." % c])

    def t_which_prime():
        lo, hi = [(2, 30), (2, 50), (50, 120)][d]
        pool = random.sample(range(lo, hi), 5)
        primes = [x for x in pool if len(_factors(x)) == 2]
        if not primes:
            p = pick([x for x in range(lo, hi) if len(_factors(x)) == 2 and x not in pool])
            pool[0] = p
            primes = [x for x in pool if len(_factors(x)) == 2]
        return _setq("Type all the prime numbers in this list:   %s" % _lst(pool),
                     primes, ["The primes are %s." % _lst(sorted(primes))],
                     "e.g. 2, 3, 5")

    def t_largest_factor():
        n = random.randint(*[(10, 50), (20, 90), (100, 300)][d])
        fs = _factors(n)
        second = fs[-2]
        return _tb("What is the largest factor of %d that is less than %d itself?"
                   % (n, n), second, "int", {},
                   ["Factors of %d: %s." % (n, _lst(fs)),
                    "The largest below %d is %d." % (n, second)])

    def t_table():
        ns = random.sample(range(*[(6, 30), (12, 60), (60, 200)][d]), 3)
        rows = [[str(n), str(len(_factors(n)))] for n in ns]
        r_i = random.randint(0, 2)
        want = len(_factors(ns[r_i]))
        return _dt("Complete the table. How many factors does the number in the empty "
                   "row have?", ["Number", "Number of factors"], rows, want,
                   ["Factors of %d: %s." % (ns[r_i], _lst(_factors(ns[r_i]))),
                    "That is %d factors." % want], missing=[r_i, 1])

    return _pick_t([t_all_factors, t_prime_composite, t_nth_multiple, t_is_factor,
                    t_is_multiple, t_common_factors, t_count_factors, t_which_prime,
                    t_largest_factor], [t_table])


@skill("Y8.1.c", "Prime factorisation in index form", S1)
def _(d=1):
    d = _d(d)
    FMT = ("Write the primes from smallest to largest, using ^ for powers and x "
           "between factors, like 2^3x3x5 (no spaces).")

    def t_full():
        n = _make_composite(d)
        pairs = _pf(n)
        return _wq("Write %d as a product of its prime factors in index form. %s"
                   % (n, FMT), _pf_str(pairs),
                   ["%d = %s." % (n, _pf_str(pairs))], "e.g. 2^3x3x5")

    def t_exponent():
        n = _make_composite(max(d, 1))
        pairs = _pf(n)
        p, e = pick(pairs)
        return _tb("In the prime factorisation of %d, what is the index (power) of %d?"
                   % (n, p), e, "int", {},
                   ["%d = %s." % (n, _pf_str(pairs)),
                    "The power of %d is %d." % (p, e)])

    def t_count_primes():
        n = _make_composite(d)
        pairs = _pf(n)
        total = sum(e for _p, e in pairs)
        return _tb("How many prime factors does %d have, counting repeats? (e.g. 12 = "
                   "2×2×3 has 3)" % n, total, "int", {},
                   ["%d = %s." % (n, " × ".join(str(p) for p, e in pairs for _ in range(e))),
                    "That is %d prime factors." % total])

    def t_distinct_primes():
        n = _make_composite(d)
        pairs = _pf(n)
        return _setq("Type all the distinct prime factors of %d." % n,
                     [p for p, _e in pairs],
                     ["%d = %s." % (n, _pf_str(pairs)),
                      "Its prime factors are %s." % _lst(p for p, _e in pairs)],
                     "e.g. 2, 3, 5")

    def t_from_factors_value():
        pairs = _pf(_make_composite(d))
        n = 1
        for p, e in pairs:
            n *= p ** e
        return _tb("Work out the value of   %s" % _pf_str(pairs).replace("x", " × "),
                   n, "int", {},
                   ["%s = %d." % (_pf_str(pairs).replace("x", " × "), n)])

    def t_is_prime_power():
        if random.random() < 0.5:
            p = pick([2, 3, 5, 7])
            n = p ** random.randint(2, 4)
        else:
            n = _make_composite(d)
        pairs = _pf(n)
        is_pp = len(pairs) == 1
        return _yn("Is %d a power of a single prime number? (yes/no)" % n,
                   "yes" if is_pp else "no",
                   ["%d = %s." % (n, _pf_str(pairs)),
                    "It %s a single prime raised to a power."
                    % ("is" if is_pp else "is not")])

    def t_missing_factor():
        n = _make_composite(max(d, 1))
        pairs = _pf(n)
        idx = random.randrange(len(pairs))
        shown = "x".join("___" if i == idx else ("%d^%d" % (p, e) if e > 1 else str(p))
                         for i, (p, e) in enumerate(pairs))
        p, e = pairs[idx]
        miss = "%d^%d" % (p, e) if e > 1 else "%d" % p
        return _wq("Complete the prime factorisation:   %d = %s.  What goes in the box? "
                   "%s" % (n, shown, FMT), miss,
                   ["%d = %s." % (n, _pf_str(pairs)),
                    "The missing part is %s." % miss], "e.g. 2^3")

    def t_smallest_prime():
        n = _make_composite(d)
        pairs = _pf(n)
        return _tb("What is the smallest prime factor of %d?" % n, pairs[0][0], "int", {},
                   ["%d = %s." % (n, _pf_str(pairs)),
                    "The smallest prime factor is %d." % pairs[0][0]])

    def t_table():
        ns = [_make_composite(d) for _ in range(3)]
        rows = [[str(n), _pf_str(_pf(n))] for n in ns]
        r_i = random.randint(0, 2)
        want = _pf_str(_pf(ns[r_i]))
        return _dt("Complete the table. Write the missing prime factorisation in index "
                   "form, smallest prime first (like 2^3x3x5, no spaces).",
                   ["Number", "Prime factorisation"], rows, want,
                   ["%d = %s." % (ns[r_i], want)], missing=[r_i, 1], atype="str")

    return _pick_t([t_full, t_exponent, t_count_primes, t_distinct_primes,
                    t_from_factors_value, t_is_prime_power, t_missing_factor,
                    t_smallest_prime], [t_table])


@skill("Y8.1.d", "Highest common factor (HCF)", S1)
def _(d=1):
    d = _d(d)

    def _pair():
        g = random.randint(*{0: (2, 6), 1: (2, 12), 2: (6, 25)}[d])
        m = {0: 5, 1: 9, 2: 12}[d]
        a = g * random.randint(2, m)
        b = g * random.randint(2, m)
        while a == b:
            b = g * random.randint(2, m)
        return a, b

    def t_two():
        a, b = _pair()
        h = math.gcd(a, b)
        return _tb("Find the highest common factor (HCF) of %d and %d." % (a, b), h,
                   "int", {},
                   ["List the factors and take the largest they share.",
                    "HCF(%d, %d) = %d." % (a, b, h)])

    def t_three():
        g = random.randint(2, {0: 5, 1: 8, 2: 15}[d])
        m1, m2, m3 = random.sample(range(2, {0: 7, 1: 9, 2: 13}[d]), 3)
        a, b, c = g * m1, g * m2, g * m3
        h = math.gcd(math.gcd(a, b), c)
        return _tb("Find the HCF of %d, %d and %d." % (a, b, c), h, "int", {},
                   ["HCF(%d, %d, %d) = %d." % (a, b, c, h)])

    def t_from_pf():
        a, b = _pair()
        h = math.gcd(a, b)
        return _tb("Using %d = %s and %d = %s, find their HCF."
                   % (a, _pf_str(_pf(a)).replace("x", " × "),
                      b, _pf_str(_pf(b)).replace("x", " × ")), h, "int", {},
                   ["Multiply the prime factors common to both.",
                    "HCF = %d." % h])

    def t_word_rows():
        h = random.randint(*{0: (2, 5), 1: (3, 9), 2: (6, 15)}[d])
        a = h * random.randint(2, 6)
        b = h * random.randint(2, 6)
        while a == b:
            b = h * random.randint(2, 6)
        who = pick(NAMES)
        return _tb("%s has %d red counters and %d blue counters, and wants to make "
                   "identical rows using all the counters, with each row a single "
                   "colour. What is the greatest number of counters that can be in "
                   "each row?" % (who, a, b), math.gcd(a, b), "int", {},
                   ["The row size must divide both %d and %d." % (a, b),
                    "The greatest such number is HCF = %d." % math.gcd(a, b)])

    def t_word_bags():
        h = random.randint(*{0: (2, 6), 1: (4, 10), 2: (8, 18)}[d])
        a = h * random.randint(2, 6)
        b = h * random.randint(2, 6)
        while a == b:
            b = h * random.randint(2, 6)
        return _tb("A packer has %d pens and %d pencils to share into identical bags "
                   "with no items left over. What is the greatest number of bags?"
                   % (a, b), math.gcd(a, b), "int", {},
                   ["The number of bags divides both %d and %d." % (a, b),
                    "Greatest = HCF = %d." % math.gcd(a, b)])

    def t_coprime():
        if d == 2:                                 # stretch: two composites, which may or may not share a factor
            a, b = pick([(15, 28), (21, 32), (25, 36), (27, 40), (35, 48), (33, 35), (21, 35), (26, 39), (45, 56), (49, 63)])
        else:
            a = pick([8, 9, 15, 16, 25, 21, 35])
            b = pick([7, 11, 13, 17, 19] if d else [7, 11, 13])
        return _yn("Do %d and %d have a highest common factor of 1? (yes/no)" % (a, b),
                   "yes" if math.gcd(a, b) == 1 else "no",
                   ["HCF(%d, %d) = %d." % (a, b, math.gcd(a, b))])

    def t_check():
        a, b = _pair()
        h = math.gcd(a, b)
        claim = h if random.random() < 0.5 else pick([x for x in range(2, h + 3) if x != h] or [h + 1])
        return _yn("%s claims the HCF of %d and %d is %d. Is that correct? (yes/no)"
                   % (pick(NAMES), a, b, claim), "yes" if claim == h else "no",
                   ["The true HCF of %d and %d is %d." % (a, b, h)])

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            a, b = _pair()
            h = math.gcd(a, b)
            rows.append([str(a), str(b), str(h)])
            if i == r_i:
                want = h
        return _dt("Complete the HCF table. What belongs in the empty cell?",
                   ["Number A", "Number B", "HCF"], rows, want,
                   ["Find the largest factor shared by the two numbers in that row.",
                    "The HCF is %d." % want], missing=[r_i, 2])

    return _pick_t([t_two, t_three, t_from_pf, t_word_rows, t_word_bags, t_coprime, t_check] if d
                   else [t_two, t_word_rows, t_word_bags, t_coprime, t_check], [t_table])


@skill("Y8.1.e", "Lowest common multiple (LCM)", S1)
def _(d=1):
    d = _d(d)

    def _pair():
        if d == 2:                                    # stretch: bigger, neither a multiple of the other
            while True:
                a, b = random.sample(range(6, 25), 2)
                if max(a, b) % min(a, b) and math.gcd(a, b) > 1:
                    return a, b
        a = random.randint(2, 9 if d == 0 else 12)
        b = random.randint(2, 9 if d == 0 else 12)
        while a == b:
            b = random.randint(2, 9 if d == 0 else 12)
        return a, b

    def t_two():
        a, b = _pair()
        return _tb("Find the lowest common multiple (LCM) of %d and %d." % (a, b),
                   _lcm(a, b), "int", {},
                   ["List multiples of each and find the first they share.",
                    "LCM(%d, %d) = %d." % (a, b, _lcm(a, b))])

    def t_three():
        a, b, c = random.sample([2, 3, 4, 5, 6] if d == 0 else
                                (range(2, 8) if d == 1 else range(4, 16)), 3)
        l = _lcm(_lcm(a, b), c)
        return _tb("Find the LCM of %d, %d and %d." % (a, b, c), l, "int", {},
                   ["LCM(%d, %d, %d) = %d." % (a, b, c, l)])

    def t_from_pf():
        lo, hi = (4, 12) if d == 0 else ((6, 20) if d == 1 else (24, 90))
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        while a == b:
            b = random.randint(lo, hi)
        return _tb("Using %d = %s and %d = %s, find their LCM."
                   % (a, _pf_str(_pf(a)).replace("x", " × "),
                      b, _pf_str(_pf(b)).replace("x", " × ")), _lcm(a, b), "int", {},
                   ["Take the highest power of each prime that appears.",
                    "LCM = %d." % _lcm(a, b)])

    def t_bells():
        a, b = _pair()
        return _tb("Two bells ring together at noon. One rings every %d minutes and the "
                   "other every %d minutes. After how many minutes do they next ring "
                   "together?" % (a, b), _lcm(a, b), "int", {},
                   ["They coincide at the LCM of %d and %d." % (a, b),
                    "LCM = %d minutes." % _lcm(a, b)])

    def t_laps():
        if d == 1:
            a, b = random.randint(3, 9), random.randint(3, 9)
            while a == b:
                b = random.randint(3, 9)
        else:
            a, b = _pair()
        return _tb("Two runners start together. One completes a lap every %d minutes, "
                   "the other every %d minutes. After how many minutes are they next at "
                   "the start line together?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d minutes." % (a, b, _lcm(a, b))])

    def t_nth_common():
        a, b = _pair()
        l = _lcm(a, b)
        i = random.randint(2, 3) if d < 2 else random.randint(3, 5)
        if d == 2:                                    # stretch: the pupil finds the LCM first
            return _tb("What is the %s common multiple of %d and %d?" % (ordinal(i), a, b),
                       l * i, "int", {},
                       ["LCM(%d, %d) = %d, and common multiples are multiples of it." % (a, b, l),
                        "The %s is %d × %d = %d." % (ordinal(i), i, l, i * l)])
        return _tb("The lowest common multiple of %d and %d is %d. What is their "
                   "%s common multiple?" % (a, b, l, ordinal(i)),
                   l * i, "int", {},
                   ["Common multiples are multiples of the LCM %d." % l,
                    "The %s is %d × %d = %d." % (ordinal(i), i, l, i * l)])

    def t_check():
        a, b = _pair()
        l = _lcm(a, b)
        claim = l if random.random() < 0.5 else (l + a if d < 2 else a * b)   # stretch: the a × b slip
        return _yn("%s says the LCM of %d and %d is %d. Is that correct? (yes/no)"
                   % (pick(NAMES), a, b, claim), "yes" if claim == l else "no",
                   ["The true LCM of %d and %d is %d." % (a, b, l)])

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            a, b = _pair()
            rows.append([str(a), str(b), str(_lcm(a, b))])
            if i == r_i:
                want = _lcm(a, b)
        return _dt("Complete the LCM table. What belongs in the empty cell?",
                   ["Number A", "Number B", "LCM"], rows, want,
                   ["Find the smallest number both values divide into.",
                    "The LCM is %d." % want], missing=[r_i, 2])

    return _pick_t([t_two, t_three, t_from_pf, t_bells, t_laps, t_nth_common,
                    t_check], [t_table])


@skill("Y8.1.f", "HCF and LCM word problems", S1)
def _(d=1):
    d = _d(d)

    def _apart(*ns):
        """No two equal, and neither of a pair a multiple of the other (easy lets one in five through)."""
        if len(set(ns)) < len(ns):
            return False
        mult = any(max(x, y) % min(x, y) == 0 for i, x in enumerate(ns) for y in ns[i + 1:])
        return not mult or (d == 0 and random.random() < 0.2)

    def _pair():
        lo, hi = (2, 6) if d == 0 else ((4, 12) if d == 1 else (12, 30))
        while True:
            a, b = random.randint(lo, hi), random.randint(lo, hi)
            if _apart(a, b):
                return a, b

    def _h():
        """Common factor and the multipliers for the HCF framings."""
        return (random.randint(2, 5), 2, 5) if d == 0 else \
               ((None, 3, 8) if d == 1 else (random.randint(8, 18), 3, 11))

    def t_bells():
        a, b = _pair()
        return _tb("At a station, one train departs every %d minutes and another every "
                   "%d minutes. They leave together at 09:00. After how many minutes do "
                   "they next leave together?" % (a, b), _lcm(a, b), "int", {},
                   ["This is the LCM of %d and %d." % (a, b),
                    "LCM = %d minutes." % _lcm(a, b)])

    def t_slabs():
        h, m0, m1 = _h()
        h = h or random.randint(3, 9)
        a, b = h * random.randint(m0, m1), h * random.randint(m0, m1)
        while not _apart(a, b):
            a, b = h * random.randint(m0, m1), h * random.randint(m0, m1)
        return _tb("A rectangular floor is %d cm by %d cm. It is to be tiled with "
                   "identical square tiles that cover it all, with no gaps or overlaps and "
                   "no tile cut. What is the largest "
                   "side length (in cm) each square tile can have?" % (a, b),
                   math.gcd(a, b), "int", {},
                   ["The tile side must divide both %d and %d." % (a, b),
                    "Largest = HCF = %d cm." % math.gcd(a, b)])

    def t_hampers():
        h = random.randint(4, 10) if d == 1 else (random.randint(2, 5) if d == 0 else random.randint(6, 15))
        a, b, c = (h * random.randint(2, 6 if d < 2 else 9) for _ in range(3))
        while not _apart(a, b, c):
            a, b, c = (h * random.randint(2, 6 if d < 2 else 9) for _ in range(3))
        g = math.gcd(math.gcd(a, b), c)
        if d == 2:                                    # stretch: one more step after the HCF
            return _tb("A shop makes the greatest possible number of identical hampers using "
                       "all of %d apples, %d oranges and %d pears, with nothing left over. How "
                       "many apples go in each hamper?" % (a, b, c), a // g, "int", {},
                       ["The greatest number of hampers is HCF(%d, %d, %d) = %d." % (a, b, c, g),
                        "Each hamper gets %d ÷ %d = %d apples." % (a, g, a // g)])
        return _tb("A shop makes identical hampers using all of %d apples, %d oranges "
                   "and %d pears, with nothing left over. What is the greatest number "
                   "of hampers?" % (a, b, c), g, "int", {},
                   ["The number of hampers divides all three amounts.",
                    "Greatest = HCF = %d." % g])

    def t_lighthouse():
        A, B = ([2, 3, 4, 6], [3, 5, 10]) if d == 0 else \
               (([6, 8, 9, 10, 12], [4, 5, 6, 15]) if d == 1 else ([14, 15, 18, 20, 24], [16, 21, 25, 27, 35]))
        a, b = pick(A), pick(B)
        while not _apart(a, b):
            a, b = pick(A), pick(B)
        return _tb("Two lighthouses flash: one every %d seconds, the other every %d "
                   "seconds. They flash together now. After how many seconds do they "
                   "next flash together?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d seconds." % (a, b, _lcm(a, b))])

    def t_ribbon():
        h, m0, m1 = _h()
        h = h or random.randint(4, 12)
        a, b = h * random.randint(m0, m1), h * random.randint(m0, m1)
        while not _apart(a, b):
            a, b = h * random.randint(m0, m1), h * random.randint(m0, m1)
        return _tb("Two ribbons of length %d cm and %d cm are cut into equal pieces as "
                   "long as possible, with none wasted. How long (in cm) is each piece?"
                   % (a, b), math.gcd(a, b), "int", {},
                   ["The piece length divides both %d and %d." % (a, b),
                    "Longest = HCF = %d cm." % math.gcd(a, b)])

    def t_buses():
        A, B = ([4, 5, 6, 10], [6, 8, 15]) if d == 0 else \
               (([12, 15, 18, 20, 24], [10, 15, 20, 25, 30]) if d == 1 else ([16, 18, 24, 27], [20, 30, 36, 40, 45]))
        a, b = pick(A), pick(B)
        while not _apart(a, b):
            a, b = pick(A), pick(B)
        return _tb("Bus A comes every %d minutes and bus B every %d minutes. Both are "
                   "at the stop at 08:00. At how many minutes past 08:00 are they both "
                   "at the stop together again?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d minutes." % (a, b, _lcm(a, b))])

    def t_which_op():
        if random.random() < 0.5:
            a = b = 0
            while not _apart(a, b):
                a, b = random.sample([4, 6, 8, 10] if d == 0 else
                                     ([6, 8, 9, 10, 12, 15] if d == 1 else [12, 15, 16, 18, 20, 24]), 2)
            return _wq("Buns come in packs of %d and rolls in packs of %d. To buy the same "
                       "number of buns and rolls, using the fewest packs, do you need the "
                       "HCF or the LCM? (type 'HCF' or 'LCM')" % (a, b), "LCM",
                       ["'Smallest number both pack sizes go into' means the lowest "
                        "common multiple.", "You need the LCM."], "HCF or LCM")
        h = random.randint(4, 9) if d == 1 else (random.randint(2, 5) if d == 0 else random.randint(8, 16))
        a, b = h * random.randint(3, 6), h * random.randint(3, 6)
        while not _apart(a, b):
            a, b = h * random.randint(3, 6), h * random.randint(3, 6)
        return _wq("To pack %d red and %d blue pens into identical boxes (single colour "
                   "per box) with the greatest box size, do you need the HCF or the "
                   "LCM? (type 'HCF' or 'LCM')" % (a, b), "HCF",
                   ["'Greatest identical size' means the highest common factor.",
                    "You need the HCF."], "HCF or LCM")

    def t_greatest_people():
        h = random.randint(5, 12) if d == 1 else (random.randint(2, 6) if d == 0 else random.randint(8, 20))
        a, b = h * random.randint(2, 6 if d < 2 else 9), h * random.randint(2, 6 if d < 2 else 9)
        while not _apart(a, b):
            a, b = h * random.randint(2, 6 if d < 2 else 9), h * random.randint(2, 6 if d < 2 else 9)
        if d == 2:                                    # stretch: one more step after the HCF
            g = math.gcd(a, b)
            return _tb("%d biscuits and %d sweets are shared equally among as many children "
                       "as possible, with none left over and every child getting the same. "
                       "How many biscuits does each child get?" % (a, b), a // g, "int", {},
                       ["The greatest number of children is HCF(%d, %d) = %d." % (a, b, g),
                        "Each child gets %d ÷ %d = %d biscuits." % (a, g, a // g)])
        return _tb("%d biscuits and %d sweets are shared equally among as many children "
                   "as possible, with none left over and every child getting the same. "
                   "What is the greatest number of children?" % (a, b),
                   math.gcd(a, b), "int", {},
                   ["The number of children divides both %d and %d." % (a, b),
                    "Greatest = HCF = %d." % math.gcd(a, b)])

    return _pick_t([t_bells, t_slabs, t_hampers, t_lighthouse, t_ribbon, t_buses,
                    t_which_op, t_greatest_people], [])


@skill("Y8.1.g", "Evaluate indices (positive integer powers)", S1)
def _(d=1):
    d = _d(d)

    def _base_exp():
        if d == 0:
            return random.randint(2, 6), 2
        if d == 1:
            return random.randint(2, 8), random.randint(2, 3)
        if random.random() < 0.3:                     # stretch: high powers of 2
            return 2, random.randint(6, 10)
        return random.randint(3, 9), random.randint(3, 4)

    def t_eval():
        b, e = _base_exp()
        return _tb("Work out %d^%d. (^ means 'to the power of')" % (b, e), b ** e,
                   "int", {},
                   ["%d^%d = %s = %d." % (b, e, " × ".join([str(b)] * e), b ** e)])

    def t_square():
        b = random.randint(2, 10) if d == 0 else (random.randint(2, 15) if d == 1 else random.randint(13, 25))
        return _tb("What is %d squared (%d^2)?" % (b, b), b * b, "int", {},
                   ["%d^2 = %d × %d = %d." % (b, b, b, b * b)])

    def t_cube():
        b = random.randint(2, 5) if d == 0 else (random.randint(2, 8) if d == 1 else random.randint(6, 12))
        return _tb("What is %d cubed (%d^3)?" % (b, b), b ** 3, "int", {},
                   ["%d^3 = %d × %d × %d = %d." % (b, b, b, b, b ** 3)])

    def t_missing_exp():
        if d == 2:                                    # stretch: longer powers
            b = pick([2, 2, 3, 4, 5])
            e = random.randint(5, 9) if b == 2 else random.randint(4, 6 if b == 3 else 5)
        else:
            b = random.randint(2, 3 if d == 0 else 5)
            e = random.randint(2, 4 if d else 3)
        return _tb("Solve for the power:   %d^? = %d" % (b, b ** e), e, "int", {},
                   ["%d^%d = %d." % (b, e, b ** e),
                    "So the power is %d." % e])

    def t_missing_base():
        if d == 2:                                    # stretch: bigger bases, or a fourth power
            e = pick([2, 3, 4])
            b = random.randint(11, 20) if e == 2 else (random.randint(6, 12) if e == 3 else random.randint(3, 6))
        else:
            b = random.randint(2, 9 if d else 6)
            e = pick([2, 3] if d else [2])
        return _tb("Solve for the base:   ?^%d = %d" % (e, b ** e), b, "int", {},
                   ["%d^%d = %d." % (b, e, b ** e), "So the base is %d." % b])

    def t_compare():
        b1, e1 = _base_exp()
        b2, e2 = _base_exp()
        while b1 ** e1 == b2 ** e2:
            b2, e2 = _base_exp()
        big = max(b1 ** e1, b2 ** e2)
        return _tb("Which is larger, %d^%d or %d^%d? Type its value."
                   % (b1, e1, b2, e2), big, "int", {},
                   ["%d^%d = %d and %d^%d = %d." % (b1, e1, b1 ** e1, b2, e2, b2 ** e2),
                    "The larger value is %d." % big])

    def t_powers_of_ten():
        e = random.randint(2, 3) if d == 0 else (random.randint(2, 6) if d == 1 else random.randint(6, 9))
        if d == 2 and random.random() < 0.5:          # stretch: the inverse
            return _tb("10^? = %s. What is the power?" % "{:,}".format(10 ** e), e, "int", {},
                       ["%s is 1 followed by %d zeros, so it is 10^%d." % ("{:,}".format(10 ** e), e, e)])
        return _tb("Work out 10^%d." % e, 10 ** e, "int", {},
                   ["10^%d is 1 followed by %d zeros = %d." % (e, e, 10 ** e)])

    def t_word():
        who = pick(NAMES)
        b = random.randint(2, 4)
        e = random.randint(2, 4) if d == 0 else (random.randint(3, 5) if d == 1 else random.randint(6, 10))
        return _tb("%s folds a piece of paper in half %d times. The number of layers is "
                   "2^%d. How many layers is that?" % (who, e, e), 2 ** e, "int", {},
                   ["2^%d = %d." % (e, 2 ** e)])

    def t_between():
        b = 2 if d < 2 else pick([3, 5])
        e = random.randint(2, 4) if d == 0 else (random.randint(3, 5) if d == 1 else random.randint(3, 6 if b == 3 else 4))
        val = b ** e
        return _tb("%d to some power equals %d (%d^? = %d). What is the power?"
                   % (b, val, b, val), e, "int", {},
                   ["%d^%d = %d." % (b, e, val)])

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            b, e = _base_exp()
            rows.append(["%d^%d" % (b, e), str(b ** e)])
            if i == r_i:
                b0, e0, want = b, e, b ** e
        return _dt("Complete the table of powers. What value belongs in the empty "
                   "cell?", ["Power", "Value"], rows, want,
                   ["%d^%d = %s = %d." % (b0, e0, " × ".join([str(b0)] * e0), want)],
                   missing=[r_i, 1])

    def t_eval_expr_index():
        b = random.randint(2, 5 if d else 3)
        e = random.randint(2, 3) if d < 2 else random.randint(3, 4)
        p = b ** e
        forms = []
        c = random.randint(2, 12 if d else 9)
        forms.append(("%d + %d^%d" % (c, b, e), c + p,
                      "%d^%d = %d, then %d + %d = %d." % (b, e, p, c, p, c + p)))
        forms.append(("%d × %d^%d" % (c, b, e), c * p,
                      "%d^%d = %d, then %d × %d = %d." % (b, e, p, c, p, c * p)))
        c2 = random.randint(2, p - 1)
        forms.append(("%d^%d − %d" % (b, e, c2), p - c2,
                      "%d^%d = %d, then %d − %d = %d." % (b, e, p, p, c2, p - c2)))
        b2 = random.randint(2, 4 if d < 2 else 9)
        forms.append(("%d^%d + %d^2" % (b, e, b2), p + b2 * b2,
                      "%d^%d = %d and %d^2 = %d, so %d + %d = %d."
                      % (b, e, p, b2, b2 * b2, p, b2 * b2, p + b2 * b2)))
        expr, val, sol = pick(forms)
        return _tb("Evaluate this numerical expression involving indices (use "
                   "BIDMAS):   %s" % expr, val, "int", {}, [sol])

    return _pick_t([t_eval, t_square, t_cube, t_missing_exp, t_missing_base,
                    t_compare, t_powers_of_ten, t_word, t_between,
                    t_eval_expr_index], [t_table])


@skill("Y8.1.h", "Indices with negative and decimal bases", S1)
def _(d=1):
    d = _d(d)

    def t_neg_even():
        if d == 2:                                    # stretch: higher even powers
            e = pick([4, 6])
            b = random.randint(5, 7) if e == 4 else random.randint(2, 3)
        else:                                         # core: squares, or 4th powers of 2–4 (≤ 256)
            e = pick([2, 4] if d else [2])
            b = random.randint(2, (9 if e == 2 else 4) if d else 5)
        val = (-b) ** e
        return _tb("Work out (−%d)^%d." % (b, e), val, "int", {},
                   ["A negative number to an even power is positive.",
                    "(−%d)^%d = %d." % (b, e, val)])

    def t_neg_odd():
        if d == 2:                                    # stretch: fifth powers or bigger cubes
            e = pick([3, 5])
            b = random.randint(7, 12) if e == 3 else random.randint(2, 4)
        else:                                         # core: cubes of 2–6, or 5th powers of 2–3 (≤ 243)
            e = pick([3, 5] if d else [3])
            b = random.randint(2, (6 if e == 3 else 3) if d else 5)
        val = (-b) ** e
        return _tb("Work out (−%d)^%d." % (b, e), val, "int", {},
                   ["A negative number to an odd power stays negative.",
                    "(−%d)^%d = %d." % (b, e, val)])

    def t_sign_only():
        b = random.randint(2, 9)
        e = random.randint(2, 3) if d == 0 else (random.randint(2, 6) if d == 1 else random.randint(7, 25))
        pos = e % 2 == 0
        return _wq("Is (−%d)^%d positive or negative? (type 'positive' or 'negative')"
                   % (b, e), "positive" if pos else "negative",
                   ["An %s power of a negative number is %s."
                    % ("even" if pos else "odd", "positive" if pos else "negative")])

    def t_dec_square():
        if d == 2:                                    # stretch: 1.x or 0.0x bases
            base = pick([Decimal(random.randint(11, 19)) / 10, Decimal(random.randint(1, 9)) / 100])
        else:
            base = Decimal(random.randint(1, 9 if d else 5)) / 10
        val = base * base
        return _numq("Work out %s^2." % _fmt(base), _fmt(val),
                     ["%s × %s = %s." % (_fmt(base), _fmt(base), _fmt(val))])

    def t_dec_cube():
        t = pick([1, 2, 3] if d == 0 else ([2, 3, 4, 5] if d == 1 else [6, 7, 8, 9, 11, 12]))
        base = Decimal(t) / 10
        val = base ** 3
        return _numq("Work out %s^3." % _fmt(base), _fmt(val),
                     ["%s × %s × %s = %s." % (_fmt(base), _fmt(base), _fmt(base),
                                              _fmt(val))])

    def t_half_power():
        base = Decimal("0.5")
        e = pick([2, 3] if d == 0 else ([2, 3, 4] if d == 1 else [4, 5, 6]))
        val = base ** e
        return _numq("Work out %s^%d." % (_fmt(base), e), _fmt(val),
                     ["%s^%d = %s." % (_fmt(base), e, _fmt(val))])

    def t_neg_dec():
        t = random.randint(1, 5) if d == 0 else (random.randint(1, 9) if d == 1 else random.randint(11, 15))
        base = Decimal(t) / 10
        e = pick([2] if d == 0 else [2, 3])
        val = (-base) ** e
        return _numq("Work out (−%s)^%d." % (_fmt(base), e), _fmt(val),
                     ["(−%s)^%d = %s (%s power)." % (_fmt(base), e, _fmt(val),
                                                     "even" if e % 2 == 0 else "odd")])

    def t_compare_sign():
        b = random.randint(2, 6 if d else 4)
        e1, e2 = (2, 3) if d < 2 else pick([(4, 5), (3, 5), (5, 4), (3, 4)])
        if d == 2:
            b = random.randint(2, 3)
        a1 = (-b) ** e1
        a2 = (-b) ** e2
        return _tb("Which is greater, (−%d)^%d or (−%d)^%d? Type its value." % (b, e1, b, e2),
                   max(a1, a2), "int", {},
                   ["(−%d)^%d = %d and (−%d)^%d = %d." % (b, e1, a1, b, e2, a2),
                    "The greater value is %d." % max(a1, a2)])

    return _pick_t([t_neg_even, t_neg_odd, t_sign_only, t_dec_square, t_dec_cube,
                    t_half_power, t_neg_dec, t_compare_sign], [])


@skill("Y8.1.i", "Laws of indices", S1)
def _(d=1):
    d = _d(d)

    def _rng(easy, core, hard):
        return (easy, core, hard)[d]

    def t_multiply_exp():
        b = random.randint(2, 6)
        m = random.randint(*_rng((2, 4), (2, 6), (5, 15)))
        n = random.randint(*_rng((2, 4), (2, 6), (4, 12)))
        return _tb("Using the laws of indices, %d^%d × %d^%d = %d^?. What is the missing "
                   "power?" % (b, m, b, n, b), m + n, "int", {},
                   ["Add the powers: %d + %d = %d." % (m, n, m + n),
                    "%d^%d × %d^%d = %d^%d." % (b, m, b, n, b, m + n)])

    def t_divide_exp():
        b = random.randint(2, 6)
        m = random.randint(*_rng((4, 7), (4, 9), (10, 24)))
        n = random.randint(1 if d < 2 else 3, m - 1)
        return _tb("Using the laws of indices, %d^%d ÷ %d^%d = %d^?. What is the missing "
                   "power?" % (b, m, b, n, b), m - n, "int", {},
                   ["Subtract the powers: %d − %d = %d." % (m, n, m - n),
                    "%d^%d ÷ %d^%d = %d^%d." % (b, m, b, n, b, m - n)])

    def t_power_of_power():
        b = random.randint(2, 5)
        m = random.randint(*_rng((2, 3), (2, 4), (3, 7)))
        n = random.randint(*_rng((2, 3), (2, 4), (3, 6)))
        return _tb("Using the laws of indices, (%d^%d)^%d = %d^?. What is the missing "
                   "power?" % (b, m, n, b), m * n, "int", {},
                   ["Multiply the powers: %d × %d = %d." % (m, n, m * n),
                    "(%d^%d)^%d = %d^%d." % (b, m, n, b, m * n)])

    def t_single_power():
        b = random.randint(2, 6)
        m = random.randint(*_rng((2, 4), (2, 5), (4, 9)))
        n = random.randint(*_rng((2, 4), (2, 5), (3, 8)))
        if d == 2:                                    # stretch: multiply then divide
            p = random.randint(2, m + n - 2)
            return _wq("Write %d^%d × %d^%d ÷ %d^%d as a single power. Use ^ , like %d^7 (no "
                       "spaces)." % (b, m, b, n, b, p, b), "%d^%d" % (b, m + n - p),
                       ["Add the powers: %d + %d = %d." % (m, n, m + n),
                        "Then subtract: %d − %d = %d, so = %d^%d." % (m + n, p, m + n - p, b, m + n - p)],
                       "e.g. %d^7" % b)
        return _wq("Write %d^%d × %d^%d as a single power. Use ^ , like %d^7 (no "
                   "spaces)." % (b, m, b, n, b), "%d^%d" % (b, m + n),
                   ["Add the powers: %d + %d = %d." % (m, n, m + n),
                    "= %d^%d." % (b, m + n)], "e.g. %d^7" % b)

    def t_solve_index():
        b = pick([2, 10] if d == 0 else ([2, 3, 5] if d == 1 else [2, 3, 4, 6, 7]))
        e = random.randint(2, 4) if d == 0 else (random.randint(2, 5) if d == 1 else
                                                 random.randint(7, 12) if b == 2 else random.randint(3, 5))
        return _tb("Solve for x:   %d^x = %d" % (b, b ** e), e, "int", {},
                   ["%d^%d = %d." % (b, e, b ** e), "So x = %d." % e])

    def t_solve_from_law():
        b = random.randint(2, 5)
        if d == 2:                                    # stretch: the unknown inside a division or a bracket
            if random.random() < 0.5:
                m, n = random.randint(9, 20), random.randint(2, 7)
                return _tb("Solve for x:   %d^%d ÷ %d^x = %d^%d" % (b, m, b, b, m - n), n, "int", {},
                           ["Dividing subtracts the powers, so %d − x = %d." % (m, m - n),
                            "x = %d." % n])
            m, n = random.randint(2, 6), random.randint(2, 5)
            return _tb("Solve for x:   (%d^x)^%d = %d^%d" % (b, n, b, m * n), m, "int", {},
                       ["A power of a power multiplies the indices, so %d × x = %d." % (n, m * n),
                        "x = %d." % m])
        m = random.randint(2, 4)
        target = m + random.randint(1, 3)
        n = target - m
        return _tb("Solve for x:   %d^%d × %d^x = %d^%d" % (b, m, b, b, target), n,
                   "int", {},
                   ["The powers on the left add to %d, so %d + x = %d." % (target, m, target),
                    "x = %d." % n])

    def t_evaluate_after():
        b = random.randint(2, 3) if d == 0 else (random.randint(2, 4) if d == 1 else random.randint(2, 5))
        m = random.randint(1 if d < 2 else 2, 2 if d == 0 else 3)
        n = random.randint(1 if d < 2 else 2, 2 if d == 0 else 3)
        if d == 2:                                    # stretch: three factors
            k = random.randint(1, 2)
            while b ** (m + n + k) > 20000:
                b -= 1
            return _tb("Simplify then evaluate:   %d^%d × %d^%d × %d^%d" % (b, m, b, n, b, k),
                       b ** (m + n + k), "int", {},
                       ["= %d^%d = %d." % (b, m + n + k, b ** (m + n + k))])
        return _tb("Simplify then evaluate:   %d^%d × %d^%d" % (b, m, b, n),
                   b ** (m + n), "int", {},
                   ["= %d^%d = %d." % (b, m + n, b ** (m + n))])

    def t_divide_value():
        b = random.randint(2, 3) if d == 0 else random.randint(2, 4 if d == 1 else 6)
        m = random.randint(*_rng((3, 5), (4, 6), (8, 15)))
        n = random.randint(1, 2) if d == 0 else (random.randint(1, 3) if d == 1 else m - random.randint(2, 4))
        return _tb("Simplify then evaluate:   %d^%d ÷ %d^%d" % (b, m, b, n),
                   b ** (m - n), "int", {},
                   ["= %d^%d = %d." % (b, m - n, b ** (m - n))])

    def t_table():
        b = random.randint(2, 6)
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            m = random.randint(*_rng((2, 4), (2, 5), (4, 12)))
            n = random.randint(*_rng((2, 4), (2, 5), (4, 12)))
            rows.append(["%d^%d × %d^%d" % (b, m, b, n), "%d^%d" % (b, m + n)])
            if i == r_i:
                m0, n0, want = m, n, "%d^%d" % (b, m + n)
        return _dt("Complete the table by writing each product as a single power (like "
                   "%d^7, no spaces). What belongs in the empty cell?" % b,
                   ["Product", "Single power"], rows, want,
                   ["Add the powers: %d + %d = %d." % (m0, n0, m0 + n0),
                    "= %s." % want], missing=[r_i, 1], atype="str")

    def t_solve_var_index():
        b = pick([2, 10] if d == 0 else ([2, 3, 5, 10] if d == 1 else [3, 4, 5, 6]))
        e = random.randint(2, 4) if d == 0 else (random.randint(2, 5) if d == 1 else random.randint(3, 6 if b < 5 else 5))
        return _tb("Solve this equation, where the index (power) is the variable "
                   "x:   %d^x = %d" % (b, b ** e), e, "int", {},
                   ["%d^%d = %d, so the variable index x = %d." % (b, e, b ** e, e)])

    return _pick_t([t_multiply_exp, t_divide_exp, t_power_of_power, t_single_power,
                    t_solve_index, t_solve_from_law, t_evaluate_after,
                    t_divide_value, t_solve_var_index], [t_table])


@skill("Y8.1.j", "Square roots and cube roots; estimate surds", S1)
def _(d=1):
    d = _d(d)

    def t_sqrt():
        r = random.randint(2, 10) if d == 0 else (random.randint(2, 15) if d == 1 else random.randint(14, 30))
        return _tb("Work out √%d." % (r * r), r, "int", {},
                   ["%d × %d = %d, so √%d = %d." % (r, r, r * r, r * r, r)])

    def t_cbrt():
        r = random.randint(2, 5) if d == 0 else (random.randint(2, 8) if d == 1 else random.randint(7, 12))
        return _tb("Work out the cube root of %d (∛%d)." % (r ** 3, r ** 3), r, "int", {},
                   ["%d × %d × %d = %d, so ∛%d = %d." % (r, r, r, r ** 3, r ** 3, r)])

    def t_solve_sq():
        r = random.randint(2, 10 if d == 0 else 12)
        if d == 2:                                    # stretch: one step before the root
            c = random.randint(5, 60)
            r = random.randint(6, 20)
            return _tb("Solve for the positive value of x:   x^2 + %d = %d" % (c, r * r + c), r,
                       "int", {}, ["x^2 = %d − %d = %d." % (r * r + c, c, r * r),
                                   "x = √%d = %d." % (r * r, r)])
        return _tb("Solve for the positive value of x:   x^2 = %d" % (r * r), r,
                   "int", {}, ["x = √%d = %d." % (r * r, r)])

    def t_solve_cube():
        r = random.randint(2, 4 if d == 0 else 7)
        if d == 2:                                    # stretch: divide first, or a negative cube
            a = random.randint(2, 5)
            if random.random() < 0.5:
                return _tb("Solve for x:   %dx^3 = %d" % (a, a * r ** 3), r, "int", {},
                           ["x^3 = %d ÷ %d = %d." % (a * r ** 3, a, r ** 3),
                            "x = ∛%d = %d." % (r ** 3, r)])
            return _tb("Solve for x:   x^3 = −%d" % (r ** 3), -r, "int", {},
                       ["(−%d)^3 = −%d, so x = −%d." % (r, r ** 3, r)])
        return _tb("Solve for x:   x^3 = %d" % (r ** 3), r, "int", {},
                   ["x = ∛%d = %d." % (r ** 3, r)])

    def t_estimate_nearest():
        r = random.randint(2, 6) if d == 0 else (random.randint(3, 12) if d == 1 else random.randint(12, 22))
        n = r * r + random.randint(1, 2 * r)          # not a perfect square
        k = math.isqrt(n)
        nearest = k + 1 if 4 * n > (2 * k + 1) ** 2 else k
        return _tb("Estimate √%d to the nearest whole number." % n, nearest, "int", {},
                   ["%d^2 = %d and %d^2 = %d." % (k, k * k, k + 1, (k + 1) ** 2),
                    "√%d is closest to %d." % (n, nearest)])

    def t_between_lower():
        r = random.randint(2, 6) if d == 0 else (random.randint(3, 12) if d == 1 else random.randint(12, 22))
        n = r * r + random.randint(1, 2 * r)
        k = math.isqrt(n)
        return _tb("√%d lies between two consecutive whole numbers. Type the smaller "
                   "one." % n, k, "int", {},
                   ["%d^2 = %d and %d^2 = %d, so √%d is between %d and %d."
                    % (k, k * k, k + 1, (k + 1) ** 2, n, k, k + 1),
                    "The smaller is %d." % k])

    def t_area():
        r = random.randint(3, 10) if d == 0 else random.randint(4, 15 if d == 1 else 25)
        if d == 2:                                    # stretch: side first, then the perimeter
            return _tb("A square has area %d cm². What is its perimeter (in cm)?" % (r * r),
                       4 * r, "int", {},
                       ["Side = √%d = %d cm." % (r * r, r), "Perimeter = 4 × %d = %d cm." % (r, 4 * r)])
        return _tb("A square has area %d cm². What is the length of one side (in cm)?"
                   % (r * r), r, "int", {},
                   ["Side = √area = √%d = %d cm." % (r * r, r)])

    def t_volume():
        r = random.randint(2, 5 if d == 0 else 8)
        if d == 2:                                    # stretch: edge first, then one face
            r = random.randint(3, 10)
            return _tb("A cube has volume %d cm³. What is the area of one face (in cm²)?" % (r ** 3),
                       r * r, "int", {},
                       ["Edge = ∛%d = %d cm." % (r ** 3, r), "Face area = %d × %d = %d cm²." % (r, r, r * r)])
        return _tb("A cube has volume %d cm³. What is the length of one edge (in cm)?"
                   % (r ** 3), r, "int", {},
                   ["Edge = ∛volume = ∛%d = %d cm." % (r ** 3, r)])

    def t_which_between():
        n = pick([2, 3, 5, 7, 8, 10, 15, 20] if d == 0 else
                 ([2, 3, 5, 7, 10, 15, 20, 27, 40, 50, 60] if d == 1 else
                  [75, 90, 110, 130, 150, 175, 200, 250, 300, 450, 500]))
        k = math.isqrt(n)
        return _tb("Between which two consecutive whole numbers does √%d lie? Type the "
                   "larger one." % n, k + 1, "int", {},
                   ["%d^2 = %d and %d^2 = %d." % (k, k * k, k + 1, (k + 1) ** 2),
                    "The larger is %d." % (k + 1)])

    def t_table():
        rs = random.sample(range(2, 11) if d == 0 else (range(2, 15) if d == 1 else range(11, 26)), 3)
        rows = [[str(r * r), str(r)] for r in rs]
        r_i = random.randint(0, 2)
        want = rs[r_i]
        return _dt("Complete the table of square roots. What belongs in the empty "
                   "cell?", ["Number", "Square root"], rows, want,
                   ["%d × %d = %d, so √%d = %d."
                    % (want, want, want * want, want * want, want)], missing=[r_i, 1])

    return _pick_t([t_sqrt, t_cbrt, t_solve_sq, t_solve_cube, t_estimate_nearest,
                    t_between_lower, t_area, t_volume, t_which_between], [t_table])


@skill("Y8.1.k", "Standard form", S1)
def _(d=1):
    d = _d(d)
    FMT = "Write it like 3.2x10^4 (use ^ , no spaces)."

    def t_to_standard_big():
        digits = _rand_digits(d)
        exp = random.randint(len(digits) - 1 + 1, 8)
        sf, value = _sf_from_digits(digits, exp)
        return _wq("Write %s in standard form. %s" % (_fmt(value), FMT), sf,
                   ["Move the point after the first digit.",
                    "%s = %s." % (_fmt(value), sf)], "e.g. 3.2x10^4")

    def t_to_ordinary_big():
        digits = _rand_digits(d)
        exp = random.randint(len(digits) - 1 + 1, 8)
        sf, value = _sf_from_digits(digits, exp)
        return _tb("Write %s as an ordinary number." % sf, _fmt(value), "int", {},
                   ["%s means %s × 10^%d." % (sf, digits[0] + ("." + digits[1:]
                                                               if len(digits) > 1 else ""), exp),
                    "= %s." % _fmt(value)])

    def t_to_standard_small():
        digits = _rand_digits(max(d, 1))
        exp = -random.randint(2, 5)
        sf, value = _sf_from_digits(digits, exp)
        return _wq("Write %s in standard form. %s" % (_fmt(value), FMT), sf,
                   ["Count how many places the point moves to sit after the first "
                    "digit (the power is negative for small numbers).",
                    "%s = %s." % (_fmt(value), sf)], "e.g. 4.2x10^-3")

    def t_to_ordinary_small():
        digits = _rand_digits(max(d, 1))
        exp = -random.randint(2, 4)
        sf, value = _sf_from_digits(digits, exp)
        return _numq("Write %s as an ordinary (decimal) number." % sf, _fmt(value),
                     ["10^%d means divide by 10 %d times, so move the decimal point %d places to the left."
                      % (exp, -exp, -exp), "%s = %s." % (sf, _fmt(value))])

    def t_compare():
        d1 = _rand_digits(d)
        d2 = _rand_digits(d)
        e1 = random.randint(3, 8)
        e2 = random.randint(3, 8)
        sf1, v1 = _sf_from_digits(d1, e1)
        sf2, v2 = _sf_from_digits(d2, e2)
        while v1 == v2:
            e2 = random.randint(3, 8)
            sf2, v2 = _sf_from_digits(d2, e2)
        bigger = sf1 if v1 > v2 else sf2
        return _wq("Which is larger, %s or %s? Type the larger one in standard form. %s"
                   % (sf1, sf2, FMT), bigger,
                   ["Compare the powers of ten first.",
                    "The larger is %s." % bigger], "e.g. 3.2x10^4")

    def t_compare_value():
        d1 = _rand_digits(d)
        d2 = _rand_digits(d)
        e1 = random.randint(3, 7)
        e2 = random.randint(3, 7)
        sf1, v1 = _sf_from_digits(d1, e1)
        sf2, v2 = _sf_from_digits(d2, e2)
        while v1 == v2:
            e2 = random.randint(3, 7)
            sf2, v2 = _sf_from_digits(d2, e2)
        return _tb("Which is larger, %s or %s? Type its value as an ordinary number."
                   % (sf1, sf2), _fmt(max(v1, v2)), "int", {},
                   ["%s = %s and %s = %s." % (sf1, _fmt(v1), sf2, _fmt(v2)),
                    "The larger is %s." % _fmt(max(v1, v2))])

    def t_symbol():
        d1 = _rand_digits(d)
        d2 = _rand_digits(d)
        e1 = random.randint(3, 8)
        e2 = random.randint(3, 8)
        sf1, v1 = _sf_from_digits(d1, e1)
        sf2, v2 = _sf_from_digits(d2, e2)
        while v1 == v2:
            e2 = random.randint(3, 8)
            sf2, v2 = _sf_from_digits(d2, e2)
        sym = "<" if v1 < v2 else ">"
        return _wq("Type < or > to compare these two numbers in standard form:"
                   "   %s ___ %s" % (sf1, sf2), sym,
                   ["%s = %s and %s = %s." % (sf1, _fmt(v1), sf2, _fmt(v2)),
                    "%s %s %s." % (sf1, sym, sf2)], "< or >")

    def t_context():
        digits = _rand_digits(d)
        exp = random.randint(6, 9)
        sf, value = _sf_from_digits(digits, exp)
        thing = pick(["the distance to a star in km", "the population of a country",
                      "the number of grains of sand on a beach"])
        return _wq("A scientist records %s as %s. Write this in standard form. %s"
                   % (thing, _fmt(value), FMT), sf,
                   ["%s = %s." % (_fmt(value), sf)], "e.g. 3.2x10^8")

    def t_table():
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            digits = _rand_digits(d)
            exp = random.randint(len(digits) - 1 + 1, 8)
            sf, value = _sf_from_digits(digits, exp)
            rows.append([_fmt(value), sf])
            if i == r_i:
                want, want_o = sf, _fmt(value)
        return _dt("Complete the table. Write the missing number in standard form "
                   "(like 3.2x10^4, no spaces).", ["Ordinary number", "Standard form"],
                   rows, want,
                   ["Move the point to just after the first digit.",
                    "%s = %s." % (want_o, want)], missing=[r_i, 1], atype="str")

    def t_convert():
        digits = _rand_digits(d)
        exp = random.randint(len(digits), 8)
        sf, value = _sf_from_digits(digits, exp)
        if random.random() < 0.5:
            return _wq("Convert this ordinary number to standard form:   %s. %s"
                       % (_fmt(value), FMT), sf,
                       ["Move the point to just after the first digit.",
                        "%s = %s." % (_fmt(value), sf)], "e.g. 3.2x10^4")
        return _tb("Convert this number from standard form to an ordinary number:"
                   "   %s" % sf, _fmt(value), "int", {},
                   ["%s means %s × 10^%d."
                    % (sf, digits[0] + ("." + digits[1:] if len(digits) > 1 else ""),
                       exp),
                    "%s = %s." % (sf, _fmt(value))])

    return _pick_t([t_to_standard_big, t_to_ordinary_big, t_to_standard_small,
                    t_to_ordinary_small, t_compare, t_compare_value, t_symbol,
                    t_context, t_convert], [t_table])
