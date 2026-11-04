# dev/app/logic/y6_gen_e.py — Year 6 generators: levels 6.8 (geometry) and
# 6.9 (measurement, statistics & problem solving).
#
# Every generator takes a difficulty tier: d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between 8+ genuinely different framings (visual model, bare
# calculation, word problem, missing number, inverse, comparison, reasoning).
#
# Visual components used here:
#   geometry ...... shape / net / circle / angle / coordinate_grid / area_grid
#   statistics .... data_table / bar_chart / line_graph / pie_chart / clock / ruler
import random
from fractions import Fraction
from .maths_engine import skill, pick, money, NAMES

S8 = "6.8 Geometry"
S9 = "6.9 Measurement, statistics & problem solving"


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
    """Choose a framing index; visual framings carry more weight."""
    total = float(sum(weights))
    r = random.random() * total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r < acc:
            return i
    return len(weights) - 1


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _a(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def _f(x):
    """Tidy a number for printing: 3.0 -> '3', 2.500 -> '2.5'."""
    if isinstance(x, int):
        return str(x)
    s = ("%.6f" % float(x)).rstrip("0").rstrip(".")
    return s if s not in ("", "-") else "0"


def _dec_ask(value, places=1):
    """Make a computed decimal actually answerable.

    A value like 133.5555... cannot be typed, and rounding it fails a tight
    tolerance -- so state the rounding in the prompt and store the ROUNDED
    value. Exact short decimals are left alone.
    Returns (answer, instruction, tolerance).
    """
    v = float(value)
    if abs(v - round(v)) < 1e-9:
        return round(v), "", 0.005
    if abs(v - round(v, 2)) < 1e-9:
        return round(v, 2), "Give your answer as a decimal.", 0.005
    return (round(v, places),
            "Give your answer to %d decimal place%s." % (places, "" if places == 1 else "s"),
            0.5 * 10 ** (-places))


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


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _distinct(count, lo, hi):
    hi = max(hi, lo + count)
    return random.sample(range(lo, hi + 1), count)


def _an(n):
    """Indefinite article for a number: 'an 8 cm', 'a 6 cm', 'an 18 m'."""
    t = str(int(n))
    return "an" if (t[0] == "8" or t[:2] in ("11", "18")) else "a"


def _coord(x, y):
    return "(%d,%d)" % (int(x), int(y))


def _q4(d):
    """A four-quadrant coordinate_grid spec (plot mode)."""
    r = _by_d(d, 5, 6, 8)
    return {"mode": "plot", "xmin": -r, "xmax": r, "ymin": -r, "ymax": r}


def _q4r(d):
    return _by_d(d, 5, 6, 8)


def _nz(lo, hi):
    """A non-zero integer in [lo, hi]."""
    v = random.randint(lo, hi)
    while v == 0:
        v = random.randint(lo, hi)
    return v


def _L_cells(R, C, r, c):
    """An L-shape: an R x C rectangle with an r x c notch cut from the top right."""
    return [[i, j] for i in range(R) for j in range(C)
            if not (i < r and j >= C - c)]


# ------------------------------------------------------------ shape facts ----
# polygons the `shape` component can actually draw (all regular but the rectangle)
_DRAWN = [("triangle", 3), ("square", 4), ("rectangle", 4), ("pentagon", 5),
          ("hexagon", 6), ("heptagon", 7), ("octagon", 8)]
_DRAWN_NAMEABLE = [("triangle", 3), ("pentagon", 5), ("hexagon", 6),
                   ("heptagon", 7), ("octagon", 8)]

_POLY = [("triangle", 3), ("quadrilateral", 4), ("pentagon", 5), ("hexagon", 6),
         ("heptagon", 7), ("octagon", 8), ("nonagon", 9), ("decagon", 10)]

_SYM_DRAWN = {"square": (4, "square"), "rectangle": (2, "rectangle"),
              "triangle": (3, "equilateral triangle"),
              "pentagon": (5, "regular pentagon"), "hexagon": (6, "regular hexagon"),
              "heptagon": (7, "regular heptagon"), "octagon": (8, "regular octagon")}

# (name, pairs of parallel sides, right angles, lines of symmetry)
_QUADS = [("square", 2, 4, 4), ("rectangle", 2, 4, 2), ("rhombus", 2, 0, 2),
          ("parallelogram", 2, 0, 0), ("trapezium", 1, 0, 0), ("kite", 0, 0, 1)]
_QUAD_NAMES = "square / rectangle / rhombus / parallelogram / trapezium / kite"

# solids the `shape` component draws: (name, faces, edges, vertices)
_SOLIDS_DRAWN = [("cube", 6, 12, 8), ("cuboid", 6, 12, 8),
                 ("square-based pyramid", 5, 8, 5), ("triangular prism", 5, 9, 6)]

# every solid Year 6 meets, drawn or not (curved surfaces counted as faces)
_SOLIDS_ALL = _SOLIDS_DRAWN + [("cylinder", 3, 2, 0), ("cone", 2, 1, 1),
                               ("sphere", 1, 0, 0),
                               ("hexagonal prism", 8, 18, 12),
                               ("pentagonal prism", 7, 15, 10),
                               ("triangular-based pyramid", 4, 6, 4)]

# nets the `net` component draws: (spec value, solid name, faces)
_NETS = [("cube", "cube", 6), ("cuboid", "cuboid", 6),
         ("square_pyramid", "square-based pyramid", 5),
         ("triangular_prism", "triangular prism", 5),
         ("cylinder", "cylinder", 3), ("cone", "cone", 2)]
_NET_NAMES = ("cube / cuboid / square-based pyramid / triangular prism / "
              "cylinder / cone")


# ================================================================== 6.8 ======
@skill("Y6.8.a", "Classify 2-D shapes and polygons", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2])

    if t == 11:                                       # sort polygons into a Venn diagram
        left, right = pick([("have 4 sides", "have a right angle"),
                            ("have more than 4 sides", "have a line of symmetry"),
                            ("have an odd number of sides", "have equal sides"),
                            ("are quadrilaterals", "have two pairs of parallel sides")])
        a = random.randint(2, _by_d(d, 6, 9, 12))      # left circle only
        b = random.randint(1, _by_d(d, 5, 8, 10))      # overlap
        c = random.randint(2, _by_d(d, 6, 9, 12))      # right circle only
        e = random.randint(0, _by_d(d, 3, 5, 8))       # outside both circles
        want = pick(["left", "right"])
        ans = a + b if want == "left" else c + b
        lab = left if want == "left" else right
        return _num_q("A set of polygons is sorted into a Venn diagram with two circles: "
                      "one circle for polygons that %s and one circle for polygons that "
                      "%s. The “%s” circle alone holds %s, the overlap of the two circles "
                      "holds %s, the “%s” circle alone holds %s and %s outside both "
                      "circles. How many polygons are in the “%s” circle altogether?"
                      % (left, right, left, _pl(a, "polygon"), _pl(b, "polygon"), right,
                         _pl(c, "polygon"),
                         "%s lie" % _pl(e, "polygon") if e != 1 else "1 polygon lies",
                         lab),
                      ans, "int", unit="polygons",
                      solution=["The whole circle is the part on its own plus the overlap.",
                                "%d + %d = %d polygons."
                                % (a if want == "left" else c, b, ans)])

    if t == 12:                                       # Venn diagram total
        left, right = pick([("have 4 sides", "have a right angle"),
                            ("have more than 4 sides", "have a line of symmetry"),
                            ("are regular", "have fewer than 6 sides")])
        a = random.randint(2, _by_d(d, 6, 9, 12))
        b = random.randint(1, _by_d(d, 5, 8, 10))
        c = random.randint(2, _by_d(d, 6, 9, 12))
        e = random.randint(1, _by_d(d, 3, 5, 8))
        return _num_q("Polygons are sorted into a Venn diagram with a circle for polygons "
                      "that %s and a circle for polygons that %s. The first circle alone "
                      "holds %s, the overlap holds %s, the second circle alone holds %s "
                      "and %s outside both circles. How many polygons were sorted "
                      "altogether?" % (left, right, _pl(a, "polygon"), _pl(b, "polygon"),
                                       _pl(c, "polygon"),
                                       "%s lie" % _pl(e, "polygon") if e != 1
                                       else "1 polygon lies"),
                      a + b + c + e, "int", unit="polygons",
                      solution=["Add every region of the Venn diagram.",
                                "%d + %d + %d + %d = %d polygons."
                                % (a, b, c, e, a + b + c + e)])

    if t == 13:                                       # congruent or similar
        w = random.randint(2, 6)
        h = random.randint(2, 6)
        while h == w:
            h = random.randint(2, 6)
        k = pick([1, 2, 3]) if d else pick([1, 2])
        ans = "congruent" if k == 1 else "similar"
        return _num_q("Congruent figures are the same shape and the same size. Similar "
                      "figures are the same shape but not the same size. Rectangle A "
                      "measures %d cm by %d cm and rectangle B measures %d cm by %d cm. "
                      "Are the two figures congruent or similar? (type one word)"
                      % (w, h, k * w, k * h),
                      ans, "str", text=True, placeholder="congruent / similar",
                      solution=["Every side of B is %d times the matching side of A." % k,
                                "The two figures are %s." % ans])

    # scale factor between two similar figures
    if t == 14:
        s = random.randint(2, 7)
        k = random.randint(2, _by_d(d, 3, 4, 6))
        return _num_q("Two similar triangles have the same shape but different sizes. The "
                      "shortest side of the smaller triangle is %d cm and the shortest "
                      "side of the larger triangle is %d cm. How many times larger are "
                      "the sides of the larger figure?" % (s, k * s),
                      k, "int", unit="times",
                      solution=["%d ÷ %d = %d." % (k * s, s, k),
                                "Every side of the larger similar figure is %d times as "
                                "long." % k])

    if t == 0:                                        # visual: name the polygon
        nm, sd = pick(_DRAWN_NAMEABLE if d else _DRAWN_NAMEABLE[:3])
        return {"prompt": "This polygon is regular. What is its name?",
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["Count the straight sides: there are %d." % sd,
                             "A polygon with %d sides is %s." % (sd, _a(nm))]}

    if t == 1:                                        # visual: count sides/vertices
        nm, sd = pick(_DRAWN)
        ask = pick(["sides", "vertices"])
        return {"prompt": "How many %s does this polygon have?"
                          % ("sides" if ask == "sides" else "vertices (corners)"),
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": ask},
                "answer": sd, "answer_type": "int",
                "solution": ["A polygon has as many vertices as sides.",
                             "This one has %d." % sd]}

    if t == 2:                                        # visual: lines of symmetry
        nm = pick(list(_SYM_DRAWN.keys()))
        lines, label = _SYM_DRAWN[nm]
        return {"prompt": "How many lines of symmetry does this shape have?",
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "lines_of_symmetry"},
                "answer": lines, "answer_type": "int",
                "solution": ["A regular polygon has one line of symmetry for each side.",
                             "%s has %s of symmetry."
                             % (_a(label).capitalize(), _pl(lines, "line"))]}

    if t == 3:                                        # interior angle sum
        nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
        return _num_q("The interior angles of a polygon with n sides add up to "
                      "(n − 2) × 180°. What do the interior angles of %s add up to?"
                      % _a(nm),
                      (sd - 2) * 180, "int", unit="degrees",
                      solution=["%s has %d sides." % (_a(nm).capitalize(), sd),
                                "(%d − 2) × 180 = %d × 180 = %d°."
                                % (sd, sd - 2, (sd - 2) * 180)])

    if t == 4:                                        # each interior angle (regular)
        nm, sd = pick([("equilateral triangle", 3), ("square", 4),
                       ("regular pentagon", 5), ("regular hexagon", 6),
                       ("regular octagon", 8), ("regular decagon", 10)])
        each = (sd - 2) * 180 // sd
        return _num_q("Every interior angle of %s is the same size. "
                      "How many degrees is each interior angle?" % _a(nm),
                      each, "int", unit="degrees",
                      solution=["The angles add up to (%d − 2) × 180 = %d°."
                                % (sd, (sd - 2) * 180),
                                "%d ÷ %d = %d°." % ((sd - 2) * 180, sd, each)])

    if t == 5:                                        # sides -> name (typed)
        nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
        return _num_q("A polygon has %d straight sides. What is it called?" % sd,
                      nm, "str", text=True, placeholder="polygon name",
                      solution=["A polygon with %d sides is called %s." % (sd, _a(nm))])

    if t == 6:                                        # quadrilateral from properties
        attrs, quad = pick([
            ("4 equal sides and 4 right angles", "square"),
            ("4 right angles, with opposite sides equal but not all four equal",
             "rectangle"),
            ("4 equal sides and no right angles", "rhombus"),
            ("two pairs of parallel sides, no right angles and not all sides equal",
             "parallelogram"),
            ("exactly one pair of parallel sides", "trapezium"),
            ("two pairs of equal sides next to each other and no parallel sides",
             "kite"),
        ])
        return _num_q("Which quadrilateral has %s? (type the name)" % attrs,
                      quad, "str", text=True, placeholder=_QUAD_NAMES,
                      solution=["%s has %s." % (_a(quad).capitalize(), attrs)])

    if t == 7:                                        # classify a triangle by sides
        kind = pick(["scalene", "isosceles", "equilateral"])
        if kind == "equilateral":
            s = random.randint(4, 14)
            sides = (s, s, s)
        elif kind == "isosceles":
            s = random.randint(6, 14)
            b = random.randint(2, 2 * s - 1)
            while b == s:
                b = random.randint(2, 2 * s - 1)
            sides = (s, s, b)
        else:
            a, b, c = sorted(random.sample(range(4, 16), 3))
            while a + b <= c:
                a, b, c = sorted(random.sample(range(4, 16), 3))
            sides = (a, b, c)
        return _num_q("A triangle has sides of %d cm, %d cm and %d cm. Is it scalene, "
                      "isosceles or equilateral? (type one word)" % sides,
                      kind, "str", text=True,
                      placeholder="scalene / isosceles / equilateral",
                      solution=["Equilateral means 3 equal sides, isosceles exactly 2, "
                                "scalene none.",
                                "This triangle is %s." % kind])

    if t == 8:                                        # regular or irregular
        regular = random.random() < 0.5
        sd = pick([4, 5, 6, 8])
        desc = ("all %d sides equal and all %d angles equal" % (sd, sd)) if regular else \
               ("%d sides, but the sides are not all the same length" % sd)
        return _num_q("A polygon has %s. Is this polygon regular or irregular? "
                      "(type one word)" % desc,
                      "regular" if regular else "irregular", "str", text=True,
                      placeholder="regular / irregular",
                      solution=["A regular polygon has all sides equal AND all angles "
                                "equal.",
                                "This one is %s." % ("regular" if regular else "irregular")])

    if t == 9:                                        # sorting / comparison
        chosen = random.sample(_POLY, 4)
        cut = pick([4, 5, 6])
        cnt = sum(1 for _, sd in chosen if sd > cut)
        return _num_q("Look at these polygons: %s. How many of them have MORE than %d "
                      "sides?" % (", ".join(nm for nm, _ in chosen), cut),
                      cnt, "int", unit="polygons",
                      solution=["Sides: %s."
                                % ", ".join("%s %d" % (nm, sd) for nm, sd in chosen),
                                "%d of them have more than %d sides." % (cnt, cut)])

    # always / sometimes / never reasoning
    stmt, ans = pick([
        ("Every square is a rectangle", "always"),
        ("Every rectangle is a square", "sometimes"),
        ("A rhombus has four equal sides", "always"),
        ("A trapezium has two pairs of parallel sides", "never"),
        ("A parallelogram has right angles", "sometimes"),
        ("A regular polygon has equal angles", "always"),
        ("A triangle has a pair of parallel sides", "never"),
    ])
    return _num_q("“%s.” Is this always, sometimes or never true? "
                  "(type one word)" % stmt,
                  ans, "str", text=True, placeholder="always / sometimes / never",
                  solution=["Test the statement against every shape it could describe.",
                            "It is %s true." % ans])


@skill("Y6.8.b", "Lines, segments, rays, parallel and perpendicular", S8)
def _(d=1):
    d = _tier(d)
    r = _q4r(d)
    t = _pick_t([1, 1, 1, 1, 2, 2, 1, 1, 1, 1])

    if t == 0:                                        # vocabulary
        desc, ans = pick([
            ("goes on for ever in both directions", "line"),
            ("has two endpoints", "line segment"),
            ("starts at one endpoint and goes on for ever in one direction", "ray"),
        ])
        return _num_q("A straight path %s. Is it a line, a line segment or a ray? "
                      "(type the answer)" % desc,
                      ans, "str", text=True, placeholder="line / line segment / ray",
                      solution=["A straight path that %s is called a %s." % (desc, ans)])

    if t == 1:                                        # endpoints
        thing, ends = pick([("a line segment", 2), ("a ray", 1), ("a line", 0)])
        return _num_q("How many endpoints does %s have?" % thing,
                      ends, "int", unit="endpoints",
                      solution=["%s has %s." % (thing.capitalize(),
                                                _pl(ends, "endpoint") if ends
                                                else "no endpoints")])

    if t == 2:                                        # parallel / perpendicular vocab
        desc, ans = pick([
            ("never meet, however far they are extended", "parallel"),
            ("cross at a right angle", "perpendicular"),
            ("stay exactly the same distance apart", "parallel"),
            ("make a 90° angle where they meet", "perpendicular"),
        ])
        return _num_q("Two straight lines %s. What are they called? (type one word)"
                      % desc,
                      ans, "str", text=True, placeholder="parallel / perpendicular",
                      solution=["Lines that %s are %s." % (desc, ans)])

    if t == 3:                                        # real life
        case, ans = pick([("the two long rails of a ladder", "parallel"),
                          ("the two strokes of the letter L", "perpendicular"),
                          ("the two edges of a straight road", "parallel"),
                          ("the corner of a picture frame", "perpendicular"),
                          ("railway tracks", "parallel"),
                          ("a flagpole and the flat ground", "perpendicular"),
                          ("the lines on lined writing paper", "parallel"),
                          ("the hands of a clock at 3 o'clock", "perpendicular")])
        return _num_q("Are %s parallel or perpendicular? (type one word)" % case,
                      ans, "str", text=True, placeholder="parallel / perpendicular",
                      solution=["%s are %s." % (case.capitalize(), ans)])

    if t == 4:                                        # visual: complete a perpendicular
        x = _nz(-r + 1, r - 1)
        y = _nz(-r + 1, r - 1)
        k = random.randint(2, r - 1)
        horizontal = random.random() < 0.5
        # BOTH directions can land on the grid, so the direction must be stated
        # or the question has two correct answers.
        if horizontal:
            if x + k <= r:
                ax, ay, way = x + k, y, "to the right of P"
            else:
                ax, ay, way = x - k, y, "to the left of P"
            word = "horizontal"
        else:
            if y + k <= r:
                ax, ay, way = x, y + k, "above P"
            else:
                ax, ay, way = x, y - k, "below P"
            word = "vertical"
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "P"]]
        return {"prompt": "P is at %s. Plot a point Q so that the line segment PQ is %s "
                          "and %d units long, with Q %s."
                          % (_coord(x, y), word, k, way),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ax, ay), "answer_type": "coord",
                "solution": ["A %s segment keeps the %s the same."
                             % (word, "y-coordinate" if horizontal else "x-coordinate"),
                             "Counting %d units from %s gives %s."
                             % (k, _coord(x, y), _coord(ax, ay))]}

    if t == 5:                                        # visual: perpendicular through a point
        x = _nz(-r + 2, r - 2)
        y = _nz(-r + 2, r - 2)
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"], [x, -y, "B"]] if y != -y else [[x, y, "A"]]
        k = random.randint(1, r - 1)
        side = pick([-1, 1])
        ax = x + side * k
        if abs(ax) > r:
            ax = x - side * k
        return {"prompt": "The segment AB is vertical. Plot a point C at the same height "
                          "as A (the same y-coordinate) and %d units %s of A, so that AC "
                          "is perpendicular to AB."
                          % (k, "right" if ax > x else "left"),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ax, y), "answer_type": "coord",
                "solution": ["AB is vertical, so a perpendicular segment must be "
                             "horizontal.",
                             "Keep y = %d and move %d units to reach %s."
                             % (y, k, _coord(ax, y))]}

    if t == 6:                                        # horizontal / vertical from coords
        x = _nz(-r, r)
        y = _nz(-r, r)
        horizontal = random.random() < 0.5
        k = random.randint(1, r)
        if horizontal:
            x2, y2 = (x + k if x + k <= r else x - k), y
        else:
            x2, y2 = x, (y + k if y + k <= r else y - k)
        ans = "horizontal" if y2 == y else "vertical"
        return _num_q("A line segment joins %s to %s. Is the segment horizontal or "
                      "vertical? (type one word)" % (_coord(x, y), _coord(x2, y2)),
                      ans, "str", text=True, placeholder="horizontal / vertical",
                      solution=["The y-coordinates match, so the segment runs straight "
                                "across." if ans == "horizontal" else
                                "The x-coordinates match, so the segment runs straight up.",
                                "It is %s." % ans])

    if t == 7:                                        # two segments: parallel or perp
        same = random.random() < 0.5
        y1, y2 = random.sample(range(-r, r + 1), 2)
        x1 = _nz(-r + 1, r - 1)
        if same:
            return _num_q("One line segment joins %s to %s. Another joins %s to %s. "
                          "Are the two segments parallel or perpendicular? "
                          "(type one word)"
                          % (_coord(-r, y1), _coord(r, y1),
                             _coord(-r, y2), _coord(r, y2)),
                          "parallel", "str", text=True,
                          placeholder="parallel / perpendicular",
                          solution=["Both segments are horizontal, so they never meet.",
                                    "They are parallel."])
        return _num_q("One line segment joins %s to %s. Another joins %s to %s. Are the "
                      "two segments parallel or perpendicular? (type one word)"
                      % (_coord(-r, y1), _coord(r, y1),
                         _coord(x1, -r), _coord(x1, r)),
                      "perpendicular", "str", text=True,
                      placeholder="parallel / perpendicular",
                      solution=["The first segment is horizontal and the second is "
                                "vertical.",
                                "They cross at a right angle, so they are perpendicular."])

    if t == 8:                                        # pairs inside a shape
        nm, par, per = pick([("square", 2, 4), ("rectangle", 2, 4),
                             ("regular hexagon", 3, 0), ("regular octagon", 4, 0),
                             ("parallelogram", 2, 0), ("regular decagon", 5, 0)])
        ask_par = per == 0 or random.random() < 0.6
        if ask_par:
            return _num_q("How many pairs of parallel sides does %s have?" % _a(nm),
                          par, "int", unit="pairs",
                          solution=["Opposite sides of %s are parallel." % _a(nm),
                                    "There are %s." % _pl(par, "pair")])
        return _num_q("Two sides are perpendicular when they meet at a right angle. "
                      "How many corners of %s are right angles?" % _a(nm),
                      per, "int", unit="corners",
                      solution=["%s has %d right-angled corners."
                                % (_a(nm).capitalize(), per)])

    # angle between clock hands (perpendicular reasoning)
    hh, deg, word = pick([(3, 90, "perpendicular"), (9, 90, "perpendicular"),
                          (12, 0, "parallel"), (6, 180, "neither")])
    if word == "neither":
        return _num_q("At 6 o'clock the two hands of a clock point in exactly opposite "
                      "directions. How many degrees is the angle between them?",
                      180, "int", unit="degrees",
                      solution=["Opposite directions make a straight line.",
                                "A straight line is 180°."])
    if word == "parallel":
        return _num_q("At 12 o'clock the hour hand and the minute hand point in exactly "
                      "the same direction. How many degrees is the angle between them?",
                      0, "int", unit="degrees",
                      solution=["The two hands lie on top of one another.",
                                "The angle between them is 0°."])
    return _num_q("At %d o'clock the hands of a clock meet at a right angle. Are the two "
                  "hands parallel or perpendicular? (type one word)" % hh,
                  "perpendicular", "str", text=True,
                  placeholder="parallel / perpendicular",
                  solution=["Lines that meet at a right angle are perpendicular."])


@skill("Y6.8.c", "Parts of a circle", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 1, 1, 1, 1, 1, 1])
    rr = random.randint(_by_d(d, 2, 3, 4), _by_d(d, 6, 10, 15))

    if t == 0:                                        # visual: radius -> diameter
        return {"prompt": "The circle has a radius of %d cm. What is its diameter, "
                          "in cm?" % rr,
                "component": "circle",
                "spec": {"radius": rr, "show": "radius", "label": "r = %d cm" % rr},
                "answer": 2 * rr, "answer_type": "int",
                "solution": ["The diameter is twice the radius.",
                             "2 × %d = %d cm." % (rr, 2 * rr)]}

    if t == 1:                                        # visual: diameter -> radius
        dia = 2 * rr
        return {"prompt": "The circle has a diameter of %d cm. What is its radius, "
                          "in cm?" % dia,
                "component": "circle",
                "spec": {"radius": rr, "show": "diameter", "label": "d = %d cm" % dia},
                "answer": rr, "answer_type": "int",
                "solution": ["The radius is half the diameter.",
                             "%d ÷ 2 = %d cm." % (dia, rr)]}

    if t == 2:                                        # visual: name the marked part
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

    if t == 3:                                        # visual: circumference from diameter
        dia = 2 * rr
        c = round(3.14 * dia, 2)
        return {"prompt": "Take π as 3.14. The circle has a diameter of %d cm. "
                          "What is its circumference, in cm?" % dia,
                "component": "circle",
                "spec": {"radius": rr, "show": "circumference",
                         "label": "d = %d cm" % dia},
                "answer": c, "answer_type": "num", "tolerance": 0.01,
                "solution": ["Circumference = π × diameter.",
                             "3.14 × %d = %s cm." % (dia, _f(c))]}

    if t == 4:                                        # part from description (typed)
        desc, ans = pick([
            ("the distance from the centre to any point on the edge", "radius"),
            ("the distance right across the circle through the centre", "diameter"),
            ("the distance all the way round the outside of the circle",
             "circumference"),
        ])
        return _num_q("In a circle, what is the name for %s? (type one word)" % desc,
                      ans, "str", text=True,
                      placeholder="radius / diameter / circumference",
                      solution=["%s is called the %s." % (desc.capitalize(), ans)])

    if t == 5:                                        # bare radius <-> diameter
        if random.random() < 0.5:
            return _num_q("A circle has a radius of %d cm. What is its diameter, in cm?"
                          % rr,
                          2 * rr, "int", unit="cm",
                          solution=["Diameter = 2 × radius.",
                                    "2 × %d = %d cm." % (rr, 2 * rr)])
        dia = 2 * rr
        return _num_q("A circle has a diameter of %d mm. What is its radius, in mm?" % dia,
                      rr, "int", unit="mm",
                      solution=["Radius = diameter ÷ 2.",
                                "%d ÷ 2 = %d mm." % (dia, rr)])

    if t == 6:                                        # circumference from radius
        c = round(2 * 3.14 * rr, 2)
        return _num_q("Take π as 3.14. A circle has a radius of %d cm. What is its "
                      "circumference, in cm?" % rr,
                      c, "num", unit="cm", tolerance=0.01,
                      solution=["Circumference = π × diameter = π × 2 × radius.",
                                "3.14 × %d = %s cm." % (2 * rr, _f(c))])

    if t == 7:                                        # word problem: wheel
        who = pick(NAMES)
        dia = pick([40, 50, 60, 70, 80])
        turns = random.randint(2, _by_d(d, 4, 8, 20))
        c = round(3.14 * dia, 2)
        total = round(c * turns, 2)
        return _num_q("Take π as 3.14. A bicycle wheel has a diameter of %d cm. %s rides "
                      "so that the wheel turns exactly %d times. How far does the wheel "
                      "roll, in cm?" % (dia, who, turns),
                      total, "num", unit="cm", tolerance=0.05,
                      solution=["One turn covers the circumference: 3.14 × %d = %s cm."
                                % (dia, _f(c)),
                                "%s × %d = %s cm." % (_f(c), turns, _f(total))])

    if t == 8:                                        # inverse: circumference -> diameter
        dia = pick([10, 20, 30, 40, 50, 100])
        c = round(3.14 * dia, 1)
        return _num_q("Take π as 3.14. A circle has a circumference of %s cm. "
                      "What is its diameter, in cm?" % _f(c),
                      dia, "num", unit="cm", tolerance=0.1,
                      solution=["Diameter = circumference ÷ π.",
                                "%s ÷ 3.14 = %d cm." % (_f(c), dia)])

    # reasoning: comparing radius and diameter of two circles
    r1 = random.randint(3, 12)
    r2 = random.randint(3, 12)
    while r2 == r1:
        r2 = random.randint(3, 12)
    return _num_q("Circle A has a radius of %d cm. Circle B has a diameter of %d cm. "
                  "How many cm longer is the LARGER diameter?" % (r1, 2 * r2),
                  abs(2 * r1 - 2 * r2), "int", unit="cm",
                  solution=["Circle A has a diameter of 2 × %d = %d cm." % (r1, 2 * r1),
                            "Circle B has a diameter of %d cm." % (2 * r2),
                            "%d − %d = %d cm." % (max(2 * r1, 2 * r2),
                                                  min(2 * r1, 2 * r2),
                                                  abs(2 * r1 - 2 * r2))])


