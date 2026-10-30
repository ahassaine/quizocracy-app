# dev/app/logic/y8_gen_c.py — Year 8 generators: strands 8.4 and 8.5
#
# 8.4  Ratio, proportion, rates & scale        (Y8.4.a .. Y8.4.j)
# 8.5  Percentages & financial maths           (Y8.5.a .. Y8.5.j)
#
# Every generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between many genuinely different framings (bare technique,
# word problem, missing value, inverse, visual model, comparison, reasoning,
# multi-step).  Visual components carry a large share of the framings:
#   data_table       -> ratio/rate tables, tables of values, price lists
#   strip_model      -> share-in-a-ratio bar models
#   coordinate_grid  -> straight-line (direct-proportion) graphs
#   scatter_plot     -> rates / trends, best-fit prediction
#   pie_chart / bar_chart -> supporting framings
#
# MONEY & PERCENTAGES are computed with integer pence (or Decimal) and rounded
# only at the end — never with raw floats.  Every subtraction is guarded so no
# answer is unintentionally negative.
import random
from decimal import Decimal
from fractions import Fraction
from .maths_engine import skill, pick, NAMES, n_words, money, ordinal

S4 = "8.4 Ratio, proportion, rates & scale"
S5 = "8.5 Percentages & financial maths"


# ---------------------------------------------------------------- helpers ----
def _t(d):
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
    for _ in range(200):
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if a != b and _hcf(a, b) == 1:
            return a, b
    return 2, 3


def _pounds(n):
    return "£%d" % int(n)


def _dstr(x):
    """Format a Decimal/number as plain decimal text (no scientific, no float junk)."""
    d = x if isinstance(x, Decimal) else Decimal(str(x))
    d = d.normalize()
    s = format(d, "f")
    return s


# ---- answer wrappers -------------------------------------------------------
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


def _decq(prompt, dec_str, solution, placeholder="e.g. 0.45", tolerance=0):
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": dec_str, "answer_type": "num",
            "tolerance": tolerance, "solution": solution}


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
    return _stripq(prompt,
                   {"mode": "equal_parts", "parts": int(parts),
                    "partLabel": "?", "totalLabel": str(total),
                    "unknown": "part"}, answer, solution)


def _total_strip(prompt, parts, one_part, answer, solution):
    return _stripq(prompt,
                   {"mode": "equal_parts", "parts": int(parts),
                    "partLabel": str(one_part), "totalLabel": "?",
                    "unknown": "total"}, answer, solution)


def _lineq(prompt, k, x, xmax, ymax, solution):
    """coordinate_grid: draw the line y = kx through the origin; the pupil plots
    the point on the line at the given x.  Answer is the coord (x, kx)."""
    spec = {"mode": "plot", "xmin": 0, "xmax": int(xmax), "ymin": 0,
            "ymax": int(ymax),
            "lines": [{"p1": [0, 0], "p2": [int(xmax), int(k * xmax)],
                       "label": "y = %dx" % k if k != 1 else "y = x"}]}
    return {"prompt": prompt, "component": "coordinate_grid", "spec": spec,
            "answer": "(%d,%d)" % (x, k * x), "answer_type": "coord",
            "tolerance": 0, "solution": solution}


def _scatterq(prompt, points, answer, answer_type, solution, xlabel, ylabel,
              line=None, highlight=None, placeholder=None):
    spec = {"points": [[p[0], p[1]] for p in points],
            "xLabel": xlabel, "yLabel": ylabel}
    if line is not None:
        spec["line"] = {"p1": list(line[0]), "p2": list(line[1])}
    if highlight is not None:
        spec["highlight"] = int(highlight)
    return {"prompt": prompt, "component": "scatter_plot", "spec": spec,
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


def _pieq(prompt, slices, answer, answer_type, solution, highlight=None):
    spec = {"slices": [[str(a), int(b)] for a, b in slices]}
    if highlight is not None:
        spec["highlight"] = int(highlight)
    return {"prompt": prompt, "component": "pie_chart", "spec": spec,
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


def _barq(prompt, cats, vals, answer, solution, answer_type="int"):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals],
                     "mode": "read"},
            "answer": answer, "answer_type": answer_type, "tolerance": 0,
            "solution": solution}


# object / people pairs
_PAIRS = [("red beads", "blue beads"), ("roses", "tulips"),
          ("cars", "vans"), ("pens", "pencils"), ("apples", "pears"),
          ("hardbacks", "paperbacks"), ("stamps", "stickers"),
          ("oak trees", "pine trees"), ("red counters", "blue counters"),
          ("plain buns", "iced buns")]
_PEOPLE = [("boys", "girls"), ("adults", "children"),
           ("singers", "musicians"), ("swimmers", "runners")]
_ITEMS = [("pen", "pens"), ("apple", "apples"), ("notebook", "notebooks"),
          ("bottle", "bottles"), ("candle", "candles"), ("badge", "badges")]


