# Year 5 generators: strands 5.4 and 5.5.
#
# Multiplication and division: mental methods, short multiplication, long multiplication by a
# 2-digit number, short division with remainders in context, ×/÷ 10, 100, 1000 (whole numbers and
# decimals), scaling and simple rates, mixed operations.  Fractions: equivalence (incl. tenths and
# hundredths), comparing related denominators, mixed numbers and improper fractions, adding and
# subtracting related denominators, multiplying fractions and mixed numbers by whole numbers.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S4 = "5.4 Multiplication & division"
S5 = "5.5 Fractions"


# ================================================================== 5.4 ======
@skill("Y5.4.a", "Multiply mentally using known facts", S4)
def _(d=1):
    d = _d(d)
    a, b = random.randint(_by(d, 2, 2, 3), _by(d, 5, 9, 9)), random.randint(_by(d, 2, 2, 3), _by(d, 6, 12, 12))

    def t_tens():
        k = pick([10, 100, 1000][: _by(d, 2, 3, 3)])
        j = pick([1, 10, 100][: _by(d, 1, 2, 3)])
        return _tb("Work out %s × %s." % (_c(a * k), _c(b * j)), a * k * b * j, "int", {},
                   ["%d × %d = %d." % (a, b, a * b),
                    "Then × %s: %s." % (_c(k * j), _c(a * b * k * j))])

    def t_double():
        n = random.randint(13, _by(d, 49, 99, 499))
        return _tb("Work out %d × 4 by doubling twice." % n, n * 4, "int", {},
                   ["Double %d is %d; double again is %d." % (n, 2 * n, 4 * n)])

    def t_partition():
        n = random.choice([v for v in range(12, _by(d, 39, 99, 199) + 1) if v % 10])
        m = random.randint(3, 9)
        t, o = (n // 10) * 10, n % 10
        return _tb("Work out %d × %d by partitioning %d into %d and %d." % (n, m, n, t, o), n * m, "int",
                   {}, ["%d × %d = %d and %d × %d = %d." % (t, m, t * m, o, m, o * m),
                        "%d + %d = %d." % (t * m, o * m, n * m)])

    def t_near():
        m = random.randint(3, 9)
        n = pick(_by(d, [19, 29, 39], [19, 29, 39, 49, 99, 199], [49, 99, 199, 299, 499]))
        return _tb("Work out %d × %d. Hint: work out %d × %d and subtract %d." % (n, m, n + 1, m, m),
                   n * m, "int", {}, ["%d × %d = %d." % (n + 1, m, (n + 1) * m),
                                      "%d − %d = %d." % ((n + 1) * m, m, n * m)])

    def t_by5():
        n = random.randint(*_by(d, (6, 24), (12, 98), (50, 499))) * 2
        return _tb("Work out %s × 5. Hint: × 10 then halve." % _c(n), n * 5, "int", {},
                   ["%s × 10 = %s; half of that is %s." % (_c(n), _c(n * 10), _c(n * 5))])

    def t_three():
        x, y, z = random.randint(2, 9), pick(_by(d, [5, 10], [5, 25, 20], [25, 50, 20])), random.randint(2, _by(d, 4, 8, 8))
        return _tb("Work out %d × %d × %d. Choose an easy order." % (x, y, z), x * y * z, "int", {},
                   ["Multiply in any order: %d." % (x * y * z)])

    def t_fact_family():
        p = a * b
        f = _by(d, 10, 30, pick([40, 60, 70, 80]))
        g = 10 if d == 2 else 1                           # stretch: both numbers scaled
        return _tb("%d × %d = %d. Use this to work out %d × %d." % (a, b, p, a * f, b * g), a * f * b * g,
                   "int", {}, ["%d × %d is %s times %d × %d." % (a * f, b * g, _c(f * g), a, b),
                               "%d × %s = %s." % (p, _c(f * g), _c(p * f * g))])

    def t_by25():
        n = random.randint(*_by(d, (1, 10), (3, 40), (30, 250))) * 4
        return _tb("Work out %d × 25. Hint: × 100 then divide by 4." % n, n * 25, "int", {},
                   ["%d × 100 = %s; ÷ 4 = %s." % (n, _c(n * 100), _c(n * 25))])

    def t_missing():
        k = pick(_by(d, [1, 10], [10, 100], [100, 1000]))
        return _tb("___ × %d = %s. What is the missing number?" % (b * 10, _c(a * b * 10 * k)), a * k, "int", {},
                   ["%d × %d = %d, so the missing number is %s." % (a, b, a * b, _c(a * k))])

    def t_compare():
        x1, y1 = random.randint(2, 9) * _by(d, 1, 10, 100), random.randint(2, 9) * 10
        x2, y2 = random.randint(2, 9) * 10, random.randint(2, 9) * _by(d, 10, 100, 100)
        if x1 * y1 == x2 * y2:
            y2 += _by(d, 10, 100, 100)
        return _tb("Which is larger, %s × %d or %d × %s? Type its value." % (_c(x1), y1, x2, _c(y2)), max(x1 * y1, x2 * y2),
                   "int", {}, ["%s × %d = %s; %d × %s = %s." % (_c(x1), y1, _c(x1 * y1), x2, _c(y2), _c(x2 * y2))])

    def t_grid():
        xs = random.sample(_by(d, [20, 30, 40, 50], [20, 30, 40, 50, 60, 70, 80, 90], [60, 70, 80, 90, 300, 400, 600, 700]), 2)
        ys = random.sample(_by(d, [2, 3, 4, 5], [3, 4, 6, 7, 8, 9], [6, 7, 8, 9]), 2)
        rows = [[_c(x), _c(x * ys[0]), _c(x * ys[1])] for x in xs]
        r, c = random.randrange(2), random.randint(1, 2)
        return _dt("Complete the multiplication grid. What belongs in the empty cell?",
                   ["×", str(ys[0]), str(ys[1])], rows, xs[r] * ys[c - 1],
                   ["%d × %d = %s." % (xs[r], ys[c - 1], _c(xs[r] * ys[c - 1]))], missing=[r, c])

    def t_double_double():
        n = random.randint(*_by(d, (6, 25), (12, 60), (45, 250)))
        return _tb("Work out %d × 8 by doubling three times." % n, n * 8, "int", {},
                   ["%d → %s → %s → %s." % (n, _c(2 * n), _c(4 * n), _c(8 * n))])

    return _pick_t([t_tens, t_double, t_partition, t_near, t_by5, t_three, t_fact_family, t_by25, t_missing,
                    t_compare, t_double_double], [t_grid])


@skill("Y5.4.b", "Multiply up to 4 digits by a 1-digit number", S4)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 100, 1000, 1000), _by(d, 999, 4999, 9999))
    m = random.randint(_by(d, 2, 3, 6), _by(d, 5, 9, 9))

    def t_plain():
        return _tb("Work out %s × %d using short multiplication." % (_c(n), m), n * m, "int", {},
                   ["Multiply each digit by %d from the ones, carrying as you go." % m,
                    "%s × %d = %s." % (_c(n), m, _c(n * m))])

    def t_word():
        what = pick([("boxes", "pencils"), ("crates", "bottles"), ("coaches", "seats")])
        return _tb("There are %d %s with %s %s in each. How many %s altogether?"
                   % (m, what[0], _c(n), what[1], what[1]), n * m, "int", {},
                   ["%s × %d = %s." % (_c(n), m, _c(n * m))])

    def t_money():
        p = random.randint(105, 999)
        return _tb("One ticket costs %dp. How much do %d tickets cost, in pence?" % (p, m), p * m, "int",
                   {"unit": "p"}, ["%d × %d = %d." % (p, m, p * m)])

    def t_partial():
        th, rest = (n // 1000) * 1000, n % 1000
        if not th:
            return t_plain()
        return _tb("%s × %d = (%s × %d) + (%s × %d) = ___" % (_c(n), m, _c(th), m, _c(rest), m),
                   n * m, "int", {}, ["%s + %s = %s." % (_c(th * m), _c(rest * m), _c(n * m))])

    def t_missing_digit():
        p = n * m
        s = list(str(n))
        k = random.randrange(len(s))
        h = s[k]
        s[k] = "□"
        return _tb("In  %s × %d = %s  one digit is hidden. What is □?" % ("".join(s), m, _c(p)),
                   int(h), "int", {}, ["%s ÷ %d = %s." % (_c(p), m, _c(n))])

    def t_table():
        nums = random.sample(range(_by(d, 100, 1000, 1000), _by(d, 999, 4999, 9999) + 1), 4)
        rows = [[x, x * m] for x in nums]
        k = random.randrange(4)
        return _io("Every Out number is the In number × %d. What goes in the empty cell?" % m, rows, k,
                   rows[k][1], ["%s × %d = %s." % (_c(rows[k][0]), m, _c(rows[k][1]))],
                   rule="× %d" % m)

    return _pick_t([t_plain, t_word, t_money, t_partial, t_missing_digit], [t_table])


@skill("Y5.4.c", "Long multiplication by a 2-digit number", S4)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 12, 120, 1000), _by(d, 99, 999, 4999))
    m = random.choice([v for v in range(_by(d, 11, 12, 21), _by(d, 19, 39, 99) + 1) if v % 10])

    def t_plain():
        t, o = (m // 10) * 10, m % 10
        return _tb("Work out %s × %d using long multiplication." % (_c(n), m), n * m, "int", {},
                   ["%s × %d = %s." % (_c(n), o, _c(n * o)),
                    "%s × %d = %s." % (_c(n), t, _c(n * t)),
                    "%s + %s = %s." % (_c(n * o), _c(n * t), _c(n * m))])

    def t_partials():
        t, o = (m // 10) * 10, m % 10
        return _tb("In the long multiplication %s × %d, the two rows are %s and %s. What is the "
                   "final answer?" % (_c(n), m, _c(n * o), _c(n * t)), n * m, "int", {},
                   ["Add the rows: %s + %s = %s." % (_c(n * o), _c(n * t), _c(n * m))])

    def t_which_row():
        t = (m // 10) * 10
        return _tb("In the long multiplication %s × %d, what is the row for %s × %d?"
                   % (_c(n), m, _c(n), t), n * t, "int", {},
                   ["%s × %d = %s." % (_c(n), t, _c(n * t))])

    def t_word():
        return _tb("A school buys %d boxes of paper. Each box holds %s sheets. How many sheets is "
                   "that?" % (m, _c(n)), n * m, "int", {"unit": "sheets"},
                   ["%s × %d = %s." % (_c(n), m, _c(n * m))])

    def t_area():
        a, b = random.randint(12, 45), random.randint(11, 35)
        return _tb("A rectangular field is %d m long and %d m wide. What is its area, in m²?" % (a, b),
                   a * b, "int", {"unit": "m²"}, ["%d × %d = %d." % (a, b, a * b)])

    def t_check():
        p = n * m
        claimed = pick([p, p + pick([10, 100, -10, n])])
        return _wq("%s says %s × %d = %s. Is that correct? (yes or no)" % (_who(), _c(n), m, _c(claimed)),
                   "yes" if claimed == p else "no", ["%s × %d = %s." % (_c(n), m, _c(p))], "yes / no")

    def t_table():
        nums = random.sample(range(100, 999), 3)
        rows = [[x, x * m] for x in nums]
        k = random.randrange(3)
        return _io("Every Out number is the In number × %d. What goes in the empty cell?" % m, rows, k,
                   rows[k][1], ["%s × %d = %s." % (_c(rows[k][0]), m, _c(rows[k][1]))],
                   rule="× %d" % m)

    return _pick_t([t_plain, t_partials, t_which_row, t_word, t_area, t_check], [t_table])


@skill("Y5.4.d", "Divide mentally using known facts", S4)
def _(d=1):
    d = _d(d)
    # easy: small tables; stretch: the 6-9 divisors and 6-12 quotients
    a = random.randint(*_by(d, (2, 6), (2, 12), (6, 12)))
    b = random.randint(*_by(d, (2, 5), (2, 9), (6, 9)))

    def t_tens():
        k = pick([10, 100, 1000][: _by(d, 2, 3, 3)])
        return _tb("Work out %s ÷ %d." % (_c(a * b * k), b), a * k, "int", {},
                   ["%d ÷ %d = %d, so %s ÷ %d = %s." % (a * b, b, a, _c(a * b * k), b, _c(a * k))])

    def t_by_tens():
        k = pick(_by(d, [10], [10, 100], [100, 1000]))
        return _tb("Work out %s ÷ %s." % (_c(a * b * k * 10), _c(b * k)), a * 10, "int", {},
                   ["Divide both by %s: %s ÷ %d = %d." % (_c(k), _c(a * b * 10), b, a * 10)])

    def t_halve():
        n = random.randint(*_by(d, (5, 25), (11, 99), (100, 250))) * 4
        return _tb("Work out %d ÷ 4 by halving twice." % n, n // 4, "int", {},
                   ["Half of %d is %d; half again is %d." % (n, n // 2, n // 4)])

    def t_partition():
        m = random.randint(*_by(d, (2, 4), (3, 8), (6, 9)))
        q = random.choice([v for v in range(*_by(d, (12, 26), (12, 40), (41, 100))) if v % 10])
        n = q * m
        t = (q // 10) * 10 * m
        return _tb("Work out %d ÷ %d by splitting %d into %d and %d." % (n, m, n, t, n - t), q, "int", {},
                   ["%d ÷ %d = %d and %d ÷ %d = %d." % (t, m, t // m, n - t, m, (n - t) // m),
                    "%d + %d = %d." % (t // m, (n - t) // m, q)])

    def t_inverse():
        k = _by(d, 10, 100, 1000)
        return _tb("___ × %d = %s. What is the missing number?" % (b, _c(a * b * k)), a * k, "int",
                   {}, ["%s ÷ %d = %s." % (_c(a * b * k), b, _c(a * k))])

    def t_by5():
        n = random.randint(*_by(d, (2, 20), (11, 99), (101, 999))) * 10
        return _tb("Work out %s ÷ 5. Hint: ÷ 10 then double." % _c(n), n // 5, "int", {},
                   ["%s ÷ 10 = %d; double is %s." % (_c(n), n // 10, _c(n // 5))])

    def t_share():
        k = pick(_by(d, [10, 100], [100, 1000], [1000]))
        return _tb("%s pounds are shared equally between %d charities. How much does each get, in pounds?"
                   % (_c(a * b * k), b), a * k, "int", {"unit": "£"},
                   ["%d ÷ %d = %d, so %s ÷ %d = %s." % (a * b, b, a, _c(a * b * k), b, _c(a * k))])

    def t_divisor():
        k = pick(_by(d, [10], [10, 100], [100, 1000]))
        return _tb("%s ÷ ___ = %s. What is the missing number?" % (_c(a * b * k), _c(a * k)), b, "int", {},
                   ["%s ÷ %s = %d." % (_c(a * b * k), _c(a * k), b)])

    def t_by25():
        n = random.randint(*_by(d, (1, 10), (2, 30), (31, 99))) * 100
        return _tb("Work out %s ÷ 25. Hint: ÷ 100 then × 4." % _c(n), n // 25, "int", {},
                   ["%s ÷ 100 = %d; × 4 = %d." % (_c(n), n // 100, n // 25)])

    def t_compare():
        x = a * b * 100
        y = random.randint(2, 9) * random.randint(2, 9) * 100
        ks = [k for k in range(2, 10) if y % k == 0 and (y // k) != x // b]
        if not ks:
            return t_tens()
        m2 = pick(ks)
        return _tb("Which is larger, %s ÷ %d or %s ÷ %d? Type its value." % (_c(x), b, _c(y), m2),
                   max(x // b, y // m2), "int", {},
                   ["%s ÷ %d = %s; %s ÷ %d = %s." % (_c(x), b, _c(x // b), _c(y), m2, _c(y // m2))])

    def t_table():
        k = pick(_by(d, [10], [10, 100], [100, 1000]))
        xs = random.sample(range(2, 13), 3)
        rows = [[_c(x * b * k), _c(x * k)] for x in xs]
        r = random.randrange(3)
        return _io("Every Out number is the In number ÷ %d. What goes in the empty cell?" % b,
                   [[x * b * k, x * k] for x in xs], r, xs[r] * k,
                   ["%s ÷ %d = %s." % (rows[r][0], b, rows[r][1])], rule="÷ %d" % b)

    def t_halve_three():
        n = random.randint(*_by(d, (2, 12), (3, 40), (41, 125))) * 8
        return _tb("Work out %d ÷ 8 by halving three times." % n, n // 8, "int", {},
                   ["%d → %d → %d → %d." % (n, n // 2, n // 4, n // 8)])

    return _pick_t([t_tens, t_by_tens, t_halve, t_partition, t_inverse, t_by5, t_share, t_divisor, t_by25, t_compare,
                    t_halve_three], [t_table])


@skill("Y5.4.e", "Short division of up to 4 digits by a 1-digit number", S4)
def _(d=1):
    d = _d(d)
    m = random.randint(_by(d, 2, 3, 6), _by(d, 5, 9, 9))
    q = random.randint(_by(d, 21, 101, 201), min(_by(d, 199, 999, 1666), (10000 - m) // m))
    r = 0 if d == 0 or random.random() < 0.5 else random.randint(1, m - 1)
    n = q * m + r

    def t_plain():
        if r:
            return _wq("Work out %s ÷ %d. Write the answer like 25 r 3." % (_c(n), m), "%d r %d" % (q, r),
                       ["%s ÷ %d = %d remainder %d." % (_c(n), m, q, r)], "e.g. 25 r 3")
        return _tb("Work out %s ÷ %d using short division." % (_c(n), m), q, "int", {},
                   ["Divide each digit from the left, carrying remainders.", "= %s." % _c(q)])

    def t_quotient_only():
        return _tb("Work out %s ÷ %d. Write the whole-number part of the answer." % (_c(n), m), q, "int",
                   {}, ["%s ÷ %d = %d remainder %d." % (_c(n), m, q, r)])

    def t_remainder():
        rr = random.randint(1, m - 1)
        nn = q * m + rr
        return _tb("What is the remainder when %s is divided by %d?" % (_c(nn), m), rr, "int", {},
                   ["%d × %d = %s; %s − %s = %d." % (q, m, _c(q * m), _c(nn), _c(q * m), rr)])

    def t_share():
        return _tb("%s stickers are shared equally between %d children. How many does each child "
                   "get?" % (_c(q * m), m), q, "int", {}, ["%s ÷ %d = %s." % (_c(q * m), m, _c(q))])

    def t_check():
        shown = q if random.random() < 0.5 else q + pick([-1, 1]) * pick([1, 10])
        return _wq("%s says %s ÷ %d = %s. Check by multiplying %s × %d. Is it correct? (yes or no)"
                   % (_who(), _c(q * m), m, _c(shown), _c(shown), m), "yes" if shown == q else "no",
                   ["%s × %d = %s." % (_c(shown), m, _c(shown * m)),
                    "That %s %s." % ("matches" if shown == q else "does not match", _c(q * m))], "yes / no")

    def t_bar():
        return _strip("The bar shows %s split into %d equal parts. How big is one part?" % (_c(q * m), m),
                      {"mode": "equal_parts", "parts": m, "partLabel": "?", "totalLabel": _c(q * m),
                       "unknown": "part"}, q, ["%s ÷ %d = %s." % (_c(q * m), m, _c(q))])

    return _pick_t([t_plain, t_quotient_only, t_remainder, t_share, t_check], [t_bar])


@skill("Y5.4.f", "Interpret remainders in context", S4)
def _(d=1):
    d = _d(d)
    m = random.randint(_by(d, 3, 4, 6), _by(d, 6, 9, 12))
    q = random.randint(5, _by(d, 30, 80, 150))
    r = random.randint(1, m - 1)
    n = q * m + r

    def t_round_up():
        return _tb("%d children are going on a trip. Each minibus holds %d children. How many "
                   "minibuses are needed?" % (n, m), q + 1, "int", {"unit": "minibuses"},
                   ["%d ÷ %d = %d remainder %d." % (n, m, q, r),
                    "The %d left over still need a minibus, so %d." % (r, q + 1)])

    def t_round_down():
        return _tb("Eggs are packed in boxes of %d. There are %d eggs. How many boxes can be filled "
                   "completely?" % (m, n), q, "int", {"unit": "boxes"},
                   ["%d ÷ %d = %d remainder %d." % (n, m, q, r), "Only %d boxes are full." % q])

    def t_left():
        return _tb("%d sweets are shared equally between %d friends. How many sweets are left over?"
                   % (n, m), r, "int", {"unit": "sweets"}, ["%d ÷ %d = %d remainder %d." % (n, m, q, r)])

    def t_money():
        price = pick([2, 3, 4, 5, 6])
        money = random.randint(20, 99)
        who = _who()
        return _tb("Notebooks cost £%d each. %s has £%d. How many notebooks can %s buy?"
                   % (price, who, money, who), money // price, "int", {"unit": "notebooks"},
                   ["%d ÷ %d = %d remainder %d." % (money, price, money // price, money % price)])

    def t_shelves():
        return _tb("%d books are put on shelves that hold %d books each. How many shelves are needed "
                   "for all the books?" % (n, m), q + 1, "int", {"unit": "shelves"},
                   ["%d ÷ %d = %d remainder %d, so one more shelf: %d." % (n, m, q, r, q + 1)])

    def t_which():
        kind = pick(["up", "down"])
        ctx = ("How many cars are needed to take %d people if each car takes %d?" % (n, m)) \
            if kind == "up" else ("How many full teams of %d can be made from %d players?" % (m, n))
        return _tb(ctx, q + 1 if kind == "up" else q, "int", {},
                   ["%d ÷ %d = %d remainder %d." % (n, m, q, r),
                    "Round %s here." % kind])

    def t_tents():
        return _tb("Each tent sleeps %d scouts. %d scouts go camping. How many tents are needed so that every scout has "
                   "a place?" % (m, n), q + 1, "int", {"unit": "tents"},
                   ["%d ÷ %d = %d remainder %d." % (n, m, q, r), "The last %d scout%s still need%s a tent: %d." % (
                       r, "" if r == 1 else "s", "s" if r == 1 else "", q + 1)])

    def t_ribbon():
        return _tb("A ribbon is %d cm long. It is cut into pieces %d cm long. How many cm of ribbon are left over?"
                   % (n, m), r, "int", {"unit": "cm"}, ["%d ÷ %d = %d remainder %d." % (n, m, q, r)])

    def t_share_fraction():
        k = pick([2, 3, 4, 5])
        pz = k * random.randint(1, 4) + random.randint(1, k - 1)
        return _tb("%d pizzas are shared equally between %d people. How much pizza does each person get? Write it as a "
                   "mixed number (like 2 1/4)." % (pz, k), _mixed(Fraction(pz, k)), "frac",
                   {"text": True, "placeholder": "e.g. 2 1/4"},
                   ["%d ÷ %d = %d remainder %d." % (pz, k, pz // k, pz % k),
                    "The %d left over %s shared too: %d/%d each." % (pz % k, "is" if pz % k == 1 else "are", pz % k, k),
                    "So each person gets %s." % _mixed(Fraction(pz, k))])

    def t_weeks():
        days = random.randint(3, 12) * 7 + random.randint(1, 6)
        return _tb("A holiday is %d days long. How many COMPLETE weeks is that?" % days, days // 7, "int",
                   {"unit": "weeks"}, ["%d ÷ 7 = %d remainder %d." % (days, days // 7, days % 7)])

    def t_more_needed():
        return _tb("Cakes are packed in boxes of %d. There are %d cakes. How many more cakes are needed to fill the last "
                   "box?" % (m, n), m - r, "int", {"unit": "cakes"},
                   ["%d ÷ %d = %d remainder %d." % (n, m, q, r), "%d − %d = %d more." % (m, r, m - r)])

    return _pick_t([t_round_up, t_round_down, t_left, t_money, t_shelves, t_which, t_tents, t_ribbon,
                    t_share_fraction, t_weeks, t_more_needed])


@skill("Y5.4.g", "Multiply and divide whole numbers by 10, 100 and 1000", S4)
def _(d=1):
    d = _d(d)
    k = pick(_by(d, [10, 100], [10, 100, 1000], [100, 1000]))
    n = random.randint(_by(d, 2, 10, 100), _by(d, 99, 999, 9999))

    def t_mult():
        return _tb("Work out %s × %s." % (_c(n), _c(k)), n * k, "int", {},
                   ["Each digit moves %d place%s to the left." % (len(str(k)) - 1,
                                                                 "" if k == 10 else "s")])

    def t_div():
        return _tb("Work out %s ÷ %s." % (_c(n * k), _c(k)), n, "int", {},
                   ["Each digit moves %d place%s to the right." % (len(str(k)) - 1,
                                                                  "" if k == 10 else "s")])

    def t_missing():
        return _tb("%s × ___ = %s. Is the missing number 10, 100 or 1000?" % (_c(n), _c(n * k)), k,
                   "int", {}, ["%s has moved %d place%s." % (_c(n), len(str(k)) - 1,
                                                             "" if k == 10 else "s")])

    def t_units():
        unit, big, f = pick([("cm", "m", 100), ("mm", "cm", 10), ("m", "km", 1000), ("g", "kg", 1000)])
        x = random.randint(2, _by(d, 20, 90, 999))
        if d == 2 and pick([0, 1]):                       # the other way: divide back to the big unit
            return _tb("How many %s are %s %s?" % (big, _c(x * f), unit), x, "int", {"unit": big},
                       ["1 %s = %d %s, so ÷ %d." % (big, f, unit, f)])
        return _tb("How many %s are in %d %s?" % (unit, x, big), x * f, "int", {"unit": unit},
                   ["1 %s = %d %s, so × %d." % (big, f, unit, f)])

    def t_table():
        nums = random.sample(range(_by(d, 2, 2, 50), _by(d, 50, 500, 5000)), 3)
        rows = [[x, x * k] for x in nums]
        i = random.randrange(3)
        return _io("Every Out number is the In number × %s. What goes in the empty cell?" % _c(k), rows,
                   i, rows[i][1], ["%s × %s = %s." % (_c(rows[i][0]), _c(k), _c(rows[i][1]))],
                   rule="× %s" % _c(k))

    return _pick_t([t_mult, t_div, t_missing, t_units], [t_table])


@skill("Y5.4.h", "Multiply and divide decimals by 10, 100 and 1000", S4)
def _(d=1):
    d = _d(d)
    k = pick(_by(d, [10, 100], [10, 100, 1000], [100, 1000]))
    dp = _by(d, 1, 2, 3)
    n = Decimal(random.randint(1, 9999)) / (10 ** dp)

    def t_mult():
        return _tb("Work out %s × %s." % (_ds(n), _c(k)), _ds(n * k), "num", {},
                   ["Digits move %d place%s to the left: %s." % (len(str(k)) - 1, "" if k == 10 else "s",
                                                                 _ds(n * k))])

    def t_div():
        m = Decimal(random.randint(1, _by(d, 99, 999, 9999)))
        return _tb("Work out %s ÷ %s." % (_ds(m), _c(k)), _ds(m / k), "num", {},
                   ["Digits move %d place%s to the right: %s." % (len(str(k)) - 1, "" if k == 10 else "s",
                                                                  _ds(m / k))])

    def t_missing():
        return _tb("%s × ___ = %s. Is the missing number 10, 100 or 1000?" % (_ds(n), _ds(n * k)), k,
                   "int", {}, ["The digits moved %d place%s." % (len(str(k)) - 1, "" if k == 10 else "s")])

    def t_money():
        p = Decimal(random.randint(*_by(d, (10, 99), (101, 999), (101, 9999)))) / _by(d, 10, 100, 100)
        q = pick(_by(d, [10], [10, 100], [100, 1000]))
        return _tb("One pen costs £%s. How much do %d pens cost, in pounds?" % (format(p, ".2f"), q),
                   _ds(p * q), "num", {"unit": "£"}, ["£%s × %d = £%s." % (format(p, ".2f"), q, format(p * q, ",.2f"))])

    def t_measure():
        x = Decimal(random.randint(11, _by(d, 99, 999, 9999))) / 10
        unit, big, f = pick([("m", "km", 1000), ("cm", "m", 100), ("kg", "g", 1000)])
        if unit == "kg":
            return _tb("Convert %s kg to grams." % _ds(x), _ds(x * 1000), "num", {"unit": "g"},
                       ["× 1000: %s g." % _ds(x * 1000)])
        if unit == "m":                                   # whole metres, so km stays within 3 d.p.
            x = Decimal(random.randint(11, _by(d, 999, 9999, 99999)))
        return _tb("Convert %s %s to %s." % (_ds(x), unit, big), _ds(x / f), "num", {"unit": big},
                   ["÷ %d: %s %s." % (f, _ds(x / f), big)])

    def t_table():
        nums = [Decimal(random.randint(1, _by(d, 99, 999, 9999))) / _by(d, 10, 10, 100) for _ in range(3)]
        rows = [[_ds(x), _ds(x * 10), _ds(x * 100), _ds(x * 1000)] for x in nums]
        r, c = random.randrange(3), random.randint(1, 3)
        ans = nums[r] * [10, 100, 1000][c - 1]
        return _dt("Complete the table. What belongs in the empty cell?", ["Number", "× 10", "× 100",
                                                                           "× 1000"],
                   rows, _ds(ans), ["%s × %s = %s." % (_ds(nums[r]), _c([10, 100, 1000][c - 1]), _ds(ans))],
                   missing=[r, c], atype="num")

    def t_missing_div():
        m = Decimal(random.randint(1, _by(d, 99, 999, 9999)))
        return _tb("%s ÷ ___ = %s. Is the missing number 10, 100 or 1000?" % (_ds(m), _ds(m / k)), k, "int", {},
                   ["The digits moved %d place%s to the right." % (len(str(k)) - 1, "" if k == 10 else "s")])

    def t_money_share():
        p = Decimal(random.randint(101, _by(d, 999, 9999, 9999))) / 100
        q = pick(_by(d, [10], [10, 100], [100, 1000]))
        tot = p * q
        return _tb("£%s is shared equally between %d people. How much does each get, in pounds?" % (format(tot, ",.2f"), q),
                   _ds(p), "num", {"unit": "£"}, ["£%s ÷ %d = £%s." % (format(tot, ",.2f"), q, format(p, ".2f"))])

    def t_compare():
        x, y = Decimal(random.randint(11, 99)) / _by(d, 10, 100, 1000), Decimal(random.randint(11, 99)) / _by(d, 1, 10, 100)
        kx, ky = pick(_by(d, [(10, 10), (100, 10)], [(100, 10), (1000, 100), (10, 10)], [(1000, 100), (1000, 10), (100, 100)]))
        if x * kx == y * ky:
            y += Decimal("0.1")
        return _tb("Which is larger, %s × %s or %s × %s? Type its value." % (_ds(x), _c(kx), _ds(y), _c(ky)),
                   _ds(max(x * kx, y * ky)), "num", {},
                   ["%s × %s = %s; %s × %s = %s." % (_ds(x), _c(kx), _ds(x * kx), _ds(y), _c(ky), _ds(y * ky))])

    def t_place():
        if d == 2:                                        # divide back down onto the line
            x = random.randint(11, 99) * 10
            return _nld("Work out %d ÷ 100 and mark the answer on the number line." % x, Decimal(x) / 100, 0, 10,
                        Decimal("0.1"), 1, ["%d ÷ 100 = %s." % (x, _ds(Decimal(x) / 100))])
        x = Decimal(random.randint(1, _by(d, 9, 99, 99))) / _by(d, 10, 100, 100)
        return _nld("Work out %s × 10 and mark the answer on the number line." % _ds(x), x * 10, 0, 10, Decimal("0.1"), 1,
                    ["%s × 10 = %s." % (_ds(x), _ds(x * 10))])

    def t_chain():
        x = Decimal(random.randint(1, _by(d, 99, 999, 9999))) / _by(d, 1, 10, 100)
        up, dn = _by(d, (100, 10), (100, 10), (1000, 100))
        return _tb("Start with %s. Multiply by %s, then divide by %d. What do you get?" % (_ds(x), _c(up), dn), _ds(x * 10),
                   "num", {}, ["%s × %s = %s." % (_ds(x), _c(up), _ds(x * up)), "%s ÷ %d = %s." % (_ds(x * up), dn, _ds(x * 10))])

    return _pick_t([t_mult, t_div, t_missing, t_money, t_measure, t_missing_div, t_money_share, t_compare, t_chain],
                   [t_table, t_place])


@skill("Y5.4.i", "Scaling problems, including by simple fractions", S4)
def _(d=1):
    d = _d(d)

    def t_times():
        a = random.randint(*_by(d, (12, 50), (12, 250), (120, 999)))
        k = random.randint(*_by(d, (2, 5), (2, 9), (6, 9)))
        return _tb("A tree is %d cm tall. A building is %d times as tall. How tall is the building, in "
                   "cm?" % (a, k), a * k, "int", {"unit": "cm"}, ["%d × %d = %d." % (a, k, a * k)])

    def t_recipe():
        if d == 2:                                  # stretch: scale by a fraction (4 -> 6 is × 3/2)
            n = pick([6, 10, 14, 18])
            per = 2 * random.randint(25, 125)
            return _tb("A recipe for 4 people uses %d g of flour. How much flour is needed for %d people, "
                       "in grams?" % (per, n), per * n // 4, "int", {"unit": "g"},
                       ["2 people need %d ÷ 2 = %d g." % (per, per // 2),
                        "%d people is %d lots of 2 people: %d × %d = %d."
                        % (n, n // 2, per // 2, n // 2, per * n // 4)])
        per = random.randint(5, 10) * 10 if d == 0 else random.randint(50, 250)
        k = random.randint(2, 3) if d == 0 else random.randint(2, 6)
        return _tb("A recipe for 4 people uses %d g of flour. How much flour is needed for %d people, "
                   "in grams?" % (per, 4 * k), per * k, "int", {"unit": "g"},
                   ["%d people is %d times as many." % (4 * k, k), "%d × %d = %d." % (per, k, per * k)])

    def t_fraction_scale():
        den = pick(_by(d, [2, 4], [2, 3, 4, 5], [5, 8, 10]))
        x = den * random.randint(*_by(d, (2, 10), (4, 30), (10, 60)))
        return _tb("A model car is 1/%d of the length of a toy bus that is %d cm long. How long is the "
                   "car, in cm?" % (den, x), x // den, "int", {"unit": "cm"},
                   ["1/%d of %d = %d ÷ %d = %d." % (den, x, x, den, x // den)])

    def t_nonunit():
        den = pick(_by(d, [3, 4], [3, 4, 5, 8], [5, 8, 10, 12]))
        num = random.randint(2, den - 1)
        x = den * random.randint(*_by(d, (2, 10), (5, 25), (10, 40)))
        return _tb("A ribbon is %d cm long. %s uses %d/%d of it. How many cm is that?"
                   % (x, _who(), num, den), x // den * num, "int", {"unit": "cm"},
                   ["1/%d of %d = %d." % (den, x, x // den), "× %d = %d." % (num, x // den * num)])

    def t_correspond():
        a = random.randint(*_by(d, (2, 4), (3, 6), (6, 12)))
        b = random.randint(*_by(d, (2, 3), (2, 5), (4, 9)))
        return _tb("A café offers %d kinds of sandwich and %d kinds of drink. A meal deal is one "
                   "sandwich and one drink. How many different meal deals are there?" % (a, b), a * b,
                   "int", {}, ["Each sandwich goes with %d drinks: %d × %d = %d." % (b, a, b, a * b)])

    def t_inverse():
        a = random.randint(*_by(d, (2, 10), (12, 90), (12, 90)))
        k = random.randint(*_by(d, (2, 4), (3, 8), (6, 9)))
        return _tb("A giraffe is %d times as heavy as a pony. The giraffe weighs %d kg. How heavy is "
                   "the pony, in kg?" % (k, a * k * 10), a * 10, "int", {"unit": "kg"},
                   ["%d ÷ %d = %d." % (a * k * 10, k, a * 10)])

    def t_bar():
        a = random.randint(*_by(d, (2, 12), (5, 60), (25, 150)))
        k = random.randint(*_by(d, (2, 4), (2, 6), (4, 6)))
        return _strip("%s has %d stickers. %s has %d times as many. How many stickers does %s have?"
                      % ("Leo", a, "Maya", k, "Maya"),
                      {"mode": "equal_parts", "parts": k, "partLabel": str(a), "totalLabel": "?",
                       "unknown": "total"}, a * k, ["%d × %d = %d." % (a, k, a * k)])

    def t_half_as():
        den = pick(_by(d, [2, 4], [2, 3, 4, 5], [5, 8, 10]))
        x = den * random.randint(*_by(d, (5, 20), (10, 60), (12, 80)))
        return _tb("A hamster's cage is %d cm long. A mouse's cage is 1/%d as long. How long is the mouse's cage, in cm?"
                   % (x, den), x // den, "int", {"unit": "cm"}, ["%d ÷ %d = %d." % (x, den, x // den)])

    def t_map():
        k = pick(_by(d, [2, 5, 10], [2, 5, 10, 25], [20, 25, 50]))
        cm = random.randint(*_by(d, (2, 10), (2, 15), (11, 25)))
        return _tb("On a map, 1 cm stands for %d km. Two towns are %d cm apart on the map. How far apart are they really, "
                   "in km?" % (k, cm), k * cm, "int", {"unit": "km"}, ["%d × %d = %d." % (cm, k, k * cm)])

    def t_how_many_times():
        a = random.randint(*_by(d, (2, 12), (12, 60), (12, 99)))
        k = random.randint(*_by(d, (2, 5), (3, 9), (6, 12)))
        return _tb("A rope is %d m long and a string is %d m long. How many times as long as the string is the rope?"
                   % (a * k, a), k, "int", {}, ["%d ÷ %d = %d." % (a * k, a, k)])

    def t_recipe_down():
        k = pick(_by(d, [2], [2, 3, 4], [3, 4, 5, 6]))
        per = k * random.randint(*_by(d, (10, 50), (20, 120), (20, 120)))
        return _tb("A recipe for %d people uses %d g of rice. How much rice is needed for 1 person, in grams?"
                   % (k * 2, per * 2), per * 2 // (k * 2), "int", {"unit": "g"},
                   ["%d ÷ %d = %d." % (per * 2, k * 2, per * 2 // (k * 2))])

    def t_table():
        if d == 2:                                  # stretch: people counts that are not multiples of 4
            per = random.randint(1, 4) * 50
            rows = [[p, per * p // 4] for p in (4, 6, 10, 14)]
            i = random.randint(1, 3)
            return _io("A recipe for 4 people uses %d g of oats. The table scales it for more people. What goes "
                       "in the empty cell?" % per, rows, i, rows[i][1],
                       ["2 people need %d ÷ 2 = %d g." % (per, per // 2),
                        "%d people is %d lots of 2: %d × %d = %d."
                        % (rows[i][0], rows[i][0] // 2, per // 2, rows[i][0] // 2, rows[i][1])], rule="grams")
        per = random.randint(2, 9 if d == 1 else 4) * 25
        rows = [[p, per * p // 4] for p in (4, 8, 12, 16)]
        i = random.randint(1, 3)
        return _io("A recipe for 4 people uses %d g of oats. The table scales it for more people. What goes in the empty "
                   "cell?" % per, rows, i, rows[i][1], ["%d people is %d times 4 people: %d × %d = %d." % (
                       rows[i][0], rows[i][0] // 4, per, rows[i][0] // 4, rows[i][1])], rule="grams")

    def t_outfits():
        if d == 0:                                  # easy: two choices to combine
            a, b = random.randint(2, 4), random.randint(2, 4)
            return _tb("%s has %d hats and %d scarves. An outfit is one hat and one scarf. How many different "
                       "outfits are possible?" % (_who(), a, b), a * b, "int", {},
                       ["%d × %d = %d." % (a, b, a * b)])
        a, b, c = [random.randint(*_by(d, 0, (2, 4), (3, 6))) for _ in range(2)] + \
            [random.randint(*_by(d, 0, (2, 3), (2, 5)))]
        return _tb("%s has %d hats, %d scarves and %d pairs of gloves. An outfit is one hat, one scarf and one pair of "
                   "gloves. How many different outfits are possible?" % (_who(), a, b, c), a * b * c, "int", {},
                   ["%d × %d × %d = %d." % (a, b, c, a * b * c)])

    return _pick_t([t_times, t_recipe, t_fraction_scale, t_nonunit, t_correspond, t_inverse, t_half_as, t_map,
                    t_how_many_times, t_recipe_down, t_outfits], [t_bar, t_table])


@skill("Y5.4.j", "Simple rates", S4)
def _(d=1):
    d = _d(d)

    def t_per_item():
        if d == 0:
            n, p = random.randint(2, 5), random.randint(2, 10) * 5
        else:
            n, p = random.randint(3, 12), random.randint(15, 95)
        if d == 2:                                  # stretch: find one, then scale to another count
            m = random.choice([x for x in range(2, 13) if x != n])
            return _tb("%d apples cost %dp altogether. How much do %d apples cost, in pence?" % (n, n * p, m),
                       p * m, "int", {"unit": "p"},
                       ["One apple: %d ÷ %d = %dp." % (n * p, n, p), "%d × %d = %d." % (p, m, p * m)])
        return _tb("%d apples cost %dp altogether. How much does one apple cost, in pence?" % (n, n * p),
                   p, "int", {"unit": "p"}, ["%d ÷ %d = %d." % (n * p, n, p)])

    def t_per_hour():
        rate = random.randint(*_by(d, (5, 10), (5, 15), (9, 15)))
        h = random.randint(*_by(d, (2, 4), (2, 8), (6, 12)))
        return _tb("A babysitter earns £%d an hour. How much is earned in %d hours, in pounds?"
                   % (rate, h), rate * h, "int", {"unit": "£"}, ["%d × %d = %d." % (rate, h, rate * h)])

    def t_speed():
        sp = pick(_by(d, [30, 50, 60], [30, 40, 50, 60, 70], [45, 55, 65, 75, 48, 64]))
        h = random.randint(*_by(d, (2, 3), (2, 5), (3, 6)))
        return _tb("A coach travels at a steady %d km every hour. How far does it go in %d hours, in km?"
                   % (sp, h), sp * h, "int", {"unit": "km"}, ["%d × %d = %d." % (sp, h, sp * h)])

    def t_per_minute():
        r = random.randint(*_by(d, (2, 5), (3, 12), (8, 15)))
        m = random.randint(*_by(d, (2, 10), (4, 15), (12, 25)))
        return _tb("A tap fills a bath at %d litres per minute. How many litres after %d minutes?"
                   % (r, m), r * m, "int", {"unit": "litres"}, ["%d × %d = %d." % (r, m, r * m)])

    def t_time_needed():
        r = random.randint(*_by(d, (2, 5), (3, 12), (8, 15)))
        m = random.randint(*_by(d, (2, 10), (4, 15), (12, 25)))
        return _tb("A printer prints %d pages a minute. How many minutes does it take to print %d "
                   "pages?" % (r, r * m), m, "int", {"unit": "minutes"}, ["%d ÷ %d = %d." % (r * m, r, m)])

    def t_best():
        a_n, b_n = random.randint(2, 5), random.randint(6, 10)
        if d == 1:
            a_p = a_n * random.randint(20, 40)
            b_p = b_n * random.randint(20, 40)
            if a_p / a_n == b_p / b_n:
                b_p += b_n
        else:                                       # easy: far apart per yoghurt; stretch: 1-3p apart
            ea = random.randint(20, 40)
            eb = ea + pick([-1, 1]) * random.randint(*_by(d, (8, 15), 0, (1, 3)))
            a_p, b_p = a_n * ea, b_n * eb
        cheaper = "A" if a_p / a_n < b_p / b_n else "B"
        return _wq("Pack A: %d yoghurts for %dp. Pack B: %d yoghurts for %dp. Which pack is cheaper per "
                   "yoghurt? (A or B)" % (a_n, a_p, b_n, b_p), cheaper,
                   ["A: %dp each. B: %dp each." % (a_p // a_n, b_p // b_n)], "A or B")

    def t_table():
        r = random.randint(*_by(d, (2, 5), (4, 12), (6, 15)))
        rows = [[h, h * r] for h in _by(d, (1, 2, 3, 4, 5), (1, 2, 3, 5, 8), (1, 3, 5, 9, 12))]
        k = random.randint(1, 4)
        return _io("A machine makes %d toys an hour. The table shows hours and toys. What goes in the "
                   "empty cell?" % r, rows, k, rows[k][1], ["%d × %d = %d." % (rows[k][0], r, rows[k][1])])

    def t_graph():
        r = pick(_by(d, [10, 20], [5, 10, 15, 20, 25], [15, 25]))
        hrs = ["0", "1", "2", "3", "4", "5"]
        pts = [(h, r * i) for i, h in enumerate(hrs)]
        q = pick(["per", "at"] + (["time"] if d == 2 else []))
        if q == "time":                             # stretch: read the graph backwards
            k = random.randint(2, 5)
            return _lg("A cyclist rides at a steady speed. The graph shows distance against time. How many "
                       "hours does it take the cyclist to ride %d km?" % (r * k), pts, k,
                       ["Find %d km on the distance axis and read across to the line, then down: %d hours."
                        % (r * k, k)], "km", "Hours")
        if q == "per":
            return _lg("A cyclist rides at a steady speed. The graph shows distance against time. How many km does the "
                       "cyclist ride each hour?", pts, r, ["The line goes up %d km every hour." % r], "km", "Hours")
        k = random.randint(1, 5)
        return _lg("A cyclist rides at a steady speed. The graph shows distance against time. How far has the cyclist "
                   "ridden after %d hour%s, in km?" % (k, "" if k == 1 else "s"), pts, r * k,
                   ["Read up from %d: %d km." % (k, r * k)], "km", "Hours")

    def t_week_wage():
        rate = random.randint(*_by(d, (5, 10), (8, 14), (9, 15)))
        h = random.randint(*_by(d, (2, 4), (3, 8), (5, 8)))
        days = random.randint(*_by(d, (2, 3), (3, 5), (4, 7)))
        return _tb("%s earns £%d an hour and works %d hours a day for %d days. How much is earned altogether, in pounds?"
                   % (_who(), rate, h, days), rate * h * days, "int", {"unit": "£"},
                   ["%d × %d = %d hours." % (h, days, h * days), "%d × %d = %d." % (h * days, rate, rate * h * days)])

    def t_per100():
        if d == 2:                                  # stretch: half-hundreds of grams
            p, g = 2 * random.randint(10, 45), pick([150, 250, 350, 450])
            return _tb("Cheese costs %dp for every 100 g. How much does %d g cost, in pence?" % (p, g),
                       p * g // 100, "int", {"unit": "p"},
                       ["50 g costs %d ÷ 2 = %dp." % (p, p // 2),
                        "%d g is %d lots of 50 g: %d × %d = %d." % (g, g // 50, p // 2, g // 50, p * g // 100)])
        p = random.randint(2, 9) * 10 if d == 0 else random.randint(20, 90)
        g = pick([200, 300] if d == 0 else [200, 300, 400, 500])
        return _tb("Cheese costs %dp for every 100 g. How much does %d g cost, in pence?" % (p, g), p * g // 100, "int",
                   {"unit": "p"}, ["%d g is %d lots of 100 g." % (g, g // 100), "%d × %d = %d." % (p, g // 100, p * g // 100)])

    def t_heart():
        bpm = pick([60, 70, 80]) if d == 0 else random.randint(60, 90 if d == 1 else 99)
        m = random.randint(*_by(d, (2, 5), (3, 10), (10, 30)))
        return _tb("A resting heart beats %d times a minute. How many times does it beat in %d minutes?" % (bpm, m),
                   bpm * m, "int", {"unit": "beats"}, ["%d × %d = %d." % (bpm, m, bpm * m)])

    def t_faster():
        a, b = random.randint(3, 9), random.randint(3, 9)
        if d == 0:                                  # easy: speeds clearly different
            while abs(a - b) < 3:
                b = random.randint(3, 9)
        elif d == 2:                                # stretch: only 10 km an hour apart
            b = a + (1 if a < 9 and (a == 3 or random.random() < 0.5) else -1)
        ta, tb = random.randint(2, 5), random.randint(2, 5)
        da, db = a * ta * 10, b * tb * 10
        if a == b:
            return t_speed()
        return _wq("Car A goes %d km in %d hours. Car B goes %d km in %d hours. Both go at steady speeds. Which car is "
                   "faster? (A or B)" % (da, ta, db, tb), "A" if a > b else "B",
                   ["A: %d km an hour. B: %d km an hour." % (a * 10, b * 10)], "A or B")

    return _pick_t([t_per_item, t_per_hour, t_speed, t_per_minute, t_time_needed, t_best, t_week_wage, t_per100,
                    t_heart, t_faster], [t_table, t_graph])


@skill("Y5.4.k", "Problems using all four operations", S4)
def _(d=1):
    d = _d(d)
    # easy: small, round numbers; stretch: bigger numbers and, in places, one step more

    def t_shop():
        if d == 0:
            a, b = random.randint(1, 3), random.randint(1, 3)
            pa, pb = random.randint(3, 9) * 10, random.randint(3, 9) * 10
        else:
            hi = _by(d, 0, 6, 9)
            a, pa, b, pb = random.randint(2, hi), random.randint(30, 95), random.randint(2, hi), random.randint(30, 95)
        pay = ((a * pa + b * pb) // 100 + 1) * 100 + pick([0, 500])
        return _tb("%s buys %d pens at %dp each and %d rulers at %dp each, and pays with £%d. How much "
                   "change is given, in pence?" % (_who(), a, pa, b, pb, pay // 100),
                   pay - a * pa - b * pb, "int", {"unit": "p"},
                   ["Cost: %d + %d = %d p." % (a * pa, b * pb, a * pa + b * pb),
                    "%d − %d = %d." % (pay, a * pa + b * pb, pay - a * pa - b * pb)])

    def t_share_after():
        total = random.randint(*_by(d, (10, 30), (200, 900), (500, 2000))) * (10 if d == 0 else 1)
        spent = random.randint(*_by(d, (2, 9), (20, 150), (100, 400))) * (10 if d == 0 else 1)
        k = random.randint(*_by(d, (2, 4), (2, 6), (4, 9)))
        rest = total - spent
        rest -= rest % k
        total = rest + spent
        return _tb("A class has £%s. It spends £%d on a trip and shares the rest equally between %d "
                   "charities. How much does each charity get, in pounds?" % (_c(total), spent, k), rest // k,
                   "int", {"unit": "£"}, ["%s − %d = %s." % (_c(total), spent, _c(rest)),
                                          "%s ÷ %d = %d." % (_c(rest), k, rest // k)])

    def t_rows_plus():
        r = random.randint(*_by(d, (3, 8), (6, 15), (12, 25)))
        c = random.randint(*_by(d, (5, 10), (8, 20), (15, 30)))
        extra = random.randint(*_by(d, (2, 9), (5, 30), (10, 60)))
        if d == 2:                                  # stretch: one more step, some are taken away
            gone = random.randint(5, 40)
            ans = r * c + extra - gone
            return _tb("A hall has %d rows of %d chairs and %d extra chairs at the side. %d chairs are taken "
                       "away to make room for a stage. How many chairs are left?" % (r, c, extra, gone), ans,
                       "int", {"unit": "chairs"},
                       ["%d × %d = %d." % (r, c, r * c), "%d + %d = %d." % (r * c, extra, r * c + extra),
                        "%d − %d = %d." % (r * c + extra, gone, ans)])
        return _tb("A hall has %d rows of %d chairs and %d extra chairs at the side. How many chairs "
                   "altogether?" % (r, c, extra), r * c + extra, "int", {"unit": "chairs"},
                   ["%d × %d = %d." % (r, c, r * c), "%d + %d = %d." % (r * c, extra, r * c + extra)])

    def t_two_step_div():
        k = random.randint(*_by(d, (2, 3), (2, 6), (4, 9)))
        per = random.randint(*_by(d, (2, 6), (6, 12), (12, 25)))
        packs = k * random.randint(1, 3)
        return _tb("A teacher has %d boxes of %d crayons. The crayons are shared equally between %d "
                   "tables. How many crayons does each table get?" % (packs, per, k), packs * per // k,
                   "int", {}, ["%d × %d = %d." % (packs, per, packs * per),
                               "%d ÷ %d = %d." % (packs * per, k, packs * per // k)])

    def t_bar():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(*_by(d, (2, 10), (4, 20), (10, 40))) for _ in cats]
        price = pick(_by(d, [2, 5], [2, 3, 4, 5], [3, 4, 6, 7]))
        return _bar("The chart shows how many cakes were sold each day. Cakes cost £%d each. How much "
                    "money was taken over all four days, in pounds?" % price, cats, vals,
                    sum(vals) * price, ["%d cakes in total." % sum(vals),
                                        "%d × %d = %d." % (sum(vals), price, sum(vals) * price)])

    def t_menu():
        items = [("Pizza", random.randint(4, _by(d, 6, 9, 12))), ("Salad", random.randint(3, 6)),
                 ("Drink", random.randint(1, 3))]
        qs = [random.randint(1, _by(d, 2, 4, 6)) for _ in items]
        tot = sum(p * q for (_, p), q in zip(items, qs))
        note = _by(d, 10, 10, 50)                   # stretch: paying with £50 notes
        pay = (tot // note + 1) * note
        return _dt("A family orders %s, %s and %s from this menu and pays with £%d. How much change do they get, in "
                   "pounds?" % (_pl(qs[0], "pizza"), _pl(qs[1], "salad"), _pl(qs[2], "drink"), pay), ["Item", "Price"],
                   [[n, "£%d" % p] for n, p in items], pay - tot,
                   ["Cost: %s = £%d." % (" + ".join("%d × £%d" % (q, p) for (_, p), q in zip(items, qs)), tot),
                    "£%d − £%d = £%d." % (pay, tot, pay - tot)])

    def t_think():
        x = random.randint(*_by(d, (3, 12), (3, 25), (12, 50)))
        m = random.randint(*_by(d, (2, 3), (2, 6), (4, 9)))
        s = random.randint(1, min(_by(d, 10, 20, 60), x * m - 1))
        return _tb("I think of a number, multiply it by %d and then subtract %d. The answer is %d. What was my number?"
                   % (m, s, x * m - s), x, "int", {},
                   ["Work backwards: %d + %d = %d." % (x * m - s, s, x * m), "%d ÷ %d = %d." % (x * m, m, x)])

    def t_tickets():
        if d == 0:
            adult, child = pick([5, 10]), pick([2, 3, 5])
            a, c = random.randint(1, 2), random.randint(1, 3)
        else:
            adult, child = random.randint(8, 15), random.randint(4, 7)
            a, c = random.randint(1, 3), random.randint(2, 5)
        if d == 2:                                  # stretch: then work out the change
            adult, child = random.randint(12, 25), random.randint(6, 12)
            a, c = random.randint(2, 4), random.randint(3, 6)
            tot = adult * a + child * c
            pay = (tot // 50 + 1) * 50
            return _tb("Zoo tickets cost £%d for an adult and £%d for a child. %d adults and %d children pay "
                       "with £%d. How much change do they get, in pounds?" % (adult, child, a, c, pay),
                       pay - tot, "int", {"unit": "£"},
                       ["%d × %d + %d × %d = %d." % (a, adult, c, child, tot), "%d − %d = %d." % (pay, tot, pay - tot)])
        return _tb("Zoo tickets cost £%d for an adult and £%d for a child. How much do %d adult%s and %d children pay "
                   "altogether, in pounds?" % (adult, child, a, "" if a == 1 else "s", c), adult * a + child * c, "int",
                   {"unit": "£"}, ["%d × %d + %d × %d = %d." % (a, adult, c, child, adult * a + child * c)])

    def t_strip_compare():
        small = random.randint(*_by(d, (2, 10), (4, 30), (25, 99)))
        k = random.randint(*_by(d, (2, 3), (2, 5), (3, 6)))
        return _strip("%s has %d marbles. %s has %d times as many. How many do they have altogether?"
                      % ("Ana", small, "Raj", k), {"mode": "equal_parts", "parts": k + 1, "partLabel": str(small),
                                                   "totalLabel": "?", "unknown": "total"}, small * (k + 1),
                      ["Raj has %d × %d = %d." % (small, k, small * k), "%d + %d = %d." % (small, small * k, small * (k + 1))])

    return _pick_t([t_shop, t_share_after, t_rows_plus, t_two_step_div, t_think, t_tickets],
                   [t_bar, t_menu, t_strip_compare])


# ================================================================== 5.5 ======
def _frac_pair(d):
    den = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 6, 8], [6, 8, 9, 10, 12]))
    num = random.randint(1, den - 1)
    return num, den


@skill("Y5.5.a", "Equivalent fractions, including tenths and hundredths", S5)
def _(d=1):
    d = _d(d)
    num, den = _frac_pair(d)
    while Fraction(num, den).denominator != den:
        num, den = _frac_pair(d)
    k = random.randint(2, _by(d, 4, 6, 9))

    def t_numerator():
        return _tb("Complete:  %d/%d = ___/%d" % (num, den, den * k), num * k, "int", {},
                   ["%d × %d = %d, so multiply the top by %d too." % (den, k, den * k, k)])

    def t_denominator():
        return _tb("Complete:  %d/%d = %d/___" % (num, den, num * k), den * k, "int", {},
                   ["%d × %d = %d, so multiply the bottom by %d too." % (num, k, num * k, k)])

    def t_simplify():
        return _wq("Write %d/%d in its simplest form." % (num * k, den * k), "%d/%d" % (num, den),
                   ["Divide top and bottom by %d: %d/%d." % (k, num, den)], "e.g. 2/3")

    def t_tenths():
        t = random.randint(1, 9)
        return _tb("Complete:  %d/10 = ___/100" % t, t * 10, "int", {},
                   ["%s = %d hundredths." % (_pl(t, "tenth"), t * 10)])

    def t_hundredths():
        t = random.randint(1, 9) * 10
        return _tb("Complete:  %d/100 = ___/10" % t, t // 10, "int", {},
                   ["%d hundredths = %s." % (t, _pl(t // 10, "tenth"))])

    def t_odd_one():
        good = [(num * j, den * j) for j in random.sample(range(2, 7), 2)]
        bad = (num * k + 1, den * k)
        opts = good + [bad]
        random.shuffle(opts)
        return _wq("Which of these is NOT equivalent to %d/%d?  %s" % (num, den,
                                                                      ", ".join("%d/%d" % o for o in opts)),
                   "%d/%d" % bad, ["%d/%d does not simplify to %d/%d." % (bad[0], bad[1], num, den)],
                   "e.g. 3/8")

    def t_area():
        parts = den * k
        if parts > 24:
            return t_numerator()
        return _area("Shade this model to show a fraction equivalent to %d/%d. It has %d equal parts."
                     % (num, den, parts), {"mode": "fraction", "parts": parts}, "%d/%d" % (num * k, parts),
                     ["%d/%d = %d/%d." % (num, den, num * k, parts)], atype="frac")

    def t_hundred_grid():
        t = random.randint(1, 9)
        return _area("This square is one whole split into 100 equal parts. Shade it to show %d/10."
                     % t, {"mode": "fraction", "parts": 100}, "%d/100" % (t * 10),
                     ["%d/10 = %d/100." % (t, t * 10)], atype="frac")

    def t_is_equiv():
        j = random.randint(2, 5)
        same = random.random() < 0.5
        top = num * j if same else num * j + pick([-1, 1])
        if top <= 0:
            top, same = num * j, True
        return _wq("Is %d/%d equivalent to %d/%d? (yes or no)" % (num, den, top, den * j), "yes" if same else "no",
                   ["%d/%d × %d/%d = %d/%d." % (num, den, j, j, num * j, den * j)], "yes / no")

    def t_pizza():
        return _tb("A pizza is cut into %d equal slices. %s eats %d/%d of it. How many slices is that?"
                   % (den * k, _who(), num, den), num * k, "int", {"unit": "slices"},
                   ["%d/%d = %d/%d." % (num, den, num * k, den * k)])

    def t_chain():
        js = [2, 3, 4]
        rows = [["%d/%d" % (num, den)] + ["%d/%d" % (num * j, den * j) for j in js]]
        c = random.randint(1, 3)
        rows[0][c] = ""
        return _dt("Every fraction in the table is equivalent to the first one. The empty cell has denominator %d. What "
                   "is its numerator?" % (den * js[c - 1]), ["Fraction", "× 2", "× 3", "× 4"], rows, num * js[c - 1],
                   ["%d/%d × %d/%d = %d/%d." % (num, den, js[c - 1], js[c - 1], num * js[c - 1], den * js[c - 1])],
                   missing=[0, c])

    def t_bar():
        parts = den * k
        if parts > 12:
            return t_denominator()
        return {"prompt": "Shade the bar to show a fraction equivalent to %d/%d. The bar has %d equal parts."
                          % (num, den, parts), "component": "fraction_bar", "spec": {"parts": parts, "mode": "shade"},
                "answer": "%d/%d" % (num * k, parts), "answer_type": "frac",
                "solution": ["%d/%d = %d/%d, so shade %d parts." % (num, den, num * k, parts, num * k)]}

    def t_line():
        dn = den * 2
        return _nld("Place %d/%d on this number line from 0 to 1. Each small step is 1/%d." % (num, den, dn),
                    Fraction(num, den), 0, 1, Fraction(1, dn), Fraction(1, den),
                    ["%d/%d = %d/%d." % (num, den, num * 2, dn)]) if dn <= 24 else t_numerator()

    def t_same_amount():
        j1, j2 = random.sample([1, 2, 3, 4], 2)
        same = random.random() < 0.6
        top2 = num * j2 if same else num * j2 + 1
        n1, n2 = random.sample(["Ava", "Ben", "Cal", "Dee"], 2)
        return _wq("%s ate %d/%d of a cake. %s ate %d/%d of an identical cake. Did they eat the same amount? (yes or no)"
                   % (n1, num * j1, den * j1, n2, top2, den * j2), "yes" if same else "no",
                   ["%d/%d = %d/%d, and %d/%d %s %d/%d." % (num * j1, den * j1, num, den, top2, den * j2,
                                                         "=" if same else "≠", num, den)], "yes / no")

    def t_class():
        return _wq("%d out of %d pupils in a group wear glasses. Write the fraction who wear glasses in its simplest form."
                   % (num * k, den * k), "%d/%d" % (num, den),
                   ["%d/%d ÷ %d/%d = %d/%d." % (num * k, den * k, k, k, num, den)], "e.g. 3/4")

    def t_scale_top():
        target_den = den * k
        return _tb("%d/%d of a pie is eaten. The pie was cut into %d equal slices. How many slices are left?"
                   % (num, den, target_den), target_den - num * k, "int", {"unit": "slices"},
                   ["%d/%d = %d/%d eaten." % (num, den, num * k, target_den),
                    "%d − %d = %d left." % (target_den, num * k, target_den - num * k)])

    return _pick_t([t_numerator, t_denominator, t_simplify, t_tenths, t_hundredths, t_odd_one, t_is_equiv, t_pizza,
                    t_same_amount, t_class, t_scale_top],
                   [t_area, t_hundred_grid, t_chain, t_bar, t_line])


@skill("Y5.5.b", "Compare and order fractions with related denominators", S5)
def _(d=1):
    d = _d(d)
    base = pick([2, 3, 4, 5])
    dens = [base * m for m in random.sample([1, 2, 3, 4], _by(d, 2, 3, 3))]
    fr = []
    while len(fr) < len(dens):                 # distinct values; redraw all if we get stuck
        fr = []
        for dn in dens:
            f = Fraction(random.randint(1, dn - 1), dn)
            if f in fr:
                break
            fr.append(f)
    shown = ["%d/%d" % (f.numerator * (dn // f.denominator), dn) for f, dn in zip(fr, dens)]
    common = max(dens)
    while any(common % x for x in dens):
        common += max(dens)

    def t_larger():
        a, b = shown[0], shown[1]
        fa, fb = fr[0], fr[1]
        if fa == fb:
            return t_order()
        return _wq("Which is larger, %s or %s?" % (a, b), a if fa > fb else b,
                   ["Write both with denominator %d." % common], "e.g. 3/4")

    def t_symbol():
        fa, fb = fr[0], fr[1]
        sym = "<" if fa < fb else (">" if fa > fb else "=")
        return _wq("Write <, > or =:  %s ___ %s" % (shown[0], shown[1]), sym,
                   ["Make the denominators the same, then compare the numerators."], "<, > or =")

    def t_order():
        if len(shown) < 3:
            return t_symbol()
        order = [s for _, s in sorted(zip(fr, shown))]
        return _wq("Write these fractions in order, smallest first, separated by commas: %s"
                   % ", ".join(shown), ", ".join(order),
                   ["Convert to a common denominator of %d." % common], "e.g. 1/4, 1/2, 5/8")

    def t_largest():
        if len(shown) < 3:
            return t_symbol()
        return _wq("Which of these is the largest? %s" % ", ".join(shown),
                   shown[fr.index(max(fr))], ["Compare with denominator %d." % common], "e.g. 5/8")

    def t_half():
        dn = pick([6, 8, 10, 12])
        n = random.choice([x for x in range(1, dn) if 2 * x != dn])
        return _wq("Is %d/%d more or less than one half? (type more or less)" % (n, dn),
                   "more" if 2 * n > dn else "less", ["Half of %d is %d." % (dn, dn // 2)], "more / less")

    def t_line():
        dn = pick([4, 8, 10])
        n = random.randint(1, dn - 1)
        return _nld("Place %d/%d on the number line from 0 to 1." % (n, dn), Fraction(n, dn), 0, 1,
                    Fraction(1, dn), Fraction(1, dn) if dn <= 4 else Fraction(1, 2) if dn == 8 else
                    Fraction(1, 10), ["%d/%d is %d of %d equal steps." % (n, dn, n, dn)])

    def t_smallest():
        if len(shown) < 3:
            return t_symbol()
        return _wq("Which of these is the smallest? %s" % ", ".join(shown), shown[fr.index(min(fr))],
                   ["Write them all with denominator %d." % common], "e.g. 1/4")

    def t_who():
        a, b = shown[0], shown[1]
        if fr[0] == fr[1]:
            return t_half()
        n1, n2 = random.sample(["Ava", "Ben", "Cal", "Dee"], 2)
        return _wq("%s ate %s of a cake and %s ate %s of the same size cake. Who ate more?" % (n1, a, n2, b),
                   n1 if fr[0] > fr[1] else n2, ["With denominator %d: compare the numerators." % common], "name")

    def t_biggest_top():
        dn = base * 2
        f = Fraction(random.randint(1, base - 1), base)
        top = int(f * dn)
        ans = top - 1
        if ans < 1:
            return t_symbol()
        return _tb("___/%d < %s. What is the LARGEST whole number that can go in the gap?" % (dn, _fs(f)), ans, "int", {},
                   ["%s = %d/%d." % (_fs(f), top, dn), "So the numerator must be less than %d." % top])

    def t_between():
        lo_, hi_, good, bads = pick([
            (Fraction(1, 4), Fraction(1, 2), Fraction(3, 8), [Fraction(1, 8), Fraction(5, 8)]),
            (Fraction(1, 3), Fraction(2, 3), Fraction(1, 2), [Fraction(1, 6), Fraction(5, 6)]),
            (Fraction(1, 2), Fraction(3, 4), Fraction(5, 8), [Fraction(3, 8), Fraction(7, 8)]),
            (Fraction(2, 5), Fraction(3, 5), Fraction(1, 2), [Fraction(3, 10), Fraction(7, 10)]),
            (Fraction(1, 5), Fraction(2, 5), Fraction(3, 10), [Fraction(1, 10), Fraction(9, 10)])])
        opts = [good] + bads
        random.shuffle(opts)
        return _wq("Which of these lies between %s and %s?  %s" % (_fs(lo_), _fs(hi_), ", ".join(_fs(o) for o in opts)),
                   _fs(good), ["%s < %s < %s." % (_fs(lo_), _fs(good), _fs(hi_))], "e.g. 3/8")

    def t_table():
        names = random.sample(["Red", "Blue", "Green", "Gold"], len(shown))
        rows = [[n, s] for n, s in zip(names, shown)]
        win = names[fr.index(max(fr))]
        return _dt("The table shows what fraction of their bottle each team drank. Which team drank the most?",
                   ["Team", "Fraction drunk"], rows, win, ["With denominator %d, the largest numerator wins." % common],
                   atype="str")

    return _pick_t([t_larger, t_symbol, t_order, t_largest, t_half, t_smallest, t_who, t_biggest_top, t_between],
                   [t_line, t_table])


@skill("Y5.5.c", "Mixed numbers and improper fractions", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 6, 8], [6, 7, 8, 9, 12]))
    w = random.randint(1, _by(d, 3, 5, 9))
    r = random.choice([v for v in range(1, den) if Fraction(v, den).denominator == den])
    imp = w * den + r

    def t_to_improper():
        return _wq("Write %d %d/%d as an improper fraction." % (w, r, den), "%d/%d" % (imp, den),
                   ["%d × %d + %d = %d." % (w, den, r, imp), "So %d/%d." % (imp, den)], "e.g. 7/4")

    def t_to_mixed():
        return _wq("Write %d/%d as a mixed number (like 2 1/3)." % (imp, den), "%d %d/%d" % (w, r, den),
                   ["%d ÷ %d = %d remainder %d." % (imp, den, w, r)], "e.g. 2 1/3")

    def t_wholes():
        return _tb("How many whole ones are there in %d/%d?" % (imp, den), w, "int", {},
                   ["%d ÷ %d = %d remainder %d." % (imp, den, w, r)])

    def t_is_improper():
        a = random.randint(1, 12)
        b = random.randint(2, 10)
        return _wq("Is %d/%d an improper fraction? (yes or no)" % (a, b), "yes" if a >= b else "no",
                   ["An improper fraction has a numerator at least as big as its denominator."], "yes / no")

    def t_sum_over():
        pairs = [(x, y) for x in range(1, den) for y in range(1, den) if x + y > den and (x + y) % den]
        if not pairs:
            return t_to_mixed()
        x, y = pick(pairs)
        return _tb("Work out %d/%d + %d/%d and write the answer as a mixed number." % (x, den, y, den),
                   _mixed(Fraction(x + y, den)), "frac", {"text": True, "placeholder": "e.g. 1 1/4"},
                   ["%d/%d + %d/%d = %d/%d." % (x, den, y, den, x + y, den),
                    "= %s." % _mixed(Fraction(x + y, den))])

    def t_line():
        return _nld("Place %d/%d on the number line." % (imp, den), Fraction(imp, den), 0, w + 2,
                    Fraction(1, den), 1, ["%d/%d = %d %d/%d." % (imp, den, w, r, den)])

    def t_numerator():
        return _tb("Complete:  %d %d/%d = ___/%d" % (w, r, den, den), imp, "int", {},
                   ["%s = %d/%d." % (_pl(w, "whole"), w * den, den), "%d + %d = %d." % (w * den, r, imp)])

    def t_pieces():
        name = pick(["quarter", "third", "fifth", "sixth", "eighth"])
        dn = {"quarter": 4, "third": 3, "fifth": 5, "sixth": 6, "eighth": 8}[name]
        k = dn * random.randint(1, 3) + random.randint(1, dn - 1)
        return _fq("A café has %d %ss of cake left (each piece is 1/%d of a whole cake). How many cakes is that? Write it as "
                   "a mixed number." % (k, name, dn), Fraction(k, dn),
                   ["%d/%d = %s." % (k, dn, _mixed(Fraction(k, dn)))], "e.g. 2 3/4")

    def t_compare():
        other = Fraction(imp, den) + pick([Fraction(1, den), -Fraction(1, den), Fraction(1, 1)])
        if other <= 0 or other.denominator == 1:
            other = Fraction(imp + 1, den)
        return _fq("Which is larger, %d/%d or %s? Type the larger one." % (imp, den, _mixed(other)),
                   max(Fraction(imp, den), other), ["%d/%d = %s." % (imp, den, _mixed(Fraction(imp, den)))],
                   "e.g. 7/4")

    def t_table():
        ws = random.sample(range(1, 6), 3)
        rs = [random.randint(1, den - 1) for _ in ws]
        rows = [["%d %d/%d" % (x, y, den), "%d/%d" % (x * den + y, den)] for x, y in zip(ws, rs)]
        k = random.randrange(3)
        return _dt("The table shows mixed numbers and the same amounts as improper fractions (all over %d). What is the "
                   "missing numerator?" % den, ["Mixed number", "Improper fraction"],
                   [[a, "?/%d" % den if i == k else b] for i, (a, b) in enumerate(rows)], ws[k] * den + rs[k],
                   ["%d × %d + %d = %d." % (ws[k], den, rs[k], ws[k] * den + rs[k])])

    def t_bars():
        if den > 8:
            return t_wholes()
        return _tb("%d bars are each split into %d equal parts. %s and %s more are shaded. How many parts are shaded "
                   "altogether?" % (w + 1, den, _pl(w, "whole bar"), _pl(r, "part")), imp, "int", {},
                   ["%d × %d + %d = %d, so %d/%d." % (w, den, r, imp, imp, den)])

    return _pick_t([t_to_improper, t_to_mixed, t_wholes, t_is_improper, t_sum_over, t_numerator, t_pieces,
                    t_compare, t_bars], [t_line, t_table])


@skill("Y5.5.d", "Add fractions with the same or related denominators", S5)
def _(d=1):
    d = _d(d)
    base = pick([2, 3, 4, 5])
    m = pick(_by(d, [1], [2, 3], [2, 3, 4]))
    big = base * m
    a = random.randint(1, base - 1) if base > 1 else 1
    b = random.randint(1, big - 1)
    fa, fb = Fraction(a, base), Fraction(b, big)
    s = fa + fb

    def t_plain():
        return _fq("Work out %d/%d + %d/%d." % (a, base, b, big), s,
                   ["%d/%d = %d/%d." % (a, base, a * m, big), "%d/%d + %d/%d = %d/%d."
                    % (a * m, big, b, big, a * m + b, big)])

    def t_mixed_answer():
        if s <= 1:
            return t_plain()
        return _wq("Work out %d/%d + %d/%d. Give your answer as a mixed number in its simplest form."
                   % (a, base, b, big), _mixed(s),
                   ["%d/%d + %d/%d = %d/%d." % (a * m, big, b, big, a * m + b, big),
                    "= %s." % _mixed(s)], "e.g. 1 1/4")

    def t_same():
        dn = pick([5, 7, 8, 9, 10, 12])
        x, y = random.randint(1, dn - 1), random.randint(1, dn - 1)
        return _fq("Work out %d/%d + %d/%d." % (x, dn, y, dn), Fraction(x + y, dn),
                   ["Add the numerators: %d/%d." % (x + y, dn)])

    def t_word():
        return _fq("%s drinks %d/%d of a bottle of water in the morning and %d/%d of it in the "
                   "afternoon. What fraction of the bottle is that altogether?" % (_who(), a, base, b, big),
                   s, ["%d/%d = %d/%d." % (a, base, a * m, big), "%d/%d + %d/%d = %d/%d."
                       % (a * m, big, b, big, a * m + b, big)])

    def t_bar():
        if s > 1:
            return t_plain()
        return {"prompt": "Shade the bar to show %d/%d + %d/%d. The bar has %d equal parts."
                          % (a, base, b, big, big),
                "component": "fraction_bar", "spec": {"parts": big, "mode": "shade"},
                "answer": "%d/%d" % (a * m + b, big), "answer_type": "frac",
                "solution": ["%d/%d = %d/%d." % (a, base, a * m, big),
                             "%d + %d = %d parts." % (a * m, b, a * m + b)]}

    def t_missing():
        if s >= 1 or fb == s:
            return t_plain()
        return _fq("%d/%d + ___ = %s. What is the missing fraction?" % (a, base, _fs(s)), fb,
                   ["%s − %d/%d = %s." % (_fs(s), a, base, _fs(fb))])

    def t_three():
        x = random.randint(1, big - 1)
        tot = fa + fb + Fraction(x, big)
        return _fq("Work out %d/%d + %d/%d + %d/%d." % (a, base, b, big, x, big), tot,
                   ["%d/%d = %d/%d." % (a, base, a * m, big),
                    "%d + %d + %d = %d, so %d/%d." % (a * m, b, x, a * m + b + x, a * m + b + x, big)])

    def t_more_than_one():
        return _wq("Is %d/%d + %d/%d more than 1, less than 1 or equal to 1? (type more, less or equal)"
                   % (a, base, b, big), "more" if s > 1 else ("less" if s < 1 else "equal"),
                   ["%d/%d + %d/%d = %d/%d." % (a * m, big, b, big, a * m + b, big)], "more / less / equal")

    def t_top():
        return _tb("%d/%d + %d/%d = ___/%d. What is the missing numerator?" % (a, base, b, big, big), a * m + b, "int", {},
                   ["%d/%d = %d/%d." % (a, base, a * m, big), "%d + %d = %d." % (a * m, b, a * m + b)])

    def t_paint():
        if s > 1:
            return t_top()
        return _fq("%s paints %d/%d of a fence on Saturday and %d/%d of it on Sunday. What fraction of the fence is painted?"
                   % (_who(), a, base, b, big), s,
                   ["%d/%d = %d/%d." % (a, base, a * m, big), "%d/%d + %d/%d = %d/%d." % (a * m, big, b, big, a * m + b, big)])

    def t_line():
        if s > 2:
            return t_plain()
        return _nld("Start at %d/%d and count on %d/%d. Mark where you land." % (a, base, b, big), s, 0, 2,
                    Fraction(1, big), 1, ["%d/%d = %d/%d." % (a, base, a * m, big),
                                          "%d/%d + %d/%d = %d/%d." % (a * m, big, b, big, a * m + b, big)])

    def t_pairs_one():
        dn = pick([4, 6, 8, 10, 12])
        x = random.randint(1, dn - 1)
        others = random.sample([y for y in range(1, dn) if y != dn - x], 2)
        opts = [dn - x] + others
        random.shuffle(opts)
        return _wq("Which of these adds to %d/%d to make exactly 1?  %s" % (x, dn, ", ".join("%d/%d" % (o, dn) for o in opts)),
                   "%d/%d" % (dn - x, dn), ["%d/%d + %d/%d = %d/%d = 1." % (x, dn, dn - x, dn, dn, dn)], "e.g. 3/8")

    def t_table():
        rows, ans = [], None
        k = random.randrange(3)
        for i in range(3):
            bs = pick([2, 3, 4, 5])
            mm = pick([2, 3])
            x, y = random.randint(1, bs - 1), random.randint(1, bs * mm - 1)
            tot = Fraction(x, bs) + Fraction(y, bs * mm)
            rows.append(["%d/%d" % (x, bs), "%d/%d" % (y, bs * mm), _fs(tot)])
            if i == k:
                ans = tot
        rows[k][2] = ""
        return _dt("In each row, first + second = total. What fraction belongs in the empty cell? (any equivalent form)",
                   ["First", "Second", "Total"], rows, _fs(ans), ["%s + %s = %s." % (rows[k][0], rows[k][1], _fs(ans))],
                   missing=[k, 2], atype="frac", placeholder="e.g. 7/8")

    def t_recipe():
        if s > 2:
            return t_plain()
        return _fq("A recipe uses %d/%d of a cup of milk and %d/%d of a cup of water. How many cups of liquid is that?"
                   % (a, base, b, big), s, ["%d/%d = %d/%d." % (a, base, a * m, big),
                                            "%d/%d + %d/%d = %d/%d." % (a * m, big, b, big, a * m + b, big)])

    return _pick_t([t_plain, t_mixed_answer, t_same, t_word, t_missing, t_three, t_more_than_one, t_top, t_paint,
                    t_pairs_one, t_recipe],
                   [t_bar, t_line, t_table])


@skill("Y5.5.e", "Subtract fractions with the same or related denominators", S5)
def _(d=1):
    d = _d(d)
    base = pick([2, 3, 4, 5])
    m = pick(_by(d, [1, 2], [2, 3], [2, 3, 4]))
    big = base * m
    a = random.randint(1, base - 1)
    fa = Fraction(a, base)
    b = random.randint(1, a * m - 1) if a * m > 1 else None

    def t_plain():
        if b is None:
            return t_from_one()
        return _fq("Work out %d/%d − %d/%d." % (a, base, b, big), fa - Fraction(b, big),
                   ["%d/%d = %d/%d." % (a, base, a * m, big),
                    "%d/%d − %d/%d = %d/%d." % (a * m, big, b, big, a * m - b, big)])

    def t_from_one():
        x = random.randint(1, big - 1)
        return _fq("Work out 1 − %d/%d." % (x, big), Fraction(big - x, big),
                   ["1 = %d/%d." % (big, big), "%d/%d − %d/%d = %d/%d." % (big, big, x, big, big - x, big)])

    def t_from_mixed():
        w = random.randint(1, 3)
        x = random.randint(1, big - 1)
        return _tb("Work out %d − %d/%d. Write the answer as a mixed number." % (w + 1, x, big),
                   _mixed(Fraction(w + 1) - Fraction(x, big)), "frac", {"text": True, "placeholder": "e.g. 1 3/4"},
                   ["%d − %d/%d = %s." % (w + 1, x, big, _mixed(Fraction(w + 1) - Fraction(x, big)))])

    def t_word():
        if b is None:
            return t_from_one()
        return _fq("A jug is %d/%d full. %s pours out %d/%d of a jug. How full is the jug now?"
                   % (a, base, _who(), b, big), fa - Fraction(b, big),
                   ["%d/%d − %d/%d = %d/%d." % (a * m, big, b, big, a * m - b, big)])

    def t_how_much_more():
        if big < 3:
            return t_from_one()
        x, y = sorted(random.sample(range(1, big), 2))
        return _fq("Tom ate %d/%d of a pizza and Ella ate %d/%d of the same size pizza. How much more "
                   "did Ella eat?" % (x, big, y, big), Fraction(y - x, big),
                   ["%d/%d − %d/%d = %d/%d." % (y, big, x, big, y - x, big)])

    def t_line():
        x = random.randint(big // 2 + 1, big - 1) if big > 2 else 1
        y = random.randint(1, x - 1) if x > 1 else 0
        if not y:
            return t_from_one()
        return _nld("Start at %d/%d and count back %d/%d. Mark where you land." % (x, big, y, big),
                    Fraction(x - y, big), 0, 1, Fraction(1, big), Fraction(1, big) if big <= 6 else
                    Fraction(1, base), ["%d/%d − %d/%d = %d/%d." % (x, big, y, big, x - y, big)])

    def t_missing():
        if b is None:
            return t_from_one()
        diff = fa - Fraction(b, big)
        return _fq("___ − %d/%d = %s. What is the missing fraction?" % (b, big, _fs(diff)), fa,
                   ["Add back: %s + %d/%d = %s." % (_fs(diff), b, big, _fs(fa))])

    def t_left_more():
        if big < 3:
            return t_from_one()
        x, y = random.sample(range(1, big), 2)
        n1, n2 = random.sample(["Ava", "Ben", "Cal", "Dee"], 2)
        return _wq("%s and %s each start with a full bottle of water. %s drinks %d/%d of it and %s drinks %d/%d of it. "
                   "Who has more water left?" % (n1, n2, n1, x, big, n2, y, big), n1 if x < y else n2,
                   ["%s has %d/%d left; %s has %d/%d left." % (n1, big - x, big, n2, big - y, big)], "name")

    def t_tank():
        if b is None:
            return t_from_one()
        return _fq("A fish tank is %d/%d full. Some water leaks out and now it is %d/%d full. What fraction of the tank "
                   "leaked out?" % (a, base, a * m - b, big), Fraction(b, big),
                   ["%d/%d = %d/%d." % (a, base, a * m, big), "%d/%d − %d/%d = %d/%d." % (a * m, big, a * m - b, big, b, big)])

    def t_top():
        if b is None:
            return t_from_one()
        return _tb("%d/%d − %d/%d = ___/%d. What is the missing numerator?" % (a, base, b, big, big), a * m - b, "int", {},
                   ["%d/%d = %d/%d." % (a, base, a * m, big), "%d − %d = %d." % (a * m, b, a * m - b)])

    def t_bar():
        if big > 12 or big < 3:
            return t_from_one()
        x = random.randint(2, big - 1)
        y = random.randint(1, x - 1)
        return {"prompt": "Shade the bar to show %d/%d − %d/%d. The bar has %d equal parts." % (x, big, y, big, big),
                "component": "fraction_bar", "spec": {"parts": big, "mode": "shade"},
                "answer": "%d/%d" % (x - y, big), "answer_type": "frac",
                "solution": ["%d − %d = %s." % (x, y, _pl(x - y, "part"))]}

    return _pick_t([t_plain, t_from_one, t_from_mixed, t_word, t_how_much_more, t_missing, t_left_more, t_tank, t_top],
                   [t_line, t_bar])


@skill("Y5.5.f", "Add and subtract mixed numbers", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 4, 5], [3, 4, 6, 8], [6, 8, 10, 12]))
    w1, w2 = random.randint(1, 5), random.randint(1, 4)
    a, b = random.randint(1, den - 1), random.randint(1, den - 1)
    A, B = w1 + Fraction(a, den), w2 + Fraction(b, den)

    def t_add():
        return _wq("Work out %d %d/%d + %d %d/%d. Write the answer as a mixed number in its simplest form."
                   % (w1, a, den, w2, b, den), _mixed(A + B),
                   ["Wholes: %d + %d = %d. Parts: %d/%d + %d/%d = %d/%d." % (w1, w2, w1 + w2, a, den, b,
                                                                              den, a + b, den),
                    "= %s." % _mixed(A + B)], "e.g. 3 1/2")

    def t_sub():
        big, small = max(A, B), min(A, B)
        if big == small:
            return t_add()
        return _wq("Work out %s − %s. Write the answer as a mixed number or whole number in its simplest "
                   "form." % (_mixed(big), _mixed(small)), _mixed(big - small),
                   ["%s − %s = %s." % (_mixed(big), _mixed(small), _mixed(big - small))], "e.g. 1 1/4")

    def t_whole_plus():
        w = random.randint(2, 6)
        return _wq("Work out %d + %s." % (w, _mixed(A)), _mixed(w + A),
                   ["Add the wholes: %d." % (w + w1)], "e.g. 5 2/3")

    def t_word():
        return _wq("A plank is %s m long. Another is %s m long. How long are they end to end, in m? "
                   "(mixed number, simplest form)" % (_mixed(A), _mixed(B)), _mixed(A + B),
                   ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))], "e.g. 4 1/2")

    def t_line():
        return _nld("Start at %s and count on %d/%d. Mark where you land." % (_mixed(A), b, den),
                    A + Fraction(b, den), w1 - 1 if w1 > 1 else 0, w1 + 3, Fraction(1, den), 1,
                    ["%s + %d/%d = %s." % (_mixed(A), b, den, _mixed(A + Fraction(b, den)))])

    def t_related():
        base_ = pick([2, 3, 4, 5])
        big_ = base_ * pick([2, 3]) if base_ < 5 else 10
        xa = random.randint(1, base_ - 1)
        yb = random.choice([v for v in range(1, big_) if Fraction(v, big_).denominator == big_])
        x, y = w1 + Fraction(xa, base_), w2 + Fraction(yb, big_)
        k_ = big_ // base_
        return _wq("Work out %d %d/%d + %d %d/%d. Write the answer as a mixed number in its simplest form."
                   % (w1, xa, base_, w2, yb, big_), _mixed(x + y),
                   ["%d/%d = %d/%d." % (xa, base_, xa * k_, big_),
                    "%d %d/%d + %d %d/%d = %s." % (w1, xa * k_, big_, w2, yb, big_, _mixed(x + y))], "e.g. 4 3/8")

    def t_whole_minus():
        w = w1 + w2 + 1
        return _wq("Work out %d − %s. Write the answer as a mixed number." % (w, _mixed(A)), _mixed(w - A),
                   ["%d − %d = %d." % (w, w1, w - w1), "%d − %s = %s." % (w - w1, _fs(A - w1), _mixed(w - A))], "e.g. 2 1/3")

    def t_missing():
        return _fq("%s + ___ = %s. What is the missing number? (fraction or mixed number)" % (_mixed(A), _mixed(A + B)), B,
                   ["%s − %s = %s." % (_mixed(A + B), _mixed(A), _mixed(B))], "e.g. 1 1/4")

    def t_compare():
        return _wq("Is %s + %s more than 5, less than 5 or equal to 5? (type more, less or equal)" % (_mixed(A), _mixed(B)),
                   "more" if A + B > 5 else ("less" if A + B < 5 else "equal"),
                   ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))], "more / less / equal")

    def t_table():
        rows = [["Monday", "%s km" % _mixed(A)], ["Tuesday", "%s km" % _mixed(B)]]
        return _dt("The table shows how far %s walked. How far is that altogether, in km? (mixed number, simplest form)"
                   % _who(), ["Day", "Distance"], rows, _mixed(A + B),
                   ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))], atype="frac",
                   placeholder="e.g. 3 1/2")

    def t_hours():
        return _wq("A film lasts %s hours and the next one lasts %s hours. How many hours is that altogether? (mixed "
                   "number, simplest form)" % (_mixed(A), _mixed(B)), _mixed(A + B),
                   ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))], "e.g. 3 1/2")

    def t_wholes():
        return _tb("Work out %s + %s. How many WHOLE ones are in the answer?" % (_mixed(A), _mixed(B)), int(A + B), "int",
                   {}, ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))])

    return _pick_t([t_add, t_sub, t_whole_plus, t_word, t_related, t_whole_minus, t_missing, t_compare, t_hours,
                    t_wholes],
                   [t_line, t_table])


@skill("Y5.5.g", "Multiply proper fractions by whole numbers", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [3, 4, 5], [4, 5, 6, 8], [6, 8, 9, 10, 12]))
    num = random.randint(1, den - 1)
    k = random.randint(2, _by(d, 4, 6, 9))
    p = Fraction(num * k, den)

    def t_plain():
        return _fq("Work out %d/%d × %d." % (num, den, k), p,
                   ["%d × %d = %d, so %d/%d." % (num, k, num * k, num * k, den)])

    def t_mixed_answer():
        if p <= 1:
            return t_plain()
        return _wq("Work out %d × %d/%d. Write the answer as a mixed number in its simplest form."
                   % (k, num, den), _mixed(p), ["%d/%d = %s." % (num * k, den, _mixed(p))], "e.g. 2 1/4")

    def t_repeated():
        return _fq("Write %s as a multiplication and work it out." % " + ".join(["%d/%d" % (num, den)] * k),
                   p, ["%d × %d/%d = %d/%d." % (k, num, den, num * k, den)])

    def t_numerator():
        return _tb("%d/%d × %d = ___/%d. What is the missing numerator?" % (num, den, k, den), num * k,
                   "int", {}, ["%d × %d = %d." % (num, k, num * k)])

    def t_word():
        return _fq("Each glass holds %d/%d of a litre. How many litres do %d glasses hold?"
                   % (num, den, k), p, ["%d × %d/%d = %d/%d litres." % (k, num, den, num * k, den)])

    def t_area():
        if num * k > den or den > 12:
            return t_plain()
        return {"prompt": "Shade the bar to show %d/%d × %d." % (num, den, k),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (num * k, den), "answer_type": "frac",
                "solution": ["%d lots of %d/%d is %d/%d." % (k, num, den, num * k, den)]}

    def t_more_than_one():
        return _wq("Is %d × %d/%d more than 1, less than 1 or equal to 1? (type more, less or equal)" % (k, num, den),
                   "more" if p > 1 else ("less" if p < 1 else "equal"),
                   ["%d × %d/%d = %d/%d." % (k, num, den, num * k, den)], "more / less / equal")

    def t_jumps():
        if p > 3:
            return t_plain()
        return _nld("Make %d jumps of %d/%d from 0. Mark where you land." % (k, num, den), p, 0, 3, Fraction(1, den), 1,
                    ["%d × %d/%d = %d/%d." % (k, num, den, num * k, den)])

    def t_ribbon():
        return _fq("%s cuts %d pieces of ribbon, each %d/%d of a metre long. How many metres of ribbon is that?"
                   % (_who(), k, num, den), p, ["%d × %d/%d = %d/%d m." % (k, num, den, num * k, den)])

    def t_how_many():
        n = num * random.randint(2, 6)
        kk = n // num
        return _tb("How many lots of %d/%d make %d/%d?" % (num, den, n, den), kk, "int", {},
                   ["%d ÷ %d = %d." % (n, num, kk)])

    def t_table():
        ks = [2, 3, 4, 5]
        rows = [[x, "%d/%d" % (num * x, den)] for x in ks]
        i = random.randrange(4)
        rows[i][1] = ""
        return _dt("Each row multiplies %d/%d by a whole number. What is the missing numerator? (All answers are out "
                   "of %d.)" % (num, den, den), ["× by", "Answer"], rows, num * ks[i],
                   ["%d × %d = %d, so %d/%d." % (num, ks[i], num * ks[i], num * ks[i], den)], missing=[i, 1])

    return _pick_t([t_plain, t_mixed_answer, t_repeated, t_numerator, t_word, t_more_than_one, t_ribbon, t_how_many],
                   [t_area, t_jumps, t_table])


@skill("Y5.5.h", "Multiply mixed numbers by whole numbers", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 4], [3, 4, 5], [4, 5, 6, 8]))
    w = random.randint(1, _by(d, 2, 3, 5))
    r = random.randint(1, den - 1)
    k = random.randint(2, _by(d, 3, 5, 6))
    M = w + Fraction(r, den)

    def t_plain():
        return _wq("Work out %s × %d. Give the answer as a mixed number or whole number in its simplest "
                   "form." % (_mixed(M), k), _mixed(M * k),
                   ["%d × %d = %d and %d/%d × %d = %s." % (w, k, w * k, r, den, k, _fs(Fraction(r * k, den))),
                    "%d + %s = %s." % (w * k, _fs(Fraction(r * k, den)), _mixed(M * k))], "e.g. 7 1/2")

    def t_improper():
        return _fq("Work out %s × %d. You may give an improper fraction." % (_mixed(M), k), M * k,
                   ["%s = %d/%d." % (_mixed(M), w * den + r, den),
                    "%d/%d × %d = %d/%d." % (w * den + r, den, k, (w * den + r) * k, den)])

    def t_word():
        return _wq("A recipe needs %s cups of flour. How many cups for %d batches? (mixed number or "
                   "whole number, simplest form)" % (_mixed(M), k), _mixed(M * k),
                   ["%s × %d = %s." % (_mixed(M), k, _mixed(M * k))], "e.g. 4 1/2")

    def t_whole_part():
        return _tb("Work out %s × %d. How many WHOLE ones are in the answer?" % (_mixed(M), k),
                   int(M * k), "int", {}, ["%s × %d = %s." % (_mixed(M), k, _mixed(M * k))])

    def t_lengths():
        return _wq("A shelf is %s m long. How long are %d of these shelves end to end, in m? (mixed number or whole "
                   "number, simplest form)" % (_mixed(M), k), _mixed(M * k),
                   ["%d × %d = %d m; %d × %d/%d = %s m." % (k, w, k * w, k, r, den, _fs(Fraction(r * k, den))),
                    "Total %s m." % _mixed(M * k)], "e.g. 6 3/4")

    def t_repeated():
        return _wq("Work out %s. Write the answer as a mixed number or whole number in its simplest form."
                   % " + ".join([_mixed(M)] * k), _mixed(M * k),
                   ["That is %s × %d." % (_mixed(M), k), "= %s." % _mixed(M * k)], "e.g. 7 1/2")

    def t_missing():
        return _tb("%s × ___ = %s. What is the missing whole number?" % (_mixed(M), _mixed(M * k)), k, "int", {},
                   ["%s × %d = %s." % (_mixed(M), k, _mixed(M * k))])

    def t_compare():
        lim = int(M * k) + pick([0, 1])
        return _wq("Is %s × %d more or less than %d? (type more or less)" % (_mixed(M), k, lim),
                   "more" if M * k > lim else "less", ["%s × %d = %s." % (_mixed(M), k, _mixed(M * k))], "more / less") \
            if M * k != lim else t_plain()

    def t_table():
        ks = [2, 3, 4]
        rows = [[x, _mixed(M * x)] for x in ks]
        i = random.randrange(3)
        return _dt("Each row shows %s multiplied by a whole number. What belongs in the empty cell? (mixed number or "
                   "whole number)" % _mixed(M), ["× by", "Answer"],
                   [[x, "" if j == i else v] for j, (x, v) in enumerate(rows)], _mixed(M * ks[i]),
                   ["%s × %d = %s." % (_mixed(M), ks[i], _mixed(M * ks[i]))], missing=[i, 1], atype="frac",
                   placeholder="e.g. 4 1/2")

    def t_jumps():
        if M * k > 10:
            return t_plain()
        return _nld("Make %d jumps of %s from 0. Mark where you land." % (k, _mixed(M)), M * k, 0, 10, Fraction(1, den), 1,
                    ["%d × %s = %s." % (k, _mixed(M), _mixed(M * k))])

    return _pick_t([t_plain, t_improper, t_word, t_whole_part, t_lengths, t_repeated, t_missing, t_compare],
                   [t_table, t_jumps])


@skill("Y5.5.i", "Fractions of amounts and fraction problems", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 6, 8], [6, 7, 8, 9, 12]))
    num = random.randint(1, den - 1)
    x = den * random.randint(_by(d, 3, 5, 10), _by(d, 12, 30, 60))

    def t_of():
        return _tb("What is %d/%d of %d?" % (num, den, x), x // den * num, "int", {},
                   ["%d ÷ %d = %d." % (x, den, x // den), "%d × %d = %d." % (x // den, num, x // den * num)])

    def t_money():
        return _tb("A coat costs £%d. In a sale it costs %d/%d of that. What is the sale price, in pounds?"
                   % (x, num, den), x // den * num, "int", {"unit": "£"},
                   ["%d ÷ %d × %d = %d." % (x, den, num, x // den * num)])

    def t_inverse():
        part = x // den * num
        return _tb("%d/%d of a number is %d. What is the number?" % (num, den, part), x, "int", {},
                   ["%d ÷ %d = %d is one part." % (part, num, x // den), "%d × %d = %d." % (x // den, den, x)])

    def t_remaining():
        return _tb("A class of %d pupils: %d/%d walk to school. How many do NOT walk?" % (x, num, den),
                   x - x // den * num, "int", {}, ["%d/%d of %d = %d." % (num, den, x, x // den * num),
                                                   "%d − %d = %d." % (x, x // den * num, x - x // den * num)])

    def t_measure():
        kind, unit, whole = pick([("1 hour", "minutes", 60), ("1 metre", "cm", 100), ("1 kg", "g", 1000),
                                  ("1 litre", "ml", 1000)])
        dn = pick([k for k in (2, 3, 4, 5, 10) if whole % k == 0])
        nm = random.randint(1, dn - 1)
        return _tb("How many %s are in %d/%d of %s?" % (unit, nm, dn, kind), whole // dn * nm, "int",
                   {"unit": unit}, ["%s = %d %s." % (kind, whole, unit),
                                    "%d ÷ %d × %d = %d." % (whole, dn, nm, whole // dn * nm)])

    def t_strip():
        return _strip("The strip shows %d split into %d equal parts. What %s worth?"
                      % (x, den, "is 1 part" if num == 1 else "are %d parts" % num), {"mode": "equal_parts", "parts": den, "partLabel": "?",
                                        "totalLabel": str(x), "unknown": "part"},
                      x // den * num, ["One part is %d." % (x // den), "%s: %d." % (_pl(num, "part"), x // den * num)])

    def t_compare():
        d2 = pick([2, 4, 5, 10])
        y = d2 * random.randint(3, 20)
        n2 = random.randint(1, d2 - 1)
        v1, v2 = x // den * num, y // d2 * n2
        if v1 == v2:
            return t_of()
        return _tb("Which is larger: %d/%d of %d or %d/%d of %d? Type its value." % (num, den, x, n2, d2, y),
                   max(v1, v2), "int", {}, ["%d/%d of %d = %d; %d/%d of %d = %d." % (num, den, x, v1, n2, d2, y, v2)])

    def t_spent():
        who = _who()
        return _tb("%s had £%d and spent %d/%d of it on a game. How much money is left, in pounds?" % (who, x, num, den),
                   x - x // den * num, "int", {"unit": "£"},
                   ["%d/%d of %d = %d." % (num, den, x, x // den * num), "%d − %d = %d." % (x, x // den * num, x - x // den * num)])

    def t_bar():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [den * random.randint(2, 12) for _ in cats]
        k = random.randrange(4)
        return _bar("The chart shows how many cakes a bakery made each day. %d/%d of %s's cakes were chocolate. How many "
                    "chocolate cakes were made on %s?" % (num, den, cats[k], cats[k]), cats, vals, vals[k] // den * num,
                    ["%d ÷ %d × %d = %d." % (vals[k], den, num, vals[k] // den * num)])

    return _pick_t([t_of, t_money, t_inverse, t_remaining, t_measure, t_compare, t_spent], [t_strip, t_bar])


@skill("Y5.5.j", "Fractions greater than 1 on a number line", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 4], [3, 4, 5], [4, 6, 8]))
    w = random.randint(1, 3)
    r = random.randint(1, den - 1)
    M = w + Fraction(r, den)

    def t_place_mixed():
        return _nld("Place %s on the number line." % _mixed(M), M, 0, 4, Fraction(1, den), 1,
                    ["Go to %d, then %d more step%s of 1/%d." % (w, r, "" if r == 1 else "s", den)])

    def t_place_improper():
        n = w * den + r
        return _nld("Place %d/%d on the number line." % (n, den), M, 0, 4, Fraction(1, den), 1,
                    ["%d/%d = %s." % (n, den, _mixed(M))])

    def t_read():
        k = pick([x for x in range(den + 1, 3 * den) if Fraction(x % den, den).denominator == den])
        return _wq("A number line from 0 to 3 has each whole split into %d equal steps. A point is "
                   "%d steps from 0. Write its value as a mixed number." % (den, k),
                   _mixed(Fraction(k, den)) if Fraction(k, den).denominator == den else
                   "%d %d/%d" % (k // den, k % den, den),
                   ["%d steps of 1/%d = %d/%d." % (k, den, k, den)], "e.g. 1 3/4")

    def t_between():
        return _wq("Which two whole numbers does %d/%d lie between? Write them like 2 and 3."
                   % (w * den + r, den), "%d and %d" % (w, w + 1),
                   ["%d/%d = %s." % (w * den + r, den, _mixed(M))], "e.g. 2 and 3")

    def t_steps():
        return _tb("On a number line marked in steps of 1/%d, how many steps is it from 0 to %s?" % (den, _mixed(M)),
                   w * den + r, "int", {}, ["%s = %d/%d, so %d steps." % (_mixed(M), w * den + r, den, w * den + r)])

    def t_improper_read():
        k = w * den + r
        return _fq("A point on a number line is %d steps of 1/%d from 0. Write its value as an improper fraction."
                   % (k, den), Fraction(k, den), ["%d steps of 1/%d = %d/%d." % (k, den, k, den)], "e.g. 7/4")

    def t_halfway():
        a_ = w
        b_ = w + 1
        return _nld("Mark the point exactly halfway between %d and %d." % (a_, b_), Fraction(2 * w + 1, 2), 0, 4,
                    Fraction(1, 4), 1, ["Halfway is %d 1/2." % w])

    def t_further():
        other = Fraction(w * den + r + pick([-2, -1, 1, 2]), den)
        if other <= 0 or other == M:
            other = M + 1
        return _fq("Which is further from 0 on a number line, %s or %s? Type it." % (_mixed(M), _fs(other)),
                   max(M, other), ["%s = %s, so %s is further from 0." % (_fs(max(M, other)), _mixed(max(M, other)),
                                                                          _mixed(max(M, other)))], "e.g. 2 1/4")

    def t_jump():
        k = random.choice([v for v in range(2, den + 3) if v % den])
        start = M
        end = start + Fraction(k, den)
        if end > 4:
            return t_place_mixed()
        return _nld("Start at %s and jump on %d/%d. Mark where you land." % (_mixed(start), k, den), end, 0, 4,
                    Fraction(1, den), 1, ["%s + %d/%d = %s." % (_mixed(start), k, den, _mixed(end))])

    def t_nearer():
        if 2 * r == den:
            return t_between()
        near = w if 2 * r < den else w + 1
        return _tb("Is %s nearer to %d or to %d on a number line? Type the whole number it is nearer to."
                   % (_mixed(M), w, w + 1), near, "int", {},
                   ["%d/%d is %s than a half." % (r, den, "less" if 2 * r < den else "more")])

    def t_to_next():
        return _fq("How far is it from %s to the next whole number on a number line? (a fraction)" % _mixed(M),
                   Fraction(den - r, den), ["%s + %d/%d = %d." % (_mixed(M), den - r, den, w + 1)], "e.g. 1/4")

    def t_order():
        a_ = Fraction(w * den + r, den)
        b_ = a_ + Fraction(pick([v for v in (1, 2, 3) if v < den]), den)
        c_ = a_ + 1
        vals = [a_, b_, c_]
        shown = [_fs(a_), _mixed(b_), _fs(c_)]
        order = sorted(zip(vals, shown))
        k = random.randint(0, 2)
        ask = ["is nearest to 0", "lies between the other two", "is furthest from 0"][k]
        return _fq("These numbers are marked on a number line: %s. Which one %s? (type it)" % (", ".join(shown), ask),
                   order[k][0], ["In order: %s." % ", ".join(s_ for _, s_ in order)], "e.g. 2 1/4")

    def t_back():
        k = random.choice([v for v in range(1, den + 2) if v % den])
        end = M - Fraction(k, den)
        return _nld("Start at %s and count back %d/%d. Mark where you land." % (_mixed(M), k, den), end, 0, 4,
                    Fraction(1, den), 1, ["%s − %d/%d = %s." % (_mixed(M), k, den, _mixed(end))])

    return _pick_t([t_read, t_between, t_steps, t_improper_read, t_further, t_nearer, t_to_next, t_order],
                   [t_place_mixed, t_place_improper, t_halfway, t_jump, t_back])
