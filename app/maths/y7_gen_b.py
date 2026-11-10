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
    # positive solutions and sides: negative numbers come in strand 7.6, after equations
    x = random.randint(_by(d, 1, 2, 3), _by(d, 20, 30, 50))
    k = random.randint(2, _by(d, 9, 12, 15))
    c = random.randint(1, _by(d, 20, 40, 90))

    def t_add():
        return _tb("Solve  x + %d = %d" % (c, x + c), x, "int", {}, ["Subtract %d from both sides: x = %d." % (c, x)])

    def t_sub():
        return _tb("Solve  x − %d = %d" % (c, x), x + c, "int", {}, ["Add %d to both sides: x = %d." % (c, x + c)])

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

    def t_decimal():
        a = Decimal(random.randint(11, 99)) / 10
        b = Decimal(random.randint(11, 99)) / 10
        return _tb("Solve  x + %s = %s" % (_ds(a), _ds(a + b)), _ds(b), "num", {},
                   ["Subtract %s from both sides: x = %s." % (_ds(a), _ds(b))])

    def t_from_left():
        return _tb("Solve  %d − x = %d" % (c + x, c), x, "int", {}, ["x = %d − %d = %d." % (c + x, c, x)])

    def t_square_perim():
        s = abs(x) + 2
        return _tb("A square has perimeter %d cm. Solve 4x = %d to find the side length x, in cm." % (4 * s, 4 * s), s, "int",
                   {"unit": "cm"}, ["x = %d ÷ 4 = %d." % (4 * s, s)])

    def t_rhs():
        return _tb("Solve  %d = %dx" % (k * x, k), x, "int", {}, ["The unknown can be on either side: x = %d ÷ %d = %d." % (k * x, k, x)])

    def t_money():
        who, p = _who(), random.randint(2, 9)
        return _tb("%s buys %d pens and pays £%d. Solve %dp = %d to find the price of one pen, p, in pounds."
                   % (who, k, k * p, k, k * p), p, "int", {"unit": "£"}, ["p = %d ÷ %d = %d." % (k * p, k, p)])

    return _pick_t([t_add, t_sub, t_mult, t_div, t_word, t_decimal, t_from_left, t_square_perim, t_rhs, t_money], [t_bar])


@skill("Y7.2.b", "Solve two-step equations", S2)
def _(d=1):
    d = _d(d)
    x = random.randint(_by(d, 1, 2, 3), _by(d, 12, 15, 20))
    k = random.randint(2, _by(d, 6, 9, 12))
    c = random.randint(_by(d, 1, -15, -30), _by(d, 15, 20, 40))
    if c == 0:
        c = 5
    c = max(c, 1 - k * x)          # every number stays positive: directed numbers come in strand 7.6

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
        y = random.randint(max(1, 1 - c), max(1, 1 - c) + 9)
        return _tb("Solve  x/%d %s = %d" % (k, _sgn(c), y + c), k * y, "int", {},
                   ["x/%d = %d." % (k, y), "x = %d." % (k * y)])

    def t_bracket():
        xb = max(x, 1 - c)
        return _tb("Solve  %d(x %s) = %d" % (k, _sgn(c), k * (xb + c)), xb, "int", {},
                   ["Divide by %d: x %s = %d." % (k, _sgn(c), xb + c), "x = %d." % xb])

    def t_cost():
        fee, per = random.randint(5, 20), random.randint(2, 9)
        n = random.randint(2, 12)
        return _tb("A gym charges a £%d joining fee plus £%d a visit. %s paid £%d in total. Form and solve an equation: "
                   "how many visits?" % (fee, per, _who(), fee + per * n), n, "int", {"unit": "visits"},
                   ["%d + %dv = %d." % (fee, per, fee + per * n), "v = %d." % n])

    def t_check():
        shown = x + pick([0, 0, 1, -1 if k * (x - 1) + c >= 0 else 1])
        return _wq("Is x = %d a solution of  %dx %s = %d ? (yes or no)" % (shown, k, _sgn(c), k * x + c),
                   "yes" if shown == x else "no",
                   ["%d × %d %s = %d." % (k, shown, _sgn(c), k * shown + c)], "yes / no")

    return _pick_t([t_plain, t_think, t_divided, t_bracket, t_cost, t_check])


