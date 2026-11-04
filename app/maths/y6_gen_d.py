# dev/app/logic/y6_gen_d.py — Year 6 generators: strand 6.7
#
# 6.7  Ratio, proportion & algebra            (Y6.7.a .. Y6.7.l)
#
# Every generator takes a difficulty tier: d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between many genuinely different framings (bare technique,
# word problem, missing number, inverse, visual model, comparison, reasoning,
# multi-step).  Visual components carry a large share of the framings:
#   data_table  -> ratio tables, (x, y) tables, price lists, sequence tables
#   strip_model -> share-in-a-ratio bar models
#   io_table    -> expression / sequence rules
#   coordinate_grid, area_grid, bar_chart, number_line -> supporting framings
import random
from .maths_engine import skill, pick, NAMES, n_words, money, ordinal

S7 = "6.7 Ratio, proportion & algebra"


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


def _hcf(a, b):
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


def _simp(a, b):
    g = _hcf(a, b) or 1
    return a // g, b // g


def _coprime_pair(lo=2, hi=9):
    while True:
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if a != b and _hcf(a, b) == 1:
            return a, b


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _pounds(n):
    """A whole number of pounds, written the UK way."""
    return "£%d" % int(n)


def _numq(prompt, answer, solution, unit=None, placeholder=None,
          answer_type="int", text=False, tolerance=0):
    spec = {}
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _wordq(prompt, answer, solution, placeholder=None):
    return _numq(prompt, answer, solution, placeholder=placeholder,
                 answer_type="str", text=True)


def _fracq(prompt, num, den, solution, placeholder="e.g. 3/8"):
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": "%d/%d" % (num, den), "answer_type": "frac",
            "tolerance": 0, "solution": solution}


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


def _stripq(prompt, spec, answer, solution):
    return {"prompt": prompt, "component": "strip_model", "spec": spec,
            "answer": int(answer), "answer_type": "int", "tolerance": 0,
            "solution": solution}


def _share_strip(prompt, parts, total, answer, solution):
    """Bar model: `total` split into `parts` equal parts; one part is unknown."""
    return _stripq(prompt,
                   {"mode": "equal_parts", "parts": int(parts),
                    "partLabel": "?", "totalLabel": str(total),
                    "unknown": "part"}, answer, solution)


def _total_strip(prompt, parts, one_part, answer, solution):
    """Bar model: `parts` equal parts each worth `one_part`; total unknown."""
    return _stripq(prompt,
                   {"mode": "equal_parts", "parts": int(parts),
                    "partLabel": str(one_part), "totalLabel": "?",
                    "unknown": "total"}, answer, solution)


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


def _gridq(prompt, x, y, solution, size=10):
    return {"prompt": prompt, "component": "coordinate_grid",
            "spec": {"mode": "plot", "size": int(size)},
            "answer": "(%d,%d)" % (x, y), "answer_type": "coord",
            "tolerance": 0, "solution": solution}


def _agread(prompt, parts, shaded, answer, solution, answer_type="int",
            placeholder=None):
    spec = {"mode": "fraction_read", "parts": int(parts), "shaded": int(shaded)}
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


def _barq(prompt, cats, vals, answer, solution):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "mode": "read"},
            "answer": answer, "answer_type": "int", "tolerance": 0,
            "solution": solution}


# object pairs — safe inside "a box / a collection / a shop" contexts
_PAIRS = [("red beads", "blue beads"), ("roses", "tulips"),
          ("cars", "vans"), ("pens", "pencils"), ("apples", "pears"),
          ("hardbacks", "paperbacks"), ("stamps", "stickers"),
          ("cubes", "cones"), ("red counters", "blue counters"),
          ("plain buns", "iced buns")]
# people pairs — used only where the context is a group of people
_PEOPLE = [("boys", "girls"), ("adults", "children"),
           ("singers", "musicians"), ("swimmers", "runners")]


