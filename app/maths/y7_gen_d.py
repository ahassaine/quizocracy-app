# Year 7 generators: strands 7.7 and 7.8.
#
# Fractional thinking: add and subtract any fractions and mixed numbers, multiply and divide
# fractions, fraction problems.  Lines and angles: notation and labelling, measuring and estimating,
# angles at a point / on a line / vertically opposite, angles in triangles and quadrilaterals,
# properties of triangles and quadrilaterals, polygon angle sums, perpendicular and parallel lines
# and constructions, area of triangles, parallelograms and trapezia.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S7 = "7.7 Fractional thinking"
S8 = "7.8 Lines & angles"


def _rf(d, proper=True):
    den = pick(_by(d, [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 9, 10], [6, 7, 8, 9, 10, 12, 15]))
    num = random.randint(1, den - 1) if proper else random.randint(den + 1, 3 * den)
    return Fraction(num, den), num, den


# ================================================================== 7.7 ======
@skill("Y7.7.a", "Add and subtract fractions with any denominators", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)
    while bd == ad:
        b, bn, bd = _rf(d)

    def t_add():
        return _fq("Work out  %d/%d + %d/%d" % (an, ad, bn, bd), a + b,
                   ["Common denominator %d." % (ad * bd // _gcd(ad, bd)), "= %s." % _fs(a + b)])

    def t_sub():
        x, y = max(a, b), min(a, b)
        return _fq("Work out  %s − %s" % (_fs(x), _fs(y)), x - y, ["Use a common denominator: %s." % _fs(x - y)])

    def t_simplest():
        s = a + b
        return _wq("Work out %d/%d + %d/%d. Give the answer in its simplest form (as a mixed number if it is more than 1)."
                   % (an, ad, bn, bd), _mixed(s), ["= %s." % _mixed(s)], "e.g. 1 1/6")

    def t_missing():
        s = a + b
        return _fq("%d/%d + ___ = %s. What is the missing fraction?" % (an, ad, _fs(s)), b,
                   ["%s − %d/%d = %s." % (_fs(s), an, ad, _fs(b))])

    def t_word():
        x, y = max(a, b), min(a, b)
        if x + y > 1:
            return t_sub()
        who = _who()
        return _fq("%s spends %s of the money in a purse on a book and %s on a game. What fraction is left?" % (who, _fs(x), _fs(y)),
                   1 - x - y, ["1 − %s − %s = %s." % (_fs(x), _fs(y), _fs(1 - x - y))])

    return _pick_t([t_add, t_sub, t_simplest, t_missing, t_word])


def _gcd(x, y):
    while y:
        x, y = y, x % y
    return x


@skill("Y7.7.b", "Add and subtract mixed numbers", S7)
def _(d=1):
    d = _d(d)
    A = random.randint(1, 6) + _rf(d)[0]
    B = random.randint(1, 4) + _rf(d)[0]

    def t_add():
        return _wq("Work out %s + %s. Give a mixed number in its simplest form." % (_mixed(A), _mixed(B)), _mixed(A + B),
                   ["= %s." % _mixed(A + B)], "e.g. 5 1/4")

    def t_sub():
        x, y = max(A, B), min(A, B)
        if x == y:
            return t_add()
        return _wq("Work out %s − %s. Give a mixed number (or whole number) in its simplest form." % (_mixed(x), _mixed(y)),
                   _mixed(x - y), ["Convert to improper fractions or subtract wholes and parts: %s." % _mixed(x - y)],
                   "e.g. 2 3/4")

    def t_whole_minus():
        w = random.randint(3, 8)
        f = _rf(d)[0]
        return _wq("Work out %d − %s." % (w, _mixed(1 + f)), _mixed(w - 1 - f), ["= %s." % _mixed(w - 1 - f)], "e.g. 2 1/3")

    def t_word():
        return _wq("A plank is %s m long. %s m is cut off. How much is left, in metres? (mixed number, simplest form)"
                   % (_mixed(A + B), _mixed(B)), _mixed(A), ["%s − %s = %s." % (_mixed(A + B), _mixed(B), _mixed(A))],
                   "e.g. 3 1/2")

    return _pick_t([t_add, t_sub, t_whole_minus, t_word])


@skill("Y7.7.c", "Multiply fractions", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)

    def t_ff():
        return _fq("Work out  %d/%d × %d/%d" % (an, ad, bn, bd), a * b,
                   ["Multiply tops and bottoms: %d/%d = %s." % (an * bn, ad * bd, _fs(a * b))])

    def t_of():
        return _fq("What is %d/%d of %d/%d?" % (an, ad, bn, bd), a * b, ["'Of' means ×: %s." % _fs(a * b)])

    def t_int():
        k = random.randint(2, 12)
        return _fq("Work out  %d × %d/%d" % (k, an, ad), k * a, ["%d × %d = %d, so %d/%d = %s." % (k, an, k * an, k * an, ad,
                                                                                              _fs(k * a))])

    def t_mixed():
        M = random.randint(1, 3) + a
        k = random.randint(2, 5)
        return _wq("Work out %s × %d. Give a mixed number (or whole number) in its simplest form." % (_mixed(M), k),
                   _mixed(M * k), ["= %s." % _mixed(M * k)], "e.g. 4 1/2")

    def t_area():
        return _fq("A rectangle is %d/%d m by %d/%d m. What is its area, in m²?" % (an, ad, bn, bd), a * b,
                   ["%s × %s = %s." % (_fs(a), _fs(b), _fs(a * b))])

    def t_cancel():
        p = random.randint(2, 5)
        q = random.randint(2, 7)
        r = random.randint(2, 7)
        return _fq("Work out  %d/%d × %d/%d  (cancel first if you can)" % (p, q * r, r, p * 2), Fraction(p, q * r) * Fraction(r, p * 2),
                   ["= %s." % _fs(Fraction(p, q * r) * Fraction(r, p * 2))])

    return _pick_t([t_ff, t_of, t_int, t_mixed, t_area, t_cancel])


@skill("Y7.7.d", "Divide with fractions", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)

    def t_by_int():
        k = random.randint(2, 6)
        return _fq("Work out  %d/%d ÷ %d" % (an, ad, k), a / k, ["Dividing by %d is the same as × 1/%d: %s." % (k, k, _fs(a / k))])

    def t_int_by_unit():
        k, u = random.randint(2, 9), random.randint(2, 8)
        return _tb("How many %s are there in %d? (work out %d ÷ 1/%d)" % (_unit_word(u), k, k, u), k * u, "int", {},
                   ["%d × %d = %d." % (k, u, k * u)])

    def t_ff():
        return _fq("Work out  %d/%d ÷ %d/%d" % (an, ad, bn, bd), a / b, ["Multiply by the reciprocal %d/%d: %s." % (bd, bn, _fs(a / b))])

    def t_reciprocal():
        return _fq("What is the reciprocal of %d/%d?" % (an, ad), 1 / a, ["Flip it: %d/%d." % (ad, an)])

    def t_word():
        k = random.randint(2, 6)
        tot = Fraction(random.randint(2, 6))
        part = Fraction(1, pick([2, 3, 4]))
        return _tb("How many %s kg bags can be filled from %s kg of rice?" % (_fs(part), _fs(tot)), int(tot / part), "int",
                   {"unit": "bags"}, ["%s ÷ %s = %d." % (_fs(tot), _fs(part), int(tot / part))])

    return _pick_t([t_by_int, t_int_by_unit, t_ff, t_reciprocal, t_word])


def _unit_word(u):
    return {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths"}[u]


@skill("Y7.7.e", "Fraction problems", S7)
def _(d=1):
    d = _d(d)

    def t_remaining():
        x = random.randint(4, 20) * 12
        return _tb("A school has %d pupils. 1/3 walk, 1/4 come by bus and the rest come by car. How many come by car?" % x,
                   x - x // 3 - x // 4, "int", {}, ["1 − 1/3 − 1/4 = 5/12.", "5/12 of %d = %d." % (x, x - x // 3 - x // 4)])

    def t_of_remainder():
        x = random.randint(3, 15) * 20
        who = _who()
        return _tb("%s has £%d. %s spends 1/4 of it, then 2/5 of what is left. How much is left now, in pounds?"
                   % (who, x, who), x * 3 // 4 * 3 // 5, "int", {"unit": "£"},
                   ["After 1/4: £%d." % (x * 3 // 4), "2/5 of that is £%d; left £%d." % (x * 3 // 4 * 2 // 5, x * 3 // 4 * 3 // 5)])

    def t_whole_from_part():
        den = pick([3, 4, 5, 8])
        num = random.randint(1, den - 1)
        part = num * random.randint(3, 20)
        return _tb("%d/%d of a number is %d. What is the number?" % (num, den, part), part // num * den, "int", {},
                   ["%d ÷ %d = %d is 1/%d." % (part, num, part // num, den), "× %d = %d." % (den, part // num * den)])

    def t_compare():
        a, b = random.sample([Fraction(2, 3), Fraction(3, 5), Fraction(5, 8), Fraction(7, 12), Fraction(4, 7)], 2)
        return _wq("Which is larger, %s or %s?" % (_fs(a), _fs(b)), _fs(max(a, b)),
                   ["%s ≈ %.3f, %s ≈ %.3f." % (_fs(a), float(a), _fs(b), float(b))], "e.g. 3/5")

    def t_recipe():
        m = Fraction(3, 4)
        k = pick([2, 3, 4, 6])
        return _wq("A recipe uses 3/4 cup of milk per batch. How much milk for %d batches? (mixed number or whole number)" % k,
                   _mixed(m * k), ["%d × 3/4 = %s." % (k, _mixed(m * k))], "e.g. 2 1/4")

    return _pick_t([t_remaining, t_of_remainder, t_whole_from_part, t_compare, t_recipe])


# ================================================================== 7.8 ======
@skill("Y7.8.a", "Angle notation and types", S8)
def _(d=1):
    d = _d(d)

    def t_type():
        deg = random.choice([x for x in range(5, 356) if x not in (90, 180)])
        return _wq("Is an angle of %d° acute, obtuse or reflex?" % deg,
                   "acute" if deg < 90 else "obtuse" if deg < 180 else "reflex", ["Compare with 90° and 180°."],
                   "acute / obtuse / reflex")

    def t_vertex():
        p, q, r = random.sample("ABCDEFPQRS", 3)
        return _wq("In the angle written ∠%s%s%s, which letter is the vertex (the corner)?" % (p, q, r), q,
                   ["The middle letter is the vertex."], "one letter")

    def t_picture():
        deg = pick([random.randint(15, 80), random.randint(100, 170), random.randint(190, 340)])
        return {"prompt": "Is this angle acute, obtuse or reflex?", "component": "angle",
                "spec": {"mode": "classify", "degrees": deg},
                "answer": "acute" if deg < 90 else "obtuse" if deg < 180 else "reflex", "answer_type": "str",
                "solution": ["It is about %d°." % deg]}

    def t_measure():
        deg = random.randint(2, 34) * 5
        return {"prompt": "Measure this angle. How many degrees is it?", "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True}, "answer": deg, "answer_type": "num",
                "tolerance": 2, "solution": ["Read from 0 on the scale along the first arm: %d°." % deg]}

    def t_reflex():
        a = random.randint(20, 170)
        return _tb("The acute or obtuse angle between two arms is %d°. What is the reflex angle?" % a, 360 - a, "int",
                   {"unit": "°"}, ["360 − %d = %d." % (a, 360 - a)])

    def t_right_symbol():
        return _wq("On a diagram, what does a small square in a corner tell you about the angle? (one word: the angle is ...)",
                   "right", ["It marks a right angle (90°)."], "one word")

    return _pick_t([t_type, t_vertex, t_reflex, t_right_symbol], [t_picture, t_measure])


@skill("Y7.8.b", "Angles at a point, on a line and vertically opposite", S8)
def _(d=1):
    d = _d(d)

    def t_line():
        a = random.randint(15, 165)
        return _tb("Two angles on a straight line: one is %d°. Find the other." % a, 180 - a, "int", {"unit": "°"},
                   ["180 − %d = %d." % (a, 180 - a)])

    def t_point():
        parts = [random.randint(40, 110) for _ in range(_by(d, 2, 3, 3))]
        return _tb("Angles of %s and one more angle meet at a point. Find the missing angle." % ", ".join("%d°" % p for p in parts),
                   360 - sum(parts), "int", {"unit": "°"}, ["360 − %d = %d." % (sum(parts), 360 - sum(parts))])

    def t_vertical():
        a = random.randint(20, 160)
        return _tb("Two straight lines cross. One angle is %d°. What is the angle vertically opposite it?" % a, a, "int",
                   {"unit": "°"}, ["Vertically opposite angles are equal."])

    def t_adjacent():
        a = random.randint(20, 160)
        return _tb("Two straight lines cross. One angle is %d°. What is the angle next to it (on the same straight line)?" % a,
                   180 - a, "int", {"unit": "°"}, ["180 − %d = %d." % (a, 180 - a)])

    def t_algebra():
        x = random.randint(10, 40)
        k = random.randint(2, 4)
        rest = 180 - (k + 1) * x
        if rest <= 0:
            return t_line()
        return _tb("Angles of x°, %dx° and %d° lie on a straight line. Find x." % (k, rest), x, "int", {"unit": "°"},
                   ["%dx + %d = 180." % (k + 1, rest), "x = %d." % x])

    def t_pic():
        deg = random.randint(3, 15) * 10
        return {"prompt": "The angle shown is %d°. Another angle sits with it on a straight line. How big is it?" % deg,
                "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 180 - deg,
                "answer_type": "int", "solution": ["180 − %d = %d." % (deg, 180 - deg)]}

    return _pick_t([t_line, t_point, t_vertical, t_adjacent, t_algebra], [t_pic])


@skill("Y7.8.c", "Angles in triangles", S8)
def _(d=1):
    d = _d(d)
    a = random.randint(20, 100)
    b = random.randint(20, 160 - a)

    def t_third():
        return _tb("Two angles of a triangle are %d° and %d°. Find the third angle." % (a, b), 180 - a - b, "int",
                   {"unit": "°"}, ["180 − %d − %d = %d." % (a, b, 180 - a - b)])

    def t_isos_base():
        apex = random.randint(20, 140) // 2 * 2
        return _tb("An isosceles triangle has an angle of %d° between its two equal sides. Find each of the other two angles."
                   % apex, (180 - apex) // 2, "int", {"unit": "°"}, ["(180 − %d) ÷ 2 = %d." % (apex, (180 - apex) // 2)])

    def t_isos_apex():
        base = random.randint(20, 85)
        return _tb("An isosceles triangle has two equal angles of %d°. Find the third angle." % base, 180 - 2 * base, "int",
                   {"unit": "°"}, ["180 − 2 × %d = %d." % (base, 180 - 2 * base)])

    def t_right():
        x = random.randint(10, 80)
        return _tb("A right-angled triangle has an angle of %d°. Find the third angle." % x, 90 - x, "int", {"unit": "°"},
                   ["180 − 90 − %d = %d." % (x, 90 - x)])

    def t_equilateral():
        return _tb("What size is each angle in an equilateral triangle?", 60, "int", {"unit": "°"}, ["180 ÷ 3 = 60."])

    def t_exterior():
        return _tb("A triangle has interior angles %d° and %d°. Find the exterior angle at the third corner (on a straight "
                   "line with the third angle)." % (a, b), a + b, "int", {"unit": "°"},
                   ["Third angle = %d°." % (180 - a - b), "180 − %d = %d." % (180 - a - b, a + b)])

    def t_possible():
        x, y, z = random.randint(20, 100), random.randint(20, 100), random.randint(20, 100)
        if random.random() < 0.5:
            z = 180 - x - y if 180 - x - y > 0 else z
        return _wq("Could a triangle have angles of %d°, %d° and %d°? (yes or no)" % (x, y, z),
                   "yes" if x + y + z == 180 else "no", ["They add up to %d°." % (x + y + z)], "yes / no")

    return _pick_t([t_third, t_isos_base, t_isos_apex, t_right, t_equilateral, t_exterior, t_possible])


@skill("Y7.8.d", "Angles and properties of quadrilaterals", S8)
def _(d=1):
    d = _d(d)

    def t_fourth():
        a, b, c = random.randint(50, 130), random.randint(50, 130), random.randint(40, 120)
        if a + b + c >= 350:
            c = 60
        return _tb("Three angles of a quadrilateral are %d°, %d° and %d°. Find the fourth." % (a, b, c), 360 - a - b - c,
                   "int", {"unit": "°"}, ["Angles in a quadrilateral add to 360°.", "360 − %d = %d." % (a + b + c, 360 - a - b - c)])

    def t_parallelogram():
        a = random.randint(40, 140)
        return _tb("A parallelogram has one angle of %d°. What size is the angle next to it?" % a, 180 - a, "int",
                   {"unit": "°"}, ["Neighbouring angles in a parallelogram add to 180°."])

    def t_kite():
        a, b = random.randint(60, 140), random.randint(40, 100)
        c = 360 - a - b - b
        if c <= 20:
            return t_fourth()
        return _tb("A kite has a pair of equal angles of %d° each and another angle of %d°. Find the last angle." % (b, a),
                   c, "int", {"unit": "°"}, ["360 − %d − %d − %d = %d." % (b, b, a, c)])

    def t_property():
        q, ans = pick([("Which quadrilateral has 4 equal sides and 4 right angles?", "square"),
                       ("Which quadrilateral has exactly one pair of parallel sides?", "trapezium"),
                       ("Which quadrilateral has 4 equal sides but its angles are not right angles?", "rhombus"),
                       ("Which quadrilateral has two pairs of equal adjacent sides and one line of symmetry?", "kite"),
                       ("Which quadrilateral has opposite sides equal and parallel, and 4 right angles, but not all sides "
                        "equal?", "rectangle")])
        return _wq(q, ans, ["That is the definition of a %s." % ans], "name")

    def t_diagonals():
        q, ans = pick([("Do the diagonals of a square cross at right angles? (yes or no)", "yes"),
                       ("Do the diagonals of a rectangle (not a square) cross at right angles? (yes or no)", "no"),
                       ("Do the diagonals of a rhombus cross at right angles? (yes or no)", "yes"),
                       ("Are the diagonals of a rectangle equal in length? (yes or no)", "yes")])
        return _wq(q, ans, ["Think of the shape's symmetry."], "yes / no")

    return _pick_t([t_fourth, t_parallelogram, t_kite, t_property, t_diagonals])


@skill("Y7.8.e", "Angles in polygons", S8)
def _(d=1):
    d = _d(d)
    n = random.randint(5, 12)
    name = {5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 11: "hendecagon",
            12: "dodecagon"}[n]

    def t_sum():
        return _tb("What do the interior angles of a %s (%d sides) add up to?" % (name, n), (n - 2) * 180, "int",
                   {"unit": "°"}, ["(n − 2) × 180 = %d × 180 = %d." % (n - 2, (n - 2) * 180)])

    def t_regular():
        if 360 % n:
            return t_sum()
        return _tb("What is each interior angle of a regular %s?" % name, 180 - 360 // n, "int", {"unit": "°"},
                   ["Exterior angle = 360 ÷ %d = %d." % (n, 360 // n), "Interior = 180 − %d = %d." % (360 // n, 180 - 360 // n)])

    def t_exterior():
        if 360 % n:
            return t_sum()
        return _tb("What is each exterior angle of a regular %s?" % name, 360 // n, "int", {"unit": "°"},
                   ["Exterior angles add to 360°: 360 ÷ %d = %d." % (n, 360 // n)])

    def t_triangles():
        return _tb("How many triangles can a %d-sided polygon be split into by drawing diagonals from one corner?" % n, n - 2,
                   "int", {}, ["Always 2 fewer than the number of sides."])

    def t_missing():
        k = 5
        angles = [random.randint(90, 130) for _ in range(k - 1)]
        return _tb("Four angles of a pentagon are %s. Find the fifth." % ", ".join("%d°" % a for a in angles), 540 - sum(angles),
                   "int", {"unit": "°"}, ["Pentagon total = 540°.", "540 − %d = %d." % (sum(angles), 540 - sum(angles))])

    def t_sides_from_ext():
        n2 = pick([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20])
        return _tb("A regular polygon has exterior angles of %d°. How many sides does it have?" % (360 // n2), n2, "int", {},
                   ["360 ÷ %d = %d." % (360 // n2, n2)])

    return _pick_t([t_sum, t_regular, t_exterior, t_triangles, t_missing, t_sides_from_ext])


@skill("Y7.8.f", "Parallel and perpendicular lines and constructions", S8)
def _(d=1):
    d = _d(d)

    def t_vocab():
        q, ans = pick([("Two lines that meet at a right angle are called what?", "perpendicular"),
                       ("Two lines that never meet and stay the same distance apart are called what?", "parallel"),
                       ("A line that cuts another line exactly in half at 90° is called the perpendicular what?", "bisector"),
                       ("Which tool, apart from a ruler, is used for standard constructions?", "compasses")])
        return _wq(q + " (one word)", ans, ["Key vocabulary."], "one word")

    def t_bisect_angle():
        a = random.randint(10, 85) * 2
        return _tb("An angle of %d° is bisected. What size are the two new angles?" % a, a // 2, "int", {"unit": "°"},
                   ["Bisect means cut in half: %d ÷ 2 = %d." % (a, a // 2)])

    def t_bisect_line():
        L = random.randint(4, 30) * 2
        return _tb("A line segment %d cm long has its perpendicular bisector drawn. How far is the crossing point from each "
                   "end, in cm?" % L, L // 2, "int", {"unit": "cm"}, ["%d ÷ 2 = %d." % (L, L // 2)])

    def t_shortest():
        return _wq("What is the shortest distance from a point to a line: along any line, or along the perpendicular? "
                   "(type any or perpendicular)", "perpendicular", ["The perpendicular distance is shortest."],
                   "any / perpendicular")

    def t_grid():
        x, y = random.randint(1, 4), random.randint(2, 6)
        k = random.randint(2, 4)
        return {"prompt": "A line goes from A(%d,%d) to B(%d,%d). Plot point C so that AC is perpendicular to AB and %d squares "
                          "long, going up." % (x, y, x + 4, y, k), "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[x, y, "A"], [x + 4, y, "B"]],
                         "lines": [{"p1": [x, y], "p2": [x + 4, y]}]},
                "answer": "(%d,%d)" % (x, y + k), "answer_type": "coord",
                "solution": ["AB is horizontal, so AC must be vertical: (%d,%d)." % (x, y + k)]}

    def t_parallel_grid():
        x, y = random.randint(1, 3), random.randint(1, 3)
        dx, dy = random.randint(1, 3), random.randint(1, 3)
        x2 = random.randint(4, 6)
        return {"prompt": "Line AB goes from (%d,%d) to (%d,%d). Starting at C(%d,%d), plot point D so that CD is parallel to AB "
                          "and the same length." % (x, y, x + dx, y + dy, x2, y), "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10,
                         "points": [[x, y, "A"], [x + dx, y + dy, "B"], [x2, y, "C"]],
                         "lines": [{"p1": [x, y], "p2": [x + dx, y + dy]}]},
                "answer": "(%d,%d)" % (x2 + dx, y + dy), "answer_type": "coord",
                "solution": ["Make the same move: %d right and %d up." % (dx, dy)]}

    return _pick_t([t_vocab, t_bisect_angle, t_bisect_line, t_shortest], [t_grid, t_parallel_grid])


@skill("Y7.8.g", "Area of triangles, parallelograms and trapezia", S8)
def _(d=1):
    d = _d(d)

    def t_triangle():
        b, h = random.randint(2, 20), random.randint(2, 20)
        return _tb("A triangle has base %d cm and perpendicular height %d cm. Find its area, in cm²." % (b, h), _ds(Fraction(b * h, 2)),
                   "num", {"unit": "cm²"}, ["½ × %d × %d = %s." % (b, h, _ds(Fraction(b * h, 2)))])

    def t_parallelogram():
        b, h = random.randint(2, 20), random.randint(2, 15)
        return _tb("A parallelogram has base %d m and perpendicular height %d m. Find its area, in m²." % (b, h), b * h, "int",
                   {"unit": "m²"}, ["base × height = %d." % (b * h)])

    def t_trapezium():
        a, b, h = random.randint(2, 15), random.randint(2, 15), random.randint(2, 12)
        return _tb("A trapezium has parallel sides %d cm and %d cm, and height %d cm. Find its area, in cm²." % (a, b, h),
                   _ds(Fraction((a + b) * h, 2)), "num", {"unit": "cm²"},
                   ["½ × (%d + %d) × %d = %s." % (a, b, h, _ds(Fraction((a + b) * h, 2)))])

    def t_reverse():
        b = random.randint(2, 16)
        h = random.randint(2, 16)
        return _tb("A triangle has area %s cm² and base %d cm. What is its perpendicular height, in cm?" % (_ds(Fraction(b * h, 2)), b),
                   h, "int", {"unit": "cm"}, ["Area × 2 ÷ base = %d." % h])

    def t_slant_trap():
        b, h, s = random.randint(4, 15), random.randint(3, 10), 0
        s = h + random.randint(1, 4)
        return _tb("A parallelogram has base %d cm, a sloping side of %d cm and perpendicular height %d cm. Find its area, in cm²."
                   % (b, s, h), b * h, "int", {"unit": "cm²"}, ["Use the perpendicular height, not the sloping side: %d × %d." % (b, h)])

    def t_compound():
        w, h, th = random.randint(4, 12), random.randint(3, 10), random.randint(2, 6)
        return _tb("A house shape is a %d cm by %d cm rectangle with a triangle on top of base %d cm and height %d cm. Find the "
                   "total area, in cm²." % (w, h, w, th), _ds(w * h + Fraction(w * th, 2)), "num", {"unit": "cm²"},
                   ["%d + %s = %s." % (w * h, _ds(Fraction(w * th, 2)), _ds(w * h + Fraction(w * th, 2)))])

    return _pick_t([t_triangle, t_parallelogram, t_trapezium, t_reverse, t_slant_trap, t_compound])