@skill("Y7.2.c", "Form equations from problems", S2)
def _(d=1):
    d = _d(d)

    def t_perimeter():
        x = random.randint(_by(d, 2, 2, 5), _by(d, 10, 15, 30))
        a = random.randint(1, _by(d, 5, 9, 20))
        return _tb("A rectangle has sides x cm and (x + %d) cm. Its perimeter is %d cm. What is x?" % (a, 4 * x + 2 * a),
                   x, "int", {"unit": "cm"}, ["2x + 2(x + %d) = 4x + %d = %d." % (a, 2 * a, 4 * x + 2 * a), "x = %d." % x])

    def t_ages():
        x = random.randint(5, _by(d, 12, 15, 40))
        diff = random.randint(2, _by(d, 10, 30, 30))
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
        n = random.randint(_by(d, 2, 5, 20), _by(d, 15, 40, 150))
        return _tb("Three consecutive whole numbers add up to %d. What is the smallest?" % (3 * n + 3), n, "int", {},
                   ["n + (n + 1) + (n + 2) = 3n + 3 = %d." % (3 * n + 3), "n = %d." % n])

    def t_write():
        k, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 10, 20, 50))
        x = random.randint(2, _by(d, 10, 12, 25))
        return _wq("I multiply a number x by %d and add %d. The answer is %d. Write the equation, like 3x+4=19."
                   % (k, c, k * x + c), "%dx+%d=%d" % (k, c, k * x + c),
                   ["%dx + %d = %d." % (k, c, k * x + c)], "e.g. 3x+4=19")

    def t_share():
        x = random.randint(3, _by(d, 10, 20, 40))
        k = random.randint(2, _by(d, 3, 4, 7))
        return _tb("Ana has %d times as many stickers as Ben. They have %d stickers altogether. How many does Ben have?"
                   % (k, (k + 1) * x), x, "int", {}, ["b + %db = %db = %d." % (k, k + 1, (k + 1) * x), "b = %d." % x])

    def t_line():
        x = random.randint(15, 45)
        a = random.randint(5, 40)
        if 3 * x + a >= 180:
            x = (180 - a) // 3 - 1
        b = 180 - 2 * x - a - x
        return _tb("Angles of 2x°, (x + %d)° and %d° lie on a straight line. What is x?" % (a, b), x, "int", {"unit": "°"},
                   ["2x + x + %d + %d = 180." % (a, b), "3x = %d, x = %d." % (180 - a - b, x)])

    def t_isosceles():
        x, base = random.randint(5, _by(d, 12, 20, 45)), random.randint(3, _by(d, 10, 15, 30))
        return _tb("An isosceles triangle has two sides of x cm and a base of %d cm. Its perimeter is %d cm. What is x?"
                   % (base, 2 * x + base), x, "int", {"unit": "cm"}, ["2x + %d = %d." % (base, 2 * x + base), "x = %d." % x])

    def t_pens():
        p = random.randint(15, _by(d, 40, 60, 99))
        extra = random.randint(5, 30)
        a, b = random.randint(2, _by(d, 3, 4, 6)), random.randint(1, _by(d, 2, 3, 5))
        tot = a * p + b * (p + extra)
        return _tb("A pen costs x pence and a ruler costs %d pence more than a pen. %d pens and %d ruler%s cost %d pence. What "
                   "is x?" % (extra, a, b, "" if b == 1 else "s", tot), p, "int", {"unit": "p"},
                   ["%dx + %d(x + %d) = %d." % (a, b, extra, tot), "%dx = %d, x = %d." % (a + b, tot - b * extra, p)])

    def t_think():
        n, k, c = random.randint(3, _by(d, 12, 20, 40)), random.randint(2, _by(d, 4, 5, 9)), random.randint(1, _by(d, 10, 15, 40))
        c = min(c, k * n - 1)                       # the stated answer stays positive (directed numbers are 7.6)
        return _tb("I think of a number, multiply it by %d and subtract %d. The answer is %d. What was my number?"
                   % (k, c, k * n - c), n, "int", {}, ["%dn − %d = %d." % (k, c, k * n - c), "%dn = %d, n = %d." % (k, k * n, n)])

    def t_quad():
        x = random.randint(45, 60)
        a = random.randint(5, 20)
        rest = 360 - (x + x + a + 2 * x)          # 100 to 175: every angle of the quadrilateral is under 180°
        return _tb("The four angles of a quadrilateral are x°, (x + %d)°, 2x° and %d°. What is x?" % (a, rest), x, "int",
                   {"unit": "°"}, ["4x + %d + %d = 360." % (a, rest), "4x = %d, x = %d." % (360 - a - rest, x)])

    def t_area():
        w = random.randint(3, _by(d, 6, 9, 12))
        x, c = random.randint(2, _by(d, 10, 12, 25)), random.randint(1, _by(d, 5, 6, 15))
        return _tb("A rectangle is %d cm wide and (x + %d) cm long. Its area is %d cm². What is x?" % (w, c, w * (x + c)), x,
                   "int", {"unit": "cm"}, ["%d(x + %d) = %d." % (w, c, w * (x + c)), "x + %d = %d, x = %d." % (c, x + c, x)])

    def t_bags():
        x, diff = random.randint(5, _by(d, 25, 40, 120)), random.randint(3, _by(d, 12, 20, 60))
        return _tb("Two bags hold x and (x + %d) marbles. There are %d marbles altogether. How many are in the smaller bag?"
                   % (diff, 2 * x + diff), x, "int", {"unit": "marbles"},
                   ["2x + %d = %d." % (diff, 2 * x + diff), "x = %d." % x])

    return _pick_t(_by(d, [t_ages, t_consecutive, t_write, t_share, t_isosceles, t_think, t_area, t_bags],
                       [t_perimeter, t_ages, t_angles, t_consecutive, t_write, t_share, t_line, t_isosceles, t_pens, t_think,
                        t_quad, t_area, t_bags],
                       [t_perimeter, t_angles, t_consecutive, t_share, t_line, t_pens, t_think, t_quad, t_area]))


@skill("Y7.2.d", "Collect like terms", S2)
def _(d=1):
    d = _d(d)
    a, b, c, e = [random.randint(_by(d, 1, -5, -9), _by(d, 9, 12, 15)) for _ in range(4)]
    a, c, b, e = a or 2, c or 3, b or 4, e or 5

    def _lin(p, q, v="x"):
        s = ("" if p == 1 else "-" if p == -1 else str(p)) + v if p else ""
        if q:
            s += ("+" if q > 0 and s else "") + str(q)
        return s or "0"

    def _add(p, q, v=""):
        """'5x + 8x', '-3x + 4x', '1 + (-5)': the letter kept, brackets round a negative second term."""
        f = (lambda n: _lin(n, 0, v)) if v else str
        return "%s + %s" % (f(p), ("(%s)" % f(q)) if q < 0 else f(q))

    def t_one_var():
        return _wq("Simplify  %s + %s" % (_lin(abs(a), 0), _lin(abs(c), 0)), _lin(abs(a) + abs(c), 0),
                   ["%s = %s." % (_add(abs(a), abs(c), "x"), _lin(abs(a) + abs(c), 0))], "e.g. 7x")

    def t_with_const():
        return _wq("Simplify  %s %s %s %s  (write it like 5x+3)" % (_lin(a, 0), _sgn(b),
                                                                  ("+ " + _lin(c, 0)) if c > 0 else ("− " + _lin(-c, 0)),
                                                                  _sgn(e)),
                   _lin(a + c, b + e), ["x terms: %s = %s. Numbers: %s = %d." % (_add(a, c, "x"), _lin(a + c, 0), _add(b, e), b + e)],
                   "e.g. 5x+3")

    def t_two_vars():
        p, q, r, s2 = [random.randint(1, 9) for _ in range(4)]
        ans = "%sx+%sy" % (p + r if p + r != 1 else "", q + s2 if q + s2 != 1 else "")
        return _wq("Simplify  %s + %s + %s + %s  (like 5x+3y)" % (_lin(p, 0), _lin(q, 0, "y"), _lin(r, 0), _lin(s2, 0, "y")), ans,
                   ["x: %s = %s. y: %s = %s." % (_add(p, r, "x"), _lin(p + r, 0), _add(q, s2, "y"), _lin(q + s2, 0, "y"))], "e.g. 5x+3y")

    def t_subtract():
        p, r = random.randint(5, 15), random.randint(1, 4)
        return _wq("Simplify  %da − %s" % (p, "a" if r == 1 else "%da" % r), "%da" % (p - r) if p - r != 1 else "a",
                   ["%da − %s = %s." % (p, _lin(r, 0, "a"), _lin(p - r, 0, "a"))],
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
                   ["%dx + %dx = %dx." % (p, q, p + q), "%d × %d = %d." % (p + q, x, (p + q) * x)])

    return _pick_t([t_one_var, t_with_const, t_two_vars, t_subtract, t_perimeter, t_evaluate])


