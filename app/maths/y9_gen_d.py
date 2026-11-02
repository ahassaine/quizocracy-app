# Year 9 generators: strands 9.6 and 9.7.
#
# Geometry: trigonometry in right-angled triangles (sides and angles), Pythagoras in context and for a
# shorter side, similar shapes (lengths and areas), congruence criteria, multi-step angle reasoning,
# loci.  Mensuration: circles, semicircles and quarter circles; surface area of cuboids, prisms and
# cylinders; volume of prisms and cylinders; converting area and volume units.
import math

from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S6 = "9.6 Trigonometry, Pythagoras & similarity"
S7 = "9.7 Circles, surface area & volume"


def _r1(x):
    return round(x + 1e-12, 1)


# ================================================================== 9.6 ======
@skill("Y9.6.a", "Trigonometry: find a missing side", S6)
def _(d=1):
    d = _d(d)
    ang = random.randint(15, 75)
    known = random.randint(4, 20)
    rad = math.radians(ang)

    def t_opp_from_hyp():
        return _tb("A right-angled triangle has hypotenuse %d cm and an angle of %d°. Find the side opposite the angle, to 1 decimal place, "
                   "in cm." % (known, ang), _r1(known * math.sin(rad)), "num", {"unit": "cm"},
                   ["opp = hyp × sin %d° = %d × %.4f = %.1f." % (ang, known, math.sin(rad), known * math.sin(rad))], tol=0.051)

    def t_adj_from_hyp():
        return _tb("A right-angled triangle has hypotenuse %d cm and an angle of %d°. Find the side next to (adjacent to) the angle, to 1 "
                   "decimal place, in cm." % (known, ang), _r1(known * math.cos(rad)), "num", {"unit": "cm"},
                   ["adj = hyp × cos %d°." % ang], tol=0.051)

    def t_opp_from_adj():
        return _tb("In a right-angled triangle the side adjacent to an angle of %d° is %d cm. Find the opposite side, to 1 decimal place, in "
                   "cm." % (ang, known), _r1(known * math.tan(rad)), "num", {"unit": "cm"}, ["opp = adj × tan %d°." % ang], tol=0.051)

    def t_hyp_from_opp():
        return _tb("In a right-angled triangle the side opposite an angle of %d° is %d cm. Find the hypotenuse, to 1 decimal place, in cm."
                   % (ang, known), _r1(known / math.sin(rad)), "num", {"unit": "cm"}, ["hyp = opp ÷ sin %d°." % ang], tol=0.051)

    def t_which_ratio():
        give, want, ans = pick([("the hypotenuse", "the opposite side", "sin"), ("the hypotenuse", "the adjacent side", "cos"),
                                ("the adjacent side", "the opposite side", "tan")])
        return _wq("You know an angle and %s, and want %s. Which ratio do you use: sin, cos or tan?" % (give, want), ans,
                   ["SOH CAH TOA."], "sin / cos / tan")

    def t_ladder():
        L = random.randint(4, 10)
        return _tb("A %d m ladder leans against a wall at %d° to the ground. How high up the wall does it reach, to 1 decimal place, in m?"
                   % (L, ang), _r1(L * math.sin(rad)), "num", {"unit": "m"}, ["height = %d × sin %d°." % (L, ang)], tol=0.051)

    return _pick_t([t_opp_from_hyp, t_adj_from_hyp, t_opp_from_adj, t_hyp_from_opp, t_which_ratio, t_ladder])


@skill("Y9.6.b", "Trigonometry: find a missing angle", S6)
def _(d=1):
    d = _d(d)
    a, b = random.randint(3, 15), random.randint(3, 15)
    h = max(a, b) + random.randint(1, 8)

    def t_tan():
        return _tb("A right-angled triangle has opposite %d cm and adjacent %d cm. Find the angle, to 1 decimal place, in degrees." % (a, b),
                   _r1(math.degrees(math.atan(a / b))), "num", {"unit": "°"}, ["angle = tan⁻¹(%d/%d)." % (a, b)], tol=0.051)

    def t_sin():
        return _tb("A right-angled triangle has opposite %d cm and hypotenuse %d cm. Find the angle, to 1 decimal place, in degrees." % (a, h),
                   _r1(math.degrees(math.asin(a / h))), "num", {"unit": "°"}, ["angle = sin⁻¹(%d/%d)." % (a, h)], tol=0.051)

    def t_cos():
        return _tb("A right-angled triangle has adjacent %d cm and hypotenuse %d cm. Find the angle, to 1 decimal place, in degrees." % (b, h),
                   _r1(math.degrees(math.acos(b / h))), "num", {"unit": "°"}, ["angle = cos⁻¹(%d/%d)." % (b, h)], tol=0.051)

    def t_ramp():
        rise, run = random.randint(1, 4), random.randint(8, 20)
        return _tb("A ramp rises %d m over a horizontal distance of %d m. What angle does it make with the ground, to 1 decimal place?" % (rise, run),
                   _r1(math.degrees(math.atan(rise / run))), "num", {"unit": "°"}, ["tan⁻¹(%d/%d)." % (rise, run)], tol=0.051)

    def t_exact():
        r, ang = pick([("sin", 30), ("cos", 60), ("tan", 45)])
        val = {"sin": "0.5", "cos": "0.5", "tan": "1"}[r]
        return _tb("%s x = %s, and x is between 0° and 90°. What is x?" % (r, val), ang, "int", {"unit": "°"}, ["%s %d° = %s." % (r, ang, val)])

    return _pick_t([t_tan, t_sin, t_cos, t_ramp, t_exact])


