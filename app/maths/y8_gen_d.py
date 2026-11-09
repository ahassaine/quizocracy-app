# dev/app/logic/y8_gen_d.py — Year 8 generators: strands 8.6 and 8.7
#
# 8.6  Algebra: expressions, brackets & sequences        (Y8.6.a .. Y8.6.j)
# 8.7  Equations, inequalities & linear graphs           (Y8.7.a .. Y8.7.k)
#
# Each generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between many genuinely different framings.
#
# ALGEBRA answer-string policy (this is the Year-8 risk — read maths_engine.check_answer):
#   * The str checker lower-cases, turns '.,!?' and '-' into spaces, then COLLAPSES
#     whitespace.  So "6x - 8" == "6x-8" (the '-' becomes a space either way), BUT
#     "6x + 8" != "6x+8" — a '+' with spaces around it survives and breaks the match.
#   * Therefore: for every expression answer we (a) FAVOUR a numeric sub-answer where we
#     can (coefficient / constant / value / solution / gradient), (b) when the answer must
#     be an expression, we PIN a single canonical no-space spelling in the prompt with a
#     worked example, choose coefficients so there is exactly one natural spelling, and
#     store that exact no-space string as the answer.  _lin_str / _quad_str / _fac_str
#     build those canonical strings; _exprq appends the "no spaces, e.g. ..." instruction.
import random
from math import gcd
from .maths_engine import skill, pick, NAMES, n_words, ordinal

S6 = "8.6 Algebra: expressions, brackets & sequences"
S7 = "8.7 Equations, inequalities & linear graphs"


# ---------------------------------------------------------------- helpers ----
def _t(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_t(d)]


def _nz(lo, hi):
    v = random.randint(lo, hi)
    while v == 0:
        v = random.randint(lo, hi)
    return v


def _coprime_c(b, hic):
    """A c in 1..hic with gcd(b, c) == 1, so k(bx+c) is fully factorised. Bounded."""
    for _ in range(20):
        c = random.randint(1, hic)
        if gcd(b, c) == 1:
            return c
    return 1


# --- canonical expression-string builders (no spaces, x-term first) ----------
def _coef(c, var):
    """A single variable term: 3,'x'->'3x'; 1,'x'->'x'; -1,'x'->'-x'; 0->''"""
    if c == 0:
        return ""
    if c == 1:
        return var
    if c == -1:
        return "-" + var
    return "%d%s" % (c, var)


def _lin_str(a, b, var="x"):
    """Canonical 'ax+b' with no spaces, x-term first. Handles zeros/signs/units."""
    xt = _coef(a, var)
    if a == 0:
        return "%d" % b
    if b == 0:
        return xt
    return "%s%s%d" % (xt, "+" if b > 0 else "-", abs(b))


def _two_var_str(ca, va, cb, vb):
    """Canonical 'ca*va + cb*vb', e.g. 7,'a',2,'b' -> '7a+2b'. Both coeffs > 0."""
    ta, tb = _coef(ca, va), _coef(cb, vb)
    return "%s+%s" % (ta, tb)


def _quad_str(b, c):
    """Canonical 'x^2+bx+c' with no spaces (leading coefficient 1)."""
    s = "x^2"
    if b != 0:
        s += ("+" if b > 0 else "-") + (("%d" % abs(b)) if abs(b) != 1 else "") + "x"
    if c != 0:
        s += ("+" if c > 0 else "-") + "%d" % abs(c)
    return s


def _fac_str(k, a, b, var="x"):
    """Canonical factorised form 'k(ax+b)', e.g. 3,1,2 -> '3(x+2)'."""
    return "%d(%s)" % (k, _lin_str(a, b, var))


# --- question builders -------------------------------------------------------
def _numq(prompt, answer, solution, unit=None, placeholder=None,
          answer_type="int", tolerance=0):
    spec = {}
    if placeholder:
        spec["placeholder"] = placeholder
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _wordq(prompt, answer, solution, placeholder=None):
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder or "a word"},
            "answer": answer, "answer_type": "str", "tolerance": 0,
            "solution": solution}


def _exprq(prompt, answer, solution, example):
    """A pinned-format expression answer. The prompt gains an explicit no-space
    example, and `answer` is the matching canonical no-space string."""
    full = prompt + " Write your answer with no spaces (for example %s)." % example
    return {"prompt": full, "component": "number",
            "spec": {"text": True, "placeholder": "e.g. %s" % example},
            "answer": answer, "answer_type": "str", "tolerance": 0,
            "solution": solution}


def _setq(prompt, values, solution, placeholder="e.g. 2, 5, 8"):
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in values), "answer_type": "set",
            "tolerance": 0, "solution": solution}


def _dtq(prompt, headers, rows, answer, solution, missing=None, caption=None,
         answer_type="int"):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if caption:
        spec["caption"] = caption
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


def _gridq(prompt, x, y, solution, r=6, points=None, lines=None):
    spec = {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r, "ymax": r}
    if points:
        spec["points"] = points
    if lines:
        spec["lines"] = lines
    return {"prompt": prompt, "component": "coordinate_grid", "spec": spec,
            "answer": "(%d,%d)" % (x, y), "answer_type": "coord",
            "tolerance": 0, "solution": solution}


def _ioq(prompt, rows, missing, answer, solution, rule=None, placeholder=None):
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": "int", "tolerance": 0,
            "solution": solution}


def _seq_table(prompt, a, b, solution_prefix, caption="Sequence",
               header="Position (n)"):
    """A data_table of a linear sequence term = a*n + b, positions 1..5, one term
    hidden. Returns (question dict)."""
    ns = [1, 2, 3, 4, 5]
    i = random.randrange(5)
    ans = a * ns[i] + b
    rows = [[str(n), "" if n == ns[i] else str(a * n + b)] for n in ns]
    return _dtq(prompt, [header, "Term"], rows, ans,
                solution_prefix + ["Position %d: %d x %d %s = %d."
                                   % (ns[i], a, ns[i], _pm(b), ans)],
                missing=(i, 1), caption=caption)


def _pm(v):
    """'+ 3' / '- 3' for a constant term in a worked solution line."""
    return ("+ %d" % v) if v >= 0 else ("- %d" % -v)


def _br(v):
    """Bracket a negative number being multiplied: 3 -> '3', -2 -> '(-2)'."""
    return ("(%d)" % v) if v < 0 else ("%d" % v)


def _ineq_spec(op, value, lo, hi):
    return {"op": op, "value": int(value), "min": int(lo), "max": int(hi)}


