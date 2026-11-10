# Year 2 generators (added 2 Nov 2026 to widen the bank).
#
# Use place value and number facts to solve problems; compare and sort common 2-D and 3-D shapes
# and everyday objects.  Short prompts for young readers.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403
from .y2_gen_a import S0, S6, KIDS, _pn, _tn, _a, FACE_WHY


@skill("Y2.0.e", "Use place value and number facts to solve problems", S0)
def _(d=1):
    d = _d(d)
    kid = pick(KIDS)

    def t_boxes():
        t, o = random.randint(_by(d, 1, 2, 4), _by(d, 5, 9, 9)), random.randint(1, 9)
        return _tb("Eggs come in boxes of 10. %s has %s and %s. How many eggs?" % (kid, _pn(t, "full box", "full boxes"), _pn(o, "loose egg")),
                   10 * t + o, "int", {}, ["%s is %d." % (_tn(t, o), 10 * t + o)])

    def t_how_many_boxes():
        n = random.randint(_by(d, 21, 21, 45), _by(d, 59, 99, 99))
        return _tb("%d pencils are packed in boxes of 10. How many boxes can be filled?" % n, n // 10, "int", {},
                   ["%d = %s, so %s." % (n, _tn(n // 10, n % 10), _pn(n // 10, "box", "boxes"))])

    def t_missing_digit():
        n = random.randint(21, _by(d, 59, 89, 79))
        m = random.randint(1, min(_by(d, 2, 9, 9), 9 - n // 10))
        if d == 2:                                      # hard: the missing number comes first, or it is a subtraction
            if random.random() < 0.5:
                return _tb("___ + %d = %d" % (10 * m, n + 10 * m), n, "int", {},
                           ["%d − %d = %d: take %s off the tens." % (n + 10 * m, 10 * m, n, _pn(m, "ten"))])
            return _tb("%d − ___ = %d" % (n + 10 * m, n), 10 * m, "int", {},
                       ["The ones digit stays the same; the tens digit went down by %d, so %d." % (m, 10 * m)])
        return _tb("%d + ___ = %d" % (n, n + 10 * m), 10 * m, "int", {},
                   ["The ones digit stays the same; the tens digit went up by %d, so %d." % (m, 10 * m)])

    def t_closest_ten():
        n = random.choice([x for x in range(11, 99) if x % 10 != 5 and x % 10])
        return _tb("Which multiple of 10 is closest to %d?" % n, int(round(n / 10.0)) * 10, "int", {},
                   ["%d is between %d and %d; it is closer to %d." % (n, (n // 10) * 10, (n // 10) * 10 + 10, int(round(n / 10.0)) * 10)])

    def t_add_ten_word():
        p = _by(d, 1, 2, random.randint(3, 4))
        n = random.randint(_by(d, 11, 15, 15), 99 - 10 * p)
        return _tb("%s had %d cards. %s was given %s of 10 cards. How many cards now?" % (kid, n, kid, _pn(p, "pack")), n + 10 * p,
                   "int", {}, ["%d%s = %d." % (n, " + 10" * p, n + 10 * p)])

    def t_greatest_diff():
        ds = random.sample(range(1, 10), 2)
        big, small = max(ds) * 10 + min(ds), min(ds) * 10 + max(ds)
        return _tb("Make the biggest and the smallest two-digit numbers from %d and %d. What is the difference?" % tuple(ds), big - small,
                   "int", {}, ["%d − %d = %d." % (big, small, big - small)])

    def t_between():
        lo = random.randint(_by(d, 1, 1, 4), _by(d, 4, 8, 9)) * 10
        k = random.randint(1, 9)
        return _tb("I am between %d and %d. My ones digit is %d. What number am I?" % (lo, lo + 10, k),
                   lo + k, "int", {}, ["%s is %d." % (_tn(lo // 10, k), lo + k)])

    def t_fact_use():
        a, b = random.randint(2, 9), random.randint(2, 9)
        while (d == 0 and a + b > 9) or (d == 2 and a + b < 11):
            a, b = random.randint(2, 9), random.randint(2, 9)
        t = 10 * random.randint(1, _by(d, 4, 7, 7))
        return _tb("%d + %d = %d. Use this to work out %d + %d." % (a, b, a + b, t + a, b), t + a + b, "int", {},
                   ["%d is %d more than %d, so the answer is %d more: %d." % (t + a, t, a, t, t + a + b)])

    def t_estimate():
        n = random.randint(15, 95) if d else 10 * random.randint(2, 9) + pick([0, 5])
        o, t = n % 10, (n // 10) * 10
        why = ("%d is exactly %d tens." % (n, n // 10) if o == 0 else
               "%d is halfway between %d and %d." % (n, t, t + 10) if o == 5 else
               "%d is a little more than %d." % (n, t) if o < 5 else "%d is a little less than %d." % (n, t + 10))
        q = _nl("Estimate where %d goes on the line from 0 to 100. Mark it." % n, n, 1, 10, [why], lo=0, hi=100)
        q["tolerance"] = 3          # an estimate: a mark within 3 of the number counts
        return q

    def t_place_value_chart():
        if d == 2:                                      # hard: more than 9 ones, so regroup ten ones into a ten
            t, o = random.randint(1, 7), random.randint(11, 19)
            return _dt("The table shows a number made of tens and ones. What is the number?", ["Tens", "Ones"], [[t, o]], 10 * t + o,
                       ["%d ones = 1 ten and %s." % (o, _pn(o - 10, "one")), "%s is %d." % (_tn(t + 1, o - 10), 10 * t + o)])
        t, o = random.randint(1, _by(d, 5, 9, 9)), random.randint(0, 9)
        return _dt("The table shows a number in tens and ones. What is the number?", ["Tens", "Ones"], [[t, o]], 10 * t + o,
                   ["%s is %d." % (_tn(t, o), 10 * t + o)])

    def t_coins_fewest_tens():
        n = random.randint(_by(d, 21, 21, 45), _by(d, 59, 99, 99))
        return _tb("%s wants to pay %dp using as many 10p coins as possible and then 1p coins. How many 10p coins?" % (kid, n), n // 10,
                   "int", {}, ["%dp = %s." % (n, _tn(n // 10, n % 10))])

    def t_blocks():
        n = random.randint(_by(d, 21, 21, 45), _by(d, 59, 99, 99))
        return {"prompt": "%s has %d sweets and buys 10 more. Make the new number with the blocks." % (kid, n - 10), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": n, "answer_type": "int", "solution": ["%d + 10 = %d." % (n - 10, n)]}

    return _pick_t(_by(d, [t_boxes, t_how_many_boxes, t_missing_digit, t_closest_ten, t_add_ten_word, t_between, t_fact_use],
                       [t_boxes, t_how_many_boxes, t_missing_digit, t_closest_ten, t_add_ten_word, t_greatest_diff, t_between,
                        t_fact_use, t_coins_fewest_tens],
                       [t_how_many_boxes, t_missing_digit, t_closest_ten, t_add_ten_word, t_greatest_diff, t_fact_use,
                        t_coins_fewest_tens]),
                   [t_estimate, t_place_value_chart, t_blocks])


@skill("Y2.6.d", "Compare and sort 2-D and 3-D shapes and everyday objects", S6)
def _(d=1):
    d = _d(d)
    FLAT = {"circle": (0, 0), "triangle": (3, 3), "square": (4, 4), "rectangle": (4, 4), "pentagon": (5, 5), "hexagon": (6, 6)}
    OBJ = [("football", "sphere"), ("tin of soup", "cylinder"), ("dice", "cube"), ("cereal box", "cuboid"),
           ("party hat", "cone"), ("orange", "sphere"), ("brick", "cuboid"), ("candle", "cylinder"), ("ice cube", "cube")]

    def t_object():
        o, sh = pick(OBJ)
        return _wq("What 3-D shape is %s? (one word)" % _a(o), sh, ["%s is %s." % (_a(o).capitalize(), _a(sh))], "shape name")

    def t_count_solid():
        items = random.sample(["cube", "circle", "sphere", "square", "cone", "triangle", "cuboid", "hexagon"], _by(d, 4, 5, 7))
        n = sum(1 for x in items if x in ("cube", "sphere", "cone", "cuboid"))
        return _tb("How many of these are 3-D shapes?  %s" % ", ".join(items), n, "int", {}, ["3-D shapes are solid: cube, sphere, cone, cuboid."])

    def t_odd_one():
        # the rule is stated, so exactly one shape is the odd one out (a bare "cylinder, cube, sphere"
        # has two defensible answers)
        group, odd, rule = pick(_by(d, [(["cube", "cuboid"], "sphere", "have only flat faces"),
                                        (["triangle", "square"], "cube", "are flat 2-D shapes"),
                                        (["pentagon", "hexagon"], "cone", "are flat 2-D shapes")],
                                    [(["square", "rectangle"], "triangle", "have 4 sides"),
                                     (["cube", "cuboid"], "sphere", "have only flat faces"),
                                     (["triangle", "square"], "cube", "are flat 2-D shapes"),
                                     (["sphere", "cylinder"], "cube", "have a curved surface"),
                                     (["pentagon", "hexagon"], "cone", "are flat 2-D shapes")],
                                    [(["square", "rectangle"], "triangle", "have 4 sides"),
                                     (["sphere", "cylinder"], "cube", "have a curved surface"),
                                     (["cone", "cylinder"], "cuboid", "have a curved surface"),
                                     (["cube", "cuboid", "triangular prism"], "cone", "have only flat faces"),
                                     (["square", "rectangle", "hexagon"], "circle", "have straight sides")]))
        items = group + [odd]
        random.shuffle(items)
        return _wq("All but one of these shapes %s. Which is the odd one out?  %s" % (rule, ", ".join(items)), odd,
                   ["%s %s." % (" and ".join(", ".join(group).rsplit(", ", 1)).capitalize(), rule),
                    "The %s is not like them, so it is the odd one out." % odd], "shape name")

    def t_more_sides():
        a, b = random.sample(_by(d, ["triangle", "square", "hexagon"], [x for x in FLAT if x != "circle" and x != "rectangle"],
                                 [x for x in FLAT if x != "circle" and x != "rectangle"]), 2)
        fewer = d == 2 and random.random() < 0.5
        return _wq("Which has %s sides, a %s or a %s?" % ("fewer" if fewer else "more", a, b),
                   a if (FLAT[a][0] > FLAT[b][0]) != fewer else b,
                   ["A %s has %d sides and a %s has %d." % (a, FLAT[a][0], b, FLAT[b][0])], "shape name")

    def t_sort_table():
        shapes = random.sample(["cube", "sphere", "cylinder", "cone", "cuboid", "square-based pyramid"], 4)
        curved = {"sphere", "cylinder", "cone"}
        rows = [[x, "?" if i == 3 else ("yes" if x in curved else "no")] for i, x in enumerate(shapes)]
        return _dt("Does each shape have a curved surface? Type yes or no for the last shape.", ["Shape", "Curved surface?"], rows,
                   "yes" if shapes[3] in curved else "no", ["Sphere, cylinder and cone have curved surfaces."], atype="str",
                   placeholder="yes / no")

    def t_faces_compare():
        a, b = pick([(("cube", 6), ("square-based pyramid", 5)), (("cuboid", 6), ("triangular prism", 5)),
                     (("triangular prism", 5), ("cube", 6))])
        return _wq("Which has more faces, a %s or a %s?" % (a[0], b[0]), a[0] if a[1] > b[1] else b[0],
                   ["A %s has %d faces; a %s has %d." % (a[0], a[1], b[0], b[1])], "shape name")

    def t_edges_compare():                              # hard: compare edges of two solids
        a, b = random.sample([("cube", 12), ("square-based pyramid", 8), ("triangular prism", 9)], 2)
        return _wq("Which has more edges, a %s or a %s?" % (a[0], b[0]), a[0] if a[1] > b[1] else b[0],
                   ["An edge is where two faces meet.", "A %s has %d edges; a %s has %d." % (a[0], a[1], b[0], b[1])], "shape name")

    def t_stack():
        q, a = pick([("Can you stack cubes on top of each other neatly? (yes or no)", "yes"),
                     ("Can you stack spheres on top of each other neatly? (yes or no)", "no"),
                     ("Will a cone roll? (yes or no)", "yes"),
                     ("Will a cuboid roll? (yes or no)", "no")])
        return _wq(q, a, ["Flat faces stack; curved surfaces roll."], "yes / no")

    def t_vertices_pic():
        name = pick(_by(d, ["cube", "cuboid"], ["cube", "cuboid", "square-based pyramid", "triangular prism"],
                        ["square-based pyramid", "triangular prism", "cube"]))
        n = {"cube": 8, "cuboid": 8, "square-based pyramid": 5, "triangular prism": 6}[name]
        return {"prompt": "How many vertices (corners) does this shape have?", "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": "vertices"}, "answer": n, "answer_type": "int",
                "solution": ["Count every corner, including the hidden one: %d." % n]}

    def t_face_on_solid():
        q, a = pick([("Which 2-D shape do you see at each end of a cylinder?", "circle"),
                     ("Which 2-D shape is the bottom of a square-based pyramid?", "square"),
                     ("Which 2-D shape is at each end of a triangular prism?", "triangle"),
                     ("Which 2-D shape is every face of a cube?", "square")])
        return _wq(q, a, [FACE_WHY[q]], "shape name")

    def t_sides_sort():
        shapes = random.sample(["triangle", "square", "rectangle", "pentagon", "hexagon", "circle"], _by(d, 4, 5, 6))
        n = random.choice(_by(d, [3, 4], [3, 4], [4, 5, 6]))
        k = sum(1 for x in shapes if FLAT[x][0] == n)
        return _tb("Sort these shapes. How many have exactly %d sides?  %s" % (n, ", ".join(shapes)), k, "int", {},
                   ["Only %s %s %d sides: %d." % (" and ".join("the " + x for x in shapes if FLAT[x][0] == n), "has" if k == 1 else "have", n, k)
                    if k else "No shape in the list has %d sides." % n])

    return _pick_t(_by(d, [t_object, t_count_solid, t_odd_one, t_more_sides, t_stack, t_face_on_solid],
                       [t_object, t_count_solid, t_odd_one, t_more_sides, t_faces_compare, t_stack, t_face_on_solid, t_sides_sort],
                       [t_count_solid, t_odd_one, t_more_sides, t_faces_compare, t_edges_compare, t_face_on_solid, t_sides_sort]),
                   [t_sort_table, t_vertices_pic])