@skill("Y7.2.e", "Equivalence and expanding a single bracket", S2)
def _(d=1):
    d = _d(d)
    k = random.randint(2, _by(d, 5, 9, 12))
    c = random.randint(1, _by(d, 10, 12, 20))

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
        stmt, ans = pick(_by(d, [("2(a + 4) ≡ 2a + 8", "true"), ("3(b − 2) ≡ 3b − 2", "false"), ("a + a + a ≡ 3a", "true"),
                                 ("4(c + 1) ≡ 4c + 4", "true"), ("2(x + 5) ≡ 2x + 5", "false")],
                             [("2(a + 4) ≡ 2a + 8", "true"), ("3(b − 2) ≡ 3b − 2", "false"), ("a + a + a ≡ 3a", "true"),
                              ("x × x ≡ 2x", "false"), ("4(c + 1) ≡ 4c + 4", "true"), ("5(d − 3) ≡ 5d − 15", "true")],
                             [("−2(x − 3) ≡ −2x + 6", "true"), ("3(2y + 1) ≡ 6y + 1", "false"), ("4(a − b) ≡ 4a − 4b", "true"),
                              ("2(x + y) ≡ 2x + y", "false"), ("x × x ≡ 2x", "false"), ("6(p − 2) ≡ 6p − 12", "true"),
                              ("−3(n + 2) ≡ −3n + 6", "false")]))
        return _wq("True or false: %s for every value of the letter?" % stmt, ans,
                   ["≡ means 'is identical to' for all values."], "true / false")

    def t_missing():
        return _tb("Complete:  %d(x + ___) ≡ %dx + %d" % (k, k, k * c), c, "int", {}, ["%d ÷ %d = %d." % (k * c, k, c)])

    def t_area():
        return _wq("A rectangle is %d cm by (x + %d) cm. Write its area as an expanded expression (like 3x+12)." % (k, c),
                   "%dx+%d" % (k, k * c), ["%d(x + %d) = %dx + %d." % (k, c, k, k * c)], "e.g. 3x+12")

    def t_two_vars():
        p, q = random.randint(2, 6), random.randint(2, 9)
        return _wq("Expand  %d(%da + %db)  (like 6a+9b)" % (k, p, q), "%da+%db" % (k * p, k * q),
                   ["%d × %da + %d × %db." % (k, p, k, q)], "e.g. 6a+9b")

    def t_expand_add():
        e = random.randint(1, 15)
        return _wq("Expand and simplify  %d(x + %d) + %d  (like 3x+17)" % (k, c, e), "%dx+%d" % (k, k * c + e),
                   ["%dx + %d + %d = %dx + %d." % (k, k * c, e, k, k * c + e)], "e.g. 3x+17")

    def t_factor_back():
        p = random.randint(1, 9)
        while _g(p, c) != 1:
            p = random.randint(1, 9)
        inner = ("x" if p == 1 else "%dx" % p) + "+%d" % c
        return _wq("Complete:  %dx + %d = %d( ___ ). Type what goes in the bracket (like 2x+3)." % (k * p, k * c, k), inner,
                   ["Divide each term by %d." % k], "e.g. 2x+3")

    def t_value_check():
        x = random.randint(2, 9)
        return _tb("Show that %d(x + %d) and %dx + %d are equal when x = %d: what value do both give?" % (k, c, k, k * c, x),
                   k * (x + c), "int", {}, ["%d × %d = %d and %d × %d + %d = %d." % (k, x + c, k * (x + c), k, x, k * c, k * (x + c))])

    def t_error():
        return _wq("%s expanded %d(x + %d) and wrote %dx + %d. Write the correct expansion (like 3x+12)." % (_who(), k, c, k, c),
                   "%dx+%d" % (k, k * c), ["Multiply %d by both terms: %d × %d = %d." % (k, k, c, k * c)], "e.g. 3x+12")

    def t_expand_neg():
        return _wq("Expand  −%d(x − %d)  (like -3x+12)" % (k, c), "-%dx+%d" % (k, k * c),
                   ["−%d × x = −%dx and −%d × −%d = +%d." % (k, k, k, c, k * c)], "e.g. -3x+12")

    def t_expand_sub():
        e = random.randint(1, k * c - 1) if k * c > 1 else 1
        return _wq("Expand and simplify  %d(x + %d) − %d  (like 3x+5)" % (k, c, e), "%dx+%d" % (k, k * c - e),
                   ["%dx + %d − %d = %dx + %d." % (k, k * c, e, k, k * c - e)], "e.g. 3x+5")

    return _pick_t(_by(d, [t_expand, t_which, t_true, t_missing, t_area, t_value_check],
                       [t_expand, t_expand_minus, t_which, t_true, t_missing, t_area, t_two_vars, t_expand_add, t_factor_back,
                        t_value_check, t_error],
                       [t_expand_minus, t_true, t_two_vars, t_expand_add, t_factor_back, t_error, t_expand_neg, t_expand_sub]))


def _g(a, b):
    while b:
        a, b = b, a % b
    return a


