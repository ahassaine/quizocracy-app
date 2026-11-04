# Year 6 additions from the 2 Nov 2026 audit: statutory items the original bank did not reach.
#
# Shapes with the same area can have different perimeters (and vice versa); volume in cm³ and m³,
# extending to mm³ and km³.  They join the existing 6.8 Geometry strand.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S8 = "6.8 Geometry"


def _pairs(n):
    return [(a, n // a) for a in range(1, int(n ** 0.5) + 1) if n % a == 0]


@skill("Y6.8.r", "Same area, different perimeter", S8)
def _(d=1):
    d = _d(d)
    area = pick(_by(d, [12, 16, 18, 20], [24, 30, 36, 40], [36, 48, 60, 64, 72]))
    rects = _pairs(area)

    def t_largest_perimeter():
        a, b = rects[0]
        return _tb("Rectangles with whole-number sides all have an area of %d cm². What is the LARGEST perimeter one "
                   "of them can have, in cm?" % area, 2 * (a + b), "int", {"unit": "cm"},
                   ["The longest, thinnest one is %d cm by %d cm." % (a, b), "2 × (%d + %d) = %d." % (a, b, 2 * (a + b))])

    def t_smallest_perimeter():
        a, b = rects[-1]
        return _tb("Rectangles with whole-number sides all have an area of %d cm². What is the SMALLEST perimeter one "
                   "of them can have, in cm?" % area, 2 * (a + b), "int", {"unit": "cm"},
                   ["The most square-like one is %d cm by %d cm." % (a, b), "2 × (%d + %d) = %d." % (a, b, 2 * (a + b))])

    def t_compare():
        (a, b), (c, e) = random.sample(rects, 2)
        return _tb("Rectangle P is %d cm by %d cm and rectangle Q is %d cm by %d cm. They have the same area. What is "
                   "the difference between their perimeters, in cm?" % (a, b, c, e), abs(2 * (a + b) - 2 * (c + e)),
                   "int", {"unit": "cm"}, ["P: %d cm. Q: %d cm." % (2 * (a + b), 2 * (c + e))])

    def t_count():
        return _tb("How many different rectangles with whole-number sides have an area of %d cm²? (A 2 × 3 and a "
                   "3 × 2 count as the same.)" % area, len(rects), "int", {},
                   ["%s." % ", ".join("%d × %d" % r for r in rects)])

    def t_same_perimeter():
        p = 2 * random.randint(8, 14)
        half = p // 2
        sides = [(a, half - a) for a in range(1, half // 2 + 1)]
        (a, b), (c, e) = random.sample(sides, 2)
        return _tb("Two rectangles both have a perimeter of %d cm. One is %d cm by %d cm; the other is %d cm by %d cm. "
                   "How much larger is the bigger area, in cm²?" % (p, a, b, c, e), abs(a * b - c * e), "int",
                   {"unit": "cm²"}, ["Areas: %d cm² and %d cm²." % (a * b, c * e)])

    def t_true():
        return _wq("True or false: two rectangles with the same area always have the same perimeter.", "false",
                   ["A %d × %d and %s %d × %d rectangle have the same area but different perimeters."
                    % (rects[0] + ("an" if str(rects[-1][0])[0] == "8" or rects[-1][0] in (11, 18) else "a",) + rects[-1])],
                   "true / false")

    def t_grid():
        a, b = rects[-1] if rects[-1][1] <= 10 else rects[len(rects) // 2]
        if b > 10 or a > 10:
            return t_compare()
        return _area("Each square is 1 cm. This rectangle has an area of %d cm². What is its perimeter, in cm?" % (a * b),
                     {"mode": "read_perimeter", "rows": a, "cols": b}, 2 * (a + b),
                     ["2 × (%d + %d) = %d." % (a, b, 2 * (a + b))])

    def t_find_sides():
        a, b = random.choice([r for r in rects if r[0] != r[1]] or rects)
        return _tb("A rectangle with whole-number sides has an area of %d cm² and a perimeter of %d cm. How long is its "
                   "longer side, in cm?" % (area, 2 * (a + b)), max(a, b), "int", {"unit": "cm"},
                   ["Look for two numbers that multiply to %d and add to %d." % (area, a + b),
                    "%d × %d = %d and %d + %d = %d, so the longer side is %d cm." % (a, b, area, a, b, a + b, max(a, b))])

    def t_largest_area():
        p = 2 * random.randint(_by(d, 6, 9, 12), _by(d, 10, 16, 25))
        half = p // 2
        a = half // 2
        return _tb("Rectangles with whole-number sides all have a perimeter of %d cm. What is the LARGEST area one of them "
                   "can have, in cm²?" % p, a * (half - a), "int", {"unit": "cm²"},
                   ["The sides add to %d cm." % half,
                    "The area is largest when the sides are as close as possible: %d × %d = %d cm²." % (a, half - a, a * (half - a))])

    def t_L_shape():
        R, C = random.randint(3, 6), random.randint(4, 7)
        r, c = random.randint(1, R - 2), random.randint(1, C - 2)
        cells = [[i, j] for i in range(R) for j in range(C) if not (i < r and j >= C - c)]
        return _area("Each square is 1 cm. This L-shape has an area of %d cm². What is its perimeter, in cm?" % len(cells),
                     {"mode": "read_perimeter", "cells": cells}, 2 * (R + C),
                     ["Cutting out a corner does not change the distance round: it is the same as a %d × %d rectangle." % (R, C),
                      "2 × (%d + %d) = %d cm." % (R, C, 2 * (R + C))])

    def t_which_longer():
        (a, b), (c, e) = random.sample(rects, 2)
        pa, pc = 2 * (a + b), 2 * (c + e)
        return _wq("Rectangle A is %d cm by %d cm. Rectangle B is %d cm by %d cm. Both have an area of %d cm². Which has "
                   "the longer perimeter? Type A or B." % (a, b, c, e, area), "A" if pa > pc else "B",
                   ["A: 2 × (%d + %d) = %d cm. B: 2 × (%d + %d) = %d cm." % (a, b, pa, c, e, pc),
                    "The thinner rectangle has the longer perimeter."], "A or B")

    def t_other_length():
        (a, b), (c, e) = random.sample(rects, 2)
        return _tb("A rectangle is %d cm by %d cm. Another rectangle has the same area and is %d cm wide. How long is it, "
                   "in cm?" % (a, b, c), e, "int", {"unit": "cm"},
                   ["The area is %d × %d = %d cm²." % (a, b, area), "%d ÷ %d = %d cm." % (area, c, e)])

    def t_table():
        rs = rects[:4] if len(rects) >= 3 else rects
        k = random.randrange(len(rs))
        rows = [[a, b, "" if i == k else 2 * (a + b)] for i, (a, b) in enumerate(rs)]
        return _dt("Every rectangle in the table has an area of %d cm². What is the missing perimeter, in cm?" % area,
                   ["Length (cm)", "Width (cm)", "Perimeter (cm)"], rows, 2 * sum(rs[k]),
                   ["2 × (%d + %d) = %d cm." % (rs[k][0], rs[k][1], 2 * sum(rs[k])),
                    "Same area, but the perimeters are all different."], missing=[k, 2])

    return _pick_t([t_largest_perimeter, t_smallest_perimeter, t_compare, t_count, t_same_perimeter, t_true, t_find_sides,
                    t_largest_area, t_which_longer, t_other_length], [t_grid, t_L_shape, t_table])


@skill("Y6.8.s", "Volume in cm³ and m³ (and mm³, km³)", S8)
def _(d=1):
    d = _d(d)

    def t_m3_to_cm3():
        k = random.randint(1, 5)
        return _tb("How many cm³ are in %d m³? (1 m = 100 cm)" % k, k * 1_000_000, "int", {"unit": "cm³"},
                   ["1 m³ = 100 × 100 × 100 = 1,000,000 cm³.", "%d × 1,000,000 = %s." % (k, _c(k * 1_000_000))])

    def t_cm3_to_mm3():
        k = random.randint(1, 9)
        return _tb("How many mm³ are in %d cm³? (1 cm = 10 mm)" % k, k * 1000, "int", {"unit": "mm³"},
                   ["1 cm³ = 10 × 10 × 10 = 1,000 mm³.", "%d × 1,000 = %s." % (k, _c(k * 1000))])

    def t_room():
        l, w, h = random.randint(3, 8), random.randint(2, 6), random.randint(2, 3)
        return _tb("A room is %d m long, %d m wide and %d m high. What is its volume, in m³?" % (l, w, h), l * w * h,
                   "int", {"unit": "m³"}, ["%d × %d × %d = %d." % (l, w, h, l * w * h)])

    def t_unit():
        what, ans = pick([("a matchbox", "cm³"), ("a swimming pool", "m³"), ("a grain of rice", "mm³"),
                          ("a lake", "km³"), ("a shoebox", "cm³"), ("a shipping container", "m³")])
        letter = "ABCD"[["mm³", "cm³", "m³", "km³"].index(ans)]
        return _wq("Which unit is most sensible for the volume of %s?  A: mm³   B: cm³   C: m³   D: km³   "
                   "Type the letter." % what, letter,
                   ["%s: choose the unit that gives a sensible-sized number." % ans], "A, B, C or D")

    def t_compare():
        a = random.randint(2, 9) * 100_000
        k = random.randint(1, 3)
        return _wq("Which is larger?  A: %d m³   B: %s cm³   Type A or B." % (k, _c(a)),
                   "A" if k * 1_000_000 > a else "B", ["%d m³ = %s cm³." % (k, _c(k * 1_000_000))], "A or B")

    def t_cubes_fit():
        e = pick([2, 5, 10])
        L, W, H = e * random.randint(2, 6), e * random.randint(2, 5), e * random.randint(1, 4)
        return _tb("How many %d cm cubes fit exactly into a box %d cm × %d cm × %d cm?" % (e, L, W, H),
                   (L // e) * (W // e) * (H // e), "int", {"unit": "cubes"},
                   ["%d × %d × %d = %d." % (L // e, W // e, H // e, (L // e) * (W // e) * (H // e))])

    def t_cuboid():
        l, w, h = random.randint(2, _by(d, 6, 10, 15)), random.randint(2, _by(d, 5, 8, 12)), random.randint(2, _by(d, 5, 8, 10))
        return _tb("A cuboid is %d cm long, %d cm wide and %d cm high. What is its volume, in cm³?" % (l, w, h), l * w * h,
                   "int", {"unit": "cm³"}, ["Volume = length × width × height.", "%d × %d × %d = %d cm³." % (l, w, h, l * w * h)])

    def t_missing_edge():
        l, w, h = random.randint(2, 10), random.randint(2, 8), random.randint(2, 9)
        return _tb("A cuboid has a volume of %d cm³. It is %d cm long and %d cm wide. How high is it, in cm?" % (l * w * h, l, w),
                   h, "int", {"unit": "cm"}, ["%d × %d = %d cm² for the base." % (l, w, l * w),
                                             "%d ÷ %d = %d cm." % (l * w * h, l * w, h)])

    def t_cube():
        k = random.randint(2, _by(d, 5, 10, 12))
        if random.random() < 0.5:
            return _tb("A cube has edges of %d cm. What is its volume, in cm³?" % k, k ** 3, "int", {"unit": "cm³"},
                       ["%d × %d × %d = %d cm³." % (k, k, k, k ** 3)])
        return _tb("A cube has a volume of %d cm³. How long is each edge, in cm?" % k ** 3, k, "int", {"unit": "cm"},
                   ["Find the number that multiplied by itself three times gives %d." % k ** 3, "%d × %d × %d = %d." % (k, k, k, k ** 3)])

    def t_litres():
        while True:
            l, w, h = pick([10, 20, 25, 40, 50]), pick([10, 20, 40, 50]), pick([10, 20, 30, 50])
            if (l * w * h) % 1000 == 0:
                break
        v = l * w * h
        return _tb("A fish tank is %d cm long, %d cm wide and %d cm high. 1 litre = 1,000 cm³. How many litres does it hold "
                   "when full?" % (l, w, h), v // 1000, "int", {"unit": "litres"},
                   ["%d × %d × %d = %s cm³." % (l, w, h, _c(v)), "%s ÷ 1,000 = %s." % (_c(v), _pl(v // 1000, "litre"))])

    def t_cm3_to_m3():
        k = random.randint(2, 9)
        return _tb("How many m³ is %s cm³?" % _c(k * 1_000_000), k, "int", {"unit": "m³"},
                   ["1 m³ = 1,000,000 cm³.", "%s ÷ 1,000,000 = %d." % (_c(k * 1_000_000), k)])

    def t_estimate():
        a, b, c = random.randint(3, 9), random.randint(2, 8), random.randint(2, 6)
        da, db = pick(["0.1", "0.2", "-0.1", "-0.2"]), pick(["0.1", "-0.1", "0.2"])
        sa, sb = Decimal(a) + Decimal(da), Decimal(b) + Decimal(db)
        return _tb("Estimate the volume of a box %s cm × %s cm × %d cm by rounding each length to the nearest whole number."
                   % (_ds(sa), _ds(sb), c), a * b * c, "int", {"unit": "cm³"},
                   ["%s rounds to %d and %s rounds to %d." % (_ds(sa), a, _ds(sb), b), "%d × %d × %d = %d cm³." % (a, b, c, a * b * c)])

    def t_cubes_pic():
        l, w, h = random.randint(2, 4), random.randint(2, 4), random.randint(1, 3)
        return _tb("A cuboid is built from 1 cm cubes. It is %d cubes long, %d cubes wide and %d %s high. What is its volume, "
                   "in cm³?" % (l, w, h, "cube" if h == 1 else "cubes"), l * w * h, "int", {"unit": "cm³"},
                   ["Each layer has %d × %d = %d cubes." % (l, w, l * w), "%d × %d = %d cm³." % (l * w, h, l * w * h)])

    return _pick_t([t_m3_to_cm3, t_cm3_to_mm3, t_room, t_unit, t_compare, t_cubes_fit, t_cuboid, t_missing_edge, t_cube,
                    t_litres, t_cm3_to_m3, t_estimate, t_cubes_pic])