def _ineqq(prompt, spec, answer, solution, answer_type="int", placeholder=None):
    s = dict(spec)
    if placeholder:
        s["placeholder"] = placeholder
    if answer_type == "str":
        s["text"] = True
    return {"prompt": prompt, "component": "inequality_line", "spec": s,
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


_OP_WORDS = {"<": "less than", "<=": "less than or equal to",
             ">": "greater than", ">=": "greater than or equal to"}


def _line_points(m, c, r):
    """Integer on-line points (x, mx+c) that lie inside a [-r, r] grid."""
    return [(x, m * x + c) for x in range(-r, r + 1) if -r <= m * x + c <= r]


# ===========================================================================
# 8.6  ALGEBRA
# ===========================================================================

# ----------------------------------------------------------------- 8.6.a -----
@skill("Y8.6.a", "Write expressions from words", S6)
def _(d=1):
    d = _t(d)
    v = pick(["n", "x", "t", "y", "m", "p"])
    k = _by_d(d, random.randint(2, 6), random.randint(2, 9), random.randint(3, 12))
    j = _by_d(d, random.randint(1, 6), random.randint(2, 12), random.randint(3, 20))
    ex = _lin_str(2, 5, v)

    def add():
        return _exprq("A number is called %s. Write an expression for %d more than %s."
                      % (v, j, v), _lin_str(1, j, v),
                      ["Adding %d gives %s." % (j, _lin_str(1, j, v))], ex)

    def subtract():
        return _exprq("A number is called %s. Write an expression for %d less than %s."
                      % (v, j, v), _lin_str(1, -j, v),
                      ["%d less than %s is %s." % (j, v, _lin_str(1, -j, v))], ex)

    def multiply():
        return _exprq("A number is called %s. Write an expression for %s multiplied by %d."
                      % (v, v, k), _coef(k, v),
                      ["%s multiplied by %d is %s." % (v, k, _coef(k, v))], ex)

    def times_add():
        return _exprq("A number is called %s. Write an expression for %d times %s, then add %d."
                      % (v, k, v, j), _lin_str(k, j, v),
                      ["%d times %s is %s, then add %d." % (k, v, _coef(k, v), j)], ex)

    def times_sub():
        return _exprq("A number is called %s. Write an expression for %d times %s, then subtract %d."
                      % (v, k, v, j), _lin_str(k, -j, v),
                      ["%d times %s is %s; subtracting %d gives %s."
                       % (k, v, _coef(k, v), j, _lin_str(k, -j, v))], ex)

    def perimeter_square():
        return _exprq("A square has sides of length %s cm. Write an expression for its "
                      "perimeter, in cm." % v, _coef(4, v),
                      ["A square has 4 equal sides: 4 x %s = %s." % (v, _coef(4, v))], ex)

    def cost():
        name = pick(NAMES)
        return _exprq("One ticket costs %s pounds. Write an expression for the cost of %d "
                      "tickets that %s buys, in pounds." % (v, k, name), _coef(k, v),
                      ["%d tickets at %s pounds each cost %s." % (k, v, _coef(k, v))], ex)

    def age():
        name = pick(NAMES)
        return _exprq("%s is %s years old now. Write an expression for %s's age in %d "
                      "%s time." % (name, v, name, j, "year's" if j == 1 else "years'"), _lin_str(1, j, v),
                      ["In %d years %s will be %s." % (j, name, _lin_str(1, j, v))], ex)

    def consecutive():
        return _exprq("A whole number is %s. Write an expression for the next whole number "
                      "after %s." % (v, v), _lin_str(1, 1, v),
                      ["The next whole number is %s." % _lin_str(1, 1, v)], ex)

    def rectangle_perim():
        return _exprq("A rectangle is %s cm long and %d cm wide. Write an expression for "
                      "its perimeter, in cm." % (v, j), _lin_str(2, 2 * j, v),
                      ["Perimeter = 2 x length + 2 x width = %s." % _lin_str(2, 2 * j, v)], ex)

    def total_lots():
        return _exprq("Write an expression for %d lots of %s added to %d."
                      % (k, v, j), _lin_str(k, j, v),
                      ["%d lots of %s is %s, plus %d." % (k, v, _coef(k, v), j)], ex)

    def coeff_of():
        return _numq("A number is %s. An expression for '%d times %s then add %d' is written "
                     "in the form (coefficient)%s + (number). What is the coefficient of %s?"
                     % (v, k, v, j, v, v), k,
                     ["'%d times %s' gives a coefficient of %d." % (k, v, k)],
                     placeholder="a number")

    opts = [add, subtract, multiply, times_add, times_sub, perimeter_square,
            cost, age, consecutive, rectangle_perim, total_lots, coeff_of]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.b -----
@skill("Y8.6.b", "Substitute and evaluate expressions", S6)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 6, 10, 12)

    def linear():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        x = random.randint(2, hi)
        return _numq("Work out the value of %s when %s = %d."
                     % (_lin_str(a, b), "x", x), a * x + b,
                     ["%d x %d + %d = %d." % (a, x, b, a * x + b)])

    def linear_neg():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        x = _nz(-hi, -1)
        return _numq("Work out the value of %s when x = %d." % (_lin_str(a, b), x),
                     a * x + b,
                     ["%d x (%d) = %d, then + %d = %d." % (a, x, a * x, b, a * x + b)])

    def two_var():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        A = random.randint(2, hi)
        B = random.randint(2, hi)
        return _numq("Work out the value of %sa + %sb when a = %d and b = %d."
                     % (a, b, A, B), a * A + b * B,
                     ["%d x %d + %d x %d = %d + %d = %d."
                      % (a, A, b, B, a * A, b * B, a * A + b * B)])

    def product():
        A = random.randint(2, hi)
        B = random.randint(2, hi)
        k = random.randint(2, 5)
        return _numq("Work out the value of %dxy when x = %d and y = %d." % (k, A, B),
                     k * A * B,
                     ["%d x %d x %d = %d." % (k, A, B, k * A * B)])

    def square():
        x = random.randint(2, hi)
        return _numq("Work out the value of x^2 when x = %d." % x, x * x,
                     ["%d^2 = %d x %d = %d." % (x, x, x, x * x)])

    def square_plus():
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Work out the value of x^2 + %d when x = %d." % (b, x), x * x + b,
                     ["%d^2 = %d, then + %d = %d." % (x, x * x, b, x * x + b)])

    def coef_square():
        k = random.randint(2, 4)
        x = random.randint(2, hi)
        return _numq("Work out the value of %dx^2 when x = %d." % (k, x), k * x * x,
                     ["%d^2 = %d, then x %d = %d." % (x, x * x, k, k * x * x)])

    def cube():
        x = random.randint(2, _by_d(d, 4, 5, 6))
        return _numq("Work out the value of x^3 when x = %d." % x, x ** 3,
                     ["%d^3 = %d x %d x %d = %d." % (x, x, x, x, x ** 3)])

    def bracket_square():
        x = random.randint(1, hi)
        b = random.randint(1, 5)
        return _numq("Work out the value of (x + %d)^2 when x = %d." % (b, x),
                     (x + b) ** 2,
                     ["x + %d = %d, then %d^2 = %d." % (b, x + b, x + b, (x + b) ** 2)])

    def formula_area():
        L = random.randint(3, hi)
        W = random.randint(2, hi)
        return _numq("The area of a rectangle is A = lw. Work out A when l = %d and "
                     "w = %d." % (L, W), L * W,
                     ["A = %d x %d = %d." % (L, W, L * W)], unit="square units")

    def three_terms():
        a = random.randint(2, 5)
        b = random.randint(2, 6)
        c = random.randint(1, hi)
        x = random.randint(2, 6)
        y = random.randint(2, 6)
        return _numq("Work out the value of %da + %db - %d when a = %d and b = %d."
                     % (a, b, c, x, y), a * x + b * y - c,
                     ["%d x %d + %d x %d - %d = %d."
                      % (a, x, b, y, c, a * x + b * y - c)])

    def divide():
        x = random.randint(2, 9) * random.randint(2, 6)
        k = pick([d2 for d2 in range(2, 10) if x % d2 == 0])
        b = random.randint(1, hi)
        return _numq("Work out the value of x/%d + %d when x = %d." % (k, b, x),
                     x // k + b,
                     ["%d / %d = %d, then + %d = %d." % (x, k, x // k, b, x // k + b)])

    def io_machine():
        a = random.randint(2, 5)
        b = random.randint(1, hi)
        xs = sorted(random.sample(range(1, 10), 4))
        i = random.randrange(4)
        rows = [[x, a * x + b] for x in xs]
        return _ioq("Each output is found from the input using the expression %s, where "
                    "x is the input. Type the missing output." % _lin_str(a, b),
                    rows, i, a * xs[i] + b,
                    ["Substitute x = %d: %d x %d + %d = %d."
                     % (xs[i], a, xs[i], b, a * xs[i] + b)],
                    rule=_lin_str(a, b))

    opts = [linear, two_var, product, square, square_plus, coef_square, cube,
            bracket_square, formula_area, three_terms, divide, io_machine]
    if d == 0:
        opts = [linear, two_var, product, square, formula_area, divide,
                square_plus, three_terms, io_machine]
    elif d == 2:
        opts = [linear_neg, two_var, coef_square, cube, bracket_square,
                three_terms, square_plus, product, divide, io_machine]
    opts = opts + [io_machine, io_machine]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.c -----
@skill("Y8.6.c", "Collect and simplify like terms", S6)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 6, 9, 12)

    def x_and_const():
        a1 = random.randint(2, hi)
        a2 = random.randint(1, hi)
        c1 = random.randint(1, hi)
        c2 = random.randint(1, hi)
        a, c = a1 + a2, c1 + c2
        expr = "%s + %d + %s + %d" % (_coef(a1, "x"), c1, _coef(a2, "x"), c2)
        return _exprq("Simplify %s by collecting like terms." % expr, _lin_str(a, c),
                      ["Add the x terms: %d + %d = %d." % (a1, a2, a),
                       "Add the numbers: %d + %d = %d." % (c1, c2, c),
                       "So %s = %s." % (expr, _lin_str(a, c))], "5x+6")

    def x_subtract():
        a1 = random.randint(4, hi + 3)
        a2 = random.randint(1, a1 - 1)
        c = random.randint(1, hi)
        expr = "%s + %d - %s" % (_coef(a1, "x"), c, _coef(a2, "x"))
        return _exprq("Simplify %s by collecting like terms." % expr,
                      _lin_str(a1 - a2, c),
                      ["The x terms: %d - %d = %d." % (a1, a2, a1 - a2),
                       "So %s = %s." % (expr, _lin_str(a1 - a2, c))], "5x+6")

    def two_var():
        ca1 = random.randint(2, hi)
        ca2 = random.randint(1, hi)
        cb1 = random.randint(2, hi)
        cb2 = random.randint(1, hi)
        expr = "%s + %s + %s + %s" % (_coef(ca1, "a"), _coef(cb1, "b"),
                                      _coef(ca2, "a"), _coef(cb2, "b"))
        ans = _two_var_str(ca1 + ca2, "a", cb1 + cb2, "b")
        return _exprq("Simplify %s by collecting like terms." % expr, ans,
                      ["a terms: %d + %d = %d." % (ca1, ca2, ca1 + ca2),
                       "b terms: %d + %d = %d." % (cb1, cb2, cb1 + cb2),
                       "So %s = %s." % (expr, ans)], "7a+2b")

    def count_x():
        a1 = random.randint(2, hi)
        a2 = random.randint(1, hi)
        a3 = random.randint(1, hi)
        return _numq("When %s + %s + %s is simplified, how many x are there (what is the "
                     "coefficient of x)?"
                     % (_coef(a1, "x"), _coef(a2, "x"), _coef(a3, "x")),
                     a1 + a2 + a3,
                     ["%d + %d + %d = %d." % (a1, a2, a3, a1 + a2 + a3)],
                     placeholder="coefficient of x")

    def const_after():
        a = random.randint(2, hi)
        c1 = random.randint(1, hi)
        c2 = random.randint(1, hi)
        return _numq("When %s + %d + %d is simplified, what is the constant term (the "
                     "number on its own)?" % (_coef(a, "x"), c1, c2), c1 + c2,
                     ["The numbers add: %d + %d = %d." % (c1, c2, c1 + c2)],
                     placeholder="a number")

    def perimeter_collect():
        a = random.randint(1, 4)
        b = random.randint(1, 4)
        expr = "sides %s, %s, %s and %s cm" % (_coef(a, "x"), _lin_str(1, b),
                                               _coef(a, "x"), _lin_str(1, b))
        return _exprq("A rectangle has %s. Write a simplified expression for its "
                      "perimeter, in cm." % expr, _lin_str(2 * a, 2 * b),
                      ["Add all four sides and collect like terms: %s."
                       % _lin_str(2 * a, 2 * b)], "5x+6")

    def three_x_terms():
        a1 = random.randint(3, hi)
        a2 = random.randint(1, a1 - 1)
        a3 = random.randint(1, 3)
        c = random.randint(1, hi)
        expr = "%s - %s + %s + %d" % (_coef(a1, "x"), _coef(a2, "x"),
                                      _coef(a3, "x"), c)
        return _exprq("Simplify %s by collecting like terms." % expr,
                      _lin_str(a1 - a2 + a3, c),
                      ["x terms: %d - %d + %d = %d." % (a1, a2, a3, a1 - a2 + a3),
                       "So %s = %s." % (expr, _lin_str(a1 - a2 + a3, c))], "5x+6")

    def xsq_and_x():
        p = random.randint(2, 4)
        q = random.randint(1, 3)
        a1 = random.randint(2, hi)
        a2 = random.randint(1, hi)
        ans = "%s+%s" % (_coef(p + q, "x^2"), _coef(a1 + a2, "x"))
        expr = "%s + %s + %s + %s" % (_coef(p, "x^2"), _coef(a1, "x"),
                                      _coef(q, "x^2"), _coef(a2, "x"))
        return _exprq("Simplify %s by collecting like terms." % expr, ans,
                      ["x^2 terms: %d + %d = %d." % (p, q, p + q),
                       "x terms: %d + %d = %d." % (a1, a2, a1 + a2),
                       "So the answer is %s." % ans], "3x^2+5x")

    def already_simplified():
        a = random.randint(2, hi)
        c = random.randint(1, hi)
        if random.random() < 0.5:
            a2 = random.randint(1, a - 1)
            messy = "%s + %d + %s" % (_coef(a - a2, "x"), c, _coef(a2, "x"))
            return _wordq("Is the expression %s already fully simplified (are there no "
                          "like terms left to collect)? Type yes or no." % messy, "no",
                          ["%s and %s are like terms, so it simplifies to %s."
                           % (_coef(a - a2, "x"), _coef(a2, "x"), _lin_str(a, c))],
                          placeholder="yes or no")
        return _wordq("Is the expression %s already fully simplified (are there no like "
                      "terms left to collect)? Type yes or no." % _lin_str(a, c), "yes",
                      ["%s has one x term and one number, so it is fully simplified."
                       % _lin_str(a, c)], placeholder="yes or no")

    def terms_and_coefficients():
        # Identify terms and coefficients: coefficient of x, coefficient of x^2,
        # or the number of terms in an expression.
        p = random.randint(2, 5)
        a = random.randint(2, hi)
        c = random.randint(1, hi)
        three = random.random() < 0.5
        if three:
            expr = "%s + %s + %d" % (_coef(p, "x^2"), _coef(a, "x"), c)
            terms = 3
        else:
            expr = "%s + %d" % (_coef(a, "x"), c)
            terms = 2
        ask = pick(["coef_x", "terms"] + (["coef_x2"] if three else []))
        if ask == "coef_x":
            return _numq("Identify terms and coefficients in the expression %s. What is "
                         "the coefficient of x (the number multiplying x)?" % expr, a,
                         ["The x term is %s, so its coefficient is %d." % (_coef(a, "x"), a)],
                         placeholder="coefficient of x")
        if ask == "coef_x2":
            return _numq("Identify terms and coefficients in the expression %s. What is "
                         "the coefficient of x^2?" % expr, p,
                         ["The x^2 term is %s, so its coefficient is %d." % (_coef(p, "x^2"), p)],
                         placeholder="coefficient of x^2")
        return _numq("Identify terms and coefficients in the expression %s. How many "
                     "terms does it have (terms are separated by + or - signs)?"
                     % expr, terms,
                     ["The terms are separated by + signs, giving %d terms." % terms],
                     placeholder="number of terms")

    opts = [x_and_const, x_subtract, two_var, count_x, const_after,
            perimeter_collect, three_x_terms, already_simplified,
            terms_and_coefficients]
    if d == 2:
        opts = [x_subtract, two_var, three_x_terms, xsq_and_x, count_x,
                const_after, perimeter_collect, terms_and_coefficients]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.d -----
@skill("Y8.6.d", "Expand a single bracket", S6)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 5, 9, 12)

    def basic():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        c = random.randint(1, hi)
        return _exprq("Expand %d(%s)." % (a, _lin_str(b, c)),
                      _lin_str(a * b, a * c),
                      ["%d x %s = %s and %d x %d = %d."
                       % (a, _coef(b, "x"), _coef(a * b, "x"), a, c, a * c),
                       "So %d(%s) = %s." % (a, _lin_str(b, c), _lin_str(a * b, a * c))],
                      "6x+8")

    def with_minus():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        c = random.randint(1, hi)
        return _exprq("Expand %d(%s)." % (a, _lin_str(b, -c)),
                      _lin_str(a * b, -a * c),
                      ["%d x %s = %s and %d x (-%d) = -%d."
                       % (a, _coef(b, "x"), _coef(a * b, "x"), a, c, a * c),
                       "So the answer is %s." % _lin_str(a * b, -a * c)], "6x-8")

    def x_outside():
        b = random.randint(1, hi)
        c = random.randint(1, hi)
        ans = "%s+%s" % (_coef(b, "x^2"), _coef(c, "x"))
        return _exprq("Expand x(%s)." % _lin_str(b, c), ans,
                      ["x times %s gives %s, and x times %d gives %s."
                       % (_coef(b, "x"), _coef(b, "x^2"), c, _coef(c, "x")),
                       "So x(%s) = %s." % (_lin_str(b, c), ans)], "x^2+3x")

    def coeff_of_x():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(1, hi)
        return _numq("Expand %d(%s). What is the coefficient of x in the answer?"
                     % (a, _lin_str(b, c)), a * b,
                     ["%d x %d = %d." % (a, b, a * b)], placeholder="coefficient of x")

    def const_term():
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(1, hi)
        return _numq("Expand %d(%s). What is the constant term (the number on its own) in "
                     "the answer?" % (a, _lin_str(b, c)), a * c,
                     ["%d x %d = %d." % (a, c, a * c)], placeholder="a number")

    def evaluate_after():
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        c = random.randint(1, 5)
        x = random.randint(2, 6)
        return _numq("Expand %d(%s) and then work out its value when x = %d."
                     % (a, _lin_str(b, c), x), a * (b * x + c),
                     ["%d(%s) = %s." % (a, _lin_str(b, c), _lin_str(a * b, a * c)),
                      "When x = %d: %d x %d + %d = %d."
                      % (x, a * b, x, a * c, a * (b * x + c))])

    def area_expand():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        return _exprq("A rectangle is %d cm wide and (%s) cm long. Write a simplified "
                      "expression for its area, in square cm." % (a, _lin_str(1, b)),
                      _lin_str(a, a * b),
                      ["Area = %d(%s) = %s." % (a, _lin_str(1, b), _lin_str(a, a * b))],
                      "6x+8")

    def expand_two():
        a1 = random.randint(2, 5)
        b1 = random.randint(1, 5)
        c1 = random.randint(1, 5)
        a2 = random.randint(1, 4)
        d2 = random.randint(1, 5)
        # a1(b1 x + c1) + a2(x + d2), collected, guaranteed positive
        A = a1 * b1 + a2
        C = a1 * c1 + a2 * d2
        return _exprq("Expand and simplify %d(%s) + %d(%s)."
                      % (a1, _lin_str(b1, c1), a2, _lin_str(1, d2)),
                      _lin_str(A, C),
                      ["%d(%s) = %s." % (a1, _lin_str(b1, c1), _lin_str(a1 * b1, a1 * c1)),
                       "%d(%s) = %s." % (a2, _lin_str(1, d2), _lin_str(a2, a2 * d2)),
                       "Collecting: %s." % _lin_str(A, C)], "6x+8")

    def distributive_property():
        # Multiply using the distributive property (name it explicitly).
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        c = random.randint(1, hi)
        return _exprq("Multiply using the distributive property: expand %d(%s) by "
                      "multiplying the %d by each term inside the bracket."
                      % (a, _lin_str(b, c), a), _lin_str(a * b, a * c),
                      ["%d x %s = %s and %d x %d = %d."
                       % (a, _coef(b, "x"), _coef(a * b, "x"), a, c, a * c),
                       "So %d(%s) = %s."
                       % (a, _lin_str(b, c), _lin_str(a * b, a * c))], "6x+8")

    def distributive_coeff():
        # Distributive property, numeric answer (coefficient of x).
        a = random.randint(2, hi)
        b = random.randint(2, hi)
        c = random.randint(1, hi)
        return _numq("Multiply using the distributive property: expand %d(%s). What is "
                     "the coefficient of x in the answer?" % (a, _lin_str(b, c)), a * b,
                     ["The distributive property multiplies %d by %s, giving %d x."
                      % (a, _coef(b, "x"), a * b)], placeholder="coefficient of x")

    def area_model_expand():
        # Multiply using the distributive property with an AREA MODEL.
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        return _exprq("Multiply using the distributive property with an area model. A "
                      "rectangle has width %d and length (%s). Find the area of each "
                      "part of the model and add them to expand %d(%s)."
                      % (a, _lin_str(1, b), a, _lin_str(1, b)), _lin_str(a, a * b),
                      ["The area model splits into %d x %s = %s and %d x %d = %d."
                       % (a, "x", _coef(a, "x"), a, b, a * b),
                       "Adding the parts: %s." % _lin_str(a, a * b)], "6x+8")

    def area_model_part():
        # Area model, numeric answer: total area for given x.
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        x = random.randint(2, 6)
        return _numq("An area model for the distributive property shows a rectangle of "
                     "width %d and length (%s). Work out the total area when x = %d."
                     % (a, _lin_str(1, b), x), a * (x + b),
                     ["Length = %d + %d = %d, so area = %d x %d = %d."
                      % (x, b, x + b, a, x + b, a * (x + b))], unit="square units")

    opts = [basic, with_minus, x_outside, coeff_of_x, const_term,
            evaluate_after, area_expand, distributive_property, distributive_coeff,
            area_model_expand, area_model_part]
    if d == 0:
        opts = [basic, coeff_of_x, const_term, area_expand, evaluate_after,
                distributive_property, distributive_coeff, area_model_expand,
                area_model_part]
    elif d == 2:
        opts = [with_minus, x_outside, expand_two, coeff_of_x, evaluate_after,
                basic, distributive_property, area_model_expand]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.e -----
@skill("Y8.6.e", "Factorise into a single bracket", S6)
def _(d=1):
    d = _t(d)

    def basic():
        k = _by_d(d, random.randint(2, 4), random.randint(2, 6), random.randint(3, 9))
        b = random.randint(2, _by_d(d, 5, 8, 10))
        c = _coprime_c(b, _by_d(d, 5, 8, 10))
        return _exprq("Factorise %s by taking out the highest common factor."
                      % _lin_str(k * b, k * c), _fac_str(k, b, c),
                      ["The highest common factor of %d and %d is %d."
                       % (k * b, k * c, k),
                       "%s = %s." % (_lin_str(k * b, k * c), _fac_str(k, b, c))],
                      "3(x+2)")

    def simple_x():
        k = _by_d(d, random.randint(2, 4), random.randint(2, 6), random.randint(3, 9))
        c = random.randint(1, _by_d(d, 5, 8, 10))
        return _exprq("Factorise %s by taking out the highest common factor."
                      % _lin_str(k, k * c), _fac_str(k, 1, c),
                      ["Both terms divide by %d." % k,
                       "%s = %s." % (_lin_str(k, k * c), _fac_str(k, 1, c))], "3(x+2)")

    def find_hcf():
        k = random.randint(2, 8)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        return _numq("To factorise %s you take out the highest common factor. What is "
                     "that highest common factor?" % _lin_str(k * b, k * c), k,
                     ["%d and %d both divide by %d." % (k * b, k * c, k)],
                     placeholder="the HCF")

    def inside_first():
        k = random.randint(2, 8)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        return _numq("%s factorises to %d(ax + b). What is the coefficient of x inside "
                     "the bracket (the value of a)?" % (_lin_str(k * b, k * c), k), b,
                     ["%d divided by %d is %d." % (k * b, k, b)], placeholder="a number")

    def inside_const():
        k = random.randint(2, 8)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        return _numq("%s factorises to %d(%s + b). What is the number b inside the "
                     "bracket?" % (_lin_str(k * b, k * c), k, _coef(b, "x")), c,
                     ["%d divided by %d is %d." % (k * c, k, c)], placeholder="a number")

    def x_factor():
        b = random.randint(2, 8)
        c = _coprime_c(b, 8)
        # bx^2 + cx  -> x(bx + c); b and c coprime so x is the whole common factor
        expr = "%s+%s" % (_coef(b, "x^2"), _coef(c, "x"))
        return _exprq("Factorise %s by taking out the common factor x." % expr,
                      "x(%s)" % _lin_str(b, c),
                      ["Both terms have a factor of x.",
                       "%s = x(%s)." % (expr, _lin_str(b, c))], "x(3x+2)")

    def check_factor():
        k = random.randint(2, 6)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        if random.random() < 0.5:
            return _wordq("Is %d(%s) the fully factorised form of %s? Type yes or no."
                          % (k, _lin_str(2 * b, 2 * c), _lin_str(2 * k * b, 2 * k * c)),
                          "no",
                          ["The highest common factor of %d and %d is %d, not %d."
                           % (2 * k * b, 2 * k * c, 2 * k, k),
                           "Fully factorised: %s = %s."
                           % (_lin_str(2 * k * b, 2 * k * c), _fac_str(2 * k, b, c))],
                          placeholder="yes or no")
        return _wordq("Is %d(%s) the fully factorised form of %s? Type yes or no."
                      % (k, _lin_str(b, c), _lin_str(k * b, k * c)), "yes",
                      ["Expanding %d(%s) gives %s, so yes."
                       % (k, _lin_str(b, c), _lin_str(k * b, k * c))],
                      placeholder="yes or no")

    def not_fully():
        # 2(2x+4) should be 4(x+2); ask for the HIGHEST common factor
        b = random.randint(1, 4)
        c = _coprime_c(b, 4)
        k = random.randint(2, 4) * 2
        return _numq("A pupil writes %s = 2(%s), but this is not fully factorised. What "
                     "is the highest common factor that should be taken out instead?"
                     % (_lin_str(k * b, k * c), _lin_str(k * b // 2, k * c // 2)), k,
                     ["Both %d and %d divide by %d, not just 2."
                      % (k * b, k * c, k)], placeholder="the HCF")

    def area_model_factorise():
        # Factorise linear expressions using an area model (rectangle).
        k = _by_d(d, random.randint(2, 4), random.randint(2, 6), random.randint(3, 9))
        b = random.randint(2, _by_d(d, 5, 8, 10))
        c = _coprime_c(b, _by_d(d, 5, 8, 10))  # coprime -> fully factorised, one form
        return _exprq("Factorise using an area model. A rectangle has area %s and one "
                      "side of length %d. Factorise %s, writing it as %d times a "
                      "bracket." % (_lin_str(k * b, k * c), k,
                                    _lin_str(k * b, k * c), k), _fac_str(k, b, c),
                      ["The area model has width %d, so divide each term by %d."
                       % (k, k),
                       "%s = %s." % (_lin_str(k * b, k * c), _fac_str(k, b, c))],
                      "3(x+2)")

    def sort_factors():
        # Sort factors of expressions: find the highest common factor to take out.
        k = random.randint(2, 8)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        t1, t2 = k * b, k * c
        hcf = gcd(t1, t2)  # exact HCF (equals k because b, c are coprime)
        return _numq("Sort the factors of the expression %s. The two terms share common "
                     "factors; what is the highest common factor that can be taken "
                     "outside a bracket?" % _lin_str(t1, t2), hcf,
                     ["%d and %d share the common factor %d, which is the highest."
                      % (t1, t2, hcf)], placeholder="the HCF")

    def area_model_side():
        # Area model, numeric: the missing side length inside the bracket.
        k = random.randint(2, 6)
        b = random.randint(2, 6)
        c = _coprime_c(b, 6)
        return _numq("An area model shows a rectangle with area %s. One side has length "
                     "%d. The other side is (ax + b); what is the value of a (the "
                     "coefficient of x on that side)?"
                     % (_lin_str(k * b, k * c), k), b,
                     ["The x term of the area is %s, and %d x a = %d, so a = %d."
                      % (_coef(k * b, "x"), k, k * b, b)],
                     placeholder="coefficient of x")

    opts = [basic, simple_x, find_hcf, inside_first, inside_const,
            check_factor, x_factor, area_model_factorise, sort_factors,
            area_model_side]
    if d == 0:
        opts = [basic, simple_x, find_hcf, inside_const, check_factor,
                sort_factors, area_model_side]
    elif d == 2:
        opts = [basic, x_factor, inside_first, inside_const, not_fully, find_hcf,
                area_model_factorise, sort_factors]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.f -----
@skill("Y8.6.f", "Expand and simplify double brackets", S6)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 5, 7, 9)

    def basic():
        p = random.randint(1, hi)
        q = random.randint(1, hi)
        return _exprq("Expand and simplify (%s)(%s)."
                      % (_lin_str(1, p), _lin_str(1, q)),
                      _quad_str(p + q, p * q),
                      ["x times x = x^2; the x terms are %s and %s."
                       % (_coef(p, "x"), _coef(q, "x")),
                       "(%s)(%s) = %s."
                       % (_lin_str(1, p), _lin_str(1, q), _quad_str(p + q, p * q))],
                      "x^2+5x+6")

    def square_bracket():
        p = random.randint(1, hi)
        return _exprq("Expand and simplify (%s)^2." % _lin_str(1, p),
                      _quad_str(2 * p, p * p),
                      ["(%s)^2 = (%s)(%s)."
                       % (_lin_str(1, p), _lin_str(1, p), _lin_str(1, p)),
                       "= %s." % _quad_str(2 * p, p * p)], "x^2+6x+9")

    def coeff_x():
        p = random.randint(1, hi)
        q = random.randint(1, hi)
        return _numq("Expand (%s)(%s). What is the coefficient of x in the simplified "
                     "answer?" % (_lin_str(1, p), _lin_str(1, q)), p + q,
                     ["The x terms are %s and %s, giving %s."
                      % (_coef(p, "x"), _coef(q, "x"), _coef(p + q, "x"))],
                     placeholder="coefficient of x")

    def const_term():
        p = random.randint(1, hi)
        q = random.randint(1, hi)
        return _numq("Expand (%s)(%s). What is the constant term (the number on its own) "
                     "in the answer?" % (_lin_str(1, p), _lin_str(1, q)), p * q,
                     ["%d x %d = %d." % (p, q, p * q)], placeholder="a number")

    def diff_squares():
        p = random.randint(2, hi)
        return _exprq("Expand and simplify (%s)(%s)."
                      % (_lin_str(1, p), _lin_str(1, -p)),
                      _quad_str(0, -p * p),
                      ["The x terms cancel: +%dx and -%dx give 0." % (p, p),
                       "= %s." % _quad_str(0, -p * p)], "x^2-9")

    def with_minus():
        p = random.randint(1, hi)
        q = random.randint(1, hi)
        # (x+p)(x-q) -> x^2 + (p-q)x - pq, keep p>q so middle positive
        if p <= q:
            p, q = q + 1, p if p < q else 1
        b = p - q
        return _exprq("Expand and simplify (%s)(%s)."
                      % (_lin_str(1, p), _lin_str(1, -q)),
                      _quad_str(b, -p * q),
                      ["x terms: +%dx and -%dx give %dx." % (p, q, b),
                       "= %s." % _quad_str(b, -p * q)], "x^2+2x-8")

    def evaluate_after():
        p = random.randint(1, 4)
        q = random.randint(1, 4)
        x = random.randint(2, 5)
        val = (x + p) * (x + q)
        return _numq("Expand (%s)(%s), then find its value when x = %d."
                     % (_lin_str(1, p), _lin_str(1, q), x), val,
                     ["The expansion is %s." % _quad_str(p + q, p * q),
                      "When x = %d: %d + %d + %d = %d."
                      % (x, x * x, (p + q) * x, p * q, val)])

    def area_double():
        p = random.randint(1, hi)
        q = random.randint(1, hi)
        return _exprq("A rectangle is (%s) cm long and (%s) cm wide. Write a simplified "
                      "expression for its area, in square cm."
                      % (_lin_str(1, p), _lin_str(1, q)), _quad_str(p + q, p * q),
                      ["Area = (%s)(%s) = %s."
                       % (_lin_str(1, p), _lin_str(1, q), _quad_str(p + q, p * q))],
                      "x^2+5x+6")

    opts = [basic, square_bracket, coeff_x, const_term, area_double, evaluate_after]
    if d == 2:
        opts = [basic, square_bracket, diff_squares, with_minus, coeff_x,
                area_double, evaluate_after]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.g -----
@skill("Y8.6.g", "Equivalent expressions", S6)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 5, 8, 10)

    def bracket_yesno():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        if random.random() < 0.5:
            return _wordq("Are %d(%s) and %s equivalent expressions? Type yes or no."
                          % (a, _lin_str(1, b), _lin_str(a, a * b)), "yes",
                          ["%d(%s) expands to %s, so they are equivalent."
                           % (a, _lin_str(1, b), _lin_str(a, a * b))],
                          placeholder="yes or no")
        off = pick([1, 2, 3])
        return _wordq("Are %d(%s) and %s equivalent expressions? Type yes or no."
                      % (a, _lin_str(1, b), _lin_str(a, a * b + off)), "no",
                      ["%d(%s) expands to %s, not %s."
                       % (a, _lin_str(1, b), _lin_str(a, a * b),
                          _lin_str(a, a * b + off))], placeholder="yes or no")

    def collect_yesno():
        a1 = random.randint(2, hi)
        a2 = random.randint(1, hi)
        c = random.randint(1, hi)
        if random.random() < 0.5:
            bad = a1 * a2 if a1 * a2 != a1 + a2 else a1 + a2 + 1
            return _wordq("Are %s + %s + %d and %s equivalent? Type yes or no."
                          % (_coef(a1, "x"), _coef(a2, "x"), c, _lin_str(bad, c)), "no",
                          ["Collecting like terms: %s + %s = %s, not %s."
                           % (_coef(a1, "x"), _coef(a2, "x"), _coef(a1 + a2, "x"),
                              _coef(bad, "x")),
                           "So they are not equivalent."], placeholder="yes or no")
        return _wordq("Are %s + %s + %d and %s equivalent? Type yes or no."
                      % (_coef(a1, "x"), _coef(a2, "x"), c,
                         _lin_str(a1 + a2, c)), "yes",
                      ["Collecting like terms: %s + %s = %s."
                       % (_coef(a1, "x"), _coef(a2, "x"), _coef(a1 + a2, "x")),
                       "So they are equivalent."], placeholder="yes or no")

    def missing_in_bracket():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Fill in the missing number: %d(x + ___) = %s."
                     % (a, _lin_str(a, a * b)), b,
                     ["%d divided by %d is %d." % (a * b, a, b)],
                     placeholder="a number")

    def missing_factor():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Fill in the missing number: ___(x + %d) = %s."
                     % (b, _lin_str(a, a * b)), a,
                     ["The coefficient of x is %d, so the factor is %d."
                      % (a, a)], placeholder="a number")

    def which_equivalent():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        correct = _lin_str(a, a * b)
        wrong = _lin_str(a, b)  # forgot to multiply the number; b != a*b as a >= 2
        options = [correct, wrong]
        random.shuffle(options)
        return _exprq("Which of these is equivalent to %d(%s): %s or %s? Type the one "
                      "that is equivalent."
                      % (a, _lin_str(1, b), options[0], options[1]), correct,
                      ["%d(%s) = %s." % (a, _lin_str(1, b), correct)], correct)

    def double_yesno():
        p = random.randint(1, 5)
        q = random.randint(1, 5)
        if random.random() < 0.5:
            return _wordq("Are (%s)(%s) and %s equivalent? Type yes or no."
                          % (_lin_str(1, p), _lin_str(1, q),
                             _quad_str(p + q, p * q)), "yes",
                          ["Expanding gives %s." % _quad_str(p + q, p * q)],
                          placeholder="yes or no")
        return _wordq("Are (%s)(%s) and %s equivalent? Type yes or no."
                      % (_lin_str(1, p), _lin_str(1, q),
                         _quad_str(p + q + 1, p * q)), "no",
                      ["Expanding gives %s, not %s."
                       % (_quad_str(p + q, p * q), _quad_str(p + q + 1, p * q))],
                      placeholder="yes or no")

    def test_value():
        a = random.randint(2, hi)
        b = random.randint(1, hi)
        x = random.randint(2, 6)
        return _numq("The expressions %d(%s) and %s are equivalent. Both give the same "
                     "value when x = %d. What is that value?"
                     % (a, _lin_str(1, b), _lin_str(a, a * b), x), a * (x + b),
                     ["%d(%d + %d) = %d x %d = %d."
                      % (a, x, b, a, x + b, a * (x + b))])

    def missing_in_double():
        p = random.randint(1, 6)
        q = random.randint(1, 6)
        return _numq("The expansion of (x + %d)(x + ___) is %s. What number goes in the "
                     "blank?" % (p, _quad_str(p + q, p * q)), q,
                     ["The constant term %d = %d x %d, so the missing number is %d."
                      % (p * q, p, q, q)], placeholder="a number")

    def bar_model_equiv():
        # Identify equivalent expressions using bar models (strip_model).
        parts = random.randint(3, _by_d(d, 4, 6, 8))
        n = random.randint(2, _by_d(d, 8, 12, 20))
        return {"prompt": "Bar models can show equivalent expressions. This bar model is "
                          "made of %d equal parts and every part is labelled x. Identify "
                          "the equivalent expression for the whole bar, then type its "
                          "value when x = %d." % (parts, n),
                "component": "strip_model",
                "spec": {"mode": "equal_parts", "parts": parts, "partLabel": "x",
                         "totalLabel": "?", "unknown": "total"},
                "answer": parts * n, "answer_type": "int", "tolerance": 0,
                "solution": ["%d equal parts of x is the expression %dx."
                             % (parts, parts),
                             "When x = %d: %d x %d = %d."
                             % (n, parts, n, parts * n)]}

    def bar_model_equiv_k():
        # Bar model where each part is k*x, for the harder tier.
        parts = random.randint(2, _by_d(d, 3, 4, 5))
        k = random.randint(2, 4)
        n = random.randint(2, _by_d(d, 6, 8, 10))
        return {"prompt": "This bar model shows equivalent expressions. It is made of %d "
                          "equal parts and every part is labelled %dx. Identify the "
                          "equivalent expression for the whole bar, then type its value "
                          "when x = %d." % (parts, k, n),
                "component": "strip_model",
                "spec": {"mode": "equal_parts", "parts": parts,
                         "partLabel": "%dx" % k, "totalLabel": "?",
                         "unknown": "total"},
                "answer": parts * k * n, "answer_type": "int", "tolerance": 0,
                "solution": ["%d equal parts of %dx is the expression %dx."
                             % (parts, k, parts * k),
                             "When x = %d: %d x %d = %d."
                             % (n, parts * k, n, parts * k * n)]}

    opts = [bracket_yesno, collect_yesno, missing_in_bracket, missing_factor,
            which_equivalent, test_value, missing_in_double, bar_model_equiv]
    if d == 2:
        opts = [bracket_yesno, collect_yesno, missing_in_bracket, missing_factor,
                double_yesno, which_equivalent, test_value, missing_in_double,
                bar_model_equiv, bar_model_equiv_k]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.h -----
