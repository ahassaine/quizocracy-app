# Year 9 generators: strands 9.0 and 9.1 (upper KS3, beyond the Year 8 bank).
#
# Zero and negative indices, standard form with negative powers and calculations, roots and
# estimating surds; expanding double brackets, factorising quadratics and the difference of two
# squares, rearranging formulae, algebraic fractions and indices in algebra.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S0 = "9.0 Indices, roots & standard form"
S1 = "9.1 Algebraic manipulation"


def _sf(x):
    """Decimal -> standard form text '3.2x10^-4' and its parts."""
    x = Decimal(x)
    e = x.adjusted()
    a = (x / (Decimal(10) ** e)).normalize()
    return "%sx10^%d" % (_ds(a), e), a, e


def _poly(b, c, var="x"):
    """x^2+bx+c as compact text."""
    s = var + "^2"
    if b:
        s += ("+" if b > 0 else "-") + ("" if abs(b) == 1 else str(abs(b))) + var
    if c:
        s += ("+" if c > 0 else "-") + str(abs(c))
    return s


def _a(n):
    """'a' or 'an' before a number as it is read aloud: an 8, an 11, an 18, an 80, an 8.5 — but a 110."""
    s = str(n).replace(",", "").lstrip("-").split(".")[0]
    return "an" if s.startswith("8") or (s[:2] in ("11", "18") and len(s) % 3 == 2) else "a"


def _bracket(p, var="x"):
    return "(%s%s%d)" % (var, "+" if p >= 0 else "-", abs(p))


# ================================================================== 9.0 ======
@skill("Y9.0.a", "Zero and negative indices", S0)
def _(d=1):
    d = _d(d)
    b = random.randint(2, _by(d, 5, 10, 10))
    n = random.randint(1, _by(d, 2, 3, 3))

    def t_zero():
        return _tb("Work out %d^0." % random.randint(2, 999), 1, "int", {}, ["Any non-zero number to the power 0 is 1."])

    def t_neg():
        return _fq("Work out %d^-%d as a fraction." % (b, n), Fraction(1, b ** n), ["%d^-%d = 1/%d^%d = 1/%d." % (b, n, b, n, b ** n)])

    def t_neg_decimal():
        k = pick([1, 2, 3])
        return _tb("Write 10^-%d as a decimal." % k, _ds(Decimal(1) / 10 ** k), "num", {}, ["1/%d = %s." % (10 ** k, _ds(Decimal(1) / 10 ** k))])

    def t_frac_neg():
        p, q = random.randint(2, 5), random.randint(2, 5)
        if p == q:
            q += 1
        return _fq("Work out (%d/%d)^-1." % (p, q), Fraction(q, p), ["A power of −1 flips the fraction: %d/%d." % (q, p)])

    def t_which_power():
        return _tb("%d^? = 1/%d. What is the power?" % (b, b ** n), -n, "int", {}, ["1/%d = %d^-%d." % (b ** n, b, n)])

    def t_laws():
        a1, a2 = random.randint(-4, 6), random.randint(-6, 4)
        return _tb("Simplify x^%d × x^%d. What is the power of x?" % (a1, a2), a1 + a2, "int", {}, ["Add the powers: %d + (%d) = %d." % (a1, a2, a1 + a2)])

    def t_frac_neg_sq():
        p, q = pick([(2, 3), (3, 4), (2, 5), (3, 5), (1, 2), (1, 3)])
        return _fq("Work out (%d/%d)^-2 as a fraction." % (p, q), Fraction(q * q, p * p),
                   ["Flip the fraction: (%d/%d)^2." % (q, p), "= %d/%d." % (q * q, p * p)])

    def t_sum():
        k = pick([2, 3])
        return _fq("Work out %d^-1 + %d^-2 as a single fraction." % (k, k), Fraction(1, k) + Fraction(1, k * k),
                   ["1/%d + 1/%d." % (k, k * k), "= %s." % _fs(Fraction(1, k) + Fraction(1, k * k))])

    def t_power_of_ten():
        k = random.randint(1, 5)
        return _tb("Write %s as a power of 10. What is the power?" % _ds(Decimal(1) / 10 ** k), -k, "int", {},
                   ["%s = 1/%s = 10^-%d." % (_ds(Decimal(1) / 10 ** k), _c(10 ** k), k)])

    def t_decimal_base():
        bb = pick([2, 4, 5, 8])
        return _tb("Work out %d^-1 as a decimal." % bb, _ds(Fraction(1, bb)), "num", {}, ["1/%d = %s." % (bb, _ds(Fraction(1, bb)))])

    def t_spot():
        return _fq("Sam says %d^-%d = −%d. What is the correct value, as a fraction?" % (b, n, b ** n), Fraction(1, b ** n),
                   ["A negative power means a reciprocal, not a negative number.", "%d^-%d = 1/%d." % (b, n, b ** n)])

    def t_mixed_laws():
        bb = pick([2, 3, 5])
        p, q = random.randint(-4, -1), random.randint(2, 5)
        v = Fraction(bb) ** (p + q)
        return _fq("Work out %d^%d × %d^%d. Give a whole number or a fraction." % (bb, p, bb, q), v,
                   ["Add the powers: %d + %d = %d." % (p, q, p + q), "%d^%d = %s." % (bb, p + q, _fs(v))])

    def t_divide_powers():
        bb = pick([2, 3, 10])
        p, q = random.randint(1, 4), random.randint(5, 7)
        return _fq("Work out %d^%d ÷ %d^%d as a fraction." % (bb, p, bb, q), Fraction(1, bb ** (q - p)),
                   ["Subtract the powers: %d − %d = %d." % (p, q, p - q), "%d^%d = 1/%d." % (bb, p - q, bb ** (q - p))])

    def t_pattern():
        bb = pick([2, 3, 10])
        pw = [3, 2, 1, 0, -1, -2]
        rows = [["%d^%d" % (bb, k), _fs(Fraction(bb) ** k)] for k in pw]
        i = random.randint(3, 5)
        return _dt("Each row is the one above divided by %d. Complete the table." % bb, ["Power", "Value"], rows,
                   _fs(Fraction(bb) ** pw[i]), ["Keep dividing by %d: %s = %s." % (bb, rows[i][0], rows[i][1])],
                   missing=[i, 1], atype="frac", placeholder="e.g. 1/4")

    return _pick_t([t_zero, t_neg, t_neg_decimal, t_frac_neg, t_which_power, t_laws, t_frac_neg_sq, t_sum, t_power_of_ten,
                    t_decimal_base, t_spot, t_mixed_laws, t_divide_powers], [t_pattern])


