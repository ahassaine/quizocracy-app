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

    def t_p_to_f():
        p = pick([5, 12, 15, 35, 45, 64, 72, 85, 2, 8, 24, 55])
        return _wq("Write %d%% as a fraction in its simplest form." % p, _fs(Fraction(p, 100)),
                   ["%d/100 = %s." % (p, _fs(Fraction(p, 100)))])

    def t_d_to_p():
        x = Decimal(random.randint(1, 1999)) / pick([100, 1000])
        return _tb("Write %s as a percentage. Give the number only." % _ds(x), _ds(x * 100), "num", {},
                   ["× 100: %s%%." % _ds(x * 100)])

    def t_grid():
        k = random.randint(3, 97)
        return _area("What percentage of the grid is shaded? Give the number only.",
                     {"mode": "fraction_read", "parts": 100, "shaded": k, "rows": 10, "cols": 10}, k,
                     ["%d of the 100 squares: %d%%." % (k, k)])

    def t_mixed_number():
        w = random.randint(1, 5)
        f = pick([Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 8), Fraction(7, 20)])
        return _wq("Write %s as a mixed number in its simplest form." % _ds(w + f), _mixed(w + f),
                   ["%s = %d + %s = %s." % (_ds(w + f), w, _ds(f), _mixed(w + f))], "e.g. 2 3/4")

    def t_f_to_p_hard():
        f = pick([Fraction(3, 8), Fraction(1, 8), Fraction(7, 40), Fraction(9, 16), Fraction(5, 16), Fraction(11, 25)])
        return _tb("Write %s as a percentage. Give the number only." % _fs(f), _ds(f * 100), "num", {},
                   ["%s = %s = %s%%." % (_fs(f), _ds(f), _ds(f * 100))])

    def t_error():
        p = pick([3, 5, 7, 4, 9, 6])
        return _tb("%s says %d%% = 0.%d. What is %d%% as a decimal?" % (_who(), p, p, p), _ds(Fraction(p, 100)), "num", {},
                   ["%d ÷ 100 = %s." % (p, _ds(Fraction(p, 100)))])

    def t_p_to_mixed():
        p = pick([125, 150, 175, 220, 240, 260, 305, 450])
        return _wq("Write %d%% as a mixed number in its simplest form." % p, _mixed(Fraction(p, 100)),
                   ["%d%% = %d/100 = %s." % (p, p, _mixed(Fraction(p, 100)))], "e.g. 1 3/4")

    def t_thousandths():
        n = pick([5, 15, 25, 45, 75, 125, 375, 8, 64])
        return _wq("Write 0.%03d as a fraction in its simplest form." % n, _fs(Fraction(n, 1000)),
                   ["%d/1000 = %s." % (n, _fs(Fraction(n, 1000)))])

    def t_same():
        f = pick(TERM[:15])
        shown = f if random.random() < 0.5 else f + pick([Fraction(1, 100), Fraction(1, 20), Fraction(1, 10)])
        return _wq("Is %s equal to %s%%? (yes or no)" % (_fs(f), _ds(shown * 100)), "yes" if shown == f else "no",
                   ["%s = %s%%." % (_fs(f), _ds(f * 100))], "yes / no")

    return _pick_t([t_f_to_d, t_d_to_f, t_f_to_p, t_p_to_d, t_eighths, t_p_to_f, t_d_to_p, t_mixed_number, t_f_to_p_hard,
                    t_error, t_p_to_mixed, t_thousandths, t_same], [t_table, t_grid])


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

    def t_money():
        p = pick([5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80])
        pounds = pick([1, 2, 3, 4, 5])
        return _fq("What fraction of £%d is %dp? Simplest form." % (pounds, p), Fraction(p, 100 * pounds),
                   ["£%d = %dp, so %d/%d = %s." % (pounds, 100 * pounds, p, 100 * pounds, _fs(Fraction(p, 100 * pounds)))])

    def t_over_100():
        b = pick([20, 40, 50, 80])
        pct = pick([p for p in (105, 110, 120, 125, 150, 175, 200, 250) if (b * p) % 100 == 0])
        a = b * pct // 100
        return _tb("What percentage of %d is %d? Give the number only." % (b, a), a * 100 // b, "int", {},
                   ["%d ÷ %d × 100 = %d%%." % (a, b, a * 100 // b)])

    def t_decimal_pct():
        b = pick([8, 16, 40])
        a = random.randint(1, b - 1)
        return _tb("What percentage of %d is %d? Give the number only." % (b, a), _ds(Fraction(a * 100, b)), "num", {},
                   ["%d ÷ %d = %s = %s%%." % (a, b, _ds(Fraction(a, b)), _ds(Fraction(a * 100, b)))])

    def t_better():
        n1, n2 = random.sample([20, 25, 40, 50], 2)
        s1, s2 = random.randint(n1 // 2, n1), random.randint(n2 // 2, n2)
        if Fraction(s1, n1) == Fraction(s2, n2):
            s2 = s2 - 1 if s2 > n2 // 2 else s2 + 1
        a, b = _who(), _who()
        while b == a:
            b = _who()
        win = a if Fraction(s1, n1) > Fraction(s2, n2) else b
        return _wq("%s scored %d out of %d in a test and %s scored %d out of %d. Who did better? (type the name)"
                   % (a, s1, n1, b, s2, n2), win,
                   ["%s: %s%%. %s: %s%%." % (a, _ds(Fraction(s1 * 100, n1)), b, _ds(Fraction(s2 * 100, n2)))], "name")

    def t_bar():
        cats = ["Red", "Blue", "Green", "Yellow"]
        tot = pick([20, 25, 50])
        v = [random.randint(1, tot // 3) for _ in range(3)]
        v.append(tot - sum(v))
        k = random.randrange(4)
        return _bar("The bar chart shows the favourite colours of %d pupils. What percentage chose %s? Give the number only."
                    % (tot, cats[k]), cats, v, _ds(Fraction(v[k] * 100, tot)),
                    ["%d out of %d = %s%%." % (v[k], tot, _ds(Fraction(v[k] * 100, tot)))], atype="num")

    def t_time_units():
        s = pick([15, 20, 30, 40, 45, 12, 36])
        return _fq("What fraction of a minute is %d seconds? Simplest form." % s, Fraction(s, 60),
                   ["%d/60 = %s." % (s, _fs(Fraction(s, 60)))])

    def t_distance():
        m = pick([100, 200, 250, 400, 500, 600, 750, 800])
        km = pick([1, 2, 4, 5])
        return _tb("What percentage of %d km is %d m? Give the number only." % (km, m), _ds(Fraction(m * 100, km * 1000)), "num", {},
                   ["%d km = %s m." % (km, _c(km * 1000)), "%d ÷ %s × 100 = %s%%." % (m, _c(km * 1000), _ds(Fraction(m * 100, km * 1000)))])

    def t_mass():
        g = pick([50, 100, 125, 200, 250, 400, 600, 750])
        return _fq("What fraction of 1 kg is %d g? Simplest form." % g, Fraction(g, 1000), ["%d/1000 = %s." % (g, _fs(Fraction(g, 1000)))])

    return _pick_t([t_fraction, t_percent, t_minutes, t_test, t_greater_one, t_units, t_money, t_over_100, t_decimal_pct,
                    t_better, t_time_units, t_distance, t_mass], [t_bar])


@skill("Y7.4.d", "Fractions and percentages of amounts", S4)
def _(d=1):
    d = _d(d)

    def t_fraction():
        den = pick([3, 4, 5, 6, 8, 10])
        num = pick([k for k in range(1, den) if Fraction(k, den).denominator == den])
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
        x = pick([20, 40, 60, 80, 120])
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

    def t_money_frac():
        den = pick([4, 5, 8, 10, 20])
        num = pick([k for k in range(1, den) if Fraction(k, den).denominator == den])
        x = pick([10, 20, 30, 40, 50, 60])
        return _tb("Work out %d/%d of £%d, in pounds." % (num, den, x), _ds(Fraction(num * x, den)), "num", {"unit": "£"},
                   ["£%d ÷ %d × %d = £%s." % (x, den, num, format(Decimal(num * x) / den, ".2f"))])

    def t_swap():
        a, b = pick([(4, 75), (8, 25), (2, 50), (16, 25), (12, 50), (6, 50), (3, 200), (24, 25)])
        return _tb("Work out %d%% of %d. (Hint: %d%% of %d is the same.)" % (a, b, b, a), _ds(Fraction(a * b, 100)), "num", {},
                   ["%d%% of %d = %s, and x%% of y = y%% of x." % (b, a, _ds(Fraction(a * b, 100)))])

    def t_vat():
        price = random.randint(3, 60) * 5
        return _tb("A bike costs £%d before VAT. VAT of 20%% is added. What is the price with VAT, in pounds?" % price,
                   price * 6 // 5, "int", {"unit": "£"}, ["20%% of %d = %d." % (price, price // 5), "%d + %d = %d." % (price, price // 5, price * 6 // 5)])

    def t_half_pct():
        x = pick([40, 80, 120, 160, 200, 240, 400])
        p = pick([Decimal("12.5"), Decimal("2.5"), Decimal("7.5"), Decimal("17.5")])
        return _tb("Work out %s%% of %d." % (_ds(p), x), _ds(p * x / 100), "num", {},
                   ["1%% of %d = %s; × %s = %s." % (x, _ds(Decimal(x) / 100), _ds(p), _ds(p * x / 100))])

    def t_bigger_offer():
        p1, f1 = pick([(30, Fraction(1, 4)), (20, Fraction(1, 4)), (40, Fraction(1, 3)), (60, Fraction(2, 3)), (35, Fraction(2, 5))])
        x = pick([v for v in range(40, 241, 10) if (v * p1) % 100 == 0 and (v * f1).denominator == 1])
        a, b = Fraction(x * p1, 100), x * f1          # never equal: each pair differs as a proportion
        return _wq("Which is bigger: %d%% of £%d or %s of £%d? (type percent or fraction)" % (p1, x, _fs(f1), x),
                   "percent" if a > b else "fraction",
                   ["%d%% of %d = %s; %s of %d = %s." % (p1, x, _fs(a), _fs(f1), x, _fs(b))], "percent / fraction")

    def t_left():
        x = random.randint(2, 30) * 10
        p = pick([10, 20, 30, 40, 60, 70, 15, 35])
        return _tb("%s has £%d and spends %d%% of it. How much is left, in pounds?" % (_who(), x, p), _ds(Fraction(x * (100 - p), 100)),
                   "num", {"unit": "£"}, ["%d%% is left: %d%% of %d = %s." % (100 - p, 100 - p, x, _ds(Fraction(x * (100 - p), 100)))])

    def t_frac_then_pct():
        x = random.randint(2, 12) * 40
        return _tb("A farmer has %d sheep. 3/4 of them are white, and 10%% of the white sheep have lambs. How many white sheep "
                   "have lambs?" % x, x * 3 // 40, "int", {"unit": "sheep"},
                   ["3/4 of %d = %d." % (x, x * 3 // 4), "10%% of %d = %d." % (x * 3 // 4, x * 3 // 40)])

    return _pick_t([t_fraction, t_percent_easy, t_percent_build, t_over_100, t_money, t_multiplier, t_money_frac, t_swap,
                    t_vat, t_half_pct, t_bigger_offer, t_left, t_frac_then_pct], [t_bar])


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

    def t_minus_missing():
        a = Decimal(random.randint(100, 9999)) / 100
        b = Decimal(random.randint(100, 9999)) / 100
        return _tb("Find the missing number:  ___ − %s = %s" % (_ds(a), _ds(b)), _ds(a + b), "num", {},
                   ["Add back: %s + %s = %s." % (_ds(b), _ds(a), _ds(a + b))])

    def t_receipt():
        items = random.sample(["Bread", "Milk", "Eggs", "Apples", "Cheese", "Juice"], 3)
        prices = [Decimal(random.randint(45, 499)) / 100 for _ in items]
        rows = [[i, format(p, ".2f")] for i, p in zip(items, prices)] + [["Total", format(sum(prices), ".2f")]]
        k = random.randrange(3)
        return _dt("A till receipt is shown, with one price missing. What is the missing price, in pounds?", ["Item", "Price (£)"],
                   rows, _ds(prices[k]), ["%s − %s = %s." % (format(sum(prices), ".2f"),
                                                            format(sum(prices) - prices[k], ".2f"), format(prices[k], ".2f"))],
                   missing=[k, 1], atype="num")

    def t_journey():
        legs = [Decimal(random.randint(12, 250)) / 10 for _ in range(3)]
        tot = sum(legs)
        return _tb("A cyclist rides %s km, then %s km, then %s km. How much further must they ride to make %s km in total?"
                   % (_ds(legs[0]), _ds(legs[1]), _ds(legs[2]), _ds(tot.to_integral_value(rounding="ROUND_CEILING") + 5)),
                   _ds(tot.to_integral_value(rounding="ROUND_CEILING") + 5 - tot), "num", {"unit": "km"},
                   ["So far %s km." % _ds(tot), "%s − %s = %s." % (_ds(tot.to_integral_value(rounding="ROUND_CEILING") + 5), _ds(tot),
                                                                   _ds(tot.to_integral_value(rounding="ROUND_CEILING") + 5 - tot))])

    def t_temps_line():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        v = [Decimal(random.randint(80, 250)) / 10 for _ in days]
        i, j = random.sample(range(5), 2)
        return _lg("The graph shows the midday temperature each day. How much warmer was it on %s than on %s, in °C?"
                   % (days[i], days[j]) if v[i] > v[j] else
                   "The graph shows the midday temperature each day. How much colder was it on %s than on %s, in °C?"
                   % (days[i], days[j]), [(dd, float(t)) for dd, t in zip(days, v)], _ds(abs(v[i] - v[j])),
                   ["%s and %s: difference %s." % (_ds(v[i]), _ds(v[j]), _ds(abs(v[i] - v[j])))], "°C", "Day", atype="num")

    def t_neg_answer():
        a = random.randint(100, 999)
        b = a + random.randint(50, 900)
        return _tb("Work out %d − %d." % (a, b), a - b, "int", {}, ["%d − %d = %d, and %d is bigger than %d, so %d − %d = −%d." % (b, a, b - a, b, a, a, b, b - a)])

    return _pick_t([t_int, t_dec, t_missing, t_perimeter, t_money, t_minus_missing, t_journey, t_neg_answer],
                   [t_receipt, t_temps_line])


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

    def t_unit_cost():
        n = random.randint(3, 9)
        each = Decimal(random.randint(25, 199)) / 100
        return _tb("%d pens cost £%s. How much does one pen cost, in pounds?" % (n, format(each * n, ".2f")), _ds(each), "num",
                   {"unit": "£"}, ["£%s ÷ %d = £%s." % (format(each * n, ".2f"), n, format(each, ".2f"))])

    def t_dd():
        a, b = Decimal(random.randint(1, 9)) / 10, Decimal(random.randint(1, 9)) / 10
        if random.random() < 0.5:
            b = Decimal(random.randint(11, 39)) / 10
        return _tb("Work out %s × %s." % (_ds(a), _ds(b)), _ds(a * b), "num", {},
                   ["%d × %d = %d, and there are %d decimal places in total." % (int(a * 10), int(b * 10), int(a * b * 100), 2)])

    def t_exchange():
        rate = pick([Decimal("1.15"), Decimal("1.18"), Decimal("1.25"), Decimal("1.3"), Decimal("1.12")])
        cur = pick(["euros", "dollars"])
        x = random.randint(2, 40) * 5
        return _tb("£1 = %s %s. How many %s do you get for £%d?" % (_ds(rate), cur, cur, x), _ds(rate * x), "num", {"unit": cur},
                   ["%d × %s = %s." % (x, _ds(rate), _ds(rate * x))])

    def t_glasses():
        g = pick([Decimal("0.2"), Decimal("0.25"), Decimal("0.3"), Decimal("0.4")])
        n = random.randint(4, 20)
        return _tb("How many %s litre glasses can be filled from %s litre%s of juice?" % (_ds(g), _ds(g * n), "" if g * n == 1 else "s"), n,
                   "int",
                   {"unit": "glasses"}, ["%s ÷ %s = %d." % (_ds(g * n), _ds(g), n)])

    def t_map():
        s = pick([Decimal("2.5"), Decimal("1.5"), Decimal("0.5"), 2, 5])
        cm = Decimal(random.randint(12, 98)) / 10
        return _tb("On a map, 1 cm stands for %s km. Two towns are %s cm apart on the map. How far apart are they really, in km?"
                   % (_ds(s), _ds(cm)), _ds(cm * s), "num", {"unit": "km"}, ["%s × %s = %s." % (_ds(cm), _ds(s), _ds(cm * s))])

    def t_div_decimal_answer():
        a = random.randint(2, 9)
        q = Decimal(random.randint(11, 999)) / 10
        if (q * a) % 1 == 0:
            q += Decimal("0.1")
        return _tb("Share £%s equally between %d people. How much does each get, in pounds?" % (format(q * a, ".2f"), a), _ds(q),
                   "num", {"unit": "£"}, ["£%s ÷ %d = £%s." % (format(q * a, ".2f"), a, format(q, ".2f"))])

    return _pick_t([t_long_mult, t_dec_mult, t_long_div, t_dec_div, t_dec_by_dec, t_related, t_area, t_unit_cost, t_dd,
                    t_exchange, t_glasses, t_map, t_div_decimal_answer])


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

    def t_fraction_bar():
        q = random.randint(2, 9)
        top = q * c
        x = random.randint(1, top - 1)
        return _tb("Work out  (%d + %d) ÷ %d" % (x, top - x, c), q, "int", {}, ["Brackets first: %d; ÷ %d = %d." % (top, c, q)])

    def t_nested():
        p, q, r = random.randint(2, 5), random.randint(1, 4), random.randint(1, 4)
        return _tb("Work out  %d × (%d + %d)²" % (p, q, r), p * (q + r) ** 2, "int", {},
                   ["Brackets: %d; power: %d; × %d = %d." % (q + r, (q + r) ** 2, p, p * (q + r) ** 2)])

    def t_error():
        return _tb("%s worked out %d + %d × %d and got %d. What is the correct answer?" % (_who(), a, b, c, (a + b) * c), a + b * c,
                   "int", {}, ["× before +: %d × %d = %d; %d + %d = %d." % (b, c, b * c, a, b * c, a + b * c)]) \
            if (a + b) * c != a + b * c else t_basic()

    def t_over():
        p, q = random.randint(2, 6), random.randint(2, 5)
        top = p * q * random.randint(2, 6)
        return _tb("Work out  %d ÷ (%d × %d)" % (top, p, q), top // (p * q), "int", {},
                   ["Brackets first: %d × %d = %d; %d ÷ %d = %d." % (p, q, p * q, top, p * q, top // (p * q))])

    def t_square_diff():
        p, q = random.randint(4, 12), random.randint(1, 3)
        return _tb("Work out  %d² − %d²" % (p, q), p * p - q * q, "int", {},
                   ["Powers first: %d − %d = %d." % (p * p, q * q, p * p - q * q)])

    def t_symbol():
        x, y = random.randint(3, 12), random.randint(2, 9)
        op, val = pick([("×", x * y), ("+", x + y), ("−", x - y)])
        if op == "−" and (x <= y or x - y in (x + y, x * y)):
            op, val = "×", x * y
        if op == "+" and x + y == x * y:
            op, val = "×", x * y
        word = {"+": "add", "−": "subtract", "×": "multiply"}[op]
        return _wq("Which operation makes this true: add, subtract or multiply?  %d ___ %d = %d" % (x, y, val), word,
                   ["%d %s %d = %d." % (x, op, y, val)], "add / subtract / multiply")

    return _pick_t([t_basic, t_brackets, t_power, t_divide, t_mixed, t_place, t_root, t_fraction_bar, t_nested, t_error, t_over,
                    t_square_diff, t_symbol])


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

    def t_times_99():
        a = random.randint(12, 89)
        b = pick([99, 999, 101, 19, 21])
        r = b + 1 if b % 10 == 9 else b - 1
        return _tb("Work out %d × %d in your head. (Hint: use %d × %d and adjust.)" % (a, b, a, r), a * b, "int", {},
                   ["%d × %d = %d; %s %d = %d." % (a, r, a * r, "subtract" if r > b else "add", a, a * b)])

    def t_subtract_comp():
        b = pick([198, 299, 99, 499, 397])
        a = random.randint(b + 101, 999)
        r = (b + 5) // 100 * 100
        return _tb("Work out %d − %d in your head. (Hint: subtract %d, then adjust.)" % (a, b, r), a - b, "int", {},
                   ["%d − %d = %d; add back %d: %d." % (a, r, a - r, r - b, a - b)])

    def t_div5():
        n = random.randint(21, 199) * 2
        return _tb("Work out %d ÷ 5 in your head. (Hint: divide by 10, then double.)" % n, _ds(Fraction(n, 5)), "num", {},
                   ["%d ÷ 10 = %s; × 2 = %s." % (n, _ds(Fraction(n, 10)), _ds(Fraction(n, 5)))])

    def t_regroup():
        k = pick([4, 8, 2])
        other = random.randint(3, 19)
        return _tb("Work out 25 × %d × %d in your head. (Hint: do 25 × %d first.)" % (other, k, k), 25 * k * other, "int", {},
                   ["25 × %d = %d; × %d = %d." % (k, 25 * k, other, 25 * k * other)])

    def t_missing_div():
        q, k = random.randint(21, 99), random.randint(3, 9)
        return _tb("Find the missing number:  ___ ÷ %d = %d" % (k, q), q * k, "int", {}, ["Inverse: %d × %d = %d." % (q, k, q * k)])

    def t_near_double():
        a = random.randint(15, 75)
        return _tb("Work out %d + %d in your head. (Hint: near doubles.)" % (a, a + 1), 2 * a + 1, "int", {},
                   ["Double %d is %d; add 1: %d." % (a, 2 * a, 2 * a + 1)])

    def t_dec_mental():
        a, b = random.randint(2, 9), random.randint(2, 9)
        return _tb("Work out 0.%d × %d0 in your head." % (a, b), a * b, "int", {},
                   ["0.%d × %d0 = %d × %d = %d." % (a, b, a, b, a * b)])

    return _pick_t([t_compensate, t_double_half, t_inverse, t_check, t_partition, t_times_99, t_subtract_comp, t_div5,
                    t_regroup, t_missing_div, t_near_double, t_dec_mental])


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

    def t_tree_swim():
        tot = random.randint(40, 90)
        adults = random.randint(15, tot - 15)
        a_sw, c_sw = random.randint(3, adults - 2), random.randint(3, tot - adults - 2)
        return _tb("A frequency tree splits %d people into %d adults and %d children. %d of the adults and %d of the children "
                   "can swim. How many people can swim altogether?" % (tot, adults, tot - adults, a_sw, c_sw), a_sw + c_sw, "int",
                   {}, ["%d + %d = %d." % (a_sw, c_sw, a_sw + c_sw)])

    def t_tree_table():
        tot = random.randint(50, 120)
        yes = random.randint(20, tot - 20)
        yy = random.randint(5, yes - 3)
        ny = random.randint(5, tot - yes - 3)
        rows = [["All", tot], ["Had breakfast", yes], ["Had breakfast and walked", yy], ["No breakfast", ""],
                ["No breakfast but walked", ny]]
        return _dt("The table lists the branches of a frequency tree. How many pupils had no breakfast?", ["Branch", "Pupils"],
                   rows, tot - yes, ["%d − %d = %d." % (tot, yes, tot - yes)], missing=[3, 1])

    def t_two_way_pct():
        g = pick([20, 25, 40, 50])
        gl2 = random.randint(1, g - 1)
        rows = [["Boys", bl, boys - bl], ["Girls", gl2, g - gl2]]
        return _dt("What percentage of the girls have school lunch? Give the number only.", ["", "School lunch", "Packed lunch"],
                   rows, _ds(Fraction(gl2 * 100, g)), ["%d out of %d = %s%%." % (gl2, g, _ds(Fraction(gl2 * 100, g)))], atype="num")

    def t_build():
        tot = random.randint(25, 34)
        girls_ = random.randint(10, tot - 8)
        bg = random.randint(2, tot - girls_ - 2)
        return _tb("A class has %d pupils and %d of them are girls. %d boys wear glasses. How many boys do NOT wear glasses?"
                   % (tot, girls_, bg), tot - girls_ - bg, "int", {},
                   ["Boys: %d − %d = %d." % (tot, girls_, tot - girls_), "%d − %d = %d." % (tot - girls_, bg, tot - girls_ - bg)])

    def t_prob():
        rows = [["Boys", bl, boys - bl], ["Girls", gl, girls - gl]]
        return _dt("One pupil is picked at random. What is the probability they are a girl with packed lunch? Simplest form.",
                   ["", "School lunch", "Packed lunch"], rows, _fs(Fraction(girls - gl, boys + girls)),
                   ["%d out of %d pupils." % (girls - gl, boys + girls)], atype="frac")

    def t_years():
        y7, y8 = [random.randint(3, 20) for _ in range(3)], [random.randint(3, 20) for _ in range(3)]
        modes = ["Walk", "Bus", "Car"]
        k = random.randrange(3)
        return _dt("The two-way table shows how pupils in Years 7 and 8 travel to school. How many pupils %s?"
                   % ("walk", "come by bus", "come by car")[k], ["", "Walk", "Bus", "Car"], [["Year 7"] + y7, ["Year 8"] + y8], y7[k] + y8[k],
                   ["%d + %d = %d." % (y7[k], y8[k], y7[k] + y8[k])])

    def t_tree_frac():
        adults = pick([12, 15, 18, 20, 24, 30])
        sw = random.randint(1, adults - 1)
        return _fq("A frequency tree shows %d adults, and %d of the adults can swim. What fraction of the adults can swim? "
                   "Simplest form." % (adults, sw), Fraction(sw, adults), ["%d/%d = %s." % (sw, adults, _fs(Fraction(sw, adults)))])

    def t_which_year():
        y7, y8 = [random.randint(3, 20) for _ in range(3)], [random.randint(3, 20) for _ in range(3)]
        k = random.randrange(3)
        if y7[k] == y8[k]:
            y8[k] += 2
        what = ("walk", "come by bus", "come by car")[k]
        return _dt("Which year group has more pupils who %s? (type 7 or 8)" % what, ["", "Walk", "Bus", "Car"],
                   [["Year 7"] + y7, ["Year 8"] + y8], 7 if y7[k] > y8[k] else 8,
                   ["Year 7: %d, Year 8: %d." % (y7[k], y8[k])])

    return _pick_t([t_tree, t_tree_swim, t_build, t_tree_frac], [t_two_way_total, t_two_way_read, t_fraction, t_tree_table, t_two_way_pct,
                                                     t_prob, t_years, t_which_year])


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
    a, b = random.choice([v for v in range(-15, 16) if v]), random.choice([v for v in range(-15, 16) if v])

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