@skill("Y6.8.d", "3-D shapes, faces, edges, vertices and nets", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2])

    if t == 10:                                       # identify three-dimensional figures
        nm, f, e, v = pick(_SOLIDS_DRAWN)
        return {"prompt": "Identify this three-dimensional figure. What is its name? "
                          "(type the name)",
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["The figure has %d faces, %d edges and %d vertices."
                             % (f, e, v),
                             "That three-dimensional figure is %s." % _a(nm)]}

    if t == 11:                                       # which figure is being described?
        desc, nm = pick([
            ("6 square faces, 12 edges and 8 vertices", "cube"),
            ("6 rectangular faces that are not all squares", "cuboid"),
            ("5 faces, 8 edges, 5 vertices and a square base", "square-based pyramid"),
            ("2 triangular faces, 3 rectangular faces and 9 edges",
             "triangular prism"),
            ("2 flat circular faces, 1 curved surface and no vertices", "cylinder"),
            ("1 flat circular face, 1 curved surface and 1 vertex", "cone"),
            ("4 triangular faces, 6 edges and 4 vertices",
             "triangular-based pyramid"),
            ("no flat faces, no edges and no vertices", "sphere"),
        ])
        return _num_q("Which three-dimensional figure is being described? The figure has "
                      "%s. (type the name)" % desc,
                      nm, "str", text=True, placeholder="e.g. cube / cylinder",
                      solution=["Check the faces, edges and vertices of each solid.",
                                "The figure being described is %s." % _a(nm)])

    if t == 12:                                       # nets of three-dimensional figures
        key, nm, faces = pick(_NETS if d else _NETS[:4])
        ask_name = random.random() < 0.6
        if ask_name:
            return {"prompt": "Nets of three-dimensional figures can be folded up. Which "
                              "three-dimensional figure does this net fold into? "
                              "(type the name)",
                    "component": "net", "spec": {"solid": key},
                    "answer": nm, "answer_type": "str",
                    "solution": ["Imagine folding the net along every line.",
                                 "The net makes %s." % _a(nm)]}
        return {"prompt": "This is the net of a three-dimensional figure. How many flat "
                          "faces will the folded figure have?",
                "component": "net", "spec": {"solid": key},
                "answer": faces, "answer_type": "int",
                "solution": ["The net folds into %s." % _a(nm),
                             "%s has %d faces." % (_a(nm).capitalize(), faces)]}

    if t == 13:                                       # viewed from different perspectives
        desc, view, ans = pick([
            ("A cube rests on a table", "from directly above (the plan view)", "square"),
            ("A cube rests on a table", "from the front", "square"),
            ("A cylinder stands upright on its circular base",
             "from directly above (the plan view)", "circle"),
            ("A cylinder stands upright on its circular base", "from the front",
             "rectangle"),
            ("A cone stands on its circular base",
             "from directly above (the plan view)", "circle"),
            ("A cone stands on its circular base", "from the front", "triangle"),
            ("A square-based pyramid stands on its square base",
             "from directly above (the plan view)", "square"),
            ("A square-based pyramid stands on its square base", "from the front",
             "triangle"),
            ("A cuboid measuring 8 cm by 5 cm by 3 cm rests on its 8 cm by 5 cm face",
             "from directly above (the plan view)", "rectangle"),
            ("A triangular prism rests on a rectangular face with its triangular ends "
             "facing the front", "from the front", "triangle"),
            ("A triangular prism rests on a rectangular face with its triangular ends "
             "facing the front", "from directly above (the plan view)", "rectangle"),
        ])
        return _num_q("Three-dimensional figures look different when they are viewed from "
                      "different perspectives. %s. Viewed %s, what 2-D shape is seen? "
                      "(type the name)" % (desc, view),
                      ans, "str", text=True,
                      placeholder="square / rectangle / triangle / circle",
                      solution=["Picture only the outline seen from that direction.",
                                "The view is %s." % _a(ans)])

    if t == 0:                                        # net -> solid
        key, nm, faces = pick(_NETS if d else _NETS[:4])
        return {"prompt": "This is the net of a 3-D shape. Which solid does it fold "
                          "into? (type the name)",
                "component": "net", "spec": {"solid": key},
                "answer": nm, "answer_type": "str",
                "solution": ["Count the flat pieces and see how they fold together.",
                             "The net folds into %s." % _a(nm)]}

    if t == 1:                                        # net -> count faces
        key, nm, faces = pick(_NETS)
        return {"prompt": "This net folds into a 3-D shape. How many faces will the "
                          "finished solid have?",
                "component": "net", "spec": {"solid": key},
                "answer": faces, "answer_type": "int",
                "solution": ["Each piece of the net becomes one face.",
                             "%s has %d faces." % (_a(nm).capitalize(), faces)]}

    if t == 2:                                        # net -> edges or vertices
        key, nm, faces = pick(_NETS[:4])
        f, e, v = [s for s in _SOLIDS_DRAWN if s[0] == nm][0][1:]
        ask = pick(["edges", "vertices"])
        return {"prompt": "This net folds into a 3-D shape. How many %s will the "
                          "finished solid have?" % ask,
                "component": "net", "spec": {"solid": key},
                "answer": e if ask == "edges" else v, "answer_type": "int",
                "solution": ["The net folds into %s." % _a(nm),
                             "%s has %d %s." % (_a(nm).capitalize(),
                                                e if ask == "edges" else v, ask)]}

    if t == 3:                                        # solid drawing -> count
        nm, f, e, v = pick(_SOLIDS_DRAWN)
        ask = pick(["faces", "edges", "vertices"])
        ans = {"faces": f, "edges": e, "vertices": v}[ask]
        return {"prompt": "How many %s does this solid have?" % ask,
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": ask},
                "answer": ans, "answer_type": "int",
                "solution": ["A face is a flat surface, an edge is where two faces meet "
                             "and a vertex is a corner.",
                             "%s has %d %s." % (_a(nm).capitalize(), ans, ask)]}

    if t == 4:                                        # solid drawing -> name
        nm, f, e, v = pick(_SOLIDS_DRAWN)
        return {"prompt": "What is the name of this 3-D shape? (type the name)",
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["It has %d faces, %d edges and %d vertices." % (f, e, v),
                             "It is %s." % _a(nm)]}

    if t == 5:                                        # named recall
        nm, f, e, v = pick(_SOLIDS_ALL if d else _SOLIDS_DRAWN)
        ask = pick(["faces", "edges", "vertices"])
        ans = {"faces": f, "edges": e, "vertices": v}[ask]
        extra = (" (count the curved surface as a face)"
                 if ask == "faces" and nm in ("cylinder", "cone", "sphere") else "")
        return _num_q("How many %s does %s have?%s" % (ask, _a(nm), extra),
                      ans, "int", unit=ask,
                      solution=["%s has %d %s." % (_a(nm).capitalize(), ans,
                                                   {"faces": "face", "edges": "edge", "vertices": "vertex"}[ask] if ans == 1 else ask)])

    if t == 6:                                        # Euler's rule
        nm, f, e, v = pick([s for s in _SOLIDS_ALL if s[0] not in
                            ("cylinder", "cone", "sphere")])
        missing = pick(["faces", "edges", "vertices"])
        if missing == "faces":
            return _num_q("For solids with flat faces, faces + vertices − edges = 2. "
                          "A solid has %d vertices and %d edges. How many faces does it "
                          "have?" % (v, e),
                          f, "int", unit="faces",
                          solution=["faces = 2 + edges − vertices.",
                                    "2 + %d − %d = %d faces." % (e, v, f)])
        if missing == "vertices":
            return _num_q("For solids with flat faces, faces + vertices − edges = 2. "
                          "A solid has %d faces and %d edges. How many vertices does it "
                          "have?" % (f, e),
                          v, "int", unit="vertices",
                          solution=["vertices = 2 + edges − faces.",
                                    "2 + %d − %d = %d vertices." % (e, f, v)])
        return _num_q("For solids with flat faces, faces + vertices − edges = 2. "
                      "A solid has %d faces and %d vertices. How many edges does it "
                      "have?" % (f, v),
                      e, "int", unit="edges",
                      solution=["edges = faces + vertices − 2.",
                                "%d + %d − 2 = %d edges." % (f, v, e)])

    if t == 7:                                        # description -> name
        desc, nm = pick([
            ("6 square faces, all the same size", "cube"),
            ("6 rectangular faces", "cuboid"),
            ("a square base and 4 triangular faces meeting at a point",
             "square-based pyramid"),
            ("2 triangular faces and 3 rectangular faces", "triangular prism"),
            ("2 flat circular faces and 1 curved surface", "cylinder"),
            ("1 flat circular face, 1 curved surface and 1 vertex", "cone"),
            ("4 triangular faces", "triangular-based pyramid"),
        ])
        return _num_q("A 3-D shape has %s. What is it called? (type the name)" % desc,
                      nm, "str", text=True, placeholder=_NET_NAMES,
                      solution=["A solid with %s is %s." % (desc, _a(nm))])

    if t == 8:                                        # combined count
        (n1, f1, e1, v1), (n2, f2, e2, v2) = random.sample(_SOLIDS_DRAWN, 2)
        ask, a1, a2 = pick([("faces", f1, f2), ("edges", e1, e2),
                            ("vertices", v1, v2)])
        return _num_q("%s and %s are placed side by side. How many %s do the two solids "
                      "have altogether?" % (_a(n1).capitalize(), _a(n2), ask),
                      a1 + a2, "int", unit=ask,
                      solution=["%s has %d and %s has %d."
                                % (_a(n1).capitalize(), a1, _a(n2), a2),
                                "%d + %d = %d." % (a1, a2, a1 + a2)])

    # net of a cube: how much card
    side = random.randint(3, _by_d(d, 6, 10, 15))
    return _num_q("A net of a cube is cut from card. Each square face has sides of "
                  "%d cm. What is the total area of card used, in cm²?" % side,
                  6 * side * side, "int", unit="cm²",
                  solution=["One face has an area of %d × %d = %d cm²."
                            % (side, side, side * side),
                            "A cube has 6 faces: 6 × %d = %d cm²."
                            % (side * side, 6 * side * side)])


