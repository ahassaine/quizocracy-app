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
    # easy: the familiar cube, cuboid and cylinder; hard: pyramids and prisms, and edges/vertices rather than faces
    EASY3, HARD3 = ["cube", "cuboid"], ["square-based pyramid", "triangular prism"]

    def t_net():
        key = pick(_by(d, ["cube", "cuboid", "cylinder"], list(NET_NAME),
                       ["square_pyramid", "triangular_prism", "cone", "cylinder"]))
        return {"prompt": "This net folds up to make a 3-D shape. What is the shape called? (type its name)",
                "component": "net", "spec": {"solid": key}, "answer": NET_NAME[key], "answer_type": "str",
                "solution": ["The faces of the net fold into a %s." % NET_NAME[key]]}

    def t_faces_net():
        key = pick(_by(d, ["cube", "cuboid"], ["cube", "cuboid", "square_pyramid", "triangular_prism"],
                       ["square_pyramid", "triangular_prism"]))
        f = SOLIDS[NET_NAME[key]][0]
        return {"prompt": "This is the net of a 3-D shape. How many faces will the shape have?",
                "component": "net", "spec": {"solid": key}, "answer": f, "answer_type": "int",
                "solution": ["Count the shapes in the net: %d." % f]}

    def t_name():
        name = pick(_by(d, EASY3, list(SOLIDS), HARD3))
        return {"prompt": "What is the name of this 3-D shape? (type its name)", "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": "name"}, "answer": name, "answer_type": "str",
                "solution": ["It is a %s." % name]}

    def t_count():
        name = pick(_by(d, EASY3, list(SOLIDS), HARD3))
        what, i = pick(_by(d, [("faces", 0), ("vertices", 2)], [("faces", 0), ("edges", 1), ("vertices", 2)],
                           [("edges", 1), ("vertices", 2)]))
        return {"prompt": "How many %s does this 3-D shape have?" % what, "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": what}, "answer": SOLIDS[name][i], "answer_type": "int",
                "solution": ["A %s has %d %s." % (name, SOLIDS[name][i], what)]}

    def t_describe():
        clues = [("cube", "6 square faces, all the same size"),
                 ("square-based pyramid", "a square base and 4 triangular faces meeting at a point"),
                 ("triangular prism", "2 triangular ends and 3 rectangular faces"),
                 ("cylinder", "2 circular faces and one curved surface"),
                 ("cone", "1 circular face, one curved surface and a point at the top"),
                 ("sphere", "one curved surface and no edges")]
        if d == 2:                                     # hard: described by its counts, not its faces' shapes
            clues = [("triangular prism", "5 faces, 9 edges and 6 vertices"),
                     ("square-based pyramid", "5 faces, 8 edges and 5 vertices"),
                     ("cuboid", "6 rectangular faces, 12 edges and 8 vertices"),
                     ("cone", "one flat face, one curved surface and one vertex")]
        name, clue = pick([clues[0], clues[3], clues[5]] if d == 0 else clues)
        return _wq("Which 3-D shape has %s?" % clue, name, ["That describes a %s." % name], "shape name")

    def t_view():
        views = [("cylinder", "from directly above", "circle"),
                 ("square-based pyramid", "from directly above", "square"),
                 ("cube", "from the front", "square"),
                 ("triangular prism", "from one end", "triangle"),
                 ("cone", "from directly below", "circle")]
        if d == 2:
            views = [("triangular prism", "from directly above (it rests on one of its rectangular faces)", "rectangle"),
                     ("cylinder", "from the side", "rectangle"),
                     ("cone", "from the side", "triangle"),
                     ("square-based pyramid", "from the front", "triangle")]
        name, view, ans = pick(views[::2] if d == 0 else views)
        return _wq("A %s stands on a table. What 2-D shape do you see when you look at it %s?" % (name, view), ans,
                   ["Looking %s at a %s shows a %s." % (view, name, ans)], "2-D shape name")

    def t_euler():
        name = pick(_by(d, EASY3, list(SOLIDS), HARD3))
        f, e, v = SOLIDS[name]
        if d == 2:                                     # hard: the vertices from faces and edges
            return _tb("A %s has %d faces and %d edges. How many vertices does it have?" % (name, f, e), v, "int", {},
                       ["Edges − faces + 2 = vertices: %d − %d + 2 = %d." % (e, f, v)])
        return _tb("A %s has %d faces and %d vertices. How many edges does it have?" % (name, f, v), e, "int", {},
                   ["Faces + vertices − 2 = edges: %d + %d − 2 = %d." % (f, v, e)])

    return _pick_t([t_describe, t_view, t_euler], [t_net, t_faces_net, t_name, t_count])


