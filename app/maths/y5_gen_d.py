# Year 5 generators: strands 5.6 and 5.7.
#
# Decimals to three places (place value, fractions <-> decimals, rounding, ordering, adding and
# subtracting, problems), per cent as "parts per hundred" and the key equivalences.
# Measurement: metric conversions, imperial approximations, perimeter of composite rectilinear
# shapes, area of rectangles and irregular shapes, volume and capacity, time conversions, measure
# and money problems with decimals.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S6 = "5.6 Decimals & percentages"
S7 = "5.7 Measurement"

DPLACE = {1: "tenths", 2: "hundredths", 3: "thousandths"}


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _rand_dec(d, lo=0, hi=99):
    dp = _by(d, 2, 3, 3) if random.random() < 0.7 else random.randint(1, 3)
    whole = random.randint(lo, hi)
    frac = random.randint(1, 10 ** dp - 1)
    return Decimal(whole) + Decimal(frac) / (10 ** dp)


def _places_after(x):
    s = _ds(x)
    return len(s.split(".")[1]) if "." in s else 0


# ================================================================== 5.6 ======
@skill("Y5.6.a", "Place value in decimals to three places", S6)
def _(d=1):
    d = _d(d)
    x = _rand_dec(d, 0, _by(d, 9, 50, 99))
    while _places_after(x) < 2:
        x = _rand_dec(d, 0, 9)
    s = _ds(x)
    dec = s.split(".")[1]

    def t_value():
        k = random.randrange(len(dec))
        while dec[k] == "0":
            k = random.randrange(len(dec))
        v = Decimal(dec[k]) / (10 ** (k + 1))
        return _tb("What is the value of the digit %s in %s? Write it as a decimal." % (dec[k], s), _ds(v),
                   "num", {}, ["The %s is in the %s place, so it is worth %s." % (dec[k], DPLACE[k + 1], _ds(v))])

    def t_place():
        k = random.randrange(len(dec))
        if dec.count(dec[k]) > 1 or dec[k] in s.split(".")[0]:
            return t_value()
        return _wq("In %s, which place is the digit %s in? (tenths, hundredths or thousandths)"
                   % (s, dec[k]), DPLACE[k + 1], ["Count places after the decimal point."],
                   "tenths / hundredths / thousandths")

    def t_count():
        p = pick([10, 100, 1000][: len(dec)])
        name = {10: "tenths", 100: "hundredths", 1000: "thousandths"}[p]
        return _tb("How many %s are there altogether in %s?" % (name, s), int(x * p), "int", {},
                   ["%s × %d = %s, so %s whole %s." % (s, p, _ds(x * p), int(x * p), name)])

    def t_partition():
        parts = [Decimal(int(s.split(".")[0]))] + [Decimal(c) / (10 ** (i + 1)) for i, c in enumerate(dec)]
        parts = [p for p in parts if p]
        if len(parts) < 3:
            return t_value()
        k = random.randrange(len(parts))
        shown = " + ".join("___" if i == k else _ds(p) for i, p in enumerate(parts))
        return _tb("Complete:  %s = %s" % (s, shown), _ds(parts[k]), "num", {},
                   ["%s = %s." % (s, " + ".join(_ds(p) for p in parts))])

    def t_thousandths():
        t = random.randint(1, 999)
        return _tb("Write %d thousandths as a decimal." % t, _ds(Decimal(t) / 1000), "num", {},
                   ["%d ÷ 1000 = %s." % (t, _ds(Decimal(t) / 1000))])

    def t_relate():
        k = pick([("tenth", "hundredths", 10), ("hundredth", "thousandths", 10), ("tenth", "thousandths", 100)])
        return _tb("How many %s make one %s?" % (k[1], k[0]), k[2], "int", {},
                   ["1 %s = %d %s." % (k[0], k[2], k[1])])

    def t_line():
        w = random.randint(0, 9)
        lo = Decimal(w) + Decimal(random.randint(0, 8)) / 10
        x2 = lo + Decimal(random.randint(1, 9)) / 100
        return _nld("Place %s on the number line." % _ds(x2), x2, lo, lo + Decimal("0.1"), Decimal("0.01"),
                    Decimal("0.05"), ["%s is %d hundredths after %s." % (_ds(x2), int((x2 - lo) * 100),
                                                                        _ds(lo))])

    return _pick_t([t_value, t_place, t_count, t_partition, t_thousandths, t_relate], [t_line])


@skill("Y5.6.b", "Write decimals as fractions", S6)
def _(d=1):
    d = _d(d)
    dp = _by(d, 1, 2, 3)
    n = random.randint(1, 10 ** dp - 1)
    while n % 10 == 0:
        n = random.randint(1, 10 ** dp - 1)
    x = Decimal(n) / (10 ** dp)

    def t_over_power():
        return _tb("Complete:  %s = ___/%d" % (_ds(x), 10 ** dp), n, "int", {},
                   ["%s means %d %s." % (_ds(x), n, DPLACE[dp])])

    def t_fraction():
        return _fq("Write %s as a fraction." % _ds(x), Fraction(n, 10 ** dp),
                   ["%s = %d/%d." % (_ds(x), n, 10 ** dp)])

    def t_simplest():
        f = Fraction(n, 10 ** dp)
        if f.denominator == 10 ** dp:
            return t_over_power()
        return _wq("Write %s as a fraction in its simplest form." % _ds(x), _fs(f),
                   ["%s = %d/%d = %s." % (_ds(x), n, 10 ** dp, _fs(f))], "e.g. 3/4")

    def t_mixed():
        w = random.randint(1, 9)
        return _wq("Write %s as a mixed number with a denominator of %d (like 3 7/10)." % (_ds(w + x), 10 ** dp),
                   "%d %d/%d" % (w, n, 10 ** dp), ["%s = %d and %d/%d." % (_ds(w + x), w, n, 10 ** dp)],
                   "e.g. 3 7/10")

    def t_grid():
        if dp > 2:
            return t_fraction()
        hund = int(x * 100)
        return _area("This square is one whole split into 100 parts. Shade it to show %s." % _ds(x),
                     {"mode": "fraction", "parts": 100}, "%d/100" % hund,
                     ["%s = %d/100." % (_ds(x), hund)], atype="frac")

    return _pick_t([t_over_power, t_fraction, t_simplest, t_mixed], [t_grid])


