# Year 7 generators: strands 7.2 and 7.3.
#
# Equality and equivalence: one- and two-step equations, forming equations, collecting like terms,
# equivalence and the ≡ idea, expanding a single bracket.  Place value and ordering: integers and
# decimals of any size, ordering with =, ≠, <, >, ≤, ≥, intervals on number lines, rounding to decimal
# places and to 1 significant figure, ranges and medians of lists.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S2 = "7.2 Equality & equivalence"
S3 = "7.3 Place value & ordering"


def _sgn(c):
    return "+ %d" % c if c >= 0 else "− %d" % -c


# ================================================================== 7.2 ======
@skill("Y7.2.a", "Solve one-step equations", S2)
def _(d=1):
    d = _d(d)
    x = random.randint(_by(d, 1, -10, -20), _by(d, 20, 30, 50))
    k = random.randint(2, _by(d, 9, 12, 15))
    c = random.randint(1, _by(d, 20, 40, 90))

    def t_add():
        return _tb("Solve  x + %d = %d" % (c, x + c), x, "int", {}, ["Subtract %d from both sides: x = %d." % (c, x)])

    def t_sub():
        return _tb("Solve  x − %d = %d" % (c, x - c), x, "int", {}, ["Add %d to both sides: x = %d." % (c, x)])

    def t_mult():
        return _tb("Solve  %dx = %d" % (k, k * x), x, "int", {}, ["Divide both sides by %d: x = %d." % (k, x)])

    def t_div():
        return _tb("Solve  x ÷ %d = %d" % (k, x), k * x, "int", {}, ["Multiply both sides by %d: x = %d." % (k, k * x)])

    def t_word():
        who = _who()
        return _tb("%s thinks of a number and multiplies it by %d. The answer is %d. What was the number?"
                   % (who, k, k * x), x, "int", {}, ["%dx = %d, so x = %d." % (k, k * x, x)])

    def t_bar():
        if x <= 0:
            return t_mult()
        return _strip("The bar model shows %dx = %d. What is x?" % (k, k * x),
                      {"mode": "equal_parts", "parts": k, "partLabel": "x", "totalLabel": str(k * x), "unknown": "part"},
                      x, ["%d ÷ %d = %d." % (k * x, k, x)])

    return _pick_t([t_add, t_sub, t_mult, t_div, t_word], [t_bar])


@skill("Y7.2.b", "Solve two-step equations", S2)
def _(d=1):
    d = _d(d)
    x = random.randint(_by(d, 1, -6, -12), _by(d, 12, 15, 20))
    k = random.randint(2, _by(d, 6, 9, 12))
    c = random.randint(_by(d, 1, -15, -30), _by(d, 15, 20, 40))
    if c == 0:
        c = 5

    def t_plain():
        return _tb("Solve  %dx %s = %d" % (k, _sgn(c), k * x + c), x, "int", {},
                   ["%s both sides: %dx = %d." % ("Subtract %d from" % c if c > 0 else "Add %d to" % -c, k, k * x),
                    "x = %d." % x])

    def t_think():
        who = _who()
        return _tb("%s thinks of a number, multiplies it by %d and then %s %d. The answer is %d. What was the number?"
                   % (who, k, "adds" if c > 0 else "subtracts", abs(c), k * x + c), x, "int", {},
                   ["Undo in reverse: %s %d, then ÷ %d." % ("− " if c > 0 else "+ ", abs(c), k), "x = %d." % x])

    def t_divided():
        y = random.randint(1, 10)
        return _tb("Solve  x/%d %s = %d" % (k, _sgn(c), y + c), k * y, "int", {},
                   ["x/%d = %d." % (k, y), "x = %d." % (k * y)])

    def t_bracket():
        return _tb("Solve  %d(x %s) = %d" % (k, _sgn(c), k * (x + c)), x, "int", {},
                   ["Divide by %d: x %s = %d." % (k, _sgn(c), x + c), "x = %d." % x])

    def t_cost():
        fee, per = random.randint(5, 20), random.randint(2, 9)
        n = random.randint(2, 12)
        return _tb("A gym charges a £%d joining fee plus £%d a visit. %s paid £%d in total. Form and solve an equation: "
                   "how many visits?" % (fee, per, _who(), fee + per * n), n, "int", {"unit": "visits"},
                   ["%d + %dv = %d." % (fee, per, fee + per * n), "v = %d." % n])

    def t_check():
        shown = x + pick([0, 0, 1, -1])
        return _wq("Is x = %d a solution of  %dx %s = %d ? (yes or no)" % (shown, k, _sgn(c), k * x + c),
                   "yes" if shown == x else "no",
                   ["%d × %d %s = %d." % (k, shown, _sgn(c), k * shown + c)], "yes / no")

    return _pick_t([t_plain, t_think, t_divided, t_bracket, t_cost, t_check])