@skill("Y8.6.h", "Generate sequences from rules", S6)
def _(d=1):
    d = _t(d)

    def t2t_add():
        start = random.randint(1, _by_d(d, 6, 10, 15))
        step = random.randint(2, _by_d(d, 5, 8, 12))
        terms = [start + step * i for i in range(5)]
        return _numq("A sequence starts at %d and the term-to-term rule is 'add %d'. "
                     "What is the 5th term?" % (start, step), terms[4],
                     ["The sequence is %s."
                      % ", ".join(str(x) for x in terms)])

    def t2t_list():
        start = random.randint(1, _by_d(d, 6, 10, 15))
        step = random.randint(2, _by_d(d, 5, 8, 10))
        terms = [start + step * i for i in range(4)]
        return _setq("A sequence starts at %d with term-to-term rule 'add %d'. Write the "
                     "first 4 terms." % (start, step), terms,
                     ["Add %d each time: %s."
                      % (step, ", ".join(str(x) for x in terms))])

    def t2t_subtract():
        step = random.randint(2, _by_d(d, 4, 6, 9))
        start = step * 5 + random.randint(1, 10)
        terms = [start - step * i for i in range(5)]
        return _numq("A sequence starts at %d and the term-to-term rule is 'subtract %d'. "
                     "What is the 4th term?" % (start, step), terms[3],
                     ["The sequence is %s."
                      % ", ".join(str(x) for x in terms)])

    def t2t_multiply():
        start = random.randint(1, 3)
        ratio = random.randint(2, _by_d(d, 2, 3, 4))
        terms = [start * ratio ** i for i in range(4)]
        return _numq("A sequence starts at %d and the term-to-term rule is 'multiply by "
                     "%d'. What is the 4th term?" % (start, ratio), terms[3],
                     ["The sequence is %s."
                      % ", ".join(str(x) for x in terms)])

    def p2t():
        a = random.randint(2, _by_d(d, 4, 6, 9))
        b = random.randint(1, _by_d(d, 6, 10, 15))
        n = random.randint(3, 8)
        return _numq("The position-to-term rule for a sequence is: term = %d x position + "
                     "%d. What is the term in position %d?" % (a, b, n), a * n + b,
                     ["%d x %d + %d = %d." % (a, n, b, a * n + b)])

    def p2t_list():
        a = random.randint(2, 5)
        b = random.randint(1, 8)
        terms = [a * n + b for n in range(1, 5)]
        return _setq("The position-to-term rule is: term = %d x position + %d. Write the "
                     "first 4 terms." % (a, b), terms,
                     ["Use positions 1, 2, 3, 4: %s."
                      % ", ".join(str(x) for x in terms)])

    def next_two():
        start = random.randint(1, 8)
        step = random.randint(2, 7)
        shown = [start + step * i for i in range(4)]
        return _numq("A sequence begins %s. If it continues with the same rule, what is "
                     "the next term?" % ", ".join(str(x) for x in shown),
                     shown[-1] + step,
                     ["The rule is 'add %d'." % step,
                      "%d + %d = %d." % (shown[-1], step, shown[-1] + step)])

    def find_rule_word():
        start = random.randint(2, 10)
        step = random.randint(2, 6)
        shown = [start + step * i for i in range(4)]
        return _numq("What is the term-to-term rule for the sequence %s? It is 'add ___'. "
                     "What number goes in the blank?"
                     % ", ".join(str(x) for x in shown), step,
                     ["Each term is %d more than the one before." % step])

    def fibonacci_like():
        a = random.randint(1, 5)
        b = random.randint(1, 6)
        seq = [a, b]
        for _ in range(3):
            seq.append(seq[-1] + seq[-2])
        return _numq("In this sequence each term is the sum of the two before it. The "
                     "sequence begins %d, %d. What is the 5th term?" % (a, b), seq[4],
                     ["The sequence is %s."
                      % ", ".join(str(x) for x in seq)])

    def p2t_table():
        a = random.randint(2, _by_d(d, 4, 6, 9))
        b = random.randint(1, _by_d(d, 6, 10, 12))
        return _seq_table("This sequence follows the position-to-term rule term = %dn + "
                          "%d. Work out the missing term in the table." % (a, b),
                          a, b, ["Use term = %dn + %d." % (a, b)],
                          caption="term = %s" % _lin_str(a, b, "n"))

    opts = [t2t_add, t2t_list, t2t_subtract, p2t, p2t_list, next_two,
            find_rule_word, p2t_table]
    if d == 0:
        opts = [t2t_add, t2t_list, p2t, next_two, find_rule_word, p2t_list,
                p2t_table]
    elif d == 2:
        opts = [t2t_subtract, t2t_multiply, p2t, p2t_list, fibonacci_like,
                next_two, p2t_table]
    opts = opts + [p2t_table, p2t_table]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.i -----