# ================================================================= 8.4.a =====
@skill("Y8.4.a", "Write and simplify ratios; equivalent ratios", S4)
def _(d=1):
    d = _t(d)
    a, b = _coprime_pair(2, _by_d(d, 5, 7, 9))
    k = _by_d(d, random.randint(2, 4), random.randint(2, 8),
              random.randint(4, 12))
    A, B = a * k, b * k

    def simplify_first():
        return _numq("Write the ratio %d : %d in its simplest form. Type the "
                     "first number of the simplified ratio." % (A, B), a,
                     ["The highest common factor of %d and %d is %d." % (A, B, k),
                      "%d ÷ %d = %d and %d ÷ %d = %d, giving %d : %d."
                      % (A, k, a, B, k, b, a, b)],
                     placeholder="first number")

    def simplify_second():
        return _numq("Write the ratio %d : %d in its simplest form. Type the "
                     "second number of the simplified ratio." % (A, B), b,
                     ["Divide both numbers by their HCF, %d." % k,
                      "%d : %d simplifies to %d : %d." % (A, B, a, b)],
                     placeholder="second number")

    def hcf_step():
        return _numq("To write %d : %d in its simplest form you divide both "
                     "numbers by their highest common factor. What is that HCF?"
                     % (A, B), k,
                     ["%d = %d × %d and %d = %d × %d." % (A, k, a, B, k, b),
                      "The HCF is %d." % k], placeholder="the HCF")

    def from_counts():
        one, two = pick(_PAIRS)
        return _numq("A box holds %d %s and %d %s. Write the ratio of %s to %s "
                     "in its simplest form and type the first number."
                     % (A, one, B, two, one, two), a,
                     ["The ratio is %d : %d." % (A, B),
                      "Dividing both parts by %d gives %d : %d." % (k, a, b)],
                     placeholder="first number")

    def equivalent_second():
        return _numq("Complete the equivalent ratio:  %d : %d = %d : ___"
                     % (a, b, a * k), b * k,
                     ["%d × %d = %d, so both parts are multiplied by %d."
                      % (a, k, a * k, k),
                      "%d × %d = %d." % (b, k, b * k)])

    def equivalent_first():
        return _numq("Complete the equivalent ratio:  %d : %d = ___ : %d"
                     % (a, b, b * k), a * k,
                     ["Both parts are multiplied by %d." % k,
                      "%d × %d = %d." % (a, k, a * k)])

    def find_multiplier():
        return _numq("The ratio %d : %d has been scaled up to %d : %d. What "
                     "number were both parts multiplied by?"
                     % (a, b, a * k, b * k), k,
                     ["%d ÷ %d = %d." % (a * k, a, k),
                      "Check: %d × %d = %d." % (b, k, b * k)],
                     placeholder="a number")

    def three_part():
        c = random.randint(2, 6)
        m = random.randint(2, 5)
        return _numq("Write the ratio %d : %d : %d in its simplest form and "
                     "type the middle number." % (a * m, b * m, c * m), b,
                     ["Every part divides by %d." % m,
                      "The simplified ratio is %d : %d : %d." % (a, b, c)],
                     placeholder="middle number")

    def measure_ratio():
        cm = random.randint(2, 9) * 10
        m = random.randint(2, 6)
        g = _hcf(cm, m * 100)
        return _numq("A rope is %d cm long and a second rope is %d m long. Using "
                     "the same units, write the ratio of the first length to the "
                     "second in its simplest form. Type the first number."
                     % (cm, m), cm // g,
                     ["%d m = %d cm." % (m, m * 100),
                      "%d : %d simplifies to %d : %d."
                      % (cm, m * 100, cm // g, (m * 100) // g)],
                     placeholder="first number")

    def ratio_table():
        n = 4
        mults = sorted(random.sample(range(1, 10), n))
        rows = [[str(a * m), str(b * m)] for m in mults]
        i = random.randrange(n)
        rows[i][1] = ""
        return _dtq("This table keeps the ratio %d : %d in every row. What number "
                    "is missing?" % (a, b), ["Part A", "Part B"], rows,
                    b * mults[i],
                    ["%d ÷ %d = %d, so Part B is %d × %d = %d."
                     % (a * mults[i], a, mults[i], b, mults[i], b * mults[i])],
                    missing=(i, 1), caption="Ratio table")

    def already_simplest():
        if random.random() < 0.5:
            return _wordq("Is the ratio %d : %d already in its simplest form? "
                          "Type yes or no." % (a, b), "yes",
                          ["The HCF of %d and %d is 1." % (a, b),
                           "So %d : %d is already simplest." % (a, b)],
                          placeholder="yes or no")
        return _wordq("Is the ratio %d : %d already in its simplest form? Type "
                      "yes or no." % (A, B), "no",
                      ["Both %d and %d divide by %d." % (A, B, k),
                       "%d : %d simplifies to %d : %d." % (A, B, a, b)],
                      placeholder="yes or no")

    def ratio_as_fraction():
        one, two = pick(_PAIRS)
        return _fracq("The ratio of %s to %s is %d : %d. Write this as a fraction "
                      "(%s ÷ %s)." % (one, two, A, B, one, two), a, b,
                      ["%d : %d as a fraction is %d/%d = %d/%d."
                       % (A, B, A, B, a, b)])

    opts = [simplify_first, simplify_second, from_counts, equivalent_second,
            equivalent_first, ratio_table, hcf_step, find_multiplier]
    if d == 0:
        opts = [simplify_first, simplify_second, from_counts, equivalent_second,
                equivalent_first, ratio_table, hcf_step]
    elif d == 2:
        opts = [simplify_first, simplify_second, three_part, measure_ratio,
                already_simplest, ratio_as_fraction, ratio_table,
                find_multiplier, equivalent_first]
    opts = opts + [ratio_table, ratio_table]
    return pick(opts)()


# ================================================================= 8.4.b =====
@skill("Y8.4.b", "Divide a quantity in a given ratio", S4)
def _(d=1):
    d = _t(d)
    a, b = _coprime_pair(1, _by_d(d, 4, 6, 8))
    if a + b > 13:
        a, b = _coprime_pair(1, 5)
    unit = _by_d(d, random.randint(2, 8), random.randint(3, 15),
                 random.randint(6, 30))
    total = (a + b) * unit

    def strip_one_part():
        return _share_strip("%s is shared in the ratio %d : %d. The bar model "
                            "shows the %d equal parts. How much is one part "
                            "worth, in pounds?"
                            % (_pounds(total), a, b, a + b),
                            a + b, _pounds(total), unit,
                            ["The ratio %d : %d needs %d equal parts."
                             % (a, b, a + b),
                             "%d ÷ %d = %d, so one part is %s."
                             % (total, a + b, unit, _pounds(unit))])

    def strip_total():
        return _total_strip("Money is shared in the ratio %d : %d, so there are "
                            "%d equal parts. Each part is worth %s. What is the "
                            "total, in pounds?"
                            % (a, b, a + b, _pounds(unit)),
                            a + b, _pounds(unit), total,
                            ["%d parts × %s = %s."
                             % (a + b, _pounds(unit), _pounds(total))])

    def larger_share():
        one, two = _two_names()
        big = max(a, b)
        who = one if a >= b else two
        return _numq("%s and %s share %s in the ratio %d : %d, with %s taking "
                     "the larger share. How much does %s get, in pounds?"
                     % (one, two, _pounds(total), a, b, who, who), big * unit,
                     ["One part is %d ÷ %d = %s." % (total, a + b, _pounds(unit)),
                      "%d × %s = %s." % (big, _pounds(unit), _pounds(big * unit))],
                     unit="£")

    def smaller_share():
        return _numq("%d sweets are shared in the ratio %d : %d. How many sweets "
                     "are in the smaller share?" % (total, a, b), min(a, b) * unit,
                     ["One part is %d ÷ %d = %d sweets." % (total, a + b, unit),
                      "%d × %d = %d sweets."
                      % (min(a, b), unit, min(a, b) * unit)], unit="sweets")

    def difference():
        if a == b:
            return larger_share()
        diff = abs(a - b) * unit
        return _numq("%d marbles are shared in the ratio %d : %d. What is the "
                     "difference between the two shares?" % (total, a, b), diff,
                     ["One part is %d ÷ %d = %d marbles." % (total, a + b, unit),
                      "The shares are %d and %d, differing by %d."
                      % (a * unit, b * unit, diff)], unit="marbles")

    def total_from_share():
        one, two = _two_names()
        return _numq("%s and %s share stickers in the ratio %d : %d. %s takes the "
                     "%d-part share and receives %d stickers. How many stickers "
                     "were shared altogether?"
                     % (one, two, a, b, one, a, a * unit), total,
                     ["One part is %d ÷ %d = %d." % (a * unit, a, unit),
                      "%d parts × %d = %d stickers." % (a + b, unit, total)],
                     unit="stickers")

    def three_way_strip():
        c = random.randint(1, 4)
        parts = a + b + c
        if parts > 13:
            return strip_one_part()
        u = random.randint(3, 12)
        tot = parts * u
        return _share_strip("%d counters are shared in the ratio %d : %d : %d. "
                            "The bar model shows the %d equal parts. How many "
                            "counters are in one part?"
                            % (tot, a, b, c, parts), parts, str(tot), u,
                            ["%d + %d + %d = %d parts." % (a, b, c, parts),
                             "%d ÷ %d = %d counters per part."
                             % (tot, parts, u)])

    def fraction_of_total():
        return _fracq("A ribbon is cut in the ratio %d : %d. What fraction of the "
                      "ribbon is the %d-part piece?" % (a, b, a), a, a + b,
                      ["There are %d equal parts." % (a + b),
                       "The %d-part piece is %d/%d." % (a, a, a + b)])

    def table_shares():
        one, two = _two_names()
        rows = [[one, "%d parts" % a, ""], [two, "%d parts" % b, str(b * unit)]]
        return _dtq("%s and %s share %d beads in the ratio %d : %d. How many "
                    "beads does %s get?" % (one, two, total, a, b, one),
                    ["Name", "Share", "Beads"], rows, a * unit,
                    ["One part is %d ÷ %d = %d beads." % (total, a + b, unit),
                     "%s has %d parts: %d beads." % (one, a, a * unit)],
                    missing=(0, 2), caption="Sharing %d beads" % total)

    opts = [strip_one_part, strip_total, larger_share, smaller_share,
            total_from_share, table_shares, fraction_of_total, three_way_strip]
    if d == 0:
        opts = [strip_one_part, strip_total, smaller_share, larger_share,
                table_shares, fraction_of_total, three_way_strip]
    elif d == 2:
        opts = [difference, total_from_share, three_way_strip, larger_share,
                smaller_share, table_shares, strip_one_part, fraction_of_total]
    opts = opts + [strip_one_part, table_shares]
    return pick(opts)()


# ================================================================= 8.4.c =====
@skill("Y8.4.c", "Compare ratios and ratio word problems", S4)
def _(d=1):
    d = _t(d)

    def which_stronger():
        # two mixtures a1:b1 and a2:b2; which has the higher proportion of first
        one, two = pick([("orange", "water"), ("blackcurrant", "water"),
                         ("red paint", "white paint")])
        a1, b1 = random.randint(1, 5), random.randint(2, 6)
        a2, b2 = random.randint(1, 5), random.randint(2, 6)
        f1, f2 = Fraction(a1, a1 + b1), Fraction(a2, a2 + b2)
        while f1 == f2:
            a2, b2 = random.randint(1, 5), random.randint(2, 6)
            f2 = Fraction(a2, a2 + b2)
        ans = "A" if f1 > f2 else "B"
        return _wordq("Drink A mixes %s and %s in the ratio %d : %d. Drink B "
                      "mixes them in the ratio %d : %d. Which drink has the "
                      "stronger %s taste? Type A or B."
                      % (one, two, a1, b1, a2, b2, one),
                      ans,
                      ["Fraction of %s in A: %d/%d = %s."
                       % (one, a1, a1 + b1, _dstr(round(float(f1), 3))),
                       "Fraction in B: %d/%d = %s."
                       % (a2, a2 + b2, _dstr(round(float(f2), 3))),
                       "Drink %s is stronger." % ans], placeholder="A or B")

    def same_ratio():
        a, b = _coprime_pair(2, 6)
        k1 = random.randint(2, 6)
        if random.random() < 0.5:
            return _wordq("Are the ratios %d : %d and %d : %d equal? Type yes or "
                          "no." % (a * k1, b * k1, a, b), "yes",
                          ["%d : %d divides by %d to give %d : %d."
                           % (a * k1, b * k1, k1, a, b)],
                          placeholder="yes or no")
        off = pick([1, 2])
        return _wordq("Are the ratios %d : %d and %d : %d equal? Type yes or no."
                      % (a * k1, b * k1 + off, a, b), "no",
                      ["%d : %d would need %d : %d to match, but the second part "
                       "is %d." % (a * k1, b * k1, a * k1, b * k1, b * k1 + off)],
                      placeholder="yes or no")

    def word_scale():
        one, two = pick(_PEOPLE)
        a, b = _coprime_pair(2, 6)
        k = _by_d(d, random.randint(2, 4), random.randint(2, 7),
                  random.randint(4, 12))
        return _numq("In a club the ratio of %s to %s is %d : %d. There are %d "
                     "%s. How many %s are there?"
                     % (one, two, a, b, a * k, one, two), b * k,
                     ["Each part is worth %d ÷ %d = %d." % (a * k, a, k),
                      "%d × %d = %d %s." % (b, k, b * k, two)], unit=two)

    def compare_prices():
        n1, n2 = random.randint(3, 8), random.randint(3, 8)
        while n2 == n1:
            n2 = random.randint(3, 8)
        each = random.randint(20, 90)
        # A is cheaper per item by construction
        pa = each
        pb = each + random.randint(2, 15)
        who = "A"
        return _wordq("Shop A sells %d pens for %s. Shop B sells %d pens for %s. "
                      "Which shop is cheaper per pen? Type A or B."
                      % (n1, money(n1 * pa), n2, money(n2 * pb)), who,
                      ["Shop A: %d ÷ %d = %dp each." % (n1 * pa, n1, pa),
                       "Shop B: %d ÷ %d = %dp each." % (n2 * pb, n2, pb),
                       "Shop A is cheaper."], placeholder="A or B")

    def combine_ratios():
        # a:b and b:c -> find a:c style, ask the a part when scaled so b matches
        a, b = _coprime_pair(2, 5)
        c = random.randint(2, 6)
        # ratio A:B = a:b, B:C = b:c already share b
        return _numq("In a recipe, flour : sugar = %d : %d and sugar : butter = "
                     "%d : %d. If %d g of sugar is used, how much flour is used, "
                     "in grams?" % (a, b, b, c, b), a,
                     ["Flour : sugar = %d : %d, and %d g of sugar means %d g of "
                      "flour." % (a, b, b, a)], unit="g")

    def table_compare():
        a, b = _coprime_pair(2, 6)
        m = random.randint(2, 6)
        if random.random() < 0.5:
            rows = [["Recipe A", str(a), str(b)],
                    ["Recipe B", str(a * m), str(b * m)]]
            return _dtq("The table shows the ratio of cocoa to milk in two hot "
                        "chocolate recipes. Are the two recipes in the same "
                        "ratio? Type yes or no.",
                        ["Recipe", "Cocoa", "Milk"], rows, "yes",
                        ["Recipe A is %d : %d." % (a, b),
                         "Recipe B is %d : %d = %d : %d, the same ratio."
                         % (a * m, b * m, a, b)],
                        caption="Hot chocolate", answer_type="str")
        rows = [["Recipe A", str(a), str(b)],
                ["Recipe B", str(a * m), str(b * m + pick([1, 2]))]]
        return _dtq("The table shows the ratio of cocoa to milk in two hot "
                    "chocolate recipes. Are the two recipes in the same ratio? "
                    "Type yes or no.",
                    ["Recipe", "Cocoa", "Milk"], rows, "no",
                    ["Recipe A is %d : %d." % (a, b),
                     "Recipe B is not a whole multiple of that, so they differ."],
                    caption="Hot chocolate", answer_type="str")

    def best_value_word():
        n1, n2 = random.randint(4, 10), random.randint(4, 10)
        while n2 == n1:
            n2 = random.randint(4, 10)
        cheaper_each = random.randint(15, 40)
        dearer_each = cheaper_each + random.randint(3, 12)
        # cheaper pack -> compute its unit price answer
        return _numq("Pack A holds %d bars for %s. Pack B holds %d bars for %s. "
                     "What is the cost of one bar from the better-value pack, in "
                     "pence?"
                     % (n1, money(n1 * cheaper_each), n2,
                        money(n2 * dearer_each)), cheaper_each,
                     ["Pack A: %d ÷ %d = %dp each."
                      % (n1 * cheaper_each, n1, cheaper_each),
                      "Pack B: %d ÷ %d = %dp each."
                      % (n2 * dearer_each, n2, dearer_each),
                      "Pack A is better value at %dp each." % cheaper_each],
                     unit="p")

    def scale_both():
        one, two = pick(_PAIRS)
        a, b = _coprime_pair(2, 6)
        k = random.randint(2, 8)
        return _numq("A pattern uses %s and %s in the ratio %d : %d. If %d %s are "
                     "used, how many items are used in total?"
                     % (one, two, a, b, a * k, one), (a + b) * k,
                     ["Each part is %d ÷ %d = %d." % (a * k, a, k),
                      "%d parts × %d = %d items." % (a + b, k, (a + b) * k)])

    def reasonable_answer():
        # multi-step word problem; identify the answer of the right magnitude
        people = random.randint(12, 40)
        each = random.randint(3, 9)
        extra = random.randint(15, 60)
        exact = people * each + extra
        scene = pick([
            "people each pay £%d for a ticket, and the group also pays £%d "
            "to hire a coach" % (each, extra),
            "members each pay £%d for a shirt, and the club also pays £%d "
            "for a trophy" % (each, extra),
            "guests each pay £%d for a meal, and the host also pays £%d "
            "for a cake" % (each, extra)])
        vals = [exact, exact // 10, exact * 10]
        order = random.sample(range(3), 3)
        shown = [vals[i] for i in order]
        ans = ["A", "B", "C"][order.index(0)]
        return _wordq(
            "Multi-step word problem: a group of %d %s. Which of these is the "
            "most reasonable answer for the total cost?  A) £%d   B) £%d   "
            "C) £%d.  Type the letter of the reasonable answer."
            % (people, scene, shown[0], shown[1], shown[2]), ans,
            ["Estimate: about %d × £%d = £%d, plus £%d, giving about £%d."
             % (people, each, people * each, extra, exact),
             "The reasonable total is around £%d, so the answer is %s."
             % (exact, ans)], placeholder="A, B or C")

    opts = [which_stronger, same_ratio, word_scale, compare_prices,
            table_compare, best_value_word, scale_both, reasonable_answer]
    if d == 0:
        opts = [same_ratio, word_scale, compare_prices, best_value_word,
                scale_both, table_compare, reasonable_answer]
    elif d == 2:
        opts = [which_stronger, combine_ratios, compare_prices, best_value_word,
                table_compare, word_scale, scale_both, reasonable_answer]
    opts = opts + [table_compare]
    return pick(opts)()


# ================================================================= 8.4.d =====
@skill("Y8.4.d", "Unit rates and equivalent rates", S4)
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
        return _numq("%d %s cost %s. At the same rate, how much do %d %s cost, in "
                     "pence?" % (n, plur, money(n * each), m, plur), m * each,
                     ["One %s costs %d ÷ %d = %dp." % (sing, n * each, n, each),
                      "%d × %d = %dp." % (m, each, m * each)], unit="p")

    def per_unit_quantity():
        per = random.randint(3, 12)
        boxes = random.randint(4, 12)
        return _numq("A machine packs %d %s into every box. How many %s are in "
                     "%d boxes?" % (per, plur, plur, boxes), per * boxes,
                     ["%d × %d = %d %s." % (per, boxes, per * boxes, plur)],
                     unit=plur)

    def rate_per_minute():
        per_min = random.randint(6, 30)
        m1 = random.randint(3, 9)
        m2 = m1 + random.randint(2, 10)
        return _numq("A printer prints %d pages in %d minutes at a steady rate. "
                     "How many pages does it print in %d minutes?"
                     % (per_min * m1, m1, m2), per_min * m2,
                     ["%d ÷ %d = %d pages per minute."
                      % (per_min * m1, m1, per_min),
                      "%d × %d = %d pages." % (per_min, m2, per_min * m2)],
                     unit="pages")

    def how_many_for():
        each = random.randint(4, 25)
        n = random.randint(3, 9)
        return _numq("One %s costs %dp. How many %s can be bought with exactly "
                     "%s?" % (sing, each, plur, money(each * n)), n,
                     ["%d ÷ %d = %d %s." % (each * n, each, n, plur)], unit=plur)

    def recipe_rate():
        people = pick([2, 3, 4, 5, 6])
        want = people * random.randint(2, _by_d(d, 3, 4, 6))
        per = random.randint(20, 90)
        return _numq("A recipe for %d people uses %d g of rice. How much rice is "
                     "needed for %d people, in grams?"
                     % (people, per * people, want), per * want,
                     ["One person needs %d ÷ %d = %d g."
                      % (per * people, people, per),
                      "%d × %d = %d g." % (per, want, per * want)], unit="g")

    def price_table():
        each = random.randint(6, 45)
        counts = sorted(random.sample(range(2, 15), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else money(c * each)]
                for j, c in enumerate(counts)]
        return _dtq("This price list charges the same for every %s. What is the "
                    "missing price, in pence?" % sing,
                    ["Number of %s" % plur, "Price"], rows, counts[i] * each,
                    ["One %s costs %dp." % (sing, each),
                     "%d × %d = %dp." % (counts[i], each, counts[i] * each)],
                    missing=(i, 1), caption="Price list")

    def rate_table():
        per = random.randint(4, 25)
        counts = sorted(random.sample(range(2, 12), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else str(c * per)]
                for j, c in enumerate(counts)]
        return _dtq("Every crate holds the same number of tiles. How many tiles "
                    "are in %d crates?" % counts[i],
                    ["Crates", "Tiles"], rows, counts[i] * per,
                    ["One crate holds %d tiles." % per,
                     "%d × %d = %d tiles." % (counts[i], per, counts[i] * per)],
                    missing=(i, 1), caption="Tiles per crate")

    def better_buy():
        n1, n2 = random.randint(4, 10), random.randint(4, 10)
        while n2 == n1:
            n2 = random.randint(4, 10)
        cheap = random.randint(12, 35)
        dear = cheap + random.randint(3, 12)
        return _wordq("Bottle A: %d litres for %s. Bottle B: %d litres for %s. "
                      "Which is better value per litre? Type A or B."
                      % (n1, money(n1 * cheap), n2, money(n2 * dear)), "A",
                      ["A: %d ÷ %d = %dp per litre." % (n1 * cheap, n1, cheap),
                       "B: %d ÷ %d = %dp per litre." % (n2 * dear, n2, dear),
                       "Bottle A is cheaper per litre."], placeholder="A or B")

    def exchange():
        rate = pick([5, 6, 8, 10, 12])
        pounds = random.randint(3, 15)
        return _numq("At a fair, £1 buys %d tokens. How many tokens does %s buy?"
                     % (rate, _pounds(pounds)), rate * pounds,
                     ["%d × %d = %d tokens." % (rate, pounds, rate * pounds)],
                     unit="tokens")

    opts = [unit_price, scale_up, per_unit_quantity, rate_per_minute,
            price_table, rate_table, how_many_for, recipe_rate]
    if d == 0:
        opts = [unit_price, scale_up, per_unit_quantity, how_many_for,
                price_table, rate_table, exchange]
    elif d == 2:
        opts = [unit_price, scale_up, rate_per_minute, recipe_rate, better_buy,
                price_table, rate_table, how_many_for]
    opts = opts + [price_table, rate_table]
    return pick(opts)()


# ================================================================= 8.4.e =====
@skill("Y8.4.e", "Speed, distance and time", S4)
def _(d=1):
    d = _t(d)

    def find_speed():
        h = random.randint(2, 8)
        s = _by_d(d, random.randint(20, 60), random.randint(30, 90),
                  random.randint(45, 120))
        return _numq("A coach travels %d km in %d hours at a steady speed. What "
                     "is its average speed, in km/h?" % (s * h, h), s,
                     ["Speed = distance ÷ time = %d ÷ %d = %d km/h."
                      % (s * h, h, s)], unit="km/h")

    def find_distance():
        s = _by_d(d, random.randint(20, 50), random.randint(30, 80),
                  random.randint(50, 110))
        h = random.randint(2, 8)
        return _numq("A train travels at a steady %d km/h for %d hours. How far "
                     "does it travel, in kilometres?" % (s, h), s * h,
                     ["Distance = speed × time = %d × %d = %d km."
                      % (s, h, s * h)], unit="km")

    def find_time():
        s = _by_d(d, random.randint(20, 50), random.randint(30, 70),
                  random.randint(40, 90))
        h = random.randint(2, 8)
        return _numq("A cyclist rides %d km at a steady %d km/h. How many hours "
                     "does the ride take?" % (s * h, s), h,
                     ["Time = distance ÷ speed = %d ÷ %d = %d hours."
                      % (s * h, s, h)], unit="hours")

    def distance_forward():
        s = random.randint(30, 90)
        h1 = random.randint(2, 5)
        h2 = h1 + random.randint(1, 4)
        return _numq("A car travels %d km in %d hours at a steady speed. How far "
                     "does it travel in %d hours, in kilometres?"
                     % (s * h1, h1, h2), s * h2,
                     ["%d ÷ %d = %d km/h." % (s * h1, h1, s),
                      "%d × %d = %d km." % (s, h2, s * h2)], unit="km")

    def minutes_speed():
        # distance in km over a whole number of minutes that divides an hour
        mins = pick([15, 20, 30, 45])
        s = pick([40, 60, 80, 20, 30])
        dist = s * mins // 60
        if dist * 60 != s * mins:
            return find_speed()
        return _numq("A runner covers %d km in %d minutes at a steady speed. What "
                     "is the speed, in km/h?" % (dist, mins), s,
                     ["%d minutes = %d/60 hour." % (mins, mins),
                      "Speed = %d ÷ (%d/60) = %d km/h." % (dist, mins, s)],
                     unit="km/h")

    def time_in_minutes():
        s = pick([60, 30, 40, 90, 20])
        mins = pick([15, 20, 30, 45, 10])
        dist = s * mins // 60
        if dist * 60 != s * mins or dist == 0:
            return find_time()
        return _numq("A bus travels %d km at a steady %d km/h. How many minutes "
                     "does the journey take?" % (dist, s), mins,
                     ["Time = %d ÷ %d = %d/60 hour = %d minutes."
                      % (dist, s, mins, mins)], unit="minutes")

    def two_leg():
        s1 = random.randint(30, 60)
        h1 = random.randint(1, 3)
        s2 = random.randint(30, 60)
        h2 = random.randint(1, 3)
        return _numq("A journey has two parts: %d hours at %d km/h, then %d hours "
                     "at %d km/h. What is the total distance, in kilometres?"
                     % (h1, s1, h2, s2), s1 * h1 + s2 * h2,
                     ["Part 1: %d × %d = %d km." % (s1, h1, s1 * h1),
                      "Part 2: %d × %d = %d km." % (s2, h2, s2 * h2),
                      "Total = %d km." % (s1 * h1 + s2 * h2)], unit="km")

    def average_speed_two_leg():
        s = random.randint(20, 40)
        h_tot = random.randint(3, 6)
        dist = s * h_tot
        return _numq("A journey of %d km takes %d hours in total. What is the "
                     "average speed for the whole journey, in km/h?"
                     % (dist, h_tot), s,
                     ["%d ÷ %d = %d km/h." % (dist, h_tot, s)], unit="km/h")

    def table_speed():
        s = random.randint(20, 60)
        hours = sorted(random.sample(range(1, 8), 4))
        i = random.randrange(4)
        rows = [[str(hh), "" if j == i else str(s * hh)]
                for j, hh in enumerate(hours)]
        return _dtq("A vehicle travels at a steady %d km/h. The table shows "
                    "distance against time. What is the missing distance, in "
                    "kilometres?" % s, ["Time (h)", "Distance (km)"], rows,
                    s * hours[i],
                    ["%d × %d = %d km." % (s, hours[i], s * hours[i])],
                    missing=(i, 1), caption="Steady %d km/h" % s)

    opts = [find_speed, find_distance, find_time, distance_forward, two_leg,
            table_speed, average_speed_two_leg]
    if d == 0:
        opts = [find_speed, find_distance, find_time, table_speed,
                distance_forward]
    elif d == 2:
        opts = [find_speed, find_distance, find_time, minutes_speed,
                time_in_minutes, two_leg, average_speed_two_leg, table_speed]
    opts = opts + [table_speed, table_speed]
    return pick(opts)()


# ================================================================= 8.4.f =====
@skill("Y8.4.f", "Recognise and solve proportions", S4)
def _(d=1):
    d = _t(d)

    def solve_proportion():
        a, b = _coprime_pair(2, 7)
        k = _by_d(d, random.randint(2, 4), random.randint(2, 8),
                  random.randint(4, 12))
        return _numq("Solve the proportion for the missing number:  %d / %d = ___ "
                     "/ %d" % (a, b, b * k), a * k,
                     ["%d ÷ %d = %d, so both parts scale by %d."
                      % (b * k, b, k, k),
                      "%d × %d = %d." % (a, k, a * k)])

    def solve_cross():
        a, b = _coprime_pair(2, 7)
        k = _by_d(d, random.randint(2, 4), random.randint(2, 7),
                  random.randint(4, 10))
        return _numq("Solve the proportion for the missing number:  %d / %d = %d "
                     "/ ___" % (a, b, a * k), b * k,
                     ["%d ÷ %d = %d." % (a * k, a, k),
                      "%d × %d = %d." % (b, k, b * k)])

    def word_proportion():
        n1 = random.randint(2, 6)
        each = random.randint(2, 9)
        n2 = n1 * random.randint(2, _by_d(d, 3, 5, 8))
        return _numq("%d identical books weigh %d g. How much do %d of the same "
                     "books weigh, in grams?" % (n1, n1 * each, n2), n2 * each,
                     ["One book weighs %d ÷ %d = %d g." % (n1 * each, n1, each),
                      "%d × %d = %d g." % (n2, each, n2 * each)], unit="g")

    def inverse_proportion():
        workers1 = random.randint(2, 6)
        days = random.randint(4, 12)
        workers2 = pick([x for x in range(1, 13)
                         if x != workers1 and (workers1 * days) % x == 0])
        return _numq("%d workers take %d days to finish a job. Working at the same "
                     "rate, how many days would %d workers take?"
                     % (workers1, days, workers2),
                     workers1 * days // workers2,
                     ["Total work = %d × %d = %d worker-days."
                      % (workers1, days, workers1 * days),
                      "%d ÷ %d = %d days."
                      % (workers1 * days, workers2, workers1 * days // workers2)],
                     unit="days")

    def is_proportional():
        a, b = random.randint(2, 6), random.randint(3, 9)
        k = random.randint(2, 5)
        if random.random() < 0.5:
            return _wordq("A stall sells %d apples for %dp and %d apples for %dp. "
                          "Is the price directly proportional to the number of "
                          "apples? Type yes or no."
                          % (a, a * 10, a * k, a * k * 10), "yes",
                          ["%dp ÷ %d = 10p each and %dp ÷ %d = 10p each."
                           % (a * 10, a, a * k * 10, a * k),
                           "The rate is the same, so it is proportional."],
                          placeholder="yes or no")
        return _wordq("A stall sells %d apples for %dp and %d apples for %dp. Is "
                      "the price directly proportional to the number of apples? "
                      "Type yes or no."
                      % (a, a * 10, a * k, a * k * 10 + 5), "no",
                      ["%dp ÷ %d = 10p each, but %dp ÷ %d is not 10p each."
                       % (a * 10, a, a * k * 10 + 5, a * k),
                       "The rate changes, so it is not proportional."],
                      placeholder="yes or no")

    def unitary():
        n = random.randint(3, 8)
        each = random.randint(3, 12)
        want = random.randint(2, 15)
        return _numq("%d pencils cost %dp. Using the unitary method, how much do "
                     "%d pencils cost, in pence?" % (n, n * each, want),
                     want * each,
                     ["One pencil costs %d ÷ %d = %dp." % (n * each, n, each),
                      "%d × %d = %dp." % (want, each, want * each)], unit="p")

    def proportion_table():
        each = random.randint(3, 12)
        counts = sorted(random.sample(range(2, 12), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else str(c * each)]
                for j, c in enumerate(counts)]
        return _dtq("The two quantities in this table are in direct proportion. "
                    "What is the missing value?", ["x", "y"], rows,
                    counts[i] * each,
                    ["y is always %d times x." % each,
                     "%d × %d = %d." % (counts[i], each, counts[i] * each)],
                    missing=(i, 1), caption="Direct proportion")

    def recipe_people():
        people = pick([2, 3, 4])
        want = people * random.randint(2, 5)
        per = random.randint(1, 4)
        return _numq("A recipe for %d people needs %d eggs. How many eggs are "
                     "needed for %d people?" % (people, per * people, want),
                     per * want,
                     ["One person needs %d ÷ %d = %d eggs."
                      % (per * people, people, per),
                      "%d × %d = %d eggs." % (per, want, per * want)], unit="eggs")

    opts = [solve_proportion, solve_cross, word_proportion, is_proportional,
            unitary, proportion_table, recipe_people]
    if d == 0:
        opts = [solve_proportion, solve_cross, word_proportion, unitary,
                proportion_table, recipe_people]
    elif d == 2:
        opts = [solve_proportion, solve_cross, inverse_proportion,
                is_proportional, word_proportion, proportion_table, unitary]
    opts = opts + [proportion_table, proportion_table]
    return pick(opts)()


# ================================================================= 8.4.g =====
@skill("Y8.4.g", "Direct proportion; constant of proportionality", S4)
def _(d=1):
    d = _t(d)

    def find_k_table():
        k = _by_d(d, random.randint(2, 5), random.randint(2, 8),
                  random.randint(3, 12))
        xs = sorted(random.sample(range(1, 10), 4))
        rows = [[str(x), str(k * x)] for x in xs]
        return _dtq("y is directly proportional to x. The table shows matching "
                    "values. What is the constant of proportionality k (where "
                    "y = kx)?", ["x", "y"], rows, k,
                    ["k = y ÷ x = %d ÷ %d = %d." % (k * xs[0], xs[0], k)],
                    caption="y = kx")

    def missing_from_table():
        k = _by_d(d, random.randint(2, 5), random.randint(2, 8),
                  random.randint(3, 12))
        xs = sorted(random.sample(range(1, 12), 4))
        i = random.randrange(4)
        rows = [[str(x), "" if j == i else str(k * x)]
                for j, x in enumerate(xs)]
        return _dtq("y is directly proportional to x with y = %dx. What is the "
                    "missing value of y?" % k, ["x", "y"], rows, k * xs[i],
                    ["y = %d × %d = %d." % (k, xs[i], k * xs[i])],
                    missing=(i, 1), caption="y = %dx" % k)

    def y_from_x():
        k = random.randint(2, _by_d(d, 5, 9, 15))
        x = random.randint(2, _by_d(d, 8, 15, 30))
        return _numq("y is directly proportional to x, and y = %dx. Work out y "
                     "when x = %d." % (k, x), k * x,
                     ["y = %d × %d = %d." % (k, x, k * x)])

    def find_k_pair():
        k = random.randint(2, _by_d(d, 6, 10, 15))
        x = random.randint(2, 9)
        return _numq("y is directly proportional to x. When x = %d, y = %d. What "
                     "is the constant of proportionality k?" % (x, k * x), k,
                     ["k = y ÷ x = %d ÷ %d = %d." % (k * x, x, k)],
                     placeholder="value of k")

    def plot_on_line():
        k = pick([1, 2, 3])
        xmax = pick([6, 8, 10])
        ymax = k * xmax
        x = random.randint(1, xmax - 1)
        return _lineq("The line y = %dx shows a direct-proportion relationship. "
                      "Plot the point on the line where x = %d."
                      % (k, x) if k != 1 else
                      "The line y = x shows a direct-proportion relationship. "
                      "Plot the point on the line where x = %d." % x,
                      k, x, xmax, ymax,
                      ["On the line, y = %d × %d = %d." % (k, x, k * x),
                       "Plot (%d, %d)." % (x, k * x)])

    def gradient_is_k():
        k = pick([2, 3, 4, 5])
        xmax = pick([5, 6])
        ymax = k * xmax
        return _numq("A direct-proportion graph is the straight line y = %dx "
                     "through the origin. What is the constant of proportionality "
                     "(the gradient of the line)?" % k, k,
                     ["The graph y = %dx has gradient %d." % (k, k),
                      "So k = %d." % k], placeholder="value of k")

    def scale_value():
        k = random.randint(2, 8)
        x1 = random.randint(2, 6)
        x2 = x1 * random.randint(2, 4)
        return _numq("y is directly proportional to x. When x = %d, y = %d. What "
                     "is y when x = %d?" % (x1, k * x1, x2), k * x2,
                     ["k = %d ÷ %d = %d." % (k * x1, x1, k),
                      "y = %d × %d = %d." % (k, x2, k * x2)])

    def x_from_y():
        k = random.randint(2, 8)
        y = k * random.randint(2, 12)
        return _numq("y is directly proportional to x with y = %dx. What is x "
                     "when y = %d?" % (k, y), y // k,
                     ["x = y ÷ %d = %d ÷ %d = %d." % (k, y, k, y // k)])

    opts = [find_k_table, missing_from_table, y_from_x, find_k_pair,
            plot_on_line, gradient_is_k, scale_value]
    if d == 0:
        opts = [find_k_table, missing_from_table, y_from_x, find_k_pair,
                plot_on_line, gradient_is_k]
    elif d == 2:
        opts = [find_k_table, missing_from_table, find_k_pair, scale_value,
                x_from_y, plot_on_line, gradient_is_k]
    opts = opts + [find_k_table, missing_from_table]
    return pick(opts)()


# ================================================================= 8.4.h =====
@skill("Y8.4.h", "Proportional relationships across graphs and equations", S4)
def _(d=1):
    d = _t(d)

    def which_is_proportional():
        # one table is y=kx (through origin), the other is y=kx+c
        k = random.randint(2, 5)
        c = random.randint(2, 6)
        xs = [1, 2, 3, 4]
        good = [[str(x), str(k * x)] for x in xs]
        bad = [[str(x), str(k * x + c)] for x in xs]
        if random.random() < 0.5:
            return _dtq("Does this table show a directly proportional "
                        "relationship (y = kx through the origin)? Type yes or "
                        "no.", ["x", "y"], good, "yes",
                        ["y ÷ x = %d for every row, and (0, 0) fits."
                         % k], caption="Table", answer_type="str")
        return _dtq("Does this table show a directly proportional relationship "
                    "(y = kx through the origin)? Type yes or no.",
                    ["x", "y"], bad, "no",
                    ["y ÷ x is not constant: %d ÷ 1 = %d but %d ÷ 2 = %s."
                     % (k + c, k + c, 2 * k + c,
                        _dstr(round((2 * k + c) / 2, 2)))],
                    caption="Table", answer_type="str")

    def equation_gives_y():
        k = random.randint(2, _by_d(d, 5, 9, 12))
        x = random.randint(2, _by_d(d, 8, 15, 25))
        return _numq("Two quantities are related by the equation y = %dx. Work "
                     "out y when x = %d." % (k, x), k * x,
                     ["y = %d × %d = %d." % (k, x, k * x)])

    def graph_point_line():
        k = pick([1, 2, 3])
        xmax = pick([6, 8])
        ymax = k * xmax
        x = random.randint(1, xmax - 1)
        lbl = "y = x" if k == 1 else "y = %dx" % k
        return _lineq("The graph shows a proportional relationship, %s. Plot the "
                      "point on the line where x = %d." % (lbl, x),
                      k, x, xmax, ymax,
                      ["On %s, when x = %d, y = %d." % (lbl, x, k * x),
                       "Plot (%d, %d)." % (x, k * x)])

    def write_equation_k():
        k = random.randint(2, 9)
        x = random.randint(2, 8)
        return _numq("y is proportional to x, and the graph passes through "
                     "(%d, %d) as well as the origin. The equation is y = kx. "
                     "What is k?" % (x, k * x), k,
                     ["k = %d ÷ %d = %d." % (k * x, x, k)],
                     placeholder="value of k")

    def compare_two_rates():
        # two proportional graphs, steeper one has bigger k
        ka = random.randint(2, 5)
        kb = ka + random.randint(1, 4)
        return _numq("Line P is y = %dx and line Q is y = %dx. Both pass through "
                     "the origin. Which line is steeper — type its k value (the "
                     "larger constant of proportionality)?" % (ka, kb), kb,
                     ["Line Q has the larger gradient, %d." % kb,
                      "The steeper line has k = %d." % kb],
                     placeholder="a number")

    def equation_from_table():
        k = random.randint(2, 9)
        xs = [2, 4, 6]
        rows = [[str(x), str(k * x)] for x in xs]
        return _dtq("This table shows a proportional relationship. It can be "
                    "written as y = kx. What is k?", ["x", "y"], rows, k,
                    ["k = %d ÷ %d = %d." % (k * xs[0], xs[0], k)],
                    caption="y = kx")

    def unit_rate_from_graph():
        k = random.randint(2, 8)
        return _numq("A proportional graph of cost against number of tickets "
                     "passes through the origin and through (%d, %d), where cost "
                     "is in pounds. What is the cost of ONE ticket, in pounds?"
                     % (5, 5 * k), k,
                     ["%d tickets cost £%d, so one ticket costs %d ÷ %d = £%d."
                      % (5, 5 * k, 5 * k, 5, k)], unit="£")

    opts = [which_is_proportional, equation_gives_y, graph_point_line,
            write_equation_k, equation_from_table, unit_rate_from_graph]
    if d == 0:
        opts = [equation_gives_y, graph_point_line, write_equation_k,
                equation_from_table, unit_rate_from_graph]
    elif d == 2:
        opts = [which_is_proportional, equation_gives_y, graph_point_line,
                compare_two_rates, equation_from_table, unit_rate_from_graph,
                write_equation_k]
    opts = opts + [which_is_proportional, equation_from_table]
    return pick(opts)()


# ================================================================= 8.4.i =====
@skill("Y8.4.i", "Constant rate of change from tables and graphs", S4)
def _(d=1):
    d = _t(d)

    def rate_from_table():
        m = _by_d(d, random.randint(2, 5), random.randint(2, 8),
                  random.randint(3, 12))
        c = random.randint(0, _by_d(d, 3, 8, 15))
        xs = sorted(random.sample(range(0, 8), 4))
        rows = [[str(x), str(m * x + c)] for x in xs]
        return _dtq("The values in this table change at a constant rate. By how "
                    "much does y increase for every increase of 1 in x?",
                    ["x", "y"], rows, m,
                    ["Between rows, y goes up by %d each time x goes up by 1."
                     % m], caption="Constant rate")

    def next_value():
        m = random.randint(2, _by_d(d, 6, 10, 15))
        c = random.randint(1, 12)
        xs = [1, 2, 3, 4]
        i = 3
        rows = [[str(x), "" if j == i else str(m * x + c)]
                for j, x in enumerate(xs)]
        return _dtq("The y-values in this table go up by the same amount each "
                    "step. What is the missing value?", ["x", "y"], rows,
                    m * xs[i] + c,
                    ["Each step adds %d, so after %d the next value is %d."
                     % (m, m * xs[i - 1] + c, m * xs[i] + c)],
                    missing=(i, 1), caption="Constant rate")

    def rate_word():
        start = random.randint(5, 20)
        per = random.randint(2, 8)
        hours = random.randint(3, 8)
        return _numq("A tank starts with %d litres and fills at a steady %d "
                     "litres per hour. How much water is in the tank after %d "
                     "hours, in litres?" % (start, per, hours),
                     start + per * hours,
                     ["Added: %d × %d = %d litres." % (per, hours, per * hours),
                      "%d + %d = %d litres." % (start, per * hours,
                                                start + per * hours)],
                     unit="litres")

    def rate_from_two_points():
        m = random.randint(2, 9)
        x1 = random.randint(1, 4)
        x2 = x1 + random.randint(2, 5)
        c = random.randint(0, 8)
        return _numq("A straight-line graph passes through (%d, %d) and (%d, %d). "
                     "What is its rate of change (the increase in y for each "
                     "increase of 1 in x)?"
                     % (x1, m * x1 + c, x2, m * x2 + c), m,
                     ["Change in y = %d − %d = %d." % (m * x2 + c, m * x1 + c,
                                                       m * (x2 - x1)),
                      "Change in x = %d − %d = %d." % (x2, x1, x2 - x1),
                      "Rate = %d ÷ %d = %d." % (m * (x2 - x1), x2 - x1, m)],
                     placeholder="rate of change")

    def gradient_scatter():
        # points on a line y = mx + c, ask the constant rate from line of best fit
        m = random.randint(2, 6)
        c = random.randint(1, 6)
        xs = [1, 2, 3, 4, 5]
        pts = [[x, m * x + c] for x in xs]
        return _scatterq("The points lie exactly on the drawn straight line. By "
                         "how much does y increase each time x increases by 1?",
                         pts, m, "num",
                         ["From x=1 to x=2, y rises from %d to %d, a rise of %d."
                          % (m + c, 2 * m + c, m),
                          "The constant rate is %d." % m],
                         "x", "y", line=([1, m + c], [5, 5 * m + c]),
                         placeholder="a number")

    def cost_rate():
        base = random.randint(2, 8)
        per = random.randint(2, 7)
        return _numq("A plumber charges a £%d call-out fee plus £%d per hour. The "
                     "total cost rises at a constant rate. By how many pounds "
                     "does the cost rise for each extra hour?" % (base, per), per,
                     ["The hourly rate is £%d, so each extra hour adds £%d."
                      % (per, per)], unit="£")

    opts = [rate_from_table, next_value, rate_word, rate_from_two_points,
            gradient_scatter, cost_rate]
    if d == 0:
        opts = [rate_from_table, next_value, rate_word, cost_rate]
    elif d == 2:
        opts = [rate_from_table, rate_from_two_points, gradient_scatter,
                rate_word, next_value, cost_rate]
    opts = opts + [rate_from_table, next_value]
    return pick(opts)()


# ================================================================= 8.4.j =====
@skill("Y8.4.j", "Scale drawings, maps and scale factors", S4)
def _(d=1):
    d = _t(d)

    def drawing_to_real():
        rep = pick([2, 4, 5, 10, 20, 50])
        cm = random.randint(2, _by_d(d, 8, 12, 20))
        return _numq("On a plan, 1 cm represents %d m. A wall is drawn %d cm "
                     "long. How long is the real wall, in metres?" % (rep, cm),
                     rep * cm,
                     ["Each cm stands for %d m." % rep,
                      "%d × %d = %d m." % (cm, rep, rep * cm)], unit="m")

    def real_to_drawing():
        rep = pick([2, 4, 5, 10, 20, 25])
        cm = random.randint(2, _by_d(d, 8, 12, 18))
        return _numq("On a plan, 1 cm represents %d m. A path is %d m long in "
                     "real life. How long is it on the plan, in centimetres?"
                     % (rep, rep * cm), cm,
                     ["%d ÷ %d = %d cm." % (rep * cm, rep, cm)], unit="cm")

    def map_km():
        rep = pick([2, 3, 5, 10])
        cm = random.randint(3, 12)
        return _numq("On a map, 1 cm represents %d km. Two towns are %d cm apart "
                     "on the map. What is the real distance, in kilometres?"
                     % (rep, cm), rep * cm,
                     ["%d × %d = %d km." % (cm, rep, rep * cm)], unit="km")

    def ratio_scale_cm():
        k = pick([100, 200, 500, 1000])
        model_cm = random.randint(3, 15)
        return _numq("A map has a scale of 1 : %d. A road is %d cm long on the "
                     "map. How long is the real road, in centimetres?"
                     % (k, model_cm), k * model_cm,
                     ["A scale of 1 : %d means real length is %d × map length."
                      % (k, k),
                      "%d × %d = %d cm." % (model_cm, k, k * model_cm)],
                     unit="cm")

    def ratio_scale_to_m():
        k = pick([100, 200, 500])
        cm = random.randint(2, 12)
        real_cm = k * cm
        return _numq("A drawing has a scale of 1 : %d. A line is %d cm long on the "
                     "drawing. How long is the real object, in metres? (100 cm = "
                     "1 m)" % (k, cm), real_cm // 100,
                     ["Real length = %d × %d = %d cm." % (cm, k, real_cm),
                      "%d cm ÷ 100 = %d m." % (real_cm, real_cm // 100)],
                     unit="m")

    def scale_factor():
        w = random.randint(3, 12)
        k = random.randint(2, _by_d(d, 4, 6, 9))
        return _numq("A shape has a side of %d cm. After an enlargement the same "
                     "side is %d cm. What is the scale factor?" % (w, w * k), k,
                     ["%d ÷ %d = %d." % (w * k, w, k)],
                     placeholder="scale factor")

    def enlarge_side():
        w = random.randint(3, 10)
        h = random.randint(3, 10)
        while h == w:
            h = random.randint(3, 10)
        k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
                  random.randint(4, 9))
        return _numq("A rectangle measures %d cm by %d cm. It is enlarged by a "
                     "scale factor of %d. How long is the longer side of the new "
                     "rectangle, in centimetres?" % (w, h, k), max(w, h) * k,
                     ["The longer side is %d cm." % max(w, h),
                      "%d × %d = %d cm." % (max(w, h), k, max(w, h) * k)],
                     unit="cm")

    def similar_missing():
        w = random.randint(2, 9)
        h = random.randint(2, 9)
        while h == w:
            h = random.randint(2, 9)
        k = _by_d(d, 2, random.randint(2, 4), random.randint(3, 7))
        return _numq("Two rectangles are similar. The smaller measures %d cm by "
                     "%d cm. The larger has a shorter side of %d cm. How long is "
                     "the longer side of the larger rectangle, in centimetres?"
                     % (w, h, min(w, h) * k), max(w, h) * k,
                     ["Scale factor = %d ÷ %d = %d." % (min(w, h) * k,
                                                        min(w, h), k),
                      "%d × %d = %d cm." % (max(w, h), k, max(w, h) * k)],
                     unit="cm")

    def scale_table():
        rep = pick([2, 5, 10, 20])
        drawn = sorted(random.sample(range(1, 14), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else str(c * rep)]
                for j, c in enumerate(drawn)]
        return _dtq("This table converts plan lengths into real lengths. 1 cm on "
                    "the plan represents %d m. What is the missing real length, "
                    "in metres?" % rep, ["Plan (cm)", "Real (m)"], rows,
                    drawn[i] * rep,
                    ["%d × %d = %d m." % (drawn[i], rep, drawn[i] * rep)],
                    missing=(i, 1), caption="Plan of a field")

    def multi_step_metric():
        # multi-step problem with metric unit conversions (scale, then m -> cm)
        rep = pick([2, 5, 10, 20])
        plan_cm = random.randint(3, 12)
        real_m = plan_cm * rep
        real_cm = real_m * 100
        return _numq(
            "Multi-step problem with metric unit conversions: on a plan, 1 cm "
            "represents %d m. A path is drawn %d cm long. Work out the real "
            "length, then convert it into centimetres (1 m = 100 cm). Give the "
            "real length in centimetres." % (rep, plan_cm), real_cm,
            ["Real length = %d × %d = %d m." % (plan_cm, rep, real_m),
             "Convert: %d m × 100 = %d cm." % (real_m, real_cm)], unit="cm")

    opts = [drawing_to_real, real_to_drawing, map_km, ratio_scale_cm,
            scale_factor, enlarge_side, scale_table, multi_step_metric]
    if d == 0:
        opts = [drawing_to_real, real_to_drawing, map_km, scale_factor,
                enlarge_side, scale_table]
    elif d == 2:
        opts = [ratio_scale_cm, ratio_scale_to_m, scale_factor, similar_missing,
                enlarge_side, map_km, scale_table, multi_step_metric]
    opts = opts + [scale_table, scale_table]
    return pick(opts)()


# ============================================================================
# ============================ 8.5 PERCENTAGES ===============================
# ============================================================================
_NICE_PCT = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]


def _pct_of(pct, base):
    """Exact integer percent of an integer base, requires divisibility."""
    return base * pct // 100


# ================================================================= 8.5.a =====
@skill("Y8.5.a", "Convert percentages, fractions and decimals", S5)
def _(d=1):
    d = _t(d)

    def pct_to_decimal():
        pct = pick([5, 12, 25, 40, 7, 60, 90, 15, 35, 48, 8])
        return _decq("Write %d%% as a decimal." % pct, _dstr(Decimal(pct) / 100),
                     ["%d%% means %d out of 100." % (pct, pct),
                      "%d ÷ 100 = %s." % (pct, _dstr(Decimal(pct) / 100))])

    def decimal_to_pct():
        dec = pick(["0.3", "0.45", "0.7", "0.08", "0.62", "0.9", "0.25", "0.14"])
        pct = int(Decimal(dec) * 100)
        return _numq("Write %s as a percentage." % dec, pct,
                     ["Multiply by 100: %s × 100 = %d%%." % (dec, pct)],
                     unit="%")

    def pct_to_fraction():
        pct = pick([10, 20, 25, 40, 50, 60, 75, 80, 5, 15])
        return _fracq("Write %d%% as a fraction in its simplest form." % pct,
                      pct, 100,
                      ["%d%% = %d/100." % (pct, pct),
                       "%d/100 simplifies to %d/%d."
                       % (pct, *_simp(pct, 100))])

    def fraction_to_pct():
        num, den = pick([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (1, 10),
                         (7, 10), (1, 20), (13, 20), (1, 25)])
        pct = num * 100 // den
        return _numq("Write the fraction %d/%d as a percentage." % (num, den),
                     pct,
                     ["%d/%d = %d ÷ %d = %d hundredths." % (num, den, num, den,
                                                            pct),
                      "So %d/%d = %d%%." % (num, den, pct)], unit="%")

    def fraction_to_decimal():
        num, den = pick([(1, 2), (1, 4), (3, 4), (1, 5), (3, 5), (1, 10),
                         (7, 10), (1, 20), (1, 8), (3, 8)])
        return _decq("Write the fraction %d/%d as a decimal." % (num, den),
                     _dstr(Decimal(num) / Decimal(den)),
                     ["%d ÷ %d = %s." % (num, den,
                                         _dstr(Decimal(num) / Decimal(den)))])

    def decimal_to_fraction():
        dec, num, den = pick([("0.5", 1, 2), ("0.25", 1, 4), ("0.75", 3, 4),
                              ("0.2", 1, 5), ("0.4", 2, 5), ("0.1", 1, 10),
                              ("0.3", 3, 10), ("0.05", 1, 20)])
        return _fracq("Write the decimal %s as a fraction in its simplest form."
                      % dec, num, den,
                      ["%s = %s." % (dec, "%d/%d" % (num, den))])

    def order_which_biggest():
        # compare a fraction, a decimal, a percentage
        vals = [("1/2", Fraction(1, 2)), ("0.6", Fraction(3, 5)),
                ("45%", Fraction(45, 100)), ("3/4", Fraction(3, 4)),
                ("0.35", Fraction(35, 100)), ("70%", Fraction(70, 100))]
        chosen = random.sample(vals, 3)
        biggest = max(chosen, key=lambda t: t[1])
        return _wordq("Which of these is the largest:  %s ,  %s ,  %s ? Type it "
                      "exactly as shown."
                      % (chosen[0][0], chosen[1][0], chosen[2][0]),
                      biggest[0],
                      ["As decimals: %s."
                       % ", ".join("%s = %s"
                                   % (c[0], _dstr(round(float(c[1]), 3)))
                                   for c in chosen),
                       "The largest is %s." % biggest[0]],
                      placeholder="one of the three")

    def complete_triple():
        pct, dec, num, den = pick([(50, "0.5", 1, 2), (25, "0.25", 1, 4),
                                   (20, "0.2", 1, 5), (10, "0.1", 1, 10),
                                   (75, "0.75", 3, 4), (40, "0.4", 2, 5)])
        return _numq("%s = ___%% . What percentage goes in the blank?"
                     % ("%d/%d" % (num, den)), pct,
                     ["%d/%d = %s = %d%%." % (num, den, dec, pct)], unit="%")

    def conversion_table():
        # equivalent fraction / decimal / percentage table with one blank
        triples = [(1, 2, "0.5", 50), (1, 4, "0.25", 25), (3, 4, "0.75", 75),
                   (1, 5, "0.2", 20), (2, 5, "0.4", 40), (3, 5, "0.6", 60),
                   (1, 10, "0.1", 10), (7, 10, "0.7", 70), (1, 20, "0.05", 5)]
        chosen = random.sample(triples, 3)
        col = 1  # always blank the decimal column (unambiguous typed value)
        rows = []
        i = random.randrange(3)
        for j, (num, den, dec, pct) in enumerate(chosen):
            frac = "%d/%d" % (num, den)
            if j == i:
                row = [frac, "" if col == 1 else dec,
                       "" if col == 2 else ("%d%%" % pct)]
            else:
                row = [frac, dec, "%d%%" % pct]
            rows.append(row)
        n, dn, dec, pct = chosen[i]
        if col == 1:
            ans, at, sol = dec, "num", ["%d/%d = %s." % (n, dn, dec)]
            what = "decimal"
        else:
            ans, at, sol = pct, "int", ["%d/%d = %d%%." % (n, dn, pct)]
            what = "percentage"
        return _dtq("Complete the equivalents table: what is the missing %s?"
                    % what, ["Fraction", "Decimal", "Percentage"], rows, ans,
                    sol, missing=(i, col), caption="Equivalent values",
                    answer_type=at)

    opts = [pct_to_decimal, decimal_to_pct, pct_to_fraction, fraction_to_pct,
            fraction_to_decimal, decimal_to_fraction, complete_triple,
            conversion_table]
    if d == 0:
        opts = [pct_to_decimal, decimal_to_pct, pct_to_fraction,
                fraction_to_pct, complete_triple, conversion_table]
    elif d == 2:
        opts = [pct_to_fraction, fraction_to_pct, fraction_to_decimal,
                decimal_to_fraction, order_which_biggest, complete_triple,
                pct_to_decimal, conversion_table]
    opts = opts + [conversion_table, conversion_table]
    return pick(opts)()


# ================================================================= 8.5.b =====
@skill("Y8.5.b", "Percentage of a quantity", S5)
def _(d=1):
    d = _t(d)

    def pct_of_number():
        pct = pick(_NICE_PCT)
        base = random.randint(2, _by_d(d, 12, 25, 60)) * (100 // _hcf(pct, 100))
        # ensure integer result: pick base multiple of 100/gcd
        g = _hcf(pct, 100)
        step = 100 // g
        base = step * random.randint(2, _by_d(d, 10, 25, 60))
        ans = base * pct // 100
        return _numq("Work out %d%% of %d." % (pct, base), ans,
                     ["%d%% of %d = %d × %d ÷ 100 = %d."
                      % (pct, base, base, pct, ans)])

    def pct_of_money():
        pct = pick([5, 10, 15, 20, 25, 40, 50, 75])
        g = _hcf(pct, 100)
        step = 100 // g
        pounds = step * random.randint(2, _by_d(d, 8, 15, 30))
        pence = pounds * 100
        ans_p = pence * pct // 100
        return _numq("Work out %d%% of %s. Give your answer in pounds."
                     % (pct, _pounds(pounds)), ans_p // 100,
                     ["%d%% of %s = %s." % (pct, _pounds(pounds),
                                            _pounds(ans_p // 100))], unit="£")

    def find_10_percent():
        base = random.randint(3, 40) * 10
        return _numq("Find 10%% of %d." % base, base // 10,
                     ["10%% is found by dividing by 10: %d ÷ 10 = %d."
                      % (base, base // 10)])

    def word_discount_amount():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        step = 100 // g
        price = step * random.randint(2, 15)
        saving = price * pct // 100
        return _numq("A coat costs %s. In a sale there is %d%% off. How much money "
                     "is taken off the price, in pounds?"
                     % (_pounds(price), pct), saving,
                     ["%d%% of %s = %s off." % (pct, _pounds(price),
                                                _pounds(saving))], unit="£")

    def pct_of_group():
        pct = pick([10, 20, 25, 50, 40])
        g = _hcf(pct, 100)
        step = 100 // g
        total = step * random.randint(2, 12)
        ans = total * pct // 100
        one, two = pick(_PEOPLE)
        return _numq("A school has %d %s. %d%% of them are also %s. How many are "
                     "%s?" % (total, one, pct, two, two), ans,
                     ["%d%% of %d = %d." % (pct, total, ans)], unit=two)

    def bar_pct():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        step = 100 // g
        vals = [step * random.randint(2, 9) for _ in range(4)]
        cats = ["Mon", "Tue", "Wed", "Thu"]
        i = random.randrange(4)
        ans = vals[i] * pct // 100
        return _barq("The chart shows how many tickets were sold each day. On %s, "
                     "%d%% of the tickets sold were child tickets. How many child "
                     "tickets were sold on %s?" % (cats[i], pct, cats[i]),
                     cats, vals, ans,
                     ["%s: %d tickets, and %d%% of %d = %d."
                      % (cats[i], vals[i], pct, vals[i], ans)])

    def pie_pct():
        # pie chart of a total; find pct of a sector count
        who = "students"
        parts = [random.randint(2, 6) for _ in range(3)]
        cats = ["Football", "Netball", "Hockey"]
        total = sum(parts) * 10
        counts = [p * 10 for p in parts]
        i = random.randrange(3)
        pct = pick([10, 20, 50])
        g = _hcf(pct, 100)
        # ensure counts[i] divisible
        counts[i] = (100 // g) * random.randint(1, 4)
        ans = counts[i] * pct // 100
        slices = list(zip(cats, counts))
        return _pieq("The pie chart shows the favourite sport of some %s. %d %s "
                     "chose %s. %d%% of those %s also play for a team. How many "
                     "is that?"
                     % (who, counts[i], who, cats[i], pct, who),
                     slices, ans,
                     "int",
                     ["%d%% of %d = %d." % (pct, counts[i], ans)],
                     highlight=i)

    def non_multiple_of_ten():
        pct = pick([15, 30, 35, 45, 5, 12])
        g = _hcf(pct, 100)
        step = 100 // g
        base = step * random.randint(2, _by_d(d, 8, 15, 25))
        ans = base * pct // 100
        return _numq("Work out %d%% of %d." % (pct, base), ans,
                     ["10%% of %d = %d, and 5%% = %d." % (base, base // 10,
                                                          base // 20)
                      if base % 20 == 0 else
                      "%d%% of %d = %d ÷ 100 × %d." % (pct, base, base, pct),
                      "%d%% of %d = %d." % (pct, base, ans)])

    def grid_model():
        # solve a percent problem using a 100-square grid model
        pct = pick([10, 20, 25, 40, 50, 5, 30, 60, 75, 80])
        g = _hcf(pct, 100)
        step = 100 // g
        base = step * random.randint(2, _by_d(d, 8, 15, 25))
        ans = base * pct // 100
        return {"prompt": "This grid model is a 100-square grid with %d squares "
                          "shaded to represent %d%%. Use the grid model to solve "
                          "this percent problem: what is %d%% of %d?"
                          % (pct, pct, pct, base),
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": 100, "shaded": pct},
                "answer": ans, "answer_type": "int", "tolerance": 0,
                "solution": ["Each shaded square is 1%% of %d." % base,
                             "%d shaded squares means %d%% of %d = %d."
                             % (pct, pct, base, ans)]}

    def pct_of_money_amount():
        # percents of numbers and money amounts
        pct = pick([5, 10, 15, 20, 25, 40, 50, 75])
        g = _hcf(pct, 100)
        step = 100 // g
        pounds = step * random.randint(2, _by_d(d, 8, 15, 30))
        ans = pounds * pct // 100
        return _numq("Percents of numbers and money amounts: work out %d%% of "
                     "the money amount %s. Give your answer in pounds."
                     % (pct, _pounds(pounds)), ans,
                     ["%d%% of %s = %s ÷ 100 × %d = %s."
                      % (pct, _pounds(pounds), _pounds(pounds), pct,
                         _pounds(ans))], unit="£")

    def pct_word_number():
        # percents of numbers: word problem
        pct = pick([10, 20, 25, 50, 40, 5, 15, 75])
        g = _hcf(pct, 100)
        step = 100 // g
        n = step * random.randint(2, _by_d(d, 10, 20, 40))
        noun, desc = pick([("books", "are non-fiction"),
                           ("seats", "have been booked"),
                           ("apples", "are ripe"),
                           ("tickets", "have been sold"),
                           ("pupils", "walk to school"),
                           ("houses", "have a garden")])
        ans = n * pct // 100
        return _numq("Percent word problem: there are %d %s and %d%% of the %s "
                     "%s. How many %s %s?"
                     % (n, noun, pct, noun, desc, noun, desc), ans,
                     ["%d%% of %d = %d." % (pct, n, ans)], unit=noun)

    opts = [pct_of_number, pct_of_money, find_10_percent, word_discount_amount,
            pct_of_group, bar_pct, non_multiple_of_ten, grid_model,
            pct_of_money_amount, pct_word_number]
    if d == 0:
        opts = [pct_of_number, find_10_percent, word_discount_amount,
                pct_of_group, bar_pct, pct_of_money, grid_model,
                pct_of_money_amount, pct_word_number]
    elif d == 2:
        opts = [pct_of_number, pct_of_money, non_multiple_of_ten,
                word_discount_amount, pct_of_group, bar_pct, pie_pct,
                grid_model, pct_of_money_amount, pct_word_number]
    opts = opts + [bar_pct, pct_of_money, grid_model]
    return pick(opts)()


# ================================================================= 8.5.c =====
@skill("Y8.5.c", "One number as a percentage of another", S5)
def _(d=1):
    d = _t(d)

    def basic():
        pct = pick([10, 20, 25, 40, 50, 5, 75, 80])
        g = _hcf(pct, 100)
        whole = (100 // g) * random.randint(2, _by_d(d, 6, 12, 25))
        part = whole * pct // 100
        return _numq("What percentage is %d out of %d?" % (part, whole), pct,
                     ["%d ÷ %d = %s." % (part, whole, _dstr(Decimal(part) /
                                                            Decimal(whole))),
                      "× 100 = %d%%." % pct], unit="%")

    def test_score():
        pct = pick([50, 60, 70, 80, 40, 25, 75, 90])
        g = _hcf(pct, 100)
        total = (100 // g) * random.randint(1, 5)
        score = total * pct // 100
        return _numq("%s scored %d out of %d in a test. What percentage is that?"
                     % (pick(NAMES), score, total), pct,
                     ["%d ÷ %d × 100 = %d%%." % (score, total, pct)], unit="%")

    def attendance():
        pct = pick([80, 90, 75, 60, 50, 95])
        g = _hcf(pct, 100)
        total = (100 // g) * random.randint(1, 4)
        present = total * pct // 100
        return _numq("Out of %d days, a pupil attended %d. What percentage of the "
                     "days did the pupil attend?" % (total, present), pct,
                     ["%d ÷ %d × 100 = %d%%." % (present, total, pct)], unit="%")

    def money_pct():
        pct = pick([10, 20, 25, 50, 40])
        g = _hcf(pct, 100)
        whole = (100 // g) * random.randint(2, 10)
        part = whole * pct // 100
        return _numq("%s saves %s out of pocket money of %s each week. What "
                     "percentage of the pocket money is saved?"
                     % (pick(NAMES), _pounds(part), _pounds(whole)), pct,
                     ["%d ÷ %d × 100 = %d%%." % (part, whole, pct)], unit="%")

    def table_pct():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        whole = (100 // g) * random.randint(2, 8)
        part = whole * pct // 100
        rows = [["Total", str(whole)], ["Faulty", str(part)]]
        return _dtq("A factory checks %d items and finds %d faulty. What "
                    "percentage of the items are faulty?" % (whole, part),
                    ["Category", "Number"], rows, pct,
                    ["%d ÷ %d × 100 = %d%%." % (part, whole, pct)],
                    caption="Quality check", answer_type="int")

    def part_of_larger():
        pct = pick([5, 10, 15, 20, 25])
        g = _hcf(pct, 100)
        whole = (100 // g) * random.randint(3, 12)
        part = whole * pct // 100
        return _numq("In a car park there are %d spaces and %d are empty. What "
                     "percentage of the spaces are empty?" % (whole, part), pct,
                     ["%d ÷ %d × 100 = %d%%." % (part, whole, pct)], unit="%")

    def what_pct_left():
        pct = pick([20, 25, 40, 50, 60])
        g = _hcf(pct, 100)
        whole = (100 // g) * random.randint(2, 8)
        used = whole * pct // 100
        left_pct = 100 - pct
        return _numq("A tank holds %d litres. %d litres have been used. What "
                     "percentage of the tank is LEFT?" % (whole, used), left_pct,
                     ["Used: %d ÷ %d × 100 = %d%%." % (used, whole, pct),
                      "Left: 100 − %d = %d%%." % (pct, left_pct)], unit="%")

    opts = [basic, test_score, attendance, money_pct, table_pct, part_of_larger]
    if d == 0:
        opts = [basic, test_score, attendance, part_of_larger, table_pct]
    elif d == 2:
        opts = [basic, test_score, money_pct, table_pct, part_of_larger,
                what_pct_left, attendance]
    opts = opts + [table_pct, table_pct]
    return pick(opts)()


# ================================================================= 8.5.d =====
@skill("Y8.5.d", "Percentage increase or decrease", S5)
def _(d=1):
    d = _t(d)

    def increase():
        pct = pick([10, 20, 25, 50, 5, 30])
        g = _hcf(pct, 100)
        base = (100 // g) * random.randint(2, _by_d(d, 8, 15, 30))
        ans = base + base * pct // 100
        return _numq("Increase %d by %d%%." % (base, pct), ans,
                     ["%d%% of %d = %d." % (pct, base, base * pct // 100),
                      "%d + %d = %d." % (base, base * pct // 100, ans)])

    def decrease():
        pct = pick([10, 20, 25, 50, 40, 5])
        g = _hcf(pct, 100)
        base = (100 // g) * random.randint(2, _by_d(d, 8, 15, 30))
        ans = base - base * pct // 100
        return _numq("Decrease %d by %d%%." % (base, pct), ans,
                     ["%d%% of %d = %d." % (pct, base, base * pct // 100),
                      "%d − %d = %d." % (base, base * pct // 100, ans)])

    def pay_rise():
        pct = pick([5, 10, 20, 25])
        g = _hcf(pct, 100)
        pay = (100 // g) * random.randint(10, 40)
        ans = pay + pay * pct // 100
        return _numq("%s earns %s a week. %s gets a %d%% pay rise. What is the new "
                     "weekly pay, in pounds?"
                     % (pick(NAMES), _pounds(pay), "That worker", pct), ans,
                     ["Rise = %d%% of %s = %s." % (pct, _pounds(pay),
                                                   _pounds(pay * pct // 100)),
                      "New pay = %s." % _pounds(ans)], unit="£")

    def population():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        start = (100 // g) * random.randint(20, 80)
        ans = start + start * pct // 100
        return _numq("A town has a population of %d. It grows by %d%%. What is the "
                     "new population?" % (start, pct), ans,
                     ["Increase = %d." % (start * pct // 100),
                      "%d + %d = %d." % (start, start * pct // 100, ans)])

    def sale_price():
        pct = pick([10, 20, 25, 50, 30])
        g = _hcf(pct, 100)
        price = (100 // g) * random.randint(2, 15)
        ans = price - price * pct // 100
        return _numq("A jacket costs %s. In a sale it is reduced by %d%%. What is "
                     "the sale price, in pounds?" % (_pounds(price), pct), ans,
                     ["Reduction = %s." % _pounds(price * pct // 100),
                      "%s − %s = %s." % (_pounds(price),
                                         _pounds(price * pct // 100),
                                         _pounds(ans))], unit="£")

    def find_new_pct():
        pct = pick([10, 20, 25, 50])
        base = 100
        ans = base + base * pct // 100
        return _numq("A price is increased by %d%%. If the original price counts "
                     "as 100%%, what percentage is the new price?" % pct,
                     100 + pct,
                     ["New price = 100%% + %d%% = %d%%." % (pct, 100 + pct)],
                     unit="%")

    def table_change():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        rows_in = sorted(random.sample(range(2, 12), 3))
        base_unit = 100 // g
        vals = [base_unit * x for x in rows_in]
        i = random.randrange(3)
        rows = [[str(v), "" if j == i else str(v + v * pct // 100)]
                for j, v in enumerate(vals)]
        ans = vals[i] + vals[i] * pct // 100
        return _dtq("Each value in the left column is increased by %d%% to give "
                    "the right column. What is the missing value?" % pct,
                    ["Before", "After +%d%%" % pct], rows, ans,
                    ["%d%% of %d = %d, so %d + %d = %d."
                     % (pct, vals[i], vals[i] * pct // 100, vals[i],
                        vals[i] * pct // 100, ans)],
                    missing=(i, 1), caption="Increase by %d%%" % pct)

    opts = [increase, decrease, pay_rise, sale_price, population, table_change]
    if d == 0:
        opts = [increase, decrease, sale_price, pay_rise, table_change]
    elif d == 2:
        opts = [increase, decrease, pay_rise, population, sale_price,
                find_new_pct, table_change]
    opts = opts + [table_change, table_change]
    return pick(opts)()


# ================================================================= 8.5.e =====
@skill("Y8.5.e", "Reverse percentages", S5)
def _(d=1):
    d = _t(d)

    def after_increase():
        pct = pick([10, 20, 25, 50])
        orig = pick([20, 40, 50, 80, 60, 100, 120, 200]) if d == 0 else \
            random.randint(2, 25) * 10
        new = orig + orig * pct // 100
        return _numq("After a %d%% increase, a price is %s. What was the original "
                     "price, in pounds?" % (pct, _pounds(new)), orig,
                     ["The new price is %d%% of the original."
                      % (100 + pct),
                      "Original = %s ÷ %d × 100 = %s."
                      % (_pounds(new), 100 + pct, _pounds(orig))], unit="£")

    def after_decrease():
        pct = pick([10, 20, 25, 50])
        orig = random.randint(2, 25) * 10
        new = orig - orig * pct // 100
        return _numq("After a %d%% decrease, a price is %s. What was the original "
                     "price, in pounds?" % (pct, _pounds(new)), orig,
                     ["The sale price is %d%% of the original." % (100 - pct),
                      "Original = %s ÷ %d × 100 = %s."
                      % (_pounds(new), 100 - pct, _pounds(orig))], unit="£")

    def sale_reverse():
        pct = pick([10, 20, 25, 50])
        orig = random.randint(3, 20) * 10
        new = orig - orig * pct // 100
        return _numq("A coat is reduced by %d%% in a sale and now costs %s. What "
                     "was the original price, in pounds?" % (pct, _pounds(new)),
                     orig,
                     ["%s is %d%% of the original." % (_pounds(new), 100 - pct),
                      "Original = %s ÷ %d × 100 = %s."
                      % (_pounds(new), 100 - pct, _pounds(orig))], unit="£")

    def find_original_amount():
        pct = pick([10, 20, 25, 50])
        orig = random.randint(2, 20) * 10
        part = orig * pct // 100
        return _numq("%d%% of a number is %d. What is the number?" % (pct, part),
                     orig,
                     ["%d%% is %d, so 1%% is %d ÷ %d = %s."
                      % (pct, part, part, pct, _dstr(Decimal(part) / pct)),
                      "100%% = %d." % orig])

    def wage_reverse():
        pct = pick([10, 20, 25])
        orig = random.randint(20, 60) * 10
        new = orig + orig * pct // 100
        return _numq("After a %d%% pay rise, a weekly wage is %s. What was the "
                     "wage before the rise, in pounds?" % (pct, _pounds(new)),
                     orig,
                     ["New wage is %d%% of the old wage." % (100 + pct),
                      "Old wage = %s ÷ %d × 100 = %s."
                      % (_pounds(new), 100 + pct, _pounds(orig))], unit="£")

    def vat_reverse():
        # price includes 20% VAT; find pre-VAT price
        pre = random.randint(2, 40) * 10
        inc = pre + pre * 20 // 100
        return _numq("A price of %s includes 20%% VAT. What was the price before "
                     "VAT was added, in pounds?" % _pounds(inc), pre,
                     ["The price with VAT is 120%% of the pre-VAT price.",
                      "%s ÷ 120 × 100 = %s." % (_pounds(inc), _pounds(pre))],
                     unit="£")

    def reverse_table():
        pct = pick([10, 20, 25, 50])
        origs = sorted(set(random.randint(2, 25) * 10 for _ in range(4)))
        while len(origs) < 4:
            origs = sorted(set(origs + [random.randint(2, 25) * 10]))
        origs = origs[:4]
        i = random.randrange(4)
        rows = [["" if j == i else str(o), str(o - o * pct // 100)]
                for j, o in enumerate(origs)]
        return _dtq("Every original price on the left was reduced by %d%% to give "
                    "the sale price on the right. What is the missing ORIGINAL "
                    "price, in pounds?" % pct,
                    ["Original", "Sale (−%d%%)" % pct], rows, origs[i],
                    ["The sale price is %d%% of the original."
                     % (100 - pct),
                     "Original = %s ÷ %d × 100 = %s."
                     % (_pounds(origs[i] - origs[i] * pct // 100), 100 - pct,
                        _pounds(origs[i]))],
                    missing=(i, 0), caption="Reverse a %d%% reduction" % pct)

    def change_find_original():
        # percent of change: find the original amount (word problem)
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        step = 100 // g
        orig = step * random.randint(2, 25)
        item = pick(["bike", "phone", "sofa", "table", "camera", "coat"])
        if random.random() < 0.5:
            new = orig + orig * pct // 100
            return _numq(
                "Percent of change word problem: after a %d%% increase, the "
                "price of a %s is %s. Find the original amount (the price "
                "before the change), in pounds."
                % (pct, item, _pounds(new)), orig,
                ["The new price is %d%% of the original amount." % (100 + pct),
                 "Original amount = %s ÷ %d × 100 = %s."
                 % (_pounds(new), 100 + pct, _pounds(orig))], unit="£")
        new = orig - orig * pct // 100
        return _numq(
            "Percent of change word problem: after a %d%% decrease, the price "
            "of a %s is %s. Find the original amount before the change, in "
            "pounds." % (pct, item, _pounds(new)), orig,
            ["The new price is %d%% of the original amount." % (100 - pct),
             "Original amount = %s ÷ %d × 100 = %s."
             % (_pounds(new), 100 - pct, _pounds(orig))], unit="£")

    opts = [after_increase, after_decrease, sale_reverse, find_original_amount,
            wage_reverse, reverse_table, change_find_original]
    if d == 0:
        opts = [after_increase, after_decrease, find_original_amount,
                sale_reverse, reverse_table, change_find_original]
    elif d == 2:
        opts = [after_increase, after_decrease, sale_reverse, wage_reverse,
                vat_reverse, find_original_amount, reverse_table,
                change_find_original]
    opts = opts + [reverse_table]
    return pick(opts)()


# ================================================================= 8.5.f =====
@skill("Y8.5.f", "Percentage equations and comparisons", S5)
def _(d=1):
    d = _t(d)

    def what_pct_change():
        base = random.randint(2, 20) * 10
        pct = pick([10, 20, 25, 50])
        rise = base * pct // 100
        newv = base + rise
        return _numq("A price rises from %s to %s. What is the percentage "
                     "increase?" % (_pounds(base), _pounds(newv)), pct,
                     ["Increase = %s." % _pounds(rise),
                      "%d ÷ %d × 100 = %d%%." % (rise, base, pct)], unit="%")

    def pct_decrease_change():
        base = random.randint(2, 20) * 10
        pct = pick([10, 20, 25, 50, 40])
        fall = base * pct // 100
        newv = base - fall
        return _numq("A price falls from %s to %s. What is the percentage "
                     "decrease?" % (_pounds(base), _pounds(newv)), pct,
                     ["Decrease = %s." % _pounds(fall),
                      "%d ÷ %d × 100 = %d%%." % (fall, base, pct)], unit="%")

    def compare_two():
        # which is bigger: p1% of A vs p2% of B
        p1 = pick([10, 20, 25, 50])
        p2 = pick([10, 20, 25, 50])
        g1 = _hcf(p1, 100)
        g2 = _hcf(p2, 100)
        a = (100 // g1) * random.randint(2, 10)
        b = (100 // g2) * random.randint(2, 10)
        v1 = a * p1 // 100
        v2 = b * p2 // 100
        while v1 == v2:
            b = (100 // g2) * random.randint(2, 10)
            v2 = b * p2 // 100
        ans = "A" if v1 > v2 else "B"
        return _wordq("Which is larger:  A) %d%% of %d   or   B) %d%% of %d ? "
                      "Type A or B." % (p1, a, p2, b), ans,
                      ["A: %d%% of %d = %d." % (p1, a, v1),
                       "B: %d%% of %d = %d." % (p2, b, v2),
                       "%s is larger." % ans], placeholder="A or B")

    def solve_pct_equation():
        pct = pick([10, 20, 25, 50, 40])
        g = _hcf(pct, 100)
        x = (100 // g) * random.randint(2, 12)
        val = x * pct // 100
        return _numq("%d%% of a number is %d. What is the number?" % (pct, val),
                     x,
                     ["1%% of the number is %d ÷ %d = %s."
                      % (val, pct, _dstr(Decimal(val) / pct)),
                      "100%% = %d." % x])

    def two_shops():
        base = random.randint(2, 20) * 10
        shopA_off = pick([10, 20, 25])
        shopB_off = pick([10, 20, 25])
        while shopB_off == shopA_off:
            shopB_off = pick([10, 20, 25])
        priceA = base - base * shopA_off // 100
        priceB = base - base * shopB_off // 100
        cheaper = "A" if priceA < priceB else "B"
        return _wordq("The same TV costs %s in both shops before discounts. Shop A "
                      "takes %d%% off; Shop B takes %d%% off. Which shop is "
                      "cheaper? Type A or B."
                      % (_pounds(base), shopA_off, shopB_off), cheaper,
                      ["Shop A: %s." % _pounds(priceA),
                       "Shop B: %s." % _pounds(priceB),
                       "Shop %s is cheaper." % cheaper], placeholder="A or B")

    def pct_more_than():
        a = random.randint(2, 12) * 10
        pct = pick([10, 20, 25, 50])
        b = a + a * pct // 100
        return _numq("B is %d and A is %d. B is what percentage MORE than A?"
                     % (b, a), pct,
                     ["Difference = %d − %d = %d." % (b, a, b - a),
                      "%d ÷ %d × 100 = %d%%." % (b - a, a, pct)], unit="%")

    def bar_compare():
        cats = ["2022", "2023"]
        base = random.randint(2, 12) * 10
        pct = pick([10, 20, 25, 50])
        newv = base + base * pct // 100
        return _barq("The bar chart shows a shop's sales (in £1000s) in two "
                     "years. By what percentage did sales increase from 2022 to "
                     "2023?", cats, [base, newv], pct,
                     ["Increase = %d − %d = %d." % (newv, base, newv - base),
                      "%d ÷ %d × 100 = %d%%." % (newv - base, base, pct)])

    opts = [what_pct_change, pct_decrease_change, compare_two,
            solve_pct_equation, two_shops, bar_compare]
    if d == 0:
        opts = [what_pct_change, pct_decrease_change, solve_pct_equation,
                compare_two, bar_compare]
    elif d == 2:
        opts = [what_pct_change, pct_decrease_change, compare_two,
                solve_pct_equation, two_shops, pct_more_than, bar_compare]
    opts = opts + [bar_compare]
    return pick(opts)()


# ================================================================= 8.5.g =====
@skill("Y8.5.g", "VAT, discount, mark-up and sale prices", S5)
def _(d=1):
    d = _t(d)

    def add_vat():
        pre = random.randint(2, _by_d(d, 15, 30, 60)) * 10
        inc = pre + pre * 20 // 100
        return _numq("A laptop costs %s before VAT. VAT is charged at 20%%. What "
                     "is the total price including VAT, in pounds?"
                     % _pounds(pre), inc,
                     ["VAT = 20%% of %s = %s." % (_pounds(pre),
                                                  _pounds(pre * 20 // 100)),
                      "%s + %s = %s." % (_pounds(pre), _pounds(pre * 20 // 100),
                                         _pounds(inc))], unit="£")

    def apply_discount():
        pct = pick([10, 15, 20, 25, 30, 50])
        g = _hcf(pct, 100)
        price = (100 // g) * random.randint(2, 15)
        ans = price - price * pct // 100
        return _numq("A pair of trainers costs %s. There is a %d%% discount. What "
                     "is the discounted price, in pounds?"
                     % (_pounds(price), pct), ans,
                     ["Discount = %s." % _pounds(price * pct // 100),
                      "%s − %s = %s." % (_pounds(price),
                                         _pounds(price * pct // 100),
                                         _pounds(ans))], unit="£")

    def mark_up():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        cost = (100 // g) * random.randint(2, 12)
        ans = cost + cost * pct // 100
        return _numq("A shop buys a bag for %s and marks it up by %d%% to set the "
                     "selling price. What is the selling price, in pounds?"
                     % (_pounds(cost), pct), ans,
                     ["Mark-up = %s." % _pounds(cost * pct // 100),
                      "%s + %s = %s." % (_pounds(cost),
                                         _pounds(cost * pct // 100),
                                         _pounds(ans))], unit="£")

    def discount_saving():
        pct = pick([10, 20, 25, 30, 50])
        g = _hcf(pct, 100)
        price = (100 // g) * random.randint(2, 15)
        saving = price * pct // 100
        return _numq("A game priced at %s has %d%% off. How much money do you "
                     "SAVE, in pounds?" % (_pounds(price), pct), saving,
                     ["%d%% of %s = %s saved." % (pct, _pounds(price),
                                                  _pounds(saving))], unit="£")

    def vat_amount_only():
        pre = random.randint(2, 30) * 10
        vat = pre * 20 // 100
        return _numq("VAT is charged at 20%%. How much VAT is added to a bill of "
                     "%s (before VAT), in pounds?" % _pounds(pre), vat,
                     ["20%% of %s = %s." % (_pounds(pre), _pounds(vat))],
                     unit="£")

    def two_step_sale():
        pct = pick([10, 20, 25])
        g = _hcf(pct, 100)
        price = (100 // g) * random.randint(4, 15)
        sale = price - price * pct // 100
        # then add nothing; ask sale price with a further comparison
        return _numq("A shop reduces a %s coat by %d%%, then charges 0%% extra. "
                     "What is the final price, in pounds?"
                     % (_pounds(price), pct), sale,
                     ["Reduced by %d%%: %s − %s = %s."
                      % (pct, _pounds(price), _pounds(price * pct // 100),
                         _pounds(sale))], unit="£")

    def table_prices():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        base = 100 // g
        prices = sorted(set(base * random.randint(2, 12) for _ in range(4)))
        while len(prices) < 4:
            prices.append(base * random.randint(2, 12))
            prices = sorted(set(prices))
        prices = prices[:4]
        i = random.randrange(4)
        rows = [[_pounds(p), "" if j == i else _pounds(p - p * pct // 100)]
                for j, p in enumerate(prices)]
        ans = prices[i] - prices[i] * pct // 100
        return _dtq("Every item in this list has %d%% off. What is the missing "
                    "sale price, in pounds?" % pct,
                    ["Full price", "Sale price"], rows, ans,
                    ["%d%% of %s = %s, so %s − %s = %s."
                     % (pct, _pounds(prices[i]),
                        _pounds(prices[i] * pct // 100), _pounds(prices[i]),
                        _pounds(prices[i] * pct // 100), _pounds(ans))],
                    missing=(i, 1), caption="Sale: %d%% off" % pct)

    def money_four_ops():
        # add, subtract, multiply and divide money amounts: word problem
        A = random.randint(2, 9)
        q = random.randint(2, 6)
        B = random.randint(2, 8)
        total = q * A + B
        k = pick([2, 3, 4, 5])
        change = k * random.randint(1, 6)
        pay = total + change
        ans = change // k
        return _numq(
            "Money word problem (add, subtract, multiply and divide): a group "
            "orders %d boxes at %s each and adds a %s delivery charge. They pay "
            "with %s and share the change equally between %d friends. How much "
            "change does each friend get, in pounds?"
            % (q, _pounds(A), _pounds(B), _pounds(pay), k), ans,
            ["Multiply: %d × %s = %s." % (q, _pounds(A), _pounds(q * A)),
             "Add delivery: %s + %s = %s."
             % (_pounds(q * A), _pounds(B), _pounds(total)),
             "Subtract for change: %s − %s = %s."
             % (_pounds(pay), _pounds(total), _pounds(change)),
             "Divide: %s ÷ %d = %s each."
             % (_pounds(change), k, _pounds(ans))], unit="£")

    def money_add_subtract():
        # money amounts word problem, integer pence throughout
        a = random.randint(120, 480)
        b = random.randint(80, 350)
        q = random.randint(2, 4)
        spent = a + b * q
        pay_pounds = spent // 100 + random.randint(1, 4)
        pay = pay_pounds * 100
        change = pay - spent
        return _numq(
            "Money word problem: one item costs %s and each of %d other items "
            "costs %s. The money amounts are added, then paid for with %s. How "
            "much change is given? Give your answer in pence."
            % (money(a), q, money(b), _pounds(pay_pounds)), change,
            ["Total cost: %s + %d × %s = %dp." % (money(a), q, money(b), spent),
             "Change: %dp − %dp = %dp." % (pay, spent, change)], unit="p")

    opts = [add_vat, apply_discount, mark_up, discount_saving, vat_amount_only,
            table_prices, money_four_ops, money_add_subtract]
    if d == 0:
        opts = [apply_discount, discount_saving, vat_amount_only, add_vat,
                table_prices, money_four_ops, money_add_subtract]
    elif d == 2:
        opts = [add_vat, apply_discount, mark_up, discount_saving,
                two_step_sale, table_prices, money_four_ops, money_add_subtract]
    opts = opts + [table_prices]
    return pick(opts)()


# ================================================================= 8.5.h =====
@skill("Y8.5.h", "Unit pricing and best buys", S5)
def _(d=1):
    d = _t(d)
    sing, plur = pick(_ITEMS)

    def unit_price():
        n = random.randint(3, 10)
        each = random.randint(8, 60)
        return _numq("A pack of %d %s costs %s. What is the price of one %s, in "
                     "pence?" % (n, plur, money(n * each), sing), each,
                     ["%d ÷ %d = %dp each." % (n * each, n, each)], unit="p")

    def best_buy_letter():
        n1, n2 = random.randint(4, 12), random.randint(4, 12)
        while n2 == n1:
            n2 = random.randint(4, 12)
        cheap = random.randint(10, 30)
        dear = cheap + random.randint(2, 12)
        return _wordq("Pack A: %d %s for %s. Pack B: %d %s for %s. Which pack is "
                      "the best buy (lowest price per %s)? Type A or B."
                      % (n1, plur, money(n1 * cheap), n2, plur,
                         money(n2 * dear), sing), "A",
                      ["A: %d ÷ %d = %dp each." % (n1 * cheap, n1, cheap),
                       "B: %d ÷ %d = %dp each." % (n2 * dear, n2, dear),
                       "Pack A is the best buy."], placeholder="A or B")

    def best_buy_table():
        rows = []
        cheap = random.randint(10, 30)
        packs = ["A", "B", "C"]
        counts = random.sample(range(3, 12), 3)
        unit_prices = [cheap, cheap + random.randint(2, 8),
                       cheap + random.randint(3, 10)]
        best_i = 0
        for i in range(3):
            rows.append([packs[i], str(counts[i]),
                         money(counts[i] * unit_prices[i])])
        return _dtq("The table shows three packs of %s. Which pack is the best "
                    "value per %s? Type the pack letter." % (plur, sing),
                    ["Pack", "Number", "Price"], rows, "A",
                    ["Work out price ÷ number for each pack.",
                     "Pack A is %dp each, the lowest." % cheap],
                    caption="Which is the best buy?", answer_type="str")

    def cost_per_100g():
        grams = pick([250, 500, 200, 400])
        per100 = random.randint(15, 60)
        price = grams // 100 * per100
        return _numq("A %d g tub of yoghurt costs %s. What is the cost per 100 g, "
                     "in pence?" % (grams, money(price)), per100,
                     ["%d g is %d lots of 100 g." % (grams, grams // 100),
                      "%d ÷ %d = %dp per 100 g." % (price, grams // 100,
                                                    per100)], unit="p")

    def how_much_cheaper():
        n = random.randint(4, 10)
        a_each = random.randint(15, 40)
        b_each = a_each + random.randint(2, 10)
        diff = (b_each - a_each) * n
        return _numq("Pack A holds %d %s at %dp each; Pack B holds the same %d %s "
                     "at %dp each. How much MORE does Pack B cost in total, in "
                     "pence?" % (n, plur, a_each, n, plur, b_each), diff,
                     ["A: %dp. B: %dp." % (n * a_each, n * b_each),
                      "%d − %d = %dp." % (n * b_each, n * a_each, diff)],
                     unit="p")

    def price_list_missing():
        each = random.randint(8, 40)
        counts = sorted(random.sample(range(2, 14), 4))
        i = random.randrange(4)
        rows = [[str(c), "" if j == i else money(c * each)]
                for j, c in enumerate(counts)]
        return _dtq("This price list charges the same for every %s. What is the "
                    "missing price, in pence?" % sing,
                    ["Number of %s" % plur, "Price"], rows, counts[i] * each,
                    ["One %s costs %dp, so %d cost %dp."
                     % (sing, each, counts[i], counts[i] * each)],
                    missing=(i, 1), caption="Price list")

    opts = [unit_price, best_buy_letter, best_buy_table, cost_per_100g,
            price_list_missing]
    if d == 0:
        opts = [unit_price, best_buy_letter, cost_per_100g, price_list_missing]
    elif d == 2:
        opts = [best_buy_letter, best_buy_table, cost_per_100g,
                how_much_cheaper, price_list_missing, unit_price]
    opts = opts + [best_buy_table, price_list_missing]
    return pick(opts)()


# ================================================================= 8.5.i =====
@skill("Y8.5.i", "Simple interest and repeated percentage change", S5)
def _(d=1):
    d = _t(d)

    def simple_interest():
        rate = pick([2, 5, 10, 4, 3])
        years = random.randint(2, 6)
        g = _hcf(rate, 100)
        principal = (100 // g) * random.randint(5, 30)
        interest = principal * rate * years // 100
        return _numq("%s is invested at %d%% simple interest per year. How much "
                     "interest is earned after %d years, in pounds?"
                     % (_pounds(principal), rate, years), interest,
                     ["One year's interest = %d%% of %s = %s."
                      % (rate, _pounds(principal),
                         _pounds(principal * rate // 100)),
                      "%d years: %s × %d = %s."
                      % (years, _pounds(principal * rate // 100), years,
                         _pounds(interest))], unit="£")

    def simple_interest_total():
        rate = pick([2, 5, 10, 4])
        years = random.randint(2, 5)
        g = _hcf(rate, 100)
        principal = (100 // g) * random.randint(5, 25)
        interest = principal * rate * years // 100
        total = principal + interest
        return _numq("%s is put in an account paying %d%% simple interest per "
                     "year. What is the total in the account after %d years, in "
                     "pounds?" % (_pounds(principal), rate, years), total,
                     ["Interest = %s × %d = %s."
                      % (_pounds(principal * rate // 100), years,
                         _pounds(interest)),
                      "Total = %s + %s = %s." % (_pounds(principal),
                                                 _pounds(interest),
                                                 _pounds(total))], unit="£")

    def compound_two_years():
        rate = pick([10, 20, 50])  # keep 2-year compound an exact integer
        principal = random.randint(2, 20) * 100  # pounds
        # compute in pounds; with these rates and multiple of 100 stays integer
        p = principal
        for _ in range(2):
            p = p + p * rate // 100
        return _numq("%s is invested at %d%% compound interest per year. What is "
                     "it worth after 2 years, in pounds? (Interest is added each "
                     "year, then earns interest the next year.)"
                     % (_pounds(principal), rate), p,
                     ["After year 1: %s + %d%% = %s."
                      % (_pounds(principal), rate,
                         _pounds(principal + principal * rate // 100)),
                      "After year 2: apply %d%% again to get %s."
                      % (rate, _pounds(p))], unit="£")

    def repeated_decrease():
        rate = pick([10, 20, 50])
        start = random.randint(2, 10) * 100
        p = start
        for _ in range(2):
            p = p - p * rate // 100
        return _numq("A car worth %s loses %d%% of its value each year. What is it "
                     "worth after 2 years, in pounds?" % (_pounds(start), rate),
                     p,
                     ["After year 1: %s − %d%% = %s."
                      % (_pounds(start), rate,
                         _pounds(start - start * rate // 100)),
                      "After year 2: apply %d%% loss again to get %s."
                      % (rate, _pounds(p))], unit="£")

    def increase_then_decrease():
        rate = pick([10, 20, 50])
        start = random.randint(2, 10) * 100
        after1 = start + start * rate // 100
        after2 = after1 - after1 * rate // 100
        return _numq("A price of %s is increased by %d%%, then the new price is "
                     "decreased by %d%%. What is the final price, in pounds?"
                     % (_pounds(start), rate, rate), after2,
                     ["After the increase: %s." % _pounds(after1),
                      "After the decrease: %s − %d%% = %s."
                      % (_pounds(after1), rate, _pounds(after2))], unit="£")

    def interest_table():
        rate = pick([5, 10, 20])
        g = _hcf(rate, 100)
        principal = (100 // g) * random.randint(5, 20)
        rows = []
        for yr in range(1, 4):
            rows.append([str(yr), _pounds(principal * rate * yr // 100)])
        i = random.randrange(3)
        ans = principal * rate * (i + 1) // 100
        rows[i][1] = ""
        return _dtq("%s is invested at %d%% simple interest. The table shows the "
                    "total interest earned. What is the missing amount, in "
                    "pounds?" % (_pounds(principal), rate),
                    ["Years", "Interest"], rows, ans,
                    ["One year = %s, so %d years = %s."
                     % (_pounds(principal * rate // 100), i + 1,
                        _pounds(ans))],
                    missing=(i, 1), caption="Simple interest at %d%%" % rate)

    opts = [simple_interest, simple_interest_total, compound_two_years,
            interest_table]
    if d == 0:
        opts = [simple_interest, simple_interest_total, interest_table]
    elif d == 2:
        opts = [simple_interest, simple_interest_total, compound_two_years,
                repeated_decrease, increase_then_decrease, interest_table]
    opts = opts + [interest_table]
    return pick(opts)()


# ================================================================= 8.5.j =====
@skill("Y8.5.j", "Multi-step percentage problems and Venn diagrams", S5)
def _(d=1):
    d = _t(d)

    def two_step_pct():
        pct1 = pick([10, 20, 25, 50])
        pct2 = pick([10, 20, 25, 50])
        g = _hcf(pct1, 100) * _hcf(pct2, 100)
        base = 100 * random.randint(2, 8)
        after1 = base * pct1 // 100
        ans = after1 * pct2 // 100
        return _numq("A club has %d members. %d%% are juniors. Of the juniors, "
                     "%d%% play in a team. How many juniors play in a team?"
                     % (base, pct1, pct2), ans,
                     ["Juniors = %d%% of %d = %d." % (pct1, base, after1),
                      "Team = %d%% of %d = %d." % (pct2, after1, ans)])

    def deposit_remaining():
        pct = pick([10, 20, 25, 50])
        g = _hcf(pct, 100)
        total = (100 // g) * random.randint(4, 20)
        deposit = total * pct // 100
        remaining = total - deposit
        return _numq("A holiday costs %s. A deposit of %d%% is paid. How much is "
                     "still left to pay, in pounds?" % (_pounds(total), pct),
                     remaining,
                     ["Deposit = %d%% of %s = %s."
                      % (pct, _pounds(total), _pounds(deposit)),
                      "Left to pay = %s − %s = %s."
                      % (_pounds(total), _pounds(deposit),
                         _pounds(remaining))], unit="£")

    def venn_both():
        # two-set Venn: total, % like A, % like B, and overlap count given
        total = random.randint(2, 6) * 10
        pctA = pick([40, 50, 60])
        pctB = pick([30, 50, 40])
        gA = _hcf(pctA, 100)
        gB = _hcf(pctB, 100)
        total = (100 // gA) * (100 // gB) * random.randint(1, 3)
        while total > 120:
            total = (100 // gA) * (100 // gB)
        onlyA = total * pctA // 100
        onlyB = total * pctB // 100
        both = random.randint(1, min(onlyA, onlyB) // 2 or 1)
        # count in exactly one of the two = (A + B) - 2*both ... but here pctA counts total who like A
        likeA = onlyA
        likeB = onlyB
        neither = total - (likeA + likeB - both)
        if neither < 0:
            return two_step_pct()
        return _numq("In a survey of %d people, %d%% like tea and %d%% like "
                     "coffee. %d people like BOTH tea and coffee. How many like "
                     "NEITHER drink? (Use a Venn diagram: total = only-tea + "
                     "only-coffee + both + neither.)"
                     % (total, pctA, pctB, both), neither,
                     ["Like tea = %d, like coffee = %d." % (likeA, likeB),
                      "Like at least one = %d + %d − %d = %d."
                      % (likeA, likeB, both, likeA + likeB - both),
                      "Neither = %d − %d = %d."
                      % (total, likeA + likeB - both, neither)])

    def venn_only_one():
        total = 100
        both = random.randint(5, 20)
        likeA = random.randint(both + 5, 60)
        likeB = random.randint(both + 5, 60)
        onlyA = likeA - both
        return _numq("In a class survey of 100 pupils, %d pupils own a bike and "
                     "%d own skates. %d pupils own BOTH. How many own a bike but "
                     "NOT skates?" % (likeA, likeB, both), onlyA,
                     ["Own a bike = %d, and %d of them also own skates."
                      % (likeA, both),
                      "Bike only = %d − %d = %d." % (likeA, both, onlyA)])

    def pct_of_remainder():
        base = 100 * random.randint(2, 6)
        pct1 = pick([20, 25, 50, 40])
        spent = base * pct1 // 100
        left = base - spent
        pct2 = pick([10, 20, 25, 50])
        second = left * pct2 // 100
        return _numq("%s has %s. %s spends %d%% on a coat, then %d%% of what is "
                     "LEFT on shoes. How much is spent on shoes, in pounds?"
                     % (pick(NAMES), _pounds(base), "That person", pct1, pct2),
                     second,
                     ["Coat = %d%% of %s = %s, leaving %s."
                      % (pct1, _pounds(base), _pounds(spent), _pounds(left)),
                      "Shoes = %d%% of %s = %s."
                      % (pct2, _pounds(left), _pounds(second))], unit="£")

    def profit_pct():
        cost = random.randint(2, 20) * 10
        pct = pick([10, 20, 25, 50])
        profit = cost * pct // 100
        sell = cost + profit
        return _numq("A trader buys an item for %s and sells it for %s. What is "
                     "the percentage profit?" % (_pounds(cost), _pounds(sell)),
                     pct,
                     ["Profit = %s − %s = %s." % (_pounds(sell), _pounds(cost),
                                                  _pounds(profit)),
                      "%d ÷ %d × 100 = %d%%." % (profit, cost, pct)], unit="%")

    def venn_table():
        # two-way table: rows Bike/No bike, cols Skates/No skates; find a pct
        both = random.randint(5, 15)
        bike_only = random.randint(5, 20)
        skate_only = random.randint(5, 20)
        neither = 100 - (both + bike_only + skate_only)
        if neither < 0:
            return venn_only_one()
        rows = [["Owns skates", str(both), str(skate_only)],
                ["No skates", str(bike_only), str(neither)]]
        # ask what percentage own a bike (both + bike_only) out of 100
        bike_total = both + bike_only
        return _dtq("This two-way table shows 100 pupils sorted by whether they "
                    "own a bike and whether they own skates. What percentage of "
                    "the pupils own a bike?",
                    ["", "Owns bike", "No bike"], rows, bike_total,
                    ["Own a bike = %d + %d = %d out of 100."
                     % (both, bike_only, bike_total),
                     "That is %d%%." % bike_total],
                    caption="Bikes and skates (100 pupils)", answer_type="int")

    opts = [two_step_pct, deposit_remaining, venn_both, venn_only_one,
            pct_of_remainder, profit_pct, venn_table]
    if d == 0:
        opts = [two_step_pct, deposit_remaining, venn_only_one, profit_pct,
                venn_table]
    elif d == 2:
        opts = [two_step_pct, venn_both, venn_only_one, pct_of_remainder,
                profit_pct, deposit_remaining, venn_table]
    opts = opts + [venn_table]
    return pick(opts)()