@skill("Y7.2.c", "Form equations from problems", S2)
def _(d=1):
    d = _d(d)

    def t_perimeter():
        x = random.randint(2, 15)
        a = random.randint(1, 9)
        return _tb("A rectangle has sides x cm and (x + %d) cm. Its perimeter is %d cm. What is x?" % (a, 4 * x + 2 * a),
                   x, "int", {"unit": "cm"}, ["2x + 2(x + %d) = 4x + %d = %d." % (a, 2 * a, 4 * x + 2 * a), "x = %d." % x])

    def t_ages():
        x = random.randint(5, 15)
        diff = random.randint(2, 30)
        return _tb("Sam is %d years older than Kai. Together their ages add up to %d. How old is Kai?"
                   % (diff, 2 * x + diff), x, "int", {"unit": "years"},
                   ["k + (k + %d) = %d." % (diff, 2 * x + diff), "2k = %d, k = %d." % (2 * x, x)])

    def t_angles():
        x = random.randint(10, 50)
        a = 180 - 3 * x
        if a <= 0:
            return t_ages()
        return _tb("The angles of a triangle are x°, 2x° and %d°. What is x?" % a, x, "int", {"unit": "°"},
                   ["x + 2x + %d = 180." % a, "3x = %d, x = %d." % (180 - a, x)])

    def t_consecutive():
        n = random.randint(5, 40)
        return _tb("Three consecutive whole numbers add up to %d. What is the smallest?" % (3 * n + 3), n, "int", {},
                   ["n + (n + 1) + (n + 2) = 3n + 3 = %d." % (3 * n + 3), "n = %d." % n])

    def t_write():
        k, c = random.randint(2, 9), random.randint(1, 20)
        x = random.randint(2, 12)
        return _wq("I multiply a number x by %d and add %d. The answer is %d. Write the equation, like 3x+4=19."
                   % (k, c, k * x + c), "%dx+%d=%d" % (k, c, k * x + c),
                   ["%dx + %d = %d." % (k, c, k * x + c)], "e.g. 3x+4=19")

    def t_share():
        x = random.randint(3, 20)
        k = random.randint(2, 4)
        return _tb("Ana has %d times as many stickers as Ben. They have %d stickers altogether. How many does Ben have?"
                   % (k, (k + 1) * x), x, "int", {}, ["b + %db = %db = %d." % (k, k + 1, (k + 1) * x), "b = %d." % x])

    return _pick_t([t_perimeter, t_ages, t_angles, t_consecutive, t_write, t_share])


