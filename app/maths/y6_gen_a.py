# dev/app/logic/y6_gen_a.py — Year 6 generators: strands 6.0 and 6.1
#
# 6.0  Number & place value to 10,000,000 (reading, writing, digit values,
#      comparing, ordering, rounding to a required degree of accuracy, Roman
#      numerals to 1,000, negative numbers and intervals across zero).
# 6.1  The four operations (column addition and subtraction, tables facts,
#      long multiplication, short and long division, estimation and inverses,
#      BIDMAS, writing expressions and multi-step problems).
#
# Difficulty `d`: 0 = easy, 1 = core (year-expected), 2 = stretch.
# Every skill offers 8+ genuinely different framings and routes a large share
# of them through the interactive components.
import random
from .maths_engine import skill, n_words, ordinal, pick, NAMES

S0 = "6.0 Number & place value"
S1 = "6.1 The four operations"

_OBJ = ["stickers", "beads", "marbles", "cards", "counters", "shells", "stamps"]
_TOWNS = ["Redhill", "Oakfield", "Larkmoor", "Westbury", "Fenton", "Millbrook",
          "Ashgrove", "Northolt", "Stanton", "Hartley"]
_CITIES = ["Oslo", "Moscow", "Helsinki", "Toronto", "Reykjavik", "Prague",
           "Warsaw", "Tallinn"]


