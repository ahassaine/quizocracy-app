# dev/app/logic/y8_gen_e.py — Year 8 generators: strands 8.8 (geometry,
# transformations & Pythagoras) and 8.9 (mensuration, statistics & probability).
#
# Every generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between 8+ genuinely different framings (visual model, bare
# calculation, word problem, missing value, inverse, comparison, reasoning,
# multi-step). Answers are computed from the generated parameters, never hard-coded,
# and every geometry fact used is internally consistent.
#
# Visual components: angle / circle / shape / net / coordinate_grid / pie_chart /
#                    data_table / bar_chart / line_graph / pictogram / scatter_plot
import math
import random
from fractions import Fraction
from .maths_engine import skill, pick, money, NAMES, ordinal


def _half_up(x, places=0):
    """Round half UP on the exact value, as taught in English schools: 19.625 -> 19.63.
    Python's round() rounds halves to even and works on the binary float."""
    from decimal import Decimal, ROUND_HALF_UP
    if isinstance(x, Fraction):
        d = Decimal(x.numerator) / Decimal(x.denominator)
    else:
        d = Decimal(str(x))
    return float(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))

S8 = "8.8 Geometry, transformations & Pythagoras"
S9 = "8.9 Mensuration, statistics & probability"


# ---------------------------------------------------------------- helpers ----
def _tier(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_tier(d)]


def _pick_t(weights):
    total = float(sum(weights))
    r = random.random() * total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r < acc:
            return i
    return len(weights) - 1


def _f(x):
    """Tidy a number for printing: 3.0 -> '3', 2.500 -> '2.5'."""
    if isinstance(x, int):
        return str(x)
    s = ("%.6f" % float(x)).rstrip("0").rstrip(".")
    return s if s not in ("", "-") else "0"


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _plp(n, plural):
    """_pl for a word given in the plural: (1, 'vertices') -> '1 vertex'."""
    one = {"vertices": "vertex", "faces": "face", "edges": "edge"}.get(plural, plural[:-1])
    return "%d %s" % (n, one if n == 1 else plural)


def _an(n):
    """'a 6' / 'an 8' / 'an 11' / 'an 18' — the article as the number is read aloud."""
    s = str(int(n))
    return ("an " if s[0] == "8" or s in ("11", "18") or (len(s) in (5, 6) and s[:2] in ("11", "18")) else "a ") + s


def _a(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def _num_q(prompt, answer, answer_type="int", unit=None, text=False,
           placeholder=None, solution=None, tolerance=0):
    spec = {}
    if unit:
        spec["unit"] = unit
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution or []}


def _coord(x, y):
    return "(%d,%d)" % (int(x), int(y))


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _bear(n):
    """Three-figure bearing string, e.g. 72 -> '072'."""
    return "%03d" % (int(n) % 360)


def _data_list(prompt, vals, answer, header="Value", solution=None, atype="int"):
    """A data_table stimulus showing a single column of values, with a typed answer."""
    return {"prompt": prompt, "component": "data_table",
            "spec": {"caption": "Data", "headers": [header],
                     "rows": [[str(v)] for v in vals]},
            "answer": answer, "answer_type": atype, "tolerance": 0,
            "solution": solution or []}


def _measure_table(prompt, caption, headers, row, answer, solution=None,
                   atype="int", tol=0):
    """A data_table stimulus showing one row of named measurements, typed answer."""
    return {"prompt": prompt, "component": "data_table",
            "spec": {"caption": caption, "headers": headers,
                     "rows": [[str(x) for x in row]]},
            "answer": answer, "answer_type": atype, "tolerance": tol,
            "solution": solution or []}


# Pythagorean triples (a <= b < c) used so answers are exact integers.
_TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17),
            (12, 16, 20), (7, 24, 25), (10, 24, 26), (20, 21, 29), (9, 40, 41),
            (12, 35, 37), (15, 20, 25), (18, 24, 30), (16, 30, 34)]


# ================================================================== 8.8 ======
@skill("Y8.8.a", "Measure, draw and classify angles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 2, 1, 1, 1])

    if t == 0:                                        # measure with a protractor
        deg = random.choice(_by_d(d,
                                  [30, 40, 50, 60, 70, 110, 120, 130],
                                  [25, 35, 45, 65, 85, 100, 115, 135, 145, 155],
                                  [15, 35, 55, 75, 95, 105, 125, 145, 165, 175]))
        return {"prompt": "Use the protractor to measure this angle. "
                          "How many degrees is it?",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": deg, "answer_type": "int", "tolerance": 2,
                "solution": ["Line the centre of the protractor up with the point of the "
                             "angle and read the scale that starts at 0.",
                             "The angle measures %d°." % deg]}

    if t == 1:                                        # classify a drawn angle
        kind = pick(_by_d(d, ["acute", "right", "obtuse"],
                          ["acute", "right", "obtuse", "reflex"],
                          ["acute", "right", "obtuse", "straight", "reflex"]))
        deg = {"acute": lambda: random.choice([15, 25, 35, 45, 55, 70, 80]),
               "right": lambda: 90,
               "obtuse": lambda: random.choice([100, 110, 125, 140, 155, 170]),
               "straight": lambda: 180,
               "reflex": lambda: random.choice([200, 230, 260, 290, 320, 350])}[kind]()
        return {"prompt": "Look at the angle. Is it acute, right, obtuse, straight or "
                          "reflex? (type one word)",
                "component": "angle", "spec": {"mode": "classify", "degrees": deg},
                "answer": kind, "answer_type": "str",
                "solution": ["Acute is under 90°, right is 90°, obtuse is between 90° and "
                             "180°, straight is 180° and reflex is over 180°.",
                             "This angle is %d°, so it is %s." % (deg, kind)]}

    if t == 2:                                        # angles on a straight line
        a = random.randint(_by_d(d, 30, 25, 20), _by_d(d, 80, 110, 140))
        rest = 180 - a
        return _num_q("Two angles sit on a straight line and together make a half turn. "
                      "One of them is %d°. How many degrees is the other, in degrees?" % a,
                      rest, "int", unit="degrees",
                      solution=["Angles on a straight line add up to 180°.",
                                "180 − %d = %d°." % (a, rest)])

    if t == 3:                                        # angles on a line, three parts
        parts = _by_d(d, 2, 3, 3)
        given = [random.randint(20, 60) for _ in range(parts)]
        while sum(given) >= 175:
            given = [random.randint(20, 50) for _ in range(parts)]
        miss = 180 - sum(given)
        return _num_q("Angles of %s all lie on the same straight line, along with one "
                      "more angle. How many degrees is the missing angle?"
                      % ", ".join("%d°" % g for g in given),
                      miss, "int", unit="degrees",
                      solution=["The angles on a straight line add up to 180°.",
                                "180 − (%s) = %d°."
                                % (" + ".join(str(g) for g in given), miss)])

    if t == 4:                                        # angles around a point
        parts = _by_d(d, 3, 3, 4)
        given = [random.randint(40, 100) for _ in range(parts)]
        while sum(given) >= 350:
            given = [random.randint(40, 80) for _ in range(parts)]
        miss = 360 - sum(given)
        return _num_q("Angles of %s meet at a point, along with one more angle that "
                      "completes the full turn. How many degrees is the missing angle?"
                      % ", ".join("%d°" % g for g in given),
                      miss, "int", unit="degrees",
                      solution=["Angles around a point add up to 360°.",
                                "360 − (%s) = %d°."
                                % (" + ".join(str(g) for g in given), miss)])

    if t == 5:                                        # classify from a number
        deg = random.choice(_by_d(d, [20, 45, 70, 90, 110, 150],
                                  [30, 60, 89, 90, 120, 150, 179, 180, 250, 300],
                                  [1, 44, 89, 90, 91, 179, 180, 200, 300, 359]))
        if deg < 90:
            kind = "acute"
        elif deg == 90:
            kind = "right"
        elif deg < 180:
            kind = "obtuse"
        elif deg == 180:
            kind = "straight"
        else:
            kind = "reflex"
        return _num_q("An angle measures %d°. Is it acute, right, obtuse, straight or "
                      "reflex? (type one word)" % deg, kind, "str", text=True,
                      placeholder="acute / right / obtuse / straight / reflex",
                      solution=["Acute < 90°, right = 90°, obtuse 90°–180°, straight = "
                                "180°, reflex > 180°.",
                                "%d° is %s." % (deg, kind)])

    if t == 6:                                        # right angle split in two
        a = random.randint(_by_d(d, 20, 15, 10), _by_d(d, 70, 75, 80))
        return _num_q("Two angles meet to form a right angle. One of them is %d°. "
                      "How many degrees is the other?" % a,
                      90 - a, "int", unit="degrees",
                      solution=["A right angle is 90°.",
                                "90 − %d = %d°." % (a, 90 - a)])

    if t == 7:                                        # measure then classify (visual)
        deg = random.choice([35, 55, 75, 100, 125, 150, 165])
        return {"prompt": "Measure this angle with the protractor and write its size in "
                          "degrees.",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": deg, "answer_type": "int", "tolerance": 2,
                "solution": ["Read the scale where the second arm crosses it.",
                             "The angle is %d°, which is %s."
                             % (deg, "acute" if deg < 90 else "obtuse")]}

    if t == 8:                                        # equal angles on a line
        k = _by_d(d, 2, 3, 4)
        each = 180 // k
        while 180 % k:
            k = pick([2, 3, 4, 5, 6])
            each = 180 // k
        return _num_q("%d equal angles sit side by side on a straight line. "
                      "How many degrees is each one?" % k, each, "int", unit="degrees",
                      solution=["The angles on a straight line total 180°.",
                                "180 ÷ %d = %d°." % (k, each)])

    # reflex partner of a drawn angle
    deg = random.choice([40, 55, 70, 110, 130, 150])
    return {"prompt": "The angle shown is measured going one way round the point. "
                      "Going the OTHER way round is the reflex angle. "
                      "How many degrees is the reflex angle?",
            "component": "angle", "spec": {"mode": "classify", "degrees": deg},
            "answer": 360 - deg, "answer_type": "int",
            "solution": ["A full turn is 360°.",
                         "360 − %d = %d°." % (deg, 360 - deg)]}


@skill("Y8.8.b", "Angle relationships", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 3])

    if t == 10:                                       # identify the named relationship
        desc, ans = pick([
            ("add up to 90°, together making a right angle", "complementary"),
            ("add up to 180°, together making a straight line", "supplementary"),
            ("are the equal angles opposite each other where two straight lines "
             "cross", "vertically opposite"),
            ("sit next to each other, sharing a vertex and one arm", "adjacent"),
            ("are exactly equal in size (the same number of degrees)", "congruent"),
        ])
        return _num_q("Two angles %s. Identify this relationship: are they "
                      "complementary, supplementary, vertically opposite, adjacent or "
                      "congruent? (type the name)" % desc, ans, "str", text=True,
                      placeholder="complementary / supplementary / vertically opposite / "
                                  "adjacent / congruent",
                      solution=["Complementary add to 90°, supplementary to 180°, "
                                "vertically opposite angles are equal, adjacent angles "
                                "are side by side, congruent angles are equal.",
                                "These angles are %s." % ans])

    if t == 0:                                        # complementary (visual)
        a = random.randint(_by_d(d, 20, 15, 5), _by_d(d, 70, 80, 85))
        return {"prompt": "The angle shown is %d°. Its COMPLEMENT is the angle that makes "
                          "a right angle (90°) with it. How many degrees is the "
                          "complement?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": 90 - a, "answer_type": "int",
                "solution": ["Complementary angles add up to 90°.",
                             "90 − %d = %d°." % (a, 90 - a)]}

    if t == 1:                                        # supplementary (visual)
        a = random.randint(_by_d(d, 40, 25, 10), _by_d(d, 100, 140, 160))
        return {"prompt": "The angle shown is %d°. Its SUPPLEMENT is the angle that makes "
                          "a straight line (180°) with it. How many degrees is the "
                          "supplement?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": 180 - a, "answer_type": "int",
                "solution": ["Supplementary angles add up to 180°.",
                             "180 − %d = %d°." % (a, 180 - a)]}

    if t == 2:                                        # vertically opposite (visual)
        a = random.randint(_by_d(d, 30, 20, 15), _by_d(d, 80, 130, 165))
        return {"prompt": "When two straight lines cross, the angle shown of %d° is "
                          "formed. How many degrees is the angle VERTICALLY OPPOSITE to "
                          "it?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": a, "answer_type": "int",
                "solution": ["Vertically opposite angles are equal.",
                             "The opposite angle is also %d°." % a]}

    if t == 3:                                        # adjacent on a line
        a = random.randint(_by_d(d, 30, 25, 20), _by_d(d, 80, 120, 150))
        return _num_q("Two angles are adjacent and lie on a straight line. One measures "
                      "%d°. How many degrees is the angle next to it?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["Adjacent angles on a straight line add up to 180°.",
                                "180 − %d = %d°." % (a, 180 - a)])

    if t == 4:                                        # name the relationship (typed)
        a = random.choice([20, 30, 40, 50, 60, 70, 80])
        pair, ans = pick([
            (90, "complementary"), (180, "supplementary"),
        ])
        b = pair - a
        return _num_q("Angles of %d° and %d° are placed together. Because they add up "
                      "to %d°, what is the name for this pair? (type one word)"
                      % (a, b, pair),
                      ans, "str", text=True, placeholder="complementary / supplementary",
                      solution=["%d + %d = %d°." % (a, b, pair),
                                "Angles adding to %d° are %s." % (pair, ans)])

    if t == 5:                                        # find x on a line, two unknowns
        x = random.randint(_by_d(d, 20, 15, 10), _by_d(d, 60, 70, 80))
        extra = random.randint(10, 40)
        # angles x and (x + extra) on a straight line
        # 2x + extra = 180
        total_extra = extra
        # ensure 2x+extra == 180 by recomputing extra
        extra = 180 - 2 * x
        while extra <= 0:
            x = random.randint(20, 70)
            extra = 180 - 2 * x
        return _num_q("Two angles on a straight line are x° and (x + %d)°. "
                      "What is the value of x?" % extra,
                      x, "int",
                      solution=["The two angles add up to 180°: x + (x + %d) = 180." % extra,
                                "2x + %d = 180, so 2x = %d and x = %d."
                                % (extra, 180 - extra, x)])

    if t == 6:                                        # complementary word problem
        who = pick(NAMES)
        a = random.randint(20, 70)
        return _num_q("%s draws two angles that together make a right angle. "
                      "The first angle is %d°. How many degrees is the second?"
                      % (who, a), 90 - a, "int", unit="degrees",
                      solution=["A right angle is 90°.",
                                "90 − %d = %d°." % (a, 90 - a)])

    if t == 7:                                        # is it complementary or supplementary
        a, b = pick([(35, 55), (40, 50), (110, 70), (130, 50), (25, 65), (140, 40)])
        ans = "complementary" if a + b == 90 else "supplementary"
        return _num_q("Angles of %d° and %d° are a pair. Are they complementary or "
                      "supplementary? (type one word)" % (a, b),
                      ans, "str", text=True, placeholder="complementary / supplementary",
                      solution=["%d + %d = %d°." % (a, b, a + b),
                                "They add to %d°, so they are %s." % (a + b, ans)])

    if t == 8:                                        # around a point with vertical pair
        a = random.randint(30, 70)
        b = random.randint(30, 70)
        # four angles round a point: a, b, a, b -> 2a+2b=360
        c = 180 - a - b
        while c <= 10:
            a, b = random.randint(30, 70), random.randint(20, 60)
            c = 180 - a - b
        return _num_q("Three angles sit side by side on a straight line. Two of them "
                      "are %d° and %d°. How many degrees is the third angle?" % (a, b),
                      c, "int", unit="degrees",
                      solution=["The three angles lie on a straight line and add to 180°.",
                                "180 − %d − %d = %d°." % (a, b, c)])

    # supplementary: find x with a multiple
    x = random.randint(_by_d(d, 20, 15, 10), 55)
    k = pick([2, 3])
    # x and k*x supplementary: x + kx = 180 -> x=180/(k+1)
    x = 180 // (k + 1)
    while (k + 1) * x != 180:
        k = pick([2, 3, 5])
        x = 180 // (k + 1)
    return _num_q("One angle is %d times the size of another, and the two are "
                  "supplementary. What is the size of the SMALLER angle, in degrees?" % k,
                  x, "int", unit="degrees",
                  solution=["Let the smaller angle be x. Then x + %dx = 180°." % k,
                            "%dx = 180, so x = %d°." % (k + 1, x)])


@skill("Y8.8.c", "Angles in parallel lines", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 1])
    a = random.randint(_by_d(d, 40, 30, 20), _by_d(d, 80, 130, 160))

    if t == 0:                                        # alternate angles (visual)
        return {"prompt": "Two parallel lines are crossed by a straight transversal. One "
                          "of the angles made is shown, %d°. How many degrees is the "
                          "ALTERNATE angle (the one in the Z-shape)?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": a, "answer_type": "int",
                "solution": ["Alternate angles are equal.",
                             "The alternate angle is also %d°." % a]}

    if t == 1:                                        # corresponding angles (visual)
        return {"prompt": "Two parallel lines are crossed by a transversal. One of the "
                          "angles made is shown, %d°. How many degrees is the "
                          "CORRESPONDING angle (the one in the F-shape)?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": a, "answer_type": "int",
                "solution": ["Corresponding angles are equal.",
                             "The corresponding angle is also %d°." % a]}

    if t == 2:                                        # co-interior angles (visual)
        return {"prompt": "Two parallel lines are crossed by a transversal. One of the "
                          "angles made is shown, %d°. How many degrees is the CO-INTERIOR "
                          "(allied) angle on the same side?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": 180 - a, "answer_type": "int",
                "solution": ["Co-interior angles add up to 180°.",
                             "180 − %d = %d°." % (a, 180 - a)]}

    if t == 3:                                        # name the type: equal, Z-shape
        shape, ans = pick([("a Z-shape", "alternate"),
                           ("an F-shape", "corresponding"),
                           ("a C-shape (or U-shape)", "co-interior")])
        return _num_q("Two parallel lines are crossed by a transversal. A pair of angles "
                      "sits in %s. What is the name for this pair of angles? (type one "
                      "word)" % shape, ans, "str", text=True,
                      placeholder="alternate / corresponding / co-interior",
                      solution=["Z-shapes give alternate angles, F-shapes give "
                                "corresponding angles and C/U-shapes give co-interior "
                                "angles.",
                                "This pair is %s." % ans])

    if t == 4:                                        # equal or supplementary?
        rel, ans = pick([("alternate", "equal"), ("corresponding", "equal"),
                         ("vertically opposite", "equal"),
                         ("co-interior", "supplementary")])
        return _num_q("In a pair of parallel lines, %s angles are always... "
                      "(type: equal or supplementary)" % rel, ans, "str", text=True,
                      placeholder="equal / supplementary",
                      solution=["Alternate, corresponding and vertically opposite angles "
                                "are equal; co-interior angles are supplementary.",
                                "%s angles are %s." % (rel.capitalize(), ans)])

    if t == 5:                                        # multi-step: alternate then line
        return _num_q("Two parallel lines are crossed by a transversal. One angle is "
                      "%d°. Its alternate angle is formed, and next to that alternate "
                      "angle (on a straight line) is another angle. How many degrees is "
                      "that last angle?" % a, 180 - a, "int", unit="degrees",
                      solution=["The alternate angle equals %d°." % a,
                                "The angle next to it on a straight line is 180 − %d = "
                                "%d°." % (a, 180 - a)])

    if t == 6:                                        # co-interior find x (visual)
        return {"prompt": "The angle shown, %d°, and an angle x° are co-interior angles "
                          "between two parallel lines. What is the value of x?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": 180 - a, "answer_type": "int",
                "solution": ["Co-interior angles add up to 180°.",
                             "x = 180 − %d = %d." % (a, 180 - a)]}

    if t == 7:                                        # true / false reasoning
        claim, tf = pick([
            ("Alternate angles between parallel lines are equal", "true"),
            ("Co-interior angles between parallel lines are equal", "false"),
            ("Corresponding angles between parallel lines are equal", "true"),
            ("Co-interior angles between parallel lines add up to 180°", "true"),
        ])
        return _num_q("True or false: %s. (type true or false)" % claim, tf, "str",
                      text=True, placeholder="true / false",
                      solution=["Alternate and corresponding angles are equal; "
                                "co-interior angles are supplementary (sum 180°).",
                                "The statement is %s." % tf])

    # find x, corresponding then vertically opposite chain
    return _num_q("A transversal crosses two parallel lines. At the top crossing an "
                  "angle of %d° is marked. Using corresponding angles, then vertically "
                  "opposite angles at the bottom crossing, what angle (in degrees) is "
                  "equal to it?" % a, a, "int", unit="degrees",
                  solution=["Corresponding angles are equal (%d°), and vertically "
                            "opposite angles are equal too." % a,
                            "So the marked angle is %d°." % a])


_QUADS8 = [("square", "4 equal sides and 4 right angles"),
           ("rectangle", "4 right angles but sides that are not all equal"),
           ("rhombus", "4 equal sides but no right angles"),
           ("parallelogram", "opposite sides equal and parallel, adjacent sides of "
                             "different lengths and no right angles"),
           ("trapezium", "exactly one pair of parallel sides"),
           ("kite", "two pairs of adjacent equal sides, but not all four sides equal")]
_TRIS8 = [("equilateral", "3 equal sides and 3 equal angles"),
          ("isosceles", "2 equal sides and 2 equal angles"),
          ("scalene", "all sides and all angles different"),
          ("right-angled", "one angle of exactly 90°")]


