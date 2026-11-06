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


def _pn(k, one, many=None):
    """3 -> '3 dots', 1 -> '1 dot'."""
    return "%d %s" % (k, one if k == 1 else (many or one + "s"))


def _tn(t, o):
    """(4, 1) -> '4 tens and 1 one'."""
    return "%s and %s" % (_pn(t, "ten"), _pn(o, "one"))


def _a(word):
    """'octagon' -> 'an octagon'."""
    return ("an " if word[0] in "aeiou" else "a ") + word


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

    def t_back_tens():
        start = random.randint(1, 9) + 10 * random.randint(5, 9)
        s = [start - 10 * i for i in range(4)]
        return _tb("Count back in 10s:  %s, ___" % ", ".join(map(str, s)), s[-1] - 10, "int", {}, ["Take away 10; the ones digit stays the same."])

    def t_threes():
        n = random.randint(2, 8)
        return _tb("A tricycle has 3 wheels. How many wheels are on %s? Count in 3s." % _pn(n, "tricycle"), 3 * n, "int", {},
                   ["%s." % ", ".join(str(3 * i) for i in range(1, n + 1))])

    def t_jumps():
        return _tb("How many jumps of %d take you from 0 to %d?" % (step, k * step), k, "int", {},
                   ["%s: %d jumps." % (", ".join(str(step * i) for i in range(1, k + 1)), k)])

    def t_in_count():
        n = step * random.randint(2, 10) + pick([0, 0, 1, 2 if step > 2 else 1])
        return _wq("Do you say %d when you count in %ss from 0? (yes or no)" % (n, step), "yes" if n % step == 0 else "no",
                   ["Counting in %ss: %s." % (step, ", ".join(str(step * i) for i in range(1, 11)))], "yes / no")

    def t_line_back():
        top = step * random.randint(k + 1, k + 4)
        return _nl("Start at %d and make %d jumps back of %d. Where do you land?" % (top, k, step), top - k * step, step, 10,
                   ["%d − %d = %d." % (top, k * step, top - k * step)], lo=0, hi=max(30, (top // 10 + 1) * 10))

    def t_missing_tens():
        start = random.randint(1, 9) + 10 * random.randint(0, 4)
        s = [start + 10 * i for i in range(5)]
        j = random.randint(1, 3)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == j else str(v) for i, v in enumerate(s)), s[j], "int", {},
                   ["The numbers go up in 10s."])

    def t_money():
        c = pick([2, 5, 10])
        return _tb("%s has %s. How much money is that, in pence?" % (_kid(), _pn(k, "%dp coin" % c)), c * k, "int", {"unit": "p"},
                   ["Count in %ss: %d." % (c, c * k)])

    return _pick_t([t_next, t_back, t_tens_any, t_missing, t_back_tens, t_threes, t_jumps, t_in_count, t_missing_tens, t_money],
                   [t_line, t_line_back])


@skill("Y2.0.b", "Tens and ones in two-digit numbers", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(11, 99)

    def t_value():
        return _tb("In %d, what is the tens digit worth?" % n, (n // 10) * 10, "int", {},
                   ["%d = %d + %d." % (n, (n // 10) * 10, n % 10)])

    def t_partition():
        return _tb("%d = %d + ___" % (n, (n // 10) * 10), n % 10, "int", {}, ["%s." % _tn(n // 10, n % 10)])

    def t_parts():
        return _tb("%d + %d = ___" % ((n // 10) * 10, n % 10), n, "int", {}, ["Tens and ones: %d." % n])

    def t_build():
        return {"prompt": "Make %d with tens and ones." % n, "component": "base_ten", "spec": {"mode": "build", "max": 9},
                "answer": n, "answer_type": "int", "solution": ["%s." % _tn(n // 10, n % 10)]}

    def t_other_way():
        t = n // 10
        if t < 2:
            return t_partition()
        return _tb("%d is %s. It is also %s and how many ones?" % (n, _tn(t, n % 10), _pn(t - 1, "ten")), n % 10 + 10, "int",
                   {}, ["Swap one ten for 10 ones: %d ones." % (n % 10 + 10)])

    def t_ones_worth():
        m = random.choice([x for x in range(11, 100) if x % 10])
        return _tb("In %d, what is the ones digit worth?" % m, m % 10, "int", {}, ["%d = %d + %d." % (m, (m // 10) * 10, m % 10)])

    def t_how_many_tens():
        return _tb("How many tens are there in %d?" % n, n // 10, "int", {}, ["%d = %s and %s." % (n, _pn(n // 10, "ten"), _pn(n % 10, "one"))])

    def t_ten_more():
        m = random.randint(11, 89)
        return _tb("What is 10 more than %d?" % m, m + 10, "int", {}, ["The tens digit goes up by 1."])

    def t_ten_less():
        m = random.randint(20, 99)
        return _tb("What is 10 less than %d?" % m, m - 10, "int", {}, ["The tens digit goes down by 1."])

    def t_swap():
        m = random.choice([x for x in range(12, 99) if x % 10 and x // 10 != x % 10])
        r = (m % 10) * 10 + m // 10
        return _tb("Swap the digits of %d. What number do you make?" % m, r, "int", {}, ["%s is %d." % (_tn(m % 10, m // 10), r)])

    def t_split():
        t = n // 10
        if t < 2:
            return t_partition()
        p = 10 * random.randint(1, t - 1)
        return _tb("%d = %d + ___" % (n, p), n - p, "int", {}, ["%d − %d = %d." % (n, p, n - p)])

    def t_coins():
        t, o = random.randint(1, 9), random.randint(1, 9)
        return _tb("%s has %s and %s. How many pence is that?" % (_kid(), _pn(t, "10p coin"), _pn(o, "1p coin")), 10 * t + o, "int",
                   {"unit": "p"}, ["%s: %dp." % (_tn(t, o), 10 * t + o)])

    def t_digit_place():
        m = random.choice([x for x in range(12, 99) if x % 10 and x // 10 != x % 10])
        which = pick(["tens", "ones"])
        return _tb("Which digit is in the %s place in %d?" % (which, m), m // 10 if which == "tens" else m % 10, "int", {},
                   ["%d: tens digit %d, ones digit %d." % (m, m // 10, m % 10)])

    def t_line():
        return _nl("Put %d on the number line." % n, n, 1, 10, ["%d is %s." % (n, _tn(n // 10, n % 10))], lo=0, hi=100)

    return _pick_t([t_value, t_partition, t_parts, t_other_way, t_ones_worth, t_how_many_tens, t_ten_more, t_ten_less, t_swap,
                    t_split, t_coins, t_digit_place], [t_build, t_line])


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

    def t_sym3():
        t, o = random.randint(1, 9), random.randint(0, 9)
        right = 10 * t + o + pick([-1, 0, 0, 1])
        sym = "<" if 10 * t + o < right else (">" if 10 * t + o > right else "=")
        return _wq("Write <, > or = :  %d + %d ___ %d" % (10 * t, o, right), sym, ["%d + %d = %d." % (10 * t, o, 10 * t + o)], "<, > or =")

    def t_compare_sums():
        x, y = random.randint(10, 40), random.randint(10, 40)
        p, q = random.randint(10, 40), random.randint(10, 40)
        sym = "<" if x + y < p + q else (">" if x + y > p + q else "=")
        return _wq("Write <, > or = :  %d + %d ___ %d + %d" % (x, y, p, q), sym,
                   ["%d + %d = %d and %d + %d = %d." % (x, y, x + y, p, q, p + q)], "<, > or =")

    def t_smallest():
        ds = random.sample(range(1, 10), 2)
        return _tb("Use the digits %d and %d to make the smallest two-digit number." % tuple(ds), min(ds) * 10 + max(ds), "int", {},
                   ["Put the smaller digit in the tens place."])

    def t_order_down():
        vals = random.sample(range(1, 100), 4)
        k = random.randint(1, 4)
        return _tb("Put these in order, largest first. Which is number %d in the list?  %s" % (k, ", ".join(map(str, vals))),
                   sorted(vals, reverse=True)[k - 1], "int", {}, ["In order: %s." % ", ".join(map(str, sorted(vals, reverse=True)))])

    def t_tens_vs():
        t = random.randint(2, 9)
        m = 10 * t + random.choice([-3, -2, -1, 1, 2, 3])
        return _tb("Which is greater: %d tens or %d? Type the greater number." % (t, m), max(10 * t, m), "int", {},
                   ["%d tens is %d." % (t, 10 * t)])

    def t_true():
        x, y = random.sample(range(10, 100), 2)
        sym = pick(["<", ">"])
        right = (x < y) if sym == "<" else (x > y)
        return _wq("Is this true?  %d %s %d  (yes or no)" % (x, sym, y), "yes" if right else "no",
                   ["%d is %s than %d." % (x, "less" if x < y else "more", y)], "yes / no")

    return _pick_t([t_symbol, t_equal, t_order, t_biggest, t_sym3, t_compare_sums, t_smallest, t_order_down, t_tens_vs, t_true],
                   [t_line])


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
    p = random.randint(1, 9)
    q = random.randint(1, 10 - p)      # tens facts stay within 100

    def t_fact():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_sub_fact():
        return _tb("%d − %d = ___" % (a + b, b), a, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_tens():
        return _tb("%d + %d = ___" % (10 * p, 10 * q), 10 * (p + q), "int", {}, ["%d + %d = %d, so %d." % (p, q, p + q, 10 * (p + q))])

    def t_bond100():
        t = random.randint(1, 9) * 10
        return _tb("%d + ___ = 100" % t, 100 - t, "int", {}, ["%d + %d = 10, so %d + %d = 100." % (t // 10, 10 - t // 10, t, 100 - t)])

    def t_related():
        return _tb("%d + %d = %d. Use this to work out %d + %d." % (a, b, a + b, a, b + 10), a + b + 10, "int", {},
                   ["%d is 10 more than %d, so the answer is 10 more." % (b + 10, b)])

    def t_sub_tens():
        return _tb("%d − %d = ___" % (10 * (p + q), 10 * q), 10 * p, "int", {}, ["%d − %d = %d, so %d." % (p + q, q, p, 10 * p)])

    def t_bond20():
        k = random.randint(1, 19)
        return _tb("%d + ___ = 20" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])

    def t_from100():
        t = random.randint(1, 9) * 10
        return _tb("100 − %d = ___" % t, 100 - t, "int", {}, ["%d + %d = 100." % (t, 100 - t)])

    def t_word():
        kid = _kid()
        return _tb("%s scores %s, then %d more. How many points altogether?" % (kid, _pn(a, "point"), b), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)])

    def t_bar():
        return _strip("The whole is %d. One part is %d. What is the other part?" % (a + b, a),
                      {"mode": "part_whole", "totalLabel": str(a + b), "partLabel": str(a), "unknown": "part", "parts": 2}, b,
                      ["%d − %d = %d." % (a + b, a, b)])

    def t_double_tens():
        k = random.randint(1, 5)
        return _tb("Double %d = ___" % (10 * k), 20 * k, "int", {}, ["Double %d is %d, so double %d is %d." % (k, 2 * k, 10 * k, 20 * k)])

    def t_true():
        right = random.random() < 0.5
        shown = p + q if right else p + q + pick([-1, 1])
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (10 * p, 10 * q, 10 * shown), "yes" if right else "no",
                   ["%d + %d = %d." % (10 * p, 10 * q, 10 * (p + q))], "yes / no")

    def t_line():
        return _nl("Start at %d. Jump on %d. Where do you land?" % (10 * p, 10 * q), 10 * (p + q), 10, 10,
                   ["%d + %d = %d." % (10 * p, 10 * q, 10 * (p + q))], lo=0, hi=100)

    return _pick_t([t_fact, t_sub_fact, t_tens, t_bond100, t_related, t_sub_tens, t_bond20, t_from100, t_word, t_double_tens, t_true],
                   [t_bar, t_line])


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

    def t_bridge():
        o = n % 10
        k = random.randint(max(1, 11 - o), 9) if o >= 2 and n < 90 else random.randint(1, 9)
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["%d + %d = %d, then + %d = %d." % (n, 10 - o, n + 10 - o, k - (10 - o), n + k)]
                   if o and k > 10 - o else ["Count on %d: %d." % (k, n + k)])

    def t_word_tens():
        k = random.randint(1, (99 - n) // 10) * 10 if n < 90 else 10
        return _tb("%s has %d stickers and gets %d more. How many stickers now?" % (_kid(), n, k), n + k, "int", {},
                   ["%d + %d = %d." % (n, k, n + k)])

    def t_word_ones():
        k = random.randint(1, 9)
        return _tb("A shop has %d apples. It sells %s. How many are left?" % (n, _pn(k, "apple")), n - k, "int", {},
                   ["%d − %d = %d." % (n, k, n - k)])

    def t_missing():
        k = random.randint(1, (99 - n) // 10) * 10 if n < 90 else 10
        return _tb("%d + ___ = %d" % (n, n + k), k, "int", {}, ["The tens digit went up by %d, so %d." % (k // 10, k)])

    def t_blocks():
        k = random.randint(1, (99 - n) // 10) * 10 if n < 90 else 10
        return {"prompt": "Work out %d + %d. Make the answer with the blocks." % (n, k), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": n + k, "answer_type": "int", "solution": ["%d." % (n + k)]}

    def t_line_back():
        k = random.randint(2, 9)
        return _nl("Start at %d and jump back %d. Where do you land?" % (n, k), n - k, 1, 10, ["%d − %d = %d." % (n, k, n - k)],
                   lo=max(0, (n // 10) * 10 - 10), hi=max(0, (n // 10) * 10 - 10) + 20)

    def t_money():
        k = pick([10, 20, 30])
        m = min(n, 99 - k)
        return _tb("%s has %dp and is given %dp more. How much now, in pence?" % (_kid(), m, k), m + k, "int", {"unit": "p"},
                   ["%d + %d = %d." % (m, k, m + k)])

    return _pick_t([t_add_ones, t_sub_ones, t_add_tens, t_sub_tens, t_bridge, t_word_tens, t_word_ones, t_missing, t_money],
                   [t_line, t_blocks, t_line_back])


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

    def t_bar():
        x, y = max(a, b), min(a, b)
        return _strip("A red ribbon is %d cm. A blue ribbon is %d cm. How much longer is the red ribbon, in cm?" % (x, y),
                      {"mode": "part_whole", "totalLabel": str(x), "partLabel": str(y), "unknown": "part", "parts": 2},
                      x - y, ["%d − %d = %d." % (x, y, x - y)]) if x > y else t_add()

    def t_three_word():
        x, y, z = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
        return _tb("%s has %d red, %d blue and %d green pens. How many pens altogether?" % (_kid(), x, y, z), x + y + z, "int", {},
                   ["%d + %d + %d = %d." % (x, y, z, x + y + z)])

    def t_missing():
        return _tb("%d + ___ = %d" % (a, a + b), b, "int", {}, ["%d − %d = %d." % (a + b, a, b)])

    return _pick_t([t_add, t_sub, t_three, t_word, t_three_word, t_missing], [t_blocks, t_bar])


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

    def t_missing_first():
        return _tb("___ + %d = %d" % (b, a + b), a, "int", {}, ["%d − %d = %d." % (a + b, b, a)])

    def t_sub_gap():
        return _tb("%d − ___ = %d" % (a + b, a), b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_true_commute():
        return _wq("Is this true?  %d + %d = %d + %d  (yes or no)" % (a, b, b, a), "yes", ["You can add in any order."], "yes / no")

    def t_family():
        return _tb("%d + %d = %d. Use this to find %d − %d." % (a, b, a + b, a + b, a), b, "int", {},
                   ["Subtraction undoes addition: %d." % b])

    def t_bar():
        return _strip("The whole is %d. One part is %d. What is the missing part?" % (a + b, b),
                      {"mode": "part_whole", "totalLabel": str(a + b), "partLabel": str(b), "unknown": "part", "parts": 2}, a,
                      ["%d − %d = %d." % (a + b, b, a)])

    def t_think():
        return _tb("I think of a number and take away %d. I get %d. What was my number?" % (b, a), a + b, "int", {},
                   ["Add back: %d + %d = %d." % (a, b, a + b)])

    def t_check_answer():
        wrong = random.random() < 0.5
        shown = a + b + (pick([-1, 1, 10]) if wrong else 0)
        return _wq("Sam says %d + %d = %d. Check it by subtracting. Is Sam right? (yes or no)" % (a, b, shown), "no" if wrong else "yes",
                   ["%d − %d = %d%s." % (shown, b, shown - b, "" if not wrong else ", not %d" % a)], "yes / no")

    return _pick_t([t_commute, t_not_commute, t_missing_add, t_missing_sub, t_check, t_missing_first, t_sub_gap, t_true_commute,
                    t_family, t_think, t_check_answer], [t_bar])


@skill("Y2.1.e", "Addition and subtraction problems", S1)
def _(d=1):
    d = _d(d)
    kid = _kid()

    def t_change():
        cost, pay = random.randint(11, 90), pick([50, 100])
        if cost >= pay:
            pay = 100
        return _tb("%s buys a toy for %dp and pays with %s. How much change, in pence?" % (kid, cost, "£1" if pay == 100 else "50p"),
                   pay - cost, "int", {"unit": "p"},
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
        return _tb("%d × %d = ___" % (k, t), k * t, "int", {}, ["%s of %d." % (_pn(k, "lot"), t)])

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

    def t_missing_div():
        return _tb("___ ÷ %d = %d" % (t, k), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_true():
        right = random.random() < 0.5
        shown = k * t if right else k * t + pick([-t, t, 1])
        return _wq("Is this true?  %d × %d = %d  (yes or no)" % (k, t, shown), "yes" if right else "no",
                   ["%d × %d = %d." % (k, t, k * t)], "yes / no")

    def t_word():
        what = {2: ("pair of socks", "pairs of socks", "socks"), 5: ("hand", "hands", "fingers"),
                10: ("pack of 10 pens", "packs of 10 pens", "pens")}[t]
        return _tb("How many %s are in %d %s?" % (what[2], k, what[0] if k == 1 else what[1]), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_line():
        return _nl("Count in %ds. Mark %d × %d on the number line." % (t, k, t), k * t, t, 10, ["%d × %d = %d." % (k, t, k * t)],
                   lo=0, hi=max(30, (k * t // 10 + 1) * 10))

    def t_double():
        return _tb("Double %d = ___" % k, 2 * k, "int", {}, ["Double means × 2: %d × 2 = %d." % (k, 2 * k)])

    def t_which_table():
        x = pick([2, 5, 10])
        n = x * random.randint(1, 12) if random.random() < 0.5 else pick([v for v in range(3, 12 * x + 1) if v % x])
        return _wq("Is %d in the %d times table? (yes or no)" % (n, x), "yes" if n % x == 0 else "no",
                   ["%d %s in the %d times table." % (n, "is" if n % x == 0 else "is not", x)], "yes / no")

    return _pick_t([t_mult, t_div, t_missing, t_missing_div, t_true, t_word, t_double, t_which_table], [t_groups, t_array, t_line])


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

    def t_next_odd():
        n = random.randint(1, 98)
        nxt = n + 1 if n % 2 == 0 else n + 2
        return _tb("What is the next odd number after %d?" % n, nxt, "int", {}, ["Odd numbers end in 1, 3, 5, 7 or 9: %d." % nxt])

    def t_prev_even():
        n = random.randint(3, 100)
        prv = n - 1 if n % 2 else n - 2
        return _tb("What is the even number just before %d?" % n, prv, "int", {}, ["%d." % prv])

    def t_houses():
        k = random.randint(3, 12)
        side = pick(["odd", "even"])
        first = 1 if side == "odd" else 2
        return _tb("The houses on one side of a street have %s numbers: %d, %d, %d, ... What is the number of house %d on that side?"
                   % (side, first, first + 2, first + 4, k), first + 2 * (k - 1), "int", {},
                   ["Count on in 2s: %d." % (first + 2 * (k - 1))])

    def t_biggest_even():
        ds = random.sample(range(1, 10), 3)
        evens = [10 * a + b for a in ds for b in ds if a != b and b % 2 == 0]
        if not evens:
            return t_is()
        return _tb("Use two of the digits %d, %d and %d. Make the biggest even number you can." % tuple(ds), max(evens), "int", {},
                   ["The ones digit must be even."])

    def t_groups():
        n = random.randint(2, 10)
        extra = pick([0, 1])
        if extra:
            return _wq("%d counters are put into pairs. One counter is left without a partner. Is %d odd or even?" % (2 * n + 1, 2 * n + 1),
                       "odd", ["One is left without a partner, so it is odd."], "odd / even")
        return {"prompt": "Here are %d counters in pairs%s. Is %d odd or even?" % (2 * n + extra, " and one more" if extra else "",
                                                                                   2 * n + extra),
                "component": "equal_groups", "spec": {"mode": "read", "groups": n, "per": 2}, "answer": "odd" if extra else "even",
                "answer_type": "str", "solution": ["%s" % ("One is left without a partner, so it is odd." if extra else "Every counter has a partner, so it is even.")]}

    def t_teams():
        n = random.randint(6, 30)
        return _wq("%d children get into pairs. Is anyone left without a partner? (yes or no)" % n, "yes" if n % 2 else "no",
                   ["%d is %s." % (n, "odd" if n % 2 else "even")], "yes / no")

    def t_sum_odd():
        x, y = random.randint(1, 20), random.randint(1, 20)
        return _wq("Is %d + %d odd or even?" % (x, y), "even" if (x + y) % 2 == 0 else "odd", ["%d + %d = %d." % (x, y, x + y)], "odd / even")

    def t_line_even():
        n = random.randint(1, 48)
        nxt = n + 1 if n % 2 else n + 2
        return _nl("Mark the first even number after %d on the number line." % n, nxt, 1, 10, ["%d is even." % nxt], lo=0, hi=50)

    return _pick_t([t_is, t_next_even, t_count, t_pairs, t_next_odd, t_prev_even, t_houses, t_biggest_even, t_teams, t_sum_odd],
                   [t_groups, t_line_even])


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
        return _tb("%s = ___" % " + ".join([str(a)] * b), a * b, "int", {}, ["%s of %d = %d × %d = %d." % (_pn(b, "lot"), a, b, a, a * b)])

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

    def t_fingers():
        return _tb("How many fingers are on %d hands?" % k, 5 * k, "int", {}, ["%d × 5 = %d." % (k, 5 * k)])

    def t_price():
        return _tb("Pencils cost %dp each. How much do %d pencils cost, in pence?" % (t, k), k * t, "int", {"unit": "p"},
                   ["%d × %d = %d." % (k, t, k * t)])

    def t_how_many_bought():
        kid = _kid()
        return _tb("Stickers cost %dp each. %s spends %dp. How many stickers does %s buy?" % (t, kid, k * t, kid), k, "int", {},
                   ["%d ÷ %d = %d." % (k * t, t, k)])

    def t_share_bar():
        return _strip("%d cakes are shared equally onto %d plates. How many on each plate?" % (k * t, t),
                      {"mode": "equal_parts", "parts": t, "partLabel": "?", "totalLabel": str(k * t), "unknown": "part"}, k,
                      ["%d ÷ %d = %d." % (k * t, t, k)]) if t <= 5 else t_share()

    def t_groups():
        return {"prompt": "%d sweets are put into bags of %d. How many bags?" % (k * t, t), "component": "equal_groups",
                "spec": {"mode": "read", "groups": k, "per": t}, "answer": k, "answer_type": "int",
                "solution": ["%d ÷ %d = %d." % (k * t, t, k)]}

    def t_array():
        return {"prompt": "Chairs are in %d rows of %d. Build the array. How many chairs?" % (k, t), "component": "array",
                "spec": {"mode": "build", "maxRows": 10, "maxCols": 10, "targetRows": k, "targetCols": t}, "answer": k * t,
                "answer_type": "int", "solution": ["%d × %d = %d." % (k, t, k * t)]}

    def t_repeated():
        return _tb("A frog jumps %d cm each hop. How far does it go in %d hops, in cm?" % (t, k), k * t, "int", {"unit": "cm"},
                   ["%s = %d." % (" + ".join([str(t)] * k), k * t)])

    return _pick_t([t_bags, t_share, t_coins, t_teams, t_fingers, t_price, t_how_many_bought, t_repeated],
                   [t_bar, t_share_bar, t_groups, t_array])


# ================================================================== 2.3 ======
@skill("Y2.3.a", "Find 1/3, 1/4, 2/4 and 3/4 of a shape", S3)
def _(d=1):
    d = _d(d)

    def t_shade():
        f = pick([(1, 3), (1, 4), (2, 4), (3, 4), (1, 2)])
        return {"prompt": "Shade %d/%d of the bar." % f, "component": "fraction_bar", "spec": {"parts": f[1], "mode": "shade"},
                "answer": "%d/%d" % f, "answer_type": "frac", "solution": ["Shade %d of the %d equal parts." % f]}

    def t_read():
        f = pick([(1, 3), (1, 4), (3, 4), (2, 4), (1, 2)])
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

    def t_grid():
        f = pick([(1, 3), (1, 4), (2, 4), (3, 4), (1, 2)])
        parts = f[1] * pick([1, 2, 3])
        return _area("Shade %d/%d of the shape." % f, {"mode": "fraction", "parts": parts}, "%d/%d" % f,
                     ["%d/%d of %d squares is %s." % (f[0], f[1], parts, _pn(parts * f[0] // f[1], "square"))], atype="frac")

    def t_bigger():
        a, b = pick([("1/3", "1/4"), ("1/2", "1/4"), ("1/2", "1/3"), ("3/4", "1/4"), ("2/4", "1/4"), ("3/4", "1/2")])
        x, y = (a, b) if random.random() < 0.5 else (b, a)
        return _fq("Which is bigger, %s or %s of the same cake?" % (x, y), Fraction(a), ["%s is bigger." % a])

    def t_is_third():
        sh = random.randint(1, 2)
        n = pick([3, 4])
        right = (n == 3 and sh == 1)
        return _wq("A bar is cut into %d equal parts and %d %s shaded. Is one third shaded? (yes or no)"
                   % (n, sh, "is" if sh == 1 else "are"), "yes" if right else "no",
                   ["One third is 1 of 3 equal parts." if not right else "1 of 3 equal parts is one third."], "yes / no")

    def t_name():
        f, w = pick([("1/3", "one third"), ("1/4", "one quarter"), ("3/4", "three quarters"), ("2/4", "two quarters")])
        return _fq("Write %s as a fraction (like 1/2)." % w, Fraction(f), ["%s = %s." % (w.capitalize(), f)])

    def t_unequal():
        return _wq("A pizza is cut into 4 pieces of different sizes. Is each piece a quarter? (yes or no)", "no",
                   ["Quarters must be 4 equal parts."], "yes / no")

    def t_how_many_more():
        f = pick([(1, 4), (2, 4), (1, 3)])
        return _tb("%d/%d of a bar is shaded. How many more %s must be shaded to fill it?" % (f[0], f[1], "quarters" if f[1] == 4 else "thirds"),
                   f[1] - f[0], "int", {}, ["%d/%d + %d/%d = 1 whole." % (f[0], f[1], f[1] - f[0], f[1])])

    def t_half_quarters():
        return _tb("How many quarters are the same as one half?", 2, "int", {}, ["2/4 = 1/2."])

    return _pick_t([t_equiv, t_parts, t_left, t_bigger, t_is_third, t_name, t_unequal, t_how_many_more, t_half_quarters],
                   [t_shade, t_read, t_grid])


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

    def t_two_quarters():
        n = 4 * random.randint(1, 8)
        return _tb("What is 2/4 of %d?" % n, n // 2, "int", {}, ["2/4 is the same as 1/2: half of %d is %d." % (n, n // 2)])

    def t_word_third():
        n = 3 * random.randint(2, 8)
        kid = _kid()
        return _tb("%s has %d marbles and gives 1/3 of them away. How many marbles are given away?" % (kid, n), n // 3, "int", {},
                   ["%d ÷ 3 = %d." % (n, n // 3)])

    def t_left():
        n = 4 * random.randint(2, 6)
        return _tb("There are %d biscuits. 1/4 of them are eaten. How many are left?" % n, n - n // 4, "int", {},
                   ["1/4 of %d is %d; %d − %d = %d." % (n, n // 4, n, n // 4, n - n // 4)])

    def t_strip():
        g = pick([3, 4])
        k = random.randint(2, 9)
        return _strip("What is 1/%d of %d?" % (g, g * k), {"mode": "equal_parts", "parts": g, "partLabel": "?", "totalLabel": str(g * k),
                                                         "unknown": "part"}, k, ["%d ÷ %d = %d." % (g * k, g, k)])

    def t_whole():
        k = random.randint(2, 10)
        g = pick([2, 3, 4])
        return _tb("1/%d of a number is %d. What is the number?" % (g, k), g * k, "int", {}, ["%d × %d = %d." % (k, g, g * k)])

    def t_money():
        n = pick([12, 20, 40, 60, 80, 100]) if random.random() < 0.5 else 4 * random.randint(2, 10)
        return _tb("%s has %dp and spends 1/4 of it. How much is spent, in pence?" % (_kid(), n), n // 4, "int", {"unit": "p"},
                   ["%d ÷ 4 = %d." % (n, n // 4)])

    return _pick_t([t_third, t_quarter, t_three_quarters, t_half_of, t_length, t_two_quarters, t_word_third, t_left, t_whole, t_money],
                   [t_groups, t_strip])


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
        t = random.randint(0, 30)
        return _tb("A thermometer shows %d °C. It gets 5 degrees warmer. What does it show now, in °C?" % t, t + 5, "int",
                   {"unit": "°C"}, ["%d + 5 = %d." % (t, t + 5)])

    def t_temp():
        a, b = random.sample(range(0, 35), 2)
        return _tb("Which is warmer, %d °C or %d °C? Type the number." % (a, b), max(a, b), "int", {}, ["%d is higher." % max(a, b)])

    def t_estimate():
        q, a = pick([("A door is about 2 ___ tall. Is it m or cm?", "m"),
                     ("A bag of sugar has a mass of about 1 ___. Is it kg or g?", "kg"),
                     ("A cup holds about 200 ___. Is it ml or litres?", "ml"),
                     ("A paper clip is about 3 ___ long. Is it cm or m?", "cm"),
                     ("A hot summer day is about ___ °C. Is it 25 or 95?", "25"),
                     ("A child has a mass of about 25 ___. Is it kg or g?", "kg")])
        return _wq(q, a, ["Think about how big the real thing is."], "type it")

    def t_grams():
        v = random.randint(1, 9) * 100
        return {"prompt": "Read the scale. How many grams?", "component": "ruler", "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v, "answer_type": "num", "tolerance": 50, "solution": ["%d g." % v]}

    def t_long_ruler():
        cm = random.randint(5, 29) if d else random.randint(5, 15)
        return {"prompt": "Measure the pencil. How long is it, in cm?", "component": "ruler",
                "spec": {"mode": "length", "value": cm, "max": 30, "unit": "cm"}, "answer": cm, "answer_type": "num", "tolerance": 0.5,
                "solution": ["It ends at %d cm." % cm]}

    def t_colder():
        a, b = random.sample(range(0, 30), 2)
        return _tb("It was %d °C in the morning and %d °C at night. How many degrees colder was the colder time?" % (max(a, b), min(a, b)),
                   abs(a - b), "int", {"unit": "°C"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_litres():
        v = random.randint(2, 9)
        return _tb("A bucket holds %d litres. How much do 2 buckets hold, in litres?" % v, 2 * v, "int", {"unit": "litres"},
                   ["%d + %d = %d." % (v, v, 2 * v)])

    def t_jug_more():
        v = random.randint(1, 8) * 100
        return {"prompt": "How much more water is needed to make 1000 ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"}, "answer": 1000 - v, "answer_type": "num",
                "tolerance": 0, "solution": ["The jug shows %d ml; 1000 − %d = %d." % (v, v, 1000 - v)]}

    return _pick_t([t_unit, t_temp, t_thermo, t_estimate, t_colder, t_litres], [t_ruler, t_scale, t_jug, t_grams, t_long_ruler, t_jug_more])


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

    def t_eq():
        unit = pick(["cm", "kg", "ml"])
        a = random.randint(10, 60)
        b = a + pick([-5, 0, 5])
        sym = "<" if a < b else (">" if a > b else "=")
        return _wq("Write <, > or = :  %d %s ___ %d %s" % (a, unit, b, unit), sym, ["Compare the numbers."], "<, > or =")

    def t_heaviest():
        names = ["red", "blue", "green"]
        v = random.sample(range(2, 30), 3)
        k = pick(["heaviest", "lightest"])
        ans = names[v.index(max(v))] if k == "heaviest" else names[v.index(min(v))]
        return _dt("The table shows the mass of three parcels. Which parcel is the %s?" % k, ["Parcel", "Mass (kg)"],
                   [[names[i], v[i]] for i in range(3)], ans, ["Compare the masses."], atype="str", placeholder="colour")

    def t_order_cap():
        v = random.sample(range(1, 10), 3)
        vals = [x * 100 for x in v]
        return _tb("Put these in order, most first. Which comes first?  %s" % ", ".join("%d ml" % x for x in vals), max(vals), "int",
                   {"unit": "ml"}, ["Order: %s." % ", ".join("%d ml" % x for x in sorted(vals, reverse=True))])

    def t_taller():
        a, b = random.sample(range(90, 140), 2)
        kids = random.sample(KIDS, 2)
        return _tb("%s is %d cm tall. %s is %d cm tall. How much taller is the taller child, in cm?" % (kids[0], a, kids[1], b), abs(a - b),
                   "int", {"unit": "cm"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_bars():
        cats = ["Jug", "Cup", "Bottle", "Bowl"]
        vals = random.sample(range(1, 10), 4)
        return _bar("The chart shows how many glasses each one fills. Which holds the most?", cats, vals, cats[vals.index(max(vals))],
                    ["%s has the tallest bar." % cats[vals.index(max(vals))]], atype="str")

    return _pick_t([t_symbol, t_longest, t_order, t_difference, t_eq, t_order_cap, t_taller], [t_heaviest, t_bars])


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
        pay = 100 if cost >= 50 else pick([50, 100])
        return _tb("A comic costs %dp. You pay with %s. How much change, in pence?" % (cost, "£1" if pay == 100 else "50p"),
                   pay - cost, "int", {"unit": "p"}, ["%d − %d = %d." % (pay, cost, pay - cost)])

    def t_two_ways():
        return _wq("Do 20p + 20p + 10p and 50p make the same amount? (yes or no)", "yes", ["Both make 50p."], "yes / no")

    def t_shop():
        a, b = random.randint(10, 45), random.randint(10, 45)
        return _tb("A pencil costs %dp and a rubber costs %dp. How much for both, in pence?" % (a, b), a + b, "int", {"unit": "p"},
                   ["%d + %d = %d." % (a, b, a + b)])

    def t_how_many_coins():
        c, tot = pick([(5, 20), (5, 30), (10, 50), (10, 70), (2, 10), (2, 16), (20, 100), (5, 50), (10, 100)])
        return _tb("How many %dp coins make %dp?" % (c, tot), tot // c, "int", {}, ["%d ÷ %d = %d." % (tot, c, tot // c)])

    def t_missing_coin():
        c = pick([1, 2, 5, 10, 20, 50])
        known = pick([x for x in (5, 10, 20, 50) if x + c <= 100])
        return _tb("%dp + ___p = %dp. Which coin is missing? Type its value in pence." % (known, known + c), c, "int", {"unit": "p"},
                   ["%d − %d = %d." % (known + c, known, c)])

    def t_same():
        a = random.sample([1, 2, 5, 10, 20], 3)
        b = sum(a) + pick([0, 0, 1, 5])
        return _wq("Mia has %s. Ben has %dp. Do they have the same amount? (yes or no)" % (" + ".join("%dp" % x for x in a), b),
                   "yes" if sum(a) == b else "no", ["%s = %dp." % (" + ".join(map(str, a)), sum(a))], "yes / no")

    def t_whole_pounds():
        p = random.randint(1, 9) * 100 + pick([0, 0, 20, 50])
        return _tb("%dp is how many whole pounds and some pence? Type the number of whole pounds." % p, p // 100, "int", {},
                   ["100p = £1, so %dp = £%d and %dp." % (p, p // 100, p % 100)])

    def t_notes():
        a, b = random.sample([5, 10, 20], 2)
        n = random.randint(1, 3)
        return _tb("%s has %s and a £%d note. How many pounds is that?" % (_kid(), _pn(n, "£%d note" % a), b), n * a + b, "int",
                   {"unit": "£"}, ["%d × £%d + £%d = £%d." % (n, a, b, n * a + b)])

    def t_change_pounds():
        cost = random.randint(2, 9)
        pay = pick([10, 20]) if cost >= 5 else pick([5, 10])
        return _tb("A book costs £%d. You pay with a £%d note. How much change, in pounds?" % (cost, pay), pay - cost, "int", {"unit": "£"},
                   ["%d − %d = %d." % (pay, cost, pay - cost)])

    return _pick_t([t_total, t_pounds, t_make, t_change, t_two_ways, t_shop, t_how_many_coins, t_missing_coin, t_same, t_whole_pounds,
                    t_notes, t_change_pounds])


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
                   ["Each number is 5 minutes: %d × 5 = %d." % (m // 5, m)] if m else
                   ["When the long hand points to 12 it is o'clock: 0 minutes past."])

    def t_type_time():
        mm = pick([5, 10, 20, 25])
        hh = random.randint(1, 12)
        return _tb("Write %d minutes past %d as a time like 4:20." % (mm, hh), "%d:%02d" % (hh, mm), "time",
                   {"text": True, "placeholder": "e.g. 4:20"}, ["%d minutes past %d is %d:%02d." % (mm, hh, hh, mm)])

    def t_quarter_hand():
        kind, num = pick([("quarter past", 3), ("half past", 6), ("quarter to", 9), ("o'clock", 12)])
        return _tb("At %s, which number does the long hand point to?" % kind, num, "int", {}, ["%s: the long hand points to %d." % (kind.capitalize(), num)])

    def t_minutes_to():
        n = random.randint(7, 11)
        return _tb("The long hand points to %d. How many minutes is it until the next o'clock?" % n, 60 - 5 * n, "int", {},
                   ["%d × 5 = %d minutes past; 60 − %d = %d." % (n, 5 * n, 5 * n, 60 - 5 * n)])

    def t_five_later():
        k = pick([5, 10, 15])
        mm = 5 * random.randint(0, (55 - k) // 5)
        return {"prompt": "It is %d:%02d. Set the clock to %d minutes later." % (h, mm, k), "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:%02d" % (h, mm + k), "answer_type": "time", "solution": ["%d:%02d + %d minutes = %d:%02d." % (h, mm, k, h, mm + k)]}

    def t_digital():
        mm = 5 * random.randint(1, 11)
        return {"prompt": "A digital clock shows %d:%02d. Show the same time on this clock." % (h, mm), "component": "clock",
                "spec": {"mode": "set"}, "answer": "%d:%02d" % (h, mm), "answer_type": "time",
                "solution": ["The long hand points to %d." % (mm // 5)]}

    def t_words_out():
        mm = pick([15, 30, 45])
        hh = random.randint(1, 11)
        word, ans = {15: ("quarter past", hh), 30: ("half past", hh), 45: ("quarter to", hh + 1)}[mm]
        return _tb("A clock shows %d:%02d. Is it quarter past, half past or quarter to which hour? Type the hour." % (hh, mm), ans, "int", {},
                   ["%d:%02d is %s %d." % (hh, mm, word, ans)])

    return _pick_t([t_long_hand, t_type_time, t_quarter_hand, t_minutes_to, t_words_out], [t_set, t_quarter, t_words, t_five_later, t_digital])


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

    def t_count_four():
        shapes = [pick(["square", "triangle", "rectangle", "pentagon", "circle", "hexagon"]) for _ in range(6)]
        n = sum(1 for x in shapes if x in ("square", "rectangle"))
        return _tb("How many of these shapes have 4 sides?  %s" % ", ".join(shapes), n, "int", {}, ["Squares and rectangles have 4 sides."])

    def t_curved():
        q, a = pick([("Which of these has a curved side: square, circle or triangle?", "circle"),
                     ("Which of these has no straight sides: hexagon, circle or rectangle?", "circle"),
                     ("Which of these has 6 sides: pentagon, hexagon or octagon?", "hexagon"),
                     ("Which of these has 8 sides: hexagon, pentagon or octagon?", "octagon")])
        return _wq(q, a, ["Count the sides."], "shape name")

    def t_name_pic():
        name = pick(["triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"])
        return {"prompt": "What is the name of this shape?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is %s." % _a(name)]}

    def t_total_sides():
        a, b = random.sample([("triangle", 3), ("square", 4), ("pentagon", 5), ("hexagon", 6)], 2)
        return _tb("How many sides do a %s and a %s have altogether?" % (a[0], b[0]), a[1] + b[1], "int", {},
                   ["%d + %d = %d." % (a[1], b[1], a[1] + b[1])])

    def t_rect_vs_square():
        return _wq("A shape has 4 straight sides. Two are long and two are short. Is it a square or a rectangle?", "rectangle",
                   ["A square has 4 sides the same length."], "square / rectangle")

    def t_same_sides():
        n = random.randint(3, 8)
        return _tb("A shape has %d corners. How many sides does it have?" % n, n, "int", {},
                   ["A flat shape with straight sides has as many sides as corners."])

    return _pick_t([t_name, t_symmetry, t_count_four, t_curved, t_total_sides, t_rect_vs_square, t_same_sides],
                   [t_sides, t_vertices, t_name_pic])


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
                "solution": ["%s × %d = %d." % (_pn(vals[k] // key, "symbol"), key, vals[k])]}

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

    def t_read_tally():
        v = random.randint(3, 19)
        return _tb("How many does this tally show?  %s" % _tally(v), v, "int", {}, ["Each bundle is 5: %d." % v])

    def t_total():
        vals = [random.randint(1, 8) for _ in cats]
        return {"prompt": "Each symbol stands for 1. How many fruits were chosen altogether?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"}, "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(map(str, vals)), sum(vals))]}

    def t_diff():
        vals = random.sample(range(1, 10), 4)
        i, j = random.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        key = pick([1, 2]) if d else 1
        vv = [v * key for v in vals]
        return {"prompt": "Each symbol stands for %d. How many more chose %s than %s?" % (key, cats[i].lower(), cats[j].lower()),
                "component": "pictogram", "spec": {"categories": cats, "values": vv, "key": key, "symbol": "circle"},
                "answer": vv[i] - vv[j], "answer_type": "int", "solution": ["%d − %d = %d." % (vv[i], vv[j], vv[i] - vv[j])]}

    def t_half_symbol():
        vals = [2 * random.randint(1, 5) - pick([0, 1]) for _ in cats]
        k = random.randrange(4)
        return {"prompt": "Each whole symbol stands for 2. Half a symbol stands for 1. How many %s?" % cats[k].lower(),
                "component": "pictogram", "spec": {"categories": cats, "values": vals, "key": 2, "symbol": "circle"},
                "answer": vals[k], "answer_type": "int", "solution": ["%d." % vals[k]]}

    def t_least():
        vals = random.sample(range(1, 10), 4)
        return {"prompt": "Which fruit was chosen the least?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"}, "answer": cats[vals.index(min(vals))],
                "answer_type": "str", "solution": ["%s has the fewest symbols." % cats[vals.index(min(vals))]]}

    def t_tally_more():
        vals = random.sample(range(2, 15), 4)
        i, j = random.sample(range(4), 2)
        rows = [[c, _tally(v)] for c, v in zip(cats, vals)]
        return _dt("The tally chart shows favourite fruit. How many more chose %s than %s?" % (cats[i].lower(), cats[j].lower())
                   if vals[i] > vals[j] else "The tally chart shows favourite fruit. How many fewer chose %s than %s?" % (cats[i].lower(), cats[j].lower()),
                   ["Fruit", "Tally"], rows, abs(vals[i] - vals[j]),
                   ["%s: %d, %s: %d; the difference is %d." % (cats[i], vals[i], cats[j], vals[j], abs(vals[i] - vals[j]))])

    def t_order():
        vals = random.sample(range(1, 10), 4)
        k = random.randint(1, 4)
        return {"prompt": "Put the fruits in order, most popular first. Which fruit is number %d?" % k, "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": [c for _, c in sorted(zip(vals, cats), reverse=True)][k - 1], "answer_type": "str",
                "solution": ["Order: %s." % ", ".join(c for _, c in sorted(zip(vals, cats), reverse=True))]}

    return _pick_t([t_read_tally], [t_pictogram, t_tally, t_most, t_total, t_diff, t_half_symbol, t_least, t_tally_more, t_order])


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