# ================================================================== 7.3 ======
@skill("Y7.3.a", "Place value in integers and decimals of any size", S3)
def _(d=1):
    d = _d(d)

    def t_value_big():
        while True:
            n = random.randint(_by(d, 100_000, 10_000_000, 1_000_000_000), _by(d, 9_999_999, 999_999_999, 99_999_999_999))
            s = str(n)
            i = random.randint(0, 3)
            if s[i] != "0" and s.count(s[i]) == 1:
                break
        place = 10 ** (len(s) - 1 - i)
        return _tb("What is the value of the digit %s in %s?" % (s[i], _c(n)), int(s[i]) * place, "int", {},
                   ["It is worth %s." % _c(int(s[i]) * place)])

    def t_value_small():
        while True:
            x = (Decimal(random.randint(0, _by(d, 99, 9999, 9999)) * 10 + random.randint(1, 9))   # last digit not 0
                 / 10 ** random.randint(_by(d, 2, 3, 4), _by(d, 3, 4, 5)))
            s = format(x, "f").split(".")[1]
            i = max(k for k in range(len(s)) if s[k] != "0")
            if format(x, "f").count(s[i]) == 1:
                break
        return _tb("What is the value of the digit %s in %s? Write it as a decimal." % (s[i], _ds(x)),
                   _ds(Decimal(s[i]) / 10 ** (i + 1)), "num", {}, ["Place %d after the point." % (i + 1)])

    def t_million():
        m = random.randint(2, _by(d, 20, 99, 999))
        k = pick(_by(d, [Decimal("0.5"), Decimal("1.5"), Decimal("2.5")],
                     [Decimal("0.5"), Decimal("1.2"), Decimal("2.75"), Decimal("3.4")],
                     [Decimal("0.25"), Decimal("4.05"), Decimal("12.6"), Decimal("0.075"), Decimal("2.35")]))
        return _tb("Write %s million in figures." % _ds(k), int(k * 1_000_000), "int", {},
                   ["%s × 1,000,000 = %s." % (_ds(k), _c(int(k * 1_000_000)))]) if random.random() < 0.5 else \
            _tb("Write %d million in figures." % m, m * 1_000_000, "int", {}, ["%d × 1,000,000." % m])

    def t_times():
        x = Decimal(random.randint(1, _by(d, 99, 999, 9999))) / _by(d, 10, 100, 1000)
        k = pick(_by(d, [10, 100, 1000], [10, 100, 1000, Decimal("0.1"), Decimal("0.01")],
                     [1000, Decimal("0.1"), Decimal("0.01"), Decimal("0.001")]))
        return _tb("Work out %s × %s." % (_ds(x), _ds(k)), _ds(x * k), "num", {}, ["= %s." % _ds(x * k)])

    def t_divide():
        x = Decimal(random.randint(1, _by(d, 999, 9999, 99999))) / _by(d, 1, 10, 100)
        k = pick(_by(d, [10, 100], [10, 100, 1000], [100, 1000]))
        return _tb("Work out %s ÷ %d." % (_ds(x), k), _ds(x / k), "num", {}, ["= %s." % _ds(x / k)])

    def t_units():
        x = Decimal(random.randint(1, _by(d, 999, 9999, 99999))) / _by(d, 10, 100, 1000)
        a, b, f = pick([("km", "m", 1000), ("m", "cm", 100), ("kg", "g", 1000), ("cm", "mm", 10)])
        return _tb("Convert %s %s to %s." % (_ds(x), a, b), _ds(x * f), "num", {"unit": b}, ["× %d." % f])

    def t_times_bigger():
        dg = random.randint(1, 9)
        p1, p2 = sorted(random.sample(range(0, _by(d, 5, 7, 9)), 2))

        def holder(p):                      # a number whose only digit dg sits in place 10^p
            while True:
                n = dg * 10 ** p + random.randint(0, 10 ** p - 1)
                if str(n).count(str(dg)) == 1:
                    return n
        a, b = holder(p2), holder(p1)
        return _tb("How many times bigger is the value of the %d in %s than the value of the %d in %s?" % (dg, _c(a), dg, _c(b)),
                   10 ** (p2 - p1), "int", {}, ["The values are %s and %s." % (_c(dg * 10 ** p2), _c(dg * 10 ** p1)),
                                                "%s ÷ %s = %s." % (_c(dg * 10 ** p2), _c(dg * 10 ** p1), _c(10 ** (p2 - p1)))])

    def t_figures():
        n = random.randint(_by(d, 100_000, 1_000_000, 10_000_000), _by(d, 999_999, 9_999_999, 999_999_999))
        if random.random() < 0.5:
            n = n // 1000 * 1000 + random.randint(0, 99)
        return _tb("Write in figures: %s." % _words(n), n, "int", {}, ["= %s." % _c(n)])

    def t_line_big():
        m = random.randint(1, 9)
        k = random.randint(1, 9)
        v = m * 1_000_000 + k * 100_000
        return _nl("Place %s on the number line." % _c(v), v, 100_000, 1_000_000, ["%s is between %d million and %d million."
                                                                                 % (_c(v), m, m + 1)], lo=0, hi=10_000_000)

    def t_bigger_decimal():
        a = Decimal(random.randint(1, 9)) / 10 + Decimal(random.randint(1, 9)) / 100
        b = a - Decimal(random.randint(1, 9)) / 1000 * pick([1, -1]) - Decimal(random.randint(0, 1)) / 100
        b = b.quantize(Decimal("0.001"))
        if a == b:
            b += Decimal("0.001")
        return _tb("Which is larger: %s or %s?" % (_ds(a), _ds(b)), _ds(max(a, b)), "num", {},
                   ["Compare digit by digit: %s and %s." % (format(a, ".3f"), format(b, ".3f"))])

    def t_partition():
        dp = _by(d, 2, 3, 3)
        x = Decimal(random.randint(1, _by(d, 99, 99, 999)) * 10 ** dp + random.randint(1, 10 ** dp - 1)) / 10 ** dp
        s = format(x, "f")
        w, f = s.split(".")
        parts = [int(w)] + [Decimal(int(ch)) / 10 ** (i + 1) for i, ch in enumerate(f)]
        k = random.randrange(1, len(parts))
        if parts[k] == 0:
            k = 1 if parts[1] else 0
        shown = " + ".join("___" if i == k else _ds(p) for i, p in enumerate(parts) if p or i == k)
        return _tb("Complete:  %s = %s" % (_ds(x), shown), _ds(parts[k]), "num", {},
                   ["%s = %s." % (_ds(x), " + ".join(_ds(p) for p in parts if p))])

    return _pick_t([t_value_big, t_value_small, t_million, t_times, t_divide, t_units, t_times_bigger, t_figures,
                    t_bigger_decimal, t_partition], [t_line_big])