@skill("Y8.8.d", "Classify triangles and quadrilaterals", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 1, 1, 1, 1, 2, 2])

    if t == 9:                                         # classify a polygon by its sides
        n = pick([5, 6, 7, 8, 9, 10, 12])
        nm = _NGON[n]
        return _num_q("Identify and classify this polygon by its number of sides. "
                      "A polygon has %d sides. What is its name? (type one word)" % n,
                      nm, "str", text=True,
                      placeholder="pentagon / hexagon / heptagon / octagon / nonagon / "
                                  "decagon / dodecagon",
                      solution=["A polygon is named by how many sides it has.",
                                "A %d-sided polygon is %s." % (n, _a(nm))])

    if t == 10:                                        # classify regular / irregular
        reg = random.random() < 0.5
        desc = ("all its sides equal and all its angles equal" if reg
                else "sides and angles that are not all equal")
        ans = "regular" if reg else "irregular"
        return _num_q("Classify this polygon. A polygon has %s. Is it a regular or an "
                      "irregular polygon? (type one word)" % desc, ans, "str", text=True,
                      placeholder="regular / irregular",
                      solution=["A regular polygon has all sides and all angles equal; "
                                "otherwise it is irregular.",
                                "This polygon is %s." % ans])

    if t == 0:                                        # visual: name the polygon
        nm, sd = pick([("triangle", 3), ("pentagon", 5), ("hexagon", 6),
                       ("octagon", 8)] if d else [("triangle", 3), ("pentagon", 5)])
        return {"prompt": "This regular polygon is drawn. What is its name? (type one word)",
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["Count the straight sides: there are %d." % sd,
                             "A polygon with %d sides is %s." % (sd, _a(nm))]}

    if t == 1:                                        # visual: count sides/vertices
        nm, sd = pick([("triangle", 3), ("square", 4), ("pentagon", 5),
                       ("hexagon", 6), ("octagon", 8)])
        ask = pick(["sides", "vertices"])
        return {"prompt": "How many %s does this shape have?"
                          % ("sides" if ask == "sides" else "vertices (corners)"),
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": ask},
                "answer": sd, "answer_type": "int",
                "solution": ["A polygon has as many vertices as sides.",
                             "This one has %d." % sd]}

    if t == 2:                                        # classify triangle by sides
        nm, desc = pick(_TRIS8)
        return _num_q("A triangle has %s. What type of triangle is it? (type one word; "
                      "use 'right-angled' if needed)" % desc, nm, "str", text=True,
                      placeholder="equilateral / isosceles / scalene / right-angled",
                      solution=["Triangles are named by their equal sides and angles.",
                                "This is %s triangle." % _a(nm)])

    if t == 3:                                        # classify quadrilateral by props
        nm, desc = pick(_QUADS8)
        return _num_q("A quadrilateral has %s. What is its name? (type one word)" % desc,
                      nm, "str", text=True,
                      placeholder="square / rectangle / rhombus / parallelogram / "
                                  "trapezium / kite",
                      solution=["Quadrilaterals are classified by their sides, angles and "
                                "parallel sides.",
                                "This shape is %s." % _a(nm)])

    if t == 4:                                        # triangle by angles
        kind, angs = pick([
            ("acute", (60, 70, 50)), ("right-angled", (90, 55, 35)),
            ("obtuse", (110, 40, 30)), ("acute", (80, 55, 45)),
            ("obtuse", (125, 30, 25)), ("acute", (75, 65, 40)),
        ])
        return _num_q("A triangle has angles of %d°, %d° and %d°. Describe the triangle "
                      "by its angles. (type one word)" % angs, kind, "str", text=True,
                      placeholder="acute / right-angled / obtuse",
                      solution=["Look at the largest angle.",
                                "This triangle is %s." % (kind if kind == "equilateral"
                                                          else kind + (" -angled"
                                                          if kind == "right" else ""))])

    if t == 5:                                        # true property (typed yes/no)
        nm, prop, ans = pick([
            ("square", "all its sides equal", "yes"),
            ("rectangle", "all its sides equal", "no"),
            ("rhombus", "all its sides equal", "yes"),
            ("trapezium", "two pairs of parallel sides", "no"),
            ("parallelogram", "two pairs of parallel sides", "yes"),
            ("kite", "any parallel sides", "no"),
        ])
        return _num_q("Does %s always have %s? (type yes or no)" % (_a(nm), prop),
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["Recall the defining properties of %s." % _a(nm),
                                "The answer is %s." % ans])

    if t == 6:                                        # count parallel side pairs
        nm, pairs = pick([("square", 2), ("rectangle", 2), ("rhombus", 2),
                          ("parallelogram", 2), ("trapezium", 1), ("kite", 0)])
        return _num_q("How many PAIRS of parallel sides does %s have?" % _a(nm),
                      pairs, "int",
                      solution=["A square, rectangle, rhombus and parallelogram have 2 "
                                "pairs; a trapezium has 1; a kite has 0.",
                                "%s has %d." % (_a(nm).capitalize(), pairs)])

    if t == 7:                                        # right angles in a quad
        nm, ra = pick([("square", 4), ("rectangle", 4), ("rhombus", 0),
                       ("parallelogram", 0), ("trapezium", 0), ("kite", 0)])
        return _num_q("How many right angles does %s always have?" % _a(nm), ra, "int",
                      solution=["Only squares and rectangles are guaranteed 4 right "
                                "angles.",
                                "%s has %d." % (_a(nm).capitalize(), ra)])

    # which shape am I (typed)
    nm, desc = pick(_QUADS8)
    return _num_q("I am a quadrilateral with %s. What am I? (type one word)" % desc,
                  nm, "str", text=True,
                  placeholder="square / rectangle / rhombus / parallelogram / "
                              "trapezium / kite",
                  solution=["Match the description to the quadrilateral.",
                            "This is %s." % _a(nm)])


@skill("Y8.8.e", "Missing angles in triangles and quadrilaterals", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 2, 2, 2, 2, 2, 2, 1, 1])

    if t == 0:                                        # third angle of a triangle
        a = random.randint(_by_d(d, 40, 30, 20), _by_d(d, 80, 100, 130))
        b = random.randint(_by_d(d, 40, 30, 20), 170 - a)
        c = 180 - a - b
        return _num_q("Two angles of a triangle are %d° and %d°. How many degrees is "
                      "the third angle?" % (a, b), c, "int", unit="degrees",
                      solution=["The angles of a triangle add up to 180°.",
                                "180 − %d − %d = %d°." % (a, b, c)])

    if t == 1:                                        # isosceles base angles (visual)
        apex = random.randint(_by_d(d, 40, 30, 20), _by_d(d, 100, 120, 140))
        base = (180 - apex) // 2
        while (180 - apex) % 2:
            apex = random.randint(20, 140)
            base = (180 - apex) // 2
        return {"prompt": "An isosceles triangle has the apex angle shown, %d°. The two "
                          "base angles are equal to each other. How many degrees is each "
                          "base angle?" % apex,
                "component": "angle", "spec": {"mode": "classify", "degrees": apex},
                "answer": base, "answer_type": "int",
                "solution": ["The three angles add to 180°.",
                             "(180 − %d) ÷ 2 = %d°." % (apex, base)]}

    if t == 2:                                        # isosceles find apex from base
        base = random.randint(_by_d(d, 40, 30, 25), 75)
        apex = 180 - 2 * base
        return _num_q("An isosceles triangle has two equal base angles of %d° each. "
                      "How many degrees is the apex angle?" % base,
                      apex, "int", unit="degrees",
                      solution=["The three angles add to 180°.",
                                "180 − 2 × %d = %d°." % (base, apex)])

    if t == 3:                                        # fourth angle of a quadrilateral
        a = random.randint(50, 120)
        b = random.randint(50, 120)
        c = random.randint(50, 120)
        while a + b + c >= 350:
            a, b, c = (random.randint(50, 110), random.randint(50, 110),
                       random.randint(50, 110))
        e = 360 - a - b - c
        return _num_q("Three angles of a quadrilateral are %d°, %d° and %d°. "
                      "How many degrees is the fourth angle?" % (a, b, c),
                      e, "int", unit="degrees",
                      solution=["The angles of a quadrilateral add up to 360°.",
                                "360 − %d − %d − %d = %d°." % (a, b, c, e)])

    if t == 4:                                        # exterior angle of a triangle
        a = random.randint(_by_d(d, 40, 35, 30), 80)
        b = random.randint(_by_d(d, 40, 35, 30), 80)
        ext = a + b
        return _num_q("The exterior angle of a triangle equals the sum of the two "
                      "opposite interior angles. Two interior angles are %d° and %d°. "
                      "How many degrees is the exterior angle at the third vertex?"
                      % (a, b), ext, "int", unit="degrees",
                      solution=["Exterior angle = sum of the two remote interior angles.",
                                "%d + %d = %d°." % (a, b, ext)])

    if t == 5:                                        # right-angled triangle other acute (visual)
        a = random.randint(_by_d(d, 25, 20, 10), 80)
        other = 90 - a
        return {"prompt": "A right-angled triangle has a 90° angle and the acute angle "
                          "shown here, %d°. How many degrees is the remaining angle?" % a,
                "component": "angle", "spec": {"mode": "classify", "degrees": a},
                "answer": other, "answer_type": "int",
                "solution": ["The angles add to 180° and one is 90°.",
                             "180 − 90 − %d = %d°." % (a, other)]}

    if t == 6:                                        # interior from exterior (triangle)
        ext = random.randint(100, 160)
        interior = 180 - ext
        return _num_q("An exterior angle of a triangle is %d°. It sits on a straight "
                      "line with the interior angle at that vertex. How many degrees is "
                      "that interior angle?" % ext, interior, "int", unit="degrees",
                      solution=["Interior + exterior = 180° (a straight line).",
                                "180 − %d = %d°." % (ext, interior)])

    if t == 7:                                        # ratio angles of a triangle
        r = pick([(1, 2, 3), (2, 3, 4), (1, 1, 2), (3, 4, 5), (2, 2, 5)])
        unit = 180 // sum(r)
        while 180 % sum(r):
            r = pick([(1, 2, 3), (2, 3, 4), (1, 1, 2), (1, 3, 5)])
            unit = 180 // sum(r)
        which = random.randrange(3)
        ang = r[which] * unit
        return _num_q("The angles of a triangle are in the ratio %s. How many degrees "
                      "is the %s angle in that ratio?"
                      % (":".join(str(x) for x in r), ordinal(which + 1)),
                      ang, "int", unit="degrees",
                      solution=["The ratio has %d parts and 180 ÷ %d = %d° per part."
                                % (sum(r), sum(r), unit),
                                "%d × %d = %d°." % (r[which], unit, ang)])

    # quadrilateral with a right angle marked
    ra = 90
    a = random.randint(70, 110)
    b = random.randint(70, 110)
    while ra + a + b >= 350:
        a, b = random.randint(70, 100), random.randint(70, 100)
    e = 360 - ra - a - b
    return _num_q("A quadrilateral has a right angle and two other angles of %d° and "
                  "%d°. How many degrees is the fourth angle?" % (a, b),
                  e, "int", unit="degrees",
                  solution=["The four angles add to 360° and one is 90°.",
                            "360 − 90 − %d − %d = %d°." % (a, b, e)])


_NGON = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon",
         7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}
_NDIV = [3, 4, 5, 6, 8, 9, 10, 12]      # n dividing 360 (exterior angle is an integer)


@skill("Y8.8.f", "Interior and exterior angles of polygons", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 1])
    n = pick(_by_d(d, [3, 4, 5, 6], [4, 5, 6, 8, 9], [5, 6, 8, 9, 10, 12]))
    nm = _NGON[n]

    if t == 0:                                        # interior angle sum
        s = (n - 2) * 180
        return _num_q("The interior angles of a polygon with n sides add up to "
                      "(n − 2) × 180°. What is the sum of the interior angles of %s "
                      "(%d sides)?" % (_a(nm), n), s, "int", unit="degrees",
                      solution=["(n − 2) × 180 with n = %d." % n,
                                "(%d − 2) × 180 = %d°." % (n, s)])

    if t == 1:                                        # each exterior angle (regular)
        ext = 360 // n
        return _num_q("A REGULAR %s has %d equal exterior angles that add up to 360°. "
                      "How many degrees is each exterior angle?" % (nm, n),
                      ext, "int", unit="degrees",
                      solution=["The exterior angles of any polygon add up to 360°.",
                                "360 ÷ %d = %d°." % (n, ext)])

    if t == 2:                                        # each interior angle (regular)
        s = (n - 2) * 180
        each = s // n
        while s % n:
            n = pick(_NDIV)
            nm = _NGON[n]
            s = (n - 2) * 180
            each = s // n
        return _num_q("A REGULAR %s has %d equal interior angles. "
                      "How many degrees is each interior angle?" % (nm, n),
                      each, "int", unit="degrees",
                      solution=["The interior angles total (%d − 2) × 180 = %d°."
                                % (n, s),
                                "%d ÷ %d = %d°." % (s, n, each)])

    if t == 3:                                        # find n from exterior angle (visual)
        nn = pick(_NDIV)
        ext = 360 // nn
        return {"prompt": "The exterior angle of a regular polygon is shown, %d°. How "
                          "many sides does the polygon have?" % ext,
                "component": "angle", "spec": {"mode": "classify", "degrees": ext},
                "answer": nn, "answer_type": "int",
                "solution": ["Number of sides = 360 ÷ exterior angle.",
                             "360 ÷ %d = %d sides." % (ext, nn)]}

    if t == 4:                                        # interior + exterior = 180 (visual)
        ext = 360 // pick(_NDIV)
        return {"prompt": "The exterior angle of a polygon is shown, %d°. The interior "
                          "and exterior angles at a vertex lie on a straight line. How "
                          "many degrees is the interior angle?" % ext,
                "component": "angle", "spec": {"mode": "classify", "degrees": ext},
                "answer": 180 - ext, "answer_type": "int",
                "solution": ["Interior + exterior = 180°.",
                             "180 − %d = %d°." % (ext, 180 - ext)]}

    if t == 5:                                        # find n from interior angle
        nn = pick([4, 5, 6, 8, 9, 10, 12])
        ext = 360 // nn
        interior = 180 - ext
        return _num_q("Each interior angle of a regular polygon is %d°. How many sides "
                      "does it have?" % interior, nn, "int", unit="sides",
                      solution=["Exterior angle = 180 − %d = %d°." % (interior, ext),
                                "360 ÷ %d = %d sides." % (ext, nn)])

    if t == 6:                                        # missing interior angle (irregular)
        # pentagon with 4 known angles
        nn = pick([4, 5])
        s = (nn - 2) * 180
        known = []
        rem = s
        for _ in range(nn - 1):
            lo = 60
            hi = min(150, rem - 60 * (nn - 1 - len(known)))
            if hi < lo:
                hi = lo
            v = random.randint(lo, hi)
            known.append(v)
            rem -= v
        miss = rem
        if miss < 30 or miss > 200:
            known = [100, 110, 120][:nn - 1] if nn == 4 else [100, 110, 120, 130]
            miss = s - sum(known)
        return _num_q("An irregular %s has interior angles that add up to %d°. "
                      "%s of the angles are %s. How many degrees is the last angle?"
                      % (_NGON[nn], s, "Three" if nn == 4 else "Four",
                         ", ".join("%d°" % k for k in known)),
                      miss, "int", unit="degrees",
                      solution=["The angles add up to %d°." % s,
                                "%d − (%s) = %d°."
                                % (s, " + ".join(str(k) for k in known), miss)])

    if t == 7:                                        # number of triangles / sum reasoning
        s = (n - 2) * 180
        return _num_q("A polygon can be split into (n − 2) triangles from one vertex. "
                      "%s has %d sides. Into how many triangles does it split?"
                      % (_a(nm).capitalize(), n), n - 2, "int", unit="triangles",
                      solution=["n − 2 with n = %d." % n,
                                "%d − 2 = %s (each 180°, total %d°)."
                                % (n, _pl(n - 2, "triangle"), s)])

    # sum of exterior angles (always 360)
    return _num_q("What is the sum of ALL the exterior angles of %s, one at each "
                  "vertex, in degrees?" % _a(nm), 360, "int", unit="degrees",
                  solution=["The exterior angles of ANY polygon add up to 360°.",
                            "The answer is 360°, whatever the number of sides."])


@skill("Y8.8.g", "Parts and properties of a circle", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 1, 1, 1, 1])
    rr = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 7, 10, 15))

    if t == 0:                                        # radius -> diameter (visual)
        return {"prompt": "The circle has a radius of %d cm. What is its diameter, in cm?"
                          % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": 2 * rr, "answer_type": "int",
                "solution": ["The diameter is twice the radius.",
                             "2 × %d = %d cm." % (rr, 2 * rr)]}

    if t == 1:                                        # diameter -> radius (visual)
        dia = 2 * rr
        return {"prompt": "The circle has a diameter of %d cm. What is its radius, in cm?"
                          % dia,
                "component": "circle",
                "spec": {"radius": rr, "show": "diameter", "label": "d = %d cm" % dia},
                "answer": rr, "answer_type": "int",
                "solution": ["The radius is half the diameter.",
                             "%d ÷ 2 = %d cm." % (dia, rr)]}

    if t == 2:                                        # name the marked part (visual)
        part = pick(["radius", "diameter", "circumference"])
        return {"prompt": "What is the name of the part of the circle marked here? "
                          "(type one word)",
                "component": "circle", "spec": {"radius": rr, "show": part},
                "answer": part, "answer_type": "str",
                "solution": [{"radius": "A line from the centre to the edge is the radius.",
                              "diameter": "A line right across through the centre is the "
                                          "diameter.",
                              "circumference": "The distance all the way round the edge is "
                                               "the circumference."}[part]]}

    if t == 3:                                        # part from description (typed)
        desc, ans = pick([
            ("a straight line from the centre to a point on the edge", "radius"),
            ("a straight line right across the circle through the centre", "diameter"),
            ("the whole distance around the outside of the circle", "circumference"),
            ("a straight line joining two points on the edge, not through the centre",
             "chord"),
            ("part of the circumference between two points", "arc"),
            ("a 'slice' of the circle between two radii", "sector"),
            ("the region between a chord and the arc it cuts off", "segment"),
            ("a straight line that just touches the circle at one point", "tangent"),
        ])
        return _num_q("In a circle, what is the name for %s? (type one word)" % desc,
                      ans, "str", text=True,
                      placeholder="radius / diameter / chord / arc / sector / segment / "
                                  "tangent / circumference",
                      solution=["Recall the parts of a circle.",
                                "This is called the %s." % ans])

    if t == 4:                                        # halves and doubles reasoning
        ask = pick(["r_from_d", "d_from_r"])
        if ask == "d_from_r":
            return _num_q("A circle has a radius of %d cm. How long is its diameter, "
                          "in cm?" % rr, 2 * rr, "int", unit="cm",
                          solution=["Diameter = 2 × radius.",
                                    "2 × %d = %d cm." % (rr, 2 * rr)])
        dia = 2 * rr
        return _num_q("A circle has a diameter of %d cm. How long is its radius, in cm?"
                      % dia, rr, "int", unit="cm",
                      solution=["Radius = diameter ÷ 2.", "%d ÷ 2 = %d cm." % (dia, rr)])

    if t == 5:                                        # true/false property
        claim, tf = pick([
            ("The diameter is twice the radius", "true"),
            ("A chord always passes through the centre", "false"),
            ("The diameter is the longest chord of a circle", "true"),
            ("A tangent crosses the circle at two points", "false"),
        ])
        return _num_q("True or false: %s. (type true or false)" % claim, tf, "str",
                      text=True, placeholder="true / false",
                      solution=["Check the definition of each part.",
                                "The statement is %s." % tf])

    if t == 6:                                        # how many radii in a diameter
        return _num_q("How many radii laid end to end make one diameter of a circle?",
                      2, "int",
                      solution=["A diameter is exactly two radii.", "The answer is 2."])

    if t == 7:                                        # semicircle angle / half turn fact
        return _num_q("A diameter splits a circle into two equal halves. Each half is "
                      "called a semicircle. Through how many degrees does the flat "
                      "(straight) edge of a semicircle turn — that is, the angle of a "
                      "straight line?", 180, "int", unit="degrees",
                      solution=["A straight line is 180°.", "The answer is 180°."])

    # part from a description, second set
    desc, ans = pick([
        ("the point that is the exact middle of the circle", "centre"),
        ("the fixed distance from the centre to the edge", "radius"),
        ("a whole circle turned once around its centre, in degrees — type the number",
         "360"),
    ])
    if ans == "360":
        return _num_q("A full turn around the centre of a circle is how many degrees?",
                      360, "int", unit="degrees",
                      solution=["One full turn is 360°.", "The answer is 360°."])
    return _num_q("In a circle, what is %s called? (type one word)" % desc, ans, "str",
                  text=True, placeholder="centre / radius",
                  solution=["Recall the parts of a circle.", "This is the %s." % ans])


_SOLIDS8 = [("cube", 6, 12, 8), ("cuboid", 6, 12, 8),
            ("square-based pyramid", 5, 8, 5), ("triangular prism", 5, 9, 6),
            ("cylinder", 3, 2, 0), ("cone", 2, 1, 1), ("sphere", 1, 0, 0)]
_NETS8 = [("cube", "cube", 6), ("cuboid", "cuboid", 6),
          ("square_pyramid", "square-based pyramid", 5),
          ("triangular_prism", "triangular prism", 5),
          ("cylinder", "cylinder", 3), ("cone", "cone", 2)]