# ================================================================= 6.7.a =====
@skill("Y6.7.a", "Write and simplify a ratio", S7)
def _(d=1):
    d = _t(d)
    a, b = _coprime_pair(2, _by_d(d, 5, 7, 9))
    k = _by_d(d, random.randint(2, 4), random.randint(2, 8),
              random.randint(4, 12))
    A, B = a * k, b * k

    def simplify_first():
        return _numq("Write the ratio %d : %d in its simplest form. Type the "
                     "first number of the simplified ratio." % (A, B), a,
                     ["The highest common factor of %d and %d is %d."
                      % (A, B, k),
                      "%d ÷ %d = %d and %d ÷ %d = %d, so the ratio is %d : %d."
                      % (A, k, a, B, k, b, a, b)],
                     placeholder="first number")

    def simplify_second():
        return _numq("Write the ratio %d : %d in its simplest form. Type the "
                     "second number of the simplified ratio." % (A, B), b,
                     ["Divide both numbers by the highest common factor, %d." % k,
                      "%d : %d simplifies to %d : %d." % (A, B, a, b)],
                     placeholder="second number")

    def hcf_step():
        return _numq("To write %d : %d in its simplest form you divide both "
                     "numbers by their highest common factor. What is that "
                     "highest common factor?" % (A, B), k,
                     ["%d = %d × %d and %d = %d × %d." % (A, k, a, B, k, b),
                      "The highest common factor is %d." % k],
                     placeholder="the HCF")

    def from_counts():
        one, two = pick(_PAIRS)
        return _numq("A box holds %d %s and %d %s. Write the ratio of %s to %s "
                     "in its simplest form and type the first number."
                     % (A, one, B, two, one, two), a,
                     ["The ratio is %d : %d." % (A, B),
                      "Dividing both parts by %d gives %d : %d." % (k, a, b)],
                     placeholder="first number")

    def from_counts_second():
        one, two = pick(_PAIRS)
        return _numq("A crate holds %d %s and %d %s. Write the ratio of %s to "
                     "%s in its simplest form and type the second number."
                     % (A, one, B, two, one, two), b,
                     ["The ratio is %d : %d." % (A, B),
                      "Dividing both parts by %d gives %d : %d." % (k, a, b)],
                     placeholder="second number")

    def words_to_figures():
        one, two = pick(_PAIRS)
        return _numq("In a box the ratio of %s to %s is %s to %s. Written "
                     "with figures this ratio is ___ : %d. What number goes in "
                     "the blank?" % (one, two, n_words(a), n_words(b), b), a,
                     ["%s in figures is %d." % (n_words(a).capitalize(), a)],
                     placeholder="a number")

    def part_to_whole():
        one, two = pick(_PEOPLE)
        return _fracq("The ratio of %s to %s in a class is %d : %d. What "
                      "fraction of the class are %s?" % (one, two, a, b, one),
                      a, a + b,
                      ["The ratio has %d + %d = %d equal parts." % (a, b, a + b),
                       "%d of those %d parts are %s, so the fraction is %d/%d."
                       % (a, a + b, one, a, a + b)])

    def part_to_whole_second():
        one, two = pick(_PAIRS)
        return _fracq("A shelf holds %s and %s in the ratio %d : %d. What "
                      "fraction of the items on the shelf are %s?"
                      % (one, two, a, b, two), b, a + b,
                      ["There are %d + %d = %d equal parts altogether."
                       % (a, b, a + b),
                       "%d parts out of %d are %s: %d/%d."
                       % (b, a + b, two, b, a + b)])

    def ratio_as_fraction():
        one, two = pick(_PAIRS)
        return _fracq("The ratio of %s to %s is %d : %d. Write this ratio as a "
                      "fraction (the number of %s divided by the number of %s)."
                      % (one, two, A, B, one, two), a, b,
                      ["%d : %d written as a fraction is %d/%d."
                       % (A, B, A, B),
                       "%d/%d simplifies to %d/%d." % (A, B, a, b)])

    def total_parts():
        return _numq("A quantity is shared in the ratio %d : %d. How many equal "
                     "parts is the quantity split into altogether?" % (a, b),
                     a + b,
                     ["%d + %d = %d equal parts." % (a, b, a + b)],
                     placeholder="number of parts")

    def three_part():
        c = random.randint(2, 6)
        m = random.randint(2, 5)
        return _numq("Write the ratio %d : %d : %d in its simplest form and "
                     "type the middle number." % (a * m, b * m, c * m), b,
                     ["Every part divides by %d." % m,
                      "The simplified ratio is %d : %d : %d." % (a, b, c)],
                     placeholder="middle number")

    def grid_shaded():
        parts = pick([10, 12, 16, 20])
        s = random.randint(2, parts - 2)
        sa, sb = _simp(s, parts - s)
        return _agread("This grid has %d squares and %d of them are shaded. "
                       "Write the ratio of shaded squares to unshaded squares "
                       "in its simplest form and type the first number."
                       % (parts, s), parts, s, sa,
                       ["%d squares are shaded and %d are unshaded."
                        % (s, parts - s),
                        "%d : %d simplifies to %d : %d."
                        % (s, parts - s, sa, sb)],
                       placeholder="first number")

    def grid_shaded_second():
        parts = pick([10, 12, 16, 20])
        s = random.randint(2, parts - 2)
        sa, sb = _simp(s, parts - s)
        return _agread("This grid has %d squares and %d of them are shaded. "
                       "Write the ratio of shaded squares to unshaded squares "
                       "in its simplest form and type the second number."
                       % (parts, s), parts, s, sb,
                       ["%d shaded and %d unshaded." % (s, parts - s),
                        "%d : %d simplifies to %d : %d."
                        % (s, parts - s, sa, sb)],
                       placeholder="second number")

    def table_counts():
        one, two = pick(_PAIRS)
        rows = [[one.capitalize(), str(A)], [two.capitalize(), str(B)]]
        return _dtq("The table shows what is in a box. Write the ratio of %s to "
                    "%s in its simplest form and type the first number."
                    % (one, two), ["Item", "Number"], rows, a,
                    ["The ratio is %d : %d." % (A, B),
                     "Divide both parts by %d to get %d : %d." % (k, a, b)],
                    caption="Contents of the box")

    def reverse_from_simplest():
        return _numq("A ratio written in its simplest form is %d : %d. The "
                     "first number of the original ratio was %d. What was the "
                     "second number?" % (a, b, A), B,
                     ["%d ÷ %d = %d, so both parts were multiplied by %d."
                      % (A, a, k, k),
                      "%d × %d = %d." % (b, k, B)])

    def already_simplest():
        if random.random() < 0.5:
            return _wordq("Is the ratio %d : %d already in its simplest form? "
                          "Type yes or no." % (a, b), "yes",
                          ["The highest common factor of %d and %d is 1."
                           % (a, b),
                           "So %d : %d is already in its simplest form."
                           % (a, b)], placeholder="yes or no")
        return _wordq("Is the ratio %d : %d already in its simplest form? Type "
                      "yes or no." % (A, B), "no",
                      ["Both %d and %d divide by %d." % (A, B, k),
                       "%d : %d simplifies to %d : %d, so it was not in its "
                       "simplest form." % (A, B, a, b)],
                      placeholder="yes or no")

    def measure_ratio():
        cm = random.randint(2, 9) * 10
        m = random.randint(2, 6)
        g = _hcf(cm, m * 100)
        return _numq("A rope is %d cm long and a second rope is %d m long. "
                     "Write the ratio of the first length to the second in its "
                     "simplest form, using the same units. Type the first "
                     "number." % (cm, m), cm // g,
                     ["%d m = %d cm." % (m, m * 100),
                      "%d : %d simplifies to %d : %d."
                      % (cm, m * 100, cm // g, (m * 100) // g)],
                     placeholder="first number")

    opts = [simplify_first, simplify_second, from_counts, from_counts_second,
            part_to_whole, ratio_as_fraction, total_parts, grid_shaded,
            table_counts, hcf_step]
    if d == 0:
        opts = [simplify_first, simplify_second, from_counts, total_parts,
                part_to_whole, grid_shaded, table_counts, words_to_figures,
                hcf_step]
    elif d == 2:
        opts = [simplify_first, simplify_second, ratio_as_fraction,
                part_to_whole_second, three_part, reverse_from_simplest,
                already_simplest, measure_ratio, grid_shaded_second,
                table_counts, from_counts_second]
    opts = opts + [grid_shaded, table_counts, grid_shaded_second, table_counts]
    return pick(opts)()


# ================================================================= 6.7.b =====
@skill("Y6.7.b", "Equivalent ratios and ratio tables", S7)
def _(d=1):
    d = _t(d)
    a, b = _coprime_pair(2, _by_d(d, 5, 7, 9))
    k = _by_d(d, random.randint(2, 4), random.randint(2, 7),
              random.randint(5, 12))

    def complete_second():
        return _numq("Complete the equivalent ratio:  %d : %d = %d : ___"
                     % (a, b, a * k), b * k,
                     ["%d × %d = %d, so both parts are multiplied by %d."
                      % (a, k, a * k, k),
                      "%d × %d = %d." % (b, k, b * k)])

    def complete_first():
        return _numq("Complete the equivalent ratio:  %d : %d = ___ : %d"
                     % (a, b, b * k), a * k,
                     ["%d × %d = %d, so both parts are multiplied by %d."
                      % (b, k, b * k, k),
                      "%d × %d = %d." % (a, k, a * k)])

    def complete_down():
        return _numq("Complete the equivalent ratio:  %d : %d = %d : ___"
                     % (a * k, b * k, a), b,
                     ["%d ÷ %d = %d, so both parts are divided by %d."
                      % (a * k, a, k, k),
                      "%d ÷ %d = %d." % (b * k, k, b)])

    def find_multiplier():
        return _numq("The ratio %d : %d has been multiplied to give %d : %d. "
                     "What number were both parts multiplied by?"
                     % (a, b, a * k, b * k), k,
                     ["%d ÷ %d = %d." % (a * k, a, k),
                      "Check: %d × %d = %d ✓." % (b, k, b * k)],
                     placeholder="a number")

    def table_missing_right():
        n = 4
        mults = sorted(random.sample(range(1, 10), n))
        rows = [[str(a * m), str(b * m)] for m in mults]
        i = random.randrange(n)
        rows[i][1] = ""
        return _dtq("This ratio table keeps the ratio %d : %d. What number is "
                    "missing from the table?" % (a, b),
                    ["Part A", "Part B"], rows, b * mults[i],
                    ["Every row keeps the ratio %d : %d." % (a, b),
                     "%d ÷ %d = %d, so Part B is %d × %d = %d."
                     % (a * mults[i], a, mults[i], b, mults[i], b * mults[i])],
                    missing=(i, 1), caption="Ratio table")

    def table_missing_left():
        n = 4
        mults = sorted(random.sample(range(1, 10), n))
        rows = [[str(a * m), str(b * m)] for m in mults]
        i = random.randrange(n)
        rows[i][0] = ""
        return _dtq("This ratio table keeps the ratio %d : %d. What number is "
                    "missing from the table?" % (a, b),
                    ["Part A", "Part B"], rows, a * mults[i],
                    ["Every row keeps the ratio %d : %d." % (a, b),
                     "%d ÷ %d = %d, so Part A is %d × %d = %d."
                     % (b * mults[i], b, mults[i], a, mults[i], a * mults[i])],
                    missing=(i, 0), caption="Ratio table")

    def recipe_table():
        m1 = random.randint(1, 3)
        m2 = m1 + random.randint(1, 4)
        m3 = m2 + random.randint(1, 4)
        f, s = a * 50, b * 20
        rows = [["%d" % m1, str(f * m1), str(s * m1)],
                ["%d" % m2, str(f * m2), str(s * m2)],
                ["%d" % m3, "", str(s * m3)]]
        return _dtq("This recipe table keeps every ingredient in proportion. "
                    "How much flour is needed for %d batches, in grams?" % m3,
                    ["Batches", "Flour (g)", "Sugar (g)"], rows, f * m3,
                    ["One batch needs %d g of flour." % f,
                     "%d × %d = %d g." % (f, m3, f * m3)],
                    missing=(2, 1), caption="Biscuit recipe")

    def word_scale_up():
        one, two = pick(_PEOPLE)
        return _numq("In a park the ratio of %s to %s is %d : %d. There are %d "
                     "%s. How many %s are there?"
                     % (one, two, a, b, a * k, one, two), b * k,
                     ["%d ÷ %d = %d, so each part is worth %d."
                      % (a * k, a, k, k),
                      "%d × %d = %d %s." % (b, k, b * k, two)], unit=two)

    def word_scale_down():
        one, two = pick(_PAIRS)
        return _numq("The ratio of %s to %s in a shop is %d : %d. There are %d "
                     "%s. How many %s are there?"
                     % (one, two, a, b, b * k, two, one), a * k,
                     ["%d ÷ %d = %d, so each part is worth %d."
                      % (b * k, b, k, k),
                      "%d × %d = %d %s." % (a, k, a * k, one)], unit=one)

    def equivalent_yes_no():
        if random.random() < 0.5:
            return _wordq("Are the ratios %d : %d and %d : %d equivalent? Type "
                          "yes or no." % (a, b, a * k, b * k), "yes",
                          ["%d : %d divides by %d to give %d : %d."
                           % (a * k, b * k, k, a, b),
                           "The ratios are equivalent."],
                          placeholder="yes or no")
        off = pick([1, 2])
        return _wordq("Are the ratios %d : %d and %d : %d equivalent? Type yes "
                      "or no." % (a, b, a * k, b * k + off), "no",
                      ["%d × %d = %d, so the second part would have to be "
                       "%d × %d = %d." % (a, k, a * k, b, k, b * k),
                       "It is %d instead, so the ratios are not equivalent."
                       % (b * k + off)],
                      placeholder="yes or no")

    def io_equivalent():
        mults = sorted(random.sample(range(2, 12), 4))
        rows = [[a * m, b * m] for m in mults]
        i = random.randrange(4)
        return _ioq("Every pair in this table is in the same ratio, %d : %d. "
                    "Type the missing Out number." % (a, b), rows, i,
                    rows[i][1],
                    ["The Out number is always the In number ÷ %d × %d."
                     % (a, b),
                     "%d ÷ %d × %d = %d." % (rows[i][0], a, b, rows[i][1])],
                    rule="ratio %d : %d" % (a, b))

    def scale_both_word():
        one, two = pick(_PAIRS)
        return _numq("A pattern uses %s and %s in the ratio %d : %d. If %d %s "
                     "are used, how many items are used altogether?"
                     % (one, two, a, b, a * k, one), (a + b) * k,
                     ["Each part is worth %d ÷ %d = %d." % (a * k, a, k),
                      "There are %d + %d = %d parts, so %d × %d = %d items."
                      % (a, b, a + b, a + b, k, (a + b) * k)])

    def table_three_rows():
        m = sorted(random.sample(range(2, 9), 3))
        rows = [["%d cm" % (a * x), "%d cm" % (b * x)] for x in m]
        i = random.randrange(3)
        rows[i][1] = ""
        return _dtq("Two lengths always stay in the ratio %d : %d. What is the "
                    "missing length, in cm?" % (a, b),
                    ["Length A", "Length B"], rows, b * m[i],
                    ["Length A is %d cm, which is %d × %d."
                     % (a * m[i], a, m[i]),
                     "Length B is %d × %d = %d cm." % (b, m[i], b * m[i])],
                    missing=(i, 1), caption="Lengths in a fixed ratio")

    def simplest_of_pair():
        return _numq("Which ratio is equivalent to %d : %d? Type the missing "
                     "number:  %d : ___" % (a * k, b * k, a), b,
                     ["%d : %d divides by %d to give %d : %d."
                      % (a * k, b * k, k, a, b)])

    opts = [complete_second, complete_first, complete_down, find_multiplier,
            table_missing_right, table_missing_left, recipe_table,
            word_scale_up, io_equivalent, table_three_rows]
    if d == 0:
        opts = [complete_second, complete_first, table_missing_right,
                table_missing_left, word_scale_up, io_equivalent,
                table_three_rows, simplest_of_pair]
    elif d == 2:
        opts = [complete_down, find_multiplier, word_scale_down,
                equivalent_yes_no, scale_both_word, recipe_table,
                table_missing_left, io_equivalent, table_three_rows,
                complete_first]
    opts = opts + [table_missing_right, recipe_table, table_three_rows,
                   io_equivalent]
    return pick(opts)()


# ================================================================= 6.7.c =====
@skill("Y6.7.c", "Ratio problems and unequal sharing", S7)
def _(d=1):
    d = _t(d)
    a, b = _coprime_pair(1, _by_d(d, 4, 6, 8))
    if a + b > 12:
        a, b = _coprime_pair(1, 5)
    unit = _by_d(d, random.randint(2, 8), random.randint(3, 15),
                 random.randint(6, 30))
    total = (a + b) * unit

    def strip_one_part():
        one, two = _two_names()
        return _share_strip("%s and %s share %s in the ratio %d : %d. The bar "
                            "model shows the %d equal parts. How much is one "
                            "part worth, in pounds?"
                            % (one, two, _pounds(total), a, b, a + b),
                            a + b, _pounds(total), unit,
                            ["The ratio %d : %d needs %d + %d = %d equal parts."
                             % (a, b, a, b, a + b),
                             "%d ÷ %d = %d, so one part is %s."
                             % (total, a + b, unit, _pounds(unit))])

    def strip_total():
        one, two = _two_names()
        return _total_strip("%s and %s share some money in the ratio %d : %d, "
                            "so there are %d equal parts. Each part is worth "
                            "%s. What is the total amount, in pounds?"
                            % (one, two, a, b, a + b, _pounds(unit)),
                            a + b, _pounds(unit), total,
                            ["There are %d + %d = %d equal parts."
                             % (a, b, a + b),
                             "%d × %d = %d, so the total is %s."
                             % (a + b, unit, total, _pounds(total))])

    def larger_share():
        one, two = _two_names()
        big, small = (a, b) if a > b else (b, a)
        who = one if a > b else two
        return _numq("%s and %s share %s in the ratio %d : %d, with %s taking "
                     "the %d parts. How much does %s get, in pounds?"
                     % (one, two, _pounds(total), a, b, who, big, who),
                     big * unit,
                     ["%d + %d = %d equal parts." % (a, b, a + b),
                      "%d ÷ %d = %d, so one part is %s."
                      % (total, a + b, unit, _pounds(unit)),
                      "%d × %d = %d, so %s gets %s."
                      % (big, unit, big * unit, who, _pounds(big * unit))],
                     unit="£")

    def smaller_share():
        one, two = _two_names()
        return _numq("%s and %s share %d sweets in the ratio %d : %d, with %s "
                     "taking the %s. How many sweets does %s get?"
                     % (one, two, total, a, b, two, "1 part" if b == 1 else "%d parts" % b, two), b * unit,
                     ["%d + %d = %d equal parts." % (a, b, a + b),
                      "%d ÷ %d = %d sweets in one part." % (total, a + b, unit),
                      "%d × %d = %d sweets." % (b, unit, b * unit)],
                     unit="sweets")

    def difference_of_shares():
        one, two = _two_names()
        diff = abs(a - b) * unit
        if diff == 0:
            return larger_share()
        return _numq("%d marbles are shared in the ratio %d : %d. What is the "
                     "difference between the two shares?" % (total, a, b), diff,
                     ["%d ÷ %d = %d marbles in one part." % (total, a + b, unit),
                      "The shares are %d and %d marbles."
                      % (a * unit, b * unit),
                      "%d − %d = %d." % (max(a, b) * unit, min(a, b) * unit,
                                         diff)],
                     unit="marbles")

    def total_from_one_share():
        one, two = _two_names()
        return _numq("%s and %s share some stickers in the ratio %d : %d. %s "
                     "gets %s and receives %d stickers. How many "
                     "stickers were shared altogether?"
                     % (one, two, a, b, one, "1 part" if a == 1 else "the %d parts" % a, a * unit), total,
                     ["%d ÷ %d = %d stickers in one part." % (a * unit, a, unit),
                      "There are %d parts altogether, so %d × %d = %d stickers."
                      % (a + b, a + b, unit, total)], unit="stickers")

    def other_share_from_one():
        one, two = _two_names()
        return _numq("Money is shared in the ratio %d : %d. The %d-part share "
                     "is %s. How much is the %d-part share, in pounds?"
                     % (a, b, a, _pounds(a * unit), b), b * unit,
                     ["One part is %d ÷ %d = %s." % (a * unit, a, _pounds(unit)),
                      "%d × %d = %d, so the other share is %s."
                      % (b, unit, b * unit, _pounds(b * unit))], unit="£")

    def total_from_difference():
        if a == b:
            return larger_share()
        diff = abs(a - b) * unit
        return _numq("A prize is shared in the ratio %d : %d. The larger share "
                     "is %s more than the smaller share. What is the total "
                     "prize, in pounds?" % (a, b, _pounds(diff)), total,
                     ["The difference is %d − %d = %s."
                      % (max(a, b), min(a, b), _pl(abs(a - b), "part")),
                      "%d ÷ %d = %d, so one part is %s."
                      % (diff, abs(a - b), unit, _pounds(unit)),
                      "%d parts altogether: %d × %d = %s."
                      % (a + b, a + b, unit, _pounds(total))], unit="£")

    def three_way_strip():
        c = random.randint(1, 4)
        parts = a + b + c
        if parts > 12:
            return strip_one_part()
        u = random.randint(3, 12)
        tot = parts * u
        return _share_strip("%d counters are shared in the ratio %d : %d : %d. "
                            "The bar model shows the %d equal parts. How many "
                            "counters are in one part?"
                            % (tot, a, b, c, parts), parts, str(tot), u,
                            ["%d + %d + %d = %d equal parts." % (a, b, c, parts),
                             "%d ÷ %d = %d counters in each part."
                             % (tot, parts, u)])

    def three_way_share():
        c = random.randint(1, 4)
        parts = a + b + c
        u = random.randint(3, 12)
        tot = parts * u
        return _numq("%d cards are shared between three children in the ratio "
                     "%d : %d : %d. How many cards are in the largest share?"
                     % (tot, a, b, c), max(a, b, c) * u,
                     ["%d + %d + %d = %d equal parts." % (a, b, c, parts),
                      "%d ÷ %d = %d cards in one part." % (tot, parts, u),
                      "The largest share is %d parts: %d × %d = %d cards."
                      % (max(a, b, c), max(a, b, c), u, max(a, b, c) * u)],
                     unit="cards")

    def missing_quantity():
        one, two = pick(_PEOPLE)
        return _numq("In a choir the ratio of %s to %s is %d : %d. There are %d "
                     "%s. How many %s are in the choir?"
                     % (one, two, a, b, a * unit, one, two), b * unit,
                     ["%d ÷ %d = %d in each part." % (a * unit, a, unit),
                      "%d × %d = %d %s." % (b, unit, b * unit, two)], unit=two)

    def how_many_more():
        one, two = pick(_PAIRS)
        if a == b:
            return missing_quantity()
        return _numq("A shop stocks %s and %s in the ratio %d : %d. There are "
                     "%d items altogether. How many more of the larger group "
                     "are there than the smaller group?"
                     % (one, two, a, b, total), abs(a - b) * unit,
                     ["%d ÷ %d = %d items in one part." % (total, a + b, unit),
                      "The groups have %d and %d items."
                      % (a * unit, b * unit),
                      "%d − %d = %d." % (max(a, b) * unit, min(a, b) * unit,
                                         abs(a - b) * unit)])

    def table_shares():
        one, two = _two_names()
        rows = [[one, "%d parts" % a, ""], [two, "%d parts" % b,
                                            str(b * unit)]]
        return _dtq("%s and %s share %d beads in the ratio %d : %d. How many "
                    "beads does %s get?" % (one, two, total, a, b, one),
                    ["Name", "Share", "Beads"], rows, a * unit,
                    ["%d ÷ %d = %d beads in one part." % (total, a + b, unit),
                     "%s has %s: %d × %d = %d beads."
                     % (one, _pl(a, "part"), a, unit, a * unit)],
                    missing=(0, 2), caption="Sharing %d beads" % total)

    def fraction_of_total():
        return _fracq("A length of ribbon is cut in the ratio %d : %d. What "
                      "fraction of the ribbon is the %d-part piece?"
                      % (a, b, a), a, a + b,
                      ["There are %d + %d = %d equal parts." % (a, b, a + b),
                       "The %d-part piece is %d/%d of the ribbon."
                       % (a, a, a + b)])

    def two_step_left():
        one, two = _two_names()
        spend = random.randint(1, max(1, a * unit - 1))
        return _numq("%s and %s share %s in the ratio %d : %d, with %s taking "
                     "%s. %s then spends %s. How much does %s have "
                     "left, in pounds?"
                     % (one, two, _pounds(total), a, b, one, "1 part" if a == 1 else "the %d parts" % a, one,
                        _pounds(spend), one), a * unit - spend,
                     ["One part is %d ÷ %d = %s."
                      % (total, a + b, _pounds(unit)),
                      "%s gets %d × %d = %s." % (one, a, unit,
                                                 _pounds(a * unit)),
                      "%d − %d = %s left." % (a * unit, spend,
                                              _pounds(a * unit - spend))],
                     unit="£")

    opts = [strip_one_part, strip_total, larger_share, smaller_share,
            difference_of_shares, total_from_one_share, missing_quantity,
            table_shares, three_way_strip, fraction_of_total]
    if d == 0:
        opts = [strip_one_part, strip_total, smaller_share, larger_share,
                missing_quantity, table_shares, fraction_of_total,
                three_way_strip]
    elif d == 2:
        opts = [total_from_difference, other_share_from_one, three_way_share,
                how_many_more, two_step_left, total_from_one_share,
                difference_of_shares, strip_one_part, table_shares,
                three_way_strip]
    opts = opts + [strip_one_part, strip_total, three_way_strip, table_shares]
    return pick(opts)()


# ================================================================= 6.7.d =====
_ITEMS = [("pen", "pens"), ("apple", "apples"), ("notebook", "notebooks"),
          ("balloon", "balloons"), ("candle", "candles"), ("badge", "badges")]


@skill("Y6.7.d", "Proportion and unit rates", S7)
def _(d=1):
    d = _t(d)
    sing, plur = pick(_ITEMS)

    def unit_price():
        n = _by_d(d, random.randint(2, 5), random.randint(3, 8),
                  random.randint(6, 12))
        each = _by_d(d, random.randint(5, 40), random.randint(12, 95),
                     random.randint(35, 180))
        return _numq("%d %s cost %s altogether. How much does one %s cost, in "
                     "pence?" % (n, plur, money(n * each), sing), each,
                     ["%d ÷ %d = %dp for one %s." % (n * each, n, each, sing)],
                     unit="p")

    def scale_up():
        n = random.randint(2, 6)
        m = n + random.randint(1, _by_d(d, 3, 6, 9))
        each = _by_d(d, random.randint(5, 30), random.randint(8, 60),
                     random.randint(15, 120))
        return _numq("%d %s cost %s. At the same rate, how much do %d %s cost, "
                     "in pence?" % (n, plur, money(n * each), m, plur),
                     m * each,
                     ["One %s costs %d ÷ %d = %dp."
                      % (sing, n * each, n, each),
                      "%d × %d = %dp." % (m, each, m * each)], unit="p")

    def how_many_for():
        each = _by_d(d, random.randint(2, 10), random.randint(4, 25),
                     random.randint(6, 40))
        n = random.randint(3, 9)
        return _numq("One %s costs %dp. How many %s can be bought with exactly "
                     "%s?" % (sing, each, plur, money(each * n)), n,
                     ["%d ÷ %d = %d %s." % (each * n, each, n, plur)],
                     unit=plur)

    def recipe_scale():
        people = pick([2, 3, 4, 5, 6])
        want = people * random.randint(2, _by_d(d, 3, 4, 6))
        per = random.randint(20, 90)
        return _numq("A recipe for %d people uses %d g of rice. How much rice "
                     "is needed for %d people, in grams?"
                     % (people, per * people, want), per * want,
                     ["One person needs %d ÷ %d = %d g."
                      % (per * people, people, per),
                      "%d × %d = %d g." % (per, want, per * want)], unit="g")

    def recipe_down():
        people = random.randint(4, 12)
        want = random.choice([x for x in range(2, people) if people % x == 0]
                             or [2])
        per = random.randint(15, 60)
        return _numq("A recipe for %d people uses %d ml of milk. How much milk "
                     "is needed for %d people, in millilitres?"
                     % (people, per * people, want), per * want,
                     ["One person needs %d ÷ %d = %d ml."
                      % (per * people, people, per),
                      "%d × %d = %d ml." % (per, want, per * want)], unit="ml")

    def speed():
        h = random.randint(2, 8)
        s = _by_d(d, random.randint(20, 60), random.randint(30, 90),
                  random.randint(45, 120))
        return _numq("A coach travels %d km in %d hours at a steady speed. How "
                     "many kilometres does the coach travel in one hour?"
                     % (s * h, h), s,
                     ["%d ÷ %d = %d km in one hour." % (s * h, h, s)],
                     unit="km")

    def speed_forward():
        s = random.randint(30, 90)
        h1 = random.randint(2, 5)
        h2 = h1 + random.randint(1, 4)
        return _numq("A train travels %d km in %d hours at a steady speed. How "
                     "far does the train travel in %d hours, in kilometres?"
                     % (s * h1, h1, h2), s * h2,
                     ["%d ÷ %d = %d km each hour." % (s * h1, h1, s),
                      "%d × %d = %d km." % (s, h2, s * h2)], unit="km")

    def machine_rate():
        per_min = random.randint(8, 40)
        m1 = random.randint(3, 9)
        m2 = m1 + random.randint(2, 10)
        return _numq("A machine fills %d bottles in %d minutes at a steady "
                     "rate. How many bottles does the machine fill in %d "
                     "minutes?" % (per_min * m1, m1, m2), per_min * m2,
                     ["%d ÷ %d = %d bottles each minute."
                      % (per_min * m1, m1, per_min),
                      "%d × %d = %d bottles." % (per_min, m2, per_min * m2)],
                     unit="bottles")

    def best_value_letter():
        u1 = random.randint(4, 30)
        u2 = u1 + random.randint(1, 8)
        n1 = random.randint(3, 12)
        n2 = random.randint(3, 12)
        while n2 == n1:
            n2 = random.randint(3, 12)
        cheaper = pick(["A", "B"])
        if cheaper == "A":
            ua, ub = u1, u2
        else:
            ua, ub = u2, u1
        return _wordq("Pack A holds %d %s and costs %s. Pack B holds %d %s and "
                      "costs %s. Which pack is better value for money? Type A "
                      "or B." % (n1, plur, money(n1 * ua), n2, plur,
                                 money(n2 * ub)), cheaper,
                      ["Pack A: %d ÷ %d = %dp for one %s."
                       % (n1 * ua, n1, ua, sing),
                       "Pack B: %d ÷ %d = %dp for one %s."
                       % (n2 * ub, n2, ub, sing),
                       "Pack %s is cheaper for each %s." % (cheaper, sing)],
                      placeholder="A or B")

    def best_value_price():
        lo = random.randint(4, 30)
        hi = lo + random.randint(1, 10)
        n1 = random.randint(3, 12)
        n2 = random.randint(3, 12)
        while n2 == n1:
            n2 = random.randint(3, 12)
        cheaper = pick(["A", "B"])
        u1, u2 = (lo, hi) if cheaper == "A" else (hi, lo)
        return _numq("Pack A holds %d %s for %s. Pack B holds %d %s for %s. "
                     "What is the cost of one %s from the better-value pack, "
                     "in pence?" % (n1, plur, money(n1 * u1), n2, plur,
                                    money(n2 * u2), sing), lo,
                     ["Pack A: %d ÷ %d = %dp each." % (n1 * u1, n1, u1),
                      "Pack B: %d ÷ %d = %dp each." % (n2 * u2, n2, u2),
                      "Pack %s is better value at %dp each." % (cheaper, lo)],
                     unit="p")

    def price_table():
        rows = []
        each = random.randint(6, 45)
        counts = sorted(random.sample(range(2, 15), 4))
        i = random.randrange(4)
        for j, c in enumerate(counts):
            rows.append([str(c), "" if j == i else money(c * each)])
        return _dtq("This price table charges the same amount for every %s. "
                    "What is the missing price, in pence?" % sing,
                    ["Number of %s" % plur, "Price"], rows, counts[i] * each,
                    ["One %s costs %d ÷ %d = %dp."
                     % (sing, counts[(i + 1) % 4] * each, counts[(i + 1) % 4],
                        each),
                     "%d × %d = %dp." % (counts[i], each, counts[i] * each)],
                    missing=(i, 1), caption="Price list")

    def quantity_table():
        per = random.randint(4, 25)
        counts = sorted(random.sample(range(2, 12), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else str(c * per)]
                for j, c in enumerate(counts)]
        return _dtq("Every box holds the same number of tiles. How many tiles "
                    "are in %d boxes?" % counts[i],
                    ["Boxes", "Tiles"], rows, counts[i] * per,
                    ["One box holds %d tiles." % per,
                     "%d × %d = %d tiles." % (counts[i], per, counts[i] * per)],
                    missing=(i, 1), caption="Tiles in boxes")

    def paint_coverage():
        per_l = random.randint(6, 14)
        litres = random.randint(3, 9)
        return _numq("One litre of paint covers %d m² of wall. How many square "
                     "metres do %d litres cover?" % (per_l, litres),
                     per_l * litres,
                     ["%d × %d = %d m²." % (per_l, litres, per_l * litres)],
                     unit="m²")

    def paint_inverse():
        per_l = random.randint(5, 12)
        litres = random.randint(3, 9)
        return _numq("One litre of paint covers %d m². How many litres are "
                     "needed to cover %d m²?" % (per_l, per_l * litres), litres,
                     ["%d ÷ %d = %d litres." % (per_l * litres, per_l, litres)],
                     unit="litres")

    def exchange_rate():
        rate = pick([5, 6, 8, 10, 12])
        pounds = random.randint(3, 15)
        return _numq("At a fair, £1 buys %d tokens. How many tokens does %s "
                     "buy?" % (rate, _pounds(pounds)), rate * pounds,
                     ["%d × %d = %d tokens." % (rate, pounds, rate * pounds)],
                     unit="tokens")

    def bar_rate():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(4, 18) for _ in cats]
        i = random.randrange(4)
        each = random.randint(5, 40)
        return _barq("The chart shows how many %s were sold each day. Every %s "
                     "costs %dp. How much money was taken on %s, in pence?"
                     % (plur, sing, each, cats[i]), cats, vals,
                     vals[i] * each,
                     ["%s: %d %s sold." % (cats[i], vals[i], plur),
                      "%d × %d = %dp." % (vals[i], each, vals[i] * each)])

    opts = [unit_price, scale_up, recipe_scale, speed, machine_rate,
            best_value_letter, price_table, quantity_table, paint_coverage,
            bar_rate, how_many_for]
    if d == 0:
        opts = [unit_price, scale_up, how_many_for, recipe_scale,
                price_table, quantity_table, exchange_rate, bar_rate,
                paint_coverage]
    elif d == 2:
        opts = [scale_up, recipe_down, speed_forward, machine_rate,
                best_value_letter, best_value_price, paint_inverse,
                price_table, quantity_table, bar_rate, unit_price]
    opts = opts + [price_table, quantity_table, bar_rate, price_table]
    return pick(opts)()


# ================================================================= 6.7.e =====
@skill("Y6.7.e", "Scale factors and scale drawings", S7)
def _(d=1):
    d = _t(d)

    def drawing_to_real():
        rep = pick([2, 4, 5, 10, 20, 50])
        cm = random.randint(2, _by_d(d, 8, 12, 20))
        return _numq("On a plan, 1 cm represents %d m. A wall is drawn %d cm "
                     "long. How long is the real wall, in metres?" % (rep, cm),
                     rep * cm,
                     ["Each centimetre stands for %d m." % rep,
                      "%d × %d = %d m." % (cm, rep, rep * cm)], unit="m")

    def real_to_drawing():
        rep = pick([2, 4, 5, 10, 20, 25])
        cm = random.randint(2, _by_d(d, 8, 12, 18))
        return _numq("On a plan, 1 cm represents %d m. A path is %d m long in "
                     "real life. How long is the path on the plan, in "
                     "centimetres?" % (rep, rep * cm), cm,
                     ["%d ÷ %d = %d cm." % (rep * cm, rep, cm)], unit="cm")

    def map_km():
        rep = pick([2, 3, 5, 10])
        cm = random.randint(3, 12)
        return _numq("On a map, 1 cm represents %d km. Two towns are %d cm "
                     "apart on the map. What is the real distance between the "
                     "towns, in kilometres?" % (rep, cm), rep * cm,
                     ["%d × %d = %d km." % (cm, rep, rep * cm)], unit="km")

    def map_km_reverse():
        rep = pick([2, 4, 5, 10])
        cm = random.randint(3, 12)
        return _numq("On a map, 1 cm represents %d km. A river is %d km long. "
                     "How long is the river on the map, in centimetres?"
                     % (rep, rep * cm), cm,
                     ["%d ÷ %d = %d cm." % (rep * cm, rep, cm)], unit="cm")

    def enlarge_side():
        w = random.randint(3, 12)
        h = random.randint(3, 12)
        while h == w:
            h = random.randint(3, 12)
        k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
                  random.randint(4, 9))
        return _numq("A rectangle measures %d cm by %d cm. It is enlarged by a "
                     "scale factor of %d. How long is the longer side of the "
                     "new rectangle, in centimetres?" % (w, h, k),
                     max(w, h) * k,
                     ["The longer side is %d cm." % max(w, h),
                      "%d × %d = %d cm." % (max(w, h), k, max(w, h) * k)],
                     unit="cm")

    def find_scale_factor():
        w = random.randint(3, 12)
        k = random.randint(2, 8)
        return _numq("A shape with a side of %d cm is enlarged so that the same "
                     "side becomes %d cm. What is the scale factor of the "
                     "enlargement?" % (w, w * k), k,
                     ["%d ÷ %d = %d." % (w * k, w, k)],
                     placeholder="scale factor")

    def similar_missing():
        w = random.randint(2, 9)
        h = random.randint(2, 9)
        while h == w:
            h = random.randint(2, 9)
        k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
                  random.randint(3, 9))
        return _numq("Two rectangles are similar. The smaller one measures "
                     "%d cm by %d cm. The larger one has a shorter side of "
                     "%d cm. How long is the longer side of the larger "
                     "rectangle, in centimetres?"
                     % (w, h, min(w, h) * k), max(w, h) * k,
                     ["%d ÷ %d = %d, so the scale factor is %d."
                      % (min(w, h) * k, min(w, h), k, k),
                      "%d × %d = %d cm." % (max(w, h), k, max(w, h) * k)],
                     unit="cm")

    def similar_triangle():
        base = random.randint(2, 8)
        side = random.randint(3, 10)
        while side == base:
            side = random.randint(3, 10)
        k = random.randint(2, 6)
        return _numq("Two triangles are similar. In the small triangle the base "
                     "is %d cm and the slant side is %d cm. In the large "
                     "triangle the base is %d cm. How long is the slant side "
                     "of the large triangle, in centimetres?"
                     % (base, side, base * k), side * k,
                     ["%d ÷ %d = %d, so the scale factor is %d."
                      % (base * k, base, k, k),
                      "%d × %d = %d cm." % (side, k, side * k)], unit="cm")

    def perimeter_after():
        w = random.randint(2, 9)
        h = random.randint(2, 9)
        k = random.randint(2, 5)
        return _numq("A rectangle measures %d cm by %d cm. It is enlarged by a "
                     "scale factor of %d. What is the perimeter of the enlarged "
                     "rectangle, in centimetres?" % (w, h, k),
                     2 * (w + h) * k,
                     ["The enlarged rectangle is %d cm by %d cm."
                      % (w * k, h * k),
                      "Perimeter = 2 × (%d + %d) = %d cm."
                      % (w * k, h * k, 2 * (w + h) * k)], unit="cm")

    def model_ratio():
        k = pick([10, 20, 25, 50, 100])
        model_cm = random.randint(4, 20)
        return _numq("A model is built to a scale of 1 : %d. A part of the "
                     "model is %d cm long. How long is the real part, in "
                     "centimetres?" % (k, model_cm), k * model_cm,
                     ["A scale of 1 : %d means the real object is %d times as "
                      "long." % (k, k),
                      "%d × %d = %d cm." % (model_cm, k, k * model_cm)],
                     unit="cm")

    def model_ratio_reverse():
        k = pick([10, 20, 25, 50])
        model_cm = random.randint(3, 15)
        return _numq("A model is built to a scale of 1 : %d. The real object is "
                     "%d cm long. How long is the model, in centimetres?"
                     % (k, k * model_cm), model_cm,
                     ["%d ÷ %d = %d cm." % (k * model_cm, k, model_cm)],
                     unit="cm")

    def scale_table():
        rep = pick([2, 5, 10, 20])
        drawn = sorted(random.sample(range(1, 14), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else str(c * rep)]
                for j, c in enumerate(drawn)]
        return _dtq("This table converts lengths on a plan into real lengths. "
                    "1 cm on the plan represents %d m. What is the missing real "
                    "length, in metres?" % rep,
                    ["Plan (cm)", "Real (m)"], rows, drawn[i] * rep,
                    ["Each centimetre stands for %d m." % rep,
                     "%d × %d = %d m." % (drawn[i], rep, drawn[i] * rep)],
                    missing=(i, 1), caption="Plan of a school field")

    def scale_table_reverse():
        rep = pick([2, 5, 10, 25])
        drawn = sorted(random.sample(range(1, 12), 4))
        i = random.randrange(4)
        rows = [["" if j == i else str(c), str(c * rep)]
                for j, c in enumerate(drawn)]
        return _dtq("This table converts lengths on a plan into real lengths. "
                    "1 cm on the plan represents %d m. What is the missing plan "
                    "length, in centimetres?" % rep,
                    ["Plan (cm)", "Real (m)"], rows, drawn[i],
                    ["%d ÷ %d = %d cm." % (drawn[i] * rep, rep, drawn[i])],
                    missing=(i, 0), caption="Plan of a park")

    def area_enlarge():
        w = random.randint(2, 6)
        h = random.randint(2, 6)
        while h == w:
            h = random.randint(2, 6)
        k = random.randint(2, 4)
        return _numq("A rectangle measures %d cm by %d cm. Each side is "
                     "multiplied by a scale factor of %d. What is the area of "
                     "the new rectangle, in square centimetres?" % (w, h, k),
                     w * h * k * k,
                     ["The new rectangle is %d cm by %d cm." % (w * k, h * k),
                      "%d × %d = %d cm²." % (w * k, h * k, w * h * k * k)],
                     unit="cm²")

    def which_bigger():
        k = random.randint(2, 6)
        base = random.randint(3, 9)
        return _numq("A photograph %d cm wide is enlarged by a scale factor of "
                     "%d. How much wider is the enlarged photograph than the "
                     "original, in centimetres?" % (base, k), base * k - base,
                     ["The enlarged width is %d × %d = %d cm."
                      % (base, k, base * k),
                      "%d − %d = %d cm wider."
                      % (base * k, base, base * k - base)], unit="cm")

    opts = [drawing_to_real, real_to_drawing, map_km, enlarge_side,
            find_scale_factor, similar_missing, scale_table, model_ratio,
            perimeter_after, scale_table_reverse]
    if d == 0:
        opts = [drawing_to_real, real_to_drawing, map_km, enlarge_side,
                find_scale_factor, scale_table, scale_table_reverse,
                model_ratio]
    elif d == 2:
        opts = [similar_missing, similar_triangle, perimeter_after,
                area_enlarge, model_ratio_reverse, map_km_reverse,
                which_bigger, scale_table, scale_table_reverse, model_ratio]
    opts = opts + [scale_table, scale_table_reverse, scale_table]
    return pick(opts)()