@skill("Y7.3.b", "Order integers, decimals and fractions with =, ≠, <, >, ≤, ≥", S3)
def _(d=1):
    d = _d(d)

    def t_symbol():
        a, b = random.sample([Decimal(random.randint(_by(d, 0, -99, -999), _by(d, 99, 99, 999)))
                              / pick(_by(d, [1, 10], [1, 10, 100], [10, 100, 1000])) for _ in range(4)], 2)
        if a == b:
            b = a + 1
        return _wq("Write < or > :  %s ___ %s" % (_ds(a), _ds(b)), "<" if a < b else ">",
                   ["On a number line the smaller number is further left."], "< or >")

    def t_neq():
        f, dec = pick(_by(d, [("1/2", "0.5"), ("1/4", "0.25"), ("3/4", "0.75"), ("1/10", "0.1")],
                          [("1/4", "0.25"), ("1/5", "0.2"), ("3/4", "0.75"), ("2/5", "0.4"), ("1/8", "0.125")],
                          [("3/8", "0.375"), ("7/20", "0.35"), ("5/8", "0.625"), ("3/25", "0.12"), ("9/20", "0.45")]))
        wrong = pick(_by(d, ["0.14", "0.5", "0.35", "0.04"], ["0.14", "0.5", "0.35", "0.04"],
                         ["0.38", "0.3", "0.65", "0.09", "0.83"]))
        same = random.random() < 0.5
        return _wq("Does = or ≠ go in the gap?  %s ___ %s   (type equal for =, or not equal for ≠)" % (f, dec if same else wrong),
                   "equal" if same else "not equal",
                   ["%s = %s, so the sign is %s." % (f, dec, "=" if same else "≠")], "equal / not equal")

    def t_order():
        vals = random.sample([Decimal(random.randint(_by(d, 0, -50, -99), _by(d, 50, 50, 99)))
                              / pick(_by(d, [1, 10], [1, 10], [10, 100])) for _ in range(6)], 4)
        vals = list(dict.fromkeys(vals))
        if len(vals) < 4:
            return t_symbol()
        asc = sorted(vals)
        return _tb("Order these from smallest to largest. Which comes 2nd?  %s" % ", ".join(_ds(v) for v in vals),
                   _ds(asc[1]), "num", {}, ["In order: %s." % ", ".join(_ds(v) for v in asc)])

    def t_mixed():
        items = _by(d, [(Fraction(1, 2), "1/2"), (Fraction(1, 4), "0.25"), (Fraction(3, 4), "75%"), (Fraction(1, 10), "0.1"),
                        (Fraction(9, 10), "9/10"), (Fraction(2, 5), "40%")],
                    [(Fraction(1, 2), "1/2"), (Fraction(3, 5), "0.6"), (Fraction(2, 5), "40%"), (Fraction(3, 4), "3/4"),
                     (Fraction(7, 10), "0.7"), (Fraction(1, 3), "1/3"), (Fraction(13, 20), "65%")],
                    # stretch: values bunched between 0.6 and 0.67, so every one must be converted
                    [(Fraction(5, 8), "5/8"), (Fraction(2, 3), "2/3"), (Fraction(3, 5), "0.6"), (Fraction(13, 20), "65%"),
                     (Fraction(16, 25), "0.64"), (Fraction(33, 50), "0.66"), (Fraction(31, 50), "62%")])
        pickd = random.sample(items, 4)
        big = max(pickd)[1]
        return _wq("Which is the largest?  %s" % ", ".join(p[1] for p in pickd), big,
                   ["As decimals: %s." % ", ".join(_ds(Decimal(p[0].numerator) / p[0].denominator) if p[0].denominator
                                                   in (2, 4, 5, 10, 20) else "%s ≈ %.3f" % (p[1], float(p[0]))
                                                   for p in pickd)], "as written")

    def t_inequality_int():
        lo, hi = random.randint(_by(d, 0, -8, -20), _by(d, 3, 3, -3)), random.randint(4, _by(d, 9, 12, 25))
        strict = pick([("<", "<"), ("≤", "<"), ("<", "≤"), ("≤", "≤")])
        vals = [n for n in range(lo - 1, hi + 2) if (n > lo if strict[0] == "<" else n >= lo) and
                (n < hi if strict[1] == "<" else n <= hi)]
        return _tb("How many whole numbers n satisfy  %d %s n %s %d ?" % (lo, strict[0], strict[1], hi), len(vals),
                   "int", {}, ["They are %s." % ", ".join(map(str, vals)) if vals else
                               "There are none: no whole number lies strictly between %d and %d." % (lo, hi)])

    def t_line():
        v = Decimal(random.randint(_by(d, 0, -40, -40), 40)) / 10
        return _nld("Place %s on the number line." % _ds(v), v, -5, 5, Decimal("0.1"), 1,
                    ["%s is between %d and %d." % (_ds(v), int(v.to_integral_value(rounding="ROUND_FLOOR")),
                                                   int(v.to_integral_value(rounding="ROUND_FLOOR")) + 1)])

    return _pick_t([t_symbol, t_neq, t_order, t_mixed, t_inequality_int], [t_line])


