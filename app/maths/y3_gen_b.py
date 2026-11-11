# dev/app/logic/y3_gen_b.py — Year 3 generators: levels 3.2, 3.3, 3.4, 3.5
#
# Every generator takes a difficulty `d`:
#   d = 0  easy    (smaller numbers, no regrouping / no exchange, single step)
#   d = 1  core    (year-expected)
#   d = 2  stretch (bigger numbers, missing-number and two-step framings)
#
# Each skill offers 4-6 genuinely different framings (bare calculation, word
# problem, missing number, inverse check, visual model, comparison, two-step)
# and routes a large share of them through the interactive components
# (array / base_ten / number_line / bar_chart / pictogram).
import random
from .maths_engine import skill, pick, NAMES, n_words, money

S2 = "3.2 Addition & subtraction (2-digit)"
S3 = "3.3 Addition & subtraction (3-digit)"
S4 = "3.4 Multiplication & division (facts)"
S5 = "3.5 Multiplication & division (calculating)"

_OBJ = ["stickers", "marbles", "conkers", "beads", "shells", "cards", "buttons", "acorns"]


# =============================================================== helpers =====
def _digits(n):
    return (n // 100, (n // 10) % 10, n % 10)


def _lvl(d):
    """Clamp difficulty to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _numq(prompt, answer, solution, unit=None, placeholder=None,
          answer_type="int", text=False):
    spec = {}
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _line_spec(vals):
    """A number line that certainly contains every value in `vals`, with a step
    that divides all of them (so the marker can land exactly on the answer)."""
    vals = [int(v) for v in vals]
    lo_v, hi_v = min(vals), max(vals)
    span = hi_v - lo_v
    cand = [s for s in (1, 2, 5, 10, 20, 25, 50, 100) if all(v % s == 0 for v in vals)]
    if not cand:
        cand = [1]
    step = cand[-1]
    for s in cand:
        if span // s <= 40:
            step = s
            break
    major = step * 5
    lo = max(0, lo_v - step * 2)
    lo = (lo // major) * major
    hi = hi_v + step * 2
    hi = -(-hi // major) * major
    if (hi - lo) // step < 6:
        hi = lo + major * 2
    return {"min": int(lo), "max": int(hi), "step": int(step), "major": int(major)}


def _lineq(prompt, target, others, solution):
    spec = _line_spec(list(others) + [target])
    return {"prompt": prompt, "component": "number_line", "spec": spec,
            "answer": int(target), "answer_type": "num",
            "tolerance": spec["step"] / 2.0, "solution": solution}


def _btq(prompt, answer, solution):
    """base_ten build — answer must be a 3-digit-or-less whole number."""
    answer = int(answer)
    return {"prompt": prompt, "component": "base_ten",
            "spec": {"mode": "build", "max": 9},
            "answer": answer, "answer_type": "int", "solution": solution}


def _arrayq(prompt, rows, cols, solution):
    rows, cols = int(rows), int(cols)
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "build",
                     "maxRows": min(10, max(6, rows + 2)),
                     "maxCols": min(12, max(6, cols + 2)),
                     "targetRows": rows, "targetCols": cols},
            "answer": rows * cols, "answer_type": "int", "solution": solution}


def _arrayreadq(prompt, rows, cols, answer, solution):
    """An array drawn (not built) with a typed answer: for the division skills, where the answer is the number in
    each row or the number of rows, not the total a built array gives."""
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "read", "rows": int(rows), "cols": int(cols)},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _barq(prompt, cats, vals, answer, solution):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "mode": "read"},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _pictq(prompt, cats, vals, key, symbol, answer, solution):
    return {"prompt": prompt, "component": "pictogram",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "key": int(key), "symbol": symbol},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _ioq(prompt, rows, missing, answer, solution, rule=None, placeholder=None,
         answer_type="int"):
    """input/output table. `rows` = [[in, out], ...]; `missing` = index of the row
    whose Out cell is blanked (pass None to ask for the rule itself)."""
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _io_rows(lo, hi, delta, n=4):
    """n distinct In values in [lo, hi] with Out = In + delta."""
    pool = list(range(int(lo), int(hi) + 1))
    n = min(n, len(pool))
    ins = sorted(random.sample(pool, n))
    return [[i, i + delta] for i in ins]


def _egq(prompt, groups, per, answer, solution, answer_type="int"):
    """equal_groups (read): G rings holding P counters each, plus a typed box."""
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "read", "groups": int(groups), "per": int(per)},
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _egbuildq(prompt, groups, per, solution):
    """equal_groups (build): the pupil sets groups & per; the value is the product."""
    groups, per = int(groups), int(per)
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "build", "maxGroups": 8, "maxPer": 10, "targetGroups": groups, "targetPer": per},
            "answer": groups * per, "answer_type": "int", "solution": solution}


def _stripq(prompt, spec, answer, solution):
    return {"prompt": prompt, "component": "strip_model", "spec": spec,
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _wordq(prompt, answer, solution, placeholder=None):
    """A typed *word* answer (used for sign / vocabulary questions)."""
    return _numq(prompt, answer, solution, placeholder=placeholder,
                 answer_type="str", text=True)


# --- column-method pair builders (guarantees are structural, not accidental) --
def _pair_add_no_carry(d=1):
    """Every column sum < 10, so the column method needs no regrouping."""
    d = _lvl(d)
    hcap = 5 if d == 0 else 9
    ocap = 6 if d == 0 else 9
    while True:
        hs = random.randint(2, hcap)            # hundreds digits sum
        ah = random.randint(1, hs - 1)
        bh = hs - ah
        if bh < 1:
            continue
        ts = random.randint(1, ocap)
        at = random.randint(0, ts)
        bt = ts - at
        os_ = random.randint(1, ocap)
        ao = random.randint(0, os_)
        bo = os_ - ao
        a = ah * 100 + at * 10 + ao
        b = bh * 100 + bt * 10 + bo
        if a >= 102 and b >= 102:
            return a, b


def _pair_add_carry(d=1):
    """At least one column sum >= 10, so regrouping is genuinely required."""
    d = _lvl(d)
    hi = 480 if d == 0 else (780 if d == 1 else 899)
    while True:
        a = random.randint(105, hi)
        b = random.randint(105, hi)
        ah, at, ao = _digits(a)
        bh, bt, bo = _digits(b)
        if (ao + bo >= 10 or at + bt >= 10) and a + b < 1000:
            # easy: exactly one carry (a carried ten must not make the tens 10 again)
            if d == 0 and not ((ao + bo >= 10 and at + bt <= 8) or (ao + bo < 10 and at + bt >= 10)):
                continue
            if d == 2 and not (ao + bo >= 10 and at + bt >= 9):
                continue
            return a, b


def _pair_sub_no_exchange(d=1):
    """Every top digit >= matching bottom digit, so no exchange is needed."""
    d = _lvl(d)
    lo, hi = (300, 699) if d == 0 else (300, 989)
    while True:
        a = random.randint(lo, hi)
        b = random.randint(102, a - 50)
        ah, at, ao = _digits(a)
        bh, bt, bo = _digits(b)
        if ao >= bo and at >= bt and ah >= bh:
            return a, b


def _pair_sub_exchange(d=1):
    """At least one top digit < bottom digit, so an exchange is required."""
    d = _lvl(d)
    lo, hi = (300, 699) if d == 0 else (300, 989)
    while True:
        a = random.randint(lo, hi)
        b = random.randint(102, a - 50)
        ah, at, ao = _digits(a)
        bh, bt, bo = _digits(b)
        if ao < bo or at < bt:
            # easy: exactly one exchange (the tens digit left after an exchange still covers the bottom one)
            if d == 0 and not ((ao < bo and at > bt) or (ao >= bo and at < bt)):
                continue
            if d == 2 and not (ao < bo and at <= bt):
                continue
            return a, b


# ------------------------------------------------------------------ 3.2 ------
@skill("Y3.2.a", "Addition and subtraction facts within 20", S2)
def _(d=1):
    d = _lvl(d)
    cap = 10 if d == 0 else 20

    def bare_add():
        a = random.randint(2, cap - 2)
        b = random.randint(2, cap - a)
        return _numq("Work out %d + %d." % (a, b), a + b,
                     ["%d + %d = %d." % (a, b, a + b)])

    def bare_sub():
        a = random.randint(max(5, cap - 8), cap)
        b = random.randint(2, a - 1)
        return _numq("Work out %d − %d." % (a, b), a - b,
                     ["%d − %d = %d." % (a, b, a - b)])

    def on_line():
        a = random.randint(2, cap - 4)
        b = random.randint(2, cap - a)
        if d and random.random() < 0.4:
            return _lineq("Start at %d and jump back %d. Mark where you land."
                          % (a + b, b), a, [a + b],
                          ["%d − %d = %d." % (a + b, b, a)])
        return _lineq("Start at %d and jump forward %d. Mark where you land."
                      % (a, b), a + b, [a],
                      ["%d + %d = %d." % (a, b, a + b)])

    def missing():
        tot = random.randint(max(6, cap - 8), cap)
        b = random.randint(2, tot - 2)
        a = tot - b
        if random.random() < 0.5:
            return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                         ["Use the inverse: %d − %d = %d." % (tot, a, b)])
        return _numq("Find the missing number:  ___ − %d = %d" % (b, a), tot,
                     ["Use the inverse: %d + %d = %d." % (a, b, tot)])

    def word():
        who = pick(NAMES)
        thing = pick(_OBJ)
        a = random.randint(3, cap - 4)
        b = random.randint(2, cap - a)
        return _numq("%s had %d %s and found %d more. How many %s now?"
                     % (who, a, thing, b, thing), a + b,
                     ["%d + %d = %d %s." % (a, b, a + b, thing)], unit=thing)

    def compare():
        a = random.randint(3, cap - 3); b = random.randint(2, cap - a)
        c = random.randint(3, cap - 3); e = random.randint(2, cap - c)
        while c + e == a + b:
            c = random.randint(3, cap - 3); e = random.randint(2, cap - c)
        big = max(a + b, c + e)
        return _numq("Which is more, %d + %d or %d + %d? Type the larger total."
                     % (a, b, c, e), big,
                     ["%d + %d = %d and %d + %d = %d." % (a, b, a + b, c, e, c + e),
                      "The larger total is %d." % big])

    def two_step():
        a = random.randint(3, 8); b = random.randint(2, 7)
        c = random.randint(2, min(6, a + b - 1))
        return _numq("Work out %d + %d − %d." % (a, b, c), a + b - c,
                     ["%d + %d = %d." % (a, b, a + b),
                      "%d − %d = %d." % (a + b, c, a + b - c)])

    def io_add():
        b = random.randint(2, max(3, cap // 2))
        rows = _io_rows(1, cap - b, b)
        m = random.randrange(len(rows))
        return _ioq("Complete this addition input/output table. The rule is add %d — "
                    "type the missing Out number." % b, rows, m, rows[m][1],
                    ["The rule adds %d to every In number." % b,
                     "%d + %d = %d." % (rows[m][0], b, rows[m][1])],
                    rule="+ %d" % b)

    def io_sub():
        b = random.randint(2, max(3, cap // 2))
        rows = _io_rows(b + 1, cap, -b)
        m = random.randrange(len(rows))
        return _ioq("Complete this subtraction input/output table. The rule is "
                    "subtract %d — type the missing Out number." % b,
                    rows, m, rows[m][1],
                    ["The rule subtracts %d from every In number." % b,
                     "%d − %d = %d." % (rows[m][0], b, rows[m][1])],
                    rule="− %d" % b)

    def io_rule():
        b = random.randint(2, max(3, cap // 2))
        if random.random() < 0.5:
            rows = _io_rows(b + 2, cap, -b)
            why = "Every Out number is %d less than its In number." % b
        else:
            rows = _io_rows(1, cap - b, b)
            why = "Every Out number is %d more than its In number." % b
        return _ioq("Write the addition or subtraction rule for this input/output "
                    "table: type the number that is added or subtracted.",
                    rows, None, b, [why, "So the rule uses %d." % b],
                    placeholder="the number")

    def balance_add():
        tot = random.randint(max(8, cap - 6), cap)
        a = random.randint(2, tot - 2)
        c = random.randint(2, tot - 2)
        while c == a:
            c = random.randint(2, tot - 2)
        return _numq("Balance this addition equation. Find the missing number:  "
                     "%d + %d = %d + ___" % (a, tot - a, c), tot - c,
                     ["Both sides must equal the same total: %d + %d = %d."
                      % (a, tot - a, tot),
                      "%d − %d = %d." % (tot, c, tot - c)])

    def balance_sub():
        res = random.randint(2, max(3, cap - 5))
        b = random.randint(1, cap - res)
        e = random.randint(1, cap - res)
        while e == b:
            e = random.randint(1, cap - res)
        return _numq("Balance this subtraction equation. Find the missing number:  "
                     "%d − %d = %d − ___" % (res + b, b, res + e), e,
                     ["The left side is %d − %d = %d." % (res + b, b, res),
                      "%d − %d = %d, so the missing number is %d."
                      % (res + e, res, e, e)])

    def zero_or_all():
        a = random.randint(5, cap)
        if random.random() < 0.5:
            return _numq("Subtract zero: work out %d − 0." % a, a,
                         ["Subtracting zero leaves the number unchanged: %d." % a])
        return _numq("Subtract all of the number: work out %d − %d." % (a, a), 0,
                     ["Subtracting all of a number leaves nothing, so the answer is 0."])

    opts = [bare_add, bare_sub, on_line, on_line, word, missing,
            io_add, io_sub, balance_add, zero_or_all]
    if d == 2:
        opts = [bare_sub, on_line, missing, word, two_step, compare,
                io_sub, io_rule, io_rule, balance_add, balance_sub]      # "18 − 0" is no hard question
    elif d == 1:
        opts += [compare, io_rule, balance_sub]
    return pick(opts)()


@skill("Y3.2.b", "Add ones or tens to a 2-digit number", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.choice([n for n in range(21, 60) if n % 10 <= 7])
        b = pick([random.randint(2, 9 - (a % 10)),
                  random.choice([10, 20, 30])])
    elif d == 1:
        a = random.randint(23, 79)
        b = pick([random.randint(2, 9), random.choice([10, 20, 30, 40])])
    else:
        a = random.randint(37, 88)
        b = pick([random.randint(4, 9), random.choice([20, 30, 40, 50])])
    b = max(2, b)
    tot = a + b

    def bare():
        return _numq("Work out %d + %d (mentally)." % (a, b), tot,
                     ["%d + %d = %d." % (a, b, tot)])

    def on_line():
        return _lineq("Start at %d and jump forward %d. Mark where you land."
                      % (a, b), tot, [a],
                      ["%d + %d = %d." % (a, b, tot)])

    def blocks():
        return _btq("Work out %d + %d, then build the answer with base ten blocks."
                    % (a, b), tot,
                    ["Add the %s: %d + %d = %d."
                     % ("tens" if b % 10 == 0 else "ones", a, b, tot)])

    def missing():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["Inverse: %d − %d = %d." % (tot, a, b)])

    def word():
        who = pick(NAMES)
        return _numq("%s has %d %s and buys %d more. How many does %s have now?"
                     % (who, a, "stickers", b, who), tot,
                     ["%d + %d = %d stickers." % (a, b, tot)], unit="stickers")

    def two_step():
        c = pick([10, 20, 5, 4])
        return _numq("Work out %d + %d + %d." % (a, b, c), tot + c,
                     ["%d + %d = %d." % (a, b, tot),
                      "%d + %d = %d." % (tot, c, tot + c)])

    def io_ten():
        step = pick([10, -10])
        rows = _io_rows(21, 79, step)
        m = random.randrange(len(rows))
        return _ioq("This input/output table has the rule add 10 or subtract 10. "
                    "Use the rule to complete the table: type the missing Out number.",
                    rows, m, rows[m][1],
                    ["The rule is %s 10." % ("add" if step > 0 else "subtract"),
                     "%d %s 10 = %d" % (rows[m][0], "+" if step > 0 else "−",
                                        rows[m][1])],
                    rule="%s 10" % ("+" if step > 0 else "−"))

    opts = [bare, on_line, blocks, word, missing, io_ten]
    if d == 2:
        opts = [on_line, blocks, missing, word, two_step, two_step, io_ten]
    return pick(opts)()


@skill("Y3.2.c", "Subtract ones or tens from a 2-digit number", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.choice([n for n in range(35, 70) if n % 10 >= 2])
        b = pick([random.randint(2, a % 10), random.choice([10, 20])])
    elif d == 1:
        a = random.randint(35, 99)
        b = pick([random.randint(2, 9), random.choice([10, 20, 30])])
    else:
        a = random.randint(52, 99)
        b = pick([random.randint(4, 9), random.choice([20, 30, 40])])
    b = max(2, min(b, a - 5))
    res = a - b

    def bare():
        return _numq("Work out %d − %d (mentally)." % (a, b), res,
                     ["%d − %d = %d." % (a, b, res)])

    def on_line():
        return _lineq("Start at %d and jump back %d. Mark where you land." % (a, b),
                      res, [a], ["%d − %d = %d." % (a, b, res)])

    def blocks():
        return _btq("Work out %d − %d, then build the answer with base ten blocks."
                    % (a, b), res, ["%d − %d = %d." % (a, b, res)])

    def missing():
        return _numq("Find the missing number:  %d − ___ = %d" % (a, res), b,
                     ["Inverse: %d − %d = %d." % (a, res, b)])

    def word():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s had %d %s and lost %d of them. How many are left?"
                     % (who, a, thing, b), res,
                     ["%d − %d = %d %s." % (a, b, res, thing)], unit=thing)

    def difference():
        return _numq("What is the difference between %d and %d?" % (a, res), b,
                     ["%d − %d = %d." % (a, res, b)])

    def model_one_digit():
        """Subtract a one-digit number from a two-digit number, no regrouping."""
        tens = random.randint(2, 9)
        ones = random.randint(4, 9)
        n = tens * 10 + ones
        s = random.randint(1, ones)
        return _btq("Use the base ten model to subtract the one-digit number %d from "
                    "the two-digit number %d. No regrouping is needed — build the "
                    "answer." % (s, n), n - s,
                    ["There are %d ones, so take %d away: %d − %d = %d."
                     % (ones, s, ones, s, ones - s),
                     "The %d tens do not change, so %d − %d = %d."
                     % (tens, n, s, n - s)])

    opts = [bare, on_line, blocks, word, missing, model_one_digit]
    if d == 2:
        opts = [on_line, blocks, missing, word, difference, difference,
                model_one_digit]
    return pick(opts)()


@skill("Y3.2.d", "Add two 2-digit numbers", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:                      # no regrouping in the ones column
        ao = random.randint(1, 4); bo = random.randint(1, 9 - ao)
        at = random.randint(1, 4); bt = random.randint(1, min(4, 9 - at))
        a = at * 10 + ao; b = bt * 10 + bo
    elif d == 1:
        a = random.randint(14, 79)
        b = random.randint(13, max(14, 99 - a))
    else:
        while True:
            a = random.randint(26, 79)
            b = random.randint(26, 79)
            if (a % 10) + (b % 10) >= 10 and a + b <= 158:
                break
    tot = a + b

    def bare():
        tens = (a - a % 10) + (b - b % 10)
        return _numq("Work out %d + %d." % (a, b), tot,
                     ["Add the tens: %d + %d = %d."
                      % (a - a % 10, b - b % 10, tens),
                      "Then the ones: %d + %d = %d, so the total is %d."
                      % (a % 10, b % 10, (a % 10) + (b % 10), tot)])

    def blocks():
        return _btq("Work out %d + %d with base ten blocks, then build the answer."
                    % (a, b), tot,
                    ["%d + %d = %d." % (a - a % 10, b - b % 10,
                                        (a - a % 10) + (b - b % 10)),
                     "Add the ones to get %d." % tot])

    def on_line():
        return _lineq("Start at %d and jump on %d. Mark where you land." % (a, b),
                      tot, [a], ["%d + %d = %d." % (a, b, tot)])

    def missing():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["Inverse: %d − %d = %d." % (tot, a, b)])

    def word():
        who = pick(NAMES)
        return _numq("%s scored %d points in game 1 and %d points in game 2. "
                     "How many points altogether?" % (who, a, b), tot,
                     ["%d + %d = %d points." % (a, b, tot)], unit="points")

    def compare():
        c = random.randint(15, 70); e = random.randint(15, 99 - c)
        while c + e == tot:
            c = random.randint(15, 70); e = random.randint(15, 99 - c)
        big = max(tot, c + e)
        return _numq("Which total is greater, %d + %d or %d + %d? Type the greater total."
                     % (a, b, c, e), big,
                     ["%d + %d = %d, %d + %d = %d." % (a, b, tot, c, e, c + e),
                      "The greater total is %d." % big])

    def io_add():
        step = random.randint(11, 39)
        rows = _io_rows(12, 99 - step, step)
        m = random.randrange(len(rows))
        return _ioq("Complete this addition input/output table. Add %d to each In "
                    "number and type the missing Out number." % step,
                    rows, m, rows[m][1],
                    ["The rule adds %d." % step,
                     "%d + %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="+ %d" % step)

    opts = [bare, blocks, on_line, word, missing, io_add]
    if d == 2:
        opts = [bare, blocks, missing, word, compare, on_line, io_add]
    return pick(opts)()


@skill("Y3.2.e", "Subtract a 2-digit number from a 2-digit number", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:                      # no exchange needed
        ao = random.randint(4, 9); bo = random.randint(1, ao)
        at = random.randint(4, 9); bt = random.randint(1, at - 1)
        a = at * 10 + ao; b = bt * 10 + bo
        if b < 11:
            b = 11
    elif d == 1:
        a = random.randint(42, 99); b = random.randint(11, a - 10)
    else:
        while True:
            a = random.randint(42, 99); b = random.randint(15, a - 12)
            if (a % 10) < (b % 10):
                break
    res = a - b

    def bare():
        return _numq("Work out %d − %d." % (a, b), res,
                     ["%d − %d = %d." % (a, b, res)])

    def blocks():
        return _btq("Work out %d − %d with base ten blocks, then build the answer."
                    % (a, b), res,
                    ["Take away %d from %d." % (b, a), "The answer is %d." % res])

    def on_line():
        return _lineq("Start at %d and count back %d. Mark where you land." % (a, b),
                      res, [a], ["%d − %d = %d." % (a, b, res)])

    def missing():
        if random.random() < 0.5:
            return _numq("Find the missing number:  %d − ___ = %d" % (a, res), b,
                         ["Inverse: %d − %d = %d." % (a, res, b)])
        return _numq("Find the missing number:  ___ − %d = %d" % (b, res), a,
                     ["Inverse: %d + %d = %d." % (res, b, a)])

    def word():
        who = pick(NAMES)
        return _numq("%s had %dp and spent %s. How much is left, in pence?"
                     % (who, a, money(b)), res,
                     ["%d − %d = %dp." % (a, b, res)], unit="p")

    def difference():
        return _numq("What is the difference between %d and %d?" % (a, b), res,
                     ["%d − %d = %d." % (a, b, res)])

    def io_sub():
        step = random.randint(11, 39)
        rows = _io_rows(step + 10, 99, -step)
        m = random.randrange(len(rows))
        return _ioq("Complete this subtraction input/output table. Subtract %d from "
                    "each In number and type the missing Out number." % step,
                    rows, m, rows[m][1],
                    ["The rule subtracts %d." % step,
                     "%d − %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="− %d" % step)

    opts = [bare, blocks, on_line, word, missing, io_sub]
    if d == 2:
        opts = [bare, blocks, missing, word, difference, on_line, io_sub]
    return pick(opts)()


@skill("Y3.2.f", "Missing number (inverse) within 100", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(10, 30); b = random.randint(5, 20)
    elif d == 1:
        a = random.randint(20, 60); b = random.randint(11, 39)
    else:
        a = random.randint(28, 64); b = random.randint(17, 35)
    tot = a + b

    def miss_add():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["Use the inverse: %d − %d = %d." % (tot, a, b)])

    def miss_start():
        return _numq("Find the missing number:  ___ − %d = %d" % (b, a), tot,
                     ["Use the inverse: %d + %d = %d." % (a, b, tot)])

    def on_line():
        return _lineq("A jump forward of %d lands on %d. Mark the number the jump "
                      "started from." % (b, tot), a, [tot],
                      ["Inverse: %d − %d = %d." % (tot, b, a)])

    def bar_model():
        return _btq("A whole of %d is split into two parts. One part is %d. "
                    "Build the other part with base ten blocks." % (tot, a), b,
                    ["Whole − part = part: %d − %d = %d." % (tot, a, b)])

    def word():
        who = pick(NAMES)
        return _numq("%s had %d %s. After being given some more, %s had %d. "
                     "How many were given?" % (who, a, "beads", who, tot), b,
                     ["Inverse: %d − %d = %d beads." % (tot, a, b)], unit="beads")

    def two_step():
        c = random.randint(5, 20)
        return _numq("Find the missing number:  %d + ___ − %d = %d"
                     % (a, c, tot - c), b,
                     ["%d + %d = %d." % (tot - c, c, tot),
                      "%d − %d = %d." % (tot, a, b)])

    def io_rule():
        step = pick([10, 20, 30]) if d == 0 else random.randint(*((11, 40) if d == 1 else (21, 45)))
        if random.random() < 0.5:
            rows = _io_rows(step + 5, 100, -step)
            why = "Every Out number is %d less than its In number." % step
        else:
            rows = _io_rows(5, 100 - step, step)
            why = "Every Out number is %d more than its In number." % step
        return _ioq("Write the addition or subtraction rule for this input/output "
                    "table: type the number that is added or subtracted.",
                    rows, None, step, [why, "So the rule uses %d." % step],
                    placeholder="the number")

    def which_sign():
        x = random.randint(*((14, 40) if d == 0 else ((24, 80) if d == 1 else (41, 80))))
        y = random.randint(*((3, 9) if d == 0 else ((5, min(20, x - 4)) if d == 1 else (16, 35))))
        if random.random() < 0.5:
            return _wordq("Which sign makes this number sentence true, + or −?  "
                          "%d ___ %d = %d.  Type plus or minus." % (x, y, x + y),
                          "plus", ["%d + %d = %d, so the sign is +." % (x, y, x + y)],
                          placeholder="plus or minus")
        return _wordq("Which sign makes this number sentence true, + or −?  "
                      "%d ___ %d = %d.  Type plus or minus." % (x, y, x - y),
                      "minus", ["%d − %d = %d, so the sign is −." % (x, y, x - y)],
                      placeholder="plus or minus")

    opts = [miss_add, miss_start, on_line, bar_model, word, io_rule, which_sign]
    if d == 2:
        opts = [miss_add, on_line, bar_model, two_step, word, io_rule, which_sign]
    return pick(opts)()


@skill("Y3.2.g", "Addition / subtraction word problem (within 100)", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(12, 35); b = random.randint(5, 15)
    elif d == 1:
        a = random.randint(23, 68); b = random.randint(11, 30)
    else:
        a = random.randint(34, 72); b = random.randint(15, 30)

    def add_word():
        who = pick(NAMES); thing = pick(_OBJ)
        return _numq("%s has %d %s and is given %d more. How many %s now?"
                     % (who, a, thing, b, thing), a + b,
                     ["'Given %d more' means %s gets more, so add." % (b, who),
                      "%d + %d = %d %s." % (a, b, a + b, thing)], unit=thing)

    def sub_word():
        who = pick(NAMES); thing = pick(_OBJ)
        top = a if a - b >= 5 else a + b
        return _numq("%s had %d %s and gave away %d. How many are left?"
                     % (who, top, thing, b), top - b,
                     ["'Gave away' and 'left' mean some are taken away, so subtract.",
                      "%d − %d = %d %s." % (top, b, top - b, thing)], unit=thing)

    def money_word():
        who = pick(NAMES)
        p1 = random.randint(20, 45); p2 = random.randint(15, 40)
        return _numq("%s buys a rubber for %s and a pencil for %s. "
                     "How much is that altogether, in pence?"
                     % (who, money(p1), money(p2)), p1 + p2,
                     ["'Altogether' means both prices put together, so add.",
                      "%d + %d = %dp." % (p1, p2, p1 + p2)], unit="p")

    def chart():
        # numbers within 100 to subtract, as the skill says (the chart prints a value between gridlines)
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(*{0: (12, 45), 1: (21, 79), 2: (31, 98)}[d]) for _ in cats]
        i, j = random.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        if vals[i] - vals[j] < 6:
            vals[j] = vals[i] - random.randint(6, min(29, vals[i] - 5))
        return _barq("The chart shows books read each day. How many more books "
                     "were read on %s than on %s?" % (cats[i], cats[j]),
                     cats, vals, vals[i] - vals[j],
                     ["'How many more … than' means find the difference, so subtract.",
                      "%s: %d, %s: %d." % (cats[i], vals[i], cats[j], vals[j]),
                      "%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j])])

    def picto():
        key = pick([2, 5]) if d == 0 else pick([5, 10])     # totals of 2-digit numbers, not 12 + 8
        cats = ["Red", "Blue", "Green"]
        vals = [key * random.randint(3, min(9, 45 // key)) for _ in cats]     # a total within 100
        return _pictq("The pictogram shows the cars in a car park. How many red "
                      "and blue cars altogether?", cats, vals, key, "car",
                      vals[0] + vals[1],
                      ["'Altogether' means red and blue together, so add.",
                       "Red %d, blue %d." % (vals[0], vals[1]),
                       "%d + %d = %d cars." % (vals[0], vals[1], vals[0] + vals[1])])

    def two_step():
        c = random.randint(8, 25)
        who = pick(NAMES)
        return _numq("%s had %d %s, gave %d to a friend, then collected %d more. "
                     "How many %s now?" % (who, a, "cards", b, c, "cards"),
                     a - b + c,
                     ["'Gave' means take away, so subtract; 'collected more' means add.",
                      "%d − %d = %d." % (a, b, a - b),
                      "%d + %d = %d cards." % (a - b, c, a - b + c)], unit="cards")

    opts = [add_word, sub_word, money_word, chart, picto]
    if d == 2:
        opts = [two_step, two_step, chart, picto, money_word, sub_word]
    return pick(opts)()


# ------------------------------------------------------------------ 3.3 ------
@skill("Y3.3.a", "Add ones, tens or hundreds to a 3-digit number", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        b = pick([random.randint(2, 5), random.choice([10, 20]), 100])
        a = random.randint(123, min(456, 940 - b))
    elif d == 1:
        b = pick([random.randint(2, 9), random.choice([10, 20, 30]),
                  random.choice([100, 200])])
        a = random.randint(123, min(780, 940 - b))
    else:
        b = pick([random.randint(5, 9), random.choice([30, 40, 50]),
                  random.choice([200, 300])])
        a = random.randint(146, min(780, 940 - b))
    tot = a + b

    def bare():
        return _numq("Work out %d + %d (mentally)." % (a, b), tot,
                     ["Add the %s: %d + %d = %d."
                      % ("hundreds" if b % 100 == 0 else
                         ("tens" if b % 10 == 0 else "ones"), a, b, tot)])

    def blocks():
        return _btq("Add %d to %d, then build the answer with base ten blocks."
                    % (b, a), tot, ["%d + %d = %d." % (a, b, tot)])

    def on_line():
        # keep 3-digit lines on round numbers so the scale stays readable
        start = (a // 10) * 10
        jump = pick([10, 20, 30, 50, 100])
        return _lineq("Start at %d and jump forward %d. Mark where you land."
                      % (start, jump), start + jump, [start],
                      ["%d + %d = %d." % (start, jump, start + jump)])

    def missing():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["Inverse: %d − %d = %d." % (tot, a, b)])

    def words():
        return _numq("Work out %s plus %d." % (n_words(a), b), tot,
                     ["%d + %d = %d." % (a, b, tot)])

    def two_step():
        c = pick([c0 for c0 in (10, 20, 100, 200) if tot + c0 <= 999])
        return _numq("Work out %d + %d + %d." % (a, b, c), tot + c,
                     ["%d + %d = %d." % (a, b, tot),
                      "%d + %d = %d." % (tot, c, tot + c)])

    opts = [bare, blocks, on_line, missing, words]
    if d == 2:
        opts = [blocks, on_line, missing, words, two_step, two_step]
    return pick(opts)()


@skill("Y3.3.b", "Column addition (no regrouping)", S3)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_add_no_carry(d)
    tot = a + b
    steps = ["Ones: %d+%d=%d, tens: %d+%d=%d, hundreds: %d+%d=%d — no regrouping."
             % (a % 10, b % 10, (a % 10) + (b % 10),
                (a // 10) % 10, (b // 10) % 10, ((a // 10) % 10) + ((b // 10) % 10),
                a // 100, b // 100, (a // 100) + (b // 100)),
             "Total: %d." % tot]

    def bare():
        return _numq("Work out %d + %d using the column method." % (a, b), tot, steps)

    def blocks():
        return _btq("Work out %d + %d using the column method, then build the "
                    "answer with base ten blocks." % (a, b), tot, steps)

    def missing():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["No column needs regrouping.",
                      "Inverse: %d − %d = %d." % (tot, a, b)])

    def word():
        who = pick(NAMES)
        return _numq("%s counted %d red bricks and %d blue bricks. How many bricks "
                     "altogether?" % (who, a, b), tot,
                     ["%d + %d = %d bricks." % (a, b, tot)], unit="bricks")

    def inverse():
        return _numq("%d + %d = ___ . Work it out, then check with the inverse."
                     % (a, b), tot,
                     ["%d + %d = %d." % (a, b, tot),
                      "Check: %d − %d = %d ✓." % (tot, b, a)])

    def digit_focus():
        return _numq("In the column addition %d + %d, what digit goes in the tens "
                     "column of the answer?" % (a, b),
                     ((a // 10) % 10) + ((b // 10) % 10),
                     ["Tens: %d + %d = %d, and there is nothing to carry."
                      % ((a // 10) % 10, (b // 10) % 10,
                         ((a // 10) % 10) + ((b // 10) % 10))])

    def io_add():
        step = pick([100, 110, 120, 200, 210, 220, 130, 140])
        pool = [i for i in range(110, 781 - step)
                if (i // 10) % 10 + (step // 10) % 10 < 10]
        rows = [[i, i + step] for i in sorted(random.sample(pool, 4))]
        m = random.randrange(len(rows))
        return _ioq("Complete this addition input/output table with three-digit "
                    "numbers. Add %d to each In number and type the missing Out "
                    "number." % step, rows, m, rows[m][1],
                    ["The rule adds %d." % step,
                     "%d + %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="+ %d" % step)

    opts = [bare, blocks, blocks, word, inverse, io_add]
    if d == 2:
        opts = [blocks, missing, missing, inverse, digit_focus, word, io_add]
    return pick(opts)()


@skill("Y3.3.c", "Column addition (with regrouping)", S3)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_add_carry(d)
    tot = a + b
    ones = (a % 10) + (b % 10)
    steps = ["Ones: %d + %d = %d%s." % (a % 10, b % 10, ones,
                                        " — carry 1 ten" if ones >= 10 else ""),
             "Carrying where a column makes 10 or more: %d + %d = %d." % (a, b, tot)]

    def bare():
        return _numq("Work out %d + %d using the column method." % (a, b), tot, steps)

    def blocks():
        return _btq("Work out %d + %d (you will need to exchange), then build the "
                    "answer with base ten blocks." % (a, b), tot, steps)

    def missing():
        return _numq("Find the missing number:  ___ + %d = %d" % (b, tot), a,
                     ["Inverse: %d − %d = %d." % (tot, b, a)])

    def word():
        return _numq("A shop sold %d tickets on Saturday and %d on Sunday. "
                     "How many tickets in total?" % (a, b),
                     tot, ["%d + %d = %d tickets." % (a, b, tot)], unit="tickets")

    def inverse():
        return _numq("%d + %d = ___ . Work it out, then check with the inverse."
                     % (a, b), tot,
                     ["%d + %d = %d." % (a, b, tot),
                      "Check: %d − %d = %d ✓." % (tot, a, b)])

    def compare():
        c, e = _pair_add_carry(d)
        while c + e == tot:
            c, e = _pair_add_carry(d)
        big = max(tot, c + e)
        return _numq("Which total is greater, %d + %d or %d + %d? Type the greater "
                     "total." % (a, b, c, e), big,
                     ["%d + %d = %d and %d + %d = %d." % (a, b, tot, c, e, c + e),
                      "The greater total is %d." % big])

    opts = [bare, blocks, blocks, word, inverse]
    if d == 2:
        opts = [blocks, missing, missing, compare, inverse, word]
    return pick(opts)()


@skill("Y3.3.d", "Column subtraction (no exchange)", S3)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_sub_no_exchange(d)
    res = a - b
    steps = ["Every digit on top is big enough, so no exchange is needed.",
             "%d − %d = %d." % (a, b, res)]

    def bare():
        return _numq("Work out %d − %d using the column method." % (a, b), res, steps)

    def blocks():
        return _btq("Work out %d − %d using the column method, then build the "
                    "answer with base ten blocks." % (a, b), res, steps)

    def missing():
        return _numq("Find the missing number:  %d − ___ = %d" % (a, res), b,
                     ["Inverse: %d − %d = %d." % (a, res, b)])

    def word():
        return _numq("A library had %d books and lent out %d. How many books are "
                     "left on the shelves?" % (a, b), res,
                     ["%d − %d = %d books." % (a, b, res)], unit="books")

    def inverse():
        return _numq("%d − %d = ___ . Work it out, then check with the inverse."
                     % (a, b), res,
                     ["%d − %d = %d." % (a, b, res),
                      "Check: %d + %d = %d ✓." % (res, b, a)])

    def difference():
        return _numq("What is the difference between %d and %d?" % (a, b), res,
                     ["%d − %d = %d." % (a, b, res)])

    def io_sub():
        step = pick([100, 110, 120, 200, 210, 130, 140, 150])
        pool = [i for i in range(step + 105, 1000)
                if (i // 10) % 10 >= (step // 10) % 10]
        rows = [[i, i - step] for i in sorted(random.sample(pool, 4))]
        m = random.randrange(len(rows))
        return _ioq("Complete this subtraction input/output table with three-digit "
                    "numbers. Subtract %d from each In number and type the missing "
                    "Out number." % step, rows, m, rows[m][1],
                    ["The rule subtracts %d." % step,
                     "%d − %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="− %d" % step)

    opts = [bare, blocks, blocks, word, inverse, io_sub]
    if d == 2:
        opts = [blocks, missing, missing, difference, inverse, word, io_sub]
    return pick(opts)()


@skill("Y3.3.e", "Column subtraction (with exchange)", S3)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_sub_exchange(d)
    res = a - b
    where = "ones" if (a % 10) < (b % 10) else "tens"
    steps = ["The %s column on top is too small, so exchange from the next column."
             % where,
             "%d − %d = %d." % (a, b, res)]

    def bare():
        return _numq("Work out %d − %d using the column method." % (a, b), res, steps)

    def blocks():
        return _btq("Work out %d − %d (you will need to exchange), then build the "
                    "answer with base ten blocks." % (a, b), res, steps)

    def missing():
        return _numq("Find the missing number:  ___ − %d = %d" % (b, res), a,
                     ["Inverse: %d + %d = %d." % (res, b, a)])

    def word():
        who = pick(NAMES)
        return _numq("%s had %d points and lost %d points. How many points now?"
                     % (who, a, b), res,
                     ["%d − %d = %d points." % (a, b, res)], unit="points")

    def inverse():
        return _numq("%d − %d = ___ . Work it out, then check with the inverse."
                     % (a, b), res,
                     ["%d − %d = %d." % (a, b, res),
                      "Check: %d + %d = %d ✓." % (res, b, a)])

    def two_step():
        c = random.randint(20, 90)
        return _numq("Work out %d − %d, then add %d. What is the final number?"
                     % (a, b, c), res + c,
                     ["%d − %d = %d." % (a, b, res),
                      "%d + %d = %d." % (res, c, res + c)])

    opts = [bare, blocks, blocks, word, inverse]
    if d == 2:
        opts = [blocks, missing, missing, two_step, inverse, word]
    return pick(opts)()


@skill("Y3.3.f", "Check a calculation with the inverse", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(120, 300); b = random.randint(100, 200)
    elif d == 1:
        a = random.randint(150, 600); b = random.randint(110, 350)
    else:
        a = random.randint(238, 640); b = random.randint(147, 350)
    tot = a + b

    def add_then_check():
        return _numq("%d + %d = ___ . Work it out, then check with the inverse."
                     % (a, b), tot,
                     ["%d + %d = %d." % (a, b, tot),
                      "Check: %d − %d = %d ✓." % (tot, b, a)])

    def sub_then_check():
        return _numq("%d − %d = ___ . Work it out, then check with the inverse."
                     % (tot, b), a,
                     ["%d − %d = %d." % (tot, b, a),
                      "Check: %d + %d = %d ✓." % (a, b, tot)])

    def find_error():
        wrong = tot + pick([-100, -10, 10, 100, -1, 1])
        if wrong > 999:                       # keep the wrong total within 1,000
            wrong = tot - 100
        return _numq("%s says %d + %d = %d. Check with the inverse and type the "
                     "correct answer." % (pick(NAMES), a, b, wrong), tot,
                     ["%d − %d = %d, not %d, so the answer was wrong."
                      % (wrong, b, wrong - b, a),
                      "The correct total is %d." % tot])

    def blocks():
        return _btq("Work out %d − %d and build the answer with base ten blocks. "
                    "Check by adding %d back on." % (tot, b, b), a,
                    ["%d − %d = %d." % (tot, b, a),
                     "Check: %d + %d = %d ✓." % (a, b, tot)])

    def on_line():
        start = (tot // 10) * 10
        # a 3-digit subtraction to check from the middle tier (920 − 20 is no calculation to check)
        jump = pick([20, 50, 100]) if d == 0 else 10 * random.randint(11 if d == 1 else 13, max(14, start // 10 - 10))
        return _lineq("Work out %d − %d and mark the answer on the number line. "
                      "Check by adding %d back on." % (start, jump, jump),
                      start - jump, [start],
                      ["%d − %d = %d." % (start, jump, start - jump),
                       "Check: %d + %d = %d ✓." % (start - jump, jump, start)])

    def missing():
        return _numq("Find the missing number:  ___ + %d = %d" % (b, tot), a,
                     ["Inverse: %d − %d = %d." % (tot, b, a)])

    opts = [add_then_check, sub_then_check, blocks, on_line, find_error, missing]
    if d == 2:
        opts = [sub_then_check, find_error, blocks, blocks, missing, on_line]
    return pick(opts)()


@skill("Y3.3.g", "Missing number / two-step problem (3-digit)", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(110, 250); b = random.randint(100, 200)
    elif d == 1:
        a = random.randint(120, 400); b = random.randint(110, 300)
    else:
        a = random.randint(216, 450); b = random.randint(128, 330)
    tot = a + b

    def missing_add():
        return _numq("Find the missing number:  %d + ___ = %d" % (a, tot), b,
                     ["Inverse: %d − %d = %d." % (tot, a, b)])

    def missing_sub():
        return _numq("Find the missing number:  %d − ___ = %d" % (tot, b), a,
                     ["Inverse: %d − %d = %d." % (tot, b, a)])

    def shop():
        c = random.randint(50, 150)
        return _numq("A shop had %d books. It sold %d, then received %d more. "
                     "How many books now?" % (tot, b, c), tot - b + c,
                     ["%d − %d = %d." % (tot, b, tot - b),
                      "%d + %d = %d books." % (tot - b, c, tot - b + c)], unit="books")

    def blocks():
        c = random.randint(20, 90)
        return _btq("Work out %d + %d − %d, then build the answer with base ten "
                    "blocks." % (a, b, c), tot - c,
                    ["%d + %d = %d." % (a, b, tot),
                     "%d − %d = %d." % (tot, c, tot - c)])

    def chart():
        cats = ["Year 3", "Year 4", "Year 5"]
        vals = [random.randint(*((6, 19) if d == 0 else ((60, 190) if d == 1 else (120, 390)))) * (10 if d == 0 else 1)
                for _ in cats]
        return _barq("The chart shows how many stickers each year group collected. "
                     "How many did Year 3 and Year 4 collect altogether?",
                     cats, vals, vals[0] + vals[1],
                     ["Year 3: %d, Year 4: %d." % (vals[0], vals[1]),
                      "%d + %d = %d." % (vals[0], vals[1], vals[0] + vals[1])])

    def two_step_line():
        start = (a // 10) * 10
        j1 = pick([100, 200])
        j2 = pick([20, 50]) if j1 == 100 else pick([20, 50, 100])
        return _lineq("Start at %d, jump forward %d, then jump back %d. Mark where "
                      "you land." % (start, j1, j2), start + j1 - j2, [start],
                      ["%d + %d = %d." % (start, j1, start + j1),
                       "%d − %d = %d." % (start + j1, j2, start + j1 - j2)])

    opts = [missing_add, missing_sub, shop, blocks, chart]
    if d == 2:
        opts = [shop, blocks, two_step_line, chart, missing_sub, blocks]
    return pick(opts)()


# ------------------------------------------------------------------ 3.4 ------
@skill("Y3.4.a", "Multiplication as an array", S4)
def _(d=1):
    d = _lvl(d)
    # Year 3 arrays: the 2, 5 and 10 facts from Year 2 to start, then the 3, 4 and 8 tables (never a 2 × 2)
    if d == 0:
        r = random.randint(2, 5); c = random.randint(3, 6)
    elif d == 1:
        r = random.randint(3, 6); c = random.randint(3, 9)
    else:
        r = random.randint(4, 8); c = random.randint(6, 12)

    def build():
        return _arrayq("Make an array to show %d × %d, then type the total number "
                       "of counters." % (r, c), r, c,
                       ["%d rows of %d = %d." % (r, c, r * c)])

    def build_from_total():
        return _arrayq("Counters are shared into %d equal rows with %d in each row. "
                       "Build the array, then type how many counters there are "
                       "altogether." % (r, c), r, c,
                       ["%d equal rows of %d." % (r, c),
                        "%d × %d = %d counters." % (r, c, r * c)])

    def commutative():
        return _arrayq("Turn the array round: build %d rows of %d and type the total."
                       % (c, r), c, r,
                       ["%d × %d = %d × %d = %d." % (c, r, r, c, r * c)])

    def read_bare():
        return _numq("An array has %d rows with %d counters in each row. How many "
                     "counters altogether?" % (r, c), r * c,
                     ["%d × %d = %d." % (r, c, r * c)])

    def rows_missing():
        return _numq("An array has %d counters altogether with %d in each row. "
                     "How many rows are there?" % (r * c, c), r,
                     ["%d ÷ %d = %d rows." % (r * c, c, r)], unit="rows")

    def word():
        who = pick(NAMES)
        return _numq("%s plants %d rows of %d seeds. How many seeds in total?"
                     % (who, r, c), r * c,
                     ["%d × %d = %d seeds." % (r, c, r * c)], unit="seeds")

    # --- equal groups: g groups of p, kept small enough for the group model ---
    if d == 0:
        g, p = random.randint(2, 4), random.randint(3, 5)
    elif d == 1:
        g, p = random.randint(3, 6), random.randint(3, 8)
    else:
        g, p = random.randint(3, 8), random.randint(4, 10)
    tot = g * p

    def count_groups():
        return _egq("Count the equal groups. There are %d equal groups with %d "
                    "counters in each group. How many counters are there in total?"
                    % (g, p), g, p, tot,
                    ["%d equal groups of %d." % (g, p),
                     "%d × %d = %d counters." % (g, p, tot)])

    def repeated_addition_array():
        # short enough to read (at most 6 terms), harder by tier: 3 + 3 + 3, then 8 + 8 + 8 + 8 + 8
        rr = random.randint(*{0: (2, 4), 1: (3, 5), 2: (4, 6)}[d])
        cc = random.randint(*{0: (2, 5), 1: (3, 8), 2: (6, 12)}[d])
        chain = " + ".join([str(cc)] * rr)
        return _numq("An array has %d rows with %d counters in each row. The repeated "
                     "addition for this array is %s. What is the total?"
                     % (rr, cc, chain), rr * cc,
                     ["%s = %d." % (chain, rr * cc),
                      "That is the same as %d × %d = %d." % (rr, cc, rr * cc)])

    def mult_expression_groups():
        return _egq("Put the %d counters into equal groups of %d. Complete the "
                    "multiplication for the equal groups:  ___ × %d = %d. Type the "
                    "missing number." % (tot, p, p, tot), g, p, g,
                    ["There are %d equal groups, so the expression is %d × %d."
                     % (g, g, p)],
                    answer_type="int")

    def write_mult_sentence():
        return _egq("Complete the multiplication sentence for these equal groups:  "
                    "%d × %d = ___" % (g, p), g, p, tot,
                    ["%d equal groups of %d." % (g, p),
                     "%d × %d = %d." % (g, p, tot)])

    def relate_add_mult_groups():
        chain = " + ".join([str(p)] * g)
        return _egq("These %d equal groups of %d can be written as the repeated "
                    "addition %s, or as the multiplication %d × %d. What is the "
                    "total?" % (g, p, chain, g, p), g, p, tot,
                    ["%s = %d." % (chain, tot),
                     "%d × %d = %d — addition and multiplication agree."
                     % (g, p, tot)])

    def relate_add_mult():
        n = random.randint(3, 6)
        v = random.randint(3, 9)
        chain = " + ".join([str(v)] * n)
        return _numq("Work out the addition %s. Then write it as a multiplication "
                     "and type the answer." % chain, n * v,
                     ["%s = %d." % (chain, n * v),
                      "As a multiplication that is %d × %d = %d." % (n, v, n * v)])

    def mult_expression_array():
        return _arrayq("Build an array with %d rows of %d. The multiplication "
                       "expression for this array is %d × %d — type its total."
                       % (r, c, r, c), r, c,
                       ["The array shows %d rows of %d." % (r, c),
                        "%d × %d = %d." % (r, c, r * c)])

    def make_array_model():
        return _arrayq("Make an array to model the multiplication %d × %d, then type "
                       "how many counters your array holds." % (r, c), r, c,
                       ["An array of %d rows of %d models %d × %d." % (r, c, r, c),
                        "%d × %d = %d." % (r, c, r * c)])

    def build_groups():
        gg, pp = min(g, 8), min(p, 10)
        return _egbuildq("Make %d equal groups with %d counters in each group, then "
                         "type how many counters there are altogether."
                         % (gg, pp), gg, pp,
                         ["%d equal groups of %d." % (gg, pp),
                          "%d × %d = %d." % (gg, pp, gg * pp)])

    opts = [build, commutative, read_bare, word, count_groups,
            repeated_addition_array, write_mult_sentence, relate_add_mult_groups,
            make_array_model, build_groups, relate_add_mult]
    if d == 2:
        opts = [build_from_total, commutative, rows_missing, word,
                count_groups, mult_expression_groups, mult_expression_array,
                relate_add_mult_groups, relate_add_mult, make_array_model,
                repeated_addition_array]
    elif d == 1:
        opts += [mult_expression_groups, mult_expression_array]
    return pick(opts)()


def _table_q(t, d):
    """Shared engine for the times-table skills."""
    d = _lvl(d)
    if d == 0:
        k = random.randint(1, 6)
    elif d == 1:
        k = random.randint(2, 12)
    else:
        k = random.randint(6, 12)
    p = t * k

    def bare():
        if random.random() < 0.5:
            return _numq("Work out %d × %d." % (t, k), p,
                         ["%d × %d = %d." % (t, k, p)])
        return _numq("Work out %d × %d." % (k, t), p,
                     ["%d × %d = %d." % (k, t, p)])

    def array_build():
        rows, cols = (t, k) if (t <= 10 and k <= 12) else (k, t)
        if rows > 10:
            rows, cols = cols, rows
        return _arrayq("Build an array of %d rows of %d to show %d × %d, then type "
                       "the total." % (rows, cols, t, k), rows, cols,
                       ["%d × %d = %d." % (rows, cols, p)])

    def missing():
        return _numq("Find the missing number:  %d × ___ = %d" % (t, p), k,
                     ["%d ÷ %d = %d." % (p, t, k)])

    def divide():
        return _numq("Work out %d ÷ %d." % (p, t), k,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (t, k, p, p, t, k)])

    def count_line():
        jumps = "jump" if k == 1 else "jumps"
        return _lineq("Count in %ds. Start at 0 and make %d %s of %d. Mark where "
                      "you land." % (t, k, jumps, t), p, [0],
                      ["%d %s of %d is %d × %d = %d." % (k, jumps, t, k, t, p)])

    def word():
        who = pick(NAMES)
        return _numq("%s has %d %s with %d apples in each bag. How many apples "
                     "altogether?" % (who, k, "bag" if k == 1 else "bags", t), p,
                     ["%d × %d = %d apples." % (k, t, p)], unit="apples")

    def compare():
        k2 = random.randint(2, 12)
        while t * k2 == p:
            k2 = random.randint(2, 12)
        big = max(p, t * k2)
        return _numq("Which is more, %d × %d or %d × %d? Type the larger product."
                     % (t, k, t, k2), big,
                     ["%d × %d = %d and %d × %d = %d." % (t, k, p, t, k2, t * k2),
                      "The larger product is %d." % big])

    opts = [bare, array_build, count_line, word, divide]
    if d == 0:
        opts = [bare, array_build, array_build, count_line, word]
    elif d == 2:
        opts = [bare, array_build, missing, divide, compare, count_line]
    return pick(opts)()


@skill("Y3.4.b", "The 3 times table", S4)
def _(d=1):
    return _table_q(3, d)


@skill("Y3.4.c", "The 4 times table", S4)
def _(d=1):
    return _table_q(4, d)


@skill("Y3.4.d", "The 8 times table", S4)
def _(d=1):
    return _table_q(8, d)


@skill("Y3.4.e", "The 2, 5 and 10 times tables", S4)
def _(d=1):
    return _table_q(pick([2, 5, 10]), d)


@skill("Y3.4.f", "Division as sharing", S4)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        g = pick([2, 3, 4, 5]); per = random.randint(2, 5)
    elif d == 1:
        g = pick([2, 3, 4, 5, 8]); per = random.randint(2, 9)
    else:
        g = pick([3, 4, 6, 8]); per = random.randint(5, 10)
    total = g * per

    def share_word():
        who = pick(NAMES)
        return _numq("%s shares %d sweets equally between %d children. How many "
                     "does each child get?" % (who, total, g), per,
                     ["%d ÷ %d = %d sweets each." % (total, g, per)], unit="sweets")

    def group_word():
        return _numq("%d cakes are put into boxes of %d. How many boxes are needed?"
                     % (total, per), g,
                     ["%d ÷ %d = %d boxes." % (total, per, g)], unit="boxes")

    def array_model():
        # the sharing is the question (total ÷ children), the array its picture: one row per child
        rows, cols = g, per
        return _arrayreadq("%d sweets are shared equally between %d children. The array shows one row for each "
                           "child. How many sweets does each child get?" % (total, rows),
                           rows, cols, cols,
                           ["%d sweets in %d equal rows." % (total, rows),
                            "%d ÷ %d = %d sweets each." % (total, rows, cols)])

    def bare():
        return _numq("Work out %d ÷ %d." % (total, g), per,
                     ["%d × %d = %d, so %d ÷ %d = %d."
                      % (g, per, total, total, g, per)])

    def missing():
        return _numq("Find the missing number:  %d ÷ ___ = %d" % (total, per), g,
                     ["%d ÷ %d = %d." % (total, per, g)])

    def two_step():
        extra = random.randint(1, 3)
        return _numq("%d sweets are shared equally between %d children. Then each "
                     "child is given %d more. How many does each child have now?"
                     % (total, g, extra), per + extra,
                     ["%d ÷ %d = %d." % (total, g, per),
                      "%d + %d = %d sweets each." % (per, extra, per + extra)],
                     unit="sweets")

    def divide_counting_groups():
        gg, pp = min(g, 8), min(per, 10)
        return _egq("Divide by making equal groups: put the %d counters into "
                    "equal groups of %d. How many equal groups are there?"
                    % (gg * pp, pp), gg, pp, gg,
                    ["Count the groups: there are %d." % gg,
                     "%d ÷ %d = %d groups." % (gg * pp, pp, gg)])

    def write_division_sentence():
        gg, pp = min(g, 8), min(per, 10)
        return _egq("Share the %d counters into %d equal groups, then complete the "
                    "division sentence:  %d ÷ %d = ___ . Type the "
                    "answer." % (gg * pp, gg, gg * pp, gg), gg, pp, pp,
                    ["Each equal group holds %d counters." % pp,
                     "%d ÷ %d = %d." % (gg * pp, gg, pp)])

    opts = [share_word, group_word, array_model, bare,
            divide_counting_groups, write_division_sentence]
    if d == 2:
        opts = [share_word, group_word, array_model, missing, two_step,
                divide_counting_groups, write_division_sentence]
    return pick(opts)()


@skill("Y3.4.g", "Divide using the 3, 4 and 8 times tables", S4)
def _(d=1):
    d = _lvl(d)
    t = pick([3, 4, 8])
    if d == 0:
        k = random.randint(2, 6)
    elif d == 1:
        k = random.randint(2, 12)
    else:
        k = random.randint(6, 12)
    p = t * k

    def bare():
        return _numq("Work out %d ÷ %d." % (p, t), k,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (t, k, p, p, t, k)])

    def bare_other():
        # dividing by the other factor still uses this table: 56 ÷ 7 is 8 because 7 × 8 = 56
        return _numq("Work out %d ÷ %d, using the %d times table." % (p, k, t), t,
                     ["In the %d times table, %d × %d = %d." % (t, k, t, p),
                      "So %d ÷ %d = %d." % (p, k, t)])

    def array_model():
        # a division to work out (the array its picture), not a total to count
        rows, cols = t, k
        return _arrayreadq("%d counters are put into %d equal rows, as the array shows. How many counters are in "
                           "each row?" % (p, rows), rows, cols, cols,
                           ["%d ÷ %d = %d." % (p, rows, cols),
                            "Check: %d rows of %d = %d." % (rows, cols, p)])

    def missing():
        return _numq("Find the missing number:  ___ ÷ %d = %d" % (t, k), p,
                     ["%d × %d = %d." % (t, k, p)])

    def word():
        return _numq("%d children are put into teams of %d. How many teams are "
                     "there?" % (p, t), k,
                     ["%d ÷ %d = %d teams." % (p, t, k)], unit="teams")

    def check_inverse():
        return _numq("%d ÷ %d = ___ . Work it out, then check by multiplying."
                     % (p, t), k,
                     ["%d ÷ %d = %d." % (p, t, k),
                      "Check: %d × %d = %d ✓." % (k, t, p)])

    opts = [bare, array_model, array_model, word, check_inverse]
    if d == 2:
        opts = [bare, bare_other, array_model, missing, check_inverse, word]
    return pick(opts)()


@skill("Y3.4.h", "Multiplication and division fact families", S4)
def _(d=1):
    d = _lvl(d)
    a = pick([2, 5, 10]) if d == 0 else pick([3, 4, 8])
    b = random.randint(2, 6) if d == 0 else random.randint(2, 12)
    p = a * b

    def mul_to_div():
        return _numq("If %d × %d = %d, what is %d ÷ %d?" % (a, b, p, p, b), a,
                     ["Same fact family: %d ÷ %d = %d." % (p, b, a)])

    def div_to_mul():
        return _numq("If %d ÷ %d = %d, what is %d × %d?" % (p, a, b, b, a), p,
                     ["Same fact family: %d × %d = %d." % (b, a, p)])

    def array_family():
        rows, cols = a, b
        return _arrayq("Build an array of %d rows of %d. It shows the whole fact "
                       "family. Type the total number of counters." % (rows, cols),
                       rows, cols,
                       ["%d × %d = %d." % (rows, cols, p),
                        "So %d ÷ %d = %d and %d ÷ %d = %d too."
                        % (p, rows, cols, p, cols, rows)])

    def missing_member():
        return _numq("Complete the fact family:  %d × ___ = %d" % (a, p), b,
                     ["%d ÷ %d = %d." % (p, a, b)])

    def word():
        who = pick(NAMES)
        return _numq("%s knows %d × %d = %d. Use that fact to work out %d ÷ %d."
                     % (who, a, b, p, p, a), b,
                     ["%d ÷ %d = %d." % (p, a, b)])

    def fourth_fact():
        return _numq("Three facts in a family are %d × %d = %d, %d × %d = %d and "
                     "%d ÷ %d = %d. What is %d ÷ %d?"
                     % (a, b, p, b, a, p, p, a, b, p, b), a,
                     ["The fourth fact is %d ÷ %d = %d." % (p, b, a)])

    def relate_groups():
        gg = random.randint(2, 6)
        pp = random.randint(2, 9)
        return _egq("%d × %d = %d. Share the %d counters into %d equal groups and use "
                    "the multiplication to complete the related division:  %d ÷ %d = ___"
                    % (gg, pp, gg * pp, gg * pp, gg, gg * pp, gg), gg, pp, pp,
                    ["Multiplication and division are related: %d × %d = %d."
                     % (gg, pp, gg * pp),
                     "So %d ÷ %d = %d." % (gg * pp, gg, pp)])

    opts = [mul_to_div, div_to_mul, array_family, word, relate_groups]
    if d == 2:
        opts = [mul_to_div, div_to_mul, array_family, missing_member,
                fourth_fact, word, relate_groups]
    return pick(opts)()


@skill("Y3.4.i", "Properties of multiplication", S4)
def _(d=1):
    d = _lvl(d)

    def commutative():
        # one factor from the Year 3 tables (2, 3, 4, 5, 8, 10), the other up to 12
        a = pick([2, 5, 10] if d == 0 else [2, 3, 4, 5, 8, 10])
        b = random.randint(2, (6, 9, 12)[d])
        if random.random() < 0.5:
            a, b = b, a
        return _numq("%d × %d = %d. So what is %d × %d?" % (a, b, a * b, b, a), a * b,
                     ["Multiplication can be done in any order: %d × %d = %d."
                      % (b, a, a * b)])

    def comm_array():
        a = random.randint(2, (4, 6, 8)[d]); b = random.randint(3, (6, 9, 10)[d])
        while a not in (2, 3, 4, 5, 8) and b not in (3, 4, 5, 8, 10):   # keep one Year 3 table
            a = random.randint(2, (4, 6, 8)[d]); b = random.randint(3, (6, 9, 10)[d])
        return _arrayq("Show that %d × %d = %d × %d: build an array of %d rows of "
                       "%d and type the total." % (a, b, b, a, b, a), b, a,
                       ["Turning the array does not change the total.",
                        "%d × %d = %d." % (b, a, a * b)])

    def associative():
        if d == 0:
            a, b, c = random.randint(2, 3), random.randint(2, 3), random.randint(2, 4)
        elif d == 1:
            a, b, c = random.randint(2, 5), random.randint(2, 4), random.randint(2, 5)
        else:
            a, b, c = random.randint(3, 5), random.randint(3, 5), random.randint(3, 6)
        return _numq("Work out %d × %d × %d." % (a, b, c), a * b * c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d × %d = %d." % (a * b, c, a * b * c)])

    def by_one_zero():
        a = random.randint(3, 12)
        if random.random() < 0.5:
            return _numq("Work out %d × 1." % a, a,
                         ["Multiplying by 1 leaves the number unchanged: %d." % a])
        return _numq("Work out %d × 0." % a, 0,
                     ["Multiplying by 0 always gives 0."])

    def distributive():
        a = random.randint(11, 19) if d < 2 else random.randint(21, 29)
        b = random.randint(3, 6) if d < 2 else random.randint(4, 8)
        return _numq("Use partitioning: %d × %d = (%d × %d) + (%d × %d) = ___"
                     % (a, b, a // 10 * 10, b, a % 10, b), a * b,
                     ["%d × %d = %d and %d × %d = %d."
                      % (a // 10 * 10, b, a // 10 * 10 * b, a % 10, b, (a % 10) * b),
                      "%d + %d = %d." % (a // 10 * 10 * b, (a % 10) * b, a * b)])

    def scaling():
        a = random.randint(2, 9); b = random.randint(2, 6 if d < 2 else 10)
        return _numq("%d × %d = %d. What is %d × %d?"
                     % (a, b, a * b, a, b * 2), a * b * 2,
                     ["Doubling one factor doubles the product: %d × 2 = %d."
                      % (a * b, a * b * 2)])

    def terms():
        """Addition, subtraction, multiplication and division terms."""
        a = random.randint(3, 9)
        b = random.randint(2, 9)
        which = pick(["sum", "difference", "product", "quotient"])
        if which == "sum":
            sent, ans = "%d + %d = %d" % (a, b, a + b), "sum"
        elif which == "difference":
            sent, ans = "%d − %d = %d" % (a + b, b, a), "difference"
        elif which == "product":
            sent, ans = "%d × %d = %d" % (a, b, a * b), "product"
        else:
            sent, ans = "%d ÷ %d = %d" % (a * b, b, a), "quotient"
        return _wordq("Maths terms: in the number sentence %s, what is the answer "
                      "called? Type sum, difference, product or quotient." % sent,
                      ans,
                      ["An addition gives a sum, a subtraction gives a difference, "
                       "a multiplication gives a product and a division gives a "
                       "quotient.",
                       "So the answer here is called the %s." % ans],
                      placeholder="sum / difference / product / quotient")

    opts = [commutative, comm_array, comm_array, associative, by_one_zero, terms]
    if d == 2:
        opts = [commutative, comm_array, associative, distributive, scaling,
                distributive, terms]
    return pick(opts)()


# ------------------------------------------------------------------ 3.5 ------
@skill("Y3.5.a", "Multiply a 2-digit number by a 1-digit number", S5)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(11, 19); b = random.randint(2, 4)
    elif d == 1:
        a = random.randint(12, 39); b = random.randint(3, 8)
    else:
        a = random.randint(24, 49); b = random.randint(6, 9)
    tens, ones = (a // 10) * 10, a % 10
    part = ["Partition: %d × %d = %d and %d × %d = %d."
            % (tens, b, tens * b, ones, b, ones * b),
            "%d + %d = %d." % (tens * b, ones * b, a * b)]

    def bare():
        return _numq("Work out %d × %d." % (a, b), a * b, part)

    def blocks():
        if a * b > 999:
            return _numq("Work out %d × %d." % (a, b), a * b, part)
        return _btq("Work out %d × %d by partitioning, then build the answer with "
                    "base ten blocks." % (a, b), a * b, part)

    def array_model():
        rows, cols = b, a
        if cols > 12:
            return _numq("An array has %d rows of %d. How many counters altogether?"
                         % (b, a), a * b, part)
        return _arrayq("Build an array of %d rows of %d to show %d × %d, then type "
                       "the total." % (rows, cols, a, b), rows, cols,
                       ["%d × %d = %d." % (rows, cols, a * b)])

    def word():
        who = pick(NAMES)
        return _numq("%s buys %d packets of cards. Each packet holds %d cards. "
                     "How many cards altogether?" % (who, b, a), a * b,
                     ["%d × %d = %d cards." % (b, a, a * b)], unit="cards")

    def missing():
        return _numq("Find the missing number:  %d × ___ = %d" % (a, a * b), b,
                     ["%d ÷ %d = %d." % (a * b, a, b)])

    def two_step():
        c = random.randint(10, 40)
        return _numq("Work out %d × %d, then add %d." % (a, b, c), a * b + c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d + %d = %d." % (a * b, c, a * b + c)])

    opts = [bare, blocks, array_model, word, blocks]
    if d == 2:
        opts = [bare, blocks, missing, two_step, word, array_model]
    return pick(opts)()


@skill("Y3.5.b", "Divide a 2-digit number by a 1-digit number", S5)
def _(d=1):
    d = _lvl(d)
    # Year 3 divides a 2-digit number by a 1-digit one beyond the tables: the easy tier is a table fact
    # (48 ÷ 4), then a 2-digit answer with no exchange (69 ÷ 3), then one with an exchange of a ten (72 ÷ 3)
    if d == 0:
        b = random.randint(2, 5); k = random.randint(3, 12)
    else:
        while True:
            b = pick([2, 3, 4, 5]) if d == 1 else pick([3, 4, 5, 6])
            k = random.randint(11 if d == 1 else 13, 99 // b)
            if ((b * k) // 10 % b == 0) == (d == 1) and b * k % 10:
                break
    a = b * k
    tens = (a // 10) * 10 if d == 1 else (a // 10 // b) * b * 10
    split = ["Split %d into %d and %d." % (a, tens, a - tens),
             "%d ÷ %d = %d and %d ÷ %d = %d." % (tens, b, tens // b, a - tens, b, (a - tens) // b),
             "%d + %d = %d, so %d ÷ %d = %d." % (tens // b, (a - tens) // b, k, a, b, k)]
    fact = ["%d ÷ %d = %d (because %d × %d = %d)." % (a, b, k, b, k, a)]
    why = fact if d == 0 else split

    def bare():
        return _numq("Work out %d ÷ %d." % (a, b), k, why)

    def array_model():
        # a division to work out with the array as its picture (one row for each share), the easy tier only
        return _arrayreadq("%d counters are shared into %d equal rows, as the array shows. How many counters are "
                           "in each row?" % (a, b), b, k, k, fact)

    def word():
        return _numq("%d pencils are shared equally between %d pots. How many "
                     "pencils in each pot?" % (a, b), k,
                     why[:-1] + ["%d ÷ %d = %d pencils." % (a, b, k)], unit="pencils")

    def missing():
        return _numq("Find the missing number:  ___ ÷ %d = %d" % (b, k), a,
                     ["%d × %d = %d." % (b, k, a)])

    def check_inverse():
        return _numq("%d ÷ %d = ___ . Work it out, then check by multiplying."
                     % (a, b), k,
                     why + ["Check: %d × %d = %d ✓." % (k, b, a)])

    def chunks():
        # repeated subtraction in big steps: take away 10 lots of b while you can, then the rest
        tens_lots = k // 10
        left = a - tens_lots * 10 * b
        steps = ", ".join("%d − %d = %d" % (a - i * 10 * b, 10 * b, a - (i + 1) * 10 * b) for i in range(tens_lots))
        return _numq("Work out %d ÷ %d by taking away 10 lots of %d (%d) at a time: %s. How many %ds are there in "
                     "%d altogether?" % (a, b, b, 10 * b, steps, b, a), k,
                     ["That is %d %s of 10, so %d %ds so far." % (tens_lots, "lot" if tens_lots == 1 else "lots",
                                                                  10 * tens_lots, b),
                      "%d is %d more %ds (%d × %d = %d)." % (left, left // b, b, left // b, b, left),
                      "%d + %d = %d, so %d ÷ %d = %d." % (10 * tens_lots, left // b, k, a, b, k)])

    def repeated_subtraction():
        chain = "%d − %d = %d" % (a, b, a - b)
        return _numq("Divide %d by %d using repeated subtraction. Start at %d and "
                     "keep subtracting %d until you reach 0 (%s, …). How many times "
                     "do you subtract %d?" % (a, b, a, b, chain, b), k,
                     ["Subtracting %d again and again from %d reaches 0 after %d "
                      "steps." % (b, a, k),
                      "Repeated subtraction is division: %d ÷ %d = %d."
                      % (a, b, k)], unit="times")

    # repeated subtraction one step at a time and the array stay with the table facts; a 2-digit answer is
    # worked by partitioning or in chunks of ten lots
    opts = [bare, array_model, word, check_inverse, repeated_subtraction]
    if d >= 1:
        opts = [bare, chunks, missing, check_inverse, word, chunks]
    return pick(opts)()


@skill("Y3.5.c", "Division with remainders", S5)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        b = random.randint(3, 5); k = random.randint(2, 6)
    elif d == 1:
        b = random.randint(3, 8); k = random.randint(3, 11)
    else:
        b = random.randint(5, 9); k = random.randint(6, 12)
    r = random.randint(1, b - 1)
    a = b * k + r

    def remainder_only():
        return _numq("Work out %d ÷ %d. Write the remainder only." % (a, b), r,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r)],
                     placeholder="the remainder")

    def quotient_only():
        return _numq("Work out %d ÷ %d. Write the whole-number part of the answer "
                     "(ignore the remainder)." % (a, b), k,
                     ["%d × %d = %d, and %d left over." % (b, k, b * k, r)],
                     placeholder="whole number part")

    def array_model():
        rows, cols = b, k
        return _arrayq("%d counters are shared equally into %d rows, with as many "
                       "as possible in each row. Build the array (the leftovers "
                       "stay out), then type how many counters are in the array."
                       % (a, b), rows, cols,
                       ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                        "The full rows hold %d counters." % (b * k)])

    def word_sweets():
        return _numq("%d sweets are shared equally between %d children. How many "
                     "sweets are left over?" % (a, b), r,
                     ["%d ÷ %d = %d each, remainder %d." % (a, b, k, r)],
                     unit="sweets")

    def word_boxes():
        return _numq("%d eggs are packed into boxes of %d. How many boxes can be "
                     "filled completely?" % (a, b), k,
                     ["%d ÷ %d = %d remainder %d, so %d full boxes."
                      % (a, b, k, r, k)], unit="boxes")

    def word_need():
        return _numq("%d children go on a trip. Each minibus holds %d children. "
                     "How many minibuses are needed so everyone travels?" % (a, b),
                     k + 1,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                      "The %d left over still need a bus, so %d buses."
                      % (r, k + 1)], unit="minibuses")

    opts = [remainder_only, quotient_only, array_model, array_model, word_sweets,
            word_boxes]
    if d == 2:
        opts = [remainder_only, quotient_only, array_model, array_model, word_need,
                word_boxes]
    return pick(opts)()


@skill("Y3.5.d", "Multiplication word problem", S5)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        n = random.randint(2, 5); per = random.randint(2, 6)
    elif d == 1:
        n = random.randint(3, 9); per = random.randint(3, 12)
    else:
        n = random.randint(4, 9); per = random.randint(6, 12)

    def pencils():
        who = pick(NAMES)
        return _numq("%s buys %d boxes of pencils. Each box holds %d pencils. "
                     "How many pencils in total?" % (who, n, per), n * per,
                     ["'Each' box holds %d — the same number %d times, so multiply." % (per, n),
                      "%d × %d = %d pencils." % (n, per, n * per)], unit="pencils")

    def money_word():
        cost = random.randint(4, 9) * 10
        return _numq("Each notebook costs %s. How much do %d notebooks cost, "
                     "in pence?" % (money(cost), n), cost * n,
                     ["'Each' one costs %dp — the same price %d times, so multiply." % (cost, n),
                      "%d × %d = %dp." % (cost, n, cost * n)], unit="p")

    def array_model():
        rows, cols = (n, per) if per <= 12 and n <= 10 else (per, n)
        return _arrayq("A tray has %d rows of %d cakes. Build the array and type "
                       "how many cakes there are." % (rows, cols), rows, cols,
                       ["'%d rows of %d' means the same number in every row, so multiply." % (rows, cols),
                        "%d × %d = %d cakes." % (rows, cols, rows * cols)])

    def picto():
        # pictures × the key: the multiplication (adding three totals up was an addition question)
        key = pick([2, 5, 10]) if d == 0 else pick([3, 4, 5, 8])
        cats = ["Class 3A", "Class 3B", "Class 3C"]
        vals = [key * random.randint(2, 7 if d == 0 else 9) for _ in cats]
        i = random.randrange(3)
        return _pictq("The pictogram shows medals won. Each picture means %d medals. How many medals did %s win?"
                      % (key, cats[i]), cats, vals, key, "medal", vals[i],
                      ["%s has %d pictures, and each one means %d medals, so multiply." % (cats[i], vals[i] // key, key),
                       "%d × %d = %d medals." % (vals[i] // key, key, vals[i])])

    def two_step():
        extra = random.randint(5, 20)
        return _numq("%d bags each hold %d marbles. There are also %d loose "
                     "marbles. How many marbles altogether?" % (n, per, extra),
                     n * per + extra,
                     ["'Each' bag holds %d, so multiply; then add the loose ones: 'altogether' means "
                      "all of them." % per,
                      "%d × %d = %d." % (n, per, n * per),
                      "%d + %d = %d marbles." % (n * per, extra, n * per + extra)],
                     unit="marbles")

    def compare():
        n2 = random.randint(2, 9); per2 = random.randint(3, 12)
        while n2 * per2 == n * per:
            per2 = random.randint(3, 12)
        big = max(n * per, n2 * per2)
        return _numq("Box A holds %d packs of %d. Box B holds %d packs of %d. "
                     "Which box holds more? Type the larger number of items."
                     % (n, per, n2, per2), big,
                     ["Box A: %d × %d = %d." % (n, per, n * per),
                      "Box B: %d × %d = %d." % (n2, per2, n2 * per2)])

    def strip_word():
        who = pick(NAMES)
        thing = pick(["baskets", "trays", "shelves", "crates"])
        return _stripq("Use the strip model to solve this multiplication word "
                       "problem. %s fills %d %s and each one holds %d apples. How "
                       "many apples altogether?" % (who, n, thing, per),
                       {"mode": "equal_parts", "parts": int(n),
                        "partLabel": str(per), "totalLabel": "?",
                        "unknown": "total"},
                       n * per,
                       ["'Each one holds %d' means %d equal parts of %d, so multiply." % (per, n, per),
                        "The strip has %d equal parts of %d." % (n, per),
                        "%d × %d = %d apples." % (n, per, n * per)])

    opts = [pencils, money_word, array_model, picto, strip_word]
    if d == 2:
        opts = [two_step, two_step, compare, picto, money_word, array_model,
                strip_word]
    return pick(opts)()


@skill("Y3.5.e", "Division word problem", S5)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        groups = random.randint(2, 5); per = random.randint(2, 5)
    elif d == 1:
        groups = random.randint(3, 8); per = random.randint(3, 9)
    else:
        groups = random.randint(4, 9); per = random.randint(5, 10)
    total = groups * per

    def teams():
        return _numq("%d children are put into teams of %d. How many teams are "
                     "there?" % (total, per), groups,
                     ["'Teams of %d' means %d in every team: how many %ds fit into %d? Divide."
                      % (per, per, per, total),
                      "%d ÷ %d = %d teams." % (total, per, groups)], unit="teams")

    def sharing():
        who = pick(NAMES)
        return _numq("%s shares %d stickers equally between %d friends. How many "
                     "stickers does each friend get?" % (who, total, groups), per,
                     ["'Shares equally' means every friend gets the same, so divide.",
                      "%d ÷ %d = %d stickers." % (total, groups, per)],
                     unit="stickers")

    def money_word():
        each = random.randint(3, 9) * 10
        tot = each * groups
        return _numq("%s is shared equally between %d children. How much does each "
                     "child get, in pence?" % (money(tot), groups), each,
                     ["'Shared equally' means every child gets the same, so divide.",
                      "%d ÷ %d = %dp each." % (tot, groups, each)], unit="p")

    def array_model():
        # the division is the question; the array (one row for each team) is its picture
        rows, cols = groups, per
        return _arrayreadq("%d children are put into %d equal teams. The array shows one row for each team. How "
                           "many children are in each team?" % (total, rows), rows, cols, cols,
                           ["'Equal teams' means every team gets the same, so divide.",
                            "%d ÷ %d = %d children in each team." % (total, rows, cols)])

    def chart():
        cats = ["Apples", "Pears", "Plums"]
        vals = [total, random.randint(10, 40), random.randint(10, 40)]
        return _barq("The chart shows fruit collected. The apples are packed into "
                     "bags of %d. How many bags of apples are there?" % per,
                     cats, vals, groups,
                     ["Apples: %d." % total,
                      "%d ÷ %d = %d bags." % (total, per, groups)])

    def two_step_clean():
        eaten = random.randint(1, max(1, per - 1))
        return _numq("%d biscuits are shared equally between %d children. One child "
                     "eats %d of theirs. How many biscuits does that child have "
                     "left?" % (total, groups, eaten), per - eaten,
                     ["'Shared equally' means divide; 'eats' and 'left' mean take away, so subtract.",
                      "%d ÷ %d = %d each." % (total, groups, per),
                      "%d − %d = %d left." % (per, eaten, per - eaten)],
                     unit="biscuits")

    def equal_groups_word():
        gg, pp = min(groups, 8), min(per, 10)
        who = pick(NAMES)
        return _egq("Use the counters to solve this division word problem. %s "
                    "puts %d conkers into equal groups of %d. How many equal groups "
                    "does %s make?" % (who, gg * pp, pp, who), gg, pp, gg,
                    ["Make groups of %d: there are %d groups." % (pp, gg),
                     "%d ÷ %d = %d groups." % (gg * pp, pp, gg)], answer_type="int")

    def strip_word():
        who = pick(NAMES)
        return _stripq("Use the strip model to solve this division word problem. %s "
                       "shares %d marbles equally between %d friends. How many "
                       "marbles does each friend get?" % (who, total, groups),
                       {"mode": "equal_parts", "parts": int(groups),
                        "partLabel": "?", "totalLabel": str(total),
                        "unknown": "part"},
                       per,
                       ["'Shares equally' means every friend gets the same, so divide.",
                        "The strip of %d is split into %d equal parts."
                        % (total, groups),
                        "%d ÷ %d = %d marbles each." % (total, groups, per)])

    opts = [teams, sharing, money_word, array_model, chart,
            equal_groups_word, strip_word]
    if d == 2:
        opts = [teams, sharing, array_model, chart, two_step_clean, money_word,
                equal_groups_word, strip_word]
    return pick(opts)()


@skill("Y3.5.f", "Mixed × and ÷ (missing number)", S5)
def _(d=1):
    d = _lvl(d)
    a = pick([2, 5, 10]) if d == 0 else pick([3, 4, 8])
    b = random.randint(*{0: (2, 6), 1: (2, 12), 2: (6, 12)}[d])
    p = a * b

    def miss_factor():
        return _numq("Find the missing number:  %d × ___ = %d" % (a, p), b,
                     ["%d ÷ %d = %d." % (p, a, b)])

    def miss_dividend():
        return _numq("Find the missing number:  ___ ÷ %d = %d" % (a, b), p,
                     ["%d × %d = %d." % (a, b, p)])

    def miss_divisor():
        return _numq("Find the missing number:  %d ÷ ___ = %d" % (p, b), a,
                     ["%d ÷ %d = %d." % (p, b, a)])

    def array_model():
        # a missing number, as the skill says, with the array as its picture
        rows, cols = a, b
        return _arrayreadq("The array has %d counters in %d equal rows. Complete:  %d × ___ = %d"
                           % (p, rows, rows, p), rows, cols, cols,
                           ["%d ÷ %d = %d." % (p, rows, cols),
                            "So %d × %d = %d." % (rows, cols, p)])

    def word():
        who = pick(NAMES)
        return _numq("%s puts %d shells into equal rows of %d. How many rows are "
                     "there?" % (who, p, a), b,
                     ["%d ÷ %d = %d rows." % (p, a, b)], unit="rows")

    opts = [miss_factor, miss_dividend, array_model, array_model, word]
    if d == 2:
        opts = [miss_factor, miss_dividend, miss_divisor, array_model, word,
                array_model]
    return pick(opts)()