@skill("Y8.8.h", "3-D solids: nets, plans and elevations", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 1, 1, 2, 2])

    if t == 8:                                         # base of a 3-D figure
        solid, base = pick([
            ("a square-based pyramid standing on its base", "square"),
            ("a triangular prism resting on a triangular end", "triangle"),
            ("a cylinder standing on one of its flat ends", "circle"),
            ("a cone standing on its base", "circle"),
            ("a cuboid resting on a face", "rectangle"),
        ])
        return _num_q("Bases of three-dimensional figures: %s. Which 2-D shape is its "
                      "base? (type the name)" % solid, base, "str", text=True,
                      placeholder="square / rectangle / triangle / circle",
                      solution=["The base is the flat 2-D face the solid stands on.",
                                "The base is %s." % _a(base)])

    if t == 9:                                         # net folds into which solid (visual)
        key, nm, faces = pick(_NETS8)
        return {"prompt": "Nets of three-dimensional figures: this net is folded up. "
                          "Which 3-D solid does the net fold into? (type the name)",
                "component": "net", "spec": {"solid": key},
                "answer": nm, "answer_type": "str",
                "solution": ["Fold the net along each edge in your mind.",
                             "This net folds into %s." % _a(nm)]}

    if t == 0:                                        # net -> solid (visual)
        key, nm, faces = pick(_NETS8 if d else _NETS8[:4])
        return {"prompt": "This is the net of a 3-D solid. Which solid does it fold into? "
                          "(type the name)",
                "component": "net", "spec": {"solid": key},
                "answer": nm, "answer_type": "str",
                "solution": ["Imagine folding the net along every line.",
                             "The net folds into %s." % _a(nm)]}

    if t == 1:                                        # net -> count faces (visual)
        key, nm, faces = pick(_NETS8[:4])
        return {"prompt": "This net folds into a 3-D solid. How many flat faces will the "
                          "finished solid have?",
                "component": "net", "spec": {"solid": key},
                "answer": faces, "answer_type": "int",
                "solution": ["Each piece of the net becomes one face.",
                             "%s has %s." % (_a(nm).capitalize(), _pl(faces, "face"))]}

    if t == 2:                                        # name a drawn solid (visual)
        nm = pick(["cube", "cuboid", "triangular prism", "square-based pyramid"])
        return {"prompt": "What is the name of this 3-D solid? (type the name)",
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["Look at the faces and how they meet.",
                             "This solid is %s." % _a(nm)]}

    if t == 3:                                        # plan view
        solid, view, ans = pick([
            ("a cylinder standing on its circular base", "from directly above (plan view)",
             "circle"),
            ("a cylinder standing on its circular base", "from the front", "rectangle"),
            ("a cone standing on its base", "from directly above (plan view)", "circle"),
            ("a cone standing on its base", "from the front", "triangle"),
            ("a square-based pyramid on its base", "from directly above (plan view)",
             "square"),
            ("a square-based pyramid on its base", "from the front", "triangle"),
            ("a cuboid resting on a rectangular face", "from directly above (plan view)",
             "rectangle"),
            ("a triangular prism resting on a rectangular face with its triangular ends "
             "at the front", "from the front", "triangle"),
        ])
        return _num_q("A 3-D solid is viewed from different directions. Looking at %s "
                      "%s, what 2-D shape is seen? (type the name)" % (solid, view),
                      ans, "str", text=True,
                      placeholder="square / rectangle / triangle / circle",
                      solution=["Picture only the outline seen from that direction.",
                                "The view is %s." % _a(ans)])

    if t == 4:                                        # count faces/edges/vertices
        nm, f, e, v = pick(_SOLIDS8[:4])
        prop, val = pick([("faces", f), ("edges", e), ("vertices", v)])
        return _num_q("How many %s does %s have?" % (prop, _a(nm)), val, "int",
                      solution=["Count the %s of %s carefully." % (prop, _a(nm)),
                                "%s has %s." % (_a(nm).capitalize(), _plp(val, prop))])

    if t == 5:                                        # name solid from a description
        nm, desc = pick([
            ("cube", "6 square faces, 12 edges and 8 vertices"),
            ("cylinder", "2 flat circular faces and 1 curved surface"),
            ("triangular prism", "2 triangular faces and 3 rectangular faces"),
            ("square-based pyramid", "1 square face and 4 triangular faces meeting at a "
             "point"),
            ("cone", "1 circular face and 1 curved surface meeting at a point"),
            ("sphere", "one curved surface and no edges or vertices"),
        ])
        return _num_q("Which solid has %s? (type the name)" % desc, nm, "str", text=True,
                      placeholder="e.g. cube / cylinder / cone / sphere",
                      solution=["Match the faces, edges and vertices.",
                                "The solid is %s." % _a(nm)])

    if t == 6:                                        # Euler F + V - E = 2
        nm, f, e, v = pick([("cube", 6, 12, 8), ("cuboid", 6, 12, 8),
                            ("triangular prism", 5, 9, 6),
                            ("square-based pyramid", 5, 8, 5)])
        ask = pick(["faces", "edges", "vertices"])
        if ask == "faces":
            q, ans = ("It has %d edges and %d vertices. Using Euler's rule "
                      "F + V − E = 2, how many faces does it have?" % (e, v), f)
        elif ask == "edges":
            q, ans = ("It has %d faces and %d vertices. Using Euler's rule "
                      "F + V − E = 2, how many edges does it have?" % (f, v), e)
        else:
            q, ans = ("It has %d faces and %d edges. Using Euler's rule "
                      "F + V − E = 2, how many vertices does it have?" % (f, e), v)
        return _num_q("A convex solid follows Euler's rule F + V − E = 2. %s" % q,
                      ans, "int",
                      solution=["Rearrange F + V − E = 2.",
                                "%s has %s." % (_a(nm).capitalize(), _plp(ans, ask))])

    # net -> name, second framing (visual)
    key, nm, faces = pick(_NETS8)
    return {"prompt": "A flat net is shown. When it is folded up, which 3-D solid is "
                      "made? (type the name)",
            "component": "net", "spec": {"solid": key},
            "answer": nm, "answer_type": "str",
            "solution": ["Fold every flap in your mind.",
                         "The net makes %s." % _a(nm)]}


