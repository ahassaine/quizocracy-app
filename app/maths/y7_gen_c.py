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
        # easy: whole-number percentages under 100; medium: up to 250, some with tenths; hard: hundredths and tiny ones
        if d == 0:
            p = Decimal(random.randint(1, 99))
        elif d == 2:
            p = Decimal(random.randint(1, 2500)) / pick([10, 100])
        else:
            p = Decimal(random.randint(1, 250)) / pick([1, 1, 10])
        return _tb("Write %s%% as a decimal." % _ds(p), _ds(p / 100), "num", {}, ["÷ 100: %s." % _ds(p / 100)])

    def t_table():
        fs = random.sample(TERM[: _by(d, 7, 12, len(TERM))], 3)
        rows = [[_fs(x), _ds(x), "%s%%" % _ds(x * 100)] for x in fs]
        r, c = random.randrange(3), pick([1, 2])
        ans = _ds(fs[r]) if c == 1 else _ds(fs[r] * 100)
        return _dt("Complete the table (for a percentage, type the number only).", ["Fraction", "Decimal", "Percentage"],
                   rows, ans, ["%s = %s = %s%%." % (_fs(fs[r]), _ds(fs[r]), _ds(fs[r] * 100))], missing=[r, c], atype="num")

    def t_eighths():
        # easy: quarters and fifths; medium: eighths; hard: sixteenths
        den, k = _by(d, pick([(4, pick([1, 3])), (5, random.randint(1, 4))]), (8, pick([1, 3, 5, 7])),
                     (16, pick([1, 3, 5, 7, 9, 11, 13, 15])))
        unit = {4: "1/4 = 0.25", 5: "1/5 = 0.2", 8: "1/8 = 0.125", 16: "1/16 = 0.0625"}[den]
        return _tb("Write %d/%d as a decimal." % (k, den), _ds(Fraction(k, den)), "num", {},
                   ["%s, so %d/%d = %s." % (unit, k, den, _ds(Fraction(k, den)))])

    def t_p_to_f():
        p = Decimal(pick(_by(d, [10, 20, 25, 30, 40, 50, 60, 75, 80, 90],
                             [5, 12, 15, 35, 45, 64, 72, 85, 2, 8, 24, 55],
                             ["12.5", "37.5", "62.5", "87.5", "2.5", "17.5", "0.5", "7.5"])))
        f = Fraction(str(p)) / 100
        return _wq("Write %s%% as a fraction in its simplest form." % _ds(p), _fs(f),
                   ["%s/100 = %s." % (_ds(p), _fs(f))] if p == int(p) else
                   ["%s%% = %s/1000 = %s." % (_ds(p), _ds(p * 10), _fs(f))])

    def t_d_to_p():
        if d == 0:
            x = Decimal(random.randint(1, 99)) / 100
        elif d == 2:
            x = Decimal(random.randint(1, 2999)) / pick([1000, 10000])
        else:
            x = Decimal(random.randint(1, 1999)) / pick([100, 1000])
        return _tb("Write %s as a percentage. Give the number only." % _ds(x), _ds(x * 100), "num", {},
                   ["× 100: %s%%." % _ds(x * 100)])

    def t_grid():
        if d == 2:      # not a 100-grid: the pupil has to scale up
            parts, rows, cols = pick([(20, 4, 5), (25, 5, 5), (50, 5, 10)])
            k = random.randint(1, parts - 1)
            pct = k * 100 // parts
            return _area("What percentage of the grid is shaded? Give the number only.",
                         {"mode": "fraction_read", "parts": parts, "shaded": k, "rows": rows, "cols": cols}, pct,
                         ["%d out of %d squares = %d out of 100: %d%%." % (k, parts, pct, pct)])
        k = random.randint(1, 9) * 10 if d == 0 else random.randint(3, 97)
        return _area("What percentage of the grid is shaded? Give the number only.",
                     {"mode": "fraction_read", "parts": 100, "shaded": k, "rows": 10, "cols": 10}, k,
                     ["%d of the 100 squares: %d%%." % (k, k)])

    def t_mixed_number():
        w = random.randint(1, _by(d, 5, 5, 12))
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)],
                     [Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 8), Fraction(7, 20)],
                     [Fraction(5, 8), Fraction(7, 8), Fraction(9, 25), Fraction(3, 40), Fraction(7, 20), Fraction(3, 16)]))
        return _wq("Write %s as a mixed number in its simplest form." % _ds(w + f), _mixed(w + f),
                   ["%s = %d + %s = %s." % (_ds(w + f), w, _ds(f), _mixed(w + f))], "e.g. 2 3/4")

    def t_f_to_p_hard():
        f = pick(_by(d, [Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(3, 10), Fraction(7, 10), Fraction(3, 20)],
                     [Fraction(3, 8), Fraction(1, 8), Fraction(7, 40), Fraction(9, 16), Fraction(5, 16), Fraction(11, 25)],
                     [Fraction(3, 16), Fraction(13, 40), Fraction(1, 32), Fraction(7, 80), Fraction(19, 16), Fraction(11, 8)]))
        return _tb("Write %s as a percentage. Give the number only." % _fs(f), _ds(f * 100), "num", {},
                   ["%s = %s = %s%%." % (_fs(f), _ds(f), _ds(f * 100))])

    def t_error():
        if d == 0:      # a tens percentage written as hundredths
            p = pick([10, 20, 30, 40, 50, 60, 70, 80, 90])
            claim = "0.0%d" % (p // 10)
        elif d == 2:    # over 100% or under 1%
            p = Decimal(pick(["125", "150", "240", "0.5", "0.8", "2.5"]))
            claim = "0." + _ds(p).replace(".", "") if p > 1 and p == int(p) else _ds(p / 10)
        else:
            p = pick([3, 5, 7, 4, 9, 6])
            claim = "0.%d" % p
        return _tb("%s says %s%% = %s. What is %s%% as a decimal?" % (_who(), _ds(p), claim, _ds(p)), _ds(Decimal(p) / 100),
                   "num", {}, ["%s ÷ 100 = %s." % (_ds(p), _ds(Decimal(p) / 100))])

    def t_p_to_mixed():
        p = pick(_by(d, [125, 150, 175, 250, 350, 450], [125, 150, 175, 220, 240, 260, 305, 450],
                     [135, 145, 216, 308, 365, 412, 515, 290]))
        return _wq("Write %d%% as a mixed number in its simplest form." % p, _mixed(Fraction(p, 100)),
                   ["%d%% = %d/100 = %s." % (p, p, _mixed(Fraction(p, 100)))], "e.g. 1 3/4")

    def t_thousandths():
        # easy: two decimal places; medium: three; hard: four
        places = _by(d, 2, 3, 4)
        n = pick(_by(d, [25, 50, 75, 20, 40, 60, 80, 5], [5, 15, 25, 45, 75, 125, 375, 8, 64],
                     [125, 625, 375, 3125, 1875, 8, 45, 2]))
        den = 10 ** places
        return _wq("Write 0.%0*d as a fraction in its simplest form." % (places, n), _fs(Fraction(n, den)),
                   ["%d/%d = %s." % (n, den, _fs(Fraction(n, den)))])

    def t_same():
        f = pick(TERM[: _by(d, 7, 15, len(TERM))])
        off = pick(_by(d, [Fraction(1, 10), Fraction(1, 5)], [Fraction(1, 100), Fraction(1, 20), Fraction(1, 10)],
                       [Fraction(1, 100), Fraction(1, 200), Fraction(1, 1000)]))
        shown = f if random.random() < 0.5 else f + off
        return _wq("Is %s equal to %s%%? (yes or no)" % (_fs(f), _ds(shown * 100)), "yes" if shown == f else "no",
                   ["%s = %s%%." % (_fs(f), _ds(f * 100))], "yes / no")

    return _pick_t([t_f_to_d, t_d_to_f, t_f_to_p, t_p_to_d, t_eighths, t_p_to_f, t_d_to_p, t_mixed_number, t_f_to_p_hard,
                    t_error, t_p_to_mixed, t_thousandths, t_same], [t_table, t_grid])


@skill("Y7.4.b", "Order fractions, decimals and percentages", S4)
def _(d=1):
    d = _d(d)
    # easy: three of halves/quarters/fifths; hard: five, including 20ths, 25ths, 50ths and values above 1
    pool = random.sample(TERM[: _by(d, 7, 16, len(TERM))], _by(d, 3, 4, 5))
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
        f = pick(TERM[: _by(d, 7, 12, 14)])
        shown = pick([_fs(f), "%s%%" % _ds(f * 100)])
        why = ("%s means %s out of 100: %s ÷ 100 = %s." % (shown, _ds(f * 100), _ds(f * 100), _ds(f)) if "%" in shown
               else "%s = %d ÷ %d = %s." % (shown, f.numerator, f.denominator, _ds(f)))
        return _nld("Place %s on the number line from 0 to 1." % shown, f, 0, 1,
                    Decimal("0.025"), Decimal("0.1"), [why, "Each labelled step is 0.1, so find %s between them." % _ds(f)])

    return _pick_t([t_largest, t_smallest, t_compare], [t_line])


@skill("Y7.4.c", "One quantity as a fraction or percentage of another", S4)
def _(d=1):
    d = _d(d)

    def t_fraction():
        b = pick(_by(d, [10, 12, 20], [10, 12, 20, 24, 30, 40, 60], [36, 48, 60, 72, 90, 120]))
        a = random.randint(1, b - 1)
        return _fq("What fraction of %d is %d? Give it in its simplest form." % (b, a), Fraction(a, b),
                   ["%d/%d = %s." % (a, b, _fs(Fraction(a, b)))])

    def t_percent():
        b = pick(_by(d, [20, 25, 50], [20, 25, 40, 50, 80, 200], [40, 80, 125, 200, 250, 400]))
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
        tot = pick(_by(d, [20, 25, 50], [20, 25, 40, 50], [40, 80, 125, 160]))   # easy: whole-number percentages
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

    # easy: one familiar step with whole-number answers; hard: unit conversion, over 100%, decimal percentages, comparing
    return _pick_t(_by(d, [t_fraction, t_percent, t_minutes, t_test, t_units, t_time_units, t_mass],
                       [t_fraction, t_percent, t_minutes, t_test, t_greater_one, t_units, t_money, t_over_100, t_decimal_pct,
                        t_better, t_time_units, t_distance, t_mass],
                       [t_fraction, t_percent, t_test, t_greater_one, t_money, t_over_100, t_decimal_pct, t_better, t_distance]),
                   [t_bar])


@skill("Y7.4.d", "Fractions and percentages of amounts", S4)
def _(d=1):
    d = _d(d)

    def t_fraction():
        den = pick(_by(d, [2, 3, 4, 5, 10], [3, 4, 5, 6, 8, 10], [6, 7, 8, 9, 12, 20]))
        num = pick([k for k in range(1, den) if Fraction(k, den).denominator == den])
        x = den * random.randint(3, _by(d, 15, 40, 120))
        return _tb("Work out %d/%d of %d." % (num, den, x), x // den * num, "int", {},
                   ["%d ÷ %d × %d = %d." % (x, den, num, x // den * num)])

    def t_percent_easy():
        p = pick(_by(d, [10, 50, 25, 20], [10, 20, 25, 50, 75, 5, 1], [5, 1, 75, 30, 60, 90]))
        x = pick(_by(d, [20, 40, 60, 80, 100, 200], [40, 60, 80, 120, 200, 360, 480], [360, 480, 520, 640, 1200, 2400]))
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
        x = random.randint(2, _by(d, 10, 30, 90)) * 10
        p = pick(_by(d, [10, 20, 50], [10, 20, 30, 40, 60, 70, 15, 35], [15, 35, 45, 65, 85, 95]))
        return _tb("%s has £%d and spends %d%% of it. How much is left, in pounds?" % (_who(), x, p), _ds(Fraction(x * (100 - p), 100)),
                   "num", {"unit": "£"}, ["%d%% is left: %d%% of %d = %s." % (100 - p, 100 - p, x, _ds(Fraction(x * (100 - p), 100)))])

    def t_frac_then_pct():
        x = random.randint(2, 12) * 40
        return _tb("A farmer has %d sheep. 3/4 of them are white, and 10%% of the white sheep have lambs. How many white sheep "
                   "have lambs?" % x, x * 3 // 40, "int", {"unit": "sheep"},
                   ["3/4 of %d = %d." % (x, x * 3 // 4), "10%% of %d = %d." % (x * 3 // 4, x * 3 // 40)])

    # easy: one step with friendly fractions and percentages; hard: build-ups, multipliers, over 100%, two-step problems
    return _pick_t(_by(d, [t_fraction, t_percent_easy, t_money_frac, t_left],
                       [t_fraction, t_percent_easy, t_percent_build, t_over_100, t_money, t_multiplier, t_money_frac, t_swap,
                        t_vat, t_half_pct, t_bigger_offer, t_left, t_frac_then_pct],
                       [t_fraction, t_percent_build, t_over_100, t_money, t_multiplier, t_swap, t_vat, t_half_pct,
                        t_bigger_offer, t_left, t_frac_then_pct]), [t_bar])


# ================================================================== 7.5 ======
@skill("Y7.5.a", "Add and subtract integers and decimals", S5)
def _(d=1):
    d = _d(d)

    def t_int():
        lo, hi = _by(d, (100, 9999), (1000, 99999), (10000, 999999))
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        op = pick(["+", "−"])
        if op == "−" and b > a:
            a, b = b, a
        return _tb("Work out %s %s %s." % (_c(a), op, _c(b)), a + b if op == "+" else a - b, "int", {},
                   ["Use a column method."])

    def t_dec():
        # easy: both to 1 d.p.; hard: mixed places up to thousandths, so the points must be lined up with care
        a = Decimal(random.randint(*_by(d, (10, 999), (100, 99999), (1000, 99999)))) / pick(_by(d, [10], [10, 100, 1000], [100, 1000]))
        b = Decimal(random.randint(*_by(d, (10, 999), (100, 9999), (100, 99999)))) / pick(_by(d, [10], [10, 100], [10, 100, 1000]))
        op = pick(["+", "−"])
        if op == "−" and b > a:
            a, b = b, a
        return _tb("Work out %s %s %s." % (_ds(a), op, _ds(b)), _ds(a + b if op == "+" else a - b), "num", {},
                   ["Line up the decimal points."])

    def t_missing():
        a = Decimal(random.randint(*_by(d, (10, 999), (100, 9999), (1000, 99999)))) / _by(d, 10, 100, 100)
        b = Decimal(random.randint(*_by(d, (10, 999), (100, 9999), (100, 99999)))) / _by(d, 10, 100, 1000)
        return _tb("Find the missing number:  %s + ___ = %s" % (_ds(a), _ds(a + b)), _ds(b), "num", {},
                   ["%s − %s = %s." % (_ds(a + b), _ds(a), _ds(b))])

    def t_perimeter():
        sides = [Decimal(random.randint(*_by(d, (2, 20), (15, 120), (105, 1250)))) / _by(d, 1, 10, pick([10, 100]))
                 for _ in range(pick(_by(d, [3, 4], [3, 4, 5], [4, 5, 6])))]
        return _tb("A shape has sides of %s cm. What is its perimeter, in cm?" % ", ".join(_ds(s) for s in sides),
                   _ds(sum(sides)), "num", {"unit": "cm"}, ["%s = %s." % (" + ".join(_ds(s) for s in sides), _ds(sum(sides)))])

    def t_money():
        items = [Decimal(random.randint(*_by(d, (50, 950), (99, 1999), (99, 2499)))) / 100 for _ in range(_by(d, 2, 3, 4))]
        pay = pick(_by(d, [10, 20], [20, 50], [50]))
        if sum(items) >= pay:
            pay = _by(d, 20, 100, 100)
        return _tb("Items cost £%s. How much change from £%d, in pounds?" % (", £".join(format(i, ".2f") for i in items), pay),
                   _ds(pay - sum(items)), "num", {"unit": "£"},
                   ["Total £%s." % format(sum(items), ".2f"), "£%d − £%s = £%s." % (pay, format(sum(items), ".2f"),
                                                                                   format(pay - sum(items), ".2f"))])

    def t_minus_missing():
        a = Decimal(random.randint(*_by(d, (10, 999), (100, 9999), (100, 99999)))) / _by(d, 10, 100, 1000)
        b = Decimal(random.randint(*_by(d, (10, 999), (100, 9999), (1000, 99999)))) / _by(d, 10, 100, 100)
        return _tb("Find the missing number:  ___ − %s = %s" % (_ds(a), _ds(b)), _ds(a + b), "num", {},
                   ["Add back: %s + %s = %s." % (_ds(b), _ds(a), _ds(a + b))])

    def t_receipt():
        items = random.sample(["Bread", "Milk", "Eggs", "Apples", "Cheese", "Juice"], 3)
        prices = [Decimal(random.randint(*_by(d, (45, 299), (45, 499), (105, 1999)))) / 100 for _ in items]
        rows = [[i, format(p, ".2f")] for i, p in zip(items, prices)] + [["Total", format(sum(prices), ".2f")]]
        k = random.randrange(3)
        return _dt("A till receipt is shown, with one price missing. What is the missing price, in pounds?", ["Item", "Price (£)"],
                   rows, _ds(prices[k]), ["%s − %s = %s." % (format(sum(prices), ".2f"),
                                                            format(sum(prices) - prices[k], ".2f"), format(prices[k], ".2f"))],
                   missing=[k, 1], atype="num")

    def t_journey():
        legs = [Decimal(random.randint(*_by(d, (12, 99), (12, 250), (105, 999)))) / _by(d, 10, 10, 100) for _ in range(3)]
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
        a = random.randint(*_by(d, (10, 99), (100, 999), (1000, 9999)))
        b = a + random.randint(*_by(d, (5, 90), (50, 900), (500, 9000)))
        return _tb("Work out %d − %d." % (a, b), a - b, "int", {}, ["%d − %d = %d, and %d is bigger than %d, so %d − %d = −%d." % (b, a, b - a, b, a, a, b, b - a)])

    return _pick_t(_by(d, [t_int, t_dec, t_missing, t_perimeter, t_money],
                       [t_int, t_dec, t_missing, t_perimeter, t_money, t_minus_missing, t_journey],
                       [t_int, t_dec, t_missing, t_money, t_minus_missing, t_journey]),       # t_neg_answer: strand 7.6 first
                   [t_receipt, t_temps_line])


@skill("Y7.5.b", "Multiply and divide integers and decimals", S5)
def _(d=1):
    d = _d(d)

    def t_long_mult():
        # easy: 3-digit × 1-digit; medium: 3-digit × 2-digit; hard: 4-digit × 2-digit
        a, b = random.randint(_by(d, 100, 100, 1000), _by(d, 999, 999, 9999)), random.randint(_by(d, 2, 12, 12), _by(d, 9, 99, 99))
        return _tb("Work out %s × %d." % (_c(a), b), a * b, "int", {},
                   ["Use %s multiplication: %s." % ("short" if b < 10 else "long", _c(a * b))])

    def t_dec_mult():
        a = Decimal(pick([v for v in range(11, _by(d, 99, 999, 999) + 1) if v % 10])) / 10
        b = random.randint(2, _by(d, 5, 9, 9)) if d < 2 else Decimal(random.randint(2, 9)) / 10
        whole_a, whole_b = int(a * 10), int(b * 10) if b < 1 else int(b)
        places = 1 + (1 if b < 1 else 0)
        return _tb("Work out %s × %s." % (_ds(a), _ds(b)), _ds(a * b), "num", {},
                   ["Leave out the decimal points: %d × %d = %s." % (whole_a, whole_b, _c(whole_a * whole_b)),
                    "There %s %d decimal place%s in the question, so put %d back: %s."
                    % ("is" if places == 1 else "are", places, "" if places == 1 else "s", places,
                       format(Decimal(whole_a * whole_b).scaleb(-places), "f")
                       + ("" if format(Decimal(whole_a * whole_b).scaleb(-places), "f") == _ds(a * b) else " = " + _ds(a * b)))])

    def t_long_div():
        # easy: short division by a single digit; hard: 3-digit answers, divisors to 49
        q, k = random.randint(_by(d, 11, 21, 101), _by(d, 99, 299, 999)), random.randint(_by(d, 2, 12, 13), _by(d, 9, 35, 49))
        return _tb("Work out %s ÷ %d." % (_c(q * k), k), q, "int", {},
                   ["Use %s division: %d." % ("short" if k < 10 else "long or short", q)])

    def t_dec_div():
        q = Decimal(random.randint(_by(d, 11, 11, 101), _by(d, 99, 999, 9999))) / _by(d, 10, 100, 1000)
        k = random.randint(2, _by(d, 5, 9, 12))
        return _tb("Work out %s ÷ %d." % (_ds(q * k), k), _ds(q), "num", {},
                   ["Divide as if there were no decimal point, and keep the point in the same place in the answer.",
                    "%s ÷ %d = %s; check: %s × %d = %s." % (_ds(q * k), k, _ds(q), _ds(q), k, _ds(q * k))])

    def t_dec_by_dec():
        q = random.randint(2, _by(d, 20, 90, 90))
        k = Decimal(pick(_by(d, ["0.1", "0.5", "0.2"], ["0.2", "0.5", "0.4", "0.25", "0.1"], ["0.25", "0.04", "0.05", "0.15", "0.4"])))
        return _tb("Work out %s ÷ %s." % (_ds(q * k), _ds(k)), q, "int", {},
                   ["Multiply both by %d to remove the decimal." % 10 ** -k.as_tuple().exponent])

    def t_related():
        a, b = random.randint(12, 99), random.randint(12, 99)
        # easy: one factor ÷ 10; medium: both ÷ 10; hard: ÷ 100 and ÷ 10
        da, db = _by(d, (10, 1), (10, 10), (100, 10))
        return _tb("Given %d × %d = %s, work out %s × %s." % (a, b, _c(a * b), _ds(Decimal(a) / da), _ds(Decimal(b) / db)),
                   _ds(Decimal(a * b) / (da * db)), "num", {},
                   [("One number is ÷ 10, so the answer is ÷ 10." if da * db == 10 else
                     "Both numbers are ÷ 10, so the answer is ÷ 100." if da * db == 100 else
                     "The numbers are ÷ 100 and ÷ 10, so the answer is ÷ 1000.")])

    def t_area():
        den = _by(d, 10, 10, 100)
        a = Decimal(pick([v for v in range(11, _by(d, 49, 99, 999) + 1) if v % den])) / den   # never a whole number
        b = random.randint(2, _by(d, 5, 12, 12)) if d < 2 else Decimal(random.randint(11, 99)) / 10
        return _tb("A rectangle is %s m by %s m. What is its area, in m²?" % (_ds(a), _ds(b)), _ds(a * b), "num",
                   {"unit": "m²"}, ["%s × %s = %s." % (_ds(a), _ds(b), _ds(a * b))])

    def t_unit_cost():
        n = random.randint(_by(d, 2, 3, 6), _by(d, 5, 9, 15))
        each = Decimal(random.randint(*_by(d, (5, 40), (25, 199), (25, 999))) * _by(d, 5, 1, 1)) / 100
        return _tb("%d pens cost £%s. How much does one pen cost, in pounds?" % (n, format(each * n, ".2f")), _ds(each), "num",
                   {"unit": "£"}, ["£%s ÷ %d = £%s." % (format(each * n, ".2f"), n, format(each, ".2f"))])

    def t_dd():
        # easy: tenths × a whole number; medium: tenths × tenths; hard: hundredths × tenths
        a = Decimal(random.randint(*_by(d, (1, 9), (1, 9), (11, 99)))) / _by(d, 10, 10, 100)
        if d == 0:
            b = Decimal(random.randint(2, 9))
        else:
            b = Decimal(random.randint(1, 9)) / 10
            if random.random() < 0.5:
                b = Decimal(random.randint(11, 39)) / 10
        pa, pb = -a.as_tuple().exponent, -b.as_tuple().exponent
        ia, ib = int(a * 10 ** pa), int(b * 10 ** pb)
        return _tb("Work out %s × %s." % (_ds(a), _ds(b)), _ds(a * b), "num", {},
                   ["%d × %d = %d, and there %s %d decimal place%s in total." % (ia, ib, ia * ib, "is" if pa + pb == 1 else "are",
                                                                              pa + pb, "" if pa + pb == 1 else "s")])

    def t_exchange():
        rate = pick(_by(d, [Decimal("1.5"), Decimal("1.2"), Decimal("1.25")],
                        [Decimal("1.15"), Decimal("1.18"), Decimal("1.25"), Decimal("1.3"), Decimal("1.12")],
                        [Decimal("1.17"), Decimal("1.28"), Decimal("1.36"), Decimal("1.14"), Decimal("1.22")]))
        cur = pick(["euros", "dollars"])
        x = random.randint(1, 10) * 10 if d == 0 else (random.randint(13, 250) if d == 2 else random.randint(2, 40) * 5)
        return _tb("£1 = %s %s. How many %s do you get for £%d?" % (_ds(rate), cur, cur, x), _ds(rate * x), "num", {"unit": cur},
                   ["%d × %s = %s." % (x, _ds(rate), _ds(rate * x))])

    def t_glasses():
        g = pick(_by(d, [Decimal("0.5"), Decimal("0.25")], [Decimal("0.2"), Decimal("0.25"), Decimal("0.3"), Decimal("0.4")],
                     [Decimal("0.15"), Decimal("0.35"), Decimal("0.125"), Decimal("0.45")]))
        n = random.randint(_by(d, 2, 4, 6), _by(d, 10, 20, 30))
        return _tb("How many %s litre glasses can be filled from %s litre%s of juice?" % (_ds(g), _ds(g * n), "" if g * n == 1 else "s"), n,
                   "int",
                   {"unit": "glasses"}, ["%s ÷ %s = %d." % (_ds(g * n), _ds(g), n)])

    def t_map():
        s = pick(_by(d, [2, 5, 10], [Decimal("2.5"), Decimal("1.5"), Decimal("0.5"), 2, 5],
                     [Decimal("1.25"), Decimal("0.75"), Decimal("2.4"), Decimal("3.5")]))
        cm = Decimal(random.randint(_by(d, 2, 12, 12), _by(d, 15, 98, 98))) / _by(d, 1, 10, 10)
        return _tb("On a map, 1 cm stands for %s km. Two towns are %s cm apart on the map. How far apart are they really, in km?"
                   % (_ds(s), _ds(cm)), _ds(cm * s), "num", {"unit": "km"}, ["%s × %s = %s." % (_ds(cm), _ds(s), _ds(cm * s))])

    def t_div_decimal_answer():
        a = random.randint(2, _by(d, 5, 9, 12))
        q = Decimal(random.randint(*_by(d, (11, 99), (11, 999), (101, 9999)))) / _by(d, 10, 10, 100)
        if (q * a) % 1 == 0:
            q += _by(d, Decimal("0.1"), Decimal("0.1"), Decimal("0.01"))
        return _tb("Share £%s equally between %d people. How much does each get, in pounds?" % (format(q * a, ".2f"), a), _ds(q),
                   "num", {"unit": "£"}, ["£%s ÷ %d = £%s." % (format(q * a, ".2f"), a, format(q, ".2f"))])

    return _pick_t([t_long_mult, t_dec_mult, t_long_div, t_dec_div, t_dec_by_dec, t_related, t_area, t_unit_cost, t_dd,
                    t_exchange, t_glasses, t_map, t_div_decimal_answer])


@skill("Y7.5.c", "Priority of operations (brackets, powers, ×÷, +−)", S5)
def _(d=1):
    d = _d(d)
    a, b, c, e = [random.randint(2, _by(d, 9, 12, 15)) for _ in range(4)]

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
        p, q, r, s = (c, e, a, b) if d == 0 and a * b < c * e else (a, b, c, e)     # easy: no negative answer
        return _tb("Work out  %d × %d − %d × %d" % (p, q, r, s), p * q - r * s, "int", {},
                   ["%d − %d = %d." % (p * q, r * s, p * q - r * s)])

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
        p, q, r = random.randint(2, _by(d, 3, 5, 9)), random.randint(1, _by(d, 3, 4, 7)), random.randint(1, _by(d, 3, 4, 7))
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
        p = random.randint(4, _by(d, 10, 12, 15))
        q = random.randint(1, min(_by(d, 3, 3, 9), p - 1))
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

    def t_three_step():
        p, q = random.randint(2, 7), random.randint(2, 7)
        sq = (p + q) ** 2
        k = pick([v for v in range(2, 15) if sq % v == 0])
        m = random.randint(1, 20)
        return _tb("Work out  (%d + %d)² ÷ %d − %d" % (p, q, k, m), sq // k - m, "int", {},
                   ["Brackets: %d; power: %d; ÷ %d = %d; − %d = %d." % (p + q, sq, k, sq // k, m, sq // k - m)])

    # easy: one or two operations; hard: powers, roots, nesting and three-step chains
    return _pick_t(_by(d, [t_basic, t_brackets, t_power, t_divide, t_mixed, t_error, t_symbol],
                       [t_basic, t_brackets, t_power, t_divide, t_mixed, t_place, t_root, t_fraction_bar, t_nested, t_error,
                        t_over, t_square_diff, t_symbol],
                       [t_mixed, t_place, t_root, t_fraction_bar, t_nested, t_error, t_over, t_square_diff, t_three_step]))


@skill("Y7.5.d", "Mental strategies and inverse operations", S5)
def _(d=1):
    d = _d(d)

    def t_compensate():
        a = random.randint(*_by(d, (21, 90), (100, 900), (1000, 9000)))
        b = pick(_by(d, [9, 19, 29, 39], [99, 199, 299, 98, 49], [199, 398, 599, 999, 1998]))
        r = b + 1 if b % 10 == 9 else (b // 50 + 1) * 50
        return _tb("Work out %d + %d in your head. (Hint: add a round number, then adjust.)" % (a, b), a + b, "int", {},
                   ["%d + %d = %d, then take away %d: %d." % (a, r, a + r, r - b, a + b)])

    def t_double_half():
        a, b = random.randint(*_by(d, (6, 24), (11, 49), (51, 249))) * 2, pick(_by(d, [5], [5, 50, 25], [5, 50, 25]))
        return _tb("Work out %d × %d. (Hint: halve one number and double the other.)" % (a, b), a * b, "int", {},
                   ["%d × %d = %d." % (a // 2, b * 2, a * b)])

    def t_inverse():
        a, b = random.randint(*_by(d, (12, 99), (100, 999), (1000, 9999))), random.randint(*_by(d, (3, 9), (12, 99), (12, 99)))
        return _tb("%d × %d = %s. What is %s ÷ %d?" % (a, b, _c(a * b), _c(a * b), a), b, "int", {},
                   ["Division undoes multiplication."])

    def t_check():
        lo, hi = _by(d, (100, 999), (1000, 9999), (10000, 99999))
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        return _tb("To check %s + %s = %s using the inverse, what subtraction gives back %s? Type the answer of %s − %s."
                   % (_c(a), _c(b), _c(a + b), _c(a), _c(a + b), _c(b)), a, "int", {}, ["%s − %s = %s." % (_c(a + b), _c(b), _c(a))])

    def t_partition():
        a, b = random.randint(*_by(d, (11, 29), (11, 49), (51, 199))), random.randint(*_by(d, (2, 5), (3, 9), (6, 9)))
        return _tb("Work out %d × %d by partitioning." % (a, b), a * b, "int", {},
                   ["%d × %d + %d × %d = %d." % ((a // 10) * 10, b, a % 10, b, a * b)])

    def t_times_99():
        a = random.randint(*_by(d, (12, 30), (12, 89), (12, 99)))
        b = pick(_by(d, [9, 11, 19, 21], [99, 999, 101, 19, 21], [99, 999, 101, 1001, 49, 51]))
        r = b + 1 if b % 10 == 9 else b - 1
        return _tb("Work out %d × %d in your head. (Hint: use %d × %d and adjust.)" % (a, b, a, r), a * b, "int", {},
                   ["%d × %d = %d; %s %d = %d." % (a, r, a * r, "subtract" if r > b else "add", a, a * b)])

    def t_subtract_comp():
        b = pick(_by(d, [19, 29, 39, 48, 59], [198, 299, 99, 499, 397], [398, 599, 997, 1998, 2499]))
        a = random.randint(b + _by(d, 11, 101, 101), _by(d, 99, 999, 9999))
        r = (b + 5) // 100 * 100 if b > 90 else (b + 5) // 10 * 10
        return _tb("Work out %d − %d in your head. (Hint: subtract %d, then adjust.)" % (a, b, r), a - b, "int", {},
                   ["%d − %d = %d; add back %d: %d." % (a, r, a - r, r - b, a - b)])

    def t_div5():
        n = _by(d, random.randint(3, 30) * 10, random.randint(21, 199) * 2, random.randint(201, 1999))   # easy: whole answer
        return _tb("Work out %d ÷ 5 in your head. (Hint: divide by 10, then double.)" % n, _ds(Fraction(n, 5)), "num", {},
                   ["%d ÷ 10 = %s; × 2 = %s." % (n, _ds(Fraction(n, 10)), _ds(Fraction(n, 5)))])

    def t_regroup():
        k = pick(_by(d, [4], [4, 8, 2], [4, 8, 12]))
        other = random.randint(*_by(d, (2, 9), (3, 19), (11, 49)))
        return _tb("Work out 25 × %d × %d in your head. (Hint: do 25 × %d first.)" % (other, k, k), 25 * k * other, "int", {},
                   ["25 × %d = %d; × %d = %d." % (k, 25 * k, other, 25 * k * other)])

    def t_missing_div():
        q, k = random.randint(*_by(d, (11, 30), (21, 99), (101, 499))), random.randint(*_by(d, (2, 5), (3, 9), (6, 9)))
        return _tb("Find the missing number:  ___ ÷ %d = %d" % (k, q), q * k, "int", {}, ["Inverse: %d × %d = %d." % (q, k, q * k)])

    def t_near_double():
        a = random.randint(*_by(d, (6, 25), (15, 75), (51, 250)))
        return _tb("Work out %d + %d in your head. (Hint: near doubles.)" % (a, a + 1), 2 * a + 1, "int", {},
                   ["Double %d is %d; add 1: %d." % (a, 2 * a, 2 * a + 1)])

    def t_dec_mental():
        a, b = random.randint(2, _by(d, 5, 9, 9)), random.randint(2, _by(d, 5, 9, 9))
        if d == 2:
            return _tb("Work out 0.%d × %d00 in your head." % (a, b), a * b * 10, "int", {},
                       ["0.%d × %d00 = %d × %d0 = %d." % (a, b, a, b, a * b * 10)])
        return _tb("Work out 0.%d × %d0 in your head." % (a, b), a * b, "int", {},
                   ["0.%d × %d0 = %d × %d = %d." % (a, b, a, b, a * b)])

    return _pick_t([t_compensate, t_double_half, t_inverse, t_check, t_partition, t_times_99, t_subtract_comp, t_div5,
                    t_regroup, t_missing_div, t_near_double, t_dec_mental])


@skill("Y7.5.e", "Frequency trees and two-way tables", S5)
def _(d=1):
    d = _d(d)
    lo, hi = _by(d, (5, 15), (10, 40), (25, 90))
    boys, girls = random.randint(lo, hi), random.randint(lo, hi)
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
        tot = random.randint(*_by(d, (30, 50), (40, 90), (80, 200)))
        adults = random.randint(15, tot - 15)
        a_sw, c_sw = random.randint(3, adults - 2), random.randint(3, tot - adults - 2)
        return _tb("A frequency tree splits %d people into %d adults and %d children. %d of the adults and %d of the children "
                   "can swim. How many people can swim altogether?" % (tot, adults, tot - adults, a_sw, c_sw), a_sw + c_sw, "int",
                   {}, ["%d + %d = %d." % (a_sw, c_sw, a_sw + c_sw)])

    def t_tree_table():
        tot = random.randint(*_by(d, (40, 60), (50, 120), (100, 300)))
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
        y7, y8 = [random.randint(3, hi // 2) for _ in range(3)], [random.randint(3, hi // 2) for _ in range(3)]
        modes = ["Walk", "Bus", "Car"]
        k = random.randrange(3)
        return _dt("The two-way table shows how pupils in Years 7 and 8 travel to school. How many pupils %s?"
                   % ("walk", "come by bus", "come by car")[k], ["", "Walk", "Bus", "Car"], [["Year 7"] + y7, ["Year 8"] + y8], y7[k] + y8[k],
                   ["%d + %d = %d." % (y7[k], y8[k], y7[k] + y8[k])])

    def t_tree_frac():
        adults = pick(_by(d, [10, 12, 20], [12, 15, 18, 20, 24, 30], [36, 40, 45, 48, 60]))
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

    # easy: read or add up a total; hard: fill gaps from totals, fractions, percentages and probabilities
    return _pick_t(_by(d, [t_tree, t_tree_swim, t_build], [t_tree, t_tree_swim, t_build, t_tree_frac],
                       [t_tree, t_build, t_tree_frac]),
                   _by(d, [t_two_way_total, t_two_way_read, t_years, t_which_year],
                       [t_two_way_total, t_two_way_read, t_fraction, t_tree_table, t_two_way_pct, t_prob, t_years, t_which_year],
                       [t_two_way_total, t_fraction, t_tree_table, t_two_way_pct, t_prob]))


# ================================================================== 7.6 ======
@skill("Y7.6.a", "Order and compare directed numbers", S6)
def _(d=1):
    d = _d(d)
    lo, hi = _by(d, (-10, 11), (-30, 30), (-100, 100))
    vals = random.sample(range(lo, hi), _by(d, 4, 5, 6))

    def t_smallest():
        return _tb("Which is the smallest?  %s" % ", ".join(map(str, vals)), min(vals), "int", {},
                   ["The most negative number is the smallest."])

    def t_symbol():
        a, b = vals[0], vals[1]
        return _wq("Write < or > :  %d ___ %d" % (a, b), "<" if a < b else ">", ["Further left on the number line is smaller."],
                   "< or >")

    def t_between():
        a, b = sorted(random.sample(range(*_by(d, (-8, 9), (-15, 15), (-60, 60))), 2))
        return _tb("How many whole numbers are strictly between %d and %d?" % (a, b), max(0, b - a - 1), "int", {},
                   ["%d − %d − 1 = %d." % (b, a, max(0, b - a - 1))])

    def t_midpoint():
        a = random.randint(*_by(d, (-10, -2), (-20, -2), (-60, -11)))
        b = a + 2 * random.randint(*_by(d, (2, 6), (2, 12), (6, 40)))
        return _tb("What number is halfway between %d and %d?" % (a, b), (a + b) // 2, "int", {}, ["(%d + %d) ÷ 2 = %d." % (a, b, (a + b) // 2)])

    def t_line():
        v = random.randint(-9, 9)
        return _nl("Place %d on the number line." % v, v, 1, 5, ["Count from 0."], lo=-10, hi=10)

    def t_temps():
        cities = ["Oslo", "Rome", "Kyiv", "Lima"]
        t = random.sample(range(*_by(d, (-8, 15), (-15, 20), (-30, 25))), 4)
        k = pick(["coldest", "warmest"])
        ans = cities[t.index(min(t) if k == "coldest" else max(t))]
        return _dt("Which city was the %s?" % k, ["City", "Temperature"], [[c, "%d °C" % x] for c, x in zip(cities, t)],
                   ans, ["%s: %d °C." % (ans, min(t) if k == "coldest" else max(t))], atype="str")

    return _pick_t([t_smallest, t_symbol, t_between, t_midpoint], [t_line, t_temps])


@skill("Y7.6.b", "Add and subtract directed numbers", S6)
def _(d=1):
    d = _d(d)
    m = _by(d, 10, 15, 50)
    a, b = random.choice([v for v in range(-m, m + 1) if v]), random.choice([v for v in range(-m, m + 1) if v])

    def t_add():
        return _tb("Work out  %d + %s" % (a, _neg(b)), a + b, "int", {},
                   ["Adding a negative is the same as subtracting." if b < 0 else "Count on %d." % b])

    def t_sub():
        return _tb("Work out  %d − %s" % (a, _neg(b)), a - b, "int", {},
                   ["Subtracting a negative is the same as adding." if b < 0 else "Count back %d." % b])

    def t_temperature():
        t0, ch = random.randint(*_by(d, (-3, 8), (-8, 5), (-25, 5))), random.randint(*_by(d, (2, 10), (3, 15), (8, 40)))
        return _tb("The temperature is %d °C. It falls by %d degrees. What is it now, in °C?" % (t0, ch), t0 - ch, "int",
                   {"unit": "°C"}, ["%d − %d = %d." % (t0, ch, t0 - ch)])

    def t_difference():
        x, y = random.randint(-_by(d, 10, 20, 80), -1), random.randint(1, _by(d, 10, 20, 80))
        return _tb("What is the difference between %d and %d?" % (x, y), y - x, "int", {}, ["%d − %s = %d." % (y, _neg(x), y - x)])

    def t_missing():
        return _tb("Find the missing number:  %d + ___ = %d" % (a, a + b), b, "int", {}, ["%d − %s = %d." % (a + b, _neg(a), b)])

    def t_bank():
        bal, spend = random.randint(*_by(d, (5, 30), (5, 50), (20, 500))), random.randint(*_by(d, (10, 50), (10, 90), (50, 900)))
        return _tb("A bank account has £%d. £%d is spent. What is the balance now, in pounds? (use a minus sign if it is "
                   "overdrawn)" % (bal, spend), bal - spend, "int", {"unit": "£"}, ["%d − %d = %d." % (bal, spend, bal - spend)])

    def t_chain():
        x, y, z = [random.choice([v for v in range(-20, 21) if v]) for _ in range(3)]
        return _tb("Work out  %d − %s + %s" % (x, _neg(y), _neg(z)), x - y + z, "int", {},
                   ["Left to right: %d − %s = %d; %d + %s = %d." % (x, _neg(y), x - y, x - y, _neg(z), x - y + z)])

    # hard adds a three-term chain and missing-number forms with larger values
    return _pick_t(_by(d, [t_add, t_sub, t_temperature, t_difference, t_bank],
                       [t_add, t_sub, t_temperature, t_difference, t_missing, t_bank],
                       [t_add, t_sub, t_temperature, t_difference, t_missing, t_bank, t_chain]))


@skill("Y7.6.c", "Multiply and divide directed numbers", S6)
def _(d=1):
    d = _d(d)
    a = random.choice([-1, 1]) * random.randint(2, _by(d, 6, 12, 20))
    b = random.choice([-1, 1]) * random.randint(2, _by(d, 6, 12, 12))      # b is the divisor in t_div: keep to the tables
    if a > 0 and b > 0:                    # directed-number practice: at least one negative
        a = -a

    def t_mult():
        return _tb("Work out  %s × %s" % (_neg(a), _neg(b)), a * b, "int", {},
                   ["Same signs give a positive; different signs give a negative."])

    def t_div():
        return _tb("Work out  %s ÷ %s" % (_neg(a * b), _neg(b)), a, "int", {}, ["Same rule for signs as multiplication."])

    def t_square():
        k = random.randint(*_by(d, (2, 6), (2, 12), (8, 15)))
        return _tb("Work out  (−%d)²" % k, k * k, "int", {}, ["(−%d) × (−%d) = %d: a negative times a negative is positive." % (k, k, k * k)])

    def t_three():
        x, y, z = [random.choice([-1, 1]) * random.randint(2, _by(d, 3, 5, 7)) for _ in range(3)]
        return _tb("Work out  %s × %s × %s" % (_neg(x), _neg(y), _neg(z)), x * y * z, "int", {},
                   ["%d negative sign%s." % (sum(1 for v in (x, y, z) if v < 0),
                                            "" if sum(1 for v in (x, y, z) if v < 0) == 1 else "s")])

    def t_missing():
        return _tb("Find the missing number:  %s × ___ = %d" % (_neg(a), a * b), b, "int", {}, ["%d ÷ %s = %d." % (a * b, _neg(a), b)])

    def t_sign():
        return _wq("Is the answer to %s × %s positive or negative?" % (_neg(a), _neg(b)), "positive" if a * b > 0 else "negative",
                   ["%s." % ("Same signs" if a * b > 0 else "Different signs")], "positive / negative")

    def t_mult_div():
        x, k, q = [random.choice([-1, 1]) * random.randint(2, 9) for _ in range(3)]
        return _tb("Work out  %s × %s ÷ %s" % (_neg(x), _neg(k * q), _neg(k)), x * q, "int", {},
                   ["Left to right: %s × %s = %d; ÷ %s = %d." % (_neg(x), _neg(k * q), x * k * q, _neg(k), x * q)])

    return _pick_t(_by(d, [t_mult, t_div, t_square, t_sign],
                       [t_mult, t_div, t_square, t_three, t_missing, t_sign],
                       [t_mult, t_div, t_square, t_three, t_missing, t_mult_div]))


def _neg_square(x):
    """(-7)² = 49, with the reason a child who wrote -49 needs."""
    if x >= 0:
        return "%d² = %d." % (x, x * x)
    return "(%d)² = (%d) × (%d) = %d: a negative times a negative is positive." % (x, x, x, x * x)


@skill("Y7.6.d", "Directed numbers: priority of operations and substitution", S6)
def _(d=1):
    d = _d(d)
    x = random.randint(*_by(d, (-5, -1), (-9, -1), (-12, -2)))
    y = random.randint(*_by(d, (-4, 4), (-6, 6), (-12, 12))) or 2

    def t_sub_linear():
        m, c = random.randint(2, 8), random.randint(-10, 10) or 3
        return _tb("Find the value of %dx %s when x = %d." % (m, "+ %d" % c if c >= 0 else "− %d" % -c, x), m * x + c,
                   "int", {}, ["%d × (%d) %s %d = %d." % (m, x, "+" if c >= 0 else "−", abs(c), m * x + c)])

    def t_sub_square():
        return _tb("Find the value of x² when x = %d." % x, x * x, "int", {}, [_neg_square(x)])

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
        m, c = random.randint(2, 5), random.randint(-5, 5) or 1
        rows = [[v, m * v + c] for v in _by(d, (-2, -1, 0, 1), (-3, -1, 0, 2), (-6, -3, 0, 4))]
        k = random.randrange(4)
        return _io("Complete the table for y = %dx %s." % (m, "+ %d" % c if c >= 0 else "− %d" % -c), rows, k, rows[k][1],
                   ["%d × (%d) %s %d = %d." % (m, rows[k][0], "+" if c >= 0 else "−", abs(c), rows[k][1])])

    def t_sub_power():
        m, c = random.randint(2, 5), random.randint(-10, 10) or -4
        return _tb("Find the value of %dx² %s when x = %d." % (m, "+ %d" % c if c >= 0 else "− %d" % -c, x), m * x * x + c,
                   "int", {}, ["Square first: " + _neg_square(x),
                               "%d × %d %s %d = %d." % (m, x * x, "+" if c >= 0 else "−", abs(c), m * x * x + c)])

    # easy: one substitution; hard: two variables, brackets and a squared term with a coefficient
    return _pick_t(_by(d, [t_sub_linear, t_sub_square, t_order],
                       [t_sub_linear, t_sub_square, t_sub_two, t_order, t_brackets],
                       [t_sub_linear, t_sub_two, t_order, t_brackets, t_sub_power]), [t_table])
