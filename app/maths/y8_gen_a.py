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

    def _pair():
        a, b = _n(), _n()
        while a == b:
            b = _n()
        return a, b

    def _many(k):
        s = set()
        while len(s) < k:
            s.add(_n())
        xs = list(s)
        random.shuffle(xs)
        return xs

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
                   sym, ["%d %s %d." % (a, sym, b)], "< or >")

    def t_temp():
        cold = pick(_CITIES)
        ta, tb = _pair()
        return _tb("At dawn it was %d°C in %s and %d°C in another city. Which "
                   "temperature is colder? Type it." % (ta, cold, tb),
                   min(ta, tb), "int", {},
                   ["Colder means lower on the scale.",
                    "%d°C is colder than %d°C." % (min(ta, tb), max(ta, tb))])

    def t_warmer_diff():
        ta, tb = _pair()
        return _tb("The temperature rose from %d°C to %d°C. By how many degrees did "
                   "it rise?" % (min(ta, tb), max(ta, tb)), max(ta, tb) - min(ta, tb),
                   "int", {},
                   ["%d − (%d) = %d." % (max(ta, tb), min(ta, tb),
                                         max(ta, tb) - min(ta, tb))])

    def t_greatest():
        xs = _many({0: 4, 1: 5, 2: 5}[d])
        return _tb("Which of these is the greatest?   %s" % _lst(xs), max(xs), "int", {},
                   ["In order: %s." % _lst(sorted(xs)), "The greatest is %d." % max(xs)])

    def t_least():
        xs = _many({0: 4, 1: 5, 2: 5}[d])
        return _tb("Which of these is the least?   %s" % _lst(xs), min(xs), "int", {},
                   ["In order: %s." % _lst(sorted(xs)), "The least is %d." % min(xs)])

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
        a = _n()
        lo = ((a - 4) // 2) * 2 - 2
        return _nl("Place %d on the number line." % a, a, lo, lo + 20, 1, 5,
                   ["%d sits %d steps from %d." % (a, a - lo, lo)])

    def t_line_least():
        xs = sorted(_many(3))
        target = xs[0]
        lo = ((target - 3) // 5) * 5
        hi = lo + 25
        while hi < xs[-1] + 1:
            hi += 5
        return _nl("Here are three integers: %s. Place the SMALLEST one on the line."
                   % _lst(sorted(xs, key=lambda _z: random.random())),
                   target, lo, hi, 1, 5,
                   ["The smallest is %d." % target])

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
        while digit == 0:
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
                     ["Line up the decimal points and compare place by place.",
                      "%s is greater." % _fmt(max(a, b))])

    def t_smaller():
        a, b = _pair()
        return _numq("Which is smaller, %s or %s? Type the smaller number."
                     % (_fmt(a), _fmt(b)), _fmt(min(a, b)),
                     ["%s is smaller." % _fmt(min(a, b))])

    def t_symbol():
        a, b = _pair()
        sym = "<" if a < b else ">"
        return _wq("Type < or > to complete:   %s ___ %s" % (_fmt(a), _fmt(b)),
                   sym, ["%s %s %s." % (_fmt(a), sym, _fmt(b))], "< or >")

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
        vals = [_dec() for _ in range(4)]
        while len(set(vals)) < 4:
            vals = [_dec() for _ in range(4)]
        rows = [[t, _fmt(v)] for t, v in zip(towns, vals)]
        big = random.random() < 0.5
        want = max(vals) if big else min(vals)
        return _dt("The table shows race times (seconds). Whose time is the %s? Type "
                   "that time." % ("longest" if big else "shortest"),
                   ["Runner", "Time (s)"], rows, _fmt(want),
                   ["In order: %s." % _lst(_fmt(v) for v in sorted(vals)),
                    "The %s time is %s." % ("longest" if big else "shortest",
                                            _fmt(want))], atype="num")

    def t_line():
        whole = random.randint(1, 6)
        k = random.randint(1, 9)
        ans = Decimal(whole) + Decimal(k) / 10
        return _nl("Place %s on the number line." % _fmt(ans), ans,
                   whole, whole + 1, Decimal("0.1"), Decimal("0.5"),
                   ["%s is %d %s past %d." % (_fmt(ans), k, "tenth" if k == 1 else "tenths", whole)])

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
        x = _dec()
        dp = random.randint(1, 3 if d else 2)
        ans = _dround(x, dp)
        return _numq("Round %s to %d decimal place%s." % (_fmt(x), dp, "" if dp == 1 else "s"),
                     _fmt(ans),
                     ["Look at the digit in the next place along.",
                      "%s to %d d.p. is %s." % (_fmt(x), dp, _fmt(ans))])

    def t_nearest():
        x = _dec()
        ans = _dround(x, 0)
        return _numq("Round %s to the nearest whole number." % _fmt(x), _fmt(ans),
                     ["The first decimal digit decides.",
                      "%s rounds to %s." % (_fmt(x), _fmt(ans))])

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
                     % (_fmt(x), sig, "" if sig == 1 else "s"), _fmt(ans),
                     ["Count significant figures from the first non-zero digit.",
                      "%s to %d s.f. is %s." % (_fmt(x), sig, _fmt(ans))])

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
                      % (sig, "" if sig == 1 else "s"),
                      "%d to %d s.f. is %s." % (n, sig, _fmt(ans))])

    def t_money():
        p = random.randint(101, 9999)
        x = Decimal(p) / 100
        ans = _dround(x, 2)
        raw = Decimal(p) / 100 + Decimal(random.randint(1, 9)) / 1000
        ans = _dround(raw, 2)
        return _numq("A till shows £%s. Round this to 2 decimal places (the nearest "
                     "penny)." % _fmt(raw), _fmt(ans),
                     ["2 d.p. gives an exact number of pence.",
                      "£%s to 2 d.p. is £%s." % (_fmt(raw), _fmt(ans))], unit="£")

    def t_measure():
        x = Decimal(pick([n for n in range(100, 10000) if n % 10])) / 100     # always 2 d.p. to round
        who = pick(NAMES)
        ans = _dround(x, 1)
        return _numq("%s measures a plank as %s m. Round this length to 1 decimal "
                     "place." % (who, _fmt(x)), _fmt(ans),
                     ["%s m to 1 d.p. is %s m." % (_fmt(x), _fmt(ans))], unit="m")

    def t_which_rounds():
        base = Decimal(random.randint(1, 8)) + Decimal(random.randint(1, 8)) / 10
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
                     ["%s rounds to %s." % (_fmt(want), _fmt(base))])

    def t_yes_no():
        x = _dec()
        dp = random.randint(1, 2)
        real = _dround(x, dp)
        claim = real if random.random() < 0.5 else real + Decimal(1).scaleb(-dp)
        return _yn("%s says %s rounded to %d d.p. is %s. Is that correct? (yes/no)"
                   % (pick(NAMES), _fmt(x), dp, _fmt(claim)),
                   "yes" if claim == real else "no",
                   ["%s to %d d.p. is %s." % (_fmt(x), dp, _fmt(real))])

    def t_table():
        xs = sorted({_dec() for _ in range(4)})
        while len(xs) < 4:
            xs = sorted({_dec() for _ in range(4)})
        rows = [[_fmt(v), _fmt(_dround(v, 1))] for v in xs]
        r = random.randint(0, 3)
        return _dt("Complete the rounding table. What belongs in the empty cell "
                   "(rounded to 1 d.p.)?", ["Number", "To 1 d.p."], rows,
                   _fmt(_dround(xs[r], 1)),
                   ["%s to 1 d.p. is %s." % (_fmt(xs[r]), _fmt(_dround(xs[r], 1)))],
                   missing=[r, 1], atype="num")

    return _pick_t([t_dp, t_nearest, t_sf_small, t_sf_big, t_money, t_measure,
                    t_which_rounds, t_yes_no],
                   [t_table])


