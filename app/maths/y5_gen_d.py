# Year 5 generators: strands 5.6 and 5.7.
#
# Decimals to three places (place value, fractions <-> decimals, rounding, ordering, adding and
# subtracting, problems), per cent as "parts per hundred" and the key equivalences.
# Measurement: metric conversions, imperial approximations, perimeter of composite rectilinear
# shapes, area of rectangles and irregular shapes, volume and capacity, time conversions, measure
# and money problems with decimals.
from .maths_engine import skill, n_words
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
        ks = [i for i in range(len(dec)) if dec[i] != "0" and s.count(dec[i]) == 1]
        if not ks:
            return t_thousandths()
        k = pick(ks)
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
        p = pick([10, 100, 1000][len(dec) - 1:])
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
                    Decimal("0.05"), ["%s is %s after %s." % (_ds(x2), _pl(int((x2 - lo) * 100), "hundredth"),
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
                   ["%s means %s." % (_ds(x), _pl(n, DPLACE[dp][:-1]))])

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

    def t_race():
        return _fq("%s has run %s of a race. What fraction of the race is that?" % (_who(), _ds(x)), Fraction(n, 10 ** dp),
                   ["%s = %d/%d." % (_ds(x), n, 10 ** dp)])

    def t_yes_no():
        right = random.random() < 0.5
        den = 10 ** dp if right else 10 ** (dp + 1)
        return _wq("Is %s equal to %d/%d? (yes or no)" % (_ds(x), n, den), "yes" if right else "no",
                   ["%s = %d/%d." % (_ds(x), n, 10 ** dp)], "yes / no")

    def t_money():
        p = random.randint(1, 99)
        return _fq("£%s is what fraction of £1?" % format(Decimal(p) / 100, ".2f"), Fraction(p, 100),
                   ["£1 = 100p, so %dp is %d/100 of £1." % (p, p)])

    def t_count():
        name = DPLACE[dp]
        return _tb("%s is how many %s?" % (_ds(x), name), n, "int", {},
                   ["%s = %d/%d, which is %s." % (_ds(x), n, 10 ** dp, _pl(n, name[:-1]))])

    def t_table():
        vals = random.sample([v for v in range(1, 10 ** dp) if v % 10], 3)
        rows = [[_ds(Decimal(v) / 10 ** dp), "%d/%d" % (v, 10 ** dp)] for v in vals]
        k = random.randrange(3)
        rows[k][1] = "?/%d" % 10 ** dp
        return _dt("The table matches decimals to fractions. What is the missing numerator?", ["Decimal", "Fraction"],
                   rows, vals[k], ["%s = %d/%d." % (rows[k][0], vals[k], 10 ** dp)])

    def t_line():
        if dp > 2:
            return t_fraction()
        return _nld("Place %d/%d on the number line from 0 to 1." % (n, 10 ** dp), Fraction(n, 10 ** dp), 0, 1,
                    Fraction(1, 10 ** dp), Fraction(1, 10), ["%d/%d = %s." % (n, 10 ** dp, _ds(x))])

    return _pick_t([t_over_power, t_fraction, t_simplest, t_mixed, t_race, t_yes_no, t_money, t_count],
                   [t_grid, t_table, t_line])


@skill("Y5.6.c", "Write fractions as decimals", S6)
def _(d=1):
    d = _d(d)

    def t_power():
        dp = _by(d, 1, 2, 3)
        n = random.randint(1, 10 ** dp - 1)
        return _tb("Write %d/%d as a decimal." % (n, 10 ** dp), _ds(Decimal(n) / 10 ** dp), "num", {},
                   ["%d ÷ %d = %s." % (n, 10 ** dp, _ds(Decimal(n) / 10 ** dp))])

    def t_key():
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)],
                     [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                      Fraction(3, 5), Fraction(4, 5)],
                     [Fraction(3, 5), Fraction(4, 5), Fraction(3, 20), Fraction(9, 20), Fraction(7, 25),
                      Fraction(12, 25), Fraction(13, 50)]))
        return _tb("Write %s as a decimal." % _fs(f), _ds(f), "num", {},
                   ["%s = %d/%d = %s." % (_fs(f), f.numerator * (100 // f.denominator), 100, _ds(f))])

    def t_scale():
        den = pick(_by(d, [2, 4, 5, 10], [2, 4, 5, 20, 25, 50], [4, 20, 25, 50]))
        num = random.randint(1, den - 1)
        if d == 2 and random.random() < 0.5:           # hard: an improper fraction, so the decimal is over 1
            num += den
        f = Fraction(num, den)
        k = 100 // den
        return _tb("Write %d/%d as a decimal. (Hint: make the denominator 100.)" % (num, den), _ds(f), "num",
                   {}, ["%d/%d = %d/100 = %s." % (num, den, num * k, _ds(f))])

    def t_mixed():
        w = random.randint(1, _by(d, 5, 9, 60))
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(7, 10)],
                     [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(7, 10), Fraction(9, 100)],
                     [Fraction(3, 5), Fraction(9, 100), Fraction(7, 1000), Fraction(43, 1000), Fraction(9, 20)]))
        return _tb("Write %d %s as a decimal." % (w, _fs(f)), _ds(w + f), "num", {},
                   ["%s = %s, so %s." % (_fs(f), _ds(f), _ds(w + f))])

    def t_table():
        fs = random.sample(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 10), Fraction(3, 10),
                                   Fraction(7, 10)],
                               [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                                Fraction(7, 10), Fraction(3, 100), Fraction(1, 20)],
                               [Fraction(3, 5), Fraction(3, 20), Fraction(9, 20), Fraction(7, 25), Fraction(13, 50),
                                Fraction(3, 100), Fraction(7, 1000), Fraction(4, 5)]), 4)
        k = random.randrange(4)
        rows = [[_fs(f), _ds(f)] for f in fs]
        return _dt("The table matches fractions to decimals. What decimal belongs in the empty cell?",
                   ["Fraction", "Decimal"], rows, _ds(fs[k]), ["%s = %s." % (_fs(fs[k]), _ds(fs[k]))],
                   missing=[k, 1], atype="num")

    def t_line():
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(3, 10), Fraction(7, 10)],
                     [Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(4, 5), Fraction(1, 2)],
                     [Fraction(3, 5), Fraction(4, 5), Fraction(3, 20), Fraction(7, 20), Fraction(9, 20),
                      Fraction(13, 20)]))
        return _nld("Place %s on the number line marked in tenths." % _fs(f), f, 0, 1, Decimal("0.05"),
                    Decimal("0.1"), ["%s = %s." % (_fs(f), _ds(f))])

    def t_distance():
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(3, 10), Fraction(7, 10)],
                     [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(2, 5), Fraction(3, 10), Fraction(7, 10)],
                     [Fraction(3, 5), Fraction(9, 20), Fraction(7, 25), Fraction(3, 50), Fraction(11, 20),
                      Fraction(7, 1000)]))
        return _tb("A path is %s of a kilometre long. Write that length as a decimal, in km." % _fs(f), _ds(f), "num",
                   {"unit": "km"}, ["%s = %s." % (_fs(f), _ds(f))])

    def t_compare():
        f = pick(_by(d, [Fraction(1, 4), Fraction(3, 4), Fraction(1, 2)],
                     [Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(1, 2)],
                     [Fraction(1, 4), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5), Fraction(7, 20), Fraction(9, 25)]))
        x = _dec(f) + pick(_by(d, [Decimal("0.1"), Decimal("-0.1")],
                               [Decimal("0.05"), Decimal("-0.05"), Decimal("0.1"), Decimal("-0.1")],
                               [Decimal("0.01"), Decimal("-0.01"), Decimal("0.005"), Decimal("-0.005")]))
        return _tb("Which is larger, %s or %s? Type the larger as a decimal." % (_fs(f), _ds(x)), _ds(max(_dec(f), x)),
                   "num", {}, ["%s = %s." % (_fs(f), _ds(f))])

    def t_largest():
        fs = random.sample(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 10), Fraction(3, 10),
                                   Fraction(9, 10)],
                               [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                                Fraction(7, 10), Fraction(3, 100), Fraction(9, 20)],
                               # hard: values bunched between 0.6 and 0.75, so every one must be converted
                               [Fraction(3, 5), Fraction(13, 20), Fraction(16, 25), Fraction(31, 50), Fraction(3, 4),
                                Fraction(7, 10), Fraction(67, 100), Fraction(69, 100)]), 3)
        return _tb("Which is largest: %s? Type it as a decimal." % ", ".join(_fs(f) for f in fs), _ds(max(fs)), "num", {},
                   ["As decimals: %s." % ", ".join(_ds(f) for f in fs)])

    def t_money():
        p = random.randint(1, 9) * 10 if d == 0 else random.randint(*_by(d, (1, 99), (1, 99), (101, 999)))
        return _tb("%d/100 of a pound is how many pounds? Write it as a decimal." % p, _ds(Decimal(p) / 100), "num",
                   {"unit": "£"}, ["%d/100 = %s." % (p, _ds(Decimal(p) / 100))])

    def t_read_grid():
        s = random.randint(1, 9) * 10 if d == 0 else random.randint(1, 99)
        return _area("The square is split into 100 equal parts. Write the shaded part as a decimal.",
                     {"mode": "fraction_read", "parts": 100, "shaded": s, "placeholder": "decimal"},
                     _ds(Decimal(s) / 100), ["%d/100 = %s." % (s, _ds(Decimal(s) / 100))], atype="num")

    def t_thousandths():
        n = random.randint(1, 99) * 10 if d == 0 else random.randint(*_by(d, (1, 999), (1, 999), (1001, 9999)))
        return _tb("Write %d/1000 as a decimal." % n, _ds(Decimal(n) / 1000), "num", {},
                   ["%d ÷ 1000 = %s." % (n, _ds(Decimal(n) / 1000))])

    def t_words():
        den, name = (1000, "thousandth") if d == 2 else (100, "hundredth")
        n = random.randint(*_by(d, (11, 50), (1, 99), (1, 999)))
        word = n_words(n)
        return _tb("Write '%s %s%s' as a decimal." % (word, name, "" if n == 1 else "s"), _ds(Decimal(n) / den), "num",
                   {}, ["%d/%d = %s." % (n, den, _ds(Decimal(n) / den))])

    def t_twentieths():
        den, k = pick(_by(d, [(50, 2), (20, 5)], [(20, 5), (50, 2), (25, 4)], [(20, 5), (25, 4)]))
        n = random.randint(1, den - 1)
        if d == 2 and random.random() < 0.5:           # hard: improper, e.g. 27/20 = 1.35
            n += den
        return _tb("Write %d/%d as a decimal by first making an equivalent fraction out of 100." % (n, den),
                   _ds(Decimal(n * k) / 100), "num", {}, ["× %d: %d/100 = %s." % (k, n * k, _ds(Decimal(n * k) / 100))])

    def t_tenths_in():
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 5), Fraction(2, 5)],
                     [Fraction(1, 2), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5)],
                     [Fraction(3, 5), Fraction(4, 5), Fraction(3, 2), Fraction(6, 5), Fraction(7, 5), Fraction(5, 2)]))
        return _tb("How many tenths are in %s?" % _fs(f), int(f * 10), "int", {},
                   ["%s = %d/10 = %s." % (_fs(f), int(f * 10), _ds(f))])

    return _pick_t([t_power, t_key, t_scale, t_mixed, t_distance, t_compare, t_largest, t_money, t_thousandths,
                    t_words, t_twentieths, t_tenths_in],
                   [t_table, t_line, t_read_grid])


