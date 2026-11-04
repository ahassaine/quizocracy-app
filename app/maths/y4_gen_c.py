# dev/app/logic/y4_gen_c.py — Year 4 generators: strands 4.4 and 4.5
#
# 4.4  Multiplication & division methods   (Y4.4.a .. Y4.4.j)
# 4.5  Fractions                           (Y4.5.a .. Y4.5.k)
#
# Every generator takes a difficulty tier:  d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between many genuinely different framings (bare method,
# word problem, missing number, inverse, visual model, comparison, reasoning).
# Visual components carry a large share of the framings:
#   area_grid / array / equal_groups / strip_model  -> multiplication & division
#   fraction_bar / area_grid / number_line          -> fractions
#   bar_chart / pictogram / data_table / io_table   -> problem solving
import random
from fractions import Fraction
from .maths_engine import skill, pick, NAMES, n_words, money

S4 = "4.4 Multiplication & division methods"
S5 = "4.5 Fractions"

_OBJ = ["stickers", "marbles", "conkers", "beads", "shells", "cards", "buttons",
        "acorns", "pebbles", "counters"]
_CONT = ["boxes", "bags", "trays", "crates", "packets", "jars", "tubs"]


# ---------------------------------------------------------------- helpers ----
def _t(d):
    """Clamp the difficulty tier to 0 / 1 / 2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_t(d)]


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


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


def _fracq(prompt, num, den, solution, placeholder="e.g. 3/4"):
    """A typed fraction answer."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": "%d/%d" % (num, den), "answer_type": "frac",
            "solution": solution}


def _wordq(prompt, answer, solution, placeholder=None):
    return _numq(prompt, answer, solution, placeholder=placeholder,
                 answer_type="str", text=True)


def _fbq(prompt, parts, num, solution):
    """fraction_bar, shade mode — the answer is the shaded fraction."""
    return {"prompt": prompt, "component": "fraction_bar",
            "spec": {"parts": int(parts), "mode": "shade"},
            "answer": "%d/%d" % (num, parts), "answer_type": "frac",
            "solution": solution}


def _agshade(prompt, parts, num, solution):
    """area_grid, fraction mode — the pupil shades the area model."""
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "fraction", "parts": int(parts)},
            "answer": "%d/%d" % (num, parts), "answer_type": "frac",
            "solution": solution}


def _agread(prompt, parts, shaded, solution, answer=None, answer_type="frac",
            placeholder=None):
    """area_grid, fraction_read mode — a model with `shaded` of `parts` filled."""
    spec = {"mode": "fraction_read", "parts": int(parts), "shaded": int(shaded)}
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer if answer is not None else "%d/%d" % (shaded, parts),
            "answer_type": answer_type, "solution": solution}


def _agarea(prompt, rows, cols, solution, answer=None):
    """area_grid, read_area mode — an area model for a multiplication."""
    rows, cols = int(rows), int(cols)
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "read_area", "rows": rows, "cols": cols},
            "answer": rows * cols if answer is None else answer,
            "answer_type": "int", "solution": solution}


def _arrayq(prompt, rows, cols, solution):
    rows, cols = int(rows), int(cols)
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "build",
                     "maxRows": min(10, max(6, rows + 2)),
                     "maxCols": min(12, max(6, cols + 2)),
                     "targetRows": rows, "targetCols": cols},
            "answer": rows * cols, "answer_type": "int", "solution": solution}


def _egq(prompt, groups, per, answer, solution):
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "read", "groups": int(groups), "per": int(per)},
            "answer": answer, "answer_type": "int", "solution": solution}


def _stripq(prompt, parts, part_label, total_label, unknown, answer, solution):
    return {"prompt": prompt, "component": "strip_model",
            "spec": {"mode": "equal_parts", "parts": int(parts),
                     "partLabel": str(part_label), "totalLabel": str(total_label),
                     "unknown": unknown},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _barq(prompt, cats, vals, answer, solution, unit=None):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "mode": "read"},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _pictq(prompt, cats, vals, key, symbol, answer, solution):
    return {"prompt": prompt, "component": "pictogram",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "key": int(key), "symbol": symbol},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _dtq(prompt, headers, rows, answer, solution, missing=None,
         answer_type="int"):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type, "solution": solution}


def _ioq(prompt, rows, missing, answer, solution, rule=None, placeholder=None):
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": "int", "solution": solution}


def _nlq(prompt, value, lo, hi, step, major, solution, tol=None):
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": lo, "max": hi, "step": step, "major": major},
            "answer": round(float(value), 6), "answer_type": "num",
            "tolerance": (step / 2.0) if tol is None else tol,
            "solution": solution}


_FRAC_WORDS = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth",
               7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth", 12: "twelfth",
               100: "hundredth"}


def _frac_words(n, d):
    """1/4 -> 'one quarter';  3/5 -> 'three fifths'."""
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%d/%d" % (n, d)
    if n == 1:
        return "one " + w
    return "%s %ss" % (n_words(n), w)


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _hcf(a, b):
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


