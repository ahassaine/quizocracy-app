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

    return _pick_t([t_zero, t_neg, t_neg_decimal, t_frac_neg, t_which_power, t_laws])


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
        q = Decimal(a * b) * Decimal(10) ** m / (Decimal(b) * Decimal(10) ** n)
        return _wq("Work out (%dx10^%d) ÷ (%dx10^%d). Give your answer in standard form." % (a * b, m, b, n), _sf(q)[0],
                   ["%d ÷ %d = %d; powers %d − %d = %d." % (a * b, b, a, m, n, m - n)], "e.g. 4x10^3")

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

    return _pick_t([t_mult, t_div, t_add, t_square])


@skill("Y9.0.d", "Roots, surds and estimating roots", S0)
def _(d=1):
    d = _d(d)

    def t_between():
        n = random.choice([x for x in range(2, 150) if int(x ** 0.5) ** 2 != x])
        lo = int(n ** 0.5)
        return _wq("√%d lies between which two whole numbers? Write them like 4 and 5." % n, "%d and %d" % (lo, lo + 1),
                   ["%d² = %d and %d² = %d." % (lo, lo * lo, lo + 1, (lo + 1) ** 2)], "e.g. 4 and 5")

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

    return _pick_t([t_between, t_simplify, t_cube_root, t_higher, t_root_power, t_exact])


# ================================================================== 9.1 ======
@skill("Y9.1.a", "Expand double brackets", S1)
def _(d=1):
    d = _d(d)
    p, q = random.randint(_by(d, 1, -9, -12), _by(d, 9, 9, 12)), random.randint(_by(d, 1, -9, -12), _by(d, 9, 9, 12))

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
    while p == 0 or q == 0:
        p, q = random.randint(1, 9), random.randint(-8, 9)

    def t_factorise():
        lo, hi = sorted([p, q])
        return _wq("Factorise %s. Write it like (x+2)(x+3), smaller number first." % _poly(p + q, p * q),
                   "%s%s" % (_bracket(lo), _bracket(hi)), ["Two numbers that multiply to %d and add to %d: %d and %d." % (p * q, p + q, lo, hi)],
                   "e.g. (x+2)(x+3)")

    def t_pair():
        return _wq("Find two numbers that multiply to %d and add to %d. Write the smaller first, like -2, 5." % (p * q, p + q),
                   "%d, %d" % tuple(sorted([p, q])), ["%d × %d = %d; %d + %d = %d." % (p, q, p * q, p, q, p + q)], "e.g. -2, 5")

    def t_dots():
        k = random.randint(2, 12)
        return _wq("Factorise x^2-%d (like (x+3)(x-3))." % (k * k), "(x+%d)(x-%d)" % (k, k), ["Difference of two squares: x² − %d²." % k],
                   "e.g. (x+3)(x-3)")

    def t_solve():
        lo, hi = sorted([p, q])
        roots = sorted([-p, -q])
        return _wq("Solve %s = 0. Write both answers, smaller first, like -3, 2." % _poly(p + q, p * q), "%d, %d" % tuple(roots),
                   ["%s%s = 0." % (_bracket(lo), _bracket(hi)), "x = %d or x = %d." % tuple(roots)], "e.g. -3, 2")

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

    return _pick_t([t_linear, t_form, t_speed, t_square, t_temp])


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

    return _pick_t([t_mult, t_div, t_pow, t_coef, t_bracket_pow, t_divide_terms])


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

    return _pick_t([_solve_frac, t_add, t_cancel])


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