@skill("Y7.2.d", "Collect like terms", S2)
def _(d=1):
    d = _d(d)
    a, b, c, e = [random.randint(_by(d, 1, -5, -9), _by(d, 9, 12, 15)) for _ in range(4)]
    a, c = a or 2, c or 3

    def _lin(p, q, v="x"):
        s = ("" if p == 1 else "-" if p == -1 else str(p)) + v if p else ""
        if q:
            s += ("+" if q > 0 and s else "") + str(q)
        return s or "0"

    def t_one_var():
        return _wq("Simplify  %dx + %dx" % (abs(a), abs(c)), _lin(abs(a) + abs(c), 0),
                   ["%d + %d = %d." % (abs(a), abs(c), abs(a) + abs(c))], "e.g. 7x")

    def t_with_const():
        return _wq("Simplify  %s %s %s %s  (write it like 5x+3)" % (_lin(a, 0), _sgn(b),
                                                                  ("+ " + _lin(c, 0)) if c > 0 else ("− " + _lin(-c, 0)),
                                                                  _sgn(e)),
                   _lin(a + c, b + e), ["x terms: %d + %d = %d. Numbers: %d + %d = %d." % (a, c, a + c, b, e, b + e)],
                   "e.g. 5x+3")

    def t_two_vars():
        p, q, r, s2 = [random.randint(1, 9) for _ in range(4)]
        ans = "%sx+%sy" % (p + r if p + r != 1 else "", q + s2 if q + s2 != 1 else "")
        return _wq("Simplify  %dx + %dy + %dx + %dy  (like 5x+3y)" % (p, q, r, s2), ans,
                   ["x: %d + %d = %d. y: %d + %d = %d." % (p, r, p + r, q, s2, q + s2)], "e.g. 5x+3y")

    def t_subtract():
        p, r = random.randint(5, 15), random.randint(1, 4)
        return _wq("Simplify  %da − %da" % (p, r), "%da" % (p - r) if p - r != 1 else "a", ["%d − %d = %d." % (p, r, p - r)],
                   "e.g. 4a")

    def t_perimeter():
        p, q = random.randint(2, 6), random.randint(1, 9)
        return _wq("A rectangle has sides %dx and %d. Write a simplified expression for its perimeter (like 6x+10)."
                   % (p, q), "%dx+%d" % (2 * p, 2 * q), ["2 × %dx + 2 × %d = %dx + %d." % (p, q, 2 * p, 2 * q)],
                   "e.g. 6x+10")

    def t_evaluate():
        x = random.randint(2, 9)
        p, q = random.randint(2, 6), random.randint(2, 6)
        return _tb("Simplify  %dx + %dx  and then find its value when x = %d." % (p, q, x), (p + q) * x, "int", {},
                   ["%dx; %d × %d = %d." % (p + q, p + q, x, (p + q) * x)])

    return _pick_t([t_one_var, t_with_const, t_two_vars, t_subtract, t_perimeter, t_evaluate])


@skill("Y7.2.e", "Equivalence and expanding a single bracket", S2)
def _(d=1):
    d = _d(d)
    k = random.randint(2, 9)
    c = random.randint(1, 12)

    def t_expand():
        return _wq("Expand  %d(x + %d)  (like 3x+12)" % (k, c), "%dx+%d" % (k, k * c), ["%d × x + %d × %d." % (k, k, c)],
                   "e.g. 3x+12")

    def t_expand_minus():
        return _wq("Expand  %d(y − %d)  (like 3y-12)" % (k, c), "%dy-%d" % (k, k * c), ["%d × y − %d × %d." % (k, k, c)],
                   "e.g. 3y-12")

    def t_which():
        good = "%dx+%d" % (k, k * c)
        bad = "%dx+%d" % (k, c)
        opts = [good, bad]
        random.shuffle(opts)
        return _wq("Which expression is equivalent to %d(x + %d):  %s  or  %s ? Type it." % (k, c, opts[0], opts[1]),
                   good, ["Multiply BOTH terms in the bracket by %d." % k], "e.g. 3x+12")

    def t_true():
        stmt, ans = pick([("2(a + 4) ≡ 2a + 8", "true"), ("3(b − 2) ≡ 3b − 2", "false"), ("a + a + a ≡ 3a", "true"),
                          ("x × x ≡ 2x", "false"), ("4(c + 1) ≡ 4c + 4", "true"), ("5(d − 3) ≡ 5d − 15", "true")])
        return _wq("True or false: %s for every value of the letter?" % stmt, ans,
                   ["≡ means 'is identical to' for all values."], "true / false")

    def t_missing():
        return _tb("Complete:  %d(x + ___) ≡ %dx + %d" % (k, k, k * c), c, "int", {}, ["%d ÷ %d = %d." % (k * c, k, c)])

    def t_area():
        return _wq("A rectangle is %d cm by (x + %d) cm. Write its area as an expanded expression (like 3x+12)." % (k, c),
                   "%dx+%d" % (k, k * c), ["%d(x + %d) = %dx + %d." % (k, c, k, k * c)], "e.g. 3x+12")

    return _pick_t([t_expand, t_expand_minus, t_which, t_true, t_missing, t_area])


