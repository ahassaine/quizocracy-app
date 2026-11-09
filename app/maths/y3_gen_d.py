# Year 3 additions from the 2 Nov 2026 audit: statutory items the original bank did not reach.
#
# Tenths from dividing by 10; days in each month, leap years and seconds in a minute;
# horizontal and vertical lines.  They join the existing 3.6 and 3.8 strands.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S6 = "3.6 Fractions"
S8 = "3.8 Time & geometry"

def _tenths_q(prompt, n, solution):
    """A fraction answer kept in tenths (4/10, not 2/5); 2/5 is still marked right by value."""
    return _tb(prompt, "%d/10" % n, "frac", {"text": True, "placeholder": "e.g. 3/10"}, solution)


MONTHS = [("January", 31), ("February", 28), ("March", 31), ("April", 30), ("May", 31), ("June", 30),
          ("July", 31), ("August", 31), ("September", 30), ("October", 31), ("November", 30), ("December", 31)]


@skill("Y3.6.k", "Tenths: dividing by 10", S6)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 1, 1, 2), _by(d, 5, 9, 9))

    def t_divide():
        return _tenths_q("Work out %d ÷ 10. Write the answer as a fraction." % n, n,
                         ["Dividing by 10 makes tenths: %d ÷ 10 = %d/10." % (n, n)])

    def t_object():
        return _tb("A ribbon is cut into 10 equal pieces. How many pieces make %d/10 of it?" % n, n, "int", {},
                   ["Each piece is 1/10, so %d/10 is %s." % (n, "1 piece" if n == 1 else "%d pieces" % n)])

    def t_share():
        return _tenths_q("%s shared equally between 10 people. What fraction of a pizza does each person get?"
                         % ("1 pizza is" if n == 1 else "%d pizzas are" % n),
                         n, ["%d ÷ 10 = %d/10." % (n, n)])

    def t_how_many_tenths():
        w = random.randint(1, _by(d, 1, 3, 5))
        if d == 2:                                      # stretch: wholes and some tenths
            return _tb("How many tenths are there in %d whole%s and %d/10?" % (w, "" if w == 1 else "s", n), 10 * w + n, "int", {},
                       ["1 whole = 10 tenths, so %d whole%s = %d tenths." % (w, "" if w == 1 else "s", 10 * w),
                        "%d + %d = %d tenths." % (10 * w, n, 10 * w + n)])
        return _tb("How many tenths are there in %d whole%s?" % (w, "" if w == 1 else "s"), 10 * w, "int", {},
                   ["1 whole = 10 tenths, so %d × 10 = %d." % (w, 10 * w)])

    def t_missing():                                    # stretch: the number being divided is missing
        return _tb("___ ÷ 10 = %d/10" % n, n, "int", {}, ["Dividing by 10 makes tenths, so %d ÷ 10 = %d/10." % (n, n)])

    def t_compare():                                    # stretch: which share is bigger
        a, b = random.sample(range(1, 10), 2)
        return _tenths_q("Which is bigger: %d ÷ 10 or %d ÷ 10? Write the bigger answer as a fraction." % (a, b), max(a, b),
                         ["%d ÷ 10 = %d/10 and %d ÷ 10 = %d/10." % (a, a, b, b), "%d/10 is bigger." % max(a, b)])

    def t_bar():
        return {"prompt": "Shade the bar to show %d ÷ 10. The bar is one whole split into tenths." % n,
                "component": "fraction_bar", "spec": {"parts": 10, "mode": "shade"},
                "answer": "%d/10" % n, "answer_type": "frac", "solution": ["%d ÷ 10 = %d/10." % (n, n)]}

    def t_line():
        return _nld("Work out %d ÷ 10 and mark it on the number line." % n, Fraction(n, 10), 0, 1, Decimal("0.1"),
                    Decimal("0.1"), ["%d ÷ 10 = %d/10." % (n, n)])

    return _pick_t(_by(d, [t_divide, t_object, t_share], [t_divide, t_object, t_share, t_how_many_tenths],
                       [t_divide, t_share, t_how_many_tenths, t_missing, t_compare]), [t_bar, t_line])