@skill("Y5.6.d", "Round decimals to the nearest whole number and to one decimal place", S6)
def _(d=1):
    d = _d(d)
    x = Decimal(random.randint(0, _by(d, 9, 30, 99))) + Decimal(random.choice([v for v in range(1, 100) if v % 10])) / 100
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
        v = x if x >= 2 else x + 2
        return _tb("%s %s %s. Round this to the nearest whole %s." % (what, _ds(v), unit, unit.rstrip("s")),
                   _ds(_r0(v)), "num", {"unit": unit}, ["%s → %s." % (_ds(v), _ds(_r0(v)))])

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

    def t_table():
        xs = [Decimal(random.randint(0, 30)) + Decimal(random.randint(1, 99)) / 100 for _ in range(3)]
        rows = [[_ds(v), _ds(_r0(v)), format(_r1(v), ".1f")] for v in xs]
        r, c = random.randrange(3), pick([1, 2])
        ans = _r0(xs[r]) if c == 1 else _r1(xs[r])
        return _dt("Complete the rounding table. What belongs in the empty cell?",
                   ["Number", "Nearest whole", "1 decimal place"], rows, _ds(ans),
                   ["%s → %s." % (_ds(xs[r]), _ds(ans))], missing=[r, c], atype="num")

    def t_smallest_to():
        t = Decimal(random.randint(10, 99)) / 10
        return _tb("A number with 2 decimal places rounds to %s to one decimal place. What is the SMALLEST it could be?"
                   % format(t, ".1f"), _ds(t - Decimal("0.05")), "num", {},
                   ["%s rounds up to %s." % (_ds(t - Decimal("0.05")), _ds(t))])

    def t_estimate():
        a = Decimal(random.randint(1, 20)) + Decimal(random.randint(1, 99)) / 100
        b = Decimal(random.randint(1, 20)) + Decimal(random.randint(1, 99)) / 100
        return _tb("Estimate %s + %s by rounding each number to the nearest whole number first." % (_ds(a), _ds(b)),
                   _ds(_r0(a) + _r0(b)), "num", {}, ["%s + %s = %s." % (_ds(_r0(a)), _ds(_r0(b)), _ds(_r0(a) + _r0(b)))])

    def t_check():
        right = random.random() < 0.5
        claimed = _r1(x) if right else _r1(x) + pick([Decimal("0.1"), Decimal("-0.1")])
        if claimed < 0:
            claimed, right = _r1(x), True
        return _wq("%s rounds %s to one decimal place and gets %s. Is that right? (yes or no)"
                   % (_who(), _ds(x), _ds(claimed)), "yes" if right else "no",
                   ["%s → %s." % (_ds(x), _ds(_r1(x)))], "yes / no")

    return _pick_t([t_whole, t_one_dp, t_context, t_which, t_money, t_smallest_to, t_estimate, t_check],
                   [t_line, t_table])


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

    def t_strip():
        return _strip("The bar model shows a whole of %s split into two parts. One part is %s. What is the other part?"
                      % (_ds(a + b), _ds(a)), {"mode": "part_whole", "totalLabel": _ds(a + b), "partLabel": _ds(a),
                                               "unknown": "part", "parts": 2}, _ds(b),
                      ["%s − %s = %s." % (_ds(a + b), _ds(a), _ds(b))], atype="num")

    def t_line():
        s = Decimal(random.randint(10, 80)) / 10
        k = Decimal(random.randint(1, 9)) / 10
        return _nld("Start at %s and add %s. Mark where you land." % (_ds(s), _ds(k)), s + k, int(s), int(s) + 2,
                    Decimal("0.1"), Decimal("0.5"), ["%s + %s = %s." % (_ds(s), _ds(k), _ds(s + k))])

    def t_change():
        cost = Decimal(random.randint(101, 1999)) / 100
        pay = pick([5, 10, 20]) if cost < 5 else pick([10, 20]) if cost < 10 else 20
        return _tb("Something costs £%s. You pay with a £%d note. How much change do you get, in pounds?"
                   % (format(cost, ".2f"), pay), _ds(pay - cost), "num", {"unit": "£"},
                   ["£%d − £%s = £%s." % (pay, format(cost, ".2f"), format(pay - cost, ".2f"))])

    def t_check():
        right = random.random() < 0.5
        s = a + b
        claimed = s if right else s + pick([Decimal("0.1"), Decimal("0.01"), Decimal("1")]) * pick([-1, 1])
        if claimed <= 0:
            claimed, right = s, True
        return _wq("%s says %s + %s = %s. Is that correct? (yes or no)" % (_who(), _ds(a), _ds(b), _ds(claimed)),
                   "yes" if right else "no", ["%s + %s = %s." % (_ds(a), _ds(b), _ds(s))], "yes / no")

    def t_to_one():
        y = Decimal(random.randint(1, 999)) / 1000
        return _tb("What must be added to %s to make 1?" % _ds(y), _ds(1 - y), "num", {},
                   ["1 − %s = %s." % (_ds(y), _ds(1 - y))])

    def t_table():
        xs = [Decimal(random.randint(11, 99)) / 10 for _ in range(3)]
        ys = [Decimal(random.randint(11, 99)) / 100 for _ in range(3)]
        rows = [[_ds(x), _ds(y), _ds(x + y)] for x, y in zip(xs, ys)]
        r = random.randrange(3)
        return _dt("In each row, first + second = total. What is the missing total?", ["First", "Second", "Total"], rows,
                   _ds(xs[r] + ys[r]), ["%s + %s = %s." % (_ds(xs[r]), _ds(ys[r]), _ds(xs[r] + ys[r]))],
                   missing=[r, 2], atype="num")

    def t_basket():
        a, b = Decimal(random.randint(55, 899)) / 100, Decimal(random.randint(55, 899)) / 100
        return _tb("A book costs £%s and a pen costs £%s. How much do they cost together, in pounds?"
                   % (format(a, ".2f"), format(b, ".2f")), _ds(a + b), "num", {"unit": "£"},
                   ["£%s + £%s = £%s." % (format(a, ".2f"), format(b, ".2f"), format(a + b, ".2f"))])

    def t_thousandths_sub():
        x = Decimal(random.randint(1001, 9999)) / 1000
        y = Decimal(random.randint(1, 999)) / 1000
        return _tb("Work out %s − %s." % (_ds(x), _ds(y)), _ds(x - y), "num", {},
                   ["Line up the thousandths.", "= %s." % _ds(x - y)])

    def t_difference():
        x, y = sorted([Decimal(random.randint(101, 999)) / 100, Decimal(random.randint(11, 99)) / 10])
        if x == y:
            y += Decimal("0.1")
        return _tb("What is the difference between %s and %s?" % (_ds(y), _ds(x)), _ds(y - x), "num", {},
                   ["%s − %s = %s." % (_ds(y), _ds(x), _ds(y - x))])

    return _pick_t([t_add, t_sub, t_to_whole, t_missing, t_measure, t_three, t_change, t_check, t_to_one, t_basket,
                    t_thousandths_sub, t_difference],
                   [t_strip, t_line, t_table])