# ================================================================== 7.3 ======
@skill("Y7.3.a", "Place value in integers and decimals of any size", S3)
def _(d=1):
    d = _d(d)

    def t_value_big():
        n = random.randint(10_000_000, 999_999_999)
        s = str(n)
        i = random.randint(0, 3)
        place = 10 ** (len(s) - 1 - i)
        return _tb("What is the value of the digit %s in %s?" % (s[i], _c(n)), int(s[i]) * place, "int", {},
                   ["It is worth %s." % _c(int(s[i]) * place)])

    def t_value_small():
        x = Decimal(random.randint(1, 99999)) / 10 ** random.randint(3, 4)
        s = format(x, "f").split(".")[1]
        i = max(k for k in range(len(s)) if s[k] != "0")
        return _tb("What is the value of the digit %s in %s? Write it as a decimal." % (s[i], _ds(x)),
                   _ds(Decimal(s[i]) / 10 ** (i + 1)), "num", {}, ["Place %d after the point." % (i + 1)])

    def t_million():
        m = random.randint(2, 99)
        k = pick([Decimal("0.5"), Decimal("1.2"), Decimal("2.75"), Decimal("3.4")])
        return _tb("Write %s million in figures." % _ds(k), int(k * 1_000_000), "int", {},
                   ["%s × 1,000,000 = %s." % (_ds(k), _c(int(k * 1_000_000)))]) if random.random() < 0.5 else \
            _tb("Write %d million in figures." % m, m * 1_000_000, "int", {}, ["%d × 1,000,000." % m])

    def t_times():
        x = Decimal(random.randint(1, 999)) / 100
        k = pick([10, 100, 1000, Decimal("0.1"), Decimal("0.01")])
        return _tb("Work out %s × %s." % (_ds(x), _ds(k)), _ds(x * k), "num", {}, ["= %s." % _ds(x * k)])

    def t_divide():
        x = Decimal(random.randint(1, 9999)) / 10
        k = pick([10, 100, 1000])
        return _tb("Work out %s ÷ %d." % (_ds(x), k), _ds(x / k), "num", {}, ["= %s." % _ds(x / k)])

    def t_units():
        x = Decimal(random.randint(1, 9999)) / 100
        a, b, f = pick([("km", "m", 1000), ("m", "cm", 100), ("kg", "g", 1000), ("cm", "mm", 10)])
        return _tb("Convert %s %s to %s." % (_ds(x), a, b), _ds(x * f), "num", {"unit": b}, ["× %d." % f])

    return _pick_t([t_value_big, t_value_small, t_million, t_times, t_divide, t_units])


