# Year 9 generators (added 2 Nov 2026 to widen the bank): strands 9.0–9.3, the KS3 statements the
# first Year 9 bank left out.
#
# Error intervals (a ≤ x < b) from rounding and truncation, and the error in an estimate; exact
# calculation with fractions, surds and multiples of π.  Expanding several brackets and factorising
# with an algebraic common factor; identities, equations and testing statements.  Forming and solving
# equations from angles, shapes and words.  Recognising linear, quadratic, cubic and reciprocal graphs;
# parallel lines from y = mx + c; approximate solutions read from graphs, including simultaneous
# equations.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403
from .y9_gen_a import S0, S1, _g, _poly
from .y9_gen_b import S2, S3, _line, _poly_txt, _t


def _set(prompt, values, solution, placeholder):
    """Several numbers in any order, e.g. both solutions of a quadratic."""
    return {"prompt": prompt, "component": "number", "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in values), "answer_type": "set", "solution": solution}


def _sx(k, var="x"):
    """3x, x, -x, -3x with ASCII minus, for typed algebra answers."""
    return var if k == 1 else ("-" + var) if k == -1 else "%d%s" % (k, var)


def _lin(a, b, var="x"):
    """ax+b as compact typed text: 5x-4, x+16, -2x."""
    s = _sx(a, var) if a else ""
    if b:
        s += ("+" if b > 0 and s else "") + str(b)
    return s or "0"


# ================================================================== 9.0 ======
_MEASURES = [("A pencil is %s cm long", "cm"), ("A parcel has a mass of %s kg", "kg"), ("A race took %s seconds", "seconds"),
             ("A jug holds %s litres", "litres"), ("A rope is %s m long", "m")]


@skill("Y9.0.e", "Error intervals and bounds", S0)
def _(d=1):
    d = _d(d)
    text, unit = pick(_MEASURES)

    def t_whole():
        v = random.randint(5, 95)
        lo_or_hi = pick(["lower", "upper"])
        ans = Decimal(v) + (Decimal("-0.5") if lo_or_hi == "lower" else Decimal("0.5"))
        return _tb((text % v) + ", to the nearest whole number. What is the %s bound?" % lo_or_hi,
                   _ds(ans), "num", {"unit": unit}, ["Half a unit either side: %s ≤ x < %s." % (_ds(Decimal(v) - Decimal("0.5")), _ds(Decimal(v) + Decimal("0.5")))])

    def t_ten():
        step = pick(_by(d, [10], [10, 100], [100, 1000]))
        v = random.randint(3, 60) * step
        return _tb("A crowd is %s people, to the nearest %d. What is the smallest number of people there could be?" % (_c(v), step),
                   v - step // 2, "int", {}, ["Half of %d is %d: %s − %d = %s." % (step, step // 2, _c(v), step // 2, _c(v - step // 2))])

    def t_dp():
        # hard: 2 decimal places (half of 0.01 is 0.005); the last digit is never 0 so the 2 dp shows
        dp = _by(d, 1, 1, 2)
        v = Decimal(random.randint(11, 99)) / 10 if dp == 1 else Decimal(random.choice([k for k in range(101, 1000) if k % 10])) / 100
        h = Decimal("0.05") if dp == 1 else Decimal("0.005")
        hi = random.random() < 0.5
        return _tb("x = %s, correct to %d decimal place%s. What is the %s bound of x?" % (format(v.quantize(Decimal(10) ** -dp), "f"), dp, "" if dp == 1 else "s", "upper" if hi else "lower"),
                   _ds(v + h if hi else v - h), "num", {},
                   ["%s ≤ x < %s." % (_ds(v - h), _ds(v + h))])

    def t_sf():
        v = pick([k for k in range(11, 100) if k % 10]) * 100     # never 8,000: a round thousand reads oddly at 2 s.f.
        return _tb("A town's population is %s, correct to 2 significant figures. What is the lower bound?" % _c(v), v - 50, "int", {},
                   ["The second significant figure is the hundreds, so ±50.", "%s ≤ P < %s." % (_c(v - 50), _c(v + 50))])

    def t_interval():
        step = pick([5, 10, 2])
        v = random.randint(3, 30) * step
        lo, hi = Fraction(v) - Fraction(step, 2), Fraction(v) + Fraction(step, 2)
        return _set("%s is %d, rounded to the nearest %d. Type the lower and upper bounds of the error interval, like 22.5, 27.5." % (
                    pick(["A length in mm", "A mass in grams", "A distance in km"]), v, step), [_ds(lo), _ds(hi)],
                    ["%s ≤ x < %s." % (_ds(lo), _ds(hi))], "e.g. 22.5, 27.5")

    def t_truncate():
        v = Decimal(random.randint(11, 99)) / 10
        return _tb("A number x is TRUNCATED (cut off, not rounded) to 1 decimal place, giving %s. What is the upper bound of x?" % format(v.quantize(Decimal("0.1")), "f"),
                   _ds(v + Decimal("0.1")), "num", {}, ["Truncating means %s ≤ x < %s." % (_ds(v), _ds(v + Decimal("0.1")))])

    def t_could_be():
        v = random.randint(20, 90)
        edge, ok = pick([(Decimal(v) + Decimal("0.5"), "no"), (Decimal(v) - Decimal("0.5"), "yes"), (Decimal(v) + Decimal("0.49"), "yes"),
                         (Decimal(v) - Decimal("0.51"), "no")])
        return _wq("A bag's mass is %d kg to the nearest kg. Could its true mass be %s kg? (yes or no)" % (v, _ds(edge)), ok,
                   ["The error interval is %s ≤ m < %s." % (_ds(Decimal(v) - Decimal("0.5")), _ds(Decimal(v) + Decimal("0.5")))], "yes / no")

    def t_max_total():
        n, v = random.randint(3, 9), random.randint(5, 25)
        return _tb("Each of %d boxes weighs %d kg, to the nearest kg. What is the upper bound of their total mass, in kg?" % (n, v),
                   _ds(n * (Decimal(v) + Decimal("0.5"))), "num", {"unit": "kg"},
                   ["Upper bound of one box: %s kg." % _ds(Decimal(v) + Decimal("0.5")), "%d × %s = %s." % (n, _ds(Decimal(v) + Decimal("0.5")), _ds(n * (Decimal(v) + Decimal("0.5"))))])

    def t_min_perimeter():
        a, b = random.randint(3, 20), random.randint(3, 20)
        lo = 2 * (Decimal(a) - Decimal("0.5")) + 2 * (Decimal(b) - Decimal("0.5"))
        return _tb("A rectangle measures %d cm by %d cm, each to the nearest cm. What is the lower bound of its perimeter, in cm?" % (a, b),
                   _ds(lo), "num", {"unit": "cm"}, ["Use the lower bounds %s and %s." % (_ds(Decimal(a) - Decimal("0.5")), _ds(Decimal(b) - Decimal("0.5"))),
                                                     "2 × %s + 2 × %s = %s." % (_ds(Decimal(a) - Decimal("0.5")), _ds(Decimal(b) - Decimal("0.5")), _ds(lo))])

    def t_estimate_error():
        x = Decimal(random.randint(41, 59)) + Decimal(random.randint(1, 9)) / 10
        y = Decimal(random.randint(2, 4)) + Decimal(random.randint(1, 9)) / 10
        ex = Decimal(int(round(x, -1)))
        ey = Decimal(int(y + Decimal("0.5")))
        est, exact = ex * ey, x * y
        return _tb("Estimate %s × %s by rounding each number to 1 significant figure. How far is the estimate from the exact answer? (a positive "
                   "number)" % (_ds(x), _ds(y)), _ds(abs(est - exact)), "num", {},
                   ["Estimate %s × %s = %s." % (_ds(ex), _ds(ey), _ds(est)), "Exact %s.  Difference %s." % (_ds(exact), _ds(abs(est - exact)))])

    def t_line():
        v = Decimal(random.randint(41, 58)) / 10
        return _nld("y = %s to 1 decimal place. Mark the LOWER bound of y on the number line." % format(v.quantize(Decimal("0.1")), "f"), v - Decimal("0.05"),
                    v - Decimal("0.3"), v + Decimal("0.2"), 0.05, 0.1, ["Lower bound = %s − 0.05 = %s." % (_ds(v), _ds(v - Decimal("0.05")))])

    # easy: one bound of a single rounded value; hard: s.f., truncation, bounds of totals and estimates
    return _pick_t(_by(d, [t_whole, t_ten, t_dp, t_interval, t_could_be],
                       [t_whole, t_ten, t_dp, t_sf, t_interval, t_truncate, t_could_be, t_max_total, t_min_perimeter, t_estimate_error],
                       [t_dp, t_sf, t_interval, t_truncate, t_could_be, t_max_total, t_min_perimeter, t_estimate_error]), [t_line])


@skill("Y9.0.f", "Exact calculation with fractions, surds and π", S0)
def _(d=1):
    d = _d(d)

    def t_add():
        # easy: one denominator is a multiple of the other (2, 4 -> 8)
        a, b = Fraction(random.randint(1, 5), pick(_by(d, [2, 4], [3, 4, 6], [3, 4, 6]))), Fraction(random.randint(1, 7), pick(_by(d, [8], [8, 9, 12], [8, 9, 12])))
        return _fq("Work out %s + %s exactly. Give a fraction or mixed number in its simplest form." % (_fs(a), _fs(b)), a + b,
                   ["Common denominator: %s." % _mixed(a + b)], "e.g. 1 5/12")

    def t_mult_mixed():
        a, b = Fraction(random.randint(5, 11), 4), Fraction(random.randint(4, 11), 3)
        return _fq("Work out %s × %s exactly." % (_mixed(a), _mixed(b)), a * b,
                   ["As improper fractions: %s × %s = %s = %s." % (_fs(a), _fs(b), _fs(a * b), _mixed(a * b))], "e.g. 3 1/2")

    def t_divide():
        a, b = Fraction(random.randint(1, 8), pick([3, 5, 9])), Fraction(pick([1, 3, 5]), pick([2, 4]))
        return _fq("Work out %s ÷ %s exactly." % (_fs(a), _fs(b)), a / b, ["Multiply by the reciprocal %s: %s." % (_fs(1 / b), _fs(a / b))])

    def t_neg():
        a, b = Fraction(random.randint(1, 4), 5), Fraction(random.randint(3, 7), 4)
        return _fq("Work out %s − %s exactly." % (_fs(a), _fs(b)), a - b, ["%s − %s = %s." % (_fs(a), _fs(b), _fs(a - b))], "e.g. -3/4")

    def t_semi_area():
        r = random.randint(1, 8) * 2
        return _tb("A semicircle has radius %d cm. Its exact area is kπ cm². What is k?" % r, r * r // 2, "int", {}, ["½ × π × %d² = %dπ." % (r, r * r // 2)])

    def t_semi_perim():
        dd = random.randint(2, 12) * 2
        which = pick(["a", "b"])
        return _tb("A semicircle has diameter %d cm. Its exact perimeter is (aπ + b) cm. What is %s?" % (dd, which),
                   dd // 2 if which == "a" else dd, "int", {}, ["Curved part ½ × π × %d = %dπ; straight edge %d." % (dd, dd // 2, dd)])

    def t_quarter():
        r = random.randint(1, 6) * 2
        return _tb("A quarter circle has radius %d cm. Its exact area is kπ cm². What is k?" % r, r * r // 4, "int", {}, ["¼ × π × %d² = %sπ." % (r, "" if r * r // 4 == 1 else r * r // 4)])

    def t_surd_square():
        k = random.randint(2, 30)
        return _tb("A square has sides of √%d cm. What is its exact area, in cm²?" % k, k, "int", {"unit": "cm²"}, ["√%d × √%d = %d." % (k, k, k)])

    def t_surd_rect():
        r, a, b = pick([2, 3, 5]), random.randint(1, _by(d, 3, 3, 5)), random.randint(2, _by(d, 4, 4, 6))
        return _tb("A rectangle is √%d cm by √%d cm. What is its exact area, in cm²?" % (a * a * r, b * b * r), a * b * r, "int", {"unit": "cm²"},
                   ["√%d = %s√%d and √%d = %d√%d." % (a * a * r, "" if a == 1 else a, r, b * b * r, b, r), "Product = %d × %d = %d." % (a * b, r, a * b * r)])

    def t_exact_or_not():
        if random.random() < 0.5:
            k = random.choice([v for v in range(11, 40) if v % 10])
            sq = Fraction(k * k, 100)
            return _wq("Is %s an exact value of √%s? (yes or no)" % (_ds(Fraction(k, 10)), _ds(sq)), "yes",
                       ["%s × %s = %s exactly." % (_ds(Fraction(k, 10)), _ds(Fraction(k, 10)), _ds(sq))], "yes / no")
        n = random.choice([x for x in range(2, 80) if int(x ** 0.5) ** 2 != x])
        return _wq("Is %s an exact value of √%d? (yes or no)" % (_ds(round(Decimal(n).sqrt(), 2)), n), "no",
                   ["√%d is irrational: its decimal never ends, so %s is only an approximation." % (n, _ds(round(Decimal(n).sqrt(), 2)))], "yes / no")

    def t_to_decimal():
        f = Fraction(random.randint(1, 15), pick([8, 16, 20, 25, 40]))
        return _tb("Write %s as an exact decimal." % _fs(f), _ds(f), "num", {}, ["%d ÷ %d = %s." % (f.numerator, f.denominator, _ds(f))])

    def t_to_fraction():
        f = Fraction(random.randint(1, 39), 40)
        return _fq("Write %s as a fraction in its simplest form." % _ds(f), f, ["%s = %s." % (_ds(f), _fs(f))])

    def t_surd_power():
        r = pick([2, 3, 5, 7])
        if d == 2 and random.random() < 0.5:
            return _tb("(√%d)⁵ = k√%d. What is k?" % (r, r), r * r, "int", {},
                       ["(√%d)⁵ = (√%d)² × (√%d)² × √%d = %d × %d × √%d = %d√%d." % (r, r, r, r, r, r, r, r * r, r)])
        return _tb("(√%d)³ = k√%d. What is k?" % (r, r), r, "int", {}, ["(√%d)³ = √%d × √%d × √%d = %d√%d." % (r, r, r, r, r, r)])

    # easy: one-step exact work; hard: mixed numbers, negatives, perimeters with π, surd products and powers
    return _pick_t(_by(d, [t_add, t_divide, t_semi_area, t_quarter, t_surd_square, t_to_decimal, t_to_fraction],
                       [t_add, t_mult_mixed, t_divide, t_neg, t_semi_area, t_semi_perim, t_quarter, t_surd_square, t_surd_rect, t_exact_or_not,
                        t_to_decimal, t_to_fraction, t_surd_power],
                       [t_add, t_mult_mixed, t_divide, t_neg, t_semi_perim, t_surd_rect, t_exact_or_not, t_surd_power]))


# ================================================================== 9.1 ======
@skill("Y9.1.f", "Expand several brackets; factorise with algebraic factors", S1)
def _(d=1):
    d = _d(d)
    # easy: no negative constant inside the brackets; hard: bigger multipliers
    a, b = random.randint(2, _by(d, 5, 5, 9)), random.randint(2, _by(d, 5, 5, 9))
    p, q = random.randint(1, 9), random.randint(_by(d, 1, -9, -9), 9) or 4

    def t_add_brackets():
        return _wq("Expand and simplify %d(x %s) + %d(x %s). Write it like 5x-4." % (a, _t(p), b, _t(q)), _lin(a + b, a * p + b * q),
                   ["%dx %s + %dx %s." % (a, _t(a * p), b, _t(b * q)), "= %s." % _lin(a + b, a * p + b * q)], "e.g. 5x-4")

    def t_sub_brackets():
        aa, bb = max(a, b) + 1, min(a, b)
        return _wq("Expand and simplify %d(x %s) − %d(x %s). Write it like 2x+16." % (aa, _t(p), bb, _t(q)), _lin(aa - bb, aa * p - bb * q),
                   ["%dx %s − %dx %s." % (aa, _t(aa * p), bb, _t(bb * q)), "Careful: −%d × %s = %s." % (bb, "(%d)" % q if q < 0 else q, _ds(-bb * q)),
                    "= %s." % _lin(aa - bb, aa * p - bb * q)], "e.g. 2x+16")

    def t_x_bracket():
        return _wq("Expand and simplify x(x %s) + %d(x %s). Write it like x^2+7x-6." % (_t(p), b, _t(q)), _poly(p + b, b * q),
                   ["x² %s + %dx %s." % (_t(p) + "x", b, _t(b * q)), "= %s." % _poly(p + b, b * q)], "e.g. x^2+7x-6")

    def t_factor_ax2():
        k = random.randint(2, 6)
        m, n = random.randint(1, 5), random.randint(1, 7)
        while _g(m, n) != 1:
            n += 1
        inner = "%s+%d" % (_sx(m), n)
        return _wq("Factorise %dx² + %dx fully (like 3x(2x+3))." % (k * m, k * n), "%dx(%s)" % (k, inner),
                   ["The highest common factor of %dx² and %dx is %dx." % (k * m, k * n, k), "= %dx(%s)." % (k, inner)], "e.g. 3x(2x+3)")

    def t_factor_outside():
        k = random.randint(2, 6)
        m, n = random.randint(2, 6), random.randint(1, 7)
        while _g(m, n) != 1:
            n += 1
        return _wq("Factorise %dx² − %dx fully. What goes OUTSIDE the bracket?" % (k * m, k * n), "%dx" % k,
                   ["HCF of %d and %d is %d, and x is a factor of both terms: %dx(%dx − %d)." % (k * m, k * n, k, k, m, n)], "e.g. 4x")

    def t_factor_xy():
        k = random.randint(2, 6)
        m, n = random.randint(1, 5), random.randint(1, 7)
        while _g(m, n) != 1:
            n += 1
        inner = "%s+%d" % (_sx(m), n)
        return _wq("Factorise %dxy + %dy fully (like 5y(2x+3))." % (k * m, k * n), "%dy(%s)" % (k, inner),
                   ["HCF %dy." % k, "= %dy(%s)." % (k, inner)], "e.g. 5y(2x+3)")

    def t_triple_const():
        r = random.sample(range(1, 6), 3)
        return _tb("Expand (x + %d)(x + %d)(x + %d). What is the constant term?" % tuple(r), r[0] * r[1] * r[2], "int", {},
                   ["Multiply the three numbers: %d × %d × %d = %d." % (r[0], r[1], r[2], r[0] * r[1] * r[2])])

    def t_triple_x2():
        r = random.sample(range(1, 6), 3)
        return _tb("Expand (x + %d)(x + %d)(x + %d). What is the coefficient of x²?" % tuple(r), sum(r), "int", {},
                   ["(x + %d)(x + %d) = %s." % (r[0], r[1], _poly_txt(r[0] + r[1], r[0] * r[1])),
                    "Times (x + %d): the x² terms are %dx² and %dx², total %d." % (r[2], r[2], r[0] + r[1], sum(r))])

    def t_two_products():
        m, n = random.randint(1, 6), random.randint(1, 6)
        return _tb("Expand and simplify (x + %d)(x + %d) + (x + %d)(x − %d). What is the coefficient of x?" % (m, n, m, m), m + n, "int", {},
                   ["%s + %s." % (_poly_txt(m + n, m * n), _poly_txt(0, -m * m)), "x terms: %dx." % (m + n)])

    def t_area():
        k, c = random.randint(2, 5), random.randint(1, 9)
        return _wq("A rectangle is %dx cm wide and (x + %d) cm long. Write its area expanded, like 2x^2+10x." % (k, c), "%dx^2+%dx" % (k, k * c),
                   ["%dx × (x + %d) = %dx² + %dx." % (k, c, k, k * c)], "e.g. 2x^2+10x")

    def t_fully():
        k, m, n = random.randint(2, 4), random.randint(2, 5), random.randint(1, 5)
        while _g(m, n) != 1:
            n += 1
        wrong = "%dx(%dx+%d)" % (k, m * 2, n * 2) if random.random() < 0.5 else None
        shown = wrong or "%dx(%dx+%d)" % (2 * k, m, n)
        return _wq("Is %dx² + %dx fully factorised as %s? (yes or no)" % (2 * k * m, 2 * k * n, shown),
                   "no" if wrong else "yes", ["Fully factorised: %dx(%dx+%d)." % (2 * k, m, n)], "yes / no")

    # easy: add two brackets, one-bracket area, factorise with the form shown; hard: subtraction, x(…), three or two products, 'fully?'
    return _pick_t(_by(d, [t_add_brackets, t_factor_ax2, t_factor_xy, t_triple_const, t_area],
                       [t_add_brackets, t_sub_brackets, t_x_bracket, t_factor_ax2, t_factor_outside, t_factor_xy, t_triple_const, t_triple_x2,
                        t_two_products, t_area, t_fully],
                       [t_sub_brackets, t_x_bracket, t_factor_outside, t_triple_x2, t_two_products, t_fully]))


_ASN = [("x² is always bigger than x.", "sometimes", "True for x = 3, false for x = 0.5."),
        ("The square of a number is never negative.", "always", "A negative times a negative is positive."),
        ("2x is bigger than x + 2.", "sometimes", "True for x = 5, false for x = 1."),
        ("Adding two odd numbers gives an odd number.", "never", "Odd + odd is always even."),
        ("n² + n is an even number (n a whole number).", "always", "n² + n = n(n + 1): one of two consecutive numbers is even."),
        ("Halving a number makes it smaller.", "sometimes", "False for 0 and for negative numbers."),
        ("x + 5 = x + 3", "never", "Subtracting x leaves 5 = 3."),
        ("3(x + 2) = 3x + 6", "always", "It is an identity: expand the bracket.")]

_CONJ = [("n² + n + 41 is prime for every whole number n ≥ 1", lambda n: n * n + n + 41),
         ("2n + 1 is prime for every whole number n ≥ 1", lambda n: 2 * n + 1),
         ("n² + 1 is prime for every whole number n ≥ 1", lambda n: n * n + 1),
         ("n² − n + 11 is prime for every whole number n ≥ 1", lambda n: n * n - n + 11),
         ("6n + 1 is prime for every whole number n ≥ 1", lambda n: 6 * n + 1)]


def _prime(v):
    return v > 1 and all(v % k for k in range(2, int(v ** 0.5) + 1))


@skill("Y9.1.g", "Identities, equations and testing statements", S1)
def _(d=1):
    d = _d(d)

    def t_identity():
        k, c = random.randint(2, 6), random.randint(1, 9)
        x = random.randint(1, 9)
        ident = random.random() < 0.5
        s = "%d(x + %d) = %dx + %d" % (k, c, k, k * c) if ident else "%d(x + %d) = %d" % (k, c, k * (x + c))
        return _wq("Is  %s  an identity (true for every x) or an equation (true for some x)? (type identity or equation)" % s,
                   "identity" if ident else "equation", ["Expand and compare both sides."], "identity / equation")

    def t_asn():
        st, ans, why = pick(_ASN)
        return _wq("Is this always, sometimes or never true?  %s" % st, ans, [why], "always / sometimes / never")

    def t_counter():
        st, f = pick(_CONJ)
        n = 1
        while _prime(f(n)):
            n += 1
        return _tb("Someone claims: '%s'. What is the smallest n that proves them wrong?" % st, n, "int", {},
                   ["n = %d gives %d, which is not prime (%s)." % (n, f(n), "%d × %d" % next((k, f(n) // k) for k in range(2, f(n)) if f(n) % k == 0))])

    def t_identity_const():
        k, a = random.randint(2, 7), random.randint(_by(d, 1, -6, -6), 9) or 3
        return _tb("%d(x + a) ≡ %dx %s for every x. Find a." % (k, k, _t(k * a)), a, "int", {}, ["%dx + %da ≡ %dx %s, so %da = %d." % (k, k, k, _t(k * a), k, k * a)])

    def t_identity_quad():
        p, q = random.randint(1, 7), random.randint(1, 7)
        return _tb("(x + %d)(x + b) ≡ x² + %dx + c for every x. Find c." % (p, p + q), p * q, "int", {},
                   ["The x terms give %d + b = %d, so b = %d." % (p, p + q, q), "c = %d × %d = %d." % (p, q, p * q)])

    def t_test():
        r1, r2 = random.randint(1, 6), random.randint(1, 6)
        x = pick([r1, r2, r1 + 1, r2 + 2])
        ok = (x - r1) * (x - r2) == 0
        return _wq("Is x = %d a solution of %s = 0? (yes or no)" % (x, _poly_txt(-(r1 + r2), r1 * r2)), "yes" if ok else "no",
                   ["%d² − %d × %d + %d = %d." % (x, r1 + r2, x, r1 * r2, (x - r1) * (x - r2))], "yes / no")

    def t_parity():
        q, a = pick([("odd + odd", "even"), ("even + odd", "odd"), ("odd × odd", "odd"), ("even × odd", "even"), ("odd − odd", "even"),
                     ("odd + odd + odd", "odd")])
        return _wq("Is %s always even or always odd?" % q, a, ["Try it with 2n + 1 for odd and 2n for even."], "even / odd")

    def t_proof():
        k = pick([3, 5])
        if k == 3:
            return _tb("Three consecutive whole numbers are n, n + 1 and n + 2. Their sum can be written as 3(n + k). What is k?", 1, "int", {},
                       ["n + n + 1 + n + 2 = 3n + 3 = 3(n + 1).", "So the sum is always a multiple of 3."])
        return _tb("Five consecutive whole numbers are n, n + 1, …, n + 4. Their sum can be written as 5(n + k). What is k?", 2, "int", {},
                   ["5n + 10 = 5(n + 2).", "So the sum is always a multiple of 5."])

    def t_disprove():
        claim, cands, ans = pick([("Squaring a number always makes it bigger.", ["2", "0.5", "10"], "0.5"),
                                  ("Dividing 10 by a number always gives an answer smaller than 10.", ["2", "5", "0.5"], "0.5"),
                                  ("Every prime number is odd.", ["3", "2", "7"], "2"),
                                  ("A number's cube is always bigger than its square.", ["3", "0.2", "5"], "0.2")])
        random.shuffle(cands)
        return _tb("'%s' Which of %s proves this wrong?" % (claim, ", ".join(cands)), ans, "num", {},
                   ["Try %s: the claim fails." % ans])

    def t_solutions():
        k, c = random.randint(2, 6), random.randint(1, 9)
        same = random.random() < 0.5
        rhs = "%dx + %d" % (k, k * c) if same else "%dx + %d" % (k, k * c + random.randint(1, 5))
        return _wq("How many solutions does %d(x + %d) = %s have? (type none, one or infinitely many)" % (k, c, rhs),
                   "infinitely many" if same else "none", ["Expand the left: %dx + %d." % (k, k * c),
                                                           "Same both sides: every x works." if same else "The x terms cancel and leave a false statement."],
                   "none / one / infinitely many")

    # easy: classify or test one statement; hard: counter-examples, matching coefficients, short proofs
    return _pick_t(_by(d, [t_identity, t_asn, t_identity_const, t_test, t_parity, t_solutions],
                       [t_identity, t_asn, t_counter, t_identity_const, t_identity_quad, t_test, t_parity, t_proof, t_disprove, t_solutions],
                       [t_counter, t_identity_const, t_identity_quad, t_proof, t_disprove, t_solutions]))


# ================================================================== 9.2 ======
@skill("Y9.2.e", "Form and solve equations from angles, shapes and words", S2)
def _(d=1):
    d = _d(d)

    def _two_sum(total):
        """ax + b and cx + e adding to `total` with a whole x."""
        while True:
            a, c = random.randint(1, 5), random.randint(1, 5)
            x = random.randint(5, 40)
            b = random.randint(-10, 30)
            e = total - (a + c) * x - b
            if -20 <= e <= 60 and a * x + b > 0 and c * x + e > 0:
                return a, b, c, e, x

    def _ex(a, b):
        return "%s%s" % ("x" if a == 1 else "%dx" % a, "" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))

    def t_line():
        a, b, c, e, x = _two_sum(180)
        return _tb("Two angles on a straight line are (%s)° and (%s)°. Find x." % (_ex(a, b), _ex(c, e)), x, "int", {},
                   ["They add to 180: %dx %s = 180." % (a + c, _t(b + e)), "x = %d." % x])

    def t_point():
        a, b, c, e, x = _two_sum(360)
        return _tb("Two angles around a point are (%s)° and (%s)°, and they make a full turn. Find x." % (_ex(a, b), _ex(c, e)), x, "int", {},
                   ["They add to 360: %dx %s = 360." % (a + c, _t(b + e)), "x = %d." % x])

    def t_triangle():
        while True:
            k1, k2, c = random.randint(1, 3), random.randint(1, 4), random.randint(0, 40)
            if (180 - c) % (1 + k1 + k2) == 0:
                x = (180 - c) // (1 + k1 + k2)
                break
        return _tb("The angles of a triangle are x°, %s° and (%s)°. Find x." % (_ex(k1, 0), _ex(k2, c)), x, "int", {},
                   ["%dx + %d = 180." % (1 + k1 + k2, c), "x = %d." % x])

    def t_vert_opp():
        x = random.randint(5, 40)
        a, c = random.sample(range(2, 7), 2)
        b = random.randint(0, 20)
        e = a * x + b - c * x
        return _tb("Two vertically opposite angles are (%s)° and (%s)°. Find x." % (_ex(a, b), _ex(c, e)), x, "int", {},
                   ["Vertically opposite angles are equal: %s = %s." % (_ex(a, b), _ex(c, e)), "x = %d." % x])

    def t_perimeter():
        x, c, k = random.randint(2, 15), random.randint(1, 9), random.randint(2, 3)
        P = 2 * (x + c) + 2 * k * x
        return _tb("A rectangle has length (x + %d) cm and width %dx cm. Its perimeter is %d cm. Find x." % (c, k, P), x, "int", {},
                   ["2(x + %d) + 2(%dx) = %d." % (c, k, P), "%dx + %d = %d, x = %d." % (2 + 2 * k, 2 * c, P, x)])

    def t_isos():
        x = random.randint(3, 15)
        a, c = random.sample(range(2, 7), 2)
        b = random.randint(1, 12)
        e = a * x - b - c * x
        return _tb("An isosceles triangle has two equal sides of (%s) cm and (%s) cm. Find x." % (_ex(a, -b), _ex(c, e)), x, "int", {},
                   ["The equal sides give %s = %s." % (_ex(a, -b), _ex(c, e)), "x = %d." % x]) if c * x + e > 0 and a * x - b > 0 else t_perimeter()

    def t_ages():
        k = pick([3, 4])
        t = random.randint(2, 9) * (k - 2)
        child = t // (k - 2)
        return _tb("A parent is %d times as old as their child. In %d years the parent will be twice as old as the child. How old is the child "
                   "now?" % (k, t), child, "int", {"unit": "years"},
                   ["%dc + %d = 2(c + %d)." % (k, t, t), "%sc = %d, c = %d." % ("" if k == 3 else k - 2, t, child)])

    def t_consecutive():
        n, k = random.randint(1, _by(d, 20, 40, 90)), pick(_by(d, [3], [3, 4, 5], [4, 5]))
        return _tb("%s consecutive whole numbers add up to %d. What is the smallest?" % (_words(k).capitalize(), k * n + k * (k - 1) // 2), n, "int", {},
                   ["n + (n + 1) + … = %dn + %d = %d." % (k, k * (k - 1) // 2, k * n + k * (k - 1) // 2), "n = %d." % n])

    def t_tickets():
        x, dsc = random.randint(6, 20), random.randint(2, 5)
        na, nc = random.randint(1, 4), random.randint(1, 5)
        tot = na * x + nc * (x - dsc)
        return _tb("An adult ticket costs £x and a child ticket costs £%d less. %s and %s cost £%d. Find x." % (dsc, _pl(na, "adult ticket"),
                   _pl(nc, "child ticket"), tot), x, "int", {"unit": "£"},
                   ["%dx + %d(x − %d) = %d." % (na, nc, dsc, tot), "%dx = %d, x = %d." % (na + nc, tot + nc * dsc, x)])

    def t_think():
        n = random.randint(2, 15)
        a, b = random.randint(2, 4), random.randint(1, 15)
        c = a + random.randint(1, 3)
        e = a * n + b - c * n
        if e == 0:
            b, e = b + 1, 1
        return _tb("I think of a number. If I multiply it by %d and add %d, I get the same answer as when I multiply it by %d and %s %d. "
                   "What is my number?" % (a, b, c, "add" if e >= 0 else "subtract", abs(e)), n, "int", {},
                   ["%dn + %d = %dn %s." % (a, b, c, _t(e)), "n = %d." % n])

    def t_quad_angles():
        x = random.randint(10, 40)
        ks = [1] + [random.randint(1, 3) for _ in range(3)]
        cs = [0] + [random.randint(0, 20) for _ in range(2)]
        cs.append(360 - sum(ks) * x - sum(cs))
        if cs[3] < -30 or ks[3] * x + cs[3] <= 0:
            return t_triangle()
        parts = ["x°"] + ["(%s)°" % _ex(k, c) for k, c in zip(ks[1:], cs[1:])]
        return _tb("The angles of a quadrilateral are %s. Find x." % ", ".join(parts), x, "int", {},
                   ["They add to 360: %dx %s = 360." % (sum(ks), _t(sum(cs))), "x = %d." % x])

    # easy: one fact, x on one side; hard: x on both sides, four angles, ages and 'think of a number'
    return _pick_t(_by(d, [t_line, t_triangle, t_perimeter, t_consecutive, t_tickets],
                       [t_line, t_point, t_triangle, t_vert_opp, t_perimeter, t_isos, t_ages, t_consecutive, t_tickets, t_think, t_quad_angles],
                       [t_point, t_vert_opp, t_isos, t_ages, t_consecutive, t_think, t_quad_angles]))


# ================================================================== 9.3 ======
_GTYPES = ["linear", "quadratic", "cubic", "reciprocal"]


def _gfun(kind):
    """(equation text, f) for a random graph of the given kind."""
    if kind == "linear":
        m, c = random.choice([v for v in range(-4, 5) if v]), random.randint(-5, 5)
        return "y = %s%s" % ({1: "x", -1: "−x"}.get(m, "%dx" % m if m > 0 else "−%dx" % -m), " " + _t(c) if c else ""), (lambda x: m * x + c)
    if kind == "quadratic":
        b, c = random.randint(-3, 3), random.randint(-5, 5)
        return "y = " + _poly_txt(b, c), (lambda x: x * x + b * x + c)
    if kind == "cubic":
        c = random.randint(-5, 5)
        return "y = x³" + ("" if c == 0 else " %s %d" % ("+" if c > 0 else "−", abs(c))), (lambda x: x ** 3 + c)
    k = pick([6, 12, 24])
    return "y = %d/x" % k, (lambda x: Fraction(k, x))


@skill("Y9.3.e", "Recognise linear, quadratic, cubic and reciprocal graphs", S3)
def _(d=1):
    d = _d(d)
    kind = pick(_GTYPES)
    eq, f = _gfun(kind)
    hint = {"linear": "Highest power of x is 1: a straight line.", "quadratic": "Highest power 2: a U-shaped (or ∩-shaped) parabola.",
            "cubic": "Highest power 3: an S-shaped curve.", "reciprocal": "x is on the bottom of a fraction: two separate curves that never touch the axes."}

    def t_equation():
        return _wq("What type of graph is %s? (linear, quadratic, cubic or reciprocal)" % eq, kind, [hint[kind]], "linear / quadratic / cubic / reciprocal")

    def t_table():
        xs = [1, 2, 3, 4, 6] if kind == "reciprocal" else [-2, -1, 0, 1, 2, 3]
        return _dt("This table of values comes from one graph. What type of graph is it? (linear, quadratic, cubic or reciprocal)", ["x", "y"],
                   [[x, _fs(f(x))] for x in xs], kind, [hint[kind]], atype="str", placeholder="type of graph")

    def t_graph():
        xs = [1, 2, 3, 4, 5, 6] if kind == "reciprocal" else [-3, -2, -1, 0, 1, 2, 3]
        return _lg("The graph joins points of one function. What type of graph is it? (linear, quadratic, cubic or reciprocal)",
                   [[str(x), float(f(x))] for x in xs], kind, [hint[kind]], "y", "x", atype="str")

    def t_feature():
        q, a = pick([("Which type of graph is a straight line?", "linear"), ("Which type of graph is U-shaped?", "quadratic"),
                     ("Which type of graph never crosses either axis?", "reciprocal"), ("Which type of graph has an S shape?", "cubic"),
                     ("Which type of graph is y = 5/x?", "reciprocal"), ("Which type of graph is y = 2x² − 1?", "quadratic")])
        return _wq(q + " (linear, quadratic, cubic or reciprocal)", a, [hint[a]], "linear / quadratic / cubic / reciprocal")

    def t_cubic_value():
        x, k = random.randint(-3, 3), random.randint(1, 5)
        return _tb("y = x³ − %dx. Find y when x = %d." % (k, x), x ** 3 - k * x, "int", {},
                   ["(%d)³ − %d × (%d) = %d." % (x, k, x, x ** 3 - k * x)])

    def t_recip_value():
        k = pick([12, 24, 36, 60])
        x = pick([v for v in (-6, -4, -3, -2, 2, 3, 4, 6) if k % v == 0])
        return _tb("y = %d/x. Find y when x = %d." % (k, x), k // x, "int", {}, ["%d ÷ %d = %d." % (k, x, k // x)])

    def t_on_graph():
        x = random.randint(-3, 3)
        y = x ** 3 + pick([0, 0, 1, -1])
        return _wq("Does the point (%d,%d) lie on the graph of y = x³? (yes or no)" % (x, y), "yes" if y == x ** 3 else "no",
                   ["%d³ = %d." % (x, x ** 3)], "yes / no")

    def t_complete():
        kk = pick(["cubic", "reciprocal"])
        if kk == "cubic":
            c = random.randint(-5, 5)
            rows = [[x, x ** 3 + c] for x in (-2, -1, 0, 1, 2, 3)]
            i = random.randrange(6)
            return _io("Complete the table for y = x³%s." % (" " + _t(c) if c else ""), rows, i, rows[i][1],
                       ["(%d)³%s = %d." % (rows[i][0], " " + _t(c) if c else "", rows[i][1])])
        k = pick([12, 24, 60])
        xs = [x for x in (1, 2, 3, 4, 5, 6, 10, 12) if k % x == 0][:6]
        rows = [[x, k // x] for x in xs]
        i = random.randrange(len(rows))
        return _io("Complete the table for y = %d/x." % k, rows, i, rows[i][1], ["%d ÷ %d = %d." % (k, rows[i][0], rows[i][1])])

    # easy: name the type from its equation, shape or plotted graph; hard: from a table, and substituting into cubics/reciprocals
    return _pick_t(_by(d, [t_equation, t_feature], [t_equation, t_feature, t_cubic_value, t_recip_value, t_on_graph],
                       [t_cubic_value, t_recip_value, t_on_graph]),
                   _by(d, [t_graph], [t_table, t_graph, t_complete], [t_table, t_complete]))


@skill("Y9.3.f", "Parallel lines and y = mx + c", S3)
def _(d=1):
    d = _d(d)
    m = random.choice([v for v in range(_by(d, 1, -5, -5), 6) if v])  # easy: positive gradients only
    c = random.randint(-6, 6)

    def t_pick():
        other = random.choice([v for v in range(-5, 6) if v and v != m])
        right = _line(m, c + random.randint(1, 5))
        wrong = _line(other, c)
        opts = [right, wrong]
        random.shuffle(opts)
        return _wq("Which line is parallel to %s?  A: %s   B: %s  (type A or B)" % (_line(m, c), opts[0], opts[1]), "A" if opts[0] == right else "B",
                   ["Parallel lines have the same gradient, %d." % m], "A / B")

    def t_rearranged():
        form = pick(["ky", "minus", "plus"])
        if form == "ky":
            k = random.randint(2, 5)
            return _tb("What is the gradient of the line %dy = %dx %s?" % (k, k * m, _t(k * c)), m, "int", {}, ["Divide by %d: y = %dx %s." % (k, m, _t(c))])
        if form == "minus":
            return _tb("What is the gradient of the line y %s %s = %d?" % ("−" if m > 0 else "+", _sx(abs(m)), c), m, "int", {},
                       ["Make y the subject: %s." % _line(m, c)])
        return _tb("What is the gradient of the line %s + y = %d?" % (_sx(-m).replace("-", "−"), c), m, "int", {},
                   ["Make y the subject: %s." % _line(m, c)])

    def t_frac_grad():
        p, q = random.randint(1, 5), pick([2, 3, 4])
        if p % q == 0:
            p += 1
        return _fq("What is the gradient of %dy + %s = 12?" % (q, _sx(p)), Fraction(-p, q), ["y = −%d/%d x + %s." % (p, q, _fs(Fraction(12, q)))], "e.g. -2/3")

    def t_through():
        x0 = random.randint(-4, 4)
        c2 = c + random.randint(1, 6)
        return _tb("A line is parallel to %s and passes through (%d,%d). Where does it cross the y-axis? Give the y-value." % (_line(m, c), x0, m * x0 + c2),
                   c2, "int", {}, ["Same gradient %d: y = %dx + c." % (m, m), "%d = %d × %s + c, so c = %d." % (m * x0 + c2, m, "(%d)" % x0 if x0 < 0 else x0, c2)])

    def t_equation():
        x0 = random.randint(-3, 3)
        c2 = c - random.randint(1, 6)
        return _wq("Write the equation of the line parallel to %s through (%d,%d). Write it like y=2x+3." % (_line(m, c), x0, m * x0 + c2), _line(m, c2),
                   ["c = %d − %d × %s = %d." % (m * x0 + c2, m, "(%d)" % x0 if x0 < 0 else x0, c2)], "e.g. y=2x+3")

    def t_are_parallel():
        k = random.randint(2, 4)
        same = random.random() < 0.5
        m2 = m if same else pick([v for v in (m - 1, m + 1) if v])
        return _wq("Are the lines %s and %dy = %dx%s parallel? (yes or no)" % (_line(m, c), k, k * m2, (" " + _t(k * (c + 2))) if c != -2 else ""), "yes" if same else "no",
                   ["The second is %s, gradient %d." % (_line(m2, c + 2), m2)], "yes / no")

    def t_meet():
        return _tb("How many times do the lines %s and %s cross?" % (_line(m, c), _line(m, c + random.randint(1, 6))), 0, "int", {},
                   ["Same gradient, different intercepts: parallel lines never meet."])

    def t_find_k():
        k = random.randint(2, 4)
        return _tb("The line y = %dx + 1 is parallel to %dy = kx − 3. Find k." % (m, k), k * m, "int", {},
                   ["%dy = kx − 3 gives gradient k/%d." % (k, k), "k/%d = %d, so k = %d." % (k, m, k * m)])

    def t_grid():
        mm = random.choice([-2, -1, 1, 2])
        c1 = random.randint(-3, 3)
        c2 = c1 + pick([-4, -3, 3, 4])
        if not -6 <= c2 <= 6:
            c2 = c1 - (c2 - c1)
        return {"prompt": "The two lines are parallel. One is %s. Type the equation of the other, like y=2x+3." % _line(mm, c1),
                "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "lines": [{"p1": [0, c1], "p2": [1, c1 + mm], "label": _line(mm, c1)},
                                                                                  {"p1": [0, c2], "p2": [1, c2 + mm]}],
                         "points": [[0, c2, ""]], "typed": True, "placeholder": "y=mx+c"},
                "answer": _line(mm, c2), "answer_type": "str", "solution": ["Same gradient %d; it crosses the y-axis at %d." % (mm, c2)]}

    # easy: spot the same gradient in y = mx + c; hard: rearrange first, fractional gradients, find k, write the equation
    return _pick_t(_by(d, [t_pick, t_through, t_meet], [t_pick, t_rearranged, t_frac_grad, t_through, t_equation, t_are_parallel, t_meet, t_find_k],
                       [t_rearranged, t_frac_grad, t_equation, t_are_parallel, t_find_k]), [t_grid])


@skill("Y9.3.g", "Approximate solutions from graphs, including simultaneous equations", S3)
def _(d=1):
    d = _d(d)

    def _pair():
        x0, y0 = random.randint(_by(d, 0, -3, -3), 3), random.randint(_by(d, 0, -3, -3), 3)  # easy: crossing in the first quadrant
        m1, m2 = random.sample([-2, -1, 1, 2, 3], 2)
        return x0, y0, (m1, y0 - m1 * x0), (m2, y0 - m2 * x0)

    def _grid(prompt, x0, y0, l1, l2, answer, atype, ph):
        return {"prompt": prompt, "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "typed": True, "placeholder": ph,
                         "lines": [{"p1": [x0, y0], "p2": [x0 + 1, y0 + l1[0]], "label": _line(*l1)},
                                   {"p1": [x0, y0], "p2": [x0 + 1, y0 + l2[0]], "label": _line(*l2)}]},
                "answer": answer, "answer_type": atype,
                "solution": ["The lines cross at (%d,%d)." % (x0, y0), "Check: %d = %d × %d %s and %d = %d × %d %s." % (
                    y0, l1[0], x0, _t(l1[1]), y0, l2[0], x0, _t(l2[1]))]}

    def t_cross():
        x0, y0, l1, l2 = _pair()
        return _grid("Use the graph to solve the simultaneous equations %s and %s. Type the crossing point like (2,-1)." % (_line(*l1), _line(*l2)),
                     x0, y0, l1, l2, "(%d,%d)" % (x0, y0), "coord", "(x,y)")

    def t_cross_x():
        x0, y0, l1, l2 = _pair()
        return _grid("Use the graph to solve %s and %s. What is x?" % (_line(*l1), _line(*l2)), x0, y0, l1, l2, x0, "num", "x =")

    def t_cross_y():
        x0, y0, l1, l2 = _pair()
        return _grid("Use the graph to solve %s and %s. What is y?" % (_line(*l1), _line(*l2)), x0, y0, l1, l2, y0, "num", "y =")

    def t_quad_root():
        k = random.choice([v for v in range(2, 15) if int(v ** 0.5) ** 2 != v])
        xs = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        q = _lg("The graph shows y = x² − %d. Estimate the POSITIVE solution of x² − %d = 0, to 1 decimal place." % (k, k),
                [[str(x), x * x - k] for x in xs], round(k ** 0.5 + 1e-12, 1), ["Read where the curve crosses the x-axis: x ≈ %.2f." % k ** 0.5],
                "y", "x", atype="num")
        q["tolerance"] = 0.21
        return q

    def t_quad_equal():
        k = pick([1, 4, 9, 16])
        xs = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        q = _lg("The graph shows y = x². Use it to solve x² = %d. Type both answers, like -3, 3." % k, [[str(x), x * x] for x in xs],
                "%d, %d" % (-int(k ** 0.5), int(k ** 0.5)), ["Read across from y = %d: x = ±%d." % (k, int(k ** 0.5))], "y", "x", atype="set")
        return q

    def t_read_y():
        b = random.randint(-3, 3)
        x = random.randint(-3, 3)
        xs = [-3, -2, -1, 0, 1, 2, 3]
        return _lg("The graph shows y = %s. Use it to find y when x = %d." % (_poly_txt(b, 0), x), [[str(v), v * v + b * v] for v in xs], x * x + b * x,
                   ["Read up from x = %d: y = %d." % (x, x * x + b * x)], "y", "x")

    def t_reciprocal():
        k = pick([24, 36, 48, 60])
        ns = [n for n in range(1, 13) if k % n == 0][:7]
        n = pick(ns[1:-1])
        return _lg("The time a job takes is t = %d/n hours when n people share it. Use the graph to find how many people finish it in %d hours."
                   % (k, k // n), [[str(v), k // v] for v in ns], n, ["Read across from t = %d: n = %d." % (k // n, n)], "Hours", "People")

    def t_exponential():
        start = pick([50, 100, 200])
        h = random.randint(2, 5)
        return _lg("A number of bacteria doubles every hour, as the graph shows. After how many hours are there %s bacteria?" % _c(start * 2 ** h),
                   [["%d h" % v, start * 2 ** v] for v in range(0, 7)], h, ["Read across from %s: %d hours." % (_c(start * 2 ** h), h)], "Bacteria", "Time")

    def t_piecewise():
        base, per, free = pick([(3, 2, 2), (4, 2, 1), (5, 3, 2)])
        km = random.randint(free + 1, 8)
        pts = [["%d km" % v, base if v <= free else base + per * (v - free)] for v in range(0, 9)]
        return _lg("A taxi fare is £%d for up to %d km, then £%d for each extra km, as the graph shows. Use it to find the fare for %d km, in pounds."
                   % (base, free, per, km), pts, base + per * (km - free), ["£%d + %d × £%d = £%d." % (base, km - free, per, base + per * (km - free))],
                   "£", "Distance")

    def t_how_many():
        c = pick([4, 0, -1, 9, -4])
        n = 2 if c > 0 else 1 if c == 0 else 0
        return _tb("How many times does the graph of y = x² meet the line y = %d?" % c, n, "int", {},
                   ["y = x² is never below 0; it touches y = 0 once and crosses higher lines twice."])

    # easy: read one value or one crossing; hard: estimate a root to 1 dp, read a reciprocal graph backwards, solve x² = k
    return _pick_t([t_how_many], _by(d, [t_cross, t_cross_x, t_cross_y, t_read_y, t_exponential, t_piecewise],
                                     [t_cross, t_cross_x, t_cross_y, t_quad_root, t_quad_equal, t_read_y, t_reciprocal, t_exponential, t_piecewise],
                                     [t_cross, t_quad_root, t_quad_equal, t_reciprocal, t_piecewise]))
