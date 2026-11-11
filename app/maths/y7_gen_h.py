# Year 7 generators: visual geometry and statistics that complete the Year 7 bank.
#
# KS3 statements covered here: line and rotational symmetry; properties of 3-D shapes (faces, edges,
# vertices) and their nets; reflections and translations on a coordinate grid; construct and interpret
# pie charts; frequency tables, bar charts, pictograms and line graphs; the probability of an event
# not happening; relative frequency and expected outcomes from experiments.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S8 = "7.8 Lines & angles"
S9 = "7.9 Sets, probability & data"

def _a(x):
    """'a 7 cm', 'an 8 cm', 'an 11-sided', 'an octagon': the article read aloud, plus the text."""
    s = str(x)
    w = s.split()[0].replace(",", "").split("-")[0]
    if w[:1].isdigit():
        vowel = w.startswith("8") or w in ("11", "18") or (len(w) in (5, 8) and w[:2] in ("11", "18"))
    else:
        vowel = w[:1].lower() in "aeiou"
    return ("an " if vowel else "a ") + s


_SIDES = {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "heptagon": 7, "octagon": 8}


def _grid(points=None, polygon=None, lines=None, typed=False, placeholder=None, span=7):
    spec = {"xmin": -span, "xmax": span, "ymin": -span, "ymax": span}
    if points:
        spec["points"] = points
    if polygon:
        spec["polygon"] = polygon
    if lines:
        spec["lines"] = lines
    if typed:
        spec["typed"] = True
        spec["placeholder"] = placeholder or "your answer"
    return spec


def _plot(prompt, spec, x, y, solution):
    return {"prompt": prompt, "component": "coordinate_grid", "spec": spec, "answer": "(%d,%d)" % (x, y),
            "answer_type": "coord", "solution": solution}


