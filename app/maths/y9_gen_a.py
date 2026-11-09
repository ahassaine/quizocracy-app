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
    b = random.randint(_by(d, 2, 2, 3), _by(d, 5, 7, 10))
    n = random.randint(_by(d, 1, 1, 2), _by(d, 2, 3, 3))      # hard: never a plain reciprocal

    def t_zero():
        if d == 2:      # hard: a zero power beside a first power
            k = random.randint(2, 30)
            return _tb("Work out %d^0 + %d^1." % (k, k), 1 + k, "int", {}, ["%d^0 = 1 and %d^1 = %d." % (k, k, k), "1 + %d = %d." % (k, 1 + k)])
        return _tb("Work out %d^0." % random.randint(2, _by(d, 20, 999, 999)), 1, "int", {}, ["Any non-zero number to the power 0 is 1."])

    def t_neg():
        return _fq("Work out %d^-%d as a fraction." % (b, n), Fraction(1, b ** n), ["%d^-%d = 1/%d^%d = 1/%d." % (b, n, b, n, b ** n)])

    def t_neg_decimal():
        k = pick(_by(d, [1, 2], [1, 2, 3], [2, 3, 4]))
        if d == 2:      # hard: a multiple of a negative power of 10
            m = random.randint(2, 9)
            v = m * Decimal(1) / 10 ** k
            return _tb("Write %d × 10^-%d as a decimal." % (m, k), _ds(v), "num", {},
                       ["10^-%d = %s." % (k, _ds(Decimal(1) / 10 ** k)), "%d × %s = %s." % (m, _ds(Decimal(1) / 10 ** k), _ds(v))])
        return _tb("Write 10^-%d as a decimal." % k, _ds(Decimal(1) / 10 ** k), "num", {}, ["1/%d = %s." % (10 ** k, _ds(Decimal(1) / 10 ** k))])

    def t_frac_neg():
        if d == 0:      # easy: a unit fraction flips to a whole number
            q = random.randint(2, 9)
            return _fq("Work out (1/%d)^-1." % q, Fraction(q), ["A power of −1 flips the fraction: %d/1 = %d." % (q, q)])
        p, q = random.randint(2, _by(d, 5, 5, 4)), random.randint(2, _by(d, 5, 5, 5))
        if p == q:
            q += 1
        if d == 2:      # hard: a power of −3
            return _fq("Work out (%d/%d)^-3 as a fraction." % (p, q), Fraction(q, p) ** 3,
                       ["Flip the fraction: (%d/%d)^3." % (q, p), "= %d/%d." % (q ** 3, p ** 3)])
        return _fq("Work out (%d/%d)^-1." % (p, q), Fraction(q, p), ["A power of −1 flips the fraction: %d/%d." % (q, p)])

    def t_which_power():
        return _tb("%d^? = 1/%d. What is the power?" % (b, b ** n), -n, "int", {}, ["1/%d = %d^-%d." % (b ** n, b, n)])

    def t_laws():
        if d == 0:      # easy: one negative power, multiplying
            a1, a2 = random.randint(1, 6), random.randint(-3, -1)
        else:
            a1, a2 = random.randint(-4, 6), random.randint(-6, 4)
        if d == 2:      # hard: dividing, so subtract a possibly negative power
            return _tb("Simplify x^%d ÷ x^%d. What is the power of x?" % (a1, a2), a1 - a2, "int", {},
                       ["Subtract the powers: %d − (%d) = %d." % (a1, a2, a1 - a2)])
        return _tb("Simplify x^%d × x^%d. What is the power of x?" % (a1, a2), a1 + a2, "int", {}, ["Add the powers: %d + (%d) = %d." % (a1, a2, a1 + a2)])

    def t_frac_neg_sq():
        p, q = pick(_by(d, [(1, 2), (1, 3), (1, 4), (1, 5)], [(2, 3), (3, 4), (2, 5), (3, 5), (1, 2), (1, 3)],
                        [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (2, 7), (3, 7), (5, 6)]))
        return _fq("Work out (%d/%d)^-2 as a fraction." % (p, q), Fraction(q * q, p * p),
                   ["Flip the fraction: (%d/%d)^2." % (q, p), "= %d/%d." % (q * q, p * p)])

    def t_sum():
        k = pick([2, 3]) if d < 2 else pick([2, 3, 4, 5])
        if d == 0:      # easy: a reciprocal plus a zero power
            return _fq("Work out %d^-1 + %d^0 as a single fraction." % (k, k), Fraction(1, k) + 1,
                       ["1/%d + 1." % k, "= %s." % _fs(Fraction(1, k) + 1)])
        if d == 2:      # hard: two different bases
            j = pick([x for x in (2, 3, 4, 5) if x != k])
            v = Fraction(1, k) + Fraction(1, j * j)
            return _fq("Work out %d^-1 + %d^-2 as a single fraction." % (k, j), v,
                       ["1/%d + 1/%d." % (k, j * j), "= %s." % _fs(v)])
        return _fq("Work out %d^-1 + %d^-2 as a single fraction." % (k, k), Fraction(1, k) + Fraction(1, k * k),
                   ["1/%d + 1/%d." % (k, k * k), "= %s." % _fs(Fraction(1, k) + Fraction(1, k * k))])

    def t_power_of_ten():
        k = random.randint(_by(d, 1, 1, 4), _by(d, 3, 5, 8))
        return _tb("Write %s as a power of 10. What is the power?" % _ds(Decimal(1) / 10 ** k), -k, "int", {},
                   ["%s = 1/%s = 10^-%d." % (_ds(Decimal(1) / 10 ** k), _c(10 ** k), k)])

    def t_decimal_base():
        bb, e = pick(_by(d, [(2, 1), (4, 1), (5, 1), (10, 1)], [(2, 1), (4, 1), (5, 1), (8, 1)],
                         [(2, 2), (2, 3), (4, 2), (5, 2), (20, 2), (5, 3)]))
        v = Fraction(1, bb ** e)
        return _tb("Work out %d^-%d as a decimal." % (bb, e), _ds(v), "num", {},
                   ["1/%d = %s." % (bb ** e, _ds(v))] if e == 1 else
                   ["%d^-%d = 1/%d^%d = 1/%d." % (bb, e, bb, e, bb ** e), "= %s." % _ds(v)])

    def t_spot():
        return _fq("Sam says %d^-%d = −%d. What is the correct value, as a fraction?" % (b, n, b ** n), Fraction(1, b ** n),
                   ["A negative power means a reciprocal, not a negative number.", "%d^-%d = 1/%d." % (b, n, b ** n)])

    def t_mixed_laws():
        bb = pick(_by(d, [2, 10], [2, 3, 5], [2, 3, 5]))
        p, q = random.randint(*_by(d, (-2, -1), (-4, -1), (-6, -3))), random.randint(*_by(d, (2, 4), (2, 5), (1, 4)))
        v = Fraction(bb) ** (p + q)
        return _fq("Work out %d^%d × %d^%d. Give a whole number or a fraction." % (bb, p, bb, q), v,
                   ["Add the powers: %d + %d = %d." % (p, q, p + q), "%d^%d = %s." % (bb, p + q, _fs(v))])

    def t_divide_powers():
        bb = pick(_by(d, [2, 10], [2, 3, 10], [2, 3, 5]))
        # easy: small positive powers; hard: the first power can be zero or negative
        p, q = random.randint(*_by(d, (1, 2), (1, 4), (-2, 2))), random.randint(*_by(d, (3, 4), (5, 7), (3, 5)))
        return _fq("Work out %d^%d ÷ %d^%d as a fraction." % (bb, p, bb, q), Fraction(1, bb ** (q - p)),
                   ["Subtract the powers: %d − %d = %d." % (p, q, p - q), "%d^%d = 1/%d." % (bb, p - q, bb ** (q - p))])

    def t_pattern():
        bb = pick(_by(d, [2, 10], [2, 3, 10], [3, 4, 5]))
        pw = [3, 2, 1, 0, -1, -2] + ([-3] if d == 2 else [])
        rows = [["%d^%d" % (bb, k), _fs(Fraction(bb) ** k)] for k in pw]
        i = random.randint(3, _by(d, 4, 5, 6))
        return _dt("Each row is the one above divided by %d. Complete the table." % bb, ["Power", "Value"], rows,
                   _fs(Fraction(bb) ** pw[i]), ["Keep dividing by %d: %s = %s." % (bb, rows[i][0], rows[i][1])],
                   missing=[i, 1], atype="frac", placeholder="e.g. 1/4")

    return _pick_t([t_zero, t_neg, t_neg_decimal, t_frac_neg, t_which_power, t_laws, t_frac_neg_sq, t_sum, t_power_of_ten,
                    t_decimal_base, t_spot, t_mixed_laws, t_divide_powers], [t_pattern])