@skill("Y8.8.i", "Reflect, rotate and translate; describe a transformation", S8)
def _(d=1):
    d = _tier(d)
    r = _by_d(d, 5, 6, 8)
    grid = {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r, "ymax": r}
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2])

    def _pt(lo=1, hi=None):
        hi = hi if hi is not None else r - 1
        x = random.randint(1, hi) * pick([-1, 1])
        y = random.randint(1, hi) * pick([-1, 1])
        return x, y

    if t == 9:                                         # reflection: graph the image
        x, y = _pt()
        axis = pick(["x-axis", "y-axis"])
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Reflection: graph the image of point P %s after a reflection "
                          "in the %s. Plot the image point." % (_coord(x, y), axis),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["A reflection in the %s changes the sign of the %s-coordinate."
                             % (axis, "y" if axis == "x-axis" else "x"),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 10:                                        # translation: graph the image
        x, y = _pt(hi=r - 3)
        a = random.randint(-2, 2) or 2
        b = random.randint(-2, 2) or -2
        ix, iy = x + a, y + b
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Translation: graph the image of point P %s after a "
                          "translation by the vector (%d, %d). Plot the image point."
                          % (_coord(x, y), a, b),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["A translation slides the point: (%d + %d, %d + %d)."
                             % (x, a, y, b),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 11:                                        # rotation 270 about origin (plot)
        x, y = _pt()
        cw = random.random() < 0.5
        ix, iy = (-y, x) if cw else (y, -x)
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Rotation: graph the image of point P %s after a rotation of "
                          "270° %s about the origin (0,0). Plot the image point."
                          % (_coord(x, y),
                             "clockwise" if cw else "anticlockwise"),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["A 270° %s rotation about the origin sends (x, y) to %s."
                             % ("clockwise" if cw else "anticlockwise",
                                "(−y, x)" if cw else "(y, −x)"),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 12:                                        # symmetry (lines / rotational order)
        shape, lines, order = pick([
            ("square", 4, 4), ("rectangle", 2, 2), ("equilateral triangle", 3, 3),
            ("isosceles triangle", 1, 1), ("rhombus", 2, 2),
            ("regular pentagon", 5, 5), ("regular hexagon", 6, 6),
        ])
        if random.random() < 0.5:
            return _num_q("Symmetry: how many lines of symmetry does %s have?" % _a(shape),
                          lines, "int", unit="lines",
                          solution=["A line of symmetry splits the shape into two "
                                    "matching halves.",
                                    "%s has %d line%s of symmetry."
                                    % (_a(shape).capitalize(), lines, "" if lines == 1 else "s")])
        return _num_q("Symmetry: what is the order of rotational symmetry of %s?"
                      % _a(shape), order, "int",
                      solution=["The order of rotational symmetry is how many times the "
                                "shape looks the same in one full turn.",
                                "%s has rotational symmetry of order %d."
                                % (_a(shape).capitalize(), order)])

    if t == 0:                                        # reflect in an axis (plot image)
        x, y = _pt()
        axis = pick(["x-axis", "y-axis"])
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Reflect the point P %s in the %s. Plot the image."
                          % (_coord(x, y), axis),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["Reflecting in the %s %s the sign of the %s-coordinate."
                             % (axis, "changes" if axis == "x-axis" else "changes",
                                "y" if axis == "x-axis" else "x"),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 1:                                        # translate by a vector (plot image)
        x, y = _pt(hi=r - 3)
        a = random.randint(-2, 2) or 2
        b = random.randint(-2, 2) or -2
        ix, iy = x + a, y + b
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Translate the point P %s by the vector (%d, %d) — that is, "
                          "%d in the x-direction and %d in the y-direction. Plot the "
                          "image." % (_coord(x, y), a, b, a, b),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["Add the vector to the coordinates: (%d + %d, %d + %d)."
                             % (x, a, y, b),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 2:                                        # rotate 180 about origin
        x, y = _pt()
        ix, iy = -x, -y
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Rotate the point P %s through 180° about the origin (0,0). "
                          "Plot the image." % _coord(x, y),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["A 180° rotation about the origin sends (x, y) to (−x, −y).",
                             "The image is %s." % _coord(ix, iy)]}

    if t == 3:                                        # rotate 90 about origin
        x, y = _pt()
        cw = random.random() < 0.5
        ix, iy = (y, -x) if cw else (-y, x)
        spec = dict(grid); spec["points"] = [[x, y, "P"]]
        return {"prompt": "Rotate the point P %s through 90° %s about the origin (0,0). "
                          "Plot the image."
                          % (_coord(x, y), "clockwise" if cw else "anticlockwise"),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["A 90° %s rotation about the origin sends (x, y) to %s."
                             % ("clockwise" if cw else "anticlockwise",
                                "(y, −x)" if cw else "(−y, x)"),
                             "The image is %s." % _coord(ix, iy)]}

    if t == 4:                                        # find the translation vector (typed coord)
        x, y = _pt(hi=r - 3)
        a = random.randint(-3, 3) or 3
        b = random.randint(-3, 3) or -3
        ix, iy = x + a, y + b
        spec = dict(grid); spec["points"] = [[x, y, "A"], [ix, iy, "B"]]
        return {"prompt": "Point A %s is translated to point B %s. Write the translation "
                          "vector in the form (x,y)." % (_coord(x, y), _coord(ix, iy)),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(a, b), "answer_type": "coord",
                "solution": ["Subtract A from B: (%d − %d, %d − %d)."
                             % (ix, x, iy, y),
                             "The vector is %s." % _coord(a, b)]}

    if t == 5:                                        # name the transformation type (typed)
        kind, clue = pick([
            ("reflection", "the shape is flipped to a mirror image across a line"),
            ("rotation", "the shape is turned about a fixed point"),
            ("translation", "the shape slides without turning or flipping"),
            ("enlargement", "the shape is made larger, keeping the same proportions"),
        ])
        return _num_q("A transformation where %s is called a... (type one word)" % clue,
                      kind, "str", text=True,
                      placeholder="reflection / rotation / translation / enlargement",
                      solution=["Match the description to the transformation.",
                                "This is %s." % _a(kind)])

    if t == 6:                                        # reflect in y=0 / x=0 typed coord (no plot)
        x, y = _pt()
        line, ix, iy = pick([("the x-axis", x, -y), ("the y-axis", -x, y)])
        return _num_q("Reflect the point %s in %s. Write the image in the form (x,y)."
                      % (_coord(x, y), line), _coord(ix, iy), "coord",
                      solution=["Reflecting in %s changes the sign of one coordinate."
                                % line,
                                "The image is %s." % _coord(ix, iy)])

    if t == 7:                                        # which transformation preserves size?
        return _num_q("Reflections, rotations and translations all keep a shape the same "
                      "size and shape (they are congruent). Which one of these three "
                      "turns the shape about a point? (type one word)",
                      "rotation", "str", text=True,
                      placeholder="reflection / rotation / translation",
                      solution=["A turn about a point is a rotation.",
                                "The answer is rotation."])

    # translate: find the image coordinates typed
    x, y = _pt(hi=r - 3)
    a = random.randint(-3, 3) or 2
    b = random.randint(-3, 3) or -2
    return _num_q("Translate the point %s by the vector (%d, %d). Write the image in the "
                  "form (x,y)." % (_coord(x, y), a, b), _coord(x + a, y + b), "coord",
                  solution=["Add the vector: (%d + %d, %d + %d)." % (x, a, y, b),
                            "The image is %s." % _coord(x + a, y + b)])


@skill("Y8.8.j", "Enlarge by a scale factor from a centre", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 2])
    k = pick(_by_d(d, [2, 3], [2, 3, 4], [2, 3, 4, 5]))

    if t == 8:                                         # dilation: graph the image (plot)
        rg = _by_d(d, 6, 8, 10)
        px = random.randint(1, rg // k)
        py = random.randint(1, rg // k)
        ix, iy = k * px, k * py
        grid = {"mode": "plot", "xmin": -1, "xmax": rg, "ymin": -1, "ymax": rg,
                "points": [[px, py, "P"], [0, 0, "C"]]}
        return {"prompt": "Dilation (enlargement): graph the image of point P %s after a "
                          "dilation by scale factor %d from the centre C at the origin "
                          "(0,0). Plot the image of P." % (_coord(px, py), k),
                "component": "coordinate_grid", "spec": grid,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["From centre (0,0) a dilation multiplies each coordinate by "
                             "the scale factor %d." % k,
                             "The image of P is %s." % _coord(ix, iy)]}

    if t == 0:                                        # new length from scale factor
        L = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 8, 12, 20))
        return _num_q("A shape is enlarged by scale factor %d. A side of length %d cm "
                      "becomes how long, in cm?" % (k, L), k * L, "int", unit="cm",
                      solution=["Multiply every length by the scale factor.",
                                "%d × %d = %d cm." % (k, L, k * L)])

    if t == 1:                                        # find scale factor from lengths
        L = random.randint(2, 9)
        return _num_q("After an enlargement, a side that was %d cm is now %d cm. "
                      "What is the scale factor?" % (L, k * L), k, "int",
                      solution=["Scale factor = new length ÷ old length.",
                                "%d ÷ %d = %d." % (k * L, L, k)])

    if t == 2:                                        # find original from image
        L = random.randint(2, 9)
        return _num_q("A shape has been enlarged by scale factor %d. A side is now %d cm. "
                      "How long was the original side, in cm?" % (k, k * L), L, "int",
                      unit="cm",
                      solution=["Divide the new length by the scale factor.",
                                "%d ÷ %d = %d cm." % (k * L, k, L)])

    if t == 3:                                        # perimeter scales by k
        P = random.randint(6, 20)
        return _num_q("A shape with perimeter %d cm is enlarged by scale factor %d. "
                      "What is the perimeter of the enlarged shape, in cm?" % (P, k),
                      k * P, "int", unit="cm",
                      solution=["Every length, including the perimeter, is multiplied by "
                                "the scale factor.",
                                "%d × %d = %d cm." % (k, P, k * P)])

    if t == 4:                                        # area scales by k^2
        A = random.randint(3, 12)
        return _num_q("A shape has area %d cm². It is enlarged by scale factor %d. "
                      "The area is multiplied by the scale factor SQUARED. "
                      "What is the new area, in cm²?" % (A, k),
                      A * k * k, "int", unit="cm²",
                      solution=["Area scale factor = %d² = %d." % (k, k * k),
                                "%d × %d = %d cm²." % (A, k * k, A * k * k)])

    if t == 5:                                        # image of a vertex from origin (plot)
        r = _by_d(d, 6, 8, 10)
        px = random.randint(1, r // k)
        py = random.randint(1, r // k)
        ix, iy = k * px, k * py
        grid = {"mode": "plot", "xmin": -1, "xmax": r, "ymin": -1, "ymax": r,
                "points": [[px, py, "P"], [0, 0, "C"]]}
        return {"prompt": "P %s is enlarged by scale factor %d from the centre C at the "
                          "origin (0,0). Plot the image of P."
                          % (_coord(px, py), k),
                "component": "coordinate_grid", "spec": grid,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["From centre (0,0), multiply each coordinate by %d." % k,
                             "The image of P is %s." % _coord(ix, iy)]}

    if t == 6:                                        # scale factor from areas
        L = random.randint(2, 6)
        oldA = L * L
        newA = (k * L) * (k * L)
        return _num_q("A square of area %d cm² is enlarged to a square of area %d cm². "
                      "What is the LENGTH scale factor?" % (oldA, newA), k, "int",
                      solution=["The area scale factor is %d ÷ %d = %d = %d²."
                                % (newA, oldA, k * k, k),
                                "So the length scale factor is √%d = %d." % (k * k, k)])

    # word problem: model / map scale
    who = pick(NAMES)
    L = random.randint(3, 9)
    return _num_q("%s enlarges a photo by scale factor %d. A tree in the photo is %d cm "
                  "tall. How tall is the tree in the enlarged photo, in cm?"
                  % (who, k, L), k * L, "int", unit="cm",
                  solution=["Multiply the length by the scale factor.",
                            "%d × %d = %d cm." % (k, L, k * L)])


@skill("Y8.8.k", "Congruent and similar figures; missing lengths and angles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 2, 2])
    k = pick(_by_d(d, [2, 3], [2, 3, 4], [2, 3, 4, 5]))

    if t == 8:                                         # congruence statement: corresponding part
        corr = {"A": "D", "B": "E", "C": "F"}
        v = pick(["A", "B", "C"])
        return _num_q("Triangle ABC is congruent to triangle DEF, written ABC ≅ DEF. "
                      "The order of the letters shows the congruence correspondence. "
                      "Which vertex of triangle DEF corresponds to vertex %s of triangle "
                      "ABC? (type one letter)" % v, corr[v], "str", text=True,
                      placeholder="D / E / F",
                      solution=["In ABC ≅ DEF, A↔D, B↔E and C↔F.",
                                "The corresponding vertex is %s." % corr[v]])

    if t == 9:                                         # similarity statement: corresponding part
        corr = {"A": "P", "B": "Q", "C": "R"}
        v = pick(["A", "B", "C"])
        return _num_q("Triangle ABC is similar to triangle PQR, written ABC ~ PQR. "
                      "The order of the letters shows the similarity correspondence. "
                      "Which vertex of triangle PQR corresponds to vertex %s of triangle "
                      "ABC? (type one letter)" % v, corr[v], "str", text=True,
                      placeholder="P / Q / R",
                      solution=["In ABC ~ PQR, A↔P, B↔Q and C↔R.",
                                "The corresponding vertex is %s." % corr[v]])

    if t == 0:                                        # similar: missing length by ratio
        a = random.randint(2, 6)
        b = random.randint(a + 1, a + 6)
        A = k * a
        B = k * b
        return _num_q("Two triangles are similar. In the small triangle a side of %d cm "
                      "matches a side of %d cm in the large triangle (scale factor %d). "
                      "Another side of the small triangle is %d cm. How long is the "
                      "matching side in the large triangle, in cm?" % (a, A, k, b),
                      B, "int", unit="cm",
                      solution=["The scale factor is %d ÷ %d = %d." % (A, a, k),
                                "%d × %d = %d cm." % (b, k, B)])

    if t == 1:                                        # similar: find scale factor
        a = random.randint(2, 8)
        return _num_q("Two similar shapes have matching sides of %d cm and %d cm. "
                      "What is the scale factor from the smaller to the larger?"
                      % (a, k * a), k, "int",
                      solution=["Scale factor = larger ÷ smaller.",
                                "%d ÷ %d = %d." % (k * a, a, k)])

    if t == 2:                                        # similar: angle preserved (visual)
        ang = random.randint(30, 110)
        return {"prompt": "Two triangles are similar. An angle in the first triangle is "
                          "shown, %d°. How many degrees is the matching angle in the "
                          "second triangle?" % ang,
                "component": "angle", "spec": {"mode": "classify", "degrees": ang},
                "answer": ang, "answer_type": "int",
                "solution": ["Similar figures have equal matching angles.",
                             "The matching angle is also %d°." % ang]}

    if t == 3:                                        # congruent: equal side
        s = random.randint(3, 12)
        return _num_q("Two triangles are congruent (identical in size and shape). "
                      "A side of the first is %d cm. How long is the matching side of "
                      "the second, in cm?" % s, s, "int", unit="cm",
                      solution=["Congruent shapes are exactly the same size.",
                                "The matching side is also %d cm." % s])

    if t == 4:                                        # congruent yes/no
        same = random.random() < 0.5
        a1 = (random.randint(3, 8), random.randint(3, 8))
        if same:
            a2 = a1
            ans = "yes"
        else:
            a2 = (a1[0] + random.randint(1, 3), a1[1])
            ans = "no"
        return _num_q("Rectangle 1 measures %d cm by %d cm. Rectangle 2 measures %d cm "
                      "by %d cm. Are the two rectangles congruent? (type yes or no)"
                      % (a1[0], a1[1], a2[0], a2[1]), ans, "str", text=True,
                      placeholder="yes / no",
                      solution=["Congruent shapes have exactly the same measurements.",
                                "The answer is %s." % ans])

    if t == 5:                                        # similar or congruent (typed)
        which, ans = pick([
            ("the same shape but different sizes", "similar"),
            ("exactly the same shape AND the same size", "congruent"),
        ])
        return _num_q("Two figures that are %s are said to be... (type one word)" % which,
                      ans, "str", text=True, placeholder="similar / congruent",
                      solution=["Same shape different size = similar; same shape same "
                                "size = congruent.",
                                "The answer is %s." % ans])

    if t == 6:                                        # similar: missing length dividing
        b = random.randint(2, 7)
        B = k * b
        A_side = k * random.randint(2, 6)
        a_side = A_side // k
        return _num_q("A large photo is a scale factor %d enlargement of a small one. "
                      "The large photo is %d cm wide. How wide is the small photo, "
                      "in cm?" % (k, B), b, "int", unit="cm",
                      solution=["Divide the large length by the scale factor.",
                                "%d ÷ %d = %d cm." % (B, k, b)])

    # similar triangles find a third-angle then match
    a = random.randint(40, 80)
    b = random.randint(40, 80)
    while a + b >= 170:
        a, b = random.randint(40, 70), random.randint(40, 70)
    c = 180 - a - b
    return _num_q("Two triangles are similar. In the first triangle two angles are %d° "
                  "and %d°. In the second triangle, what is the size of the angle that "
                  "matches the THIRD angle of the first, in degrees?" % (a, b),
                  c, "int", unit="degrees",
                  solution=["The third angle of the first triangle is 180 − %d − %d = "
                            "%d°." % (a, b, c),
                            "Similar triangles have equal matching angles, so it is %d°."
                            % c])


@skill("Y8.8.l", "Pythagoras' theorem", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 4])
    a, b, c = pick(_TRIPLES if d else _TRIPLES[:6])

    if t == 8:                                        # hypotenuse from a table (visual)
        return _measure_table("The table gives the two shorter sides of a right-angled "
                              "triangle. Work out the hypotenuse, in cm.",
                              "Right-angled triangle", ["Side a (cm)", "Side b (cm)"],
                              [a, b], c,
                              ["Hypotenuse² = %d² + %d² = %d." % (a, b, c * c),
                               "Hypotenuse = √%d = %d cm." % (c * c, c)])

    if t == 0:                                        # find the hypotenuse (triple)
        return _num_q("A right-angled triangle has the two shorter sides %d cm and %d cm. "
                      "How long is the hypotenuse, in cm?" % (a, b), c, "int", unit="cm",
                      solution=["Hypotenuse² = %d² + %d² = %d + %d = %d."
                                % (a, b, a * a, b * b, c * c),
                                "Hypotenuse = √%d = %d cm." % (c * c, c)])

    if t == 1:                                        # find a shorter side (triple)
        return _num_q("A right-angled triangle has a hypotenuse of %d cm and one shorter "
                      "side of %d cm. How long is the other shorter side, in cm?"
                      % (c, a), b, "int", unit="cm",
                      solution=["Missing² = %d² − %d² = %d − %d = %d."
                                % (c, a, c * c, a * a, b * b),
                                "Missing side = √%d = %d cm." % (b * b, b)])

    if t == 2:                                        # hypotenuse, round to 1 dp
        p = random.randint(_by_d(d, 3, 4, 5), 9)
        q = random.randint(2, 9)
        while (p, q) in [(x, y) for x, y, _ in _TRIPLES] or p == q:
            q = random.randint(2, 9)
        h = math.sqrt(p * p + q * q)
        hr = round(h, 1)
        return _num_q("A right-angled triangle has shorter sides %d cm and %d cm. "
                      "Work out the hypotenuse. Give your answer to 1 decimal place, "
                      "in cm." % (p, q), hr, "num", tolerance=0.05, unit="cm",
                      solution=["Hypotenuse² = %d² + %d² = %d." % (p, q, p * p + q * q),
                                "Hypotenuse = √%d = %s cm (1 d.p.)."
                                % (p * p + q * q, _f(hr))])

    if t == 3:                                        # shorter side, round to 1 dp
        # use hypotenuse h and side s, both integers, missing not a perfect square
        h = random.randint(_by_d(d, 7, 8, 10), 15)
        s = random.randint(3, h - 2)
        val = h * h - s * s
        while val <= 0 or int(math.isqrt(val)) ** 2 == val:
            s = random.randint(3, h - 2)
            val = h * h - s * s
        m = round(math.sqrt(val), 1)
        return _num_q("A right-angled triangle has hypotenuse %d cm and one shorter side "
                      "%d cm. Work out the other shorter side. Give your answer to 1 "
                      "decimal place, in cm." % (h, s), m, "num", tolerance=0.05,
                      unit="cm",
                      solution=["Missing² = %d² − %d² = %d." % (h, s, val),
                                "Missing side = √%d = %s cm (1 d.p.)." % (val, _f(m))])

    if t == 4:                                        # ladder word problem (triple)
        return _num_q("A ladder %d m long leans against a wall. Its foot is %d m from "
                      "the base of the wall. How far up the wall does the ladder reach, "
                      "in m?" % (c, a), b, "int", unit="m",
                      solution=["The ladder is the hypotenuse: height² = %d² − %d² = %d."
                                % (c, a, b * b),
                                "Height = √%d = %d m." % (b * b, b)])

    if t == 5:                                        # diagonal of a rectangle (triple)
        return _num_q("A rectangle measures %d cm by %d cm. How long is its diagonal, "
                      "in cm?" % (a, b), c, "int", unit="cm",
                      solution=["The diagonal is the hypotenuse: diagonal² = %d² + %d² = "
                                "%d." % (a, b, c * c),
                                "Diagonal = √%d = %d cm." % (c * c, c)])

    if t == 6:                                        # perimeter of a right triangle
        return _num_q("A right-angled triangle has shorter sides %d cm and %d cm. "
                      "Work out the length of the hypotenuse, then the perimeter of the "
                      "triangle, in cm." % (a, b), a + b + c, "int", unit="cm",
                      solution=["Hypotenuse = √(%d² + %d²) = √%d = %d cm."
                                % (a, b, c * c, c),
                                "Perimeter = %d + %d + %d = %d cm." % (a, b, c, a + b + c)])

    if t == 7:                                        # distance between two points
        px, py = random.randint(-4, 0), random.randint(-4, 0)
        qx, qy = px + a, py + b
        return _num_q("On a coordinate grid, work out the distance between the points "
                      "%s and %s, in units. (The horizontal gap is %d and the vertical "
                      "gap is %d.)" % (_coord(px, py), _coord(qx, qy), a, b),
                      c, "int", unit="units",
                      solution=["Distance² = %d² + %d² = %d." % (a, b, c * c),
                                "Distance = √%d = %d units." % (c * c, c)])

    # is a triangle right-angled given the hypotenuse? find missing when told right
    return _num_q("A right-angled triangle has legs of %d cm and %d cm. "
                  "Work out the hypotenuse, in cm." % (a, b), c, "int", unit="cm",
                  solution=["h² = %d² + %d² = %d." % (a, b, c * c),
                            "h = √%d = %d cm." % (c * c, c)])


@skill("Y8.8.m", "Converse of Pythagoras", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 1, 1, 4, 3])
    a, b, c = pick(_TRIPLES if d else _TRIPLES[:6])

    if t == 8:                                         # converse: is it a right triangle?
        yes = random.random() < 0.5
        cc = c if yes else c + pick([1, 2])
        return _num_q("Converse of Pythagoras' theorem: is it a right triangle? "
                      "A triangle has sides %d cm, %d cm and %d cm. Using the converse, "
                      "check whether a² + b² = c² for the longest side. Is it a right "
                      "triangle? (type yes or no)" % (a, b, cc),
                      "yes" if yes else "no", "str", text=True, placeholder="yes / no",
                      solution=["%d² + %d² = %d, and %d² = %d."
                                % (a, b, a * a + b * b, cc, cc * cc),
                                "They are %s, so by the converse it %s a right triangle."
                                % ("equal" if yes else "not equal",
                                   "IS" if yes else "is NOT")])

    if t == 7:                                        # sides table, is it right-angled (visual)
        yes = random.random() < 0.5
        cc = c if yes else c + pick([1, 2])
        return _measure_table("The table gives the three sides of a triangle. Test "
                              "whether a² + b² = c² for the longest side c. Is the "
                              "triangle right-angled? (type yes or no)",
                              "Triangle sides (cm)", ["a", "b", "c"], [a, b, cc],
                              "yes" if yes else "no", atype="str",
                              solution=["%d² + %d² = %d, and %d² = %d."
                                        % (a, b, a * a + b * b, cc, cc * cc),
                                        "They are %s, so the triangle %s right-angled."
                                        % ("equal" if yes else "not equal",
                                           "IS" if yes else "is not")])

    if t == 0:                                        # is it right-angled? (yes, triple)
        return _num_q("A triangle has sides %d cm, %d cm and %d cm. Test whether it is "
                      "right-angled by checking if a² + b² = c². Is it right-angled? "
                      "(type yes or no)" % (a, b, c), "yes", "str", text=True,
                      placeholder="yes / no",
                      solution=["%d² + %d² = %d + %d = %d, and %d² = %d."
                                % (a, b, a * a, b * b, a * a + b * b, c, c * c),
                                "They are equal, so the triangle IS right-angled."])

    if t == 1:                                        # is it right-angled? (no)
        cc = c + pick([1, 2])
        return _num_q("A triangle has sides %d cm, %d cm and %d cm. Check whether "
                      "a² + b² = c². Is the triangle right-angled? (type yes or no)"
                      % (a, b, cc), "no", "str", text=True, placeholder="yes / no",
                      solution=["%d² + %d² = %d, but %d² = %d."
                                % (a, b, a * a + b * b, cc, cc * cc),
                                "They are NOT equal, so the triangle is not "
                                "right-angled."])

    if t == 2:                                        # acute / right / obtuse test
        kind = pick(["right", "acute", "obtuse"])
        if kind == "right":
            sides = (a, b, c)
        elif kind == "acute":
            sides = (a, b, c - 1)
        else:
            sides = (a, b, c + 2)
        s = sorted(sides)
        lhs = s[0] ** 2 + s[1] ** 2
        rhs = s[2] ** 2
        real = "right" if lhs == rhs else ("acute" if lhs > rhs else "obtuse")
        return _num_q("For the longest side c, compare a² + b² with c². A triangle has "
                      "sides %d, %d and %d. If a² + b² = c² it is right-angled, if bigger "
                      "it is acute, if smaller it is obtuse. Which is it? (type one word)"
                      % sides, real, "str", text=True,
                      placeholder="right / acute / obtuse",
                      solution=["%d² + %d² = %d and %d² = %d."
                                % (s[0], s[1], lhs, s[2], rhs),
                                "%s, so the triangle is %s-angled."
                                % ("They are equal" if real == "right"
                                   else ("The sum is larger" if real == "acute"
                                         else "The sum is smaller"),
                                   real) if real == "right" else
                                "The triangle is %s." % real])

    if t == 3:                                        # value of a^2+b^2 (int)
        return _num_q("To test a triangle with sides %d, %d and %d for a right angle, "
                      "work out %d² + %d² (the two shorter sides squared and added)."
                      % (a, b, c, a, b), a * a + b * b, "int",
                      solution=["%d² = %d and %d² = %d." % (a, a * a, b, b * b),
                                "%d + %d = %d." % (a * a, b * b, a * a + b * b)])

    if t == 4:                                        # value of c^2 (int)
        return _num_q("For the triangle with sides %d, %d and %d, work out the square of "
                      "the LONGEST side, %d²." % (a, b, c, c), c * c, "int",
                      solution=["%d² = %d × %d = %d." % (c, c, c, c * c)])

    if t == 5:                                        # word: is the corner square?
        return _num_q("A builder measures a triangular frame with sides %d cm, %d cm and "
                      "%d cm and wants a perfect right-angled corner. Does %d² + %d² = "
                      "%d²? Answer whether the corner is a true right angle (type yes or "
                      "no)." % (a, b, c, a, b, c), "yes", "str", text=True,
                      placeholder="yes / no",
                      solution=["%d + %d = %d = %d." % (a * a, b * b, a * a + b * b, c * c),
                                "The equation holds, so the corner IS a right angle."])

    # which is the hypotenuse (longest side)
    return _num_q("In a right-angled triangle with sides %d, %d and %d, the hypotenuse "
                  "is the longest side. Which of the three lengths is the hypotenuse?"
                  % (a, b, c), c, "int",
                  solution=["The hypotenuse is opposite the right angle and is the "
                            "longest side.",
                            "Here that is %d." % c])


@skill("Y8.8.n", "Ruler-and-compass constructions", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 1, 1])

    if t == 7:                                        # bisecting a straight angle
        return _num_q("A perpendicular bisector construction is used to split a straight "
                      "angle (180°) into two equal parts. How many degrees is each part?",
                      90, "int", unit="degrees",
                      solution=["A straight angle is 180° and it is split in half.",
                                "180 ÷ 2 = 90°."])

    if t == 0:                                        # identify construction from description
        desc, ans = pick([
            ("cuts a line segment exactly in half and crosses it at 90°",
             "perpendicular bisector"),
            ("cuts an angle exactly in half into two equal parts", "angle bisector"),
        ])
        return _num_q("Which standard construction produces a line that %s? "
                      "(type two words)" % desc, ans, "str", text=True,
                      placeholder="perpendicular bisector / angle bisector",
                      solution=["Equal arcs from each end of a segment give the "
                                "perpendicular bisector; equal arcs from an angle give "
                                "the angle bisector.",
                                "The answer is the %s." % ans])

    if t == 1:                                        # what tool
        return _num_q("Which drawing instrument is used to draw arcs of equal radius "
                      "when doing a construction? (type one word)", "compasses", "str",
                      text=True, placeholder="compasses / ruler / protractor",
                      solution=["Arcs of equal radius are drawn with a pair of "
                                "compasses.",
                                "The answer is compasses."])

    if t == 2:                                        # angle bisector halves the angle
        ang = pick([40, 60, 80, 90, 100, 120, 140])
        return _num_q("An angle of %d° is bisected by a ruler-and-compass construction. "
                      "How many degrees is each of the two equal angles?" % ang,
                      ang // 2, "int", unit="degrees",
                      solution=["Bisecting halves the angle.",
                                "%d ÷ 2 = %d°." % (ang, ang // 2)])

    if t == 3:                                        # perpendicular bisector makes 90
        return _num_q("A perpendicular bisector meets the original line segment. "
                      "At how many degrees does it cross the segment?", 90, "int",
                      unit="degrees",
                      solution=["'Perpendicular' means at a right angle.",
                                "The answer is 90°."])

    if t == 4:                                        # bisector of a segment - equal halves
        L = pick([6, 8, 10, 12, 14, 16])
        return _num_q("A line segment of length %d cm is cut by its perpendicular "
                      "bisector. How long is each of the two equal parts, in cm?" % L,
                      L // 2, "int", unit="cm",
                      solution=["The bisector cuts the segment exactly in half.",
                                "%d ÷ 2 = %d cm." % (L, L // 2)])

    if t == 5:                                        # construct 60 by equilateral
        return _num_q("Constructing an equilateral triangle with compasses creates an "
                      "angle you can copy. How many degrees is each angle of an "
                      "equilateral triangle?", 60, "int", unit="degrees",
                      solution=["An equilateral triangle has three equal angles adding "
                                "to 180°.",
                                "180 ÷ 3 = 60°."])

    # true/false about constructions
    claim, tf = pick([
        ("A perpendicular bisector passes through the midpoint of the segment", "true"),
        ("An angle bisector is drawn using a protractor only", "false"),
        ("Construction arcs should all have the same compass radius unless told "
         "otherwise", "true"),
    ])
    return _num_q("True or false: %s. (type true or false)" % claim, tf, "str",
                  text=True, placeholder="true / false",
                  solution=["Standard constructions use compasses and a straight edge.",
                            "The statement is %s." % tf])


@skill("Y8.8.o", "Three-figure bearings", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 2, 2, 2, 2, 2, 1, 1])
    _COMPASS = [("north", 0), ("east", 90), ("south", 180), ("west", 270),
                ("north-east", 45), ("south-east", 135), ("south-west", 225),
                ("north-west", 315)]

    if t == 0:                                        # compass direction -> bearing
        name, val = pick(_COMPASS)
        return _num_q("Bearings are measured clockwise from north and written with three "
                      "figures. What is the three-figure bearing of due %s? "
                      "(write it as three figures, e.g. 072)" % name, val, "int",
                      solution=["North is 000°, and bearings increase clockwise.",
                                "Due %s is %s°." % (name, _bear(val))])

    if t == 1:                                        # bearing -> compass direction
        name, val = pick(_COMPASS)
        return _num_q("A ship sails on a bearing of %s°. Which compass direction is "
                      "that? (type the direction, e.g. north-east)" % _bear(val),
                      name, "str", text=True,
                      placeholder="north / east / south / west / north-east ...",
                      solution=["Compare with north = 000°, east = 090°, south = 180°, "
                                "west = 270°.",
                                "%s° is due %s." % (_bear(val), name)])

    if t == 2:                                        # back bearing (add 180)
        b = random.randint(_by_d(d, 10, 5, 1), 170)
        back = b + 180
        return _num_q("The bearing of B from A is %s°. The BACK bearing (of A from B) is "
                      "found by adding 180°. What is the back bearing? "
                      "(write three figures)" % _bear(b), back, "int",
                      solution=["Back bearing = %d + 180 = %d." % (b, back),
                                "As a three-figure bearing that is %s°." % _bear(back)])

    if t == 3:                                        # back bearing (subtract 180)
        b = random.randint(190, 350)
        back = b - 180
        return _num_q("The bearing of Q from P is %s°. Because this is more than 180°, "
                      "the back bearing (of P from Q) is found by SUBTRACTING 180°. "
                      "What is the back bearing? (write three figures)" % _bear(b),
                      back, "int",
                      solution=["Back bearing = %d − 180 = %d." % (b, back),
                                "As a three-figure bearing that is %s°." % _bear(back)])

    if t == 4:                                        # angle turned between two bearings
        b1 = random.randint(10, 150)
        turn = random.randint(20, 120)
        b2 = b1 + turn
        return _num_q("A walker faces on a bearing of %s° then turns clockwise to face "
                      "%s°. Through how many degrees did the walker turn?"
                      % (_bear(b1), _bear(b2)), turn, "int", unit="degrees",
                      solution=["The turn is the difference in bearings.",
                                "%d − %d = %d°." % (b2, b1, turn)])

    if t == 5:                                        # bearing from a clockwise angle from north
        ang = random.randint(_by_d(d, 10, 5, 1), 99)
        return _num_q("A lighthouse is seen at an angle of %d° measured clockwise from "
                      "north. Write this as a three-figure bearing." % ang, _bear(ang), "str", text=True, placeholder="e.g. 072",
                      solution=["The bearing IS the clockwise angle from north.",
                                "As three figures: %s°." % _bear(ang)])

    if t == 6:                                        # bearing of due north/east reasoning
        pairs = pick([("north and east", "north-east", 45),
                      ("south and east", "south-east", 135),
                      ("south and west", "south-west", 225),
                      ("north and west", "north-west", 315)])
        _, name, val = pairs
        return _num_q("A path runs exactly halfway between %s. What three-figure bearing "
                      "is this? (write three figures)" % pairs[0], val, "int",
                      solution=["Halfway between the two directions is the %s bearing."
                                % name,
                                "That is %s°." % _bear(val)])

    # opposite direction bearing
    b = pick([30, 45, 60, 90, 120, 150])
    return _num_q("A boat travels on a bearing of %s°. It then turns to travel in exactly "
                  "the OPPOSITE direction. What three-figure bearing is it now on? "
                  "(write three figures)" % _bear(b), b + 180, "int",
                  solution=["The opposite direction is 180° round.",
                            "%d + 180 = %d°, written %s°." % (b, b + 180, _bear(b + 180))])


# ================================================================== 8.9 ======
_METRIC8 = [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10),
            ("kg", "g", 1000), ("l", "ml", 1000), ("t", "kg", 1000),
            ("m", "mm", 1000)]
_UNITWORD = {"km": "kilometres", "m": "metres", "cm": "centimetres", "mm": "millimetres",
             "kg": "kilograms", "g": "grams", "l": "litres", "ml": "millilitres",
             "t": "tonnes"}


@skill("Y8.9.a", "Convert and estimate metric units", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 2, 5, 1])
    big, small, k = pick(_METRIC8)

    if t == 7:                                        # conversion table with a gap (visual)
        base = random.randint(1, 6)
        vs = [base + i for i in range(4)]
        rows = [[str(v), str(v * k)] for v in vs]
        i = random.randrange(4)
        j = random.randrange(2)
        ans = int(rows[i][j])
        blank = [list(r) for r in rows]
        blank[i][j] = "?"
        return {"prompt": "This table converts %s into %s (1 %s = %d %s). What number "
                          "belongs in the cell marked ?"
                          % (_UNITWORD[big], _UNITWORD[small], big, k, small),
                "component": "data_table",
                "spec": {"caption": "%s and %s" % (_UNITWORD[big].capitalize(),
                                                   _UNITWORD[small].capitalize()),
                         "headers": [big, small], "rows": blank, "missing": [i, j]},
                "answer": ans, "answer_type": "int",
                "solution": ["1 %s = %d %s." % (big, k, small),
                             "The missing number is %d." % ans]}

    if t == 0:                                        # big -> small (multiply)
        v = random.randint(_by_d(d, 2, 2, 3), _by_d(d, 9, 20, 40))
        return _num_q("Convert %d %s into %s. (1 %s = %d %s)"
                      % (v, big, _UNITWORD[small], big, k, small),
                      v * k, "int", unit=small,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%d × %d = %d %s." % (v, k, v * k, small)])

    if t == 1:                                        # small -> big (divide, exact)
        v = random.randint(2, _by_d(d, 9, 20, 40)) * k
        return _num_q("Convert %d %s into %s. (1 %s = %d %s)"
                      % (v, small, _UNITWORD[big], big, k, small),
                      v // k, "int", unit=big,
                      solution=["%d %s = 1 %s." % (k, small, big),
                                "%d ÷ %d = %d %s." % (v, k, v // k, big)])

    if t == 2:                                        # decimal big -> small
        whole = random.randint(1, 8)
        half = pick([25, 5, 75, 2]) if k >= 100 else 5
        v = whole + half / 100.0 if k >= 100 else whole + 0.5
        res = int(round(v * k))
        return _num_q("Convert %s %s into %s. (1 %s = %d %s)"
                      % (_f(v), big, _UNITWORD[small], big, k, small),
                      res, "int", unit=small,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%s × %d = %d %s." % (_f(v), k, res, small)])

    if t == 3:                                        # small -> big giving a decimal
        v = random.randint(1, k // 2) + random.randint(1, k - 1)
        # ensure a tidy-ish decimal: pick v as multiple giving 1 or 2 dp
        v = pick([k // 4, k // 2, 3 * k // 4, k + k // 2]) if k in (100, 1000) else k // 2
        res = v / float(k)
        return _num_q("Convert %d %s into %s, as a decimal." % (v, small, _UNITWORD[big]),
                      res, "num", unit=big, tolerance=0.0005,
                      solution=["%d %s = 1 %s." % (k, small, big),
                                "%d ÷ %d = %s %s." % (v, k, _f(res), big)])

    if t == 4:                                        # estimate real-life quantity (typed)
        item, unit, val = pick([
            ("the mass of an apple", "grams", "g"),
            ("the height of a classroom door", "metres", "m"),
            ("the length of an ant", "millimetres", "mm"),
            ("the capacity of a bath", "litres", "l"),
            ("the distance between two cities", "kilometres", "km"),
            ("the mass of a car", "tonnes", "tonne"),
        ])
        return _num_q("Which metric unit is the most sensible for measuring %s? "
                      "(type the unit name, e.g. grams)" % item, unit, "str", text=True,
                      placeholder="millimetres / centimetres / metres / kilometres / "
                                  "grams / kilograms / tonnes / litres",
                      solution=["Choose a unit that gives a sensible-sized number.",
                                "%s is best measured in %s." % (item.capitalize(), unit)])

    if t == 5:                                        # add two mixed measures
        aa = random.randint(1, 8)
        bb = random.randint(1, k - 1)
        total = aa * k + bb
        return _num_q("Add %d %s and %d %s. Give the total in %s."
                      % (aa, big, bb, small, _UNITWORD[small]),
                      total, "int", unit=small,
                      solution=["%d %s = %d %s." % (aa, big, aa * k, small),
                                "%d + %d = %d %s." % (aa * k, bb, total, small)])

    if t == 6:                                        # compare two measures
        v1 = random.randint(2, 9) * k          # in small units
        v2 = round(random.uniform(1.2, 9.5), 1)  # in big units
        while abs(v1 - v2 * k) < 1:
            v2 = round(random.uniform(1.2, 9.5), 1)
        ans = "A" if v1 > v2 * k else "B"
        return _num_q("Measurement A is %d %s. Measurement B is %s %s. Which is larger? "
                      "(type A or B)" % (v1, small, _f(v2), big), ans, "str", text=True,
                      placeholder="A / B",
                      solution=["B = %s %s = %s %s." % (_f(v2), big, _f(v2 * k), small),
                                "The larger is %s." % ans])

    # word problem: total in big units
    who = pick(NAMES)
    n = random.randint(3, 8)
    each = random.randint(150, 950)
    total = n * each
    return _num_q("%s buys %d bags of rice, each %d g. What is the total mass in "
                  "kilograms?" % (who, n, each), total / 1000.0, "num", unit="kg",
                  tolerance=0.0005,
                  solution=["%d × %d = %d g." % (n, each, total),
                            "%d ÷ 1000 = %s kg." % (total, _f(total / 1000.0))])


@skill("Y8.9.b", "Convert area/volume units; metric-imperial; precision", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 2, 1, 1, 5, 3, 3, 3, 3])

    if t == 10:                                       # square metres <-> hectares
        ha = random.randint(2, _by_d(d, 5, 12, 40))
        if random.random() < 0.5:
            return _num_q("Convert between square metres and hectares. "
                          "1 hectare = 10 000 m². How many square metres are there in "
                          "%d hectares?" % ha, ha * 10000, "int", unit="m²",
                          solution=["1 hectare = 10 000 m².",
                                    "%d × 10 000 = %d m²." % (ha, ha * 10000)])
        return _num_q("Convert between square metres and hectares. "
                      "1 hectare = 10 000 m². How many hectares is %d m²?"
                      % (ha * 10000), ha, "int", unit="hectares",
                      solution=["1 hectare = 10 000 m².",
                                "%d ÷ 10 000 = %d hectares." % (ha * 10000, ha)])

    if t == 11:                                       # square / cubic units of length
        if random.random() < 0.5:
            m = random.randint(2, _by_d(d, 4, 7, 12))
            return _num_q("Convert square units of length. 1 m² = 10 000 cm². "
                          "How many square centimetres are there in %d m²?" % m,
                          m * 10000, "int", unit="cm²",
                          solution=["1 m = 100 cm, so 1 m² = 100 × 100 = 10 000 cm².",
                                    "%d × 10 000 = %d cm²." % (m, m * 10000)])
        m = random.randint(2, _by_d(d, 3, 5, 9))
        return _num_q("Convert cubic units of length. 1 m³ = 1 000 000 cm³. "
                      "How many cubic centimetres are there in %d m³?" % m,
                      m * 1000000, "int", unit="cm³",
                      solution=["1 m = 100 cm, so 1 m³ = 100 × 100 × 100 = 1 000 000 cm³.",
                                "%d × 1 000 000 = %d cm³." % (m, m * 1000000)])

    if t == 12:                                       # cubic metres <-> litres
        v = random.randint(2, _by_d(d, 6, 15, 40))
        if random.random() < 0.5:
            return _num_q("Convert between cubic metres and litres. 1 m³ = 1000 litres. "
                          "How many litres of water fill a tank of %d m³?" % v,
                          v * 1000, "int", unit="litres",
                          solution=["1 m³ = 1000 litres.",
                                    "%d × 1000 = %d litres." % (v, v * 1000)])
        return _num_q("Convert between cubic metres and litres. 1 m³ = 1000 litres. "
                      "How many cubic metres is %d litres?" % (v * 1000), v, "int",
                      unit="m³", solution=["1 m³ = 1000 litres.",
                                           "%d ÷ 1000 = %d m³." % (v * 1000, v)])

    if t == 13:                                       # estimate imperial measurements
        item, unit, ans = pick([
            ("the length of a school bus", "feet", 40),
            ("the height of a door", "feet", 7),
            ("the mass of an apple", "ounces", 6),
            ("the amount of milk in a large carton", "pints", 4),
            ("the length of an adult's foot", "inches", 10),
        ])
        distractors = sorted({ans * 3, max(1, ans // 3), ans * 8} - {ans})
        opts = sorted(set([ans] + distractors[:2]))
        return _num_q("Estimate this imperial measurement. Which is the most reasonable "
                      "estimate for %s: %s %s? (type the number)"
                      % (item, ", ".join(str(o) for o in opts), unit),
                      ans, "int", unit=unit,
                      solution=["A sensible estimate is about %d %s." % (ans, unit)])

    if t == 9:                                        # area conversion table (visual)
        big, small, k = pick([("cm²", "mm²", 100), ("m²", "cm²", 10000)])
        vs = [random.randint(1, 5) + i for i in range(4)]
        rows = [[str(v), str(v * k)] for v in vs]
        i = random.randrange(4)
        j = random.randrange(2)
        ans = int(rows[i][j])
        blank = [list(r) for r in rows]
        blank[i][j] = "?"
        return {"prompt": "This table converts %s into %s (1 %s = %d %s). What number "
                          "belongs in the cell marked ?" % (big, small, big, k, small),
                "component": "data_table",
                "spec": {"caption": "%s and %s" % (big, small),
                         "headers": [big, small], "rows": blank, "missing": [i, j]},
                "answer": ans, "answer_type": "int",
                "solution": ["1 %s = %d %s." % (big, k, small),
                             "The missing number is %d." % ans]}

    if t == 0:                                        # cm^2 <-> mm^2 or m^2 <-> cm^2
        big, small, k = pick([("cm²", "mm²", 100), ("m²", "cm²", 10000)])
        v = random.randint(2, _by_d(d, 6, 12, 25))
        return _num_q("Area conversion: 1 %s = %d %s. Convert %d %s into %s."
                      % (big, k, small, v, big, small),
                      v * k, "int", unit=small,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%d × %d = %d %s." % (v, k, v * k, small)])

    if t == 1:                                        # m^3 <-> cm^3 or litre <-> cm^3
        big, small, k = pick([("m³", "cm³", 1000000), ("litre", "cm³", 1000)])
        v = random.randint(2, _by_d(d, 5, 9, 15))
        return _num_q("Volume conversion: 1 %s = %d %s. Convert %d %s into %s."
                      % (big, k, small, v, big, small),
                      v * k, "int", unit=small,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%d × %d = %d %s." % (v, k, v * k, small)])

    if t == 2:                                        # area convert back (divide)
        big, small, k = pick([("cm²", "mm²", 100), ("m²", "cm²", 10000)])
        v = random.randint(2, 8) * k
        return _num_q("Convert %d %s into %s. (1 %s = %d %s)"
                      % (v, small, big, big, k, small),
                      v // k, "int", unit=big,
                      solution=["%d %s = 1 %s." % (k, small, big),
                                "%d ÷ %d = %d %s." % (v, k, v // k, big)])

    if t == 3:                                        # metric-imperial length
        approx, factor, unit_from, unit_to = pick([
            ("1 inch ≈ 2.5 cm", 2.5, "inches", "cm"),
            ("1 foot ≈ 30 cm", 30, "feet", "cm"),
            ("1 mile ≈ 1.6 km", 1.6, "miles", "km"),
        ])
        n = random.randint(2, _by_d(d, 6, 12, 20))
        val = round(n * factor, 2)
        return _num_q("%s. About how many %s are there in %d %s?"
                      % (approx, unit_to, n, unit_from), val, "num", unit=unit_to,
                      tolerance=0.05,
                      solution=[approx + ".",
                                "%d × %s = %s %s." % (n, _f(factor), _f(val), unit_to)])

    if t == 4:                                        # metric-imperial mass/capacity
        approx, factor, unit_from, unit_to = pick([
            ("1 kg ≈ 2.2 pounds", 2.2, "kg", "pounds"),
            ("1 gallon ≈ 4.5 litres", 4.5, "gallons", "litres"),
        ])
        n = random.randint(2, _by_d(d, 5, 9, 15))
        val = round(n * factor, 2)
        return _num_q("%s. About how many %s are there in %d %s?"
                      % (approx, unit_to, n, unit_from), val, "num", unit=unit_to,
                      tolerance=0.05,
                      solution=[approx + ".",
                                "%d × %s = %s %s." % (n, _f(factor), _f(val), unit_to)])

    if t == 5:                                        # round to decimal places
        whole = random.randint(2, 98)
        dp = pick([1, 2])
        if dp == 1:                                   # 2 decimals in, round to 1
            dec = random.randint(1, 99)
            while dec % 10 in (0, 5):                 # avoid halves and trivial cases
                dec = random.randint(1, 99)
            v = whole + dec / 100.0
        else:                                         # 3 decimals in, round to 2
            dec = random.randint(1, 999)
            while dec % 10 in (0, 5):
                dec = random.randint(1, 999)
            v = whole + dec / 1000.0
        res = round(v, dp)
        return _num_q("Round %s to %d decimal place%s."
                      % (_f(v), dp, "" if dp == 1 else "s"), res, "num",
                      tolerance=0,
                      solution=["Look at the digit after the %s decimal place."
                                % ("first" if dp == 1 else "second"),
                                "%s rounds to %s." % (_f(v), _f(res))])

    if t == 6:                                        # round to significant figures
        sf = pick([1, 2, 3])
        v = random.randint(1000, 99999)
        while v % (10 ** (len(str(v)) - sf)) == 0:     # already at that accuracy: nothing to do
            v = random.randint(1000, 99999)
        # round v to sf significant figures
        from math import log10, floor
        digits = int(floor(log10(v)))
        f = 10 ** (digits - sf + 1)
        res = (v + f // 2) // f * f                    # round half up, as taught
        return _num_q("Round %d to %d significant figure%s." % (v, sf, "" if sf == 1
                                                                else "s"),
                      res, "int",
                      solution=["Keep the first %d non-zero digit%s and fill the rest "
                                "with zeros, rounding as needed." % (sf, "" if sf == 1
                                                                     else "s"),
                                "%d to %d s.f. is %d." % (v, sf, res)])

    if t == 7:                                        # precision: bounds / nearest
        v = random.randint(10, 90) * 10
        return _num_q("A length is given as %d cm, measured to the nearest 10 cm. "
                      "What is the SMALLEST length it could actually be, in cm?" % v,
                      v - 5, "num", unit="cm", tolerance=0.001,
                      solution=["Measured to the nearest 10 cm, the true value is within "
                                "5 cm.",
                                "The smallest possible value is %d − 5 = %d cm."
                                % (v, v - 5)])

    # area word problem
    side = random.randint(2, 6)
    return _num_q("A square tile has sides of %d cm, so its area is %d cm². "
                  "What is that area in mm²? (1 cm² = 100 mm²)" % (side, side * side),
                  side * side * 100, "int", unit="mm²",
                  solution=["Area = %d × %d = %d cm²." % (side, side, side * side),
                            "%d × 100 = %d mm²." % (side * side, side * side * 100)])


@skill("Y8.9.c", "Area of triangles, parallelograms, trapeziums, rhombuses", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 1, 5, 3])

    if t == 9:                                        # area from a measurements table (visual)
        base = random.randint(4, 20)
        h = random.randint(3, 14)
        while (base * h) % 2:
            h += 1
        return _measure_table("The table gives the base and perpendicular height of a "
                              "triangle. Work out its area, in cm². (Area = ½ × base × "
                              "height.)", "Triangle", ["Base (cm)", "Height (cm)"],
                              [base, h], base * h // 2,
                              ["Area = ½ × %d × %d = %d cm²."
                               % (base, h, base * h // 2)])

    if t == 10:                                       # parallelogram area from table (visual)
        base = random.randint(4, 20)
        h = random.randint(3, 14)
        return _measure_table("The table gives the base and perpendicular height of a "
                              "parallelogram. Work out its area, in cm². "
                              "(Area = base × height.)", "Parallelogram",
                              ["Base (cm)", "Height (cm)"], [base, h], base * h,
                              ["Area = %d × %d = %d cm²." % (base, h, base * h)])

    if t == 0:                                        # triangle area
        base = random.randint(_by_d(d, 4, 5, 6), _by_d(d, 12, 18, 24))
        h = random.randint(3, _by_d(d, 10, 16, 22))
        while (base * h) % 2:
            h += 1
        return _num_q("A triangle has base %d cm and perpendicular height %d cm. "
                      "Area = ½ × base × height. What is its area, in cm²?" % (base, h),
                      base * h // 2, "int", unit="cm²",
                      solution=["Area = ½ × %d × %d." % (base, h),
                                "= %d cm²." % (base * h // 2)])

    if t == 1:                                        # parallelogram area
        base = random.randint(_by_d(d, 4, 5, 6), _by_d(d, 12, 18, 25))
        h = random.randint(3, _by_d(d, 10, 15, 20))
        return _num_q("A parallelogram has base %d cm and perpendicular height %d cm. "
                      "Area = base × height. What is its area, in cm²?" % (base, h),
                      base * h, "int", unit="cm²",
                      solution=["Area = %d × %d." % (base, h),
                                "= %d cm²." % (base * h)])

    if t == 2:                                        # trapezium area
        aa = random.randint(3, 10)
        bb = random.randint(aa + 1, aa + 12)
        h = random.randint(2, _by_d(d, 8, 12, 18))
        while ((aa + bb) * h) % 2:
            h += 1
        area = (aa + bb) * h // 2
        return _num_q("A trapezium has parallel sides %d cm and %d cm, and the distance "
                      "between them is %d cm. Area = ½ × (a + b) × h. What is its area, "
                      "in cm²?" % (aa, bb, h), area, "int", unit="cm²",
                      solution=["Area = ½ × (%d + %d) × %d." % (aa, bb, h),
                                "= ½ × %d × %d = %d cm²." % (aa + bb, h, area)])

    if t == 3:                                        # rhombus / kite from diagonals
        d1 = random.randint(4, 16)
        d2 = random.randint(4, 16)
        while (d1 * d2) % 2:
            d2 += 1
        return _num_q("A rhombus has diagonals of %d cm and %d cm. "
                      "Area = ½ × d₁ × d₂. What is its area, in cm²?" % (d1, d2),
                      d1 * d2 // 2, "int", unit="cm²",
                      solution=["Area = ½ × %d × %d." % (d1, d2),
                                "= %d cm²." % (d1 * d2 // 2)])

    if t == 4:                                        # inverse: triangle base from area
        base = random.randint(4, 16)
        h = random.randint(3, 12)
        while (base * h) % 2:
            h += 1
        area = base * h // 2
        return _num_q("A triangle has area %d cm² and perpendicular height %d cm. "
                      "What is the length of its base, in cm? (Area = ½ × base × height.)"
                      % (area, h), base, "int", unit="cm",
                      solution=["base = 2 × area ÷ height.",
                                "2 × %d ÷ %d = %d cm." % (area, h, base)])

    if t == 5:                                        # inverse: parallelogram height
        base = random.randint(4, 15)
        h = random.randint(3, 12)
        area = base * h
        return _num_q("A parallelogram has area %d cm² and base %d cm. "
                      "What is its perpendicular height, in cm?" % (area, base), h, "int",
                      unit="cm",
                      solution=["height = area ÷ base.",
                                "%d ÷ %d = %d cm." % (area, base, h)])

    if t == 6:                                        # triangle area word problem
        who = pick(NAMES)
        base = random.randint(6, 20)
        h = random.randint(4, 16)
        while (base * h) % 2:
            h += 1
        return _num_q("%s cuts a triangular flag with base %d cm and height %d cm. "
                      "What is the area of the flag, in cm²?" % (who, base, h),
                      base * h // 2, "int", unit="cm²",
                      solution=["Area = ½ × %d × %d = %d cm²."
                                % (base, h, base * h // 2)])

    if t == 7:                                        # compare two areas
        A1 = random.randint(20, 60)
        A2 = random.randint(20, 60)
        while A1 == A2:
            A2 = random.randint(20, 60)
        ans = "A" if A1 > A2 else "B"
        return _num_q("Triangle A has area %d cm² and parallelogram B has area %d cm². "
                      "Which has the LARGER area? (type A or B)" % (A1, A2), ans, "str",
                      text=True, placeholder="A / B",
                      solution=["Compare %d cm² and %d cm²." % (A1, A2),
                                "The larger is %s." % ans])

    # trapezium: find the missing parallel side
    aa = random.randint(3, 9)
    h = random.randint(2, 8) * 2
    bb = random.randint(aa + 2, aa + 10)
    area = (aa + bb) * h // 2
    return _num_q("A trapezium has area %d cm², a height of %d cm and one parallel side "
                  "of %d cm. How long is the other parallel side, in cm? "
                  "(Area = ½ × (a + b) × h.)" % (area, h, aa), bb, "int", unit="cm",
                  solution=["a + b = 2 × area ÷ h = 2 × %d ÷ %d = %d."
                            % (area, h, aa + bb),
                            "%d − %d = %d cm." % (aa + bb, aa, bb)])


@skill("Y8.9.d", "Circumference and area of circles and parts", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 1, 1])
    rr = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 7, 10, 14))

    if t == 0:                                        # circumference from diameter (3.14)
        dia = 2 * rr
        c = round(3.14 * dia, 2)
        return {"prompt": "Take π as 3.14. A circle has diameter %d cm. What is its "
                          "circumference, in cm? (C = π × d)" % dia,
                "component": "circle",
                "spec": {"radius": rr, "show": "circumference", "label": "d = %d cm" % dia},
                "answer": c, "answer_type": "num", "tolerance": 0.05,
                "solution": ["C = π × diameter = 3.14 × %d." % dia,
                             "= %s cm." % _f(c)]}

    if t == 1:                                        # area from radius (3.14)
        a = round(3.14 * rr * rr, 2)
        return {"prompt": "Take π as 3.14. A circle has radius %d cm. What is its area, "
                          "in cm²? (A = π × r²)" % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": a, "answer_type": "num", "tolerance": 0.05,
                "solution": ["A = π × r² = 3.14 × %d²." % rr,
                             "= 3.14 × %d = %s cm²." % (rr * rr, _f(a))]}

    if t == 2:                                        # circumference in terms of pi (coeff)
        dia = 2 * rr
        return {"prompt": "Leave your answer in terms of π. This circle has diameter %d "
                          "cm, so its circumference is kπ cm where C = πd. What is the "
                          "value of k?" % dia,
                "component": "circle",
                "spec": {"radius": rr, "show": "circumference", "label": "d = %d cm" % dia},
                "answer": dia, "answer_type": "int",
                "solution": ["C = π × d = π × %d = %dπ." % (dia, dia),
                             "So k = %d." % dia]}

    if t == 3:                                        # area in terms of pi (coeff)
        return {"prompt": "Leave your answer in terms of π. This circle has radius %d cm, "
                          "so its area is kπ cm² where A = πr². What is the value of k?"
                          % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": rr * rr, "answer_type": "int",
                "solution": ["A = π × r² = π × %d² = %dπ." % (rr, rr * rr),
                             "So k = %d." % (rr * rr)]}

    if t == 4:                                        # circumference from radius (3.14)
        c = round(2 * 3.14 * rr, 2)
        return {"prompt": "Take π as 3.14. This circle has radius %d cm. What is its "
                          "circumference, in cm? (C = 2 × π × r)" % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": c, "answer_type": "num", "tolerance": 0.05,
                "solution": ["C = 2 × π × r = 2 × 3.14 × %d." % rr,
                             "= %s cm." % _f(c)]}

    if t == 5:                                        # semicircle area
        a = round(3.14 * rr * rr / 2.0, 2)
        return {"prompt": "Take π as 3.14. A semicircle (half circle) has radius %d cm. "
                          "What is its area, in cm²? (area = ½ × π × r²)" % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": a, "answer_type": "num", "tolerance": 0.05,
                "solution": ["Full circle area = 3.14 × %d² = %s cm²."
                             % (rr, _f(round(3.14 * rr * rr, 2))),
                             "Half of that is %s cm²." % _f(a)]}

    if t == 6:                                        # diameter from circumference (3.14)
        dia = 2 * rr
        c = round(3.14 * dia, 2)
        return {"prompt": "Take π as 3.14. This circle has a circumference of about %s "
                          "cm. Work out its diameter, in cm. (d = C ÷ π)" % _f(c),
                "component": "circle",
                "spec": {"radius": rr, "show": "circumference",
                         "label": "C = %s cm" % _f(c)},
                "answer": dia, "answer_type": "num", "tolerance": 0.1,
                "solution": ["d = C ÷ π = %s ÷ 3.14." % _f(c),
                             "= %d cm." % dia]}

    # quarter circle area in terms of pi coefficient
    return {"prompt": "Leave your answer in terms of π. A quarter circle has radius %d "
                      "cm. Its area is kπ cm² where the area is ¼ × π × r². What is k? "
                      "(give a fraction or decimal)" % rr,
            "component": "circle",
            "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
            "answer": str(Fraction(rr * rr, 4)), "answer_type": "frac",
            "solution": ["Area = ¼ × π × %d² = %dπ ÷ 4." % (rr, rr * rr),
                         "So k = %d/4." % (rr * rr)]}


@skill("Y8.9.e", "Perimeter and area of compound shapes", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 5, 3, 3])

    if t == 9:                                         # triangle + semicircle compound area
        b = random.randint(6, 14)
        h = random.randint(4, 12)
        while (b * h) % 2:
            h += 1
        r = random.randint(2, 6)
        tri = b * h // 2
        semi = round(3.14 * r * r / 2.0, 2)
        total = round(tri + semi, 2)
        return _num_q("A compound figure is made of a triangle joined to a semicircle. "
                      "The triangle has base %d cm and perpendicular height %d cm. The "
                      "semicircle has radius %d cm. Taking π as 3.14, work out the total "
                      "area of the compound figure, in cm². Give your answer to 2 decimal "
                      "places." % (b, h, r), total, "num", tolerance=0.05, unit="cm²",
                      solution=["Triangle = ½ × %d × %d = %d cm²." % (b, h, tri),
                                "Semicircle = ½ × 3.14 × %d² = %s cm²." % (r, _f(semi)),
                                "%d + %s = %s cm²." % (tri, _f(semi), _f(total))])

    if t == 10:                                        # rectangle + quarter circle compound
        L = random.randint(5, 12)
        Wd = random.randint(3, 8)
        r = random.randint(2, 6)
        rect = L * Wd
        quarter = _half_up(Fraction(314 * r * r, 400), 2)
        total = round(rect + quarter, 2)
        return _num_q("A compound figure is made of a rectangle with a quarter circle "
                      "attached to one corner. The rectangle measures %d cm by %d cm and "
                      "the quarter circle has radius %d cm. Taking π as 3.14, work out "
                      "the total area, in cm². Give your answer to 2 decimal places."
                      % (L, Wd, r), total, "num", tolerance=0.05, unit="cm²",
                      solution=["Rectangle = %d × %d = %d cm²." % (L, Wd, rect),
                                "Quarter circle = ¼ × 3.14 × %d² = %s cm²."
                                % (r, _f(quarter)),
                                "%d + %s = %s cm²." % (rect, _f(quarter), _f(total))])

    if t == 8:                                        # two-rectangle area from a table (visual)
        a1, b1 = random.randint(3, 12), random.randint(3, 9)
        a2, b2 = random.randint(3, 12), random.randint(3, 9)
        area = a1 * b1 + a2 * b2
        return _measure_table("A compound shape is made of two rectangles. The table "
                              "gives their sides. Work out the total area, in cm².",
                              "Two rectangles",
                              ["Rect 1 length", "Rect 1 width", "Rect 2 length",
                               "Rect 2 width"], [a1, b1, a2, b2], area,
                              ["%d × %d = %d and %d × %d = %d."
                               % (a1, b1, a1 * b1, a2, b2, a2 * b2),
                               "%d + %d = %d cm²." % (a1 * b1, a2 * b2, area)])

    if t == 0:                                        # L-shape area (rectangle minus corner)
        W = random.randint(_by_d(d, 6, 8, 10), _by_d(d, 12, 16, 22))
        H = random.randint(_by_d(d, 5, 6, 8), _by_d(d, 10, 14, 18))
        w = random.randint(2, W - 3)
        h = random.randint(2, H - 3)
        area = W * H - w * h
        return _num_q("An L-shape is %s cm by %d cm rectangle with %s cm by %d cm "
                      "rectangle cut out of one corner. What is the area of the L-shape, "
                      "in cm²?" % (_an(W), H, _an(w), h), area, "int", unit="cm²",
                      solution=["Big rectangle = %d × %d = %d cm²." % (W, H, W * H),
                                "Cut-out = %d × %d = %d cm²." % (w, h, w * h),
                                "%d − %d = %d cm²." % (W * H, w * h, area)])

    if t == 1:                                        # L-shape perimeter (unchanged)
        W = random.randint(8, 20)
        H = random.randint(6, 16)
        return _num_q("An L-shape is made by cutting a small rectangle out of one corner "
                      "of %s cm by %d cm rectangle. The perimeter of an L-shape like "
                      "this equals the perimeter of the whole rectangle. What is the "
                      "perimeter, in cm?" % (_an(W), H), 2 * (W + H), "int", unit="cm",
                      solution=["Perimeter = 2 × (%d + %d)." % (W, H),
                                "= %d cm." % (2 * (W + H))])

    if t == 2:                                        # two rectangles joined - area
        a1, b1 = random.randint(3, 10), random.randint(3, 8)
        a2, b2 = random.randint(3, 10), random.randint(3, 8)
        area = a1 * b1 + a2 * b2
        return _num_q("A compound shape is made of two rectangles: one %d cm by %d cm "
                      "and one %d cm by %d cm. What is the total area, in cm²?"
                      % (a1, b1, a2, b2), area, "int", unit="cm²",
                      solution=["%d × %d = %d and %d × %d = %d."
                                % (a1, b1, a1 * b1, a2, b2, a2 * b2),
                                "%d + %d = %d cm²." % (a1 * b1, a2 * b2, area)])

    if t == 3:                                        # rectangle + square area
        L = random.randint(6, 14)
        Wd = random.randint(3, 8)
        s = random.randint(2, 6)
        area = L * Wd + s * s
        return _num_q("A shape is %s cm by %d cm rectangle with %s cm square attached "
                      "to one side. What is the total area, in cm²?" % (_an(L), Wd, _an(s)),
                      area, "int", unit="cm²",
                      solution=["Rectangle = %d × %d = %d cm²." % (L, Wd, L * Wd),
                                "Square = %d × %d = %d cm²." % (s, s, s * s),
                                "%d + %d = %d cm²." % (L * Wd, s * s, area)])

    if t == 4:                                        # border / frame area
        W = random.randint(8, 16)
        H = random.randint(6, 14)
        m = random.randint(1, min(3, (min(W, H) - 2) // 2))
        outer = W * H
        inner = (W - 2 * m) * (H - 2 * m)
        return _num_q("A photo frame is %s cm by %d cm rectangle with a rectangular "
                      "hole cut out, leaving a border %d cm wide all the way round. "
                      "What is the area of the border (the frame), in cm²?" % (_an(W), H, m),
                      outer - inner, "int", unit="cm²",
                      solution=["Outer area = %d × %d = %d cm²." % (W, H, outer),
                                "Inner hole = %d × %d = %d cm²."
                                % (W - 2 * m, H - 2 * m, inner),
                                "%d − %d = %d cm²." % (outer, inner, outer - inner)])

    if t == 5:                                        # missing length in an L-shape
        W = random.randint(8, 16)
        a = random.randint(2, W - 3)
        b = W - a
        return _num_q("Along the top of an L-shape, the full width is %d cm. One part of "
                      "the top edge is %d cm. How long is the remaining part of that "
                      "edge, in cm?" % (W, a), b, "int", unit="cm",
                      solution=["The two parts add up to the full width.",
                                "%d − %d = %d cm." % (W, a, b)])

    if t == 6:                                        # rectangle with square hole - area
        W = random.randint(8, 16)
        H = random.randint(8, 16)
        s = random.randint(2, min(W, H) - 3)
        area = W * H - s * s
        return _num_q("%s cm by %d cm rectangular sheet has %s cm square hole cut out "
                      "of the middle. What area of sheet is left, in cm²?"
                      % (_an(W).capitalize(), H, _an(s)),
                      area, "int", unit="cm²",
                      solution=["Sheet = %d × %d = %d cm²." % (W, H, W * H),
                                "Hole = %d × %d = %d cm²." % (s, s, s * s),
                                "%d − %d = %d cm²." % (W * H, s * s, area)])

    # T-shape / cross area from two rectangles, word problem
    who = pick(NAMES)
    a1, b1 = random.randint(6, 12), random.randint(2, 4)
    a2, b2 = random.randint(2, 4), random.randint(4, 8)
    area = a1 * b1 + a2 * b2
    return _num_q("%s makes a T-shape from %s cm by %d cm bar and %s cm by %d cm bar. "
                  "What is the total area, in cm²?" % (who, _an(a1), b1, _an(a2), b2), area, "int",
                  unit="cm²",
                  solution=["%d × %d = %d and %d × %d = %d."
                            % (a1, b1, a1 * b1, a2, b2, a2 * b2),
                            "%d + %d = %d cm²." % (a1 * b1, a2 * b2, area)])


@skill("Y8.9.f", "Volume of cubes, cuboids and prisms", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 5, 4])

    if t == 9:                                         # volume of a compound solid
        l1, w1, h1 = (random.randint(3, 10), random.randint(2, 6),
                      random.randint(2, 6))
        l2, w2, h2 = (random.randint(2, 6), random.randint(2, 6),
                      random.randint(2, 6))
        v1 = l1 * w1 * h1
        v2 = l2 * w2 * h2
        total = v1 + v2
        return _num_q("A compound solid is made of two cuboids joined together. One "
                      "cuboid measures %d cm by %d cm by %d cm and the other measures "
                      "%d cm by %d cm by %d cm. What is the total volume of the compound "
                      "solid, in cm³?" % (l1, w1, h1, l2, w2, h2), total, "int",
                      unit="cm³",
                      solution=["First cuboid = %d × %d × %d = %d cm³."
                                % (l1, w1, h1, v1),
                                "Second cuboid = %d × %d × %d = %d cm³."
                                % (l2, w2, h2, v2),
                                "%d + %d = %d cm³." % (v1, v2, total)])

    if t == 8:                                        # cuboid volume from a table (visual)
        l = random.randint(2, 15)
        w = random.randint(2, 12)
        h = random.randint(2, 12)
        return _measure_table("The table gives the length, width and height of a cuboid. "
                              "Work out its volume, in cm³. "
                              "(Volume = length × width × height.)", "Cuboid",
                              ["Length (cm)", "Width (cm)", "Height (cm)"], [l, w, h],
                              l * w * h,
                              ["V = %d × %d × %d = %d cm³." % (l, w, h, l * w * h)])

    if t == 0:                                        # cuboid volume
        l = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 8, 12, 18))
        w = random.randint(2, _by_d(d, 7, 10, 14))
        h = random.randint(2, _by_d(d, 7, 10, 14))
        return _num_q("A cuboid measures %d cm by %d cm by %d cm. "
                      "Volume = length × width × height. What is its volume, in cm³?"
                      % (l, w, h), l * w * h, "int", unit="cm³",
                      solution=["V = %d × %d × %d." % (l, w, h),
                                "= %d cm³." % (l * w * h)])

    if t == 1:                                        # cube volume
        s = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 7, 10, 13))
        return _num_q("A cube has edges of %d cm. What is its volume, in cm³?" % s,
                      s ** 3, "int", unit="cm³",
                      solution=["V = %d × %d × %d." % (s, s, s), "= %d cm³." % (s ** 3)])

    if t == 2:                                        # prism from cross-section
        A = random.randint(_by_d(d, 6, 10, 12), _by_d(d, 20, 40, 60))
        L = random.randint(3, _by_d(d, 10, 15, 20))
        return _num_q("A prism has a cross-section of area %d cm² and a length of %d cm. "
                      "Volume = cross-section area × length. What is its volume, in cm³?"
                      % (A, L), A * L, "int", unit="cm³",
                      solution=["V = %d × %d." % (A, L), "= %d cm³." % (A * L)])

    if t == 3:                                        # triangular prism volume
        base = random.randint(3, 12)
        h = random.randint(2, 10)
        while (base * h) % 2:
            h += 1
        L = random.randint(4, 15)
        cross = base * h // 2
        return _num_q("A triangular prism has a triangular cross-section with base %d cm "
                      "and height %d cm, and a length of %d cm. What is its volume, in "
                      "cm³? (cross-section = ½ × base × height)" % (base, h, L),
                      cross * L, "int", unit="cm³",
                      solution=["Cross-section = ½ × %d × %d = %d cm²."
                                % (base, h, cross),
                                "V = %d × %d = %d cm³." % (cross, L, cross * L)])

    if t == 4:                                        # inverse: cuboid missing edge
        l = random.randint(2, 10)
        w = random.randint(2, 10)
        h = random.randint(2, 10)
        V = l * w * h
        return _num_q("A cuboid has volume %d cm³. Its base measures %d cm by %d cm. "
                      "How tall is it, in cm?" % (V, l, w), h, "int", unit="cm",
                      solution=["height = volume ÷ (length × width).",
                                "%d ÷ (%d × %d) = %d ÷ %d = %d cm."
                                % (V, l, w, V, l * w, h)])

    if t == 5:                                        # cube edge from volume
        s = pick([2, 3, 4, 5, 6, 7, 8, 9, 10])
        return _num_q("A cube has volume %d cm³. How long is each edge, in cm?" % (s ** 3),
                      s, "int", unit="cm",
                      solution=["Edge = cube root of the volume.",
                                "The cube root of %d is %d cm." % (s ** 3, s)])

    if t == 6:                                        # capacity litres word problem
        l = random.randint(10, 40)
        w = random.randint(10, 40)
        h = random.randint(10, 40)
        V = l * w * h
        return _num_q("A tank measures %d cm by %d cm by %d cm. How many litres of water "
                      "does it hold when full? (1 litre = 1000 cm³)" % (l, w, h),
                      V / 1000.0, "num", unit="litres", tolerance=0.0005,
                      solution=["Volume = %d × %d × %d = %d cm³." % (l, w, h, V),
                                "%d ÷ 1000 = %s litres." % (V, _f(V / 1000.0))])

    # stacking cubes word problem
    s = random.randint(2, 5)
    n = random.randint(3, 8)
    return _num_q("%d identical cubes, each of edge %d cm, are stacked together. "
                  "What is the total volume, in cm³?" % (n, s), n * s ** 3, "int",
                  unit="cm³",
                  solution=["Each cube = %d³ = %d cm³." % (s, s ** 3),
                            "%d × %d = %d cm³." % (n, s ** 3, n * s ** 3)])


@skill("Y8.9.g", "Volume of cylinders; surface area of prisms and cylinders", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 1, 1, 5])
    rr = random.randint(_by_d(d, 2, 3, 3), _by_d(d, 6, 8, 12))
    hh = random.randint(_by_d(d, 3, 4, 5), _by_d(d, 10, 14, 20))

    if t == 8:                                        # cuboid surface area from a table (visual)
        l = random.randint(2, 10)
        w = random.randint(2, 10)
        h = random.randint(2, 10)
        SA = 2 * (l * w + l * h + w * h)
        return _measure_table("The table gives the dimensions of a cuboid. Work out its "
                              "total surface area, in cm². (SA = 2(lw + lh + wh).)",
                              "Cuboid", ["Length (cm)", "Width (cm)", "Height (cm)"],
                              [l, w, h], SA,
                              ["lw + lh + wh = %d + %d + %d = %d."
                               % (l * w, l * h, w * h, l * w + l * h + w * h),
                               "2 × %d = %d cm²." % (l * w + l * h + w * h, SA)])

    if t == 0:                                        # cylinder volume (3.14)
        V = round(3.14 * rr * rr * hh, 2)
        return _num_q("Take π as 3.14. A cylinder has radius %d cm and height %d cm. "
                      "What is its volume, in cm³? (V = π × r² × h)" % (rr, hh),
                      V, "num", tolerance=0.5, unit="cm³",
                      solution=["V = 3.14 × %d² × %d = 3.14 × %d × %d."
                                % (rr, hh, rr * rr, hh),
                                "= %s cm³." % _f(V)])

    if t == 1:                                        # cylinder volume in terms of pi (coeff)
        return _num_q("Leave your answer in terms of π. A cylinder has radius %d cm and "
                      "height %d cm, so its volume is kπ cm³ where V = πr²h. "
                      "What is the value of k?" % (rr, hh), rr * rr * hh, "int",
                      solution=["V = π × %d² × %d = %dπ." % (rr, hh, rr * rr * hh),
                                "So k = %d." % (rr * rr * hh)])

    if t == 2:                                        # cuboid surface area
        l = random.randint(2, 9)
        w = random.randint(2, 9)
        h = random.randint(2, 9)
        SA = 2 * (l * w + l * h + w * h)
        return _num_q("A cuboid measures %d cm by %d cm by %d cm. Surface area = "
                      "2(lw + lh + wh). What is its total surface area, in cm²?"
                      % (l, w, h), SA, "int", unit="cm²",
                      solution=["lw + lh + wh = %d + %d + %d = %d."
                                % (l * w, l * h, w * h, l * w + l * h + w * h),
                                "2 × %d = %d cm²." % (l * w + l * h + w * h, SA)])

    if t == 3:                                        # cube surface area
        s = random.randint(2, 12)
        return _num_q("A cube has edges of %d cm. Surface area = 6 × (edge)². "
                      "What is its surface area, in cm²?" % s, 6 * s * s, "int",
                      unit="cm²",
                      solution=["One face = %d × %d = %d cm²." % (s, s, s * s),
                                "6 × %d = %d cm²." % (s * s, 6 * s * s)])

    if t == 4:                                        # cylinder curved surface area (terms of pi)
        return _num_q("Leave your answer in terms of π. The curved surface of a cylinder "
                      "has area 2πrh. For radius %d cm and height %d cm this is kπ cm². "
                      "What is the value of k?" % (rr, hh), 2 * rr * hh, "int",
                      solution=["Curved surface = 2 × π × %d × %d = %dπ."
                                % (rr, hh, 2 * rr * hh),
                                "So k = %d." % (2 * rr * hh)])

    if t == 5:                                        # triangular prism surface area
        a = 3
        b = 4
        c = 5
        L = random.randint(5, 15)
        # right triangle 3-4-5 cross-section, area 6
        cross = 6
        SA = 2 * cross + (a + b + c) * L
        return _num_q("A triangular prism has a right-angled triangular cross-section "
                      "with sides 3 cm, 4 cm and 5 cm (area 6 cm²) and length %d cm. "
                      "Surface area = 2 × cross-section + perimeter × length. "
                      "What is the total surface area, in cm²?" % L, SA, "int",
                      unit="cm²",
                      solution=["Two triangular ends = 2 × 6 = 12 cm².",
                                "Three rectangles = (3 + 4 + 5) × %d = %d cm²."
                                % (L, 12 * L),
                                "12 + %d = %d cm²." % (12 * L, SA)])

    if t == 6:                                        # cylinder total SA in terms of pi
        # 2πr(r+h) = coeff = 2r(r+h)
        coeff = 2 * rr * (rr + hh)
        return _num_q("Leave your answer in terms of π. The TOTAL surface area of a "
                      "cylinder is 2πr(r + h). For radius %d cm and height %d cm this is "
                      "kπ cm². What is the value of k?" % (rr, hh), coeff, "int",
                      solution=["k = 2 × r × (r + h) = 2 × %d × (%d + %d)."
                                % (rr, rr, hh),
                                "= 2 × %d × %d = %d." % (rr, rr + hh, coeff)])

    # cylinder volume word problem (3.14)
    V = round(3.14 * rr * rr * hh, 2)
    return _num_q("Take π as 3.14. A cylindrical can has radius %d cm and height %d cm. "
                  "How much does it hold, in cm³? (V = π × r² × h)" % (rr, hh), V, "num",
                  tolerance=0.5, unit="cm³",
                  solution=["V = 3.14 × %d² × %d." % (rr, hh),
                            "= %s cm³." % _f(V)])


_CHART8 = [
    ("Favourite sport", ["Football", "Netball", "Tennis", "Cricket"], "students"),
    ("Books read this week", ["Mon", "Tue", "Wed", "Thu"], "books"),
    ("How students travel to school", ["Walk", "Bus", "Car", "Cycle"], "students"),
    ("Goals scored", ["Team A", "Team B", "Team C", "Team D"], "goals"),
]


def _distinct(count, lo, hi):
    hi = max(hi, lo + count)
    return random.sample(range(lo, hi + 1), count)


@skill("Y8.9.h", "Interpret and construct tables, bar charts, pictograms and line graphs",
       S9)
def _(d=1):
    d = _tier(d)
    title, cats, unit = pick(_CHART8)
    n = len(cats)
    lo, hi = _by_d(d, (4, 20), (6, 40), (8, 90))
    vals = _distinct(n, lo, hi)
    i, j = random.sample(range(n), 2)
    t = _pick_t([2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1])

    if t == 9:                                         # create bar graph: categorical data
        scale = pick([2, 5, 10])
        v = vals[i]
        return _num_q("%s. This is categorical data. To create a bar graph, each square "
                      "on the vertical axis is worth %d %s. The category '%s' has a value "
                      "of %d %s. How many squares tall should its bar be?"
                      % (title, scale, unit, cats[i], v * scale, unit), v, "int",
                      unit="squares",
                      solution=["Each square stands for %d." % scale,
                                "%d ÷ %d = %s." % (v * scale, scale, _pl(v, "square"))])

    if t == 10:                                        # create bar graph: grouped data
        groups = ["1–5", "6–10", "11–15", "16–20"]
        sq = random.sample(range(1, 9), 4)
        scale = pick([2, 5, 10])
        gi = random.randrange(4)
        count = sq[gi] * scale
        return _num_q("Some data is sorted into equal grouped class intervals. To create "
                      "a bar graph for this grouped data, each square on the axis is worth "
                      "%d. The class interval %s has a frequency of %d. How many squares "
                      "tall should that bar be?" % (scale, groups[gi], count), sq[gi],
                      "int", unit="squares",
                      solution=["Each square stands for %d." % scale,
                                "%d ÷ %d = %s." % (count, scale, _pl(sq[gi], "square"))])

    if t == 0:                                        # read one bar
        spec = {"categories": cats, "values": vals, "mode": "read"}
        return {"prompt": "%s. Use the bar chart. How many %s are shown for %s?"
                          % (title, unit, cats[i]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["The %s bar reaches %d." % (cats[i], vals[i])]}

    if t == 1:                                        # difference between two bars
        spec = {"categories": cats, "values": vals, "mode": "read"}
        return {"prompt": "%s. Use the bar chart. What is the difference between %s and "
                          "%s?" % (title, cats[i], cats[j]),
                "component": "bar_chart", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (cats[i], vals[i], cats[j], vals[j]),
                             "%d − %d = %d." % (max(vals[i], vals[j]),
                                                min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 2:                                        # total of the bars
        spec = {"categories": cats, "values": vals, "mode": "read"}
        return {"prompt": "%s. Use the bar chart. What is the total of all the bars?"
                          % title,
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(v) for v in vals), sum(vals))]}

    if t == 3:                                        # tallest / shortest (typed)
        spec = {"categories": cats, "values": vals, "mode": "read"}
        want_top = random.random() < 0.5
        which = cats[vals.index(max(vals) if want_top else min(vals))]
        return {"prompt": "%s. Use the bar chart. Which category is the %s? "
                          "(type the label)"
                          % (title, "LARGEST" if want_top else "SMALLEST"),
                "component": "bar_chart", "spec": spec,
                "answer": which, "answer_type": "str",
                "solution": ["The %s bar is %s with %d."
                             % ("tallest" if want_top else "shortest", which,
                                max(vals) if want_top else min(vals))]}

    if t == 4:                                        # frequency table with a gap
        total = sum(vals)
        rows = [[c, str(v)] for c, v in zip(cats, vals)]
        k = random.randrange(n)
        blank = [list(r) for r in rows]
        blank[k][1] = "?"
        return {"prompt": "%s. The frequencies in this table add up to %d. What number "
                          "belongs in the cell marked ?" % (title, total),
                "component": "data_table",
                "spec": {"caption": title, "headers": ["Category", "Frequency"],
                         "rows": blank, "missing": [k, 1]},
                "answer": vals[k], "answer_type": "int",
                "solution": ["The other rows add up to %d." % (total - vals[k]),
                             "%d − %d = %d." % (total, total - vals[k], vals[k])]}

    if t == 5:                                        # pictogram read
        key = pick([2, 5, 10])
        pv = [key * random.randint(1, 6) for _ in range(n)]
        spec = {"categories": cats, "values": pv, "key": key, "symbol": "●"}
        return {"prompt": "%s. Use the pictogram, where each symbol stands for %d %s. "
                          "How many %s are shown for %s?"
                          % (title, key, unit, unit, cats[i]),
                "component": "pictogram", "spec": spec,
                "answer": pv[i], "answer_type": "int",
                "solution": ["Each symbol is %d %s and %s has %s."
                             % (key, unit, cats[i], _pl(pv[i] // key, "symbol")),
                             "%d × %d = %d." % (pv[i] // key, key, pv[i])]}

    if t == 6:                                        # pictogram: count symbols
        key = pick([2, 5, 10])
        pv = [key * random.randint(1, 6) for _ in range(n)]
        spec = {"categories": cats, "values": pv, "key": key, "symbol": "●"}
        return {"prompt": "%s. In a pictogram each symbol stands for %d %s. How many "
                          "symbols are needed to show %s, which has a value of %d?"
                          % (title, key, unit, cats[i], pv[i]),
                "component": "pictogram", "spec": spec,
                "answer": pv[i] // key, "answer_type": "int",
                "solution": ["%d ÷ %d = %s." % (pv[i], key, _pl(pv[i] // key, "symbol"))]}

    if t == 7:                                        # line graph read
        labels = ["9 am", "10 am", "11 am", "12 pm", "1 pm"][:5]
        lvals = sorted(random.sample(range(5, 40), 5))
        if random.random() < 0.4:
            random.shuffle(lvals)
        pts = [[lab, v] for lab, v in zip(labels, lvals)]
        k = random.randrange(5)
        return {"prompt": "Temperature during the morning. Use the line graph. What is "
                          "the reading at %s, in °C?" % labels[k],
                "component": "line_graph",
                "spec": {"points": pts, "yLabel": "°C", "xLabel": "Time"},
                "answer": lvals[k], "answer_type": "int",
                "solution": ["Find %s along the bottom and read up to the line."
                             % labels[k],
                             "The reading is %d °C." % lvals[k]]}

    # construct: bar height in squares
    scale = pick([2, 5, 10])
    v = vals[i]
    return _num_q("%s. A bar chart is drawn with each square worth %d %s. %s has a value "
                  "of %d. How many squares tall should the %s bar be?"
                  % (title, scale, unit, cats[i], v * scale, cats[i]),
                  v, "int", unit="squares",
                  solution=["Each square is worth %d." % scale,
                            "%d ÷ %d = %s." % (v * scale, scale, _pl(v, "square"))])


@skill("Y8.9.i", "Stem-and-leaf diagrams and line plots", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 2, 1])
    stems = sorted(random.sample(range(1, 9), _by_d(d, 3, 3, 4)))
    leaves = [sorted(random.sample(range(0, 10), random.randint(2, 4))) for _ in stems]
    values = sorted([s * 10 + lf for s, lvs in zip(stems, leaves) for lf in lvs])
    rows = [[str(s), " ".join(str(lf) for lf in lvs)]
            for s, lvs in zip(stems, leaves)]
    cap = "Stem-and-leaf (%d | %d means %d)" % (stems[0], leaves[0][0], values[0])

    def _table(q, ans, atype="int", sol=None):
        return {"prompt": "%s (In this stem-and-leaf diagram the stem is the tens digit "
                          "and each leaf is a units digit.)" % q,
                "component": "data_table",
                "spec": {"caption": cap, "headers": ["Stem", "Leaves"], "rows": rows},
                "answer": ans, "answer_type": atype,
                "solution": sol or ["The values are %s."
                                    % ", ".join(str(v) for v in values),
                                    "The answer is %s." % ans]}

    if t == 6:                                        # largest value on a stem row
        k = random.randrange(len(stems))
        big = stems[k] * 10 + leaves[k][-1]
        return _table("What is the largest value on the row with stem %d?" % stems[k],
                      big, sol=["The largest leaf on the stem-%d row is %d."
                                % (stems[k], leaves[k][-1]),
                                "So the value is %d." % big])

    if t == 0:                                        # count all
        return _table("How many values are shown altogether?", len(values))

    if t == 1:                                        # range
        return _table("What is the range (largest − smallest) of the values?",
                      values[-1] - values[0],
                      sol=["Largest = %d, smallest = %d." % (values[-1], values[0]),
                           "%d − %d = %d." % (values[-1], values[0],
                                              values[-1] - values[0])])

    if t == 2:                                        # largest
        return _table("What is the largest value shown?", values[-1])

    if t == 3:                                        # smallest
        return _table("What is the smallest value shown?", values[0])

    if t == 4:                                        # median
        m = values[len(values) // 2] if len(values) % 2 else \
            (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2.0
        if isinstance(m, float) and m == int(m):
            m = int(m)
        return _table("What is the median (middle value) of the data?", m,
                      atype="num" if isinstance(m, float) else "int",
                      sol=["In order: %s." % ", ".join(str(v) for v in values),
                           "The median is %s." % _f(m)])

    if t == 5:                                        # count on a stem row
        k = random.randrange(len(stems))
        return _table("How many values are on the row with stem %d?" % stems[k],
                      len(leaves[k]),
                      sol=["Count the leaves on the stem-%d row." % stems[k],
                           "There are %d." % len(leaves[k])])

    # create: how many leaves on a stem, from a list
    k = random.randrange(len(stems))
    shown = list(values)
    random.shuffle(shown)
    return _num_q("A stem-and-leaf diagram is being made for these values: %s. The stem "
                  "is the tens digit and each leaf a units digit. How many leaves will "
                  "be on the row with stem %d?" % (", ".join(str(v) for v in shown),
                                                   stems[k]),
                  len(leaves[k]), "int", unit="leaves",
                  solution=["The values in the %ds are %s."
                            % (stems[k] * 10,
                               ", ".join(str(stems[k] * 10 + lf) for lf in leaves[k])),
                            "That row has %d leaves." % len(leaves[k])])


_PIE8 = [
    ("how %d students travel to school", ["Walk", "Bus", "Car", "Cycle"], "students"),
    ("the favourite fruit of %d children", ["Apple", "Banana", "Grape", "Pear"],
     "children"),
    ("how %d people voted", ["Red", "Blue", "Green", "Yellow"], "people"),
    ("how %d minutes of lessons were spent", ["Reading", "Writing", "Talking",
                                              "Testing"], "minutes"),
]


def _pie_parts(total):
    """Split total into 4 positive parts whose sector angles are whole degrees."""
    # choose parts so each part * (360/total) is an integer -> total divides 360*part;
    # simplest: pick totals that divide 360, then any parts work.
    while True:
        cuts = sorted(random.sample(range(1, total), 3))
        parts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2]]
        if all(p >= 2 for p in parts) and len(set(parts)) == 4:
            return parts


@skill("Y8.9.j", "Pie charts using central angles", S9)
def _(d=1):
    d = _tier(d)
    topic, cats, who = pick(_PIE8)
    total = pick([36, 40, 60, 72, 90, 120])          # all divide 360
    topic = topic % total
    one = {"students": "student", "children": "child", "people": "person",
           "minutes": "minute"}[who]
    unit = 360 // total
    parts = _pie_parts(total)
    slices = [[c, p] for c, p in zip(cats, parts)]
    i = random.randrange(4)
    ang = parts[i] * unit
    t = _pick_t([3, 3, 2, 2, 2, 1, 1, 1])

    if t == 0:                                        # angle of a sector (visual)
        return {"prompt": "This pie chart shows %s. The %s sector is outlined. "
                          "How many degrees is its angle?" % (topic, cats[i]),
                "component": "pie_chart", "spec": {"slices": slices, "highlight": i},
                "answer": ang, "answer_type": "int",
                "solution": ["The whole pie is %d %s, and 360 ÷ %d = %d° each."
                             % (total, who, total, unit),
                             "%d × %d = %d°." % (parts[i], unit, ang)]}

    if t == 1:                                        # count from an angle (visual)
        return {"prompt": "This pie chart shows %s. The outlined sector has an angle of "
                          "%d°. How many %s does it stand for?" % (topic, ang, who),
                "component": "pie_chart",
                "spec": {"slices": slices, "highlight": i, "showAngles": True},
                "answer": parts[i], "answer_type": "int",
                "solution": ["Each %s is 360 ÷ %d = %d°." % (one, total, unit),
                             "%d ÷ %d = %d %s." % (ang, unit, parts[i], who)]}

    if t == 2:                                        # largest / smallest (visual)
        want_big = random.random() < 0.5
        which = cats[parts.index(max(parts) if want_big else min(parts))]
        return {"prompt": "This pie chart shows %s. Which sector is the %s? "
                          "(type the label)"
                          % (topic, "LARGEST" if want_big else "SMALLEST"),
                "component": "pie_chart", "spec": {"slices": slices},
                "answer": which, "answer_type": "str",
                "solution": ["The %s sector is %s (%d %s)."
                             % ("largest" if want_big else "smallest", which,
                                max(parts) if want_big else min(parts), who)]}

    if t == 3:                                        # fraction of the pie (visual)
        fr = Fraction(parts[i], total)
        return {"prompt": "This pie chart shows %s. What fraction of the whole pie is the "
                          "outlined sector? Give your answer as a fraction." % topic,
                "component": "pie_chart", "spec": {"slices": slices, "highlight": i},
                "answer": "%d/%d" % (fr.numerator, fr.denominator), "answer_type": "frac",
                "solution": ["The sector is %d out of %d %s." % (parts[i], total, who),
                             "%d/%d = %d/%d." % (parts[i], total, fr.numerator,
                                                 fr.denominator)]}

    if t == 4:                                        # bare: angle from a share
        share = random.randint(2, total - 1)
        return _num_q("On a pie chart of %d %s, one category has %d %s. How many degrees "
                      "is its sector angle?" % (total, who, share, who),
                      unit * share, "int", unit="degrees",
                      solution=["Each %s is 360 ÷ %d = %d°." % (one, total, unit),
                                "%d × %d = %d°." % (share, unit, unit * share)])

    if t == 5:                                        # percentage -> angle
        pct = pick([10, 20, 25, 40, 50, 75])
        return _num_q("A sector is %d%% of a pie chart. How many degrees is its angle?"
                      % pct, 360 * pct // 100, "int", unit="degrees",
                      solution=["The whole pie is 360° and 1% is 3.6°.",
                                "%d × 3.6 = %d°." % (pct, 360 * pct // 100)])

    if t == 6:                                        # remaining sector
        used = random.sample([30, 45, 60, 75, 90, 100, 120], 3)
        while sum(used) >= 350:
            used = random.sample([30, 45, 60, 75, 90], 3)
        return _num_q("A pie chart has four sectors. Three have angles %s. How many "
                      "degrees is the fourth?" % ", ".join("%d°" % u for u in used),
                      360 - sum(used), "int", unit="degrees",
                      solution=["%s = %d°." % (" + ".join(str(u) for u in used),
                                               sum(used)),
                                "360 − %d = %d°." % (sum(used), 360 - sum(used))])

    # inverse: total from a sector
    each = pick([2, 3, 4, 5, 6, 8, 9, 10, 12])
    n_tot = 360 // each
    share = random.randint(2, n_tot - 1)
    return _num_q("On a pie chart, a sector of %d° stands for %d %s. How many %s are in "
                  "the whole survey?" % (share * each, share, who, who),
                  n_tot, "int", unit=who,
                  solution=["%d° ÷ %d %s = %d° each." % (share * each, share, who, each),
                            "360 ÷ %d = %d %s." % (each, n_tot, who)])


@skill("Y8.9.k", "Mean, median, mode and range", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 2, 1, 1, 1])
    n = _by_d(d, 5, 6, 8)

    if t == 0:                                        # mean of a list
        # choose values with an integer mean
        vals = [random.randint(1, 20) for _ in range(n)]
        while sum(vals) % n:
            vals = [random.randint(1, 20) for _ in range(n)]
        return _data_list("Work out the MEAN of the values in this table.", vals,
                          sum(vals) // n, "Scores",
                          ["Add them: %d." % sum(vals),
                           "%d ÷ %d = %d." % (sum(vals), n, sum(vals) // n)])

    if t == 1:                                        # range
        vals = [random.randint(1, 40) for _ in range(n)]
        return _data_list("Work out the RANGE of the values in this table.", vals,
                          max(vals) - min(vals), "Scores",
                          ["Largest = %d, smallest = %d." % (max(vals), min(vals)),
                           "%d − %d = %d." % (max(vals), min(vals),
                                              max(vals) - min(vals))])

    if t == 2:                                        # median (odd count)
        m = n if n % 2 else n + 1
        vals = random.sample(range(1, 40), m)
        s = sorted(vals)
        med = s[m // 2]
        return _data_list("Work out the MEDIAN (middle value) of the data in this table.",
                          vals, med, "Scores",
                          ["In order: %s." % ", ".join(str(v) for v in s),
                           "The middle value is %d." % med])

    if t == 3:                                        # mode
        base = random.sample(range(1, 20), n - 1)
        rep = pick(base)
        vals = base + [rep]
        random.shuffle(vals)
        return _data_list("Work out the MODE (most common value) of the data in this "
                          "table.", vals, rep, "Scores",
                          ["%d appears most often." % rep, "The mode is %d." % rep])

    if t == 4:                                        # missing value for a target mean
        mean = random.randint(5, 15)
        others = [random.randint(1, 20) for _ in range(n - 1)]
        missing = mean * n - sum(others)
        while missing < 1 or missing > 30:
            others = [random.randint(1, 20) for _ in range(n - 1)]
            missing = mean * n - sum(others)
        return _num_q("There are %d numbers with a mean of %d. %d of them are %s. "
                      "What is the missing number?"
                      % (n, mean, n - 1, ", ".join(str(v) for v in others)),
                      missing, "int",
                      solution=["The total must be %d × %d = %d." % (n, mean, mean * n),
                                "%d − %d = %d." % (mean * n, sum(others), missing)])

    if t == 5:                                        # mean from a frequency table
        cats = [1, 2, 3, 4]
        freqs = [random.randint(1, 6) for _ in cats]
        total_items = sum(freqs)
        total_sum = sum(c * f for c, f in zip(cats, freqs))
        while total_sum % total_items:
            freqs = [random.randint(1, 6) for _ in cats]
            total_items = sum(freqs)
            total_sum = sum(c * f for c, f in zip(cats, freqs))
        rows = [[str(c), str(f)] for c, f in zip(cats, freqs)]
        return {"prompt": "This frequency table shows how many pets each of several "
                          "students owns. Work out the MEAN number of pets per student.",
                "component": "data_table",
                "spec": {"caption": "Pets owned", "headers": ["Pets", "Frequency"],
                         "rows": rows},
                "answer": total_sum // total_items, "answer_type": "int",
                "solution": ["Total pets = %s = %d."
                             % (" + ".join("%d×%d" % (c, f)
                                           for c, f in zip(cats, freqs)), total_sum),
                             "Total students = %d." % total_items,
                             "%d ÷ %d = %d." % (total_sum, total_items,
                                                total_sum // total_items)]}

    if t == 6:                                        # median from a frequency table (total items)
        cats = [0, 1, 2, 3]
        freqs = [random.randint(1, 5) for _ in cats]
        rows = [[str(c), str(f)] for c, f in zip(cats, freqs)]
        return {"prompt": "This frequency table shows goals scored in some matches. "
                          "How many matches were there ALTOGETHER?",
                "component": "data_table",
                "spec": {"caption": "Goals per match", "headers": ["Goals", "Frequency"],
                         "rows": rows},
                "answer": sum(freqs), "answer_type": "int",
                "solution": ["Add the frequencies: %s = %d."
                             % (" + ".join(str(f) for f in freqs), sum(freqs))]}

    if t == 7:                                        # word: mean score
        who = pick(NAMES)
        k = random.randint(4, 6)
        scores = [random.randint(3, 10) for _ in range(k)]
        while sum(scores) % k:
            scores = [random.randint(3, 10) for _ in range(k)]
        return _num_q("%s scores %s in %d games. What is the mean score?"
                      % (who, ", ".join(str(s) for s in scores), k),
                      sum(scores) // k, "int",
                      solution=["Total = %d." % sum(scores),
                                "%d ÷ %d = %d." % (sum(scores), k, sum(scores) // k)])

    if t == 8:                                        # which average? reasoning
        which, ans = pick([
            ("the most common value", "mode"),
            ("the middle value when the data is in order", "median"),
            ("the total shared equally between all the values", "mean"),
            ("the difference between the largest and smallest", "range"),
        ])
        return _num_q("Which measure is %s? (type one word)" % which, ans, "str",
                      text=True, placeholder="mean / median / mode / range",
                      solution=["Recall what each measure describes.",
                                "The answer is the %s." % ans])

    # new mean after adding a value
    vals = [random.randint(2, 12) for _ in range(n)]
    while sum(vals) % n:
        vals = [random.randint(2, 12) for _ in range(n)]
    old_mean = sum(vals) // n
    extra = random.randint(2, 15)
    new_total = sum(vals) + extra
    while new_total % (n + 1):
        extra = random.randint(2, 15)
        new_total = sum(vals) + extra
    return _num_q("The mean of %d numbers is %d, so their total is %d. One more number, "
                  "%d, is added. What is the mean of all %d numbers now?"
                  % (n, old_mean, sum(vals), extra, n + 1),
                  new_total // (n + 1), "int",
                  solution=["New total = %d + %d = %d." % (sum(vals), extra, new_total),
                            "%d ÷ %d = %d." % (new_total, n + 1, new_total // (n + 1))])


@skill("Y8.9.l", "Outliers, populations, samples and bias", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 2, 2, 2, 2, 2, 1, 1, 2, 1])

    if t == 8:                                         # mean after removing the outlier
        base = [random.randint(10, 20) for _ in range(4)]
        while sum(base) % 4:
            base = [random.randint(10, 20) for _ in range(4)]
        outlier = pick([random.randint(80, 100), random.randint(1, 4)])
        data = base + [outlier]
        random.shuffle(data)
        ans = sum(base) // 4
        return _num_q("This data set contains one outlier: %s. Identify the outlier and "
                      "remove it. What is the mean of the remaining values? (Removing an "
                      "outlier changes the mean.)"
                      % ", ".join(str(v) for v in data), ans, "int",
                      solution=["The outlier is %d; the other values are %s."
                                % (outlier, ", ".join(str(v) for v in base)),
                                "Mean of the rest = %d ÷ 4 = %d."
                                % (sum(base), ans)])

    if t == 9:                                         # effect of removing the outlier
        high = random.random() < 0.5
        ans = "decrease" if high else "increase"
        return _num_q("A data set has one outlier that is a very %s value compared with "
                      "the rest. What is the effect on the mean of removing this outlier "
                      "— does the mean increase or decrease? (type one word)"
                      % ("high" if high else "low"), ans, "str", text=True,
                      placeholder="increase / decrease",
                      solution=["A very high outlier pulls the mean up, so removing it "
                                "lowers the mean; a very low outlier does the opposite.",
                                "Removing it makes the mean %s." % ans])

    if t == 0:                                        # find the outlier value
        base = sorted(random.sample(range(20, 40), 5))
        outlier = pick([random.randint(1, 8), random.randint(80, 99)])
        vals = base + [outlier]
        random.shuffle(vals)
        return _data_list("Most of these values are clustered together but one is an "
                          "outlier (very different). Which value is the outlier?",
                          vals, outlier, "Value",
                          ["Five values are between %d and %d; %d is far away."
                           % (base[0], base[-1], outlier),
                           "The outlier is %d." % outlier])

    if t == 1:                                        # population vs sample vocab
        desc, ans = pick([
            ("every single member of the group you want to study", "population"),
            ("a smaller part of the group, chosen to represent it", "sample"),
        ])
        return _num_q("In statistics, what do we call %s? (type one word)" % desc,
                      ans, "str", text=True, placeholder="population / sample",
                      solution=["The whole group is the population; a part of it is a "
                                "sample.",
                                "The answer is %s." % ans])

    if t == 2:                                        # biased or fair sample (typed)
        scenario, ans = pick([
            ("asking only football fans whether football should get more funding",
             "biased"),
            ("choosing names at random from a list of every student", "fair"),
            ("surveying only people leaving a gym about how much they exercise",
             "biased"),
            ("picking every 10th person from a full register", "fair"),
        ])
        return _num_q("A survey is carried out by %s. Is this sample likely to be fair or "
                      "biased? (type one word)" % scenario, ans, "str", text=True,
                      placeholder="fair / biased",
                      solution=["A fair sample represents the whole population; a biased "
                                "one favours certain answers.",
                                "This sample is %s." % ans])

    if t == 3:                                        # effect of outlier on mean
        base = [random.randint(10, 20) for _ in range(4)]
        outlier = random.randint(80, 100)
        vals = base + [outlier]
        mean_with = sum(vals) / 5.0
        mean_without = sum(base) / 4.0
        ans = "mean" if True else "median"
        return _num_q("A data set is %s. One value is a very high outlier. Which average "
                      "is affected MORE by this outlier — the mean or the median? "
                      "(type one word)" % ", ".join(str(v) for v in vals),
                      "mean", "str", text=True, placeholder="mean / median",
                      solution=["The mean uses every value, so a large outlier pulls it "
                                "up; the median (middle value) barely changes.",
                                "The mean is affected more."])

    if t == 4:                                        # median resistant - compute both roughly
        base = sorted([random.randint(10, 20) for _ in range(4)])
        outlier = random.randint(70, 90)
        vals = base + [outlier]
        s = sorted(vals)
        median = s[2]
        return _data_list("This data contains an outlier. Find the MEDIAN (middle value) "
                          "of the values in the table.", vals, median, "Value",
                          ["In order: %s." % ", ".join(str(v) for v in s),
                           "The middle value is %d (the outlier hardly affects it)."
                           % median])

    if t == 5:                                        # is it an outlier yes/no
        base = sorted(random.sample(range(30, 45), 4))
        val = pick([random.randint(30, 45), random.randint(1, 5)])
        is_out = val < 20 or val > 60
        vals = sorted(base + [val])
        return _num_q("In the data %s, is the value %d an outlier (very different from "
                      "the rest)? (type yes or no)"
                      % (", ".join(str(v) for v in vals), val),
                      "yes" if is_out else "no", "str", text=True, placeholder="yes / no",
                      solution=["An outlier sits far from the cluster of other values.",
                                "The value %d %s an outlier." % (val, "is" if is_out
                                                                 else "is not")])

    if t == 6:                                        # sample size sensible
        return _num_q("To find out the favourite subject of all 900 students in a school, "
                      "a fair sample of 90 students is surveyed. What FRACTION of the "
                      "whole school is this sample? Give your answer as a fraction.",
                      "90/900", "frac",
                      solution=["90 out of 900 = 90/900 = 1/10.",
                                "The sample is one tenth of the population."])

    # why sample rather than whole population
    reason, ans = pick([
        ("asking every person would take too long and cost too much", "sample"),
        ("you want an exact figure for every single member", "population"),
    ])
    return _num_q("When %s, should you survey a sample or the whole population? "
                  "(type one word)" % reason, ans, "str", text=True,
                  placeholder="sample / population",
                  solution=["Samples save time; a census (whole population) gives exact "
                            "figures but is costly.",
                            "The best choice here is the %s." % ans])


@skill("Y8.9.m", "Scatter graphs and correlation", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 2, 2, 2, 2, 1, 2, 2])
    kind = pick(["positive", "negative", "none"])
    # each context is paired with the correlation it really has
    _CTX = {
        "positive": [("Height (cm)", "Mass (kg)", "height and mass"),
                     ("Hours revised", "Test score", "revision time and test score"),
                     ("Temperature (°C)", "Ice creams sold", "temperature and ice creams sold")],
        "negative": [("Age of car (years)", "Value (£1000s)", "a car's age and its value"),
                     ("Temperature (°C)", "Hot drinks sold", "temperature and hot drinks sold"),
                     ("Hours of TV a week", "Test score", "hours of TV watched and test score")],
        "none": [("Shoe size", "Test score", "shoe size and test score"),
                 ("House number", "Height (cm)", "house number and height"),
                 ("Day of birth in the month", "Hours of sleep", "day of birth and hours of sleep")],
    }

    def _ctx(k):
        return pick(_CTX[k])

    xlab, ylab, ctx = _ctx(kind)

    def _pts(kind):
        xs = sorted(random.sample(range(1, 20), 7))
        pts = []
        for x in xs:
            if kind == "positive":
                y = 2 * x + random.randint(-2, 2)
            elif kind == "negative":
                y = 40 - 2 * x + random.randint(-2, 2)
            else:
                y = random.randint(5, 35)
            pts.append([x, max(1, y)])
        return pts

    if t == 8:                                         # create a scatter plot (plot a point)
        x0 = random.randint(2, 12)
        y0 = random.randint(2, 20)
        return _num_q("Create a scatter plot for this data. One data pair is "
                      "(%s = %d, %s = %d). When this point is plotted on the scatter "
                      "graph, how far up the y-axis is it (its y-coordinate)?"
                      % (xlab, x0, ylab, y0), y0, "int",
                      solution=["A point (x, y) is plotted x across and y up.",
                                "The point (%d, %d) is plotted at height %d."
                                % (x0, y0, y0)])

    if t == 9:                                         # make a prediction from best-fit line
        m = pick([2, 3])
        c = random.randint(2, 8)
        pts = [[x, m * x + c + random.randint(-2, 2)]
               for x in sorted(random.sample(range(1, 10), 6))]
        xq = pick([4, 5, 6, 7, 8])
        pred = m * xq + c
        return {"prompt": "This scatter graph has a line of best fit. Make a prediction: "
                          "use the line of best fit, which follows y = %dx + %d, to "
                          "predict the y-value when x = %d." % (m, c, xq),
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab,
                         "line": {"p1": [0, c], "p2": [10, c + 10 * m]}},
                "answer": pred, "answer_type": "num", "tolerance": 1,
                "solution": ["The line of best fit is y = %dx + %d." % (m, c),
                             "At x = %d, y = %d × %d + %d = %d."
                             % (xq, m, xq, c, pred)]}

    if t == 0:                                        # describe correlation (visual)
        pts = _pts(kind)
        return {"prompt": "This scatter graph shows %s. Describe the correlation. "
                          "(type: positive, negative or none)" % ctx,
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab},
                "answer": kind, "answer_type": "str",
                "solution": ["Positive: points rise; negative: points fall; none: no "
                             "clear pattern.",
                             "This shows %s correlation."
                             % (kind if kind != "none" else "no")]}

    if t == 1:                                        # predict from line of best fit (visual)
        # line through (0, c) and (10, c+10m) with integer prediction
        m = pick([2, 3])
        c = random.randint(2, 8)
        x1, y1 = 0, c
        x2, y2 = 10, c + 10 * m
        pts = [[x, m * x + c + random.randint(-2, 2)] for x in sorted(
            random.sample(range(1, 10), 6))]
        xq = pick([4, 5, 6, 7, 8])
        pred = m * xq + c
        return {"prompt": "This scatter graph has a line of best fit drawn on it. "
                          "Use the line to predict the y-value when x = %d." % xq,
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab,
                         "line": {"p1": [x1, y1], "p2": [x2, y2]}},
                "answer": pred, "answer_type": "num", "tolerance": 1,
                "solution": ["The line of best fit follows y = %dx + %d." % (m, c),
                             "At x = %d, y = %d × %d + %d = %d." % (xq, m, xq, c, pred)]}

    if t == 2:                                        # identify outlier x-value (visual)
        xlab, ylab, ctx = _ctx("positive")
        pts = _pts("positive")
        ox = random.randint(6, 15)
        oy = random.randint(1, 4)                       # low y where trend is high
        pts.append([ox, oy])
        pts.sort()
        idx = pts.index([ox, oy])
        return {"prompt": "This scatter graph mostly shows a positive trend, but one "
                          "point does not fit the pattern (an outlier). Type the "
                          "x-value of that outlier point.",
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab},
                "answer": ox, "answer_type": "int",
                "solution": ["Most points rise together, but one sits well below the "
                             "trend.",
                             "The outlier is at x = %d." % ox]}

    if t == 3:                                        # correlation from a real context (typed)
        ctx2, ans = pick([
            ("As height increases, mass tends to increase", "positive"),
            ("As a car gets older, its value tends to fall", "negative"),
            ("As temperature rises, more ice creams are sold", "positive"),
            ("As the amount of rain increases, ice cream sales fall", "negative"),
            ("A person's shoe size and their exam mark", "none"),
        ])
        return _num_q("%s. What type of correlation is this? (type positive, negative or "
                      "none)" % ctx2, ans, "str", text=True,
                      placeholder="positive / negative / none",
                      solution=["Both increasing together = positive; one up as the "
                                "other down = negative; no link = none.",
                                "This is %s correlation."
                                % (ans if ans != "none" else "no")])

    if t == 4:                                        # what the trend means (typed)
        rel, ans = pick([
            ("positive", "increases"), ("negative", "decreases"),
        ])
        return _num_q("A scatter graph of revision hours against test score shows %s "
                      "correlation. So as revision hours increase, the test score tends "
                      "to... (type one word: increases or decreases)" % rel, ans, "str",
                      text=True, placeholder="increases / decreases",
                      solution=["Positive correlation means both rise together; negative "
                                "means one falls as the other rises.",
                                "The score tends to %s." % ans])

    if t == 6:                                        # describe correlation, downhill (visual)
        xlab, ylab, ctx = _ctx("negative")
        pts = _pts("negative")
        return {"prompt": "This scatter graph shows %s. The points go downhill from "
                          "top-left to bottom-right. What type of correlation is this? "
                          "(type positive, negative or none)" % ctx,
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab},
                "answer": "negative", "answer_type": "str",
                "solution": ["Points falling from left to right show negative "
                             "correlation.",
                             "The answer is negative."]}

    if t == 5:                                        # read a point (visual)
        pts = _pts(kind)
        k = random.randrange(len(pts))
        return {"prompt": "This scatter graph shows %s. The outlined point has an x-value "
                          "of %d (%s). What is its y-value (%s)?"
                          % (ctx, pts[k][0], xlab.lower(), ylab.lower()),
                "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": xlab, "yLabel": ylab,
                         "highlight": k},
                "answer": pts[k][1], "answer_type": "int",
                "solution": ["Find x = %d and read up to the outlined point."
                             % pts[k][0],
                             "The y-value is %d." % pts[k][1]]}

    # strength/type reasoning (typed)
    return _num_q("On a scatter graph, the points lie almost exactly along a straight "
                  "line sloping upwards. Is the correlation positive or negative? "
                  "(type one word)", "positive", "str", text=True,
                  placeholder="positive / negative",
                  solution=["Points sloping upwards show positive correlation.",
                            "The answer is positive."])


_DICE = [(1, "landing on a 6", 6, 1), ]


@skill("Y8.9.n", "Probability of single events", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 2, 2, 1, 1, 4, 1, 1])

    if t == 10:                                        # collected data -> probability + prediction
        trials = pick([10, 20, 25, 50])
        success = random.randint(1, trials - 1)
        mult = pick([2, 3, 4, 5])
        newN = trials * mult
        pred = success * mult
        return _num_q("Use collected data to find a probability and make a prediction. "
                      "In a test a spinner was spun %d times and landed on red %d times "
                      "(this is collected data). Based on these results, if the spinner "
                      "is spun %d more times, how many times would you predict it lands "
                      "on red?" % (trials, success, newN), pred, "int", unit="times",
                      solution=["Experimental probability of red = %d/%d."
                                % (success, trials),
                                "Prediction = %d/%d × %d = %d times."
                                % (success, trials, newN, pred)])

    if t == 11:                                        # prediction from theoretical probability
        target, fav = pick([("an even number", 3), ("a number greater than 4", 2),
                            ("a 6", 1), ("a prime number", 3)])
        n = pick([12, 18, 24, 30, 60])
        pred = fav * n // 6
        return _num_q("Make a prediction using theoretical probability. A fair six-sided "
                      "dice is rolled %d times. Using the theoretical probability, "
                      "predict how many times you would expect to roll %s."
                      % (n, target), pred, "int", unit="times",
                      solution=["Theoretical probability = %d/6." % fav,
                                "Prediction = %d/6 × %d = %d times." % (fav, n, pred)])

    if t == 9:                                        # spinner as a pie chart (visual)
        r = random.randint(1, 4)
        b = random.randint(1, 4)
        g = random.randint(1, 4)
        total = r + b + g
        colour, fav = pick([("red", r), ("blue", b), ("green", g)])
        fr = Fraction(fav, total)
        return {"prompt": "This spinner is split into coloured sections by size, as shown. "
                          "The spinner is spun once. What is the probability it lands on "
                          "%s? Give your answer as a fraction." % colour,
                "component": "pie_chart",
                "spec": {"slices": [["Red", r], ["Blue", b], ["Green", g]]},
                "answer": "%d/%d" % (fav, total), "answer_type": "frac",
                "solution": ["The spinner has %d equal parts and %d are %s."
                             % (total, fav, colour),
                             "P = %d/%d." % (fav, total)]}

    if t == 0:                                        # dice probability (fraction)
        target, fav = pick([("an even number", 3), ("a number greater than 4", 2),
                            ("a 6", 1), ("a number less than 3", 2),
                            ("a prime number", 3)])
        fr = Fraction(fav, 6)
        return _num_q("A fair six-sided dice is rolled. What is the probability of "
                      "rolling %s? Give your answer as a fraction." % target,
                      "%d/6" % fav, "frac",
                      solution=["There are 6 equally likely outcomes and %d are %s."
                                % (fav, target),
                                "P = %d/6 = %d/%d." % (fav, fr.numerator, fr.denominator)])

    if t == 1:                                        # coloured balls (fraction)
        r = random.randint(2, 6)
        b = random.randint(2, 6)
        g = random.randint(1, 5)
        total = r + b + g
        colour, fav = pick([("red", r), ("blue", b), ("green", g)])
        fr = Fraction(fav, total)
        return _num_q("A bag has %d red, %d blue and %d green counters. One counter is "
                      "taken at random. What is the probability it is %s? "
                      "Give your answer as a fraction." % (r, b, g, colour),
                      "%d/%d" % (fav, total), "frac",
                      solution=["There are %d counters and %d are %s."
                                % (total, fav, colour),
                                "P = %d/%d." % (fav, total)])

    if t == 2:                                        # probability as a decimal
        fav = random.randint(1, 9)
        total = 10 if fav <= 10 else 20
        total = pick([10, 20, 5, 4])
        fav = random.randint(1, total - 1)
        p = fav / float(total)
        return _num_q("A spinner has %d equal sections and %d of them are winning "
                      "sections. What is the probability of winning, as a DECIMAL?"
                      % (total, fav), round(p, 4), "num", tolerance=0.001,
                      solution=["P = %d ÷ %d = %s." % (fav, total, _f(round(p, 4)))])

    if t == 3:                                        # probability as a percentage
        total = pick([4, 5, 10, 20])
        fav = random.randint(1, total - 1)
        pct = 100 * fav // total
        while (100 * fav) % total:
            total = pick([4, 5, 10, 20])
            fav = random.randint(1, total - 1)
            pct = 100 * fav // total
        return _num_q("A spinner has %d equal sections; %d are red. What is the "
                      "probability of landing on red, as a PERCENTAGE?" % (total, fav),
                      pct, "num", unit="%", tolerance=0.1,
                      solution=["P = %d/%d = %d%%." % (fav, total, pct)])

    if t == 4:                                        # complement (not event)
        total = pick([6, 8, 10])
        fav = random.randint(1, total - 1)
        fr = Fraction(total - fav, total)
        return _num_q("The probability of an event is %d/%d. What is the probability that "
                      "it does NOT happen? Give your answer as a fraction."
                      % (fav, total), "%d/%d" % (total - fav, total), "frac",
                      solution=["P(not) = 1 − P(event).",
                                "1 − %d/%d = %d/%d." % (fav, total, total - fav, total)])

    if t == 5:                                        # expected frequency
        total = pick([4, 5, 6, 10])
        fav = random.randint(1, total - 1)
        n = pick([20, 40, 60, 100, 120])
        while (n * fav) % total:
            n = pick([20, 40, 60, 100, 120])
        exp = n * fav // total
        return _num_q("The probability of a spinner landing on blue is %d/%d. "
                      "If it is spun %d times, how many times would you EXPECT it to "
                      "land on blue?" % (fav, total, n), exp, "int", unit="times",
                      solution=["Expected = probability × number of trials.",
                                "%d/%d × %d = %d." % (fav, total, n, exp)])

    if t == 6:                                        # experimental probability
        trials = pick([20, 50, 100])
        success = random.randint(1, trials - 1)
        fr = Fraction(success, trials)
        return _num_q("In an experiment a drawing pin was dropped %d times and landed "
                      "point-up %d times. What is the experimental probability of it "
                      "landing point-up? Give your answer as a fraction."
                      % (trials, success), "%d/%d" % (success, trials), "frac",
                      solution=["Experimental probability = successes ÷ trials.",
                                "%d/%d." % (success, trials)])

    if t == 7:                                        # likelihood word (typed)
        p, ans = pick([(Fraction(0), "impossible"), (Fraction(1), "certain"),
                       (Fraction(1, 2), "even chance")])
        return _num_q("An event has probability %s. In words, is it impossible, certain "
                      "or an even chance? (type your answer)"
                      % ("0" if p == 0 else ("1" if p == 1 else "1/2")),
                      ans, "str", text=True,
                      placeholder="impossible / certain / even chance",
                      solution=["0 = impossible, 1 = certain, 1/2 = even chance.",
                                "This is %s." % ans])

    # cards from a deck (fraction)
    target, fav = pick([("a heart", 13), ("a king", 4), ("the ace of spades", 1),
                        ("a red card", 26), ("a picture card (J, Q, K)", 12)])
    fr = Fraction(fav, 52)
    return _num_q("One card is taken at random from a standard pack of 52 playing cards. "
                  "What is the probability it is %s? Give your answer as a fraction."
                  % target, "%d/52" % fav, "frac",
                  solution=["There are 52 cards and %d are %s." % (fav, target),
                            "P = %d/52 = %d/%d." % (fav, fr.numerator, fr.denominator)])


@skill("Y8.9.o", "Sample spaces and combined events", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2])

    if t == 10:                                        # compound events: number of outcomes
        a = pick([2, 3, 4])
        b = pick([2, 3, 4, 5])
        c = pick([2, 3])
        return _num_q("Compound events: find the number of outcomes. A three-course meal "
                      "is made by choosing %d starters, %d main courses and %d puddings. "
                      "Using the counting principle, how many different meals (outcomes) "
                      "are possible?" % (a, b, c), a * b * c, "int", unit="outcomes",
                      solution=["Multiply the number of choices at each stage: "
                                "%d × %d × %d." % (a, b, c),
                                "= %d outcomes." % (a * b * c)])

    if t in (8, 9):                                   # sample-space grid (visual)
        # two dice, table of totals; ask a count or a probability
        headers = ["+"] + [str(c) for c in range(1, 7)]
        rows = [[str(r)] + [str(r + c) for c in range(1, 7)] for r in range(1, 7)]
        target = pick([5, 6, 7, 8, 9, 10])
        ways = sum(1 for r in range(1, 7) for c in range(1, 7) if r + c == target)
        if t == 8:                                    # count
            return {"prompt": "This table shows the total when two fair dice are added "
                              "(one dice across the top, one down the side). In how many "
                              "of the 36 cells is the total equal to %d?" % target,
                    "component": "data_table",
                    "spec": {"caption": "Sum of two dice", "headers": headers,
                             "rows": rows},
                    "answer": ways, "answer_type": "int",
                    "solution": ["Count the cells showing %d." % target,
                                 "There are %d of them out of 36." % ways]}
        fr = Fraction(ways, 36)
        return {"prompt": "This table shows the total when two fair dice are added. "
                          "What is the probability the total is %d? Give a fraction."
                          % target,
                "component": "data_table",
                "spec": {"caption": "Sum of two dice", "headers": headers, "rows": rows},
                "answer": "%d/36" % ways, "answer_type": "frac",
                "solution": ["%d of the 36 cells show %d." % (ways, target),
                             "P = %d/36 = %d/%d." % (ways, fr.numerator,
                                                     fr.denominator)]}

    if t == 0:                                        # size of sample space
        setup, size = pick([
            ("two fair coins are flipped", 4),
            ("a coin is flipped and a six-sided dice is rolled", 12),
            ("two six-sided dice are rolled", 36),
            ("a four-sided spinner is spun and a coin is flipped", 8),
        ])
        return _num_q("When %s, how many equally likely outcomes are there in the sample "
                      "space altogether?" % setup, size, "int",
                      solution=["Multiply the number of outcomes for each part.",
                                "There are %d outcomes." % size])

    if t == 1:                                        # two dice sum probability
        target = pick([2, 3, 7, 11, 12, 6, 8])
        ways = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2,
                12: 1}[target]
        fr = Fraction(ways, 36)
        return _num_q("Two fair six-sided dice are rolled and their scores are added. "
                      "What is the probability the total is %d? Give your answer as a "
                      "fraction." % target, "%d/36" % ways, "frac",
                      solution=["There are 36 outcomes and %d give a total of %d."
                                % (ways, target),
                                "P = %d/36 = %d/%d." % (ways, fr.numerator,
                                                        fr.denominator)])

    if t == 2:                                        # coin and dice combined event
        fr = Fraction(1, 12)
        return _num_q("A fair coin and a fair six-sided dice are used. What is the "
                      "probability of getting a head AND a six? Give your answer as a "
                      "fraction.", "1/12", "frac",
                      solution=["There are 2 × 6 = 12 equally likely outcomes.",
                                "Only 1 is (head, six), so P = 1/12."])

    if t == 3:                                        # mutually exclusive OR
        total = pick([6, 8, 10])
        a = random.randint(1, total - 2)
        b = random.randint(1, total - a)
        fr = Fraction(a + b, total)
        return _num_q("Two events cannot both happen (they are mutually exclusive). "
                      "One has probability %d/%d and the other %d/%d. What is the "
                      "probability that ONE OR THE OTHER happens? Give a fraction."
                      % (a, total, b, total), "%d/%d" % (a + b, total), "frac",
                      solution=["For mutually exclusive events, add the probabilities.",
                                "%d/%d + %d/%d = %d/%d." % (a, total, b, total, a + b,
                                                            total)])

    if t == 4:                                        # count favourable outcomes two dice
        target = pick(["a double", "a total of 7", "at least one 6"])
        ways = {"a double": 6, "a total of 7": 6, "at least one 6": 11}[target]
        return _num_q("Two fair six-sided dice are rolled (36 outcomes in total). "
                      "How many of the outcomes give %s?" % target, ways, "int",
                      solution=["List or count the matching outcomes.",
                                "There are %d such outcomes out of 36." % ways])

    if t == 5:                                        # product rule (count)
        aa = pick([2, 3, 4])
        bb = pick([2, 3, 4, 5])
        return _num_q("A meal deal offers %d choices of sandwich and %d choices of drink. "
                      "How many different sandwich-and-drink combinations are possible?"
                      % (aa, bb), aa * bb, "int", unit="combinations",
                      solution=["Multiply the choices: %d × %d." % (aa, bb),
                                "= %d combinations." % (aa * bb)])

    if t == 6:                                        # spinner and spinner sum
        target = pick([2, 3, 4, 5, 6])
        # two 3-sided spinners (1,2,3): outcomes 9
        ways = {2: 1, 3: 2, 4: 3, 5: 2, 6: 1}[target]
        fr = Fraction(ways, 9)
        return _num_q("Two spinners each show 1, 2 or 3 with equal chance. Their numbers "
                      "are added. Out of the 9 equally likely outcomes, what is the "
                      "probability the total is %d? Give a fraction." % target,
                      "%d/9" % ways, "frac",
                      solution=["There are 3 × 3 = 9 outcomes, %d give a total of %d."
                                % (ways, target),
                                "P = %d/9." % ways])

    # mutually exclusive: are they? P(A)+P(B) not exceeding 1 reasoning
    return _num_q("Rolling a fair dice, are the events 'rolling a 2' and 'rolling an odd "
                  "number' mutually exclusive (they cannot happen at the same time)? "
                  "(type yes or no)", "yes", "str", text=True, placeholder="yes / no",
                  solution=["2 is an even number, so it cannot also be odd.",
                            "The events cannot happen together, so yes."])
