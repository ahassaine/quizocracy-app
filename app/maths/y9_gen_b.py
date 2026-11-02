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
    x = random.randint(-8, 12)
    a, c = random.randint(3, 9), random.randint(1, 2)
    b = random.randint(-15, 15)
    e = (a - c) * x + b

    def t_both():
        return _tb("Solve  %s %s = %s %s" % (_k(a), _t(b), _k(c), _t(e)), x, "int", {},
                   ["%dx − %dx = %d − (%d)." % (a, c, e, b), "%dx = %d, x = %d." % (a - c, e - b, x)])

    def t_brackets():
        k, m = random.randint(2, 5), random.randint(-6, 6)
        rhs = k * (x + m) - 2 * x
        return _tb("Solve  %d(x %s) = 2x %s" % (k, _t(m), _t(rhs)), x, "int", {},
                   ["%dx %s = 2x %s." % (k, _t(k * m), _t(rhs)), "x = %d." % x])

    def t_two_brackets():
        p, q = random.randint(2, 5), random.randint(1, 4)
        if p == q:
            p += 1
        r, s2 = random.randint(-5, 5), random.randint(-5, 5)
        lhs_c, rhs_c = p * r, q * s2
        if (rhs_c - lhs_c) % (p - q):
            return t_both()
        xx = (rhs_c - lhs_c) // (p - q)
        return _tb("Solve  %d(x %s) = %d(x %s)" % (p, _t(r), q, _t(s2)), xx, "int", {},
                   ["%dx %s = %dx %s." % (p, _t(lhs_c), q, _t(rhs_c)), "x = %d." % xx])

    def t_negative_coef():
        k = random.randint(2, 6)
        return _tb("Solve  %d − %dx = %d" % (b, k, b - k * x), x, "int", {}, ["−%dx = %d, x = %d." % (k, -k * x, x)])

    def t_word():
        y = random.randint(3, 15)
        return _tb("I think of a number, multiply it by 5 and subtract 3. I get the same as when I multiply it by 2 and add %d. What is "
                   "the number?" % (3 * y - 3), y, "int", {}, ["5n − 3 = 2n + %d." % (3 * y - 3), "3n = %d, n = %d." % (3 * y, y)])

    return _pick_t([t_both, t_brackets, t_two_brackets, t_negative_coef, t_word])


