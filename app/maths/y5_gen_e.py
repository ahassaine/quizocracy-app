# Year 5 generators: strands 5.8 and 5.9.
#
# Geometry: 3-D shapes from 2-D representations, angles in degrees (estimate, classify, measure),
# angles at a point, on a straight line and multiples of 90°, properties of rectangles, regular and
# irregular polygons, reflection and translation.  Statistics: line graphs (read, compare, sum,
# difference) and tables including timetables.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S8 = "5.8 Geometry"
S9 = "5.9 Statistics"

SOLIDS = {
    "cube": (6, 12, 8), "cuboid": (6, 12, 8), "square-based pyramid": (5, 8, 5),
    "triangular prism": (5, 9, 6),
}
NET_NAME = {"cube": "cube", "cuboid": "cuboid", "square_pyramid": "square-based pyramid",
            "triangular_prism": "triangular prism", "cylinder": "cylinder", "cone": "cone"}


def _kind(deg):
    if deg < 90:
        return "acute"
    if deg == 90:
        return "right"
    if deg < 180:
        return "obtuse"
    if deg == 180:
        return "straight"
    return "reflex"


# ================================================================== 5.8 ======
@skill("Y5.8.a", "Identify 3-D shapes from 2-D representations", S8)
def _(d=1):
    d = _d(d)

    def t_net():
        key = pick(list(NET_NAME))
        return {"prompt": "This net folds up to make a 3-D shape. What is the shape called? (type its name)",
                "component": "net", "spec": {"solid": key}, "answer": NET_NAME[key], "answer_type": "str",
                "solution": ["The faces of the net fold into a %s." % NET_NAME[key]]}

    def t_faces_net():
        key = pick(["cube", "cuboid", "square_pyramid", "triangular_prism"])
        f = SOLIDS[NET_NAME[key]][0]
        return {"prompt": "This is the net of a 3-D shape. How many faces will the shape have?",
                "component": "net", "spec": {"solid": key}, "answer": f, "answer_type": "int",
                "solution": ["Count the shapes in the net: %d." % f]}

    def t_name():
        name = pick(list(SOLIDS))
        return {"prompt": "What is the name of this 3-D shape? (type its name)", "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": "name"}, "answer": name, "answer_type": "str",
                "solution": ["It is a %s." % name]}

    def t_count():
        name = pick(list(SOLIDS))
        what, i = pick([("faces", 0), ("edges", 1), ("vertices", 2)])
        return {"prompt": "How many %s does this 3-D shape have?" % what, "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": what}, "answer": SOLIDS[name][i], "answer_type": "int",
                "solution": ["A %s has %d %s." % (name, SOLIDS[name][i], what)]}

    def t_describe():
        name, clue = pick([("cube", "6 square faces, all the same size"),
                           ("square-based pyramid", "a square base and 4 triangular faces meeting at a point"),
                           ("triangular prism", "2 triangular ends and 3 rectangular faces"),
                           ("cylinder", "2 circular faces and one curved surface"),
                           ("cone", "1 circular face, one curved surface and a point at the top"),
                           ("sphere", "one curved surface and no edges")])
        return _wq("Which 3-D shape has %s?" % clue, name, ["That describes a %s." % name], "shape name")

    def t_view():
        name, view, ans = pick([("cylinder", "from directly above", "circle"),
                                ("square-based pyramid", "from directly above", "square"),
                                ("cube", "from the front", "square"),
                                ("triangular prism", "from one end", "triangle"),
                                ("cone", "from directly below", "circle")])
        return _wq("A %s stands on a table. What 2-D shape do you see when you look at it %s?" % (name, view), ans,
                   ["Looking %s at a %s shows a %s." % (view, name, ans)], "2-D shape name")

    def t_euler():
        name = pick(list(SOLIDS))
        f, e, v = SOLIDS[name]
        return _tb("A %s has %d faces and %d vertices. How many edges does it have?" % (name, f, v), e, "int", {},
                   ["Faces + vertices − 2 = edges: %d + %d − 2 = %d." % (f, v, e)])

    return _pick_t([t_describe, t_view, t_euler], [t_net, t_faces_net, t_name, t_count])