@skill("Y9.0.b", "Standard form with negative powers", S0)
def _(d=1):
    d = _d(d)

    def t_small_to_sf():
        x = Decimal(random.randint(11, 999)) / Decimal(10) ** random.randint(4, 8)
        sf, a, e = _sf(x)
        return _wq("Write %s in standard form (like 3.2x10^-4)." % _ds(x), sf, ["Move the point %d places: %s × 10^%d." % (-e, _ds(a), e)],
                   "e.g. 3.2x10^-4")

    def t_sf_to_small():
        a = Decimal(random.randint(11, 99)) / 10
        e = -random.randint(2, 6)
        return _tb("Write %sx10^%d as an ordinary number." % (_ds(a), e), _ds(a * Decimal(10) ** e), "num", {},
                   ["Move the point %d places left." % -e])

    def t_order():
        vals = [Decimal(random.randint(11, 99)) / 10 * Decimal(10) ** random.randint(-6, 6) for _ in range(4)]
        shown = [_sf(v)[0] for v in vals]
        return _wq("Which is the smallest?  %s  (type it as written)" % ", ".join(shown), shown[vals.index(min(vals))],
                   ["Compare the powers first."], "as written")

    def t_power():
        x = Decimal(random.randint(1, 9)) * Decimal(10) ** -random.randint(3, 9)
        return _tb("%s written in standard form is A × 10^n. What is n?" % _ds(x), _sf(x)[2], "int", {}, ["Count the places: n = %d." % _sf(x)[2]])

    def t_context():
        thing, x = pick([("the width of a human hair, in metres", Decimal("0.00008")),
                         ("the mass of a grain of sand, in grams", Decimal("0.0006")),
                         ("the diameter of a red blood cell, in metres", Decimal("0.000007"))])
        return _wq("Write %s, %s, in standard form (like 3.2x10^-4)." % (thing, _ds(x)), _sf(x)[0], ["= %s." % _sf(x)[0]], "e.g. 8x10^-5")

    return _pick_t([t_small_to_sf, t_sf_to_small, t_order, t_power, t_context])


