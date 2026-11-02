# Year 7 generators: strands 7.0 and 7.1 (KS3 programme of study, Year 7 part).
#
# KS3 is one statutory stage; Year 7 here is the entry layer used by common KS3 schemes:
# sequences (term-to-term, position-to-term, linear and other sequences) and algebraic notation
# (writing and reading expressions, substitution, function machines, formulae).
# Year 8 (y8_gen_*) carries the deeper KS3 work.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S0 = "7.0 Sequences"
S1 = "7.1 Algebraic notation"


def _lin(d):
    a = random.randint(_by(d, 1, -5, -20), _by(d, 20, 30, 50))
    step = random.choice([x for x in range(_by(d, 2, -9, -15), _by(d, 10, 12, 15) + 1) if x not in (0,)])
    if d == 0:
        step = abs(step)
    return a, step


def _nth(a, step):
    """nth term of the sequence a, a+step, ... as text: 3n + 2."""
    c = a - step
    sign = "+" if c > 0 else "−"
    if c == 0:
        return "%dn" % step
    return "%dn %s %d" % (step, sign, abs(c))


def _expr(coef, var, const=0):
    """3x + 2, x − 4, −2y, 5 (compact algebra text, no spaces)."""
    out = ""
    if coef:
        out = ("" if coef == 1 else "-" if coef == -1 else str(coef)) + var
    if const:
        out += ("+" if const > 0 and out else "") + str(const)
    return out or "0"