# ================================================================== 7.8 ======
@skill("Y7.8.i", "Line and rotational symmetry", S8)
def _(d=1):
    d = _d(d)

    pic_names = _by(d, ["triangle", "square", "hexagon", "rectangle"], list(_SIDES) + ["rectangle"],
                    ["pentagon", "heptagon", "octagon", "rectangle"])

    def t_lines_pic():
        name = pick(pic_names)
        n = 2 if name == "rectangle" else _SIDES[name]
        return {"prompt": "How many lines of symmetry does this shape have? (All its sides are equal unless it is a rectangle.)",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "lines_of_symmetry"}, "answer": n,
                "answer_type": "int", "solution": ["It has %d line%s of symmetry." % (n, "" if n == 1 else "s")]}

    def t_order_pic():
        name = pick(pic_names)
        n = 2 if name == "rectangle" else _SIDES[name]
        return {"prompt": "What is the order of rotational symmetry of this shape? (All its sides are equal unless it is a "
                          "rectangle.)", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"}, "answer": n,
                "answer_type": "int", "solution": ["It looks the same %d times in a full turn." % n]}

    def t_named_lines():
        easy = [("rectangle (not a square)", 2), ("square", 4), ("equilateral triangle", 3), ("isosceles triangle (not equilateral)", 1)]
        hard = [("kite", 1), ("parallelogram (not a rectangle or rhombus)", 0), ("rhombus (not a square)", 2), ("isosceles trapezium", 1),
                ("scalene triangle", 0)]
        name, n = pick(_by(d, easy, hard + easy, hard))
        return _tb("How many lines of symmetry does %s have?" % _a(name), n, "int", {}, ["Fold it in your head: %d." % n])

    def t_named_order():
        easy = [("square", 4), ("equilateral triangle", 3), ("regular hexagon", 6)]
        hard = [("parallelogram (not a rectangle or rhombus)", 2), ("kite", 1), ("rhombus (not a square)", 2), ("isosceles trapezium", 1)]
        name, n = pick(_by(d, easy, hard + easy, hard))
        return _tb("What is the order of rotational symmetry of %s?" % _a(name), n, "int", {},
                   ["Count how many times it fits onto itself in one full turn: %d." % n])

    def t_letters():
        easy = [("H", 2, 2), ("A", 1, 1), ("E", 1, 1), ("T", 1, 1), ("M", 1, 1)]
        hard = [("N", 0, 2), ("Z", 0, 2), ("S", 0, 2), ("X", 2, 2), ("I", 2, 2), ("H", 2, 2)]   # rotation without reflection
        letter, lines, order = pick(_by(d, easy, easy + hard, hard))
        if random.random() < 0.5:
            return _tb("How many lines of symmetry does the capital letter %s have (in a plain block font)?" % letter, lines, "int",
                       {}, ["%s has %d." % (letter, lines)])
        return _tb("What is the order of rotational symmetry of the capital letter %s (in a plain block font)?" % letter, order,
                   "int", {}, ["%s fits onto itself %d time%s in a full turn." % (letter, order, "" if order == 1 else "s")])

    def t_poly_grid():
        name, pts, n = pick([
            ("kite", [[0, 4], [2, 1], [0, -4], [-2, 1]], 1),
            ("parallelogram", [[-4, -2], [2, -2], [4, 2], [-2, 2]], 0),
            ("isosceles trapezium", [[-4, -2], [4, -2], [2, 2], [-2, 2]], 1),
            ("rhombus", [[0, 4], [3, 0], [0, -4], [-3, 0]], 2),
            ("arrow", [[-4, 0], [0, 4], [4, 0], [2, 0], [2, -4], [-2, -4], [-2, 0]], 1),
            ("rectangle", [[-5, -2], [5, -2], [5, 2], [-5, 2]], 2)])
        return {"prompt": "How many lines of symmetry does the shape on the grid have?", "component": "coordinate_grid",
                "spec": _grid(polygon=pts, typed=True, placeholder="number"), "answer": n, "answer_type": "int",
                "solution": ["This %s has %d line%s of symmetry." % (name, n, "" if n == 1 else "s")]}

    def t_complete():
        k = random.randint(-2, 2) if d else 0            # easy: the mirror is the y-axis
        x, y = k - random.randint(1, _by(d, 3, 4, 4)), random.randint(-5, 5)
        return _plot("The dashed line x = %d is a mirror line. Point A is at (%d,%d). Plot the point that makes the pattern "
                     "symmetrical about the mirror line." % (k, x, y),
                     _grid(points=[[x, y, "A"]], lines=[{"p1": [k, 0], "p2": [k, 1], "dashed": True}]),
                     2 * k - x, y, ["A is %s left of the line, so the image is the same distance right: (%d,%d)."
                                    % (_pl(k - x, "square"), 2 * k - x, y)])

    def t_sides_from_lines():
        n = random.randint(*_by(d, (5, 8), (5, 12), (9, 20)))
        return _tb("A regular polygon has %d lines of symmetry. How many sides does it have?" % n, n, "int", {},
                   ["A regular polygon has as many lines of symmetry as sides."])

    def t_angle():
        n = pick(_by(d, [3, 4, 6, 8], [3, 4, 5, 6, 8, 9, 10, 12], [5, 9, 10, 12, 15, 18, 20, 36]))
        return _tb("What is the smallest angle you can turn a regular polygon with %d sides through so that it looks the same?"
                   % n, 360 // n, "int", {"unit": "°"}, ["360 ÷ %d = %d." % (n, 360 // n)])

    return _pick_t([t_named_lines, t_named_order, t_letters, t_sides_from_lines, t_angle],
                   _by(d, [t_lines_pic, t_order_pic, t_complete], [t_lines_pic, t_order_pic, t_poly_grid, t_complete],
                       [t_lines_pic, t_order_pic, t_poly_grid, t_poly_grid, t_complete]))


_SOLIDS = {"cube": (6, 12, 8), "cuboid": (6, 12, 8), "square-based pyramid": (5, 8, 5), "triangular prism": (5, 9, 6)}
_NETS = {"cube": "cube", "cuboid": "cuboid", "square_pyramid": "square-based pyramid", "triangular_prism": "triangular prism",
         "cylinder": "cylinder", "cone": "cone"}


@skill("Y7.8.j", "3-D shapes: faces, edges, vertices and nets", S8)
def _(d=1):
    d = _d(d)

    def t_count_pic():
        name = pick(_by(d, ["cube", "cuboid"], list(_SOLIDS), ["square-based pyramid", "triangular prism"]))
        ask = pick(["faces", "edges", "vertices"])
        n = _SOLIDS[name][("faces", "edges", "vertices").index(ask)]
        return {"prompt": "How many %s does this solid have? (Count the hidden ones too.)" % ask, "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": ask}, "answer": n, "answer_type": "int",
                "solution": ["A %s has %d faces, %d edges and %d vertices." % ((name,) + _SOLIDS[name])]}

    def t_name_pic():
        name = pick(["cube", "cuboid", "triangular prism"])
        return {"prompt": "What is the name of this solid?", "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_net_name():
        key = pick(["cube", "cuboid", "triangular_prism", "cylinder", "cone"])
        return {"prompt": "This net folds up to make which 3-D solid?", "component": "net", "spec": {"solid": key},
                "answer": _NETS[key], "answer_type": "str", "solution": ["It folds into a %s." % _NETS[key]]}

    def t_net_faces():
        key = pick(_by(d, ["cube", "cuboid"], ["cube", "cuboid", "square_pyramid", "triangular_prism"], ["square_pyramid", "triangular_prism"]))
        n = {"cube": 6, "cuboid": 6, "square_pyramid": 5, "triangular_prism": 5}[key]
        return {"prompt": "How many faces will the solid made from this net have?", "component": "net", "spec": {"solid": key},
                "answer": n, "answer_type": "int", "solution": ["Each flat piece of the net is one face: %d." % n]}

    def t_prism():
        n, nm = pick(_by(d, [(4, "square-based"), (3, "triangular")],
                         [(5, "pentagonal"), (6, "hexagonal"), (8, "octagonal"), (4, "square-based"), (3, "triangular")],
                         [(5, "pentagonal"), (6, "hexagonal"), (7, "heptagonal"), (8, "octagonal"), (10, "decagonal")]))
        ask = pick(["faces", "edges", "vertices"])
        val = {"faces": n + 2, "edges": 3 * n, "vertices": 2 * n}[ask]
        return _tb("How many %s does %s prism have?" % (ask, _a(nm)), val, "int", {},
                   ["Its two ends have %d sides each." % n, "Faces = %d + 2, edges = 3 × %d, vertices = 2 × %d." % (n, n, n)])

    def t_pyramid():
        n, nm = pick(_by(d, [(3, "triangle-based"), (5, "pentagon-based")],
                         [(5, "pentagon-based"), (6, "hexagon-based"), (3, "triangle-based"), (8, "octagon-based")],
                         [(6, "hexagon-based"), (7, "heptagon-based"), (8, "octagon-based"), (10, "decagon-based")]))
        ask = pick(["faces", "edges", "vertices"])
        val = {"faces": n + 1, "edges": 2 * n, "vertices": n + 1}[ask]
        return _tb("How many %s does %s pyramid have?" % (ask, _a(nm)), val, "int", {},
                   ["The base has %d sides." % n, "Faces = %d + 1, edges = 2 × %d, vertices = %d + 1." % (n, n, n)])

    def t_euler():
        f, v = pick([(6, 8), (5, 6), (5, 5), (7, 10), (8, 12), (7, 7), (4, 4)])
        if d == 2 and random.random() < 0.5:           # stretch: rearrange the formula to find the faces
            e = f + v - 2
            return _tb("A solid with flat faces has %d edges and %d vertices. Using faces + vertices − edges = 2, how many faces "
                       "does it have?" % (e, v), f, "int", {}, ["faces = 2 + edges − vertices = 2 + %d − %d = %d." % (e, v, f)])
        return _tb("A solid with flat faces has %d faces and %d vertices. Using faces + vertices − edges = 2, how many edges "
                   "does it have?" % (f, v), f + v - 2, "int", {}, ["%d + %d − 2 = %d." % (f, v, f + v - 2)])

    def t_facts():
        q, ans = pick([("How many faces of a cube meet at each vertex?", 3),
                       ("How many rectangular faces does a triangular prism have?", 3),
                       ("How many triangular faces does a square-based pyramid have?", 4),
                       ("How many edges of a cube meet at each vertex?", 3),
                       ("How many square faces does a cube have?", 6)])
        return _tb(q, ans, "int", {}, ["Picture the solid and count."])

    def t_face_shape():
        q, ans = pick([("What 2-D shape are the faces of a cube?", "square"),
                       ("What 2-D shape is the base of a square-based pyramid?", "square"),
                       ("What 2-D shape are the two end faces of a triangular prism?", "triangle"),
                       ("What 2-D shape is the flat face of a cone?", "circle"),
                       ("What 2-D shape are the sloping faces of a pyramid?", "triangle")])
        return _wq(q, ans, ["It is a %s." % ans], "shape name")

    return _pick_t(_by(d, [t_prism, t_facts, t_face_shape], [t_prism, t_pyramid, t_euler, t_facts, t_face_shape],
                       [t_prism, t_pyramid, t_euler, t_facts]),
                   _by(d, [t_count_pic, t_name_pic, t_net_name, t_net_faces], [t_count_pic, t_name_pic, t_net_name, t_net_faces],
                       [t_count_pic, t_net_faces]))


@skill("Y7.8.k", "Reflect and translate on a coordinate grid", S8)
def _(d=1):
    d = _d(d)
    x, y = random.choice([v for v in range(-6, 7) if v]), random.choice([v for v in range(-6, 7) if v])

    def t_x_axis():
        return _plot("Reflect the point P(%d,%d) in the x-axis. Plot its image." % (x, y), _grid(points=[[x, y, "P"]]), x, -y,
                     ["Reflecting in the x-axis keeps x and changes the sign of y: (%d,%d)." % (x, -y)])

    def t_y_axis():
        return _plot("Reflect the point P(%d,%d) in the y-axis. Plot its image." % (x, y), _grid(points=[[x, y, "P"]]), -x, y,
                     ["Reflecting in the y-axis keeps y and changes the sign of x: (%d,%d)." % (-x, y)])

    def t_line_x():
        k = random.randint(-3, 3)
        px = k + random.choice([v for v in range(-3, 4) if v])
        return _plot("Reflect P(%d,%d) in the dashed line x = %d. Plot its image." % (px, y, k),
                     _grid(points=[[px, y, "P"]], lines=[{"p1": [k, 0], "p2": [k, 1], "dashed": True}]), 2 * k - px, y,
                     ["P is %d square%s from the line, so the image is the same distance on the other side: (%d,%d)."
                      % (abs(px - k), "" if abs(px - k) == 1 else "s", 2 * k - px, y)])

    def t_line_y():
        k = random.randint(-3, 3)
        py = k + random.choice([v for v in range(-3, 4) if v])
        return _plot("Reflect P(%d,%d) in the dashed line y = %d. Plot its image." % (x, py, k),
                     _grid(points=[[x, py, "P"]], lines=[{"p1": [0, k], "p2": [1, k], "dashed": True}]), x, 2 * k - py,
                     ["The image is the same distance on the other side of y = %d: (%d,%d)." % (k, x, 2 * k - py)])

    def t_translate():
        m = _by(d, 3, 4, 6)
        a, b = random.randint(-m, m), random.randint(-m, m)
        if a == 0 and b == 0:
            a = 2
        px = random.randint(max(-6, -6 - a), min(6, 6 - a))      # P and its image both stay on the grid
        py = random.randint(max(-6, -6 - b), min(6, 6 - b))
        how = "%d %s and %d %s" % (abs(a), "right" if a >= 0 else "left", abs(b), "up" if b >= 0 else "down")
        return _plot("Translate P(%d,%d) %s. Plot its image." % (px, py, how), _grid(points=[[px, py, "P"]]), px + a, py + b,
                     ["(%d %s %d, %d %s %d) = (%d,%d)." % (px, "+" if a >= 0 else "−", abs(a), py, "+" if b >= 0 else "−", abs(b),
                                                           px + a, py + b)])

    def t_describe():
        a, b = random.randint(1, 5), random.randint(1, 5)
        px, py = random.randint(-6, 1), random.randint(-6, 1)
        ask = pick(["right", "up"])
        if d == 2 and random.random() < 0.5:           # stretch: the move is left or down, so A′ is behind A
            px, py, a, b, ask = px + a, py + b, -a, -b, {"right": "left", "up": "down"}[ask]
        return {"prompt": "Point A moves to A′ by a translation. How many squares %s does it move?" % ask,
                "component": "coordinate_grid", "spec": _grid(points=[[px, py, "A"], [px + a, py + b, "A′"]], typed=True,
                                                               placeholder="squares"),
                "answer": abs(a) if ask in ("right", "left") else abs(b), "answer_type": "int",
                "solution": ["A(%d,%d) to A′(%d,%d): %d %s and %d %s." % (px, py, px + a, py + b, abs(a), "right" if a > 0 else "left",
                                                                          abs(b), "up" if b > 0 else "down")]}

    def t_reverse():
        a, b = random.randint(1, 4), random.randint(1, 4)
        qx, qy = random.randint(-2, 6), random.randint(-2, 6)
        return _tb("After a translation %d right and %d up, a point is at (%d,%d). Where was it before? Write it like (1,2)."
                   % (a, b, qx, qy), "(%d,%d)" % (qx - a, qy - b), "coord", {"text": True, "placeholder": "(x,y)"},
                   ["Undo it: %d left and %d down." % (a, b)])

    def t_triangle():
        k = pick([0, 1, -1])
        tri = [[k + 1, 1], [k + 4, 1], [k + 1, 4]]
        v = random.randrange(3)
        return _plot("Triangle ABC is reflected in the dashed line x = %d. Plot the image of %s." % (k, "ABC"[v]),
                     _grid(points=[[p[0], p[1], "ABC"[i]] for i, p in enumerate(tri)], polygon=tri,
                           lines=[{"p1": [k, 0], "p2": [k, 1], "dashed": True}]), 2 * k - tri[v][0], tri[v][1],
                     ["%s(%d,%d) is %s right of the line, so its image is the same distance left: (%d,%d)."
                      % ("ABC"[v], tri[v][0], tri[v][1], _pl(tri[v][0] - k, "square"), 2 * k - tri[v][0], tri[v][1])])

    def t_invariant():
        on = random.randint(-6, 6)
        return _tb("Which point stays in the same place when it is reflected in the x-axis: (%d,%d) or (%d,0)? Write it like "
                   "(1,2)." % (on, 3, on), "(%d,0)" % on, "coord", {"text": True, "placeholder": "(x,y)"},
                   ["Points on the mirror line do not move."])

    def t_two_steps():
        a = random.randint(1, 4)
        px, py = random.randint(-5, 3), random.choice([v for v in range(-5, 6) if v])
        return _plot("Translate P(%d,%d) %d right, then reflect the result in the x-axis. Plot the final point." % (px, py, a),
                     _grid(points=[[px, py, "P"]]), px + a, -py,
                     ["After the translation: (%d,%d)." % (px + a, py), "After the reflection: (%d,%d)." % (px + a, -py)])

    return _pick_t(_by(d, [t_invariant], [t_reverse, t_invariant], [t_reverse]),
                   _by(d, [t_x_axis, t_y_axis, t_translate, t_describe],
                       [t_x_axis, t_y_axis, t_line_x, t_line_y, t_translate, t_describe, t_triangle, t_two_steps],
                       [t_line_x, t_line_y, t_translate, t_describe, t_triangle, t_two_steps]))


# ================================================================== 7.9 ======
_TOPICS = [("favourite fruit", ["Apple", "Banana", "Grape", "Orange"]),
           ("favourite pet", ["Cat", "Dog", "Fish", "Rabbit"]),
           ("favourite colour", ["Red", "Blue", "Green", "Yellow"]),
           ("favourite sport", ["Football", "Tennis", "Netball", "Swimming"])]


def _pie_data(total_choices=(18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120)):
    """Counts for four categories whose total divides 360, so every angle is a whole number of degrees."""
    tot = pick(list(total_choices))
    cuts = sorted(random.sample(range(1, tot), 3))
    counts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], tot - cuts[2]]
    return tot, counts