@skill("Y7.3.c", "Round to decimal places", S3)
def _(d=1):
    d = _d(d)
    dp = random.randint(1, _by(d, 1, 2, 3))
    x = Decimal(random.randint(1, 999999)) / 10 ** random.randint(dp + 1, dp + 3)
    q = Decimal(1).scaleb(-dp)
    r = x.quantize(q, rounding="ROUND_HALF_UP")

    def t_plain():
        return _tb("Round %s to %d decimal place%s." % (_ds(x), dp, "" if dp == 1 else "s"), format(r, "f"), "num", {},
                   ["Look at the next digit after place %d." % dp, "%s → %s." % (_ds(x), format(r, "f"))])

    def t_money():
        # easy: 3 d.p. under £10; medium: up to £1000; hard: 4 d.p. (exchange-rate style)
        places = _by(d, 3, 3, 4)
        p = Decimal(random.randint(_by(d, 1000, 10000, 100000), _by(d, 9999, 999999, 9999999))) / 10 ** places
        return _tb("A calculator shows £%s. Round it to the nearest penny, in pounds." % _ds(p),
                   format(p.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"), "f"), "num", {"unit": "£"},
                   ["2 decimal places: £%s." % format(p.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"), "f")])

    def t_trap_nine():
        w = random.randint(1, 30)
        if d == 0:      # no carry: 0.8x rounds within the tenths
            v = Decimal(w) + Decimal("0.8") + Decimal(random.randint(5, 9)) / 100
            r1 = v.quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
            return _tb("Round %s to 1 decimal place." % _ds(v), format(r1, "f"), "num", {},
                       ["The hundredths digit is 5 or more, so the 8 rounds up to 9: %s." % format(r1, "f")])
        if d == 2:      # 2 d.p. with a double carry: x.99y → (x+1).00
            v = Decimal(w) + Decimal("0.99") + Decimal(random.randint(5, 9)) / 1000
            r2 = v.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
            return _tb("Round %s to 2 decimal places." % _ds(v), format(r2, "f"), "num", {},
                       ["The 9 hundredths round up, carrying through the tenths into the ones: %s (written %s to 2 d.p.)."
                        % (_ds(r2), format(r2, "f"))])
        v = Decimal(w) + Decimal("0.9") + Decimal(random.randint(5, 9)) / 100
        r1 = v.quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        return _tb("Round %s to 1 decimal place." % _ds(v), format(r1, "f"), "num", {},
                   ["The 9 rounds up, carrying into the ones: %s (written %s to 1 d.p.)." % (_ds(r1), format(r1, "f"))])

    def t_between():
        if d == 0:      # nearest whole number
            lo = Decimal(random.randint(2, 30))
            return _tb("A number rounds to %s to the nearest whole number. What is the smallest it could be?" % _ds(lo),
                       _ds(lo - Decimal("0.5")), "num", {}, ["Halfway down: %s." % _ds(lo - Decimal("0.5"))])
        if d == 2:      # 2 d.p.
            lo = Decimal(random.randint(101, 999)) / 100
            return _tb("A number rounds to %s to 2 decimal places. What is the smallest it could be?" % format(lo, "f"),
                       _ds(lo - Decimal("0.005")), "num", {}, ["Halfway down: %s." % _ds(lo - Decimal("0.005"))])
        lo = Decimal(random.randint(10, 99)) / 10
        return _tb("A number rounds to %s to 1 decimal place. What is the smallest it could be?" % _ds(lo),
                   _ds(lo - Decimal("0.05")), "num", {}, ["Halfway down: %s." % _ds(lo - Decimal("0.05"))])

    def t_measure():
        what, unit, lo, hi = pick([("A runner's time", "seconds", 9000, 99999), ("A baby's mass", "kg", 2000, 5000),
                                   ("The length of a leaf", "cm", 1000, 25000), ("A bottle's capacity", "litres", 500, 3000)])
        if d == 0:      # 2 d.p. reading, round to 1 d.p.
            v = Decimal(random.randint(lo // 10, hi // 10)) / 100
            k = 1
        elif d == 2:    # 4 d.p. reading, round to 2 or 3 d.p.
            v = Decimal(random.randint(lo * 10, hi * 10)) / 10000
            k = random.randint(2, 3)
        else:
            v = Decimal(random.randint(lo, hi)) / 1000
            k = random.randint(1, 2)
        r1 = v.quantize(Decimal(1).scaleb(-k), rounding="ROUND_HALF_UP")
        return _tb("%s is %s %s. Round this to %d decimal place%s." % (what, _ds(v), unit, k, "" if k == 1 else "s"), format(r1, "f"),
                   "num", {"unit": unit}, ["%s → %s." % (_ds(v), format(r1, "f"))])

    def t_divide_round():
        a, b = random.randint(_by(d, 10, 10, 100), _by(d, 50, 99, 999)), pick(_by(d, [3, 6, 9], [3, 6, 7, 9, 11, 12],
                                                                                    [7, 11, 12, 13, 17]))
        if a % b == 0:
            a += 1
        k = _by(d, 1, 2, 3)
        q = (Decimal(a) / Decimal(b)).quantize(Decimal(1).scaleb(-k), rounding="ROUND_HALF_UP")
        return _tb("Work out %d ÷ %d on a calculator and round the answer to %d decimal place%s."
                   % (a, b, k, "" if k == 1 else "s"), format(q, "f"), "num", {},
                   ["%d ÷ %d = %s…" % (a, b, format(Decimal(a) / Decimal(b), ".5f")), "To %d d.p.: %s." % (k, format(q, "f"))])

    def t_largest_2dp():
        if d == 0:      # 1 d.p. that rounds to a whole number
            r0 = Decimal(random.randint(2, 30))
            return _tb("What is the largest number with 1 decimal place that rounds to %s to the nearest whole number?" % _ds(r0),
                       _ds(r0 + Decimal("0.4")), "num", {},
                       ["%s rounds up to %s, so the largest is %s." % (_ds(r0 + Decimal("0.5")), _ds(r0 + 1),
                                                                      _ds(r0 + Decimal("0.4")))])
        if d == 2:      # 3 d.p. that rounds to a 2 d.p. number
            r2 = Decimal(random.randint(101, 999)) / 100
            return _tb("What is the largest number with 3 decimal places that rounds to %s to 2 decimal places?" % format(r2, "f"),
                       _ds(r2 + Decimal("0.004")), "num", {},
                       ["%s rounds up to %s, so the largest is %s." % (_ds(r2 + Decimal("0.005")), format(r2 + Decimal("0.01"), "f"),
                                                                      _ds(r2 + Decimal("0.004")))])
        r1 = Decimal(random.randint(11, 99)) / 10
        return _tb("What is the largest number with 2 decimal places that rounds to %s to 1 decimal place?" % _ds(r1),
                   _ds(r1 + Decimal("0.04")), "num", {},
                   ["%s rounds up to %s, so the largest is %s." % (_ds(r1 + Decimal("0.05")), _ds(r1 + Decimal("0.1")),
                                                                  _ds(r1 + Decimal("0.04")))])

    def t_error():
        w = random.randint(1, 20)
        if d == 0:      # rounded up when the next digit was under 5
            t, h = random.randint(1, 7), random.randint(1, 4)
            v = Decimal(w) + Decimal(t) / 10 + Decimal(h) / 100
            r1 = v.quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
            return _tb("%s rounded %s to 1 decimal place and wrote %s. What is the correct answer?"
                       % (_who(), _ds(v), _ds(r1 + Decimal("0.1"))), format(r1, "f"), "num", {},
                       ["The hundredths digit is %d, which is less than 5, so round down: %s." % (h, _ds(r1))])
        if d == 2:      # 2 d.p. version of the 9-carry slip
            v = Decimal(w) + Decimal("0.99") + Decimal(random.randint(5, 9)) / 1000
            r2 = v.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
            return _tb("%s rounded %s to 2 decimal places and wrote %d.910. What is the correct answer?" % (_who(), _ds(v), w),
                       format(r2, "f"), "num", {}, ["The 9 hundredths round up, carrying through the tenths into the ones: %s (written %s)."
                                            % (_ds(r2), format(r2, "f"))])
        v = Decimal(w) + Decimal(random.randint(95, 99)) / 100
        r1 = v.quantize(Decimal("0.1"), rounding="ROUND_HALF_UP")
        return _tb("%s rounded %s to 1 decimal place and wrote %d.10. What is the correct answer?" % (_who(), _ds(v), w),
                   format(r1, "f"), "num", {}, ["The 9 tenths round up to a whole one: %s (written %s)." % (_ds(r1), format(r1, "f"))])

    def t_whole():
        # easy: one decimal place; medium: two; hard: three, larger numbers
        places = _by(d, 1, 2, 3)
        v = Decimal(random.randint(_by(d, 11, 1001, 10001), _by(d, 999, 99999, 9999999))) / 10 ** places
        r1 = v.quantize(Decimal(1), rounding="ROUND_HALF_UP")
        return _tb("Round %s to the nearest whole number." % _ds(v), format(r1, "f"), "num", {}, ["Look at the tenths digit: %s." % _ds(r1)])

    def t_which():
        # easy: rounds to a whole number; medium: to 1 d.p.; hard: to 2 d.p.
        k = _by(d, 0, 1, 2)
        u = Decimal(1).scaleb(-k)                 # the rounding unit
        r1 = Decimal(random.randint(_by(d, 2, 11, 101), _by(d, 30, 99, 999))) * u
        good = r1 + Decimal(random.randint(-5, 4)) * u / 10
        bads = [r1 - u * Decimal("0.6"), r1 + u * Decimal("0.5"), r1 + u * Decimal("1.1"), r1 - u]
        shown = [good] + random.sample(bads, 3)
        random.shuffle(shown)
        to = "the nearest whole number" if k == 0 else "%d decimal place%s" % (k, "" if k == 1 else "s")
        fmt = "." + str(k + 1) + "f"
        return _tb("Which of these rounds to %s to %s?  %s" % (format(r1, "." + str(k) + "f"), to, ", ".join(format(s, fmt) for s in shown)),
                   _ds(good), "num", {}, ["Numbers from %s up to (not including) %s round to %s." % (_ds(r1 - u / 2),
                                                                                                   _ds(r1 + u / 2), _ds(r1))])

    def t_table():
        names = random.sample(["Ava", "Ben", "Cal", "Dee", "Eli"], 3)
        # easy: 2 d.p. heights to 1 d.p.; medium: 3 d.p. to 2 d.p.; hard: 4 d.p. to 3 d.p.
        k = _by(d, 1, 2, 3)
        vals = [Decimal(random.randint(11, 19) * 10 ** k + random.randint(0, 10 ** k - 1)) / 10 ** (k + 1) for _ in names]
        kk = random.randrange(3)
        r1 = vals[kk].quantize(Decimal(1).scaleb(-k), rounding="ROUND_HALF_UP")
        return _dt("The table shows jump heights in metres. Round %s's jump to %d decimal place%s." % (names[kk], k, "" if k == 1 else "s"),
                   ["Name", "Height (m)"], [[n, _ds(v)] for n, v in zip(names, vals)], _ds(r1),
                   ["%s → %s." % (_ds(vals[kk]), format(r1, "f"))], atype="num")

    return _pick_t([t_plain, t_money, t_trap_nine, t_between, t_measure, t_divide_round, t_largest_2dp, t_error, t_whole,
                    t_which], [t_table])


@skill("Y7.3.d", "Round to 1 significant figure and estimate", S3)
def _(d=1):
    d = _d(d)

    def _sf1(v):
        v = Decimal(v)
        e = v.adjusted()
        return v.scaleb(-e).quantize(Decimal(1), rounding="ROUND_HALF_UP").scaleb(e)

    def t_round():
        v = pick([random.randint(11, _by(d, 999, 99999, 9_999_999)),
                  Decimal(random.randint(11, _by(d, 99, 999, 9999))) / _by(d, 100, 1000, 100000)])
        r = _sf1(v)
        return _tb("Round %s to 1 significant figure." % (_c(v) if isinstance(v, int) else _ds(v)), _ds(r), "num", {},
                   ["Keep the first non-zero digit, rounding it: %s." % _ds(r)])

    def t_estimate_mult():
        a, b = random.randint(_by(d, 11, 11, 101), _by(d, 49, 99, 999)), random.randint(11, _by(d, 49, 99, 99))
        ea, eb = _sf1(a), _sf1(b)
        return _tb("Estimate %d × %d by rounding each number to 1 significant figure." % (a, b), int(ea * eb), "int", {},
                   ["%s × %s = %s." % (_ds(ea), _ds(eb), _ds(ea * eb))])

    def t_estimate_div():
        # built from the rounded pair, so the estimate always divides exactly
        unit = _by(d, 100, 100, 1000)
        ea, eb = pick([(m * unit, t * 10) for m in range(2, 10) for t in range(1, _by(d, 3, 5, 9) + 1)
                       if (m * unit) % (t * 10) == 0])
        a = pick([v for v in range(ea - unit // 2, ea + unit // 2) if v != ea])
        b = pick([v for v in range(max(11, eb - 5), eb + 5) if v != eb])
        ea, eb = _sf1(a), _sf1(b)
        return _tb("Estimate %d ÷ %d by rounding each number to 1 significant figure." % (a, b), int(ea / eb), "int", {},
                   ["%s ÷ %s = %s." % (_ds(ea), _ds(eb), _ds(ea / eb))])

    def t_sensible():
        a, b = random.randint(21, _by(d, 49, 89, 899)), random.randint(21, 89)
        right = a * b
        wrong = right * 10
        shown = pick([right, wrong])
        return _wq("%s says %d × %d = %s. Use an estimate to decide: is it sensible? (yes or no)" % (_who(), a, b, _c(shown)),
                   "yes" if shown == right else "no",
                   ["Estimate: %s × %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(a) * _sf1(b)))], "yes / no")

    def t_decimal_est():
        a = Decimal(random.randint(21, 99)) / _by(d, 10, 10, 100)
        b = random.randint(21, _by(d, 89, 89, 899))
        return _tb("Estimate %s × %d by rounding each number to 1 significant figure." % (_ds(a), b),
                   _ds(_sf1(a) * _sf1(b)), "num", {}, ["%s × %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(a) * _sf1(b)))])

    def t_est_add():
        a, b = [random.randint(_by(d, 110, 1100, 11000), _by(d, 949, 9499, 94999)) for _ in range(2)]
        return _tb("Estimate %s + %s by rounding each number to 1 significant figure." % (_c(a), _c(b)), int(_sf1(a) + _sf1(b)),
                   "int", {}, ["%s + %s = %s." % (_c(int(_sf1(a))), _c(int(_sf1(b))), _c(int(_sf1(a) + _sf1(b))))])

    def t_est_money():
        n = random.randint(11, _by(d, 29, 49, 99))
        p = Decimal(random.randint(150, 950)) / 100 - Decimal("0.01") * pick([0, 1, 5])
        return _tb("%d tickets cost £%s each. Estimate the total cost by rounding each number to 1 significant figure, in pounds."
                   % (n, format(p, ".2f")), _ds(_sf1(n) * _sf1(p)), "num", {"unit": "£"},
                   ["%s × %s = %s." % (_ds(_sf1(n)), _ds(_sf1(p)), _ds(_sf1(n) * _sf1(p)))])

    def t_est_frac():
        a, b = random.randint(21, 89), random.randint(21, 89)
        c = pick([Decimal("4.8"), Decimal("5.2"), Decimal("1.9"), Decimal("2.1"), Decimal("9.7"), Decimal("10.3")])
        top = _sf1(a) * _sf1(b)
        if top % _sf1(c):
            return t_est_add()
        return _tb("Estimate (%d × %d) ÷ %s by rounding each number to 1 significant figure." % (a, b, _ds(c)),
                   _ds(top / _sf1(c)), "num", {}, ["(%s × %s) ÷ %s = %s ÷ %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(c)),
                                                                                     _ds(top), _ds(_sf1(c)), _ds(top / _sf1(c)))])

    def t_count_sf():
        v = pick(_by(d, ["4,025", "12.05", "0.004", "360.1", "5.002", "0.0089"],
                     ["0.0305", "4,025", "0.70", "12.05", "0.004", "360.1", "5.002", "0.0089", "7.0"],
                     ["0.0305", "0.70", "0.0089", "7.0", "0.0400", "10.050", "0.00602"]))
        n = {"0.0305": 3, "4,025": 4, "0.70": 2, "12.05": 4, "0.004": 1, "360.1": 4, "5.002": 4, "0.0089": 2, "7.0": 2,
             "0.0400": 3, "10.050": 5, "0.00602": 3}[v]
        return _tb("How many significant figures does %s have, as written?" % v, n, "int", {},
                   ["Start counting at the first non-zero digit; zeros between or after (after the point) count."])

    def t_est_area():
        a = Decimal(random.randint(51, 94)) / 10
        b = Decimal(random.randint(21, 49)) / 10
        return _tb("A room is %s m by %s m. Estimate its area by rounding each length to 1 significant figure, in m²."
                   % (_ds(a), _ds(b)), _ds(_sf1(a) * _sf1(b)), "num", {"unit": "m²"},
                   ["%s × %s = %s." % (_ds(_sf1(a)), _ds(_sf1(b)), _ds(_sf1(a) * _sf1(b)))])

    def t_over_under():
        a, b = random.randint(21, 99), random.randint(21, 99)
        ea, eb = _sf1(a), _sf1(b)
        if (ea - a) * (eb - b) < 0 or ea == a or eb == b:
            a, b = 10 * random.randint(2, 4) + random.randint(1, 3), 10 * random.randint(2, 4) + random.randint(1, 3)
            ea, eb = _sf1(a), _sf1(b)
        over = ea > a
        return _wq("You estimate %d × %d as %s × %s. Is the estimate bigger or smaller than the exact answer? (type bigger or "
                   "smaller)" % (a, b, _ds(ea), _ds(eb)), "bigger" if over else "smaller",
                   ["Both numbers were rounded %s." % ("up" if over else "down")], "bigger / smaller")

    return _pick_t(_by(d, [t_round, t_estimate_mult, t_sensible, t_est_add, t_est_money, t_count_sf, t_est_area],
                       [t_round, t_estimate_mult, t_estimate_div, t_sensible, t_decimal_est, t_est_add, t_est_money, t_est_frac,
                        t_count_sf, t_est_area, t_over_under],
                       [t_round, t_estimate_mult, t_estimate_div, t_sensible, t_decimal_est, t_est_add, t_est_frac, t_count_sf,
                        t_over_under]))


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
