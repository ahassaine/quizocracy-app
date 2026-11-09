# Year 7 generators: ratio and proportion, powers and roots, area, volume and straight-line graphs.
#
# KS3 statements covered here: use ratio notation, including reduction to simplest form; divide a
# quantity into two parts in a given part:part or part:whole ratio; relate ratios to fractions;
# solve problems involving direct proportion (unitary method, recipes, best buys); use squares,
# cubes and their roots; derive and apply formulae for the perimeter and area of rectangles and
# compound rectilinear shapes and the volume of cuboids; work with coordinates in all four
# quadrants and plot straight-line graphs from tables of values.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S4 = "7.4 Fractions, decimals & percentages"
S5 = "7.5 Applications of number"
S6 = "7.6 Directed number"

def _a(x):
    """'a 7 cm', 'an 8 cm', 'an 11-sided', 'an octagon': the article read aloud, plus the text."""
    s = str(x)
    w = s.split()[0].replace(",", "").split("-")[0]
    if w[:1].isdigit():
        vowel = w.startswith("8") or w in ("11", "18") or (len(w) in (5, 8) and w[:2] in ("11", "18"))
    else:
        vowel = w[:1].lower() in "aeiou"
    return ("an " if vowel else "a ") + s



def _g(a, b):
    while b:
        a, b = b, a % b
    return a


def _coprime(lo=1, hi=9):
    """Two different numbers with no common factor: a ratio already in its simplest form."""
    while True:
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        if a != b and _g(a, b) == 1:
            return a, b