# ================================================================== 4.4 ======
@skill("Y4.4.a", "Multiply by 10, 100 and multiples of 10", S4)
def _(d=1):
    d = _t(d)
    base = _by_d(d, random.randint(2, 9), random.randint(3, 40),
                 random.randint(12, 90))
    mult = _by_d(d, pick([10, 100]), pick([10, 10, 100, 20, 30, 40, 50]),
                 pick([100, 100, 30, 40, 60, 70, 80, 90]))

    def bare():
        return _numq("Work out %d × %d." % (base, mult), base * mult,
                     ["%d × %d = %d." % (base, mult, base * mult)])

    def place_value():
        n = random.randint(3, 68)
        if random.random() < 0.5:
            return _numq("Multiply %d by 10. Every digit moves one place to the "
                         "left — what is the answer?" % n, n * 10,
                         ["%d × 10 = %d." % (n, n * 10),
                          "The digits move one place left and a 0 fills the ones "
                          "column."])
        return _numq("Multiply %d by 100. Every digit moves two places to the "
                     "left — what is the answer?" % n, n * 100,
                     ["%d × 100 = %d." % (n, n * 100),
                      "The digits move two places left."])

    def multiple_of_ten():
        a = random.randint(3, _by_d(d, 9, 12, 24))
        tens = pick([20, 30, 40, 50, 60, 70, 80, 90])
        return _numq("Work out %d × %d." % (a, tens), a * tens,
                     ["%d × %d = %d." % (a, tens // 10, a * tens // 10),
                      "Now multiply by 10: %d × 10 = %d."
                      % (a * tens // 10, a * tens)])

    def place_value_multiple():
        a = random.randint(3, _by_d(d, 9, 12, 24))
        tens = pick([20, 30, 40, 50, 60, 70, 80, 90])
        return _numq("Multiply by a multiple of 10 using place value. Work out "
                     "%d × %d." % (a, tens), a * tens,
                     ["%d is a multiple of 10: %d = %d × 10."
                      % (tens, tens, tens // 10),
                      "%d × %d = %d." % (a, tens // 10, a * tens // 10),
                      "Place value moves the digits one place left: %d × 10 = %d."
                      % (a * tens // 10, a * tens)])

    def divide_ending_zeros():
        q = random.randint(2, _by_d(d, 8, 12, 24))
        t = pick([20, 30, 40, 50, 60, 70, 80, 90])
        big = q * t
        return _numq("Divide numbers ending in zeros. Work out %d ÷ %d."
                     % (big, t), q,
                     ["Both numbers end in a zero, so take one zero off each: "
                      "%d ÷ %d." % (big // 10, t // 10),
                      "%d ÷ %d = %d." % (big // 10, t // 10, q)])

    def divide_ending_zeros_word():
        who = pick(NAMES)
        q = random.randint(3, _by_d(d, 9, 15, 30))
        t = pick([20, 30, 40, 50])
        big = q * t
        return _numq("%s shares %d beads equally into bags of %d beads. How many "
                     "bags does %s fill? Both numbers end in zeros, so divide the "
                     "easy way." % (who, big, t, who), q,
                     ["%d ÷ %d: take a zero off each number." % (big, t),
                      "%d ÷ %d = %d bags." % (big // 10, t // 10, q)],
                     unit="bags")

    def missing_factor():
        a = random.randint(3, 45)
        m = pick([10, 100])
        return _numq("Find the missing number:  %d × ___ = %d" % (a, a * m), m,
                     ["%d ÷ %d = %d." % (a * m, a, m)])

    def missing_start():
        a = random.randint(3, 45)
        m = pick([10, 100, 20, 30])
        return _numq("Find the missing number:  ___ × %d = %d" % (m, a * m), a,
                     ["%d ÷ %d = %d." % (a * m, m, a)])

    def word():
        who = pick(NAMES)
        n = random.randint(4, 24)
        m = pick([10, 100])
        return _numq("%s packs %s into %s of %d. How many %s does %s pack "
                     "altogether?" % (who, "counters", _pl(n, "box"), m,
                                      "counters", who), n * m,
                     ["%d × %d = %d counters." % (n, m, n * m)], unit="counters")

    def money_word():
        n = random.randint(3, 20)
        p = pick([10, 20, 30, 50])
        return _numq("A pencil costs %s. How much do %d pencils cost, in pence?"
                     % (money(p), n), n * p,
                     ["%d × %d = %dp." % (n, p, n * p)], unit="p")

    def io_ten():
        m = pick([10, 100, 20, 30])
        ins = sorted(random.sample(range(2, 40), 4))
        rows = [[i, i * m] for i in ins]
        k = random.randrange(4)
        return _ioq("This input/output table multiplies every In number by %d. "
                    "Type the missing Out number." % m, rows, k, rows[k][1],
                    ["The rule is × %d." % m,
                     "%d × %d = %d." % (rows[k][0], m, rows[k][1])],
                    rule="× %d" % m)

    def io_rule():
        m = pick([10, 100, 20, 50])
        ins = sorted(random.sample(range(2, 30), 4))
        rows = [[i, i * m] for i in ins]
        return _ioq("Every Out number in this table is made by multiplying the In "
                    "number by the same amount. Type the number that is multiplied "
                    "by.", rows, None, m,
                    ["%d × %d = %d." % (rows[0][0], m, rows[0][1]),
                     "The rule multiplies by %d." % m],
                    placeholder="the number")

    def compare():
        a = random.randint(3, 30)
        b = random.randint(3, 30)
        m1, m2 = pick([10, 100]), pick([10, 100, 20, 30])
        while a * m1 == b * m2:
            b = random.randint(3, 30)
        big = max(a * m1, b * m2)
        return _numq("Which is greater, %d × %d or %d × %d? Type the greater "
                     "product." % (a, m1, b, m2), big,
                     ["%d × %d = %d and %d × %d = %d."
                      % (a, m1, a * m1, b, m2, b * m2),
                      "The greater product is %d." % big])

    def chain():
        a = random.randint(2, 9)
        return _numq("Work out %d × 10 × 10." % a, a * 100,
                     ["%d × 10 = %d." % (a, a * 10),
                      "%d × 10 = %d, which is the same as %d × 100."
                      % (a * 10, a * 100, a)])

    def on_line():
        a = random.randint(2, 9)
        m = pick([10, 100])
        val = a * m
        return _nlq("Work out %d × %d and mark the answer on the number line."
                    % (a, m), val, 0, 10 * m, m, 5 * m,
                    ["%d × %d = %d." % (a, m, val),
                     "Count %s of %d from 0." % (_pl(a, "step"), m)])

    def inverse():
        a = random.randint(3, 40)
        m = pick([10, 100])
        return _numq("%d × %d = ___ . Work it out, then check by dividing the "
                     "answer by %d." % (a, m, m), a * m,
                     ["%d × %d = %d." % (a, m, a * m),
                      "Check: %d ÷ %d = %d ✓." % (a * m, m, a)])

    opts = [bare, place_value, multiple_of_ten, place_value_multiple,
            divide_ending_zeros, divide_ending_zeros_word, word, money_word,
            io_ten, on_line, missing_factor, chain, inverse]
    if d == 0:
        opts = [bare, place_value, place_value, place_value_multiple,
                divide_ending_zeros, word, io_ten, on_line, chain, money_word]
    elif d == 2:
        opts = [multiple_of_ten, place_value_multiple, divide_ending_zeros,
                divide_ending_zeros_word, missing_factor, missing_start,
                io_rule, io_ten, compare, money_word, inverse, on_line]
    opts = opts + [on_line, io_ten, on_line, on_line]
    return pick(opts)()


@skill("Y4.4.b", "Multiply a 2-digit number by a 1-digit number", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        a = random.randint(11, 19)
        b = random.randint(2, 4)
    elif d == 1:
        a = random.randint(13, 49)
        b = random.randint(3, 7)
    else:
        a = random.randint(34, 98)
        b = random.randint(6, 9)
    tens, ones = (a // 10) * 10, a % 10
    part = ["Partition %d into %d and %d." % (a, tens, ones),
            "%d × %d = %d and %d × %d = %d."
            % (tens, b, tens * b, ones, b, ones * b),
            "%d + %d = %d." % (tens * b, ones * b, a * b)]

    def bare():
        return _numq("Work out %d × %d using short multiplication." % (a, b),
                     a * b, part)

    def area_model():
        r = random.randint(2, 5)
        c = random.randint(11, 16)
        return _agarea("Use the area model to work out %d × %d. Count all the "
                       "squares — how many are there altogether?" % (r, c),
                       r, c,
                       ["The area model is %d rows of %d squares." % (r, c),
                        "%d × %d = %d." % (r, c, r * c)])

    def array_model():
        r = random.randint(2, 6)
        c = random.randint(10, 12)
        return _arrayq("Build an array with %d rows of %d to model %d × %d, then "
                       "type the total." % (r, c, r, c), r, c,
                       ["%d rows of %d." % (r, c),
                        "%d × %d = %d." % (r, c, r * c)])

    def partial_products():
        return _numq("Use partitioning:  %d × %d = (%d × %d) + (%d × %d) = ___"
                     % (a, b, tens, b, ones, b), a * b, part)

    def carry_digit():
        return _numq("In the short multiplication %d × %d, the ones are done "
                     "first. What is %d × %d?" % (a, b, ones, b), ones * b,
                     ["The ones digit of %d is %d." % (a, ones),
                      "%d × %d = %d." % (ones, b, ones * b)])

    def missing_factor():
        return _numq("Find the missing number:  %d × ___ = %d" % (a, a * b), b,
                     ["%d ÷ %d = %d." % (a * b, a, b)])

    def word():
        who = pick(NAMES)
        cont = pick(_CONT)
        thing = pick(_OBJ)
        return _numq("%s fills %d %s with %d %s in each one. How many %s "
                     "altogether?" % (who, b, cont, a, thing, thing), a * b,
                     ["%d × %d = %d %s." % (b, a, a * b, thing)], unit=thing)

    def money_word():
        cost = random.randint(12, 60)
        n = random.randint(3, 8)
        return _numq("A notebook costs %s. How much do %d notebooks cost, in "
                     "pence?" % (money(cost), n), cost * n,
                     ["%d × %d = %dp." % (cost, n, cost * n)], unit="p")

    def measure_word():
        n = random.randint(3, 9)
        per = random.randint(15, 45)
        return _numq("One shelf is %d cm long. How long are %d of these shelves "
                     "placed end to end, in cm?" % (per, n), per * n,
                     ["%d × %d = %d cm." % (per, n, per * n)], unit="cm")

    def compare():
        c = random.randint(12, 49)
        e = random.randint(3, 9)
        while c * e == a * b:
            e = random.randint(3, 9)
        big = max(a * b, c * e)
        return _numq("Which product is greater, %d × %d or %d × %d? Type the "
                     "greater product." % (a, b, c, e), big,
                     ["%d × %d = %d and %d × %d = %d."
                      % (a, b, a * b, c, e, c * e),
                      "The greater product is %d." % big])

    def io_mult():
        k = random.randint(3, 8)
        ins = sorted(random.sample(range(11, 40), 4))
        rows = [[i, i * k] for i in ins]
        m = random.randrange(4)
        return _ioq("This table multiplies each In number by %d. Type the missing "
                    "Out number." % k, rows, m, rows[m][1],
                    ["The rule is × %d." % k,
                     "%d × %d = %d." % (rows[m][0], k, rows[m][1])],
                    rule="× %d" % k)

    def two_step():
        c = random.randint(10, 60)
        return _numq("Work out %d × %d, then add %d." % (a, b, c), a * b + c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d + %d = %d." % (a * b, c, a * b + c)])

    def strip_model():
        who = pick(NAMES)
        n = random.randint(3, 6)
        per = random.randint(12, 30)
        return _stripq("Use the strip model. %s buys %d %s and each one holds %d "
                       "%s. How many %s does %s buy altogether?"
                       % (who, n, "packets", per, "seeds", "seeds", who),
                       n, str(per), "?", "total", n * per,
                       ["The strip shows %d equal parts of %d." % (n, per),
                        "%d × %d = %d seeds." % (n, per, n * per)])

    opts = [bare, area_model, array_model, partial_products, word, money_word,
            io_mult, strip_model, measure_word]
    if d == 0:
        opts = [bare, area_model, area_model, array_model, partial_products,
                word, io_mult, strip_model]
    elif d == 2:
        opts = [bare, bare, partial_products, missing_factor, carry_digit,
                compare, two_step, word, money_word, measure_word, io_mult]
    opts = opts + [area_model, array_model, strip_model, area_model]
    return pick(opts)()


@skill("Y4.4.c", "Multiply a 3-digit number by a 1-digit number", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        a = random.randint(102, 232)
        b = random.randint(2, 3)
    elif d == 1:
        a = random.randint(112, 439)
        b = random.randint(3, 6)
    else:
        a = random.randint(234, 899)
        b = random.randint(6, 9)
    h, tn, on = a // 100, (a // 10) % 10, a % 10
    part = ["Partition %d into %d, %d and %d." % (a, h * 100, tn * 10, on),
            "%d × %d = %d, %d × %d = %d, %d × %d = %d."
            % (h * 100, b, h * 100 * b, tn * 10, b, tn * 10 * b, on, b, on * b),
            "%d + %d + %d = %d."
            % (h * 100 * b, tn * 10 * b, on * b, a * b)]

    def bare():
        return _numq("Work out %d × %d using short multiplication." % (a, b),
                     a * b, part)

    def partial_products():
        return _numq("Use partitioning:  %d × %d = (%d × %d) + (%d × %d) + "
                     "(%d × %d) = ___" % (a, b, h * 100, b, tn * 10, b, on, b),
                     a * b, part)

    def hundreds_step():
        return _numq("In the short multiplication %d × %d, what is %d × %d?"
                     % (a, b, h * 100, b), h * 100 * b,
                     ["The hundreds digit of %d is %d, worth %d." % (a, h, h * 100),
                      "%d × %d = %d." % (h * 100, b, h * 100 * b)])

    def missing_factor():
        return _numq("Find the missing number:  %d × ___ = %d" % (a, a * b), b,
                     ["%d ÷ %d = %d." % (a * b, a, b)])

    def missing_start():
        return _numq("Find the missing number:  ___ × %d = %d" % (b, a * b), a,
                     ["%d ÷ %d = %d." % (a * b, b, a)])

    def word():
        n = random.randint(3, 8)
        per = random.randint(115, 380)
        return _numq("A crate holds %d apples. How many apples are there in %d "
                     "full crates?" % (per, n), per * n,
                     ["%d × %d = %d apples." % (per, n, per * n)],
                     unit="apples")

    def money_word():
        cost = random.randint(115, 450)
        n = random.randint(3, 7)
        return _numq("A ticket costs %s. How much do %d tickets cost, in pence?"
                     % (money(cost), n), cost * n,
                     ["%d × %d = %dp." % (cost, n, cost * n)], unit="p")

    def price_table():
        items = ["Kite", "Torch", "Puzzle", "Football"]
        prices = random.sample(range(120, 480), 4)
        k = random.randrange(4)
        n = random.randint(3, 6)
        rows = [[items[i], money(prices[i])] for i in range(4)]
        return _dtq("This price list shows the cost of each item. How much do %d "
                    "%ss cost altogether, in pence?" % (n, items[k].lower()),
                    ["Item", "Price"], rows, prices[k] * n,
                    ["One %s costs %s, which is %dp."
                     % (items[k].lower(), money(prices[k]), prices[k]),
                     "%d × %d = %dp." % (prices[k], n, prices[k] * n)])

    def measure_word():
        n = random.randint(3, 9)
        per = random.randint(105, 320)
        return _numq("One bag of flour has a mass of %d g. What is the mass of %d "
                     "bags, in grams?" % (per, n), per * n,
                     ["%d × %d = %d g." % (per, n, per * n)], unit="g")

    def compare():
        c = random.randint(110, 420)
        e = random.randint(3, 8)
        while c * e == a * b:
            e = random.randint(3, 8)
        big = max(a * b, c * e)
        return _numq("Which product is greater, %d × %d or %d × %d? Type the "
                     "greater product." % (a, b, c, e), big,
                     ["%d × %d = %d and %d × %d = %d."
                      % (a, b, a * b, c, e, c * e),
                      "The greater product is %d." % big])

    def io_mult():
        k = random.randint(3, 7)
        ins = sorted(random.sample(range(101, 320), 4))
        m = random.randrange(4)
        rows = [[i, i * k] for i in ins]
        return _ioq("This table multiplies each three-digit In number by %d. Type "
                    "the missing Out number." % k, rows, m, rows[m][1],
                    ["The rule is × %d." % k,
                     "%d × %d = %d." % (rows[m][0], k, rows[m][1])],
                    rule="× %d" % k)

    def two_step():
        c = random.randint(3, 9)
        n = random.randint(105, 240)
        return _numq("Work out %d × %d, then subtract %d." % (n, c, 100),
                     n * c - 100,
                     ["%d × %d = %d." % (n, c, n * c),
                      "%d − 100 = %d." % (n * c, n * c - 100)])

    def estimate():
        n = random.randint(196, 812)
        k = random.randint(3, 6)
        rounded = int(round(n / 100.0)) * 100
        return _numq("Estimate %d × %d by rounding %d to the nearest hundred "
                     "first. What is the estimate?" % (n, k, n), rounded * k,
                     ["%d rounded to the nearest hundred is %d." % (n, rounded),
                      "%d × %d = %d." % (rounded, k, rounded * k)])

    opts = [bare, bare, partial_products, word, money_word, price_table,
            measure_word, io_mult, hundreds_step]
    if d == 0:
        opts = [bare, partial_products, hundreds_step, word, money_word,
                price_table, io_mult]
    elif d == 2:
        opts = [bare, partial_products, missing_factor, missing_start, compare,
                two_step, estimate, word, price_table, measure_word]
    opts = opts + [price_table, io_mult, price_table]
    return pick(opts)()


@skill("Y4.4.d", "Divide a 2-digit number by a 1-digit number", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        b = random.randint(2, 4)
        k = random.randint(3, 9)
    elif d == 1:
        b = random.randint(3, 8)
        k = random.randint(4, 12)
    else:
        b = random.randint(4, 9)
        k = random.randint(7, 12)
    a = b * k

    def bare():
        return _numq("Work out %d ÷ %d." % (a, b), k,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (b, k, a, a, b, k)])

    def bare_other():
        return _numq("Work out %d ÷ %d." % (a, k), b,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (k, b, a, a, k, b)])

    def partition():
        tens = (a // 10) * 10
        while tens % b != 0 and tens > 0:
            tens -= 10
        rest = a - tens
        if tens == 0 or rest == 0 or rest % b != 0:
            return bare()
        return _numq("Divide by partitioning:  %d ÷ %d = (%d ÷ %d) + (%d ÷ %d) "
                     "= ___" % (a, b, tens, b, rest, b), k,
                     ["%d ÷ %d = %d and %d ÷ %d = %d."
                      % (tens, b, tens // b, rest, b, rest // b),
                      "%d + %d = %d." % (tens // b, rest // b, k)])

    def array_model():
        rows, cols = (b, k) if k <= 12 else (k, b)
        return _arrayq("%d counters are shared into %d equal rows. Build the "
                       "array, then type how many counters there are altogether."
                       % (a, rows), rows, cols,
                       ["%d ÷ %d = %d in each row." % (a, rows, cols),
                        "%d × %d = %d counters." % (rows, cols, a)])

    def equal_groups():
        g, p = min(b, 8), min(k, 10)
        return _egq("These equal groups show a division. %d counters are put into "
                    "equal groups of %d. How many equal groups are there?"
                    % (g * p, p), g, p, g,
                    ["Count the equal groups: %d." % g,
                     "%d ÷ %d = %d groups." % (g * p, p, g)])

    def word_share():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s shares %d %s equally between %d children. How many does "
                     "each child get?" % (who, a, thing, b), k,
                     ["%d ÷ %d = %d %s each." % (a, b, k, thing)], unit=thing)

    def word_group():
        thing = pick(_OBJ)
        return _numq("%d %s are put into bags of %d. How many bags are needed?"
                     % (a, thing, b), k,
                     ["%d ÷ %d = %d bags." % (a, b, k)], unit="bags")

    def missing():
        if random.random() < 0.5:
            return _numq("Find the missing number:  ___ ÷ %d = %d" % (b, k), a,
                         ["%d × %d = %d." % (b, k, a)])
        return _numq("Find the missing number:  %d ÷ ___ = %d" % (a, k), b,
                     ["%d ÷ %d = %d." % (a, k, b)])

    def inverse():
        return _numq("%d ÷ %d = ___ . Work it out, then check by multiplying."
                     % (a, b), k,
                     ["%d ÷ %d = %d." % (a, b, k),
                      "Check: %d × %d = %d ✓." % (k, b, a)])

    def strip_model():
        who = pick(NAMES)
        return _stripq("Use the strip model. %s shares %d marbles equally between "
                       "%d friends. How many marbles does each friend get?"
                       % (who, a, b), b, "?", str(a), "part", k,
                       ["The strip of %d is split into %d equal parts." % (a, b),
                        "%d ÷ %d = %d marbles each." % (a, b, k)])

    def io_div():
        kk = random.randint(2, 9)
        ins = sorted(random.sample([kk * m for m in range(2, 12)], 4))
        m = random.randrange(4)
        rows = [[i, i // kk] for i in ins]
        return _ioq("This table divides each In number by %d. Type the missing "
                    "Out number." % kk, rows, m, rows[m][1],
                    ["The rule is ÷ %d." % kk,
                     "%d ÷ %d = %d." % (rows[m][0], kk, rows[m][1])],
                    rule="÷ %d" % kk)

    def money_word():
        each = random.randint(4, 12)
        n = random.randint(3, 8)
        tot = each * n
        return _numq("%s is shared equally between %d children. How much does "
                     "each child get, in pence?" % (money(tot), n), each,
                     ["%d ÷ %d = %dp each." % (tot, n, each)], unit="p")

    def two_step():
        extra = random.randint(1, max(1, k - 1))
        return _numq("%d sweets are shared equally between %d children. One child "
                     "eats %d of them. How many sweets does that child have left?"
                     % (a, b, extra), k - extra,
                     ["%d ÷ %d = %d each." % (a, b, k),
                      "%d − %d = %d left." % (k, extra, k - extra)],
                     unit="sweets")

    opts = [bare, array_model, equal_groups, word_share, word_group, inverse,
            strip_model, io_div, money_word]
    if d == 0:
        opts = [bare, array_model, array_model, equal_groups, word_share,
                word_group, strip_model, io_div]
    elif d == 2:
        opts = [bare, bare_other, partition, missing, inverse, word_share,
                two_step, strip_model, io_div, money_word]
    opts = opts + [array_model, strip_model, equal_groups]
    return pick(opts)()


@skill("Y4.4.e", "Divide a 3-digit number by a 1-digit number", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        b = random.randint(2, 4)
        k = random.randint(31, 99)
    elif d == 1:
        b = random.randint(3, 6)
        k = random.randint(35, 160)
    else:
        b = random.randint(4, 9)
        k = random.randint(45, 190)
    a = b * k
    if a > 999:
        k = 999 // b
        a = b * k

    def bare():
        return _numq("Work out %d ÷ %d using short division." % (a, b), k,
                     ["%d × %d = %d, so %d ÷ %d = %d." % (b, k, a, a, b, k)])

    def partition():
        hund = (a // 100) * 100
        while hund > 0 and hund % b != 0:
            hund -= 100
        rest = a - hund
        if hund == 0 or rest == 0 or rest % b != 0:
            return bare()
        return _numq("Divide by partitioning:  %d ÷ %d = (%d ÷ %d) + (%d ÷ %d) "
                     "= ___" % (a, b, hund, b, rest, b), k,
                     ["%d ÷ %d = %d and %d ÷ %d = %d."
                      % (hund, b, hund // b, rest, b, rest // b),
                      "%d + %d = %d." % (hund // b, rest // b, k)])

    def first_step():
        h = a // 100
        if h < b:
            return bare()
        return _numq("Short division starts with the hundreds. In %d ÷ %d, how "
                     "many whole %ss are there in %s?"
                     % (a, b, b, _pl(h, "hundred")), h // b,
                     ["%d ÷ %d = %d remainder %d." % (h, b, h // b, h % b),
                      "So the first digit of the answer is %d." % (h // b)])

    def missing():
        if random.random() < 0.5:
            return _numq("Find the missing number:  ___ ÷ %d = %d" % (b, k), a,
                         ["%d × %d = %d." % (b, k, a)])
        return _numq("Find the missing number:  %d ÷ ___ = %d" % (a, k), b,
                     ["%d ÷ %d = %d." % (a, k, b)])

    def inverse():
        return _numq("%d ÷ %d = ___ . Work it out, then check by multiplying."
                     % (a, b), k,
                     ["%d ÷ %d = %d." % (a, b, k),
                      "Check: %d × %d = %d ✓." % (k, b, a)])

    def word_share():
        thing = pick(_OBJ)
        return _numq("%d %s are shared equally between %d classes. How many does "
                     "each class get?" % (a, thing, b), k,
                     ["%d ÷ %d = %d %s." % (a, b, k, thing)], unit=thing)

    def word_group():
        return _numq("%d chairs are put into rows of %d. How many rows are there?"
                     % (a, b), k,
                     ["%d ÷ %d = %d rows." % (a, b, k)], unit="rows")

    def money_word():
        n = random.randint(3, 8)
        each = random.randint(35, 120)
        tot = each * n
        return _numq("%s is shared equally between %d children. How much does "
                     "each child get, in pence?" % (money(tot), n), each,
                     ["%d ÷ %d = %dp each." % (tot, n, each)], unit="p")

    def measure_word():
        n = random.randint(3, 8)
        each = random.randint(40, 120)
        tot = each * n
        return _numq("A ribbon %d cm long is cut into %d equal pieces. How long is "
                     "each piece, in cm?" % (tot, n), each,
                     ["%d ÷ %d = %d cm." % (tot, n, each)], unit="cm")

    def strip_model():
        parts = min(b, 8)
        each = a // b
        return _stripq("Use the strip model. A strip worth %d is split into %d "
                       "equal parts. What is each part worth?" % (parts * each,
                                                                  parts),
                       parts, "?", str(parts * each), "part", each,
                       ["%d ÷ %d = %d." % (parts * each, parts, each)])

    def io_div():
        kk = random.randint(2, 8)
        ins = sorted(random.sample([kk * m for m in range(30, 120)], 4))
        m = random.randrange(4)
        rows = [[i, i // kk] for i in ins]
        return _ioq("This table divides each three-digit In number by %d. Type "
                    "the missing Out number." % kk, rows, m, rows[m][1],
                    ["The rule is ÷ %d." % kk,
                     "%d ÷ %d = %d." % (rows[m][0], kk, rows[m][1])],
                    rule="÷ %d" % kk)

    def bar_chart():
        cats = ["Year 3", "Year 4", "Year 5"]
        per = random.randint(20, 60)
        n = random.randint(3, 6)
        vals = [per * n, random.randint(60, 190), random.randint(60, 190)]
        return _barq("The chart shows how many stickers each year group collected. "
                     "The Year 3 stickers are shared equally between %d classes. "
                     "How many stickers does each Year 3 class get?" % n,
                     cats, vals, per,
                     ["Year 3 collected %d stickers." % (per * n),
                      "%d ÷ %d = %d stickers each." % (per * n, n, per)])

    def two_step():
        n = random.randint(2, 6)
        each = random.randint(40, 110)
        tot = each * n
        left = random.randint(5, 30)
        return _numq("%d apples are shared equally between %d shops. One shop "
                     "sells %d of its apples. How many apples does that shop have "
                     "left?" % (tot, n, left), each - left,
                     ["%d ÷ %d = %d apples each." % (tot, n, each),
                      "%d − %d = %d left." % (each, left, each - left)],
                     unit="apples")

    opts = [bare, bare, partition, word_share, word_group, money_word,
            measure_word, io_div, bar_chart, strip_model]
    if d == 0:
        opts = [bare, partition, first_step, word_share, word_group, io_div,
                strip_model, bar_chart]
    elif d == 2:
        opts = [bare, partition, first_step, missing, inverse, two_step,
                money_word, measure_word, io_div, bar_chart]
    opts = opts + [io_div, bar_chart, strip_model]
    return pick(opts)()


@skill("Y4.4.f", "Division with remainders", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        b = random.randint(3, 5)
        k = random.randint(3, 9)
    elif d == 1:
        b = random.randint(3, 8)
        k = random.randint(5, 14)
    else:
        b = random.randint(5, 9)
        k = random.randint(12, 30)
    r = random.randint(1, b - 1)
    a = b * k + r

    def remainder_only():
        return _numq("Work out %d ÷ %d. Type the remainder only." % (a, b), r,
                     ["%d × %d = %d." % (b, k, b * k),
                      "%d − %d = %d, so the remainder is %d."
                      % (a, b * k, r, r)], placeholder="the remainder")

    def quotient_only():
        return _numq("Work out %d ÷ %d. Type the whole-number part of the answer "
                     "(ignore the remainder)." % (a, b), k,
                     ["%d × %d = %d, with %d left over." % (b, k, b * k, r),
                      "The whole-number part is %d." % k],
                     placeholder="whole number part")

    def complete_sentence():
        return _numq("Complete the division:  %d ÷ %d = %d remainder ___"
                     % (a, b, k), r,
                     ["%d × %d = %d." % (b, k, b * k),
                      "%d − %d = %d." % (a, b * k, r)])

    def word_boxes():
        thing = pick(["eggs", "cakes", "apples", "pencils"])
        return _numq("%d %s are packed into boxes of %d. How many boxes can be "
                     "filled completely?" % (a, thing, b), k,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                      "Only full boxes count, so %d boxes." % k], unit="boxes")

    def word_left():
        thing = pick(["eggs", "cakes", "apples", "pencils"])
        return _numq("%d %s are packed into boxes of %d. How many %s are left "
                     "over?" % (a, thing, b, thing), r,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                      "%s %s left over." % (_pl(r, thing[:-1], thing), "is" if r == 1 else "are")], unit=thing)

    def word_round_up():
        return _numq("%d children go on a trip. Each minibus holds %d children. "
                     "How many minibuses are needed so that every child travels?"
                     % (a, b), k + 1,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                      "The %d left over still need a minibus, so %d minibuses "
                      "are needed." % (r, k + 1)], unit="minibuses")

    def word_more_needed():
        thing = pick(["eggs", "cakes", "buns"])
        return _numq("%d %s are packed into boxes of %d. How many more %s are "
                     "needed to fill one more box completely?" % (a, thing, b,
                                                                  thing),
                     b - r,
                     ["%d ÷ %d = %d remainder %d." % (a, b, k, r),
                      "%d − %d = %d more are needed." % (b, r, b - r)],
                     unit=thing)

    def word_share_left():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s shares %d %s equally between %d children. How many %s "
                     "does each child get?" % (who, a, thing, b, thing), k,
                     ["%d ÷ %d = %d each, with %d left over." % (a, b, k, r)],
                     unit=thing)

    def array_model():
        rows, cols = (b, k) if k <= 12 else (min(b, 10), min(k, 12))
        full = rows * cols
        return _arrayq("%d counters are shared equally into %d rows, with some "
                       "left over. Build only the full rows, then type how many "
                       "counters are in your array." % (full + r, rows),
                       rows, cols,
                       ["%d ÷ %d = %d in each row, remainder %d."
                        % (full + r, rows, cols, r),
                       "The full rows hold %d counters." % full])

    def equal_groups():
        g, p = min(b, 8), min(k, 10)
        rr = random.randint(1, g - 1) if g > 1 else 1
        return _egq("These equal groups show %d counters shared into %d equal "
                    "groups, with %s left over. How many counters were there "
                    "altogether?" % (g * p, g, _pl(rr, "counter")), g, p,
                    g * p + rr,
                    ["%d equal groups of %d is %d." % (g, p, g * p),
                     "%d + %d = %d counters." % (g * p, rr, g * p + rr)])

    def money_word():
        each = random.randint(3, 9)
        n = random.randint(3, 7)
        rem = random.randint(1, each - 1) if each > 1 else 1
        tot = each * n + rem
        return _numq("%s is shared equally between %d children, in whole pence. "
                     "How many pence are left over?" % (money(tot), n), rem,
                     ["%d ÷ %d = %d remainder %d." % (tot, n, each, rem),
                      "%dp is left over." % rem], unit="p")

    def missing_dividend():
        return _numq("Find the missing number:  ___ ÷ %d = %d remainder %d"
                     % (b, k, r), a,
                     ["%d × %d = %d." % (b, k, b * k),
                      "%d + %d = %d." % (b * k, r, a)])

    opts = [remainder_only, quotient_only, complete_sentence, word_boxes,
            word_left, word_round_up, array_model, equal_groups, money_word]
    if d == 0:
        opts = [remainder_only, quotient_only, complete_sentence, word_boxes,
                word_left, array_model, equal_groups, word_share_left]
    elif d == 2:
        opts = [remainder_only, quotient_only, word_round_up, word_more_needed,
                missing_dividend, money_word, array_model, word_boxes,
                word_share_left]
    opts = opts + [array_model, equal_groups, array_model]
    return pick(opts)()


@skill("Y4.4.g", "Multiplication word problems", S4)
def _(d=1):
    d = _t(d)
    n = _by_d(d, random.randint(2, 5), random.randint(3, 9), random.randint(4, 12))
    per = _by_d(d, random.randint(3, 8), random.randint(4, 12),
                random.randint(11, 32))

    def correspondence():
        who = pick(NAMES)
        return _numq("%s has %d hats and %d scarves. How many different hat and "
                     "scarf pairs can %s make?" % (who, n, per, who), n * per,
                     ["Each of the %d hats can go with each of the %d scarves."
                      % (n, per),
                      "%d × %d = %d pairs." % (n, per, n * per)], unit="pairs")

    def scaling():
        who = pick(NAMES)
        base = random.randint(6, 40)
        k = random.randint(3, 8)
        return _numq("A blue ribbon is %d cm long. A red ribbon is %d times as "
                     "long as the blue ribbon. How long is the red ribbon, in cm?"
                     % (base, k), base * k,
                     ["%d × %d = %d cm." % (base, k, base * k)], unit="cm")

    def comparison():
        a, b = _two_names()
        base = random.randint(5, 30)
        k = random.randint(3, 7)
        return _numq("%s has %d stickers. %s has %d times as many stickers as %s. "
                     "How many stickers do %s and %s have altogether?"
                     % (a, base, b, k, a, a, b), base + base * k,
                     ["%s has %d × %d = %d stickers." % (b, base, k, base * k),
                      "%d + %d = %d stickers altogether."
                      % (base, base * k, base + base * k)], unit="stickers")

    def rate():
        cost = random.randint(15, 95)
        m = random.randint(3, 9)
        return _numq("One balloon costs %s. How much do %d balloons cost, in "
                     "pence?" % (money(cost), m), cost * m,
                     ["%d × %d = %dp." % (cost, m, cost * m)], unit="p")

    def rows_of():
        rows = random.randint(6, 14)
        cols = random.randint(8, 20)
        return _numq("A hall has %d rows of chairs with %d chairs in each row. "
                     "How many chairs are there altogether?" % (rows, cols),
                     rows * cols,
                     ["%d × %d = %d chairs." % (rows, cols, rows * cols)],
                     unit="chairs")

    def area_model():
        rows = random.randint(3, 8)
        cols = random.randint(6, 14)
        return _agarea("A patio is made from square tiles. Use the area model to "
                       "work out how many tiles there are altogether.",
                       rows, cols,
                       ["The patio is %d rows of %d tiles." % (rows, cols),
                        "%d × %d = %d tiles." % (rows, cols, rows * cols)])

    def picto():
        key = pick([5, 10])
        cats = ["Class 4A", "Class 4B", "Class 4C"]
        vals = [key * random.randint(3, 9) for _ in cats]
        return _pictq("The pictogram shows how many books each class read. How "
                      "many books were read altogether?", cats, vals, key,
                      "book", sum(vals),
                      ["%s." % ", ".join("%s: %d" % (c, v)
                                         for c, v in zip(cats, vals)),
                       "%s = %d books." % (" + ".join(str(v) for v in vals),
                                           sum(vals))])

    def bar_chart():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(6, 24) for _ in cats]
        i = random.randrange(4)
        k = random.randint(3, 6)
        return _barq("The chart shows how many cakes were sold each day. Each "
                     "cake costs %dp. How much money was taken on %s, in pence?"
                     % (k, cats[i]), cats, vals, vals[i] * k,
                     ["%s: %d cakes." % (cats[i], vals[i]),
                      "%d × %d = %dp." % (vals[i], k, vals[i] * k)])

    def price_table():
        items = ["Pen", "Ruler", "Rubber", "Glue stick"]
        prices = random.sample(range(25, 180), 4)
        i = random.randrange(4)
        m = random.randint(3, 8)
        rows = [[items[j], money(prices[j])] for j in range(4)]
        return _dtq("Use the price list. How much do %d %ss cost altogether, in "
                    "pence?" % (m, items[i].lower()), ["Item", "Price"], rows,
                    prices[i] * m,
                    ["One %s costs %dp." % (items[i].lower(), prices[i]),
                     "%d × %d = %dp." % (prices[i], m, prices[i] * m)])

    def strip_model():
        who = pick(NAMES)
        return _stripq("Use the strip model. %s fills %d trays and each tray holds "
                       "%d buns. How many buns does %s bake altogether?"
                       % (who, n, per, who), n, str(per), "?", "total", n * per,
                       ["The strip shows %d equal parts of %d." % (n, per),
                        "%d × %d = %d buns." % (n, per, n * per)])

    def two_step():
        who = pick(NAMES)
        loose = random.randint(4, 30)
        return _numq("%s has %d %s each holding %d %s, and %d loose %s. How many "
                     "%s does %s have altogether?"
                     % (who, n, pick(_CONT), per, "beads", loose, "beads",
                        "beads", who), n * per + loose,
                     ["%d × %d = %d." % (n, per, n * per),
                      "%d + %d = %d beads." % (n * per, loose, n * per + loose)],
                     unit="beads")

    def times_as_many_measure():
        base = random.randint(15, 60)
        k = random.randint(3, 9)
        return _numq("A puppy has a mass of %d g. Its mother has a mass %d times "
                     "as great. What is the mass of the mother, in grams?"
                     % (base * 10, k), base * 10 * k,
                     ["%d × %d = %d g." % (base * 10, k, base * 10 * k)],
                     unit="g")

    opts = [correspondence, scaling, comparison, rate, rows_of, area_model,
            picto, bar_chart, price_table, strip_model]
    if d == 0:
        opts = [rate, rows_of, area_model, picto, strip_model, scaling,
                price_table, bar_chart]
    elif d == 2:
        opts = [correspondence, comparison, two_step, times_as_many_measure,
                price_table, bar_chart, scaling, rows_of, area_model]
    opts = opts + [area_model, picto, bar_chart]
    return pick(opts)()


@skill("Y4.4.h", "Division word problems", S4)
def _(d=1):
    d = _t(d)
    groups = _by_d(d, random.randint(2, 5), random.randint(3, 8),
                   random.randint(4, 9))
    per = _by_d(d, random.randint(3, 8), random.randint(4, 14),
                random.randint(12, 40))
    total = groups * per

    def sharing():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s shares %d %s equally between %d friends. How many %s "
                     "does each friend get?" % (who, total, thing, groups, thing),
                     per, ["%d ÷ %d = %d %s each." % (total, groups, per, thing)],
                     unit=thing)

    def grouping():
        thing = pick(_OBJ)
        return _numq("%d %s are packed into bags of %d. How many bags are filled?"
                     % (total, thing, per), groups,
                     ["%d ÷ %d = %d bags." % (total, per, groups)], unit="bags")

    def scaling_down():
        base = random.randint(4, 30)
        k = random.randint(3, 8)
        return _numq("A red ribbon is %d cm long. That is %d times as long as a "
                     "blue ribbon. How long is the blue ribbon, in cm?"
                     % (base * k, k), base,
                     ["%d ÷ %d = %d cm." % (base * k, k, base)], unit="cm")

    def comparison():
        a, b = _two_names()
        base = random.randint(4, 20)
        k = random.randint(3, 7)
        return _numq("%s has %d marbles. That is %d times as many marbles as %s "
                     "has. How many marbles does %s have?"
                     % (a, base * k, k, b, b), base,
                     ["%d ÷ %d = %d marbles." % (base * k, k, base)],
                     unit="marbles")

    def rate():
        each = random.randint(12, 60)
        m = random.randint(3, 8)
        return _numq("%d identical books cost %s in total. How much does one book "
                     "cost, in pence?" % (m, money(each * m)), each,
                     ["%d ÷ %d = %dp." % (each * m, m, each)], unit="p")

    def measure():
        each = random.randint(15, 90)
        m = random.randint(3, 8)
        return _numq("A plank of wood %d cm long is cut into %d equal pieces. How "
                     "long is each piece, in cm?" % (each * m, m), each,
                     ["%d ÷ %d = %d cm." % (each * m, m, each)], unit="cm")

    def bar_chart():
        cats = ["Apples", "Pears", "Plums"]
        vals = [total, random.randint(20, 90), random.randint(20, 90)]
        return _barq("The chart shows how much fruit was picked. The apples are "
                     "packed into bags of %d. How many bags of apples are there?"
                     % per, cats, vals, groups,
                     ["There are %d apples." % total,
                      "%d ÷ %d = %d bags." % (total, per, groups)])

    def picto():
        key = pick([5, 10])
        cats = ["Red", "Blue", "Green"]
        vals = [key * random.randint(3, 9) for _ in cats]
        n = pick([2, 3, 4, 5])
        while vals[0] % n:
            vals[0] += key
        return _pictq("The pictogram shows the counters in a box. The red counters "
                      "are shared equally between %d children. How many red "
                      "counters does each child get?" % n, cats, vals, key,
                      "counter", vals[0] // n,
                      ["There are %d red counters." % vals[0],
                       "%d ÷ %d = %d each." % (vals[0], n, vals[0] // n)])

    def strip_model():
        who = pick(NAMES)
        return _stripq("Use the strip model. %s shares %d conkers equally between "
                       "%d friends. How many conkers does each friend get?"
                       % (who, total, groups), groups, "?", str(total), "part",
                       per,
                       ["The strip of %d is split into %d equal parts."
                        % (total, groups),
                        "%d ÷ %d = %d conkers each." % (total, groups, per)])

    def equal_groups():
        g, p = min(groups, 8), min(per, 10)
        return _egq("Use the equal groups. %d shells are put into equal groups of "
                    "%d. How many equal groups are made?" % (g * p, p), g, p, g,
                    ["Count the equal groups: %d." % g,
                     "%d ÷ %d = %d groups." % (g * p, p, g)])

    def two_step():
        each = random.randint(6, 20)
        m = random.randint(3, 7)
        extra = random.randint(2, 9)
        return _numq("%d biscuits are shared equally between %d plates. Then %d "
                     "more biscuits are added to one plate. How many biscuits are "
                     "on that plate?" % (each * m, m, extra), each + extra,
                     ["%d ÷ %d = %d biscuits each." % (each * m, m, each),
                      "%d + %d = %d." % (each, extra, each + extra)],
                     unit="biscuits")

    def remainder_context():
        b = random.randint(3, 8)
        k = random.randint(4, 20)
        r = random.randint(1, b - 1)
        return _numq("%d children are put into teams of %d. How many complete "
                     "teams are there?" % (b * k + r, b), k,
                     ["%d ÷ %d = %d remainder %d." % (b * k + r, b, k, r),
                      "Only complete teams count, so %d teams." % k],
                     unit="teams")

    def money_table():
        items = ["Cinema", "Museum", "Zoo", "Aquarium"]
        n = random.randint(3, 8)
        eaches = random.sample(range(120, 460), 4)
        i = random.randrange(4)
        rows = [[items[j], money(eaches[j] * n)] for j in range(4)]
        return _dtq("This table shows the total cost for a group of %d children "
                    "at each place. How much does one child pay to visit the %s, "
                    "in pence?" % (n, items[i].lower()),
                    ["Place", "Total cost for %d" % n], rows, eaches[i],
                    ["The total for the %s is %dp." % (items[i].lower(),
                                                       eaches[i] * n),
                     "%d ÷ %d = %dp each." % (eaches[i] * n, n, eaches[i])])

    opts = [sharing, grouping, scaling_down, rate, measure, bar_chart, picto,
            strip_model, equal_groups, money_table]
    if d == 0:
        opts = [sharing, grouping, measure, bar_chart, picto, strip_model,
                equal_groups, rate]
    elif d == 2:
        opts = [scaling_down, comparison, rate, two_step, remainder_context,
                money_table, bar_chart, strip_model, measure]
    opts = opts + [bar_chart, strip_model, picto]
    return pick(opts)()


@skill("Y4.4.i", "Mixed and multi-step problems, order of operations", S4)
def _(d=1):
    d = _t(d)

    def brackets_first():
        a = random.randint(2, _by_d(d, 8, 12, 20))
        b = random.randint(2, _by_d(d, 8, 12, 20))
        c = random.randint(2, _by_d(d, 4, 6, 9))
        return _numq("Work out (%d + %d) × %d. Do the brackets first."
                     % (a, b, c), (a + b) * c,
                     ["%d + %d = %d." % (a, b, a + b),
                      "%d × %d = %d." % (a + b, c, (a + b) * c)])

    def no_brackets():
        a = random.randint(2, _by_d(d, 12, 30, 60))
        b = random.randint(2, _by_d(d, 6, 9, 12))
        c = random.randint(2, _by_d(d, 4, 7, 9))
        return _numq("Work out %d + %d × %d. Multiplication is done before "
                     "addition." % (a, b, c), a + b * c,
                     ["%d × %d = %d." % (b, c, b * c),
                      "%d + %d = %d." % (a, b * c, a + b * c)])

    def brackets_matter():
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        c = random.randint(2, 6)
        v1, v2 = (a + b) * c, a + b * c
        while v1 == v2:
            c = random.randint(2, 6)
            v1, v2 = (a + b) * c, a + b * c
        return _numq("Work out both (%d + %d) × %d and %d + %d × %d. Type the "
                     "larger answer." % (a, b, c, a, b, c), max(v1, v2),
                     ["(%d + %d) × %d = %d." % (a, b, c, v1),
                      "%d + %d × %d = %d, so the larger answer is %d."
                      % (a, b, c, v2, max(v1, v2))])

    def subtract_brackets():
        c = random.randint(2, _by_d(d, 4, 6, 9))
        b = random.randint(2, _by_d(d, 8, 12, 18))
        a = b + random.randint(2, _by_d(d, 8, 15, 25))
        return _numq("Work out (%d − %d) × %d. Do the brackets first."
                     % (a, b, c), (a - b) * c,
                     ["%d − %d = %d." % (a, b, a - b),
                      "%d × %d = %d." % (a - b, c, (a - b) * c)])

    def divide_brackets():
        c = random.randint(2, _by_d(d, 4, 6, 9))
        k = random.randint(2, _by_d(d, 6, 10, 12))
        a = random.randint(2, 20)
        tot = c * k
        b = tot - a
        if b < 1:
            a = random.randint(1, max(1, tot - 1))
            b = tot - a
        return _numq("Work out (%d + %d) ÷ %d. Do the brackets first."
                     % (a, b, c), tot // c,
                     ["%d + %d = %d." % (a, b, tot),
                      "%d ÷ %d = %d." % (tot, c, tot // c)])

    def missing_sign():
        while True:
            x = random.randint(2, _by_d(d, 9, 12, 20))
            y = random.randint(2, _by_d(d, 6, 9, 12))
            op = pick(["add", "subtract", "multiply", "divide"])
            vals = {"add": x + y, "subtract": x - y, "multiply": x * y,
                    "divide": x // y if y and x % y == 0 else None}
            target = vals[op]
            if target is None or target < 1:
                continue
            hits = [k for k, v in vals.items() if v == target]
            if len(hits) == 1:
                break
        return _wordq("Which operation makes this true?  %d ___ %d = %d.  Type "
                      "add, subtract, multiply or divide." % (x, y, target), op,
                      ["Try each operation: only one gives %d." % target,
                       "%d %s %d = %d." % (x, {"add": "+", "subtract": "−",
                                               "multiply": "×",
                                               "divide": "÷"}[op], y, target)],
                      placeholder="add / subtract / multiply / divide")

    def find_missing_sign():
        while True:
            x = random.randint(2, _by_d(d, 9, 12, 20))
            y = random.randint(2, _by_d(d, 6, 9, 12))
            op = pick(["add", "subtract", "multiply", "divide"])
            vals = {"add": x + y, "subtract": x - y, "multiply": x * y,
                    "divide": x // y if y and x % y == 0 else None}
            target = vals[op]
            if target is None or target < 1:
                continue
            if len([k for k, v in vals.items() if v == target]) == 1:
                break
        return _wordq("Find the missing sign in this numerical operation:  "
                      "%d ___ %d = %d.  Type add, subtract, multiply or divide "
                      "for the missing sign." % (x, y, target), op,
                      ["Only one sign makes the operation give %d." % target,
                       "%d %s %d = %d." % (x, {"add": "+", "subtract": "−",
                                               "multiply": "×",
                                               "divide": "÷"}[op], y, target)],
                      placeholder="add / subtract / multiply / divide")

    def balance():
        cands = []
        while not cands:
            a = random.randint(2, 9)
            b = random.randint(2, 12)
            cands = [k for k in range(2, 25)
                     if (a * b) % k == 0 and k != a and k != b
                     and (a * b) // k != k]
        c = pick(cands)
        return _numq("Balance the equation. Find the missing number:  "
                     "%d × %d = %d × ___" % (a, b, c), (a * b) // c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d ÷ %d = %d." % (a * b, c, (a * b) // c)])

    def two_step_word():
        who = pick(NAMES)
        n = random.randint(3, 9)
        per = random.randint(11, 40)
        spent = random.randint(5, 40)
        return _numq("%s buys %d packs of cards with %d cards in each pack, then "
                     "gives away %d cards. How many cards does %s have left?"
                     % (who, n, per, spent, who), n * per - spent,
                     ["%d × %d = %d cards." % (n, per, n * per),
                      "%d − %d = %s." % (n * per, spent, _pl(n * per - spent, "card"))],
                     unit="cards")

    def two_step_money():
        n = random.randint(2, 6)
        cost = random.randint(30, 140)
        paid = pick([p for p in (200, 300, 400, 500, 600, 800, 1000)
                     if p > n * cost] or [n * cost + 100])
        return _numq("%s buys %d pens at %s each and pays with %s. How much "
                     "change is given, in pence?"
                     % (pick(NAMES), n, money(cost), money(paid)),
                     paid - n * cost,
                     ["%d × %d = %dp spent." % (n, cost, n * cost),
                      "%d − %d = %dp change." % (paid, n * cost, paid - n * cost)],
                     unit="p")

    def missing_number_two_step():
        a = random.randint(2, 9)
        b = random.randint(3, 12)
        c = random.randint(5, 40)
        return _numq("Find the missing number:  %d × ___ + %d = %d"
                     % (a, c, a * b + c), b,
                     ["%d − %d = %d." % (a * b + c, c, a * b),
                      "%d ÷ %d = %d." % (a * b, a, b)])

    def chart_two_step():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(5, 20) for _ in cats]
        i, j = random.sample(range(4), 2)
        k = random.randint(2, 5)
        return _barq("The chart shows how many tickets were sold each day. Add "
                     "the %s and %s tickets, then multiply the total by %d. What "
                     "is the answer?" % (cats[i], cats[j], k), cats, vals,
                     (vals[i] + vals[j]) * k,
                     ["%s: %d and %s: %d." % (cats[i], vals[i], cats[j], vals[j]),
                      "(%d + %d) × %d = %d."
                      % (vals[i], vals[j], k, (vals[i] + vals[j]) * k)])

    def table_two_step():
        items = ["Juice", "Bun", "Apple", "Yoghurt"]
        prices = random.sample(range(20, 120), 4)
        i, j = random.sample(range(4), 2)
        rows = [[items[m], money(prices[m])] for m in range(4)]
        k = random.randint(2, 5)
        return _dtq("Use the price list. What is the total cost of %d %ss and one "
                    "%s, in pence?" % (k, items[i].lower(), items[j].lower()),
                    ["Item", "Price"], rows, prices[i] * k + prices[j],
                    ["%d × %d = %dp." % (prices[i], k, prices[i] * k),
                     "%d + %d = %dp." % (prices[i] * k, prices[j],
                                         prices[i] * k + prices[j])])

    def three_ops():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 20)
        return _numq("Work out %d × %d − %d. Multiplication is done before "
                     "subtraction." % (a, b, c), a * b - c,
                     ["%d × %d = %d." % (a, b, a * b),
                      "%d − %d = %d." % (a * b, c, a * b - c)]) \
            if a * b > c else _numq("Work out %d × %d + %d." % (a, b, c),
                                    a * b + c,
                                    ["%d × %d = %d." % (a, b, a * b),
                                     "%d + %d = %d." % (a * b, c, a * b + c)])

    opts = [brackets_first, no_brackets, subtract_brackets, divide_brackets,
            missing_sign, find_missing_sign, two_step_word, two_step_money,
            chart_two_step, table_two_step, three_ops]
    if d == 0:
        opts = [brackets_first, no_brackets, subtract_brackets, missing_sign,
                find_missing_sign, two_step_word, chart_two_step,
                table_two_step, three_ops]
    elif d == 2:
        opts = [brackets_matter, divide_brackets, missing_sign,
                find_missing_sign, balance, missing_number_two_step,
                two_step_money, two_step_word, chart_two_step, table_two_step]
    opts = opts + [chart_two_step, table_two_step, chart_two_step,
                   table_two_step]
    return pick(opts)()


@skill("Y4.4.j", "Numerical and simple variable expressions", S4)
def _(d=1):
    d = _t(d)
    var = pick(["n", "a", "b", "k", "m", "y"])

    def evaluate_add():
        v = random.randint(3, _by_d(d, 20, 60, 200))
        k = random.randint(4, _by_d(d, 20, 50, 150))
        return _numq("Evaluate the expression %s + %d when %s = %d."
                     % (var, k, var, v), v + k,
                     ["Replace %s with %d: %d + %d." % (var, v, v, k),
                      "%d + %d = %d." % (v, k, v + k)])

    def evaluate_sub():
        v = random.randint(_by_d(d, 12, 25, 60), _by_d(d, 30, 90, 300))
        k = random.randint(2, min(v - 1, _by_d(d, 10, 30, 90)))
        return _numq("Evaluate the expression %s − %d when %s = %d."
                     % (var, k, var, v), v - k,
                     ["Replace %s with %d: %d − %d." % (var, v, v, k),
                      "%d − %d = %d." % (v, k, v - k)])

    def evaluate_mult():
        v = random.randint(2, _by_d(d, 9, 12, 30))
        k = random.randint(2, _by_d(d, 6, 9, 12))
        return _numq("Evaluate the expression %d × %s when %s = %d."
                     % (k, var, var, v), k * v,
                     ["Replace %s with %d: %d × %d." % (var, v, k, v),
                      "%d × %d = %d." % (k, v, k * v)])

    def evaluate_two_step():
        v = random.randint(2, _by_d(d, 8, 12, 20))
        k = random.randint(2, _by_d(d, 5, 9, 12))
        c = random.randint(2, _by_d(d, 10, 25, 60))
        return _numq("Evaluate the expression %d × %s + %d when %s = %d."
                     % (k, var, c, var, v), k * v + c,
                     ["%d × %d = %d." % (k, v, k * v),
                      "%d + %d = %d." % (k * v, c, k * v + c)])

    def evaluate_brackets():
        v = random.randint(2, _by_d(d, 8, 12, 20))
        c = random.randint(2, _by_d(d, 8, 15, 30))
        k = random.randint(2, _by_d(d, 4, 6, 9))
        return _numq("Evaluate the expression (%s + %d) × %d when %s = %d."
                     % (var, c, k, var, v), (v + c) * k,
                     ["%d + %d = %d." % (v, c, v + c),
                      "%d × %d = %d." % (v + c, k, (v + c) * k)])

    def two_variables():
        v = random.randint(2, _by_d(d, 8, 12, 20))
        w = random.randint(2, _by_d(d, 8, 12, 20))
        return _numq("Evaluate the expression a × b when a = %d and b = %d."
                     % (v, w), v * w, ["%d × %d = %d." % (v, w, v * w)])

    def two_variables_mixed():
        v = random.randint(2, _by_d(d, 9, 12, 20))
        w = random.randint(2, _by_d(d, 9, 20, 40))
        return _numq("Evaluate the expression 3 × a + b when a = %d and b = %d."
                     % (v, w), 3 * v + w,
                     ["3 × %d = %d." % (v, 3 * v),
                      "%d + %d = %d." % (3 * v, w, 3 * v + w)])

    def write_slot_add():
        k = random.randint(3, 40)
        return _numq("A number %s is %d more than a number %s. The expression is "
                     "%s + ___ . Type the missing number."
                     % (var, k, var, var), k,
                     ["'%d more than %s' means add %d." % (k, var, k),
                      "The expression is %s + %d." % (var, k)])

    def write_slot_mult():
        k = random.randint(2, 12)
        return _numq("There are %d %s in each box. The expression for the number "
                     "in b boxes is b × ___ . Type the missing number."
                     % (k, "cakes"), k,
                     ["Each box holds %d cakes." % k,
                      "b boxes hold b × %d cakes." % k])

    def write_slot_var():
        k = random.randint(2, 12)
        return _wordq("A bag holds %s sweets. The expression for the number of "
                      "sweets in %d bags is %d × ___ . Type the missing letter."
                      % (var, k, k), var,
                      ["Each bag holds %s sweets." % var,
                       "%d bags hold %d × %s sweets." % (k, k, var)],
                      placeholder="a letter")

    def word_evaluate():
        who = pick(NAMES)
        k = random.randint(3, 12)
        v = random.randint(3, _by_d(d, 9, 15, 30))
        return _numq("A box holds %s pencils. %s has %d boxes, so %s has %d × %s "
                     "pencils. How many pencils does %s have when %s = %d?"
                     % (var, who, k, who, k, var, who, var, v), k * v,
                     ["Replace %s with %d: %d × %d." % (var, v, k, v),
                      "%d × %d = %d pencils." % (k, v, k * v)], unit="pencils")

    def variable_equation_word():
        who = pick(NAMES)
        per = random.randint(3, _by_d(d, 8, 12, 20))
        k = random.randint(2, _by_d(d, 5, 9, 12))
        return _numq("Write a variable equation to represent this word problem, "
                     "then use it to answer. %s fills %d boxes with the same "
                     "number of pencils and uses %d pencils in total. The letter "
                     "%s stands for the number of pencils in one box. What is "
                     "the value of %s?" % (who, k, per * k, var, var), per,
                     ["The equation for the word problem is %d × %s = %d."
                      % (k, var, per * k),
                      "%d ÷ %d = %d, so %s = %d."
                      % (per * k, k, per, var, per)])

    def variable_equation_add():
        who = pick(NAMES)
        start = random.randint(5, _by_d(d, 30, 80, 200))
        extra = random.randint(3, _by_d(d, 20, 50, 120))
        return _numq("Write a variable equation to represent this word problem, "
                     "then use it to answer. %s starts with %s stickers, is "
                     "given %d more stickers, and then has %d stickers "
                     "altogether. What is the value of %s?"
                     % (who, var, extra, start + extra, var), start,
                     ["The equation for the word problem is %s + %d = %d."
                      % (var, extra, start + extra),
                      "%d − %d = %d, so %s = %d."
                      % (start + extra, extra, start, var, start)],
                     unit="stickers")

    def solve_for_var():
        v = random.randint(3, _by_d(d, 20, 40, 90))
        k = random.randint(3, _by_d(d, 15, 40, 80))
        return _numq("Find the value of %s:  %s + %d = %d." % (var, var, k, v + k),
                     v, ["Use the inverse: %d − %d = %d." % (v + k, k, v)])

    def solve_for_var_mult():
        v = random.randint(2, _by_d(d, 8, 12, 20))
        k = random.randint(2, _by_d(d, 6, 9, 12))
        return _numq("Find the value of %s:  %d × %s = %d." % (var, k, var, k * v),
                     v, ["Use the inverse: %d ÷ %d = %d." % (k * v, k, v)])

    def io_expression():
        k = random.randint(2, 9)
        c = random.randint(1, 20)
        ins = sorted(random.sample(range(2, 25), 4))
        rows = [[i, k * i + c] for i in ins]
        m = random.randrange(4)
        return _ioq("Every Out number is worked out from the In number using the "
                    "expression %d × In + %d. Type the missing Out number."
                    % (k, c), rows, m, rows[m][1],
                    ["%d × %d = %d." % (k, rows[m][0], k * rows[m][0]),
                     "%d + %d = %d." % (k * rows[m][0], c, rows[m][1])],
                    rule="× %d + %d" % (k, c))

    def table_evaluate():
        k = random.randint(2, 9)
        vals = sorted(random.sample(range(2, 20), 3))
        i = random.randrange(3)
        rows = [[str(v), str(k * v) if j != i else ""]
                for j, v in enumerate(vals)]
        return _dtq("This table shows the value of the expression %d × %s for "
                    "different values of %s. What is the missing value?"
                    % (k, var, var), [var, "%d × %s" % (k, var)], rows,
                    k * vals[i],
                    ["When %s = %d, the expression is %d × %d."
                     % (var, vals[i], k, vals[i]),
                     "%d × %d = %d." % (k, vals[i], k * vals[i])],
                    missing=(i, 1))

    opts = [evaluate_add, evaluate_sub, evaluate_mult, evaluate_two_step,
            two_variables, write_slot_add, write_slot_mult, word_evaluate,
            variable_equation_word, variable_equation_add, io_expression,
            table_evaluate, solve_for_var]
    if d == 0:
        opts = [evaluate_add, evaluate_sub, evaluate_mult, write_slot_add,
                write_slot_mult, word_evaluate, variable_equation_word,
                variable_equation_add, io_expression, table_evaluate]
    elif d == 2:
        opts = [evaluate_two_step, evaluate_brackets, two_variables,
                two_variables_mixed, write_slot_var, solve_for_var,
                solve_for_var_mult, variable_equation_word,
                variable_equation_add, io_expression, table_evaluate,
                word_evaluate]
    opts = opts + [io_expression, table_evaluate, table_evaluate,
                   io_expression]
    return pick(opts)()


# ================================================================== 4.5 ======
def _dens(d):
    return _by_d(d, [2, 3, 4, 5], [3, 4, 5, 6, 8, 10], [5, 6, 7, 8, 9, 10, 12])


@skill("Y4.5.a", "Fractions as equal parts of a whole or a set", S5)
def _(d=1):
    d = _t(d)
    den = pick(_dens(d))
    n = 1 if d == 0 and random.random() < 0.5 else random.randint(1, den - 1)

    def shade_bar():
        return _fbq("Shade %d/%d of the bar." % (n, den), den, n,
                    ["The bar is split into %d equal parts." % den,
                     "Shade %d of them to show %d/%d." % (n, n, den)])

    def shade_bar_words():
        food = pick(["chocolate bar", "loaf of bread", "ribbon", "cake"])
        return _fbq("A %s is cut into %d equal pieces. Shade %s of it."
                    % (food, den, _frac_words(n, den)), den, n,
                    ["%s means %d out of %d equal parts."
                     % (_frac_words(n, den).capitalize(), n, den),
                     "Shade %s." % _pl(n, "part")])

    def fraction_bars():
        return _fbq("Understand fractions with fraction bars. This fraction bar "
                    "is one whole split into %d equal parts. Shade the fraction "
                    "bar to show %d/%d." % (den, n, den), den, n,
                    ["A fraction bar shows the whole split into equal parts.",
                     "Shade %d of the %d parts to show %d/%d."
                     % (n, den, n, den)])

    def fraction_bars_words():
        return _fbq("Understand fractions with fraction bars. Shade this "
                    "fraction bar of %d equal parts to show %s."
                    % (den, _frac_words(n, den)), den, n,
                    ["%s means %d of the %d equal parts of the bar."
                     % (_frac_words(n, den).capitalize(), n, den),
                     "Shade %s." % _pl(n, "part")])

    def shade_area():
        parts = pick([4, 6, 8, 9, 10, 12])
        k = random.randint(1, parts - 1)
        return _agshade("This area model is one whole split into %d equal parts. "
                        "Shade it to show %d/%d." % (parts, k, parts), parts, k,
                        ["The area model has %d equal parts." % parts,
                         "Shade %s." % _pl(k, "part")])

    def read_area():
        parts = pick([4, 6, 8, 9, 10, 12])
        k = random.randint(1, parts - 1)
        return _agread("Write the fraction of this area model that is shaded.",
                       parts, k,
                       ["The model has %d equal parts and %s shaded."
                        % (parts, _pl(k, "part")),
                        "The fraction shaded is %d/%d." % (k, parts)],
                       placeholder="e.g. 3/4")

    def shade_left():
        eaten = random.randint(1, den - 1)
        return _fbq("A pizza is cut into %d equal slices and %d %s eaten. Shade "
                    "the fraction that is left."
                    % (den, eaten, "is" if eaten == 1 else "are"), den,
                    den - eaten,
                    ["%d − %d = %s left." % (den, eaten, _pl(den - eaten,
                                                             "slice")),
                     "That is %d/%d." % (den - eaten, den)])

    def set_fraction():
        per = random.randint(1, 4)
        tot = den * per
        col = pick(["red", "blue", "green", "yellow"])
        return _fracq("A bag holds %d marbles. %d of them are %s. What fraction "
                      "of the marbles are %s?" % (tot, per * n, col, col),
                      per * n, tot,
                      ["%d out of %d marbles are %s." % (per * n, tot, col),
                       "The fraction is %d/%d." % (per * n, tot)])

    def set_groups():
        per = random.randint(2, 6)
        tot = den * per
        return _fracq("%d counters are shared equally into %d groups. What "
                      "fraction of the counters is one group?" % (tot, den),
                      1, den,
                      ["Each group is one of %d equal groups." % den,
                       "That is 1/%d of the counters." % den])

    def write_fraction():
        return _fracq("A shape is split into %d equal parts and %d %s shaded. "
                      "Write the fraction that is shaded."
                      % (den, n, "part is" if n == 1 else "parts are"), n, den,
                      ["%d shaded out of %d equal parts." % (n, den),
                       "The fraction is %d/%d." % (n, den)])

    def count_parts():
        per = 2 if den * 2 <= 12 else 1
        parts = den * per
        return _numq("A bar is split into %d equal parts. %s of the bar is "
                     "shaded. How many parts are shaded?"
                     % (parts, _frac_words(n, den).capitalize()), n * per,
                     ["%d ÷ %d = %s in each %s."
                      % (parts, den, _pl(per, "part"),
                         _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %s shaded." % (per, n, _pl(n * per, "part"))],
                     unit="parts")

    def fraction_of_set_count():
        per = random.randint(2, 6)
        tot = den * per
        thing = pick(_OBJ)
        return _numq("%s has %d %s and puts them into %d equal groups. How many "
                     "%s are in each group?" % (pick(NAMES), tot, thing, den,
                                                thing), per,
                     ["%d ÷ %d = %d." % (tot, den, per),
                      "Each group is 1/%d of the %s." % (den, thing)],
                     unit=thing)

    def not_shaded():
        return _fracq("A strip has %d equal parts and %d %s NOT shaded. Write the "
                      "fraction that IS shaded."
                      % (den, den - n, "part is" if den - n == 1
                         else "parts are"), n, den,
                      ["%d − %d = %s shaded." % (den, den - n, _pl(n, "part")),
                       "That is %d/%d." % (n, den)])

    opts = [shade_bar, shade_bar_words, fraction_bars, fraction_bars_words,
            shade_area, read_area, shade_left, set_fraction, write_fraction,
            set_groups, fraction_of_set_count]
    if d == 0:
        opts = [shade_bar, shade_bar_words, fraction_bars, fraction_bars_words,
                shade_area, read_area, shade_left, write_fraction, set_groups,
                fraction_of_set_count]
    elif d == 2:
        opts = [shade_area, read_area, fraction_bars, fraction_bars_words,
                set_fraction, write_fraction, not_shaded, count_parts,
                shade_left, fraction_of_set_count, shade_bar]
    opts = opts + [shade_area, read_area]
    return pick(opts)()


@skill("Y4.5.b", "Proper fractions, including hundredths", S5)
def _(d=1):
    d = _t(d)

    def read_hundredths():
        k = pick([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90]) if d < 2 \
            else random.randint(11, 89)
        return _agread("This hundred square is one whole. Write the fraction of "
                       "the hundred square that is shaded. Use hundredths.",
                       100, k,
                       ["The square has 100 equal parts.",
                        "%s are shaded, so the fraction is %d/100."
                        % (_pl(k, "part"), k)],
                       placeholder="e.g. 37/100")

    def shade_hundredths():
        k = pick([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        return _agshade("This area model is one whole split into 100 equal parts. "
                        "Shade it to show %d/100." % k, 100, k,
                        ["Each small square is one hundredth.",
                         "Shade %d of the 100 squares." % k])

    def tenths_to_hundredths():
        n = random.randint(1, 9)
        return _numq("Complete:  %d/10 = ___/100" % n, n * 10,
                     ["One tenth is the same as ten hundredths.",
                      "%d × 10 = %d, so %d/10 = %d/100." % (n, n * 10, n,
                                                            n * 10)])

    def hundredths_to_tenths():
        n = random.randint(1, 9)
        return _numq("Complete:  %d/100 = ___/10" % (n * 10), n,
                     ["Ten hundredths make one tenth.",
                      "%d ÷ 10 = %d, so %d/100 = %d/10." % (n * 10, n, n * 10,
                                                            n)])

    def make_a_whole():
        k = pick([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        return _numq("How many more hundredths are needed to make %d/100 up to "
                     "1 whole?" % k, 100 - k,
                     ["1 whole = 100/100.",
                      "100 − %d = %d hundredths." % (k, 100 - k)],
                     unit="hundredths")

    def denominator_vocab():
        n = random.randint(1, 99)
        if random.random() < 0.5:
            return _numq("In the fraction %d/100, what is the denominator?" % n,
                         100,
                         ["The denominator is the bottom number of a fraction.",
                          "In %d/100 the denominator is 100." % n])
        return _numq("In the fraction %d/100, what is the numerator?" % n, n,
                     ["The numerator is the top number of a fraction.",
                      "In %d/100 the numerator is %d." % (n, n)])

    def proper_choice():
        den = pick([4, 5, 6, 8, 10])
        prop = random.randint(1, den - 1)
        imp = den + random.randint(1, 4)
        if random.random() < 0.5:
            labels, k = ["%d/%d" % (prop, den), "%d/%d" % (imp, den)], "A"
        else:
            labels, k = ["%d/%d" % (imp, den), "%d/%d" % (prop, den)], "B"
        return _wordq("A proper fraction is less than 1 whole. Which of these is "
                      "a proper fraction? A: %s   B: %s.  Type A or B."
                      % (labels[0], labels[1]), k,
                      ["A proper fraction has a numerator smaller than its "
                       "denominator.",
                       "%d/%d is less than 1 whole, so the answer is %s."
                       % (prop, den, k)], placeholder="A or B")

    def word_hundredths():
        who = pick(NAMES)
        k = pick([15, 20, 25, 35, 40, 45, 60, 70, 80])
        return _fracq("A pack of 100 stickers is shared out. %s takes %d of the "
                      "stickers. What fraction of the pack does %s take? Use "
                      "hundredths." % (who, k, who), k, 100,
                      ["%d out of 100 stickers." % k,
                       "The fraction is %d/100." % k],
                      placeholder="e.g. 37/100")

    def tenths_bar():
        n = random.randint(1, 9)
        return _fbq("This bar is one whole split into tenths. Shade %s."
                    % _pl(n, "tenth"), 10, n,
                    ["Shade %d of the 10 equal parts." % n,
                     "That is %d/10." % n])

    def proper_from_parts():
        den = pick([6, 8, 9, 10, 12, 100])
        num = random.randint(1, den - 1)
        return _fracq("A shape is split into %d equal parts and %s are shaded. "
                      "Write the proper fraction that is shaded."
                      % (den, _pl(num, "part")), num, den,
                      ["%d shaded out of %d equal parts." % (num, den),
                       "The fraction is %d/%d, which is less than 1 whole."
                       % (num, den)])

    def compare_to_whole():
        den = pick([5, 6, 8, 10, 100])
        num = random.randint(1, den - 1)
        return _numq("How many more %ss are needed to make %d/%d up to 1 whole?"
                     % (_FRAC_WORDS.get(den, "part"), num, den), den - num,
                     ["1 whole = %d/%d." % (den, den),
                      "%d − %d = %d." % (den, num, den - num)])

    opts = [read_hundredths, shade_hundredths, tenths_to_hundredths,
            hundredths_to_tenths, make_a_whole, word_hundredths, tenths_bar,
            proper_from_parts, denominator_vocab]
    if d == 0:
        opts = [read_hundredths, shade_hundredths, tenths_to_hundredths,
                tenths_bar, proper_from_parts, denominator_vocab,
                word_hundredths]
    elif d == 2:
        opts = [read_hundredths, hundredths_to_tenths, tenths_to_hundredths,
                make_a_whole, proper_choice, compare_to_whole, word_hundredths,
                proper_from_parts, shade_hundredths]
    opts = opts + [read_hundredths, shade_hundredths, tenths_bar]
    return pick(opts)()


@skill("Y4.5.c", "Fractions on a number line", S5)
def _(d=1):
    d = _t(d)
    term = _by_d(d, [2, 4, 5], [2, 4, 5, 10], [4, 5, 8, 10])

    def place_unit():
        den = pick(term)
        return _nlq("Place 1/%d on the number line." % den, 1.0 / den, 0, 1,
                    1.0 / den, 1.0 / den,
                    ["The line from 0 to 1 is split into %d equal steps." % den,
                     "1/%d is the first step from 0." % den])

    def place_proper():
        den = pick(term)
        n = random.randint(1, den - 1)
        return _nlq("Place %d/%d on the number line." % (n, den),
                    n / float(den), 0, 1, 1.0 / den, 1.0 / den,
                    ["Each step on the line is 1/%d." % den,
                     "Count %s from 0." % _pl(n, "step")])

    def unit_fraction_line():
        den = pick(term)
        return _nlq("Fractions of number lines: unit fractions. This number line "
                    "from 0 to 1 is split into %d equal parts. Place the unit "
                    "fraction 1/%d on the number line." % (den, den),
                    1.0 / den, 0, 1, 1.0 / den, 1.0 / den,
                    ["A unit fraction has 1 as its numerator.",
                     "1/%d is the first mark after 0 on the number line." % den])

    def unit_fraction_line_words():
        den = pick(term)
        return _nlq("Unit fractions on number lines: place %s on this number "
                    "line, which runs from 0 to 1 in steps of 1/%d."
                    % (_frac_words(1, den), den), 1.0 / den, 0, 1, 1.0 / den,
                    1.0 / den,
                    ["%s is written 1/%d." % (_frac_words(1, den).capitalize(),
                                              den),
                     "It is one step of 1/%d from 0." % den])

    def identify_on_line():
        den = pick(term)
        n = random.randint(1, den - 1)
        return _nlq("Identify fractions on number lines. This number line from 0 "
                    "to 1 is split into %d equal steps. Identify where %d/%d is "
                    "and place the marker there." % (den, n, den),
                    n / float(den), 0, 1, 1.0 / den, 1.0 / den,
                    ["Each step on the number line is 1/%d." % den,
                     "%d/%d is %s from 0." % (n, den, _pl(n, "step"))])

    def place_tenths():
        n = random.randint(1, _by_d(d, 9, 14, 19))
        return _nlq("Place %d/10 on the number line." % n, n / 10.0, 0, 2, 0.1,
                    0.5,
                    ["Each small step on the line is one tenth.",
                     "Count %s from 0." % _pl(n, "step")], tol=0.05)

    def place_improper():
        den = pick([2, 4, 5])
        n = random.randint(den + 1, den * 2 - 1)
        return _nlq("Place %d/%d on the number line. It is greater than 1 whole."
                    % (n, den), n / float(den), 0, 2, 1.0 / den, 1.0,
                    ["Each step is 1/%d, and %d/%d is one whole."
                     % (den, den, den),
                     "Count %d steps from 0." % n])

    def place_equivalent():
        line_den = pick([4, 8, 10])
        eq = pick([(1, 2), (1, 4), (3, 4)]) if line_den in (4, 8) \
            else pick([(1, 2), (1, 5), (2, 5)])
        en, ed = eq
        return _nlq("The line from 0 to 1 is split into %d equal steps. Place %s "
                    "on the line." % (line_den, _frac_words(en, ed)),
                    en / float(ed), 0, 1, 1.0 / line_den, 1.0 / line_den,
                    ["%s = %d/%d." % (_frac_words(en, ed).capitalize(),
                                      en * line_den // ed, line_den),
                     "Count %d steps from 0." % (en * line_den // ed)])

    def graph_larger():
        den = pick([4, 5, 8, 10])
        a, b = random.sample(range(1, den), 2)
        larger = random.random() < 0.5
        k = max(a, b) if larger else min(a, b)
        word = "larger" if larger else "smaller"
        return _nlq("Which fraction is %s, %d/%d or %d/%d? Place the %s fraction "
                    "on the number line." % (word, a, den, b, den, word),
                    k / float(den), 0, 1, 1.0 / den, 1.0 / den,
                    ["The denominators match, so compare the numerators.",
                     "The %s fraction is %d/%d." % (word, k, den)])

    def identify_mark():
        den = pick(_dens(d))
        n = random.randint(1, den - 1)
        return _fracq("A number line from 0 to 1 is split into %d equal parts. "
                      "Which fraction is at the %s mark from 0?"
                      % (den, _ord(n)), n, den,
                      ["Each part is 1/%d." % den,
                       "The %s mark is %d/%d." % (_ord(n), n, den)])

    def next_step():
        den = pick([x for x in _dens(d) if x >= 3])   # need room before the last mark
        n = random.randint(1, den - 2)
        return _fracq("A number line is marked in %ss. A point is at %d/%d. Which "
                      "fraction is at the next mark to the right?"
                      % (_FRAC_WORDS.get(den, "part"), n, den), n + 1, den,
                      ["One step to the right adds 1/%d." % den,
                       "%d/%d + 1/%d = %d/%d." % (n, den, den, n + 1, den)])

    def halfway():
        den = pick([4, 6, 8, 10, 12])
        return _fracq("A number line runs from 0 to 1 and is split into %d equal "
                      "steps. Which fraction is exactly halfway along the line?"
                      % den, den // 2, den,
                      ["Halfway is %d of the %d steps." % (den // 2, den),
                       "That is %d/%d, which is one half." % (den // 2, den)])

    def word_line():
        den = pick(term)
        n = random.randint(1, den - 1)
        who = pick(NAMES)
        return _nlq("%s runs along a track that is marked in %ss of the way. %s "
                    "stops after %d/%d of the track. Place that point on the "
                    "number line, where 1 stands for the whole track."
                    % (who, _FRAC_WORDS.get(den, "part"), who, n, den),
                    n / float(den), 0, 1, 1.0 / den, 1.0 / den,
                    ["The whole track is 1 on the line.",
                     "%d/%d is %s from 0." % (n, den, _pl(n, "step"))])

    opts = [place_unit, place_proper, place_proper, unit_fraction_line,
            unit_fraction_line_words, identify_on_line, place_tenths,
            place_equivalent, graph_larger, identify_mark, next_step]
    if d == 0:
        opts = [place_unit, place_proper, unit_fraction_line,
                unit_fraction_line_words, identify_on_line, place_tenths,
                identify_mark, next_step, halfway, place_equivalent]
    elif d == 2:
        opts = [place_proper, place_tenths, place_improper, place_equivalent,
                unit_fraction_line, identify_on_line, graph_larger,
                identify_mark, next_step, word_line]
    return pick(opts)()


@skill("Y4.5.d", "Count up and down in tenths and hundredths", S5)
def _(d=1):
    d = _t(d)

    def next_tenth():
        n = random.randint(1, 8)
        return _fracq("Count on in tenths:  %d/10, ___ . Write the next fraction."
                      % n, n + 1, 10,
                      ["One tenth more than %d/10 is %d/10." % (n, n + 1)],
                      placeholder="e.g. 4/10")

    def back_tenth():
        n = random.randint(2, 10)
        return _fracq("Count back in tenths:  %d/10, ___ . Write the next "
                      "fraction." % n, n - 1, 10,
                      ["One tenth less than %d/10 is %d/10." % (n, n - 1)],
                      placeholder="e.g. 4/10")

    def next_hundredth():
        n = random.randint(_by_d(d, 1, 20, 60), _by_d(d, 20, 70, 98))
        return _fracq("Count on in hundredths:  %d/100, ___ . Write the next "
                      "fraction." % n, n + 1, 100,
                      ["One hundredth more than %d/100 is %d/100." % (n, n + 1)],
                      placeholder="e.g. 47/100")

    def back_hundredth():
        n = random.randint(_by_d(d, 3, 20, 60), _by_d(d, 25, 80, 99))
        return _fracq("Count back in hundredths:  %d/100, ___ . Write the next "
                      "fraction." % n, n - 1, 100,
                      ["One hundredth less than %d/100 is %d/100." % (n, n - 1)],
                      placeholder="e.g. 47/100")

    def sequence_tenths():
        step = _by_d(d, 2, 2, 3)
        start = random.randint(1, max(1, 10 - 3 * step))
        seq = [start + i * step for i in range(3)]
        return _fracq("What comes next?  %s, ___"
                      % ", ".join("%d/10" % v for v in seq),
                      seq[-1] + step, 10,
                      ["The count goes up in %s each time." % _pl(step, "tenth"),
                       "%d/10 + %d/10 = %d/10." % (seq[-1], step,
                                                   seq[-1] + step)],
                      placeholder="e.g. 7/10")

    def sequence_hundredths():
        step = pick([5, 10, 20, 25])
        start = pick([step, step * 2])
        seq = [start + i * step for i in range(3)]
        return _fracq("What comes next?  %s, ___"
                      % ", ".join("%d/100" % v for v in seq),
                      seq[-1] + step, 100,
                      ["The count goes up in %s each time."
                       % _pl(step, "hundredth"),
                       "%d/100 + %d/100 = %d/100." % (seq[-1], step,
                                                      seq[-1] + step)],
                      placeholder="e.g. 45/100")

    def cross_the_whole():
        n = random.randint(7, 9)
        return _fracq("Count on in tenths past 1 whole:  %d/10, %d/10, ___ . "
                      "Write the next fraction." % (n, n + 1), n + 2, 10,
                      ["10/10 is 1 whole, and the count carries on.",
                       "%d/10 + 1/10 = %d/10." % (n + 1, n + 2)],
                      placeholder="e.g. 11/10")

    def how_many_to_whole():
        n = random.randint(1, 9)
        return _numq("How many more tenths are needed to make %d/10 up to 1 "
                     "whole?" % n, 10 - n,
                     ["1 whole = 10/10.",
                      "10 − %d = %s." % (n, _pl(10 - n, "tenth"))],
                     unit="tenths")

    def count_steps():
        who = pick(NAMES)
        start = random.randint(1, 5)
        steps = random.randint(2, 5)
        return _fracq("%s starts at %d/10 and counts on %s in tenths. Where does "
                      "%s stop?" % (who, start, _pl(steps, "step"), who),
                      start + steps, 10,
                      ["%d steps of 1/10 is %d/10." % (steps, steps),
                       "%d/10 + %d/10 = %d/10." % (start, steps, start + steps)],
                      placeholder="e.g. 7/10")

    def line_tenths():
        n = random.randint(1, _by_d(d, 9, 14, 19))
        return _nlq("Count in tenths and place %d/10 on the number line." % n,
                    n / 10.0, 0, 2, 0.1, 0.5,
                    ["Each step on the line is one tenth.",
                     "Count %s from 0." % _pl(n, "tenth")], tol=0.05)

    def bar_tenths():
        n = random.randint(1, 9)
        return _fbq("This bar is one whole split into tenths. Count in tenths and "
                    "shade %s." % _pl(n, "tenth"), 10, n,
                    ["Each part of the bar is one tenth.",
                     "Shade %d parts to show %d/10." % (n, n)])

    def hundredths_grid():
        k = pick([5, 10, 15, 20, 25, 30, 40, 50])
        step = pick([5, 10])
        return _agread("This hundred square shows a fraction in hundredths. Count "
                       "on %s from the shaded fraction. Which fraction do you "
                       "reach?" % _pl(step, "hundredth"), 100, k,
                       ["The shaded fraction is %d/100." % k,
                        "%d/100 + %d/100 = %d/100." % (k, step, k + step)],
                       answer="%d/100" % (k + step), placeholder="e.g. 45/100")

    def decimal_tenths():
        start = random.randint(_by_d(d, 4, 5, 12), _by_d(d, 6, 17, 27))
        up = random.random() < 0.6
        seq = [start + (i if up else -i) for i in range(3)]
        nxt = seq[-1] + (1 if up else -1)

        def f1(v):
            return ("%.1f" % (v / 10.0)).rstrip("0").rstrip(".")
        return _numq("Count %s in steps of 0.1:  %s, ___" % ("on" if up else "back", ", ".join(f1(v) for v in seq)), f1(nxt),
                     ["Each step is one tenth.", "%s %s 0.1 = %s." % (f1(seq[-1]), "+" if up else "−", f1(nxt))],
                     answer_type="num", placeholder="e.g. 1.4")

    def decimal_hundredths():
        start = random.randint(12, 95)
        up = random.random() < 0.5
        seq = [start + (i if up else -i) for i in range(3)]
        nxt = seq[-1] + (1 if up else -1)
        return _numq("Count %s in steps of 0.01:  %s, ___" % ("on" if up else "back", ", ".join("%.2f" % (v / 100.0) for v in seq)),
                     ("%.2f" % (nxt / 100.0)).rstrip("0").rstrip("."),
                     ["Each step is one hundredth.", "The next number is %.2f." % (nxt / 100.0)],
                     answer_type="num", placeholder="e.g. 0.46")

    def tenth_in_hundredths():
        n = random.randint(1, 89)
        return _fracq("Start at %d/100 and count on 1 tenth. Which fraction do you reach?" % n, n + 10, 100,
                      ["1 tenth = 10/100.", "%d/100 + 10/100 = %d/100." % (n, n + 10)], placeholder="e.g. 45/100")

    def missing_middle():
        n = random.randint(1, 7)
        return _fracq("Fill the gap in the count:  %d/10, ___, %d/10" % (n, n + 2), n + 1, 10,
                      ["The count goes up in tenths.", "The missing fraction is %d/10." % (n + 1)], placeholder="e.g. 4/10")

    opts = [next_tenth, back_tenth, next_hundredth, back_hundredth,
            sequence_tenths, line_tenths, bar_tenths, how_many_to_whole,
            count_steps, decimal_tenths, tenth_in_hundredths, missing_middle]
    if d == 0:
        opts = [next_tenth, back_tenth, sequence_tenths, line_tenths,
                bar_tenths, how_many_to_whole, count_steps, decimal_tenths, missing_middle]
    elif d == 2:
        opts = [next_hundredth, back_hundredth, sequence_hundredths,
                cross_the_whole, hundredths_grid, line_tenths, count_steps,
                sequence_tenths, decimal_tenths, decimal_hundredths, tenth_in_hundredths]
    if d == 1:
        opts += [decimal_hundredths]
    opts = opts + [line_tenths, bar_tenths, hundredths_grid]
    return pick(opts)()


@skill("Y4.5.e", "Equivalent fractions", S5)
def _(d=1):
    d = _t(d)
    base = pick(_by_d(d, [(1, 2), (1, 4), (1, 3)],
                      [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (2, 5), (1, 5)],
                      [(1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (5, 6), (3, 8)]))
    n, den = base
    k = _by_d(d, 2, random.randint(2, 4), random.randint(2, 5))

    def missing_numerator():
        return _numq("Complete the equivalent fraction:  %d/%d = ___/%d"
                     % (n, den, den * k), n * k,
                     ["The denominator was multiplied by %d." % k,
                      "Do the same to the numerator: %d × %d = %d."
                      % (n, k, n * k)])

    def missing_denominator():
        return _numq("Complete the equivalent fraction:  %d/%d = %d/___"
                     % (n, den, n * k), den * k,
                     ["The numerator was multiplied by %d." % k,
                      "Do the same to the denominator: %d × %d = %d."
                      % (den, k, den * k)])

    def missing_down():
        return _numq("Complete the equivalent fraction:  %d/%d = ___/%d"
                     % (n * k, den * k, den), n,
                     ["The denominator was divided by %d." % k,
                      "Do the same to the numerator: %d ÷ %d = %d."
                      % (n * k, k, n)])

    def shade_bar():
        kk = k if den * k <= 12 else max(2, 12 // den)
        parts = den * kk
        return _fbq("This bar has %d equal parts. Shade it to show %d/%d."
                    % (parts, n, den), parts, n * kk,
                    ["%d/%d = %d/%d." % (n, den, n * kk, parts),
                     "Shade %d of the %d parts." % (n * kk, parts)])

    def shade_area():
        options = [m for m in (2, 3, 4) if den * m <= 12]
        kk = pick(options) if options else 2
        parts = den * kk
        return _agshade("Show the fraction equivalent to %d/%d on this area "
                        "model. The model has %d equal parts."
                        % (n, den, parts), parts, n * kk,
                        ["%d/%d and %d/%d cover the same amount."
                         % (n, den, n * kk, parts),
                         "Shade %d of the %d equal parts." % (n * kk, parts)])

    def on_line():
        line_den = pick([4, 8, 10])
        eq = pick([(1, 2), (1, 4), (3, 4)]) if line_den in (4, 8) \
            else pick([(1, 2), (1, 5), (2, 5)])
        en, ed = eq
        return _nlq("The line from 0 to 1 is split into %d equal steps. Mark %s "
                    "on the line." % (line_den, _frac_words(en, ed)),
                    en / float(ed), 0, 1, 1.0 / line_den, 1.0 / line_den,
                    ["%d/%d = %d/%d." % (en, ed, en * line_den // ed, line_den),
                     "Count %d steps from 0." % (en * line_den // ed)])

    def how_many():
        word = _FRAC_WORDS.get(den * k, "%dth" % (den * k)) + "s"
        return _numq("How many %s are the same as %s?"
                     % (word, _frac_words(n, den)), n * k,
                     ["%d/%d = %d/%d." % (n, den, n * k, den * k),
                      "So the answer is %d." % (n * k)], unit=word)

    def tenths_hundredths():
        m = random.randint(1, 9)
        if random.random() < 0.5:
            return _numq("Complete:  %d/10 = ___/100" % m, m * 10,
                         ["Multiply top and bottom by 10.",
                          "%d/10 = %d/100." % (m, m * 10)])
        return _numq("Complete:  %d/100 = ___/10" % (m * 10), m,
                     ["Divide top and bottom by 10.",
                      "%d/100 = %d/10." % (m * 10, m)])

    def word_cake():
        who = pick(NAMES)
        return _numq("%s cuts a cake into %d equal slices and takes %s of the "
                     "cake. How many slices does %s take?"
                     % (who, den * k, _frac_words(n, den), who), n * k,
                     ["%d slices ÷ %d = %d slices in one %s."
                      % (den * k, den, k, _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %d slices." % (k, n, n * k)], unit="slices")

    def choose_equivalent():
        good = "%d/%d" % (n * k, den * k)
        bad = "%d/%d" % (n * k + 1, den * k)
        if random.random() < 0.5:
            labels, ans = [good, bad], "A"
        else:
            labels, ans = [bad, good], "B"
        return _wordq("Which fraction is equivalent to %d/%d?  A: %s   B: %s.  "
                      "Type A or B." % (n, den, labels[0], labels[1]), ans,
                      ["Multiply the numerator and denominator of %d/%d by %d."
                       % (n, den, k),
                       "%d/%d = %d/%d, so the answer is %s."
                       % (n, den, n * k, den * k, ans)], placeholder="A or B")

    def read_area_equivalent():
        parts = pick([4, 6, 8, 10, 12])
        num = random.randint(1, parts - 1)
        g = _hcf(num, parts)
        return _agread("Write the fraction of this area model that is shaded, "
                       "using the number of parts you can see.", parts, num,
                       ["The model has %d equal parts with %s shaded."
                        % (parts, _pl(num, "part")),
                        "That is %d/%d%s." % (num, parts,
                                              ", which is the same as %d/%d"
                                              % (num // g, parts // g)
                                              if g > 1 else "")],
                       placeholder="e.g. 3/4")

    opts = [missing_numerator, missing_denominator, shade_bar, shade_area,
            on_line, how_many, tenths_hundredths, word_cake,
            read_area_equivalent]
    if d == 0:
        opts = [missing_numerator, missing_denominator, shade_bar, shade_area,
                on_line, tenths_hundredths, read_area_equivalent]
    elif d == 2:
        opts = [missing_numerator, missing_denominator, missing_down, how_many,
                choose_equivalent, tenths_hundredths, word_cake, shade_area,
                on_line]
    opts = opts + [shade_area, on_line]
    return pick(opts)()


@skill("Y4.5.f", "Simplest form", S5)
def _(d=1):
    d = _t(d)
    simple = pick(_by_d(d, [(1, 2), (1, 3), (1, 4), (2, 3)],
                        [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (2, 5), (3, 5),
                         (1, 5)],
                        [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6), (3, 8),
                         (5, 8), (7, 10)]))
    sn, sd = simple
    k = _by_d(d, 2, random.randint(2, 4), random.randint(2, 6))
    bn, bd = sn * k, sd * k

    def numerator_of_simplest():
        return _numq("Write %d/%d in its simplest form. Type the numerator of "
                     "the simplest form." % (bn, bd), sn,
                     ["Divide the numerator and the denominator by %d." % k,
                      "%d/%d = %d/%d, so the numerator is %d."
                      % (bn, bd, sn, sd, sn)])

    def denominator_of_simplest():
        return _numq("Write %d/%d in its simplest form. Type the denominator of "
                     "the simplest form." % (bn, bd), sd,
                     ["Divide the numerator and the denominator by %d." % k,
                      "%d/%d = %d/%d, so the denominator is %d."
                      % (bn, bd, sn, sd, sd)])

    def lowest_terms_numerator():
        return _numq("Write this fraction in its lowest terms:  %d/%d.  Type the "
                     "numerator of the fraction written in lowest terms."
                     % (bn, bd), sn,
                     ["Divide the numerator and the denominator by %d." % k,
                      "In lowest terms %d/%d = %d/%d, so the numerator is %d."
                      % (bn, bd, sn, sd, sn)])

    def lowest_terms_denominator():
        return _numq("Write this fraction in its lowest terms:  %d/%d.  Type the "
                     "denominator of the fraction written in lowest terms."
                     % (bn, bd), sd,
                     ["Divide the numerator and the denominator by %d." % k,
                      "In lowest terms %d/%d = %d/%d, so the denominator is %d."
                      % (bn, bd, sn, sd, sd)])

    def lowest_terms_bar():
        return _fbq("Write the fraction %d/%d in its lowest terms, then shade "
                    "this bar of %d equal parts to show it." % (bn, bd, sd),
                    sd, sn,
                    ["Divide both parts of %d/%d by %d." % (bn, bd, k),
                     "In lowest terms %d/%d = %d/%d, so shade %d of the %d parts."
                     % (bn, bd, sn, sd, sn, sd)])

    def lowest_terms_area():
        # the model must NOT have bd parts, or no simplifying is needed
        cands = [m for m in (sd, sd * 2, sd * 3) if 3 <= m <= 12 and m != bd]
        if not cands:
            return lowest_terms_bar()
        parts = cands[0]
        shaded = sn * (parts // sd)
        return _agshade("Write %d/%d in its lowest terms, then shade this area "
                        "model of %d equal parts to show the same amount."
                        % (bn, bd, parts), parts, shaded,
                        ["%d/%d in lowest terms is %d/%d." % (bn, bd, sn, sd),
                         "On a model of %d equal parts that is %s shaded."
                         % (parts, _pl(shaded, "part"))])

    def divide_by_what():
        return _numq("To write %d/%d in its simplest form, the numerator and the "
                     "denominator are both divided by the same number. What is "
                     "that number?" % (bn, bd), k,
                     ["The highest common factor of %d and %d is %d."
                      % (bn, bd, k),
                      "%d ÷ %d = %d and %d ÷ %d = %d."
                      % (bn, k, sn, bd, k, sd)])

    def already_simplest():
        if random.random() < 0.5:
            return _wordq("Is %d/%d already in its simplest form? Type yes or no."
                          % (sn, sd), "yes",
                          ["The only number that divides both %d and %d is 1."
                           % (sn, sd),
                           "So %d/%d is already in its simplest form."
                           % (sn, sd)], placeholder="yes or no")
        return _wordq("Is %d/%d already in its simplest form? Type yes or no."
                      % (bn, bd), "no",
                      ["Both %d and %d can be divided by %d." % (bn, bd, k),
                       "%d/%d = %d/%d, so it was not in its simplest form."
                       % (bn, bd, sn, sd)], placeholder="yes or no")

    def which_is_simplest():
        if random.random() < 0.5:
            labels, ans = ["%d/%d" % (bn, bd), "%d/%d" % (sn, sd)], "B"
        else:
            labels, ans = ["%d/%d" % (sn, sd), "%d/%d" % (bn, bd)], "A"
        return _wordq("These two fractions are equivalent. Which one is written "
                      "in its simplest form?  A: %s   B: %s.  Type A or B."
                      % (labels[0], labels[1]), ans,
                      ["%d/%d can still be divided by %d." % (bn, bd, k),
                       "%d/%d cannot be simplified further, so the answer is %s."
                       % (sn, sd, ans)], placeholder="A or B")

    def shade_simplest():
        return _fbq("This bar has %d equal parts. Shade it to show %d/%d, which "
                    "has been written in its simplest form." % (sd, bn, bd),
                    sd, sn,
                    ["%d/%d = %d/%d in its simplest form." % (bn, bd, sn, sd),
                     "Shade %d of the %d parts." % (sn, sd)])

    def word_slices():
        who = pick(NAMES)
        return _numq("A cake is cut into %d equal slices and %s eats %d of them. "
                     "In its simplest form the fraction %s eats is %d/___ of "
                     "the cake. Type the missing denominator."
                     % (bd, who, bn, who, sn), sd,
                     ["%d/%d simplifies by dividing both parts by %d."
                      % (bn, bd, k),
                      "%d/%d = %d/%d." % (bn, bd, sn, sd)])

    def set_simplest():
        tot = bd
        red = bn
        return _numq("A bag holds %d counters and %d of them are red. Written in "
                     "its simplest form, the fraction of red counters has "
                     "numerator %d. What is its denominator?" % (tot, red, sn),
                     sd,
                     ["%d/%d is the fraction of red counters." % (red, tot),
                      "Divide both parts by %d: %d/%d." % (k, sn, sd)])

    def common_factor():
        g = _hcf(bn, bd)
        return _numq("What is the highest common factor of %d and %d?" % (bn, bd),
                     g,
                     ["%d and %d can both be divided by %d." % (bn, bd, g),
                      "The highest common factor is %d." % g])

    def hundredths_simplest():
        pair = pick([(50, 2), (25, 4), (75, 4), (20, 5), (40, 5), (60, 5),
                     (80, 5), (10, 10), (30, 10), (70, 10), (90, 10)])
        hk, sdn = pair
        num = hk * sdn // 100
        return _numq("Write %d/100 in its simplest form. Type the denominator of "
                     "the simplest form." % hk, sdn,
                     ["%d/100 = %d/%d." % (hk, num, sdn),
                      "The denominator of the simplest form is %d." % sdn])

    opts = [numerator_of_simplest, denominator_of_simplest,
            lowest_terms_numerator, lowest_terms_denominator, lowest_terms_bar,
            lowest_terms_area, divide_by_what, already_simplest,
            which_is_simplest, shade_simplest, word_slices, common_factor]
    if d == 0:
        opts = [numerator_of_simplest, denominator_of_simplest,
                lowest_terms_numerator, lowest_terms_bar, lowest_terms_area,
                divide_by_what, already_simplest, shade_simplest,
                common_factor]
    elif d == 2:
        opts = [numerator_of_simplest, denominator_of_simplest,
                lowest_terms_denominator, lowest_terms_bar, lowest_terms_area,
                divide_by_what, already_simplest, which_is_simplest,
                set_simplest, word_slices, common_factor, hundredths_simplest]
    opts = opts + [shade_simplest, shade_simplest, lowest_terms_bar,
                   lowest_terms_area, shade_simplest, lowest_terms_bar]
    return pick(opts)()


@skill("Y4.5.g", "Decompose a fraction into a sum of fractions", S5)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [4, 5, 6], [5, 6, 8, 10], [8, 9, 10, 12]))
    tot = random.randint(3, den)
    a = random.randint(1, tot - 1)
    b = tot - a

    def missing_part():
        return _numq("Complete:  %d/%d = %d/%d + ___/%d" % (tot, den, a, den,
                                                            den), b,
                     ["%d − %d = %d." % (tot, a, b),
                      "%d/%d = %d/%d + %d/%d." % (tot, den, a, den, b, den)])

    def missing_first():
        return _numq("Complete:  %d/%d = ___/%d + %d/%d" % (tot, den, den, b,
                                                            den), a,
                     ["%d − %d = %d." % (tot, b, a),
                      "%d/%d = %d/%d + %d/%d." % (tot, den, a, den, b, den)])

    def unit_fractions():
        chain = " + ".join(["1/%d" % den] * tot) if tot <= 6 else None
        why = ("%s = %d/%d." % (chain, tot, den) if chain
               else "Adding 1/%d together %d times gives %d/%d."
                    % (den, tot, tot, den))
        return _numq("How many 1/%d parts are needed to make %d/%d?"
                     % (den, tot, den), tot,
                     ["Each part is 1/%d, so count the parts in %d/%d."
                      % (den, tot, den), why])

    def three_parts():
        if tot < 3:
            return missing_part()
        x = random.randint(1, tot - 2)
        y = random.randint(1, tot - x - 1)
        z = tot - x - y
        return _numq("Complete:  %d/%d = %d/%d + %d/%d + ___/%d"
                     % (tot, den, x, den, y, den, den), z,
                     ["%d + %d = %d." % (x, y, x + y),
                      "%d − %d = %d." % (tot, x + y, z)])

    def whole_decompose():
        x = random.randint(1, den - 1)
        return _numq("1 whole = %d/%d. Complete:  1 = %d/%d + ___/%d"
                     % (den, den, x, den, den), den - x,
                     ["1 whole is %d/%d." % (den, den),
                      "%d − %d = %d." % (den, x, den - x)])

    def sum_as_fraction():
        return _fracq("Work out %d/%d + %d/%d. Write the answer as a fraction."
                      % (a, den, b, den), tot, den,
                      ["Add the numerators and keep the denominator.",
                       "%d + %d = %d, so the answer is %d/%d."
                       % (a, b, tot, tot, den)])

    def shade_missing():
        return _fbq("%d/%d = %d/%d + ? Shade the missing fraction on the bar."
                    % (tot, den, a, den), den, b,
                    ["%d − %d = %s still missing." % (tot, a, _pl(b, "part")),
                     "That is %d/%d." % (b, den)])

    def shade_total():
        return _fbq("Shade the bar to show %d/%d + %d/%d." % (a, den, b, den),
                    den, tot,
                    ["Shade %s, then %d more." % (_pl(a, "part"), b),
                     "%d + %d = %d parts, which is %d/%d."
                     % (a, b, tot, tot, den)])

    def word_two_parts():
        who = pick(NAMES)
        return _fracq("%s eats %d/%d of a pizza in the morning and %d/%d of the "
                      "same pizza in the afternoon. What fraction of the pizza "
                      "has %s eaten in total?" % (who, a, den, b, den, who),
                      tot, den,
                      ["%d/%d + %d/%d = %d/%d." % (a, den, b, den, tot, den)])

    def word_missing():
        who = pick(NAMES)
        return _fracq("%s needs %d/%d of a metre of ribbon and already has %d/%d "
                      "of a metre. What fraction of a metre does %s still need?"
                      % (who, tot, den, a, den, who), b, den,
                      ["%d/%d is made of %d/%d and %d/%d more."
                       % (tot, den, a, den, b, den),
                       "%d/%d − %d/%d = %d/%d." % (tot, den, a, den, b, den)])

    def area_decompose():
        parts = pick([6, 8, 10, 12])
        x = random.randint(1, parts - 2)
        y = random.randint(1, parts - x - 1)
        return _agshade("Shade this area model to show %d/%d + %d/%d."
                        % (x, parts, y, parts), parts, x + y,
                        ["%d + %d = %d parts." % (x, y, x + y),
                         "Shade %d of the %d parts." % (x + y, parts)])

    def equal_halves():
        t2 = 2 * random.randint(1, den // 2)
        return _numq("Split %d/%d into two equal fractions:  %d/%d = ___/%d + ___/%d. What number goes in each gap?"
                     % (t2, den, t2, den, den, den), t2 // 2,
                     ["%d ÷ 2 = %d." % (t2, t2 // 2), "%d/%d = %d/%d + %d/%d." % (t2, den, t2 // 2, den, t2 // 2, den)])

    def beyond_whole():
        x = random.randint(1, den - 1)
        return _fracq("Write 1 + %d/%d as a single fraction with denominator %d." % (x, den, den), den + x, den,
                      ["1 = %d/%d." % (den, den), "%d/%d + %d/%d = %d/%d." % (den, den, x, den, den + x, den)],
                      placeholder="e.g. 9/8")

    def true_false():
        wrong = random.random() < 0.5
        shown = "%d/%d" % (tot, 2 * den) if wrong else "%d/%d" % (tot, den)
        return _wordq("Is this correct?  %d/%d + %d/%d = %s  Type yes or no." % (a, den, b, den, shown), "no" if wrong else "yes",
                      ["When the denominators are the same, add only the numerators: %d/%d." % (tot, den),
                       "So the statement is %s." % ("wrong" if wrong else "correct")], placeholder="yes or no")

    opts = [missing_part, missing_first, unit_fractions, whole_decompose,
            sum_as_fraction, shade_missing, shade_total, word_two_parts,
            area_decompose, word_missing, equal_halves, true_false]
    if d == 0:
        opts = [missing_part, missing_first, unit_fractions, whole_decompose,
                shade_total, word_two_parts, area_decompose, equal_halves, true_false]
    elif d == 2:
        opts = [missing_part, three_parts, three_parts, unit_fractions,
                whole_decompose, word_missing, word_two_parts, shade_missing,
                area_decompose, beyond_whole, equal_halves, true_false]
    opts = opts + [shade_total, area_decompose, shade_missing]
    return pick(opts)()


@skill("Y4.5.h", "Compare and order fractions", S5)
def _(d=1):
    d = _t(d)

    def same_den_larger():
        den = pick(_by_d(d, [4, 5, 6], [4, 5, 6, 8, 10], [6, 8, 9, 10, 12]))
        a, b = random.sample(range(1, den), 2)
        return _fracq("Which is larger, %d/%d or %d/%d? Write the fraction."
                      % (a, den, b, den), max(a, b), den,
                      ["The denominators are the same, so compare the "
                       "numerators.",
                       "%d > %d, so %d/%d is larger."
                       % (max(a, b), min(a, b), max(a, b), den)])

    def same_den_smaller():
        den = pick(_by_d(d, [4, 5, 6], [4, 5, 6, 8, 10], [6, 8, 9, 10, 12]))
        a, b = random.sample(range(1, den), 2)
        return _fracq("Which is smaller, %d/%d or %d/%d? Write the fraction."
                      % (a, den, b, den), min(a, b), den,
                      ["The denominators are the same, so compare the "
                       "numerators.",
                       "%d < %d, so %d/%d is smaller."
                       % (min(a, b), max(a, b), min(a, b), den)])

    def same_num_larger():
        d1, d2 = random.sample(_by_d(d, [2, 3, 4], [2, 3, 4, 5, 6, 8],
                                     [3, 5, 6, 7, 8, 9, 10, 12]), 2)
        num = random.randint(1, min(d1, d2) - 1) if min(d1, d2) > 1 else 1
        return _fracq("Which is larger, %d/%d or %d/%d? Write the fraction."
                      % (num, d1, num, d2), num, min(d1, d2),
                      ["The numerators are the same, so compare the parts.",
                       "Splitting into %d parts gives bigger parts than %d "
                       "parts, so %d/%d is larger."
                       % (min(d1, d2), max(d1, d2), num, min(d1, d2))])

    def same_num_smaller():
        d1, d2 = random.sample(_by_d(d, [2, 3, 4], [2, 3, 4, 5, 6, 8],
                                     [3, 5, 6, 7, 8, 9, 10, 12]), 2)
        num = random.randint(1, min(d1, d2) - 1) if min(d1, d2) > 1 else 1
        return _fracq("Which is smaller, %d/%d or %d/%d? Write the fraction."
                      % (num, d1, num, d2), num, max(d1, d2),
                      ["The numerators are the same, so compare the parts.",
                       "More parts means smaller parts, so %d/%d is smaller."
                       % (num, max(d1, d2))])

    def largest_of_three():
        den = pick([6, 8, 9, 10, 12])
        nums = random.sample(range(1, den), 3)
        return _fracq("Which of these is the largest?  %s.  Write the fraction."
                      % ", ".join("%d/%d" % (v, den) for v in nums),
                      max(nums), den,
                      ["Same denominator, so compare the numerators: %s."
                       % ", ".join(str(v) for v in sorted(nums)),
                       "The largest is %d/%d." % (max(nums), den)])

    def smallest_of_three():
        num = random.randint(1, 2)
        dens = random.sample([3, 4, 5, 6, 8, 10, 12], 3)
        dens = [x for x in dens if x > num]
        while len(dens) < 3:
            extra = pick([5, 6, 8, 10, 12])
            if extra not in dens:
                dens.append(extra)
        return _fracq("Which of these is the smallest?  %s.  Write the fraction."
                      % ", ".join("%d/%d" % (num, v) for v in dens),
                      num, max(dens),
                      ["The numerators are all %d, so the fraction with the most "
                       "parts is smallest." % num,
                       "The smallest is %d/%d." % (num, max(dens))])

    def shade_larger():
        den = pick([4, 5, 6, 8, 10])
        a, b = random.sample(range(1, den), 2)
        return _fbq("Shade the larger of %d/%d and %d/%d on this bar."
                    % (a, den, b, den), den, max(a, b),
                    ["Same denominator: more parts shaded means a larger "
                     "fraction.",
                     "Shade %d of the %d parts." % (max(a, b), den)])

    def shade_smaller():
        den = pick([4, 5, 6, 8, 10])
        a, b = random.sample(range(1, den), 2)
        return _fbq("Shade the SMALLER of %d/%d and %d/%d on this bar."
                    % (a, den, b, den), den, min(a, b),
                    ["Same denominator: fewer parts shaded means a smaller "
                     "fraction.",
                     "Shade %d of the %d parts." % (min(a, b), den)])

    def line_larger():
        den = pick([4, 5, 8, 10])
        a, b = random.sample(range(1, den), 2)
        return _nlq("Which is larger, %d/%d or %d/%d? Place the larger fraction "
                    "on the number line." % (a, den, b, den),
                    max(a, b) / float(den), 0, 1, 1.0 / den, 1.0 / den,
                    ["Same denominator, so compare the numerators.",
                     "The larger fraction is %d/%d." % (max(a, b), den)])

    def graph_compare_same_den():
        den = pick(_by_d(d, [4, 5, 8], [4, 5, 6, 8, 10], [6, 8, 9, 10, 12]))
        a, b = random.sample(range(1, den), 2)
        want_larger = random.random() < 0.5
        k = max(a, b) if want_larger else min(a, b)
        word = "larger" if want_larger else "smaller"
        step = 1.0 / den
        gap = abs(a - b) / float(den)
        return _nlq("Graph and compare fractions with the same denominator on "
                    "number lines. Compare %d/%d and %d/%d, then graph the %s "
                    "fraction on this number line of %d equal steps."
                    % (a, den, b, den, word, den), k / float(den), 0, 1, step,
                    step,
                    ["The denominators are the same, so compare the numerators "
                     "%d and %d." % (a, b),
                     "The %s fraction is %d/%d, which is %s from 0."
                     % (word, k, den, _pl(k, "step"))],
                    tol=min(step / 2.0, gap * 0.4))

    def graph_compare_same_num():
        d1, d2 = random.sample(_by_d(d, [2, 3, 4, 5], [2, 3, 4, 5, 6, 8],
                                     [3, 4, 5, 6, 8, 10, 12]), 2)
        num = random.randint(1, min(d1, d2) - 1) if min(d1, d2) > 1 else 1
        want_larger = random.random() < 0.5
        # with the same numerator, the smaller denominator gives the larger
        # fraction — graph that one, so the line's step always fits.
        den = min(d1, d2) if want_larger else max(d1, d2)
        word = "larger" if want_larger else "smaller"
        step = 1.0 / den
        gap = abs(num / float(d1) - num / float(d2))
        return _nlq("Graph and compare fractions with the same numerator on "
                    "number lines. Compare %d/%d and %d/%d, then graph the %s "
                    "fraction on this number line of %d equal steps."
                    % (num, d1, num, d2, word, den), num / float(den), 0, 1,
                    step, step,
                    ["The numerators are the same, so the fraction with fewer "
                     "parts is the larger one.",
                     "The %s fraction is %d/%d, which is %s from 0."
                     % (word, num, den, _pl(num, "step"))],
                    tol=min(step / 2.0, gap * 0.4))

    def word_who():
        p, q = _two_names()
        den = pick([5, 6, 8, 10])
        a, b = random.sample(range(1, den), 2)
        return _wordq("%s ate %d/%d of a pie and %s ate %d/%d of an identical "
                      "pie. Who ate more? Type the name."
                      % (p, a, den, q, b, den), p if a > b else q,
                      ["Both pies are cut into %d equal parts." % den,
                       "%d/%d is more than %d/%d, so %s ate more."
                       % (max(a, b), den, min(a, b), den, p if a > b else q)],
                      placeholder="a name")

    def word_who_unit():
        p, q = _two_names()
        d1, d2 = random.sample([3, 4, 5, 6, 8, 10], 2)
        return _wordq("%s drank 1/%d of a bottle of juice and %s drank 1/%d of "
                      "an identical bottle. Who drank more? Type the name."
                      % (p, d1, q, d2), p if d1 < d2 else q,
                      ["Fewer equal parts means each part is bigger.",
                       "1/%d is more than 1/%d, so %s drank more."
                       % (min(d1, d2), max(d1, d2), p if d1 < d2 else q)],
                      placeholder="a name")

    def how_many_more():
        den = pick([6, 8, 10, 12])
        a, b = random.sample(range(1, den), 2)
        return _numq("%d/%d and %d/%d are shaded on two identical bars. How many "
                     "MORE parts are shaded on the larger one?"
                     % (a, den, b, den), abs(a - b),
                     ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))],
                     unit="parts")

    def compare_word():
        den = pick([5, 6, 8, 10])
        a, b = random.sample(range(1, den), 2)
        return _wordq("Is %d/%d larger or smaller than %d/%d? Type larger or "
                      "smaller." % (a, den, b, den),
                      "larger" if a > b else "smaller",
                      ["Same denominator, so compare %d and %d." % (a, b),
                       "%d/%d is %s than %d/%d."
                       % (a, den, "larger" if a > b else "smaller", b, den)],
                      placeholder="larger or smaller")

    opts = [same_den_larger, same_den_smaller, same_num_larger, same_num_smaller,
            shade_larger, shade_smaller, line_larger, graph_compare_same_den,
            graph_compare_same_num, word_who, word_who_unit, how_many_more]
    if d == 0:
        opts = [same_den_larger, same_den_smaller, same_num_larger,
                shade_larger, shade_smaller, line_larger,
                graph_compare_same_den, graph_compare_same_num, word_who]
    elif d == 2:
        opts = [same_num_larger, same_num_smaller, largest_of_three,
                smallest_of_three, line_larger, graph_compare_same_den,
                graph_compare_same_num, word_who, word_who_unit,
                how_many_more, compare_word]
    opts = opts + [shade_larger, line_larger, shade_smaller,
                   graph_compare_same_den, graph_compare_same_num]
    return pick(opts)()


@skill("Y4.5.i", "Add and subtract fractions with the same denominator", S5)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [4, 5, 6], [4, 5, 6, 8, 10], [6, 8, 9, 10, 12, 100]))
    if den == 100:
        a = random.randint(10, 60)
        b = random.randint(10, 100 - a)
    else:
        a = random.randint(1, den - 2)
        b = random.randint(1, den - a - 1)

    def add_bare():
        return _fracq("Work out %d/%d + %d/%d." % (a, den, b, den), a + b, den,
                      ["Add the numerators and keep the denominator the same.",
                       "%d + %d = %d, so the answer is %d/%d."
                       % (a, b, a + b, a + b, den)])

    def sub_bare():
        return _fracq("Work out %d/%d − %d/%d." % (a + b, den, b, den), a, den,
                      ["Subtract the numerators and keep the denominator.",
                       "%d − %d = %d, so the answer is %d/%d."
                       % (a + b, b, a, a, den)])

    def add_shade():
        if den == 100:
            return _agshade("Shade this area model to show %d/100 + %d/100."
                            % (a, b), 100, a + b,
                            ["%d + %d = %d hundredths." % (a, b, a + b),
                             "Shade %d of the 100 squares." % (a + b)])
        return _fbq("Shade the bar to show %d/%d + %d/%d." % (a, den, b, den),
                    den, a + b,
                    ["Shade %s, then %d more." % (_pl(a, "part"), b),
                     "%d + %d = %d parts shaded: %d/%d."
                     % (a, b, a + b, a + b, den)])

    def sub_shade():
        if den == 100:
            return _agshade("A hundred square had %d/100 shaded, then %d/100 was "
                            "rubbed out. Shade what is left." % (a + b, b),
                            100, a,
                            ["%d − %d = %d hundredths left." % (a + b, b, a),
                             "That is %d/100." % a])
        return _fbq("A bar had %d/%d shaded, then %d/%d was rubbed out. Shade "
                    "what is left." % (a + b, den, b, den), den, a,
                    ["%d − %d = %s left." % (a + b, b, _pl(a, "part")),
                     "That is %d/%d." % (a, den)])

    def missing_add():
        return _numq("Complete:  %d/%d + ___/%d = %d/%d"
                     % (a, den, den, a + b, den), b,
                     ["%d − %d = %d." % (a + b, a, b),
                      "The missing numerator is %d." % b])

    def missing_sub():
        return _numq("Complete:  %d/%d − ___/%d = %d/%d"
                     % (a + b, den, den, a, den), b,
                     ["%d − %d = %d." % (a + b, a, b),
                      "The missing numerator is %d." % b])

    def make_whole():
        return _fracq("What must be added to %d/%d to make 1 whole? Write the "
                      "fraction." % (a, den), den - a, den,
                      ["1 whole = %d/%d." % (den, den),
                       "%d/%d − %d/%d = %d/%d."
                       % (den, den, a, den, den - a, den)])

    def from_whole():
        return _fracq("Work out 1 − %d/%d. Write the answer as a fraction."
                      % (b, den), den - b, den,
                      ["1 whole = %d/%d." % (den, den),
                       "%d/%d − %d/%d = %d/%d."
                       % (den, den, b, den, den - b, den)])

    def word_add():
        who = pick(NAMES)
        return _fracq("%s drinks %d/%d of a bottle of juice in the morning and "
                      "%d/%d in the afternoon. What fraction of the bottle has "
                      "%s drunk?" % (who, a, den, b, den, who), a + b, den,
                      ["%d/%d + %d/%d = %d/%d." % (a, den, b, den, a + b, den)])

    def word_sub():
        who = pick(NAMES)
        return _fracq("%s had %d/%d of a cake and gave %d/%d of the cake away. "
                      "What fraction of the cake is left?"
                      % (who, a + b, den, b, den), a, den,
                      ["%d/%d − %d/%d = %d/%d." % (a + b, den, b, den, a, den)])

    def three_add():
        if den == 100 or a + b >= den - 1:
            return add_bare()
        c = random.randint(1, den - a - b)
        return _fracq("Work out %d/%d + %d/%d + %d/%d."
                      % (a, den, b, den, c, den), a + b + c, den,
                      ["Add the numerators: %d + %d + %d = %d."
                       % (a, b, c, a + b + c),
                       "The answer is %d/%d." % (a + b + c, den)])

    def improper_add():
        dd = pick([4, 5, 6, 8])
        x = random.randint(2, dd - 1)
        y = random.randint(dd - x + 1, dd - 1)
        return _fracq("Work out %d/%d + %d/%d. The answer is greater than 1 "
                      "whole." % (x, dd, y, dd), x + y, dd,
                      ["%d + %d = %d." % (x, y, x + y),
                       "The answer is %d/%d, which is more than 1 whole."
                       % (x + y, dd)])

    opts = [add_bare, sub_bare, add_shade, sub_shade, missing_add, make_whole,
            from_whole, word_add, word_sub]
    if d == 0:
        opts = [add_bare, sub_bare, add_shade, sub_shade, make_whole,
                word_add, word_sub]
    elif d == 2:
        opts = [add_bare, sub_bare, missing_add, missing_sub, make_whole,
                from_whole, three_add, improper_add, word_add, word_sub,
                add_shade]
    opts = opts + [add_shade, sub_shade, add_shade]
    return pick(opts)()


@skill("Y4.5.j", "Find a fraction of a quantity", S5)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [2, 4], [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 10]))
    per = random.randint(2, _by_d(d, 6, 12, 20))
    total = den * per
    n = 1 if d == 0 else random.randint(1, den - 1)

    def bare():
        return _numq("What is %d/%d of %d?" % (n, den, total), per * n,
                     ["%d ÷ %d = %d (that is one part)." % (total, den, per),
                      "%d × %d = %d." % (per, n, per * n)])

    def bare_words():
        return _numq("What is %s of %d?" % (_frac_words(n, den), total), per * n,
                     ["%d ÷ %d = %d." % (total, den, per),
                      "%d × %d = %d." % (per, n, per * n)])

    def word():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s has %d %s and gives away %s of them. How many %s does "
                     "%s give away?" % (who, total, thing,
                                        _frac_words(n, den), thing, who),
                     per * n,
                     ["%d ÷ %d = %d." % (total, den, per),
                      "%d × %d = %d %s." % (per, n, per * n, thing)], unit=thing)

    def word_left():
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s has %d %s and gives away %s of them. How many %s does "
                     "%s have left?" % (who, total, thing, _frac_words(n, den),
                                        thing, who), total - per * n,
                     ["%s of %d is %d." % (_frac_words(n, den).capitalize(),
                                           total, per * n),
                      "%d − %d = %d %s left." % (total, per * n,
                                                 total - per * n, thing)],
                     unit=thing)

    def inverse():
        return _numq("%s of a number is %d. What is the number?"
                     % (_frac_words(1, den).capitalize(), per), total,
                     ["One part is %d and there are %d equal parts."
                      % (per, den),
                      "%d × %d = %d." % (per, den, total)])

    def money_word():
        dn = pick([2, 4, 5, 10])
        each = random.randint(5, 40)
        tot = dn * each
        num = random.randint(1, dn - 1)
        return _numq("What is %s of %s? Give your answer in pence."
                     % (_frac_words(num, dn), money(tot)), each * num,
                     ["%d ÷ %d = %dp (one part)." % (tot, dn, each),
                      "%d × %d = %dp." % (each, num, each * num)], unit="p")

    def measure_word():
        dn = pick([2, 4, 5, 10])
        num = random.randint(1, dn - 1)
        return _numq("What is %s of 1 metre, in centimetres?"
                     % _frac_words(num, dn), 100 // dn * num,
                     ["1 metre = 100 cm.",
                      "100 ÷ %d = %d cm, and %d × %d = %d cm."
                      % (dn, 100 // dn, 100 // dn, num, 100 // dn * num)],
                     unit="cm")

    def strip_model():
        return _stripq("Use the strip model. The whole strip is %d and it is "
                       "split into %d equal parts. What is one part worth?"
                       % (total, den), den, "?", str(total), "part", per,
                       ["%d ÷ %d = %d." % (total, den, per),
                        "Each part is %d." % per])

    def bar_chart():
        cats = ["Reading", "Maths", "Art"]
        dn = pick([2, 4, 5])
        base = random.randint(4, 15) * dn
        vals = [base, random.randint(10, 60), random.randint(10, 60)]
        num = random.randint(1, dn - 1)
        return _barq("The chart shows how many minutes were spent on each "
                     "subject. How many minutes is %s of the Reading time?"
                     % _frac_words(num, dn), cats, vals, base // dn * num,
                     ["Reading took %d minutes." % base,
                      "%d ÷ %d = %d, and %d × %d = %d minutes."
                      % (base, dn, base // dn, base // dn, num,
                         base // dn * num)])

    def compare():
        dn2 = pick([2, 4, 5])
        per2 = random.randint(2, 12)
        total2 = dn2 * per2
        while per2 == per * n:
            per2 = random.randint(2, 12)
            total2 = dn2 * per2
        big = max(per * n, per2)
        return _numq("Which is more, %s of %d or %s of %d? Type the larger "
                     "amount." % (_frac_words(n, den), total,
                                  _frac_words(1, dn2), total2), big,
                     ["%s of %d = %d." % (_frac_words(n, den), total, per * n),
                      "%s of %d = %d, so the larger amount is %d."
                      % (_frac_words(1, dn2), total2, per2, big)])

    def two_step():
        extra = random.randint(2, 15)
        return _numq("Work out %s of %d, then add %d."
                     % (_frac_words(n, den), total, extra), per * n + extra,
                     ["%s of %d = %d." % (_frac_words(n, den).capitalize(),
                                          total, per * n),
                      "%d + %d = %d." % (per * n, extra, per * n + extra)])

    def hundredths_of():
        hk = pick([10, 20, 25, 50, 75])
        base = pick([100, 200, 300, 400, 500, 800])
        one = base // 100
        val = one * hk
        return _numq("What is %d/100 of %d?" % (hk, base), val,
                     ["1/100 of %d is %d." % (base, one),
                      "%d × %d = %d, so %d/100 of %d = %d."
                      % (one, hk, val, hk, base, val)])

    opts = [bare, bare_words, word, word_left, inverse, money_word,
            measure_word, strip_model, bar_chart]
    if d == 0:
        opts = [bare, bare_words, word, strip_model, bar_chart, money_word,
                measure_word]
    elif d == 2:
        opts = [bare, word, word_left, inverse, money_word, measure_word,
                compare, two_step, hundredths_of, bar_chart, strip_model]
    opts = opts + [strip_model, bar_chart, strip_model]
    return pick(opts)()


@skill("Y4.5.k", "Fraction word problems", S5)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [4, 5, 6], [4, 5, 6, 8, 10], [5, 6, 8, 9, 10, 12]))

    def eaten_left():
        who = pick(NAMES)
        n = random.randint(1, den - 1)
        return _fracq("A pizza is cut into %d equal slices. %s eats %d of the "
                      "slices. What fraction of the pizza is left?"
                      % (den, who, n), den - n, den,
                      ["%d − %d = %s left." % (den, n, _pl(den - n, "slice")),
                       "That is %d/%d of the pizza." % (den - n, den)])

    def two_people_add():
        p, q = _two_names()
        a = random.randint(1, den - 2)
        b = random.randint(1, den - a - 1)
        return _fracq("%s eats %d/%d of a cake and %s eats %d/%d of the same "
                      "cake. What fraction of the cake do %s and %s eat "
                      "altogether?" % (p, a, den, q, b, den, p, q), a + b, den,
                      ["%d/%d + %d/%d = %d/%d." % (a, den, b, den, a + b, den)])

    def two_people_left():
        p, q = _two_names()
        a = random.randint(1, den - 2)
        b = random.randint(1, den - a - 1)
        return _fracq("A cake is cut into %d equal pieces. %s takes %s "
                      "and %s takes %s. What fraction of the cake is "
                      "left?" % (den, p, _pl(a, "piece"), q, _pl(b, "piece")), den - a - b, den,
                      ["%d + %d = %s taken." % (a, b, _pl(a + b, "piece")),
                       "%d − %d = %s left, which is %d/%d."
                       % (den, a + b, _pl(den - a - b, "piece"), den - a - b, den)])

    def fraction_of_quantity():
        per = random.randint(3, 12)
        total = den * per
        n = random.randint(1, den - 1)
        who = pick(NAMES)
        thing = pick(_OBJ)
        return _numq("%s has %d %s and gives %s of them to a friend. How many %s "
                     "does %s give away?" % (who, total, thing,
                                             _frac_words(n, den), thing, who),
                     per * n,
                     ["%d ÷ %d = %d." % (total, den, per),
                      "%d × %d = %d %s." % (per, n, per * n, thing)], unit=thing)

    def money_fraction():
        dn = pick([2, 4, 5, 10])
        each = random.randint(6, 40)
        tot = dn * each
        num = random.randint(1, dn - 1)
        who = pick(NAMES)
        return _numq("%s has %s and spends %s of it. How much does %s spend, in "
                     "pence?" % (who, money(tot), _frac_words(num, dn), who),
                     each * num,
                     ["%d ÷ %d = %dp." % (tot, dn, each),
                      "%d × %d = %dp." % (each, num, each * num)], unit="p")

    def measure_fraction():
        dn = pick([2, 4, 5, 10])
        num = random.randint(1, dn - 1)
        length = dn * random.randint(4, 25)
        return _numq("A ribbon is %d cm long. %s of the ribbon is cut off. How "
                     "long is the piece that is cut off, in cm?"
                     % (length, _frac_words(num, dn).capitalize()),
                     length // dn * num,
                     ["%d ÷ %d = %d cm." % (length, dn, length // dn),
                      "%d × %d = %d cm." % (length // dn, num,
                                            length // dn * num)], unit="cm")

    def who_more():
        p, q = _two_names()
        a, b = random.sample(range(1, den), 2)
        return _wordq("%s reads %d/%d of a book and %s reads %d/%d of an "
                      "identical book. Who reads more? Type the name."
                      % (p, a, den, q, b, den), p if a > b else q,
                      ["Both books are split into %d equal parts." % den,
                       "%d/%d is more than %d/%d, so %s reads more."
                       % (max(a, b), den, min(a, b), den, p if a > b else q)],
                      placeholder="a name")

    def shade_context():
        n = random.randint(1, den - 1)
        who = pick(NAMES)
        return _fbq("%s paints %d out of %d equal sections of a fence. Shade the "
                    "bar to show the fraction %s has painted."
                    % (who, n, den, who), den, n,
                    ["%d out of %d equal sections." % (n, den),
                     "That is %d/%d." % (n, den)])

    def unit_fraction_model():
        who = pick(NAMES)
        item = pick(["ribbon", "cake", "pizza", "loaf of bread", "melon"])
        return _fbq("Unit fractions: model this word problem. %s cuts a %s into "
                    "%d equal pieces and takes one piece. Shade the bar to model "
                    "the fraction of the %s that %s takes."
                    % (who, item, den, item, who), den, 1,
                    ["One piece out of %d equal pieces is a unit fraction."
                     % den,
                     "Shade 1 of the %d parts to model 1/%d." % (den, den)])

    def unit_fraction_model_quantity():
        who = pick(NAMES)
        per = random.randint(3, 12)
        total = den * per
        thing = pick(_OBJ)
        return _stripq("Unit fractions: model this word problem with the strip. "
                       "%s shares %d %s equally between %d friends. How many %s "
                       "does one friend get, which is 1/%d of the %s?"
                       % (who, total, thing, den, thing, den, thing),
                       den, "?", str(total), "part", per,
                       ["The strip shows %d split into %d equal parts."
                        % (total, den),
                        "%d ÷ %d = %d, so 1/%d of %d is %d."
                        % (total, den, per, den, total, per)])

    def set_fraction():
        per = random.randint(2, 8)
        total = den * per
        n = random.randint(1, den - 1)
        col = pick(["red", "blue", "green"])
        return _fracq("A box holds %d counters and %d of them are %s. What "
                      "fraction of the counters are %s?"
                      % (total, per * n, col, col), per * n, total,
                      ["%d out of %d counters are %s." % (per * n, total, col),
                       "The fraction is %d/%d." % (per * n, total)])

    def hundredths_word():
        k = pick([15, 20, 25, 30, 40, 60, 75, 80])
        who = pick(NAMES)
        return _fracq("A jigsaw has 100 pieces. %s has fitted %d of them. What "
                      "fraction of the jigsaw has %s fitted? Use hundredths."
                      % (who, k, who), k, 100,
                      ["%d out of 100 pieces." % k,
                       "The fraction is %d/100." % k],
                      placeholder="e.g. 37/100")

    def area_context():
        parts = pick([6, 8, 10, 12])
        k = random.randint(1, parts - 1)
        return _agread("This garden is split into equal plots. Write the "
                       "fraction of the garden that has been dug over (the "
                       "shaded part).", parts, k,
                       ["The garden has %d equal plots with %s dug over."
                        % (parts, _pl(k, "plot")),
                        "The fraction is %d/%d." % (k, parts)],
                       placeholder="e.g. 3/8")

    def two_step():
        per = random.randint(3, 10)
        total = den * per
        n = random.randint(1, den - 1)
        extra = random.randint(2, 10)
        who = pick(NAMES)
        return _numq("%s has %d sweets, eats %s of them, then is given %d more. "
                     "How many sweets does %s have now?"
                     % (who, total, _frac_words(n, den), extra, who),
                     total - per * n + extra,
                     ["%s of %d = %d eaten." % (_frac_words(n, den).capitalize(),
                                                total, per * n),
                      "%d − %d = %d, then %d + %d = %d sweets."
                      % (total, per * n, total - per * n, total - per * n,
                         extra, total - per * n + extra)], unit="sweets")

    opts = [eaten_left, two_people_add, two_people_left, fraction_of_quantity,
            money_fraction, measure_fraction, who_more, shade_context,
            unit_fraction_model, unit_fraction_model_quantity, set_fraction,
            area_context]
    if d == 0:
        opts = [eaten_left, fraction_of_quantity, shade_context, set_fraction,
                unit_fraction_model, unit_fraction_model_quantity,
                area_context, who_more, measure_fraction]
    elif d == 2:
        opts = [two_people_add, two_people_left, fraction_of_quantity,
                money_fraction, measure_fraction, who_more, hundredths_word,
                two_step, set_fraction, unit_fraction_model_quantity,
                area_context]
    opts = opts + [shade_context, area_context, shade_context,
                   unit_fraction_model, unit_fraction_model_quantity,
                   area_context]
    return pick(opts)()