# ================================================================== 7.0 ======
@skill("Y7.0.a", "Continue a sequence using a term-to-term rule", S0)
def _(d=1):
    d = _d(d)
    a, step = _lin(d)
    terms = [a + i * step for i in range(5)]

    def t_next():
        return _tb("What is the next term in this sequence?  %s, ..." % ", ".join(map(str, terms)), a + 5 * step,
                   "int", {}, ["The term-to-term rule is %s %d." % ("add" if step > 0 else "subtract", abs(step))])

    def t_rule():
        return _wq("Describe the term-to-term rule for  %s, ...  (for example: add 4)"
                   % ", ".join(map(str, terms[:4])), "%s %d" % ("add" if step > 0 else "subtract", abs(step)),
                   ["Each term is %d %s than the one before." % (abs(step), "more" if step > 0 else "less")],
                   "add … / subtract …")

    def t_from_rule():
        k = random.randint(4, 7)
        return _tb("A sequence starts at %d and the rule is '%s %d'. What is term %d?"
                   % (a, "add" if step > 0 else "subtract", abs(step), k), a + (k - 1) * step, "int", {},
                   ["Term %d = %d + %d × %d = %d." % (k, a, k - 1, step, a + (k - 1) * step)])

    def t_missing():
        k = random.randint(1, 3)
        shown = ", ".join("___" if i == k else str(t) for i, t in enumerate(terms))
        return _tb("Find the missing term:  %s" % shown, terms[k], "int", {},
                   ["The step is %d." % step])

    def t_multiply():
        r = pick([2, 3, -2]) if d else 2
        b = random.randint(1, 5)
        t = [b * r ** i for i in range(4)]
        return _tb("The rule is 'multiply by %d'. What is the next term?  %s, ..." % (r, ", ".join(map(str, t))),
                   t[-1] * r, "int", {}, ["%d × %d = %d." % (t[-1], r, t[-1] * r)])

    def t_first_over():
        lim = a + step * random.randint(6, 12) + (abs(step) // 2 if step > 0 else 0)
        if step <= 0:
            return t_next()
        k = 0
        while a + k * step <= lim:
            k += 1
        return _tb("The sequence %s, ... keeps going. What is the first term greater than %d?"
                   % (", ".join(map(str, terms[:4])), lim), a + k * step, "int", {},
                   ["Keep adding %d until you pass %d." % (step, lim)])

    def t_table():
        rows = [[i + 1, t] for i, t in enumerate(terms)]
        k = random.randint(1, 4)
        return _io("The table shows the first five terms of a sequence. What is the missing term?", rows, k,
                   terms[k], ["The terms go %s in %ds." % ("up" if step > 0 else "down", abs(step))])

    return _pick_t([t_next, t_rule, t_from_rule, t_missing, t_multiply, t_first_over], [t_table])


@skill("Y7.0.b", "Use a position-to-term rule", S0)
def _(d=1):
    d = _d(d)
    m = random.randint(_by(d, 2, -5, -8), _by(d, 6, 9, 12))
    if m == 0:
        m = 3
    c = random.randint(_by(d, 0, -10, -20), _by(d, 10, 15, 25))
    rule = _expr(m, "n", c)

    def t_term():
        n = random.randint(_by(d, 1, 5, 10), _by(d, 10, 20, 100))
        return _tb("The nth term of a sequence is %s. What is term %d?" % (rule, n), m * n + c, "int", {},
                   ["Put n = %d: %d × %d %s %d = %d." % (n, m, n, "+" if c >= 0 else "−", abs(c), m * n + c)])

    def t_first_three():
        return _wq("Write the first three terms of the sequence with nth term %s, separated by commas." % rule,
                   ", ".join(str(m * n + c) for n in (1, 2, 3)), ["n = 1, 2, 3."], "e.g. 5, 8, 11")

    def t_is_term():
        n = random.randint(3, 30)
        v = m * n + c + pick([0, 0, 1])
        ok = (v - c) % m == 0 and (v - c) // m >= 1
        return _wq("Is %d a term in the sequence with nth term %s? (yes or no)" % (v, rule), "yes" if ok else "no",
                   ["%s = %d gives n = %s." % (rule, v, _fs(Fraction(v - c, m)))], "yes / no")

    def t_which_position():
        n = random.randint(3, 40)
        return _tb("In the sequence with nth term %s, which term is equal to %d?" % (rule, m * n + c), n, "int", {},
                   ["%s = %d, so n = %d." % (rule, m * n + c, n)])

    def t_table():
        rows = [[n, m * n + c] for n in (1, 2, 3, 10)]
        k = random.randrange(4)
        return _io("The rule is: term = %s. What goes in the empty cell?" % rule, rows, k, rows[k][1],
                   ["%d × %d %s %d = %d." % (m, rows[k][0], "+" if c >= 0 else "−", abs(c), rows[k][1])])

    return _pick_t([t_term, t_first_three, t_is_term, t_which_position], [t_table])


@skill("Y7.0.c", "Find the nth term of a linear sequence", S0)
def _(d=1):
    d = _d(d)
    a, step = _lin(d)
    terms = [a + i * step for i in range(5)]
    rule = _nth(a, step).replace(" ", "").replace("−", "-")

    def t_rule():
        return _wq("Find the nth term of  %s, ...  (write it like 3n+2)" % ", ".join(map(str, terms)), rule,
                   ["The step is %d, so it starts %dn." % (step, step),
                    "%d × 1 = %d; to get %d, %s %d." % (step, step, a, "add" if a - step >= 0 else "subtract",
                                                       abs(a - step))], "e.g. 3n+2")

    def t_coef():
        return _tb("The nth term of  %s, ...  is ?n + c. What is the number in front of n?"
                   % ", ".join(map(str, terms)), step, "int", {}, ["It is the common difference: %d." % step])

    def t_term100():
        return _tb("What is the 100th term of  %s, ...?" % ", ".join(map(str, terms)), a + 99 * step, "int", {},
                   ["nth term = %s." % _nth(a, step), "Put n = 100: %d." % (a + 99 * step)])

    def t_zeroth():
        return _tb("For the sequence  %s, ...  what is the constant c in the nth term %dn + c?"
                   % (", ".join(map(str, terms)), step), a - step, "int", {},
                   ["Term 0 would be %d − %d = %d." % (a, step, a - step)])

    def t_pattern():
        per, base = random.randint(2, 5), random.randint(1, 6)
        return _tb("Pattern 1 has %d sticks, pattern 2 has %d, pattern 3 has %d. Each new pattern adds the same number "
                   "of sticks. How many sticks are in pattern 20?" % (base + per, base + 2 * per, base + 3 * per),
                   base + 20 * per, "int", {"unit": "sticks"},
                   ["nth term = %dn + %d." % (per, base), "%d × 20 + %d = %d." % (per, base, base + 20 * per)])

    return _pick_t([t_rule, t_coef, t_term100, t_zeroth, t_pattern])


@skill("Y7.0.d", "Recognise linear, geometric and other sequences", S0)
def _(d=1):
    d = _d(d)

    def _kind():
        k = pick(["linear", "geometric", "square", "triangular", "fibonacci"])
        if k == "linear":
            a, s = random.randint(1, 20), random.randint(2, 9)
            return k, [a + i * s for i in range(5)]
        if k == "geometric":
            a, r = random.randint(1, 5), pick([2, 3, 10])
            return k, [a * r ** i for i in range(5)]
        if k == "square":
            return k, [i * i for i in range(1, 6)]
        if k == "triangular":
            return k, [i * (i + 1) // 2 for i in range(1, 6)]
        x, y = random.randint(1, 3), random.randint(1, 4)
        t = [x, y]
        for _ in range(3):
            t.append(t[-1] + t[-2])
        return k, t

    def t_type():
        k, t = _kind()
        if k in ("square", "triangular", "fibonacci"):
            return t_next_special()
        return _wq("Is the sequence %s, ... linear or geometric?" % ", ".join(map(str, t)), k,
                   ["Linear: add the same each time. Geometric: multiply by the same each time."], "linear / geometric")

    def t_next_special():
        k, t = _kind()
        if k == "linear":
            nxt = 2 * t[-1] - t[-2]
        elif k == "geometric":
            nxt = t[-1] * (t[1] // t[0])
        elif k == "square":
            nxt = 36
        elif k == "triangular":
            nxt = 21
        else:
            nxt = t[-1] + t[-2]
        return _tb("What is the next term?  %s, ..." % ", ".join(map(str, t)), nxt, "int", {},
                   [{"linear": "Same difference each time.", "geometric": "Same multiplier each time.",
                     "square": "These are square numbers: 6² = 36.", "triangular": "Add one more each time: 15 + 6 = 21.",
                     "fibonacci": "Add the two previous terms."}[k]])

    def t_ratio():
        a, r = random.randint(1, 6), pick([2, 3, 4, 5])
        t = [a * r ** i for i in range(4)]
        return _tb("What is the common ratio of the geometric sequence %s, ...?" % ", ".join(map(str, t)), r, "int", {},
                   ["%d ÷ %d = %d." % (t[1], t[0], r)])

    def t_name():
        t, k = pick([("1, 4, 9, 16, 25", "square"), ("1, 3, 6, 10, 15", "triangular"), ("1, 8, 27, 64", "cube")])
        return _wq("What are the numbers %s called? (one word: square, triangular or cube numbers)" % t, k,
                   ["They are the %s numbers." % k], "square / triangular / cube")

    def t_fib():
        x, y = random.randint(1, 5), random.randint(1, 6)
        t = [x, y]
        for _ in range(4):
            t.append(t[-1] + t[-2])
        k = random.randint(2, 5)
        shown = ", ".join("___" if i == k else str(v) for i, v in enumerate(t))
        return _tb("Each term is the sum of the two before it. Find the missing term:  %s" % shown, t[k], "int", {},
                   ["%d + %d = %d." % (t[k - 2], t[k - 1], t[k])])

    return _pick_t([t_type, t_next_special, t_ratio, t_name, t_fib])


@skill("Y7.0.e", "Sequences from patterns and in context", S0)
def _(d=1):
    d = _d(d)

    def t_tiles():
        add, start = random.randint(2, 6), random.randint(1, 8)
        n = random.randint(6, 15)
        return _tb("A tile pattern uses %d tiles in step 1, %d in step 2 and %d in step 3. How many tiles in step %d?"
                   % (start + add, start + 2 * add, start + 3 * add, n), start + add * n, "int", {"unit": "tiles"},
                   ["Each step adds %d: %d + %d × %d = %d." % (add, start, add, n, start + add * n)])

    def t_savings():
        s, w = random.randint(5, 40), random.randint(2, 10)
        n = random.randint(5, 20)
        who = _who()
        return _tb("%s has £%d and saves £%d each week. How much will %s have after %d weeks?" % (who, s, w, who, n),
                   s + w * n, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (s, w, n, s + w * n)])

    def t_tables():
        p, extra = random.randint(2, 4), random.randint(2, 4)
        n = random.randint(5, 12)
        return _tb("Square tables are pushed together in a row. 1 table seats %d people, 2 tables seat %d, 3 tables "
                   "seat %d. How many people can sit at %d tables?" % (p + extra, 2 * p + extra, 3 * p + extra, n),
                   p * n + extra, "int", {"unit": "people"}, ["Seats = %dn + %d." % (p, extra),
                                                              "%d × %d + %d = %d." % (p, n, extra, p * n + extra)])

    def t_which_step():
        add, start = random.randint(3, 7), random.randint(1, 10)
        n = random.randint(8, 25)
        return _tb("A pattern has %d dots in step 1 and gains %d dots each step. Which step has %d dots?"
                   % (start + add, add, start + add * n), n, "int", {}, ["%d + %dn = %d gives n = %d." % (start, add,
                                                                                                     start + add * n, n)])

    def t_cooling():
        t0, drop = random.randint(60, 90), random.randint(3, 8)
        k = random.randint(3, 8)
        return _tb("A cup of tea is %d °C and cools by %d degrees every minute for the first few minutes. What is its "
                   "temperature after %d minutes, in °C?" % (t0, drop, k), t0 - drop * k, "int", {"unit": "°C"},
                   ["%d − %d × %d = %d." % (t0, drop, k, t0 - drop * k)])

    return _pick_t([t_tiles, t_savings, t_tables, t_which_step, t_cooling])


# ================================================================== 7.1 ======
@skill("Y7.1.a", "Write expressions using algebraic notation", S1)
def _(d=1):
    d = _d(d)
    v = pick(["x", "y", "n", "a", "m"])
    k = random.randint(2, 9)
    c = random.randint(1, 12)

    def t_more():
        return _wq("Write an expression for %d more than %s." % (c, v), "%s+%d" % (v, c), ["%s + %d." % (v, c)],
                   "e.g. x+5")

    def t_less():
        return _wq("Write an expression for %d less than %s." % (c, v), "%s-%d" % (v, c), ["%s − %d." % (v, c)],
                   "e.g. x-5")

    def t_times():
        return _wq("Write an expression for %s multiplied by %d, in the shortest form." % (v, k), "%d%s" % (k, v),
                   ["%d × %s is written %d%s." % (k, v, k, v)], "e.g. 4x")

    def t_two_step():
        return _wq("Write an expression for: multiply %s by %d, then add %d." % (v, k, c), "%d%s+%d" % (k, v, c),
                   ["%d%s + %d." % (k, v, c)], "e.g. 3x+2")

    def t_bracket():
        return _wq("Write an expression for: add %d to %s, then multiply by %d." % (c, v, k), "%d(%s+%d)" % (k, v, c),
                   ["Brackets show the adding comes first: %d(%s + %d)." % (k, v, c)], "e.g. 2(x+3)")

    def t_divide():
        return _wq("Write an expression for %s divided by %d, using a slash (like x/3)." % (v, k), "%s/%d" % (v, k),
                   ["%s ÷ %d is written %s/%d." % (v, k, v, k)], "e.g. x/3")

    def t_word():
        who = _who()
        return _wq("%s has n sweets and is given %d more, then eats %d. Write an expression for how many sweets %s "
                   "has now, in its simplest form." % (who, c + k, k, who), "n+%d" % c,
                   ["n + %d − %d = n + %d." % (c + k, k, c)], "e.g. n+4")

    def t_perimeter():
        return _wq("A square has sides of length %s cm. Write an expression for its perimeter." % v, "4%s" % v,
                   ["%s + %s + %s + %s = 4%s." % (v, v, v, v, v)], "e.g. 4x")

    return _pick_t([t_more, t_less, t_times, t_two_step, t_bracket, t_divide, t_word, t_perimeter])


@skill("Y7.1.b", "Read algebraic notation (ab, 3y, a², a/b)", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(2, 9), random.randint(2, 9)

    def t_ab():
        return _tb("If a = %d and b = %d, what is ab?" % (a, b), a * b, "int", {}, ["ab means a × b = %d." % (a * b)])

    def t_3y():
        k = random.randint(2, 9)
        return _tb("If y = %d, what is %dy?" % (b, k), k * b, "int", {}, ["%dy means %d × y = %d." % (k, k, k * b)])

    def t_sq():
        return _tb("If a = %d, what is a²?" % a, a * a, "int", {}, ["a² means a × a = %d." % (a * a)])

    def t_cube():
        a2 = random.randint(2, 5)
        return _tb("If x = %d, what is x³?" % a2, a2 ** 3, "int", {}, ["x³ = x × x × x = %d." % a2 ** 3])

    def t_frac():
        q = random.randint(2, 9)
        return _tb("If a = %d and b = %d, what is a/b?" % (q * b, b), q, "int", {}, ["a/b means a ÷ b = %d." % q])

    def t_same():
        k = random.randint(3, 6)
        return _wq("Write  %s  in the shortest form." % " + ".join(["y"] * k), "%dy" % k,
                   ["%d lots of y is %dy." % (k, k)], "e.g. 4y")

    def t_a2b():
        a2, b2 = random.randint(2, 4), random.randint(2, 5)
        return _tb("If a = %d and b = %d, what is a²b?" % (a2, b2), a2 * a2 * b2, "int", {},
                   ["a²b = a × a × b = %d × %d × %d = %d." % (a2, a2, b2, a2 * a2 * b2)])

    def t_equivalent():
        return _q_equiv()

    return _pick_t([t_ab, t_3y, t_sq, t_cube, t_frac, t_same, t_a2b, t_equivalent])


def _q_equiv():
    q, ans, why = pick([("Is 3a the same as a + a + a?", "yes", "3a means 3 lots of a."),
                        ("Is a² the same as 2a?", "no", "a² = a × a, but 2a = a + a."),
                        ("Is ab the same as ba?", "yes", "Multiplication can be done in any order."),
                        ("Is a/b the same as b/a?", "no", "Division cannot be swapped."),
                        ("Is 2(a + 3) the same as 2a + 3?", "no", "2(a + 3) = 2a + 6.")])
    return _wq(q + " (yes or no)", ans, [why], "yes / no")


@skill("Y7.1.c", "Substitute into expressions", S1)
def _(d=1):
    d = _d(d)
    x = random.randint(_by(d, 1, -5, -9), _by(d, 10, 10, 12))
    y = random.randint(_by(d, 1, -3, -6), _by(d, 8, 9, 9))

    def t_linear():
        m, c = random.randint(2, 9), random.randint(1, 15)
        return _tb("Work out the value of %dx + %d when x = %d." % (m, c, x), m * x + c, "int", {},
                   ["%d × %d + %d = %d." % (m, x, c, m * x + c)])

    def t_two_vars():
        m, n = random.randint(2, 6), random.randint(2, 6)
        return _tb("Work out %da + %db when a = %d and b = %d." % (m, n, x, y), m * x + n * y, "int", {},
                   ["%d × %d + %d × %d = %d." % (m, x, n, y, m * x + n * y)])

    def t_square():
        return _tb("Work out x² + %d when x = %d." % (y, x), x * x + y, "int", {}, ["%d² = %d; + %d = %d." % (x, x * x, y,
                                                                                                         x * x + y)])

    def t_bracket():
        m, c = random.randint(2, 6), random.randint(1, 9)
        return _tb("Work out %d(x + %d) when x = %d." % (m, c, x), m * (x + c), "int", {},
                   ["%d + %d = %d; × %d = %d." % (x, c, x + c, m, m * (x + c))])

    def t_subtract():
        m, c = random.randint(2, 9), random.randint(1, 20)
        return _tb("Work out %d − %dx when x = %d." % (c, m, x), c - m * x, "int", {},
                   ["%d − %d × %d = %d." % (c, m, x, c - m * x)])

    def t_table():
        m, c = random.randint(2, 6), random.randint(-5, 9)
        rows = [[v, m * v + c] for v in (1, 2, 5, 10)]
        k = random.randrange(4)
        return _io("Complete the table for y = %s." % _expr(m, "x", c).replace("+", " + ").replace("-", " − "), rows,
                   k, rows[k][1], ["%d × %d %s %d = %d." % (m, rows[k][0], "+" if c >= 0 else "−", abs(c), rows[k][1])])

    return _pick_t([t_linear, t_two_vars, t_square, t_bracket, t_subtract], [t_table])


@skill("Y7.1.d", "Function machines and inverse operations", S1)
def _(d=1):
    d = _d(d)
    m, c = random.randint(2, 9), random.randint(1, 20)
    x = random.randint(1, 15)

    def t_output():
        return _tb("A function machine does: × %d, then + %d. What comes out when %d goes in?" % (m, c, x), m * x + c,
                   "int", {}, ["%d × %d = %d; + %d = %d." % (x, m, m * x, c, m * x + c)])

    def t_input():
        return _tb("A function machine does: × %d, then + %d. %d comes out. What went in?" % (m, c, m * x + c), x, "int",
                   {}, ["Work backwards: − %d, then ÷ %d." % (c, m), "(%d − %d) ÷ %d = %d." % (m * x + c, c, m, x)])

    def t_order_matters():
        return _tb("A function machine does: + %d, then × %d. What comes out when %d goes in?" % (c, m, x), (x + c) * m,
                   "int", {}, ["%d + %d = %d; × %d = %d." % (x, c, x + c, m, (x + c) * m)])

    def t_expression():
        return _wq("A function machine does: × %d, then − %d. Write the output when x goes in." % (m, c),
                   "%dx-%d" % (m, c), ["x × %d − %d = %dx − %d." % (m, c, m, c)], "e.g. 3x-2")

    def t_find_rule():
        rows = [[v, m * v] for v in (1, 2, 5, 8)]
        return _io("A function machine multiplies by a number. What is that number?", rows, None, m,
                   ["%d ÷ %d = %d." % (rows[1][1], rows[1][0], m)])

    def t_table():
        rows = [[v, m * v + c] for v in (1, 3, 4, 10)]
        k = random.randrange(4)
        return _io("The machine is: × %d, then + %d. What goes in the empty cell?" % (m, c), rows, k, rows[k][1],
                   ["%d × %d + %d = %d." % (rows[k][0], m, c, rows[k][1])], rule="× %d, + %d" % (m, c))

    return _pick_t([t_output, t_input, t_order_matters, t_expression], [t_find_rule, t_table])


@skill("Y7.1.e", "Use formulae given in words and symbols", S1)
def _(d=1):
    d = _d(d)

    def t_cost():
        fee, per, h = random.randint(5, 30), random.randint(3, 12), random.randint(2, 8)
        return _tb("A plumber charges £%d to call plus £%d for each hour. How much for %d hours, in pounds?"
                   % (fee, per, h), fee + per * h, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (fee, per, h, fee + per * h)])

    def t_symbols():
        l, w = random.randint(3, 20), random.randint(2, 15)
        return _tb("The formula for the perimeter of a rectangle is P = 2l + 2w. Find P when l = %d and w = %d." % (l, w),
                   2 * l + 2 * w, "int", {}, ["2 × %d + 2 × %d = %d." % (l, w, 2 * l + 2 * w)])

    def t_area():
        b, h = random.randint(2, 12) * 2, random.randint(2, 12)
        return _tb("The area of a triangle is A = bh/2. Find A when b = %d and h = %d." % (b, h), b * h // 2, "int", {},
                   ["%d × %d ÷ 2 = %d." % (b, h, b * h // 2)])

    def t_speed():
        s, t = random.randint(3, 12) * 10, random.randint(2, 5)
        return _tb("Distance = speed × time. A car travels at %d km/h for %d hours. How far does it go, in km?" % (s, t),
                   s * t, "int", {"unit": "km"}, ["%d × %d = %d." % (s, t, s * t)])

    def t_write():
        per, fee = random.randint(2, 9), random.randint(3, 20)
        return _wq("A taxi charges £%d plus £%d per mile. Write a formula for the cost C in pounds for m miles, like "
                   "C=2m+5." % (fee, per), "C=%dm+%d" % (per, fee), ["C = %dm + %d." % (per, fee)], "e.g. C=2m+5")

    def t_reverse():
        fee, per = random.randint(5, 20), random.randint(2, 9)
        h = random.randint(2, 9)
        return _tb("A hall costs £%d plus £%d per hour. A booking cost £%d. How many hours was it?"
                   % (fee, per, fee + per * h), h, "int", {"unit": "hours"},
                   ["(%d − %d) ÷ %d = %d." % (fee + per * h, fee, per, h)])

    return _pick_t([t_cost, t_symbols, t_area, t_speed, t_write, t_reverse])


@skill("Y7.1.f", "Vocabulary: expressions, equations, formulae, terms", S1)
def _(d=1):
    d = _d(d)

    def t_classify():
        item, ans = pick([("3x + 5", "expression"), ("3x + 5 = 20", "equation"), ("A = lw", "formula"),
                          ("2a − b", "expression"), ("y = mx + c", "formula"), ("x − 4 = 9", "equation"),
                          ("x > 7", "inequality")])
        return _wq("Is  %s  an expression, an equation, a formula or an inequality?" % item, ans,
                   ["An expression has no equals sign; an equation can be solved; a formula links quantities; an "
                    "inequality uses < or >."], "expression / equation / formula / inequality")

    def t_terms():
        k = random.randint(2, 5)
        terms = random.sample(["3x", "5", "y²", "2ab", "7y", "x", "9"], k)
        return _tb("How many terms are in the expression  %s ?" % " + ".join(terms), k, "int", {},
                   ["The terms are %s." % ", ".join(terms)])

    def t_coef():
        m = random.randint(2, 12)
        v = pick(["x", "y", "p"])
        c = random.randint(1, 9)
        return _tb("What is the coefficient of %s in  %d%s + %d ?" % (v, m, v, c), m, "int", {},
                   ["The coefficient is the number multiplying %s: %d." % (v, m)])

    def t_constant():
        m, c = random.randint(2, 9), random.randint(1, 20)
        return _tb("What is the constant term in  %dx + %d ?" % (m, c), c, "int", {}, ["The term with no letter: %d." % c])

    def t_like():
        a, b = random.sample(["3x", "4y", "x²", "5x", "2xy", "7"], 2)
        like = a.lstrip("0123456789") == b.lstrip("0123456789")
        return _wq("Are %s and %s like terms? (yes or no)" % (a, b), "yes" if like else "no",
                   ["Like terms have exactly the same letters and powers."], "yes / no")

    return _pick_t([t_classify, t_terms, t_coef, t_constant, t_like])
