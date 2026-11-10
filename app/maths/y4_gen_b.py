# dev/app/logic/y4_gen_b.py — Year 4 generators: strands 4.2 and 4.3
#
# 4.2  Addition & subtraction with up to 4 digits (mental multiples, column
#      methods including exchanging across zeros, three-or-more addends,
#      missing numbers / missing digits / balanced equations, word problems,
#      input-output and data tables).
# 4.3  Multiplication & division facts to 12 x 12 (equal groups and arrays,
#      tables, fact families, multiples and factor pairs, divisibility rules,
#      square numbers, the laws of arithmetic, products of three numbers).
#
# Difficulty `d`: 0 = easy, 1 = core (year-expected), 2 = stretch.
# Every generator offers 8+ genuinely different framings and routes a large
# share of them through the interactive components.
import random
from .maths_engine import skill, pick, NAMES, n_words, money, ordinal

S2 = "4.2 Addition & subtraction (4-digit)"
S3 = "4.3 Multiplication & division facts"

_OBJ = ["stickers", "marbles", "conkers", "beads", "shells", "cards", "buttons",
        "acorns", "stamps", "counters"]
_PLACES = ["Redhill", "Oakfield", "Larkmoor", "Westbury", "Fenton", "Millbrook",
           "Ashgrove", "Northolt"]


# =============================================================== helpers =====
def _lvl(d):
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


def _wordq(prompt, answer, solution, placeholder=None):
    return _numq(prompt, answer, solution, placeholder=placeholder,
                 answer_type="str", text=True)


def _setq(prompt, values, solution, placeholder="e.g. 4, 8, 12"):
    """Order-insensitive list of numbers."""
    vals = sorted(int(v) for v in values)
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in vals),
            "answer_type": "set", "solution": solution}


def _line_spec(vals, prefer=None):
    """A number line that certainly contains every value, with a step that
    divides all of them so the marker can land exactly on the answer."""
    vals = [int(v) for v in vals]
    lo_v, hi_v = min(vals), max(vals)
    span = hi_v - lo_v
    pool = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000]
    if prefer:
        pool = sorted(set(pool + [int(prefer)]))
    cand = [s for s in pool if all(v % s == 0 for v in vals)]
    if not cand:
        cand = [1]
    step = cand[-1]
    for s in cand:
        if span // s <= 20:
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


def _lineq(prompt, target, others, solution, prefer=None):
    spec = _line_spec(list(others) + [target], prefer)
    return {"prompt": prompt, "component": "number_line", "spec": spec,
            "answer": int(target), "answer_type": "num",
            "tolerance": spec["step"] / 2.0, "solution": solution}


def _fit(r, c):
    """Orient (rows, cols) so the array component can actually build it."""
    r, c = int(r), int(c)
    if r <= 10 and c <= 12:
        return r, c
    if c <= 10 and r <= 12:
        return c, r
    return None


def _arrayq(prompt, rows, cols, solution):
    """Array build. Falls back to a typed box when the array is too big."""
    rows, cols = int(rows), int(cols)
    if _fit(rows, cols) != (rows, cols):
        prompt = prompt.replace("Build ", "Picture ")
        return _numq(prompt, rows * cols, solution)
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "build",
                     "maxRows": min(10, max(6, rows + 2)),
                     "maxCols": min(12, max(6, cols + 2)),
                     "targetRows": rows, "targetCols": cols},
            "answer": rows * cols, "answer_type": "int", "solution": solution}


def _egq(prompt, groups, per, answer, solution, answer_type="int"):
    """equal_groups (read): G rings holding P counters each, plus a typed box."""
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "read", "groups": int(groups), "per": int(per)},
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _egbuildq(prompt, groups, per, solution):
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "build", "maxGroups": 8, "maxPer": 10,
                     "targetGroups": int(groups), "targetPer": int(per)},
            "answer": int(groups) * int(per), "answer_type": "int",
            "solution": solution}


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


def _stripq(prompt, spec, answer, solution):
    return {"prompt": prompt, "component": "strip_model", "spec": spec,
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _areaq(prompt, rows, cols, solution):
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "read_area", "rows": int(rows), "cols": int(cols)},
            "answer": int(rows) * int(cols), "answer_type": "int",
            "solution": solution}


def _ioq(prompt, rows, missing, answer, solution, rule=None, placeholder=None,
         answer_type="int"):
    """input/output table. `rows` = [[in, out], ...]; `missing` = index of the
    row whose Out cell is blanked (None = ask for the rule itself)."""
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _io_rows(lo, hi, delta, n=4, mult=1):
    """n distinct In values in [lo, hi] (multiples of `mult`) with Out = In + delta."""
    lo, hi = int(lo), int(hi)
    pool = [v for v in range(lo, hi + 1) if v % mult == 0]
    if len(pool) < n:
        pool = list(range(lo, hi + 1))
    n = min(n, len(pool))
    ins = sorted(random.sample(pool, n))
    return [[i, i + delta] for i in ins]


def _dtq(prompt, headers, rows, answer, solution, missing=None, caption=None,
         answer_type="int", placeholder=None):
    """data_table. `rows` = list of lists of cell strings; `missing` = [r, c]."""
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        mr, mc = int(missing[0]), int(missing[1])
        spec["missing"] = [mr, mc]
        spec["rows"][mr][mc] = ""          # never show the hidden value
    if caption:
        spec["caption"] = caption
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _com(n):
    """Plain digits — no thousands separators (answers are typed as digits)."""
    return "%d" % int(n)


def _pv(count, name):
    """'3 hundreds' / '1 hundred' — `name` is the plural place-value word."""
    count = int(count)
    return "%d %s" % (count, name if count != 1 else name[:-1])