@skill("Y7.3.b", "Order integers, decimals and fractions with =, ≠, <, >, ≤, ≥", S3)
def _(d=1):
    d = _d(d)

    def t_symbol():
        a, b = random.sample([Decimal(random.randint(-99, 99)) / pick([1, 10, 100]) for _ in range(4)], 2)
        if a == b:
            b = a + 1
        return _wq("Write < or > :  %s ___ %s" % (_ds(a), _ds(b)), "<" if a < b else ">",
                   ["On a number line the smaller number is further left."], "< or >")

    def t_neq():
        f, dec = pick([("1/4", "0.25"), ("1/5", "0.2"), ("3/4", "0.75"), ("2/5", "0.4"), ("1/8", "0.125")])
        wrong = pick(["0.14", "0.5", "0.35", "0.04"])
        same = random.random() < 0.5
        return _wq("Write = or ≠ :  %s ___ %s" % (f, dec if same else wrong), "=" if same else "≠",
                   ["%s = %s." % (f, dec)], "= or ≠")

    def t_order():
        vals = random.sample([Decimal(random.randint(-50, 50)) / pick([1, 10]) for _ in range(6)], 4)
        vals = list(dict.fromkeys(vals))
        if len(vals) < 4:
            return t_symbol()
        asc = sorted(vals)
        return _tb("Order these from smallest to largest. Which comes 2nd?  %s" % ", ".join(_ds(v) for v in vals),
                   _ds(asc[1]), "num", {}, ["In order: %s." % ", ".join(_ds(v) for v in asc)])

    def t_mixed():
        items = [(Fraction(1, 2), "1/2"), (Fraction(3, 5), "0.6"), (Fraction(2, 5), "40%"), (Fraction(3, 4), "3/4"),
                 (Fraction(7, 10), "0.7"), (Fraction(1, 3), "1/3"), (Fraction(13, 20), "65%")]
        pickd = random.sample(items, 4)
        big = max(pickd)[1]
        return _wq("Which is the largest?  %s" % ", ".join(p[1] for p in pickd), big,
                   ["As decimals: %s." % ", ".join(_ds(Decimal(p[0].numerator) / p[0].denominator) if p[0].denominator
                                                   in (2, 4, 5, 10, 20) else "%s ≈ %.3f" % (p[1], float(p[0]))
                                                   for p in pickd)], "as written")

    def t_inequality_int():
        lo, hi = random.randint(-8, 3), random.randint(4, 12)
        strict = pick([("<", "<"), ("≤", "<"), ("<", "≤"), ("≤", "≤")])
        vals = [n for n in range(lo - 1, hi + 2) if (n > lo if strict[0] == "<" else n >= lo) and
                (n < hi if strict[1] == "<" else n <= hi)]
        return _tb("How many whole numbers n satisfy  %d %s n %s %d ?" % (lo, strict[0], strict[1], hi), len(vals),
                   "int", {}, ["They are %s." % ", ".join(map(str, vals))])

    def t_line():
        v = Decimal(random.randint(-40, 40)) / 10
        return _nld("Place %s on the number line." % _ds(v), v, -5, 5, Decimal("0.1"), 1,
                    ["%s is between %d and %d." % (_ds(v), int(v // 1), int(v // 1) + 1)])

    return _pick_t([t_symbol, t_neq, t_order, t_mixed, t_inequality_int], [t_line])


@skill("Y7.3.c", "Round to decimal places", S3)
def _(d=1):
    d = _d(d)
    dp = random.randint(1, _by(d, 1, 2, 3))
    x = Decimal(random.randint(1, 999999)) / 10 ** random.randint(dp + 1, dp + 3)
    q = Decimal(1).scaleb(-dp)
    r = x.quantize(q, rounding="ROUND_HALF_UP")

    def t_plain():
        return _tb("Round %s to %d decimal place%s." % (_ds(x), dp, "" if dp == 1 else "s"), _ds(r), "num", {},
                   ["Look at the next digit after place %d." % dp, "%s → %s." % (_ds(x), format(r, "f"))])

    def t_money():
        p = Decimal(random.randint(10000, 999999)) / 1000
        return _tb("A calculator shows £%s. Round it to the nearest penny, in pounds." % _ds(p),
                   _ds(p.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")), "num", {"unit": "£"},
                   ["2 decimal places: £%s." % format(p.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"), "f")])

    def t_trap_nine():
        w = random.randint(1, 30)
        v = Decimal(w) + Decimal("0.9") + Decimal(random.randint(5, 9)) / 100
        r1 = v.quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        return _tb("Round %s to 1 decimal place." % _ds(v), _ds(r1), "num", {},
                   ["The 9 rounds up, carrying into the ones: %s (written %s to 1 d.p.)." % (_ds(r1), format(r1, "f"))])

    def t_between():
        lo = Decimal(random.randint(10, 99)) / 10
        return _tb("A number rounds to %s to 1 decimal place. What is the smallest it could be?" % _ds(lo),
                   _ds(lo - Decimal("0.05")), "num", {}, ["Halfway down: %s." % _ds(lo - Decimal("0.05"))])

    return _pick_t([t_plain, t_plain, t_money, t_trap_nine, t_between])


@skill("Y7.3.d", "Round to 1 significant figure and estimate", S3)
def _(d=1):
    d = _d(d)

    def _sf1(v):
        v = Decimal(v)
        e = v.adjusted()
        return v.scaleb(-e).quantize(Decimal(1), rounding="ROUND_HALF_UP").scaleb(e)

    def t_round():
        v = pick([random.randint(11, 99999), Decimal(random.randint(11, 999)) / 1000])
        r = _sf1(v)
        return _tb("Round %s to 1 significant figure." % (_c(v) if isinstance(v, int) else _ds(v)), _ds(r), "num", {},
                   ["Keep the first non-zero digit, rounding it: %s." % _ds(r)])

    def t_estimate_mult():
        a, b = random.randint(11, 99), random.randint(11, 99)
        ea, eb = _sf1(a), _sf1(b)
        return _tb("Estimate %d × %d by rounding each number to 1 significant figure." % (a, b), int(ea * eb), "int", {},
                   ["%s × %s = %s." % (_ds(ea), _ds(eb), _ds(ea * eb))])

    def t_estimate_div():
        a = random.randint(110, 990)
        b = random.randint(11, 49)
        ea, eb = _sf1(a), _sf1(b)
        if ea % eb:
            return t_estimate_mult()
        return _tb("Estimate %d ÷ %d by rounding each number to 1 significant figure." % (a, b), int(ea / eb), "int", {},
                   ["%s ÷ %s = %s." % (_ds(ea), _ds(eb), _ds(ea / eb))])

    def t_sensible():
        a, b = random.randint(21, 89), random.randint(21, 89)
        right = a * b
        wrong = right * 10
        shown = pick([right, wrong])
        return _wq("%s says %d × %d = %s. Use an estimate to decide: is it sensible? (yes or no)" % (_who(), a, b, _c(shown)),
                   "yes" if shown == right else "no",
                   ["Estimate: %s × %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(a) * _sf1(b)))], "yes / no")

    def t_decimal_est():
        a = Decimal(random.randint(21, 99)) / 10
        b = random.randint(21, 89)
        return _tb("Estimate %s × %d by rounding each number to 1 significant figure." % (_ds(a), b),
                   _ds(_sf1(a) * _sf1(b)), "num", {}, ["%s × %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(a) * _sf1(b)))])

    return _pick_t([t_round, t_round, t_estimate_mult, t_estimate_div, t_sensible, t_decimal_est])


@skill("Y7.3.e", "Range and median of a list", S3)
def _(d=1):
    d = _d(d)
    n = pick(_by(d, [5, 7], [5, 6, 7, 8], [6, 8, 9, 10]))
    vals = [random.randint(_by(d, 1, -10, -20), _by(d, 30, 50, 99)) for _ in range(n)]

    def t_range():
        return _tb("Find the range of: %s" % ", ".join(map(str, vals)), max(vals) - min(vals), "int", {},
                   ["%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))])

    def t_median():
        s = sorted(vals)
        m = Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)
        return _tb("Find the median of: %s" % ", ".join(map(str, vals)), _ds(m), "num", {},
                   ["In order: %s." % ", ".join(map(str, s)), "Median = %s." % _ds(m)])

    def t_decimal_median():
        dv = sorted(Decimal(random.randint(10, 99)) / 10 for _ in range(5))
        random.shuffle(dv)
        return _tb("Find the median of these heights in metres: %s" % ", ".join(_ds(v) for v in dv),
                   _ds(sorted(dv)[2]), "num", {"unit": "m"}, ["The middle one in order is %s." % _ds(sorted(dv)[2])])

    def t_missing_range():
        hi = max(vals)
        r = hi - min(vals)
        return _tb("A list has a range of %d and its largest value is %d. What is its smallest value?" % (r, hi), hi - r,
                   "int", {}, ["%d − %d = %d." % (hi, r, hi - r)])

    return _pick_t([t_range, t_median, t_decimal_median, t_missing_range])
