# Year 5 generators: strands 5.2 and 5.3.
#
# Addition and subtraction with more than 4 digits (written and mental), inverse checks,
# multi-step problems and the equals sign; multiples, factors, common factors, primes,
# prime factors, square and cube numbers.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S2 = "5.2 Addition & subtraction"
S3 = "5.3 Multiples, factors, primes, squares & cubes"

PRIMES = [p for p in range(2, 101) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def _big(d):
    return random.randint(_by(d, 10000, 20000, 100000), _by(d, 99999, 999999, 999999))


def _factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def _pairs(n):
    return [(k, n // k) for k in range(1, int(n ** 0.5) + 1) if n % k == 0]


# ================================================================== 5.2 ======
@skill("Y5.2.a", "Column addition with more than 4 digits", S2)
def _(d=1):
    d = _d(d)
    a, b = _big(d), _big(d)
    if d == 0:
        b = random.randint(1000, 9999)

    def t_plain():
        return _tb("Work out %s + %s using the column method." % (_c(a), _c(b)), a + b, "int", {},
                   ["Line up the digits by place value and add from the ones.",
                    "%s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_three():
        c = random.randint(1000, 99999)
        return _tb("Add these three numbers: %s, %s and %s." % (_c(a), _c(b), _c(c)), a + b + c, "int",
                   {}, ["%s + %s = %s." % (_c(a), _c(b), _c(a + b)),
                        "%s + %s = %s." % (_c(a + b), _c(c), _c(a + b + c))])

    def t_word():
        what = pick([("visitors came to the zoo in July", "in August"),
                     ("people ran the race last year", "this year"),
                     ("litres of water were used on Monday", "on Tuesday")])
        return _tb("%s %s and %s %s. How many altogether?" % (_c(a), what[0], _c(b), what[1]),
                   a + b, "int", {}, ["%s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_missing_digit():
        s = a + b
        st = list(str(a))
        k = random.randrange(1, len(st))
        hidden = st[k]
        st[k] = "□"
        return _tb("In this column addition one digit is hidden: %s + %s = %s. What is the "
                   "missing digit □?" % ("".join(st), _c(b), _c(s)), int(hidden), "int", {},
                   ["%s − %s = %s." % (_c(s), _c(b), _c(a))])

    def t_money():
        x, y = random.randint(10000, 99999), random.randint(10000, 99999)
        return _tb("A charity raised £%s in spring and £%s in autumn. How much did it raise "
                   "altogether, in pounds?" % (_c(x), _c(y)), x + y, "int", {"unit": "£"},
                   ["£%s + £%s = £%s." % (_c(x), _c(y), _c(x + y))])

    def t_table():
        names = random.sample(["North Stand", "South Stand", "East Stand", "West Stand"], 3)
        vals = [random.randint(10000, 40000) for _ in names]
        rows = [[n, _c(v)] for n, v in zip(names, vals)] + [["Total", _c(sum(vals))]]
        return _dt("The table shows the crowd in each stand. What is the total?", ["Stand", "People"],
                   rows, sum(vals), ["%s = %s." % (" + ".join(_c(v) for v in vals), _c(sum(vals)))],
                   missing=[3, 1])

    return _pick_t([t_plain, t_three, t_word, t_missing_digit, t_money], [t_table])


@skill("Y5.2.b", "Column subtraction with more than 4 digits", S2)
def _(d=1):
    d = _d(d)
    a = _big(d)
    b = random.randint(1000, a - 1)
    if d == 2 and random.random() < 0.5:              # exchanging across zeros
        a = random.randint(1, 9) * 100000 + random.randint(0, 9) * 1000 + pick([0, 100, 10])
        b = random.randint(10000, a - 1)

    def t_plain():
        return _tb("Work out %s − %s using the column method." % (_c(a), _c(b)), a - b, "int", {},
                   ["Subtract from the ones, exchanging where needed.",
                    "%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_difference():
        return _tb("What is the difference between %s and %s?" % (_c(a), _c(b)), a - b, "int", {},
                   ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_word():
        return _tb("A stadium holds %s people. %s tickets have been sold. How many tickets are "
                   "left?" % (_c(a), _c(b)), a - b, "int", {},
                   ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_from_round():
        r = random.randint(1, 9) * pick([100000, 10000])
        x = random.randint(1, r - 1)
        return _tb("Work out %s − %s." % (_c(r), _c(x)), r - x, "int", {},
                   ["Exchange across the zeros.", "%s − %s = %s." % (_c(r), _c(x), _c(r - x))])

    def t_bar():
        return _strip("The bar model shows a whole of %s split into two parts. One part is %s. "
                      "How big is the other part?" % (_c(a), _c(b)),
                      {"mode": "part_whole", "totalLabel": _c(a), "partLabel": _c(b),
                       "unknown": "part", "parts": 2},
                      a - b, ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    def t_how_many_more():
        c1, c2 = random.sample(["Fenton", "Oakfield", "Redhill", "Stanton"], 2)
        return _tb("%s has %s people and %s has %s people. How many more people live in %s?"
                   % (c1, _c(a), c2, _c(b), c1), a - b, "int", {},
                   ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))])

    return _pick_t([t_plain, t_difference, t_word, t_from_round, t_how_many_more], [t_bar])


@skill("Y5.2.c", "Add and subtract large numbers mentally", S2)
def _(d=1):
    d = _d(d)
    base = random.randint(10, 99) * _by(d, 100, 1000, 1000) + random.randint(0, 9) * _by(d, 10, 100, 1)

    def t_add_round():
        k = random.randint(1, 9) * pick([1000, 10000])
        return _tb("Work out mentally: %s + %s" % (_c(base), _c(k)), base + k, "int", {},
                   ["Only the %s digit changes (with any carry)." % ("thousands" if k < 10000 else
                                                                     "ten thousands")])

    def t_near():
        k = random.randint(2, 9) * 1000
        off = pick([1, 2, 10, 100])
        x = k - off
        return _tb("Work out %s + %s. Hint: add %s and then take away %s." % (_c(base), _c(x), _c(k),
                                                                             _c(off)),
                   base + x, "int", {},
                   ["%s + %s = %s." % (_c(base), _c(k), _c(base + k)),
                    "%s − %s = %s." % (_c(base + k), _c(off), _c(base + x))])

    def t_sub_near():
        k = random.randint(2, 9) * 1000
        off = pick([1, 2, 10, 100])
        x = k - off
        b = base + 10000
        return _tb("Work out mentally: %s − %s" % (_c(b), _c(x)), b - x, "int", {},
                   ["Subtract %s, then add back %s." % (_c(k), _c(off)),
                    "%s − %s + %s = %s." % (_c(b), _c(k), _c(off), _c(b - x))])

    def t_bonds():
        t = pick([10000, 100000, 1000000])
        x = random.randint(1, t // 1000 - 1) * pick([1000, 100, 10]) if t > 10000 else \
            random.randint(1, 99) * 100
        x = min(x, t - 1)
        return _tb("What must be added to %s to make %s?" % (_c(x), _c(t)), t - x, "int", {},
                   ["%s − %s = %s." % (_c(t), _c(x), _c(t - x))])

    def t_double():
        x = random.randint(11, 49) * pick([1000, 10000])
        return _tb("Double %s." % _c(x), 2 * x, "int", {}, ["%s + %s = %s." % (_c(x), _c(x), _c(2 * x))])

    def t_half():
        x = random.randint(11, 98) * pick([2000, 20000])
        return _tb("Halve %s." % _c(x), x // 2, "int", {}, ["%s ÷ 2 = %s." % (_c(x), _c(x // 2))])

    return _pick_t([t_add_round, t_near, t_sub_near, t_bonds, t_double, t_half])


@skill("Y5.2.d", "Missing numbers and checking with the inverse", S2)
def _(d=1):
    d = _d(d)
    a, b = _big(d), random.randint(1000, 99999)

    def t_add_missing():
        return _tb("Find the missing number:  %s + ___ = %s" % (_c(a), _c(a + b)), b, "int", {},
                   ["Use the inverse: %s − %s = %s." % (_c(a + b), _c(a), _c(b))])

    def t_sub_missing_first():
        return _tb("Find the missing number:  ___ − %s = %s" % (_c(b), _c(a)), a + b, "int", {},
                   ["Use the inverse: %s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_sub_missing_second():
        x = a + b
        return _tb("Find the missing number:  %s − ___ = %s" % (_c(x), _c(a)), b, "int", {},
                   ["%s − %s = %s." % (_c(x), _c(a), _c(b))])

    def t_check():
        s = a + b
        wrong = s + pick([-1, 1]) * pick([10, 100, 1000, 9])
        shown = pick([s, wrong])
        ok = shown == s
        return _wq("%s worked out %s + %s = %s and checked it with the inverse, %s − %s. Is the "
                   "answer correct? (yes or no)" % (_who(), _c(a), _c(b), _c(shown), _c(shown), _c(b)),
                   "yes" if ok else "no",
                   ["%s − %s = %s, which %s %s." % (_c(shown), _c(b), _c(shown - b),
                                                     "is" if ok else "is not", _c(a))], "yes / no")

    def t_inverse_fact():
        s = a + b
        return _tb("%s + %s = %s. Use this to work out %s − %s." % (_c(a), _c(b), _c(s), _c(s), _c(a)),
                   b, "int", {}, ["Addition and subtraction are inverses: %s − %s = %s."
                                  % (_c(s), _c(a), _c(b))])

    def t_think():
        x = random.randint(10000, 90000)
        k = random.randint(1000, 9000)
        res = x + k
        return _tb("%s thinks of a number and adds %s. The answer is %s. What was the number?"
                   % (_who(), _c(k), _c(res)), x, "int", {},
                   ["%s − %s = %s." % (_c(res), _c(k), _c(x))])

    return _pick_t([t_add_missing, t_sub_missing_first, t_sub_missing_second, t_check,
                    t_inverse_fact, t_think])


@skill("Y5.2.e", "Multi-step addition and subtraction problems", S2)
def _(d=1):
    d = _d(d)
    who = _who()

    def t_bank():
        start = random.randint(2000, 20000)
        add = random.randint(500, 9000)
        spend = random.randint(500, start + add - 100)
        return _tb("A club has £%s. It raises £%s at a fair and then spends £%s on kit. How much "
                   "does it have now, in pounds?" % (_c(start), _c(add), _c(spend)),
                   start + add - spend, "int", {"unit": "£"},
                   ["%s + %s = %s." % (_c(start), _c(add), _c(start + add)),
                    "%s − %s = %s." % (_c(start + add), _c(spend), _c(start + add - spend))])

    def t_three_days():
        target = random.randint(30000, 90000)
        a, b = random.randint(5000, target // 3), random.randint(5000, target // 3)
        return _tb("A school wants to collect %s bottle tops. It collects %s in the first week and "
                   "%s in the second. How many more does it need?" % (_c(target), _c(a), _c(b)),
                   target - a - b, "int", {},
                   ["%s + %s = %s collected." % (_c(a), _c(b), _c(a + b)),
                    "%s − %s = %s." % (_c(target), _c(a + b), _c(target - a - b))])

    def t_compare_totals():
        a1, a2, b1, b2 = [random.randint(10000, 60000) for _ in range(4)]
        diff = abs((a1 + a2) - (b1 + b2))
        return _tb("Team Red scored %s and %s points in two games. Team Blue scored %s and %s. "
                   "What is the difference between the two teams' totals?"
                   % (_c(a1), _c(a2), _c(b1), _c(b2)), diff, "int", {},
                   ["Red: %s. Blue: %s." % (_c(a1 + a2), _c(b1 + b2)), "Difference: %s." % _c(diff)])

    def t_journey():
        total = random.randint(1000, 5000)
        a = random.randint(200, total // 3)
        b = random.randint(200, total // 3)
        return _tb("A car journey is %s km. %s drives %s km on day 1 and %s km on day 2. How far "
                   "is left to drive, in km?" % (_c(total), who, _c(a), _c(b)), total - a - b, "int",
                   {"unit": "km"}, ["%s − %s − %s = %s." % (_c(total), _c(a), _c(b), _c(total - a - b))])

    def t_table():
        months = ["Jan", "Feb", "Mar"]
        sold = [random.randint(10000, 50000) for _ in months]
        target = sum(sold) + random.randint(1000, 20000)
        rows = [[m, _c(v)] for m, v in zip(months, sold)]
        return _dt("A factory's target was %s toys for these three months. The table shows how many "
                   "it made. By how many did it miss the target?" % _c(target), ["Month", "Toys made"],
                   rows, target - sum(sold),
                   ["Total made: %s." % _c(sum(sold)), "%s − %s = %s." % (_c(target), _c(sum(sold)),
                                                                          _c(target - sum(sold)))])

    def t_bar():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(10, 90) * 100 for _ in cats]
        target = sum(vals) + random.randint(5, 40) * 100
        return _bar("The chart shows how many people visited a museum each day. The museum hoped for "
                    "%s visitors over the four days. How many short of that target was it?"
                    % _c(target), cats, vals, target - sum(vals),
                    ["Total: %s = %s." % (" + ".join(_c(v) for v in vals), _c(sum(vals))),
                     "%s − %s = %s." % (_c(target), _c(sum(vals)), _c(target - sum(vals)))])

    return _pick_t([t_bank, t_three_days, t_compare_totals, t_journey], [t_table, t_bar])


@skill("Y5.2.f", "The equals sign and balanced number sentences", S2)
def _(d=1):
    d = _d(d)
    u = _by(d, 10, 100, 1000)

    def t_balance_add():
        a, b = random.randint(10, 99) * u, random.randint(10, 99) * u
        c = random.randint(5, (a + b) // u - 5) * u
        return _tb("Make both sides equal:  %s + %s = %s + ___" % (_c(a), _c(b), _c(c)), a + b - c,
                   "int", {}, ["The left side is %s." % _c(a + b),
                               "%s − %s = %s." % (_c(a + b), _c(c), _c(a + b - c))])

    def t_balance_sub():
        a = random.randint(50, 99) * u
        b = random.randint(10, 40) * u
        c = random.choice([x for x in range(10, 41) if x * u != b]) * u
        return _tb("Make both sides equal:  %s − %s = ___ − %s" % (_c(a), _c(b), _c(c)),
                   a - b + c, "int", {}, ["The left side is %s." % _c(a - b),
                                          "%s + %s = %s." % (_c(a - b), _c(c), _c(a - b + c))])

    def t_true():
        a, b = random.randint(100, 999) * u, random.randint(100, 999) * u
        rhs = a + b if random.random() < 0.5 else a + b + pick([-1, 1]) * pick([u, 10 * u])
        ok = rhs == a + b
        return _wq("Is this number sentence true or false?  %s + %s = %s" % (_c(a), _c(b), _c(rhs)),
                   "true" if ok else "false", ["%s + %s = %s." % (_c(a), _c(b), _c(a + b))],
                   "true / false")

    def t_meaning():
        a, b = random.randint(20, 90), random.randint(20, 90)
        return _tb("%s writes %d + %d = ___ + %d. The '=' means both sides have the same value. "
                   "What number goes in the gap?" % (_who(), a, b, b), a, "int", {},
                   ["Both sides add %d, so the gap must be %d." % (b, a)])

    def t_mixed():
        a, b = random.randint(2, 9) * u, random.randint(2, 9)
        lhs = a * b
        c = pick([k for k in (2, 3, 4, 5, 6, 8, 10) if lhs % k == 0 and k != b])
        return _tb("Make both sides equal:  %s × %d = ___ × %d" % (_c(a), b, c), lhs // c, "int", {},
                   ["The left side is %s." % _c(lhs), "%s ÷ %d = %s." % (_c(lhs), c, _c(lhs // c))])

    return _pick_t([t_balance_add, t_balance_sub, t_true, t_meaning, t_mixed])


# ================================================================== 5.3 ======
@skill("Y5.3.a", "Multiples", S3)
def _(d=1):
    d = _d(d)
    m = pick(_by(d, [2, 3, 4, 5, 10], [6, 7, 8, 9, 11, 12], [13, 15, 25, 7, 9]))

    def t_list():
        k = random.randint(4, 6)
        return _wq("List the first %d multiples of %d, starting with %d. Separate them with commas."
                   % (k, m, m), ", ".join(str(m * i) for i in range(1, k + 1)),
                   ["Count in %ds." % m], "e.g. 3, 6, 9")

    def t_which():
        good = m * random.randint(3, 12)
        bad = [good + random.randint(1, m - 1) if m > 1 else good + 1 for _ in range(2)]
        bad = [b for b in bad if b % m] or [good + 1]
        opts = [good] + bad[:2]
        random.shuffle(opts)
        return _tb("Which of these is a multiple of %d?  %s" % (m, ", ".join(map(str, opts))), good,
                   "int", {}, ["%d ÷ %d = %d exactly." % (good, m, good // m)])

    def t_is():
        n = random.randint(20, 150)
        return _wq("Is %d a multiple of %d? (yes or no)" % (n, m), "yes" if n % m == 0 else "no",
                   ["%d ÷ %d = %d remainder %d." % (n, m, n // m, n % m)], "yes / no")

    def t_count():
        hi = random.randint(5, 10) * 10
        return _tb("How many multiples of %d are there between 1 and %d?" % (m, hi), hi // m, "int", {},
                   ["%d ÷ %d = %d (ignore any remainder)." % (hi, m, hi // m)])

    def t_nearest():
        n = random.randint(30, 200)
        below, above = (n // m) * m, (n // m + 1) * m
        nearest = below if n - below < above - n else above
        if n - below == above - n:
            return t_count()
        return _tb("Which multiple of %d is nearest to %d?" % (m, n), nearest, "int", {},
                   ["The multiples either side are %d and %d." % (below, above)])

    def t_both():
        a, b = random.sample([2, 3, 4, 5, 6, 10], 2)
        lcm = a * b // _gcd(a, b)
        n = lcm * random.randint(2, 6)
        return _wq("Is %d a multiple of both %d and %d? (yes or no)" % (n, a, b), "yes",
                   ["%d ÷ %d = %d and %d ÷ %d = %d." % (n, a, n // a, n, b, n // b)], "yes / no") \
            if random.random() < 0.5 else _wq(
                "Is %d a multiple of both %d and %d? (yes or no)" % (n + a, a, b),
                "yes" if (n + a) % b == 0 else "no",
                ["%d ÷ %d leaves remainder %d." % (n + a, b, (n + a) % b)], "yes / no")

    def t_table():
        rows = [[i, m * i] for i in range(1, 6)]
        k = random.randint(1, 4)
        return _io("The table shows multiples of %d. What goes in the empty cell?" % m, rows, k,
                   rows[k][1], ["%d × %d = %d." % (rows[k][0], m, rows[k][1])], rule="× %d" % m)

    return _pick_t([t_list, t_which, t_is, t_count, t_nearest, t_both], [t_table])


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


@skill("Y5.3.b", "Factors and factor pairs", S3)
def _(d=1):
    d = _d(d)
    n = pick(_by(d, [12, 16, 18, 20, 24, 30, 36], [24, 36, 40, 42, 48, 60, 64, 72],
                 [72, 84, 90, 96, 100, 120, 144]))

    def t_all():
        return _wq("List ALL the factors of %d, smallest first, separated by commas." % n,
                   ", ".join(map(str, _factors(n))),
                   ["Factor pairs: %s." % ", ".join("%d × %d" % p for p in _pairs(n))], "e.g. 1, 2, 3")

    def t_count():
        return _tb("How many factors does %d have?" % n, len(_factors(n)), "int", {},
                   ["The factors are %s." % ", ".join(map(str, _factors(n)))])

    def t_partner():
        a, b = pick([p for p in _pairs(n) if p[0] > 1])
        return _tb("%d × ___ = %d. Find the other number in the factor pair." % (a, n), b, "int", {},
                   ["%d ÷ %d = %d." % (n, a, b)])

    def t_is_factor():
        k = random.randint(2, 15)
        return _wq("Is %d a factor of %d? (yes or no)" % (k, n), "yes" if n % k == 0 else "no",
                   ["%d ÷ %d = %d remainder %d." % (n, k, n // k, n % k)], "yes / no")

    def t_pairs_count():
        return _tb("How many different factor pairs does %d have? (Count 2 × 3 and 3 × 2 as the "
                   "same pair.)" % n, len(_pairs(n)), "int", {},
                   ["%s." % ", ".join("%d × %d" % p for p in _pairs(n))])

    def t_array():
        a, b = pick([p for p in _pairs(n) if p[0] > 1])
        return {"prompt": "Build an array with %d rows of %d. How many counters is that? The rows and "
                          "columns are a factor pair of the total." % (a, b),
                "component": "array", "spec": {"mode": "build", "maxRows": 12, "maxCols": 12,
                                               "targetRows": a, "targetCols": b},
                "answer": n, "answer_type": "int", "solution": ["%d × %d = %d." % (a, b, n)]} \
            if a <= 12 and b <= 12 else t_partner()

    def t_table():
        ps = _pairs(n)
        rows = [[a, b] for a, b in ps]
        k = random.randrange(len(rows))
        return _dt("This table lists every factor pair of %d. What number belongs in the empty cell?"
                   % n, ["Factor", "Partner"], rows, ps[k][1], ["%d ÷ %d = %d." % (n, ps[k][0], ps[k][1])],
                   missing=[k, 1])

    def t_largest():
        f = [k for k in _factors(n) if k < n]
        return _tb("What is the largest factor of %d that is smaller than %d?" % (n, n), max(f), "int",
                   {}, ["%d ÷ 2 = %d" % (n, n // 2) if n % 2 == 0 else "Check the factor list."])

    return _pick_t([t_all, t_count, t_partner, t_is_factor, t_pairs_count, t_largest], [t_array, t_table])


@skill("Y5.3.c", "Common factors of two numbers", S3)
def _(d=1):
    d = _d(d)
    g = pick(_by(d, [2, 3, 4, 5], [4, 6, 8, 9], [6, 8, 12, 15]))
    a, b = random.sample([g * k for k in range(2, 9)], 2)
    common = [k for k in _factors(min(a, b)) if a % k == 0 and b % k == 0]

    def t_list():
        return _wq("List all the common factors of %d and %d, smallest first, separated by commas."
                   % (a, b), ", ".join(map(str, common)),
                   ["Factors of %d: %s." % (a, ", ".join(map(str, _factors(a)))),
                    "Factors of %d: %s." % (b, ", ".join(map(str, _factors(b))))], "e.g. 1, 2, 4")

    def t_highest():
        return _tb("What is the highest common factor of %d and %d?" % (a, b), max(common), "int", {},
                   ["Common factors: %s." % ", ".join(map(str, common))])

    def t_count():
        return _tb("How many common factors do %d and %d have?" % (a, b), len(common), "int", {},
                   ["They are %s." % ", ".join(map(str, common))])

    def t_is():
        k = random.randint(2, 12)
        ok = a % k == 0 and b % k == 0
        return _wq("Is %d a common factor of %d and %d? (yes or no)" % (k, a, b), "yes" if ok else "no",
                   ["%d %s into %d and %s into %d." % (k, "goes" if a % k == 0 else "does not go", a,
                                                       "goes" if b % k == 0 else "does not go", b)],
                   "yes / no")

    def t_groups():
        return _tb("%d boys and %d girls are put into teams. Every team has the same number of boys "
                   "and the same number of girls, with nobody left out. What is the greatest number "
                   "of teams?" % (a, b), max(common), "int", {"unit": "teams"},
                   ["The number of teams must divide %d and %d." % (a, b),
                    "The highest common factor is %d." % max(common)])

    def t_table():
        rows = [[a, ", ".join(map(str, _factors(a)))], [b, ", ".join(map(str, _factors(b)))]]
        return _dt("The table lists the factors of two numbers. What is their highest common factor?",
                   ["Number", "Factors"], rows, max(common),
                   ["The largest number in both lists is %d." % max(common)])

    return _pick_t([t_list, t_highest, t_count, t_is, t_groups], [t_table])


@skill("Y5.3.d", "Prime numbers to 100", S3)
def _(d=1):
    d = _d(d)

    def t_is():
        n = random.randint(2, _by(d, 19, 60, 100))
        p = n in PRIMES
        why = ("%d has exactly two factors, 1 and %d." % (n, n)) if p else \
              ("%d = %d × %d." % (n, _factors(n)[1], n // _factors(n)[1]))
        return _wq("Is %d a prime number? (yes or no)" % n, "yes" if p else "no", [why], "yes / no")

    def t_list_small():
        return _wq("Write all the prime numbers less than 20, separated by commas.",
                   "2, 3, 5, 7, 11, 13, 17, 19", ["A prime has exactly two factors."], "e.g. 2, 3, 5")

    def t_between():
        lo = random.randint(1, 8) * 10
        hi = lo + 10
        ps = [p for p in PRIMES if lo < p < hi]
        if not ps:
            return t_is()
        return _wq("List the prime numbers between %d and %d, separated by commas." % (lo, hi),
                   ", ".join(map(str, ps)), ["Check each odd number for factors."], "e.g. 11, 13")

    def t_odd_one():
        ps = random.sample([p for p in PRIMES if p < _by(d, 30, 60, 100)], 3)
        c = random.choice([n for n in range(9, _by(d, 30, 60, 100), 2) if n not in PRIMES])
        opts = ps + [c]
        random.shuffle(opts)
        return _tb("Which of these numbers is NOT prime?  %s" % ", ".join(map(str, opts)), c, "int", {},
                   ["%d = %d × %d." % (c, _factors(c)[1], c // _factors(c)[1])])

    def t_count():
        hi = pick([20, 30, 40, 50])
        return _tb("How many prime numbers are there less than %d?" % hi,
                   len([p for p in PRIMES if p < hi]), "int", {},
                   ["%s." % ", ".join(str(p) for p in PRIMES if p < hi)])

    def t_next():
        p = pick(PRIMES[:-1])
        nxt = PRIMES[PRIMES.index(p) + 1]
        return _tb("What is the next prime number after %d?" % p, nxt, "int", {},
                   ["Check %s." % ", ".join(str(x) for x in range(p + 1, nxt + 1))])

    def t_even():
        return _tb("Which is the only even prime number?", 2, "int", {},
                   ["Every other even number has 2 as a factor."])

    return _pick_t([t_is, t_is, t_list_small, t_between, t_odd_one, t_count, t_next, t_even])


@skill("Y5.3.e", "Prime factors and composite numbers", S3)
def _(d=1):
    d = _d(d)
    n = random.choice([x for x in range(_by(d, 6, 12, 30), _by(d, 40, 100, 200)) if len(_pf(x)) > 1])
    pf = _pf(n)

    def t_composite():
        k = random.randint(4, 60)
        return _wq("Is %d prime or composite? (type prime or composite)" % k,
                   "prime" if k in PRIMES else "composite",
                   ["A composite number has more than two factors."], "prime / composite")

    def t_prime_factors():
        u = sorted(set(pf))
        return _wq("List the PRIME factors of %d, smallest first, separated by commas (each one "
                   "once)." % n, ", ".join(map(str, u)),
                   ["%d = %s." % (n, " × ".join(map(str, pf)))], "e.g. 2, 3")

    def t_product():
        return _tb("%s = ?  (This is a product of prime factors.)" % " × ".join(map(str, pf)), n, "int",
                   {}, ["Multiply: %d." % n])

    def t_largest():
        return _tb("What is the largest prime factor of %d?" % n, max(pf), "int", {},
                   ["%d = %s." % (n, " × ".join(map(str, pf)))])

    def t_missing():
        k = random.randrange(len(pf))
        shown = " × ".join("___" if i == k else str(x) for i, x in enumerate(pf))
        return _tb("Complete the prime factorisation:  %d = %s" % (n, shown), pf[k], "int", {},
                   ["%d = %s." % (n, " × ".join(map(str, pf)))])

    def t_vocab():
        return _wq("A whole number greater than 1 with more than two factors is called what? "
                   "(one word)", "composite", ["Prime: exactly two factors. Composite: more than two."],
                   "one word")

    return _pick_t([t_composite, t_prime_factors, t_product, t_largest, t_missing, t_vocab])


def _pf(n):
    out, k = [], 2
    while n > 1:
        while n % k == 0:
            out.append(k)
            n //= k
        k += 1
    return out


@skill("Y5.3.f", "Square numbers and the ² notation", S3)
def _(d=1):
    d = _d(d)
    k = random.randint(_by(d, 2, 4, 8), _by(d, 10, 12, 15))

    def t_eval():
        return _tb("Work out %d²." % k, k * k, "int", {}, ["%d² = %d × %d = %d." % (k, k, k, k * k)])

    def t_root():
        return _tb("___² = %d. What is the missing number?" % (k * k), k, "int", {},
                   ["%d × %d = %d." % (k, k, k * k)])

    def t_is():
        n = random.randint(10, 150)
        sq = int(n ** 0.5) ** 2 == n
        return _wq("Is %d a square number? (yes or no)" % n, "yes" if sq else "no",
                   ["%d² = %d and %d² = %d." % (int(n ** 0.5), int(n ** 0.5) ** 2, int(n ** 0.5) + 1,
                                                (int(n ** 0.5) + 1) ** 2)], "yes / no")

    def t_area():
        return _area("This square is %d squares wide. What is its area in squares? (This is %d².)"
                     % (k, k), {"mode": "read_area", "rows": k, "cols": k}, k * k,
                     ["%d × %d = %d." % (k, k, k * k)]) if k <= 12 else t_eval()

    def t_between():
        a = random.randint(10, 80)
        b = a + random.randint(30, 60)
        sqs = [i * i for i in range(1, 16) if a < i * i < b]
        return _tb("How many square numbers are there between %d and %d?" % (a, b), len(sqs), "int", {},
                   ["%s." % (", ".join(map(str, sqs)) or "None")])

    def t_sum():
        a, b = random.sample(range(2, 10), 2)
        return _tb("Work out %d² + %d²." % (a, b), a * a + b * b, "int", {},
                   ["%d + %d = %d." % (a * a, b * b, a * a + b * b)])

    def t_next():
        return _tb("The square numbers go 1, 4, 9, 16, ... What is the %s square number?"
                   % _ordinal(k), k * k, "int", {}, ["%d² = %d." % (k, k * k)])

    return _pick_t([t_eval, t_root, t_is, t_between, t_sum, t_next], [t_area])


def _ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


@skill("Y5.3.g", "Cube numbers and the ³ notation", S3)
def _(d=1):
    d = _d(d)
    k = random.randint(_by(d, 1, 2, 4), _by(d, 5, 6, 10))

    def t_eval():
        return _tb("Work out %d³." % k, k ** 3, "int", {},
                   ["%d³ = %d × %d × %d = %d." % (k, k, k, k, k ** 3)])

    def t_root():
        return _tb("___³ = %d. What is the missing number?" % k ** 3, k, "int", {},
                   ["%d × %d × %d = %d." % (k, k, k, k ** 3)])

    def t_blocks():
        return _tb("A large cube is built from small 1 cm cubes. It is %d cubes long, %d wide and %d "
                   "tall. How many small cubes are used?" % (k, k, k), k ** 3, "int", {"unit": "cubes"},
                   ["%d × %d × %d = %d." % (k, k, k, k ** 3)])

    def t_is():
        n = pick([8, 27, 64, 125, 216, 9, 16, 36, 100, 81, 1000, 50])
        c = round(n ** (1 / 3)) ** 3 == n
        return _wq("Is %d a cube number? (yes or no)" % n, "yes" if c else "no",
                   ["%d³ = %d." % (round(n ** (1 / 3)), round(n ** (1 / 3)) ** 3)], "yes / no")

    def t_compare():
        a, b = random.randint(2, 6), random.randint(3, 12)
        x, y = a ** 3, b ** 2
        if x == y:
            return t_eval()
        return _tb("Which is larger, %d³ or %d²? Type its value." % (a, b), max(x, y), "int", {},
                   ["%d³ = %d and %d² = %d." % (a, x, b, y)])

    def t_both():
        return _tb("Which number below 100, other than 1, is both a square number and a cube number?",
                   64, "int", {}, ["64 = 8² = 4³."])

    return _pick_t([t_eval, t_root, t_blocks, t_is, t_compare, t_both])


@skill("Y5.3.h", "Problems with factors, multiples, squares and cubes", S3)
def _(d=1):
    d = _d(d)

    def t_rows():
        n = pick([24, 36, 48, 60, 72])
        k = pick([p for p in _pairs(n) if 2 < p[0]])
        return _tb("%d chairs are set out in equal rows of %d. How many rows are there?" % (n, k[0]),
                   k[1], "int", {"unit": "rows"}, ["%d ÷ %d = %d." % (n, k[0], k[1])])

    def t_buses():
        a, b = random.sample([4, 5, 6, 8, 10, 12], 2)
        lcm = a * b // _gcd(a, b)
        return _tb("One light flashes every %d seconds and another every %d seconds. They flash "
                   "together now. After how many seconds will they next flash together?" % (a, b), lcm,
                   "int", {"unit": "seconds"},
                   ["Multiples of %d: %s." % (a, ", ".join(str(a * i) for i in range(1, lcm // a + 1))),
                    "The first one in both lists is %d." % lcm])

    def t_square_garden():
        k = random.randint(4, 12)
        return _tb("A square patio is made of %d square tiles. How many tiles long is each side?"
                   % (k * k), k, "int", {"unit": "tiles"}, ["%d² = %d." % (k, k * k)])

    def t_think():
        k = random.randint(2, 9)
        clue = pick(["square", "cube"])
        f = (lambda x: x * x) if clue == "square" else (lambda x: x ** 3)
        v = f(k)
        lo = random.randint(f(k - 1) + 1, v - 1) if v - f(k - 1) > 1 else v - 1
        hi = random.randint(v + 1, f(k + 1) - 1)
        return _tb("I am a %s number between %d and %d. What am I?" % (clue, lo, hi), v, "int", {},
                   ["%d%s = %d is the only %s number in that range." % (k, "²" if clue == "square"
                                                                        else "³", v, clue)])

    def t_mystery():
        cands = [x for x in range(20, 60) if x % 3 == 0 and x % 4 == 0]
        n = pick(cands)
        return _tb("I am a multiple of 3 and of 4. I am between %d and %d. What am I?"
                   % (n - random.randint(1, 5), n + random.randint(1, 5)), n, "int", {},
                   ["Multiples of 12: 12, 24, 36, 48."]) if \
            sum(1 for x in cands if n - 5 <= x <= n + 5) == 1 else t_square_garden()

    def t_packs():
        a, b = random.sample([6, 8, 9, 10, 12], 2)
        lcm = a * b // _gcd(a, b)
        return _tb("Rolls come in packs of %d and sausages in packs of %d. What is the smallest number "
                   "of each you can buy so that there are the same number of rolls and sausages?"
                   % (a, b), lcm, "int", {}, ["The first common multiple of %d and %d is %d." % (a, b, lcm)])

    return _pick_t([t_rows, t_buses, t_square_garden, t_think, t_mystery, t_packs])
