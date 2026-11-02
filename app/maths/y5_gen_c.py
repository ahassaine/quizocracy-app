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
    a, b = random.randint(2, 9), random.randint(2, 12)

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
        n = random.randint(12, _by(d, 39, 99, 199))
        m = random.randint(3, 9)
        t, o = (n // 10) * 10, n % 10
        return _tb("Work out %d × %d by partitioning %d into %d and %d." % (n, m, n, t, o), n * m, "int",
                   {}, ["%d × %d = %d and %d × %d = %d." % (t, m, t * m, o, m, o * m),
                        "%d + %d = %d." % (t * m, o * m, n * m)])

    def t_near():
        m = random.randint(3, 9)
        n = pick([19, 29, 39, 49, 99, 199])
        return _tb("Work out %d × %d. Hint: work out %d × %d and subtract %d." % (n, m, n + 1, m, m),
                   n * m, "int", {}, ["%d × %d = %d." % (n + 1, m, (n + 1) * m),
                                      "%d − %d = %d." % ((n + 1) * m, m, n * m)])

    def t_by5():
        n = random.randint(12, 98) * 2
        return _tb("Work out %d × 5. Hint: × 10 then halve." % n, n * 5, "int", {},
                   ["%d × 10 = %d; half of that is %d." % (n, n * 10, n * 5)])

    def t_three():
        x, y, z = random.randint(2, 9), pick([5, 25, 20]), random.randint(2, 8)
        return _tb("Work out %d × %d × %d. Choose an easy order." % (x, y, z), x * y * z, "int", {},
                   ["Multiply in any order: %d." % (x * y * z)])

    def t_fact_family():
        p = a * b
        return _tb("%d × %d = %d. Use this to work out %d × %d." % (a, b, p, a * 30, b), a * 30 * b,
                   "int", {}, ["%d × %d is 30 times %d × %d." % (a * 30, b, a, b),
                               "%d × 30 = %d." % (p, p * 30)])

    return _pick_t([t_tens, t_double, t_partition, t_near, t_by5, t_three, t_fact_family])


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
        nums = random.sample(range(1000, 9999), 4)
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
    m = random.randint(_by(d, 11, 12, 21), _by(d, 19, 39, 99))

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
    a, b = random.randint(2, 12), random.randint(2, 9)

    def t_tens():
        k = pick([10, 100, 1000][: _by(d, 2, 3, 3)])
        return _tb("Work out %s ÷ %d." % (_c(a * b * k), b), a * k, "int", {},
                   ["%d ÷ %d = %d, so %s ÷ %d = %s." % (a * b, b, a, _c(a * b * k), b, _c(a * k))])

    def t_by_tens():
        k = pick([10, 100])
        return _tb("Work out %s ÷ %s." % (_c(a * b * k * 10), _c(b * k)), a * 10, "int", {},
                   ["Divide both by %s: %s ÷ %d = %d." % (_c(k), _c(a * b * 10), b, a * 10)])

    def t_halve():
        n = random.randint(11, 99) * 4
        return _tb("Work out %d ÷ 4 by halving twice." % n, n // 4, "int", {},
                   ["Half of %d is %d; half again is %d." % (n, n // 2, n // 4)])

    def t_partition():
        m = random.randint(3, 8)
        q = random.randint(12, 39)
        n = q * m
        t = (q // 10) * 10 * m
        return _tb("Work out %d ÷ %d by splitting %d into %d and %d." % (n, m, n, t, n - t), q, "int", {},
                   ["%d ÷ %d = %d and %d ÷ %d = %d." % (t, m, t // m, n - t, m, (n - t) // m),
                    "%d + %d = %d." % (t // m, (n - t) // m, q)])

    def t_inverse():
        return _tb("___ × %d = %s. What is the missing number?" % (b, _c(a * b * 100)), a * 100, "int",
                   {}, ["%s ÷ %d = %s." % (_c(a * b * 100), b, _c(a * 100))])

    def t_by5():
        n = random.randint(11, 99) * 10
        return _tb("Work out %d ÷ 5. Hint: ÷ 10 then double." % n, n // 5, "int", {},
                   ["%d ÷ 10 = %d; double is %d." % (n, n // 10, n // 5)])

    return _pick_t([t_tens, t_by_tens, t_halve, t_partition, t_inverse, t_by5])


@skill("Y5.4.e", "Short division of up to 4 digits by a 1-digit number", S4)
def _(d=1):
    d = _d(d)
    m = random.randint(_by(d, 2, 3, 6), _by(d, 5, 9, 9))
    q = random.randint(_by(d, 21, 101, 201), _by(d, 199, 999, 1666))
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

    return _pick_t([t_round_up, t_round_down, t_left, t_money, t_shelves, t_which])


@skill("Y5.4.g", "Multiply and divide whole numbers by 10, 100 and 1000", S4)
def _(d=1):
    d = _d(d)
    k = pick([10, 100, 1000])
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
        x = random.randint(2, 90)
        return _tb("How many %s are in %d %s?" % (unit, x, big), x * f, "int", {"unit": unit},
                   ["1 %s = %d %s, so × %d." % (big, f, unit, f)])

    def t_table():
        nums = random.sample(range(2, 500), 3)
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
        m = Decimal(random.randint(1, 999))
        return _tb("Work out %s ÷ %s." % (_ds(m), _c(k)), _ds(m / k), "num", {},
                   ["Digits move %d place%s to the right: %s." % (len(str(k)) - 1, "" if k == 10 else "s",
                                                                  _ds(m / k))])

    def t_missing():
        return _tb("%s × ___ = %s. Is the missing number 10, 100 or 1000?" % (_ds(n), _ds(n * k)), k,
                   "int", {}, ["The digits moved %d place%s." % (len(str(k)) - 1, "" if k == 10 else "s")])

    def t_money():
        p = Decimal(random.randint(101, 999)) / 100
        q = pick([10, 100])
        return _tb("One pen costs £%s. How much do %d pens cost, in pounds?" % (format(p, ".2f"), q),
                   _ds(p * q), "num", {"unit": "£"}, ["£%s × %d = £%s." % (format(p, ".2f"), q, _ds(p * q))])

    def t_measure():
        x = Decimal(random.randint(11, 999)) / 10
        unit, big, f = pick([("m", "km", 1000), ("cm", "m", 100), ("kg", "g", 1000)])
        if unit == "kg":
            return _tb("Convert %s kg to grams." % _ds(x), _ds(x * 1000), "num", {"unit": "g"},
                       ["× 1000: %s g." % _ds(x * 1000)])
        return _tb("Convert %s %s to %s." % (_ds(x), unit, big), _ds(x / f), "num", {"unit": big},
                   ["÷ %d: %s %s." % (f, _ds(x / f), big)])

    def t_table():
        nums = [Decimal(random.randint(1, 999)) / 10 for _ in range(3)]
        rows = [[_ds(x), _ds(x * 10), _ds(x * 100), _ds(x * 1000)] for x in nums]
        r, c = random.randrange(3), random.randint(1, 3)
        ans = nums[r] * [10, 100, 1000][c - 1]
        return _dt("Complete the table. What belongs in the empty cell?", ["Number", "× 10", "× 100",
                                                                           "× 1000"],
                   rows, _ds(ans), ["%s × %s = %s." % (_ds(nums[r]), _c([10, 100, 1000][c - 1]), _ds(ans))],
                   missing=[r, c], atype="num")

    return _pick_t([t_mult, t_div, t_missing, t_money, t_measure], [t_table])


@skill("Y5.4.i", "Scaling problems, including by simple fractions", S4)
def _(d=1):
    d = _d(d)

    def t_times():
        a, k = random.randint(12, 250), random.randint(2, 9)
        return _tb("A tree is %d cm tall. A building is %d times as tall. How tall is the building, in "
                   "cm?" % (a, k), a * k, "int", {"unit": "cm"}, ["%d × %d = %d." % (a, k, a * k)])

    def t_recipe():
        per, k = random.randint(50, 250), random.randint(2, 6)
        return _tb("A recipe for 4 people uses %d g of flour. How much flour is needed for %d people, "
                   "in grams?" % (per, 4 * k), per * k, "int", {"unit": "g"},
                   ["%d people is %d times as many." % (4 * k, k), "%d × %d = %d." % (per, k, per * k)])

    def t_fraction_scale():
        den = pick([2, 3, 4, 5])
        x = den * random.randint(4, 30)
        return _tb("A model car is 1/%d of the length of a toy bus that is %d cm long. How long is the "
                   "car, in cm?" % (den, x), x // den, "int", {"unit": "cm"},
                   ["1/%d of %d = %d ÷ %d = %d." % (den, x, x, den, x // den)])

    def t_nonunit():
        den = pick([3, 4, 5, 8])
        num = random.randint(2, den - 1)
        x = den * random.randint(5, 25)
        return _tb("A ribbon is %d cm long. %s uses %d/%d of it. How many cm is that?"
                   % (x, _who(), num, den), x // den * num, "int", {"unit": "cm"},
                   ["1/%d of %d = %d." % (den, x, x // den), "× %d = %d." % (num, x // den * num)])

    def t_correspond():
        a, b = random.randint(3, 6), random.randint(2, 5)
        return _tb("A café offers %d kinds of sandwich and %d kinds of drink. A meal deal is one "
                   "sandwich and one drink. How many different meal deals are there?" % (a, b), a * b,
                   "int", {}, ["Each sandwich goes with %d drinks: %d × %d = %d." % (b, a, b, a * b)])

    def t_inverse():
        a, k = random.randint(12, 90), random.randint(3, 8)
        return _tb("A giraffe is %d times as heavy as a pony. The giraffe weighs %d kg. How heavy is "
                   "the pony, in kg?" % (k, a * k * 10), a * 10, "int", {"unit": "kg"},
                   ["%d ÷ %d = %d." % (a * k * 10, k, a * 10)])

    def t_bar():
        a, k = random.randint(5, 60), random.randint(2, 6)
        return _strip("%s has %d stickers. %s has %d times as many. How many stickers does %s have?"
                      % ("Leo", a, "Maya", k, "Maya"),
                      {"mode": "equal_parts", "parts": k, "partLabel": str(a), "totalLabel": "?",
                       "unknown": "total"}, a * k, ["%d × %d = %d." % (a, k, a * k)])

    return _pick_t([t_times, t_recipe, t_fraction_scale, t_nonunit, t_correspond, t_inverse], [t_bar])


@skill("Y5.4.j", "Simple rates", S4)
def _(d=1):
    d = _d(d)

    def t_per_item():
        n, p = random.randint(3, 12), random.randint(15, 95)
        return _tb("%d apples cost %dp altogether. How much does one apple cost, in pence?" % (n, n * p),
                   p, "int", {"unit": "p"}, ["%d ÷ %d = %d." % (n * p, n, p)])

    def t_per_hour():
        rate, h = random.randint(5, 15), random.randint(2, 8)
        return _tb("A babysitter earns £%d an hour. How much is earned in %d hours, in pounds?"
                   % (rate, h), rate * h, "int", {"unit": "£"}, ["%d × %d = %d." % (rate, h, rate * h)])

    def t_speed():
        sp, h = pick([30, 40, 50, 60, 70]), random.randint(2, 5)
        return _tb("A coach travels at a steady %d km every hour. How far does it go in %d hours, in km?"
                   % (sp, h), sp * h, "int", {"unit": "km"}, ["%d × %d = %d." % (sp, h, sp * h)])

    def t_per_minute():
        r, m = random.randint(3, 12), random.randint(4, 15)
        return _tb("A tap fills a bath at %d litres per minute. How many litres after %d minutes?"
                   % (r, m), r * m, "int", {"unit": "litres"}, ["%d × %d = %d." % (r, m, r * m)])

    def t_time_needed():
        r, m = random.randint(3, 12), random.randint(4, 15)
        return _tb("A printer prints %d pages a minute. How many minutes does it take to print %d "
                   "pages?" % (r, r * m), m, "int", {"unit": "minutes"}, ["%d ÷ %d = %d." % (r * m, r, m)])

    def t_best():
        a_n, b_n = random.randint(2, 5), random.randint(6, 10)
        a_p = a_n * random.randint(20, 40)
        b_p = b_n * random.randint(20, 40)
        if a_p / a_n == b_p / b_n:
            b_p += b_n
        cheaper = "A" if a_p / a_n < b_p / b_n else "B"
        return _wq("Pack A: %d yoghurts for %dp. Pack B: %d yoghurts for %dp. Which pack is cheaper per "
                   "yoghurt? (A or B)" % (a_n, a_p, b_n, b_p), cheaper,
                   ["A: %dp each. B: %dp each." % (a_p // a_n, b_p // b_n)], "A or B")

    def t_table():
        r = random.randint(4, 12)
        rows = [[h, h * r] for h in (1, 2, 3, 5, 8)]
        k = random.randint(1, 4)
        return _io("A machine makes %d toys an hour. The table shows hours and toys. What goes in the "
                   "empty cell?" % r, rows, k, rows[k][1], ["%d × %d = %d." % (rows[k][0], r, rows[k][1])])

    return _pick_t([t_per_item, t_per_hour, t_speed, t_per_minute, t_time_needed, t_best], [t_table])


@skill("Y5.4.k", "Problems using all four operations", S4)
def _(d=1):
    d = _d(d)

    def t_shop():
        a, pa, b, pb = random.randint(2, 6), random.randint(30, 95), random.randint(2, 6), random.randint(30, 95)
        pay = ((a * pa + b * pb) // 100 + 1) * 100 + pick([0, 500])
        return _tb("%s buys %d pens at %dp each and %d rulers at %dp each, and pays with £%d. How much "
                   "change is given, in pence?" % (_who(), a, pa, b, pb, pay // 100),
                   pay - a * pa - b * pb, "int", {"unit": "p"},
                   ["Cost: %d + %d = %d p." % (a * pa, b * pb, a * pa + b * pb),
                    "%d − %d = %d." % (pay, a * pa + b * pb, pay - a * pa - b * pb)])

    def t_share_after():
        total, spent, k = random.randint(200, 900), random.randint(20, 150), random.randint(2, 6)
        rest = total - spent
        rest -= rest % k
        total = rest + spent
        return _tb("A class has £%d. It spends £%d on a trip and shares the rest equally between %d "
                   "charities. How much does each charity get, in pounds?" % (total, spent, k), rest // k,
                   "int", {"unit": "£"}, ["%d − %d = %d." % (total, spent, rest),
                                          "%d ÷ %d = %d." % (rest, k, rest // k)])

    def t_rows_plus():
        r, c, extra = random.randint(6, 15), random.randint(8, 20), random.randint(5, 30)
        return _tb("A hall has %d rows of %d chairs and %d extra chairs at the side. How many chairs "
                   "altogether?" % (r, c, extra), r * c + extra, "int", {"unit": "chairs"},
                   ["%d × %d = %d." % (r, c, r * c), "%d + %d = %d." % (r * c, extra, r * c + extra)])

    def t_order():
        a, b, c = random.randint(2, 20), random.randint(2, 9), random.randint(2, 9)
        return _tb("Work out %d + %d × %d. (Multiply before adding.)" % (a, b, c), a + b * c, "int", {},
                   ["%d × %d = %d first." % (b, c, b * c), "%d + %d = %d." % (a, b * c, a + b * c)])

    def t_brackets():
        a, b, c = random.randint(2, 20), random.randint(2, 20), random.randint(2, 9)
        return _tb("Work out (%d + %d) × %d." % (a, b, c), (a + b) * c, "int", {},
                   ["Brackets first: %d." % (a + b), "%d × %d = %d." % (a + b, c, (a + b) * c)])

    def t_two_step_div():
        k, per = random.randint(2, 6), random.randint(6, 12)
        packs = k * random.randint(1, 3)
        return _tb("A teacher has %d boxes of %d crayons. The crayons are shared equally between %d "
                   "tables. How many crayons does each table get?" % (packs, per, k), packs * per // k,
                   "int", {}, ["%d × %d = %d." % (packs, per, packs * per),
                               "%d ÷ %d = %d." % (packs * per, k, packs * per // k)])

    def t_bar():
        cats = ["Mon", "Tue", "Wed", "Thu"]
        vals = [random.randint(4, 20) for _ in cats]
        price = pick([2, 3, 4, 5])
        i = random.randrange(4)
        return _bar("The chart shows how many cakes were sold each day. Cakes cost £%d each. How much "
                    "money was taken over all four days, in pounds?" % price, cats, vals,
                    sum(vals) * price, ["%d cakes in total." % sum(vals),
                                        "%d × %d = %d." % (sum(vals), price, sum(vals) * price)])

    return _pick_t([t_shop, t_share_after, t_rows_plus, t_order, t_brackets, t_two_step_div], [t_bar])


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
                   ["%d tenths = %d hundredths." % (t, t * 10)])

    def t_hundredths():
        t = random.randint(1, 9) * 10
        return _tb("Complete:  %d/100 = ___/10" % t, t // 10, "int", {},
                   ["%d hundredths = %d tenths." % (t, t // 10)])

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

    return _pick_t([t_numerator, t_denominator, t_simplify, t_tenths, t_hundredths, t_odd_one],
                   [t_area, t_hundred_grid])


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

    return _pick_t([t_larger, t_symbol, t_order, t_largest, t_half], [t_line])


@skill("Y5.5.c", "Mixed numbers and improper fractions", S5)
def _(d=1):
    d = _d(d)
    den = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 6, 8], [6, 7, 8, 9, 12]))
    w = random.randint(1, _by(d, 3, 5, 9))
    r = random.randint(1, den - 1)
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
        return _wq("Work out %d/%d + %d/%d and write the answer as a mixed number." % (x, den, y, den),
                   "%d %d/%d" % ((x + y) // den, (x + y) % den, den),
                   ["%d/%d + %d/%d = %d/%d." % (x, den, y, den, x + y, den),
                    "= %d %d/%d." % ((x + y) // den, (x + y) % den, den)], "e.g. 1 1/4")

    def t_line():
        return _nld("Place %d/%d on the number line." % (imp, den), Fraction(imp, den), 0, w + 2,
                    Fraction(1, den), 1, ["%d/%d = %d %d/%d." % (imp, den, w, r, den)])

    return _pick_t([t_to_improper, t_to_mixed, t_wholes, t_is_improper, t_sum_over], [t_line])


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

    return _pick_t([t_plain, t_mixed_answer, t_same, t_word, t_missing], [t_bar])


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
        return _wq("Work out %d − %d/%d. Write the answer as a mixed number." % (w + 1, x, big),
                   _mixed(Fraction(w + 1) - Fraction(x, big)),
                   ["%d − %d/%d = %s." % (w + 1, x, big, _mixed(Fraction(w + 1) - Fraction(x, big)))],
                   "e.g. 1 3/4")

    def t_word():
        if b is None:
            return t_from_one()
        return _fq("A jug is %d/%d full. %s pours out %d/%d of a jug. How full is the jug now?"
                   % (a, base, _who(), b, big), fa - Fraction(b, big),
                   ["%d/%d − %d/%d = %d/%d." % (a * m, big, b, big, a * m - b, big)])

    def t_how_much_more():
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
                    Fraction(1, 2), ["%d/%d − %d/%d = %d/%d." % (x, big, y, big, x - y, big)])

    return _pick_t([t_plain, t_from_one, t_from_mixed, t_word, t_how_much_more], [t_line])


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
        return _wq("Work out %d + %d %d/%d." % (w, w1, a, den), _mixed(w + A),
                   ["Add the wholes: %d." % (w + w1)], "e.g. 5 2/3")

    def t_word():
        return _wq("A plank is %s m long. Another is %s m long. How long are they end to end, in m? "
                   "(mixed number, simplest form)" % (_mixed(A), _mixed(B)), _mixed(A + B),
                   ["%s + %s = %s." % (_mixed(A), _mixed(B), _mixed(A + B))], "e.g. 4 1/2")

    def t_line():
        return _nld("Start at %s and count on %d/%d. Mark where you land." % (_mixed(A), b, den),
                    A + Fraction(b, den), w1 - 1 if w1 > 1 else 0, w1 + 3, Fraction(1, den), 1,
                    ["%s + %d/%d = %s." % (_mixed(A), b, den, _mixed(A + Fraction(b, den)))])

    return _pick_t([t_add, t_sub, t_whole_plus, t_word], [t_line])


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

    return _pick_t([t_plain, t_mixed_answer, t_repeated, t_numerator, t_word], [t_area])


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

    return _pick_t([t_plain, t_improper, t_word, t_whole_part])


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
                      x // den * num, ["One part is %d." % (x // den), "%d parts: %d." % (num, x // den * num)])

    return _pick_t([t_of, t_money, t_inverse, t_remaining, t_measure], [t_strip])


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

    return _pick_t([t_read, t_between], [t_place_mixed, t_place_improper])