@skill("Y5.6.g", "Problems with decimals to three places", S6)
def _(d=1):
    d = _d(d)

    def t_jumps():
        names = random.sample(["Maya", "Noah", "Sara", "Leo"], 2)
        if d == 0:
            a = Decimal(random.randint(20, 45)) / 10
            b = a + Decimal(random.randint(1, 6)) / 10
        else:
            a = Decimal(random.randint(*_by(d, (200, 450), (200, 450), (150, 400)))) / 100
            b = a + Decimal(random.randint(*_by(d, (1, 60), (1, 60), (55, 150)))) / 100     # hard: crosses a metre
        return _tb("%s jumped %s m and %s jumped %s m. How much further did %s jump, in metres?"
                   % (names[0], _ds(a), names[1], _ds(b), names[1]), _ds(b - a), "num", {"unit": "m"},
                   ["%s − %s = %s." % (_ds(b), _ds(a), _ds(b - a))])

    def t_mass():
        dp = _by(d, 10, 1000, 1000)
        a = Decimal(random.randint(*_by(d, (1, 29), (100, 2999), (1001, 4999)))) / dp
        b = Decimal(random.randint(*_by(d, (1, 29), (100, 2999), (1001, 4999)))) / dp
        return _tb("A bag of apples weighs %s kg and a bag of pears weighs %s kg. What is the total mass, "
                   "in kg?" % (_ds(a), _ds(b)), _ds(a + b), "num", {"unit": "kg"},
                   ["%s + %s = %s." % (_ds(a), _ds(b), _ds(a + b))])

    def t_race():
        t1 = Decimal(random.randint(1100, 1600)) / 100
        diff = Decimal(random.randint(1, 9)) / 10 if d == 0 else \
            Decimal(random.randint(*_by(d, (1, 99), (1, 99), (105, 250)))) / 100
        return _tb("In a 100 m race Noah ran %s seconds. Leo was %s seconds faster. What was Leo's time, in "
                   "seconds?" % (_ds(t1), _ds(diff)), _ds(t1 - diff), "num", {"unit": "seconds"},
                   ["Faster means less time: %s − %s = %s." % (_ds(t1), _ds(diff), _ds(t1 - diff))])

    def t_fill():
        cap = Decimal(random.randint(_by(d, 2, 2, 3), 5))
        dp = _by(d, 10, 1000, 1000)
        a = Decimal(random.randint(*_by(d, (1, 9), (100, 900), (1050, 1950)))) / dp
        b = Decimal(random.randint(*_by(d, (1, 9), (100, 900), (105, 950)))) / dp
        if a + b >= cap:
            b = Decimal("0.25")
        return _tb("A %s litre jug has %s litres in it. %s litres are added. How much more is needed to "
                   "fill it, in litres?" % (_ds(cap), _ds(a), _ds(b)), _ds(cap - a - b), "num",
                   {"unit": "litres"}, ["%s + %s = %s." % (_ds(a), _ds(b), _ds(a + b)),
                                        "%s − %s = %s." % (_ds(cap), _ds(a + b), _ds(cap - a - b))])

    def t_table():
        names = ["Mon", "Tue", "Wed"]
        vals = [Decimal(random.randint(*_by(d, (10, 50), (10, 99), (1005, 2995)))) / _by(d, 10, 10, 100) for _ in names]
        rows = [[n, "%s km" % _ds(v)] for n, v in zip(names, vals)]
        return _dt("The table shows how far %s cycled each day. What is the total distance, in km?" % _who(),
                   ["Day", "Distance"], rows, _ds(sum(vals)),
                   ["%s = %s." % (" + ".join(_ds(v) for v in vals), _ds(sum(vals)))], atype="num")

    def t_rain():
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        vals = [Decimal(random.randint(0, 6)) / 2 for _ in days]
        if max(vals) < 2:
            vals[random.randrange(5)] = Decimal("2.5")
        i, j = random.sample(range(5), 2)
        if d == 2:                                     # hard: three days and a difference to finish
            k = random.choice([x for x in range(5) if x not in (i, j)])
            tot = vals[i] + vals[j] + vals[k]
            return _lg("The graph shows rainfall each day, in cm. How much less than 10 cm fell on %s, %s and %s "
                       "altogether, in cm?" % (days[i], days[j], days[k]), [(dd, float(v)) for dd, v in zip(days, vals)],
                       _ds(10 - tot), ["%s + %s + %s = %s." % (_ds(vals[i]), _ds(vals[j]), _ds(vals[k]), _ds(tot)),
                                       "10 − %s = %s." % (_ds(tot), _ds(10 - tot))], "cm", "Day", atype="num")
        return _lg("The graph shows rainfall each day, in cm. How much rain fell on %s and %s altogether, in cm?"
                   % (days[i], days[j]), [(dd, float(v)) for dd, v in zip(days, vals)], _ds(vals[i] + vals[j]),
                   ["%s + %s = %s." % (_ds(vals[i]), _ds(vals[j]), _ds(vals[i] + vals[j]))], "cm", "Day", atype="num")

    def t_relay():
        # easy: tenths; medium: hundredths; hard: thousandths (electronic timing)
        ts = [Decimal(random.randint(*_by(d, (115, 159), (1150, 1590), (11500, 15900)))) / _by(d, 10, 100, 1000)
              for _ in range(4)]
        return _tb("Four runners in a relay take %s seconds. What is the team's total time, in seconds?"
                   % ", ".join(_ds(t) for t in ts), _ds(sum(ts)), "num", {"unit": "seconds"},
                   ["%s = %s." % (" + ".join(_ds(t) for t in ts), _ds(sum(ts)))])

    def t_heights():
        a = Decimal(random.randint(*_by(d, (12, 17), (120, 175), (120, 175)))) / _by(d, 10, 100, 100)
        k = Decimal(random.randint(*_by(d, (1, 4), (5, 40), (5, 40)))) / _by(d, 10, 100, 100)
        who = _who()
        if d == 2:                                     # hard: the gap is given in cm
            return _tb("%s is %s m tall. %s's brother is %d cm shorter. How tall is the brother, in metres?"
                       % (who, _ds(a), who, int(k * 100)), _ds(a - k), "num", {"unit": "m"},
                       ["%d cm = %s m." % (int(k * 100), _ds(k)), "%s − %s = %s." % (_ds(a), _ds(k), _ds(a - k))])
        return _tb("%s is %s m tall. %s's brother is %s m shorter. How tall is the brother, in metres?"
                   % (who, _ds(a), who, _ds(k)), _ds(a - k), "num", {"unit": "m"},
                   ["%s − %s = %s." % (_ds(a), _ds(k), _ds(a - k))])

    def t_parcel():
        a = Decimal(random.randint(*_by(d, (2, 5), (1100, 4900), (2100, 4900)))) / _by(d, 1, 1000, 1000)
        g = random.randint(*_by(d, (1, 9), (105, 950), (1050, 1950))) * _by(d, 100, 1, 1)
        return _tb("A box weighs %s kg. A book weighing %s g is taken out. How heavy is the box now, in kg?" % (_ds(a), _c(g)),
                   _ds(a - Decimal(g) / 1000), "num", {"unit": "kg"},
                   ["%s g = %s kg." % (_c(g), _ds(Decimal(g) / 1000)), "%s − %s = %s." % (_ds(a), _ds(Decimal(g) / 1000),
                                                                                     _ds(a - Decimal(g) / 1000))])

    def t_bar():
        names = ["Ana", "Ben", "Cal", "Dev"]
        vals = [Decimal(random.randint(*_by(d, (15, 45), (150, 450), (150, 450)))) / _by(d, 10, 100, 100) for _ in names]
        return _bar("The chart shows how far each child jumped, in metres. What is the difference between the longest "
                    "and the shortest jump, in metres?", names, [float(v) for v in vals], _ds(max(vals) - min(vals)),
                    ["%s − %s = %s." % (_ds(max(vals)), _ds(min(vals)), _ds(max(vals) - min(vals)))], atype="num")

    return _pick_t([t_jumps, t_mass, t_race, t_fill, t_relay, t_heights, t_parcel], [t_table, t_rain, t_bar])


