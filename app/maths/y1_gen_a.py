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

    return _pick_t([t_next, t_missing, t_across_ten, t_before], [t_line])


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
                "solution": ["%s is %d tens and %d ones." % (n_words(n), n // 10, n % 10)]}

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

    return _pick_t([t_next, t_missing, t_socks], [t_groups, t_line])


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
        return _tb("%s has %d %s. %s gets one more. How many now?" % (kid, n, t[0], kid), n + 1, "int", {},
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
        return _wq("%s has %d stickers, %s has %d and %s has %d. Who has the most?" % (kids[0], vals[0], kids[1], vals[1],
                                                                                      kids[2], vals[2]),
                   kids[vals.index(max(vals))], ["%d is the biggest number." % max(vals)], "name")

    def t_fewer():
        vals = random.sample(range(1, 20), 2)
        kids = random.sample(KIDS, 2)
        return _wq("%s has %d marbles. %s has %d marbles. Who has fewer?" % (kids[0], vals[0], kids[1], vals[1]),
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
        return _tb("How many tens are in %d?" % n, n // 10, "int", {}, ["%d = %d tens and %d ones." % (n, n // 10, n % 10)])

    def t_ones():
        return _tb("How many ones are in %d?" % n, n % 10, "int", {}, ["%d = %d tens and %d ones." % (n, n // 10, n % 10)])

    def t_build():
        return {"prompt": "Make %d with tens and ones." % n, "component": "base_ten", "spec": {"mode": "build", "max": 9},
                "answer": n, "answer_type": "int", "solution": ["%d tens and %d ones." % (n // 10, n % 10)]}

    def t_from_parts():
        return _tb("%d tens and %d ones make what number?" % (n // 10, n % 10), n, "int", {}, ["%d." % n])

    return _pick_t([t_tens, t_ones, t_from_parts], [t_build])


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

    return _pick_t([t_missing, t_take, t_word, t_partner])


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
        return _tb("10 + %d = ___" % k, 10 + k, "int", {}, ["Ten and %d ones is %d." % (k, 10 + k)])

    return _pick_t([t_missing, t_sub, t_related, t_double, t_ten_plus])


@skill("Y1.1.c", "Add and subtract within 20", S1)
def _(d=1):
    d = _d(d)
    a = random.randint(1, _by(d, 10, 15, 19))
    b = random.randint(0, 20 - a)

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

    return _pick_t([t_add, t_sub, t_zero], [t_line_add, t_line_sub])


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

    return _pick_t([t_left, t_sub_missing, t_true, t_sign])


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
        return _tb("%d people are on a bus. %d get off. How many are on the bus now?" % (on, off), on - off, "int", {},
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
    g, p = random.randint(2, 5), pick([2, 5, 10]) if d else random.randint(2, 5)

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

    return _pick_t([t_word, t_legs], [t_groups, t_array])


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

    return _pick_t([t_share, t_group, t_half], [t_pic])


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

    return _pick_t([t_quantity, t_word, t_equal], [t_shape, t_bar4])


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

    return _pick_t([t_quantity, t_parts, t_pizza], [t_shape, t_groups])


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

    return _pick_t([t_hand, t_later, t_long_hand], [t_oclock, t_half])


# ================================================================== 1.5 ======
@skill("Y1.5.a", "Name 2-D and 3-D shapes", S5)
def _(d=1):
    d = _d(d)

    def t_2d():
        name = pick(["triangle", "square", "rectangle", "pentagon", "hexagon"] if d else ["triangle", "square", "rectangle"])
        return {"prompt": "What is this shape called?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is a %s." % name]}

    def t_3d():
        name = pick(["cube", "cuboid", "square-based pyramid"])
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

    return _pick_t([t_sides, t_object, t_circle], [t_2d, t_3d])


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
        start, opp = pick([("the door", "the window"), ("the board", "the back wall")])
        return _wq("You face %s and make a whole turn. What do you face now? (type the same thing again if it has not changed)"
                   % start, start, ["A whole turn brings you back to the start."], "type it")

    def t_position():
        q, a = pick([("The cat is ON the mat. Is the mat above or below the cat?", "below"),
                     ("The bird is flying OVER the tree. Is the bird above or below the tree?", "above"),
                     ("Sam is standing BEHIND Mia. Who is in front?", "Mia")])
        return _wq(q, a, ["Use position words."], "word")

    def t_half_turn():
        return _tb("How many half turns make a whole turn?", 2, "int", {}, ["2 half turns make a whole turn."])

    return _pick_t([t_halves, t_face, t_position, t_half_turn], [t_turn_pic])