@skill("Y8.0.d", "Integers and decimals on number lines", S0)
def _(d=1):
    d = _d(d)

    def t_int_pos():
        lo = random.randint(0, 40)
        step = pick([1, 2])
        ans = lo + step * random.randint(1, 9)
        return _nl("Place %d on the number line." % ans, ans, lo, lo + step * 10,
                   step, step * 5, ["%d is %d %s of %d past %d."
                                    % (ans, (ans - lo) // step,
                                       "step" if ans - lo == step else "steps", step, lo)])

    def t_int_neg():
        span = pick([10, 20])
        ans = random.randint(-span, span)
        while ans == 0:
            ans = random.randint(-span, span)
        return _nl("Place %d on the number line." % ans, ans, -span, span, 1,
                   5, ["Count %s from zero." % ("left" if ans < 0 else "right")])

    def t_dec_tenths():
        whole = random.randint(0, 5)
        k = random.randint(1, 9)
        ans = Decimal(whole) + Decimal(k) / 10
        return _nl("Place %s on the number line." % _fmt(ans), ans, whole, whole + 1,
                   Decimal("0.1"), Decimal("0.5"),
                   ["%s is %d %s past %d." % (_fmt(ans), k, "tenth" if k == 1 else "tenths", whole)])

    def t_dec_neg():
        whole = -random.randint(1, 4)
        k = random.randint(1, 9)
        ans = Decimal(whole) - Decimal(k) / 10
        return _nl("Place %s on the number line." % _fmt(ans), ans, whole - 1, whole + 1,
                   Decimal("0.1"), Decimal("0.5"),
                   ["%s is between %d and %d." % (_fmt(ans), whole - 1, whole)])

    def t_between():
        lo = random.randint(-5, 5)
        a = lo + 2
        b = lo + 5
        ans = lo + 3 + random.randint(0, 1)
        return _nl("Place a whole number on the line that is greater than %d and less "
                   "than %d." % (a, b), ans, lo, lo + 8, 1, 4,
                   ["The whole numbers between %d and %d are %d and %d."
                    % (a, b, a + 1, b - 1),
                    "%d works." % ans])

    def t_rounded():
        x = Decimal(random.randint(1, 8)) + Decimal(random.randint(1, 9)) / 10
        ans = _dround(x, 0)
        lo = int(x) - 1
        return _nl("Round %s to the nearest whole number, then place your answer on "
                   "the line." % _fmt(x), ans, lo, lo + 4, 1, 1,
                   ["%s rounds to %s." % (_fmt(x), _fmt(ans))])

    def t_midpoint():
        step = pick([2, 4, 10])
        lo = random.randint(-2, 4) * step
        a = lo + step
        b = lo + 3 * step
        ans = (a + b) // 2
        return _nl("Place the number that is exactly halfway between %d and %d."
                   % (a, b), ans, lo, lo + 4 * step, step // 2, step,
                   ["Halfway between %d and %d is %d." % (a, b, ans)])

    def t_count_on():
        start = random.randint(-6, 6)
        step = pick([1, 2, 3])
        jumps = random.randint(2, 4)
        ans = start + step * jumps
        return _nl("Start at %d and count on %d jumps of %d. Place where you land."
                   % (start, jumps, step), ans, min(start, ans) - 2,
                   min(start, ans) - 2 + 12, 1, 5,
                   ["%d + %d × %d = %d." % (start, jumps, step, ans)])

    def t_temp_line():
        ans = random.randint(-8, 8)
        while ans == 0:
            ans = random.randint(-8, 8)
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
        return _nl("Graph the integer %d on the number line. On a VERTICAL number "
                   "line the positive integers go up from zero and the negative "
                   "integers go down below zero." % ans,
                   ans, -span, span, step, step * 5,
                   ["%d sits %d step%s %s zero."
                    % (ans, k, "" if k == 1 else "s",
                       "above" if ans > 0 else "below")])

    return _pick_t([t_int_pos], [t_int_neg, t_dec_tenths, t_dec_neg, t_between,
                                 t_rounded, t_midpoint, t_count_on, t_temp_line,
                                 t_graph_h, t_graph_v])