@skill("Y5.8.b", "Estimate and classify acute, obtuse and reflex angles", S8)
def _(d=1):
    d = _d(d)

    def t_classify_pic():
        # easy: well clear of 90° and 180°; hard: close to them, where the eye is easily fooled
        deg = pick([random.randint(*_by(d, (20, 70), (15, 80), (78, 89))),
                    random.randint(*_by(d, (110, 160), (100, 170), (91, 104))),
                    random.randint(*_by(d, (200, 330), (190, 340), (181, 195))),
                    90 if d < 2 else random.randint(166, 179)])
        return {"prompt": "Is this angle acute, right, obtuse or reflex? (type one word)", "component": "angle",
                "spec": {"mode": "classify", "degrees": deg}, "answer": _kind(deg), "answer_type": "str",
                "solution": ["It is %d°, so it is %s." % (deg, _kind(deg))]}

    def t_classify_num():
        far = lambda x: min(abs(x - 90), abs(x - 180), 360 - x)     # distance to the nearest boundary
        deg = random.choice([x for x in range(5, 356) if x not in (90, 180) and _by(d, far(x) >= 15, True, far(x) <= 12)])
        return _wq("An angle measures %d°. Is it acute, obtuse or reflex?" % deg, _kind(deg),
                   ["Acute < 90° < obtuse < 180° < reflex < 360°."], "acute / obtuse / reflex")

    def t_estimate():
        deg = random.choice(_by(d, [45, 135, 270], [30, 45, 60, 120, 135, 150, 210, 270, 300],
                                [30, 60, 120, 150, 210, 300]))
        gap = _by(d, 60, 30, 15)                       # how far the wrong options are from the true size
        opts = sorted({deg, pick([d2 for d2 in (20, 45, 80, 100, 160, 200, 250, 320) if abs(d2 - deg) > gap]),
                       pick([d2 for d2 in (10, 70, 110, 170, 230, 290, 340) if abs(d2 - deg) > gap])})
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
        degs = random.sample(_by(d, [20, 30, 45, 60, 120, 135, 150, 210, 240, 270, 300, 330],
                                 [20, 35, 50, 75, 95, 110, 130, 165, 200, 250, 300, 340],
                                 [85, 89, 91, 95, 170, 179, 181, 190, 265, 275, 350, 355]), _by(d, 4, 5, 6))
        kind = pick(["acute", "obtuse", "reflex"])
        return _tb("How many of these angles are %s?  %s" % (kind, ", ".join("%d°" % x for x in degs)),
                   sum(1 for x in degs if _kind(x) == kind), "int", {},
                   ["%s: %s." % (kind.capitalize(), ", ".join("%d°" % x for x in degs if _kind(x) == kind) or "none")])

    def t_compare():
        a, b = random.sample(_by(d, [25, 40, 65, 100, 125, 150, 200, 260, 310],
                                 [25, 40, 65, 100, 125, 150, 200, 260, 310],
                                 [85, 95, 175, 185, 265, 275, 345, 355]), 2)
        return _tb("Which angle is larger, %d° or %d°?" % (a, b), max(a, b), "int", {},
                   ["%d° is larger." % max(a, b)])

    def t_clock():
        h = pick(_by(d, [1, 2, 3, 6], [1, 2, 3, 4, 5, 6, 7, 8], [4, 5, 7, 8, 9, 10, 11]))
        deg = 30 * min(h, 12 - h)
        kind = _kind(deg)
        return _wq("At %d o'clock, what kind of angle do the hands make on the inside (the smaller angle)? (acute, right, "
                   "obtuse or straight)" % h, kind, ["Each hour mark is 30°: the hands are %d° apart." % deg],
                   "acute / right / obtuse / straight")

    def t_turn_kind():
        turns = [(1, "a quarter turn", 90), (2, "a half turn", 180), (3, "three quarters of a turn", 270),
                 (0, "a third of a turn", 120), (0, "an eighth of a turn", 45)]
        if d == 2:
            turns = [(0, "a third of a turn", 120), (0, "an eighth of a turn", 45), (0, "two thirds of a turn", 240),
                     (0, "three eighths of a turn", 135), (0, "five eighths of a turn", 225)]
        f, name, deg = pick(turns[:3] if d == 0 else turns)
        return _wq("What kind of angle is %s: acute, right, obtuse, straight or reflex?" % name, _kind(deg),
                   ["%s is %d°." % (name.capitalize(), deg)], "angle type")

    def t_shape_angle():
        name, kind = pick(_by(d, [("square", "right"), ("equilateral triangle", "acute"), ("rectangle", "right")],
                              [("square", "right"), ("regular hexagon", "obtuse"), ("equilateral triangle", "acute"),
                               ("regular octagon", "obtuse"), ("rectangle", "right")],
                              [("regular pentagon", "obtuse"), ("regular hexagon", "obtuse"), ("regular octagon", "obtuse"),
                               ("equilateral triangle", "acute"), ("regular decagon", "obtuse")]))
        return _wq("What kind of angle is each inside corner of %s %s? (acute, right or obtuse)" % ("an" if name[0] in "aeiou" else "a", name), kind,
                   ["The inside angles of %s %s are %s." % ("an" if name[0] in "aeiou" else "a", name, kind)], "acute / right / obtuse")

    return _pick_t([t_classify_num, t_range, t_count, t_compare, t_clock, t_turn_kind, t_shape_angle],
                   [t_classify_pic, t_estimate])


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

    def t_two_readings():
        a = random.randint(1, 8) * 10
        b = a + random.randint(3, 10) * 10
        if b > 180:
            b = 180
        return _tb("A protractor is placed on an angle. One arm crosses the scale at %d° and the other arm crosses the same "
                   "scale at %d°. How big is the angle?" % (a, b), b - a, "int", {"unit": "°"},
                   ["Count from %d to %d: %d − %d = %d." % (a, b, b, a, b - a)])

    def t_reflex_pic():
        deg = random.randint(3, 16) * 10
        return {"prompt": "Measure the angle shown. Then work out the reflex angle that goes the other way round. How big "
                          "is the reflex angle?", "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True}, "answer": 360 - deg,
                "answer_type": "num", "tolerance": 2,
                "solution": ["The angle shown is %d°." % deg, "360 − %d = %d." % (deg, 360 - deg)]}

    def t_wrong_scale():
        deg = random.randint(2, 16) * 10
        return _tb("%s measured an angle and read %d°, but used the wrong scale on the protractor. What is the real size of "
                   "the angle?" % (_who(), 180 - deg), deg, "int", {"unit": "°"},
                   ["The two scales add up to 180°: 180 − %d = %d." % (180 - deg, deg)])

    def t_between():
        a, b = random.sample([20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170], 2)
        lo_, hi_ = min(a, b), max(a, b)
        return _tb("How many degrees bigger is an angle of %d° than an angle of %d°?" % (hi_, lo_), hi_ - lo_, "int",
                   {"unit": "°"}, ["%d − %d = %d." % (hi_, lo_, hi_ - lo_)])

    def t_possible():
        deg = random.randint(2, 17) * 10 + pick([0, 5])
        claim = pick(["acute", "obtuse"])
        ok = _kind(deg) == claim
        return _wq("%s measures an angle as %d° and says it is %s. Could that be right? (yes or no)"
                   % (_who(), deg, claim), "yes" if ok else "no", ["%d° is %s." % (deg, _kind(deg))], "yes / no")

    def t_halfway_mark():
        a = random.randint(1, 16) * 10
        return _tb("An arm of an angle points exactly halfway between the %d° mark and the %d° mark on a protractor. What "
                   "reading is that, in degrees?" % (a, a + 10), a + 5, "int", {"unit": "°"},
                   ["Halfway between %d and %d is %d." % (a, a + 10, a + 5)])

    def t_right_split():
        a = random.randint(10, 80)
        return _tb("A right angle is split into two angles. One is measured as %d°. How big is the other, in degrees?" % a,
                   90 - a, "int", {"unit": "°"}, ["90 − %d = %d." % (a, 90 - a)])

    def t_sum_measured():
        a, b = random.randint(2, 9) * 10, random.randint(2, 9) * 10 + 5
        return _tb("Two angles next to each other are measured as %d° and %d°. How big is the angle they make together, in "
                   "degrees?" % (a, b), a + b, "int", {"unit": "°"}, ["%d + %d = %d." % (a, b, a + b)])

    return _pick_t([t_reflex_from_inner, t_difference, t_two_readings, t_wrong_scale, t_between, t_possible,
                    t_halfway_mark, t_right_split, t_sum_measured],
                   [t_measure, t_measure, t_scale_trap, t_reflex_pic])


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

    def _ang(lo, hi):
        # easy: whole tens; medium: any whole number; hard: never a multiple of 5
        if d == 0:
            return random.randint(-(-lo // 10), hi // 10) * 10
        a = random.randint(lo, hi)
        if d == 2 and a % 5 == 0:
            a += pick([-2, -1, 1, 2])
        return a

    def t_missing():
        a = _ang(15, 165)
        return _tb("Two angles sit together on a straight line. One is %d°. How big is the other, in degrees?" % a,
                   180 - a, "int", {"unit": "°"}, ["Angles on a straight line add up to 180°.",
                                                   "180 − %d = %d." % (a, 180 - a)])

    def t_three():
        a, b = _ang(20, 80), _ang(20, _by(d, 80, 80, 95))
        return _tb("Three angles sit on a straight line. Two are %d° and %d°. How big is the third, in degrees?"
                   % (a, b), 180 - a - b, "int", {"unit": "°"}, ["180 − %d − %d = %d." % (a, b, 180 - a - b)])

    def t_equal():
        k = pick(_by(d, [2, 3, 4], [2, 3, 4, 5, 6], [5, 6, 9, 10, 12]))
        return _tb("A straight line is split into %d equal angles. How big is each, in degrees?" % k, 180 // k,
                   "int", {"unit": "°"}, ["180 ÷ %d = %d." % (k, 180 // k)])

    def t_half_turn():
        start, opp = pick([("north", "south"), ("east", "west"), ("south", "north"), ("west", "east")])
        return _wq("You face %s and make a half turn. Which way do you face now?" % start, opp,
                   ["A half turn is 180°."], "direction")

    def t_algebra():
        if d == 2:                                     # hard: three times, so 4 equal parts
            a = random.randint(10, 40)
            return _tb("On a straight line, one angle is three times another and there is a third angle of %d°. "
                       "How big is the smallest of the other two, in degrees? (Hint: 4 equal parts share %d°.)"
                       % (180 - 4 * a, 4 * a), a, "int", {"unit": "°"},
                       ["180 − %d = %d." % (180 - 4 * a, 4 * a), "%d ÷ 4 = %d." % (4 * a, a)]) if 180 - 4 * a > 0 \
                else t_missing()
        a = random.randint(2, 5) * 10 if d == 0 else random.randint(20, 70)
        return _tb("On a straight line, one angle is twice another and there is a third angle of %d°. "
                   "How big is the smallest of the other two, in degrees? (Hint: 3 equal parts share %d°.)"
                   % (180 - 3 * a, 3 * a), a, "int", {"unit": "°"},
                   ["180 − %d = %d." % (180 - 3 * a, 3 * a), "%d ÷ 3 = %d." % (3 * a, a)]) if 180 - 3 * a > 0 else t_missing()

    def t_pic():
        deg = random.randint(*_by(d, (3, 15), (3, 15), (5, 31))) * _by(d, 10, 10, 5)
        return {"prompt": "The angle shown is %d°. Together with another angle it makes a straight line. How big is "
                          "the other angle, in degrees?" % deg, "component": "angle",
                "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 180 - deg, "answer_type": "int",
                "solution": ["180 − %d = %d." % (deg, 180 - deg)]}

    def t_four():
        a, b, c = _ang(15, 50), _ang(15, 50), _ang(15, 50)
        return _tb("Four angles sit together on a straight line. Three of them are %d°, %d° and %d°. How big is the fourth, "
                   "in degrees?" % (a, b, c), 180 - a - b - c, "int", {"unit": "°"},
                   ["180 − %d − %d − %d = %d." % (a, b, c, 180 - a - b - c)])

    def t_check():
        a = random.randint(20, 160)
        a = random.randint(2, 16) * 10 if d == 0 else a
        b = 180 - a + pick(_by(d, [0, 0, -20, 20], [0, 0, -10, 10, -5, 5], [0, 0, -2, 2, -1, 1]))
        return _wq("Could angles of %d° and %d° sit together on a straight line? (yes or no)" % (a, b),
                   "yes" if a + b == 180 else "no", ["%d + %d = %d; a straight line is 180°." % (a, b, a + b)], "yes / no")

    def t_table():
        rows = []
        for _ in range(3):
            x = _ang(15, 165)
            rows.append([x, 180 - x])
        k = random.randrange(3)
        c = pick([0, 1])
        ans = rows[k][c]
        return _dt("Each row shows two angles that sit together on a straight line. What angle belongs in the empty cell, "
                   "in degrees?", ["Angle A (°)", "Angle B (°)"], rows, ans,
                   ["180 − %d = %d." % (rows[k][1 - c], ans)], missing=[k, c])

    def t_vertically():
        a = _ang(20, 160)
        return _tb("Two straight lines cross. One of the four angles they make is %d°. The angle next to it on the same line "
                   "is how many degrees?" % a, 180 - a, "int", {"unit": "°"}, ["They sit on a straight line: 180 − %d = %d." % (a, 180 - a)])

    return _pick_t([t_missing, t_three, t_equal, t_half_turn, t_algebra, t_four, t_check, t_vertically],
                   [t_pic, t_table])


@skill("Y5.8.f", "Right angles, turns and multiples of 90°", S8)
def _(d=1):
    d = _d(d)
    DIRS = ["north", "east", "south", "west"]

    def t_right_angles():
        k = random.randint(*_by(d, (1, 2), (1, 4), (3, 8)))
        return _tb("How many degrees %s %s?" % ("is" if k == 1 else "are", _pl(k, "right angle")), 90 * k, "int",
                   {"unit": "°"}, ["%d × 90 = %d." % (k, 90 * k)])

    def t_how_many_right():
        deg = 90 * random.randint(*_by(d, (1, 2), (1, 4), (3, 8)))
        return _tb("How many right angles make %d°?" % deg, deg // 90, "int", {}, ["%d ÷ 90 = %d." % (deg, deg // 90)])

    def t_compass():
        s = random.randrange(4)
        k = random.randint(1, _by(d, 2, 3, 3))
        cw = random.random() < 0.5
        end = DIRS[(s + (k if cw else -k)) % 4]
        if d == 2:                                     # hard: two turns, opposite ways
            k2 = random.randint(1, 3)
            end = DIRS[(s + (k - k2 if cw else k2 - k)) % 4]
            way, back = ("clockwise", "anticlockwise") if cw else ("anticlockwise", "clockwise")
            return _wq("You face %s. You turn %d° %s, then %d° %s. Which way do you face now?"
                       % (DIRS[s], 90 * k, way, 90 * k2, back), end,
                       ["%d° is %d right angle%s and %d° is %d." % (90 * k, k, "" if k == 1 else "s", 90 * k2, k2),
                        "Overall you turn %s %s, so you face %s." % (_pl(abs(k - k2), "right angle"),
                                                                  way if k >= k2 else back, end)], "direction")
        return _wq("You face %s and turn %d° %s. Which way do you face now?"
                   % (DIRS[s], 90 * k, "clockwise" if cw else "anticlockwise"), end,
                   ["%d° is %d right angle%s." % (90 * k, k, "" if k == 1 else "s")], "direction")

    def t_turn_size():
        s, e = random.sample(range(4), 2)
        k = (e - s) % 4
        if d == 2:                                     # hard: anticlockwise
            k = (s - e) % 4
            return _tb("You face %s and turn anticlockwise until you face %s. How many degrees have you turned?"
                       % (DIRS[s], DIRS[e]), 90 * k, "int", {"unit": "°"},
                       ["That is %d quarter turn%s anticlockwise." % (k, "" if k == 1 else "s")])
        if d == 0 and k != 1:                          # easy: one quarter turn clockwise
            e = (s + 1) % 4
            k = 1
        return _tb("You face %s and turn clockwise until you face %s. How many degrees have you turned?"
                   % (DIRS[s], DIRS[e]), 90 * k, "int", {"unit": "°"}, ["That is %d quarter turn%s." % (k, "" if k == 1 else "s")])

    def t_turn_pic():
        deg = pick(_by(d, [90, 180], [90, 180, 270, 360], [270, 360]))
        return {"prompt": "The arrow shows a turn. How many degrees is it?", "component": "angle",
                "spec": {"mode": "turn", "degrees": deg}, "answer": deg, "answer_type": "int",
                "solution": ["It is %d quarter turn%s: %d°." % (deg // 90, "" if deg == 90 else "s", deg)]}

    def t_is_multiple():
        deg = pick(_by(d, [90, 180, 45, 100], [90, 180, 270, 360, 45, 120, 135, 200],
                       [450, 540, 630, 720, 135, 225, 300, 400]))
        return _wq("Is %d° a multiple of 90°? (yes or no)" % deg, "yes" if deg % 90 == 0 else "no",
                   ["%d ÷ 90 %s." % (deg, "is a whole number" if deg % 90 == 0 else "is not a whole number")], "yes / no")

    return _pick_t([t_right_angles, t_how_many_right, t_compass, t_turn_size, t_is_multiple], [t_turn_pic])


@skill("Y5.8.g", "Use properties of rectangles to find missing lengths and angles", S8)
def _(d=1):
    d = _d(d)

    def t_opposite():
        a = random.randint(*_by(d, (3, 12), (3, 30), (31, 99)))
        return _tb("A rectangle has one side of %d cm. How long is the opposite side, in cm?" % a, a, "int",
                   {"unit": "cm"}, ["Opposite sides of a rectangle are equal."])

    def t_perimeter_side():
        a, b = (random.randint(*_by(d, (2, 10), (3, 25), (15, 60))) for _ in range(2))
        return _tb("A rectangle has a perimeter of %d cm. Its length is %d cm. What is its width, in cm?"
                   % (2 * (a + b), a), b, "int", {"unit": "cm"},
                   ["Length + width = %d ÷ 2 = %d." % (2 * (a + b), a + b), "%d − %d = %d." % (a + b, a, b)])

    def t_angle():
        return _tb("What is the size of each angle inside a rectangle, in degrees?", 90, "int", {"unit": "°"},
                   ["All four angles of a rectangle are right angles."])

    def t_diagonal_angle():
        a = random.randint(*_by(d, (2, 7), (15, 75), (11, 79))) * _by(d, 10, 1, 1)
        if d == 2 and a % 5 == 0:                      # hard: never a multiple of 5
            a += 1
        return _tb("A diagonal splits a corner of a rectangle into two angles. One is %d°. How big is the other, in "
                   "degrees?" % a, 90 - a, "int", {"unit": "°"}, ["The corner is 90°.", "90 − %d = %d." % (a, 90 - a)])

    def t_square_from_perimeter():
        s = random.randint(*_by(d, (2, 10), (3, 25), (15, 40)))
        return _tb("A square has a perimeter of %d cm. How long is each side, in cm?" % (4 * s), s, "int",
                   {"unit": "cm"}, ["A square has 4 equal sides: %d ÷ 4 = %d." % (4 * s, s)])

    def t_split():
        W, a = random.randint(*_by(d, (10, 20), (12, 30), (30, 60))), random.randint(*_by(d, (2, 5), (3, 9), (11, 25)))
        return _tb("A rectangle %d cm long is cut into two smaller rectangles. One piece is %d cm long. How long is "
                   "the other piece, in cm?" % (W, a), W - a, "int", {"unit": "cm"}, ["%d − %d = %d." % (W, a, W - a)])

    def t_corners():
        return _wq("Is a square a special kind of rectangle? (yes or no)", "yes",
                   ["A square has 4 right angles and opposite sides equal, so it is a rectangle."], "yes / no")

    def t_grid():
        x0, y0 = random.randint(1, 3), random.randint(1, 3)
        w, h = random.randint(2, _by(d, 4, 5, 6)), random.randint(2, 4)
        corners = [[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]]
        # easy/medium: the missing corner is D, after A, B, C in order; hard: any corner can be the missing one
        k = random.randrange(4) if d == 2 else 3
        pts = [c + [n] for c, n in zip(corners, "ABCD") if c != corners[k]]
        ans = corners[k]
        return {"prompt": "%s, %s and %s are three corners of a rectangle. Plot the fourth corner." % tuple(p[2] for p in pts),
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": pts}, "answer": "(%d,%d)" % tuple(ans),
                "answer_type": "coord", "solution": ["Opposite sides are equal and parallel: (%d,%d)." % tuple(ans)]}

    def t_diagonals():
        k = random.randint(*_by(d, (5, 12), (5, 25), (26, 60)))
        return _tb("One diagonal of a rectangle is %d cm long. How long is the other diagonal, in cm?" % k, k, "int",
                   {"unit": "cm"}, ["The diagonals of a rectangle are equal."])

    def t_side_from_grid():
        x0, y0 = random.randint(1, 3), random.randint(1, 3)
        w, h = random.randint(2, 6), random.randint(2, 5)
        pts = [[x0, y0, "A"], [x0 + w, y0, "B"], [x0 + w, y0 + h, "C"], [x0, y0 + h, "D"]]
        ask_w = random.random() < 0.5
        return {"prompt": "ABCD is a rectangle on a 1 cm grid. How long is side %s, in cm?" % ("AB" if ask_w else "BC"),
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": pts,
                         "polygon": [[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]]},
                "answer": w if ask_w else h, "answer_type": "int",
                "solution": ["Count the squares: %d cm." % (w if ask_w else h)]}

    def t_joined():
        a, b, h = (random.randint(*_by(d, r0, r1, r2)) for r0, r1, r2 in
                   [((2, 6), (3, 12), (8, 25)), ((2, 6), (3, 12), (8, 25)), ((2, 5), (2, 9), (6, 20))])
        return _tb("Two rectangles, each %d cm tall, are put side by side to make one big rectangle. Their widths are %d cm "
                   "and %d cm. What is the perimeter of the big rectangle, in cm?" % (h, a, b), 2 * (a + b + h), "int",
                   {"unit": "cm"}, ["The big rectangle is %d cm by %d cm." % (a + b, h),
                                    "2 × (%d + %d) = %d." % (a + b, h, 2 * (a + b + h))])

    def t_square_area():
        s = random.randint(*_by(d, (2, 6), (2, 12), (6, 15)))
        return _tb("A square has an area of %d cm². What is its perimeter, in cm?" % (s * s), 4 * s, "int", {"unit": "cm"},
                   ["Each side is %d cm because %d × %d = %d." % (s, s, s, s * s), "4 × %d = %d." % (s, 4 * s)])

    def t_corner_sum():
        return _tb("What do the four inside angles of a rectangle add up to, in degrees?", 360, "int", {"unit": "°"},
                   ["4 right angles: 4 × 90 = 360."])

    return _pick_t([t_opposite, t_perimeter_side, t_angle, t_diagonal_angle, t_square_from_perimeter, t_split,
                    t_corners, t_diagonals, t_joined, t_square_area, t_corner_sum], [t_grid, t_side_from_grid])


@skill("Y5.8.h", "Regular and irregular polygons", S8)
def _(d=1):
    d = _d(d)
    POLY = [("triangle", 3), ("quadrilateral", 4), ("pentagon", 5), ("hexagon", 6), ("heptagon", 7),
            ("octagon", 8), ("nonagon", 9), ("decagon", 10)]
    # easy: up to hexagons; hard: hexagons and beyond (heptagon, nonagon, decagon) and bigger numbers
    PL = _by(d, POLY[:4], POLY, POLY[3:])

    def t_regular():
        name, n = pick(PL)
        eq_s, eq_a = pick([(True, True), (True, False), (False, True), (False, False)])
        if n == 3:
            eq_a = eq_s
        ok = eq_s and eq_a
        return _wq("%s %s has %s sides and %s angles. Is it regular? (yes or no)"
                   % ("An" if name[0] in "aeiou" else "A", name, "all equal" if eq_s else "unequal",
                      "all equal" if eq_a else "unequal"),
                   "yes" if ok else "no", ["A regular polygon has ALL sides equal AND ALL angles equal."], "yes / no")

    def t_rhombus():
        if d == 2 and random.random() < 0.5:
            return _wq("A rectangle that is not a square has 4 equal angles but its sides are not all equal. Is it a "
                       "regular polygon? (yes or no)", "no", ["Its sides are not all equal, so it is irregular."],
                       "yes / no")
        return _wq("A rhombus has 4 equal sides but its angles are not all equal. Is it a regular polygon? "
                   "(yes or no)", "no", ["Its angles are not all equal, so it is irregular."], "yes / no")

    def t_name():
        name, n = pick(PL[1:] if d < 2 else PL)
        return _wq("What is the name of a polygon with %d sides?" % n, name, ["%d sides: %s." % (n, name)], "name")

    def t_sides():
        name, n = pick(PL)
        return _tb("How many sides does %s %s have?" % ("an" if name[0] in "aeiou" else "a", name), n, "int", {}, ["%s %s has %d sides." % ("An" if name[0] in "aeiou" else "A", name, n)])

    def t_perimeter():
        name, n = pick(PL)
        s = random.randint(*_by(d, (2, 10), (3, 15), (6, 25)))
        return _tb("A regular %s has sides of %d cm. What is its perimeter, in cm?" % (name, s), n * s, "int",
                   {"unit": "cm"}, ["All %d sides are equal: %d × %d = %d." % (n, n, s, n * s)])

    def t_side_from_perimeter():
        name, n = pick(PL)
        s = random.randint(*_by(d, (2, 10), (3, 15), (6, 25)))
        return _tb("A regular %s has a perimeter of %d cm. How long is each side, in cm?" % (name, n * s), s, "int",
                   {"unit": "cm"}, ["%d ÷ %d = %d." % (n * s, n, s)])

    def t_shape():
        name = pick(_by(d, ["triangle", "square"], ["triangle", "square", "pentagon", "hexagon", "octagon"],
                        ["pentagon", "hexagon", "octagon"]))
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

    def _gap(lo, hi):
        # easy: the shape sits next to the mirror; hard: as far from it as the grid allows
        return _by(d, hi, random.randint(lo, hi), lo)

    def t_vertical():
        m = random.randint(4, 6)
        poly = _poly(_gap(max(0, 2 * m - 10), m - 3), random.randint(1, 6))
        k = random.randrange(len(poly))
        x, y = poly[k]
        pts = [[px, py, "A" if i == k else ""] for i, (px, py) in enumerate(poly) if i == k]
        return {"prompt": "The shape is reflected in the dashed vertical mirror line (x = %d). Plot where corner A "
                          "goes." % m, "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": pts,
                         "lines": [{"p1": [m, 0], "p2": [m, 10], "dashed": True, "label": "mirror"}]},
                "answer": "(%d,%d)" % (2 * m - x, y), "answer_type": "coord",
                "solution": ["A is %s left of the mirror, so its image is %s right of it." % (_pl(m - x, "square"), _pl(m - x, "square")),
                             "(%d,%d)." % (2 * m - x, y)]}

    def t_horizontal():
        m = random.randint(4, 6)
        poly = _poly(random.randint(1, 6), _gap(max(0, 2 * m - 10), m - 3))
        k = random.randrange(len(poly))
        x, y = poly[k]
        return {"prompt": "The shape is reflected in the dashed horizontal mirror line (y = %d). Plot where corner A "
                          "goes." % m, "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": [[x, y, "A"]],
                         "lines": [{"p1": [0, m], "p2": [10, m], "dashed": True, "label": "mirror"}]},
                "answer": "(%d,%d)" % (x, 2 * m - y), "answer_type": "coord",
                "solution": ["A is %s below the mirror, so its image is %s above it." % (_pl(m - y, "square"), _pl(m - y, "square")),
                             "(%d,%d)." % (x, 2 * m - y)]}

    def t_words():
        m = random.randint(3, 7)
        x = random.randint(_by(d, m - 2, 0, 0), m - 1)
        y = random.randint(0, 9)
        if d == 2:                                     # hard: the point starts on the right of the mirror
            x = random.randint(m + 1, min(2 * m, 10))
            return _wq("A point at (%d,%d) is reflected in a vertical mirror line through x = %d. Where does it go? "
                       "Write it like (3,4)." % (x, y, m), "(%d,%d)" % (2 * m - x, y),
                       ["Same distance on the other side: %d − %d = %d, %d − %d = %d." % (x, m, x - m, m, x - m, 2 * m - x)],
                       "(x,y)")
        return _wq("A point at (%d,%d) is reflected in a vertical mirror line through x = %d. Where does it go? "
                   "Write it like (3,4)." % (x, y, m), "(%d,%d)" % (2 * m - x, y),
                   ["Same distance on the other side: %d − %d = %d, %d + %d = %d." % (m, x, m - x, m, m - x, 2 * m - x)],
                   "(x,y)")

    def t_unchanged():
        what = pick(["the length of its sides", "the size of its angles", "its area"])
        return _wq("When a shape is reflected, does %s change? (yes or no)" % what, "no",
                   ["Reflection makes a mirror image the same size and shape."], "yes / no")

    def t_distance():
        a = random.randint(1, _by(d, 3, 6, 6))
        if d == 2:                                     # hard: work out the distance to the mirror first
            m = random.randint(a + 1, 10)
            return _tb("A point is at x = %d. The mirror line is x = %d. How far is its reflection from the point, in "
                       "squares?" % (m - a, m), 2 * a, "int", {"unit": "squares"},
                       ["It is %d − %d = %d squares from the mirror." % (m, m - a, a), "%d + %d = %d." % (a, a, 2 * a)])
        return _tb("A point is %s to the left of a mirror line. How far is its reflection from the point, in "
                   "squares?" % _pl(a, "square"), 2 * a, "int", {"unit": "squares"}, ["%d to the mirror and %d back: %d." % (a, a, 2 * a)])

    def t_words_h():
        m = random.randint(3, 7)
        x = random.randint(0, 9)
        y = random.randint(_by(d, m - 2, 0, 0), m - 1)
        if d == 2:                                     # hard: the point starts above the mirror
            y = random.randint(m + 1, min(2 * m, 10))
            return _wq("A point at (%d,%d) is reflected in a horizontal mirror line through y = %d. Where does it go? "
                       "Write it like (3,4)." % (x, y, m), "(%d,%d)" % (x, 2 * m - y),
                       ["The x stays the same; y is %d above the mirror, so the image is %d below: %d."
                        % (y - m, y - m, 2 * m - y)], "(x,y)")
        return _wq("A point at (%d,%d) is reflected in a horizontal mirror line through y = %d. Where does it go? Write it "
                   "like (3,4)." % (x, y, m), "(%d,%d)" % (x, 2 * m - y),
                   ["The x stays the same; y is %d below the mirror, so the image is %d above: %d." % (m - y, m - y, 2 * m - y)],
                   "(x,y)")

    def t_find_mirror():
        x = random.randint(0, 4)
        gap = random.randint(1, _by(d, 2, 3, 3))
        y = random.randint(0, 9)
        if d == 2:                                     # hard: the image lands to the left
            return _tb("A point at (%d,%d) is reflected in a vertical mirror line and lands at (%d,%d). The mirror line "
                       "is x = ? What number is it?" % (x + 2 * gap, y, x, y), x + gap, "int", {},
                       ["The mirror is halfway: (%d + %d) ÷ 2 = %d." % (x + 2 * gap, x, x + gap)])
        return _tb("A point at (%d,%d) is reflected in a vertical mirror line and lands at (%d,%d). The mirror line is "
                   "x = ? What number is it?" % (x, y, x + 2 * gap, y), x + gap, "int", {},
                   ["The mirror is halfway: (%d + %d) ÷ 2 = %d." % (x, x + 2 * gap, x + gap)])

    def t_on_line():
        m = random.randint(3, 7)
        y = random.randint(0, 9)
        return _wq("A point at (%d,%d) is reflected in the vertical mirror line x = %d. Where does it go? Write it like (3,4)."
                   % (m, y, m), "(%d,%d)" % (m, y), ["A point ON the mirror line does not move."], "(x,y)")

    def t_left_right():
        side = pick(["left", "right"])
        if d == 2 and random.random() < 0.5:           # hard: a horizontal mirror does not swap left and right
            return _wq("A flag points to the %s. It is reflected in a horizontal mirror line. Which way does the image "
                       "point? (left or right)" % side, side, ["A horizontal mirror flips up and down, not left and right."],
                       "left / right")
        return _wq("A flag points to the %s. It is reflected in a vertical mirror line. Which way does the image point? "
                   "(left or right)" % side, "right" if side == "left" else "left",
                   ["A vertical mirror swaps left and right."], "left / right")

    def t_vertical_low():
        m = random.randint(4, 6)
        poly = _poly(_by(d, m, random.randint(m, 7), 7), random.randint(1, 6))
        if max(p[0] for p in poly) > 10 or min(2 * m - p[0] for p in poly) < 0:
            return t_vertical()
        k = random.randrange(len(poly))
        x, y = poly[k]
        return {"prompt": "The shape is reflected in the dashed vertical mirror line (x = %d). Plot where corner A goes."
                          % m, "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "polygon": poly, "points": [[x, y, "A"]],
                         "lines": [{"p1": [m, 0], "p2": [m, 10], "dashed": True, "label": "mirror"}]},
                "answer": "(%d,%d)" % (2 * m - x, y), "answer_type": "coord",
                "solution": ["A is %s right of the mirror, so its image is %s left of it." % (_pl(x - m, "square"), _pl(x - m, "square")),
                             "(%d,%d)." % (2 * m - x, y)]} if x > m else t_vertical()

    return _pick_t([t_words, t_unchanged, t_distance, t_words_h, t_find_mirror, t_on_line, t_left_right],
                   [t_vertical, t_horizontal, t_vertical_low])


@skill("Y5.8.j", "Translation on a grid", S8)
def _(d=1):
    d = _d(d)

    def _move():
        if d == 0:                                     # easy: one direction only, up to 3 squares
            k = pick([-3, -2, -1, 1, 2, 3])
            return (k, 0) if random.random() < 0.5 else (0, k)
        if d == 2:                                     # hard: always both directions, 2 to 4 squares each
            return pick([-4, -3, -2, 2, 3, 4]), pick([-4, -3, -2, 2, 3, 4])
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
def _temps(d=1):
    """Hourly playground temperatures. Easy: small, gentle changes; hard: 8 readings that rise and fall more."""
    hrs = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00"] + (["14:00", "15:00"] if d == 2 else [])
    v = random.randint(*_by(d, (4, 8), (4, 12), (6, 15)))
    vals = []
    for _ in hrs:
        vals.append(v)
        v = min(30, max(0, v + random.randint(*_by(d, (-1, 2), (-2, 4), (-4, 4)))))
    return hrs, vals


@skill("Y5.9.a", "Read and interpret line graphs", S9)
def _(d=1):
    d = _d(d)
    hrs, vals = _temps(d)

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
        return _lg("Temperature in the playground. At what time was it warmest? (type the time, like 10:00)",
                   list(zip(hrs, vals)), hrs[vals.index(top)], ["The highest point is at %s." % hrs[vals.index(top)]],
                   "°C", "Time", atype="time")

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
        h = sorted(random.sample(range(*_by(d, (2, 20), (2, 40), (10, 100))), 5))
        k = random.randrange(5)
        return _lg("The graph shows the height of a sunflower. How tall was it in %s, in cm?" % weeks[k],
                   list(zip(weeks, h)), h[k], ["Read across: %d cm." % h[k]], "cm", "Week")

    def t_lowest():
        return _lg("Temperature in the playground. What was the lowest temperature, in °C?", list(zip(hrs, vals)),
                   min(vals), ["The lowest point is %d °C." % min(vals)], "°C", "Time")

    def t_count_above():
        lim = random.randint(min(vals), max(vals))
        n = sum(1 for v in vals if v > lim)
        return _lg("Temperature in the playground. At how many of the times shown was it warmer than %d °C?" % lim,
                   list(zip(hrs, vals)), n, ["Readings above %d: %s." % (lim, ", ".join(str(v) for v in vals if v > lim) or "none")],
                   "°C", "Time")

    def t_growth():
        weeks = ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5"]
        h = sorted(random.sample(range(*_by(d, (2, 20), (2, 40), (10, 100))), 5))
        i, j = sorted(random.sample(range(5), 2))
        return _lg("The graph shows the height of a sunflower. How much did it grow between %s and %s, in cm?"
                   % (weeks[i], weeks[j]), list(zip(weeks, h)), h[j] - h[i],
                   ["%d − %d = %d cm." % (h[j], h[i], h[j] - h[i])], "cm", "Week")

    def t_coldest_time():
        low = min(vals)
        if vals.count(low) > 1:
            return t_lowest()
        return _lg("Temperature in the playground. At what time was it coldest? (type the time, like 10:00)",
                   list(zip(hrs, vals)), hrs[vals.index(low)], ["The lowest point is at %s." % hrs[vals.index(low)]],
                   "°C", "Time", atype="time")

    def t_steps():
        mins = ["0", "10", "20", "30", "40"]
        st = [random.randint(*_by(d, (1, 5), (5, 30), (15, 60))) * _by(d, 100, 10, 10) for _ in mins]
        st = [sum(st[:k + 1]) for k in range(5)]
        k = random.randint(1, 4)
        return _lg("The graph shows the total number of steps %s had walked after each 10 minutes. How many steps had been "
                   "walked after %s minutes?" % (_who(), mins[k]), list(zip(mins, st)), st[k],
                   ["Read across from %s minutes: %d." % (mins[k], st[k])], "Steps", "Minutes")

    return _pick_t([], [t_read, t_highest, t_when, t_rise, t_plant, t_lowest, t_count_above, t_growth, t_coldest_time,
                        t_steps])


@skill("Y5.9.b", "Comparison, sum and difference problems from line graphs", S9)
def _(d=1):
    d = _d(d)
    hrs, vals = _temps(d)

    def _cnt(lo, hi):
        # easy: multiples of 5 up to 40; medium: lo-hi; hard: larger, up to 95
        return random.randint(1, 8) * 5 if d == 0 else random.randint(*_by(d, (lo, hi), (lo, hi), (hi - 15, 95)))

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
        s = [_cnt(5, 40) for _ in days]
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
                   "EARLIER time (like 09:00).", list(zip(hrs, vals)), hrs[k],
                   ["%s to %s: up %s." % (hrs[k], hrs[k + 1], _pl(top, "degree"))], "°C", "Time", atype="time")

    def t_total():
        days = ["Mon", "Tue", "Wed", "Thu"]
        s = [_cnt(5, 30) for _ in days]
        return _lg("The graph shows books borrowed each day. How many books were borrowed altogether?",
                   list(zip(days, s)), sum(s), ["%s = %d." % (" + ".join(map(str, s)), sum(s))], "Books", "Day")

    def t_two_lines_words():
        days = ["Mon", "Tue", "Wed"]
        a, b = [_cnt(10, 30) for _ in days], [_cnt(10, 30) for _ in days]
        k = random.randrange(3)
        return _dt("Two shops recorded their sales. What is the difference between the two shops' sales on %s?"
                   % days[k], ["Day", "Shop A", "Shop B"],
                   [[dd, x, y] for dd, x, y in zip(days, a, b)], abs(a[k] - b[k]),
                   ["%d − %d = %d." % (max(a[k], b[k]), min(a[k], b[k]), abs(a[k] - b[k]))])

    def t_how_many_more():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        s = [_cnt(5, 40) for _ in days]
        i, j = random.sample(range(5), 2)
        if s[i] == s[j]:
            s[i] += 3
        hi_, lo_ = (i, j) if s[i] > s[j] else (j, i)
        return _lg("The graph shows ice creams sold each day. How many more were sold on %s than on %s?"
                   % (days[hi_], days[lo_]), list(zip(days, s)), s[hi_] - s[lo_],
                   ["%d − %d = %d." % (s[hi_], s[lo_], s[hi_] - s[lo_])], "Ice creams", "Day")

    def t_sum_week():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        s = [_cnt(5, 40) for _ in days]
        k = random.randint(2, 4)
        return _lg("The graph shows ice creams sold each day. How many were sold from Monday to %s inclusive?"
                   % ["", "", "Wednesday", "Thursday", "Friday"][k], list(zip(days, s)), sum(s[:k + 1]),
                   ["%s = %d." % (" + ".join(map(str, s[:k + 1])), sum(s[:k + 1]))], "Ice creams", "Day")

    def t_fall_total():
        falls = [vals[k] - vals[k + 1] for k in range(len(vals) - 1) if vals[k + 1] < vals[k]]
        if not falls:
            return t_range()
        return _lg("Temperature in the playground. Add up every drop in temperature from one reading to the next. How many "
                   "degrees is that altogether?", list(zip(hrs, vals)), sum(falls),
                   ["The drops are %s." % ", ".join(map(str, falls)), "Total %d." % sum(falls)], "°C", "Time")

    return _pick_t([t_two_lines_words], [t_diff, t_range, t_sales_sum, t_biggest_rise, t_total, t_how_many_more,
                                         t_sum_week, t_fall_total])


@skill("Y5.9.c", "Complete, read and interpret tables", S9)
def _(d=1):
    d = _d(d)

    def _cnt(lo, hi):
        # easy: the smaller half of the range; hard: larger, two- and three-digit counts
        return random.randint(*_by(d, (lo, (lo + hi) // 2), (lo, hi), (hi, hi * 5)))

    def _close(n):
        # n different values; hard: bunched within a dozen of each other so they must be read carefully
        return random.sample(range(20, 120, 10) if d == 0 else range(20, 120) if d == 1 else
                             range(random.randint(30, 100), 0, -1)[:12], n)

    def t_total_col():
        clubs = ["Football", "Art", "Chess", "Music"]
        boys = [_cnt(3, 20) for _ in clubs]
        girls = [_cnt(3, 20) for _ in clubs]
        rows = [[c, b, g, b + g] for c, b, g in zip(clubs, boys, girls)]
        k = random.randrange(4)
        return _dt("The table shows how many boys and girls go to each club. What number belongs in the empty cell?",
                   ["Club", "Boys", "Girls", "Total"], rows, boys[k] + girls[k],
                   ["%d + %d = %d." % (boys[k], girls[k], boys[k] + girls[k])], missing=[k, 3])

    def t_missing_part():
        clubs = ["Football", "Art", "Chess"]
        boys = [_cnt(3, 20) for _ in clubs]
        girls = [_cnt(3, 20) for _ in clubs]
        rows = [[c, b, g, b + g] for c, b, g in zip(clubs, boys, girls)]
        k = random.randrange(3)
        return _dt("Complete the table. How many girls go to %s?" % clubs[k], ["Club", "Boys", "Girls", "Total"],
                   rows, girls[k], ["%d − %d = %d." % (boys[k] + girls[k], boys[k], girls[k])], missing=[k, 2])

    def t_read_compare():
        pets = ["Dog", "Cat", "Fish", "Rabbit"]
        y5 = [_cnt(2, 15) for _ in pets]
        y6 = [_cnt(2, 15) for _ in pets]
        k = random.randrange(4)
        return _dt("The table shows the pets owned by Year 5 and Year 6. How many %s are there altogether?"
                   % {"Dog": "dogs", "Cat": "cats", "Fish": "fish", "Rabbit": "rabbits"}[pets[k]], ["Pet", "Year 5", "Year 6"], [[p, a, b] for p, a, b in zip(pets, y5, y6)],
                   y5[k] + y6[k], ["%d + %d = %d." % (y5[k], y6[k], y5[k] + y6[k])])

    def t_most():
        cities = ["Leeds", "York", "Hull", "Bath"]
        rain = _close(4)
        return _dt("The table shows rainfall in mm. Which city had the most rain?", ["City", "Rainfall (mm)"],
                   [[c, r] for c, r in zip(cities, rain)], cities[rain.index(max(rain))],
                   ["The largest is %d mm." % max(rain)], atype="str")

    def t_column_total():
        items = ["Pens", "Pencils", "Rulers"]
        q = [_cnt(10, 90) for _ in items]
        rows = [[i, x] for i, x in zip(items, q)] + [["Total", sum(q)]]
        return _dt("The table shows stock in a cupboard. What is the total?", ["Item", "Number"], rows, sum(q),
                   ["%s = %d." % (" + ".join(map(str, q)), sum(q))], missing=[3, 1])

    def t_least():
        cities = ["Leeds", "York", "Hull", "Bath"]
        rain = _close(4)
        return _dt("The table shows rainfall in mm. Which city had the least rain?", ["City", "Rainfall (mm)"],
                   [[c, r] for c, r in zip(cities, rain)], cities[rain.index(min(rain))],
                   ["The smallest is %d mm." % min(rain)], atype="str")

    def t_two_way():
        sports = ["Swim", "Run", "Cycle"]
        y5 = [_cnt(3, 20) for _ in sports]
        y6 = [_cnt(3, 20) for _ in sports]
        rows = [[s, a, b] for s, a, b in zip(sports, y5, y6)]
        return _dt("The table shows which sport pupils chose. How many pupils chose altogether, in both years?",
                   ["Sport", "Year 5", "Year 6"], rows, sum(y5) + sum(y6),
                   ["Year 5: %d. Year 6: %d." % (sum(y5), sum(y6)), "%d + %d = %d." % (sum(y5), sum(y6), sum(y5) + sum(y6))])

    def t_how_many_more():
        pets = ["Dog", "Cat", "Fish", "Rabbit"]
        y5 = [_cnt(2, 15) for _ in pets]
        y6 = [_cnt(2, 15) for _ in pets]
        k = random.randrange(4)
        if y5[k] == y6[k]:
            y6[k] += 2
        more = "Year 5" if y5[k] > y6[k] else "Year 6"
        return _dt("The table shows the pets owned by Year 5 and Year 6. How many more %s owners are in %s than in the other "
                   "year?" % (pets[k].lower(), more), ["Pet", "Year 5", "Year 6"],
                   [[p, a, b] for p, a, b in zip(pets, y5, y6)], abs(y5[k] - y6[k]),
                   ["%d − %d = %d." % (max(y5[k], y6[k]), min(y5[k], y6[k]), abs(y5[k] - y6[k]))])

    def t_tally_total():
        fruit = ["Apple", "Banana", "Pear", "Grape"]
        n = [_cnt(4, 25) for _ in fruit]
        rows = [[f, x] for f, x in zip(fruit, n)]
        k = random.randrange(4)
        tot = sum(n)
        rows.append(["Total", tot])
        ans = n[k]
        rows[k][1] = ""
        return _dt("The table shows favourite fruits and the total. One number is missing. What is it?",
                   ["Fruit", "Pupils"], rows, ans, ["%d − %s = %d." % (tot, " − ".join(str(x) for i, x in enumerate(n) if i != k), ans)],
                   missing=[k, 1])

    return _pick_t([], [t_total_col, t_missing_part, t_read_compare, t_most, t_column_total, t_least, t_two_way,
                        t_how_many_more, t_tally_total])


@skill("Y5.9.d", "Read and use timetables", S9)
def _(d=1):
    d = _d(d)
    stops = ["Bridge St", "Park Rd", "Market", "Station"]
    # easy: gaps of 5, 10 or 15 minutes and buses on the quarter hours; hard: awkward gaps and departure times
    if d == 0:
        gaps = [random.randint(1, 3) * 5 for _ in range(3)]
        starts = sorted(random.sample(range(8 * 60, 9 * 60 + 1, 15), 3))
    elif d == 1:
        gaps = [random.randint(5, 20) for _ in range(3)]
        starts = sorted(random.sample(range(7 * 60, 11 * 60, 5), 3))
    else:
        gaps = [random.randint(7, 26) for _ in range(3)]
        starts = sorted(random.sample(range(7 * 60 + 3, 11 * 60, 7), 3))

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
        late = random.randint(*_by(d, (1, 2), (3, 15), (11, 25))) * _by(d, 5, 1, 1)
        k = random.randrange(3)
        return _dt("Use the bus timetable. Bus %d is %d minutes late at every stop. At what time does it reach Market? "
                   "(type it like 09:45)" % (k + 1, late), headers, rows, _t(starts[k] + sum(gaps[:2]) + late),
                   ["%s + %d minutes." % (_t(starts[k] + sum(gaps[:2])), late)], atype="time")

    def t_route():
        return _dt("Use the bus timetable. How many minutes does the whole route take, from Bridge St to the Station?",
                   headers, rows, sum(gaps), ["%d + %d + %d = %d minutes." % (gaps[0], gaps[1], gaps[2], sum(gaps))])

    def t_latest():
        k = random.randrange(3)
        need = starts[k] + sum(gaps) + random.randint(0, 4)
        if k < 2 and need >= starts[k + 1] + sum(gaps):
            need = starts[k + 1] + sum(gaps) - 1
        return _dt("Use the bus timetable. %s must be at the Station by %s. Which is the latest bus to catch? (type 1, 2 or 3)"
                   % (_who(), _t(need)), headers, rows, k + 1,
                   ["Bus %d reaches the Station at %s." % (k + 1, _t(starts[k] + sum(gaps)))])

    def t_missed():
        k = random.randint(0, 1)
        return _dt("Use the bus timetable. %s just misses Bus %d at Park Rd. How many minutes until the next bus leaves Park "
                   "Rd?" % (_who(), k + 1), headers, rows, starts[k + 1] - starts[k],
                   ["Bus %d is at Park Rd at %s and Bus %d at %s." % (k + 1, _t(starts[k] + gaps[0]), k + 2,
                                                                      _t(starts[k + 1] + gaps[0]))])

    def t_which_stop():
        k = random.randrange(3)
        i = random.randint(1, 3)
        return _dt("Use the bus timetable. Bus %d arrives at a stop at %s. Which stop is it? (type its name)"
                   % (k + 1, _t(starts[k] + sum(gaps[:i]))), headers, rows, stops[i],
                   ["Read down the Bus %d column." % (k + 1)], atype="str")

    def t_later():
        i, j = sorted(random.sample(range(3), 2))
        return _dt("Use the bus timetable. How many minutes later than Bus %d does Bus %d reach Market?" % (i + 1, j + 1),
                   headers, rows, starts[j] - starts[i],
                   ["%s to %s is %d minutes." % (_t(starts[i] + sum(gaps[:2])), _t(starts[j] + sum(gaps[:2])),
                                                 starts[j] - starts[i])])

    def t_from_park():
        k = random.randrange(3)
        return _dt("Use the bus timetable. %s gets on Bus %d at Park Rd. How many minutes is the ride to the Station?"
                   % (_who(), k + 1), headers, rows, gaps[1] + gaps[2],
                   ["%s to %s: %d minutes." % (_t(starts[k] + gaps[0]), _t(starts[k] + sum(gaps)), gaps[1] + gaps[2])])

    def t_leave_market():
        k = random.randrange(3)
        return _dt("Use the bus timetable. At what time is Bus %d at Market? (type it like 09:45)" % (k + 1), headers, rows,
                   _t(starts[k] + sum(gaps[:2])), ["Read down the Bus %d column to Market." % (k + 1)], atype="time")

    return _pick_t([], [t_journey, t_arrive, t_catch, t_wait, t_late, t_route, t_latest, t_missed, t_which_stop,
                        t_later, t_from_park, t_leave_market])
