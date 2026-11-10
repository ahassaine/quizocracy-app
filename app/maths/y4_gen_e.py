# dev/app/logic/y4_gen_e.py — Year 4 generators: levels 4.8 (geometry) and 4.9
# (statistics & consolidation).
#
# Every generator takes a difficulty tier: d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between 8+ genuinely different framings (visual model, bare
# calculation, word problem, missing number, inverse, comparison, reasoning).
#
# Visual components used here:
#   geometry ...... shape / angle / coordinate_grid / area_grid
#   statistics .... data_table / pictogram / bar_chart / line_graph
import random
from .maths_engine import skill, pick, money, NAMES

S8 = "4.8 Geometry"
S9 = "4.9 Statistics & consolidation"


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


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


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


_GATE = "|\u0336" * 4            # a bundle of five: four bars crossed by the fifth


def _tally(n):
    """7 -> gate + ' ||' (a bundle of five is four bars crossed by a fifth)."""
    n = int(n)
    parts = [_GATE] * (n // 5)
    if n % 5:
        parts.append("|" * (n % 5))
    return " ".join(parts) if parts else "0"


def _distinct(count, lo, hi):
    """A list of `count` distinct integers in [lo, hi]."""
    hi = max(hi, lo + count)
    return random.sample(range(lo, hi + 1), count)


def _chart(d, n_cats=4, pool=None):
    cats = random.sample(pool or ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"],
                         n_cats)
    lo, hi = _by_d(d, (2, 9), (3, 15), (4, 24))
    return cats, _distinct(n_cats, lo, hi)


# --------------------------------------------------------------- geometry ----
# polygons the `shape` component can actually draw (all regular but the rectangle)
_DRAWN = [("triangle", 3), ("square", 4), ("rectangle", 4), ("pentagon", 5),
          ("hexagon", 6), ("heptagon", 7), ("octagon", 8)]
_DRAWN_NAMEABLE = [s for s in _DRAWN if s[0] not in ("square", "rectangle")]

# every polygon name Year 4 meets, drawn or not
_POLY = [("triangle", 3), ("quadrilateral", 4), ("pentagon", 5), ("hexagon", 6),
         ("heptagon", 7), ("octagon", 8), ("nonagon", 9), ("decagon", 10)]

# objects used when deciding which objects take up space and so have volume
_HAS_VOLUME = ["a cereal box", "a football", "a dice", "a house brick",
               "a tin of beans", "a wooden cube", "a marble"]
_NO_VOLUME = ["a square drawn on paper", "a photograph printed on a page",
              "a shadow on a wall", "a circle painted on the playground",
              "a triangle printed in a book"]

_SOLIDS = [("cube", 6, 12, 8), ("cuboid", 6, 12, 8),
           ("square-based pyramid", 5, 8, 5), ("triangular prism", 5, 9, 6)]

# name -> (lines of symmetry, label used in prose)
_SYM_DRAWN = {"square": (4, "square"), "rectangle": (2, "rectangle"),
              "triangle": (3, "equilateral triangle"),
              "pentagon": (5, "regular pentagon"), "hexagon": (6, "regular hexagon"),
              "heptagon": (7, "regular heptagon"), "octagon": (8, "regular octagon")}

_SYM_NAMED = [("square", 4), ("rectangle", 2), ("equilateral triangle", 3),
              ("isosceles triangle", 1), ("scalene triangle", 0), ("rhombus", 2),
              ("parallelogram", 0), ("kite", 1), ("regular pentagon", 5),
              ("regular hexagon", 6), ("regular octagon", 8)]

_SYM_LETTERS = [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 1), ("H", 2),
                ("I", 2), ("M", 1), ("T", 1), ("U", 1), ("V", 1), ("W", 1),
                ("X", 2), ("Y", 1)]

# quadrilateral facts: (name, pairs of parallel sides, right angles, equal sides,
#                       lines of symmetry)
_QUADS = [("square", 2, 4, 4, 4), ("rectangle", 2, 4, 2, 2), ("rhombus", 2, 0, 4, 2),
          ("parallelogram", 2, 0, 2, 0), ("trapezium", 1, 0, 0, 0), ("kite", 0, 0, 2, 1)]
_QUAD_NAMES = "square / rectangle / rhombus / parallelogram / trapezium / kite"


def _grid_size(d):
    return _by_d(d, 6, 8, 10)


def _coord(x, y):
    return "(%d,%d)" % (int(x), int(y))


# places and objects used when a coordinate plane is read as a map
_PLACES = ["library", "school", "park", "museum", "harbour", "post office",
           "swimming pool", "market", "castle", "windmill", "railway station", "farm"]

_OBJECTS = ["kite", "anchor", "star", "drum", "lantern", "acorn", "bell", "shell"]


def _spread_points(n, size):
    """`n` distinct lattice points in the first quadrant, all with different x and y."""
    xs = random.sample(range(0, size + 1), n)
    ys = random.sample(range(0, size + 1), n)
    return list(zip(xs, ys))


def _L_cells(R, C, r, c):
    """An L-shape: an R x C rectangle with an r x c notch cut from the top right."""
    return [[i, j] for i in range(R) for j in range(C)
            if not (i < r and j >= C - c)]


def _notch_cells(R, C, h, a, w):
    """An R x C rectangle with an h-deep, w-wide notch cut into the middle of the top edge."""
    return [[i, j] for i in range(R) for j in range(C)
            if not (i < h and a <= j < a + w)]


def _stair_cells(R, C):
    """A staircase: the bottom row is C squares long and each row above is one shorter."""
    return [[i, j] for i in range(R) for j in range(C - (R - 1 - i))]


def _perim(cells):
    """Unit edges on the boundary of a set of grid cells."""
    cs = set(map(tuple, cells))
    return sum(1 for (i, j) in cs for (di, dj) in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (i + di, j + dj) not in cs)