@skill("Y8.6.i", "nth term of a linear sequence", S6)
def _(d=1):
    d = _t(d)

    def _seq(a, b):
        return [a * n + b for n in range(1, 6)]

    def term_at_n():
        a = random.randint(2, _by_d(d, 5, 8, 11))
        b = _by_d(d, random.randint(0, 6), _nz(-6, 8), _nz(-9, 9))
        seq = _seq(a, b)
        n = random.randint(6, 20)
        return _numq("The nth term of a sequence is %s. The first terms are %s. Work out "
                     "the %s term."
                     % (_lin_str(a, b, "n"), ", ".join(str(x) for x in seq), ordinal(n)),
                     a * n + b,
                     ["%d x %d + (%d) = %d." % (a, n, b, a * n + b)])

    def find_a():
        a = random.randint(2, _by_d(d, 5, 8, 11))
        b = _nz(-6, 8)
        seq = _seq(a, b)
        return _numq("The nth term rule of the sequence %s is an + b. What is the value "
                     "of a (the common difference)?"
                     % ", ".join(str(x) for x in seq), a,
                     ["The terms go up by %d each time, so a = %d." % (a, a)],
                     placeholder="value of a")

    def find_b():
        a = random.randint(2, _by_d(d, 5, 8, 11))
        b = _nz(-6, 8)
        seq = _seq(a, b)
        return _numq("The nth term rule of the sequence %s is %dn + b. What is the value "
                     "of b?" % (", ".join(str(x) for x in seq), a), b,
                     ["The first term is %d, and %d x 1 = %d, so b = %d - %d = %d."
                      % (seq[0], a, a, seq[0], a, b)], placeholder="value of b")

    def pin_rule():
        a = random.randint(2, _by_d(d, 4, 7, 9))
        b = random.randint(1, 8)
        seq = _seq(a, b)
        return _exprq("Find the nth term rule of the sequence %s. Give it in the form "
                      "an+b, using the letter n." % ", ".join(str(x) for x in seq),
                      _lin_str(a, b, "n"),
                      ["The common difference is %d, so the rule starts %dn." % (a, a),
                       "%dn gives %d for n=1, and the first term is %d, so add %d."
                       % (a, a, seq[0], b),
                       "The rule is %s." % _lin_str(a, b, "n")], "3n+2")

    def is_term_in():
        a = random.randint(2, 6)
        b = random.randint(1, 6)
        n = random.randint(4, 9)
        val = a * n + b
        if d < 2 and random.random() < 0.5:  # d2 already has not_term_in
            val += random.randint(1, a - 1)
            return _wordq("The nth term of a sequence is %s. Is %d a term in this "
                          "sequence? Type yes or no." % (_lin_str(a, b, "n"), val), "no",
                          ["Solve %dn + %d = %d: %dn = %d, and %d / %d is not a whole "
                           "number, so %d is not a term." % (a, b, val, a, val - b,
                                                             val - b, a, val)],
                          placeholder="yes or no")
        return _wordq("The nth term of a sequence is %s. Is %d a term in this sequence? "
                      "Type yes or no." % (_lin_str(a, b, "n"), val), "yes",
                      ["%d = %d x %d + %d, which is the %s term."
                       % (val, a, n, b, ordinal(n))], placeholder="yes or no")

    def not_term_in():
        a = random.randint(3, 6)
        b = random.randint(1, 5)
        n = random.randint(4, 9)
        val = a * n + b + 1  # deliberately off the sequence
        return _wordq("The nth term of a sequence is %s. Is %d a term in this sequence? "
                      "Type yes or no." % (_lin_str(a, b, "n"), val), "no",
                      ["Solving %dn + %d = %d does not give a whole number for n."
                       % (a, b, val)], placeholder="yes or no")

    def which_position():
        a = random.randint(2, 6)
        b = random.randint(1, 6)
        n = random.randint(5, 12)
        val = a * n + b
        return _numq("The nth term of a sequence is %s. The value %d appears in the "
                     "sequence. In which position does it appear?"
                     % (_lin_str(a, b, "n"), val), n,
                     ["Solve %dn + %d = %d: %dn = %d, so n = %d."
                      % (a, b, val, a, val - b, n)], placeholder="position")

    def tenth_term():
        a = random.randint(2, 7)
        b = random.randint(1, 8)
        seq = _seq(a, b)
        return _numq("The first terms of a sequence are %s. What is the 10th term?"
                     % ", ".join(str(x) for x in seq), a * 10 + b,
                     ["The nth term rule is %s." % _lin_str(a, b, "n"),
                      "%d x 10 + %d = %d." % (a, b, a * 10 + b)])

    def missing_in_table():
        a = random.randint(2, _by_d(d, 5, 8, 11))
        b = random.randint(1, 8)
        return _seq_table("The terms of a linear sequence are shown against their "
                          "positions. The nth term rule is %s. Find the missing term."
                          % _lin_str(a, b, "n"), a, b,
                          ["Use the rule %s." % _lin_str(a, b, "n")],
                          caption="nth term = %s" % _lin_str(a, b, "n"))

    opts = [find_a, find_b, is_term_in, which_position, tenth_term, pin_rule,
            missing_in_table]
    if d == 0:
        opts = [find_a, find_b, tenth_term, term_at_n, is_term_in,
                missing_in_table]
    elif d == 2:
        opts = [term_at_n, pin_rule, which_position, not_term_in, find_b,
                is_term_in, missing_in_table]
    opts = opts + [missing_in_table, missing_in_table]
    return pick(opts)()