@skill("Y8.0.e", "Order and classify rational numbers", S0)
def _(d=1):
    d = _d(d)

    def _frac():
        den = pick([2, 4, 5, 8, 10, 20, 25])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        if random.random() < 0.4:
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
        other = dv + pick([Decimal("0.1"), Decimal("-0.1"), Decimal("0.15"),
                           Decimal("-0.2")])
        vals = [(dv, _fmt_frac(f)), (other, _fmt(other))]
        smaller = min(vals, key=lambda z: z[0])
        return _numq("Which is smaller, %s or %s? Type your answer as a decimal."
                     % (vals[0][1], vals[1][1]), _fmt(smaller[0]),
                     ["%s = %s." % (_fmt_frac(f), _fmt(dv)),
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
                      "The smallest is %s." % _fmt(min(vals))])

    def t_between():
        target = pick([Fraction(1, 4), Fraction(3, 8), Fraction(3, 5),
                       Fraction(7, 10)])
        dv = Decimal(target.numerator) / Decimal(target.denominator)
        lo = dv - Decimal("0.15")
        hi = dv + Decimal("0.15")
        others = [dv - Decimal("0.3"), dv + Decimal("0.3")]
        toks = [(_fmt_frac(target), dv)] + [("%s" % _fmt(o), o) for o in others]
        random.shuffle(toks)
        shown = _lst(t for t, _v in toks)
        return _numq("Which of these lies between %s and %s? Type it as a decimal."
                     "   %s" % (_fmt(lo), _fmt(hi), shown), _fmt(dv),
                     ["%s = %s, which is between %s and %s."
                      % (_fmt_frac(target), _fmt(dv), _fmt(lo), _fmt(hi))])

    def t_is_integer():
        num = random.randint(2, 9) * pick([2, 3, 4])
        den = pick([2, 3, 4])
        f = Fraction(num, den)
        return _yn("Is %s an integer? (yes/no)" % _fmt_frac(f),
                   "yes" if f.denominator == 1 else "no",
                   ["%s = %s." % (_fmt_frac(f), _fmt_frac(f)) if f.denominator != 1
                    else "%s = %d, a whole number." % ("%d/%d" % (num, den), num // den)])

    def t_terminating():
        den = pick([2, 3, 4, 5, 6, 8, 9, 11])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        return _yn("Does the fraction %s give a terminating decimal? (yes/no)"
                   % _fmt_frac(f), "yes" if _terminates(f) else "no",
                   ["A fraction terminates only if its denominator (in lowest terms) "
                    "has just 2s and 5s as prime factors.",
                    "%s is %s." % (_fmt_frac(f),
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
        if random.random() < 0.5:
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
        return {"prompt": "Find the multiplicative inverse (the reciprocal) of the "
                "fraction %d/%d. Give your answer as a fraction, like 5/2." % (a, b),
                "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 5/2"},
                "answer": "%d/%d" % (b, a), "answer_type": "frac", "tolerance": 0,
                "solution": ["To find the reciprocal, swap the numerator and "
                             "denominator.",
                             "The multiplicative inverse of %d/%d is %d/%d."
                             % (a, b, b, a)]}

    return _pick_t([t_frac_to_dec, t_compare, t_order_smallest, t_between,
                    t_is_integer, t_terminating, t_count_neg, t_nth_dec,
                    t_reciprocal], [])


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
        return Decimal(random.randint(-50, 50)) + Decimal(random.randint(0, 99)) / 100

    def _sym(a, b):
        return "<" if a < b else (">" if a > b else "=")

    def t_int_sym():
        a, b = _int(), _int()
        return _wq("Type <, > or = to compare:   %d ___ %d" % (a, b), _sym(a, b),
                   ["%d %s %d." % (a, _sym(a, b), b)], "< > or =")

    def t_dec_sym():
        a, b = _dec(), _dec()
        return _wq("Type <, > or = to compare:   %s ___ %s" % (_fmt(a), _fmt(b)),
                   _sym(a, b), ["%s %s %s." % (_fmt(a), _sym(a, b), _fmt(b))], "< > or =")

    def t_equal_case():
        f = Fraction(random.randint(1, 5), pick([2, 4, 5, 10]))
        dv = Decimal(f.numerator) / Decimal(f.denominator)
        if random.random() < 0.5:
            b = dv
        else:
            b = dv + pick([Decimal("0.1"), Decimal("-0.1")])
        return _wq("Type <, > or = to compare:   %s ___ %s" % (_fmt_frac(f), _fmt(b)),
                   _sym(dv, b),
                   ["%s = %s." % (_fmt_frac(f), _fmt(dv)),
                    "%s %s %s." % (_fmt(dv), _sym(dv, b), _fmt(b))], "< > or =")

    def t_neg_vs_pos():
        a = -random.randint(1, 30)
        b = random.randint(1, 30)
        if random.random() < 0.5:
            a, b = b, a
        return _wq("Type <, > or = to compare:   %d ___ %d" % (a, b), _sym(a, b),
                   ["A negative number is always less than a positive one.",
                    "%d %s %d." % (a, _sym(a, b), b)], "< > or =")

    def t_expr():
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)
        left = a + b
        right = random.randint(-16, 16)
        return _wq("Type <, > or = to compare:   %d + (%d) ___ %d" % (a, b, right),
                   _sym(left, right),
                   ["%d + (%d) = %d." % (a, b, left),
                    "%d %s %d." % (left, _sym(left, right), right)], "< > or =")

    def t_ineq_yes():
        op = pick(["<", ">"])
        value = random.randint(-4, 6)
        test = value + pick([-2, -1, 1, 2])
        sat = (test < value) if op == "<" else (test > value)
        return _ineq("The number line shows an inequality in x. Does x = %d satisfy "
                     "it? (yes/no)" % test, op, value, value - 6, value + 6,
                     "yes" if sat else "no",
                     ["The arrow shows x %s %d." % (op, value),
                      "%d %s %d is %s." % (test, op, value,
                                           "true" if sat else "false")])

    def t_ineq_read():
        op = pick(["<", ">", "<=", ">="])
        value = random.randint(-4, 6)
        disp = {"<": "<", ">": ">", "<=": "<=", ">=": ">="}[op]
        return _ineq("Read the inequality shown on the number line and type it (use x, "
                     "like x>3).", op, value, value - 6, value + 6,
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
        a, b = _dec(), _dec()
        return _dt("Type <, > or = for the empty cell to compare the two numbers.",
                   ["First", "Symbol", "Second"], [[_fmt(a), "?", _fmt(b)]],
                   _sym(a, b), ["%s %s %s." % (_fmt(a), _sym(a, b), _fmt(b))],
                   missing=[0, 1], atype="str")

    return _pick_t([t_int_sym, t_dec_sym, t_equal_case, t_neg_vs_pos, t_expr,
                    t_true_false],
                   [t_ineq_yes, t_ineq_read, t_table_sym])


@skill("Y8.0.g", "Priority of operations (BIDMAS)", S0)
def _(d=1):
    d = _d(d)

    def t_bracket_add():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        ans = a * (b + c)
        return _tb("Work out:   %d × (%d + %d)" % (a, b, c), ans, "int", {},
                   ["Brackets first: %d + %d = %d." % (b, c, b + c),
                    "%d × %d = %d." % (a, b + c, ans)])

    def t_mul_before_add():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 20)
        ans = c + a * b
        return _tb("Work out:   %d + %d × %d" % (c, a, b), ans, "int", {},
                   ["Multiply first: %d × %d = %d." % (a, b, a * b),
                    "%d + %d = %d." % (c, a * b, ans)])

    def t_index():
        a = random.randint(2, 5)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        ans = b + a ** 2 * (1 if d == 0 else 1)
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
        q = random.randint(2, 9)
        b = random.randint(2, 9)
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
        a = Decimal(random.randint(2, 9)) / 10 * 10          # keep tidy
        a = Decimal(random.randint(2, 9))
        b = Decimal(random.randint(2, 9)) / 10
        c = random.randint(2, 6)
        ans = a + b * c
        return _numq("Work out:   %s + %s × %d" % (_fmt(a), _fmt(b), c), _fmt(ans),
                     ["Multiply first: %s × %d = %s." % (_fmt(b), c, _fmt(b * c)),
                      "%s + %s = %s." % (_fmt(a), _fmt(b * c), _fmt(ans))])

    def t_missing_val():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(3, 20)
        total = a * b + c
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
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            c = random.randint(2, 12)
            rows.append(["%d + %d × %d" % (c, a, b), str(c + a * b)])
            if i == r_i:
                a0, b0, c0, want = a, b, c, c + a * b
        return _dt("Complete the table using BIDMAS. What value belongs in the empty "
                   "cell?", ["Calculation", "Answer"], rows, want,
                   ["Multiply before adding: %d × %d = %d." % (a0, b0, a0 * b0),
                    "%d + %d = %d." % (c0, a0 * b0, want)], missing=[r_i, 1])

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

    return _pick_t([t_bracket_add, t_mul_before_add, t_index, t_full, t_div_mix,
                    t_two_bracket, t_decimal, t_missing_val, t_insert_bracket,
                    t_compare, t_word, t_eval_dec], [t_table])


@skill("Y8.0.h", "Estimate to check a calculation", S0)
def _(d=1):
    d = _d(d)

    def t_product():
        a = random.randint(11, 89) * (10 if d else 1) + random.randint(0, 9)
        b = random.randint(11, 89)
        A, B = _r1sf(a), _r1sf(b)
        return _tb("Estimate %d × %d by rounding each number to 1 significant figure."
                   % (a, b), A * B, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d × %d = %d." % (A, B, A * B)])

    def t_sum():
        xs = [random.randint(110, 890) for _ in range(3)]
        est = sum(_r1sf(x) for x in xs)
        return _tb("Estimate %s by rounding each number to 1 significant figure."
                   % " + ".join(str(x) for x in xs), est, "int", {},
                   ["Rounded: %s." % " + ".join(str(_r1sf(x)) for x in xs),
                    "Estimate = %d." % est])

    def t_diff():
        a = random.randint(400, 900)
        b = random.randint(100, 350)
        A, B = _r1sf(a), _r1sf(b)
        return _tb("Estimate %d − %d by rounding each number to 1 significant figure."
                   % (a, b), A - B, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d − %d = %d." % (A, B, A - B)])

    def t_quotient():
        for _ in range(30):
            B = pick([2, 3, 4, 5, 6, 8]) * pick([1, 10])
            q = random.randint(2, 40)
            A = B * q
            if len(str(A)) <= 4 and _r1sf(A) == A:
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
        a = random.randint(21, 89)
        b = random.randint(21, 89)
        real = a * b
        A, B = _r1sf(a), _r1sf(b)
        est = A * B
        claim = real if random.random() < 0.5 else real + random.choice([-1, 1]) * random.randint(200, 900)
        return _yn("%s worked out %d × %d and got %d. Rounding each number to 1 s.f. "
                   "gives an estimate of %d. Is %d a reasonable answer? (yes/no)"
                   % (pick(NAMES), a, b, claim, est, claim),
                   "yes" if claim == real else "no",
                   ["Estimate: %d × %d = %d." % (A, B, est),
                    "The exact answer is %d, so %d is %s." % (real, claim,
                        "reasonable" if claim == real else "not reasonable")])

    def t_money():
        items = random.randint(3, 5)
        prices = [random.randint(180, 690) for _ in range(items)]
        est = sum(_r1sf(p) for p in prices)
        show = ", ".join("£%s" % _fmt(Decimal(p) / 100) for p in prices)
        return _tb("A shopper buys items priced %s (in pence: %s). Estimate the total "
                   "in PENCE by rounding each price to 1 significant figure."
                   % (show, ", ".join(str(p) for p in prices)), est, "int", {},
                   ["Rounded pence: %s." % " + ".join(str(_r1sf(p)) for p in prices),
                    "Estimate = %dp." % est])

    def t_which_est():
        a = random.randint(180, 620)
        b = random.randint(18, 62)
        A, B = _r1sf(a), _r1sf(b)
        good = A * B
        opts = [good, _r1sf(a) * b, a * B, good * 10]
        opts = list(dict.fromkeys(opts))
        while len(opts) < 4:
            opts.append(good + random.randint(1, 5) * 1000)
        show = opts[:]
        random.shuffle(show)
        return _tb("Round each number to 1 significant figure to estimate %d × %d. "
                   "Which of these is that estimate?   %s" % (a, b, _lst(show)),
                   good, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, A, b, B),
                    "%d × %d = %d." % (A, B, good)])

    def t_check_div():
        b = pick([19, 21, 29, 31, 39, 41])
        q = random.randint(15, 45)
        a = b * q + random.randint(0, b - 1)
        A, B = _r1sf(a), _r1sf(b)
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
            a = random.randint(21, 89)
            b = random.randint(21, 89)
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
            return Decimal(random.randint(lo, hi)) + Decimal(random.randint(0, 9)) / 10

        op = pick(["sum", "difference", "product"])
        if op == "sum":
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
        return _tb("What single digit goes in the box to make %d%d_ divisible by %d? "
                   "(smallest such digit)" % (a, b, k), need, "int", {},
                   ["The digit sum must be a multiple of %d." % k,
                    "%d + %d + %d = %d, a multiple of %d." % (a, b, need, a + b + need, k)])

    def t_rule_word():
        k = pick([2, 3, 4, 5, 9, 10])
        n = random.randint(100, 999)
        return _yn("You can test divisibility by %d using the rule: %s. Using this, is "
                   "%d divisible by %d? (yes/no)" % (k, RULES[k], n, k),
                   "yes" if n % k == 0 else "no",
                   ["%d ÷ %d %s exact." % (n, k, "is" if n % k == 0 else "is not")])

    def t_digit_sum():
        n = random.randint(100, 9999)
        ds = sum(int(c) for c in str(n))
        return _tb("What is the digit sum of %d? (This tests divisibility by 3 and 9.)"
                   % n, ds, "int", {},
                   ["Add the digits: %s = %d." % (" + ".join(str(n)), ds)])

    def t_by_six():
        n = random.randint(100, 999)
        return _yn("A number is divisible by 6 if it is divisible by both 2 and 3. Is "
                   "%d divisible by 6? (yes/no)" % n, "yes" if n % 6 == 0 else "no",
                   ["%d is %s and %s." % (n, "even" if n % 2 == 0 else "odd",
                                          "a multiple of 3" if n % 3 == 0
                                          else "not a multiple of 3"),
                    "So it %s divisible by 6." % ("is" if n % 6 == 0 else "is not")])

    def t_count():
        k = pick([2, 3, 5])
        xs = random.sample(range(20, 200), 6)
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
        k = random.randint(3, 12)
        i = random.randint(3, 9)
        return _tb("What is the %s multiple of %d?" % (ordinal(i), k), k * i, "int", {},
                   ["%d × %d = %d." % (k, i, k * i)])

    def t_is_factor():
        b = random.randint(2, 12)
        n = b * random.randint(2, 9) if random.random() < 0.5 else random.randint(20, 90)
        return _yn("Is %d a factor of %d? (yes/no)" % (b, n),
                   "yes" if n % b == 0 else "no",
                   ["%d ÷ %d %s exact." % (n, b, "is" if n % b == 0 else "is not")])

    def t_is_multiple():
        k = random.randint(3, 12)
        n = k * random.randint(2, 12) if random.random() < 0.5 else random.randint(20, 140)
        return _yn("Is %d a multiple of %d? (yes/no)" % (n, k),
                   "yes" if n % k == 0 else "no",
                   ["%d %s in the %d times table." % (n, "is" if n % k == 0 else "is not", k)])

    def t_common_factors():
        a = random.randint(12, 40)
        b = random.randint(12, 40)
        while b == a:
            b = random.randint(12, 40)
        common = sorted(set(_factors(a)) & set(_factors(b)))
        return _setq("Type all the common factors of %d and %d." % (a, b), common,
                     ["Common factors of %d and %d: %s." % (a, b, _lst(common))],
                     "e.g. 1, 2, 4")

    def t_count_factors():
        n = random.randint(12, 60)
        c = len(_factors(n))
        return _tb("How many factors does %d have?" % n, c, "int", {},
                   ["Factors of %d: %s." % (n, _lst(_factors(n))),
                    "That is %d factors." % c])

    def t_which_prime():
        pool = random.sample(range(2, 50), 5)
        primes = [x for x in pool if len(_factors(x)) == 2]
        if not primes:
            p = pick([x for x in (2, 3, 5, 7, 11, 13, 17, 19, 23) if x not in pool])
            pool[0] = p
            primes = [x for x in pool if len(_factors(x)) == 2]
        return _setq("Type all the prime numbers in this list:   %s" % _lst(pool),
                     primes, ["The primes are %s." % _lst(sorted(primes))],
                     "e.g. 2, 3, 5")

    def t_largest_factor():
        n = random.randint(20, 90)
        fs = _factors(n)
        second = fs[-2]
        return _tb("What is the largest factor of %d that is less than %d itself?"
                   % (n, n), second, "int", {},
                   ["Factors of %d: %s." % (n, _lst(fs)),
                    "The largest below %d is %d." % (n, second)])

    def t_table():
        ns = random.sample(range(12, 60), 3)
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
    FMT = "Use ^ for powers and x between factors, like 2^3x3x5 (no spaces)."

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
                   "form (like 2^3x3x5, no spaces).",
                   ["Number", "Prime factorisation"], rows, want,
                   ["%d = %s." % (ns[r_i], want)], missing=[r_i, 1], atype="str")

    return _pick_t([t_full, t_exponent, t_count_primes, t_distinct_primes,
                    t_from_factors_value, t_is_prime_power, t_missing_factor,
                    t_smallest_prime], [t_table])


@skill("Y8.1.d", "Highest common factor (HCF)", S1)
def _(d=1):
    d = _d(d)

    def _pair():
        g = random.randint(2, 12)
        a = g * random.randint(2, 9)
        b = g * random.randint(2, 9)
        while a == b:
            b = g * random.randint(2, 9)
        return a, b

    def t_two():
        a, b = _pair()
        h = math.gcd(a, b)
        return _tb("Find the highest common factor (HCF) of %d and %d." % (a, b), h,
                   "int", {},
                   ["List the factors and take the largest they share.",
                    "HCF(%d, %d) = %d." % (a, b, h)])

    def t_three():
        g = random.randint(2, 8)
        m1, m2, m3 = random.sample(range(2, 9), 3)
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
        h = random.randint(3, 9)
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
        h = random.randint(4, 10)
        a = h * random.randint(2, 6)
        b = h * random.randint(2, 6)
        return _tb("A packer has %d pens and %d pencils to share into identical bags "
                   "with no items left over. What is the greatest number of bags?"
                   % (a, b), math.gcd(a, b), "int", {},
                   ["The number of bags divides both %d and %d." % (a, b),
                    "Greatest = HCF = %d." % math.gcd(a, b)])

    def t_coprime():
        a = pick([8, 9, 15, 16, 25, 21, 35])
        b = pick([7, 11, 13, 17, 19])
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

    return _pick_t([t_two, t_three, t_from_pf, t_word_rows, t_word_bags, t_coprime,
                    t_check], [t_table])


@skill("Y8.1.e", "Lowest common multiple (LCM)", S1)
def _(d=1):
    d = _d(d)

    def _pair():
        a = random.randint(2, 9 if d == 0 else 12)
        b = random.randint(2, 9 if d == 0 else 12)
        while a == b:
            b = random.randint(2, 12)
        return a, b

    def t_two():
        a, b = _pair()
        return _tb("Find the lowest common multiple (LCM) of %d and %d." % (a, b),
                   _lcm(a, b), "int", {},
                   ["List multiples of each and find the first they share.",
                    "LCM(%d, %d) = %d." % (a, b, _lcm(a, b))])

    def t_three():
        a, b, c = random.sample(range(2, 8), 3)
        l = _lcm(_lcm(a, b), c)
        return _tb("Find the LCM of %d, %d and %d." % (a, b, c), l, "int", {},
                   ["LCM(%d, %d, %d) = %d." % (a, b, c, l)])

    def t_from_pf():
        a, b = random.randint(6, 20), random.randint(6, 20)
        while a == b:
            b = random.randint(6, 20)
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
        a, b = random.randint(3, 9), random.randint(3, 9)
        while a == b:
            b = random.randint(3, 9)
        return _tb("Two runners start together. One completes a lap every %d minutes, "
                   "the other every %d minutes. After how many minutes are they next at "
                   "the start line together?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d minutes." % (a, b, _lcm(a, b))])

    def t_nth_common():
        a, b = _pair()
        l = _lcm(a, b)
        i = random.randint(2, 3)
        return _tb("The lowest common multiple of %d and %d is %d. What is their "
                   "%s common multiple?" % (a, b, l, ordinal(i)),
                   l * i, "int", {},
                   ["Common multiples are multiples of the LCM %d." % l,
                    "The %s is %d × %d = %d." % (ordinal(i), i, l, i * l)])

    def t_check():
        a, b = _pair()
        l = _lcm(a, b)
        claim = l if random.random() < 0.5 else l + a
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

    def t_bells():
        a = random.randint(4, 12)
        b = random.randint(4, 12)
        while a == b:
            b = random.randint(4, 12)
        return _tb("At a station, one train departs every %d minutes and another every "
                   "%d minutes. They leave together at 09:00. After how many minutes do "
                   "they next leave together?" % (a, b), _lcm(a, b), "int", {},
                   ["This is the LCM of %d and %d." % (a, b),
                    "LCM = %d minutes." % _lcm(a, b)])

    def t_slabs():
        h = random.randint(3, 9)
        a = h * random.randint(3, 8)
        b = h * random.randint(3, 8)
        return _tb("A rectangular floor is %d cm by %d cm. It is to be tiled with "
                   "identical square tiles, using whole tiles only. What is the largest "
                   "side length (in cm) each square tile can have?" % (a, b),
                   math.gcd(a, b), "int", {},
                   ["The tile side must divide both %d and %d." % (a, b),
                    "Largest = HCF = %d cm." % math.gcd(a, b)])

    def t_hampers():
        h = random.randint(4, 10)
        a = h * random.randint(2, 6)
        b = h * random.randint(2, 6)
        c = h * random.randint(2, 6)
        g = math.gcd(math.gcd(a, b), c)
        return _tb("A shop makes identical hampers using all of %d apples, %d oranges "
                   "and %d pears, with nothing left over. What is the greatest number "
                   "of hampers?" % (a, b, c), g, "int", {},
                   ["The number of hampers divides all three amounts.",
                    "Greatest = HCF = %d." % g])

    def t_lighthouse():
        a = pick([6, 8, 9, 10, 12])
        b = pick([4, 5, 6, 15])
        while a == b:
            b = pick([4, 5, 6, 15])
        return _tb("Two lighthouses flash: one every %d seconds, the other every %d "
                   "seconds. They flash together now. After how many seconds do they "
                   "next flash together?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d seconds." % (a, b, _lcm(a, b))])

    def t_ribbon():
        h = random.randint(4, 12)
        a = h * random.randint(3, 8)
        b = h * random.randint(3, 8)
        return _tb("Two ribbons of length %d cm and %d cm are cut into equal pieces as "
                   "long as possible, with none wasted. How long (in cm) is each piece?"
                   % (a, b), math.gcd(a, b), "int", {},
                   ["The piece length divides both %d and %d." % (a, b),
                    "Longest = HCF = %d cm." % math.gcd(a, b)])

    def t_buses():
        a = pick([12, 15, 18, 20, 24])
        b = pick([10, 15, 20, 25, 30])
        while a == b:
            b = pick([10, 15, 20, 25, 30])
        return _tb("Bus A comes every %d minutes and bus B every %d minutes. Both are "
                   "at the stop at 08:00. At how many minutes past 08:00 are they both "
                   "at the stop together again?" % (a, b), _lcm(a, b), "int", {},
                   ["LCM(%d, %d) = %d minutes." % (a, b, _lcm(a, b))])

    def t_which_op():
        h = random.randint(4, 9)
        a = h * random.randint(3, 6)
        b = h * random.randint(3, 6)
        return _wq("To pack %d red and %d blue pens into identical boxes (single colour "
                   "per box) with the greatest box size, do you need the HCF or the "
                   "LCM? (type 'HCF' or 'LCM')" % (a, b), "HCF",
                   ["'Greatest identical size' means the highest common factor.",
                    "You need the HCF."], "HCF or LCM")

    def t_greatest_people():
        h = random.randint(5, 12)
        a = h * random.randint(2, 6)
        b = h * random.randint(2, 6)
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
        return random.randint(2, 6), random.randint(2, 4)

    def t_eval():
        b, e = _base_exp()
        return _tb("Work out %d^%d. (^ means 'to the power of')" % (b, e), b ** e,
                   "int", {},
                   ["%d^%d = %s = %d." % (b, e, " × ".join([str(b)] * e), b ** e)])

    def t_square():
        b = random.randint(2, 15 if d else 10)
        return _tb("What is %d squared (%d^2)?" % (b, b), b * b, "int", {},
                   ["%d^2 = %d × %d = %d." % (b, b, b, b * b)])

    def t_cube():
        b = random.randint(2, 8 if d else 5)
        return _tb("What is %d cubed (%d^3)?" % (b, b), b ** 3, "int", {},
                   ["%d^3 = %d × %d × %d = %d." % (b, b, b, b, b ** 3)])

    def t_missing_exp():
        b = random.randint(2, 5)
        e = random.randint(2, 4)
        return _tb("Solve for the power:   %d^? = %d" % (b, b ** e), e, "int", {},
                   ["%d^%d = %d." % (b, e, b ** e),
                    "So the power is %d." % e])

    def t_missing_base():
        b = random.randint(2, 9)
        e = pick([2, 3])
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
        e = random.randint(2, 6)
        return _tb("Work out 10^%d." % e, 10 ** e, "int", {},
                   ["10^%d is 1 followed by %d zeros = %d." % (e, e, 10 ** e)])

    def t_word():
        who = pick(NAMES)
        b = random.randint(2, 4)
        e = random.randint(3, 5)
        return _tb("%s folds a piece of paper in half %d times. The number of layers is "
                   "2^%d. How many layers is that?" % (who, e, e), 2 ** e, "int", {},
                   ["2^%d = %d." % (e, 2 ** e)])

    def t_between():
        b = pick([2, 3])
        e = random.randint(3, 5)
        val = b ** e
        return _tb("2 to some power equals %d (2^? = %d). What is the power?"
                   % (2 ** e, 2 ** e), e, "int", {},
                   ["2^%d = %d." % (e, 2 ** e)])

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
        b = random.randint(2, 5)
        e = random.randint(2, 3)
        p = b ** e
        forms = []
        c = random.randint(2, 12)
        forms.append(("%d + %d^%d" % (c, b, e), c + p,
                      "%d^%d = %d, then %d + %d = %d." % (b, e, p, c, p, c + p)))
        forms.append(("%d × %d^%d" % (c, b, e), c * p,
                      "%d^%d = %d, then %d × %d = %d." % (b, e, p, c, p, c * p)))
        c2 = random.randint(2, p - 1)
        forms.append(("%d^%d − %d" % (b, e, c2), p - c2,
                      "%d^%d = %d, then %d − %d = %d." % (b, e, p, p, c2, p - c2)))
        b2 = random.randint(2, 4)
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
        b = random.randint(2, 9)
        e = pick([2, 4] if d else [2])
        val = (-b) ** e
        return _tb("Work out (−%d)^%d." % (b, e), val, "int", {},
                   ["A negative number to an even power is positive.",
                    "(−%d)^%d = %d." % (b, e, val)])

    def t_neg_odd():
        b = random.randint(2, 9)
        e = pick([3, 5] if d else [3])
        val = (-b) ** e
        return _tb("Work out (−%d)^%d." % (b, e), val, "int", {},
                   ["A negative number to an odd power stays negative.",
                    "(−%d)^%d = %d." % (b, e, val)])

    def t_sign_only():
        b = random.randint(2, 9)
        e = random.randint(2, 6)
        pos = e % 2 == 0
        return _wq("Is (−%d)^%d positive or negative? (type 'positive' or 'negative')"
                   % (b, e), "positive" if pos else "negative",
                   ["An %s power of a negative number is %s."
                    % ("even" if pos else "odd", "positive" if pos else "negative")])

    def t_dec_square():
        t = random.randint(1, 9)
        base = Decimal(t) / 10
        val = base * base
        return _numq("Work out %s^2." % _fmt(base), _fmt(val),
                     ["%s × %s = %s." % (_fmt(base), _fmt(base), _fmt(val))])

    def t_dec_cube():
        t = pick([2, 3, 4, 5])
        base = Decimal(t) / 10
        val = base ** 3
        return _numq("Work out %s^3." % _fmt(base), _fmt(val),
                     ["%s × %s × %s = %s." % (_fmt(base), _fmt(base), _fmt(base),
                                              _fmt(val))])

    def t_half_power():
        base = Decimal("0.5")
        e = pick([2, 3, 4])
        val = base ** e
        return _numq("Work out %s^%d." % (_fmt(base), e), _fmt(val),
                     ["%s^%d = %s." % (_fmt(base), e, _fmt(val))])

    def t_neg_dec():
        t = random.randint(1, 9)
        base = Decimal(t) / 10
        e = pick([2, 3])
        val = (-base) ** e
        return _numq("Work out (−%s)^%d." % (_fmt(base), e), _fmt(val),
                     ["(−%s)^%d = %s (%s power)." % (_fmt(base), e, _fmt(val),
                                                     "even" if e % 2 == 0 else "odd")])

    def t_compare_sign():
        b = random.randint(2, 6)
        a1 = (-b) ** 2
        a2 = (-b) ** 3
        return _tb("Which is greater, (−%d)^2 or (−%d)^3? Type its value." % (b, b),
                   max(a1, a2), "int", {},
                   ["(−%d)^2 = %d and (−%d)^3 = %d." % (b, a1, b, a2),
                    "The greater value is %d." % max(a1, a2)])

    return _pick_t([t_neg_even, t_neg_odd, t_sign_only, t_dec_square, t_dec_cube,
                    t_half_power, t_neg_dec, t_compare_sign], [])


@skill("Y8.1.i", "Laws of indices", S1)
def _(d=1):
    d = _d(d)

    def t_multiply_exp():
        b = random.randint(2, 6)
        m = random.randint(2, 6)
        n = random.randint(2, 6)
        return _tb("Using the laws of indices, %d^%d × %d^%d = %d^?. What is the missing "
                   "power?" % (b, m, b, n, b), m + n, "int", {},
                   ["Add the powers: %d + %d = %d." % (m, n, m + n),
                    "%d^%d × %d^%d = %d^%d." % (b, m, b, n, b, m + n)])

    def t_divide_exp():
        b = random.randint(2, 6)
        m = random.randint(4, 9)
        n = random.randint(1, m - 1)
        return _tb("Using the laws of indices, %d^%d ÷ %d^%d = %d^?. What is the missing "
                   "power?" % (b, m, b, n, b), m - n, "int", {},
                   ["Subtract the powers: %d − %d = %d." % (m, n, m - n),
                    "%d^%d ÷ %d^%d = %d^%d." % (b, m, b, n, b, m - n)])

    def t_power_of_power():
        b = random.randint(2, 5)
        m = random.randint(2, 4)
        n = random.randint(2, 4)
        return _tb("Using the laws of indices, (%d^%d)^%d = %d^?. What is the missing "
                   "power?" % (b, m, n, b), m * n, "int", {},
                   ["Multiply the powers: %d × %d = %d." % (m, n, m * n),
                    "(%d^%d)^%d = %d^%d." % (b, m, n, b, m * n)])

    def t_single_power():
        b = random.randint(2, 6)
        m = random.randint(2, 5)
        n = random.randint(2, 5)
        return _wq("Write %d^%d × %d^%d as a single power. Use ^ , like %d^7 (no "
                   "spaces)." % (b, m, b, n, b), "%d^%d" % (b, m + n),
                   ["Add the powers: %d + %d = %d." % (m, n, m + n),
                    "= %d^%d." % (b, m + n)], "e.g. %d^7" % b)

    def t_solve_index():
        b = pick([2, 3, 5])
        e = random.randint(2, 5)
        return _tb("Solve for x:   %d^x = %d" % (b, b ** e), e, "int", {},
                   ["%d^%d = %d." % (b, e, b ** e), "So x = %d." % e])

    def t_solve_from_law():
        b = random.randint(2, 5)
        m = random.randint(2, 4)
        target = m + random.randint(1, 3)
        n = target - m
        return _tb("Solve for x:   %d^%d × %d^x = %d^%d" % (b, m, b, b, target), n,
                   "int", {},
                   ["The powers on the left add to %d, so %d + x = %d." % (target, m, target),
                    "x = %d." % n])

    def t_evaluate_after():
        b = random.randint(2, 4)
        m = random.randint(1, 3)
        n = random.randint(1, 3)
        return _tb("Simplify then evaluate:   %d^%d × %d^%d" % (b, m, b, n),
                   b ** (m + n), "int", {},
                   ["= %d^%d = %d." % (b, m + n, b ** (m + n))])

    def t_divide_value():
        b = random.randint(2, 4)
        m = random.randint(4, 6)
        n = random.randint(1, 3)
        return _tb("Simplify then evaluate:   %d^%d ÷ %d^%d" % (b, m, b, n),
                   b ** (m - n), "int", {},
                   ["= %d^%d = %d." % (b, m - n, b ** (m - n))])

    def t_table():
        b = random.randint(2, 6)
        rows = []
        want = None
        r_i = random.randint(0, 2)
        for i in range(3):
            m = random.randint(2, 5)
            n = random.randint(2, 5)
            rows.append(["%d^%d × %d^%d" % (b, m, b, n), "%d^%d" % (b, m + n)])
            if i == r_i:
                m0, n0, want = m, n, "%d^%d" % (b, m + n)
        return _dt("Complete the table by writing each product as a single power (like "
                   "%d^7, no spaces). What belongs in the empty cell?" % b,
                   ["Product", "Single power"], rows, want,
                   ["Add the powers: %d + %d = %d." % (m0, n0, m0 + n0),
                    "= %s." % want], missing=[r_i, 1], atype="str")

    def t_solve_var_index():
        b = pick([2, 3, 5, 10])
        e = random.randint(2, 5)
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
        r = random.randint(2, 15 if d else 10)
        return _tb("Work out √%d." % (r * r), r, "int", {},
                   ["%d × %d = %d, so √%d = %d." % (r, r, r * r, r * r, r)])

    def t_cbrt():
        r = random.randint(2, 8 if d else 5)
        return _tb("Work out the cube root of %d (∛%d)." % (r ** 3, r ** 3), r, "int", {},
                   ["%d × %d × %d = %d, so ∛%d = %d." % (r, r, r, r ** 3, r ** 3, r)])

    def t_solve_sq():
        r = random.randint(2, 12)
        return _tb("Solve for the positive value of x:   x^2 = %d" % (r * r), r,
                   "int", {}, ["x = √%d = %d." % (r * r, r)])

    def t_solve_cube():
        r = random.randint(2, 7)
        return _tb("Solve for x:   x^3 = %d" % (r ** 3), r, "int", {},
                   ["x = ∛%d = %d." % (r ** 3, r)])

    def t_estimate_nearest():
        r = random.randint(3, 12)
        n = r * r + random.randint(1, 2 * r)          # not a perfect square
        k = math.isqrt(n)
        nearest = k + 1 if 4 * n > (2 * k + 1) ** 2 else k
        return _tb("Estimate √%d to the nearest whole number." % n, nearest, "int", {},
                   ["%d^2 = %d and %d^2 = %d." % (k, k * k, k + 1, (k + 1) ** 2),
                    "√%d is closest to %d." % (n, nearest)])

    def t_between_lower():
        r = random.randint(3, 12)
        n = r * r + random.randint(1, 2 * r)
        k = math.isqrt(n)
        return _tb("√%d lies between two consecutive whole numbers. Type the smaller "
                   "one." % n, k, "int", {},
                   ["%d^2 = %d and %d^2 = %d, so √%d is between %d and %d."
                    % (k, k * k, k + 1, (k + 1) ** 2, n, k, k + 1),
                    "The smaller is %d." % k])

    def t_area():
        r = random.randint(4, 15)
        return _tb("A square has area %d cm². What is the length of one side (in cm)?"
                   % (r * r), r, "int", {},
                   ["Side = √area = √%d = %d cm." % (r * r, r)])

    def t_volume():
        r = random.randint(2, 8)
        return _tb("A cube has volume %d cm³. What is the length of one edge (in cm)?"
                   % (r ** 3), r, "int", {},
                   ["Edge = ∛volume = ∛%d = %d cm." % (r ** 3, r)])

    def t_which_between():
        n = pick([2, 3, 5, 7, 10, 15, 20, 27, 40, 50, 60])
        k = math.isqrt(n)
        return _tb("Between which two consecutive whole numbers does √%d lie? Type the "
                   "larger one." % n, k + 1, "int", {},
                   ["%d^2 = %d and %d^2 = %d." % (k, k * k, k + 1, (k + 1) ** 2),
                    "The larger is %d." % (k + 1)])

    def t_table():
        rs = random.sample(range(2, 15), 3)
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
                     ["%s = %s." % (sf, _fmt(value))])

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
