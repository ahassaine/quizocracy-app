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
    step = random.choice([x for x in range(_by(d, 2, -9, -15), _by(d, 10, 12, 15) + 1) if x not in (0, 1, -1)])
    if d == 0:
        # the easiest tier is still Year 7: not a times-table count such as 10, 20, 30 or 0, 6, 12
        step = pick([3, 4, 6, 7, 8, 9, 11, 12])
        a = random.choice([v for v in range(2, 31) if v % step])
    elif a % step == 0:                 # nor at the harder tiers (11, 22, 33, 44)
        a += random.randint(1, abs(step) - 1)
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
        r = pick([2, 3, 4]) if d else 2             # multiplying by a negative waits for strand 7.6
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
    m = random.randint(_by(d, 2, 2, 3), _by(d, 6, 9, 12))       # a negative n coefficient waits for strand 7.6
    if m == 0:
        m = 3
    c = max(random.randint(_by(d, 0, -10, -20), _by(d, 10, 15, 25)), 1 - m)    # 4n − 3 yes; a term below 0, not yet
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
    step = abs(step)                    # an nth term like −6n + 20 needs directed numbers (strand 7.6) ...
    if a - step < 0:                    # ... and so does a constant below 0: 3n − 2 is written, not asked for
        a = step + random.randint(0, 20)
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

    def t_nth_given():
        n = random.randint(6, _by(d, 12, 25, 60))
        return _tb("The nth term of a sequence is %s. What is term number %d?" % (_nth(a, step), n), a + (n - 1) * step,
                   "int", {}, ["Put n = %d into %s: %d." % (n, _nth(a, step), a + (n - 1) * step)])

    def t_first_terms():
        return _wq("Write the first three terms of the sequence with nth term %s, with commas (like 5, 8, 11)."
                   % _nth(a, step), "%d, %d, %d" % (a, a + step, a + 2 * step),
                   ["n = 1, 2 and 3 give %d, %d and %d." % (a, a + step, a + 2 * step)], "e.g. 5, 8, 11")

    def t_in_sequence():
        k = random.randint(8, 30)
        v = a + (k - 1) * step + pick([0, 0, 1])
        inside = (v - a) % step == 0
        return _wq("Is %d a term of the sequence  %s, ...? (yes or no)" % (v, ", ".join(map(str, terms))),
                   "yes" if inside else "no",
                   ["nth term = %s." % _nth(a, step),
                    ("%d − %d = %d, which is %d steps of %d, so yes." % (v, a, v - a, (v - a) // step, step)) if inside else
                    ("%d − %d = %d, which is not a whole number of steps of %d, so no." % (v, a, v - a, step))], "yes / no")

    def t_which_term():
        k = random.randint(10, _by(d, 30, 50, 120))
        v = a + (k - 1) * step
        return _tb("Which term of  %s, ...  is %d?" % (", ".join(map(str, terms)), v), k, "int", {},
                   ["nth term = %s." % _nth(a, step), "%s = %d gives n = %d." % (_nth(a, step), v, k)])

    def t_gap_term():
        return _tb("Find the missing term:  %d, %d, ?, %d, %d" % (terms[0], terms[1], terms[3], terms[4]), terms[2],
                   "int", {}, ["The step is %d: %d + %d = %d." % (step, terms[1], step, terms[2])])

    def t_first_over():
        lim = a + random.randint(15, 40) * step + random.randint(1, step - 1)
        k = (lim - a) // step + 2
        return _tb("The nth term of a sequence is %s. Which is the first term number whose value is more than %d?"
                   % (_nth(a, step), lim), k, "int", {},
                   ["Term %d is %d and term %d is %d." % (k - 1, a + (k - 2) * step, k, a + (k - 1) * step)])

    return _pick_t([t_rule, t_coef, t_term100, t_zeroth, t_pattern, t_nth_given, t_first_terms, t_in_sequence,
                    t_which_term, t_gap_term, t_first_over])


@skill("Y7.0.d", "Recognise linear, geometric and other sequences", S0)
def _(d=1):
    d = _d(d)

    def _kind():
        k = pick(["linear", "geometric", "square", "triangular", "fibonacci"])
        if k == "linear":
            a, s = random.randint(1, _by(d, 10, 20, 50)), random.randint(_by(d, 2, 2, 3), _by(d, 5, 9, 15))
            return k, [a + i * s for i in range(5)]
        if k == "geometric":
            a, r = random.randint(1, _by(d, 3, 5, 6)), pick(_by(d, [2, 10], [2, 3, 10], [2, 3, 4, 5]))
            return k, [a * r ** i for i in range(5)]
        if k == "square":
            return k, [i * i for i in range(1, 6)]
        if k == "triangular":
            return k, [i * (i + 1) // 2 for i in range(1, 6)]
        x, y = random.randint(1, _by(d, 2, 3, 9)), random.randint(1, _by(d, 3, 4, 12))
        t = [x, y]
        for _ in range(3):
            t.append(t[-1] + t[-2])
        return k, t

    def t_type():
        k, t = _kind()
        if k in ("square", "triangular", "fibonacci"):
            return _next_q(k, t)                         # the type already drawn, not a fresh draw
        return _wq("Is the sequence %s, ... linear or geometric?" % ", ".join(map(str, t)), k,
                   ["Linear: add the same each time. Geometric: multiply by the same each time."], "linear / geometric")

    def t_next_special():
        return _next_q(*_kind())

    def _next_q(k, t):
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
        a, r = random.randint(1, _by(d, 5, 6, 12)), pick(_by(d, [2, 3, 10], [2, 3, 4, 5], [3, 4, 5, 6]))
        t = [a * r ** i for i in range(4)]
        return _tb("What is the common ratio of the geometric sequence %s, ...?" % ", ".join(map(str, t)), r, "int", {},
                   ["%d ÷ %d = %d." % (t[1], t[0], r)])

    def t_name():
        t, k = pick([("1, 4, 9, 16, 25", "square"), ("1, 3, 6, 10, 15", "triangular"), ("1, 8, 27, 64", "cube")])
        return _wq("What are the numbers %s called? (one word: square, triangular or cube numbers)" % t, k,
                   ["They are the %s numbers." % k], "square / triangular / cube")

    def t_fib():
        x, y = random.randint(1, _by(d, 3, 5, 12)), random.randint(1, _by(d, 4, 6, 15))
        t = [x, y]
        for _ in range(4):
            t.append(t[-1] + t[-2])
        k = random.randint(_by(d, 2, 2, 0), 5)          # stretch: an early term, found by working backwards
        shown = ", ".join("___" if i == k else str(v) for i, v in enumerate(t))
        how = "%d + %d = %d." % (t[k - 2], t[k - 1], t[k]) if k >= 2 else "%d − %d = %d." % (t[k + 2], t[k + 1], t[k])
        return _tb("Each term is the sum of the two before it. Find the missing term:  %s" % shown, t[k], "int", {}, [how])

    def t_geo_term():
        a, r = random.randint(1, 5), pick([2, 3])
        k = random.randint(_by(d, 3, 5, 6), _by(d, 4, 7, 8))
        return _tb("A geometric sequence starts at %d and each term is %d times the one before. What is term %d?" % (a, r, k),
                   a * r ** (k - 1), "int", {}, ["%d × %d^%d = %d." % (a, r, k - 1, a * r ** (k - 1))])

    def t_halving():
        end = random.randint(1, 9) * pick([1, 3, 5])
        t = [end * 2 ** (5 - i) for i in range(5)]
        return _tb("What is the next term?  %s, ..." % ", ".join(map(str, t)), end, "int", {},
                   ["Each term is half the one before: %d ÷ 2 = %d." % (t[-1], end)])

    def t_nth_special():
        k, n = pick([("square", random.randint(_by(d, 4, 9, 13), _by(d, 10, 15, 20))),
                     ("triangular", random.randint(_by(d, 4, 6, 10), _by(d, 7, 12, 20))),
                     ("cube", random.randint(_by(d, 2, 4, 6), _by(d, 5, 7, 10)))])
        v = {"square": n * n, "triangular": n * (n + 1) // 2, "cube": n ** 3}[k]
        how = {"square": "%d × %d" % (n, n), "triangular": "%d × %d ÷ 2" % (n, n + 1), "cube": "%d × %d × %d" % (n, n, n)}[k]
        return _tb("What is the %s %s number?" % (_ord(n), k), v, "int", {}, ["%s = %d." % (how, v)])

    def t_not_square():
        sq = random.sample([x * x for x in range(_by(d, 2, 3, 6), _by(d, 11, 13, 16))], 3)
        odd = pick([x for x in range(10, _by(d, 101, 145, 226)) if int(x ** 0.5) ** 2 != x])
        shown = sq + [odd]
        random.shuffle(shown)
        return _tb("Which of these is NOT a square number?  %s" % ", ".join(map(str, shown)), odd, "int", {},
                   ["%s are square numbers." % ", ".join(map(str, sorted(sq)))])

    def t_linear_table():
        lin = random.random() < 0.5
        a = random.randint(1, _by(d, 9, 9, 30))
        s = random.randint(2, _by(d, 5, 6, 12))
        vals = [a + s * i for i in range(5)] if lin else [a * 2 ** i for i in range(5)]
        return _io("The table shows the first five terms of a sequence. Is the sequence linear? (yes or no)",
                   [[i + 1, v] for i, v in enumerate(vals)], None, "yes" if lin else "no",
                   ["%s." % ("The terms go up by %d each time" % s if lin else "The differences are not the same")], atype="str")

    def t_increasing():
        a, r = random.randint(2, 6), pick(_by(d, [2, 3], [2, 3], [2, 3, 4]))
        neg = random.random() < _by(d, 0, 0.5, 0.7)     # easy: increasing only, so the ratio is a whole number
        t = [a * r ** i for i in range(4)] if not neg else [a * r ** 3 // r ** i for i in range(4)]
        return _tb("Find the common ratio of %s, ... (it may be a fraction)" % ", ".join(map(str, t)),
                   _fs(Fraction(t[1], t[0])), "frac", {"text": True, "placeholder": "e.g. 3 or 1/2"},
                   ["%d ÷ %d = %s." % (t[1], t[0], _fs(Fraction(t[1], t[0])))])

    return _pick_t(_by(d, [t_type, t_next_special, t_ratio, t_name, t_fib, t_halving, t_nth_special, t_not_square],
                       [t_type, t_next_special, t_ratio, t_name, t_fib, t_geo_term, t_halving, t_nth_special, t_not_square,
                        t_increasing],
                       [t_type, t_next_special, t_ratio, t_fib, t_geo_term, t_nth_special, t_not_square, t_increasing]),
                   [t_linear_table])


def _ord(n):
    return "%d%s" % (n, "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


@skill("Y7.0.e", "Sequences from patterns and in context", S0)
def _(d=1):
    d = _d(d)

    def t_tiles():
        add, start = random.randint(2, _by(d, 5, 6, 9)), random.randint(1, 8)
        n = random.randint(_by(d, 4, 6, 20), _by(d, 10, 15, 50))
        return _tb("A tile pattern uses %d tiles in step 1, %d in step 2 and %d in step 3. How many tiles in step %d?"
                   % (start + add, start + 2 * add, start + 3 * add, n), start + add * n, "int", {"unit": "tiles"},
                   ["Each step adds %d: %d + %d × %d = %d." % (add, start, add, n, start + add * n)])

    def t_savings():
        s, w = random.randint(5, _by(d, 20, 40, 90)), random.randint(2, _by(d, 5, 10, 15))
        n = random.randint(_by(d, 3, 5, 12), _by(d, 10, 20, 52))
        who = _who()
        return _tb("%s has £%d and saves £%d each week. How much will %s have after %d weeks?" % (who, s, w, who, n),
                   s + w * n, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (s, w, n, s + w * n)])

    def t_tables():
        p, extra = random.randint(2, 4), random.randint(2, 4)
        n = random.randint(_by(d, 4, 5, 15), _by(d, 8, 12, 40))
        return _tb("Tables are pushed together in a row. 1 table seats %d people, 2 tables seat %d, 3 tables "
                   "seat %d. How many people can sit at %d tables?" % (p + extra, 2 * p + extra, 3 * p + extra, n),
                   p * n + extra, "int", {"unit": "people"}, ["Seats = %dn + %d." % (p, extra),
                                                              "%d × %d + %d = %d." % (p, n, extra, p * n + extra)])

    def t_which_step():
        add, start = random.randint(3, _by(d, 5, 7, 12)), random.randint(1, 10)
        n = random.randint(_by(d, 4, 8, 20), _by(d, 10, 25, 60))
        return _tb("A pattern has %d dots in step 1 and gains %d dots each step. Which step has %d dots?"
                   % (start + add, add, start + add * n), n, "int", {}, ["%d + %dn = %d gives n = %d." % (start, add,
                                                                                                     start + add * n, n)])

    def t_cooling():
        t0, drop = random.randint(60, 90), random.randint(3, 8)
        k = random.randint(3, min(8, (t0 - 25) // drop))
        return _tb("A cup of tea is %d °C and cools by %d degrees every minute for the first few minutes. What is its "
                   "temperature after %d minutes, in °C?" % (t0, drop, k), t0 - drop * k, "int", {"unit": "°C"},
                   ["%d − %d × %d = %d." % (t0, drop, k, t0 - drop * k)])

    def t_sticks_table():
        add, start = random.randint(2, 5), random.randint(1, 4)
        n = pick(_by(d, [5, 6, 8, 10], [10, 12, 15, 20], [25, 30, 40, 50]))
        rows = [[k, start + add * k] for k in (1, 2, 3, n)]
        return _io("A matchstick pattern: the table shows the pattern number and the number of matchsticks. What goes in the "
                   "empty cell?", rows, 3, start + add * n,
                   ["Each pattern adds %d: sticks = %dn + %d." % (add, add, start), "%d × %d + %d = %d." % (add, n, start, start + add * n)])

    def t_theatre():
        first, more = random.randint(12, 24), random.randint(1, 3)
        r = random.randint(8, 20)
        return _tb("In a theatre, row 1 has %d seats and each row has %d more seat%s than the row in front. How many seats are "
                   "in row %d?" % (first, more, "" if more == 1 else "s", r), first + more * (r - 1), "int", {"unit": "seats"},
                   ["%d + %d × %d = %d." % (first, more, r - 1, first + more * (r - 1))])

    def t_bounce():
        h = pick([160, 320, 240, 480, 128])
        k = random.randint(_by(d, 1, 2, 3), _by(d, 2, 4, 5))
        return _tb("A ball is dropped from %d cm. Each bounce reaches half the height of the one before. How high is bounce "
                   "%d, in cm?" % (h, k), _ds(Fraction(h, 2 ** k)), "num", {"unit": "cm"},
                   ["Halve %d times: %d ÷ %d = %s." % (k, h, 2 ** k, _ds(Fraction(h, 2 ** k)))])

    def t_doubling():
        s = pick([5, 10, 20, 25, 50])
        k = random.randint(_by(d, 2, 3, 5), _by(d, 4, 6, 8))
        return _tb("A number of cells doubles every hour. There are %d cells at the start. How many after %d hours?" % (s, k),
                   s * 2 ** k, "int", {"unit": "cells"}, ["%d × 2^%d = %d." % (s, k, s * 2 ** k)])

    def t_formula():
        add, start = random.randint(2, _by(d, 5, 6, 12)), random.randint(1, _by(d, 5, 9, 20))
        return _wq("A pattern has %d tiles in pattern 1, %d in pattern 2 and %d in pattern 3. Write a formula for the number "
                   "of tiles T in pattern n, like T=3n+2." % (start + add, start + 2 * add, start + 3 * add),
                   "T=%dn+%d" % (add, start), ["Goes up %d each time, so %dn; %d × 1 + %d = %d." % (add, add, add, start, start + add)],
                   "e.g. T=3n+2")

    def t_savings_graph():
        s, w = random.randint(0, 6) * 5, random.randint(2, _by(d, 4, 8, 8)) * 5
        pts = [("Wk %d" % k, s + w * k) for k in range(5)]
        wk = 10 if d == 1 else (6 if d == 0 else pick([15, 20, 26]))
        return _lg("The graph shows how much is in a savings jar each week. The same amount is added every week. How much "
                   "will be in the jar in week %d, in pounds?" % wk, pts, s + w * wk,
                   ["%d is added each week." % w, "%d + %d × %d = %d." % (s, w, wk, s + w * wk)], "£", "Week")

    def t_taxi_over():
        fee, per = random.randint(2, 5), random.randint(2, _by(d, 3, 3, 4))
        lim = random.randint(_by(d, 12, 20, 40), _by(d, 25, 40, 90))
        k = (lim - fee) // per + 1
        return _tb("A taxi costs £%d plus £%d for each mile. What is the smallest whole number of miles for which the fare is "
                   "more than £%d?" % (fee, per, lim), k, "int", {"unit": "miles"},
                   ["%d + %d × %d = %d, which is not more than %d." % (fee, per, k - 1, fee + per * (k - 1), lim),
                    "%d + %d × %d = %d." % (fee, per, k, fee + per * k)])

    return _pick_t(_by(d, [t_tiles, t_savings, t_tables, t_cooling, t_theatre, t_bounce, t_doubling],
                       [t_tiles, t_savings, t_tables, t_which_step, t_cooling, t_theatre, t_bounce, t_doubling, t_formula,
                        t_taxi_over],
                       [t_tiles, t_savings, t_tables, t_which_step, t_theatre, t_bounce, t_doubling, t_formula, t_taxi_over]),
                   [t_sticks_table, t_savings_graph])


# ================================================================== 7.1 ======
@skill("Y7.1.a", "Write expressions using algebraic notation", S1)
def _(d=1):
    d = _d(d)
    v = pick(["x", "y", "n", "a", "m"])
    k = random.randint(2, _by(d, 5, 9, 12))
    c = random.randint(1, _by(d, 10, 12, 30))

    def t_more():
        return _wq("Write an expression for %d more than %s. Write the letter first." % (c, v), "%s+%d" % (v, c), ["%s + %d." % (v, c)],
                   "e.g. x+5")

    def t_less():
        return _wq("Write an expression for %d less than %s." % (c, v), "%s-%d" % (v, c),
                   ["“%d less than %s” means start at %s and take %d away: %s − %d." % (c, v, v, c, v, c),
                    "%d − %s would be the other way round: %s less than %d." % (c, v, v, c)],
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
        # the same idea in many settings, so the sentence is not the same one every day with a new letter
        part = {2: "half", 3: "a third", 4: "a quarter", 5: "a fifth", 6: "a sixth", 7: "a seventh", 8: "an eighth",
                9: "a ninth", 10: "a tenth", 11: "an eleventh", 12: "a twelfth"}[k]
        who = _who()
        u = "n" if v == "a" else v                    # "Sara has a stickers" would read as English
        ask = pick([
            "Write an expression for %s divided by %d, using a slash (like x/3)." % (u, k),
            "Write %s of %s as an expression. Use a slash for dividing." % (part, u),
            "%s has %s stickers and shares them equally between %d friends. Write an expression for how many "
            "each friend gets (use / for divide)." % (who, u, k),
            "A ribbon %s cm long is cut into %d equal pieces. Write an expression for the length of one piece, "
            "using a slash." % (u, k),
            "%d tickets cost %s pounds altogether. Write an expression for the cost of one ticket in pounds, "
            "using / to divide." % (k, u),
            "Write the expression for: think of a number %s, then divide it by %d. Use a slash." % (u, k),
        ])
        return _wq(ask, "%s/%d" % (u, k),
                   ["Dividing by %d, or splitting into %d equal parts, is %s ÷ %d. In algebra it is written %s/%d."
                    % (k, k, u, k, u, k)], "e.g. x/3")

    def t_word():
        who = _who()
        return _wq("%s has n sweets and is given %d more, then eats %d. Write an expression for how many sweets %s "
                   "has now, in its simplest form." % (who, c + k, k, who), "n+%d" % c,
                   ["n + %d − %d = n + %d." % (c + k, k, c)], "e.g. n+4")

    def t_perimeter():
        return _wq("A square has sides of length %s cm. Write an expression for its perimeter." % v, "4%s" % v,
                   ["%s + %s + %s + %s = 4%s." % (v, v, v, v, v)], "e.g. 4x")

    def t_from():
        n = c + k
        return _wq("Write an expression for %s subtracted from %d." % (v, n), "%d-%s" % (n, v),
                   ["Start with %d and take away %s: %d − %s." % (n, v, n, v)], "e.g. 10-x")

    def t_two_step_sub():
        return _wq("Write an expression for: multiply %s by %d, then subtract %d." % (v, k, c), "%d%s-%d" % (k, v, c),
                   ["%d%s − %d." % (k, v, c)], "e.g. 3x-2")

    return _pick_t(_by(d, [t_more, t_less, t_times, t_divide, t_perimeter],
                       [t_more, t_less, t_times, t_two_step, t_bracket, t_divide, t_word, t_perimeter],
                       [t_two_step, t_two_step_sub, t_bracket, t_divide, t_word, t_from]))


@skill("Y7.1.b", "Read algebraic notation (ab, 3y, a², a/b)", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(2, _by(d, 5, 9, 12)), random.randint(2, _by(d, 5, 9, 12))

    def t_ab():
        return _tb("If a = %d and b = %d, what is ab?" % (a, b), a * b, "int", {}, ["ab means a × b = %d." % (a * b)])

    def t_3y():
        k = random.randint(2, _by(d, 5, 9, 15))
        return _tb("If y = %d, what is %dy?" % (b, k), k * b, "int", {}, ["%dy means %d × y = %d." % (k, k, k * b)])

    def t_sq():
        return _tb("If a = %d, what is a²?" % a, a * a, "int", {}, ["a² means a × a = %d." % (a * a)])

    def t_cube():
        a2 = random.randint(2, _by(d, 3, 5, 6))
        return _tb("If x = %d, what is x³?" % a2, a2 ** 3, "int", {}, ["x³ = x × x × x = %d." % a2 ** 3])

    def t_frac():
        q = random.randint(2, 9)
        return _tb("If a = %d and b = %d, what is a/b?" % (q * b, b), q, "int", {}, ["a/b means a ÷ b = %d." % q])

    def t_same():
        k = random.randint(3, _by(d, 5, 6, 8))
        return _wq("Write  %s  in the shortest form." % " + ".join(["y"] * k), "%dy" % k,
                   ["%d lots of y is %dy." % (k, k)], "e.g. 4y")

    def t_a2b():
        a2, b2 = random.randint(2, _by(d, 3, 4, 6)), random.randint(2, _by(d, 3, 5, 9))
        return _tb("If a = %d and b = %d, what is a²b?" % (a2, b2), a2 * a2 * b2, "int", {},
                   ["a²b = a × a × b = %d × %d × %d = %d." % (a2, a2, b2, a2 * a2 * b2)])

    def t_equivalent():
        return _q_equiv()

    def t_kab():
        k = random.randint(2, 5)
        return _tb("If a = %d and b = %d, what is %dab?" % (a, b, k), k * a * b, "int", {},
                   ["%dab means %d × a × b = %d × %d × %d = %d." % (k, k, k, a, b, k * a * b)])

    def t_2a2():
        k = random.randint(2, 5)
        return _tb("If a = %d, what is %da²?" % (a, k), k * a * a, "int", {},
                   ["Square first: a² = %d; then × %d = %d." % (a * a, k, k * a * a)])

    return _pick_t(_by(d, [t_ab, t_3y, t_sq, t_frac, t_same],
                       [t_ab, t_3y, t_sq, t_cube, t_frac, t_same, t_a2b, t_equivalent],
                       [t_sq, t_cube, t_frac, t_a2b, t_equivalent, t_kab, t_2a2]))


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
    # whole numbers from 1: substituting a negative number needs directed numbers, which come in strand 7.6
    x = random.randint(_by(d, 1, 2, 3), _by(d, 10, 10, 12))
    y = random.randint(_by(d, 1, 1, 2), _by(d, 8, 9, 9))

    def t_linear():
        m, c = random.randint(2, 9), random.randint(1, 15)
        return _tb("Work out the value of %dx + %d when x = %d." % (m, c, x), m * x + c, "int", {},
                   ["%d × %d + %d = %d." % (m, x, c, m * x + c)])

    def t_two_vars():
        m, n = random.randint(2, 6), random.randint(2, 6)
        return _tb("Work out %da + %db when a = %d and b = %d." % (m, n, x, y), m * x + n * y, "int", {},
                   ["%d × %d + %d × %d = %d." % (m, x, n, y, m * x + n * y)])

    def t_square():
        c = -y if y <= x * x and random.random() < 0.5 else y          # x² − 4 as well as x² + 4, never below 0
        return _tb("Work out x² %s %d when x = %d." % ("+" if c >= 0 else "−", abs(c), x), x * x + c, "int", {},
                   ["x² means x × x, so square first: %d² = %d." % (x, x * x),
                    "Then %s %d: %d." % ("add" if c >= 0 else "take away", abs(c), x * x + c)])

    def t_bracket():
        m, c = random.randint(2, 6), random.randint(1, 9)
        return _tb("Work out %d(x + %d) when x = %d." % (m, c, x), m * (x + c), "int", {},
                   ["%d + %d = %d; × %d = %d." % (x, c, x + c, m, m * (x + c))])

    def t_subtract():
        m = random.randint(2, 9)
        c = m * x + random.randint(0, 20)                 # the answer stays 0 or more
        return _tb("Work out %d − %dx when x = %d." % (c, m, x), c - m * x, "int", {},
                   ["%d − %d × %d = %d." % (c, m, x, c - m * x)])

    def t_table():
        m = random.randint(2, 6)
        c = random.randint(max(-5, 1 - m), 9)             # every y in the table is positive
        rows = [[v, m * v + c] for v in (1, 2, 5, 10)]
        k = random.randrange(4)
        return _io("Complete the table for y = %s." % _expr(m, "x", c).replace("+", " + ").replace("-", " − "), rows,
                   k, rows[k][1], ["%d × %d %s %d = %d." % (m, rows[k][0], "+" if c >= 0 else "−", abs(c), rows[k][1])])

    def t_formula():
        l, w = random.randint(3, 15), random.randint(2, 12)
        return _tb("The perimeter of a rectangle is P = 2l + 2w. Find P when l = %d and w = %d." % (l, w), 2 * l + 2 * w,
                   "int", {"unit": "cm"}, ["2 × %d + 2 × %d = %d." % (l, w, 2 * l + 2 * w)])

    def t_product():
        c = random.randint(1, 20)
        return _tb("Work out ab + %d when a = %d and b = %d." % (c, x, y), x * y + c, "int", {},
                   ["ab means a × b: %d × %d = %d." % (x, y, x * y), "%d + %d = %d." % (x * y, c, x * y + c)])

    def t_divide():
        m = random.randint(2, 5)
        top = m * x
        return _tb("Work out x/%d + %d when x = %d." % (m, y, top), x + y, "int", {},
                   ["%d ÷ %d = %d." % (top, m, x), "%d + %d = %d." % (x, y, x + y)])

    return _pick_t([t_linear, t_two_vars, t_square, t_bracket, t_subtract, t_formula, t_product, t_divide], [t_table])


@skill("Y7.1.d", "Function machines and inverse operations", S1)
def _(d=1):
    d = _d(d)
    m, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 10, 20, 40))
    x = random.randint(1, _by(d, 10, 15, 25))

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

    def t_divide_first():
        q = random.randint(2, 15) + c                # what comes out is never below 0
        return _tb("A function machine does: ÷ %d, then − %d. What comes out when %d goes in?" % (m, c, m * q), q - c, "int",
                   {}, ["%d ÷ %d = %d; − %d = %d." % (m * q, m, q, c, q - c)])

    def t_three_step():
        a, b = random.randint(1, 9), random.randint(2, 5)
        e = random.randint(1, min(9, (x + a) * b))      # never below 0: Year 7 meets directed numbers later
        return _tb("A function machine does: + %d, then × %d, then − %d. What comes out when %d goes in?" % (a, b, e, x),
                   (x + a) * b - e, "int", {}, ["%d + %d = %d; × %d = %d; − %d = %d." % (x, a, x + a, b, (x + a) * b, e, (x + a) * b - e)])

    def t_bracket_expr():
        return _wq("A function machine does: + %d, then × %d. Write the output when x goes in, using brackets (like 3(x+2))."
                   % (c, m), "%d(x+%d)" % (m, c), ["The adding happens first, so it goes in brackets: %d(x + %d)." % (m, c)],
                   "e.g. 3(x+2)")

    def t_square_machine():
        v = random.randint(2, _by(d, 6, 12, 15))
        return _tb("A function machine does: square the number, then + %d. What comes out when %d goes in?" % (c, v), v * v + c,
                   "int", {}, ["%d² = %d; + %d = %d." % (v, v * v, c, v * v + c)])

    def t_find_add():
        a = random.randint(3, _by(d, 20, 40, 90))
        rows = [[v, v + a] for v in random.sample(range(1, 30), 4)]
        return _io("A function machine adds a number. What number does it add?", rows, None, a,
                   ["%d − %d = %d." % (rows[0][1], rows[0][0], a)])

    def t_same():
        same = random.random() < 0.5
        k2 = m * c if same else pick([c, m * c + pick([1, -1])])
        return _wq("Machine A does: × %d, then + %d. Machine B does: + %d, then × %d. Do they always give the same output? "
                   "(yes or no)" % (m, k2, c, m), "yes" if same else "no",
                   ["Machine B gives %d(x + %d) = %dx + %d." % (m, c, m, m * c),
                    "Machine A gives %dx + %d." % (m, k2)], "yes / no")

    def t_input_three():
        a, b, e = random.randint(1, 9), random.randint(2, 5), random.randint(1, 9)
        out = (x + a) * b - e
        return _tb("A function machine does: + %d, then × %d, then − %d. %d comes out. What went in?" % (a, b, e, out), x, "int",
                   {}, ["Work backwards: + %d, then ÷ %d, then − %d." % (e, b, a),
                        "%d + %d = %d; ÷ %d = %d; − %d = %d." % (out, e, out + e, b, x + a, a, x)])

    return _pick_t(_by(d, [t_output, t_input, t_order_matters, t_square_machine],
                       [t_output, t_input, t_order_matters, t_expression, t_divide_first, t_three_step, t_bracket_expr,
                        t_square_machine, t_same],
                       [t_input, t_expression, t_divide_first, t_three_step, t_bracket_expr, t_same, t_input_three]),
                   _by(d, [t_find_rule, t_table, t_find_add], [t_find_rule, t_table, t_find_add], [t_table]))


@skill("Y7.1.e", "Use formulae given in words and symbols", S1)
def _(d=1):
    d = _d(d)

    def t_cost():
        fee, per, h = (random.randint(5, _by(d, 20, 30, 60)), random.randint(3, _by(d, 10, 12, 25)),
                       random.randint(2, _by(d, 5, 8, 12)))
        return _tb("A plumber charges £%d to call plus £%d for each hour. How much for %d hours, in pounds?"
                   % (fee, per, h), fee + per * h, "int", {"unit": "£"}, ["%d + %d × %d = %d." % (fee, per, h, fee + per * h)])

    def t_symbols():
        l, w = random.randint(3, _by(d, 10, 20, 60)), random.randint(2, _by(d, 10, 15, 45))
        return _tb("The formula for the perimeter of a rectangle is P = 2l + 2w. Find P when l = %d and w = %d." % (l, w),
                   2 * l + 2 * w, "int", {}, ["2 × %d + 2 × %d = %d." % (l, w, 2 * l + 2 * w)])

    def t_area():
        b, h = random.randint(2, _by(d, 6, 12, 20)) * 2, random.randint(2, _by(d, 10, 12, 25))
        return _tb("The area of a triangle is A = bh/2. Find A when b = %d and h = %d." % (b, h), b * h // 2, "int", {},
                   ["%d × %d ÷ 2 = %d." % (b, h, b * h // 2)])

    def t_speed():
        s, t = random.randint(3, _by(d, 8, 12, 12)) * 10 + (pick([0, 5]) if d == 2 else 0), random.randint(2, _by(d, 3, 5, 7))
        return _tb("Distance = speed × time. A car travels at %d km/h for %d hours. How far does it go, in km?" % (s, t),
                   s * t, "int", {"unit": "km"}, ["%d × %d = %d." % (s, t, s * t)])

    def t_write():
        per, fee = random.randint(2, 9), random.randint(3, _by(d, 10, 20, 40))
        return _wq("A taxi charges £%d plus £%d per mile. Write a formula for the cost C in pounds for m miles, like "
                   "C=2m+5." % (fee, per), "C=%dm+%d" % (per, fee), ["C = %dm + %d." % (per, fee)], "e.g. C=2m+5")

    def t_reverse():
        fee, per = random.randint(5, _by(d, 10, 20, 60)), random.randint(2, _by(d, 5, 9, 25))
        h = random.randint(2, _by(d, 5, 9, 12))
        return _tb("A hall costs £%d plus £%d per hour. A booking cost £%d. How many hours was it?"
                   % (fee, per, fee + per * h), h, "int", {"unit": "hours"},
                   ["(%d − %d) ÷ %d = %d." % (fee + per * h, fee, per, h)])

    def t_chicken():
        kg = pick([Decimal("1.5"), Decimal("2"), Decimal("2.5"), Decimal("3"), Decimal("1")])
        mins = int(kg * 2 * 20 + 20)
        return _tb("To roast a chicken: allow 20 minutes per 500 g, plus 20 minutes. How many minutes for a %s kg chicken?"
                   % _ds(kg), mins, "int", {"unit": "minutes"},
                   ["%s kg = %d lots of 500 g." % (_ds(kg), int(kg * 2)), "%d × 20 + 20 = %d." % (int(kg * 2), mins)])

    def t_fahrenheit():
        cdeg = pick([0, 5, 10, 15, 20, 25, 30, 35, 40, 100])      # below 0 °C waits for directed numbers (7.6)
        f = cdeg * 9 // 5 + 32
        return _tb("The formula F = 1.8C + 32 changes °C to °F. Find F when C = %d." % cdeg, f, "int", {"unit": "°F"},
                   ["1.8 × %d + 32 = %d." % (cdeg, f)])

    def t_miles():
        mi = random.randint(2, 25) * 5
        return _tb("To change miles to kilometres: multiply by 8, then divide by 5. How many km is %d miles?" % mi, mi * 8 // 5,
                   "int", {"unit": "km"}, ["%d × 8 = %d; ÷ 5 = %d." % (mi, mi * 8, mi * 8 // 5)])

    def t_width():
        w, l = random.randint(2, _by(d, 9, 12, 25)), random.randint(3, _by(d, 10, 15, 30))
        return _tb("The area of a rectangle is A = lw. A = %d cm² and l = %d cm. Find w, in cm." % (l * w, l), w, "int",
                   {"unit": "cm"}, ["w = A ÷ l = %d ÷ %d = %d." % (l * w, l, w)])

    def t_table():
        per, fee = random.randint(3, 9), random.randint(5, 25)
        ns = [1, 2, 5, 10]
        rows = [[n, per * n + fee] for n in ns]
        k = random.randrange(4)
        return _io("A club charges C = %dn + %d pounds for n sessions. What goes in the empty cell?" % (per, fee), rows, k,
                   rows[k][1], ["%d × %d + %d = %d." % (per, rows[k][0], fee, rows[k][1])], rule="C = %dn + %d" % (per, fee))

    def t_mean_formula():
        a, b, c = [random.randint(10, _by(d, 30, 40, 99)) for _ in range(3)]
        s = a + b + c
        while s % 3:
            c += 1
            s = a + b + c
        return _tb("The formula m = (a + b + c)/3 gives the mean of three numbers. Find m when a = %d, b = %d and c = %d."
                   % (a, b, c), s // 3, "int", {}, ["(%d + %d + %d) ÷ 3 = %d ÷ 3 = %d." % (a, b, c, s, s // 3)])

    return _pick_t(_by(d, [t_cost, t_symbols, t_area, t_speed, t_miles],
                       [t_cost, t_symbols, t_area, t_speed, t_write, t_reverse, t_chicken, t_fahrenheit, t_miles, t_width,
                        t_mean_formula],
                       [t_cost, t_symbols, t_area, t_write, t_reverse, t_chicken, t_fahrenheit, t_width, t_mean_formula]),
                   [t_table])


@skill("Y7.1.f", "Vocabulary: expressions, equations, formulae, terms", S1)
def _(d=1):
    d = _d(d)

    def t_classify():
        item, ans = pick(_by(d, [("3x + 5", "expression"), ("3x + 5 = 20", "equation"), ("A = lw", "formula"),
                                 ("x − 4 = 9", "equation"), ("2a − b", "expression"), ("x > 7", "inequality")],
                             [("3x + 5", "expression"), ("3x + 5 = 20", "equation"), ("A = lw", "formula"),
                              ("2a − b", "expression"), ("P = 2l + 2w", "formula"), ("x − 4 = 9", "equation"),
                              ("x > 7", "inequality")],
                             [("4(x − 1)", "expression"), ("5 = 2y + 1", "equation"), ("v = u + at", "formula"),
                              ("3y ≤ 12", "inequality"), ("C = πd", "formula"), ("7 − 2x > 1", "inequality"),
                              ("a² + 2ab", "expression"), ("2(x + 3) = 14", "equation")]))
        return _wq("Is  %s  an expression, an equation, a formula or an inequality?" % item, ans,
                   ["An expression has no equals sign; an equation can be solved; a formula links quantities; an "
                    "inequality uses < or >."], "expression / equation / formula / inequality")

    def t_terms():
        k = random.randint(2, _by(d, 3, 5, 6))
        terms = random.sample(["3x", "5", "y²", "2ab", "7y", "z", "4xy"], k)
        if d == 2:                                  # stretch: some terms are subtracted, which does not change the count
            shown = terms[0] + "".join(" %s %s" % (pick(["+", "−"]), t) for t in terms[1:])
        else:
            shown = " + ".join(terms)
        return _tb("How many terms are in the expression  %s ?" % shown, k, "int", {},
                   ["The terms are %s." % ", ".join(terms)])

    def t_coef():
        m = random.randint(2, 12)
        v = pick(["x", "y", "p"])
        c = random.randint(1, 9)
        if d == 2 and random.random() < 0.5:        # stretch: a bare letter, so the coefficient is 1
            return _tb("What is the coefficient of %s in  %d + %s ?" % (v, c, v), 1, "int", {},
                       ["%s means 1 × %s, so the coefficient is 1." % (v, v)])
        if d == 2:                                  # stretch: the letter term comes second
            return _tb("What is the coefficient of %s in  %d + %d%s ?" % (v, c, m, v), m, "int", {},
                       ["The coefficient is the number multiplying %s: %d." % (v, m)])
        return _tb("What is the coefficient of %s in  %d%s + %d ?" % (v, m, v, c), m, "int", {},
                   ["The coefficient is the number multiplying %s: %d." % (v, m)])

    def t_constant():
        m, c = random.randint(2, 9), random.randint(1, 20)
        if d == 2:                                  # stretch: three terms, constant in the middle
            n = random.randint(2, 9)
            return _tb("What is the constant term in  %dx + %d + %dy ?" % (m, c, n), c, "int", {},
                       ["The term with no letter: %d." % c])
        return _tb("What is the constant term in  %dx + %d ?" % (m, c), c, "int", {}, ["The term with no letter: %d." % c])

    def t_like():
        # each group lists the spellings of one letter part; a "yes" takes both terms from one group (about half the time)
        groups = _by(d, [["x"], ["y"], [""]], [["x"], ["y"], ["x²"], ["xy"], [""]],
                     [["x"], ["x²"], ["xy", "yx"], ["x²y", "yx²"], ["xy²", "y²x"]])
        g = pick(groups)
        if random.random() < 0.45:                  # like terms; at hard mostly the reordered letters (xy and yx)
            if d == 2 and random.random() < 0.7:
                g = pick([gg for gg in groups if len(gg) > 1])
            pa, pb = random.sample(g, 2) if len(g) > 1 else (g[0], g[0])
        else:
            pa, pb = g[0], pick(pick([gg for gg in groups if gg is not g]))
        ca, cb = random.sample(range(2, 10), 2)
        a = "%s%s" % ("" if pa and random.random() < 0.2 else ca, pa)     # sometimes a bare letter part: x, yx
        b = "%d%s" % (cb, pb)
        if random.random() < 0.5:
            a, b = b, a

        def _letters(t):                            # "x²y" -> {"x": 2, "y": 1}, so xy and yx compare equal
            out, last = {}, None
            for ch in t.lstrip("0123456789"):
                if ch == "²":
                    out[last] += 1
                else:
                    out[ch], last = out.get(ch, 0) + 1, ch
            return sorted(out.items())
        like = _letters(a) == _letters(b)
        return _wq("Are %s and %s like terms? (yes or no)" % (a, b), "yes" if like else "no",
                   ["Like terms have exactly the same letters and powers."], "yes / no")

    return _pick_t([t_classify, t_terms, t_coef, t_constant, t_like])
