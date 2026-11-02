# Year 7 generators: further KS3 entry skills that complete the Year 7 bank.
#
# Inequality notation (7.2), multiplying and dividing algebraic terms (7.1), standard units with
# decimals (7.3), percentages over 100% and percentage change in context (7.4), perimeter and area
# with decimals (7.5) and coordinates in four quadrants (7.8).
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S1 = "7.1 Algebraic notation"
S2 = "7.2 Equality & equivalence"
S3 = "7.3 Place value & ordering"
S4 = "7.4 Fractions, decimals & percentages"
S5 = "7.5 Applications of number"
S8 = "7.8 Lines & angles"


@skill("Y7.1.g", "Multiply and divide algebraic terms", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(2, 9), random.randint(2, 9)

    def t_coef():
        return _wq("Simplify  %da × %db  (like 6ab)" % (a, b), "%dab" % (a * b), ["%d × %d = %d; a × b = ab." % (a, b, a * b)],
                   "e.g. 6ab")

    def t_square():
        return _wq("Simplify  %dx × %dx  (use ^ for a power, like 6x^2)" % (a, b), "%dx^2" % (a * b),
                   ["x × x = x²: %dx²." % (a * b)], "e.g. 6x^2")

    def t_divide():
        return _wq("Simplify  %dy ÷ %d" % (a * b, a), "%dy" % b if b != 1 else "y", ["%d ÷ %d = %d." % (a * b, a, b)], "e.g. 3y")

    def t_cancel():
        return _wq("Simplify  %dab ÷ %da" % (a * b, a), "%db" % b, ["%d ÷ %d = %d; ab ÷ a = b." % (a * b, a, b)], "e.g. 3b")

    def t_number():
        return _wq("Simplify  %d × %dm" % (a, b), "%dm" % (a * b), ["%d × %d = %d." % (a, b, a * b)], "e.g. 12m")

    def t_value():
        x = random.randint(2, 6)
        return _tb("Simplify  %dx × %d  and find its value when x = %d." % (a, b, x), a * b * x, "int", {},
                   ["%dx; %d × %d = %d." % (a * b, a * b, x, a * b * x)])

    return _pick_t([t_coef, t_square, t_divide, t_cancel, t_number, t_value])


@skill("Y7.2.f", "Inequality notation and number lines", S2)
def _(d=1):
    d = _d(d)
    v = random.randint(-5, 8)

    def t_read():
        op = pick(["<", "<=", ">", ">="])
        word = {"<": "less than", "<=": "less than or equal to", ">": "greater than", ">=": "greater than or equal to"}[op]
        return {"prompt": "The number line shows an inequality for x. Write it (use <, >, <= or >=, like x>3).",
                "component": "inequality_line", "spec": {"op": op, "value": v, "min": v - 6, "max": v + 6},
                "answer": "x%s%d" % (op, v), "answer_type": "str",
                "solution": ["x is %s %d: x %s %d." % (word, v, op.replace("<=", "≤").replace(">=", "≥"), v)]}

    def t_satisfy():
        op = pick(["<", "≤", ">", "≥"])
        t = v + pick([-2, -1, 0, 1, 2])
        ok = {"<": t < v, "≤": t <= v, ">": t > v, "≥": t >= v}[op]
        return _wq("Does x = %d satisfy x %s %d? (yes or no)" % (t, op, v), "yes" if ok else "no",
                   ["%d %s %d is %s." % (t, op, v, "true" if ok else "false")], "yes / no")

    def t_integers():
        lo, hi = v, v + random.randint(3, 7)
        ops = pick([("<", "<"), ("≤", "<"), ("<", "≤"), ("≤", "≤")])
        vals = [n for n in range(lo, hi + 1) if (n > lo if ops[0] == "<" else n >= lo) and (n < hi if ops[1] == "<" else n <= hi)]
        return _wq("List the whole numbers n that satisfy  %d %s n %s %d, separated by commas." % (lo, ops[0], ops[1], hi),
                   ", ".join(map(str, vals)), ["Check the ends: < leaves the end out, ≤ keeps it."], "e.g. 2, 3, 4")

    def t_words():
        k = random.randint(3, 15)
        phrase, ans = pick([("at least %d", "x>=%d"), ("more than %d", "x>%d"), ("at most %d", "x<=%d"), ("fewer than %d", "x<%d")])
        return _wq("There are %s people in a room. Write this as an inequality for x (use <, >, <= or >=, like x>3)." % (phrase % k),
                   ans % k, ["'%s' → %s." % (phrase % k, ans % k)], "e.g. x>=3")

    def t_largest():
        k = random.randint(3, 20)
        return _tb("x is a whole number and x < %d. What is the largest value x can take?" % k, k - 1, "int", {},
                   ["x must be less than %d, so %d." % (k, k - 1)])

    return _pick_t([t_satisfy, t_integers, t_words, t_largest], [t_read])


@skill("Y7.3.f", "Standard units with decimal quantities", S3)
def _(d=1):
    d = _d(d)
    big, small, f = pick([("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10), ("kg", "g", 1000), ("litres", "ml", 1000),
                          ("tonnes", "kg", 1000)])

    def t_down():
        x = Decimal(random.randint(1, 9999)) / pick([10, 100, 1000])
        return _tb("Convert %s %s to %s." % (_ds(x), big, small), _ds(x * f), "num", {"unit": small}, ["× %d." % f])

    def t_up():
        x = random.randint(1, 99999)
        return _tb("Convert %s %s to %s." % (_c(x), small, big), _ds(Decimal(x) / f), "num", {"unit": big}, ["÷ %d." % f])

    def t_time():
        h = Decimal(random.randint(1, 20)) / 4
        return _tb("How many minutes are in %s hours?" % _ds(h), int(h * 60), "int", {"unit": "minutes"},
                   ["%s × 60 = %d." % (_ds(h), int(h * 60))])

    def t_time_dec():
        m = pick([15, 30, 45, 6, 12, 36, 90, 150])
        return _tb("Write %d minutes as a decimal number of hours." % m, _ds(Fraction(m, 60)), "num", {"unit": "hours"},
                   ["%d ÷ 60 = %s." % (m, _ds(Fraction(m, 60)))])

    def t_add_mixed():
        a = Decimal(random.randint(11, 99)) / 10
        b = random.randint(50, f - 1) if f > 10 else random.randint(1, 9)
        return _tb("Add %s %s and %d %s. Give your answer in %s." % (_ds(a), big, b, small, big), _ds(a + Decimal(b) / f), "num",
                   {"unit": big}, ["%d %s = %s %s." % (b, small, _ds(Decimal(b) / f), big)])

    def t_order():
        vals = [("%s %s" % (_ds(Decimal(random.randint(1, 99)) / 10), big)), ("%d %s" % (random.randint(100, 9999), small))]
        a = Decimal(vals[0].split()[0]) * f
        b = Decimal(vals[1].split()[0])
        if a == b:
            return t_down()
        return _wq("Which is larger: %s or %s? Type it exactly as written." % (vals[0], vals[1]), vals[0] if a > b else vals[1],
                   ["%s = %s %s." % (vals[0], _ds(a), small)], "as written")

    return _pick_t([t_down, t_up, t_time, t_time_dec, t_add_mixed, t_order])


@skill("Y7.4.e", "Percentages over 100% and percentage change", S4)
def _(d=1):
    d = _d(d)

    def t_increase():
        x = random.randint(2, 40) * 10
        p = pick([10, 20, 25, 50, 15, 5])
        return _tb("Increase £%d by %d%%. Give the new amount in pounds." % (x, p), _ds(Fraction(x * (100 + p), 100)), "num",
                   {"unit": "£"}, ["%d%% of %d = %s." % (p, x, _ds(Fraction(x * p, 100))),
                                   "%d + %s = %s." % (x, _ds(Fraction(x * p, 100)), _ds(Fraction(x * (100 + p), 100)))])

    def t_decrease():
        x = random.randint(2, 40) * 10
        p = pick([10, 20, 25, 50, 30, 5])
        return _tb("Decrease %d kg by %d%%. Give the new amount in kg." % (x, p), _ds(Fraction(x * (100 - p), 100)), "num",
                   {"unit": "kg"}, ["%d%% of %d = %s." % (p, x, _ds(Fraction(x * p, 100)))])

    def t_over():
        x = random.randint(2, 20) * 20
        p = pick([150, 200, 120, 250, 300])
        return _tb("A town's population is %d%% of what it was 50 years ago, when it was %d. What is it now?" % (p, x),
                   x * p // 100, "int", {}, ["%d%% = × %s." % (p, _ds(Fraction(p, 100))), "%d × %s = %d." % (x, _ds(Fraction(p, 100)), x * p // 100)])

    def t_as_percent():
        a = random.randint(2, 20) * 5
        b = a + random.randint(1, 20) * 5
        return _tb("%d is what percentage of %d? Give the number only." % (b, a), _ds(Fraction(b * 100, a)), "num", {},
                   ["%d ÷ %d × 100 = %s." % (b, a, _ds(Fraction(b * 100, a)))]) if (b * 100) % a == 0 else t_increase()

    def t_multiplier():
        p = pick([110, 125, 150, 200, 85, 60])
        return _tb("Multiplying by %s is the same as finding what percentage of the amount? Give the number only."
                   % _ds(Fraction(p, 100)), p, "int", {}, ["%s × 100 = %d%%." % (_ds(Fraction(p, 100)), p)])

    def t_change():
        old = random.randint(2, 20) * 10
        p = pick([10, 20, 25, 50])
        new = old + old * p // 100 * pick([1, -1])
        up = new > old
        return _tb("A price changes from £%d to £%d. What is the percentage %s? Give the number only."
                   % (old, new, "increase" if up else "decrease"), abs(new - old) * 100 // old, "int", {},
                   ["Change £%d; %d ÷ %d × 100 = %d%%." % (abs(new - old), abs(new - old), old, abs(new - old) * 100 // old)])

    return _pick_t([t_increase, t_decrease, t_over, t_as_percent, t_multiplier, t_change])


@skill("Y7.5.f", "Perimeter and area problems with decimals", S5)
def _(d=1):
    d = _d(d)

    def t_rect_p():
        a, b = Decimal(random.randint(11, 99)) / 10, Decimal(random.randint(11, 99)) / 10
        return _tb("A rectangle is %s m by %s m. Find its perimeter, in m." % (_ds(a), _ds(b)), _ds(2 * (a + b)), "num",
                   {"unit": "m"}, ["2 × (%s + %s) = %s." % (_ds(a), _ds(b), _ds(2 * (a + b)))])

    def t_rect_a():
        a, b = Decimal(random.randint(11, 99)) / 10, random.randint(2, 12)
        return _tb("A rectangle is %s cm by %d cm. Find its area, in cm²." % (_ds(a), b), _ds(a * b), "num", {"unit": "cm²"},
                   ["%s × %d = %s." % (_ds(a), b, _ds(a * b))])

    def t_fence():
        a, b = random.randint(5, 30), random.randint(5, 30)
        price = Decimal(random.randint(150, 900)) / 100
        return _tb("A rectangular garden is %d m by %d m. Fencing costs £%s per metre. How much to fence all the way round, "
                   "in pounds?" % (a, b, format(price, ".2f")), _ds(2 * (a + b) * price), "num", {"unit": "£"},
                   ["Perimeter %d m." % (2 * (a + b)), "%d × %s = %s." % (2 * (a + b), format(price, ".2f"), _ds(2 * (a + b) * price))])

    def t_tiles():
        a, b = random.randint(2, 8), random.randint(2, 8)
        t = pick([Decimal("0.5"), Decimal("0.25")])
        n = (a / t) * (b / t)
        return _tb("A floor is %d m by %d m. Square tiles are %s m wide. How many tiles cover the floor exactly?" % (a, b, _ds(t)),
                   int(n), "int", {"unit": "tiles"}, ["%d × %d tiles." % (int(a / t), int(b / t))])

    def t_missing():
        a = Decimal(random.randint(11, 99)) / 10
        b = random.randint(2, 9)
        return _tb("A rectangle has area %s cm² and width %d cm. What is its length, in cm?" % (_ds(a * b), b), _ds(a), "num",
                   {"unit": "cm"}, ["%s ÷ %d = %s." % (_ds(a * b), b, _ds(a))])

    return _pick_t([t_rect_p, t_rect_a, t_fence, t_tiles, t_missing])


@skill("Y7.8.h", "Coordinates in all four quadrants", S8)
def _(d=1):
    d = _d(d)
    x, y = random.randint(-6, 6), random.randint(-6, 6)

    def t_plot():
        return {"prompt": "Plot the point (%d,%d)." % (x, y), "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7}, "answer": "(%d,%d)" % (x, y), "answer_type": "coord",
                "solution": ["Go %d along, then %d up or down." % (x, y)]}

    def t_quadrant():
        a, b = random.choice([-1, 1]) * random.randint(1, 9), random.choice([-1, 1]) * random.randint(1, 9)
        q = 1 if a > 0 and b > 0 else 2 if a < 0 < b else 3 if a < 0 and b < 0 else 4
        return _tb("Which quadrant is (%d,%d) in? (1, 2, 3 or 4, numbered anticlockwise from top right)" % (a, b), q, "int", {},
                   ["x is %s and y is %s." % ("positive" if a > 0 else "negative", "positive" if b > 0 else "negative")])

    def t_midpoint():
        a, b = random.randint(-6, 6), random.randint(-6, 6)
        c, e = a + 2 * random.randint(-3, 3), b + 2 * random.randint(-3, 3)
        return _wq("Find the midpoint of (%d,%d) and (%d,%d). Write it like (1,2)." % (a, b, c, e), "(%d,%d)" % ((a + c) // 2, (b + e) // 2),
                   ["Average the x's and the y's."], "(x,y)")

    def t_square():
        x0, y0 = random.randint(-5, 1), random.randint(-5, 1)
        s = random.randint(2, 4)
        pts = [[x0, y0, "A"], [x0 + s, y0, "B"], [x0 + s, y0 + s, "C"]]
        return {"prompt": "A, B and C are three corners of a square. Plot the fourth corner.", "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "points": pts}, "answer": "(%d,%d)" % (x0, y0 + s),
                "answer_type": "coord", "solution": ["(%d,%d)." % (x0, y0 + s)]}

    def t_axis():
        on = pick(["x", "y"])
        p = "(%d,0)" % random.randint(-8, 8) if on == "x" else "(0,%d)" % random.randint(-8, 8)
        return _wq("The point %s lies on which axis? (x or y)" % p, on, ["%s coordinate is 0." % ("The y" if on == "x" else "The x")],
                   "x or y")

    def t_distance():
        a = random.randint(-6, 0)
        b = random.randint(1, 6)
        y0 = random.randint(-5, 5)
        return _tb("How far apart are (%d,%d) and (%d,%d), in units?" % (a, y0, b, y0), b - a, "int", {},
                   ["Same y, so count along: %d − (%d) = %d." % (b, a, b - a)])

    return _pick_t([t_quadrant, t_midpoint, t_axis, t_distance], [t_plot, t_square])