# ----------------------------------------------------------------- 8.6.j -----
@skill("Y8.6.j", "Arithmetic, geometric and special sequences", S6)
def _(d=1):
    d = _t(d)

    def classify_arith():
        start = random.randint(1, 8)
        step = random.randint(2, 6)
        seq = [start + step * i for i in range(4)]
        return _wordq("Is the sequence %s arithmetic or geometric? Type one word."
                      % ", ".join(str(x) for x in seq), "arithmetic",
                      ["Each term is %d MORE than the last (a common difference), so it "
                       "is arithmetic." % step], placeholder="arithmetic or geometric")

    def classify_geo():
        start = random.randint(1, 3)
        ratio = random.randint(2, 3)
        seq = [start * ratio ** i for i in range(4)]
        return _wordq("Is the sequence %s arithmetic or geometric? Type one word."
                      % ", ".join(str(x) for x in seq), "geometric",
                      ["Each term is MULTIPLIED by %d (a common ratio), so it is "
                       "geometric." % ratio], placeholder="arithmetic or geometric")

    def common_diff():
        start = random.randint(1, 9)
        step = random.randint(2, _by_d(d, 5, 8, 11))
        seq = [start + step * i for i in range(4)]
        return _numq("What is the common difference of the arithmetic sequence %s?"
                     % ", ".join(str(x) for x in seq), step,
                     ["%d - %d = %d." % (seq[1], seq[0], step)],
                     placeholder="common difference")

    def common_ratio():
        start = random.randint(1, 4)
        ratio = random.randint(2, _by_d(d, 2, 3, 4))
        seq = [start * ratio ** i for i in range(4)]
        return _numq("What is the common ratio of the geometric sequence %s?"
                     % ", ".join(str(x) for x in seq), ratio,
                     ["%d / %d = %d." % (seq[1], seq[0], ratio)],
                     placeholder="common ratio")

    def next_geo():
        start = random.randint(1, 4)
        ratio = random.randint(2, 3)
        seq = [start * ratio ** i for i in range(4)]
        return _numq("Find the next term of the geometric sequence %s."
                     % ", ".join(str(x) for x in seq), seq[-1] * ratio,
                     ["Multiply by %d: %d x %d = %d."
                      % (ratio, seq[-1], ratio, seq[-1] * ratio)])

    def next_arith():
        start = random.randint(1, 9)
        step = random.randint(2, 8)
        seq = [start + step * i for i in range(4)]
        return _numq("Find the next term of the arithmetic sequence %s."
                     % ", ".join(str(x) for x in seq), seq[-1] + step,
                     ["Add %d: %d + %d = %d."
                      % (step, seq[-1], step, seq[-1] + step)])

    def square_numbers():
        n = random.randint(3, _by_d(d, 6, 9, 12))
        return _numq("The square numbers are 1, 4, 9, 16, ... What is the %s square "
                     "number?" % ordinal(n), n * n,
                     ["The nth square number is n^2: %d^2 = %d." % (n, n * n)])

    def triangular_numbers():
        n = random.randint(3, _by_d(d, 6, 8, 10))
        return _numq("The triangular numbers are 1, 3, 6, 10, 15, ... What is the %s "
                     "triangular number?" % ordinal(n), n * (n + 1) // 2,
                     ["The nth triangular number is n(n+1)/2: %d x %d / 2 = %d."
                      % (n, n + 1, n * (n + 1) // 2)])

    def next_square():
        k = random.randint(3, 8)
        seq = [i * i for i in range(1, k)]
        return _numq("These are the first square numbers: %s. What is the next square "
                     "number?" % ", ".join(str(x) for x in seq), k * k,
                     ["The next square number is %d^2 = %d." % (k, k * k)])

    def name_special():
        return _wordq("What name is given to the sequence 1, 3, 6, 10, 15, 21, ...? "
                      "Type one word.", "triangular",
                      ["These are the triangular numbers: 1, 1+2, 1+2+3, ..."],
                      placeholder="one word")

    def arith_table():
        start = random.randint(1, 9)
        step = random.randint(2, _by_d(d, 5, 8, 11))
        return _seq_table("This is an arithmetic sequence. Work out the missing term in "
                          "the table.", step, start - step,
                          ["The terms go up by %d each time." % step],
                          caption="Arithmetic sequence")

    def mixed_review():
        # Number sequences: mixed review -- a mixed bag of sequence types.
        kind = pick(["arith", "geo", "square", "triangular", "fib"])
        if kind == "arith":
            start = random.randint(1, 9)
            step = random.randint(2, _by_d(d, 5, 8, 11))
            seq = [start + step * i for i in range(4)]
            return _numq("Number sequences: mixed review. Find the next term of the "
                         "sequence %s." % ", ".join(str(x) for x in seq),
                         seq[-1] + step,
                         ["This is arithmetic (add %d): %d + %d = %d."
                          % (step, seq[-1], step, seq[-1] + step)])
        if kind == "geo":
            start = random.randint(1, 4)
            ratio = random.randint(2, _by_d(d, 2, 3, 3))
            seq = [start * ratio ** i for i in range(4)]
            return _numq("Number sequences: mixed review. Find the next term of the "
                         "sequence %s." % ", ".join(str(x) for x in seq),
                         seq[-1] * ratio,
                         ["This is geometric (multiply by %d): %d x %d = %d."
                          % (ratio, seq[-1], ratio, seq[-1] * ratio)])
        if kind == "square":
            k = random.randint(3, _by_d(d, 6, 8, 10))
            seq = [i * i for i in range(1, k)]
            return _numq("Number sequences: mixed review. These are square numbers: %s. "
                         "What is the next term?" % ", ".join(str(x) for x in seq),
                         k * k, ["The next square number is %d^2 = %d." % (k, k * k)])
        if kind == "triangular":
            k = random.randint(3, _by_d(d, 6, 8, 9))
            seq = [i * (i + 1) // 2 for i in range(1, k)]
            return _numq("Number sequences: mixed review. These are triangular numbers: "
                         "%s. What is the next term?"
                         % ", ".join(str(x) for x in seq), k * (k + 1) // 2,
                         ["The next triangular number is %d x %d / 2 = %d."
                          % (k, k + 1, k * (k + 1) // 2)])
        a = random.randint(1, 5)
        b = random.randint(1, 6)
        seq = [a, b]
        for _ in range(3):
            seq.append(seq[-1] + seq[-2])
        return _numq("Number sequences: mixed review. In this sequence each term is the "
                     "sum of the two before it: %s. What is the next term?"
                     % ", ".join(str(x) for x in seq[:4]), seq[4],
                     ["%d + %d = %d." % (seq[2], seq[3], seq[4])])

    opts = [classify_arith, classify_geo, common_diff, common_ratio, next_geo,
            next_arith, square_numbers, triangular_numbers, arith_table,
            mixed_review]
    if d == 0:
        opts = [classify_arith, classify_geo, common_diff, next_arith,
                square_numbers, next_square, arith_table, mixed_review]
    elif d == 2:
        opts = [common_ratio, next_geo, square_numbers, triangular_numbers,
                name_special, common_diff, classify_geo, arith_table,
                mixed_review]
    opts = opts + [arith_table, arith_table]
    return pick(opts)()


# ===========================================================================
# 8.7  EQUATIONS, INEQUALITIES & LINEAR GRAPHS
# ===========================================================================

# ----------------------------------------------------------------- 8.7.a -----
@skill("Y8.7.a", "Coordinates in all four quadrants", S7)
def _(d=1):
    d = _t(d)
    r = _by_d(d, 5, 6, 8)

    def plot_point():
        x = _nz(-r, r)
        y = _nz(-r, r)
        return _gridq("Plot the point (%d, %d)." % (x, y), x, y,
                      ["Go %d along the x-axis and %d up/down the y-axis."
                       % (x, y)], r=r)

    def read_point():
        x = _nz(-r, r)
        y = _nz(-r, r)
        return {"prompt": "Type the coordinates of the point P shown on the grid.",
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[x, y, "P"]]},
                "answer": "(%d,%d)" % (x, y), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["P is %d along and %d up/down, so P = (%d, %d)."
                             % (x, y, x, y)]}

    def which_quadrant():
        x = _nz(-r, r)
        y = _nz(-r, r)
        quad = {(1, 1): "first", (-1, 1): "second", (-1, -1): "third",
                (1, -1): "fourth"}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
        return _wordq("In which quadrant does the point (%d, %d) lie? Type first, second, "
                      "third or fourth." % (x, y), quad,
                      ["x is %s and y is %s, so it is the %s quadrant."
                       % ("positive" if x > 0 else "negative",
                          "positive" if y > 0 else "negative", quad)],
                      placeholder="first / second / third / fourth")

    def midpoint():
        x1 = _nz(-r, r)
        x2 = _nz(-r, r)
        while (x1 + x2) % 2 != 0:
            x2 = _nz(-r, r)
        y1 = _nz(-r, r)
        y2 = _nz(-r, r)
        while (y1 + y2) % 2 != 0:
            y2 = _nz(-r, r)
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return {"prompt": "A is (%d, %d) and B is (%d, %d). Plot the midpoint of AB."
                          % (x1, y1, x2, y2),
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[x1, y1, "A"], [x2, y2, "B"]]},
                "answer": "(%d,%d)" % (mx, my), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Midpoint x = (%d + %d)/2 = %d." % (x1, x2, mx),
                             "Midpoint y = (%d + %d)/2 = %d." % (y1, y2, my)]}

    def reflect_x():
        x = _nz(-r, r)
        y = _nz(-r, r)
        return {"prompt": "Point P is at (%d, %d). Plot its reflection in the x-axis."
                          % (x, y),
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[x, y, "P"]]},
                "answer": "(%d,%d)" % (x, -y), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Reflecting in the x-axis keeps x and flips the sign of y.",
                             "(%d, %d) -> (%d, %d)." % (x, y, x, -y)]}

    def reflect_y():
        x = _nz(-r, r)
        y = _nz(-r, r)
        return {"prompt": "Point P is at (%d, %d). Plot its reflection in the y-axis."
                          % (x, y),
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[x, y, "P"]]},
                "answer": "(%d,%d)" % (-x, y), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Reflecting in the y-axis flips the sign of x.",
                             "(%d, %d) -> (%d, %d)." % (x, y, -x, y)]}

    def translate():
        x = _nz(-r + 2, r - 2)
        y = _nz(-r + 2, r - 2)
        dx = _nz(-2, 2)
        dy = _nz(-2, 2)
        return {"prompt": "Point P is at (%d, %d). Plot the point after translating it "
                          "%d %s and %d %s."
                          % (x, y, abs(dx), "right" if dx > 0 else "left",
                             abs(dy), "up" if dy > 0 else "down"),
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[x, y, "P"]]},
                "answer": "(%d,%d)" % (x + dx, y + dy), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Add %d to x and %d to y." % (dx, dy),
                             "(%d, %d) -> (%d, %d)." % (x, y, x + dx, y + dy)]}

    def fourth_vertex():
        x = _nz(-r + 1, r - 1)
        y = _nz(-r + 1, r - 1)
        w = random.randint(1, r - 1)
        h = random.randint(1, r - 1)
        # rectangle with vertices (x,y),(x+w,y),(x+w,y+h),(x,y+h); keep on grid
        if x + w > r:
            w = -w
        if y + h > r:
            h = -h
        pts = [[x, y, "A"], [x + w, y, "B"], [x + w, y + h, "C"]]
        return {"prompt": "A, B and C are three corners of a rectangle. Plot the fourth "
                          "corner D.",
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": pts},
                "answer": "(%d,%d)" % (x, y + h), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["D lines up with A vertically and with C horizontally.",
                             "D = (%d, %d)." % (x, y + h)]}

    def on_axis():
        x = _nz(-r, r)
        if random.random() < 0.5:
            return _wordq("The point (0, %d) lies on one of the axes. Which axis is it on? "
                          "Type x or y." % x, "y",
                          ["The x-coordinate is 0, so the point is on the y-axis."],
                          placeholder="x or y")
        return _wordq("The point (%d, 0) lies on one of the axes. Which axis is it on? "
                      "Type x or y." % x, "x",
                      ["The y-coordinate is 0, so the point is on the x-axis."],
                      placeholder="x or y")

    def coordinate_plane_review():
        # Coordinate plane review -- plot a point in any quadrant.
        x = _nz(-r, r)
        y = _nz(-r, r)
        return _gridq("Coordinate plane review: plot the point with coordinates (%d, %d) "
                      "on the coordinate plane." % (x, y), x, y,
                      ["Go %d along the x-axis, then %d up or down the y-axis, and mark "
                       "the point." % (x, y)], r=r)

    def follow_directions():
        # Follow directions on a coordinate plane: start, move, plot the finish.
        sx = random.randint(-r + 3, r - 3)
        sy = random.randint(-r + 3, r - 3)
        h = random.randint(1, 3)
        ver = random.randint(1, 3)
        hdir = pick(["right", "left"])
        vdir = pick(["up", "down"])
        ex = sx + (h if hdir == "right" else -h)
        ey = sy + (ver if vdir == "up" else -ver)
        return {"prompt": "Follow the directions on the coordinate plane. Start at the "
                          "point (%d, %d), move %d %s and %d %s, then plot the point "
                          "where you finish." % (sx, sy, h, hdir, ver, vdir),
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r,
                         "ymax": r, "points": [[sx, sy, "Start"]]},
                "answer": "(%d,%d)" % (ex, ey), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Moving %s changes x, moving %s changes y." % (hdir, vdir),
                             "(%d, %d) -> (%d, %d)." % (sx, sy, ex, ey)]}

    opts = [plot_point, read_point, which_quadrant, midpoint, reflect_x,
            reflect_y, translate, fourth_vertex, on_axis,
            coordinate_plane_review, follow_directions]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.b -----