# ================================================================== 7.4 ======
@skill("Y7.4.f", "Ratio notation and simplifying ratios", S4)
def _(d=1):
    d = _d(d)
    a, b = _coprime(1, _by(d, 5, 9, 12))
    k = random.randint(2, _by(d, 6, 9, 12))

    def t_simplify():
        return _wq("Write %d : %d in its simplest form. Type it like 2:3." % (a * k, b * k), "%d:%d" % (a, b),
                   ["Divide both by %d." % k, "%d : %d." % (a, b)], "e.g. 2:3")

    def t_missing():
        return _tb("Find the missing number:  %d : %d = %d : ___" % (a, b, a * k), b * k, "int", {},
                   ["%d × %d = %d, so %d × %d = %d." % (a, k, a * k, b, k, b * k)])

    def t_class():
        return _tb("A class has %d boys and %d girls. Written in its simplest form, the ratio boys : girls is %d : ___. What is the "
                   "missing number?" % (a * k, b * k, a), b, "int", {}, ["%d : %d, divide both by %d." % (a * k, b * k, k)])

    def t_units():
        cm, m = pick([(50, 2), (25, 1), (20, 1), (75, 3), (40, 2), (30, 3)])
        return _tb("Write %d cm : %d m in the form 1 : n. What is n?" % (cm, m), _ds(Fraction(m * 100, cm)), "num", {},
                   ["Same units first: %d cm : %d cm." % (cm, m * 100), "Divide by %d: 1 : %s." % (cm, _ds(Fraction(m * 100, cm)))])

    def t_one_to_n():
        p = pick([2, 4, 5, 8, 10])
        q = p * random.randint(1, 5) + random.randint(1, p - 1)      # not a multiple of p, so n is a decimal
        return _tb("Write %d : %d in the form 1 : n. What is n?" % (p, q), _ds(Fraction(q, p)), "num", {},
                   ["Divide both by %d: 1 : %s." % (p, _ds(Fraction(q, p)))])

    def t_three():
        c = random.choice([v for v in range(1, 10) if v not in (a, b)])     # a, b coprime, so a : b : c is simplest
        return _tb("Simplify %d : %d : %d fully. It becomes %d : %d : ___. What is the missing number?"
                   % (a * k, b * k, c * k, a, b), c, "int", {}, ["Divide all three by %d." % k])

    def t_equivalent():
        same = random.random() < 0.5
        m2 = random.choice([v for v in range(2, 7) if v != k])
        p, q = (a * m2, b * m2) if same else (a * m2, b * m2 + 1)
        return _wq("Are %d : %d and %d : %d equivalent ratios? (yes or no)" % (a * k, b * k, p, q), "yes" if same else "no",
                   ["%d : %d simplifies to %d : %d." % (a * k, b * k, a, b),
                    "%d : %d simplifies to %d : %d." % (p, q, p // _g(p, q), q // _g(p, q))], "yes / no")

    def t_decimals():
        p, q = Decimal(a) / 2, Decimal(b) / 2          # a, b coprime, so at least one half is not whole
        return _tb("Write %s : %s as a ratio of whole numbers in its simplest form. It is %d : ___. What is the missing number?"
                   % (_ds(p), _ds(q), a), b, "int", {}, ["Multiply both by 2: %d : %d." % (a, b)])

    def t_order():
        fl, su = a * k * 10, b * k * 10
        return _tb("A recipe uses %d g of flour and %d g of sugar. Written in its simplest form, the ratio sugar : flour is "
                   "%d : ___. What is the missing number?" % (fl, su, b), a, "int", {},
                   ["The order matters: sugar first, %d : %d, then divide by %d." % (su, fl, k * 10)])

    def t_bar():
        cats = ["Red", "Blue"]
        return _bar("The bar chart shows the counters in a bag. Written in its simplest form, the ratio red : blue is %d : ___. "
                    "What is the missing number?" % a, cats, [a * k, b * k], b,
                    ["%d : %d, divide both by %d." % (a * k, b * k, k)])

    def t_grid():
        rows, cols = pick([(2, 5), (3, 4), (2, 6), (4, 5), (3, 5), (2, 4)])
        n = rows * cols
        s = random.randint(1, n - 1)
        g = _g(s, n - s)
        return _area("Some squares are shaded. Written in its simplest form, the ratio shaded : unshaded is %d : ___. What is "
                     "the missing number?" % (s // g), {"mode": "fraction_read", "parts": n, "shaded": s, "rows": rows,
                                                         "cols": cols, "placeholder": "number"},
                     (n - s) // g, ["%d shaded and %d unshaded: %d : %d." % (s, n - s, s // g, (n - s) // g)])

    def t_money():
        pounds, pence = random.randint(1, 9), random.randint(1, 9) * 10
        g = _g(pounds * 100, pence)
        return _tb("Write £%d : %dp in its simplest form. It is %d : ___. What is the missing number?"
                   % (pounds, pence, pounds * 100 // g), pence // g, "int", {},
                   ["£%d = %dp." % (pounds, pounds * 100), "%d : %d, divide both by %d." % (pounds * 100, pence, g)])

    return _pick_t([t_simplify, t_missing, t_class, t_units, t_one_to_n, t_three, t_equivalent, t_decimals, t_order, t_money],
                   [t_bar, t_grid])


@skill("Y7.4.g", "Share a quantity in a given ratio", S4)
def _(d=1):
    d = _d(d)
    a, b = _coprime(1, _by(d, 5, 7, 9))
    part = random.randint(2, _by(d, 10, 20, 40))
    tot = (a + b) * part

    def t_larger():
        return _tb("Share £%d in the ratio %d : %d. How much is the larger share, in pounds?" % (tot, a, b), max(a, b) * part, "int",
                   {"unit": "£"}, ["%d + %d = %d parts; one part = £%d." % (a, b, a + b, part),
                                   "%d × %d = %d." % (max(a, b), part, max(a, b) * part)])

    def t_smaller():
        who1, who2 = random.sample(NAMES, 2)
        return _tb("%s and %s share %d sweets in the ratio %d : %d. How many sweets does %s get?" % (who1, who2, tot, a, b, who1),
                   a * part, "int", {"unit": "sweets"}, ["One part = %d ÷ %d = %d." % (tot, a + b, part),
                                                         "%s gets %d × %d = %d." % (who1, a, part, a * part)])

    def t_one_part():
        return _strip("£%d is shared in the ratio %d : %d. The bar shows the %d equal parts. How much is one part, in pounds?"
                      % (tot, a, b, a + b), {"mode": "equal_parts", "parts": a + b, "partLabel": "?", "totalLabel": "£%d" % tot,
                                            "unknown": "part"}, part, ["%d ÷ %d = %d." % (tot, a + b, part)])

    def t_difference():
        if a == b:
            return t_larger()
        lo, hi = min(a, b), max(a, b)
        return _tb("Two numbers are in the ratio %d : %d. The larger is %d more than the smaller. What is the smaller number?"
                   % (lo, hi, (hi - lo) * part), lo * part, "int", {},
                   ["The difference is %d part%s = %d, so one part = %d." % (hi - lo, "" if hi - lo == 1 else "s", (hi - lo) * part,
                                                                            part), "%d × %d = %d." % (lo, part, lo * part)])

    def t_given_one():
        return _tb("Paint is mixed in the ratio blue : white = %d : %d. %d litres of blue are used. How many litres of white are "
                   "needed?" % (a, b, a * part), b * part, "int", {"unit": "litres"},
                   ["One part = %d ÷ %d = %d." % (a * part, a, part), "White = %d × %d = %d." % (b, part, b * part)])

    def t_total():
        return _tb("Boys and girls in a choir are in the ratio %d : %d. There are %d boys. How many children are in the choir?"
                   % (a, b, a * part), tot, "int", {"unit": "children"},
                   ["One part = %d." % part, "%d parts in total: %d." % (a + b, tot)])

    def t_three_way():
        c = random.randint(1, 6)
        t3 = (a + b + c) * part
        return _tb("Share %d in the ratio %d : %d : %d. What is the largest share?" % (t3, a, b, c), max(a, b, c) * part, "int", {},
                   ["%d parts; one part = %d." % (a + b + c, part), "%d × %d = %d." % (max(a, b, c), part, max(a, b, c) * part)])

    def t_angles():
        p, q, r = pick([(1, 2, 3), (2, 3, 4), (1, 1, 2), (2, 3, 5), (1, 3, 5), (3, 4, 5), (1, 2, 6), (4, 5, 9)])
        one = 180 // (p + q + r)
        return _tb("The angles of a triangle are in the ratio %d : %d : %d. What is the largest angle?" % (p, q, r), r * one, "int",
                   {"unit": "°"}, ["%d parts = 180°, so one part = %d°." % (p + q + r, one), "%d × %d = %d." % (r, one, r * one)])

    def t_concrete():
        s = pick([2, 3, 4, 5])
        kg = (1 + s) * random.randint(2, 12)
        return _tb("Mortar is cement and sand mixed in the ratio 1 : %d. How much sand is in %d kg of mortar, in kg?" % (s, kg),
                   kg // (1 + s) * s, "int", {"unit": "kg"}, ["%d parts; one part = %d kg." % (1 + s, kg // (1 + s)),
                                                              "Sand = %d × %d = %d kg." % (s, kg // (1 + s), kg // (1 + s) * s)])

    def t_check():
        right = random.random() < 0.5
        x, y = (a * part, b * part) if right else (a * part + 1, b * part - 1)
        return _wq("%s shares %d stickers in the ratio %d : %d and gives out %d and %d. Is this right? (yes or no)"
                   % (_who(), tot, a, b, x, y), "yes" if right else "no",
                   ["One part = %d, so the shares are %d and %d." % (part, a * part, b * part)], "yes / no")

    def t_ages():
        y1, y2 = pick([(6, 9), (8, 12), (4, 6), (10, 15), (6, 10), (9, 12)])
        g = _g(y1, y2)
        unit = random.randint(2, 8) * 5
        money = (y1 + y2) // g * unit
        return _tb("Grandma shares £%d between two children in the ratio of their ages, %d and %d. How much does the older child "
                   "get, in pounds?" % (money, y1, y2), y2 // g * unit, "int", {"unit": "£"},
                   ["%d : %d = %d : %d." % (y1, y2, y1 // g, y2 // g), "One part = £%d, so £%d." % (unit, y2 // g * unit)])

    def t_fraction():
        return _fq("£%d is shared in the ratio %d : %d. What fraction of the money does the first person get? Simplest form."
                   % (tot, a, b), Fraction(a, a + b), ["%d out of %d parts." % (a, a + b)])

    return _pick_t([t_larger, t_smaller, t_difference, t_given_one, t_total, t_three_way, t_angles, t_concrete, t_check, t_ages,
                    t_fraction], [t_one_part])


@skill("Y7.4.h", "Ratio, fractions and direct proportion", S4)
def _(d=1):
    d = _d(d)
    a, b = _coprime(1, _by(d, 5, 9, 12))

    def t_fraction_of():
        return _fq("Red and blue beads are in the ratio %d : %d. What fraction of the beads are red?" % (a, b), Fraction(a, a + b),
                   ["%d + %d = %d parts; red is %d of them." % (a, b, a + b, a)])

    def t_frac_to_ratio():
        f = pick(_by(d, [Fraction(1, 4), Fraction(2, 5), Fraction(1, 3), Fraction(3, 4), Fraction(3, 5)],
                     [Fraction(2, 5), Fraction(3, 8), Fraction(1, 4), Fraction(3, 7), Fraction(5, 9), Fraction(4, 9)],
                     [Fraction(3, 8), Fraction(5, 12), Fraction(7, 10), Fraction(4, 9), Fraction(5, 9), Fraction(7, 12)]))
        return _tb("%s of a class are boys and the rest are girls. The ratio boys : girls is %d : ___. What is the missing number?"
                   % (_fs(f), f.numerator), f.denominator - f.numerator, "int", {},
                   ["Out of %d parts, %d are boys and %d are girls." % (f.denominator, f.numerator, f.denominator - f.numerator)])

    def t_recipe():
        if d == 0:                                  # easy: scale up by a whole number
            n1 = pick([2, 4])
            n2 = n1 * pick([2, 3])
        else:
            n1 = pick(_by(d, None, [2, 4, 6], [3, 4, 6]))
            n2 = pick([v for v in _by(d, None, (3, 5, 8, 9, 10, 12), (5, 7, 9, 10, 14, 15)) if v != n1])
        g = random.randint(2, 9) * 30
        return _tb("A recipe for %d people uses %d g of flour. How much flour is needed for %d people, in g?" % (n1, g, n2),
                   _ds(Fraction(g * n2, n1)), "num", {"unit": "g"},
                   ["For 1 person: %d ÷ %d = %s g." % (g, n1, _ds(Fraction(g, n1))), "For %d: %s g." % (n2, _ds(Fraction(g * n2, n1)))])

    def t_unit_price():
        n1, n2 = random.randint(_by(d, 2, 3, 3), _by(d, 4, 6, 9)), random.randint(_by(d, 5, 7, 10), _by(d, 10, 12, 25))
        each = Decimal(random.randint(_by(d, 3, 15, 15), _by(d, 19, 95, 199)) * _by(d, 5, 1, 1)) / 100
        return _tb("%d pens cost £%s. How much do %d pens cost, in pounds?" % (n1, format(each * n1, ".2f"), n2), _ds(each * n2), "num",
                   {"unit": "£"}, ["One pen: £%s." % format(each, ".2f"), "%d pens: £%s." % (n2, format(each * n2, ".2f"))])

    def t_recipe_table():
        serves = pick([4, 6])
        ing = [["Flour", 50 * random.randint(3, 8), "g"], ["Milk", 50 * random.randint(4, 10), "ml"], ["Eggs", random.randint(2, 4), ""]]
        new = pick([v for v in (2, 3, 8, 9, 12) if (v * 50) % serves == 0 and v != serves])
        k = random.randrange(2)
        name, amt, unit = ing[k]
        return _dt("The table shows a pancake recipe for %d people. How much %s is needed for %d people, in %s?"
                   % (serves, name.lower(), new, unit), ["Ingredient", "Amount"],
                   [[n, "%d %s" % (q, u) if u else str(q)] for n, q, u in ing], _ds(Fraction(amt * new, serves)),
                   ["%d ÷ %d × %d = %s." % (amt, serves, new, _ds(Fraction(amt * new, serves)))], atype="num")

    def t_best_buy():
        na, nb = pick([(6, 10), (4, 6), (5, 8), (3, 4)])
        pa = Decimal(random.randint(20, 60)) / 10 * na / 5
        ua = pa / na
        ub = ua + pick(_by(d, [Decimal("0.10"), Decimal("-0.10"), Decimal("0.20"), Decimal("-0.20")],
                           [Decimal("0.02"), Decimal("-0.02"), Decimal("0.05"), Decimal("-0.05")],
                           [Decimal("0.01"), Decimal("-0.01"), Decimal("0.02"), Decimal("-0.02")]))
        pa, pb = pa.quantize(Decimal("0.01")), (ub * nb).quantize(Decimal("0.01"))
        if pa / na == pb / nb:
            pb += Decimal("0.05")
        return _wq("Pack A has %d cans for £%s. Pack B has %d cans for £%s. Which is better value? (A or B)"
                   % (na, format(pa, ".2f"), nb, format(pb, ".2f")), "A" if pa / na < pb / nb else "B",
                   ["Price per can: A £%s, B £%s." % (format(pa / na, ".3f"), format(pb / nb, ".3f"))], "A or B")

    def t_conversion():
        if d == 2 and random.random() < 0.5:        # stretch: convert the other way
            km = random.randint(3, 25) * 8
            return _tb("5 miles is about 8 km. About how many miles is %d km?" % km, km * 5 // 8, "int", {"unit": "miles"},
                       ["%d ÷ 8 = %d; × 5 = %d." % (km, km // 8, km * 5 // 8)])
        mi = random.randint(2, _by(d, 10, 20, 40)) * 5
        return _tb("5 miles is about 8 km. About how many km is %d miles?" % mi, mi * 8 // 5, "int", {"unit": "km"},
                   ["%d ÷ 5 = %d; × 8 = %d." % (mi, mi // 5, mi * 8 // 5)])

    def t_table():
        k = random.randint(2, _by(d, 5, 9, 15))
        xs = random.sample(range(1, _by(d, 11, 13, 21)), 4)
        rows = [[x, k * x] for x in xs]
        m = random.randrange(4)
        return _io("y is directly proportional to x. What goes in the empty cell?", rows, m, k * xs[m],
                   ["y = %d × x." % k, "%d × %d = %d." % (k, xs[m], k * xs[m])])

    def t_wages():
        rate = Decimal(random.randint(18, _by(d, 24, 30, 45))) / 2
        h1, h2 = random.randint(3, _by(d, 4, 6, 8)), random.randint(7, _by(d, 10, 12, 20))
        return _tb("%s earns £%s for %d hours of work. How much will they earn for %d hours, in pounds?"
                   % (_who(), format(rate * h1, ".2f"), h1, h2), _ds(rate * h2), "num", {"unit": "£"},
                   ["One hour: £%s." % format(rate, ".2f"), "%d hours: £%s." % (h2, format(rate * h2, ".2f"))])

    def t_scale_down():
        n1 = pick(_by(d, [8, 12], [8, 12], [12, 15, 16]))
        n2 = pick(_by(d, [2, 4], [2, 3, 4, 6], [5, 7, 9, 10]))
        g = n1 * random.randint(5, 30)
        return _tb("A stew for %d people uses %d g of beef. How much beef is needed for %d people, in g?" % (n1, g, n2),
                   _ds(Fraction(g * n2, n1)), "num", {"unit": "g"}, ["%d ÷ %d × %d = %s." % (g, n1, n2, _ds(Fraction(g * n2, n1)))])

    def t_how_many_times():
        return _fq("In the ratio %d : %d, the second amount is how many times the first? (A fraction is fine.)" % (a, b),
                   Fraction(b, a), ["%d ÷ %d = %s." % (b, a, _fs(Fraction(b, a)))], "e.g. 5/2")

    def t_petrol():
        lit = random.randint(_by(d, 10, 20, 35), _by(d, 30, 50, 80))
        p = Decimal(random.randint(130, 160)) / 100
        return _tb("Petrol costs £%s per litre. How much does %d litres cost, in pounds?" % (format(p, ".2f"), lit), _ds(p * lit),
                   "num", {"unit": "£"}, ["%d × %s = %s." % (lit, format(p, ".2f"), _ds(p * lit))])

    every = [t_fraction_of, t_frac_to_ratio, t_recipe, t_unit_price, t_best_buy, t_conversion, t_wages, t_scale_down,
             t_how_many_times, t_petrol]
    return _pick_t(_by(d, [t_fraction_of, t_frac_to_ratio, t_recipe, t_unit_price, t_best_buy, t_conversion, t_scale_down],
                       every, every), [t_recipe_table, t_table])


# ================================================================== 7.5 ======
@skill("Y7.5.g", "Squares, cubes and roots", S5)
def _(d=1):
    d = _d(d)
    n = random.randint(2, _by(d, 10, 12, 15))
    c = random.randint(2, _by(d, 5, 6, 10))

    def t_square():
        return _tb("Work out %d²." % n, n * n, "int", {}, ["%d × %d = %d." % (n, n, n * n)])

    def t_cube():
        return _tb("Work out %d³." % c, c ** 3, "int", {}, ["%d × %d × %d = %d." % (c, c, c, c ** 3)])

    def t_root():
        return _tb("Work out √%d." % (n * n), n, "int", {}, ["%d × %d = %d." % (n, n, n * n)])

    def t_cube_root():
        return _tb("Work out the cube root of %d." % c ** 3, c, "int", {}, ["%d × %d × %d = %d." % (c, c, c, c ** 3)])

    def t_between():
        v = random.choice([x for x in range(3, 140) if int(x ** 0.5) ** 2 != x])
        lo = int(v ** 0.5)
        return _tb("√%d lies between two whole numbers next to each other. What is the smaller one?" % v, lo, "int", {},
                   ["%d² = %d and %d² = %d, so √%d is between %d and %d." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, v, lo, lo + 1)])

    def t_decimal_sq():
        k = random.randint(1, 9)
        return _tb("Work out 0.%d²." % k, _ds(Decimal(k * k) / 100), "num", {},
                   ["0.%d × 0.%d = %s." % (k, k, _ds(Decimal(k * k) / 100))])

    def t_negative():
        return _tb("Work out (−%d)²." % n, n * n, "int", {}, ["Negative × negative is positive: %d." % (n * n)])

    def t_only_square():
        lo = random.randint(2, 11)
        a, b = lo * lo + 1, (lo + 1) ** 2 + 1          # only (lo + 1)² lies strictly between
        return _tb("Which square number is between %d and %d?" % (a, b), (lo + 1) ** 2, "int", {},
                   ["%d² = %d." % (lo + 1, (lo + 1) ** 2)])

    def t_sum():
        p, q = random.randint(1, 9), random.randint(1, 9)
        return _tb("Work out %d² + %d²." % (p, q), p * p + q * q, "int", {}, ["%d + %d = %d." % (p * p, q * q, p * p + q * q)])

    def t_both():
        v, ans = pick([(64, "yes"), (1, "yes"), (729, "yes"), (36, "no"), (8, "no"), (100, "no"), (27, "no"), (16, "no")])
        return _wq("Is %d both a square number and a cube number? (yes or no)" % v, ans,
                   ["Squares: 1, 4, 9, 16, 25, 36, 49, 64, … Cubes: 1, 8, 27, 64, 125, …, 729."], "yes / no")

    def t_grid():
        sd = random.randint(2, 9)
        return _area("The square is made of 1 cm squares. Its area is a square number. What is its side length, in cm?",
                     {"mode": "read_area", "rows": sd, "cols": sd, "placeholder": "cm"}, sd,
                     ["%d × %d = %d squares, so each side is %d cm." % (sd, sd, sd * sd, sd)])

    def t_power_ten():
        k = random.randint(2, 6)
        return _tb("Work out 10^%d." % k, 10 ** k, "int", {}, ["1 followed by %d zeros: %s." % (k, _c(10 ** k))])

    def t_side_from_area():
        return _tb("A square has area %d cm². How long is each side, in cm?" % (n * n), n, "int", {"unit": "cm"},
                   ["√%d = %d." % (n * n, n)])

    return _pick_t([t_square, t_cube, t_root, t_cube_root, t_between, t_decimal_sq, t_negative, t_only_square, t_sum, t_both,
                    t_power_ten, t_side_from_area], [t_grid])


def _cells_perimeter(cells):
    """Boundary length of a set of unit squares (each edge not shared with another square)."""
    s = set(map(tuple, cells))
    return sum(1 for r, c in s for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (r + dr, c + dc) not in s)


def _rectilinear(d):
    """An L, U or T shape of unit squares inside an R × C box, with its cells."""
    R, C = random.randint(3, _by(d, 5, 7, 8)), random.randint(4, _by(d, 6, 8, 10))
    kind = pick(["L", "U", "T"])
    cut = set()
    if kind == "L":
        h, w = random.randint(1, R - 2), random.randint(1, C - 2)
        cut = {(r, c) for r in range(h) for c in range(C - w, C)}
    elif kind == "U":
        h, w0 = random.randint(1, R - 2), random.randint(1, C - 3)
        w = random.randint(1, C - 1 - w0 - 1)
        cut = {(r, c) for r in range(h) for c in range(w0, w0 + w)}
    else:
        h = random.randint(1, R - 2)
        w0 = random.randint(1, C // 2 - 1) if C >= 4 else 1
        cut = {(r, c) for r in range(h, R) for c in list(range(0, w0)) + list(range(C - w0, C))}
    cells = [[r, c] for r in range(R) for c in range(C) if (r, c) not in cut]
    return cells


@skill("Y7.5.h", "Perimeter and area of rectangles and compound shapes", S5)
def _(d=1):
    d = _d(d)
    L, W = random.randint(3, _by(d, 10, 15, 25)), random.randint(2, _by(d, 8, 12, 20))

    def t_read_area():
        cells = _rectilinear(d)
        return _area("Each square is 1 cm². What is the area of the shape, in cm²?", {"mode": "read_area", "cells": cells,
                                                                                        "placeholder": "cm²"},
                     len(cells), ["Count the squares: %d." % len(cells)])

    def t_read_perimeter():
        cells = _rectilinear(d)
        p = _cells_perimeter(cells)
        return _area("Each square has sides of 1 cm. What is the perimeter of the shape, in cm?",
                     {"mode": "read_perimeter", "cells": cells, "placeholder": "cm"}, p,
                     ["Walk round the outside edge counting each side: %d cm." % p])

    def t_rect_area():
        return _tb("A rectangle is %d cm long and %d cm wide. What is its area, in cm²?" % (L, W), L * W, "int", {"unit": "cm²"},
                   ["%d × %d = %d." % (L, W, L * W)])

    def t_rect_perim():
        return _tb("A rectangle is %d m long and %d m wide. What is its perimeter, in m?" % (L, W), 2 * (L + W), "int", {"unit": "m"},
                   ["2 × (%d + %d) = %d." % (L, W, 2 * (L + W))])

    def t_l_area():
        big_l, big_w = L + 4, W + 3
        cl, cw = random.randint(1, L + 2), random.randint(1, W + 1)
        return _tb("An L-shape is %s cm by %d cm rectangle with %s cm by %d cm rectangle cut from one corner. What is its "
                   "area, in cm²?" % (_a(big_l), big_w, _a(cl), cw), big_l * big_w - cl * cw, "int", {"unit": "cm²"},
                   ["%d − %d = %d." % (big_l * big_w, cl * cw, big_l * big_w - cl * cw)])

    def t_l_perim():
        big_l, big_w = L + 4, W + 3
        cl, cw = random.randint(1, L + 2), random.randint(1, W + 1)
        return _tb("An L-shape is %s cm by %d cm rectangle with %s cm by %d cm rectangle cut from one corner. What is its "
                   "perimeter, in cm?" % (_a(big_l), big_w, _a(cl), cw), 2 * (big_l + big_w), "int", {"unit": "cm"},
                   ["Cutting a corner moves two sides inwards but keeps their lengths:",
                    "perimeter = 2 × (%d + %d) = %d." % (big_l, big_w, 2 * (big_l + big_w))])

    def t_missing_side():
        return _tb("A rectangle has area %d cm² and length %d cm. What is its width, in cm?" % (L * W, L), W, "int", {"unit": "cm"},
                   ["%d ÷ %d = %d." % (L * W, L, W)])

    def t_largest_perim():
        A = pick([12, 16, 18, 20, 24, 30, 36])
        return _tb("A rectangle has area %d cm² and whole-number sides. What is the largest perimeter it can have, in cm?" % A,
                   2 * (A + 1), "int", {"unit": "cm"}, ["The longest, thinnest rectangle: 1 cm by %d cm, perimeter %d cm." % (A, 2 * (A + 1))])

    def t_square_from_perim():
        s = random.randint(2, 15)
        return _tb("A square has perimeter %d cm. What is its area, in cm²?" % (4 * s), s * s, "int", {"unit": "cm²"},
                   ["Side = %d ÷ 4 = %d." % (4 * s, s), "Area = %d × %d = %d." % (s, s, s * s)])

    def t_build():
        A = random.randint(6, 20)
        return _area("Shade a shape with an area of %d squares." % A, {"mode": "build_area", "rows": 5, "cols": 6}, A,
                     ["Any %d squares make an area of %d square units." % (A, A)])

    def t_frame():
        ow, oh = random.randint(8, 20), random.randint(6, 15)
        b = random.randint(1, 2)
        return _tb("A picture frame is %d cm by %d cm on the outside and %d cm wide all round. What is the area of the frame "
                   "itself, in cm²?" % (ow, oh, b), ow * oh - (ow - 2 * b) * (oh - 2 * b), "int", {"unit": "cm²"},
                   ["Inside: %d × %d = %d." % (ow - 2 * b, oh - 2 * b, (ow - 2 * b) * (oh - 2 * b)),
                    "%d − %d = %d." % (ow * oh, (ow - 2 * b) * (oh - 2 * b), ow * oh - (ow - 2 * b) * (oh - 2 * b))])

    def t_units():
        cm = random.randint(2, 9) * 100
        m = random.randint(2, 6)
        return _tb("A rug is %d cm long and %d m wide. What is its area, in m²?" % (cm, m), cm // 100 * m, "int", {"unit": "m²"},
                   ["%d cm = %d m." % (cm, cm // 100), "%d × %d = %d." % (cm // 100, m, cm // 100 * m)])

    def t_same_perim():
        p = 2 * random.randint(6, 12)
        half = p // 2
        best = (half // 2) * (half - half // 2)
        return _tb("Rectangles with whole-number sides all have a perimeter of %d cm. What is the largest area one can have, in "
                   "cm²?" % p, best, "int", {"unit": "cm²"},
                   ["Length + width = %d; the closer to a square, the bigger: %d × %d = %d." % (half, half // 2, half - half // 2, best)])

    return _pick_t([t_rect_area, t_rect_perim, t_l_area, t_l_perim, t_missing_side, t_largest_perim, t_square_from_perim, t_frame,
                    t_units, t_same_perim], [t_read_area, t_read_perimeter, t_build])


@skill("Y7.5.i", "Volume of cuboids", S5)
def _(d=1):
    d = _d(d)
    l, w, h = [random.randint(2, _by(d, 6, 10, 15)) for _ in range(3)]

    def t_volume():
        return _tb("A cuboid is %d cm long, %d cm wide and %d cm high. What is its volume, in cm³?" % (l, w, h), l * w * h, "int",
                   {"unit": "cm³"}, ["%d × %d × %d = %d." % (l, w, h, l * w * h)])

    def t_cube():
        return _tb("A cube has edges of %d cm. What is its volume, in cm³?" % l, l ** 3, "int", {"unit": "cm³"},
                   ["%d × %d × %d = %d." % (l, l, l, l ** 3)])

    def t_height():
        return _tb("A cuboid has volume %d cm³. Its base is %d cm by %d cm. How high is it, in cm?" % (l * w * h, l, w), h, "int",
                   {"unit": "cm"}, ["Base area = %d cm²." % (l * w), "%d ÷ %d = %d." % (l * w * h, l * w, h)])

    def t_count():
        return _tb("A cuboid is built from 1 cm cubes: %d cubes long, %d cubes wide and %d cubes high. How many cubes are used?"
                   % (l, w, h), l * w * h, "int", {"unit": "cubes"}, ["%d × %d = %d in each layer; %d layers: %d." % (l, w, l * w, h, l * w * h)])

    def t_litres():
        L, W, H = random.randint(2, 8) * 10, random.randint(2, 6) * 10, random.randint(2, 5) * 10
        return _tb("A fish tank is %d cm by %d cm by %d cm. How many litres does it hold when full? (1 litre = 1000 cm³)"
                   % (L, W, H), L * W * H // 1000, "int", {"unit": "litres"},
                   ["%d × %d × %d = %s cm³." % (L, W, H, _c(L * W * H)), "÷ 1000 = %d litres." % (L * W * H // 1000)])

    def t_fit():
        a, b, c = random.randint(2, 4), random.randint(2, 4), random.randint(1, 3)
        s = pick([2, 5, 10])
        return _tb("How many boxes %d cm by %d cm by %d cm fit exactly into a crate %d cm by %d cm by %d cm, packed the same way "
                   "round?" % (s, s, s, a * s, b * s, c * s), a * b * c, "int", {"unit": "boxes"},
                   ["%d × %d × %d = %d." % (a, b, c, a * b * c)])

    def t_decimal():
        a = Decimal(random.randint(3, 19)) / 2
        return _tb("A cuboid is %s m by %d m by %d m. What is its volume, in m³?" % (_ds(a), w, h), _ds(a * w * h), "num",
                   {"unit": "m³"}, ["%s × %d × %d = %s." % (_ds(a), w, h, _ds(a * w * h))])

    def t_compare():
        a2, b2, c2 = l + 1, w, max(1, h - 1)
        if a2 * b2 * c2 == l * w * h:
            c2 += 1
        return _wq("Box A is %d × %d × %d cm. Box B is %d × %d × %d cm. Which holds more? (A or B)" % (l, w, h, a2, b2, c2),
                   "A" if l * w * h > a2 * b2 * c2 else "B", ["A: %d cm³. B: %d cm³." % (l * w * h, a2 * b2 * c2)], "A or B")

    def t_cube_side():
        return _tb("A cube has a volume of %d cm³. How long is each edge, in cm?" % l ** 3, l, "int", {"unit": "cm"},
                   ["%d × %d × %d = %d." % (l, l, l, l ** 3)])

    def t_layers():
        return _tb("The bottom layer of a cuboid made of cubes has %d cubes. There are %d layers. How many cubes altogether?"
                   % (l * w, h), l * w * h, "int", {"unit": "cubes"}, ["%d × %d = %d." % (l * w, h, l * w * h)])

    def t_shape():
        return {"prompt": "This cuboid is %d cm long, %d cm wide and %d cm high. What is its volume, in cm³?" % (l, w, h),
                "component": "shape", "spec": {"kind": "3d", "name": "cuboid", "ask": "sides"}, "answer": l * w * h,
                "answer_type": "int", "solution": ["%d × %d × %d = %d." % (l, w, h, l * w * h)]}

    def t_ml():
        L, W, H = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        return _tb("A carton is %d cm by %d cm by %d cm. How many millilitres does it hold? (1 cm³ = 1 ml)" % (L, W, H), L * W * H,
                   "int", {"unit": "ml"}, ["%d × %d × %d = %d cm³ = %d ml." % (L, W, H, L * W * H, L * W * H)])

    return _pick_t([t_volume, t_cube, t_height, t_count, t_litres, t_fit, t_decimal, t_compare, t_cube_side, t_layers, t_ml],
                   [t_shape])


# ================================================================== 7.6 ======
def _yx(m, c):
    """'y = 2x − 3' style text."""
    s = "y = " + ("" if m == 1 else "−" if m == -1 else str(m).replace("-", "−")) + "x"
    if c:
        s += (" + %d" % c) if c > 0 else (" − %d" % -c)
    return s


@skill("Y7.6.e", "Tables of values and graphs of y = mx + c", S6)
def _(d=1):
    d = _d(d)
    m = random.choice([v for v in range(_by(d, 1, -3, -4), _by(d, 3, 4, 5) + 1) if v])
    c = random.randint(_by(d, 0, -4, -6), _by(d, 4, 5, 6))
    rule = _yx(m, c)

    def t_table():
        xs = [-2, -1, 0, 1, 2, 3]
        k = random.randrange(6)
        return _io("Complete the table of values for %s. What goes in the empty cell?" % rule, [[x, m * x + c] for x in xs], k,
                   m * xs[k] + c, ["%d × (%d) %s = %d." % (m, xs[k], ("+ %d" % c) if c >= 0 else ("− %d" % -c), m * xs[k] + c)],
                   rule=rule)

    def t_plot():
        x = random.choice([v for v in range(-3, 4) if abs(m * v + c) <= 7])
        return {"prompt": "Plot the point on the line %s where x = %d." % (rule, x), "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7}, "answer": "(%d,%d)" % (x, m * x + c), "answer_type": "coord",
                "solution": ["y = %d, so the point is (%d,%d)." % (m * x + c, x, m * x + c)]}

    def t_read():
        x = random.choice([v for v in range(-3, 4) if abs(m * v + c) <= 7])
        return {"prompt": "The line %s is drawn. What is y when x = %d?" % (rule, x), "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "typed": True, "placeholder": "y =",
                         "lines": [{"p1": [0, c], "p2": [1, m + c]}]}, "answer": m * x + c, "answer_type": "int",
                "solution": ["Go to x = %d and read across: y = %d." % (x, m * x + c)]}

    def t_on_line():
        x = random.randint(-4, 5)
        y = m * x + c + pick([0, 0, 1, -2])
        return _wq("Does the point (%d,%d) lie on the line %s? (yes or no)" % (x, y, rule), "yes" if y == m * x + c else "no",
                   ["When x = %d, y = %d." % (x, m * x + c)], "yes / no")

    def t_intercept():
        return _tb("At what value of y does the line %s cross the y-axis?" % rule, c, "int", {},
                   ["On the y-axis x = 0, so y = %d." % c])

    def t_horizontal():
        k = random.randint(-5, 5)
        hz = random.random() < 0.5
        return _wq("Which of these lines is %s: y = %d or x = %d? (type it like y=3)" % ("horizontal" if hz else "vertical", k, k),
                   ("y=%d" if hz else "x=%d") % k, ["y = k is horizontal; x = k is vertical."], "e.g. y=3")

    def t_missing_coord():
        x = random.randint(-3, 6)
        return _tb("The point (%d, ?) lies on the line %s. What is the missing y-coordinate?" % (x, rule), m * x + c, "int", {},
                   ["y = %d × %d %s = %d." % (m, x, ("+ %d" % c) if c >= 0 else ("− %d" % -c), m * x + c)])

    def t_find_x():
        x = random.randint(-3, 6)
        return _tb("On the line %s, what is x when y = %d?" % (rule, m * x + c), x, "int", {},
                   ["%d = %dx %s, so x = %d." % (m * x + c, m, ("+ %d" % c) if c >= 0 else ("− %d" % -c), x)])

    def t_cross():
        a, b = random.randint(-6, 6), random.randint(-6, 6)
        return {"prompt": "Plot the point where the lines x = %d and y = %d cross." % (a, b), "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7,
                         "lines": [{"p1": [a, 0], "p2": [a, 1]}, {"p1": [0, b], "p2": [1, b]}]},
                "answer": "(%d,%d)" % (a, b), "answer_type": "coord", "solution": ["Every point on x = %d has x = %d, and on y = %d has "
                                                                                   "y = %d: (%d,%d)." % (a, a, b, b, a, b)]}

    def t_negative_x():
        x = random.randint(-6, -1)
        return _tb("Find y when x = %d for the line %s." % (x, rule), m * x + c, "int", {},
                   ["%d × (%d) = %d; %s = %d." % (m, x, m * x, ("+ %d" % c) if c >= 0 else ("− %d" % -c), m * x + c)])

    def t_steeper():
        m2 = m + pick([1, 2]) if m > 0 else m - pick([1, 2])
        return _wq("Which line is steeper: %s or %s? (type the number in front of x)"
                   % (_yx(m, 1), _yx(m2, 1)),
                   str(m2), ["The bigger the number in front of x (ignoring its sign), the steeper the line."], "e.g. 3")

    return _pick_t([t_on_line, t_intercept, t_horizontal, t_missing_coord, t_find_x, t_negative_x, t_steeper],
                   [t_table, t_plot, t_read, t_cross])