@skill("Y7.9.g", "Pie charts: read and calculate angles", S9)
def _(d=1):
    d = _d(d)
    topic, cats = pick(_TOPICS)
    # easy totals give 10°, 6°, 4° or 2° a person; stretch ones give awkward 15°, 9°, 8°, 5° or 3°
    tot, counts = _pie_data(_by(d, (36, 60, 90, 180), (18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120), (24, 40, 45, 72, 120)))
    per = 360 // tot
    k = random.randrange(4)

    def t_angle_from_table():
        return _dt("The table shows the %s of %d people. A pie chart is drawn. What angle should the %s sector have?"
                   % (topic, tot, cats[k]), ["Choice", "Frequency"], [[c, n] for c, n in zip(cats, counts)], counts[k] * per,
                   ["Each person gets 360 ÷ %d = %d°." % (tot, per), "%d × %d = %d°." % (counts[k], per, counts[k] * per)])

    def t_count_from_angle():
        slices = [[c, n * per] for c, n in zip(cats, counts)]
        return {"prompt": "The pie chart shows the %s of %d people. How many people chose %s?" % (topic, tot, cats[k]),
                "component": "pie_chart", "spec": {"slices": slices, "mode": "read", "highlight": k, "showAngles": True},
                "answer": counts[k], "answer_type": "int",
                "solution": ["%d° out of 360°." % (counts[k] * per), "%d/360 × %d = %d." % (counts[k] * per, tot, counts[k])]}

    def t_per_person():
        return _tb("A pie chart shows the answers of %d people. How many degrees stand for one person?" % tot, per, "int",
                   {"unit": "°"}, ["360 ÷ %d = %d." % (tot, per)])

    def t_missing_angle():
        ang = [n * per for n in counts]
        rows = [[c, "%d°" % a] for c, a in zip(cats, ang)]
        rows[k][1] = ""
        return _dt("The table gives the angles of a pie chart. What is the missing angle, in degrees?", ["Sector", "Angle"], rows,
                   ang[k], ["Angles add up to 360°: 360 − %d = %d." % (360 - ang[k], ang[k])], missing=[k, 1])

    def t_percent():
        p = pick(_by(d, [10, 25, 50], [10, 20, 25, 30, 40, 50], [15, 30, 35, 40, 45]))
        n = pick(_by(d, [40, 100, 200], [40, 60, 80, 120, 200, 300], [60, 80, 120, 140, 260, 300]))
        return {"prompt": "%d people answered a survey. The pie chart shows the percentages. How many people chose %s?" % (n, cats[0]),
                "component": "pie_chart", "spec": {"slices": [[cats[0], p], [cats[1], 100 - p - 25], [cats[2], 25]],
                                                   "mode": "read", "highlight": 0, "showPercents": True},
                "answer": n * p // 100, "answer_type": "int", "solution": ["%d%% of %d = %d." % (p, n, n * p // 100)]}

    def t_quarter():
        f, ang = pick(_by(d, [("a quarter", 90), ("a half", 180), ("three quarters", 270), ("a tenth", 36)],
                          [("a quarter", 90), ("a half", 180), ("a third", 120), ("an eighth", 45), ("a sixth", 60),
                           ("three quarters", 270)],
                          [("two thirds", 240), ("five eighths", 225), ("three tenths", 108), ("five twelfths", 150),
                           ("a fifth", 72), ("five sixths", 300)]))
        return _tb("A sector is %s of a pie chart. What is its angle?" % f, ang, "int", {"unit": "°"},
                   ["%s of 360° = %d°." % (f[0].upper() + f[1:], ang)])

    def t_total_from_sector():
        ang = counts[k] * per
        return _tb("In a pie chart the %s sector has an angle of %d° and stands for %d people. How many people are in the pie "
                   "chart altogether?" % (cats[k], ang, counts[k]), tot, "int", {"unit": "people"},
                   ["%d people take %d°, so one person is %d°." % (counts[k], ang, per), "360 ÷ %d = %d." % (per, tot)])

    def t_compare_pies():
        a, b = random.sample([40, 60, 80, 120, 200], 2)
        if d == 2:                                     # stretch: different angles, so the bigger total need not win
            na = nb = 0
            while na == nb:
                ang_a, ang_b = random.sample([36, 54, 72, 90, 108, 144, 180], 2)   # multiples of 18°: whole pupils for every total
                na, nb = a * ang_a // 360, b * ang_b // 360
            return _wq("School A's pie chart shows %d pupils, with a football sector of %d°. School B's shows %d pupils, with a "
                       "football sector of %d°. Which school has more pupils who chose football? (A or B)" % (a, ang_a, b, ang_b),
                       "A" if na > nb else "B",
                       ["A: %d/360 × %d = %d. B: %d/360 × %d = %d." % (ang_a, a, na, ang_b, b, nb)], "A or B")
        return _wq("School A's pie chart shows %d pupils and School B's shows %d. In both charts the football sector is 90°. "
                   "Which school has more pupils who chose football? (A or B)" % (a, b), "A" if a > b else "B",
                   ["A: %d ÷ 4 = %d. B: %d ÷ 4 = %d." % (a, a // 4, b, b // 4)], "A or B")

    def t_fraction():
        slices = [[c, n * per] for c, n in zip(cats, counts)]
        return {"prompt": "The pie chart shows the %s of %d people, with the angles marked. What fraction chose %s? Simplest form."
                          % (topic, tot, cats[k]), "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": k, "showAngles": True},
                "answer": _fs(Fraction(counts[k], tot)), "answer_type": "frac",
                "solution": ["%d/360 = %s." % (counts[k] * per, _fs(Fraction(counts[k], tot)))]}

    def t_largest_angle():
        return _dt("The table shows the %s of %d people. What angle would the biggest sector of a pie chart have?" % (topic, tot),
                   ["Choice", "Frequency"], [[c, n] for c, n in zip(cats, counts)], max(counts) * per,
                   ["%d × %d = %d°." % (max(counts), per, max(counts) * per)])

    def t_frequency_back():
        ang = counts[k] * per
        return _tb("A pie chart of %d people has %s sector of %d°. How many people does that sector stand for?"
                   % (tot, _a(cats[k]), ang), counts[k], "int", {"unit": "people"},
                   ["%d ÷ 360 × %d = %d." % (ang, tot, counts[k])])

    return _pick_t(_by(d, [t_per_person, t_quarter, t_frequency_back], [t_per_person, t_quarter, t_total_from_sector, t_compare_pies,
                                                                       t_frequency_back],
                       [t_quarter, t_total_from_sector, t_compare_pies, t_frequency_back]),
                   _by(d, [t_angle_from_table, t_count_from_angle, t_missing_angle, t_largest_angle],
                       [t_angle_from_table, t_count_from_angle, t_missing_angle, t_percent, t_fraction, t_largest_angle],
                       [t_angle_from_table, t_count_from_angle, t_missing_angle, t_percent, t_fraction]))


@skill("Y7.9.h", "Frequency tables, bar charts and line graphs", S9)
def _(d=1):
    d = _d(d)
    topic, cats = pick(_TOPICS)
    v = [random.randint(2, _by(d, 12, 25, 40)) for _ in cats]
    k = random.randrange(4)

    def t_total():
        # a percentage of the class: the total first, then one frequency out of it
        tot = pick(_by(d, [20, 25], [20, 25, 40, 50], [40, 50, 80]))
        while True:
            cuts = sorted(random.sample(range(1, tot), 3))
            f = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
            if (100 * f[k]) % tot == 0:
                break
        return _dt("The frequency table shows the %s of a class. What percentage of the class chose %s? Give the number only."
                   % (topic, cats[k]), ["Choice", "Frequency"], [[c, n] for c, n in zip(cats, f)], 100 * f[k] // tot,
                   ["The class has %s = %d pupils." % (" + ".join(map(str, f)), tot),
                    "%d out of %d = %d ÷ %d × 100 = %d%%." % (f[k], tot, f[k], tot, 100 * f[k] // tot)])

    def t_missing_freq():
        rows = [[c, n] for c, n in zip(cats, v)] + [["Total", sum(v)]]
        return _dt("The frequency table shows the %s of a class. What is the missing frequency?" % topic, ["Choice", "Frequency"],
                   rows, v[k], ["%d − %d = %d." % (sum(v), sum(v) - v[k], v[k])], missing=[k, 1])

    def t_goals():
        # easy: 0–2 goals, small frequencies; hard: 0–5 goals, frequencies to 12
        f = [random.randint(1, _by(d, 5, 8, 12)) for _ in range(_by(d, 3, 5, 6))]
        return _dt("The table shows the number of goals a team scored in each match of a season. How many goals did they score "
                   "altogether?", ["Goals in a match", "Number of matches"], [[g, n] for g, n in enumerate(f)],
                   sum(g * n for g, n in enumerate(f)),
                   ["Multiply each number of goals by its frequency: %s = %d." % (" + ".join("%d × %d" % (g, n) for g, n in enumerate(f)),
                                                                                  sum(g * n for g, n in enumerate(f)))])

    def t_matches():
        f = [random.randint(1, _by(d, 5, 8, 12)) for _ in range(_by(d, 3, 5, 6))]
        if d == 2:      # hard: matches in which they scored at least g goals
            g = random.randint(2, 4)
            return _dt("The table shows the number of goals a team scored in each match. In how many matches did they score "
                       "%d or more goals?" % g, ["Goals in a match", "Number of matches"], [[i, n] for i, n in enumerate(f)],
                       sum(f[g:]), ["%s = %d." % (" + ".join(map(str, f[g:])), sum(f[g:]))])
        # the mean from a frequency table: total goals ÷ number of matches, a whole number or one decimal place
        while (10 * sum(g * n for g, n in enumerate(f))) % sum(f):
            f = [random.randint(1, _by(d, 5, 8, 12)) for _ in range(_by(d, 3, 5, 6))]
        tg, nm = sum(g * n for g, n in enumerate(f)), sum(f)
        return _dt("The table shows the number of goals a team scored in each match. What is the mean number of goals per "
                   "match?", ["Goals in a match", "Number of matches"], [[g, n] for g, n in enumerate(f)],
                   _ds(Decimal(tg) / nm), ["Total goals: %s = %d." % (" + ".join("%d × %d" % (g, n) for g, n in enumerate(f)), tg),
                                           "Matches: %d. Mean = %d ÷ %d = %s." % (nm, tg, nm, _ds(Decimal(tg) / nm))],
                   atype="num")

    def t_grouped():
        groups = ["0–9", "10–19", "20–29", "30–39", "40–49"]
        f = [random.randint(1, _by(d, 8, 12, 20)) for _ in groups]
        if d == 2:      # hard: a band in the middle of the table
            lo = random.randint(1, 2)
            hi = random.randint(lo + 2, 5)
            return _dt("The grouped frequency table shows test marks out of 50. How many pupils scored from %d to %d?"
                       % (10 * lo, 10 * hi - 1), ["Mark", "Frequency"], [[g, n] for g, n in zip(groups, f)], sum(f[lo:hi]),
                       ["%s = %d." % (" + ".join(map(str, f[lo:hi])), sum(f[lo:hi]))])
        lo = random.randint(_by(d, 2, 1, 1), 3)
        return _dt("The grouped frequency table shows test marks out of 50. How many pupils scored %d or more?" % (10 * lo),
                   ["Mark", "Frequency"], [[g, n] for g, n in zip(groups, f)], sum(f[lo:]),
                   ["%s = %d." % (" + ".join(map(str, f[lo:])), sum(f[lo:]))])

    def t_bar_over():
        lim = random.randint(_by(d, 3, 5, 8), _by(d, 8, 15, 22))
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        vals = [random.randint(2, _by(d, 12, 20, 30)) for _ in days]
        while lim in vals:
            lim += 1
        over = [x for x in vals if x > lim]
        if d == 2:      # hard: add up the busy days as well
            return _bar("The bar chart shows how many books were borrowed each day. How many books were borrowed altogether on "
                        "the days when more than %d were borrowed?" % lim, days, vals, sum(over),
                        ["Bars above %d: %s." % (lim, ", ".join(map(str, over)) or "none"), "Total %d." % sum(over)])
        vals[-1] += (-sum(vals)) % 5
        return _bar("The bar chart shows how many books were borrowed each day. What is the mean number of books borrowed "
                    "per day?", days, vals, sum(vals) // 5,
                    ["%s = %d books in 5 days." % (" + ".join(map(str, vals)), sum(vals)),
                     "Mean = %d ÷ 5 = %d." % (sum(vals), sum(vals) // 5)])

    def t_bar_two_smallest():
        s = sorted(v)
        if s[1] == s[2]:
            v[v.index(s[2])] += 1
            s = sorted(v)
        f = Fraction(s[0] + s[1], sum(v))
        return _bar("The bar chart shows the %s of a class. What fraction of the class is in the two smallest groups "
                    "together? Simplest form." % topic, cats, v, _fs(f),
                    ["The two smallest groups: %d + %d = %d. The class: %s = %d." % (s[0], s[1], s[0] + s[1],
                                                                                   " + ".join(map(str, v)), sum(v)),
                     "%d out of %d = %s." % (s[0] + s[1], sum(v), _fs(f))], atype="frac")

    def t_line_read():
        hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm"]
        t = [random.randint(8, 24) // _by(d, 2, 1, 1) * _by(d, 2, 1, 1) for _ in hours]      # easy: even readings
        t[-1] += (-sum(t)) % 6
        return _lg("The line graph shows the temperature during a day. What was the mean of the six temperatures, in °C?",
                   list(zip(hours, t)), sum(t) // 6,
                   ["Read every point: %s = %d." % (" + ".join(map(str, t)), sum(t)), "Mean = %d ÷ 6 = %d °C." % (sum(t), sum(t) // 6)],
                   "°C", "Time")

    def t_line_range():
        hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"][: _by(d, 4, 6, 8)]
        t = [random.randint(8, 24) for _ in hours]
        if d == 2:      # hard: the biggest rise from one hour to the next
            rises = [t[i + 1] - t[i] for i in range(len(t) - 1)]
            if max(rises) <= 0:
                t[1] = t[0] + 4
                rises = [t[i + 1] - t[i] for i in range(len(t) - 1)]
            i = rises.index(max(rises))
            return _lg("The line graph shows the temperature during a day. What was the biggest rise in temperature from one hour "
                       "to the next, in °C?", list(zip(hours, t)), max(rises),
                       ["The steepest climb is %s to %s: %d − %d = %d." % (hours[i], hours[i + 1], t[i + 1], t[i], max(rises))],
                       "°C", "Time")
        return _lg("The line graph shows the temperature during a day. What is the difference between the highest and lowest "
                   "temperatures, in °C?", list(zip(hours, t)), max(t) - min(t),
                   ["%d − %d = %d." % (max(t), min(t), max(t) - min(t))], "°C", "Time")

    def t_two_classes():
        # compare proportions, not counts: 7A has 25 pupils and 7B has 20 (a harder pair: 30 and 40)
        def split(tot):
            cuts = sorted(random.sample(range(1, tot), 3))
            return [y - x for x, y in zip([0] + cuts, cuts + [tot])]
        na, nb = (25, 20) if d < 2 else (40, 50)
        a, b = split(na), split(nb)
        while a[k] * nb == b[k] * na:
            a, b = split(na), split(nb)
        pa, pb = Fraction(100 * a[k], na), Fraction(100 * b[k], nb)
        return _dt("The table shows the %s of two classes. 7A has %d pupils and 7B has %d. Which class has the greater "
                   "PERCENTAGE of pupils who chose %s? (type 7A or 7B)" % (topic, na, nb, cats[k]),
                   ["Choice", "7A", "7B"], [[c, x, y] for c, x, y in zip(cats, a, b)], "7A" if pa > pb else "7B",
                   ["7A: %d out of %d = %s%%. 7B: %d out of %d = %s%%." % (a[k], na, _ds(Decimal(pa.numerator) / pa.denominator),
                                                                        b[k], nb, _ds(Decimal(pb.numerator) / pb.denominator)),
                    "The classes are different sizes, so compare percentages: %s has the greater one." % ("7A" if pa > pb else "7B")],
                   atype="str")

    def t_pictogram_half():
        # easy: whole symbols only; medium: halves; hard: halves of bigger keys, and comparing two rows
        key = pick(_by(d, [2, 4, 10], [2, 4, 6, 10], [4, 6, 8, 12]))
        vals = [key * random.randint(1, 6) + (key // 2 if random.random() < 0.5 else 0) for _ in cats]
        spec = {"categories": cats, "values": vals, "key": key, "symbol": "star", "unit": "people"}
        if d == 2:
            j = random.choice([x for x in range(4) if x != k])
            if vals[j] == vals[k]:
                vals[j] += key
            hi_, lo_ = (k, j) if vals[k] > vals[j] else (j, k)
            return {"prompt": "The pictogram shows the %s of a group. Each symbol stands for %d people. How many more people "
                              "chose %s than %s?" % (topic, key, cats[hi_], cats[lo_]), "component": "pictogram",
                    "spec": spec, "answer": vals[hi_] - vals[lo_], "answer_type": "int",
                    "solution": ["%s: %d, %s: %d (half a symbol is %d)." % (cats[hi_], vals[hi_], cats[lo_], vals[lo_], key // 2),
                                 "%d − %d = %d." % (vals[hi_], vals[lo_], vals[hi_] - vals[lo_])]}
        return {"prompt": "The pictogram shows the %s of a group. Each symbol stands for %d people. How many people chose %s?"
                          % (topic, key, cats[k]), "component": "pictogram",
                "spec": spec, "answer": vals[k], "answer_type": "int",
                "solution": ["Whole symbols × %d, and half a symbol is %d: %d." % (key, key // 2, vals[k])]}

    def t_modal_group():
        groups = ["0–9", "10–19", "20–29", "30–39", "40–49"][: _by(d, 3, 4, 5)]
        f = random.sample(range(2, _by(d, 13, 20, 30)), len(groups))
        i = f.index(max(f))
        if d == 2:      # hard: modal group compared with the smallest group
            j = f.index(min(f))
            return _dt("The table shows test marks. How many more pupils are in the modal group than in the group with the "
                       "lowest frequency?", ["Mark", "Frequency"], [[g, n] for g, n in zip(groups, f)], max(f) - min(f),
                       ["Modal group %s has %d; %s has %d." % (groups[i], max(f), groups[j], min(f)),
                        "%d − %d = %d." % (max(f), min(f), max(f) - min(f))])
        return _dt("The table shows test marks. How many pupils are in the modal group (the group with the highest frequency)?",
                   ["Mark", "Frequency"], [[g, n] for g, n in zip(groups, f)], max(f),
                   ["The modal group is %s with %d pupils." % (groups[i], max(f))])

    return _pick_t([], [t_total, t_missing_freq, t_goals, t_matches, t_grouped, t_bar_over, t_bar_two_smallest, t_line_read,
                        t_line_range, t_two_classes, t_pictogram_half, t_modal_group])


@skill("Y7.9.i", "Probability: events not happening and experiments", S9)
def _(d=1):
    d = _d(d)

    def t_not_frac():
        den = pick(_by(d, [4, 5, 10], [5, 7, 8, 9, 10, 12], [12, 15, 16, 20, 25]))
        num = random.randint(1, den - 1)
        return _fq("The probability that a bus is late is %d/%d. What is the probability that it is NOT late?" % (num, den),
                   Fraction(den - num, den), ["1 − %d/%d = %d/%d." % (num, den, den - num, den)])

    def t_not_dec():
        p = Decimal(random.randint(1, _by(d, 9, 99, 999))) / _by(d, 10, 100, 1000)
        return _tb("The probability of winning a game is %s. What is the probability of not winning?" % _ds(p), _ds(1 - p), "num",
                   {}, ["1 − %s = %s." % (_ds(p), _ds(1 - p))])

    def t_not_pct():
        p = random.randint(1, 19) * 5 if d == 0 else random.randint(5, 95)
        return _tb("The chance of snow tomorrow is %d%%. What is the chance of no snow, as a percentage? Give the number only." % p,
                   100 - p, "int", {}, ["100 − %d = %d." % (p, 100 - p)])

    def t_rel_freq():
        n = pick([20, 25, 40, 50, 100])
        h = random.randint(n // 4, 3 * n // 4)
        return _fq("A coin is flipped %d times and lands on heads %d times. What is the relative frequency of heads? Simplest "
                   "form." % (n, h), Fraction(h, n), ["%d out of %d = %s." % (h, n, _fs(Fraction(h, n)))])

    def t_expected():
        p = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(1, 5), Fraction(1, 10)],
                     [Fraction(1, 2), Fraction(1, 4), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5), Fraction(1, 6)],
                     [Fraction(3, 10), Fraction(2, 5), Fraction(3, 8), Fraction(5, 12), Fraction(7, 20), Fraction(3, 4)]))
        n = p.denominator * random.randint(*_by(d, (2, 10), (5, 40), (10, 60)))
        shown = _ds(p) if p.denominator in (2, 4, 5, 10) and random.random() < 0.4 else _fs(p)
        return _tb("The probability a spinner lands on red is %s. It is spun %d times. How many times would you expect red?"
                   % (shown, n), int(p * n), "int", {},
                   ["%s × %d = %d." % (_fs(p), n, int(p * n))])

    def t_dice_table():
        n = pick([30, 60, 120])
        f = [random.randint(n // 9, n // 4) for _ in range(5)]
        f.append(n - sum(f))
        if f[-1] <= 0:
            f = [n // 6] * 6
        k = random.randrange(6)
        return _dt("A dice is rolled %d times. The table shows the results. Estimate the probability of rolling a %d. Simplest form."
                   % (n, k + 1), ["Score", "Frequency"], [[i + 1, x] for i, x in enumerate(f)], _fs(Fraction(f[k], n)),
                   ["Relative frequency = %d/%d = %s." % (f[k], n, _fs(Fraction(f[k], n)))], atype="frac")

    def t_reliable():
        a, b = random.sample([10, 20, 50, 500, 1000, 2000], 2)
        return _tb("Two pupils estimate the probability of a drawing pin landing point up. One drops it %d times, the other %d "
                   "times. How many drops gave the more reliable estimate?" % (a, b), max(a, b), "int", {},
                   ["More trials give a more reliable estimate."])

    def t_bar_rel():
        cols = ["Red", "Blue", "Green", "Yellow"]
        f = [random.randint(3, 15) for _ in cols]
        tot = sum(f)
        k = random.randrange(4)
        return _bar("A spinner was spun %d times and the results are shown. What is the relative frequency of %s? Simplest form."
                    % (tot, cols[k]), cols, f, _fs(Fraction(f[k], tot)), ["%d out of %d = %s." % (f[k], tot, _fs(Fraction(f[k], tot)))],
                    atype="frac")

    def t_not_bag():
        r, b, g = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        return _fq("A bag has %d red, %d blue and %d green balls. One is picked at random. What is the probability it is NOT red? "
                   "Simplest form." % (r, b, g), Fraction(b + g, r + b + g),
                   ["Not red: %d + %d = %d out of %d." % (b, g, b + g, r + b + g)])

    def t_neither():
        pa = Decimal(random.randint(1, 4)) / 10 + (Decimal(random.randint(1, 9)) / 100 if d == 2 else 0)
        pb = Decimal(random.randint(1, 4)) / 10 + (Decimal(random.randint(0, 9)) / 100 if d else 0)
        return _tb("A spinner can land on A, B or C only. P(A) = %s and P(B) = %s. What is P(C)?" % (_ds(pa), _ds(pb)),
                   _ds(1 - pa - pb), "num", {}, ["1 − %s − %s = %s." % (_ds(pa), _ds(pb), _ds(1 - pa - pb))])

    def t_scale_up():
        n1 = pick([20, 40, 50, 100, 120])
        hits = random.randint(1, n1 // 2)
        g = n1 // _gcd(n1, hits)
        n2 = g * random.randint(2, 10)
        return _tb("In %d trials an event happened %d times. Based on this, how many times would you expect it in %d trials?"
                   % (n1, hits, n2), hits * n2 // n1, "int", {},
                   ["Relative frequency %d/%d." % (hits, n1), "%d/%d × %d = %d." % (hits, n1, n2, hits * n2 // n1)])

    def t_fair():
        n = 600
        f = [random.randint(90, 110) for _ in range(5)]
        f.append(n - sum(f))                         # 50 to 150
        six = f[5]
        return _dt("A dice is rolled 600 times. How many sixes would you expect if the dice is fair?", ["Score", "Frequency"],
                   [[i + 1, x] for i, x in enumerate(f)], 100,
                   ["P(6) = 1/6 and 1/6 × 600 = 100. (It actually landed on 6 %d times.)" % six])

    return _pick_t(_by(d, [t_not_frac, t_not_dec, t_not_pct, t_expected, t_reliable, t_not_bag, t_neither],
                       [t_not_frac, t_not_dec, t_not_pct, t_rel_freq, t_expected, t_reliable, t_not_bag, t_neither, t_scale_up],
                       [t_not_frac, t_not_dec, t_rel_freq, t_expected, t_not_bag, t_neither, t_scale_up]),
                   _by(d, [t_bar_rel], [t_dice_table, t_bar_rel, t_fair], [t_dice_table, t_bar_rel, t_fair]))


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a
