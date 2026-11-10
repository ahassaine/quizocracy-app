# dev/app/logic/y4_gen_a.py — Year 4 generators: strands 4.0 and 4.1
#
# Number & place value (to 10,000, Roman numerals, negative numbers) and
# comparing / ordering / rounding / estimating / patterns.
#
# Every generator takes a difficulty `d`: 0 = easy, 1 = core, 2 = stretch.
# Each skill offers 8+ genuinely different framings (bare calculation, word
# problem, missing number, inverse, visual model, comparison, reasoning) and
# leans on `number_line`, `base_ten`, `io_table`, `data_table` and `line_graph`
# wherever the concept is about representing, ordering or rounding numbers.
import random
from .maths_engine import skill, n_words, ordinal, pick, NAMES

S0 = "4.0 Number & place value"
S1 = "4.1 Compare, order, round, estimate, patterns"


# ------------------------------------------------------------------ utils ----
def _d(d):
    """Clamp difficulty to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _c(n):
    """UK thousands separator for display: 3482 -> '3,482'."""
    return "{:,}".format(int(n))


def _lst(xs):
    return ", ".join(_c(x) if isinstance(x, int) else str(x) for x in xs)


def _w4(n):
    """Words for 0-10,000, UK style: 3482 -> 'three thousand four hundred and eighty-two'."""
    n = int(n)
    if n == 10000:
        return "ten thousand"
    if n < 1000:
        return n_words(n)
    th, r = n // 1000, n % 1000
    s = n_words(th) + " thousand"
    if r == 0:
        return s
    if r < 100:
        return s + " and " + n_words(r)
    return s + " " + n_words(r)


_RVAL = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
         (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _rom(n):
    """Roman numeral for 1-100 (subtractive form)."""
    n = int(n)
    out = ""
    for v, s in _RVAL:
        while n >= v:
            out += s
            n -= v
    return out


def _thousands(d):
    """A 4-digit number of the right size for this difficulty."""
    if d == 0:
        return random.randint(1, 9) * 1000 + random.randint(1, 9) * 100 + \
               random.randint(1, 9) * 10 + random.randint(1, 9)
    if d == 1:
        return random.randint(1001, 9999)
    if random.random() < 0.5:                # zeros trip pupils up
        th = random.randint(1, 9)
        h = pick([0, 0, 9])
        t = pick([0, 9, random.randint(0, 9)])
        o = pick([0, 9, random.randint(0, 9)])
        return th * 1000 + h * 100 + t * 10 + o
    return random.randint(1001, 9999)


def _num_for(d):
    """A number of the right size: 3-digit at d=0, 4-digit above."""
    if d == 0:                               # no zero digits: "800 = ___ + 0 + 0" teaches nothing
        return random.randint(1, 9) * 100 + random.randint(1, 9) * 10 + random.randint(1, 9)
    return _thousands(d)


def _distinct4(d):
    """A number whose digits are all different (so a digit names one place)."""
    if d == 0:
        a, b, c = random.sample(range(1, 10), 3)
        return a * 100 + b * 10 + c
    a, b, c, e = random.sample(range(1, 10), 4)
    return a * 1000 + b * 100 + c * 10 + e


def _places(d):
    if d == 0:
        return [(100, "hundreds"), (10, "tens"), (1, "ones")]
    return [(1000, "thousands"), (100, "hundreds"), (10, "tens"), (1, "ones")]


def _pl(k, word):
    """'1 ten' / '3 tens'."""
    k = int(k)
    return "%d %s" % (k, word if k == 1 else word + "s")


def _thto(n):
    """'3 thousands, 4 hundreds, 8 tens and 2 ones'."""
    n = int(n)
    th, h, t, o = n // 1000, (n // 100) % 10, (n // 10) % 10, n % 10
    parts = ([_pl(th, "thousand")] if th else []) + \
            [_pl(h, "hundred"), _pl(t, "ten")]
    return ", ".join(parts) + " and " + _pl(o, "one")


def _r(n, unit):
    """Round n to the nearest `unit`, halves up (n >= 0)."""
    n, unit = int(n), int(unit)
    return ((n + unit // 2) // unit) * unit


def _r10(n):
    return _r(n, 10)


def _r100(n):
    return _r(n, 100)


def _r1000(n):
    return _r(n, 1000)


# --- question builders -------------------------------------------------------
def _tb(prompt, ans, atype="int", spec=None, solution=None):
    """A typed-answer question (the plain `number` component)."""
    return {"prompt": prompt, "component": "number", "spec": spec or {},
            "answer": ans, "answer_type": atype, "solution": solution or []}


def _wq(prompt, ans, solution, placeholder="type your answer"):
    """A typed *word* answer."""
    return _tb(prompt, ans, "str", {"text": True, "placeholder": placeholder}, solution)


def _bt(prompt, ans, solution):
    """A build-it-with-place-value-blocks question (answer must be 0-999)."""
    ans = int(ans)
    return {"prompt": prompt, "component": "base_ten", "spec": {"mode": "build", "max": 9},
            "answer": ans, "answer_type": "int", "solution": solution}


def _nl(prompt, ans, step, major, solution, lo=None, hi=None):
    """Place-the-marker-on-a-number-line. `ans` and `major` are multiples of `step`."""
    ans = int(ans)
    if lo is None:
        lo = (ans // major) * major - 2 * major
        if lo < 0 and ans >= 0:
            lo = 0
    if hi is None:
        hi = lo + 5 * major
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": lo, "max": hi, "step": step, "major": major},
            "answer": ans, "answer_type": "num", "tolerance": step / 2.0,
            "solution": solution}


def _io(prompt, rows, missing, answer, solution, rule=None, atype="int"):
    """input/output table; `missing` = index of the row whose Out cell is blank."""
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _dt(prompt, headers, rows, answer, solution, missing=None, atype="int"):
    """A bordered data table; `missing` = [row, col] rendered as a blank box."""
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _lg(prompt, points, answer, solution, ylabel="°C", xlabel="Time",
        missing=None, atype="int"):
    spec = {"points": [[str(a), b] for a, b in points], "yLabel": ylabel, "xLabel": xlabel}
    if missing is not None:
        spec["missing"] = int(missing)
    return {"prompt": prompt, "component": "line_graph", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _rank(k, word):
    """'coldest' for 1st, '3rd coldest' otherwise."""
    return word if int(k) == 1 else "%s %s" % (ordinal(k), word)


def _pick_t(plain, visual):
    """Choose a framing; visual framings are twice as likely as typed ones."""
    return random.choice(list(plain) + list(visual) + list(visual))()


# ================================================================== 4.0 ======
@skill("Y4.0.a", "Count in multiples of 6, 7, 9, 25 and 1000", S0)
def _(d=1):
    d = _d(d)
    step = pick([6, 25, 1000] if d == 0 else [6, 7, 9, 25, 1000])
    kmax = {0: 6, 1: 9, 2: 12}[d]
    if step == 1000:                      # keep every term within 10,000
        start = random.randint(1, 5) * step
        offset = 0 if d == 0 else pick([0, 0, 100 * random.randint(1, 9)])
    else:
        start = random.randint(2, kmax) * step
        # counting on from *any* number, not just a multiple
        offset = 0 if d == 0 else pick([0, 0, random.randint(1, step - 1)])
    base = start + offset

    def t_next():
        back = d >= 1 and random.random() < 0.4 and base - 3 * step >= 0
        sg = -step if back else step
        ans = base + sg
        return _tb("Count %s in %ss from %s. What number comes next?"
                   % ("back" if back else "on", _c(step), _c(base)), ans, "int", {},
                   ["%s each time: %s %s %s = %s."
                    % ("Subtract %s" % _c(step) if back else "Add %s" % _c(step),
                       _c(base), "−" if back else "+", _c(step), _c(ans))])

    def t_three():
        ans = base + 3 * step
        return _tb("Start at %s and count on in %ss. What number do you land on after 3 jumps?"
                   % (_c(base), _c(step)), ans, "int", {},
                   ["3 × %s = %s." % (_c(step), _c(3 * step)),
                    "%s + %s = %s." % (_c(base), _c(3 * step), _c(ans))])

    def t_missing():
        terms = [base + i * step for i in range(5)]
        idx = random.randint(1, 3)
        shown = ", ".join("___" if i == idx else _c(t) for i, t in enumerate(terms))
        return _tb("These numbers are counting on in %ss. Find the missing one:  %s"
                   % (_c(step), shown), terms[idx], "int", {},
                   ["%s + %s = %s." % (_c(terms[idx - 1]), _c(step), _c(terms[idx]))])

    def t_back_zero():
        k = random.randint(4, 7)
        first = k * step
        terms = [first - i * step for i in range(4)]
        ans = terms[-1] - step
        return _tb("Count back in %ss:  %s, ___  What number comes next?"
                   % (_c(step), _lst(terms)), ans, "int", {},
                   ["Subtract %s each time." % _c(step),
                    "%s − %s = %s." % (_c(terms[-1]), _c(step), _c(ans))])

    def t_word():
        k = random.randint(3, 6 if d == 0 else 9)
        if step == 1000:
            who = pick(NAMES)
            return _tb("%s saves £%s every year. How much has %s saved after %d years?"
                       % (who, _c(step), who, k), k * step, "int", {"unit": "£"},
                       ["Count on in %ss, %d times." % (_c(step), k),
                        "%d × %s = %s." % (k, _c(step), _c(k * step))])
        holder, thing = pick([("crates", "eggs"), ("boxes", "pencils"),
                              ("bags", "marbles"), ("trays", "buns")])
        who = pick(NAMES)
        return _tb("%s has %d %s. Each one holds %d %s. How many %s altogether?"
                   % (who, k, holder, step, thing, thing), k * step, "int", {"unit": thing},
                   ["'Each' one holds %d — the same number %d times, so multiply. 'Altogether' means all of "
                    "them together." % (step, k),
                    "Count on in %ds, %d times." % (step, k),
                    "%d × %d = %s." % (k, step, _c(k * step))])

    def t_inverse():
        k = random.randint(4, 9)
        return _tb("%s counts on in %ss from 0: %s, %s, %s, ... How many counts does it take "
                   "to reach %s?" % (pick(NAMES), _c(step), _c(step), _c(2 * step),
                                     _c(3 * step), _c(k * step)),
                   k, "int", {"unit": "counts"},
                   ["%s ÷ %s = %d." % (_c(k * step), _c(step), k)])

    def t_will_say():
        who = pick(NAMES)
        k = random.randint(3, 9)
        hit = random.random() < 0.5
        if step == 1000:
            target = k * step if hit else k * step + 100 * random.randint(1, 9)
        else:
            target = k * step if hit else k * step + random.randint(1, step - 1)
        ans = "yes" if target % step == 0 else "no"
        return _wq("%s counts in %ss starting at 0. Will %s say the number %s? "
                   "(type 'yes' or 'no')" % (who, _c(step), who, _c(target)),
                   ans,
                   ["%s ÷ %s %s exactly." % (_c(target), _c(step),
                                             "divides" if ans == "yes" else "does not divide"),
                    "So the answer is %s." % ans], "yes / no")

    def t_line():
        st = step if step <= 25 else 1000
        k = random.randint(2, 4)
        s = random.randint(1, 5) * st
        ans = s + k * st
        major = {6: 30, 7: 35, 9: 45, 25: 100, 1000: 5000}[st]
        lo, hi = (0, 10000) if st == 1000 else (None, None)
        return _nl("Start at %s and count on %d lots of %s. Place the number you land on."
                   % (_c(s), k, _c(st)), ans, st, major,
                   ["%d × %s = %s." % (k, _c(st), _c(k * st)),
                    "%s + %s = %s." % (_c(s), _c(k * st), _c(ans))], lo=lo, hi=hi)

    def t_blocks():
        st = step if step <= 25 else 100
        k = random.randint(2, 4)
        s = random.randint(1, max(1, (900 - k * st) // st)) * st
        ans = s + k * st
        return _bt("Count on %d lots of %d from %d, then build the number you land on."
                   % (k, st, s), ans,
                   ["%d × %d = %d." % (k, st, k * st),
                    "%d + %d = %d." % (s, k * st, ans)])

    def t_table():
        rows = [[i, base + i * step] for i in range(1, 5)]
        miss = random.randint(1, 3)
        return _io("Each row counts on one more lot of %s from %s. "
                   "What number goes in the empty cell?" % (_c(step), _c(base)),
                   rows, miss, rows[miss][1],
                   ["Each Out is %s more than the one above." % _c(step),
                    "%s + %s = %s." % (_c(rows[miss - 1][1]), _c(step), _c(rows[miss][1]))],
                   rule="× %s, then + %s" % (_c(step), _c(base)))

    return _pick_t([t_next, t_three, t_missing, t_back_zero, t_word, t_inverse, t_will_say],
                   [t_line, t_blocks, t_table])


@skill("Y4.0.b", "Read and write numbers to 10,000", S0)
def _(d=1):
    d = _d(d)
    n = _num_for(d)

    def t_words_to_num():
        return _tb("Write '%s' as a numeral." % _w4(n), n, "int", {},
                   ["'%s' is %s." % (_w4(n), _c(n))])

    def t_num_to_words():
        return _wq("Write the number %s in words." % _c(n), _w4(n),
                   ["%s is '%s'." % (_c(n), _w4(n))], "type in words")

    def t_cheque():
        who = pick(NAMES)
        return _wq("%s is filling in a cheque for £%s. Write that amount in words."
                   % (who, _c(n)), _w4(n),
                   ["%s in words is '%s'." % (_c(n), _w4(n))], "type in words")

    def t_from_parts():
        return _tb("Write the number that has %s." % _thto(n), n, "int", {},
                   ["%s makes %s." % (_thto(n).capitalize(), _c(n))])

    def t_zeros():
        th = random.randint(1, 9)
        h, t = pick([(0, 0), (0, random.randint(1, 9)), (random.randint(1, 9), 0)])
        m = th * 1000 + h * 100 + t * 10 + random.randint(0, 9)
        return _tb("Read this number carefully and write it as a numeral:  '%s'" % _w4(m),
                   m, "int", {},
                   ["A missing place value is written as a zero.",
                    "'%s' is %s." % (_w4(m), _c(m))])

    def t_compare_words():
        m = _num_for(d)
        while m == n:
            m = _num_for(d)
        big = max(n, m)
        return _tb("Which is the greater number, '%s' or '%s'? Write it in numerals."
                   % (_w4(n), _w4(m)), big, "int", {},
                   ["'%s' is %s and '%s' is %s." % (_w4(n), _c(n), _w4(m), _c(m)),
                    "%s is greater." % _c(big)])

    def t_population():
        who = pick(["Ashby", "Redhill", "Newport", "Stanton", "Hartley"])
        return _wq("The village of %s has a population of %s. Write that number in words."
                   % (who, _c(n)), _w4(n),
                   ["%s is '%s'." % (_c(n), _w4(n))], "type in words")

    def t_shifted_words():
        amt = pick([10, 100, 1000])
        base = n if n + amt <= 9999 else n - amt
        ans = base + amt
        return _wq("What is %s more than %s? Write your answer in words."
                   % (_c(amt), _c(base)), _w4(ans),
                   ["%s + %s = %s." % (_c(base), _c(amt), _c(ans)),
                    "%s is '%s'." % (_c(ans), _w4(ans))], "type in words")

    def t_table():
        ns = random.sample(range(1000, 9999), 4) if d >= 1 else random.sample(range(101, 999), 4)
        rows = [[_w4(x), _c(x)] for x in ns]
        r = random.randint(0, 3)
        return _dt("This table shows numbers in words and in numerals. "
                   "What numeral belongs in the empty cell?",
                   ["In words", "In numerals"], rows, ns[r],
                   ["'%s' is %s." % (_w4(ns[r]), _c(ns[r]))], missing=[r, 1])

    def t_table_words():
        ns = random.sample(range(1000, 9999), 4) if d >= 1 else random.sample(range(101, 999), 4)
        rows = [[_c(x), _w4(x)] for x in ns]
        r = random.randint(0, 3)
        return _dt("What goes in the empty cell? Write the number in words.",
                   ["In numerals", "In words"], rows, _w4(ns[r]),
                   ["%s is '%s'." % (_c(ns[r]), _w4(ns[r]))], missing=[r, 1], atype="str")

    def t_blocks():
        m = random.randint(101, 999)
        return _bt("Build the number '%s' using the place-value blocks." % _w4(m), m,
                   ["'%s' is %d." % (_w4(m), m), "%d = %s." % (m, _thto(m))])

    return _pick_t([t_words_to_num, t_num_to_words, t_cheque, t_from_parts, t_zeros,
                    t_compare_words, t_population, t_shifted_words],
                   [t_table, t_table_words, t_blocks])


@skill("Y4.0.c", "Represent numbers to 10,000", S0)
def _(d=1):
    d = _d(d)

    def t_place_100():
        step, major = 100, 500
        ans = random.randint(1, 19) * 500 + random.randint(0, 4) * 100
        if d == 0:
            ans = random.randint(1, 9) * 100
        elif d == 2:                         # finer ticks: every 50, labelled every 250
            step, major = 50, 250
            ans = random.randint(2, 98) * 100 + 50
        return _nl("Place %s on the number line." % _c(ans), ans, step, major,
                   ["%s lies between %s and %s."
                    % (_c(ans), _c((ans // major) * major), _c((ans // major) * major + major))])

    def t_place_words():
        step, major = {0: (1000, 1000), 1: (500, 1000), 2: (100, 500)}[d]
        ans = {0: random.randint(1, 9) * 1000, 1: random.randint(2, 19) * 500,
               2: random.randint(11, 99) * 100}[d]
        return _nl("Place '%s' on the number line." % _w4(ans), ans, step, major,
                   ["'%s' is %s." % (_w4(ans), _c(ans))])

    def t_halfway():
        gap = {0: 2000, 1: 1000, 2: pick([200, 400, 600, 800])}[d]
        a = random.randint(1, 7) * 1000 + (random.randint(0, 9 - gap // 100) * 100 if d == 2 else 0)
        b = a + gap
        ans = a + gap // 2
        step, major = (500, 1000) if d == 0 else (100, 500)
        return _nl("Place the number that is halfway between %s and %s on the number line."
                   % (_c(a), _c(b)), ans, step, major,
                   ["Half of %s is %s." % (_c(gap), _c(gap // 2)),
                    "%s + %s = %s." % (_c(a), _c(gap // 2), _c(ans))])

    def t_place_1000():
        if d == 2:                           # a half-thousand between the labelled marks
            ans = random.randint(1, 8) * 1000 + 500
            return _nl("Place %s on the number line." % _c(ans), ans, 500, 1000,
                       ["%s is halfway between %s and %s."
                        % (_c(ans), _c(ans - 500), _c(ans + 500))], lo=0, hi=10000)
        ans = random.randint(1, 5 if d == 0 else 9) * 1000
        return _nl("Place %s on the number line." % _c(ans), ans, 1000, 5000,
                   ["%s is %s of 1,000." % (_c(ans), _pl(ans // 1000, "lot"))])

    def t_mark():
        k = random.randint(2, 5) if d == 0 else random.randint(2, 9)
        gap = {0: 1000, 1: pick([500, 1000]), 2: pick([200, 250, 500])}[d]
        ans = k * gap
        return _tb("A number line runs from 0 to %s with a mark every %s. "
                   "What number is at the %s mark after 0?" % (_c(10 * gap), _c(gap), ordinal(k)),
                   ans, "int", {},
                   ["%d × %s = %s." % (k, _c(gap), _c(ans))])

    def t_how_many_hundreds():
        if d == 2:                           # tens in a 4-digit multiple of 10
            m = random.randint(101, 999) * 10
            return _tb("How many tens are there in %s?" % _c(m), m // 10, "int",
                       {"unit": "tens"},
                       ["%s ÷ 10 = %d." % (_c(m), m // 10)])
        m = random.randint(11, 30 if d == 0 else 99) * 100
        return _tb("How many hundreds are there in %s?" % _c(m), m // 100, "int",
                   {"unit": "hundreds"},
                   ["%s ÷ 100 = %d." % (_c(m), m // 100)])

    def t_how_many_thousands():
        m = random.randint(1, 5 if d == 0 else 9) * 1000
        if d == 2:
            m += random.randint(1, 9) * 100
        return _tb("How many hundreds make %s?" % _c(m), m // 100, "int", {"unit": "hundreds"},
                   ["Ten hundreds make 1,000.",
                    "%s ÷ 100 = %d." % (_c(m), m // 100)])

    def t_blocks_words():
        if d == 0:
            m = random.randint(1, 5) * 100 + random.randint(1, 9) * 10 + random.randint(1, 9)
        elif d == 2:                         # a zero digit to notice
            m = random.randint(1, 9) * 100 + pick([0, random.randint(1, 9) * 10])
            m += random.randint(1, 9) if m % 100 == 0 else 0
        else:
            m = random.randint(101, 999)
        return _bt("Build the number '%s' with the place-value blocks." % _w4(m), m,
                   ["'%s' is %d." % (_w4(m), m)])

    def t_blocks_part():
        n = _thousands(d)
        while n % 1000 == 0:
            n = _thousands(d)
        part = n % 1000
        return _bt("Here is the number %s. Build the part that is left when the thousands "
                   "are taken away." % _c(n), part,
                   ["%s − %s = %d." % (_c(n), _c((n // 1000) * 1000), part),
                    "%d = %s." % (part, _thto(part))])

    def t_blocks_regroup():
        h = random.randint(1, 3 if d == 0 else 6)
        t = random.randint(10, {0: 12, 1: 15, 2: 19}[d])
        o = random.randint(10, 15) if d == 2 else random.randint(0, 9)   # d=2: regroup twice
        val = h * 100 + t * 10 + o
        who = pick(NAMES)
        sol = ["%d tens is %d, so ten of them swap for another hundred." % (t, t * 10)]
        if o >= 10:
            sol.append("%d ones is %d, so ten of them swap for another ten." % (o, o))
        return _bt("%s has %s, %s and %s. Build that number with the blocks."
                   % (who, _pl(h, "hundred"), _pl(t, "ten"), _pl(o, "one")), val,
                   sol + ["%d + %d + %d = %d." % (h * 100, t * 10, o, val)])

    def t_blocks_1000_less():
        n = _thousands(d)
        ans = n - (n // 1000) * 1000
        if ans == 0:
            ans = random.randint(101, 999)
            n = (random.randint(1, 9)) * 1000 + ans
        return _bt("Build the number that is %s less than %s."
                   % (_c((n // 1000) * 1000), _c(n)), ans,
                   ["%s − %s = %d." % (_c(n), _c((n // 1000) * 1000), ans)])

    return _pick_t([t_mark, t_how_many_hundreds, t_how_many_thousands],
                   [t_place_100, t_place_words, t_halfway, t_place_1000,
                    t_blocks_words, t_blocks_part, t_blocks_regroup, t_blocks_1000_less])


@skill("Y4.0.d", "Place value in 4-digit numbers", S0)
def _(d=1):
    d = _d(d)

    def t_which_digit():
        n = _num_for(d)
        pos, place = pick(_places(d))
        return _tb("In the number %s, which digit is in the %s place?" % (_c(n), place),
                   (n // pos) % 10, "int", {},
                   ["%s = %s." % (_c(n), _thto(n)),
                    "The %s digit is %d." % (place, (n // pos) % 10)])

    def t_from_words():
        n = _num_for(d)
        pos, place = pick(_places(d))
        return _tb("In the number '%s', which digit is in the %s place?" % (_w4(n), place),
                   (n // pos) % 10, "int", {},
                   ["'%s' is %s." % (_w4(n), _c(n)),
                    "The %s digit is %d." % (place, (n // pos) % 10)])

    def t_value():
        n = _distinct4(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        return _tb("In the number %s, what is the VALUE of the digit in the %s place?"
                   % (_c(n), place), dig * pos, "int", {},
                   ["The %s digit is %d." % (place, dig),
                    "Its value is %d × %s = %s." % (dig, _c(pos), _c(dig * pos))])

    def t_named_value():
        n = _distinct4(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        return _tb("What is the value of the digit %d in the number %s?" % (dig, _c(n)),
                   dig * pos, "int", {},
                   ["The %d is in the %s place." % (dig, place),
                    "It is worth %s." % _c(dig * pos)])

    def t_which_place():
        n = _distinct4(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        opts = "thousands, hundreds, tens or ones" if d >= 1 else "hundreds, tens or ones"
        return _wq("In the number %s, which place is the digit %d in? (%s)" % (_c(n), dig, opts),
                   place, ["%s = %s." % (_c(n), _thto(n)),
                           "The %d is in the %s place." % (dig, place)],
                   "thousands / hundreds / tens / ones")

    def t_odd_one_out():
        pos, place = pick(_places(d))
        dig = random.randint(1, 9)

        def make(has):
            for _ in range(200):
                m = _num_for(d)
                if (((m // pos) % 10) == dig) == has:
                    return m
            return dig * pos + (1000 if d >= 1 else 100)
        target = make(True)
        opts = [target]
        while len(opts) < 4:
            m = make(False)
            if m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers has %s %d in the %s place?   %s"
                   % ("an" if dig == 8 else "a", dig, place, _lst(opts)), target, "int", {},
                   ["Check the %s digit of each number." % place,
                    "%s has %d in the %s place." % (_c(target), dig, place)])

    def t_worth_more():
        pos1, pl1 = pick(_places(d)[:-1])
        rest = [p for p in _places(d) if p[0] < pos1]
        pos2, pl2 = pick(rest)
        dig = random.randint(2, 9)
        others = [x for x in range(1, 10) if x != dig]
        a = sum(p * (dig if p == pos1 else pick(others)) for p, _pl in _places(d))
        b = sum(p * (dig if p == pos2 else pick(others)) for p, _pl in _places(d))
        va, vb = dig * pos1, dig * pos2
        return _tb("The digit %d appears in %s and in %s. How much MORE is it worth in %s?"
                   % (dig, _c(a), _c(b), _c(a)), va - vb, "int", {},
                   ["In %s the %d is worth %s; in %s the %d is worth %s."
                    % (_c(a), dig, _c(va), _c(b), dig, _c(vb)),
                    "%s − %s = %s." % (_c(va), _c(vb), _c(va - vb))])

    def t_guess():
        n = _distinct4(d)
        parts = [(place, (n // pos) % 10) for pos, place in _places(d)]
        random.shuffle(parts)
        desc = ", ".join("%d in the %s place" % (dig, place) for place, dig in parts)
        return _tb("Guess the number: it has %s. What is the number?" % desc, n, "int", {},
                   ["Put each digit in its place.", "The number is %s." % _c(n)])

    def t_chart():
        n = _distinct4(max(d, 1))
        digits = [str(n // 1000), str((n // 100) % 10), str((n // 10) % 10), str(n % 10)]
        col = random.randint(0, 3)
        place = ["thousands", "hundreds", "tens", "ones"][col]
        # the number is given in words, so the digit is read from them, not copied from the same number in figures
        return _dt("This place-value chart shows the number %s. "
                   "Which digit belongs in the empty %s cell?" % (_w4(n), place),
                   ["Thousands", "Hundreds", "Tens", "Ones"], [digits], int(digits[col]),
                   ["%s = %s." % (_c(n), _thto(n)),
                    "The %s digit is %s." % (place, digits[col])], missing=[0, col])

    def t_chart_value():
        n = _distinct4(max(d, 1))
        digits = [str(n // 1000), str((n // 100) % 10), str((n // 10) % 10), str(n % 10)]
        col = random.randint(0, 3)
        pos = [1000, 100, 10, 1][col]
        place = ["thousands", "hundreds", "tens", "ones"][col]
        dig = int(digits[col])
        return _dt("The place-value chart shows %s. What is the VALUE of the digit in the "
                   "%s column?" % (_c(n), place),
                   ["Thousands", "Hundreds", "Tens", "Ones"], [digits], dig * pos,
                   ["The %s digit is %d." % (place, dig),
                    "%d × %s = %s." % (dig, _c(pos), _c(dig * pos))])

    def t_build_value():
        n = _distinct4(d)
        cand = [(p, pl) for p, pl in _places(d) if p <= 100]
        pos, place = pick(cand)
        dig = (n // pos) % 10
        return _bt("Build the VALUE of the digit %d in the number %s." % (dig, _c(n)),
                   dig * pos,
                   ["The %d is in the %s place, so it is worth %d." % (dig, place, dig * pos)])

    return _pick_t([t_which_digit, t_from_words, t_value, t_named_value, t_which_place,
                    t_odd_one_out, t_worth_more, t_guess],
                   [t_chart, t_chart_value, t_build_value])


@skill("Y4.0.e", "Partition and expanded form (4-digit)", S0)
def _(d=1):
    d = _d(d)
    n = _num_for(d)
    th, h, t, o = n // 1000, (n // 100) % 10, (n // 10) % 10, n % 10
    parts = [th * 1000, h * 100, t * 10, o]
    keys = [0, 1, 2, 3] if d >= 1 else [1, 2, 3]

    def t_missing_part():
        idx = pick([k for k in keys if parts[k]] or keys)
        shown = " + ".join("___" if k == idx else _c(parts[k]) for k in keys)
        return _tb("Complete the partition:  %s = %s" % (_c(n), shown), parts[idx], "int", {},
                   ["%s = %s." % (_c(n), " + ".join(_c(parts[k]) for k in keys))])

    def t_recombine():
        expr = " + ".join(_c(parts[k]) for k in keys if parts[k]) or "0"
        if "+" not in expr:
            return t_missing_part()
        return _tb("Which number is this?   %s" % expr, n, "int", {},
                   ["%s = %s." % (expr, _c(n))])

    def t_expanded():
        expr = " + ".join(_c(parts[k]) for k in keys if parts[k]) or "0"
        if "+" not in expr:
            return t_missing_part()
        return _tb("Convert from expanded form to a single number:  %s = ___" % expr,
                   n, "int", {},
                   ["Add the parts together.", "%s = %s." % (expr, _c(n))])

    def t_two_part():
        first = th * 1000 if d >= 1 and th else h * 100
        if n - first == 0:
            return t_missing_part()
        return _tb("Complete:  %s = %s + ___" % (_c(n), _c(first)), n - first, "int", {},
                   ["%s − %s = %s." % (_c(n), _c(first), _c(n - first))])

    def t_flexible_th():
        if d == 0 or th == 0:
            return t_missing_part()
        ans = 1000 + h * 100
        return _tb("Complete this partition:  %s = %s + ___ + %d + %d"
                   % (_c(n), _c((th - 1) * 1000), t * 10, o), ans, "int", {},
                   ["One thousand has been exchanged for ten hundreds.",
                    "%s + %s + %d + %d = %s."
                    % (_c((th - 1) * 1000), _c(ans), t * 10, o, _c(n))])

    def t_flexible_h():
        if h == 0:
            return t_missing_part()
        ans = 100 + t * 10
        pre = [_c(th * 1000)] if d >= 1 else []
        pre.append(_c((h - 1) * 100))
        return _tb("Complete this partition:  %s = %s + ___ + %d"
                   % (_c(n), " + ".join(pre), o), ans, "int", {},
                   ["One hundred has been exchanged for ten tens.",
                    "%s + %s + %d = %s." % (" + ".join(pre), _c(ans), o, _c(n))])

    def t_regroup():
        a = random.randint(1, 7)
        b = random.randint(10, 16)
        cc = random.randint(0, 9)
        val = a * 1000 + b * 100 + cc
        return _tb("What number has %s, %s and %s?"
                   % (_pl(a, "thousand"), _pl(b, "hundred"), _pl(cc, "one")),
                   val, "int", {},
                   ["%d hundreds is %s, which is %d thousand%s."
                    % (b, _c(b * 100), b // 10, " and %s" % _c((b % 10) * 100) if b % 10 else ""),
                    "%s + %s + %d = %s." % (_c(a * 1000), _c(b * 100), cc, _c(val))])

    def t_word():
        who = pick(NAMES)
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        cc = random.randint(1, 9)
        val = a * 1000 + b * 100 + cc * 10
        return _tb("%s has %d bundle%s of notes worth £1,000 each, %d bundle%s worth £100 each "
                   "and %d £10 note%s. How much money does %s have altogether?"
                   % (who, a, "" if a == 1 else "s", b, "" if b == 1 else "s", cc, "" if cc == 1 else "s", who),
                   val, "int", {"unit": "£"},
                   ["%s + %s + %d = %s." % (_c(a * 1000), _c(b * 100), cc * 10, _c(val))])

    def t_how_many_left():
        m = _num_for(max(d, 1))
        return _tb("Take the thousands away from %s. What number is left?" % _c(m),
                   m % 1000, "int", {},
                   ["%s − %s = %s." % (_c(m), _c((m // 1000) * 1000), _c(m % 1000))])

    def t_table():
        m = _distinct4(max(d, 1))
        rows = [[_c(m), _c((m // 1000) * 1000), _c((m // 100) % 10 * 100),
                 str((m // 10) % 10 * 10), str(m % 10)]]
        col = random.randint(1, 4)
        vals = [(m // 1000) * 1000, ((m // 100) % 10) * 100, ((m // 10) % 10) * 10, m % 10]
        return _dt("This table partitions a number. What belongs in the empty cell?",
                   ["Number", "Thousands", "Hundreds", "Tens", "Ones"], rows,
                   vals[col - 1],
                   ["%s = %s." % (_c(m), " + ".join(_c(v) for v in vals))],
                   missing=[0, col])

    def t_build_expr():
        m = random.randint(111, 999)
        expr = " + ".join(str(x) for x in
                          [(m // 100) * 100, ((m // 10) % 10) * 10, m % 10] if x)
        return _bt("Build the number that is %s." % expr, m, ["%s = %d." % (expr, m)])

    return _pick_t([t_missing_part, t_recombine, t_expanded, t_two_part, t_flexible_th,
                    t_flexible_h, t_regroup, t_word, t_how_many_left],
                   [t_table, t_build_expr])


def _cross(a, up):
    """A 4-digit number where adding (up) or taking away `a` crosses the next boundary."""
    th = random.randint(1, 8)
    if a == 10:
        h = random.randint(0, 9)
        return th * 1000 + h * 100 + (90 + random.randint(0, 9) if up else random.randint(0, 9))
    if a == 100:
        return th * 1000 + (900 + random.randint(0, 99) if up else random.randint(0, 99))
    return th * 1000 + random.randint(0, 999)


@skill("Y4.0.f", "1000, 100 or 10 more or less", S0)
def _(d=1):
    d = _d(d)
    amt = pick([10, 100]) if d == 0 else pick([10, 100, 1000])
    n = random.randint(120, 880) if d == 0 else random.randint(1010, 8990)
    more = random.random() < 0.5

    def t_bare():
        ans = n + amt if more else n - amt
        return _tb("What is %s %s than %s?" % (_c(amt), "more" if more else "less", _c(n)),
                   ans, "int", {},
                   ["%s %s %s = %s." % (_c(n), "+" if more else "−", _c(amt), _c(ans))])

    def t_boundary():
        """A calculation that crosses a place-value boundary."""
        if d == 0:                           # 3-digit, crossing one hundred
            up = random.random() < 0.5
            base = random.randint(1, 8) * 100 + (random.randint(90, 99) if up
                                                 else random.randint(1, 9))
            ans = base + 10 if up else base - 10
            return _tb("What is 10 %s than %d?" % ("more" if up else "less", base),
                       ans, "int", {},
                       ["Watch the place-value boundary.",
                        "%d %s 10 = %d." % (base, "+" if up else "−", ans)])
        if d == 2:                           # crosses a thousand
            a = pick([10, 100])
            up = random.random() < 0.5
            base = random.randint(1, 8) * 1000 + \
                (1000 - a + random.randint(0, a - 1) if up else random.randint(0, a - 1))
            ans = base + a if up else base - a
            return _tb("What is %s %s than %s?" % (_c(a), "more" if up else "less", _c(base)),
                       ans, "int", {},
                       ["Watch the place-value boundary: the thousands digit changes too.",
                        "%s %s %s = %s." % (_c(base), "+" if up else "−", _c(a), _c(ans))])
        a = pick([10, 100, 1000])
        if a == 10:
            base = random.randint(1, 8) * 1000 + random.randint(1, 9) * 100 + 95
        elif a == 100:
            base = random.randint(1, 8) * 1000 + 950 + random.randint(0, 9)
        else:
            base = random.randint(1, 8) * 1000 + random.randint(1, 9) * 100 + random.randint(0, 9)
        up = random.random() < 0.5 or base - a < 0
        ans = base + a if up else base - a
        return _tb("What is %s %s than %s?" % (_c(a), "more" if up else "less", _c(base)),
                   ans, "int", {},
                   ["Watch the place-value boundary.",
                    "%s %s %s = %s." % (_c(base), "+" if up else "−", _c(a), _c(ans))])

    def t_word():
        who = pick(NAMES)
        thing = pick(["stickers", "stamps", "beads", "conkers"])
        ans = n + amt if more else n - amt
        if more:
            return _tb("%s has %s %s and then collects %s more. How many %s does %s have now?"
                       % (who, _c(n), thing, _c(amt), thing, who), ans, "int", {"unit": thing},
                       ["%s + %s = %s." % (_c(n), _c(amt), _c(ans))])
        return _tb("%s has %s %s and then gives %s of the %s away. How many %s does %s have "
                   "left?" % (who, _c(n), thing, _c(amt), thing, thing, who), ans, "int",
                   {"unit": thing},
                   ["%s − %s = %s." % (_c(n), _c(amt), _c(ans))])

    def t_money():
        who = pick(NAMES)
        a = {0: 100, 1: pick([100, 1000]), 2: pick([10, 100, 1000])}[d]
        base = random.randint(2, 8) * 1000 + random.randint(0, 9) * 100
        if d == 0:
            base = random.randint(2, 8) * 100 + random.randint(0, 9) * 10
        elif d == 2:
            base = _cross(a, more)
        return _tb("A charity has raised £%s. %s donates another £%s. How much has the "
                   "charity raised now?" % (_c(base), who, _c(a)), base + a, "int", {"unit": "£"},
                   ["£%s + £%s = £%s." % (_c(base), _c(a), _c(base + a))]) if more else \
            _tb("A charity has £%s and spends £%s on equipment. How much is left?"
                % (_c(base), _c(a)), base - a, "int", {"unit": "£"},
                ["£%s − £%s = £%s." % (_c(base), _c(a), _c(base - a))])

    def t_inverse():
        result = n + amt if more else n - amt
        return _tb("%s thought of a number, %s %s and got %s. What was the number?"
                   % (pick(NAMES), "added" if more else "subtracted", _c(amt), _c(result)),
                   n, "int", {},
                   ["Do the opposite: %s %s %s = %s."
                    % (_c(result), "−" if more else "+", _c(amt), _c(n))])

    def t_two_step():
        if d == 0:
            base = random.randint(220, 780)
            ans = base + 100 - 10
            return _tb("Start at %d. Add 100, then take away 10. What number do you reach?"
                       % base, ans, "int", {},
                       ["%d + 100 = %d." % (base, base + 100),
                        "%d − 10 = %d." % (base + 100, ans)])
        base = random.randint(2200, 7800)
        ans = base + 1000 - 100
        if d == 2:                           # three steps
            ans -= 10
            return _tb("Start at %s. Add 1,000, take away 100, then take away 10. "
                       "What number do you reach?" % _c(base), ans, "int", {},
                       ["%s + 1,000 = %s." % (_c(base), _c(base + 1000)),
                        "%s − 100 = %s." % (_c(base + 1000), _c(base + 900)),
                        "%s − 10 = %s." % (_c(base + 900), _c(ans))])
        return _tb("Start at %s. Add 1,000, then take away 100. What number do you reach?"
                   % _c(base), ans, "int", {},
                   ["%s + 1,000 = %s." % (_c(base), _c(base + 1000)),
                    "%s − 100 = %s." % (_c(base + 1000), _c(ans))])

    def t_how_much():
        a = random.randint(1, 8) * 1000 + random.randint(0, 9) * 100
        gap = pick([10, 100, 1000])
        if d == 0:
            a = random.randint(1, 8) * 100 + random.randint(1, 8) * 10
            gap = pick([10, 100])
        elif d == 2:                         # the gap crosses a boundary: harder to spot
            gap = pick([10, 100])
            a = _cross(gap, True)
        b = a + gap
        if d == 2:
            return _tb("Complete:  %s + ___ = %s" % (_c(a), _c(b)), gap, "int", {},
                       ["%s − %s = %s." % (_c(b), _c(a), _c(gap))])
        return _tb("How much MORE is %s than %s?" % (_c(b), _c(a)), gap, "int", {},
                   ["%s − %s = %s." % (_c(b), _c(a), _c(gap))])

    def t_line():
        base = random.randint(3, 18) * 500   # never 1,000, so "1,000 less" is not 0
        a = pick([100, 1000])
        step, major = 100, 500
        if d == 0:
            base, a, step, major = random.randint(2, 8) * 1000, 1000, 500, 1000
        elif d == 2:                         # a finer line, counting in tens
            base, a, step, major = random.randint(101, 989) * 10, 10, 10, 50
        up = random.random() < 0.5 or base - a < 0
        ans = base + a if up else base - a
        return _nl("Place the number that is %s %s than %s on the number line."
                   % (_c(a), "more" if up else "less", _c(base)), ans, step, major,
                   ["%s %s %s = %s." % (_c(base), "+" if up else "−", _c(a), _c(ans))])

    def t_build():
        base = random.randint(150, 850)
        a = pick([10, 100])
        up = random.random() < 0.5
        if d == 0:                           # no boundary to cross
            base = random.randint(2, 8) * 100 + random.randint(1, 8) * 10 + random.randint(0, 9)
        elif d == 2:                         # crosses a hundred
            a = 10
            base = random.randint(1, 8) * 100 + (random.randint(90, 99) if up
                                                 else random.randint(0, 9))
        ans = base + a if up else base - a
        return _bt("Build the number that is %d %s than %d." % (a, "more" if up else "less", base),
                   ans, ["%d %s %d = %d." % (base, "+" if up else "−", a, ans)])

    def t_io():
        a = pick([10, 100]) if d == 0 else pick([10, 100, 1000])
        up = random.random() < 0.5
        if d == 0:
            ins = sorted(random.sample(range(120, 880), 4))
        elif d == 2 and a < 1000:            # every row crosses a boundary
            ins = []
            while len(ins) < 4:
                x = _cross(a, up)
                if x not in ins:
                    ins.append(x)
            ins.sort()
        else:
            ins = sorted(random.sample(range(1200, 8800), 4))
        rows = [[i, i + a if up else i - a] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the empty cell?",
                   rows, miss, rows[miss][1],
                   ["The rule is %s %s." % ("add" if up else "subtract", _c(a)),
                    "%s %s %s = %s." % (_c(rows[miss][0]), "+" if up else "−",
                                        _c(a), _c(rows[miss][1]))],
                   rule="%s %s" % ("+" if up else "−", _c(a)))

    def t_table():
        if d == 0:
            ns = sorted(random.sample(range(120, 880), 3))
            a = pick([10, 100])
        else:
            ns = sorted(random.sample(range(1200, 8800), 3))
            a = pick([10, 100, 1000])
        if d == 2 and a < 1000:              # numbers sitting on a boundary
            ns = []
            while len(ns) < 3:
                x = _cross(a, random.random() < 0.5)
                if x not in ns:
                    ns.append(x)
            ns.sort()
        rows = [[_c(x), _c(x - a), _c(x + a)] for x in ns]
        r = random.randint(0, 2)
        col = pick([1, 2])
        ans = ns[r] - a if col == 1 else ns[r] + a
        return _dt("Complete the table. What number belongs in the empty cell?",
                   ["Number", "%s less" % _c(a), "%s more" % _c(a)], rows, ans,
                   ["%s %s %s = %s." % (_c(ns[r]), "−" if col == 1 else "+", _c(a), _c(ans))],
                   missing=[r, col])

    return _pick_t([t_bare, t_boundary, t_word, t_money, t_inverse, t_two_step, t_how_much],
                   [t_line, t_build, t_io, t_table])


@skill("Y4.0.g", "Even and odd numbers", S0)
def _(d=1):
    d = _d(d)

    def num():
        return _num_for(d)

    def t_bare():
        n = num()
        ans = "even" if n % 2 == 0 else "odd"
        return _wq("Is %s even or odd? (type 'even' or 'odd')" % _c(n), ans,
                   ["Look at the ones digit (%d)." % (n % 10),
                    "%s is %s." % (_c(n), ans)], "even / odd")

    def t_next():
        n = num()
        want = pick(["even", "odd"])
        m = n + 1
        while (m % 2 == 0) != (want == "even"):
            m += 1
        return _tb("What is the next %s number after %s?" % (want, _c(n)), m, "int", {},
                   ["%s is %s." % (_c(n), "even" if n % 2 == 0 else "odd"),
                    "The next %s number is %s." % (want, _c(m))])

    def t_before():
        n = num()
        want = pick(["even", "odd"])
        m = n - 1
        while (m % 2 == 0) != (want == "even"):
            m -= 1
        return _tb("Which %s number comes just BEFORE %s?" % (want, _c(n)), m, "int", {},
                   ["%s is %s." % (_c(n), "even" if n % 2 == 0 else "odd"),
                    "The %s number just before it is %s." % (want, _c(m))])

    def t_odd_one_out():
        want_odd = random.random() < 0.5

        def gen(is_odd):
            while True:
                m = num()
                if (m % 2 == 1) == is_odd:
                    return m
        target = gen(want_odd)
        opts = [target]
        while len(opts) < 4:
            m = gen(not want_odd)
            if m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Only ONE of these numbers is %s. Which one?   %s"
                   % ("odd" if want_odd else "even", _lst(opts)), target, "int", {},
                   ["Check the ones digit of each number.",
                    "%s is the %s one." % (_c(target), "odd" if want_odd else "even")])

    def t_count():
        opts = []
        while len(opts) < 6:
            m = num()
            if m not in opts:
                opts.append(m)
        want_even = random.random() < 0.5
        cnt = sum(1 for x in opts if (x % 2 == 0) == want_even)
        return _tb("How many of these numbers are %s?   %s"
                   % ("EVEN" if want_even else "ODD", _lst(opts)), cnt, "int", {},
                   ["The %s ones are: %s." % ("even" if want_even else "odd",
                                              _lst([x for x in opts
                                                    if (x % 2 == 0) == want_even]) or "none"),
                    "That is %d." % cnt])

    def t_share():
        n = num()
        ans = "yes" if n % 2 == 0 else "no"
        return _wq("Can %s sweets be shared equally between 2 children with none left over? "
                   "(type 'yes' or 'no')" % _c(n), ans,
                   ["%s is %s." % (_c(n), "even" if n % 2 == 0 else "odd"),
                    "So the answer is %s." % ans], "yes / no")

    def t_rule_add():
        a, b = pick([("odd", "odd"), ("odd", "even"), ("even", "even"), ("even", "odd")])
        ans = "even" if (a == b) else "odd"
        x = random.choice([3, 5, 7, 9] if a == "odd" else [2, 4, 6, 8])
        y = random.choice([3, 5, 7, 9] if b == "odd" else [2, 4, 6, 8])
        return _wq("Is the answer to '%s number + %s number' always even or always odd? "
                   "(type 'even' or 'odd')" % (a, b), ans,
                   ["Try an example: %d + %d = %d, which is %s." % (x, y, x + y, ans),
                    "%s + %s is always %s." % (a, b, ans)], "even / odd")

    def t_rule_multiply():
        a, b = pick([("odd", "odd"), ("odd", "even"), ("even", "even")])
        ans = "odd" if (a == "odd" and b == "odd") else "even"
        x = random.choice([3, 5, 7, 9] if a == "odd" else [2, 4, 6, 8])
        y = random.choice([3, 5, 7, 9] if b == "odd" else [2, 4, 6, 8])
        return _wq("Is the answer to '%s number × %s number' always even or always odd? "
                   "(type 'even' or 'odd')" % (a, b), ans,
                   ["Try an example: %d × %d = %d, which is %s." % (x, y, x * y, ans),
                    "An even factor always makes the product even.",
                    "%s × %s is always %s." % (a, b, ans)], "even / odd")

    def t_apply():
        a, b = num(), num()
        op = pick(["+", "−"])
        if op == "−" and a < b:
            a, b = b, a
        val = a + b if op == "+" else a - b
        ans = "even" if val % 2 == 0 else "odd"
        return _wq("Without working out the exact answer, is %s %s %s even or odd? "
                   "(type 'even' or 'odd')" % (_c(a), op, _c(b)), ans,
                   ["%s is %s and %s is %s."
                    % (_c(a), "even" if a % 2 == 0 else "odd",
                       _c(b), "even" if b % 2 == 0 else "odd"),
                    "So the answer is %s." % ans], "even / odd")

    def t_largest():
        n = num()
        want = pick(["even", "odd"])
        m = n - 1
        while (m % 2 == 0) != (want == "even"):
            m -= 1
        return _tb("What is the largest %s number that is smaller than %s?" % (want, _c(n)),
                   m, "int", {},
                   ["Count back from %s until the number is %s." % (_c(n), want),
                    "The answer is %s." % _c(m)])

    def t_how_many_between():
        a = random.randint(20, 80) * (1 if d == 0 else 10)
        b = a + pick([10, 20])
        want_even = random.random() < 0.5
        cnt = sum(1 for x in range(a + 1, b) if (x % 2 == 0) == want_even)
        return _tb("How many %s numbers are there between %s and %s (not counting %s and %s "
                   "themselves)?" % ("even" if want_even else "odd", _c(a), _c(b), _c(a), _c(b)),
                   cnt, "int", {},
                   ["List the numbers from %s to %s." % (_c(a + 1), _c(b - 1)),
                    "There are %d." % cnt])

    def t_line():
        n = random.randint(20, 60)
        if n % 2 == 0:
            n += 1
        ans = n + 1
        return _nl("Place the first EVEN number after %d on the number line." % n, ans, 2, 10,
                   ["%d is odd, so the next even number is %d." % (n, ans)])

    def t_build():
        want = pick(["even", "odd"])
        m = random.randint(120, 880)
        while (m % 2 == 0) != (want == "even"):
            m += 1
        return _bt("Build the smallest %s number that is bigger than %d." % (want, m - 2), m,
                   ["Count on from %d until the number is %s." % (m - 2, want),
                    "The answer is %d." % m])

    return _pick_t([t_bare, t_next, t_before, t_odd_one_out, t_count, t_share, t_rule_add,
                    t_rule_multiply, t_apply, t_largest, t_how_many_between],
                   [t_line, t_build])


@skill("Y4.0.h", "Roman numerals to 100", S0)
def _(d=1):
    d = _d(d)
    hi = {0: 20, 1: 50, 2: 100}[d]

    def num():
        return random.randint(1, hi)

    def t_roman_to_num():
        n = num()
        return _tb("Write this Roman numeral as a number:  %s" % _rom(n), n, "int", {},
                   ["%s = %d." % (_rom(n), n)])

    def t_num_to_roman():
        n = num()
        return _wq("Write %d as a Roman numeral." % n, _rom(n),
                   ["%d is written %s." % (n, _rom(n))], "e.g. XIV")

    def t_clock():
        n = random.randint(1, 12)
        return _tb("A clock face is numbered with Roman numerals. Which number does %s stand for?"
                   % _rom(n), n, "int", {},
                   ["%s = %d." % (_rom(n), n)])

    def t_chapter():
        who = pick(NAMES)
        n = num()
        return _tb("%s is reading Chapter %s of a book. Which chapter number is that?"
                   % (who, _rom(n)), n, "int", {},
                   ["%s = %d." % (_rom(n), n)])

    def t_add():
        a, b = random.randint(1, hi // 2), random.randint(1, hi // 2)
        return _tb("Work this out and write the answer as an ordinary number:  %s + %s"
                   % (_rom(a), _rom(b)), a + b, "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d + %d = %d." % (a, b, a + b)])

    def t_subtract():
        a = random.randint(hi // 2, hi)
        b = random.randint(1, a - 1)
        return _tb("Work this out and write the answer as an ordinary number:  %s − %s"
                   % (_rom(a), _rom(b)), a - b, "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d − %d = %d." % (a, b, a - b)])

    def t_greater():
        a, b = random.sample(range(1, hi + 1), 2)
        big = max(a, b)
        return _tb("Which is greater, %s or %s? Write your answer as an ordinary number."
                   % (_rom(a), _rom(b)), big, "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d is greater." % big])

    def t_more_than():
        n = random.randint(1, hi - 10)
        amt = pick([1, 5, 10])
        ans = n + amt
        return _wq("What is %d more than %s? Write your answer as a Roman numeral."
                   % (amt, _rom(n)), _rom(ans),
                   ["%s = %d, and %d + %d = %d." % (_rom(n), n, n, amt, ans),
                    "%d is written %s." % (ans, _rom(ans))], "e.g. XIV")

    def t_sequence():
        step = pick([s for s in [1, 2, 5, 10] if 4 * s < hi])
        start = random.randint(1, max(1, (hi - 4 * step)))
        terms = [start + i * step for i in range(4)]
        ans = terms[-1] + step
        return _wq("Continue this sequence of Roman numerals. What comes next?   %s, ___"
                   % ", ".join(_rom(t) for t in terms), _rom(ans),
                   ["The numbers are %s, going up in %ds." % (_lst(terms), step),
                    "%d + %d = %d, which is %s." % (terms[-1], step, ans, _rom(ans))],
                   "e.g. XIV")

    def t_largest_of_three():
        ns = random.sample(range(1, hi + 1), 3)
        big = max(ns)
        return _tb("Which of these Roman numerals is the largest? Write it as an ordinary "
                   "number.   %s" % ", ".join(_rom(x) for x in ns), big, "int", {},
                   ["In order: %s." % ", ".join("%s = %d" % (_rom(x), x) for x in sorted(ns)),
                    "The largest is %d." % big])

    def t_table():
        ns = sorted(random.sample(range(1, hi + 1), 4))
        rows = [[str(x), _rom(x)] for x in ns]
        r = random.randint(0, 3)
        want_roman = random.random() < 0.5
        if want_roman:
            return _dt("Complete the table. What Roman numeral belongs in the empty cell?",
                       ["Number", "Roman numeral"], rows, _rom(ns[r]),
                       ["%d is written %s." % (ns[r], _rom(ns[r]))],
                       missing=[r, 1], atype="str")
        return _dt("Complete the table. What ordinary number belongs in the empty cell?",
                   ["Number", "Roman numeral"], rows, ns[r],
                   ["%s = %d." % (_rom(ns[r]), ns[r])], missing=[r, 0])

    def t_line():
        n = random.randint(1, 10) * 5
        return _nl("Place the number %s on the number line." % _rom(n), n, 5, 25,
                   ["%s = %d." % (_rom(n), n)])

    return _pick_t([t_roman_to_num, t_num_to_roman, t_clock, t_chapter, t_add, t_subtract,
                    t_greater, t_more_than, t_sequence, t_largest_of_three],
                   [t_table, t_line])


@skill("Y4.0.i", "Ordinal numbers to 100th", S0)
def _(d=1):
    d = _d(d)
    top = {0: 20, 1: 50, 2: 100}[d]

    def t_figures():
        n = random.randint(2, top)
        return _wq("Write the ordinal number for position %d (in figures, e.g. 4th)." % n,
                   ordinal(n), ["Position %d is written %s." % (n, ordinal(n))], "e.g. 41st")

    def t_race():
        pos = random.randint(2, max(3, top - 5))
        total = pos + random.randint(1, 9)
        who = pick(NAMES)
        return _tb("%s finished %s in a race of %d runners. How many runners finished AFTER %s?"
                   % (who, ordinal(pos), total, who), total - pos, "int", {"unit": "runners"},
                   ["%d − %d = %d." % (total, pos, total - pos)])

    def t_from_back():
        total = random.randint(8, top)
        pos = random.randint(2, total - 1)
        who = pick(NAMES)
        return _tb("There are %d children in a queue. %s is %s from the FRONT. "
                   "What position is %s from the BACK?" % (total, who, ordinal(pos), who),
                   total - pos + 1, "int", {},
                   ["%d − %d = %d children are behind %s." % (total, pos, total - pos, who),
                    "So %s is %s from the back." % (who, ordinal(total - pos + 1))])

    def t_who():
        k = {0: 4, 1: 6, 2: 8}[d]
        names = random.sample(NAMES, k)
        pos = random.randint(2, k)
        return _wq("The finishing order was: %s. Who finished %s? (write the name)"
                   % (", ".join(names), ordinal(pos)), names[pos - 1],
                   ["Counting along the list, %s is %s." % (names[pos - 1], ordinal(pos))],
                   "a name")

    def t_between():
        a = random.randint(2, top - 10)
        b = a + random.randint(4, 10)
        return _tb("In a queue, one child is %s and another child is %s. How many children "
                   "are standing BETWEEN those two positions?"
                   % (ordinal(a), ordinal(b)), b - a - 1, "int", {},
                   ["%d − %d = %d, then take away the child at %s."
                    % (b, a, b - a, ordinal(b)),
                    "There are %d children between them." % (b - a - 1)])

    def t_later():
        a = random.randint(1, top - 12)
        gap = random.randint(3, 12)
        return _wq("Sports day is on the %s day of term. A concert is %d days later. "
                   "Which day of term is the concert? (write it like %s)"
                   % (ordinal(a), gap, ordinal(a)), ordinal(a + gap),
                   ["%d + %d = %d." % (a, gap, a + gap),
                    "That is the %s day." % ordinal(a + gap)], "e.g. 41st")

    def t_term():
        step = pick({0: [2, 5, 10], 1: [3, 4, 6, 7, 9, 25], 2: [6, 7, 9, 25]}[d])
        k = random.randint(*{0: (4, 8), 1: (4, 12), 2: (10, 20)}[d])
        ans = k * step
        return _tb("A sequence starts at %d and goes up in %ds: %d, %d, %d, ... "
                   "What is the %s term?" % (step, step, step, 2 * step, 3 * step, ordinal(k)),
                   ans, "int", {},
                   ["The %s term is %d × %d." % (ordinal(k), k, step),
                    "%d × %d = %s." % (k, step, _c(ans))])

    def t_every_nth():
        gap = pick([3, 4, 6, 25] if d == 2 else [2, 5, 10])
        k = random.randint(*{0: (3, 8), 1: (3, 12), 2: (8, 20)}[d])
        ans = gap * k
        return _tb("Every %s house on a street is painted white, starting with house number %d. "
                   "What is the number of the %s white house?" % (ordinal(gap), gap, ordinal(k)),
                   ans, "int", {},
                   ["%d × %d = %d." % (k, gap, ans)])

    def t_position_of():
        gap = pick([3, 4, 6, 25] if d == 2 else [2, 5, 10])
        k = random.randint(*{0: (3, 8), 1: (3, 12), 2: (8, 20)}[d])
        val = gap * k
        return _wq("Trees are planted every %d metres along a path, the first at %d m. "
                   "Which tree is at %d m? (write it like 4th)" % (gap, gap, val),
                   ordinal(k), ["%d ÷ %d = %d." % (val, gap, k),
                                "That is the %s tree." % ordinal(k)], "e.g. 12th")

    def t_last():
        total = random.randint(20, top)
        who = pick(NAMES)
        return _wq("%d people are in a queue and %s is last. What position is %s? "
                   "(write it like 4th)" % (total, who, who), ordinal(total),
                   ["The last of %d people is the %s." % (total, ordinal(total))], "e.g. 40th")

    def t_line():
        gap = {0: 10, 1: pick([5, 10]), 2: pick([5, 25])}[d]
        k = random.randint(3, 5) if d == 0 else random.randint(3, 9) if d == 1 else random.randint(6, 12)
        ans = gap * k
        major = 50 if gap == 5 else 100
        return _nl("Lamp posts stand every %d metres along a road, the first at %d m. "
                   "Place the %s lamp post on the line." % (gap, gap, ordinal(k)),
                   ans, gap, major,
                   ["%s lamp post = %d × %d = %d m." % (ordinal(k), k, gap, ans)])

    def t_table():
        names = random.sample(NAMES, 5)
        times = sorted(random.sample(range(45, 90), 5))
        rows = [[names[i], "%d seconds" % times[i]] for i in range(5)]
        pos = random.randint(1, 3) if d == 0 else random.randint(1, 5)
        if d == 2:                           # rows not in finishing order: sort them first
            random.shuffle(rows)
        return _dt("This table shows the times in a 400 m race (the fastest time wins). "
                   "Who finished %s? (write the name)" % ordinal(pos),
                   ["Runner", "Time"], rows, names[pos - 1],
                   ["The fastest time is %d seconds." % times[0],
                    "%s finished %s." % (names[pos - 1], ordinal(pos))], atype="str")

    return _pick_t([t_figures, t_race, t_from_back, t_who, t_between, t_later, t_term,
                    t_every_nth, t_position_of, t_last], [t_line, t_table])


@skill("Y4.0.j", "Negative numbers and counting through zero", S0)
def _(d=1):
    d = _d(d)
    span = {0: 6, 1: 10, 2: 20}[d]
    lim = min(9, span) if d < 2 else 19      # how far from 0 the number line reaches
    lo, hi = (-10, 10) if d < 2 else (-20, 20)

    def t_count_back():
        if d == 2:                           # in tens, further below zero
            start = 10 * random.randint(1, 2)
            terms = [start - 10 * i for i in range(4)]
            ans = terms[-1] - 10
            return _tb("Count back in tens:  %s, ___  What number comes next?"
                       % ", ".join(str(t) for t in terms), ans, "int", {},
                       ["Keep subtracting 10, straight through zero.",
                        "%d − 10 = %d." % (terms[-1], ans)])
        start = random.randint(1, 3)
        terms = [start - i for i in range(4)]
        ans = terms[-1] - 1
        return _tb("Count back in ones:  %s, ___  What number comes next?"
                   % ", ".join(str(t) for t in terms), ans, "int", {},
                   ["Counting back past zero gives negative numbers.",
                    "%d − 1 = %d." % (terms[-1], ans)])

    def t_count_back_step():
        step = pick({0: [2, 5], 1: [2, 3, 5], 2: [4, 6, 25]}[d])
        start = step * random.randint(1, 3)
        terms = [start - i * step for i in range(4)]
        ans = terms[-1] - step
        return _tb("Count back in %ds:  %s, ___  What number comes next?"
                   % (step, ", ".join(str(t) for t in terms)), ans, "int", {},
                   ["Keep subtracting %d, straight through zero." % step,
                    "%d − %d = %d." % (terms[-1], step, ans)])

    def t_temp_fall():
        start = random.randint(1, span)
        fall = start + random.randint(1, span)
        ans = start - fall
        return _tb("At midday the temperature is %d°C. By midnight it has fallen by %d°C. "
                   "What is the temperature at midnight?" % (start, fall), ans, "int",
                   {"unit": "°C"},
                   ["%d − %d = %d." % (start, fall, ans),
                    "The temperature is %d°C." % ans])

    def t_temp_rise():
        start = -random.randint(1, span)
        rise = random.randint(1, 2 * span)
        ans = start + rise
        return _tb("At 6 am the temperature is %d°C. By noon it has risen by %d°C. "
                   "What is the temperature at noon?" % (start, rise), ans, "int", {"unit": "°C"},
                   ["%d + %d = %d." % (start, rise, ans),
                    "The temperature is %d°C." % ans])

    def t_difference():
        a = -random.randint(1, span)
        b = random.randint(1, span)
        return _tb("How many degrees warmer is %d°C than %d°C?" % (b, a), b - a, "int",
                   {"unit": "°C"},
                   ["From %d°C up to 0°C is %s." % (a, _pl(-a, "degree")),
                    "Then 0°C up to %d°C is %d more, so %d degrees altogether."
                    % (b, b, b - a)])

    def t_missing():
        step = pick({0: [1, 2], 1: [1, 2, 5], 2: [3, 4, 25]}[d])
        start = step * (2 if d < 2 else random.randint(1, 3))
        terms = [start - i * step for i in range(6)]
        idx = random.randint(3, 5)
        shown = ", ".join("___" if i == idx else str(t) for i, t in enumerate(terms))
        return _tb("This sequence counts back through zero. Find the missing number:  %s" % shown,
                   terms[idx], "int", {},
                   ["The rule is subtract %d each time." % step,
                    "%d − %d = %d." % (terms[idx - 1], step, terms[idx])])

    def t_lift():
        who = pick(NAMES)
        down = random.randint(1, 2 if d == 0 else 3)
        up = random.randint(1, 3 if d == 0 else 5)
        ans = -down + up
        if d == 2:                           # two moves
            back = random.randint(ans + 1, ans + 4)
            return _tb("In a car park, floor 0 is the ground floor and the basement floors are "
                       "−1, −2 and so on. %s parks on floor %d, goes up %s, then down %s. "
                       "Which floor is %s on now?"
                       % (who, -down, _pl(up, "floor"), _pl(back, "floor"), who),
                       ans - back, "int", {},
                       ["%d + %d = %d." % (-down, up, ans),
                        "%d − %d = %d." % (ans, back, ans - back)])
        return _tb("In a car park, floor 0 is the ground floor and the basement floors are "
                   "−1, −2 and so on. %s parks on floor %d, then goes up %s. "
                   "Which floor is %s on now?" % (who, -down, _pl(up, "floor"), who), ans, "int", {},
                   ["%d + %d = %d." % (-down, up, ans)])

    def t_how_far():
        n = -random.randint(1, span)
        return _tb("How many do you count on from %d to reach 0?" % n, -n, "int", {},
                   ["From %d to 0 is %d." % (n, -n)])

    def t_line_place():
        ans = -random.randint(1, lim)
        return _nl("Place %d on the number line." % ans, ans, 1, 5, lo=lo, hi=hi,
                   solution=["Negative numbers sit to the LEFT of zero.",
                             "%d is %d to the left of 0." % (ans, -ans)])

    def t_graph_integer():
        ans = pick([-1, 1]) * random.randint(1, lim)
        return _nl("Mark the number %d on the number line." % ans, ans, 1, 5, lo=lo, hi=hi,
                   solution=["Numbers below zero go to the left of zero; "
                             "numbers above zero go to the right.",
                             "%d is %d to the %s of 0."
                             % (ans, abs(ans), "left" if ans < 0 else "right")])

    def t_graph_integer_count():
        start = random.randint(-5, 5) if d < 2 else random.randint(-9, 9)
        move = random.randint(1, 5) if d < 2 else random.randint(6, 11)
        back = random.random() < 0.5
        ans = start - move if back else start + move
        return _nl("Start at %d and count %s %d. "
                   "Mark the number you reach on the number line."
                   % (start, "back" if back else "on", move), ans, 1, 5, lo=lo, hi=hi,
                   solution=["%d %s %d = %d." % (start, "−" if back else "+", move, ans)])

    def t_line_count():
        start = random.randint(1, {0: 3, 1: 5, 2: 9}[d])
        back = start + random.randint(1, {0: 4, 1: 8, 2: 10}[d])
        ans = start - back
        return _nl("Start at %d and count back %d. Place the number you land on."
                   % (start, back), ans, 1, 5, lo=lo, hi=hi,
                   solution=["%d − %d = %d." % (start, back, ans)])

    def t_line_temp():
        ans = -random.randint(1, lim)
        return _nl("The temperature is %d°C. Place that temperature on the number line." % ans,
                   ans, 1, 5, lo=lo, hi=hi,
                   solution=["%d°C is %s below zero." % (ans, _pl(-ans, "degree"))])

    def t_graph():
        hours = ["6 am", "9 am", "12 pm", "3 pm", "6 pm"]
        vals = [-random.randint(*{0: (1, 3), 1: (2, 6), 2: (6, 10)}[d])]
        for _i in range(4):                  # d=2: the temperature can dip as well as rise
            vals.append(vals[-1] + (pick([-2, -1, 1, 2, 3]) if d == 2 else random.randint(1, 3)))
        idx = random.randint(0, 4)
        return _lg("This graph shows the temperature during one day. "
                   "What was the temperature at %s?" % hours[idx],
                   list(zip(hours, vals)), vals[idx],
                   ["Read up from %s to the plotted point." % hours[idx],
                    "The temperature was %d°C." % vals[idx]], missing=idx)

    def t_graph_rise():
        hours = ["6 am", "8 am", "10 am", "12 pm", "2 pm"]
        vals = [-random.randint(*{0: (1, 3), 1: (3, 7), 2: (6, 10)}[d])]
        for _i in range(4):
            vals.append(vals[-1] + random.randint(1, 4 if d == 2 else 3))
        return _lg("This graph shows the temperature during one morning. "
                   "How many degrees did the temperature rise between 6 am and 2 pm?",
                   list(zip(hours, vals)), vals[-1] - vals[0],
                   ["At 6 am it was %d°C and at 2 pm it was %d°C." % (vals[0], vals[-1]),
                    "%d − (%d) = %d degrees." % (vals[-1], vals[0], vals[-1] - vals[0])])

    return _pick_t([t_count_back, t_count_back_step, t_temp_fall, t_temp_rise, t_difference,
                    t_missing, t_lift, t_how_far],
                   [t_line_place, t_line_count, t_line_temp, t_graph, t_graph_rise,
                    t_graph_integer, t_graph_integer_count])


@skill("Y4.0.k", "Compare and order positive and negative integers", S0)
def _(d=1):
    d = _d(d)
    span = {0: 6, 1: 10, 2: 20}[d]

    def sample(k, lo=None, hi=None):
        """k distinct integers, at least one of them negative."""
        lo = -span if lo is None else lo
        hi = span if hi is None else hi
        while True:
            ns = random.sample(range(lo, hi + 1), k)
            if any(x < 0 for x in ns):
                return ns

    def uk_day(k):
        """k midday temperatures for UK towns on ONE day: within about 11 degrees of each other."""
        lo = random.randint(-min(span, 12), -1 if d < 2 else -4)
        return sample(k, lo, lo + 11)

    def two():
        a, b = sample(2)
        if random.random() < 0.1:
            b = a
        return a, b

    def t_symbol():
        a, b = two()
        ans = "=" if a == b else (">" if a > b else "<")
        return _wq("Compare:  %d ___ %d   (write <, > or =)" % (a, b), ans,
                   ["On a number line, %d is to the %s of %d."
                    % (a, "right" if a > b else ("left" if a < b else "same place as"), b),
                    "%d %s %d." % (a, ans, b)], "<, > or =")

    def t_greater():
        a, b = sample(2)
        return _tb("Which is greater, %d or %d?" % (a, b), max(a, b), "int", {},
                   ["The number further to the right on a number line is greater.",
                    "%d is greater than %d." % (max(a, b), min(a, b))])

    def t_smallest():
        ns = sample(4)
        return _tb("Which is the SMALLEST of these numbers?   %s"
                   % ", ".join(str(x) for x in ns), min(ns), "int", {},
                   ["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                    "The smallest is %d." % min(ns)])

    def t_nth_lowest():
        ns = sample(5)
        k = random.randint(2, 4)
        ans = sorted(ns)[k - 1]
        return _tb("Put these numbers in order from lowest to highest:  %s. "
                   "Which number comes %s?" % (", ".join(str(x) for x in ns), ordinal(k)),
                   ans, "int", {},
                   ["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                    "The %s number is %d." % (ordinal(k), ans)])

    def t_coldest():
        cities = random.sample(["Leeds", "Cardiff", "Dundee", "Truro", "Belfast", "Norwich"], 4)
        temps = uk_day(4)
        coldest = random.random() < 0.5
        val = min(temps) if coldest else max(temps)
        who = cities[temps.index(val)]
        pairs = ", ".join("%s %d°C" % (c, t) for c, t in zip(cities, temps))
        return _wq("Midday temperatures: %s. Which place was the %s? (write the name)"
                   % (pairs, "coldest" if coldest else "warmest"), who,
                   ["In order: %s." % ", ".join("%d°C" % t for t in sorted(temps)),
                    "The %s was %s at %d°C."
                    % ("coldest" if coldest else "warmest", who, val)], "a place name")

    def t_between():
        a = random.randint(-span, 0)
        b = a + random.randint(3, 8)
        target = random.randint(a + 1, b - 1)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(-span - 5, span + 5)
            if not (a < m < b) and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers lies BETWEEN %d and %d?   %s"
                   % (a, b, ", ".join(str(x) for x in opts)), target, "int", {},
                   ["%d is greater than %d and less than %d." % (target, a, b)])

    def t_count_up_first():
        a, b = random.sample(range(-span, 0), 2)
        first = min(a, b)
        return _tb("Counting up from %d, which number do you reach FIRST: %d or %d?"
                   % (-span - 2, a, b), first, "int", {},
                   ["Counting up, the smaller number comes first.",
                    "%d is smaller than %d." % (first, max(a, b))])

    def t_warmer_by():
        a = -random.randint(1, span)
        b = random.randint(0, span)
        return _tb("On Monday the temperature was %d°C and on Tuesday it was %d°C. "
                   "How many degrees warmer was Tuesday?" % (a, b), b - a, "int", {"unit": "°C"},
                   ["From %d°C to 0°C is %s, then 0°C to %d°C is %d more."
                    % (a, _pl(-a, "degree"), b, b),
                    "That is %s warmer." % _pl(b - a, "degree")])

    def t_line_smaller():
        a, b = sample(2, *{0: (-5, 5), 1: (-9, 9), 2: (-9, 2)}[d])     # stretch: mostly two negatives
        smaller = random.random() < 0.5
        ans = min(a, b) if smaller else max(a, b)
        return _nl("Compare %d and %d. Place the %s number on the number line."
                   % (a, b, "SMALLER" if smaller else "GREATER"), ans, 1, 5, lo=-10, hi=10,
                   solution=["Numbers get smaller as you move left.",
                             "%d is greater than %d." % (max(a, b), min(a, b)),
                             "The %s number is %d." % ("smaller" if smaller else "greater", ans)])

    def t_line_order():
        ns = sample(4, *{0: (-5, 5), 1: (-9, 9), 2: (-9, 3)}[d])
        k = random.randint(1, 4)
        ans = sorted(ns)[k - 1]
        return _nl("Order these numbers from lowest to highest:  %s. Place the %s one on "
                   "the number line." % (", ".join(str(x) for x in ns), ordinal(k)),
                   ans, 1, 5, lo=-10, hi=10,
                   solution=["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                             "The %s is %d." % (ordinal(k), ans)])

    def t_table():
        cities = random.sample(["Leeds", "Cardiff", "Dundee", "Truro", "Belfast", "Norwich"], 5)
        temps = uk_day(5)
        rows = [[cities[i], "%d°C" % temps[i]] for i in range(5)]
        k = random.randint(1, 5)
        order = sorted(range(5), key=lambda i: temps[i])
        who = cities[order[k - 1]]
        return _dt("This table shows midday temperatures. Which place was the %s? "
                   "(write the name)" % _rank(k, "coldest"),
                   ["Place", "Temperature"], rows, who,
                   ["Coldest first: %s." % ", ".join("%s %d°C" % (cities[i], temps[i])
                                                     for i in order),
                    "The %s is %s." % (_rank(k, "coldest"), who)], atype="str")

    return _pick_t([t_symbol, t_greater, t_smallest, t_nth_lowest, t_coldest, t_between,
                    t_count_up_first, t_warmer_by],
                   [t_line_smaller, t_line_order, t_table])


# ================================================================== 4.1 ======
@skill("Y4.1.a", "Compare and order numbers to 10,000", S1)
def _(d=1):
    d = _d(d)

    def one():
        return _num_for(d)

    def two():
        a = one()
        b = a if random.random() < 0.12 else one()
        return a, b

    def vals_for(k):
        """k different 4-digit values: d=0 all thousands digits differ, d=2 they share one."""
        if d == 0:
            return [t * 1000 + random.randint(0, 999) for t in random.sample(range(1, 10), k)]
        if d == 2:
            th = random.randint(1, 9) * 1000
            if random.random() < 0.5:        # same hundreds digit too
                th += random.randint(0, 9) * 100
                return [th + x for x in random.sample(range(0, 100), k)]
            return [th + x for x in random.sample(range(0, 1000), k)]
        return random.sample(range(1200, 9800), k)

    def t_symbol():
        a, b = two()
        ans = "=" if a == b else (">" if a > b else "<")
        return _wq("Compare:  %s ___ %s   (write <, > or =)" % (_c(a), _c(b)), ans,
                   ["Compare the thousands first, then the hundreds, tens and ones.",
                    "%s %s %s." % (_c(a), ans, _c(b))], "<, > or =")

    def t_symbol_sum():
        a = random.randint(1000, 4000)
        b = random.randint(100, 3000)
        cc = random.randint(1500, 7000)
        if d == 0:                           # whole thousands and hundreds only
            a, b = random.randint(1, 4) * 1000, random.randint(1, 9) * 100
            cc = random.randint(15, 70) * 100
        elif d == 2:                         # a sum on each side
            e = random.randint(100, 3000)
            cc = random.randint(1000, 4000)
            e = a + b - cc + pick([-10, -1, 0, 1, 10, 100]) if 100 < a + b - cc < 3000 else e
            left, right = a + b, cc + e
            ans = "=" if left == right else (">" if left > right else "<")
            return _wq("Compare:  %s + %s ___ %s + %s   (write <, > or =)"
                       % (_c(a), _c(b), _c(cc), _c(e)), ans,
                       ["%s + %s = %s." % (_c(a), _c(b), _c(left)),
                        "%s + %s = %s." % (_c(cc), _c(e), _c(right)),
                        "%s %s %s." % (_c(left), ans, _c(right))], "<, > or =")
        left = a + b
        ans = "=" if left == cc else (">" if left > cc else "<")
        return _wq("Compare:  %s + %s ___ %s   (write <, > or =)" % (_c(a), _c(b), _c(cc)), ans,
                   ["%s + %s = %s." % (_c(a), _c(b), _c(left)),
                    "%s %s %s." % (_c(left), ans, _c(cc))], "<, > or =")

    def t_greater():
        a, b = two()
        while a == b:
            b = one()
        return _tb("Which is greater, %s or %s? Write the greater number." % (_c(a), _c(b)),
                   max(a, b), "int", {},
                   ["%s is greater than %s." % (_c(max(a, b)), _c(min(a, b)))])

    def t_word():
        a, b = two()
        while a == b:
            b = one()
        n1, n2 = random.sample(NAMES, 2)
        thing = pick(["points", "steps", "stickers", "air miles"])
        who = n1 if a > b else n2
        return _wq("%s scored %s %s and %s scored %s %s. Who scored more? (write the name)"
                   % (n1, _c(a), thing, n2, _c(b), thing), who,
                   ["%s is greater than %s." % (_c(max(a, b)), _c(min(a, b))),
                    "So %s scored more." % who], "a name")

    def t_words_compare():
        a, b = one(), one()
        while a == b:
            b = one()
        return _tb("Which is smaller, '%s' or '%s'? Write it in numerals."
                   % (_w4(a), _w4(b)), min(a, b), "int", {},
                   ["'%s' is %s and '%s' is %s." % (_w4(a), _c(a), _w4(b), _c(b)),
                    "%s is smaller." % _c(min(a, b))])

    def t_extreme():
        ns = random.sample(range(1000, 9999) if d >= 1 else range(101, 999), 4)
        if d == 2:                           # stretch: they share the thousands digit
            ns = vals_for(4)
        big = random.random() < 0.5
        ans = max(ns) if big else min(ns)
        return _tb("Which is the %s of these numbers?   %s"
                   % ("largest" if big else "smallest", _lst(ns)), ans, "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The %s is %s." % ("largest" if big else "smallest", _c(ans))])

    def t_nth():
        ns = random.sample(range(1000, 9999) if d >= 1 else range(101, 999), 5)
        if d == 2:
            ns = vals_for(5)
        k = random.randint(2, 4)
        asc = random.random() < 0.5
        ans = sorted(ns)[k - 1] if asc else sorted(ns, reverse=True)[k - 1]
        return _tb("Put these numbers in order from %s:  %s. Which number comes %s?"
                   % ("smallest to largest" if asc else "largest to smallest",
                      _lst(ns), ordinal(k)), ans, "int", {},
                   ["In order: %s." % _lst(sorted(ns) if asc else sorted(ns, reverse=True)),
                    "The %s is %s." % (ordinal(k), _c(ans))])

    def t_between():
        a = random.randint(1000, 7000)
        b = a + random.randint(300, 900)
        if d == 0:
            a = random.randint(1, 7) * 1000
            b = a + 1000
        elif d == 2:                         # a narrow gap, distractors just outside it
            b = a + random.randint(20, 90)
        target = random.randint(a + 1, b - 1)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(a - 200, b + 200) if d == 2 else random.randint(1000, 9999)
            if not (a < m < b) and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers lies BETWEEN %s and %s?   %s"
                   % (_c(a), _c(b), _lst(opts)), target, "int", {},
                   ["%s is bigger than %s and smaller than %s."
                    % (_c(target), _c(a), _c(b))])

    def t_table_extreme():
        teams = random.sample(["Rovers", "City", "United", "Albion", "Wanderers", "Athletic"], 4)
        vals = vals_for(4)
        rows = [[teams[i], _c(vals[i])] for i in range(4)]
        big = random.random() < 0.5
        val = max(vals) if big else min(vals)
        who = teams[vals.index(val)]
        return _dt("This table shows the crowd at four football matches. Which team had the "
                   "%s crowd? (write the name)" % ("largest" if big else "smallest"),
                   ["Team", "Crowd"], rows, who,
                   ["In order: %s." % _lst(sorted(vals)),
                    "The %s crowd was %s, at %s."
                    % ("largest" if big else "smallest", _c(val), who)], atype="str")

    def t_table_nth():
        towns = random.sample(["Ashby", "Redhill", "Newport", "Stanton", "Hartley", "Elmwood"], 5)
        vals = vals_for(5)
        rows = [[towns[i], _c(vals[i])] for i in range(5)]
        k = random.randint(1, 5)
        order = sorted(range(5), key=lambda i: -vals[i])
        who = towns[order[k - 1]]
        return _dt("This table shows the population of five villages. Which village has the "
                   "%s population? (write the name)" % _rank(k, "largest"),
                   ["Village", "People"], rows, who,
                   ["Largest first: %s." % ", ".join("%s %s" % (towns[i], _c(vals[i]))
                                                     for i in order),
                    "The %s population is %s." % (_rank(k, "largest"), who)], atype="str")

    def t_table_value():
        towns = random.sample(["Ashby", "Redhill", "Newport", "Stanton", "Hartley"], 4)
        vals = vals_for(4)
        rows = [[towns[i], _c(vals[i])] for i in range(4)]
        k = random.randint(1, 4)
        val = sorted(vals)[k - 1]
        return _dt("This table shows how many books each library lent last month. "
                   "Write the %s number in the table." % _rank(k, "smallest"),
                   ["Library", "Books lent"], rows, val,
                   ["In order: %s." % _lst(sorted(vals)),
                    "The %s number is %s." % (_rank(k, "smallest"), _c(val))])

    def t_line():
        unit, step, major = {0: (1000, 1000, 5000), 1: (500, 500, 2500), 2: (100, 100, 500)}[d]
        a = random.randint(2, 19) * 500
        if d == 0:
            a = random.randint(1, 9) * 1000
        elif d == 2:                         # close together: only the hundreds differ
            a = random.randint(11, 95) * 100
        b = a
        while b == a:
            b = random.randint(2, 19) * 500 if d == 1 else \
                random.randint(1, 9) * 1000 if d == 0 else a + random.randint(-4, 4) * 100
        big = random.random() < 0.5
        ans = max(a, b) if big else min(a, b)
        return _nl("Compare %s and %s. Place the %s number on the number line."
                   % (_c(a), _c(b), "GREATER" if big else "SMALLER"), ans, step, major,
                   ["On a number line the greater number is further to the right.",
                    "%s is greater than %s." % (_c(max(a, b)), _c(min(a, b)))])

    def t_build():
        a, b = random.sample(range(101, 999), 2)
        if d == 0:                           # different hundreds digits
            h1, h2 = random.sample(range(1, 10), 2)
            a, b = h1 * 100 + random.randint(0, 99), h2 * 100 + random.randint(0, 99)
        elif d == 2:                         # same hundreds digit: compare the tens and ones
            h = random.randint(1, 9) * 100
            a, b = [h + x for x in random.sample(range(0, 100), 2)]
        return _bt("Build the SMALLER of these two numbers: %d and %d." % (a, b), min(a, b),
                   ["%d is greater than %d." % (max(a, b), min(a, b)),
                    "The smaller number is %d." % min(a, b)])

    return _pick_t([t_symbol, t_symbol_sum, t_greater, t_word, t_words_compare, t_extreme,
                    t_nth, t_between],
                   [t_table_extreme, t_table_nth, t_table_value, t_line, t_build])


@skill("Y4.1.b", "Round to the nearest 10 or 100", S1)
def _(d=1):
    d = _d(d)
    lo, hi = {0: (101, 989), 1: (1001, 9899), 2: (1001, 9899)}[d]

    def num(unit):
        if d == 2:
            r = random.random()
            if r < 0.35:                     # exactly halfway
                return random.randint(lo // unit, (hi - unit) // unit) * unit + unit // 2
            if r < 0.7:                      # rounding up rolls over the next place: 3,697 -> 3,700
                if unit == 10:
                    return random.randint(11, 98) * 100 - random.randint(1, 4)
                return random.randint(2, 9) * 1000 - random.randint(1, 49)
        return random.randint(lo, hi)

    def t_bare10():
        n = num(10)
        return _tb("Round %s to the nearest 10." % _c(n), _r10(n), "int", {},
                   ["The ones digit is %d." % (n % 10),
                    "%s rounds to %s." % (_c(n), _c(_r10(n)))])

    def t_bare100():
        n = num(100)
        return _tb("Round %s to the nearest 100." % _c(n), _r100(n), "int", {},
                   ["The tens digit is %d." % ((n // 10) % 10),
                    "%s rounds to %s." % (_c(n), _c(_r100(n)))])

    def t_word():
        n = num(pick([10, 100]))
        unit = pick([10, 100])
        who = pick(NAMES)
        thing = pick(["beads", "stickers", "conkers", "sunflower seeds"])
        return _tb("%s counted %s %s. Round that number to the nearest %d."
                   % (who, _c(n), thing, unit), _r(n, unit), "int", {"unit": thing},
                   ["%s rounds to %s." % (_c(n), _c(_r(n, unit)))])

    def t_crowd():
        n = random.randint(105, 985) if d == 0 else random.randint(1005, 9895)
        unit = pick([10, 100])
        if d == 2:
            n = num(unit)
        return _tb("%s people watched a match. Round that number to the nearest %d."
                   % (_c(n), unit), _r(n, unit), "int", {"unit": "people"},
                   ["Look at the digit to the right of the %s place."
                    % ("tens" if unit == 10 else "hundreds"),
                    "%s rounds to %s." % (_c(n), _c(_r(n, unit)))])

    def t_inverse():
        unit = pick([10, 100])
        r = random.randint(lo // unit + 1, hi // unit) * unit
        if d == 2:                           # a round number: the range crosses the next place
            r = random.randint(2, 9) * 10 * unit if unit == 100 else random.randint(11, 98) * 100
        smallest = random.random() < 0.5
        ans = r - unit // 2 if smallest else r + unit // 2 - 1
        return _tb("A whole number rounds to %s when rounded to the nearest %d. "
                   "What is the %s number it could be?"
                   % (_c(r), unit, "SMALLEST" if smallest else "LARGEST"), ans, "int", {},
                   ["Every number from %s to %s rounds to %s."
                    % (_c(r - unit // 2), _c(r + unit // 2 - 1), _c(r)),
                    "The %s is %s." % ("smallest" if smallest else "largest", _c(ans))])

    def t_odd_one_out():
        unit = pick([10, 100])
        r = random.randint(lo // unit + 1, hi // unit - 1) * unit
        target = random.randint(r - unit // 2, r + unit // 2 - 1)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(r - 2 * unit, r + 2 * unit) if d == 2 else random.randint(lo, hi)
            if _r(m, unit) != r and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers rounds to %s when rounded to the nearest %d?   %s"
                   % (_c(r), unit, _lst(opts)), target, "int", {},
                   ["Only %s lies between %s and %s."
                    % (_c(target), _c(r - unit // 2), _c(r + unit // 2 - 1)),
                    "%s rounds to %s." % (_c(target), _c(r))])

    def t_both():
        unit = pick([10, 100])
        n = num(unit)
        other = 100 if unit == 10 else 10
        return _tb("%s is rounded to the nearest %d and to the nearest %d. "
                   "What is it rounded to the nearest %d?" % (_c(n), other, unit, unit),
                   _r(n, unit), "int", {},
                   ["To the nearest %d, %s rounds to %s." % (unit, _c(n), _c(_r(n, unit)))])

    def t_difference():
        unit = pick([10, 100])
        n = num(unit)
        while n % unit == 0:                 # a change of 0 is no question
            n = num(unit)
        ans = abs(_r(n, unit) - n)
        return _tb("%s is rounded to the nearest %d. How much does the number change by?"
                   % (_c(n), unit), ans, "int", {},
                   ["%s rounds to %s." % (_c(n), _c(_r(n, unit))),
                    "The difference is %d." % ans])

    def t_line():
        n = num(pick([10, 100]))
        unit = pick([10, 100])
        ans = _r(n, unit)
        if unit == 10:
            return _nl("Round %s to the nearest 10 and place your answer on the number line."
                       % _c(n), ans, 10, 50,
                       ["The ones digit is %d." % (n % 10),
                        "%s rounds to %s." % (_c(n), _c(ans))])
        return _nl("Round %s to the nearest 100 and place your answer on the number line."
                   % _c(n), ans, 100, 500,
                   ["The tens digit is %d." % ((n // 10) % 10),
                    "%s rounds to %s." % (_c(n), _c(ans))])

    def t_io():
        unit = pick([10, 100])
        ins = []
        while len(ins) < 4:
            x = num(unit)
            if x not in ins:
                ins.append(x)
        ins.sort()
        rows = [[i, _r(i, unit)] for i in ins]
        miss = random.randint(0, 3)
        return _io("Each Out number is the In number rounded to the nearest %d. "
                   "What goes in the empty cell?" % unit, rows, miss, rows[miss][1],
                   ["%s rounds to %s." % (_c(rows[miss][0]), _c(rows[miss][1]))],
                   rule="round to nearest %d" % unit)

    def t_table():
        ns = []
        while len(ns) < 3:
            x = num(pick([10, 100]))
            if x not in ns:
                ns.append(x)
        ns.sort()
        rows = [[_c(x), _c(_r10(x)), _c(_r100(x))] for x in ns]
        r = random.randint(0, 2)
        col = pick([1, 2])
        ans = _r10(ns[r]) if col == 1 else _r100(ns[r])
        return _dt("Complete the rounding table. What number belongs in the empty cell?",
                   ["Number", "Nearest 10", "Nearest 100"], rows, ans,
                   ["%s rounded to the nearest %d is %s."
                    % (_c(ns[r]), 10 if col == 1 else 100, _c(ans))], missing=[r, col])

    def t_build():
        n = random.randint(111, 899)
        unit = pick([10, 100])
        if d == 2:                           # halfway, or rounding rolls over a hundred
            if unit == 100:
                n = random.randint(1, 8) * 100 + 50
            else:
                n = pick([random.randint(2, 9) * 100 - random.randint(1, 4),
                          random.randint(11, 89) * 10 + 5])
        ans = _r(n, unit)
        return _bt("Round %d to the nearest %d, then build your answer with the blocks."
                   % (n, unit), ans, ["%d rounds to %d." % (n, ans)])

    return _pick_t([t_bare10, t_bare100, t_word, t_crowd, t_inverse, t_odd_one_out, t_both,
                    t_difference], [t_line, t_io, t_table, t_build])


@skill("Y4.1.c", "Round to the nearest 1000", S1)
def _(d=1):
    d = _d(d)
    lo, hi = (1050, 8950) if d == 0 else (1005, 9995)

    def num():
        if d == 2 and random.random() < 0.35:
            return random.randint(1, 8) * 1000 + 500          # exact halfway
        return random.randint(lo, hi)

    def t_bare():
        n = num()
        return _tb("Round %s to the nearest 1,000." % _c(n), _r1000(n), "int", {},
                   ["The hundreds digit is %d." % ((n // 100) % 10),
                    "%s rounds to %s." % (_c(n), _c(_r1000(n)))])

    def t_word():
        n = num()
        return _tb("%s people ran a marathon. Round that number to the nearest 1,000."
                   % _c(n), _r1000(n), "int", {"unit": "people"},
                   ["The hundreds digit is %d." % ((n // 100) % 10),
                    "%s rounds to %s." % (_c(n), _c(_r1000(n)))])

    def t_money_car():
        n = num()
        return _tb("A second-hand car costs £%s. Round that price to the nearest £1,000."
                   % _c(n), _r1000(n), "int", {"unit": "£"},
                   ["The hundreds digit is %d." % ((n // 100) % 10),
                    "£%s rounds to £%s." % (_c(n), _c(_r1000(n)))])

    def t_money_charity():
        who = pick(NAMES)
        n = num()
        return _tb("%s's school raised £%s for charity. Rounded to the nearest £1,000, "
                   "how much is that?" % (who, _c(n)), _r1000(n), "int", {"unit": "£"},
                   ["£%s rounds to £%s." % (_c(n), _c(_r1000(n)))])

    def t_inverse():
        r = random.randint(2, 9) * 1000
        smallest = random.random() < 0.5
        ans = r - 500 if smallest else r + 499
        return _tb("A whole number rounds to %s when rounded to the nearest 1,000. "
                   "What is the %s number it could be?"
                   % (_c(r), "SMALLEST" if smallest else "LARGEST"), ans, "int", {},
                   ["Every number from %s to %s rounds to %s."
                    % (_c(r - 500), _c(r + 499), _c(r)),
                    "The %s is %s." % ("smallest" if smallest else "largest", _c(ans))])

    def t_odd_one_out():
        r = random.randint(2, 8) * 1000
        target = random.randint(r - 500, r + 499)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(1005, 9995)
            if _r1000(m) != r and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers rounds to %s when rounded to the nearest 1,000?   %s"
                   % (_c(r), _lst(opts)), target, "int", {},
                   ["Only %s lies between %s and %s." % (_c(target), _c(r - 500), _c(r + 499)),
                    "%s rounds to %s." % (_c(target), _c(r))])

    def t_compare_rounded():
        a, b = num(), num()
        while _r1000(a) == _r1000(b):
            b = num()
        return _tb("%s and %s are each rounded to the nearest 1,000. Which number has the "
                   "LARGER rounded value? Write that rounded value."
                   % (_c(a), _c(b)), max(_r1000(a), _r1000(b)), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r1000(a)), _c(b), _c(_r1000(b))),
                    "The larger rounded value is %s." % _c(max(_r1000(a), _r1000(b)))])

    def t_difference():
        n = num()
        ans = abs(_r1000(n) - n)
        return _tb("%s is rounded to the nearest 1,000. How much does the number change by?"
                   % _c(n), ans, "int", {},
                   ["%s rounds to %s." % (_c(n), _c(_r1000(n))),
                    "The difference is %s." % _c(ans)])

    def t_line():
        n = num()
        ans = _r1000(n)
        return _nl("Round %s to the nearest 1,000 and place your answer on the number line."
                   % _c(n), ans, 1000, 2000,
                   ["The hundreds digit is %d." % ((n // 100) % 10),
                    "%s rounds to %s." % (_c(n), _c(ans))])

    def t_io():
        ins = sorted(random.sample(range(1005, 9995), 4))
        rows = [[i, _r1000(i)] for i in ins]
        miss = random.randint(0, 3)
        return _io("Each Out number is the In number rounded to the nearest 1,000. "
                   "What goes in the empty cell?", rows, miss, rows[miss][1],
                   ["%s rounds to %s." % (_c(rows[miss][0]), _c(rows[miss][1]))],
                   rule="round to nearest 1,000")

    def t_table():
        items = random.sample(["a small car", "a caravan", "a motorbike", "a boat",
                               "a horse box", "a mini digger"], 3)
        vals = [num() for _i in range(3)]
        rows = [[items[i], "£%s" % _c(vals[i]), "£%s" % _c(_r1000(vals[i]))] for i in range(3)]
        r = random.randint(0, 2)
        return _dt("This price list shows prices rounded to the nearest £1,000. "
                   "What belongs in the empty cell? (write the rounded price)",
                   ["Item", "Price", "Nearest £1,000"], rows, _r1000(vals[r]),
                   ["£%s rounds to £%s." % (_c(vals[r]), _c(_r1000(vals[r])))],
                   missing=[r, 2])

    def t_estimate():
        a, b = num(), num()
        ra, rb = _r1000(a), _r1000(b)
        return _tb("Estimate %s + %s by rounding each number to the nearest 1,000 first." % (_c(a), _c(b)), ra + rb, "int", {},
                   ["%s rounds to %s and %s rounds to %s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "%s + %s = %s." % (_c(ra), _c(rb), _c(ra + rb))])

    def t_distance():
        n = num()
        place = pick(["Rome", "Madrid", "Berlin", "Athens", "Lisbon"])
        return _tb("A plane flies %s km to %s. About how far is that, to the nearest 1,000 km?" % (_c(n), place), _r1000(n), "int",
                   {"unit": "km"}, ["The hundreds digit is %d." % ((n // 100) % 10), "%s km rounds to %s km." % (_c(n), _c(_r1000(n)))])

    def t_how_many_round():
        r = random.randint(2, 8) * 1000
        vals = random.sample(range(r - 900, r + 900), 5)
        k = sum(1 for v in vals if _r1000(v) == r)
        return _tb("How many of these numbers round to %s when rounded to the nearest 1,000?   %s" % (_c(r), _lst(vals)), k,
                   "int", {}, ["Numbers from %s to %s round to %s." % (_c(r - 500), _c(r + 499), _c(r)), "%d of them do." % k])

    return _pick_t([t_bare, t_word, t_money_car, t_money_charity, t_inverse, t_odd_one_out,
                    t_compare_rounded, t_difference, t_estimate, t_distance, t_how_many_round], [t_line, t_io, t_table])


@skill("Y4.1.d", "Estimate sums and differences", S1)
def _(d=1):
    d = _d(d)
    unit = 100 if d == 0 else pick([100, 1000])

    def pair(u):
        if u == 100:
            return random.randint(111, 889), random.randint(111, 889)
        return random.randint(1050, 4950), random.randint(1050, 4950)

    def t_add():
        a, b = pair(unit)
        ra, rb = _r(a, unit), _r(b, unit)
        return _tb("Estimate %s + %s by rounding each number to the nearest %s."
                   % (_c(a), _c(b), _c(unit)), ra + rb, "int", {},
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "%s + %s = %s." % (_c(ra), _c(rb), _c(ra + rb))])

    def t_sub():
        a, b = pair(unit)
        while _r(a, unit) == _r(b, unit):
            a, b = pair(unit)
        if a < b:
            a, b = b, a
        ra, rb = _r(a, unit), _r(b, unit)
        return _tb("Estimate %s − %s by rounding each number to the nearest %s."
                   % (_c(a), _c(b), _c(unit)), ra - rb, "int", {},
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "%s − %s = %s." % (_c(ra), _c(rb), _c(ra - rb))])

    def t_word_add():
        a, b = pair(unit)
        n1, n2 = random.sample(NAMES, 2)
        thing = pick(["stamps", "beads", "air miles", "points"])
        ra, rb = _r(a, unit), _r(b, unit)
        return _tb("%s has %s %s and %s has %s %s. Estimate the total by rounding each "
                   "number to the nearest %s."
                   % (n1, _c(a), thing, n2, _c(b), thing, _c(unit)), ra + rb, "int",
                   {"unit": thing},
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "About %s altogether." % _c(ra + rb)])

    def t_word_sub():
        a, b = pair(unit)
        while _r(a, unit) == _r(b, unit):
            a, b = pair(unit)
        if a < b:
            a, b = b, a
        ra, rb = _r(a, unit), _r(b, unit)
        return _tb("A stadium holds %s people and %s tickets have been sold. Estimate how "
                   "many seats are still free by rounding each number to the nearest %s."
                   % (_c(a), _c(b), _c(unit)), ra - rb, "int", {"unit": "seats"},
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "About %s seats are free." % _c(ra - rb)])

    def t_three():
        u = 100
        a, b, cc = (random.randint(111, 889) for _i in range(3))
        ra, rb, rc = _r(a, u), _r(b, u), _r(cc, u)
        return _tb("Estimate %s + %s + %s by rounding each number to the nearest 100."
                   % (_c(a), _c(b), _c(cc)), ra + rb + rc, "int", {},
                   ["%s ≈ %s, %s ≈ %s, %s ≈ %s."
                    % (_c(a), _c(ra), _c(b), _c(rb), _c(cc), _c(rc)),
                    "%s + %s + %s = %s." % (_c(ra), _c(rb), _c(rc), _c(ra + rb + rc))])

    def t_money():
        a = random.randint(111, 889)
        b = random.randint(111, 889)
        ra, rb = _r100(a), _r100(b)
        return _tb("A bike costs £%s and a scooter costs £%s. Estimate the total cost by "
                   "rounding each price to the nearest £100." % (_c(a), _c(b)),
                   ra + rb, "int", {"unit": "£"},
                   ["£%s ≈ £%s and £%s ≈ £%s." % (_c(a), _c(ra), _c(b), _c(rb)),
                    "About £%s altogether." % _c(ra + rb)])

    def t_how_far():
        a, b = pair(100)
        est = _r100(a) + _r100(b)
        exact = a + b
        return _tb("%s + %s is estimated by rounding each number to the nearest 100. "
                   "How far is the estimate from the exact answer?" % (_c(a), _c(b)),
                   abs(est - exact), "int", {},
                   ["The estimate is %s and the exact answer is %s." % (_c(est), _c(exact)),
                    "The difference is %s." % _c(abs(est - exact))])

    def t_check():
        a, b = pair(100)
        exact = a + b
        est = _r100(a) + _r100(b)
        return _tb("%s says that %s + %s is about %s. What is the exact answer?"
                   % (pick(NAMES), _c(a), _c(b), _c(est)), exact, "int", {},
                   ["%s + %s = %s." % (_c(a), _c(b), _c(exact))])

    def t_line():
        a, b = pair(100)
        ans = _r100(a) + _r100(b)
        return _nl("Estimate %s + %s by rounding each number to the nearest 100, then place "
                   "your estimate on the number line." % (_c(a), _c(b)), ans, 100, 500,
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(_r100(a)), _c(b), _c(_r100(b))),
                    "The estimate is %s." % _c(ans)])

    def t_table():
        items = random.sample(["a tent", "a rucksack", "a sleeping bag", "a stove",
                               "a torch", "a map"], 3)
        vals = [random.randint(111, 889) for _i in range(3)]
        rows = [[items[i], "£%s" % _c(vals[i])] for i in range(3)]
        ans = sum(_r100(v) for v in vals)
        return _dt("Estimate the total cost of all three items by rounding each price to the "
                   "nearest £100.", ["Item", "Price"], rows, ans,
                   ["%s." % ", ".join("£%s ≈ £%s" % (_c(v), _c(_r100(v))) for v in vals),
                    "About £%s altogether." % _c(ans)])

    def t_table_diff():
        towns = random.sample(["Ashby", "Redhill", "Newport", "Stanton"], 2)
        vals = random.sample(range(1050, 8950), 2)
        while _r1000(vals[0]) == _r1000(vals[1]):
            vals = random.sample(range(1050, 8950), 2)
        vals.sort(reverse=True)
        rows = [[towns[i], _c(vals[i])] for i in range(2)]
        ans = _r1000(vals[0]) - _r1000(vals[1])
        return _dt("These are the populations of two villages. Estimate how many more people "
                   "live in %s than in %s by rounding each population to the nearest 1,000."
                   % (towns[0], towns[1]),
                   ["Village", "People"], rows, ans,
                   ["%s ≈ %s and %s ≈ %s."
                    % (_c(vals[0]), _c(_r1000(vals[0])), _c(vals[1]), _c(_r1000(vals[1]))),
                    "%s − %s = %s." % (_c(_r1000(vals[0])), _c(_r1000(vals[1])), _c(ans))])

    return _pick_t([t_add, t_sub, t_word_add, t_word_sub, t_three, t_money, t_how_far,
                    t_check], [t_line, t_table, t_table_diff])


@skill("Y4.1.e", "Estimate products and quotients", S1)
def _(d=1):
    d = _d(d)

    def _v(lo=3, hi=9):
        """The one-digit multiplier/divisor: 2-5 when easy, the 6-9 tables at stretch."""
        if d == 0:
            return random.randint(2, min(hi, 5))
        return random.randint(max(lo, 6) if d == 2 else lo, hi)

    def _off(opts):
        """How far the real number sits from the round one: right next to it when easy,
        the far end (nearer the halfway point) at stretch."""
        if d == 1:
            return pick(opts)
        mags = sorted({abs(o) for o in opts})
        keep = mags[:max(1, len(mags) // 2)] if d == 0 else mags[len(mags) // 2:]
        return pick([o for o in opts if abs(o) in keep])

    def _tens():
        """The round number in a 'nearest 10' estimate: 3-digit at stretch (347 × 6)."""
        return random.randint(11, 49) * 10 if d == 2 else random.randint(2, 9) * 10

    def t_product_10():
        v = _v()
        b = _tens()
        n = b + _off([-4, -3, -2, -1, 1, 2, 3, 4])
        return _tb("Estimate %d × %s by rounding %s to the nearest 10." % (v, _c(n), _c(n)),
                   v * b, "int", {},
                   ["%s ≈ %s." % (_c(n), _c(b)),
                    "%d × %s = %s." % (v, _c(b), _c(v * b))])

    def t_product_100():
        v = _v(2, 6) if d < 2 else random.randint(6, 9)
        b = random.randint(2, 9) * 100
        n = b + _off([-40, -30, -20, 20, 30, 40])
        return _tb("Estimate %d × %s by rounding %s to the nearest 100." % (v, _c(n), _c(n)),
                   v * b, "int", {},
                   ["%s ≈ %s." % (_c(n), _c(b)),
                    "%d × %s = %s." % (v, _c(b), _c(v * b))])

    def t_word_product():
        v = _v()
        b = _tens()
        n = b + _off([-3, -2, -1, 1, 2, 3])
        who = pick(NAMES)
        thing = pick(["stickers", "beads", "marbles", "seeds"])
        return _tb("%s buys %d packets of %s. Each packet holds %s %s. Estimate how many %s "
                   "%s has by rounding %s to the nearest 10."
                   % (who, v, thing, _c(n), thing, thing, who, _c(n)), v * b, "int",
                   {"unit": thing},
                   ["%s ≈ %s." % (_c(n), _c(b)),
                    "%d × %s = %s." % (v, _c(b), _c(v * b))])

    def t_quotient_compat():
        v = _v(4, 9) if d < 2 else random.randint(6, 9)
        q = random.randint(2, 9) * 10 if d < 2 else random.randint(11, 99) * 10
        exact = v * q
        n = exact + (pick([-1, 1]) if v == 4 else _off([-2, -1, 1, 2]))   # 2 off with v=4 is a tie
        return _tb("Estimate %s ÷ %d. Use the number closest to %s that divides exactly by %d."
                   % (_c(n), v, _c(n), v), q, "int", {},
                   ["%s is the closest number to %s that divides exactly by %d."
                    % (_c(exact), _c(n), v),
                    "%s ÷ %d = %d." % (_c(exact), v, q)])

    def t_quotient_100():
        if d == 2:                           # 4-digit, nearest 1,000 / 100 still divides evenly
            v = pick([2, 4, 5])
            b = random.randint(2, 9) * 1000
            n = b + pick([-300, -200, -100, 100, 200, 300])
            return _tb("Estimate %s ÷ %d by rounding %s to the nearest 1,000." % (_c(n), v, _c(n)),
                       b // v, "int", {},
                       ["%s ≈ %s." % (_c(n), _c(b)),
                        "%s ÷ %d = %s." % (_c(b), v, _c(b // v))])
        v = 2 if d == 0 else pick([2, 4, 5])
        b = random.randint(2, 9) * 100
        n = b + _off([-30, -20, -10, 10, 20, 30])
        return _tb("Estimate %s ÷ %d by rounding %s to the nearest 100." % (_c(n), v, _c(n)),
                   b // v, "int", {},
                   ["%s ≈ %s." % (_c(n), _c(b)),
                    "%s ÷ %d = %d." % (_c(b), v, b // v)])

    def t_word_quotient():
        v = _v(4, 9) if d < 2 else random.randint(6, 9)
        q = random.randint(2, 9) * 10 if d < 2 else random.randint(11, 99) * 10
        n = v * q + (pick([-1, 1]) if v == 4 else _off([-2, -1, 1, 2]))   # 2 off with v=4 is a tie
        who = pick(NAMES)
        return _tb("%s shares %s marbles equally between %d friends. Estimate how many "
                   "marbles each friend gets. Use the number closest to %s that divides "
                   "exactly by %d." % (who, _c(n), v, _c(n), v), q, "int", {"unit": "marbles"},
                   ["%s ÷ %d = %d." % (_c(v * q), v, q)])

    def t_buses():
        per = 50 if d == 0 else pick([40, 50])
        buses = random.randint(3, 6) if d == 0 else random.randint(3 if d == 1 else 6, 9)
        # stretch: often just past the previous full coach, the "one more coach" trap
        n = per * buses - random.randint(1, {0: 9, 1: 20, 2: per - 1}[d])
        return _tb("A school has %s pupils. Each coach carries %d pupils. Estimate how many "
                   "coaches are needed by rounding %s up to the nearest %d."
                   % (_c(n), per, _c(n), per), buses, "int", {"unit": "coaches"},
                   ["%s rounds up to %s." % (_c(n), _c(per * buses)),
                    "%s ÷ %d = %d coaches." % (_c(per * buses), per, buses)])

    def t_closest():
        v = _v()
        b = random.randint(2, 9) * 10
        n = b + pick([-3, -2, 2, 3])
        exact = v * b
        opts = {exact, exact * 10, max(1, exact // 10)}
        if d == 2:                           # near-miss options: one ten too many / too few
            opts |= {v * (b - 10), v * (b + 10)}
        opts = sorted(opts)
        return _tb("About how much is %d × %d? Choose the closest estimate:   %s"
                   % (v, n, _lst(opts)), exact, "int", {},
                   ["%d ≈ %d, and %d × %d = %s." % (n, b, v, b, _c(exact)),
                    "The closest estimate is %s." % _c(exact)])

    def t_inequality_true():
        v = _v()
        b = random.randint(3, 9) * 10
        n = b + _off([-3, -2, -1, 1, 2, 3])
        exact = v * n
        # the gap always beats the rounding error (at most 9 × 3 = 27), so the estimate decides it
        gap = pick({0: [100, 150], 1: [50, 100, 150], 2: [40, 50]}[d])
        down = (v * b - gap) >= 40 and random.random() < 0.5
        target = v * b - gap if down else v * b + gap
        ans = "true" if exact > target else "false"
        return _wq("Use estimation to solve this inequality. Is it true or false?   "
                   "%d × %d > %s   (type 'true' or 'false')" % (v, n, _c(target)), ans,
                   ["%d is about %d, and %d × %d = %s." % (n, b, v, b, _c(v * b)),
                    "%s is %s than %s, so the inequality is %s."
                    % (_c(v * b), "greater" if exact > target else "less", _c(target), ans)],
                   "true / false")

    def t_inequality_smallest():
        v = random.randint(2, 5) if d == 0 else random.randint(3 if d == 1 else 6, 9)
        b = random.randint(2, 9) * 10
        # stretch: the target is not itself a multiple of v
        target = v * b + (random.randint(1, v - 1) if d == 2 else 0)
        ans = b + 1
        if target == v * b:
            why = "%d × %s = %s, which is not greater than %s." % (v, _c(b), _c(target), _c(target))
        else:
            why = "%d × %s = %s, which is still less than %s." % (v, _c(b), _c(v * b), _c(target))
        return _tb("Solve this inequality using estimation:   %d × ___ > %s   "
                   "What is the smallest whole number that can go in the gap to make the "
                   "inequality true?" % (v, _c(target)), ans, "int", {},
                   [why,
                    "One more lot of %d is needed, so the smallest whole number is %s."
                    % (v, _c(ans))])

    def t_two_products():
        # stretch only: an extra step, two estimates added together
        v1, v2 = random.randint(3, 9), random.randint(3, 9)
        b1, b2 = random.randint(2, 9) * 10, random.randint(2, 9) * 10
        n1, n2 = b1 + pick([-3, -2, -1, 1, 2, 3]), b2 + pick([-3, -2, -1, 1, 2, 3])
        ans = v1 * b1 + v2 * b2
        return _tb("Estimate %d × %d + %d × %d by rounding each two-digit number to the "
                   "nearest 10." % (v1, n1, v2, n2), ans, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (n1, b1, n2, b2),
                    "%d × %d = %s and %d × %d = %s." % (v1, b1, _c(v1 * b1), v2, b2, _c(v2 * b2)),
                    "%s + %s = %s." % (_c(v1 * b1), _c(v2 * b2), _c(ans))])

    def t_line():
        v = _v()
        b = random.randint(2, 6) * 10
        n = b + _off([-3, -2, 2, 3])
        ans = v * b
        return _nl("Estimate %d × %d by rounding %d to the nearest 10, then place your "
                   "estimate on the number line." % (v, n, n), ans, 10, 100,
                   ["%d ≈ %d." % (n, b), "%d × %d = %d." % (v, b, ans)])

    def t_table():
        items = random.sample(["pencils", "rubbers", "rulers", "glue sticks"], 2)
        per = [random.randint(2, 9) * 10 + _off([-2, -1, 1, 2]) for _i in range(2)]
        packs = [{0: random.randint(2, 5), 1: random.randint(3, 8), 2: random.randint(6, 9)}[d]
                 for _i in range(2)]
        rows = [[items[i], str(packs[i]), str(per[i])] for i in range(2)]
        r = random.randint(0, 1)
        b = _r10(per[r])
        ans = packs[r] * b
        return _dt("Estimate how many %s there are altogether by rounding the number in "
                   "each pack to the nearest 10." % items[r],
                   ["Item", "Packs", "In each pack"], rows, ans,
                   ["%d ≈ %d." % (per[r], b),
                    "%d × %d = %s." % (packs[r], b, _c(ans))])

    def t_build():
        v = random.randint(2, 4)
        b = random.randint(3, 9) * 10 if d < 2 else random.randint(11, 24) * 10
        if v * b > 999:
            v = 999 // b
        n = b + _off([-2, -1, 1, 2])
        ans = v * b
        return _bt("Estimate %d × %s by rounding %s to the nearest 10, then build your "
                   "estimate with the blocks." % (v, _c(n), _c(n)), ans,
                   ["%s ≈ %s." % (_c(n), _c(b)), "%d × %s = %d." % (v, _c(b), ans)])

    plain = [t_product_10, t_product_100, t_word_product, t_quotient_compat,
             t_quotient_100, t_word_quotient, t_buses, t_closest,
             t_inequality_true, t_inequality_smallest]
    if d == 2:
        plain.append(t_two_products)
    return _pick_t(plain, [t_line, t_table, t_build])


@skill("Y4.1.f", "Number sequences and rules", S1)
def _(d=1):
    d = _d(d)
    steps = {0: [2, 3, 5, 10], 1: [6, 7, 9, 25, 50], 2: [6, 7, 9, 25, 100, 1000]}[d]
    step = pick(steps)
    start = random.randint(2, 4 if step >= 1000 else 9) * step + \
        (0 if d == 0 else pick([0, 0, random.randint(1, 9)]))
    terms = [start + i * step for i in range(6)]

    def t_next():
        ts = terms[:4]
        ans = ts[-1] + step
        return _tb("What is the next number in this sequence?   %s, ___" % _lst(ts),
                   ans, "int", {},
                   ["The sequence goes up in %ss." % _c(step),
                    "%s + %s = %s." % (_c(ts[-1]), _c(step), _c(ans))])

    def t_next_two():
        ts = [start + i * step for i in range(4)]
        if ts[-1] + 2 * step > 999:
            ts = [i * pick([2, 3, 5]) + 4 for i in range(4)]
            st = ts[1] - ts[0]
        else:
            st = step
        nxt = [ts[-1] + st, ts[-1] + 2 * st]
        return _tb("Continue the sequence — write the next two numbers:  %s, ___, ___"
                   % ", ".join(str(t) for t in ts),
                   "%d, %d" % (nxt[0], nxt[1]), "str",
                   {"text": True, "placeholder": "e.g. %d, %d" % (nxt[0], nxt[1] - 1)},
                   ["The rule is add %d each time." % st,
                    "The next two are %d and %d." % (nxt[0], nxt[1])])

    def t_back():
        big = start + 5 * step
        ts = [big - i * step for i in range(4)]
        ans = ts[-1] - step
        return _tb("This sequence counts backwards. What is the next number?   %s, ___"
                   % _lst(ts), ans, "int", {},
                   ["The rule is subtract %s each time." % _c(step),
                    "%s − %s = %s." % (_c(ts[-1]), _c(step), _c(ans))])

    def t_missing():
        idx = random.randint(1, 4)
        shown = ", ".join("___" if i == idx else _c(t) for i, t in enumerate(terms[:5]))
        return _tb("Find the missing number:  %s" % shown, terms[idx], "int", {},
                   ["The sequence goes up in %ss." % _c(step),
                    "%s + %s = %s." % (_c(terms[idx - 1]), _c(step), _c(terms[idx]))])

    def t_first():
        shown = ", ".join(["___"] + [_c(t) for t in terms[1:5]])
        return _tb("Find the missing FIRST number:  %s" % shown, terms[0], "int", {},
                   ["Count back %s from %s." % (_c(step), _c(terms[1])),
                    "%s − %s = %s." % (_c(terms[1]), _c(step), _c(terms[0]))])

    def t_rule_size():
        back = random.random() < 0.4
        ts = [terms[3] - i * step for i in range(4)] if back else terms[:4]
        return _tb("These numbers follow a rule:  %s. How much does the sequence change by "
                   "each time? (write the size of the step)" % _lst(ts), step, "int", {},
                   ["%s %s %s = %s." % (_c(ts[0]), "−" if back else "+", _c(step), _c(ts[1])),
                    "The step is %s." % _c(step)])

    def t_rule_direction():
        back = random.random() < 0.5
        ts = [terms[3] - i * step for i in range(4)] if back else terms[:4]
        ans = "down" if back else "up"
        return _wq("Look at this sequence:  %s. Does it go up or down? (type 'up' or 'down')"
                   % _lst(ts), ans,
                   ["Each number is %s %s than the one before."
                    % (_c(step), "less" if back else "more"),
                    "The sequence goes %s." % ans], "up / down")

    def t_nth():
        k = random.randint(5, 12)
        st = pick([6, 7, 9, 25])
        ans = k * st
        return _tb("A sequence starts at %d and goes up in %ds: %d, %d, %d, ... "
                   "What is the %s number in the sequence?"
                   % (st, st, st, 2 * st, 3 * st, ordinal(k)), ans, "int", {},
                   ["The %s number is %d × %d." % (ordinal(k), k, st),
                    "%d × %d = %s." % (k, st, _c(ans))])

    def t_word():
        who = pick(NAMES)
        st = pick([6, 7, 9, 25])
        first = st * random.randint(2, 5)
        k = random.randint(5, 9)
        return _tb("%s starts with £%d in a money box and adds £%d every week. How much is "
                   "in the money box after %d weeks?" % (who, first, st, k),
                   first + k * st, "int", {"unit": "£"},
                   ["%s adds £%d, %d times." % (who, st, k),
                    "%d × %d = %d, and %d + %d = %d."
                    % (k, st, k * st, first, k * st, first + k * st)])

    def t_double():
        first = pick([2, 3, 4, 5])
        ts = [first * (2 ** i) for i in range(4)]
        ans = ts[-1] * 2
        return _tb("Look at the rule in this sequence:  %s, ___  What is the next number?"
                   % _lst(ts), ans, "int", {},
                   ["Each number is double the one before.",
                    "%d × 2 = %d." % (ts[-1], ans)])

    def t_io():
        a = pick([6, 7, 9, 25, 100])
        ins = sorted(random.sample(range(2, 40), 4))
        rows = [[i, i * a] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What goes in the empty cell?",
                   rows, miss, rows[miss][1],
                   ["The rule is multiply by %d." % a,
                    "%d × %d = %s." % (rows[miss][0], a, _c(rows[miss][1]))],
                   rule="× %d" % a)

    def t_io_rule():
        a = pick([6, 7, 9, 25])
        ins = sorted(random.sample(range(2, 30), 4))
        rows = [[i, i * a] for i in ins]
        return _io("Every Out number is made from the In number by the same rule. "
                   "What number is the In number multiplied by?", rows, None, a,
                   ["%d × %d = %d." % (ins[0], a, ins[0] * a),
                    "The rule is multiply by %d." % a])

    def t_line():
        st = pick([25, 50, 100])
        s = random.randint(2, 8) * st
        ts = [s + i * st for i in range(4)]
        ans = ts[-1] + st
        major = {25: 100, 50: 200, 100: 500}[st]
        return _nl("Continue the sequence %s, ... and place the NEXT number on the number line."
                   % _lst(ts), ans, st, major,
                   ["The sequence goes up in %ds." % st,
                    "%s + %d = %s." % (_c(ts[-1]), st, _c(ans))])

    def t_table():
        st = pick([6, 7, 9, 25])
        s = st * random.randint(2, 6)
        vals = [s + i * st for i in range(5)]
        r = random.randint(0, 4)
        return _dt("This table shows a number sequence. What number belongs in the empty cell?",
                   ["Position", "1", "2", "3", "4", "5"],
                   [["Number"] + [_c(v) for v in vals]], vals[r],
                   ["The sequence goes up in %ds." % st,
                    "The %s number is %s." % (ordinal(r + 1), _c(vals[r]))],
                   missing=[0, r + 1])

    return _pick_t([t_next, t_next_two, t_back, t_missing, t_first, t_rule_size,
                    t_rule_direction, t_nth, t_word, t_double],
                   [t_io, t_io_rule, t_line, t_table])


def _best(digs, big, ok=None):
    """Largest/smallest number using each digit once (no leading zero), optionally filtered."""
    from itertools import permutations
    ns = [int("".join(map(str, p))) for p in permutations(digs) if p[0] != 0]
    ns = [m for m in ns if ok is None or ok(m)]
    return max(ns) if big else min(ns)


@skill("Y4.1.g", "Number puzzles and logical reasoning", S1)
def _(d=1):
    d = _d(d)

    def t_digit_clues():
        if d == 2:                           # 3-digit: one more clue to juggle
            h = random.randint(1, 9)
            t, o = random.sample(range(0, 10), 2)
            n = h * 100 + t * 10 + o
            rel = ("its tens digit is %d more than its ones digit" % (t - o) if t > o else
                   "its ones digit is %d more than its tens digit" % (o - t))
            return _tb("Guess the number: it is a 3-digit number with %s. Its digits "
                       "add up to %d and %s. What is the number?" % (_pl(h, "hundred"), h + t + o, rel),
                       n, "int", {},
                       ["The tens and ones digits add up to %d − %d = %d." % (h + t + o, h, t + o),
                        "They are %d and %d, so the number is %d." % (t, o, n)])
        t, o = random.sample(range(1, 6 if d == 0 else 10), 2)
        n = t * 10 + o
        return _tb("Guess the number: it is a 2-digit number. Its digits add up to %d and "
                   "its tens digit is %d more than its ones digit. What is the number?"
                   % (t + o, t - o) if t > o else
                   "Guess the number: it is a 2-digit number. Its digits add up to %d and "
                   "its ones digit is %d more than its tens digit. What is the number?"
                   % (t + o, o - t), n, "int", {},
                   ["The two digits are %d and %d." % (t, o),
                    "The number is %d." % n])

    def t_largest_from_digits():
        k = 4 if d >= 1 else 3
        digs = random.sample(range(1, 10), k)
        if d == 2:                           # a zero cannot go first
            digs[random.randrange(k)] = 0
        big = random.random() < 0.5
        ans = _best(digs, big)
        return _tb("Use each of the digits %s once. What is the %s number you can make?"
                   % (", ".join(str(x) for x in digs), "LARGEST" if big else "SMALLEST"),
                   ans, "int", {},
                   ["Put the %s digit first%s." % ("largest" if big else "smallest",
                                                  "" if big or 0 not in digs else
                                                  " (not 0: it cannot start a number)"),
                    "The answer is %s." % _c(ans)])

    def t_largest_even():
        if d == 2:                           # the SMALLEST even number is a harder search
            digs = random.sample(range(1, 10), 4)
            if all(x % 2 for x in digs):
                digs[0] = pick([2, 4, 6, 8])
            ans = _best(digs, False, lambda m: m % 2 == 0)
            return _tb("Use each of the digits %s once. What is the smallest EVEN number you "
                       "can make?" % ", ".join(str(x) for x in digs), ans, "int", {},
                       ["An even number must end in an even digit.",
                        "Keep the smallest digits at the front: the answer is %s." % _c(ans)])
        digs = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4 if d else 3)
        evens = [x for x in digs if x % 2 == 0]
        if not evens:
            digs[0] = pick([2, 4, 6, 8])
            digs = list(dict.fromkeys(digs))
            while len(digs) < (4 if d else 3):
                m = random.randint(1, 9)
                if m not in digs:
                    digs.append(m)
            evens = [x for x in digs if x % 2 == 0]
        last = min(evens)
        rest = sorted([x for x in digs if x != last], reverse=True)
        ans = int("".join(str(x) for x in rest + [last]))
        return _tb("Use each of the digits %s once. What is the largest EVEN number you can "
                   "make?" % ", ".join(str(x) for x in digs), ans, "int", {},
                   ["An even number ends in an even digit, so use the smallest even digit "
                    "(%d) at the end." % last,
                    "The answer is %s." % _c(ans)])

    def t_sum_and_diff():
        small = random.randint(*{0: (3, 15), 1: (5, 40), 2: (25, 150)}[d])
        gap = random.randint(*{0: (2, 10), 1: (2, 20), 2: (10, 60)}[d])
        big = small + gap
        want_big = random.random() < 0.5
        return _tb("Two numbers add up to %d. The difference between the two numbers is %d. "
                   "What is the %s number?" % (small + big, gap,
                                               "LARGER" if want_big else "SMALLER"),
                   big if want_big else small, "int", {},
                   ["%d + %d = %d and %d − %d = %d."
                    % (big, small, big + small, big, small, gap),
                    "The %s number is %d." % ("larger" if want_big else "smaller",
                                              big if want_big else small)])

    def t_product_and_sum():
        a, b = random.sample({0: range(2, 7), 1: range(2, 13), 2: range(6, 13)}[d], 2)
        want_big = random.random() < 0.5
        return _tb("Two whole numbers multiply to make %d and add up to %d. "
                   "What is the %s number?" % (a * b, a + b,
                                               "LARGER" if want_big else "SMALLER"),
                   max(a, b) if want_big else min(a, b), "int", {},
                   ["%d × %d = %d and %d + %d = %d." % (a, b, a * b, a, b, a + b),
                    "The %s number is %d." % ("larger" if want_big else "smaller",
                                              max(a, b) if want_big else min(a, b))])

    def t_find_two_sum_diff():
        small = random.randint(*{0: (3, 15), 1: (3, 40), 2: (25, 150)}[d])
        gap = random.randint(*{0: (2, 10), 1: (2, 20), 2: (10, 60)}[d])
        big = small + gap
        want_big = random.random() < 0.5
        return _tb("Find two numbers with a sum of %d and a difference of %d. "
                   "What is the %s number?"
                   % (small + big, gap, "LARGER" if want_big else "SMALLER"),
                   big if want_big else small, "int", {},
                   ["Take the difference away from the sum: %d − %d = %d, and half of that "
                    "is %d." % (small + big, gap, 2 * small, small),
                    "The two numbers are %d and %d." % (small, big)])

    def t_find_two_product_quotient():
        b = random.randint(2, {0: 5, 1: 8, 2: 12}[d])
        q = random.randint(2, {0: 4, 1: 6, 2: 9}[d])
        a = q * b
        want_big = random.random() < 0.5
        return _tb("Find two numbers with a product of %s and a quotient of %d. "
                   "What is the %s number?"
                   % (_c(a * b), q, "LARGER" if want_big else "SMALLER"),
                   a if want_big else b, "int", {},
                   ["%d × %d = %s and %d ÷ %d = %d." % (a, b, _c(a * b), a, b, q),
                    "The two numbers are %d and %d." % (b, a)])

    def t_find_two_all_clues():
        b = random.randint(2, {0: 5, 1: 9, 2: 12}[d])
        q = random.randint(2, {0: 3, 1: 5, 2: 8}[d])
        a = q * b
        want_big = random.random() < 0.5
        return _tb("Find two numbers from these clues: the sum of the two numbers is %d, "
                   "their difference is %d, their product is %s and their quotient is %d. "
                   "What is the %s number?"
                   % (a + b, a - b, _c(a * b), q, "LARGER" if want_big else "SMALLER"),
                   a if want_big else b, "int", {},
                   ["The quotient is %d, so the larger number is %d times the smaller one."
                    % (q, q),
                    "%d and %d fit every clue." % (b, a)])

    def t_consecutive():
        if d == 2:                           # four in a row: no single middle number
            first = random.randint(10, 80)
            total = 4 * first + 6
            want = pick(["smallest", "largest"])
            ans = first if want == "smallest" else first + 3
            return _tb("Four numbers that follow one after the other (like 7, 8, 9, 10) add up "
                       "to %d. What is the %s number?" % (total, want.upper()), ans, "int", {},
                       ["The others are 1, 2 and 3 more than the smallest: %d − 6 = %d."
                        % (total, total - 6),
                        "%d ÷ 4 = %d, so the numbers are %d, %d, %d and %d."
                        % (total - 6, first, first, first + 1, first + 2, first + 3)])
        mid = random.randint(3, 20) if d == 0 else random.randint(5, 60)
        total = 3 * mid
        want = pick(["smallest", "middle", "largest"])
        ans = {"smallest": mid - 1, "middle": mid, "largest": mid + 1}[want]
        return _tb("Three numbers that follow one after the other (like 7, 8, 9) add up to %d. "
                   "What is the %s number?" % (total, want.upper()), ans, "int", {},
                   ["%d ÷ 3 = %d, so the middle number is %d." % (total, mid, mid),
                    "The three numbers are %d, %d and %d." % (mid - 1, mid, mid + 1)])

    def t_think_of_number():
        who = pick(NAMES)
        start = random.randint(*{0: (2, 10), 1: (3, 12), 2: (6, 25)}[d])
        mult = random.randint(*{0: (2, 3), 1: (2, 5), 2: (3, 9)}[d])
        add = random.randint(*{0: (1, 10), 1: (3, 20), 2: (10, 50)}[d])
        end = start * mult + add
        return _tb("%s thinks of a number, multiplies it by %d and then adds %d. "
                   "The answer is %d. What number did %s think of?"
                   % (who, mult, add, end, who),
                   start, "int", {},
                   ["Work backwards: %d − %d = %d." % (end, add, end - add),
                    "%d ÷ %d = %d." % (end - add, mult, start)])

    def t_think_of_number2():
        who = pick(NAMES)
        start = random.randint(10, 30) if d == 0 else random.randint(20, 90)
        sub = random.randint(1, 9) if d == 0 else random.randint(5, 15)
        k = 3 if d == 2 else 2               # stretch: trebles instead of doubles
        end = (start - sub) * k
        return _tb("%s thinks of a number, subtracts %d and then %s the result. "
                   "The answer is %d. What number did %s think of?"
                   % (who, sub, "trebles" if k == 3 else "doubles", end, who),
                   start, "int", {},
                   ["Work backwards: %d ÷ %d = %d." % (end, k, end // k),
                    "%d + %d = %d." % (end // k, sub, start)])

    def t_rounding_puzzle():
        unit = {0: 10, 1: 100, 2: 1000}[d]
        r = random.randint(2, 9) * (100 if d < 2 else 1000) + (random.randint(1, 9) * 10 if d == 0 else 0)
        big = random.random() < 0.5
        ans = r + unit // 2 - 1 if big else r - unit // 2
        return _tb("What is the %s whole number that rounds to %s when rounded to the "
                   "nearest %s?" % ("LARGEST" if big else "SMALLEST", _c(r), _c(unit)), ans, "int", {},
                   ["Numbers from %s to %s round to %s." % (_c(r - unit // 2), _c(r + unit // 2 - 1), _c(r)),
                    "The %s is %s." % ("largest" if big else "smallest", _c(ans))])

    def t_multiple_clues():
        """Brute-forced so the clues have exactly one answer."""
        for _try in range(60):
            lo = random.randint(*{0: (20, 100), 1: (20, 400), 2: (400, 950)}[d])
            hi = lo + random.randint(*{0: (20, 40), 1: (20, 60), 2: (60, 120)}[d])
            m = pick({0: [2, 5, 10], 1: [3, 4, 6, 7, 9, 25], 2: [6, 7, 9]}[d])
            s = random.randint(3, 18 if d < 2 else 24)
            cands = [x for x in range(lo + 1, hi)
                     if x % m == 0 and sum(int(ch) for ch in str(x)) == s]
            if len(cands) == 1:
                n = cands[0]
                return _tb("I am thinking of a number between %d and %d. It is a multiple of "
                           "%d and its digits add up to %d. What is my number?"
                           % (lo, hi, m, s), n, "int", {},
                           ["The multiples of %d between %d and %d are: %s."
                            % (m, lo, hi, ", ".join(str(x) for x in range(lo + 1, hi)
                                                    if x % m == 0)),
                            "Only %d has digits adding to %d." % (n, s)])
        return t_sum_and_diff()

    def t_coins():
        who = pick(NAMES)
        two = random.randint(*{0: (1, 5), 1: (2, 9), 2: (8, 20)}[d])
        one = random.randint(*{0: (1, 5), 1: (2, 9), 2: (8, 20)}[d])
        return _tb("%s has %d coins altogether. Every coin is either a £2 coin or a £1 coin, "
                   "and the coins are worth £%d in total. How many £2 coins does %s have?"
                   % (who, two + one, 2 * two + one, who),
                   two, "int", {"unit": "coins"},
                   ["If all %d coins were £1 coins they would be worth £%d."
                    % (two + one, two + one),
                    "Each £2 coin adds £1 more, and £%d − £%d = £%d, so there are %d £2 coins."
                    % (2 * two + one, two + one, two, two)])

    def t_ages():
        small = random.randint(3, 8) if d == 0 else random.randint(3, 12)
        k = 2 if d == 0 else random.randint(2, 4)
        who1, who2 = random.sample(NAMES, 2)
        if d == 2:                           # given the difference instead of the total
            k = random.randint(3, 6)
            return _tb("%s is %d times as old as %s. %s is %d years older than %s. "
                       "How old is %s?" % (who1, k, who2, who1, small * (k - 1), who2, who2),
                       small, "int", {"unit": "years"},
                       ["Think of %s's age as 1 part and %s's age as %d parts, so the "
                        "difference is %d parts." % (who2, who1, k, k - 1),
                        "%d ÷ %d = %d, so %s is %d." % (small * (k - 1), k - 1, small, who2, small)])
        return _tb("%s is %d times as old as %s. The two ages add up to %d years altogether. "
                   "How old is %s?" % (who1, k, who2, small * (k + 1), who2),
                   small, "int", {"unit": "years"},
                   ["Think of %s's age as 1 part and %s's age as %d parts, so %d parts "
                    "altogether." % (who2, who1, k, k + 1),
                    "%d ÷ %d = %d, so %s is %d." % (small * (k + 1), k + 1, small, who2, small)])

    def t_missing_digit():
        th = random.randint(1, 9)
        h = random.randint(0, 9)
        t = random.randint(0, 9)
        o = random.randint(0, 9)
        n = th * 1000 + h * 100 + t * 10 + o
        target = random.randint(1, 9) * 1000 + random.randint(0, 9) * 100
        if d == 0:                           # 3-digit, up to the next hundred
            n = h * 100 + t * 10 + 100 * (h == 0)
            target = (n // 100 + 1) * 100
        elif d == 2:                         # the target has tens too: no tidy complement
            target += random.randint(1, 9) * 10
        diff = target - n
        if diff <= 0:
            return t_rounding_puzzle()
        return _tb("What must be added to %s to make %s?" % (_c(n), _c(target)),
                   diff, "int", {},
                   ["%s − %s = %s." % (_c(target), _c(n), _c(diff))])

    def t_line():
        small = random.randint(*{0: (2, 10), 1: (5, 30), 2: (20, 60)}[d])
        gap = random.randint(*{0: (2, 8), 1: (2, 15), 2: (5, 30)}[d])
        big = small + gap
        return _nl("Two numbers add up to %d. The difference between the two numbers is %d. "
                   "Place the LARGER number on the number line." % (small + big, gap),
                   big, 1, 10,
                   ["Half of (%d + %d) is %d." % (small + big, gap, big),
                    "The two numbers are %d and %d." % (small, big)])

    def t_build():
        digs = random.sample(range(1, 10), 3)
        if d == 2:                           # with a zero
            digs[random.randrange(3)] = 0
        big = random.random() < 0.5
        ans = _best(digs, big)
        return _bt("Use each of the digits %s once to make the %s possible number, then "
                   "build it." % (", ".join(str(x) for x in digs),
                                  "largest" if big else "smallest"), ans,
                   ["Put the %s digit first." % ("largest" if big else "smallest"),
                    "The answer is %d." % ans])

    return _pick_t([t_digit_clues, t_largest_from_digits, t_largest_even, t_sum_and_diff,
                    t_find_two_sum_diff, t_find_two_product_quotient, t_find_two_all_clues,
                    t_product_and_sum, t_consecutive, t_think_of_number, t_think_of_number2,
                    t_rounding_puzzle, t_multiple_clues, t_coins, t_ages, t_missing_digit],
                   [t_line, t_build])


def _repeat_step(k, size, item):
    """Explain where position k lands in a pattern that repeats every `size` items."""
    full, left = divmod(k, size)
    if left == 0:
        return ("%d ÷ %d = %d exactly, so %d full repeats end at position %d: it is the "
                "LAST %s of the pattern." % (k, size, full, full, k, item))
    return ("%d ÷ %d = %d remainder %d: after %d full repeats (%d %ss), count on %d more, "
            "so it is %s %d of the pattern."
            % (k, size, full, left, full, full * size, item, left, item, left))


@skill("Y4.1.h", "Shape and growing patterns", S1)
def _(d=1):
    d = _d(d)
    # matchstick patterns: shape, sticks for the first shape, sticks added each time
    PATTERNS = [("squares", 4, 3), ("triangles", 3, 2), ("hexagons", 6, 5),
                ("pentagons", 5, 4)]
    if d == 0:                               # easy: the two familiar shapes only
        PATTERNS = PATTERNS[:2]

    def t_next_term():
        name, first, add = pick(PATTERNS)
        k = random.randint(3, 4 if d == 0 else 5)
        ahead = 2 if d == 2 else 1           # stretch: two shapes beyond the list
        counts = [first + i * add for i in range(k)]
        ans = counts[-1] + ahead * add
        return _tb("A pattern is made from matchsticks. 1 %s uses %d sticks, and each extra "
                   "%s in the row uses %d more sticks: %s. How many sticks are needed for "
                   "%d %s?" % (name[:-1], first, name[:-1], add, _lst(counts), k + ahead, name),
                   ans, "int", {"unit": "sticks"},
                   ["Each new %s adds %d sticks." % (name[:-1], add),
                    ("%d + %d = %d." % (counts[-1], add, ans)) if ahead == 1 else
                    ("%d + %d + %d = %d." % (counts[-1], add, add, ans))])

    def t_nth_term():
        name, first, add = pick(PATTERNS)
        k = random.randint(*{0: (4, 6), 1: (6, 12), 2: (15, 30)}[d])
        ans = first + (k - 1) * add
        return _tb("In a matchstick pattern, 1 %s uses %d sticks and every extra %s uses %d "
                   "more sticks. How many sticks are needed for %d %s?"
                   % (name[:-1], first, name[:-1], add, k, name), ans, "int", {"unit": "sticks"},
                   ["%d extra %s need %d × %d = %d sticks." % (k - 1, name, k - 1, add,
                                                               (k - 1) * add),
                    "%d + %d = %d." % (first, (k - 1) * add, ans)])

    def t_inverse():
        name, first, add = pick(PATTERNS)
        k = random.randint(*{0: (3, 6), 1: (4, 10), 2: (12, 25)}[d])
        total = first + (k - 1) * add
        return _tb("In a matchstick pattern, 1 %s uses %d sticks and every extra %s uses %d "
                   "more sticks. %s uses %d sticks altogether. How many %s are in the pattern?"
                   % (name[:-1], first, name[:-1], add, pick(NAMES), total, name),
                   k, "int", {"unit": name},
                   ["%d − %d = %d sticks are used by the extra %s."
                    % (total, first, total - first, name),
                    "%d ÷ %d = %d extra, so %d %s altogether."
                    % (total - first, add, k - 1, k, name)])

    def t_step_size():
        name, first, add = pick(PATTERNS)
        j = 0 if d < 2 else random.randint(5, 12)   # stretch: a later stretch of the pattern
        counts = [first + (j + i) * add for i in range(5 if d < 2 else 4)]
        return _tb("A growing pattern of %s uses these numbers of matchsticks:  %s. "
                   "How many extra sticks are added each time?" % (name, _lst(counts)),
                   add, "int", {"unit": "sticks"},
                   ["%d − %d = %d." % (counts[1], counts[0], add)])

    def t_difference():
        name, first, add = pick(PATTERNS)
        a = random.randint(*{0: (2, 4), 1: (3, 6), 2: (8, 15)}[d])
        b = a + random.randint(*{0: (1, 3), 1: (2, 5), 2: (6, 12)}[d])
        ans = (b - a) * add
        return _tb("In a matchstick pattern of %s, each extra %s uses %d more sticks. "
                   "How many more sticks are needed for %d %s than for %d %s?"
                   % (name, name[:-1], add, b, name, a, name), ans, "int", {"unit": "sticks"},
                   ["There are %d more %s." % (b - a, name),
                    "%d × %d = %d." % (b - a, add, ans)])

    def t_square_numbers():
        k = random.randint(*{0: (3, 5), 1: (3, 9), 2: (10, 12)}[d])
        ans = k * k
        return _tb("A pattern is made from dots in squares: pattern 1 has 1 dot, pattern 2 has "
                   "4 dots, pattern 3 has 9 dots, pattern 4 has 16 dots. "
                   "How many dots are in pattern %d?" % k, ans, "int", {"unit": "dots"},
                   ["Each pattern is a square of dots: %d rows of %d." % (k, k),
                    "%d × %d = %d." % (k, k, ans)])

    def t_triangle_rows():
        k = random.randint(*{0: (4, 5), 1: (4, 9), 2: (10, 12)}[d])
        ans = k * (k + 1) // 2
        return _tb("A triangle of counters is built in rows: row 1 has 1 counter, row 2 has 2, "
                   "row 3 has 3, and so on. How many counters are used altogether for %d rows?"
                   % k, ans, "int", {"unit": "counters"},
                   ["Add the rows: %s." % " + ".join(str(i) for i in range(1, k + 1)),
                    "That makes %d." % ans])

    def t_repeating_shape():
        seq = random.sample(["circle", "square", "triangle", "star", "hexagon"], 3)
        k = random.randint(*{0: (7, 15), 1: (10, 40), 2: (41, 99)}[d])
        ans = seq[(k - 1) % 3]
        return _wq("A pattern repeats these shapes over and over: %s, %s, %s, %s, %s, %s, ... "
                   "Which shape is in position %d? (type the word)"
                   % (seq[0], seq[1], seq[2], seq[0], seq[1], seq[2], k), ans,
                   ["The pattern repeats every 3 shapes.",
                    _repeat_step(k, 3, "shape"),
                    "So position %d is the %s." % (k, ans)], "a shape name")

    def t_repeating_colour():
        seq = random.sample(["red", "blue", "green", "yellow"], 4)
        k = random.randint(*{0: (9, 20), 1: (12, 50), 2: (51, 120)}[d])
        ans = seq[(k - 1) % 4]
        return _wq("Beads are threaded in a repeating pattern: %s, %s, %s, %s, %s, ... "
                   "What colour is bead number %d? (type the word)"
                   % (seq[0], seq[1], seq[2], seq[3], seq[0], k), ans,
                   ["The pattern repeats every 4 beads.",
                    _repeat_step(k, 4, "bead"),
                    "So bead number %d is %s." % (k, ans)], "a colour")

    def t_tiles():
        who = pick(NAMES)
        first = random.randint(2, 4 if d == 0 else 6)
        add = random.randint(*{0: (2, 4), 1: (2, 6), 2: (3, 9)}[d])
        k = random.randint(*{0: (4, 6), 1: (5, 10), 2: (12, 20)}[d])
        ans = first + (k - 1) * add
        return _tb("%s builds a pattern with tiles. Pattern 1 uses %d tiles and each pattern "
                   "after that uses %d more tiles than the one before. How many tiles are in "
                   "pattern %d?" % (who, first, add, k), ans, "int", {"unit": "tiles"},
                   ["Pattern %d = %d + %d × %d." % (k, first, k - 1, add),
                    "%d + %d = %d." % (first, (k - 1) * add, ans)])

    def t_io():
        name, first, add = pick(PATTERNS)
        ins = [1, 2, 3, 4] if d < 2 else [1, 2, 3, random.randint(7, 12)]   # stretch: jump ahead
        rows = [[i, first + (i - 1) * add] for i in ins]
        miss = 3 if d == 2 and random.random() < 0.6 else random.randint(0, 3)
        return _io("This table shows how many matchsticks are used to make a row of %s. "
                   "What number goes in the empty cell?" % name,
                   rows, miss, rows[miss][1],
                   ["Each extra %s adds %d sticks." % (name[:-1], add),
                    "%d %s %d sticks." % (rows[miss][0], name + " need" if rows[miss][0] != 1 else name[:-1] + " needs", rows[miss][1])],
                   rule="× %d, then + %d" % (add, first - add))

    def t_table():
        name, first, add = pick(PATTERNS)
        cols = [1, 2, 3, 4, 5] if d < 2 else [1, 2, 3, 4, random.randint(8, 15)]   # stretch: jump ahead
        vals = [first + (c - 1) * add for c in cols]
        r = 4 if d == 2 and random.random() < 0.6 else random.randint(0, 4)
        return _dt("This table shows a growing pattern of %s made from matchsticks. "
                   "What number belongs in the empty cell?" % name,
                   ["Number of %s" % name] + [str(c) for c in cols],
                   [["Matchsticks"] + [str(v) for v in vals]], vals[r],
                   ["Each extra %s adds %d sticks." % (name[:-1], add),
                    "%d %s %s %d sticks." % (cols[r], name if r else name[:-1], "need" if r else "needs", vals[r])],
                   missing=[0, r + 1])

    def t_table_repeat():
        seq = random.sample(["circle", "square", "triangle"], 3)
        cells = [seq[i % 3] for i in range(6)]
        k = random.randint(*{0: (7, 12), 1: (10, 30), 2: (31, 60)}[d])
        ans = seq[(k - 1) % 3]
        return _dt("This table shows the first six shapes of a repeating pattern. "
                   "Which shape is in position %d? (type the word)" % k,
                   ["Position", "1", "2", "3", "4", "5", "6"],
                   [["Shape"] + cells], ans,
                   ["The pattern repeats every 3 shapes.",
                    "Position %d is the %s." % (k, ans)], atype="str")

    def t_line():
        add = pick([5, 10, 25])
        first = add * random.randint(1, 2)
        k = random.randint(*{0: (2, 4), 1: (3, 6), 2: (5, 8)}[d])
        ans = first + k * add
        major = {5: 50, 10: 100, 25: 100}[add]
        return _nl("A growing pattern uses %d counters in pattern 1 and %d more counters in "
                   "each pattern after that. Place the number of counters in pattern %d on "
                   "the number line." % (first, add, k + 1), ans, add, major,
                   ["Pattern %d = %d + %d × %d = %d." % (k + 1, first, k, add, ans)])

    return _pick_t([t_next_term, t_nth_term, t_inverse, t_step_size, t_difference,
                    t_square_numbers, t_triangle_rows, t_repeating_shape, t_repeating_colour,
                    t_tiles], [t_io, t_table, t_table_repeat, t_line])