# ================================================================ helpers ====
def _d(d):
    """Clamp difficulty to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _c(n):
    """UK thousands separator: 3482617 -> '3,482,617'."""
    return "{:,}".format(int(n))


def _lst(xs):
    return ", ".join(_c(x) if isinstance(x, int) else str(x) for x in xs)


def _wn(n):
    """Words for 0-10,000,000, UK style."""
    n = int(n)
    if n == 0:
        return "zero"
    if n < 0:
        return "negative " + _wn(-n)
    parts = []
    mil, rest = n // 1000000, n % 1000000
    th, r = rest // 1000, rest % 1000
    if mil:
        parts.append(n_words(mil) + " million")
    if th:
        parts.append(n_words(th) + " thousand")
    if r:
        parts.append(("and " + n_words(r)) if (parts and r < 100) else n_words(r))
    return " ".join(parts)


_RV = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
       (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _rom(n):
    """Roman numeral for 1-1000 (subtractive form)."""
    n = int(n)
    out = ""
    for v, s in _RV:
        while n >= v:
            out += s
            n -= v
    return out


def _r(n, unit):
    """Round n to the nearest `unit`, halves up (n >= 0)."""
    n, unit = int(n), int(unit)
    return ((n + unit // 2) // unit) * unit


_UNITW = {10: "10", 100: "100", 1000: "1,000", 10000: "10,000",
          100000: "100,000", 1000000: "1,000,000"}


# --------------------------------------------------------- number sources ---
def _bignum(d):
    """A number of the right size for this difficulty."""
    if d == 0:
        return random.randint(10001, 999999)
    if d == 1:
        return random.randint(100001, 9999999)
    if random.random() < 0.5:                     # zeros inside trip pupils up
        digs = [random.randint(1, 9)] + [pick([0, 0, random.randint(0, 9)])
                                         for _ in range(6)]
        return int("".join(str(x) for x in digs))
    return random.randint(1000001, 9999999)


def _distinct(d):
    """A number whose digits are all different, so a digit names one place."""
    k = {0: 5, 1: 6, 2: 7}[d]
    digs = random.sample(range(0, 10), k)
    if digs[0] == 0:
        digs[0] = pick([x for x in range(1, 10) if x not in digs[1:]])
    return int("".join(str(x) for x in digs))


_PLACES = [(1000000, "millions"), (100000, "hundred thousands"),
           (10000, "ten thousands"), (1000, "thousands"),
           (100, "hundreds"), (10, "tens"), (1, "ones")]


def _places_of(n):
    """The place columns that the number n actually has."""
    n = int(n)
    return [(p, w) for p, w in _PLACES if p <= n]


def _pl(k, word):
    k = int(k)
    return "%d %s" % (k, word if k == 1 else word + "s")


def _parts_of(n):
    """'3 millions, 4 hundred thousands, ... and 2 ones' for a number."""
    n = int(n)
    bits = []
    for p, w in _places_of(n):
        dig = (n // p) % 10
        name = {"millions": "million", "hundred thousands": "hundred thousand",
                "ten thousands": "ten thousand", "thousands": "thousand",
                "hundreds": "hundred", "tens": "ten", "ones": "one"}[w]
        bits.append(_pl(dig, name))
    return ", ".join(bits[:-1]) + " and " + bits[-1]


def _expanded(n):
    """['3,000,000', '400,000', ...] for the non-zero places of n."""
    n = int(n)
    return [_c(((n // p) % 10) * p) for p, _w in _places_of(n) if (n // p) % 10]


# ------------------------------------------------------ question builders ----
def _tb(prompt, ans, atype="int", spec=None, solution=None):
    """A typed-answer question on the plain `number` component."""
    return {"prompt": prompt, "component": "number", "spec": spec or {},
            "answer": ans, "answer_type": atype, "solution": solution or []}


def _wq(prompt, ans, solution, placeholder="type your answer"):
    """A typed word / text answer."""
    return _tb(prompt, ans, "str", {"text": True, "placeholder": placeholder}, solution)


def _yn(prompt, ans, solution):
    return _wq(prompt, ans, solution, "yes / no")


def _setq(prompt, values, solution, placeholder="e.g. 4, 8, 12"):
    vals = sorted(int(v) for v in values)
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in vals),
            "answer_type": "set", "solution": solution}


def _nlq(prompt, ans, solution, step=1, major=None, lo=None, hi=None):
    """Place-the-marker on a number line. `step` must divide `ans` and `major`."""
    ans = int(ans)
    step = int(step)
    if major is None:
        major = step * 5
    if lo is None:
        lo = ((ans - 3 * step) // major) * major
    if hi is None:
        hi = lo + major * 4
        while hi < ans + step:
            hi += major
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": int(lo), "max": int(hi), "step": step, "major": int(major)},
            "answer": ans, "answer_type": "num", "tolerance": step / 2.0,
            "solution": solution}


def _dt(prompt, headers, rows, answer, solution, missing=None, atype="int"):
    """A bordered data table; `missing` = [row, col] rendered as a blank box."""
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _io(prompt, rows, missing, answer, solution, rule=None, atype="int"):
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _lg(prompt, points, answer, solution, ylabel="°C", xlabel="Time",
        missing=None, atype="int"):
    spec = {"points": [[str(a), b] for a, b in points],
            "yLabel": ylabel, "xLabel": xlabel}
    if missing is not None:
        spec["missing"] = int(missing)
    return {"prompt": prompt, "component": "line_graph", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _bar(prompt, cats, vals, answer, solution, atype="int"):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": [str(c) for c in cats],
                     "values": [int(v) for v in vals], "mode": "read"},
            "answer": answer, "answer_type": atype, "solution": solution}


def _pict(prompt, cats, vals, key, symbol, answer, solution):
    return {"prompt": prompt, "component": "pictogram",
            "spec": {"categories": [str(c) for c in cats],
                     "values": [int(v) for v in vals],
                     "key": int(key), "symbol": symbol},
            "answer": answer, "answer_type": "int", "solution": solution}


def _arr(prompt, rows, cols, solution, answer=None):
    """Array build (rows <= 10, cols <= 12), else fall back to a typed box."""
    rows, cols = int(rows), int(cols)
    if not (rows <= 10 and cols <= 12):
        rows, cols = cols, rows
    if not (rows <= 10 and cols <= 12):
        return _tb(prompt, rows * cols if answer is None else answer, "int", {}, solution)
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "build", "maxRows": min(10, max(6, rows + 2)),
                     "maxCols": min(12, max(6, cols + 2)),
                     "targetRows": rows, "targetCols": cols},
            "answer": rows * cols if answer is None else answer,
            "answer_type": "int", "solution": solution}


def _eg(prompt, groups, per, answer, solution):
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "read", "groups": int(groups), "per": int(per)},
            "answer": answer, "answer_type": "int", "solution": solution}


def _strip(prompt, parts, part_label, total_label, unknown, answer, solution):
    return {"prompt": prompt, "component": "strip_model",
            "spec": {"mode": "equal_parts", "parts": int(parts),
                     "partLabel": str(part_label), "totalLabel": str(total_label),
                     "unknown": unknown},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _area(prompt, rows, cols, solution, answer=None):
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "read_area", "rows": int(rows), "cols": int(cols)},
            "answer": int(rows) * int(cols) if answer is None else answer,
            "answer_type": "int", "solution": solution}


def _pick_t(plain, visual):
    """Choose a framing; visual framings are twice as likely as typed ones."""
    return random.choice(list(plain) + list(visual) + list(visual))()


def _pair_list(a, b, pool, ok, extras=4):
    """A shuffled list holding a and b plus up to `extras` distractors taken from
    `pool`, chosen so that a and b are the ONLY pair satisfying `ok(x, y)`.

    One bounded pass over a shuffled pool — never a search loop, so it cannot hang.
    """
    out = [int(a), int(b)]
    cand = [int(p) for p in pool if int(p) not in out]
    random.shuffle(cand)
    for v in cand:
        if len(out) >= 2 + int(extras):
            break
        if any(ok(v, u) or ok(u, v) for u in out):
            continue
        out.append(v)
    random.shuffle(out)
    return out


# ================================================================== 6.0 ======
@skill("Y6.0.a", "Read and write numbers to 10,000,000", S0)
def _(d=1):
    d = _d(d)
    n = _bignum(d)

    def t_words_to_num():
        return _tb("Write '%s' as a numeral." % _wn(n), n, "int", {},
                   ["'%s' is %s." % (_wn(n), _c(n))])

    def t_parts():
        m = _bignum(d)
        return _tb("Write the number that has %s." % _parts_of(m), m, "int", {},
                   ["Put each digit in its place.", "The number is %s." % _c(m)])

    def t_expanded():
        m = _bignum(d)
        ex = _expanded(m)
        if len(ex) < 2:
            m = _bignum(1)
            ex = _expanded(m)
        return _tb("Write this expanded form as a single number:   %s" % " + ".join(ex),
                   m, "int", {}, ["%s = %s." % (" + ".join(ex), _c(m))])

    def t_zeros():
        digs = [random.randint(1, 9)] + [pick([0, 0, random.randint(1, 9)])
                                         for _ in range(6)]
        m = int("".join(str(x) for x in digs))
        return _tb("Read this carefully and write it as a numeral:   '%s'" % _wn(m),
                   m, "int", {},
                   ["An empty place value is written as a zero.",
                    "'%s' is %s." % (_wn(m), _c(m))])

    def t_compare_words():
        a, b = _bignum(d), _bignum(d)
        while a == b:
            b = _bignum(d)
        return _tb("Which is the greater number, '%s' or '%s'? Write it in numerals."
                   % (_wn(a), _wn(b)), max(a, b), "int", {},
                   ["'%s' is %s and '%s' is %s." % (_wn(a), _c(a), _wn(b), _c(b)),
                    "%s is greater." % _c(max(a, b))])

    def t_population():
        town = pick(_TOWNS)
        return _tb("The population of %s is written as '%s'. Write that population "
                   "as a numeral." % (town, _wn(n)), n, "int", {},
                   ["'%s' is %s." % (_wn(n), _c(n))])

    def t_digit_cards():
        digs = random.sample(range(1, 10), 7 if d == 2 else 6)
        big = random.random() < 0.5
        ans = int("".join(str(x) for x in sorted(digs, reverse=big)))
        return _tb("Use each of these digit cards once to make the %s possible number:"
                   "   %s" % ("largest" if big else "smallest",
                              ", ".join(str(x) for x in digs)), ans, "int", {},
                   ["Put the %s digits in the highest places."
                    % ("largest" if big else "smallest"),
                    "The number is %s." % _c(ans)])

    def t_next():
        base = pick([999999, 1999999, 4999999, 9999999, 3099999])
        return _tb("What number is 1 more than %s?" % _c(base), base + 1, "int", {},
                   ["%s + 1 = %s." % (_c(base), _c(base + 1))])

    def t_odometer():
        who = pick(NAMES)
        km = random.randint(10, 98) * 1000 + random.randint(1, 999)
        return _tb("The milometer in the van %s drives reads '%s' kilometres. "
                   "Write that reading as a numeral." % (who, _wn(km)), km, "int", {},
                   ["'%s' is %s." % (_wn(km), _c(km))])

    def t_table():
        ns = [_bignum(d) for _ in range(4)]
        rows = [[_wn(x), _c(x)] for x in ns]
        r = random.randint(0, 3)
        return _dt("This table shows numbers in words and in numerals. What numeral "
                   "belongs in the empty cell?", ["In words", "In numerals"], rows,
                   ns[r], ["'%s' is %s." % (_wn(ns[r]), _c(ns[r]))], missing=[r, 1])

    def t_chart():
        m = _distinct(max(d, 1))
        ps = _places_of(m)
        digits = [str((m // p) % 10) for p, _w in ps]
        col = random.randint(0, len(ps) - 1)
        heads = [w.title() for _p, w in ps]
        return _dt("This place-value chart shows the number %s. Which digit belongs "
                   "in the empty %s cell?" % (_c(m), ps[col][1]),
                   heads, [digits], int(digits[col]),
                   ["%s = %s." % (_c(m), _parts_of(m)),
                    "The %s digit is %s." % (ps[col][1], digits[col])],
                   missing=[0, col])

    def t_chart_read():
        m = _distinct(max(d, 1))
        ps = _places_of(m)
        digits = [str((m // p) % 10) for p, _w in ps]
        heads = [w.title() for _p, w in ps]
        return _dt("Read the number shown in this place-value chart and write it as "
                   "a numeral.", heads, [digits], m,
                   ["The chart shows %s." % _parts_of(m),
                    "The number is %s." % _c(m)])

    return _pick_t([t_words_to_num, t_parts, t_expanded, t_zeros, t_compare_words,
                    t_population, t_digit_cards, t_next, t_odometer],
                   [t_table, t_chart, t_chart_read])


@skill("Y6.0.b", "Write numbers to 10,000,000 in words", S0)
def _(d=1):
    d = _d(d)
    n = _bignum(d)
    PH = "type in words"

    def t_plain():
        return _wq("Write the number %s in words." % _c(n), _wn(n),
                   ["%s is '%s'." % (_c(n), _wn(n))], PH)

    def t_cheque():
        who = pick(NAMES)
        amt = random.randint(1001, 999999)
        return _wq("%s is filling in a cheque for £%s. Write that amount in words."
                   % (who, _c(amt)), _wn(amt),
                   ["%s in words is '%s'." % (_c(amt), _wn(amt))], PH)

    def t_zeros():
        digs = [random.randint(1, 9)] + [pick([0, 0, random.randint(1, 9)])
                                         for _ in range(6)]
        m = int("".join(str(x) for x in digs))
        return _wq("Write %s in words. Take care with the zeros." % _c(m), _wn(m),
                   ["%s = %s." % (_c(m), _parts_of(m)),
                    "In words that is '%s'." % _wn(m)], PH)

    def t_more():
        amt = pick([1, 10, 1000, 10000, 100000])
        base = n if n + amt <= 10000000 else n - amt
        ans = base + amt
        return _wq("What is %s more than %s? Write your answer in words."
                   % (_c(amt), _c(base)), _wn(ans),
                   ["%s + %s = %s." % (_c(base), _c(amt), _c(ans)),
                    "%s is '%s'." % (_c(ans), _wn(ans))], PH)

    def t_less():
        amt = pick([1, 100, 1000, 100000])
        base = max(n, amt + 1000)
        ans = base - amt
        return _wq("What is %s less than %s? Write your answer in words."
                   % (_c(amt), _c(base)), _wn(ans),
                   ["%s − %s = %s." % (_c(base), _c(amt), _c(ans)),
                    "%s is '%s'." % (_c(ans), _wn(ans))], PH)

    def t_expanded():
        m = _bignum(max(d, 1))
        ex = _expanded(m)
        return _wq("Add these parts together and write the total in words:   %s"
                   % " + ".join(ex), _wn(m),
                   ["%s = %s." % (" + ".join(ex), _c(m)),
                    "%s is '%s'." % (_c(m), _wn(m))], PH)

    def t_population():
        town = pick(_TOWNS)
        return _wq("The population of %s is %s. Write that number in words."
                   % (town, _c(n)), _wn(n),
                   ["%s is '%s'." % (_c(n), _wn(n))], PH)

    def t_stadium():
        seats = random.randint(11, 89) * 1000 + random.randint(1, 999)
        return _wq("A stadium holds %s people. Write that number in words." % _c(seats),
                   _wn(seats), ["%s is '%s'." % (_c(seats), _wn(seats))], PH)

    def t_rounded():
        m = _bignum(max(d, 1))
        unit = pick([1000, 10000, 100000])
        ans = _r(m, unit)
        return _wq("Round %s to the nearest %s, then write your answer in words."
                   % (_c(m), _UNITW[unit]), _wn(ans),
                   ["%s to the nearest %s is %s." % (_c(m), _UNITW[unit], _c(ans)),
                    "%s is '%s'." % (_c(ans), _wn(ans))], PH)

    def t_table():
        ns = [_bignum(d) for _ in range(4)]
        rows = [[_c(x), _wn(x)] for x in ns]
        r = random.randint(0, 3)
        return _dt("What goes in the empty cell? Write the number in words.",
                   ["In numerals", "In words"], rows, _wn(ns[r]),
                   ["%s is '%s'." % (_c(ns[r]), _wn(ns[r]))],
                   missing=[r, 1], atype="str")

    def t_chart():
        m = _distinct(max(d, 1))
        ps = _places_of(m)
        digits = [str((m // p) % 10) for p, _w in ps]
        heads = [w.title() for _p, w in ps]
        return _dt("Write the number shown in this place-value chart in words.",
                   heads, [digits], _wn(m),
                   ["The chart shows %s." % _c(m),
                    "In words that is '%s'." % _wn(m)], atype="str")

    def t_bar():
        towns = random.sample(_TOWNS, 4)
        vals = [random.randint(12, 98) * 1000 for _ in range(4)]
        i = random.randint(0, 3)
        return _bar("The bar chart shows the population of four towns. Write the "
                    "population of %s in words." % towns[i], towns, vals,
                    _wn(vals[i]),
                    ["%s has a population of %s." % (towns[i], _c(vals[i])),
                     "In words that is '%s'." % _wn(vals[i])], atype="str")

    return _pick_t([t_plain, t_cheque, t_zeros, t_more, t_less, t_expanded,
                    t_population, t_stadium, t_rounded],
                   [t_table, t_chart, t_bar])


@skill("Y6.0.c", "Value of each digit; standard and expanded form", S0)
def _(d=1):
    d = _d(d)

    def t_which_digit():
        n = _bignum(d)
        pos, place = pick(_places_of(n))
        return _tb("In the number %s, which digit is in the %s place?" % (_c(n), place),
                   (n // pos) % 10, "int", {},
                   ["%s = %s." % (_c(n), _parts_of(n)),
                    "The %s digit is %d." % (place, (n // pos) % 10)])

    def t_value():
        n = _distinct(d)
        pos, place = pick(_places_of(n))
        dig = (n // pos) % 10
        return _tb("In the number %s, what is the VALUE of the digit in the %s place?"
                   % (_c(n), place), dig * pos, "int", {},
                   ["The %s digit is %d." % (place, dig),
                    "Its value is %d × %s = %s." % (dig, _c(pos), _c(dig * pos))])

    def t_named_value():
        n = _distinct(d)
        pos, place = pick(_places_of(n))
        dig = (n // pos) % 10
        return _tb("What is the value of the digit %d in the number %s?" % (dig, _c(n)),
                   dig * pos, "int", {},
                   ["The %d is in the %s place." % (dig, place),
                    "It is worth %s." % _c(dig * pos)])

    def t_which_place():
        n = _distinct(d)
        pos, place = pick(_places_of(n))
        dig = (n // pos) % 10
        opts = " / ".join(w for _p, w in _places_of(n))
        return _wq("In the number %s, which place is the digit %d in? (%s)"
                   % (_c(n), dig, opts), place,
                   ["%s = %s." % (_c(n), _parts_of(n)),
                    "The %d is in the %s place." % (dig, place)], opts)

    def t_expanded_to_std():
        n = _bignum(d)
        ex = _expanded(n)
        return _tb("Write this expanded form as a single number:   %s" % " + ".join(ex),
                   n, "int", {}, ["%s = %s." % (" + ".join(ex), _c(n))])

    def t_missing_part():
        n = _bignum(max(d, 1))
        ex = _expanded(n)
        if len(ex) < 3:
            n = random.randint(1111111, 9999999)
            ex = _expanded(n)
        idx = random.randrange(len(ex))
        shown = " + ".join("___" if i == idx else v for i, v in enumerate(ex))
        return _tb("Complete the expanded form:   %s = %s" % (_c(n), shown),
                   int(ex[idx].replace(",", "")), "int", {},
                   ["%s = %s." % (_c(n), " + ".join(ex))])

    def t_worth_more():
        ps = _PLACES[-{0: 5, 1: 6, 2: 7}[d]:]
        pos1, _w1 = pick(ps[:-1])
        pos2, _w2 = pick([p for p in ps if p[0] < pos1])
        dig = random.randint(2, 9)
        others = [x for x in range(1, 10) if x != dig]
        a = sum(p * (dig if p == pos1 else pick(others)) for p, _w in ps)
        b = sum(p * (dig if p == pos2 else pick(others)) for p, _w in ps)
        return _tb("The digit %d appears in %s and in %s. How much MORE is it worth "
                   "in %s?" % (dig, _c(a), _c(b), _c(a)),
                   dig * pos1 - dig * pos2, "int", {},
                   ["In %s the %d is worth %s; in %s the %d is worth %s."
                    % (_c(a), dig, _c(dig * pos1), _c(b), dig, _c(dig * pos2)),
                    "%s − %s = %s." % (_c(dig * pos1), _c(dig * pos2),
                                       _c(dig * pos1 - dig * pos2))])

    def t_times_bigger():
        pos = pick([10, 100, 1000, 10000, 100000])
        dig = random.randint(2, 9)
        small = dig
        big = dig * pos
        return _tb("In one number the digit %d is worth %s. In another number the "
                   "same digit is worth %s. How many times bigger is the second "
                   "value?" % (dig, _c(small), _c(big)), pos, "int", {},
                   ["%s ÷ %s = %s." % (_c(big), _c(small), _c(pos))])

    def t_guess():
        n = _distinct(d)
        bits = [(w, (n // p) % 10) for p, w in _places_of(n)]
        random.shuffle(bits)
        desc = ", ".join("%d in the %s place" % (dg, w) for w, dg in bits)
        return _tb("Work out the number: it has %s. What is the number?" % desc,
                   n, "int", {},
                   ["Put each digit in its place.", "The number is %s." % _c(n)])

    def t_change():
        n = _distinct(max(d, 1))
        pos, place = pick(_places_of(n)[:-1])
        dig = (n // pos) % 10
        new = pick([x for x in range(0, 10) if x != dig])
        ans = n + (new - dig) * pos
        return _tb("In the number %s, the digit in the %s place is changed to %d. "
                   "What is the new number?" % (_c(n), place, new), ans, "int", {},
                   ["The %s digit changes from %d to %d." % (place, dig, new),
                    "The new number is %s." % _c(ans)])

    def t_chart_value():
        n = _distinct(max(d, 1))
        ps = _places_of(n)
        digits = [str((n // p) % 10) for p, _w in ps]
        col = random.randint(0, len(ps) - 1)
        pos, place = ps[col]
        dig = int(digits[col])
        return _dt("The place-value chart shows %s. What is the VALUE of the digit "
                   "in the %s column?" % (_c(n), place),
                   [w.title() for _p, w in ps], [digits], dig * pos,
                   ["The %s digit is %d." % (place, dig),
                    "%d × %s = %s." % (dig, _c(pos), _c(dig * pos))])

    def t_table_expanded():
        ns = [_distinct(max(d, 1)) for _ in range(3)]
        rows = [[_c(x), " + ".join(_expanded(x))] for x in ns]
        r = random.randint(0, 2)
        return _dt("This table shows numbers in standard form and expanded form. "
                   "What number belongs in the empty cell?",
                   ["Standard form", "Expanded form"], rows, ns[r],
                   ["%s = %s." % (" + ".join(_expanded(ns[r])), _c(ns[r]))],
                   missing=[r, 0])

    def t_table_missing_expanded():
        n = _distinct(max(d, 1))
        ps = _places_of(n)
        vals = [_c(((n // p) % 10) * p) for p, _w in ps]
        col = random.randint(0, len(ps) - 1)
        return _dt("This table splits %s into the value of each digit. What belongs "
                   "in the empty cell?" % _c(n),
                   [w.title() for _p, w in ps], [vals],
                   ((n // ps[col][0]) % 10) * ps[col][0],
                   ["The %s digit is %d, so it is worth %s."
                    % (ps[col][1], (n // ps[col][0]) % 10, vals[col])],
                   missing=[0, col])

    return _pick_t([t_which_digit, t_value, t_named_value, t_which_place,
                    t_expanded_to_std, t_missing_part, t_worth_more,
                    t_times_bigger, t_guess, t_change],
                   [t_chart_value, t_table_expanded, t_table_missing_expanded])


@skill("Y6.0.d", "Compare numbers to 10,000,000", S0)
def _(d=1):
    d = _d(d)

    def _pair():
        a = _bignum(d)
        if random.random() < 0.5:                 # close pair: same leading digits
            k = pick([10, 100, 1000, 10000])
            b = a + pick([-1, 1]) * random.randint(1, 9) * k
            if b <= 0:
                b = a + k
        else:
            b = _bignum(d)
        while b == a:
            b = _bignum(d)
        return a, b

    def t_greater():
        a, b = _pair()
        return _tb("Which is the greater number, %s or %s? Type the greater number."
                   % (_c(a), _c(b)), max(a, b), "int", {},
                   ["Compare the digits from the left.",
                    "%s is greater than %s." % (_c(max(a, b)), _c(min(a, b)))])

    def t_smaller():
        a, b = _pair()
        return _tb("Which is the smaller number, %s or %s? Type the smaller number."
                   % (_c(a), _c(b)), min(a, b), "int", {},
                   ["Compare the digits from the left.",
                    "%s is smaller than %s." % (_c(min(a, b)), _c(max(a, b)))])

    def t_symbol():
        a, b = _pair()
        sym = "<" if a < b else ">"
        return _wq("Type the correct symbol, < or >, to complete this statement:"
                   "   %s ___ %s" % (_c(a), _c(b)), sym,
                   ["%s %s %s." % (_c(a), sym, _c(b))], "< or >")

    def t_words_vs_numeral():
        a, b = _pair()
        return _tb("Which is greater, '%s' or %s? Type the greater number in numerals."
                   % (_wn(a), _c(b)), max(a, b), "int", {},
                   ["'%s' is %s." % (_wn(a), _c(a)),
                    "%s is greater." % _c(max(a, b))])

    def t_yes_no():
        a, b = _pair()
        claim = random.random() < 0.5
        stated = "greater than" if claim else "less than"
        truth = (a > b) if claim else (a < b)
        return _yn("Is this statement true? '%s is %s %s.' (type 'yes' or 'no')"
                   % (_c(a), stated, _c(b)), "yes" if truth else "no",
                   ["%s %s %s." % (_c(a), ">" if a > b else "<", _c(b)),
                    "So the statement is %s." % ("true" if truth else "false")])

    def t_missing_digit():
        head = random.randint(1, 8)
        tail = random.randint(0, 99999)
        dig = random.randint(1, 8)
        b = head * 1000000 + dig * 100000 + tail
        bigger = random.random() < 0.5
        ans = dig + 1 if bigger else dig - 1
        shown = "%d,_%s" % (head, "{:,}".format(tail + 100000)[1:])
        target = head * 1000000 + ans * 100000 + tail
        return _tb("One digit is missing from this number:   %s.  The number must be "
                   "%s than %s, and as close to %s as possible. What is the missing "
                   "digit?" % (shown, "greater" if bigger else "less", _c(b), _c(b)),
                   ans, "int", {},
                   ["The missing digit is in the hundred thousands place, where %s "
                    "has a %d." % (_c(b), dig),
                    "A %d makes the number %s, which is %s than %s."
                    % (ans, _c(target), "greater" if bigger else "less", _c(b))])

    def t_greatest_of_four():
        ns = [_bignum(d) for _ in range(4)]
        while len(set(ns)) < 4:
            ns = [_bignum(d) for _ in range(4)]
        return _tb("Which of these is the greatest?   %s" % _lst(ns), max(ns), "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The greatest is %s." % _c(max(ns))])

    def t_after_change():
        a = _bignum(max(d, 1))
        amt = pick([1000, 10000, 100000])
        b = a + amt + pick([-1, 1]) * random.randint(1, 9) * 100
        return _tb("%s adds %s to %s. Is the result greater or less than %s? Type "
                   "the result." % (pick(NAMES), _c(amt), _c(a), _c(b)),
                   a + amt, "int", {},
                   ["%s + %s = %s." % (_c(a), _c(amt), _c(a + amt)),
                    "%s is %s %s." % (_c(a + amt), "greater than" if a + amt > b
                                      else "less than", _c(b))])

    def t_between():
        a = random.randint(2, 8) * 1000000
        b = a + 1000000
        k = random.randint(2, 8)
        ans = a + k * 100000
        lo_b = a + (k - 1) * 100000
        hi_b = a + (k + 1) * 100000
        return _nlq("Place the number on the line that is greater than %s and less "
                    "than %s." % (_c(lo_b), _c(hi_b)), ans,
                    ["The only mark between %s and %s is %s."
                     % (_c(lo_b), _c(hi_b), _c(ans))],
                    step=100000, major=500000, lo=a, hi=b)

    def t_table():
        towns = random.sample(_TOWNS, 4)
        vals = [_bignum(max(d, 1)) for _ in range(4)]
        while len(set(vals)) < 4:
            vals = [_bignum(max(d, 1)) for _ in range(4)]
        rows = [[t, _c(v)] for t, v in zip(towns, vals)]
        big = random.random() < 0.5
        want = max(vals) if big else min(vals)
        return _dt("The table shows the population of four towns. Which town has the "
                   "%s population? Type that population." % ("largest" if big else "smallest"),
                   ["Town", "Population"], rows, want,
                   ["In order: %s." % _lst(sorted(vals)),
                    "%s has the %s population, %s."
                    % (towns[vals.index(want)], "largest" if big else "smallest", _c(want))])

    def t_bar():
        towns = random.sample(_TOWNS, 4)
        vals = random.sample(range(120, 980), 4)
        vals = [v * 1000 for v in vals]
        i, j = random.sample(range(4), 2)
        return _bar("The bar chart shows the number of visitors to four museums. "
                    "Which had more visitors, %s or %s? Type that number."
                    % (towns[i], towns[j]), towns, vals,
                    max(vals[i], vals[j]),
                    ["%s had %s and %s had %s."
                     % (towns[i], _c(vals[i]), towns[j], _c(vals[j])),
                     "The greater number is %s." % _c(max(vals[i], vals[j]))])

    def t_table_symbol():
        a, b = _pair()
        sym = "<" if a < b else ">"
        return _dt("Compare the two numbers in the table. Type the correct symbol, "
                   "< or >, for the empty cell.",
                   ["First number", "Symbol", "Second number"],
                   [[_c(a), sym, _c(b)]], sym,
                   ["%s %s %s." % (_c(a), sym, _c(b))], missing=[0, 1], atype="str")

    return _pick_t([t_greater, t_smaller, t_symbol, t_words_vs_numeral, t_yes_no,
                    t_missing_digit, t_greatest_of_four, t_after_change],
                   [t_between, t_table, t_bar, t_table_symbol])


@skill("Y6.0.e", "Order numbers to 10,000,000", S0)
def _(d=1):
    d = _d(d)
    k = {0: 4, 1: 5, 2: 6}[d]

    def _many():
        ns = [_bignum(d) for _ in range(k)]
        while len(set(ns)) < k:
            ns = [_bignum(d) for _ in range(k)]
        return ns

    def t_smallest():
        ns = _many()
        return _tb("Type the SMALLEST of these numbers:   %s" % _lst(ns),
                   min(ns), "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The smallest is %s." % _c(min(ns))])

    def t_largest():
        ns = _many()
        return _tb("Type the LARGEST of these numbers:   %s" % _lst(ns),
                   max(ns), "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The largest is %s." % _c(max(ns))])

    def t_nth_smallest():
        ns = _many()
        i = random.randint(2, k - 1)
        ans = sorted(ns)[i - 1]
        return _tb("Put these numbers in order, smallest first. Which number is %s?"
                   "   %s" % (ordinal(i), _lst(ns)), ans, "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The %s number is %s." % (ordinal(i), _c(ans))])

    def t_nth_largest():
        ns = _many()
        i = random.randint(2, k - 1)
        ans = sorted(ns, reverse=True)[i - 1]
        return _tb("Put these numbers in order, largest first. Which number is %s?"
                   "   %s" % (ordinal(i), _lst(ns)), ans, "int", {},
                   ["In order, largest first: %s." % _lst(sorted(ns, reverse=True)),
                    "The %s number is %s." % (ordinal(i), _c(ans))])

    def t_middle():
        ns = [_bignum(d) for _ in range(5)]
        while len(set(ns)) < 5:
            ns = [_bignum(d) for _ in range(5)]
        ans = sorted(ns)[2]
        return _tb("Order these five numbers. Which one is in the middle?   %s"
                   % _lst(ns), ans, "int", {},
                   ["In order: %s." % _lst(sorted(ns)),
                    "The middle number is %s." % _c(ans)])

    def t_words_mixed():
        ns = _many()[:4]
        shown = []
        for i, x in enumerate(ns):
            shown.append("'%s'" % _wn(x) if i % 2 else _c(x))
        return _tb("Type the largest of these numbers, in numerals:   %s"
                   % ", ".join(shown), max(ns), "int", {},
                   ["In numerals: %s." % _lst(ns),
                    "The largest is %s." % _c(max(ns))])

    def t_out_of_place():
        ns = sorted(_many())
        i = random.randint(1, len(ns) - 2)
        swapped = ns[:]
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        return _tb("These numbers should be in order, smallest first, but two have "
                   "been swapped:   %s.  Type the number that should come FIRST of "
                   "the two swapped ones." % _lst(swapped), ns[i], "int", {},
                   ["The correct order is %s." % _lst(ns),
                    "%s should come before %s." % (_c(ns[i]), _c(ns[i + 1]))])

    def t_fits_between():
        a = _bignum(max(d, 1))
        b = a + random.randint(20000, 90000)
        opts = [a - random.randint(1000, 9000), b + random.randint(1000, 9000),
                a + random.randint(1000, 9000)]
        ans = opts[2]
        random.shuffle(opts)
        return _tb("Which of these numbers lies between %s and %s?   %s"
                   % (_c(a), _c(b), _lst(opts)), ans, "int", {},
                   ["%s is greater than %s and less than %s."
                    % (_c(ans), _c(a), _c(b))])

    def t_set():
        ns = _many()[:4]
        lim = sorted(ns)[1]
        big = [x for x in ns if x > lim]
        return _setq("Type all of these numbers that are greater than %s:   %s"
                     % (_c(lim), _lst(ns)), big,
                     ["The numbers greater than %s are %s." % (_c(lim), _lst(sorted(big)))],
                     "e.g. 120000, 340000")

    def t_table():
        towns = random.sample(_TOWNS, 4)
        vals = _many()[:4]
        rows = [[t, _c(v)] for t, v in zip(towns, vals)]
        i = random.randint(1, 3)
        ans = sorted(vals)[i]
        return _dt("The table shows the population of four towns. Put the "
                   "populations in order, smallest first. Which population is %s?"
                   % ordinal(i + 1), ["Town", "Population"], rows, ans,
                   ["In order: %s." % _lst(sorted(vals)),
                    "The %s is %s." % (ordinal(i + 1), _c(ans))])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        vals = random.sample(range(110, 990), 4)
        vals = [v * 1000 for v in vals]
        i = random.randint(1, 3)
        ans = sorted(vals, reverse=True)[i]
        return _bar("The bar chart shows attendance at four events. Put the "
                    "attendances in order, largest first. Which is %s? Type that "
                    "number." % ordinal(i + 1), cats, vals, ans,
                    ["In order, largest first: %s." % _lst(sorted(vals, reverse=True)),
                     "The %s is %s." % (ordinal(i + 1), _c(ans))])

    def t_line():
        base = random.randint(1, 8) * 1000000
        ns = sorted(random.sample(range(1, 10), 3))
        ns = [base + x * 100000 for x in ns]
        i = random.randint(0, 2)
        shown = ns[:]
        random.shuffle(shown)
        word = "smallest" if i == 0 else ("largest" if i == 2 else "middle")
        return _nlq("Put these numbers in order: %s. Place the %s one on the number "
                    "line." % (_lst(shown), word), ns[i],
                    ["In order: %s." % _lst(ns),
                     "The %s is %s." % (word, _c(ns[i]))],
                    step=100000, major=500000, lo=base, hi=base + 1000000)

    return _pick_t([t_smallest, t_largest, t_nth_smallest, t_nth_largest, t_middle,
                    t_words_mixed, t_out_of_place, t_fits_between, t_set],
                   [t_table, t_bar, t_line])


@skill("Y6.0.f", "Round to a required degree of accuracy", S0)
def _(d=1):
    d = _d(d)
    UNITS = {0: [10, 100, 1000], 1: [10, 100, 1000, 10000, 100000],
             2: [1000, 10000, 100000, 1000000]}[d]

    def _pair():
        unit = pick(UNITS)
        lo = unit * 3
        hi = min(9999999, unit * 999)
        n = random.randint(max(lo, 1000), max(hi, 2000))
        return n, unit

    def t_bare():
        n, unit = _pair()
        return _tb("Round %s to the nearest %s." % (_c(n), _UNITW[unit]),
                   _r(n, unit), "int", {},
                   ["Look at the digit to the right of the %s place." % _UNITW[unit],
                    "%s to the nearest %s is %s." % (_c(n), _UNITW[unit], _c(_r(n, unit)))])

    def t_context():
        n = random.randint(11000, 89000)
        unit = pick([100, 1000])
        return _tb("%s people attended a concert. Round %s to the nearest %s."
                   % (_c(n), _c(n), _UNITW[unit]), _r(n, unit), "int", {},
                   ["%s to the nearest %s is %s."
                    % (_c(n), _UNITW[unit], _c(_r(n, unit)))])

    def t_money():
        p = random.randint(100000, 9999999)
        unit = pick([1000, 10000])
        return _tb("A charity raised £%s. Round that amount to the nearest £%s."
                   % (_c(p), _UNITW[unit]), _r(p, unit), "int", {"unit": "£"},
                   ["£%s to the nearest £%s is £%s."
                    % (_c(p), _UNITW[unit], _c(_r(p, unit)))])

    def t_smallest():
        unit = pick([100, 1000, 10000])
        target = random.randint(5, 90) * unit
        return _tb("A whole number rounds to %s when rounded to the nearest %s. "
                   "What is the SMALLEST whole number it could be?"
                   % (_c(target), _UNITW[unit]), target - unit // 2, "int", {},
                   ["Half of %s is %s." % (_UNITW[unit], _c(unit // 2)),
                    "%s − %s = %s." % (_c(target), _c(unit // 2), _c(target - unit // 2))])

    def t_largest():
        unit = pick([100, 1000, 10000])
        target = random.randint(5, 90) * unit
        return _tb("A whole number rounds to %s when rounded to the nearest %s. "
                   "What is the LARGEST whole number it could be?"
                   % (_c(target), _UNITW[unit]), target + unit // 2 - 1, "int", {},
                   ["Anything from %s upwards would round to the next %s."
                    % (_c(target + unit // 2), _UNITW[unit]),
                    "So the largest is %s." % _c(target + unit // 2 - 1)])

    def t_two_ways():
        n = random.randint(120000, 980000)
        u1, u2 = 1000, 100000
        return _tb("Round %s to the nearest %s, then round that answer to the "
                   "nearest %s. What is the final answer?"
                   % (_c(n), _UNITW[u1], _UNITW[u2]), _r(_r(n, u1), u2), "int", {},
                   ["%s to the nearest %s is %s." % (_c(n), _UNITW[u1], _c(_r(n, u1))),
                    "%s to the nearest %s is %s."
                    % (_c(_r(n, u1)), _UNITW[u2], _c(_r(_r(n, u1), u2)))])

    def t_which_rounds():
        unit = pick([100, 1000])
        target = random.randint(6, 90) * unit
        good = target + random.randint(-unit // 2 + 1, unit // 2 - 1)
        opts = [good,
                target + unit + random.randint(0, unit // 2 - 1),
                target - unit - random.randint(0, unit // 2 - 1),
                target + 2 * unit]
        random.shuffle(opts)
        return _tb("Which of these numbers rounds to %s when rounded to the nearest "
                   "%s?   %s" % (_c(target), _UNITW[unit], _lst(opts)), good, "int", {},
                   ["%s rounds to %s." % (_c(good), _c(target))])

    def t_yes_no():
        unit = pick([1000, 10000])
        n = random.randint(20, 900) * unit + random.randint(1, unit - 1)
        claim = _r(n, unit) if random.random() < 0.5 else _r(n, unit) + unit
        return _yn("%s says that %s rounded to the nearest %s is %s. Is that "
                   "correct? (type 'yes' or 'no')"
                   % (pick(NAMES), _c(n), _UNITW[unit], _c(claim)),
                   "yes" if claim == _r(n, unit) else "no",
                   ["%s to the nearest %s is %s."
                    % (_c(n), _UNITW[unit], _c(_r(n, unit)))])

    def t_line():
        unit = pick([1000, 10000, 100000])
        n = random.randint(4, 40) * unit + random.randint(1, unit - 1)
        ans = _r(n, unit)
        return _nlq("Round %s to the nearest %s and place your answer on the number "
                    "line." % (_c(n), _UNITW[unit]), ans,
                    ["%s lies between %s and %s."
                     % (_c(n), _c((n // unit) * unit), _c((n // unit) * unit + unit)),
                     "It rounds to %s." % _c(ans)],
                    step=unit, major=unit * 5)

    def t_line_which():
        unit = pick([1000, 10000])
        small = unit // 10
        base = random.randint(3, 30) * unit
        return _nlq("Place the largest number marked on this line that still rounds "
                    "DOWN to %s when rounded to the nearest %s."
                    % (_c(base), _UNITW[unit]), base + 4 * small,
                    ["Halfway to %s is %s, which would round up."
                     % (_c(base + unit), _c(base + unit // 2)),
                     "The largest mark below halfway is %s." % _c(base + 4 * small)],
                    step=small, major=unit // 2, lo=base, hi=base + unit)

    def t_table():
        unit = pick([1000, 10000, 100000])
        ns = sorted(random.sample(range(unit * 3, unit * 90), 4))
        rows = [[_c(x), _c(_r(x, unit))] for x in ns]
        r = random.randint(0, 3)
        return _dt("Complete the rounding table. What belongs in the empty cell?",
                   ["Number", "Rounded to the nearest %s" % _UNITW[unit]], rows,
                   _r(ns[r], unit),
                   ["%s to the nearest %s is %s."
                    % (_c(ns[r]), _UNITW[unit], _c(_r(ns[r], unit)))], missing=[r, 1])

    def t_table_two():
        n = random.randint(120000, 9800000)
        us = [1000, 10000, 100000, 1000000]
        row = [_c(_r(n, u)) for u in us]
        col = random.randint(0, 3)
        return _dt("The table rounds %s to different degrees of accuracy. What "
                   "belongs in the empty cell?" % _c(n),
                   ["Nearest %s" % _UNITW[u] for u in us], [row], _r(n, us[col]),
                   ["%s to the nearest %s is %s."
                    % (_c(n), _UNITW[us[col]], _c(_r(n, us[col])))], missing=[0, col])

    return _pick_t([t_bare, t_context, t_money, t_smallest, t_largest, t_two_ways,
                    t_which_rounds, t_yes_no],
                   [t_line, t_line_which, t_table, t_table_two])


@skill("Y6.0.g", "Roman numerals to 1,000", S0)
def _(d=1):
    d = _d(d)
    hi = {0: 200, 1: 600, 2: 1000}[d]
    PH = "e.g. MCXLIV"

    def num():
        return random.randint(1, hi)

    def year():
        return random.randint(1000, 2026) if d == 2 else random.randint(1500, 1999)

    def t_roman_to_num():
        n = num()
        return _tb("Write this Roman numeral as a number:   %s" % _rom(n), n, "int", {},
                   ["%s = %d." % (_rom(n), n)])

    def t_num_to_roman():
        n = num()
        return _wq("Write %d as a Roman numeral." % n, _rom(n),
                   ["%d is written %s." % (n, _rom(n))], PH)

    def t_year_to_num():
        y = year()
        return _tb("A building has the year %s carved above the door. Which year is "
                   "that?" % _rom(y), y, "int", {},
                   ["%s = %d." % (_rom(y), y)])

    def t_num_to_year():
        y = year()
        return _wq("Write the year %d in Roman numerals." % y, _rom(y),
                   ["%d = %s." % (y, _rom(y))], PH)

    def t_add():
        a, b = random.randint(1, hi // 2), random.randint(1, hi // 2)
        return _tb("Work this out and write the answer as an ordinary number:"
                   "   %s + %s" % (_rom(a), _rom(b)), a + b, "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d + %d = %d." % (a, b, a + b)])

    def t_subtract():
        a = random.randint(hi // 2, hi)
        b = random.randint(1, a - 1)
        return _tb("Work this out and write the answer as an ordinary number:"
                   "   %s − %s" % (_rom(a), _rom(b)), a - b, "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d − %d = %d." % (a, b, a - b)])

    def t_greater():
        a, b = random.sample(range(1, hi + 1), 2)
        return _tb("Which is greater, %s or %s? Write the answer as an ordinary "
                   "number." % (_rom(a), _rom(b)), max(a, b), "int", {},
                   ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b),
                    "%d is greater." % max(a, b)])

    def t_sequence():
        step = pick([1, 5, 10, 50, 100])
        start = random.randint(1, max(1, hi - 5 * step))
        terms = [start + i * step for i in range(4)]
        ans = terms[-1] + step
        return _wq("Continue this sequence of Roman numerals. What comes next?"
                   "   %s, ___" % ", ".join(_rom(t) for t in terms), _rom(ans),
                   ["The numbers are %s, going up in %ds." % (_lst(terms), step),
                    "%d + %d = %d, which is %s." % (terms[-1], step, ans, _rom(ans))],
                   PH)

    def t_how_long_ago():
        y = year()
        now = 2026
        return _tb("A church was built in the year %s. How many years ago was that, "
                   "counting from 2026?" % _rom(y), now - y, "int", {"unit": "years"},
                   ["%s = %d." % (_rom(y), y),
                    "%d − %d = %d." % (now, y, now - y)])

    def t_largest_of_three():
        ns = random.sample(range(1, hi + 1), 3)
        return _tb("Which of these Roman numerals is the largest? Write it as an "
                   "ordinary number.   %s" % ", ".join(_rom(x) for x in ns),
                   max(ns), "int", {},
                   ["In order: %s." % ", ".join("%s = %d" % (_rom(x), x)
                                                for x in sorted(ns)),
                    "The largest is %d." % max(ns)])

    def t_table():
        ns = sorted(random.sample(range(1, hi + 1), 4))
        want_roman = random.random() < 0.5
        rows = [[str(x), _rom(x)] for x in ns]
        r = random.randint(0, 3)
        if want_roman:
            return _dt("Complete the table. What Roman numeral belongs in the empty "
                       "cell?", ["Number", "Roman numeral"], rows, _rom(ns[r]),
                       ["%d is written %s." % (ns[r], _rom(ns[r]))],
                       missing=[r, 1], atype="str")
        return _dt("Complete the table. What ordinary number belongs in the empty "
                   "cell?", ["Number", "Roman numeral"], rows, ns[r],
                   ["%s = %d." % (_rom(ns[r]), ns[r])], missing=[r, 0])

    def t_table_years():
        ys = sorted(random.sample(range(1200, 2020), 4))
        events = random.sample(["Castle built", "Bridge opened", "Abbey founded",
                                "Town hall built", "Harbour built", "Mill opened"], 4)
        rows = [[e, _rom(y)] for e, y in zip(events, ys)]
        r = random.randint(0, 3)
        return _dt("The table shows dates written in Roman numerals. In which year "
                   "did '%s' happen? Type an ordinary number." % events[r],
                   ["Event", "Year"], rows, ys[r],
                   ["%s = %d." % (_rom(ys[r]), ys[r])])

    def t_line():
        n = random.randint(2, 18) * 50
        return _nlq("The Roman numeral %s is written on a number line. Place it."
                    % _rom(n), n, ["%s = %d." % (_rom(n), n)], step=50, major=250)

    return _pick_t([t_roman_to_num, t_num_to_roman, t_year_to_num, t_num_to_year,
                    t_add, t_subtract, t_greater, t_sequence, t_how_long_ago,
                    t_largest_of_three],
                   [t_table, t_table_years, t_line])


@skill("Y6.0.h", "Negative numbers in context", S0)
def _(d=1):
    d = _d(d)
    R = {0: 10, 1: 20, 2: 50}[d]

    def _temp():
        return random.randint(-R, R)

    def t_colder():
        a, b = _temp(), _temp()
        while a == b:
            b = _temp()
        return _tb("On Monday the temperature was %d °C and on Tuesday it was %d °C. "
                   "Which was the colder temperature? Type that temperature."
                   % (a, b), min(a, b), "int", {"unit": "°C"},
                   ["%d is %s %d on a number line." % (min(a, b), "left of", max(a, b)),
                    "So %d °C is colder." % min(a, b)])

    def t_warmer():
        a, b = _temp(), _temp()
        while a == b:
            b = _temp()
        return _tb("Which is the warmer temperature, %d °C or %d °C? Type that "
                   "temperature." % (a, b), max(a, b), "int", {"unit": "°C"},
                   ["%d is further right on a number line than %d."
                    % (max(a, b), min(a, b)),
                    "So %d °C is warmer." % max(a, b)])

    def t_symbol():
        a, b = _temp(), _temp()
        while a == b:
            b = _temp()
        sym = "<" if a < b else ">"
        return _wq("Type the correct symbol, < or >:   %d ___ %d" % (a, b), sym,
                   ["On a number line %d comes %s %d."
                    % (a, "before" if a < b else "after", b),
                    "%d %s %d." % (a, sym, b)], "< or >")

    def t_order_smallest():
        ns = random.sample(range(-R, R + 1), 5)
        return _tb("Type the SMALLEST of these integers:   %s"
                   % ", ".join(str(x) for x in ns), min(ns), "int", {},
                   ["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                    "The smallest is %d." % min(ns)])

    def t_nth():
        ns = random.sample(range(-R, R + 1), 5)
        i = random.randint(2, 4)
        ans = sorted(ns)[i - 1]
        return _tb("Put these integers in order, smallest first. Which is %s?   %s"
                   % (ordinal(i), ", ".join(str(x) for x in ns)), ans, "int", {},
                   ["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                    "The %s is %d." % (ordinal(i), ans)])

    def t_bank():
        who1, who2 = random.sample(NAMES, 2)
        a = -random.randint(5, 200)
        b = -random.randint(5, 200)
        while a == b:
            b = -random.randint(5, 200)
        worse = min(a, b)
        name = who1 if a == worse else who2
        return _tb("%s has a bank balance of −£%d and %s has a balance of −£%d. "
                   "Whose balance is further below zero? Type that balance as a "
                   "negative number." % (who1, -a, who2, -b), worse, "int",
                   {"unit": "£"},
                   ["%d is further from zero on the negative side than %d."
                    % (worse, max(a, b)),
                    "%s has the balance of £%d." % (name, worse)])

    def t_floors():
        a = -random.randint(1, 4)
        b = random.randint(1, 6)
        return _tb("A lift can reach floor %d (a basement) and floor %d. Which floor "
                   "is lower? Type that floor number." % (a, b), a, "int", {},
                   ["%d is below zero, so it is lower than %d." % (a, b)])

    def t_less_than():
        lim = -random.randint(1, R // 2)
        ns = random.sample(range(-R, R + 1), 5)
        good = [x for x in ns if x < lim]
        if not good:
            ns[0] = lim - 1
            good = [x for x in ns if x < lim]
        return _setq("Type all of these integers that are less than %d:   %s"
                     % (lim, ", ".join(str(x) for x in ns)), good,
                     ["The integers less than %d are %s."
                      % (lim, ", ".join(str(x) for x in sorted(good)))],
                     "e.g. -8, -5")

    def t_count_back():
        start = random.randint(1, 6)
        step = random.randint(2, 5)
        k = random.randint(2, 4)
        ans = start - step * k
        return _tb("Count back in %ds from %d. What is the %s number you say?"
                   % (step, start, ordinal(k)), ans, "int", {},
                   ["%d − %d = %d." % (start, step * k, ans)])

    def t_line():
        ans = random.randint(-min(R, 12), -1)
        return _nlq("Place %d on the number line." % ans, ans,
                    ["%d is %d to the left of zero." % (ans, -ans)],
                    step=1, major=5)

    def t_line_order():
        L = min(R, 9)
        ns = random.sample(range(-L, L + 1), 3)
        i = random.randint(0, 2)
        ans = sorted(ns)[i]
        return _nlq("Put %s in order, smallest first, then place the %s number on "
                    "the line." % (", ".join(str(x) for x in ns), ordinal(i + 1)),
                    ans, ["In order: %s." % ", ".join(str(x) for x in sorted(ns)),
                          "The %s number is %d." % (ordinal(i + 1), ans)],
                    step=1, major=5, lo=min(ns) - 2, hi=max(ns) + 2)

    def t_table():
        cities = random.sample(_CITIES, 4)
        temps = random.sample(range(-R, R + 1), 4)
        rows = [[c, "%d °C" % t] for c, t in zip(cities, temps)]
        cold = random.random() < 0.5
        ans = min(temps) if cold else max(temps)
        return _dt("The table shows midnight temperatures. Which city was the %s? "
                   "Type that temperature." % ("coldest" if cold else "warmest"),
                   ["City", "Temperature"], rows, ans,
                   ["In order: %s." % ", ".join("%d" % t for t in sorted(temps)),
                    "The %s was %s at %d °C."
                    % ("coldest" if cold else "warmest",
                       cities[temps.index(ans)], ans)])

    def t_graph():
        hrs = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
        temps = [random.randint(-R, R) for _ in range(6)]
        cold = random.random() < 0.5
        ans = min(temps) if cold else max(temps)
        return _lg("The graph shows the temperature through one day. What was the "
                   "%s temperature?" % ("lowest" if cold else "highest"),
                   list(zip(hrs, temps)), ans,
                   ["The readings are %s." % ", ".join(str(t) for t in temps),
                    "The %s is %d °C." % ("lowest" if cold else "highest", ans)])

    def t_opposite():
        n = random.randint(1, R)
        x = -n if random.random() < 0.5 else n
        return _tb("Opposite integers are the same distance from zero, one on each "
                   "side of zero. What is the opposite of %d?" % x, -x, "int", {},
                   ["%d is %d away from zero." % (x, n),
                    "The opposite integer is %d away from zero on the other side, "
                    "which is %d." % (n, -x)])

    def t_opposite_distance():
        n = random.randint(1, R)
        x = -n if random.random() < 0.5 else n
        return _tb("The integers %d and %d are opposite integers. How far from zero "
                   "is each of them? Type the distance." % (x, -x), n, "int", {},
                   ["Opposite integers are the same distance from zero.",
                    "%d and %d are both %d away from zero." % (x, -x, n)])

    def t_opposite_line():
        n = random.randint(1, min(R, 8))
        x = -n if random.random() < 0.5 else n
        return _nlq("Place the opposite of %d on the number line." % x, -x,
                    ["Opposite integers are the same distance from zero, one on "
                     "each side of zero.",
                     "The opposite of %d is %d." % (x, -x)],
                    step=1, major=5, lo=-(n + 3), hi=n + 3)

    return _pick_t([t_colder, t_warmer, t_symbol, t_order_smallest, t_nth, t_bank,
                    t_floors, t_less_than, t_count_back, t_opposite,
                    t_opposite_distance],
                   [t_line, t_line_order, t_table, t_graph, t_opposite_line])


@skill("Y6.0.i", "Intervals across zero", S0)
def _(d=1):
    d = _d(d)
    R = {0: 10, 1: 20, 2: 40}[d]

    def t_rise():
        start = -random.randint(1, R)
        rise = random.randint(abs(start) + 1, abs(start) + R)
        return _tb("At dawn the temperature was %d °C. By midday it had risen by "
                   "%d °C. What was the temperature at midday?" % (start, rise),
                   start + rise, "int", {"unit": "°C"},
                   ["From %d °C it takes %d °C to reach 0 °C." % (start, -start),
                    "There are %d °C left, so the temperature is %d °C."
                    % (rise + start, start + rise)])

    def t_fall():
        start = random.randint(1, R)
        fall = start + random.randint(1, R)
        return _tb("At noon the temperature was %d °C. By midnight it had fallen by "
                   "%d °C. What was the temperature at midnight?" % (start, fall),
                   start - fall, "int", {"unit": "°C"},
                   ["From %d °C it takes %d °C to reach 0 °C." % (start, start),
                    "There are %d °C left to fall, so the temperature is %d °C."
                    % (fall - start, start - fall)])

    def t_difference():
        a = -random.randint(1, R)
        b = random.randint(1, R)
        return _tb("What is the difference between %d °C and %d °C?" % (a, b),
                   b - a, "int", {"unit": "°C"},
                   ["From %d °C up to 0 °C is %d °C." % (a, -a),
                    "From 0 °C up to %d °C is %d °C." % (b, b),
                    "%d + %d = %d." % (-a, b, b - a)])

    def t_how_much_rise():
        a = -random.randint(1, R)
        b = random.randint(1, R)
        return _tb("The temperature is %d °C. How many degrees must it rise to reach "
                   "%d °C?" % (a, b), b - a, "int", {"unit": "°C"},
                   ["%d − (%d) = %d." % (b, a, b - a)])

    def t_how_much_fall():
        a = random.randint(1, R)
        b = -random.randint(1, R)
        return _tb("The temperature is %d °C. How many degrees must it fall to reach "
                   "%d °C?" % (a, b), a - b, "int", {"unit": "°C"},
                   ["From %d °C down to 0 °C is %d °C." % (a, a),
                    "Then a further %d °C, so %d + %d = %d." % (-b, a, -b, a - b)])

    def t_two_step():
        start = random.randint(1, R)
        fall = start + random.randint(2, R)
        rise = random.randint(1, R)
        return _tb("The temperature starts at %d °C, falls by %d °C and then rises "
                   "by %d °C. What is the final temperature?" % (start, fall, rise),
                   start - fall + rise, "int", {"unit": "°C"},
                   ["%d − %d = %d." % (start, fall, start - fall),
                    "%d + %d = %d." % (start - fall, rise, start - fall + rise)])

    def t_start():
        end = random.randint(1, R)
        rise = end + random.randint(1, R)
        return _tb("After rising by %d °C the temperature reached %d °C. What was "
                   "the temperature before the rise?" % (rise, end), end - rise,
                   "int", {"unit": "°C"},
                   ["Work backwards: %d − %d = %d." % (end, rise, end - rise)])

    def t_lift():
        a = -random.randint(1, 4)
        b = random.randint(1, 8)
        return _tb("A lift is at floor %d. It goes up %d floors. Which floor does "
                   "the lift reach?" % (a, b - a), b, "int", {},
                   ["%d + %d = %d." % (a, b - a, b)])

    def t_bank():
        who = pick(NAMES)
        bal = -random.randint(10, 200)
        pay = -bal + random.randint(5, 200)
        return _tb("%s has a bank balance of −£%d and then pays in £%d. What is the "
                   "new balance in pounds?" % (who, -bal, pay), bal + pay, "int",
                   {"unit": "£"},
                   ["It takes £%d to reach zero." % (-bal),
                    "£%d − £%d = £%d." % (pay, -bal, bal + pay)])

    def t_line():
        L = min(R, 8)
        start = -random.randint(1, L)
        rise = random.randint(abs(start) + 1, abs(start) + L)
        ans = start + rise
        return _nlq("The temperature is %d °C and rises by %d °C. Place the new "
                    "temperature on the number line." % (start, rise), ans,
                    ["%d + %d = %d." % (start, rise, ans)],
                    step=1, major=5, lo=start - 2, hi=ans + 2)

    def t_line_diff():
        L = min(R, 8)
        start = random.randint(1, L)
        fall = start + random.randint(1, L)
        ans = start - fall
        return _nlq("The temperature is %d °C and falls by %d °C. Place the new "
                    "temperature on the number line." % (start, fall), ans,
                    ["From %d °C it takes %d °C to reach 0 °C." % (start, start),
                     "There are %d °C still to fall, so the new temperature is %d °C."
                     % (fall - start, ans)],
                    step=1, major=5, lo=ans - 2, hi=start + 2)

    def t_table():
        cities = random.sample(_CITIES, 4)
        night = [random.randint(-R, -1) for _ in range(4)]
        day = [n + random.randint(abs(n) + 1, abs(n) + R) for n in night]
        rows = [[c, "%d °C" % n, "%d °C" % dd]
                for c, n, dd in zip(cities, night, day)]
        i = random.randint(0, 3)
        return _dt("The table shows night and day temperatures. By how many degrees "
                   "did the temperature rise in %s?" % cities[i],
                   ["City", "Night", "Day"], rows, day[i] - night[i],
                   ["%d − (%d) = %d." % (day[i], night[i], day[i] - night[i])])

    def t_graph():
        hrs = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
        temps = [random.randint(-R, -1) for _ in range(3)] + \
                [random.randint(1, R) for _ in range(3)]
        i = random.randint(0, 2)
        j = random.randint(3, 5)
        return _lg("The graph shows the temperature through one day. How many "
                   "degrees warmer was it at %s than at %s?" % (hrs[j], hrs[i]),
                   list(zip(hrs, temps)), temps[j] - temps[i],
                   ["At %s it was %d °C and at %s it was %d °C."
                    % (hrs[i], temps[i], hrs[j], temps[j]),
                    "%d − (%d) = %d." % (temps[j], temps[i], temps[j] - temps[i])])

    def t_sub_line():
        L = min(R, 8)
        a = random.randint(-L, L)
        b = random.randint(1, L)
        ans = a - b
        return _nlq("Use the number line to subtract the integers:   %d − %d   "
                    "Place the answer on the number line." % (a, b), ans,
                    ["Start at %d and count %d steps to the left." % (a, b),
                     "%d − %d = %d." % (a, b, ans)],
                    step=1, major=5, lo=min(ans, a) - 2, hi=max(ans, a) + 2)

    def t_sub_line_neg():
        L = min(R, 8)
        a = random.randint(-L, L)
        b = random.randint(1, L)
        ans = a + b
        return _nlq("Use the number line to subtract the integers:   %d − (−%d)   "
                    "Place the answer on the number line." % (a, b), ans,
                    ["Subtracting a negative integer moves to the right.",
                     "%d − (−%d) = %d + %d = %d." % (a, b, a, b, ans)],
                    step=1, major=5, lo=min(ans, a) - 2, hi=max(ans, a) + 2)

    return _pick_t([t_rise, t_fall, t_difference, t_how_much_rise, t_how_much_fall,
                    t_two_step, t_start, t_lift, t_bank],
                   [t_line, t_line_diff, t_table, t_graph, t_sub_line,
                    t_sub_line_neg])


@skill("Y6.0.j", "Place-value and parity reasoning", S0)
def _(d=1):
    d = _d(d)

    def t_how_many_thousands():
        n = random.randint(11, 9999) * 1000 + (0 if d == 0 else random.randint(0, 999))
        return _tb("How many WHOLE thousands are there in %s?" % _c(n),
                   n // 1000, "int", {"unit": "thousands"},
                   ["%s ÷ 1,000 = %s remainder %d." % (_c(n), _c(n // 1000), n % 1000),
                    "So there are %s whole thousands." % _c(n // 1000)])

    def t_how_many_hundreds():
        n = random.randint(101, 99999) * 100 if d == 2 else random.randint(101, 9999) * 100
        return _tb("How many hundreds make %s?" % _c(n), n // 100, "int",
                   {"unit": "hundreds"}, ["%s ÷ 100 = %s." % (_c(n), _c(n // 100))])

    def t_parity_sum():
        a, b = pick([("odd", "odd"), ("odd", "even"), ("even", "even")])
        ans = "even" if a == b else "odd"
        x = pick([3, 5, 7, 9] if a == "odd" else [2, 4, 6, 8])
        y = pick([3, 5, 7, 9] if b == "odd" else [2, 4, 6, 8])
        return _wq("Is the answer to 'an %s number + an %s number' always even or "
                   "always odd? (type 'even' or 'odd')" % (a, b), ans,
                   ["Try an example: %d + %d = %d, which is %s." % (x, y, x + y, ans),
                    "%s + %s is always %s." % (a, b, ans)], "even / odd")

    def t_parity_product():
        a, b = pick([("odd", "odd"), ("odd", "even"), ("even", "even")])
        ans = "odd" if (a == "odd" and b == "odd") else "even"
        x = pick([3, 5, 7, 9] if a == "odd" else [2, 4, 6, 8])
        y = pick([3, 5, 7, 9] if b == "odd" else [2, 4, 6, 8])
        return _wq("Is the answer to 'an %s number × an %s number' always even or "
                   "always odd? (type 'even' or 'odd')" % (a, b), ans,
                   ["Try an example: %d × %d = %d, which is %s." % (x, y, x * y, ans),
                    "An even factor always makes the product even.",
                    "%s × %s is always %s." % (a, b, ans)], "even / odd")

    def t_parity_apply():
        a, b = _bignum(d), _bignum(d)
        op = pick(["+", "−", "×"])
        if op == "−" and a < b:
            a, b = b, a
        val = a + b if op == "+" else (a - b if op == "−" else a * b)
        ans = "even" if val % 2 == 0 else "odd"
        return _wq("Without working out the exact answer, is %s %s %s even or odd? "
                   "(type 'even' or 'odd')" % (_c(a), op, _c(b)), ans,
                   ["%s is %s and %s is %s."
                    % (_c(a), "even" if a % 2 == 0 else "odd",
                       _c(b), "even" if b % 2 == 0 else "odd"),
                    "So the answer is %s." % ans], "even / odd")

    def t_cards_even():
        digs = random.sample([2, 4, 6, 8], 2) + random.sample([1, 3, 5, 7, 9], 4)
        last = min(x for x in digs if x % 2 == 0)
        rest = sorted([x for x in digs if x != last], reverse=True)
        ans = int("".join(str(x) for x in rest + [last]))
        return _tb("Use each of these digit cards once to make the LARGEST possible "
                   "EVEN number:   %s" % ", ".join(str(x) for x in digs), ans, "int", {},
                   ["An even number must end in an even digit, so use the smaller "
                    "even card, %d, in the ones place." % last,
                    "Put the remaining digits in order, largest first: %s." % _c(ans)])

    def t_cards_odd():
        digs = random.sample([1, 3, 5, 7, 9], 2) + random.sample([2, 4, 6, 8], 4)
        last = max(x for x in digs if x % 2 == 1)
        rest = sorted([x for x in digs if x != last])
        ans = int("".join(str(x) for x in rest + [last]))
        return _tb("Use each of these digit cards once to make the SMALLEST possible "
                   "ODD number:   %s" % ", ".join(str(x) for x in digs), ans, "int", {},
                   ["An odd number must end in an odd digit, so use the larger odd "
                    "card, %d, in the ones place." % last,
                    "Put the remaining digits in order, smallest first: %s." % _c(ans)])

    def t_which_even():
        want_even = random.random() < 0.5
        ns = []
        for i in range(4):
            x = _bignum(d)
            odd_wanted = want_even if i else (not want_even)
            # i == 0 is the odd one out; make its parity the opposite of the rest
            if (x % 2 == 1) != odd_wanted:
                x += 1
            ns.append(x)
        target = ns[0]
        random.shuffle(ns)
        return _tb("Only ONE of these numbers is %s. Which one?   %s"
                   % ("even" if want_even else "odd", _lst(ns)), target, "int", {},
                   ["Look at the ones digit of each number.",
                    "%s is the %s one." % (_c(target), "even" if want_even else "odd")])

    def t_ten_more():
        n = _bignum(max(d, 1))
        amt = pick([10, 1000, 10000, 100000])
        return _tb("What is %s more than %s?" % (_c(amt), _c(n)), n + amt, "int", {},
                   ["%s + %s = %s." % (_c(n), _c(amt), _c(n + amt))])

    def t_which_digit_changes():
        n = random.randint(1000000, 8999999)
        amt = pick([1000, 10000, 100000])
        place = {1000: "thousands", 10000: "ten thousands",
                 100000: "hundred thousands"}[amt]
        return _wq("When %s is added to %s, which place-value column changes first? "
                   "(type 'thousands', 'ten thousands' or 'hundred thousands')"
                   % (_c(amt), _c(n)), place,
                   ["%s is 1 in the %s column." % (_c(amt), place)],
                   "thousands / ten thousands / hundred thousands")

    def t_io():
        amt = pick([100, 1000, 10000])
        up = random.random() < 0.5
        ins = sorted(random.sample(range(120000, 980000), 4))
        rows = [[i, i + amt if up else i - amt] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is %s %s." % ("add" if up else "subtract", _c(amt)),
                    "%s %s %s = %s." % (_c(rows[miss][0]), "+" if up else "−",
                                        _c(amt), _c(rows[miss][1]))],
                   rule="%s %s" % ("+" if up else "−", _c(amt)))

    def t_table_parity():
        ns = [_bignum(d) for _ in range(4)]
        rows = [[_c(x), "even" if x % 2 == 0 else "odd"] for x in ns]
        r = random.randint(0, 3)
        return _dt("Complete the table. Is the number in that row even or odd? "
                   "(type 'even' or 'odd')", ["Number", "Even or odd"], rows,
                   "even" if ns[r] % 2 == 0 else "odd",
                   ["The ones digit of %s is %d." % (_c(ns[r]), ns[r] % 10),
                    "So %s is %s." % (_c(ns[r]),
                                      "even" if ns[r] % 2 == 0 else "odd")],
                   missing=[r, 1], atype="str")

    def t_table_thousands():
        ns = sorted(random.sample(range(120000, 9800000), 3))
        rows = [[_c(x), _c(x // 1000), _c(x // 100)] for x in ns]
        r = random.randint(0, 2)
        col = pick([1, 2])
        ans = ns[r] // 1000 if col == 1 else ns[r] // 100
        return _dt("The table counts whole thousands and whole hundreds in each "
                   "number. What belongs in the empty cell?",
                   ["Number", "Whole thousands", "Whole hundreds"], rows, ans,
                   ["%s ÷ %s = %s (ignoring the remainder)."
                    % (_c(ns[r]), "1,000" if col == 1 else "100", _c(ans))],
                   missing=[r, col])

    def t_choose_sum():
        mult = {0: 10, 1: 5, 2: 25}[d]
        pool = [k * mult for k in range(2, 40)]
        a, b = random.sample(pool, 2)
        s = a + b
        nums = _pair_list(a, b, pool, lambda x, y: x + y == s)
        return _setq("Choose the TWO numbers from this list that have a sum of %d, "
                     "then type both of them:   %s"
                     % (s, ", ".join(str(x) for x in nums)), [a, b],
                     ["%d + %d = %d." % (min(a, b), max(a, b), s),
                      "No other pair in the list has that sum."],
                     "type two numbers")

    def t_choose_difference():
        mult = {0: 10, 1: 5, 2: 25}[d]
        pool = [k * mult for k in range(2, 40)]
        a, b = random.sample(pool, 2)
        a, b = max(a, b), min(a, b)
        diff = a - b
        nums = _pair_list(a, b, pool, lambda x, y: abs(x - y) == diff)
        return _setq("Choose the TWO numbers from this list that have a difference "
                     "of %d, then type both of them:   %s"
                     % (diff, ", ".join(str(x) for x in nums)), [a, b],
                     ["%d − %d = %d." % (a, b, diff),
                      "No other pair in the list has that difference."],
                     "type two numbers")

    def t_venn():
        clubs = random.sample(["Football club", "Chess club", "Art club",
                               "Judo club", "Coding club", "Drama club"], 2)
        A, B = clubs
        a_only = random.randint(4, 20)
        b_only = random.randint(4, 20)
        both = random.randint(2, 12)
        none = random.randint(0, 8)
        rows = [["%s only" % A, str(a_only)],
                ["Both %s and %s" % (A, B), str(both)],
                ["%s only" % B, str(b_only)],
                ["Neither club", str(none)]]
        kind = pick(["a", "b", "total", "one"])
        if kind == "a":
            qtext = "How many pupils are in %s altogether?" % A
            ans = a_only + both
            sol = ["%s only (%d) and both clubs (%d) are all in %s."
                   % (A, a_only, both, A),
                   "%d + %d = %d." % (a_only, both, ans)]
        elif kind == "b":
            qtext = "How many pupils are in %s altogether?" % B
            ans = b_only + both
            sol = ["%s only (%d) and both clubs (%d) are all in %s."
                   % (B, b_only, both, B),
                   "%d + %d = %d." % (b_only, both, ans)]
        elif kind == "total":
            qtext = "How many pupils are in the class altogether?"
            ans = a_only + b_only + both + none
            sol = ["Add all four regions of the Venn diagram.",
                   "%d + %d + %d + %d = %d."
                   % (a_only, both, b_only, none, ans)]
        else:
            qtext = "How many pupils are in exactly one of the two clubs?"
            ans = a_only + b_only
            sol = ["Exactly one club means the two 'only' regions.",
                   "%d + %d = %d." % (a_only, b_only, ans)]
        return _dt("A Venn diagram has two overlapping rings, one for %s and one "
                   "for %s. The table gives the number of pupils in each region of "
                   "the Venn diagram. %s" % (A, B, qtext),
                   ["Region of the Venn diagram", "Number of pupils"], rows,
                   ans, sol, atype="int")

    return _pick_t([t_how_many_thousands, t_how_many_hundreds, t_parity_sum,
                    t_parity_product, t_parity_apply, t_cards_even, t_cards_odd,
                    t_which_even, t_ten_more, t_which_digit_changes,
                    t_choose_sum, t_choose_difference],
                   [t_io, t_table_parity, t_table_thousands, t_venn])


# ================================================================== 6.1 ======
def _op(d):
    """An operand of the right size for column arithmetic at this difficulty."""
    if d == 0:
        return random.randint(1001, 99999)
    if d == 1:
        return random.randint(100001, 999999)
    return random.randint(1000001, 9999999)


@skill("Y6.1.a", "Column addition and subtraction to 10,000,000", S1)
def _(d=1):
    d = _d(d)

    def t_add():
        a, b = _op(d), _op(d)
        return _tb("Work out:   %s + %s" % (_c(a), _c(b)), a + b, "int", {},
                   ["Line up the digits in their place-value columns.",
                    "%s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_sub():
        a, b = _op(d), _op(d)
        a, b = max(a, b), min(a, b)
        return _tb("Work out:   %s − %s" % (_c(a), _c(b)), a - b, "int", {},
                   ["Line up the digits in their place-value columns.",
                    "%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_three():
        a, b, cc = _op(d), _op(d), _op(d)
        return _tb("Work out:   %s + %s + %s" % (_c(a), _c(b), _c(cc)),
                   a + b + cc, "int", {},
                   ["%s + %s = %s." % (_c(a), _c(b), _c(a + b)),
                    "%s + %s = %s." % (_c(a + b), _c(cc), _c(a + b + cc))])

    def t_missing_addend():
        a, b = _op(d), _op(d)
        return _tb("Find the missing number:   %s + ___ = %s" % (_c(a), _c(a + b)),
                   b, "int", {},
                   ["Subtract to find the missing part.",
                    "%s − %s = %s." % (_c(a + b), _c(a), _c(b))])

    def t_missing_start():
        a, b = _op(d), _op(d)
        a = max(a, b) + b
        return _tb("Find the missing number:   ___ − %s = %s" % (_c(b), _c(a - b)),
                   a, "int", {},
                   ["Add to undo the subtraction.",
                    "%s + %s = %s." % (_c(a - b), _c(b), _c(a))])

    def t_population():
        t1, t2 = random.sample(_TOWNS, 2)
        p1, p2 = _op(max(d, 1)), _op(max(d, 1))
        p1, p2 = max(p1, p2), min(p1, p2)
        if random.random() < 0.5:
            return _tb("%s has a population of %s and %s has a population of %s. "
                       "What is the total population of the two towns?"
                       % (t1, _c(p1), t2, _c(p2)), p1 + p2, "int", {"unit": "people"},
                       ["%s + %s = %s." % (_c(p1), _c(p2), _c(p1 + p2))])
        return _tb("%s has a population of %s and %s has a population of %s. How "
                   "many more people live in %s?" % (t1, _c(p1), t2, _c(p2), t1),
                   p1 - p2, "int", {"unit": "people"},
                   ["%s − %s = %s." % (_c(p1), _c(p2), _c(p1 - p2))])

    def t_money():
        who = pick(NAMES)
        raised = random.randint(100000, 999999)
        target = raised + random.randint(1000, 99999)
        return _tb("A charity wants to raise £%s and has raised £%s so far. How much "
                   "more must the charity raise?" % (_c(target), _c(raised)),
                   target - raised, "int", {"unit": "£"},
                   ["£%s − £%s = £%s." % (_c(target), _c(raised), _c(target - raised))]) \
            if random.random() < 0.5 else \
            _tb("%s has £%s in a savings account and pays in another £%s. How much "
                "is in the account now?" % (who, _c(raised), _c(target - raised)),
                target, "int", {"unit": "£"},
                ["£%s + £%s = £%s." % (_c(raised), _c(target - raised), _c(target))])

    def t_inverse_check():
        a, b = _op(d), _op(d)
        a, b = max(a, b), min(a, b)
        return _tb("%s works out %s − %s = %s. Which addition checks this answer? "
                   "Type the total that the addition should give."
                   % (pick(NAMES), _c(a), _c(b), _c(a - b)), a, "int", {},
                   ["The inverse check is %s + %s." % (_c(a - b), _c(b)),
                    "%s + %s = %s, which matches the starting number."
                    % (_c(a - b), _c(b), _c(a))])

    def t_multi():
        a, b = _op(d), _op(d)
        cc = random.randint(1000, min(a + b, 999999))
        return _tb("Work out:   %s + %s − %s" % (_c(a), _c(b), _c(cc)),
                   a + b - cc, "int", {},
                   ["%s + %s = %s." % (_c(a), _c(b), _c(a + b)),
                    "%s − %s = %s." % (_c(a + b), _c(cc), _c(a + b - cc))])

    def t_table():
        items = random.sample(["Salaries", "Building work", "Equipment", "Transport",
                               "Books", "Repairs"], 3)
        vals = [_op(max(d, 1)) for _ in range(3)]
        rows = [[i, "£" + _c(v)] for i, v in zip(items, vals)]
        rows.append(["Total", "£" + _c(sum(vals))])
        r = random.randint(0, 2)
        return _dt("The table shows a school's spending. What amount in pounds "
                   "belongs in the empty cell?", ["Item", "Amount"], rows, vals[r],
                   ["The three items must add up to the total.",
                    "£%s − £%s − £%s = £%s."
                    % (_c(sum(vals)), _c(vals[(r + 1) % 3]), _c(vals[(r + 2) % 3]),
                       _c(vals[r]))], missing=[r, 1])

    def t_table_diff():
        years = ["2022", "2023", "2024", "2025"]
        vals = [random.randint(100000, 999999) for _ in range(4)]
        rows = [[y, _c(v)] for y, v in zip(years, vals)]
        i, j = sorted(random.sample(range(4), 2))
        return _dt("The table shows how many visitors a museum had each year. How "
                   "many more visitors were there in %s than in %s?"
                   % (years[j] if vals[j] > vals[i] else years[i],
                      years[i] if vals[j] > vals[i] else years[j]),
                   ["Year", "Visitors"], rows, abs(vals[j] - vals[i]),
                   ["%s − %s = %s." % (_c(max(vals[i], vals[j])),
                                       _c(min(vals[i], vals[j])),
                                       _c(abs(vals[j] - vals[i])))])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        vals = [random.randint(120, 980) * 100 for _ in range(4)]
        i, j = sorted(random.sample(range(4), 2))
        return _bar("The bar chart shows tickets sold at four venues. How many "
                    "tickets were sold at %s and %s altogether?" % (cats[i], cats[j]),
                    cats, vals, vals[i] + vals[j],
                    ["%s + %s = %s." % (_c(vals[i]), _c(vals[j]),
                                        _c(vals[i] + vals[j]))])

    def t_io():
        amt = _op(max(d, 1))
        up = random.random() < 0.5
        ins = sorted(random.sample(range(1000000, 8000000), 4))
        if not up:
            # the rule is applied to every row, so it must not take the
            # SMALLEST input below zero
            amt = min(amt, ins[0] - 1000)
        rows = [[i, i + amt if up else i - amt] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is %s %s." % ("add" if up else "subtract", _c(amt)),
                    "%s %s %s = %s." % (_c(rows[miss][0]), "+" if up else "−",
                                        _c(amt), _c(rows[miss][1]))],
                   rule="%s %s" % ("+" if up else "−", _c(amt)))

    return _pick_t([t_add, t_sub, t_three, t_missing_addend, t_missing_start,
                    t_population, t_money, t_inverse_check, t_multi],
                   [t_table, t_table_diff, t_bar, t_io])


@skill("Y6.1.b", "Multiplication and division facts to 12 x 12", S1)
def _(d=1):
    d = _d(d)
    LO, HI = {0: (2, 8), 1: (2, 12), 2: (6, 12)}[d]

    def _f():
        return random.randint(LO, HI), random.randint(LO, HI)

    def t_mult():
        a, b = _f()
        return _tb("What is %d × %d?" % (a, b), a * b, "int", {},
                   ["%d × %d = %d." % (a, b, a * b)])

    def t_div():
        a, b = _f()
        return _tb("What is %d ÷ %d?" % (a * b, a), b, "int", {},
                   ["%d × %d = %d, so %d ÷ %d = %d." % (a, b, a * b, a * b, a, b)])

    def t_missing_factor():
        a, b = _f()
        return _tb("Find the missing factor:   %d × ___ = %d" % (a, a * b), b, "int", {},
                   ["%d ÷ %d = %d." % (a * b, a, b)])

    def t_missing_dividend():
        a, b = _f()
        return _tb("Find the missing number:   ___ ÷ %d = %d" % (a, b), a * b, "int", {},
                   ["%d × %d = %d." % (b, a, a * b)])

    def t_missing_divisor():
        a, b = _f()
        return _tb("Find the missing number:   %d ÷ ___ = %d" % (a * b, b), a, "int", {},
                   ["%d ÷ %d = %d." % (a * b, b, a)])

    def t_word():
        a, b = _f()
        who = pick(NAMES)
        thing = pick(_OBJ)
        holder = pick(["boxes", "bags", "trays", "packets"])
        if random.random() < 0.5:
            return _tb("%s has %d %s of %s with %d in each. How many %s does %s have "
                       "altogether?" % (who, a, holder, thing, b, thing, who),
                       a * b, "int", {"unit": thing},
                       ["%d × %d = %d." % (a, b, a * b)])
        return _tb("%s shares %d %s equally between %d children. How many %s does "
                   "each child get?" % (who, a * b, thing, a, thing), b, "int",
                   {"unit": thing}, ["%d ÷ %d = %d." % (a * b, a, b)])

    def t_fact_family():
        a, b = _f()
        while a == b:
            a, b = _f()
        return _tb("%d × %d = %d. Use this fact to work out %d ÷ %d."
                   % (a, b, a * b, a * b, b), a, "int", {},
                   ["Multiplication and division are inverses.",
                    "%d ÷ %d = %d." % (a * b, b, a)])

    def t_square():
        a = random.randint(max(LO, 2), HI)
        return _tb("What is %d squared?" % a, a * a, "int", {},
                   ["%d × %d = %d." % (a, a, a * a)])

    def t_three_factors():
        a, b = _f()
        cc = random.randint(2, 5)
        return _tb("Work out:   %d × %d × %d" % (a, b, cc), a * b * cc, "int", {},
                   ["%d × %d = %d." % (a, b, a * b),
                    "%d × %d = %d." % (a * b, cc, a * b * cc)])

    def t_factor_pairs():
        n = pick([24, 36, 48, 60, 72, 96, 100, 120, 144])
        pairs = [x for x in range(1, 13) if n % x == 0]
        return _setq("Type all the numbers from 1 to 12 that divide exactly into %d."
                     % n, pairs,
                     ["%d divides exactly by %s."
                      % (n, ", ".join(str(x) for x in pairs))], "e.g. 2, 3, 4")

    def t_array():
        a, b = _f()
        return _arr("Build an array that shows %d × %d, then type the product."
                    % (a, b), a, b, ["%d rows of %d." % (a, b),
                                     "%d × %d = %d." % (a, b, a * b)])

    def t_eg():
        a = random.randint(2, 8)
        b = random.randint(2, 10)
        return _eg("The picture shows %d equal groups. How many counters are there "
                   "altogether?" % a, a, b, a * b,
                   ["%d groups of %d." % (a, b), "%d × %d = %d." % (a, b, a * b)])

    def t_eg_div():
        a = random.randint(2, 8)
        b = random.randint(2, 10)
        return _eg("%d counters have been shared into %d equal groups. How many "
                   "counters are in each group?" % (a * b, a), a, b, b,
                   ["%d ÷ %d = %d." % (a * b, a, b)])

    def t_io():
        b = random.randint(LO, HI)
        ins = sorted(random.sample(range(2, 13), 4))
        rows = [[i, i * b] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is × %d." % b,
                    "%d × %d = %d." % (rows[miss][0], b, rows[miss][1])],
                   rule="× %d" % b)

    def t_area():
        a = random.randint(2, 10)
        b = random.randint(2, 12)
        return _area("The grid is %d squares tall and %d squares wide. How many "
                     "small squares are there altogether?" % (a, b), a, b,
                     ["%d × %d = %d." % (a, b, a * b)])

    def t_table():
        b = random.randint(LO, HI)
        ins = sorted(random.sample(range(2, 13), 4))
        rows = [[str(i), str(i * b)] for i in ins]
        r = random.randint(0, 3)
        return _dt("This table shows the %d times table. What number belongs in the "
                   "empty cell?" % b, ["Number", "Number × %d" % b], rows,
                   ins[r] * b, ["%d × %d = %d." % (ins[r], b, ins[r] * b)],
                   missing=[r, 1])

    def t_choose_multiples():
        top = pick([10, 12])
        n = random.randint(3, top)
        ks = random.sample(range(2, 13), 3)
        mults = [n * k for k in ks]
        spare = [x for x in range(2, n * 13) if x % n != 0 and x not in mults]
        others = random.sample(spare, 4)
        nums = mults + others
        random.shuffle(nums)
        return _setq("Choose the multiples of %d. Type every number in this list "
                     "that is a multiple of %d:   %s"
                     % (n, n, ", ".join(str(x) for x in nums)), mults,
                     ["A multiple of %d is in the %d times table." % (n, n),
                      "The multiples of %d here are %s."
                      % (n, ", ".join(str(x) for x in sorted(mults)))],
                     "e.g. 12, 24, 36")

    def t_choose_product():
        a, b = random.sample(range(3, 13), 2)
        p = a * b
        nums = _pair_list(a, b, range(2, 13), lambda x, y: x * y == p)
        return _setq("Choose the TWO numbers from this list with a product of %d, "
                     "then type both of them:   %s"
                     % (p, ", ".join(str(x) for x in nums)), [a, b],
                     ["%d × %d = %d." % (min(a, b), max(a, b), p),
                      "No other pair in the list has that product."],
                     "type two numbers")

    def t_choose_quotient():
        q = random.randint(2, 9)
        b = random.randint(2, 12)
        a = q * b
        nums = _pair_list(a, b, range(2, 121), lambda x, y: y != 0 and x == y * q)
        return _setq("Choose the TWO numbers from this list that give a quotient of "
                     "%d when the larger is divided by the smaller, then type both "
                     "of them:   %s" % (q, ", ".join(str(x) for x in nums)), [a, b],
                     ["%d ÷ %d = %d." % (a, b, q),
                      "No other pair in the list gives that quotient."],
                     "type two numbers")

    return _pick_t([t_mult, t_div, t_missing_factor, t_missing_dividend,
                    t_missing_divisor, t_word, t_fact_family, t_square,
                    t_three_factors, t_factor_pairs, t_choose_multiples,
                    t_choose_product, t_choose_quotient],
                   [t_array, t_eg, t_eg_div, t_io, t_area, t_table])


@skill("Y6.1.c", "Long multiplication: 4-digit by 2-digit", S1)
def _(d=1):
    d = _d(d)

    def _pair():
        a = random.randint(1000, 9999)
        b = {0: random.randint(11, 29), 1: random.randint(12, 59),
             2: random.randint(21, 99)}[d]
        return a, b

    def t_bare():
        a, b = _pair()
        return _tb("Work out:   %s × %d" % (_c(a), b), a * b, "int", {},
                   ["%s × %d = %s." % (_c(a), b % 10, _c(a * (b % 10))),
                    "%s × %d = %s." % (_c(a), (b // 10) * 10, _c(a * (b // 10) * 10)),
                    "%s + %s = %s." % (_c(a * (b % 10)), _c(a * (b // 10) * 10),
                                       _c(a * b))])

    def t_cost():
        a, b = _pair()
        return _tb("A school orders %d laptops costing £%s each. What is the total "
                   "cost?" % (b, _c(a)), a * b, "int", {"unit": "£"},
                   ["%d × £%s = £%s." % (b, _c(a), _c(a * b))])

    def t_seats():
        rows = random.randint(21, 96)
        per = random.randint(1000, 9999)
        return _tb("A stadium has %d blocks of seats with %s seats in each block. "
                   "How many seats are there altogether?" % (rows, _c(per)),
                   rows * per, "int", {"unit": "seats"},
                   ["%d × %s = %s." % (rows, _c(per), _c(rows * per))])

    def t_partial():
        a, b = _pair()
        tens = (b // 10) * 10
        return _tb("This is one step of a long multiplication. Work out:   %s × %d"
                   % (_c(a), tens), a * tens, "int", {},
                   ["%s × %d = %s." % (_c(a), b // 10, _c(a * (b // 10))),
                    "Multiply by 10: %s." % _c(a * tens)])

    def t_partial_sum():
        a, b = _pair()
        p1 = a * (b % 10)
        p2 = a * (b // 10) * 10
        return _tb("In a long multiplication of %s × %d the two partial products are "
                   "%s and %s. What is the final answer?" % (_c(a), b, _c(p1), _c(p2)),
                   a * b, "int", {},
                   ["%s + %s = %s." % (_c(p1), _c(p2), _c(a * b))])

    def t_missing_factor():
        a, b = _pair()
        return _tb("Find the missing number:   ___ × %d = %s" % (b, _c(a * b)),
                   a, "int", {},
                   ["Use the inverse: %s ÷ %d = %s." % (_c(a * b), b, _c(a))])

    def t_inverse():
        a, b = _pair()
        return _tb("%s knows that %s × %d = %s. What is %s ÷ %d?"
                   % (pick(NAMES), _c(a), b, _c(a * b), _c(a * b), b), a, "int", {},
                   ["Division undoes multiplication.",
                    "%s ÷ %d = %s." % (_c(a * b), b, _c(a))])

    def t_compare():
        a, b = _pair()
        cc, e = _pair()
        while a * b == cc * e:
            cc, e = _pair()
        big = max(a * b, cc * e)
        return _tb("Which is larger, %s × %d or %s × %d? Type the larger product."
                   % (_c(a), b, _c(cc), e), big, "int", {},
                   ["%s × %d = %s." % (_c(a), b, _c(a * b)),
                    "%s × %d = %s." % (_c(cc), e, _c(cc * e)),
                    "The larger product is %s." % _c(big)])

    def t_two_step():
        a, b = _pair()
        extra = random.randint(100, 9999)
        return _tb("A shop buys %d boxes of tiles at £%s each and then pays £%s for "
                   "delivery. What is the total cost?" % (b, _c(a), _c(extra)),
                   a * b + extra, "int", {"unit": "£"},
                   ["%d × £%s = £%s." % (b, _c(a), _c(a * b)),
                    "£%s + £%s = £%s." % (_c(a * b), _c(extra), _c(a * b + extra))])

    def t_table():
        b = {0: random.randint(11, 29), 1: random.randint(12, 59),
             2: random.randint(21, 99)}[d]
        ins = sorted(random.sample(range(1000, 9999), 4))
        rows = [[_c(i), _c(i * b)] for i in ins]
        r = random.randint(0, 3)
        return _dt("Each row multiplies the first number by %d. What belongs in the "
                   "empty cell?" % b, ["Number", "Number × %d" % b], rows,
                   ins[r] * b, ["%s × %d = %s." % (_c(ins[r]), b, _c(ins[r] * b))],
                   missing=[r, 1])

    def t_table_cost():
        items = random.sample(["Laptops", "Tablets", "Projectors", "Printers",
                               "Cameras"], 3)
        qty = [random.randint(21, 89) for _ in range(3)]
        price = [random.randint(1000, 9999) for _ in range(3)]
        rows = [[it, str(q), "£" + _c(p), "£" + _c(q * p)]
                for it, q, p in zip(items, qty, price)]
        r = random.randint(0, 2)
        return _dt("Complete the order form. What total cost in pounds belongs in "
                   "the empty cell?", ["Item", "Quantity", "Price each", "Total"],
                   rows, qty[r] * price[r],
                   ["%d × £%s = £%s." % (qty[r], _c(price[r]), _c(qty[r] * price[r]))],
                   missing=[r, 3])

    def t_io():
        b = random.randint(12, 49)
        ins = sorted(random.sample(range(1000, 9999), 4))
        rows = [[i, i * b] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is × %d." % b,
                    "%s × %d = %s." % (_c(rows[miss][0]), b, _c(rows[miss][1]))],
                   rule="× %d" % b)

    return _pick_t([t_bare, t_cost, t_seats, t_partial, t_partial_sum,
                    t_missing_factor, t_inverse, t_compare, t_two_step],
                   [t_table, t_table_cost, t_io])


@skill("Y6.1.d", "Multiply by 1-digit numbers and powers of ten", S1)
def _(d=1):
    d = _d(d)

    def t_single():
        a = random.randint(1000, 9999) if d else random.randint(100, 999)
        b = random.randint(3, 9)
        return _tb("Work out:   %s × %d" % (_c(a), b), a * b, "int", {},
                   ["%s × %d = %s." % (_c(a), b, _c(a * b))])

    def t_power():
        a = random.randint(12, 9999)
        p = pick([10, 100] if d == 0 else [10, 100, 1000])
        return _tb("Work out:   %s × %s" % (_c(a), _c(p)), a * p, "int", {},
                   ["Every digit moves %d place%s to the left."
                    % (len(str(p)) - 1, "" if p == 10 else "s"),
                    "%s × %s = %s." % (_c(a), _c(p), _c(a * p))])

    def t_missing_power():
        a = random.randint(12, 9999)
        p = pick([10, 100, 1000])
        return _tb("Find the missing number:   %s × ___ = %s" % (_c(a), _c(a * p)),
                   p, "int", {},
                   ["%s ÷ %s = %s." % (_c(a * p), _c(a), _c(p))])

    def t_divide_power():
        p = pick([10, 100, 1000])
        a = random.randint(12, 9999) * p
        return _tb("Work out:   %s ÷ %s" % (_c(a), _c(p)), a // p, "int", {},
                   ["Every digit moves %d place%s to the right."
                    % (len(str(p)) - 1, "" if p == 10 else "s"),
                    "%s ÷ %s = %s." % (_c(a), _c(p), _c(a // p))])

    def t_decimal():
        whole = random.randint(2, 99)
        dec = random.randint(1, 9)
        val = whole + dec / 10.0
        p = pick([10, 100])
        ans = int(round(val * p))
        return _tb("Work out:   %s × %d" % ("%.1f" % val, p), ans, "num", {},
                   ["Every digit moves %d place%s to the left."
                    % (len(str(p)) - 1, "" if p == 10 else "s"),
                    "%s × %d = %s." % ("%.1f" % val, p, _c(ans))])

    def t_combined():
        a = random.randint(11, 99)
        b = random.randint(3, 9)
        p = pick([10, 100])
        return _tb("Work out:   %d × %d × %d" % (a, b, p), a * b * p, "int", {},
                   ["%d × %d = %s." % (a, b, _c(a * b)),
                    "%s × %d = %s." % (_c(a * b), p, _c(a * b * p))])

    def t_word():
        who = pick(NAMES)
        a = random.randint(1000, 9999)
        b = random.randint(3, 9)
        return _tb("%s cycles %s metres each day. How far does %s cycle in %d days?"
                   % (who, _c(a), who, b), a * b, "int", {"unit": "m"},
                   ["%d × %s = %s." % (b, _c(a), _c(a * b))])

    def t_units():
        km = random.randint(12, 999)
        which = pick([("km", "m", 1000), ("kg", "g", 1000), ("l", "ml", 1000),
                      ("m", "cm", 100), ("cm", "mm", 10)])
        big, small, f = which
        return _tb("Convert %s %s into %s." % (_c(km), big, small), km * f, "int",
                   {"unit": small},
                   ["1 %s = %s %s." % (big, _c(f), small),
                    "%s × %s = %s." % (_c(km), _c(f), _c(km * f))])

    def t_inverse():
        a = random.randint(1000, 9999)
        b = random.randint(3, 9)
        return _tb("Find the missing number:   ___ × %d = %s" % (b, _c(a * b)),
                   a, "int", {},
                   ["%s ÷ %d = %s." % (_c(a * b), b, _c(a))])

    def t_io():
        rule = pick([10, 100, 1000, random.randint(3, 9)])
        ins = sorted(random.sample(range(120, 9999), 4))
        rows = [[i, i * rule] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is × %s." % _c(rule),
                    "%s × %s = %s." % (_c(rows[miss][0]), _c(rule),
                                       _c(rows[miss][1]))],
                   rule="× %s" % _c(rule))

    def t_table_convert():
        big, small, f = pick([("km", "m", 1000), ("kg", "g", 1000), ("l", "ml", 1000)])
        ins = sorted(random.sample(range(2, 99), 4))
        rows = [["%d %s" % (i, big), "%s %s" % (_c(i * f), small)] for i in ins]
        r = random.randint(0, 3)
        return _dt("Complete the conversion table. What number belongs in the empty "
                   "cell?", ["%s" % big.upper(), "%s" % small.upper()], rows,
                   ins[r] * f,
                   ["1 %s = %s %s." % (big, _c(f), small),
                    "%d × %s = %s." % (ins[r], _c(f), _c(ins[r] * f))],
                   missing=[r, 1])

    def t_table_multiples():
        a = random.randint(1000, 9999)
        ps = [1, 10, 100, 1000]
        row = [_c(a * p) for p in ps]
        col = random.randint(1, 3)
        return _dt("The table multiplies %s by powers of ten. What belongs in the "
                   "empty cell?" % _c(a), ["× 1", "× 10", "× 100", "× 1,000"], [row],
                   a * ps[col],
                   ["%s × %s = %s." % (_c(a), _c(ps[col]), _c(a * ps[col]))],
                   missing=[0, col])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        vals = [random.randint(120, 900) for _ in range(4)]
        i = random.randint(0, 3)
        return _bar("The bar chart shows how many boxes each depot holds. Each box "
                    "holds 100 items. How many items are at %s?" % cats[i],
                    cats, vals, vals[i] * 100,
                    ["%s has %d boxes." % (cats[i], vals[i]),
                     "%d × 100 = %s." % (vals[i], _c(vals[i] * 100))])

    def t_mult_pattern():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        steps = 3 if d == 0 else 4
        lines = []
        for i in range(steps - 1):
            x = a * (10 ** i)
            lines.append("%s × %d = %s" % (_c(x), b, _c(x * b)))
        last = a * (10 ** (steps - 1))
        lines.append("%s × %d = ___" % (_c(last), b))
        return _tb("This multiplication pattern moves over increasing place values. "
                   "What number completes the pattern?   %s" % ",   ".join(lines),
                   last * b, "int", {},
                   ["%d × %d = %d." % (a, b, a * b),
                    "Each line multiplies a number ten times as large, so the "
                    "answer is ten times as large.",
                    "%s × %d = %s." % (_c(last), b, _c(last * b))])

    def t_mult_zeros():
        if d == 0:
            a = random.randint(2, 9) * 100
            b = random.randint(2, 9) * 10
        elif d == 1:
            a = random.randint(11, 99) * 100
            b = random.randint(2, 9) * 100
        else:
            a = random.randint(11, 99) * 100
            b = random.randint(11, 99) * 10
        za = len(str(a)) - len(str(a).rstrip("0"))
        zb = len(str(b)) - len(str(b).rstrip("0"))
        na, nb = a // (10 ** za), b // (10 ** zb)
        return _tb("Both of these numbers end in zeros. Work out:   %s × %s"
                   % (_c(a), _c(b)), a * b, "int", {},
                   ["Multiply the other digits first: %d × %d = %s."
                    % (na, nb, _c(na * nb)),
                    "There are %d zeros in total, so write %d zeros on the end."
                    % (za + zb, za + zb),
                    "%s × %s = %s." % (_c(a), _c(b), _c(a * b))])

    def t_mult_zeros_word():
        per = random.randint(2, 9) * 100 if d else random.randint(2, 9) * 10
        n = random.randint(2, 9) * (100 if d == 2 else 10)
        thing = pick(["tins", "bricks", "bottles", "tiles"])
        holder = pick(["crates", "pallets", "boxes"])
        return _tb("A depot receives %s %s, and each one holds %s %s. Both numbers "
                   "end in zeros. How many %s does the depot receive altogether?"
                   % (_c(n), holder, _c(per), thing, thing), n * per, "int",
                   {"unit": thing},
                   ["%s × %s = %s." % (_c(n), _c(per), _c(n * per))])

    return _pick_t([t_single, t_power, t_missing_power, t_divide_power, t_decimal,
                    t_combined, t_word, t_units, t_inverse, t_mult_pattern,
                    t_mult_zeros, t_mult_zeros_word],
                   [t_io, t_table_convert, t_table_multiples, t_bar])


@skill("Y6.1.e", "Short division with remainders", S1)
def _(d=1):
    d = _d(d)

    def _pair(exact=False):
        b = {0: random.randint(3, 6), 1: random.randint(3, 9),
             2: random.randint(6, 9)}[d]
        q = random.randint(1000 // b + 1, (9999 - b) // b)
        if exact:
            return q * b, b
        return q * b + random.randint(1, b - 1), b

    def t_quotient():
        a, b = _pair()
        return _tb("Work out %s ÷ %d. Type the whole-number part of the answer "
                   "(ignore the remainder)." % (_c(a), b), a // b, "int", {},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "The whole-number part is %s." % _c(a // b)])

    def t_remainder():
        a, b = _pair()
        return _tb("Work out %s ÷ %d. What is the REMAINDER?" % (_c(a), b),
                   a % b, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(b * (a // b))),
                    "%s − %s = %d." % (_c(a), _c(b * (a // b)), a % b)])

    def t_exact():
        a, b = _pair(exact=True)
        return _tb("Work out:   %s ÷ %d" % (_c(a), b), a // b, "int", {},
                   ["%s ÷ %d = %s." % (_c(a), b, _c(a // b))])

    def t_full_boxes():
        a, b = _pair()
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many boxes can be filled "
                   "completely?" % (_c(a), thing, b), a // b, "int", {"unit": "boxes"},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "%s boxes can be filled." % _c(a // b)])

    def t_left_over():
        a, b = _pair()
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many %s are left over?"
                   % (_c(a), thing, b, thing), a % b, "int", {"unit": thing},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "%d are left over." % (a % b)])

    def t_check():
        a, b = _pair()
        return _tb("%s divides %s by %d and gets %s remainder %d. Multiply and add "
                   "to check: what does %d × %s + %d come to?"
                   % (pick(NAMES), _c(a), b, _c(a // b), a % b, b, _c(a // b), a % b),
                   a, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(b * (a // b))),
                    "%s + %d = %s, the starting number."
                    % (_c(b * (a // b)), a % b, _c(a))])

    def t_missing_dividend():
        a, b = _pair()
        return _tb("A number divided by %d gives %s remainder %d. What is the number?"
                   % (b, _c(a // b), a % b), a, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(b * (a // b))),
                    "%s + %d = %s." % (_c(b * (a // b)), a % b, _c(a))])

    def t_divides_exactly():
        exact = random.random() < 0.5
        a, b = _pair(exact=exact)
        return _yn("Does %d divide exactly into %s, with no remainder? (type 'yes' "
                   "or 'no')" % (b, _c(a)), "yes" if a % b == 0 else "no",
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "So the answer is %s." % ("yes" if a % b == 0 else "no")])

    def t_money():
        b = random.randint(3, 9)
        total = random.randint(1000, 9999)
        return _tb("£%s is shared equally between %d clubs. How many whole pounds "
                   "does each club get?" % (_c(total), b), total // b, "int",
                   {"unit": "£"},
                   ["%s ÷ %d = %s remainder %d."
                    % (_c(total), b, _c(total // b), total % b),
                    "Each club gets £%s." % _c(total // b)])

    def t_strip():
        b = random.randint(3, 9)
        q = random.randint(120, 900)
        return _strip("The bar shows %s split into %d equal parts. How big is each "
                      "part?" % (_c(q * b), b), b, "?", _c(q * b), "part", q,
                      ["%s ÷ %d = %s." % (_c(q * b), b, _c(q))])

    def t_table():
        b = random.randint(3, 9)
        ins = sorted(random.sample(range(1000, 9999), 4))
        rows = [[_c(i), _c(i // b), str(i % b)] for i in ins]
        r = random.randint(0, 3)
        col = pick([1, 2])
        ans = ins[r] // b if col == 1 else ins[r] % b
        return _dt("This table divides each number by %d. What belongs in the empty "
                   "cell?" % b, ["Number", "Quotient", "Remainder"], rows, ans,
                   ["%s ÷ %d = %s remainder %d."
                    % (_c(ins[r]), b, _c(ins[r] // b), ins[r] % b)],
                   missing=[r, col])

    def t_io():
        b = random.randint(3, 9)
        ins = sorted(random.sample(range(200, 9999 // b), 4))
        rows = [[i * b, i] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is ÷ %d." % b,
                    "%s ÷ %d = %s." % (_c(rows[miss][0]), b, _c(rows[miss][1]))],
                   rule="÷ %d" % b)

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        b = random.randint(3, 9)
        vals = [random.randint(100, 900) * b for _ in range(4)]
        i = random.randint(0, 3)
        return _bar("The bar chart shows how many books each library received. The "
                    "books at %s are shared equally between %d schools. How many "
                    "books does each school get?" % (cats[i], b), cats, vals,
                    vals[i] // b,
                    ["%s received %s books." % (cats[i], _c(vals[i])),
                     "%s ÷ %d = %s." % (_c(vals[i]), b, _c(vals[i] // b))])

    def t_div_pattern():
        b = random.randint(2, 9)
        q = random.randint(2, 9)
        steps = 3 if d == 0 else 4
        lines = []
        for i in range(steps - 1):
            x = q * b * (10 ** i)
            lines.append("%s ÷ %d = %s" % (_c(x), b, _c(x // b)))
        last = q * b * (10 ** (steps - 1))
        lines.append("%s ÷ %d = ___" % (_c(last), b))
        return _tb("This division pattern moves over increasing place values. What "
                   "number completes the pattern?   %s" % ",   ".join(lines),
                   last // b, "int", {},
                   ["%d ÷ %d = %d." % (q * b, b, q),
                    "Each line divides a number ten times as large, so the answer "
                    "is ten times as large.",
                    "%s ÷ %d = %s." % (_c(last), b, _c(last // b))])

    def t_div_zeros():
        if d == 0:
            b = random.randint(2, 9) * 10
            q = random.randint(2, 9)
        elif d == 1:
            b = random.randint(2, 9) * 100
            q = random.randint(2, 9) * 10
        else:
            b = random.randint(11, 49) * 10
            q = random.randint(2, 9) * 100
        a = b * q
        zb = len(str(b)) - len(str(b).rstrip("0"))
        return _tb("Both of these numbers end in zeros. Work out:   %s ÷ %s"
                   % (_c(a), _c(b)), q, "int", {},
                   ["Cross out %d zero%s from the end of each number: %s ÷ %s."
                    % (zb, "" if zb == 1 else "s", _c(a // (10 ** zb)),
                       _c(b // (10 ** zb))),
                    "%s ÷ %s = %s." % (_c(a), _c(b), _c(q))])

    def t_div_zeros_word():
        b = random.randint(2, 9) * (100 if d else 10)
        q = random.randint(2, 9) * (10 if d else 1)
        a = b * q
        thing = pick(_OBJ)
        return _tb("A warehouse divides %s %s equally into packs of %s. Both "
                   "numbers end in zeros. How many packs are made?"
                   % (_c(a), thing, _c(b)), q, "int", {"unit": "packs"},
                   ["%s ÷ %s = %s." % (_c(a), _c(b), _c(q))])

    return _pick_t([t_quotient, t_remainder, t_exact, t_full_boxes, t_left_over,
                    t_check, t_missing_dividend, t_divides_exactly, t_money,
                    t_div_pattern, t_div_zeros, t_div_zeros_word],
                   [t_strip, t_table, t_io, t_bar])


@skill("Y6.1.f", "Long division: 4-digit by 2-digit", S1)
def _(d=1):
    d = _d(d)

    def _pair(exact=False):
        b = {0: random.randint(11, 20), 1: random.randint(12, 35),
             2: random.randint(15, 49)}[d]
        q = random.randint(1000 // b + 1, (9999 - b) // b)
        if exact:
            return q * b, b
        return q * b + random.randint(1, b - 1), b

    def t_exact():
        a, b = _pair(exact=True)
        return _tb("Work out:   %s ÷ %d" % (_c(a), b), a // b, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(a)),
                    "So %s ÷ %d = %s." % (_c(a), b, _c(a // b))])

    def t_quotient():
        a, b = _pair()
        return _tb("Work out %s ÷ %d. Type the whole-number part of the answer."
                   % (_c(a), b), a // b, "int", {},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "The whole-number part is %s." % _c(a // b)])

    def t_remainder():
        a, b = _pair()
        if a % b == 0:
            a += 1
        return _tb("Work out %s ÷ %d. What is the REMAINDER?" % (_c(a), b),
                   a % b, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(b * (a // b))),
                    "%s − %s = %d." % (_c(a), _c(b * (a // b)), a % b)])

    def t_fraction():
        a, b = _pair()
        if a % b == 0:
            a += 1
        return _tb("Work out %s ÷ %d. Write the remainder as a fraction of %d — type "
                   "just that fraction, for example 3/8." % (_c(a), b, b),
                   "%d/%d" % (a % b, b), "frac",
                   {"text": True, "placeholder": "e.g. 3/8"},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "As a fraction of %d the remainder is %d/%d." % (b, a % b, b)])

    def t_rounded():
        a, b = _pair()
        if a % b == 0:
            a += 1
        q, r = a // b, a % b
        ans = q + 1 if 2 * r >= b else q
        return _tb("Work out %s ÷ %d and round your answer to the nearest whole "
                   "number." % (_c(a), b), ans, "int", {},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(q), r),
                    "The remainder %d is %s half of %d, so the answer rounds %s to %s."
                    % (r, "at least" if 2 * r >= b else "less than", b,
                       "up" if 2 * r >= b else "down", _c(ans))])

    def t_coaches():
        b = random.randint(32, 56)
        total = random.randint(400, 2000)
        need = -(-total // b)
        return _tb("%s pupils are going on a trip. Each coach holds %d pupils. How "
                   "many coaches are needed so that every pupil has a seat?"
                   % (_c(total), b), need, "int", {"unit": "coaches"},
                   ["%s ÷ %d = %d remainder %d." % (_c(total), b, total // b, total % b),
                    "The pupils left over still need a coach, so %d coaches are "
                    "needed." % need])

    def t_full():
        a, b = _pair()
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many FULL boxes are "
                   "there?" % (_c(a), thing, b), a // b, "int", {"unit": "boxes"},
                   ["%s ÷ %d = %s remainder %d." % (_c(a), b, _c(a // b), a % b),
                    "There are %s full boxes." % _c(a // b)])

    def t_missing():
        a, b = _pair(exact=True)
        return _tb("Find the missing number:   ___ ÷ %d = %s" % (b, _c(a // b)),
                   a, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(a))])

    def t_price():
        b = random.randint(12, 48)
        each = random.randint(15, 300)
        total = b * each
        return _tb("%d identical chairs cost £%s altogether. How much does one chair "
                   "cost?" % (b, _c(total)), each, "int", {"unit": "£"},
                   ["£%s ÷ %d = £%s." % (_c(total), b, _c(each))])

    def t_check():
        a, b = _pair()
        return _tb("%s divides %s by %d and gets %s remainder %d. Check it: what is "
                   "%d × %s + %d?" % (pick(NAMES), _c(a), b, _c(a // b), a % b,
                                      b, _c(a // b), a % b), a, "int", {},
                   ["%d × %s = %s." % (b, _c(a // b), _c(b * (a // b))),
                    "%s + %d = %s." % (_c(b * (a // b)), a % b, _c(a))])

    def t_table():
        b = random.randint(12, 40)
        ins = sorted(random.sample(range(1000, 9999), 4))
        rows = [[_c(i), _c(i // b), str(i % b)] for i in ins]
        r = random.randint(0, 3)
        col = pick([1, 2])
        ans = ins[r] // b if col == 1 else ins[r] % b
        return _dt("This table divides each number by %d. What belongs in the empty "
                   "cell?" % b, ["Number", "Whole-number answer", "Remainder"], rows,
                   ans, ["%s ÷ %d = %s remainder %d."
                         % (_c(ins[r]), b, _c(ins[r] // b), ins[r] % b)],
                   missing=[r, col])

    def t_io():
        b = random.randint(12, 40)
        ins = sorted(random.sample(range(40, 400), 4))
        rows = [[i * b, i] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. What number goes in the "
                   "empty cell?", rows, miss, rows[miss][1],
                   ["The rule is ÷ %d." % b,
                    "%s ÷ %d = %s." % (_c(rows[miss][0]), b, _c(rows[miss][1]))],
                   rule="÷ %d" % b)

    def t_strip():
        b = random.randint(3, 12)
        q = random.randint(120, 800)
        return _strip("The bar shows %s shared into %d equal parts. How big is one "
                      "part?" % (_c(q * b), b), b, "?", _c(q * b), "part", q,
                      ["%s ÷ %d = %s." % (_c(q * b), b, _c(q))])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        b = random.randint(12, 40)
        vals = [random.randint(40, 240) * b for _ in range(4)]
        i = random.randint(0, 3)
        return _bar("The bar chart shows how many chairs were delivered to four "
                    "halls. The chairs at %s are set out in rows of %d. How many "
                    "full rows are there?" % (cats[i], b), cats, vals, vals[i] // b,
                    ["%s received %s chairs." % (cats[i], _c(vals[i])),
                     "%s ÷ %d = %s." % (_c(vals[i]), b, _c(vals[i] // b))])

    return _pick_t([t_exact, t_quotient, t_remainder, t_fraction, t_rounded,
                    t_coaches, t_full, t_missing, t_price, t_check],
                   [t_table, t_io, t_strip, t_bar])


@skill("Y6.1.g", "Estimate and check using rounding and inverses", S1)
def _(d=1):
    d = _d(d)

    def t_est_add():
        unit = pick([100, 1000] if d else [10, 100])
        a = random.randint(unit * 3, unit * 90)
        b = random.randint(unit * 3, unit * 90)
        return _tb("Estimate %s + %s by first rounding each number to the nearest "
                   "%s." % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) + _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s + %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) + _r(b, unit)))])

    def t_est_sub():
        unit = pick([100, 1000] if d else [10, 100])
        a = random.randint(unit * 30, unit * 90)
        b = random.randint(unit * 3, unit * 29)
        return _tb("Estimate %s − %s by first rounding each number to the nearest "
                   "%s." % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) - _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s − %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) - _r(b, unit)))])

    def t_est_mult():
        a = random.randint(1200, 9800)
        b = random.randint(21, 89)
        return _tb("Estimate %s × %d by rounding %s to the nearest 1,000 and %d to "
                   "the nearest 10." % (_c(a), b, _c(a), b),
                   _r(a, 1000) * _r(b, 10), "int", {},
                   ["%s rounds to %s and %d rounds to %d."
                    % (_c(a), _c(_r(a, 1000)), b, _r(b, 10)),
                    "%s × %d = %s." % (_c(_r(a, 1000)), _r(b, 10),
                                       _c(_r(a, 1000) * _r(b, 10)))])

    def t_est_div():
        b = random.randint(2, 9)
        k = random.randint(1, 9) * b                 # thousands, divisible by b
        rounded = k * 1000
        a = rounded + random.randint(-499, 499)
        return _tb("Estimate %s ÷ %d by first rounding %s to the nearest 1,000."
                   % (_c(a), b, _c(a)), rounded // b, "int", {},
                   ["%s rounds to %s." % (_c(a), _c(rounded)),
                    "%s ÷ %d = %s." % (_c(rounded), b, _c(rounded // b))])

    def t_reasonable():
        a = random.randint(1200, 9800)
        b = random.randint(21, 89)
        true = a * b
        wrong = random.random() < 0.5
        claim = true // 10 if wrong else true
        return _yn("%s works out %s × %d and gets %s. Use estimation to decide: is "
                   "that answer reasonable? (type 'yes' or 'no')"
                   % (pick(NAMES), _c(a), b, _c(claim)), "no" if wrong else "yes",
                   ["A good estimate is %s × %d = %s."
                    % (_c(_r(a, 1000)), _r(b, 10), _c(_r(a, 1000) * _r(b, 10))),
                    "The answer given is %s, so it is %s."
                    % (_c(claim), "not reasonable" if wrong else "reasonable")])

    def t_inverse_add():
        a, b = _op(max(d, 1)), _op(max(d, 1))
        return _tb("%s works out %s + %s = %s. Which subtraction checks this? Type "
                   "the answer to %s − %s." % (pick(NAMES), _c(a), _c(b), _c(a + b),
                                               _c(a + b), _c(b)), a, "int", {},
                   ["%s − %s = %s, which is the number we started with."
                    % (_c(a + b), _c(b), _c(a))])

    def t_inverse_mult():
        a = random.randint(1000, 9999)
        b = random.randint(12, 49)
        return _tb("A calculation gives %s × %d = %s. Use the inverse to check it: "
                   "what is %s ÷ %d?" % (_c(a), b, _c(a * b), _c(a * b), b),
                   a, "int", {},
                   ["%s ÷ %d = %s, which is the number we started with."
                    % (_c(a * b), b, _c(a))])

    def t_find_error():
        a, b = _op(max(d, 1)), _op(max(d, 1))
        a, b = max(a, b), min(a, b)
        return _tb("%s works out %s − %s and gets %s, which an estimate shows is "
                   "wrong. What is the correct answer?"
                   % (pick(NAMES), _c(a), _c(b), _c((a - b) + 1000)), a - b, "int", {},
                   ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_est_total():
        prices = [random.randint(101, 999) for _ in range(4)]
        est = sum(_r(p, 100) for p in prices)
        return _tb("Estimate the total of these prices by rounding each one to the "
                   "nearest £100:   %s" % ", ".join("£" + _c(p) for p in prices),
                   est, "int", {"unit": "£"},
                   ["Rounded: %s." % ", ".join("£" + _c(_r(p, 100)) for p in prices),
                    "The estimated total is £%s." % _c(est)])

    def t_table():
        unit = pick([100, 1000])
        ns = sorted(random.sample(range(unit * 3, unit * 90), 4))
        rows = [[_c(x), _c(_r(x, unit))] for x in ns]
        i, j = sorted(random.sample(range(4), 2))
        return _dt("The table rounds each number to the nearest %s. Use the rounded "
                   "values to estimate the total of %s and %s."
                   % (_UNITW[unit], _c(ns[i]), _c(ns[j])),
                   ["Number", "Rounded to the nearest %s" % _UNITW[unit]], rows,
                   _r(ns[i], unit) + _r(ns[j], unit),
                   ["%s + %s = %s." % (_c(_r(ns[i], unit)), _c(_r(ns[j], unit)),
                                       _c(_r(ns[i], unit) + _r(ns[j], unit)))])

    def t_table_est():
        items = random.sample(["Chairs", "Desks", "Shelves", "Cabinets", "Lamps"], 3)
        vals = [random.randint(1010, 9990) for _ in range(3)]
        rows = [[it, "£" + _c(v)] for it, v in zip(items, vals)]
        est = sum(_r(v, 1000) for v in vals)
        return _dt("Estimate the total cost by rounding every price to the nearest "
                   "£1,000.", ["Item", "Price"], rows, est,
                   ["Rounded: %s." % ", ".join("£" + _c(_r(v, 1000)) for v in vals),
                    "The estimated total is £%s." % _c(est)], atype="int")

    def t_io():
        b = random.randint(11, 40)
        ins = sorted(random.sample(range(100, 900), 4))
        rows = [[i, i * b] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number follows the same rule. Work out the rule, then "
                   "fill the empty cell.", rows, miss, rows[miss][1],
                   ["Use the inverse: %s ÷ %s = %d gives the rule × %d."
                    % (_c(rows[0][1]), _c(rows[0][0]), b, b),
                    "%s × %d = %s." % (_c(rows[miss][0]), b, _c(rows[miss][1]))])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        vals = [random.randint(1100, 9900) for _ in range(4)]
        i, j = sorted(random.sample(range(4), 2))
        est = _r(vals[i], 1000) + _r(vals[j], 1000)
        return _bar("The bar chart shows tickets sold. Estimate how many tickets "
                    "were sold at %s and %s altogether, by rounding each number to "
                    "the nearest 1,000." % (cats[i], cats[j]), cats, vals, est,
                    ["%s rounds to %s and %s rounds to %s."
                     % (_c(vals[i]), _c(_r(vals[i], 1000)),
                        _c(vals[j]), _c(_r(vals[j], 1000))),
                     "The estimate is %s." % _c(est)])

    def t_est_sum4():
        unit = 100 if d == 0 else pick([100, 1000])
        a = random.randint(1010, 9899)
        b = random.randint(1010, 9899)
        return _tb("Estimate the sum of the four-digit whole numbers %s and %s by "
                   "rounding each number to the nearest %s."
                   % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) + _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s + %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) + _r(b, unit)))])

    def t_est_diff4():
        unit = 100 if d == 0 else pick([100, 1000])
        a = random.randint(6010, 9899)
        b = random.randint(1010, 3899)
        return _tb("Estimate the difference between the four-digit whole numbers %s "
                   "and %s by rounding each number to the nearest %s."
                   % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) - _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s − %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) - _r(b, unit)))])

    def t_est_sum6():
        unit = 10000 if d == 0 else pick([10000, 100000])
        a = random.randint(101000, 989999)
        b = random.randint(101000, 989999)
        return _tb("Estimate the sum of the six-digit whole numbers %s and %s by "
                   "rounding each number to the nearest %s."
                   % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) + _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s + %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) + _r(b, unit)))])

    def t_est_diff6():
        unit = 10000 if d == 0 else pick([10000, 100000])
        a = random.randint(601000, 989999)
        b = random.randint(101000, 389999)
        return _tb("Estimate the difference between the six-digit whole numbers %s "
                   "and %s by rounding each number to the nearest %s."
                   % (_c(a), _c(b), _UNITW[unit]),
                   _r(a, unit) - _r(b, unit), "int", {},
                   ["%s rounds to %s and %s rounds to %s."
                    % (_c(a), _c(_r(a, unit)), _c(b), _c(_r(b, unit))),
                    "%s − %s = %s." % (_c(_r(a, unit)), _c(_r(b, unit)),
                                       _c(_r(a, unit) - _r(b, unit)))])

    def t_compatible():
        b = random.randint(3, 9)
        scale = {0: 10, 1: 100, 2: 1000}[d]
        comp = random.randint(2, 9) * scale * b
        off = random.randint(1, max(2, scale))
        a = comp + (off if random.random() < 0.5 else -off)
        if a % b == 0:
            a += 1
        return _tb("Estimate the quotient %s ÷ %d using compatible numbers. Replace "
                   "%s with the compatible number %s, which divides exactly by %d, "
                   "and work out the estimate." % (_c(a), b, _c(a), _c(comp), b),
                   comp // b, "int", {},
                   ["%s and %d are compatible numbers because %s ÷ %d has no "
                    "remainder." % (_c(comp), b, _c(comp), b),
                    "%s ÷ %d = %s." % (_c(comp), b, _c(comp // b))])

    return _pick_t([t_est_add, t_est_sub, t_est_mult, t_est_div, t_reasonable,
                    t_inverse_add, t_inverse_mult, t_find_error, t_est_total,
                    t_est_sum4, t_est_diff4, t_est_sum6, t_est_diff6,
                    t_compatible],
                   [t_table, t_table_est, t_io, t_bar])


@skill("Y6.1.h", "Order of operations (BIDMAS)", S1)
def _(d=1):
    d = _d(d)
    HI = {0: 9, 1: 12, 2: 20}[d]

    def t_add_mult():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        return _tb("Work out:   %d + %d × %d" % (a, b, cc), a + b * cc, "int", {},
                   ["Multiplication comes before addition.",
                    "%d × %d = %d." % (b, cc, b * cc),
                    "%d + %d = %d." % (a, b * cc, a + b * cc)])

    def t_mult_sub():
        b, cc = random.randint(3, HI), random.randint(2, HI)
        a = random.randint(1, b * cc)
        return _tb("Work out:   %d × %d − %d" % (b, cc, a), b * cc - a, "int", {},
                   ["Multiplication comes before subtraction.",
                    "%d × %d = %d." % (b, cc, b * cc),
                    "%d − %d = %d." % (b * cc, a, b * cc - a)])

    def t_brackets_add():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        return _tb("Work out:   (%d + %d) × %d" % (a, b, cc), (a + b) * cc, "int", {},
                   ["Brackets first: %d + %d = %d." % (a, b, a + b),
                    "%d × %d = %d." % (a + b, cc, (a + b) * cc)])

    def t_brackets_sub():
        a = random.randint(5, HI + 8)
        b = random.randint(1, a - 1)
        cc = random.randint(2, HI)
        return _tb("Work out:   (%d − %d) × %d" % (a, b, cc), (a - b) * cc, "int", {},
                   ["Brackets first: %d − %d = %d." % (a, b, a - b),
                    "%d × %d = %d." % (a - b, cc, (a - b) * cc)])

    def t_div_add():
        b = random.randint(2, 9)
        q = random.randint(2, HI)
        a = random.randint(2, HI)
        return _tb("Work out:   %d ÷ %d + %d" % (q * b, b, a), q + a, "int", {},
                   ["Division comes before addition.",
                    "%d ÷ %d = %d." % (q * b, b, q),
                    "%d + %d = %d." % (q, a, q + a)])

    def t_sub_div():
        b = random.randint(2, 9)
        q = random.randint(2, HI)
        a = q * b + random.randint(1, HI)
        return _tb("Work out:   %d − %d ÷ %d" % (a, q * b, b), a - q, "int", {},
                   ["Division comes before subtraction.",
                    "%d ÷ %d = %d." % (q * b, b, q),
                    "%d − %d = %d." % (a, q, a - q)])

    def t_square():
        a = random.randint(2, HI)
        b = random.randint(3, 12)
        return _tb("Work out:   %d + %d²" % (a, b), a + b * b, "int", {},
                   ["Indices come before addition.",
                    "%d² = %d." % (b, b * b),
                    "%d + %d = %d." % (a, b * b, a + b * b)])

    def t_square_mult():
        a = random.randint(2, 9)
        b = random.randint(3, 9)
        return _tb("Work out:   %d × %d²" % (a, b), a * b * b, "int", {},
                   ["%d² = %d." % (b, b * b),
                    "%d × %d = %d." % (a, b * b, a * b * b)])

    def t_three_ops():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        e = random.randint(1, a + b * cc)
        return _tb("Work out:   %d + %d × %d − %d" % (a, b, cc, e),
                   a + b * cc - e, "int", {},
                   ["%d × %d = %d first." % (b, cc, b * cc),
                    "%d + %d − %d = %d." % (a, b * cc, e, a + b * cc - e)])

    def t_bracket_div():
        b = random.randint(2, 9)
        q = random.randint(2, HI)
        a = random.randint(1, q * b - 1)
        return _tb("Work out:   (%d + %d) ÷ %d" % (a, q * b - a, b), q, "int", {},
                   ["Brackets first: %d + %d = %d." % (a, q * b - a, q * b),
                    "%d ÷ %d = %d." % (q * b, b, q)])

    def t_compare():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        v1, v2 = a + b * cc, (a + b) * cc
        while v1 == v2:
            a, b, cc = (random.randint(2, HI) for _ in range(3))
            v1, v2 = a + b * cc, (a + b) * cc
        return _tb("Which is larger, %d + %d × %d or (%d + %d) × %d? Type the larger "
                   "value." % (a, b, cc, a, b, cc), max(v1, v2), "int", {},
                   ["%d + %d × %d = %d." % (a, b, cc, v1),
                    "(%d + %d) × %d = %d." % (a, b, cc, v2),
                    "The larger value is %d." % max(v1, v2)])

    def t_difference():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        v1, v2 = a + b * cc, (a + b) * cc
        return _tb("Work out %d + %d × %d and then (%d + %d) × %d. What is the "
                   "difference between the two answers?" % (a, b, cc, a, b, cc),
                   abs(v1 - v2), "int", {},
                   ["%d + %d × %d = %d." % (a, b, cc, v1),
                    "(%d + %d) × %d = %d." % (a, b, cc, v2),
                    "The difference is %d." % abs(v1 - v2)])

    def t_io():
        m = random.randint(2, 9)
        add = random.randint(2, 20)
        ins = sorted(random.sample(range(2, 30), 4))
        rows = [[i, i * m + add] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number is worked out with the rule shown. What number "
                   "goes in the empty cell?", rows, miss, rows[miss][1],
                   ["Multiply first, then add.",
                    "%d × %d + %d = %d." % (rows[miss][0], m, add, rows[miss][1])],
                   rule="× %d + %d" % (m, add))

    def t_table():
        rows = []
        vals = []
        for _ in range(3):
            a, b, cc = (random.randint(2, HI) for _ in range(3))
            expr = pick(["%d + %d × %d" % (a, b, cc),
                         "(%d + %d) × %d" % (a, b, cc),
                         "%d × %d + %d" % (a, b, cc)])
            v = eval(expr.replace("×", "*"))
            rows.append([expr, str(v)])
            vals.append(v)
        r = random.randint(0, 2)
        return _dt("Work out each expression using BIDMAS. What value belongs in the "
                   "empty cell?", ["Expression", "Value"], rows, vals[r],
                   ["Work out brackets and multiplication before addition.",
                    "%s = %d." % (rows[r][0], vals[r])], missing=[r, 1])

    def t_true_false():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        form = random.randrange(4)
        if form == 0:
            expr, true, alt = "%d + %d × %d" % (a, b, cc), a + b * cc, (a + b) * cc
        elif form == 1:
            expr, true, alt = "(%d + %d) × %d" % (a, b, cc), (a + b) * cc, a + b * cc
        elif form == 2:
            q = random.randint(2, 9)
            expr = "%d + %d ÷ %d" % (a, q * b, b)
            true, alt = a + q, (a + q * b) // b
        else:
            e = random.randint(1, b * cc)
            expr = "%d × %d − %d" % (b, cc, e)
            true, alt = b * cc - e, b * cc - e + random.randint(1, 6)
        if alt == true:
            alt = true + random.randint(1, 6)
        shown = true if random.random() < 0.5 else alt
        ans = "true" if shown == true else "false"
        return _wq("Is this equation with mixed operations true or false?   %s = %d "
                   "  (type 'true' or 'false')" % (expr, shown), ans,
                   ["Use BIDMAS: %s = %d." % (expr, true),
                    "The equation shows %d, so it is %s." % (shown, ans)],
                   "true / false")

    return _pick_t([t_add_mult, t_mult_sub, t_brackets_add, t_brackets_sub,
                    t_div_add, t_sub_div, t_square, t_square_mult, t_three_ops,
                    t_bracket_div, t_compare, t_difference, t_true_false],
                   [t_io, t_table])


@skill("Y6.1.i", "Write and evaluate numerical expressions", S1)
def _(d=1):
    d = _d(d)
    HI = {0: 10, 1: 15, 2: 25}[d]
    SIGNS = "add / subtract / multiply / divide"

    def t_sign_add():
        a, b = random.randint(3, HI), random.randint(3, HI)
        return _wq("Which operation makes this true?   %d ___ %d = %d   (type "
                   "'add', 'subtract', 'multiply' or 'divide')" % (a, b, a + b),
                   "add", ["%d + %d = %d." % (a, b, a + b)], SIGNS)

    def t_sign_sub():
        b = random.randint(3, HI - 1)
        a = random.randint(HI, HI * 2)
        if a % b == 0:                    # else a ÷ b could also fit
            a += 1
        return _wq("Which operation makes this true?   %d ___ %d = %d   (type "
                   "'add', 'subtract', 'multiply' or 'divide')" % (a, b, a - b),
                   "subtract", ["%d − %d = %d." % (a, b, a - b)], SIGNS)

    def t_sign_mult():
        a, b = random.randint(3, 12), random.randint(3, 12)
        return _wq("Which operation makes this true?   %d ___ %d = %d   (type "
                   "'add', 'subtract', 'multiply' or 'divide')" % (a, b, a * b),
                   "multiply", ["%d × %d = %d." % (a, b, a * b)], SIGNS)

    def t_sign_div():
        b, q = random.randint(3, 12), random.randint(3, 12)
        return _wq("Which operation makes this true?   %d ___ %d = %d   (type "
                   "'add', 'subtract', 'multiply' or 'divide')" % (q * b, b, q),
                   "divide", ["%d ÷ %d = %d." % (q * b, b, q)], SIGNS)

    def t_product_minus():
        a, b = random.randint(3, 12), random.randint(3, 12)
        cc = random.randint(1, a * b - 1)
        return _tb("Write this as a calculation and work it out: subtract %d from "
                   "the product of %d and %d." % (cc, a, b), a * b - cc, "int", {},
                   ["The product of %d and %d is %d." % (a, b, a * b),
                    "%d − %d = %d." % (a * b, cc, a * b - cc)])

    def t_sum_times():
        a, b = random.randint(2, HI), random.randint(2, HI)
        cc = random.randint(2, 9)
        return _tb("Write this as a calculation and work it out: multiply the sum of "
                   "%d and %d by %d." % (a, b, cc), (a + b) * cc, "int", {},
                   ["The sum of %d and %d is %d." % (a, b, a + b),
                    "%d × %d = %d." % (a + b, cc, (a + b) * cc)])

    def t_double_sum():
        a, b = random.randint(10, 99), random.randint(10, 99)
        return _tb("Write this as a calculation and work it out: double the sum of "
                   "%d and %d." % (a, b), 2 * (a + b), "int", {},
                   ["%d + %d = %d." % (a, b, a + b),
                    "%d × 2 = %d." % (a + b, 2 * (a + b))])

    def t_difference_divided():
        b = random.randint(2, 9)
        q = random.randint(3, 20)
        small = random.randint(2, HI)
        big = small + q * b
        return _tb("Write this as a calculation and work it out: divide the "
                   "difference between %d and %d by %d." % (big, small, b), q,
                   "int", {},
                   ["The difference between %d and %d is %d." % (big, small, q * b),
                    "%d ÷ %d = %d." % (q * b, b, q)])

    def t_evaluate():
        a, b, cc = (random.randint(2, HI) for _ in range(3))
        return _tb("Work out the value of this expression:   %d × (%d + %d)"
                   % (a, b, cc), a * (b + cc), "int", {},
                   ["Brackets first: %d + %d = %d." % (b, cc, b + cc),
                    "%d × %d = %d." % (a, b + cc, a * (b + cc))])

    def t_missing_number():
        m = random.randint(3, 9)
        x = random.randint(3, 20)
        add = random.randint(2, 30)
        return _tb("Find the missing number:   %d × ___ + %d = %d"
                   % (m, add, m * x + add), x, "int", {},
                   ["%d − %d = %d." % (m * x + add, add, m * x),
                    "%d ÷ %d = %d." % (m * x, m, x)])

    def t_missing_in_brackets():
        cc = random.randint(2, 9)
        a = random.randint(2, HI)
        b = random.randint(2, HI)
        return _tb("Find the missing number:   (%d + ___) × %d = %d"
                   % (a, cc, (a + b) * cc), b, "int", {},
                   ["%d ÷ %d = %d." % ((a + b) * cc, cc, a + b),
                    "%d − %d = %d." % (a + b, a, b)])

    def t_word_expr():
        who = pick(NAMES)
        a = random.randint(3, 12)
        b = random.randint(10, 99)
        cc = random.randint(1, 50)
        return _tb("%s buys %d packs of cards costing %d p each and pays with a %d p "
                   "voucher. Write a calculation for the amount still to pay, then "
                   "work it out." % (who, a, b, a * b + cc), cc, "int", {"unit": "p"},
                   ["%d × %d = %d." % (a, b, a * b),
                    "%d − %d = %d." % (a * b + cc, a * b, cc)])

    def t_table():
        rows = []
        vals = []
        for _ in range(3):
            a, b, cc = (random.randint(2, HI) for _ in range(3))
            phrase, v = pick([("the sum of %d and %d, multiplied by %d" % (a, b, cc),
                               (a + b) * cc),
                              ("the product of %d and %d, plus %d" % (a, b, cc),
                               a * b + cc),
                              ("%d more than the product of %d and %d" % (cc, a, b),
                               a * b + cc)])
            rows.append([phrase, str(v)])
            vals.append(v)
        r = random.randint(0, 2)
        return _dt("Each row describes a calculation in words. What value belongs in "
                   "the empty cell?", ["In words", "Value"], rows, vals[r],
                   ["%s = %d." % (rows[r][0].capitalize(), vals[r])],
                   missing=[r, 1])

    def t_table_sign():
        a, b = random.randint(3, 12), random.randint(3, 12)
        which = pick(["add", "subtract", "multiply", "divide"])
        if which == "add":
            x, y, v, sym = a, b, a + b, "+"
        elif which == "subtract":
            x, y, v, sym = a * b, b, a * b - b, "−"
        elif which == "multiply":
            x, y, v, sym = a, b, a * b, "×"
        else:
            x, y, v, sym = a * b, b, a, "÷"
        return _dt("Which operation belongs in the empty cell? (type 'add', "
                   "'subtract', 'multiply' or 'divide')",
                   ["First number", "Operation", "Second number", "Answer"],
                   [[str(x), sym, str(y), str(v)]], which,
                   ["%d %s %d = %d." % (x, sym, y, v)], missing=[0, 1], atype="str")

    def t_io():
        m = random.randint(2, 9)
        sub = random.randint(1, 10)
        ins = sorted(random.sample(range(5, 40), 4))
        rows = [[i, i * m - sub] for i in ins]
        miss = random.randint(0, 3)
        return _io("Every Out number is worked out with the rule shown. What number "
                   "goes in the empty cell?", rows, miss, rows[miss][1],
                   ["%d × %d = %d, then subtract %d."
                    % (rows[miss][0], m, rows[miss][0] * m, sub),
                    "The answer is %d." % rows[miss][1]],
                   rule="× %d − %d" % (m, sub))

    return _pick_t([t_sign_add, t_sign_sub, t_sign_mult, t_sign_div,
                    t_product_minus, t_sum_times, t_double_sum,
                    t_difference_divided, t_evaluate, t_missing_number,
                    t_missing_in_brackets, t_word_expr],
                   [t_table, t_table_sign, t_io])


@skill("Y6.1.j", "Multi-step problems with the four operations", S1)
def _(d=1):
    d = _d(d)
    SC = {0: 1, 1: 2, 2: 4}[d]

    def t_shopping():
        who = pick(NAMES)
        a, b = random.randint(2, 6), random.randint(2, 6)
        p1 = random.randint(2, 9) * 3 * SC
        p2 = random.randint(1, 8) * 2 * SC
        spent = a * p1 + b * p2
        paid = spent + random.randint(1, 20) * 5
        return _tb("%s buys %d books at £%s each and %d pens at £%s each, and pays "
                   "with £%s. How much change does %s get?"
                   % (who, a, _c(p1), b, _c(p2), _c(paid), who), paid - spent,
                   "int", {"unit": "£"},
                   ["%d × £%s = £%s." % (a, _c(p1), _c(a * p1)),
                    "%d × £%s = £%s." % (b, _c(p2), _c(b * p2)),
                    "£%s + £%s = £%s spent." % (_c(a * p1), _c(b * p2), _c(spent)),
                    "£%s − £%s = £%s." % (_c(paid), _c(spent), _c(paid - spent))])

    def t_share_after():
        who = pick(NAMES)
        n = random.randint(3, 9)
        each = random.randint(10, 60) * SC
        used = random.randint(5, 40) * SC
        total = n * each + used
        return _tb("A school has %s pencils and uses %s of them. The rest are shared "
                   "equally between %d classes. How many pencils does each class "
                   "get?" % (_c(total), _c(used), n), each, "int",
                   {"unit": "pencils"},
                   ["%s − %s = %s left." % (_c(total), _c(used), _c(n * each)),
                    "%s ÷ %d = %s." % (_c(n * each), n, _c(each))])

    def t_rate():
        who = pick(NAMES)
        per = random.randint(120, 900)
        days = random.randint(4, 12)
        extra = random.randint(50, 500)
        return _tb("%s runs %s metres each day for %d days, and then runs a further "
                   "%s metres. What is the total distance %s runs?"
                   % (who, _c(per), days, _c(extra), who), per * days + extra,
                   "int", {"unit": "m"},
                   ["%d × %s = %s." % (days, _c(per), _c(per * days)),
                    "%s + %s = %s." % (_c(per * days), _c(extra),
                                       _c(per * days + extra))])

    def t_boxes_left():
        per = random.randint(12, 40)
        boxes = random.randint(20, 90)
        sold = random.randint(50, per * boxes - 50)
        return _tb("A warehouse has %d boxes with %d items in each box. %s items are "
                   "sold. How many items are left?" % (boxes, per, _c(sold)),
                   per * boxes - sold, "int", {"unit": "items"},
                   ["%d × %d = %s." % (boxes, per, _c(per * boxes)),
                    "%s − %s = %s." % (_c(per * boxes), _c(sold),
                                       _c(per * boxes - sold))])

    def t_tiles():
        w = random.randint(6, 25)
        h = random.randint(6, 25)
        packs = random.randint(4, 12)
        per_pack = (w * h) // packs + 1
        return _tb("A floor is %d tiles wide and %d tiles long. Tiles come in packs "
                   "of %d. How many whole packs are needed to cover the floor "
                   "completely?" % (w, h, per_pack), -(-(w * h) // per_pack),
                   "int", {"unit": "packs"},
                   ["%d × %d = %d tiles are needed." % (w, h, w * h),
                    "%d ÷ %d = %d remainder %d, so %d packs are needed."
                    % (w * h, per_pack, (w * h) // per_pack, (w * h) % per_pack,
                       -(-(w * h) // per_pack))])

    def t_money_split():
        n = random.randint(3, 8)
        each = random.randint(20, 300)
        fee = random.randint(10, 200)
        total = n * each + fee
        return _tb("A group raises £%s. £%s is kept for costs and the rest is shared "
                   "equally between %d charities. How much does each charity get?"
                   % (_c(total), _c(fee), n), each, "int", {"unit": "£"},
                   ["£%s − £%s = £%s." % (_c(total), _c(fee), _c(n * each)),
                    "£%s ÷ %d = £%s." % (_c(n * each), n, _c(each))])

    def t_compare_totals():
        a1, p1 = random.randint(3, 9), random.randint(20, 200)
        a2, p2 = random.randint(3, 9), random.randint(20, 200)
        while a1 * p1 == a2 * p2:
            p2 = random.randint(20, 200)
        return _tb("Shop A sells %d boxes at £%d each. Shop B sells %d boxes at £%d "
                   "each. What is the difference between the two totals?"
                   % (a1, p1, a2, p2), abs(a1 * p1 - a2 * p2), "int", {"unit": "£"},
                   ["Shop A: %d × £%d = £%s." % (a1, p1, _c(a1 * p1)),
                    "Shop B: %d × £%d = £%s." % (a2, p2, _c(a2 * p2)),
                    "The difference is £%s." % _c(abs(a1 * p1 - a2 * p2))])

    def t_journey():
        speed = random.randint(40, 90)
        hours = random.randint(2, 6)
        rest = random.randint(10, 200)
        total = speed * hours + rest
        return _tb("A coach travels %d kilometres each hour for %d hours, then "
                   "travels a further %d kilometres. How far does the coach travel "
                   "in total?" % (speed, hours, rest), total, "int", {"unit": "km"},
                   ["%d × %d = %d." % (speed, hours, speed * hours),
                    "%d + %d = %d." % (speed * hours, rest, total)])

    def t_missing_step():
        n = random.randint(4, 12)
        each = random.randint(15, 90)
        total = n * each
        extra = random.randint(10, 200)
        return _tb("%s items are packed equally into %d crates, and then %s more "
                   "items are added to one crate. How many items are in that crate "
                   "now?" % (_c(total), n, _c(extra)), each + extra, "int",
                   {"unit": "items"},
                   ["%s ÷ %d = %d in each crate." % (_c(total), n, each),
                    "%d + %s = %s." % (each, _c(extra), _c(each + extra))])

    def t_table_bill():
        items = random.sample(["Paint", "Brushes", "Rollers", "Trays", "Cloths"], 3)
        qty = [random.randint(3, 20) for _ in range(3)]
        price = [random.randint(3, 60) for _ in range(3)]
        rows = [[it, str(q), "£" + str(p)] for it, q, p in zip(items, qty, price)]
        total = sum(q * p for q, p in zip(qty, price))
        return _dt("The table shows an order. What is the total cost in pounds?",
                   ["Item", "Quantity", "Price each"], rows, total,
                   ["%s." % "; ".join("%d × £%d = £%s" % (q, p, _c(q * p))
                                      for q, p in zip(qty, price)),
                    "The total is £%s." % _c(total)])

    def t_table_change():
        items = random.sample(["Tent", "Sleeping bag", "Torch", "Stove", "Map"], 3)
        price = [random.randint(5, 80) for _ in range(3)]
        rows = [[it, "£" + str(p)] for it, p in zip(items, price)]
        i, j = sorted(random.sample(range(3), 2))
        spent = price[i] + price[j]
        paid = spent + random.randint(1, 40)
        return _dt("The table shows prices in a camping shop. %s buys the %s and the "
                   "%s and pays with £%d. How much change is there?"
                   % (pick(NAMES), items[i].lower(), items[j].lower(), paid),
                   ["Item", "Price"], rows, paid - spent,
                   ["£%d + £%d = £%d spent." % (price[i], price[j], spent),
                    "£%d − £%d = £%d." % (paid, spent, paid - spent)])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        vals = [random.randint(40, 400) for _ in range(4)]
        i, j = sorted(random.sample(range(4), 2))
        n = random.randint(2, 8)
        return _bar("The bar chart shows how many books each library received. The "
                    "books from %s and %s are put together and shared equally "
                    "between %d schools. How many books does each school get? "
                    "(Type the whole-number part.)" % (cats[i], cats[j], n),
                    cats, vals, (vals[i] + vals[j]) // n,
                    ["%d + %d = %d books." % (vals[i], vals[j], vals[i] + vals[j]),
                     "%d ÷ %d = %d remainder %d."
                     % (vals[i] + vals[j], n, (vals[i] + vals[j]) // n,
                        (vals[i] + vals[j]) % n)])

    def t_pict():
        cats = random.sample(_TOWNS, 4)
        key = pick([5, 10, 20])
        counts = [random.randint(2, 9) for _ in range(4)]
        vals = [cc * key for cc in counts]
        i, j = sorted(random.sample(range(4), 2))
        return _pict("The pictogram shows tickets sold. How many more tickets were "
                     "sold at %s than at %s?"
                     % (cats[i] if vals[i] >= vals[j] else cats[j],
                        cats[j] if vals[i] >= vals[j] else cats[i]),
                     cats, vals, key, "★", abs(vals[i] - vals[j]),
                     ["%s sold %d and %s sold %d."
                      % (cats[i], vals[i], cats[j], vals[j]),
                      "The difference is %d." % abs(vals[i] - vals[j])])

    def t_strip():
        parts = random.randint(3, 8)
        each = random.randint(30, 400)
        return _strip("The bar shows %s shared equally into %d parts. Two of the "
                      "parts are put together. How many are in those two parts?"
                      % (_c(parts * each), parts), parts, "?", _c(parts * each),
                      "part", 2 * each,
                      ["%s ÷ %d = %s in each part." % (_c(parts * each), parts, _c(each)),
                       "%s × 2 = %s." % (_c(each), _c(2 * each))])

    def t_reasonable():
        per = random.randint(12, 40)
        boxes = random.randint(20, 90)
        extra = random.randint(20, 200)
        true = per * boxes + extra
        opts = [true, true * 10, true // 10]
        random.shuffle(opts)
        return _tb("A warehouse holds %d boxes with %d items in each box, and a "
                   "further %d loose items. This multi-step word problem has one "
                   "reasonable answer. Use estimation to identify the reasonable "
                   "answer, then type it:   %s"
                   % (boxes, per, extra, ", ".join(_c(x) for x in opts)),
                   true, "int", {"unit": "items"},
                   ["About %d × %d is about %s." % (boxes, per, _c(boxes * per)),
                    "Adding %d gives %s, so %s is the reasonable answer."
                    % (extra, _c(true), _c(true))])

    def _info_case():
        return pick([("boxes", "box", "tea", "teabags"),
                     ("crates", "crate", "apples", "apples"),
                     ("packs", "pack", "pencils", "pencils"),
                     ("sacks", "sack", "flour", "bread rolls")])

    def t_extra_info():
        pl, sg, goods, inner = _info_case()
        qty = random.randint(12, 40)
        price = random.randint(3, 30)
        held = random.randint(20, 60)
        facts = [("There are %d %s of %s." % (qty, pl, goods), False),
                 ("Each %s costs £%d." % (sg, price), False),
                 ("Each %s holds %d %s." % (sg, held, inner), True)]
        random.shuffle(facts)
        ans = [i for i, f in enumerate(facts) if f[1]][0] + 1
        text = "   ".join("%d. %s" % (i + 1, f[0]) for i, f in enumerate(facts))
        return _tb("This word problem has extra information. To work out the total "
                   "cost of the %s of %s, which numbered fact is NOT needed? Type "
                   "1, 2 or 3.   %s" % (pl, goods, text), ans, "int", {},
                   ["The total cost is the number of %s multiplied by the price of "
                    "each %s." % (pl, sg),
                    "Fact %d gives the number of %s in each %s, which the cost does "
                    "not depend on." % (ans, inner, sg)])

    def t_missing_info():
        pl, sg, goods, inner = _info_case()
        qty = random.randint(12, 40)
        price = random.randint(3, 30)
        held = random.randint(20, 60)
        hide_price = random.random() < 0.5
        given = ["Each %s holds %d %s." % (sg, held, inner)]
        if hide_price:
            given.append("There are %d %s of %s." % (qty, pl, goods))
            ans = "the price of each %s" % sg
        else:
            given.append("Each %s costs £%d." % (sg, price))
            ans = "the number of %s" % pl
        random.shuffle(given)
        opts = ["the number of %s" % pl, "the price of each %s" % sg,
                "the number of %s in each %s" % (inner, sg)]
        return _wq("This word problem has missing information.   %s   The question "
                   "is: what is the total cost of the %s of %s? Type the "
                   "information that is still needed: '%s', '%s' or '%s'."
                   % ("   ".join(given), pl, goods, opts[0], opts[1], opts[2]), ans,
                   ["The total cost needs the number of %s and the price of each %s."
                    % (pl, sg),
                    "The word problem does not give %s, so that is the missing "
                    "information." % ans],
                   "type the missing information")

    return _pick_t([t_shopping, t_share_after, t_rate, t_boxes_left, t_tiles,
                    t_money_split, t_compare_totals, t_journey, t_missing_step,
                    t_reasonable, t_extra_info, t_missing_info],
                   [t_table_bill, t_table_change, t_bar, t_pict, t_strip])


@skill("Y6.1.k", "Interpret remainders in context", S1)
def _(d=1):
    d = _d(d)
    SC = {0: 1, 1: 2, 2: 4}[d]

    def t_coaches():
        per = random.randint(30, 56)
        total = random.randint(200, 400) * SC
        if total % per == 0:
            total += 1
        return _tb("%s pupils go on a trip. Each coach holds %d pupils. How many "
                   "coaches are needed?" % (_c(total), per), -(-total // per),
                   "int", {"unit": "coaches"},
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), per, total // per, total % per),
                    "The %d pupils left over still need a coach, so %d coaches are "
                    "needed." % (total % per, -(-total // per))])

    def t_full_boxes():
        per = random.randint(6, 24)
        total = random.randint(100, 400) * SC
        if total % per == 0:
            total += 1
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many boxes are COMPLETELY "
                   "full?" % (_c(total), thing, per), total // per, "int",
                   {"unit": "boxes"},
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), per, total // per, total % per),
                    "Only %d boxes are completely full." % (total // per)])

    def t_left_over():
        per = random.randint(6, 24)
        total = random.randint(100, 400) * SC
        if total % per == 0:
            total += 1
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many %s are left over?"
                   % (_c(total), thing, per, thing), total % per, "int",
                   {"unit": thing},
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), per, total // per, total % per),
                    "%d are left over." % (total % per)])

    def t_how_many_more():
        per = random.randint(6, 24)
        total = random.randint(100, 400) * SC
        if total % per == 0:
            total += 1
        thing = pick(_OBJ)
        return _tb("%s %s are packed into boxes of %d. How many MORE %s are needed "
                   "to fill the last box?" % (_c(total), thing, per, thing),
                   per - total % per, "int", {"unit": thing},
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), per, total // per, total % per),
                    "%d − %d = %d more are needed."
                    % (per, total % per, per - total % per)])

    def t_money_left():
        n = random.randint(3, 9)
        total = random.randint(100, 900) * SC
        if total % n == 0:
            total += 1
        return _tb("£%s is shared equally between %d children, in whole pounds. How "
                   "many pounds are left over?" % (_c(total), n), total % n, "int",
                   {"unit": "£"},
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), n, total // n, total % n),
                    "£%d is left over." % (total % n)])

    def t_fraction():
        n = random.randint(3, 10)
        q = random.randint(10, 90)
        r = random.randint(1, n - 1)
        total = q * n + r
        return _tb("%d cakes are shared equally between %d people, and the last cake "
                   "is cut up. Each person gets %d whole cakes and a fraction of "
                   "another. Type that fraction, for example 3/8."
                   % (total, n, q), "%d/%d" % (r, n), "frac",
                   {"text": True, "placeholder": "e.g. 3/8"},
                   ["%d ÷ %d = %d remainder %d." % (total, n, q, r),
                    "The %d remaining cakes shared between %d people is %d/%d each."
                    % (r, n, r, n)])

    def t_rounded():
        n = random.randint(3, 12)
        q = random.randint(20, 90)
        r = random.randint(1, n - 1)
        total = q * n + r
        ans = q + 1 if 2 * r >= n else q
        return _tb("%d metres of rope is cut into %d equal pieces. How long is each "
                   "piece, to the nearest whole metre?" % (total, n), ans, "int",
                   {"unit": "m"},
                   ["%d ÷ %d = %d remainder %d." % (total, n, q, r),
                    "The remainder %d is %s half of %d, so each piece is about %d m."
                    % (r, "at least" if 2 * r >= n else "less than", n, ans)])

    def t_reasonable():
        per = random.randint(20, 50)
        total = random.randint(200, 900)
        if total % per == 0:
            total += 1
        right = -(-total // per)
        claim = (total // per) if random.random() < 0.5 else right
        return _yn("%s pupils each need one seat and every minibus holds %d pupils. "
                   "%s says %d minibuses are enough. Is that correct? (type 'yes' or "
                   "'no')" % (_c(total), per, pick(NAMES), claim),
                   "yes" if claim >= right else "no",
                   ["%s ÷ %d = %d remainder %d."
                    % (_c(total), per, total // per, total % per),
                    "%d minibuses are needed, so the answer is %s."
                    % (right, "yes" if claim >= right else "no")])

    def t_lifts():
        cap = random.randint(8, 16)
        total = random.randint(60, 400)
        if total % cap == 0:
            total += 1
        return _tb("%d people are waiting for a lift that carries %d people at a "
                   "time. How many lift journeys are needed to carry everyone?"
                   % (total, cap), -(-total // cap), "int", {"unit": "journeys"},
                   ["%d ÷ %d = %d remainder %d."
                    % (total, cap, total // cap, total % cap),
                    "The people left over need one more journey, so %d journeys are "
                    "needed." % (-(-total // cap))])

    def t_table():
        per = random.randint(6, 24)
        ins = sorted(random.sample(range(200, 2000), 4))
        rows = [[_c(i), _c(i // per), str(i % per)] for i in ins]
        r = random.randint(0, 3)
        col = pick([1, 2])
        ans = ins[r] // per if col == 1 else ins[r] % per
        return _dt("Items are packed into boxes of %d. The table shows full boxes "
                   "and items left over. What belongs in the empty cell?" % per,
                   ["Items", "Full boxes", "Left over"], rows, ans,
                   ["%s ÷ %d = %s remainder %d."
                    % (_c(ins[r]), per, _c(ins[r] // per), ins[r] % per)],
                   missing=[r, col])

    def t_table_coaches():
        rows = []
        answers = []
        for _ in range(3):
            per = random.randint(30, 56)
            total = random.randint(100, 900)
            if total % per == 0:
                total += 1
            rows.append([_c(total), str(per), str(-(-total // per))])
            answers.append(-(-total // per))
        r = random.randint(0, 2)
        return _dt("Every pupil must have a seat. What number of coaches belongs in "
                   "the empty cell?", ["Pupils", "Seats per coach", "Coaches needed"],
                   rows, answers[r],
                   ["Divide, then round UP because the pupils left over still need a "
                    "coach.", "The answer is %d." % answers[r]], missing=[r, 2])

    def t_bar():
        cats = random.sample(_TOWNS, 4)
        per = random.randint(8, 30)
        vals = [random.randint(60, 600) for _ in range(4)]
        i = random.randint(0, 3)
        if vals[i] % per == 0:
            vals[i] += 1
        return _bar("The bar chart shows how many pupils are at each school. Every "
                    "school sends its pupils in minibuses holding %d pupils. How "
                    "many minibuses does %s need?" % (per, cats[i]), cats, vals,
                    -(-vals[i] // per),
                    ["%s has %d pupils." % (cats[i], vals[i]),
                     "%d ÷ %d = %d remainder %d, so %d minibuses are needed."
                     % (vals[i], per, vals[i] // per, vals[i] % per,
                        -(-vals[i] // per))])

    def t_strip():
        parts = random.randint(3, 9)
        each = random.randint(20, 200)
        return _strip("The bar shows %s items shared equally into %d groups. How "
                      "many items are in each group?" % (_c(parts * each), parts),
                      parts, "?", _c(parts * each), "part", each,
                      ["%s ÷ %d = %s." % (_c(parts * each), parts, _c(each))])

    return _pick_t([t_coaches, t_full_boxes, t_left_over, t_how_many_more,
                    t_money_left, t_fraction, t_rounded, t_reasonable, t_lifts],
                   [t_table, t_table_coaches, t_bar, t_strip])
