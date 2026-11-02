# Year 7 generators: strands 7.4, 7.5 and 7.6.
#
# Fractions, decimals and percentages: equivalence and conversion (terminating decimals), ordering,
# one quantity as a fraction or percentage of another, percentages over 100%, fractions and
# percentages of amounts as operators.  Applications of number: the four operations with integers
# and decimals, priority of operations, mental strategies, perimeter and money problems, frequency
# trees and two-way tables.  Directed number: ordering, the four operations, priority of operations
# and substitution with negatives.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S4 = "7.4 Fractions, decimals & percentages"
S5 = "7.5 Applications of number"
S6 = "7.6 Directed number"

TERM = [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5),
        Fraction(1, 8), Fraction(3, 8), Fraction(5, 8), Fraction(7, 8), Fraction(1, 10), Fraction(3, 10), Fraction(7, 20),
        Fraction(9, 25), Fraction(1, 20), Fraction(3, 50), Fraction(7, 2), Fraction(9, 4)]


def _neg(n):
    return "(%d)" % n if n < 0 else str(n)


# ================================================================== 7.4 ======
@skill("Y7.4.a", "Convert between fractions, decimals and percentages", S4)
def _(d=1):
    d = _d(d)
    f = pick(TERM[: _by(d, 7, 15, len(TERM))])

    def t_f_to_d():
        return _tb("Write %s as a decimal." % _fs(f), _ds(f), "num", {}, ["%d ÷ %d = %s." % (f.numerator, f.denominator, _ds(f))])

    def t_d_to_f():
        return _wq("Write %s as a fraction in its simplest form." % _ds(f), _fs(f),
                   ["%s = %s." % (_ds(f), _fs(f))], "e.g. 3/8")

    def t_f_to_p():
        return _tb("Write %s as a percentage. Give the number only." % _fs(f), _ds(f * 100), "num", {},
                   ["%s × 100 = %s%%." % (_fs(f), _ds(f * 100))])

    def t_p_to_d():
        p = Decimal(random.randint(1, 250)) / pick([1, 1, 10])
        return _tb("Write %s%% as a decimal." % _ds(p), _ds(p / 100), "num", {}, ["÷ 100: %s." % _ds(p / 100)])

    def t_table():
        fs = random.sample(TERM[:12], 3)
        rows = [[_fs(x), _ds(x), "%s%%" % _ds(x * 100)] for x in fs]
        r, c = random.randrange(3), pick([1, 2])
        ans = _ds(fs[r]) if c == 1 else _ds(fs[r] * 100)
        return _dt("Complete the table (for a percentage, type the number only).", ["Fraction", "Decimal", "Percentage"],
                   rows, ans, ["%s = %s = %s%%." % (_fs(fs[r]), _ds(fs[r]), _ds(fs[r] * 100))], missing=[r, c], atype="num")

    def t_eighths():
        k = pick([1, 3, 5, 7])
        return _tb("Write %d/8 as a decimal." % k, _ds(Fraction(k, 8)), "num", {},
                   ["1/8 = 0.125, so %d/8 = %s." % (k, _ds(Fraction(k, 8)))])

    return _pick_t([t_f_to_d, t_d_to_f, t_f_to_p, t_p_to_d, t_eighths], [t_table])


@skill("Y7.4.b", "Order fractions, decimals and percentages", S4)
def _(d=1):
    d = _d(d)
    pool = random.sample(TERM[:16], 4)
    shown = [pick([_fs(f), _ds(f), "%s%%" % _ds(f * 100)]) for f in pool]

    def t_largest():
        return _wq("Which is the largest?  %s  (type it as written)" % ", ".join(shown), shown[pool.index(max(pool))],
                   ["As decimals: %s." % ", ".join(_ds(f) for f in pool)], "as written")

    def t_smallest():
        return _wq("Which is the smallest?  %s  (type it as written)" % ", ".join(shown), shown[pool.index(min(pool))],
                   ["As decimals: %s." % ", ".join(_ds(f) for f in pool)], "as written")

    def t_compare():
        a, b = pool[0], pool[1]
        if a == b:
            return t_largest()
        return _wq("Write < or > :  %s ___ %s" % (shown[0], shown[1]), "<" if a < b else ">",
                   ["%s = %s and %s = %s." % (shown[0], _ds(a), shown[1], _ds(b))], "< or >")

    def t_line():
        f = pick(TERM[:12])
        return _nld("Place %s on the number line from 0 to 1." % pick([_fs(f), "%s%%" % _ds(f * 100)]), f, 0, 1,
                    Decimal("0.025"), Decimal("0.1"), ["It is %s." % _ds(f)])

    return _pick_t([t_largest, t_smallest, t_compare], [t_line])


