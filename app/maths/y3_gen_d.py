# Year 3 additions from the 2 Nov 2026 audit: statutory items the original bank did not reach.
#
# Tenths from dividing by 10; days in each month, leap years and seconds in a minute;
# horizontal and vertical lines.  They join the existing 3.6 and 3.8 strands.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S6 = "3.6 Fractions"
S8 = "3.8 Time & geometry"

MONTHS = [("January", 31), ("February", 28), ("March", 31), ("April", 30), ("May", 31), ("June", 30),
          ("July", 31), ("August", 31), ("September", 30), ("October", 31), ("November", 30), ("December", 31)]


@skill("Y3.6.k", "Tenths: dividing by 10", S6)
def _(d=1):
    d = _d(d)
    n = random.randint(1, 9)

    def t_divide():
        return _fq("Work out %d ÷ 10. Write the answer as a fraction." % n, Fraction(n, 10),
                   ["Dividing by 10 makes tenths: %d ÷ 10 = %d/10." % (n, n)], "e.g. 3/10")

    def t_object():
        return _tb("A ribbon is cut into 10 equal pieces. How many pieces make %d/10 of it?" % n, n, "int", {},
                   ["Each piece is 1/10, so %d/10 is %d pieces." % (n, n)])

    def t_share():
        return _fq("%d pizzas are shared equally between 10 people. What fraction of a pizza does each person get?" % n,
                   Fraction(n, 10), ["%d ÷ 10 = %d/10." % (n, n)], "e.g. 3/10")

    def t_how_many_tenths():
        w = random.randint(1, 3)
        return _tb("How many tenths are there in %d whole%s?" % (w, "" if w == 1 else "s"), 10 * w, "int", {},
                   ["1 whole = 10 tenths, so %d × 10 = %d." % (w, 10 * w)])

    def t_bar():
        return {"prompt": "Shade the bar to show %d ÷ 10. The bar is one whole split into tenths." % n,
                "component": "fraction_bar", "spec": {"parts": 10, "mode": "shade"},
                "answer": "%d/10" % n, "answer_type": "frac", "solution": ["%d ÷ 10 = %d/10." % (n, n)]}

    def t_line():
        return _nld("Work out %d ÷ 10 and mark it on the number line." % n, Fraction(n, 10), 0, 1, Decimal("0.1"),
                    Decimal("0.1"), ["%d ÷ 10 = %d/10." % (n, n)])

    return _pick_t([t_divide, t_object, t_share, t_how_many_tenths], [t_bar, t_line])


@skill("Y3.8.m", "Days in each month, leap years and seconds in a minute", S8)
def _(d=1):
    d = _d(d)

    def t_month():
        m, days = pick([x for x in MONTHS if x[0] != "February"])
        return _tb("How many days are there in %s?" % m, days, "int", {"unit": "days"},
                   ["30 days has September, April, June and November; all the rest have 31, except February."])

    def t_feb():
        y = pick([2024, 2025, 2026, 2027, 2028])
        return _tb("How many days are there in February %d?" % y, 29 if y % 4 == 0 else 28, "int", {"unit": "days"},
                   ["%d %s a leap year." % (y, "is" if y % 4 == 0 else "is not"),
                    "February has %d days." % (29 if y % 4 == 0 else 28)])

    def t_year():
        leap = random.random() < 0.5
        return _tb("How many days are there in a %s?" % ("leap year" if leap else "year that is not a leap year"),
                   366 if leap else 365, "int", {"unit": "days"},
                   ["A normal year has 365 days; a leap year has one more."])

    def t_seconds():
        k = random.randint(1, 5) if d else 1
        return _tb("How many seconds are there in %d minute%s?" % (k, "" if k == 1 else "s"), 60 * k, "int",
                   {"unit": "seconds"}, ["1 minute = 60 seconds, so %d × 60 = %d." % (k, 60 * k)])

    def t_thirty():
        return _tb("How many months of the year have exactly 30 days?", 4, "int", {"unit": "months"},
                   ["April, June, September and November."])

    def t_two_months():
        a, b = random.sample([x for x in MONTHS if x[0] != "February"], 2)
        return _tb("How many days are there in %s and %s altogether?" % (a[0], b[0]), a[1] + b[1], "int",
                   {"unit": "days"}, ["%d + %d = %d." % (a[1], b[1], a[1] + b[1])])

    def t_weeks():
        k = random.randint(2, 5)
        return _tb("How many days are there in %d weeks?" % k, 7 * k, "int", {"unit": "days"},
                   ["1 week = 7 days, so %d × 7 = %d." % (k, 7 * k)])

    return _pick_t([t_month, t_feb, t_year, t_seconds, t_thirty, t_two_months, t_weeks])


@skill("Y3.8.n", "Horizontal and vertical lines", S8)
def _(d=1):
    d = _d(d)

    def t_name():
        what, ans = pick([("The edge of a table top, running from side to side", "horizontal"),
                          ("A flagpole standing straight up", "vertical"),
                          ("The line where the sea meets the sky", "horizontal"),
                          ("A lamp post", "vertical"),
                          ("A shelf on a wall", "horizontal"),
                          ("The side of a door frame", "vertical")])
        return _wq("%s: is it horizontal or vertical?" % what, ans,
                   ["Horizontal goes side to side; vertical goes straight up and down."], "horizontal / vertical")

    def t_letters():
        letter, h, v = pick([("T", 1, 1), ("H", 1, 2), ("E", 3, 1), ("L", 1, 1), ("F", 2, 1), ("I", 0, 1)])
        kind = pick(["horizontal", "vertical"])
        return _tb("Look at the capital letter %s. How many %s lines does it have?" % (letter, kind),
                   h if kind == "horizontal" else v, "int", {},
                   ["%s has %d horizontal and %d vertical line%s." % (letter, h, v, "" if v == 1 else "s")])

    def t_shape():
        name, h, v = pick([("square", 2, 2), ("rectangle", 2, 2)])
        return _tb("A %s sits flat on the floor. How many of its sides are vertical?" % name, v, "int", {},
                   ["Two sides go up and down."])

    def t_plot():
        x, y = random.randint(1, 6), random.randint(1, 6)
        k = random.randint(2, 4)
        horiz = random.random() < 0.5
        ans = (x + k, y) if horiz else (x, y + k)
        return {"prompt": "Plot a point so that the line from A to your point is %s and %d squares long, going %s."
                          % ("horizontal" if horiz else "vertical", k, "right" if horiz else "up"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 10, "points": [[x, y, "A"]]},
                "answer": "(%d,%d)" % ans, "answer_type": "coord",
                "solution": ["A %s line keeps the same %s." % ("horizontal" if horiz else "vertical",
                                                               "height" if horiz else "across position")]}

    def t_perp():
        return _wq("A horizontal line and a vertical line meet. What kind of angle do they make? (one word)", "right",
                   ["Horizontal and vertical lines are perpendicular: they meet at a right angle."], "one word")

    return _pick_t([t_name, t_letters, t_shape, t_perp], [t_plot])
