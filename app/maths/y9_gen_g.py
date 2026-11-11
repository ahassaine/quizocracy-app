# Year 9 generators (added 2 Nov 2026 to widen the bank): strands 9.4–9.9, the KS3 statements the
# first Year 9 bank left out.
#
# Rates, exchange rates and changing compound units; ratio linked to fractions and to linear
# functions.  Money: wages and overtime, simple income tax, bills, payslips, statements and best buys.
# Angle reasoning with algebra (parallel lines, polygons).  Systematic listing, counting outcomes and
# tree diagrams.  Charts for grouped numerical data.
from .maths_engine import skill, ordinal
from .y5_common import *  # noqa: F401,F403
from .y9_gen_a import _g
from .y9_gen_c import S4, S5
from .y9_gen_d import S6
from .y9_gen_e import S8, S9


def _ex(a, b):
    """ax + b for display inside an angle or length: x, 3x + 20, 2x − 5."""
    return "%s%s" % ("x" if a == 1 else "%dx" % a, "" if b == 0 else (" + %d" % b if b > 0 else " − %d" % -b))


def _money(v):
    """Pounds to 2 decimal places as text: 341.04, 5.25, 12.00 -> '12.00'."""
    return format(Decimal(v).quantize(Decimal("0.01")), "f")


# ================================================================== 9.4 ======
_CURR = [("euros", "€", Decimal("1.15")), ("US dollars", "$", Decimal("1.25")), ("euros", "€", Decimal("1.20")),
         ("Swiss francs", "CHF ", Decimal("1.10"))]