@skill("Y3.8.m", "Days in each month, leap years and seconds in a minute", S8)
def _(d=1):
    d = _d(d)

    def t_month():
        if d == 2:                                      # stretch: find the month first
            i = random.choice([k for k in range(12) if "February" not in (MONTHS[k][0], MONTHS[(k + 1) % 12][0])])
            m, days = MONTHS[(i + 1) % 12]
            return _tb("How many days are there in the month that comes straight after %s?" % MONTHS[i][0], days, "int",
                       {"unit": "days"}, ["The month after %s is %s." % (MONTHS[i][0], m),
                                          "30 days has September, April, June and November; all the rest have 31, except February."])
        m, days = pick([x for x in MONTHS if x[0] != "February"])
        return _tb("How many days are there in %s?" % m, days, "int", {"unit": "days"},
                   ["30 days has September, April, June and November; all the rest have 31, except February."])

    def t_feb():
        if d == 0:
            leap = random.random() < 0.5
            return _tb("How many days are there in February in %s?" % ("a leap year" if leap else "a year that is not a leap year"),
                       29 if leap else 28, "int", {"unit": "days"},
                       ["February has 28 days, or 29 in a leap year."])
        if d == 2:                                      # stretch: leap years come every 4 years
            y = pick([2029, 2030, 2031, 2032, 2036])
            return _tb("2024 was a leap year, and leap years come every 4 years. How many days are there in February %d?" % y,
                       29 if y % 4 == 0 else 28, "int", {"unit": "days"},
                       ["The leap years are 2024, 2028, 2032, 2036, ...",
                        "%d %s a leap year, so February has %d days." % (y, "is" if y % 4 == 0 else "is not",
                                                                       29 if y % 4 == 0 else 28)])
        y = pick([2024, 2025, 2026, 2027, 2028])
        return _tb("How many days are there in February %d?" % y, 29 if y % 4 == 0 else 28, "int", {"unit": "days"},
                   ["%d %s a leap year." % (y, "is" if y % 4 == 0 else "is not"),
                    "February has %d days." % (29 if y % 4 == 0 else 28)])

    def t_year():
        leap = random.random() < 0.5
        if d == 2:                                      # stretch: two years, one of them a leap year
            return _tb("How many days are there in 2 years when one of them is a leap year?", 731, "int", {"unit": "days"},
                       ["365 + 366 = 731."])
        return _tb("How many days are there in a %s?" % ("leap year" if leap else "year that is not a leap year"),
                   366 if leap else 365, "int", {"unit": "days"},
                   ["A normal year has 365 days; a leap year has one more."])

    def t_seconds():
        k = random.randint(1, 5) if d else 1
        if d == 2:                                      # stretch: a half minute as well
            k = random.randint(1, 4)
            return _tb("How many seconds are there in %d and a half minutes?" % k, 60 * k + 30, "int",
                       {"unit": "seconds"}, ["%d × 60 = %d, and half a minute is 30 seconds." % (k, 60 * k),
                                             "%d + 30 = %d." % (60 * k, 60 * k + 30)])
        return _tb("How many seconds are there in %d minute%s?" % (k, "" if k == 1 else "s"), 60 * k, "int",
                   {"unit": "seconds"}, ["1 minute = 60 seconds, so %d × 60 = %d." % (k, 60 * k)])

    def t_thirty():
        if d == 2:
            return _tb("How many months of the year have exactly 31 days?", 7, "int", {"unit": "months"},
                       ["January, March, May, July, August, October and December."])
        return _tb("How many months of the year have exactly 30 days?", 4, "int", {"unit": "months"},
                   ["April, June, September and November."])

    def t_two_months():
        ms = random.sample([x for x in MONTHS if x[0] != "February"], 3 if d == 2 else 2)
        names = ", ".join(m[0] for m in ms[:-1]) + " and " + ms[-1][0]
        tot = sum(m[1] for m in ms)
        return _tb("How many days are there in %s altogether?" % names, tot, "int",
                   {"unit": "days"}, ["%s = %d." % (" + ".join(str(m[1]) for m in ms), tot)])

    def t_weeks():
        k = random.randint(2, _by(d, 3, 5, 5))
        if d == 2:                                      # stretch: weeks and days
            j = random.randint(1, 6)
            return _tb("How many days are there in %d weeks and %d day%s?" % (k, j, "" if j == 1 else "s"), 7 * k + j, "int",
                       {"unit": "days"}, ["%d × 7 = %d." % (k, 7 * k), "%d + %d = %d." % (7 * k, j, 7 * k + j)])
        return _tb("How many days are there in %d weeks?" % k, 7 * k, "int", {"unit": "days"},
                   ["1 week = 7 days, so %d × 7 = %d." % (k, 7 * k)])

    return _pick_t([t_month, t_feb, t_year, t_seconds, t_thirty, t_two_months, t_weeks])