@skill("Y5.8.b", "Estimate and classify acute, obtuse and reflex angles", S8)
def _(d=1):
    d = _d(d)

    def t_classify_pic():
        deg = pick([random.randint(15, 80), random.randint(100, 170), random.randint(190, 340), 90])
        return {"prompt": "Is this angle acute, right, obtuse or reflex? (type one word)", "component": "angle",
                "spec": {"mode": "classify", "degrees": deg}, "answer": _kind(deg), "answer_type": "str",
                "solution": ["It is %d°, so it is %s." % (deg, _kind(deg))]}

    def t_classify_num():
        deg = random.choice([x for x in range(5, 356) if x not in (90, 180)])
        return _wq("An angle measures %d°. Is it acute, obtuse or reflex?" % deg, _kind(deg),
                   ["Acute < 90° < obtuse < 180° < reflex < 360°."], "acute / obtuse / reflex")

    def t_estimate():
        deg = random.choice([30, 45, 60, 120, 135, 150, 210, 270, 300])
        opts = sorted({deg, pick([d2 for d2 in (20, 45, 80, 100, 160, 200, 250, 320) if abs(d2 - deg) > 30]),
                       pick([d2 for d2 in (10, 70, 110, 170, 230, 290, 340) if abs(d2 - deg) > 30])})
        return {"prompt": "Estimate the size of this angle. Which is closest: %s? Type the number."
                          % ", ".join("%d°" % o for o in opts), "component": "angle",
                "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": deg, "answer_type": "int",
                "solution": ["Compare it with a right angle (90°) and a straight line (180°)."]}

    def t_range():
        kind = pick(["acute", "obtuse", "reflex"])
        ans = {"acute": "0 and 90", "obtuse": "90 and 180", "reflex": "180 and 360"}[kind]
        return _wq("An %s angle is between which two numbers of degrees? Write them like 0 and 90." % kind
                   if kind in ("acute", "obtuse") else "A reflex angle is between which two numbers of degrees? "
                   "Write them like 0 and 90.", ans, ["%s angles are between %s degrees." % (kind.capitalize(), ans)],
                   "e.g. 0 and 90")

    def t_count():
        degs = random.sample([20, 35, 50, 75, 95, 110, 130, 165, 200, 250, 300, 340], 5)
        kind = pick(["acute", "obtuse", "reflex"])
        return _tb("How many of these angles are %s?  %s" % (kind, ", ".join("%d°" % x for x in degs)),
                   sum(1 for x in degs if _kind(x) == kind), "int", {},
                   ["%s: %s." % (kind.capitalize(), ", ".join("%d°" % x for x in degs if _kind(x) == kind) or "none")])

    def t_compare():
        a, b = random.sample([25, 40, 65, 100, 125, 150, 200, 260, 310], 2)
        return _tb("Which angle is larger, %d° or %d°?" % (a, b), max(a, b), "int", {},
                   ["%d° is larger." % max(a, b)])

    return _pick_t([t_classify_num, t_range, t_count, t_compare], [t_classify_pic, t_estimate])