def _digits4(n):
    n = int(n)
    return (n // 1000, (n // 100) % 10, (n // 10) % 10, n % 10)


# --- structured 4-digit pair builders ---------------------------------------
def _pair_add4(d=1, carry=True):
    """Two numbers whose column addition does (or does not) need regrouping."""
    d = _lvl(d)
    lo, hi = (1000, 4999) if d == 0 else ((1000, 8999) if d == 1 else (2000, 9499))
    while True:
        a = random.randint(lo, hi)
        b = random.randint(1000 if d else 100, hi - 1000)
        if a + b > 9999:
            continue
        da, db = _digits4(a), _digits4(b)
        carries = [da[i] + db[i] >= 10 for i in (1, 2, 3)]
        if carry and any(carries):
            if d == 2 and sum(carries) < 2:
                continue
            return a, b
        if not carry and not any(carries):
            return a, b


def _pair_sub4(d=1, exchange=True):
    d = _lvl(d)
    lo, hi = (2000, 5999) if d == 0 else ((2000, 9499) if d == 1 else (3000, 9899))
    while True:
        a = random.randint(lo, hi)
        b = random.randint(1000 if d else 200, a - 500)
        da, db = _digits4(a), _digits4(b)
        need = [da[i] < db[i] for i in (1, 2, 3)]
        if exchange and any(need):
            if d == 2 and sum(need) < 2:
                continue
            return a, b
        if not exchange and not any(need):
            return a, b


def _pair_sub_zeros(d=1):
    """a has zeros that force exchanging across them (e.g. 5000 − 2346)."""
    d = _lvl(d)
    style = pick(["thousand", "hundreds", "tens"]) if d else "thousand"
    if style == "thousand":
        a = random.randint(2, 9) * 1000
    elif style == "hundreds":
        a = random.randint(2, 9) * 1000 + random.randint(1, 9)
    else:
        a = random.randint(2, 9) * 1000 + random.randint(1, 9) * 100
    lo = 100 if d == 0 else 1000
    b = random.randint(lo, a - 500)
    for _ in range(500):
        if (b % 1000 > 0) if style == "thousand" else (b % 100 > a % 100):
            break
        b = random.randint(lo, a - 500)
    return a, int(b)


# ================================================================== 4.2 ======
@skill("Y4.2.a", "Add and subtract multiples of 10, 100 and 1000 mentally", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        unit = pick([10, 100])
        a = random.randint(12, 45) * 100
    elif d == 1:
        unit = pick([10, 100, 1000])
        a = random.randint(102, 780) * 10
    else:
        unit = pick([10, 100, 1000])
        a = random.randint(1024, 8760)
        a = (a // 10) * 10
    k = random.randint(2, 8)
    b = unit * k
    while a + b > 9999:
        k -= 1
        if k < 1:
            k, unit = 2, 10
        b = unit * k
    tot = a + b
    unit_name = {10: "ten", 100: "hundred", 1000: "thousand"}[unit]

    def bare_add():
        return _numq("Work out %s + %s mentally." % (_com(a), _com(b)), tot,
                     ["Count on %s: %d + %d = %d." % (_pv(k, unit_name + "s"), a, b, tot)])

    def bare_sub():
        return _numq("Work out %s − %s mentally." % (_com(tot), _com(b)), a,
                     ["Count back %s: %d − %d = %d." % (_pv(k, unit_name + "s"), tot, b, a)])

    def on_line():
        base = (a // unit) * unit
        if random.random() < 0.5:
            return _lineq("Start at %s and jump forward %s. Mark where you land."
                          % (_com(base), _com(b)), base + b, [base],
                          ["%d + %d = %d." % (base, b, base + b)])
        return _lineq("Start at %s and jump back %s. Mark where you land."
                      % (_com(base + b), _com(b)), base, [base + b],
                      ["%d − %d = %d." % (base + b, b, base)])

    def missing_add():
        return _numq("Find the missing number:  %s + ___ = %s" % (_com(a), _com(tot)),
                     b, ["Use the inverse: %d − %d = %d." % (tot, a, b)])

    def missing_start():
        return _numq("Find the missing number:  ___ − %s = %s" % (_com(b), _com(a)),
                     tot, ["Use the inverse: %d + %d = %d." % (a, b, tot)])

    def word():
        who = pick(NAMES)
        return _numq("%s is saving up. %s has saved %s points and then wins %s more "
                     "points. How many points does %s have now?"
                     % (who, who, _com(a), _com(b), who), tot,
                     ["%d + %d = %d points." % (a, b, tot)], unit="points")

    def how_many_hundreds():
        cap = max(1, (9999 - a) // unit)
        n = random.randint(min(2, cap), min(9, cap))
        return _numq("How many %ss must be added to %s to make %s?"
                     % (unit_name, _com(a), _com(a + n * unit)), n,
                     ["%d − %d = %d." % (a + n * unit, a, n * unit),
                      "%d ÷ %d = %s." % (n * unit, unit, _pv(n, unit_name + "s"))],
                     unit=unit_name + "s")

    def two_step():
        c = pick([x for x in (10, 100, 1000) if x * 2 < tot] or [10])
        m = random.randint(2, min(5, max(2, (tot - 100) // c)))
        while c * m == b:
            m += 1
            if c * m >= tot:
                c, m = 10, 2
                break
        return _numq("Work out %s + %s − %s mentally."
                     % (_com(a), _com(b), _com(c * m)), tot - c * m,
                     ["%d + %d = %d." % (a, b, tot),
                      "%d − %d = %d." % (tot, c * m, tot - c * m)])

    def compare():
        c = pick([x * unit for x in range(2, 10) if a + x * unit <= 9999 and x * unit != b]
                 or [x * 10 for x in range(2, 10) if x * 10 != b])
        big = max(tot, a + c)
        return _numq("Which total is greater, %s + %s or %s + %s? Type the greater "
                     "total." % (_com(a), _com(b), _com(a), _com(c)), big,
                     ["%d + %d = %d and %d + %d = %d." % (a, b, tot, a, c, a + c),
                      "The greater total is %d." % big])

    def io_mult():
        step = pick([10, 100, 1000, 20, 200, 2000, 50, 500])
        rows = _io_rows(1000, 9000 - step, step, mult=10)
        m = random.randrange(len(rows))
        return _ioq("This function machine adds %s to every In number. Type the "
                    "missing Out number." % _com(step), rows, m, rows[m][1],
                    ["The rule adds %d." % step,
                     "%d + %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="+ %s" % _com(step))

    def io_sub_mult():
        step = pick([10, 100, 1000, 300, 30, 2000])
        rows = _io_rows(step + 1000, 9990, -step, mult=10)
        m = random.randrange(len(rows))
        return _ioq("This function machine subtracts %s from every In number. Type "
                    "the missing Out number." % _com(step), rows, m, rows[m][1],
                    ["The rule subtracts %d." % step,
                     "%d − %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="− %s" % _com(step))

    def place_value():
        n = random.randint(1234, 8765)
        which = pick([10, 100, 1000])
        return _numq("What number is %s more than %s?" % (_com(which), _com(n)),
                     n + which,
                     ["Count on one more %s." %
                      {10: "ten", 100: "hundred", 1000: "thousand"}[which],
                      "%d + %d = %d." % (n, which, n + which)])

    _PLACE_NAMES = ["ones", "tens", "hundreds", "thousands"]

    def add_pattern():
        x = random.randint(2, 7)
        y = random.randint(2, 9 - x)
        k = 3 if d < 2 else 4
        lines = ["%d + %d = %d" % (x * 10 ** i, y * 10 ** i, (x + y) * 10 ** i)
                 for i in range(k - 1)]
        m = 10 ** (k - 1)
        lines.append("%d + %d = ___" % (x * m, y * m))
        nm = _PLACE_NAMES[k - 1]
        return _numq("Continue the addition pattern over increasing place values. "
                     "Type the missing total.  %s" % ",   ".join(lines),
                     (x + y) * m,
                     ["The digits stay the same; each line moves up one place value.",
                      "%s + %s = %s." % (_pv(x, nm), _pv(y, nm), _pv(x + y, nm)),
                      "%d + %d = %d." % (x * m, y * m, (x + y) * m)])

    def sub_pattern():
        x = random.randint(3, 9)
        y = random.randint(1, x - 1)
        k = 3 if d < 2 else 4
        lines = ["%d − %d = %d" % (x * 10 ** i, y * 10 ** i, (x - y) * 10 ** i)
                 for i in range(k - 1)]
        m = 10 ** (k - 1)
        lines.append("%d − %d = ___" % (x * m, y * m))
        nm = _PLACE_NAMES[k - 1]
        return _numq("Continue the subtraction pattern over increasing place values. "
                     "Type the missing answer.  %s" % ",   ".join(lines),
                     (x - y) * m,
                     ["The digits stay the same; each line moves up one place value.",
                      "%s − %s = %s." % (_pv(x, nm), _pv(y, nm), _pv(x - y, nm)),
                      "%d − %d = %d." % (x * m, y * m, (x - y) * m)])

    opts = [bare_add, bare_sub, on_line, word, missing_add, io_mult, place_value,
            how_many_hundreds, add_pattern, sub_pattern]
    if d == 1:
        opts += [missing_start, io_sub_mult, compare]
    elif d == 2:
        opts = [bare_sub, on_line, missing_add, missing_start, word, two_step,
                compare, io_sub_mult, io_mult, how_many_hundreds, place_value,
                add_pattern, sub_pattern]
    return pick(opts)()


@skill("Y4.2.b", "Column addition (up to 4 digits)", S2)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_add4(d, carry=(d > 0 or random.random() < 0.5))
    tot = a + b
    da, db = _digits4(a), _digits4(b)
    steps = ["Ones: %d + %d = %d. Tens: %d + %d = %d."
             % (da[3], db[3], da[3] + db[3], da[2], db[2], da[2] + db[2]),
             "Carry into the next column whenever a column makes 10 or more.",
             "%d + %d = %d." % (a, b, tot)]

    def bare():
        return _numq("Work out %s + %s using the column method." % (_com(a), _com(b)),
                     tot, steps)

    def word_visitors():
        p1, p2 = random.sample(_PLACES, 2)
        return _numq("A museum had %s visitors in %s and %s visitors in %s. How "
                     "many visitors altogether?"
                     % (_com(a), p1, _com(b), p2), tot,
                     ["%d + %d = %d visitors." % (a, b, tot)], unit="visitors")

    def money_add():
        p1 = random.randint(1005, 4999)
        p2 = random.randint(1005, 4999)
        return _numq("A club spent %s on kit and %s on travel. How much was spent "
                     "altogether? Give your answer in pence."
                     % (money(p1), money(p2)), p1 + p2,
                     ["%d + %d = %d pence, which is %s."
                      % (p1, p2, p1 + p2, money(p1 + p2))], unit="p")

    def missing_addend():
        return _numq("Find the missing number:  %s + ___ = %s" % (_com(a), _com(tot)),
                     b, ["Use the inverse: %d − %d = %d." % (tot, a, b)])

    def inverse_check():
        return _numq("%s + %s = ___ . Work it out with the column method, then check "
                     "with the inverse." % (_com(a), _com(b)), tot,
                     ["%d + %d = %d." % (a, b, tot),
                      "Check: %d − %d = %d ✓." % (tot, b, a)])

    def digit_focus():
        col = pick(["ones", "tens"])
        if col == "ones":
            ans = (da[3] + db[3]) % 10
            why = "Ones: %d + %d = %d, so the ones digit is %d." % (
                da[3], db[3], da[3] + db[3], ans)
        else:
            carry = 1 if da[3] + db[3] >= 10 else 0
            ans = (da[2] + db[2] + carry) % 10
            why = "Tens: %d + %d%s = %d, so the tens digit is %d." % (
                da[2], db[2], " + 1 carried" if carry else "",
                da[2] + db[2] + carry, ans)
        return _numq("In the column addition %s + %s, which digit is in the %s "
                     "column of the answer?" % (_com(a), _com(b), col), ans,
                     [why], placeholder="a single digit")

    def find_error():
        wrong = tot + pick([o for o in (-1000, -100, -10, 10, 100, 1000) if 0 < tot + o <= 9999])
        who = pick(NAMES)
        return _numq("%s writes %s + %s = %s. That answer is wrong. Type the correct "
                     "total." % (who, _com(a), _com(b), _com(wrong)), tot,
                     ["Line up the columns and add: %d + %d = %d." % (a, b, tot),
                      "%d was %d out." % (wrong, abs(wrong - tot))])

    def compare():
        c, e = _pair_add4(d)
        while c + e == tot:
            c, e = _pair_add4(d)
        big = max(tot, c + e)
        return _numq("Which total is greater, %s + %s or %s + %s? Type the greater "
                     "total." % (_com(a), _com(b), _com(c), _com(e)), big,
                     ["%d + %d = %d and %d + %d = %d." % (a, b, tot, c, e, c + e),
                      "The greater total is %d." % big])

    def io_add():
        step = pick([1010, 1100, 2200, 1250, 3030, 2001, 1111])
        rows = _io_rows(1000, 9999 - step, step)
        m = random.randrange(len(rows))
        return _ioq("Add %s to every In number using the column method. Type the "
                    "missing Out number." % _com(step), rows, m, rows[m][1],
                    ["The rule adds %d." % step,
                     "%d + %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="+ %s" % _com(step))

    def table_total():
        names = random.sample(_PLACES, 3)
        vals = [random.randint(1005, 3299) for _ in names]
        return _dtq("The table shows how many books each library lent last year. "
                    "How many books were lent altogether?",
                    ["Library", "Books lent"],
                    [[names[i], _com(vals[i])] for i in range(3)],
                    sum(vals),
                    ["%s = %d books."
                     % (" + ".join(_com(v) for v in vals), sum(vals))],
                    caption="Books lent")

    def words_form():
        h = a % 1000
        aw = "%s thousand" % n_words(a // 1000)
        if 0 < h < 100:
            aw += " and %s" % n_words(h)
        elif h:
            aw += ", %s" % n_words(h)
        return _numq("Work out %s plus %s using the column method."
                     % (aw, _com(b)), tot,
                     ["%s is %d." % (aw[0].upper() + aw[1:], a),
                      "%d + %d = %d." % (a, b, tot)])

    opts = [bare, bare, word_visitors, money_add, inverse_check, io_add,
            table_total, digit_focus]
    if d == 1:
        opts += [missing_addend, find_error, compare]
    elif d == 2:
        opts = [bare, missing_addend, find_error, compare, digit_focus,
                money_add, io_add, io_add, table_total, table_total,
                inverse_check, word_visitors, words_form]
    return pick(opts)()


@skill("Y4.2.c", "Column subtraction (up to 4 digits)", S2)
def _(d=1):
    d = _lvl(d)
    a, b = _pair_sub4(d, exchange=(d > 0 or random.random() < 0.5))
    res = a - b

    def bare():
        return _numq("Work out %s − %s using the column method." % (_com(a), _com(b)),
                     res, ["Exchange whenever the top digit is too small.",
                           "%d − %d = %d." % (a, b, res)])

    def across_zeros():
        z, y = _pair_sub_zeros(d)
        return _numq("Work out %s − %s using the column method. You will need to "
                     "exchange across the zeros." % (_com(z), _com(y)), z - y,
                     ["Where the top digit is 0 there is nothing to take away, so "
                      "exchange from the next column that has something in it.",
                      "%d − %d = %d." % (z, y, z - y)])

    def across_zeros_word():
        z, y = _pair_sub_zeros(d)
        who = pick(NAMES)
        return _numq("A stadium holds %s people. %s counts %s empty seats. How many "
                     "people are in the stadium?" % (_com(z), who, _com(y)), z - y,
                     ["%d − %d = %d people." % (z, y, z - y)], unit="people")

    def word_left():
        who = pick(NAMES)
        return _numq("%s had %s points and lost %s points. How many points does %s "
                     "have now?" % (who, _com(a), _com(b), who), res,
                     ["%d − %d = %d points." % (a, b, res)], unit="points")

    def difference():
        return _numq("What is the difference between %s and %s?"
                     % (_com(a), _com(b)), res,
                     ["The difference is found by subtracting: %d − %d = %d."
                      % (a, b, res)])

    def missing_minuend():
        return _numq("Find the missing number:  ___ − %s = %s" % (_com(b), _com(res)),
                     a, ["Use the inverse: %d + %d = %d." % (res, b, a)])

    def missing_subtrahend():
        return _numq("Find the missing number:  %s − ___ = %s" % (_com(a), _com(res)),
                     b, ["Use the inverse: %d − %d = %d." % (a, res, b)])

    def inverse_check():
        return _numq("%s − %s = ___ . Work it out, then check by adding."
                     % (_com(a), _com(b)), res,
                     ["%d − %d = %d." % (a, b, res),
                      "Check: %d + %d = %d ✓." % (res, b, a)])

    def io_sub():
        step = pick([1010, 1100, 2020, 1250, 3003, 1111])
        rows = _io_rows(step + 1000, 9999, -step)
        m = random.randrange(len(rows))
        return _ioq("Subtract %s from every In number using the column method. Type "
                    "the missing Out number." % _com(step), rows, m, rows[m][1],
                    ["The rule subtracts %d." % step,
                     "%d − %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="− %s" % _com(step))

    def table_diff():
        names = random.sample(_PLACES, 3)
        vals = sorted([random.randint(1105, 8999) for _ in range(3)], reverse=True)
        random.shuffle(vals)
        i = vals.index(max(vals))
        j = vals.index(min(vals))
        return _dtq("The table shows the population of three villages. How many more "
                    "people live in %s than in %s?" % (names[i], names[j]),
                    ["Village", "People"],
                    [[names[k], _com(vals[k])] for k in range(3)],
                    vals[i] - vals[j],
                    ["%s has %d people and %s has %d."
                     % (names[i], vals[i], names[j], vals[j]),
                     "%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j])],
                    caption="Village populations")

    def find_error():
        wrong = res + pick([o for o in (-1000, -100, -10, 10, 100, 1000) if res + o > 0])
        who = pick(NAMES)
        return _numq("%s writes %s − %s = %s. That answer is wrong. Type the correct "
                     "answer." % (who, _com(a), _com(b), _com(wrong)), res,
                     ["%d − %d = %d." % (a, b, res),
                      "Check by adding: %d + %d = %d ✓." % (res, b, a)])

    def money_change():
        cost = random.randint(1050, 4990)
        paid = pick([5000, 10000])
        while paid <= cost:
            paid = 10000
        return _numq("A bike costs %s. It is paid for with %s. How much change is "
                     "given? Give your answer in pence."
                     % (money(cost), money(paid)), paid - cost,
                     ["%d − %d = %d pence, which is %s."
                      % (paid, cost, paid - cost, money(paid - cost))], unit="p")

    opts = [bare, across_zeros, across_zeros_word, word_left, difference,
            inverse_check, io_sub, io_sub, table_diff, table_diff, money_change]
    if d == 1:
        opts += [missing_subtrahend, find_error]
    elif d == 2:
        opts = [across_zeros, across_zeros, missing_minuend, missing_subtrahend,
                find_error, difference, io_sub, io_sub, table_diff, table_diff,
                money_change, across_zeros_word, inverse_check]
    return pick(opts)()


@skill("Y4.2.d", "Add three or more numbers", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        vals = [random.randint(105, 899) for _ in range(3)]
    elif d == 1:
        vals = [random.randint(1005, 3299) for _ in range(3)]
    else:
        vals = [random.randint(1005, 2499) for _ in range(4)]
    tot = sum(vals)
    chain = " + ".join(_com(v) for v in vals)

    def bare():
        run = vals[0]
        sol = []
        for v in vals[1:]:
            sol.append("%d + %d = %d." % (run, v, run + v))
            run += v
        return _numq("Work out %s using the column method." % chain, tot, sol)

    def word_three():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s collects %s in three weeks: %s in week 1, %s in week 2 and "
                     "%s in week 3. How many %s does %s collect altogether?"
                     % (who, thing, _com(vals[0]), _com(vals[1]), _com(vals[2]),
                        thing, who), sum(vals[:3]),
                     ["%s = %d %s." % (" + ".join(_com(v) for v in vals[:3]),
                                       sum(vals[:3]), thing)], unit=thing)

    def money_total():
        ps = [random.randint(105, 999) for _ in range(3)]
        items = random.sample(["a book", "a game", "a pen set", "a poster",
                               "a rucksack"], 3)
        return _numq("A shopping list has %s for %s, %s for %s and %s for %s. What "
                     "is the total cost in pence?"
                     % (items[0], money(ps[0]), items[1], money(ps[1]),
                        items[2], money(ps[2])), sum(ps),
                     ["%s = %d pence, which is %s."
                      % (" + ".join(str(p) for p in ps), sum(ps), money(sum(ps)))],
                     unit="p")

    def pairs_to_ten():
        base = [random.randint(2, 9) for _ in range(3)]
        k = random.choice([10 - base[0], 10 - base[1]])
        nums = base + [k]
        random.shuffle(nums)
        return _numq("Add these four numbers, looking for pairs that make 10:  %s"
                     % " + ".join(str(v) for v in nums), sum(nums),
                     ["Pair the numbers that make 10 first, then add the rest.",
                      "The total is %d." % sum(nums)])

    def missing_addend():
        i = random.randrange(len(vals))
        shown = [("___" if j == i else _com(v)) for j, v in enumerate(vals)]
        return _numq("Find the missing number:  %s = %s"
                     % (" + ".join(shown), _com(tot)), vals[i],
                     ["Add the numbers you can see: %d."
                      % (tot - vals[i]),
                      "%d − %d = %d." % (tot, tot - vals[i], vals[i])])

    def chart_total():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        cvals = [random.randint(120, 480) for _ in cats]
        return _barq("The chart shows how many tickets were sold each day. How many "
                     "tickets were sold altogether?", cats, cvals, sum(cvals),
                     ["%s = %d tickets."
                      % (" + ".join(str(v) for v in cvals), sum(cvals))])

    def table_total():
        names = random.sample(["Year 3", "Year 4", "Year 5", "Year 6"], 4)
        tvals = [random.randint(1005, 2499) for _ in names]
        return _dtq("The table shows how many steps each class walked. How many "
                    "steps did the four classes walk altogether?",
                    ["Class", "Steps"],
                    [[names[i], _com(tvals[i])] for i in range(4)],
                    sum(tvals),
                    ["%s = %d steps."
                     % (" + ".join(_com(v) for v in tvals), sum(tvals))],
                    caption="Steps walked")

    def table_missing_total():
        names = random.sample(_PLACES, 3)
        tvals = [random.randint(1005, 2999) for _ in names]
        rows = [[names[i], _com(tvals[i])] for i in range(3)]
        rows.append(["Total", ""])
        return _dtq("Complete the table: type the missing total.",
                    ["Village", "Trees planted"], rows, sum(tvals),
                    ["%s = %d trees."
                     % (" + ".join(_com(v) for v in tvals), sum(tvals))],
                    missing=[3, 1], caption="Trees planted")

    def order_reasoning():
        n = [random.randint(11, 49) for _ in range(3)]
        return _numq("Add these three numbers in any order:  %s. Adding in a "
                     "different order gives the same total. What is the total?"
                     % " + ".join(str(v) for v in n), sum(n),
                     ["%d + %d = %d." % (n[0], n[1], n[0] + n[1]),
                      "%d + %d = %d." % (n[0] + n[1], n[2], sum(n))])

    def add_then_compare():
        other = [random.randint(1005, 3299) for _ in range(3)]
        while sum(other) == tot:
            other = [random.randint(1005, 3299) for _ in range(3)]
        big = max(tot, sum(other))
        return _numq("Which total is greater, %s or %s? Type the greater total."
                     % (chain, " + ".join(_com(v) for v in other)), big,
                     ["%s = %d." % (chain, tot),
                      "%s = %d." % (" + ".join(_com(v) for v in other), sum(other)),
                      "The greater total is %d." % big])

    def strip_total():
        parts = random.randint(3, 5)
        each = random.randint(105, 899)
        return _stripq("The strip model shows %d equal parts of %s. What is the total?"
                       % (parts, _com(each)),
                       {"mode": "equal_parts", "parts": parts,
                        "partLabel": _com(each), "totalLabel": "?",
                        "unknown": "total"}, parts * each,
                       ["%s = %d." % (" + ".join([_com(each)] * parts), parts * each),
                        "That is the same as %d × %d = %d."
                        % (parts, each, parts * each)])

    opts = [bare, word_three, money_total, pairs_to_ten, chart_total, table_total,
            table_missing_total, strip_total, order_reasoning]
    if d == 1:
        opts += [missing_addend]
    elif d == 2:
        opts = [bare, bare, word_three, missing_addend, missing_addend,
                add_then_compare, table_total, table_missing_total, chart_total,
                money_total, strip_total]
    return pick(opts)()


@skill("Y4.2.e", "Missing numbers, missing digits and balanced equations", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(120, 640); b = random.randint(105, 320)
    elif d == 1:
        a = random.randint(1020, 5400); b = random.randint(1005, 3200)
    else:
        a = random.randint(2140, 6400); b = random.randint(1280, 3300)
    tot = a + b

    def missing_addend():
        return _numq("Find the missing number:  %s + ___ = %s" % (_com(a), _com(tot)),
                     b, ["Use the inverse: %d − %d = %d." % (tot, a, b)])

    def missing_first():
        return _numq("Find the missing number:  ___ + %s = %s" % (_com(b), _com(tot)),
                     a, ["Use the inverse: %d − %d = %d." % (tot, b, a)])

    def missing_subtrahend():
        return _numq("Find the missing number:  %s − ___ = %s" % (_com(tot), _com(b)),
                     a, ["Use the inverse: %d − %d = %d." % (tot, b, a)])

    def missing_minuend():
        return _numq("Find the missing number:  ___ − %s = %s" % (_com(b), _com(a)),
                     tot, ["Use the inverse: %d + %d = %d." % (a, b, tot)])

    def missing_digit_add():
        x, y = _pair_add4(d)
        s = x + y
        i = random.randrange(4)
        shown = list(_com(x))
        hidden = int(shown[i])
        shown[i] = "?"
        return _numq("One digit is hidden. Find the digit that makes this addition "
                     "correct:  %s + %s = %s. Type the missing digit."
                     % ("".join(shown), _com(y), _com(s)), hidden,
                     ["Use the inverse: %d − %d = %d." % (s, y, x),
                      "So the hidden digit is %d." % hidden],
                     placeholder="a single digit")

    def missing_digit_sub():
        x, y = _pair_sub4(d)
        r = x - y
        i = random.randrange(4)
        shown = list(_com(y))
        hidden = int(shown[i])
        shown[i] = "?"
        return _numq("One digit is hidden. Find the digit that makes this subtraction "
                     "correct:  %s − %s = %s. Type the missing digit."
                     % (_com(x), "".join(shown), _com(r)), hidden,
                     ["Use the inverse: %d − %d = %d." % (x, r, y),
                      "So the hidden digit is %d." % hidden],
                     placeholder="a single digit")

    def balance_add():
        c = random.randint(100, tot - 100)
        while c == a:
            c = random.randint(100, tot - 100)
        return _numq("Balance this equation. Find the missing number:  "
                     "%s + %s = %s + ___" % (_com(a), _com(b), _com(c)), tot - c,
                     ["Both sides must equal the same total: %d + %d = %d."
                      % (a, b, tot),
                      "%d − %d = %d." % (tot, c, tot - c)])

    def balance_sub():
        res = a
        e = random.randint(105, 900)
        while e == b:
            e = random.randint(105, 900)
        return _numq("Balance this equation. Find the missing number:  "
                     "%s − %s = ___ − %s" % (_com(tot), _com(b), _com(e)), res + e,
                     ["The left side is %d − %d = %d." % (tot, b, res),
                      "%d + %d = %d, so the missing number is %d."
                      % (res, e, res + e, res + e)])

    def balance_mixed():
        c = random.randint(105, max(105, min(900, 9999 - tot)))
        return _numq("Balance this equation. Find the missing number:  "
                     "%s + %s = %s − ___" % (_com(a), _com(b), _com(tot + c)), c,
                     ["The left side is %d + %d = %d." % (a, b, tot),
                      "%d − %d = %d, so the missing number is %d."
                      % (tot + c, tot, c, c)])

    def which_sign():
        x = random.randint(320, 890) if d == 0 else random.randint(1200, 6800)
        y = random.randint(105, 300) if d == 0 else random.randint(105, 900)
        if random.random() < 0.5:
            return _wordq("Which sign makes this number sentence true, + or −?  "
                          "%s ___ %s = %s.  Type plus or minus."
                          % (_com(x), _com(y), _com(x + y)), "plus",
                          ["%d + %d = %d, so the sign is +." % (x, y, x + y)],
                          placeholder="plus or minus")
        return _wordq("Which sign makes this number sentence true, + or −?  "
                      "%s ___ %s = %s.  Type plus or minus."
                      % (_com(x), _com(y), _com(x - y)), "minus",
                      ["%d − %d = %d, so the sign is −." % (x, y, x - y)],
                      placeholder="plus or minus")

    def strip_part():
        return _stripq("The bar model shows a whole of %s split into two parts. One "
                       "part is %s. What is the other part?" % (_com(tot), _com(a)),
                       {"mode": "part_whole", "totalLabel": _com(tot),
                        "partLabel": _com(a), "unknown": "part"}, b,
                       ["Whole − part = part.",
                        "%d − %d = %d." % (tot, a, b)])

    def io_rule():
        step = pick([100, 1000, 250, 500, 1100, 2000])
        if random.random() < 0.5:
            rows = _io_rows(step + 1000, 9999, -step, mult=10)
            why = "Every Out number is %d less than its In number." % step
        else:
            rows = _io_rows(1000, 9999 - step, step, mult=10)
            why = "Every Out number is %d more than its In number." % step
        return _ioq("What number does this function machine add or subtract? Type "
                    "just that number.", rows, None, step,
                    [why, "So the rule uses %d." % step],
                    placeholder="the number")

    def two_step_missing():
        c = random.randint(105, 900)
        return _numq("Find the missing number:  %s + ___ − %s = %s"
                     % (_com(a), _com(c), _com(tot - c)), b,
                     ["Undo the subtraction first: %d + %d = %d."
                      % (tot - c, c, tot),
                      "Then %d − %d = %d." % (tot, a, b)])

    opts = [missing_addend, missing_first, missing_subtrahend, missing_minuend,
            balance_add, which_sign, strip_part, strip_part, io_rule, io_rule,
            missing_digit_add]
    if d == 1:
        opts += [balance_sub, missing_digit_sub]
    elif d == 2:
        opts = [missing_first, missing_minuend, missing_digit_add,
                missing_digit_sub, balance_add, balance_sub, balance_mixed,
                two_step_missing, io_rule, io_rule, strip_part, strip_part,
                which_sign]
    return pick(opts)()


@skill("Y4.2.f", "Addition and subtraction word problems", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = random.randint(210, 890); b = random.randint(105, 200)
    elif d == 1:
        a = random.randint(1200, 6800); b = random.randint(1050, min(3200, 9999 - a))
    else:
        a = random.randint(2400, 8600); b = random.randint(1250, min(3400, 9999 - a))
    c = random.randint(105, 900)

    def total_word():
        p1, p2 = random.sample(_PLACES, 2)
        return _numq("A charity walk raised £%s in %s and £%s in %s. How many "
                     "pounds were raised altogether?"
                     % (_com(a), p1, _com(b), p2), a + b,
                     ["'Altogether' means both amounts put together, so add.",
                      "%d + %d = %d pounds." % (a, b, a + b)], unit="pounds")

    def how_many_more():
        return _numq("A school library has %s books. A town library has %s books. "
                     "How many more books does the school library have?"
                     % (_com(a + b), _com(b)), a,
                     ["'How many more' means find the difference, so subtract.",
                      "%d − %d = %d books." % (a + b, b, a)], unit="books")

    def distance():
        who = pick(NAMES)
        return _numq("%s cycles %s m on Saturday and %s m on Sunday. How many metres "
                     "does %s cycle in total?" % (who, _com(a), _com(b), who), a + b,
                     ["'In total' means both days put together, so add.",
                      "%d + %d = %d m." % (a, b, a + b)], unit="m")

    def two_step_shop():
        who = pick(NAMES)
        return _numq("%s had %s points. %s spent %s points on a prize and then earned "
                     "%s more points. How many points does %s have now?"
                     % (who, _com(a + b), who, _com(b), _com(c), who), a + c,
                     ["'Spent' means take away, so subtract; 'earned more' means add.",
                      "%d − %d = %d." % (a + b, b, a),
                      "%d + %d = %d points." % (a, c, a + c)], unit="points")

    def two_step_stock():
        return _numq("A warehouse held %s boxes. %s boxes arrived and %s boxes were "
                     "sent out. How many boxes are in the warehouse now?"
                     % (_com(a), _com(b), _com(c)), a + b - c,
                     ["'Arrived' means more came in, so add; 'sent out' means some left, so subtract.",
                      "%d + %d = %d." % (a, b, a + b),
                      "%d − %d = %d boxes." % (a + b, c, a + b - c)], unit="boxes")

    def money_two_step():
        p1 = random.randint(1050, 3999)
        p2 = random.randint(505, 1999)
        paid = 10000
        return _numq("%s buys a tent for %s and a torch for %s, and pays with %s. "
                     "How much change is given? Give your answer in pence."
                     % (pick(NAMES), money(p1), money(p2), money(paid)),
                     paid - p1 - p2,
                     ["%d + %d = %d pence spent." % (p1, p2, p1 + p2),
                      "%d − %d = %d pence, which is %s."
                      % (paid, p1 + p2, paid - p1 - p2, money(paid - p1 - p2))],
                     unit="p")

    def chart_word():
        cats = ["Year 3", "Year 4", "Year 5", "Year 6"]
        vals = [random.randint(120, 480) for _ in cats]
        i, j = random.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        if vals[i] == vals[j]:
            vals[i] += 25
        return _barq("The chart shows how many house points each year group earned. "
                     "How many more points did %s earn than %s?" % (cats[i], cats[j]),
                     cats, vals, vals[i] - vals[j],
                     ["'How many more … than' means find the difference, so subtract.",
                      "%s: %d, %s: %d." % (cats[i], vals[i], cats[j], vals[j]),
                      "%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j])])

    def table_word():
        names = random.sample(_PLACES, 3)
        vals = [random.randint(1005, 4999) for _ in names]
        return _dtq("The table shows how many people visited each park last month. "
                    "How many people visited %s and %s altogether?"
                    % (names[0], names[1]),
                    ["Park", "Visitors"],
                    [[names[i], _com(vals[i])] for i in range(3)],
                    vals[0] + vals[1],
                    ["'Altogether' means both parks put together, so add.",
                     "%s: %d, %s: %d." % (names[0], vals[0], names[1], vals[1]),
                     "%d + %d = %d visitors."
                     % (vals[0], vals[1], vals[0] + vals[1])],
                    caption="Park visitors")

    def picto_word():
        key = pick([10, 20, 50])
        cats = ["Red", "Blue", "Green"]
        vals = [key * random.randint(3, 9) for _ in cats]
        return _pictq("The pictogram shows the cars counted in a survey. How many "
                      "red and green cars were counted altogether?",
                      cats, vals, key, "car", vals[0] + vals[2],
                      ["'Altogether' means red and green together, so add.",
                       "Red %d and green %d." % (vals[0], vals[2]),
                       "%d + %d = %d cars." % (vals[0], vals[2],
                                               vals[0] + vals[2])])

    def strip_compare():
        return _stripq("The bar model shows a total of %s made of two parts. One "
                       "part is %s. How big is the other part?"
                       % (_com(a + b), _com(a)),
                       {"mode": "part_whole", "totalLabel": _com(a + b),
                        "partLabel": _com(a), "unknown": "part"}, b,
                       ["%d − %d = %d." % (a + b, a, b)])

    def population_diff():
        p1, p2 = random.sample(_PLACES, 2)
        return _numq("%s has a population of %s and %s has a population of %s. What "
                     "is the difference between the two populations?"
                     % (p1, _com(a + b), p2, _com(b)), a,
                     ["'Difference' means how much bigger one is than the other, so subtract.",
                      "%d − %d = %d people." % (a + b, b, a)], unit="people")

    opts = [total_word, how_many_more, distance, chart_word, table_word,
            picto_word, strip_compare, population_diff]
    if d == 1:
        opts += [two_step_shop, two_step_stock, money_two_step]
    elif d == 2:
        opts = [two_step_shop, two_step_stock, money_two_step, money_two_step,
                chart_word, table_word, population_diff, strip_compare,
                how_many_more, picto_word]
    return pick(opts)()


@skill("Y4.2.g", "Input/output tables and data tables (± to 4 digits)", S2)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        step = pick([100, 200, 500, 1000, 110])
        lo, hi = 200, 4000
    elif d == 1:
        step = pick([1010, 1100, 1250, 2200, 3030, 1111, 2001])
        lo, hi = 1000, 8000
    else:
        step = pick([1234, 2345, 1408, 3607, 2809, 1750])
        lo, hi = 1000, 9000
    hi = min(hi, 9999 - step)

    def io_add():
        rows = _io_rows(lo, hi, step)
        m = random.randrange(len(rows))
        return _ioq("Complete the function machine table. Type the missing Out "
                    "number.", rows, m, rows[m][1],
                    ["The rule adds %d." % step,
                     "%d + %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="+ %s" % _com(step))

    def io_sub():
        rows = _io_rows(lo + step, 9999, -step)
        m = random.randrange(len(rows))
        return _ioq("Complete the function machine table. Type the missing Out "
                    "number.", rows, m, rows[m][1],
                    ["The rule subtracts %d." % step,
                     "%d − %d = %d." % (rows[m][0], step, rows[m][1])],
                    rule="− %s" % _com(step))

    def io_rule_add():
        rows = _io_rows(lo, hi, step)
        return _ioq("What number is added to every In number? Type just that number.",
                    rows, None, step,
                    ["%d − %d = %d." % (rows[0][1], rows[0][0], step),
                     "Every Out number is %d more than its In number." % step],
                    placeholder="the number")

    def io_rule_sub():
        rows = _io_rows(lo + step, 9999, -step)
        return _ioq("What number is subtracted from every In number? Type just that "
                    "number.", rows, None, step,
                    ["%d − %d = %d." % (rows[0][0], rows[0][1], step),
                     "Every Out number is %d less than its In number." % step],
                    placeholder="the number")

    def dt_find_in():
        rows = _io_rows(lo, hi, step, n=4)
        m = random.randrange(len(rows))
        body = [[_com(i), _com(o)] for i, o in rows]
        return _dtq("The rule is add %s. Type the missing In number." % _com(step),
                    ["In", "Out"], body, rows[m][0],
                    ["Use the inverse: %d − %d = %d."
                     % (rows[m][1], step, rows[m][0])],
                    missing=[m, 0], caption="Rule: + %s" % _com(step))

    def dt_find_in_sub():
        rows = _io_rows(lo + step, 9999, -step, n=4)
        m = random.randrange(len(rows))
        body = [[_com(i), _com(o)] for i, o in rows]
        return _dtq("The rule is subtract %s. Type the missing In number."
                    % _com(step), ["In", "Out"], body, rows[m][0],
                    ["Use the inverse: %d + %d = %d."
                     % (rows[m][1], step, rows[m][0])],
                    missing=[m, 0], caption="Rule: − %s" % _com(step))

    def dt_frequency():
        cats = random.sample(["Football", "Netball", "Swimming", "Running",
                              "Cycling", "Tennis"], 4)
        vals = [random.randint(105, 1999) for _ in cats]
        body = [[cats[i], _com(vals[i])] for i in range(4)]
        body.append(["Total", ""])
        return _dtq("Complete the frequency table: type the missing total.",
                    ["Club", "Members"], body, sum(vals),
                    ["%s = %d members."
                     % (" + ".join(_com(v) for v in vals), sum(vals))],
                    missing=[4, 1], caption="Club members")

    def dt_missing_part():
        cats = random.sample(["Football", "Netball", "Swimming", "Running",
                              "Cycling", "Tennis"], 3)
        vals = [random.randint(105, 1999) for _ in cats]
        total = sum(vals)
        m = random.randrange(3)
        body = [[cats[i], "" if i == m else _com(vals[i])] for i in range(3)]
        body.append(["Total", _com(total)])
        return _dtq("One number is missing from the table. Type the missing number.",
                    ["Club", "Members"], body, vals[m],
                    ["The two clubs shown add to %d."
                     % (total - vals[m]),
                     "%d − %d = %d." % (total, total - vals[m], vals[m])],
                    missing=[m, 1], caption="Club members")

    def dt_two_row_diff():
        names = random.sample(_PLACES, 4)
        vals = [random.randint(1005, 8999) for _ in names]
        i, j = random.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        if vals[i] == vals[j]:
            vals[i] += 100
        return _dtq("The table shows how many tickets each town sold. How many more "
                    "tickets did %s sell than %s?" % (names[i], names[j]),
                    ["Town", "Tickets"],
                    [[names[k], _com(vals[k])] for k in range(4)],
                    vals[i] - vals[j],
                    ["%s: %d and %s: %d."
                     % (names[i], vals[i], names[j], vals[j]),
                     "%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j])],
                    caption="Tickets sold")

    def dt_price_list():
        items = random.sample(["Tent", "Torch", "Sleeping bag", "Backpack",
                               "Water bottle"], 4)
        ps = [random.randint(505, 4999) for _ in items]
        i, j = random.sample(range(4), 2)
        return _dtq("The price list shows camping gear. How much do the %s and the "
                    "%s cost together? Give your answer in pence."
                    % (items[i].lower(), items[j].lower()),
                    ["Item", "Price"],
                    [[items[k], money(ps[k])] for k in range(4)],
                    ps[i] + ps[j],
                    ["%d + %d = %d pence, which is %s."
                     % (ps[i], ps[j], ps[i] + ps[j], money(ps[i] + ps[j]))],
                    caption="Price list", placeholder="pence")

    opts = [io_add, io_sub, io_rule_add, io_rule_sub, dt_find_in, dt_frequency,
            dt_two_row_diff, dt_price_list, dt_missing_part]
    if d == 2:
        opts = [io_sub, io_rule_add, io_rule_sub, dt_find_in, dt_find_in_sub,
                dt_missing_part, dt_two_row_diff, dt_price_list, dt_frequency,
                io_add]
    return pick(opts)()


# ================================================================== 4.3 ======
@skill("Y4.3.a", "Understand multiplication: equal groups, arrays, number lines", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        g, p = random.randint(2, 5), random.randint(2, 5)
    elif d == 1:
        g, p = random.randint(2, 8), random.randint(2, 9)
    else:
        g, p = random.randint(4, 8), random.randint(5, 10)
    tot = g * p
    r, c = _fit(g, p) or (g, p)

    def groups_read():
        return _egq("There are %d equal groups with %d counters in each group. How "
                    "many counters are there altogether?" % (g, p), g, p, tot,
                    ["%d equal groups of %d." % (g, p),
                     "%d × %d = %d counters." % (g, p, tot)])

    def groups_build():
        return _egbuildq("Make %d equal groups with %d counters in each group, then "
                         "type how many counters there are altogether." % (g, p),
                         g, p,
                         ["%d equal groups of %d." % (g, p),
                          "%d × %d = %d." % (g, p, tot)])

    def groups_missing_factor():
        return _egq("Put the %d counters into equal groups of %d to show ___ × %d = %d. "
                    "How many equal groups are there?" % (tot, p, p, tot), g, p, g,
                    ["Each group holds %d counters and the total is %d." % (p, tot),
                     "%d ÷ %d = %d groups." % (tot, p, g)])

    def array_build():
        return _arrayq("Build an array with %d rows of %d to show %d × %d, then type "
                       "the total." % (r, c, r, c), r, c,
                       ["%d rows of %d." % (r, c),
                        "%d × %d = %d." % (r, c, tot)])

    def array_turn():
        rr, cc = _fit(c, r) or (c, r)
        return _arrayq("Turn the array round: build %d rows of %d and type the total. "
                       "It shows that %d × %d gives the same answer as %d × %d."
                       % (rr, cc, rr, cc, cc, rr), rr, cc,
                       ["Turning an array does not change how many counters it holds.",
                        "%d × %d = %d × %d = %d." % (rr, cc, cc, rr, rr * cc)])

    def array_read():
        return _numq("An array has %d rows with %d counters in each row. How many "
                     "counters are there altogether?" % (r, c), tot,
                     ["%d × %d = %d." % (r, c, tot)])

    def on_line():
        step = p
        jumps = g
        return _lineq("Start at 0 and make %d equal jumps of %d. Mark where you land."
                      % (jumps, step), tot, [0],
                      ["%d jumps of %d is %d × %d." % (jumps, step, jumps, step),
                       "%d × %d = %d." % (jumps, step, tot)], prefer=step)

    def repeated_addition():
        n = min(g, 6)
        chain = " + ".join([str(p)] * n)
        return _numq("Write this repeated addition as a multiplication and work it "
                     "out:  %s" % chain, n * p,
                     ["%s is %d lots of %d." % (chain, n, p),
                      "%d × %d = %d." % (n, p, n * p)])

    def word_groups():
        who = pick(NAMES)
        thing = pick(["boxes", "trays", "bags", "crates"])
        return _numq("%s fills %d %s and each one holds %d cakes. How many cakes "
                     "does %s have altogether?" % (who, g, thing, p, who), tot,
                     ["%d × %d = %d cakes." % (g, p, tot)], unit="cakes")

    def strip_model():
        return _stripq("The strip model shows %d equal parts of %d. What is the "
                       "total?" % (g, p),
                       {"mode": "equal_parts", "parts": min(g, 12),
                        "partLabel": str(p), "totalLabel": "?",
                        "unknown": "total"}, min(g, 12) * p,
                       ["%d equal parts of %d." % (min(g, 12), p),
                        "%d × %d = %d." % (min(g, 12), p, min(g, 12) * p)])

    def sentence():
        return _egq("Complete the multiplication sentence for these equal groups:  "
                    "%d × %d = ___" % (g, p), g, p, tot,
                    ["%d equal groups of %d." % (g, p),
                     "%d × %d = %d." % (g, p, tot)])

    opts = [groups_read, groups_build, array_build, array_read, on_line,
            repeated_addition, word_groups, strip_model, sentence]
    if d == 2:
        opts = [groups_read, groups_missing_factor, array_build, array_turn,
                on_line, word_groups, strip_model, repeated_addition, array_read]
    return pick(opts)()


@skill("Y4.3.b", "Multiplication facts to 12 × 12", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        t = pick([2, 3, 4, 5, 10]); k = random.randint(3, 10)
    elif d == 1:
        t = random.randint(2, 12); k = random.randint(2, 12)
    else:
        t = random.randint(6, 12); k = random.randint(6, 12)
    p = t * k

    def bare():
        x, y = (t, k) if random.random() < 0.5 else (k, t)
        return _numq("Work out %d × %d." % (x, y), p,
                     ["%d × %d = %d." % (x, y, p)])

    def missing_factor():
        if random.random() < 0.5:
            return _numq("Find the missing factor:  %d × ___ = %d" % (t, p), k,
                         ["%d ÷ %d = %d." % (p, t, k)])
        return _numq("Find the missing factor:  ___ × %d = %d" % (k, p), t,
                     ["%d ÷ %d = %d." % (p, k, t)])

    def array_build():
        rr, cc = _fit(t, k) or (t, k)
        return _arrayq("Build an array with %d rows of %d, then type the product."
                       % (rr, cc), rr, cc, ["%d × %d = %d." % (rr, cc, p)])

    def count_line():
        return _lineq("Count in %ds. Start at 0 and make %d jumps of %d. Mark where "
                      "you land." % (t, k, t), p, [0],
                      ["%d jumps of %d is %d × %d = %d." % (k, t, k, t, p)],
                      prefer=t)

    def word():
        who = pick(NAMES)
        thing = pick(["bags", "boxes", "packs", "trays"])
        return _numq("%s buys %d %s of apples with %d apples in each. How many "
                     "apples does %s buy?" % (who, k, thing, t, who), p,
                     ["%d × %d = %d apples." % (k, t, p)], unit="apples")

    def money_word():
        each = random.randint(2, 12)
        n = random.randint(3, 12)
        return _numq("Pencils cost %s each. How much do %d pencils cost, in pence?"
                     % (money(each), n), each * n,
                     ["%d × %d = %dp." % (each, n, each * n)], unit="p")

    def compare():
        t2 = random.randint(2, 12); k2 = random.randint(2, 12)
        while t2 * k2 == p:
            k2 = random.randint(2, 12)
        big = max(p, t2 * k2)
        return _numq("Which product is larger, %d × %d or %d × %d? Type the larger "
                     "product." % (t, k, t2, k2), big,
                     ["%d × %d = %d and %d × %d = %d." % (t, k, p, t2, k2, t2 * k2),
                      "The larger product is %d." % big])

    def io_times():
        rows = [[i, i * t] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(len(rows))
        return _ioq("This function machine multiplies every In number by %d. Type "
                    "the missing Out number." % t, rows, m, rows[m][1],
                    ["%d × %d = %d." % (rows[m][0], t, rows[m][1])],
                    rule="× %d" % t)

    def doubling():
        return _numq("%d × %d = %d. Use that fact to work out %d × %d."
                     % (t, k, p, t, k * 2), p * 2,
                     ["Doubling one factor doubles the product.",
                      "%d × 2 = %d." % (p, p * 2)])

    def dt_table():
        base = random.randint(2, 9)
        rows = [[str(i), str(i * base)] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(4)
        val = int(rows[m][1])
        return _dtq("The table shows the %d times table. Type the missing product."
                    % base, ["Number", "× %d" % base], rows, val,
                    ["%s × %d = %d." % (rows[m][0], base, val)],
                    missing=[m, 1], caption="The %d times table" % base)

    def groups():
        gg, pp = min(t, 8), min(k, 10)
        return _egq("These equal groups show a multiplication fact. There are %d "
                    "groups of %d. What is the product?" % (gg, pp), gg, pp, gg * pp,
                    ["%d × %d = %d." % (gg, pp, gg * pp)])

    def mul_pattern():
        f = pick([2, 3, 4, 5]) if d == 0 else random.randint(2, 9)
        s = pick([2, 3, 4, 5]) if d == 0 else random.randint(2, 9)
        k = 3 if d < 2 else 4
        lines = ["%d × %d = %d" % (f, s * 10 ** i, f * s * 10 ** i)
                 for i in range(k - 1)]
        m = 10 ** (k - 1)
        lines.append("%d × %d = ___" % (f, s * m))
        nm = ["ones", "tens", "hundreds", "thousands"][k - 1]
        return _numq("Continue the multiplication pattern over increasing place "
                     "values. Type the missing product.  %s" % ",   ".join(lines),
                     f * s * m,
                     ["The known fact is %d × %d = %d." % (f, s, f * s),
                      "%d × %s = %s." % (f, _pv(s, nm), _pv(f * s, nm)),
                      "%d × %d = %d." % (f, s * m, f * s * m)])

    opts = [bare, bare, array_build, count_line, word, money_word, io_times,
            dt_table, groups, mul_pattern]
    if d == 1:
        opts += [missing_factor, compare]
    elif d == 2:
        opts = [bare, missing_factor, missing_factor, compare, doubling,
                io_times, dt_table, word, money_word, array_build, mul_pattern]
    return pick(opts)()


@skill("Y4.3.c", "Division facts to 12 × 12", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        t = pick([2, 3, 4, 5, 10]); k = random.randint(3, 10)
    elif d == 1:
        t = random.randint(2, 12); k = random.randint(2, 12)
    else:
        t = random.randint(6, 12); k = random.randint(6, 12)
    p = t * k

    def bare():
        return _numq("Work out %d ÷ %d." % (p, t), k,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (t, k, p, p, t, k)])

    def bare_other():
        return _numq("Work out %d ÷ %d." % (p, k), t,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (k, t, p, p, k, t)])

    def missing_dividend():
        return _numq("Find the missing number:  ___ ÷ %d = %d" % (t, k), p,
                     ["%d × %d = %d." % (t, k, p)])

    def missing_divisor():
        return _numq("Find the missing number:  %d ÷ ___ = %d" % (p, k), t,
                     ["%d ÷ %d = %d." % (p, k, t)])

    def share_word():
        who = pick(NAMES)
        return _numq("%s shares %d stickers equally between %d friends. How many "
                     "stickers does each friend get?" % (who, p, t), k,
                     ["%d ÷ %d = %d stickers each." % (p, t, k)], unit="stickers")

    def group_word():
        return _numq("%d children are put into teams of %d. How many teams are "
                     "there?" % (p, k), t,
                     ["%d ÷ %d = %d teams." % (p, k, t)], unit="teams")

    def array_model():
        rr, cc = _fit(t, k) or (t, k)
        return _arrayq("Counters are shared into %d equal rows with %d counters in "
                       "each row. Build the array, then type how many counters were "
                       "shared altogether." % (rr, cc), rr, cc,
                       ["%d × %d = %d." % (rr, cc, p),
                        "That is why %d ÷ %d = %d." % (p, rr, cc)])

    def groups_read():
        gg, pp = min(t, 8), min(k, 10)
        return _egq("%d counters have been put into equal groups of %d. How many "
                    "equal groups are there?" % (gg * pp, pp), gg, pp, gg,
                    ["Count the groups: there are %d." % gg,
                     "%d ÷ %d = %d groups." % (gg * pp, pp, gg)])

    def inverse_check():
        return _numq("%d ÷ %d = ___ . Work it out, then check by multiplying."
                     % (p, t), k,
                     ["%d ÷ %d = %d." % (p, t, k),
                      "Check: %d × %d = %d ✓." % (k, t, p)])

    def io_divide():
        rows = [[i * t, i] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(len(rows))
        return _ioq("This function machine divides every In number by %d. Type the "
                    "missing Out number." % t, rows, m, rows[m][1],
                    ["%d ÷ %d = %d." % (rows[m][0], t, rows[m][1])],
                    rule="÷ %d" % t)

    def money_word():
        each = random.randint(2, 12)
        n = random.randint(3, 12)
        return _numq("%s is shared equally between %d children. How much does each "
                     "child get, in pence?" % (money(each * n), n), each,
                     ["%d ÷ %d = %dp each." % (each * n, n, each)], unit="p")

    def dt_divide():
        base = random.randint(2, 9)
        rows = [[str(i * base), str(i)] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(4)
        val = int(rows[m][1])
        return _dtq("Each number in the first column has been divided by %d. Type "
                    "the missing answer." % base,
                    ["Number", "÷ %d" % base], rows, val,
                    ["%s ÷ %d = %d." % (rows[m][0], base, val)],
                    missing=[m, 1], caption="Dividing by %d" % base)

    def div_pattern():
        f = pick([2, 3, 4, 5]) if d == 0 else random.randint(2, 9)
        s = pick([2, 3, 4, 5]) if d == 0 else random.randint(2, 9)
        q = f * s
        k = 3 if d < 2 else 4
        lines = ["%d ÷ %d = %d" % (q * 10 ** i, f, s * 10 ** i)
                 for i in range(k - 1)]
        m = 10 ** (k - 1)
        lines.append("%d ÷ %d = ___" % (q * m, f))
        nm = ["ones", "tens", "hundreds", "thousands"][k - 1]
        return _numq("Continue the division pattern over increasing place values. "
                     "Type the missing answer.  %s" % ",   ".join(lines),
                     s * m,
                     ["The known fact is %d ÷ %d = %d." % (q, f, s),
                      "%s ÷ %d = %s." % (_pv(q, nm), f, _pv(s, nm)),
                      "%d ÷ %d = %d." % (q * m, f, s * m)])

    opts = [bare, bare_other, share_word, group_word, array_model, groups_read,
            inverse_check, io_divide, dt_divide, money_word, div_pattern]
    if d == 2:
        opts = [bare, bare_other, missing_dividend, missing_divisor, share_word,
                group_word, io_divide, dt_divide, inverse_check, array_model,
                div_pattern]
    return pick(opts)()


@skill("Y4.3.d", "Multiplication and division fact families", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a = pick([2, 3, 4, 5, 10]); b = random.randint(2, 9)
    elif d == 1:
        a = random.randint(2, 12); b = random.randint(2, 12)
    else:
        a = random.randint(6, 12); b = random.randint(6, 12)
    while a == b:
        b = random.randint(2, 12)
    p = a * b

    def mul_to_div():
        return _numq("%d × %d = %d is one fact in a family. Use it to work out "
                     "%d ÷ %d." % (a, b, p, p, b), a,
                     ["The same family gives %d ÷ %d = %d." % (p, b, a)])

    def div_to_mul():
        return _numq("%d ÷ %d = %d is one fact in a family. Use it to work out "
                     "%d × %d." % (p, a, b, b, a), p,
                     ["The same family gives %d × %d = %d." % (b, a, p)])

    def fourth_fact():
        return _numq("Three facts in a family are %d × %d = %d, %d × %d = %d and "
                     "%d ÷ %d = %d. What is the answer to the fourth fact, %d ÷ %d?"
                     % (a, b, p, b, a, p, p, a, b, p, b), a,
                     ["The fourth fact is %d ÷ %d = %d." % (p, b, a)])

    def missing_member():
        return _numq("Complete this fact family:  %d × ___ = %d" % (a, p), b,
                     ["%d ÷ %d = %d." % (p, a, b)])

    def array_family():
        rr, cc = _fit(a, b) or (a, b)
        return _arrayq("Build an array of %d rows of %d. It shows the whole fact "
                       "family. Type the total number of counters." % (rr, cc),
                       rr, cc,
                       ["%d × %d = %d and %d × %d = %d." % (rr, cc, p, cc, rr, p),
                        "So %d ÷ %d = %d and %d ÷ %d = %d as well."
                        % (p, rr, cc, p, cc, rr)])

    def groups_family():
        gg, pp = min(a, 8), min(b, 10)
        return _egq("%d × %d = %d. Share the %d counters into %d equal groups and use "
                    "that fact to complete the related division:  %d ÷ %d = ___"
                    % (gg, pp, gg * pp, gg * pp, gg, gg * pp, gg), gg, pp, pp,
                    ["Multiplication and division are inverses.",
                     "%d ÷ %d = %d." % (gg * pp, gg, pp)])

    def word_family():
        who = pick(NAMES)
        return _numq("%s knows that %d × %d = %d. Use that fact to work out how many "
                     "rows of %d are needed to hold %d counters."
                     % (who, a, b, p, b, p), a,
                     ["%d ÷ %d = %d rows." % (p, b, a)], unit="rows")

    def dt_family():
        rows = [["%d × %d" % (a, b), _com(p)],
                ["%d × %d" % (b, a), _com(p)],
                ["%d ÷ %d" % (p, a), _com(b)],
                ["%d ÷ %d" % (p, b), ""]]
        return _dtq("This table shows one fact family. Type the missing answer.",
                    ["Fact", "Answer"], rows, a,
                    ["The family uses %d, %d and %d." % (a, b, p),
                     "%d ÷ %d = %d." % (p, b, a)],
                    missing=[3, 1], caption="Fact family")

    def third_number():
        return _numq("A fact family uses the numbers %d, %d and one more number. "
                     "The multiplication fact is %d × %d = ___ . What is the third "
                     "number?" % (a, b, a, b), p,
                     ["%d × %d = %d, so the third number is %d." % (a, b, p, p)])

    def io_family():
        rows = [[i * a, i] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(len(rows))
        return _ioq("This machine divides by %d, the inverse of multiplying by %d. "
                    "Type the missing Out number." % (a, a), rows, m, rows[m][1],
                    ["%d ÷ %d = %d." % (rows[m][0], a, rows[m][1]),
                     "Check: %d × %d = %d ✓." % (rows[m][1], a, rows[m][0])],
                    rule="÷ %d" % a)

    def real_world_pattern():
        one, many = pick([("box", "boxes"), ("crate", "crates"),
                          ("pack", "packs"), ("tray", "trays")])
        thing = pick(["pencils", "apples", "beads", "tiles", "cards", "bricks"])
        per = random.randint(2, 9)
        n = random.randint(2, 9)
        e = 2 if d < 2 else 3
        counts = [n * 10 ** i for i in range(e + 1)]
        lead = ("Real-world pattern: multiplication and division work the same way "
                "over increasing place values. One %s holds %d %s." % (one, per, thing))

        def _join(parts):
            parts = list(parts)
            if len(parts) < 2:
                return parts[0]
            return ", ".join(parts[:-1]) + " and " + parts[-1]

        if random.random() < 0.5:
            shown = _join("%d %s hold %d %s" % (c, many, c * per, thing)
                          for c in counts[:e])
            return _numq("%s So %s. Use multiplication to work out how many %s are "
                         "in %d %s." % (lead, shown, thing, counts[e], many),
                         counts[e] * per,
                         ["Each step multiplies by 10.",
                          "%d × %d = %d %s."
                          % (counts[e], per, counts[e] * per, thing)],
                         unit=thing)
        shown = _join("%d %s fill %d %s" % (c * per, thing, c, many)
                      for c in counts[:e])
        return _numq("%s So %s. Use division to work out how many %s are needed for "
                     "%d %s." % (lead, shown, many, counts[e] * per, thing),
                     counts[e],
                     ["Each step multiplies by 10.",
                      "%d ÷ %d = %d %s."
                      % (counts[e] * per, per, counts[e], many)],
                     unit=many)

    def count_facts():
        return _numq("The numbers %d, %d and %d make a fact family. How many different multiplication and division facts "
                     "can you write with them?" % (a, b, p), 4,
                     ["%d × %d = %d and %d × %d = %d." % (a, b, p, b, a, p),
                      "%d ÷ %d = %d and %d ÷ %d = %d, so 4 facts." % (p, a, b, p, b, a)])

    def wrong_fact():
        wrong = random.random() < 0.5
        shown = "%d ÷ %d = %d" % (a, p, b) if wrong else "%d ÷ %d = %d" % (p, b, a)
        return _wordq("Does %s belong to the fact family of %d × %d = %d? Type yes or no." % (shown, a, b, p),
                      "no" if wrong else "yes",
                      ["The family is %d × %d, %d × %d, %d ÷ %d and %d ÷ %d." % (a, b, b, a, p, a, p, b),
                       "%s %s one of them." % (shown, "is not" if wrong else "is")], placeholder="yes or no")

    opts = [mul_to_div, div_to_mul, array_family, groups_family, word_family,
            dt_family, third_number, io_family, real_world_pattern, wrong_fact]
    if d == 1:
        opts += [missing_member, fourth_fact, count_facts]
    elif d == 2:
        opts = [mul_to_div, div_to_mul, fourth_fact, missing_member, dt_family,
                word_family, third_number, io_family, array_family, groups_family,
                real_world_pattern, wrong_fact]
    return pick(opts)()


@skill("Y4.3.e", "Multiples and factor pairs", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        base = pick([2, 3, 4, 5, 10])
    elif d == 1:
        base = random.randint(2, 12)
    else:
        base = random.randint(6, 12)

    def nth_multiple():
        n = random.randint(3, 12)
        return _numq("What is the %s multiple of %d?" % (ordinal(n), base), n * base,
                     ["Count in %ds: the %s multiple is %d × %d = %d."
                      % (base, ordinal(n), n, base, n * base)])

    def next_multiple():
        n = random.randint(2, 9)
        return _numq("The multiples of %d are %s, … What is the next multiple of %d?"
                     % (base, ", ".join(str(base * i) for i in range(1, n + 1)),
                        base), base * (n + 1),
                     ["%d × %d = %d." % (base, n + 1, base * (n + 1))])

    def is_multiple():
        n = base * random.randint(2, 12)
        if random.random() < 0.5:
            n += random.randint(1, base - 1) if base > 1 else 1
        yes = (n % base == 0)
        return _wordq("Is %d a multiple of %d? Type yes or no." % (n, base),
                      "yes" if yes else "no",
                      ["%d ÷ %d = %s." % (n, base,
                                          "%d exactly" % (n // base) if yes
                                          else "%d remainder %d" % (n // base,
                                                                    n % base)),
                       "So %d %s a multiple of %d."
                       % (n, "is" if yes else "is not", base)],
                      placeholder="yes or no")

    def list_multiples():
        n = random.randint(3, 5)
        return _setq("List the first %d multiples of %d, starting at %d."
                     % (n, base, base),
                     [base * i for i in range(1, n + 1)],
                     ["Count in %ds: %s."
                      % (base, ", ".join(str(base * i) for i in range(1, n + 1)))],
                     placeholder="separate with commas")

    def pick_multiples():
        pool = set()
        good = [base * random.randint(2, 9) for _ in range(2)]
        while len(set(good)) < 2:
            good = [base * random.randint(2, 9) for _ in range(2)]
        pool.update(good)
        while len(pool) < 5:
            x = random.randint(4, base * 10)
            if x % base != 0:
                pool.add(x)
        lst = sorted(pool)
        ans = [x for x in lst if x % base == 0]
        return _setq("Which of these numbers are multiples of %d?  %s"
                     % (base, ", ".join(str(x) for x in lst)), ans,
                     ["Divide each number by %d and keep the ones with no "
                      "remainder." % base,
                      "The multiples of %d are %s."
                      % (base, ", ".join(str(x) for x in ans))])

    def factor_pair_missing():
        n = base * random.randint(2, 12)
        other = n // base
        return _numq("Complete this factor pair of %d:  %d × ___ = %d"
                     % (n, base, n), other,
                     ["%d ÷ %d = %d." % (n, base, other)])

    def list_factors():
        n = pick([12, 16, 18, 20, 24]) if d == 0 else pick([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 45, 48, 60])
        facs = [i for i in range(1, n + 1) if n % i == 0]
        return _setq("List all the factors of %d." % n, facs,
                     ["Try each number in turn: %s divide into %d exactly."
                      % (", ".join(str(f) for f in facs), n),
                      "%d has %d factors." % (n, len(facs))],
                     placeholder="separate with commas")

    def count_factor_pairs():
        n = pick([12, 16, 18, 20, 24, 28, 30, 36, 40, 48])
        pairs = [(i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0]
        return _numq("How many different factor pairs does %d have?" % n, len(pairs),
                     ["The factor pairs of %d are %s."
                      % (n, ", ".join("%d × %d" % pr for pr in pairs)),
                      "That is %d factor pairs." % len(pairs)],
                     unit="pairs")

    def is_factor():
        n = pick([12, 16, 18, 20, 24, 30, 36, 40, 48])
        f = random.randint(2, 12)
        yes = (n % f == 0)
        return _wordq("Is %d a factor of %d? Type yes or no." % (f, n),
                      "yes" if yes else "no",
                      ["%d ÷ %d = %s."
                       % (n, f, "%d exactly" % (n // f) if yes
                          else "%d remainder %d" % (n // f, n % f)),
                       "So %d %s a factor of %d."
                       % (f, "is" if yes else "is not", n)],
                      placeholder="yes or no")

    def array_factor_pair():
        n = base * random.randint(2, 9)
        other = n // base
        rr, cc = _fit(base, other) or (base, other)
        return _arrayq("Build an array with %d rows of %d, then type how many "
                       "counters it holds. The rows and the columns are a factor "
                       "pair of that total." % (rr, cc), rr, cc,
                       ["%d × %d = %d, so %d and %d are a factor pair of %d."
                        % (rr, cc, n, rr, cc, n)])

    def common_multiple():
        x = pick([2, 3, 4, 5, 6])
        y = pick([i for i in (2, 3, 4, 5, 6, 8, 9, 10)
                  if i % x and x % i])
        lcm = x * y
        for m in range(max(x, y), x * y + 1):
            if m % x == 0 and m % y == 0:
                lcm = m
                break
        return _numq("What is the smallest number that is a multiple of both %d and "
                     "%d?" % (x, y), lcm,
                     ["Multiples of %d: %s…" % (x, ", ".join(str(x * i)
                                                             for i in range(1, lcm // x + 1))),
                      "Multiples of %d: %s…" % (y, ", ".join(str(y * i)
                                                             for i in range(1, lcm // y + 1))),
                      "The smallest number in both lists is %d." % lcm])

    def word_multiple():
        who = pick(NAMES)
        n = random.randint(4, 12)
        return _numq("%s buys %d packs of pens with %d pens in each pack. How many "
                     "pens does %s buy altogether?" % (who, n, base, who), base * n,
                     ["%d × %d = %d pens." % (n, base, n * base),
                      "It is a multiple of %d because it is %d lots of %d."
                      % (base, n, base)], unit="pens")

    def io_multiples():
        rows = [[i, i * base] for i in sorted(random.sample(range(2, 13), 4))]
        m = random.randrange(len(rows))
        return _ioq("Every Out number is a multiple of %d. Type the missing Out "
                    "number." % base, rows, m, rows[m][1],
                    ["%d × %d = %d." % (rows[m][0], base, rows[m][1]),
                     "%d is the %s multiple of %d."
                     % (rows[m][1], ordinal(rows[m][0]), base)],
                    rule="× %d" % base)

    def line_multiples():
        j = random.randint(3, 8)
        return _lineq("Count in %ds. Start at 0 and mark the %s multiple of %d."
                      % (base, ordinal(j), base), base * j, [0],
                      ["The %s multiple of %d is %d × %d = %d."
                       % (ordinal(j), base, j, base, base * j)], prefer=base)

    def dt_factor_pairs():
        n = pick([12, 16, 18, 20, 24, 30, 36, 40, 48])
        pairs = [(i, n // i) for i in range(1, int(n ** 0.5) + 1) if n % i == 0]
        m = random.randrange(len(pairs))
        rows = [[str(x), str(y)] for x, y in pairs]
        return _dtq("The table lists the factor pairs of %d. Type the missing "
                    "number." % n, ["Factor", "Factor"], rows, pairs[m][1],
                    ["%d ÷ %d = %d." % (n, pairs[m][0], pairs[m][1]),
                     "So %d and %d are a factor pair of %d."
                     % (pairs[m][0], pairs[m][1], n)],
                    missing=[m, 1], caption="Factor pairs of %d" % n)

    def choose_multiples():
        bb = pick([2, 3, 4, 5, 10]) if d == 0 else random.randint(2, 10)
        good = set()
        while len(good) < 3:
            good.add(bb * random.randint(2, 12))
        bad = set()
        while len(bad) < 3:
            x = random.randint(2, bb * 12)
            if x % bb and x not in good:
                bad.add(x)
        lst = sorted(good | bad)
        ans = [x for x in lst if x % bb == 0]
        return _setq("Choose the multiples of the given number %d. Type every number "
                     "in this list that is a multiple of %d:  %s"
                     % (bb, bb, ", ".join(str(x) for x in lst)), ans,
                     ["Divide each number by %d and keep the ones with no "
                      "remainder." % bb,
                      "The multiples of %d are %s."
                      % (bb, ", ".join(str(x) for x in ans))],
                     placeholder="separate with commas")

    opts = [nth_multiple, next_multiple, is_multiple, list_multiples,
            factor_pair_missing, list_factors, array_factor_pair, is_factor,
            word_multiple, io_multiples, line_multiples, dt_factor_pairs,
            choose_multiples]
    if d == 1:
        opts += [pick_multiples, count_factor_pairs]
    elif d == 2:
        opts = [nth_multiple, is_multiple, pick_multiples, list_factors,
                count_factor_pairs, common_multiple, is_factor,
                factor_pair_missing, list_multiples, array_factor_pair,
                io_multiples, line_multiples, dt_factor_pairs, choose_multiples]
    return pick(opts)()


@skill("Y4.3.f", "Divisibility rules", S3)
def _(d=1):
    d = _lvl(d)
    # Year 4 tests divisibility by 2, 5 and 10 (last digit) and by times-table facts to 12 x 12;
    # the digit-sum rule for 3 and 9 is not in the Year 4 curriculum.
    rules = [2, 5, 10]
    r = pick(rules)
    _WHY = {2: "A number is divisible by 2 if its last digit is even (0, 2, 4, 6 or 8).",
            5: "A number is divisible by 5 if its last digit is 0 or 5.",
            10: "A number is divisible by 10 if its last digit is 0."}

    def _rand(lo=100, hi=999):
        return random.randint(lo, hi)

    def yes_no():
        n = _rand(100, 999) if d < 2 else _rand(1000, 9999)
        if random.random() < 0.5:
            n = n - (n % r)
        yes = (n % r == 0)
        sol = [_WHY[r], "The last digit of %d is %d." % (n, n % 10)]
        sol.append("So %d %s divisible by %d." % (n, "is" if yes else "is not", r))
        return _wordq("Is %d divisible by %d? Type yes or no." % (n, r),
                      "yes" if yes else "no", sol, placeholder="yes or no")

    def sort_list():
        lst = []
        while len(lst) < 6:
            x = random.randint(100, 999) if d < 2 else random.randint(1000, 9999)
            if random.random() < 0.5:
                x = x - (x % r)
            if x not in lst:
                lst.append(x)
        if all(x % r == 0 for x in lst):
            lst[0] += 1
        ans = [x for x in lst if x % r == 0]
        if not ans:
            lst[0] = lst[0] - (lst[0] % r)
            ans = [x for x in lst if x % r == 0]
        return _setq("Sort these numbers. Type all the numbers that are divisible "
                     "by %d:  %s" % (r, ", ".join(str(x) for x in sorted(lst))), ans,
                     [_WHY[r],
                      "The numbers divisible by %d are %s."
                      % (r, ", ".join(str(x) for x in sorted(ans)))],
                     placeholder="e.g. 120, 345")

    def digit_sum():                 # times-table facts: is it in the table?
        rr = random.randint(3, 12)
        if random.random() < 0.5:
            n = rr * random.randint(2, 12)
        else:
            n = rr * random.randint(2, 11) + random.randint(1, rr - 1)
        yes = n % rr == 0
        return _wordq("Is %d in the %d times table? Type yes or no." % (n, rr), "yes" if yes else "no",
                      ["%d × %d = %d." % (rr, n // rr, rr * (n // rr)),
                       "%d %s in the %d times table%s." % (n, "is" if yes else "is not", rr,
                                                           "" if yes else " (it leaves %d over)" % (n % rr))],
                      placeholder="yes or no")

    def which_rule():                # which last digits pass the test
        rr = pick([2, 5, 10])
        ends = {2: [0, 2, 4, 6, 8], 5: [0, 5], 10: [0]}[rr]
        return _setq("A whole number divides exactly by %d. Which digits could it end in? Type them all." % rr,
                     ends, [_WHY[rr]], placeholder="e.g. 1, 3")

    def missing_digit():
        rr = pick([2, 5])
        pre = random.randint(10, 99)
        dg = max(x for x in range(10) if (pre * 10 + x) % rr == 0)
        return _numq("Find the largest digit that can replace the ? so that %d? is "
                     "divisible by %d. Type that digit." % (pre, rr), dg,
                     [_WHY[rr], "%d%d ÷ %d = %d exactly." % (pre, dg, rr, (pre * 10 + dg) // rr)],
                     placeholder="a single digit")

    def dt_sort():
        nums = []
        while len(nums) < 4:
            x = random.randint(100, 999)
            if random.random() < 0.5:
                x = x - (x % r)
            if x not in nums:
                nums.append(x)
        m = random.randrange(4)
        rows = [[str(nums[i]),
                 "" if i == m else ("yes" if nums[i] % r == 0 else "no")]
                for i in range(4)]
        ans = "yes" if nums[m] % r == 0 else "no"
        return _dtq("Complete the sorting table. Type yes or no for the blank cell.",
                    ["Number", "Divisible by %d?" % r], rows, ans,
                    [_WHY[r],
                     "%d %s divisible by %d."
                     % (nums[m], "is" if ans == "yes" else "is not", r)],
                    missing=[m, 1], answer_type="str", placeholder="yes or no")

    def count_in_list():
        while True:
            lst = [random.randint(100, 999) for _ in range(6)]
            for i in range(3):
                lst[i] = lst[i] - (lst[i] % r)
            if len(set(lst)) == 6:
                break
        random.shuffle(lst)
        n = len([x for x in lst if x % r == 0])
        return _numq("How many of these numbers are divisible by %d?  %s"
                     % (r, ", ".join(str(x) for x in lst)), n,
                     [_WHY[r], "%d of them are divisible by %d." % (n, r)],
                     unit="numbers")

    def both_rules():
        r2 = pick([x for x in (2, 5, 10) if x != r])
        lst = []
        both = r * r2 * random.randint(2, 6)
        while both > 9999:
            both = r * r2 * 2
        lst.append(both)
        while len(lst) < 5:
            x = random.randint(100, 999)
            if x not in lst:
                lst.append(x)
        ans = [x for x in lst if x % r == 0 and x % r2 == 0]
        return _setq("Type all the numbers that are divisible by both %d and %d:  %s"
                     % (r, r2, ", ".join(str(x) for x in sorted(lst))), ans,
                     [_WHY[r], _WHY[r2],
                      "The numbers passing both tests are %s."
                      % ", ".join(str(x) for x in sorted(ans))],
                     placeholder="e.g. 120")

    def make_divisible():
        n = random.randint(100, 990)
        while n % r == 0:
            n = random.randint(100, 990)
        need = (r - n % r) % r
        return _numq("What is the smallest number you must add to %d to make a "
                     "number divisible by %d?" % (n, r), need,
                     [_WHY[r],
                      "%d + %d = %d, and %d ÷ %d = %d exactly."
                      % (n, need, n + need, n + need, r, (n + need) // r)])

    def dt_two_tests():
        r2 = pick([x for x in (2, 5, 10) if x != r])
        nums = []
        while len(nums) < 4:
            x = random.randint(100, 999)
            if random.random() < 0.5:
                x = x - (x % r)
            if x not in nums:
                nums.append(x)
        m = random.randrange(4)
        col = pick([1, 2])
        rule = r if col == 1 else r2
        rows = []
        for i, x in enumerate(nums):
            c1 = "yes" if x % r == 0 else "no"
            c2 = "yes" if x % r2 == 0 else "no"
            if i == m:
                if col == 1:
                    c1 = ""
                else:
                    c2 = ""
            rows.append([str(x), c1, c2])
        ans = "yes" if nums[m] % rule == 0 else "no"
        return _dtq("Complete the sorting table. Type yes or no for the blank cell.",
                    ["Number", "Divisible by %d?" % r, "Divisible by %d?" % r2],
                    rows, ans, [_WHY[rule],
                                "%d %s divisible by %d."
                                % (nums[m], "is" if ans == "yes" else "is not",
                                   rule)],
                    missing=[m, col], answer_type="str", placeholder="yes or no")

    def next_multiple():
        n = random.randint(101, 989)
        while n % r == 0:
            n += 1
        ans = n + (r - n % r)
        return _numq("What is the smallest number greater than %d that is divisible by %d?" % (n, r), ans,
                     [_WHY[r], "%d ÷ %d = %d exactly." % (ans, r, ans // r)])

    def packing():
        who = pick(NAMES)
        n = _rand(100, 999)
        if random.random() < 0.5:
            n = n - (n % r)
        yes = n % r == 0
        return _wordq("%s has %d stickers to put into packs of %d. Will every pack be full with none left over? Type yes or no."
                      % (who, n, r), "yes" if yes else "no",
                      [_WHY[r], "So %d %s divisible by %d." % (n, "is" if yes else "is not", r)], placeholder="yes or no")

    def largest_three_digit():
        ans = 999 - 999 % r
        return _numq("What is the largest 3-digit number that is divisible by %d?" % r, ans,
                     [_WHY[r], "%d ÷ %d = %d exactly, and no bigger 3-digit number works." % (ans, r, ans // r)])

    def end_digits():
        rr = pick([2, 5, 10])
        n = random.randint(10, 99) * 10 + random.randint(0, 9)
        last = n % 10
        yes = n % rr == 0
        return _wordq("A number ends in %d. Is it divisible by %d? Type yes or no." % (last, rr), "yes" if yes else "no",
                      [_WHY[rr], "A last digit of %d %s the test." % (last, "passes" if yes else "fails")], placeholder="yes or no")

    opts = [yes_no, sort_list, dt_sort, dt_sort, dt_two_tests, dt_two_tests,
            count_in_list, digit_sum, which_rule, make_divisible, next_multiple, packing, largest_three_digit]
    if d == 1:
        opts += [missing_digit]
    elif d == 2:
        opts = [yes_no, sort_list, dt_sort, dt_two_tests, dt_two_tests,
                both_rules, missing_digit, make_divisible, count_in_list,
                digit_sum, next_multiple, packing, largest_three_digit]
    if d == 0:
        opts += [end_digits]
    return pick(opts)()


@skill("Y4.3.g", "Square numbers to 12 × 12", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        n = random.randint(2, 6)
    elif d == 1:
        n = random.randint(2, 12)
    else:
        n = random.randint(7, 12)
    sq = n * n

    def bare():
        return _numq("Work out %d × %d." % (n, n), sq,
                     ["%d × %d = %d." % (n, n, sq),
                      "%d is a square number." % sq])

    def squared_notation():
        return _numq("What is %d squared?" % n, sq,
                     ["%d squared means %d × %d." % (n, n, n),
                      "%d × %d = %d." % (n, n, sq)])

    def root():
        return _numq("Which number multiplied by itself gives %d?" % sq, n,
                     ["%d × %d = %d." % (n, n, sq)])

    def area_square():
        return _areaq("This square is %d squares wide and %d squares tall. What is "
                      "its area in square units?" % (n, n), min(n, 12), min(n, 12),
                      ["Area = %d × %d = %d square units."
                       % (min(n, 12), min(n, 12), min(n, 12) * min(n, 12)),
                       "%d is a square number." % (min(n, 12) * min(n, 12))])

    def array_square():
        m = min(n, 10)
        return _arrayq("Build a square array with %d rows of %d, then type the total "
                       "number of counters." % (m, m), m, m,
                       ["%d × %d = %d." % (m, m, m * m),
                        "A square array always shows a square number."])

    def is_square():
        if random.random() < 0.5:
            x = sq
        else:
            x = sq + random.randint(1, max(1, n))
        yes = any(i * i == x for i in range(1, 13))
        return _wordq("Is %d a square number? Type yes or no." % x,
                      "yes" if yes else "no",
                      ["The square numbers to 12 × 12 are 1, 4, 9, 16, 25, 36, 49, "
                       "64, 81, 100, 121 and 144.",
                       "So %d %s a square number." % (x, "is" if yes else "is not")],
                      placeholder="yes or no")

    def list_squares():
        lo = pick([1, 10, 20, 30, 50, 60])
        hi = lo + pick([40, 50, 60, 70])
        vals = [i * i for i in range(1, 13) if lo <= i * i <= hi]
        while len(vals) < 2:
            hi += 30
            vals = [i * i for i in range(1, 13) if lo <= i * i <= hi]
        return _setq("Type all the square numbers between %d and %d (including %d "
                     "and %d)." % (lo, hi, lo, hi), vals,
                     ["Square the whole numbers in turn: %s."
                      % ", ".join("%d × %d = %d" % (i, i, i * i)
                                  for i in range(1, 13) if lo <= i * i <= hi)],
                     placeholder="separate with commas")

    def next_square():
        m = random.randint(4, 11)
        return _numq("The square numbers start 1, 4, 9, … What is the square "
                     "number that comes straight after %d?" % (m * m),
                     (m + 1) * (m + 1),
                     ["%d = %d × %d." % (m * m, m, m),
                      "The next one is %d × %d = %d."
                      % (m + 1, m + 1, (m + 1) * (m + 1))])

    def word_tiles():
        who = pick(NAMES)
        m = min(n, 12)
        return _numq("%s lays square tiles to make a big square with %d tiles along "
                     "each side. How many tiles does %s use?" % (who, m, who), m * m,
                     ["%d × %d = %d tiles." % (m, m, m * m)], unit="tiles")

    def difference_squares():
        m = random.randint(2, 11)
        return _numq("What is the difference between %d squared and %d squared?"
                     % (m + 1, m), (m + 1) ** 2 - m * m,
                     ["%d × %d = %d and %d × %d = %d."
                      % (m + 1, m + 1, (m + 1) ** 2, m, m, m * m),
                      "%d − %d = %d." % ((m + 1) ** 2, m * m, (m + 1) ** 2 - m * m)])

    def dt_squares():
        ns = sorted(random.sample(range(2, 13), 4))
        m = random.randrange(4)
        rows = [[str(v), "" if i == m else str(v * v)] for i, v in enumerate(ns)]
        return _dtq("Complete the table of square numbers. Type the missing square "
                    "number.", ["Number", "Squared"], rows, ns[m] * ns[m],
                    ["%d × %d = %d." % (ns[m], ns[m], ns[m] * ns[m])],
                    missing=[m, 1], caption="Square numbers")

    def side_from_area():
        return _numq("A square has an area of %d square centimetres. How long is each side, in cm?" % sq, n,
                     ["%d × %d = %d, so each side is %d cm." % (n, n, sq, n)], unit="cm")

    def sum_of_squares():
        a, b = random.sample(range(2, 10 if d < 2 else 13), 2)
        return _numq("Work out %d squared add %d squared." % (a, b), a * a + b * b,
                     ["%d × %d = %d and %d × %d = %d." % (a, a, a * a, b, b, b * b), "%d + %d = %d." % (a * a, b * b, a * a + b * b)])

    def odd_even():
        return _wordq("Is %d squared odd or even? Type odd or even." % n, "even" if sq % 2 == 0 else "odd",
                      ["%d × %d = %d." % (n, n, sq), "An odd number times an odd number is odd; an even number squared is even."],
                      placeholder="odd or even")

    def closest_square():
        m = random.randint(3, 11)
        x = m * m + pick([1, 2, -1, -2])
        lo = max(i * i for i in range(1, 13) if i * i <= x)
        hi = min(i * i for i in range(1, 14) if i * i >= x)
        ans = lo if x - lo < hi - x else hi
        return _numq("Which square number is closest to %d?" % x, ans,
                     ["%d lies between %d and %d." % (x, lo, hi), "It is closer to %d." % ans])

    opts = [bare, squared_notation, root, area_square, array_square, is_square,
            word_tiles, dt_squares, next_square, side_from_area, odd_even]
    if d == 1:
        opts += [list_squares, sum_of_squares, closest_square]
    elif d == 2:
        opts = [squared_notation, root, list_squares, is_square,
                difference_squares, next_square, dt_squares, area_square,
                word_tiles, bare, side_from_area, sum_of_squares, closest_square]
    return pick(opts)()


@skill("Y4.3.h", "Commutativity, associativity and the distributive property", S3)
def _(d=1):
    d = _lvl(d)

    def commutative():
        a = random.randint(2, 12); b = random.randint(2, 12)
        while b == a:
            b = random.randint(2, 12)
        return _numq("%d × %d = %d. Use the same fact to work out %d × %d."
                     % (a, b, a * b, b, a), a * b,
                     ["Multiplication can be done in either order.",
                      "%d × %d = %d × %d = %d." % (b, a, a, b, a * b)])

    def comm_array():
        a = random.randint(2, 6)
        b = random.randint(3, 10)
        while b == a:                       # commutativity is vacuous for a square array
            b = random.randint(3, 10)
        rr, cc = _fit(b, a) or (b, a)
        return _arrayq("Build an array with %d rows of %d and type the total. It "
                       "shows that %d × %d gives the same product as %d × %d."
                       % (rr, cc, rr, cc, cc, rr), rr, cc,
                       ["Turning an array round does not change the total.",
                        "%d × %d = %d." % (b, a, a * b)])

    def associative():
        if d == 0:
            a, b, c = random.randint(2, 3), random.randint(2, 3), random.randint(2, 4)
        elif d == 1:
            a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 6)
        else:
            a, b, c = random.randint(3, 6), random.randint(3, 6), random.randint(3, 8)
        return _numq("Work out (%d × %d) × %d." % (a, b, c), a * b * c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d × %d = %d." % (a * b, c, a * b * c)])

    def associative_regroup():
        a = random.randint(2, 9)
        b, c = pick([(2, 5), (5, 2), (2, 50), (4, 25), (5, 4)])
        return _numq("Group the easy pair first: %d × %d × %d = ___"
                     % (a, b, c), a * b * c,
                     ["%d × %d = %d." % (b, c, b * c),
                      "%d × %d = %d." % (a, b * c, a * b * c)])

    def distributive():
        a = random.randint(11, 19) if d < 2 else pick([x for x in range(21, 40) if x % 10])
        b = random.randint(3, 6) if d < 2 else random.randint(4, 9)
        t, o = (a // 10) * 10, a % 10
        return _numq("Use partitioning:  %d × %d = (%d × %d) + (%d × %d) = ___"
                     % (a, b, t, b, o, b), a * b,
                     ["%d × %d = %d and %d × %d = %d."
                      % (t, b, t * b, o, b, o * b),
                      "%d + %d = %d." % (t * b, o * b, a * b)])

    def distributive_missing():
        a = random.randint(11, 19)
        b = random.randint(3, 8)
        t, o = (a // 10) * 10, a % 10
        return _numq("%d × %d = (%d × %d) + (___ × %d). What number is missing?"
                     % (a, b, t, b, b), o,
                     ["%d splits into %d and %d." % (a, t, o),
                      "So the missing number is %d." % o])

    def distributive_word():
        who = pick(NAMES)
        a = random.randint(11, 19)
        b = random.randint(3, 7)
        t, o = (a // 10) * 10, a % 10
        return _numq("%s buys %d boxes of %d pencils. %s works out %d × %d as "
                     "(%d × %d) + (%d × %d). How many pencils is that altogether?"
                     % (who, b, a, who, b, a, b, t, b, o), a * b,
                     ["%d × %d = %d and %d × %d = %d."
                      % (b, t, b * t, b, o, b * o),
                      "%d + %d = %d pencils." % (b * t, b * o, a * b)],
                     unit="pencils")

    def name_property():
        which = pick(["commutative", "associative", "distributive"])
        a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 5)
        while b == a:
            b = random.randint(2, 9)
        if which == "commutative":
            sent = "%d × %d = %d × %d" % (a, b, b, a)
        elif which == "associative":
            sent = "(%d × %d) × %d = %d × (%d × %d)" % (a, b, c, a, b, c)
        else:
            sent = "%d × (%d + %d) = (%d × %d) + (%d × %d)" % (a, b, c, a, b, a, c)
        return _wordq("Which property of multiplication does this show?  %s  "
                      "Type commutative, associative or distributive." % sent,
                      which,
                      ["Commutative: the order of the factors can change.",
                       "Associative: the factors can be grouped differently.",
                       "Distributive: a factor can be shared over an addition.",
                       "This one is the %s property." % which],
                      placeholder="commutative / associative / distributive")

    def by_one_zero():
        a = random.randint(3, 12)
        if random.random() < 0.5:
            return _numq("Work out %d × 1." % a, a,
                         ["Multiplying by 1 leaves the number unchanged: %d." % a])
        return _numq("Work out %d × 0." % a, 0,
                     ["Multiplying by 0 always gives 0."])

    def distribute_over_add():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        return _numq("Work out %d × (%d + %d)." % (a, b, c), a * (b + c),
                     ["%d + %d = %d." % (b, c, b + c),
                      "%d × %d = %d." % (a, b + c, a * (b + c)),
                      "This is the same as (%d × %d) + (%d × %d) = %d + %d."
                      % (a, b, a, c, a * b, a * c)])

    def easier_order():
        a = pick([2, 5])
        b = pick([3, 7, 9, 11])
        c = 5 if a == 2 else 2
        return _numq("Reorder the factors to make this easier, then work it out:  "
                     "%d × %d × %d" % (b, a, c), a * b * c,
                     ["%d × %d = %d, which is easy to multiply by."
                      % (a, c, a * c),
                      "%d × %d = %d." % (a * c, b, a * b * c)])

    def area_distributive():
        rows = random.randint(3, 8)
        cols = pick([11, 12])
        return _areaq("This rectangle is %d squares tall and %d squares wide. Split "
                      "%d into 10 and %d to work out the area in square units."
                      % (rows, cols, cols, cols - 10), rows, cols,
                      ["%d × 10 = %d and %d × %d = %d."
                       % (rows, rows * 10, rows, cols - 10, rows * (cols - 10)),
                       "%d + %d = %d square units."
                       % (rows * 10, rows * (cols - 10), rows * cols)])

    def groups_commutative():
        g = random.randint(2, 8); pp = random.randint(2, 10)
        while pp == g:
            pp = random.randint(2, 10)
        return _egq("These %d equal groups of %d show %d × %d. What is %d × %d?"
                    % (g, pp, g, pp, pp, g), g, pp, g * pp,
                    ["The order of the factors does not change the product.",
                     "%d × %d = %d × %d = %d." % (pp, g, g, pp, g * pp)])

    opts = [commutative, comm_array, comm_array, associative,
            associative_regroup, distributive, name_property, by_one_zero,
            distribute_over_add, easier_order, area_distributive,
            groups_commutative]
    if d == 2:
        opts = [commutative, associative_regroup, distributive,
                distributive_missing, distributive_word, name_property,
                distribute_over_add, easier_order, associative, comm_array,
                area_distributive, groups_commutative]
    return pick(opts)()


@skill("Y4.3.i", "Multiply three numbers together", S3)
def _(d=1):
    d = _lvl(d)
    if d == 0:
        a, b, c = random.randint(2, 3), random.randint(2, 4), random.randint(2, 4)
    elif d == 1:
        a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 6)
    else:
        a, b, c = random.randint(3, 6), random.randint(3, 6), random.randint(4, 9)
    p = a * b * c

    def bare():
        return _numq("Work out %d × %d × %d." % (a, b, c), p,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d × %d = %d." % (a * b, c, p)])

    def brackets():
        return _numq("Work out %d × (%d × %d)." % (a, b, c), p,
                     ["Do the brackets first: %d × %d = %d." % (b, c, b * c),
                      "%d × %d = %d." % (a, b * c, p)])

    def easier_pair():
        x = pick([2, 4, 5])
        y = 5 if x == 2 else (25 if x == 4 else 2)
        z = random.randint(3, 9)
        return _numq("Choose the easiest order, then work out %d × %d × %d."
                     % (z, x, y), x * y * z,
                     ["%d × %d = %d." % (x, y, x * y),
                      "%d × %d = %d." % (x * y, z, x * y * z)])

    def with_ten():
        x = random.randint(2, 9)
        y = random.randint(2, 9)
        return _numq("Work out %d × %d × 10." % (x, y), x * y * 10,
                     ["%d × %d = %d." % (x, y, x * y),
                      "%d × 10 = %d." % (x * y, x * y * 10)])

    def word_shelves():
        who = pick(NAMES)
        return _numq("A library has %d shelves. Each shelf holds %d boxes and each "
                     "box holds %d books. How many books are there altogether?"
                     % (a, b, c), p,
                     ["%d × %d = %d boxes." % (a, b, a * b),
                      "%d × %d = %d books." % (a * b, c, p)], unit="books")

    def word_teams():
        return _numq("There are %d schools. Each school sends %d teams and each team "
                     "has %d players. How many players are there in total?"
                     % (a, b, c), p,
                     ["%d × %d = %d teams." % (a, b, a * b),
                      "%d × %d = %d players." % (a * b, c, p)], unit="players")

    def missing_third():
        return _numq("Find the missing number:  %d × %d × ___ = %d" % (a, b, p), c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d ÷ %d = %d." % (p, a * b, c)])

    def order_same():
        return _numq("%d × %d × %d = %d. What is %d × %d × %d?"
                     % (a, b, c, p, c, a, b), p,
                     ["The factors can be multiplied in any order.",
                      "%d × %d × %d = %d." % (c, a, b, p)])

    def compare():
        x, y, z = random.randint(2, 5), random.randint(2, 5), random.randint(2, 6)
        while x * y * z == p:
            z = random.randint(2, 6)
        big = max(p, x * y * z)
        return _numq("Which product is larger, %d × %d × %d or %d × %d × %d? Type "
                     "the larger product." % (a, b, c, x, y, z), big,
                     ["%d × %d × %d = %d." % (a, b, c, p),
                      "%d × %d × %d = %d." % (x, y, z, x * y * z),
                      "The larger product is %d." % big])

    def money_word():
        each = random.randint(2, 9)
        packs = random.randint(2, 6)
        per = random.randint(2, 6)
        return _numq("Badges cost %s each. %s buys %d packs with %d badges in each "
                     "pack. What is the total cost in pence?"
                     % (money(each), pick(NAMES), packs, per),
                     each * packs * per,
                     ["%d × %d = %d badges." % (packs, per, packs * per),
                      "%d × %d = %dp." % (packs * per, each,
                                          packs * per * each)], unit="p")

    def dt_three():
        layers = random.randint(2, 5)
        rr = random.randint(2, 6)
        cc = random.randint(2, 6)
        return _dtq("The table describes a stack of cubes. How many cubes are there "
                    "altogether?",
                    ["Part", "How many"],
                    [["Layers", str(layers)],
                     ["Rows in each layer", str(rr)],
                     ["Cubes in each row", str(cc)]],
                    layers * rr * cc,
                    ["One layer holds %d × %d = %d cubes." % (rr, cc, rr * cc),
                     "%d × %d = %d cubes in the whole stack."
                     % (layers, rr * cc, layers * rr * cc)],
                    caption="A stack of cubes")

    def io_two_steps():
        x, y = pick([(2, 3), (3, 4), (2, 5), (4, 5), (2, 6), (3, 5)])
        rows = [[i, i * x * y] for i in sorted(random.sample(range(2, 10), 4))]
        m = random.randrange(len(rows))
        return _ioq("This machine multiplies by %d and then by %d. Type the missing "
                    "Out number." % (x, y), rows, m, rows[m][1],
                    ["%d × %d = %d." % (rows[m][0], x, rows[m][0] * x),
                     "%d × %d = %d." % (rows[m][0] * x, y, rows[m][1])],
                    rule="× %d then × %d" % (x, y))

    def dt_teams():
        sch = random.randint(2, 6)
        tm = random.randint(2, 5)
        pl = random.randint(3, 9)
        return _dtq("The table describes a sports tournament. How many players are "
                    "there altogether?", ["Part", "How many"],
                    [["Schools", str(sch)], ["Teams from each school", str(tm)],
                     ["Players in each team", str(pl)]], sch * tm * pl,
                    ["%d × %d = %d teams." % (sch, tm, sch * tm),
                     "%d × %d = %d players." % (sch * tm, pl, sch * tm * pl)],
                    caption="Tournament")

    opts = [bare, brackets, easier_pair, with_ten, word_shelves, word_teams,
            order_same, dt_three, dt_three, money_word, io_two_steps,
            io_two_steps, dt_teams]
    if d == 2:
        opts = [bare, brackets, easier_pair, missing_third, compare,
                word_shelves, word_teams, money_word, with_ten, dt_three,
                dt_teams, io_two_steps, io_two_steps]
    return pick(opts)()
