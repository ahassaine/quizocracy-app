# Year 9 generators: strands 9.4 and 9.5.
#
# Ratio and proportion: ratio problems with differences and totals, ratio as a fraction, direct and
# inverse proportion, compound measures (speed with unit changes, density, pressure, rates).
# Percentages and finance: repeated percentage change and compound interest, depreciation, reverse
# percentages, percentage change and comparison, simple versus compound interest.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S4 = "9.4 Ratio, proportion & compound measures"
S5 = "9.5 Percentages & finance"


# ================================================================== 9.4 ======
@skill("Y9.4.a", "Ratio problems with differences and totals", S4)
def _(d=1):
    d = _d(d)
    a, b = random.randint(1, 7), random.randint(1, 7)
    while a == b:
        b = random.randint(1, 7)
    unit = random.randint(2, 15)

    def t_difference():
        return _tb("Sweets are shared between Ali and Ben in the ratio %d:%d. Ben gets %d %s sweets than Ali. How many sweets are there "
                   "altogether?" % (a, b, abs(b - a) * unit, "more" if b > a else "fewer"), (a + b) * unit, "int", {},
                   ["The difference is %d part%s = %d, so 1 part = %d." % (abs(b - a), "" if abs(b - a) == 1 else "s", abs(b - a) * unit, unit),
                    "%d parts = %d." % (a + b, (a + b) * unit)])

    def t_one_part():
        return _tb("Red and blue beads are in the ratio %d:%d. There are %d red beads. How many blue beads?" % (a, b, a * unit), b * unit,
                   "int", {}, ["1 part = %d." % unit, "%d × %d = %d." % (b, unit, b * unit)])

    def t_fraction():
        return _fq("Boys and girls are in the ratio %d:%d. What fraction of the group are girls?" % (a, b), Fraction(b, a + b),
                   ["Girls are %d out of %d parts." % (b, a + b)])

    def t_three():
        c = random.randint(1, 5)
        return _tb("£%d is shared in the ratio %d:%d:%d. How much is the largest share, in pounds?" % ((a + b + c) * unit, a, b, c),
                   max(a, b, c) * unit, "int", {"unit": "£"}, ["1 part = £%d." % unit, "Largest share: %d × %d = %d." % (max(a, b, c), unit, max(a, b, c) * unit)])

    def t_simplify():
        k = random.randint(2, 8)
        return _wq("Write %d:%d in its simplest form (like 2:3)." % (a * k, b * k), "%d:%d" % (a // _g(a, b), b // _g(a, b)),
                   ["Divide both by %d." % (k * _g(a, b))], "e.g. 2:3")

    def t_units():
        cm = random.randint(20, 90)
        return _wq("Write the ratio %d cm : 1 m in its simplest form (like 2:5)." % cm, "%d:%d" % (cm // _g(cm, 100), 100 // _g(cm, 100)),
                   ["1 m = 100 cm, so %d:100." % cm], "e.g. 2:5")

    def t_one_to_n():
        k = pick([2, 4, 5, 8])
        x = random.randint(1, 9) * k
        return _tb("Write %d:%d in the form 1:n. What is n?" % (k, x), x // k, "int", {}, ["Divide both by %d." % k])

    return _pick_t([t_difference, t_one_part, t_fraction, t_three, t_simplify, t_units, t_one_to_n])


def _g(a, b):
    while b:
        a, b = b, a % b
    return a


@skill("Y9.4.b", "Direct and inverse proportion", S4)
def _(d=1):
    d = _d(d)

    def t_inverse_workers():
        w, days = random.randint(2, 6), random.randint(2, 12)
        w2 = pick([x for x in (2, 3, 4, 6, 8, 12) if x != w and (w * days) % x == 0] or [w * 2])
        return _tb("%d builders take %d days to build a wall. How many days would %d builders take, working at the same rate?" % (w, days, w2),
                   _ds(Fraction(w * days, w2)), "num", {"unit": "days"}, ["Total work = %d builder-days." % (w * days), "%d ÷ %d = %s." % (w * days, w2, _ds(Fraction(w * days, w2)))])

    def t_inverse_speed():
        s, t = random.randint(2, 8) * 10, random.randint(2, 6)
        s2 = pick([x for x in (20, 30, 40, 60, 80, 120) if x != s and (s * t) % x == 0] or [s * 2])
        return _tb("A journey takes %d hours at %d km/h. How long does it take at %d km/h, in hours?" % (t, s, s2), _ds(Fraction(s * t, s2)),
                   "num", {"unit": "hours"}, ["Distance %d km." % (s * t), "%d ÷ %d = %s h." % (s * t, s2, _ds(Fraction(s * t, s2)))])

    def t_direct():
        n, cost = random.randint(2, 8), random.randint(30, 250)
        n2 = random.randint(3, 15)
        return _tb("%d metres of cable cost £%d. How much do %d metres cost, in pounds?" % (n, n * cost, n2),
                   n2 * cost, "int", {"unit": "£"}, ["1 m = £%d." % cost, "%d × %d = %d." % (n2, cost, n2 * cost)])

    def t_which():
        q, a = pick([("The number of people painting a fence and the time it takes", "inverse"),
                     ("The number of tickets bought and the total cost", "direct"),
                     ("The speed of a car and the time a fixed journey takes", "inverse"),
                     ("The length of a fence and the number of posts needed", "direct")])
        return _wq("%s: is this direct or inverse proportion?" % q, a, ["Direct: both increase together. Inverse: one goes up as the other goes down."],
                   "direct / inverse")

    def t_table():
        k = random.randint(2, 9) * 6
        xs = [1, 2, 3, 6]
        rows = [[x, k // x] for x in xs]
        i = random.randrange(4)
        return _io("y is inversely proportional to x (x × y is always the same). What goes in the empty cell?", rows, i, rows[i][1],
                   ["x × y = %d." % k, "%d ÷ %d = %d." % (k, rows[i][0], rows[i][1])])

    def t_recipe():
        serves, g = 4, random.randint(4, 30) * 10
        n = pick([6, 10, 2, 12])
        return _tb("A recipe for %d people needs %d g of rice. How much for %d people, in grams?" % (serves, g, n), g * n // serves, "int",
                   {"unit": "g"}, ["%d ÷ %d × %d = %d." % (g, serves, n, g * n // serves)])

    return _pick_t([t_inverse_workers, t_inverse_speed, t_direct, t_which, t_recipe], [t_table])


@skill("Y9.4.c", "Compound measures: speed, density and pressure", S4)
def _(d=1):
    d = _d(d)

    def t_speed():
        sp, t = random.randint(4, 12) * 10, pick([Fraction(1, 2), Fraction(3, 2), 2, Fraction(5, 2), 3])
        return _tb("A car travels at %d km/h for %s hours. How far does it go, in km?" % (sp, _ds(Fraction(t))), _ds(sp * Fraction(t)),
                   "num", {"unit": "km"}, ["%d × %s = %s." % (sp, _ds(Fraction(t)), _ds(sp * Fraction(t)))])

    def t_minutes():
        sp = random.randint(2, 10) * 12            # 12k km/h × m/60 h is always exact for these m
        m = pick([15, 20, 30, 45, 90])
        return _tb("A train travels at %d km/h. How far does it travel in %d minutes, in km?" % (sp, m), _ds(Fraction(sp * m, 60)), "num",
                   {"unit": "km"}, ["%d minutes = %s hours." % (m, _ds(Fraction(m, 60))), "%d × %s = %s." % (sp, _ds(Fraction(m, 60)), _ds(Fraction(sp * m, 60)))])

    def t_convert():
        ms = random.randint(2, 30)
        return _tb("Convert %d m/s to km/h." % ms, _ds(Fraction(ms * 3600, 1000)), "num", {"unit": "km/h"},
                   ["× 3600 seconds, ÷ 1000 metres: × 3.6.", "%d × 3.6 = %s." % (ms, _ds(Fraction(ms * 3600, 1000)))])

    def t_density():
        dens, vol = random.randint(2, 12), random.randint(5, 50)
        q = pick(["mass", "density", "volume"])
        if q == "mass":
            return _tb("A metal has density %d g/cm³. What is the mass of %d cm³, in grams?" % (dens, vol), dens * vol, "int", {"unit": "g"},
                       ["mass = density × volume = %d." % (dens * vol)])
        if q == "density":
            return _tb("An object has mass %d g and volume %d cm³. What is its density, in g/cm³?" % (dens * vol, vol), dens, "int",
                       {"unit": "g/cm³"}, ["density = mass ÷ volume = %d." % dens])
        return _tb("A block has mass %d g and density %d g/cm³. What is its volume, in cm³?" % (dens * vol, dens), vol, "int", {"unit": "cm³"},
                   ["volume = mass ÷ density = %d." % vol])

    def t_pressure():
        f, a = random.randint(2, 20) * 10, random.randint(2, 10)
        return _tb("A force of %d N acts on an area of %d m². What is the pressure, in N/m²?" % (f * a, a), f, "int", {"unit": "N/m²"},
                   ["pressure = force ÷ area = %d." % f])

    def t_rate():
        lit, mins = random.randint(2, 12), random.randint(3, 15)
        return _tb("A tap fills a tank at %d litres per minute. The tank holds %d litres. How many minutes to fill it?" % (lit, lit * mins), mins,
                   "int", {"unit": "minutes"}, ["%d ÷ %d = %d." % (lit * mins, lit, mins)])

    def t_avg_speed():
        d1, d2 = random.randint(2, 6) * 10, random.randint(2, 6) * 10
        return _tb("A cyclist rides %d km in the first hour and %d km in the second hour. What is the average speed, in km/h?" % (d1, d2),
                   _ds(Fraction(d1 + d2, 2)), "num", {"unit": "km/h"}, ["Total %d km in 2 hours." % (d1 + d2)])

    return _pick_t([t_speed, t_minutes, t_convert, t_density, t_pressure, t_rate, t_avg_speed])


# ================================================================== 9.5 ======
@skill("Y9.5.a", "Compound interest and repeated percentage change", S5)
def _(d=1):
    d = _d(d)
    P = random.randint(2, 20) * 100
    r = pick([2, 3, 4, 5, 10])
    n = random.randint(2, 3)

    def t_compound():
        v = Decimal(P) * (1 + Decimal(r) / 100) ** n
        return _tb("£%d is invested at %d%% compound interest per year. What is it worth after %d years? Give pounds to 2 decimal places."
                   % (P, r, n), _ds(v.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")), "num", {"unit": "£"},
                   ["%d × %s^%d = %s." % (P, _ds(1 + Decimal(r) / 100), n, format(v.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"), "f"))])

    def t_multiplier():
        up = random.random() < 0.5
        return _tb("What single number do you multiply by to %s an amount by %d%% each year for %d years? (Give it to 4 decimal places.)"
                   % ("increase" if up else "decrease", r, n), _ds(((1 + Decimal(r) / 100) if up else (1 - Decimal(r) / 100)) ** n),
                   "num", {}, ["(%s)^%d." % (_ds((1 + Decimal(r) / 100) if up else (1 - Decimal(r) / 100)), n)], tol=0.00005)

    def t_depreciation():
        v = Decimal(P * 10) * (1 - Decimal(r * 2) / 100) ** n
        return _tb("A car worth £%d loses %d%% of its value each year. What is it worth after %d years? Give pounds to 2 decimal places."
                   % (P * 10, r * 2, n), _ds(v.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")), "num", {"unit": "£"},
                   ["%d × %s^%d." % (P * 10, _ds(1 - Decimal(r * 2) / 100), n)])

    def t_simple_vs_compound():
        simple = P * r * n // 100
        comp = (Decimal(P) * (1 + Decimal(r) / 100) ** n - P).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
        return _tb("£%d is invested for %d years at %d%%. How much MORE interest does compound interest give than simple interest? Give "
                   "pounds to 2 decimal places." % (P, n, r), _ds(comp - simple), "num", {"unit": "£"},
                   ["Simple: £%d. Compound: £%s." % (simple, format(comp, "f"))])

    def t_up_down():
        p = pick([10, 20, 25, 50])
        x = random.randint(2, 20) * 20
        res = Fraction(x) * Fraction(100 + p, 100) * Fraction(100 - p, 100)
        return _tb("A price of £%d goes up by %d%% and then down by %d%%. What is the final price, in pounds?" % (x, p, p), _ds(res), "num",
                   {"unit": "£"}, ["%d × %s × %s = %s." % (x, _ds(Fraction(100 + p, 100)), _ds(Fraction(100 - p, 100)), _ds(res)),
                                   "It does not return to £%d." % x])

    return _pick_t([t_compound, t_multiplier, t_depreciation, t_simple_vs_compound, t_up_down])


@skill("Y9.5.b", "Reverse percentages and percentage change", S5)
def _(d=1):
    d = _d(d)

    def t_reverse_up():
        p = pick([10, 20, 25, 50, 5])
        orig = random.randint(2, 40) * 20
        new = orig * (100 + p) // 100
        return _tb("After a %d%% increase, a price is £%d. What was the original price, in pounds?" % (p, new), orig, "int", {"unit": "£"},
                   ["%d%% of the original = £%d." % (100 + p, new), "£%d ÷ %s = £%d." % (new, _ds(Fraction(100 + p, 100)), orig)])

    def t_reverse_down():
        p = pick([10, 20, 25, 30, 40])
        orig = random.randint(2, 40) * 10
        new = orig * (100 - p) // 100
        return _tb("In a %d%% sale, a coat costs £%d. What was the price before the sale, in pounds?" % (p, new), orig, "int", {"unit": "£"},
                   ["%d%% = £%d." % (100 - p, new), "£%d ÷ %s = £%d." % (new, _ds(Fraction(100 - p, 100)), orig)])

    def t_vat():
        orig = random.randint(2, 50) * 10
        return _tb("A price including 20%% VAT is £%d. What is the price without VAT, in pounds?" % (orig * 6 // 5), orig, "int", {"unit": "£"},
                   ["£%d ÷ 1.2 = £%d." % (orig * 6 // 5, orig)])

    def t_change():
        old = random.randint(2, 20) * 20
        new = old + pick([-1, 1]) * old * pick([5, 10, 15, 20, 25, 40]) // 100
        return _tb("A value changes from %d to %d. What is the percentage change? (Use a minus sign for a decrease.)" % (old, new),
                   _ds(Fraction((new - old) * 100, old)), "num", {}, ["(%d − %d) ÷ %d × 100." % (new, old, old)])

    def t_profit():
        cost = random.randint(2, 30) * 10
        p = pick([10, 20, 25, 40, 50])
        return _tb("A shop buys a bike for £%d and sells it for £%d. What is the percentage profit?" % (cost, cost * (100 + p) // 100), p,
                   "int", {}, ["Profit £%d." % (cost * p // 100), "%d ÷ %d × 100 = %d%%." % (cost * p // 100, cost, p)])

    return _pick_t([t_reverse_up, t_reverse_down, t_vat, t_change, t_profit])
