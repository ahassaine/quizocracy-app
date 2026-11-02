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
                   ["A %d × %d and a %d × %d rectangle have the same area but different perimeters."
                    % (rects[0] + rects[-1])], "true / false")

    def t_grid():
        a, b = rects[-1] if rects[-1][1] <= 10 else rects[len(rects) // 2]
        if b > 10 or a > 10:
            return t_compare()
        return _area("Each square is 1 cm. This rectangle has an area of %d cm². What is its perimeter, in cm?" % (a * b),
                     {"mode": "read_perimeter", "rows": a, "cols": b}, 2 * (a + b),
                     ["2 × (%d + %d) = %d." % (a, b, 2 * (a + b))])

    return _pick_t([t_largest_perimeter, t_smallest_perimeter, t_compare, t_count, t_same_perimeter, t_true], [t_grid])


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

    return _pick_t([t_m3_to_cm3, t_cm3_to_mm3, t_room, t_unit, t_compare, t_cubes_fit])