@skill("Y5.8.c", "Measure angles in degrees with a protractor", S8)
def _(d=1):
    d = _d(d)

    def t_measure():
        deg = random.randint(1, 17) * 10 if d == 0 else random.randint(2, 34) * 5
        return {"prompt": "Measure this angle with the protractor. How many degrees is it?", "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True}, "answer": deg, "answer_type": "num",
                "tolerance": 2, "solution": ["Start from 0 on the scale that the first arm crosses.",
                                             "The angle is %d°." % deg]}

    def t_scale_trap():
        deg = random.randint(2, 16) * 10
        return {"prompt": "Measure this angle. Be careful to read the scale that starts at 0 on the horizontal arm. "
                          "How many degrees is it?", "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True}, "answer": deg, "answer_type": "num",
                "tolerance": 2, "solution": ["Reading the other scale would give %d°." % (180 - deg),
                                             "The angle is %d°." % deg]}

    def t_reflex_from_inner():
        inner = random.randint(3, 16) * 10
        return _tb("The inside angle between two arms measures %d°. What is the reflex angle on the other side?"
                   % inner, 360 - inner, "int", {"unit": "°"}, ["360 − %d = %d." % (inner, 360 - inner)])

    def t_difference():
        a, b = random.randint(2, 17) * 10, random.randint(2, 17) * 10
        if a == b:
            b += 10
        return _tb("One angle measures %d° and another measures %d°. What is the difference in degrees?" % (a, b),
                   abs(a - b), "int", {"unit": "°"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    return _pick_t([t_reflex_from_inner, t_difference], [t_measure, t_measure, t_scale_trap])


@skill("Y5.8.d", "Angles at a point and whole turns (360°)", S8)
def _(d=1):
    d = _d(d)

    def t_missing():
        k = _by(d, 2, 3, 4)
        parts = [random.randint(20, 120) for _ in range(k)]
        while sum(parts) >= 340:
            parts = [random.randint(20, 100) for _ in range(k)]
        return _tb("Angles of %s meet at a point with one more angle. How many degrees is the missing angle?"
                   % ", ".join("%d°" % p for p in parts), 360 - sum(parts), "int", {"unit": "°"},
                   ["Angles at a point add up to 360°.", "360 − %d = %d." % (sum(parts), 360 - sum(parts))])

    def t_equal():
        k = pick([3, 4, 5, 6, 8, 9, 10, 12])
        return _tb("%d equal angles meet at a point. How big is each one, in degrees?" % k, 360 // k, "int",
                   {"unit": "°"}, ["360 ÷ %d = %d." % (k, 360 // k)])

    def t_turn():
        f, name = pick([(Fraction(1, 4), "a quarter"), (Fraction(1, 2), "a half"), (Fraction(3, 4), "three quarters"),
                        (Fraction(1, 3), "a third"), (Fraction(1, 8), "an eighth")])
        return _tb("How many degrees is %s of a full turn?" % name, int(360 * f), "int", {"unit": "°"},
                   ["A full turn is 360°.", "%s × 360 = %d." % (_fs(f), int(360 * f))])

    def t_clock():
        h = random.randint(1, 11)
        return _tb("The minute hand of a clock turns from 12 to %d. How many degrees has it turned?" % h, 30 * h,
                   "int", {"unit": "°"}, ["Each hour mark is 360 ÷ 12 = 30°.", "%d × 30 = %d." % (h, 30 * h)])

    def t_pie():
        a, b = random.randint(3, 10) * 10, random.randint(3, 10) * 10
        c = 360 - a - b
        return {"prompt": "A circle is split into three angles at the centre. Two are %d° and %d°. How many degrees "
                          "is the third?" % (a, b), "component": "pie_chart",
                "spec": {"slices": [["A", a], ["B", b], ["C", c]], "mode": "read", "highlight": 2},
                "answer": c, "answer_type": "int", "solution": ["360 − %d − %d = %d." % (a, b, c)]}

    def t_angle_pic():
        deg = random.randint(4, 16) * 10
        return {"prompt": "The angle shown is %d°. What angle would make a full turn with it?" % deg,
                "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 360 - deg,
                "answer_type": "int", "solution": ["360 − %d = %d." % (deg, 360 - deg)]}

    return _pick_t([t_missing, t_equal, t_turn, t_clock], [t_pie, t_angle_pic])


@skill("Y5.8.e", "Angles on a straight line and half turns (180°)", S8)
def _(d=1):
    d = _d(d)

    def t_missing():
        a = random.randint(15, 165)
        return _tb("Two angles sit together on a straight line. One is %d°. How big is the other, in degrees?" % a,
                   180 - a, "int", {"unit": "°"}, ["Angles on a straight line add up to 180°.",
                                                   "180 − %d = %d." % (a, 180 - a)])

    def t_three():
        a, b = random.randint(20, 80), random.randint(20, 80)
        return _tb("Three angles sit on a straight line. Two are %d° and %d°. How big is the third, in degrees?"
                   % (a, b), 180 - a - b, "int", {"unit": "°"}, ["180 − %d − %d = %d." % (a, b, 180 - a - b)])

    def t_equal():
        k = pick([2, 3, 4, 5, 6])
        return _tb("A straight line is split into %d equal angles. How big is each, in degrees?" % k, 180 // k,
                   "int", {"unit": "°"}, ["180 ÷ %d = %d." % (k, 180 // k)])

    def t_half_turn():
        start, opp = pick([("north", "south"), ("east", "west"), ("south", "north"), ("west", "east")])
        return _wq("You face %s and make a half turn. Which way do you face now?" % start, opp,
                   ["A half turn is 180°."], "direction")

    def t_algebra():
        a = random.randint(20, 70)
        return _tb("On a straight line, one angle is twice another and there is a third angle of %d°. "
                   "How big is the smallest of the other two, in degrees? (Hint: 3 equal parts share %d°.)"
                   % (180 - 3 * a, 3 * a), a, "int", {"unit": "°"},
                   ["180 − %d = %d." % (180 - 3 * a, 3 * a), "%d ÷ 3 = %d." % (3 * a, a)]) if 180 - 3 * a > 0 else t_missing()

    def t_pic():
        deg = random.randint(3, 15) * 10
        return {"prompt": "The angle shown is %d°. Together with another angle it makes a straight line. How big is "
                          "the other angle, in degrees?" % deg, "component": "angle",
                "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 180 - deg, "answer_type": "int",
                "solution": ["180 − %d = %d." % (deg, 180 - deg)]}

    return _pick_t([t_missing, t_three, t_equal, t_half_turn, t_algebra], [t_pic])


@skill("Y5.8.f", "Right angles, turns and multiples of 90°", S8)
def _(d=1):
    d = _d(d)
    DIRS = ["north", "east", "south", "west"]

    def t_right_angles():
        k = random.randint(1, 4)
        return _tb("How many degrees are %d right angle%s?" % (k, "" if k == 1 else "s"), 90 * k, "int",
                   {"unit": "°"}, ["%d × 90 = %d." % (k, 90 * k)])

    def t_how_many_right():
        deg = 90 * random.randint(1, 4)
        return _tb("How many right angles make %d°?" % deg, deg // 90, "int", {}, ["%d ÷ 90 = %d." % (deg, deg // 90)])

    def t_compass():
        s = random.randrange(4)
        k = random.randint(1, 3)
        cw = random.random() < 0.5
        end = DIRS[(s + (k if cw else -k)) % 4]
        return _wq("You face %s and turn %d° %s. Which way do you face now?"
                   % (DIRS[s], 90 * k, "clockwise" if cw else "anticlockwise"), end,
                   ["%d° is %d right angle%s." % (90 * k, k, "" if k == 1 else "s")], "direction")

    def t_turn_size():
        s, e = random.sample(range(4), 2)
        k = (e - s) % 4
        return _tb("You face %s and turn clockwise until you face %s. How many degrees have you turned?"
                   % (DIRS[s], DIRS[e]), 90 * k, "int", {"unit": "°"}, ["That is %d quarter turn%s." % (k, "" if k == 1 else "s")])

    def t_turn_pic():
        deg = pick([90, 180, 270, 360])
        return {"prompt": "The arrow shows a turn. How many degrees is it?", "component": "angle",
                "spec": {"mode": "turn", "degrees": deg}, "answer": deg, "answer_type": "int",
                "solution": ["It is %d quarter turn%s: %d°." % (deg // 90, "" if deg == 90 else "s", deg)]}

    def t_is_multiple():
        deg = pick([90, 180, 270, 360, 45, 120, 135, 200])
        return _wq("Is %d° a multiple of 90°? (yes or no)" % deg, "yes" if deg % 90 == 0 else "no",
                   ["%d ÷ 90 %s." % (deg, "is a whole number" if deg % 90 == 0 else "is not a whole number")], "yes / no")

    return _pick_t([t_right_angles, t_how_many_right, t_compass, t_turn_size, t_is_multiple], [t_turn_pic])


@skill("Y5.8.g", "Use properties of rectangles to find missing lengths and angles", S8)
def _(d=1):
    d = _d(d)

    def t_opposite():
        a = random.randint(3, 30)
        return _tb("A rectangle has one side of %d cm. How long is the opposite side, in cm?" % a, a, "int",
                   {"unit": "cm"}, ["Opposite sides of a rectangle are equal."])

    def t_perimeter_side():
        a, b = random.randint(3, 25), random.randint(3, 25)
        return _tb("A rectangle has a perimeter of %d cm. Its length is %d cm. What is its width, in cm?"
                   % (2 * (a + b), a), b, "int", {"unit": "cm"},
                   ["Length + width = %d ÷ 2 = %d." % (2 * (a + b), a + b), "%d − %d = %d." % (a + b, a, b)])

    def t_angle():
        return _tb("What is the size of each angle inside a rectangle, in degrees?", 90, "int", {"unit": "°"},
                   ["All four angles of a rectangle are right angles."])

    def t_diagonal_angle():
        a = random.randint(15, 75)
        return _tb("A diagonal splits a corner of a rectangle into two angles. One is %d°. How big is the other, in "
                   "degrees?" % a, 90 - a, "int", {"unit": "°"}, ["The corner is 90°.", "90 − %d = %d." % (a, 90 - a)])

    def t_square_from_perimeter():
        s = random.randint(3, 25)
        return _tb("A square has a perimeter of %d cm. How long is each side, in cm?" % (4 * s), s, "int",
                   {"unit": "cm"}, ["A square has 4 equal sides: %d ÷ 4 = %d." % (4 * s, s)])

    def t_split():
        W, a = random.randint(12, 30), random.randint(3, 9)
        return _tb("A rectangle %d cm long is cut into two smaller rectangles. One piece is %d cm long. How long is "
                   "the other piece, in cm?" % (W, a), W - a, "int", {"unit": "cm"}, ["%d − %d = %d." % (W, a, W - a)])

    def t_corners():
        return _wq("Is a square a special kind of rectangle? (yes or no)", "yes",
                   ["A square has 4 right angles and opposite sides equal, so it is a rectangle."], "yes / no")

    def t_grid():
        x0, y0 = random.randint(1, 3), random.randint(1, 3)
        w, h = random.randint(2, 5), random.randint(2, 4)
        pts = [[x0, y0, "A"], [x0 + w, y0, "B"], [x0 + w, y0 + h, "C"]]
        return {"prompt": "A, B and C are three corners of a rectangle. Plot the fourth corner.",
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": pts}, "answer": "(%d,%d)" % (x0, y0 + h),
                "answer_type": "coord", "solution": ["Opposite sides are equal and parallel: (%d,%d)." % (x0, y0 + h)]}

    return _pick_t([t_opposite, t_perimeter_side, t_angle, t_diagonal_angle, t_square_from_perimeter, t_split,
                    t_corners], [t_grid])


@skill("Y5.8.h", "Regular and irregular polygons", S8)
def _(d=1):
    d = _d(d)
    POLY = [("triangle", 3), ("quadrilateral", 4), ("pentagon", 5), ("hexagon", 6), ("heptagon", 7),
            ("octagon", 8), ("nonagon", 9), ("decagon", 10)]

    def t_regular():
        name, n = pick(POLY)
        eq_s, eq_a = pick([(True, True), (True, False), (False, True), (False, False)])
        ok = eq_s and eq_a
        return _wq("A %s has %s sides and %s angles. Is it regular? (yes or no)"
                   % (name, "all equal" if eq_s else "unequal", "all equal" if eq_a else "unequal"),
                   "yes" if ok else "no", ["A regular polygon has ALL sides equal AND ALL angles equal."], "yes / no")

    def t_rhombus():
        return _wq("A rhombus has 4 equal sides but its angles are not all equal. Is it a regular polygon? "
                   "(yes or no)", "no", ["Its angles are not all equal, so it is irregular."], "yes / no")

    def t_name():
        name, n = pick(POLY[1:])
        return _wq("What is the name of a polygon with %d sides?" % n, name, ["%d sides: %s." % (n, name)], "name")

    def t_sides():
        name, n = pick(POLY)
        return _tb("How many sides does a %s have?" % name, n, "int", {}, ["A %s has %d sides." % (name, n)])

    def t_perimeter():
        name, n = pick(POLY)
        s = random.randint(3, 15)
        return _tb("A regular %s has sides of %d cm. What is its perimeter, in cm?" % (name, s), n * s, "int",
                   {"unit": "cm"}, ["All %d sides are equal: %d × %d = %d." % (n, n, s, n * s)])

    def t_side_from_perimeter():
        name, n = pick(POLY)
        s = random.randint(3, 15)
        return _tb("A regular %s has a perimeter of %d cm. How long is each side, in cm?" % (name, n * s), s, "int",
                   {"unit": "cm"}, ["%d ÷ %d = %d." % (n * s, n, s)])

    def t_shape():
        name = pick(["triangle", "square", "pentagon", "hexagon", "octagon"])
        n = {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}[name]
        return {"prompt": "This is a regular polygon. How many lines of symmetry does it have?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "lines_of_symmetry"}, "answer": n, "answer_type": "int",
                "solution": ["A regular polygon with %d sides has %d lines of symmetry." % (n, n)]}

    return _pick_t([t_regular, t_rhombus, t_name, t_sides, t_perimeter, t_side_from_perimeter], [t_shape])


def _poly(x0, y0):
    shape = pick([[(0, 0), (2, 0), (2, 1), (0, 1)], [(0, 0), (2, 0), (0, 2)], [(0, 0), (3, 0), (3, 2), (1, 2)],
                  [(0, 0), (1, 0), (1, 2), (0, 2)]])
    return [[x0 + x, y0 + y] for x, y in shape]


@skill("Y5.8.i", "Reflection in a mirror line", S8)
def _(d=1):
    d = _d(d)

    def t_vertical():
        m = random.randint(4, 6)
        poly = _poly(random.randint(0, m - 3), random.randint(1, 6))
        k = random.randrange(len(poly))
        x, y = poly[k]
        pts = [[px, py, "A" if i == k else ""] for i, (px, py) in enumerate(poly) if i == k]
        return {"prompt": "The shape is reflected in the dashed vertical mirror line (x = %d). Plot where corner A "
                          "goes." % m, "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": pts,
                         "lines": [{"p1": [m, 0], "p2": [m, 10], "dashed": True, "label": "mirror"}]},
                "answer": "(%d,%d)" % (2 * m - x, y), "answer_type": "coord",
                "solution": ["A is %d squares left of the mirror, so its image is %d squares right of it." % (m - x, m - x),
                             "(%d,%d)." % (2 * m - x, y)]}

    def t_horizontal():
        m = random.randint(4, 6)
        poly = _poly(random.randint(1, 6), random.randint(0, m - 3))
        k = random.randrange(len(poly))
        x, y = poly[k]
        return {"prompt": "The shape is reflected in the dashed horizontal mirror line (y = %d). Plot where corner A "
                          "goes." % m, "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": [[x, y, "A"]],
                         "lines": [{"p1": [0, m], "p2": [10, m], "dashed": True, "label": "mirror"}]},
                "answer": "(%d,%d)" % (x, 2 * m - y), "answer_type": "coord",
                "solution": ["A is %d squares below the mirror, so its image is %d squares above it." % (m - y, m - y),
                             "(%d,%d)." % (x, 2 * m - y)]}

    def t_words():
        m = random.randint(3, 7)
        x = random.randint(0, m - 1)
        y = random.randint(0, 9)
        return _wq("A point at (%d,%d) is reflected in a vertical mirror line through x = %d. Where does it go? "
                   "Write it like (3,4)." % (x, y, m), "(%d,%d)" % (2 * m - x, y),
                   ["Same distance on the other side: %d − %d = %d, %d + %d = %d." % (m, x, m - x, m, m - x, 2 * m - x)],
                   "(x,y)")

    def t_unchanged():
        what = pick(["the length of its sides", "the size of its angles", "its area"])
        return _wq("When a shape is reflected, does %s change? (yes or no)" % what, "no",
                   ["Reflection makes a mirror image the same size and shape."], "yes / no")

    def t_distance():
        a = random.randint(1, 6)
        return _tb("A point is %d squares to the left of a mirror line. How far is its reflection from the point, in "
                   "squares?" % a, 2 * a, "int", {"unit": "squares"}, ["%d to the mirror and %d back: %d." % (a, a, 2 * a)])

    return _pick_t([t_words, t_unchanged, t_distance], [t_vertical, t_horizontal])


@skill("Y5.8.j", "Translation on a grid", S8)
def _(d=1):
    d = _d(d)

    def _move():
        dx, dy = random.randint(-4, 4), random.randint(-4, 4)
        while dx == 0 and dy == 0:
            dx, dy = random.randint(-4, 4), random.randint(-4, 4)
        return dx, dy

    def _say(dx, dy):
        parts = []
        if dx:
            parts.append("%d %s" % (abs(dx), "right" if dx > 0 else "left"))
        if dy:
            parts.append("%d %s" % (abs(dy), "up" if dy > 0 else "down"))
        return " and ".join(parts)

    def t_plot():
        dx, dy = _move()
        x0, y0 = random.randint(max(0, -dx), min(7, 7 - dx)), random.randint(max(0, -dy), min(7, 7 - dy))
        poly = _poly(x0, y0)
        poly = [[min(max(x, 0), 10), min(max(y, 0), 10)] for x, y in poly]
        k = random.randrange(len(poly))
        x, y = poly[k]
        if not (0 <= x + dx <= 10 and 0 <= y + dy <= 10):
            dx, dy = -dx, -dy
        if not (0 <= x + dx <= 10 and 0 <= y + dy <= 10):
            return t_words()
        return {"prompt": "The shape is translated %s. Plot where corner A goes." % _say(dx, dy),
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": [[x, y, "A"]]},
                "answer": "(%d,%d)" % (x + dx, y + dy), "answer_type": "coord",
                "solution": ["(%d,%d) moves %s to (%d,%d)." % (x, y, _say(dx, dy), x + dx, y + dy)]}

    def t_words():
        dx, dy = _move()
        x, y = random.randint(4, 6), random.randint(4, 6)
        return _wq("The point (%d,%d) is translated %s. Where does it go? Write it like (3,4)." % (x, y, _say(dx, dy)),
                   "(%d,%d)" % (x + dx, y + dy), ["Add %d to x and %d to y." % (dx, dy)], "(x,y)")

    def t_describe():
        dx, dy = _move()
        if dx == 0 or dy == 0:
            dx, dy = (dx or 2), (dy or 3)
        x, y = random.randint(4, 6), random.randint(4, 6)
        return _tb("A point moves from (%d,%d) to (%d,%d). How many squares does it move %s?"
                   % (x, y, x + dx, y + dy, "right" if dx > 0 else "left"), abs(dx), "int", {},
                   ["The x-coordinate changes by %d." % dx])

    def t_back():
        dx, dy = _move()
        x, y = random.randint(4, 6), random.randint(4, 6)
        return _wq("After a translation %s, a point is at (%d,%d). Where did it start? Write it like (3,4)."
                   % (_say(dx, dy), x, y), "(%d,%d)" % (x - dx, y - dy), ["Undo the move: (%d,%d)." % (x - dx, y - dy)],
                   "(x,y)")

    def t_same():
        return _wq("After a translation, is the shape the same size and the same way round? (yes or no)", "yes",
                   ["A translation only slides the shape."], "yes / no")

    return _pick_t([t_words, t_describe, t_back, t_same], [t_plot, t_plot])


# ================================================================== 5.9 ======
def _temps():
    hrs = ["8 am", "9 am", "10 am", "11 am", "12 pm", "1 pm"]
    v = random.randint(4, 12)
    vals = []
    for _ in hrs:
        vals.append(v)
        v = max(0, v + random.randint(-2, 4))
    return hrs, vals


@skill("Y5.9.a", "Read and interpret line graphs", S9)
def _(d=1):
    d = _d(d)
    hrs, vals = _temps()

    def t_read():
        k = random.randrange(len(hrs))
        return _lg("Temperature in the playground. What was the temperature at %s, in °C?" % hrs[k],
                   list(zip(hrs, vals)), vals[k], ["Read up from %s to the line: %d °C." % (hrs[k], vals[k])], "°C", "Time")

    def t_highest():
        top = max(vals)
        return _lg("Temperature in the playground. What was the highest temperature, in °C?", list(zip(hrs, vals)), top,
                   ["The highest point is %d °C." % top], "°C", "Time")

    def t_when():
        top = max(vals)
        if vals.count(top) > 1:
            return t_read()
        return _lg("Temperature in the playground. At what time was it warmest? (type the time, like 10 am)",
                   list(zip(hrs, vals)), hrs[vals.index(top)], ["The highest point is at %s." % hrs[vals.index(top)]],
                   "°C", "Time", atype="str")

    def t_rise():
        k = random.randrange(len(hrs) - 1)
        ch = vals[k + 1] - vals[k]
        if ch == 0:
            return t_read()
        return _lg("Temperature in the playground. Between %s and %s, did the temperature rise or fall? (type rise or "
                   "fall)" % (hrs[k], hrs[k + 1]), list(zip(hrs, vals)), "rise" if ch > 0 else "fall",
                   ["%d °C to %d °C." % (vals[k], vals[k + 1])], "°C", "Time", atype="str")

    def t_plant():
        weeks = ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5"]
        h = sorted(random.sample(range(2, 40), 5))
        k = random.randrange(5)
        return _lg("The graph shows the height of a sunflower. How tall was it in %s, in cm?" % weeks[k],
                   list(zip(weeks, h)), h[k], ["Read across: %d cm." % h[k]], "cm", "Week")

    return _pick_t([], [t_read, t_highest, t_when, t_rise, t_plant])


@skill("Y5.9.b", "Comparison, sum and difference problems from line graphs", S9)
def _(d=1):
    d = _d(d)
    hrs, vals = _temps()

    def t_diff():
        i, j = random.sample(range(len(hrs)), 2)
        return _lg("Temperature in the playground. What is the difference between the temperatures at %s and %s, in "
                   "degrees?" % (hrs[i], hrs[j]), list(zip(hrs, vals)), abs(vals[i] - vals[j]),
                   ["%d and %d: difference %d." % (vals[i], vals[j], abs(vals[i] - vals[j]))], "°C", "Time")

    def t_range():
        return _lg("Temperature in the playground. How many degrees warmer was the warmest reading than the coldest?",
                   list(zip(hrs, vals)), max(vals) - min(vals),
                   ["%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))], "°C", "Time")

    def t_sales_sum():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        s = [random.randint(5, 40) for _ in days]
        i, j = random.sample(range(5), 2)
        return _lg("The graph shows ice creams sold each day. How many were sold on %s and %s altogether?"
                   % (days[i], days[j]), list(zip(days, s)), s[i] + s[j],
                   ["%d + %d = %d." % (s[i], s[j], s[i] + s[j])], "Ice creams", "Day")

    def t_biggest_rise():
        rises = [vals[k + 1] - vals[k] for k in range(len(vals) - 1)]
        top = max(rises)
        if rises.count(top) > 1 or top <= 0:
            return t_diff()
        k = rises.index(top)
        return _lg("Temperature in the playground. Between which two times did the temperature rise the most? Type the "
                   "EARLIER time (like 9 am).", list(zip(hrs, vals)), hrs[k],
                   ["%s to %s: up %d degrees." % (hrs[k], hrs[k + 1], top)], "°C", "Time", atype="str")

    def t_total():
        days = ["Mon", "Tue", "Wed", "Thu"]
        s = [random.randint(5, 30) for _ in days]
        return _lg("The graph shows books borrowed each day. How many books were borrowed altogether?",
                   list(zip(days, s)), sum(s), ["%s = %d." % (" + ".join(map(str, s)), sum(s))], "Books", "Day")

    def t_two_lines_words():
        days = ["Mon", "Tue", "Wed"]
        a, b = [random.randint(10, 30) for _ in days], [random.randint(10, 30) for _ in days]
        k = random.randrange(3)
        return _dt("Two shops recorded their sales. What is the difference between the two shops' sales on %s?"
                   % days[k], ["Day", "Shop A", "Shop B"],
                   [[dd, x, y] for dd, x, y in zip(days, a, b)], abs(a[k] - b[k]),
                   ["%d − %d = %d." % (max(a[k], b[k]), min(a[k], b[k]), abs(a[k] - b[k]))])

    return _pick_t([t_two_lines_words], [t_diff, t_range, t_sales_sum, t_biggest_rise, t_total])


@skill("Y5.9.c", "Complete, read and interpret tables", S9)
def _(d=1):
    d = _d(d)

    def t_total_col():
        clubs = ["Football", "Art", "Chess", "Music"]
        boys = [random.randint(3, 20) for _ in clubs]
        girls = [random.randint(3, 20) for _ in clubs]
        rows = [[c, b, g, b + g] for c, b, g in zip(clubs, boys, girls)]
        k = random.randrange(4)
        return _dt("The table shows how many boys and girls go to each club. What number belongs in the empty cell?",
                   ["Club", "Boys", "Girls", "Total"], rows, boys[k] + girls[k],
                   ["%d + %d = %d." % (boys[k], girls[k], boys[k] + girls[k])], missing=[k, 3])

    def t_missing_part():
        clubs = ["Football", "Art", "Chess"]
        boys = [random.randint(3, 20) for _ in clubs]
        girls = [random.randint(3, 20) for _ in clubs]
        rows = [[c, b, g, b + g] for c, b, g in zip(clubs, boys, girls)]
        k = random.randrange(3)
        return _dt("Complete the table. How many girls go to %s?" % clubs[k], ["Club", "Boys", "Girls", "Total"],
                   rows, girls[k], ["%d − %d = %d." % (boys[k] + girls[k], boys[k], girls[k])], missing=[k, 2])

    def t_read_compare():
        pets = ["Dog", "Cat", "Fish", "Rabbit"]
        y5 = [random.randint(2, 15) for _ in pets]
        y6 = [random.randint(2, 15) for _ in pets]
        k = random.randrange(4)
        return _dt("The table shows the pets owned by Year 5 and Year 6. How many %s are there altogether?"
                   % {"Dog": "dogs", "Cat": "cats", "Fish": "fish", "Rabbit": "rabbits"}[pets[k]], ["Pet", "Year 5", "Year 6"], [[p, a, b] for p, a, b in zip(pets, y5, y6)],
                   y5[k] + y6[k], ["%d + %d = %d." % (y5[k], y6[k], y5[k] + y6[k])])

    def t_most():
        cities = ["Leeds", "York", "Hull", "Bath"]
        rain = random.sample(range(20, 120), 4)
        return _dt("The table shows rainfall in mm. Which city had the most rain?", ["City", "Rainfall (mm)"],
                   [[c, r] for c, r in zip(cities, rain)], cities[rain.index(max(rain))],
                   ["The largest is %d mm." % max(rain)], atype="str")

    def t_column_total():
        items = ["Pens", "Pencils", "Rulers"]
        q = [random.randint(10, 90) for _ in items]
        rows = [[i, x] for i, x in zip(items, q)] + [["Total", sum(q)]]
        return _dt("The table shows stock in a cupboard. What is the total?", ["Item", "Number"], rows, sum(q),
                   ["%s = %d." % (" + ".join(map(str, q)), sum(q))], missing=[3, 1])

    return _pick_t([], [t_total_col, t_missing_part, t_read_compare, t_most, t_column_total])


@skill("Y5.9.d", "Read and use timetables", S9)
def _(d=1):
    d = _d(d)
    stops = ["Bridge St", "Park Rd", "Market", "Station"]
    gaps = [random.randint(5, 20) for _ in range(3)]
    starts = sorted(random.sample(range(7 * 60, 11 * 60, 5), 3))

    def _t(m):
        return "%02d:%02d" % divmod(m, 60)

    rows = []
    for i, s in enumerate(stops):
        off = sum(gaps[:i])
        rows.append([s] + [_t(b + off) for b in starts])
    headers = ["Stop", "Bus 1", "Bus 2", "Bus 3"]

    def t_journey():
        a, b = sorted(random.sample(range(4), 2))
        mins = sum(gaps[a:b])
        return _dt("Use the bus timetable. How many minutes does it take to go from %s to %s?" % (stops[a], stops[b]),
                   headers, rows, mins, ["%s to %s on any bus: %d minutes." % (stops[a], stops[b], mins)])

    def t_arrive():
        k = random.randrange(3)
        return _dt("Use the bus timetable. Bus %d leaves Bridge St at %s. At what time does it reach the Station? "
                   "(type it like 09:45)" % (k + 1, _t(starts[k])), headers, rows, _t(starts[k] + sum(gaps)),
                   ["Read down the Bus %d column." % (k + 1)], atype="time")

    def t_catch():
        k = random.randrange(3)
        arrive = starts[k] - random.randint(1, 9)
        if k > 0 and arrive <= starts[k - 1]:
            arrive = starts[k - 1] + 1
        who = _who()
        return _dt("Use the bus timetable. %s gets to Bridge St at %s. Which bus is the first one %s can catch? (type "
                   "1, 2 or 3)" % (who, _t(arrive), who), headers, rows, k + 1,
                   ["The next bus to leave after %s is Bus %d." % (_t(arrive), k + 1)])

    def t_wait():
        k = random.randint(1, 2)
        return _dt("Use the bus timetable. How many minutes after Bus %d does Bus %d leave Bridge St?" % (k, k + 1),
                   headers, rows, starts[k] - starts[k - 1],
                   ["%s to %s is %d minutes." % (_t(starts[k - 1]), _t(starts[k]), starts[k] - starts[k - 1])])

    def t_late():
        late = random.randint(3, 15)
        k = random.randrange(3)
        return _dt("Use the bus timetable. Bus %d is %d minutes late at every stop. At what time does it reach Market? "
                   "(type it like 09:45)" % (k + 1, late), headers, rows, _t(starts[k] + sum(gaps[:2]) + late),
                   ["%s + %d minutes." % (_t(starts[k] + sum(gaps[:2])), late)], atype="time")

    return _pick_t([], [t_journey, t_arrive, t_catch, t_wait, t_late])
