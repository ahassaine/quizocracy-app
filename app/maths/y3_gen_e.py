# Year 3: extra framings for existing skills, and three skills the curriculum asks for that
# the bank lacked (Y3.3.h subtracting ones/tens/hundreds mentally, Y3.5.g scaling and
# correspondence problems, Y3.8.o 12- and 24-hour clocks).
#
# Extra framings are merged into a skill with _more(key, n_orig, builder): the builder takes the
# difficulty and returns its framings (visual ones listed twice); the original generator stays
# in y3_gen_a..d and is drawn with weight n_orig, roughly how many framings it already has.
from .maths_engine import skill, GENERATORS, call_generator, n_words, money, pick, NAMES
from .y3_gen_c import _hm, _frac_words, _a, _pl
from .y5_common import random, Fraction, _d, _by, _pick_t, _tb, _wq, _fq, _nl, _nld, _io, _dt, _bar, _strip

S3 = "3.3 Addition & subtraction (3-digit)"
S5 = "3.5 Multiplication & division (calculating)"
S8 = "3.8 Time & geometry"


def _more(key, n_orig, builder):
    orig = GENERATORS[key]

    def gen(d=1):
        d = _d(d)
        extra = builder(d)
        k = random.randrange(n_orig + len(extra))
        return call_generator(orig, d) if k < n_orig else extra[k - n_orig]()
    GENERATORS[key] = gen


# ------------------------------------------------------------- builders ----
def _bt(prompt, ans, solution):
    return {"prompt": prompt, "component": "base_ten", "spec": {"mode": "build", "max": 9},
            "answer": int(ans), "answer_type": "int", "solution": solution}


def _eg(prompt, groups, per, ans, solution):
    return {"prompt": prompt, "component": "equal_groups",
            "spec": {"mode": "read", "groups": int(groups), "per": int(per)},
            "answer": ans, "answer_type": "int", "solution": solution}


def _pict(prompt, cats, vals, key, symbol, ans, solution):
    return {"prompt": prompt, "component": "pictogram",
            "spec": {"categories": list(cats), "values": [int(v) for v in vals], "key": int(key), "symbol": symbol},
            "answer": ans, "answer_type": "int", "solution": solution}


def _ruler(prompt, mode, value, mx, unit, ans, solution):
    return {"prompt": prompt, "component": "ruler",
            "spec": {"mode": mode, "value": int(value), "max": int(mx), "unit": unit},
            "answer": ans, "answer_type": "int", "solution": solution}


def _clock(prompt, h, m, solution):
    return {"prompt": prompt, "component": "clock", "spec": {"mode": "set"},
            "answer": _hm(h, m), "answer_type": "time", "solution": solution}


def _time(prompt, h, m, solution):
    """A typed 12-hour time answer like 4:05 (a.m./p.m. not needed)."""
    return _tb(prompt, _hm(h, m), "time", {"text": True, "placeholder": "e.g. 4:05"}, solution)