# ================================================================== 4.8 ======
@skill("Y4.8.a", "Identify and classify polygons", S8)
def _(d=1):
    d = _tier(d)
    # stretch: the many-sided shapes, where counting and naming are harder
    pool = _by_d(d, [s for s in _DRAWN if s[1] <= 6], _DRAWN, [s for s in _DRAWN if s[1] >= 5])
    name, sides = pick(pool)
    t = _pick_t([2, 2, 2, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # visual: count sides
        return {"prompt": "How many sides does this polygon have?",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": sides, "answer_type": "int",
                "solution": ["Count the straight sides all the way round.",
                             "It has %d sides." % sides]}

    if t == 1:                                        # visual: count vertices
        return {"prompt": "How many vertices (corners) does this polygon have?",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "vertices"},
                "answer": sides, "answer_type": "int",
                "solution": ["A polygon has as many vertices as sides.",
                             "It has %d vertices." % sides]}

    if t == 2:                                        # visual: name it
        nm, sd = pick([s for s in pool if s in _DRAWN_NAMEABLE] or _DRAWN_NAMEABLE)
        return {"prompt": "What is the name of this polygon? (type one word)",
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["It has %d straight sides." % sd,
                             "A polygon with %d sides is %s." % (sd, _a(nm))]}

    if t == 3:                                        # sides -> name (typed)
        nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
        return _num_q("A polygon has %d straight sides. What is it called?" % sd,
                      nm, "str", text=True, placeholder="polygon name",
                      solution=["A polygon with %d sides is called %s." % (sd, _a(nm))])

    if t == 4:                                        # regular or irregular
        regular = random.random() < 0.5
        sd = pick(_by_d(d, [3, 4, 6], [4, 5, 6, 8], [4, 5, 6, 7, 8]))
        desc = ("all %d sides equal and all %d angles equal" % (sd, sd)) if regular else \
               ("%d sides, but the sides are not all the same length" % sd)
        if d == 2 and not regular:                    # stretch: only half the rule is met
            desc = pick(["all %d sides equal, but its angles are not all equal" % sd,
                         "all %d angles equal, but its sides are not all equal" % sd])
        return _num_q("A polygon has %s. Is this polygon regular or irregular? "
                      "(type one word)" % desc,
                      "regular" if regular else "irregular", "str", text=True,
                      placeholder="regular / irregular",
                      solution=["A regular polygon has all sides equal AND all angles equal.",
                                "This polygon is %s." % ("regular" if regular else "irregular")])

    if t == 5:                                        # real world
        things = [("a stop sign", "octagon", 8),
                  ("a honeycomb cell", "hexagon", 6),
                  ("a football's black patch", "pentagon", 5),
                  ("a road warning sign", "triangle", 3),
                  ("a chess board square", "square", 4),
                  ("a 50p coin's outline", "heptagon", 7)]
        thing, nm, sd = pick(_by_d(d, [things[i] for i in (1, 3, 4)], things,
                                   [things[i] for i in (0, 2, 5)]))
        ask_sides = random.random() < 0.5
        if ask_sides:
            return _num_q("In the real world, %s is shaped like %s. "
                          "How many sides does it have?" % (thing, _a(nm)),
                          sd, "int", unit="sides",
                          solution=["%s has %d straight sides." % (_a(nm).capitalize(), sd)])
        return _num_q("In the real world, %s is shaped like a regular polygon with %d sides "
                      "(all sides and all angles equal). What is that polygon called? "
                      "(type one word)" % (thing, sd),
                      nm, "str", text=True, placeholder="polygon name",
                      solution=["A regular polygon with %d sides is %s." % (sd, _a(nm))])

    if t == 6:                                        # comparison
        polys = _by_d(d, _POLY[:5], _POLY, _POLY[2:])
        (n1, s1), (n2, s2) = random.sample(polys, 2)
        while s1 == s2:
            (n1, s1), (n2, s2) = random.sample(polys, 2)
        big, bs, small, ss = (n1, s1, n2, s2) if s1 > s2 else (n2, s2, n1, s1)
        return _num_q("How many MORE vertices does %s have than %s?" % (_a(big), _a(small)),
                      bs - ss, "int", unit="vertices",
                      solution=["%s has %d vertices and %s has %d."
                                % (_a(big).capitalize(), bs, _a(small), ss),
                                "%d − %d = %d." % (bs, ss, bs - ss)])

    if t == 7:                                        # sorting
        chosen = random.sample(_by_d(d, _POLY[:6], _POLY, _POLY), _by_d(d, 3, 4, 5))
        cut = pick(_by_d(d, [4, 5], [4, 5, 6], [5, 6, 7, 8]))
        cnt = sum(1 for _, sd in chosen if sd > cut)
        return _num_q("Sort these polygons by their number of sides: %s. "
                      "How many of them have MORE than %d sides?"
                      % (", ".join(nm for nm, _ in chosen), cut),
                      cnt, "int", unit="polygons",
                      solution=["Sides: %s." % ", ".join("%s %d" % (nm, sd) for nm, sd in chosen),
                                "%d of them have more than %d sides." % (cnt, cut)])

    if t == 8:                                        # total sides
        if d == 2:                                    # stretch: three of the larger polygons
            (n1, s1), (n2, s2), (n3, s3) = random.sample(_POLY[3:], 3)
            return _num_q("%s, %s and %s are drawn side by side. How many sides do they "
                          "have altogether?" % (_a(n1).capitalize(), _a(n2), _a(n3)),
                          s1 + s2 + s3, "int", unit="sides",
                          solution=["%d + %d + %d = %d sides." % (s1, s2, s3, s1 + s2 + s3)])
        (n1, s1), (n2, s2) = random.sample(_POLY[:5] if d == 0 else _POLY, 2)
        return _num_q("%s and %s are drawn side by side. How many sides do they have "
                      "altogether?" % (_a(n1).capitalize(), _a(n2)),
                      s1 + s2, "int", unit="sides",
                      solution=["%d + %d = %d sides." % (s1, s2, s1 + s2)])

    # riddle: sides + vertices
    nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
    return _num_q("A polygon has %d sides and vertices altogether (its sides added to "
                  "its vertices). What is the polygon called?" % (2 * sd),
                  nm, "str", text=True, placeholder="polygon name",
                  solution=["Sides and vertices are equal in number, so %d ÷ 2 = %d sides."
                            % (2 * sd, sd),
                            "A polygon with %d sides is %s." % (sd, _a(nm))])


@skill("Y4.8.b", "Draw polygons and plot shapes", S8)
def _(d=1):
    d = _tier(d)
    size = _grid_size(d)
    t = _pick_t([2, 2, 2, 1, 2, 1, 1, 2, 1])

    if t == 0:                                        # 4th vertex of a rectangle
        w = random.randint(2, size - 2)
        h = random.randint(2, size - 2)
        while h == w:
            h = random.randint(2, size - 2)
        x = random.randint(0, size - w)
        y = random.randint(0, size - h)
        return {"prompt": "Three corners of a rectangle are %s, %s and %s. "
                          "Plot the fourth corner."
                          % (_coord(x, y), _coord(x + w, y), _coord(x, y + h)),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + w, y + h), "answer_type": "coord",
                "solution": ["The rectangle is %d squares wide and %d squares tall." % (w, h),
                             "The fourth corner is %s." % _coord(x + w, y + h)]}

    if t == 1:                                        # 4th vertex of a square
        s = random.randint(2, size - 2)
        x = random.randint(0, size - s)
        y = random.randint(0, size - s)
        return {"prompt": "Three corners of a square are %s, %s and %s. "
                          "Plot the fourth corner."
                          % (_coord(x, y), _coord(x + s, y), _coord(x + s, y + s)),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x, y + s), "answer_type": "coord",
                "solution": ["Every side of the square is %d squares long." % s,
                             "The missing corner is %s." % _coord(x, y + s)]}

    if t == 2:                                        # top-right corner of a square
        s = random.randint(2, size - 2)
        x = random.randint(0, size - s)
        y = random.randint(0, size - s)
        return {"prompt": "A square is drawn with its bottom-left corner at %s and sides "
                          "of %d squares. Plot the top-right corner of the square."
                          % (_coord(x, y), s),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + s, y + s), "answer_type": "coord",
                "solution": ["Move %d squares right and %d squares up from %s."
                             % (s, s, _coord(x, y)),
                             "The top-right corner is %s." % _coord(x + s, y + s)]}

    if t == 3:                                        # typed coordinates
        w = random.randint(2, size - 2)
        h = random.randint(2, size - 2)
        while h == w:
            h = random.randint(2, size - 2)
        x = random.randint(0, size - w)
        y = random.randint(0, size - h)
        return _num_q("Three corners of a rectangle are %s, %s and %s. Write the "
                      "coordinates of the fourth corner."
                      % (_coord(x, y), _coord(x + w, y), _coord(x, y + h)),
                      _coord(x + w, y + h), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["The fourth corner lines up with %s across and %s up."
                                % (_coord(x + w, y), _coord(x, y + h)),
                                "It is %s." % _coord(x + w, y + h)])

    if t == 4:                                        # right-angled triangle
        b = random.randint(2, size - 2)
        ht = random.randint(2, size - 2)
        x = random.randint(0, size - b)
        y = random.randint(0, size - ht)
        return {"prompt": "A right-angled triangle has vertices at %s and %s. Its third "
                          "vertex is %d squares directly above %s. Plot the third vertex."
                          % (_coord(x, y), _coord(x + b, y), ht, _coord(x, y)),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x, y + ht), "answer_type": "coord",
                "solution": ["Directly above means the x-coordinate stays as %d." % x,
                             "%d + %d = %d, so the vertex is %s."
                             % (y, ht, y + ht, _coord(x, y + ht))]}

    if t == 5:                                        # how many vertices to plot
        nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
        return _num_q("To draw %s you plot one point for each vertex, then join them up. "
                      "How many points must you plot?" % _a(nm),
                      sd, "int", unit="points",
                      solution=["%s has %d vertices." % (_a(nm).capitalize(), sd),
                                "So you plot %d points." % sd])

    if t == 6:                                        # length of a side from coordinates
        w = random.randint(2, size - 1)
        h = random.randint(2, size - 1)
        x = random.randint(0, size - w)
        y = random.randint(0, size - h)
        ask_w = random.random() < 0.5
        return _num_q("A rectangle has corners at %s, %s, %s and %s. How many squares "
                      "long is its %s?"
                      % (_coord(x, y), _coord(x + w, y), _coord(x + w, y + h),
                         _coord(x, y + h), "base" if ask_w else "height"),
                      w if ask_w else h, "int", unit="squares",
                      solution=["The base runs from x = %d to x = %d." % (x, x + w)
                                if ask_w else
                                "The height runs from y = %d to y = %d." % (y, y + h),
                                "That is %d squares." % (w if ask_w else h)])

    if t == 7:                                        # centre of a rectangle
        w = 2 * random.randint(1, max(1, (size - 1) // 2))
        h = 2 * random.randint(1, max(1, (size - 1) // 2))
        x = random.randint(0, size - w)
        y = random.randint(0, size - h)
        return {"prompt": "A rectangle has opposite corners at %s and %s, with its sides "
                          "along the grid lines. Plot the point where its two diagonals "
                          "cross." % (_coord(x, y), _coord(x + w, y + h)),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + w // 2, y + h // 2), "answer_type": "coord",
                "solution": ["The diagonals cross at the middle of the rectangle.",
                             "Half of %d is %d and half of %d is %d, so the point is %s."
                             % (w, w // 2, h, h // 2, _coord(x + w // 2, y + h // 2))]}

    # perimeter of the plotted rectangle (reasoning)
    w = random.randint(2, size - 1)
    h = random.randint(2, size - 1)
    x = random.randint(0, size - w)
    y = random.randint(0, size - h)
    return _num_q("A rectangle is drawn with corners at %s, %s, %s and %s. What is its "
                  "perimeter, in squares?"
                  % (_coord(x, y), _coord(x + w, y), _coord(x + w, y + h), _coord(x, y + h)),
                  2 * (w + h), "int", unit="squares",
                  solution=["The rectangle is %d squares by %d squares." % (w, h),
                            "%d + %d + %d + %d = %d." % (w, h, w, h, 2 * (w + h))])


@skill("Y4.8.c", "Classify triangles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 2, 1, 1, 1])

    if t == 0:                                        # classify by sides
        kind = pick(["scalene", "isosceles", "equilateral"])
        if kind == "equilateral":
            s = random.randint(3, 12)
            sides = (s, s, s)
        elif kind == "isosceles":
            s = random.randint(4, 12)
            b = random.randint(2, 2 * s - 1)
            while b == s:
                b = random.randint(2, 2 * s - 1)
            sides = (s, s, b)
        else:
            a, b, c = sorted(random.sample(range(4, 15), 3))
            while a + b <= c:
                a, b, c = sorted(random.sample(range(4, 15), 3))
            if d == 2:                                # stretch: lengths one apart, easy to misread
                a = random.randint(5, 12)
                b, c = a + 1, a + 2
            sides = (a, b, c)
        if d == 2:                                    # stretch: the equal sides are not listed first
            sides = tuple(random.sample(sides, 3))
        return _num_q("A triangle has sides of %d cm, %d cm and %d cm. Is it scalene, "
                      "isosceles or equilateral? (type one word)" % sides,
                      kind, "str", text=True,
                      placeholder="scalene / isosceles / equilateral",
                      solution=["Equilateral means 3 equal sides, isosceles means exactly "
                                "2 equal sides, scalene means no equal sides.",
                                "This triangle is %s." % kind])

    if t == 1:                                        # classify by angles: test with a page corner
        test, kind = pick(_by_d(d, [
            ("the corner fits exactly into one of the angles", "right"),
            ("one angle is wider than the corner, so a gap is left beside it", "obtuse"),
            ("the corner is too wide to fit into any of the angles", "acute"),
        ], [
            ("the corner fits exactly into one of the angles", "right"),
            ("one angle opens wider than the corner", "obtuse"),
            ("every angle is narrower than the corner", "acute"),
            ("the corner is too wide to fit into any of the angles", "acute"),
        ], [                                          # stretch: the deciding angle comes last
            ("two angles are narrower than the corner and the third matches it exactly",
             "right"),
            ("two angles are narrower than the corner, but the third leaves a gap when the "
             "corner is fitted into it", "obtuse"),
            ("even the widest angle is narrower than the corner", "acute"),
            ("the corner fits exactly into the largest angle", "right"),
        ]))
        return _num_q("%s tests each angle of a triangle with the square corner of a page: "
                      "%s. Is it an acute, right or obtuse triangle? (type one word)"
                      % (pick(NAMES), test),
                      kind, "str", text=True, placeholder="acute / right / obtuse",
                      solution=["The corner of a page is a right angle.",
                                "A right triangle has a right angle; an obtuse triangle has an "
                                "angle bigger than a right angle; in an acute triangle every "
                                "angle is smaller than a right angle.",
                                "So this triangle is %s." % kind])

    if t == 2:                                        # name -> equal sides
        kind, eq = pick([("equilateral", 3), ("isosceles", 2), ("scalene", 0)][:2 if d == 0 else 3])
        if d == 2:                                    # stretch: equal angles go with equal sides
            return _num_q("How many equal angles does %s triangle have? (type 0 if none "
                          "are equal)" % _a(kind), eq, "int", unit="angles",
                          solution=["Equal sides sit opposite equal angles.",
                                    "%s triangle has %s, so it has %d equal angles."
                                    % (_a(kind).capitalize(), _pl(eq, "equal side"), eq)])
        return _num_q("How many equal sides does %s triangle have?" % _a(kind),
                      eq, "int", unit="sides",
                      solution=["%s triangle has %s of equal length."
                                % (_a(kind).capitalize(), _pl(eq, "side"))])

    if t == 3:                                        # described angles -> acute / right / obtuse
        desc, kind = pick(_by_d(d, [
            ("one angle that is a right angle", "right"),
            ("one angle that is bigger than a right angle", "obtuse"),
            ("three angles that are all smaller than a right angle", "acute"),
        ], [
            ("one square corner, like the corner of a page", "right"),
            ("one angle that is wider than the corner of a book", "obtuse"),
            ("three angles that are all narrower than a square corner", "acute"),
            ("one angle that is bigger than a right angle", "obtuse"),
        ], [                                          # stretch: the deciding angle is hidden in the list
            ("two angles smaller than a right angle and one angle bigger than a right "
             "angle", "obtuse"),
            ("two angles smaller than a right angle and one angle that is exactly a "
             "quarter turn", "right"),
            ("a largest angle that is smaller than a right angle", "acute"),
            ("three equal sides, so three equal angles that are each smaller than a right "
             "angle", "acute"),
        ]))
        return _num_q("A triangle has %s. Is it an acute, right or obtuse triangle? "
                      "(type one word)" % desc,
                      kind, "str", text=True, placeholder="acute / right / obtuse",
                      solution=["A right triangle has a right angle; an obtuse triangle has an "
                                "angle bigger than a right angle; in an acute triangle every "
                                "angle is smaller than a right angle.",
                                "So this triangle is %s." % kind])

    if t == 4:                                        # description -> name
        descs = [("all three sides the same length", "equilateral"),
                 ("exactly two sides the same length", "isosceles"),
                 ("no two sides the same length", "scalene"),
                 ("all three angles equal", "equilateral"),
                 ("two equal angles at its base", "isosceles"),
                 ("three different angles", "scalene")]
        desc, kind = pick(_by_d(d, descs[:3], descs[:5], descs[3:]))
        return _num_q("A triangle has %s. What kind of triangle is it? (type one word)" % desc,
                      kind, "str", text=True,
                      placeholder="scalene / isosceles / equilateral",
                      solution=["A triangle with %s is %s." % (desc, _a(kind))])

    if t == 5:                                        # sort triangles by their sides
        if d == 2:                                    # stretch: use the two equal sides
            a = random.randint(5, 15)
            b = random.randint(2, 2 * a - 1)
            while b == a:
                b = random.randint(2, 2 * a - 1)
            return _num_q("An isosceles triangle has two sides of %d cm and a third side of "
                          "%d cm. What is its perimeter?" % (a, b),
                          2 * a + b, "int", unit="cm",
                          solution=["The two equal sides are %d cm each." % a,
                                    "%d + %d + %d = %d cm." % (a, a, b, 2 * a + b)])
        tris = [(5, 5, 5), (4, 6, 7), (6, 6, 3), (8, 8, 8), (3, 5, 6), (7, 4, 7),
                (9, 9, 5), (5, 7, 9)]
        chosen = random.sample(tris, _by_d(d, 3, 4, 4))
        want = pick(["equilateral", "isosceles", "scalene"])

        def _kind(s):
            n = len(set(s))
            return "equilateral" if n == 1 else ("isosceles" if n == 2 else "scalene")
        cnt = sum(1 for s in chosen if _kind(s) == want)
        return _num_q("Here are the side lengths of some triangles, in cm: %s. How many of "
                      "them are %s? (type 0 if none)"
                      % ("; ".join("%d, %d, %d" % s for s in chosen), want),
                      cnt, "int", unit="triangles",
                      solution=["%s." % "; ".join("%d, %d, %d is %s" % (s + (_kind(s),))
                                                 for s in chosen),
                                "%d of them %s %s." % (cnt, "is" if cnt == 1 else "are", want)])

    if t == 6:                                        # visual (the drawn triangle is regular)
        ask = _by_d(d, "classify", pick(["classify", "symmetry"]), "symmetry")
        if ask == "classify":
            return {"prompt": "This triangle has three equal sides and three equal angles. "
                              "Is it scalene, isosceles or equilateral? (type one word)",
                    "component": "shape",
                    "spec": {"kind": "2d", "name": "triangle", "ask": "name"},
                    "answer": "equilateral", "answer_type": "str",
                    "solution": ["Three equal sides means equilateral."]}
        return {"prompt": "This is an equilateral triangle. "
                          "How many lines of symmetry does it have?",
                "component": "shape",
                "spec": {"kind": "2d", "name": "triangle", "ask": "lines_of_symmetry"},
                "answer": 3, "answer_type": "int",
                "solution": ["A fold from each vertex to the middle of the opposite side "
                             "matches the two halves.",
                             "An equilateral triangle has 3 lines of symmetry."]}

    if t == 7:                                        # isosceles: a missing side from the perimeter
        a = random.randint(*_by_d(d, (3, 9), (6, 20), (8, 40)))
        b = random.randint(2, 2 * a - 1)
        while b == a:
            b = random.randint(2, 2 * a - 1)
        per = 2 * a + b
        if d == 2:                                    # stretch: find the two equal sides
            return _num_q("An isosceles triangle has a perimeter of %d cm. One side is %d cm "
                          "and the other two sides are equal to each other. How long is each of the "
                          "equal sides?" % (per, b),
                          a, "int", unit="cm",
                          solution=["%d − %d = %d cm is shared by the two equal sides."
                                    % (per, b, 2 * a),
                                    "%d ÷ 2 = %d cm." % (2 * a, a)])
        return _num_q("An isosceles triangle has two equal sides of %d cm and a perimeter "
                      "of %d cm. How long is the third side?" % (a, per),
                      b, "int", unit="cm",
                      solution=["The two equal sides make %d + %d = %d cm." % (a, a, 2 * a),
                                "%d − %d = %d cm." % (per, 2 * a, b)])

    if t == 8:                                        # perimeter of an equilateral triangle
        s = random.randint(3, _by_d(d, 9, 15, 25))
        return _num_q("An equilateral triangle has sides of %d cm. What is its perimeter?" % s,
                      3 * s, "int", unit="cm",
                      solution=["All 3 sides are %d cm." % s,
                                "3 × %d = %d cm." % (s, 3 * s)])

    # reasoning: can a triangle be both?
    kind, ans = pick(_by_d(d, [("three equal angles", "equilateral"),
                               ("a right angle and two equal sides", "isosceles")],
                           [("a right angle and two equal sides", "isosceles"),
                            ("one angle bigger than a right angle and no equal sides",
                             "scalene"),
                            ("three equal angles", "equilateral")],
                           [("two equal angles and a third angle that is larger", "isosceles"),
                            ("a right angle and two other angles that are different from "
                             "each other", "scalene"),
                            ("a right angle and two equal angles", "isosceles"),
                            ("one angle bigger than a right angle and no equal sides",
                             "scalene")]))
    return _num_q("A triangle has %s. Classify it by its sides: scalene, isosceles or "
                  "equilateral? (type one word)" % kind,
                  ans, "str", text=True, placeholder="scalene / isosceles / equilateral",
                  solution=["Classifying by sides means counting equal sides. Equal angles "
                            "sit opposite equal sides, so equal angles count too.",
                            "This triangle is %s." % ans])


@skill("Y4.8.d", "Classify quadrilaterals", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2 if d == 2 else 0])
    # easy: the everyday quadrilaterals; stretch: lean on the ones pupils mix up
    easy_q = ("square", "rectangle", "trapezium")
    hard_q = ("rhombus", "parallelogram", "trapezium", "kite")
    quads = _by_d(d, [q for q in _QUADS if q[0] in easy_q], _QUADS,
                  [q for q in _QUADS if q[0] in hard_q])

    if t == 0:                                        # attributes -> name
        attrs, quad = pick([x for x in [
            ("4 equal sides and 4 right angles", "square"),
            ("4 right angles, with opposite sides equal but not all four sides equal",
             "rectangle"),
            ("4 equal sides but no right angles", "rhombus"),
            ("two pairs of parallel sides, no right angles and not all sides equal",
             "parallelogram"),
            ("exactly one pair of parallel sides", "trapezium"),
            ("two pairs of equal sides next to each other and no parallel sides", "kite"),
        ] if d == 1 or x[1] in [q[0] for q in quads]])
        return _num_q("Which quadrilateral has %s? (type the name)" % attrs,
                      quad, "str", text=True, placeholder=_QUAD_NAMES,
                      solution=["%s has %s." % (_a(quad).capitalize(), attrs)])

    if t == 1:                                        # pairs of parallel sides
        quad, par, ra, eq, sym = pick(quads)
        return _num_q("How many pairs of parallel sides does %s have?" % _a(quad),
                      par, "int", unit="pairs",
                      solution=["%s has %s of parallel sides."
                                % (_a(quad).capitalize(), _pl(par, "pair"))])

    if t == 2:                                        # right angles
        quad, par, ra, eq, sym = pick(quads)
        return _num_q("How many right angles must %s always have?" % _a(quad),
                      ra, "int", unit="right angles",
                      solution=["%s has %s." % (_a(quad).capitalize(),
                                                _pl(ra, "right angle") if ra else
                                                "no right angles")])

    if t == 3:                                        # perpendicular sides
        quad, per = pick(_by_d(d, [("square", 4), ("rectangle", 4)],
                               [("square", 4), ("rectangle", 4), ("rhombus", 0),
                                ("parallelogram", 0), ("kite", 0)],
                               [("rhombus", 0), ("parallelogram", 0), ("kite", 0),
                                ("square", 4)]))
        return _num_q("Two sides are perpendicular when they meet at a right angle. "
                      "How many pairs of perpendicular sides must %s always have at its corners?"
                      % _a(quad),
                      per, "int", unit="pairs",
                      solution=["A pair of perpendicular sides meets at a right angle.",
                                "%s has %d right-angled corners." % (_a(quad).capitalize(), per)])

    if t == 4:                                        # visual: square / rectangle
        nm = pick(["square", "rectangle"])
        ask = pick(["sides", "vertices", "parallel", "symmetry"])
        if ask == "sides":
            return {"prompt": "This quadrilateral has square corners. How many sides does "
                              "it have?",
                    "component": "shape",
                    "spec": {"kind": "2d", "name": nm, "ask": "sides",
                             "marks": "right_angle"},
                    "answer": 4, "answer_type": "int",
                    "solution": ["A quadrilateral always has 4 sides."]}
        if ask == "vertices":
            return {"prompt": "Every corner of this quadrilateral is a right angle. "
                              "How many right angles does it have?",
                    "component": "shape",
                    "spec": {"kind": "2d", "name": nm, "ask": "vertices",
                             "marks": "right_angle"},
                    "answer": 4, "answer_type": "int",
                    "solution": ["It has 4 corners and every one is a right angle."]}
        if ask == "parallel":
            return {"prompt": "In this quadrilateral the opposite sides are parallel. "
                              "How many PAIRS of parallel sides does it have?",
                    "component": "shape",
                    "spec": {"kind": "2d", "name": nm, "ask": "sides"},
                    "answer": 2, "answer_type": "int",
                    "solution": ["The top and bottom are one pair; the two ends are another.",
                                 "That is 2 pairs of parallel sides."]}
        return {"prompt": "How many lines of symmetry does this %s have?" % nm,
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "lines_of_symmetry"},
                "answer": 4 if nm == "square" else 2, "answer_type": "int",
                "solution": ["Look for every fold that makes the two halves match.",
                             "%s has %s of symmetry." % (_a(nm).capitalize(),
                                                         _pl(4 if nm == "square" else 2, "line"))]}

    if t == 5:                                        # all four sides equal?
        quad = pick([q[0] for q in quads] if d != 1 else
                    ["square", "rectangle", "rhombus", "parallelogram", "trapezium", "kite"])
        ans = "yes" if quad in ("square", "rhombus") else "no"
        return _num_q("Does %s always have all four sides the same length? "
                      "(type yes or no)" % _a(quad),
                      ans, "str", text=True, placeholder="yes / no",
                      solution=["A square and a rhombus are the quadrilaterals with 4 "
                                "equal sides.",
                                "So the answer for %s is %s." % (_a(quad), ans)])

    if t == 6:                                        # real-life
        things = [("a football pitch", "rectangle"),
                  ("a chess board", "square"),
                  ("a kite flown on a string", "kite"),
                  ("the face of a house brick", "rectangle"),
                  ("a leaning street sign shaped like a squashed square", "rhombus")]
        thing, quad = pick(_by_d(d, things[:2] + things[3:4], things, things[2:3] + things[4:]))
        return _num_q("In the real world, %s is shaped like which quadrilateral? "
                      "(type the name)" % thing,
                      quad, "str", text=True, placeholder=_QUAD_NAMES,
                      solution=["%s is shaped like %s." % (thing.capitalize(), _a(quad))])

    if t == 7:                                        # sorting
        two = not (d == 2 and random.random() < 0.5)
        # "two pairs" leaves the trapezium out: whether one can have two depends on the definition taught
        chosen = random.sample([q for q in _QUADS if not two or q[0] != "trapezium"], _by_d(d, 3, 4, 5))
        if not two:                                   # stretch: a different property to sort by
            cnt = sum(1 for q in chosen if q[1] >= 1)
            return _num_q("Sort these quadrilaterals: %s. How many of them have AT LEAST ONE "
                          "pair of parallel sides?" % ", ".join(q[0] for q in chosen),
                          cnt, "int", unit="quadrilaterals",
                          solution=["Pairs of parallel sides: %s."
                                    % ", ".join("%s %d" % (q[0], q[1]) for q in chosen),
                                    "%d of them have at least 1 pair." % cnt])
        cnt = sum(1 for q in chosen if q[1] == 2)
        return _num_q("Sort these quadrilaterals: %s. How many of them have TWO pairs of "
                      "parallel sides?" % ", ".join(q[0] for q in chosen),
                      cnt, "int", unit="quadrilaterals",
                      solution=["Pairs of parallel sides: %s."
                                % ", ".join("%s %d" % (q[0], q[1]) for q in chosen),
                                "%d of them have 2 pairs." % cnt])

    if t == 8:                                        # lines of symmetry of a quadrilateral
        quad, sym = pick(_by_d(d, [("square", 4), ("rectangle", 2)],
                               [("square", 4), ("rectangle", 2), ("rhombus", 2),
                                ("parallelogram", 0), ("kite", 1)],
                               [("rhombus", 2), ("parallelogram", 0), ("kite", 1),
                                ("rectangle", 2)]))
        return _num_q("How many lines of symmetry does %s have?" % _a(quad),
                      sym, "int", unit="lines",
                      solution=["%s has %s of symmetry."
                                % (_a(quad).capitalize(), _pl(sym, "line"))])

    if t == 10:                                       # stretch: one family inside another
        q1, q2, ans, why = pick([
            ("square", "rectangle", "yes", "A square has 4 right angles, so it is a special rectangle."),
            ("rectangle", "square", "no", "A rectangle's sides need not all be equal."),
            ("square", "rhombus", "yes", "A square has 4 equal sides, so it is a special rhombus."),
            ("rhombus", "square", "no", "A rhombus need not have right angles."),
            ("rhombus", "parallelogram", "yes", "A rhombus has two pairs of parallel sides."),
            ("parallelogram", "rhombus", "no", "A parallelogram's sides need not all be equal."),
            ("rectangle", "parallelogram", "yes", "A rectangle has two pairs of parallel sides."),
            ("parallelogram", "rectangle", "no", "A parallelogram need not have right angles."),
        ])
        return _num_q("Is every %s also %s? (type yes or no)" % (q1, _a(q2)),
                      ans, "str", text=True, placeholder="yes / no",
                      solution=[why, "So the answer is %s." % ans])

    # perimeter from the properties: the equal sides need not all be given
    if d == 0:                                        # easy: a square or rectangle
        if random.random() < 0.5:
            s = random.randint(3, 12)
            return _num_q("A square has sides of %d cm. What is its perimeter?" % s,
                          4 * s, "int", unit="cm",
                          solution=["All 4 sides of a square are equal.",
                                    "4 × %d = %d cm." % (s, 4 * s)])
        w, h = random.sample(range(2, 13), 2)
        return _num_q("A rectangle is %d cm long and %d cm wide. What is its perimeter?"
                      % (w, h), 2 * (w + h), "int", unit="cm",
                      solution=["Opposite sides of a rectangle are equal.",
                                "%d + %d + %d + %d = %d cm." % (w, h, w, h, 2 * (w + h))])
    if d == 1:                                        # the shapes pupils mix up
        quad = pick(["rhombus", "parallelogram", "kite"])
        if quad == "rhombus":
            s = random.randint(4, 15)
            return _num_q("A rhombus has one side of %d cm. What is its perimeter?" % s,
                          4 * s, "int", unit="cm",
                          solution=["All 4 sides of a rhombus are equal.",
                                    "4 × %d = %d cm." % (s, 4 * s)])
        a, b = random.sample(range(3, 16), 2)
        how = ("Opposite sides of a parallelogram are equal." if quad == "parallelogram"
               else "A kite has two pairs of equal sides next to each other.")
        return _num_q("%s has two sides next to each other of %d cm and %d cm. What is its "
                      "perimeter?" % (_a(quad).capitalize(), a, b),
                      2 * (a + b), "int", unit="cm",
                      solution=[how, "%d + %d + %d + %d = %d cm." % (a, b, a, b, 2 * (a + b))])
    # stretch: work back from the perimeter
    if random.random() < 0.5:
        quad = pick(["square", "rhombus"])
        s = random.randint(6, 25)
        return _num_q("%s has a perimeter of %d cm. How long is each side?"
                      % (_a(quad).capitalize(), 4 * s),
                      s, "int", unit="cm",
                      solution=["All 4 sides of %s are equal." % _a(quad),
                                "%d ÷ 4 = %d cm." % (4 * s, s)])
    quad = pick(["rectangle", "parallelogram"])
    a, b = random.sample(range(4, 20), 2)
    return _num_q("%s has a perimeter of %d cm. One of its sides is %d cm. How long is "
                  "each side next to that one?"
                  % (_a(quad).capitalize(), 2 * (a + b), a),
                  b, "int", unit="cm",
                  solution=["Opposite sides are equal, so %d cm and the side next to it "
                            "make half the perimeter." % a,
                            "%d ÷ 2 = %d, and %d − %d = %d cm."
                            % (2 * (a + b), a + b, a + b, a, b)])


@skill("Y4.8.e", "Lines, line segments, rays and their relationships", S8)
def _(d=1):
    d = _tier(d)
    size = _grid_size(d)
    t = _pick_t([1, 1, 1, 1, 1, 2, 1, 1, 1, 1])

    if t == 0:                                        # vocabulary: which is it?
        desc, ans = pick(_by_d(d, [
            ("goes on for ever in both directions", "line"),
            ("has two endpoints", "line segment"),
        ], [
            ("goes on for ever in both directions", "line"),
            ("has two endpoints", "line segment"),
            ("starts at one endpoint and goes on for ever in one direction", "ray"),
        ], [                                          # stretch: described indirectly
            ("can be measured with a ruler because it stops at both ends", "line segment"),
            ("has exactly one endpoint", "ray"),
            ("has no endpoints at all", "line"),
            ("is like a beam of torchlight, starting at the torch", "ray"),
        ]))
        return _num_q("A straight path %s. Is it a line, a line segment or a ray? "
                      "(type the answer)" % desc,
                      ans, "str", text=True, placeholder="line / line segment / ray",
                      solution=["A straight path that %s is called a %s." % (desc, ans)])

    if t == 1:                                        # count endpoints
        if d == 2:                                    # stretch: a mixture to total up
            ns, nr, nl = random.randint(1, 4), random.randint(1, 3), random.randint(0, 2)
            tot = 2 * ns + nr
            return _num_q("A drawing has %s, %s and %s. How many endpoints are there "
                          "altogether?" % (_pl(ns, "line segment"), _pl(nr, "ray"),
                                           _pl(nl, "line")),
                          tot, "int", unit="endpoints",
                          solution=["A line segment has 2 endpoints, a ray has 1 and a line "
                                    "has none.",
                                    "%d × 2 + %d × 1 + %d × 0 = %d." % (ns, nr, nl, tot)])
        thing, ends = pick([("a line segment", 2), ("a ray", 1), ("a line", 0)][:2 if d == 0 else 3])
        return _num_q("How many endpoints does %s have?" % thing,
                      ends, "int", unit="endpoints",
                      solution=["%s has %s." % (thing.capitalize(),
                                                _pl(ends, "endpoint") if ends else
                                                "no endpoints")])

    if t == 2:                                        # horizontal / vertical from coords
        x = random.randint(0, size)
        y = random.randint(0, size)
        horizontal = random.random() < 0.5
        k = random.randint(1, max(1, size - 1))
        if horizontal:
            x2, y2 = min(size, x + k), y
            if x2 == x:
                x2 = max(0, x - k)
        else:
            x2, y2 = x, min(size, y + k)
            if y2 == y:
                y2 = max(0, y - k)
        ans = "horizontal" if y2 == y else "vertical"
        return _num_q("A line segment joins %s to %s. Is the segment horizontal or "
                      "vertical? (type one word)" % (_coord(x, y), _coord(x2, y2)),
                      ans, "str", text=True, placeholder="horizontal / vertical",
                      solution=["The y-coordinates are the same, so the segment goes "
                                "straight across." if ans == "horizontal" else
                                "The x-coordinates are the same, so the segment goes "
                                "straight up.",
                                "It is %s." % ans])

    if t == 3:                                        # parallel / perpendicular vocab
        descs = [("never meet, however far they are extended", "parallel"),
                 ("cross at a right angle", "perpendicular"),
                 ("stay exactly the same distance apart", "parallel"),
                 ("make a right angle where they meet", "perpendicular"),
                 ("meet to make a square corner, a quarter turn", "perpendicular"),
                 ("are like the opposite sides of a rectangle", "parallel")]
        desc, ans = pick(_by_d(d, descs[:2], descs[:4], descs[2:]))
        return _num_q("Two straight lines %s. What are they called? (type one word)" % desc,
                      ans, "str", text=True, placeholder="parallel / perpendicular",
                      solution=["Lines that %s are %s." % (desc, ans)])

    if t == 4:                                        # real-life parallel / perpendicular
        cases = [("railway tracks", "parallel"),
                 ("the two strokes of the letter L", "perpendicular"),
                 ("the lines on lined writing paper", "parallel"),
                 ("a flagpole and the flat ground", "perpendicular"),
                 ("the two long rails of a ladder", "parallel"),
                 ("the two edges of a straight road", "parallel"),
                 ("the corner of a picture frame", "perpendicular"),
                 ("the two long strokes of the letter H", "parallel"),
                 ("the two strokes of the letter T", "perpendicular"),
                 ("the top and bottom edges of a door", "parallel")]
        case, ans = pick(_by_d(d, cases[:4], cases[:8], cases[4:]))
        return _num_q("Are %s parallel or perpendicular? (type one word)" % case,
                      ans, "str", text=True, placeholder="parallel / perpendicular",
                      solution=["%s are %s." % (case.capitalize(), ans)])

    if t == 5:                                        # plot to make a horizontal segment
        horizontal = random.random() < 0.5
        k = random.randint(2, max(2, size - 2))
        if horizontal:
            x = random.randint(0, size - k)
            y = random.randint(0, size)
            ax, ay = x + k, y
            word, dirn = "horizontal", "to the right of"
        else:
            x = random.randint(0, size)
            y = random.randint(0, size - k)
            ax, ay = x, y + k
            word, dirn = "vertical", "above"
        return {"prompt": "Plot a point so that the line segment from %s to your point is "
                          "%s and %d squares long, with your point %s %s."
                          % (_coord(x, y), word, k, dirn, _coord(x, y)),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(ax, ay), "answer_type": "coord",
                "solution": ["A %s segment keeps the %s the same."
                             % (word, "y-coordinate" if horizontal else "x-coordinate"),
                             "Count %d squares %s %s to reach %s."
                             % (k, dirn.replace(" of", ""), _coord(x, y), _coord(ax, ay))]}

    if t == 6:                                        # clock hands
        if d == 2:                                    # stretch: find the other time
            h = pick([3, 9])
            other = 12 - h
            return _num_q("At %d o'clock the hands of a clock are perpendicular. At which "
                          "other o'clock time are the hands perpendicular too? "
                          "(type the hour)" % h,
                          other, "int",
                          solution=["The hands are perpendicular when they make a right angle.",
                                    "At %d o'clock the hour hand points the opposite way, "
                                    "still at a right angle to the minute hand." % other])
        h, ans = pick([(3, "perpendicular"), (9, "perpendicular"), (6, "neither")][:2 if d == 0 else 3])
        if ans == "neither":
            return _num_q("At 6 o'clock the two hands of a clock point in exactly opposite "
                          "directions, making a straight line. How many right angles make "
                          "the angle between them?",
                          2, "int", unit="right angles",
                          solution=["A straight line is a half turn.",
                                    "A half turn is two right angles."])
        return _num_q("At %d o'clock, the hands of a clock meet at a right angle. Are the "
                      "hands parallel or perpendicular? (type one word)" % h,
                      "perpendicular", "str", text=True,
                      placeholder="parallel / perpendicular",
                      solution=["Lines that meet at a right angle are perpendicular."])

    if t == 7:                                        # counting in a shape
        nm, par, per = pick(_by_d(d, [("square", 2, 4), ("rectangle", 2, 4)],
                                  [("square", 2, 4), ("rectangle", 2, 4),
                                   ("regular hexagon", 3, 0), ("regular octagon", 4, 0)],
                                  [("regular hexagon", 3, 0), ("regular octagon", 4, 0),
                                   ("kite", 0, 0), ("parallelogram", 2, 0),
                                   ("triangle", 0, 0)]))
        return _num_q("How many pairs of parallel sides does %s have?%s"
                      % (_a(nm), " (type 0 if none)" if d == 2 else ""),
                      par, "int", unit="pairs",
                      solution=["Opposite sides of %s are parallel." % _a(nm) if par >= 2 else
                                "Check each pair of sides of %s to see if they never meet." % _a(nm),
                                "There %s %s." % ("is" if par == 1 else "are", _pl(par, "pair"))])

    if t == 8:                                        # perpendicular from coordinates
        x = random.randint(1, size - 1)
        y = random.randint(1, size - 1)
        return _num_q("One line segment joins %s to %s. A second joins %s to %s. "
                      "Are the two segments parallel or perpendicular? (type one word)"
                      % (_coord(0, y), _coord(size, y), _coord(x, 0), _coord(x, size)),
                      "perpendicular", "str", text=True,
                      placeholder="parallel / perpendicular",
                      solution=["The first segment is horizontal and the second is vertical.",
                                "A horizontal and a vertical line cross at a right angle, "
                                "so they are perpendicular."])

    # two horizontal segments -> parallel
    y1, y2 = random.sample(range(0, size + 1), 2)
    return _num_q("One line segment joins %s to %s. Another joins %s to %s. Are the two "
                  "segments parallel or perpendicular? (type one word)"
                  % (_coord(0, y1), _coord(size, y1), _coord(0, y2), _coord(size, y2)),
                  "parallel", "str", text=True, placeholder="parallel / perpendicular",
                  solution=["Both segments are horizontal, so they never meet.",
                            "They are parallel."])


# Year 4 angles are compared with a right angle, not measured in degrees.
# Each described angle carries its size in sixths of a right angle, only to compare them.
_ANG_EASY = [("half a right angle", 3), ("a right angle", 6), ("a quarter turn", 6),
             ("one and a half right angles", 9), ("two right angles", 12),
             ("a half turn", 12)]


def _clock_ang(h):
    """The smaller angle between the hands at h o'clock, as (words, size)."""
    return ("the smaller angle between the hands of a clock at %d o'clock" % h,
            2 * min(h, 12 - h))


def _ang_kind(size):
    return ("acute" if size < 6 else "right" if size == 6 else
            "obtuse" if size < 12 else "straight")


def _ang_pool(d):
    """Described angles: easy in right angles, stretch read off a clock face."""
    clock = [_clock_ang(h) for h in range(1, 12)]
    return _by_d(d, _ANG_EASY, _ANG_EASY + clock[:6], clock)


@skill("Y4.8.f", "Compare and classify angles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # angle: classify (visual)
        choices = _by_d(d, ["acute", "right", "obtuse"],
                        ["acute", "right", "obtuse", "straight"],
                        ["acute", "right", "obtuse", "straight"])
        kind = pick(choices)
        near = d == 2                                 # stretch: close to a right angle
        deg = {"acute": lambda: random.choice([70, 75, 80, 85] if near
                                              else [20, 30, 35, 45, 55, 65, 75, 80]),
               "right": lambda: 90,
               "obtuse": lambda: random.choice([95, 100, 105, 110] if near
                                               else [100, 110, 120, 135, 150, 160, 170]),
               "straight": lambda: 180}[kind]()
        return {"prompt": "Look at the angle. Is it acute, right, obtuse or straight? "
                          "(type one word)",
                "component": "angle", "spec": {"mode": "classify", "degrees": deg},
                "answer": kind, "answer_type": "str",
                "solution": ["Acute is smaller than a right angle, right is exactly a square "
                             "corner, obtuse is bigger than a right angle but smaller than two, "
                             "and straight is two right angles.",
                             "This angle is %s, so it is %s."
                             % ({"acute": "smaller than a right angle",
                                 "right": "a square corner",
                                 "obtuse": "bigger than a right angle but not a straight line",
                                 "straight": "a straight line"}[kind], kind)]}

    if t == 1:                                        # drawn angle against a right angle
        deg = random.choice(_by_d(d, [25, 35, 145, 155],
                                  [40, 55, 65, 115, 125, 140],
                                  [75, 80, 84, 96, 100, 105]))   # stretch: close to a right angle
        kind = "acute" if deg < 90 else "obtuse"
        return {"prompt": "Imagine the corner of a page fitted into this angle. If the angle is "
                          "smaller than the corner, type acute; if it is bigger, type obtuse.",
                "component": "angle", "spec": {"mode": "classify", "degrees": deg},
                "answer": kind, "answer_type": "str",
                "solution": ["The corner of a page is a right angle.",
                             "This angle is %s than a right angle, so it is %s."
                             % ("smaller" if kind == "acute" else "bigger", kind)]}

    if t == 2:                                        # angle: turn (visual)
        deg = pick(_by_d(d, [90, 180], [90, 180, 270, 360], [180, 270, 360]))
        quarters = deg // 90
        word = {1: "quarter", 2: "half", 3: "three-quarter", 4: "full"}[quarters]
        if random.random() < 0.5:
            return {"prompt": "The arrow shows a turn. How many right angles does it turn "
                              "through?",
                    "component": "angle", "spec": {"mode": "turn", "degrees": deg},
                    "answer": quarters, "answer_type": "int",
                    "solution": ["Each quarter turn is one right angle.",
                                 "This is a %s turn, so it is %s."
                                 % (word, _pl(quarters, "right angle"))]}
        return {"prompt": "The arrow shows a turn. Is it a quarter, half, three-quarter or "
                          "full turn? (type one word)",
                "component": "angle", "spec": {"mode": "turn", "degrees": deg},
                "answer": word, "answer_type": "str",
                "solution": ["Count the right angles: 1 is a quarter turn, 2 a half turn, "
                             "3 a three-quarter turn and 4 a full turn.",
                             "This turn is %s, so it is a %s turn."
                             % (_pl(quarters, "right angle"), word)]}

    if t == 3:                                        # right angles in a turn (typed)
        word, ra = pick(_by_d(d, [("a quarter turn", 1), ("a half turn", 2),
                                  ("a straight angle", 2)],
                              [("a quarter turn", 1), ("a half turn", 2),
                               ("a three-quarter turn", 3), ("a full turn", 4),
                               ("a straight angle", 2)],
                              [("two half turns", 4), ("a half turn and a quarter turn", 3),
                               ("one and a half full turns", 6), ("two full turns", 8),
                               ("three quarter turns", 3)]))
        return _num_q("How many right angles make %s?" % word,
                      ra, "int", unit="right angles",
                      solution=["A quarter turn is 1 right angle and a full turn is 4.",
                                "%s is %s." % (word.capitalize(), _pl(ra, "right angle"))])

    if t == 4:                                        # classify a described angle (typed)
        descs = [("smaller than a right angle", "acute"),
                 ("exactly a quarter turn", "right"),
                 ("bigger than a right angle but smaller than a straight line", "obtuse"),
                 ("exactly a half turn", "straight")]
        desc, kind = pick(_by_d(d, descs[:3], descs + [(w, _ang_kind(s)) for w, s in _ANG_EASY
                                         if w != "a right angle"],
                                [(w, _ang_kind(s)) for w, s in _ang_pool(2)]))
        return _num_q("An angle is %s. Is it acute, right, obtuse or straight? "
                      "(type one word)" % desc,
                      kind, "str", text=True,
                      placeholder="acute / right / obtuse / straight",
                      solution=["Acute is smaller than a right angle, obtuse is between one and "
                                "two right angles, and straight is two right angles.",
                                "%s is %s." % (desc[0].upper() + desc[1:], kind)])

    if t == 5:                                        # compare two angles
        while True:
            (wa, sa), (wb, sb) = random.sample(_ang_pool(d), 2)
            if sa != sb and (d > 0 or _ang_kind(sa) != _ang_kind(sb)):
                break
        ans = "A" if sa > sb else "B"
        return _num_q("Angle A is %s. Angle B is %s. Which angle is larger? (type A or B)"
                      % (wa, wb),
                      ans, "str", text=True, placeholder="A / B",
                      solution=["Compare each angle with a right angle."
                                + (" On a clock the gap from one hour to the next is a third of a right angle."
                                   if "clock" in wa + wb else ""),
                                "Angle %s is larger." % ans])

    if t == 6:                                        # order angles by size
        n = _by_d(d, 3, 4, 4)
        while True:
            angs = random.sample(_ang_pool(d), n)
            if len(set(s for _, s in angs)) == n:
                break
        labels = "ABCD"[:n]
        order = sorted(range(n), key=lambda i: angs[i][1])
        if d == 0:
            ask, pos = pick([("smallest", 0), ("largest", n - 1)])
            q = "Which angle is the %s?" % ask
        else:
            pos = random.randrange(1, n - 1)
            q = ("Put them in order from smallest to largest. Which angle comes %s?"
                 % ["1st", "2nd", "3rd", "4th"][pos])
        return _num_q("%s %s (type the letter)"
                      % (" ".join("Angle %s is %s." % (labels[i], angs[i][0]) for i in range(n)), q),
                      labels[order[pos]], "str", text=True, placeholder="A, B, C or D",
                      solution=["Smallest to largest: %s." % ", ".join(labels[i] for i in order),
                                "So the answer is %s." % labels[order[pos]]])

    if t == 7:                                        # count the acute or obtuse angles
        hours = _by_d(d, [1, 2, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
                      [2, 3, 4, 8, 9, 10, 6, 5, 7])   # stretch: near a right angle, both sides
        hs = sorted(random.sample(hours, _by_d(d, 3, 4, 5)))
        want = pick(["acute", "obtuse"])
        hit = [h for h in hs if _ang_kind(_clock_ang(h)[1]) == want]
        return _num_q("Look at the smaller angle between the hands of a clock at each of these "
                      "times: %s. How many of the angles are %s? (type 0 if none)"
                      % (", ".join("%d o'clock" % h for h in hs), want),
                      len(hit), "int", unit="angles",
                      solution=["At 3 o'clock and 9 o'clock the hands make a right angle. "
                                "Closer to 12 the angle is acute; further from 12 (but not 6) "
                                "it is obtuse.",
                                ("The %s ones are at %s, so there %s %d."
                                 % (want, ", ".join("%d o'clock" % h for h in hit),
                                    "is" if len(hit) == 1 else "are", len(hit))) if hit else
                                "None of them is %s, so the answer is 0." % want])

    if t == 8:                                        # minute hand turn in right angles
        mins = pick(_by_d(d, [15, 30], [15, 30, 45, 60], [45, 75, 90, 120]))
        ra = mins // 15
        return _num_q("The minute hand of a clock turns a full turn every hour. How many right "
                      "angles does it turn through in %d minutes?" % mins,
                      ra, "int", unit="right angles",
                      solution=["15 minutes is a quarter turn: 1 right angle.",
                                "%d minutes is %s of 15 minutes, so %s."
                                % (mins, _pl(ra, "lot"), _pl(ra, "right angle"))])

    # compass turn in right angles
    dirs = ["North", "East", "South", "West"]
    i = random.randrange(4)
    j = (i + random.randint(1, 2 if d == 0 else 3)) % 4
    ra = (j - i) % 4
    who = pick(NAMES)
    way = "clockwise"
    if d == 2 and random.random() < 0.5:              # stretch: anticlockwise
        way, ra = "anticlockwise", 4 - ra
    return _num_q("%s faces %s and turns %s to face %s. How many right angles has %s "
                  "turned through?" % (who, dirs[i], way, dirs[j], who),
                  ra, "int", unit="right angles",
                  solution=["Each quarter turn between compass points is 1 right angle.",
                            "%s to %s %s is %s." % (dirs[i], dirs[j], way,
                                                    _pl(ra, "right angle"))])


@skill("Y4.8.g", "Lines of symmetry and symmetric figures", S8)
def _(d=1):
    d = _tier(d)
    drawn = list(_SYM_DRAWN.items())
    pool = _by_d(d, [k for k, v in drawn if v[0] <= 4], [k for k, v in drawn],
                 [k for k, v in drawn if v[0] >= 3])  # stretch: more lines to find
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2])

    if t in (0, 1):                                   # visual count
        nm = pick(pool)
        lines, label = _SYM_DRAWN[nm]
        return {"prompt": "How many lines of symmetry does this shape have?",
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "lines_of_symmetry"},
                "answer": lines, "answer_type": "int",
                "solution": ["Look for every fold line that makes the two halves match "
                             "exactly.",
                             "%s has %s of symmetry."
                             % (_a(label).capitalize(), _pl(lines, "line"))]}

    if t == 2:                                        # recall by name
        tricky = ("rectangle", "isosceles triangle", "scalene triangle", "rhombus",
                  "parallelogram", "kite")             # the ones pupils get wrong
        nm, lines = pick(_by_d(d, [s for s in _SYM_NAMED if s[1] <= 4],
                               _SYM_NAMED, [s for s in _SYM_NAMED if s[0] in tricky]))
        return _num_q("How many lines of symmetry does %s have?" % _a(nm),
                      lines, "int", unit="lines",
                      solution=["%s has %s of symmetry."
                                % (_a(nm).capitalize(), _pl(lines, "line"))])

    if t == 3:                                        # regular polygon rule
        sides = pick(_by_d(d, [3, 4], [3, 4, 5, 6], [3, 4, 5, 6, 7, 8, 9, 10]))
        return _num_q("A regular polygon has %d equal sides. How many lines of symmetry "
                      "does it have?" % sides,
                      sides, "int", unit="lines",
                      solution=["A regular polygon has as many lines of symmetry as sides.",
                                "So it has %d lines of symmetry." % sides])

    if t == 4:                                        # inverse
        sides = pick(_by_d(d, [3, 4], [3, 4, 5, 6, 8], [5, 6, 7, 8, 9, 10]))
        return _num_q("A regular polygon has %d lines of symmetry. How many sides does it "
                      "have?" % sides,
                      sides, "int", unit="sides",
                      solution=["For a regular polygon, lines of symmetry = number of sides.",
                                "So it has %d sides." % sides])

    if t == 5:                                        # capital letters
        if d == 2:                                    # stretch: some letters have none
            L, lines = pick([x for x in _SYM_LETTERS if x[1] == 2] +
                            [("F", 0), ("J", 0), ("L", 0), ("N", 0), ("P", 0), ("S", 0),
                             ("Z", 0), ("K", 1), ("D", 1)])
            return _num_q("Here is the capital letter %s. How many lines of symmetry does it "
                          "have? (type 0 if it has none)" % L,
                          lines, "int", unit="lines",
                          solution=["Fold the letter and see which folds match exactly.",
                                    "The letter %s has %s of symmetry."
                                    % (L, _pl(lines, "line") if lines else "no lines")])
        L, lines = pick(_SYM_LETTERS if d else [x for x in _SYM_LETTERS
                                                if x[0] in "AMTUVW"])
        return _num_q("The capital letter %s is written as a symmetric figure. How many "
                      "lines of symmetry does it have?" % L,
                      lines, "int", unit="lines",
                      solution=["Fold the letter and see which folds match exactly.",
                                "The letter %s has %s of symmetry." % (L, _pl(lines, "line"))])

    if t == 6:                                        # comparison
        named = _by_d(d, [s for s in _SYM_NAMED if s[0] in ("square", "rectangle",
                                                           "equilateral triangle",
                                                           "regular hexagon")],
                      _SYM_NAMED, _SYM_NAMED[3:])
        (n1, l1), (n2, l2) = random.sample(named, 2)
        while l1 == l2:
            (n1, l1), (n2, l2) = random.sample(named, 2)
        big, bl, small, sl = (n1, l1, n2, l2) if l1 > l2 else (n2, l2, n1, l1)
        return _num_q("How many MORE lines of symmetry does %s have than %s?"
                      % (_a(big), _a(small)),
                      bl - sl, "int", unit="lines",
                      solution=["%s has %d and %s has %d."
                                % (_a(big).capitalize(), bl, _a(small), sl),
                                "%d − %d = %d." % (bl, sl, bl - sl)])

    if t == 7:                                        # total
        if d == 2:                                    # stretch: three shapes
            (n1, l1), (n2, l2), (n3, l3) = random.sample(_SYM_NAMED, 3)
            return _num_q("%s, %s and %s are drawn on a poster. How many lines of symmetry "
                          "do the three shapes have altogether?"
                          % (_a(n1).capitalize(), _a(n2), _a(n3)),
                          l1 + l2 + l3, "int", unit="lines",
                          solution=["%s has %d, %s has %d and %s has %d."
                                    % (_a(n1).capitalize(), l1, _a(n2), l2, _a(n3), l3),
                                    "%d + %d + %d = %d." % (l1, l2, l3, l1 + l2 + l3)])
        (n1, l1), (n2, l2) = random.sample(_SYM_NAMED[:3] + _SYM_NAMED[8:] if d == 0
                                           else _SYM_NAMED, 2)
        return _num_q("%s and %s are drawn on a poster. How many lines of symmetry do the "
                      "two shapes have altogether?" % (_a(n1).capitalize(), _a(n2)),
                      l1 + l2, "int", unit="lines",
                      solution=["%s has %d and %s has %d."
                                % (_a(n1).capitalize(), l1, _a(n2), l2),
                                "%d + %d = %d." % (l1, l2, l1 + l2)])

    if t == 8:                                        # symmetric figure: complete the half
        half = random.randint(2, _by_d(d, 5, 9, 14))
        return _num_q("A symmetric figure is made of squares. One half of it, on one side of "
                      "the mirror line, is made of %s. The other half is its mirror image. "
                      "How many squares does the whole figure use?" % _pl(half, "square"),
                      2 * half, "int", unit="squares",
                      solution=["The mirror image uses the same number of squares.",
                                "%d + %d = %d squares." % (half, half, 2 * half)])

    if t == 9:                                        # reflections: image of a point
        size = _grid_size(d)
        vertical = random.random() < 0.5
        if vertical:
            m = random.randint(2, size - 2)
            gap = random.randint(1, min(m, size - m))
            x, y = m - gap, random.randint(0, size)
            img = _coord(m + gap, y)
            return _num_q("A point at %s is reflected in the vertical mirror line x = %d. "
                          "Write the coordinates of the reflection."
                          % (_coord(x, y), m),
                          img, "coord", text=True, placeholder="e.g. (3,5)",
                          solution=["The point is %s to the left of the mirror line, so its "
                                    "reflection is %s to the right of it."
                                    % (_pl(gap, "square"), _pl(gap, "square")),
                                    "%d + %d = %d, so the reflection is at %s."
                                    % (m, gap, m + gap, img)])
        m = random.randint(2, size - 2)
        gap = random.randint(1, min(m, size - m))
        x, y = random.randint(0, size), m - gap
        img = _coord(x, m + gap)
        return _num_q("A point at %s is reflected in the horizontal mirror line y = %d. "
                      "Write the coordinates of the reflection." % (_coord(x, y), m),
                      img, "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["The point is %s below the mirror line, so its reflection is "
                                "%s above it." % (_pl(gap, "square"), _pl(gap, "square")),
                                "%d + %d = %d, so the reflection is at %s."
                                % (m, gap, m + gap, img)])

    # reflections: distance from the mirror line, and what a reflection keeps the same
    if random.random() < 0.5:
        gap = random.randint(1, _by_d(d, 5, 9, 15))
        return _num_q("A shape is reflected in a mirror line. One corner of the shape is %s "
                      "from the mirror line. How many squares from the mirror line is the "
                      "reflection of that corner?" % _pl(gap, "square"),
                      gap, "int", unit="squares",
                      solution=["A reflection is the same distance from the mirror line as "
                                "the original, but on the other side.",
                                "So the reflection is %s from the mirror line."
                                % _pl(gap, "square")])
    nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
    ask_sides = random.random() < 0.5
    if ask_sides:
        return _num_q("%s is reflected in a mirror line. How many sides does the reflection "
                      "have?" % _a(nm).capitalize(),
                      sd, "int", unit="sides",
                      solution=["A reflection flips a shape over but does not change its "
                                "size or how many sides it has.",
                                "So the reflection has %d sides." % sd])
    s = random.randint(2, _by_d(d, 9, 15, 30))
    return _num_q("A square with sides of %d cm is reflected in a mirror line. What is the "
                  "length of each side of the reflection, in cm?" % s,
                  s, "int", unit="cm",
                  solution=["A reflection does not change the size of a shape.",
                            "Each side of the reflection is still %d cm." % s])


@skill("Y4.8.h", "Coordinates in the first quadrant", S8)
def _(d=1):
    d = _tier(d)
    size = _grid_size(d)
    t = _pick_t([2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2])

    if t == 0:                                        # plot a given point
        x, y = random.randint(0, size), random.randint(0, size)
        return {"prompt": "Plot the point %s on the grid." % _coord(x, y),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["The first number is along the x-axis: go %d right." % x,
                             "The second number is up the y-axis: go %d up." % y]}

    if t == 1:                                        # plot from a description
        x, y = random.randint(1, size), random.randint(1, size)
        return {"prompt": "Start at the origin (0,0). Plot the point that is %s along the "
                          "x-axis and %s up the y-axis."
                          % (_pl(x, "square"), _pl(y, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["Across first, then up.",
                             "The point is %s." % _coord(x, y)]}

    if t == 2:                                        # treasure map word problem
        who = pick(NAMES)
        x, y = random.randint(1, size), random.randint(1, size)
        return {"prompt": "%s buries a treasure %s east and %s north of the corner marked "
                          "(0,0) on a square map. Plot where the treasure is."
                          % (who, _pl(x, "square"), _pl(y, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x, y), "answer_type": "coord",
                "solution": ["East is along the x-axis and north is up the y-axis.",
                             "The treasure is at %s." % _coord(x, y)]}

    if t == 3:                                        # typed coordinates
        x, y = random.randint(0, size), random.randint(0, size)
        return _num_q("A point is %s to the right of the y-axis and %s "
                      "above the x-axis. Write its coordinates." % (_pl(x, "square"), _pl(y, "square")),
                      _coord(x, y), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["Coordinates are written (across, up).",
                                "The point is %s." % _coord(x, y)])

    if t == 4:                                        # read one coordinate
        x, y = random.randint(0, size), random.randint(0, size)
        want = pick(["x", "y"])
        return _num_q("A point is at %s. What is its %s-coordinate?" % (_coord(x, y), want),
                      x if want == "x" else y, "int",
                      solution=["Coordinates are written (x, y).",
                                "The %s-coordinate is %d." % (want, x if want == "x" else y)])

    if t == 5:                                        # plot relative to another point
        right = random.random() < 0.5
        up = random.random() < 0.5
        x = random.randint(0, size - 2) if right else random.randint(2, size)
        y = random.randint(0, size - 2) if up else random.randint(2, size)
        dx = random.randint(1, size - x) if right else -random.randint(1, x)
        dy = random.randint(1, size - y) if up else -random.randint(1, y)
        return {"prompt": "Point A is at %s. Plot point B, which is %s to the %s of A and "
                          "%s %s A."
                          % (_coord(x, y), _pl(abs(dx), "square"),
                             "right" if right else "left", _pl(abs(dy), "square"),
                             "above" if up else "below"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["Moving %s changes the x-coordinate from %d to %d."
                             % ("right" if right else "left", x, x + dx),
                             "Moving %s changes the y-coordinate from %d to %d, so B is %s."
                             % ("up" if up else "down", y, y + dy,
                                _coord(x + dx, y + dy))]}

    if t == 6:                                        # points on an axis
        k = random.randint(1, size)
        on_x = random.random() < 0.5
        return {"prompt": "Plot the point that is on the %s-axis, %s from the origin."
                          % ("x" if on_x else "y", _pl(k, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(k, 0) if on_x else _coord(0, k), "answer_type": "coord",
                "solution": ["Every point on the %s-axis has %s-coordinate 0."
                             % ("x" if on_x else "y", "y" if on_x else "x"),
                             "The point is %s." % (_coord(k, 0) if on_x else _coord(0, k))]}

    if t == 7:                                        # distance between two points
        y = random.randint(0, size)
        x1, x2 = sorted(random.sample(range(0, size + 1), 2))
        return _num_q("Point A is at %s and point B is at %s. How many squares apart are "
                      "they?" % (_coord(x1, y), _coord(x2, y)),
                      x2 - x1, "int", unit="squares",
                      solution=["Both points have y-coordinate %d, so count along." % y,
                                "%d − %d = %s." % (x2, x1, _pl(x2 - x1, "square"))])

    if t == 8:                                        # midpoint of a horizontal segment
        y = random.randint(0, size)
        x1 = random.randint(0, size - 2)
        span = 2 * random.randint(1, max(1, (size - x1) // 2))
        x2 = x1 + span
        return _num_q("Point A is at %s and point B is at %s. Write the coordinates of the "
                      "point exactly halfway between them."
                      % (_coord(x1, y), _coord(x2, y)),
                      _coord(x1 + span // 2, y), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["The two points are %d squares apart." % span,
                                "Half of %d is %d, so the middle point is %s."
                                % (span, span // 2, _coord(x1 + span // 2, y))])

    if t == 9:                                        # objects on a coordinate plane
        objs = random.sample(_OBJECTS, 3)
        pts = _spread_points(3, size)
        listed = ", ".join("the %s is at %s" % (objs[k], _coord(*pts[k])) for k in range(3))
        k = random.randrange(3)
        if random.random() < 0.5:
            return _num_q("Some objects are drawn on a coordinate plane: %s. Write the "
                          "coordinates of the %s." % (listed, objs[k]),
                          _coord(*pts[k]), "coord", text=True, placeholder="e.g. (3,5)",
                          solution=["Coordinates are written (across, up).",
                                    "The %s is at %s." % (objs[k], _coord(*pts[k]))])
        return _num_q("Some objects are drawn on a coordinate plane: %s. Which object is at "
                      "%s? (type the object)" % (listed, _coord(*pts[k])),
                      objs[k], "str", text=True, placeholder="object name",
                      solution=["Read across first, then up.",
                                "The object at %s is the %s."
                                % (_coord(*pts[k]), objs[k])])

    if t == 10:                                       # coordinate map: find the coordinates
        places = random.sample(_PLACES, 3)
        pts = _spread_points(3, size)
        listed = ", ".join("the %s is at %s" % (places[k], _coord(*pts[k]))
                           for k in range(3))
        k = random.randrange(3)
        return _num_q("A coordinate plane is used as a map of a town: %s. Find the "
                      "coordinates of the %s on the map." % (listed, places[k]),
                      _coord(*pts[k]), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["On a map drawn on a coordinate plane, read the across "
                                "number first and the up number second.",
                                "The %s is at %s." % (places[k], _coord(*pts[k]))])

    if t == 11:                                       # coordinate map: count the distance
        a, b = random.sample(_PLACES, 2)
        gap = random.randint(2, size)
        if random.random() < 0.5:                     # same row
            y = random.randint(0, size)
            x1 = random.randint(0, size - gap)
            p1, p2 = (x1, y), (x1 + gap, y)
            why = "Both places have the same y-coordinate, so count along the row."
        else:                                         # same column
            x = random.randint(0, size)
            y1 = random.randint(0, size - gap)
            p1, p2 = (x, y1), (x, y1 + gap)
            why = "Both places have the same x-coordinate, so count up the column."
        return _num_q("On a coordinate plane used as a map, the %s is at %s and the %s is "
                      "at %s. Each square is 1 unit. Count the distance between the two "
                      "places, in units." % (a, _coord(*p1), b, _coord(*p2)),
                      gap, "int", unit="units",
                      solution=[why, "The distance is %d units." % gap])

    # coordinate map: distance in km, or the travel time
    a, b = random.sample(_PLACES, 2)
    gap = random.randint(2, size)
    per = pick(_by_d(d, [2, 5], [2, 3, 5, 10], [3, 4, 5, 6, 10]))
    if random.random() < 0.5:                         # same row
        y = random.randint(0, size)
        x1 = random.randint(0, size - gap)
        p1, p2 = (x1, y), (x1 + gap, y)
    else:                                             # same column
        x = random.randint(0, size)
        y1 = random.randint(0, size - gap)
        p1, p2 = (x, y1), (x, y1 + gap)
    if random.random() < 0.5:
        return _num_q("On a coordinate plane used as a map, the %s is at %s and the %s is "
                      "at %s. Each square on the map stands for %d km. Find the distance "
                      "between the two places, in km."
                      % (a, _coord(*p1), b, _coord(*p2), per),
                      gap * per, "int", unit="km",
                      solution=["The two places are %d squares apart on the map." % gap,
                                "%d × %d = %d km." % (gap, per, gap * per)])
    return _num_q("On a coordinate plane used as a map, the %s is at %s and the %s is at "
                  "%s. A bus takes %d minutes to travel one square. Find the travel time "
                  "between the two places, in minutes."
                  % (a, _coord(*p1), b, _coord(*p2), per),
                  gap * per, "int", unit="minutes",
                  solution=["The distance between the two places is %d squares." % gap,
                            "%d × %d = %d minutes." % (gap, per, gap * per)])


@skill("Y4.8.i", "Translations", S8)
def _(d=1):
    d = _tier(d)
    size = _grid_size(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 2])

    if t == 0:                                        # plot the image of a point
        x, y = random.randint(0, size - 2), random.randint(0, size - 2)
        dx = random.randint(1, size - x)
        dy = random.randint(1, size - y)
        return {"prompt": "The point %s is translated %s right and %s up. "
                          "Plot where the point lands."
                          % (_coord(x, y), _pl(dx, "square"), _pl(dy, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["Add %d to the x-coordinate and %d to the y-coordinate."
                             % (dx, dy),
                             "%d + %d = %d and %d + %d = %d, so the image is %s."
                             % (x, dx, x + dx, y, dy, y + dy, _coord(x + dx, y + dy))]}

    if t == 1:                                        # plot after left / down
        x = random.randint(2, size)
        y = random.randint(2, size)
        dx = random.randint(1, x)
        dy = random.randint(1, y)
        return {"prompt": "The point %s is translated %s left and %s down. "
                          "Plot where the point lands."
                          % (_coord(x, y), _pl(dx, "square"), _pl(dy, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x - dx, y - dy), "answer_type": "coord",
                "solution": ["Subtract %d from the x-coordinate and %d from the "
                             "y-coordinate." % (dx, dy),
                             "The image is %s." % _coord(x - dx, y - dy)]}

    if t == 2:                                        # typed image coordinates
        x, y = random.randint(0, size - 2), random.randint(0, size - 2)
        dx = random.randint(1, size - x)
        dy = random.randint(1, size - y)
        return _num_q("A counter at %s is moved %s to the right and %s up. Write the "
                      "coordinates of its new position."
                      % (_coord(x, y), _pl(dx, "square"), _pl(dy, "square")),
                      _coord(x + dx, y + dy), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["%d + %d = %d across and %d + %d = %d up."
                                % (x, dx, x + dx, y, dy, y + dy),
                                "The new position is %s." % _coord(x + dx, y + dy)])

    if t == 3:                                        # describe: how many right
        x, y = random.randint(0, size - 2), random.randint(0, size - 2)
        dx = random.randint(1, size - x)
        dy = random.randint(1, size - y)
        ask_x = random.random() < 0.5
        return _num_q("A shape is translated so that its corner moves from %s to %s. "
                      "How many squares does it move %s?"
                      % (_coord(x, y), _coord(x + dx, y + dy),
                         "to the right" if ask_x else "up"),
                      dx if ask_x else dy, "int", unit="squares",
                      solution=["%d − %d = %d across." % (x + dx, x, dx) if ask_x else
                                "%d − %d = %d up." % (y + dy, y, dy),
                                "So it moves %s %s." % (_pl(dx if ask_x else dy, "square"),
                                                        "right" if ask_x else "up")])

    if t == 4:                                        # inverse translation
        dx = random.randint(1, size - 1)
        dy = random.randint(1, size - 1)
        ask_x = random.random() < 0.5
        return _num_q("A shape is translated %s right and %s up. To move it straight back "
                      "to where it started, how many squares must it move %s?"
                      % (_pl(dx, "square"), _pl(dy, "square"),
                         "left" if ask_x else "down"),
                      dx if ask_x else dy, "int", unit="squares",
                      solution=["To undo a translation, move back the same amount the "
                                "other way.",
                                "So move %s %s." % (_pl(dx if ask_x else dy, "square"),
                                                    "left" if ask_x else "down")])

    if t == 5:                                        # two-step translation
        x, y = random.randint(0, 2), random.randint(0, 2)
        a = random.randint(1, 3)
        b = random.randint(1, 3)
        return _num_q("A counter starts at %s. It is translated %s right, then %s right "
                      "again. Write the coordinates of its final position."
                      % (_coord(x, y), _pl(a, "square"), _pl(b, "square")),
                      _coord(x + a + b, y), "coord", text=True, placeholder="e.g. (3,5)",
                      solution=["%d + %d = %s right altogether." % (a, b, _pl(a + b, "square")),
                                "The counter finishes at %s." % _coord(x + a + b, y)])

    if t == 6:                                        # translation keeps the shape
        nm, sd = pick(_by_d(d, _POLY[:4], _POLY[:6], _POLY))
        ask = pick(["sides", "size"])
        if ask == "sides":
            return _num_q("%s is translated 5 squares right and 3 squares down. "
                          "How many sides does the translated shape have?"
                          % _a(nm).capitalize(),
                          sd, "int", unit="sides",
                          solution=["A translation slides a shape without turning it or "
                                    "changing its size.",
                                    "So it still has %d sides." % sd])
        s = random.randint(2, 9)
        return _num_q("A square with sides of %d cm is translated 4 squares up. "
                      "What is the length of each side of the translated square, in cm?" % s,
                      s, "int", unit="cm",
                      solution=["A translation does not change the size of a shape.",
                                "Each side is still %d cm." % s])

    if t == 7:                                        # word problem on a grid
        who = pick(NAMES)
        x, y = random.randint(0, size - 3), random.randint(0, size - 3)
        dx, dy = random.randint(1, 3), random.randint(1, 3)
        return {"prompt": "%s moves a game piece from %s by translating it %s right and "
                          "%s up. Plot the square the piece ends on."
                          % (who, _coord(x, y), _pl(dx, "square"), _pl(dy, "square")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": size},
                "answer": _coord(x + dx, y + dy), "answer_type": "coord",
                "solution": ["Right changes the x-coordinate, up changes the y-coordinate.",
                             "The piece ends at %s." % _coord(x + dx, y + dy)]}

    if t == 8:                                # translation: where does another corner land?
        w = random.randint(1, 3)
        x, y = random.randint(0, size - 4), random.randint(0, size - 4)
        dx, dy = random.randint(1, 3), random.randint(1, 3)
        return _num_q("A square has corners at %s and %s (and two more). The square is "
                      "translated %s right and %s up. Write the new coordinates of the "
                      "corner that was at %s."
                      % (_coord(x, y), _coord(x + w, y), _pl(dx, "square"),
                         _pl(dy, "square"), _coord(x + w, y)),
                      _coord(x + w + dx, y + dy), "coord", text=True,
                      placeholder="e.g. (3,5)",
                      solution=["Every corner moves the same way: %d right and %d up."
                                % (dx, dy),
                                "%s moves to %s." % (_coord(x + w, y),
                                                     _coord(x + w + dx, y + dy))])

    # name the transformation: reflection, rotation or translation
    ask = "Is this a reflection, a rotation or a translation? (type the word)"
    kind = pick(["reflection", "rotation", "translation"])
    if kind == "translation":
        dx, dy = random.randint(1, size - 1), random.randint(1, size - 1)
        x, y = random.randint(0, size - dx), random.randint(0, size - dy)
        if random.random() < 0.5:
            body = ("Every point of a shape moves %s to the right and %s up, and the shape "
                    "is not turned or flipped over."
                    % (_pl(dx, "square"), _pl(dy, "square")))
        else:
            body = ("A corner of a shape moves from %s to %s, and every other point of the "
                    "shape moves %s right and %s up as well."
                    % (_coord(x, y), _coord(x + dx, y + dy), _pl(dx, "square"),
                       _pl(dy, "square")))
        return _num_q("%s %s" % (body, ask), "translation", "str", text=True,
                      placeholder="reflection / rotation / translation",
                      solution=["A translation slides every point the same distance in the "
                                "same direction, with no turning and no flipping.",
                                "So this is a translation."])
    if kind == "reflection":
        m = random.randint(2, size - 2)
        gap = random.randint(1, min(m, size - m))
        y = random.randint(0, size)
        if random.random() < 0.5:
            body = ("A shape is flipped over a mirror line, so each point lands the same "
                    "distance on the other side of the line.")
        else:
            body = ("A point at %s is mapped to %s by flipping it over the mirror line "
                    "x = %d." % (_coord(m - gap, y), _coord(m + gap, y), m))
        return _num_q("%s %s" % (body, ask), "reflection", "str", text=True,
                      placeholder="reflection / rotation / translation",
                      solution=["Flipping a shape over a mirror line is a reflection.",
                                "So this is a reflection."])
    turn, deg = pick([("a quarter turn", 90), ("a half turn", 180),
                      ("a three-quarter turn", 270)])
    body = ("A shape is turned %s (%d degrees) about a point, and it is not flipped over "
            "and does not slide." % (turn, deg))
    return _num_q("%s %s" % (body, ask), "rotation", "str", text=True,
                  placeholder="reflection / rotation / translation",
                  solution=["Turning a shape about a point is a rotation.",
                            "So this is a rotation."])


@skill("Y4.8.j", "Perimeter of rectilinear shapes", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1])

    if t == 9:                                        # visual: notch in the top edge
        R, C = random.randint(3, _by_d(d, 4, 6, 8)), random.randint(5, _by_d(d, 6, 8, 9))
        h, w = random.randint(1, R - 1), random.randint(1, C - 4)
        a = random.randint(1, C - 1 - w)
        cells = _notch_cells(R, C, h, a, w)
        return {"prompt": "Find the perimeter of this shape. Count the unit sides all the way round the edge.",
                "component": "area_grid", "spec": {"mode": "read_perimeter", "cells": cells},
                "answer": _perim(cells), "answer_type": "int",
                "solution": ["Without the notch the rectangle would have a perimeter of %d units." % (2 * (R + C)),
                             "The notch adds its two inside edges of %d units each: %d + %d = %d units."
                             % (h, 2 * (R + C), 2 * h, _perim(cells))]}

    if t == 10:                                       # visual: staircase
        R = random.randint(2, _by_d(d, 3, 4, 5))
        C = random.randint(R + 1, R + _by_d(d, 2, 3, 4))
        cells = _stair_cells(R, C)
        return {"prompt": "Find the perimeter of this staircase shape, in units.",
                "component": "area_grid", "spec": {"mode": "read_perimeter", "cells": cells},
                "answer": _perim(cells), "answer_type": "int",
                "solution": ["The steps add up to the same as the outside rectangle: %d across and %d up." % (C, R),
                             "%d + %d + %d + %d = %d units." % (C, R, C, R, 2 * (R + C))]}

    if t == 11:                                       # regular polygons
        name, n = pick([("equilateral triangle", 3), ("regular pentagon", 5), ("regular hexagon", 6), ("regular octagon", 8)])
        side = random.randint(2, _by_d(d, 10, 15, 25))
        if random.random() < 0.5:
            return _num_q("A %s has sides of %d cm. What is its perimeter?" % (name, side), n * side, "int", unit="cm",
                          solution=["All %d sides are the same length." % n, "%d × %d = %d cm." % (n, side, n * side)])
        return _num_q("A %s has a perimeter of %d cm. How long is each side?" % (name, n * side), side, "int", unit="cm",
                      solution=["All %d sides are equal." % n, "%d ÷ %d = %d cm." % (n * side, n, side)])

    if t == 12:                                       # mixed units
        m = random.randint(1, 3)
        cm = random.randint(2, 9) * 10
        return _num_q("A rectangle is %d m long and %d cm wide. What is its perimeter, in centimetres?" % (m, cm),
                      2 * (100 * m + cm), "int", unit="cm",
                      solution=["%d m = %d cm." % (m, 100 * m),
                                "%d + %d + %d + %d = %d cm." % (100 * m, cm, 100 * m, cm, 2 * (100 * m + cm))])

    if t == 0:                                        # visual: rectangle on a grid
        rows = random.randint(2, _by_d(d, 4, 6, 8))
        cols = random.randint(2, _by_d(d, 5, 7, 9))
        return {"prompt": "Find the perimeter of this rectilinear shape. Count the unit "
                          "sides all the way round the edge.",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "rows": rows, "cols": cols},
                "answer": 2 * (rows + cols), "answer_type": "int",
                "solution": ["The shape is %d squares by %d squares." % (rows, cols),
                             "%d + %d + %d + %d = %d units."
                             % (cols, rows, cols, rows, 2 * (rows + cols))]}

    if t == 1:                                        # visual: L-shape on a grid
        R = random.randint(3, _by_d(d, 4, 6, 8))
        C = random.randint(3, _by_d(d, 5, 7, 9))
        r = random.randint(1, R - 2)
        c = random.randint(1, C - 2)
        return {"prompt": "Find the perimeter of this rectilinear shape. Count the unit "
                          "sides all the way round the edge.",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "cells": _L_cells(R, C, r, c)},
                "answer": 2 * (R + C), "answer_type": "int",
                "solution": ["The shape fits inside a rectangle %d squares by %d squares."
                             % (R, C),
                             "The steps in the edge do not change the distance round: "
                             "%d + %d + %d + %d = %d units." % (C, R, C, R, 2 * (R + C))]}

    if t == 2:                                        # bare rectangle perimeter
        w = random.randint(2, _by_d(d, 12, 25, 60))
        h = random.randint(2, _by_d(d, 12, 25, 60))
        w, h = max(w, h), min(w, h)
        return _num_q("A rectangle is %d cm long and %d cm wide. What is its perimeter?"
                      % (w, h),
                      2 * (w + h), "int", unit="cm",
                      solution=["Perimeter = %d + %d + %d + %d." % (w, h, w, h),
                                "That is %d cm." % (2 * (w + h))])

    if t == 3:                                        # missing side of a rectangle
        w = random.randint(2, _by_d(d, 10, 20, 40))
        h = random.randint(2, _by_d(d, 10, 20, 40))
        p = 2 * (w + h)
        return _num_q("A rectangle has a perimeter of %d cm. One side is %d cm. "
                      "How long is the side next to it?" % (p, w),
                      h, "int", unit="cm",
                      solution=["Half the perimeter is one long side plus one short side: "
                                "%d ÷ 2 = %d cm." % (p, p // 2),
                                "%d − %d = %d cm." % (p // 2, w, h)])

    if t == 4:                                        # square: side from perimeter
        s = random.randint(2, _by_d(d, 10, 20, 40))
        ask_side = random.random() < 0.5
        if ask_side:
            return _num_q("A square has a perimeter of %d cm. How long is each side?" % (4 * s),
                          s, "int", unit="cm",
                          solution=["A square has 4 equal sides.",
                                    "%d ÷ 4 = %d cm." % (4 * s, s)])
        return _num_q("A square has sides of %d cm. What is its perimeter?" % s,
                      4 * s, "int", unit="cm",
                      solution=["4 × %d = %d cm." % (s, 4 * s)])

    if t == 5:                                        # missing side of a rectilinear shape
        W = random.randint(6, _by_d(d, 10, 16, 24))
        w = random.randint(2, W - 2)
        return _num_q("A rectilinear shape has one long bottom edge of %d cm. Its top is "
                      "made of two horizontal edges: one is %d cm. How long is the other "
                      "horizontal edge along the top?" % (W, W - w),
                      w, "int", unit="cm",
                      solution=["The two top edges together must match the bottom edge.",
                                "%d − %d = %d cm." % (W, W - w, w)])

    if t == 6:                                        # L-shape perimeter from lengths
        W = random.randint(5, _by_d(d, 9, 14, 20))
        H = random.randint(4, _by_d(d, 8, 12, 18))
        w = random.randint(1, W - 2)
        h = random.randint(1, H - 2)
        if H > W:
            W, H, w, h = H, W, h, w
        return _num_q("An L-shaped room fits exactly inside a rectangle %d m long and %d m "
                      "wide, with a smaller %d m by %d m rectangle cut out of one corner. "
                      "What is the perimeter of the L-shaped room, in metres?"
                      % (W, H, w, h),
                      2 * (W + H), "int", unit="m",
                      solution=["Cutting a rectangle out of a corner does not change the "
                                "distance all the way round.",
                                "Perimeter = %d + %d + %d + %d = %d m."
                                % (W, H, W, H, 2 * (W + H))])

    if t == 7:                                        # word problem: fencing
        who = pick(NAMES)
        w = random.randint(3, _by_d(d, 10, 18, 30))
        h = random.randint(3, _by_d(d, 10, 18, 30))
        per_m = pick([2, 3, 4, 5])
        p = 2 * (w + h)
        ask_cost = random.random() < 0.5
        if ask_cost:
            return _num_q("%s fences a rectangular garden %d m by %d m. Fencing costs £%d "
                          "for each metre. How much does the fencing cost, in pounds?"
                          % (who, w, h, per_m),
                          p * per_m, "int", unit="pounds",
                          solution=["Perimeter = 2 × (%d + %d) = %d m." % (w, h, p),
                                    "%d × £%d = £%d." % (p, per_m, p * per_m)])
        return _num_q("%s walks once all the way round a rectangular field %d m by %d m. "
                      "How far does %s walk, in metres?" % (who, w, h, who),
                      p, "int", unit="m",
                      solution=["Perimeter = %d + %d + %d + %d." % (w, h, w, h),
                                "That is %d m." % p])

    # comparison of two perimeters
    w1, h1 = random.randint(3, 15), random.randint(3, 15)
    w2, h2 = random.randint(3, 15), random.randint(3, 15)
    p1, p2 = 2 * (w1 + h1), 2 * (w2 + h2)
    while p1 == p2:
        w2, h2 = random.randint(3, 15), random.randint(3, 15)
        p2 = 2 * (w2 + h2)
    return _num_q("Rectangle A is %d cm by %d cm and rectangle B is %d cm by %d cm. "
                  "How many centimetres BIGGER is the larger perimeter?"
                  % (w1, h1, w2, h2),
                  abs(p1 - p2), "int", unit="cm",
                  solution=["Perimeter of A = %d cm and perimeter of B = %d cm." % (p1, p2),
                            "%d − %d = %d cm." % (max(p1, p2), min(p1, p2), abs(p1 - p2))])


@skill("Y4.8.k", "Area by counting squares", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1])

    if t == 12:                                       # visual: notch in the top edge
        R, C = random.randint(3, _by_d(d, 4, 6, 8)), random.randint(5, _by_d(d, 6, 8, 9))
        h, w = random.randint(1, R - 1), random.randint(1, C - 4)
        a = random.randint(1, C - 1 - w)
        cells = _notch_cells(R, C, h, a, w)
        return {"prompt": "Find the area of this shape by counting the unit squares it covers.",
                "component": "area_grid", "spec": {"mode": "read_area", "cells": cells},
                "answer": len(cells), "answer_type": "int",
                "solution": ["The full rectangle is %d × %d = %d squares." % (R, C, R * C),
                             "The notch removes %d × %d = %d: %d − %d = %d square units." % (h, w, h * w, R * C, h * w, len(cells))]}

    if t == 13:                                       # visual: staircase
        R = random.randint(2, _by_d(d, 3, 4, 5))
        C = random.randint(R + 1, R + _by_d(d, 2, 3, 4))
        cells = _stair_cells(R, C)
        rows_txt = " + ".join(str(C - (R - 1 - i)) for i in range(R))
        return {"prompt": "Find the area of this staircase shape by counting squares.",
                "component": "area_grid", "spec": {"mode": "read_area", "cells": cells},
                "answer": len(cells), "answer_type": "int",
                "solution": ["Count each row: %s." % rows_txt, "That is %d square units." % len(cells)]}

    if t == 14:                                       # half the area
        w = random.randint(2, _by_d(d, 6, 8, 10))
        h = 2 * random.randint(1, _by_d(d, 3, 4, 5))
        return _num_q("A rectangle %d squares by %d squares is cut in half along a straight line. What is the area of "
                      "each half, in square units?" % (w, h), w * h // 2, "int", unit="square units",
                      solution=["The whole rectangle is %d × %d = %d square units." % (w, h, w * h),
                                "Half of %d is %d." % (w * h, w * h // 2)])

    if t == 0:                                        # visual: rectangle area
        rows = random.randint(2, _by_d(d, 4, 6, 8))
        cols = random.randint(2, _by_d(d, 5, 7, 9))
        return {"prompt": "Find the area of this shape by counting the unit squares it "
                          "covers.",
                "component": "area_grid",
                "spec": {"mode": "read_area", "rows": rows, "cols": cols},
                "answer": rows * cols, "answer_type": "int",
                "solution": ["The shape is %d rows of %d squares." % (rows, cols),
                             "%d × %d = %d square units." % (rows, cols, rows * cols)]}

    if t == 1:                                        # visual: L-shape area
        R = random.randint(3, _by_d(d, 4, 6, 8))
        C = random.randint(3, _by_d(d, 5, 7, 9))
        r = random.randint(1, R - 2)
        c = random.randint(1, C - 2)
        return {"prompt": "Find the area of this shape by counting the unit squares it "
                          "covers.",
                "component": "area_grid",
                "spec": {"mode": "read_area", "cells": _L_cells(R, C, r, c)},
                "answer": R * C - r * c, "answer_type": "int",
                "solution": ["A full %d by %d rectangle would be %d squares."
                             % (R, C, R * C),
                             "%s %s missing from the corner: %d − %d = %d square "
                             "units." % (_pl(r * c, "square"), "is" if r * c == 1 else "are", R * C, r * c, R * C - r * c)]}

    if t == 2:                                        # build an area
        rows = random.randint(3, 6)
        cols = random.randint(3, 6)
        target = random.randint(3, rows * cols - 1)
        return {"prompt": "Shade squares on the grid to make a shape with an area of "
                          "%d square units." % target,
                "component": "area_grid",
                "spec": {"mode": "build_area", "rows": rows, "cols": cols},
                "answer": target, "answer_type": "int",
                "solution": ["Each shaded square is 1 square unit.",
                             "Shade exactly %d squares." % target]}

    if t == 3:                                        # bare area of a rectangle
        w = random.randint(2, _by_d(d, 8, 12, 20))
        h = random.randint(2, _by_d(d, 8, 12, 20))
        w, h = max(w, h), min(w, h)
        return _num_q("A rectangle is %d squares long and %d squares wide. What is its "
                      "area, in square units?" % (w, h),
                      w * h, "int", unit="square units",
                      solution=["Area = length × width.",
                                "%d × %d = %d square units." % (w, h, w * h)])

    if t == 4:                                        # missing side from area
        w = random.randint(2, _by_d(d, 8, 12, 15))
        h = random.randint(2, _by_d(d, 8, 12, 15))
        return _num_q("A rectangle has an area of %d square units. One side is %d units "
                      "long. How long is the other side?" % (w * h, w),
                      h, "int", unit="units",
                      solution=["Area = length × width, so width = area ÷ length.",
                                "%d ÷ %d = %d units." % (w * h, w, h)])

    if t == 5:                                        # compare two areas
        w1, h1 = random.randint(2, 9), random.randint(2, 9)
        w2, h2 = random.randint(2, 9), random.randint(2, 9)
        while w1 * h1 == w2 * h2:
            w2, h2 = random.randint(2, 9), random.randint(2, 9)
        a1, a2 = w1 * h1, w2 * h2
        return _num_q("Shape A covers %d rows of %d squares. Shape B covers %d rows of %d "
                      "squares. How many MORE squares does the larger shape cover?"
                      % (h1, w1, h2, w2),
                      abs(a1 - a2), "int", unit="squares",
                      solution=["A = %d × %d = %d squares and B = %d × %d = %d squares."
                                % (h1, w1, a1, h2, w2, a2),
                                "%d − %d = %d." % (max(a1, a2), min(a1, a2), abs(a1 - a2))])

    if t == 6:                                        # word problem: tiles
        who = pick(NAMES)
        w = random.randint(3, _by_d(d, 6, 10, 15))
        h = random.randint(3, _by_d(d, 6, 10, 15))
        w, h = max(w, h), min(w, h)
        return _num_q("%s covers a rectangular tray %d tiles long and %d tiles wide, with "
                      "no gaps. How many square tiles does %s use?" % (who, w, h, who),
                      w * h, "int", unit="tiles",
                      solution=["%d rows of %d tiles." % (h, w),
                                "%d × %d = %d tiles." % (h, w, w * h)])

    if t == 7:                                        # area of an L-shape by splitting
        a, b = random.randint(2, 8), random.randint(2, 8)
        c, e = random.randint(2, 8), random.randint(2, 8)
        return _num_q("A rectilinear shape is made of two rectangles joined together. One "
                      "is %d squares by %d squares and the other is %d squares by %d "
                      "squares. What is the total area, in square units?" % (a, b, c, e),
                      a * b + c * e, "int", unit="square units",
                      solution=["%d × %d = %d and %d × %d = %d." % (a, b, a * b, c, e, c * e),
                                "%d + %d = %d square units." % (a * b, c * e, a * b + c * e)])

    if t == 8:                                        # area and perimeter contrasted
        w = random.randint(2, _by_d(d, 6, 9, 14))
        h = random.randint(2, _by_d(d, 6, 9, 14))
        ask_area = random.random() < 0.5
        return _num_q("A rectangle is %d squares by %d squares. What is its %s?"
                      % (w, h, "area, in square units" if ask_area
                         else "perimeter, in units"),
                      w * h if ask_area else 2 * (w + h), "int",
                      unit="square units" if ask_area else "units",
                      solution=["Area counts the squares inside; perimeter counts the unit "
                                "sides round the edge.",
                                "%d × %d = %d square units." % (w, h, w * h) if ask_area
                                else "2 × (%d + %d) = %d units." % (w, h, 2 * (w + h))])

    if t == 9:                                        # select the figure with a given area
        mx = _by_d(d, 5, 7, 9)
        figs, seen = [], set()
        while len(figs) < 4:
            w, h = random.randint(2, mx), random.randint(2, mx)
            if w * h in seen:
                continue
            seen.add(w * h)
            figs.append((w, h))
        letters = "ABCD"
        k = random.randrange(4)
        listed = ", ".join("figure %s is %d squares by %d squares"
                           % (letters[i], figs[i][0], figs[i][1]) for i in range(4))
        target = figs[k][0] * figs[k][1]
        return _num_q("Four figures are drawn on squared paper: %s. Select the figure with "
                      "an area of %d square units. Type its letter." % (listed, target),
                      letters[k], "str", text=True, placeholder="A, B, C or D",
                      solution=["Areas: %s."
                                % ", ".join("%s = %d × %d = %d"
                                            % (letters[i], figs[i][0], figs[i][1],
                                               figs[i][0] * figs[i][1]) for i in range(4)),
                                "Figure %s has an area of %d square units."
                                % (letters[k], target)])

    if t == 10:                                       # select two figures with the same area
        mx = _by_d(d, 6, 8, 10)
        pool = []
        for area in range(6, mx * mx + 1):
            pairs = [(w, area // w) for w in range(2, mx + 1)
                     if area % w == 0 and 2 <= area // w <= mx and w <= area // w]
            if len(pairs) >= 2:
                pool.append((area, pairs))
        area, pairs = pick(pool)
        (w1, h1), (w2, h2) = random.sample(pairs, 2)
        figs = [(w1, h1), (w2, h2)]
        seen = {area}
        while len(figs) < 4:
            w, h = random.randint(2, mx), random.randint(2, mx)
            if w * h in seen:
                continue
            seen.add(w * h)
            figs.append((w, h))
        order = list(range(4))
        random.shuffle(order)
        figs = [figs[i] for i in order]
        pos = [i for i in range(4) if order[i] in (0, 1)]
        letters = "ABCD"
        listed = ", ".join("figure %s is %d squares by %d squares"
                           % (letters[i], figs[i][0], figs[i][1]) for i in range(4))
        first, second = letters[pos[0]], letters[pos[1]]
        return _num_q("Four figures are drawn on squared paper: %s. Exactly two of the "
                      "figures have the same area. Select the two figures with the same "
                      "area: one of them is figure %s, so type the letter of the other one."
                      % (listed, first),
                      second, "str", text=True, placeholder="A, B, C or D",
                      solution=["Areas: %s."
                                % ", ".join("%s = %d" % (letters[i],
                                                         figs[i][0] * figs[i][1])
                                            for i in range(4)),
                                "Figures %s and %s both have an area of %d square units."
                                % (first, second, area)])

    # create a figure with a given area
    rows = random.randint(3, _by_d(d, 4, 5, 6))
    cols = random.randint(3, _by_d(d, 4, 5, 6))
    target = random.randint(3, rows * cols - 1)
    return {"prompt": "Create a figure with an area of %d square units: shade exactly that "
                      "many unit squares on the grid." % target,
            "component": "area_grid",
            "spec": {"mode": "build_area", "rows": rows, "cols": cols},
            "answer": target, "answer_type": "int",
            "solution": ["Each shaded square is 1 square unit of area.",
                         "A figure with an area of %d square units needs %d shaded squares."
                         % (target, target)]}


@skill("Y4.8.l", "3-D shapes: faces, edges and vertices", S8)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [s for s in _SOLIDS if s[0] in ("cube", "cuboid")], _SOLIDS,
                 [s for s in _SOLIDS if s[0] != "cube"])     # stretch: the less familiar solids
    name, f, e, v = pick(pool)
    t = _pick_t([2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2])

    if t == 0:                                        # faces (visual)
        return {"prompt": "How many faces does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "faces"},
                "answer": f, "answer_type": "int",
                "solution": ["A face is a flat surface.",
                             "%s has %d faces." % (_a(name).capitalize(), f)]}

    if t == 1:                                        # edges (visual)
        return {"prompt": "How many edges does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "edges"},
                "answer": e, "answer_type": "int",
                "solution": ["An edge is where two faces meet.",
                             "%s has %d edges." % (_a(name).capitalize(), e)]}

    if t == 2:                                        # vertices (visual)
        return {"prompt": "How many vertices (corners) does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "vertices"},
                "answer": v, "answer_type": "int",
                "solution": ["A vertex is a corner where edges meet.",
                             "%s has %d vertices." % (_a(name).capitalize(), v)]}

    if t == 3:                                        # name it (visual)
        nm, ff, ee, vv = pick([s for s in pool if s[0] != "cuboid"] or pool)
        return {"prompt": "What is the name of this solid?",
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["It has %d faces, %d edges and %d vertices." % (ff, ee, vv),
                             "It is %s." % _a(nm)]}

    if t == 4:                                        # riddle
        nm, ff, ee, vv = pick([s for s in _SOLIDS if s[0] != "cuboid"][:2 if d == 0 else 3])
        if d == 2:                                    # stretch: one clue fewer
            extra = ", and every face is a square" if nm == "cube" else ""
            return _num_q("A solid has %d faces and %d vertices%s. What is it called?"
                          % (ff, vv, extra),
                          nm, "str", text=True, placeholder="solid name",
                          solution=["Check the faces and vertices of each solid you know.",
                                    "%d faces and %d vertices%s describe %s."
                                    % (ff, vv, extra, _a(nm))])
        sq = ", and every face is a square" if nm == "cube" else ""     # a cuboid has the same counts
        return _num_q("A solid has %d faces, %d edges and %d vertices%s. What is it called?"
                      % (ff, ee, vv, sq),
                      nm, "str", text=True, placeholder="solid name",
                      solution=["%d faces, %d edges and %d vertices%s describe %s."
                                % (ff, ee, vv, sq, _a(nm))])

    if t == 5:                                        # faces + vertices - edges
        if d == 2:                                    # stretch: compare two solids
            (n1, f1, e1, v1), (n2, f2, e2, v2) = random.sample(_SOLIDS[1:], 2)
            what = pick(["edges", "vertices"])
            a1, a2 = (e1, e2) if what == "edges" else (v1, v2)
            while a1 == a2:
                (n1, f1, e1, v1), (n2, f2, e2, v2) = random.sample(_SOLIDS[1:], 2)
                a1, a2 = (e1, e2) if what == "edges" else (v1, v2)
            if a1 < a2:
                n1, n2, a1, a2 = n2, n1, a2, a1
            return _num_q("How many MORE %s does %s have than %s?" % (what, _a(n1), _a(n2)),
                          a1 - a2, "int", unit=what,
                          solution=["%s has %d %s and %s has %d."
                                    % (_a(n1).capitalize(), a1, what, _a(n2), a2),
                                    "%d − %d = %d." % (a1, a2, a1 - a2)])
        nm, ff, ee, vv = pick(_SOLIDS[:2] if d == 0 else _SOLIDS)
        which = pick(["sum", "diff"])
        if which == "sum":
            return _num_q("How many faces and vertices does %s have altogether?" % _a(nm),
                          ff + vv, "int",
                          solution=["%s has %d faces and %d vertices."
                                    % (_a(nm).capitalize(), ff, vv),
                                    "%d + %d = %d." % (ff, vv, ff + vv)])
        return _num_q("How many MORE edges than faces does %s have?" % _a(nm),
                      ee - ff, "int", unit="edges",
                      solution=["%s has %d edges and %d faces."
                                % (_a(nm).capitalize(), ee, ff),
                                "%d − %d = %d." % (ee, ff, ee - ff)])

    if t == 6:                                        # real world
        things = [("a dice", "cube", 6, 12, 8),
                  ("a cereal box", "cuboid", 6, 12, 8),
                  ("a tent with triangular ends", "triangular prism", 5, 9, 6),
                  ("an Egyptian pyramid", "square-based pyramid", 5, 8, 5),
                  ("a chocolate bar box with triangular ends", "triangular prism", 5, 9, 6)]
        thing, solid, ff, ee, vv = pick(_by_d(d, things[:2], things[:4], things[2:]))
        ask = pick(["faces", "edges", "vertices", "name"])
        if ask == "name":
            return _num_q("In the real world, %s is shaped like which solid? "
                          "(type the name)" % thing,
                          solid, "str", text=True, placeholder="solid name",
                          solution=["%s is shaped like %s." % (thing.capitalize(), _a(solid))])
        val = {"faces": ff, "edges": ee, "vertices": vv}[ask]
        return _num_q("In the real world, %s is shaped like %s. How many %s does it have?"
                      % (thing, _a(solid), ask),
                      val, "int", unit=ask,
                      solution=["%s has %d faces, %d edges and %d vertices."
                                % (_a(solid).capitalize(), ff, ee, vv),
                                "So it has %d %s." % (val, ask)])

    if t == 7:                                        # nets and traced faces
        if random.random() < 0.5:
            traces = [("cube", "one face", "square"),
                      ("cuboid", "the flat base", "rectangle"),
                      ("cylinder", "one flat end", "circle"),
                      ("square-based pyramid", "the base", "square"),
                      ("triangular prism", "one end face", "triangle"),
                      ("cone", "the flat end", "circle"),
                      ("square-based pyramid", "one sloping face", "triangle"),
                      ("triangular prism", "one long side face", "rectangle")]
            solid, part, traced = pick(_by_d(d, traces[:3], traces[:6],
                                             traces[3:]))   # stretch: less familiar faces
            return _num_q("A pencil is drawn round %s of %s to trace it onto paper. Which "
                          "2-D shape is traced? (type the shape)" % (part, _a(solid)),
                          traced, "str", text=True, placeholder="shape name",
                          solution=["%s of %s is %s."
                                    % (part.capitalize(), _a(solid), _a(traced))])
        solid, faces, face_shape = pick(_by_d(d, [("cube", 6, "square")],
                                              [("cube", 6, "square"),
                                               ("square-based pyramid", 4, "triangle")],
                                              [("square-based pyramid", 4, "triangle"),
                                               ("triangular prism", 3, "rectangle"),
                                               ("triangular prism", 2, "triangle")]))
        if solid == "triangular prism":               # stretch: a net with two kinds of face
            return _num_q("A net of a triangular prism is cut out and folded up. It has "
                          "rectangles and triangles. How many %ss does the net need?"
                          % face_shape,
                          faces, "int", unit=face_shape + "s",
                          solution=["A triangular prism has 5 faces: 2 triangular ends and "
                                    "3 rectangles joining them.",
                                    "So the net needs %d %ss." % (faces, face_shape)])
        if solid == "cube":
            return _num_q("A net of a cube is cut out and folded up. How many squares does "
                          "the net need?",
                          6, "int", unit="squares",
                          solution=["A cube has 6 faces and every face is a square.",
                                    "So the net needs 6 squares."])
        return _num_q("A net of a square-based pyramid is cut out and folded up. It has "
                      "one square base and some triangles. How many triangles does the net "
                      "need?",
                      4, "int", unit="triangles",
                      solution=["A square-based pyramid has 5 faces: 1 square and the rest "
                                "triangles.",
                                "5 − 1 = 4 triangles."])

    if t == 8:                                        # sorting solids
        chosen = random.sample(_SOLIDS, _by_d(d, 2, 3, 4))
        if d == 2:                                    # stretch: sort by edges or vertices
            what, k = pick([("vertices", 3), ("edges", 2)])
            cut = pick([6, 8] if what == "vertices" else [9, 12])
            cnt = sum(1 for s in chosen if s[k] == cut)
            return _num_q("Sort these solids into two groups: those with %d %s and those "
                          "without. Solids: %s. How many of them have %d %s?"
                          % (cut, what, ", ".join(s[0] for s in chosen), cut, what),
                          cnt, "int", unit="solids",
                          solution=["%s: %s." % (what.capitalize(),
                                                 ", ".join("%s %d" % (s[0], s[k]) for s in chosen)),
                                    "%d of them have %d %s." % (cnt, cut, what)])
        cnt = sum(1 for s in chosen if s[1] == 6)
        return _num_q("Sort these solids into two groups: those with 6 faces and those "
                      "without. Solids: %s. How many of them have 6 faces?"
                      % ", ".join(s[0] for s in chosen),
                      cnt, "int", unit="solids",
                      solution=["Faces: %s."
                                % ", ".join("%s %d" % (s[0], s[1]) for s in chosen),
                                "%d of them have 6 faces." % cnt])

    if t == 9:                                        # identify objects with volume
        n_solid = random.randint(*_by_d(d, (1, 2), (2, 3), (3, 5)))
        n_flat = random.randint(*_by_d(d, (1, 1), (1, 2), (2, 4)))
        solids = random.sample(_HAS_VOLUME, n_solid)
        flats = random.sample(_NO_VOLUME, n_flat)
        items = solids + flats
        random.shuffle(items)
        return _num_q("A solid object takes up space, so it has volume. A flat object drawn "
                      "on a surface does not. Identify the objects with volume in this "
                      "list: %s. How many of the objects have volume?"
                      % ", ".join(items),
                      n_solid, "int", unit="objects",
                      solution=["These objects take up space, so they have volume: %s."
                                % ", ".join(solids),
                                "That is %d of the objects." % n_solid])

    if t == 10:                                       # volume of cuboids made of unit cubes
        mx = _by_d(d, 4, 5, 6)
        L, W, H = (random.randint(2, mx), random.randint(2, mx), random.randint(2, mx))
        style = random.randrange(3)
        if style == 0:
            return _num_q("A cuboid is made of unit cubes. It is %d cubes long, %d cubes "
                          "wide and %d cubes high. What is the volume of the cuboid, in "
                          "unit cubes?" % (L, W, H),
                          L * W * H, "int", unit="unit cubes",
                          solution=["Each layer holds %d × %d = %d unit cubes."
                                    % (L, W, L * W),
                                    "There are %d layers: %d × %d = %d unit cubes."
                                    % (H, L * W, H, L * W * H)])
        if style == 1:
            return _num_q("A cuboid made of unit cubes has %d layers. Each layer is a "
                          "rectangle of %d cubes by %d cubes. What is the volume of the "
                          "cuboid, in unit cubes?" % (H, L, W),
                          L * W * H, "int", unit="unit cubes",
                          solution=["One layer is %d × %d = %d unit cubes." % (L, W, L * W),
                                    "%d layers: %d × %d = %d unit cubes."
                                    % (H, L * W, H, L * W * H)])
        return _num_q("A cuboid made of unit cubes has a volume of %d unit cubes. It is %d "
                      "cubes long and %d cubes wide. How many cubes high is it?"
                      % (L * W * H, L, W),
                      H, "int", unit="cubes",
                      solution=["Each layer is %d × %d = %d unit cubes." % (L, W, L * W),
                                "%d ÷ %d = %d layers." % (L * W * H, L * W, H)])

    # identify three-dimensional shapes
    nm, ff, ee, vv = pick([s for s in pool if s[0] != "cuboid"] or pool)
    if random.random() < 0.5:
        return {"prompt": "Identify this three-dimensional shape. Type its name.",
                "component": "shape", "spec": {"kind": "3d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["Count the faces, edges and vertices: %d faces, %d edges and "
                             "%d vertices." % (ff, ee, vv),
                             "This three-dimensional shape is %s." % _a(nm)]}
    nm2, ff2, ee2, vv2 = pick([s for s in _SOLIDS if s[0] != "cuboid"])
    if d == 2:                                        # stretch: edges and vertices only
        extra = ", and every face is a square" if nm2 == "cube" else ""
        return _num_q("Identify the three-dimensional shape that has %d edges and %d "
                      "vertices%s. Type its name." % (ee2, vv2, extra),
                      nm2, "str", text=True, placeholder="shape name",
                      solution=["Check the edges and vertices of each solid you know.",
                                "A three-dimensional shape with %d edges and %d vertices%s "
                                "is %s." % (ee2, vv2, extra, _a(nm2))])
    sq2 = ", and every face is a square" if nm2 == "cube" else ""   # a cuboid has the same counts
    return _num_q("Identify the three-dimensional shape that has %d flat faces, %d edges "
                  "and %d vertices%s. Type its name." % (ff2, ee2, vv2, sq2),
                  nm2, "str", text=True, placeholder="shape name",
                  solution=["A three-dimensional shape with %d faces, %d edges and %d "
                            "vertices%s is %s." % (ff2, ee2, vv2, sq2, _a(nm2))])


# ================================================================== 4.9 ======
_TALLY_TOPICS = [
    ("Favourite fruit", "Fruit", ["Apple", "Banana", "Pear", "Orange", "Grapes"], "children"),
    ("Birds seen in the garden", "Bird", ["Robin", "Sparrow", "Magpie", "Blackbird", "Pigeon"], "birds"),
    ("Cars in the car park", "Colour", ["Red", "Blue", "White", "Black", "Silver"], "cars"),
    ("Favourite sport", "Sport", ["Football", "Netball", "Swimming", "Cricket", "Tennis"], "children"),
    ("Books borrowed", "Type", ["Comic", "Poetry", "Adventure", "Science", "History"], "books"),
]


@skill("Y4.9.a", "Tally charts and frequency tables", S9)
def _(d=1):
    d = _tier(d)
    title, col, items, unit = pick(_TALLY_TOPICS)
    n = _by_d(d, 3, 4, 5)
    cats = items[:n]
    lo, hi = _by_d(d, (2, 12), (3, 19), (4, 28))
    vals = _distinct(n, lo, hi)
    rows = [[c, _tally(v), str(v)] for c, v in zip(cats, vals)]
    headers = [col, "Tally", "Frequency"]
    i, j = random.sample(range(n), 2)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 2])

    if t == 0:                                        # missing frequency from the tally
        blank = [[c, ty, ("" if k == i else fr)] for k, (c, ty, fr) in enumerate(rows)]
        return {"prompt": "Read the tally chart. What number goes in the empty Frequency "
                          "box for %s?" % cats[i],
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": blank,
                         "missing": [i, 2]},
                "answer": vals[i], "answer_type": "int",
                "solution": ["Each bundle %s stands for 5." % _GATE,
                             "%s has %d." % (cats[i], vals[i])]}

    if t == 1:                                        # read one frequency
        return {"prompt": "Use the frequency table. How many %s are recorded for %s?"
                          % (unit, cats[i]),
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": vals[i], "answer_type": "int",
                "solution": ["Find the %s row and read the Frequency column." % cats[i],
                             "It shows %d." % vals[i]]}

    if t == 2:                                        # total
        return {"prompt": "Use the frequency table. How many %s were recorded altogether?"
                          % unit,
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(v) for v in vals), sum(vals))]}

    if t == 3:                                        # difference
        big = cats[i] if vals[i] > vals[j] else cats[j]
        small = cats[j] if vals[i] > vals[j] else cats[i]
        return {"prompt": "Use the frequency table. How many MORE were recorded for %s "
                          "than for %s?" % (big, small),
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (big, max(vals[i], vals[j]), small, min(vals[i], vals[j])),
                             "%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 4:                                        # most common (typed)
        top = cats[vals.index(max(vals))]
        return {"prompt": "Use the frequency table. Which row has the highest frequency? "
                          "(type the name)",
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": top, "answer_type": "str",
                "solution": ["The largest frequency is %d." % max(vals),
                             "That is %s." % top]}

    if t == 5:                                        # least common (typed)
        bot = cats[vals.index(min(vals))]
        return {"prompt": "Use the frequency table. Which row has the lowest frequency? "
                          "(type the name)",
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": bot, "answer_type": "str",
                "solution": ["The smallest frequency is %d." % min(vals),
                             "That is %s." % bot]}

    if t == 6:                                        # bundles of five (no component)
        v = vals[i]
        return _num_q("A tally chart records %d %s. Tally marks are drawn in bundles of "
                      "five. How many complete bundles of five are drawn?" % (v, unit),
                      v // 5, "int", unit="bundles",
                      solution=["%d ÷ 5 = %d remainder %d." % (v, v // 5, v % 5),
                                "So there are %s of five." % _pl(v // 5, "complete bundle")])

    if t == 7:                                        # tally -> number, typed
        v = random.randint(6, _by_d(d, 14, 24, 39))
        return _num_q("A tally chart shows this tally for %s:   %s   "
                      "What number does it stand for?" % (cats[i], _tally(v)),
                      v, "int",
                      solution=["Each bundle %s stands for 5 and each single mark for 1." % _GATE,
                                "%s and %s make %d."
                                % (_pl(v // 5, "bundle"), _pl(v % 5, "extra mark"), v)])

    # two-step: total of two rows
    return {"prompt": "Use the frequency table. How many %s were recorded for %s and %s "
                      "altogether?" % (unit, cats[i], cats[j]),
            "component": "data_table",
            "spec": {"caption": title, "headers": headers, "rows": rows},
            "answer": vals[i] + vals[j], "answer_type": "int",
            "solution": ["%s = %d and %s = %d." % (cats[i], vals[i], cats[j], vals[j]),
                         "%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}


@skill("Y4.9.b", "Pictograms", S9)
def _(d=1):
    d = _tier(d)
    key = pick(_by_d(d, [2, 5], [2, 5, 10], [4, 5, 10, 20]))
    symbol = pick(["circle", "star", "apple"])
    cats = random.sample(["Apples", "Pears", "Plums", "Oranges", "Bananas"], 4)
    mults = _distinct(4, 1, 8)
    vals = [key * m for m in mults]
    spec = {"categories": cats, "values": vals, "key": key, "symbol": symbol}
    i, j = random.sample(range(4), 2)
    t = _pick_t([2, 2, 2, 2, 2, 1, 1, 1, 1])

    if t == 0:                                        # read one row
        return {"prompt": "Use the pictogram. How many %s are there?" % cats[i].lower(),
                "component": "pictogram", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["Each symbol stands for %d." % key,
                             "%s × %d = %d." % (_pl(vals[i] // key, "symbol"), key, vals[i])]}

    if t == 1:                                        # count symbols
        return {"prompt": "Use the pictogram. How many symbols are drawn in the %s row?"
                          % cats[i].lower(),
                "component": "pictogram", "spec": spec,
                "answer": vals[i] // key, "answer_type": "int",
                "solution": ["%s is %d and each symbol stands for %d."
                             % (cats[i], vals[i], key),
                             "%d ÷ %d = %s." % (vals[i], key, _pl(vals[i] // key, "symbol"))]}

    if t == 2:                                        # total of two rows
        return {"prompt": "Use the pictogram. How many %s and %s are there altogether?"
                          % (cats[i].lower(), cats[j].lower()),
                "component": "pictogram", "spec": spec,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%s = %d and %s = %d." % (cats[i], vals[i], cats[j], vals[j]),
                             "%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    if t == 3:                                        # difference
        big = cats[i] if vals[i] > vals[j] else cats[j]
        small = cats[j] if vals[i] > vals[j] else cats[i]
        return {"prompt": "Use the pictogram. How many MORE %s than %s are there?"
                          % (big.lower(), small.lower()),
                "component": "pictogram", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (big, max(vals[i], vals[j]), small, min(vals[i], vals[j])),
                             "%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 4:                                        # grand total
        return {"prompt": "Use the pictogram. How many pieces of fruit are there in total?",
                "component": "pictogram", "spec": spec,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s." % " + ".join(str(v) for v in vals),
                             "The total is %d." % sum(vals)]}

    if t == 5:                                        # most / fewest (typed)
        want_most = random.random() < 0.5
        which = cats[vals.index(max(vals) if want_most else min(vals))]
        return {"prompt": "Use the pictogram. Which fruit has the %s? (type the name)"
                          % ("longest row" if want_most else "shortest row"),
                "component": "pictogram", "spec": spec,
                "answer": which, "answer_type": "str",
                "solution": ["The %s row is %s with %d."
                             % ("longest" if want_most else "shortest", which,
                                max(vals) if want_most else min(vals))]}

    if t == 6:                                        # create a pictogram
        k = random.randrange(4)
        return _num_q("You are drawing a pictogram where one symbol stands for %d. There "
                      "are %d %s. How many symbols would you draw in that row?"
                      % (key, vals[k], cats[k].lower()),
                      vals[k] // key, "int", unit="symbols",
                      solution=["%d ÷ %d = %d." % (vals[k], key, vals[k] // key),
                                "Draw %s." % _pl(vals[k] // key, "symbol")])

    if t == 7:                                        # symbols -> value
        k = random.randrange(4)
        return _num_q("In a pictogram, one symbol stands for %d. %s draws %s in the %s row. "
                      "How many %s does that stand for?"
                      % (key, pick(NAMES), _pl(vals[k] // key, "symbol"),
                         cats[k].lower(), cats[k].lower()),
                      vals[k], "int", unit=cats[k].lower(),
                      solution=["%s × %d = %d." % (_pl(vals[k] // key, "symbol"), key, vals[k])])

    # two-step from the pictogram
    give = random.randint(1, min(vals) - 1) if min(vals) > 1 else 1
    return {"prompt": "Use the pictogram. %d of the %s %s given away. How many %s are "
                      "left?" % (give, cats[i].lower(), "is" if give == 1 else "are",
                                 cats[i].lower()),
            "component": "pictogram", "spec": spec,
            "answer": vals[i] - give, "answer_type": "int",
            "solution": ["The pictogram shows %d %s." % (vals[i], cats[i].lower()),
                         "%d − %d = %d." % (vals[i], give, vals[i] - give)]}


_GROUPS = [("0–4", "5–9", "10–14", "15–19"), ("1–5", "6–10", "11–15", "16–20")]


@skill("Y4.9.c", "Bar charts, including grouped data", S9)
def _(d=1):
    d = _tier(d)
    grouped = random.random() < 0.45
    if grouped:
        cats = list(pick(_GROUPS))
        lo, hi = _by_d(d, (2, 9), (3, 14), (4, 20))
        vals = _distinct(4, lo, hi)
        what, unit = pick([("children", "children"), ("scores", "scores")])
    else:
        cats, vals = _chart(d, 4)
        what, unit = "votes", "votes"
    spec = {"categories": cats, "values": vals, "mode": "read"}
    i, j = random.sample(range(4), 2)
    t = _pick_t([2, 1, 1, 1, 1, 1, 1, 1, 1, 2])

    if t == 0:                                        # read one bar
        return {"prompt": "Use the bar chart. How many %s are shown for %s?"
                          % (unit, cats[i]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["The %s bar reaches %d." % (cats[i], vals[i])]}

    if t == 1:                                        # tallest bar
        top = cats[vals.index(max(vals))]
        return {"prompt": "Use the bar chart. Which bar is the TALLEST? (type its label)",
                "component": "bar_chart", "spec": spec,
                "answer": top, "answer_type": "str",
                "solution": ["The tallest bar is %s with %d." % (top, max(vals))]}

    if t == 2:                                        # shortest bar
        bot = cats[vals.index(min(vals))]
        return {"prompt": "Use the bar chart. Which bar is the SHORTEST? (type its label)",
                "component": "bar_chart", "spec": spec,
                "answer": bot, "answer_type": "str",
                "solution": ["The shortest bar is %s with %d." % (bot, min(vals))]}

    if t == 3:                                        # total
        return {"prompt": "Use the bar chart. What is the total of all four bars?",
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s." % " + ".join(str(v) for v in vals),
                             "The total is %d." % sum(vals)]}

    if t == 4:                                        # difference
        return {"prompt": "Use the bar chart. What is the difference between the %s bar "
                          "and the %s bar?" % (cats[i], cats[j]),
                "component": "bar_chart", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d." % (cats[i], vals[i], cats[j], vals[j]),
                             "%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 5:                                        # how many more to reach a target
        target = max(vals) + random.randint(1, 8)
        return {"prompt": "Use the bar chart. How many more would the %s bar need to reach "
                          "%d?" % (cats[i], target),
                "component": "bar_chart", "spec": spec,
                "answer": target - vals[i], "answer_type": "int",
                "solution": ["%s is %d." % (cats[i], vals[i]),
                             "%d − %d = %d." % (target, vals[i], target - vals[i])]}

    if t == 6:                                        # two bars combined
        return {"prompt": "Use the bar chart. How many %s are shown by the %s bar and the "
                          "%s bar together?" % (unit, cats[i], cats[j]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    if t == 7:                                        # grouped: last two groups
        cats2 = list(pick(_GROUPS))
        vals2 = _distinct(4, 3, 18)
        # the two TALLEST bars, named so the pupil still has to read their heights
        a, b = sorted(sorted(range(4), key=lambda k: -vals2[k])[:2])
        return {"prompt": "This bar chart shows grouped data. The two tallest bars are "
                          "%s and %s. How many are in those two groups altogether?"
                          % (cats2[a], cats2[b]),
                "component": "bar_chart",
                "spec": {"categories": cats2, "values": vals2, "mode": "read"},
                "answer": vals2[a] + vals2[b], "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (cats2[a], vals2[a], cats2[b], vals2[b]),
                             "%d + %d = %d." % (vals2[a], vals2[b], vals2[a] + vals2[b])]}

    if t == 8:                                        # grouped: how many NOT in one group
        return {"prompt": "Use the bar chart. How many are NOT in the %s bar?" % cats[i],
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals) - vals[i], "answer_type": "int",
                "solution": ["The total of all the bars is %d." % sum(vals),
                             "%d − %d = %d." % (sum(vals), vals[i], sum(vals) - vals[i])]}

    # two-step problems: interpret the bar chart, then calculate
    k = pick([m for m in range(4) if m not in (i, j)])
    styles = [1, 2] if vals[i] + vals[j] <= vals[k] else [0, 1, 2]
    style = pick(styles)
    if style == 0:
        return {"prompt": "Interpret the bar chart to solve this two-step problem. How many "
                          "MORE %s are shown by the %s bar and the %s bar together than by "
                          "the %s bar?" % (unit, cats[i], cats[j], cats[k]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] + vals[j] - vals[k], "answer_type": "int",
                "solution": ["Step 1: %d + %d = %d." % (vals[i], vals[j],
                                                        vals[i] + vals[j]),
                             "Step 2: %d − %d = %d."
                             % (vals[i] + vals[j], vals[k],
                                vals[i] + vals[j] - vals[k])]}
    if style == 1:
        extra = random.randint(2, _by_d(d, 6, 10, 20))
        return {"prompt": "Interpret the bar chart to solve this two-step problem. The %s "
                          "bar and the %s bar are added together, then %d more %s are "
                          "counted. What is the new total?"
                          % (cats[i], cats[j], extra, unit),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] + vals[j] + extra, "answer_type": "int",
                "solution": ["Step 1: %d + %d = %d." % (vals[i], vals[j],
                                                        vals[i] + vals[j]),
                             "Step 2: %d + %d = %d."
                             % (vals[i] + vals[j], extra, vals[i] + vals[j] + extra)]}
    return {"prompt": "Interpret the bar chart to solve this two-step problem. Take the "
                      "difference between the %s bar and the %s bar, then add the %s bar. "
                      "What is the result?" % (cats[i], cats[j], cats[k]),
            "component": "bar_chart", "spec": spec,
            "answer": abs(vals[i] - vals[j]) + vals[k], "answer_type": "int",
            "solution": ["Step 1: %d − %d = %d." % (max(vals[i], vals[j]),
                                                    min(vals[i], vals[j]),
                                                    abs(vals[i] - vals[j])),
                         "Step 2: %d + %d = %d."
                         % (abs(vals[i] - vals[j]), vals[k],
                            abs(vals[i] - vals[j]) + vals[k])]}


_LG_TOPICS = [
    ("Temperature in the playground", "°C", "Time",
     ["8 am", "10 am", "12 pm", "2 pm", "4 pm"], 6, 22),
    ("Height of a sunflower", "cm", "Week",
     ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"], 10, 90),
    ("Water in the school pond", "cm", "Month",
     ["Jan", "Feb", "Mar", "Apr", "May"], 20, 70),
    ("Books read by Class 4", "books", "Day",
     ["Mon", "Tue", "Wed", "Thu", "Fri"], 5, 40),
]


@skill("Y4.9.d", "Time graphs (line graphs)", S9)
def _(d=1):
    d = _tier(d)
    title, ylab, xlab, labels, lo, hi = pick(_LG_TOPICS)
    n = _by_d(d, 4, 5, 5)
    labels = labels[:n]
    step = _by_d(d, 5, 2, 1)
    vals = sorted(random.sample(range(lo, hi + 1, step), n))
    if random.random() < 0.5 and title != "Height of a sunflower":
        random.shuffle(vals)
    while len(set(vals)) != n:
        vals = random.sample(range(lo, hi + 1, step), n)
    pts = [[lab, v] for lab, v in zip(labels, vals)]
    spec = {"points": pts, "yLabel": ylab, "xLabel": xlab}
    i, j = random.sample(range(n), 2)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # read a point
        return {"prompt": "%s. Use the graph. What was the reading at %s?"
                          % (title, labels[i]),
                "component": "line_graph", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["Find %s along the bottom and read across to the y-axis."
                             % labels[i],
                             "The reading is %d %s." % (vals[i], ylab)]}

    if t == 1:                                        # missing point read-off
        k = random.randrange(n)
        sp = dict(spec)
        sp["missing"] = k
        return {"prompt": "%s. The point marked ? is at %s. Read the graph and write its "
                          "value." % (title, labels[k]),
                "component": "line_graph", "spec": sp,
                "answer": vals[k], "answer_type": "int",
                "solution": ["Read across from the ? to the y-axis.",
                             "The value is %d %s." % (vals[k], ylab)]}

    if t == 2:                                        # difference between two points
        return {"prompt": "%s. Use the graph. What is the difference between the readings "
                          "at %s and %s?" % (title, labels[i], labels[j]),
                "component": "line_graph", "spec": spec,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (labels[i], vals[i], labels[j], vals[j]),
                             "%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 3:                                        # highest reading
        return {"prompt": "%s. Use the graph. What was the HIGHEST reading?" % title,
                "component": "line_graph", "spec": spec,
                "answer": max(vals), "answer_type": "int",
                "solution": ["The highest point on the graph is at %s."
                             % labels[vals.index(max(vals))],
                             "It reads %d %s." % (max(vals), ylab)]}

    if t == 4:                                        # lowest reading label (typed)
        ask = {"Temperature in the playground": "At what time was the temperature lowest?",
               "Height of a sunflower": "In which week was the sunflower shortest?",
               "Water in the school pond": "In which month was the water lowest?",
               "Books read by Class 4": "On which day did Class 4 read the fewest books?"}[title]
        return {"prompt": "%s. Use the graph. %s (type it as it is written on the graph)" % (title, ask),
                "component": "line_graph", "spec": spec,
                "answer": labels[vals.index(min(vals))], "answer_type": "str",
                "solution": ["The lowest point is %d %s." % (min(vals), ylab),
                             "That happens at %s." % labels[vals.index(min(vals))]]}

    if t == 5:                                        # rise or fall between two points
        k = random.randrange(n - 1)
        change = vals[k + 1] - vals[k]
        return {"prompt": "%s. Use the graph. By how much did the reading change between "
                          "%s and %s? Write the size of the change."
                          % (title, labels[k], labels[k + 1]),
                "component": "line_graph", "spec": spec,
                "answer": abs(change), "answer_type": "int",
                "solution": ["%s = %d and %s = %d."
                             % (labels[k], vals[k], labels[k + 1], vals[k + 1]),
                             "The change is %d %s." % (abs(change), ylab[:-1] if abs(change) == 1 and ylab.endswith("s") else ylab)]}

    if t == 6:                                        # rose or fell (typed)
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

    if t == 7:                                        # total of two readings
        return {"prompt": "%s. Use the graph. What is the total of the readings at %s and "
                          "%s?" % (title, labels[i], labels[j]),
                "component": "line_graph", "spec": spec,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    # range from the graph
    return {"prompt": "%s. Use the graph. Take the lowest reading away from the highest "
                      "reading. What is the answer?" % title,
            "component": "line_graph", "spec": spec,
            "answer": max(vals) - min(vals), "answer_type": "int",
            "solution": ["The highest reading is %d and the lowest is %d."
                         % (max(vals), min(vals)),
                         "%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))]}


def _plot_data(d):
    """A small line-plot data set: (labels, counts, singular, plural, who-word)."""
    sing, plur, who = pick([("pet", "pets", "children"),
                            ("goal", "goals", "children"),
                            ("book", "books", "children"),
                            ("badge", "badges", "children")])
    start = random.randint(0, 2)
    labels = [start + k for k in range(_by_d(d, 4, 5, 5))]
    counts = [random.randint(1, _by_d(d, 5, 7, 9)) for _ in labels]
    while len(set(counts)) != len(counts):
        counts = [random.randint(1, _by_d(d, 5, 7, 9)) for _ in labels]
    return labels, counts, sing, plur, who


@skill("Y4.9.e", "Line plots", S9)
def _(d=1):
    d = _tier(d)
    labels, counts, sing, plur, who = _plot_data(d)
    lw = lambda k: _pl(k, sing, plur)                 # '1 pet' / '3 pets'
    plot = "; ".join("%s → %s" % (lw(lab), " ".join(["x"] * c))
                     for lab, c in zip(labels, counts))
    intro = ("A line plot shows how many %s each of some %s has. Each x stands for one "
             "child.   %s  " % (plur, who, plot))
    headers = ["Number of %s" % plur, "Number of %s" % who]
    rows = [[str(lab), str(c)] for lab, c in zip(labels, counts)]
    i, j = random.sample(range(len(labels)), 2)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2])

    if t == 0:                                        # read one column
        return _num_q("%s  How many %s have %s?" % (intro, who, lw(labels[i])),
                      counts[i], "int", unit=who,
                      solution=["Count the crosses above %d." % labels[i],
                                "There are %d." % counts[i]])

    if t == 1:                                        # total children
        return _num_q("%s  How many %s are in the line plot altogether?" % (intro, who),
                      sum(counts), "int", unit=who,
                      solution=["%s = %d." % (" + ".join(str(c) for c in counts), sum(counts))])

    if t == 2:                                        # tallest column (mode)
        top = labels[counts.index(max(counts))]
        return _num_q("%s  Which number of %s has the MOST crosses?" % (intro, plur),
                      top, "int",
                      solution=["The tallest column has %d crosses." % max(counts),
                                "That column is %s." % lw(top)])

    if t == 3:                                        # difference between columns
        hi_lab = labels[i] if counts[i] > counts[j] else labels[j]
        lo_lab = labels[j] if counts[i] > counts[j] else labels[i]
        return _num_q("%s  How many MORE %s have %s than have %s?"
                      % (intro, who, lw(hi_lab), lw(lo_lab)),
                      abs(counts[i] - counts[j]), "int", unit=who,
                      solution=["The columns have %d and %s."
                                % (max(counts[i], counts[j]), _pl(min(counts[i], counts[j]), "cross", "crosses")),
                                "%d − %d = %d." % (max(counts[i], counts[j]),
                                                   min(counts[i], counts[j]),
                                                   abs(counts[i] - counts[j]))])

    if t == 4:                                        # same data as a frequency table
        return {"prompt": "This table holds the same data as a line plot. How many %s are "
                          "recorded altogether?" % who,
                "component": "data_table",
                "spec": {"caption": "Number of %s" % plur,
                         "headers": headers, "rows": rows},
                "answer": sum(counts), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(c) for c in counts), sum(counts))]}

    if t == 5:                                        # more than a value
        cut = labels[len(labels) // 2]
        cnt = sum(c for lab, c in zip(labels, counts) if lab > cut)
        return _num_q("%s  How many %s have MORE than %s?" % (intro, who, lw(cut)),
                      cnt, "int", unit=who,
                      solution=["Add the crosses in every column above %d." % cut,
                                "That gives %d." % cnt])

    if t == 6:                                        # range of the line plot
        used = [lab for lab, c in zip(labels, counts) if c > 0]
        return _num_q("%s  What is the range (the largest number of %s take away the "
                      "smallest)?" % (intro, plur),
                      max(used) - min(used), "int",
                      solution=["The largest is %d and the smallest is %d."
                                % (max(used), min(used)),
                                "%d − %d = %d." % (max(used), min(used),
                                                   max(used) - min(used))])

    if t == 7:                                        # total number of items
        total = sum(lab * c for lab, c in zip(labels, counts))
        return _num_q("%s  How many %s do all the %s have altogether?" % (intro, plur, who),
                      total, "int",
                      solution=["Multiply each number by how many crosses it has, then add.",
                                "%s = %d."
                                % (" + ".join("%d×%d" % (lab, c)
                                              for lab, c in zip(labels, counts)), total)])

    if t == 9:                                        # the same data drawn as a chart
        return {"prompt": "The chart shows how many %s each of some %s has. How many %s have %s?"
                          % (plur, who, who, lw(labels[i])),
                "component": "bar_chart",
                "spec": {"categories": [str(lab) for lab in labels], "values": counts, "mode": "read"},
                "answer": counts[i], "answer_type": "int",
                "solution": ["Read the bar above %d." % labels[i], "It reaches %d." % counts[i]]}

    if t == 10:                                       # fewer than a value
        cut = labels[len(labels) // 2]
        cnt = sum(c for lab, c in zip(labels, counts) if lab < cut)
        return _num_q("%s  How many %s have FEWER than %s?" % (intro, who, lw(cut)), cnt, "int", unit=who,
                      solution=["Add the crosses in every column below %d." % cut, "That gives %d." % cnt])

    if t == 11:                                       # missing count from the total
        k = random.randrange(len(labels))
        r2 = [[lab, "" if n == k else c] for n, (lab, c) in enumerate(rows)]
        return {"prompt": "%d %s were asked how many %s they have. The table shows the results, but one number is "
                          "missing. What is it?" % (sum(counts), who, plur),
                "component": "data_table",
                "spec": {"headers": headers, "rows": r2, "missing": [k, 1]},
                "answer": counts[k], "answer_type": "int",
                "solution": ["The other numbers add to %d." % (sum(counts) - counts[k]),
                             "%d − %d = %d." % (sum(counts), sum(counts) - counts[k], counts[k])]}

    if t == 12:                                       # at least a value
        cut = labels[len(labels) // 2]
        cnt = sum(c for lab, c in zip(labels, counts) if lab >= cut)
        return _num_q("%s  How many %s have %s or more?" % (intro, who, lw(cut)), cnt, "int", unit=who,
                      solution=["Add the crosses for %d and every column above it." % cut, "That gives %d." % cnt])

    if t == 13:                                       # least common value, from a chart
        low = min(counts)
        if counts.count(low) == 1:
            ans = labels[counts.index(low)]
            return {"prompt": "The chart shows how many %s each of some %s has. Which number of %s is the LEAST common?"
                              % (plur, who, plur),
                    "component": "bar_chart",
                    "spec": {"categories": [str(lab) for lab in labels], "values": counts, "mode": "read"},
                    "answer": ans, "answer_type": "int",
                    "solution": ["The shortest bar is above %d." % ans, "Only %d %s that many." % (low, "child has" if low == 1 else "children have")]}

    # build a line plot: how many crosses to draw
    v = random.randint(2, 9)
    return _num_q("You are drawing a line plot. Each x stands for one child. %d children "
                  "have %s. How many crosses do you draw above %d?"
                  % (v, lw(labels[i]), labels[i]),
                  v, "int", unit="crosses",
                  solution=["One cross for each child.",
                            "Draw %d crosses." % v])


@skill("Y4.9.f", "Comparison questions from data", S9)
def _(d=1):
    d = _tier(d)
    cats, vals = _chart(d, 4, pool=["Rovers", "United", "City", "Albion", "Wanderers"])
    unit = pick(["goals", "points", "runs"])
    bar = {"categories": cats, "values": vals, "mode": "read"}
    tbl_rows = [[c, str(v)] for c, v in zip(cats, vals)]
    tbl = {"caption": "%s scored" % unit.capitalize(),
           "headers": ["Team", unit.capitalize()], "rows": tbl_rows}
    i, j = random.sample(range(4), 2)
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 2, 1])

    if t == 0:                                        # sum from a bar chart
        return {"prompt": "Use the bar chart. How many %s did %s and %s get altogether?"
                          % (unit, cats[i], cats[j]),
                "component": "bar_chart", "spec": bar,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%s = %d and %s = %d." % (cats[i], vals[i], cats[j], vals[j]),
                             "%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    if t == 1:                                        # difference from a table
        return {"prompt": "Use the table. How many MORE %s did %s get than %s?"
                          % (unit, cats[i] if vals[i] > vals[j] else cats[j],
                             cats[j] if vals[i] > vals[j] else cats[i]),
                "component": "data_table", "spec": tbl,
                "answer": abs(vals[i] - vals[j]), "answer_type": "int",
                "solution": ["%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                                abs(vals[i] - vals[j]))]}

    if t == 2:                                        # most (typed)
        return {"prompt": "Use the table. Which team got the MOST %s? (type the name)" % unit,
                "component": "data_table", "spec": tbl,
                "answer": cats[vals.index(max(vals))], "answer_type": "str",
                "solution": ["The largest number is %d." % max(vals),
                             "That is %s." % cats[vals.index(max(vals))]]}

    if t == 3:                                        # least (typed)
        return {"prompt": "Use the table. Which team got the FEWEST %s? (type the name)" % unit,
                "component": "data_table", "spec": tbl,
                "answer": cats[vals.index(min(vals))], "answer_type": "str",
                "solution": ["The smallest number is %d." % min(vals),
                             "That is %s." % cats[vals.index(min(vals))]]}

    if t == 4:                                        # total of all
        return {"prompt": "Use the table. How many %s were scored altogether?" % unit,
                "component": "data_table", "spec": tbl,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(str(v) for v in vals), sum(vals))]}

    if t == 5:                                        # two-step: total minus one
        return {"prompt": "Use the table. How many %s were scored by all the teams EXCEPT "
                          "%s?" % (unit, cats[i]),
                "component": "data_table", "spec": tbl,
                "answer": sum(vals) - vals[i], "answer_type": "int",
                "solution": ["Total = %d." % sum(vals),
                             "%d − %d = %d." % (sum(vals), vals[i], sum(vals) - vals[i])]}

    if t == 6:                                        # two-step: difference of two sums
        a, b, c, e = vals
        # the subtracted category must be the smallest, or the answer goes negative
        order = sorted(range(3), key=lambda k: vals[k])
        i0, i1, i2 = order[2], order[1], order[0]
        a, b, c = vals[i0], vals[i1], vals[i2]
        cats = [cats[i0], cats[i1], cats[i2]] + list(cats[3:])
        return {"prompt": "Use the table. Add the %s of %s and %s, then take away the %s "
                          "of %s. What is the answer?"
                          % (unit, cats[0], cats[1], unit, cats[2]),
                "component": "data_table", "spec": tbl,
                "answer": a + b - c, "answer_type": "int",
                "solution": ["%d + %d = %d." % (a, b, a + b),
                             "%d − %d = %d." % (a + b, c, a + b - c)]}

    if t == 7:                                        # comparison from a bar chart, two-step
        k = pick([2, 3, 4])
        return {"prompt": "Use the bar chart. How many more %s would %s and %s need "
                          "between them to reach %d %s altogether?"
                          % (unit, cats[i], cats[j], vals[i] + vals[j] + k, unit),
                "component": "bar_chart", "spec": bar,
                "answer": k, "answer_type": "int",
                "solution": ["%s + %s = %d + %d = %d."
                             % (cats[i], cats[j], vals[i], vals[j], vals[i] + vals[j]),
                             "%d − %d = %d." % (vals[i] + vals[j] + k, vals[i] + vals[j], k)]}

    # comparison as a multiple
    base = vals[0]
    mult = pick([2, 3])
    return _num_q("%s scored %d %s. %s scored %d times as many. How many %s did %s score?"
                  % (cats[0], base, unit, cats[1], mult, unit, cats[1]),
                  base * mult, "int", unit=unit,
                  solution=["%d × %d = %d." % (base, mult, base * mult)])


# (title, column A, column B, row A, row B, phrases for each of the four labels,
#  and the noun being sorted). Each phrase completes "How many <phrase> are there?"
_CARROLL = [
    ("Shape sort", "Has 4 sides", "Does not have 4 sides", "Red", "Not red",
     "shapes with 4 sides", "shapes without 4 sides", "red shapes", "shapes that are not red",
     "shapes"),
    ("Class survey", "Wears glasses", "Does not wear glasses", "Girls", "Boys",
     "children who wear glasses", "children who do not wear glasses", "girls", "boys",
     "children"),
    ("Number sort", "Even", "Odd", "Less than 20", "20 or more",
     "even numbers", "odd numbers", "numbers less than 20", "numbers that are 20 or more",
     "numbers"),
    ("Pet survey", "Has a dog", "No dog", "Has a cat", "No cat",
     "children with a dog", "children without a dog", "children with a cat",
     "children without a cat", "children"),
]


@skill("Y4.9.g", "Venn and Carroll diagrams", S9)
def _(d=1):
    d = _tier(d)
    (title, colA, colB, rowA, rowB,
     phA, phB, phR, phS, noun) = pick(_CARROLL)
    hi = _by_d(d, 9, 15, 25)
    a, b, c, e = [random.randint(1, hi) for _ in range(4)]
    headers = ["", colA, colB]
    rows = [[rowA, str(a), str(b)], [rowB, str(c), str(e)]]
    t = _pick_t([2, 2, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # missing cell in a Carroll diagram
        total = a + b + c + e
        blank = [[rowA, str(a), str(b)], [rowB, str(c), ""]]
        return {"prompt": "This Carroll diagram sorts %d %s in total. How many belong in "
                          "the empty box — the box for '%s' and '%s'?"
                          % (total, noun, rowB, colB),
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": blank,
                         "missing": [1, 2]},
                "answer": e, "answer_type": "int",
                "solution": ["%d + %d + %d = %d are already shown." % (a, b, c, a + b + c),
                             "%d − %d = %d." % (total, a + b + c, e)]}

    if t == 1:                                        # read one region
        r, cc = random.randrange(2), random.randrange(2)
        val = [[a, b], [c, e]][r][cc]
        return {"prompt": "Use the Carroll diagram. How many are in the box for '%s' and "
                          "'%s'?" % ([rowA, rowB][r], [colA, colB][cc]),
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": val, "answer_type": "int",
                "solution": ["Look where the '%s' row meets the '%s' column."
                             % ([rowA, rowB][r], [colA, colB][cc]),
                             "The box shows %d." % val]}

    if t == 2:                                        # row total
        return {"prompt": "Use the Carroll diagram. How many %s are there altogether?" % phR,
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": a + b, "answer_type": "int",
                "solution": ["Add across the '%s' row: %d + %d = %d." % (rowA, a, b, a + b)]}

    if t == 3:                                        # column total
        return {"prompt": "Use the Carroll diagram. How many %s are there altogether?" % phA,
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": a + c, "answer_type": "int",
                "solution": ["Add down the '%s' column: %d + %d = %d."
                             % (colA, a, c, a + c)]}

    if t == 4:                                        # grand total
        return {"prompt": "Use the Carroll diagram. How many %s are sorted altogether?"
                          % noun,
                "component": "data_table",
                "spec": {"caption": title, "headers": headers, "rows": rows},
                "answer": a + b + c + e, "answer_type": "int",
                "solution": ["%d + %d + %d + %d = %d." % (a, b, c, e, a + b + c + e)]}

    if t == 5:                                        # Venn: overlap
        only_a = random.randint(2, hi)
        both = random.randint(1, hi)
        only_b = random.randint(2, hi)
        outside = random.randint(0, 6)
        return _num_q("In a Venn diagram one ring is 'likes football' and the other is "
                      "'likes swimming'. %d children like only football, %d like only "
                      "swimming, %d like both and %d like neither. How many children like "
                      "football altogether?" % (only_a, only_b, both, outside),
                      only_a + both, "int", unit="children",
                      solution=["The football ring holds the football-only children AND "
                                "the overlap.",
                                "%d + %d = %d." % (only_a, both, only_a + both)])

    if t == 6:                                        # Venn: total in the diagram
        only_a = random.randint(2, hi)
        both = random.randint(1, hi)
        only_b = random.randint(2, hi)
        outside = random.randint(0, 6)
        return _num_q("In a Venn diagram one ring is 'has a bike' and the other is 'has "
                      "roller skates'. %d children are in the bike ring only, %d are in "
                      "the skates ring only, %d are in the overlap and %d are outside both "
                      "rings. How many children were asked altogether?"
                      % (only_a, only_b, both, outside),
                      only_a + only_b + both + outside, "int", unit="children",
                      solution=["%d + %d + %d + %d = %d."
                                % (only_a, only_b, both, outside,
                                   only_a + only_b + both + outside)])

    if t == 7:                                        # Venn: overlap by subtraction
        total_a = random.randint(8, hi + 8)
        both = random.randint(1, total_a - 1)
        return _num_q("In a Venn diagram, %d children are inside the 'plays the recorder' "
                      "ring. %d of them %s also inside the 'sings in the choir' ring. How "
                      "many children play the recorder but do NOT sing in the choir?"
                      % (total_a, both, "is" if both == 1 else "are"),
                      total_a - both, "int", unit="children",
                      solution=["%d − %d = %d." % (total_a, both, total_a - both)])

    # Carroll: how many are in the second row (the 'not' row)
    return {"prompt": "Use the Carroll diagram. How many %s are there altogether?" % phS,
            "component": "data_table",
            "spec": {"caption": title, "headers": headers, "rows": rows},
            "answer": c + e, "answer_type": "int",
            "solution": ["The '%s' row holds %d and %d." % (rowB, c, e),
                         "%d + %d = %d." % (c, e, c + e)]}


@skill("Y4.9.h", "Likelihood and simple probability", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # certain / impossible / likely
        events = [
            ("rolling a number less than 7 on an ordinary dice", "certain"),
            ("rolling a 9 on an ordinary dice", "impossible"),
            ("picking a red counter from a bag of only red counters", "certain"),
            ("picking a blue counter from a bag of only red counters", "impossible"),
            ("the sun rising tomorrow morning", "certain"),
            ("a fair coin landing on heads", "even chance"),
        ]
        hard = [                                      # stretch: you have to reason it out
            ("rolling an even number on an ordinary dice", "even chance"),
            ("rolling a 0 on an ordinary dice", "impossible"),
            ("rolling a number greater than 0 on an ordinary dice", "certain"),
            ("picking a red counter from a bag of 5 red and 5 blue counters", "even chance"),
            ("rolling a number from 1 to 3 on an ordinary dice", "even chance"),
        ]
        event, ans = pick(_by_d(d, events[2:], events, events[:2] + hard))
        return _num_q("Is this certain, impossible or an even chance: %s? "
                      "(type the answer)" % event,
                      ans, "str", text=True, placeholder="certain / impossible / even chance",
                      solution=["%s is %s." % (event.capitalize(), ans)])

    if t == 1:                                        # likely / unlikely from counters
        red = random.randint(*_by_d(d, (8, 12), (7, 12), (7, 10)))
        blue = random.randint(*_by_d(d, (1, 2), (1, 3), (3, 5)))   # stretch: closer counts
        ask_red = random.random() < 0.5
        ans = "likely" if ask_red else "unlikely"
        return _num_q("A bag holds %s and %s. One counter is "
                      "taken without looking. Is taking a %s counter likely or unlikely? "
                      "(type one word)" % (_pl(red, "red counter"), _pl(blue, "blue counter"),
                                            "red" if ask_red else "blue"),
                      ans, "str", text=True, placeholder="likely / unlikely",
                      solution=["There are many more red counters than blue ones.",
                                "So taking a %s counter is %s."
                                % ("red" if ask_red else "blue", ans)])

    if t == 2:                                        # counting the other outcome
        red = random.randint(*_by_d(d, (2, 6), (3, 12), (5, 15)))
        blue = random.randint(*_by_d(d, (2, 6), (3, 12), (5, 15)))
        if d == 2:                                    # stretch: two other colours to add
            green = random.randint(3, 12)
            return _num_q("A bag holds %s, %s and %s. How many counters in the bag are "
                          "NOT red?" % (_pl(red, "red counter"), _pl(blue, "blue counter"),
                                        _pl(green, "green counter")),
                          blue + green, "int", unit="counters",
                          solution=["The blue and the green counters are not red.",
                                    "%d + %d = %d." % (blue, green, blue + green)])
        return _num_q("A bag holds %s and %s. How many counters "
                      "in the bag are NOT red?"
                      % (_pl(red, "red counter"), _pl(blue, "blue counter")),
                      blue, "int", unit="counters",
                      solution=["Only the blue counters are not red.",
                                "That is %d." % blue])

    if t == 3:                                        # total outcomes
        if d == 2:
            n = random.randint(8, 12)
            return _num_q("A spinner has %d equal sections numbered 1 to %d. How many "
                          "different numbers could it land on?" % (n, n),
                          n, "int", unit="numbers",
                          solution=["The spinner shows 1, 2, ... up to %d." % n,
                                    "That is %d different numbers." % n])
        return _num_q("An ordinary dice is numbered 1 to 6. How many different numbers "
                      "could it land on?",
                      6, "int", unit="numbers",
                      solution=["The dice shows 1, 2, 3, 4, 5 or 6.",
                                "That is 6 different numbers."])

    if t == 4:                                        # favourable outcomes on a dice
        if d == 2:                                    # stretch: a 1-10 spinner, two conditions
            kind, cnt, fit = pick([("a multiple of 3", 3, "3, 6, 9"),
                                   ("a number bigger than 6", 4, "7, 8, 9, 10"),
                                   ("an even number less than 9", 4, "2, 4, 6, 8"),
                                   ("an odd number bigger than 4", 3, "5, 7, 9"),
                                   ("a multiple of 4", 2, "4, 8")])
            return _num_q("A spinner has 10 equal sections numbered 1 to 10. On how many "
                          "sections could it land on %s?" % kind,
                          cnt, "int", unit="sections",
                          solution=["The numbers that fit are %s." % fit,
                                    "There are %d." % cnt])
        kind, cnt = pick(_by_d(d, [("an even number", 3), ("an odd number", 3)],
                               [("an even number", 3), ("an odd number", 3),
                                ("a number bigger than 4", 2), ("a number less than 3", 2),
                                ("a multiple of 3", 2)], None))
        return _num_q("An ordinary dice is numbered 1 to 6. On how many of the six faces "
                      "would you roll %s?" % kind,
                      cnt, "int", unit="faces",
                      solution=["List the faces 1, 2, 3, 4, 5, 6 and count those that fit.",
                                "There are %d." % cnt])

    if t == 5:                                        # probability as a fraction
        red = random.randint(1, 3 if d == 0 else 5)
        others = random.randint(1, 4 if d == 0 else 7)
        total = red + others
        if d == 2:                                    # stretch: three colours in the bag
            yel = random.randint(1, 5)
            grn = random.randint(1, 5)
            total = red + yel + grn
            return _num_q("A bag holds %s, %s and %s. One counter is taken without looking. "
                          "Write the fraction of the counters that are red."
                          % (_pl(red, "red counter"), _pl(yel, "yellow counter"),
                             _pl(grn, "green counter")),
                          "%d/%d" % (red, total), "frac", text=True, placeholder="e.g. 3/8",
                          solution=["There are %d + %d + %d = %d counters in total."
                                    % (red, yel, grn, total),
                                    "%d of them are red, so the fraction is %d/%d."
                                    % (red, red, total)])
        return _num_q("A bag holds %s and %s. One counter is taken without looking. "
                      "Write the fraction of the counters that are red."
                      % (_pl(red, "red counter"), _pl(others, "yellow counter")),
                      "%d/%d" % (red, total), "frac", text=True, placeholder="e.g. 3/8",
                      solution=["There are %d + %d = %d counters in total."
                                % (red, others, total),
                                "%d of them are red, so the fraction is %d/%d."
                                % (red, red, total)])

    if t == 6:                                        # spinner
        parts = pick(_by_d(d, [4, 5, 6], [4, 5, 6, 8, 10], [8, 10, 12]))
        wins = random.randint(1, parts - 1)
        if d == 2 and random.random() < 0.5:          # stretch: the sections that are NOT green
            rest = parts - wins
            return _num_q("A spinner has %d equal sections and %d of them %s green. Write the "
                          "fraction of the spinner that is NOT green."
                          % (parts, wins, "is" if wins == 1 else "are"),
                          "%d/%d" % (rest, parts), "frac", text=True, placeholder="e.g. 3/8",
                          solution=["%d − %d = %s %s not green." % (parts, wins, _pl(rest, "section"), "is" if rest == 1 else "are"),
                                    "The fraction is %d/%d." % (rest, parts)])
        return _num_q("A spinner has %d equal sections and %d of them %s green. Write the "
                      "fraction of the spinner that is green."
                      % (parts, wins, "is" if wins == 1 else "are"),
                      "%d/%d" % (wins, parts), "frac", text=True, placeholder="e.g. 3/8",
                      solution=["%s out of %d %s green." % (_pl(wins, "section"), parts, "is" if wins == 1 else "are"),
                                "The fraction is %d/%d." % (wins, parts)])

    if t == 7:                                        # make it certain
        red = random.randint(2, 8)
        blue = random.randint(1, 3 if d == 0 else 5)
        if d == 2:                                    # stretch: two colours must go
            grn = random.randint(1, 5)
            return _num_q("A bag holds %s, %s and %s. How many counters must be taken out "
                          "so that picking a red counter becomes certain?"
                          % (_pl(red, "red counter"), _pl(blue, "blue counter"),
                             _pl(grn, "green counter")),
                          blue + grn, "int", unit="counters",
                          solution=["Picking red is certain only when every counter is red.",
                                    "Take out all %d blue and %d green: %d + %d = %d."
                                    % (blue, grn, blue, grn, blue + grn)])
        return _num_q("A bag holds %s and %s. How many blue "
                      "counters must be taken out so that picking a red counter becomes "
                      "certain?" % (_pl(red, "red counter"), _pl(blue, "blue counter")),
                      blue, "int", unit="counters",
                      solution=["Picking red is certain only when every counter is red.",
                                "All %s must be taken out." % _pl(blue, "blue counter")])

    # ordering likelihood
    if d == 2:                                        # stretch: same-size bags, close counts
        total = random.randint(10, 16)
        a = random.randint(3, total - 4)
        b = a + pick([-2, -1, 1, 2])
        win = "A" if a > b else "B"
        return _num_q("Bag A holds %d counters and %d of them are red. Bag B also holds %d "
                      "counters and %d of them are red. From which bag are you more likely "
                      "to pick a red counter? (type A or B)" % (total, a, total, b),
                      win, "str", text=True, placeholder="A / B",
                      solution=["Both bags hold %d counters, so compare %d/%d with %d/%d."
                                % (total, a, total, b, total),
                                "Bag %s has more red counters, so red is more likely from "
                                "bag %s." % (win, win)])
    a = random.randint(1, 3 if d == 0 else 4)
    b = random.randint(8 if d == 0 else 6, 12)
    if random.random() < 0.5:                         # don't let the answer always be B
        a, b, win = b, a, "A"
    else:
        win = "B"
    return _num_q("Bag A holds %s and 10 white counters. Bag B holds %s and 10 white "
                  "counters. From which bag are you more likely to pick a red counter? "
                  "(type A or B)" % (_pl(a, "red counter"), _pl(b, "red counter")),
                  win, "str", text=True, placeholder="A / B",
                  solution=["Bag %s has more red counters among the same 10 white ones." % win,
                            "So a red counter is more likely from bag %s." % win])


@skill("Y4.9.i", "Mean and range", S9)
def _(d=1):
    d = _tier(d)
    n = _by_d(d, 3, 4, 5)
    t = _pick_t([1, 1, 1, 1, 1, 1, 2, 1, 1])

    def _mean_set(count, lo, hi):
        """A list whose total divides exactly by `count`."""
        vals = [random.randint(lo, hi) for _ in range(count)]
        while sum(vals) % count:
            vals[random.randrange(count)] = random.randint(lo, hi)
        return vals

    if t == 0:                                        # mean of a list
        vals = _mean_set(n, _by_d(d, 2, 3, 5), _by_d(d, 10, 20, 40))
        m = sum(vals) // n
        return _num_q("Work out the mean of these numbers: %s."
                      % ", ".join(str(v) for v in vals),
                      m, "int",
                      solution=["Add them: %s = %d." % (" + ".join(str(v) for v in vals),
                                                        sum(vals)),
                                "%d ÷ %d = %d." % (sum(vals), n, m)])

    if t == 1:                                        # range of a list
        vals = _distinct(n, 1, _by_d(d, 20, 40, 80))
        return _num_q("Work out the range of these numbers: %s."
                      % ", ".join(str(v) for v in vals),
                      max(vals) - min(vals), "int",
                      solution=["The range is the largest take away the smallest.",
                                "%d − %d = %d." % (max(vals), min(vals),
                                                   max(vals) - min(vals))])

    if t == 2:                                        # mean word problem
        who = pick(NAMES)
        thing = pick(["goals", "points", "stickers", "marbles"])
        vals = _mean_set(n, 2, _by_d(d, 10, 18, 30))
        m = sum(vals) // n
        return _num_q("%s scored %s %s over %d games. What is the mean number of %s per "
                      "game?" % (who, ", ".join(str(v) for v in vals[:-1]),
                                 "and %d %s" % (vals[-1], thing), n, thing),
                      m, "int", unit=thing,
                      solution=["Total = %d." % sum(vals),
                                "%d ÷ %d = %d." % (sum(vals), n, m)])

    if t == 3:                                        # missing value from the mean
        m = random.randint(3, _by_d(d, 10, 15, 25))
        others = [random.randint(1, 2 * m) for _ in range(n - 1)]
        last = m * n - sum(others)
        while last < 1:
            others = [random.randint(1, 2 * m) for _ in range(n - 1)]
            last = m * n - sum(others)
        return _num_q("The mean of %d numbers is %d. %d of the numbers are %s. What is the "
                      "last number?" % (n, m, n - 1, ", ".join(str(v) for v in others)),
                      last, "int",
                      solution=["The total must be %d × %d = %d." % (m, n, m * n),
                                "%d − %d = %d." % (m * n, sum(others), last)])

    if t == 4:                                        # total from the mean
        m = random.randint(3, _by_d(d, 10, 20, 40))
        return _num_q("The mean of %d numbers is %d. What is the total of all %d numbers?"
                      % (n, m, n),
                      m * n, "int",
                      solution=["Total = mean × how many numbers.",
                                "%d × %d = %d." % (m, n, m * n)])

    if t == 5:                                        # range word problem
        temps = _distinct(n, -5 if d == 2 else 1, _by_d(d, 20, 25, 30))
        return _num_q("The temperature at noon on %d days was %s °C. What was the range of "
                      "the temperatures?" % (n, ", ".join(str(v) for v in temps)),
                      max(temps) - min(temps), "int", unit="degrees",
                      solution=["The highest was %d °C and the lowest was %d °C."
                                % (max(temps), min(temps)),
                                "%d − %d = %d." % (max(temps), min(temps),
                                                   max(temps) - min(temps))])

    if t == 6:                                        # mean or range from a bar chart
        cats, vals = _chart(d, 4)
        ask_mean = sum(vals) % 4 == 0
        spec = {"categories": cats, "values": vals, "mode": "read"}
        if ask_mean:
            return {"prompt": "Use the bar chart. What is the mean of the four bars?",
                    "component": "bar_chart", "spec": spec,
                    "answer": sum(vals) // 4, "answer_type": "int",
                    "solution": ["Total = %d." % sum(vals),
                                 "%d ÷ 4 = %d." % (sum(vals), sum(vals) // 4)]}
        return {"prompt": "Use the bar chart. What is the range of the four bars?",
                "component": "bar_chart", "spec": spec,
                "answer": max(vals) - min(vals), "answer_type": "int",
                "solution": ["The tallest bar is %d and the shortest is %d."
                             % (max(vals), min(vals)),
                             "%d − %d = %d." % (max(vals), min(vals),
                                                max(vals) - min(vals))]}

    if t == 7:                                        # compare two means
        v1 = _mean_set(3, 2, 18)
        v2 = _mean_set(3, 2, 18)
        m1, m2 = sum(v1) // 3, sum(v2) // 3
        while m1 == m2:
            v2 = _mean_set(3, 2, 18)
            m2 = sum(v2) // 3
        return _num_q("Team A scored %s and team B scored %s. Which team has the higher "
                      "mean score? Write that mean."
                      % (", ".join(str(v) for v in v1), ", ".join(str(v) for v in v2)),
                      max(m1, m2), "int",
                      solution=["Team A: %d ÷ 3 = %d. Team B: %d ÷ 3 = %d."
                                % (sum(v1), m1, sum(v2), m2),
                                "The higher mean is %d." % max(m1, m2)])

    # mean of a data table
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"][:n]
    vals = _mean_set(n, 2, _by_d(d, 12, 20, 35))
    rows = [[dd, str(v)] for dd, v in zip(days, vals)]
    ask_mean = random.random() < 0.5
    if ask_mean:
        return {"prompt": "Use the table. What is the mean number of books read per day?",
                "component": "data_table",
                "spec": {"caption": "Books read", "headers": ["Day", "Books"], "rows": rows},
                "answer": sum(vals) // n, "answer_type": "int",
                "solution": ["Total = %d." % sum(vals),
                             "%d ÷ %d = %d." % (sum(vals), n, sum(vals) // n)]}
    return {"prompt": "Use the table. What is the range of the number of books read?",
            "component": "data_table",
            "spec": {"caption": "Books read", "headers": ["Day", "Books"], "rows": rows},
            "answer": max(vals) - min(vals), "answer_type": "int",
            "solution": ["The most was %d and the fewest was %d." % (max(vals), min(vals)),
                         "%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))]}


@skill("Y4.9.j", "Mixed multi-step reasoning", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                        # money: buy several, get change
        who = pick(NAMES)
        n = random.randint(2, _by_d(d, 4, 6, 9))
        price = random.randint(15, _by_d(d, 80, 250, 480))
        cost = n * price
        note = next(v for v in (200, 500, 1000, 2000, 5000) if v > cost)
        paid = "£2 coin" if note == 200 else "£%d note" % (note // 100)
        return _num_q("%s buys %s at %s each and pays with a %s. How much change does %s "
                      "get? Write the answer in pence."
                      % (who, _pl(n, "pencil"), money(price), paid, who),
                      note - cost, "int", unit="p",
                      solution=["%d × %s = %s." % (n, money(price), money(cost)),
                                "%s − %s = %s." % (money(note), money(cost),
                                                   money(note - cost))])

    if t == 1:                                        # multiply then add
        a = random.randint(3, 12)
        b = random.randint(3, 12)
        c = random.randint(5, _by_d(d, 30, 80, 200))
        return _num_q("A box holds %d pencils. A school buys %d boxes and is given %d extra "
                      "pencils. How many pencils does the school have?" % (a, b, c),
                      a * b + c, "int", unit="pencils",
                      solution=["%d × %d = %d." % (a, b, a * b),
                                "%d + %d = %d." % (a * b, c, a * b + c)])

    if t == 2:                                        # fraction of an amount, two-step
        den = pick([2, 3, 4, 5, 10])
        per = random.randint(3, _by_d(d, 10, 20, 40))
        total = den * per
        num = random.randint(1, den - 1)
        who = pick(NAMES)
        return _num_q("%s has %d stickers and gives away %d/%d of them. How many stickers "
                      "does %s have left?" % (who, total, num, den, who),
                      total - per * num, "int", unit="stickers",
                      solution=["%d ÷ %d = %d, so %d/%d of %d is %d."
                                % (total, den, per, num, den, total, per * num),
                                "%d − %d = %d." % (total, per * num, total - per * num)])

    if t == 3:                                        # measures: convert then subtract
        m = random.randint(2, _by_d(d, 5, 9, 15))
        cm = random.randint(10, 95)
        cut = random.randint(20, 95)
        total = m * 100 + cm
        return _num_q("A rope is %d m %d cm long. %d cm is cut off. How long is the rope "
                      "now, in centimetres?" % (m, cm, cut),
                      total - cut, "int", unit="cm",
                      solution=["%d m %d cm = %d cm." % (m, cm, total),
                                "%d − %d = %d cm." % (total, cut, total - cut)])

    if t == 4:                                        # time: duration across the hour
        h = random.randint(1, 11)
        mstart = pick([5, 10, 15, 20, 25, 35, 40, 45, 50, 55])
        dur = random.randint(20, _by_d(d, 45, 75, 110))
        total_start = h * 60 + mstart
        end = total_start + dur
        return _num_q("A film starts at %d:%02d and lasts %d minutes. At what time does it "
                      "finish? Write the time as h:mm." % (h, mstart, dur),
                      "%d:%02d" % (((end // 60 - 1) % 12) + 1, end % 60), "time",
                      text=True, placeholder="e.g. 3:45",
                      solution=["%d:%02d plus %d minutes." % (h, mstart, dur),
                                "The film finishes at %d:%02d."
                                % (((end // 60 - 1) % 12) + 1, end % 60)])

    if t == 5:                                        # division with a remainder
        per = random.randint(3, 9)
        groups = random.randint(3, _by_d(d, 8, 14, 25))
        rem = random.randint(1, per - 1)
        total = per * groups + rem
        ask_rem = random.random() < 0.5
        if ask_rem:
            return _num_q("%d children are put into teams of %d. How many children are "
                          "left over?" % (total, per),
                          rem, "int", unit="children",
                          solution=["%d ÷ %d = %d remainder %d." % (total, per, groups, rem),
                                    "So %d are left over." % rem])
        return _num_q("%d children are put into teams of %d. How many complete teams are "
                      "there?" % (total, per),
                      groups, "int", unit="teams",
                      solution=["%d ÷ %d = %d remainder %d." % (total, per, groups, rem),
                                "That makes %d complete teams." % groups])

    if t == 6:                                        # perimeter + cost (geometry link)
        w = random.randint(3, _by_d(d, 8, 15, 25))
        h = random.randint(3, _by_d(d, 8, 15, 25))
        cost = pick([2, 3, 4, 5])
        p = 2 * (w + h)
        return _num_q("A rectangular vegetable patch is %d m by %d m. Edging strips cost "
                      "£%d for each metre and must go all the way round. What is the total "
                      "cost, in pounds?" % (w, h, cost),
                      p * cost, "int", unit="pounds",
                      solution=["Perimeter = 2 × (%d + %d) = %d m." % (w, h, p),
                                "%d × £%d = £%d." % (p, cost, p * cost)])

    if t == 7:                                        # data + calculation
        cats, vals = _chart(d, 4, pool=["Monday", "Tuesday", "Wednesday", "Thursday"])
        each = pick([2, 3, 4, 5])
        return {"prompt": "Use the bar chart. Each ticket costs £%d. How much money was "
                          "taken on %s and %s altogether, in pounds?"
                          % (each, cats[0], cats[1]),
                "component": "bar_chart",
                "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": each * (vals[0] + vals[1]), "answer_type": "int",
                "solution": ["%d + %d = %d tickets." % (vals[0], vals[1], vals[0] + vals[1]),
                             "%d × £%d = £%d." % (vals[0] + vals[1], each,
                                                  each * (vals[0] + vals[1]))]}

    if t == 8:                                        # negative numbers
        start = -random.randint(1, 9)
        rise = random.randint(2, _by_d(d, 8, 15, 25))
        ask_rise = random.random() < 0.5
        if ask_rise:
            return _num_q("At midnight the temperature was %d °C. By noon it had risen by "
                          "%d degrees. What was the temperature at noon, in °C?"
                          % (start, rise),
                          start + rise, "int", unit="degrees",
                          solution=["Count up %d from %d." % (rise, start),
                                    "%d + %d = %d °C." % (start, rise, start + rise)])
        end = start + rise
        return _num_q("At midnight the temperature was %d °C and by noon it was %d °C. By "
                      "how many degrees did the temperature rise?" % (start, end),
                      rise, "int", unit="degrees",
                      solution=["Count up from %d to %d." % (start, end),
                                "That is a rise of %d degrees." % rise])

    if t == 9:                                        # area + reasoning
        w = random.randint(2, _by_d(d, 6, 10, 15))
        h = random.randint(2, _by_d(d, 6, 10, 15))
        used = random.randint(1, w * h - 1)
        return _num_q("A rectangular tray is %d tiles by %d tiles. %s has already laid %s. "
                      "How many more tiles are needed to fill the tray?"
                      % (w, h, pick(NAMES), _pl(used, "tile")),
                      w * h - used, "int", unit="tiles",
                      solution=["%d × %d = %d tiles fill the tray." % (w, h, w * h),
                                "%d − %d = %d." % (w * h, used, w * h - used)])

    # multi-step with a scaling comparison
    small = random.randint(4, _by_d(d, 12, 25, 45))
    mult = pick([2, 3, 4])
    extra = random.randint(2, min(20, small * mult - 1))
    one, two = _two_names()
    return _num_q("%s has %d marbles. %s starts with %d times as many, then loses %d. "
                  "How many marbles does %s have now?"
                  % (one, small, two, mult, extra, two),
                  small * mult - extra, "int", unit="marbles",
                  solution=["%d × %d = %d." % (small, mult, small * mult),
                            "%d − %d = %d." % (small * mult, extra, small * mult - extra)])