@skill("Y9.0.b", "Standard form with negative powers", S0)
def _(d=1):
    d = _d(d)

    def t_small_to_sf():
        # easy: 2 significant figures, few places; stretch: 3 s.f. and up to 9 places (still typeable)
        x = Decimal(random.randint(_by(d, 11, 11, 101), _by(d, 99, 999, 999))) / Decimal(10) ** random.randint(_by(d, 3, 4, 6), _by(d, 5, 8, 9))
        sf, a, e = _sf(x)
        return _wq("Write %s in standard form (like 3.2x10^-4)." % _ds(x), sf, ["Move the point %d places: %s × 10^%d." % (-e, _ds(a), e)],
                   "e.g. 3.2x10^-4")

    def t_sf_to_small():
        a = Decimal(random.randint(_by(d, 2, 11, 101), _by(d, 9, 99, 999))) / _by(d, 1, 10, 100)
        e = -random.randint(_by(d, 1, 2, 4), _by(d, 3, 6, 7))   # 3 s.f. at 10^-7 is 9 places, still typeable
        return _tb("Write %sx10^%d as an ordinary number." % (_ds(a), e), _ds(a * Decimal(10) ** e), "num", {},
                   ["Move the point %s left." % _pl(-e, "place")])

    def t_order():
        # easy: three numbers with different powers; stretch: five, some sharing a power
        k = _by(d, 3, 4, 5)
        while True:
            if d == 0:
                pw = random.sample(range(-6, 7), k)
            else:
                pw = [random.randint(_by(d, -6, -6, -5), _by(d, 6, 6, -1)) for _ in range(k)]
            vals = [Decimal(random.randint(11, 99)) / 10 * Decimal(10) ** p for p in pw]
            if len(set(vals)) == k:
                break
        shown = [_sf(v)[0] for v in vals]
        return _wq("Which is the smallest?  %s  (type it as written)" % ", ".join(shown), shown[vals.index(min(vals))],
                   ["Compare the powers first%s." % ("; if two powers match, compare the numbers in front" if d == 2 else "")], "as written")

    def t_power():
        x = Decimal(random.randint(1, _by(d, 9, 9, 999))) * Decimal(10) ** -random.randint(_by(d, 2, 3, 5), _by(d, 5, 9, 9))
        return _tb("%s written in standard form is A × 10^n. What is n?" % _ds(x), _sf(x)[2], "int", {}, ["Count the places: n = %d." % _sf(x)[2]])

    def t_context():
        thing, x = pick(_by(d, [("the width of a human hair, in metres", Decimal("0.00008")),
                                ("the mass of a grain of sand, in grams", Decimal("0.0006"))],
                            [("the width of a human hair, in metres", Decimal("0.00008")),
                             ("the mass of a grain of sand, in grams", Decimal("0.0006")),
                             ("the diameter of a red blood cell, in metres", Decimal("0.000007"))],
                            [("the diameter of a virus, in metres", Decimal("0.00000012")),
                             ("the wavelength of red light, in metres", Decimal("0.00000068")),
                             ("the mass of a mosquito, in kilograms", Decimal("0.0000025"))]))
        return _wq("Write %s, %s, in standard form (like 3.2x10^-4)." % (thing, _ds(x)), _sf(x)[0], ["= %s." % _sf(x)[0]], "e.g. 3.2x10^-4")

    return _pick_t([t_small_to_sf, t_sf_to_small, t_order, t_power, t_context])