@skill("Y5.6.h", "Per cent as parts per hundred", S6)
def _(d=1):
    d = _d(d)
    # easy: whole tens; medium: any 1-99; hard: single-digit per cents (7% = 0.07, not 0.7) and awkward values
    p = random.randint(1, 9) * 10 if d == 0 else random.randint(1, 99)
    if d == 2 and (p % 10 == 0 or random.random() < 0.4):
        p = random.randint(1, 9)

    def t_to_fraction():
        return _tb("Complete:  %d%% = ___/100" % p, p, "int", {}, ["Per cent means out of 100."])

    def t_to_decimal():
        return _tb("Write %d%% as a decimal." % p, _ds(Decimal(p) / 100), "num", {},
                   ["%d%% = %d/100 = %s." % (p, p, _ds(Decimal(p) / 100))])

    def t_from_decimal():
        return _tb("Write %s as a percentage. Give the number only." % _ds(Decimal(p) / 100), p, "int", {},
                   ["%s = %d/100 = %d%%." % (_ds(Decimal(p) / 100), p, p)])

    def t_rest():
        if d == 2 and p < 80:                          # hard: two groups to take away
            q = random.randint(1, 99 - p)
            return _tb("%d%% of a class have school dinners and %d%% bring a packed lunch. The rest go home for lunch. "
                       "What percentage go home? Give the number only." % (p, q), 100 - p - q, "int", {},
                       ["%d + %d = %d." % (p, q, p + q), "100 − %d = %d." % (p + q, 100 - p - q)])
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
        ps = random.sample(_by(d, range(10, 91, 10), range(1, 99), range(1, 99)), 3)
        if d == 2:
            ps[0] = random.randint(1, 9)
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

    def t_compare():
        x = Decimal(random.randint(1, 9)) / 10
        if d == 2 and p < 10:                          # hard: the 7% versus 0.7 trap
            x = Decimal(p) / 10
        if p == int(x * 100):
            return t_to_decimal()
        return _tb("Which is more, %d%% or %s? Type the larger as a decimal." % (p, _ds(x)),
                   _ds(max(Decimal(p) / 100, x)), "num", {}, ["%d%% = %s." % (p, _ds(Decimal(p) / 100))])

    def t_tiles():
        colour = pick(["red", "blue", "green"])
        return _tb("A wall has 100 tiles. %d of them are %s. What percentage of the tiles are %s? Give the number only."
                   % (p, colour, colour), p, "int", {}, ["%d out of 100 = %d%%." % (p, p)])

    def t_tenths():
        if d == 2:                                     # hard: twentieths, e.g. 35% = 7/20
            t = random.choice([x for x in range(1, 20) if x % 2])
            return _tb("Complete:  %d%% = ___/20" % (t * 5), t, "int", {},
                       ["%d%% = %d/100 = %d/20." % (t * 5, t * 5, t)])
        t = random.randint(1, 9)
        return _tb("Complete:  %d%% = ___/10" % (t * 10), t, "int", {}, ["%d%% = %d/100 = %d/10." % (t * 10, t * 10, t)])

    def t_largest():
        lo, hi = _by(d, (10, 90), (30, 70), (45, 55))     # the closer the values, the harder
        a_ = Decimal(random.randint(lo, hi)) / 100
        b_ = random.randint(lo, hi)
        c_ = random.randint(lo, hi)
        vals = {"%s" % _ds(a_): a_, "%d%%" % b_: Decimal(b_) / 100, "%d/100" % c_: Decimal(c_) / 100}
        if len(set(vals.values())) < 3:
            return t_rest()
        best = max(vals.values())
        return _tb("Which is the largest: %s? Type it as a decimal." % ", ".join(vals), _ds(best), "num", {},
                   ["As decimals: %s." % ", ".join(_ds(v) for v in vals.values())])

    def t_bar():
        if p > 90 or p < 10:
            return t_grid()
        return {"prompt": "The bar is split into 10 equal parts. Shade %d%% of it." % (p // 10 * 10),
                "component": "fraction_bar", "spec": {"parts": 10, "mode": "shade"},
                "answer": "%d/10" % (p // 10), "answer_type": "frac",
                "solution": ["%d%% = %d/100 = %d/10." % (p // 10 * 10, p // 10 * 10, p // 10)]}

    return _pick_t([t_to_fraction, t_to_decimal, t_from_decimal, t_rest, t_compare, t_tiles, t_tenths, t_largest],
                   [t_grid, t_read_grid, t_table, t_bar])


@skill("Y5.6.i", "Percentage equivalents of halves, quarters, fifths, tenths and 25ths", S6)
def _(d=1):
    d = _d(d)
    if d == 0:
        f = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(random.randint(1, 9), 10)])
    elif d == 1:
        f = pick([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5),
                  Fraction(4, 5), Fraction(random.randint(1, 9), 10), Fraction(random.randint(1, 24), 25),
                  Fraction(random.randint(1, 49), 50)])
    else:                                              # hard: mostly 25ths and 50ths
        f = pick([Fraction(3, 5), Fraction(4, 5), Fraction(random.randint(1, 24), 25),
                  Fraction(random.randint(1, 49), 50)])
    pc = int(f * 100)

    def t_to_pc():
        return _tb("Write %s as a percentage. Give the number only." % _fs(f), pc, "int", {},
                   ["%s = %d/100 = %d%%." % (_fs(f), pc, pc)])

    def t_from_pc():
        return _wq("Write %d%% as a fraction in its simplest form." % pc, _fs(f),
                   ["%d%% = %d/100 = %s." % (pc, pc, _fs(f))], "e.g. 1/4")

    def t_compare():
        g = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)],
                     [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(4, 5)],
                     [Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(7, 20)]))
        q = random.randint(1, 9) * 10 if d == 0 else random.randint(1, 99)
        if d == 2:                                     # hard: the per cent is within a few of the fraction
            q = int(g * 100) + pick([-4, -3, -2, -1, 1, 2, 3, 4])
        if g * 100 == q:
            q += 1
        return _tb("Which is greater, %s or %d%%? Give the greater one as a percentage (number only)." % (_fs(g), q),
                   max(int(g * 100), q), "int", {}, ["%s = %d%%." % (_fs(g), int(g * 100))])

    def t_score():
        den = pick(_by(d, [10, 20], [10, 20, 25, 50], [25, 50]))
        sc = random.randint(1, den)
        return _tb("%s scored %d out of %d in a test. What percentage is that? Give the number only."
                   % (_who(), sc, den), sc * 100 // den, "int", {},
                   ["%d/%d = %d/100 = %d%%." % (sc, den, sc * 100 // den, sc * 100 // den)])

    def t_pie():
        a = pick(_by(d, [50, 25], [50, 25, 20, 10], [50, 25, 20, 10]))
        rest = 100 - a
        b = rest // 2
        slices = [["Football", a], ["Swimming", b], ["Tennis", rest - b]]
        return {"prompt": "The pie chart shows favourite sports. What percentage chose Football? Give the "
                          "number only.", "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": a, "answer_type": "int",
                "solution": ["Football is %s of the circle: %d%%." % (_fs(Fraction(a, 100)), a)]}

    def t_decimal():
        return _tb("Write %s as a percentage. Give the number only." % _ds(f), pc, "int", {},
                   ["%s = %s = %d%%." % (_ds(f), _fs(f), pc)])

    def t_order():
        fs = random.sample(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 10), Fraction(9, 10)],
                               [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                                Fraction(3, 5), Fraction(4, 5), Fraction(7, 10), Fraction(3, 10)],
                               # hard: all between 30% and 50%, with 25ths and 50ths
                               [Fraction(2, 5), Fraction(9, 25), Fraction(11, 25), Fraction(17, 50), Fraction(23, 50),
                                Fraction(7, 20), Fraction(9, 20), Fraction(3, 10)]), 3)
        q = random.choice([x for x in _by(d, range(10, 91, 10), range(5, 96), range(31, 50))
                           if Fraction(x, 100) not in fs])
        vals = fs + [Fraction(q, 100)]
        shown = [_fs(v) for v in fs] + ["%d%%" % q]
        return _tb("Which is the smallest: %s? Give its value as a percentage (number only)." % ", ".join(shown),
                   int(min(vals) * 100), "int", {}, ["As percentages: %s." % ", ".join("%d%%" % int(v * 100) for v in vals)])

    def t_table():
        fs = random.sample(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 10), Fraction(3, 10),
                                   Fraction(7, 10)],
                               [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
                                Fraction(3, 10), Fraction(7, 25), Fraction(9, 50)],
                               [Fraction(3, 5), Fraction(7, 25), Fraction(9, 50), Fraction(13, 20), Fraction(17, 25),
                                Fraction(3, 20), Fraction(11, 50)]), 3)
        rows = [[_fs(v), _ds(v), "%d%%" % int(v * 100)] for v in fs]
        r = random.randrange(3)
        rows[r][2] = ""
        return _dt("Complete the table. What percentage belongs in the empty cell? Give the number only.",
                   ["Fraction", "Decimal", "Per cent"], rows, int(fs[r] * 100),
                   ["%s = %s = %d%%." % (_fs(fs[r]), _ds(fs[r]), int(fs[r] * 100))], missing=[r, 2])

    def t_bar():
        k = random.randint(1, 4)
        return {"prompt": "The bar is split into 5 equal parts. Shade %d%% of it." % (k * 20),
                "component": "fraction_bar", "spec": {"parts": 5, "mode": "shade"},
                "answer": "%d/5" % k, "answer_type": "frac", "solution": ["%d%% = %d/5." % (k * 20, k)]}

    def t_class():
        den = pick(_by(d, [10, 20], [20, 25, 50], [25, 50]))
        k = random.randint(1, den - 1)
        return _tb("In a club of %d children, %d play the piano. What percentage play the piano? Give the number only."
                   % (den, k), k * 100 // den, "int", {}, ["%d/%d = %d/100 = %d%%." % (k, den, k * 100 // den, k * 100 // den)])

    def t_word_fraction():
        pc_ = pick(_by(d, [10, 25, 50, 75], [10, 20, 25, 40, 50, 60, 75, 80], [4, 12, 15, 35, 44, 64, 85]))
        return _wq("%d%% of the children in a choir are boys. What fraction of the choir are boys? Give it in its simplest "
                   "form." % pc_, _fs(Fraction(pc_, 100)), ["%d%% = %d/100 = %s." % (pc_, pc_, _fs(Fraction(pc_, 100)))],
                   "e.g. 2/5")

    def t_25ths():
        if d == 2:                                     # hard: fiftieths
            k = random.randint(1, 49)
            return _tb("Write %d/50 as a percentage. Give the number only." % k, 2 * k, "int", {},
                       ["× 2: %d/100 = %d%%." % (2 * k, 2 * k)])
        k = random.randint(1, _by(d, 10, 24, 24))
        return _tb("Write %d/25 as a percentage. Give the number only." % k, 4 * k, "int", {},
                   ["× 4: %d/100 = %d%%." % (4 * k, 4 * k)])

    def t_rest_fraction():
        f2 = pick(_by(d, [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(3, 10)],
                      [Fraction(1, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 10), Fraction(1, 2)],
                      [Fraction(3, 5), Fraction(7, 20), Fraction(9, 25), Fraction(13, 50), Fraction(4, 5)]))
        return _tb("%s of a garden is grass. What percentage is NOT grass? Give the number only." % _fs(f2),
                   100 - int(f2 * 100), "int", {}, ["%s = %d%%." % (_fs(f2), int(f2 * 100)),
                                                    "100 − %d = %d." % (int(f2 * 100), 100 - int(f2 * 100))])

    return _pick_t([t_to_pc, t_from_pc, t_compare, t_score, t_decimal, t_order, t_class, t_word_fraction, t_25ths,
                    t_rest_fraction], [t_pie, t_table, t_bar])


@skill("Y5.6.j", "Percentage problems", S6)
def _(d=1):
    d = _d(d)

    def t_simple_of():
        if d == 2:                                     # hard: a non-unit fraction, e.g. 75% = 3/4
            pc, den, num = pick([(75, 4, 3), (40, 5, 2), (60, 5, 3), (30, 10, 3), (80, 5, 4)])
            amt = den * random.randint(3, 30)
            return _tb("What is %d%% of %d?" % (pc, amt), amt * pc // 100, "int", {},
                       ["%d%% = %d/%d." % (pc, num, den), "%d ÷ %d × %d = %d." % (amt, den, num, amt * pc // 100)])
        p, x = pick(_by(d, [(50, 2), (10, 10)], [(50, 2), (25, 4), (10, 10), (20, 5)], [])), \
            random.randint(2, _by(d, 10, 20, 20))
        amt = p[1] * x * (pick([1, 10]) if d else 1)
        return _tb("What is %d%% of %d?" % (p[0], amt), amt * p[0] // 100, "int", {},
                   ["%d%% = 1/%d." % (p[0], p[1]), "%d ÷ %d = %d." % (amt, p[1], amt * p[0] // 100)])

    def t_sale():
        p = pick(_by(d, [10, 50], [10, 20, 25, 50], [20, 25, 40, 75]))
        price = random.randint(2, _by(d, 10, 20, 30)) * (100 // _gcd(p, 100))      # the saving is a whole number of pounds
        off = price * p // 100
        return _tb("A game costs £%d. There is %d%% off. How much do you save, in pounds?" % (price, p), off,
                   "int", {"unit": "£"}, ["%d%% of %d = %d." % (p, price, off)])

    def t_left():
        n = pick(_by(d, [20, 40, 100], [20, 40, 50, 100, 200], [40, 80, 120, 160, 300]))
        p = pick(_by(d, [10, 50], [10, 20, 25, 50, 75], [20, 25, 40, 60, 75]))
        if n * p % 100:
            n = 100
        return _tb("A farmer has %d sheep. %d%% are in the top field. How many are NOT in the top field?"
                   % (n, p), n - n * p // 100, "int", {},
                   ["%d%% of %d = %d." % (p, n, n * p // 100), "%d − %d = %d." % (n, n * p // 100, n - n * p // 100)])

    def t_compare_scores():
        a_t, b_t = _by(d, (10, 20), (20, 25), (25, 50))
        a_s = random.randint(a_t // 2, a_t)
        b_s = random.randint(_by(d, 5, 10, 25), b_t)
        pa, pb = a_s * 100 // a_t, b_s * 100 // b_t
        if pa == pb:
            b_s -= 1
            pb = b_s * 100 // b_t
        return _wq("Maya scored %d out of %d. Noah scored %d out of %d. Who did better? (compare the "
                   "percentages)" % (a_s, a_t, b_s, b_t), "Maya" if pa > pb else "Noah",
                   ["Maya: %d%%. Noah: %d%%." % (pa, pb)], "name")

    def t_grid():
        s = random.randint(1, 9) * 10 if d == 0 else random.randint(5, 95)
        return _area("Some of this 100-square is shaded. What percentage is NOT shaded? Give the number only.",
                     {"mode": "fraction_read", "parts": 100, "shaded": s, "placeholder": "number"}, 100 - s,
                     ["%d%% is shaded, so %d%% is not." % (s, 100 - s)])

    def t_class():
        n = pick([20, 24, 28, 32, 36, 40])
        p = pick(_by(d, [25, 50], [25, 50, 75], [20, 40, 60, 75]))
        if p % 25:                                     # hard: fifths need a class size that is a multiple of 5
            n = pick([25, 30, 35, 40])
        return _tb("There are %d pupils in a class. %d%% of them walk to school. How many pupils walk?" % (n, p),
                   n * p // 100, "int", {"unit": "pupils"}, ["%d%% = %s." % (p, _fs(Fraction(p, 100))),
                                                            "%s of %d = %d." % (_fs(Fraction(p, 100)), n, n * p // 100)])

    def t_sale_price():
        p = pick(_by(d, [10, 50], [10, 20, 25, 50], [20, 25, 40, 75]))
        price = random.randint(2, _by(d, 10, 20, 30)) * (100 // _gcd(p, 100))
        return _tb("A coat costs £%d. In a sale there is %d%% off. What is the sale price, in pounds?" % (price, p),
                   price - price * p // 100, "int", {"unit": "£"},
                   ["%d%% of %d = %d." % (p, price, price * p // 100), "%d − %d = %d." % (price, price * p // 100,
                                                                                       price - price * p // 100)])

    def t_which_more():
        a_p, b_p = (pick(_by(d, [10, 50], [10, 20, 25, 50], [20, 25, 40, 75])) for _ in range(2))
        x = 100 // _gcd(a_p, 100) * random.randint(2, 12)
        y = 100 // _gcd(b_p, 100) * random.randint(2, 12)
        va, vb = x * a_p // 100, y * b_p // 100
        if va == vb:
            return t_simple_of()
        return _tb("Which is more: %d%% of %d or %d%% of %d? Type its value." % (a_p, x, b_p, y), max(va, vb), "int", {},
                   ["%d%% of %d = %d; %d%% of %d = %d." % (a_p, x, va, b_p, y, vb)])

    def t_table():
        items = [("Book", random.randint(2, 20) * 10), ("Bag", random.randint(2, 20) * 10),
                 ("Lamp", random.randint(2, 20) * 10)]
        p = pick(_by(d, [10, 50], [10, 20, 50], [20, 30, 40]))
        k = random.randrange(3)
        return _dt("Everything in the shop has %d%% off. How much do you save on the %s, in pounds?"
                   % (p, items[k][0].lower()), ["Item", "Price"], [[n, "£%d" % v] for n, v in items],
                   items[k][1] * p // 100, ["%d%% of £%d = £%d." % (p, items[k][1], items[k][1] * p // 100)])

    def t_pie():
        a = pick([10, 20, 25, 30, 40])
        b = pick([x for x in (10, 15, 20, 25, 30) if a + x < 100])
        c = 100 - a - b
        slices = [["Walk", a], ["Car", b], ["Bus", c]]
        total = pick(_by(d, [100], [20, 40, 60, 80, 100, 200], [200, 300, 400, 500, 600]))
        while total * c % 100:
            total += 20
        return {"prompt": "The pie chart shows how %d pupils travel to school. %d%% walk and %d%% come by car. How many "
                          "pupils come by bus?" % (total, a, b), "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": 2}, "answer": total * c // 100,
                "answer_type": "int", "solution": ["Bus: 100 − %d − %d = %d%%." % (a, b, c),
                                                   "%d%% of %d = %d." % (c, total, total * c // 100)]}

    return _pick_t([t_simple_of, t_sale, t_left, t_compare_scores, t_class, t_sale_price, t_which_more],
                   [t_grid, t_table, t_pie])


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
        bigger = big if x * f > y else small
        return _wq("Which is more: %d %s or %d %s? Type the unit of the larger amount (%s or %s)."
                   % (x, big, y, small, big, small), bigger,
                   ["%d %s = %d %s." % (x, big, x * f, small)], "%s or %s" % (big, small))

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
        # easy: even numbers (whole answers); hard: bigger, odd numbers
        n = random.randint(1, 5) * 2 if d == 0 else random.randint(*_by(d, (2, 12), (2, 12), (13, 39)))
        if d == 2 and n % 2 == 0:
            n += 1
        return _tb("1 inch is about 2.5 cm. About how many centimetres is %d inches?" % n,
                   _ds(Decimal(n) * Decimal("2.5")), "num", {"unit": "cm"},
                   ["%d × 2.5 = %s." % (n, _ds(Decimal(n) * Decimal("2.5")))], tol=0.01)

    def t_pounds():
        n = random.randint(1, 4) * 5 if d == 0 else random.randint(2, 20)
        if d == 2:                                     # hard: the inverse, pounds back to kg
            return _tb("1 kg is about 2.2 pounds. About how many kg is %s pounds?" % _ds(Decimal(n) * Decimal("2.2")),
                       n, "int", {"unit": "kg"},
                       ["%s ÷ 2.2 = %d." % (_ds(Decimal(n) * Decimal("2.2")), n)])
        return _tb("1 kg is about 2.2 pounds. About how many pounds is %d kg?" % n,
                   _ds(Decimal(n) * Decimal("2.2")), "num", {"unit": "pounds"},
                   ["%d × 2.2 = %s." % (n, _ds(Decimal(n) * Decimal("2.2")))])

    def t_pints():
        n = random.randint(1, 3) * 4 if d == 0 else random.randint(*_by(d, (2, 12), (2, 12), (13, 30)))
        return _tb("1 litre is about 1.75 pints. About how many pints is %d litres?" % n,
                   _ds(Decimal(n) * Decimal("1.75")), "num", {"unit": "pints"},
                   ["%d × 1.75 = %s." % (n, _ds(Decimal(n) * Decimal("1.75")))])

    def t_feet():
        n = random.randint(2, _by(d, 5, 10, 10))
        if d == 2:                                     # hard: feet and inches
            i = random.randint(1, 11)
            return _tb("1 foot is 12 inches. How many inches are in %d feet %d inch%s?" % (n, i, "" if i == 1 else "es"),
                       12 * n + i, "int", {"unit": "inches"}, ["%d × 12 + %d = %d." % (n, i, 12 * n + i)])
        return _tb("1 foot is 12 inches. How many inches are in %d feet?" % n, 12 * n, "int",
                   {"unit": "inches"}, ["%d × 12 = %d." % (n, 12 * n)])

    def t_miles():
        n = 5 * random.randint(1, _by(d, 4, 12, 20))
        if d == 2:                                     # hard: the inverse, km back to miles
            return _tb("5 miles is about 8 km. About how many miles is %d km?" % (n // 5 * 8), n, "int",
                       {"unit": "miles"}, ["%d ÷ 8 = %s of 8 km." % (n // 5 * 8, _pl(n // 5, "lot")),
                                           "%d × 5 = %d." % (n // 5, n)])
        return _tb("5 miles is about 8 km. About how many km is %d miles?" % n, n // 5 * 8, "int",
                   {"unit": "km"}, ["%d ÷ 5 = %s of 5 miles." % (n, _pl(n // 5, "lot")), "%d × 8 = %d." % (n // 5, n // 5 * 8)])

    def t_back():
        n = random.randint(2, _by(d, 4, 10, 10))
        if d == 2:                                     # hard: answer in kg, a decimal
            return _tb("1 pound is about 450 g. About how many kilograms is %d pounds?" % n,
                       _ds(Decimal(450 * n) / 1000), "num", {"unit": "kg"},
                       ["%d × 450 = %d g." % (n, 450 * n), "= %s kg." % _ds(Decimal(450 * n) / 1000)])
        return _tb("1 pound is about 450 g. About how many grams is %d pounds?" % n, 450 * n, "int",
                   {"unit": "g"}, ["%d × 450 = %d." % (n, 450 * n)])

    def t_sensible():
        q, a = pick([("How tall is a door, in feet: about 7, 70 or 700?", 7),
                     ("How much milk is in a big carton, in pints: about 4, 40 or 400?", 4),
                     ("How heavy is a bag of sugar, in pounds: about 2, 20 or 200?", 2),
                     ("How long is a pencil, in inches: about 7, 70 or 700?", 7)])
        return _tb(q, a, "int", {}, ["Use what you know about everyday objects."])

    def t_table():
        rows = [[i, _ds(Decimal(i) * Decimal("2.5"))] for i in _by(d, (2, 4, 6, 8, 10), (1, 2, 4, 6, 10), (1, 3, 7, 9, 15))]
        k = random.randint(1, 4)
        return _dt("This table converts inches to centimetres (1 inch ≈ 2.5 cm). What belongs in the empty "
                   "cell?", ["Inches", "Centimetres"], rows, rows[k][1],
                   ["%d × 2.5 = %s." % (rows[k][0], rows[k][1])], missing=[k, 1], atype="num")

    def t_longer():
        f = random.randint(*_by(d, (1, 4), (1, 4), (3, 8)))
        cm = f * 30 + pick(_by(d, [-15, 15], [-12, -8, 8, 12], [-5, -3, 3, 5]))
        unit = "foot" if f == 1 else "feet"
        return _wq("Which is longer, %d %s or %d cm? (1 foot is about 30 cm.) Type %s or cm." % (f, unit, cm, unit),
                   unit if f * 30 > cm else "cm",
                   ["%d × 30 = %d cm." % (f, f * 30)], "%s or cm" % unit)

    def t_stone():
        st = random.randint(*_by(d, (2, 5), (5, 12), (5, 12)))
        if d == 2:                                     # hard: stones and pounds
            lb = random.randint(1, 13)
            return _tb("1 stone is 14 pounds. How many pounds is %d stone %d pound%s?" % (st, lb, "" if lb == 1 else "s"),
                       14 * st + lb, "int", {"unit": "pounds"}, ["%d × 14 + %d = %d." % (st, lb, 14 * st + lb)])
        return _tb("1 stone is 14 pounds. How many pounds is %d stone?" % st, 14 * st, "int", {"unit": "pounds"},
                   ["%d × 14 = %d." % (st, 14 * st)])

    def t_yards():
        y = random.randint(2, _by(d, 10, 20, 12))
        if d == 2:                                     # hard: two steps, yards to feet to inches
            return _tb("1 yard is 3 feet and 1 foot is 12 inches. How many inches are in %d yards?" % y, 36 * y, "int",
                       {"unit": "inches"}, ["%d × 3 = %d feet." % (y, 3 * y), "%d × 12 = %d." % (3 * y, 36 * y)])
        return _tb("1 yard is 3 feet. How many feet are in %d yards?" % y, 3 * y, "int", {"unit": "feet"},
                   ["%d × 3 = %d." % (y, 3 * y)])

    return _pick_t([t_inches, t_pounds, t_pints, t_feet, t_miles, t_back, t_sensible, t_longer, t_stone, t_yards],
                   [t_table])


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
        return _tb("An L-shaped garden is made by cutting a rectangle %d m by %d m out of one corner of a rectangle "
                   "%d m by %d m. What is the perimeter of the garden, in m?" % (cw, ch, W, H),
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

    def t_fence():
        a, b = random.randint(4, 20), random.randint(4, 20)
        cost = random.randint(3, 12)
        return _tb("A rectangular field is %d m by %d m. Fencing costs £%d a metre. How much does it cost to fence all the "
                   "way round, in pounds?" % (a, b, cost), 2 * (a + b) * cost, "int", {"unit": "£"},
                   ["Perimeter: 2 × (%d + %d) = %d m." % (a, b, 2 * (a + b)), "%d × %d = %d." % (2 * (a + b), cost,
                                                                                               2 * (a + b) * cost)])

    def t_rect_grid():
        w, h = random.randint(2, 8), random.randint(2, 6)
        cells = [[r, c] for r in range(h) for c in range(w)]
        return _area("Each square is 1 cm long. What is the perimeter of this rectangle, in cm?",
                     {"mode": "read_perimeter", "cells": cells, "rows": h, "cols": w}, 2 * (w + h),
                     ["2 × (%d + %d) = %d cm." % (w, h, 2 * (w + h))])

    def t_table():
        dims = [(random.randint(3, 20), random.randint(3, 20)) for _ in range(3)]
        rows = [["%d cm" % a, "%d cm" % b, "%d cm" % (2 * (a + b))] for a, b in dims]
        r = random.randrange(3)
        c = pick([1, 2])
        ans = dims[r][1] if c == 1 else 2 * sum(dims[r])
        rows[r][c] = ""
        return _dt("The table gives the length, width and perimeter of three rectangles. What number belongs in the empty "
                   "cell, in cm?", ["Length", "Width", "Perimeter"], rows, ans,
                   ["Perimeter = 2 × (length + width)." if c == 2 else
                    "Half the perimeter is %d; %d − %d = %d." % (sum(dims[r]), sum(dims[r]), dims[r][0], ans)],
                   missing=[r, c])

    def t_which_longer():
        a, b, c, e = [random.randint(3, 15) for _ in range(4)]
        if a + b == c + e:
            e += 1
        return _wq("Rectangle A is %d cm by %d cm. Rectangle B is %d cm by %d cm. Which has the longer perimeter? (A or B)"
                   % (a, b, c, e), "A" if a + b > c + e else "B",
                   ["A: %d cm. B: %d cm." % (2 * (a + b), 2 * (c + e))], "A or B")

    def t_regular_mix():
        name, n = pick([("pentagon", 5), ("hexagon", 6), ("octagon", 8)])
        s = random.randint(3, 12)
        return _tb("A garden is a square of side %d m joined to a regular %s of side %d m along one edge. What is the "
                   "perimeter of the whole garden, in m?" % (s, name, s), (4 - 1) * s + (n - 1) * s, "int", {"unit": "m"},
                   ["The shared edge is inside, so it does not count.", "%d + %d = %d sides of %d m: %d m." % (
                       3, n - 1, 3 + n - 1, s, (3 + n - 1) * s)])

    return _pick_t([t_l_words, t_missing_side, t_rect, t_inverse, t_metres, t_fence, t_which_longer, t_regular_mix],
                   [t_grid, t_rect_grid, t_table])


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
        return _tb("An L-shaped room is a rectangle %d m by %d m with a corner %d m by %d m missing. What is "
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

    def t_carpet():
        a, b, cost = random.randint(2, 9), random.randint(2, 9), random.randint(5, 25)
        return _tb("A room is %d m by %d m. Carpet costs £%d for each m². How much does it cost to carpet the room, in "
                   "pounds?" % (a, b, cost), a * b * cost, "int", {"unit": "£"},
                   ["Area: %d × %d = %d m²." % (a, b, a * b), "%d × %d = %d." % (a * b, cost, a * b * cost)])

    def t_table():
        dims = [(random.randint(2, 15), random.randint(2, 15)) for _ in range(3)]
        rows = [["%d cm" % a, "%d cm" % b, "%d cm²" % (a * b)] for a, b in dims]
        r, c = random.randrange(3), pick([1, 2])
        ans = dims[r][1] if c == 1 else dims[r][0] * dims[r][1]
        rows[r][c] = ""
        return _dt("The table gives the length, width and area of three rectangles. What number belongs in the empty cell?",
                   ["Length", "Width", "Area"], rows, ans,
                   ["Area = length × width." if c == 2 else "%d ÷ %d = %d." % (dims[r][0] * dims[r][1], dims[r][0], ans)],
                   missing=[r, c])

    def t_two_rooms():
        a, b, c, e = [random.randint(2, 8) for _ in range(4)]
        return _tb("A flat has two rectangular rooms: one %d m by %d m and one %d m by %d m. What is the total floor area, "
                   "in m²?" % (a, b, c, e), a * b + c * e, "int", {"unit": "m²"},
                   ["%d + %d = %d." % (a * b, c * e, a * b + c * e)])

    def t_unit():
        what, ans = pick([("a football pitch", "m"), ("a postage stamp", "cm"), ("a classroom floor", "m"),
                          ("a playing card", "cm"), ("a garden", "m"), ("a page of a book", "cm")])
        return _wq("Would you measure the area of %s in square centimetres (cm²) or square metres (m²)? Type cm or m."
                   % what, ans, ["Small things use cm²; large things use m²."], "cm or m")

    return _pick_t([t_rect, t_side, t_square, t_l_words, t_compare, t_same_perimeter, t_carpet, t_two_rooms, t_unit],
                   [t_compound, t_build, t_table])


@skill("Y5.7.e", "Estimate the area of irregular shapes", S7)
def _(d=1):
    d = _d(d)

    def t_count():
        whole, half = random.randint(*_by(d, (4, 15), (6, 30), (20, 60))), 2 * random.randint(*_by(d, (1, 3), (1, 8), (5, 15)))
        return _tb("A leaf drawn on a 1 cm grid covers %d whole squares and %d half squares. Estimate its "
                   "area, in cm²." % (whole, half), whole + half // 2, "int", {"unit": "cm²"},
                   ["Two halves make one whole: %d ÷ 2 = %d." % (half, half // 2),
                    "%d + %d = %d cm²." % (whole, half // 2, whole + half // 2)])

    def t_more_than_half():
        whole, big = random.randint(*_by(d, (4, 15), (6, 30), (20, 60))), random.randint(*_by(d, (2, 6), (2, 12), (8, 20)))
        if d == 2:                                     # hard: the less-than-half squares are given as a distractor
            small = random.randint(3, 15)
            return _tb("A puddle drawn on a 1 cm grid fully covers %d squares. It covers more than half of %d other "
                       "squares and less than half of %d more. Count a square if more than half is covered. Estimate the "
                       "area, in cm²." % (whole, big, small), whole + big, "int", {"unit": "cm²"},
                       ["Ignore the %d small bits." % small, "%d + %d = %d cm²." % (whole, big, whole + big)])
        return _tb("A puddle drawn on a 1 cm grid fully covers %d squares. It covers more than half of %d "
                   "other squares and less than half of some more. Count a square if more than half is "
                   "covered. Estimate the area, in cm²." % (whole, big), whole + big, "int", {"unit": "cm²"},
                   ["%d + %d = %d cm²." % (whole, big, whole + big)])

    def t_cells():
        rows, cols = 6, 8
        cells = {(random.randrange(rows), random.randrange(cols))}
        target = random.randint(*_by(d, (6, 14), (10, 26), (24, 36)))
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
        lo = random.randint(*_by(d, (5, 10), (10, 40), (30, 80))) * _by(d, 2, 1, 1)
        if d == 2:                                     # hard: the touched squares are not simply half of the rest
            t = random.randint(9, 40)
            return _tb("A pond fully covers %d squares of a 1 m grid and touches %d more squares. Its area is between %d m² "
                       "and how many m²?" % (lo, t, lo), lo + t, "int", {"unit": "m²"},
                       ["At most it covers every touched square: %d + %d = %d." % (lo, t, lo + t)])
        return _tb("A pond fully covers %d squares of a 1 m grid and touches %d more squares. Its area is "
                   "between %d m² and how many m²?" % (lo, lo // 2, lo), lo + lo // 2, "int", {"unit": "m²"},
                   ["At most it covers every touched square: %d + %d = %d." % (lo, lo // 2, lo + lo // 2)])

    def t_compare():
        w_lo, w_hi = _by(d, (4, 15), (8, 25), (20, 50))
        h_hi = _by(d, 3, 6, 15)
        a_w, a_h = random.randint(w_lo, w_hi), 2 * random.randint(1, h_hi)
        b_w, b_h = random.randint(w_lo, w_hi), 2 * random.randint(1, h_hi)
        ea, eb = a_w + a_h // 2, b_w + b_h // 2
        if ea == eb:
            b_w += 1
            eb += 1
        return _wq("Leaf A covers %d whole squares and %d half squares. Leaf B covers %d whole squares and %d half squares. "
                   "Which leaf has the larger area? (A or B)" % (a_w, a_h, b_w, b_h), "A" if ea > eb else "B",
                   ["A: %d + %d = %d. B: %d + %d = %d." % (a_w, a_h // 2, ea, b_w, b_h // 2, eb)], "A or B")

    def t_table():
        shapes = ["Pond", "Lawn", "Patio"]
        whole = [random.randint(*_by(d, (4, 15), (6, 30), (20, 60))) for _ in shapes]
        half = [2 * random.randint(*_by(d, (1, 3), (1, 8), (5, 15))) for _ in shapes]
        k = random.randrange(3)
        return _dt("A plan of a garden is drawn on a 1 m grid. The table counts the squares each part covers. Estimate the "
                   "area of the %s, in m², counting two half squares as one whole." % shapes[k].lower(),
                   ["Part", "Whole squares", "Half squares"], [[s, w, h] for s, w, h in zip(shapes, whole, half)],
                   whole[k] + half[k] // 2, ["%d + %d ÷ 2 = %d m²." % (whole[k], half[k], whole[k] + half[k] // 2)])

    def t_sensible():
        q, a = pick([("The outline of a child's hand, drawn on 1 cm squared paper. Is its area about 12 cm², 120 cm² or 1,200 cm²?", 120),
                     ("A puddle in the playground. Is its area about 1 m², 100 m² or 1,000 m²?", 1),
                     ("A postcard. Is its area about 15 cm², 150 cm² or 1,500 cm²?", 150),
                     ("A school field. Is its area about 50 m², 5,000 m² or 500,000 m²?", 5000)])
        return _tb(q + " Type the number.", a, "int", {}, ["Picture the real object."])

    def t_halves_only():
        h = 2 * random.randint(*_by(d, (2, 6), (4, 15), (12, 40)))
        return _tb("The edge of a lake drawn on a 1 km grid cuts %d squares exactly in half. Estimate the area those half "
                   "squares cover, in km²." % h, h // 2, "int", {"unit": "km²"}, ["Two halves make one: %d ÷ 2 = %d." % (h, h // 2)])

    def t_rule():
        full, more, less = (random.randint(*_by(d, r0, r1, r2)) for r0, r1, r2 in
                            [((4, 15), (8, 30), (20, 60)), ((2, 5), (2, 10), (8, 20)), ((2, 5), (2, 10), (8, 20))])
        return _tb("A shape on a 1 cm grid covers %d squares completely, more than half of %d squares and less than half of "
                   "%d squares. Using the rule 'count more than half, ignore less than half', estimate its area, in cm²."
                   % (full, more, less), full + more, "int", {"unit": "cm²"},
                   ["%d + %d = %d; the %d small bits are ignored." % (full, more, full + more, less)])

    def t_scale():
        sq = random.randint(*_by(d, (10, 40), (10, 40), (25, 60)))
        k = pick(_by(d, [10, 100], [4, 10, 100], [4, 25, 50]))
        return _tb("On a map, each grid square stands for %d m². A park covers about %d squares. Estimate the park's area, "
                   "in m²." % (k, sq), sq * k, "int", {"unit": "m²"}, ["%d × %d = %d." % (sq, k, sq * k)])

    return _pick_t([t_count, t_more_than_half, t_between, t_compare, t_sensible, t_halves_only, t_rule, t_scale],
                   [t_cells, t_table])


@skill("Y5.7.f", "Volume of cuboids using 1 cm³ cubes", S7)
def _(d=1):
    d = _d(d)
    l, w, h = random.randint(2, _by(d, 4, 6, 10)), random.randint(2, _by(d, 3, 5, 8)), random.randint(1, _by(d, 3, 5, 6))

    def t_count():
        return _tb("A cuboid is built from 1 cm cubes: %d cubes long, %d wide and %d tall. How many cubes "
                   "is that?" % (l, w, h), l * w * h, "int", {"unit": "cm³"},
                   ["%d × %d = %d in one layer." % (l, w, l * w), "%s: %d." % (_pl(h, "layer"), l * w * h)])

    def t_layer():
        return _tb("One layer of a cuboid has %d cubes. The cuboid has %s. What is its volume, in cm³?"
                   % (l * w, _pl(h, "layer")), l * w * h, "int", {"unit": "cm³"}, ["%d × %d = %d." % (l * w, h, l * w * h)])

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

    def t_add_layer():
        return _tb("A cuboid of 1 cm cubes is %d cubes long, %d wide and %d tall. Another layer is added on top. What is "
                   "the new volume, in cm³?" % (l, w, h), l * w * (h + 1), "int", {"unit": "cm³"},
                   ["One layer is %d × %d = %d cubes." % (l, w, l * w), "%s: %d." % (_pl(h + 1, "layer"), l * w * (h + 1))])

    def t_same():
        v = l * w * h
        good = (l * h, w, 1)
        bad = (l + 1, w, h)
        first = random.random() < 0.5
        A, B = (good, bad) if first else (bad, good)
        return _wq("A cuboid is %d × %d × %d cm. Which of these has the SAME volume? A: %d × %d × %d cm. B: %d × %d × %d cm. "
                   "(A or B)" % ((l, w, h) + A + B), "A" if first else "B",
                   ["%d × %d × %d = %d cm³." % (l, w, h, v), "%d × %d × %d = %d cm³." % (good + (v,))], "A or B")

    def t_room():
        a, b, c = random.randint(2, 6), random.randint(2, 5), random.randint(2, 3)
        return _tb("A storeroom is a cuboid %d m long, %d m wide and %d m high. How many 1 m³ crates would fill it exactly?"
                   % (a, b, c), a * b * c, "int", {"unit": "m³"}, ["%d × %d × %d = %d m³." % (a, b, c, a * b * c)])

    def t_half():
        v = l * w * h
        if v % 2:
            return t_layer()
        return _tb("A box is %d cm long, %d cm wide and %d cm tall. It is half full of 1 cm cubes. How many cubes are in it?"
                   % (l, w, h), v // 2, "int", {"unit": "cubes"},
                   ["Full: %d × %d × %d = %d." % (l, w, h, v), "Half: %d." % (v // 2)])

    def t_estimate():
        q, a = pick([("Is the volume of a dice about 1 cm³, 100 cm³ or 1,000 cm³?", 1),
                     ("Is the volume of a shoebox about 60 cm³, 6,000 cm³ or 600,000 cm³?", 6000),
                     ("Is the volume of a sugar cube about 1 cm³, 50 cm³ or 500 cm³?", 1),
                     ("Is the volume of a garden shed about 1 m³, 10 m³ or 100 m³?", 10)])
        return _tb(q + " Type the number.", a, "int", {}, ["Picture 1 cm cubes (the size of a sugar cube) or 1 m cubes."])

    return _pick_t([t_count, t_layer, t_missing, t_compare, t_cube, t_add_layer, t_same, t_room, t_half, t_estimate],
                   [t_table])


@skill("Y5.7.g", "Estimate and measure capacity", S7)
def _(d=1):
    d = _d(d)

    def t_jug():
        mx = pick(_by(d, [500, 1000], [500, 1000, 2000], [1000, 2000]))
        step = _by(d, 100, 50, 50)
        v = random.randint(1, mx // step - 1) * step
        if d == 2:                                     # hard: read in ml, answer in litres
            return {"prompt": "Read the measuring jug. How much water is in it, in litres?", "component": "ruler",
                    "spec": {"mode": "capacity", "value": v, "max": mx, "unit": "ml"}, "answer": _ds(Decimal(v) / 1000),
                    "answer_type": "num", "tolerance": 0.025,
                    "solution": ["The water reaches %d ml." % v, "%d ml = %s litres." % (v, _ds(Decimal(v) / 1000))]}
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
        cup, n = pick(_by(d, [200, 250], [150, 200, 250], [125, 150, 175])), random.randint(*_by(d, (2, 4), (2, 8), (5, 15)))
        bottle = pick(_by(d, [1000], [1000, 2000], [2000, 3000]))
        if cup * n > bottle:
            n = bottle // cup
        return _tb("A %d litre bottle of squash fills cups of %d ml. %d cups are poured. How much is left, in "
                   "ml?" % (bottle // 1000, cup, n), bottle - cup * n, "int", {"unit": "ml"},
                   ["%d × %d = %d." % (n, cup, n * cup), "%d − %d = %d." % (bottle, n * cup, bottle - n * cup)])

    def t_how_many():
        cup = pick(_by(d, [100, 250, 500], [100, 200, 250, 500], [125, 200, 250]))
        tot = pick(_by(d, [1000, 2000], [1000, 2000, 3000], [2000, 3000, 5000]))
        return _tb("How many %d ml glasses can be filled from %s?" % (cup, _pl(tot // 1000, "litre")), tot // cup,
                   "int", {}, ["%s = %d ml." % (_pl(tot // 1000, "litre"), tot), "%d ÷ %d = %d." % (tot, cup, tot // cup)])

    def t_volume_capacity():
        if d == 2:                                     # hard: give the answer in litres
            l, w, h = (10 * random.randint(1, 6) for _ in range(3))
            return _tb("A box-shaped tank is %d cm × %d cm × %d cm inside. 1 cm³ holds 1 ml. How many litres does it "
                       "hold?" % (l, w, h), _ds(Decimal(l * w * h) / 1000), "num", {"unit": "litres"},
                       ["%d × %d × %d = %d ml." % (l, w, h, l * w * h), "= %s litres." % _ds(Decimal(l * w * h) / 1000)])
        l, w, h = (random.randint(*_by(d, (2, 10), (5, 20), (5, 20))) for _ in range(3))
        return _tb("A box-shaped tank is %d cm × %d cm × %d cm inside. 1 cm³ holds 1 ml. How many ml does it "
                   "hold?" % (l, w, h), l * w * h, "int", {"unit": "ml"}, ["%d × %d × %d = %d." % (l, w, h, l * w * h)])

    def t_table():
        drinks = ["Milk", "Juice", "Water"]
        ml = [random.randint(*_by(d, (1, 9), (2, 19), (21, 199))) * _by(d, 100, 50, 5) for _ in drinks]
        rows = [[n, "%d ml" % v] for n, v in zip(drinks, ml)]
        return _dt("The table shows how much of each drink is left in the fridge. How many ml is that altogether?",
                   ["Drink", "Amount"], rows, sum(ml), ["%s = %d ml." % (" + ".join(map(str, ml)), sum(ml))])

    def t_doses():
        dose = pick(_by(d, [5, 10], [5, 10], [15, 20, 25]))
        bottle = pick(_by(d, [50, 100, 200], [100, 150, 200, 250], [300, 600]))
        return _tb("A bottle holds %d ml of medicine. One dose is %d ml. How many doses are in the bottle?" % (bottle, dose),
                   bottle // dose, "int", {"unit": "doses"}, ["%d ÷ %d = %d." % (bottle, dose, bottle // dose)])

    def t_litres():
        l_ = random.randint(1, 9)
        # hard: fewer than 100 ml, so a zero is needed as a place holder (3 litres 40 ml = 3040 ml)
        ml = random.randint(*_by(d, (1, 9), (1, 19), (1, 9))) * _by(d, 100, 50, 10)
        return _tb("A paddling pool holds %s and %d ml. How many ml is that altogether?" % (_pl(l_, "litre"), ml),
                   l_ * 1000 + ml, "int", {"unit": "ml"}, ["%d × 1000 + %d = %d." % (l_, ml, l_ * 1000 + ml)])

    def t_jug_more():
        mx = pick(_by(d, [500], [500, 1000], [1000, 2000]))
        step = _by(d, 100, 50, 50)
        v = random.randint(1, mx // step - 2) * step
        return {"prompt": "Read the measuring jug. How much more water is needed to reach %d ml?" % mx, "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": mx, "unit": "ml"}, "answer": mx - v,
                "answer_type": "num", "tolerance": 25, "solution": ["The jug holds %d ml; %d − %d = %d." % (v, mx, v, mx - v)]}

    return _pick_t([t_sensible, t_cups, t_how_many, t_volume_capacity, t_doses, t_litres], [t_jug, t_table, t_jug_more])


@skill("Y5.7.h", "Convert between units of time", S7)
def _(d=1):
    d = _d(d)

    def t_hm():
        h, m = random.randint(*_by(d, (1, 3), (1, 5), (4, 12))), random.randint(1, _by(d, 11, 59, 59)) * _by(d, 5, 1, 1)
        return _tb("How many minutes are in %s %s?" % (_pl(h, "hour"), _pl(m, "minute")), 60 * h + m, "int",
                   {"unit": "minutes"}, ["%d × 60 + %d = %d." % (h, m, 60 * h + m)])

    def t_mh():
        m = random.randint(5, 16) * 15 if d == 0 else random.randint(*_by(d, (61, 400), (61, 400), (400, 900)))
        return _tb("Write %d minutes as hours and minutes in the form h:mm (for example 2:15 means 2 hours "
                   "15 minutes)." % m, "%d:%02d" % divmod(m, 60), "time", {"text": True, "placeholder": "h:mm"},
                   ["%d ÷ 60 = %d remainder %d." % (m, m // 60, m % 60)])

    def t_seconds():
        m, s = random.randint(*_by(d, (1, 3), (1, 6), (5, 15))), random.randint(0, _by(d, 5, 59, 59)) * _by(d, 10, 1, 1)
        return _tb("How many seconds are in %s %s?" % (_pl(m, "minute"), _pl(s, "second")), 60 * m + s, "int",
                   {"unit": "seconds"}, ["%d × 60 + %d = %d." % (m, s, 60 * m + s)])

    def t_days():
        w = random.randint(2, _by(d, 5, 12, 12))
        if d == 2:                                     # hard: weeks and days
            k = random.randint(1, 6)
            return _tb("How many days are in %d weeks and %s?" % (w, _pl(k, "day")), 7 * w + k, "int", {"unit": "days"},
                       ["%d × 7 + %d = %d." % (w, k, 7 * w + k)])
        return _tb("How many days are in %d weeks?" % w, 7 * w, "int", {"unit": "days"}, ["%d × 7 = %d." % (w, 7 * w)])

    def t_months():
        y = random.randint(2, _by(d, 5, 9, 9))
        if d == 2:                                     # hard: years and months
            k = random.randint(1, 11)
            return _tb("How many months are in %d years and %s?" % (y, _pl(k, "month")), 12 * y + k, "int",
                       {"unit": "months"}, ["%d × 12 + %d = %d." % (y, k, 12 * y + k)])
        return _tb("How many months are in %d years?" % y, 12 * y, "int", {"unit": "months"},
                   ["%d × 12 = %d." % (y, 12 * y)])

    def t_month_days():
        if d == 2:                                     # hard: two months together
            ms = [("January", 31), ("February", 28), ("March", 31), ("April", 30), ("May", 31), ("June", 30),
                  ("July", 31), ("August", 31), ("September", 30), ("October", 31), ("November", 30), ("December", 31)]
            i = random.randint(2, 10)
            (a, da), (b, db) = ms[i], ms[i + 1]
            return _tb("How many days are there in %s and %s together?" % (a, b), da + db, "int", {"unit": "days"},
                       ["%s has %d days and %s has %d." % (a, da, b, db), "%d + %d = %d." % (da, db, da + db)])
        m, days = pick([("April", 30), ("June", 30), ("September", 30), ("November", 30), ("January", 31),
                        ("March", 31), ("July", 31), ("October", 31), ("December", 31)])
        return _tb("How many days are there in %s?" % m, days, "int", {"unit": "days"},
                   ["30 days has September, April, June and November."])

    def t_leap():
        y = pick([2024, 2028, 2032, 2025, 2026, 2027, 2030])
        if d == 2:                                     # hard: depends on whether February has 29 days
            feb = 29 if y % 4 == 0 else 28
            return _tb("How many days are there in January and February %d together?" % y, 31 + feb, "int",
                       {"unit": "days"}, ["%d %s a leap year, so February has %d days." % (y, "is" if feb == 29 else
                                                                                        "is not", feb),
                                          "31 + %d = %d." % (feb, 31 + feb)])
        return _tb("How many days are there in the year %d?" % y, 366 if y % 4 == 0 else 365, "int",
                   {"unit": "days"}, ["%d %s divisible by 4, so it %s a leap year." % (y, "is" if y % 4 == 0 else
                                                                                       "is not",
                                                                                       "is" if y % 4 == 0 else "is not")])

    def t_hours_days():
        h = random.randint(*_by(d, (1, 2), (2, 5), (5, 9))) * 24 + random.randint(_by(d, 1, 0, 0), 23)
        return _tb("%d hours is some whole days and some hours left over. How many hours are left over?" % h,
                   h % 24, "int", {"unit": "hours"}, ["%d ÷ 24 = %d remainder %d." % (h, h // 24, h % 24)])

    def t_timetable():
        starts = [(9, 15), (10, 5), (11, 40)]
        k = random.randrange(3)
        dur = random.randint(3, 11) * 5 if d == 0 else random.randint(*_by(d, (25, 95), (25, 95), (65, 150)))
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
        g = Decimal(random.randint(*_by(d, (1, 4), (5, 40), (21, 95)))) * _by(d, 100, 10, 5)
        k = random.randint(*_by(d, (2, 3), (2, 5), (4, 8)))
        return _tb("A cake for 6 people needs %s g of flour. How much flour, in kg, for %d people?"
                   % (_ds(g), 6 * k), _ds(g * k / 1000), "num", {"unit": "kg"},
                   ["%s × %d = %s g." % (_ds(g), k, _ds(g * k)), "= %s kg." % _ds(g * k / 1000)])

    def t_lengths():
        n = random.randint(*_by(d, (2, 4), (3, 9), (3, 9)))
        x = Decimal(random.randint(*_by(d, (11, 49), (11, 99), (125, 499)))) / _by(d, 10, 10, 100)
        return _tb("%d planks are each %s m long. What is their total length, in metres?" % (n, _ds(x)),
                   _ds(n * x), "num", {"unit": "m"}, ["%d × %s = %s." % (n, _ds(x), _ds(n * x))])

    def t_share():
        n = random.randint(*_by(d, (2, 4), (2, 8), (6, 9)))
        each = Decimal(random.randint(*_by(d, (1, 9), (11, 99), (11, 99)))) / _by(d, 10, 100, 100)
        tot = each * n
        return _tb("%s %s of juice is shared equally into %d bottles. How much is in each bottle, in "
                   "litres?" % (_ds(tot), "litre" if tot == 1 else "litres", n), _ds(each), "num", {"unit": "litres"},
                   ["%s ÷ %d = %s." % (_ds(tot), n, _ds(each))])

    def t_mixed_units():
        a = Decimal(random.randint(11, 49)) / 10
        # easy: whole hundreds of grams; hard: under 100 g, so 45 g = 0.045 kg needs place holders
        b = random.randint(*_by(d, (1, 9), (150, 950), (5, 95))) * _by(d, 100, 1, 1)
        return _tb("A parcel weighs %s kg. A second parcel weighs %d g. What is their total mass, in kg?"
                   % (_ds(a), b), _ds(a + Decimal(b) / 1000), "num", {"unit": "kg"},
                   ["%d g = %s kg." % (b, _ds(Decimal(b) / 1000)), "%s + %s = %s." % (_ds(a), _ds(Decimal(b) / 1000),
                                                                                     _ds(a + Decimal(b) / 1000))])

    def t_run():
        lap = Decimal(random.randint(*_by(d, (2, 8), (2, 8), (25, 85)))) / _by(d, 10, 10, 100)
        n = random.randint(*_by(d, (2, 5), (3, 12), (3, 12)))
        return _tb("A running track is %s km round. %s runs %d laps. How far is that, in km?" % (_ds(lap), _who(), n),
                   _ds(lap * n), "num", {"unit": "km"}, ["%d × %s = %s." % (n, _ds(lap), _ds(lap * n))])

    def t_table():
        items = [("Flour", Decimal(random.randint(5, 30)) / 10), ("Sugar", Decimal(random.randint(2, 15)) / 10),
                 ("Butter", Decimal(random.randint(1, 9)) / 10)]
        k = random.randint(*_by(d, (2, 3), (2, 5), (6, 9)))
        i = random.randrange(3)
        return _dt("A baker's recipe uses these amounts. The baker makes %d times the recipe. How many kg of %s are "
                   "needed?" % (k, items[i][0].lower()), ["Ingredient", "Mass (kg)"],
                   [[n, _ds(v)] for n, v in items], _ds(items[i][1] * k),
                   ["%s × %d = %s." % (_ds(items[i][1]), k, _ds(items[i][1] * k))], atype="num")

    def t_graph():
        wk = ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5"]
        vals = sorted(Decimal(v) / _by(d, 1, 2, 4) for v in random.sample(range(*_by(d, (1, 9), (2, 13), (4, 25))), 5))
        i, j = sorted(random.sample(range(5), 2))
        return _lg("The graph shows a puppy's mass each week, in kg. How much heavier was it in %s than in %s, in kg?"
                   % (wk[j], wk[i]), [(a, float(v)) for a, v in zip(wk, vals)], _ds(vals[j] - vals[i]),
                   ["%s − %s = %s." % (_ds(vals[j]), _ds(vals[i]), _ds(vals[j] - vals[i]))], "kg", "Week", atype="num")

    def t_compare():
        a = Decimal(random.randint(*_by(d, (11, 49), (105, 495), (105, 495)))) / _by(d, 10, 100, 100)
        b = random.randint(*_by(d, (11, 49), (105, 495), (105, 495))) * _by(d, 10, 1, 1)
        if d == 2:                                     # hard: within a few cm of each other
            b = int(a * 100) + pick([-9, -5, -2, 2, 5, 9])
        if a * 100 == b:
            b += 1
        return _tb("Which is longer, %s m or %d cm? Type the longer length in cm." % (_ds(a), b), max(int(a * 100), b),
                   "int", {"unit": "cm"}, ["%s m = %d cm." % (_ds(a), int(a * 100))])

    def t_scale_down():
        g = random.randint(*_by(d, (1, 3), (2, 9), (2, 9))) * 300
        if d == 2:                                     # hard: scale down then up, 9 people to 6
            return _tb("A cake for 9 people needs %d g of flour. How much flour is needed for 6 people, in kg?" % g,
                       _ds(Decimal(g) / 3 * 2 / 1000), "num", {"unit": "kg"},
                       ["%d ÷ 3 = %d g for 3 people." % (g, g // 3), "× 2 = %d g = %s kg." % (g // 3 * 2,
                                                                                         _ds(Decimal(g // 3 * 2) / 1000))])
        return _tb("A cake for 9 people needs %d g of flour. How much flour is needed for 3 people, in kg?" % g,
                   _ds(Decimal(g) / 3 / 1000), "num", {"unit": "kg"},
                   ["%d ÷ 3 = %d g." % (g, g // 3), "= %s kg." % _ds(Decimal(g // 3) / 1000)])

    def t_ribbon_cm():
        a = Decimal(random.randint(*_by(d, (15, 49), (15, 49), (25, 49)))) / 10
        cm = random.randint(*_by(d, (2, 9), (15, 95), (105, 195))) * _by(d, 10, 1, 1)
        return _tb("A roll has %s m of ribbon. %d cm is cut off. How much is left, in metres?" % (_ds(a), cm),
                   _ds(a - Decimal(cm) / 100), "num", {"unit": "m"},
                   ["%d cm = %s m." % (cm, _ds(Decimal(cm) / 100)), "%s − %s = %s." % (_ds(a), _ds(Decimal(cm) / 100),
                                                                                       _ds(a - Decimal(cm) / 100))])

    def t_drinks():
        l_ = random.randint(*_by(d, (1, 2), (1, 3), (2, 3)))
        cups = random.randint(*_by(d, (2, 4), (3, 8), (5, 12)))
        cup = pick(_by(d, [200, 250], [150, 200, 250], [125, 150, 175]))
        if cups * cup >= l_ * 1000:
            cups = (l_ * 1000 - 1) // cup
        return _tb("A jug holds %d litre%s of lemonade. %d cups of %d ml are poured out. How much is left, in litres?"
                   % (l_, "" if l_ == 1 else "s", cups, cup), _ds(Decimal(l_ * 1000 - cups * cup) / 1000), "num",
                   {"unit": "litres"}, ["%d × %d = %d ml poured." % (cups, cup, cups * cup),
                                        "%d − %d = %d ml = %s %s." % (l_ * 1000, cups * cup, l_ * 1000 - cups * cup,
                                                                       _ds(Decimal(l_ * 1000 - cups * cup) / 1000),
                                                                       "litre" if l_ * 1000 - cups * cup == 1000 else "litres")])

    def t_laps_m():
        lap = random.randint(*_by(d, (2, 5), (2, 8), (15, 45))) * _by(d, 100, 50, 10)
        n = random.randint(*_by(d, (2, 5), (3, 12), (5, 15)))
        return _tb("A running track is %d m round. %s runs %d laps. How far is that, in km?" % (lap, _who(), n),
                   _ds(Decimal(lap * n) / 1000), "num", {"unit": "km"},
                   ["%d × %d = %d m." % (lap, n, lap * n), "= %s km." % _ds(Decimal(lap * n) / 1000)])

    def t_tins():
        tin = Decimal(random.randint(*_by(d, (2, 9), (2, 9), (25, 95)))) / _by(d, 10, 10, 100)
        n = random.randint(*_by(d, (2, 4), (3, 9), (3, 9)))
        return _tb("A tin of beans weighs %s kg. What do %d tins weigh, in grams?" % (_ds(tin), n),
                   int(tin * n * 1000), "int", {"unit": "g"},
                   ["%d × %s = %s kg." % (n, _ds(tin), _ds(tin * n)), "= %d g." % int(tin * n * 1000)])

    return _pick_t([t_scale_recipe, t_lengths, t_share, t_mixed_units, t_run, t_compare, t_scale_down, t_ribbon_cm,
                    t_drinks, t_laps_m, t_tins],
                   [t_table, t_graph])


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
        return _dt("Use the price list. How much do %s %s%s and one %s cost altogether, in pounds?"
                   % (n_words(qa), menu[a][0].lower(), "" if qa == 1 else ("es" if menu[a][0] == "Sandwich" else "s"),
                      menu[b][0].lower()), ["Item", "Price"], rows,
                   _ds(tot), ["%d × £%s + £%s = £%s." % (qa, format(Decimal(menu[a][1]) / 100, ".2f"),
                                                         format(Decimal(menu[b][1]) / 100, ".2f"), format(tot, ".2f"))],
                   atype="num")

    return _pick_t([t_change, t_multiple, t_split, t_save], [t_table])
