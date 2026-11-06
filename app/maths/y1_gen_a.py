# Year 1 generators (National Curriculum, Year 1 programme of study).
#
# Short prompts for young readers, leaning on pictures: counting and numbers to 100, number bonds,
# adding and subtracting within 20, equal groups and sharing, halves and quarters, measures, coins
# and notes, days and months, o'clock and half past, 2-D and 3-D shapes, turns and position.
from .maths_engine import skill, n_words
from .y5_common import *  # noqa: F401,F403

S0 = "1.0 Counting & place value"
S1 = "1.1 Addition & subtraction"
S2 = "1.2 Multiplication & division"
S3 = "1.3 Fractions"
S4 = "1.4 Measurement"
S5 = "1.5 Shape, position & direction"

KIDS = ["Sam", "Mia", "Ben", "Ava", "Leo", "Isla", "Jay", "Zoe"]
THINGS = [("apples", "apple"), ("cars", "car"), ("stars", "star"), ("sweets", "sweet"), ("books", "book"), ("shells", "shell")]


def _kid():
    return pick(KIDS)


def _pn(k, one, many=None):
    """3 -> '3 dots', 1 -> '1 dot'."""
    return "%d %s" % (k, one if k == 1 else (many or one + "s"))


def _to(n):
    """47 -> '4 tens and 7 ones'; 11 -> '1 ten and 1 one'."""
    return "%s and %s" % (_pn(n // 10, "ten"), _pn(n % 10, "one"))


# ================================================================== 1.0 ======
@skill("Y1.0.a", "Count forwards and backwards to 100", S0)
def _(d=1):
    d = _d(d)
    start = random.randint(_by(d, 0, 10, 40), _by(d, 15, 60, 95))
    back = random.random() < 0.4 and start > 5

    def t_next():
        s = [start - i if back else start + i for i in range(3)]
        return _tb("What comes next?  %s, ___" % ", ".join(map(str, s)), s[-1] + (-1 if back else 1), "int", {},
                   ["Count %s one." % ("back" if back else "on")])

    def t_missing():
        s = [start + i for i in range(5)]
        k = random.randint(1, 3)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == k else str(v) for i, v in enumerate(s)), s[k],
                   "int", {}, ["Count on in ones."])

    def t_across_ten():
        t = random.randint(1, 9) * 10
        return _tb("Count on:  %d, %d, %d, ___" % (t - 3, t - 2, t - 1), t, "int", {}, ["After %d comes %d." % (t - 1, t)])

    def t_line():
        n = random.randint(0, _by(d, 20, 50, 100))
        lo = (n // 10) * 10
        return _nl("Put %d on the number line." % n, n, 1, 5, ["Count along from %d." % lo], lo=lo, hi=lo + 10)

    def t_before():
        n = random.randint(2, _by(d, 20, 60, 100))
        return _tb("Which number comes just before %d?" % n, n - 1, "int", {}, ["Count back one: %d." % (n - 1)])

    def t_after():
        n = random.randint(0, _by(d, 19, 59, 99))
        return _tb("Which number comes just after %d?" % n, n + 1, "int", {}, ["Count on one: %d." % (n + 1)])

    def t_between():
        n = random.randint(1, _by(d, 19, 59, 99))
        return _tb("Which number is between %d and %d?" % (n - 1, n + 1), n, "int", {}, ["%d, %d, %d." % (n - 1, n, n + 1)])

    def t_missing_back():
        s = [start + 4 - i for i in range(5)]
        k = random.randint(1, 3)
        return _tb("Count back. Find the missing number:  %s" % ", ".join("___" if i == k else str(v) for i, v in enumerate(s)),
                   s[k], "int", {}, ["Count back in ones."])

    def t_count_on():
        k = random.randint(2, 5)
        return _tb("Start at %d. Count on %d. Where do you stop?" % (start, k), start + k, "int", {},
                   ["%s." % ", ".join(str(start + i) for i in range(1, k + 1))])

    def t_count_back():
        n = random.randint(6, _by(d, 20, 60, 100))
        k = random.randint(2, 5)
        return _tb("Start at %d. Count back %d. Where do you stop?" % (n, k), n - k, "int", {},
                   ["%s." % ", ".join(str(n - i) for i in range(1, k + 1))])

    def t_to_100():
        n = random.randint(94, 97) if d == 2 else random.randint(36, 89)
        return _tb("Count on:  %d, %d, %d, ___" % (n, n + 1, n + 2), n + 3, "int", {}, ["After %d comes %d." % (n + 2, n + 3)])

    def t_line_back():
        n = random.randint(3, _by(d, 20, 50, 100))
        lo = max(0, ((n - 3) // 10) * 10)
        return _nl("Start at %d and count back 3. Mark where you stop." % n, n - 3, 1, 5, ["%d, %d, %d." % (n - 1, n - 2, n - 3)],
                   lo=lo, hi=lo + 10 if n <= lo + 10 else lo + 20)

    return _pick_t([t_next, t_missing, t_across_ten, t_before, t_after, t_between, t_missing_back, t_count_on, t_count_back,
                    t_to_100], [t_line, t_line_back])


@skill("Y1.0.b", "Read and write numbers to 20 in words", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(0 if d else 1, _by(d, 10, 20, 20))

    def t_word_to_num():
        return _tb("Write this number in digits: %s" % n_words(n), n, "int", {}, ["%s is %d." % (n_words(n), n)])

    def t_num_to_word():
        return _wq("Write %d in words." % n, n_words(n), ["%d is %s." % (n, n_words(n))], "word")

    def t_count_objects():
        k = random.randint(2, 10)
        return {"prompt": "How many counters are there altogether?", "component": "equal_groups",
                "spec": {"mode": "read", "groups": 1, "per": k}, "answer": k, "answer_type": "int",
                "solution": ["Count them: %d." % k]}

    def t_blocks():
        return {"prompt": "Make %s with the blocks." % n_words(n), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": n, "answer_type": "int",
                "solution": ["%s is %s." % (n_words(n), _to(n))]}

    return _pick_t([t_word_to_num, t_num_to_word, t_word_to_num, t_num_to_word, t_count_objects], [t_blocks])


@skill("Y1.0.c", "Count in twos, fives and tens", S0)
def _(d=1):
    d = _d(d)
    step = pick(_by(d, [2, 10], [2, 5, 10], [2, 5, 10]))
    k = random.randint(2, _by(d, 6, 8, 10))

    def t_next():
        s = [step * i for i in range(k - 2, k + 1)]
        return _tb("Count in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] + step, "int", {},
                   ["Add %d." % step])

    def t_missing():
        s = [step * i for i in range(1, 6)]
        j = random.randint(1, 3)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == j else str(v) for i, v in enumerate(s)), s[j],
                   "int", {}, ["Count in %ss." % step])

    def t_groups():
        return {"prompt": "There are %d groups of %d. Count in %ss. How many altogether?" % (k, step, step),
                "component": "equal_groups", "spec": {"mode": "read", "groups": k, "per": step}, "answer": k * step,
                "answer_type": "int", "solution": ["%s." % ", ".join(str(step * i) for i in range(1, k + 1))]}

    def t_socks():
        return _tb("How many socks are in %d pairs? Count in 2s." % k, 2 * k, "int", {}, ["%s." % ", ".join(str(2 * i) for i in range(1, k + 1))])

    def t_line():
        return _nl("Start at 0 and make %d jumps of %d. Where do you land?" % (k, step), k * step, step, 10,
                   ["%d jumps of %d is %d." % (k, step, k * step)], lo=0, hi=max(20, (k * step // 10 + 1) * 10))

    def t_back():
        s = [step * i for i in range(k + 1, k - 2, -1)]
        return _tb("Count back in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] - step, "int", {}, ["Take away %d." % step])

    def t_hands():
        return _tb("How many fingers are on %d hands? Count in 5s." % k, 5 * k, "int", {},
                   ["%s." % ", ".join(str(5 * i) for i in range(1, k + 1))])

    def t_coins():
        c = pick([2, 5, 10])
        return _tb("%s has %d %dp coins. How many pence is that? Count in %ss." % (_kid(), k, c, c), k * c, "int", {"unit": "p"},
                   ["%s." % ", ".join(str(c * i) for i in range(1, k + 1))])

    def t_sticks():
        return _tb("There are %d bundles of 10 sticks. How many sticks? Count in 10s." % k, 10 * k, "int", {},
                   ["%s." % ", ".join(str(10 * i) for i in range(1, k + 1))])

    def t_how_many_jumps():
        return _tb("How many jumps of %d take you from 0 to %d?" % (step, k * step), k, "int", {},
                   ["%s: %d jumps." % (", ".join(str(step * i) for i in range(1, k + 1)), k)])

    def t_in_list():
        n = step * random.randint(1, 10) + pick([0, 1])
        yes = n % step == 0
        return _wq("Do you say %d when you count in %ss from 0? (yes or no)" % (n, step), "yes" if yes else "no",
                   ["Counting in %ss: %s." % (step, ", ".join(str(step * i) for i in range(1, 11)))], "yes / no")

    return _pick_t([t_next, t_missing, t_socks, t_back, t_hands, t_coins, t_sticks, t_how_many_jumps, t_in_list],
                   [t_groups, t_line])


@skill("Y1.0.d", "One more and one less", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(1, _by(d, 19, 50, 99))

    def t_more():
        return _tb("What is one more than %d?" % n, n + 1, "int", {}, ["%d + 1 = %d." % (n, n + 1)])

    def t_less():
        return _tb("What is one less than %d?" % n, n - 1, "int", {}, ["%d − 1 = %d." % (n, n - 1)])

    def t_word():
        kid = _kid()
        t = pick(THINGS)
        return _tb("%s has %d %s. %s gets one more. How many now?" % (kid, n, t[1] if n == 1 else t[0], kid), n + 1, "int", {},
                   ["One more than %d is %d." % (n, n + 1)])

    def t_blocks():
        m = min(n, 98)
        return {"prompt": "Make the number that is one more than %d." % m, "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": m + 1, "answer_type": "int", "solution": ["%d." % (m + 1)]}

    return _pick_t([t_more, t_less, t_word], [t_blocks])


@skill("Y1.0.e", "Compare numbers: more, less, most, least", S0)
def _(d=1):
    d = _d(d)
    a, b = random.sample(range(1, _by(d, 20, 50, 100)), 2)

    def t_more():
        return _tb("Which is more, %d or %d?" % (a, b), max(a, b), "int", {}, ["%d is more." % max(a, b)])

    def t_less():
        return _tb("Which is less, %d or %d?" % (a, b), min(a, b), "int", {}, ["%d is less." % min(a, b)])

    def t_most():
        vals = random.sample(range(1, 30), 3)
        kids = random.sample(KIDS, 3)
        return _wq("%s has %s, %s has %d and %s has %d. Who has the most?" % (kids[0], _pn(vals[0], "sticker"), kids[1], vals[1],
                                                                                      kids[2], vals[2]),
                   kids[vals.index(max(vals))], ["%d is the biggest number." % max(vals)], "name")

    def t_fewer():
        vals = random.sample(range(1, 20), 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s has %s. %s has %s. Who has fewer?" % (kids[0], _pn(vals[0], "marble"), kids[1], _pn(vals[1], "marble")),
                   kids[vals.index(min(vals))], ["%d is less than %d." % (min(vals), max(vals))], "name")

    def t_pictogram():
        cats = random.sample(["Cats", "Dogs", "Fish", "Birds"], 3)
        vals = random.sample(range(1, 9), 3)
        return {"prompt": "Which pet is the most popular?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": cats[vals.index(max(vals))], "answer_type": "str",
                "solution": ["%s has the most: %d." % (cats[vals.index(max(vals))], max(vals))]}

    return _pick_t([t_more, t_less, t_most, t_fewer], [t_pictogram])


@skill("Y1.0.f", "Tens and ones to 100", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(11, _by(d, 30, 70, 99))

    def t_tens():
        return _tb("How many tens are in %d?" % n, n // 10, "int", {}, ["%d = %s." % (n, _to(n))])

    def t_ones():
        return _tb("How many ones are in %d?" % n, n % 10, "int", {}, ["%d = %s." % (n, _to(n))])

    def t_build():
        return {"prompt": "Make %d with tens and ones." % n, "component": "base_ten", "spec": {"mode": "build", "max": 9},
                "answer": n, "answer_type": "int", "solution": ["%s." % _to(n)]}

    def t_from_parts():
        return _tb("%s make what number?" % _to(n), n, "int", {}, ["%d." % n])

    def t_partition():
        return _tb("%d = %d + ___" % (n, (n // 10) * 10), n % 10, "int", {}, ["%s is %d, so the rest is %d." % (_pn(n // 10, "ten"), (n // 10) * 10, n % 10)])

    def t_bundles():
        return _tb("%s has %s of 10 straws and %s. How many straws?" % (_kid(), _pn(n // 10, "bundle"), _pn(n % 10, "loose straw")), n, "int", {},
                   ["%s is %d." % (_to(n), n)])

    def t_ten_more():
        m = random.randint(11, 89)
        return _tb("What is 10 more than %d?" % m, m + 10, "int", {}, ["The tens digit goes up by one: %d." % (m + 10)])

    def t_ten_less():
        m = random.randint(11, 99)
        return _tb("What is 10 less than %d?" % m, m - 10, "int", {}, ["The tens digit goes down by one: %d." % (m - 10)])

    def t_line():
        return _nl("Put %d on the number line." % n, n, 1, 10, ["%s." % _to(n)], lo=0, hi=100)

    def t_bigger():
        a, b = random.sample(range(11, 100), 2)
        while a // 10 == b // 10:
            a, b = random.sample(range(11, 100), 2)
        return _tb("Which is bigger, %d or %d? Look at the tens." % (a, b), max(a, b), "int", {},
                   ["%d has more tens." % max(a, b)])

    def t_tens_only():
        t = random.randint(1, 10)
        return _tb("What number is %s?" % _pn(t, "ten"), 10 * t, "int", {}, ["%s = %d." % (_pn(t, "ten"), 10 * t)])

    return _pick_t([t_tens, t_ones, t_from_parts, t_partition, t_bundles, t_ten_more, t_ten_less, t_bigger, t_tens_only],
                   [t_build, t_line])


# ================================================================== 1.1 ======
@skill("Y1.1.a", "Number bonds to 10", S1)
def _(d=1):
    d = _d(d)
    a = random.randint(0, 10)

    def t_missing():
        return _tb("%d + ___ = 10" % a, 10 - a, "int", {}, ["%d and %d make 10." % (a, 10 - a)])

    def t_take():
        return _tb("10 − %d = ___" % a, 10 - a, "int", {}, ["%d + %d = 10." % (a, 10 - a)])

    def t_word():
        kid = _kid()
        return _tb("%s has 10 sweets and eats %d. How many are left?" % (kid, a), 10 - a, "int", {}, ["10 − %d = %d." % (a, 10 - a)])

    def t_partner():
        return _tb("Which number goes with %d to make 10?" % a, 10 - a, "int", {}, ["%d + %d = 10." % (a, 10 - a)])

    def t_left_missing():
        return _tb("___ + %d = 10" % a, 10 - a, "int", {}, ["%d and %d make 10." % (10 - a, a)])

    def t_frame():
        return _tb("A ten frame has %s. How many empty spaces are there?" % _pn(a, "dot"), 10 - a, "int", {},
                   ["A ten frame has 10 spaces: 10 − %d = %d." % (a, 10 - a)])

    def t_bar():
        return _strip("The whole is 10. One part is %d. What is the other part?" % a,
                      {"mode": "part_whole", "totalLabel": "10", "partLabel": str(a), "unknown": "part", "parts": 2}, 10 - a,
                      ["10 − %d = %d." % (a, 10 - a)])

    def t_line():
        return _nl("Which number goes with %d to make 10? Mark it on the number line." % a, 10 - a, 1, 5,
                   ["%d + %d = 10." % (a, 10 - a)], lo=0, hi=10)

    def t_sub_missing():
        return _tb("10 − ___ = %d" % a, 10 - a, "int", {}, ["10 − %d = %d." % (10 - a, a)])

    def t_pencils():
        return _tb("A box holds 10 pencils. It has %d in it. How many more will fill it?" % a, 10 - a, "int", {},
                   ["%d + %d = 10." % (a, 10 - a)])

    def t_ten_equals():
        return _tb("10 = %d + ___" % a, 10 - a, "int", {}, ["%d and %d make 10." % (a, 10 - a)])

    return _pick_t([t_missing, t_take, t_word, t_partner, t_left_missing, t_frame, t_sub_missing, t_pencils, t_ten_equals],
                   [t_bar, t_line])


@skill("Y1.1.b", "Number bonds and facts within 20", S1)
def _(d=1):
    d = _d(d)
    tot = random.randint(_by(d, 11, 12, 15), 20)
    a = random.randint(1, tot - 1)

    def t_missing():
        return _tb("%d + ___ = %d" % (a, tot), tot - a, "int", {}, ["%d − %d = %d." % (tot, a, tot - a)])

    def t_sub():
        return _tb("%d − %d = ___" % (tot, a), tot - a, "int", {}, ["%d + %d = %d." % (a, tot - a, tot)])

    def t_related():
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        return _tb("%d + %d = %d. So what is %d − %d?" % (b, c, b + c, b + c, c), b, "int", {}, ["It undoes the adding."])

    def t_double():
        k = random.randint(1, 10)
        return _tb("Double %d is ___" % k, 2 * k, "int", {}, ["%d + %d = %d." % (k, k, 2 * k)])

    def t_ten_plus():
        k = random.randint(1, 9)
        return _tb("10 + %d = ___" % k, 10 + k, "int", {}, ["Ten and %s is %d." % (_pn(k, "one"), 10 + k)])

    def t_bond20():
        k = random.randint(1, 19)
        return _tb("%d + ___ = 20" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])

    def t_near_double():
        k = random.randint(2, 9)
        return _tb("Double %d is %d. So what is %d + %d?" % (k, 2 * k, k, k + 1), 2 * k + 1, "int", {},
                   ["%d + %d is one more than double %d: %d." % (k, k + 1, k, 2 * k + 1)])

    def t_family():
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        return _tb("%d + %d = %d. So what is %d − %d?" % (b, c, b + c, b + c, b), c, "int", {},
                   ["Take away the %d you added: %d." % (b, c)])

    def t_halve():
        k = random.randint(1, 10)
        return _tb("%d − %d = ___" % (2 * k, k), k, "int", {}, ["Half of %d is %d." % (2 * k, k)])

    def t_bar():
        return _strip("The whole is %d. One part is %d. What is the other part?" % (tot, a),
                      {"mode": "part_whole", "totalLabel": str(tot), "partLabel": str(a), "unknown": "part", "parts": 2}, tot - a,
                      ["%d − %d = %d." % (tot, a, tot - a)])

    def t_teen_sub():
        k = random.randint(1, 9)
        return _tb("1%d − %d = ___" % (k, k), 10, "int", {}, ["Take away the ones: 10 is left."]) if random.random() < 0.5 else \
            _tb("1%d − 10 = ___" % k, k, "int", {}, ["Take away the ten: %d is left." % k])

    def t_story():
        kid = _kid()
        return _tb("%s has %s. %s needs %d pens. How many more pens does %s need?" % (kid, _pn(a, "pen"), kid, tot, kid), tot - a, "int", {},
                   ["%d + ___ = %d, so %d." % (a, tot, tot - a)])

    def t_line():
        return _nl("Start at %d. Jump on %d. Where do you land?" % (a, tot - a), tot, 1, 5, ["%d + %d = %d." % (a, tot - a, tot)],
                   lo=0, hi=20)

    def t_true():
        shown = pick([tot - a, tot - a, tot - a + 1, tot - a - 1 if tot - a > 1 else tot - a + 2])
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (a, shown, tot), "yes" if a + shown == tot else "no",
                   ["%d + %d = %d." % (a, tot - a, tot)], "yes / no")

    def t_dominoes():
        x, y = random.randint(1, 6), random.randint(1, 6)
        return _tb("A domino has %s on one side and %d on the other. How many spots altogether?" % (_pn(x, "spot"), y), x + y, "int", {},
                   ["%d + %d = %d." % (x, y, x + y)])

    def t_how_many_fewer():
        return _tb("There are %d cats and %s. How many fewer dogs than cats?" % (tot, _pn(a, "dog")), tot - a, "int", {},
                   ["%d − %d = %d." % (tot, a, tot - a)])

    return _pick_t([t_missing, t_sub, t_related, t_double, t_ten_plus, t_bond20, t_near_double, t_family, t_halve, t_teen_sub,
                    t_story, t_true, t_dominoes, t_how_many_fewer], [t_bar, t_line])


@skill("Y1.1.c", "Add and subtract within 20", S1)
def _(d=1):
    d = _d(d)
    a = random.randint(1, _by(d, 10, 15, 19))
    b = random.randint(1, 20 - a)

    def t_add():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["Count on %d from %d." % (b, a)])

    def t_sub():
        x = a + b
        return _tb("%d − %d = ___" % (x, b), a, "int", {}, ["Count back %d from %d." % (b, x)])

    def t_line_add():
        return _nl("Start at %d and jump on %d. Where do you land?" % (a, b), a + b, 1, 5, ["%d + %d = %d." % (a, b, a + b)],
                   lo=0, hi=20)

    def t_line_sub():
        x = a + b
        return _nl("Start at %d and jump back %d. Where do you land?" % (x, b), a, 1, 5, ["%d − %d = %d." % (x, b, a)],
                   lo=0, hi=20)

    def t_zero():
        k = random.randint(1, 20)
        return _tb("%d + 0 = ___" % k if random.random() < 0.5 else "%d − 0 = ___" % k, k, "int", {},
                   ["Adding or taking away 0 changes nothing."])

    def t_cross_ten():
        x = random.randint(6, 9)
        y = random.randint(11 - x, 9)
        return _tb("%d + %d = ___" % (x, y), x + y, "int", {}, ["%d + %d makes 10, then %d more: %d." % (x, 10 - x, y - (10 - x), x + y)])

    def t_teen_add():
        k = random.randint(1, 8)
        m = random.randint(1, 9 - k)
        return _tb("1%d + %d = ___" % (k, m), 10 + k + m, "int", {}, ["%d + %d = %d, so 1%d + %d = %d." % (k, m, k + m, k, m, 10 + k + m)])

    def t_teen_sub():
        k = random.randint(2, 9)
        m = random.randint(1, k)
        return _tb("1%d − %d = ___" % (k, m), 10 + k - m, "int", {}, ["%d − %d = %d, so 1%d − %d = %d." % (k, m, k - m, k, m, 10 + k - m)])

    def t_more_sum():
        x, y = random.randint(2, 9), random.randint(2, 9)
        p, q = random.randint(2, 9), random.randint(2, 9)
        while x + y == p + q:
            p, q = random.randint(2, 9), random.randint(2, 9)
        return _tb("Which is more, %d + %d or %d + %d? Type the bigger answer." % (x, y, p, q), max(x + y, p + q), "int", {},
                   ["%d + %d = %d and %d + %d = %d." % (x, y, x + y, p, q, p + q)])

    def t_add_three():
        x, y, z = random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
        return _tb("%d + %d + %d = ___" % (x, y, z), x + y + z, "int", {}, ["%d + %d = %d, then + %d = %d." % (x, y, x + y, z, x + y + z)])

    def t_count_all():
        return {"prompt": "Count all the counters. %d + %d = ___" % (a, b), "component": "equal_groups",
                "spec": {"mode": "read", "groups": 1, "per": a + b}, "answer": a + b, "answer_type": "int",
                "solution": ["%d and %d more make %d." % (a, b, a + b)]} if 0 < a + b <= 20 and b > 0 else t_add()

    def t_add_word():
        kid = _kid()
        return _tb("%s has %s and wins %d more. How many marbles now?" % (kid, _pn(a, "marble"), b), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)])

    def t_sub_word():
        return _tb("There are %d birds on a wall. %d fly away. How many are left?" % (a + b, b), a, "int", {},
                   ["%d − %d = %d." % (a + b, b, a)])

    def t_take_bar():
        return _strip("There are %d children. %s. How many are boys?" % (a + b, "1 is a girl" if b == 1 else "%d are girls" % b),
                      {"mode": "part_whole", "totalLabel": str(a + b), "partLabel": str(b), "unknown": "part", "parts": 2}, a,
                      ["%d − %d = %d." % (a + b, b, a)]) if b > 0 else t_add()

    def t_which_sum():
        return _tb("%d + %d = %d. What is %d + %d?" % (a, b, a + b, b, a), a + b, "int", {}, ["Adding in any order gives the same answer."])

    def t_steps():
        return _tb("A frog is on step %d. It hops up %s. Which step is it on now?" % (a, _pn(b, "step")), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)])

    return _pick_t([t_add, t_sub, t_zero, t_cross_ten, t_teen_add, t_teen_sub, t_more_sum, t_add_three, t_add_word, t_sub_word,
                    t_which_sum, t_steps], [t_line_add, t_line_sub, t_count_all, t_take_bar])


@skill("Y1.1.d", "Missing numbers and the = sign", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(1, 10), random.randint(1, 9)

    def t_left():
        return _tb("___ + %d = %d" % (b, a + b), a, "int", {}, ["%d − %d = %d." % (a + b, b, a)])

    def t_sub_missing():
        return _tb("%d = ___ − %d" % (a, b), a + b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_true():
        right = a + b
        shown = pick([right, right + 1, right - 1])
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (a, b, shown), "yes" if shown == right else "no",
                   ["%d + %d = %d." % (a, b, right)], "yes / no")

    def t_sign():
        return _wq("Which sign goes in the gap, + or −?  %d ___ %d = %d" % (a + b, b, a), "−",
                   ["%d take away %d is %d." % (a + b, b, a)], "+ or −") if random.random() < 0.5 else \
            _wq("Which sign goes in the gap, + or −?  %d ___ %d = %d" % (a, b, a + b), "+", ["%d add %d is %d." % (a, b, a + b)],
                "+ or −")

    def t_nc_style():
        return _tb("___ − %d = %d" % (b, a), a + b, "int", {}, ["What number take away %d leaves %d? %d + %d = %d." % (b, a, a, b, a + b)])

    def t_both_sides():
        c = random.randint(1, a + b - 1)
        return _tb("%d + %d = %d + ___" % (a, b, c), a + b - c, "int", {},
                   ["Both sides make %d. %d − %d = %d." % (a + b, a + b, c, a + b - c)])

    def t_sub_gap():
        return _tb("%d − ___ = %d" % (a + b, a), b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_right_side():
        return _tb("___ = %d + %d" % (a, b), a + b, "int", {}, ["The = sign means both sides are the same: %d." % (a + b)])

    def t_true_sub():
        right = a
        shown = pick([right, right + 1, right - 1 if right > 1 else right + 2])
        return _wq("Is this true?  %d − %d = %d  (yes or no)" % (a + b, b, shown), "yes" if shown == right else "no",
                   ["%d − %d = %d." % (a + b, b, right)], "yes / no")

    def t_mystery():
        return _tb("I think of a number. I add %d and get %d. What is my number?" % (b, a + b), a, "int", {},
                   ["%d − %d = %d." % (a + b, b, a)])

    def t_balance():
        return _tb("%d + ___ = %d + %d" % (b, a, b), a, "int", {}, ["The same numbers in any order: %d." % a])

    def t_bar_missing():
        return _strip("The whole is %d. One part is %d. What is the missing part?" % (a + b, b),
                      {"mode": "part_whole", "totalLabel": str(a + b), "partLabel": str(b), "unknown": "part", "parts": 2}, a,
                      ["%d + ___ = %d, so %d." % (b, a + b, a)])

    def t_line_missing():
        return _nl("%d + ___ = %d. Mark the missing number on the number line." % (b, a + b), a, 1, 5,
                   ["%d − %d = %d." % (a + b, b, a)], lo=0, hi=10)

    def t_bag():
        return _tb("A bag had some sweets. %s put in %d more. Now there are %d. How many were in the bag at first?" % (_kid(), b, a + b),
                   a, "int", {}, ["___ + %d = %d, so %d." % (b, a + b, a)])

    return _pick_t([t_left, t_sub_missing, t_true, t_sign, t_nc_style, t_both_sides, t_sub_gap, t_right_side, t_true_sub,
                    t_mystery, t_balance, t_bag], [t_bar_missing, t_line_missing])


@skill("Y1.1.e", "Addition and subtraction word problems", S1)
def _(d=1):
    d = _d(d)
    kid = _kid()
    t = pick(THINGS)
    a, b = random.randint(2, 12), random.randint(1, 8)

    def t_add():
        return _tb("%s has %d %s. %s finds %d more. How many %s now?" % (kid, a, t[0], kid, b, t[0]), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)])

    def t_sub():
        return _tb("%s has %d %s and gives away %d. How many are left?" % (kid, a + b, t[0], b), a, "int", {},
                   ["%d − %d = %d." % (a + b, b, a)])

    def t_difference():
        other = pick([k for k in KIDS if k != kid])
        return _tb("%s has %d %s. %s has %d. How many more does %s have?" % (kid, a + b, t[0], other, a, kid), b, "int", {},
                   ["%d − %d = %d." % (a + b, a, b)])

    def t_bus():
        on, off = random.randint(5, 12), random.randint(1, 5)
        return _tb("%d people are on a bus. %d %s off. How many are on the bus now?" % (on, off, "gets" if off == 1 else "get"), on - off, "int", {},
                   ["%d − %d = %d." % (on, off, on - off)])

    def t_groups():
        return {"prompt": "There are %d %s in one bag and %d in another. How many altogether?" % (a, t[0], b),
                "component": "equal_groups", "spec": {"mode": "read", "groups": 1, "per": a + b}, "answer": a + b,
                "answer_type": "int", "solution": ["%d + %d = %d." % (a, b, a + b)]}

    return _pick_t([t_add, t_sub, t_difference, t_bus], [t_groups])


# ================================================================== 1.2 ======
@skill("Y1.2.a", "Equal groups and arrays", S2)
def _(d=1):
    d = _d(d)
    g, p = random.randint(2, 5), pick([2, 5, 10]) if d else pick([2, 10])

    def t_groups():
        return {"prompt": "How many altogether? There are %d groups of %d." % (g, p), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": p}, "answer": g * p, "answer_type": "int",
                "solution": ["Count in %ds: %d." % (p, g * p)]}

    def t_array():
        return {"prompt": "Make an array with %d rows of %d. How many dots?" % (g, p), "component": "array",
                "spec": {"mode": "build", "maxRows": 6, "maxCols": 10, "targetRows": g, "targetCols": p},
                "answer": g * p, "answer_type": "int", "solution": ["%d rows of %d is %d." % (g, p, g * p)]}

    def t_word():
        return _tb("There are %d plates. Each plate has %d biscuits. How many biscuits altogether?" % (g, p), g * p, "int", {},
                   ["Count in %ds: %d." % (p, g * p)])

    def t_legs():
        n, legs, what = pick([(random.randint(2, 6), 2, "birds"), (random.randint(2, 5), 4, "dogs")])
        return _tb("How many legs do %d %s have?" % (n, what), n * legs, "int", {}, ["%d lots of %d = %d." % (n, legs, n * legs)])

    def t_wheels():
        n = random.randint(2, 5)
        what, w = pick([("bikes", 2), ("cars", 4)])
        return _tb("How many wheels are on %d %s?" % (n, what), n * w, "int", {}, ["Count in %ds: %d." % (w, n * w)])

    def t_shoes():
        n = random.randint(2, 10)
        return _tb("%d children each wear a pair of shoes. How many shoes is that?" % n, 2 * n, "int", {},
                   ["Count in 2s: %d." % (2 * n)])

    def t_boxes():
        n = random.randint(2, 6)
        return _tb("There are %d boxes. Each box has 10 pencils. How many pencils?" % n, 10 * n, "int", {},
                   ["Count in 10s: %d." % (10 * n)])

    def t_groups_count():
        return {"prompt": "How many groups are there?", "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": p}, "answer": g, "answer_type": "int",
                "solution": ["There are %d groups of %d." % (g, p)]}

    def t_double():
        k = random.randint(1, 10)
        return _tb("Double %d. How many is 2 groups of %d?" % (k, k), 2 * k, "int", {}, ["%d + %d = %d." % (k, k, 2 * k)])

    def t_bar():
        return _strip("There are %d bags with %d sweets in each. How many sweets?" % (g, p),
                      {"mode": "equal_parts", "parts": g, "partLabel": str(p), "totalLabel": "?", "unknown": "total"}, g * p,
                      ["Count in %ds: %d." % (p, g * p)])

    def t_rows():
        return _tb("Chairs are put in %d rows with %d chairs in each row. How many chairs?" % (g, p), g * p, "int", {},
                   ["%d rows of %d is %d." % (g, p, g * p)])

    return _pick_t([t_word, t_legs, t_wheels, t_shoes, t_boxes, t_double, t_rows], [t_groups, t_array, t_groups_count, t_bar])


@skill("Y1.2.b", "Sharing and grouping", S2)
def _(d=1):
    d = _d(d)
    k, each = random.randint(2, 5), random.randint(2, 5)

    def t_share():
        return _tb("%d sweets are shared equally between %d children. How many does each child get?" % (k * each, k), each,
                   "int", {}, ["%d shared into %d groups is %d each." % (k * each, k, each)])

    def t_group():
        return _tb("%d eggs go in boxes of %d. How many boxes?" % (k * each, each), k, "int", {},
                   ["Make groups of %d: %d groups." % (each, k)])

    def t_half():
        n = 2 * random.randint(1, 10)
        return _tb("Half of %d is ___" % n, n // 2, "int", {}, ["Share %d into 2 equal groups: %d." % (n, n // 2)])

    def t_pic():
        return {"prompt": "%d counters are shared into %d equal groups. How many in each group?" % (k * each, k),
                "component": "equal_groups", "spec": {"mode": "read", "groups": k, "per": each}, "answer": each,
                "answer_type": "int", "solution": ["Each group has %d." % each]}

    def t_fair():
        n = random.randint(5, 16)
        return _wq("Can %d sweets be shared fairly between 2 children? (yes or no)" % n, "yes" if n % 2 == 0 else "no",
                   ["%s" % ("Each gets %d." % (n // 2) if n % 2 == 0 else "One would be left over.")], "yes / no")

    def t_how_many_groups():
        return {"prompt": "%d counters are put in groups of %d. How many groups are there?" % (k * each, each),
                "component": "equal_groups", "spec": {"mode": "read", "groups": k, "per": each}, "answer": k,
                "answer_type": "int", "solution": ["There are %d groups of %d." % (k, each)]}

    def t_strip():
        return _strip("%d stickers are shared equally into %d pages. How many on each page?" % (k * each, k),
                      {"mode": "equal_parts", "parts": k, "partLabel": "?", "totalLabel": str(k * each), "unknown": "part"}, each,
                      ["%d shared into %d is %d each." % (k * each, k, each)])

    def t_tens():
        n = random.randint(2, 5)
        return _tb("%d pencils go into packs of 10. How many packs?" % (10 * n), n, "int", {}, ["Count in 10s: %d packs." % n])

    def t_pairs():
        n = random.randint(2, 10)
        return _tb("%d socks are put into pairs. How many pairs?" % (2 * n), n, "int", {}, ["Count in 2s: %d pairs." % n])

    def t_fives():
        n = random.randint(2, 6)
        return _tb("%d flowers go into vases of 5. How many vases?" % (5 * n), n, "int", {}, ["Count in 5s: %d vases." % n])

    def t_plates():
        return _tb("%s puts %d cakes onto %d plates, the same on each plate. How many cakes on each plate?" % (_kid(), k * each, k),
                   each, "int", {}, ["Share them out one at a time: %d each." % each])

    return _pick_t([t_share, t_group, t_half, t_fair, t_tens, t_pairs, t_fives, t_plates], [t_pic, t_how_many_groups, t_strip])


# ================================================================== 1.3 ======
@skill("Y1.3.a", "Halves", S3)
def _(d=1):
    d = _d(d)

    def t_shape():
        return {"prompt": "Shade one half of the bar.", "component": "fraction_bar", "spec": {"parts": 2, "mode": "shade"},
                "answer": "1/2", "answer_type": "frac", "solution": ["One of two equal parts."]}

    def t_bar4():
        return {"prompt": "The bar has 4 equal parts. Shade half of it.", "component": "fraction_bar",
                "spec": {"parts": 4, "mode": "shade"}, "answer": "2/4", "answer_type": "frac", "solution": ["Half of 4 parts is 2 parts."]}

    def t_quantity():
        n = 2 * random.randint(1, 10)
        return _tb("What is half of %d?" % n, n // 2, "int", {}, ["%d shared into 2 equal groups is %d." % (n, n // 2)])

    def t_word():
        n = 2 * random.randint(2, 8)
        return _tb("%s has %d strawberries and gives half to a friend. How many does the friend get?" % (_kid(), n), n // 2,
                   "int", {}, ["Half of %d is %d." % (n, n // 2)])

    def t_equal():
        return _wq("Are the two halves of a shape always the same size? (yes or no)", "yes", ["Halves are equal parts."], "yes / no")

    def t_how_many_halves():
        return _tb("How many halves make a whole?", 2, "int", {}, ["2 halves make 1 whole."])

    def t_half_groups():
        n = random.randint(1, 8)
        return {"prompt": "The counters are in 2 equal groups. What is half of %d?" % (2 * n), "component": "equal_groups",
                "spec": {"mode": "read", "groups": 2, "per": n}, "answer": n, "answer_type": "int",
                "solution": ["One group has %d." % n]}

    def t_grid():
        parts = pick([2, 4, 6, 8])
        return _area("Shade half of the shape.", {"mode": "fraction", "parts": parts}, "%d/%d" % (parts // 2, parts),
                     ["Half of %d squares is %s." % (parts, _pn(parts // 2, "square"))], atype="frac")

    def t_is_half():
        parts = pick([4, 6, 8])
        sh = pick([parts // 2, parts // 2, parts // 2 - 1, parts // 2 + 1])
        return _wq("%d of the %d equal parts %s shaded. Is half shaded? (yes or no)" % (sh, parts, "is" if sh == 1 else "are"), "yes" if 2 * sh == parts else "no",
                   ["Half of %d is %d." % (parts, parts // 2)], "yes / no")

    def t_length():
        n = 2 * random.randint(2, 10)
        return _tb("A string is %d cm long. It is cut in half. How long is each piece, in cm?" % n, n // 2, "int", {"unit": "cm"},
                   ["Half of %d is %d." % (n, n // 2)])

    def t_whole():
        n = random.randint(2, 10)
        return _tb("Half of a number is %d. What is the number?" % n, 2 * n, "int", {}, ["Double %d is %d." % (n, 2 * n)])

    return _pick_t([t_quantity, t_word, t_equal, t_how_many_halves, t_is_half, t_length, t_whole],
                   [t_shape, t_bar4, t_half_groups, t_grid])


@skill("Y1.3.b", "Quarters", S3)
def _(d=1):
    d = _d(d)

    def t_shape():
        return {"prompt": "Shade one quarter of the bar.", "component": "fraction_bar", "spec": {"parts": 4, "mode": "shade"},
                "answer": "1/4", "answer_type": "frac", "solution": ["One of four equal parts."]}

    def t_quantity():
        n = 4 * random.randint(1, 5)
        return _tb("What is a quarter of %d?" % n, n // 4, "int", {}, ["Share %d into 4 equal groups: %d." % (n, n // 4)])

    def t_parts():
        return _tb("How many quarters make a whole?", 4, "int", {}, ["4 quarters make 1 whole."])

    def t_pizza():
        return _tb("A pizza is cut into quarters. How many slices are there?", 4, "int", {}, ["Quarters means 4 equal parts."])

    def t_groups():
        n = random.randint(1, 5)
        return {"prompt": "There are 4 equal groups. What is one quarter of %d?" % (4 * n), "component": "equal_groups",
                "spec": {"mode": "read", "groups": 4, "per": n}, "answer": n, "answer_type": "int",
                "solution": ["One group has %d." % n]}

    def t_bar8():
        return {"prompt": "The bar has 8 equal parts. Shade one quarter of it.", "component": "fraction_bar",
                "spec": {"parts": 8, "mode": "shade"}, "answer": "2/8", "answer_type": "frac",
                "solution": ["8 parts shared into 4 groups is 2 parts."]}

    def t_grid():
        parts = pick([4, 8, 12])
        return _area("Shade one quarter of the shape.", {"mode": "fraction", "parts": parts}, "%d/%d" % (parts // 4, parts),
                     ["A quarter of %d squares is %s." % (parts, _pn(parts // 4, "square"))], atype="frac")

    def t_word():
        n = 4 * random.randint(1, 5)
        what = pick(["grapes", "stickers", "pens", "marbles"])
        return _tb("%s has %d %s and gives a quarter of them away. How many %s are given away?" % (_kid(), n, what, what), n // 4,
                   "int", {}, ["Share %d into 4 equal groups: %d." % (n, n // 4)])

    def t_bigger():
        return _wq("A cake is the same size each time. Which piece is bigger: a half or a quarter? (half or quarter)", "half",
                   ["2 equal parts give bigger pieces than 4 equal parts."], "half / quarter")

    def t_half_of_half():
        return _wq("Cut a sandwich in half. Then cut one half in half again. What is each small piece? (half or quarter)",
                   "quarter", ["Half of a half is a quarter."], "half / quarter")

    def t_is_quarter():
        parts = 4
        sh = random.randint(1, 3)
        return _wq("A square is cut into 4 equal parts. %d %s shaded. Is that one quarter? (yes or no)"
                   % (sh, "part is" if sh == 1 else "parts are"), "yes" if sh == 1 else "no",
                   ["One quarter is 1 of %d equal parts." % parts], "yes / no")

    def t_length():
        n = 4 * random.randint(1, 5)
        return _tb("A ribbon is %d cm long. What is a quarter of it, in cm?" % n, n // 4, "int", {"unit": "cm"},
                   ["%d shared into 4 equal parts is %d." % (n, n // 4)])

    def t_equal_parts():
        return _wq("Are quarters equal parts? (yes or no)", "yes", ["A quarter is one of four equal parts."], "yes / no")

    return _pick_t([t_quantity, t_parts, t_pizza, t_word, t_bigger, t_half_of_half, t_is_quarter, t_length, t_equal_parts],
                   [t_shape, t_groups, t_bar8, t_grid])


# ================================================================== 1.4 ======
@skill("Y1.4.a", "Compare lengths, heights, mass and capacity", S4)
def _(d=1):
    d = _d(d)

    def t_longer():
        a, b = random.sample(range(2, 20), 2)
        return _wq("A red ribbon is %d cm long. A blue ribbon is %d cm long. Which is longer? (red or blue)" % (a, b),
                   "red" if a > b else "blue", ["%d cm is more than %d cm." % (max(a, b), min(a, b))], "red or blue")

    def t_heavier():
        a, b = random.sample(range(1, 20), 2)
        return _wq("A bag of apples weighs %d kg. A bag of potatoes weighs %d kg. Which is heavier? (apples or potatoes)" % (a, b),
                   "apples" if a > b else "potatoes", ["The bigger number is heavier."], "apples or potatoes")

    def t_words():
        q, ans = pick([("Which is heavier: an elephant or a mouse?", "elephant"), ("Which is taller: a giraffe or a cat?", "giraffe"),
                       ("Which holds more: a bath or a cup?", "bath"), ("Which is lighter: a feather or a brick?", "feather"),
                       ("Which is shorter: a pencil or a bus?", "pencil")])
        return _wq(q, ans, ["Think about the real things."], "one word")

    def t_full():
        return _wq("A jug has no water in it. Is it full or empty?", "empty", ["No water means empty."], "full or empty")

    def t_ruler():
        cm = random.randint(2, 15)
        return {"prompt": "How long is the pencil, in cm?", "component": "ruler",
                "spec": {"mode": "length", "value": cm, "max": 20, "unit": "cm"}, "answer": cm, "answer_type": "num",
                "tolerance": 0.5, "solution": ["It reaches %d cm." % cm]}

    def t_difference():
        a, b = random.sample(range(2, 20), 2)
        return _tb("One tower is %d cubes tall. Another is %d cubes tall. How many cubes taller is the bigger one?" % (a, b),
                   abs(a - b), "int", {}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_jug():
        v = random.randint(1, 9) * 100
        return {"prompt": "How much water is in the jug, in ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"}, "answer": v, "answer_type": "num",
                "tolerance": 50, "solution": ["The water reaches %d ml." % v]}

    def t_quicker():
        a, b = random.sample(range(5, 60), 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s ran round the field in %d seconds. %s took %d seconds. Who was quicker?" % (kids[0], a, kids[1], b),
                   kids[0] if a < b else kids[1], ["Fewer seconds means quicker."], "name")

    return _pick_t([t_longer, t_heavier, t_words, t_full, t_difference, t_quicker], [t_ruler, t_jug])


@skill("Y1.4.b", "Coins and notes", S4)
def _(d=1):
    d = _d(d)

    def t_value():
        name, v = pick([("1p", 1), ("2p", 2), ("5p", 5), ("10p", 10), ("20p", 20), ("50p", 50)])
        return _tb("How many pence is a %s coin worth?" % name, v, "int", {}, ["%s = %d pence." % (name, v)])

    def t_more():
        a, b = random.sample([1, 2, 5, 10, 20, 50], 2)
        return _tb("Which coin is worth more, %dp or %dp? Type the number of pence." % (a, b), max(a, b), "int", {},
                   ["%dp is worth more." % max(a, b)])

    def t_add():
        cs = random.sample([1, 2, 5, 10], _by(d, 2, 2, 3))
        return _tb("%s has these coins: %s. How many pence altogether?" % (_kid(), ", ".join("%dp" % c for c in cs)), sum(cs),
                   "int", {}, ["%s = %dp." % (" + ".join("%d" % c for c in cs), sum(cs))])

    def t_notes():
        return _wq("Is £5 a coin or a note?", "note", ["£5, £10 and £20 are notes."], "coin or note")

    def t_pounds():
        return _tb("How many 10p coins make £1?", 10, "int", {}, ["£1 = 100p; 10 × 10p = 100p."])

    return _pick_t([t_value, t_more, t_add, t_notes, t_pounds])


@skill("Y1.4.c", "Days, months and order of events", S4)
def _(d=1):
    d = _d(d)
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
           "December"]

    def t_after():
        k = random.randrange(7)
        return _wq("Which day comes after %s?" % DAYS[k], DAYS[(k + 1) % 7], ["The days go in order."], "day")

    def t_before():
        k = random.randrange(7)
        return _wq("Which day comes before %s?" % DAYS[k], DAYS[(k - 1) % 7], ["The days go in order."], "day")

    def t_tomorrow():
        k = random.randrange(7)
        return _wq("Today is %s. What day will it be tomorrow?" % DAYS[k], DAYS[(k + 1) % 7], ["Tomorrow is the next day."], "day")

    def t_yesterday():
        k = random.randrange(7)
        return _wq("Today is %s. What day was it yesterday?" % DAYS[k], DAYS[(k - 1) % 7], ["Yesterday was the day before."], "day")

    def t_month():
        k = random.randrange(12)
        return _wq("Which month comes after %s?" % MON[k], MON[(k + 1) % 12], ["The months go in order."], "month")

    def t_counts():
        q, a = pick([("How many days are in a week?", 7), ("How many months are in a year?", 12)])
        return _tb(q, a, "int", {}, ["%d." % a])

    def t_order():
        a, b = pick([("eat breakfast", "eat lunch"), ("wake up", "go to school"), ("brush your teeth", "go to bed")])
        return _wq("Which do you usually do first: %s or %s?" % (b, a), a, ["%s comes before %s." % (a.capitalize(), b)],
                   "type it")

    return _pick_t([t_after, t_before, t_tomorrow, t_yesterday, t_month, t_counts, t_order])


@skill("Y1.4.d", "O'clock and half past", S4)
def _(d=1):
    d = _d(d)
    h = random.randint(1, 12)

    def t_oclock():
        return {"prompt": "Set the clock to %d o'clock." % h, "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:00" % h, "answer_type": "time", "solution": ["The long hand points to 12, the short hand to %d." % h]}

    def t_half():
        return {"prompt": "Set the clock to half past %d." % h, "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:30" % h, "answer_type": "time",
                "solution": ["The long hand points to 6; the short hand is halfway past %d." % h]}

    def t_hand():
        return _tb("At %d o'clock, which number does the short hand point to?" % h, h, "int", {}, ["The short hand shows the hour."])

    def t_later():
        return _tb("It is %d o'clock. What time will it be one hour later? Type the hour." % h, h % 12 + 1, "int", {},
                   ["One hour later is %d o'clock." % (h % 12 + 1)])

    def t_long_hand():
        return _tb("At half past %d, which number does the long hand point to?" % h, 6, "int", {}, ["Half past: the long hand points to 6."])

    def t_long_oclock():
        return _tb("At %d o'clock, which number does the long hand point to?" % h, 12, "int", {}, ["O'clock: the long hand points to 12."])

    def t_earlier():
        return _tb("It is %d o'clock. What time was it one hour earlier? Type the hour." % h, (h - 2) % 12 + 1, "int", {},
                   ["One hour earlier is %d o'clock." % ((h - 2) % 12 + 1)])

    def t_half_later():
        return {"prompt": "It is %d o'clock. Set the clock to half an hour later." % h, "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:30" % h, "answer_type": "time", "solution": ["Half an hour after %d o'clock is half past %d." % (h, h)]}

    def t_hour_after_half():
        return {"prompt": "It is half past %d. Set the clock to one hour later." % h, "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:30" % (h % 12 + 1), "answer_type": "time", "solution": ["One hour later is half past %d." % (h % 12 + 1)]}

    def t_short_half():
        return _tb("At half past %d, the short hand is between %d and which number?" % (h, h), h % 12 + 1, "int", {},
                   ["It is halfway from %d to %d." % (h, h % 12 + 1)])

    def t_which_first():
        a, b = random.sample(range(1, 10), 2)
        return _tb("Both times are after lunch on the same day. Which is earlier: %d o'clock or %d o'clock? Type the hour." % (a, b),
                   min(a, b), "int", {},
                   ["%d o'clock comes before %d o'clock." % (min(a, b), max(a, b))])

    def t_half_or_oclock():
        a = random.randint(1, 11)
        return _wq("Which is later: %d o'clock or half past %d? (type o'clock or half past)" % (a, a), "half past",
                   ["Half past %d is half an hour after %d o'clock." % (a, a)], "o'clock / half past")

    def t_bed():
        a = random.randint(6, 8)
        return {"prompt": "%s goes to bed at half past %d in the evening. Set the clock." % (_kid(), a), "component": "clock",
                "spec": {"mode": "set"}, "answer": "%d:30" % a, "answer_type": "time",
                "solution": ["Long hand on 6, short hand just past %d." % a]}

    def t_school():
        return {"prompt": "School starts at 9 o'clock. Set the clock.", "component": "clock", "spec": {"mode": "set"},
                "answer": "9:00", "answer_type": "time", "solution": ["Long hand on 12, short hand on 9."]}

    return _pick_t([t_hand, t_later, t_long_hand, t_long_oclock, t_earlier, t_short_half, t_which_first, t_half_or_oclock],
                   [t_oclock, t_half, t_half_later, t_hour_after_half, t_bed, t_school])


# ================================================================== 1.5 ======
@skill("Y1.5.a", "Name 2-D and 3-D shapes", S5)
def _(d=1):
    d = _d(d)

    def t_2d():
        name = pick(["triangle", "square", "rectangle", "pentagon", "hexagon"] if d else ["triangle", "square", "rectangle"])
        return {"prompt": "What is this shape called?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_3d():
        name = pick(["cube", "cuboid"])
        return {"prompt": "What is this 3-D shape called?", "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_sides():
        name, n = pick([("triangle", 3), ("square", 4), ("rectangle", 4)])
        return _tb("How many sides does a %s have?" % name, n, "int", {}, ["A %s has %d sides." % (name, n)])

    def t_object():
        q, a = pick([("A ball is the shape of a ...", "sphere"), ("A dice is the shape of a ...", "cube"),
                     ("A tin of beans is the shape of a ...", "cylinder"), ("A cereal box is the shape of a ...", "cuboid"),
                     ("An ice cream cone is the shape of a ...", "cone")])
        return _wq(q + " (one word)", a, ["It is a %s." % a], "shape name")

    def t_circle():
        return _wq("Which flat shape has no corners and no straight sides?", "circle", ["A circle is round."], "shape name")

    def t_pyramid():
        return _wq("A solid shape has a square at the bottom and triangles that meet at a point at the top. What is it? (one word)",
                   "pyramid", ["It is a pyramid."], "shape name")

    def t_count_sides():
        name = pick(["triangle", "square", "rectangle", "pentagon", "hexagon"] if d else ["triangle", "square", "rectangle"])
        return {"prompt": "Count the sides. How many sides does this shape have?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": {"triangle": 3, "square": 4, "rectangle": 4, "pentagon": 5, "hexagon": 6}[name], "answer_type": "int",
                "solution": ["Count each straight side once."]}

    def t_corners():
        name, n = pick([("triangle", 3), ("square", 4), ("rectangle", 4)])
        return _tb("How many corners does a %s have?" % name, n, "int", {}, ["A %s has %d corners." % (name, n)])

    def t_which():
        n, name = pick([(3, "triangle"), (4, "square"), (0, "circle")])
        if n == 0:
            return _wq("Which flat shape is perfectly round?", "circle", ["A circle is round."], "shape name")
        if n == 4:
            return _wq("Which shape has 4 sides that are all the same length? (one word)", "square", ["All 4 sides are equal."], "shape name")
        return _wq("Which shape has 3 straight sides?", "triangle", ["Tri means three."], "shape name")

    def t_flat():
        name, a = pick([("cube", "solid"), ("circle", "flat"), ("sphere", "solid"), ("triangle", "flat"), ("cuboid", "solid"),
                        ("square", "flat"), ("cylinder", "solid"), ("rectangle", "flat")])
        return _wq("Is a %s a flat shape or a solid shape? (flat or solid)" % name, a,
                   ["Flat shapes are 2-D; solid shapes are 3-D."], "flat / solid")

    def t_square_rect():
        return _wq("A square has 4 square corners like a rectangle. Is a square a special rectangle? (yes or no)", "yes",
                   ["A square is a rectangle with all its sides the same length."], "yes / no")

    def t_rolls():
        name, a = pick([("sphere", "yes"), ("cube", "no"), ("cylinder", "yes"), ("cuboid", "no"), ("pyramid", "no")])
        return _wq("Can a %s roll? (yes or no)" % name, a, ["Shapes with a curved surface can roll."], "yes / no")

    def t_how_many():
        shapes = [pick(["triangle", "square", "circle", "rectangle"]) for _ in range(6)]
        what = pick(sorted(set(shapes)))
        return _tb("How many %ss are in this list?  %s" % (what, ", ".join(shapes)), shapes.count(what), "int", {},
                   ["Count each %s: %d." % (what, shapes.count(what))])

    return _pick_t([t_sides, t_object, t_circle, t_pyramid, t_corners, t_which, t_flat, t_square_rect, t_rolls, t_how_many],
                   [t_2d, t_3d, t_count_sides])


@skill("Y1.5.b", "Turns, position and direction", S5)
def _(d=1):
    d = _d(d)

    def t_turn_pic():
        deg, name = pick([(90, "quarter"), (180, "half"), (270, "three-quarter"), (360, "whole")])
        return {"prompt": "The arrow shows a turn. Is it a quarter, half, three-quarter or whole turn?", "component": "angle",
                "spec": {"mode": "turn", "degrees": deg}, "answer": name, "answer_type": "str", "solution": ["It is a %s turn." % name]}

    def t_halves():
        return _tb("How many quarter turns make a whole turn?", 4, "int", {}, ["4 quarter turns make a whole turn."])

    def t_face():
        front, back = pick([("door", "window"), ("board", "clock"), ("tree", "house")])
        turn, a = pick([("a whole turn", front), ("a half turn", back)])
        return _wq("You face the %s. The %s is behind you. You make %s. What do you face now? (%s or %s)"
                   % (front, back, turn, front, back), a,
                   ["A whole turn brings you back to the start." if a == front else "A half turn makes you face the other way."],
                   "%s / %s" % (front, back))

    def t_position():
        q, a = pick([("The cat is ON the mat. Is the mat above or below the cat?", "below"),
                     ("The bird is flying OVER the tree. Is the bird above or below the tree?", "above"),
                     ("Sam is standing BEHIND Mia. Who is in front?", "Mia")])
        return _wq(q, a, ["Use position words."], "word")

    def t_half_turn():
        return _tb("How many half turns make a whole turn?", 2, "int", {}, ["2 half turns make a whole turn."])

    def t_three_q():
        return _tb("How many quarter turns make a three-quarter turn?", 3, "int", {}, ["3 quarter turns make a three-quarter turn."])

    def t_two_halves():
        q, a = pick([("You make a quarter turn and then another quarter turn. What turn is that altogether? (half or whole)", "half"),
                     ("You make a half turn and then another half turn. What turn is that altogether? (half or whole)", "whole")])
        return _wq(q, a, ["Add the turns together."], "half / whole")

    def t_line_up():
        kids = random.sample(KIDS, 3)
        which, a = pick([("first", kids[0]), ("in the middle", kids[1]), ("last", kids[2])])
        return _wq("%s, %s and %s stand in a line in that order. Who is %s?" % (kids[0], kids[1], kids[2], which), a,
                   ["The order is %s, %s, %s." % tuple(kids)], "name")

    def t_more_position():
        q, a = pick([("A ball is UNDER the table. Is the table above or below the ball?", "above"),
                     ("A book is on the TOP shelf. Is it high or low?", "high"),
                     ("A cup is INSIDE a box. Is the cup in or out of the box?", "in"),
                     ("The sun is in the sky. Is it above or below the trees?", "above"),
                     ("A dog sits NEXT TO a cat. Is the dog beside or on top of the cat? (beside or on top)", "beside")])
        return _wq(q, a, ["Use position words."], "word")

    def t_grid():
        x, y = random.randint(1, 3), random.randint(1, 3)
        r = random.randint(1, 3)
        u = random.randint(1, 3)
        return {"prompt": "Start at the dot. Move %d square%s right and %d square%s up. Mark where you stop."
                          % (r, "" if r == 1 else "s", u, "" if u == 1 else "s"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord", "solution": ["%d right, then %d up." % (r, u)]}

    def t_clock_turn():
        q, a = pick([("The long hand of a clock goes from 12 to 6. Is that a quarter, half or whole turn?", "half"),
                     ("The long hand of a clock goes from 12 to 3. Is that a quarter, half or whole turn?", "quarter"),
                     ("The long hand of a clock goes from 12 all the way round to 12. Is that a quarter, half or whole turn?", "whole"),
                     ("The long hand of a clock goes from 12 to 9. Is that a quarter, half or three-quarter turn?", "three-quarter")])
        return _wq(q, a, ["A quarter turn moves the hand 3 numbers on."], "turn")

    return _pick_t([t_halves, t_face, t_position, t_half_turn, t_three_q, t_two_halves, t_line_up, t_more_position, t_clock_turn],
                   [t_turn_pic, t_grid])