@skill("Y9.0.c", "Calculate with numbers in standard form", S0)
def _(d=1):
    d = _d(d)
    # easy: products under 10 and positive powers; stretch: products that need re-normalising and negative powers
    if d == 0:
        a = random.randint(2, 4)
        b = random.randint(2, 9 // a)
    else:
        a, b = random.randint(_by(d, 2, 2, 3), 9), random.randint(_by(d, 2, 2, 3), 9)
    m, n = random.randint(_by(d, 1, -5, -9), _by(d, 6, 8, 9)), random.randint(_by(d, 1, -5, -9), _by(d, 6, 8, 9))

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
        # easy: same power, no carry; core: powers one apart; stretch: powers two apart
        e = random.randint(3, _by(d, 6, 6, 8))
        gap = _by(d, 0, 1, 2)
        p, q = (random.randint(1, 5), random.randint(1, 4)) if d == 0 else (a, b)
        x, y = Decimal(p) * 10 ** e, Decimal(q) * 10 ** (e - gap)
        return _wq("Work out %s + %s. Give your answer in standard form." % (_sf(x)[0], _sf(y)[0]), _sf(x + y)[0],
                   ["As ordinary numbers: %s + %s = %s." % (_c(int(x)), _c(int(y)), _c(int(x + y)))], "e.g. 4.3x10^5")

    def t_square():
        k = random.randint(_by(d, 1, 2, 4), _by(d, 3, 4, 9))
        e = pick(_by(d, [1, 2, 3], [2, 3, 4, 5], [-4, -3, -2, 3, 4, 5, 6]))
        p = Decimal(k * k) * Decimal(10) ** (2 * e)
        return _wq("Work out (%dx10^%d)². Give your answer in standard form." % (k, e), _sf(p)[0], ["%d² = %d; power × 2." % (k, k * k)],
                   "e.g. 2.5x10^7")

    def t_subtract():
        e = random.randint(3, _by(d, 6, 6, 8))
        gap = _by(d, 0, 1, 2)
        x, y = Decimal(max(a, b)) * 10 ** e, Decimal(min(a, b)) * 10 ** (e - gap)
        if x == y:
            x = Decimal(max(a, b) + 1) * 10 ** e
        return _wq("Work out %s − %s. Give your answer in standard form." % (_sf(x)[0], _sf(y)[0]), _sf(x - y)[0],
                   ["As ordinary numbers: %s − %s = %s." % (_c(int(x)), _c(int(y)), _c(int(x - y)))], "e.g. 4.3x10^5")

    def t_times_bigger():
        e1 = random.randint(_by(d, 4, 5, 4), _by(d, 6, 9, 8))
        # at most 10^6 apart, so the answer stays typeable in full; stretch: the smaller one may have a negative power
        e2 = random.randint(max(_by(d, 1, 1, -2), e1 - 6), min(_by(d, 3, 4, 4), e1 - 1))
        big, small = a * b, b
        return _tb("How many times bigger is %dx10^%d than %dx10^%d?" % (big, e1, small, e2) if big < 10 else
                   "How many times bigger is %s than %dx10^%d?" % (_sf(Decimal(big) * 10 ** e1)[0], small, e2),
                   a * 10 ** (e1 - e2), "int", {}, ["Divide: %d × 10^%d = %s." % (a, e1 - e2, _c(a * 10 ** (e1 - e2)))])

    def t_power_n():
        p = Decimal(a * b) * Decimal(10) ** (m + n)
        return _tb("(%dx10^%d) × (%dx10^%d) = A × 10^n in standard form. What is n?" % (a, m, b, n), _sf(p)[2], "int", {},
                   ["%d × %d = %d, and 10^%d × 10^%d = 10^%d." % (a, b, a * b, m, n, m + n), "%s, so n = %d." % (_sf(p)[0], _sf(p)[2])])

    def t_context_grains():
        mass, cnt = a, b
        pm, pc = _by(d, -2, -4, -random.randint(5, 7)), _by(d, 4, 6, random.randint(7, 9))
        p = Decimal(mass * cnt) * Decimal(10) ** (pm + pc)
        return _wq("A grain of rice has a mass of %dx10^%d kg. What is the mass of %dx10^%d grains, in kg? Give your answer in standard form."
                   % (mass, pm, cnt, pc), _sf(p)[0], ["%d × %d = %d; powers %d + %d = %d." % (mass, cnt, mass * cnt, pm, pc, pm + pc),
                                                      "= %s kg." % _sf(p)[0]],
                   "e.g. 1.2x10^3")

    def t_light():
        dist = pick(_by(d, [(Decimal("6"), 7, 200), (Decimal("1.5"), 8, 500), (Decimal("3"), 8, 1000)],
                        [(Decimal("1.5"), 8, 500), (Decimal("3.9"), 8, 1300), (Decimal("6"), 7, 200), (Decimal("4.5"), 8, 1500)],
                        [(Decimal("3.9"), 8, 1300), (Decimal("1.08"), 9, 3600), (Decimal("2.7"), 9, 9000), (Decimal("7.2"), 7, 240)]))
        return _tb("Light travels 3x10^5 km every second. A distance is %sx10^%d km. How many seconds does light take to cover it?"
                   % (_ds(dist[0]), dist[1]), dist[2], "int", {"unit": "seconds"},
                   ["%sx10^%d ÷ 3x10^5 = %d." % (_ds(dist[0]), dist[1], dist[2])])

    def t_sqrt():
        k = random.randint(_by(d, 2, 2, 4), _by(d, 3, 9, 9))
        e = random.randint(1, _by(d, 3, 5, 5)) * 2
        if d == 2:                                   # stretch: k² ≥ 16 is shown in standard form, so the power is odd
            shown = _sf(Decimal(k * k) * Decimal(10) ** e)[0]
            return _wq("Work out √(%s). Give your answer in standard form." % shown, "%dx10^%d" % (k, e // 2),
                       ["%s = %dx10^%d." % (shown, k * k, e), "√%d = %d and √10^%d = 10^%d." % (k * k, k, e, e // 2)], "e.g. 3x10^4")
        return _wq("Work out √(%dx10^%d). Give your answer in standard form." % (k * k, e), "%dx10^%d" % (k, e // 2),
                   ["√%d = %d and √10^%d = 10^%d." % (k * k, k, e, e // 2)], "e.g. 3x10^4")

    return _pick_t([t_mult, t_div, t_add, t_square, t_subtract, t_times_bigger, t_power_n, t_context_grains, t_light, t_sqrt])


@skill("Y9.0.d", "Roots, surds and estimating roots", S0)
def _(d=1):
    d = _d(d)
    surds = _by(d, [2, 3, 5], [2, 3, 5, 6, 7], [2, 3, 5, 6, 7, 10, 11])

    def t_between():
        n = random.choice([x for x in range(_by(d, 2, 2, 150), _by(d, 50, 150, 400)) if int(x ** 0.5) ** 2 != x])
        lo = int(n ** 0.5)
        return {"prompt": "√%d lies between which two whole numbers? Type them like 4, 5." % n, "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 4, 5"}, "answer": "%d, %d" % (lo, lo + 1), "answer_type": "set",
                "solution": ["%d² = %d and %d² = %d." % (lo, lo * lo, lo + 1, (lo + 1) ** 2)]}

    def t_simplify():
        k, r = random.randint(2, _by(d, 3, 6, 9)), pick(surds)
        return _tb("√%d = k√%d. What is k?" % (k * k * r, r), k, "int", {}, ["√%d = √%d × √%d = %d√%d." % (k * k * r, k * k, r, k, r)])

    def t_cube_root():
        k = random.randint(_by(d, 1, -6, -10), _by(d, 5, 10, 12))
        return _tb("Work out the cube root of %d." % k ** 3, k, "int", {}, ["%d³ = %d." % (k, k ** 3)])

    def t_higher():
        b, n = pick(_by(d, [(2, 4), (2, 5), (10, 3), (3, 3)], [(2, 5), (2, 6), (3, 4), (2, 10), (5, 3), (4, 4)],
                        [(3, 5), (2, 8), (5, 4), (6, 3), (2, 10), (4, 5)]))
        return _tb("Work out %d^%d." % (b, n), b ** n, "int", {}, ["= %d." % b ** n])

    def t_root_power():
        b, n = pick(_by(d, [(2, 4), (10, 3), (2, 5)], [(2, 4), (3, 4), (2, 5), (10, 3)], [(3, 5), (5, 4), (2, 6), (4, 5), (3, 4)]))
        return _tb("What is the %s root of %d?" % ({4: "fourth", 5: "fifth", 3: "cube", 6: "sixth"}[n], b ** n), b, "int", {},
                   ["%d^%d = %d." % (b, n, b ** n)])

    def t_exact():
        n = random.choice([x for x in range(_by(d, 2, 2, 60), _by(d, 30, 60, 200)) if int(x ** 0.5) ** 2 != x])
        return _tb("Give √%d correct to 1 decimal place." % n, round(n ** 0.5 + 1e-12, 1), "num", {}, ["√%d ≈ %.3f." % (n, n ** 0.5)], tol=0.05)

    def t_surd_mult():
        r, k = pick(surds), random.randint(2, _by(d, 2, 4, 6))
        return _tb("Work out √%d × √%d." % (r, r * k * k), r * k, "int", {}, ["√%d = √%d × √%d = %d." % (r * r * k * k, r * r, k * k, r * k)])

    def t_surd_add():
        r = pick(_by(d, [2, 3], [2, 3, 5], [2, 3, 5, 6, 7]))
        p, q = random.randint(1, _by(d, 2, 4, 5)), random.randint(2, _by(d, 3, 5, 7))
        if d == 2 and random.random() < 0.5 and q != p:          # stretch: subtract surds
            p, q = min(p, q), max(p, q)
            return _tb("√%d − √%d = k√%d. What is k?" % (q * q * r, p * p * r, r), q - p, "int", {},
                       ["√%d = %d√%d and √%d = %s√%d." % (q * q * r, q, r, p * p * r, "" if p == 1 else p, r), "%d − %d = %d." % (q, p, q - p)])
        return _tb("√%d + √%d = k√%d. What is k?" % (p * p * r, q * q * r, r), p + q, "int", {},
                   ["√%d = %s√%d and √%d = %d√%d." % (p * p * r, "" if p == 1 else p, r, q * q * r, q, r), "%d + %d = %d." % (p, q, p + q)])

    def t_surd_square():
        k, r = random.randint(2, _by(d, 3, 6, 9)), pick(surds)
        return _tb("Work out (%d√%d)²." % (k, r), k * k * r, "int", {}, ["%d² × (√%d)² = %d × %d = %d." % (k, r, k * k, r, k * k * r)])

    def t_nearest():
        n = random.choice([x for x in range(_by(d, 10, 10, 200), _by(d, 60, 200, 600)) if int(x ** 0.5) ** 2 != x])
        return _tb("Estimate √%d to the nearest whole number." % n, int(n ** 0.5 + 0.5), "int", {},
                   ["%d² = %d and %d² = %d; %d is nearer %d." % (int(n ** 0.5), int(n ** 0.5) ** 2, int(n ** 0.5) + 1,
                                                               (int(n ** 0.5) + 1) ** 2, n, int(n ** 0.5 + 0.5) ** 2)])

    def t_cube_between():
        n = random.choice([x for x in range(_by(d, 10, 10, 130), _by(d, 130, 400, 1000)) if round(x ** (1 / 3)) ** 3 != x])
        lo = int(round(n ** (1 / 3)))
        if lo ** 3 > n:
            lo -= 1
        return {"prompt": "The cube root of %d lies between which two whole numbers? Type them like 4, 5." % n, "component": "number",
                "spec": {"text": True, "placeholder": "e.g. 4, 5"}, "answer": "%d, %d" % (lo, lo + 1), "answer_type": "set",
                "solution": ["%d³ = %d and %d³ = %d." % (lo, lo ** 3, lo + 1, (lo + 1) ** 3)]}

    def t_on_line():
        n = random.choice([x for x in range(2, _by(d, 16, 30, 99)) if int(x ** 0.5) ** 2 != x])
        lo = int(n ** 0.5)
        return _nld("Mark √%d on the number line (to the nearest tenth)." % n, round(n ** 0.5 + 1e-12, 1), lo, lo + 1, 0.1, 0.5,
                    ["√%d ≈ %.2f." % (n, n ** 0.5)])

    def t_mixed():
        k = random.randint(2, _by(d, 3, 6, 9))
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
        return _wq("Expand and simplify %s%s (like x^2+5x-3)." % (_bracket(p), _bracket(q)), _poly(p + q, p * q),
                   ["x² %s %s %s %s %s %d." % ("+" if p > 0 else "−", ("" if abs(p) == 1 else abs(p)) and "%dx" % abs(p) or "x", "+" if q > 0 else "−", ("" if abs(q) == 1 else abs(q)) and "%dx" % abs(q) or "x", "+" if p * q > 0 else "−", abs(p * q)), "= %s." % _poly(p + q, p * q)], "e.g. x^2+5x-3")

    def t_coef():
        return _tb("Expand %s%s. What is the coefficient of x?" % (_bracket(p), _bracket(q)), p + q, "int", {},
                   ["%d + %d = %d." % (p, q, p + q)])

    def t_const():
        return _tb("Expand %s%s. What is the constant term?" % (_bracket(p), _bracket(q)), p * q, "int", {}, ["%d × %d = %d." % (p, q, p * q)])

    def t_square():
        return _wq("Expand %s² (like x^2+5x+4)." % _bracket(p), _poly(2 * p, p * p), ["%s%s = %s." % (_bracket(p), _bracket(p), _poly(2 * p, p * p))],
                   "e.g. x^2+5x+4")

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
        return _wq("Factorise x^2-%d. Write the + bracket first, like (x+20)(x-20)." % (k * k), "(x+%d)(x-%d)" % (k, k), ["Difference of two squares: x² − %d²." % k],
                   "e.g. (x+20)(x-20)")

    def t_solve():
        lo, hi = sorted([p, q])
        roots = sorted([-p, -q])
        if p == q:
            return _tb("Solve %s = 0." % _poly(p + q, p * q), -p, "int", {},
                       ["%s%s = 0." % (_bracket(p), _bracket(p)), "Both brackets give the same answer: x = %d." % -p])
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
        m, c = random.randint(2, _by(d, 5, 9, 9)), random.randint(1, _by(d, 10, 20, 30))
        x = random.randint(1, 10)
        if d == 2 and random.random() < 0.5:            # stretch: a negative x-term, y = c − mx
            y = c - m * x
            return _tb("y = %d − %dx. Make x the subject, then find x when y = %d." % (c, m, y), x, "int", {},
                       ["x = (%d − y) ÷ %d." % (c, m),
                        "(%d − %s) ÷ %d = %d." % (c, ("(−%d)" % -y) if y < 0 else y, m, x)])
        y = m * x + c
        return _tb("y = %dx + %d. Make x the subject, then find x when y = %d." % (m, c, y), (y - c) // m, "int", {},
                   ["x = (y − %d) ÷ %d." % (c, m), "(%d − %d) ÷ %d = %d." % (y, c, m, (y - c) // m)])

    def t_form():
        kind = pick(_by(d, ["vuat", "perim"], ["vuat", "perim", "tri"], ["vuat", "perim", "tri", "trap"]))
        if kind == "vuat":
            u, a, t = random.randint(0, _by(d, 10, 20, 30)), random.randint(2, _by(d, 5, 9, 12)), random.randint(2, _by(d, 5, 10, 12))
            return _tb("v = u + at. Make a the subject, then find a when v = %d, u = %d and t = %d." % (u + a * t, u, t), a, "int", {},
                       ["a = (v − u) / t.", "(%d − %d) ÷ %d = %d." % (u + a * t, u, t, a)])
        if kind == "perim":
            l, w = random.randint(3, _by(d, 10, 20, 40)), random.randint(2, _by(d, 10, 15, 30))
            return _tb("P = 2l + 2w. Make w the subject, then find w when P = %d and l = %d." % (2 * l + 2 * w, l), w, "int", {},
                       ["w = (P − 2l) / 2.", "(%d − %d) ÷ 2 = %d." % (2 * l + 2 * w, 2 * l, w)])
        if kind == "trap":                              # stretch: area of a trapezium
            a, b = random.randint(2, 12), random.randint(2, 12)
            h = random.randint(1, 8) * (1 if (a + b) % 2 == 0 else 2)
            A = (a + b) * h // 2
            return _tb("A = (a + b)h/2. Make h the subject, then find h when A = %d, a = %d and b = %d." % (A, a, b), h, "int", {},
                       ["h = 2A / (a + b).", "2 × %d ÷ %d = %d." % (A, a + b, h)])
        b, h = random.randint(2, 12) * 2, random.randint(2, 15)
        return _tb("A = bh/2. Make h the subject, then find h when A = %d and b = %d." % (b * h // 2, b), h, "int", {},
                   ["h = 2A / b.", "2 × %d ÷ %d = %d." % (b * h // 2, b, h)])

    def t_speed():
        s, t = random.randint(_by(d, 2, 20, 35), _by(d, 9, 80, 95)) * _by(d, 10, 1, 1), random.randint(2, _by(d, 5, 6, 9))
        return _tb("d = st. Make t the subject and find t when d = %d and s = %d." % (s * t, s), t, "int", {}, ["t = d ÷ s = %d." % t])

    def t_square():
        r = random.randint(2, _by(d, 9, 12, 12))
        if d == 2:                                      # stretch: a coefficient to undo before the square root
            k = random.randint(2, 5)
            return _tb("A = %dr². Make r the subject and find r when A = %d (r is positive)." % (k, k * r * r), r, "int", {},
                       ["r = √(A ÷ %d)." % k, "√(%d ÷ %d) = √%d = %d." % (k * r * r, k, r * r, r)])
        return _tb("A = r². Make r the subject and find r when A = %d (r is positive)." % (r * r), r, "int", {}, ["r = √A = %d." % r])

    def t_temp():
        c = pick(_by(d, [0, 10, 20, 100], [0, 10, 20, 25, 30, 35, 40, 100], [-40, -20, -10, 5, 15, 45, 60]))
        f = c * 9 // 5 + 32
        return _tb("F = 9C/5 + 32. Rearrange to find C when F = %d." % f, c, "int", {}, ["C = 5(F − 32)/9 = %d." % c])

    def t_volume():
        l, w, h = random.randint(2, _by(d, 5, 9, 12)), random.randint(2, _by(d, 5, 9, 12)), random.randint(2, _by(d, 6, 12, 15))
        return _tb("V = lwh. Make h the subject, then find h when V = %d, l = %d and w = %d." % (l * w * h, l, w), h, "int", {},
                   ["h = V / (lw).", "%d ÷ %d = %d." % (l * w * h, l * w, h)])

    def t_circle():
        r = random.randint(2, _by(d, 10, 20, 15))
        if d == 2:                                      # stretch: from the area, so a square root as well
            return _tb("A = πr². Make r the subject, then find r when A = %dπ." % (r * r), r, "int", {},
                       ["r = √(A / π).", "√(%dπ ÷ π) = √%d = %d." % (r * r, r * r, r)])
        return _tb("C = 2πr. Make r the subject, then find r when C = %dπ." % (2 * r), r, "int", {}, ["r = C / (2π).", "%dπ ÷ 2π = %d." % (2 * r, r)])

    def t_which():
        a, b = random.randint(2, 9), random.randint(2, 9)
        if d == 2:                                      # stretch: y = (x + a)/b, undo the division first
            right = "x = %dy − %d" % (b, a)
            wrong = pick(["x = %d(y − %d)" % (b, a), "x = y/%d − %d" % (b, a), "x = %dy + %d" % (b, a)])
            q = "y = (x + %d)/%d" % (a, b)
            steps = "Multiply by %d, then subtract %d: %s." % (b, a, right)
        else:
            right = "x = (y − %d) / %d" % (a, b)
            wrong = pick(["x = y/%d − %d" % (b, a), "x = %dy − %d" % (b, a), "x = (y + %d) / %d" % (a, b)])
            q = "y = %dx + %d" % (b, a)
            steps = "Subtract %d, then divide by %d: %s." % (a, b, right)
        opts = [right, wrong]
        random.shuffle(opts)
        return _wq("Make x the subject of %s. Which is correct?  A: %s   B: %s  (type A or B)" % (q, opts[0], opts[1]),
                   "A" if opts[0] == right else "B", [steps], "A / B")

    def t_suvat():
        u, a = random.randint(0, _by(d, 3, 6, 9)), random.randint(1, _by(d, 2, 4, 6))
        s = random.randint(1, _by(d, 6, 12, 20))
        v2 = u * u + 2 * a * s
        return _tb("v² = u² + 2as. Make s the subject, then find s when v² = %d, u = %d and a = %d." % (v2, u, a), s, "int", {},
                   ["s = (v² − u²) / 2a.", "(%d − %d) ÷ %d = %d." % (v2, u * u, 2 * a, s)])

    def t_interest():
        P, R, T = random.randint(2, _by(d, 10, 20, 50)) * 100, pick(_by(d, [5, 10], [2, 4, 5, 10], [2, 3, 4, 6, 8])), random.randint(2, _by(d, 4, 6, 8))
        I = P * R * T // 100
        if d == 2:                                      # stretch: make the rate the subject
            return _tb("Simple interest I = PRT/100. Make R the subject, then find R when I = %d, P = %d and T = %d." % (I, P, T), R,
                       "int", {"unit": "%"}, ["R = 100I / (PT).", "100 × %d ÷ (%d × %d) = %d." % (I, P, T, R)])
        return _tb("Simple interest I = PRT/100. Make T the subject, then find T when I = %d, P = %d and R = %d." % (I, P, R), T,
                   "int", {"unit": "years"}, ["T = 100I / (PR).", "100 × %d ÷ (%d × %d) = %d." % (I, P, R, T)])

    def t_fraction_form():
        k, c = random.randint(2, _by(d, 3, 6, 9)), random.randint(1, _by(d, 5, 9, 15))
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
    a, b = random.randint(2, _by(d, 5, 9, 12)), random.randint(2, _by(d, 5, 9, 12))

    def t_mult():
        return _tb("Simplify x^%d × x^%d. What is the power?" % (a, b), a + b, "int", {}, ["Add powers."])

    def t_div():
        return _tb("Simplify x^%d ÷ x^%d. What is the power?" % (a + b, b), a, "int", {}, ["Subtract powers."])

    def t_pow():
        return _tb("Simplify (x^%d)^%d. What is the power?" % (a, b), a * b, "int", {}, ["Multiply powers."])

    def t_coef():
        p, q = random.randint(2, _by(d, 4, 6, 9)), random.randint(2, _by(d, 4, 6, 9))
        if d == 2 and random.random() < 0.5:            # stretch: a negative coefficient
            p = -p
        return _wq("Simplify %dx^%d × %dx^%d (like 6x^5)." % (p, a, q, b), "%dx^%d" % (p * q, a + b), ["Multiply numbers, add powers."], "e.g. 6x^5")

    def t_bracket_pow():
        p, n = random.randint(2, _by(d, 3, 4, 3)), _by(d, 2, 2, 3)
        if n == 2:
            return _wq("Simplify (%dx^%d)^2 (like 25x^8)." % (p, a), "%dx^%d" % (p * p, 2 * a), ["Square the number and double the power."], "e.g. 25x^8")
        return _wq("Simplify (%dx^%d)^3 (like 8x^12)." % (p, a), "%dx^%d" % (p ** 3, 3 * a), ["Cube the number and multiply the power by 3."], "e.g. 8x^12")

    def t_divide_terms():
        p, q = random.randint(2, _by(d, 4, 6, 9)), random.randint(2, _by(d, 4, 6, 9))
        return _wq("Simplify %dx^%d ÷ %dx^%d (like 3x^2)." % (p * q, a + b, q, b), "%dx^%d" % (p, a) if a != 1 else "%dx" % p,
                   ["Divide numbers, subtract powers."], "e.g. 3x^2")

    def t_neg_result():
        return _tb("Simplify x^%d ÷ x^%d. What is the power of x?" % (b, a + b), -a, "int", {}, ["%d − %d = %d." % (b, a + b, -a)])

    def t_zero():
        return _tb("Simplify y^%d ÷ y^%d. What is the power of y?" % (a, a), 0, "int", {}, ["%d − %d = 0, and y^0 = 1." % (a, a)])

    def t_two_letters():
        p, q, r, s = [random.randint(2, _by(d, 4, 6, 8)) for _ in range(4)]
        if d == 2:                                      # stretch: then divide by a power of b as well
            u = random.randint(1, q + s - 1)
            return _tb("Simplify a^%d b^%d × a^%d b^%d ÷ (a b^%d). What is the power of b?" % (p, q, r, s, u), q + s - u, "int", {},
                       ["Add the powers of b, then subtract: %d + %d − %d = %d." % (q, s, u, q + s - u)])
        return _tb("Simplify a^%d b^%d × a^%d b^%d. What is the power of b?" % (p, q, r, s), q + s, "int", {},
                   ["Add the powers of each letter separately: b^%d." % (q + s)])

    def t_solve():
        bb = pick(_by(d, [2, 3], [2, 3, 5], [2, 3, 5]))
        k = random.randint(1, 3)
        x = random.randint(2, _by(d, 4, 6, 6))
        if d == 2:                                      # stretch: a power of a power on the left
            return _tb("(%d^x)^2 × %d^%d = %d^%d. Find x." % (bb, bb, k, bb, 2 * x + k), x, "int", {},
                       ["2x + %d = %d." % (k, 2 * x + k), "2x = %d, so x = %d." % (2 * x, x)])
        return _tb("%d^x × %d^%d = %d^%d. Find x." % (bb, bb, k, bb, x + k), x, "int", {}, ["x + %d = %d." % (k, x + k), "x = %d." % x])

    def t_evaluate():
        v, g = random.randint(2, _by(d, 3, 5, 4)), _by(d, 2, 2, 3)
        return _tb("Simplify x^%d ÷ x^%d, then find its value when x = %d." % (a + g, a, v), v ** g, "int", {},
                   ["x^%d ÷ x^%d = x^%d." % (a + g, a, g), "%d^%d = %d." % (v, g, v ** g)])

    def t_neg_coef():
        p, n = random.randint(2, 3), pick(_by(d, [2], [2, 3], [3, 4]))
        return _tb("Expand (−%dx^%d)^%d. What is the number in front of x?" % (p, a, n), (-p) ** n, "int", {},
                   ["(−%d)^%d = %d." % (p, n, (-p) ** n), "The power of x becomes %d." % (a * n)])

    def t_quotient_two():
        p, q = random.randint(2, _by(d, 3, 5, 8)), random.randint(1, _by(d, 3, 4, 6))
        return _tb("Simplify %dx^%dy^%d ÷ %dx^%dy. What is the power of x?" % (6 * p, a + 3, q + 1, 3 * p, 3), a, "int", {},
                   ["%d ÷ %d = 2; x^%d ÷ x^3 = x^%d; y^%d ÷ y = y^%d." % (6 * p, 3 * p, a + 3, a, q + 1, q)])

    return _pick_t([t_mult, t_div, t_pow, t_coef, t_bracket_pow, t_divide_terms, t_neg_result, t_zero, t_two_letters, t_solve, t_evaluate,
                    t_neg_coef, t_quotient_two])


@skill("Y9.1.e", "Algebraic fractions and expressions with fractions", S1)
def _(d=1):
    d = _d(d)

    def t_add():
        a, b = random.sample(_by(d, [2, 3, 5], [2, 3, 4, 5], [2, 3, 4, 5, 6, 8, 9]), 2)
        return _wq("Write x/%d + x/%d as a single fraction in its simplest form (like 9x/14)." % (a, b), "%dx/%d" % (a + b, a * b) if _g(a + b, a * b) == 1
                   else "%dx/%d" % ((a + b) // _g(a + b, a * b), a * b // _g(a + b, a * b)),
                   ["Common denominator %d." % (a * b // _g(a, b))], "e.g. 5x/6")

    def t_cancel():
        k, p = random.randint(2, _by(d, 3, 6, 9)), random.randint(2, _by(d, 5, 9, 12))
        return _wq("Simplify %dx/%d (like 3x)." % (k * p, k), "%dx" % p, ["%d ÷ %d = %d." % (k * p, k, p)], "e.g. 3x")

    def t_sub_k():
        a, b = sorted(random.sample(_by(d, [2, 3, 4], [2, 3, 4, 5, 6, 8], [3, 4, 5, 6, 8, 9, 10, 12]), 2))
        return _fq("x/%d − x/%d = kx. What is k, as a fraction?" % (a, b), Fraction(1, a) - Fraction(1, b),
                   ["Common denominator %d: %dx/%d − %dx/%d." % (a * b // _g(a, b), b // _g(a, b), a * b // _g(a, b), a // _g(a, b), a * b // _g(a, b)),
                    "k = %s." % _fs(Fraction(1, a) - Fraction(1, b))])

    def t_add_k():
        a, b = random.sample(_by(d, [2, 3, 4], [2, 3, 4, 5, 7], [3, 4, 5, 6, 7, 9]), 2)
        p = random.randint(1, _by(d, 1, 3, 5))
        return _fq("%s/%d + x/%d = kx. What is k, as a fraction?" % ("x" if p == 1 else "%dx" % p, a, b), Fraction(p, a) + Fraction(1, b),
                   ["k = %d/%d + 1/%d = %s." % (p, a, b, _fs(Fraction(p, a) + Fraction(1, b)))])

    def t_multiply():
        p, q = random.randint(2, _by(d, 3, 6, 9)), random.randint(2, _by(d, 3, 6, 9))
        k = _by(d, 2, 2, random.randint(3, 5))
        return _tb("Simplify (%dx/%d) × (%d/x)." % (p, q, k * q), k * p, "int", {}, ["The x's cancel: %d × %d ÷ %d = %d." % (p, k * q, q, k * p)])

    def t_divide():
        a = pick(_by(d, [2, 3], [2, 3, 4, 5], [2, 3, 4, 5, 6]))
        k = random.randint(2, _by(d, 3, 5, 6))
        c = _by(d, 1, 1, pick([v for v in range(2, 8) if _g(v, a) == 1]))   # stretch: a coefficient on the first x
        return _tb("Simplify (%sx/%d) ÷ (x/%d)." % ("" if c == 1 else c, a, a * k), c * k, "int", {},
                   ["Multiply by the reciprocal: %sx/%d × %d/x = %d." % ("" if c == 1 else c, a, a * k, c * k)])

    def t_factor_cancel():
        k = random.randint(2, _by(d, 5, 9, 9))
        if d == 2:                                      # stretch: a common factor in front as well
            c = random.randint(2, 5)
            return _tb("(%dx² + %dx)/(%dx) simplifies to x + k. What is k?" % (c, c * k, c), k, "int", {},
                       ["Factorise the top: %dx(x + %d)." % (c, k), "Cancel %dx: x + %d." % (c, k)])
        return _tb("(x² + %dx)/x simplifies to x + k. What is k?" % k, k, "int", {}, ["Factorise the top: x(x + %d)." % k, "Cancel x: x + %d." % k])

    def t_quad_cancel():
        if d == 2:                                      # stretch: negative numbers in the brackets
            p, q = random.sample([v for v in range(-9, 10) if v], 2)

            def sp(t):
                return t.replace("^2", "²").replace("+", " + ").replace("-", " − ")
            top = sp(_poly(p + q, p * q))
            return _tb("(%s)/%s simplifies to x + k. What is k?" % (top, sp(_bracket(p))), q, "int", {},
                       ["%s = %s%s." % (top, sp(_bracket(p)), sp(_bracket(q))), "Cancel %s: k = %d." % (sp(_bracket(p)), q)])
        p, q = random.sample(range(1, _by(d, 6, 9, 9)), 2)
        return _tb("(x² + %dx + %d)/(x + %d) simplifies to x + k. What is k?" % (p + q, p * q, p), q, "int", {},
                   ["x² + %dx + %d = (x + %d)(x + %d)." % (p + q, p * q, p, q), "Cancel (x + %d): x + %d." % (p, q)])

    def t_solve_linear_frac():
        a, k = random.randint(1, _by(d, 1, 3, 3)), random.randint(_by(d, 2, 4, 5), _by(d, 3, 6, 9))
        x, c = random.randint(1, 12), random.choice(_by(d, [1, 2, 3, 4], [-4, -3, -2, -1, 1, 2, 3, 4], [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]))
        b = k * (x + c) - a * x
        ax = "%sx" % ("" if a == 1 else a)
        num = ("%s %s %d" % (ax, "+" if b > 0 else "−", abs(b))) if b else ax
        return _tb("Solve %s/%d = x %s." % (("(%s)" % num) if b else num, k, ("+ %d" % c) if c >= 0 else ("− %d" % -c)), x, "int", {},
                   ["Multiply by %d: %s = %dx %s %d." % (k, num, k, "+" if k * c >= 0 else "−", abs(k * c)),
                    "x = %d." % x])

    def t_substitute():
        x = random.randint(_by(d, 3, 3, 8), _by(d, 8, 12, 20))
        c = _by(d, 6, 6, random.randint(7, 15))
        k = random.choice([v for v in range(1, x) if (x + c) % v == 0 and v != x])
        return _tb("Find the value of (x + %d)/(x − %d) when x = %d." % (c, x - k, x), (x + c) // k, "int", {},
                   ["(%d + %d) ÷ (%d − %d) = %d ÷ %d = %d." % (x, c, x, x - k, x + c, k, (x + c) // k)])

    return _pick_t([lambda: _solve_frac(d), t_add, t_cancel, t_sub_k, t_add_k, t_multiply, t_divide, t_factor_cancel, t_quad_cancel,
                    t_solve_linear_frac, t_substitute])


def _g(a, b):
    while b:
        a, b = b, a % b
    return a


def _solve_frac(d=1):
    k, x = random.randint(2, _by(d, 5, 9, 9)), random.randint(1, _by(d, 10, 12, 20))
    c = random.randint(1, _by(d, 5, 10, 20))
    rhs = Fraction(x + c, k)
    if rhs.denominator != 1:
        x += k - (x + c) % k
        rhs = Fraction(x + c, k)
    return _tb("Solve (x + %d)/%d = %d." % (c, k, rhs), x, "int", {}, ["x + %d = %d." % (c, rhs * k), "x = %d." % x])
