# Year 9 generators: strands 9.2 and 9.3.
#
# Equations: unknowns on both sides with brackets and fractions, simple quadratics (x² = k),
# simultaneous linear equations, inequalities including dividing by a negative.  Graphs: gradient
# between two points, the equation of a line through two points, parallel lines, intercepts,
# quadratic graphs (tables, roots, turning points) and distance–time graphs.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S2 = "9.2 Equations & inequalities"
S3 = "9.3 Graphs"


def _t(c):
    return ("+ %d" % c) if c >= 0 else ("− %d" % -c)


def _m(v):
    """A number with a proper minus sign: −15, not -15."""
    return ("−%d" % -v) if v < 0 else "%d" % v


def _k(k, v="x"):
    """3x, x, −x for display."""
    return v if k == 1 else ("−" + v) if k == -1 else "%d%s" % (k, v)


def _line(m, c):
    """y=2x+3 compact text."""
    s = "y=%sx" % ("" if m == 1 else "-" if m == -1 else str(m))
    if c > 0:
        s += "+%d" % c
    elif c < 0:
        s += "%d" % c
    return s


# ================================================================== 9.2 ======
@skill("Y9.2.a", "Equations with unknowns on both sides and brackets", S2)
def _(d=1):
    d = _d(d)
    # easy: positive x and constants, x on the right once; hard: wider range, bigger coefficients
    x = random.randint(*_by(d, (1, 10), (-8, 12), (-12, 15)))
    a, c = random.randint(*_by(d, (3, 6), (3, 9), (5, 12))), random.randint(*_by(d, (1, 1), (1, 2), (2, 4)))
    b = random.choice([v for v in range(*_by(d, (1, 13), (-15, 16), (-20, 21))) if v])
    e = (a - c) * x + b
    while e == 0 or b == 0:
        b += 1
        e += 1

    def undo(n, v="x"):
        """The inverse step that clears the number n from the side with the unknown."""
        return ("Take %d from both sides" % n) if n > 0 else ("Add %d to both sides" % -n)

    def steps(kx, n, rhs, v="x"):
        """kx + n = rhs, solved by inverse steps: clear the number, then divide."""
        return ["%s: %s = %s." % (undo(n), _k(kx, v), _m(rhs - n)),
                "Divide both sides by %d: %s = %s." % (kx, v, _m((rhs - n) // kx))]

    def t_both():
        return _tb("Solve  %s %s = %s %s" % (_k(a), _t(b), _k(c), _t(e)), x, "int", {},
                   ["Take %s from both sides, so the x terms are on one side: %s %s = %s." % (_k(c), _k(a - c), _t(b), _m(e))]
                   + steps(a - c, b, e))

    def t_brackets():
        k, m = random.randint(*_by(d, (3, 5), (3, 6), (3, 9))), random.choice([v for v in range(*_by(d, (1, 7), (-6, 7), (-9, 10))) if v])
        rhs = k * (x + m) - 2 * x
        if rhs == 0:
            return t_both()
        return _tb("Solve  %d(x %s) = 2x %s" % (k, _t(m), _t(rhs)), x, "int", {},
                   ["Multiply out the bracket: %dx %s = 2x %s." % (k, _t(k * m), _t(rhs)),
                    "Take 2x from both sides: %s %s = %s." % (_k(k - 2), _t(k * m), _m(rhs))] + steps(k - 2, k * m, rhs))

    def t_two_brackets():
        p, q = random.randint(*_by(d, (2, 5), (2, 5), (3, 8))), random.randint(*_by(d, (1, 4), (1, 4), (2, 6)))
        if p == q:
            p += 1
        rr = [v for v in range(*_by(d, (-5, 6), (-5, 6), (-9, 10))) if v]
        r, s2 = random.choice(rr), random.choice(rr)
        lhs_c, rhs_c = p * r, q * s2
        if (rhs_c - lhs_c) % (p - q):
            return t_both()
        xx = (rhs_c - lhs_c) // (p - q)
        return _tb("Solve  %d(x %s) = %d(x %s)" % (p, _t(r), q, _t(s2)), xx, "int", {},
                   ["Multiply out both brackets: %dx %s = %dx %s." % (p, _t(lhs_c), q, _t(rhs_c)),
                    "Take %dx from both sides: %s %s = %s." % (q, _k(p - q), _t(lhs_c), _m(rhs_c))] + steps(p - q, lhs_c, rhs_c))

    def t_negative_coef():
        k = random.randint(2, 6)
        return _tb("Solve  %d − %dx = %d" % (b, k, b - k * x), x, "int", {},
                   ["%s: −%dx = %s." % (undo(b), k, _m(-k * x)),
                    "Divide both sides by −%d (a negative divided by a negative is positive): x = %d." % (k, x)
                    if x > 0 else "Divide both sides by −%d: x = %s." % (k, _m(x))])

    def t_word():
        y = random.randint(*_by(d, (2, 10), (3, 15), (6, 25)))
        p, s, q = _by(d, (4, 1, 2), (5, 3, 2), (7, 4, 3))     # pn − s = qn + K
        kk = (p - q) * y - s
        return _tb("I think of a number, multiply it by %d and subtract %d. I get the same as when I multiply it by %d and add %d. What is "
                   "the number?" % (p, s, q, kk), y, "int", {},
                   ["Call the number n: %dn − %d = %dn + %d." % (p, s, q, kk),
                    "Take %dn from both sides: %s − %d = %d." % (q, _k(p - q, "n"), s, kk)] + steps(p - q, -s, kk, "n"))

    plain = [t_both, t_brackets, t_two_brackets, t_negative_coef, t_word]
    if d == 0:
        plain = [t_both, t_brackets, t_word]
    elif d == 2:
        plain = [t_both, t_brackets, t_two_brackets, t_two_brackets, t_negative_coef, t_word]
    return _pick_t(plain)


@skill("Y9.2.b", "Equations with fractions and simple quadratics", S2)
def _(d=1):
    d = _d(d)

    def t_fraction():
        k, x = random.randint(*_by(d, (2, 5), (2, 6), (3, 9))), random.randint(*_by(d, (1, 10), (-5, 12), (-12, 15)))
        c = random.randint(*_by(d, (1, 9), (1, 9), (5, 20)))
        return _tb("Solve  x/%d %s = %d" % (k, _t(c), x + c), k * x, "int", {}, ["x/%d = %d, so x = %d." % (k, x, k * x)])

    def t_both_frac():
        a, b = pick([(2, 3), (3, 4), (2, 5), (4, 5)])
        x = a * b * random.randint(*_by(d, (1, 4), (1, 6), (2, 9)))
        return _tb("Solve  x/%d + x/%d = %d" % (a, b, x // a + x // b), x, "int", {},
                   ["Multiply by %d: %dx + %dx = %d." % (a * b, b, a, (x // a + x // b) * a * b), "x = %d." % x])

    def t_square():
        k = random.randint(*_by(d, (2, 10), (2, 15), (11, 20)))
        return _tb("Solve x² = %d. Give the positive answer." % (k * k), k, "int", {}, ["x = ±%d." % k])

    def t_square_neg():
        k = random.randint(*_by(d, (2, 10), (2, 12), (8, 15)))
        return _tb("Solve x² = %d. Give the NEGATIVE answer." % (k * k), -k, "int", {}, ["x = ±%d." % k])

    def t_sq_linear():
        k, c = random.randint(*_by(d, (2, 6), (2, 9), (5, 12))), random.randint(*_by(d, (1, 10), (1, 30), (10, 60)))
        return _tb("Solve x² + %d = %d. Give the positive answer." % (c, k * k + c), k, "int", {}, ["x² = %d, x = %d." % (k * k, k)])

    def t_count():
        k = random.randint(1, 9)
        return _tb("How many solutions does x² = %d have?" % (k * k), 2, "int", {}, ["x = %d or x = −%d." % (k, k)])

    def t_frac_each_side():
        p, q = pick([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6)])
        x = random.randint(*_by(d, (-6, 15), (-6, 15), (-12, 20)))
        a = random.randint(*_by(d, (-5, 9), (-5, 9), (-9, 12)))
        # (x + a)/p = (x + b)/q  ->  q(x + a) = p(x + b)  ->  b = (q(x + a) − px)/p must be whole
        num = q * (x + a) - p * x
        if num % p:
            x += next(k for k in range(1, p + 1) if (q * (x + k + a) - p * (x + k)) % p == 0)
            num = q * (x + a) - p * x
        b = num // p
        _f = lambda c, k: ("x/%d" % k) if c == 0 else "(x %s)/%d" % (_t(c), k)
        return _tb("Solve  %s = %s" % (_f(a, p), _f(b, q)), x, "int", {},
                   ["Cross-multiply: %d%s = %d%s." % (q, "x" if a == 0 else "(x %s)" % _t(a), p, "x" if b == 0 else "(x %s)" % _t(b)), "x = %d." % x])

    def t_reciprocal():
        x = pick([2, 3, 4, 5, 6, 8])
        k = x * random.randint(2, 9)
        c = random.randint(1, 9)
        return _tb("Solve  %d/x + %d = %d" % (k, c, k // x + c), x, "int", {}, ["%d/x = %d." % (k, k // x), "x = %d ÷ %d = %d." % (k, k // x, x)])

    def t_coef_square():
        a, k = random.randint(*_by(d, (2, 3), (2, 5), (3, 8))), random.randint(*_by(d, (2, 6), (2, 10), (4, 12)))
        return _tb("Solve %dx² = %d. Give the positive answer." % (a, a * k * k), k, "int", {}, ["x² = %d." % (k * k), "x = %d." % k])

    def t_bracket_square():
        h, k = random.choice([v for v in range(*_by(d, (-6, 7), (-6, 7), (-9, 10))) if v]), random.randint(*_by(d, (2, 9), (2, 9), (4, 12)))
        return _tb("Solve (x %s)² = %d. Give the LARGER answer." % (_t(-h), k * k), h + k, "int", {},
                   ["x %s = ±%d." % (_t(-h), k), "x = %d or x = %d." % (h + k, h - k)])

    def t_both():
        k = random.randint(*_by(d, (2, 10), (2, 13), (9, 20)))
        return {"prompt": "Solve x² = %d. Type both answers, like -3, 3." % (k * k), "component": "number",
                "spec": {"text": True, "placeholder": "e.g. -3, 3"}, "answer": "%d, %d" % (-k, k), "answer_type": "set",
                "solution": ["x = %d or x = −%d." % (k, k)]}

    def t_rectangle():
        k, x = random.randint(*_by(d, (2, 3), (2, 5), (3, 7))), random.randint(*_by(d, (2, 6), (2, 9), (4, 12)))
        return _tb("A rectangle is x cm wide and %dx cm long. Its area is %d cm². Find x." % (k, k * x * x), x, "int", {"unit": "cm"},
                   ["%dx² = %d." % (k, k * x * x), "x² = %d, x = %d." % (x * x, x)])

    plain = [t_fraction, t_both_frac, t_square, t_square_neg, t_sq_linear, t_count, t_frac_each_side, t_reciprocal, t_coef_square,
             t_bracket_square, t_both, t_rectangle]
    if d == 0:
        plain = [t_fraction, t_square, t_square_neg, t_sq_linear, t_count, t_both, t_rectangle]
    elif d == 2:
        plain = [t_fraction, t_both_frac, t_frac_each_side, t_frac_each_side, t_reciprocal, t_coef_square, t_bracket_square, t_both, t_rectangle]
    return _pick_t(plain)


@skill("Y9.2.c", "Simultaneous linear equations", S2)
def _(d=1):
    d = _d(d)
    # easy: positive solutions, small coefficients; hard: negatives likely, one equation must be scaled first
    lo, hi = _by(d, (1, 9), (-5, 9), (-9, 12))
    x, y = random.randint(lo, hi), random.randint(lo, hi)

    def t_add():
        a, b = random.randint(1, 4), random.randint(1, 5)
        return _tb("Solve:  %s + %s = %d  and  %s − %s = %d.  What is x?" % (_k(a), _k(b, "y"), a * x + b * y, _k(a), _k(b, "y"), a * x - b * y), x, "int", {},
                   ["Add them: %dx = %d." % (2 * a, 2 * a * x), "x = %d." % x])

    def t_find_y():
        a, b = random.randint(1, 4), random.randint(1, 5)
        return _tb("Solve:  %s + %s = %d  and  %s − %s = %d.  What is y?" % (_k(a), _k(b, "y"), a * x + b * y, _k(a), _k(b, "y"), a * x - b * y), y, "int", {},
                   ["Subtract them: %dy = %d." % (2 * b, 2 * b * y), "y = %d." % y])

    def t_subtract():
        a, b, c = random.randint(1, 5), random.randint(1, _by(d, 3, 5, 9)), random.randint(1, 5)
        if a == c:
            c += 1
        return _tb("Solve:  %s + %s = %d  and  %s + %s = %d.  What is x?" % (_k(a), _k(b, "y"), a * x + b * y, _k(c), _k(b, "y"), c * x + b * y), x, "int", {},
                   ["Subtract: %s = %d." % (_k(a - c), (a - c) * x), "x = %d." % x])

    def t_substitute():
        m, c = random.randint(1, 4), random.choice([v for v in range(*_by(d, (1, 6), (-5, 6), (-9, 10))) if v])
        k = random.randint(1, _by(d, 2, 3, 4))
        yy = m * x + c
        return _tb("y = %s %s and x + %s = %d. Find x." % (_k(m), _t(c), _k(k, "y"), x + k * yy), x, "int", {},
                   ["Substitute: x + %d(%s %s) = %d." % (k, _k(m), _t(c), x + k * yy), "x = %d." % x])

    def t_word():
        a, b = random.randint(*_by(d, (2, 9), (2, 9), (4, 15))), random.randint(*_by(d, (2, 9), (2, 9), (4, 15)))
        n1, n2 = random.randint(1, 5), random.randint(1, 5)
        m1, m2 = random.randint(1, 5), random.randint(1, 5)
        if n1 * m2 == n2 * m1:
            m2 += 1
        return _tb("%s and %s cost %dp. %s and %s cost %dp. How much is one pen, in pence?"
                   % (_pl(n1, "pen"), _pl(m1, "pencil"), n1 * a * 10 + m1 * b * 10, _pl(n2, "pen"), _pl(m2, "pencil"), n2 * a * 10 + m2 * b * 10), a * 10, "int", {"unit": "p"},
                   ["Solve the pair of equations: pen = %dp, pencil = %dp." % (a * 10, b * 10)])

    def t_check():
        a, b = random.randint(1, 5), random.randint(1, 5)
        cand = (x + pick([0, 1]), y)
        ok = a * cand[0] + b * cand[1] == a * x + b * y and cand[0] - cand[1] == x - y
        return _wq("Does x = %d, y = %d solve both  %s + %s = %d  and  x − y = %d ? (yes or no)" % (cand[0], cand[1], _k(a), _k(b, "y"), a * x + b * y, x - y),
                   "yes" if ok else "no", ["Substitute into both."], "yes / no")

    def t_scale():
        # a x + b y = P and c x + kb y = Q: multiply the first by k, then subtract
        a, b, k = random.randint(1, 5), random.randint(1, 4), random.randint(2, 4)
        c = random.choice([v for v in range(1, 9) if v != k * a])
        p1, q1 = a * x + b * y, c * x + k * b * y
        return _tb("Solve:  %s + %s = %d  and  %s + %s = %d.  What is x?" % (_k(a), _k(b, "y"), p1, _k(c), _k(k * b, "y"), q1), x, "int", {},
                   ["Multiply the first by %d: %s + %s = %d." % (k, _k(k * a), _k(k * b, "y"), k * p1),
                    "Subtract the second: %s = %d." % (_k(k * a - c), k * p1 - q1), "x = %d." % x])

    plain = [t_add, t_find_y, t_subtract, t_substitute, t_word, t_check]
    if d == 0:
        plain = [t_add, t_find_y, t_subtract, t_substitute, t_check]
    elif d == 2:
        plain = [t_subtract, t_substitute, t_word, t_scale, t_scale]
    return _pick_t(plain)


@skill("Y9.2.d", "Solve inequalities, including with negatives", S2)
def _(d=1):
    d = _d(d)
    # easy: positive boundary and constants; hard: x on both sides, a multiple of 3 in the double inequality
    x0 = random.randint(*_by(d, (1, 10), (-6, 10), (-10, 12)))
    k = random.randint(*_by(d, (2, 5), (2, 6), (3, 9)))
    c = random.choice([v for v in range(*_by(d, (1, 11), (-10, 11), (-15, 16))) if v])

    def t_basic():
        return _tb("Solve  %dx %s > %d. The answer is x > ___ ." % (k, _t(c), k * x0 + c), x0, "int", {},
                   ["%dx > %d, x > %d." % (k, k * x0, x0)])

    def t_negative():
        return _wq("Solve  %d − %dx ≥ %d. Write the answer like x<=3." % (c, k, c - k * x0), "x<=%d" % x0,
                   ["−%dx ≥ %d." % (k, -k * x0), "Dividing by a negative flips the sign: x ≤ %d." % x0], "e.g. x<=3")

    def t_double():
        lo, hi = random.randint(*_by(d, (0, 3), (-5, 3), (-8, 3))), random.randint(*_by(d, (4, 9), (4, 12), (4, 15)))
        mm = _by(d, 2, 2, 3)
        return _tb("How many whole numbers satisfy  %d < %dx ≤ %d ?" % (mm * lo, mm, mm * hi), hi - lo, "int", {},
                   ["%d < x ≤ %d." % (lo, hi), "x = %s." % ", ".join(str(v) for v in range(lo + 1, hi + 1))])

    def t_largest():
        return _tb("x is a whole number and %dx %s < %d. What is the largest possible value of x?" % (k, _t(c), k * x0 + c + 1), x0, "int", {},
                   ["x < %s, so x = %d." % (_fs(Fraction(k * x0 + 1, k)), x0)])

    def t_line():
        op = pick(["<", "<=", ">", ">="])
        return {"prompt": "Write the inequality shown (like x>3, using <, >, <= or >=).", "component": "inequality_line",
                "spec": {"op": op, "value": x0, "min": x0 - 6, "max": x0 + 6}, "answer": "x%s%d" % (op, x0), "answer_type": "str",
                "solution": ["Open circle: < or >. Filled circle: ≤ or ≥."]}

    def t_both_sides():
        q = random.randint(1, k - 1) if k > 2 else 1
        e = c + (k - q) * x0
        last = "x < %d." % x0 if k - q == 1 else "%s < %d, x < %d." % (_k(k - q), (k - q) * x0, x0)
        return _wq("Solve  %dx %s < %s%s. Write the answer like x<3." % (k, _t(c), _k(q), (" " + _t(e)) if e else ""), "x<%d" % x0,
                   ["%dx − %s < %d − (%d)." % (k, _k(q), e, c), last], "e.g. x<3")

    plain = [t_basic, t_negative, t_double, t_largest]
    if d == 0:
        plain = [t_basic, t_double, t_largest]
    elif d == 2:
        plain = [t_negative, t_negative, t_double, t_largest, t_both_sides, t_both_sides]
    return _pick_t(plain, [t_line])


# ================================================================== 9.3 ======
@skill("Y9.3.a", "Gradient between two points", S3)
def _(d=1):
    d = _d(d)
    # easy: points in the first quadrant, positive gradient; hard: wider grid, steeper, fractional gradients anywhere
    x1, y1 = random.randint(*_by(d, (0, 4), (-5, 5), (-8, 8))), random.randint(*_by(d, (0, 4), (-5, 5), (-8, 8)))
    m = random.choice([v for v in range(*_by(d, (1, 4), (-4, 5), (-6, 7))) if v])
    dx = random.randint(1, _by(d, 3, 4, 5))
    x2, y2 = x1 + dx, y1 + m * dx

    def t_grad():
        return _tb("Find the gradient of the line through (%d,%d) and (%d,%d)." % (x1, y1, x2, y2), m, "int", {},
                   ["(%d − %s) ÷ (%d − %s) = %d." % (y2, "(%d)" % y1 if y1 < 0 else y1, x2, "(%d)" % x1 if x1 < 0 else x1, m)])

    def t_frac():
        a, b = random.randint(1, 5), random.randint(2, 5)
        if a % b == 0:
            a += 1
        return _fq("Find the gradient of the line through (0,0) and (%d,%d)." % (b, a), Fraction(a, b), ["Rise %d over run %d." % (a, b)])

    def t_frac_points():
        a, b = random.choice([v for v in range(-7, 8) if v]), random.randint(2, 6)
        if a % b == 0:
            a += 1
        return _fq("Find the gradient of the line through (%d,%d) and (%d,%d). Give it as a fraction." % (x1, y1, x1 + b, y1 + a), Fraction(a, b),
                   ["Change in y: %d. Change in x: %d." % (a, b), "Gradient = %s." % _fs(Fraction(a, b))], "e.g. -3/4")

    def t_steeper():
        m2 = random.choice([v for v in range(*_by(d, (1, 7), (-6, 7), (-9, 10))) if v and abs(v) != abs(m)])
        return _wq("Which line is steeper: y = %s + 1 or y = %s − 2? Type the gradient of the steeper one." % (_k(m), _k(m2)),
                   str(m if abs(m) > abs(m2) else m2), ["Compare the sizes of the gradients."], "a number")

    def t_graph():
        return {"prompt": "The line is drawn. What is its gradient?", "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "lines": [{"p1": [x1, y1], "p2": [x2, y2]}],
                         "points": [[x1, y1, "A"], [x2, y2, "B"]], "typed": True},
                "answer": m, "answer_type": "num", "solution": ["From A to B: up %d, across %d." % (m * dx, dx)]} \
            if all(-7 <= v <= 7 for v in (x1, y1, x2, y2)) else t_grad()

    plain = [t_grad, t_frac, t_steeper]
    if d == 2:
        plain = [t_grad, t_frac_points, t_frac_points, t_steeper]
    return _pick_t(plain, [t_graph])


@skill("Y9.3.b", "Equation of a straight line", S3)
def _(d=1):
    d = _d(d)
    # easy: positive gradient and intercept, points to the right of the axis; hard: steeper, negatives, parallel through a point
    m = random.choice([v for v in range(*_by(d, (1, 4), (-4, 5), (-6, 7))) if v])
    c = random.randint(*_by(d, (0, 6), (-6, 6), (-10, 10)))

    def t_two_points():
        x1, x2 = random.sample(range(*_by(d, (0, 5), (-4, 5), (-6, 7))), 2)
        return _wq("Find the equation of the line through (%d,%d) and (%d,%d). Write it like y=2x+3." % (x1, m * x1 + c, x2, m * x2 + c),
                   _line(m, c), ["Gradient %d; substitute to get c = %d." % (m, c)], "e.g. y=2x+3")

    def t_point_grad():
        x1 = random.randint(*_by(d, (1, 4), (-4, 4), (-6, 6)))
        return _wq("A line has gradient %d and passes through (%d,%d). Write its equation like y=2x+3." % (m, x1, m * x1 + c), _line(m, c),
                   ["c = %d − %d × %s = %d." % (m * x1 + c, m, "(%d)" % x1 if x1 < 0 else x1, c)], "e.g. y=2x+3")

    def t_parallel():
        c2 = c + random.randint(1, 5)
        return _wq("Write the equation of the line parallel to %s that crosses the y-axis at %d. Write it like y=2x+3."
                   % (_line(m, c), c2), _line(m, c2), ["Parallel lines share the gradient %d." % m], "e.g. y=2x+3")

    def t_rearrange():
        a = random.randint(2, 5)
        if d == 2:
            return _tb("Write %dy %sx = %d in the form y = mx + c. What is m?" % (a, _t(-a * m), a * c), m, "int", {},
                       ["%dy = %s %s." % (a, _k(a * m), _t(a * c)), "Divide by %d: %s." % (a, _line(m, c))])
        return _tb("Write %dy = %dx%s in the form y = mx + c. What is m?" % (a, a * m, (" " + _t(a * c)) if c else ""), m, "int", {}, ["Divide by %d." % a])

    def t_parallel_point():
        x1 = random.choice([v for v in range(-5, 6) if v])
        c2 = c + random.choice([v for v in range(-6, 7) if v])
        return _wq("Find the equation of the line parallel to %s that passes through (%d,%d). Write it like y=2x+3."
                   % (_line(m, c), x1, m * x1 + c2), _line(m, c2),
                   ["Same gradient %d." % m, "c = %d − %s × %s = %d." % (m * x1 + c2, "(%d)" % m if m < 0 else m, "(%d)" % x1 if x1 < 0 else x1, c2)], "e.g. y=2x+3")

    def t_x_intercept():
        k = random.choice([v for v in range(-5, 6) if v])
        return _tb("Where does y = %s %s cross the x-axis? Give the x-value." % (_k(m), _t(-m * k)), k, "int", {},
                   ["Set y = 0: %s = %d, x = %d." % (_k(m), m * k, k)])

    plain = [t_two_points, t_point_grad, t_parallel, t_rearrange, t_x_intercept]
    if d == 0:
        plain = [t_two_points, t_point_grad, t_parallel, t_rearrange]
    elif d == 2:
        plain = [t_two_points, t_point_grad, t_parallel_point, t_parallel_point, t_rearrange, t_x_intercept]
    return _pick_t(plain)


@skill("Y9.3.c", "Quadratic graphs", S3)
def _(d=1):
    d = _d(d)
    # easy: small roots, table and intercept reading; hard: wider roots and table, turning point by symmetry
    p, q = random.randint(*_by(d, (-3, 0), (-5, 0), (-8, 0))), random.randint(*_by(d, (1, 4), (1, 5), (1, 8)))

    def t_table():
        b, c = -(p + q), p * q
        xs = _by(d, [-2, -1, 0, 1, 2, 3], [-2, -1, 0, 1, 2, 3], [-3, -2, -1, 0, 1, 2, 3, 4])
        rows = [[x, x * x + b * x + c] for x in xs]
        k = random.randrange(len(xs))
        return _io("Complete the table for y = %s." % _poly_txt(b, c), rows, k, rows[k][1],
                   ["Substitute x = %d: y = %d." % (rows[k][0], rows[k][1])])

    def t_roots():
        b, c = -(p + q), p * q
        return {"prompt": "Where does y = %s cross the x-axis? Type both x-values like -2, 3." % _poly_txt(b, c), "component": "number",
                "spec": {"text": True, "placeholder": "e.g. -2, 3"}, "answer": "%d, %d" % tuple(sorted([p, q])), "answer_type": "set",
                "solution": ["It factorises to (x %s)(x %s)." % (_t(-p), _t(-q))]}

    def t_turning():
        h, k = random.choice([v for v in range(*_by(d, (-4, 5), (-4, 5), (-7, 8))) if v]), random.choice([v for v in range(*_by(d, (-6, 7), (-6, 7), (-12, 13))) if v])
        return _wq("y = (x %s)² %s. Write the coordinates of the lowest point, like (2,-3)." % (_t(-h), _t(k)), "(%d,%d)" % (h, k),
                   ["The squared part is 0 when x = %d, giving y = %d." % (h, k)], "(x,y)")

    def t_y_intercept():
        b, c = random.randint(*_by(d, (0, 6), (-6, 6), (-9, 9))), random.randint(*_by(d, (1, 9), (-9, 9), (-20, 20)))
        return _tb("Where does y = %s cross the y-axis? Give the y-value." % _poly_txt(b, c), c, "int", {}, ["Put x = 0: y = %d." % c])

    def t_shape():
        return _wq("Is the graph of y = x² a straight line, a U-shaped curve or an S-shaped curve? (type straight, U or S)", "U",
                   ["Quadratic graphs are U-shaped (parabolas)."], "straight / U / S")

    def t_symmetry():
        b, c = -(p + q), p * q
        return _tb("The graph of y = %s crosses the x-axis at x = %d and x = %d. What is the x-coordinate of its lowest point?"
                   % (_poly_txt(b, c), p, q), _ds(Fraction(p + q, 2)), "num", {},
                   ["The curve is symmetrical, so the lowest point is halfway between the roots.", "(%d + %d) ÷ 2 = %s." % (p, q, _ds(Fraction(p + q, 2)))])

    plain = [t_table, t_roots, t_turning, t_y_intercept, t_shape]
    if d == 0:
        plain = [t_table, t_table, t_roots, t_y_intercept, t_shape]
    elif d == 2:
        plain = [t_table, t_roots, t_roots, t_turning, t_symmetry, t_symmetry]
    return _pick_t(plain)


def _poly_txt(b, c):
    s = "x²"
    if b:
        s += " %s %s" % ("+" if b > 0 else "−", ("" if abs(b) == 1 else str(abs(b))) + "x")
    if c:
        s += " %s %d" % ("+" if c > 0 else "−", abs(c))
    return s


@skill("Y9.3.d", "Distance–time and real-life graphs", S3)
def _(d=1):
    d = _d(d)

    def _journey(out_h, stop_h, speed):
        """Hourly points: out at `speed`, stop, then home in 2 hours (evenly spaced labels)."""
        pts, dist = [["0 h", 0]], 0
        for h in range(1, out_h + 1):
            dist += speed
            pts.append(["%d h" % h, dist])
        for h in range(out_h + 1, out_h + stop_h + 1):
            pts.append(["%d h" % h, dist])
        pts.append(["%d h" % (out_h + stop_h + 1), dist // 2])
        pts.append(["%d h" % (out_h + stop_h + 2), 0])
        return pts, dist

    def t_speed():
        speed, out_h = random.randint(*_by(d, (2, 4), (2, 6), (4, 9))) * 5, random.randint(*_by(d, (1, 2), (1, 3), (2, 4)))
        pts, dist = _journey(out_h, random.randint(1, 2), speed)
        return _lg("The graph shows a cycle ride (distance from home, in km, each hour). What was the speed on the way out, in km/h?",
                   pts, speed, ["%d km in %d h = %d km/h." % (dist, out_h, speed)], "km", "Time")

    def t_stop():
        speed, out_h, stop = random.randint(2, 6) * 5, random.randint(1, 3), random.randint(1, 2)
        pts, dist = _journey(out_h, stop, speed)
        return _lg("The graph shows a journey (distance from home each hour). For how many hours did the traveller stop?", pts, stop,
                   ["The flat part lasts %d hour%s." % (stop, "" if stop == 1 else "s")], "km", "Time")

    def t_formula():
        rate, fixed = random.randint(*_by(d, (2, 5), (2, 9), (12, 45))), random.randint(*_by(d, (5, 20), (5, 30), (20, 80)))
        h = random.randint(*_by(d, (2, 5), (2, 8), (3, 9)))
        return _tb("A plumber's charge is shown by a straight-line graph: £%d call-out plus £%d per hour. What does the line give for %d "
                   "hours, in pounds?" % (fixed, rate, h), fixed + rate * h, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (fixed, rate, h, fixed + rate * h)])

    def t_gradient_meaning():
        q, a = pick([("On a distance–time graph, what does the gradient show? (one word)", "speed"),
                     ("On a distance–time graph, does a horizontal line show the person is moving or stationary? (type moving or stationary)", "stationary")])
        return _wq(q, a, ["Gradient = distance ÷ time."], "one word")

    def t_formula_back():
        rate, fixed = random.randint(12, 45), random.randint(20, 80)
        h = random.randint(2, 9)
        return _tb("A plumber's charge is shown by a straight-line graph: £%d call-out plus £%d per hour. A bill was £%d. How many hours did "
                   "the job take?" % (fixed, rate, fixed + rate * h), h, "int", {"unit": "hours"},
                   ["£%d − £%d = £%d for the hours." % (fixed + rate * h, fixed, rate * h), "%d ÷ %d = %d hours." % (rate * h, rate, h)])

    def t_conversion():
        m = 5 * random.randint(*_by(d, (1, 6), (2, 16), (10, 40)))
        return _tb("A conversion graph shows 5 miles = 8 km. Use it to convert %d miles to km." % m, m // 5 * 8, "int", {"unit": "km"},
                   ["%d ÷ 5 × 8 = %d." % (m, m // 5 * 8)])

    def t_far():
        speed, out_h = random.randint(2, 6) * 5, random.randint(2, 3)
        pts, dist = _journey(out_h, random.randint(1, 2), speed)
        return _lg("The graph shows a walk (distance from home each hour). What is the greatest distance from home, in km?", pts, dist,
                   ["The highest point on the graph is %d km." % dist], "km", "Time")

    def t_home_speed():
        speed, out_h = random.randint(*_by(d, (2, 6), (2, 6), (3, 9))) * 10, random.randint(1, 3)
        pts, dist = _journey(out_h, 1, speed)
        return _lg("The graph shows a drive (distance from home each hour). The return home takes the last 2 hours. What is the average "
                   "speed on the way home, in km/h?", pts, _ds(Fraction(dist, 2)), ["%d km in 2 hours = %s km/h." % (dist, _ds(Fraction(dist, 2)))],
                   "km", "Time", atype="num")

    def t_total():
        speed, out_h = random.randint(2, 6) * 5, random.randint(1, 3)
        pts, dist = _journey(out_h, random.randint(1, 2), speed)
        return _lg("The graph shows a bike ride that starts and ends at home. What is the total distance cycled, in km?", pts, 2 * dist,
                   ["%d km out and %d km back." % (dist, dist)], "km", "Time")

    def t_tank():
        rate = random.randint(*_by(d, (1, 4), (2, 9), (5, 15))) * 5
        start = random.randint(0, 4) * 10
        pts = [["%d min" % m, start + rate * m] for m in range(0, 6)]
        return _lg("The graph shows the water in a tank as it fills. At what rate does it fill, in litres per minute?", pts, rate,
                   ["Each minute it rises by %d litres." % rate], "litres", "Time")

    def t_tariffs():
        fixed, per_a = random.randint(*_by(d, (2, 10), (2, 10), (5, 20))), random.randint(*_by(d, (2, 6), (2, 6), (3, 9)))
        per_b = per_a + pick([1, 2, 5])            # 100 × fixed always divides exactly
        m = fixed * 100 // (per_b - per_a)
        return _tb("Phone plan A costs £%d a month plus %dp a minute. Plan B costs %dp a minute and nothing else. Their graphs cross where the "
                   "costs are equal. For how many minutes is that?" % (fixed, per_a, per_b), m, "int", {"unit": "minutes"},
                   ["In pence: %d + %dm = %dm." % (fixed * 100, per_a, per_b), "%dm = %d, m = %d." % (per_b - per_a, fixed * 100, m)])

    def t_runner():
        sp = random.randint(3, 8)
        t = pick([20, 40, 50, 60, 80, 100])
        return _tb("A runner's distance–time graph is a straight line from (0 s, 0 m) to (%d s, %d m). What is the gradient, in m/s?"
                   % (t, sp * t), sp, "int", {"unit": "m/s"}, ["%d ÷ %d = %d m/s." % (sp * t, t, sp)])

    def t_conv_back():
        k = 8 * random.randint(*_by(d, (2, 16), (2, 16), (10, 40)))
        return _tb("A conversion graph shows 5 miles = 8 km. Use it to convert %d km to miles." % k, k // 8 * 5, "int", {"unit": "miles"},
                   ["%d ÷ 8 × 5 = %d." % (k, k // 8 * 5)])

    def t_temp_rise():
        temps = [random.randint(2, 8)]
        for _ in range(6):
            temps.append(temps[-1] + random.randint(-1, 4))
        hours = ["6 am", "8 am", "10 am", "noon", "2 pm", "4 pm", "6 pm"]
        i, j = sorted(random.sample(range(7), 2))
        return _lg("The graph shows the temperature during a day. By how many degrees did it change from %s to %s? (Use a minus sign for a fall.)"
                   % (hours[i], hours[j]), list(zip(hours, temps)), temps[j] - temps[i], ["%d − %d = %d." % (temps[j], temps[i], temps[j] - temps[i])],
                   "°C", "Time")

    plain = [t_formula, t_gradient_meaning, t_conversion, t_tariffs, t_runner, t_conv_back]
    visual = [t_speed, t_stop, t_far, t_home_speed, t_total, t_tank, t_temp_rise]
    if d == 0:
        plain, visual = [t_formula, t_gradient_meaning, t_conversion], [t_speed, t_stop, t_far, t_total, t_tank]
    elif d == 2:
        plain, visual = [t_formula, t_formula_back, t_tariffs, t_runner, t_conv_back], [t_speed, t_home_speed, t_tank, t_temp_rise]
    return _pick_t(plain, visual)