def _split(m):
    """Minutes after midnight -> (h, m) on a 12-hour clock face."""
    return (m // 60) % 12 or 12, m % 60


def _lst(xs):
    return ", ".join(str(x) for x in xs)


def _and(xs):
    """['a', 'b', 'c'] -> 'a, b and c'."""
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _r10(n):
    return ((int(n) + 5) // 10) * 10


def _r100(n):
    return ((int(n) + 50) // 100) * 100


def _tf(stmt, true, solution):
    return _wq("True or false: %s (type true or false)" % stmt, "true" if true else "false", solution, "true / false")


def _yn(prompt, yes, solution):
    return _wq(prompt + " (type yes or no)", "yes" if yes else "no", solution, "yes / no")


def _u(k, place):
    """'1 ten' / '3 tens' for place = 'hundreds', 'tens' or 'ones'."""
    return "%d %s" % (k, place[:-1] if k == 1 else place)


_SCHOOLS = ["Oak", "Elm", "Ash", "Birch", "Willow", "Maple"]


# ================================================================ 3.0 ======
def _x30c(d):
    lo, hi = (11, 98) if d == 0 else (101, 998)

    def t_one_more_less():
        step = 1 if d == 0 else pick([1, 100])
        up = random.random() < 0.5
        n = random.randint(lo + 1, hi - 1) if step == 1 else random.randint(200 if not up else 101, 899 if up else 998)
        ans = n + step if up else n - step
        return _wq("What is %d %s than %d? Write your answer in words." % (step, "more" if up else "less", n), n_words(ans),
                   ["%d %s %d = %d." % (n, "+" if up else "−", step, ans), "In words: %s." % n_words(ans)], "type the words")

    def t_regroup():
        if d == 0:
            t, o = random.randint(1, 7), random.randint(10, 19)
            n, desc = 10 * t + o, "%s and %d ones" % (_u(t, "tens"), o)
        elif d == 1:
            h, o = random.randint(1, 9), random.randint(1, 9)
            n, desc = 100 * h + o, "%s and %s (and no tens)" % (_u(h, "hundreds"), _u(o, "ones"))
        else:
            h, t = random.randint(1, 7), random.randint(10, 19)
            n, desc = 100 * h + 10 * t, "%s and %d tens" % (_u(h, "hundreds"), t)
        return _wq("Write in words the number made from %s." % desc, n_words(n),
                   ["Put the parts together: the number is %d." % n, "In words: %s." % n_words(n)], "type the words")

    def t_sum():
        if d == 0:
            parts = [10 * random.randint(2, 9), random.randint(1, 9)]
        else:
            parts = [100 * random.randint(1, 9), 10 * random.randint(0, 9), random.randint(0, 9)]
            parts = [p for p in parts if p] if parts[1] or parts[2] else parts[:1] + [random.randint(1, 9)]
        n = sum(parts)
        return _wq("Work out %s and write the answer in words." % " + ".join(str(p) for p in parts), n_words(n),
                   ["%s = %d." % (" + ".join(str(p) for p in parts), n), "In words: %s." % n_words(n)], "type the words")

    def t_mistake():
        who = pick(NAMES)
        if d == 0:
            o = random.randint(3, 9)
            n, wrong = 10 + o, n_words(10 * o)
        else:
            h, o = random.randint(1, 9), random.randint(1, 9)
            n, wrong = 100 * h + o, n_words(100 * h + 10 * o)
        return _wq("%s wrote '%s' for the number %d. That is wrong. Write %d correctly in words." % (who, wrong, n, n, ),
                   n_words(n), ["'%s' is the number %d." % (wrong, n + (9 * (n % 10) if d else 10 * (n % 10) - n)),
                                "%d in words is %s." % (n, n_words(n))], "type the words")

    def t_halfway():
        if d == 0:
            a = 10 * random.randint(1, 8)
            b = a + 20
        elif d == 1:
            a = 100 * random.randint(1, 8)
            b = a + 100
        else:
            a = 10 * random.randint(11, 97)
            b = a + 20
        m = (a + b) // 2
        return _wq("Which number is exactly halfway between %d and %d? Write it in words." % (a, b), n_words(m),
                   ["Halfway between %d and %d is %d." % (a, b, m), "In words: %s." % n_words(m)], "type the words")

    def t_cards():
        k = 2 if d == 0 else 3
        while True:
            ds = random.sample(range(0, 10), k)
            if d == 2 and 0 not in ds:
                ds[0] = 0
            big = int("".join(str(x) for x in sorted(ds, reverse=True)))
            small_digits = sorted(ds)
            if small_digits[0] == 0:
                first = next(x for x in small_digits if x)
                small_digits.remove(first)
                small_digits = [first] + small_digits
            small = int("".join(str(x) for x in small_digits))
            if big >= 10 ** (k - 1):
                break
        want_big = random.random() < 0.5
        n = big if want_big else small
        return _wq("Use each of the digit cards %s once to make the %s %d-digit number you can. Write it in words."
                   % (_lst(ds), "largest" if want_big else "smallest", k), n_words(n),
                   ["The %s number is %d." % ("largest" if want_big else "smallest", n), "In words: %s." % n_words(n)],
                   "type the words")

    def t_table():
        ns = random.sample(range(lo, hi + 1), 3)
        miss = random.randrange(3)
        rows = [[str(n), n_words(n)] for n in ns]
        return _dt("Complete the table: type the words for the number with the missing cell.", ["Digits", "Words"], rows,
                   n_words(ns[miss]), ["%d in words is %s." % (ns[miss], n_words(ns[miss]))], missing=(miss, 1),
                   atype="str", placeholder="type the words")

    return [t_one_more_less, t_regroup, t_sum, t_mistake, t_halfway, t_cards, t_table, t_table]


def _x30f(d):
    three = d >= 1

    def num():
        return random.randint(101, 999) if three else random.randint(11, 99)

    def t_total_tens():
        n = 10 * (random.randint(11, 99) if three else random.randint(2, 9))
        return _tb("How many tens are there altogether in %d?" % n, n // 10, "int", {},
                   ["%d = %d tens." % (n, n // 10)] if three else ["%d is %d tens." % (n, n // 10)])

    def t_largest():
        ds = random.sample(range(1, 10), 3 if three else 2)
        big = sorted(ds, reverse=True)
        place, val = ("hundreds", big[0] * 100) if three else ("tens", big[0] * 10)
        n = int("".join(str(x) for x in big))
        return _tb("Make the largest number you can with the digits %s, using each once. What is the value of the "
                   "digit in the %s place?" % (_lst(ds), place), val, "int", {},
                   ["The largest number is %d." % n, "Its %s digit is worth %d." % (place, val)])

    def t_change():
        n = num()
        pos, place = (100, "hundreds") if (three and random.random() < 0.5) else (10, "tens")
        old = (n // pos) % 10
        new = random.choice([x for x in range(10) if x != old and not (pos == 100 and x == 0)])
        m = n + (new - old) * pos
        up = m > n
        return _tb("The %s digit of %d changes from %d to %d. By how much does the number %s?"
                   % (place, n, old, new, "increase" if up else "decrease"), abs(m - n), "int", {},
                   ["%d becomes %d." % (n, m), "The difference is %d." % abs(m - n)])

    def t_missing():
        n = num()
        while (n // 10) % 10 == 0 or n % 10 == 0:
            n = num()
        pos = random.choice([100, 10] if three else [10, 1])
        val = (n // pos) % 10 * pos
        return _tb("Find the missing number:  %d − ___ = %d" % (n, n - val), val, "int", {},
                   ["The answer has lost the %s digit." % {100: "hundreds", 10: "tens", 1: "ones"}[pos],
                    "That digit is worth %d." % val])

    def t_sum_values():
        n = num()
        while n // 10 % 10 == 0 or n % 10 == 0:
            n = num()
        if three:
            a, b = n // 100 * 100, n % 10
            return _tb("In %d, add the value of the hundreds digit and the value of the ones digit. What do you get?" % n, a + b, "int", {},
                       ["The values are %d and %d." % (a, b), "%d + %d = %d." % (a, b, a + b)])
        a, b = n // 10 * 10, n % 10
        return _tb("In %d, what is the difference between the value of the tens digit and the value of the ones digit?" % n, a - b,
                   "int", {}, ["The values are %d and %d." % (a, b), "%d − %d = %d." % (a, b, a - b)])

    def t_chart():
        n = num()
        while len(set(str(n))) < len(str(n)):
            n = num()
        heads = ["Hundreds", "Tens", "Ones"] if three else ["Tens", "Ones"]
        pos, place = pick([(100, "Hundreds"), (10, "Tens"), (1, "Ones")] if three else [(10, "Tens"), (1, "Ones")])
        val = (n // pos) % 10 * pos
        return _dt("This place value chart shows a number. What is the value of the digit in the %s column?" % place,
                   heads, [list(str(n))], val, ["The digit %d is in the %s column." % ((n // pos) % 10, place.lower()),
                                                 "It is worth %d." % val])

    return [t_total_tens, t_largest, t_change, t_missing, t_sum_values, t_chart, t_chart]


# ================================================================ 3.1 ======
def _x31a(d):
    lo, hi = (11, 99) if d == 0 else (101, 999)

    def t_box_digit():
        while True:
            if d == 0:
                o, b = random.randint(0, 9), random.randint(25, 85)
                ok = [x for x in range(1, 10) if 10 * x + o > b]
                shown, val = "□%d" % o, None
            else:
                h, o = random.randint(1, 9), random.randint(0, 9)
                b = 100 * h + random.randint(20, 89)
                ok = [x for x in range(0, 10) if 100 * h + 10 * x + o > b]
                shown = "%d□%d" % (h, o)
            if ok and ok[0] > (1 if d == 0 else 0):
                break
        return _tb("%s > %d. What is the smallest digit that can go in the box?" % (shown, b), ok[0], "int", {},
                   ["Try the digits in order.", "%s is the first that is greater than %d." % (shown.replace("□", str(ok[0])), b)])

    def t_words():
        n = random.randint(lo, hi)
        s = str(n)
        while len(set(s)) < len(s):
            n = random.randint(lo, hi)
            s = str(n)
        m = int(s[0] + s[2] + s[1]) if len(s) == 3 else int(s[1] + s[0])
        if m < 10:
            m += 10 * random.randint(1, 9)
        big = max(n, m)
        return _tb("Which is greater: %s or %d? Type the greater number in digits." % (n_words(n), m), big, "int", {},
                   ["%s is %d." % (n_words(n).capitalize(), n), "%d is greater." % big])

    def t_true_false():
        a = random.randint(lo, hi)
        s = str(a)
        b = int(s[::-1]) if s[-1] != "0" else a + random.randint(1, 9)
        if b == a:
            b = a + 10
        sign = pick(["<", ">"])
        truth = a < b if sign == "<" else a > b
        return _tf("%d %s %d" % (a, sign, b), truth, ["Compare the %s first." % ("tens" if d == 0 else "hundreds"),
                                                       "%d is %s than %d." % (a, "less" if a < b else "greater", b)])

    def t_table():
        k = 4
        schools = random.sample(_SCHOOLS, k)
        h = random.randint(1, 8)
        vals = random.sample(range(h * 100 + 5, h * 100 + 199), k) if d else random.sample(range(20, 99), k)
        most = random.random() < 0.5
        tgt = vals.index(max(vals) if most else min(vals))
        return _dt("The table shows how many pupils are at four schools. Which school has the %s pupils? (type the name)"
                   % ("most" if most else "fewest"), ["School", "Pupils"], [[s, v] for s, v in zip(schools, vals)],
                   schools[tgt], ["Compare the numbers place by place.", "%s has %d." % (schools[tgt], vals[tgt])],
                   atype="str", placeholder="school name")

    def t_bars():
        cats = random.sample(["Class 3A", "Class 3B", "Class 3C", "Class 3D"], 3)
        while True:
            vals = [random.randint(2, 9) * (10 if d == 0 else 100) for _ in cats]
            if len(set(vals)) == 3:
                break
        most = random.random() < 0.5
        tgt = vals.index(max(vals) if most else min(vals))
        return {"prompt": "The bar chart shows how many cans each class collected. Which class collected the %s? "
                          "(type the class, like 3B)" % ("most" if most else "fewest"),
                "component": "bar_chart", "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": cats[tgt].replace("Class ", ""), "answer_type": "str",
                "solution": ["The %s bar is %s." % ("tallest" if most else "shortest", cats[tgt]),
                             "%s collected %d cans." % (cats[tgt], vals[tgt])]}

    def t_build_between():
        n = random.randint(lo + 1, min(hi - 1, 999 if d else 98))
        return _bt("Build the number that is greater than %d and less than %d." % (n - 1, n + 1), n,
                   ["The only whole number between %d and %d is %d." % (n - 1, n + 1, n)])

    def t_count_between():
        a = random.randint(lo, hi - 20)
        gap = random.randint(3, _by(d, 8, 12, 20))
        b = a + gap
        return _tb("How many whole numbers are greater than %d and less than %d?" % (a, b), gap - 1, "int", {},
                   ["They are %d to %d." % (a + 1, b - 1), "That is %d numbers." % (gap - 1)])

    return [t_box_digit, t_words, t_true_false, t_count_between, t_table, t_table, t_bars, t_bars,
            t_build_between, t_build_between]


def _x31c(d):
    lo, hi = (11, 99) if d == 0 else (101, 989)

    def num():
        n = random.randint(lo, hi)
        return n if n % 10 else n + random.randint(1, 4)

    def t_ruler():
        v = random.randint(11, 29)
        while v % 10 == 0:
            v = random.randint(11, 29)
        thing = pick(["ribbon", "pencil case", "strip of card"])
        return _ruler("Measure the %s with the ruler, then round its length to the nearest 10 cm." % thing,
                      "length", v, 30, "cm", _r10(v), ["The %s is %d cm long." % (thing, v),
                                                       "%d cm rounds to %d cm." % (v, _r10(v))])

    def t_count():
        r = 10 * random.randint(2, 9 if d == 0 else 98)
        return _tb("How many whole numbers round to %d when rounded to the nearest 10?" % r, 10, "int", {},
                   ["%d to %d all round to %d." % (r - 5, r + 4, r), "That is 10 numbers."])

    def t_table():
        ns = random.sample(range(lo, hi + 1), 3)
        miss = random.randrange(3)
        return _dt("Complete the table: round each number to the nearest 10.", ["Number", "Nearest 10"],
                   [[n, _r10(n)] for n in ns], _r10(ns[miss]),
                   ["The ones digit of %d is %d." % (ns[miss], ns[miss] % 10), "%d rounds to %d." % (ns[miss], _r10(ns[miss]))],
                   missing=(miss, 1))

    def t_true_false():
        n = num()
        claim = pick([_r10(n), _r10(n) + 10 if n % 10 < 5 else _r10(n) - 10])
        return _tf("%d rounded to the nearest 10 is %d." % (n, claim), claim == _r10(n),
                   ["The ones digit is %d, so round %s." % (n % 10, "up" if n % 10 >= 5 else "down"),
                    "%d rounds to %d." % (n, _r10(n))])

    def t_sum():
        a, b = (random.randint(11, 49), random.randint(11, 49)) if d == 0 else (random.randint(101, 499), random.randint(11, 99))
        s = a + b
        return _tb("Work out %d + %d, then round the answer to the nearest 10." % (a, b), _r10(s), "int", {},
                   ["%d + %d = %d." % (a, b, s), "%d rounds to %d." % (s, _r10(s))])

    def t_money():
        p = random.randint(11, 99)
        while p % 10 == 0:
            p = random.randint(11, 99)
        thing = pick(["comic", "pencil", "apple", "bag of crisps"])
        return _tb("%s costs %dp. Round the price to the nearest 10p, in pence." % (_a(thing).capitalize(), p), _r10(p), "int",
                   {"unit": "p"}, ["The ones digit is %d." % (p % 10), "%dp rounds to %dp." % (p, _r10(p))])

    return [t_count, t_true_false, t_sum, t_money, t_ruler, t_ruler, t_table, t_table]


def _x31d(d):
    lo, hi = (110, 590) if d == 0 else (110, 979)

    def num():
        n = random.randint(lo, hi)
        return n if n % 100 else n + random.randint(1, 40)

    def t_scale(mode, unit, what):
        def t():
            v = 10 * random.randint(11, 99)
            while v % 100 in (0, 50):
                v = 10 * random.randint(11, 99)
            return _ruler("Read the %s, then round it to the nearest 100 %s." % (what, unit), mode, v, 1000, unit, _r100(v),
                          ["The %s reads %d %s." % (what.split(" on ")[0], v, unit), "%d rounds to %d." % (v, _r100(v))])
        return t

    def t_count():
        r = 100 * random.randint(2, 9)
        return _tb("How many whole numbers round to %d when rounded to the nearest 100?" % r, 100, "int", {},
                   ["%d to %d all round to %d." % (r - 50, r + 49, r), "That is 100 numbers."])

    def t_table():
        ns = random.sample(range(lo, hi + 1), 3)
        miss = random.randrange(3)
        return _dt("Complete the table: round each number to the nearest 100.", ["Number", "Nearest 100"],
                   [[n, _r100(n)] for n in ns], _r100(ns[miss]),
                   ["The tens digit of %d is %d." % (ns[miss], ns[miss] // 10 % 10), "%d rounds to %d." % (ns[miss], _r100(ns[miss]))],
                   missing=(miss, 1))

    def t_true_false():
        n = num()
        claim = pick([_r100(n), _r100(n) + 100 if n % 100 < 50 else _r100(n) - 100])
        return _tf("%d rounded to the nearest 100 is %d." % (n, claim), claim == _r100(n),
                   ["The tens digit is %d, so round %s." % (n // 10 % 10, "up" if n % 100 >= 50 else "down"),
                    "%d rounds to %d." % (n, _r100(n))])

    def t_ten_vs_hundred():
        n = num()
        while n % 10 == 0 or _r10(n) == _r100(n):
            n = num()
        a, b = _r10(n), _r100(n)
        return _tb("Round %d to the nearest 10, then round %d to the nearest 100. What is the difference between "
                   "your two answers?" % (n, n), abs(a - b), "int", {},
                   ["Nearest 10: %d. Nearest 100: %d." % (a, b), "The difference is %d." % abs(a - b)])

    def t_sum():
        a, b = random.randint(110, 450), random.randint(110, 450)
        s = a + b
        return _tb("Work out %d + %d, then round the answer to the nearest 100." % (a, b), _r100(s), "int", {},
                   ["%d + %d = %d." % (a, b, s), "%d rounds to %d." % (s, _r100(s))])

    jug = t_scale("capacity", "ml", "jug")
    scales = t_scale("mass", "g", "scales")
    return [t_count, t_true_false, t_ten_vs_hundred, t_sum, jug, jug, scales, scales, t_table, t_table]


def _x31e(d):
    to10 = d == 0
    unit, rnd = (10, _r10) if to10 else (100, _r100)

    def two():
        return (random.randint(12, 89), random.randint(12, 89)) if to10 else (random.randint(110, 480), random.randint(110, 480))

    def t_spot_wrong():
        a, b = two()
        c, e = two()
        wrong = c + e + pick([-1, 1]) * (100 if not to10 else 20)
        first_wrong = random.random() < 0.5
        A = "%d + %d = %d" % (c, e, wrong) if first_wrong else "%d + %d = %d" % (a, b, a + b)
        B = "%d + %d = %d" % (a, b, a + b) if first_wrong else "%d + %d = %d" % (c, e, wrong)
        bad = (c, e)
        return _wq("Use estimating to find the calculation that must be wrong.  A: %s   B: %s  (type A or B)" % (A, B),
                   "A" if first_wrong else "B",
                   ["%d + %d is about %d + %d = %d." % (bad[0], bad[1], rnd(bad[0]), rnd(bad[1]), rnd(bad[0]) + rnd(bad[1])),
                    "So %s cannot be right." % ("A" if first_wrong else "B")], "A / B")

    def t_money():
        k = 3 if d == 2 else 2
        ps = [random.randint(11, 99) for _ in range(k)]
        est = sum(_r10(p) for p in ps)
        return _tb("Estimate the total cost of items costing %s by rounding each price to the nearest 10p. "
                   "Give your estimate in pence." % _and(["%dp" % p for p in ps]), est, "int", {"unit": "p"},
                   ["%s." % ", ".join("%dp ≈ %dp" % (p, _r10(p)) for p in ps), "The estimate is %dp." % est])

    def t_more_less():
        target = 100 if to10 else 1000
        while True:
            a, b = (random.randint(20, 79), random.randint(20, 79)) if to10 else (random.randint(200, 790), random.randint(200, 790))
            if abs(a + b - target) >= (12 if to10 else 120):
                break
        more = a + b > target
        return _wq("Without working it out exactly, is %d + %d more or less than %d? (type more or less)" % (a, b, target),
                   "more" if more else "less",
                   ["%d + %d is about %d + %d = %d." % (a, b, rnd(a), rnd(b), rnd(a) + rnd(b)),
                    "That is %s than %d." % ("more" if more else "less", target)], "more / less")

    def t_seats():
        a, b = two()
        if a < b:
            a, b = b, a
        if rnd(a) == rnd(b):
            a += unit
        what, taken = pick([("seats in a hall", "taken"), ("tickets for a show", "sold")])
        return _tb("There are %d %s and %d are %s. Estimate how many are left by rounding each number to the nearest %d."
                   % (a, what, b, taken, unit), rnd(a) - rnd(b), "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, rnd(a), b, rnd(b)), "%d − %d = %d." % (rnd(a), rnd(b), rnd(a) - rnd(b))])

    def t_how_far():
        a, b = two()
        est, exact = rnd(a) + rnd(b), a + b
        return _tb("Estimate %d + %d by rounding each number to the nearest %d, then work it out exactly. "
                   "How far is your estimate from the exact answer?" % (a, b, unit), abs(est - exact), "int", {},
                   ["Estimate: %d + %d = %d. Exact: %d." % (rnd(a), rnd(b), est, exact), "The gap is %d." % abs(est - exact)])

    def t_table():
        days = ["Monday", "Tuesday", "Wednesday"]
        vals = [two()[0] for _ in days]
        est = sum(rnd(v) for v in vals)
        return _dt("The table shows tickets sold at a fair. Estimate the total by rounding each number to the nearest %d."
                   % unit, ["Day", "Tickets"], [[a, b] for a, b in zip(days, vals)], est,
                   ["%s." % ", ".join("%d ≈ %d" % (v, rnd(v)) for v in vals), "The estimate is %d." % est])

    return [t_spot_wrong, t_money, t_more_less, t_seats, t_how_far, t_table, t_table]


def _x31f(d):
    step = pick({0: [2, 5, 10], 1: [3, 4, 8, 50, 100], 2: [4, 8, 25, 50, 100]}[d])

    def t_table():
        a = step * random.randint(1, 10)
        vals = [a + i * step for i in range(6)]
        rows = [["Number"] + [str(v) for v in vals[:4]] + ["…", str(vals[5])]]
        return _dt("The table shows a sequence. What is the 6th number?", ["Position", "1st", "2nd", "3rd", "4th", "5th", "6th"],
                   rows, vals[5], ["The sequence goes up in %ds." % step, "5th: %d, 6th: %d." % (vals[4], vals[5])],
                   missing=(0, 6))

    def t_mistake():
        a = step * random.randint(1, 10)
        vals = [a + i * step for i in range(5)]
        i = random.randint(1, 3)
        right = vals[i]
        vals[i] = right + pick([-1, 1]) * random.randint(1, max(1, step // 2 if step > 2 else 1))
        return _tb("One number in this sequence is wrong: %s. What should it be?" % _lst(vals), right, "int", {},
                   ["The sequence goes up in %ds." % step, "The %s number should be %d." % (["1st", "2nd", "3rd", "4th"][i], right)])

    def t_back():
        st = 10 if d == 0 else 100
        n = random.randint(40, 99) if d == 0 else random.randint(450, 999)
        k = random.randint(2, 4)
        return _tb("Count back in %ds from %d. What is the %s number you say after %d?" % (st, n, ["", "1st", "2nd", "3rd", "4th"][k], n),
                   n - k * st, "int", {}, ["%s." % _lst(n - i * st for i in range(k + 1)), "The answer is %d." % (n - k * st)])

    def t_in_seq():
        s = pick([3, 4, 8, 5])
        n = random.randint(30, 100)
        yes = n % s == 0
        return _yn("The sequence %s, ... counts on in %ds from %d. Will %d be in it?" % (_lst([s, 2 * s, 3 * s, 4 * s]), s, s, n), yes,
                   ["The sequence is the %d times table." % s,
                    "%d %s a multiple of %d." % (n, "is" if yes else "is not", s)])

    def t_nth():
        first = random.randint(1, 20)
        k = random.randint(5, 8)
        ans = first + (k - 1) * step
        return _tb("A sequence starts at %d and the rule is add %d. What is the %dth number?" % (first, step, k), ans, "int", {},
                   ["The %dth number is %d steps on from the 1st." % (k, k - 1), "%d + %d × %d = %d." % (first, k - 1, step, ans)])

    def t_line_back():
        st = pick([5, 10, 50, 100] if d else [5, 10])
        major = {5: 25, 10: 50, 50: 100, 100: 200}[st]
        top = st * random.randint(6, 9)
        vals = [top - i * st for i in range(4)]
        ans = vals[-1] - st
        return _nl("Continue the sequence %s, ... and place the NEXT number on the number line." % _lst(vals), ans, st, major,
                   ["The sequence goes down in %ds." % st, "%d − %d = %d." % (vals[-1], st, ans)])

    return [t_mistake, t_back, t_in_seq, t_nth, t_table, t_table, t_line_back, t_line_back]


# ================================================================ 3.2 ======
def _x32b(d):
    def t_money():
        a = random.randint(11, 89)
        b = pick([10 * random.randint(1, 9 - a // 10), random.randint(2, 9)]) if a < 90 else random.randint(2, 9)
        x, y = random.sample(["pencil", "rubber", "ruler", "badge", "sticker sheet"], 2)
        return _tb("%s costs %dp and %s costs %dp. How much do they cost together, in pence?" % (_a(x).capitalize(), a, _a(y), b), a + b, "int",
                   {"unit": "p"}, ["%dp + %dp = %dp." % (a, b, a + b)])

    def t_next_ten():
        n = random.randint(11, 98)
        while n % 10 == 0:
            n = random.randint(11, 98)
        return _tb("What must be added to %d to make the next multiple of 10?" % n, 10 - n % 10, "int", {},
                   ["The next multiple of 10 is %d." % (n + 10 - n % 10), "%d − %d = %d." % (n + 10 - n % 10, n, 10 - n % 10)])

    def t_inverse():
        add = pick([10, 20, 30, 40]) if d else random.randint(2, 9)
        n = random.randint(11, 99 - add)
        who = pick(NAMES)
        return _tb("%s adds %d to a number and gets %d. What was the number?" % (who, add, n + add), n, "int", {},
                   ["Undo the adding: %d − %d = %d." % (n + add, add, n)])

    def t_equal():
        b = 10 * random.randint(2, 5)
        a = random.randint(11, 99 - b)
        k = 10 * random.randint(1, b // 10 - 1)
        return _tb("Find the missing number:  %d + %d = %d + ___" % (a, b, a + k), b - k, "int", {},
                   ["%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, a + k, b - k)])

    def t_repeat():
        k = random.randint(2, 4)
        st = pick([10, 1]) if d == 0 else pick([10, 20])
        n = random.randint(11, 99 - k * st)
        return _tb("Start at %d and add %d, %s. Where do you end?" % (n, st, {2: "twice", 3: "three times", 4: "four times"}[k]),
                   n + k * st, "int", {}, ["%s." % _lst(n + i * st for i in range(k + 1))])

    def t_strip():
        b = pick([10 * random.randint(1, 4), random.randint(3, 9)])
        tot = random.randint(b + 11, 99)
        return _strip("The strip model shows a whole of %d split into two parts. One part is %d. What is the other part?"
                      % (tot, b), {"mode": "part_whole", "parts": 2, "totalLabel": str(tot), "partLabel": str(b), "unknown": "part"},
                      tot - b, ["%d − %d = %d." % (tot, b, tot - b), "Check: %d + %d = %d." % (tot - b, b, tot)])

    return [t_money, t_next_ten, t_inverse, t_equal, t_repeat, t_strip, t_strip]


def _x32d(d):
    def two():
        if d == 0:
            a, b = random.randint(11, 60), random.randint(11, 30)
            while a % 10 + b % 10 >= 10:
                b = random.randint(11, 30)
            return a, b
        return random.randint(15, 89), random.randint(15, 89)

    def t_money():
        a, b = two()
        x, y = random.sample(["sandwich", "drink", "apple", "yoghurt", "cake"], 2)
        return _tb("%s costs %dp and %s costs %dp. What is the total cost, in pence?" % (_a(x).capitalize(), a, _a(y), b), a + b, "int", {"unit": "p"},
                   ["%d + %d = %d." % (a, b, a + b), "The total is %dp." % (a + b)])

    def t_bond100():
        a = random.randint(11, 89)
        return _tb("What must be added to %d to make 100?" % a, 100 - a, "int", {},
                   ["%d + %d = 100." % (a, 100 - a)])

    def t_error():
        while True:
            a, b = random.randint(15, 79), random.randint(15, 79)
            if a % 10 + b % 10 >= 10:
                break
        wrong = a + b - 10
        who = pick(NAMES)
        return _tb("%s says %d + %d = %d. %s forgot the ten made from the ones. What is the correct answer?"
                   % (who, a, b, wrong, who), a + b, "int", {},
                   ["%d + %d = %d ones, which is 1 ten and %s." % (a % 10, b % 10, a % 10 + b % 10, _pl((a + b) % 10, "one")),
                    "%d + %d = %d." % (a, b, a + b)])

    def t_cards():
        ds = random.sample(range(1, 10), 4)
        s = sorted(ds, reverse=True)
        best = 10 * (s[0] + s[1]) + s[2] + s[3]
        return _tb("Use the digit cards %s once each to make two 2-digit numbers with the LARGEST possible total. "
                   "What is the total?" % _lst(ds), best, "int", {},
                   ["Put the two biggest digits, %d and %d, in the tens places." % (s[0], s[1]),
                    "%d%d + %d%d = %d." % (s[0], s[2], s[1], s[3], best)])

    def t_length():
        a, b = two()
        return _tb("A path is made of two parts, %d m and %d m long. How long is the whole path, in metres?" % (a, b), a + b, "int",
                   {"unit": "m"}, ["%d + %d = %d m." % (a, b, a + b)])

    def t_table():
        a, b = two()
        who = random.sample(NAMES, 1)[0]
        return _dt("The table shows %s's scores in two games. What is the total?" % who, ["Game", "Points"],
                   [["Game 1", a], ["Game 2", b], ["Total", a + b]], a + b, ["%d + %d = %d." % (a, b, a + b)], missing=(2, 1))

    def t_bars():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = random.sample(range(2, 10), 4)
        vals = [v * 5 for v in vals] if d == 0 else [v * 10 for v in vals]
        i, j = random.sample(range(4), 2)
        return _bar("The chart shows how many books were borrowed each day. How many were borrowed on %s and %s together?"
                    % (cats[i], cats[j]), cats, vals, vals[i] + vals[j], ["%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])])

    return [t_money, t_bond100, t_error, t_cards, t_length, t_table, t_table, t_bars, t_bars]


def _x32e(d):
    def two():
        a = random.randint(31, 99)
        b = random.randint(11, a - 5)
        if d == 0:
            while b % 10 > a % 10:
                b = random.randint(11, a - 5)
        return a, b

    def t_strip():
        a, b = two()
        return _strip("The whole is %d. One part is %d. What is the other part?" % (a, b),
                      {"mode": "part_whole", "parts": 2, "totalLabel": str(a), "partLabel": str(b), "unknown": "part"},
                      a - b, ["%d − %d = %d." % (a, b, a - b)])

    def t_bars():
        cats = random.sample(["Red", "Blue", "Green", "Yellow"], 2)
        a, b = two()
        a, b = 10 * (a // 10), 10 * (b // 10)
        if a == b:
            a += 10
        return _bar("The chart shows votes for two colours. How many more votes did %s get than %s?" % (cats[0], cats[1]),
                    cats, [a, b], a - b, ["%d − %d = %d." % (a, b, a - b)])

    def t_error():
        while True:
            a, b = random.randint(41, 95), random.randint(12, 39)
            if a % 10 < b % 10 and a > b:
                break
        wrong = (a // 10 - b // 10) * 10 + (b % 10 - a % 10)
        who = pick(NAMES)
        return _tb("%s says %d − %d = %d, because %s took the smaller ones digit from the larger one. What is the correct answer?"
                   % (who, a, b, wrong, who), a - b, "int", {},
                   ["%s take away %s needs an exchange." % (_u(a % 10, "ones"), _u(b % 10, "ones")), "%d − %d = %d." % (a, b, a - b)])

    def t_age():
        a, b = random.randint(30, 79), random.randint(5, 25)
        who = pick(NAMES)
        rel = pick(["grandad", "aunt", "teacher", "uncle"])
        return _tb("%s's %s is %d. %s is %d. How many years older is the %s?" % (who, rel, a, who, b, rel), a - b, "int", {},
                   ["%d − %d = %d years." % (a, b, a - b)])

    def t_cards():
        ds = random.sample(range(1, 10), 4)
        s = sorted(ds)
        big, small = 10 * s[3] + s[2], 10 * s[0] + s[1]
        return _tb("Use the digit cards %s once each. Make the largest 2-digit number with two cards and the smallest "
                   "2-digit number with the other two. What is the difference?" % _lst(ds), big - small, "int", {},
                   ["Largest: %d. Smallest: %d." % (big, small), "%d − %d = %d." % (big, small, big - small)])

    def t_table():
        a, b = two()
        return _dt("A shop had some apples. The table shows how many were sold. How many are left?", ["", "Apples"],
                   [["At the start", a], ["Sold", b], ["Left", a - b]], a - b, ["%d − %d = %d." % (a, b, a - b)], missing=(2, 1))

    return [t_error, t_age, t_cards, t_strip, t_strip, t_bars, t_bars, t_table, t_table]


def _x32f(d):
    def t_strip():
        tot = random.randint(30, 99)
        b = random.randint(11, tot - 8)
        return _strip("Find the missing part. The whole is %d and one part is %d." % (tot, b),
                      {"mode": "part_whole", "parts": 2, "totalLabel": str(tot), "partLabel": str(b), "unknown": "part"},
                      tot - b, ["%d + ___ = %d." % (b, tot), "%d − %d = %d." % (tot, b, tot - b)])

    def t_balance():
        a, b, c = random.randint(11, 40), random.randint(11, 40), random.randint(5, 20)
        while a + b - c <= 0 or a + b - c == b:
            c = random.randint(5, 20)
        x = a + b - c
        return _tb("Find the missing number:  %d + ___ = %d + %d" % (c, a, b), x, "int", {},
                   ["%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, x)])

    def t_think():
        sub = random.randint(11, 40)
        res = random.randint(11, 99 - sub)
        who = pick(NAMES)
        op = pick(["subtracts", "adds"])
        if op == "adds":
            return _tb("%s thinks of a number and adds %d. The answer is %d. What was the number?" % (who, sub, res + sub), res, "int", {},
                       ["Undo it: %d − %d = %d." % (res + sub, sub, res)])
        return _tb("%s thinks of a number and subtracts %d. The answer is %d. What was the number?" % (who, sub, res), res + sub,
                   "int", {}, ["Undo it: %d + %d = %d." % (res, sub, res + sub)])

    def t_digit():
        a = random.randint(21, 69)
        b = random.randint(11, 29)
        tot = a + b
        return _tb("A digit is missing:  %d□ + %d = %d. What is the missing digit?" % (a // 10, b, tot), a % 10, "int", {},
                   ["%d − %d = %d." % (tot, b, a), "So the missing digit is %d." % (a % 10)])

    def t_table():
        k = random.randint(11, 30)
        ins = random.sample(range(11, 99 - k), 3)
        miss = random.randrange(3)
        rows = [[i, i + k] for i in ins]
        return _dt("In this table %d is added to each starting number. Type the missing starting number." % k,
                   ["Start", "Add %d" % k], rows, ins[miss], ["%d − %d = %d." % (ins[miss] + k, k, ins[miss])], missing=(miss, 0))

    return [t_balance, t_think, t_digit, t_strip, t_strip, t_table, t_table]


# ================================================================ 3.3 ======
def _no_carry():
    while True:
        a, b = random.randint(101, 799), random.randint(101, 199 if random.random() < 0.3 else 899)
        if all(int(x) + int(y) < 10 for x, y in zip("%03d" % a, "%03d" % b)) and a + b < 1000:
            return a, b


def _carry():
    while True:
        a, b = random.randint(105, 799), random.randint(105, 799)
        if a + b < 1000 and (a % 10 + b % 10 >= 10 or a // 10 % 10 + b // 10 % 10 >= 10):
            return a, b


def _no_exchange():
    while True:
        a, b = random.randint(200, 999), random.randint(101, 899)
        if a > b and all(int(x) >= int(y) for x, y in zip("%03d" % a, "%03d" % b)):
            return a, b


def _exchange():
    while True:
        a, b = random.randint(300, 999), random.randint(101, 799)
        if a > b and (a % 10 < b % 10 or a // 10 % 10 < b // 10 % 10):
            return a, b


def _column_set(kind):
    """Framings shared by the four column-method skills; kind is add/carry/sub/exchange."""
    pair = {"add": _no_carry, "carry": _carry, "sub": _no_exchange, "exchange": _exchange}[kind]
    add = kind in ("add", "carry")
    op = "+" if add else "−"

    def res(a, b):
        return a + b if add else a - b

    def t_box():
        a, b = pair()
        r = res(a, b)
        pos = random.choice([0, 1, 2])
        sa = list("%03d" % a)
        dig = sa[pos]
        sa[pos] = "□"
        return _tb("A digit is missing:  %s %s %d = %d. What is the missing digit?" % ("".join(sa), op, b, r), int(dig), "int", {},
                   ["Work backwards: %d %s %d = %d." % (r, "−" if add else "+", b, a), "The missing digit is %s." % dig])

    def t_columns():
        a, b = pair()
        return _dt("The table shows a column %s. What is the answer?" % ("addition" if add else "subtraction"),
                   ["", "H", "T", "O"], [[""] + list(str(a)), [op] + list("%3d" % b)], res(a, b),
                   ["Work from the ones column to the hundreds column.", "%d %s %d = %d." % (a, op, b, res(a, b))])

    def t_strip():
        a, b = pair()
        if add:
            return _strip("The strip model shows a whole of %d. One part is %d. Use column subtraction to check: what is "
                          "the other part?" % (a + b, a),
                          {"mode": "part_whole", "parts": 2, "totalLabel": str(a + b), "partLabel": str(a), "unknown": "part"},
                          b, ["%d − %d = %d." % (a + b, a, b), "Check: %d + %d = %d." % (a, b, a + b)])
        return _strip("The whole is %d and one part is %d. What is the other part?" % (a, b),
                      {"mode": "part_whole", "parts": 2, "totalLabel": str(a), "partLabel": str(b), "unknown": "part"},
                      a - b, ["%d − %d = %d." % (a, b, a - b)])

    def t_bars():
        cats = random.sample(["Year 3", "Year 4", "Year 5", "Year 6"], 2)
        a, b = pair()
        a, b = 10 * (a // 10), 10 * (b // 10)
        if add:
            return _bar("The chart shows how many raffle tickets two year groups sold. How many did they sell altogether?",
                        cats, [a, b], a + b, ["%d + %d = %d." % (a, b, a + b)])
        if a == b:
            a += 10
        return _bar("The chart shows how many raffle tickets two year groups sold. How many more did %s sell than %s?"
                    % (cats[0], cats[1]), cats, [a, b], a - b, ["%d − %d = %d." % (a, b, a - b)])

    def t_error():
        who = pick(NAMES)
        if kind == "add":
            a = random.randint(201, 799)
            b = random.randint(11, 99)
            while a % 10 + b % 10 >= 10 or a // 10 % 10 + b // 10 >= 10 or a + 10 * b >= 1000:
                a, b = random.randint(201, 799), random.randint(11, 99)
            return _tb("%s worked out %d + %d and got %d, by lining up the %d under the hundreds and tens. What is the "
                       "correct answer?" % (who, a, b, a + 10 * b, b), a + b, "int", {},
                       ["Line the ones up under the ones.", "%d + %d = %d." % (a, b, a + b)])
        if kind == "carry":
            a, b = pair()
            wrong = int("".join(str((int(x) + int(y)) % 10) for x, y in zip("%03d" % a, "%03d" % b)))
            return _tb("%s worked out %d + %d = %d but forgot to carry. What is the correct answer?" % (who, a, b, wrong),
                       a + b, "int", {}, ["Carry each ten ones into the next column.", "%d + %d = %d." % (a, b, a + b)])
        if kind == "sub":
            a = random.randint(300, 999)
            b = random.randint(11, 99)
            while a % 10 < b % 10 or a // 10 % 10 < b // 10 or a // 100 <= b // 10 or (a - 10 * b) < 0:
                a, b = random.randint(300, 999), random.randint(11, 99)
            return _tb("%s worked out %d − %d and got %d, by lining the %d up under the hundreds and tens. What is the "
                       "correct answer?" % (who, a, b, a - 10 * b, b), a - b, "int", {},
                       ["Line the ones up under the ones.", "%d − %d = %d." % (a, b, a - b)])
        a, b = pair()
        wrong = int("".join(str(abs(int(x) - int(y))) for x, y in zip("%03d" % a, "%03d" % b)))
        return _tb("%s worked out %d − %d = %d by taking the smaller digit from the larger one in each column. What is the "
                   "correct answer?" % (who, a, b, wrong), a - b, "int", {},
                   ["Where the top digit is smaller, exchange from the next column.", "%d − %d = %d." % (a, b, a - b)])

    def t_three():
        if add:
            while True:
                xs = [random.randint(101, 399) for _ in range(3)]
                s = sum(xs)
                no_c = all(sum(int(("%03d" % x)[i]) for x in xs) < 10 for i in range(3))
                if s < 1000 and (no_c if kind == "add" else not no_c):
                    break
            return _tb("Work out %s." % " + ".join(str(x) for x in xs), s, "int", {},
                       ["Add the columns from the ones.", "= %d." % s])
        a, b = pair()
        c = random.randint(1, a - b) if a - b > 1 else 1
        return _tb("Work out %d − %d − %d." % (a, b, c), a - b - c, "int", {},
                   ["%d − %d = %d." % (a, b, a - b), "%d − %d = %d." % (a - b, c, a - b - c)])

    def t_exchanges():
        if add:
            a, b = pair()
            n = 0
            carry = 0
            for x, y in zip(reversed("%03d" % a), reversed("%03d" % b)):
                s = int(x) + int(y) + carry
                carry = 1 if s >= 10 else 0
                n += carry
            return _tb("In the column addition %d + %d, how many times do you need to carry a ten or a hundred into the next "
                       "column?" % (a, b), n, "int", {}, ["Work from the ones: carry when a column makes 10 or more.",
                                                        "%d + %d = %d, with %s." % (a, b, a + b, _pl(n, "carry", "carries"))])
        a, b = pair()
        n = 0
        borrow = 0
        for x, y in zip(reversed("%03d" % a), reversed("%03d" % b)):
            top = int(x) - borrow
            borrow = 1 if top < int(y) else 0
            n += borrow
        return _tb("In the column subtraction %d − %d, how many exchanges do you need to make?" % (a, b), n, "int", {},
                   ["Exchange when the top digit is smaller than the bottom digit.",
                    "%d − %d = %d, with %s." % (a, b, a - b, _pl(n, "exchange"))])

    def t_context():
        a, b = pair()
        x, y = random.sample(["London", "Leeds", "York", "Bath", "Hull"], 2)
        if add:
            return _tb("A coach drives %d km from %s to %s, then %d km back towards home. How far does it drive altogether?"
                       % (a, x, y, b), a + b, "int", {"unit": "km"}, ["%d + %d = %d km." % (a, b, a + b)])
        return _tb("A coach trip is %d km. After %d km the coach stops for lunch. How many km are left?" % (a, b), a - b, "int",
                   {"unit": "km"}, ["%d − %d = %d km." % (a, b, a - b)])

    plain = [t_box, t_error, t_three, t_context]
    if kind in ("carry", "exchange"):
        plain.append(t_exchanges)
    return plain + [t_columns, t_columns, t_strip, t_strip, t_bars, t_bars]


def _x33f(d):
    def pair():
        return random.randint(120, 600), random.randint(110, 390)

    def t_which_check():
        a, b = pair()
        add = random.random() < 0.5
        if not add and a < b:
            a, b = b, a
        if a == b:
            a += 7
        r = a + b if add else a - b
        stmt = "%d %s %d = %d" % (a, "+" if add else "−", b, r)
        right = "%d − %d" % (r, b) if add else "%d + %d" % (r, b)
        wrongs = ["%d + %d" % (r, b), "%d + %d" % (a, b)] if add else ["%d − %d" % (r, b), "%d + %d" % (a, b)]
        opts = [right] + wrongs
        random.shuffle(opts)
        letter = "ABC"[opts.index(right)]
        return _wq("Which calculation checks %s?  A: %s   B: %s   C: %s  (type A, B or C)" % (stmt, opts[0], opts[1], opts[2]),
                   letter, ["The inverse of %s is %s." % ("adding" if add else "subtracting", "subtracting" if add else "adding"),
                            "%s = %d." % (right, a)], "A / B / C")

    def t_should_get():
        a, b = pair()
        return _tb("To check %d + %d = %d, Leo works out %d − %d. What should Leo get?" % (a, b, a + b, a + b, b), a, "int", {},
                   ["Subtracting %d undoes adding %d." % (b, b), "%d − %d = %d." % (a + b, b, a)])

    def t_family():
        a, b = pair()
        k = random.randint(1, 3)
        return _tb("You know that %d + %d = %d. Use this to find %d − %d." % (a, b, a + b, a + b, b + k), a - k, "int", {},
                   ["%d − %d = %d." % (a + b, b, a), "Taking away %d more leaves %d less: %d − %d = %d." % (k, k, a, k, a - k)])

    def t_sensible():
        a, b = random.randint(150, 450), random.randint(150, 450)
        right = random.random() < 0.5
        claim = a + b if right else a + b + pick([-100, 100])
        return _yn("Leo says %d + %d = %d. Check it with the inverse: is Leo right?" % (a, b, claim), right,
                   ["%d − %d = %d." % (claim, b, claim - b), "%s" % ("That gets back to %d, so Leo is right." % a if right
                                                                      else "That is not %d, so Leo is wrong: %d + %d = %d." % (a, a, b, a + b))])

    def t_odd_wrong():
        cs = []
        for _ in range(3):
            a, b = pair()
            cs.append((a, b))
        bad = random.randrange(3)
        shown = []
        for i, (a, b) in enumerate(cs):
            r = a + b + (pick([-10, 10]) if i == bad else 0)
            shown.append("%s: %d + %d = %d" % ("ABC"[i], a, b, r))
        a, b = cs[bad]
        return _wq("One of these is wrong. Check each one with the inverse.  %s  (type A, B or C)" % "   ".join(shown), "ABC"[bad],
                   ["Subtract the second number from each answer.", "%s should be %d + %d = %d." % ("ABC"[bad], a, b, a + b)],
                   "A / B / C")

    def t_table():
        rows = []
        for _ in range(3):
            a, b = pair()
            rows.append([a, b, a + b])
        miss = random.randrange(3)
        a, b, _t = rows[miss]
        return _dt("Each row shows a start number, the number added, and the total. Use the inverse to find the missing start number.",
                   ["Start", "Added", "Total"], rows, a, ["%d − %d = %d." % (a + b, b, a)], missing=(miss, 0))

    def t_strip():
        a, b = pair()
        claim = a + b + pick([0, 0, -10, 10, 100])
        return _strip("Ella says %d + %d = %d. The strip checks it: the whole is %d and one part is %d. What is the other part? "
                      "(If it is not %d, Ella made a mistake.)" % (a, b, claim, claim, a, b),
                      {"mode": "part_whole", "parts": 2, "totalLabel": str(claim), "partLabel": str(a), "unknown": "part"},
                      claim - a, ["%d − %d = %d." % (claim, a, claim - a),
                                  "So Ella is right." if claim == a + b else "That is not %d, so Ella is wrong: %d + %d = %d." % (b, a, b, a + b)])

    return [t_which_check, t_should_get, t_family, t_sensible, t_odd_wrong, t_table, t_table, t_strip, t_strip]


def _x33g(d):
    def t_more_than():
        a = random.randint(110, 400)
        k = random.randint(50, 300)
        x, y = pick([("Shelf A", "Shelf B"), ("Class 3A", "Class 3B"), ("The red team", "The blue team")])
        thing = pick(["books", "cans", "points"])
        more = random.random() < 0.5
        b = a + k if more else a - k
        if b <= 0:
            more, b = True, a + k
        return _tb("%s has %d %s. %s has %d %s than %s. How many %s are there altogether?"
                   % (x, a, thing, y, k, "more" if more else "fewer", x.lower() if x.startswith("The") else x, thing),
                   a + b, "int", {}, ["%s has %d %s %d = %d." % (y, a, "+" if more else "−", k, b), "%d + %d = %d." % (a, b, a + b)])

    def t_stay():
        boys, girls = random.randint(110, 300), random.randint(110, 300)
        go = random.randint(60, boys + girls - 50)
        return _tb("A school has %d boys and %d girls. %d pupils go on a trip. How many pupils stay at school?" % (boys, girls, go),
                   boys + girls - go, "int", {}, ["%d + %d = %d pupils." % (boys, girls, boys + girls),
                                                  "%d − %d = %d." % (boys + girls, go, boys + girls - go)])

    def t_table():
        a, b, c = random.randint(110, 300), random.randint(110, 300), random.randint(110, 300)
        days = ["Monday", "Tuesday", "Wednesday"]
        miss = random.randrange(3)
        vals = [a, b, c]
        rows = [[dname, v] for dname, v in zip(days, vals)] + [["Total", a + b + c]]
        return _dt("The table shows visitors to a museum. The total is given. How many visitors came on %s?" % days[miss],
                   ["Day", "Visitors"], rows, vals[miss],
                   ["The other two days make %d." % (a + b + c - vals[miss]), "%d − %d = %d." % (a + b + c, a + b + c - vals[miss], vals[miss])],
                   missing=(miss, 1))

    def t_balance():
        a, b = random.randint(150, 400), random.randint(100, 300)
        n = random.randint(500, 900)
        x = n - a - b
        while x <= 0:
            n = random.randint(500, 900)
            x = n - a - b
        return _tb("Find the missing number:  %d − ___ = %d + %d" % (n, a, b), x, "int", {},
                   ["%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (n, a + b, x)])

    def t_bars():
        cats = ["Year 3", "Year 4", "Year 5"]
        vals = [10 * random.randint(10, 40) for _ in cats]
        while vals[0] + vals[1] <= vals[2]:
            vals = [10 * random.randint(10, 40) for _ in cats]
        return _bar("The chart shows how many cans each year group collected. How many more cans did Year 3 and Year 4 "
                    "collect together than Year 5?", cats, vals, vals[0] + vals[1] - vals[2],
                    ["%d + %d = %d." % (vals[0], vals[1], vals[0] + vals[1]),
                     "%d − %d = %d." % (vals[0] + vals[1], vals[2], vals[0] + vals[1] - vals[2])])

    return [t_more_than, t_stay, t_balance, t_table, t_table, t_bars, t_bars]


# ================================================================ 3.4 ======
_LEGS = {2: ("pair of socks", "pairs of socks", "socks"), 3: ("tricycle", "tricycles", "wheels"),
         4: ("chair", "chairs", "legs"), 5: ("hand", "hands", "fingers"), 8: ("spider", "spiders", "legs"),
         10: ("box of 10 pencils", "boxes of 10 pencils", "pencils")}


def _table_extra(tabs):
    """Extra framings for the times-table skills; tabs is the table(s) the skill covers."""
    def builder(d):
        t = pick(tabs)
        k = random.randint(1, 6) if d == 0 else random.randint(2, 12)
        p = t * k

        def t_double():
            if t in (4, 8):
                h = t // 2
                return _tb("%d × %d = %d. Double it to find %d × %d." % (h, k, h * k, t, k), p, "int", {},
                           ["%d is double %d, so double %d." % (t, h, h * k), "%d × 2 = %d." % (h * k, p)])
            if t == 5:
                return _tb("10 × %d = %d. Halve it to find 5 × %d." % (k, 10 * k, k), p, "int", {},
                           ["5 is half of 10.", "%d ÷ 2 = %d." % (10 * k, p)])
            if t == 3:
                return _tb("2 × %d = %d. Add one more %d to find 3 × %d." % (k, 2 * k, k, k), p, "int", {},
                           ["3 lots is 2 lots and 1 more lot.", "%d + %d = %d." % (2 * k, k, p)])
            return _tb("%d × %d = %d. What is %d × %d?" % (t, k, p, t, k + 1), p + t, "int", {},
                       ["One more %d: %d + %d = %d." % (t, p, t, p + t)])

        def t_context():
            one, many, what = _LEGS[t]
            return _tb("One %s has %d %s. How many %s do %d %s have altogether?" % (one, t, what, what, k, one if k == 1 else many),
                       p, "int", {}, ["%d × %d = %d %s." % (k, t, p, what)])

        def t_context_div():
            one, many, what = _LEGS[t]
            return _tb("There are %d %s altogether, and each %s has %d. How many %s are there?" % (p, what, one, t, many), k, "int", {},
                       ["%d ÷ %d = %d." % (p, t, k)])

        def t_is_multiple():
            n = random.randint(t * 2, t * 12 + t)
            yes = n % t == 0
            q = n // t
            sol = ["%d = %d × %d." % (n, q, t)] if yes else \
                ["%d × %d = %d and %d × %d = %d, so %d is between them." % (q, t, q * t, q + 1, t, (q + 1) * t, n)]
            return _yn("Is %d in the %d times table?" % (n, t), yes, sol)

        def t_which_multiple():
            m = t * random.randint(2, 12)
            opts = [m]
            while len(opts) < 4:
                x = random.randint(t + 1, t * 12)
                if x % t and x not in opts:
                    opts.append(x)
            random.shuffle(opts)
            return _tb("Which of these numbers is in the %d times table?   %s" % (t, _lst(opts)), m, "int", {},
                       ["%d = %d × %d." % (m, m // t, t)])

        def t_groups():
            g = min(k, 8)
            return _eg("Each ring holds %d counters. How many counters are there altogether?" % t, g, t, g * t,
                       ["%s of %d." % (_pl(g, "group"), t), "%d × %d = %d." % (g, t, g * t)])

        def t_io():
            ins = random.sample(range(2, 13), 4)
            miss = random.randrange(4)
            return _io("Each Out number is the In number multiplied by %d. Type the missing Out number." % t,
                       [[i, i * t] for i in ins], miss, ins[miss] * t, ["%d × %d = %d." % (ins[miss], t, ins[miss] * t)],
                       rule="× %d" % t)

        def t_pictogram():
            cats = random.sample(["Cars", "Bikes", "Buses", "Vans"], 3)
            vals = [t * random.randint(1, 6) for _ in cats]
            i = random.randrange(3)
            return _pict("Each symbol stands for %d. How many %s are there?" % (t, cats[i].lower()), cats, vals, t, "circle", vals[i],
                         ["That row has %s." % _pl(vals[i] // t, "symbol"), "%d × %d = %d." % (vals[i] // t, t, vals[i])])

        return [t_double, t_context, t_context_div, t_is_multiple, t_which_multiple,
                t_groups, t_groups, t_io, t_io, t_pictogram, t_pictogram]
    return builder


def _x34f(d):
    per = random.randint(2, 5 if d == 0 else 10)
    n = pick([2, 3, 4, 5] if d == 0 else [2, 3, 4, 5, 8])
    tot = per * n

    def t_strip():
        return _strip("%d sweets are shared equally between %d children. The strip model shows the sharing. How many does each "
                      "child get?" % (tot, n), {"mode": "equal_parts", "parts": n, "partLabel": "?", "totalLabel": str(tot),
                                                "unknown": "part"}, per, ["%d ÷ %d = %d." % (tot, n, per)])

    def t_coins():
        c = pick([2, 5, 10])
        k = random.randint(2, 9)
        return _tb("How many %dp coins make %dp?" % (c, c * k), k, "int", {}, ["%d ÷ %d = %d." % (c * k, c, k)])

    def t_how_many_people():
        who = pick(NAMES)
        return _tb("%s shares %d grapes equally. Everyone gets %d. How many people share the grapes?" % (who, tot, per), n, "int", {},
                   ["%d ÷ %d = %d." % (tot, per, n)])

    def t_can_share():
        m = random.randint(10, 40)
        k = random.randint(2, 5)
        yes = m % k == 0
        return _yn("Can %d stickers be shared equally between %d children with none left over?" % (m, k), yes,
                   ["%d ÷ %d = %d%s." % (m, k, m // k, "" if yes else " remainder %d" % (m % k))])

    def t_table():
        rows = []
        for _ in range(3):
            g = random.randint(2, 5)
            e = random.randint(2, 10)
            rows.append([g * e, g, e])
        miss = random.randrange(3)
        return _dt("Each row shows some sweets shared equally between some children. How many does each child get in the row "
                   "with the missing number?", ["Sweets", "Children", "Each child gets"], rows, rows[miss][2],
                   ["%d ÷ %d = %d." % (rows[miss][0], rows[miss][1], rows[miss][2])], missing=(miss, 2))

    def t_bars():
        cats = ["Red", "Blue", "Green"]
        k = pick([2, 3, 4, 5])
        vals = [k * random.randint(2, 6) for _ in cats]
        i = random.randrange(3)
        return _bar("The chart shows stickers in three colours. The %s stickers are shared equally between %d friends. How many "
                    "does each friend get?" % (cats[i].lower(), k), cats, vals, vals[i] // k,
                    ["There are %d %s stickers." % (vals[i], cats[i].lower()), "%d ÷ %d = %d." % (vals[i], k, vals[i] // k)])

    return [t_coins, t_how_many_people, t_can_share, t_strip, t_strip, t_table, t_table, t_bars, t_bars]


def _x34g(d):
    t = pick([3, 4, 8] if d else [3, 4])
    k = random.randint(2, 6) if d == 0 else random.randint(2, 12)
    p = t * k

    def t_strip():
        return _strip("Share %d equally into %d parts. How much is in each part?" % (p, t),
                      {"mode": "equal_parts", "parts": t, "partLabel": "?", "totalLabel": str(p), "unknown": "part"}, k,
                      ["%d ÷ %d = %d." % (p, t, k)])

    def t_groups():
        g = min(k, 8)
        return _eg("%d counters are put into groups of %d. How many groups are there?" % (g * t, t), g, t, g,
                   ["Count the rings.", "%d ÷ %d = %d." % (g * t, t, g)])

    def t_io():
        ins = random.sample(range(2, 13), 4)
        miss = random.randrange(4)
        return _io("Each Out number is the In number divided by %d. Type the missing Out number." % t,
                   [[i * t, i] for i in ins], miss, ins[miss], ["%d ÷ %d = %d." % (ins[miss] * t, t, ins[miss])], rule="÷ %d" % t)

    def t_legs():
        if t == 8:
            return _tb("Some spiders have %d legs altogether. Each spider has 8 legs. How many spiders are there?" % p, k, "int", {},
                       ["%d ÷ 8 = %d." % (p, k)])
        if t == 4:
            return _tb("Some cars have %d wheels altogether. Each car has 4 wheels. How many cars are there?" % p, k, "int", {},
                       ["%d ÷ 4 = %d." % (p, k)])
        return _tb("Some tricycles have %d wheels altogether. Each tricycle has 3 wheels. How many tricycles are there?" % p, k,
                   "int", {}, ["%d ÷ 3 = %d." % (p, k)])

    def t_divisor():
        return _tb("Find the missing number:  %d ÷ ___ = %d" % (p, k), t, "int", {}, ["%d × %d = %d." % (k, t, p)])

    def t_bigger():
        m = 24 * random.randint(1, 4)
        return _tb("Which is bigger, %d ÷ 4 or %d ÷ 8? Type the bigger answer." % (m, m), m // 4, "int", {},
                   ["%d ÷ 4 = %d and %d ÷ 8 = %d." % (m, m // 4, m, m // 8), "Sharing between fewer gives more each."])

    def t_halve():
        m = 8 * random.randint(2, 12)
        return _tb("%d ÷ 4 = %d. Use this to work out %d ÷ 8." % (m, m // 4, m), m // 8, "int", {},
                   ["Dividing by 8 is half of dividing by 4.", "%d ÷ 2 = %d." % (m // 4, m // 8)])

    return [t_legs, t_divisor, t_bigger, t_halve, t_strip, t_strip, t_groups, t_groups, t_io, t_io]


def _x34h(d):
    t = pick([3, 4, 8] if d else [2, 3, 4, 5])
    k = random.randint(2, 6) if d == 0 else random.randint(2, 12)
    p = t * k

    def t_times10():
        return _tb("%d × %d = %d. Use this fact to work out %d × %d." % (t, k, p, t, 10 * k), 10 * p, "int", {},
                   ["%d is 10 times %d, so the answer is 10 times %d." % (10 * k, k, p), "%d × 10 = %d." % (p, 10 * p)])

    def t_div10():
        return _tb("%d × %d = %d. Use this fact to work out %d ÷ %d." % (t, k, p, 10 * p, t), 10 * k, "int", {},
                   ["%d is 10 times %d." % (10 * p, p), "So the answer is 10 times %d = %d." % (k, 10 * k)])

    def t_symbol():
        t2 = 2 * t if t in (2, 4) else t
        if t2 == t:
            return _tb("▲ × %d = %d. What is ▲ × 10?" % (t, p), 10 * k, "int", {}, ["▲ = %d ÷ %d = %d." % (p, t, k), "%d × 10 = %d." % (k, 10 * k)])
        return _tb("▲ × %d = %d. What is ▲ × %d?" % (t, p, t2), k * t2, "int", {},
                   ["▲ = %d ÷ %d = %d." % (p, t, k), "%d × %d = %d." % (k, t2, k * t2)])

    def t_strip():
        return _strip("The strip has %d equal parts of %d. What is the total?"
                      % (k, t), {"mode": "equal_parts", "parts": k, "partLabel": str(t), "totalLabel": "?",
                                                               "unknown": "total"}, p, ["%d × %d = %d." % (k, t, p), "So %d ÷ %d = %d." % (p, t, k)])

    def t_io():
        ins = random.sample(range(2, 13), 4)
        miss = random.randrange(4)
        return _io("The rule divides by %d. Type the missing Out number." % t, [[i * t, i] for i in ins], miss, ins[miss],
                   ["%d × %d = %d, so %d ÷ %d = %d." % (ins[miss], t, ins[miss] * t, ins[miss] * t, t, ins[miss])], rule="÷ %d" % t)

    def t_not_family():
        others = [k * t2 for t2 in (2, 3, 4, 5, 8, 10) if k * t2 != p]
        odd = pick(others) if others else p + 1
        nums = [t, k, p, odd]
        random.shuffle(nums)
        if t == k:
            return t_times10()
        return _tb("Three of these numbers make a multiplication fact family. Which number does NOT belong?   %s" % _lst(nums), odd,
                   "int", {}, ["%d × %d = %d and %d ÷ %d = %d." % (t, k, p, p, t, k), "%d does not belong." % odd])

    return [t_times10, t_div10, t_symbol, t_not_family, t_strip, t_strip, t_io, t_io]


def _x34i(d):
    def t_assoc():
        a, b, c = pick([(4, 7, 5), (5, 9, 2), (2, 8, 5), (5, 6, 2), (4, 3, 5), (2, 13, 5)])
        return _tb("Work out %d × %d × %d. Tip: multiply the pair that makes 10 or 20 first." % (a, b, c), a * b * c, "int", {},
                   ["%d × %d = %d first." % (a, c, a * c), "%d × %d = %d." % (a * c, b, a * b * c)])

    def t_commute():
        a, b = random.randint(2, 12), random.randint(2, 12)
        return _tb("Find the missing number:  %d × %d = %d × ___" % (a, b, b), a, "int", {},
                   ["Multiplying in either order gives the same product."])

    def t_distribute():
        a, b = random.randint(3, 8), random.randint(6, 9)
        c = random.randint(2, b - 2)
        return _tb("Find the missing number:  %d × %d = %d × %d + %d × ___" % (a, b, a, c, a), b - c, "int", {},
                   ["%d = %d + %d." % (b, c, b - c), "So %d × %d = %d × %d + %d × %d." % (a, b, a, c, a, b - c)])

    def t_zero():
        n = random.randint(11, 99)
        if random.random() < 0.5:
            return _tb("Work out %d × 0." % n, 0, "int", {}, ["Any number multiplied by 0 is 0."])
        return _tb("Work out %d × 1." % n, n, "int", {}, ["Multiplying by 1 leaves a number the same."])

    def t_div_order():
        a, b = random.randint(2, 5), random.randint(2, 5)
        p = a * b * pick([2, 3])
        return _tf("%d ÷ %d is the same as %d ÷ %d." % (p, a, a, p), False,
                   ["%d ÷ %d = %d, but %d ÷ %d is less than 1." % (p, a, p // a, a, p), "Division cannot be done in either order."])

    def t_groups():
        g, per = random.randint(2, 6), random.randint(2, 9)
        return _eg("There are %d groups of %d. %d × %d gives the same total. Type the total." % (g, per, per, g), g, per, g * per,
                   ["%d × %d = %d × %d = %d." % (g, per, per, g, g * per)])

    return [t_assoc, t_commute, t_distribute, t_zero, t_div_order, t_groups, t_groups]


# ================================================================ 3.5 ======
def _x35a(d):
    t = random.randint(2, 4) if d == 0 else pick([3, 4, 5, 8])
    n = random.randint(11, 24) if d == 0 else random.randint(13, 49 if d == 1 else 99)
    tens, ones = n // 10 * 10, n % 10

    def t_grid():
        if random.random() < 0.5:
            return _dt("The grid method shows %d × %d. What number goes in the empty box?" % (n, t), ["×", str(tens), str(ones)],
                       [[t, tens * t, ones * t]], ones * t, ["%d × %d = %d." % (ones, t, ones * t)], missing=(0, 2))
        return _dt("The grid method shows %d × %d. Add the two parts. What is %d × %d?" % (n, t, n, t), ["×", str(tens), str(ones)],
                   [[t, tens * t, ones * t]], n * t, ["%d + %d = %d." % (tens * t, ones * t, n * t)])

    def t_partition():
        return _tb("%d × %d = %d × %d + %d × %d = %d + ___" % (n, t, tens, t, ones, t, tens * t), ones * t, "int", {},
                   ["%d × %d = %d." % (ones, t, ones * t), "So %d × %d = %d." % (n, t, n * t)])

    def t_money():
        thing = pick(["ticket", "book", "pair of gloves", "board game"])
        return _tb("One %s costs £%d. How much do %d cost, in pounds?" % (thing, n, t), n * t, "int", {"unit": "£"},
                   ["%d × %d = %d." % (n, t, n * t), "That is £%d." % (n * t)])

    def t_strip():
        return _strip("The strip has %d equal parts. Each part is %d. What is the total?" % (t, n),
                      {"mode": "equal_parts", "parts": t, "partLabel": str(n), "totalLabel": "?", "unknown": "total"}, n * t,
                      ["%d × %d = %d." % (n, t, n * t)])

    def t_estimate():
        m = n if n % 10 else n + 3
        return _tb("Estimate %d × %d by rounding %d to the nearest 10 first." % (m, t, m), _r10(m) * t, "int", {},
                   ["%d ≈ %d." % (m, _r10(m)), "%d × %d = %d." % (_r10(m), t, _r10(m) * t)])

    def t_compare():
        a, b = random.randint(12, 30), random.randint(12, 30)
        x, y = random.sample([3, 4, 5, 8], 2)
        while a * x == b * y:
            b += 1
        return _tb("Which is greater, %d × %d or %d × %d? Type the greater product." % (a, x, b, y), max(a * x, b * y), "int", {},
                   ["%d × %d = %d and %d × %d = %d." % (a, x, a * x, b, y, b * y)])

    def t_length():
        return _tb("A bench is %d cm long. %d benches are put end to end. How long is the row, in cm?" % (n, t), n * t, "int",
                   {"unit": "cm"}, ["%d × %d = %d cm." % (n, t, n * t)])

    return [t_partition, t_money, t_estimate, t_compare, t_length, t_grid, t_grid, t_strip, t_strip]


def _x35b(d):
    t = random.randint(2, 4) if d == 0 else pick([2, 3, 4, 5, 8])
    q = random.randint(11, 24) if d == 0 else random.randint(11, 99 // t)
    n = t * q

    def t_partition():
        a = (n // (10 * t)) * 10 * t
        if a == 0 or a == n:
            return t_halve()
        return _tb("Work out %d ÷ %d by splitting %d into %d and %d. What is the answer?" % (n, t, n, a, n - a), q, "int", {},
                   ["%d ÷ %d = %d and %d ÷ %d = %d." % (a, t, a // t, n - a, t, (n - a) // t), "%d + %d = %d." % (a // t, (n - a) // t, q)])

    def t_strip():
        return _strip("The strip shows %d split into %d equal parts. How much is each part?" % (n, t),
                      {"mode": "equal_parts", "parts": t, "partLabel": "?", "totalLabel": str(n), "unknown": "part"}, q,
                      ["%d ÷ %d = %d." % (n, t, q)])

    def t_table():
        rows = []
        for _ in range(3):
            tt = random.randint(2, 5)
            qq = random.randint(11, 99 // tt)
            rows.append([tt * qq, tt, qq])
        miss = random.randrange(3)
        return _dt("Each row shows a total shared into equal groups. Type the missing amount in each group.",
                   ["Total", "Groups", "Each group"], rows, rows[miss][2], ["%d ÷ %d = %d." % tuple(rows[miss])], missing=(miss, 2))

    def t_halve():
        m = 2 * random.randint(11, 49)
        return _tb("What is half of %d?" % m, m // 2, "int", {}, ["%d ÷ 2 = %d." % (m, m // 2)])

    def t_money():
        return _tb("£%d is shared equally between %d people. How many pounds does each person get?" % (n, t), q, "int", {"unit": "£"},
                   ["%d ÷ %d = %d." % (n, t, q)])

    def t_check():
        who = pick(NAMES)
        wrong = q + pick([-1, 1])
        return _tb("%s says %d ÷ %d = %d. Multiply to check, then type the correct answer." % (who, n, t, wrong), q, "int", {},
                   ["%d × %d = %d, not %d." % (wrong, t, wrong * t, n), "%d ÷ %d = %d." % (n, t, q)])

    def t_ribbon():
        return _tb("A ribbon %d cm long is cut into %d equal pieces. How long is each piece, in cm?" % (n, t), q, "int", {"unit": "cm"},
                   ["%d ÷ %d = %d cm." % (n, t, q)])

    def t_io():
        ins = random.sample(range(10, 99 // t + 1), 3)
        miss = random.randrange(3)
        return _io("Each Out number is the In number divided by %d. Type the missing Out number." % t, [[i * t, i] for i in ins], miss,
                   ins[miss], ["%d ÷ %d = %d." % (ins[miss] * t, t, ins[miss])], rule="÷ %d" % t)

    return [t_partition, t_halve, t_money, t_check, t_ribbon, t_strip, t_strip, t_table, t_table, t_io, t_io]


def _x35c(d):
    t = random.randint(2, 5) if d == 0 else pick([3, 4, 5, 8, 10])
    q = random.randint(2, 9)
    r = random.randint(1, t - 1)
    n = t * q + r

    def t_largest_rem():
        return _tb("When you divide a whole number by %d, what is the LARGEST remainder you can get?" % t, t - 1, "int", {},
                   ["The remainder must be smaller than %d." % t, "So the largest is %d." % (t - 1)])

    def t_reverse():
        return _tb("A number divided by %d gives %d remainder %d. What is the number?" % (t, q, r), n, "int", {},
                   ["%d × %d = %d." % (q, t, q * t), "%d + %d = %d." % (q * t, r, n)])

    def t_which():
        opts = [n]
        while len(opts) < 4:
            x = t * random.randint(2, 9)
            if x not in opts:
                opts.append(x)
        random.shuffle(opts)
        return _tb("Which of these numbers leaves a remainder when divided by %d?   %s" % (t, _lst(opts)), n, "int", {},
                   ["The others are in the %d times table." % t, "%d ÷ %d = %d remainder %d." % (n, t, q, r)])

    def t_money_left():
        c = pick([5, 10, 20])
        k = random.randint(2, 8)
        left = random.randint(1, c - 1)
        m = c * k + left
        who = pick(NAMES)
        return _tb("%s has %dp and buys as many %dp stickers as possible. How much money is left, in pence?" % (who, m, c), left, "int",
                   {"unit": "p"}, ["%d ÷ %d = %d remainder %d." % (m, c, k, left), "%dp is left." % left])

    def t_table():
        rows = []
        for _ in range(3):
            qq, rr = random.randint(2, 9), random.randint(0, t - 1)
            rows.append([t * qq + rr, qq, rr])
        miss = random.randrange(3)
        return _dt("Each number is divided by %d. Type the missing remainder." % t, ["Number", "Answer", "Remainder"], rows,
                   rows[miss][2], ["%d × %d = %d." % (rows[miss][1], t, rows[miss][1] * t),
                                   "%d − %d = %d." % (rows[miss][0], rows[miss][1] * t, rows[miss][2])], missing=(miss, 2))

    def t_teams():
        return _tb("%d children make teams of %d. How many children are left without a team?" % (n, t), r, "int", {},
                   ["%d ÷ %d = %d remainder %d." % (n, t, q, r)])

    return [t_largest_rem, t_reverse, t_which, t_money_left, t_teams, t_table, t_table]


def _x35d(d):
    t = pick([3, 4, 5, 8] if d else [2, 5, 10])
    k = random.randint(2, 6) if d == 0 else random.randint(3, 12)

    def t_price_table():
        items = random.sample([("ruler", 30), ("pencil", 15), ("rubber", 25), ("pen", 40), ("sharpener", 20)], 3)
        i = random.randrange(3)
        m = random.randint(2, 4 if d == 0 else 6)
        return _dt("The price list shows a school shop. How much do %d %ss cost, in pence?" % (m, items[i][0]), ["Item", "Price"],
                   [[nm, "%dp" % pr] for nm, pr in items], m * items[i][1],
                   ["%d × %dp = %dp." % (m, items[i][1], m * items[i][1])])

    def t_bars():
        cats = ["Red", "Blue", "Green"]
        vals = random.sample(range(2, 10), 3)
        i = random.randrange(3)
        return _bar("The chart shows votes. Each vote earns %d points. How many points did %s get?" % (t, cats[i]), cats, vals,
                    vals[i] * t, ["%s got %d votes." % (cats[i], vals[i]), "%d × %d = %d points." % (vals[i], t, vals[i] * t)])

    def t_plates():
        g = random.randint(2, 8)
        per = random.randint(2, 6)
        return _eg("Each plate has %d cakes on it. How many cakes are there altogether?" % per, g, per, g * per,
                   ["%d plates of %d." % (g, per), "%d × %d = %d." % (g, per, g * per)])

    def t_laps():
        who = pick(NAMES)
        return _tb("Each lap of the park is %d km. %s runs %d laps. How far does %s run, in km?" % (t, who, k, who),
                   t * k, "int", {"unit": "km"}, ["%d × %d = %d km." % (k, t, t * k)])

    def t_fortnight():
        p = random.randint(2, 6)
        who = pick(NAMES)
        return _tb("%s reads %d pages every day for 2 weeks. How many pages does %s read?" % (who, p, who), 14 * p, "int", {},
                   ["2 weeks = 14 days.", "14 × %d = %d pages." % (p, 14 * p)])

    return [t_laps, t_fortnight, t_price_table, t_price_table, t_bars, t_bars, t_plates, t_plates]


def _x35e(d):
    t = pick([2, 3, 4, 5] if d == 0 else [3, 4, 5, 8, 10])
    k = random.randint(2, 6) if d == 0 else random.randint(3, 12)
    n = t * k

    def t_price_table():
        price = pick([2, 4, 5, 10])
        m = random.randint(2, 9)
        thing = pick(["pencil", "badge", "sticker"])
        return _dt("The price list shows that one %s costs %dp. How many can you buy with %dp?" % (thing, price, price * m),
                   ["Item", "Price"], [[thing, "%dp" % price]], m, ["%d ÷ %d = %d." % (price * m, price, m)])

    def t_weeks():
        w = random.randint(2, 4)
        return _tb("A holiday lasts %d days. How many weeks is that?" % (7 * w), w, "int", {}, ["7 days = 1 week.", "%d ÷ 7 = %d." % (7 * w, w)])

    def t_ribbon():
        return _tb("A piece of string %d cm long is cut into %d equal pieces. How long is each piece, in cm?" % (n, t), k, "int",
                   {"unit": "cm"}, ["%d ÷ %d = %d cm." % (n, t, k)])

    def t_and_friends():
        who = pick(NAMES)
        f = t - 1
        return _tb("%s and %s share %d marbles equally. How many marbles does each person get?"
                   % (who, _pl(f, "friend"), n), k, "int", {}, ["That is %d people, not %d." % (t, f), "%d ÷ %d = %d." % (n, t, k)])

    def t_bad_ones():
        bad = random.randint(2, 6)
        tot = n + bad
        return _tb("A box holds %d apples. %d are bad. The rest are packed into bags of %d. How many bags are there?" % (tot, bad, t),
                   k, "int", {}, ["%d − %d = %d good apples." % (tot, bad, n), "%d ÷ %d = %d bags." % (n, t, k)])

    return [t_weeks, t_ribbon, t_and_friends, t_bad_ones, t_price_table, t_price_table]


def _x35f(d):
    t = pick([2, 3, 4, 5] if d == 0 else [3, 4, 8, 5])
    k = random.randint(2, 6) if d == 0 else random.randint(2, 12)
    p = t * k

    def t_balance():
        a, b = pick([(2, 6), (3, 4), (2, 12), (4, 6), (3, 8), (2, 8), (4, 4), (2, 10)])
        tot = a * b
        x = pick([y for y in (2, 3, 4, 6, 8, 12) if tot % y == 0 and y not in (a, tot)])
        return _tb("Find the missing number:  ___ × %d = %d × %d" % (x, a, b), tot // x, "int", {},
                   ["%d × %d = %d." % (a, b, tot), "%d ÷ %d = %d." % (tot, x, tot // x)])

    def t_rule():
        ins = random.sample(range(1, 13), 4)
        return _io("Each Out number is the In number multiplied by the same number. What is that number?", [[i, i * t] for i in ins],
                   None, t, ["%d × %d = %d." % (ins[0], t, ins[0] * t)])

    def t_strip():
        return _strip("The total is %d and the strip has %d equal parts. What is each part?" % (p, t),
                      {"mode": "equal_parts", "parts": t, "partLabel": "?", "totalLabel": str(p), "unknown": "part"}, k,
                      ["%d ÷ %d = %d." % (p, t, k)])

    def t_div_balance():
        a, b = pick([(3, 4), (2, 6), (2, 4), (3, 3), (2, 5)])
        q = a * b
        m = pick([2, 3, 4])
        return _tb("Find the missing number:  %d ÷ ___ = %d × %d" % (q * m, a, b), m, "int", {},
                   ["%d × %d = %d." % (a, b, q), "%d ÷ %d = %d." % (q * m, q, m)])

    def t_think():
        who = pick(NAMES)
        return _tb("%s thinks of a number and multiplies it by %d. The answer is %d. What was the number?" % (who, t, p), k, "int", {},
                   ["Undo it: %d ÷ %d = %d." % (p, t, k)])

    def t_digit():
        tt = pick([2, 3])
        a = random.randint(11, 33 if tt == 3 else 49)
        return _tb("A digit is missing:  %d□ × %d = %d. What is the missing digit?" % (a // 10, tt, a * tt), a % 10, "int", {},
                   ["%d ÷ %d = %d." % (a * tt, tt, a), "The missing digit is %d." % (a % 10)])

    def t_table():
        rows = []
        for _ in range(3):
            x, y = random.randint(2, 9), random.choice([3, 4, 8])
            rows.append([x, y, x * y])
        miss = random.randrange(3)
        return _dt("Each row shows a multiplication: first number × second number = product. Type the missing first number.",
                   ["First", "Second", "Product"], rows, rows[miss][0], ["%d ÷ %d = %d." % (rows[miss][2], rows[miss][1], rows[miss][0])],
                   missing=(miss, 0))

    return [t_balance, t_div_balance, t_think, t_digit, t_rule, t_rule, t_strip, t_strip, t_table, t_table]


@skill("Y3.5.g", "Scaling and correspondence problems", S5)
def _(d=1):
    d = _d(d)
    k = pick([2, 3, 4] if d == 0 else [2, 3, 4, 5, 8, 10])
    a = random.randint(2, 6 if d == 0 else 12)
    x, y = random.sample(NAMES, 2)

    def t_times_as_many():
        thing = pick(["stickers", "marbles", "shells", "badges"])
        return _tb("%s has %d %s. %s has %d times as many. How many %s does %s have?" % (x, a, thing, y, k, thing, y), a * k, "int", {},
                   ["%d times as many as %d is %d × %d." % (k, a, k, a), "= %d." % (a * k)])

    def t_reverse():
        thing = pick(["cards", "beads", "conkers"])
        return _tb("%s has %d %s. That is %d times as many as %s has. How many %s does %s have?" % (y, a * k, thing, k, x, thing, x),
                   a, "int", {}, ["%d ÷ %d = %d." % (a * k, k, a)])

    def t_tall():
        h = random.randint(2, 9)
        return _tb("A plant is %d cm tall. A tree is %d times as tall. How tall is the tree, in cm?" % (h, k), h * k, "int",
                   {"unit": "cm"}, ["%d × %d = %d cm." % (h, k, h * k)])

    def t_how_many_times():
        return _tb("A red ribbon is %d cm long and a blue ribbon is %d cm long. How many times longer is the blue ribbon?"
                   % (a, a * k), k, "int", {}, ["%d ÷ %d = %d." % (a * k, a, k)])

    def t_recipe():
        e = random.randint(1, 3)
        f = pick([2, 3, 4])
        return _tb("A recipe for 2 people uses %s. How many eggs are needed for %d people?" % (_pl(e, "egg"), 2 * f), e * f, "int", {},
                   ["%d people is %d times as many as 2." % (2 * f, f), "%d × %d = %d eggs." % (e, f, e * f)])

    def t_outfits():
        h, s = random.randint(2, 4), random.randint(2, 5)
        return _tb("%s has %s and %s. How many different outfits of one hat and one scarf can %s make?"
                   % (x, _pl(h, "hat"), _pl(s, "scarf", "scarves"), x), h * s, "int", {},
                   ["Each hat goes with each of the %d scarves." % s, "%d × %d = %d outfits." % (h, s, h * s)])

    def t_sandwiches():
        b, f = random.randint(2, 3), random.randint(3, 6)
        return _tb("A café has %d kinds of bread and %d fillings. A sandwich uses one bread and one filling. How many different "
                   "sandwiches can be made?" % (b, f), b * f, "int", {}, ["%d × %d = %d." % (b, f, b * f)])

    def t_meals():
        s, m, p = random.randint(2, 3), random.randint(2, 3), 2
        return _tb("A menu has %d starters, %d mains and %d puddings. A meal has one of each. How many different meals are possible?"
                   % (s, m, p), s * m * p, "int", {}, ["%d × %d × %d = %d." % (s, m, p, s * m * p)])

    def t_table():
        h, s = 2, random.randint(3, 4)
        hats = ["red hat", "blue hat"]
        scarves = ["spotty", "stripy", "plain", "checked"][:s]
        rows = [[hat] + ["✓"] * s for hat in hats]
        return _dt("The table lists every hat and scarf pair (a tick is one outfit). How many outfits are there?",
                   ["Hat"] + scarves, rows, h * s, ["%d rows of %d ticks." % (h, s), "%d × %d = %d." % (h, s, h * s)])

    def t_strip():
        return _strip("%s has %d sweets. %s has %d times as many. The strip shows %s's sweets. How many does %s have?" % (x, a, y, k, y, y),
                      {"mode": "equal_parts", "parts": k, "partLabel": str(a), "totalLabel": "?", "unknown": "total"}, a * k,
                      ["%d equal parts of %d." % (k, a), "%d × %d = %d." % (k, a, a * k)])

    def t_groups():
        g = min(k, 8)
        p = min(a, 10)
        return _eg("Each ring is one box of %d cakes. A baker makes %d times as many cakes as one box. How many cakes is that?" % (p, g),
                   g, p, g * p, ["%d × %d = %d." % (g, p, g * p)])

    def t_bars():
        b = random.randint(2, 6)
        return _bar("Red got %d times as many votes as Blue. The chart shows Blue's votes. How many votes did Red get?" % k,
                    ["Blue"], [b], b * k, ["Blue got %d." % b, "%d × %d = %d." % (b, k, b * k)])

    def t_n_to_m():
        if random.random() < 0.5:
            c, cost = pick([(2, 10), (3, 20), (4, 25), (5, 30)])
            n = random.randint(2, 4)
            return _tb("%d pencils cost %dp. How much do %d pencils cost, in pence?" % (c, cost, c * n), cost * n, "int", {"unit": "p"},
                       ["%d pencils is %d lots of %d." % (c * n, n, c), "%d × %dp = %dp." % (n, cost, cost * n)])
        c, w = pick([(4, 1), (5, 1), (6, 2), (8, 2)])
        n = random.randint(2, 5)
        return _tb("On a school trip there %s %d %s for every %d children. How many adults are needed for %d children?"
                   % ("is" if w == 1 else "are", w, "adult" if w == 1 else "adults", c, c * n), w * n, "int", {},
                   ["%d children is %d groups of %d." % (c * n, n, c), "%d × %d = %d adults." % (n, w, w * n)])

    plain = [t_times_as_many, t_reverse, t_tall, t_how_many_times, t_recipe, t_outfits, t_sandwiches, t_n_to_m]
    return _pick_t(plain + ([t_meals] if d == 2 else []),
                      [t_table, t_strip, t_groups, t_bars])



# ================================================================ 3.6 ======
def _fbar(prompt, parts, num, solution):
    return {"prompt": prompt, "component": "fraction_bar", "spec": {"parts": int(parts), "mode": "shade"},
            "answer": "%d/%d" % (num, parts), "answer_type": "frac", "solution": solution}


def _x36d(d):
    den = pick([2, 4, 5, 10] if d < 2 else [4, 5, 8, 10])

    def t_steps():
        return _tb("A number line from 0 to 1 is split into steps of 1/%d. How many steps are there from 0 to 1?" % den, den, "int", {},
                   ["%d/%d makes 1 whole." % (den, den), "So there are %d steps." % den])

    def t_halfway():
        dn = pick([4, 8, 10] if d else [4, 10])
        num = random.randint(1, dn - 1)
        return _fq("Which fraction is exactly halfway between %d/%d and %d/%d on a number line?" % (num - 1, dn, num + 1, dn),
                   Fraction(num, dn), ["One step on from %d/%d is %d/%d." % (num - 1, dn, num, dn)], "e.g. 3/8")

    def t_gap():
        dn = pick([4, 5, 8, 10])
        a, b = sorted(random.sample(range(1, dn), 2))
        return _tb("On a number line marked in steps of 1/%d, how many steps is it from %d/%d to %d/%d?" % (dn, a, dn, b, dn), b - a,
                   "int", {}, ["%d − %d = %d." % (b, a, b - a)])

    return [t_steps, t_halfway, t_gap]


def _x36e(d):
    def t_count_on():
        a = random.randint(1, 5)
        k = random.randint(2, 10 - a - 1)
        return _fq("Start at %d/10 and count on %s. Where do you finish?" % (a, _pl(k, "tenth")), Fraction(a + k, 10),
                   ["%d/10 + %d/10 = %d/10." % (a, k, a + k)], "e.g. 7/10")

    def t_to_whole():
        a = random.randint(5, 7)
        blanks = 10 - (a + 2)
        return _fq("Count on in tenths: %d/10, %d/10, %d/10, %s. What is the last missing number? (a fraction or a whole number)"
                   % (a, a + 1, a + 2, ", ".join(["___"] * blanks)), Fraction(1),
                   ["The count goes %s." % ", ".join("%d/10" % v for v in range(a + 3, 11)), "10/10 is 1 whole."], "e.g. 1")

    def t_back_from_one():
        k = random.randint(2, 6)
        return _fq("Count back in tenths from 1: 1, 9/10, 8/10, ... What is the %s number in the count (1 is the 1st)?"
                   % ["", "", "2nd", "3rd", "4th", "5th", "6th", "7th"][k + 1], Fraction(10 - k, 10),
                   ["Each step takes away 1/10.", "After %s you reach %d/10." % (_pl(k, "step"), 10 - k)], "e.g. 7/10")

    def t_missing():
        st = random.randint(1, 2)
        a = random.randint(1, 3)
        seq = [a + i * st for i in range(4)]
        miss = random.randint(1, 2)
        shown = ["%d/10" % v if i != miss else "___" for i, v in enumerate(seq)]
        return _fq("Find the missing number:  %s" % ", ".join(shown), Fraction(seq[miss], 10),
                   ["The count goes up by %s." % _pl(st, "tenth"), "The missing number is %d/10." % seq[miss]], "e.g. 5/10")

    def t_tenths_over():
        w, t = 1, random.randint(1, 9)
        return _tb("How many tenths are there in 1 and %d/10?" % t, 10 * w + t, "int", {},
                   ["1 whole is 10 tenths.", "10 + %d = %d tenths." % (t, 10 + t)])

    def t_ruler():
        v = random.randint(1, 9)
        return _ruler("The strip is 10 cm long, so each centimetre is one tenth of it. The ruler shows a piece cut from the strip. "
                      "How many tenths of the strip is the piece?", "length", v, 10, "cm", v,
                      ["The piece is %d cm." % v, "That is %d/10 of the strip." % v])

    def t_bar():
        a = random.randint(1, 5)
        k = random.randint(1, 4)
        return _fbar("Start at %d/10 and count on %s. Shade where you finish." % (a, _pl(k, "tenth")), 10, a + k,
                     ["%d/10 + %d/10 = %d/10." % (a, k, a + k)])

    plain = [t_count_on, t_to_whole, t_back_from_one, t_missing] + ([t_tenths_over] if d == 2 else [])
    return plain + [t_ruler, t_ruler, t_bar, t_bar]


def _x36h(d):
    den = pick([4, 5, 6, 8] if d == 0 else [5, 6, 7, 8, 9, 10, 12])

    def t_middle():
        ns = random.sample(range(1, den), 3)
        mid = sorted(ns)[1]
        return _fq("Put %s in order from smallest to largest. Which fraction is in the middle?" % ", ".join("%d/%d" % (n, den) for n in ns),
                   Fraction(mid, den), ["Same denominator, so compare the numerators: %s." % ", ".join(str(n) for n in sorted(ns)),
                                        "The middle one is %d/%d." % (mid, den)], "e.g. 3/8")

    def t_sign():
        a, b = random.sample(range(1, den), 2)
        if random.random() < 0.2:
            b = a
        sign = "<" if a < b else (">" if a > b else "=")
        return _wq("Compare:  %d/%d ___ %d/%d   (type <, > or =)" % (a, den, b, den), sign,
                   ["The denominators are the same, so compare %d and %d." % (a, b)], "< > =")

    def t_between():
        a = random.randint(1, den - 3)
        return _fbar("Shade a fraction of this bar that is bigger than %d/%d but smaller than %d/%d." % (a, den, a + 2, den), den, a + 1,
                     ["Only %d/%d lies between them." % (a + 1, den)])

    def t_how_many():
        a = random.randint(1, den - 2)
        return _tb("How many fractions with denominator %d are greater than %d/%d and less than 1 whole?" % (den, a, den), den - a - 1,
                   "int", {}, ["They are %d/%d up to %d/%d." % (a + 1, den, den - 1, den), "That is %d." % (den - a - 1)])

    def t_further():
        a, b = sorted(random.sample(range(1, den), 2))
        x, y = random.sample(NAMES, 2)
        return _fq("%s ran %d/%d of a track and %s ran %d/%d of it. How much further did %s run? (write the fraction)"
                   % (x, a, den, y, b, den, y), Fraction(b - a, den), ["%d/%d − %d/%d = %d/%d." % (b, den, a, den, b - a, den)], "e.g. 2/8")

    def t_missing_num():
        a = random.randint(1, den - 3)
        return _tb("?/%d is bigger than %d/%d but smaller than %d/%d. What is the missing numerator?" % (den, a, den, a + 2, den), a + 1,
                   "int", {}, ["The numerator must be between %d and %d." % (a, a + 2)])

    return [t_middle, t_sign, t_how_many, t_further, t_missing_num, t_between, t_between]


def _x36i(d):
    den = pick([3, 4, 5] if d == 0 else [5, 6, 7, 8, 9, 10])

    def t_three():
        while True:
            xs = [random.randint(1, den - 2) for _ in range(3)]
            if sum(xs) <= den:
                break
        return _fq("Work out %s." % " + ".join("%d/%d" % (x, den) for x in xs), Fraction(sum(xs), den),
                   ["Add the numerators: %s = %d." % (" + ".join(map(str, xs)), sum(xs)), "= %d/%d." % (sum(xs), den)], "e.g. 5/8")

    def t_line():
        dn = pick([4, 5, 10] if d else [4, 10])
        a = random.randint(1, dn - 2)
        b = random.randint(1, dn - a)
        return _nld("Work out %d/%d + %d/%d and mark the answer on the number line." % (a, dn, b, dn), Fraction(a + b, dn), 0, 1, 1 / dn,
                    1 / dn, ["%d/%d + %d/%d = %d/%d." % (a, dn, b, dn, a + b, dn)])

    def t_larger():
        s1, s2 = random.sample(range(2, den + 1), 2)
        a, c = random.randint(1, s1 - 1), random.randint(1, s2 - 1)
        b, e = s1 - a, s2 - c
        big = max(s1, s2)
        return _fq("Which is larger: %d/%d + %d/%d or %d/%d + %d/%d? Type the larger total as a fraction." % (a, den, b, den, c, den, e, den),
                   Fraction(big, den), ["%d/%d and %d/%d." % (a + b, den, c + e, den), "The larger is %d/%d." % (big, den)], "e.g. 5/8")

    def t_pizza():
        x, y = random.sample(NAMES, 2)
        a = random.randint(1, 4)
        b = random.randint(1, 8 - a - 1)
        return _fq("A pizza is cut into 8 equal slices. %s eats %s and %s eats %s. What fraction of the pizza has been eaten?"
                   % (x, _pl(a, "slice"), y, _pl(b, "slice")), Fraction(a + b, 8), ["%d/8 + %d/8 = %d/8." % (a, b, a + b)], "e.g. 3/8")

    def t_repeat():
        k = random.randint(2, 4)
        a = random.randint(1, (den - 1) // k)
        return _fq("Add %d/%d to itself %s altogether (%s). What is the total?" % (a, den, {2: "twice", 3: "three times", 4: "four times"}[k],
                   " + ".join(["%d/%d" % (a, den)] * k)), Fraction(a * k, den), ["%d × %d = %d, so the total is %d/%d." % (a, k, a * k, a * k, den)],
                   "e.g. 6/8")

    return [t_three, t_larger, t_pizza, t_repeat, t_line, t_line]


def _x36j(d):
    den = pick([3, 4, 5] if d == 0 else [5, 6, 7, 8, 9, 10])
    a = random.randint(2, den - 1)
    b = random.randint(1, a - 1)

    def t_line():
        dn = pick([4, 5, 10] if d else [4, 10])
        x = random.randint(2, dn)
        y = random.randint(1, x - 1)
        return _nld("Start at %d/%d and go back %d/%d. Mark where you land on the number line." % (x, dn, y, dn), Fraction(x - y, dn), 0, 1,
                    1 / dn, 1 / dn, ["%d/%d − %d/%d = %d/%d." % (x, dn, y, dn, x - y, dn)])

    def t_bigger_by():
        return _fq("How much bigger is %d/%d than %d/%d?" % (a, den, b, den), Fraction(a - b, den),
                   ["%d/%d − %d/%d = %d/%d." % (a, den, b, den, a - b, den)], "e.g. 2/8")

    def t_missing_first():
        return _fq("Find the missing fraction:  ___ − %d/%d = %d/%d" % (b, den, a - b, den), Fraction(a, den),
                   ["%d/%d + %d/%d = %d/%d." % (a - b, den, b, den, a, den)], "e.g. 6/9")

    def t_jug():
        full = random.randint(4, 9)
        out = random.randint(1, full - 1)
        return _fq("A jug is %d/10 full of water. %d/10 of the jug is poured out. What fraction of the jug is full now?" % (full, out),
                   Fraction(full - out, 10), ["%d/10 − %d/10 = %d/10." % (full, out, full - out)], "e.g. 4/10")

    def t_two_step():
        x = random.randint(1, den - 2)
        y = random.randint(1, den - x - 1)
        return _fq("Work out 1 − %d/%d − %d/%d." % (x, den, y, den), Fraction(den - x - y, den),
                   ["1 = %d/%d." % (den, den), "%d − %d − %d = %d, so %d/%d." % (den, x, y, den - x - y, den - x - y, den)], "e.g. 2/7")

    def t_cake_left():
        k = pick([6, 8, 10])
        e = random.randint(1, k - 1)
        return _fq("A cake is cut into %d equal slices and %s eaten. What fraction of the cake is left?"
                   % (k, "1 slice is" if e == 1 else "%d slices are" % e), Fraction(k - e, k),
                   ["The whole cake is %d/%d." % (k, k), "%d/%d − %d/%d = %d/%d." % (k, k, e, k, k - e, k)], "e.g. 5/8")

    def t_smaller():
        dn = max(den, 5)          # thirds allow only 2/3 − 1/3, so two different results need at least fifths
        p1, q1 = sorted(random.sample(range(1, dn), 2), reverse=True)
        p2, q2 = sorted(random.sample(range(1, dn), 2), reverse=True)
        while p1 - q1 == p2 - q2:
            p2, q2 = sorted(random.sample(range(1, dn), 2), reverse=True)
        small = min(p1 - q1, p2 - q2)
        return _fq("Which is smaller: %d/%d − %d/%d or %d/%d − %d/%d? Type the smaller answer." % (p1, dn, q1, dn, p2, dn, q2, dn),
                   Fraction(small, dn), ["%d/%d and %d/%d." % (p1 - q1, dn, p2 - q2, dn), "The smaller is %d/%d." % (small, dn)], "e.g. 2/7")

    return [t_bigger_by, t_missing_first, t_jug, t_two_step, t_cake_left, t_smaller, t_line, t_line]


def _x36k(d):
    n = random.randint(1, 9)

    def t_ribbon():
        return _fq("%d m of ribbon is shared equally between 10 children. What fraction of a metre does each child get?" % n,
                   Fraction(n, 10), ["%d ÷ 10 = %d/10." % (n, n)], "e.g. 3/10")

    def t_reverse():
        return _tb("Some pizzas are shared equally between 10 people and each person gets %d/10 of a pizza. How many pizzas were "
                   "shared?" % n, n, "int", {}, ["10 people × %d/10 = %d/10 = %d." % (n, 10 * n, n)])

    def t_tenth_of():
        m = 10 * random.randint(2, 9 if d < 2 else 99)
        return _tb("What is 1/10 of %d?" % m, m // 10, "int", {}, ["Finding 1/10 means dividing by 10.", "%d ÷ 10 = %d." % (m, m // 10)])

    def t_tenth_cm():
        m = 10 * random.randint(2, 10)
        return _tb("A rope is %d cm long. It is cut into 10 equal pieces. How long is each piece, in cm?" % m, m // 10, "int",
                   {"unit": "cm"}, ["%d ÷ 10 = %d cm." % (m, m // 10)])

    def t_table():
        ns = random.sample(range(1, 10), 3)
        miss = random.randrange(3)
        return _dt("Complete the table: divide each number by 10 and write the answer as a fraction.", ["Number", "÷ 10"],
                   [[x, "%d/10" % x] for x in ns], "%d/10" % ns[miss], ["%d ÷ 10 = %d/10." % (ns[miss], ns[miss])], missing=(miss, 1),
                   atype="frac", placeholder="e.g. 3/10")

    return [t_ribbon, t_reverse, t_tenth_of, t_tenth_cm, t_table, t_table]


# ================================================================ 3.7 ======
def _x37b(d):
    def t_mm():
        a = random.randint(60, 150)
        b = random.randint(5, 40)
        return _tb("A pencil is %d mm long. It is sharpened and loses %d mm. How long is it now, in mm?" % (a, b), a - b, "int",
                   {"unit": "mm"}, ["%d − %d = %d mm." % (a, b, a - b)])

    def t_m_cm_add():
        m1, c1, m2, c2 = random.randint(1, 3), 10 * random.randint(1, 5), random.randint(1, 3), 10 * random.randint(1, 4)
        tot = 100 * (m1 + m2) + c1 + c2
        return _tb("Add %d m %d cm and %d m %d cm. Give your answer in cm." % (m1, c1, m2, c2), tot, "int", {"unit": "cm"},
                   ["%d cm + %d cm = %d cm." % (100 * m1 + c1, 100 * m2 + c2, tot)])

    def t_to_metre():
        c = random.randint(11, 89)
        return _tb("A ribbon is %d cm long. How much more ribbon is needed to make 1 m?" % c, 100 - c, "int", {"unit": "cm"},
                   ["1 m = 100 cm.", "100 − %d = %d cm." % (c, 100 - c)])

    def t_mixed_diff():
        c = random.randint(3, 12)
        m = random.randint(10, 10 * c - 5)
        while m == 10 * c:
            m += 3
        return _tb("A worm is %d cm long and a caterpillar is %d mm long. What is the difference in their lengths, in mm?" % (c, m),
                   abs(10 * c - m), "int", {"unit": "mm"}, ["%d cm = %d mm." % (c, 10 * c), "%d − %d = %d mm." % (max(10 * c, m), min(10 * c, m), abs(10 * c - m))])

    def t_bars():
        cats = random.sample(NAMES, 3)
        vals = random.sample(range(60, 190, 10), 3)
        i, j = random.sample(range(3), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        return _bar("The chart shows how far three children jumped, in cm. How much further did %s jump than %s, in cm?" % (cats[i], cats[j]),
                    cats, vals, vals[i] - vals[j], ["%d − %d = %d cm." % (vals[i], vals[j], vals[i] - vals[j])])

    def t_table():
        vals = [random.randint(12, 60) for _ in range(3)]
        return _dt("The table shows three pieces of ribbon. What is their total length, in cm?", ["Ribbon", "Length (cm)"],
                   [["Red", vals[0]], ["Blue", vals[1]], ["Green", vals[2]]], sum(vals),
                   ["%d + %d + %d = %d cm." % (vals[0], vals[1], vals[2], sum(vals))])

    return [t_mm, t_m_cm_add, t_to_metre, t_mixed_diff, t_bars, t_bars, t_table, t_table]


# ================================================================ 3.8 ======
_RN = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]


def _x38b(d):
    h = random.randint(1, 12)

    def t_roman():
        m5 = random.randint(1, 11)
        return _time("On a clock with Roman numerals, the hour hand is just past %s and the minute hand points to %s. Write the time "
                     "in digital form (h:mm)." % (_RN[h % 12], _RN[m5]), h, 5 * m5,
                     ["%s is %d, so it is after %d o'clock." % (_RN[h % 12], h, h), "The minute hand on %s means %d minutes past." % (_RN[m5], 5 * m5)])

    def t_points_to():
        k = random.randint(1, 11)
        return _tb("The minute hand points to the %d. How many minutes past the hour is it?" % k, 5 * k, "int", {"unit": "minutes"},
                   ["Each number on the clock is 5 minutes.", "%d × 5 = %d minutes." % (k, 5 * k)])

    def t_minutes_to():
        mm = pick([5, 10, 20, 25])
        nh = h % 12 + 1
        return _time("Write '%d minutes to %d' in digital form (h:mm)." % (mm, nh), h, 60 - mm,
                     ["%d minutes to %d is %d minutes after %d o'clock." % (mm, nh, 60 - mm, h), "= %s." % _hm(h, 60 - mm)])

    def t_small_marks():
        k = random.randint(1, 10)
        extra = random.randint(1, 4)
        return _tb("The minute hand is %s after the %d. How many minutes past the hour is it?" % (_pl(extra, "small mark"), k),
                   5 * k + extra, "int", {"unit": "minutes"}, ["The %d means %d minutes." % (k, 5 * k), "%d + %d = %d." % (5 * k, extra, 5 * k + extra)])

    def t_how_many_to():
        m = random.randint(1, 11) * 5 + (random.randint(1, 4) if d == 2 else 0)
        return _tb("The time is %s. How many minutes are there until %d o'clock?" % (_hm(h, m), h % 12 + 1), 60 - m, "int",
                   {"unit": "minutes"}, ["60 − %d = %s." % (m, _pl(60 - m, "minute"))])

    def t_to_form():
        mm = pick([35, 40, 45, 50, 55])
        return _tb("%s is ___ minutes to %d. What is the missing number?" % (_hm(h, mm), h % 12 + 1), 60 - mm, "int", {},
                   ["60 − %d = %d." % (mm, 60 - mm)])

    return [t_roman, t_points_to, t_minutes_to, t_small_marks, t_how_many_to, t_to_form]


def _x38d(d):
    h = random.randint(1, 12)

    def t_compare():
        x, y = random.sample(NAMES, 2)
        s1, s2 = 5 * random.randint(0, 3), 5 * random.randint(0, 3)
        l1, l2 = 5 * random.randint(3, 8), 5 * random.randint(3, 8)
        while l1 == l2:
            l2 = 5 * random.randint(3, 8)
        longer = x if l1 > l2 else y
        return _tb("%s walks from %s to %s. %s walks from %s to %s. How many minutes longer is %s's walk?"
                   % (x, _hm(h, s1), _hm(h, s1 + l1), y, _hm(h, s2), _hm(h, s2 + l2), longer), abs(l1 - l2), "int", {"unit": "minutes"},
                   ["%s: %d minutes. %s: %d minutes." % (x, l1, y, l2), "%d − %d = %d minutes." % (max(l1, l2), min(l1, l2), abs(l1 - l2))])

    def t_tv():
        shows = random.sample(["Cartoons", "News", "Quiz", "Nature", "Music"], 3)
        starts = [0]
        for _ in range(3):
            starts.append(starts[-1] + 5 * random.randint(2, 4))
        i = random.randrange(3)
        return _dt("The TV guide shows start times. Each show ends when the next one starts. How many minutes long is %s?" % shows[i],
                   ["Show", "Starts"], [[sh, _hm(h, st)] for sh, st in zip(shows, starts)] + [["Bedtime story", _hm(h, starts[3])]],
                   starts[i + 1] - starts[i], ["%s starts at %s and ends at %s." % (shows[i], _hm(h, starts[i]), _hm(h, starts[i + 1])),
                                               "That is %d minutes." % (starts[i + 1] - starts[i])])

    def t_end_typed():
        s = 5 * random.randint(0, 6)
        l = 5 * random.randint(2, 11 - s // 5)
        return _time("A cake goes into the oven at %s and needs %d minutes. What time does it come out? (h:mm)" % (_hm(h, s), l), h, s + l,
                     ["%s + %d minutes = %s." % (_hm(h, s), l, _hm(h, s + l))])

    def t_quarter():
        f, mins = pick([("a quarter of an hour", 15), ("half an hour", 30), ("three quarters of an hour", 45)])
        return _tb("How many minutes are there in %s?" % f, mins, "int", {"unit": "minutes"}, ["1 hour = 60 minutes.", "%s = %d minutes." % (f.capitalize(), mins)])

    def t_bars():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = random.sample(range(10, 60, 5), 4)
        i, j = random.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        return _bar("The chart shows how many minutes %s spent reading each day. How many more minutes on %s than on %s?"
                    % (pick(NAMES), cats[i], cats[j]), cats, vals, vals[i] - vals[j], ["%d − %d = %d minutes." % (vals[i], vals[j], vals[i] - vals[j])])

    return [t_compare, t_end_typed, t_quarter, t_tv, t_tv, t_bars, t_bars]


def _x38e(d):
    h = random.randint(1, 11)

    def t_timetable():
        stops = random.sample(["Park", "Library", "School", "Market", "Station", "Pool"], 4)
        t0 = 60 * h + 5 * random.randint(6, 10)
        times = [t0]
        for _ in range(3):
            times.append(times[-1] + 5 * random.randint(3, 6))
        i, j = sorted(random.sample(range(4), 2))
        return _dt("The bus timetable shows when the bus reaches each stop. How many minutes does the bus take from %s to %s?" % (stops[i], stops[j]),
                   ["Stop", "Time"], [[st, _hm(*_split(t))] for st, t in zip(stops, times)], times[j] - times[i],
                   ["%s to %s." % (_hm(*_split(times[i])), _hm(*_split(times[j]))), "That is %d minutes." % (times[j] - times[i])])

    def t_compare():
        a0, b0 = 60 * h + 5 * random.randint(6, 11), 60 * h + 5 * random.randint(4, 11)
        la, lb = 5 * random.randint(5, 16), 5 * random.randint(5, 16)
        while la == lb:
            lb = 5 * random.randint(5, 16)
        return _tb("Film A runs from %s to %s. Film B runs from %s to %s. How many minutes longer is the longer film?"
                   % (_hm(*_split(a0)), _hm(*_split(a0 + la)), _hm(*_split(b0)), _hm(*_split(b0 + lb))), abs(la - lb), "int", {"unit": "minutes"},
                   ["Film A: %d minutes. Film B: %d minutes." % (la, lb), "%d − %d = %d." % (max(la, lb), min(la, lb), abs(la - lb))])

    def t_end():
        s = 60 * h + 5 * random.randint(6, 11)
        l = 5 * random.randint(4, 12)
        return _time("A football match starts at %s and lasts %d minutes. What time does it end? (h:mm)" % (_hm(*_split(s)), l),
                     *_split(s + l), ["%s + %d minutes = %s." % (_hm(*_split(s)), l, _hm(*_split(s + l)))])

    def t_start():
        e = 60 * (h + 1) + 5 * random.randint(0, 6)
        l = 5 * random.randint(6, 12)
        return _time("A swim finished at %s. It lasted %d minutes. What time did it start? (h:mm)" % (_hm(*_split(e)), l),
                     *_split(e - l), ["%s − %d minutes = %s." % (_hm(*_split(e)), l, _hm(*_split(e - l)))])

    def t_long():
        s = 60 * h + 5 * random.randint(6, 11)
        l = 5 * random.randint(14, 22)
        return _tb("How many minutes are there from %s to %s?" % (_hm(*_split(s)), _hm(*_split(s + l))), l, "int", {"unit": "minutes"},
                   ["Count on to the next o'clock, then on again.", "That is %d minutes." % l])

    def t_buses():
        s = 60 * h + 5 * random.randint(6, 11)
        gap = pick([15, 20, 25])
        k = random.randint(2, 3)
        return _time("A bus leaves at %s and then every %d minutes. What time does the %s bus after it leave? (h:mm)"
                     % (_hm(*_split(s)), gap, ["", "", "2nd", "3rd"][k]), *_split(s + k * gap),
                     ["%s." % ", ".join(_hm(*_split(s + i * gap)) for i in range(k + 1))])

    def t_later():
        s = 60 * h + 5 * random.randint(1, 11)
        l = 60 + 5 * random.randint(1, 11)
        return _time("It is %s. What time will it be in 1 hour and %d minutes? (h:mm)" % (_hm(*_split(s)), l - 60), *_split(s + l),
                     ["1 hour later is %s." % _hm(*_split(s + 60)), "%d minutes more is %s." % (l - 60, _hm(*_split(s + l)))])

    return [t_compare, t_end, t_start, t_long, t_buses, t_later, t_timetable, t_timetable]


def _x38j(d):
    def t_classify():
        deg = pick([random.randint(20, 75), 90, random.randint(105, 165)])
        word = "acute" if deg < 90 else ("right" if deg == 90 else "obtuse")
        return {"prompt": "Is this angle acute, right or obtuse? (type the word)", "component": "angle",
                "spec": {"mode": "classify", "degrees": deg}, "answer": word, "answer_type": "str",
                "solution": ["Compare it with a right angle (a square corner).",
                             "It is %s." % {"acute": "smaller than a right angle, so acute", "right": "a right angle",
                                            "obtuse": "bigger than a right angle, so obtuse"}[word]]}

    def t_turn():
        k = random.randint(1, 4)
        return {"prompt": "How many right angles make this turn?", "component": "angle",
                "spec": {"mode": "turn", "degrees": 90 * k}, "answer": k, "answer_type": "int",
                "solution": ["A quarter turn is 1 right angle.", "This turn is %s." % _pl(k, "right angle")]}

    def t_shape():
        name, obtuse = pick([("pentagon", 5), ("hexagon", 6), ("octagon", 8), ("square", 0), ("triangle", 0)])
        return {"prompt": "This is a regular shape. How many of its angles are bigger than a right angle?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "vertices"}, "answer": obtuse, "answer_type": "int",
                "solution": ["Compare each corner with a square corner.",
                             "%s." % ("All %d angles are obtuse" % obtuse if obtuse else "None of the angles is bigger than a right angle")]}

    def t_letters():
        letter, n = pick([("L", 1), ("T", 2), ("E", 4), ("H", 4), ("F", 3)])
        return _tb("The capital letter %s is written with straight lines that meet at square corners. How many right angles does it have?" % letter,
                   n, "int", {}, ["Count the square corners where the lines meet.", "%s has %s." % (letter, _pl(n, "right angle"))])

    return [t_letters, t_classify, t_classify, t_turn, t_turn, t_shape, t_shape]


# ================================================================ 3.9 ======
def _x39h(d):
    def t_shop():
        items = random.sample([("apple", 20), ("banana", 15), ("orange", 25), ("pear", 30)], 2)
        a, b = random.randint(1, 3), random.randint(1, 2)
        cost = a * items[0][1] + b * items[1][1]
        return _dt("The price list shows a fruit stall. %s buys %d %s and %d %s and pays with a £1 coin. How much change, in pence?"
                   % (pick(NAMES), a, items[0][0] + ("s" if a > 1 else ""), b, items[1][0] + ("s" if b > 1 else "")),
                   ["Fruit", "Price"], [[nm, "%dp" % pr] for nm, pr in items], 100 - cost,
                   ["%d × %dp + %d × %dp = %dp." % (a, items[0][1], b, items[1][1], cost), "100p − %dp = %dp." % (cost, 100 - cost)])

    def t_pict():
        cats = ["Cats", "Dogs", "Fish"]
        key = pick([2, 5])
        vals = [key * random.randint(2, 6) for _ in cats]
        while vals[0] + vals[1] <= vals[2]:
            vals = [key * random.randint(2, 6) for _ in cats]
        return _pict("The pictogram shows pets owned by a class (each symbol stands for %d). How many more cats and dogs together than "
                     "fish are there?" % key, cats, vals, key, "circle", vals[0] + vals[1] - vals[2],
                     ["Cats %d, dogs %d, fish %d." % tuple(vals), "%d + %d − %d = %d." % (vals[0], vals[1], vals[2], vals[0] + vals[1] - vals[2])])

    def t_swim():
        p = pick([50, 60, 75])
        k = random.randint(2, 3)
        return _tb("A swim costs %dp. %s swims %d times a week for 2 weeks. How much does that cost, in pence?" % (p, pick(NAMES), k),
                   2 * k * p, "int", {"unit": "p"}, ["%d × 2 = %d swims." % (k, 2 * k), "%d × %dp = %dp." % (2 * k, p, 2 * k * p)])

    def t_strip_cut():
        piece = 2 * random.randint(4, 15)
        tot = 3 * piece
        return _tb("A strip of card %d cm long is cut into 3 equal pieces. One piece is cut in half. How long is each half, in cm?" % tot,
                   piece // 2, "int", {"unit": "cm"}, ["%d ÷ 3 = %d cm." % (tot, piece), "%d ÷ 2 = %d cm." % (piece, piece // 2)])

    def t_quarter_eaten():
        tot = 12 * random.randint(1, 4)
        left = tot - tot // 4
        k = pick([x for x in (2, 3) if left % x == 0])
        return _tb("A bag has %d sweets. 1/4 of them are eaten. The rest are shared equally between %d friends. How many does each friend get?"
                   % (tot, k), left // k, "int", {}, ["1/4 of %d = %d." % (tot, tot // 4), "%d − %d = %d." % (tot, tot // 4, left),
                                                      "%d ÷ %d = %d." % (left, k, left // k)])

    def t_twice():
        x, y = random.sample(NAMES, 2)
        a = random.randint(6, 25)
        return _tb("%s has %d stamps. %s has twice as many. How many stamps do they have altogether?" % (x, a, y), 3 * a, "int", {},
                   ["%s has %d × 2 = %d." % (y, a, 2 * a), "%d + %d = %d." % (a, 2 * a, 3 * a)])

    def t_strip_share():
        k = random.randint(3, 5)
        each = random.randint(2, 9)
        return _strip("%d friends share the cost of a present equally. Each pays £%d. The strip shows the shares. How much does the present cost, in pounds?"
                      % (k, each), {"mode": "equal_parts", "parts": k, "partLabel": "£%d" % each, "totalLabel": "?", "unknown": "total"},
                      k * each, ["%d × £%d = £%d." % (k, each, k * each)])

    return [t_swim, t_strip_cut, t_quarter_eaten, t_twice, t_shop, t_shop, t_pict, t_pict, t_strip_share, t_strip_share]


# ============================================================ new skills ====
@skill("Y3.3.h", "Subtract ones, tens or hundreds from a 3-digit number", S3)
def _(d=1):
    d = _d(d)

    def amount():
        unit = pick([1, 10, 100] if d else [1, 10])
        return unit * random.randint(1, 9), unit

    def start(sub, unit, cross=False):
        """A 3-digit start whose answer stays 3-digit; cross=True makes the subtraction cross a ten or a hundred."""
        while True:
            n = random.randint(sub + 100 if unit < 100 else sub + 1, 999)
            if (sub // unit > n // unit % 10) == cross:
                return n

    def t_bare():
        sub, unit = amount()
        n = start(sub, unit, cross=(d == 2 and unit != 100))
        return _tb("Work out %d − %d (mentally)." % (n, sub), n - sub, "int", {},
                   ["Take %s away from the %s." % (_u(sub // unit, {1: "ones", 10: "tens", 100: "hundreds"}[unit]),
                                                 {1: "ones", 10: "tens", 100: "hundreds"}[unit]), "%d − %d = %d." % (n, sub, n - sub)])

    def t_words():
        sub, unit = amount()
        n = start(sub, unit)
        return _tb("Work out %s minus %d." % (n_words(n), sub), n - sub, "int", {}, ["%s is %d." % (n_words(n).capitalize(), n),
                                                                                    "%d − %d = %d." % (n, sub, n - sub)])

    def t_missing():
        sub, unit = amount()
        n = start(sub, unit)
        return _tb("Find the missing number:  %d − ___ = %d" % (n, n - sub), sub, "int", {}, ["%d − %d = %d." % (n, n - sub, sub)])

    def t_build():
        sub, unit = amount()
        n = start(sub, unit)
        return _bt("Work out %d − %d, then build the answer with base ten blocks." % (n, sub), n - sub, ["%d − %d = %d." % (n, sub, n - sub)])

    def t_line():
        unit = pick([10, 100] if d else [10])
        sub = unit * random.randint(1, 4)
        n = unit * random.randint(5, 9) if unit == 100 else 10 * random.randint(15, 95)
        return _nl("Start at %d and jump back %d. Mark where you land." % (n, sub), n - sub, unit, 50 if unit == 10 else 100,
                   ["%d − %d = %d." % (n, sub, n - sub)])

    def t_io():
        unit = pick([10, 100] if d else [1, 10])
        sub = unit * random.randint(1, 3)
        ins = random.sample(range(sub + 100, 1000), 4)
        miss = random.randrange(4)
        return _io("Subtract %d from each In number. Type the missing Out number." % sub, [[i, i - sub] for i in ins], miss, ins[miss] - sub,
                   ["%d − %d = %d." % (ins[miss], sub, ins[miss] - sub)], rule="− %d" % sub)

    def t_pages():
        sub, unit = amount()
        n = start(sub, unit)
        who = pick(NAMES)
        return _tb("A book has %d pages. %s has read %s. How many pages are left to read?" % (n, who, _pl(sub, "page")), n - sub, "int", {},
                   ["%d − %d = %d pages." % (n, sub, n - sub)])

    def t_reverse():
        sub, unit = amount()
        n = start(sub, unit)
        return _tb("I think of a number and subtract %d. The answer is %d. What was my number?" % (sub, n - sub), n, "int", {},
                   ["Undo it: %d + %d = %d." % (n - sub, sub, n)])

    def t_count_back():
        unit = pick([10, 100] if d else [1, 10])
        n = random.randint(4 * unit + 100, 999)
        return _tb("Count back in %ds: %d, %d, %d, ___ . What comes next?" % (unit, n, n - unit, n - 2 * unit), n - 3 * unit, "int", {},
                   ["Each step takes away %d." % unit, "%d − %d = %d." % (n - 2 * unit, unit, n - 3 * unit)])

    def t_compare():
        n = random.randint(320, 999)
        a, b = pick([(100, 10), (10, 1), (100, 1)])
        return _tb("Which is smaller, %d − %d or %d − %d? Type the smaller answer." % (n, a, n, b), n - a, "int", {},
                   ["%d − %d = %d and %d − %d = %d." % (n, a, n - a, n, b, n - b), "Taking away more leaves less."])

    def t_two():
        n = random.randint(400, 999)
        h, t = 100 * random.randint(1, n // 100 - 1), 10 * random.randint(1, 9)
        return _tb("Work out %d − %d − %d." % (n, h, t), n - h - t, "int", {},
                   ["%d − %d = %d." % (n, h, n - h), "%d − %d = %d." % (n - h, t, n - h - t)])

    def t_error():
        k = random.randint(1, 5)
        n = 100 * random.randint(k + 1, 9) + 10 * random.randint(k, 9) + random.randint(0, 9)
        sub = 10 * k
        who = pick(NAMES)
        return _tb("%s says %d − %d = %d. %s took away hundreds instead of tens. What is the correct answer?" % (who, n, sub, n - 100 * k, who),
                   n - sub, "int", {}, ["%d is %s." % (sub, _u(k, "tens")), "%d − %d = %d." % (n, sub, n - sub)])

    def t_strip():
        sub, unit = amount()
        n = start(sub, unit)
        return _strip("The whole is %d and one part is %d. What is the other part?" % (n, sub),
                      {"mode": "part_whole", "parts": 2, "totalLabel": str(n), "partLabel": str(sub), "unknown": "part"}, n - sub,
                      ["%d − %d = %d." % (n, sub, n - sub)])

    return _pick_t([t_bare, t_words, t_missing, t_pages, t_reverse, t_count_back, t_compare, t_two, t_error],
                   [t_build, t_line, t_io, t_strip])


@skill("Y3.8.o", "12-hour and 24-hour clocks; a.m. and p.m.", S8)
def _(d=1):
    d = _d(d)
    h12 = random.randint(1, 11)
    m = 5 * random.randint(0, 11) if d < 2 else random.randint(0, 59)

    def t_to_24():
        return _wq("Write %s p.m. as a 24-hour clock time (like 15:30)." % _hm(h12, m), "%d:%02d" % (h12 + 12, m),
                   ["For p.m. times add 12 to the hour.", "%d + 12 = %d, so %d:%02d." % (h12, h12 + 12, h12 + 12, m)], "e.g. 15:30")

    def t_to_12():
        return _wq("Write %d:%02d as a 12-hour clock time, without a.m. or p.m. (like 4:05)." % (h12 + 12, m), _hm(h12, m),
                   ["Take 12 from the hour: %d − 12 = %d." % (h12 + 12, h12), "It is %s p.m." % _hm(h12, m)], "e.g. 4:05")

    def t_am_pm():
        hh = random.randint(0, 23)
        word = "a.m." if hh < 12 else "p.m."
        return _wq("Is %02d:%02d in the morning (a.m.) or after midday (p.m.)? Type a.m. or p.m." % (hh, m), "am" if hh < 12 else "pm",
                   ["Times before 12:00 are a.m.; from 12:00 they are p.m.", "%02d:%02d is %s" % (hh, m, word)], "am / pm")

    def t_part_of_day():
        hh, part = pick([(7, "morning"), (9, "morning"), (10, "morning"), (14, "afternoon"), (15, "afternoon"), (16, "afternoon"),
                         (19, "evening"), (20, "evening"), (21, "evening")])
        return _wq("%d:%02d — is that in the morning, afternoon or evening? (type the word)" % (hh, m), part,
                   ["%d:%02d is %s %s" % (hh, m, _hm(hh, m), "a.m." if hh < 12 else "p.m."), "That is the %s." % part], "morning / afternoon / evening")

    def t_noon():
        if random.random() < 0.5:
            return _tb("How many hours are there from 12 noon to %d p.m.?" % h12, h12, "int", {"unit": "hours"},
                       ["Noon is 12 o'clock in the middle of the day.", "Then count on %s." % _pl(h12, "hour")])
        return _tb("How many hours are there from midnight to %d a.m.?" % h12, h12, "int", {"unit": "hours"},
                   ["Midnight is 12 o'clock at night.", "Then count on %s." % _pl(h12, "hour")])

    def t_hours_between():
        a = random.randint(6, 11)
        b = random.randint(13, 20)
        return _tb("A shop opens at %02d:00 and closes at %d:00. How many hours is it open?" % (a, b), b - a, "int", {"unit": "hours"},
                   ["%d − %d = %d hours." % (b, a, b - a)])

    def t_film_end():
        s = 60 * (h12 + 12) + 5 * random.randint(6, 11)
        l = 5 * random.randint(4, 10)
        e = s + l
        return _wq("A film starts at %d:%02d and lasts %d minutes. What time does it end? Use the 24-hour clock (like 19:45)." % (s // 60, s % 60, l),
                   "%d:%02d" % (e // 60, e % 60), ["%d:%02d + %d minutes = %d:%02d." % (s // 60, s % 60, l, e // 60, e % 60)], "e.g. 19:45")

    def t_across_noon():
        s = 60 * random.randint(10, 11) + 5 * random.randint(0, 11)
        e = 60 * random.randint(12, 13) + 5 * random.randint(0, 11)
        sh, sm = _split(s)
        eh, em = _split(e)
        return _tb("A trip starts at %s a.m. and ends at %s p.m. How many minutes does it last?" % (_hm(sh, sm), _hm(eh, em)), e - s, "int",
                   {"unit": "minutes"}, ["Count on to 12 noon: %d minutes." % (720 - s), "Then on to %s p.m.: %d minutes." % (_hm(eh, em), e - 720),
                                         "%d + %d = %d minutes." % (720 - s, e - 720, e - s)])

    def t_set():
        return _clock("Set the clock to show %d:%02d." % (h12 + 12, m), h12, m,
                      ["%d:%02d is %s p.m." % (h12 + 12, m, _hm(h12, m)), "The hour hand goes near %d." % h12])

    def t_timetable():
        stops = random.sample(["Leeds", "York", "Hull", "Bath", "Derby"], 3)
        t0 = 60 * random.randint(13, 18) + 5 * random.randint(0, 6)
        times = [t0, t0 + 5 * random.randint(5, 9)]
        times.append(times[-1] + 5 * random.randint(5, 12))
        i, j = pick([(0, 1), (1, 2), (0, 2)])
        return _dt("The train timetable uses the 24-hour clock. How many minutes does the train take from %s to %s?" % (stops[i], stops[j]),
                   ["Station", "Time"], [[st, "%d:%02d" % (t // 60, t % 60)] for st, t in zip(stops, times)], times[j] - times[i],
                   ["%d:%02d to %d:%02d." % (times[i] // 60, times[i] % 60, times[j] // 60, times[j] % 60), "That is %d minutes." % (times[j] - times[i])])

    def t_am_to_24():
        hh = random.randint(1, 9)
        return _wq("Write %s a.m. as a 24-hour clock time using four digits (like 09:15)." % _hm(hh, m), "%02d:%02d" % (hh, m),
                   ["Morning times keep the same hour.", "Write it with four digits: %02d:%02d." % (hh, m)], "e.g. 09:15")

    def t_noon_or_midnight():
        pm = random.random() < 0.5
        mm = 5 * random.randint(1, 11)
        return _wq("Is 12:%02d %s a few minutes after noon or a few minutes after midnight? (type noon or midnight)" % (mm, "p.m." if pm else "a.m."),
                   "noon" if pm else "midnight", ["12 noon is 12:00 p.m.; midnight is 12:00 a.m.",
                                                  "So 12:%02d %s is just after %s." % (mm, "p.m." if pm else "a.m.", "noon" if pm else "midnight")],
                   "noon / midnight")

    return _pick_t([t_to_24, t_to_12, t_am_pm, t_part_of_day, t_noon, t_hours_between, t_film_end, t_across_noon,
                    t_am_to_24, t_noon_or_midnight],
                   [t_set, t_timetable])


# ============================================================ wiring =======
for _key, _n, _b in [
    ("Y3.0.c", 7, _x30c), ("Y3.0.f", 8, _x30f),
    ("Y3.1.a", 7, _x31a), ("Y3.1.c", 6, _x31c), ("Y3.1.d", 6, _x31d), ("Y3.1.e", 6, _x31e), ("Y3.1.f", 7, _x31f),
    ("Y3.2.b", 7, _x32b), ("Y3.2.d", 7, _x32d), ("Y3.2.e", 8, _x32e), ("Y3.2.f", 8, _x32f),
    ("Y3.3.b", 7, lambda d: _column_set("add")), ("Y3.3.c", 6, lambda d: _column_set("carry")),
    ("Y3.3.d", 7, lambda d: _column_set("sub")), ("Y3.3.e", 6, lambda d: _column_set("exchange")),
    ("Y3.3.f", 6, _x33f), ("Y3.3.g", 6, _x33g),
    ("Y3.4.b", 7, _table_extra([3])), ("Y3.4.c", 7, _table_extra([4])), ("Y3.4.d", 7, _table_extra([8])),
    ("Y3.4.e", 7, _table_extra([2, 5, 10])), ("Y3.4.f", 8, _x34f), ("Y3.4.g", 5, _x34g), ("Y3.4.h", 7, _x34h), ("Y3.4.i", 8, _x34i),
    ("Y3.5.a", 7, _x35a), ("Y3.5.b", 7, _x35b), ("Y3.5.c", 6, _x35c), ("Y3.5.d", 8, _x35d), ("Y3.5.e", 9, _x35e), ("Y3.5.f", 5, _x35f),
    ("Y3.6.d", 8, _x36d), ("Y3.6.e", 8, _x36e), ("Y3.6.h", 6, _x36h), ("Y3.6.i", 6, _x36i), ("Y3.6.j", 6, _x36j), ("Y3.6.k", 8, _x36k),
    ("Y3.7.b", 7, _x37b),
    ("Y3.8.b", 6, _x38b), ("Y3.8.d", 5, _x38d), ("Y3.8.e", 6, _x38e), ("Y3.8.j", 7, _x38j),
    ("Y3.9.h", 6, _x39h),
]:
    _more(_key, _n, _b)