@skill("Y9.4.d", "Rates, exchange rates and changing compound units", S4)
def _(d=1):
    d = _d(d)
    name, sym, rate = pick(_CURR)

    def t_to_foreign():
        gbp = random.randint(2, _by(d, 10, 40, 40)) * 10
        return _tb("£1 = %s%s. How many %s do you get for £%d?" % (sym, _money(rate), name, gbp), _money(gbp * rate), "num", {},
                   ["%d × %s = %s." % (gbp, _money(rate), _money(gbp * rate))])

    def t_to_pounds():
        gbp = random.randint(2, 40) * 4
        return _tb("£1 = %s%s. A meal costs %s%s. How much is that in pounds?" % (sym, _money(rate), sym, _money(gbp * rate)), gbp, "num",
                   {"unit": "£"}, ["%s ÷ %s = %d." % (_money(gbp * rate), _money(rate), gbp)])

    def t_compare():
        uk = random.randint(8, 40) * 5
        abroad_gbp = uk + pick([-1, 1]) * random.randint(1, 5) * 4
        abroad = abroad_gbp * rate
        return _tb("A pair of trainers costs £%d in the UK and %s%s abroad, where £1 = %s%s. How much cheaper is the cheaper one, in pounds?"
                   % (uk, sym, _money(abroad), sym, _money(rate)), abs(uk - abroad_gbp), "num", {"unit": "£"},
                   ["%s%s ÷ %s = £%d." % (sym, _money(abroad), _money(rate), abroad_gbp), "Difference £%d." % abs(uk - abroad_gbp)])

    def t_commission():
        gbp, pct = random.randint(1, 10) * 100, pick([1, 2, 3])
        left = gbp * (100 - pct) // 100
        return _tb("A bureau takes %d%% commission from the pounds first, then changes the rest at £1 = %s%s. How many %s do you get for £%d?"
                   % (pct, sym, _money(rate), name, gbp), _ds(left * rate), "num", {},
                   ["%d%% of £%d = £%d, leaving £%d." % (pct, gbp, gbp - left, left), "%d × %s = %s." % (left, _money(rate), _ds(left * rate))])

    def t_kmh_ms():
        v = 18 * random.randint(1, 7)
        return _tb("Convert %d km/h to m/s." % v, v * 5 // 18, "int", {"unit": "m/s"},
                   ["%d km/h = %s m per hour." % (v, _c(v * 1000)), "÷ 3600 seconds = %d m/s." % (v * 5 // 18)])

    def t_mmin_kmh():
        v = random.randint(2, 30) * 50
        return _tb("A cyclist rides at %d m per minute. What is that in km/h?" % v, _ds(Fraction(v * 60, 1000)), "num", {"unit": "km/h"},
                   ["%d × 60 = %s m per hour." % (v, _c(v * 60)), "÷ 1000 = %s km/h." % _ds(Fraction(v * 60, 1000))])

    def t_density_units():
        dg = Decimal(random.randint(5, 120)) / 10
        return _tb("A material has density %s g/cm³. What is that in kg/m³?" % _ds(dg), _ds(dg * 1000), "num", {"unit": "kg/m³"},
                   ["1 g/cm³ = 1000 kg/m³ (1 m³ = 1,000,000 cm³ and 1 kg = 1000 g).", "%s × 1000 = %s." % (_ds(dg), _ds(dg * 1000))])

    def t_flow():
        mls = random.randint(2, 30) * 25
        return _tb("A tap drips %d ml every second. How many litres is that per minute?" % mls, _ds(Fraction(mls * 60, 1000)), "num",
                   {"unit": "litres"}, ["%d × 60 = %s ml per minute." % (mls, _c(mls * 60)), "÷ 1000 = %s litres." % _ds(Fraction(mls * 60, 1000))])

    def t_wage_minutes():
        hourly = Decimal(random.randint(1100, 1800)) / 100
        mins = pick([15, 20, 30, 45, 40])
        pay = hourly * mins / 60
        return _tb("Someone is paid £%s per hour. How much do they earn for %d minutes, to the nearest penny?" % (_money(hourly), mins),
                   _money(pay.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")), "num", {"unit": "£"},
                   ["%s × %d ÷ 60 = %s…" % (_money(hourly), mins, format(pay.quantize(Decimal("0.0001")), "f"))])

    def t_typing():
        wpm, mins = random.randint(30, 70), random.randint(10, 90)
        words = wpm * mins
        return _tb("A typist types %d words per minute. How many minutes will %s words take?" % (wpm, _c(words)), mins, "int", {"unit": "minutes"},
                   ["%s ÷ %d = %d." % (_c(words), wpm, mins)])

    def t_table():
        rows = [["Euro (€)", "1.15"], ["US dollar ($)", "1.25"], ["Swiss franc (CHF)", "1.10"]]
        plural = ["euros", "US dollars", "Swiss francs"]
        if d == 2:                                  # hard only: yen, whose large rate gives answers in the tens of thousands
            rows.insert(2, ["Japanese yen (¥)", "190"])
            plural.insert(2, "Japanese yen")
        i = random.randrange(len(rows))
        amt = random.randint(2, 20) * 10
        r = Decimal(rows[i][1])
        return _dt("The table shows exchange rates for one pound. How many %s do you get for £%d?" % (plural[i], amt), ["Currency", "Per pound"],
                   rows, _ds(amt * r), ["%d × %s = %s." % (amt, rows[i][1], _ds(amt * r))], atype="num")

    def t_graph():
        pts = [["£%d" % g, float(g * rate)] for g in range(0, 101, 20)]
        g = random.randint(1, 5) * 20
        return _lg("The conversion graph changes pounds to %s. Use it to convert £%d." % (name, g), pts, _ds(g * rate),
                   ["Read up from £%d: %s%s." % (g, sym, _ds(g * rate))], name[:1].upper() + name[1:], "Pounds", atype="num")

    # easy: one conversion or one rate; hard: two steps (commission, compare prices) and changing both units of a compound unit
    return _pick_t(_by(d, [t_to_foreign, t_to_pounds, t_typing],
                       [t_to_foreign, t_to_pounds, t_compare, t_commission, t_kmh_ms, t_mmin_kmh, t_density_units, t_flow, t_wage_minutes, t_typing],
                       [t_compare, t_commission, t_kmh_ms, t_mmin_kmh, t_density_units, t_flow, t_wage_minutes]),
                   _by(d, [t_table, t_graph], [t_table, t_graph], [t_table]))


@skill("Y9.4.e", "Ratio, fractions and linear functions", S4)
def _(d=1):
    d = _d(d)
    a, b = random.randint(1, 9), random.randint(2, 9)
    while a == b or _g(a, b) != 1:
        a, b = random.randint(1, 9), random.randint(2, 9)

    def t_part_of_part():
        return _fq("The ratio of apples to pears is %d:%d. The number of apples is what fraction of the number of pears?" % (a, b), Fraction(a, b),
                   ["apples ÷ pears = %d/%d." % (a, b)])

    def t_part_of_whole():
        return _fq("Sand and cement are mixed in the ratio %d:%d. What fraction of the mixture is cement?" % (a, b), Fraction(b, a + b),
                   ["Cement is %d of the %d parts." % (b, a + b)])

    def t_k():
        return _fq("y and x are always in the ratio %d:%d (y:x). Write y = kx. What is k, as a fraction?" % (a, b), Fraction(a, b),
                   ["y/x = %d/%d, so y = %s x." % (a, b, _fs(Fraction(a, b)))])

    def t_unit_rate():
        kg, cost = pick([(4, 10), (5, 12), (2, 7), (8, 18), (3, 12)])
        return _tb("%d kg of potatoes cost £%d, and cost is proportional to mass. Write cost = k × mass. What is k, in pounds per kg?" % (kg, cost),
                   _ds(Fraction(cost, kg)), "num", {"unit": "£/kg"}, ["k = %d ÷ %d = %s." % (cost, kg, _ds(Fraction(cost, kg)))])

    def t_io():
        k = random.randint(2, 8)
        xs = sorted(random.sample(range(1, 13), 4))
        rows = [[x, k * x] for x in xs]
        i = random.randrange(4)
        return _io("Litres of paint (x) and area covered (y, in m²) are always in the ratio 1:%d. What goes in the empty cell?" % k, rows, i, rows[i][1],
                   ["y = %dx." % k, "%d × %d = %d." % (k, rows[i][0], rows[i][1])])

    def t_grid():
        px, py = pick(_by(d, [(1, 2), (1, 3), (2, 1), (3, 1)], [(3, 2), (2, 3), (4, 1), (1, 3), (3, 1), (2, 1)],
                          [(4, 3), (2, 3), (4, 1), (3, 2), (4, 5), (2, 5)]))
        # never ask at P itself (the picture would be the answer): a multiple of P, or (stretch) a half step
        mult = pick(_by(d, [Fraction(2)], [Fraction(2), Fraction(3)],
                        [Fraction(3)] + ([Fraction(1, 2), Fraction(5, 2)] if px % 2 == 0 else [Fraction(4)])))
        ask_x, ans = int(px * mult), py * mult
        return {"prompt": "The line shows y and x in a fixed ratio. It passes through P. What is y when x = %d?" % ask_x, "component": "coordinate_grid",
                "spec": {"xmin": -1, "xmax": 8, "ymin": -1, "ymax": 8, "lines": [{"p1": [0, 0], "p2": [px, py]}], "points": [[px, py, "P"]],
                         "typed": True, "placeholder": "y ="},
                "answer": int(ans) if ans.denominator == 1 else float(ans), "answer_type": "num",
                "solution": ["y:x = %d:%d at P." % (py, px), "x = %d is %s × %d, so y = %s × %d = %s."
                             % (ask_x, _fs(mult), px, _fs(mult), py, _fs(ans) if ans.denominator == 1 else "%g" % float(ans))]}

    def t_times_as():
        p, q = pick([(3, 2), (5, 2), (4, 3), (5, 3), (7, 4)])
        return _wq("A is %s times as big as B. Write the ratio A:B in its simplest form (like 3:2)." % _mixed(Fraction(p, q)), "%d:%d" % (p, q),
                   ["A = %s × B, so A:B = %s:1 = %d:%d." % (_fs(Fraction(p, q)), _fs(Fraction(p, q)), p, q)], "e.g. 3:2")

    def t_frac_to_ratio():
        return _wq("x is %s of y. Write the ratio x:y (like 4:7)." % _fs(Fraction(a, b)), "%d:%d" % (a, b), ["x:y = %d:%d." % (a, b)], "e.g. 4:7")

    def t_bigger_than_one():
        p, q = max(a, b), min(a, b)
        return _fq("Boys and girls in a club are in the ratio %d:%d. The number of boys is what fraction of the number of girls?" % (p, q),
                   Fraction(p, q), ["boys ÷ girls = %d/%d (more than 1, as there are more boys)." % (p, q)], "e.g. 7/4")

    def t_proportional():
        m, c = random.randint(2, 6), random.choice([0, 0, random.randint(1, 9)])
        return _wq("Is y = %dx%s a proportional relationship (y and x always in the same ratio)? (yes or no)" % (m, "" if c == 0 else " + %d" % c),
                   "yes" if c == 0 else "no", ["Proportional graphs are straight lines through the origin.",
                                               "Here y ÷ x is always %d." % m if c == 0 else "When x = 0, y = %d, not 0." % c], "yes / no")

    def t_gradient():
        p, q = pick([(2, 1), (3, 1), (3, 2), (5, 2), (4, 1)])
        return _tb("Flour and butter are used in the ratio %d:%d. A graph shows flour (up) against butter (across). What is its gradient?" % (p, q),
                   _ds(Fraction(p, q)), "num", {}, ["Every %d g of butter needs %d g of flour: gradient %d/%d = %s." % (q, p, p, q, _ds(Fraction(p, q)))])

    # easy: ratio to fraction and back directly; hard: k in y = kx, gradients, fractions above 1, mixed-number multipliers
    return _pick_t(_by(d, [t_part_of_part, t_part_of_whole, t_frac_to_ratio, t_proportional],
                       [t_part_of_part, t_part_of_whole, t_k, t_unit_rate, t_times_as, t_frac_to_ratio, t_bigger_than_one, t_proportional, t_gradient],
                       [t_part_of_whole, t_k, t_unit_rate, t_times_as, t_bigger_than_one, t_gradient]),
                   _by(d, [t_io, t_grid], [t_io, t_grid], [t_grid]))


# ================================================================== 9.5 ======
@skill("Y9.5.c", "Money: wages, tax, bills and best buys", S5)
def _(d=1):
    d = _d(d)
    who = _who()

    def t_overtime():
        rate = Decimal(random.randint(22, 36)) / 2
        basic, extra = random.randint(30, 38), random.randint(2, 8)
        pay = rate * basic + rate * Decimal("1.5") * extra
        return _tb("%s is paid £%s an hour for the first %d hours a week and time-and-a-half after that. One week %s work %d hours. How "
                   "much do they earn, in pounds?" % (who, _money(rate), basic, "they", basic + extra), _ds(pay), "num", {"unit": "£"},
                   ["%d × £%s = £%s." % (basic, _money(rate), _money(rate * basic)),
                    "%d × £%s = £%s." % (extra, _money(rate * Decimal("1.5")), _money(rate * Decimal("1.5") * extra)), "Total £%s." % _money(pay)])

    def t_monthly():
        year = random.randint(18, 45) * 1200
        return _tb("A salary is £%s a year. How much is that per month, in pounds?" % _c(year), year // 12, "int", {"unit": "£"},
                   ["%s ÷ 12 = %s." % (_c(year), _c(year // 12))])

    def t_tax():
        allowance = 12570
        pay = random.randint(14, 50) * 1000
        tax = (Decimal(pay - allowance) * Decimal("0.2"))
        return _tb("In this example, the first £12,570 of a year's pay is tax-free and the rest is taxed at 20%%. %s earns £%s a year. How much "
                   "tax do they pay, in pounds?" % (who, _c(pay)), _ds(tax), "num", {"unit": "£"},
                   ["Taxable pay: £%s − £12,570 = £%s." % (_c(pay), _c(pay - allowance)), "20%% of that = £%s." % _money(tax)])

    def t_bill():
        days, stand = random.randint(28, 31), pick([50, 45, 60])
        units, price = random.randint(100, 400), pick([24, 25, 28, 30])
        total = Decimal(days * stand + units * price) / 100
        return _tb("An electricity bill has a standing charge of %dp a day plus %dp for each unit. In %d days a home uses %d units. What is the "
                   "bill, in pounds?" % (stand, price, days, units), _ds(total), "num", {"unit": "£"},
                   ["%d × %dp = %dp." % (days, stand, days * stand), "%d × %dp = %dp." % (units, price, units * price), "Total £%s." % _money(total)])

    def t_best_buy():
        g1, g2 = pick([(200, 500), (250, 400), (300, 750), (400, 1000), (500, 800)])
        u1 = random.randint(15, 40) * 2
        u2 = u1 + pick([-6, -4, 4, 6])
        p1, p2 = Decimal(u1 * g1) / 10000, Decimal(u2 * g2) / 10000
        return _tb("Cereal: %d g for £%s, or %d g for £%s. What is the price per 100 g of the BETTER buy, in pence?" % (g1, _money(p1), g2, _money(p2)),
                   min(u1, u2), "int", {"unit": "p"}, ["Per 100 g: %dp and %dp." % (u1, u2), "The cheaper per 100 g is %dp." % min(u1, u2)])

    def t_statement():
        bal = random.randint(700, 1500)
        moves = [("Wages", random.randint(300, 900)), ("Rent", -random.randint(200, 500)), ("Shopping", -random.randint(20, 120)),
                 ("Refund", random.randint(5, 40))]
        random.shuffle(moves)
        rows, b = [], bal
        rows.append(["Start", "", _c(bal)])
        for lab, amt in moves:
            b += amt
            rows.append([lab, ("+" if amt > 0 else "−") + _c(abs(amt)), _c(b)])
        i = random.randint(1, 4)
        return _dt("Complete the bank statement (in pounds).", ["Item", "Money in/out", "Balance"], rows, int(rows[i][2].replace(",", "")),
                   ["Each balance = the one above + money in − money out."], missing=[i, 2])

    def t_contract():
        up, monthly, months = random.randint(0, 20) * 10, random.randint(15, 45), pick([12, 18, 24])
        return _tb("A phone contract costs £%d up front and £%d a month for %d months. What is the total cost, in pounds?" % (up, monthly, months),
                   up + monthly * months, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (up, monthly, months, up + monthly * months)])

    def t_credit():
        cash = random.randint(30, 90) * 10
        dep, m, n = cash // 10, random.randint(5, 15) * 5, pick([12, 24])
        return _tb("A sofa costs £%d cash, or £%d deposit plus %d payments of £%d. How much MORE does paying in instalments cost, in pounds?"
                   % (cash, dep, n, m), dep + n * m - cash, "int", {"unit": "£"},
                   ["%d + %d × %d = %d." % (dep, n, m, dep + n * m), "%d − %d = %d." % (dep + n * m, cash, dep + n * m - cash)]) \
            if dep + n * m > cash else t_contract()

    def t_vat():
        price = random.randint(5, 80) * 5
        return _tb("A price is £%d before VAT at 20%%. What is the price including VAT, in pounds?" % price, price * 6 // 5, "int", {"unit": "£"},
                   ["%d × 1.2 = %d." % (price, price * 6 // 5)])

    def t_payslip():
        gross = random.randint(15, 35) * 100
        tax, ni, pen = gross * 20 // 100 - random.randint(1, 9) * 10, gross * 8 // 100, gross * 5 // 100
        rows = [["Gross pay", _c(gross)], ["Income tax", _c(tax)], ["National Insurance", _c(ni)], ["Pension", _c(pen)], ["Net pay", ""]]
        return _dt("A monthly payslip (in pounds). What is the net pay (gross pay minus all deductions)?", ["", "£"], rows, gross - tax - ni - pen,
                   ["%s − %s − %s − %s = %s." % (_c(gross), _c(tax), _c(ni), _c(pen), _c(gross - tax - ni - pen))], missing=[4, 1])

    def t_discount():
        price = random.randint(2, 15) * 20
        pct, cash = pick([10, 20, 25]), random.randint(2, 8) * 5
        a, b = price * (100 - pct) // 100, price - cash
        if a == b:
            cash += 5
            b = price - cash
        return _tb("A £%d coat is on offer: %d%% off in shop A, or £%d off in shop B. What is the lower price, in pounds?" % (price, pct, cash),
                   min(a, b), "int", {"unit": "£"}, ["Shop A: £%d. Shop B: £%d." % (a, b)])

    def t_hourly():
        rate = Decimal(random.randint(22, 40)) / 2
        hrs = random.randint(15, 40)
        return _tb("%s earned £%s for working %d hours. What is the hourly rate of pay, in pounds?" % (who, _money(rate * hrs), hrs), _ds(rate), "num",
                   {"unit": "£"}, ["£%s ÷ %d = £%s." % (_money(rate * hrs), hrs, _money(rate))])

    def t_saving():
        target, per = random.randint(20, 90) * 10, random.randint(3, 12) * 5
        return _tb("%s wants to save £%d for a bike and saves £%d each week. How many weeks until they have enough?" % (who, target, per),
                   -(-target // per), "int", {"unit": "weeks"}, ["%d ÷ %d = %s, so %d weeks." % (target, per, _ds(Fraction(target, per)) if
                                                                Fraction(target, per).denominator in (1, 2, 4, 5, 10) else "%.2f…" % (target / per), -(-target // per))])

    def t_split():
        bill, people = random.randint(8, 30) * 6, pick([3, 4, 6])
        tip = pick([10, 12, 15])
        total = Decimal(bill) * (100 + tip) / 100
        share = (total / people).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
        return _tb("A meal costs £%d. A %d%% service charge is added and the total is shared equally by %d people. How much does each pay, to the "
                   "nearest penny?" % (bill, tip, people), _ds(share), "num", {"unit": "£"},
                   ["£%d × %s = £%s." % (bill, _ds(Decimal(100 + tip) / 100), _money(total)), "÷ %d = £%s." % (people, _money(share))])

    def t_budget():
        income = random.randint(12, 30) * 100
        rent, food, bills = income * pick([30, 35, 40]) // 100, random.randint(20, 50) * 5, random.randint(10, 30) * 5
        return _tb("A monthly income is £%s. Rent is £%s, food £%d and bills £%d. How much is left, in pounds?" % (_c(income), _c(rent), food, bills),
                   income - rent - food - bills, "int", {"unit": "£"}, ["%s − %s − %d − %d = %s." % (_c(income), _c(rent), food, bills,
                                                                                                   _c(income - rent - food - bills))])

    # easy: one or two whole-pound steps; hard: overtime, tax, bills, unit pricing and percentages with pennies
    return _pick_t(_by(d, [t_monthly, t_contract, t_vat, t_discount, t_hourly, t_budget],
                       [t_overtime, t_monthly, t_tax, t_bill, t_best_buy, t_contract, t_credit, t_vat, t_discount, t_hourly, t_saving, t_split, t_budget],
                       [t_overtime, t_tax, t_bill, t_best_buy, t_credit, t_saving, t_split]),
                   _by(d, [t_statement], [t_statement, t_payslip], [t_statement, t_payslip]))


# ================================================================== 9.6 ======
@skill("Y9.6.g", "Angle reasoning with algebra", S6)
def _(d=1):
    d = _d(d)

    def _equal_pair():
        while True:
            x = random.randint(5, 25)
            a, c = random.sample(range(2, 8), 2)
            if a < c:
                a, c = c, a
            b = random.randint(-10, 20)
            if 0 < a * x + b < 180:
                break
        e = (a - c) * x + b
        return a, b, c, e, x

    def t_corresponding():
        a, b, c, e, x = _equal_pair()
        return _tb("Two corresponding angles on parallel lines are (%s)° and (%s)°. Find x." % (_ex(a, b), _ex(c, e)), x, "int", {},
                   ["Corresponding angles are equal: %s = %s." % (_ex(a, b), _ex(c, e)), "%sx = %d, so x = %d." % ("" if a - c == 1 else a - c, e - b, x)])

    def t_alternate_size():
        a, b, c, e, x = _equal_pair()
        ang = a * x + b
        if not 0 < ang < 180:
            return t_corresponding()
        return _tb("Two alternate angles on parallel lines are (%s)° and (%s)°. How big is each angle?" % (_ex(a, b), _ex(c, e)), ang, "int", {"unit": "°"},
                   ["Alternate angles are equal: %s = %s, so x = %d." % (_ex(a, b), _ex(c, e), x), "Each angle is %d × %d%s = %d°." % (
                       a, x, (" + %d" % b) if b > 0 else (" − %d" % -b) if b < 0 else "", ang)])

    def t_co_interior():
        while True:
            x = random.randint(10, 40)
            a, c = random.randint(1, 4), random.randint(1, 4)
            b = random.randint(-10, 30)
            e = 180 - (a + c) * x - b
            if 0 < a * x + b < 180 and 0 < c * x + e < 180:
                break
        return _tb("Two co-interior angles between parallel lines are (%s)° and (%s)°. Find x." % (_ex(a, b), _ex(c, e)), x, "int", {},
                   ["Co-interior angles add to 180°: %dx %s = 180." % (a + c, "" if b + e == 0 else ("+ %d" % (b + e) if b + e > 0 else "− %d" % -(b + e))),
                    "x = %d." % x])

    def t_exterior():
        x = random.randint(10, 30)
        a, c = random.randint(1, 3), random.randint(1, 3)
        b, e = random.randint(0, 20), random.randint(0, 20)
        ext = (a + c) * x + b + e
        if ext >= 180:
            return t_co_interior()
        return _tb("In a triangle, two interior angles are (%s)° and (%s)°. The exterior angle at the third corner is %d°. Find x." % (_ex(a, b), _ex(c, e), ext),
                   x, "int", {}, ["Exterior angle = sum of the two opposite interior angles: %dx + %d = %d." % (a + c, b + e, ext), "x = %d." % x])

    def t_pentagon():
        n, total = pick([(5, 540), (6, 720)])
        ks = [random.randint(1, 3) for _ in range(n)]
        x = random.randint(20, 60)
        cs = [random.randint(-10, 30) for _ in range(n - 1)]
        cs.append(total - sum(ks) * x - sum(cs))
        if any(k * x + c <= 0 or k * x + c >= 360 for k, c in zip(ks, cs)):
            return t_co_interior()
        name = {5: "pentagon", 6: "hexagon"}[n]
        return _tb("The interior angles of a %s are %s (all in degrees). Find x." % (name, ", ".join(_ex(k, c) for k, c in zip(ks, cs))), x, "int", {},
                   ["Angles in a %s add to %d°." % (name, total), "%dx %s = %d, x = %d." % (sum(ks), "+ %d" % sum(cs) if sum(cs) >= 0 else "− %d" % -sum(cs), total, x)])

    def t_regular_ratio():
        k = pick([2, 3, 4, 5])
        n = 2 * (k + 1)
        return _tb("Each interior angle of a regular polygon is %d times each exterior angle. How many sides does it have?" % k, n, "int", {},
                   ["Interior + exterior = 180, so %d × exterior = 180 and exterior = %s." % (k + 1, _ds(Fraction(180, k + 1))),
                    "Sides = 360 ÷ %s = %d." % (_ds(Fraction(180, k + 1)), n)])

    def t_parallelogram():
        a, b, c, e, x = _equal_pair()
        ang = a * x + b
        if not 0 < ang < 180:
            return t_corresponding()
        return _tb("Opposite angles of a parallelogram are (%s)° and (%s)°. What is the size of one of the OTHER two angles?" % (_ex(a, b), _ex(c, e)),
                   180 - ang, "int", {"unit": "°"}, ["Opposite angles are equal: x = %d, so they are %d°." % (x, ang), "Neighbouring angles add to 180°: %d°." % (180 - ang)])

    def t_point():
        x = random.randint(10, 40)
        ks = [random.randint(1, 4) for _ in range(3)]
        cs = [random.randint(0, 20) for _ in range(2)]
        cs.append(360 - sum(ks) * x - sum(cs))
        if not 0 < ks[2] * x + cs[2] < 180 or not -20 <= cs[2] <= 120:
            return t_exterior()
        return _tb("Three angles meet at a point: %s. Find x." % ", ".join("(%s)°" % _ex(k, c) for k, c in zip(ks, cs)), x, "int", {},
                   ["Angles around a point add to 360°.", "%dx %s = 360, x = %d." % (sum(ks), "+ %d" % sum(cs) if sum(cs) >= 0 else "− %d" % -sum(cs), x)])

    def t_isos():
        x = random.randint(20, 70)
        apex = 180 - 2 * x
        if apex <= 0:
            return t_point()
        return _tb("An isosceles triangle has base angles of x° each and an apex angle of %d°. Find x." % apex, x, "int", {},
                   ["2x + %d = 180." % apex, "x = %d." % x])

    def t_polygon_n():
        n = pick([5, 6, 8, 9, 10, 12])
        tot = (n - 2) * 180
        return _tb("The interior angles of a polygon add up to %s°. How many sides does it have?" % _c(tot), n, "int", {},
                   ["(n − 2) × 180 = %d, so n − 2 = %d." % (tot, n - 2), "n = %d." % n])

    # easy: one angle fact gives one equation for x; hard: find x then the angle, polygons with five or six expressions, regular-polygon ratios
    return _pick_t(_by(d, [t_corresponding, t_co_interior, t_exterior, t_isos, t_polygon_n],
                       [t_corresponding, t_alternate_size, t_co_interior, t_exterior, t_pentagon, t_regular_ratio, t_parallelogram, t_point, t_isos,
                        t_polygon_n],
                       [t_alternate_size, t_pentagon, t_regular_ratio, t_parallelogram, t_point]))


# ================================================================== 9.8 ======
@skill("Y9.8.e", "Systematic listing, counting outcomes and tree diagrams", S8)
def _(d=1):
    d = _d(d)
    r, b = random.randint(2, 7), random.randint(2, 7)
    n = r + b

    def t_with_rep():
        return _fq("A bag has %d red and %d blue counters. A counter is taken, put back, then another is taken. Use a tree diagram: what is "
                   "P(both red)? (simplest form)" % (r, b), Fraction(r, n) ** 2, ["%d/%d × %d/%d = %s." % (r, n, r, n, _fs(Fraction(r, n) ** 2))])

    def t_without():
        return _fq("A bag has %d red and %d blue counters. Two are taken WITHOUT putting the first back. What is P(both red)? (simplest form)" % (r, b),
                   Fraction(r, n) * Fraction(r - 1, n - 1), ["%d/%d × %d/%d = %s." % (r, n, r - 1, n - 1, _fs(Fraction(r, n) * Fraction(r - 1, n - 1)))])

    def t_one_each():
        p = Fraction(r, n) * Fraction(b, n) * 2
        return _fq("A bag has %d red and %d blue counters. A counter is taken, put back, then another is taken. What is P(one of each colour)? "
                   "(simplest form)" % (r, b), p, ["RB or BR: 2 × %d/%d × %d/%d = %s." % (r, n, b, n, _fs(p))])

    def t_at_least():
        p = pick([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 5)])
        return _fq("The probability a bus is late is %s each day, independently. Over two days, what is P(late at least once)? (simplest form)" % _fs(p),
                   1 - (1 - p) ** 2, ["P(never late) = %s × %s = %s." % (_fs(1 - p), _fs(1 - p), _fs((1 - p) ** 2)), "1 − %s = %s." % (_fs((1 - p) ** 2), _fs(1 - (1 - p) ** 2))])

    def t_tree_table():
        p, q = Fraction(random.randint(1, 9), 10), Fraction(random.randint(1, 9), 10)
        rows = [["Win, Win", _ds(p * q)], ["Win, Lose", _ds(p * (1 - q))], ["Lose, Win", _ds((1 - p) * q)], ["Lose, Lose", _ds((1 - p) * (1 - q))]]
        i = random.randrange(4)
        return _dt("A player wins the first game with probability %s and the second with probability %s, independently. The table lists the "
                   "ends of the tree diagram. Fill in the gap." % (_ds(p), _ds(q)), ["Outcome", "Probability"], rows, rows[i][1],
                   ["Multiply along the branches.", "%s." % rows[i][1]], missing=[i, 1], atype="num")

    def t_digits():
        k = pick([3, 4])
        digits = random.sample(range(1, 10), k)
        return _tb("How many different two-digit numbers can be made from the digits %s, using each digit at most once?" % ", ".join(map(str, digits)),
                   k * (k - 1), "int", {}, ["%d choices for the tens digit, then %d for the units: %d × %d = %d." % (k, k - 1, k, k - 1, k * (k - 1))])

    def t_arrange():
        k = pick(_by(d, [3, 4], [3, 4, 5], [4, 5]))
        word = pick({3: ["CAT", "SUN", "BOX"], 4: ["MATH", "FISH", "CLAY"], 5: ["PLANT", "CHAIR", "MOUSE"]}[k])
        f = 1
        for v in range(2, k + 1):
            f *= v
        return _tb("In how many different orders can the letters of %s be arranged?" % word, f, "int", {},
                   [" × ".join(str(v) for v in range(k, 0, -1)) + " = %d." % f])

    def t_pairs():
        k = random.randint(4, 8)
        return _tb("%d friends each shake hands once with every other friend. How many handshakes are there?" % k, k * (k - 1) // 2, "int", {},
                   ["List them systematically: %s = %d." % (" + ".join(str(v) for v in range(k - 1, 0, -1)), k * (k - 1) // 2)])

    def t_codes():
        letters, digits = random.randint(2, 5), pick([5, 10])
        return _tb("A code is one letter from %s followed by one digit from %s. How many different codes are there?" % (
                   ", ".join("ABCDE"[:letters]), "0 to 9" if digits == 10 else "1 to 5"), letters * digits, "int", {},
                   ["%d × %d = %d." % (letters, digits, letters * digits)])

    def t_listed_prob():
        digits = random.sample(range(1, 10), 3)
        nums = [10 * a + bb for a in digits for bb in digits if a != bb]
        even = sum(1 for v in nums if v % 2 == 0)
        return _fq("Two-digit numbers are made from %s, using each digit at most once. One is chosen at random. What is P(it is even)? (simplest form)"
                   % ", ".join(map(str, digits)), Fraction(even, len(nums)),
                   ["List them: %s." % ", ".join(map(str, nums)), "%d of %d are even." % (even, len(nums))])

    def t_menu():
        s, m = random.randint(2, 4), random.randint(2, 5)
        return _tb("A café offers %d sandwiches and %d drinks. How many different sandwich-and-drink combinations are there?" % (s, m), s * m, "int", {},
                   ["List them in a grid: %d × %d = %d." % (s, m, s * m)])

    # easy: product rule for two choices, one branch of a tree with replacement; hard: without replacement, either order, 'at least', listing
    return _pick_t(_by(d, [t_with_rep, t_digits, t_arrange, t_codes, t_menu],
                       [t_with_rep, t_without, t_one_each, t_at_least, t_digits, t_arrange, t_pairs, t_codes, t_listed_prob, t_menu],
                       [t_without, t_one_each, t_at_least, t_arrange, t_pairs, t_listed_prob]), [t_tree_table])


# ================================================================== 9.9 ======
_GCHART = [("Time (min)", "times, in minutes", 0, 10), ("Height (cm)", "heights, in cm", 140, 5), ("Mass (kg)", "masses, in kg", 40, 5),
           ("Score", "test scores", 0, 20)]


@skill("Y9.9.e", "Charts for grouped numerical data", S9)
def _(d=1):
    d = _d(d)
    head, desc, base, w = pick(_GCHART)
    k = pick(_by(d, [4], [4, 5], [5]))
    groups = [(base + i * w, base + (i + 1) * w) for i in range(k)]
    f = [random.randint(1, 16) for _ in groups]
    cats = ["%d–%d" % g for g in groups]

    def t_read():
        # a frequency polygon plots each class at its midpoint
        i = random.randrange(k)
        mid = Fraction(groups[i][0] + groups[i][1], 2)
        return _bar("The bar chart shows grouped %s. A frequency polygon is drawn from it. At what value on the horizontal axis "
                    "is the point for the class %s plotted?" % (desc, cats[i]), cats, f, _ds(mid),
                    ["A frequency polygon plots each class at its midpoint.",
                     "(%d + %d) ÷ 2 = %s, at a height of %d." % (groups[i][0], groups[i][1], _ds(mid), f[i])], atype="num")

    def t_total():
        # an estimated mean straight from the chart, using midpoints
        mids = [Fraction(a + b, 2) for a, b in groups]
        T = sum(mp * x for mp, x in zip(mids, f))
        m = round(float(T / sum(f)) + 1e-12, 1)
        q = _bar("The bar chart shows grouped %s. Use the midpoints to estimate the mean, to 1 decimal place." % desc, cats, f, m,
                 ["Σ(midpoint × f) = %s = %s." % (" + ".join("%s×%d" % (_ds(mp), x) for mp, x in zip(mids, f)), _ds(T)),
                  "Σf = %d, so the estimated mean is %s ÷ %d ≈ %s." % (sum(f), _ds(T), sum(f), m)], atype="num")
        q["tolerance"] = 0.051
        return q

    def t_above():
        i = random.randint(1, k - 1)
        return _bar("The bar chart shows grouped %s (each bar includes its upper value). How many values are more than %d?" % (desc, groups[i][0]), cats, f, sum(f[i:]),
                    ["Add the bars from %s up: %d." % (cats[i], sum(f[i:]))])

    def t_modal():
        if f.count(max(f)) > 1:
            f[f.index(max(f))] += 1          # one clear modal class
        return _bar("The bar chart shows grouped %s. Type the lower end of the modal class." % desc, cats, f, groups[f.index(max(f))][0],
                    ["The tallest bar is %s." % cats[f.index(max(f))]])

    def t_width():
        return _bar("The bar chart shows grouped %s. What is the class width?" % desc, cats, f, w, ["%d − %d = %d." % (groups[0][1], groups[0][0], w)])

    def t_difference():
        # the class that holds the median, read from the bars (an odd total, so there is one middle value)
        if sum(f) % 2 == 0:
            f[-1] += 1
        n = sum(f)
        pos, cum = (n + 1) // 2, 0
        for i, x in enumerate(f):
            cum += x
            if cum >= pos:
                break
        return _bar("The bar chart shows grouped %s. Which class contains the median? Type its lower end." % desc, cats, f,
                    groups[i][0], ["There are %d values, so the median is the %s value." % (n, ordinal(pos)),
                                   "Adding the bars from the left, the %s value is in %s." % (ordinal(pos), cats[i])])

    def t_percent():
        tot = sum(f)
        i = random.randrange(k)
        pc = Fraction(100 * f[i], tot)
        for _ in range(500):                   # a total that gives a percentage with at most two decimal places
            if pc.denominator in (1, 2, 4, 5, 10, 20, 25, 50):
                break
            f[:] = [random.randint(1, 16) for _ in groups]
            tot = sum(f)
            pc = Fraction(100 * f[i], tot)
        return _bar("The bar chart shows grouped %s. What percentage of the values are in %s?" % (desc, cats[i]), cats, f, _ds(pc),
                    ["%d out of %d = %s%%." % (f[i], tot, _ds(pc))], atype="num")

    def t_tally():
        g = random.randrange(k)
        raw = [random.randint(groups[0][0] + 1, groups[-1][1]) for _ in range(random.randint(12, 18))]
        cnt = sum(1 for v in raw if groups[g][0] < v <= groups[g][1])
        return _tb("Here are some %s: %s. How many go in the class %d < x ≤ %d?" % (desc, ", ".join(map(str, raw)), groups[g][0], groups[g][1]), cnt,
                   "int", {}, ["Count values above %d and up to and including %d: %d." % (groups[g][0], groups[g][1], cnt)])

    def t_boundary():
        g = random.randint(1, min(2, k - 1))
        v = groups[g][0]
        return _tb("Classes are %s. A value of exactly %d goes in the class that starts at which number?" % (
                   ", ".join("%d < x ≤ %d" % gg for gg in groups[:3]), v), groups[g - 1][0], "int", {},
                   ["%d < x ≤ %d includes %d, because of the ≤." % (groups[g - 1][0], v, v)]) if g <= 2 else t_read()

    def t_line_chart():
        vals = [0, 1, 2, 3, 4, 5]
        ff = [random.randint(1, 10) for _ in vals]
        tot = sum(v * x for v, x in zip(vals, ff))
        m = Fraction(tot, sum(ff))
        while m.denominator not in (1, 2, 4, 5, 10):
            ff = [random.randint(1, 10) for _ in vals]
            tot = sum(v * x for v, x in zip(vals, ff))
            m = Fraction(tot, sum(ff))
        return _bar("The bar chart shows how many goals a team scored per match. What is the mean number of goals?", [str(v) for v in vals], ff,
                    _ds(m), ["Total goals %d in %d matches." % (tot, sum(ff)), "%d ÷ %d = %s." % (tot, sum(ff), _ds(m))], atype="num")

    def t_pie():
        kk = 4
        ff = random.sample([3, 6, 9, 12, 15, 18, 24, 27, 30], kk)
        tot = sum(ff)
        while 360 % tot:
            ff = random.sample([3, 6, 9, 12, 15, 18, 24, 27, 30], kk)
            tot = sum(ff)
        i = random.randrange(kk)
        return {"prompt": "The pie chart shows %d grouped %s. The %s sector is %d°. How many values are in that class?" % (tot, desc, cats[i], ff[i] * 360 // tot),
                "component": "pie_chart", "spec": {"slices": [[c, x] for c, x in zip(cats, ff)], "mode": "read", "highlight": i},
                "answer": ff[i], "answer_type": "int", "solution": ["%d/360 × %d = %d." % (ff[i] * 360 // tot, tot, ff[i])]}

    # easy: read one bar, add the bars, modal class, class width; hard: cumulative counts, percentages, means, pie sectors, class boundaries
    return _pick_t(_by(d, [t_tally], [t_tally, t_boundary], [t_tally, t_boundary]),
                   _by(d, [t_read, t_total, t_modal, t_width, t_difference],
                       [t_read, t_total, t_above, t_modal, t_width, t_difference, t_percent, t_line_chart, t_pie],
                       [t_above, t_difference, t_percent, t_line_chart, t_pie]))