# ================================================================= 6.7.f =====
@skill("Y6.7.f", "Use simple formulae", S7)
def _(d=1):
    d = _t(d)

    def perimeter_formula():
        l = random.randint(3, _by_d(d, 12, 25, 60))
        w = random.randint(2, _by_d(d, 10, 20, 45))
        return _numq("The perimeter of a rectangle is given by the formula "
                     "P = 2 × (l + w). Work out P when l = %d cm and w = %d cm."
                     % (l, w), 2 * (l + w),
                     ["l + w = %d + %d = %d." % (l, w, l + w),
                      "P = 2 × %d = %d cm." % (l + w, 2 * (l + w))], unit="cm")

    def area_rect_formula():
        l = random.randint(3, _by_d(d, 12, 25, 40))
        w = random.randint(2, _by_d(d, 10, 20, 30))
        return _numq("The area of a rectangle is given by A = l × w. Work out A "
                     "when l = %d cm and w = %d cm." % (l, w), l * w,
                     ["A = %d × %d = %d cm²." % (l, w, l * w)], unit="cm²")

    def triangle_formula():
        b = random.randint(2, 20) * 2
        h = random.randint(3, _by_d(d, 10, 18, 30))
        return _numq("The area of a triangle is given by A = (b × h) ÷ 2. Work "
                     "out A when b = %d cm and h = %d cm." % (b, h),
                     b * h // 2,
                     ["b × h = %d × %d = %d." % (b, h, b * h),
                      "A = %d ÷ 2 = %d cm²." % (b * h, b * h // 2)], unit="cm²")

    def volume_formula():
        l = random.randint(2, _by_d(d, 6, 10, 15))
        w = random.randint(2, _by_d(d, 6, 9, 12))
        h = random.randint(2, _by_d(d, 5, 8, 12))
        return _numq("The volume of a cuboid is given by V = l × w × h. Work "
                     "out V when l = %d cm, w = %d cm and h = %d cm."
                     % (l, w, h), l * w * h,
                     ["%d × %d = %d." % (l, w, l * w),
                      "V = %d × %d = %d cm³." % (l * w, h, l * w * h)],
                     unit="cm³")

    def cost_formula():
        a = random.randint(2, _by_d(d, 6, 9, 15))
        b = random.randint(1, _by_d(d, 8, 20, 45))
        n = random.randint(2, _by_d(d, 8, 15, 30))
        return _numq("The cost of hiring a bike is given by the formula "
                     "C = %dn + %d, where C is the cost in pounds and n is the "
                     "number of hours. Work out C when n = %d." % (a, b, n),
                     a * n + b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "C = %d + %d = %d." % (a * n, b, a * n + b)], unit="£")

    def cost_formula_inverse():
        a = random.randint(2, 9)
        b = random.randint(2, 20)
        n = random.randint(2, 12)
        return _numq("The cost of a taxi ride is C = %dm + %d, where C is the "
                     "cost in pounds and m is the number of miles. A ride costs "
                     "%s. How many miles was the ride?"
                     % (a, b, _pounds(a * n + b)), n,
                     ["%d − %d = %d." % (a * n + b, b, a * n),
                      "%d ÷ %d = %d miles." % (a * n, a, n)], unit="miles")

    def square_perimeter():
        s = random.randint(3, _by_d(d, 12, 25, 45))
        return _numq("The perimeter of a square is given by P = 4s. Work out P "
                     "when s = %d cm." % s, 4 * s,
                     ["P = 4 × %d = %d cm." % (s, 4 * s)], unit="cm")

    def square_perimeter_inverse():
        s = random.randint(3, 30)
        return _numq("The perimeter of a square is given by P = 4s. A square "
                     "has P = %d cm. What is s, in centimetres?" % (4 * s), s,
                     ["%d ÷ 4 = %d cm." % (4 * s, s)], unit="cm")

    def distance_formula():
        speed = random.randint(20, _by_d(d, 60, 90, 120))
        time = random.randint(2, _by_d(d, 5, 8, 12))
        return _numq("Distance is given by the formula d = s × t, where s is "
                     "speed in km/h and t is time in hours. Work out d when "
                     "s = %d and t = %d." % (speed, time), speed * time,
                     ["d = %d × %d = %d km." % (speed, time, speed * time)],
                     unit="km")

    def distance_inverse():
        speed = random.randint(20, 90)
        time = random.randint(2, 9)
        return _numq("Distance is given by d = s × t. A journey has d = %d km "
                     "and t = %d hours. What is the speed s, in km/h?"
                     % (speed * time, time), speed,
                     ["%d ÷ %d = %d km/h." % (speed * time, time, speed)],
                     unit="km/h")

    def formula_in_words():
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        n = random.randint(2, 15)
        return _numq("To find the number of chairs needed, multiply the number "
                     "of tables by %d and then add %d. How many chairs are "
                     "needed for %d tables?" % (a, b, n), a * n + b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "%d + %d = %d chairs." % (a * n, b, a * n + b)],
                     unit="chairs")

    def formula_table():
        a = random.randint(2, 8)
        b = random.randint(1, 15)
        ns = sorted(random.sample(range(1, 15), 4))
        i = random.randrange(4)
        rows = [[str(n), "" if j == i else str(a * n + b)]
                for j, n in enumerate(ns)]
        return _dtq("This table uses the formula C = %dn + %d. What is the "
                    "missing value of C?" % (a, b), ["n", "C"], rows,
                    a * ns[i] + b,
                    ["C = %d × %d + %d." % (a, ns[i], b),
                     "C = %d + %d = %d." % (a * ns[i], b, a * ns[i] + b)],
                    missing=(i, 1), caption="C = %dn + %d" % (a, b))

    def formula_io():
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        ns = sorted(random.sample(range(1, 20), 4))
        rows = [[n, a * n + b] for n in ns]
        i = random.randrange(4)
        return _ioq("This table uses the formula y = %dx + %d. Type the missing "
                    "Out number." % (a, b), rows, i, rows[i][1],
                    ["y = %d × %d + %d = %d."
                     % (a, ns[i], b, a * ns[i] + b)],
                    rule="y = %dx + %d" % (a, b))

    def two_substitutions():
        a = random.randint(2, 9)
        b = random.randint(1, 15)
        n1 = random.randint(2, 8)
        n2 = n1 + random.randint(1, 8)
        return _numq("The formula T = %dn + %d gives the total. What is the "
                     "difference between T when n = %d and T when n = %d?"
                     % (a, b, n2, n1), a * (n2 - n1),
                     ["When n = %d, T = %d." % (n2, a * n2 + b),
                      "When n = %d, T = %d." % (n1, a * n1 + b),
                      "%d − %d = %d." % (a * n2 + b, a * n1 + b,
                                         a * (n2 - n1))])

    def subtract_formula():
        a = random.randint(2, 9)
        n = random.randint(3, 15)
        b = random.randint(1, a * n - 1)
        return _numq("The formula L = %dn − %d gives the length in centimetres. "
                     "Work out L when n = %d." % (a, b, n), a * n - b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "L = %d − %d = %d cm." % (a * n, b, a * n - b)],
                     unit="cm")

    def divide_formula():
        a = pick([2, 3, 4, 5, 6])
        q = random.randint(2, 20)
        b = random.randint(1, 15)
        return _numq("The formula S = n ÷ %d + %d is used to work out a score. "
                     "Work out S when n = %d." % (a, b, a * q), q + b,
                     ["%d ÷ %d = %d." % (a * q, a, q),
                      "S = %d + %d = %d." % (q, b, q + b)])

    opts = [perimeter_formula, area_rect_formula, cost_formula, square_perimeter,
            distance_formula, formula_in_words, formula_table, formula_io,
            volume_formula, triangle_formula]
    if d == 0:
        opts = [perimeter_formula, area_rect_formula, square_perimeter,
                cost_formula, formula_in_words, formula_table, formula_io,
                distance_formula]
    elif d == 2:
        opts = [triangle_formula, volume_formula, cost_formula_inverse,
                square_perimeter_inverse, distance_inverse, two_substitutions,
                subtract_formula, divide_formula, formula_table, formula_io]
    opts = opts + [formula_table, formula_io, formula_table]
    return pick(opts)()