@skill("Y9.6.c", "Pythagoras: shorter sides and problems", S6)
def _(d=1):
    d = _d(d)
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29)]

    def t_short():
        a, b, c = pick(triples)
        return _tb("A right-angled triangle has hypotenuse %d cm and one short side %d cm. Find the other side, in cm." % (c, a), b, "int",
                   {"unit": "cm"}, ["√(%d² − %d²) = √%d = %d." % (c, a, c * c - a * a, b)])

    def t_decimal():
        a, b = random.randint(3, 15), random.randint(3, 15)
        return _tb("Find the hypotenuse of a right-angled triangle with sides %d cm and %d cm, to 1 decimal place." % (a, b),
                   _r1(math.hypot(a, b)), "num", {"unit": "cm"}, ["√(%d + %d) = √%d." % (a * a, b * b, a * a + b * b)], tol=0.051)

    def t_diagonal():
        a, b = random.randint(3, 20), random.randint(3, 20)
        return _tb("A rectangle is %d m by %d m. How long is its diagonal, to 1 decimal place, in m?" % (a, b), _r1(math.hypot(a, b)),
                   "num", {"unit": "m"}, ["√(%d² + %d²)." % (a, b)], tol=0.051)

    def t_distance():
        x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
        a, b, c = pick(triples[:4])
        x2, y2 = x1 + a, y1 + b
        return _tb("Find the distance between (%d,%d) and (%d,%d)." % (x1, y1, x2, y2), c, "int", {},
                   ["Across %d, up %d: √(%d² + %d²) = %d." % (a, b, a, b, c)])

    def t_is_right():
        a, b, c = pick(triples)
        c2 = c + pick([0, 0, 1])
        return _wq("A triangle has sides %d, %d and %d. Is it right-angled? (yes or no)" % (a, b, c2), "yes" if c2 == c else "no",
                   ["%d² + %d² = %d; %d² = %d." % (a, b, a * a + b * b, c2, c2 * c2)], "yes / no")

    return _pick_t([t_short, t_decimal, t_diagonal, t_distance, t_is_right])


@skill("Y9.6.d", "Similar shapes: lengths and areas", S6)
def _(d=1):
    d = _d(d)
    k = pick([2, 3, 4, Fraction(3, 2), Fraction(5, 2)])
    a = random.randint(2, 10) * 2

    def t_length():
        return _tb("Two triangles are similar. A side of %d cm in the small one matches %s cm in the large one. Another side in the small "
                   "one is %d cm. How long is the matching side in the large one, in cm?" % (a, _ds(Fraction(a) * k), a + 2, ),
                   _ds(Fraction(a + 2) * k), "num", {"unit": "cm"}, ["Scale factor %s." % _ds(Fraction(k)), "%d × %s = %s." % (a + 2, _ds(Fraction(k)), _ds(Fraction(a + 2) * k))])

    def t_scale():
        return _tb("A photo %d cm wide is enlarged to %s cm wide. What is the scale factor?" % (a, _ds(Fraction(a) * k)), _ds(Fraction(k)),
                   "num", {}, ["%s ÷ %d = %s." % (_ds(Fraction(a) * k), a, _ds(Fraction(k)))])

    def t_area():
        sf = pick([2, 3, 4, 5])
        A = random.randint(3, 20)
        return _tb("Two similar shapes have lengths in the ratio 1:%d. The small one has area %d cm². What is the area of the large one, in cm²?"
                   % (sf, A), A * sf * sf, "int", {"unit": "cm²"}, ["Area scale factor = %d² = %d." % (sf, sf * sf), "%d × %d = %d." % (A, sf * sf, A * sf * sf)])

    def t_shadow():
        h, s = random.randint(1, 3), random.randint(2, 5)
        tree_s = s * random.randint(3, 8)
        return _tb("A %d m pole casts a %d m shadow. At the same time a tree casts a %d m shadow. How tall is the tree, in m?" % (h, s, tree_s),
                   _ds(Fraction(h * tree_s, s)), "num", {"unit": "m"}, ["Same ratio: %d × %d ÷ %d = %s." % (h, tree_s, s, _ds(Fraction(h * tree_s, s)))])

    def t_angle():
        x = random.randint(20, 120)
        return _tb("Two triangles are similar. One has an angle of %d°. What is the matching angle in the other triangle?" % x, x, "int",
                   {"unit": "°"}, ["Similar shapes have equal angles."])

    return _pick_t([t_length, t_scale, t_area, t_shadow, t_angle])