@skill("Y8.7.b", "Solve one- and two-step linear equations", S7)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 6, 10, 12)

    def add():
        x = random.randint(1, hi)
        b = random.randint(1, hi)
        return _numq("Solve x + %d = %d." % (b, x + b), x,
                     ["Subtract %d from both sides: x = %d - %d = %d."
                      % (b, x + b, b, x)], placeholder="x =")

    def subtract():
        x = random.randint(1, hi)
        b = random.randint(1, hi)
        return _numq("Solve x - %d = %d." % (b, x - b), x,
                     ["Add %d to both sides: x = %d + %d = %d."
                      % (b, x - b, b, x)], placeholder="x =")

    def multiply():
        a = random.randint(2, hi)
        x = random.randint(2, hi)
        return _numq("Solve %dx = %d." % (a, a * x), x,
                     ["Divide both sides by %d: x = %d / %d = %d."
                      % (a, a * x, a, x)], placeholder="x =")

    def divide():
        a = pick([2, 3, 4, 5, 6])
        x = random.randint(2, hi) * a
        return _numq("Solve x / %d = %d." % (a, x // a), x,
                     ["Multiply both sides by %d: x = %d x %d = %d."
                      % (a, x // a, a, x)], placeholder="x =")

    def two_step():
        a = random.randint(2, hi)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx + %d = %d." % (a, b, a * x + b), x,
                     ["Subtract %d: %dx = %d." % (b, a, a * x),
                      "Divide by %d: x = %d." % (a, x)], placeholder="x =")

    def two_step_sub():
        a = random.randint(2, hi)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx - %d = %d." % (a, b, a * x - b), x,
                     ["Add %d: %dx = %d." % (b, a, a * x),
                      "Divide by %d: x = %d." % (a, x)], placeholder="x =")

    def negative_solution():
        a = random.randint(2, hi)
        x = _nz(-hi, -1)
        b = random.randint(1, hi)
        return _numq("Solve %dx + %d = %d." % (a, b, a * x + b), x,
                     ["Subtract %d: %dx = %d." % (b, a, a * x),
                      "Divide by %d: x = %d." % (a, x)], placeholder="x =")

    def word_two_step():
        a = random.randint(2, 6)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        name = pick(NAMES)
        return _numq("%s thinks of a number, multiplies it by %d, then adds %d. The "
                     "result is %d. What was the number?"
                     % (name, a, b, a * x + b), x,
                     ["%dx + %d = %d, so %dx = %d and x = %d."
                      % (a, b, a * x + b, a, a * x, x)], placeholder="the number")

    def fraction_step():
        a = pick([2, 3, 4, 5])
        x = random.randint(2, 8) * a
        b = random.randint(1, hi)
        return _numq("Solve x / %d + %d = %d." % (a, b, x // a + b), x,
                     ["Subtract %d: x/%d = %d." % (b, a, x // a),
                      "Multiply by %d: x = %d." % (a, x)], placeholder="x =")

    def check_solution():
        a = random.randint(2, 6)
        x = random.randint(2, 8)
        b = random.randint(1, hi)
        t = x if random.random() < 0.5 else x + pick([-1, 1])
        ok = t == x
        return _wordq("Is x = %d the solution of %dx + %d = %d? Type yes or no."
                      % (t, a, b, a * x + b), "yes" if ok else "no",
                      ["%d x %d + %d = %d, %s %d."
                       % (a, t, b, a * t + b, "which is correct: it equals" if ok
                          else "which does not equal", a * x + b)],
                      placeholder="yes or no")

    opts = [add, subtract, multiply, divide, two_step, two_step_sub,
            word_two_step, check_solution]
    if d == 0:
        opts = [add, subtract, multiply, divide, check_solution]
    elif d == 2:
        opts = [two_step, two_step_sub, negative_solution, fraction_step,
                word_two_step]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.c -----
@skill("Y8.7.c", "Equations with brackets and like terms", S7)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 5, 8, 11)

    def bracket():
        a = random.randint(2, 5)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        rhs = a * (x + c)
        return _numq("Solve %d(x + %d) = %d." % (a, c, rhs), x,
                     ["Divide both sides by %d: x + %d = %d." % (a, c, rhs // a),
                      "Subtract %d: x = %d." % (c, x)], placeholder="x =")

    def bracket_expand():
        a = random.randint(2, 5)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        b = random.randint(1, hi)
        rhs = a * (x + c) + b
        return _numq("Solve %d(x + %d) + %d = %d." % (a, c, b, rhs), x,
                     ["Expand: %dx + %d = %d." % (a, a * c + b, rhs),
                      "Subtract %d: %dx = %d, so x = %d."
                      % (a * c + b, a, a * x, x)], placeholder="x =")

    def collect_then_solve():
        a1 = random.randint(2, 5)
        a2 = random.randint(1, 4)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        a = a1 + a2
        rhs = a * x + c
        return _numq("Solve %s + %s + %d = %d."
                     % (_coef(a1, "x"), _coef(a2, "x"), c, rhs), x,
                     ["Collect like terms: %dx + %d = %d." % (a, c, rhs),
                      "Subtract %d: %dx = %d, so x = %d." % (c, a, a * x, x)],
                     placeholder="x =")

    def two_brackets():
        a = random.randint(2, 4)
        b = random.randint(2, 4)
        x = random.randint(2, hi)
        c = random.randint(1, 4)
        e = random.randint(1, 4)
        rhs = a * (x + c) + b * (x + e)
        return _numq("Solve %d(x + %d) + %d(x + %d) = %d." % (a, c, b, e, rhs), x,
                     ["Expand both brackets: %dx + %d = %d."
                      % (a + b, a * c + b * e, rhs),
                      "%dx = %d, so x = %d." % (a + b, (a + b) * x, x)],
                     placeholder="x =")

    def bracket_word():
        a = random.randint(2, 5)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        name = pick(NAMES)
        return _numq("%s adds %d to a number, then multiplies the result by %d. The "
                     "answer is %d. What was the number?"
                     % (name, c, a, a * (x + c)), x,
                     ["%d(x + %d) = %d, so x + %d = %d and x = %d."
                      % (a, c, a * (x + c), c, x + c, x)], placeholder="the number")

    def minus_bracket():
        a = random.randint(2, 4)
        x = random.randint(3, hi)
        c = random.randint(1, x - 1)
        rhs = a * (x - c)
        return _numq("Solve %d(x - %d) = %d." % (a, c, rhs), x,
                     ["Divide by %d: x - %d = %d." % (a, c, rhs // a),
                      "Add %d: x = %d." % (c, x)], placeholder="x =")

    def bracket_perimeter():
        a = random.randint(2, 4)
        x = random.randint(2, hi)
        c = random.randint(1, 5)
        perim = 2 * (x + (x + c))
        return _numq("A rectangle is x cm wide and (x + %d) cm long. Its perimeter is "
                     "%d cm. What is x, in cm?" % (c, perim), x,
                     ["Perimeter = 2(x + x + %d) = 4x + %d = %d."
                      % (c, 2 * c, perim),
                      "4x = %d, so x = %d." % (perim - 2 * c, x)], placeholder="x =")

    def collect_like_both():
        a1 = random.randint(3, 6)
        a2 = random.randint(1, a1 - 1)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        a = a1 - a2
        rhs = a * x + c
        return _numq("Solve %s - %s + %d = %d."
                     % (_coef(a1, "x"), _coef(a2, "x"), c, rhs), x,
                     ["Collect like terms: %dx + %d = %d." % (a, c, rhs),
                      "%dx = %d, so x = %d." % (a, a * x, x)], placeholder="x =")

    def algebra_tiles():
        # Model and solve equations using algebra tiles (described in words).
        a = random.randint(2, hi)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        rhs = a * x + b
        return _numq("Model and solve using algebra tiles. On one side of the mat there "
                     "are %d x-tiles and %d unit tiles; the other side has %d unit "
                     "tiles, and the two sides balance. How many units does one x-tile "
                     "stand for? (Solve %dx + %d = %d.)"
                     % (a, b, rhs, a, b, rhs), x,
                     ["Remove %d unit tiles from both sides: %d x-tiles = %d units."
                      % (b, a, a * x),
                      "Share equally between the %d x-tiles: x = %d." % (a, x)],
                     placeholder="x =")

    def solve_distributive():
        # Solve equations with the distributive property.
        a = random.randint(2, 5)
        x = random.randint(2, hi)
        c = random.randint(1, hi)
        rhs = a * (x + c)
        return _numq("Solve %d(x + %d) = %d. Use the distributive property to expand the "
                     "bracket first." % (a, c, rhs), x,
                     ["Distributive property: %d(x + %d) = %dx + %d."
                      % (a, c, a, a * c),
                      "%dx + %d = %d, so %dx = %d and x = %d."
                      % (a, a * c, rhs, a, a * x, x)], placeholder="x =")

    def solve_distributive_both():
        # Distributive property on one side, x-term on the other.
        a = random.randint(2, 4)
        c = random.randint(1, 5)
        cc = random.randint(1, a - 1)
        x = random.randint(2, hi)
        e = a * (x + c) - cc * x  # a(x+c) = cc x + e, e > 0
        return _numq("Solve %d(x + %d) = %s + %d. Expand using the distributive "
                     "property, then collect the x terms."
                     % (a, c, _coef(cc, "x"), e), x,
                     ["Distributive property: %dx + %d = %dx + %d."
                      % (a, a * c, cc, e),
                      "Move the x terms: %dx = %d, so x = %d."
                      % (a - cc, e - a * c, x)], placeholder="x =")

    opts = [bracket, bracket_expand, collect_then_solve, bracket_word,
            minus_bracket, bracket_perimeter, algebra_tiles, solve_distributive]
    if d == 0:
        opts = [bracket, bracket_word, minus_bracket, algebra_tiles,
                solve_distributive]
    elif d == 2:
        opts = [bracket_expand, collect_then_solve, two_brackets, minus_bracket,
                bracket_perimeter, collect_like_both, solve_distributive,
                solve_distributive_both]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.d -----
@skill("Y8.7.d", "Equations with the unknown on both sides", S7)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 5, 8, 10)

    def basic():
        # ax + b = cx + e, with a > c and all numbers positive (e = (a-c)x + b)
        a = random.randint(3, hi + 2)
        c = random.randint(1, a - 1)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        e = (a - c) * x + b
        return _numq("Solve %s + %d = %s + %d."
                     % (_coef(a, "x"), b, _coef(c, "x"), e), x,
                     ["Subtract %dx from both sides: %dx + %d = %d."
                      % (c, a - c, b, e),
                      "Subtract %d: %dx = %d, so x = %d." % (b, a - c, e - b, x)],
                     placeholder="x =")

    def simple():
        a = random.randint(2, hi)
        c = random.randint(1, a - 1) if a > 1 else 1
        x = random.randint(2, hi)
        e = random.randint(1, hi)
        # ax = cx + e -> (a-c)x = e
        diff = a - c
        e = diff * x
        return _numq("Solve %s = %s + %d." % (_coef(a, "x"), _coef(c, "x"), e), x,
                     ["Subtract %dx: %dx = %d." % (c, diff, e),
                      "Divide by %d: x = %d." % (diff, x)], placeholder="x =")

    def with_bracket():
        a = random.randint(3, 5)
        c = random.randint(1, a - 1)  # c < a keeps e positive and the coefficient tidy
        x = random.randint(2, hi)
        inner = random.randint(1, 4)
        # a(x + inner) = cx + e, with e = (a-c)x + a*inner > 0
        e = a * (x + inner) - c * x
        return _numq("Solve %d(x + %d) = %s + %d."
                     % (a, inner, _coef(c, "x"), e), x,
                     ["Expand: %dx + %d = %dx + %d." % (a, a * inner, c, e),
                      "Move x terms: %dx = %d, so x = %d."
                      % (a - c, e - a * inner, x)], placeholder="x =")

    def word():
        a = random.randint(3, 6)
        c = random.randint(1, a - 1)
        x = random.randint(2, hi)
        e = (a - c) * x
        return _numq("A number multiplied by %d equals the same number multiplied by %d, "
                     "plus %d. What is the number?" % (a, c, e), x,
                     ["%dx = %dx + %d, so %dx = %d and x = %d."
                      % (a, c, e, a - c, e, x)], placeholder="the number")

    def both_sides_const():
        a = random.randint(3, hi)
        c = random.randint(1, a - 1)
        x = random.randint(2, hi)
        b = random.randint(1, hi)
        e = (a - c) * x + b
        return _numq("Solve %s + %d = %s + %d."
                     % (_coef(c, "x"), e, _coef(a, "x"), b), x,
                     ["Subtract %dx: %d = %dx + %d." % (c, e, a - c, b),
                      "Subtract %d: %dx = %d, so x = %d." % (b, a - c, e - b, x)],
                     placeholder="x =")

    def check_both():
        a = random.randint(3, 6)
        c = random.randint(1, a - 1)
        x = random.randint(2, 6)
        e = (a - c) * x
        t = x if random.random() < 0.5 else x + pick([-1, 1])
        ok = t == x
        return _wordq("Is x = %d the solution of %s = %s + %d? Type yes or no."
                      % (t, _coef(a, "x"), _coef(c, "x"), e), "yes" if ok else "no",
                      ["%d x %d = %d and %d x %d + %d = %d, so the two sides are %s."
                       % (a, t, a * t, c, t, e, c * t + e,
                          "equal" if ok else "not equal")], placeholder="yes or no")

    def geometry():
        a = random.randint(3, 6)
        c = random.randint(1, a - 1)
        x = random.randint(2, hi)
        e = (a - c) * x
        return _numq("Two sides of a shape have equal length. One is %s cm and the "
                     "other is (%s + %d) cm. What is the value of x, in cm?"
                     % (_coef(a, "x"), _coef(c, "x"), e), x,
                     ["%dx = %dx + %d, so %dx = %d and x = %d."
                      % (a, c, e, a - c, e, x)], placeholder="x =")

    def both_sides_sub():
        a = random.randint(3, hi + 2)
        c = random.randint(1, a - 1)
        x = random.randint(2, hi)
        e = random.randint(1, (a - c) * x - 1)  # keeps b >= 1
        b = (a - c) * x - e
        return _numq("Solve %s - %d = %s + %d."
                     % (_coef(a, "x"), b, _coef(c, "x"), e), x,
                     ["Subtract %dx: %dx - %d = %d." % (c, a - c, b, e),
                      "Add %d: %dx = %d, so x = %d." % (b, a - c, e + b, x)],
                     placeholder="x =")

    opts = [simple, basic, word, both_sides_const, check_both, geometry,
            both_sides_sub]
    if d == 2:
        opts = [basic, with_bracket, both_sides_const, word, geometry, simple,
                both_sides_sub]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.e -----
@skill("Y8.7.e", "Form and solve equations from words", S7)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 6, 10, 14)

    def think_number():
        a = random.randint(2, 6)
        b = random.randint(1, hi)
        x = random.randint(2, hi)
        name = pick(NAMES)
        return _numq("%s thinks of a number, multiplies it by %d and adds %d. The answer "
                     "is %d. Form an equation and solve it to find the number."
                     % (name, a, b, a * x + b), x,
                     ["%dx + %d = %d, so %dx = %d and x = %d."
                      % (a, b, a * x + b, a, a * x, x)], placeholder="the number")

    def consecutive():
        n = random.randint(5, hi)
        total = n + (n + 1)
        return _numq("Two consecutive whole numbers add up to %d. What is the smaller "
                     "number?" % total, n,
                     ["Let the smaller be n. Then n + (n + 1) = %d." % total,
                      "2n + 1 = %d, so 2n = %d and n = %d." % (total, total - 1, n)],
                     placeholder="the smaller number")

    def rectangle():
        w = random.randint(3, hi)
        extra = random.randint(1, 6)
        length = w + extra
        perim = 2 * (w + length)
        return _numq("A rectangle is %d cm longer than it is wide. Its perimeter is %d "
                     "cm. What is the width, in cm?" % (extra, perim), w,
                     ["Let the width be w. Length = w + %d." % extra,
                      "2(w + w + %d) = %d, so 4w + %d = %d and w = %d."
                      % (extra, perim, 2 * extra, perim, w)], placeholder="the width")

    def angles_straight():
        x = random.randint(20, 60)
        b = random.randint(10, 40)
        # x + (x + b) = 180
        if 2 * x + b != 180:
            x = (180 - b) // 2
            if (180 - b) % 2 != 0:
                b += 1
                x = (180 - b) // 2
        return _numq("Two angles on a straight line are x degrees and (x + %d) degrees. "
                     "Angles on a straight line add up to 180 degrees. What is x, in "
                     "degrees?" % b, x,
                     ["x + (x + %d) = 180, so 2x = %d and x = %d."
                      % (b, 180 - b, x)], placeholder="x =")

    def age():
        child = random.randint(6, 14)
        mult = random.randint(2, 4)
        parent = child * mult
        name1, name2 = pick(NAMES), pick(NAMES)
        while name2 == name1:
            name2 = pick(NAMES)
        return _numq("%s is %d times as old as %s. Together their ages add up to %d "
                     "years. How old is %s (the younger one)?"
                     % (name1, mult, name2, child + parent, name2), child,
                     ["Let %s's age be x. Then x + %dx = %d."
                      % (name2, mult, child + parent),
                      "%dx = %d, so x = %d." % (mult + 1, child + parent, child)],
                     placeholder="the younger age")

    def sweets_share():
        a = random.randint(2, 5)
        extra = random.randint(2, 10)
        x = random.randint(3, hi)
        total = x + (a * x + extra)
        name1, name2 = pick(NAMES), pick(NAMES)
        while name2 == name1:
            name2 = pick(NAMES)
        return _numq("%s has x sweets. %s has %d more than %d times as many as %s. "
                     "Together they have %d sweets. How many sweets does %s have?"
                     % (name1, name2, extra, a, name1, total, name1), x,
                     ["x + (%dx + %d) = %d, so %dx = %d and x = %d."
                      % (a, extra, total, a + 1, total - extra, x)],
                     placeholder="a number")

    def cost_problem():
        each = random.randint(2, 8)
        fixed = random.randint(3, 20)
        n = random.randint(2, hi)
        total = each * n + fixed
        return _numq("A taxi charges a fixed £%d plus £%d per mile. A journey "
                     "costs £%d. How many miles was the journey?"
                     % (fixed, each, total), n,
                     ["%dn + %d = %d, so %dn = %d and n = %d."
                      % (each, fixed, total, each, total - fixed, n)],
                     placeholder="number of miles")

    def form_only():
        a = random.randint(2, 6)
        b = random.randint(1, hi)
        result = random.randint(20, 60)
        return _wordq("A number x is multiplied by %d and then %d is added, giving %d. "
                      "Which equation shows this? Type it in the form ax+b=c with no "
                      "spaces, like 3x+4=19." % (a, b, result),
                      "%dx+%d=%d" % (a, b, result),
                      ["'Multiplied by %d' gives %dx; 'add %d' gives + %d; result is %d."
                       % (a, a, b, b, result)], placeholder="e.g. 3x+4=19")

    def two_var_evaluate():
        # Solve word problems involving two-variable equations (evaluate).
        p1 = random.randint(2, 6)
        p2 = random.randint(2, 6)
        n1 = random.randint(2, hi)
        n2 = random.randint(2, hi)
        itemA, itemB = pick([("apples", "pears"), ("pens", "pencils"),
                             ("adult tickets", "child tickets"),
                             ("red beads", "blue beads")])
        total = p1 * n1 + p2 * n2
        return _numq("A shop uses the two-variable equation c = %da + %db for the total "
                     "cost c pounds, where a is the number of %s and b is the number of "
                     "%s. Work out c when a = %d and b = %d, in pounds."
                     % (p1, p2, itemA, itemB, n1, n2), total,
                     ["c = %d x %d + %d x %d = %d + %d = %d."
                      % (p1, n1, p2, n2, p1 * n1, p2 * n2, total)], placeholder="pounds")

    def two_var_solve():
        # Two-variable equation: given c and a, find b.
        p1 = random.randint(2, 6)
        p2 = pick([2, 3, 4, 5])
        n1 = random.randint(1, hi)
        b = random.randint(1, hi)
        total = p1 * n1 + p2 * b
        return _numq("A word problem gives the two-variable equation c = %da + %db. It "
                     "is known that c = %d and a = %d. Work out the value of b."
                     % (p1, p2, total, n1), b,
                     ["Substitute: %d = %d x %d + %db, so %db = %d."
                      % (total, p1, n1, p2, p2, total - p1 * n1),
                      "b = %d." % b], placeholder="value of b")

    opts = [think_number, consecutive, rectangle, angles_straight, age,
            cost_problem, two_var_evaluate, two_var_solve]
    if d == 0:
        opts = [think_number, consecutive, rectangle, cost_problem,
                two_var_evaluate]
    elif d == 2:
        opts = [angles_straight, age, sweets_share, cost_problem, rectangle,
                form_only, two_var_evaluate, two_var_solve]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.f -----
@skill("Y8.7.f", "Represent and interpret inequalities on a number line", S7)
def _(d=1):
    d = _t(d)

    def _bounds(v):
        lo = min(v - 3, -1)
        hi = max(v + 3, 1)
        return lo, hi

    def write_inequality():
        op = pick(["<", "<=", ">", ">="])
        v = random.randint(-3, 6)
        lo, hi = _bounds(v)
        return _ineqq("The number line shows an inequality. Write it using x. Use <, <=, "
                      ">, or >= and no spaces (for example x>3 or x<=2).",
                      _ineq_spec(op, v, lo, hi), "x%s%d" % (op, v),
                      ["The circle is at %d and the arrow points %s."
                       % (v, "right (greater)" if op in (">", ">=") else "left (less)"),
                       "A %s circle means the value is %s, so x %s %d."
                       % ("filled" if op in ("<=", ">=") else "hollow",
                          "included" if op in ("<=", ">=") else "not included", op, v)],
                      answer_type="str", placeholder="e.g. x>3")

    def boundary_value():
        op = pick(["<", "<=", ">", ">="])
        v = random.randint(*_by_d(d, (0, 8), (-3, 6), (-15, -2)))     # stretch: a negative boundary
        lo, hi = _bounds(v)
        return _ineqq("What is the boundary value marked by the circle on this number "
                      "line?", _ineq_spec(op, v, lo, hi), v,
                      ["The circle is drawn at %d." % v], placeholder="a number")

    def open_or_closed():
        op = pick(["<", "<=", ">", ">="])
        v = random.randint(*_by_d(d, (0, 8), (-3, 6), (-15, -2)))
        lo, hi = _bounds(v)
        closed = op in ("<=", ">=")
        return _ineqq("Is the value %d included in the inequality shown (is the circle "
                      "filled in)? Type yes or no." % v,
                      _ineq_spec(op, v, lo, hi), "yes" if closed else "no",
                      ["A filled circle (<= or >=) includes the value; a hollow circle "
                       "(< or >) does not."], answer_type="str",
                      placeholder="yes or no")

    def _sat(op, v):
        lo, hi = _bounds(v)
        t = v + random.randint(-2, 2)
        ok = {"<": t < v, "<=": t <= v, ">": t > v, ">=": t >= v}[op]
        return _ineqq("Does the whole number %d satisfy the inequality shown on the "
                      "number line? Type yes or no." % t,
                      _ineq_spec(op, v, lo, hi), "yes" if ok else "no",
                      ["The number line shows x %s %d (a %s circle at %d)."
                       % (op, v, "filled" if op in ("<=", ">=") else "hollow", v),
                       "%d %s it, so the answer is %s."
                       % (t, "satisfies" if ok else "does not satisfy",
                          "yes" if ok else "no")],
                      answer_type="str", placeholder="yes or no")

    def satisfies():
        return _sat(pick([">", ">="]), random.randint(-2, 4))

    def satisfies_less():
        return _sat(pick(["<", "<="]), random.randint(0, 5))

    def direction():
        op = pick(["<", "<=", ">", ">="])
        v = random.randint(-3, 6)
        lo, hi = _bounds(v)
        want = "greater" if op in (">", ">=") else "less"
        return _ineqq("Does the shaded arrow show the values GREATER than %d or LESS than "
                      "%d? Type greater or less." % (v, v),
                      _ineq_spec(op, v, lo, hi), want,
                      ["The arrow points %s, showing the %s values."
                       % ("right" if want == "greater" else "left", want)],
                      answer_type="str", placeholder="greater or less")

    def smallest_integer():
        v = random.randint(-3, 6)
        lo, hi = _bounds(v)
        # x >= v  -> smallest integer is v ;  x > v -> v+1
        op = pick([">", ">="])
        ans = v if op == ">=" else v + 1
        return _ineqq("This number line shows an inequality for x. What is the smallest "
                      "whole number that x can be?", _ineq_spec(op, v, lo, hi), ans,
                      ["A %s circle at %d means the smallest whole number is %d."
                       % ("filled" if op == ">=" else "hollow", v, ans)],
                      placeholder="a number")

    def largest_integer():
        v = random.randint(-1, 6)
        lo, hi = _bounds(v)
        op = pick(["<", "<="])
        ans = v if op == "<=" else v - 1
        return _ineqq("This number line shows an inequality for x. What is the largest "
                      "whole number that x can be?", _ineq_spec(op, v, lo, hi), ans,
                      ["A %s circle at %d means the largest whole number is %d."
                       % ("filled" if op == "<=" else "hollow", v, ans)],
                      placeholder="a number")

    opts = [write_inequality, boundary_value, open_or_closed, satisfies,
            satisfies_less, direction, smallest_integer, largest_integer]
    if d == 0:
        opts = [boundary_value, open_or_closed, satisfies, satisfies_less,
                direction]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.g -----
@skill("Y8.7.g", "Solve one- and two-step inequalities", S7)
def _(d=1):
    d = _t(d)
    hi = _by_d(d, 6, 10, 14)

    def one_step_gt():
        a = random.randint(2, 6)
        v = random.randint(2, hi)
        return _numq("Solve %dx > %d. The solution is x > ___ . What number goes in the "
                     "blank?" % (a, a * v), v,
                     ["Divide both sides by %d: x > %d." % (a, v)],
                     placeholder="a number")

    def one_step_lt():
        a = random.randint(2, 6)
        v = random.randint(2, hi)
        return _numq("Solve %dx < %d. The solution is x < ___ . What number goes in the "
                     "blank?" % (a, a * v), v,
                     ["Divide both sides by %d: x < %d." % (a, v)],
                     placeholder="a number")

    def add_step():
        b = random.randint(1, hi)
        v = random.randint(1, hi)
        return _numq("Solve x + %d >= %d. The solution is x >= ___ . What number goes in "
                     "the blank?" % (b, v + b), v,
                     ["Subtract %d from both sides: x >= %d." % (b, v)],
                     placeholder="a number")

    def two_step():
        a = random.randint(2, 5)
        v = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx + %d > %d. The solution is x > ___ . What number goes in "
                     "the blank?" % (a, b, a * v + b), v,
                     ["Subtract %d: %dx > %d." % (b, a, a * v),
                      "Divide by %d: x > %d." % (a, v)], placeholder="a number")

    def two_step_le():
        a = random.randint(2, 5)
        v = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx - %d <= %d. The solution is x <= ___ . What number goes "
                     "in the blank?" % (a, b, a * v - b), v,
                     ["Add %d: %dx <= %d." % (b, a, a * v),
                      "Divide by %d: x <= %d." % (a, v)], placeholder="a number")

    def smallest_int():
        a = random.randint(2, 5)
        v = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx + %d > %d, then write down the smallest whole number "
                     "that x can be." % (a, b, a * v + b), v + 1,
                     ["The solution is x > %d, so the smallest whole number is %d."
                      % (v, v + 1)], placeholder="a number")

    def largest_int():
        a = random.randint(2, 5)
        v = random.randint(2, hi)
        b = random.randint(1, hi)
        return _numq("Solve %dx + %d < %d, then write down the largest whole number "
                     "that x can be." % (a, b, a * v + b), v - 1,
                     ["The solution is x < %d, so the largest whole number is %d."
                      % (v, v - 1)], placeholder="a number")

    def pin_solution():
        a = random.randint(2, 5)
        v = random.randint(2, hi)
        return _wordq("Solve %dx >= %d. Write your answer in the form x>=n with no "
                      "spaces, like x>=4." % (a, a * v), "x>=%d" % v,
                      ["Divide both sides by %d: x >= %d." % (a, v)],
                      placeholder="e.g. x>=4")

    def word_inequality():
        each = random.randint(2, 6)
        fixed = random.randint(1, 10)
        v = random.randint(3, hi)
        budget = each * v + fixed
        return _numq("Rides cost £%d each plus an entry fee of £%d. With £%d "
                     "you can afford at most how many rides? (Solve %dn + %d <= %d.)"
                     % (each, fixed, budget, each, fixed, budget), v,
                     ["%dn + %d <= %d, so %dn <= %d and n <= %d."
                      % (each, fixed, budget, each, budget - fixed, v)],
                     placeholder="number of rides")

    opts = [one_step_gt, one_step_lt, add_step, two_step, two_step_le,
            smallest_int, largest_int, word_inequality]
    if d == 0:
        opts = [one_step_gt, one_step_lt, add_step, smallest_int, largest_int]
    elif d == 2:
        opts = [two_step, two_step_le, smallest_int, largest_int, pin_solution,
                word_inequality]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.h -----