@skill("Y3.8.n", "Horizontal and vertical lines", S8)
def _(d=1):
    d = _d(d)

    def t_name():
        what, ans = pick(_by(d, [("A flagpole standing straight up", "vertical"), ("A shelf on a wall", "horizontal"),
                                 ("A lamp post", "vertical"), ("The edge of a table top, running from side to side", "horizontal")],
                             [("The edge of a table top, running from side to side", "horizontal"),
                              ("A flagpole standing straight up", "vertical"),
                              ("The line where the sea meets the sky", "horizontal"),
                              ("A lamp post", "vertical"),
                              ("A shelf on a wall", "horizontal"),
                              ("The side of a door frame", "vertical")],
                             [("The surface of still water in a bath", "horizontal"),
                              ("A string hanging straight down with a weight on the end", "vertical"),
                              ("The line where the sea meets the sky", "horizontal"),
                              ("The side of a door frame", "vertical"),
                              ("The top step of a staircase", "horizontal"),
                              ("The corner where two walls of a room meet", "vertical")]))
        return _wq("%s: is it horizontal or vertical?" % what, ans,
                   ["Horizontal goes side to side; vertical goes straight up and down."], "horizontal / vertical")

    def t_letters():
        letter, h, v = pick(_by(d, [("T", 1, 1), ("L", 1, 1)], [("T", 1, 1), ("H", 1, 2), ("E", 3, 1), ("L", 1, 1), ("F", 2, 1)],
                                [("H", 1, 2), ("E", 3, 1), ("F", 2, 1)]))
        kind = pick(["horizontal", "vertical"])
        return _tb("Look at the capital letter %s. How many %s lines does it have?" % (letter, kind),
                   h if kind == "horizontal" else v, "int", {},
                   ["%s has %d horizontal and %d vertical line%s." % (letter, h, v, "" if v == 1 else "s")])

    def t_shape():
        name, h, v = pick([("square", 2, 2), ("rectangle", 2, 2)])
        return _tb("A %s is drawn on the board with its bottom side horizontal. How many of its sides are vertical?" % name, v, "int", {},
                   ["Two sides go up and down."])

    def t_plot():
        x, y = (random.randint(1, 6), random.randint(1, 6)) if d < 2 else (random.randint(1, 9), random.randint(1, 9))
        k = random.randint(_by(d, 1, 2, 3), _by(d, 3, 4, 5))
        horiz = random.random() < 0.5
        c = x if horiz else y
        back = d == 2 and (c + k > 10 or (c - k >= 1 and random.random() < 0.5))     # stretch: going left or down
        step = -k if back else k
        ans = (x + step, y) if horiz else (x, y + step)
        return {"prompt": "Plot a point so that the line from A to your point is %s and %s long, going %s."
                          % ("horizontal" if horiz else "vertical", "1 square" if k == 1 else "%d squares" % k,
                             ("left" if back else "right") if horiz else ("down" if back else "up")),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 10, "points": [[x, y, "A"]]},
                "answer": "(%d,%d)" % ans, "answer_type": "coord",
                "solution": ["A %s line keeps the same %s." % ("horizontal" if horiz else "vertical",
                                                               "height" if horiz else "across position")]}

    def t_shape_horizontal():                           # stretch: count the horizontal sides as well
        name, h, v = pick([("rectangle", 2, 2), ("right-angled triangle", 1, 1)])
        kind = pick(["horizontal", "vertical"])
        return _tb("A %s is drawn with its bottom side horizontal%s. How many of its sides are %s?"
                   % (name, " and its right angle at the bottom left" if "triangle" in name else "", kind),
                   h if kind == "horizontal" else v, "int", {},
                   ["%s has %d horizontal and %d vertical side%s; %s." % ("A " + name, h, v, "" if v == 1 else "s",
                                                                       "the third side slopes" if "triangle" in name else "no side slopes")])

    def t_perp():
        return _wq("A horizontal line and a vertical line meet. Is the angle they make acute, right or obtuse?", "right",
                   ["Horizontal and vertical lines are perpendicular: they meet at a right angle."], "acute / right / obtuse")

    return _pick_t(_by(d, [t_name, t_letters, t_shape], [t_name, t_letters, t_shape, t_perp],
                       [t_name, t_letters, t_shape_horizontal]), [t_plot])
