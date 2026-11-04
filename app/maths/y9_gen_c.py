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

    def t_strip():
        who = _who()
        return _strip("%s and a friend share £%d in the ratio %d:%d. How much does %s get, in pounds?" % (who, (a + b) * unit, a, b, who),
                      {"mode": "equal_parts", "parts": a + b, "partLabel": "?", "total": (a + b) * unit, "totalLabel": "£%d" % ((a + b) * unit)},
                      a * unit, ["%d parts = £%d, so 1 part = £%d." % (a + b, (a + b) * unit, unit), "%d × %d = £%d." % (a, unit, a * unit)])

    def t_join():
        k = random.randint(2, 9)
        p, q = pick([(3, 4), (2, 3), (4, 5), (5, 7), (3, 5)])
        return _tb("In a club, boys and girls are in the ratio %d:%d. Then %d more boys join and now there are equal numbers of boys and "
                   "girls. How many girls are in the club?" % (p, q, k * (q - p)), q * k, "int", {},
                   ["The extra boys make up %d part%s: %d part%s = %d." % (q - p, "" if q - p == 1 else "s", q - p, "" if q - p == 1 else "s", k * (q - p)),
                    "1 part = %d, girls = %d × %d = %d." % (k, q, k, q * k)])

    def t_link():
        p, q, r = random.randint(1, 6), random.randint(2, 6), random.randint(1, 9)
        g = _g(p, r)
        return _wq("a:b = %d:%d and b:c = %d:%d. Write a:c in its simplest form (like 2:5)." % (p, q, q, r), "%d:%d" % (p // g, r // g),
                   ["b matches in both, so a:b:c = %d:%d:%d." % (p, q, r), "a:c = %d:%d." % (p // g, r // g)], "e.g. 2:5")

    def t_frac_to_ratio():
        num, den = pick([(2, 5), (3, 8), (1, 4), (3, 7), (4, 9), (5, 12), (2, 7)])
        return _wq("%s of the members of a choir are boys and the rest are girls. Write the ratio boys:girls (like 2:3)." % _fs(Fraction(num, den)),
                   "%d:%d" % (num, den - num), ["Boys %d parts out of %d; girls %d parts." % (num, den, den - num)], "e.g. 2:3")

    def t_squash():
        r = random.randint(4, 9)
        part = random.randint(1, 6) * 50
        lit = _ds(Fraction(part * (r + 1), 1000))
        lw = "litre" if lit == "1" else "litres"
        return _tb("Squash is mixed with water in the ratio 1:%d. A jug holds %s %s of drink. How much squash is in it, in ml?"
                   % (r, lit, lw), part, "int", {"unit": "ml"},
                   ["%s %s = %d ml." % (lit, lw, part * (r + 1)), "%d ÷ %d parts = %d ml." % (part * (r + 1), r + 1, part)])

    def t_map():
        sc = pick([25000, 50000, 10000, 20000])
        cm = random.randint(2, 12)
        return _tb("A map has scale 1:%s. Two towns are %d cm apart on the map. How far apart are they in real life, in km?" % (_c(sc), cm),
                   _ds(Fraction(sc * cm, 100000)), "num", {"unit": "km"},
                   ["%d × %s = %s cm." % (cm, _c(sc), _c(sc * cm)), "÷ 100,000 = %s km." % _ds(Fraction(sc * cm, 100000))])

    return _pick_t([t_difference, t_one_part, t_fraction, t_three, t_simplify, t_units, t_one_to_n, t_join, t_link, t_frac_to_ratio, t_squash,
                    t_map], [t_strip])


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

    def t_direct_formula():
        k = random.randint(2, 9)
        x1, x2 = random.sample(range(2, 12), 2)
        return _tb("y is directly proportional to x. When x = %d, y = %d. Find y when x = %d." % (x1, k * x1, x2), k * x2, "int", {},
                   ["y = kx, so k = %d ÷ %d = %d." % (k * x1, x1, k), "y = %d × %d = %d." % (k, x2, k * x2)])

    def t_inverse_formula():
        k = pick([12, 24, 36, 48, 60, 72, 120])
        x1, x2 = random.sample([v for v in range(2, 13) if k % v == 0], 2)
        return _tb("y is inversely proportional to x. When x = %d, y = %d. Find y when x = %d." % (x1, k // x1, x2), k // x2, "int", {},
                   ["y = k/x, so k = %d × %d = %d." % (x1, k // x1, k), "y = %d ÷ %d = %d." % (k, x2, k // x2)])

    def t_graph():
        k = random.randint(1, 3)
        x0 = random.randint(1, 2)
        return {"prompt": "The graph shows y directly proportional to x. What is the value of k in y = kx?", "component": "coordinate_grid",
                "spec": {"xmin": -1, "xmax": 7, "ymin": -1, "ymax": 7, "lines": [{"p1": [0, 0], "p2": [x0, k * x0]}],
                         "points": [[x0, k * x0, "P"]], "typed": True, "placeholder": "k ="},
                "answer": k, "answer_type": "num", "solution": ["P is (%d,%d): k = %d ÷ %d = %d." % (x0, k * x0, k * x0, x0, k)]}

    def t_origin():
        return {"prompt": "The graph of a direct proportion is a straight line through which point? Type it like (2,5).", "component": "number",
                "spec": {"text": True, "placeholder": "(x,y)"}, "answer": "(0,0)", "answer_type": "coord",
                "solution": ["When x = 0, y = k × 0 = 0: the line passes through the origin (0,0)."]}

    def t_animals():
        n, days = random.randint(2, 8) * 2, random.randint(3, 12)
        n2 = pick([v for v in range(2, 25) if v != n and (n * days) % v == 0])
        return _tb("Hay for %d horses lasts %d days. How long would the same hay last %d horses, in days?" % (n, days, n2), n * days // n2, "int",
                   {"unit": "days"}, ["%d horse-days of hay." % (n * days), "%d ÷ %d = %d." % (n * days, n2, n * days // n2)])

    def t_direct_table():
        k = random.randint(3, 15)
        xs = sorted(random.sample(range(1, 13), 4))
        rows = [[x, k * x] for x in xs]
        i = random.randrange(1, 4)
        return _io("y is directly proportional to x. What goes in the empty cell?", rows, i, rows[i][1],
                   ["y ÷ x = %d each time." % k, "%d × %d = %d." % (rows[i][0], k, rows[i][1])])

    return _pick_t([t_inverse_workers, t_inverse_speed, t_direct, t_which, t_recipe, t_direct_formula, t_inverse_formula, t_origin, t_animals],
                   [t_table, t_graph, t_direct_table])


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

    def t_time():
        sp = pick([40, 48, 50, 80, 90, 120])          # not 60, where km and minutes match
        mins = pick([30, 45, 75, 90, 105, 150])
        dist = Fraction(sp * mins, 60)
        if dist.denominator != 1:
            mins = 60
            dist = Fraction(sp)
        dist = int(dist)
        return _tb("A coach travels %d km at a steady %d km/h. How long does the journey take, in minutes?" % (dist, sp), mins, "int",
                   {"unit": "minutes"}, ["%d ÷ %d = %s hour%s." % (dist, sp, _ds(Fraction(mins, 60)), "" if mins == 60 else "s"), "= %d minutes." % mins])

    def t_cube_mass():
        dens, s = pick([("19", 2), ("8", 3), ("11", 2), ("3", 4), ("7", 3)])
        return _tb("A solid cube has edges of %d cm and is made of a metal with density %s g/cm³. What is its mass, in grams?" % (s, dens),
                   int(dens) * s ** 3, "int", {"unit": "g"}, ["Volume = %d³ = %d cm³." % (s, s ** 3), "%d × %s = %d g." % (s ** 3, dens, int(dens) * s ** 3)])

    def t_area_from_pressure():
        p, a = random.randint(2, 20) * 25, random.randint(2, 12)
        return _tb("A box exerts a pressure of %d N/m² with a force of %d N. What area is it resting on, in m²?" % (p, p * a), a, "int",
                   {"unit": "m²"}, ["area = force ÷ pressure = %d ÷ %d = %d." % (p * a, p, a)])

    def t_fuel():
        per100 = random.randint(4, 9)
        km = pick([50, 150, 200, 250, 300, 350, 400, 450])
        return _tb("A car uses %d litres of fuel per 100 km. How much fuel does it use on a %d km journey, in litres?" % (per100, km),
                   _ds(Fraction(per100 * km, 100)), "num", {"unit": "litres"}, ["%d ÷ 100 × %d = %s." % (per100, km, _ds(Fraction(per100 * km, 100)))])

    def t_pop_density():
        dens, area = random.randint(2, 40) * 100, random.randint(2, 15)
        return _tb("A town of %s people covers %d km². What is its population density, in people per km²?" % (_c(dens * area), area), dens,
                   "int", {"unit": "people/km²"}, ["%s ÷ %d = %s." % (_c(dens * area), area, _c(dens))])

    def t_faster():
        s1, s2 = random.sample(range(3, 10), 2)
        t1, t2 = pick([10, 20, 25]), pick([12, 15, 30])
        a, b = _who(), _who()
        while b == a:
            b = _who()
        return _tb("%s runs %d m in %d s. %s runs %d m in %d s. What is the speed of the faster runner, in m/s?" % (a, s1 * t1, t1, b, s2 * t2, t2),
                   max(s1, s2), "int", {"unit": "m/s"}, ["%s: %d m/s. %s: %d m/s." % (a, s1, b, s2)])

    return _pick_t([t_speed, t_minutes, t_convert, t_density, t_pressure, t_rate, t_avg_speed, t_time, t_cube_mass, t_area_from_pressure,
                    t_fuel, t_pop_density, t_faster])


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

    def t_years():
        target = pick([Fraction(5, 4), Fraction(3, 2), 2])
        v, yrs = Decimal(P), 0
        while v <= P * Decimal(target.numerator) / target.denominator:
            v *= 1 + Decimal(r) / 100
            yrs += 1
        return _tb("£%d is invested at %d%% compound interest per year. After how many whole years will it first be worth more than £%s?"
                   % (P, r, _ds(P * target)), yrs, "int", {"unit": "years"},
                   ["Keep multiplying by %s: after %d years it is £%s." % (_ds(1 + Decimal(r) / 100), yrs, format(v.quantize(Decimal("0.01")), "f"))])

    def t_rate_from_multiplier():
        k = random.randint(1, 30)
        up = random.random() < 0.5
        mult = (Decimal(100 + k) if up else Decimal(100 - k)) / 100
        return _tb("A value is multiplied by %s each year. What is the yearly percentage %s?" % (_ds(mult), "increase" if up else "decrease"), k,
                   "int", {"unit": "%"}, ["%s = %s %s %s." % (_ds(mult), "1", "+" if up else "−", _ds(Decimal(k) / 100)), "That is %d%%." % k])

    def t_doubling():
        start, hrs = pick([100, 200, 250, 500, 1000]), random.randint(3, 7)
        return _tb("A colony of %d bacteria doubles every hour. How many bacteria are there after %d hours?" % (start, hrs), start * 2 ** hrs,
                   "int", {}, ["%d × 2^%d = %s." % (start, hrs, _c(start * 2 ** hrs))])

    def t_table():
        rate = pick([10, 20, 50])
        start = pick([1000, 2000, 500])
        vals = [Decimal(start) * (1 + Decimal(rate) / 100) ** k for k in range(4)]
        i = random.randint(1, 3)
        return _dt("Money grows by %d%% compound interest each year. Complete the table (in pounds)." % rate, ["Year", "Value (£)"],
                   [[k, _ds(v)] for k, v in enumerate(vals)], _ds(vals[i]),
                   ["Multiply the year before by %s: %s × %s = %s." % (_ds(1 + Decimal(rate) / 100), _ds(vals[i - 1]), _ds(1 + Decimal(rate) / 100), _ds(vals[i]))],
                   missing=[i, 1], atype="num")

    def t_graph_rate():
        rate, start = pick([(10, 10000), (20, 6250), (25, 2560), (50, 1600)])     # every value a whole number of pounds
        pts = [["Year %d" % k, int(Decimal(start) * (1 - Decimal(rate) / 100) ** k)] for k in range(5)]
        return _lg("The graph shows a machine's value (in £) as it loses the same percentage each year. What percentage does it lose each year?",
                   pts, rate, ["%d → %d: a fall of %d, which is %d%% of %d." % (pts[0][1], pts[1][1], pts[0][1] - pts[1][1], rate, pts[0][1])],
                   "£", "Year")

    def t_interest_only():
        v = (Decimal(P) * (1 + Decimal(r) / 100) ** n).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
        return _tb("£%d is saved at %d%% compound interest per year for %d years. How much INTEREST is earned? Give pounds to 2 decimal places."
                   % (P, r, n), _ds(v - P), "num", {"unit": "£"}, ["Final value £%s." % format(v, "f"), "£%s − £%d = £%s." % (format(v, "f"), P, format(v - P, "f"))])

    return _pick_t([t_compound, t_multiplier, t_depreciation, t_simple_vs_compound, t_up_down, t_years, t_rate_from_multiplier, t_doubling,
                    t_interest_only], [t_table, t_graph_rate])


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

    def t_reverse_odd():
        p = pick([15, 35, 45, 12, 8])
        orig = random.randint(1, 20) * 100
        new = orig * (100 - p) // 100
        return _tb("A house plant's price fell by %d%% to £%d. What was it before, in pounds?" % (p, new), orig, "int", {"unit": "£"},
                   ["%d%% = £%d." % (100 - p, new), "£%d ÷ %s = £%d." % (new, _ds(Fraction(100 - p, 100)), orig)])

    def t_new_as_pct():
        old = random.randint(2, 20) * 20
        p = pick([110, 125, 150, 80, 75, 60, 140])
        return _tb("A price changes from £%d to £%d. The new price is what percentage of the old price?" % (old, old * p // 100), p, "int",
                   {"unit": "%"}, ["%d ÷ %d × 100 = %d%%." % (old * p // 100, old, p)])

    def t_pay_rise():
        p = pick([2, 4, 5, 10])
        old = random.randint(10, 60) * 50
        who = _who()
        return _tb("After a %d%% pay rise, %s earns £%s a month. How much did they earn before the rise, in pounds?" % (p, who, _c(old * (100 + p) // 100)),
                   old, "int", {"unit": "£"}, ["%d%% = £%s." % (100 + p, _c(old * (100 + p) // 100)), "÷ %s = £%s." % (_ds(Fraction(100 + p, 100)), _c(old))])

    def t_mistake():
        p = pick([20, 25, 50, 10])
        orig = random.randint(2, 30) * 20
        new = orig * (100 + p) // 100
        wrong = new - new * p // 100 if (new * p) % 100 == 0 else None
        if wrong is None or wrong == orig:
            return t_reverse_up()
        who = _who()
        return _tb("After a %d%% increase a price is £%d. %s works out the original price as £%s by taking %d%% off £%d. That is wrong. "
                   "What was the original price, in pounds?" % (p, new, who, _ds(wrong), p, new), orig, "int", {"unit": "£"},
                   ["£%d is %d%% of the original, so divide by %s." % (new, 100 + p, _ds(Fraction(100 + p, 100))), "£%d ÷ %s = £%d." % (new, _ds(Fraction(100 + p, 100)), orig)])

    def t_house():
        old = random.randint(15, 40) * 10000
        p = pick([2, 4, 5, 6, 8, 10])
        new = old - old * p // 100
        return _tb("A house price falls from £%s to £%s. What is the percentage decrease?" % (_c(old), _c(new)), p, "int", {"unit": "%"},
                   ["Fall £%s." % _c(old - new), "%s ÷ %s × 100 = %d%%." % (_c(old - new), _c(old), p)])

    def t_divide_by():
        p = random.randint(1, 60)
        return _tb("A price has been increased by %d%%. What single number do you divide the new price by to find the original?" % p,
                   _ds(Fraction(100 + p, 100)), "num", {}, ["The new price is %d%% = %s × the original." % (100 + p, _ds(Fraction(100 + p, 100)))])

    def t_strip():
        p = pick([20, 25, 50])
        orig = random.randint(2, 30) * (100 // p)
        new = orig * (100 + p) // 100
        parts = 100 // p + 1
        return _strip("After a %d%% increase a bag holds %d g. The bar shows the new amount split into %d equal parts of %d%% each. How much did "
                      "the bag hold before the increase, in grams?" % (p, new, parts, p),
                      {"mode": "equal_parts", "parts": parts, "partLabel": "%d%%" % p, "total": new, "totalLabel": "%d g" % new},
                      orig, ["%d parts = %d g, so 1 part = %d g." % (parts, new, new // parts), "The original is %d parts: %d g." % (parts - 1, orig)])

    return _pick_t([t_reverse_up, t_reverse_down, t_vat, t_change, t_profit, t_reverse_odd, t_new_as_pct, t_pay_rise, t_mistake, t_house,
                    t_divide_by], [t_strip])
