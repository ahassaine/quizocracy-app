# Year 2 generators (National Curriculum, Year 2 programme of study).
#
# Place value to 100, counting in 2s/3s/5s/10s, <, > and =; addition and subtraction facts to 20 and
# related facts to 100, two-digit calculations, commutativity and inverses; the 2, 5 and 10 tables,
# odd and even, × and ÷ statements; 1/3, 1/4, 2/4, 3/4; standard units, scales, money and change,
# time to five minutes; properties of 2-D and 3-D shapes, patterns and turns; pictograms, tally
# charts, block diagrams and tables.  Short prompts for young readers.
from .maths_engine import skill, n_words
from .y5_common import *  # noqa: F401,F403

S0 = "2.0 Number & place value"
S1 = "2.1 Addition & subtraction"
S2 = "2.2 Multiplication & division"
S3 = "2.3 Fractions"
S4 = "2.4 Measurement & money"
S5 = "2.5 Time"
S6 = "2.6 Shape, position & direction"
S7 = "2.7 Statistics"

KIDS = ["Sam", "Mia", "Ben", "Ava", "Leo", "Isla", "Jay", "Zoe"]


def _kid():
    return pick(KIDS)


# ================================================================== 2.0 ======
@skill("Y2.0.a", "Count in 2s, 3s, 5s and 10s", S0)
def _(d=1):
    d = _d(d)
    step = pick([2, 3, 5, 10])
    k = random.randint(2, 8)

    def t_next():
        s = [step * i for i in range(k, k + 3)]
        return _tb("Count in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] + step, "int", {}, ["Add %d." % step])

    def t_back():
        s = [step * i for i in range(k + 3, k, -1)]
        return _tb("Count back in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] - step, "int", {}, ["Take away %d." % step])

    def t_tens_any():
        start = random.randint(1, 9) + 10 * random.randint(0, 3)
        s = [start + 10 * i for i in range(4)]
        return _tb("Count on in 10s:  %s, ___" % ", ".join(map(str, s)), s[-1] + 10, "int", {}, ["The ones digit stays the same."])

    def t_missing():
        s = [step * i for i in range(1, 7)]
        j = random.randint(1, 4)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == j else str(v) for i, v in enumerate(s)), s[j], "int",
                   {}, ["Count in %ss." % step])

    def t_line():
        return _nl("Start at 0 and make %d jumps of %d. Where do you land?" % (k, step), k * step, step, 10,
                   ["%d jumps of %d = %d." % (k, step, k * step)], lo=0, hi=max(30, (k * step // 10 + 1) * 10))

    return _pick_t([t_next, t_back, t_tens_any, t_missing], [t_line])


@skill("Y2.0.b", "Tens and ones in two-digit numbers", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(11, 99)

    def t_value():
        return _tb("In %d, what is the tens digit worth?" % n, (n // 10) * 10, "int", {},
                   ["%d = %d + %d." % (n, (n // 10) * 10, n % 10)])

    def t_partition():
        return _tb("%d = %d + ___" % (n, (n // 10) * 10), n % 10, "int", {}, ["%d tens and %d ones." % (n // 10, n % 10)])

    def t_parts():
        return _tb("%d + %d = ___" % ((n // 10) * 10, n % 10), n, "int", {}, ["Tens and ones: %d." % n])

    def t_build():
        return {"prompt": "Make %d with tens and ones." % n, "component": "base_ten", "spec": {"mode": "build", "max": 9},
                "answer": n, "answer_type": "int", "solution": ["%d tens and %d ones." % (n // 10, n % 10)]}

    def t_other_way():
        t = n // 10
        if t < 2:
            return t_partition()
        return _tb("%d is %d tens and %d ones. It is also %d tens and how many ones?" % (n, t, n % 10, t - 1), n % 10 + 10, "int",
                   {}, ["Swap one ten for 10 ones: %d ones." % (n % 10 + 10)])

    return _pick_t([t_value, t_partition, t_parts, t_other_way], [t_build])


@skill("Y2.0.c", "Compare and order numbers to 100 with <, > and =", S0)
def _(d=1):
    d = _d(d)
    a, b = random.sample(range(1, 100), 2)

    def t_symbol():
        return _wq("Write < or > :  %d ___ %d" % (a, b), "<" if a < b else ">", ["%d is %s than %d." % (a, "less" if a < b else "more", b)],
                   "< or >")

    def t_equal():
        x, y = random.randint(10, 50), random.randint(10, 40)
        right = random.random() < 0.5
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (x, y, x + y if right else x + y + 1),
                   "yes" if right else "no", ["%d + %d = %d." % (x, y, x + y)], "yes / no")

    def t_order():
        vals = random.sample(range(1, 100), 4)
        k = random.randint(1, 4)
        return _tb("Put these in order, smallest first. Which is number %d in the list?  %s" % (k, ", ".join(map(str, vals))),
                   sorted(vals)[k - 1], "int", {}, ["In order: %s." % ", ".join(map(str, sorted(vals)))])

    def t_biggest():
        ds = random.sample(range(1, 10), 2)
        return _tb("Use the digits %d and %d to make the biggest two-digit number." % tuple(ds), max(ds) * 10 + min(ds), "int", {},
                   ["Put the bigger digit in the tens place."])

    def t_line():
        n = random.randint(0, 100)
        return _nl("Put %d on the number line." % n, n, 1, 10, ["Count from %d." % ((n // 10) * 10)], lo=0, hi=100)

    return _pick_t([t_symbol, t_equal, t_order, t_biggest], [t_line])


@skill("Y2.0.d", "Read and write numbers to 100 in numerals and words", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(11, 100)

    def t_to_num():
        return _tb("Write in digits: %s" % n_words(n), n, "int", {}, ["%s = %d." % (n_words(n), n)])

    def t_to_word():
        return _wq("Write %d in words." % n, n_words(n), ["%d = %s." % (n, n_words(n))], "words")

    def t_odd_even():
        k = random.randint(1, 99)
        return _wq("Is %d odd or even?" % k, "even" if k % 2 == 0 else "odd", ["Look at the ones digit: %d." % (k % 10)], "odd / even")

    def t_estimate():
        n2 = random.randint(10, 90)
        return _nl("Estimate where %d goes on a line from 0 to 100, and mark it." % n2, n2, 1, 10, ["About %d." % n2], lo=0, hi=100)

    return _pick_t([t_to_num, t_to_word, t_odd_even], [t_estimate])


# ================================================================== 2.1 ======
@skill("Y2.1.a", "Addition and subtraction facts to 20 and related facts to 100", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(_by(d, 1, 3, 5), _by(d, 6, 10, 10)), random.randint(_by(d, 1, 3, 5), _by(d, 6, 10, 10))

    def t_fact():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_sub_fact():
        return _tb("%d − %d = ___" % (a + b, b), a, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_tens():
        return _tb("%d + %d = ___" % (10 * a, 10 * b), 10 * (a + b), "int", {}, ["%d + %d = %d, so %d." % (a, b, a + b, 10 * (a + b))])

    def t_bond100():
        t = random.randint(1, 9) * 10
        return _tb("%d + ___ = 100" % t, 100 - t, "int", {}, ["%d + %d = 10, so %d + %d = 100." % (t // 10, 10 - t // 10, t, 100 - t)])

    def t_related():
        return _tb("%d + %d = %d. Use this to work out %d + %d." % (a, b, a + b, a, b + 10), a + b + 10, "int", {},
                   ["%d is 10 more than %d, so the answer is 10 more." % (b + 10, b)])

    return _pick_t([t_fact, t_sub_fact, t_tens, t_bond100, t_related])


@skill("Y2.1.b", "Add and subtract two-digit numbers and ones or tens", S1)
def _(d=1):
    d = _d(d)
    n = random.randint(11, 89)

    def t_add_ones():
        k = random.randint(1, 9)
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["Count on %d." % k])

    def t_sub_ones():
        k = random.randint(1, 9)
        return _tb("%d − %d = ___" % (n, k), n - k, "int", {}, ["Count back %d." % k])

    def t_add_tens():
        k = random.randint(1, (99 - n) // 10) * 10 if n < 90 else 10
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["The tens digit goes up; the ones stay the same."])

    def t_sub_tens():
        k = random.randint(1, n // 10) * 10
        return _tb("%d − %d = ___" % (n, k), n - k, "int", {}, ["The tens digit goes down; the ones stay the same."])

    def t_line():
        k = random.randint(2, 9)
        return _nl("Start at %d and jump on %d. Where do you land?" % (n, k), n + k, 1, 10, ["%d + %d = %d." % (n, k, n + k)],
                   lo=(n // 10) * 10, hi=(n // 10) * 10 + 20)

    return _pick_t([t_add_ones, t_sub_ones, t_add_tens, t_sub_tens], [t_line])


@skill("Y2.1.c", "Add and subtract two two-digit numbers; add three one-digit numbers", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(11, 60), random.randint(11, 39)

    def t_add():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["Add the tens, then the ones: %d." % (a + b)])

    def t_sub():
        x, y = max(a, b), min(a, b)
        return _tb("%d − %d = ___" % (x, y), x - y, "int", {}, ["%d − %d = %d." % (x, y, x - y)])

    def t_three():
        x, y, z = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        return _tb("%d + %d + %d = ___" % (x, y, z), x + y + z, "int", {}, ["Look for a pair that makes 10."])

    def t_blocks():
        s = a + b
        if s > 99:
            return t_add()
        return {"prompt": "Work out %d + %d and make the answer with the blocks." % (a, b), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": s, "answer_type": "int", "solution": ["%d." % s]}

    def t_word():
        kid = _kid()
        return _tb("%s read %d pages on Monday and %d pages on Tuesday. How many pages altogether?" % (kid, a, b), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)])

    return _pick_t([t_add, t_sub, t_three, t_word], [t_blocks])


@skill("Y2.1.d", "Any order for addition; inverse and missing numbers", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(5, 50), random.randint(5, 40)

    def t_commute():
        return _tb("%d + %d = %d. What is %d + %d?" % (a, b, a + b, b, a), a + b, "int", {}, ["You can add in any order."])

    def t_not_commute():
        return _wq("Is %d − %d the same as %d − %d? (yes or no)" % (a + b, b, b, a + b), "no",
                   ["Subtraction cannot be done in any order."], "yes / no")

    def t_missing_add():
        return _tb("%d + ___ = %d" % (a, a + b), b, "int", {}, ["%d − %d = %d." % (a + b, a, b)])

    def t_missing_sub():
        return _tb("___ − %d = %d" % (b, a), a + b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_check():
        return _tb("%d − %d = %d. Which addition checks this? Work out %d + %d." % (a + b, b, a, a, b), a + b, "int", {},
                   ["Adding back gives %d." % (a + b)])

    return _pick_t([t_commute, t_not_commute, t_missing_add, t_missing_sub, t_check])


@skill("Y2.1.e", "Addition and subtraction problems", S1)
def _(d=1):
    d = _d(d)
    kid = _kid()

    def t_change():
        cost, pay = random.randint(11, 90), pick([50, 100])
        if cost >= pay:
            pay = 100
        return _tb("%s buys a toy for %dp and pays with %dp. How much change?" % (kid, cost, pay), pay - cost, "int", {"unit": "p"},
                   ["%d − %d = %d." % (pay, cost, pay - cost)])

    def t_more():
        a, b = random.randint(10, 50), random.randint(5, 40)
        return _tb("%s has %d stickers. Ben has %d more than %s. How many does Ben have?" % (kid, a, b, kid), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)]) if kid != "Ben" else t_left()

    def t_left():
        a, b = random.randint(30, 90), random.randint(5, 25)
        return _tb("A class had %d pencils. %d were lost. How many are left?" % (a, b), a - b, "int", {}, ["%d − %d = %d." % (a, b, a - b)])

    def t_two_step():
        a, b, c = random.randint(20, 50), random.randint(5, 20), random.randint(5, 20)
        return _tb("There were %d people on a train. %d got off and %d got on. How many now?" % (a, b, c), a - b + c, "int", {},
                   ["%d − %d = %d; + %d = %d." % (a, b, a - b, c, a - b + c)])

    def t_bar():
        whole, part = random.randint(30, 90), random.randint(10, 25)
        return _strip("The bar shows %d altogether. One part is %d. What is the other part?" % (whole, part),
                      {"mode": "part_whole", "totalLabel": str(whole), "partLabel": str(part), "unknown": "part", "parts": 2},
                      whole - part, ["%d − %d = %d." % (whole, part, whole - part)])

    return _pick_t([t_change, t_more, t_left, t_two_step], [t_bar])


# ================================================================== 2.2 ======
@skill("Y2.2.a", "The 2, 5 and 10 times tables", S2)
def _(d=1):
    d = _d(d)
    t = pick([2, 5, 10])
    k = random.randint(1, 12)

    def t_mult():
        return _tb("%d × %d = ___" % (k, t), k * t, "int", {}, ["%d lots of %d." % (k, t)])

    def t_div():
        return _tb("%d ÷ %d = ___" % (k * t, t), k, "int", {}, ["How many %ss make %d? %d." % (t, k * t, k)])

    def t_missing():
        return _tb("___ × %d = %d" % (t, k * t), k, "int", {}, ["%d ÷ %d = %d." % (k * t, t, k)])

    def t_groups():
        g = random.randint(2, 6)
        return {"prompt": "There are %d groups of %d. Write the total." % (g, t), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": t}, "answer": g * t, "answer_type": "int",
                "solution": ["%d × %d = %d." % (g, t, g * t)]}

    def t_array():
        g = random.randint(2, 6)
        return {"prompt": "Build an array of %d rows of %d. How many altogether?" % (g, t), "component": "array",
                "spec": {"mode": "build", "maxRows": 10, "maxCols": 10, "targetRows": g, "targetCols": t}, "answer": g * t,
                "answer_type": "int", "solution": ["%d × %d = %d." % (g, t, g * t)]}

    return _pick_t([t_mult, t_div, t_missing], [t_groups, t_array])


@skill("Y2.2.b", "Odd and even numbers", S2)
def _(d=1):
    d = _d(d)

    def t_is():
        n = random.randint(1, 100)
        return _wq("Is %d odd or even?" % n, "even" if n % 2 == 0 else "odd", ["Even numbers end in 0, 2, 4, 6 or 8."], "odd / even")

    def t_next_even():
        n = random.randint(1, 98)
        nxt = n + 1 if n % 2 else n + 2
        return _tb("What is the next even number after %d?" % n, nxt, "int", {}, ["%d." % nxt])

    def t_count():
        lo = random.randint(1, 20)
        hi = lo + random.randint(5, 10)
        return _tb("How many odd numbers are there from %d to %d?" % (lo, hi), sum(1 for x in range(lo, hi + 1) if x % 2),
                   "int", {}, ["%s." % ", ".join(str(x) for x in range(lo, hi + 1) if x % 2)])

    def t_pairs():
        n = random.randint(4, 30)
        return _wq("Can %d socks be put into pairs with none left over? (yes or no)" % n, "yes" if n % 2 == 0 else "no",
                   ["%d is %s." % (n, "even" if n % 2 == 0 else "odd")], "yes / no")

    return _pick_t([t_is, t_next_even, t_count, t_pairs])


@skill("Y2.2.c", "Write and solve × and ÷ statements; any order for ×", S2)
def _(d=1):
    d = _d(d)
    a, b = pick([2, 5, 10]), random.randint(2, 10)

    def t_commute():
        return _tb("%d × %d = %d. What is %d × %d?" % (a, b, a * b, b, a), a * b, "int", {}, ["Multiplication can be done in any order."])

    def t_div_not():
        return _wq("Is %d ÷ %d the same as %d ÷ %d? (yes or no)" % (a * b, a, a, a * b), "no", ["Division cannot be done in any order."],
                   "yes / no")

    def t_repeated():
        return _tb("%s = ___" % " + ".join([str(a)] * b), a * b, "int", {}, ["%d lots of %d = %d × %d = %d." % (b, a, b, a, a * b)])

    def t_fact_family():
        return _tb("%d × %d = %d. So %d ÷ %d = ___" % (a, b, a * b, a * b, b), a, "int", {}, ["Division undoes multiplication."])

    def t_write():
        return _tb("What is %d groups of %d?" % (b, a), a * b, "int", {}, ["%d × %d = %d." % (b, a, a * b)])

    return _pick_t([t_commute, t_div_not, t_repeated, t_fact_family, t_write])


@skill("Y2.2.d", "Multiplication and division problems", S2)
def _(d=1):
    d = _d(d)
    t = pick([2, 5, 10])
    k = random.randint(2, 10)

    def t_bags():
        return _tb("There are %d bags with %d apples in each. How many apples?" % (k, t), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_share():
        return _tb("%d sweets are shared equally between %d children. How many each?" % (k * t, t), k, "int", {},
                   ["%d ÷ %d = %d." % (k * t, t, k)])

    def t_coins():
        return _tb("How much are %d %dp coins worth, in pence?" % (k, t), k * t, "int", {"unit": "p"}, ["%d × %d = %d." % (k, t, k * t)])

    def t_teams():
        return _tb("%d children make teams of %d. How many teams?" % (k * t, t), k, "int", {}, ["%d ÷ %d = %d." % (k * t, t, k)])

    def t_bar():
        return _strip("%d children each have %d stickers. How many stickers altogether?" % (k, t),
                      {"mode": "equal_parts", "parts": k, "partLabel": str(t), "totalLabel": "?", "unknown": "total"}, k * t,
                      ["%d × %d = %d." % (k, t, k * t)])

    return _pick_t([t_bags, t_share, t_coins, t_teams], [t_bar])


# ================================================================== 2.3 ======
@skill("Y2.3.a", "Find 1/3, 1/4, 2/4 and 3/4 of a shape", S3)
def _(d=1):
    d = _d(d)

    def t_shade():
        f = pick([(1, 3), (1, 4), (2, 4), (3, 4), (2, 3)])
        return {"prompt": "Shade %d/%d of the bar." % f, "component": "fraction_bar", "spec": {"parts": f[1], "mode": "shade"},
                "answer": "%d/%d" % f, "answer_type": "frac", "solution": ["Shade %d of the %d equal parts." % f]}

    def t_read():
        f = pick([(1, 3), (1, 4), (3, 4), (2, 3), (1, 2)])
        return _area("What fraction of the shape is shaded?", {"mode": "fraction_read", "parts": f[1], "shaded": f[0]},
                     "%d/%d" % f, ["%d out of %d equal parts." % f], atype="frac")

    def t_equiv():
        return _wq("Is 2/4 the same as 1/2? (yes or no)", "yes", ["2 quarters make a half."], "yes / no")

    def t_parts():
        n, name = pick([(3, "thirds"), (4, "quarters")])
        return _tb("How many %s make a whole?" % name, n, "int", {}, ["%d %s make 1 whole." % (n, name)])

    def t_left():
        f = pick([(1, 4), (3, 4), (1, 3)])
        return _wq("A cake is cut into %d equal pieces and %d %s eaten. What fraction is left? (like 1/4)" % (f[1], f[0],
                                                                                                              "is" if f[0] == 1 else "are"),
                   "%d/%d" % (f[1] - f[0], f[1]), ["%d out of %d pieces are left." % (f[1] - f[0], f[1])], "e.g. 1/4")

    return _pick_t([t_equiv, t_parts, t_left], [t_shade, t_read])


@skill("Y2.3.b", "Fractions of a set or quantity", S3)
def _(d=1):
    d = _d(d)

    def t_third():
        n = 3 * random.randint(1, 10)
        return _tb("What is 1/3 of %d?" % n, n // 3, "int", {}, ["Share %d into 3 equal groups: %d." % (n, n // 3)])

    def t_quarter():
        n = 4 * random.randint(1, 10)
        return _tb("What is 1/4 of %d?" % n, n // 4, "int", {}, ["Share %d into 4 equal groups: %d." % (n, n // 4)])

    def t_three_quarters():
        n = 4 * random.randint(1, 8)
        return _tb("What is 3/4 of %d?" % n, 3 * n // 4, "int", {}, ["1/4 of %d is %d, so 3/4 is %d." % (n, n // 4, 3 * n // 4)])

    def t_half_of():
        n = 2 * random.randint(2, 15)
        return _tb("1/2 of %d = ___" % n, n // 2, "int", {}, ["Half of %d is %d." % (n, n // 2)])

    def t_groups():
        k = random.randint(2, 6)
        g = pick([3, 4])
        return {"prompt": "%d counters are in %d equal groups. What is 1/%d of %d?" % (g * k, g, g, g * k), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": k}, "answer": k, "answer_type": "int",
                "solution": ["One group has %d." % k]}

    def t_length():
        n = 4 * random.randint(2, 6)
        return _tb("A ribbon is %d cm long. %s cuts off 1/4 of it. How long is the piece cut off, in cm?" % (n, _kid()), n // 4,
                   "int", {"unit": "cm"}, ["%d ÷ 4 = %d." % (n, n // 4)])

    return _pick_t([t_third, t_quarter, t_three_quarters, t_half_of, t_length], [t_groups])


# ================================================================== 2.4 ======
@skill("Y2.4.a", "Choose units and read scales", S4)
def _(d=1):
    d = _d(d)

    def t_unit():
        q, a = pick([("Would you measure the length of a pencil in cm or m?", "cm"),
                     ("Would you measure the height of a door in cm or m?", "m"),
                     ("Would you weigh a bag of potatoes in g or kg?", "kg"),
                     ("Would you weigh a sweet in g or kg?", "g"),
                     ("Would you measure a bath of water in ml or litres?", "litres"),
                     ("Would you measure a spoon of medicine in ml or litres?", "ml")])
        return _wq(q, a, ["Choose the unit that fits the size."], "unit")

    def t_ruler():
        cm = random.randint(3, 19)
        return {"prompt": "How long is it, in cm?", "component": "ruler", "spec": {"mode": "length", "value": cm, "max": 20, "unit": "cm"},
                "answer": cm, "answer_type": "num", "tolerance": 0.5, "solution": ["%d cm." % cm]}

    def t_scale():
        mx = pick([10, 20])
        v = random.randint(1, mx - 1)
        return {"prompt": "Read the scale. How many kg?", "component": "ruler", "spec": {"mode": "mass", "value": v, "max": mx, "unit": "kg"},
                "answer": v, "answer_type": "num", "tolerance": 0.5, "solution": ["%d kg." % v]}

    def t_jug():
        v = random.randint(1, 9) * 100
        return {"prompt": "How much water is in the jug, in ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"}, "answer": v, "answer_type": "num",
                "tolerance": 50, "solution": ["%d ml." % v]}

    def t_thermo():
        t = random.randint(-5, 30)
        t = random.randint(0, 30)
        return _tb("A thermometer shows %d °C. It gets 5 degrees warmer. What does it show now, in °C?" % t, t + 5, "int",
                   {"unit": "°C"}, ["%d + 5 = %d." % (t, t + 5)])

    def t_temp():
        a, b = random.sample(range(0, 35), 2)
        return _tb("Which is warmer, %d °C or %d °C? Type the number." % (a, b), max(a, b), "int", {}, ["%d is higher." % max(a, b)])

    return _pick_t([t_unit, t_temp, t_thermo], [t_ruler, t_scale, t_jug])


@skill("Y2.4.b", "Compare and order lengths, mass and capacity", S4)
def _(d=1):
    d = _d(d)

    def t_symbol():
        unit = pick(["cm", "kg", "ml", "m", "g", "litres"])
        a, b = random.sample(range(2, 99), 2)
        return _wq("Write < or > :  %d %s ___ %d %s" % (a, unit, b, unit), "<" if a < b else ">", ["Compare the numbers."], "< or >")

    def t_longest():
        names = ["red", "blue", "green"]
        v = random.sample(range(5, 60), 3)
        return _wq("Ribbons: red %d cm, blue %d cm, green %d cm. Which is the longest?" % tuple(v), names[v.index(max(v))],
                   ["%d cm is the longest." % max(v)], "colour")

    def t_order():
        v = random.sample(range(1, 40), 3)
        return _tb("Put these masses in order, lightest first. Which is in the middle?  %s" % ", ".join("%d kg" % x for x in v),
                   sorted(v)[1], "int", {"unit": "kg"}, ["Order: %s." % ", ".join("%d kg" % x for x in sorted(v))])

    def t_difference():
        a, b = random.sample(range(10, 90), 2)
        return _tb("A jug holds %d ml. A cup holds %d ml. How much more does the bigger one hold, in ml?" % (max(a, b), min(a, b)),
                   abs(a - b), "int", {"unit": "ml"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    return _pick_t([t_symbol, t_longest, t_order, t_difference])


@skill("Y2.4.c", "Money: £ and p, making amounts and giving change", S4)
def _(d=1):
    d = _d(d)

    def t_total():
        cs = random.sample([1, 2, 5, 10, 20, 50], _by(d, 2, 3, 4))
        return _tb("What is the total of %s, in pence?" % " + ".join("%dp" % c for c in cs), sum(cs), "int", {"unit": "p"},
                   ["%s = %dp." % (" + ".join(map(str, cs)), sum(cs))])

    def t_pounds():
        a, b = random.randint(1, 5), pick([10, 20, 50])
        return _tb("How many pence is £%d and %dp?" % (a, b), 100 * a + b, "int", {"unit": "p"}, ["£1 = 100p, so %dp." % (100 * a + b)])

    def t_make():
        target = pick([15, 25, 30, 35, 60, 70, 80])
        return _tb("What is the fewest coins you can use to make %dp?" % target,
                   _fewest(target), "int", {}, ["Use the biggest coins first."])

    def t_change():
        cost = random.randint(5, 95)
        pay = 100 if cost > 50 else pick([50, 100])
        return _tb("A comic costs %dp. You pay with %s. How much change, in pence?" % (cost, "£1" if pay == 100 else "50p"),
                   pay - cost, "int", {"unit": "p"}, ["%d − %d = %d." % (pay, cost, pay - cost)])

    def t_two_ways():
        return _wq("Do 20p + 20p + 10p and 50p make the same amount? (yes or no)", "yes", ["Both make 50p."], "yes / no")

    def t_shop():
        a, b = random.randint(10, 45), random.randint(10, 45)
        return _tb("A pencil costs %dp and a rubber costs %dp. How much for both, in pence?" % (a, b), a + b, "int", {"unit": "p"},
                   ["%d + %d = %d." % (a, b, a + b)])

    return _pick_t([t_total, t_pounds, t_make, t_change, t_two_ways, t_shop])


def _fewest(p):
    n = 0
    for c in (50, 20, 10, 5, 2, 1):
        n += p // c
        p %= c
    return n


# ================================================================== 2.5 ======
@skill("Y2.5.a", "Tell the time to five minutes", S5)
def _(d=1):
    d = _d(d)
    h = random.randint(1, 12)
    m = 5 * random.randint(0, 11)

    def t_set():
        return {"prompt": "Set the clock to %d:%02d." % (h, m), "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:%02d" % (h, m), "answer_type": "time", "solution": ["The long hand points to %d." % (m // 5 or 12)]}

    def t_quarter():
        kind = pick(["quarter past", "quarter to", "half past"])
        mm = {"quarter past": 15, "half past": 30, "quarter to": 45}[kind]
        hh = h if kind != "quarter to" else (h - 2) % 12 + 1
        return {"prompt": "Set the clock to %s %d." % (kind, h), "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:%02d" % (hh, mm), "answer_type": "time", "solution": ["%s %d is %d:%02d." % (kind.capitalize(), h, hh, mm)]}

    def t_words():
        mm = pick([5, 10, 20, 25])
        past = random.random() < 0.5
        hh = h if past else (h - 2) % 12 + 1
        mins = mm if past else 60 - mm
        return {"prompt": "Set the clock to %d minutes %s %d." % (mm, "past" if past else "to", h), "component": "clock",
                "spec": {"mode": "set"}, "answer": "%d:%02d" % (hh, mins), "answer_type": "time",
                "solution": ["%d minutes %s %d is %d:%02d." % (mm, "past" if past else "to", h, hh, mins)]}

    def t_long_hand():
        return _tb("The long hand points to %d. How many minutes past the hour is that?" % (m // 5 or 12), m if m else 0, "int", {},
                   ["Each number is 5 minutes: %d × 5 = %d." % (m // 5, m)])

    return _pick_t([t_long_hand], [t_set, t_quarter, t_words])


@skill("Y2.5.b", "Minutes, hours and comparing times", S5)
def _(d=1):
    d = _d(d)

    def t_facts():
        q, a = pick([("How many minutes are in an hour?", 60), ("How many hours are in a day?", 24),
                     ("How many minutes are in half an hour?", 30), ("How many minutes are in a quarter of an hour?", 15)])
        return _tb(q, a, "int", {}, ["%d." % a])

    def t_later():
        h = random.randint(1, 10)
        k = random.randint(1, 3)
        return _tb("It is %d o'clock. What time will it be in %d hour%s? Type the hour." % (h, k, "" if k == 1 else "s"),
                   (h + k - 1) % 12 + 1, "int", {}, ["Count on %d." % k])

    def t_compare():
        a, b = random.sample([10, 15, 20, 30, 45, 50], 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s read for %d minutes. %s read for %d minutes. Who read for longer?" % (kids[0], a, kids[1], b),
                   kids[0] if a > b else kids[1], ["%d minutes is longer." % max(a, b)], "name")

    def t_duration():
        start = random.randint(1, 10)
        k = random.randint(1, 2)
        return _tb("A film starts at %d o'clock and ends at %d o'clock. How many hours long is it?" % (start, start + k), k, "int", {},
                   ["%d − %d = %d." % (start + k, start, k)])

    def t_half_hour():
        h = random.randint(1, 11)
        return _tb("It is %d o'clock. How many minutes until half past %d?" % (h, h), 30, "int", {}, ["Half an hour is 30 minutes."])

    return _pick_t([t_facts, t_later, t_compare, t_duration, t_half_hour])


# ================================================================== 2.6 ======
@skill("Y2.6.a", "Properties of 2-D shapes", S6)
def _(d=1):
    d = _d(d)

    def t_sides():
        name = pick(["triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"])
        return {"prompt": "How many sides does this shape have?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": {"triangle": 3, "square": 4, "rectangle": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}[name],
                "answer_type": "int", "solution": ["Count the sides."]}

    def t_vertices():
        name = pick(["triangle", "square", "pentagon", "hexagon"])
        return {"prompt": "How many corners (vertices) does this shape have?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "vertices"},
                "answer": {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6}[name], "answer_type": "int",
                "solution": ["Count the corners."]}

    def t_name():
        n, name = pick([(3, "triangle"), (5, "pentagon"), (6, "hexagon"), (8, "octagon")])
        return _wq("Which shape has %d straight sides?" % n, name, ["%d sides: %s." % (n, name)], "shape name")

    def t_symmetry():
        q, a = pick([("Does a square have a vertical line of symmetry? (yes or no)", "yes"),
                     ("Does a circle have a vertical line of symmetry? (yes or no)", "yes"),
                     ("Does the capital letter A have a vertical line of symmetry? (yes or no)", "yes"),
                     ("Does the capital letter F have a vertical line of symmetry? (yes or no)", "no"),
                     ("Does the capital letter L have a vertical line of symmetry? (yes or no)", "no")])
        return _wq(q, a, ["Fold it down the middle: do both halves match?"], "yes / no")

    return _pick_t([t_name, t_symmetry], [t_sides, t_vertices])


@skill("Y2.6.b", "Properties of 3-D shapes", S6)
def _(d=1):
    d = _d(d)
    SOL = {"cube": (6, 12, 8), "cuboid": (6, 12, 8), "square-based pyramid": (5, 8, 5), "triangular prism": (5, 9, 6)}

    def t_count():
        name = pick(list(SOL))
        what, i = pick([("faces", 0), ("edges", 1), ("vertices", 2)])
        return {"prompt": "How many %s does this shape have?" % what, "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": what}, "answer": SOL[name][i], "answer_type": "int",
                "solution": ["A %s has %d %s." % (name, SOL[name][i], what)]}

    def t_face_shape():
        q, a = pick([("What 2-D shape is the flat face of a cylinder?", "circle"),
                     ("What 2-D shape are the faces of a cube?", "square"),
                     ("What 2-D shape are the sloping faces of a pyramid?", "triangle"),
                     ("What 2-D shape is the flat face of a cone?", "circle")])
        return _wq(q, a, ["Look at the flat faces."], "shape name")

    def t_roll():
        q, a = pick([("Can a sphere roll? (yes or no)", "yes"), ("Can a cube roll? (yes or no)", "no"),
                     ("Does a sphere have any flat faces? (yes or no)", "no")])
        return _wq(q, a, ["Curved surfaces roll."], "yes / no")

    def t_sort():
        shapes = random.sample(["cube", "sphere", "cylinder", "cone", "cuboid", "pyramid"], 4)
        curved = sum(1 for s in shapes if s in ("sphere", "cylinder", "cone"))
        return _tb("How many of these have a curved surface?  %s" % ", ".join(shapes), curved, "int", {},
                   ["Sphere, cylinder and cone have curved surfaces."])

    return _pick_t([t_face_shape, t_roll, t_sort], [t_count])


@skill("Y2.6.c", "Patterns, turns and direction", S6)
def _(d=1):
    d = _d(d)
    DIRS = ["north", "east", "south", "west"]

    def t_pattern():
        unit = random.sample(["circle", "square", "triangle", "star"], pick([2, 3]))
        k = random.randint(len(unit) * 2 + 1, 12)
        seq = [unit[i % len(unit)] for i in range(len(unit) * 2)]
        return _wq("The pattern goes: %s, ... What is shape number %d?" % (", ".join(seq), k), unit[(k - 1) % len(unit)],
                   ["The pattern repeats every %d shapes." % len(unit)], "shape")

    def t_turn():
        s = random.randrange(4)
        k = random.randint(1, 3)
        cw = random.random() < 0.5
        return _wq("You face %s and make %s turn %s. Which way do you face now?"
                   % (DIRS[s], {1: "a quarter", 2: "a half", 3: "a three-quarter"}[k], "clockwise" if cw else "anticlockwise"),
                   DIRS[(s + (k if cw else -k)) % 4], ["A quarter turn is one right angle."], "direction")

    def t_right_angles():
        k, name = pick([(1, "a quarter turn"), (2, "a half turn"), (3, "a three-quarter turn"), (4, "a whole turn")])
        return _tb("How many right angles are in %s?" % name, k, "int", {}, ["%s = %d right angle%s." % (name.capitalize(), k, "" if k == 1 else "s")])

    def t_turn_pic():
        deg, name = pick([(90, "quarter"), (180, "half"), (270, "three-quarter")])
        return {"prompt": "The arrow shows an anticlockwise turn. Is it a quarter, half or three-quarter turn?", "component": "angle",
                "spec": {"mode": "turn", "degrees": deg}, "answer": name, "answer_type": "str", "solution": ["%s turn." % name.capitalize()]}

    def t_grid():
        x, y = random.randint(1, 4), random.randint(1, 4)
        r, u = random.randint(1, 4), random.randint(1, 4)
        return {"prompt": "Start at the dot. Move %d square%s right and %d square%s up. Mark where you finish."
                          % (r, "" if r == 1 else "s", u, "" if u == 1 else "s"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord", "solution": ["%d right, %d up." % (r, u)]}

    return _pick_t([t_pattern, t_turn, t_right_angles], [t_turn_pic, t_grid])


# ================================================================== 2.7 ======
@skill("Y2.7.a", "Pictograms and tally charts", S7)
def _(d=1):
    d = _d(d)
    cats = random.sample(["Apples", "Bananas", "Grapes", "Pears", "Oranges"], 4)

    def t_pictogram():
        key = pick([1, 2, 5]) if d else 1
        vals = [key * random.randint(1, 6) for _ in cats]
        k = random.randrange(4)
        return {"prompt": "Each symbol stands for %d. How many %s?" % (key, cats[k].lower()), "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"}, "answer": vals[k], "answer_type": "int",
                "solution": ["%d symbols × %d = %d." % (vals[k] // key, key, vals[k])]}

    def t_tally():
        vals = [random.randint(2, 14) for _ in cats]
        rows = [[c, _tally(v), v] for c, v in zip(cats, vals)]
        k = random.randrange(4)
        return _dt("Read the tally chart. What number goes in the empty box?", ["Fruit", "Tally", "Total"], rows, vals[k],
                   ["Count in 5s for each bundle, then the extra ones: %d." % vals[k]], missing=[k, 2])

    def t_most():
        vals = random.sample(range(1, 10), 4)
        return {"prompt": "Which fruit was chosen most?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"}, "answer": cats[vals.index(max(vals))],
                "answer_type": "str", "solution": ["%s has the most symbols." % cats[vals.index(max(vals))]]}

    return _pick_t([], [t_pictogram, t_tally, t_most])


def _tally(v):
    return " ".join(["||||\\"] * (v // 5) + (["|" * (v % 5)] if v % 5 else []))


@skill("Y2.7.b", "Block diagrams and tables: totals and comparisons", S7)
def _(d=1):
    d = _d(d)
    cats = random.sample(["Red", "Blue", "Green", "Yellow"], 4)
    vals = [random.randint(1, 12) for _ in cats]

    def t_read():
        k = random.randrange(4)
        return _bar("The block diagram shows favourite colours. How many chose %s?" % cats[k], cats, vals, vals[k],
                    ["Read the top of the %s bar: %d." % (cats[k], vals[k])])

    def t_total():
        return _bar("The block diagram shows favourite colours. How many children altogether?", cats, vals, sum(vals),
                    ["%s = %d." % (" + ".join(map(str, vals)), sum(vals))])

    def t_more():
        i, j = random.sample(range(4), 2)
        if vals[i] == vals[j]:
            return t_total()
        return _bar("How many more chose %s than %s?" % (cats[i] if vals[i] > vals[j] else cats[j],
                                                        cats[j] if vals[i] > vals[j] else cats[i]), cats, vals,
                    abs(vals[i] - vals[j]), ["%d − %d = %d." % (max(vals[i], vals[j]), min(vals[i], vals[j]), abs(vals[i] - vals[j]))])

    def t_table():
        rows = [[c, v] for c, v in zip(cats, vals)]
        i, j = random.sample(range(4), 2)
        return _dt("The table shows votes. How many votes did %s and %s get altogether?" % (cats[i], cats[j]), ["Colour", "Votes"],
                   rows, vals[i] + vals[j], ["%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])])

    def t_least():
        if vals.count(min(vals)) > 1:
            return t_total()
        return _bar("Which colour was chosen the least?", cats, vals, cats[vals.index(min(vals))],
                    ["%s has the shortest bar." % cats[vals.index(min(vals))]], atype="str")

    return _pick_t([], [t_read, t_total, t_more, t_table, t_least])