@skill("Y6.8.e", "Measure and classify angles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1])

    if t == 10:                                       # estimate without a protractor
        deg = random.choice([20, 30, 40, 50, 60, 70, 80, 100, 110, 120, 130, 140, 150, 160])
        return {"prompt": "Estimate the size of this angle in degrees, without a protractor. "
                          "(Your estimate must be within 10° of the real size.)",
                "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True},
                "answer": deg, "answer_type": "int", "tolerance": 10,
                "solution": ["Compare it with a right angle (90°) and a straight line (180°).",
                             "The angle is %d°." % deg]}

    if t == 11:                                       # fractions of a turn
        num, den = pick([(1, 3), (2, 3), (1, 6), (1, 8), (3, 8), (5, 6), (1, 12), (5, 12), (1, 5), (2, 5)])
        return _num_q("A full turn is 360°. How many degrees is %d/%d of a turn?" % (num, den), 360 * num // den, "int",
                      unit="degrees", solution=["360 ÷ %d = %d." % (den, 360 // den),
                                                "%d × %d = %d°." % (num, 360 // den, 360 * num // den)])

    if t == 12:                                       # compass turns
        dirs = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
        s0 = random.randrange(8)
        k = random.randint(1, 7)
        cw = random.random() < 0.5
        end = dirs[(s0 + (k if cw else -k)) % 8]
        return _num_q("You face %s and turn %d° %s. Which direction do you face now?"
                      % (dirs[s0], 45 * k, "clockwise" if cw else "anticlockwise"), end, "str", text=True,
                      placeholder="e.g. south-west",
                      solution=["Each 45° turn moves one compass point.",
                                "%d ÷ 45 = %s %s, so you face %s." % (45 * k, _pl(k, "point"), "clockwise" if cw else "anticlockwise", end)])

    if t == 0:                                        # measure with a protractor
        deg = random.choice(_by_d(d, [30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
                                  [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130,
                                   140, 150],
                                  [15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125,
                                   135, 145, 155, 165]))
        return {"prompt": "Use the protractor to measure this angle. "
                          "How many degrees is it?",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": deg, "answer_type": "int", "tolerance": 2,
                "solution": ["Line the protractor's centre up with the point of the "
                             "angle and read the scale that starts at 0.",
                             "The angle measures %d°." % deg]}

    if t == 1:                                        # classify a drawn angle
        kind = pick(_by_d(d, ["acute", "right", "obtuse"],
                          ["acute", "right", "obtuse", "reflex"],
                          ["acute", "right", "obtuse", "straight", "reflex"]))
        deg = {"acute": lambda: random.choice([15, 25, 35, 45, 55, 65, 75, 85]),
               "right": lambda: 90,
               "obtuse": lambda: random.choice([95, 105, 120, 135, 145, 160, 175]),
               "straight": lambda: 180,
               "reflex": lambda: random.choice([190, 210, 235, 260, 285, 310, 340])}[kind]()
        return {"prompt": "Look at the angle. Is it acute, right, obtuse, straight or "
                          "reflex? (type one word)",
                "component": "angle", "spec": {"mode": "classify", "degrees": deg},
                "answer": kind, "answer_type": "str",
                "solution": ["Acute is under 90°, right is exactly 90°, obtuse is "
                             "between 90° and 180°, straight is 180° and reflex is "
                             "over 180°.",
                             "This angle is %d°, so it is %s." % (deg, kind)]}

    if t == 2:                                        # measure, then classify
        deg = random.choice([35, 55, 75, 100, 125, 145, 160])
        return {"prompt": "Measure this angle with the protractor and write its size in "
                          "degrees.",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": deg, "answer_type": "int", "tolerance": 2,
                "solution": ["Read the scale where the second ray crosses it.",
                             "The angle is %d°, which is %s."
                             % (deg, "acute" if deg < 90 else "obtuse")]}

    if t == 3:                                        # classify from a number
        deg = random.choice(_by_d(d, [15, 35, 55, 75, 90, 95, 120, 145],
                                  [15, 35, 55, 75, 89, 90, 95, 120, 145, 179, 180,
                                   200, 260, 300],
                                  [1, 44, 89, 90, 91, 179, 180, 181, 269, 359]))
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
                      "reflex? (type one word)" % deg,
                      kind, "str", text=True,
                      placeholder="acute / right / obtuse / straight / reflex",
                      solution=["Acute < 90°, right = 90°, obtuse is between 90° and "
                                "180°, straight = 180°, reflex > 180°.",
                                "%d° is %s." % (deg, kind)])

    if t == 4:                                        # reflex partner
        deg = random.choice([20, 35, 50, 65, 80, 100, 115, 130, 150, 170])
        return _num_q("An angle of %d° is drawn. Angles all the way round a point add up "
                      "to 360°. How many degrees is the reflex angle on the other side "
                      "of the two rays?" % deg,
                      360 - deg, "int", unit="degrees",
                      solution=["The two angles together make a full turn of 360°.",
                                "360 − %d = %d°." % (deg, 360 - deg)])

    if t == 5:                                        # smallest / largest
        angs = random.sample([15, 40, 65, 88, 92, 118, 140, 175, 205, 250, 300], 4)
        want_big = random.random() < 0.5
        return _num_q("Four angles measure %s. Write the size of the %s angle."
                      % (", ".join("%d°" % a for a in angs),
                         "LARGEST" if want_big else "SMALLEST"),
                      max(angs) if want_big else min(angs), "int", unit="degrees",
                      solution=["Put the sizes in order: %s."
                                % ", ".join("%d" % a for a in sorted(angs)),
                                "The %s is %d°." % ("largest" if want_big else "smallest",
                                                    max(angs) if want_big else min(angs))])

    if t == 6:                                        # how many acute in a list
        angs = random.sample([12, 28, 45, 63, 81, 90, 104, 132, 168, 195, 240, 310], 5)
        cnt = sum(1 for a in angs if a < 90)
        return _num_q("Five angles measure %s. How many of them are acute?"
                      % ", ".join("%d°" % a for a in angs),
                      cnt, "int", unit="angles",
                      solution=["An acute angle is less than 90°.",
                                "%s %s under 90°, so the answer is %d."
                                % (", ".join("%d" % a for a in angs if a < 90) or "No angles",
                                   "are" if cnt != 1 else "is", cnt)])

    if t == 7:                                        # turn
        deg = pick([45, 90, 135, 180, 225, 270, 315, 360])
        return {"prompt": "The arrow shows a turn. How many degrees is the turn?",
                "component": "angle", "spec": {"mode": "turn", "degrees": deg},
                "answer": deg, "answer_type": "int",
                "solution": ["A quarter turn is 90° and a full turn is 360°.",
                             "This turn is %d°." % deg]}

    if t == 8:                                        # difference between two angles
        a, b = random.sample([25, 40, 55, 70, 85, 95, 110, 130, 150, 165, 200, 250], 2)
        return _num_q("One angle measures %d° and another measures %d°. How many degrees "
                      "BIGGER is the larger angle?" % (a, b),
                      abs(a - b), "int", unit="degrees",
                      solution=["%d − %d = %d°." % (max(a, b), min(a, b), abs(a - b))])

    # clock hands angle
    mins = pick([5, 10, 15, 20, 25, 30, 40, 45, 50])
    return _num_q("The minute hand of a clock goes all the way round in 60 minutes. "
                  "How many degrees does the minute hand turn in %d minutes?" % mins,
                  6 * mins, "int", unit="degrees",
                  solution=["360 ÷ 60 = 6°, so the minute hand turns 6° each minute.",
                            "6 × %d = %d°." % (mins, 6 * mins)])


@skill("Y6.8.f", "Angles on a line, at a point, and vertically opposite", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 2])

    if t == 10:                                       # vertical angles
        a = random.randint(_by_d(d, 25, 15, 11), _by_d(d, 155, 165, 169))
        return _num_q("Two straight lines cross at a point. The two angles opposite each "
                      "other at that point are called vertical angles (or vertically "
                      "opposite angles), and vertical angles are always equal. One of a "
                      "pair of vertical angles measures %d°. Find the missing angle: how "
                      "many degrees is the other vertical angle?" % a,
                      a, "int", unit="degrees",
                      solution=["Vertical angles are equal.",
                                "The missing vertical angle is also %d°." % a])

    if t == 11:                                       # adjacent angles
        total = random.randint(_by_d(d, 80, 100, 120), _by_d(d, 150, 170, 180))
        a = random.randint(20, total - 20)
        return _num_q("Two adjacent angles share a vertex and one arm. Together the two "
                      "adjacent angles make an angle of %d°. One of the adjacent angles "
                      "is %d°. Find the missing angle: how many degrees is the other "
                      "adjacent angle?" % (total, a),
                      total - a, "int", unit="degrees",
                      solution=["The two adjacent angles add up to %d°." % total,
                                "%d − %d = %d°." % (total, a, total - a)])

    if t == 12:                                       # supplementary angles
        a = random.randint(_by_d(d, 25, 15, 11), _by_d(d, 155, 165, 169))
        return _num_q("Two angles are supplementary when they add up to 180°. One of a "
                      "pair of supplementary angles is %d°. Find the missing angle: how "
                      "many degrees is the other supplementary angle?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["Supplementary angles add up to 180°.",
                                "180 − %d = %d°." % (a, 180 - a)])

    if t == 13:                                       # complementary angles
        a = random.randint(_by_d(d, 15, 10, 6), _by_d(d, 75, 80, 84))
        return _num_q("Two angles are complementary when they add up to 90°. One of a "
                      "pair of complementary angles is %d°. Find the missing angle: how "
                      "many degrees is the other complementary angle?" % a,
                      90 - a, "int", unit="degrees",
                      solution=["Complementary angles add up to 90°.",
                                "90 − %d = %d°." % (a, 90 - a)])

    if t == 14:                                       # vertical, adjacent and supplementary
        a = random.randint(_by_d(d, 30, 20, 15), _by_d(d, 150, 160, 165))
        step = pick(["vertical", "supplementary"])
        if step == "vertical":
            return _num_q("Two straight lines cross. The angle marked x is %d°. The angle "
                          "y is adjacent to x on a straight line, so x and y are "
                          "supplementary. The angle z is vertically opposite y. How many "
                          "degrees is z?" % a,
                          180 - a, "int", unit="degrees",
                          solution=["x and y are supplementary: 180 − %d = %d°."
                                    % (a, 180 - a),
                                    "z is vertical to y, so z = y = %d°." % (180 - a)])
        return _num_q("Two straight lines cross. The angle marked x is %d°. The angle y "
                      "is vertically opposite x, and the angle z is adjacent to y on a "
                      "straight line. How many degrees is z?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["Vertical angles are equal, so y = %d°." % a,
                                "z and y are supplementary: 180 − %d = %d°."
                                % (a, 180 - a)])

    if t == 15:                                       # name the relationship
        want = pick(["supplementary", "complementary"])
        tot = 180 if want == "supplementary" else 90
        a = random.randint(20, tot - 20)
        return _num_q("Angles that add up to 90° are complementary and angles that add up "
                      "to 180° are supplementary. One angle is %d° and another angle is "
                      "%d°. Are the two angles complementary or supplementary? "
                      "(type one word)" % (a, tot - a),
                      want, "str", text=True,
                      placeholder="complementary / supplementary",
                      solution=["%d + %d = %d°." % (a, tot - a, tot),
                                "Angles that add up to %d° are %s." % (tot, want)])

    if t == 0:                                        # visual: measure then complete 180
        deg = random.choice([30, 40, 50, 60, 70, 80, 100, 110, 120, 130, 140, 150])
        return {"prompt": "Measure the angle shown. It sits on a straight line next to a "
                          "second angle. How many degrees is the second angle?",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": 180 - deg, "answer_type": "int", "tolerance": 2,
                "solution": ["The angle shown measures %d°." % deg,
                             "Angles on a straight line add up to 180°.",
                             "180 − %d = %d°." % (deg, 180 - deg)]}

    if t == 1:                                        # visual: measure then complete 360
        deg = random.choice([40, 60, 80, 100, 120, 140, 160])
        return {"prompt": "Measure the angle shown. Another angle joins it to make a full "
                          "turn round the point. How many degrees is that other angle?",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": 360 - deg, "answer_type": "int", "tolerance": 2,
                "solution": ["The angle shown measures %d°." % deg,
                             "Angles at a point add up to 360°.",
                             "360 − %d = %d°." % (deg, 360 - deg)]}

    if t == 2:                                        # two angles on a line
        a = random.randint(_by_d(d, 20, 15, 11), _by_d(d, 160, 165, 169))
        return _num_q("Two angles sit side by side on a straight line. One of them is "
                      "%d°. How many degrees is the other?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["Angles on a straight line add up to 180°.",
                                "180 − %d = %d°." % (a, 180 - a)])

    if t == 3:                                        # three angles on a line
        a = random.randint(20, 70)
        b = random.randint(20, 170 - a)
        c = 180 - a - b
        return _num_q("Three angles sit side by side on a straight line. Two of them are "
                      "%d° and %d°. How many degrees is the third?" % (a, b),
                      c, "int", unit="degrees",
                      solution=["Angles on a straight line add up to 180°.",
                                "%d + %d = %d, and 180 − %d = %d°."
                                % (a, b, a + b, a + b, c)])

    if t == 4:                                        # angles at a point
        n = _by_d(d, 2, 3, 4)
        angs = [random.randint(35, 110) for _ in range(n)]
        while not (60 <= sum(angs) <= 330):
            angs = [random.randint(35, 110) for _ in range(n)]
        rest = 360 - sum(angs)
        return _num_q("Angles at a point add up to 360°. Angles of %s and one more angle "
                      "meet at a point. How many degrees is the last angle?"
                      % ", ".join("%d°" % v for v in angs),
                      rest, "int", unit="degrees",
                      solution=["%s = %d°."
                                % (" + ".join("%d" % v for v in angs), sum(angs)),
                                "360 − %d = %d°." % (sum(angs), rest)])

    if t == 5:                                        # vertically opposite
        a = random.randint(20, 160)
        ask_opp = random.random() < 0.5
        if ask_opp:
            return _num_q("Two straight lines cross. One of the four angles made is %d°. "
                          "How many degrees is the angle vertically opposite it?" % a,
                          a, "int", unit="degrees",
                          solution=["Vertically opposite angles are equal.",
                                    "So the opposite angle is also %d°." % a])
        return _num_q("Two straight lines cross. One of the four angles made is %d°. "
                      "How many degrees is the angle NEXT to it?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["The two angles next to each other lie on a straight line.",
                                "180 − %d = %d°." % (a, 180 - a)])

    if t == 6:                                        # two equal angles on a line
        rest = pick([20, 30, 40, 50, 60, 70, 80, 90, 100])
        each = (180 - rest) // 2
        rest = 180 - 2 * each
        return _num_q("Three angles sit on a straight line. One is %d° and the other two "
                      "are equal to each other. How many degrees is each of the equal "
                      "angles?" % rest,
                      each, "int", unit="degrees",
                      solution=["180 − %d = %d° is shared by the two equal angles."
                                % (rest, 180 - rest),
                                "%d ÷ 2 = %d°." % (180 - rest, each)])

    if t == 7:                                        # equal angles at a point
        n = pick([3, 4, 5, 6, 8])
        return _num_q("%d equal angles meet at a point and fill the whole turn. "
                      "How many degrees is each angle?" % n,
                      360 // n, "int", unit="degrees",
                      solution=["Angles at a point add up to 360°.",
                                "360 ÷ %d = %d°." % (n, 360 // n)])

    if t == 8:                                        # multi-step: line + point
        a = random.randint(30, 120)
        b = random.randint(30, 120)
        # angles at a point are a, b, (180 - a) and c, so c = 180 - b
        c = 180 - b
        return _num_q("Four angles meet at a point. Two of them are %d° and %d°. "
                      "A third is on a straight line with the %d° angle. How many degrees "
                      "is the fourth angle?" % (a, b, a),
                      c, "int", unit="degrees",
                      solution=["The third angle is 180 − %d = %d°." % (a, 180 - a),
                                "So far: %d + %d + %d = %d°."
                                % (a, b, 180 - a, a + b + 180 - a),
                                "360 − %d = %d°." % (180 + b, c)])

    # reasoning: is it possible?
    vals, ok = pick([([70, 60, 40], False), ([90, 55, 35], True),
                     ([120, 60], True), ([100, 90], False),
                     ([45, 45, 90], True), ([80, 80, 30], False)])
    return _num_q("These angles are said to sit side by side on a straight line: %s. "
                  "Is that possible? (type yes or no)"
                  % ", ".join("%d°" % v for v in vals),
                  "yes" if ok else "no", "str", text=True, placeholder="yes / no",
                  solution=["%s = %d°." % (" + ".join("%d" % v for v in vals), sum(vals)),
                            "Angles on a straight line must total 180°, so the answer "
                            "is %s." % ("yes" if ok else "no")])


@skill("Y6.8.g", "Angles in a triangle", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 2, 3, 3])

    if t == 13:                                       # rotational symmetry: amount of rotation
        nm, order = pick([("equilateral triangle", 3), ("square", 4),
                          ("regular pentagon", 5), ("regular hexagon", 6),
                          ("regular octagon", 8), ("rectangle", 2),
                          ("parallelogram", 2), ("regular decagon", 10)])
        return _num_q("A shape has rotational symmetry when it fits onto itself as it is "
                      "turned. %s has rotational symmetry of order %d. What is the "
                      "smallest amount of rotation, in degrees, that turns it onto itself?"
                      % (_a(nm).capitalize(), order),
                      360 // order, "int", unit="degrees",
                      solution=["A full turn is 360° and the shape fits onto itself %d "
                                "times in a full turn." % order,
                                "360 ÷ %d = %d°." % (order, 360 // order)])

    if t == 14:                                       # amount of rotation -> order
        order = pick([2, 3, 4, 5, 6, 8])
        ask_order = random.random() < 0.5
        if ask_order:
            return _num_q("A shape has rotational symmetry. The smallest amount of "
                          "rotation that turns the shape onto itself is %d°. What is the "
                          "order of rotational symmetry of the shape?" % (360 // order),
                          order, "int",
                          solution=["360 ÷ %d = %d." % (360 // order, order),
                                    "The order of rotational symmetry is %d." % order])
        turns = pick([2, 3])
        return _num_q("A shape has rotational symmetry of order %d, so the smallest amount "
                      "of rotation that turns it onto itself is %d°. Through how many "
                      "degrees has the shape turned after %d of these smallest rotations?"
                      % (order, 360 // order, turns),
                      turns * (360 // order), "int", unit="degrees",
                      solution=["Each rotation is 360 ÷ %d = %d°."
                                % (order, 360 // order),
                                "%d × %d = %d°." % (turns, 360 // order,
                                                    turns * (360 // order))])

    if t == 10:                                       # visual: measure, then find the third
        a = random.choice([30, 40, 50, 60, 70, 80])
        deg = random.choice([30, 40, 50, 60, 70, 80, 100, 110])
        third = 180 - a - deg
        while third < 10:
            deg = random.choice([30, 40, 50, 60])
            third = 180 - a - deg
        return {"prompt": "The angle shown is one angle of a triangle. Another angle of "
                          "the same triangle is %d°. Measure the angle shown, then work "
                          "out the third angle of the triangle, in degrees." % a,
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": third, "answer_type": "int", "tolerance": 2,
                "solution": ["The angle shown measures %d°." % deg,
                             "The angles of a triangle add up to 180°.",
                             "180 − (%d + %d) = %d°." % (deg, a, third)]}

    if t == 11:                                       # visual: isosceles from a drawn apex
        deg = random.choice([20, 30, 40, 50, 60, 70, 80, 100, 120, 140])
        base = (180 - deg) // 2
        return {"prompt": "The angle shown is the top angle of an isosceles triangle "
                          "whose two base angles are equal. Measure the angle shown, then "
                          "work out one base angle, in degrees.",
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": base, "answer_type": "int", "tolerance": 2,
                "solution": ["The angle shown measures %d°." % deg,
                             "180 − %d = %d° is shared by the two equal base angles."
                             % (deg, 180 - deg),
                             "%d ÷ 2 = %d°." % (180 - deg, base)]}

    if t == 12:                                       # visual: equilateral triangle
        return {"prompt": "This triangle has three equal sides and three equal angles. "
                          "How many degrees is each angle?",
                "component": "shape",
                "spec": {"kind": "2d", "name": "triangle", "ask": "vertices"},
                "answer": 60, "answer_type": "int",
                "solution": ["The angles of a triangle add up to 180°.",
                             "180 ÷ 3 = 60°."]}

    if t == 0:                                        # two given, find the third
        a = random.randint(_by_d(d, 30, 20, 11), _by_d(d, 80, 100, 130))
        b = random.randint(_by_d(d, 30, 20, 11), 170 - a)
        c = 180 - a - b
        return _num_q("Two angles of a triangle are %d° and %d°. What is the third "
                      "angle, in degrees?" % (a, b),
                      c, "int", unit="degrees",
                      solution=["The angles of a triangle add up to 180°.",
                                "%d + %d = %d, and 180 − %d = %d°."
                                % (a, b, a + b, a + b, c)])

    if t == 1:                                        # right-angled triangle
        a = random.randint(15, 75)
        return _num_q("A right-angled triangle has one angle of 90° and another of %d°. "
                      "What is the third angle, in degrees?" % a,
                      90 - a, "int", unit="degrees",
                      solution=["The angles add up to 180° and one of them is 90°.",
                                "180 − 90 = 90, and 90 − %d = %d°." % (a, 90 - a)])

    if t == 2:                                        # isosceles: apex -> base
        base = random.randint(35, 85)
        apex = 180 - 2 * base
        return _num_q("An isosceles triangle has an angle of %d° at the top and two equal "
                      "angles at the base. How many degrees is each base angle?" % apex,
                      base, "int", unit="degrees",
                      solution=["180 − %d = %d° is shared by the two equal angles."
                                % (apex, 180 - apex),
                                "%d ÷ 2 = %d°." % (180 - apex, base)])

    if t == 3:                                        # isosceles: base -> apex
        base = random.randint(30, 80)
        apex = 180 - 2 * base
        return _num_q("An isosceles triangle has two equal base angles of %d° each. "
                      "How many degrees is the angle at the top?" % base,
                      apex, "int", unit="degrees",
                      solution=["%d + %d = %d°." % (base, base, 2 * base),
                                "180 − %d = %d°." % (2 * base, apex)])

    if t == 4:                                        # equilateral
        return _num_q("All three angles of an equilateral triangle are equal. "
                      "How many degrees is each angle?",
                      60, "int", unit="degrees",
                      solution=["The angles of a triangle add up to 180°.",
                                "180 ÷ 3 = 60°."])

    if t == 5:                                        # classify from two angles
        a = random.randint(20, 100)
        b = random.randint(20, min(150, 175 - a))
        c = 180 - a - b
        while c < 5:
            a = random.randint(20, 100)
            b = random.randint(20, min(150, 175 - a))
            c = 180 - a - b
        biggest = max(a, b, c)
        kind = "right" if biggest == 90 else ("obtuse" if biggest > 90 else "acute")
        return _num_q("Two angles of a triangle are %d° and %d°. Work out the third "
                      "angle, then say whether the triangle is acute, right or obtuse. "
                      "(type one word)" % (a, b),
                      kind, "str", text=True, placeholder="acute / right / obtuse",
                      solution=["The third angle is 180 − %d = %d°." % (a + b, c),
                                "The largest angle is %d°, so the triangle is %s."
                                % (biggest, kind)])

    if t == 6:                                        # ratio of angles
        k = pick([1, 2, 3, 4, 5, 6])
        mult = pick([[1, 2, 3], [1, 1, 4], [2, 3, 4], [1, 3, 5], [1, 2, 2]])
        unit = 180 // sum(mult)
        if 180 % sum(mult) != 0:
            mult = [1, 2, 3]
            unit = 30
        angs = [m * unit for m in mult]
        want = random.randrange(3)
        return _num_q("The three angles of a triangle are in the ratio %s. "
                      "How many degrees is the %s angle in that ratio?"
                      % (" : ".join(str(m) for m in mult),
                         ["first", "second", "third"][want]),
                      angs[want], "int", unit="degrees",
                      solution=["The ratio has %d parts altogether and 180 ÷ %d = %d°."
                                % (sum(mult), sum(mult), unit),
                                "%d × %d = %d°." % (mult[want], unit, angs[want])])

    if t == 7:                                        # exterior angle
        a = random.randint(30, 80)
        b = random.randint(30, 80)
        c = 180 - a - b
        ext = 180 - c
        return _num_q("Two angles of a triangle are %d° and %d°. The third angle sits on "
                      "a straight line with an angle outside the triangle. How many "
                      "degrees is that outside angle?" % (a, b),
                      ext, "int", unit="degrees",
                      solution=["The third angle is 180 − %d = %d°." % (a + b, c),
                                "180 − %d = %d°." % (c, ext)])

    if t == 8:                                        # possible or not
        vals, ok = pick([([60, 70, 50], True), ([90, 45, 45], True),
                         ([100, 50, 40], False), ([80, 60, 30], False),
                         ([120, 30, 30], True), ([45, 45, 45], False)])
        return _num_q("Could a triangle have angles of %s? (type yes or no)"
                      % ", ".join("%d°" % v for v in vals),
                      "yes" if ok else "no", "str", text=True, placeholder="yes / no",
                      solution=["%s = %d°."
                                % (" + ".join("%d" % v for v in vals), sum(vals)),
                                "A triangle's angles must total exactly 180°, so the "
                                "answer is %s." % ("yes" if ok else "no")])

    # word problem
    who = pick(NAMES)
    a = random.randint(25, 70)
    b = a + random.randint(10, 40)
    c = 180 - a - b
    return _num_q("%s draws a triangle. The smallest angle is %d° and the next angle is "
                  "%d° larger than the smallest. How many degrees is the largest angle?"
                  % (who, a, b - a),
                  c, "int", unit="degrees",
                  solution=["The second angle is %d + %d = %d°." % (a, b - a, b),
                            "180 − (%d + %d) = 180 − %d = %d°." % (a, b, a + b, c)])


@skill("Y6.8.h", "Angles in a quadrilateral", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 4, 2, 3, 3, 3])

    if t == 12:                                       # identify rhombuses
        case, ans = pick([
            ("has four equal sides and two pairs of parallel sides", "yes"),
            ("has four equal sides and four right angles", "yes"),
            ("has four right angles but its sides are 8 cm, 5 cm, 8 cm and 5 cm", "no"),
            ("has exactly one pair of parallel sides", "no"),
            ("has sides of 6 cm, 6 cm, 6 cm and 6 cm", "yes"),
            ("has sides of 7 cm, 7 cm, 4 cm and 4 cm with no parallel sides", "no"),
            ("has two pairs of parallel sides with sides of 9 cm, 5 cm, 9 cm and 5 cm",
             "no"),
        ])
        return _num_q("A rhombus is a quadrilateral with four equal sides. Identify "
                      "whether this quadrilateral is a rhombus: the quadrilateral %s. "
                      "(type yes or no)" % case,
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["Check whether all four sides are equal in length.",
                                "The answer is %s." % ans])

    if t == 13:                                       # relationships between quadrilaterals
        stmt, ans = pick([
            ("A square is a rhombus", "always"),
            ("A square is a rectangle", "always"),
            ("A rectangle is a square", "sometimes"),
            ("A rhombus is a square", "sometimes"),
            ("A rhombus is a parallelogram", "always"),
            ("A parallelogram is a rhombus", "sometimes"),
            ("A rectangle is a parallelogram", "always"),
            ("A square is a parallelogram", "always"),
            ("A parallelogram is a quadrilateral", "always"),
            ("A trapezium is a quadrilateral", "always"),
            ("A quadrilateral is a triangle", "never"),
            ("A rhombus is a pentagon", "never"),
        ])
        return _num_q("Think about the relationships between quadrilaterals. “%s.” Is "
                      "this always, sometimes or never true? (type one word)" % stmt,
                      ans, "str", text=True, placeholder="always / sometimes / never",
                      solution=["Ask whether every shape of the first kind must also be "
                                "a shape of the second kind.",
                                "The statement is %s true." % ans])

    if t == 14:                                       # describe relationships among quads
        desc, nm = pick([
            ("a rhombus with four right angles", "square"),
            ("a rectangle with four equal sides", "square"),
            ("a parallelogram with four equal sides and no right angles", "rhombus"),
            ("a parallelogram with four right angles and sides that are not all equal",
             "rectangle"),
            ("a quadrilateral with exactly one pair of parallel sides", "trapezium"),
            ("a quadrilateral with two pairs of parallel sides and no right angles, "
             "whose sides are not all equal", "parallelogram"),
        ])
        return _num_q("Quadrilaterals can be described using their relationships to one "
                      "another. Which quadrilateral is %s? (type the name)" % desc,
                      nm, "str", text=True, placeholder=_QUAD_NAMES,
                      solution=["%s is %s." % (_a(nm).capitalize(), desc)])

    if t == 10:                                       # visual: measure, then find the rest
        deg = random.choice([50, 60, 70, 80, 100, 110, 120, 130])
        a = random.randint(60, 120)
        b = random.randint(60, 120)
        rest = 360 - deg - a - b
        while not (20 <= rest <= 200):
            a = random.randint(60, 120)
            b = random.randint(60, 120)
            rest = 360 - deg - a - b
        return {"prompt": "The angle shown is one angle of a quadrilateral. Two of the "
                          "other angles are %d° and %d°. Measure the angle shown, then "
                          "work out the fourth angle, in degrees." % (a, b),
                "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True},
                "answer": rest, "answer_type": "int", "tolerance": 2,
                "solution": ["The angle shown measures %d°." % deg,
                             "The angles of a quadrilateral add up to 360°.",
                             "360 − (%d + %d + %d) = %d°." % (deg, a, b, rest)]}

    if t == 11:                                       # visual: regular polygon angle
        nm = pick(["square", "rectangle"])
        return {"prompt": "Every corner of this quadrilateral is a right angle. "
                          "How many degrees do its four angles add up to?",
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "vertices",
                         "marks": "right_angle"},
                "answer": 360, "answer_type": "int",
                "solution": ["4 × 90 = 360°.",
                             "Any quadrilateral's angles add up to 360°."]}

    if t == 0:                                       # three given, find the fourth
        a = random.randint(50, 130)
        b = random.randint(50, 130)
        c = random.randint(50, 130)
        rest = 360 - a - b - c
        while not (20 <= rest <= 200):
            a, b, c = (random.randint(50, 130), random.randint(50, 130),
                       random.randint(50, 130))
            rest = 360 - a - b - c
        return _num_q("Three angles of a quadrilateral are %d°, %d° and %d°. "
                      "What is the fourth angle, in degrees?" % (a, b, c),
                      rest, "int", unit="degrees",
                      solution=["The angles of a quadrilateral add up to 360°.",
                                "%d + %d + %d = %d, and 360 − %d = %d°."
                                % (a, b, c, a + b + c, a + b + c, rest)])

    if t == 1:                                        # two given, other two equal
        a = random.randint(60, 130)
        b = random.randint(60, 130)
        each = (360 - a - b) // 2
        b = 360 - a - 2 * each
        return _num_q("A quadrilateral has angles of %d° and %d°. The other two angles "
                      "are equal to each other. How many degrees is each of them?"
                      % (a, b),
                      each, "int", unit="degrees",
                      solution=["360 − (%d + %d) = %d° is shared by the two equal angles."
                                % (a, b, 360 - a - b),
                                "%d ÷ 2 = %d°." % (360 - a - b, each)])

    if t == 2:                                        # parallelogram
        a = random.randint(35, 145)
        ask_opp = random.random() < 0.5
        if ask_opp:
            return _num_q("In a parallelogram, opposite angles are equal. One angle is "
                          "%d°. How many degrees is the angle opposite it?" % a,
                          a, "int", unit="degrees",
                          solution=["Opposite angles of a parallelogram are equal.",
                                    "So the opposite angle is %d°." % a])
        return _num_q("In a parallelogram the four angles add up to 360° and opposite "
                      "angles are equal. One angle is %d°. How many degrees is an angle "
                      "next to it?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["Two angles of %d° use up %d°." % (a, 2 * a),
                                "360 − %d = %d° for the other two, and %d ÷ 2 = %d°."
                                % (2 * a, 360 - 2 * a, 360 - 2 * a, 180 - a)])

    if t == 3:                                        # kite
        top = random.randint(50, 130)
        bottom = random.randint(40, 120)
        each = (360 - top - bottom) // 2
        bottom = 360 - top - 2 * each
        return _num_q("A kite has one angle of %d° at the top and one of %d° at the "
                      "bottom. The two side angles are equal. How many degrees is each "
                      "side angle?" % (top, bottom),
                      each, "int", unit="degrees",
                      solution=["360 − (%d + %d) = %d°." % (top, bottom, 360 - top - bottom),
                                "%d ÷ 2 = %d°." % (360 - top - bottom, each)])

    if t == 4:                                        # trapezium co-interior
        a = random.randint(50, 130)
        return _num_q("In a trapezium, the two angles on the same side between the "
                      "parallel lines add up to 180°. One of them is %d°. How many "
                      "degrees is the other?" % a,
                      180 - a, "int", unit="degrees",
                      solution=["The two angles add up to 180°.",
                                "180 − %d = %d°." % (a, 180 - a)])

    if t == 5:                                        # ratio
        mult = pick([[1, 2, 3, 4], [1, 1, 2, 2], [2, 3, 3, 4], [1, 3, 4, 4],
                     [1, 2, 2, 3]])
        unit = 360 // sum(mult)
        angs = [m * unit for m in mult]
        want = random.randrange(4)
        return _num_q("The four angles of a quadrilateral are in the ratio %s. "
                      "How many degrees is the %s angle in that ratio?"
                      % (" : ".join(str(m) for m in mult),
                         ["first", "second", "third", "fourth"][want]),
                      angs[want], "int", unit="degrees",
                      solution=["The ratio has %d parts and 360 ÷ %d = %d°."
                                % (sum(mult), sum(mult), unit),
                                "%d × %d = %d°." % (mult[want], unit, angs[want])])

    if t == 6:                                        # visual: rectangle / square
        nm = pick(["square", "rectangle"])
        ask = pick(["total", "each"])
        if ask == "total":
            return {"prompt": "Every corner of this quadrilateral is a right angle. "
                              "What do its four angles add up to, in degrees?",
                    "component": "shape",
                    "spec": {"kind": "2d", "name": nm, "ask": "vertices",
                             "marks": "right_angle"},
                    "answer": 360, "answer_type": "int",
                    "solution": ["4 × 90 = 360°.",
                                 "The angles of any quadrilateral add up to 360°."]}
        return {"prompt": "This quadrilateral has four equal angles. How many degrees is "
                          "each angle?",
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "vertices",
                         "marks": "right_angle"},
                "answer": 90, "answer_type": "int",
                "solution": ["The four angles add up to 360°.",
                             "360 ÷ 4 = 90°."]}

    if t == 7:                                        # possible or not
        vals, ok = pick([([90, 90, 90, 90], True), ([100, 80, 100, 80], True),
                         ([120, 60, 120, 70], False), ([70, 110, 70, 110], True),
                         ([90, 90, 90, 80], False), ([45, 135, 45, 135], True)])
        return _num_q("Could a quadrilateral have angles of %s? (type yes or no)"
                      % ", ".join("%d°" % v for v in vals),
                      "yes" if ok else "no", "str", text=True, placeholder="yes / no",
                      solution=["%s = %d°."
                                % (" + ".join("%d" % v for v in vals), sum(vals)),
                                "A quadrilateral's angles must total exactly 360°, so "
                                "the answer is %s." % ("yes" if ok else "no")])

    if t == 8:                                        # split into triangles
        return _num_q("A quadrilateral can be split into 2 triangles by drawing one "
                      "diagonal. The angles of a triangle add up to 180°. What do the "
                      "angles of the quadrilateral add up to, in degrees?",
                      360, "int", unit="degrees",
                      solution=["2 triangles, each with 180°.",
                                "2 × 180 = 360°."])

    # word problem
    who = pick(NAMES)
    a = random.randint(60, 110)
    b = a + random.randint(10, 40)
    c = random.randint(50, 110)
    rest = 360 - a - b - c
    while not (20 <= rest <= 200):
        a = random.randint(60, 110)
        b = a + random.randint(10, 40)
        c = random.randint(50, 110)
        rest = 360 - a - b - c
    return _num_q("%s draws a quadrilateral. One angle is %d°, the next is %d° larger "
                  "than that one, and a third angle is %d°. How many degrees is the "
                  "last angle?" % (who, a, b - a, c),
                  rest, "int", unit="degrees",
                  solution=["The second angle is %d + %d = %d°." % (a, b - a, b),
                            "%d + %d + %d = %d, and 360 − %d = %d°."
                            % (a, b, c, a + b + c, a + b + c, rest)])


@skill("Y6.8.i", "Coordinates in all four quadrants", S8)
def _(d=1):
    d = _tier(d)
    r = _q4r(d)
    t = _pick_t([3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3])

    if t == 10:                                       # describe the coordinate plane
        which = pick(["origin", "axis", "quadrants", "axis_name"])
        if which == "origin":
            return _num_q("On the coordinate plane the horizontal axis and the vertical "
                          "axis cross at the origin. Write the coordinates of the origin, "
                          "in the form (x,y).",
                          _coord(0, 0), "coord", text=True, placeholder="e.g. (-2,3)",
                          solution=["The origin is where both coordinates are zero.",
                                    "The origin is (0,0)."])
        if which == "axis":
            k = _nz(-r, r)
            on_y = random.random() < 0.5
            pt = _coord(0, k) if on_y else _coord(k, 0)
            return _num_q("Describe the coordinate plane: the point %s lies on one of the "
                          "two axes. Which axis is it on? (type x-axis or y-axis)" % pt,
                          "y-axis" if on_y else "x-axis", "str", text=True,
                          placeholder="x-axis / y-axis",
                          solution=["A point with x = 0 lies on the vertical axis; a "
                                    "point with y = 0 lies on the horizontal axis.",
                                    "%s lies on the %s."
                                    % (pt, "y-axis" if on_y else "x-axis")])
        if which == "quadrants":
            return _num_q("The two axes of a coordinate plane divide it into equal "
                          "regions called quadrants. How many quadrants does a coordinate "
                          "plane have?",
                          4, "int", unit="quadrants",
                          solution=["The x-axis and the y-axis cut the plane into four "
                                    "regions.",
                                    "There are 4 quadrants."])
        horiz = random.random() < 0.5
        return _num_q("On the coordinate plane, what is the name of the %s axis? "
                      "(type x-axis or y-axis)" % ("horizontal" if horiz else "vertical"),
                      "x-axis" if horiz else "y-axis", "str", text=True,
                      placeholder="x-axis / y-axis",
                      solution=["The horizontal axis is the x-axis and the vertical axis "
                                "is the y-axis.",
                                "The %s axis is the %s."
                                % ("horizontal" if horiz else "vertical",
                                   "x-axis" if horiz else "y-axis")])

    if t == 11:                                       # objects on a coordinate plane
        x1, y1 = _nz(-r, r), _nz(-r, r)
        x2, y2 = _nz(-r, r), _nz(-r, r)
        while (x2, y2) == (x1, y1):
            x2, y2 = _nz(-r, r), _nz(-r, r)
        obj1, ltr1, obj2, ltr2 = pick([("park", "P", "shop", "S"),
                                       ("library", "L", "museum", "M"),
                                       ("bank", "B", "café", "C"),
                                       ("theatre", "T", "garden", "G")])
        first = random.random() < 0.5
        ax, ay = (x1, y1) if first else (x2, y2)
        name = obj1 if first else obj2
        spec = dict(_q4(d))
        spec["points"] = [[x1, y1, ltr1], [x2, y2, ltr2]]
        return {"prompt": "The grid shows two objects on a coordinate plane: %s marks the "
                          "%s and %s marks the %s. Plot the point that shows where the %s "
                          "is." % (ltr1, obj1, ltr2, obj2, name),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ax, ay), "answer_type": "coord",
                "solution": ["Read across to the x-axis, then up or down to the y-axis.",
                             "The %s is at %s." % (name, _coord(ax, ay))]}

    if t == 12:                                       # coordinate planes as maps
        x = random.randint(-r + 2, r - 2)
        y = random.randint(-r + 2, r - 2)
        dx = random.randint(1, 2)
        dy = random.randint(1, 2)
        east = random.random() < 0.5
        north = random.random() < 0.5
        gx = x + dx if east else x - dx
        gy = y + dy if north else y - dy
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "S"]]
        return {"prompt": "A map is drawn on a coordinate plane and each unit stands for "
                          "1 km. S marks the station. The sports centre is %d km %s and "
                          "%d km %s of the station. Plot the point that shows the sports "
                          "centre." % (dx, "east" if east else "west",
                                       dy, "north" if north else "south"),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(gx, gy), "answer_type": "coord",
                "solution": ["East is right, west is left, north is up and south is down.",
                             "From %s move to %s." % (_coord(x, y), _coord(gx, gy))]}

    if t == 0:                                        # plot a named point
        x, y = _nz(-r, r), _nz(-r, r)
        return {"prompt": "Plot the point %s on the grid." % _coord(x, y),
                "component": "coordinate_grid", "spec": _q4(d),
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["The first number is the x-coordinate: %d." % x,
                             "The second number is the y-coordinate: %d." % y]}

    if t == 1:                                        # read a plotted point
        x, y = _nz(-r, r), _nz(-r, r)
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"]]
        return {"prompt": "Write the coordinates of the point A, in the form (x,y).",
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["Read across to the x-axis: %d." % x,
                             "Read down or up to the y-axis: %d." % y,
                             "A is at %s." % _coord(x, y)]}

    if t == 2:                                        # fourth vertex of a rectangle
        w = random.randint(2, r)
        h = random.randint(2, r)
        while h == w:
            h = random.randint(2, r)
        x = random.randint(-r, r - w)
        y = random.randint(-r, r - h)
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"], [x + w, y, "B"], [x, y + h, "D"]]
        return {"prompt": "A, B and D are three corners of a rectangle. Plot the fourth "
                          "corner.",
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(x + w, y + h), "answer_type": "coord",
                "solution": ["The rectangle is %d units wide and %d units tall." % (w, h),
                             "The fourth corner is %s." % _coord(x + w, y + h)]}

    if t == 3:                                        # plot from a description
        x, y = _nz(-r, r), _nz(-r, r)
        return {"prompt": "Plot the point whose x-coordinate is %d and whose "
                          "y-coordinate is %d." % (x, y),
                "component": "coordinate_grid", "spec": _q4(d),
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["Go %d along the x-axis and %d along the y-axis." % (x, y),
                             "That is the point %s." % _coord(x, y)]}

    if t == 4:                                        # which quadrant
        x, y = _nz(-r, r), _nz(-r, r)
        quad = 1 if (x > 0 and y > 0) else (2 if (x < 0 and y > 0)
                                            else (3 if (x < 0 and y < 0) else 4))
        return _num_q("The four quadrants are numbered 1 (top right), 2 (top left), "
                      "3 (bottom left) and 4 (bottom right). Which quadrant contains the "
                      "point %s? Write the number." % _coord(x, y),
                      quad, "int",
                      solution=["x = %d is %s and y = %d is %s."
                                % (x, "positive" if x > 0 else "negative",
                                   y, "positive" if y > 0 else "negative"),
                                "That is quadrant %d." % quad])

    if t == 5:                                        # length of a side
        x, y = _nz(-r, r - 1), _nz(-r, r - 1)
        horizontal = random.random() < 0.5
        k = random.randint(2, r)
        if horizontal:
            x2 = x + k if x + k <= r else x - k
            y2 = y
        else:
            x2 = x
            y2 = y + k if y + k <= r else y - k
        return _num_q("A line segment joins %s to %s. How many units long is it?"
                      % (_coord(x, y), _coord(x2, y2)),
                      k, "int", unit="units",
                      solution=["The segment is %s, so count along one axis."
                                % ("horizontal" if horizontal else "vertical"),
                                "From %d to %d is %d units."
                                % (x if horizontal else y, x2 if horizontal else y2, k)])

    if t == 6:                                        # midpoint
        x1, y1 = _nz(-r, r), _nz(-r, r)
        dx = 2 * random.randint(1, max(1, r // 2))
        dy = 2 * random.randint(1, max(1, r // 2))
        x2 = x1 + dx if x1 + dx <= r else x1 - dx
        y2 = y1 + dy if y1 + dy <= r else y1 - dy
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return _num_q("A and B are the ends of a straight line. A is at %s and B is at "
                      "%s. Write the coordinates of the midpoint of AB, in the form (x,y)."
                      % (_coord(x1, y1), _coord(x2, y2)),
                      _coord(mx, my), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["The midpoint's x is halfway between %d and %d: %d."
                                % (x1, x2, mx),
                                "The midpoint's y is halfway between %d and %d: %d."
                                % (y1, y2, my),
                                "The midpoint is %s." % _coord(mx, my)])

    if t == 7:                                        # typed fourth vertex of a square
        s = random.randint(2, r)
        x = random.randint(-r, r - s)
        y = random.randint(-r, r - s)
        return _num_q("Three corners of a square are %s, %s and %s. Write the coordinates "
                      "of the fourth corner, in the form (x,y)."
                      % (_coord(x, y), _coord(x + s, y), _coord(x + s, y + s)),
                      _coord(x, y + s), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["Every side of the square is %d units long." % s,
                                "The missing corner is %s." % _coord(x, y + s)])

    if t == 8:                                        # move from a point
        x, y = _nz(-r + 2, r - 2), _nz(-r + 2, r - 2)
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        while dx == 0 and dy == 0:
            dx, dy = random.randint(-2, 2), random.randint(-2, 2)
        return _num_q("Start at %s. Move %d %s and %d %s. Write the coordinates of the "
                      "point you reach, in the form (x,y)."
                      % (_coord(x, y), abs(dx), "right" if dx >= 0 else "left",
                         abs(dy), "up" if dy >= 0 else "down"),
                      _coord(x + dx, y + dy), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["x: %d %s %d = %d." % (x, "+" if dx >= 0 else "−",
                                                       abs(dx), x + dx),
                                "y: %d %s %d = %d." % (y, "+" if dy >= 0 else "−",
                                                       abs(dy), y + dy),
                                "The point is %s." % _coord(x + dx, y + dy)])

    # perimeter of a rectangle given by its corners
    w = random.randint(2, r)
    h = random.randint(2, r)
    x = random.randint(-r, r - w)
    y = random.randint(-r, r - h)
    return _num_q("A rectangle has corners at %s, %s, %s and %s. What is its perimeter, "
                  "in units?" % (_coord(x, y), _coord(x + w, y), _coord(x + w, y + h),
                                 _coord(x, y + h)),
                  2 * (w + h), "int", unit="units",
                  solution=["The rectangle is %d units by %d units." % (w, h),
                            "2 × (%d + %d) = %d units." % (w, h, 2 * (w + h))])


@skill("Y6.8.j", "Translate a shape on a grid", S8)
def _(d=1):
    d = _tier(d)
    r = _q4r(d)
    t = _pick_t([3, 3, 2, 2, 1, 1, 1, 1, 1, 3, 3, 3])
    dx = _nz(-_by_d(d, 3, 4, 5), _by_d(d, 3, 4, 5))
    dy = _nz(-_by_d(d, 3, 4, 5), _by_d(d, 3, 4, 5))

    def _desc(ax, ay):
        parts = []
        if ax:
            parts.append("%d %s" % (abs(ax), "right" if ax > 0 else "left"))
        if ay:
            parts.append("%d %s" % (abs(ay), "up" if ay > 0 else "down"))
        return " and ".join(parts)

    if t == 9:                                        # translations: graph the image
        x = random.randint(max(-r, -r - dx), min(r - 2, r - dx - 2))
        y = random.randint(max(-r, -r - dy), min(r - 2, r - dy - 2))
        poly = [[x, y], [x + 2, y], [x + 2, y + 2], [x, y + 2]]
        spec = dict(_q4(d))
        spec["polygon"] = poly
        spec["points"] = [[x, y, "P"]]
        return {"prompt": "The square is translated %s. Graph the image by plotting the "
                          "point that the vertex P is translated onto." % _desc(dx, dy),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["In a translation every vertex of the shape moves the same "
                             "way.",
                             "P at %s translates to %s."
                             % (_coord(x, y), _coord(x + dx, y + dy))]}

    if t == 10:                                       # identify the transformation
        rule = pick(["translation", "reflection", "rotation"])
        if rule == "translation":
            ax, ay = _nz(-4, 4), _nz(-4, 4)
            desc = ("every point (x,y) of the shape moves to (x %s %d, y %s %d)"
                    % ("+" if ax > 0 else "−", abs(ax), "+" if ay > 0 else "−", abs(ay)))
        elif rule == "reflection":
            axis = pick(["x-axis", "y-axis"])
            desc = ("every point (x,y) of the shape moves to (%s)"
                    % ("x, −y" if axis == "x-axis" else "−x, y"))
        else:
            desc = "every point (x,y) of the shape moves to (−x, −y), a half turn about " \
                   "the origin"
        return _num_q("Identify the transformation. On a coordinate grid %s. The shape "
                      "keeps its size and shape. Is this a reflection, a rotation or a "
                      "translation? (type one word)" % desc,
                      rule, "str", text=True,
                      placeholder="reflection / rotation / translation",
                      solution=["A translation slides, a reflection flips and a rotation "
                                "turns the shape.",
                                "This transformation is a %s." % rule])

    if t == 11:                                       # combination of transformations
        x, y = _nz(-r + 1, r - 1), _nz(-r + 1, r - 1)
        ax = _nz(-3, 3)
        ay = _nz(-3, 3)
        axis = pick(["x-axis", "y-axis"])
        rx, ry = (x, -y) if axis == "x-axis" else (-x, y)
        return _num_q("A combination of transformations is used. The point %s is first "
                      "reflected in the %s, and the image is then translated %s. Write "
                      "the coordinates of the final image, in the form (x,y)."
                      % (_coord(x, y), axis, _desc(ax, ay)),
                      _coord(rx + ax, ry + ay), "coord", text=True,
                      placeholder="e.g. (-2,3)",
                      solution=["The reflection sends %s to %s."
                                % (_coord(x, y), _coord(rx, ry)),
                                "The translation then gives %s."
                                % _coord(rx + ax, ry + ay)])

    if t == 0:                                        # plot the image of a point
        x = random.randint(max(-r, -r - dx), min(r, r - dx))
        y = random.randint(max(-r, -r - dy), min(r, r - dy))
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"]]
        return {"prompt": "Translate the point A %s. Plot the point A lands on."
                          % _desc(dx, dy),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["A is at %s." % _coord(x, y),
                             "Moving %s gives %s."
                             % (_desc(dx, dy), _coord(x + dx, y + dy))]}

    if t == 1:                                        # translate a vertex of a triangle
        x = random.randint(max(-r, -r - dx), min(r - 2, r - dx - 2))
        y = random.randint(max(-r, -r - dy), min(r - 2, r - dy - 2))
        poly = [[x, y], [x + 2, y], [x, y + 2]]
        spec = dict(_q4(d))
        spec["polygon"] = poly
        spec["points"] = [[x, y, "P"]]
        return {"prompt": "The whole triangle is translated %s. Plot the point that the "
                          "vertex P lands on." % _desc(dx, dy),
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["Every vertex moves the same way.",
                             "P at %s moves to %s."
                             % (_coord(x, y), _coord(x + dx, y + dy))]}

    if t == 2:                                        # typed image
        x = random.randint(max(-r, -r - dx), min(r, r - dx))
        y = random.randint(max(-r, -r - dy), min(r, r - dy))
        return _num_q("The point %s is translated %s. Write the coordinates of its new "
                      "position, in the form (x,y)." % (_coord(x, y), _desc(dx, dy)),
                      _coord(x + dx, y + dy), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["x: %d + (%d) = %d." % (x, dx, x + dx),
                                "y: %d + (%d) = %d." % (y, dy, y + dy),
                                "The new position is %s." % _coord(x + dx, y + dy)])

    if t == 3:                                        # describe the translation (size)
        x = random.randint(max(-r, -r - dx), min(r, r - dx))
        y = random.randint(max(-r, -r - dy), min(r, r - dy))
        ask_x = abs(dx) > 0 and (abs(dy) == 0 or random.random() < 0.5)
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"], [x + dx, y + dy, "B"]]
        # NB the answer is a COUNT, and coordinate_grid can only return "(x,y)" --
        # rendering the grid here would make the question impossible to answer.
        # State the two points in the prompt and take a typed number instead.
        if ask_x:
            return {"prompt": "A shape is translated so that the point A %s lands exactly "
                              "on B %s. How many units does it move %s?"
                              % (_coord(x, y), _coord(x + dx, y + dy),
                                 "right" if dx > 0 else "left"),
                    "component": "number",
                    "answer": abs(dx), "answer_type": "int",
                    "solution": ["A has x = %d and B has x = %d." % (x, x + dx),
                                 "That is a move of %d units %s."
                                 % (abs(dx), "right" if dx > 0 else "left")]}
        return {"prompt": "A shape is translated so that the point A %s lands exactly on "
                          "B %s. How many units does it move %s?"
                          % (_coord(x, y), _coord(x + dx, y + dy),
                             "up" if dy > 0 else "down"),
                "component": "number",
                "answer": abs(dy), "answer_type": "int",
                "solution": ["A has y = %d and B has y = %d." % (y, y + dy),
                             "That is a move of %d units %s."
                             % (abs(dy), "up" if dy > 0 else "down")]}

    if t == 4:                                        # inverse: back to the start
        x = random.randint(max(-r, -r - dx), min(r, r - dx))
        y = random.randint(max(-r, -r - dy), min(r, r - dy))
        return _num_q("A point is translated %s and lands on %s. Where did the point "
                      "start? Write the coordinates in the form (x,y)."
                      % (_desc(dx, dy), _coord(x + dx, y + dy)),
                      _coord(x, y), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["Undo the move: go the opposite way.",
                                "The point started at %s." % _coord(x, y)])

    if t == 5:                                        # two translations combined
        ex, ey = _nz(-3, 3), _nz(-3, 3)
        x, y = 0, 0
        return _num_q("A shape at the origin (0,0) is translated %s, and then translated "
                      "%s. Write the coordinates of the point that started at (0,0), in "
                      "the form (x,y)." % (_desc(dx, dy), _desc(ex, ey)),
                      _coord(dx + ex, dy + ey), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["x: 0 + (%d) + (%d) = %d." % (dx, ex, dx + ex),
                                "y: 0 + (%d) + (%d) = %d." % (dy, ey, dy + ey),
                                "The point is at %s." % _coord(dx + ex, dy + ey)])

    if t == 6:                                        # does the shape change?
        prop, ans = pick([("the lengths of its sides", "no"),
                          ("the sizes of its angles", "no"),
                          ("its area", "no"),
                          ("the position of its vertices", "yes")])
        return _num_q("A shape is translated across a grid. Does a translation change "
                      "%s? (type yes or no)" % prop,
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["A translation slides a shape without turning or "
                                "resizing it.",
                                "So the answer is %s." % ans])

    if t == 7:                                        # translate all vertices
        x = random.randint(max(-r, -r - dx), min(r - 2, r - dx - 2))
        y = random.randint(max(-r, -r - dy), min(r - 2, r - dy - 2))
        return _num_q("A square has corners at %s, %s, %s and %s. The square is "
                      "translated %s. Write the new coordinates of the corner that was "
                      "at %s, in the form (x,y)."
                      % (_coord(x, y), _coord(x + 2, y), _coord(x + 2, y + 2),
                         _coord(x, y + 2), _desc(dx, dy), _coord(x + 2, y + 2)),
                      _coord(x + 2 + dx, y + 2 + dy), "coord", text=True,
                      placeholder="e.g. (-2,3)",
                      solution=["Add the move to that corner.",
                                "x: %d + (%d) = %d and y: %d + (%d) = %d."
                                % (x + 2, dx, x + 2 + dx, y + 2, dy, y + 2 + dy),
                                "The corner is at %s." % _coord(x + 2 + dx, y + 2 + dy)])

    # total distance moved
    x = random.randint(max(-r, -r - dx), min(r, r - dx))
    y = random.randint(max(-r, -r - dy), min(r, r - dy))
    return _num_q("A counter is translated %s. Counting only whole squares along the "
                  "grid lines, how many squares does the counter travel altogether?"
                  % _desc(dx, dy),
                  abs(dx) + abs(dy), "int", unit="squares",
                  solution=["%s across and %s up or down."
                            % (_pl(abs(dx), "square"), _pl(abs(dy), "square")),
                            "%d + %d = %d squares." % (abs(dx), abs(dy),
                                                       abs(dx) + abs(dy))])


@skill("Y6.8.k", "Reflect a shape in the axes", S8)
def _(d=1):
    d = _tier(d)
    r = _q4r(d)
    t = _pick_t([3, 3, 2, 2, 1, 1, 1, 1, 1, 4])

    if t == 9:                                        # reflections: graph the image
        axis = pick(["x-axis", "y-axis"])
        # keep the whole square inside one quadrant, so it never crosses the mirror line
        x = random.randint(1, r - 2)
        y = random.randint(1, r - 2)
        if random.random() < 0.5:
            x = -(x + 2)
        if random.random() < 0.5:
            y = -(y + 2)
        poly = [[x, y], [x + 2, y], [x + 2, y + 2], [x, y + 2]]
        spec = dict(_q4(d))
        spec["polygon"] = poly
        spec["points"] = [[x, y, "P"]]
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        return {"prompt": "The square is reflected in the %s. Graph the image by plotting "
                          "the point that the vertex P is reflected onto." % axis,
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["Reflecting in the %s changes the sign of the %s."
                             % (axis, "y-coordinate" if axis == "x-axis"
                                else "x-coordinate"),
                             "The image of P at %s is %s."
                             % (_coord(x, y), _coord(ix, iy))]}

    if t == 0:                                        # plot the reflection of a point
        x, y = _nz(-r, r), _nz(-r, r)
        axis = pick(["x-axis", "y-axis"])
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        spec = dict(_q4(d))
        spec["points"] = [[x, y, "A"]]
        return {"prompt": "Reflect the point A in the %s. Plot the image of A." % axis,
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["Reflecting in the %s %s."
                             % (axis, "changes the sign of the y-coordinate"
                                if axis == "x-axis" else
                                "changes the sign of the x-coordinate"),
                             "A at %s becomes %s." % (_coord(x, y), _coord(ix, iy))]}

    if t == 1:                                        # reflect a vertex of a triangle
        axis = pick(["x-axis", "y-axis"])
        x = random.randint(-r + 2, r - 2)
        y = random.randint(-r + 2, r - 2)
        while x == 0 or y == 0:
            x, y = random.randint(-r + 2, r - 2), random.randint(-r + 2, r - 2)
        poly = [[x, y], [x + 2, y], [x, y + 2]]
        if max(abs(p[0]) for p in poly) > r or max(abs(p[1]) for p in poly) > r:
            poly = [[x, y], [x - 2, y], [x, y - 2]]
        spec = dict(_q4(d))
        spec["polygon"] = poly
        spec["points"] = [[x, y, "P"]]
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        return {"prompt": "The triangle is reflected in the %s. Plot the point that the "
                          "vertex P is reflected onto." % axis,
                "component": "coordinate_grid", "spec": spec,
                "answer": _coord(ix, iy), "answer_type": "coord",
                "solution": ["P is at %s." % _coord(x, y),
                             "Reflected in the %s it lands on %s." % (axis, _coord(ix, iy))]}

    if t == 2:                                        # typed reflection
        x, y = _nz(-r, r), _nz(-r, r)
        axis = pick(["x-axis", "y-axis"])
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        return _num_q("The point %s is reflected in the %s. Write the coordinates of its "
                      "image, in the form (x,y)." % (_coord(x, y), axis),
                      _coord(ix, iy), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["Reflecting in the %s keeps %s and changes the sign of %s."
                                % (axis, "x" if axis == "x-axis" else "y",
                                   "y" if axis == "x-axis" else "x"),
                                "The image is %s." % _coord(ix, iy)])

    if t == 3:                                        # which axis was used
        x, y = _nz(-r, r), _nz(-r, r)
        axis = pick(["x-axis", "y-axis"])
        ix, iy = (x, -y) if axis == "x-axis" else (-x, y)
        return _num_q("The point %s is reflected onto %s. Which axis is the mirror line? "
                      "(type x-axis or y-axis)" % (_coord(x, y), _coord(ix, iy)),
                      axis, "str", text=True, placeholder="x-axis / y-axis",
                      solution=["The %s stayed the same and the %s changed sign."
                                % ("x-coordinate" if axis == "x-axis" else "y-coordinate",
                                   "y-coordinate" if axis == "x-axis" else "x-coordinate"),
                                "The mirror line is the %s." % axis])

    if t == 4:                                        # reflect twice
        x, y = _nz(-r, r), _nz(-r, r)
        return _num_q("The point %s is reflected in the x-axis, and the image is then "
                      "reflected in the y-axis. Write the coordinates of the final point, "
                      "in the form (x,y)." % _coord(x, y),
                      _coord(-x, -y), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["First reflection: %s becomes %s."
                                % (_coord(x, y), _coord(x, -y)),
                                "Second reflection: %s becomes %s."
                                % (_coord(x, -y), _coord(-x, -y))])

    if t == 5:                                        # points on the mirror line
        axis = pick(["x-axis", "y-axis"])
        k = _nz(-r, r)
        pt = _coord(k, 0) if axis == "x-axis" else _coord(0, k)
        return _num_q("The point %s is reflected in the %s. Write the coordinates of its "
                      "image, in the form (x,y)." % (pt, axis),
                      pt, "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["The point already lies on the mirror line.",
                                "A point on the mirror line does not move, so the image "
                                "is %s." % pt])

    if t == 6:                                        # distance from the mirror
        x, y = _nz(-r, r), _nz(-r, r)
        axis = pick(["x-axis", "y-axis"])
        gap = abs(y) if axis == "x-axis" else abs(x)
        return _num_q("The point %s is reflected in the %s. How many units apart are the "
                      "point and its image?" % (_coord(x, y), axis),
                      2 * gap, "int", unit="units",
                      solution=["The point is %d units from the %s." % (gap, axis),
                                "The image is the same distance on the other side: "
                                "%d + %d = %d units." % (gap, gap, 2 * gap)])

    if t == 7:                                        # reflection of a rectangle corner
        axis = pick(["x-axis", "y-axis"])
        w, h = random.randint(2, 3), random.randint(2, 3)
        x = random.randint(1, r - w)
        y = random.randint(1, r - h)
        if random.random() < 0.5:
            x = -x - w
        if random.random() < 0.5:
            y = -y - h
        cx, cy = x + w, y + h
        ix, iy = (cx, -cy) if axis == "x-axis" else (-cx, cy)
        return _num_q("A rectangle has one corner at %s. The rectangle is reflected in "
                      "the %s. Write the new coordinates of that corner, in the form "
                      "(x,y)." % (_coord(cx, cy), axis),
                      _coord(ix, iy), "coord", text=True, placeholder="e.g. (-2,3)",
                      solution=["Reflecting in the %s changes the sign of the %s."
                                % (axis, "y-coordinate" if axis == "x-axis"
                                   else "x-coordinate"),
                                "The corner lands on %s." % _coord(ix, iy)])

    # reasoning
    prop, ans = pick([("the size of the shape", "no"),
                      ("the lengths of the sides", "no"),
                      ("the sizes of the angles", "no"),
                      ("which way round the shape faces", "yes")])
    return _num_q("A shape is reflected in the y-axis. Does the reflection change %s? "
                  "(type yes or no)" % prop,
                  ans, "str", text=True, placeholder="yes / no",
                  solution=["A reflection produces a mirror image of the same size.",
                            "So the answer is %s." % ans])


@skill("Y6.8.l", "Perimeter of rectangles and compound shapes", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 1, 1, 1, 1, 1])
    lo, hi = _by_d(d, (3, 12), (4, 25), (6, 60))

    if t == 0:                                        # visual: perimeter of a rectangle
        rows = random.randint(2, _by_d(d, 5, 7, 8))
        cols = random.randint(2, _by_d(d, 6, 9, 10))
        return {"prompt": "Each square is 1 cm by 1 cm. What is the perimeter of this "
                          "shape, in cm?",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "rows": rows, "cols": cols},
                "answer": 2 * (rows + cols), "answer_type": "int",
                "solution": ["The rectangle is %d cm by %d cm." % (cols, rows),
                             "2 × (%d + %d) = %d cm." % (cols, rows, 2 * (rows + cols))]}

    if t == 1:                                        # visual: L-shape perimeter
        R = random.randint(3, _by_d(d, 5, 6, 8))
        C = random.randint(3, _by_d(d, 6, 8, 10))
        r_ = random.randint(1, R - 2)
        c_ = random.randint(1, C - 2)
        return {"prompt": "Each square is 1 cm by 1 cm. What is the perimeter of this "
                          "compound shape, in cm?",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "cells": _L_cells(R, C, r_, c_)},
                "answer": 2 * (R + C), "answer_type": "int",
                "solution": ["The L-shape fits exactly inside %s %d cm by %d cm rectangle."
                             % (_an(C), C, R),
                             "The steps in the L add up to the same distance as the "
                             "rectangle's sides: 2 × (%d + %d) = %d cm."
                             % (C, R, 2 * (R + C))]}

    if t == 2:                                        # rectangle perimeter (bare)
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        while h == w:
            h = random.randint(lo, hi)
        return _num_q("A rectangle measures %d cm by %d cm. What is its perimeter, in cm?"
                      % (w, h),
                      2 * (w + h), "int", unit="cm",
                      solution=["Perimeter = 2 × (length + width).",
                                "2 × (%d + %d) = %d cm." % (w, h, 2 * (w + h))])

    if t == 3:                                        # missing side from perimeter
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        p = 2 * (w + h)
        return _num_q("A rectangle has a perimeter of %d cm. One side is %d cm. "
                      "How long is the side next to it, in cm?" % (p, w),
                      h, "int", unit="cm",
                      solution=["Half the perimeter is %d ÷ 2 = %d cm." % (p, p // 2),
                                "%d − %d = %d cm." % (p // 2, w, h)])

    if t == 4:                                        # square from perimeter
        s = random.randint(lo, hi)
        return _num_q("A square has a perimeter of %d cm. How long is each side, in cm?"
                      % (4 * s),
                      s, "int", unit="cm",
                      solution=["A square has 4 equal sides.",
                                "%d ÷ 4 = %d cm." % (4 * s, s)])

    if t == 5:                                        # L-shape from dimensions
        W = random.randint(6, _by_d(d, 12, 20, 30))
        H = random.randint(5, _by_d(d, 10, 18, 26))
        a = random.randint(2, W - 2)
        b = random.randint(2, H - 2)
        return _num_q("An L-shape is made by cutting %s %d cm by %d cm rectangle out of "
                      "the corner of %s %d cm by %d cm rectangle. What is the perimeter "
                      "of the L-shape, in cm?" % (_an(a), a, b, _an(W), W, H),
                      2 * (W + H), "int", unit="cm",
                      solution=["The two cut edges are %d cm and %d cm, and they replace "
                                "exactly the same lengths that were removed." % (a, b),
                                "So the perimeter is still 2 × (%d + %d) = %d cm."
                                % (W, H, 2 * (W + H))])

    if t == 6:                                        # word problem: fencing cost
        who = pick(NAMES)
        w = random.randint(4, _by_d(d, 10, 15, 25))
        h = random.randint(4, _by_d(d, 10, 15, 25))
        cost = pick([3, 4, 5, 6, 8])
        p = 2 * (w + h)
        return _num_q("%s fences a rectangular garden measuring %d m by %d m. Fencing "
                      "costs £%d per metre. What is the total cost, in pounds?"
                      % (who, w, h, cost),
                      p * cost, "int", unit="pounds",
                      solution=["Perimeter = 2 × (%d + %d) = %d m." % (w, h, p),
                                "%d × %d = %d pounds." % (p, cost, p * cost)])

    if t == 7:                                        # regular polygon perimeter
        nm, sd = pick([("equilateral triangle", 3), ("square", 4),
                       ("regular pentagon", 5), ("regular hexagon", 6),
                       ("regular octagon", 8)])
        s = random.randint(lo, hi)
        if random.random() < 0.5:
            return _num_q("%s has sides of %d cm. What is its perimeter, in cm?"
                          % (_a(nm).capitalize(), s),
                          sd * s, "int", unit="cm",
                          solution=["All %d sides are %d cm." % (sd, s),
                                    "%d × %d = %d cm." % (sd, s, sd * s)])
        return _num_q("%s has a perimeter of %d cm. How long is each side, in cm?"
                      % (_a(nm).capitalize(), sd * s),
                      s, "int", unit="cm",
                      solution=["%s has %d equal sides." % (_a(nm).capitalize(), sd),
                                "%d ÷ %d = %d cm." % (sd * s, sd, s)])

    if t == 8:                                        # comparison
        w1 = random.randint(lo, hi)
        h1 = random.randint(lo, hi)
        w2 = random.randint(lo, hi)
        h2 = random.randint(lo, hi)
        p1, p2 = 2 * (w1 + h1), 2 * (w2 + h2)
        while p1 == p2:
            w2 = random.randint(lo, hi)
            p2 = 2 * (w2 + h2)
        return _num_q("Rectangle A measures %d cm by %d cm. Rectangle B measures %d cm by "
                      "%d cm. How many cm larger is the bigger perimeter?"
                      % (w1, h1, w2, h2),
                      abs(p1 - p2), "int", unit="cm",
                      solution=["A: 2 × (%d + %d) = %d cm." % (w1, h1, p1),
                                "B: 2 × (%d + %d) = %d cm." % (w2, h2, p2),
                                "%d − %d = %d cm." % (max(p1, p2), min(p1, p2),
                                                      abs(p1 - p2))])

    # mixed units
    w_m = random.randint(2, 9)
    h_cm = random.randint(1, 9) * 50
    p_cm = 2 * (w_m * 100 + h_cm)
    return _num_q("A rectangle is %d m long and %d cm wide. What is its perimeter, in cm?"
                  % (w_m, h_cm),
                  p_cm, "int", unit="cm",
                  solution=["%d m = %d cm." % (w_m, w_m * 100),
                            "2 × (%d + %d) = %d cm." % (w_m * 100, h_cm, p_cm)])


@skill("Y6.8.m", "Area of rectangles and squares", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1])
    lo, hi = _by_d(d, (2, 9), (3, 15), (4, 40))

    if t == 10:                                       # visual: L-shape split into rectangles
        R, C = random.randint(3, _by_d(d, 5, 7, 8)), random.randint(4, _by_d(d, 6, 9, 10))
        r, c = random.randint(1, R - 2), random.randint(1, C - 2)
        area = R * C - r * c
        return {"prompt": "Each square is 1 cm². Find the area of this compound shape, in cm². "
                          "(Split it into rectangles or subtract the missing corner.)",
                "component": "area_grid", "spec": {"mode": "read_area", "cells": _L_cells(R, C, r, c)},
                "answer": area, "answer_type": "int",
                "solution": ["The whole rectangle would be %d × %d = %d cm²." % (R, C, R * C),
                             "The missing corner is %d × %d = %d cm², so %d − %d = %d cm²."
                             % (r, c, r * c, R * C, r * c, area)]}

    if t == 11:                                       # a half-metre side
        w = random.randint(1, _by_d(d, 6, 9, 15))
        h = 2 * random.randint(1, _by_d(d, 4, 6, 10))
        return _num_q("A rectangle measures %d.5 m by %d m. What is its area, in m²?" % (w, h),
                      (2 * w + 1) * h // 2, "int", unit="m²",
                      solution=["Area = %d.5 × %d." % (w, h),
                                "%d × %d = %d and 0.5 × %d = %d, so %d m²." % (w, h, w * h, h, h // 2, (2 * w + 1) * h // 2)])

    if t == 12:                                       # from the perimeter to the area
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        return _num_q("A rectangle has a perimeter of %d cm. Its length is %d cm. What is its area, in cm²?"
                      % (2 * (w + h), w), w * h, "int", unit="cm²",
                      solution=["Half the perimeter is %d cm, so the width is %d − %d = %d cm." % (w + h, w + h, w, h),
                                "Area = %d × %d = %d cm²." % (w, h, w * h)])

    if t == 13:                                       # how many small rectangles fit
        a, b = random.randint(2, 5), random.randint(2, 5)
        m, n = random.randint(2, 6), random.randint(2, 6)
        return _num_q("Cards measure %d cm by %d cm. How many cards fit on a board %d cm by %d cm, laid the same way "
                      "with no gaps or overlaps?" % (a, b, a * m, b * n), m * n, "int", unit="cards",
                      solution=["%d ÷ %d = %d cards along one side and %d ÷ %d = %d along the other." % (a * m, a, m, b * n, b, n),
                                "%d × %d = %d cards." % (m, n, m * n)])

    if t == 0:                                        # visual: count squares
        rows = random.randint(2, _by_d(d, 5, 7, 9))
        cols = random.randint(2, _by_d(d, 6, 9, 10))
        return {"prompt": "Each square is 1 cm². What is the area of this rectangle, "
                          "in cm²?",
                "component": "area_grid",
                "spec": {"mode": "read_area", "rows": rows, "cols": cols},
                "answer": rows * cols, "answer_type": "int",
                "solution": ["The rectangle is %d rows of %d squares." % (rows, cols),
                             "%d × %d = %d cm²." % (rows, cols, rows * cols)]}

    if t == 1:                                        # visual: build an area
        rows = _by_d(d, 5, 6, 8)
        cols = _by_d(d, 6, 8, 10)
        target = random.randint(4, rows * cols - 2)
        return {"prompt": "Each square is 1 cm². Shade squares to make a shape with an "
                          "area of %d cm². How many squares must you shade?" % target,
                "component": "area_grid",
                "spec": {"mode": "build_area", "rows": rows, "cols": cols},
                "answer": target, "answer_type": "int",
                "solution": ["Each shaded square is 1 cm² of area.",
                             "Shade exactly %d squares." % target]}

    if t == 2:                                        # bare rectangle area
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        return _num_q("A rectangle measures %d cm by %d cm. What is its area, in cm²?"
                      % (w, h),
                      w * h, "int", unit="cm²",
                      solution=["Area = length × width.",
                                "%d × %d = %d cm²." % (w, h, w * h)])

    if t == 3:                                        # square area
        s = random.randint(lo, hi)
        return _num_q("A square has sides of %d m. What is its area, in m²?" % s,
                      s * s, "int", unit="m²",
                      solution=["Area of a square = side × side.",
                                "%d × %d = %d m²." % (s, s, s * s)])

    if t == 4:                                        # missing side from area
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        return _num_q("A rectangle has an area of %d cm². One side is %d cm. "
                      "How long is the other side, in cm?" % (w * h, w),
                      h, "int", unit="cm",
                      solution=["Missing side = area ÷ known side.",
                                "%d ÷ %d = %d cm." % (w * h, w, h)])

    if t == 5:                                        # side from square area
        s = pick([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] if d else [2, 3, 4, 5, 6, 7])
        return _num_q("A square has an area of %d cm². How long is each side, in cm?"
                      % (s * s),
                      s, "int", unit="cm",
                      solution=["Look for the number multiplied by itself to give %d."
                                % (s * s),
                                "%d × %d = %d, so each side is %d cm."
                                % (s, s, s * s, s)])

    if t == 6:                                        # word problem: cost of turf
        who = pick(NAMES)
        w = random.randint(3, _by_d(d, 8, 12, 20))
        h = random.randint(3, _by_d(d, 8, 12, 20))
        cost = pick([4, 5, 6, 7, 9])
        return _num_q("%s lays turf on a rectangular lawn measuring %d m by %d m. Turf "
                      "costs £%d per square metre. What is the total cost, in pounds?"
                      % (who, w, h, cost),
                      w * h * cost, "int", unit="pounds",
                      solution=["Area = %d × %d = %d m²." % (w, h, w * h),
                                "%d × %d = %d pounds." % (w * h, cost, w * h * cost)])

    if t == 7:                                        # area and perimeter together
        w = random.randint(lo, hi)
        h = random.randint(lo, hi)
        while h == w:
            h = random.randint(lo, hi)
        return _num_q("A rectangle measures %d cm by %d cm. Work out its area and its "
                      "perimeter, then write the DIFFERENCE between the two numbers."
                      % (w, h),
                      abs(w * h - 2 * (w + h)), "int",
                      solution=["Area = %d × %d = %d." % (w, h, w * h),
                                "Perimeter = 2 × (%d + %d) = %d." % (w, h, 2 * (w + h)),
                                "%d − %d = %d." % (max(w * h, 2 * (w + h)),
                                                   min(w * h, 2 * (w + h)),
                                                   abs(w * h - 2 * (w + h)))])

    if t == 8:                                        # comparison
        w1, h1 = random.randint(lo, hi), random.randint(lo, hi)
        w2, h2 = random.randint(lo, hi), random.randint(lo, hi)
        while w1 * h1 == w2 * h2:
            w2 = random.randint(lo, hi)
        return _num_q("Rectangle A measures %d cm by %d cm. Rectangle B measures %d cm by "
                      "%d cm. How many cm² larger is the bigger area?"
                      % (w1, h1, w2, h2),
                      abs(w1 * h1 - w2 * h2), "int", unit="cm²",
                      solution=["A: %d × %d = %d cm²." % (w1, h1, w1 * h1),
                                "B: %d × %d = %d cm²." % (w2, h2, w2 * h2),
                                "%d − %d = %d cm²." % (max(w1 * h1, w2 * h2),
                                                       min(w1 * h1, w2 * h2),
                                                       abs(w1 * h1 - w2 * h2))])

    # tiles needed
    tile = pick([10, 20])
    w = random.randint(2, 80 // tile) * tile
    h = random.randint(2, 80 // tile) * tile
    n = (w // tile) * (h // tile)
    return _num_q("A wall measures %d cm by %d cm. It is covered with square tiles of "
                  "side %d cm, with no gaps. How many tiles are needed?" % (w, h, tile),
                  n, "int", unit="tiles",
                  solution=["Wall area = %d × %d = %d cm²." % (w, h, w * h),
                            "Tile area = %d × %d = %d cm²." % (tile, tile, tile * tile),
                            "%d ÷ %d = %d tiles." % (w * h, tile * tile, n)])


@skill("Y6.8.n", "Area of parallelograms", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 1, 3, 1, 1])
    lo, hi = _by_d(d, (2, 9), (3, 15), (4, 30))
    b = random.randint(lo, hi)
    h = random.randint(lo, hi)

    if t == 14:                                       # two steps: area, then cost
        who = pick(NAMES)
        cost = pick([2, 3, 4, 5])
        return _num_q("%s sows grass seed on a field shaped like a parallelogram, with a base of %d m and a perpendicular "
                      "height of %d m. Seed costs £%d for each square metre. How much does the seed cost, in pounds?"
                      % (who, b, h, cost), b * h * cost, "int", unit="pounds",
                      solution=["Area = %d × %d = %d m²." % (b, h, b * h), "%d × £%d = £%d." % (b * h, cost, b * h * cost)])

    if t == 11:                                       # a half-centimetre base
        bb = random.randint(2, _by_d(d, 8, 12, 20))
        hh = 2 * random.randint(1, _by_d(d, 4, 6, 10))
        return _num_q("A parallelogram has a base of %d.5 cm and a perpendicular height of %d cm. What is its area, in cm²?"
                      % (bb, hh), (2 * bb + 1) * hh // 2, "int", unit="cm²",
                      solution=["Area = base × perpendicular height = %d.5 × %d." % (bb, hh),
                                "%d × %d = %d and 0.5 × %d = %d, so %d cm²." % (bb, hh, bb * hh, hh, hh // 2, (2 * bb + 1) * hh // 2)])

    if t == 12:                                       # drawn on a grid
        bb = random.randint(2, 5)
        hh = random.randint(2, 5)
        sh = random.randint(1, 3)
        x0, y0 = random.randint(0, 2), random.randint(0, 2)
        poly = [[x0, y0], [x0 + bb, y0], [x0 + bb + sh, y0 + hh], [x0 + sh, y0 + hh]]
        return {"prompt": "The parallelogram is drawn on a centimetre grid. What is its area, in cm²?",
                "component": "coordinate_grid",
                "spec": {"mode": "plot", "size": 10, "polygon": poly, "typed": True, "placeholder": "cm²"},
                "answer": bb * hh, "answer_type": "int",
                "solution": ["The base runs along the bottom: %d cm. The perpendicular height is %d cm." % (bb, hh),
                             "Area = %d × %d = %d cm²." % (bb, hh, bb * hh)]}

    if t == 13:                                       # mixed units
        m = pick([1, 2])
        extra = pick([20, 40, 50, 60])
        hh = random.randint(2, 9) * 10
        base_cm = 100 * m + extra
        return _num_q("A parallelogram has a base of %d.%d m and a perpendicular height of %d cm. What is its area, in cm²?"
                      % (m, extra // 10, hh), base_cm * hh, "int", unit="cm²",
                      solution=["%d.%d m = %d cm." % (m, extra // 10, base_cm),
                                "%d × %d = %s cm²." % (base_cm, hh, "{:,}".format(base_cm * hh))])

    if t == 9:                                        # visual: the rearranged rectangle
        rows = random.randint(2, _by_d(d, 5, 7, 8))
        cols = random.randint(2, _by_d(d, 6, 9, 10))
        return {"prompt": "A parallelogram with a base of %d cm and a perpendicular "
                          "height of %d cm is cut and rearranged into this rectangle. "
                          "Each square is 1 cm². What is the area of the parallelogram, "
                          "in cm²?" % (cols, rows),
                "component": "area_grid",
                "spec": {"mode": "read_area", "rows": rows, "cols": cols},
                "answer": rows * cols, "answer_type": "int",
                "solution": ["The rectangle has the same base and height as the "
                             "parallelogram.",
                             "%d × %d = %d cm²." % (cols, rows, rows * cols)]}

    if t == 10:                                       # visual: shade the area
        rows = _by_d(d, 5, 6, 8)
        cols = _by_d(d, 6, 8, 10)
        bb = random.randint(2, min(cols, 6))
        hh = random.randint(2, min(rows, max(2, 24 // bb)))
        return {"prompt": "A parallelogram has a base of %d cm and a perpendicular height "
                          "of %d cm. Each square below is 1 cm². Shade squares to show "
                          "the same area. How many squares must you shade?" % (bb, hh),
                "component": "area_grid",
                "spec": {"mode": "build_area", "rows": rows, "cols": cols},
                "answer": bb * hh, "answer_type": "int",
                "solution": ["Area = base × perpendicular height.",
                             "%d × %d = %d cm², so shade %d squares."
                             % (bb, hh, bb * hh, bb * hh)]}

    if t == 0:                                        # direct
        return _num_q("A parallelogram has a base of %d cm and a perpendicular height of "
                      "%d cm. What is its area, in cm²?" % (b, h),
                      b * h, "int", unit="cm²",
                      solution=["Area of a parallelogram = base × perpendicular height.",
                                "%d × %d = %d cm²." % (b, h, b * h)])

    if t == 1:                                        # with a slant-side distractor
        slant = h + random.randint(1, 5)
        return _num_q("A parallelogram has a base of %d cm, a perpendicular height of "
                      "%d cm and sloping sides of %d cm. What is its area, in cm²?"
                      % (b, h, slant),
                      b * h, "int", unit="cm²",
                      solution=["Area uses the PERPENDICULAR height, not the sloping side.",
                                "%d × %d = %d cm²." % (b, h, b * h)])

    if t == 2:                                        # inverse: find the base
        return _num_q("A parallelogram has an area of %d cm² and a perpendicular height "
                      "of %d cm. What is its base, in cm?" % (b * h, h),
                      b, "int", unit="cm",
                      solution=["base = area ÷ height.",
                                "%d ÷ %d = %d cm." % (b * h, h, b)])

    if t == 3:                                        # inverse: find the height
        return _num_q("A parallelogram has an area of %d cm² and a base of %d cm. "
                      "What is its perpendicular height, in cm?" % (b * h, b),
                      h, "int", unit="cm",
                      solution=["height = area ÷ base.",
                                "%d ÷ %d = %d cm." % (b * h, b, h)])

    if t == 4:                                        # word problem
        who = pick(NAMES)
        return _num_q("%s cuts a parallelogram-shaped patch of felt with a base of %d cm "
                      "and a perpendicular height of %d cm. What is the area of the "
                      "patch, in cm²?" % (who, b, h),
                      b * h, "int", unit="cm²",
                      solution=["Area = base × perpendicular height.",
                                "%d × %d = %d cm²." % (b, h, b * h)])

    if t == 5:                                        # compare with a rectangle
        w = random.randint(lo, hi)
        hh = random.randint(lo, hi)
        while w * hh == b * h:
            w = random.randint(lo, hi)
        return _num_q("A parallelogram has a base of %d cm and a perpendicular height of "
                      "%d cm. A rectangle measures %d cm by %d cm. How many cm² larger is "
                      "the bigger area?" % (b, h, w, hh),
                      abs(b * h - w * hh), "int", unit="cm²",
                      solution=["Parallelogram: %d × %d = %d cm²." % (b, h, b * h),
                                "Rectangle: %d × %d = %d cm²." % (w, hh, w * hh),
                                "%d − %d = %d cm²." % (max(b * h, w * hh),
                                                       min(b * h, w * hh),
                                                       abs(b * h - w * hh))])

    if t == 6:                                        # two parallelograms
        b2 = random.randint(lo, hi)
        h2 = random.randint(lo, hi)
        return _num_q("A shape is made from two parallelograms joined edge to edge. One "
                      "has a base of %d cm and a height of %d cm; the other has a base of "
                      "%d cm and a height of %d cm. What is the total area, in cm²?"
                      % (b, h, b2, h2),
                      b * h + b2 * h2, "int", unit="cm²",
                      solution=["First: %d × %d = %d cm²." % (b, h, b * h),
                                "Second: %d × %d = %d cm²." % (b2, h2, b2 * h2),
                                "%d + %d = %d cm²." % (b * h, b2 * h2, b * h + b2 * h2)])

    if t == 7:                                        # why base x height (reasoning)
        return _num_q("A parallelogram can be cut and rearranged into a rectangle with "
                      "the same base and the same perpendicular height. A parallelogram "
                      "has a base of %d cm and a height of %d cm. What is the area of the "
                      "rectangle it makes, in cm²?" % (b, h),
                      b * h, "int", unit="cm²",
                      solution=["The rectangle has the same base and height.",
                                "%d × %d = %d cm²." % (b, h, b * h)])

    # doubling reasoning
    return _num_q("A parallelogram has a base of %d cm and a perpendicular height of "
                  "%d cm. The base is doubled but the height stays the same. What is the "
                  "new area, in cm²?" % (b, h),
                  2 * b * h, "int", unit="cm²",
                  solution=["The new base is 2 × %d = %d cm." % (b, 2 * b),
                            "%d × %d = %d cm²." % (2 * b, h, 2 * b * h)])


@skill("Y6.8.o", "Area of triangles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 4, 3])
    hi = _by_d(d, 10, 16, 30)
    b = 2 * random.randint(2, hi // 2)                 # even base keeps b x h / 2 exact
    h = random.randint(3, hi)

    if t == 9:                                        # visual: half the drawn rectangle
        rows = random.randint(2, _by_d(d, 5, 7, 8))
        cols = 2 * random.randint(1, _by_d(d, 3, 4, 5))
        return {"prompt": "A triangle has the same base and the same perpendicular height "
                          "as this rectangle, and each square is 1 cm². What is the area "
                          "of the TRIANGLE, in cm²?",
                "component": "area_grid",
                "spec": {"mode": "read_area", "rows": rows, "cols": cols},
                "answer": rows * cols // 2, "answer_type": "int",
                "solution": ["The rectangle is %d × %d = %d cm²." % (cols, rows,
                                                                     rows * cols),
                             "A triangle is half of that: %d ÷ 2 = %d cm²."
                             % (rows * cols, rows * cols // 2)]}

    if t == 10:                                       # visual: shade the triangle's area
        rows = _by_d(d, 5, 6, 8)
        cols = _by_d(d, 6, 8, 10)
        bb = 2 * random.randint(1, min(cols // 2, 4))
        hh = random.randint(2, min(rows, max(2, 48 // bb)))
        area = bb * hh // 2
        return {"prompt": "A triangle has a base of %d cm and a perpendicular height of "
                          "%d cm. Each square below is 1 cm². Shade squares to show the "
                          "same area. How many squares must you shade?" % (bb, hh),
                "component": "area_grid",
                "spec": {"mode": "build_area", "rows": rows, "cols": cols},
                "answer": area, "answer_type": "int",
                "solution": ["Area = ½ × base × height.",
                             "½ × %d × %d = %d cm², so shade %d squares."
                             % (bb, hh, area, area)]}

    if t == 0:                                        # direct
        return _num_q("A triangle has a base of %d cm and a perpendicular height of "
                      "%d cm. What is its area, in cm²?" % (b, h),
                      b * h // 2, "int", unit="cm²",
                      solution=["Area of a triangle = ½ × base × height.",
                                "%d × %d = %d, and %d ÷ 2 = %d cm²."
                                % (b, h, b * h, b * h, b * h // 2)])

    if t == 1:                                        # right-angled triangle
        return _num_q("A right-angled triangle has the two sides that meet at the right "
                      "angle measuring %d cm and %d cm. What is its area, in cm²?" % (b, h),
                      b * h // 2, "int", unit="cm²",
                      solution=["Those two sides are the base and the perpendicular "
                                "height.",
                                "½ × %d × %d = %d cm²." % (b, h, b * h // 2)])

    if t == 2:                                        # half a rectangle
        return _num_q("A rectangle measures %d cm by %d cm. A diagonal splits it into two "
                      "identical triangles. What is the area of ONE triangle, in cm²?"
                      % (b, h),
                      b * h // 2, "int", unit="cm²",
                      solution=["The rectangle's area is %d × %d = %d cm²." % (b, h, b * h),
                                "%d ÷ 2 = %d cm²." % (b * h, b * h // 2)])

    if t == 3:                                        # inverse: find the base
        area = b * h // 2
        return _num_q("A triangle has an area of %d cm² and a perpendicular height of "
                      "%d cm. What is its base, in cm?" % (area, h),
                      b, "int", unit="cm",
                      solution=["base = 2 × area ÷ height.",
                                "2 × %d = %d, and %d ÷ %d = %d cm."
                                % (area, 2 * area, 2 * area, h, b)])

    if t == 4:                                        # inverse: find the height
        area = b * h // 2
        return _num_q("A triangle has an area of %d cm² and a base of %d cm. "
                      "What is its perpendicular height, in cm?" % (area, b),
                      h, "int", unit="cm",
                      solution=["height = 2 × area ÷ base.",
                                "2 × %d = %d, and %d ÷ %d = %d cm."
                                % (area, 2 * area, 2 * area, b, h)])

    if t == 5:                                        # word problem
        who = pick(NAMES)
        thing = pick(["a triangular sail", "a triangular flag", "a bunting triangle",
                      "a triangular garden bed"])
        return _num_q("%s makes %s with a base of %d cm and a perpendicular height of "
                      "%d cm. What is its area, in cm²?" % (who, thing, b, h),
                      b * h // 2, "int", unit="cm²",
                      solution=["½ × %d × %d = %d cm²." % (b, h, b * h // 2)])

    if t == 6:                                        # slant distractor
        slant = h + random.randint(2, 6)
        return _num_q("A triangle has a base of %d cm, a perpendicular height of %d cm "
                      "and a sloping side of %d cm. What is its area, in cm²?"
                      % (b, h, slant),
                      b * h // 2, "int", unit="cm²",
                      solution=["Use the perpendicular height, not the sloping side.",
                                "½ × %d × %d = %d cm²." % (b, h, b * h // 2)])

    if t == 7:                                        # two triangles
        b2 = 2 * random.randint(2, hi // 2)
        h2 = random.randint(3, hi)
        return _num_q("A shape is made from two triangles. One has a base of %d cm and a "
                      "height of %d cm; the other has a base of %d cm and a height of "
                      "%d cm. What is the total area, in cm²?" % (b, h, b2, h2),
                      b * h // 2 + b2 * h2 // 2, "int", unit="cm²",
                      solution=["First: ½ × %d × %d = %d cm²." % (b, h, b * h // 2),
                                "Second: ½ × %d × %d = %d cm²." % (b2, h2, b2 * h2 // 2),
                                "%d + %d = %d cm²." % (b * h // 2, b2 * h2 // 2,
                                                       b * h // 2 + b2 * h2 // 2)])

    # triangle cut from a rectangle
    area = b * h // 2
    return _num_q("A triangle with a base of %d cm and a perpendicular height of %d cm is "
                  "cut out of a rectangle measuring %d cm by %d cm. What area of the "
                  "rectangle is left, in cm²?" % (b, h, b, h),
                  b * h - area, "int", unit="cm²",
                  solution=["Rectangle: %d × %d = %d cm²." % (b, h, b * h),
                            "Triangle: %d ÷ 2 = %d cm²." % (b * h, area),
                            "%d − %d = %d cm²." % (b * h, area, b * h - area)])


@skill("Y6.8.p", "Area of compound shapes", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # visual: L-shape area
        R = random.randint(3, _by_d(d, 5, 6, 8))
        C = random.randint(3, _by_d(d, 6, 8, 10))
        r_ = random.randint(1, R - 2)
        c_ = random.randint(1, C - 2)
        return {"prompt": "Each square is 1 cm². What is the area of this compound shape, "
                          "in cm²?",
                "component": "area_grid",
                "spec": {"mode": "read_area", "cells": _L_cells(R, C, r_, c_)},
                "answer": R * C - r_ * c_, "answer_type": "int",
                "solution": ["A full %d by %d rectangle would be %d cm²."
                             % (R, C, R * C),
                             "The missing piece is %d × %d = %d cm²."
                             % (r_, c_, r_ * c_),
                             "%d − %d = %d cm²." % (R * C, r_ * c_, R * C - r_ * c_)]}

    if t == 1:                                        # visual: area then perimeter
        R = random.randint(3, _by_d(d, 5, 6, 8))
        C = random.randint(3, _by_d(d, 6, 8, 10))
        r_ = random.randint(1, R - 2)
        c_ = random.randint(1, C - 2)
        return {"prompt": "Each square is 1 cm by 1 cm. What is the perimeter of this "
                          "compound shape, in cm?",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "cells": _L_cells(R, C, r_, c_)},
                "answer": 2 * (R + C), "answer_type": "int",
                "solution": ["Follow the outline all the way round.",
                             "The steps fit exactly into %s %d cm by %d cm rectangle: "
                             "2 × (%d + %d) = %d cm." % (_an(C), C, R, C, R, 2 * (R + C))]}

    if t == 2:                                        # L-shape from dimensions
        W = random.randint(6, _by_d(d, 12, 20, 30))
        H = random.randint(5, _by_d(d, 10, 18, 26))
        a = random.randint(2, W - 2)
        b = random.randint(2, H - 2)
        return _num_q("An L-shape is made by cutting %s %d cm by %d cm rectangle from "
                      "the corner of %s %d cm by %d cm rectangle. What is the area of the "
                      "L-shape, in cm²?" % (_an(a), a, b, _an(W), W, H),
                      W * H - a * b, "int", unit="cm²",
                      solution=["Whole rectangle: %d × %d = %d cm²." % (W, H, W * H),
                                "Cut-out: %d × %d = %d cm²." % (a, b, a * b),
                                "%d − %d = %d cm²." % (W * H, a * b, W * H - a * b)])

    if t == 3:                                        # two rectangles joined
        w1 = random.randint(3, _by_d(d, 8, 14, 25))
        h1 = random.randint(3, _by_d(d, 8, 14, 25))
        w2 = random.randint(3, _by_d(d, 8, 14, 25))
        h2 = random.randint(3, _by_d(d, 8, 14, 25))
        return _num_q("A compound shape is made from two rectangles joined edge to edge. "
                      "One measures %d cm by %d cm and the other measures %d cm by %d cm. "
                      "What is the total area, in cm²?" % (w1, h1, w2, h2),
                      w1 * h1 + w2 * h2, "int", unit="cm²",
                      solution=["First: %d × %d = %d cm²." % (w1, h1, w1 * h1),
                                "Second: %d × %d = %d cm²." % (w2, h2, w2 * h2),
                                "%d + %d = %d cm²." % (w1 * h1, w2 * h2,
                                                       w1 * h1 + w2 * h2)])

    if t == 4:                                        # rectangle + triangle
        w = random.randint(4, _by_d(d, 10, 16, 24))
        h = random.randint(3, _by_d(d, 8, 12, 20))
        th = 2 * random.randint(2, 6)
        return _num_q("A house shape is made from a rectangle %d cm by %d cm with a "
                      "triangular roof on top. The roof has a base of %d cm and a "
                      "perpendicular height of %d cm. What is the total area, in cm²?"
                      % (w, h, w, th),
                      w * h + w * th // 2, "int", unit="cm²",
                      solution=["Rectangle: %d × %d = %d cm²." % (w, h, w * h),
                                "Triangle: ½ × %d × %d = %d cm²." % (w, th, w * th // 2),
                                "%d + %d = %d cm²." % (w * h, w * th // 2,
                                                       w * h + w * th // 2)])

    if t == 5:                                        # hole cut out (middle)
        W = random.randint(8, _by_d(d, 14, 20, 30))
        H = random.randint(6, _by_d(d, 12, 18, 26))
        a = random.randint(2, W - 4)
        b = random.randint(2, H - 4)
        return _num_q("A rectangular sheet of card measures %d cm by %d cm. A rectangular "
                      "hole measuring %d cm by %d cm is cut out of the middle. What area "
                      "of card is left, in cm²?" % (W, H, a, b),
                      W * H - a * b, "int", unit="cm²",
                      solution=["Card: %d × %d = %d cm²." % (W, H, W * H),
                                "Hole: %d × %d = %d cm²." % (a, b, a * b),
                                "%d − %d = %d cm²." % (W * H, a * b, W * H - a * b)])

    if t == 6:                                        # missing length from area
        W = random.randint(6, _by_d(d, 12, 18, 26))
        H = random.randint(5, _by_d(d, 10, 16, 22))
        a = random.randint(2, W - 2)
        b = random.randint(2, H - 2)
        area = W * H - a * b
        return _num_q("An L-shape is made by cutting a rectangle %d cm wide out of the "
                      "corner of %s %d cm by %d cm rectangle. The L-shape has an area of "
                      "%d cm². How tall was the piece that was cut out, in cm?"
                      % (a, _an(W), W, H, area),
                      b, "int", unit="cm",
                      solution=["Whole rectangle: %d × %d = %d cm²." % (W, H, W * H),
                                "Cut-out area: %d − %d = %d cm²." % (W * H, area, a * b),
                                "%d ÷ %d = %d cm." % (a * b, a, b)])

    if t == 7:                                        # same area, different perimeter
        area = pick([12, 16, 18, 24, 36])
        pairs = [(w, area // w) for w in range(1, area + 1)
                 if area % w == 0 and w <= area // w]
        (w1, h1), (w2, h2) = random.sample(pairs, 2) if len(pairs) > 1 \
            else (pairs[0], pairs[0])
        p1, p2 = 2 * (w1 + h1), 2 * (w2 + h2)
        return _num_q("Two rectangles each have an area of %d cm². One measures %d cm by "
                      "%d cm and the other measures %d cm by %d cm. How many cm larger is "
                      "the bigger perimeter?" % (area, w1, h1, w2, h2),
                      abs(p1 - p2), "int", unit="cm",
                      solution=["First perimeter: 2 × (%d + %d) = %d cm." % (w1, h1, p1),
                                "Second perimeter: 2 × (%d + %d) = %d cm." % (w2, h2, p2),
                                "%d − %d = %d cm." % (max(p1, p2), min(p1, p2),
                                                      abs(p1 - p2))])

    if t == 8:                                        # area and perimeter of the same shape
        W = random.randint(5, _by_d(d, 10, 16, 24))
        H = random.randint(4, _by_d(d, 9, 14, 20))
        a = random.randint(2, W - 2)
        b = random.randint(2, H - 2)
        ask_area = random.random() < 0.5
        if ask_area:
            return _num_q("An L-shaped room is %s %d m by %d m rectangle with %s %d m by "
                          "%d m corner missing. What is the area of the floor, in m²?"
                          % (_an(W), W, H, _an(a), a, b),
                          W * H - a * b, "int", unit="m²",
                          solution=["%d × %d = %d m²." % (W, H, W * H),
                                    "%d × %d = %d m²." % (a, b, a * b),
                                    "%d − %d = %d m²." % (W * H, a * b, W * H - a * b)])
        return _num_q("An L-shaped room is %s %d m by %d m rectangle with %s %d m by "
                      "%d m corner missing. Skirting board runs all the way round the "
                      "outside of the L. How many metres of skirting board are needed?"
                      % (_an(W), W, H, _an(a), a, b),
                      2 * (W + H), "int", unit="m",
                      solution=["The L-shape's outline is the same length as the whole "
                                "rectangle's outline.",
                                "2 × (%d + %d) = %d m." % (W, H, 2 * (W + H))])

    # cost of covering a compound floor
    who = pick(NAMES)
    W = random.randint(5, 12)
    H = random.randint(4, 10)
    a = random.randint(2, W - 2)
    b = random.randint(2, H - 2)
    cost = pick([6, 8, 9, 12])
    area = W * H - a * b
    return _num_q("%s covers an L-shaped floor with carpet. The floor is %s %d m by "
                  "%d m rectangle with %s %d m by %d m corner missing. Carpet costs £%d "
                  "per square metre. What is the total cost, in pounds?"
                  % (who, _an(W), W, H, _an(a), a, b, cost),
                  area * cost, "int", unit="pounds",
                  solution=["Area = %d − %d = %d m²." % (W * H, a * b, area),
                            "%d × %d = %d pounds." % (area, cost, area * cost)])


@skill("Y6.8.q", "Volume of cubes and cuboids", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3])
    hi = _by_d(d, 6, 10, 20)
    l = random.randint(2, hi)
    w = random.randint(2, hi)
    h = random.randint(2, hi)

    if t == 11:                                       # compare volumes of cuboids (words)
        who = pick(NAMES)
        l2 = random.randint(2, hi)
        w2 = random.randint(2, hi)
        h2 = random.randint(2, hi)
        if l2 * w2 * h2 == l * w * h:                 # never let the two be equal
            h2 += 1
        va, vb = l * w * h, l2 * w2 * h2
        ask_which = random.random() < 0.5
        if ask_which:
            return _num_q("%s compares two cuboid boxes. Box A measures %d cm by %d cm by "
                          "%d cm and box B measures %d cm by %d cm by %d cm. Which box "
                          "has the larger volume? (type A or B)"
                          % (who, l, w, h, l2, w2, h2),
                          "A" if va > vb else "B", "str", text=True, placeholder="A / B",
                          solution=["Box A: %d × %d × %d = %d cm³." % (l, w, h, va),
                                    "Box B: %d × %d × %d = %d cm³." % (l2, w2, h2, vb),
                                    "Box %s has the larger volume."
                                    % ("A" if va > vb else "B")])
        return _num_q("%s compares two cuboid boxes. Box A measures %d cm by %d cm by "
                      "%d cm and box B measures %d cm by %d cm by %d cm. How many cm³ "
                      "more does the larger box hold?"
                      % (who, l, w, h, l2, w2, h2),
                      abs(va - vb), "int", unit="cm³",
                      solution=["Box A: %d × %d × %d = %d cm³." % (l, w, h, va),
                                "Box B: %d × %d × %d = %d cm³." % (l2, w2, h2, vb),
                                "%d − %d = %d cm³." % (max(va, vb), min(va, vb),
                                                       abs(va - vb))])

    if t == 12:                                       # compare dimensions, equal volumes
        who = pick(NAMES)
        a1 = random.randint(2, _by_d(d, 5, 8, 10))    # first cuboid: a1 x b1 x c1
        b1 = random.randint(2, _by_d(d, 5, 8, 10))
        k = pick([2, 3, 4])
        c1 = k * random.randint(1, _by_d(d, 3, 4, 6))
        vol = a1 * b1 * c1
        b2 = b1 * k                                   # second cuboid: a1 x b2 x c2
        c2 = c1 // k
        return _num_q("%s builds two cuboids with the same volume. The first cuboid "
                      "measures %d cm by %d cm by %d cm. The second cuboid has a base "
                      "measuring %d cm by %d cm. How tall is the second cuboid, in cm?"
                      % (who, a1, b1, c1, a1, b2),
                      c2, "int", unit="cm",
                      solution=["Volume of the first cuboid: %d × %d × %d = %d cm³."
                                % (a1, b1, c1, vol),
                                "Base area of the second cuboid: %d × %d = %d cm²."
                                % (a1, b2, a1 * b2),
                                "%d ÷ %d = %d cm." % (vol, a1 * b2, c2)])

    if t == 0:                                        # visual cuboid + dimensions
        nm = pick(["cube", "cuboid"])
        if nm == "cube":
            s = random.randint(2, _by_d(d, 6, 10, 15))
            return {"prompt": "This cube has edges of %d cm. What is its volume, in cm³?"
                              % s,
                    "component": "shape",
                    "spec": {"kind": "3d", "name": "cube", "ask": "faces"},
                    "answer": s ** 3, "answer_type": "int",
                    "solution": ["Volume of a cube = edge × edge × edge.",
                                 "%d × %d × %d = %d cm³." % (s, s, s, s ** 3)]}
        return {"prompt": "This cuboid measures %d cm by %d cm by %d cm. What is its "
                          "volume, in cm³?" % (l, w, h),
                "component": "shape",
                "spec": {"kind": "3d", "name": "cuboid", "ask": "faces"},
                "answer": l * w * h, "answer_type": "int",
                "solution": ["Volume = length × width × height.",
                             "%d × %d × %d = %d cm³." % (l, w, h, l * w * h)]}

    if t == 10:                                       # visual: cube edge from volume
        s = pick([2, 3, 4, 5, 6, 10])
        return {"prompt": "This cube has a volume of %d cm³. How long is each edge, "
                          "in cm?" % (s ** 3),
                "component": "shape",
                "spec": {"kind": "3d", "name": "cube", "ask": "edges"},
                "answer": s, "answer_type": "int",
                "solution": ["Find the number that multiplies by itself three times to "
                             "give %d." % (s ** 3),
                             "%d × %d × %d = %d, so each edge is %d cm."
                             % (s, s, s, s ** 3, s)]}

    if t == 1:                                        # bare cuboid volume
        return _num_q("A cuboid measures %d cm by %d cm by %d cm. What is its volume, "
                      "in cm³?" % (l, w, h),
                      l * w * h, "int", unit="cm³",
                      solution=["Volume = length × width × height.",
                                "%d × %d = %d, and %d × %d = %d cm³."
                                % (l, w, l * w, l * w, h, l * w * h)])

    if t == 2:                                        # cube volume
        s = random.randint(2, _by_d(d, 6, 10, 15))
        return _num_q("A cube has edges of %d cm. What is its volume, in cm³?" % s,
                      s ** 3, "int", unit="cm³",
                      solution=["Volume of a cube = edge × edge × edge.",
                                "%d × %d × %d = %d cm³." % (s, s, s, s ** 3)])

    if t == 3:                                        # missing dimension
        return _num_q("A cuboid has a volume of %d cm³. Its base measures %d cm by %d cm. "
                      "How tall is the cuboid, in cm?" % (l * w * h, l, w),
                      h, "int", unit="cm",
                      solution=["Base area = %d × %d = %d cm²." % (l, w, l * w),
                                "%d ÷ %d = %d cm." % (l * w * h, l * w, h)])

    if t == 4:                                        # from base area
        base = l * w
        return _num_q("A cuboid has a base area of %d cm² and a height of %d cm. "
                      "What is its volume, in cm³?" % (base, h),
                      base * h, "int", unit="cm³",
                      solution=["Volume = base area × height.",
                                "%d × %d = %d cm³." % (base, h, base * h)])

    if t == 5:                                        # cube edge from volume
        s = pick([2, 3, 4, 5, 6, 10])
        return _num_q("A cube has a volume of %d cm³. How long is each edge, in cm?"
                      % (s ** 3),
                      s, "int", unit="cm",
                      solution=["Find the number that multiplies by itself three times "
                                "to give %d." % (s ** 3),
                                "%d × %d × %d = %d, so each edge is %d cm."
                                % (s, s, s, s ** 3, s)])

    if t == 6:                                        # water tank in litres
        L = pick([10, 20, 25, 30, 40, 50])
        W = pick([10, 20, 25, 30, 40])
        H = pick([10, 20, 25, 30, 40])
        cm3 = L * W * H
        return _num_q("1000 cm³ of water is 1 litre. A tank measures %d cm by %d cm by "
                      "%d cm. How many litres of water does the tank hold when it is "
                      "full?" % (L, W, H),
                      cm3 / 1000.0, "num", unit="litres", tolerance=0.001,
                      solution=["Volume = %d × %d × %d = %d cm³." % (L, W, H, cm3),
                                "%d ÷ 1000 = %s %s." % (cm3, _f(cm3 / 1000.0), "litre" if cm3 == 1000 else "litres")])

    if t == 7:                                        # cubes in a box
        L, W, H = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
        c = pick([2, 3])
        return _num_q("A box measures %d cm by %d cm by %d cm. How many small cubes with "
                      "edges of 1 cm are needed to fill it completely?" % (L, W, H),
                      L * W * H, "int", unit="cubes",
                      solution=["Each 1 cm cube has a volume of 1 cm³.",
                                "%d × %d × %d = %d cubes." % (L, W, H, L * W * H)])

    if t == 8:                                        # compare two cuboids
        l2, w2, h2 = (random.randint(2, hi), random.randint(2, hi),
                      random.randint(2, hi))
        while l2 * w2 * h2 == l * w * h:
            l2 = random.randint(2, hi)
        return _num_q("Cuboid A measures %d cm by %d cm by %d cm. Cuboid B measures %d cm "
                      "by %d cm by %d cm. How many cm³ larger is the bigger volume?"
                      % (l, w, h, l2, w2, h2),
                      abs(l * w * h - l2 * w2 * h2), "int", unit="cm³",
                      solution=["A: %d × %d × %d = %d cm³." % (l, w, h, l * w * h),
                                "B: %d × %d × %d = %d cm³." % (l2, w2, h2, l2 * w2 * h2),
                                "%d − %d = %d cm³."
                                % (max(l * w * h, l2 * w2 * h2),
                                   min(l * w * h, l2 * w2 * h2),
                                   abs(l * w * h - l2 * w2 * h2))])

    # m3 / doubling
    if random.random() < 0.5:
        L, W, H = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        return _num_q("A storage container measures %d m by %d m by %d m. What is its "
                      "volume, in m³?" % (L, W, H),
                      L * W * H, "int", unit="m³",
                      solution=["Volume = %d × %d × %d = %d m³." % (L, W, H, L * W * H)])
    return _num_q("A cuboid measures %d cm by %d cm by %d cm. Its height is doubled and "
                  "the other measurements stay the same. What is the new volume, in cm³?"
                  % (l, w, h),
                  2 * l * w * h, "int", unit="cm³",
                  solution=["Old volume: %d × %d × %d = %d cm³." % (l, w, h, l * w * h),
                            "Doubling the height doubles the volume: %d × 2 = %d cm³."
                            % (l * w * h, 2 * l * w * h)])


# ================================================================== 6.9 ======
# (big unit, small unit, how many small in one big)
_METRIC = [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10),
           ("m", "mm", 1000), ("kg", "g", 1000), ("l", "ml", 1000),
           ("tonne", "kg", 1000)]
_UNIT_WORD = {"km": "kilometres", "m": "metres", "cm": "centimetres",
              "mm": "millimetres", "kg": "kilograms", "g": "grams",
              "l": "litres", "ml": "millilitres", "tonne": "tonnes"}


@skill("Y6.9.a", "Convert metric units", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 4, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3])
    big, small, k = pick(_METRIC if d else _METRIC[:5])

    if t == 12:                                       # choose the appropriate metric unit
        item, opts, ans = pick([
            ("the mass of an apple", "grams / kilograms / tonnes", "grams"),
            ("the mass of a lorry", "grams / kilograms / tonnes", "tonnes"),
            ("the mass of a Year 6 pupil", "grams / kilograms / tonnes", "kilograms"),
            ("the length of a pencil", "millimetres / centimetres / metres / kilometres",
             "centimetres"),
            ("the distance between two cities",
             "millimetres / centimetres / metres / kilometres", "kilometres"),
            ("the height of a door", "millimetres / centimetres / metres / kilometres",
             "metres"),
            ("the thickness of a one-pound coin",
             "millimetres / centimetres / metres / kilometres", "millimetres"),
            ("the water held by a teaspoon", "millilitres / litres", "millilitres"),
            ("the water held by a bath", "millilitres / litres", "litres"),
            ("the length of a football pitch",
             "millimetres / centimetres / metres / kilometres", "metres"),
        ])
        return _num_q("Choose the appropriate metric unit of measure for %s. (type one "
                      "word: %s)" % (item, opts),
                      ans, "str", text=True, placeholder=opts,
                      solution=["Think about the size of the thing being measured.",
                                "The appropriate metric unit is %s." % ans])

    if t == 13:                                       # more reasonable temperature
        thing, good, bad = pick([
            ("a cup of hot tea", 70, 7),
            ("a snowy winter morning", -3, 30),
            ("the water in a swimming pool", 27, 72),
            ("the inside of a fridge", 4, 40),
            ("water that is boiling", 100, 10),
            ("a warm summer day in the UK", 25, 65),
            ("the inside of a freezer", -18, 18),
            ("a comfortable classroom", 20, 45),
        ])
        first = random.random() < 0.5
        a, b = (good, bad) if first else (bad, good)
        return _num_q("Choose the more reasonable temperature for %s: %d °C or %d °C? "
                      "Write the number of degrees Celsius." % (thing, a, b),
                      good, "num", unit="°C", tolerance=0.001,
                      solution=["Compare each temperature with everyday experience.",
                                "The more reasonable temperature is %d °C." % good])

    if t == 14:                                       # multi-step metric conversions
        which = pick(["length", "mass", "capacity"])
        if which == "length":
            m = random.randint(3, _by_d(d, 6, 9, 15))
            n = random.randint(2, 5)
            each = pick([20, 25, 40, 50]) if m * 100 > 5 * 50 else 20
            while n * each >= m * 100:
                n -= 1
            cut = n * each
            return _num_q("This is a multi-step problem with metric unit conversions. "
                          "A rope is %d m long. %d pieces, each %d cm long, are cut off. "
                          "How many centimetres of rope are left?" % (m, n, each),
                          m * 100 - cut, "int", unit="cm",
                          solution=["%d m = %d cm." % (m, m * 100),
                                    "%d × %d = %d cm are cut off." % (n, each, cut),
                                    "%d − %d = %d cm." % (m * 100, cut, m * 100 - cut)])
        if which == "mass":
            kg = random.randint(2, _by_d(d, 5, 9, 15))
            n = random.randint(2, 6)
            each = pick([100, 150, 200, 250])
            while n * each >= kg * 1000:
                n -= 1
            used = n * each
            return _num_q("A bag of rice holds %d kg. %d portions, each %d g, are taken "
                          "out. How many grams of rice are left in the bag?"
                          % (kg, n, each),
                          kg * 1000 - used, "int", unit="g",
                          solution=["%d kg = %d g." % (kg, kg * 1000),
                                    "%d × %d = %d g are taken out." % (n, each, used),
                                    "%d − %d = %d g." % (kg * 1000, used,
                                                         kg * 1000 - used)])
        litres = random.randint(2, _by_d(d, 5, 8, 12))
        n = random.randint(2, 6)
        each = pick([150, 200, 250, 300])
        while n * each >= litres * 1000:
            n -= 1
        poured = n * each
        return _num_q("A jug holds %d litres of juice. %d glasses, each holding %d ml, "
                      "are poured out. How many millilitres of juice are left in the jug?"
                      % (litres, n, each),
                      litres * 1000 - poured, "int", unit="ml",
                      solution=["%s = %d ml." % (_pl(litres, "litre"), litres * 1000),
                                "%d × %d = %d ml are poured out." % (n, each, poured),
                                "%d − %d = %d ml." % (litres * 1000, poured,
                                                      litres * 1000 - poured)])

    if t == 15:                                       # precision
        if random.random() < 0.5:
            thing, opts, ans = pick([
                ("the length of a pencil", "metres / centimetres / millimetres",
                 "millimetres"),
                ("the mass of a letter", "tonnes / kilograms / grams", "grams"),
                ("the medicine in a spoon", "litres / millilitres", "millilitres"),
                ("the width of a fingernail", "metres / centimetres / millimetres",
                 "millimetres"),
            ])
            return _num_q("Precision means measuring in the smallest sensible unit. Which "
                          "unit would measure %s with the most precision? (type one word: "
                          "%s)" % (thing, opts),
                          ans, "str", text=True, placeholder=opts,
                          solution=["The smaller the unit, the more precise the "
                                    "measurement.",
                                    "The most precise of these units is %s." % ans])
        whole = random.randint(3, 19)
        one_dp = round(whole + pick([1, 2, 3, 4, 6, 7, 8, 9]) / 10.0, 1)
        two_dp = round(one_dp + pick([1, 2, 3, 4, 5, 6, 7, 8, 9]) / 100.0, 2)
        return _num_q("Three pupils measure the same pencil and record %d cm, %s cm and "
                      "%s cm. Which measurement is the most precise? Write it in "
                      "centimetres, as a number only."
                      % (whole, _f(one_dp), _f(two_dp)),
                      two_dp, "num", unit="cm", tolerance=0.0005,
                      solution=["The most precise measurement is the one recorded to the "
                                "smallest part of a centimetre.",
                                "%s cm is measured to the nearest hundredth of a "
                                "centimetre." % _f(two_dp)])

    if t == 10:                                       # ruler: read cm, answer in mm
        mx = pick([10, 15, 20])
        v = random.randint(1, mx)
        return {"prompt": "Read the ruler. How long is the line, in millimetres?",
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm"},
                "answer": v * 10, "answer_type": "int",
                "solution": ["The line measures %d cm." % v,
                             "1 cm = 10 mm, so %d × 10 = %d mm." % (v, v * 10)]}

    if t == 11:                                       # scale / jug: answer in the big unit
        if random.random() < 0.5:
            v = random.randrange(50, 1000, 50)
            return {"prompt": "Read the scale. What is the mass, in kilograms? "
                              "Give your answer as a decimal.",
                    "component": "ruler",
                    "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                    "answer": v / 1000.0, "answer_type": "num", "tolerance": 0.0005,
                    "solution": ["The pointer is at %d g." % v,
                                 "%d ÷ 1000 = %s kg." % (v, _f(v / 1000.0))]}
        v = random.randrange(50, 1000, 50)
        return {"prompt": "Read the jug. How many litres of liquid does it hold? "
                          "Give your answer as a decimal.",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v / 1000.0, "answer_type": "num", "tolerance": 0.0005,
                "solution": ["The liquid reaches the %d ml mark." % v,
                             "%d ÷ 1000 = %s %s." % (v, _f(v / 1000.0), "litre" if v == 1000 else "litres")]}

    def _small_val():
        if d == 0:
            return k * random.randint(1, 9)
        if d == 1:
            return k * random.randint(1, 9) + (k // 10) * random.randint(0, 9)
        return random.randint(k // 2, 20 * k)

    if t == 0:                                        # small -> big (decimals)
        v = _small_val()
        return _num_q("Convert %d %s into %s. Write your answer as a decimal if you need "
                      "to." % (v, small, _UNIT_WORD[big]),
                      v / float(k), "num", unit=big, tolerance=0.0005,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%d ÷ %d = %s %s." % (v, k, _f(v / float(k)), big)])

    if t == 1:                                        # big -> small
        whole = random.randint(1, _by_d(d, 9, 20, 60))
        frac = pick([0, 0.5, 0.25, 0.75, 0.1, 0.2, 0.125, 0.375, 0.05])
        v = whole + frac
        small_v = v * k
        if abs(small_v - round(small_v)) > 1e-9:
            v = whole + 0.5
            small_v = v * k
        return _num_q("Convert %s %s into %s." % (_f(v), big, _UNIT_WORD[small]),
                      int(round(small_v)), "int", unit=small,
                      solution=["1 %s = %d %s." % (big, k, small),
                                "%s × %d = %d %s." % (_f(v), k, int(round(small_v)),
                                                      small)])

    if t == 2:                                        # conversion table with a gap
        big2, small2, k2 = pick(_METRIC[:5])
        vals = sorted(random.sample(range(1, 20), 4))
        headers = [_UNIT_WORD[big2].capitalize(), _UNIT_WORD[small2].capitalize()]
        rows = [[_f(v / 2.0), str(int(v * k2 / 2))] for v in vals]
        i = random.randrange(4)
        j = random.randrange(2)
        ans = rows[i][j]
        blank = [list(r) for r in rows]
        blank[i][j] = "?"
        return {"prompt": "This table converts %s into %s. What number belongs in the "
                          "cell marked ?" % (_UNIT_WORD[big2], _UNIT_WORD[small2]),
                "component": "data_table",
                "spec": {"caption": "%s and %s" % (headers[0], headers[1]),
                         "headers": headers, "rows": blank, "missing": [i, j]},
                "answer": float(ans), "answer_type": "num", "tolerance": 0.0005,
                "solution": ["1 %s = %d %s." % (big2, k2, small2),
                             "The missing number is %s." % ans]}

    if t == 3:                                        # compare two measures
        v1 = _small_val()
        v2 = round(random.uniform(0.5, 15.0), 3)
        while abs(v1 - v2 * k) < 1e-9:
            v2 = round(random.uniform(0.5, 15.0), 3)
        bigger = "A" if v1 > v2 * k else "B"
        return _num_q("Measurement A is %d %s. Measurement B is %s %s. Which is larger? "
                      "(type A or B)" % (v1, small, _f(v2), big),
                      bigger, "str", text=True, placeholder="A / B",
                      solution=["B is %s %s = %s %s."
                                % (_f(v2), big, _f(v2 * k), small),
                                "%s %s is larger, so the answer is %s."
                                % (_f(max(v1, v2 * k)), small, bigger)])

    if t == 4:                                        # add two mixed measures
        a = random.randint(1, 9)
        b = random.randint(1, k - 1) if k <= 100 else random.randint(1, 999)
        total = a * k + b
        return _num_q("Add %d %s and %d %s. Write the total in %s." % (a, big, b, small,
                                                                       _UNIT_WORD[small]),
                      total, "int", unit=small,
                      solution=["%d %s = %d %s." % (a, big, a * k, small),
                                "%d + %d = %d %s." % (a * k, b, total, small)])

    if t == 5:                                        # word problem: total mass
        who = pick(NAMES)
        n = random.randint(3, 8)
        each = random.randint(150, 950)
        total = n * each
        return _num_q("%s buys %d bags of flour. Each bag weighs %d g. What is the total "
                      "mass, in kilograms?" % (who, n, each),
                      total / 1000.0, "num", unit="kg", tolerance=0.0005,
                      solution=["%d × %d = %d g." % (n, each, total),
                                "%d ÷ 1000 = %s kg." % (total, _f(total / 1000.0))])

    if t == 6:                                        # remaining after using some
        cap = pick([1, 2, 3, 5])
        used = random.randint(100, cap * 1000 - 100)
        left = cap * 1000 - used
        return _num_q("A bottle holds %d litre%s of water. %d ml is poured out. "
                      "How many millilitres are left?"
                      % (cap, "" if cap == 1 else "s", used),
                      left, "int", unit="ml",
                      solution=["%s = %d ml." % (_pl(cap, "litre"), cap * 1000),
                                "%d − %d = %d ml." % (cap * 1000, used, left)])

    if t == 7:                                        # order three measures
        v = [random.randint(1, 9000) for _ in range(3)]
        while len(set(v)) < 3:
            v = [random.randint(1, 9000) for _ in range(3)]
        return _num_q("Three lengths are %d m, %s km and %d cm. Write the LONGEST of the "
                      "three in metres." % (v[0], _f(v[1] / 1000.0), v[2]),
                      max(v[0], v[1], v[2] / 100.0), "num", unit="m", tolerance=0.005,
                      solution=["%s km = %d m and %d cm = %s m."
                                % (_f(v[1] / 1000.0), v[1], v[2], _f(v[2] / 100.0)),
                                "The longest is %s m."
                                % _f(max(v[0], v[1], v[2] / 100.0))])

    if t == 8:                                        # scale up 3 dp
        v = random.randint(1, 999)
        return _num_q("A parcel weighs %d g. What is its mass in kilograms? "
                      "Give your answer as a decimal." % v,
                      v / 1000.0, "num", unit="kg", tolerance=0.0005,
                      solution=["1 kg = 1000 g.",
                                "%d ÷ 1000 = %s kg." % (v, _f(v / 1000.0))])

    # multi-step: distance in km
    who = pick(NAMES)
    legs = random.randint(3, 5)
    each = random.randint(150, 900)
    total = legs * each
    return _num_q("%s runs %d laps of a track. Each lap is %d m. What is the total "
                  "distance, in kilometres?" % (who, legs, each),
                  total / 1000.0, "num", unit="km", tolerance=0.0005,
                  solution=["%d × %d = %d m." % (legs, each, total),
                            "%d ÷ 1000 = %s km." % (total, _f(total / 1000.0))])


# (singular, plural, other unit, factor, the stated fact, is the fact approximate?)
_IMPERIAL = [
    ("inch", "inches", "cm", 2.5, "1 inch is about 2.5 cm", True),
    ("foot", "feet", "inches", 12, "1 foot = 12 inches", False),
    ("yard", "yards", "feet", 3, "1 yard = 3 feet", False),
    ("pound", "pounds", "g", 450, "1 pound is about 450 g", True),
    ("stone", "stone", "pounds", 14, "1 stone = 14 pounds", False),
    ("pint", "pints", "ml", 568, "1 pint is about 568 ml", True),
    ("gallon", "gallons", "pints", 8, "1 gallon = 8 pints", False),
]


@skill("Y6.9.b", "Miles, kilometres and imperial equivalences", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 6, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3])

    if t == 10:                                       # appropriate imperial unit
        item, opts, ans = pick([
            ("the width of a book", "inches / feet / yards / miles", "inches"),
            ("the height of a room", "inches / feet / yards / miles", "feet"),
            ("the distance from London to Manchester",
             "inches / feet / yards / miles", "miles"),
            ("the length of a cricket pitch", "inches / feet / yards / miles", "yards"),
            ("the weight of a letter", "ounces / pounds / stone", "ounces"),
            ("the weight of a bag of potatoes", "ounces / pounds / stone", "pounds"),
            ("the weight of an adult", "ounces / pounds / stone", "stone"),
            ("the milk in a small carton", "pints / gallons", "pints"),
            ("the petrol in a car's tank", "pints / gallons", "gallons"),
        ])
        return _num_q("Choose the appropriate imperial unit of measure for %s. (type one "
                      "word: %s)" % (item, opts),
                      ans, "str", text=True, placeholder=opts,
                      solution=["Think about the size of the thing being measured.",
                                "The appropriate imperial unit is %s." % ans])

    if t == 11:                                       # compare and convert imperial length
        big, small, f, one = pick([("feet", "inches", 12, "foot"),
                                   ("yards", "feet", 3, "yard")])
        a = random.randint(2, _by_d(d, 5, 8, 12))
        b = (a * f + pick([-7, -5, -2, -1, 1, 2, 5, 7]) if f == 12
             else a * f + pick([-2, -1, 1, 2]))
        if b < 1:
            b = a * f + f // 2 + 1
        ans = "A" if a * f > b else "B"
        return _num_q("Compare and convert these imperial units of length. 1 %s = %d %s. "
                      "Length A is %d %s and length B is %d %s. Which length is longer? "
                      "(type A or B)" % (one, f, small, a, big, b, small),
                      ans, "str", text=True, placeholder="A / B",
                      solution=["A is %d × %d = %d %s." % (a, f, a * f, small),
                                "%d %s against %d %s, so %s is longer."
                                % (a * f, small, b, small, ans)])

    if t == 12:                                       # compare and convert imperial weight
        big, small, f = pick([("stone", "pounds", 14), ("pounds", "ounces", 16)])
        a = random.randint(2, _by_d(d, 5, 8, 12))
        b = a * f + pick([-9, -6, -3, -1, 1, 3, 6, 9])
        if b < 1:
            b = a * f + f // 2 + 1
        ans = "A" if a * f > b else "B"
        one = "stone" if big == "stone" else "pound"
        return _num_q("Compare and convert these imperial units of weight. 1 %s = %d %s. "
                      "Weight A is %d %s and weight B is %d %s. Which weight is heavier? "
                      "(type A or B)" % (one, f, small, a, big, b, small),
                      ans, "str", text=True, placeholder="A / B",
                      solution=["A is %d × %d = %d %s." % (a, f, a * f, small),
                                "%d %s against %d %s, so %s is heavier."
                                % (a * f, small, b, small, ans)])

    if t == 13:                                       # compare and convert imperial volume
        big, small, f, one = pick([("gallons", "pints", 8, "gallon"),
                                   ("pints", "fluid ounces", 20, "pint")])
        a = random.randint(2, _by_d(d, 4, 6, 9))
        b = a * f + pick([-7, -4, -2, -1, 1, 2, 4, 7])
        if b < 1:
            b = a * f + f // 2 + 1
        ans = "A" if a * f > b else "B"
        return _num_q("Compare and convert these imperial units of volume. 1 %s = %d %s. "
                      "Container A holds %d %s and container B holds %d %s. Which "
                      "container holds more? (type A or B)"
                      % (one, f, small, a, big, b, small),
                      ans, "str", text=True, placeholder="A / B",
                      solution=["A holds %d × %d = %d %s." % (a, f, a * f, small),
                                "%d %s against %d %s, so %s holds more."
                                % (a * f, small, b, small, ans)])

    if t == 14:                                       # mixed imperial units
        big, small, f, one = pick([("feet", "inches", 12, "foot"),
                                   ("yards", "feet", 3, "yard"),
                                   ("stone", "pounds", 14, "stone"),
                                   ("pounds", "ounces", 16, "pound"),
                                   ("gallons", "pints", 8, "gallon")])
        a = random.randint(2, _by_d(d, 5, 9, 15))
        b = random.randint(2, f - 1)
        return _num_q("Imperial measurements are often written in mixed units. "
                      "1 %s = %d %s. Write %d %s %d %s as a number of %s."
                      % (one, f, small, a, big, b, small, small),
                      a * f + b, "int", unit=small,
                      solution=["%d %s = %d %s." % (a, big, a * f, small),
                                "%d + %d = %d %s." % (a * f, b, a * f + b, small)])

    if t == 0:                                        # miles -> km
        miles = 5 * random.randint(1, _by_d(d, 6, 12, 30))
        return _num_q("5 miles is about 8 km. About how many kilometres is %d miles?"
                      % miles,
                      miles // 5 * 8, "int", unit="km",
                      solution=["%d ÷ 5 = %s of 5 miles." % (miles, _pl(miles // 5, "lot")),
                                "%d × 8 = %d km." % (miles // 5, miles // 5 * 8)])

    if t == 1:                                        # km -> miles
        km = 8 * random.randint(1, _by_d(d, 6, 12, 30))
        return _num_q("8 km is about 5 miles. About how many miles is %d km?" % km,
                      km // 8 * 5, "int", unit="miles",
                      solution=["%d ÷ 8 = %s of 8 km." % (km, _pl(km // 8, "lot")),
                                "%d × 5 = %d miles." % (km // 8, km // 8 * 5)])

    if t == 2:                                        # conversion table
        rows = []
        base = random.randint(1, 5)
        for i in range(4):
            m = 5 * (base + i)
            rows.append([str(m), str(m // 5 * 8)])
        i = random.randrange(4)
        j = random.randrange(2)
        ans = int(rows[i][j])
        blank = [list(r) for r in rows]
        blank[i][j] = "?"
        return {"prompt": "This table converts miles into kilometres, using 5 miles ≈ "
                          "8 km. What number belongs in the cell marked ?",
                "component": "data_table",
                "spec": {"caption": "Miles and kilometres", "headers": ["Miles", "km"],
                         "rows": blank, "missing": [i, j]},
                "answer": ans, "answer_type": "int",
                "solution": ["Every 5 miles is 8 km.",
                             "The missing number is %d." % ans]}

    if t == 3:                                        # inch / foot / yard
        sing, plur, unit, factor, fact, approx = pick(_IMPERIAL[:3])
        n = random.randint(2, _by_d(d, 6, 12, 20))
        val = n * factor
        return _num_q("%s. %s many %s are there in %d %s?"
                      % (fact, "About how" if approx else "How", unit, n,
                         plur if n != 1 else sing),
                      val, "num", unit=unit, tolerance=0.05,
                      solution=[fact + ".",
                                "%d × %s = %s %s." % (n, _f(factor), _f(val), unit)])

    if t == 4:                                        # mass / capacity
        sing, plur, unit, factor, fact, approx = pick(_IMPERIAL[3:])
        n = random.randint(2, _by_d(d, 5, 9, 15))
        val = n * factor
        return _num_q("%s. %s many %s are there in %d %s?"
                      % (fact, "About how" if approx else "How", unit, n, plur),
                      val, "num", unit=unit, tolerance=0.5,
                      solution=[fact + ".",
                                "%d × %s = %s %s." % (n, _f(factor), _f(val), unit)])

    if t == 5:                                        # inverse
        sing, plur, unit, factor, fact, approx = pick(_IMPERIAL)
        n = random.randint(2, 12)
        val = n * factor
        return _num_q("%s. %s many %s are there in %s %s?"
                      % (fact, "About how" if approx else "How", plur, _f(val), unit),
                      n, "num", unit=plur, tolerance=0.05,
                      solution=[fact + ".",
                                "%s ÷ %s = %d %s." % (_f(val), _f(factor), n, plur)])

    if t == 6:                                        # road sign word problem
        who = pick(NAMES)
        km = 8 * random.randint(2, 12)
        return _num_q("A road sign says the next town is %d km away. Using 8 km ≈ 5 "
                      "miles, about how many miles away is the town?" % km,
                      km // 8 * 5, "int", unit="miles",
                      solution=["%d ÷ 8 = %d." % (km, km // 8),
                                "%d × 5 = %d miles." % (km // 8, km // 8 * 5)])

    if t == 7:                                        # compare
        miles = 5 * random.randint(2, 12)
        km = random.randint(10, 120)
        while km == miles // 5 * 8:
            km = random.randint(10, 120)
        ans = "A" if miles // 5 * 8 > km else "B"
        return _num_q("Journey A is %d miles. Journey B is %d km. Using 5 miles ≈ 8 km, "
                      "which journey is longer? (type A or B)" % (miles, km),
                      ans, "str", text=True, placeholder="A / B",
                      solution=["Journey A is about %d ÷ 5 × 8 = %d km."
                                % (miles, miles // 5 * 8),
                                "%d km against %d km, so %s is longer."
                                % (miles // 5 * 8, km, ans)])

    if t == 8:                                        # weight in stone and pounds
        st = random.randint(4, 14)
        lb = random.randint(0, 13)
        return _num_q("1 stone = 14 pounds. How many pounds is %d stone %s?"
                      % (st, _pl(lb, "pound")),
                      st * 14 + lb, "int", unit="pounds",
                      solution=["%d × 14 = %d pounds." % (st, st * 14),
                                "%d + %d = %d pounds." % (st * 14, lb, st * 14 + lb)])

    # gallons -> litres via pints
    gal = random.randint(1, 6)
    pints = gal * 8
    ml = pints * 568
    return _num_q("1 gallon = 8 pints and 1 pint is about 568 ml. About how many "
                  "millilitres are there in %d gallon%s?"
                  % (gal, "" if gal == 1 else "s"),
                  ml, "num", unit="ml", tolerance=1,
                  solution=["%d × 8 = %d pints." % (gal, pints),
                            "%d × 568 = %d ml." % (pints, ml)])


def _hm(h, m):
    return "%d:%02d" % (h, m)


def _hm24(h, m):
    return "%02d:%02d" % (h, m)


_CITIES = [("New York", -5), ("Los Angeles", -8), ("Rio de Janeiro", -4),
           ("Cairo", 2), ("Moscow", 3), ("Dubai", 4), ("Karachi", 5),
           ("Bangkok", 7), ("Beijing", 8), ("Tokyo", 9), ("Sydney", 11)]


@skill("Y6.9.c", "Time problems and 24-hour clock", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 1, 1, 1, 4, 1, 1, 1, 1, 3, 3, 4])

    if t == 12:                                       # find start and end times (words)
        who = pick(NAMES)
        event, place = pick([("swimming lesson", "the pool"),
                             ("music rehearsal", "the hall"),
                             ("science club", "the lab"),
                             ("football match", "the park"),
                             ("art workshop", "the studio")])
        mins = random.randint(_by_d(d, 20, 35, 45), _by_d(d, 75, 140, 220))
        h1 = random.randint(8, 18)
        m1 = random.randrange(0, 60, 5)
        start = h1 * 60 + m1
        end = start + mins
        if random.random() < 0.5:
            return _num_q("%s arrives at %s and the %s starts at %s. The %s lasts %d "
                          "minutes. Find the end time. Write the answer as a 24-hour "
                          "clock time, in the form 14:30."
                          % (who, place, event, _hm24(h1, m1), event, mins),
                          _hm24((end // 60) % 24, end % 60), "str", text=True,
                          placeholder="e.g. 14:30",
                          solution=["%d minutes is %s and %s."
                                    % (mins, _pl(mins // 60, "hour"), _pl(mins % 60, "minute")),
                                    "%s + %d minutes = %s."
                                    % (_hm24(h1, m1), mins,
                                       _hm24((end // 60) % 24, end % 60))])
        return _num_q("The %s that %s attends ends at %s and lasts %d minutes. Find the "
                      "start time. Write the answer as a 24-hour clock time, in the form "
                      "14:30." % (event, who, _hm24((end // 60) % 24, end % 60), mins),
                      _hm24(h1, m1), "str", text=True, placeholder="e.g. 14:30",
                      solution=["Count back %d minutes from %s."
                                % (mins, _hm24((end // 60) % 24, end % 60)),
                                "The %s started at %s." % (event, _hm24(h1, m1))])

    if t == 10:                                       # clock: set a 24-hour time
        h24 = random.randint(13, 23)
        m = random.randrange(0, 60, 5)
        return {"prompt": "A timetable shows %s. Set the clock to show that time."
                          % _hm24(h24, m),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h24 - 12, m), "answer_type": "time",
                "solution": ["%s in 12-hour time is %s."
                             % (_hm24(h24, m), _hm(h24 - 12, m)),
                             "Put the hour hand %s %d and the minute hand on %d."
                             % ("on" if m == 0 else "just past", h24 - 12, m // 5 or 12)]}

    if t == 11:                                       # clock: set the finish time
        h = random.randint(1, 11)
        m = random.randrange(0, 60, 5)
        mins = random.randint(10, 55)
        end = h * 60 + m + mins
        eh, em = (end // 60), end % 60
        if eh > 12:
            eh -= 12
        return {"prompt": "An activity starts at %s and lasts %d minutes. Set the clock "
                          "to the time it finishes." % (_hm(h, m), mins),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(eh, em), "answer_type": "time",
                "solution": ["%s + %d minutes = %s." % (_hm(h, m), mins, _hm(eh, em)),
                             "Set the hour hand %s %d and the minute hand on %d."
                             % ("on" if em == 0 else "just past", eh, em // 5 or 12)]}

    if t == 0:                                        # journey length in minutes
        h1 = random.randint(6, 18)
        m1 = random.randrange(0, 60, 5)
        mins = random.randint(_by_d(d, 20, 40, 70), _by_d(d, 90, 180, 300))
        start = h1 * 60 + m1
        end = start + mins
        return _num_q("A train leaves at %s and arrives at %s (24-hour clock). "
                      "How many minutes does the journey take?"
                      % (_hm24(h1, m1), _hm24((end // 60) % 24, end % 60)),
                      mins, "int", unit="minutes",
                      solution=["From %s to %s." % (_hm24(h1, m1),
                                                    _hm24((end // 60) % 24, end % 60)),
                                "That is %s and %s = %d minutes."
                                % (_pl(mins // 60, "hour"), _pl(mins % 60, "minute"), mins)])

    if t == 1:                                        # 12h -> 24h
        h = random.randint(1, 11)
        m = random.randrange(0, 60, 5)
        pm = random.random() < 0.5
        h24 = h + 12 if pm else h
        return _num_q("Write %s %s as a 24-hour clock time, in the form %s."
                      % (_hm(h, m), "pm" if pm else "am", "14:30"),
                      _hm24(h24, m), "str", text=True, placeholder="e.g. 14:30",
                      solution=["For pm times, add 12 to the hours." if pm else
                                "For am times before 10, write a zero in front of the "
                                "hours.",
                                "%s %s is %s." % (_hm(h, m), "pm" if pm else "am",
                                                  _hm24(h24, m))])

    if t == 2:                                        # 24h -> 12h
        h24 = random.randint(13, 23)
        m = random.randrange(0, 60, 5)
        return _num_q("A timetable shows %s. Write that time on a 12-hour clock, in the "
                      "form 2:30 (the pm is understood)." % _hm24(h24, m),
                      _hm(h24 - 12, m), "time",
                      solution=["Subtract 12 from the hours: %d − 12 = %d."
                                % (h24, h24 - 12),
                                "%s is %s pm." % (_hm24(h24, m), _hm(h24 - 12, m))])

    if t == 3:                                        # finish time
        h1 = random.randint(7, 20)
        m1 = random.randrange(0, 60, 5)
        mins = random.randint(_by_d(d, 15, 35, 55), _by_d(d, 80, 150, 260))
        end = h1 * 60 + m1 + mins
        return _num_q("A film starts at %s and lasts %d minutes. At what time does it "
                      "finish? Write the answer as a 24-hour clock time, in the form "
                      "14:30." % (_hm24(h1, m1), mins),
                      _hm24((end // 60) % 24, end % 60), "str", text=True,
                      placeholder="e.g. 14:30",
                      solution=["%d minutes is %s and %s."
                                % (mins, _pl(mins // 60, "hour"), _pl(mins % 60, "minute")),
                                "%s + %d minutes = %s."
                                % (_hm24(h1, m1), mins,
                                   _hm24((end // 60) % 24, end % 60))])

    if t == 4:                                        # start time (inverse)
        h2 = random.randint(9, 22)
        m2 = random.randrange(0, 60, 5)
        mins = random.randint(20, _by_d(d, 60, 120, 200))
        start = h2 * 60 + m2 - mins
        while start < 0:
            mins = random.randint(20, 60)
            start = h2 * 60 + m2 - mins
        return _num_q("A lesson finished at %s and lasted %d minutes. At what time did it "
                      "start? Write the answer as a 24-hour clock time, in the form 14:30."
                      % (_hm24(h2, m2), mins),
                      _hm24(start // 60, start % 60), "str", text=True,
                      placeholder="e.g. 14:30",
                      solution=["Count back %d minutes from %s." % (mins, _hm24(h2, m2)),
                                "The lesson started at %s."
                                % _hm24(start // 60, start % 60)])

    if t == 5:                                        # timetable (data_table)
        stops = random.sample(["Ashford", "Bewley", "Carlton", "Denham", "Eastgate",
                               "Fairholme"], 4)
        h = random.randint(6, 18)
        m = random.randrange(0, 60, 5)
        gaps = [random.randint(8, 35) for _ in range(3)]
        times = [h * 60 + m]
        for g in gaps:
            times.append(times[-1] + g)
        rows = [[s, _hm24((tm // 60) % 24, tm % 60)] for s, tm in zip(stops, times)]
        i = random.randrange(3)
        return {"prompt": "This is a bus timetable. How many minutes does the bus take to "
                          "get from %s to %s?" % (stops[i], stops[i + 1]),
                "component": "data_table",
                "spec": {"caption": "Bus timetable", "headers": ["Stop", "Time"],
                         "rows": rows},
                "answer": gaps[i], "answer_type": "int",
                "solution": ["%s: %s and %s: %s."
                             % (stops[i], rows[i][1], stops[i + 1], rows[i + 1][1]),
                             "The gap is %d minutes." % gaps[i]]}

    if t == 6:                                        # time zone
        city, off = pick(_CITIES)
        h = random.randint(6, 20)
        m = random.randrange(0, 60, 15)
        local = (h + off) % 24
        return _num_q("When it is %s in London, %s is %d hour%s %s. What is the time in "
                      "%s? Write the answer as a 24-hour clock time, in the form 14:30."
                      % (_hm24(h, m), city, abs(off), "" if abs(off) == 1 else "s",
                         "ahead" if off > 0 else "behind", city),
                      _hm24(local, m), "str", text=True, placeholder="e.g. 14:30",
                      solution=["%d %s %d = %d." % (h, "+" if off > 0 else "−",
                                                    abs(off), (h + off) % 24),
                                "The time in %s is %s." % (city, _hm24(local, m))])

    if t == 7:                                        # time zone flight
        city, off = pick(_CITIES)
        dep_h = random.randint(6, 14)
        dep_m = random.randrange(0, 60, 15)
        flight = random.randint(3, 12) * 60 + random.randrange(0, 60, 15)
        arrive_uk = dep_h * 60 + dep_m + flight
        local = (arrive_uk + off * 60) % (24 * 60)
        return _num_q("A plane leaves London at %s and flies for %d hours and %d minutes. "
                      "%s is %d hour%s %s London time. What is the local time in %s when "
                      "the plane lands? Write the answer as a 24-hour clock time, in the "
                      "form 14:30."
                      % (_hm24(dep_h, dep_m), flight // 60, flight % 60, city,
                         abs(off), "" if abs(off) == 1 else "s",
                         "ahead of" if off > 0 else "behind", city),
                      _hm24(local // 60, local % 60), "str", text=True,
                      placeholder="e.g. 14:30",
                      solution=["Landing time in London time: %s."
                                % _hm24((arrive_uk // 60) % 24, arrive_uk % 60),
                                "Then %s %d hours gives %s."
                                % ("add" if off > 0 else "take off", abs(off),
                                   _hm24(local // 60, local % 60))])

    if t == 8:                                        # days / hours / minutes
        val, frm, to, factor = pick([(random.randint(2, 9), "days", "hours", 24),
                                     (random.randint(2, 9), "hours", "minutes", 60),
                                     (random.randint(2, 9), "minutes", "seconds", 60),
                                     (random.randint(2, 8), "weeks", "days", 7),
                                     (random.randint(2, 6), "years", "months", 12)])
        return _num_q("How many %s are there in %d %s?" % (to, val, frm),
                      val * factor, "int", unit=to,
                      solution=["1 %s = %d %s." % (frm[:-1], factor, to),
                                "%d × %d = %d %s." % (val, factor, val * factor, to)])

    # total time across several activities
    who = pick(NAMES)
    n = random.randint(3, 5)
    mins = [random.randint(15, 75) for _ in range(n)]
    total = sum(mins)
    return _num_q("%s does %d activities lasting %s minutes. What is the total time, in "
                  "hours and minutes? Write only the number of MINUTES left over after "
                  "the whole hours." % (who, n, ", ".join(str(x) for x in mins)),
                  total % 60, "int", unit="minutes",
                  solution=["%s = %d minutes." % (" + ".join(str(x) for x in mins), total),
                            "%d minutes = %s and %s."
                            % (total, _pl(total // 60, "hour"), _pl(total % 60, "minute"))])


_SHOP = [("pencil", 45), ("notebook", 185), ("ruler", 65), ("rubber", 35),
         ("pen", 95), ("folder", 275), ("glue stick", 120), ("calculator", 640),
         ("water bottle", 350), ("lunch box", 425)]


@skill("Y6.9.d", "Money problems", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 6, 1, 1, 1, 2, 1, 1, 1, 1])
    who = pick(NAMES)

    if t == 0:                                        # change from a note
        item, price = pick(_SHOP)
        n = random.randint(2, _by_d(d, 3, 5, 9))
        total = n * price
        note = pick([p for p in (500, 1000, 2000, 5000) if p > total] or [10000])
        return _num_q("%s buys %d %s%s at %s each and pays with a %s note. How much "
                      "change is given? Answer in pounds."
                      % (who, n, item, "" if n == 1 else "s", money(price), money(note)),
                      (note - total) / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%d × %s = %s." % (n, money(price), money(total)),
                                "%s − %s = %s." % (money(note), money(total),
                                                   money(note - total))])

    if t == 1:                                        # total of a shopping list (table)
        items = random.sample(_SHOP, _by_d(d, 3, 4, 5))
        qty = [random.randint(1, 4) for _ in items]
        rows = [[nm, money(pr), str(q), money(pr * q)]
                for (nm, pr), q in zip(items, qty)]
        total = sum(pr * q for (nm, pr), q in zip(items, qty))
        return {"prompt": "This is a shopping receipt. What is the total cost? "
                          "Answer in pounds.",
                "component": "data_table",
                "spec": {"caption": "Receipt", "headers": ["Item", "Price", "Number",
                                                           "Cost"],
                         "rows": rows},
                "answer": total / 100.0, "answer_type": "num", "tolerance": 0.005,
                "solution": ["Add the cost column: %s."
                             % " + ".join(money(pr * q)
                                          for (nm, pr), q in zip(items, qty)),
                             "The total is %s." % money(total)]}

    if t == 2:                                        # best value
        n1 = pick([3, 4, 5, 6])
        unit = pick([25, 30, 40, 45, 50])
        p1 = n1 * unit
        n2 = n1 * 2
        p2 = n2 * unit - pick([10, 20, 30, 40])
        cheaper = "B"
        return _num_q("A pack of %d pens costs %s. A pack of %d of the same pens costs "
                      "%s. How much cheaper is ONE pen in the larger pack, in pence?"
                      % (n1, money(p1), n2, money(p2)),
                      p1 // n1 - p2 // n2 if p2 % n2 == 0 and p1 % n1 == 0
                      else round(p1 / n1 - p2 / n2, 2),
                      "num", unit="p", tolerance=0.01,
                      solution=["Small pack: %s ÷ %d = %sp each."
                                % (money(p1), n1, _f(round(p1 / n1, 2))),
                                "Large pack: %s ÷ %d = %sp each."
                                % (money(p2), n2, _f(round(p2 / n2, 2))),
                                "The difference is %sp."
                                % _f(round(p1 / n1 - p2 / n2, 2))])

    if t == 3:                                        # percentage discount
        price = pick([1200, 1500, 2000, 2400, 3000, 3600, 4500, 5000])
        pct = pick([10, 20, 25, 50])
        off = price * pct // 100
        return _num_q("A coat costs %s. In a sale the price is reduced by %d%%. "
                      "What is the sale price? Answer in pounds."
                      % (money(price), pct),
                      (price - off) / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%d%% of %s is %s." % (pct, money(price), money(off)),
                                "%s − %s = %s." % (money(price), money(off),
                                                   money(price - off))])

    if t == 4:                                        # sharing a cost
        n = pick([3, 4, 5, 6, 8])
        each = random.randint(120, 950)
        total = n * each
        return _num_q("%d friends share the cost of a present that costs %s equally. "
                      "How much does each friend pay? Answer in pounds."
                      % (n, money(total)),
                      each / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%s ÷ %d = %s." % (money(total), n, money(each))])

    if t == 5:                                        # unit price / how many affordable
        item, price = pick(_SHOP)
        budget = pick([500, 1000, 1500, 2000, 3000])
        n = budget // price
        return _num_q("%s has %s to spend. One %s costs %s. What is the greatest number "
                      "of %ss %s can buy?" % (who, money(budget), item, money(price),
                                              item, who),
                      n, "int", unit=item + "s",
                      solution=["%s ÷ %s = %d with some money left over."
                                % (money(budget), money(price), n),
                                "%s can buy %d." % (who, n)])

    if t == 6:                                        # two items and change
        (i1, p1), (i2, p2) = random.sample(_SHOP, 2)
        a = random.randint(1, 3)
        b = random.randint(1, 3)
        total = a * p1 + b * p2
        paid = pick([p for p in (1000, 2000, 5000) if p > total] or [10000])
        return _num_q("%s buys %d %s%s at %s each and %d %s%s at %s each, paying with "
                      "%s. How much change is given, in pence?"
                      % (who, a, i1, "" if a == 1 else "s", money(p1),
                         b, i2, "" if b == 1 else "s", money(p2), money(paid)),
                      paid - total, "int", unit="p",
                      solution=["%d × %s = %s and %d × %s = %s."
                                % (a, money(p1), money(a * p1), b, money(p2),
                                   money(b * p2)),
                                "Total %s, so change is %s − %s = %s."
                                % (money(total), money(paid), money(total),
                                   money(paid - total))])

    if t == 7:                                        # profit
        cost = random.randint(50, 400)
        sell = cost + random.randint(20, 200)
        n = random.randint(5, _by_d(d, 12, 25, 60))
        return _num_q("A stall buys badges for %s each and sells them for %s each. "
                      "%d badges are sold. What is the total profit? Answer in pounds."
                      % (money(cost), money(sell), n),
                      n * (sell - cost) / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["Profit on one badge: %s − %s = %s."
                                % (money(sell), money(cost), money(sell - cost)),
                                "%d × %s = %s." % (n, money(sell - cost),
                                                   money(n * (sell - cost)))])

    if t == 8:                                        # currency-free multi-step
        weekly = pick([250, 300, 350, 400, 500])
        weeks = random.randint(4, 12)
        spend = random.randint(200, weekly * weeks // 2)
        left = weekly * weeks - spend
        return _num_q("%s saves %s each week for %d weeks, then spends %s. "
                      "How much money is left? Answer in pounds."
                      % (who, money(weekly), weeks, money(spend)),
                      left / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%d × %s = %s saved." % (weeks, money(weekly),
                                                         money(weekly * weeks)),
                                "%s − %s = %s." % (money(weekly * weeks), money(spend),
                                                   money(left))])

    # pounds and pence conversion
    p = random.randint(105, 9995)
    if random.random() < 0.5:
        return _num_q("Write %s in pence." % money(p), p, "int", unit="p",
                      solution=["£1 = 100p.",
                                "%s is %d pence." % (money(p), p)])
    return _num_q("Write %dp in pounds, as a decimal." % p, p / 100.0, "num", unit="£",
                  tolerance=0.005,
                  solution=["100p = £1.",
                            "%d ÷ 100 = %s." % (p, _f(p / 100.0))])


_CHART_TOPICS = [
    ("Favourite sport", ["Football", "Netball", "Tennis", "Cricket", "Hockey"],
     "children"),
    ("Books borrowed", ["Mon", "Tue", "Wed", "Thu", "Fri"], "books"),
    ("Way of travelling to school", ["Walk", "Bus", "Car", "Cycle", "Train"],
     "children"),
    ("Ice creams sold", ["Mon", "Tue", "Wed", "Thu", "Fri"], "ice creams"),
    ("Goals scored", ["Team A", "Team B", "Team C", "Team D", "Team E"], "goals"),
]


def _chart_data(d, n=4):
    title, pool, unit = pick(_CHART_TOPICS)
    cats = pool[:n]
    lo, hi = _by_d(d, (4, 20), (6, 40), (8, 90))
    vals = _distinct(n, lo, hi)
    return title, cats, vals, unit


@skill("Y6.9.e", "Interpret and construct tables and bar/line graphs", S9)
def _(d=1):
    d = _tier(d)
    n = _by_d(d, 4, 4, 5)
    title, cats, vals, unit = _chart_data(d, n)
    spec = {"categories": cats, "values": vals, "mode": "read"}
    i, j = random.sample(range(n), 2)
    t = _pick_t([2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 3, 3, 3, 3])
    grp1, grp2 = pick([("Year 5", "Year 6"), ("Boys", "Girls"), ("2024", "2025"),
                       ("Morning", "Afternoon")])
    v2 = [max(1, v + pick([-6, -4, -3, 3, 4, 6])) for v in vals]

    if t == 10:                                       # create bar graphs (categorical)
        scale = pick([2, 5, 10])
        sq = _distinct(n, 2, 10)                      # a bar is at most 10 squares tall
        rows = [[c, str(v * scale)] for c, v in zip(cats, sq)]
        return {"prompt": "%s. A bar graph is being created for this categorical data. On "
                          "the scale, one square stands for %d %s. How many squares tall "
                          "should the bar for %s be?" % (title, scale, unit, cats[i]),
                "component": "data_table",
                "spec": {"caption": title, "headers": ["Category", unit.capitalize()],
                         "rows": rows},
                "answer": sq[i], "answer_type": "int",
                "solution": ["%s has a value of %d." % (cats[i], sq[i] * scale),
                             "%d ÷ %d = %d squares." % (sq[i] * scale, scale, sq[i])]}

    if t == 11:                                       # interpret double bar graphs
        rows = [[c, str(a), str(b)] for c, a, b in zip(cats, vals, v2)]
        ask = pick(["diff", "total", "which"])
        spec_t = {"caption": "%s — %s and %s" % (title, grp1, grp2),
                  "headers": ["Category", grp1, grp2], "rows": rows}
        if ask == "diff":
            return {"prompt": "%s. A double bar graph is drawn from this table, with one "
                              "%s bar and one %s bar for each category. For %s, what is "
                              "the difference between the heights of the two bars?"
                              % (title, grp1, grp2, cats[i]),
                    "component": "data_table", "spec": spec_t,
                    "answer": abs(vals[i] - v2[i]), "answer_type": "int",
                    "solution": ["%s: %d and %s: %d."
                                 % (grp1, vals[i], grp2, v2[i]),
                                 "%d − %d = %d." % (max(vals[i], v2[i]),
                                                    min(vals[i], v2[i]),
                                                    abs(vals[i] - v2[i]))]}
        if ask == "total":
            return {"prompt": "%s. A double bar graph is drawn from this table, with one "
                              "%s bar and one %s bar for each category. What is the total "
                              "of all the %s bars?" % (title, grp1, grp2, grp2),
                    "component": "data_table", "spec": spec_t,
                    "answer": sum(v2), "answer_type": "int",
                    "solution": ["%s = %d." % (" + ".join(str(v) for v in v2), sum(v2))]}
        taller = grp1 if vals[i] > v2[i] else grp2
        return {"prompt": "%s. A double bar graph is drawn from this table, with one %s "
                          "bar and one %s bar for each category. For %s, which of the two "
                          "bars is taller? (type %s or %s)"
                          % (title, grp1, grp2, cats[i], grp1, grp2),
                "component": "data_table", "spec": spec_t,
                "answer": taller, "answer_type": "str",
                "solution": ["%s: %d and %s: %d." % (grp1, vals[i], grp2, v2[i]),
                             "The taller bar is %s." % taller]}

    if t == 12:                                       # create double bar graphs
        scale = pick([2, 5, 10])
        sq1 = _distinct(n, 2, 10)                     # a bar is at most 10 squares tall
        sq2 = [max(2, min(10, s + pick([-3, -2, 2, 3]))) for s in sq1]
        rows = [[c, str(a * scale), str(b * scale)] for c, a, b in zip(cats, sq1, sq2)]
        use2 = random.random() < 0.5
        grp = grp2 if use2 else grp1
        val = (sq2 if use2 else sq1)[i]
        return {"prompt": "%s. A double bar graph is being created from this table, with "
                          "one %s bar and one %s bar for each category. One square on the "
                          "scale stands for %d %s. How many squares tall should the %s "
                          "bar for %s be?"
                          % (title, grp1, grp2, scale, unit, grp, cats[i]),
                "component": "data_table",
                "spec": {"caption": "%s — %s and %s" % (title, grp1, grp2),
                         "headers": ["Category", grp1, grp2], "rows": rows},
                "answer": val, "answer_type": "int",
                "solution": ["The %s value for %s is %d." % (grp, cats[i], val * scale),
                             "%d ÷ %d = %d squares." % (val * scale, scale, val)]}

    if t == 13:                                       # frequency tables: multi-step
        rows = [[c, str(v)] for c, v in zip(cats, vals)]
        rest = [x for x in range(n) if x not in (i, j)]
        k = rest[0]
        m = rest[1] if len(rest) > 1 else k
        pair1 = vals[i] + vals[j]
        pair2 = vals[k] + (vals[m] if m != k else 0)
        return {"prompt": "%s. Interpret the frequency table to solve this multi-step "
                          "problem. Work out the total for %s and %s "
                          "together, and the total for %s. What is the difference between "
                          "the two totals?"
                          % (title, cats[i], cats[j],
                             "%s and %s together" % (cats[k], cats[m]) if m != k
                             else cats[k]),
                "component": "data_table",
                "spec": {"caption": title, "headers": ["Category", "Frequency"],
                         "rows": rows},
                "answer": abs(pair1 - pair2), "answer_type": "int",
                "solution": ["%s and %s: %d + %d = %d."
                             % (cats[i], cats[j], vals[i], vals[j], pair1),
                             "The other total is %d." % pair2,
                             "%d − %d = %d." % (max(pair1, pair2), min(pair1, pair2),
                                                abs(pair1 - pair2))]}

    if t == 0:                                        # read one bar
        return {"prompt": "%s. Use the bar chart. How many %s are shown for %s?"
                          % (title, unit, cats[i]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["The %s bar reaches %d." % (cats[i], vals[i])]}

    if t == 1:                                        # difference between two bars
        return {"prompt": "%s. Use the bar chart. What is the difference between %s and "
                          "%s?" % (title, cats[i], cats[j]),
                "component": "bar_chart", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (cats[i], vals[i], cats[j], vals[j]),
                             "%d − %d = %d." % (max(vals[i], vals[j]),
                                                min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 2:                                        # total
        return {"prompt": "%s. Use the bar chart. What is the total of all the bars?"
                          % title,
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(v) for v in vals), sum(vals))]}

    if t == 3:                                        # tallest / shortest (typed)
        want_top = random.random() < 0.5
        which = cats[vals.index(max(vals) if want_top else min(vals))]
        return {"prompt": "%s. Use the bar chart. Which bar is the %s? (type the label)"
                          % (title, "TALLEST" if want_top else "SHORTEST"),
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

    if t == 5:                                        # two-way table
        boys = [random.randint(3, 15) for _ in range(3)]
        girls = [random.randint(3, 15) for _ in range(3)]
        labels = cats[:3]
        rows = [[labels[k], str(boys[k]), str(girls[k]),
                 str(boys[k] + girls[k])] for k in range(3)]
        k = random.randrange(3)
        ask = pick(["row", "column"])
        if ask == "row":
            return {"prompt": "%s. Use the two-way table. How many children are in the "
                              "%s row altogether?" % (title, labels[k]),
                    "component": "data_table",
                    "spec": {"caption": title,
                             "headers": ["Category", "Boys", "Girls", "Total"],
                             "rows": rows},
                    "answer": boys[k] + girls[k], "answer_type": "int",
                    "solution": ["%d + %d = %d." % (boys[k], girls[k],
                                                    boys[k] + girls[k])]}
        return {"prompt": "%s. Use the two-way table. How many boys are there "
                          "altogether?" % title,
                "component": "data_table",
                "spec": {"caption": title,
                         "headers": ["Category", "Boys", "Girls", "Total"],
                         "rows": rows},
                "answer": sum(boys), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(b) for b in boys), sum(boys))]}

    if t == 6:                                        # construct: bar height
        scale = pick([2, 5, 10])
        v = vals[i]
        return _num_q("%s. A bar chart is drawn with each square on the axis worth %d "
                      "%s. %s has a value of %d. How many squares tall should the %s bar "
                      "be?" % (title, scale, unit, cats[i], v * scale, cats[i]),
                      v, "int", unit="squares",
                      solution=["Each square is worth %d." % scale,
                                "%d ÷ %d = %d squares." % (v * scale, scale, v)])

    if t == 7:                                        # more than average
        mean = sum(vals) // n
        cnt = sum(1 for v in vals if v > mean)
        return {"prompt": "%s. Use the bar chart. How many bars are TALLER than %d?"
                          % (title, mean),
                "component": "bar_chart", "spec": spec,
                "answer": cnt, "answer_type": "int",
                "solution": ["The values are %s." % ", ".join(str(v) for v in vals),
                             "%d of them are more than %d." % (cnt, mean)]}

    if t == 8:                                        # two-step from the chart
        others = [x for x in range(n) if x not in (i, j)]
        # the bar being taken away must not exceed the two added together,
        # or the result goes negative
        total_ij = vals[i] + vals[j]
        fits = [x for x in others if vals[x] <= total_ij]
        k = pick(fits) if fits else min(others, key=lambda x: vals[x])
        if vals[k] > total_ij:                 # still impossible -> add instead
            return {"prompt": "%s. Use the bar chart. Add %s, %s and %s together. "
                              "What is the total?" % (title, cats[i], cats[j], cats[k]),
                    "component": "bar_chart", "spec": spec,
                    "answer": total_ij + vals[k], "answer_type": "int",
                    "solution": ["%d + %d = %d." % (vals[i], vals[j], total_ij),
                                 "%d + %d = %d." % (total_ij, vals[k],
                                                    total_ij + vals[k])]}
        return {"prompt": "%s. Use the bar chart. Add %s and %s together, then take away "
                          "%s. What is the result?" % (title, cats[i], cats[j], cats[k]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] + vals[j] - vals[k], "answer_type": "int",
                "solution": ["Step 1: %d + %d = %d." % (vals[i], vals[j],
                                                        vals[i] + vals[j]),
                             "Step 2: %d − %d = %d." % (vals[i] + vals[j], vals[k],
                                                        vals[i] + vals[j] - vals[k])]}

    # table -> which category (typed)
    rows = [[c, str(v)] for c, v in zip(cats, vals)]
    target = pick(vals)
    which = cats[vals.index(target)]
    return {"prompt": "%s. Use the table. Which category has a frequency of %d? "
                      "(type the label)" % (title, target),
            "component": "data_table",
            "spec": {"caption": title, "headers": ["Category", "Frequency"],
                     "rows": rows},
            "answer": which, "answer_type": "str",
            "solution": ["Look down the frequency column for %d." % target,
                         "That row is %s." % which]}


# (phrase taking the total, sector labels, plural noun, singular noun)
_PIE_TOPICS = [
    ("the favourite sport of %d children", ["Football", "Netball", "Tennis", "Cricket"],
     "children", "child"),
    ("the favourite fruit of %d children", ["Apples", "Bananas", "Grapes", "Pears"],
     "children", "child"),
    ("how %d children travel to school", ["Walk", "Bus", "Car", "Cycle"],
     "children", "child"),
    ("the pets kept by %d children", ["Dog", "Cat", "Fish", "Rabbit"],
     "children", "child"),
    ("the favourite colour of %d people", ["Blue", "Red", "Green", "Yellow"],
     "people", "person"),
]


def _pie_data(d):
    """A whole-number data set whose parts each give a whole number of degrees."""
    total = pick([30, 36, 40, 45, 60, 72, 90, 120, 180] if d else [36, 60, 90, 120])
    n = 4
    unit = 360 // total
    while True:
        parts = [random.randint(1, total - 3) for _ in range(n - 1)]
        last = total - sum(parts)
        if last >= 1:
            parts.append(last)
            if len(set(parts)) == n:
                return total, parts, unit


@skill("Y6.9.f", "Pie charts", S9)
def _(d=1):
    d = _tier(d)
    topic, cats, who, one = pick(_PIE_TOPICS)
    total, parts, unit = _pie_data(d)
    shows = topic % total
    slices = [[c, p] for c, p in zip(cats, parts)]
    i = random.randrange(4)
    ang = parts[i] * unit
    t = _pick_t([3, 3, 2, 2, 1, 1, 1, 1, 1])

    if t == 0:                                        # angle of a sector (visual)
        return {"prompt": "This pie chart shows %s. The %s sector is outlined. "
                          "How many degrees is the angle of that sector?"
                          % (shows, cats[i]),
                "component": "pie_chart",
                "spec": {"slices": slices, "highlight": i},
                "answer": ang, "answer_type": "int",
                "solution": ["The whole pie is %d %s and 360 ÷ %d = %d° per %s."
                             % (total, who, total, unit, one),
                             "%d × %d = %d°." % (parts[i], unit, ang)]}

    if t == 1:                                        # count from an angle (visual)
        return {"prompt": "This pie chart shows %s. The outlined sector has an angle of "
                          "%d°. How many %s does that sector stand for?"
                          % (shows, ang, who),
                "component": "pie_chart",
                "spec": {"slices": slices, "highlight": i, "showAngles": True},
                "answer": parts[i], "answer_type": "int",
                "solution": ["360 ÷ %d = %d°, so each %s is %d°."
                             % (total, unit, one, unit),
                             "%d ÷ %d = %d %s." % (ang, unit, parts[i], who)]}

    if t == 2:                                        # largest / smallest sector
        want_big = random.random() < 0.5
        which = cats[parts.index(max(parts) if want_big else min(parts))]
        return {"prompt": "This pie chart shows %s. Which sector is the %s? "
                          "(type the label)"
                          % (shows, "LARGEST" if want_big else "SMALLEST"),
                "component": "pie_chart", "spec": {"slices": slices},
                "answer": which, "answer_type": "str",
                "solution": ["The %s sector is %s, with %d %s."
                             % ("largest" if want_big else "smallest", which,
                                max(parts) if want_big else min(parts), who)]}

    if t == 3:                                        # fraction of the pie (visual)
        fr = Fraction(parts[i], total)
        return {"prompt": "This pie chart shows %s. What fraction of the whole pie is "
                          "the outlined sector? Write it as a fraction." % shows,
                "component": "pie_chart",
                "spec": {"slices": slices, "highlight": i},
                "answer": "%d/%d" % (fr.numerator, fr.denominator),
                "answer_type": "frac",
                "solution": ["The sector stands for %d out of %d %s."
                             % (parts[i], total, who),
                             ("%d/%d simplifies to %d/%d."
                              % (parts[i], total, fr.numerator, fr.denominator))
                             if fr.denominator != total else
                             ("%d/%d is already in its simplest form."
                              % (parts[i], total))]}

    if t == 4:                                        # bare: angle from a share
        n_tot = pick([20, 24, 30, 36, 40, 45, 60, 72, 90])
        share = random.randint(1, n_tot - 1)
        while (360 * share) % n_tot:
            share = random.randint(1, n_tot - 1)
        return _num_q("%d of %d children chose football in a survey shown on a pie chart. "
                      "How many degrees is the angle of the football sector?"
                      % (share, n_tot),
                      360 * share // n_tot, "int", unit="degrees",
                      solution=["Each child is worth 360 ÷ %d = %s°."
                                % (n_tot, _f(360.0 / n_tot)),
                                "%d × %s = %d°." % (share, _f(360.0 / n_tot),
                                                    360 * share // n_tot)])

    if t == 5:                                        # inverse: total from a sector
        each = pick([2, 3, 4, 5, 6, 8, 9, 10, 12])
        n_tot = 360 // each
        share = random.randint(2, n_tot - 1)
        return _num_q("On a pie chart, a sector with an angle of %d° stands for %d "
                      "children. How many children are in the whole survey?"
                      % (share * each, share),
                      n_tot, "int", unit="children",
                      solution=["%d° ÷ %d children = %d° for each child."
                                % (share * each, share, each),
                                "360 ÷ %d = %d children altogether." % (each, n_tot)])

    if t == 6:                                        # percentage of the pie
        pct = pick([10, 20, 25, 40, 50, 75])
        return _num_q("A sector of a pie chart is %d%% of the whole chart. How many "
                      "degrees is its angle?" % pct,
                      360 * pct // 100, "int", unit="degrees",
                      solution=["The whole pie is 360° and 1%% is 3.6°.",
                                "%d × 3.6 = %d°." % (pct, 360 * pct // 100)])

    if t == 7:                                        # remaining sector
        used = random.sample([30, 45, 60, 75, 90, 100, 120], 3)
        while sum(used) >= 350:
            used = random.sample([30, 45, 60, 75, 90], 3)
        return _num_q("A pie chart has four sectors. Three of them have angles of %s. "
                      "How many degrees is the fourth sector?"
                      % ", ".join("%d°" % u for u in used),
                      360 - sum(used), "int", unit="degrees",
                      solution=["%s = %d°." % (" + ".join(str(u) for u in used),
                                               sum(used)),
                                "360 − %d = %d°." % (sum(used), 360 - sum(used))])

    # two sectors compared (visual)
    j = (i + 1 + random.randrange(3)) % 4
    return {"prompt": "This pie chart shows %s. How many more %s are in the %s sector "
                      "than in the %s sector?"
                      % (shows, who,
                         cats[i] if parts[i] > parts[j] else cats[j],
                         cats[j] if parts[i] > parts[j] else cats[i]),
            "component": "pie_chart", "spec": {"slices": slices},
            "answer": abs(parts[i] - parts[j]), "answer_type": "int",
            "solution": ["%s = %d and %s = %d." % (cats[i], parts[i], cats[j], parts[j]),
                         "%d − %d = %d." % (max(parts[i], parts[j]),
                                            min(parts[i], parts[j]),
                                            abs(parts[i] - parts[j]))]}


_LG6_TOPICS = [
    ("Temperature in the school garden", "°C", "Time",
     ["8 am", "10 am", "12 pm", "2 pm", "4 pm"],
     ["9 am", "11 am", "1 pm", "3 pm"], 4, 26),
    ("Height of a sunflower", "cm", "Week",
     ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
     ["the middle of week 1 and week 2", "the middle of week 2 and week 3",
      "the middle of week 3 and week 4", "the middle of week 4 and week 5"], 10, 90),
    ("Depth of water in a tank", "cm", "Hour",
     ["1 h", "2 h", "3 h", "4 h", "5 h"],
     ["1.5 h", "2.5 h", "3.5 h", "4.5 h"], 10, 80),
    ("Distance travelled by a cyclist", "km", "Time",
     ["0 min", "15 min", "30 min", "45 min", "60 min"],
     ["7.5 min", "22.5 min", "37.5 min", "52.5 min"], 0, 30),
]


@skill("Y6.9.g", "Interpret line graphs", S9)
def _(d=1):
    d = _tier(d)
    title, ylab, xlab, labels, mids, lo, hi = pick(_LG6_TOPICS)
    n = 5
    step = 2
    vals = sorted(random.sample(range(lo, hi + 1, step), n))
    if random.random() < 0.35:
        random.shuffle(vals)
    while len(set(vals)) != n:
        vals = random.sample(range(lo, hi + 1, step), n)
    pts = [[lab, v] for lab, v in zip(labels, vals)]
    spec = {"points": pts, "yLabel": ylab, "xLabel": xlab}
    i, j = random.sample(range(n), 2)
    t = _pick_t([2, 3, 2, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # read a plotted point
        return {"prompt": "%s. Use the graph. What is the reading at %s?"
                          % (title, labels[i]),
                "component": "line_graph", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["Find %s along the bottom and read across." % labels[i],
                             "The reading is %d %s." % (vals[i], ylab)]}

    if t == 1:                                        # read BETWEEN plotted points
        k = random.randrange(n - 1)
        mid = (vals[k] + vals[k + 1]) // 2
        return {"prompt": "%s. Use the graph. Estimate the reading exactly halfway "
                          "between %s and %s." % (title, labels[k], labels[k + 1]),
                "component": "line_graph", "spec": spec,
                "answer": mid, "answer_type": "num", "tolerance": 1,
                "solution": ["At %s the graph reads %d and at %s it reads %d."
                             % (labels[k], vals[k], labels[k + 1], vals[k + 1]),
                             "Halfway between them is (%d + %d) ÷ 2 = %d %s."
                             % (vals[k], vals[k + 1], mid, ylab)]}

    if t == 2:                                        # difference between two readings
        return {"prompt": "%s. Use the graph. What is the difference between the readings "
                          "at %s and %s?" % (title, labels[i], labels[j]),
                "component": "line_graph", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (labels[i], vals[i], labels[j], vals[j]),
                             "%d − %d = %d." % (max(vals[i], vals[j]),
                                                min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 3:                                        # highest reading
        return {"prompt": "%s. Use the graph. What is the HIGHEST reading shown?" % title,
                "component": "line_graph", "spec": spec,
                "answer": max(vals), "answer_type": "int",
                "solution": ["The highest point is at %s." % labels[vals.index(max(vals))],
                             "It reads %d %s." % (max(vals), ylab)]}

    if t == 4:                                        # where was it lowest (typed)
        return {"prompt": "%s. Use the graph. At which point along the bottom was the "
                          "reading LOWEST? (type the label)" % title,
                "component": "line_graph", "spec": spec,
                "answer": labels[vals.index(min(vals))], "answer_type": "str",
                "solution": ["The lowest reading is %d %s." % (min(vals), ylab),
                             "That happens at %s." % labels[vals.index(min(vals))]]}

    if t == 5:                                        # missing point
        k = random.randrange(n)
        sp = dict(spec)
        sp["missing"] = k
        return {"prompt": "%s. The point marked ? is at %s. Read the graph and write its "
                          "value." % (title, labels[k]),
                "component": "line_graph", "spec": sp,
                "answer": vals[k], "answer_type": "int",
                "solution": ["Read across from the ? to the y-axis.",
                             "The value is %d %s." % (vals[k], ylab)]}

    if t == 6:                                        # steepest rise (typed)
        rises = [vals[k + 1] - vals[k] for k in range(n - 1)]
        k = rises.index(max(rises))
        return {"prompt": "%s. Use the graph. Between which point and the NEXT point does "
                          "the graph rise the most? (type the label of the earlier point)"
                          % title,
                "component": "line_graph", "spec": spec,
                "answer": labels[k], "answer_type": "str",
                "solution": ["The changes are %s."
                             % ", ".join(str(r) for r in rises),
                             "The biggest rise starts at %s." % labels[k]]}

    if t == 7:                                        # range
        return {"prompt": "%s. Use the graph. Take the lowest reading away from the "
                          "highest reading. What is the answer?" % title,
                "component": "line_graph", "spec": spec,
                "answer": max(vals) - min(vals), "answer_type": "int",
                "solution": ["Highest = %d, lowest = %d." % (max(vals), min(vals)),
                             "%d − %d = %d." % (max(vals), min(vals),
                                                max(vals) - min(vals))]}

    if t == 8:                                        # rose or fell (typed)
        k = random.randrange(n - 1)
        while vals[k + 1] == vals[k]:
            k = random.randrange(n - 1)
        ans = "rose" if vals[k + 1] > vals[k] else "fell"
        return {"prompt": "%s. Use the graph. Between %s and %s, did the reading rise or "
                          "fall? (type rose or fell)" % (title, labels[k], labels[k + 1]),
                "component": "line_graph", "spec": spec,
                "answer": ans, "answer_type": "str",
                "solution": ["%s = %d and %s = %d."
                             % (labels[k], vals[k], labels[k + 1], vals[k + 1]),
                             "So the reading %s." % ans]}

    # conversion graph reasoning (no picture claimed)
    rate = pick([2, 4, 5, 8, 10])
    x = random.randint(2, 12)
    return _num_q("A conversion graph is a straight line through (0,0). It shows that "
                  "1 unit on the bottom axis is worth %d units on the side axis. "
                  "What value on the side axis matches %d on the bottom axis?"
                  % (rate, x),
                  rate * x, "int",
                  solution=["Each step of 1 across gives a rise of %d." % rate,
                            "%d × %d = %d." % (x, rate, rate * x)])


@skill("Y6.9.h", "Calculate and interpret the mean", S9)
def _(d=1):
    d = _tier(d)
    n = _by_d(d, 4, 5, 6)
    t = _pick_t([2, 4, 1, 1, 1, 1, 1, 3, 1, 1, 3, 3, 3])
    mean = random.randint(_by_d(d, 4, 8, 15), _by_d(d, 15, 30, 60))
    vals = [mean + random.randint(-3, 3) for _ in range(n - 1)]
    vals.append(n * mean - sum(vals))
    while min(vals) < 1:
        vals = [mean + random.randint(-3, 3) for _ in range(n - 1)]
        vals.append(n * mean - sum(vals))
    random.shuffle(vals)
    total = sum(vals)

    if t == 10:                                       # identify statistical questions
        q, ans = pick([
            ("How many minutes does each pupil in Year 6 spend reading each day?", "yes"),
            ("How tall is each child in Class 6?", "yes"),
            ("How many pets does each family in Year 6 own?", "yes"),
            ("How long does each pupil in Year 6 take to get to school?", "yes"),
            ("What are the shoe sizes of the children in Year 6?", "yes"),
            ("How many minutes are there in one hour?", "no"),
            ("How many days are there in September?", "no"),
            ("How many pupils are on the register in Class 6 today?", "no"),
            ("How many millimetres are there in one metre?", "no"),
            ("What is the mass of this particular book?", "no"),
        ])
        return _num_q("A statistical question is one that is answered by collecting data "
                      "that varies from person to person or from case to case. Identify "
                      "whether this is a statistical question: “%s” (type yes or no)" % q,
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["Ask whether the answer needs data that varies, or is a "
                                "single fixed fact.",
                                "The answer is %s." % ans])

    if t == 11:                                       # random or biased sample
        case, ans = pick([
            ("every pupil's name is put into a hat and 30 names are drawn out", "random"),
            ("a computer picks 40 pupils from the whole school register at random",
             "random"),
            ("25 names are drawn at random from a box holding every pupil's name",
             "random"),
            ("only the members of the football team are asked about favourite sports",
             "biased"),
            ("only the pupils leaving the school library are asked how much they enjoy "
             "reading", "biased"),
            ("only the pupils who own a bicycle are asked how they travel to school",
             "biased"),
            ("only the pupils in the school choir are asked about favourite subjects",
             "biased"),
        ])
        return _num_q("A school wants to survey its pupils. In this sample, %s. Identify "
                      "the sample: is it random or biased? (type one word)" % case,
                      ans, "str", text=True, placeholder="random / biased",
                      solution=["A random sample gives every pupil the same chance of "
                                "being chosen; a biased sample favours one group.",
                                "This sample is %s." % ans])

    if t == 12:                                       # representative sample
        case, ans = pick([
            ("50 pupils chosen at random from every year group in the school", "yes"),
            ("20 pupils chosen at random from the whole school register", "yes"),
            ("only the pupils in Year 1", "no"),
            ("only the pupils who play a musical instrument", "no"),
            ("only the members of the netball team", "no"),
            ("100 pupils chosen at random from the whole school register", "yes"),
        ])
        return _num_q("A survey asks about the favourite lunch of pupils in a school. The "
                      "sample is %s. Is this sample representative of all the pupils in "
                      "the school? (type yes or no)" % case,
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["A representative sample looks like the whole group it "
                                "stands for.",
                                "The answer is %s." % ans])

    if t == 0:                                        # mean of a list
        return _num_q("Work out the mean of these numbers: %s."
                      % ", ".join(str(v) for v in vals),
                      mean, "num", tolerance=0.005,
                      solution=["%s = %d." % (" + ".join(str(v) for v in vals), total),
                                "%d ÷ %d = %d." % (total, n, mean)])

    if t == 1:                                        # mean from a table
        cats = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][:n]
        rows = [[c, str(v)] for c, v in zip(cats, vals)]
        return {"prompt": "This table shows how many books were borrowed each day. "
                          "What is the mean number of books borrowed per day?",
                "component": "data_table",
                "spec": {"caption": "Books borrowed", "headers": ["Day", "Books"],
                         "rows": rows},
                "answer": mean, "answer_type": "num", "tolerance": 0.005,
                "solution": ["Total = %d." % total,
                             "%d ÷ %d = %d." % (total, n, mean)]}

    if t == 2:                                        # missing value from the mean
        k = random.randrange(n)
        others = vals[:k] + vals[k + 1:]
        return _num_q("The mean of %d numbers is %d. %d of the numbers are %s. "
                      "What is the missing number?"
                      % (n, mean, n - 1, ", ".join(str(v) for v in others)),
                      vals[k], "int",
                      solution=["The total must be %d × %d = %d." % (n, mean, total),
                                "%s = %d." % (" + ".join(str(v) for v in others),
                                              total - vals[k]),
                                "%d − %d = %d." % (total, total - vals[k], vals[k])])

    if t == 3:                                        # total from the mean
        return _num_q("The mean of %d numbers is %d. What do the %d numbers add up to?"
                      % (n, mean, n),
                      total, "int",
                      solution=["Total = mean × how many numbers.",
                                "%d × %d = %d." % (mean, n, total)])

    if t == 4:                                        # word problem: mean score
        who = pick(NAMES)
        return _num_q("%s scores %s in %d tests. What is the mean score?"
                      % (who, ", ".join(str(v) for v in vals), n),
                      mean, "num", tolerance=0.005,
                      solution=["%s = %d." % (" + ".join(str(v) for v in vals), total),
                                "%d ÷ %d = %d." % (total, n, mean)])

    if t == 5:                                        # mean with a decimal answer
        vs = [random.randint(2, _by_d(d, 12, 25, 60)) for _ in range(4)]
        tot = sum(vs)
        return _num_q("Work out the mean of %s. Give your answer as a decimal if needed."
                      % ", ".join(str(v) for v in vs),
                      tot / 4.0, "num", tolerance=0.005,
                      solution=["%s = %d." % (" + ".join(str(v) for v in vs), tot),
                                "%d ÷ 4 = %s." % (tot, _f(tot / 4.0))])

    if t == 6:                                        # new mean after one more value
        extra = mean + pick([-6, -4, 4, 6, 8])
        new_mean = (total + extra) / float(n + 1)
        ans_m, instr_m, tol_m = _dec_ask(new_mean)
        return _num_q("The mean of %d numbers is %d. A new number, %d, is added to the "
                      "set. What is the mean of all %d numbers? %s"
                      % (n, mean, extra, n + 1, instr_m),
                      ans_m, "num", tolerance=tol_m,
                      solution=["Old total = %d × %d = %d." % (n, mean, total),
                                "New total = %d + %d = %d." % (total, extra,
                                                               total + extra),
                                "%d ÷ %d = %s." % (total + extra, n + 1, _f(new_mean))])

    if t == 7:                                        # mean from a bar chart
        cats = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F"][:n]
        return {"prompt": "Use the bar chart. What is the mean of the %d values shown?"
                          % n,
                "component": "bar_chart",
                "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": mean, "answer_type": "num", "tolerance": 0.005,
                "solution": ["Total = %d." % total,
                             "%d ÷ %d = %d." % (total, n, mean)]}

    if t == 8:                                        # what score is needed
        target = mean + pick([1, 2, 3])
        need = target * (n + 1) - total
        return _num_q("The mean of %d test scores is %d. What score is needed in one more "
                      "test to make the mean of all %d tests exactly %d?"
                      % (n, mean, n + 1, target),
                      need, "int", unit="marks",
                      solution=["The new total must be %d × %d = %d."
                                % (n + 1, target, target * (n + 1)),
                                "%d − %d = %d." % (target * (n + 1), total, need)])

    # combined mean of two groups
    n1 = pick([4, 5, 6])
    n2 = pick([4, 5, 6])
    m1 = random.randint(5, 20)
    m2 = random.randint(5, 20)
    comb = (n1 * m1 + n2 * m2) / float(n1 + n2)
    ans_c, instr_c, tol_c = _dec_ask(120 + comb)
    return _num_q("A group of %d children has a mean height of %d cm. Another group of "
                  "%d children has a mean height of %d cm. What is the mean height of "
                  "all %d children? %s"
                  % (n1, 120 + m1, n2, 120 + m2, n1 + n2, instr_c),
                  ans_c, "num", unit="cm", tolerance=tol_c,
                  solution=["First group total: %d × %d = %d cm."
                            % (n1, 120 + m1, n1 * (120 + m1)),
                            "Second group total: %d × %d = %d cm."
                            % (n2, 120 + m2, n2 * (120 + m2)),
                            "(%d + %d) ÷ %d = %s cm."
                            % (n1 * (120 + m1), n2 * (120 + m2), n1 + n2,
                               _f(120 + comb))])


def _mode_data(d, n=7):
    """A data set with exactly one mode."""
    lo, hi = _by_d(d, (1, 12), (2, 20), (3, 40))
    while True:
        vals = [random.randint(lo, hi) for _ in range(n)]
        counts = {}
        for v in vals:
            counts[v] = counts.get(v, 0) + 1
        top = max(counts.values())
        if top >= 2 and list(counts.values()).count(top) == 1:
            for v, c in counts.items():
                if c == top:
                    return vals, v


@skill("Y6.9.i", "Mode, median and range", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 4, 4, 1, 1, 1, 1, 4, 3])
    n = _by_d(d, 5, 7, 9)

    if t in (10, 11):                                 # stem-and-leaf plots
        stems = sorted(random.sample(range(1, 8), 3))
        leaves = [sorted(random.sample(range(0, 10), random.randint(2, 4)))
                  for _ in stems]
        values = sorted([s * 10 + lf for s, lvs in zip(stems, leaves) for lf in lvs])
        rows = [[str(s), " ".join(str(lf) for lf in lvs)]
                for s, lvs in zip(stems, leaves)]
        cap = "Stem-and-leaf plot (%d | %d means %d)" % (stems[0], leaves[0][0],
                                                         values[0])
        if t == 10:                                   # interpret
            ask = pick(["count", "largest", "smallest", "range", "row"])
            k = random.randrange(3)
            if ask == "count":
                q, ans = "How many values are shown in the plot altogether?", len(values)
            elif ask == "largest":
                q, ans = "What is the largest value in the plot?", values[-1]
            elif ask == "smallest":
                q, ans = "What is the smallest value in the plot?", values[0]
            elif ask == "range":
                q, ans = ("What is the range of the values in the plot?",
                          values[-1] - values[0])
            else:
                q, ans = ("How many values are on the row with stem %d?" % stems[k],
                          len(leaves[k]))
            return {"prompt": "Interpret this stem-and-leaf plot. The stem is the tens "
                              "digit and each leaf is a units digit. %s" % q,
                    "component": "data_table",
                    "spec": {"caption": cap, "headers": ["Stem", "Leaves"],
                             "rows": rows},
                    "answer": ans, "answer_type": "int",
                    "solution": ["The values are %s."
                                 % ", ".join(str(v) for v in values),
                                 "The answer is %d." % ans]}
        k = random.randrange(3)                       # create
        shown = list(values)
        random.shuffle(shown)
        return _num_q("A stem-and-leaf plot is being created for these values: %s. The "
                      "stem is the tens digit and each leaf is a units digit. How many "
                      "leaves will be on the row with stem %d?"
                      % (", ".join(str(v) for v in shown), stems[k]),
                      len(leaves[k]), "int", unit="leaves",
                      solution=["The values in the %ds are %s."
                                % (stems[k] * 10,
                                   ", ".join(str(s * 10 + lf) for lf in leaves[k]
                                             for s in [stems[k]])),
                                "That row has %d leaves." % len(leaves[k])])

    if t == 0:                                        # mode
        vals, mode = _mode_data(d, n)
        return _num_q("What is the mode of this set of numbers: %s?"
                      % ", ".join(str(v) for v in vals),
                      mode, "int",
                      solution=["The mode is the value that appears most often.",
                                "%d appears more times than any other value." % mode])

    if t == 1:                                        # median (odd count)
        vals = random.sample(range(1, _by_d(d, 20, 40, 90)), n)
        med = sorted(vals)[n // 2]
        return _num_q("What is the median of this set of numbers: %s?"
                      % ", ".join(str(v) for v in vals),
                      med, "int",
                      solution=["In order: %s." % ", ".join(str(v) for v in sorted(vals)),
                                "The middle value of %d numbers is the %s: %d."
                                % (n, "%dth" % (n // 2 + 1), med)])

    if t == 2:                                        # range
        vals = random.sample(range(1, _by_d(d, 25, 50, 100)), n)
        return _num_q("What is the range of this set of numbers: %s?"
                      % ", ".join(str(v) for v in vals),
                      max(vals) - min(vals), "int",
                      solution=["Range = largest − smallest.",
                                "%d − %d = %d." % (max(vals), min(vals),
                                                   max(vals) - min(vals))])

    if t == 3:                                        # median (even count)
        m = _by_d(d, 4, 6, 8)
        vals = random.sample(range(1, 60), m)
        s = sorted(vals)
        med = (s[m // 2 - 1] + s[m // 2]) / 2.0
        return _num_q("What is the median of this set of numbers: %s? Give your answer as "
                      "a decimal if needed." % ", ".join(str(v) for v in vals),
                      med, "num", tolerance=0.005,
                      solution=["In order: %s." % ", ".join(str(v) for v in s),
                                "There are %d numbers, so take the mean of the middle "
                                "two: (%d + %d) ÷ 2 = %s."
                                % (m, s[m // 2 - 1], s[m // 2], _f(med))])

    if t == 4:                                        # from a data table
        vals, mode = _mode_data(d, 6)
        cats = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        rows = [[c, str(v)] for c, v in zip(cats, vals)]
        ask = pick(["mode", "range"])
        ans = mode if ask == "mode" else max(vals) - min(vals)
        return {"prompt": "This table shows the number of goals scored each day. "
                          "What is the %s of the six values?" % ask,
                "component": "data_table",
                "spec": {"caption": "Goals scored", "headers": ["Day", "Goals"],
                         "rows": rows},
                "answer": ans, "answer_type": "int",
                "solution": ["The values are %s." % ", ".join(str(v) for v in vals),
                             "The %s is %d." % (ask, ans)]}

    if t == 5:                                        # from a bar chart
        cats = ["Red", "Blue", "Green", "Yellow", "Purple"]
        vals = _distinct(5, 3, _by_d(d, 20, 40, 80))
        ask = pick(["range", "median"])
        ans = (max(vals) - min(vals)) if ask == "range" else sorted(vals)[2]
        return {"prompt": "Use the bar chart. What is the %s of the five values?" % ask,
                "component": "bar_chart",
                "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": ans, "answer_type": "int",
                "solution": ["In order: %s." % ", ".join(str(v) for v in sorted(vals)),
                             "The %s is %d." % (ask, ans)]}

    if t == 6:                                        # missing value for a given range
        vals = random.sample(range(5, 40), n - 1)
        want = max(vals) - min(vals) + random.randint(2, 10)
        missing = min(vals) + want if random.random() < 0.5 else max(vals) - want
        if missing < 0:
            missing = min(vals) + want
        rng = max(vals + [missing]) - min(vals + [missing])
        return _num_q("A set of numbers is %s and one more number. The range of the whole "
                      "set is %d. What is the missing number, if it is the %s value in "
                      "the set?"
                      % (", ".join(str(v) for v in vals), rng,
                         "largest" if missing > max(vals) else "smallest"),
                      missing, "int",
                      solution=["The other numbers run from %d to %d."
                                % (min(vals), max(vals)),
                                "A range of %d means the missing value is %d."
                                % (rng, missing)])

    if t == 7:                                        # mean vs median vs mode vocabulary
        desc, ans = pick([("the value that appears most often", "mode"),
                          ("the middle value when the data is put in order", "median"),
                          ("the largest value take away the smallest value", "range"),
                          ("the total divided by how many values there are", "mean")])
        return _num_q("In statistics, which average or measure is %s? (type one word)"
                      % desc,
                      ans, "str", text=True, placeholder="mean / median / mode / range",
                      solution=["%s is the %s." % (desc.capitalize(), ans)])

    if t == 8:                                        # all three from one small set
        vals, mode = _mode_data(d, 5)
        ask = pick(["mode", "median", "range"])
        s = sorted(vals)
        ans = {"mode": mode, "median": s[2], "range": s[-1] - s[0]}[ask]
        return _num_q("For the numbers %s, what is the %s?"
                      % (", ".join(str(v) for v in vals), ask),
                      ans, "int",
                      solution=["In order: %s." % ", ".join(str(v) for v in s),
                                "The %s is %d." % (ask, ans)])

    # compare the range of two sets
    a = random.sample(range(1, 50), 5)
    b = random.sample(range(1, 50), 5)
    ra, rb = max(a) - min(a), max(b) - min(b)
    while ra == rb:
        b = random.sample(range(1, 50), 5)
        rb = max(b) - min(b)
    return _num_q("Set A is %s and Set B is %s. How much larger is the bigger range?"
                  % (", ".join(str(v) for v in a), ", ".join(str(v) for v in b)),
                  abs(ra - rb), "int",
                  solution=["Range of A: %d − %d = %d." % (max(a), min(a), ra),
                            "Range of B: %d − %d = %d." % (max(b), min(b), rb),
                            "%d − %d = %d." % (max(ra, rb), min(ra, rb), abs(ra - rb))])


@skill("Y6.9.j", "Simple probability as a fraction", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 3, 3])
    colours = ["red", "blue", "green", "yellow"]

    def _frac(a, b):
        f = Fraction(a, b)
        return "%d/%d" % (f.numerator, f.denominator)

    if t in (12, 13):                                 # collected data: probability/prediction
        T = pick([20, 25, 40, 50])
        c1 = random.randint(2, T - 6)
        c2 = random.randint(2, T - c1 - 3)
        c3 = T - c1 - c2
        cs = random.sample(["Red", "Blue", "Green", "Yellow"], 3)
        counts = [c1, c2, c3]
        k = random.randrange(3)
        rows = [[c, str(v)] for c, v in zip(cs, counts)]
        if t == 12:
            return {"prompt": "A counter was taken from a bag and put back %d times. The "
                              "table shows the collected data. Use the collected data to "
                              "find the probability that the next counter taken is %s. "
                              "Write your answer as a fraction." % (T, cs[k].lower()),
                    "component": "data_table",
                    "spec": {"caption": "Results of %d draws" % T,
                             "headers": ["Colour", "Times drawn"], "rows": rows},
                    "answer": _frac(counts[k], T), "answer_type": "frac",
                    "solution": ["%s was drawn %d times out of %d."
                                 % (cs[k], counts[k], T),
                                 "The probability is %s." % _frac(counts[k], T)]}
        mult = pick([2, 3, 4, 5])
        return {"prompt": "A counter was taken from a bag and put back %d times. The "
                          "table shows the collected data. Use the data to make a "
                          "prediction: if the same experiment is repeated %d times, about "
                          "how many times would you predict a %s counter?"
                          % (T, T * mult, cs[k].lower()),
                "component": "data_table",
                "spec": {"caption": "Results of %d draws" % T,
                         "headers": ["Colour", "Times drawn"], "rows": rows},
                "answer": counts[k] * mult, "answer_type": "int", "tolerance": 0,
                "solution": ["%s came up %d times in %d draws."
                             % (cs[k], counts[k], T),
                             "%d draws is %d times as many, so predict %d × %d = %d."
                             % (T * mult, mult, counts[k], mult, counts[k] * mult)]}

    if t == 10:                                       # pie chart of a bag of counters
        cs = random.sample(["Red", "Blue", "Green", "Yellow"], 3)
        ns = [random.randint(2, _by_d(d, 6, 9, 14)) for _ in range(3)]
        tot = sum(ns)
        k = random.randrange(3)
        return {"prompt": "The pie chart shows the %d counters in a bag. One counter is "
                          "picked at random. What is the probability that it is %s? "
                          "Write your answer as a fraction." % (tot, cs[k].lower()),
                "component": "pie_chart",
                "spec": {"slices": [[c, n] for c, n in zip(cs, ns)], "highlight": k},
                "answer": _frac(ns[k], tot), "answer_type": "frac",
                "solution": ["There are %d counters altogether and %d are %s."
                             % (tot, ns[k], cs[k].lower()),
                             "The probability is %s." % _frac(ns[k], tot)]}

    if t == 11:                                       # bar chart of a bag of counters
        cs = random.sample(["Red", "Blue", "Green", "Yellow"], 4)
        ns = _distinct(4, 2, _by_d(d, 8, 12, 20))
        tot = sum(ns)
        k = random.randrange(4)
        return {"prompt": "The bar chart shows the counters in a bag. One counter is "
                          "picked at random. What is the probability that it is %s? "
                          "Write your answer as a fraction." % cs[k].lower(),
                "component": "bar_chart",
                "spec": {"categories": cs, "values": ns, "mode": "read"},
                "answer": _frac(ns[k], tot), "answer_type": "frac",
                "solution": ["Total counters: %s = %d."
                             % (" + ".join(str(n) for n in ns), tot),
                             "%d of them are %s, so the probability is %s."
                             % (ns[k], cs[k].lower(), _frac(ns[k], tot))]}

    if t == 0:                                        # bag of counters
        n1 = random.randint(2, _by_d(d, 5, 9, 15))
        n2 = random.randint(2, _by_d(d, 5, 9, 15))
        c1, c2 = random.sample(colours, 2)
        tot = n1 + n2
        return _num_q("A bag holds %d %s counters and %d %s counters. One counter is "
                      "taken out without looking. What is the probability that it is "
                      "%s? Write your answer as a fraction."
                      % (n1, c1, n2, c2, c1),
                      _frac(n1, tot), "frac",
                      solution=["There are %d counters altogether." % tot,
                                "%d of them are %s, so the probability is %s."
                                % (n1, c1, _frac(n1, tot))])

    if t == 1:                                        # three colours
        ns = [random.randint(1, _by_d(d, 5, 8, 12)) for _ in range(3)]
        cs = random.sample(colours, 3)
        tot = sum(ns)
        k = random.randrange(3)
        return _num_q("A bag holds %s counters. One counter is picked at random. What is "
                      "the probability that it is %s? Write your answer as a fraction."
                      % (", ".join("%d %s" % (n, c) for n, c in zip(ns, cs)), cs[k]),
                      _frac(ns[k], tot), "frac",
                      solution=["Total counters: %s = %d."
                                % (" + ".join(str(n) for n in ns), tot),
                                "The probability is %s." % _frac(ns[k], tot)])

    if t == 2:                                        # NOT the event
        n1 = random.randint(2, 12)
        n2 = random.randint(2, 12)
        c1, c2 = random.sample(colours, 2)
        tot = n1 + n2
        return _num_q("A bag holds %d %s counters and %d %s counters. One counter is "
                      "picked at random. What is the probability that it is NOT %s? "
                      "Write your answer as a fraction." % (n1, c1, n2, c2, c1),
                      _frac(n2, tot), "frac",
                      solution=["%d of the %d counters are not %s." % (n2, tot, c1),
                                "The probability is %s." % _frac(n2, tot)])

    if t == 3:                                        # dice
        tgt, desc = pick([([1], "a 1"), ([6], "a 6"), ([2, 4, 6], "an even number"),
                          ([1, 3, 5], "an odd number"),
                          ([4, 5, 6], "a number greater than 3"),
                          ([1, 2, 3], "a number less than 4"),
                          ([2, 3, 5], "a prime number")])
        return _num_q("A fair six-sided dice numbered 1 to 6 is rolled once. What is the "
                      "probability of rolling %s? Write your answer as a fraction." % desc,
                      _frac(len(tgt), 6), "frac",
                      solution=["The successful outcomes are %s."
                                % ", ".join(str(v) for v in tgt),
                                "%d out of 6 is %s." % (len(tgt), _frac(len(tgt), 6))])

    if t == 4:                                        # spinner
        n = pick([4, 5, 6, 8, 10])
        k = random.randint(1, n - 1)
        return _num_q("A fair spinner has %d equal sections. %d of the sections are "
                      "shaded. What is the probability that the spinner lands on a shaded "
                      "section? Write your answer as a fraction." % (n, k),
                      _frac(k, n), "frac",
                      solution=["%d successful sections out of %d equal sections."
                                % (k, n),
                                "The probability is %s." % _frac(k, n)])

    if t == 5:                                        # numbered cards
        n = pick([10, 12, 15, 20])
        multiple = pick([2, 3, 5])
        cnt = n // multiple
        return _num_q("Cards numbered 1 to %d are shuffled and one is picked at random. "
                      "What is the probability that the number on the card is a multiple "
                      "of %d? Write your answer as a fraction." % (n, multiple),
                      _frac(cnt, n), "frac",
                      solution=["The multiples of %d up to %d are %s: that is %d cards."
                                % (multiple, n,
                                   ", ".join(str(multiple * (x + 1))
                                             for x in range(cnt)), cnt),
                                "The probability is %s." % _frac(cnt, n)])

    if t == 6:                                        # how many counters (inverse)
        tot = pick([12, 15, 18, 20, 24, 30])
        f = pick([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 3),
                  Fraction(3, 5), Fraction(1, 6)])
        while (tot * f.numerator) % f.denominator:
            tot = pick([12, 24, 30, 60])
        k = tot * f.numerator // f.denominator
        c1 = pick(colours)
        return _num_q("A bag holds %d counters. The probability of picking a %s counter "
                      "is %d/%d. How many %s counters are in the bag?"
                      % (tot, c1, f.numerator, f.denominator, c1),
                      k, "int", unit="counters",
                      solution=["%d/%d of %d = %d." % (f.numerator, f.denominator,
                                                       tot, k)])

    if t == 7:                                        # certain / impossible / even chance
        case, ans = pick([
            ("picking a red counter from a bag that holds only red counters", "certain"),
            ("picking a blue counter from a bag that holds only red counters",
             "impossible"),
            ("a fair coin landing on heads", "even chance"),
            ("rolling a 7 on a fair six-sided dice numbered 1 to 6", "impossible"),
            ("rolling a number less than 7 on a fair six-sided dice numbered 1 to 6",
             "certain"),
            ("rolling an even number on a fair six-sided dice numbered 1 to 6",
             "even chance"),
        ])
        return _num_q("How likely is %s? (type certain, impossible or even chance)" % case,
                      ans, "str", text=True,
                      placeholder="certain / impossible / even chance",
                      solution=["Think about how many of the outcomes are successful.",
                                "It is %s." % ans])

    if t == 8:                                        # probability as a percentage
        n = pick([10, 20, 25, 50])
        k = random.randint(1, n - 1)
        while (100 * k) % n:
            k = random.randint(1, n - 1)
        return _num_q("A bag holds %d counters and %d of them are green. One counter is "
                      "picked at random. What is the probability of picking green, as a "
                      "percentage?" % (n, k),
                      100 * k // n, "int", unit="%",
                      solution=["%d out of %d is %d/%d." % (k, n, k, n),
                                "As a percentage that is %d%%." % (100 * k // n)])

    # expected number of successes
    n = pick([2, 3, 4, 5, 6])
    trials = pick([12, 18, 24, 30, 60])
    return _num_q("A fair spinner has %d equal sections, numbered 1 to %d. The spinner is "
                  "spun %d times. About how many times would you expect it to land on "
                  "section 1?" % (n, n, trials),
                  trials // n, "int", unit="times",
                  solution=["The probability of section 1 is 1/%d." % n,
                            "%d ÷ %d = %d times." % (trials, n, trials // n)])


_SPEND = ["Food", "Travel", "Clubs", "Books", "Games", "Savings", "Presents"]


@skill("Y6.9.k", "Financial literacy: records and budgets", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3])
    who = pick(NAMES)

    if t == 10:                                       # advantages and disadvantages
        kind, feature, ans = pick([
            ("an advantage", "no bank account is needed to pay this way", "cash"),
            ("a disadvantage", "if it is lost or stolen it usually cannot be replaced",
             "cash"),
            ("an advantage",
             "the money comes straight out of the bank account, so no debt is built up",
             "debit card"),
            ("a disadvantage",
             "the payment is refused if there is not enough money in the bank account",
             "debit card"),
            ("an advantage",
             "it allows something to be bought now and paid back to the bank later",
             "credit card"),
            ("a disadvantage",
             "interest has to be paid if the bill is not paid off in full",
             "credit card"),
            ("an advantage",
             "money put aside in this account earns interest while it waits to be spent",
             "savings account"),
            ("a disadvantage",
             "the money has to be built up first, so the purchase must wait",
             "savings account"),
        ])
        return _num_q("Identify the payment method. Which payment method has %s: “%s”? "
                      "(type cash, debit card, credit card or savings account)"
                      % (kind, feature),
                      ans, "str", text=True,
                      placeholder="cash / debit card / credit card / savings account",
                      solution=["Compare how each payment method takes the money.",
                                "That is %s of using %s." % (kind, ans)])

    if t == 11:                                       # evaluate payment methods
        price = pick([4500, 6000, 8500, 12000, 20000])
        enough = random.random() < 0.5
        bal = price + pick([500, 1500, 3000]) if enough else price - pick([500, 1500,
                                                                          3000])
        if bal < 0:
            bal = price + 500
            enough = True
        ans = "debit card" if bal >= price else "credit card"
        return _num_q("%s wants to buy a coat costing %s today and has %s in the bank "
                      "account. Evaluate the payment methods: %s does not want to borrow "
                      "money unless there is no other way to pay today. Which payment "
                      "method should %s use — a debit card or a credit card? "
                      "(type the answer)"
                      % (who, money(price), money(bal), who, who),
                      ans, "str", text=True, placeholder="debit card / credit card",
                      solution=["The coat costs %s and the account holds %s."
                                % (money(price), money(bal)),
                                "There is %s money in the account, so a %s is the right "
                                "choice." % ("enough" if bal >= price else "not enough",
                                             ans)])

    if t == 0:                                        # budget table: total spending
        cats = random.sample(_SPEND, _by_d(d, 3, 4, 5))
        amounts = [random.randint(150, 1800) for _ in cats]
        rows = [[c, money(a)] for c, a in zip(cats, amounts)]
        return {"prompt": "This is a monthly spending record. What is the total spent? "
                          "Answer in pounds.",
                "component": "data_table",
                "spec": {"caption": "Monthly spending", "headers": ["Item", "Amount"],
                         "rows": rows},
                "answer": sum(amounts) / 100.0, "answer_type": "num",
                "tolerance": 0.005,
                "solution": ["Add the amounts: %s."
                             % " + ".join(money(a) for a in amounts),
                             "The total is %s." % money(sum(amounts))]}

    if t == 1:                                        # budget table: money left
        cats = random.sample(_SPEND, _by_d(d, 3, 4, 5))
        amounts = [random.randint(150, 1200) for _ in cats]
        spent = sum(amounts)
        income = ((spent + random.randint(200, 2500)) // 100 + 1) * 100
        rows = [[c, money(a)] for c, a in zip(cats, amounts)]
        return {"prompt": "%s has an income of %s this month. This table shows what %s "
                          "spent. How much money is left at the end of the month? "
                          "Answer in pounds." % (who, money(income), who),
                "component": "data_table",
                "spec": {"caption": "%s — spending" % who,
                         "headers": ["Item", "Amount"], "rows": rows},
                "answer": (income - spent) / 100.0, "answer_type": "num",
                "tolerance": 0.005,
                "solution": ["Total spent: %s." % money(spent),
                             "%s − %s = %s." % (money(income), money(spent),
                                                money(income - spent))]}

    if t == 2:                                        # savings over months
        each = pick([500, 750, 1000, 1250, 1500, 2000])
        months = random.randint(3, _by_d(d, 6, 12, 24))
        return _num_q("%s saves %s every month for %d months. How much is saved "
                      "altogether? Answer in pounds." % (who, money(each), months),
                      each * months / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%s × %d = %s." % (money(each), months,
                                                   money(each * months))])

    if t == 3:                                        # how long to save for a target
        each = pick([500, 800, 1000, 1500, 2000, 2500])
        months = random.randint(3, 15)
        target = each * months
        return _num_q("%s wants to buy a bike costing %s and saves %s each month. "
                      "How many months will it take to save enough?"
                      % (who, money(target), money(each)),
                      months, "int", unit="months",
                      solution=["%s ÷ %s = %d." % (money(target), money(each), months),
                                "It takes %d months." % months])

    if t == 4:                                        # percentage of income saved
        income = pick([80000, 100000, 120000, 150000, 200000])
        pct = pick([5, 10, 15, 20, 25])
        saved = income * pct // 100
        return _num_q("A monthly income is %s. %d%% of it is put into savings. "
                      "How much is saved each month? Answer in pounds."
                      % (money(income), pct),
                      saved / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%d%% of %s is %s." % (pct, money(income), money(saved)),
                                "That is %s saved each month." % money(saved)])

    if t == 5:                                        # running balance
        start = pick([2000, 3000, 5000, 10000])
        ins = [random.randint(200, 1500) for _ in range(2)]
        outs = [random.randint(200, 1200) for _ in range(2)]
        bal = start + sum(ins) - sum(outs)
        rows = ([["Starting balance", money(start), ""]] +
                [["Money in", money(v), ""] for v in ins] +
                [["Money out", "", money(v)] for v in outs])
        return {"prompt": "This is a record of money in and money out. What is the "
                          "balance at the end? Answer in pounds.",
                "component": "data_table",
                "spec": {"caption": "Account record",
                         "headers": ["Entry", "In", "Out"], "rows": rows},
                "answer": bal / 100.0, "answer_type": "num", "tolerance": 0.005,
                "solution": ["Money in: %s + %s = %s."
                             % (money(ins[0]), money(ins[1]), money(sum(ins))),
                             "Money out: %s + %s = %s."
                             % (money(outs[0]), money(outs[1]), money(sum(outs))),
                             "%s + %s − %s = %s." % (money(start), money(sum(ins)),
                                                     money(sum(outs)), money(bal))]}

    if t == 6:                                        # weekly budget per day
        weekly = pick([700, 1400, 2100, 2800, 3500])
        return _num_q("%s has a budget of %s for a whole week and plans to spend the same "
                      "amount each day. How much can %s spend each day? Answer in pounds."
                      % (who, money(weekly), who),
                      weekly / 700.0, "num", unit="£", tolerance=0.005,
                      solution=["%s ÷ 7 = %s." % (money(weekly), money(weekly // 7))])

    if t == 7:                                        # over or under budget
        budget = pick([5000, 7500, 10000, 15000])
        spent = budget + pick([-2500, -1200, -300, 450, 1600, 3000])
        over = spent > budget
        return _num_q("A budget for a school trip is %s. The trip actually costs %s. "
                      "By how much is the trip over or under budget? Answer in pounds."
                      % (money(budget), money(spent)),
                      abs(spent - budget) / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%s and %s differ by %s."
                                % (money(budget), money(spent),
                                   money(abs(spent - budget))),
                                "The trip is %s budget by %s."
                                % ("over" if over else "under",
                                   money(abs(spent - budget)))])

    if t == 8:                                        # simple interest style
        saved = pick([10000, 20000, 25000, 50000])
        pct = pick([2, 4, 5, 10])
        interest = saved * pct // 100
        return _num_q("%s puts %s into a savings account that adds %d%% at the end of the "
                      "year. How much is in the account after one year? Answer in pounds."
                      % (who, money(saved), pct),
                      (saved + interest) / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["%d%% of %s is %s." % (pct, money(saved),
                                                       money(interest)),
                                "%s + %s = %s." % (money(saved), money(interest),
                                                   money(saved + interest))])

    # income minus a list of bills, per week
    weeks = pick([4, 5])
    weekly_in = pick([4000, 5000, 6000])
    bills = [random.randint(500, 2500) for _ in range(3)]
    left = weekly_in * weeks - sum(bills)
    while left < 0:
        bills = [random.randint(300, 1200) for _ in range(3)]
        left = weekly_in * weeks - sum(bills)
    return _num_q("%s earns %s a week for %d weeks. Bills of %s must be paid out of that "
                  "money. How much is left? Answer in pounds."
                  % (who, money(weekly_in), weeks,
                     ", ".join(money(b) for b in bills)),
                  left / 100.0, "num", unit="£", tolerance=0.005,
                  solution=["Earnings: %s × %d = %s." % (money(weekly_in), weeks,
                                                         money(weekly_in * weeks)),
                            "Bills: %s = %s." % (" + ".join(money(b) for b in bills),
                                                 money(sum(bills))),
                            "%s − %s = %s." % (money(weekly_in * weeks),
                                               money(sum(bills)), money(left))])


@skill("Y6.9.l", "Mixed multi-step reasoning", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3])
    who = pick(NAMES)

    if t == 11:                                       # number line: negative temperatures
        lo = pick([-20, -15, -10])
        hi = pick([10, 15, 20])
        step = 1 if hi - lo <= 30 else 2
        start = random.randint(lo + 2, -1)
        rise = random.randint(3, hi - start)
        return {"prompt": "The temperature is %d °C and then rises by %d °C. Mark the new "
                          "temperature on the number line." % (start, rise),
                "component": "number_line",
                "spec": {"min": lo, "max": hi, "step": step, "major": 5},
                "answer": start + rise, "answer_type": "num", "tolerance": step / 2.0,
                "solution": ["Count up %d from %d." % (rise, start),
                             "%d + %d = %d °C." % (start, rise, start + rise)]}

    if t == 12:                                       # data table: multi-step totals
        cats = random.sample(["Year 3", "Year 4", "Year 5", "Year 6"], 4)
        vals = _distinct(4, 20, _by_d(d, 60, 120, 200))
        rows = [[c, str(v)] for c, v in zip(cats, vals)]
        pct = pick([10, 25, 50])
        k = random.randrange(4)
        while (vals[k] * pct) % 100:
            vals[k] = vals[k] - vals[k] % (100 // pct if pct != 50 else 2)
            if vals[k] < 4:
                vals[k] = 100 // pct * 4
            rows = [[c, str(v)] for c, v in zip(cats, vals)]
        part = vals[k] * pct // 100
        return {"prompt": "This table shows how many pupils are in each year group. "
                          "%d%% of the pupils in %s go swimming. How many pupils in %s go "
                          "swimming?" % (pct, cats[k], cats[k]),
                "component": "data_table",
                "spec": {"caption": "Pupils by year group",
                         "headers": ["Year group", "Pupils"], "rows": rows},
                "answer": part, "answer_type": "int",
                "solution": ["%s has %d pupils." % (cats[k], vals[k]),
                             "%d%% of %d = %d pupils." % (pct, vals[k], part)]}

    if t == 13:                                       # bar chart: two-step reasoning
        cats = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        vals = _distinct(5, 5, _by_d(d, 25, 45, 80))
        i, j = random.sample(range(5), 2)
        return {"prompt": "The bar chart shows how many tickets were sold each day. "
                          "Tickets cost £%d each. How much money was taken on %s and %s "
                          "together, in pounds?" % (3, cats[i], cats[j]),
                "component": "bar_chart",
                "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": 3 * (vals[i] + vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d tickets."
                             % (cats[i], vals[i], cats[j], vals[j]),
                             "%d + %d = %d tickets." % (vals[i], vals[j],
                                                        vals[i] + vals[j]),
                             "%d × 3 = %d pounds." % (vals[i] + vals[j],
                                                      3 * (vals[i] + vals[j]))]}

    if t == 0:                                        # percentage then subtraction
        total = pick([200, 250, 300, 400, 500, 600])
        pct = pick([10, 20, 25, 40, 60, 75])
        part = total * pct // 100
        return _num_q("A school has %d pupils. %d%% of them walk to school. "
                      "How many pupils do NOT walk to school?" % (total, pct),
                      total - part, "int", unit="pupils",
                      solution=["%d%% of %d = %d pupils walk." % (pct, total, part),
                                "%d − %d = %d pupils." % (total, part, total - part)])

    if t == 1:                                        # ratio sharing
        parts = pick([[2, 3], [3, 5], [1, 4], [2, 7], [3, 4]])
        unit = random.randint(3, _by_d(d, 8, 15, 30))
        total = sum(parts) * unit
        want = random.randrange(2)
        return _num_q("%s and a friend share %d sweets in the ratio %d : %d. How many "
                      "sweets does the person with the %s share get?"
                      % (who, total, parts[0], parts[1],
                         "larger" if parts[want] == max(parts) else "smaller"),
                      parts[want] * unit, "int", unit="sweets",
                      solution=["The ratio has %d parts and %d ÷ %d = %d per part."
                                % (sum(parts), total, sum(parts), unit),
                                "%d × %d = %d sweets." % (parts[want], unit,
                                                          parts[want] * unit)])

    if t == 2:                                        # area then cost
        w = random.randint(4, 12)
        h = random.randint(4, 12)
        cost = pick([5, 6, 8, 12])
        return _num_q("A rectangular room measures %d m by %d m. Flooring costs £%d per "
                      "square metre and fitting costs a flat £%d. What is the total "
                      "cost, in pounds?" % (w, h, cost, 50),
                      w * h * cost + 50, "int", unit="pounds",
                      solution=["Area = %d × %d = %d m²." % (w, h, w * h),
                                "Flooring: %d × %d = %d pounds." % (w * h, cost,
                                                                    w * h * cost),
                                "%d + 50 = %d pounds." % (w * h * cost,
                                                          w * h * cost + 50)])

    if t == 3:                                        # BIDMAS
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        c = random.randint(2, 12)
        e = random.randint(2, 9)
        return _num_q("Work out %d + %d × %d − %d." % (a, b, c, e),
                      a + b * c - e, "int",
                      solution=["Multiplication comes before addition and subtraction.",
                                "%d × %d = %d." % (b, c, b * c),
                                "%d + %d − %d = %d." % (a, b * c, e, a + b * c - e)])

    if t == 4:                                        # fraction of an amount, two steps
        total = pick([120, 180, 240, 300, 360, 480])
        f1 = pick([Fraction(1, 3), Fraction(1, 4), Fraction(2, 5), Fraction(1, 6),
                   Fraction(3, 8)])
        while (total * f1.numerator) % f1.denominator:
            total = pick([120, 240, 360, 480])
        used = total * f1.numerator // f1.denominator
        left = total - used
        half = left // 2
        return _num_q("A tank holds %d litres of water. %d/%d of the water is used, then "
                      "half of what is left is used. How many litres are left in the tank?"
                      % (total, f1.numerator, f1.denominator),
                      left - half, "int", unit="litres",
                      solution=["%d/%d of %d = %d litres used."
                                % (f1.numerator, f1.denominator, total, used),
                                "%d − %d = %d litres left." % (total, used, left),
                                "Half of %d is %d, so %d litres remain."
                                % (left, half, left - half)])

    if t == 5:                                        # rate problem
        n = random.randint(3, 9)
        each = random.randint(4, 15)
        want = n * random.randint(2, 5)
        return _num_q("%d identical machines make %d toys in an hour. At the same rate, "
                      "how many toys would %d machines make in an hour?"
                      % (n, n * each, want),
                      want * each, "int", unit="toys",
                      solution=["One machine makes %d ÷ %d = %d toys."
                                % (n * each, n, each),
                                "%d × %d = %d toys." % (want, each, want * each)])

    if t == 6:                                        # perimeter + algebra flavour
        s = random.randint(3, 15)
        extra = random.randint(2, 10)
        p = 2 * (s + s + extra)
        return _num_q("A rectangle is %d cm longer than it is wide, and its perimeter is "
                      "%d cm. How wide is the rectangle, in cm?" % (extra, p),
                      s, "int", unit="cm",
                      solution=["Half the perimeter is %d ÷ 2 = %d cm." % (p, p // 2),
                                "%d − %d = %d, and %d ÷ 2 = %d cm."
                                % (p // 2, extra, p // 2 - extra, p // 2 - extra, s)])

    if t == 7:                                        # mean + missing value in context
        n = pick([4, 5, 6])
        mean = random.randint(8, 30)
        vals = [mean + random.randint(-4, 4) for _ in range(n - 1)]
        last = n * mean - sum(vals)
        while last < 1:
            vals = [mean + random.randint(-4, 4) for _ in range(n - 1)]
            last = n * mean - sum(vals)
        return _num_q("%s scores %s in %d spelling tests. The mean score over all %d "
                      "tests is %d. What was the score in the last test?"
                      % (who, ", ".join(str(v) for v in vals), n - 1, n, mean),
                      last, "int", unit="marks",
                      solution=["Total needed: %d × %d = %d." % (n, mean, n * mean),
                                "%s = %d." % (" + ".join(str(v) for v in vals),
                                              sum(vals)),
                                "%d − %d = %d." % (n * mean, sum(vals), last)])

    if t == 8:                                        # scale / proportion with money
        n1 = pick([3, 4, 5, 6])
        price = random.randint(60, 400)
        n2 = n1 * random.randint(2, 5)
        return _num_q("%d identical pens cost %s. At the same price each, how much do "
                      "%d pens cost? Answer in pounds."
                      % (n1, money(n1 * price), n2),
                      n2 * price / 100.0, "num", unit="£", tolerance=0.005,
                      solution=["One pen costs %s ÷ %d = %s."
                                % (money(n1 * price), n1, money(price)),
                                "%d × %s = %s." % (n2, money(price), money(n2 * price))])

    if t == 9:                                        # negative numbers in context
        start = random.randint(-12, -1)
        rise = random.randint(3, 25)
        return _num_q("At midnight the temperature is %d °C. By midday it has risen by "
                      "%d °C. What is the temperature at midday, in °C?" % (start, rise),
                      start + rise, "int", unit="°C",
                      solution=["Count up %d from %d." % (rise, start),
                                "%d + %d = %d °C." % (start, rise, start + rise)])

    # volume + capacity + time, three steps
    L, W, H = pick([10, 20, 25, 30]), pick([10, 20, 25]), pick([10, 20, 30, 40])
    litres = L * W * H / 1000.0
    rate = pick([2, 4, 5, 10])
    mins = litres / rate
    ans_t, instr_t, tol_t = _dec_ask(mins)
    return _num_q("A tank measures %d cm by %d cm by %d cm. 1000 cm³ of water is 1 litre. "
                  "Water flows in at %d litres per minute. How many minutes does it take "
                  "to fill the tank? %s"
                  % (L, W, H, rate, instr_t),
                  ans_t, "num", unit="minutes", tolerance=tol_t,
                  solution=["Volume = %d × %d × %d = %d cm³." % (L, W, H, L * W * H),
                            "That is %s %s." % (_f(litres), "litre" if litres == 1 else "litres"),
                            "%s ÷ %d = %s %s." % (_f(litres), rate, _f(mins), "minute" if mins == 1 else "minutes")])