# ================================================================= 6.7.g =====
@skill("Y6.7.g", "Write and evaluate algebraic expressions", S7)
def _(d=1):
    d = _t(d)
    v = pick(["n", "x", "a", "y", "m"])

    def evaluate_linear():
        a = random.randint(2, _by_d(d, 6, 9, 12))
        b = random.randint(1, _by_d(d, 10, 25, 60))
        n = random.randint(2, _by_d(d, 9, 15, 30))
        return _numq("Work out the value of %d%s + %d when %s = %d."
                     % (a, v, b, v, n), a * n + b,
                     ["%d%s means %d × %s." % (a, v, a, v),
                      "%d × %d = %d." % (a, n, a * n),
                      "%d + %d = %d." % (a * n, b, a * n + b)])

    def evaluate_subtract():
        a = random.randint(2, _by_d(d, 6, 9, 12))
        n = random.randint(3, _by_d(d, 9, 15, 25))
        b = random.randint(1, a * n - 1)
        return _numq("Work out the value of %d%s − %d when %s = %d."
                     % (a, v, b, v, n), a * n - b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "%d − %d = %d." % (a * n, b, a * n - b)])

    def evaluate_divide():
        a = pick([2, 3, 4, 5, 6, 8])
        q = random.randint(2, _by_d(d, 8, 15, 25))
        b = random.randint(1, 20)
        return _numq("Work out the value of %s ÷ %d + %d when %s = %d."
                     % (v, a, b, v, a * q), q + b,
                     ["%d ÷ %d = %d." % (a * q, a, q),
                      "%d + %d = %d." % (q, b, q + b)])

    def evaluate_brackets():
        a = random.randint(2, _by_d(d, 4, 7, 10))
        b = random.randint(1, _by_d(d, 6, 12, 25))
        n = random.randint(2, _by_d(d, 8, 14, 25))
        return _numq("Work out the value of %d(%s + %d) when %s = %d."
                     % (a, v, b, v, n), a * (n + b),
                     ["Brackets first: %d + %d = %d." % (n, b, n + b),
                      "%d × %d = %d." % (a, n + b, a * (n + b))])

    def evaluate_two_vars():
        a = random.randint(2, _by_d(d, 5, 8, 11))
        b = random.randint(2, _by_d(d, 5, 8, 11))
        x = random.randint(2, _by_d(d, 8, 12, 20))
        y = random.randint(2, _by_d(d, 8, 12, 20))
        return _numq("Work out the value of %dx + %dy when x = %d and y = %d."
                     % (a, b, x, y), a * x + b * y,
                     ["%d × %d = %d and %d × %d = %d."
                      % (a, x, a * x, b, y, b * y),
                      "%d + %d = %d." % (a * x, b * y, a * x + b * y)])

    def phrase_more_than():
        b = random.randint(3, _by_d(d, 15, 40, 90))
        n = random.randint(2, _by_d(d, 12, 30, 80))
        return _numq("An expression for '%d more than %s' is %s + %d. What is "
                     "the value of this expression when %s = %d?"
                     % (b, v, v, b, v, n), n + b,
                     ["%d + %d = %d." % (n, b, n + b)])

    def phrase_less_than():
        n = random.randint(10, _by_d(d, 30, 70, 150))
        b = random.randint(2, n - 1)
        return _numq("An expression for '%d less than %s' is %s − %d. What is "
                     "the value of this expression when %s = %d?"
                     % (b, v, v, b, v, n), n - b,
                     ["%d − %d = %d." % (n, b, n - b)])

    def phrase_times():
        a = random.randint(2, 12)
        n = random.randint(2, _by_d(d, 10, 20, 40))
        return _numq("An expression for '%s multiplied by %d' is %d%s. What is "
                     "the value of this expression when %s = %d?"
                     % (v, a, a, v, v, n), a * n,
                     ["%d × %d = %d." % (a, n, a * n)])

    def word_expression():
        who = pick(NAMES)
        each = random.randint(2, 9)
        extra = random.randint(1, 20)
        n = random.randint(3, 15)
        return _numq("%s buys %s bags of marbles with %d marbles in each bag, "
                     "and %d loose marbles. The total is %d%s + %d marbles. How "
                     "many marbles is that when %s = %d?"
                     % (who, v, each, extra, each, v, extra, v, n),
                     each * n + extra,
                     ["%d × %d = %d marbles in the bags." % (each, n, each * n),
                      "%d + %d = %d marbles." % (each * n, extra,
                                                 each * n + extra)],
                     unit="marbles")

    def perimeter_expression():
        a = random.randint(2, 8)
        b = random.randint(1, 15)
        n = random.randint(2, 12)
        return _numq("The perimeter of a shape is given by the expression "
                     "%d%s + %d centimetres. What is the perimeter when "
                     "%s = %d?" % (a, v, b, v, n), a * n + b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "%d + %d = %d cm." % (a * n, b, a * n + b)], unit="cm")

    def coefficient():
        a = random.randint(2, 12)
        b = random.randint(1, 20)
        return _numq("In the expression %d%s + %d, what is the coefficient of "
                     "%s (the number that %s is multiplied by)?"
                     % (a, v, b, v, v), a,
                     ["%d%s means %d × %s, so the coefficient is %d."
                      % (a, v, a, v, a)], placeholder="a number")

    def like_terms():
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        return _numq("Simplify %d%s + %d%s by collecting like terms. The answer "
                     "is ___%s — type the number that goes in the blank."
                     % (a, v, b, v, v), a + b,
                     ["%d lots of %s plus %d lots of %s is %d lots of %s."
                      % (a, v, b, v, a + b, v)], placeholder="a number")

    def like_terms_subtract():
        a = random.randint(5, 14)
        b = random.randint(1, a - 1)
        return _numq("Simplify %d%s − %d%s. The answer is ___%s — type the "
                     "number that goes in the blank." % (a, v, b, v, v), a - b,
                     ["%d − %d = %d, so the answer is %d%s."
                      % (a, b, a - b, a - b, v)], placeholder="a number")

    def expression_table():
        a = random.randint(2, 8)
        b = random.randint(1, 15)
        xs = sorted(random.sample(range(1, 16), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(a * x + b)]
                for j, x in enumerate(xs)]
        return _dtq("This table shows the value of the expression %dx + %d for "
                    "different values of x. What is the missing value?" % (a, b),
                    ["x", "%dx + %d" % (a, b)], rows, a * xs[i] + b,
                    ["%d × %d = %d." % (a, xs[i], a * xs[i]),
                     "%d + %d = %d." % (a * xs[i], b, a * xs[i] + b)],
                    missing=(i, 1), caption="Values of %dx + %d" % (a, b))

    def expression_io():
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        xs = sorted(random.sample(range(1, 20), 4))
        rows = [[x, a * x + b] for x in xs]
        i = random.randrange(4)
        return _ioq("Every Out number is worked out with the expression "
                    "%dx + %d. Type the missing Out number." % (a, b), rows, i,
                    rows[i][1],
                    ["%d × %d + %d = %d." % (a, xs[i], b, a * xs[i] + b)],
                    rule="%dx + %d" % (a, b))

    def squared():
        n = random.randint(2, _by_d(d, 6, 9, 12))
        b = random.randint(1, 20)
        return _numq("Work out the value of %s² + %d when %s = %d."
                     % (v, b, v, n), n * n + b,
                     ["%s² means %d × %d = %d." % (v, n, n, n * n),
                      "%d + %d = %d." % (n * n, b, n * n + b)])

    def compare_expressions():
        a = random.randint(2, 7)
        b = random.randint(2, 7)
        while b == a:
            b = random.randint(2, 7)
        c = random.randint(1, 15)
        n = random.randint(3, 12)
        v1, v2 = a * n + c, b * n
        return _numq("When %s = %d, work out the difference between %d%s + %d "
                     "and %d%s." % (v, n, a, v, c, b, v), abs(v1 - v2),
                     ["%d%s + %d = %d." % (a, v, c, v1),
                      "%d%s = %d." % (b, v, v2),
                      "%d − %d = %d." % (max(v1, v2), min(v1, v2),
                                         abs(v1 - v2))])

    def property_addition():
        """Properties of addition (commutative / associative / identity) with
        a variable."""
        b = random.randint(2, _by_d(d, 9, 20, 50))
        c = random.randint(2, _by_d(d, 9, 20, 50))
        kind = pick(["identity", "commutative", "associative", "name_comm",
                     "name_ident"])
        if kind == "identity":
            return _wordq("The identity property of addition says that adding "
                          "zero leaves a number unchanged. Complete this "
                          "statement for the variable %s:   %s + 0 = ___   "
                          "Type the missing expression." % (v, v), v,
                          ["Adding 0 changes nothing.",
                           "So %s + 0 = %s." % (v, v)],
                          placeholder="an expression")
        if kind == "commutative":
            return _wordq("The commutative property of addition says that the "
                          "order of the two numbers being added does not change "
                          "the total. Complete this statement:   %s + %d = %d "
                          "+ ___   Type the missing expression."
                          % (v, b, b), v,
                          ["Swapping the order keeps the same total.",
                           "So the missing expression is %s." % v],
                          placeholder="an expression")
        if kind == "associative":
            return _numq("The associative property of addition lets you regroup "
                         "the numbers being added:   (%s + %d) + %d = %s + ___  "
                         " Type the missing number." % (v, b, c, v), b + c,
                         ["Add %d and %d first." % (b, c),
                          "%d + %d = %d." % (b, c, b + c)],
                         placeholder="a number")
        if kind == "name_comm":
            return _wordq("Properties of addition also work with variables. "
                          "Which property of addition is shown by the "
                          "statement %s + %d = %d + %s, where %s is a "
                          "variable? Type commutative, associative or "
                          "identity." % (v, b, b, v, v),
                          "commutative",
                          ["Only the order of the two numbers has changed.",
                           "That is the commutative property of addition."],
                          placeholder="type the word")
        return _wordq("Properties of addition also work with variables. Which "
                      "property of addition is shown by the statement "
                      "%s + 0 = %s, where %s is a variable? Type commutative, "
                      "associative or identity." % (v, v, v), "identity",
                      ["Adding zero leaves the variable unchanged.",
                       "That is the identity property of addition."],
                      placeholder="type the word")

    def property_multiplication():
        """Properties of multiplication (commutative / associative / identity /
        distributive) with a variable."""
        b = random.randint(2, _by_d(d, 6, 9, 12))
        c = random.randint(2, _by_d(d, 6, 9, 12))
        kind = pick(["identity", "commutative", "associative", "distributive",
                     "name_comm", "name_dist"])
        if kind == "identity":
            return _wordq("The identity property of multiplication says that "
                          "multiplying by one leaves a number unchanged. "
                          "Complete this statement for the variable %s:   %s × "
                          "1 = ___   Type the missing expression." % (v, v), v,
                          ["Multiplying by 1 changes nothing.",
                           "So %s × 1 = %s." % (v, v)],
                          placeholder="an expression")
        if kind == "commutative":
            return _numq("The commutative property of multiplication says that "
                         "the order of the two factors does not change the "
                         "product. Complete this statement:   %d × %s = %s × "
                         "___   Type the missing number." % (b, v, v), b,
                         ["Swapping the factors keeps the same product.",
                          "So %d × %s = %s × %d." % (b, v, v, b)],
                         placeholder="a number")
        if kind == "associative":
            return _numq("The associative property of multiplication lets you "
                         "regroup the factors:   (%s × %d) × %d = %s × ___   "
                         "Type the missing number." % (v, b, c, v), b * c,
                         ["Multiply %d and %d first." % (b, c),
                          "%d × %d = %d." % (b, c, b * c)],
                         placeholder="a number")
        if kind == "distributive":
            return _numq("The distributive property of multiplication says "
                         "%d(%s + %d) = %d%s + ___   Type the missing number."
                         % (b, v, c, b, v), b * c,
                         ["Multiply %d by each term inside the brackets."
                          % b,
                          "%d × %d = %d." % (b, c, b * c)],
                         placeholder="a number")
        if kind == "name_comm":
            return _wordq("Properties of multiplication also work with "
                          "variables. Which property of multiplication is shown "
                          "by the statement %d × %s = %s × %d, where %s is a "
                          "variable? Type commutative, associative, identity or "
                          "distributive." % (b, v, v, b, v), "commutative",
                          ["Only the order of the two factors has changed.",
                           "That is the commutative property of "
                           "multiplication."], placeholder="type the word")
        return _wordq("Properties of multiplication also work with variables. "
                      "Which property of multiplication is shown by the "
                      "statement %d(%s + %d) = %d%s + %d, where %s is a "
                      "variable? Type commutative, associative, identity or "
                      "distributive." % (b, v, c, b, v, b * c, v),
                      "distributive",
                      ["The %d has been multiplied by each term inside the "
                       "brackets." % b,
                       "That is the distributive property."],
                      placeholder="type the word")

    def bar_model_expression():
        """Identify equivalent expressions using bar models (strip_model)."""
        parts = random.randint(3, _by_d(d, 4, 6, 8))
        n = random.randint(2, _by_d(d, 8, 12, 20))
        if d == 2 and random.random() < 0.5:
            k = random.randint(2, 4)
            return _total_strip(
                "Bar models can show equivalent expressions. This bar model "
                "is made of %d equal parts and every part is labelled %d%s. "
                "Identify the equivalent expression for the "
                "whole bar, then type the value of that expression when "
                "%s = %d."
                % (parts, k, v, v, n),
                parts, "%d%s" % (k, v), parts * k * n,
                ["%d equal parts of %d%s is the expression %d%s."
                 % (parts, k, v, parts * k, v),
                 "%d × %d = %d." % (parts * k, n, parts * k * n)])
        return _total_strip(
            "Bar models can show equivalent expressions. This bar model is "
            "made of %d equal parts and every part is labelled %s. Identify "
            "the equivalent expression for the whole bar, "
            "then type the value of that expression when %s = %d."
            % (parts, v, v, n),
            parts, v, parts * n,
            ["%d equal parts of %s is the expression %d%s."
             % (parts, v, parts, v),
             "%d × %d = %d." % (parts, n, parts * n)])

    opts = [evaluate_linear, evaluate_subtract, evaluate_brackets,
            evaluate_two_vars, phrase_more_than, phrase_times, word_expression,
            expression_table, expression_io, coefficient, like_terms,
            property_addition, property_multiplication, bar_model_expression]
    if d == 0:
        opts = [evaluate_linear, phrase_more_than, phrase_less_than,
                phrase_times, coefficient, like_terms, expression_table,
                expression_io, perimeter_expression, property_addition,
                property_multiplication, bar_model_expression]
    elif d == 2:
        opts = [evaluate_brackets, evaluate_two_vars, evaluate_divide,
                squared, compare_expressions, like_terms_subtract,
                word_expression, expression_table, expression_io,
                evaluate_subtract, property_addition, property_multiplication,
                bar_model_expression]
    opts = opts + [expression_table, expression_io, expression_table,
                   bar_model_expression]
    return pick(opts)()


