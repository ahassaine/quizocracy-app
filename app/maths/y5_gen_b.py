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
    while a + b > 999999:                                 # Year 5 numbers go to 1,000,000
        a, b = _big(d), _big(d)
    if d == 0:
        b = random.randint(1000, 9999)

    def t_plain():
        return _tb("Work out %s + %s using the column method." % (_c(a), _c(b)), a + b, "int", {},
                   ["Line up the digits by place value and add from the ones.",
                    "%s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_three():
        c = random.randint(1000, 99999)
        if a + b + c > 999999:
            return t_plain()
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

    def t_strip():
        return _strip("The bar model shows two parts, %s and %s. What is the whole?" % (_c(a), _c(b)),
                      {"mode": "part_whole", "totalLabel": "?", "partLabel": _c(a), "unknown": "total", "parts": 2},
                      a + b, ["%s + %s = %s." % (_c(a), _c(b), _c(a + b))])

    def t_digit_of_answer():
        s = a + b
        place, name = pick([(1000, "thousands"), (100, "hundreds"), (10000, "ten thousands")])
        if s < place:
            return t_plain()
        return _tb("Work out %s + %s. What is the %s digit of the answer?" % (_c(a), _c(b), name), (s // place) % 10,
                   "int", {}, ["%s + %s = %s." % (_c(a), _c(b), _c(s)),
                               "The %s digit is %d." % (name, (s // place) % 10)])

    def t_mileage():
        start = random.randint(10000, 89999)
        trip = random.randint(120, 4999)
        return _tb("A car's mileometer showed %s miles. After a holiday it had gone %s more miles. What did it show then?"
                   % (_c(start), _c(trip)), start + trip, "int", {"unit": "miles"},
                   ["%s + %s = %s." % (_c(start), _c(trip), _c(start + trip))])

    def t_bar():
        cats = ["Jan", "Feb", "Mar", "Apr"]
        vals = [random.randint(11, 99) * 1000 + random.randint(0, 999) for _ in cats]
        i, j = random.sample(range(4), 2)
        return _bar("The chart shows how many people visited a theme park each month. How many visited in %s and %s "
                    "altogether?" % (cats[i], cats[j]), cats, vals, vals[i] + vals[j],
                    ["%s + %s = %s." % (_c(vals[i]), _c(vals[j]), _c(vals[i] + vals[j]))])

    def t_which_error():
        s = a + b
        wrong = s + pick([-1, 1]) * pick([1000, 10000, 100])
        if wrong <= 0:
            wrong = s + 1000
        first = random.random() < 0.5
        return _wq("Two pupils work out %s + %s. Ann gets %s and Ben gets %s. Who is right? (type Ann or Ben)"
                   % (_c(a), _c(b), _c(s if first else wrong), _c(wrong if first else s)), "Ann" if first else "Ben",
                   ["%s + %s = %s." % (_c(a), _c(b), _c(s))], "Ann or Ben")

    return _pick_t([t_plain, t_three, t_word, t_missing_digit, t_money, t_digit_of_answer, t_mileage, t_which_error],
                   [t_table, t_strip, t_bar])


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
        x = pick([random.randint(11, 98) * 2000, random.randint(6, 49) * 20000])
        return _tb("Halve %s." % _c(x), x // 2, "int", {}, ["%s ÷ 2 = %s." % (_c(x), _c(x // 2))])

    def t_sub_round():
        k = random.randint(1, 9) * pick([1000, 10000])
        b = base + k
        return _tb("Work out mentally: %s − %s" % (_c(b), _c(k)), base, "int", {},
                   ["Only the %s digit changes (with any exchange)." % ("thousands" if k < 10000 else "ten thousands")])

    def t_bridge():
        x = random.randint(1, 9) * 10000 - random.randint(1, 9) * 100
        k = random.randint(2, 9) * 100
        return _tb("Work out %s + %s. Hint: go to the next ten thousand first." % (_c(x), _c(k)), x + k, "int", {},
                   ["%s + %s = %s." % (_c(x), _c(-x % 10000), _c(x + (-x % 10000))),
                    "Then add the remaining %s: %s." % (_c(k - (-x % 10000)), _c(x + k))]) if k > -x % 10000 else t_add_round()

    def t_near_double():
        x = random.randint(11, 49) * 1000
        k = pick([1, 10, 100])
        return _tb("Work out %s + %s. Hint: use a double." % (_c(x), _c(x + k)), 2 * x + k, "int", {},
                   ["Double %s is %s." % (_c(x), _c(2 * x)), "Add %s more: %s." % (_c(k), _c(2 * x + k))])

    def t_count_up():
        x = random.randint(2, 8) * 10000 + random.randint(1, 9) * 100
        y = (x // 10000 + random.randint(1, 3)) * 10000 + random.randint(1, 9) * 100
        return _tb("Find the difference between %s and %s by counting up." % (_c(x), _c(y)), y - x, "int", {},
                   ["Count up from %s to %s, then to %s." % (_c(x), _c((x // 10000 + 1) * 10000), _c(y)),
                    "Difference: %s." % _c(y - x)])

    def t_which_method():
        k = random.randint(2, 9) * 1000
        off = pick([1, 10, 100])
        b = base + 10000
        good = "subtract %s, then add %s" % (_c(k), _c(off))
        bad = "subtract %s, then subtract %s" % (_c(k), _c(off))
        first = random.random() < 0.5
        return _wq("To work out %s − %s, which method is right? A: %s. B: %s. (type A or B)"
                   % (_c(b), _c(k - off), good if first else bad, bad if first else good), "A" if first else "B",
                   ["%s is %s less than %s, so you took away too much: add %s back." % (_c(k - off), _c(off), _c(k), _c(off))],
                   "A or B")

    return _pick_t([t_add_round, t_near, t_sub_near, t_bonds, t_double, t_half, t_sub_round, t_bridge,
                    t_near_double, t_count_up, t_which_method])


@skill("Y5.2.d", "Missing numbers and checking with the inverse", S2)
def _(d=1):
    d = _d(d)
    a, b = _big(d), random.randint(1000, 99999)
    a = min(a, 999999 - b)                                # keep a + b within 1,000,000

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
                   ["%s − %s = %s, which %s the first number, %s." % (_c(shown), _c(b), _c(shown - b),
                                                                        "matches" if ok else "does not match", _c(a))],
                   "yes / no")

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

    def t_which_check():
        s = a + b
        good = "%s − %s" % (_c(s), _c(b))
        bad = pick(["%s + %s" % (_c(s), _c(b)), "%s − %s" % (_c(b), _c(a))])
        first = random.random() < 0.5
        return _wq("Which calculation checks %s + %s = %s? A: %s   B: %s   (type A or B)"
                   % (_c(a), _c(b), _c(s), good if first else bad, bad if first else good), "A" if first else "B",
                   ["Subtraction undoes addition: %s should give %s." % (good, _c(a))], "A or B")

    def t_start_money():
        spent, left = random.randint(1000, 9000), random.randint(10000, 60000)
        return _tb("A club spent £%s on a minibus repair and had £%s left. How much did it have before the repair, in "
                   "pounds?" % (_c(spent), _c(left)), spent + left, "int", {"unit": "£"},
                   ["Undo the spending: %s + %s = %s." % (_c(left), _c(spent), _c(spent + left))])

    def t_strip():
        s = a + b
        return _strip("The bar model shows a whole of %s. One part is %s. What is the missing part?" % (_c(s), _c(a)),
                      {"mode": "part_whole", "totalLabel": _c(s), "partLabel": _c(a), "unknown": "part", "parts": 2},
                      b, ["%s − %s = %s." % (_c(s), _c(a), _c(b))])

    def t_table():
        xs = [random.randint(10000, 60000) for _ in range(3)]
        ks = [random.randint(1000, 30000) for _ in range(3)]
        rows = [[_c(x), _c(k), _c(x + k)] for x, k in zip(xs, ks)]
        r = random.randrange(3)
        c = pick([0, 1])
        ans = xs[r] if c == 0 else ks[r]
        return _dt("In each row, first number + second number = total. What belongs in the empty cell?",
                   ["First", "Second", "Total"], rows, ans,
                   ["%s − %s = %s." % (_c(xs[r] + ks[r]), _c(ks[r] if c == 0 else xs[r]), _c(ans))], missing=[r, c])

    def t_take_think():
        x = random.randint(20000, 90000)
        k = random.randint(1000, x - 1000)
        return _tb("%s thinks of a number and subtracts %s. The answer is %s. What was the number?"
                   % (_who(), _c(k), _c(x - k)), x, "int", {},
                   ["Undo it: %s + %s = %s." % (_c(x - k), _c(k), _c(x))])

    return _pick_t([t_add_missing, t_sub_missing_first, t_sub_missing_second, t_check,
                    t_inverse_fact, t_think, t_which_check, t_start_money, t_take_think], [t_strip, t_table])


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

    def t_train():
        start = random.randint(150, 400)
        off1, on1 = random.randint(20, 120), random.randint(20, 150)
        off2 = random.randint(10, start - off1 + on1 - 10)
        end = start - off1 + on1 - off2
        return _tb("A train leaves with %d passengers. At the first stop %d get off and %d get on. At the second stop "
                   "%d get off. How many passengers are on the train now?" % (start, off1, on1, off2), end, "int",
                   {"unit": "passengers"},
                   ["%d − %d + %d = %d." % (start, off1, on1, start - off1 + on1),
                    "%d − %d = %d." % (start - off1 + on1, off2, end)])

    def t_mountains():
        a, b, c = random.sample(range(2100, 8848), 3)
        names = ["Peak A", "Peak B", "Peak C"]
        hi, lo = max(a, b, c), min(a, b, c)
        return _dt("The table shows the heights of three mountains. How much higher is the tallest than the shortest, "
                   "in metres?", ["Mountain", "Height (m)"], [[n, _c(v)] for n, v in zip(names, (a, b, c))], hi - lo,
                   ["%s − %s = %s." % (_c(hi), _c(lo), _c(hi - lo))])

    def t_savings():
        goal = random.randint(30, 90) * 100
        have = random.randint(5, goal // 200) * 100
        gift = random.randint(2, 10) * 100
        return _tb("%s is saving £%s for a car. %s has £%s and is given £%s for a birthday. How much more is needed, in "
                   "pounds?" % (who, _c(goal), who, _c(have), _c(gift)), goal - have - gift, "int", {"unit": "£"},
                   ["%s + %s = %s." % (_c(have), _c(gift), _c(have + gift)),
                    "%s − %s = %s." % (_c(goal), _c(have + gift), _c(goal - have - gift))])

    def t_charity():
        a, b = random.randint(10000, 40000), random.randint(10000, 40000)
        total = a + b + random.randint(5000, 30000)
        return _tb("A charity run raised £%s in three weeks. It raised £%s in week 1 and £%s in week 2. How much did it "
                   "raise in week 3, in pounds?" % (_c(total), _c(a), _c(b)), total - a - b, "int", {"unit": "£"},
                   ["%s + %s = %s." % (_c(a), _c(b), _c(a + b)), "%s − %s = %s." % (_c(total), _c(a + b), _c(total - a - b))])

    def t_graph():
        yrs = ["2021", "2022", "2023", "2024", "2025"]
        v = [random.randint(20, 90) * 100 for _ in yrs]
        i, j = sorted(random.sample(range(5), 2))
        k = random.choice([x for x in range(5) if x not in (i, j)])
        ans = v[i] + v[j] - v[k]
        if ans <= 0:
            k, j = j, k
            ans = v[i] + v[j] - v[k]
        if ans <= 0:
            return t_train()
        return _lg("The graph shows how many tickets a theatre sold each year. Add the sales for %s and %s, then "
                   "subtract the sales for %s. What do you get?" % (yrs[i], yrs[j], yrs[k]), list(zip(yrs, v)), ans,
                   ["%s + %s − %s = %s." % (_c(v[i]), _c(v[j]), _c(v[k]), _c(ans))], "Tickets", "Year")

    return _pick_t([t_bank, t_three_days, t_compare_totals, t_journey, t_train, t_savings, t_charity],
                   [t_table, t_bar, t_mountains, t_graph])


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
        a, b = random.randint(100, 499) * u, random.randint(100, 499) * u
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

    def t_true_sub():
        a, b = random.randint(200, 999) * u, random.randint(10, 199) * u
        rhs = a - b if random.random() < 0.5 else a - b + pick([-1, 1]) * pick([u, 10 * u])
        return _wq("Is this number sentence true or false?  %s − %s = %s" % (_c(a), _c(b), _c(rhs)),
                   "true" if rhs == a - b else "false", ["%s − %s = %s." % (_c(a), _c(b), _c(a - b))], "true / false")

    def t_sign():
        a, b = random.randint(100, 900) * u, random.randint(10, 90) * u
        plus = random.random() < 0.5
        c = random.randint(10, 90) * u
        rhs = a + b - c if plus else a - b - c
        if rhs <= 0:
            plus, rhs = True, a + b - c
        return _wq("Which sign, + or −, goes in the gap?  %s ___ %s = %s + %s" % (_c(a), _c(b), _c(rhs), _c(c)),
                   "+" if plus else "-", ["The right side is %s." % _c(rhs + c),
                                          "%s %s %s = %s." % (_c(a), "+" if plus else "−", _c(b), _c(rhs + c))], "+ or −")

    def t_both_sides_sub():
        a, b = random.randint(30, 90) * u, random.randint(5, 25) * u
        c = random.randint(30, 90) * u
        if c + b - a <= 0 or c == a:
            c = a + random.randint(1, 9) * u
        return _tb("Make both sides equal:  %s + ___ = %s + %s" % (_c(a), _c(c), _c(b)), c + b - a, "int", {},
                   ["The right side is %s." % _c(c + b), "%s − %s = %s." % (_c(c + b), _c(a), _c(c + b - a))])

    def t_balance_word():
        a, b = random.randint(20, 60), random.randint(20, 60)
        c = random.randint(10, a + b - 10)
        return _tb("A balance has weights of %d g and %d g in one pan. The other pan has a weight of %d g. How many "
                   "more grams are needed in the second pan to balance?" % (a, b, c), a + b - c, "int", {"unit": "g"},
                   ["%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, a + b - c)])

    return _pick_t([t_balance_add, t_balance_sub, t_true, t_meaning, t_mixed, t_true_sub, t_sign, t_both_sides_sub,
                    t_balance_word])


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
        bad = random.sample([x for x in range(good - m + 1, good + 2 * m) if x % m], 2)
        opts = [good] + bad
        random.shuffle(opts)
        return _tb("Which of these is a multiple of %d?  %s" % (m, ", ".join(map(str, opts))), good,
                   "int", {}, ["%d ÷ %d = %d exactly." % (good, m, good // m)])

    def t_is():
        n = random.randint(20, 150)
        return _wq("Is %d a multiple of %d? (yes or no)" % (n, m), "yes" if n % m == 0 else "no",
                   ["%d ÷ %d = %d remainder %d." % (n, m, n // m, n % m)], "yes / no")

    def t_count():
        hi = random.randint(5, 10) * 10
        return _tb("How many multiples of %d are there from 1 to %d?" % (m, hi), hi // m, "int", {},
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

    def t_first_common():
        a, b = random.sample([2, 3, 4, 5, 6, 8, 9, 10], 2)
        lcm = a * b // _gcd(a, b)
        return _tb("What is the smallest number that is a multiple of both %d and %d?" % (a, b), lcm, "int", {},
                   ["Multiples of %d: %s." % (max(a, b), ", ".join(str(max(a, b) * i) for i in range(1, lcm // max(a, b) + 1))),
                    "%d is the first one that %d also divides." % (lcm, min(a, b))])

    def t_largest_below():
        n = random.randint(40, 300)
        if n % m == 0:
            n += 1
        return _tb("What is the largest multiple of %d that is less than %d?" % (m, n), (n // m) * m, "int", {},
                   ["%d ÷ %d = %d remainder %d." % (n, m, n // m, n % m), "%d × %d = %d." % (n // m, m, (n // m) * m)])

    def t_in_range():
        lo = random.randint(2, 10) * 10
        hi = lo + random.randint(3, 8) * 10
        ms = [x for x in range(lo + 1, hi) if x % m == 0]
        return _tb("How many multiples of %d are there between %d and %d? (Do not count %d or %d themselves.)" % (m, lo, hi, lo, hi), len(ms), "int", {},
                   ["They are %s." % (", ".join(map(str, ms)) or "none")])

    def t_rows():
        n = m * random.randint(4, 12)
        opts = [n, n + random.randint(1, m - 1), n - random.randint(1, m - 1)] if m > 2 else [n, n + 1, n - 1]
        random.shuffle(opts)
        return _tb("Chairs are put out in full rows of %d. Which of these could be the number of chairs?  %s"
                   % (m, ", ".join(map(str, opts))), n, "int", {},
                   ["The number must be a multiple of %d: %d ÷ %d = %d." % (m, n, m, n // m)])

    def t_set():
        pool = list(range(m * 2, m * 2 + 10 * m))
        nums = sorted(random.sample(pool, 8))
        ms = [x for x in nums if x % m == 0]
        if not ms:
            nums[0] = m * 3
            nums = sorted(set(nums))
            ms = [x for x in nums if x % m == 0]
        return _tb("Type all the multiples of %d in this list, separated by commas: %s" % (m, ", ".join(map(str, nums))),
                   ", ".join(map(str, ms)), "set", {"text": True, "placeholder": "e.g. 12, 18"},
                   ["%s %s divisible by %d." % (", ".join(map(str, ms)), "is" if len(ms) == 1 else "are", m)])

    def t_seq_gap():
        start = random.randint(2, 9)
        seq = [m * (start + i) for i in range(5)]
        k = random.randint(1, 3)
        return _tb("These are multiples of %d in order: %s. What is the missing number?"
                   % (m, ", ".join("___" if i == k else str(x) for i, x in enumerate(seq))), seq[k], "int", {},
                   ["Add %d each time: %d + %d = %d." % (m, seq[k - 1], m, seq[k])])

    def t_bus():
        mins = pick([5, 10, 12, 15, 20])
        t = mins * random.randint(2, 11)
        off = t + pick([0, 0, random.randint(1, mins - 1)])
        return _wq("A bus leaves the depot every %d minutes, starting at 9:00. Does a bus leave exactly %d minutes after "
                   "9:00? (yes or no)" % (mins, off), "yes" if off % mins == 0 else "no",
                   ["%d ÷ %d = %d remainder %d." % (off, mins, off // mins, off % mins)], "yes / no")

    def t_sum():
        a = m * random.randint(2, 9)
        b = m * random.randint(2, 9)
        return _wq("%d and %d are both multiples of %d. Is their sum a multiple of %d too? (yes or no)" % (a, b, m, m), "yes",
                   ["%d + %d = %d = %d × %d." % (a, b, a + b, m, (a + b) // m)], "yes / no") if random.random() < 0.5 else \
            _tb("%d and %d are both multiples of %d. Their sum is %d × ___. What is the missing number?" % (a, b, m, m),
                (a + b) // m, "int", {}, ["%d + %d = %d = %d × %d." % (a, b, a + b, m, (a + b) // m)])

    return _pick_t([t_list, t_which, t_is, t_count, t_nearest, t_both, t_first_common, t_largest_below, t_in_range,
                    t_rows, t_set, t_seq_gap, t_bus, t_sum], [t_table])


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
                   {}, ["%d ÷ 2 = %d." % (n, n // 2) if n % 2 == 0 else "Check the factor list."])

    def t_not_factor():
        fs = [k for k in _factors(n) if 1 < k < n]
        goods = random.sample(fs, min(3, len(fs)))
        bad = random.choice([k for k in range(3, n // 2) if n % k])
        opts = goods + [bad]
        random.shuffle(opts)
        return _tb("Which of these is NOT a factor of %d?  %s" % (n, ", ".join(map(str, opts))), bad, "int", {},
                   ["%d ÷ %d = %d remainder %d." % (n, bad, n // bad, n % bad)])

    def t_pair_sum():
        a, b = pick([p for p in _pairs(n) if p[0] > 1])
        others = [p for p in _pairs(n) if p[0] + p[1] == a + b]
        if len(others) > 1:
            return t_partner()
        return _tb("Two numbers multiply to make %d and add up to %d. What is the SMALLER of the two numbers?"
                   % (n, a + b), a, "int", {},
                   ["%d × %d = %d and %d + %d = %d." % (a, b, n, a, b, a + b)]) if a != b else t_partner()

    def t_who_am_i():
        k = pick([6, 8, 10, 12, 14, 15, 16, 18, 20, 21, 28])
        return _tb("My factors are %s. What number am I?" % ", ".join(map(str, _factors(k))), k, "int", {},
                   ["The largest factor of a number is the number itself: %d." % k])

    def t_set():
        return _tb("Type all the factors of %d, in any order, separated by commas." % n, ", ".join(map(str, _factors(n))),
                   "set", {"text": True, "placeholder": "e.g. 1, 2, 3"},
                   ["Factor pairs: %s." % ", ".join("%d × %d" % p for p in _pairs(n))])

    def t_teams():
        a, b = pick([p for p in _pairs(n) if p[0] > 1])
        return _tb("%d children are split into equal teams of %d with nobody left out. How many teams are there?"
                   % (n, a), b, "int", {"unit": "teams"}, ["%d ÷ %d = %d." % (n, a, b)])

    return _pick_t([t_all, t_count, t_partner, t_is_factor, t_pairs_count, t_largest, t_not_factor, t_pair_sum,
                    t_who_am_i, t_set, t_teams], [t_array, t_table])


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

    def t_not_common():
        fa = [k for k in _factors(a) if b % k]
        if not fa:
            return t_highest()
        bad = pick(fa)
        goods = random.sample(common, min(2, len(common)))
        opts = goods + [bad]
        random.shuffle(opts)
        return _tb("Which of these is NOT a common factor of %d and %d?  %s" % (a, b, ", ".join(map(str, opts))), bad,
                   "int", {}, ["%d is a factor of %d but not of %d." % (bad, a, b)])

    def t_tiles():
        return _tb("A floor is %d squares long and %d squares wide. It is covered with square tiles, each the same size, "
                   "with sides a whole number of squares and none cut. What is the largest side length the tiles can have?"
                   % (a, b), max(common), "int", {"unit": "squares"},
                   ["The side must divide %d and %d exactly." % (a, b), "The highest common factor is %d." % max(common)])

    def t_ribbons():
        return _tb("Two ribbons are %d cm and %d cm long. Both are cut into pieces that are all the same whole number "
                   "of cm, with nothing left over. What is the longest each piece can be, in cm?" % (a, b), max(common),
                   "int", {"unit": "cm"}, ["Common factors of %d and %d: %s." % (a, b, ", ".join(map(str, common)))])

    def t_set():
        return _tb("Type all the common factors of %d and %d, in any order, separated by commas." % (a, b),
                   ", ".join(map(str, common)), "set", {"text": True, "placeholder": "e.g. 1, 2, 4"},
                   ["Factors of %d: %s." % (a, ", ".join(map(str, _factors(a)))),
                    "Factors of %d: %s." % (b, ", ".join(map(str, _factors(b))))])

    def t_missing_list():
        fs = _factors(a)
        k = random.randint(1, len(fs) - 2)
        rows = [[a, ", ".join("?" if i == k else str(x) for i, x in enumerate(fs))]]
        return _dt("One factor of %d is missing from the list and shown as ?. Which factor is missing?" % a,
                   ["Number", "Factors"], rows, fs[k], ["%d × %d = %d." % (fs[k], a // fs[k], a)])

    def t_is_hcf():
        k = pick(common[1:] or common)
        right = k == max(common)
        return _wq("Is %d the HIGHEST common factor of %d and %d? (yes or no)" % (k, a, b), "yes" if right else "no",
                   ["Common factors: %s; the highest is %d." % (", ".join(map(str, common)), max(common))], "yes / no")

    def t_only_one():
        fa = [k for k in _factors(a) if b % k]
        return _tb("How many factors of %d are NOT factors of %d?" % (a, b), len(fa), "int", {},
                   ["Factors of %d: %s." % (a, ", ".join(map(str, _factors(a)))),
                    "Not factors of %d: %s." % (b, ", ".join(map(str, fa)) or "none")])

    def t_bags():
        return _tb("%d pencils and %d rubbers are shared into identical party bags with none left over. What is the "
                   "greatest number of bags that can be made?" % (a, b), max(common), "int", {"unit": "bags"},
                   ["The number of bags must divide %d and %d: the highest common factor is %d." % (a, b, max(common))])

    return _pick_t([t_list, t_highest, t_count, t_is, t_groups, t_not_common, t_tiles, t_ribbons, t_set, t_is_hcf,
                    t_only_one, t_bags], [t_table, t_missing_list])


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
        return _tb("Write all the prime numbers less than 20, separated by commas.",
                   "2, 3, 5, 7, 11, 13, 17, 19", "set", {"text": True, "placeholder": "e.g. 2, 3, 5"},
                   ["A prime has exactly two factors."])

    def t_between():
        lo = random.randint(1, 8) * 10
        hi = lo + 10
        ps = [p for p in PRIMES if lo < p < hi]
        if not ps:
            return t_is()
        return _tb("List the prime numbers between %d and %d, separated by commas." % (lo, hi),
                   ", ".join(map(str, ps)), "set", {"text": True, "placeholder": "e.g. 11, 13"},
                   ["Check each odd number for factors."])

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

    def t_smallest_factor():
        n = random.choice([x for x in range(15, _by(d, 50, 100, 100)) if x not in PRIMES and x % 2])
        return _tb("%d is not prime. What is its smallest factor other than 1?" % n, _factors(n)[1], "int", {},
                   ["%d = %d × %d." % (n, _factors(n)[1], n // _factors(n)[1])])

    def t_largest_below():
        n = random.randint(20, 100)
        p = max(q for q in PRIMES if q < n)
        return _tb("What is the largest prime number less than %d?" % n, p, "int", {},
                   ["Check downwards from %d: %d is prime." % (n - 1, p)])

    def t_two_primes():
        p, q = random.sample([x for x in PRIMES if x < 40], 2)
        return _tb("%d and %d are both prime. What is their sum?" % (p, q), p + q, "int", {},
                   ["%d + %d = %d." % (p, q, p + q)])

    def t_set():
        nums = random.sample(range(2, _by(d, 30, 60, 100)), 7)
        ps = [x for x in nums if x in PRIMES]
        if not ps:
            nums[0] = pick([x for x in PRIMES if x < 30])
            ps = [x for x in nums if x in PRIMES]
        return _tb("Type every prime number in this list, separated by commas: %s" % ", ".join(map(str, nums)),
                   ", ".join(map(str, ps)), "set", {"text": True, "placeholder": "e.g. 7, 13"},
                   ["%s." % "; ".join("%d %s" % (x, "is prime" if x in PRIMES else "= %d × %d" % (_factors(x)[1], x // _factors(x)[1]))
                                      for x in nums)])

    def t_table():
        nums = random.sample(range(10, _by(d, 40, 80, 100)), 4)
        rows = [[x, ", ".join(map(str, _factors(x)))] for x in nums]
        ps = [x for x in nums if x in PRIMES]
        return _dt("The table lists the factors of four numbers. How many of the numbers are prime?",
                   ["Number", "Factors"], rows, len(ps),
                   ["A prime has exactly two factors.", "Prime: %s." % (", ".join(map(str, ps)) or "none")])

    def t_sum_sentence():
        n = pick([x for x in range(10, 60, 2)])
        ways = [(p, n - p) for p in PRIMES if p <= n - p and (n - p) in PRIMES]
        if not ways:
            return t_is()
        return _tb("How many different ways can %d be written as the sum of two prime numbers? (Count 3 + 7 and 7 + 3 as "
                   "the same way.)" % n, len(ways), "int", {},
                   ["%s." % ", ".join("%d + %d" % w for w in ways)])

    return _pick_t([t_is, t_is, t_list_small, t_between, t_odd_one, t_count, t_next, t_even, t_smallest_factor,
                    t_largest_below, t_two_primes, t_set, t_sum_sentence], [t_table])


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

    def t_how_many():
        return _tb("%d written as a product of prime numbers is %s. How many prime numbers are multiplied together (count "
                   "repeats)?" % (n, " × ".join(map(str, pf))), len(pf), "int", {}, ["Count them: %d." % len(pf)])

    def t_next_composite():
        k = pick([p for p in PRIMES if 10 < p < 90])
        nxt = k + 1
        return _tb("What is the first composite number after %d?" % k, nxt, "int", {},
                   ["%d is even, so it is composite." % nxt])

    def t_is_pf():
        q = pick([2, 3, 5, 7, 11])
        ok = n % q == 0
        return _wq("Is %d a prime factor of %d? (yes or no)" % (q, n), "yes" if ok else "no",
                   ["%d = %s." % (n, " × ".join(map(str, pf)))], "yes / no")

    def t_tree():
        rows = []
        m = n
        for p in pf[:-1]:
            rows.append([m, "%d × %d" % (p, m // p)])
            m //= p
        k = 0                                   # later rows would give the hidden number away
        ans = rows[k][0]
        rows[k][0] = ""
        return _dt("This table is a factor tree written as steps: each number splits into a prime × what is left. What "
                   "number did the tree start with?", ["Number", "Split"], rows, ans,
                   ["%s = %d." % (rows[k][1], ans)], missing=[k, 0])

    def t_count_composite():
        lo = random.randint(1, 8) * 10
        cs = [x for x in range(lo + 1, lo + 10) if x not in PRIMES]
        return _tb("How many composite numbers are there between %d and %d? (Do not count %d or %d themselves.)" % (lo, lo + 10, lo, lo + 10), len(cs), "int", {},
                   ["Composite: %s." % ", ".join(map(str, cs))])

    return _pick_t([t_composite, t_prime_factors, t_product, t_largest, t_missing, t_vocab, t_how_many,
                    t_next_composite, t_is_pf, t_count_composite], [t_tree])


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
        return _tb("How many square numbers are there between %d and %d? (Do not count %d or %d themselves.)" % (a, b, a, b), len(sqs), "int", {},
                   ["%s." % (", ".join(map(str, sqs)) or "None")])

    def t_sum():
        a, b = random.sample(range(2, 10), 2)
        return _tb("Work out %d² + %d²." % (a, b), a * a + b * b, "int", {},
                   ["%d + %d = %d." % (a * a, b * b, a * a + b * b)])

    def t_next():
        return _tb("The square numbers go 1, 4, 9, 16, ... What is the %s square number?"
                   % _ordinal(k), k * k, "int", {}, ["%d² = %d." % (k, k * k)])

    def t_gap():
        return _tb("What is the difference between %d² and %d²?" % (k + 1, k), (k + 1) ** 2 - k * k, "int", {},
                   ["%d − %d = %d." % ((k + 1) ** 2, k * k, (k + 1) ** 2 - k * k)])

    def t_largest_below():
        n = random.randint(20, 200)
        r = int(n ** 0.5)
        if r * r == n:
            n += 1
        return _tb("What is the largest square number less than %d?" % n, r * r, "int", {},
                   ["%d² = %d and %d² = %d." % (r, r * r, r + 1, (r + 1) ** 2)])

    def t_tiles():
        return _tb("A square chessboard-style floor has %d tiles along each side. How many tiles cover the whole floor?"
                   % k, k * k, "int", {"unit": "tiles"}, ["%d² = %d × %d = %d." % (k, k, k, k * k)])

    def t_table():
        ks = random.sample(range(2, 13), 4)
        rows = [[x, x * x] for x in ks]
        i = random.randrange(4)
        return _io("Each Out number is the In number squared. What goes in the empty cell?", rows, i, ks[i] ** 2,
                   ["%d² = %d." % (ks[i], ks[i] ** 2)], rule="squared")

    def t_side_from_area():
        return _tb("A square has an area of %d cm². How long is each side, in cm?" % (k * k), k, "int", {"unit": "cm"},
                   ["%d × %d = %d." % (k, k, k * k)])

    return _pick_t([t_eval, t_root, t_is, t_between, t_sum, t_next, t_gap, t_largest_below, t_tiles, t_side_from_area],
                   [t_area, t_table])


def _ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


@skill("Y5.3.g", "Cube numbers and the ³ notation", S3)
def _(d=1):
    d = _d(d)
    k = random.randint(2, _by(d, 5, 6, 10))

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

    def t_gap():
        return _tb("What is the difference between %d³ and %d³?" % (k + 1, k), (k + 1) ** 3 - k ** 3, "int", {},
                   ["%d − %d = %d." % ((k + 1) ** 3, k ** 3, (k + 1) ** 3 - k ** 3)])

    def t_sum():
        a, b = random.sample(range(1, 6), 2)
        return _tb("Work out %d³ + %d³." % (a, b), a ** 3 + b ** 3, "int", {},
                   ["%d + %d = %d." % (a ** 3, b ** 3, a ** 3 + b ** 3)])

    def t_smallest_above():
        n = random.randint(10, 900)
        r = 1
        while r ** 3 <= n:
            r += 1
        return _tb("What is the smallest cube number greater than %d?" % n, r ** 3, "int", {},
                   ["%d³ = %d and %d³ = %d." % (r - 1, (r - 1) ** 3, r, r ** 3)])

    def t_table():
        ks = random.sample(range(1, 11), 4)
        rows = [[x, x ** 3] for x in ks]
        i = random.randrange(4)
        return _io("Each Out number is the In number cubed. What goes in the empty cell?", rows, i, ks[i] ** 3,
                   ["%d³ = %d × %d × %d = %d." % (ks[i], ks[i], ks[i], ks[i], ks[i] ** 3)], rule="cubed")

    def t_edge():
        return _tb("A cube is built from %d small 1 cm cubes. How many small cubes long is each edge?" % k ** 3, k, "int",
                   {"unit": "cubes"}, ["%d × %d × %d = %d." % (k, k, k, k ** 3)])

    def t_notation():
        return _tb("%d³ means %d × %d × %d. What is its value?" % (k, k, k, k), k ** 3, "int", {},
                   ["%d × %d = %d; × %d = %d." % (k, k, k * k, k, k ** 3)])

    return _pick_t([t_eval, t_root, t_blocks, t_is, t_compare, t_both, t_gap, t_sum, t_smallest_above, t_edge,
                    t_notation], [t_table])


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
        return _tb("Rolls come in packs of %d and sausages in packs of %d. You want exactly the same number of "
                   "rolls as sausages. What is the smallest number of rolls you can buy?"
                   % (a, b), lcm, "int", {}, ["The first common multiple of %d and %d is %d." % (a, b, lcm)])

    def t_prime_age():
        lo = random.randint(20, 85)
        ps = [p for p in PRIMES if lo < p < lo + 6]
        if len(ps) != 1:
            return t_rows()
        return _tb("My grandad's age is a prime number. He is older than %d but younger than %d. How old is he?"
                   % (lo, lo + 6), ps[0], "int", {"unit": "years"},
                   ["Check %s: only %d is prime." % (", ".join(map(str, range(lo + 1, lo + 6))), ps[0])])

    def t_class_size():
        a, b = random.sample([3, 4, 5, 6, 8], 2)
        lcm = a * b // _gcd(a, b)
        k = random.randint(1, 3)
        n = lcm * k
        lo, hi = n - random.randint(1, lcm - 1), n + random.randint(1, lcm - 1)
        if sum(1 for x in range(lo + 1, hi) if x % lcm == 0) != 1 or lo < 1:
            return t_buses()
        return _tb("A group of children can stand in equal rows of %d or in equal rows of %d with nobody left over. There "
                   "are more than %d and fewer than %d children. How many children are there?" % (a, b, lo, hi), n,
                   "int", {}, ["The number must be a common multiple of %d and %d: a multiple of %d." % (a, b, lcm),
                               "Between %d and %d that is %d." % (lo, hi, n)])

    def t_cube_tower():
        k = random.randint(3, 6)
        return _tb("%s builds a cube from small cubes, %d along each edge, then takes away one small cube from each "
                   "corner. How many small cubes are left?" % (_who(), k), k ** 3 - 8, "int", {"unit": "cubes"},
                   ["%d³ = %d." % (k, k ** 3), "A cube has 8 corners: %d − 8 = %d." % (k ** 3, k ** 3 - 8)])

    def t_square_and_prime():
        sq = pick([4, 9, 16, 25, 36, 49])
        p = pick(PRIMES[:8])                        # primes to 19, which Year 5 recall
        return _tb("I am the sum of a square number and a prime number. The square number is %d and the prime is the "
                   "%s prime number. What am I?" % (sq, _ordinal(PRIMES.index(p) + 1)), sq + p, "int", {},
                   ["The %s prime is %d." % (_ordinal(PRIMES.index(p) + 1), p), "%d + %d = %d." % (sq, p, sq + p)])

    def t_area_square():
        k = random.randint(3, 12)
        cost = random.randint(2, 9)
        return _tb("A square patio is %d m long on each side. Paving costs £%d for each m². How much does it cost to pave, "
                   "in pounds?" % (k, cost), k * k * cost, "int", {"unit": "£"},
                   ["Area: %d² = %d m²." % (k, k * k), "%d × %d = %d." % (k * k, cost, k * k * cost)])

    return _pick_t([t_rows, t_buses, t_square_garden, t_think, t_mystery, t_packs, t_prime_age, t_class_size,
                    t_cube_tower, t_square_and_prime, t_area_square])
