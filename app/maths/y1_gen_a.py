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


def _why_cmp(a, b):
    """Why one of two numbers is more, in Year 1 words: "49 has 4 tens and 27 has only 2 tens"."""
    hi, lo = max(a, b), min(a, b)
    if hi // 10 > lo // 10:
        return "%d has %s and %d has %s" % (hi, _pn(hi // 10, "ten"), lo, "only " + _pn(lo // 10, "ten") if lo >= 10 else "no tens")
    return "%d and %d have the same tens, and %d has more ones" % (hi, lo, hi)


def _counted(step, k):
    """"Count in 5s: 5, 10, 15, 20." (k steps of step), the Year 1 way to find a total of equal groups."""
    return "Count in %ds: %s." % (step, ", ".join(str(step * i) for i in range(1, k + 1)))


# Why, for the real things a Year 1 child compares (the answer is the key).
_REAL = {"elephant": "An elephant is huge and a mouse is tiny, so the elephant is heavier.",
         "giraffe": "A giraffe's neck reaches the treetops; a cat is small. The giraffe is taller.",
         "bath": "You could fill lots of cups from one bath, so the bath holds more.",
         "feather": "A feather floats in the air; a brick is hard to lift. The feather is lighter.",
         "pencil": "A pencil fits in your hand; a bus is longer than a car. The pencil is shorter."}

_CLOCK_TURN = {"quarter": "From 12 to 3 is a quarter of the way round: a quarter turn.",
               "half": "From 12 to 6 is half of the way round: a half turn.",
               "three-quarter": "From 12 to 9 is three quarters of the way round: a three-quarter turn.",
               "whole": "All the way round and back to 12 is a whole turn."}

# Why, for each position question (the question is the key).
_WHERE = {"The cat is ON the mat. Is the mat above or below the cat?": "The cat sits on top of the mat, so the mat is below the cat.",
          "The bird is flying OVER the tree. Is the bird above or below the tree?": "Over means higher up, so the bird is above the tree.",
          "Sam is standing BEHIND Mia. Who is in front?": "Sam is behind Mia, so Mia is in front.",
          "A ball is UNDER the table. Is the table above or below the ball?": "The ball is under the table, so the table is above the ball.",
          "A book is on the TOP shelf. Is it high or low?": "The top shelf is the highest one, so the book is high.",
          "A cup is INSIDE a box. Is the cup in or out of the box?": "Inside means in, so the cup is in the box.",
          "The sun is in the sky. Is it above or below the trees?": "The sky is higher than the trees, so the sun is above them.",
          "A dog sits NEXT TO a cat. Is the dog beside or on top of the cat? (beside or on top)": "Next to means beside."}


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
        return _tb("Which number is between %d and %d?" % (n - 1, n + 1), n, "int", {}, ["Count on from %d: %d, %d, %d. The number in the middle is %d." % (n - 1, n - 1, n, n + 1, n)])

    def t_missing_back():
        s = [start + 4 - i for i in range(5)]
        k = random.randint(1, 3)
        return _tb("Count back. Find the missing number:  %s" % ", ".join("___" if i == k else str(v) for i, v in enumerate(s)),
                   s[k], "int", {}, ["Count back in ones."])

    def t_count_on():
        k = random.randint(2, 5)
        return _tb("Start at %d. Count on %d. Where do you stop?" % (start, k), start + k, "int", {},
                   ["Count on %d from %d: %s. You stop on %d." % (k, start, ", ".join(str(start + i) for i in range(1, k + 1)), start + k)])

    def t_count_back():
        n = random.randint(6, _by(d, 20, 60, 100))
        k = random.randint(2, 5)
        return _tb("Start at %d. Count back %d. Where do you stop?" % (n, k), n - k, "int", {},
                   ["Count back %d from %d: %s. You stop on %d." % (k, n, ", ".join(str(n - i) for i in range(1, k + 1)), n - k)])

    def t_to_100():
        n = random.randint(94, 97) if d == 2 else random.randint(36, 89)
        return _tb("Count on:  %d, %d, %d, ___" % (n, n + 1, n + 2), n + 3, "int", {}, ["After %d comes %d." % (n + 2, n + 3)])

    def t_line_back():
        n = random.randint(3, _by(d, 20, 50, 100))
        lo = max(0, ((n - 3) // 10) * 10)
        return _nl("Start at %d and count back 3. Mark where you stop." % n, n - 3, 1, 5, ["Count back 3 from %d: %d, %d, %d." % (n, n - 1, n - 2, n - 3)],
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
        k = random.randint(2, _by(d, 10, 12, 12))      # counted, then written as a word (the skill)
        return {"prompt": "Count the counters. Write how many in words.", "component": "equal_groups",
                "spec": {"mode": "read", "groups": 1, "per": k}, "answer": n_words(k), "answer_type": "str",
                "solution": ["Count them: %d." % k, "%d in words is %s." % (k, n_words(k))]}

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
                "answer_type": "int", "solution": ["Count in %ds: %s. That makes %d." % (step, ", ".join(str(step * i) for i in range(1, k + 1)), step * k)]}

    def t_socks():
        return _tb("How many socks are in %d pairs? Count in 2s." % k, 2 * k, "int", {}, ["Count in %ds: %s. That makes %d." % (2, ", ".join(str(2 * i) for i in range(1, k + 1)), 2 * k)])

    def t_line():
        return _nl("Start at 0 and make %d jumps of %d. Where do you land?" % (k, step), k * step, step, 10,
                   ["%d jumps of %d. %s" % (k, step, _counted(step, k))], lo=0, hi=max(20, (k * step // 10 + 1) * 10))

    def t_back():
        s = [step * i for i in range(k + 1, k - 2, -1)]
        return _tb("Count back in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] - step, "int", {}, ["Take away %d." % step])

    def t_hands():
        return _tb("How many fingers are on %d hands? Count in 5s." % k, 5 * k, "int", {},
                   ["Count in %ds: %s. That makes %d." % (5, ", ".join(str(5 * i) for i in range(1, k + 1)), 5 * k)])

    def t_coins():
        c = pick([2, 5, 10])
        return _tb("%s has %s %dp coins. How many pence is that? Count in %ss." % (_kid(), _cnt(k), c, c), k * c, "int", {"unit": "p"},
                   ["Count in %ds: %s. That makes %d." % (c, ", ".join(str(c * i) for i in range(1, k + 1)), c * k)])

    def t_sticks():
        return _tb("There are %d bundles of 10 sticks. How many sticks? Count in 10s." % k, 10 * k, "int", {},
                   ["Count in %ds: %s. That makes %d." % (10, ", ".join(str(10 * i) for i in range(1, k + 1)), 10 * k)])

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
                "spec": {"mode": "build", "max": 9}, "answer": m + 1, "answer_type": "int", "solution": ["One more: count on 1 from %d to %d." % (m, m + 1)]}

    return _pick_t([t_more, t_less, t_word], [t_blocks])


@skill("Y1.0.e", "Compare numbers: more, less, most, least", S0)
def _(d=1):
    d = _d(d)
    a, b = random.sample(range(1, _by(d, 20, 50, 100)), 2)
    if d == 2 and random.random() < 0.6:                # hard: same tens, so the ones decide
        t = random.randint(2, 9) * 10
        a, b = [t + x for x in random.sample(range(10), 2)]

    def t_more():
        return _tb("Which is more, %d or %d?" % (a, b), max(a, b), "int", {}, ["%s, so %d is more." % (_why_cmp(a, b), max(a, b))])

    def t_less():
        return _tb("Which is less, %d or %d?" % (a, b), min(a, b), "int", {}, ["%s, so %d is less." % (_why_cmp(a, b), min(a, b))])

    def t_most():
        k = _by(d, 3, 3, 4)                             # hard: four children, and sometimes the least
        vals = random.sample(range(1, _by(d, 11, 30, 100)), k)
        kids = random.sample(KIDS, k)
        most = d < 2 or random.random() < 0.5
        win = max(vals) if most else min(vals)
        return _wq("%s and %s has %d. Who has the %s?" % (", ".join("%s has %s" % (kids[0], _pn(vals[0], "sticker")) if i == 0 else
                                                                   "%s has %d" % (kids[i], vals[i]) for i in range(k - 1)),
                                                         kids[-1], vals[-1], "most" if most else "least"),
                   kids[vals.index(win)], ["%d is the %s number." % (win, "biggest" if most else "smallest")], "name")

    def t_fewer():
        vals = random.sample(range(1, _by(d, 11, 20, 100)), 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s has %s. %s has %s. Who has fewer?" % (kids[0], _pn(vals[0], "marble"), kids[1], _pn(vals[1], "marble")),
                   kids[vals.index(min(vals))], ["%d is less than %d." % (min(vals), max(vals))], "name")

    def t_pictogram():
        k = _by(d, 3, 3, 4)
        cats = random.sample(["Cats", "Dogs", "Fish", "Birds"], k)
        vals = random.sample(range(1, _by(d, 6, 9, 11)), k)
        most = d < 2 or random.random() < 0.5
        win = max(vals) if most else min(vals)
        return {"prompt": "Which pet is the %s popular?" % ("most" if most else "least"), "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": cats[vals.index(win)], "answer_type": "str",
                "solution": ["%s has the %s: %d." % (cats[vals.index(win)], "most" if most else "fewest", win)]}

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
        return _tb("%s make what number?" % _to(n), n, "int", {}, ["%s is %d, and %s more make %d." % (_pn(n // 10, "ten"), (n // 10) * 10, _pn(n % 10, "one"), n)])

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
    a = random.randint(_by(d, 5, 0, 1), _by(d, 9, 10, 5))     # easy: small part to find; hard: big part

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
        # the frame is drawn: 2 rows of 5 spaces, `a` of them with a dot (a 5-year-old can't picture it from words)
        return _area("A ten frame has %s. How many empty spaces are there?" % _pn(a, "dot"),
                     {"mode": "fraction_read", "parts": 10, "rows": 2, "cols": 5, "shaded": a, "dots": True,
                      "placeholder": ""}, 10 - a, ["A ten frame has 10 spaces: 10 − %d = %d." % (a, 10 - a)])

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

    def t_three_parts():                                # hard: three numbers make 10
        x = random.randint(1, 7)
        y = random.randint(1, 8 - x)
        return _tb("%d + %d + ___ = 10" % (x, y), 10 - x - y, "int", {},
                   ["%d + %d = %d." % (x, y, x + y), "%d and %d make 10." % (x + y, 10 - x - y)])

    def t_sub_equals():                                 # hard: the = sign on the left
        return _tb("%d = 10 − ___" % a, 10 - a, "int", {}, ["10 − %d = %d." % (10 - a, a)])

    return _pick_t(_by(d, [t_missing, t_take, t_word, t_partner, t_frame, t_pencils],
                       [t_missing, t_take, t_word, t_partner, t_left_missing, t_frame, t_sub_missing, t_pencils, t_ten_equals],
                       [t_left_missing, t_sub_missing, t_ten_equals, t_three_parts, t_sub_equals, t_pencils]),
                   [t_bar, t_line])


@skill("Y1.1.b", "Number bonds and facts within 20", S1)
def _(d=1):
    d = _d(d)
    tot = random.randint(_by(d, 11, 12, 15), _by(d, 15, 20, 20))
    a = random.randint(10, tot - 1) if d == 0 else random.randint(1, tot - 1)     # easy: teen + ones, no bridging

    def t_missing():
        return _tb("%d + ___ = %d" % (a, tot), tot - a, "int", {}, ["%d − %d = %d." % (tot, a, tot - a)])

    def t_sub():
        return _tb("%d − %d = ___" % (tot, a), tot - a, "int", {}, ["%d + %d = %d." % (a, tot - a, tot)])

    def t_related():
        b = random.randint(_by(d, 1, 1, 3), _by(d, 5, 9, 9))
        c = random.randint(_by(d, 1, 1, 11 - b), _by(d, 5, 9, 9))  # hard: the fact crosses 10
        return _tb("%d + %d = %d. So what is %d − %d?" % (b, c, b + c, b + c, c), b, "int", {}, ["Taking away %d undoes adding %d: %d − %d = %d." % (c, c, b + c, c, b)])

    def t_double():
        k = random.randint(_by(d, 1, 1, 6), _by(d, 5, 10, 10))
        return _tb("Double %d is ___" % k, 2 * k, "int", {}, ["%d + %d = %d." % (k, k, 2 * k)])

    def t_ten_plus():
        k = random.randint(1, 9)
        if d == 2:                                      # hard: the missing part
            return _tb("10 + ___ = %d" % (10 + k), k, "int", {}, ["Ten and %s is %d." % (_pn(k, "one"), 10 + k)])
        return _tb("10 + %d = ___" % k, 10 + k, "int", {}, ["Ten and %s is %d." % (_pn(k, "one"), 10 + k)])

    def t_bond20():
        k = random.randint(_by(d, 11, 1, 1), 19)       # easy: a teen number, so a small jump
        if d == 2:                                      # hard: the = sign on the left / take away
            return _tb("20 = %d + ___" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)]) if random.random() < 0.5 else \
                _tb("20 − ___ = %d" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])
        return _tb("%d + ___ = 20" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])

    def t_near_double():
        k = random.randint(_by(d, 2, 2, 5), _by(d, 5, 9, 9))
        if d == 2 and random.random() < 0.5:            # hard: one less than double
            return _tb("Double %d is %d. So what is %d + %d?" % (k, 2 * k, k, k - 1), 2 * k - 1, "int", {},
                       ["%d + %d is one less than double %d: %d." % (k, k - 1, k, 2 * k - 1)])
        return _tb("Double %d is %d. So what is %d + %d?" % (k, 2 * k, k, k + 1), 2 * k + 1, "int", {},
                   ["%d + %d is one more than double %d: %d." % (k, k + 1, k, 2 * k + 1)])

    def t_family():
        b = random.randint(2, _by(d, 5, 9, 9))
        c = random.randint(_by(d, 2, 2, max(2, 11 - b)), _by(d, 5, 9, 9))
        return _tb("%d + %d = %d. So what is %d − %d?" % (b, c, b + c, b + c, b), c, "int", {},
                   ["Take away the %d you added: %d." % (b, c)])

    def t_halve():
        k = random.randint(_by(d, 1, 1, 6), _by(d, 5, 10, 10))
        return _tb("%d − %d = ___" % (2 * k, k), k, "int", {}, ["Half of %d is %d." % (2 * k, k)])

    def t_bar():
        return _strip("The whole is %d. One part is %d. What is the other part?" % (tot, a),
                      {"mode": "part_whole", "totalLabel": str(tot), "partLabel": str(a), "unknown": "part", "parts": 2}, tot - a,
                      ["%d − %d = %d." % (tot, a, tot - a)])

    def t_teen_sub():
        k = random.randint(1, 9)
        if d == 2:                                      # hard: the missing number taken away
            return _tb("1%d − ___ = 10" % k, k, "int", {}, ["Take away the ones: 1%d − %d = 10." % (k, k)]) if random.random() < 0.5 else \
                _tb("1%d − ___ = %d" % (k, k), 10, "int", {}, ["Take away the ten: 1%d − 10 = %d." % (k, k)])
        return _tb("1%d − %d = ___" % (k, k), 10, "int", {}, ["Take away the ones: 10 is left."]) if random.random() < 0.5 else \
            _tb("1%d − 10 = ___" % k, k, "int", {}, ["Take away the ten: %d is left." % k])

    def t_story():
        kid = _kid()
        return _tb("%s has %s. %s needs %d pens. How many more pens does %s need?" % (kid, _pn(a, "pen"), kid, tot, kid), tot - a, "int", {},
                   ["%d + ___ = %d, so %d." % (a, tot, tot - a)])

    def t_line():
        return _nl(_jump(a, tot - a), tot, 1, 5, ["%d + %d = %d." % (a, tot - a, tot)],
                   lo=0, hi=20)

    def t_true():
        shown = pick([tot - a, tot - a, tot - a + 1, tot - a - 1 if tot - a > 1 else tot - a + 2])
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (a, shown, tot), "yes" if a + shown == tot else "no",
                   ["%d + %d = %d%s." % (a, shown, a + shown, "" if a + shown == tot else ", not %d" % tot)], "yes / no")

    def t_dominoes():
        x, y = random.randint(1, _by(d, 4, 6, 6)), random.randint(1, _by(d, 4, 6, 6))
        if d == 2:                                      # hard: two dominoes, four numbers
            z, w = random.randint(1, 6), random.randint(1, 6)
            return _tb("Two dominoes: one has %s and %s, the other has %d and %d. How many spots altogether?" % (_pn(x, "spot"), _pn(y, "spot"), z, w),
                       x + y + z + w, "int", {}, ["%d + %d + %d + %d = %d." % (x, y, z, w, x + y + z + w)])
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
    a = random.randint(_by(d, 1, 2, 4), _by(d, 10, 15, 17))
    b = random.randint(_by(d, 1, 2, 3), 20 - a)          # hard: no "+ 1" or "− 1" facts

    def t_add():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["Count on %d from %d." % (b, a)])

    def t_sub():
        x = a + b
        return _tb("%d − %d = ___" % (x, b), a, "int", {}, ["Count back %d from %d." % (b, x)])

    def t_line_add():
        return _nl(_jump(a, b), a + b, 1, 5, ["%d + %d = %d." % (a, b, a + b)],
                   lo=0, hi=20)

    def t_line_sub():
        x = a + b
        return _nl(_jump(x, b, back=True), a, 1, 5, ["%d − %d = %d." % (x, b, a)],
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

    return _pick_t([t_add, t_sub, t_cross_ten, t_teen_add, t_teen_sub, t_more_sum, t_add_three, t_add_word, t_sub_word,
                    t_which_sum, t_steps] + ([t_zero] if d < 2 else []), [t_line_add, t_line_sub, t_count_all, t_take_bar])


@skill("Y1.1.d", "Missing numbers and the = sign", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(_by(d, 1, 1, 4), _by(d, 5, 10, 11)), random.randint(_by(d, 1, 1, 3), _by(d, 4, 9, 9))

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
                   ["%d − %d = %d." % (a + b, b, a)], lo=0, hi=10 if a <= 10 else 20)

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
    a, b = random.randint(_by(d, 2, 2, 6), _by(d, 6, 12, 12)), random.randint(_by(d, 1, 1, 4), _by(d, 4, 8, 8))

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
        on, off = random.randint(_by(d, 4, 5, 11), _by(d, 9, 12, 20)), random.randint(1, _by(d, 3, 5, 9))
        return _tb("%d people are on a bus. %d %s off. How many are on the bus now?" % (on, off, "gets" if off == 1 else "get"), on - off, "int", {},
                   ["%d − %d = %d." % (on, off, on - off)])

    def t_groups():
        return {"prompt": "There are %d %s in one bag and %d in another. How many altogether?" % (a, t[0], b),
                "component": "equal_groups", "spec": {"mode": "read", "groups": 1, "per": a + b}, "answer": a + b,
                "answer_type": "int", "solution": ["%d + %d = %d." % (a, b, a + b)]}

    def t_two_step():                                   # hard: two steps
        c = random.randint(1, a - 1)
        return _tb("%s has %d %s. %s finds %d more, then gives %d away. How many %s now?" % (kid, a, t[0], kid, b, c, t[0]),
                   a + b - c, "int", {}, ["%d + %d = %d." % (a, b, a + b), "%d − %d = %d." % (a + b, c, a + b - c)])

    def t_start_unknown():                              # hard: the start is missing
        return _tb("%s had some %s and gave away %d. Now %s has %d. How many did %s have at first?" % (kid, t[0], b, kid, a, kid),
                   a + b, "int", {}, ["Put back the %d given away: %d + %d = %d." % (b, a, b, a + b)])

    return _pick_t(_by(d, [t_add, t_sub, t_add, t_bus], [t_add, t_sub, t_difference, t_bus],
                       [t_add, t_sub, t_difference, t_bus, t_two_step, t_start_unknown]), [t_groups])


# ================================================================== 1.2 ======
@skill("Y1.2.a", "Equal groups and arrays", S2)
def _(d=1):
    d = _d(d)
    g, p = random.randint(2, 5), pick([2, 5, 10]) if d else pick([2, 10])

    def t_groups():
        return {"prompt": "How many altogether? There are %d groups of %d." % (g, p), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": p}, "answer": g * p, "answer_type": "int",
                "solution": [_counted(p, g)]}

    def t_array():
        return {"prompt": "Make an array with %d rows of %d. How many dots?" % (g, p), "component": "array",
                "spec": {"mode": "build", "maxRows": 6, "maxCols": 10, "targetRows": g, "targetCols": p},
                "answer": g * p, "answer_type": "int", "solution": ["%d rows of %d. %s" % (g, p, _counted(p, g))]}

    def t_word():
        return _tb("There are %d plates. Each plate has %d biscuits. How many biscuits altogether?" % (g, p), g * p, "int", {},
                   [_counted(p, g)])

    def t_legs():
        # Year 1 counts in 2s, 5s and 10s (not 4s): birds' legs, starfish arms
        n, legs, what, part = pick([(random.randint(2, 8), 2, "birds", "leg"), (random.randint(2, 6), 5, "starfish", "arm")])
        return _tb("How many %ss do %d %s have?" % (part, n, what), n * legs, "int", {},
                   ["%s each: %s" % (_pn(legs, part), _counted(legs, n))])

    def t_wheels():
        n = random.randint(2, _by(d, 5, 8, 10))        # 2 wheels each: count in 2s (not 4s for cars)
        return _tb("How many wheels are on %d bikes?" % n, n * 2, "int", {}, [_counted(2, n)])

    def t_shoes():
        n = random.randint(2, 10)
        return _tb("%d children each wear a pair of shoes. How many shoes is that?" % n, 2 * n, "int", {},
                   [_counted(2, n)])

    def t_boxes():
        n = random.randint(2, 6)
        return _tb("There are %d boxes. Each box has 10 pencils. How many pencils?" % n, 10 * n, "int", {},
                   [_counted(10, n)])

    def t_groups_count():
        return {"prompt": "How many groups are there?", "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": p}, "answer": g, "answer_type": "int",
                "solution": ["Count the groups one by one: there are %d, each with %d." % (g, p)]}

    def t_double():
        k = random.randint(1, 10)
        return _tb("Double %d. How many is 2 groups of %d?" % (k, k), 2 * k, "int", {}, ["%d + %d = %d." % (k, k, 2 * k)])

    def t_bar():
        return _strip("There are %d bags with %d sweets in each. How many sweets?" % (g, p),
                      {"mode": "equal_parts", "parts": g, "partLabel": str(p), "totalLabel": "?", "unknown": "total"}, g * p,
                      [_counted(p, g)])

    def t_rows():
        return _tb("Chairs are put in %d rows with %d chairs in each row. How many chairs?" % (g, p), g * p, "int", {},
                   ["%d rows of %d. %s" % (g, p, _counted(p, g))])

    return _pick_t([t_word, t_legs, t_wheels, t_shoes, t_boxes, t_double, t_rows], [t_groups, t_array, t_groups_count, t_bar])


@skill("Y1.2.b", "Sharing and grouping", S2)
def _(d=1):
    d = _d(d)
    k, each = random.randint(2, _by(d, 3, 5, 5)), random.randint(_by(d, 2, 2, 3), _by(d, 5, 5, 6))

    def t_share():
        return _tb("%d sweets are shared equally between %d children. How many does each child get?" % (k * each, k), each,
                   "int", {}, ["%d shared into %d groups is %d each." % (k * each, k, each)])

    def t_group():
        return _tb("%d eggs go in boxes of %d. How many boxes?" % (k * each, each), k, "int", {},
                   ["Make groups of %d: %d groups." % (each, k)])

    def t_half():
        n = 2 * random.randint(_by(d, 1, 1, 6), _by(d, 5, 10, 10))
        return _tb("Half of %d is ___" % n, n // 2, "int", {}, ["Share %d into 2 equal groups: %d." % (n, n // 2)])

    def t_pic():
        return {"prompt": "%d counters are shared into %d equal groups. How many in each group?" % (k * each, k),
                "component": "equal_groups", "spec": {"mode": "read", "groups": k, "per": each}, "answer": each,
                "answer_type": "int", "solution": ["Each group has %d." % each]}

    def t_fair():
        n = random.randint(_by(d, 4, 5, 9), _by(d, 10, 16, 20))
        return _wq("Can %d sweets be shared fairly between 2 children? (yes or no)" % n, "yes" if n % 2 == 0 else "no",
                   ["%s" % ("Each gets %d." % (n // 2) if n % 2 == 0 else "One would be left over.")], "yes / no")

    def t_how_many_groups():
        return {"prompt": "%d counters are put in groups of %d. How many groups are there?" % (k * each, each),
                "component": "equal_groups", "spec": {"mode": "read", "groups": k, "per": each}, "answer": k,
                "answer_type": "int", "solution": ["Count in %ds to %d: %s. That is %s." % (each, k * each, ", ".join(str(each * i) for i in range(1, k + 1)), _pn(k, "group"))]}

    def t_strip():
        return _strip("%d stickers are shared equally into %d pages. How many on each page?" % (k * each, k),
                      {"mode": "equal_parts", "parts": k, "partLabel": "?", "totalLabel": str(k * each), "unknown": "part"}, each,
                      ["%d shared into %d is %d each." % (k * each, k, each)])

    def t_tens():
        n = random.randint(2, _by(d, 3, 5, 9))
        return _tb("%d pencils go into packs of 10. How many packs?" % (10 * n), n, "int", {}, ["Count in 10s: %d packs." % n])

    def t_pairs():
        n = random.randint(_by(d, 2, 2, 6), _by(d, 5, 10, 12))
        return _tb("%d socks are put into pairs. How many pairs?" % (2 * n), n, "int", {}, ["Count in 2s: %d pairs." % n])

    def t_fives():
        n = random.randint(2, _by(d, 3, 6, 8))
        return _tb("%d flowers go into vases of 5. How many vases?" % (5 * n), n, "int", {}, ["Count in 5s: %d vases." % n])

    def t_plates():
        return _tb("%s puts %d cakes onto %d plates, the same on each plate. How many cakes on each plate?" % (_kid(), k * each, k),
                   each, "int", {}, ["Share them out one at a time: %d each." % each])

    def t_missing_total():                              # hard: work back from the share
        return _tb("Some cakes are shared equally between %d children. Each child gets %d. How many cakes were there?" % (k, each),
                   k * each, "int", {}, ["%d groups of %d: count in %ds to %d." % (k, each, each, k * each)])

    return _pick_t(_by(d, [t_share, t_group, t_half, t_fair, t_pairs, t_plates],
                       [t_share, t_group, t_half, t_fair, t_tens, t_pairs, t_fives, t_plates],
                       [t_share, t_group, t_half, t_tens, t_pairs, t_fives, t_plates, t_missing_total]),
                   [t_pic, t_how_many_groups, t_strip])


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
        n = 2 * random.randint(_by(d, 1, 1, 5), _by(d, 5, 10, 10))
        return _tb("What is half of %d?" % n, n // 2, "int", {}, ["%d shared into 2 equal groups is %d." % (n, n // 2)])

    def t_word():
        n = 2 * random.randint(_by(d, 1, 2, 5), _by(d, 5, 8, 10))
        return _tb("%s has %d strawberries and gives half to a friend. How many does the friend get?" % (_kid(), n), n // 2,
                   "int", {}, ["Half of %d is %d." % (n, n // 2)])

    def t_equal():
        return _wq("Are the two halves of a shape always the same size? (yes or no)", "yes", ["Halves are equal parts."], "yes / no")

    def t_how_many_halves():
        return _tb("How many halves make a whole?", 2, "int", {}, ["2 halves make 1 whole."])

    def t_half_groups():
        n = random.randint(_by(d, 1, 1, 4), _by(d, 5, 8, 10))
        return {"prompt": "Share the %d counters into 2 equal groups. What is half of %d?" % (2 * n, 2 * n), "component": "equal_groups",
                "spec": {"mode": "read", "groups": 2, "per": n}, "answer": n, "answer_type": "int",
                "solution": ["One group has %d." % n]}

    def t_grid():
        parts = pick(_by(d, [2, 4], [2, 4, 6, 8], [6, 8, 10]))
        return _area("Shade half of the shape.", {"mode": "fraction", "parts": parts}, "%d/%d" % (parts // 2, parts),
                     ["Half of %d squares is %s." % (parts, _pn(parts // 2, "square"))], atype="frac")

    def t_is_half():
        parts = pick(_by(d, [4], [4, 6, 8], [6, 8, 10]))
        sh = pick([parts // 2, parts // 2, parts // 2 - 1, parts // 2 + 1])
        return _area("%d of the %d equal parts %s shaded. Is half shaded? (yes or no)" % (sh, parts, "is" if sh == 1 else "are"),
                     {"mode": "fraction_read", "parts": parts, "rows": 1, "cols": parts, "shaded": sh, "placeholder": "yes / no"},
                     "yes" if 2 * sh == parts else "no", ["Half of %d is %d." % (parts, parts // 2)], atype="str")

    def t_length():
        n = 2 * random.randint(_by(d, 1, 2, 5), _by(d, 5, 10, 10))
        return _tb("A string is %d cm long. It is cut in half. How long is each piece, in cm?" % n, n // 2, "int", {"unit": "cm"},
                   ["Half of %d is %d." % (n, n // 2)])

    def t_whole():
        n = random.randint(2, 10)
        return _tb("Half of a number is %d. What is the number?" % n, 2 * n, "int", {}, ["Double %d is %d." % (n, 2 * n)])

    def t_half_left():                                  # hard: how many are left after giving half away
        n = 2 * random.randint(3, 10)
        return _tb("A bag has %d marbles. Half of them roll away. How many marbles are still in the bag?" % n, n // 2, "int", {},
                   ["Half of %d is %d, so %d roll away and %d stay." % (n, n // 2, n // 2, n // 2)])

    return _pick_t(_by(d, [t_quantity, t_word, t_equal, t_how_many_halves, t_length],
                       [t_quantity, t_word, t_equal, t_how_many_halves, t_is_half, t_length, t_whole],
                       [t_quantity, t_word, t_is_half, t_length, t_whole, t_whole, t_half_left]),
                   _by(d, [t_shape, t_half_groups, t_grid], [t_shape, t_bar4, t_half_groups, t_grid], [t_bar4, t_half_groups, t_grid]))


@skill("Y1.3.b", "Quarters", S3)
def _(d=1):
    d = _d(d)

    def t_shape():
        return {"prompt": "Shade one quarter of the bar.", "component": "fraction_bar", "spec": {"parts": 4, "mode": "shade"},
                "answer": "1/4", "answer_type": "frac", "solution": ["One of four equal parts."]}

    def t_quantity():
        n = 4 * random.randint(_by(d, 1, 1, 2), _by(d, 3, 5, 5))
        return _tb("What is a quarter of %d?" % n, n // 4, "int", {}, ["Share %d into 4 equal groups: %d." % (n, n // 4)])

    def t_parts():
        return _tb("How many quarters make a whole?", 4, "int", {}, ["4 quarters make 1 whole."])

    def t_pizza():
        return _tb("A pizza is cut into quarters. How many slices are there?", 4, "int", {}, ["Quarters means 4 equal parts."])

    def t_groups():
        n = random.randint(_by(d, 1, 1, 2), _by(d, 3, 5, 5))
        return {"prompt": "Share the %d counters into 4 equal groups. What is one quarter of %d?" % (4 * n, 4 * n), "component": "equal_groups",
                "spec": {"mode": "read", "groups": 4, "per": n}, "answer": n, "answer_type": "int",
                "solution": ["One group has %d." % n]}

    def t_bar8():
        return {"prompt": "The bar has 8 equal parts. Shade one quarter of it.", "component": "fraction_bar",
                "spec": {"parts": 8, "mode": "shade"}, "answer": "2/8", "answer_type": "frac",
                "solution": ["8 parts shared into 4 groups is 2 parts."]}

    def t_grid():
        parts = pick(_by(d, [4], [4, 8, 12], [8, 12]))
        return _area("Shade one quarter of the shape.", {"mode": "fraction", "parts": parts}, "%d/%d" % (parts // 4, parts),
                     ["A quarter of %d squares is %s." % (parts, _pn(parts // 4, "square"))], atype="frac")

    def t_word():
        n = 4 * random.randint(_by(d, 1, 1, 2), _by(d, 3, 5, 5))
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
        return _area("A square is cut into 4 equal parts. %d %s shaded. Is that one quarter? (yes or no)"
                     % (sh, "part is" if sh == 1 else "parts are"),
                     {"mode": "fraction_read", "parts": 4, "rows": 2, "cols": 2, "shaded": sh, "placeholder": "yes / no"},
                     "yes" if sh == 1 else "no", ["One quarter is 1 of %d equal parts." % parts], atype="str")

    def t_length():
        n = 4 * random.randint(_by(d, 1, 1, 2), _by(d, 3, 5, 5))
        return _tb("A ribbon is %d cm long. What is a quarter of it, in cm?" % n, n // 4, "int", {"unit": "cm"},
                   ["%d shared into 4 equal parts is %d." % (n, n // 4)])

    def t_equal_parts():
        return _wq("Are quarters equal parts? (yes or no)", "yes", ["A quarter is one of four equal parts."], "yes / no")

    def t_whole():                                      # hard: from a quarter back to the whole
        n = random.randint(2, 5)
        return _tb("A quarter of a number is %d. What is the number?" % n, 4 * n, "int", {},
                   ["4 quarters make the whole: %d + %d + %d + %d = %d." % (n, n, n, n, 4 * n)])

    return _pick_t(_by(d, [t_quantity, t_parts, t_pizza, t_word, t_bigger, t_equal_parts],
                       [t_quantity, t_parts, t_pizza, t_word, t_bigger, t_half_of_half, t_is_quarter, t_length, t_equal_parts],
                       [t_quantity, t_word, t_half_of_half, t_is_quarter, t_length, t_whole, t_whole]),
                   _by(d, [t_shape, t_groups, t_grid], [t_shape, t_groups, t_bar8, t_grid], [t_groups, t_bar8, t_grid]))


# ================================================================== 1.4 ======
@skill("Y1.4.a", "Compare lengths, heights, mass and capacity", S4)
def _(d=1):
    d = _d(d)

    def _pair(lo, hi):
        """Two different lengths: far apart when easy, close together when hard."""
        a, b = random.sample(range(_by(d, 2, lo, lo + 4), _by(d, 11, hi, hi)), 2)
        while (d == 0 and abs(a - b) < 3) or (d == 2 and abs(a - b) > 3):
            a, b = random.sample(range(_by(d, 2, lo, lo + 4), _by(d, 11, hi, hi)), 2)
        return a, b

    def t_longer():
        a, b = _pair(2, 20)
        return _wq("A red ribbon is %d cm long. A blue ribbon is %d cm long. Which is longer? (red or blue)" % (a, b),
                   "red" if a > b else "blue", ["%d cm is more than %d cm." % (max(a, b), min(a, b))], "red or blue")

    def t_heavier():
        a, b = _pair(1, 20)
        return _wq("A bag of apples weighs %d kg. A bag of potatoes weighs %d kg. Which is heavier? (apples or potatoes)" % (a, b),
                   "apples" if a > b else "potatoes", ["The bigger number is heavier."], "apples or potatoes")

    def t_words():
        q, ans = pick([("Which is heavier: an elephant or a mouse?", "elephant"), ("Which is taller: a giraffe or a cat?", "giraffe"),
                       ("Which holds more: a bath or a cup?", "bath"), ("Which is lighter: a feather or a brick?", "feather"),
                       ("Which is shorter: a pencil or a bus?", "pencil")])
        return _wq(q, ans, [_REAL[ans]], "one word")

    def t_full():
        return _wq("A jug has no water in it. Is it full or empty?", "empty", ["No water means empty."], "full or empty")

    def t_ruler():
        cm = random.randint(_by(d, 2, 2, 8), _by(d, 10, 15, 19))
        return {"prompt": "How long is the pencil, in cm?", "component": "ruler",
                "spec": {"mode": "length", "value": cm, "max": 20, "unit": "cm"}, "answer": cm, "answer_type": "num",
                "tolerance": 0.5, "solution": ["It reaches %d cm." % cm]}

    def t_difference():
        a, b = random.sample(range(_by(d, 2, 2, 8), _by(d, 11, 20, 21)), 2)
        return _tb("One tower is %d cubes tall. Another is %d cubes tall. How many cubes taller is the bigger one?" % (a, b),
                   abs(a - b), "int", {}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_jug():                                        # non-standard units: the jug is marked in cups
        top = _by(d, 5, 5, 10)
        v = random.randint(1, top - 1)
        if d == 2 and random.random() < 0.5:            # hard: how many more cups to fill it
            return {"prompt": "The jug is marked in cups. It holds %d cups when full. How many more cups of water will fill it?" % top,
                    "component": "ruler", "spec": {"mode": "capacity", "value": v, "max": top, "unit": "cups"},
                    "answer": top - v, "answer_type": "num", "tolerance": 0,
                    "solution": ["It has %s. %d − %d = %s more." % (_pn(v, "cup"), top, v, _pn(top - v, "cup"))]}
        return {"prompt": "The jug is marked in cups. How many cups of water are in it?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": top, "unit": "cups"}, "answer": v, "answer_type": "num",
                "tolerance": 0, "solution": ["The water reaches %s." % _pn(v, "cup")]}

    def t_quicker():
        a, b = random.sample(range(5, 60), 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s ran round the field in %d seconds. %s took %d seconds. Who was quicker?" % (kids[0], a, kids[1], b),
                   kids[0] if a < b else kids[1], ["Fewer seconds means quicker."], "name")

    def t_tallest():                                    # hard: order three heights
        vals = random.sample(range(60, 100), 3)
        kids = random.sample(KIDS, 3)
        most = pick([("tallest", max), ("shortest", min)])
        ans = kids[vals.index(most[1](vals))]
        return _wq("%s is %d cm tall, %s is %d cm tall and %s is %d cm tall. Who is the %s?"
                   % (kids[0], vals[0], kids[1], vals[1], kids[2], vals[2], most[0]), ans,
                   ["%s is %d cm, the %s height." % (ans, most[1](vals), "biggest" if most[1] is max else "smallest")], "name")

    return _pick_t(_by(d, [t_longer, t_heavier, t_words, t_full, t_difference],
                       [t_longer, t_heavier, t_words, t_full, t_difference, t_quicker],
                       [t_longer, t_heavier, t_difference, t_quicker, t_tallest, t_tallest]),
                   _by(d, [t_ruler], [t_ruler, t_jug], [t_ruler, t_jug]))


@skill("Y1.4.b", "Coins and notes", S4)
def _(d=1):
    d = _d(d)
    coins = _by(d, [1, 2, 5, 10], [1, 2, 5, 10, 20, 50], [1, 2, 5, 10, 20, 50])

    def t_value():
        name, v = pick(_by(d, [("1p", 1), ("2p", 2), ("5p", 5), ("10p", 10)],
                           [("1p", 1), ("2p", 2), ("5p", 5), ("10p", 10), ("20p", 20), ("50p", 50)],
                           [("10p", 10), ("20p", 20), ("50p", 50), ("£1", 100)]))      # hard: the £1 coin in pence
        return _tb("How many pence is a %s coin worth?" % name, v, "int", {}, ["%s = %d pence." % (name, v)])

    def t_more():
        if d == 2:                                      # hard: three coins, most or least
            cs = random.sample(coins, 3)
            most = random.random() < 0.5
            win = max(cs) if most else min(cs)
            return _tb("Which coin is worth the %s: %s? Type the number of pence." % ("most" if most else "least",
                                                                                     ", ".join("%dp" % c for c in cs)),
                       win, "int", {}, ["%d pence is the %s of %s, so %dp is worth the %s." % (win, "biggest" if most else "smallest", ", ".join("%d" % c for c in sorted(cs)), win, "most" if most else "least")])
        a, b = random.sample(coins, 2)
        return _tb("Which coin is worth more, %dp or %dp? Type the number of pence." % (a, b), max(a, b), "int", {},
                   ["%d pence is more than %d %s, so %dp is worth more." % (max(a, b), min(a, b), "penny" if min(a, b) == 1 else "pence", max(a, b))])

    def t_add():
        cs = random.sample(_by(d, [1, 2, 5], [1, 2, 5, 10], [1, 2, 5, 10, 20]), _by(d, 2, 2, 3))
        return _tb("%s has these coins: %s. How many pence altogether?" % (_kid(), ", ".join("%dp" % c for c in cs)), sum(cs),
                   "int", {}, ["%s = %dp." % (" + ".join("%d" % c for c in cs), sum(cs))])

    def t_notes():
        m, a = pick(_by(d, [("£5", "note"), ("£10", "note"), ("10p", "coin"), ("5p", "coin")],
                        [("£5", "note")],
                        [("£1", "coin"), ("£2", "coin"), ("£20", "note"), ("50p", "coin"), ("£10", "note")]))
        return _wq("Is %s a coin or a note?" % m, a, ["£5, £10 and £20 are notes; pence, £1 and £2 are coins."], "coin or note")

    def t_pounds():
        c, tot = pick(_by(d, [(1, 5), (1, 10), (2, 10), (5, 10)],
                          [(10, 100)],
                          [(20, 100), (50, 100), (5, 50), (2, 20), (10, 50)]))
        tn = "£1" if tot == 100 else "%dp" % tot
        return _tb("How many %dp coins make %s?" % (c, tn), tot // c, "int", {},
                   ["%sCount in %ds: %s. That is %s." % ("£1 = 100p. " if tot == 100 else "", c,
                                                          ", ".join("%dp" % (c * i) for i in range(1, tot // c + 1)),
                                                          _pn(tot // c, "coin"))])

    return _pick_t([t_value, t_more, t_add, t_notes, t_pounds])


@skill("Y1.4.c", "Days, months and order of events", S4)
def _(d=1):
    d = _d(d)
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
           "December"]

    def t_after():
        k = random.randrange(7)
        return _wq("Which day comes after %s?" % DAYS[k], DAYS[(k + 1) % 7], ["The days go in order: %s comes just after %s." % (DAYS[(k + 1) % 7], DAYS[k])], "day")

    def t_before():
        k = random.randrange(7)
        return _wq("Which day comes before %s?" % DAYS[k], DAYS[(k - 1) % 7], ["The days go in order: %s comes just before %s." % (DAYS[(k - 1) % 7], DAYS[k])], "day")

    def t_tomorrow():
        k = random.randrange(7)
        return _wq("Today is %s. What day will it be tomorrow?" % DAYS[k], DAYS[(k + 1) % 7], ["Tomorrow is the next day: after %s comes %s." % (DAYS[k], DAYS[(k + 1) % 7])], "day")

    def t_yesterday():
        k = random.randrange(7)
        return _wq("Today is %s. What day was it yesterday?" % DAYS[k], DAYS[(k - 1) % 7], ["Yesterday was the day before: just before %s comes %s." % (DAYS[k], DAYS[(k - 1) % 7])], "day")

    def t_month():
        k = random.randrange(12)
        return _wq("Which month comes after %s?" % MON[k], MON[(k + 1) % 12], ["The months go in order: %s comes just after %s." % (MON[(k + 1) % 12], MON[k])], "month")

    def t_counts():
        q, a = pick([("How many days are in a week?", 7), ("How many months are in a year?", 12)])
        return _tb(q, a, "int", {}, ["Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: 7 days." if a == 7 else
                                     "January, February and on to December: 12 months."])

    def t_order():
        a, b = pick([("eat breakfast", "eat lunch"), ("wake up", "go to school"), ("brush your teeth", "go to bed")])
        return _wq("Which do you usually do first: %s or %s?" % (b, a), a, ["%s comes before %s." % (a.capitalize(), b)],
                   "type it")

    def t_days_on():                                    # hard: more than one day on or back
        k = random.randrange(7)
        j = random.randint(2, 3)
        fwd = random.random() < 0.6
        when = ("the day after tomorrow" if j == 2 else "in 3 days") if fwd else ("the day before yesterday" if j == 2 else "3 days ago")
        ans = DAYS[(k + j) % 7] if fwd else DAYS[(k - j) % 7]
        return _wq("Today is %s. What day %s %s?" % (DAYS[k], "will it be" if fwd else "was it", when), ans,
                   ["Count %s %d days from %s: %s." % ("on" if fwd else "back", j, DAYS[k],
                                                     ", ".join(DAYS[(k + (i if fwd else -i)) % 7] for i in range(1, j + 1)))], "day")

    def t_month_before():                               # hard: months backwards
        k = random.randrange(12)
        return _wq("Which month comes before %s?" % MON[k], MON[(k - 1) % 12], ["The months go in order: %s comes just before %s."
                                                                               % (MON[(k - 1) % 12], MON[k])], "month")

    return _pick_t(_by(d, [t_after, t_tomorrow, t_after, t_counts, t_order],
                       [t_after, t_before, t_tomorrow, t_yesterday, t_month, t_counts, t_order],
                       [t_before, t_yesterday, t_month, t_month_before, t_days_on, t_days_on]))


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
        return _tb("At %d o'clock, which number does the short hand point to?" % h, h, "int", {}, ["The short hand shows the hour: at %d o'clock it points to %d." % (h, h)])

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

    def t_two_hours():                                  # hard: two hours on from half past
        return {"prompt": "It is half past %d. Set the clock to 2 hours later." % h, "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:30" % ((h + 1) % 12 + 1), "answer_type": "time",
                "solution": ["1 hour later is half past %d; 2 hours later is half past %d." % (h % 12 + 1, (h + 1) % 12 + 1)]}

    def t_half_earlier():                               # hard: back half an hour
        return {"prompt": "It is half past %d. Set the clock to half an hour earlier." % h, "component": "clock",
                "spec": {"mode": "set"}, "answer": "%d:00" % h, "answer_type": "time",
                "solution": ["Half an hour before half past %d is %d o'clock." % (h, h)]}

    return _pick_t(_by(d, [t_hand, t_later, t_long_oclock, t_which_first],
                       [t_hand, t_later, t_long_hand, t_long_oclock, t_earlier, t_short_half, t_which_first, t_half_or_oclock],
                       [t_long_hand, t_earlier, t_short_half, t_half_or_oclock]),
                   _by(d, [t_oclock, t_oclock, t_half, t_school],
                       [t_oclock, t_half, t_half_later, t_hour_after_half, t_bed, t_school],
                       [t_half, t_half_later, t_hour_after_half, t_bed, t_two_hours, t_half_earlier]))


# ================================================================== 1.5 ======
@skill("Y1.5.a", "Name 2-D and 3-D shapes", S5)
def _(d=1):
    d = _d(d)

    flat = _by(d, ["triangle", "square", "rectangle"], ["triangle", "square", "rectangle"],
               ["rectangle", "square", "rectangle", "square", "triangle"])   # hard: square or rectangle?
    edges = {"triangle": 3, "square": 4, "rectangle": 4}

    def t_2d():
        name = pick(flat)
        return {"prompt": "What is this shape called?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_3d():
        name = pick(_by(d, ["cube", "cuboid"], ["cube", "cuboid"], ["cuboid", "pyramid", "cube", "pyramid"]))
        return {"prompt": "What is this 3-D shape called?", "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_sides():
        name, n = pick(_by(d, [("triangle", 3), ("square", 4)], [("triangle", 3), ("square", 4), ("rectangle", 4)],
                           [("rectangle", 4), ("circle", 0), ("triangle", 3)]))     # hard: a circle has no straight sides
        return _tb("How many straight sides does a %s have?" % name, n, "int", {}, ["A %s has %d straight sides." % (name, n)])

    def t_object():
        q, a = pick(_by(d, [("A ball is the shape of a ...", "sphere"), ("A dice is the shape of a ...", "cube"),
                            ("A cereal box is the shape of a ...", "cuboid")],
                        [("A ball is the shape of a ...", "sphere"), ("A dice is the shape of a ...", "cube"),
                         ("A tin of beans is the shape of a ...", "cylinder"), ("A cereal box is the shape of a ...", "cuboid"),
                         ("An ice cream cone is the shape of a ...", "cone")],
                        [("A tin of beans is the shape of a ...", "cylinder"), ("An ice cream cone is the shape of a ...", "cone"),
                         ("A brick is the shape of a ...", "cuboid"), ("An orange is the shape of a ...", "sphere"),
                         ("A tent with a square floor and a pointed top is the shape of a ...", "pyramid")]))
        return _wq(q + " (one word)", a, ["It is a %s." % a], "shape name")

    def t_circle():
        return _wq("Which flat shape has no corners and no straight sides?", "circle", ["A circle is round."], "shape name")

    def t_pyramid():
        return _wq("A solid shape has a square at the bottom and triangles that meet at a point at the top. What is it? (one word)",
                   "pyramid", ["It is a pyramid."], "shape name")

    def t_count_sides():
        name = pick(flat)
        return {"prompt": "Count the sides. How many sides does this shape have?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": edges[name], "answer_type": "int",
                "solution": ["Count each straight side once."]}

    def t_corners():
        name, n = pick(_by(d, [("triangle", 3), ("square", 4)], [("triangle", 3), ("square", 4), ("rectangle", 4)],
                           [("rectangle", 4), ("circle", 0), ("triangle", 3)]))     # hard: a circle has no corners
        return _tb("How many corners does a %s have?" % name, n, "int", {}, ["A %s has %d corners." % (name, n)])

    def t_which():
        n, name = pick(_by(d, [(3, "triangle"), (0, "circle")], [(3, "triangle"), (4, "square"), (0, "circle")],
                           [(4, "square"), (4, "rectangle"), (4, "rectangle"), (3, "triangle")]))
        if name == "rectangle":                         # hard: tell a rectangle from a square
            return _wq("Which shape has 4 square corners, 2 long sides and 2 short sides? (one word)", "rectangle",
                       ["A rectangle has 2 long sides and 2 short sides."], "shape name")
        if n == 0:
            return _wq("Which flat shape is perfectly round?", "circle", ["A circle is round."], "shape name")
        if n == 4:
            return _wq("Which shape has 4 sides that are all the same length? (one word)", "square", ["A square has 4 sides, all the same length."], "shape name")
        return _wq("Which shape has 3 straight sides?", "triangle", ["Tri means three."], "shape name")

    def t_flat():
        name, a = pick(_by(d, [("cube", "solid"), ("circle", "flat"), ("sphere", "solid"), ("square", "flat")],
                           [("cube", "solid"), ("circle", "flat"), ("sphere", "solid"), ("triangle", "flat"), ("cuboid", "solid"),
                            ("square", "flat"), ("cylinder", "solid"), ("rectangle", "flat")],
                           [("pyramid", "solid"), ("triangle", "flat"), ("cylinder", "solid"), ("circle", "flat"), ("cone", "solid"),
                            ("rectangle", "flat"), ("cuboid", "solid")]))
        return _wq("Is a %s a flat shape or a solid shape? (flat or solid)" % name, a,
                   ["Flat shapes are 2-D; solid shapes are 3-D."], "flat / solid")

    def t_square_rect():
        return _wq("A square has 4 square corners like a rectangle. Is a square a special rectangle? (yes or no)", "yes",
                   ["A square is a rectangle with all its sides the same length."], "yes / no")

    def t_rolls():
        name, a = pick(_by(d, [("sphere", "yes"), ("cube", "no")],
                           [("sphere", "yes"), ("cube", "no"), ("cylinder", "yes"), ("cuboid", "no"), ("pyramid", "no")],
                           [("cylinder", "yes"), ("cuboid", "no"), ("pyramid", "no"), ("cone", "yes")]))
        return _wq("Can a %s roll? (yes or no)" % name, a, ["Shapes with a curved surface can roll."], "yes / no")

    def t_how_many():
        shapes = [pick(_by(d, ["triangle", "square", "circle"], ["triangle", "square", "circle", "rectangle"],
                           ["triangle", "square", "circle", "rectangle", "cube"])) for _ in range(_by(d, 4, 6, 8))]
        what = pick(sorted(set(shapes)))
        return _tb("How many %ss are in this list?  %s" % (what, ", ".join(shapes)), shapes.count(what), "int", {},
                   ["Count each %s: %d." % (what, shapes.count(what))])

    return _pick_t(_by(d, [t_sides, t_object, t_circle, t_corners, t_which, t_flat, t_rolls, t_how_many],
                       [t_sides, t_object, t_circle, t_pyramid, t_corners, t_which, t_flat, t_square_rect, t_rolls, t_how_many],
                       [t_sides, t_object, t_pyramid, t_corners, t_which, t_flat, t_square_rect, t_rolls, t_how_many]),
                   [t_2d, t_3d, t_count_sides])


@skill("Y1.5.b", "Turns, position and direction", S5)
def _(d=1):
    d = _d(d)

    def t_turn_pic():
        deg, name = pick(_by(d, [(90, "quarter"), (180, "half"), (360, "whole")],
                             [(90, "quarter"), (180, "half"), (270, "three-quarter"), (360, "whole")],
                             [(90, "quarter"), (270, "three-quarter"), (270, "three-quarter"), (180, "half")]))
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
        return _wq(q, a, [_WHERE[q]], "word")

    def t_half_turn():
        return _tb("How many half turns make a whole turn?", 2, "int", {}, ["2 half turns make a whole turn."])

    def t_three_q():
        return _tb("How many quarter turns make a three-quarter turn?", 3, "int", {}, ["3 quarter turns make a three-quarter turn."])

    def t_two_halves():
        q, a = pick([("You make a quarter turn and then another quarter turn. What turn is that altogether? (half or whole)", "half"),
                     ("You make a half turn and then another half turn. What turn is that altogether? (half or whole)", "whole")])
        return _wq(q, a, ["Two quarter turns make a half turn." if a == "half" else "Two half turns make a whole turn."], "half / whole")

    def t_turn_sum():                                   # hard: mixed turns add up
        q, a = pick([("You make a half turn and then a quarter turn. What turn is that altogether? (quarter, half, three-quarter or whole)",
                      "three-quarter"),
                     ("You make a three-quarter turn and then a quarter turn. What turn is that altogether? (quarter, half, three-quarter or whole)",
                      "whole"),
                     ("You make a quarter turn, then another, then another. What turn is that altogether? (quarter, half, three-quarter or whole)",
                      "three-quarter")])
        return _wq(q, a, ["A quarter turn is 1 of 4 equal turns; add up the quarters."], "turn")

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
        return _wq(q, a, [_WHERE[q]], "word")

    def t_grid():
        if d == 2:                                      # hard: left or down as well, up to 4 squares
            x, y = random.randint(1, 7), random.randint(1, 7)
            r = random.choice([k for k in range(-4, 5) if k and 1 <= x + k <= 7])
            u = random.choice([k for k in range(-4, 5) if k and 1 <= y + k <= 7])
        else:
            x, y = random.randint(1, 3), random.randint(1, 3)
            r = random.randint(1, _by(d, 2, 3, 3))
            u = random.randint(1, _by(d, 2, 3, 3))
        return {"prompt": "Start at the dot. Move %d square%s %s and %d square%s %s. Mark where you stop."
                          % (abs(r), "" if abs(r) == 1 else "s", "right" if r > 0 else "left",
                             abs(u), "" if abs(u) == 1 else "s", "up" if u > 0 else "down"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord",
                "solution": ["%d %s, then %d %s." % (abs(r), "right" if r > 0 else "left", abs(u), "up" if u > 0 else "down")]}

    def t_clock_turn():
        q, a = pick([("The long hand of a clock goes from 12 to 6. Is that a quarter, half or whole turn?", "half"),
                     ("The long hand of a clock goes from 12 to 3. Is that a quarter, half or whole turn?", "quarter"),
                     ("The long hand of a clock goes from 12 all the way round to 12. Is that a quarter, half or whole turn?", "whole"),
                     ("The long hand of a clock goes from 12 to 9. Is that a quarter, half or three-quarter turn?", "three-quarter")])
        return _wq(q, a, [_CLOCK_TURN[a]], "turn")

    return _pick_t(_by(d, [t_face, t_position, t_half_turn, t_line_up, t_more_position],
                       [t_halves, t_face, t_position, t_half_turn, t_three_q, t_two_halves, t_line_up, t_more_position, t_clock_turn],
                       [t_halves, t_face, t_three_q, t_two_halves, t_turn_sum, t_turn_sum, t_clock_turn]),
                   [t_turn_pic, t_grid])


def _cnt(k):
    """A count before a coin ("four 5p coins", not "4 5p coins", which reads as 45p)."""
    return _COUNT_WORDS[k] if 0 <= k < len(_COUNT_WORDS) else str(k)


_COUNT_WORDS = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"]