@skill("Y8.7.h", "Tables of values and plotting", S7)
def _(d=1):
    d = _t(d)
    m = _by_d(d, random.randint(1, 2), random.randint(1, 3), _nz(-3, 3))
    c = _by_d(d, random.randint(0, 3), _nz(-3, 4), _nz(-4, 4))
    r = 6

    def fill_table():
        xs = [-2, -1, 0, 1, 2, 3]
        rows = [[str(x), str(m * x + c)] for x in xs]
        i = random.randrange(len(xs))
        ans = m * xs[i] + c
        rows[i][1] = ""
        return _dtq("This table is for the line y = %s. Work out the missing y-value "
                    "when x = %d." % (_lin_str(m, c), xs[i]),
                    ["x", "y"], rows, ans,
                    ["Substitute x = %d: y = %d x %s %s = %d."
                     % (xs[i], m, _br(xs[i]), _pm(c), ans)],
                    missing=(i, 1), caption="y = %s" % _lin_str(m, c))

    def value_of_y():
        x = random.randint(-3, 4)
        return _numq("For the line y = %s, work out the value of y when x = %d."
                     % (_lin_str(m, c), x), m * x + c,
                     ["y = %d x %s %s = %d." % (m, _br(x), _pm(c), m * x + c)],
                     placeholder="y =")

    def value_of_x():
        x = random.randint(1, 4)
        y = m * x + c
        if m == 0:
            return value_of_y()
        return _numq("For the line y = %s, the value of y is %d. What is the matching "
                     "value of x?" % (_lin_str(m, c), y), x,
                     ["Solve %s = %d: %dx = %d, so x = %d."
                      % (_lin_str(m, c), y, m, y - c, x)], placeholder="x =")

    def plot_from_rule():
        x = random.randint(0, 3)
        y = m * x + c
        if not (-r <= y <= r):
            x, y = 0, c
        return _gridq("A table of values is built from y = %s. Work out the y-value when "
                      "x = %d, then plot the point (x, y)."
                      % (_lin_str(m, c), x), x, y,
                      ["When x = %d, y = %d x %d %s = %d." % (x, m, x, _pm(c), y),
                       "Plot (%d, %d)." % (x, y)], r=r)

    def complete_pair():
        x = random.randint(-2, 3)
        y = m * x + c
        return _numq("A table of values for y = %s includes the column x = %d. What is "
                     "the y-value in that column?" % (_lin_str(m, c), x), y,
                     ["y = %d x %s %s = %d." % (m, _br(x), _pm(c), y)], placeholder="y =")

    def which_point_on():
        if d == 0 and random.random() < 0.5:  # d1/d2 already include which_point_not
            return which_point_not()
        x = random.randint(1, 4)
        y = m * x + c
        return _wordq("Is the point (%d, %d) in the table of values for y = %s? Type yes "
                      "or no." % (x, y, _lin_str(m, c)), "yes",
                      ["When x = %d, y = %d x %d %s = %d, so yes."
                       % (x, m, x, _pm(c), y)], placeholder="yes or no")

    def which_point_not():
        x = random.randint(1, 4)
        y = m * x + c + 1
        return _wordq("Is the point (%d, %d) in the table of values for y = %s? Type yes "
                      "or no." % (x, y, _lin_str(m, c)), "no",
                      ["When x = %d, y should be %d, not %d, so no."
                       % (x, m * x + c, y)], placeholder="yes or no")

    def plot_simple():
        x = random.randint(0, 3)
        y = m * x + c
        if not (-r <= y <= r):
            x, y = 0, c
        return _gridq("A table of values for y = %s includes the point (%d, %d). Plot "
                      "this point." % (_lin_str(m, c), x, y), x, y,
                      ["Go to x = %d, y = %d and plot the point." % (x, y)], r=r)

    def indep_dep():
        # Identify independent and dependent variables.
        indep_desc, iv, dep_desc, dv = pick([
            ("the number of hours worked", "h", "the total pay", "p"),
            ("the number of tickets bought", "t", "the total cost", "c"),
            ("the time spent driving", "t", "the distance travelled", "d"),
            ("the number of days saved", "d", "the amount of money saved", "s"),
            ("the number of lengths swum", "n", "the time taken", "t")])
        if random.random() < 0.5:
            return _wordq("In a study, %s (%s) is worked out from %s (%s). Which is the "
                          "independent variable? Type its letter."
                          % (dep_desc, dv, indep_desc, iv), iv,
                          ["The independent variable is the one chosen or changed "
                           "freely, %s." % iv], placeholder="a letter")
        return _wordq("In a study, %s (%s) is worked out from %s (%s). Which is the "
                      "dependent variable? Type its letter."
                      % (dep_desc, dv, indep_desc, iv), dv,
                      ["The dependent variable is the one that responds to the other, "
                       "%s." % dv], placeholder="a letter")

    opts = [fill_table, value_of_y, value_of_x, complete_pair, which_point_on,
            which_point_not, plot_simple, plot_from_rule, indep_dep,
            fill_table, plot_simple, plot_from_rule]
    if d == 0:
        opts = [fill_table, value_of_y, complete_pair, which_point_on,
                plot_simple, plot_from_rule, fill_table, plot_simple, indep_dep]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.i -----