@skill("Y7.4.c", "One quantity as a fraction or percentage of another", S4)
def _(d=1):
    d = _d(d)

    def t_fraction():
        b = pick([10, 12, 20, 24, 30, 40, 60])
        a = random.randint(1, b - 1)
        return _fq("What fraction of %d is %d? Give it in its simplest form." % (b, a), Fraction(a, b),
                   ["%d/%d = %s." % (a, b, _fs(Fraction(a, b)))])

    def t_percent():
        b = pick([20, 25, 40, 50, 80, 200])
        a = random.randint(1, b)
        while (a * 100) % b:
            a = random.randint(1, b)
        return _tb("What percentage of %d is %d? Give the number only." % (b, a), a * 100 // b, "int", {},
                   ["%d/%d = %d%%." % (a, b, a * 100 // b)])

    def t_minutes():
        m = pick([15, 20, 30, 40, 45, 12, 6])
        return _fq("What fraction of an hour is %d minutes? Simplest form." % m, Fraction(m, 60),
                   ["%d/60 = %s." % (m, _fs(Fraction(m, 60)))])

    def t_test():
        tot = pick([20, 25, 40, 50])
        sc = random.randint(tot // 3, tot)
        return _tb("%s scored %d out of %d. What percentage is that? Give the number only." % (_who(), sc, tot),
                   _ds(Fraction(sc * 100, tot)), "num", {}, ["%d ÷ %d × 100 = %s%%." % (sc, tot, _ds(Fraction(sc * 100, tot)))])

    def t_greater_one():
        b = random.randint(2, 9)
        a = b + random.randint(1, b)
        return _fq("What fraction of %d is %d? (It is more than 1.)" % (b, a), Fraction(a, b),
                   ["%d/%d." % (a, b)], "e.g. 7/4")

    def t_units():
        cm = random.randint(1, 19) * 5
        return _fq("What fraction of 1 metre is %d cm? Simplest form." % cm, Fraction(cm, 100),
                   ["%d/100 = %s." % (cm, _fs(Fraction(cm, 100)))])

    return _pick_t([t_fraction, t_percent, t_minutes, t_test, t_greater_one, t_units])


@skill("Y7.4.d", "Fractions and percentages of amounts", S4)
def _(d=1):
    d = _d(d)

    def t_fraction():
        den = pick([3, 4, 5, 6, 8, 10])
        num = random.randint(1, den - 1)
        x = den * random.randint(3, _by(d, 15, 40, 120))
        return _tb("Work out %d/%d of %d." % (num, den, x), x // den * num, "int", {},
                   ["%d ÷ %d × %d = %d." % (x, den, num, x // den * num)])

    def t_percent_easy():
        p = pick([10, 20, 25, 50, 75, 5, 1])
        x = pick([40, 60, 80, 120, 200, 360, 480])
        return _tb("Work out %d%% of %d." % (p, x), _ds(Fraction(p * x, 100)), "num", {},
                   ["%d%% of %d = %s." % (p, x, _ds(Fraction(p * x, 100)))])

    def t_percent_build():
        p = pick([15, 35, 45, 12, 65, 85])
        x = pick([20, 40, 60, 80, 200, 300])
        return _tb("Work out %d%% of %d. (Hint: build it from 10%% and 5%% or 1%%.)" % (p, x), _ds(Fraction(p * x, 100)),
                   "num", {}, ["10%% of %d = %s." % (x, _ds(Fraction(x, 10))), "%d%% = %s." % (p, _ds(Fraction(p * x, 100)))])

    def t_over_100():
        p = pick([110, 120, 125, 150, 200, 250])
        x = pick([20, 40, 60, 80, 100])
        return _tb("Work out %d%% of %d." % (p, x), _ds(Fraction(p * x, 100)), "num", {},
                   ["%d%% means %s times the amount." % (p, _ds(Fraction(p, 100))), "= %s." % _ds(Fraction(p * x, 100))])

    def t_money():
        price = random.randint(4, 40) * 5
        p = pick([10, 20, 25, 30, 40])
        return _tb("A jacket costs £%d. It is reduced by %d%%. What is the new price, in pounds?" % (price, p),
                   _ds(Fraction(price * (100 - p), 100)), "num", {"unit": "£"},
                   ["%d%% of %d = %s." % (p, price, _ds(Fraction(price * p, 100))),
                    "%d − %s = %s." % (price, _ds(Fraction(price * p, 100)), _ds(Fraction(price * (100 - p), 100)))])

    def t_multiplier():
        p = pick([10, 20, 35, 60, 75])
        up = random.random() < 0.5
        return _tb("To %s an amount by %d%%, what decimal do you multiply by?" % ("increase" if up else "decrease", p),
                   _ds(Fraction(100 + p if up else 100 - p, 100)), "num", {},
                   ["100%% %s %d%% = %d%% = %s." % ("+" if up else "−", p, 100 + p if up else 100 - p,
                                                    _ds(Fraction(100 + p if up else 100 - p, 100)))])

    def t_bar():
        x = random.randint(4, 30) * 10
        return _strip("The bar is %d split into 10 equal parts. What is 30%% of %d?" % (x, x),
                      {"mode": "equal_parts", "parts": 10, "partLabel": "?", "totalLabel": str(x), "unknown": "part"},
                      x * 3 // 10, ["One part is 10%% = %d." % (x // 10), "3 parts = %d." % (x * 3 // 10)])

    return _pick_t([t_fraction, t_percent_easy, t_percent_build, t_over_100, t_money, t_multiplier], [t_bar])


# ================================================================== 7.5 ======
@skill("Y7.5.a", "Add and subtract integers and decimals", S5)
def _(d=1):
    d = _d(d)

    def t_int():
        a, b = random.randint(1000, 99999), random.randint(1000, 99999)
        op = pick(["+", "−"])
        if op == "−" and b > a:
            a, b = b, a
        return _tb("Work out %s %s %s." % (_c(a), op, _c(b)), a + b if op == "+" else a - b, "int", {},
                   ["Use a column method."])

    def t_dec():
        a = Decimal(random.randint(100, 99999)) / pick([10, 100, 1000])
        b = Decimal(random.randint(100, 9999)) / pick([10, 100])
        op = pick(["+", "−"])
        if op == "−" and b > a:
            a, b = b, a
        return _tb("Work out %s %s %s." % (_ds(a), op, _ds(b)), _ds(a + b if op == "+" else a - b), "num", {},
                   ["Line up the decimal points."])

    def t_missing():
        a = Decimal(random.randint(100, 9999)) / 100
        b = Decimal(random.randint(100, 9999)) / 100
        return _tb("Find the missing number:  %s + ___ = %s" % (_ds(a), _ds(a + b)), _ds(b), "num", {},
                   ["%s − %s = %s." % (_ds(a + b), _ds(a), _ds(b))])

    def t_perimeter():
        sides = [Decimal(random.randint(15, 120)) / 10 for _ in range(pick([3, 4, 5]))]
        return _tb("A shape has sides of %s cm. What is its perimeter, in cm?" % ", ".join(_ds(s) for s in sides),
                   _ds(sum(sides)), "num", {"unit": "cm"}, ["%s = %s." % (" + ".join(_ds(s) for s in sides), _ds(sum(sides)))])

    def t_money():
        items = [Decimal(random.randint(99, 1999)) / 100 for _ in range(3)]
        pay = pick([20, 50])
        if sum(items) >= pay:
            pay = 100
        return _tb("Items cost £%s. How much change from £%d, in pounds?" % (", £".join(format(i, ".2f") for i in items), pay),
                   _ds(pay - sum(items)), "num", {"unit": "£"},
                   ["Total £%s." % format(sum(items), ".2f"), "£%d − £%s = £%s." % (pay, format(sum(items), ".2f"),
                                                                                   format(pay - sum(items), ".2f"))])

    return _pick_t([t_int, t_dec, t_missing, t_perimeter, t_money])


@skill("Y7.5.b", "Multiply and divide integers and decimals", S5)
def _(d=1):
    d = _d(d)

    def t_long_mult():
        a, b = random.randint(100, 999), random.randint(12, 99)
        return _tb("Work out %d × %d." % (a, b), a * b, "int", {}, ["Use long multiplication: %s." % _c(a * b)])

    def t_dec_mult():
        a = Decimal(random.randint(11, 999)) / 10
        b = random.randint(2, 9) if d < 2 else Decimal(random.randint(2, 9)) / 10
        return _tb("Work out %s × %s." % (_ds(a), _ds(b)), _ds(a * b), "num", {}, ["= %s." % _ds(a * b)])

    def t_long_div():
        q, k = random.randint(21, 299), random.randint(12, 35)
        return _tb("Work out %s ÷ %d." % (_c(q * k), k), q, "int", {}, ["Use long or short division: %d." % q])

    def t_dec_div():
        q = Decimal(random.randint(11, 999)) / 100
        k = random.randint(2, 9)
        return _tb("Work out %s ÷ %d." % (_ds(q * k), k), _ds(q), "num", {}, ["= %s." % _ds(q)])

    def t_dec_by_dec():
        q, k = random.randint(2, 90), Decimal(pick(["0.2", "0.5", "0.4", "0.25", "0.1"]))
        return _tb("Work out %s ÷ %s." % (_ds(q * k), _ds(k)), q, "int", {},
                   ["Multiply both by %d to remove the decimal." % (100 if k == Decimal("0.25") else 10)])

    def t_related():
        a, b = random.randint(12, 99), random.randint(12, 99)
        return _tb("Given %d × %d = %s, work out %s × %s." % (a, b, _c(a * b), _ds(Decimal(a) / 10), _ds(Decimal(b) / 10)),
                   _ds(Decimal(a * b) / 100), "num", {}, ["Both numbers are ÷ 10, so the answer is ÷ 100."])

    def t_area():
        a = Decimal(random.randint(11, 99)) / 10
        b = random.randint(2, 12)
        return _tb("A rectangle is %s m by %d m. What is its area, in m²?" % (_ds(a), b), _ds(a * b), "num",
                   {"unit": "m²"}, ["%s × %d = %s." % (_ds(a), b, _ds(a * b))])

    return _pick_t([t_long_mult, t_dec_mult, t_long_div, t_dec_div, t_dec_by_dec, t_related, t_area])


@skill("Y7.5.c", "Priority of operations (brackets, powers, ×÷, +−)", S5)
def _(d=1):
    d = _d(d)
    a, b, c, e = [random.randint(2, 12) for _ in range(4)]

    def t_basic():
        return _tb("Work out  %d + %d × %d" % (a, b, c), a + b * c, "int", {}, ["× first: %d; then + %d = %d." % (b * c, a, a + b * c)])

    def t_brackets():
        return _tb("Work out  (%d + %d) × %d" % (a, b, c), (a + b) * c, "int", {}, ["Brackets first: %d." % (a + b)])

    def t_power():
        return _tb("Work out  %d + %d²" % (a, b), a + b * b, "int", {}, ["Powers first: %d² = %d." % (b, b * b)])

    def t_divide():
        q = random.randint(2, 9)
        return _tb("Work out  %d − %d ÷ %d" % (a + 20, b * q, b), a + 20 - q, "int", {}, ["÷ first: %d." % q])

    def t_mixed():
        return _tb("Work out  %d × %d − %d × %d" % (a, b, c, e), a * b - c * e, "int", {},
                   ["%d − %d = %d." % (a * b, c * e, a * b - c * e)])

    def t_place():
        tgt = (a + b) * c
        if tgt == a + b * c:
            return t_basic()
        return _wq("Brackets are added to  %d + %d × %d  to make it equal %d. What goes inside the brackets? Type it like "
                   "2+3." % (a, b, c, tgt), "%d+%d" % (a, b), ["(%d + %d) × %d = %d." % (a, b, c, tgt)], "e.g. 2+3")

    def t_root():
        k = random.randint(2, 12)
        return _tb("Work out  %d + √%d × %d" % (a, k * k, c), a + k * c, "int", {}, ["√%d = %d; × %d = %d; + %d." % (k * k, k, c, k * c, a)])

    return _pick_t([t_basic, t_brackets, t_power, t_divide, t_mixed, t_place, t_root])


@skill("Y7.5.d", "Mental strategies and inverse operations", S5)
def _(d=1):
    d = _d(d)

    def t_compensate():
        a = random.randint(100, 900)
        b = pick([99, 199, 299, 98, 49])
        r = (b // 50 + 1) * 50 if b % 50 else b
        return _tb("Work out %d + %d in your head. (Hint: add a round number, then adjust.)" % (a, b), a + b, "int", {},
                   ["%d + %d = %d, then take away %d: %d." % (a, r, a + r, r - b, a + b)])

    def t_double_half():
        a, b = random.randint(11, 49) * 2, pick([5, 50, 25])
        return _tb("Work out %d × %d. (Hint: halve one number and double the other.)" % (a, b), a * b, "int", {},
                   ["%d × %d = %d." % (a // 2, b * 2, a * b)])

    def t_inverse():
        a, b = random.randint(100, 999), random.randint(12, 99)
        return _tb("%d × %d = %s. What is %s ÷ %d?" % (a, b, _c(a * b), _c(a * b), a), b, "int", {},
                   ["Division undoes multiplication."])

    def t_check():
        a, b = random.randint(1000, 9999), random.randint(1000, 9999)
        return _tb("To check %s + %s = %s using the inverse, what subtraction gives back %s? Type the answer of %s − %s."
                   % (_c(a), _c(b), _c(a + b), _c(a), _c(a + b), _c(b)), a, "int", {}, ["%s − %s = %s." % (_c(a + b), _c(b), _c(a))])

    def t_partition():
        a, b = random.randint(11, 49), random.randint(3, 9)
        return _tb("Work out %d × %d by partitioning." % (a, b), a * b, "int", {},
                   ["%d × %d + %d × %d = %d." % ((a // 10) * 10, b, a % 10, b, a * b)])

    return _pick_t([t_compensate, t_double_half, t_inverse, t_check, t_partition])


@skill("Y7.5.e", "Frequency trees and two-way tables", S5)
def _(d=1):
    d = _d(d)
    boys, girls = random.randint(10, 40), random.randint(10, 40)
    bl, gl = random.randint(1, boys - 1), random.randint(1, girls - 1)

    def t_two_way_total():
        rows = [["Boys", bl, boys - bl, boys], ["Girls", gl, girls - gl, girls], ["Total", bl + gl, boys + girls - bl - gl,
                                                                                  boys + girls]]
        r, c = random.randrange(3), random.randint(1, 3)
        return _dt("The two-way table shows pupils who have school lunch or packed lunch. What number is missing?",
                   ["", "School lunch", "Packed lunch", "Total"], rows, rows[r][c],
                   ["Rows and columns add up to their totals."], missing=[r, c])

    def t_two_way_read():
        rows = [["Boys", bl, boys - bl], ["Girls", gl, girls - gl]]
        return _dt("How many pupils have packed lunch altogether?", ["", "School lunch", "Packed lunch"], rows,
                   boys + girls - bl - gl, ["%d + %d = %d." % (boys - bl, girls - gl, boys + girls - bl - gl)])

    def t_tree():
        tot = boys + girls
        return _tb("A frequency tree starts with %d pupils. %d are boys. Of the girls, %d walk to school. How many girls do "
                   "NOT walk?" % (tot, boys, gl), girls - gl, "int", {},
                   ["Girls: %d − %d = %d." % (tot, boys, girls), "%d − %d = %d." % (girls, gl, girls - gl)])

    def t_fraction():
        rows = [["Boys", bl, boys - bl], ["Girls", gl, girls - gl]]
        return _dt("What fraction of the boys have school lunch? Simplest form.", ["", "School lunch", "Packed lunch"], rows,
                   _fs(Fraction(bl, boys)), ["%d out of %d = %s." % (bl, boys, _fs(Fraction(bl, boys)))], atype="frac")

    return _pick_t([t_tree], [t_two_way_total, t_two_way_read, t_fraction])


# ================================================================== 7.6 ======
@skill("Y7.6.a", "Order and compare directed numbers", S6)
def _(d=1):
    d = _d(d)
    vals = random.sample(range(-30, 30), 5)

    def t_smallest():
        return _tb("Which is the smallest?  %s" % ", ".join(map(str, vals)), min(vals), "int", {},
                   ["The most negative number is the smallest."])

    def t_symbol():
        a, b = vals[0], vals[1]
        return _wq("Write < or > :  %d ___ %d" % (a, b), "<" if a < b else ">", ["Further left on the number line is smaller."],
                   "< or >")

    def t_between():
        a, b = sorted(random.sample(range(-15, 15), 2))
        return _tb("How many whole numbers are strictly between %d and %d?" % (a, b), max(0, b - a - 1), "int", {},
                   ["%d − %d − 1 = %d." % (b, a, max(0, b - a - 1))])

    def t_midpoint():
        a = random.randint(-20, -2)
        b = a + 2 * random.randint(2, 12)
        return _tb("What number is halfway between %d and %d?" % (a, b), (a + b) // 2, "int", {}, ["(%d + %d) ÷ 2 = %d." % (a, b, (a + b) // 2)])

    def t_line():
        v = random.randint(-9, 9)
        return _nl("Place %d on the number line." % v, v, 1, 5, ["Count from 0."], lo=-10, hi=10)

    def t_temps():
        cities = ["Oslo", "Rome", "Kyiv", "Lima"]
        t = random.sample(range(-15, 20), 4)
        k = pick(["coldest", "warmest"])
        ans = cities[t.index(min(t) if k == "coldest" else max(t))]
        return _dt("Which city was the %s?" % k, ["City", "Temperature"], [[c, "%d °C" % x] for c, x in zip(cities, t)],
                   ans, ["%s: %d °C." % (ans, min(t) if k == "coldest" else max(t))], atype="str")

    return _pick_t([t_smallest, t_symbol, t_between, t_midpoint], [t_line, t_temps])


@skill("Y7.6.b", "Add and subtract directed numbers", S6)
def _(d=1):
    d = _d(d)
    a, b = random.randint(-15, 15), random.randint(-15, 15)

    def t_add():
        return _tb("Work out  %d + %s" % (a, _neg(b)), a + b, "int", {},
                   ["Adding a negative is the same as subtracting." if b < 0 else "Count on %d." % b])

    def t_sub():
        return _tb("Work out  %d − %s" % (a, _neg(b)), a - b, "int", {},
                   ["Subtracting a negative is the same as adding." if b < 0 else "Count back %d." % b])

    def t_temperature():
        t0, ch = random.randint(-8, 5), random.randint(3, 15)
        return _tb("The temperature is %d °C. It falls by %d degrees. What is it now, in °C?" % (t0, ch), t0 - ch, "int",
                   {"unit": "°C"}, ["%d − %d = %d." % (t0, ch, t0 - ch)])

    def t_difference():
        x, y = random.randint(-20, -1), random.randint(1, 20)
        return _tb("What is the difference between %d and %d?" % (x, y), y - x, "int", {}, ["%d − %s = %d." % (y, _neg(x), y - x)])

    def t_missing():
        return _tb("Find the missing number:  %d + ___ = %d" % (a, a + b), b, "int", {}, ["%d − %s = %d." % (a + b, _neg(a), b)])

    def t_bank():
        bal, spend = random.randint(5, 50), random.randint(10, 90)
        return _tb("A bank account has £%d. £%d is spent. What is the balance now, in pounds? (use a minus sign if it is "
                   "overdrawn)" % (bal, spend), bal - spend, "int", {"unit": "£"}, ["%d − %d = %d." % (bal, spend, bal - spend)])

    return _pick_t([t_add, t_sub, t_temperature, t_difference, t_missing, t_bank])


@skill("Y7.6.c", "Multiply and divide directed numbers", S6)
def _(d=1):
    d = _d(d)
    a, b = random.choice([-1, 1]) * random.randint(2, 12), random.choice([-1, 1]) * random.randint(2, 12)
    if a > 0 and b > 0:                    # directed-number practice: at least one negative
        a = -a

    def t_mult():
        return _tb("Work out  %s × %s" % (_neg(a), _neg(b)), a * b, "int", {},
                   ["Same signs give a positive; different signs give a negative."])

    def t_div():
        return _tb("Work out  %s ÷ %s" % (_neg(a * b), _neg(b)), a, "int", {}, ["Same rule for signs as multiplication."])

    def t_square():
        k = random.randint(2, 12)
        return _tb("Work out  (−%d)²" % k, k * k, "int", {}, ["(−%d) × (−%d) = %d." % (k, k, k * k)])

    def t_three():
        x, y, z = [random.choice([-1, 1]) * random.randint(2, 5) for _ in range(3)]
        return _tb("Work out  %s × %s × %s" % (_neg(x), _neg(y), _neg(z)), x * y * z, "int", {},
                   ["%d negative sign%s." % (sum(1 for v in (x, y, z) if v < 0),
                                            "" if sum(1 for v in (x, y, z) if v < 0) == 1 else "s")])

    def t_missing():
        return _tb("Find the missing number:  %s × ___ = %d" % (_neg(a), a * b), b, "int", {}, ["%d ÷ %s = %d." % (a * b, _neg(a), b)])

    def t_sign():
        return _wq("Is the answer to %s × %s positive or negative?" % (_neg(a), _neg(b)), "positive" if a * b > 0 else "negative",
                   ["%s." % ("Same signs" if a * b > 0 else "Different signs")], "positive / negative")

    return _pick_t([t_mult, t_div, t_square, t_three, t_missing, t_sign])


@skill("Y7.6.d", "Directed numbers: priority of operations and substitution", S6)
def _(d=1):
    d = _d(d)
    x = random.randint(-9, -1)
    y = random.randint(-6, 6) or 2

    def t_sub_linear():
        m, c = random.randint(2, 8), random.randint(-10, 10)
        return _tb("Find the value of %dx %s when x = %d." % (m, "+ %d" % c if c >= 0 else "− %d" % -c, x), m * x + c,
                   "int", {}, ["%d × (%d) %s %d = %d." % (m, x, "+" if c >= 0 else "−", abs(c), m * x + c)])

    def t_sub_square():
        return _tb("Find the value of x² when x = %d." % x, x * x, "int", {}, ["(%d)² = %d." % (x, x * x)])

    def t_sub_two():
        return _tb("Find the value of 3a − 2b when a = %d and b = %d." % (x, y), 3 * x - 2 * y, "int", {},
                   ["3 × (%d) − 2 × (%d) = %d." % (x, y, 3 * x - 2 * y)])

    def t_order():
        a, b, c = random.randint(-9, 9), random.randint(-6, -2), random.randint(2, 6)
        return _tb("Work out  %d + %s × %d" % (a, _neg(b), c), a + b * c, "int", {}, ["× first: %d." % (b * c)])

    def t_brackets():
        a, b, c = random.randint(-9, 9), random.randint(-9, 9), random.randint(-5, -2)
        return _tb("Work out  (%d + %s) × %s" % (a, _neg(b), _neg(c)), (a + b) * c, "int", {}, ["Brackets: %d." % (a + b)])

    def t_table():
        m, c = random.randint(2, 5), random.randint(-5, 5)
        rows = [[v, m * v + c] for v in (-3, -1, 0, 2)]
        k = random.randrange(4)
        return _io("Complete the table for y = %dx %s." % (m, "+ %d" % c if c >= 0 else "− %d" % -c), rows, k, rows[k][1],
                   ["%d × (%d) %s %d = %d." % (m, rows[k][0], "+" if c >= 0 else "−", abs(c), rows[k][1])])

    return _pick_t([t_sub_linear, t_sub_square, t_sub_two, t_order, t_brackets], [t_table])