@skill("Y5.6.c", "Write fractions as decimals", S6)
def _(d=1):
    d = _d(d)

    def t_power():
        dp = _by(d, 1, 2, 3)
        n = random.randint(1, 10 ** dp - 1)
        return _tb("Write %d/%d as a decimal." % (n, 10 ** dp), _ds(Decimal(n) / 10 ** dp), "num", {},
                   ["%d ÷ %d = %s." % (n, 10 ** dp, _ds(Decimal(n) / 10 ** dp))])

    def t_key():
        f = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                  Fraction(3, 5), Fraction(4, 5)])
        return _tb("Write %s as a decimal." % _fs(f), _ds(f), "num", {},
                   ["%s = %d/%d = %s." % (_fs(f), f.numerator * (100 // f.denominator), 100, _ds(f))])

    def t_scale():
        den = pick([2, 4, 5, 20, 25, 50])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        k = 100 // den
        return _tb("Write %d/%d as a decimal. (Hint: make the denominator 100.)" % (num, den), _ds(f), "num",
                   {}, ["%d/%d = %d/100 = %s." % (num, den, num * k, _ds(f))])

    def t_mixed():
        w = random.randint(1, 9)
        f = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(7, 10), Fraction(9, 100)])
        return _tb("Write %d %s as a decimal." % (w, _fs(f)), _ds(w + f), "num", {},
                   ["%s = %s, so %s." % (_fs(f), _ds(f), _ds(w + f))])

    def t_table():
        fs = random.sample([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                            Fraction(7, 10), Fraction(3, 100), Fraction(1, 20)], 4)
        k = random.randrange(4)
        rows = [[_fs(f), _ds(f)] for f in fs]
        return _dt("The table matches fractions to decimals. What decimal belongs in the empty cell?",
                   ["Fraction", "Decimal"], rows, _ds(fs[k]), ["%s = %s." % (_fs(fs[k]), _ds(fs[k]))],
                   missing=[k, 1], atype="num")

    def t_line():
        f = pick([Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(4, 5), Fraction(1, 2)])
        return _nld("Place %s on the number line marked in tenths." % _fs(f), f, 0, 1, Decimal("0.05"),
                    Decimal("0.1"), ["%s = %s." % (_fs(f), _ds(f))])

    return _pick_t([t_power, t_key, t_scale, t_mixed], [t_table, t_line])


@skill("Y5.6.d", "Round decimals to the nearest whole number and to one decimal place", S6)
def _(d=1):
    d = _d(d)
    x = Decimal(random.randint(0, _by(d, 9, 30, 99))) + Decimal(random.randint(1, 99)) / 100
    if d == 2 and random.random() < 0.4:
        x = Decimal(random.randint(0, 20)) + Decimal(pick([95, 96, 97, 98, 99, 45, 55, 5, 51])) / 100

    def _r1(v):
        return (v * 10 + Decimal("0.5")).to_integral_value(rounding="ROUND_FLOOR") / 10

    def _r0(v):
        return (v + Decimal("0.5")).to_integral_value(rounding="ROUND_FLOOR")

    def t_whole():
        return _tb("Round %s to the nearest whole number." % _ds(x), _ds(_r0(x)), "num", {},
                   ["Look at the tenths digit.", "%s → %s." % (_ds(x), _ds(_r0(x)))])

    def t_one_dp():
        return _tb("Round %s to one decimal place." % _ds(x), _ds(_r1(x)), "num", {},
                   ["Look at the hundredths digit.", "%s → %s." % (_ds(x), _ds(_r1(x)))])

    def t_context():
        what, unit = pick([("A parcel weighs", "kg"), ("A long jump is", "m"), ("A bottle holds", "litres")])
        return _tb("%s %s %s. Round this to the nearest whole %s." % (what, _ds(x), unit, unit.rstrip("s")),
                   _ds(_r0(x)), "num", {"unit": unit}, ["%s → %s." % (_ds(x), _ds(_r0(x)))])

    def t_which():
        target = random.randint(2, 9)
        good = Decimal(target) + Decimal(pick([-1, 1]) * random.randint(1, 49)) / 100
        bad = [Decimal(target) + Decimal(random.randint(51, 99)) / 100,
               Decimal(target) - Decimal(random.randint(51, 99)) / 100]
        opts = [good] + bad
        random.shuffle(opts)
        return _tb("Which of these rounds to %d (nearest whole number)?  %s"
                   % (target, ", ".join(_ds(o) for o in opts)), _ds(good), "num", {},
                   ["%s rounds to %d." % (_ds(good), target)])

    def t_money():
        p = Decimal(random.randint(101, 9999)) / 100
        return _tb("Round £%s to the nearest pound. Give the number of pounds." % format(p, ".2f"),
                   _ds(_r0(p)), "num", {"unit": "£"}, ["£%s → £%s." % (format(p, ".2f"), _ds(_r0(p)))])

    def t_line():
        lo = Decimal(int(x))
        return _nld("Round %s to one decimal place and mark it on the line." % _ds(x), _r1(x), lo, lo + 1,
                    Decimal("0.1"), Decimal("0.5"), ["%s → %s." % (_ds(x), _ds(_r1(x)))]) \
            if _r1(x) <= lo + 1 else t_one_dp()

    return _pick_t([t_whole, t_one_dp, t_context, t_which, t_money], [t_line])


@skill("Y5.6.e", "Compare and order decimals to three places", S6)
def _(d=1):
    d = _d(d)
    w = random.randint(0, 9)
    k = _by(d, 3, 4, 5)
    vals = set()
    while len(vals) < k:
        dp = random.randint(1, 3)
        vals.add(Decimal(w) + Decimal(random.randint(1, 10 ** dp - 1)) / 10 ** dp)
    vals = list(vals)
    random.shuffle(vals)
    asc = sorted(vals)

    def t_larger():
        a, b = vals[0], vals[1]
        return _tb("Which is larger, %s or %s?" % (_ds(a), _ds(b)), _ds(max(a, b)), "num", {},
                   ["Compare digit by digit from the left."])

    def t_symbol():
        a, b = vals[0], vals[1]
        return _wq("Write <, > or =:  %s ___ %s" % (_ds(a), _ds(b)), "<" if a < b else ">",
                   ["Line up the decimal points; fill gaps with zeros."], "<, > or =")

    def t_smallest():
        return _tb("Which is the smallest? %s" % ", ".join(_ds(v) for v in vals), _ds(asc[0]), "num", {},
                   ["In order: %s." % ", ".join(_ds(v) for v in asc)])

    def t_position():
        i = random.randint(2, k)
        return _tb("Put these in order, smallest first. Which is %s? %s"
                   % ({2: "2nd", 3: "3rd"}.get(i, "%dth" % i), ", ".join(_ds(v) for v in vals)),
                   _ds(asc[i - 1]), "num", {}, ["In order: %s." % ", ".join(_ds(v) for v in asc)])

    def t_trap():
        a = Decimal(w) + Decimal(random.randint(2, 9)) / 10
        b = Decimal(w) + Decimal(random.randint(11, 99)) / 1000
        return _tb("Which is larger, %s or %s? (Careful: more digits does not mean larger.)"
                   % (_ds(a), _ds(b)), _ds(max(a, b)), "num", {},
                   ["%s = %s and %s." % (_ds(a), format(a, ".3f"), _ds(b))])

    def t_table():
        names = random.sample(["Maya", "Noah", "Sara", "Leo", "Priya"], k)
        rows = [[n, "%s m" % _ds(v)] for n, v in zip(names, vals)]
        win = names[vals.index(max(vals))]
        return _dt("The table shows how far each pupil threw a ball. Who threw the furthest?",
                   ["Name", "Distance"], rows, win, ["The largest is %s." % _ds(max(vals))], atype="str")

    return _pick_t([t_larger, t_symbol, t_smallest, t_position, t_trap], [t_table])


@skill("Y5.6.f", "Add and subtract decimals", S6)
def _(d=1):
    d = _d(d)
    dp = _by(d, 1, 2, 3)
    a = Decimal(random.randint(10, 999)) / 10 ** dp * pick([1, 10])
    b = Decimal(random.randint(10, 999)) / 10 ** random.randint(1, dp)

    def t_add():
        return _tb("Work out %s + %s." % (_ds(a), _ds(b)), _ds(a + b), "num", {},
                   ["Line up the decimal points.", "= %s." % _ds(a + b)])

    def t_sub():
        x, y = max(a, b), min(a, b)
        if x == y:
            return t_add()
        return _tb("Work out %s − %s." % (_ds(x), _ds(y)), _ds(x - y), "num", {},
                   ["Line up the decimal points; use zeros as place holders.", "= %s." % _ds(x - y)])

    def t_to_whole():
        w = random.randint(1, 10)
        y = Decimal(random.randint(1, 10 ** dp - 1)) / 10 ** dp
        return _tb("What must be added to %s to make %d?" % (_ds(w - 1 + y), w), _ds(1 - y), "num", {},
                   ["%d − %s = %s." % (w, _ds(w - 1 + y), _ds(1 - y))])

    def t_missing():
        return _tb("Find the missing number:  %s + ___ = %s" % (_ds(a), _ds(a + b)), _ds(b), "num", {},
                   ["%s − %s = %s." % (_ds(a + b), _ds(a), _ds(b))])

    def t_measure():
        x = Decimal(random.randint(101, 999)) / 100
        y = Decimal(random.randint(11, 99)) / 100
        return _tb("A ribbon is %s m long. %s m is cut off. How much is left, in metres?" % (_ds(x), _ds(y)),
                   _ds(x - y), "num", {"unit": "m"}, ["%s − %s = %s." % (_ds(x), _ds(y), _ds(x - y))])

    def t_three():
        xs = [Decimal(random.randint(1, 99)) / 10 for _ in range(3)]
        return _tb("Add: %s + %s + %s" % tuple(_ds(v) for v in xs), _ds(sum(xs)), "num", {},
                   ["= %s." % _ds(sum(xs))])

    return _pick_t([t_add, t_sub, t_to_whole, t_missing, t_measure, t_three])


@skill("Y5.6.g", "Problems with decimals to three places", S6)
def _(d=1):
    d = _d(d)

    def t_jumps():
        names = random.sample(["Maya", "Noah", "Sara", "Leo"], 2)
        a = Decimal(random.randint(200, 450)) / 100
        b = a + Decimal(random.randint(1, 60)) / 100
        return _tb("%s jumped %s m and %s jumped %s m. How much further did %s jump, in metres?"
                   % (names[0], _ds(a), names[1], _ds(b), names[1]), _ds(b - a), "num", {"unit": "m"},
                   ["%s − %s = %s." % (_ds(b), _ds(a), _ds(b - a))])

    def t_mass():
        a = Decimal(random.randint(100, 2999)) / 1000
        b = Decimal(random.randint(100, 2999)) / 1000
        return _tb("A bag of apples weighs %s kg and a bag of pears weighs %s kg. What is the total mass, "
                   "in kg?" % (_ds(a), _ds(b)), _ds(a + b), "num", {"unit": "kg"},
                   ["%s + %s = %s." % (_ds(a), _ds(b), _ds(a + b))])

    def t_race():
        t1 = Decimal(random.randint(1100, 1600)) / 100
        diff = Decimal(random.randint(1, 99)) / 100
        return _tb("In a 100 m race Noah ran %s seconds. Leo was %s seconds faster. What was Leo's time, in "
                   "seconds?" % (_ds(t1), _ds(diff)), _ds(t1 - diff), "num", {"unit": "seconds"},
                   ["Faster means less time: %s − %s = %s." % (_ds(t1), _ds(diff), _ds(t1 - diff))])

    def t_fill():
        cap = Decimal(random.randint(2, 5))
        a = Decimal(random.randint(100, 900)) / 1000
        b = Decimal(random.randint(100, 900)) / 1000
        if a + b >= cap:
            b = Decimal("0.25")
        return _tb("A %s litre jug has %s litres in it. %s litres are added. How much more is needed to "
                   "fill it, in litres?" % (_ds(cap), _ds(a), _ds(b)), _ds(cap - a - b), "num",
                   {"unit": "litres"}, ["%s + %s = %s." % (_ds(a), _ds(b), _ds(a + b)),
                                        "%s − %s = %s." % (_ds(cap), _ds(a + b), _ds(cap - a - b))])

    def t_table():
        names = ["Mon", "Tue", "Wed"]
        vals = [Decimal(random.randint(10, 99)) / 10 for _ in names]
        rows = [[n, "%s km" % _ds(v)] for n, v in zip(names, vals)]
        return _dt("The table shows how far %s cycled each day. What is the total distance, in km?" % _who(),
                   ["Day", "Distance"], rows, _ds(sum(vals)),
                   ["%s = %s." % (" + ".join(_ds(v) for v in vals), _ds(sum(vals)))], atype="num")

    return _pick_t([t_jumps, t_mass, t_race, t_fill], [t_table])


@skill("Y5.6.h", "Per cent as parts per hundred", S6)
def _(d=1):
    d = _d(d)
    p = random.randint(1, 99)

    def t_to_fraction():
        return _tb("Complete:  %d%% = ___/100" % p, p, "int", {}, ["Per cent means out of 100."])

    def t_to_decimal():
        return _tb("Write %d%% as a decimal." % p, _ds(Decimal(p) / 100), "num", {},
                   ["%d%% = %d/100 = %s." % (p, p, _ds(Decimal(p) / 100))])

    def t_from_decimal():
        return _tb("Write %s as a percentage. Give the number only." % _ds(Decimal(p) / 100), p, "int", {},
                   ["%s = %d/100 = %d%%." % (_ds(Decimal(p) / 100), p, p)])

    def t_rest():
        return _tb("%d%% of a class have school dinners. What percentage do NOT? Give the number only." % p,
                   100 - p, "int", {}, ["100 − %d = %d." % (p, 100 - p)])

    def t_grid():
        return _area("The square is split into 100 equal parts. Shade %d%% of it." % p,
                     {"mode": "fraction", "parts": 100}, "%d/100" % p, ["%d%% = %d out of 100." % (p, p)],
                     atype="frac")

    def t_read_grid():
        return _area("What percentage of the 100-square is shaded? Give the number only.",
                     {"mode": "fraction_read", "parts": 100, "shaded": p, "placeholder": "number"}, p,
                     ["%d of the 100 squares are shaded: %d%%." % (p, p)])

    def t_table():
        ps = random.sample(range(1, 99), 3)
        rows = [["%d%%" % x, "%d/100" % x, _ds(Decimal(x) / 100)] for x in ps]
        r, c = random.randrange(3), pick([1, 2])
        ans = ps[r] if c == 1 else _ds(Decimal(ps[r]) / 100)
        if c == 1:
            return _dt("Complete the table. Type the missing numerator (the number out of 100).",
                       ["Per cent", "Fraction", "Decimal"], rows, ans, ["%d%% = %d/100." % (ps[r], ps[r])],
                       missing=[r, 1])
        return _dt("Complete the table. What decimal belongs in the empty cell?", ["Per cent", "Fraction",
                                                                                   "Decimal"],
                   rows, ans, ["%d%% = %s." % (ps[r], ans)], missing=[r, 2], atype="num")

    return _pick_t([t_to_fraction, t_to_decimal, t_from_decimal, t_rest], [t_grid, t_read_grid, t_table])


@skill("Y5.6.i", "Percentage equivalents of halves, quarters, fifths, tenths and 25ths", S6)
def _(d=1):
    d = _d(d)
    f = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5),
              Fraction(4, 5), Fraction(random.randint(1, 9), 10), Fraction(random.randint(1, 24), 25),
              Fraction(random.randint(1, 49), 50)])
    pc = int(f * 100)

    def t_to_pc():
        return _tb("Write %s as a percentage. Give the number only." % _fs(f), pc, "int", {},
                   ["%s = %d/100 = %d%%." % (_fs(f), pc, pc)])

    def t_from_pc():
        return _wq("Write %d%% as a fraction in its simplest form." % pc, _fs(f),
                   ["%d%% = %d/100 = %s." % (pc, pc, _fs(f))], "e.g. 1/4")

    def t_compare():
        g = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(4, 5)])
        q = random.randint(1, 99)
        if g * 100 == q:
            q += 1
        return _wq("Which is greater, %s or %d%%? Type the one that is greater." % (_fs(g), q),
                   _fs(g) if g * 100 > q else "%d%%" % q, ["%s = %d%%." % (_fs(g), int(g * 100))],
                   "e.g. 3/4 or 70%")

    def t_score():
        den = pick([10, 20, 25, 50])
        sc = random.randint(1, den)
        return _tb("%s scored %d out of %d in a test. What percentage is that? Give the number only."
                   % (_who(), sc, den), sc * 100 // den, "int", {},
                   ["%d/%d = %d/100 = %d%%." % (sc, den, sc * 100 // den, sc * 100 // den)])

    def t_pie():
        a = pick([50, 25, 20, 10])
        rest = 100 - a
        b = rest // 2
        slices = [["Football", a], ["Swimming", b], ["Tennis", rest - b]]
        return {"prompt": "The pie chart shows favourite sports. What percentage chose Football? Give the "
                          "number only.", "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": a, "answer_type": "int",
                "solution": ["Football is %s of the circle: %d%%." % (_fs(Fraction(a, 100)), a)]}

    return _pick_t([t_to_pc, t_from_pc, t_compare, t_score], [t_pie])


@skill("Y5.6.j", "Percentage problems", S6)
def _(d=1):
    d = _d(d)

    def t_simple_of():
        p, x = pick([(50, 2), (25, 4), (10, 10), (20, 5)]), random.randint(2, 20)
        amt = p[1] * x * pick([1, 10])
        return _tb("What is %d%% of %d?" % (p[0], amt), amt * p[0] // 100, "int", {},
                   ["%d%% = 1/%d." % (p[0], p[1]), "%d ÷ %d = %d." % (amt, p[1], amt * p[0] // 100)])

    def t_sale():
        p = pick([10, 20, 25, 50])
        price = random.randint(2, 20) * (100 // _gcd(p, 100))      # the saving is a whole number of pounds
        off = price * p // 100
        return _tb("A game costs £%d. There is %d%% off. How much do you save, in pounds?" % (price, p), off,
                   "int", {"unit": "£"}, ["%d%% of %d = %d." % (p, price, off)])

    def t_left():
        n = pick([20, 40, 50, 100, 200])
        p = pick([10, 20, 25, 50, 75])
        if n * p % 100:
            n = 100
        return _tb("A farmer has %d sheep. %d%% are in the top field. How many are NOT in the top field?"
                   % (n, p), n - n * p // 100, "int", {},
                   ["%d%% of %d = %d." % (p, n, n * p // 100), "%d − %d = %d." % (n, n * p // 100, n - n * p // 100)])

    def t_compare_scores():
        a_s, a_t = random.randint(10, 20), 20
        b_s, b_t = random.randint(10, 25), 25
        pa, pb = a_s * 5, b_s * 4
        if pa == pb:
            b_s += 1
            pb = b_s * 4
        return _wq("Maya scored %d out of 20. Noah scored %d out of 25. Who did better? (compare the "
                   "percentages)" % (a_s, b_s), "Maya" if pa > pb else "Noah",
                   ["Maya: %d%%. Noah: %d%%." % (pa, pb)], "name")

    def t_grid():
        s = random.randint(5, 95)
        return _area("Some of this 100-square is shaded. What percentage is NOT shaded? Give the number only.",
                     {"mode": "fraction_read", "parts": 100, "shaded": s, "placeholder": "number"}, 100 - s,
                     ["%d%% is shaded, so %d%% is not." % (s, 100 - s)])

    return _pick_t([t_simple_of, t_sale, t_left, t_compare_scores], [t_grid])


# ================================================================== 5.7 ======
_CONV = [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10), ("kg", "g", 1000), ("l", "ml", 1000),
         ("m", "mm", 1000)]


@skill("Y5.7.a", "Convert between metric units", S7)
def _(d=1):
    d = _d(d)
    big, small, f = pick(_CONV)

    def t_down():
        x = random.randint(2, 30) if d == 0 else Decimal(random.randint(11, 999)) / pick([10, 100])
        return _tb("Convert %s %s into %s." % (_ds(x), big, small), _ds(Decimal(str(x)) * f), "num",
                   {"unit": small}, ["1 %s = %d %s, so × %d." % (big, f, small, f)])

    def t_up():
        x = random.randint(1, 99) * (f // 10 if f >= 100 else 1) + (random.randint(1, 9) if d else 0)
        return _tb("Convert %s %s into %s." % (_c(x), small, big), _ds(Decimal(x) / f), "num", {"unit": big},
                   ["%d %s = 1 %s, so ÷ %d." % (f, small, big, f)])

    def t_mixed_units():
        w, r = random.randint(1, 9), random.randint(1, f - 1)
        return _tb("Write %d %s %d %s in %s." % (w, big, r, small, small), w * f + r, "int", {"unit": small},
                   ["%d × %d + %d = %d." % (w, f, r, w * f + r)])

    def t_compare():
        x = random.randint(1, 9)
        y = x * f + pick([-1, 1]) * random.randint(1, f // 2)
        bigger = "%d %s" % (x, big) if x * f > y else "%d %s" % (y, small)
        return _wq("Which is more: %d %s or %d %s? Type it exactly as written." % (x, big, y, small), bigger,
                   ["%d %s = %d %s." % (x, big, x * f, small)], "e.g. 3 kg")

    def t_add():
        a = Decimal(random.randint(11, 99)) / 10
        b = random.randint(100, f - 1) if f >= 1000 else random.randint(1, f - 1)
        return _tb("Add %s %s and %d %s. Give your answer in %s." % (_ds(a), big, b, small, small),
                   _ds(a * f + b), "num", {"unit": small},
                   ["%s %s = %s %s." % (_ds(a), big, _ds(a * f), small), "+ %d = %s." % (b, _ds(a * f + b))])

    def t_table():
        xs = random.sample(range(1, 20), 4)
        rows = [["%d %s" % (x, big), "%d %s" % (x * f, small)] for x in xs]
        k = random.randrange(4)
        rows[k][1] = ""
        return _dt("This table converts %s to %s. What number belongs in the empty cell, in %s?"
                   % (big, small, small), [big, small], rows, xs[k] * f,
                   ["%d × %d = %d." % (xs[k], f, xs[k] * f)], missing=[k, 1])

    def t_ruler():
        mm = random.randint(11, 189)
        return {"prompt": "Read the ruler. How long is the line, in millimetres?",
                "component": "ruler", "spec": {"mode": "length", "value": mm / 10, "max": 20, "unit": "cm"},
                "answer": mm, "answer_type": "num", "tolerance": 3,
                "solution": ["%s cm = %d mm." % (_ds(Decimal(mm) / 10), mm)]} if mm % 5 == 0 else t_up()

    return _pick_t([t_down, t_up, t_mixed_units, t_compare, t_add], [t_table, t_ruler])


@skill("Y5.7.b", "Approximate imperial equivalents", S7)
def _(d=1):
    d = _d(d)

    def t_inches():
        n = random.randint(2, 12)
        return _tb("1 inch is about 2.5 cm. About how many centimetres is %d inches?" % n,
                   _ds(Decimal(n) * Decimal("2.5")), "num", {"unit": "cm"},
                   ["%d × 2.5 = %s." % (n, _ds(Decimal(n) * Decimal("2.5")))], tol=0.01)

    def t_pounds():
        n = random.randint(2, 20)
        return _tb("1 kg is about 2.2 pounds. About how many pounds is %d kg?" % n,
                   _ds(Decimal(n) * Decimal("2.2")), "num", {"unit": "pounds"},
                   ["%d × 2.2 = %s." % (n, _ds(Decimal(n) * Decimal("2.2")))])

    def t_pints():
        n = random.randint(2, 12)
        return _tb("1 litre is about 1.75 pints. About how many pints is %d litres?" % n,
                   _ds(Decimal(n) * Decimal("1.75")), "num", {"unit": "pints"},
                   ["%d × 1.75 = %s." % (n, _ds(Decimal(n) * Decimal("1.75")))])

    def t_feet():
        n = random.randint(2, 10)
        return _tb("1 foot is 12 inches. How many inches are in %d feet?" % n, 12 * n, "int",
                   {"unit": "inches"}, ["%d × 12 = %d." % (n, 12 * n)])

    def t_miles():
        n = 5 * random.randint(1, 12)
        return _tb("5 miles is about 8 km. About how many km is %d miles?" % n, n // 5 * 8, "int",
                   {"unit": "km"}, ["%d ÷ 5 = %d lots of 5 miles." % (n, n // 5), "%d × 8 = %d." % (n // 5, n // 5 * 8)])

    def t_back():
        n = random.randint(2, 10)
        return _tb("1 pound is about 450 g. About how many grams is %d pounds?" % n, 450 * n, "int",
                   {"unit": "g"}, ["%d × 450 = %d." % (n, 450 * n)])

    def t_sensible():
        q, a = pick([("How tall is a door, in feet: about 7, 70 or 700?", 7),
                     ("How much milk is in a big carton, in pints: about 4, 40 or 400?", 4),
                     ("How heavy is a bag of sugar, in pounds: about 2, 20 or 200?", 2),
                     ("How long is a pencil, in inches: about 7, 70 or 700?", 7)])
        return _tb(q, a, "int", {}, ["Use what you know about everyday objects."])

    def t_table():
        rows = [[i, _ds(Decimal(i) * Decimal("2.5"))] for i in (1, 2, 4, 6, 10)]
        k = random.randint(1, 4)
        return _dt("This table converts inches to centimetres (1 inch ≈ 2.5 cm). What belongs in the empty "
                   "cell?", ["Inches", "Centimetres"], rows, rows[k][1],
                   ["%d × 2.5 = %s." % (rows[k][0], rows[k][1])], missing=[k, 1], atype="num")

    return _pick_t([t_inches, t_pounds, t_pints, t_feet, t_miles, t_back, t_sensible], [t_table])


def _l_shape(d):
    """An L-shaped rectilinear figure as grid cells, plus its full width/height and the cut-out."""
    W, H = random.randint(4, _by(d, 6, 8, 10)), random.randint(4, _by(d, 6, 8, 9))
    cw, ch = random.randint(1, W - 2), random.randint(1, H - 2)
    cells = [[r, c] for r in range(H) for c in range(W) if not (r < ch and c >= W - cw)]
    return W, H, cw, ch, cells


@skill("Y5.7.c", "Perimeter of composite rectilinear shapes", S7)
def _(d=1):
    d = _d(d)

    def t_grid():
        W, H, cw, ch, cells = _l_shape(d)
        return _area("Each square is 1 cm long. What is the perimeter of this shape, in cm?",
                     {"mode": "read_perimeter", "cells": cells, "rows": H, "cols": W}, 2 * (W + H),
                     ["An L-shape has the same perimeter as its surrounding rectangle.",
                      "2 × (%d + %d) = %d cm." % (W, H, 2 * (W + H))])

    def t_l_words():
        W, H = random.randint(8, 20), random.randint(6, 16)
        cw, ch = random.randint(2, W - 3), random.randint(2, H - 3)
        return _tb("An L-shaped garden is made by cutting a %d m by %d m rectangle out of one corner of a "
                   "%d m by %d m rectangle. What is the perimeter of the garden, in m?" % (cw, ch, W, H),
                   2 * (W + H), "int", {"unit": "m"},
                   ["Cutting out a corner does not change the total perimeter here.",
                    "2 × (%d + %d) = %d m." % (W, H, 2 * (W + H))])

    def t_missing_side():
        W, H = random.randint(8, 20), random.randint(6, 16)
        cw = random.randint(2, W - 3)
        return _tb("An L-shape has a bottom edge of %d cm. Its top edge is %d cm. A step in the shape "
                   "makes a short horizontal edge. How long is that short edge, in cm?" % (W, W - cw), cw,
                   "int", {"unit": "cm"}, ["%d − %d = %d." % (W, W - cw, cw)])

    def t_rect():
        a, b = random.randint(3, 30), random.randint(3, 30)
        unit = pick(["cm", "m"])
        return _tb("A rectangle is %d %s by %d %s. What is its perimeter, in %s?" % (a, unit, b, unit, unit),
                   2 * (a + b), "int", {"unit": unit}, ["2 × (%d + %d) = %d." % (a, b, 2 * (a + b))])

    def t_inverse():
        a = random.randint(3, 25)
        p = 2 * (a + random.randint(3, 25))
        return _tb("A rectangle has a perimeter of %d cm. One side is %d cm. How long is the other side, in "
                   "cm?" % (p, a), p // 2 - a, "int", {"unit": "cm"},
                   ["Half the perimeter is %d." % (p // 2), "%d − %d = %d." % (p // 2, a, p // 2 - a)])

    def t_metres():
        a, b = Decimal(random.randint(15, 95)) / 10, Decimal(random.randint(15, 95)) / 10
        return _tb("A rectangular pond is %s m by %s m. What is its perimeter, in metres?" % (_ds(a), _ds(b)),
                   _ds(2 * (a + b)), "num", {"unit": "m"}, ["2 × (%s + %s) = %s." % (_ds(a), _ds(b), _ds(2 * (a + b)))])

    return _pick_t([t_l_words, t_missing_side, t_rect, t_inverse, t_metres], [t_grid])


@skill("Y5.7.d", "Area of rectangles and compound shapes in cm² and m²", S7)
def _(d=1):
    d = _d(d)

    def t_rect():
        a, b = random.randint(2, _by(d, 12, 25, 40)), random.randint(2, _by(d, 12, 20, 30))
        unit = pick(["cm", "m"])
        return _tb("A rectangle is %d %s long and %d %s wide. What is its area, in %s²?" % (a, unit, b, unit, unit),
                   a * b, "int", {"unit": unit + "²"}, ["%d × %d = %d." % (a, b, a * b)])

    def t_side():
        a, b = random.randint(2, 15), random.randint(2, 15)
        return _tb("A rectangle has an area of %d cm². One side is %d cm. How long is the other side, in cm?"
                   % (a * b, a), b, "int", {"unit": "cm"}, ["%d ÷ %d = %d." % (a * b, a, b)])

    def t_square():
        k = random.randint(2, 12)
        return _tb("A square has sides of %d m. What is its area, in m²?" % k, k * k, "int", {"unit": "m²"},
                   ["%d × %d = %d." % (k, k, k * k)])

    def t_compound():
        W, H, cw, ch, cells = _l_shape(d)
        return _area("Each square is 1 cm². What is the area of this shape, in cm²?",
                     {"mode": "read_area", "cells": cells, "rows": H, "cols": W}, len(cells),
                     ["Whole rectangle: %d × %d = %d." % (W, H, W * H),
                      "Cut-out: %d × %d = %d." % (cw, ch, cw * ch), "%d − %d = %d." % (W * H, cw * ch, len(cells))])

    def t_l_words():
        W, H = random.randint(8, 20), random.randint(6, 16)
        cw, ch = random.randint(2, W - 3), random.randint(2, H - 3)
        return _tb("An L-shaped room is a %d m by %d m rectangle with a %d m by %d m corner missing. What is "
                   "its floor area, in m²?" % (W, H, cw, ch), W * H - cw * ch, "int", {"unit": "m²"},
                   ["%d × %d = %d." % (W, H, W * H), "%d × %d = %d." % (cw, ch, cw * ch),
                    "%d − %d = %d." % (W * H, cw * ch, W * H - cw * ch)])

    def t_compare():
        a, b, c, e = [random.randint(3, 12) for _ in range(4)]
        if a * b == c * e:
            e += 1
        return _wq("Rectangle A is %d cm by %d cm. Rectangle B is %d cm by %d cm. Which has the larger "
                   "area? (A or B)" % (a, b, c, e), "A" if a * b > c * e else "B",
                   ["A = %d cm², B = %d cm²." % (a * b, c * e)], "A or B")

    def t_same_perimeter():
        a, b = random.randint(2, 6), random.randint(7, 12)
        p = 2 * (a + b)
        side = p // 4
        return _tb("A %d cm by %d cm rectangle and a square have the same perimeter (%d cm). How much larger "
                   "is the area of the square, in cm²?" % (a, b, p), side * side - a * b, "int", {"unit": "cm²"},
                   ["The square has sides of %d cm, area %d cm²." % (side, side * side),
                    "The rectangle's area is %d cm²." % (a * b)]) if p % 4 == 0 else t_compare()

    def t_build():
        n = random.randint(8, 30)
        return _area("Each square is 1 cm². Shade squares to make a shape with an area of %d cm²." % n,
                     {"mode": "build_area", "rows": 6, "cols": 8}, n, ["Shade %d squares." % n])

    return _pick_t([t_rect, t_side, t_square, t_l_words, t_compare, t_same_perimeter], [t_compound, t_build])


@skill("Y5.7.e", "Estimate the area of irregular shapes", S7)
def _(d=1):
    d = _d(d)

    def t_count():
        whole, half = random.randint(6, 30), 2 * random.randint(1, 8)
        return _tb("A leaf drawn on a 1 cm grid covers %d whole squares and %d half squares. Estimate its "
                   "area, in cm²." % (whole, half), whole + half // 2, "int", {"unit": "cm²"},
                   ["Two halves make one whole: %d ÷ 2 = %d." % (half, half // 2),
                    "%d + %d = %d cm²." % (whole, half // 2, whole + half // 2)])

    def t_more_than_half():
        whole, big = random.randint(6, 30), random.randint(2, 12)
        return _tb("A puddle drawn on a 1 cm grid fully covers %d squares. It covers more than half of %d "
                   "other squares and less than half of some more. Count a square if more than half is "
                   "covered. Estimate the area, in cm²." % (whole, big), whole + big, "int", {"unit": "cm²"},
                   ["%d + %d = %d cm²." % (whole, big, whole + big)])

    def t_cells():
        rows, cols = 6, 8
        cells = {(random.randrange(rows), random.randrange(cols))}
        target = random.randint(10, 26)
        while len(cells) < target:                     # grow one connected blob
            r, c = random.choice(sorted(cells))
            dr, dc = pick([(0, 1), (1, 0), (0, -1), (-1, 0)])
            if 0 <= r + dr < rows and 0 <= c + dc < cols:
                cells.add((r + dr, c + dc))
        cells = [list(x) for x in sorted(cells)]
        return _area("Each square is 1 cm². Count the squares to find the area of this shape, in cm².",
                     {"mode": "read_area", "cells": cells, "rows": rows, "cols": cols}, len(cells),
                     ["There are %d squares." % len(cells)])

    def t_between():
        lo = random.randint(10, 40)
        return _tb("A pond fully covers %d squares of a 1 m grid and touches %d more squares. Its area is "
                   "between %d m² and how many m²?" % (lo, lo // 2, lo), lo + lo // 2, "int", {"unit": "m²"},
                   ["At most it covers every touched square: %d + %d = %d." % (lo, lo // 2, lo + lo // 2)])

    return _pick_t([t_count, t_more_than_half, t_between], [t_cells])


@skill("Y5.7.f", "Volume of cuboids using 1 cm³ cubes", S7)
def _(d=1):
    d = _d(d)
    l, w, h = random.randint(2, _by(d, 4, 6, 10)), random.randint(2, _by(d, 3, 5, 8)), random.randint(1, _by(d, 3, 5, 6))

    def t_count():
        return _tb("A cuboid is built from 1 cm cubes: %d cubes long, %d wide and %d tall. How many cubes "
                   "is that?" % (l, w, h), l * w * h, "int", {"unit": "cm³"},
                   ["%d × %d = %d in one layer." % (l, w, l * w), "%d layers: %d." % (h, l * w * h)])

    def t_layer():
        return _tb("One layer of a cuboid has %d cubes. The cuboid has %d layers. What is its volume, in cm³?"
                   % (l * w, h), l * w * h, "int", {"unit": "cm³"}, ["%d × %d = %d." % (l * w, h, l * w * h)])

    def t_missing():
        v = l * w * h
        return _tb("A cuboid has a volume of %d cm³. It is %d cm long and %d cm wide. How tall is it, in cm?"
                   % (v, l, w), h, "int", {"unit": "cm"}, ["%d × %d = %d." % (l, w, l * w),
                                                           "%d ÷ %d = %d." % (v, l * w, h)])

    def t_compare():
        a = (random.randint(2, 6), random.randint(2, 6), random.randint(2, 6))
        b = (random.randint(2, 6), random.randint(2, 6), random.randint(2, 6))
        va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
        if va == vb:
            return t_count()
        return _wq("Box A is %d × %d × %d cm. Box B is %d × %d × %d cm. Which holds more 1 cm cubes? (A or B)"
                   % (a + b), "A" if va > vb else "B", ["A: %d cm³. B: %d cm³." % (va, vb)], "A or B")

    def t_cube():
        k = random.randint(2, 6)
        return _tb("A cube has edges of %d cm. What is its volume, in cm³?" % k, k ** 3, "int",
                   {"unit": "cm³"}, ["%d × %d × %d = %d." % (k, k, k, k ** 3)])

    def t_table():
        rows = [["Length", "%d cm" % l], ["Width", "%d cm" % w], ["Height", "%d cm" % h]]
        return _dt("The table gives the size of a cuboid. What is its volume, in cm³?", ["Measure", "Size"],
                   rows, l * w * h, ["%d × %d × %d = %d." % (l, w, h, l * w * h)])

    return _pick_t([t_count, t_layer, t_missing, t_compare, t_cube], [t_table])


@skill("Y5.7.g", "Estimate and measure capacity", S7)
def _(d=1):
    d = _d(d)

    def t_jug():
        mx = pick([500, 1000, 2000])
        v = random.randint(1, mx // 50 - 1) * 50
        return {"prompt": "Read the measuring jug. How much water is in it, in ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": mx, "unit": "ml"}, "answer": v,
                "answer_type": "num", "tolerance": 25, "solution": ["The water reaches %d ml." % v]}

    def t_sensible():
        q, a = pick([("A teaspoon holds about 5 ml, 50 ml or 500 ml?", 5),
                     ("A can of drink holds about 33 ml, 330 ml or 3,300 ml?", 330),
                     ("A bath holds about 15 litres, 150 litres or 1,500 litres?", 150),
                     ("A mug holds about 3 ml, 300 ml or 3,000 ml?", 300),
                     ("A bucket holds about 1 litre, 10 litres or 100 litres?", 10)])
        return _tb(q + " Type the number.", a, "int", {}, ["Think about the real object."])

    def t_cups():
        cup, n = pick([150, 200, 250]), random.randint(2, 8)
        bottle = pick([1000, 2000])
        if cup * n > bottle:
            n = bottle // cup
        return _tb("A %d litre bottle of squash fills cups of %d ml. %d cups are poured. How much is left, in "
                   "ml?" % (bottle // 1000, cup, n), bottle - cup * n, "int", {"unit": "ml"},
                   ["%d × %d = %d." % (n, cup, n * cup), "%d − %d = %d." % (bottle, n * cup, bottle - n * cup)])

    def t_how_many():
        cup = pick([100, 200, 250, 500])
        tot = pick([1000, 2000, 3000])
        return _tb("How many %d ml glasses can be filled from %d litres?" % (cup, tot // 1000), tot // cup,
                   "int", {}, ["%d litres = %d ml." % (tot // 1000, tot), "%d ÷ %d = %d." % (tot, cup, tot // cup)])

    def t_volume_capacity():
        l, w, h = random.randint(5, 20), random.randint(5, 20), random.randint(5, 20)
        return _tb("A box-shaped tank is %d cm × %d cm × %d cm inside. 1 cm³ holds 1 ml. How many ml does it "
                   "hold?" % (l, w, h), l * w * h, "int", {"unit": "ml"}, ["%d × %d × %d = %d." % (l, w, h, l * w * h)])

    return _pick_t([t_sensible, t_cups, t_how_many, t_volume_capacity], [t_jug])


@skill("Y5.7.h", "Convert between units of time", S7)
def _(d=1):
    d = _d(d)

    def t_hm():
        h, m = random.randint(1, 5), random.randint(1, 59)
        return _tb("How many minutes are in %d hours %d minutes?" % (h, m), 60 * h + m, "int",
                   {"unit": "minutes"}, ["%d × 60 + %d = %d." % (h, m, 60 * h + m)])

    def t_mh():
        m = random.randint(61, 400)
        return _tb("Write %d minutes as hours and minutes in the form h:mm (for example 2:15 means 2 hours "
                   "15 minutes)." % m, "%d:%02d" % divmod(m, 60), "time", {"text": True, "placeholder": "h:mm"},
                   ["%d ÷ 60 = %d remainder %d." % (m, m // 60, m % 60)])

    def t_seconds():
        m, s = random.randint(1, 6), random.randint(0, 59)
        return _tb("How many seconds are in %d minutes %d seconds?" % (m, s), 60 * m + s, "int",
                   {"unit": "seconds"}, ["%d × 60 + %d = %d." % (m, s, 60 * m + s)])

    def t_days():
        w = random.randint(2, 12)
        return _tb("How many days are in %d weeks?" % w, 7 * w, "int", {"unit": "days"}, ["%d × 7 = %d." % (w, 7 * w)])

    def t_months():
        y = random.randint(2, 9)
        return _tb("How many months are in %d years?" % y, 12 * y, "int", {"unit": "months"},
                   ["%d × 12 = %d." % (y, 12 * y)])

    def t_month_days():
        m, days = pick([("April", 30), ("June", 30), ("September", 30), ("November", 30), ("January", 31),
                        ("March", 31), ("July", 31), ("October", 31), ("December", 31)])
        return _tb("How many days are there in %s?" % m, days, "int", {"unit": "days"},
                   ["30 days has September, April, June and November."])

    def t_leap():
        y = pick([2024, 2028, 2032, 2025, 2026, 2027, 2030])
        return _tb("How many days are there in the year %d?" % y, 366 if y % 4 == 0 else 365, "int",
                   {"unit": "days"}, ["%d %s divisible by 4, so it %s a leap year." % (y, "is" if y % 4 == 0 else
                                                                                       "is not",
                                                                                       "is" if y % 4 == 0 else "is not")])

    def t_hours_days():
        h = random.randint(2, 5) * 24 + random.randint(0, 23)
        return _tb("%d hours is some whole days and some hours left over. How many hours are left over?" % h,
                   h % 24, "int", {"unit": "hours"}, ["%d ÷ 24 = %d remainder %d." % (h, h // 24, h % 24)])

    def t_timetable():
        starts = [(9, 15), (10, 5), (11, 40)]
        k = random.randrange(3)
        dur = random.randint(25, 95)
        sh, sm = starts[k]
        end = sh * 60 + sm + dur
        rows = [["Bus %s" % "ABC"[i], "%02d:%02d" % st, "%02d:%02d" % divmod(st[0] * 60 + st[1] + dur, 60)]
                for i, st in enumerate(starts)]
        return _dt("The timetable shows three buses that all take the same time. How many minutes does each "
                   "journey take?", ["Bus", "Leaves", "Arrives"], rows, dur,
                   ["%02d:%02d to %02d:%02d is %d minutes." % (sh, sm, end // 60, end % 60, dur)])

    return _pick_t([t_hm, t_mh, t_seconds, t_days, t_months, t_month_days, t_leap, t_hours_days], [t_timetable])


@skill("Y5.7.i", "Measure problems using decimals and scaling", S7)
def _(d=1):
    d = _d(d)

    def t_scale_recipe():
        g = Decimal(random.randint(5, 40)) * 10
        k = random.randint(2, 5)
        return _tb("A cake for 6 people needs %s g of flour. How much flour, in kg, for %d people?"
                   % (_ds(g), 6 * k), _ds(g * k / 1000), "num", {"unit": "kg"},
                   ["%s × %d = %s g." % (_ds(g), k, _ds(g * k)), "= %s kg." % _ds(g * k / 1000)])

    def t_lengths():
        n = random.randint(3, 9)
        x = Decimal(random.randint(11, 99)) / 10
        return _tb("%d planks are each %s m long. What is their total length, in metres?" % (n, _ds(x)),
                   _ds(n * x), "num", {"unit": "m"}, ["%d × %s = %s." % (n, _ds(x), _ds(n * x))])

    def t_share():
        n = random.randint(2, 8)
        each = Decimal(random.randint(11, 99)) / 100
        tot = each * n
        return _tb("%s litres of juice are shared equally into %d bottles. How much is in each bottle, in "
                   "litres?" % (_ds(tot), n), _ds(each), "num", {"unit": "litres"},
                   ["%s ÷ %d = %s." % (_ds(tot), n, _ds(each))])

    def t_mixed_units():
        a = Decimal(random.randint(11, 49)) / 10
        b = random.randint(150, 950)
        return _tb("A parcel weighs %s kg. A second parcel weighs %d g. What is their total mass, in kg?"
                   % (_ds(a), b), _ds(a + Decimal(b) / 1000), "num", {"unit": "kg"},
                   ["%d g = %s kg." % (b, _ds(Decimal(b) / 1000)), "%s + %s = %s." % (_ds(a), _ds(Decimal(b) / 1000),
                                                                                     _ds(a + Decimal(b) / 1000))])

    def t_run():
        lap = Decimal(random.randint(2, 8)) / 10
        n = random.randint(3, 12)
        return _tb("A running track is %s km round. %s runs %d laps. How far is that, in km?" % (_ds(lap), _who(), n),
                   _ds(lap * n), "num", {"unit": "km"}, ["%d × %s = %s." % (n, _ds(lap), _ds(lap * n))])

    return _pick_t([t_scale_recipe, t_lengths, t_share, t_mixed_units, t_run])


@skill("Y5.7.j", "Money problems with decimals", S7)
def _(d=1):
    d = _d(d)

    def t_change():
        n = _by(d, 2, 3, 3)
        pay = pick([5, 10, 20])
        items = [Decimal(random.randint(50, pay * 100 // n - 10)) / 100 for _ in range(n)]
        return _tb("%s buys items costing %s and pays with £%d. How much change, in pounds?"
                   % (_who(), ", ".join("£" + format(i, ".2f") for i in items), pay), _ds(pay - sum(items)), "num",
                   {"unit": "£"}, ["Total: £%s." % format(sum(items), ".2f"),
                                   "£%d − £%s = £%s." % (pay, format(sum(items), ".2f"), format(pay - sum(items), ".2f"))])

    def t_multiple():
        p = Decimal(random.randint(105, 999)) / 100
        n = random.randint(3, 9)
        return _tb("A comic costs £%s. How much do %d comics cost, in pounds?" % (format(p, ".2f"), n), _ds(p * n),
                   "num", {"unit": "£"}, ["£%s × %d = £%s." % (format(p, ".2f"), n, format(p * n, ".2f"))])

    def t_split():
        n = random.randint(2, 6)
        each = Decimal(random.randint(150, 2500)) / 100
        return _tb("A bill of £%s is shared equally between %d friends. How much does each pay, in pounds?"
                   % (format(each * n, ".2f"), n), _ds(each), "num", {"unit": "£"},
                   ["£%s ÷ %d = £%s." % (format(each * n, ".2f"), n, format(each, ".2f"))])

    def t_save():
        price = Decimal(random.randint(1500, 9000)) / 100
        have = Decimal(random.randint(200, int(price * 100) - 100)) / 100
        return _tb("A bike helmet costs £%s. %s has saved £%s. How much more is needed, in pounds?"
                   % (format(price, ".2f"), _who(), format(have, ".2f")), _ds(price - have), "num", {"unit": "£"},
                   ["£%s − £%s = £%s." % (format(price, ".2f"), format(have, ".2f"), format(price - have, ".2f"))])

    def t_table():
        menu = [("Sandwich", random.randint(180, 399)), ("Juice", random.randint(80, 199)),
                ("Fruit pot", random.randint(90, 249)), ("Muffin", random.randint(120, 299))]
        rows = [[n, "£" + format(Decimal(p) / 100, ".2f")] for n, p in menu]
        a, b = random.sample(range(4), 2)
        qa = random.randint(1, 3)
        tot = Decimal(menu[a][1] * qa + menu[b][1]) / 100
        return _dt("Use the price list. How much do %d %s%s and one %s cost altogether, in pounds?"
                   % (qa, menu[a][0].lower(), "" if qa == 1 else "s", menu[b][0].lower()), ["Item", "Price"], rows,
                   _ds(tot), ["%d × £%s + £%s = £%s." % (qa, format(Decimal(menu[a][1]) / 100, ".2f"),
                                                         format(Decimal(menu[b][1]) / 100, ".2f"), format(tot, ".2f"))],
                   atype="num")

    return _pick_t([t_change, t_multiple, t_split, t_save], [t_table])