@skill("Y9.6.e", "Congruence criteria and angle reasoning", S6)
def _(d=1):
    d = _d(d)

    def t_criteria():
        q, a = pick([("Two triangles have all three pairs of sides equal. Which congruence rule is this?", "SSS"),
                     ("Two triangles have two sides and the angle between them equal. Which rule?", "SAS"),
                     ("Two triangles have two angles and the side between them equal. Which rule?", "ASA"),
                     ("Two right-angled triangles have equal hypotenuses and one other equal side. Which rule?", "RHS")])
        return _wq(q + " (SSS, SAS, ASA or RHS)", a, ["The conditions match %s." % a], "SSS / SAS / ASA / RHS")

    def t_aaa():
        return _wq("Two triangles have all three angles equal. Must they be congruent? (yes or no)", "no",
                   ["Equal angles mean similar, not necessarily the same size."], "yes / no")

    def t_parallel_triangle():
        x, y = random.randint(30, 80), random.randint(30, 80)
        return _tb("In a triangle, one angle is alternate to an angle of %d° and another is corresponding to an angle of %d°. Find the third "
                   "angle." % (x, y), 180 - x - y, "int", {"unit": "°"}, ["Alternate and corresponding angles are equal.", "180 − %d − %d = %d." % (x, y, 180 - x - y)])

    def t_isos_exterior():
        apex = random.randint(20, 100) // 2 * 2
        return _tb("An isosceles triangle has apex angle %d°. Find the exterior angle at one of the base corners." % apex,
                   180 - (180 - apex) // 2, "int", {"unit": "°"}, ["Base angle = %d°." % ((180 - apex) // 2), "Exterior = 180 − %d." % ((180 - apex) // 2)])

    def t_polygon():
        n = pick([5, 6, 8, 9, 10, 12])
        return _tb("A regular polygon has %d sides. Find the size of one interior angle." % n, 180 - 360 // n, "int", {"unit": "°"},
                   ["Exterior = 360 ÷ %d = %d." % (n, 360 // n), "Interior = 180 − %d." % (360 // n)]) if 360 % n == 0 else \
            _tb("Find the sum of the interior angles of a %d-sided polygon." % n, (n - 2) * 180, "int", {"unit": "°"}, ["(%d − 2) × 180." % n])

    def t_co_interior():
        x = random.randint(40, 140)
        return _tb("Two angles between a pair of parallel lines are co-interior (they form a C shape). One is %d°. Find the other." % x, 180 - x,
                   "int", {"unit": "°"}, ["Co-interior angles add to 180°."])

    return _pick_t([t_criteria, t_aaa, t_parallel_triangle, t_isos_exterior, t_polygon, t_co_interior])


@skill("Y9.6.f", "Loci and perpendicular distance", S6)
def _(d=1):
    d = _d(d)

    def t_locus_point():
        return _wq("The set of points exactly 3 cm from a fixed point forms what shape? (one word)", "circle",
                   ["All points the same distance from a point lie on a circle."], "one word")

    def t_locus_two():
        return _wq("Points that are the same distance from A and from B lie on which line? (two words: the perpendicular ...)", "bisector",
                   ["It is the perpendicular bisector of AB."], "one word")

    def t_angle_bisector():
        return _wq("Points the same distance from two lines that meet lie on which line? (two words: the angle ...)", "bisector",
                   ["It is the angle bisector."], "one word")

    def t_goat():
        r = random.randint(2, 10)
        return _tb("A goat is tied to a post with a rope %d m long. It can graze inside a circle. What is the greatest distance it can reach "
                   "from the post, in m?" % r, r, "int", {"unit": "m"}, ["The radius is the rope length."])

    def t_perp():
        x0, y0 = random.randint(-4, 4), random.randint(1, 6)
        return _tb("What is the shortest distance from the point (%d,%d) to the x-axis?" % (x0, y0), y0, "int", {},
                   ["The perpendicular distance is the y-coordinate: %d." % y0])

    return _pick_t([t_locus_point, t_locus_two, t_angle_bisector, t_goat, t_perp])


# ================================================================== 9.7 ======
@skill("Y9.7.a", "Circles, semicircles and quarter circles", S7)
def _(d=1):
    d = _d(d)
    r = random.randint(2, 15)

    def t_area_pi():
        return _tb("A circle has radius %d cm. Its area is kπ cm². What is k?" % r, r * r, "int", {}, ["A = πr² = %dπ." % (r * r)])

    def t_circ():
        return _tb("A circle has diameter %d cm. Find its circumference, to 1 decimal place, in cm." % (2 * r), _r1(math.pi * 2 * r), "num",
                   {"unit": "cm"}, ["C = πd = %.3f." % (math.pi * 2 * r)], tol=0.051)

    def t_semi_area():
        return _tb("Find the area of a semicircle with radius %d cm, to 1 decimal place, in cm²." % r, _r1(math.pi * r * r / 2), "num",
                   {"unit": "cm²"}, ["½πr² = %.3f." % (math.pi * r * r / 2)], tol=0.051)

    def t_semi_perim():
        return _tb("Find the perimeter of a semicircle with diameter %d cm (curved part plus the straight edge), to 1 decimal place, in cm."
                   % (2 * r), _r1(math.pi * r + 2 * r), "num", {"unit": "cm"}, ["πr + 2r = %.3f." % (math.pi * r + 2 * r)], tol=0.051)

    def t_quarter():
        return _tb("Find the area of a quarter circle with radius %d cm, to 1 decimal place, in cm²." % r, _r1(math.pi * r * r / 4), "num",
                   {"unit": "cm²"}, ["¼πr² = %.3f." % (math.pi * r * r / 4)], tol=0.051)

    def t_radius_from_area():
        return _tb("A circle has area %dπ cm². What is its radius, in cm?" % (r * r), r, "int", {"unit": "cm"}, ["r² = %d, r = %d." % (r * r, r)])

    def t_pic():
        return {"prompt": "Find the area of this circle, to 1 decimal place, in cm².", "component": "circle",
                "spec": {"radius": r, "show": "radius", "label": "r = %d cm" % r}, "answer": _r1(math.pi * r * r), "answer_type": "num",
                "tolerance": 0.051, "solution": ["πr² = π × %d = %.3f." % (r * r, math.pi * r * r)]}

    return _pick_t([t_area_pi, t_circ, t_semi_area, t_semi_perim, t_quarter, t_radius_from_area], [t_pic])


@skill("Y9.7.b", "Surface area of cuboids, prisms and cylinders", S7)
def _(d=1):
    d = _d(d)

    def t_cuboid():
        l, w, h = random.randint(2, 12), random.randint(2, 10), random.randint(2, 10)
        return _tb("Find the surface area of a cuboid %d cm × %d cm × %d cm, in cm²." % (l, w, h), 2 * (l * w + l * h + w * h), "int",
                   {"unit": "cm²"}, ["2(%d + %d + %d) = %d." % (l * w, l * h, w * h, 2 * (l * w + l * h + w * h))])

    def t_cube():
        s = random.randint(2, 12)
        return _tb("A cube has edges of %d cm. Find its surface area, in cm²." % s, 6 * s * s, "int", {"unit": "cm²"}, ["6 × %d² = %d." % (s, 6 * s * s)])

    def t_tri_prism():
        a, b, c = pick([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
        L = random.randint(5, 20)
        sa = a * b + L * (a + b + c)
        return _tb("A triangular prism has a right-angled triangle end with sides %d, %d and %d cm, and length %d cm. Find its surface area, in "
                   "cm²." % (a, b, c, L), sa, "int", {"unit": "cm²"}, ["Two ends: 2 × ½ × %d × %d = %d." % (a, b, a * b),
                                                                     "Three rectangles: %d × (%d + %d + %d) = %d." % (L, a, b, c, L * (a + b + c))])

    def t_cylinder_pi():
        r, h = random.randint(2, 10), random.randint(2, 15)
        return _tb("A closed cylinder has radius %d cm and height %d cm. Its surface area is kπ cm². What is k?" % (r, h), 2 * r * r + 2 * r * h,
                   "int", {}, ["2πr² + 2πrh = %dπ + %dπ." % (2 * r * r, 2 * r * h)])

    def t_cube_from_sa():
        s = random.randint(2, 10)
        return _tb("A cube has surface area %d cm². How long is each edge, in cm?" % (6 * s * s), s, "int", {"unit": "cm"},
                   ["One face = %d ÷ 6 = %d; edge = %d." % (6 * s * s, s * s, s)])

    def t_net():
        return {"prompt": "This is the net of a cuboid. How many rectangular faces does it have?", "component": "net",
                "spec": {"solid": "cuboid"}, "answer": 6, "answer_type": "int", "solution": ["A cuboid has 6 faces."]}

    return _pick_t([t_cuboid, t_cube, t_tri_prism, t_cylinder_pi, t_cube_from_sa], [t_net])


@skill("Y9.7.c", "Volume of prisms and cylinders", S7)
def _(d=1):
    d = _d(d)

    def t_prism():
        A, L = random.randint(5, 40), random.randint(3, 20)
        return _tb("A prism has cross-section area %d cm² and length %d cm. Find its volume, in cm³." % (A, L), A * L, "int", {"unit": "cm³"},
                   ["V = %d × %d = %d." % (A, L, A * L)])

    def t_tri_prism():
        b, h, L = random.randint(2, 12) * 2, random.randint(2, 10), random.randint(3, 15)
        return _tb("A triangular prism has a triangle end with base %d cm and height %d cm, and length %d cm. Find its volume, in cm³." % (b, h, L),
                   b * h // 2 * L, "int", {"unit": "cm³"}, ["½ × %d × %d = %d; × %d = %d." % (b, h, b * h // 2, L, b * h // 2 * L)])

    def t_cylinder():
        r, h = random.randint(2, 10), random.randint(2, 15)
        return _tb("Find the volume of a cylinder with radius %d cm and height %d cm, to 1 decimal place, in cm³." % (r, h),
                   _r1(math.pi * r * r * h), "num", {"unit": "cm³"}, ["πr²h = %.3f." % (math.pi * r * r * h)], tol=0.051)

    def t_cylinder_pi():
        r, h = random.randint(2, 10), random.randint(2, 15)
        return _tb("A cylinder has radius %d cm and height %d cm. Its volume is kπ cm³. What is k?" % (r, h), r * r * h, "int", {},
                   ["πr²h = %dπ." % (r * r * h)])

    def t_height():
        A, h = random.randint(4, 30), random.randint(2, 15)
        return _tb("A prism has volume %d cm³ and cross-section area %d cm². How long is it, in cm?" % (A * h, A), h, "int", {"unit": "cm"},
                   ["%d ÷ %d = %d." % (A * h, A, h)])

    def t_litres():
        l, w, h = random.randint(10, 50), random.randint(10, 40), random.randint(10, 30)
        return _tb("A tank is %d cm × %d cm × %d cm. How many litres does it hold? (1 litre = 1000 cm³)" % (l, w, h), _ds(Fraction(l * w * h, 1000)),
                   "num", {"unit": "litres"}, ["%d cm³ ÷ 1000." % (l * w * h)])

    return _pick_t([t_prism, t_tri_prism, t_cylinder, t_cylinder_pi, t_height, t_litres])


@skill("Y9.7.d", "Convert area and volume units", S7)
def _(d=1):
    d = _d(d)

    def t_m2_cm2():
        k = random.randint(2, 9)
        return _tb("How many cm² are in %d m²?" % k, k * 10000, "int", {"unit": "cm²"}, ["1 m² = 100 × 100 = 10,000 cm²."])

    def t_cm2_mm2():
        k = random.randint(2, 30)
        return _tb("How many mm² are in %d cm²?" % k, k * 100, "int", {"unit": "mm²"}, ["1 cm² = 10 × 10 = 100 mm²."])

    def t_cm2_m2():
        k = random.randint(1, 99) * 1000
        return _tb("Convert %s cm² to m²." % _c(k), _ds(Fraction(k, 10000)), "num", {"unit": "m²"}, ["÷ 10,000."])

    def t_cm3_m3():
        k = random.randint(1, 5)
        return _tb("How many cm³ are in %d m³?" % k, k * 1_000_000, "int", {"unit": "cm³"}, ["1 m³ = 100³ = 1,000,000 cm³."])

    def t_ml():
        k = random.randint(1, 3000)
        return _tb("A container holds %d cm³. How many ml is that?" % k, k, "int", {"unit": "ml"}, ["1 cm³ = 1 ml."])

    def t_trap():
        return _wq("True or false: 1 m² = 100 cm².", "false", ["1 m² = 100 cm × 100 cm = 10,000 cm²."], "true / false")

    return _pick_t([t_m2_cm2, t_cm2_mm2, t_cm2_m2, t_cm3_m3, t_ml, t_trap])