# ================================================================= 6.7.h =====
@skill("Y6.7.h", "Solve one-step equations", S7)
def _(d=1):
    d = _t(d)
    v = pick(["x", "n", "a", "y", "p"])

    def add_equation():
        x = random.randint(2, _by_d(d, 15, 40, 120))
        b = random.randint(2, _by_d(d, 15, 45, 150))
        return _numq("Solve the equation:  %s + %d = %d" % (v, b, x + b), x,
                     ["Subtract %d from both sides." % b,
                      "%d − %d = %d, so %s = %d." % (x + b, b, x, v, x)],
                     placeholder="%s = ?" % v)

    def add_equation_flipped():
        x = random.randint(2, _by_d(d, 15, 40, 120))
        b = random.randint(2, _by_d(d, 15, 45, 150))
        return _numq("Solve the equation:  %d + %s = %d" % (b, v, x + b), x,
                     ["Subtract %d from both sides." % b,
                      "%d − %d = %d, so %s = %d." % (x + b, b, x, v, x)],
                     placeholder="%s = ?" % v)

    def add_equation_right():
        x = random.randint(2, _by_d(d, 15, 40, 100))
        b = random.randint(2, _by_d(d, 15, 45, 120))
        return _numq("Solve the equation:  %d = %s + %d" % (x + b, v, b), x,
                     ["Subtract %d from both sides." % b,
                      "%d − %d = %d, so %s = %d." % (x + b, b, x, v, x)],
                     placeholder="%s = ?" % v)

    def subtract_equation():
        x = random.randint(2, _by_d(d, 20, 60, 150))
        b = random.randint(2, _by_d(d, 15, 45, 120))
        return _numq("Solve the equation:  %s − %d = %d" % (v, b, x), x + b,
                     ["Add %d to both sides." % b,
                      "%d + %d = %d, so %s = %d." % (x, b, x + b, v, x + b)],
                     placeholder="%s = ?" % v)

    def subtract_from():
        x = random.randint(2, _by_d(d, 15, 40, 90))
        b = x + random.randint(2, _by_d(d, 20, 50, 120))
        return _numq("Solve the equation:  %d − %s = %d" % (b, v, b - x), x,
                     ["%s = %d − %d." % (v, b, b - x),
                      "%s = %d." % (v, x)], placeholder="%s = ?" % v)

    def multiply_equation():
        a = random.randint(2, _by_d(d, 6, 9, 12))
        x = random.randint(2, _by_d(d, 10, 20, 45))
        return _numq("Solve the equation:  %d%s = %d" % (a, v, a * x), x,
                     ["%d%s means %d × %s." % (a, v, a, v),
                      "Divide both sides by %d: %d ÷ %d = %d."
                      % (a, a * x, a, x)], placeholder="%s = ?" % v)

    def multiply_equation_dot():
        a = random.randint(2, _by_d(d, 6, 9, 12))
        x = random.randint(2, _by_d(d, 10, 20, 45))
        return _numq("Solve the equation:  %s × %d = %d" % (v, a, a * x), x,
                     ["Divide both sides by %d." % a,
                      "%d ÷ %d = %d, so %s = %d." % (a * x, a, x, v, x)],
                     placeholder="%s = ?" % v)

    def divide_equation():
        a = random.randint(2, _by_d(d, 6, 9, 12))
        q = random.randint(2, _by_d(d, 10, 20, 40))
        return _numq("Solve the equation:  %s ÷ %d = %d" % (v, a, q), a * q,
                     ["Multiply both sides by %d." % a,
                      "%d × %d = %d, so %s = %d." % (q, a, a * q, v, a * q)],
                     placeholder="%s = ?" % v)

    def divide_into():
        x = random.randint(2, 12)
        q = random.randint(2, 12)
        return _numq("Solve the equation:  %d ÷ %s = %d" % (x * q, v, q), x,
                     ["%s = %d ÷ %d." % (v, x * q, q),
                      "%s = %d." % (v, x)], placeholder="%s = ?" % v)

    def fraction_form():
        a = random.randint(2, 9)
        q = random.randint(2, 20)
        return _numq("Solve the equation:  %s/%d = %d" % (v, a, q), a * q,
                     ["%s/%d means %s ÷ %d." % (v, a, v, a),
                      "Multiply both sides by %d: %d × %d = %d."
                      % (a, q, a, a * q)], placeholder="%s = ?" % v)

    def check_solution():
        a = random.randint(2, 9)
        x = random.randint(2, 15)
        if random.random() < 0.5:
            return _wordq("Is %s = %d a solution of the equation %d%s = %d? "
                          "Type yes or no." % (v, x, a, v, a * x), "yes",
                          ["%d × %d = %d." % (a, x, a * x),
                           "The equation is true, so %s = %d is a solution."
                           % (v, x)], placeholder="yes or no")
        wrong = x + pick([-2, -1, 1, 2])
        if wrong < 1:
            wrong = x + 2
        return _wordq("Is %s = %d a solution of the equation %d%s = %d? Type "
                      "yes or no." % (v, wrong, a, v, a * x), "no",
                      ["%d × %d = %d, not %d." % (a, wrong, a * wrong, a * x),
                       "So %s = %d is not a solution." % (v, wrong)],
                      placeholder="yes or no")

    def check_solution_add():
        b = random.randint(3, 30)
        x = random.randint(2, 40)
        wrong = x + pick([-3, -2, 2, 3])
        if wrong < 1:
            wrong = x + 3
        if random.random() < 0.5:
            return _wordq("Is %s = %d a solution of the equation %s + %d = %d? "
                          "Type yes or no." % (v, x, v, b, x + b), "yes",
                          ["%d + %d = %d ✓." % (x, b, x + b)],
                          placeholder="yes or no")
        return _wordq("Is %s = %d a solution of the equation %s + %d = %d? Type "
                      "yes or no." % (v, wrong, v, b, x + b), "no",
                      ["%d + %d = %d, not %d." % (wrong, b, wrong + b, x + b),
                       "So %s = %d is not a solution." % (v, wrong)],
                      placeholder="yes or no")

    def word_equation_add():
        who = pick(NAMES)
        x = random.randint(5, 60)
        b = random.randint(3, 40)
        return _numq("%s has %s stickers and is given %d more, making %d "
                     "altogether. The equation is %s + %d = %d. Solve it to "
                     "find %s." % (who, v, b, x + b, v, b, x + b, v), x,
                     ["%d − %d = %d." % (x + b, b, x),
                      "%s = %d." % (v, x)], placeholder="%s = ?" % v)

    def word_equation_mult():
        who = pick(NAMES)
        a = random.randint(3, 9)
        x = random.randint(3, 20)
        return _numq("%s packs %d boxes, each with %s pencils, and uses %d "
                     "pencils in total. The equation is %d%s = %d. Solve it to "
                     "find %s." % (who, a, v, a * x, a, v, a * x, v), x,
                     ["%d ÷ %d = %d." % (a * x, a, x),
                      "%s = %d." % (v, x)], placeholder="%s = ?" % v)

    def strip_equation():
        a = random.randint(2, 8)
        x = random.randint(3, 20)
        return _share_strip("This bar model shows the equation %d%s = %d. The "
                            "whole bar is %d and it is split into %d equal "
                            "parts. What is the value of %s?"
                            % (a, v, a * x, a * x, a, v), a, str(a * x), x,
                            ["Each part of the bar is worth %s." % v,
                             "%d ÷ %d = %d, so %s = %d."
                             % (a * x, a, x, v, x)])

    def strip_equation_total():
        a = random.randint(2, 8)
        x = random.randint(3, 20)
        return _total_strip("This bar model has %d equal parts and each part is "
                            "worth %d. If %s stands for the whole bar, what is "
                            "the value of %s?" % (a, x, v, v), a, str(x),
                            a * x,
                            ["%d × %d = %d." % (a, x, a * x),
                             "%s = %d." % (v, a * x)])

    def equation_table():
        a = random.randint(2, 8)
        b = random.randint(1, 15)
        xs = sorted(random.sample(range(1, 16), 4))
        i = random.randrange(4)
        rows = [["" if j == i else str(x), str(a * x + b)]
                for j, x in enumerate(xs)]
        return _dtq("Every row of this table fits the rule %dx + %d = y. What "
                    "value of x is missing?" % (a, b), ["x", "y"], rows, xs[i],
                    ["%d − %d = %d." % (a * xs[i] + b, b, a * xs[i]),
                     "%d ÷ %d = %d." % (a * xs[i], a, xs[i])],
                    missing=(i, 0), caption="%dx + %d = y" % (a, b))

    def one_step_add_sub():
        """Solve one-step addition and subtraction equations with whole
        numbers."""
        x = random.randint(2, _by_d(d, 15, 40, 120))
        b = random.randint(2, _by_d(d, 15, 45, 150))
        if random.random() < 0.5:
            return _numq("One-step equations with whole numbers are solved by "
                         "addition or subtraction. Solve this one-step addition "
                         "equation:   %s + %d = %d   Type the value of %s."
                         % (v, b, x + b, v), x,
                         ["Addition is undone by subtraction.",
                          "%d − %d = %d, so %s = %d." % (x + b, b, x, v, x)],
                         placeholder="%s = ?" % v)
        return _numq("One-step equations with whole numbers are solved by "
                     "addition or subtraction. Solve this one-step subtraction "
                     "equation:   %s − %d = %d   Type the value of %s."
                     % (v, b, x, v), x + b,
                     ["Subtraction is undone by addition.",
                      "%d + %d = %d, so %s = %d." % (x, b, x + b, v, x + b)],
                     placeholder="%s = ?" % v)

    def one_step_mult_div():
        """Solve one-step multiplication and division equations with whole
        numbers."""
        a = random.randint(2, _by_d(d, 6, 9, 12))
        q = random.randint(2, _by_d(d, 10, 20, 45))
        if random.random() < 0.5:
            return _numq("One-step equations with whole numbers are solved by "
                         "multiplication or division. Solve this one-step "
                         "multiplication equation:   %d%s = %d   Type the value "
                         "of %s."
                         % (a, v, a * q, v), q,
                         ["%d%s means %d × %s." % (a, v, a, v),
                          "Multiplication is undone by division: %d ÷ %d = %d."
                          % (a * q, a, q)], placeholder="%s = ?" % v)
        return _numq("One-step equations with whole numbers are solved by "
                     "multiplication or division. Solve this one-step division "
                     "equation:   %s ÷ %d = %d   Type the value of %s."
                     % (v, a, q, v), a * q,
                     ["Division is undone by multiplication.",
                      "%d × %d = %d, so %s = %d." % (q, a, a * q, v, a * q)],
                     placeholder="%s = ?" % v)

    opts = [add_equation, subtract_equation, multiply_equation, divide_equation,
            add_equation_right, strip_equation, word_equation_add,
            word_equation_mult, equation_table, check_solution,
            one_step_add_sub, one_step_mult_div]
    if d == 0:
        opts = [add_equation, add_equation_flipped, subtract_equation,
                multiply_equation, divide_equation, strip_equation,
                strip_equation_total, word_equation_add, equation_table,
                one_step_add_sub, one_step_mult_div]
    elif d == 2:
        opts = [subtract_from, divide_into, fraction_form, multiply_equation_dot,
                check_solution, check_solution_add, add_equation_right,
                word_equation_mult, equation_table, strip_equation,
                one_step_add_sub, one_step_mult_div]
    opts = opts + [strip_equation, equation_table, strip_equation_total,
                   equation_table]
    return pick(opts)()


