# Year 9 generators: strands 9.6 and 9.7.
#
# Geometry: trigonometry in right-angled triangles (sides and angles), Pythagoras in context and for a
# shorter side, similar shapes (lengths and areas), congruence criteria, multi-step angle reasoning,
# loci.  Mensuration: circles, semicircles and quarter circles; surface area of cuboids, prisms and
# cylinders; volume of prisms and cylinders; converting area and volume units.
import math

from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403
from .y9_gen_a import _a

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
        return _tb("%s %d m ladder leans against a wall at %d° to the ground. How high up the wall does it reach, to 1 decimal place, in m?"
                   % (_a(L).capitalize(), L, ang), _r1(L * math.sin(rad)), "num", {"unit": "m"}, ["height = %d × sin %d°." % (L, ang)], tol=0.051)

    def t_adj_from_opp():
        return _tb("In a right-angled triangle, the side opposite an angle of %d° is %d cm. Find the side adjacent to that angle, to 1 decimal "
                   "place, in cm." % (ang, known), _r1(known / math.tan(rad)), "num", {"unit": "cm"}, ["adj = opp ÷ tan %d°." % ang], tol=0.051)

    def t_hyp_from_adj():
        return _tb("The side adjacent to an angle of %d° in a right-angled triangle is %d cm. Find the hypotenuse, to 1 decimal place, in cm."
                   % (ang, known), _r1(known / math.cos(rad)), "num", {"unit": "cm"}, ["hyp = adj ÷ cos %d°." % ang], tol=0.051)

    def t_elevation():
        dist = random.randint(10, 60)
        return _tb("From a point %d m from the foot of a tree, the angle of elevation to the top is %d°. How tall is the tree, to 1 decimal "
                   "place, in m?" % (dist, ang), _r1(dist * math.tan(rad)), "num", {"unit": "m"}, ["height = %d × tan %d°." % (dist, ang)], tol=0.051)

    def t_plane():
        a2, km = random.randint(5, 20), random.randint(2, 12)
        return _tb("A plane climbs in a straight line at %d° to the ground. After flying %d km along that line, how high is it, to 1 decimal "
                   "place, in km?" % (a2, km), _r1(km * math.sin(math.radians(a2))), "num", {"unit": "km"},
                   ["height = %d × sin %d°." % (km, a2)], tol=0.051)

    def t_isosceles():
        side, base_ang = random.randint(5, 15), random.randint(30, 75)
        return _tb("An isosceles triangle has two equal sides of %d cm and base angles of %d°. Find the length of the base, to 1 decimal place, "
                   "in cm." % (side, base_ang), _r1(2 * side * math.cos(math.radians(base_ang))), "num", {"unit": "cm"},
                   ["Split it into two right-angled triangles: half the base = %d × cos %d°." % (side, base_ang),
                    "Base = 2 × %.3f." % (side * math.cos(math.radians(base_ang)))], tol=0.051)

    def t_value():
        f, name = pick([(math.sin, "sin"), (math.cos, "cos"), (math.tan, "tan")])
        return _tb("Use a calculator: give %s %d° to 3 decimal places." % (name, ang), round(f(rad) + 1e-12, 3), "num", {},
                   ["%s %d° = %.5f." % (name, ang, f(rad))], tol=0.0005)

    return _pick_t([t_opp_from_hyp, t_adj_from_hyp, t_opp_from_adj, t_hyp_from_opp, t_which_ratio, t_ladder, t_adj_from_opp, t_hyp_from_adj,
                    t_elevation, t_plane, t_isosceles, t_value])


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

    def t_elevation():
        hgt, dist = random.randint(5, 40), random.randint(10, 60)
        return _tb("A building is %d m tall. You stand %d m from its base. What is the angle of elevation to the top, to 1 decimal place?"
                   % (hgt, dist), _r1(math.degrees(math.atan(hgt / dist))), "num", {"unit": "°"}, ["tan⁻¹(%d/%d)." % (hgt, dist)], tol=0.051)

    def t_ladder():
        L = random.randint(4, 10)
        up = random.randint(2, L - 1)
        return _tb("%s %d m ladder reaches %d m up a wall. What angle does it make with the ground, to 1 decimal place?" % (_a(L).capitalize(), L, up),
                   _r1(math.degrees(math.asin(up / L))), "num", {"unit": "°"}, ["sin⁻¹(%d/%d)." % (up, L)], tol=0.051)

    def t_which():
        s1, s2, ans = pick([("opposite", "hypotenuse", "sin"), ("adjacent", "hypotenuse", "cos"), ("opposite", "adjacent", "tan")])
        return _wq("You know the %s and the %s and want the angle. Which inverse do you use? (type sin, cos or tan)" % (s1, s2), ans,
                   ["SOH CAH TOA: %s uses %s and %s." % (ans, s1, s2)], "sin / cos / tan")

    def t_line_angle():
        x2, y2 = random.randint(1, 7), random.randint(1, 7)
        return {"prompt": "What angle does the line from O(0,0) to P make with the x-axis? Give it to 1 decimal place.", "component": "coordinate_grid",
                "spec": {"xmin": -1, "xmax": 8, "ymin": -1, "ymax": 8, "lines": [{"p1": [0, 0], "p2": [x2, y2]}],
                         "points": [[0, 0, "O"], [x2, y2, "P"]], "typed": True, "placeholder": "degrees"},
                "answer": _r1(math.degrees(math.atan2(y2, x2))), "answer_type": "num", "tolerance": 0.051,
                "solution": ["Up %d, across %d: tan⁻¹(%d/%d) = %.2f°." % (y2, x2, y2, x2, math.degrees(math.atan2(y2, x2)))]}

    def t_apex():
        L, base = random.randint(6, 15), random.randint(3, 10)
        return _tb("An isosceles triangle has equal sides of %d cm and a base of %d cm. Find the angle at the top (between the equal sides), "
                   "to 1 decimal place." % (L, base), _r1(2 * math.degrees(math.asin(base / 2 / L))), "num", {"unit": "°"},
                   ["Half the angle = sin⁻¹(%s/%d)." % (_ds(Fraction(base, 2)), L), "Double it."], tol=0.051)

    def t_third():
        return _tb("A right-angled triangle has opposite %d cm and adjacent %d cm for angle A. Find the OTHER acute angle, to 1 decimal place."
                   % (a, b), _r1(90 - math.degrees(math.atan(a / b))), "num", {"unit": "°"},
                   ["A = tan⁻¹(%d/%d) = %.2f°." % (a, b, math.degrees(math.atan(a / b))), "The other is 90° − A."], tol=0.051)

    return _pick_t([t_tan, t_sin, t_cos, t_ramp, t_exact, t_elevation, t_ladder, t_which, t_apex, t_third], [t_line_angle])


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

    def t_ladder():
        a, b, c = pick(triples)
        return _tb("A %d m ladder leans against a wall with its foot %d m from the wall. How high up the wall does it reach, in m?" % (c, a), b,
                   "int", {"unit": "m"}, ["√(%d² − %d²) = √%d = %d." % (c, a, c * c - a * a, b)])

    def t_isos_height():
        a, b, c = pick(triples)
        return _tb("An isosceles triangle has two sides of %d cm and a base of %d cm. Find its perpendicular height, in cm." % (c, 2 * a), b, "int",
                   {"unit": "cm"}, ["Half the base is %d cm." % a, "√(%d² − %d²) = %d." % (c, a, b)])

    def t_perimeter():
        a, b, c = pick(triples)
        return _tb("The two shorter sides of a right-angled triangle are %d cm and %d cm. What is its perimeter, in cm?" % (a, b), a + b + c,
                   "int", {"unit": "cm"}, ["Hypotenuse = √(%d + %d) = %d." % (a * a, b * b, c), "%d + %d + %d = %d." % (a, b, c, a + b + c)])

    def t_grid():
        dx, dy = random.choice([(3, 4), (4, 3), (3, 3), (2, 5), (5, 2), (4, 4), (1, 6), (6, 1), (2, 3), (5, 5)])
        sx, sy = pick([1, -1]), pick([1, -1])
        x1, y1 = random.randint(-6, 6 - dx) if sx > 0 else random.randint(-6 + dx, 6), random.randint(-6, 6 - dy) if sy > 0 else random.randint(-6 + dy, 6)
        x2, y2 = x1 + sx * dx, y1 + sy * dy
        return {"prompt": "Find the distance AB, to 1 decimal place.", "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "points": [[x1, y1, "A"], [x2, y2, "B"]],
                         "lines": [{"p1": [x1, y1], "p2": [x2, y2], "dashed": True}], "typed": True, "placeholder": "length"},
                "answer": _r1(math.hypot(dx, dy)), "answer_type": "num", "tolerance": 0.051,
                "solution": ["Across %d, up/down %d." % (dx, dy), "√(%d + %d) = √%d ≈ %.3f." % (dx * dx, dy * dy, dx * dx + dy * dy, math.hypot(dx, dy))]}

    def t_square_diag():
        dg = random.randint(4, 20)
        return _tb("A square has a diagonal of %d cm. How long is each side, to 1 decimal place, in cm?" % dg, _r1(dg / math.sqrt(2)), "num",
                   {"unit": "cm"}, ["s² + s² = %d², so s² = %s." % (dg, _ds(Fraction(dg * dg, 2))), "s = √%s ≈ %.3f." % (_ds(Fraction(dg * dg, 2)), dg / math.sqrt(2))],
                   tol=0.051)

    def t_short_decimal():
        h = random.randint(8, 20)
        a = random.randint(2, h - 2)
        return _tb("The hypotenuse of a right-angled triangle is %d cm and one other side is %d cm. Find the third side, to 1 decimal place, in "
                   "cm." % (h, a), _r1(math.sqrt(h * h - a * a)), "num", {"unit": "cm"}, ["√(%d − %d) = √%d." % (h * h, a * a, h * h - a * a)], tol=0.051)

    return _pick_t([t_short, t_decimal, t_diagonal, t_distance, t_is_right, t_ladder, t_isos_height, t_perimeter, t_square_diag,
                    t_short_decimal], [t_grid])


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
        return _tb("A %d m pole casts a %d m shadow. At the same time a tree casts %s %d m shadow. How tall is the tree, in m?" % (h, s, _a(tree_s), tree_s),
                   _ds(Fraction(h * tree_s, s)), "num", {"unit": "m"}, ["Same ratio: %d × %d ÷ %d = %s." % (h, tree_s, s, _ds(Fraction(h * tree_s, s)))])

    def t_angle():
        x, y = random.randint(20, 80), random.randint(20, 80)
        return _tb("Two triangles are similar. The small one has angles of %d° and %d°. The large one is %s times bigger. What is the third "
                   "angle of the LARGE triangle?" % (x, y, _ds(Fraction(k))), 180 - x - y, "int", {"unit": "°"},
                   ["Enlarging does not change angles.", "180 − %d − %d = %d." % (x, y, 180 - x - y)])

    def t_area_back():
        sf = random.randint(2, 5)
        small = random.randint(2, 9)
        A = random.randint(2, 12)
        return _tb("Two similar shapes have areas %d cm² and %d cm². A side of the smaller shape is %d cm. How long is the matching side of the "
                   "larger shape, in cm?" % (A, A * sf * sf, small), small * sf, "int", {"unit": "cm"},
                   ["Area scale factor %d ÷ %d = %d." % (A * sf * sf, A, sf * sf), "Length scale factor √%d = %d." % (sf * sf, sf),
                    "%d × %d = %d." % (small, sf, small * sf)])

    def t_nested():
        ad, scale = random.randint(2, 8), pick([Fraction(3, 2), 2, Fraction(5, 2), 3])
        ab = Fraction(ad) * scale
        de = random.randint(2, 9) * 2
        return _tb("In triangle ABC, D is on AB and E is on AC, with DE parallel to BC. AD = %d cm, AB = %s cm and DE = %d cm. Find BC, in cm."
                   % (ad, _ds(ab), de), _ds(de * scale), "num", {"unit": "cm"},
                   ["Triangles ADE and ABC are similar, scale factor %s ÷ %d = %s." % (_ds(ab), ad, _ds(Fraction(scale))), "BC = %d × %s = %s." % (de, _ds(Fraction(scale)), _ds(de * scale))])

    def t_reduce():
        k2 = pick([Fraction(2, 5), Fraction(3, 5), Fraction(1, 5), Fraction(4, 5), Fraction(1, 2), Fraction(3, 4)])
        side = random.randint(2, 9) * 5
        return _tb("A shape is enlarged by scale factor %s, which makes it smaller. A side of %d cm becomes how long, in cm?" % (_fs(k2), side),
                   _ds(side * k2), "num", {"unit": "cm"}, ["%d × %s = %s." % (side, _fs(k2), _ds(side * k2))])

    def t_perimeter():
        sf, P = random.randint(2, 6), random.randint(8, 40)
        return _tb("Two shapes are similar with scale factor %d. The smaller has a perimeter of %d cm. What is the perimeter of the larger, in cm?"
                   % (sf, P), sf * P, "int", {"unit": "cm"}, ["Perimeter is a length, so multiply by %d." % sf])

    def t_are_similar():
        w, h = random.randint(2, 6), random.randint(3, 9)
        k = pick([Fraction(3, 2), 2, Fraction(5, 2), 3])
        ok = random.random() < 0.5
        w2, h2 = Fraction(w) * k, Fraction(h) * k + (0 if ok else 1)
        return _wq("Is a %d cm by %d cm rectangle similar to %s %s cm by %s cm rectangle? (yes or no)" % (w, h, _a(_ds(w2)), _ds(w2), _ds(h2)),
                   "yes" if ok else "no", ["%s ÷ %d = %s and %s ÷ %d = %s." % (_ds(w2), w, _fs(w2 / w), _ds(h2), h, _fs(h2 / h)),
                                           "Similar only if both scale factors match."], "yes / no")

    def t_length_sf_from_area():
        sf = random.randint(2, 7)
        return _tb("The area of a shape is multiplied by %d when it is enlarged. What is the length scale factor?" % (sf * sf), sf, "int", {},
                   ["Area scale factor = (length scale factor)², so √%d = %d." % (sf * sf, sf)])

    return _pick_t([t_length, t_scale, t_area, t_shadow, t_angle, t_area_back, t_nested, t_reduce, t_perimeter, t_are_similar,
                    t_length_sf_from_area])


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
            _tb("Find the sum of the interior angles of %s %d-sided polygon." % (_a(n), n), (n - 2) * 180, "int", {"unit": "°"}, ["(%d − 2) × 180." % n])

    def t_co_interior():
        x = random.randint(40, 140)
        return _tb("Two angles between a pair of parallel lines are co-interior (they form a C shape). One is %d°. Find the other." % x, 180 - x,
                   "int", {"unit": "°"}, ["Co-interior angles add to 180°."])

    def t_not_proof():
        return _wq("Which of these does NOT prove two triangles are congruent: SSS, SAS, AAA or RHS?", "AAA",
                   ["Equal angles alone give similar triangles, which can be different sizes."], "SSS / SAS / AAA / RHS")

    def t_ssa():
        return _wq("Two triangles have two pairs of equal sides and an equal angle that is NOT between them. Must they be congruent? (yes or no)",
                   "no", ["Side-side-angle (with the angle not between the sides) can give two different triangles."], "yes / no")

    def t_matching_side():
        sides = random.sample(range(4, 15), 3)
        names = [("AB", "DE"), ("BC", "EF"), ("AC", "DF")]
        k = random.randrange(3)
        return _tb("Triangle ABC is congruent to triangle DEF (A matches D, B matches E, C matches F). AB = %d cm, BC = %d cm and AC = %d cm. "
                   "How long is %s, in cm?" % (sides[0], sides[1], sides[2], names[k][1]), sides[k], "int", {"unit": "cm"},
                   ["%s matches %s, so it is %d cm." % (names[k][1], names[k][0], sides[k])])

    def t_matching_angle():
        A = random.randint(30, 80)
        B = random.randint(30, 150 - A)
        C = 180 - A - B
        letter, val = "F", C
        return _tb("Triangle ABC is congruent to triangle DEF (A matches D, B matches E, C matches F). Angle A = %d° and angle B = %d°. "
                   "What is angle %s?" % (A, B, letter), val, "int", {"unit": "°"},
                   ["Angle C = 180 − %d − %d = %d." % (A, B, C), "Angle %s matches angle %s: %d°." % (letter, "ABC"["DEF".index(letter)], val)])

    def t_exterior_sum():
        x, y = random.randint(25, 80), random.randint(25, 80)
        return _tb("Two interior angles of a triangle are %d° and %d°. Find the exterior angle at the third corner." % (x, y), x + y, "int",
                   {"unit": "°"}, ["The exterior angle equals the sum of the two opposite interior angles: %d + %d = %d." % (x, y, x + y)])

    def t_polygon_sides():
        n = pick([5, 6, 8, 9, 10, 12, 15, 18, 20])
        return _tb("Each exterior angle of a regular polygon is %d°. How many sides does it have?" % (360 // n), n, "int", {},
                   ["360 ÷ %d = %d." % (360 // n, n)])

    return _pick_t([t_criteria, t_aaa, t_parallel_triangle, t_isos_exterior, t_polygon, t_co_interior, t_not_proof, t_ssa, t_matching_side,
                    t_matching_angle, t_exterior_sum, t_polygon_sides])


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

    def t_y_axis():
        x0, y0 = random.choice([v for v in range(-7, 8) if v]), random.randint(-6, 6)
        return _tb("What is the shortest distance from the point (%d,%d) to the y-axis?" % (x0, y0), abs(x0), "int", {},
                   ["The perpendicular distance to the y-axis is the size of the x-coordinate: %d." % abs(x0)])

    def t_horizontal():
        x0, y0, k = random.randint(-5, 5), random.randint(-6, 6), random.randint(-6, 6)
        if y0 == k:
            k += 2
        return _tb("What is the shortest distance from the point (%d,%d) to the line y = %d?" % (x0, y0, k), abs(y0 - k), "int", {},
                   ["The line is horizontal, so measure straight up or down: |%d − (%d)| = %d." % (y0, k, abs(y0 - k))])

    def t_vertical():
        x0, y0, k = random.randint(-6, 6), random.randint(-5, 5), random.randint(-6, 6)
        if x0 == k:
            k -= 3
        return _tb("What is the shortest distance from the point (%d,%d) to the line x = %d?" % (x0, y0, k), abs(x0 - k), "int", {},
                   ["The line is vertical, so measure straight across: |%d − (%d)| = %d." % (x0, k, abs(x0 - k))])

    def t_parallel_lines():
        return _wq("The set of points exactly 2 cm from a long straight line forms two lines. How are they placed compared with the first line? "
                   "(one word)", "parallel", ["They are two lines parallel to it, one on each side."], "one word")

    def t_corner_goat():
        r = random.randint(1, 6) * 2
        return _tb("A goat is tied to the corner of a rectangular field with %s %d m rope. It can graze a quarter circle. Its grazing area is "
                   "kπ m². What is k?" % (_a(r), r), r * r // 4, "int", {}, ["¼ × π × %d² = %dπ." % (r, r * r // 4)])

    def t_midpoint():
        x1, y1 = random.randint(-6, 0), random.randint(-6, 4)
        x2, y2 = x1 + 2 * random.randint(1, 3), y1 + 2 * random.randint(-2, 3)
        if not -7 <= y2 <= 7:
            y2 = y1 + 2
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return {"prompt": "The perpendicular bisector of AB crosses AB at a point. Type that point like (2,-3).", "component": "coordinate_grid",
                "spec": {"xmin": -7, "xmax": 7, "ymin": -7, "ymax": 7, "points": [[x1, y1, "A"], [x2, y2, "B"]],
                         "lines": [{"p1": [x1, y1], "p2": [x2, y2]}], "typed": True, "placeholder": "(x,y)"},
                "answer": "(%d,%d)" % (mx, my), "answer_type": "coord",
                "solution": ["It crosses AB at its midpoint: ((%d + %d)/2, (%d + %d)/2) = (%d,%d)." % (x1, x2, y1, y2, mx, my)]}

    def t_equidistant():
        a = random.randint(-6, 4)
        b = a + 2 * random.randint(1, 5)
        return _tb("Which point on the x-axis is the same distance from (%d,0) and (%d,0)? Give its x-coordinate." % (a, b), (a + b) // 2, "int",
                   {}, ["It is halfway between: (%d + %d) ÷ 2 = %d." % (a, b, (a + b) // 2)])

    return _pick_t([t_locus_point, t_locus_two, t_angle_bisector, t_goat, t_perp, t_y_axis, t_horizontal, t_vertical, t_parallel_lines,
                    t_corner_goat, t_equidistant], [t_midpoint])


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

    def t_area_from_circ():
        return _tb("A circle has circumference %dπ cm. Its area is kπ cm². What is k?" % (2 * r), r * r, "int", {},
                   ["d = %d, so r = %d." % (2 * r, r), "A = π × %d² = %dπ." % (r, r * r)])

    def t_quarter_perim():
        return _tb("Find the perimeter of a quarter circle with radius %d cm (the arc plus two radii), to 1 decimal place, in cm." % r,
                   _r1(math.pi * r / 2 + 2 * r), "num", {"unit": "cm"}, ["Arc = 2π × %d ÷ 4 = %.3f." % (r, math.pi * r / 2), "+ 2 × %d." % r], tol=0.051)

    def t_ring():
        R = r + random.randint(1, 5)
        return _tb("A ring is the region between circles of radius %d cm and %d cm. Its area is kπ cm². What is k?" % (r, R), R * R - r * r, "int",
                   {}, ["%d²π − %d²π = %dπ." % (R, r, R * R - r * r)])

    def t_square_minus():
        return _tb("A circle of radius %d cm fits exactly inside a square. Find the area of the square NOT covered by the circle, to 1 decimal "
                   "place, in cm²." % r, _r1(4 * r * r - math.pi * r * r), "num", {"unit": "cm²"},
                   ["Square: %d × %d = %d." % (2 * r, 2 * r, 4 * r * r), "Circle: π × %d = %.3f." % (r * r, math.pi * r * r)], tol=0.051)

    def t_wheel():
        dcm, turns = pick([50, 60, 70, 80]), pick([10, 50, 100, 200])
        return _tb("A wheel has a diameter of %d cm. How far does it roll in %d full turns, to 1 decimal place, in metres?" % (dcm, turns),
                   _r1(math.pi * dcm * turns / 100), "num", {"unit": "m"},
                   ["One turn = π × %d cm." % dcm, "%d turns = %.2f cm = %.3f m." % (turns, math.pi * dcm * turns, math.pi * dcm * turns / 100)], tol=0.051)

    def t_diam_from_circ():
        C = random.randint(10, 90)
        return _tb("A circle has a circumference of %d cm. Find its diameter, to 1 decimal place, in cm." % C, _r1(C / math.pi), "num",
                   {"unit": "cm"}, ["d = C ÷ π = %.3f." % (C / math.pi)], tol=0.051)

    def t_pic_circ():
        return {"prompt": "Find the circumference of this circle, to 1 decimal place, in cm.", "component": "circle",
                "spec": {"radius": r, "show": "diameter", "label": "d = %d cm" % (2 * r)}, "answer": _r1(math.pi * 2 * r), "answer_type": "num",
                "tolerance": 0.051, "solution": ["πd = π × %d = %.3f." % (2 * r, math.pi * 2 * r)]}

    return _pick_t([t_area_pi, t_circ, t_semi_area, t_semi_perim, t_quarter, t_radius_from_area, t_area_from_circ, t_quarter_perim, t_ring,
                    t_square_minus, t_wheel, t_diam_from_circ], [t_pic, t_pic_circ])


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

    def t_cyl_decimal():
        r, h = random.randint(2, 10), random.randint(2, 15)
        return _tb("Find the total surface area of a closed cylinder with radius %d cm and height %d cm, to 1 decimal place, in cm²." % (r, h),
                   _r1(2 * math.pi * r * r + 2 * math.pi * r * h), "num", {"unit": "cm²"},
                   ["2πr² + 2πrh = %dπ ≈ %.3f." % (2 * r * r + 2 * r * h, 2 * math.pi * r * r + 2 * math.pi * r * h)], tol=0.051)

    def t_open_box():
        l, w, h = random.randint(3, 12), random.randint(2, 10), random.randint(2, 8)
        return _tb("An open box (no lid) is a cuboid %d cm long, %d cm wide and %d cm tall. What is its outside surface area, in cm²?" % (l, w, h),
                   l * w + 2 * l * h + 2 * w * h, "int", {"unit": "cm²"},
                   ["Base %d; two long sides %d; two short sides %d." % (l * w, 2 * l * h, 2 * w * h), "Total %d." % (l * w + 2 * l * h + 2 * w * h)])

    def t_curved():
        r, h = random.randint(2, 10), random.randint(2, 15)
        return _tb("The curved surface of a cylinder (a tube with no ends) has radius %d cm and height %d cm. Its area is kπ cm². What is k?"
                   % (r, h), 2 * r * h, "int", {}, ["Curved area = 2πrh = %dπ." % (2 * r * h)])

    def t_paint():
        s = random.randint(2, 5)
        cover = pick([5, 8, 10, 12])
        sa = 6 * s * s
        return _tb("A cube-shaped box with %d m edges is painted on every face. One tin of paint covers %d m². How many tins are needed?" % (s, cover),
                   -(-sa // cover), "int", {"unit": "tins"}, ["Surface area 6 × %d = %d m²." % (s * s, sa), "%d ÷ %d = %s, so %d tins." % (sa, cover, _ds(Fraction(sa, cover)), -(-sa // cover))])

    def t_missing_height():
        l, w, h = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
        return _tb("A cuboid is %d cm long and %d cm wide. Its surface area is %d cm². How tall is it, in cm?" % (l, w, 2 * (l * w + l * h + w * h)),
                   h, "int", {"unit": "cm"}, ["2(%d + %dh + %dh) = %d." % (l * w, l, w, 2 * (l * w + l * h + w * h)),
                                               "%dh = %d, h = %d." % (2 * (l + w), 2 * (l * w + l * h + w * h) - 2 * l * w, h)])

    def t_open_cyl():
        r, h = random.randint(2, 9), random.randint(3, 15)
        return _tb("A tin can has no lid: one circular base and a curved side. Its radius is %d cm and its height %d cm. Its outside surface "
                   "area is kπ cm². What is k?" % (r, h), r * r + 2 * r * h, "int", {},
                   ["Base πr² = %dπ." % (r * r), "Curved side 2πrh = %dπ." % (2 * r * h), "Total %dπ." % (r * r + 2 * r * h)])

    def t_net_solid():
        solid, faces = pick([("cube", 6), ("cuboid", 6), ("square_pyramid", 5), ("triangular_prism", 5)])
        return {"prompt": "This is the net of a 3-D solid. How many faces does the solid have?", "component": "net", "spec": {"solid": solid},
                "answer": faces, "answer_type": "int", "solution": ["Count the shapes in the net: %d faces." % faces]}

    return _pick_t([t_cuboid, t_cube, t_tri_prism, t_cylinder_pi, t_cube_from_sa, t_cyl_decimal, t_open_box, t_curved, t_paint,
                    t_missing_height, t_open_cyl], [t_net_solid])


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

    def t_cuboid_missing():
        l, w, h = random.randint(2, 12), random.randint(2, 10), random.randint(2, 12)
        return _tb("A cuboid has volume %d cm³. It is %d cm long and %d cm wide. How tall is it, in cm?" % (l * w * h, l, w), h, "int", {"unit": "cm"},
                   ["%d ÷ (%d × %d) = %d." % (l * w * h, l, w, h)])

    def t_cyl_height():
        r, h = random.randint(2, 8), random.randint(2, 15)
        return _tb("A cylinder has radius %d cm and volume %dπ cm³. How tall is it, in cm?" % (r, r * r * h), h, "int", {"unit": "cm"},
                   ["π × %d² × h = %dπ." % (r, r * r * h), "h = %d ÷ %d = %d." % (r * r * h, r * r, h)])

    def t_cubes_fit():
        s = pick([2, 3, 5])
        a, b, c = [s * random.randint(1, 5) for _ in range(3)]
        return _tb("How many cubes with %d cm edges fit exactly into a box %d cm × %d cm × %d cm?" % (s, a, b, c), (a // s) * (b // s) * (c // s),
                   "int", {}, ["%d × %d × %d = %d." % (a // s, b // s, c // s, (a // s) * (b // s) * (c // s))])

    def t_trapezium():
        p, q, h = random.randint(2, 10), random.randint(2, 10), random.randint(2, 8) * 2
        L = random.randint(3, 20)
        A = (p + q) * h // 2
        return _tb("A prism has a trapezium cross-section with parallel sides %d cm and %d cm, %d cm apart. The prism is %d cm long. Find its "
                   "volume, in cm³." % (p, q, h, L), A * L, "int", {"unit": "cm³"},
                   ["Cross-section ½(%d + %d) × %d = %d." % (p, q, h, A), "%d × %d = %d." % (A, L, A * L)])

    def t_cyl_litres():
        r, h = random.randint(5, 20), random.randint(10, 50)
        return _tb("A cylindrical tank has radius %d cm and height %d cm. How many litres does it hold, to 1 decimal place? (1 litre = 1000 cm³)"
                   % (r, h), _r1(math.pi * r * r * h / 1000), "num", {"unit": "litres"},
                   ["π × %d² × %d = %.2f cm³." % (r, h, math.pi * r * r * h), "÷ 1000."], tol=0.051)

    def t_l_prism():
        a, b = random.randint(5, 10), random.randint(4, 8)
        c, e = random.randint(2, a - 2), random.randint(2, b - 2)
        L = random.randint(3, 15)
        A = a * b - c * e
        return _tb("A prism's cross-section is an L-shape: %s %d cm × %d cm rectangle with %s %d cm × %d cm corner cut away. The prism is "
                   "%d cm long. Find its volume, in cm³." % (_a(a), a, b, _a(c), c, e, L), A * L, "int", {"unit": "cm³"},
                   ["Cross-section %d − %d = %d." % (a * b, c * e, A), "%d × %d = %d." % (A, L, A * L)])

    return _pick_t([t_prism, t_tri_prism, t_cylinder, t_cylinder_pi, t_height, t_litres, t_cuboid_missing, t_cyl_height, t_cubes_fit,
                    t_trapezium, t_cyl_litres, t_l_prism])


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
        cup, jug = pick([(125, 2), (250, 3), (200, 1), (250, 2), (500, 4), (125, 1)])
        return _tb("A cup holds %d cm³. How many cups of water fill a %d-litre jug?" % (cup, jug), jug * 1000 // cup, "int", {"unit": "cups"},
                   ["1 cm³ = 1 ml, so a cup holds %d ml." % cup, "%d ml ÷ %d = %d." % (jug * 1000, cup, jug * 1000 // cup)])

    def t_trap():
        return _wq("True or false: 1 m² = 100 cm².", "false", ["1 m² = 100 cm × 100 cm = 10,000 cm²."], "true / false")

    def t_mm2_cm2():
        k = random.randint(5, 999)
        return _tb("Convert %d mm² to cm²." % k, _ds(Fraction(k, 100)), "num", {"unit": "cm²"}, ["1 cm² = 100 mm², so ÷ 100."])

    def t_m3_litres():
        k = pick([Fraction(1, 2), 1, 2, 3, Fraction(3, 2), Fraction(1, 4), 5])
        return _tb("A tank holds %s m³ of water. How many litres is that?" % _ds(Fraction(k)), int(k * 1000), "int", {"unit": "litres"},
                   ["1 m³ = 1,000,000 cm³ = 1000 litres."])

    def t_litres_cm3():
        k = pick([Fraction(1, 2), Fraction(5, 2), Fraction(3, 4), 2, 4, Fraction(6, 5)])
        return _tb("How many cm³ are in %s litres?" % _ds(Fraction(k)), int(k * 1000), "int", {"unit": "cm³"}, ["1 litre = 1000 cm³."])

    def t_hectares():
        a, b = random.randint(1, 8) * 50, random.randint(2, 8) * 100
        return _tb("A field is %d m by %d m. 1 hectare = 10,000 m². What is its area in hectares?" % (a, b), _ds(Fraction(a * b, 10000)), "num",
                   {"unit": "hectares"}, ["%d × %d = %s m²." % (a, b, _c(a * b)), "÷ 10,000 = %s." % _ds(Fraction(a * b, 10000))])

    def t_km2():
        k = random.randint(2, 9)
        return _tb("How many m² are in %d km²?" % k, k * 1_000_000, "int", {"unit": "m²"}, ["1 km² = 1000 × 1000 = 1,000,000 m²."])

    def t_mm3():
        k = random.randint(1, 50) * 100
        return _tb("Convert %s mm³ to cm³." % _c(k), _ds(Fraction(k, 1000)), "num", {"unit": "cm³"}, ["1 cm³ = 10 × 10 × 10 = 1000 mm³."])

    def t_room():
        a, b = random.randint(20, 60) * 10, random.randint(20, 50) * 10
        return _tb("A room is %d cm by %d cm. What is its floor area in m²?" % (a, b), _ds(Fraction(a * b, 10000)), "num", {"unit": "m²"},
                   ["%s m × %s m = %s m²." % (_ds(Fraction(a, 100)), _ds(Fraction(b, 100)), _ds(Fraction(a * b, 10000)))])

    return _pick_t([t_m2_cm2, t_cm2_mm2, t_cm2_m2, t_cm3_m3, t_ml, t_trap, t_mm2_cm2, t_m3_litres, t_litres_cm3, t_hectares, t_km2, t_mm3,
                    t_room])