@skill("Y9.2.b", "Equations with fractions and simple quadratics", S2)
def _(d=1):
    d = _d(d)

    def t_fraction():
        k, x = random.randint(2, 6), random.randint(-5, 12)
        c = random.randint(1, 9)
        return _tb("Solve  x/%d %s = %d" % (k, _t(c), x + c), k * x, "int", {}, ["x/%d = %d, so x = %d." % (k, x, k * x)])

    def t_both_frac():
        a, b = pick([(2, 3), (3, 4), (2, 5), (4, 5)])
        x = a * b * random.randint(1, 6)
        return _tb("Solve  x/%d + x/%d = %d" % (a, b, x // a + x // b), x, "int", {},
                   ["Multiply by %d: %dx + %dx = %d." % (a * b, b, a, (x // a + x // b) * a * b), "x = %d." % x])

    def t_square():
        k = random.randint(2, 15)
        return _tb("Solve x² = %d. Give the positive answer." % (k * k), k, "int", {}, ["x = ±%d." % k])

    def t_square_neg():
        k = random.randint(2, 12)
        return _tb("Solve x² = %d. Give the NEGATIVE answer." % (k * k), -k, "int", {}, ["x = ±%d." % k])

    def t_sq_linear():
        k, c = random.randint(2, 9), random.randint(1, 30)
        return _tb("Solve x² + %d = %d. Give the positive answer." % (c, k * k + c), k, "int", {}, ["x² = %d, x = %d." % (k * k, k)])

    def t_count():
        k = random.randint(1, 9)
        return _tb("How many solutions does x² = %d have?" % (k * k), 2, "int", {}, ["x = %d or x = −%d." % (k, k)])

    return _pick_t([t_fraction, t_both_frac, t_square, t_square_neg, t_sq_linear, t_count])


@skill("Y9.2.c", "Simultaneous linear equations", S2)
def _(d=1):
    d = _d(d)
    x, y = random.randint(-5, 9), random.randint(-5, 9)

    def t_add():
        a, b = random.randint(1, 4), random.randint(1, 5)
        return _tb("Solve:  %s + %s = %d  and  %s − %s = %d.  What is x?" % (_k(a), _k(b, "y"), a * x + b * y, _k(a), _k(b, "y"), a * x - b * y), x, "int", {},
                   ["Add them: %dx = %d." % (2 * a, 2 * a * x), "x = %d." % x])

    def t_find_y():
        a, b = random.randint(1, 4), random.randint(1, 5)
        return _tb("Solve:  %s + %s = %d  and  %s − %s = %d.  What is y?" % (_k(a), _k(b, "y"), a * x + b * y, _k(a), _k(b, "y"), a * x - b * y), y, "int", {},
                   ["Subtract them: %dy = %d." % (2 * b, 2 * b * y), "y = %d." % y])

    def t_subtract():
        a, b, c = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
        if a == c:
            c += 1
        return _tb("Solve:  %s + %s = %d  and  %s + %s = %d.  What is x?" % (_k(a), _k(b, "y"), a * x + b * y, _k(c), _k(b, "y"), c * x + b * y), x, "int", {},
                   ["Subtract: %dx = %d." % (a - c, (a - c) * x), "x = %d." % x])

    def t_substitute():
        m, c = random.randint(1, 4), random.randint(-5, 5)
        k = random.randint(1, 3)
        yy = m * x + c
        return _tb("y = %dx %s and x + %dy = %d. Find x." % (m, _t(c), k, x + k * yy), x, "int", {},
                   ["Substitute: x + %d(%dx %s) = %d." % (k, m, _t(c), x + k * yy), "x = %d." % x])

    def t_word():
        a, b = random.randint(2, 9), random.randint(2, 9)
        n1, n2 = random.randint(1, 5), random.randint(1, 5)
        m1, m2 = random.randint(1, 5), random.randint(1, 5)
        if n1 * m2 == n2 * m1:
            m2 += 1
        return _tb("%d pens and %d pencils cost %dp. %d pens and %d pencils cost %dp. How much is one pen, in pence?"
                   % (n1, m1, n1 * a * 10 + m1 * b * 10, n2, m2, n2 * a * 10 + m2 * b * 10), a * 10, "int", {"unit": "p"},
                   ["Solve the pair of equations: pen = %dp, pencil = %dp." % (a * 10, b * 10)])

    def t_check():
        a, b = random.randint(1, 5), random.randint(1, 5)
        cand = (x + pick([0, 1]), y)
        ok = a * cand[0] + b * cand[1] == a * x + b * y and cand[0] - cand[1] == x - y
        return _wq("Does x = %d, y = %d solve both  %s + %s = %d  and  x − y = %d ? (yes or no)" % (cand[0], cand[1], _k(a), _k(b, "y"), a * x + b * y, x - y),
                   "yes" if ok else "no", ["Substitute into both."], "yes / no")

    return _pick_t([t_add, t_find_y, t_subtract, t_substitute, t_word, t_check])


@skill("Y9.2.d", "Solve inequalities, including with negatives", S2)
def _(d=1):
    d = _d(d)
    x0 = random.randint(-6, 10)
    k = random.randint(2, 6)
    c = random.randint(-10, 10)

    def t_basic():
        return _tb("Solve  %dx %s > %d. The answer is x > ___ ." % (k, _t(c), k * x0 + c), x0, "int", {},
                   ["%dx > %d, x > %d." % (k, k * x0, x0)])

    def t_negative():
        return _wq("Solve  %d − %dx ≥ %d. Write the answer like x<=3." % (c, k, c - k * x0), "x<=%d" % x0,
                   ["−%dx ≥ %d." % (k, -k * x0), "Dividing by a negative flips the sign: x ≤ %d." % x0], "e.g. x<=3")

    def t_double():
        lo, hi = random.randint(-5, 3), random.randint(4, 12)
        return _tb("How many whole numbers satisfy  %d < 2x ≤ %d ?" % (2 * lo, 2 * hi), hi - lo, "int", {},
                   ["%d < x ≤ %d." % (lo, hi), "x = %s." % ", ".join(str(v) for v in range(lo + 1, hi + 1))])

    def t_largest():
        return _tb("x is a whole number and %dx %s < %d. What is the largest possible value of x?" % (k, _t(c), k * x0 + c + 1), x0, "int", {},
                   ["x < %s, so x = %d." % (_fs(Fraction(k * x0 + 1, k)), x0)])

    def t_line():
        op = pick(["<", "<=", ">", ">="])
        return {"prompt": "Write the inequality shown (like x>3, using <, >, <= or >=).", "component": "inequality_line",
                "spec": {"op": op, "value": x0, "min": x0 - 6, "max": x0 + 6}, "answer": "x%s%d" % (op, x0), "answer_type": "str",
                "solution": ["Open circle: < or >. Filled circle: ≤ or ≥."]}

    return _pick_t([t_basic, t_negative, t_double, t_largest], [t_line])


# ================================================================== 9.3 ======
@skill("Y9.3.a", "Gradient between two points", S3)
def _(d=1):
    d = _d(d)
    x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
    m = random.choice([v for v in range(-4, 5) if v])
    dx = random.randint(1, 4)
    x2, y2 = x1 + dx, y1 + m * dx

    def t_grad():
        return _tb("Find the gradient of the line through (%d,%d) and (%d,%d)." % (x1, y1, x2, y2), m, "int", {},
                   ["(%d − %s) ÷ (%d − %s) = %d." % (y2, "(%d)" % y1 if y1 < 0 else y1, x2, "(%d)" % x1 if x1 < 0 else x1, m)])

    def t_frac():
        a, b = random.randint(1, 5), random.randint(2, 5)
        if a % b == 0:
            a += 1
        return _fq("Find the gradient of the line through (0,0) and (%d,%d)." % (b, a), Fraction(a, b), ["Rise %d over run %d." % (a, b)])

    def t_steeper():
        m2 = random.choice([v for v in range(-6, 7) if v and abs(v) != abs(m)])
        return _wq("Which line is steeper: y = %dx + 1 or y = %dx − 2? Type the gradient of the steeper one." % (m, m2),
                   str(m if abs(m) > abs(m2) else m2), ["Compare the sizes of the gradients."], "a number")

    def t_graph():
        return {"prompt": "The line is drawn. What is its gradient?", "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "lines": [{"p1": [x1, y1], "p2": [x2, y2]}],
                         "points": [[x1, y1, "A"], [x2, y2, "B"]], "typed": True},
                "answer": m, "answer_type": "num", "solution": ["From A to B: up %d, across %d." % (m * dx, dx)]} \
            if all(-7 <= v <= 7 for v in (x1, y1, x2, y2)) else t_grad()

    return _pick_t([t_grad, t_frac, t_steeper], [t_graph])


@skill("Y9.3.b", "Equation of a straight line", S3)
def _(d=1):
    d = _d(d)
    m = random.choice([v for v in range(-4, 5) if v])
    c = random.randint(-6, 6)

    def t_two_points():
        x1, x2 = random.sample(range(-4, 5), 2)
        return _wq("Find the equation of the line through (%d,%d) and (%d,%d). Write it like y=2x+3." % (x1, m * x1 + c, x2, m * x2 + c),
                   _line(m, c), ["Gradient %d; substitute to get c = %d." % (m, c)], "e.g. y=2x+3")

    def t_point_grad():
        x1 = random.randint(-4, 4)
        return _wq("A line has gradient %d and passes through (%d,%d). Write its equation like y=2x+3." % (m, x1, m * x1 + c), _line(m, c),
                   ["c = %d − %d × %s = %d." % (m * x1 + c, m, "(%d)" % x1 if x1 < 0 else x1, c)], "e.g. y=2x+3")

    def t_parallel():
        c2 = c + random.randint(1, 5)
        return _wq("Write the equation of the line parallel to %s that crosses the y-axis at %d. Write it like y=2x+3."
                   % (_line(m, c), c2), _line(m, c2), ["Parallel lines share the gradient %d." % m], "e.g. y=2x+3")

    def t_rearrange():
        a = random.randint(2, 5)
        return _tb("Write %dy = %dx %s in the form y = mx + c. What is m?" % (a, a * m, _t(a * c)), m, "int", {}, ["Divide by %d." % a])

    def t_x_intercept():
        k = random.choice([v for v in range(-5, 6) if v])
        return _tb("Where does y = %dx %s cross the x-axis? Give the x-value." % (m, _t(-m * k)), k, "int", {},
                   ["Set y = 0: %dx = %d, x = %d." % (m, m * k, k)])

    return _pick_t([t_two_points, t_point_grad, t_parallel, t_rearrange, t_x_intercept])


@skill("Y9.3.c", "Quadratic graphs", S3)
def _(d=1):
    d = _d(d)
    p, q = random.randint(-5, 0), random.randint(1, 5)

    def t_table():
        b, c = -(p + q), p * q
        xs = [-2, -1, 0, 1, 2, 3]
        rows = [[x, x * x + b * x + c] for x in xs]
        k = random.randrange(len(xs))
        return _io("Complete the table for y = %s." % _poly_txt(b, c), rows, k, rows[k][1],
                   ["Substitute x = %d: y = %d." % (rows[k][0], rows[k][1])])

    def t_roots():
        b, c = -(p + q), p * q
        return _wq("Where does y = %s cross the x-axis? Write both x-values, smaller first, like -2, 3." % _poly_txt(b, c),
                   "%d, %d" % tuple(sorted([p, q])), ["It factorises to (x %s)(x %s)." % (_t(-p), _t(-q))], "e.g. -2, 3")

    def t_turning():
        h, k = random.choice([v for v in range(-4, 5) if v]), random.randint(-6, 6)
        return _wq("y = (x %s)² %s. Write the coordinates of the lowest point, like (2,-3)." % (_t(-h), _t(k)), "(%d,%d)" % (h, k),
                   ["The squared part is 0 when x = %d, giving y = %d." % (h, k)], "(x,y)")

    def t_y_intercept():
        b, c = random.randint(-6, 6), random.randint(-9, 9)
        return _tb("Where does y = %s cross the y-axis? Give the y-value." % _poly_txt(b, c), c, "int", {}, ["Put x = 0: y = %d." % c])

    def t_shape():
        return _wq("Is the graph of y = x² a straight line, a U-shaped curve or an S-shaped curve? (type straight, U or S)", "U",
                   ["Quadratic graphs are U-shaped (parabolas)."], "straight / U / S")

    return _pick_t([t_table, t_roots, t_turning, t_y_intercept, t_shape])


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
        speed, out_h = random.randint(2, 6) * 5, random.randint(1, 3)
        pts, dist = _journey(out_h, random.randint(1, 2), speed)
        return _lg("The graph shows a cycle ride (distance from home, in km, each hour). What was the speed on the way out, in km/h?",
                   pts, speed, ["%d km in %d h = %d km/h." % (dist, out_h, speed)], "km", "Time")

    def t_stop():
        speed, out_h, stop = random.randint(2, 6) * 5, random.randint(1, 3), random.randint(1, 2)
        pts, dist = _journey(out_h, stop, speed)
        return _lg("The graph shows a journey (distance from home each hour). For how many hours did the traveller stop?", pts, stop,
                   ["The flat part lasts %d hour%s." % (stop, "" if stop == 1 else "s")], "km", "Time")

    def t_formula():
        rate, fixed = random.randint(2, 9), random.randint(5, 30)
        h = random.randint(2, 8)
        return _tb("A plumber's charge is shown by a straight-line graph: £%d call-out plus £%d per hour. What does the line give for %d "
                   "hours, in pounds?" % (fixed, rate, h), fixed + rate * h, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (fixed, rate, h, fixed + rate * h)])

    def t_gradient_meaning():
        q, a = pick([("On a distance–time graph, what does the gradient show? (one word)", "speed"),
                     ("On a distance–time graph, what does a horizontal line show? (one word: the person is ...)", "stationary")])
        return _wq(q, a, ["Gradient = distance ÷ time."], "one word")

    def t_conversion():
        m = 5 * random.randint(2, 16)
        return _tb("A conversion graph shows 5 miles = 8 km. Use it to convert %d miles to km." % m, m // 5 * 8, "int", {"unit": "km"},
                   ["%d ÷ 5 × 8 = %d." % (m, m // 5 * 8)])

    return _pick_t([t_formula, t_gradient_meaning, t_conversion], [t_speed, t_stop])