# ================================================================= 6.7.i =====
@skill("Y6.7.i", "Pairs of values satisfying a two-variable equation", S7)
def _(d=1):
    d = _t(d)

    def sum_pair():
        s = _by_d(d, random.randint(8, 20), random.randint(15, 60),
                  random.randint(40, 150))
        x = random.randint(1, s - 1)
        return _numq("x + y = %d. If x = %d, what is the value of y?" % (s, x),
                     s - x,
                     ["%d − %d = %d." % (s, x, s - x),
                      "y = %d." % (s - x)], placeholder="y = ?")

    def sum_pair_x():
        s = _by_d(d, random.randint(8, 20), random.randint(15, 60),
                  random.randint(40, 150))
        y = random.randint(1, s - 1)
        return _numq("x + y = %d. If y = %d, what is the value of x?" % (s, y),
                     s - y,
                     ["%d − %d = %d." % (s, y, s - y),
                      "x = %d." % (s - y)], placeholder="x = ?")

    def linear_y():
        a = random.randint(2, _by_d(d, 4, 7, 10))
        b = random.randint(1, _by_d(d, 8, 20, 40))
        x = random.randint(1, _by_d(d, 8, 12, 25))
        return _numq("y = %dx + %d. What is the value of y when x = %d?"
                     % (a, b, x), a * x + b,
                     ["%d × %d = %d." % (a, x, a * x),
                      "y = %d + %d = %d." % (a * x, b, a * x + b)],
                     placeholder="y = ?")

    def linear_x():
        a = random.randint(2, _by_d(d, 4, 7, 9))
        b = random.randint(1, _by_d(d, 8, 20, 40))
        x = random.randint(1, _by_d(d, 8, 12, 25))
        return _numq("y = %dx + %d. What is the value of x when y = %d?"
                     % (a, b, a * x + b), x,
                     ["%d − %d = %d." % (a * x + b, b, a * x),
                      "%d ÷ %d = %d, so x = %d." % (a * x, a, x, x)],
                     placeholder="x = ?")

    def two_term_equation():
        a = random.randint(2, _by_d(d, 4, 6, 9))
        x = random.randint(1, _by_d(d, 6, 10, 18))
        y = random.randint(1, _by_d(d, 10, 25, 50))
        return _numq("%dx + y = %d. What is the value of y when x = %d?"
                     % (a, a * x + y, x), y,
                     ["%d × %d = %d." % (a, x, a * x),
                      "%d − %d = %d, so y = %d."
                      % (a * x + y, a * x, y, y)], placeholder="y = ?")

    def double_equation():
        y = random.randint(2, _by_d(d, 10, 25, 60))
        k = random.randint(2, _by_d(d, 4, 6, 9))
        return _numq("x = %dy. What is the value of x when y = %d?" % (k, y),
                     k * y,
                     ["x = %d × %d = %d." % (k, y, k * y)],
                     placeholder="x = ?")

    def table_missing_y():
        a = random.randint(2, _by_d(d, 4, 6, 9))
        b = random.randint(0, _by_d(d, 6, 15, 30))
        xs = sorted(random.sample(range(1, 13), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(a * x + b)]
                for j, x in enumerate(xs)]
        eq = "y = %dx + %d" % (a, b) if b else "y = %dx" % a
        return _dtq("This table of (x, y) pairs fits the equation %s. What is "
                    "the missing value of y?" % eq, ["x", "y"], rows,
                    a * xs[i] + b,
                    ["%d × %d = %d." % (a, xs[i], a * xs[i]),
                     "y = %d." % (a * xs[i] + b)],
                    missing=(i, 1), caption=eq)

    def table_missing_x():
        a = random.randint(2, _by_d(d, 4, 6, 9))
        b = random.randint(0, _by_d(d, 6, 15, 30))
        xs = sorted(random.sample(range(1, 13), 4))
        i = random.randrange(4)
        rows = [["" if j == i else str(x), str(a * x + b)]
                for j, x in enumerate(xs)]
        eq = "y = %dx + %d" % (a, b) if b else "y = %dx" % a
        return _dtq("This table of (x, y) pairs fits the equation %s. What is "
                    "the missing value of x?" % eq, ["x", "y"], rows, xs[i],
                    ["%d − %d = %d." % (a * xs[i] + b, b, a * xs[i]),
                     "%d ÷ %d = %d." % (a * xs[i], a, xs[i])],
                    missing=(i, 0), caption=eq)

    def table_sum():
        s = random.randint(10, 30)
        xs = sorted(random.sample(range(1, s), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(s - x)]
                for j, x in enumerate(xs)]
        return _dtq("Every (x, y) pair in this table fits x + y = %d. What is "
                    "the missing value of y?" % s, ["x", "y"], rows,
                    s - xs[i],
                    ["%d − %d = %d." % (s, xs[i], s - xs[i])],
                    missing=(i, 1), caption="x + y = %d" % s)

    def plot_point():
        a = random.randint(1, 3)
        b = random.randint(0, 4)
        x = random.randint(1, max(1, (10 - b) // a))
        y = a * x + b
        coef = "x" if a == 1 else "%dx" % a
        eq = ("y = %s + %d" % (coef, b)) if b else ("y = %s" % coef)
        return _gridq("The equation %s is satisfied by many (x, y) pairs. Plot "
                      "the point on the grid where x = %d." % (eq, x), x, y,
                      ["%d × %d = %d, so y = %d." % (a, x, a * x, y),
                       "The point is (%d, %d)." % (x, y)], size=10)

    def plot_point_sum():
        s = random.randint(4, 10)
        x = random.randint(1, s - 1)
        return _gridq("Plot the point on the grid that fits x + y = %d and has "
                      "x = %d." % (s, x), x, s - x,
                      ["%d − %d = %d, so y = %d." % (s, x, s - x, s - x),
                       "The point is (%d, %d)." % (x, s - x)], size=10)

    def word_pair():
        who = pick(NAMES)
        s = random.randint(10, 40)
        x = random.randint(1, s - 1)
        return _numq("%s has x red counters and y blue counters, with x + y = "
                     "%d counters altogether. If x = %d, what is y?"
                     % (who, s, x), s - x,
                     ["%d − %d = %d blue counters." % (s, x, s - x)],
                     placeholder="y = ?")

    def cost_pair():
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        x = random.randint(1, 8)
        y = random.randint(1, 10)
        total = a * x + b * y
        return _numq("A ticket costs %s and a programme costs %s. The equation "
                     "%dx + %dy = %d gives the total cost in pounds, where x is "
                     "the number of tickets and y is the number of programmes. "
                     "If x = %d, what is y?"
                     % (_pounds(a), _pounds(b), a, b, total, x), y,
                     ["%d × %d = %d." % (a, x, a * x),
                      "%d − %d = %d." % (total, a * x, b * y),
                      "%d ÷ %d = %d." % (b * y, b, y)], placeholder="y = ?")

    def satisfies_check():
        a = random.randint(2, 6)
        b = random.randint(1, 12)
        x = random.randint(1, 10)
        y = a * x + b
        if random.random() < 0.5:
            return _wordq("Does the pair x = %d, y = %d satisfy the equation "
                          "y = %dx + %d? Type yes or no." % (x, y, a, b), "yes",
                          ["%d × %d + %d = %d ✓." % (a, x, b, y)],
                          placeholder="yes or no")
        off = pick([1, 2, 3])
        return _wordq("Does the pair x = %d, y = %d satisfy the equation "
                      "y = %dx + %d? Type yes or no." % (x, y + off, a, b),
                      "no",
                      ["%d × %d + %d = %d, not %d." % (a, x, b, y, y + off)],
                      placeholder="yes or no")

    def io_pairs():
        a = random.randint(2, 8)
        b = random.randint(0, 20)
        xs = sorted(random.sample(range(1, 16), 4))
        rows = [[x, a * x + b] for x in xs]
        i = random.randrange(4)
        eq = "y = %dx + %d" % (a, b) if b else "y = %dx" % a
        return _ioq("Each row of this table is an (x, y) pair fitting %s. Type "
                    "the missing Out number." % eq, rows, i, rows[i][1],
                    ["%d × %d + %d = %d." % (a, xs[i], b, a * xs[i] + b)],
                    rule=eq)

    def complete_relationship_table():
        """Complete a table for a two-variable relationship."""
        a = random.randint(2, _by_d(d, 3, 5, 8))
        b = random.randint(1, _by_d(d, 5, 12, 25))
        xs = sorted(random.sample(range(1, 13), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(a * x + b)]
                for j, x in enumerate(xs)]
        eq = "y = %dx + %d" % (a, b)
        return _dtq("This table shows a two-variable relationship between x and "
                    "y, given by the rule %s. Complete the table: type the "
                    "value that belongs in the empty cell." % eq,
                    ["x", "y"], rows, a * xs[i] + b,
                    ["%d × %d = %d." % (a, xs[i], a * xs[i]),
                     "%d + %d = %d." % (a * xs[i], b, a * xs[i] + b)],
                    missing=(i, 1), caption="Two-variable relationship: %s" % eq)

    def graph_relationship():
        """Graph a two-variable relationship on the coordinate grid."""
        size = 10
        a = _by_d(d, 1, 2, random.randint(2, 3))
        b = _by_d(d, random.randint(0, 3), 1, random.randint(0, 3))
        xmax = (size - b) // a
        if xmax < 1:
            a, b, xmax = 1, 1, size - 1
        x = random.randint(1, min(xmax, size))
        y = a * x + b
        coef = "x" if a == 1 else "%dx" % a
        eq = ("y = %s + %d" % (coef, b)) if b else ("y = %s" % coef)
        return _gridq("Graph this two-variable relationship: %s. Plot the point "
                      "on the grid for x = %d." % (eq, x), x, y,
                      ["Put x = %d into %s." % (x, eq),
                       "y = %d, so the point is (%d, %d)." % (y, x, y)],
                      size=size)

    opts = [sum_pair, linear_y, two_term_equation, table_missing_y,
            table_missing_x, table_sum, plot_point, io_pairs, word_pair,
            sum_pair_x, complete_relationship_table, graph_relationship]
    if d == 0:
        opts = [sum_pair, sum_pair_x, double_equation, linear_y,
                table_missing_y, table_sum, plot_point_sum, io_pairs,
                word_pair, complete_relationship_table, graph_relationship]
    elif d == 2:
        opts = [linear_x, two_term_equation, cost_pair, satisfies_check,
                table_missing_x, table_missing_y, plot_point, io_pairs,
                linear_y, complete_relationship_table, graph_relationship]
    opts = opts + [table_missing_y, table_sum, plot_point, io_pairs,
                   complete_relationship_table, graph_relationship]
    return pick(opts)()


# ================================================================= 6.7.j =====
@skill("Y6.7.j", "Enumerate combinations of two variables", S7)
def _(d=1):
    d = _t(d)

    def count_positive_sum():
        s = _by_d(d, random.randint(5, 10), random.randint(8, 20),
                  random.randint(15, 40))
        return _numq("x and y are whole numbers greater than 0 and x + y = %d. "
                     "How many different pairs of values are possible?" % s,
                     s - 1,
                     ["x can be 1, 2, 3, … up to %d." % (s - 1),
                      "That gives %d different pairs." % (s - 1)],
                     placeholder="how many pairs")

    def count_including_zero():
        s = _by_d(d, random.randint(4, 9), random.randint(6, 15),
                  random.randint(12, 30))
        return _numq("x and y are whole numbers, and zero is allowed. If "
                     "x + y = %d, how many different pairs of values are "
                     "possible?" % s, s + 1,
                     ["x can be 0, 1, 2, … up to %d." % s,
                      "That is %d values, so %d pairs." % (s + 1, s + 1)],
                     placeholder="how many pairs")

    def count_two_coefficient():
        a = pick([2, 3, 4, 5])
        s = a * random.randint(2, _by_d(d, 4, 7, 12)) + random.randint(1, a - 1)
        cnt = sum(1 for x in range(1, s // a + 1) if s - a * x >= 1)
        return _numq("x and y are whole numbers greater than 0 and %dx + y = "
                     "%d. How many different pairs of values are possible?"
                     % (a, s), cnt,
                     ["x can be 1 up to %d, because %dx must be less than %d."
                      % (cnt, a, s),
                      "That gives %d pairs." % cnt],
                     placeholder="how many pairs")

    def count_both_coefficients():
        a = pick([2, 3, 4])
        b = pick([3, 5, 6, 7])
        while b == a:
            b = pick([3, 5, 6, 7])
        tot = a * random.randint(1, 6) + b * random.randint(1, 6)
        cnt = sum(1 for x in range(1, tot // a + 1)
                  if (tot - a * x) > 0 and (tot - a * x) % b == 0)
        if cnt == 0:
            return count_positive_sum()
        return _numq("x and y are whole numbers greater than 0 and %dx + %dy = "
                     "%d. How many different pairs of values are possible?"
                     % (a, b, tot), cnt,
                     ["Try x = 1, 2, 3, … and check whether %d − %dx divides "
                      "exactly by %d." % (tot, a, b),
                      "There %s %s that %s." % ("is" if cnt == 1 else "are", _pl(cnt, "pair"), "works" if cnt == 1 else "work")],
                     placeholder="how many pairs")

    def list_y_values():
        s = random.randint(6, 14)
        lo = 1
        hi = min(s - 1, lo + _by_d(d, 2, 3, 4))
        ys = [s - x for x in range(lo, hi + 1)]
        return _setq("x + y = %d, and x takes every whole-number value from %d "
                     "to %d. List all the matching values of y, separated by "
                     "commas." % (s, lo, hi), sorted(ys),
                     ["When x = %d, y = %d." % (lo, s - lo),
                      "The values of y are %s."
                      % ", ".join(str(t) for t in sorted(ys))])

    def list_x_values():
        a = pick([2, 3, 4])
        vals = sorted(random.sample(range(1, 9), 3))
        ys = [a * x for x in vals]
        return _setq("y = %dx. When x takes the values %s, list all the "
                     "matching values of y, separated by commas."
                     % (a, ", ".join(str(t) for t in vals)), ys,
                     ["%d × %d = %d." % (a, vals[0], ys[0]),
                      "The values of y are %s."
                      % ", ".join(str(t) for t in ys)])

    def outfit_combinations():
        m = random.randint(3, _by_d(d, 5, 7, 9))
        n = random.randint(3, _by_d(d, 5, 7, 9))
        one, two = pick([("shirts", "ties"), ("hats", "scarves"),
                         ("tops", "skirts"), ("starters", "main courses"),
                         ("flavours of ice cream", "toppings")])
        who = pick(NAMES)
        return _numq("A menu offers %d %s and %d %s. How many different "
                     "combinations of one of each are possible?"
                     % (m, one, n, two), m * n,
                     ["Each of the %d %s can go with each of the %d %s."
                      % (m, one, n, two),
                      "%d × %d = %d combinations." % (m, n, m * n)],
                     unit="combinations")

    def coin_ways():
        a, b = pick([(2, 5), (5, 10), (2, 10), (5, 20)])
        n = random.randint(2, 8)
        target = a * n + b * random.randint(1, 4)
        cnt = sum(1 for x in range(0, target // a + 1)
                  if (target - a * x) % b == 0)
        return _numq("A machine takes only %dp and %dp coins. In how many "
                     "different ways can exactly %dp be paid, if the number of "
                     "each coin can be zero or more?" % (a, b, target), cnt,
                     ["Try each possible number of %dp coins and check whether "
                      "the amount left divides exactly by %dp." % (a, b),
                      "There %s %s." % ("is" if cnt == 1 else "are", _pl(cnt, "way"))],
                     placeholder="how many ways")

    def pairs_table():
        s = random.randint(8, 20)
        xs = sorted(random.sample(range(1, s), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(s - x)]
                for j, x in enumerate(xs)]
        return _dtq("This table lists some of the pairs of whole numbers with "
                    "x + y = %d. What is the missing value?" % s,
                    ["x", "y"], rows, s - xs[i],
                    ["%d − %d = %d." % (s, xs[i], s - xs[i])],
                    missing=(i, 1), caption="Pairs with x + y = %d" % s)

    def largest_value():
        a = pick([2, 3, 4, 5])
        s = a * random.randint(3, 9) + random.randint(1, a - 1)
        best = (s - 1) // a
        return _numq("x and y are whole numbers greater than 0 and %dx + y = "
                     "%d. What is the largest possible value of x?" % (a, s),
                     best,
                     ["y must be at least 1, so %dx can be at most %d."
                      % (a, s - 1),
                      "%d ÷ %d = %d remainder %d, so x is at most %d."
                      % (s - 1, a, best, (s - 1) % a, best)],
                     placeholder="largest x")

    def smallest_value():
        s = random.randint(10, 30)
        return _numq("x and y are whole numbers greater than 0 with x + y = %d "
                     "and x greater than y. What is the smallest possible value "
                     "of x?" % s, s // 2 + 1,
                     ["Half of %d is %s." % (s, ("%.1f" % (s / 2.0)).rstrip("0")
                                             .rstrip(".")),
                      "x must be bigger than y, so the smallest x is %d."
                      % (s // 2 + 1)], placeholder="smallest x")

    def count_x_less_y():
        s = random.randint(7, 25)
        cnt = sum(1 for x in range(1, s) if x < s - x)
        return _numq("x and y are whole numbers greater than 0 with x + y = %d "
                     "and x less than y. How many pairs are possible?" % s,
                     cnt,
                     ["List the pairs with x smaller than y.",
                      "There are %d such pairs." % cnt],
                     placeholder="how many pairs")

    def sandwich_choices():
        m = random.randint(3, 6)
        n = random.randint(2, 5)
        p = random.randint(2, 4)
        return _numq("A lunch deal has %d sandwich choices, %d drink choices "
                     "and %d snack choices. How many different lunches are "
                     "possible if one of each is chosen?" % (m, n, p),
                     m * n * p,
                     ["%d × %d = %d sandwich and drink pairs." % (m, n, m * n),
                      "%d × %d = %d lunches." % (m * n, p, m * n * p)],
                     unit="lunches")

    def combo_table():
        m = random.randint(3, 6)
        n = random.randint(3, 6)
        rows = [["Shirts", str(m)], ["Ties", str(n)]]
        return _dtq("The table shows how many of each item are in a wardrobe. "
                    "How many different shirt-and-tie combinations are "
                    "possible?", ["Item", "Number"], rows, m * n,
                    ["%d × %d = %d combinations." % (m, n, m * n)],
                    caption="Wardrobe")

    opts = [count_positive_sum, count_including_zero, outfit_combinations,
            pairs_table, list_y_values, list_x_values, count_two_coefficient,
            combo_table, largest_value, sandwich_choices]
    if d == 0:
        opts = [count_positive_sum, outfit_combinations, pairs_table,
                list_x_values, combo_table, sandwich_choices,
                count_including_zero, list_y_values]
    elif d == 2:
        opts = [count_two_coefficient, count_both_coefficients, coin_ways,
                count_x_less_y, largest_value, smallest_value, list_y_values,
                pairs_table, combo_table, count_positive_sum]
    opts = opts + [pairs_table, combo_table, pairs_table]
    return pick(opts)()


# ================================================================= 6.7.k =====
@skill("Y6.7.k", "Generate and describe linear sequences", S7)
def _(d=1):
    d = _t(d)
    step = _by_d(d, pick([2, 3, 4, 5, 10]), random.randint(2, 9),
                 pick([6, 7, 8, 9, 11, 12, 15, 20, 25]))
    start = _by_d(d, random.randint(1, 10), random.randint(1, 30),
                  random.randint(3, 80))
    terms = [start + i * step for i in range(6)]

    def next_term():
        shown = terms[:4]
        return _numq("Here is a sequence:  %s, …  What is the next term?"
                     % ", ".join(str(t) for t in shown), terms[4],
                     ["The sequence goes up by %d each time." % step,
                      "%d + %d = %d." % (terms[3], step, terms[4])])

    def next_two():
        shown = terms[:4]
        return _setq("Here is a sequence:  %s, …  Write the next two terms, "
                     "separated by a comma."
                     % ", ".join(str(t) for t in shown),
                     [terms[4], terms[5]],
                     ["The rule is add %d." % step,
                      "%d and %d." % (terms[4], terms[5])],
                     placeholder="e.g. 20, 25")

    def state_rule():
        shown = terms[:5]
        return _numq("Here is a sequence:  %s.  The rule is 'add ___'. What "
                     "number goes in the blank?"
                     % ", ".join(str(t) for t in shown), step,
                     ["%d − %d = %d." % (terms[1], terms[0], step),
                      "The rule is add %d." % step],
                     placeholder="a number")

    def state_rule_down():
        st = random.randint(2, 9)
        first = st * random.randint(8, 20)
        seq = [first - i * st for i in range(5)]
        return _numq("Here is a sequence:  %s.  The rule is 'subtract ___'. "
                     "What number goes in the blank?"
                     % ", ".join(str(t) for t in seq), st,
                     ["%d − %d = %d." % (seq[0], seq[1], st),
                      "The rule is subtract %d." % st],
                     placeholder="a number")

    def next_term_down():
        st = random.randint(2, 9)
        first = st * random.randint(8, 25)
        seq = [first - i * st for i in range(5)]
        return _numq("Here is a sequence:  %s, …  What is the next term?"
                     % ", ".join(str(t) for t in seq[:4]), seq[4],
                     ["The sequence goes down by %d each time." % st,
                      "%d − %d = %d." % (seq[3], st, seq[4])])

    def nth_from_rule():
        a = random.randint(2, _by_d(d, 5, 9, 12))
        b = random.randint(1, _by_d(d, 8, 20, 40))
        n = random.randint(5, _by_d(d, 10, 20, 50))
        return _numq("The rule for the nth term of a sequence is %dn + %d. What "
                     "is the %s term?" % (a, b, ordinal(n)), a * n + b,
                     ["%d × %d = %d." % (a, n, a * n),
                      "%d + %d = %d." % (a * n, b, a * n + b)])

    def first_from_rule():
        a = random.randint(2, 9)
        b = random.randint(1, 25)
        return _numq("The rule for the nth term of a sequence is %dn + %d. What "
                     "is the first term?" % (a, b), a + b,
                     ["Put n = 1: %d × 1 + %d." % (a, b),
                      "The first term is %d." % (a + b)])

    def rule_coefficient():
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        seq = [a * n + b for n in range(1, 6)]
        return _numq("Here is a sequence:  %s.  The rule for the nth term is "
                     "___n + %d. What number goes in the blank?"
                     % (", ".join(str(t) for t in seq), b), a,
                     ["The terms go up by %d each time." % a,
                      "So the rule is %dn + %d." % (a, b)],
                     placeholder="a number")

    def rule_constant():
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        seq = [a * n + b for n in range(1, 6)]
        return _numq("Here is a sequence:  %s.  The rule for the nth term is "
                     "%dn + ___. What number goes in the blank?"
                     % (", ".join(str(t) for t in seq), a), b,
                     ["The terms go up by %d, so the rule starts %dn."
                      % (a, a),
                      "%d × 1 = %d, and the first term is %d, so add %d."
                      % (a, a, seq[0], b)], placeholder="a number")

    def far_term():
        n = pick([10, 12, 15, 20, 25, 50, 100])
        return _numq("A sequence starts at %d and goes up by %d each time. What "
                     "is the %s term?" % (start, step, ordinal(n)),
                     start + (n - 1) * step,
                     ["From the first term there are %d steps of %d."
                      % (n - 1, step),
                      "%d + %d = %d." % (start, (n - 1) * step,
                                         start + (n - 1) * step)])

    def is_it_in():
        target = terms[2]
        if random.random() < 0.5:
            return _wordq("A sequence starts at %d and goes up by %d each time. "
                          "Is %d a term in this sequence? Type yes or no."
                          % (start, step, target), "yes",
                          ["%d − %d = %d, which divides exactly by %d."
                           % (target, start, target - start, step),
                           "So %d is in the sequence." % target],
                          placeholder="yes or no")
        off = random.randint(1, step - 1) if step > 1 else 1
        return _wordq("A sequence starts at %d and goes up by %d each time. Is "
                      "%d a term in this sequence? Type yes or no."
                      % (start, step, target + off), "no",
                      ["%d − %d = %d, which does not divide exactly by %d."
                       % (target + off, start, target + off - start, step),
                       "So %d is not in the sequence." % (target + off)],
                      placeholder="yes or no")

    def sequence_table():
        a = random.randint(2, 8)
        b = random.randint(0, 15)
        poss = sorted(random.sample(range(1, 12), 4))
        i = random.randrange(4)
        rows = [[str(p), "" if j == i else str(a * p + b)]
                for j, p in enumerate(poss)]
        rule = "%dn + %d" % (a, b) if b else "%dn" % a
        return _dtq("This table shows the terms of a sequence with the rule %s. "
                    "What is the missing term?" % rule,
                    ["Position (n)", "Term"], rows, a * poss[i] + b,
                    ["%d × %d = %d." % (a, poss[i], a * poss[i]),
                     "The term is %d." % (a * poss[i] + b)],
                    missing=(i, 1), caption="Sequence rule: %s" % rule)

    def sequence_io():
        a = random.randint(2, 9)
        b = random.randint(0, 20)
        poss = sorted(random.sample(range(1, 16), 4))
        rows = [[p, a * p + b] for p in poss]
        i = random.randrange(4)
        rule = "%dn + %d" % (a, b) if b else "%dn" % a
        return _ioq("The In column is the position n and the Out column is the "
                    "term. The rule is %s. Type the missing Out number." % rule,
                    rows, i, rows[i][1],
                    ["%d × %d + %d = %d." % (a, poss[i], b, a * poss[i] + b)],
                    rule=rule)

    def which_position():
        n = random.randint(5, 15)
        val = start + (n - 1) * step
        return _numq("A sequence starts at %d and goes up by %d each time. "
                     "Which position in the sequence has the value %d? (The "
                     "first term is position 1.)" % (start, step, val), n,
                     ["%d − %d = %d." % (val, start, val - start),
                      "%d ÷ %d = %d steps, so it is term number %d."
                      % (val - start, step, n - 1, n)],
                     placeholder="position number")

    def decimal_sequence():
        st = pick([2, 4, 5, 25])
        first = random.randint(1, 20)
        seq = [(first + i * st) / 10.0 for i in range(5)]
        txt = ", ".join(("%g" % t) for t in seq[:4])
        return _numq("Here is a sequence of decimals:  %s, …  What is the next "
                     "term?" % txt, round(seq[4], 3),
                     ["The sequence goes up by %g each time." % (st / 10.0),
                      "%g + %g = %g." % (seq[3], st / 10.0, seq[4])],
                     answer_type="num", tolerance=0.0001)

    def two_step_rule_pattern():
        """Use a two-step rule to complete a number pattern."""
        mult = _by_d(d, 2, pick([2, 3]), pick([2, 3, 4]))
        add = random.randint(1, _by_d(d, 3, 6, 10))
        first = random.randint(1, _by_d(d, 4, 6, 9))
        seq = [first]
        for _ in range(4):
            seq.append(seq[-1] * mult + add)
        rule = ("double then add %d" % add if mult == 2
                else "multiply by %d then add %d" % (mult, add))
        if random.random() < 0.5:
            return _numq("The two-step rule for this number pattern is '%s'. "
                         "Use the two-step rule to complete the pattern: what "
                         "is the next term?   %s, …"
                         % (rule, ", ".join(str(t) for t in seq[:4])), seq[4],
                         ["%d × %d = %d." % (seq[3], mult, seq[3] * mult),
                          "%d + %d = %d." % (seq[3] * mult, add, seq[4])],
                         placeholder="next term")
        i = random.randint(1, 3)
        shown = ["___" if j == i else str(t) for j, t in enumerate(seq[:5])]
        return _numq("The two-step rule for this number pattern is '%s'. Use "
                     "the two-step rule to complete the pattern: what is the "
                     "missing term?   %s" % (rule, ", ".join(shown)), seq[i],
                     ["%d × %d = %d." % (seq[i - 1], mult,
                                         seq[i - 1] * mult),
                      "%d + %d = %d." % (seq[i - 1] * mult, add, seq[i])],
                     placeholder="missing term")

    opts = [next_term, state_rule, nth_from_rule, sequence_table, sequence_io,
            far_term, next_two, rule_coefficient, next_term_down,
            which_position, two_step_rule_pattern]
    if d == 0:
        opts = [next_term, state_rule, next_two, next_term_down,
                state_rule_down, sequence_table, sequence_io, first_from_rule,
                two_step_rule_pattern]
    elif d == 2:
        opts = [nth_from_rule, rule_coefficient, rule_constant, far_term,
                which_position, is_it_in, decimal_sequence, sequence_table,
                sequence_io, state_rule_down, two_step_rule_pattern]
    opts = opts + [sequence_table, sequence_io, sequence_table]
    return pick(opts)()


# ================================================================= 6.7.l =====
@skill("Y6.7.l", "Missing terms and sequence problems", S7)
def _(d=1):
    d = _t(d)
    step = _by_d(d, pick([2, 3, 5, 10]), random.randint(2, 9),
                 pick([6, 7, 8, 9, 12, 15, 20, 25]))
    start = _by_d(d, random.randint(1, 12), random.randint(2, 40),
                  random.randint(5, 90))
    terms = [start + i * step for i in range(7)]

    def missing_middle():
        i = random.randint(1, 4)
        shown = ["___" if j == i else str(t) for j, t in enumerate(terms[:6])]
        return _numq("Find the missing term in this sequence:  %s"
                     % ", ".join(shown), terms[i],
                     ["The sequence goes up by %d each time." % step,
                      "%d + %d = %d." % (terms[i - 1], step, terms[i])],
                     placeholder="missing term")

    def missing_first():
        shown = ["___"] + [str(t) for t in terms[1:6]]
        return _numq("Find the missing first term in this sequence:  %s"
                     % ", ".join(shown), terms[0],
                     ["The sequence goes up by %d each time." % step,
                      "%d − %d = %d." % (terms[1], step, terms[0])],
                     placeholder="missing term")

    def missing_last():
        shown = [str(t) for t in terms[:5]] + ["___"]
        return _numq("Find the missing last term in this sequence:  %s"
                     % ", ".join(shown), terms[5],
                     ["The sequence goes up by %d each time." % step,
                      "%d + %d = %d." % (terms[4], step, terms[5])],
                     placeholder="missing term")

    def two_missing():
        shown = [str(terms[0]), "___", str(terms[2]), "___", str(terms[4])]
        return _setq("Two terms are missing from this sequence:  %s.  Write "
                     "both missing terms, separated by a comma."
                     % ", ".join(shown), [terms[1], terms[3]],
                     ["The sequence goes up by %d each time." % step,
                      "The missing terms are %d and %d."
                      % (terms[1], terms[3])],
                     placeholder="e.g. 12, 20")

    def gap_of_two():
        i = random.randint(1, 4)
        return _numq("In a sequence that goes up by equal steps, one term is %d "
                     "and the term two places later is %d. What is the term "
                     "between them?" % (terms[i - 1], terms[i + 1]), terms[i],
                     ["The two terms are 2 steps apart: %d − %d = %d."
                      % (terms[i + 1], terms[i - 1], 2 * step),
                      "One step is %d ÷ 2 = %d." % (2 * step, step),
                      "%d + %d = %d." % (terms[i - 1], step, terms[i])],
                     placeholder="middle term")

    def missing_down():
        st = random.randint(2, 9)
        first = st * random.randint(9, 25)
        seq = [first - i * st for i in range(6)]
        i = random.randint(1, 4)
        shown = ["___" if j == i else str(t) for j, t in enumerate(seq)]
        return _numq("Find the missing term in this decreasing sequence:  %s"
                     % ", ".join(shown), seq[i],
                     ["The sequence goes down by %d each time." % st,
                      "%d − %d = %d." % (seq[i - 1], st, seq[i])],
                     placeholder="missing term")

    def savings_word():
        who = pick(NAMES)
        wk = random.randint(5, 12)
        return _numq("%s starts with %s and saves %s every week. How much has "
                     "%s saved after %d weeks, in pounds?"
                     % (who, _pounds(start), _pounds(step), who, wk),
                     start + step * wk,
                     ["%d weeks of saving is %d × %d = %s."
                      % (wk, step, wk, _pounds(step * wk)),
                      "%d + %d = %s." % (start, step * wk,
                                         _pounds(start + step * wk))],
                     unit="£")

    def matchstick_pattern():
        per = random.randint(2, 5)
        first = per + random.randint(1, 4)
        n = random.randint(5, _by_d(d, 8, 12, 30))
        return _numq("A pattern is made from matchsticks. The first shape uses "
                     "%d matchsticks and every extra shape uses %d more. How "
                     "many matchsticks are needed for %d shapes?"
                     % (first, per, n), first + per * (n - 1),
                     ["After the first shape there are %d more shapes."
                      % (n - 1),
                      "%d + %d × %d = %d matchsticks."
                      % (first, per, n - 1, first + per * (n - 1))],
                     unit="matchsticks")

    def tables_and_chairs():
        per = random.randint(2, 4)
        first = per + random.randint(2, 4)
        n = random.randint(4, 15)
        return _numq("Tables are pushed together in a line. One table seats %d "
                     "people, and each extra table adds %d more seats. How many "
                     "people can sit at %d tables?" % (first, per, n),
                     first + per * (n - 1),
                     ["%d extra tables add %d × %d = %d seats."
                      % (n - 1, per, n - 1, per * (n - 1)),
                      "%d + %d = %d people."
                      % (first, per * (n - 1), first + per * (n - 1))],
                     unit="people")

    def which_term_exceeds():
        limit = start + step * random.randint(4, 12)
        n = 1
        while start + (n - 1) * step <= limit:
            n += 1
        return _numq("A sequence starts at %d and goes up by %d each time. "
                     "Which is the first position whose term is greater than "
                     "%d? (The first term is position 1.)"
                     % (start, step, limit), n,
                     ["Term %d is %d, which is not greater than %d."
                      % (n - 1, start + (n - 2) * step, limit),
                      "Term %d is %d, which is greater than %d."
                      % (n, start + (n - 1) * step, limit)],
                     placeholder="position number")

    def sequence_table_gap():
        poss = [1, 2, 3, 4, 5]
        i = random.randint(1, 4)
        rows = [[str(p), "" if j == i else str(terms[p - 1])]
                for j, p in enumerate(poss)]
        return _dtq("This table shows a sequence that goes up by equal steps. "
                    "What is the missing term?", ["Position", "Term"], rows,
                    terms[i],
                    ["The step is %d − %d = %d."
                     % (terms[1] if i != 1 else terms[3],
                        terms[0] if i != 1 else terms[2], step),
                     "The missing term is %d." % terms[i]],
                    missing=(i, 1), caption="A linear sequence")

    def sequence_table_two_gaps():
        poss = [1, 2, 3, 4, 5, 6]
        rows = [[str(p), "" if p in (3, 5) else str(terms[p - 1])]
                for p in poss]
        return _dtq("This table shows a sequence that goes up by equal steps. "
                    "What is the term at position 3?", ["Position", "Term"],
                    rows, terms[2],
                    ["The step is %d − %d = %d." % (terms[1], terms[0], step),
                     "%d + %d = %d." % (terms[1], step, terms[2])],
                    missing=(2, 1), caption="A linear sequence")

    def bar_sequence():
        cats = ["Week 1", "Week 2", "Week 3", "Week 4"]
        vals = terms[:4]
        return _barq("The chart shows how many books were read each week. The "
                     "numbers go up by the same amount each week. How many "
                     "books would be read in Week 5 if the pattern "
                     "continues?", cats, vals, terms[4],
                     ["The pattern goes up by %d each week." % step,
                      "%d + %d = %d books." % (terms[3], step, terms[4])])

    def total_of_terms():
        n = random.randint(3, 5)
        tot = sum(terms[:n])
        return _numq("A sequence starts at %d and goes up by %d each time. What "
                     "is the total of the first %d terms?" % (start, step, n),
                     tot,
                     ["The first %d terms are %s."
                      % (n, ", ".join(str(t) for t in terms[:n])),
                      "Their total is %d." % tot])

    def step_from_two_terms():
        i = random.randint(2, 4)
        gap = i
        return _numq("In a sequence with equal steps, the first term is %d and "
                     "the %s term is %d. What is the step between terms?"
                     % (terms[0], ordinal(i + 1), terms[i]), step,
                     ["From term 1 to term %d there are %d steps."
                      % (i + 1, gap),
                      "%d − %d = %d, and %d ÷ %d = %d."
                      % (terms[i], terms[0], terms[i] - terms[0],
                         terms[i] - terms[0], gap, step)],
                     placeholder="the step")

    def mixed_review():
        """Number sequences: mixed review — one framing, several sequence
        types (increasing, decreasing, multiplying, square numbers,
        two-step)."""
        kinds = ["up", "down", "multiply"]
        if d >= 1:
            kinds = kinds + ["square", "two_step"]
        kind = pick(kinds)
        if kind == "up":
            seq = terms[:5]
            why = ["The rule is add %d each time." % step,
                   "%d + %d = %d." % (seq[3], step, seq[4])]
        elif kind == "down":
            st = random.randint(2, 9)
            first = st * random.randint(9, 25)
            seq = [first - i * st for i in range(5)]
            why = ["The rule is subtract %d each time." % st,
                   "%d − %d = %d." % (seq[3], st, seq[4])]
        elif kind == "multiply":
            m = _by_d(d, 2, pick([2, 3]), pick([2, 3, 4]))
            first = random.randint(1, _by_d(d, 4, 6, 8))
            seq = [first * (m ** i) for i in range(5)]
            why = ["The rule is multiply by %d each time." % m,
                   "%d × %d = %d." % (seq[3], m, seq[4])]
        elif kind == "square":
            first = random.randint(1, 5)
            seq = [(first + i) ** 2 for i in range(5)]
            why = ["These are the square numbers from %d² onwards." % first,
                   "%d × %d = %d." % (first + 4, first + 4, seq[4])]
        else:
            m = pick([2, 3])
            add = random.randint(1, 5)
            first = random.randint(1, 5)
            seq = [first]
            for _ in range(4):
                seq.append(seq[-1] * m + add)
            why = ["The rule is multiply by %d then add %d." % (m, add),
                   "%d × %d + %d = %d." % (seq[3], m, add, seq[4])]
        return _numq("Number sequences: mixed review. The rule could be adding, "
                     "subtracting, multiplying each time, square numbers or a "
                     "two-step rule. Work out the rule, then type the next "
                     "term.   %s, …"
                     % ", ".join(str(t) for t in seq[:4]), seq[4], why,
                     placeholder="next term")

    opts = [missing_middle, missing_first, missing_last, two_missing,
            gap_of_two, missing_down, savings_word, matchstick_pattern,
            sequence_table_gap, bar_sequence, mixed_review]
    if d == 0:
        opts = [missing_middle, missing_first, missing_last, missing_down,
                sequence_table_gap, bar_sequence, savings_word,
                sequence_table_two_gaps, mixed_review]
    elif d == 2:
        opts = [two_missing, gap_of_two, step_from_two_terms,
                which_term_exceeds, matchstick_pattern, tables_and_chairs,
                total_of_terms, sequence_table_gap, bar_sequence,
                missing_down, mixed_review]
    opts = opts + [sequence_table_gap, bar_sequence, sequence_table_two_gaps]
    return pick(opts)()