@skill("Y8.7.i", "Plot straight-line graphs y = mx + c", S7)
def _(d=1):
    d = _t(d)
    r = _by_d(d, 6, 6, 8)

    def _mc():
        m = pick([1, 2, -1, -2] if d == 2 else [1, 2, -1] if d == 1 else [1, 2])
        c = _by_d(d, random.randint(0, 2), random.randint(-2, 3), _nz(-3, 3))
        return m, c

    def _line_spec(m, c, label=True):
        pts = _line_points(m, c, r)
        p1, p2 = pts[0], pts[-1]
        line = {"p1": [p1[0], p1[1]], "p2": [p2[0], p2[1]]}
        if label:
            line["label"] = "y = %s" % _lin_str(m, c)
        return {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r, "ymax": r,
                "lines": [line]}

    def plot_on_line():
        m, c = _mc()
        pts = [p for p in _line_points(m, c, r) if -r + 1 <= p[0] <= r - 1]
        px, py = pick(pts)
        spec = _line_spec(m, c)
        return {"prompt": "The line y = %s is drawn. Plot the point on the line where "
                          "x = %d." % (_lin_str(m, c), px),
                "component": "coordinate_grid", "spec": spec,
                "answer": "(%d,%d)" % (px, py), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["When x = %d, y = %d x %s %s = %d."
                             % (px, m, _br(px), _pm(c), py),
                             "Plot (%d, %d), which lies on the line." % (px, py)]}

    def read_y():
        m, c = _mc()
        pts = [p for p in _line_points(m, c, r) if -r + 1 <= p[0] <= r - 1]
        px, py = pick(pts)
        spec = _line_spec(m, c)
        return {"prompt": "Use the line y = %s shown on the grid. What is the value of y "
                          "when x = %d?" % (_lin_str(m, c), px),
                "component": "coordinate_grid", "spec": spec,
                "answer": py, "answer_type": "int", "tolerance": 0,
                "solution": ["Read up from x = %d to the line: y = %d." % (px, py)]}

    def read_x():
        m, c = _mc()
        if m == 0:
            return read_y()
        pts = [p for p in _line_points(m, c, r) if -r + 1 <= p[1] <= r - 1]
        if not pts:
            return read_y()
        px, py = pick(pts)
        spec = _line_spec(m, c)
        return {"prompt": "Use the line y = %s shown on the grid. What is the value of x "
                          "when y = %d?" % (_lin_str(m, c), py),
                "component": "coordinate_grid", "spec": spec,
                "answer": px, "answer_type": "int", "tolerance": 0,
                "solution": ["Read across from y = %d to the line: x = %d." % (py, px)]}

    def plot_intercept():
        m, c = _mc()
        spec = _line_spec(m, c)
        return {"prompt": "The line y = %s is drawn. Plot the point where the line "
                          "crosses the y-axis." % _lin_str(m, c),
                "component": "coordinate_grid", "spec": spec,
                "answer": "(0,%d)" % c, "answer_type": "coord", "tolerance": 0,
                "solution": ["The line crosses the y-axis where x = 0, at (0, %d)." % c]}

    def plot_origin_side():
        m, c = _mc()
        pts = [p for p in _line_points(m, c, r) if -r + 1 <= p[0] <= r - 1
               and p[1] != 0]
        px, py = pick(pts)
        spec = _line_spec(m, c)
        return {"prompt": "The line y = %s is drawn. Plot the point on the line where "
                          "y = %d." % (_lin_str(m, c), py),
                "component": "coordinate_grid", "spec": spec,
                "answer": "(%d,%d)" % (px, py), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["Read along y = %d to the line: x = %d." % (py, px),
                             "Plot (%d, %d)." % (px, py)]}

    def plot_second_point():
        m, c = _mc()
        pts = [p for p in _line_points(m, c, r) if -r + 1 <= p[0] <= r - 1
               and p[0] != 0]
        px, py = pick(pts)
        spec = _line_spec(m, c, label=False)
        return {"prompt": "The line y = %s is drawn. Plot one more point that lies on "
                          "this line where x = %d." % (_lin_str(m, c), px),
                "component": "coordinate_grid", "spec": spec,
                "answer": "(%d,%d)" % (px, py), "answer_type": "coord",
                "tolerance": 0,
                "solution": ["When x = %d, y = %d, so plot (%d, %d)."
                             % (px, py, px, py)]}

    opts = [plot_on_line, read_y, read_x, plot_intercept, plot_origin_side,
            plot_second_point]
    if d == 0:
        opts = [read_y, plot_intercept, plot_on_line, plot_origin_side]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.j -----
@skill("Y8.7.j", "Gradient and y-intercept", S7)
def _(d=1):
    d = _t(d)
    r = _by_d(d, 6, 6, 8)

    def _mc():
        m = pick([1, 2] if d == 0 else [1, 2, -1] if d == 1 else [1, 2, -1, -2, 3])
        c = _by_d(d, random.randint(0, 2), _nz(-3, 3), _nz(-4, 4))
        return m, c

    def _spec(m, c, label=False):
        pts = _line_points(m, c, r)
        p1, p2 = pts[0], pts[-1]
        line = {"p1": [p1[0], p1[1]], "p2": [p2[0], p2[1]]}
        if label:
            line["label"] = "y = %s" % _lin_str(m, c)
        return {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r, "ymax": r,
                "lines": [line]}

    def gradient():
        m, c = _mc()
        return {"prompt": "A straight line is drawn on the grid. What is its gradient?",
                "component": "coordinate_grid", "spec": _spec(m, c),
                "answer": m, "answer_type": "int", "tolerance": 0,
                "solution": ["For every 1 unit right, the line goes %d %s."
                             % (abs(m), "up" if m > 0 else "down"),
                             "The gradient is %d." % m]}

    def intercept():
        m, c = _mc()
        return {"prompt": "A straight line is drawn on the grid. What is its y-intercept "
                          "(the y-value where it crosses the y-axis)?",
                "component": "coordinate_grid", "spec": _spec(m, c),
                "answer": c, "answer_type": "int", "tolerance": 0,
                "solution": ["The line crosses the y-axis at y = %d." % c]}

    def gradient_from_eqn():
        m = _nz(-6, 6)
        c = _nz(-9, 9)
        return _numq("What is the gradient of the line y = %s?" % _lin_str(m, c), m,
                     ["In y = mx + c the gradient is m, which is %d here." % m],
                     placeholder="gradient")

    def intercept_from_eqn():
        m = _nz(-6, 6)
        c = _nz(-9, 9)
        return _numq("What is the y-intercept of the line y = %s?" % _lin_str(m, c), c,
                     ["In y = mx + c the y-intercept is c, which is %d here." % c],
                     placeholder="y-intercept")

    def gradient_two_points():
        x1 = random.randint(-3, 1)
        x2 = x1 + random.randint(1, 3)
        m = _nz(-3, 3)
        c = _nz(-3, 3)
        y1, y2 = m * x1 + c, m * x2 + c
        return _numq("A line passes through (%d, %d) and (%d, %d). What is its gradient?"
                     % (x1, y1, x2, y2), m,
                     ["Gradient = change in y / change in x = (%d - %d)/(%d - %d) = %d."
                      % (y2, y1, x2, x1, m)], placeholder="gradient")

    def steeper():
        m1 = random.randint(1, 4)
        m2 = m1 + random.randint(1, 3)
        line = pick(["A", "B"])
        gA, gB = (m1, m2) if line == "B" else (m2, m1)
        return _wordq("Line A has gradient %d and line B has gradient %d. Which line is "
                      "steeper? Type A or B." % (gA, gB),
                      "B" if m2 == gB else "A",
                      ["The steeper line has the larger gradient (%d)." % m2],
                      placeholder="A or B")

    def parallel_gradient():
        m = _nz(-5, 5)
        c1 = _nz(-6, 6)
        c2 = _nz(-6, 6)
        while c2 == c1:
            c2 = _nz(-6, 6)
        return _numq("A line is parallel to y = %s. Parallel lines have the same "
                     "gradient. What is the gradient of the parallel line?"
                     % _lin_str(m, c1), m,
                     ["Parallel lines share a gradient, so it is %d." % m],
                     placeholder="gradient")

    def missing_coord_gradient():
        # Find a missing coordinate using the gradient (find y at a new x).
        m = _nz(-3, 3)
        x1 = random.randint(-3, 2)
        y1 = _nz(-4, 4)
        dx = random.randint(1, 3)
        x2 = x1 + dx
        y2 = y1 + m * dx
        return _numq("A line has gradient %d and passes through the point (%d, %d). "
                     "Another point on the line has x-coordinate %d. Use the gradient "
                     "to find its missing y-coordinate." % (m, x1, y1, x2), y2,
                     ["From x = %d to x = %d is %d to the right, so y changes by %d x %d "
                      "= %d." % (x1, x2, dx, m, dx, m * dx),
                      "y = %d + (%d) = %d." % (y1, m * dx, y2)],
                     placeholder="y-coordinate")

    def missing_coord_x():
        # Find a missing x-coordinate using the gradient.
        m = pick([1, 2, 3])
        x1 = random.randint(-3, 1)
        y1 = _nz(-4, 3)
        dx = random.randint(1, 3)
        x2 = x1 + dx
        y2 = y1 + m * dx
        return _numq("A line has gradient %d and passes through (%d, %d). Another point "
                     "on the line has y-coordinate %d. Use the gradient to find its "
                     "missing x-coordinate." % (m, x1, y1, y2), x2,
                     ["y goes from %d to %d, a rise of %d; with gradient %d that is a "
                      "run of %d." % (y1, y2, m * dx, m, dx),
                      "x = %d + %d = %d." % (x1, dx, x2)],
                     placeholder="x-coordinate")

    opts = [gradient, intercept, gradient_from_eqn, intercept_from_eqn,
            gradient_two_points, parallel_gradient, steeper,
            missing_coord_gradient, missing_coord_x]
    if d == 0:
        opts = [gradient, intercept, gradient_from_eqn, intercept_from_eqn,
                steeper, missing_coord_gradient]
    return pick(opts)()


# ----------------------------------------------------------------- 8.7.k -----
@skill("Y8.7.k", "Equation of a line; real-life linear graphs", S7)
def _(d=1):
    d = _t(d)

    def find_m_of_eqn():
        m = _nz(-6, 6)
        c = _nz(-9, 9)
        return _numq("The equation of a line is y = %s. It is written as y = mx + c. "
                     "What is the value of m?" % _lin_str(m, c), m,
                     ["m is the coefficient of x, which is %d." % m],
                     placeholder="value of m")

    def find_c_of_eqn():
        m = _nz(-6, 6)
        c = _nz(-9, 9)
        return _numq("The equation of a line is y = %s, written as y = mx + c. What is "
                     "the value of c?" % _lin_str(m, c), c,
                     ["c is the constant term, which is %d." % c],
                     placeholder="value of c")

    def eqn_from_m_c():
        m = random.randint(2, 6)
        c = random.randint(1, 8)
        return _wordq("A line has gradient %d and y-intercept %d. Write its equation in "
                      "the form y=mx+c with no spaces, like y=2x+3." % (m, c),
                      "y=%s" % _lin_str(m, c),
                      ["Put m = %d and c = %d into y = mx + c: y = %s."
                       % (m, c, _lin_str(m, c))], placeholder="e.g. y=2x+3")

    def taxi_rate():
        fixed = random.randint(2, 6)
        rate = random.randint(1, 5)
        miles = random.randint(3, 12)
        return _numq("A taxi graph is a straight line. The fare starts at £%d "
                     "(the y-intercept) and rises by £%d per mile (the gradient). "
                     "What is the fare for %d miles, in pounds?" % (fixed, rate, miles),
                     fixed + rate * miles,
                     ["Fare = %d + %d × %d = £%d."
                      % (fixed, rate, miles, fixed + rate * miles)], placeholder="pounds")

    def taxi_rate_gradient():
        fixed = random.randint(2, 6)
        rate = random.randint(1, 5)
        return _numq("A taxi charges a fixed fee of £%d plus £%d per mile. On "
                     "a distance-cost graph, what is the gradient of the line?"
                     % (fixed, rate), rate,
                     ["The gradient is the cost per mile, £%d." % rate],
                     placeholder="gradient")

    def taxi_intercept():
        fixed = random.randint(2, 8)
        rate = random.randint(1, 5)
        return _numq("A taxi charges a fixed fee of £%d plus £%d per mile. On "
                     "a distance-cost graph, what is the y-intercept (the cost of a "
                     "0-mile journey), in pounds?" % (fixed, rate), fixed,
                     ["The y-intercept is the fixed starting fee, £%d." % fixed],
                     placeholder="pounds")

    def tank_fill():
        start = random.randint(2, 10)
        rate = random.randint(2, 6)
        mins = random.randint(3, 10)
        return _numq("A tank starts with %d litres of water and fills at %d litres per "
                     "minute. This is modelled by a straight-line graph. How much water "
                     "is in the tank after %d minutes, in litres?" % (start, rate, mins),
                     start + rate * mins,
                     ["Water = %d + %d x %d = %d litres."
                      % (start, rate, mins, start + rate * mins)], placeholder="litres")

    def find_value_from_eqn():
        m = random.randint(2, 5)
        c = random.randint(1, 8)
        x = random.randint(2, 8)
        return _numq("A line has equation y = %s. What is the value of y when x = %d?"
                     % (_lin_str(m, c), x), m * x + c,
                     ["y = %d x %d + %d = %d." % (m, x, c, m * x + c)],
                     placeholder="y =")

    def gradient_from_two_readings():
        rate = random.randint(2, 6)
        t1 = random.randint(2, 3)
        t2 = t1 + random.randint(2, 4)
        base = random.randint(1, 5)
        d1 = base + rate * t1
        d2 = base + rate * t2
        return _numq("On a distance-time graph, a car is at %d km after %d hours and %d "
                     "km after %d hours. What is the gradient (the speed, in km per "
                     "hour)?" % (d1, t1, d2, t2), rate,
                     ["Gradient = (%d - %d)/(%d - %d) = %d km per hour."
                      % (d2, d1, t2, t1, rate)], placeholder="km per hour")

    opts = [find_m_of_eqn, find_c_of_eqn, eqn_from_m_c, taxi_rate,
            taxi_rate_gradient, taxi_intercept, tank_fill, find_value_from_eqn]
    if d == 0:
        opts = [find_m_of_eqn, find_c_of_eqn, taxi_rate, taxi_intercept,
                find_value_from_eqn]
    elif d == 2:
        opts = [eqn_from_m_c, taxi_rate, tank_fill, find_value_from_eqn,
                gradient_from_two_readings, taxi_rate_gradient]
    return pick(opts)()