@skill("Y9.0.c", "Calculate with numbers in standard form", S0)
def _(d=1):
    d = _d(d)
    a, b = random.randint(2, 9), random.randint(2, 9)
    m, n = random.randint(-5, 8), random.randint(-5, 8)

    def t_mult():
        p = Decimal(a * b) * Decimal(10) ** (m + n)
        return _wq("Work out (%dx10^%d) × (%dx10^%d). Give your answer in standard form." % (a, m, b, n), _sf(p)[0],
                   ["%d × %d = %d; powers %d + %d = %d." % (a, b, a * b, m, n, m + n), "= %s." % _sf(p)[0]], "e.g. 1.2x10^5")

    def t_div():
        top = Decimal(a * b) * Decimal(10) ** m
        q = top / (Decimal(b) * Decimal(10) ** n)
        return _wq("Work out (%s) ÷ (%dx10^%d). Give your answer in standard form." % (_sf(top)[0], b, n), _sf(q)[0],
                   ["%s = %dx10^%d." % (_sf(top)[0], a * b, m), "%d ÷ %d = %d; powers %d − %d = %d." % (a * b, b, a, m, n, m - n),
                    "= %s." % _sf(q)[0]], "e.g. 4x10^3")

    def t_add():
        e = random.randint(3, 6)
        x, y = Decimal(a) * 10 ** e, Decimal(b) * 10 ** (e - 1)
        return _wq("Work out %s + %s. Give your answer in standard form." % (_sf(x)[0], _sf(y)[0]), _sf(x + y)[0],
                   ["As ordinary numbers: %s + %s = %s." % (_c(int(x)), _c(int(y)), _c(int(x + y)))], "e.g. 4.3x10^5")

    def t_square():
        k = random.randint(2, 4)
        e = random.randint(2, 5)
        p = Decimal(k * k) * Decimal(10) ** (2 * e)
        return _wq("Work out (%dx10^%d)². Give your answer in standard form." % (k, e), _sf(p)[0], ["%d² = %d; power × 2." % (k, k * k)],
                   "e.g. 9x10^6")

    def t_subtract():
        e = random.randint(3, 6)
        x, y = Decimal(max(a, b)) * 10 ** e, Decimal(min(a, b)) * 10 ** (e - 1)
        return _wq("Work out %s − %s. Give your answer in standard form." % (_sf(x)[0], _sf(y)[0]), _sf(x - y)[0],
                   ["As ordinary numbers: %s − %s = %s." % (_c(int(x)), _c(int(y)), _c(int(x - y)))], "e.g. 4.3x10^5")

    def t_times_bigger():
        e1, e2 = random.randint(5, 9), random.randint(1, 4)
        big, small = a * b, b
        return _tb("How many times bigger is %dx10^%d than %dx10^%d?" % (big, e1, small, e2) if big < 10 else
                   "How many times bigger is %s than %dx10^%d?" % (_sf(Decimal(big) * 10 ** e1)[0], small, e2),
                   a * 10 ** (e1 - e2), "int", {}, ["Divide: %d × 10^%d = %s." % (a, e1 - e2, _c(a * 10 ** (e1 - e2)))])

    def t_power_n():
        p = Decimal(a * b) * Decimal(10) ** (m + n)
        return _tb("(%dx10^%d) × (%dx10^%d) = A × 10^n in standard form. What is n?" % (a, m, b, n), _sf(p)[2], "int", {},
                   ["%d × %d = %d, and 10^%d × 10^%d = 10^%d." % (a, b, a * b, m, n, m + n), "%s, so n = %d." % (_sf(p)[0], _sf(p)[2])])

    def t_context_grains():
        mass = random.randint(2, 9)
        cnt = random.randint(2, 9)
        p = Decimal(mass * cnt) * Decimal(10) ** (-4 + 6)
        return _wq("A grain of rice has a mass of %dx10^-4 kg. What is the mass of %dx10^6 grains, in kg? Give your answer in standard form."
                   % (mass, cnt), _sf(p)[0], ["%d × %d = %d; powers −4 + 6 = 2." % (mass, cnt, mass * cnt), "= %s kg." % _sf(p)[0]],
                   "e.g. 1.2x10^3")

    def t_light():
        dist = pick([(Decimal("1.5"), 8, 500), (Decimal("3.9"), 8, 1300), (Decimal("6"), 7, 200), (Decimal("4.5"), 8, 1500)])
        return _tb("Light travels 3x10^5 km every second. A distance is %sx10^%d km. How many seconds does light take to cover it?"
                   % (_ds(dist[0]), dist[1]), dist[2], "int", {"unit": "seconds"},
                   ["%sx10^%d ÷ 3x10^5 = %d." % (_ds(dist[0]), dist[1], dist[2])])

    def t_sqrt():
        k = random.randint(2, 9)
        e = random.randint(1, 5) * 2
        return _wq("Work out √(%dx10^%d). Give your answer in standard form." % (k * k, e), "%dx10^%d" % (k, e // 2),
                   ["√%d = %d and √10^%d = 10^%d." % (k * k, k, e, e // 2)], "e.g. 3x10^4")

    return _pick_t([t_mult, t_div, t_add, t_square, t_subtract, t_times_bigger, t_power_n, t_context_grains, t_light, t_sqrt])


@skill("Y9.0.d", "Roots, surds and estimating roots", S0)
def _(d=1):
    d = _d(d)

    def t_between():
        n = random.choice([x for x in range(2, 150) if int(x ** 0.5) ** 2 != x])
        lo = int(n ** 0.5)
        return {"prompt": "√%d lies between which two whole numbers? Type them like 4, 5." % n, "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 4, 5"}, "answer": "%d, %d" % (lo, lo + 1), "answer_type": "set",
                "solution": ["%d² = %d and %d² = %d." % (lo, lo * lo, lo + 1, (lo + 1) ** 2)]}

    def t_simplify():
        k, r = random.randint(2, 6), pick([2, 3, 5, 6, 7])
        return _tb("√%d = k√%d. What is k?" % (k * k * r, r), k, "int", {}, ["√%d = √%d × √%d = %d√%d." % (k * k * r, k * k, r, k, r)])

    def t_cube_root():
        k = random.randint(-6, 10)
        return _tb("Work out the cube root of %d." % k ** 3, k, "int", {}, ["%d³ = %d." % (k, k ** 3)])

    def t_higher():
        b, n = pick([(2, 5), (2, 6), (3, 4), (2, 10), (5, 3), (4, 4)])
        return _tb("Work out %d^%d." % (b, n), b ** n, "int", {}, ["= %d." % b ** n])

    def t_root_power():
        b, n = pick([(2, 4), (3, 4), (2, 5), (10, 3)])
        return _tb("What is the %s root of %d?" % ({4: "fourth", 5: "fifth", 3: "cube"}[n], b ** n), b, "int", {}, ["%d^%d = %d." % (b, n, b ** n)])

    def t_exact():
        n = random.choice([x for x in range(2, 60) if int(x ** 0.5) ** 2 != x])
        return _tb("Give √%d correct to 1 decimal place." % n, round(n ** 0.5 + 1e-12, 1), "num", {}, ["√%d ≈ %.3f." % (n, n ** 0.5)], tol=0.05)

    def t_surd_mult():
        r, k = pick([2, 3, 5, 7]), random.randint(2, 4)
        return _tb("Work out √%d × √%d." % (r, r * k * k), r * k, "int", {}, ["√%d = √%d × √%d = %d." % (r * r * k * k, r * r, k * k, r * k)])

    def t_surd_add():
        r = pick([2, 3, 5])
        p, q = random.randint(1, 4), random.randint(2, 5)
        return _tb("√%d + √%d = k√%d. What is k?" % (p * p * r, q * q * r, r), p + q, "int", {},
                   ["√%d = %s√%d and √%d = %d√%d." % (p * p * r, "" if p == 1 else p, r, q * q * r, q, r), "%d + %d = %d." % (p, q, p + q)])

    def t_surd_square():
        k, r = random.randint(2, 6), pick([2, 3, 5, 7])
        return _tb("Work out (%d√%d)²." % (k, r), k * k * r, "int", {}, ["%d² × (√%d)² = %d × %d = %d." % (k, r, k * k, r, k * k * r)])

    def t_nearest():
        n = random.choice([x for x in range(10, 200) if int(x ** 0.5) ** 2 != x])
        return _tb("Estimate √%d to the nearest whole number." % n, int(n ** 0.5 + 0.5), "int", {},
                   ["%d² = %d and %d² = %d; %d is nearer %d." % (int(n ** 0.5), int(n ** 0.5) ** 2, int(n ** 0.5) + 1,
                                                               (int(n ** 0.5) + 1) ** 2, n, int(n ** 0.5 + 0.5) ** 2)])

    def t_cube_between():
        n = random.choice([x for x in range(10, 400) if round(x ** (1 / 3)) ** 3 != x])
        lo = int(round(n ** (1 / 3)))
        if lo ** 3 > n:
            lo -= 1
        return {"prompt": "The cube root of %d lies between which two whole numbers? Type them like 4, 5." % n, "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 4, 5"}, "answer": "%d, %d" % (lo, lo + 1), "answer_type": "set",
                "solution": ["%d³ = %d and %d³ = %d." % (lo, lo ** 3, lo + 1, (lo + 1) ** 3)]}

    def t_on_line():
        n = random.choice([x for x in range(2, 30) if int(x ** 0.5) ** 2 != x])
        lo = int(n ** 0.5)
        return _nld("Mark √%d on the number line (to the nearest tenth)." % n, round(n ** 0.5 + 1e-12, 1), lo, lo + 1, 0.1, 0.5,
                    ["√%d ≈ %.2f." % (n, n ** 0.5)])

    def t_mixed():
        k = random.randint(2, 6)
        return _tb("Work out √%d + ∛%d." % ((k + 1) ** 2, k ** 3), k + 1 + k, "int", {}, ["√%d = %d, ∛%d = %d." % ((k + 1) ** 2, k + 1, k ** 3, k)])

    return _pick_t([t_between, t_simplify, t_cube_root, t_higher, t_root_power, t_exact, t_surd_mult, t_surd_add, t_surd_square,
                    t_nearest, t_cube_between, t_mixed], [t_on_line])


# ================================================================== 9.1 ======
@skill("Y9.1.a", "Expand double brackets", S1)
def _(d=1):
    d = _d(d)
    lo, hi = _by(d, 1, -9, -12), _by(d, 9, 9, 12)
    p, q = [random.choice([v for v in range(lo, hi + 1) if v]) for _ in range(2)]

    def t_expand():
        return _wq("Expand and simplify %s%s (like x^2+5x+6)." % (_bracket(p), _bracket(q)), _poly(p + q, p * q),
                   ["x² + %dx + %dx + %d." % (p, q, p * q), "= %s." % _poly(p + q, p * q)], "e.g. x^2+5x+6")

    def t_coef():
        return _tb("Expand %s%s. What is the coefficient of x?" % (_bracket(p), _bracket(q)), p + q, "int", {},
                   ["%d + %d = %d." % (p, q, p + q)])

    def t_const():
        return _tb("Expand %s%s. What is the constant term?" % (_bracket(p), _bracket(q)), p * q, "int", {}, ["%d × %d = %d." % (p, q, p * q)])

    def t_square():
        return _wq("Expand %s² (like x^2+6x+9)." % _bracket(p), _poly(2 * p, p * p), ["%s%s = %s." % (_bracket(p), _bracket(p), _poly(2 * p, p * p))],
                   "e.g. x^2+6x+9")

    def t_coef2():
        a = random.randint(2, 4)
        return _tb("Expand (%dx%s%d)(x%s%d). What is the coefficient of x?" % (a, "+" if p >= 0 else "-", abs(p), "+" if q >= 0 else "-", abs(q)),
                   a * q + p, "int", {}, ["%dx × %d + %d × x = %dx." % (a, q, p, a * q + p)])

    def t_value():
        x = random.randint(2, 6)
        return _tb("Find the value of %s%s when x = %d." % (_bracket(p), _bracket(q), x), (x + p) * (x + q), "int", {},
                   ["(%d) × (%d) = %d." % (x + p, x + q, (x + p) * (x + q))])

    return _pick_t([t_expand, t_coef, t_const, t_square, t_coef2, t_value])


@skill("Y9.1.b", "Factorise quadratics and the difference of two squares", S1)
def _(d=1):
    d = _d(d)
    p, q = random.randint(_by(d, 1, -8, -10), 9), random.randint(_by(d, 1, -8, -10), 9)
    while p == 0 or q == 0 or p == -q:          # x² − k² belongs to the difference-of-two-squares template
        p, q = random.randint(1, 9), random.randint(-8, 9)

    def t_factorise():
        lo, hi = sorted([p, q])
        return _wq("Factorise %s. Write it like (x+2)(x+3), smaller number first." % _poly(p + q, p * q),
                   "%s%s" % (_bracket(lo), _bracket(hi)), ["Two numbers that multiply to %d and add to %d: %d and %d." % (p * q, p + q, lo, hi)],
                   "e.g. (x+2)(x+3)")

    def t_pair():
        return {"prompt": "Find two numbers that multiply to %d and add to %d. Type them like -2, 5." % (p * q, p + q), "component": "number",
                "spec": {"text": True, "placeholder": "e.g. -2, 5"}, "answer": "%d, %d" % tuple(sorted([p, q])), "answer_type": "set",
                "solution": ["%d × %d = %d; %d + %d = %d." % (p, q, p * q, p, q, p + q)]}

    def t_dots():
        k = random.randint(2, 12)
        return _wq("Factorise x^2-%d (like (x+3)(x-3))." % (k * k), "(x+%d)(x-%d)" % (k, k), ["Difference of two squares: x² − %d²." % k],
                   "e.g. (x+3)(x-3)")

    def t_solve():
        lo, hi = sorted([p, q])
        roots = sorted([-p, -q])
        return {"prompt": "Solve %s = 0. Type both answers like -3, 2." % _poly(p + q, p * q), "component": "number",
                "spec": {"text": True, "placeholder": "e.g. -3, 2"}, "answer": "%d, %d" % tuple(roots), "answer_type": "set",
                "solution": ["%s%s = 0." % (_bracket(lo), _bracket(hi)), "x = %d or x = %d." % tuple(roots)]}

    return _pick_t([t_factorise, t_pair, t_dots, t_solve, _common2])


def _common2():
    while True:
        a, b = random.randint(1, 9), random.randint(1, 9)
        if _g(a, b) == 1:
            break
    k = random.randint(2, 8)
    inner = ("x" if a == 1 else "%dx" % a) + "+%d" % b
    return _wq("Factorise %dx+%d fully (like 3(2x+5))." % (k * a, k * b), "%d(%s)" % (k, inner),
               ["The highest common factor is %d." % k, "%d(%s)." % (k, inner)], "e.g. 3(2x+5)")


@skill("Y9.1.c", "Rearrange formulae to change the subject", S1)
def _(d=1):
    d = _d(d)

    def t_linear():
        m, c = random.randint(2, 9), random.randint(1, 20)
        y = m * random.randint(1, 10) + c
        return _tb("y = %dx + %d. Make x the subject, then find x when y = %d." % (m, c, y), (y - c) // m, "int", {},
                   ["x = (y − %d) ÷ %d." % (c, m), "(%d − %d) ÷ %d = %d." % (y, c, m, (y - c) // m)])

    def t_form():
        kind = pick(["vuat", "perim", "tri"])
        if kind == "vuat":
            u, a, t = random.randint(0, 20), random.randint(2, 9), random.randint(2, 10)
            return _tb("v = u + at. Make a the subject, then find a when v = %d, u = %d and t = %d." % (u + a * t, u, t), a, "int", {},
                       ["a = (v − u) / t.", "(%d − %d) ÷ %d = %d." % (u + a * t, u, t, a)])
        if kind == "perim":
            l, w = random.randint(3, 20), random.randint(2, 15)
            return _tb("P = 2l + 2w. Make w the subject, then find w when P = %d and l = %d." % (2 * l + 2 * w, l), w, "int", {},
                       ["w = (P − 2l) / 2.", "(%d − %d) ÷ 2 = %d." % (2 * l + 2 * w, 2 * l, w)])
        b, h = random.randint(2, 12) * 2, random.randint(2, 15)
        return _tb("A = bh/2. Make h the subject, then find h when A = %d and b = %d." % (b * h // 2, b), h, "int", {},
                   ["h = 2A / b.", "2 × %d ÷ %d = %d." % (b * h // 2, b, h)])

    def t_speed():
        s, t = random.randint(20, 80), random.randint(2, 6)
        return _tb("d = st. Make t the subject and find t when d = %d and s = %d." % (s * t, s), t, "int", {}, ["t = d ÷ s = %d." % t])

    def t_square():
        r = random.randint(2, 12)
        return _tb("A = r². Make r the subject and find r when A = %d (r is positive)." % (r * r), r, "int", {}, ["r = √A = %d." % r])

    def t_temp():
        c = pick([0, 10, 20, 25, 30, 35, 40, 100])
        f = c * 9 // 5 + 32
        return _tb("F = 9C/5 + 32. Rearrange to find C when F = %d." % f, c, "int", {}, ["C = 5(F − 32)/9 = %d." % c])

    def t_volume():
        l, w, h = random.randint(2, 9), random.randint(2, 9), random.randint(2, 12)
        return _tb("V = lwh. Make h the subject, then find h when V = %d, l = %d and w = %d." % (l * w * h, l, w), h, "int", {},
                   ["h = V / (lw).", "%d ÷ %d = %d." % (l * w * h, l * w, h)])

    def t_circle():
        r = random.randint(2, 20)
        return _tb("C = 2πr. Make r the subject, then find r when C = %dπ." % (2 * r), r, "int", {}, ["r = C / (2π).", "%dπ ÷ 2π = %d." % (2 * r, r)])

    def t_which():
        a, b = random.randint(2, 9), random.randint(2, 9)
        right = "x = (y − %d) / %d" % (a, b)
        wrong = pick(["x = y/%d − %d" % (b, a), "x = %dy − %d" % (b, a), "x = (y + %d) / %d" % (a, b)])
        opts = [right, wrong]
        random.shuffle(opts)
        return _wq("Make x the subject of y = %dx + %d. Which is correct?  A: %s   B: %s  (type A or B)" % (b, a, opts[0], opts[1]),
                   "A" if opts[0] == right else "B", ["Subtract %d, then divide by %d: %s." % (a, b, right)], "A / B")

    def t_suvat():
        u, a = random.randint(0, 6), random.randint(1, 4)
        s = random.randint(1, 12)
        v2 = u * u + 2 * a * s
        return _tb("v² = u² + 2as. Make s the subject, then find s when v² = %d, u = %d and a = %d." % (v2, u, a), s, "int", {},
                   ["s = (v² − u²) / 2a.", "(%d − %d) ÷ %d = %d." % (v2, u * u, 2 * a, s)])

    def t_interest():
        P, R, T = random.randint(2, 20) * 100, pick([2, 4, 5, 10]), random.randint(2, 6)
        return _tb("Simple interest I = PRT/100. Make T the subject, then find T when I = %d, P = %d and R = %d." % (P * R * T // 100, P, R), T,
                   "int", {"unit": "years"}, ["T = 100I / (PR).", "100 × %d ÷ (%d × %d) = %d." % (P * R * T // 100, P, R, T)])

    def t_fraction_form():
        k, c = random.randint(2, 6), random.randint(1, 9)
        x = random.randint(1, 12)
        return _tb("y = x/%d − %d. Make x the subject, then find x when y = %s." % (k, c, _ds(Fraction(x, k) - c)), x, "int", {},
                   ["x = %d(y + %d)." % (k, c), "%d × (%s + %d) = %d." % (k, _ds(Fraction(x, k) - c), c, x)]) \
            if Fraction(x, k).denominator == 1 else \
            _tb("y = x/%d − %d. Make x the subject, then find x when y = %d." % (k, c, x), k * (x + c), "int", {},
                ["x = %d(y + %d)." % (k, c), "%d × (%d + %d) = %d." % (k, x, c, k * (x + c))])

    return _pick_t([t_linear, t_form, t_speed, t_square, t_temp, t_volume, t_circle, t_which, t_suvat, t_interest, t_fraction_form])


@skill("Y9.1.d", "Indices in algebra", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(2, 9), random.randint(2, 9)

    def t_mult():
        return _tb("Simplify x^%d × x^%d. What is the power?" % (a, b), a + b, "int", {}, ["Add powers."])

    def t_div():
        return _tb("Simplify x^%d ÷ x^%d. What is the power?" % (a + b, b), a, "int", {}, ["Subtract powers."])

    def t_pow():
        return _tb("Simplify (x^%d)^%d. What is the power?" % (a, b), a * b, "int", {}, ["Multiply powers."])

    def t_coef():
        p, q = random.randint(2, 6), random.randint(2, 6)
        return _wq("Simplify %dx^%d × %dx^%d (like 6x^5)." % (p, a, q, b), "%dx^%d" % (p * q, a + b), ["Multiply numbers, add powers."], "e.g. 6x^5")

    def t_bracket_pow():
        p = random.randint(2, 4)
        return _wq("Simplify (%dx^%d)^2 (like 9x^6)." % (p, a), "%dx^%d" % (p * p, 2 * a), ["Square the number and double the power."], "e.g. 9x^6")

    def t_divide_terms():
        p, q = random.randint(2, 6), random.randint(2, 6)
        return _wq("Simplify %dx^%d ÷ %dx^%d (like 3x^2)." % (p * q, a + b, q, b), "%dx^%d" % (p, a) if a != 1 else "%dx" % p,
                   ["Divide numbers, subtract powers."], "e.g. 3x^2")

    def t_neg_result():
        return _tb("Simplify x^%d ÷ x^%d. What is the power of x?" % (b, a + b), -a, "int", {}, ["%d − %d = %d." % (b, a + b, -a)])

    def t_zero():
        return _tb("Simplify y^%d ÷ y^%d. What is the power of y?" % (a, a), 0, "int", {}, ["%d − %d = 0, and y^0 = 1." % (a, a)])

    def t_two_letters():
        p, q, r, s = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
        return _tb("Simplify a^%d b^%d × a^%d b^%d. What is the power of b?" % (p, q, r, s), q + s, "int", {},
                   ["Add the powers of each letter separately: b^%d." % (q + s)])

    def t_solve():
        bb = pick([2, 3, 5])
        k = random.randint(1, 3)
        x = random.randint(2, 6)
        return _tb("%d^x × %d^%d = %d^%d. Find x." % (bb, bb, k, bb, x + k), x, "int", {}, ["x + %d = %d." % (k, x + k), "x = %d." % x])

    def t_evaluate():
        v = random.randint(2, 5)
        return _tb("Simplify x^%d ÷ x^%d, then find its value when x = %d." % (a + 2, a, v), v * v, "int", {},
                   ["x^%d ÷ x^%d = x²." % (a + 2, a), "%d² = %d." % (v, v * v)])

    def t_neg_coef():
        p, n = random.randint(2, 3), pick([2, 3])
        return _tb("Expand (−%dx^%d)^%d. What is the number in front of x?" % (p, a, n), (-p) ** n, "int", {},
                   ["(−%d)^%d = %d." % (p, n, (-p) ** n), "The power of x becomes %d." % (a * n)])

    def t_quotient_two():
        p, q = random.randint(2, 5), random.randint(1, 4)
        return _tb("Simplify %dx^%dy^%d ÷ %dx^%dy. What is the power of x?" % (6 * p, a + 3, q + 1, 3 * p, 3), a, "int", {},
                   ["%d ÷ %d = 2; x^%d ÷ x^3 = x^%d; y^%d ÷ y = y^%d." % (6 * p, 3 * p, a + 3, a, q + 1, q)])

    return _pick_t([t_mult, t_div, t_pow, t_coef, t_bracket_pow, t_divide_terms, t_neg_result, t_zero, t_two_letters, t_solve, t_evaluate,
                    t_neg_coef, t_quotient_two])


@skill("Y9.1.e", "Algebraic fractions and expressions with fractions", S1)
def _(d=1):
    d = _d(d)

    def t_add():
        a, b = random.randint(2, 5), random.randint(2, 5)
        if a == b:
            b += 1
        return _wq("Write x/%d + x/%d as a single fraction (like 5x/6)." % (a, b), "%dx/%d" % (a + b, a * b) if _g(a + b, a * b) == 1
                   else "%dx/%d" % ((a + b) // _g(a + b, a * b), a * b // _g(a + b, a * b)),
                   ["Common denominator %d." % (a * b)], "e.g. 5x/6")

    def t_cancel():
        k, p = random.randint(2, 6), random.randint(2, 9)
        return _wq("Simplify %dx/%d (like 3x)." % (k * p, k), "%dx" % p, ["%d ÷ %d = %d." % (k * p, k, p)], "e.g. 3x")

    def t_sub_k():
        a, b = sorted(random.sample([2, 3, 4, 5, 6, 8], 2))
        return _fq("x/%d − x/%d = kx. What is k, as a fraction?" % (a, b), Fraction(1, a) - Fraction(1, b),
                   ["Common denominator %d: %dx/%d − %dx/%d." % (a * b // _g(a, b), b // _g(a, b), a * b // _g(a, b), a // _g(a, b), a * b // _g(a, b)),
                    "k = %s." % _fs(Fraction(1, a) - Fraction(1, b))])

    def t_add_k():
        a, b = random.sample([2, 3, 4, 5, 7], 2)
        p = random.randint(1, 3)
        return _fq("%s/%d + x/%d = kx. What is k, as a fraction?" % ("x" if p == 1 else "%dx" % p, a, b), Fraction(p, a) + Fraction(1, b),
                   ["k = %d/%d + 1/%d = %s." % (p, a, b, _fs(Fraction(p, a) + Fraction(1, b)))])

    def t_multiply():
        p, q = random.randint(2, 6), random.randint(2, 6)
        return _tb("Simplify (%dx/%d) × (%d/x)." % (p, q, 2 * q), 2 * p, "int", {}, ["The x's cancel: %d × %d ÷ %d = %d." % (p, 2 * q, q, 2 * p)])

    def t_divide():
        a = pick([2, 3, 4, 5])
        k = random.randint(2, 5)
        return _tb("Simplify (x/%d) ÷ (x/%d)." % (a, a * k), k, "int", {}, ["Multiply by the reciprocal: x/%d × %d/x = %d." % (a, a * k, k)])

    def t_factor_cancel():
        k = random.randint(2, 9)
        return _tb("(x² + %dx)/x simplifies to x + k. What is k?" % k, k, "int", {}, ["Factorise the top: x(x + %d)." % k, "Cancel x: x + %d." % k])

    def t_quad_cancel():
        p, q = random.sample(range(1, 9), 2)
        return _tb("(x² + %dx + %d)/(x + %d) simplifies to x + k. What is k?" % (p + q, p * q, p), q, "int", {},
                   ["x² + %dx + %d = (x + %d)(x + %d)." % (p + q, p * q, p, q), "Cancel (x + %d): x + %d." % (p, q)])

    def t_solve_linear_frac():
        a, k = random.randint(1, 3), random.randint(4, 6)
        x, c = random.randint(1, 12), random.randint(-4, 4)
        b = k * (x + c) - a * x
        return _tb("Solve (%sx %s)/%d = x %s." % ("" if a == 1 else a, ("+ %d" % b) if b >= 0 else ("− %d" % -b), k,
                                                   ("+ %d" % c) if c >= 0 else ("− %d" % -c)), x, "int", {},
                   ["Multiply by %d: %sx %s %d = %dx %s %d." % (k, "" if a == 1 else a, "+" if b >= 0 else "−", abs(b), k,
                                                                 "+" if k * c >= 0 else "−", abs(k * c)),
                    "x = %d." % x])

    def t_substitute():
        x = random.randint(3, 12)
        k = random.choice([v for v in range(1, x) if (x + 6) % v == 0 and v != x])
        return _tb("Find the value of (x + 6)/(x − %d) when x = %d." % (x - k, x), (x + 6) // k, "int", {},
                   ["(%d + 6) ÷ (%d − %d) = %d ÷ %d = %d." % (x, x, x - k, x + 6, k, (x + 6) // k)])

    return _pick_t([_solve_frac, t_add, t_cancel, t_sub_k, t_add_k, t_multiply, t_divide, t_factor_cancel, t_quad_cancel,
                    t_solve_linear_frac, t_substitute])


def _g(a, b):
    while b:
        a, b = b, a % b
    return a


def _solve_frac():
    k, x = random.randint(2, 9), random.randint(1, 12)
    c = random.randint(1, 10)
    rhs = Fraction(x + c, k)
    if rhs.denominator != 1:
        x += k - (x + c) % k
        rhs = Fraction(x + c, k)
    return _tb("Solve (x + %d)/%d = %d." % (c, k, rhs), x, "int", {}, ["x + %d = %d." % (c, rhs * k), "x = %d." % x])
