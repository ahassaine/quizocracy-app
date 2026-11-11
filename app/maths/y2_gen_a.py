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


# Division whys for Year 2: the counting or the multiplication fact first (÷ is new), then the ÷ fact.
def _groups_why(tot, t, what):
    """How many groups of t make tot: "Count in 5s to 20: 5, 10, 15, 20. That is 4 bags." """
    k = tot // t
    if k <= 12:
        return "Count in %ds to %d: %s. That is %s." % (t, tot, ", ".join(str(t * i) for i in range(1, k + 1)), _pn(k, what))
    return "%d × %d = %d, so that is %s." % (k, t, tot, _pn(k, what))


def _share_why(tot, g, what="each"):
    """tot shared into g equal groups: "4 × 5 = 20, so 20 shared between 4 is 5 each." """
    k = tot // g
    return "%d × %d = %d, so %d shared into %d equal groups is %d %s." % (g, k, tot, tot, g, k, what)


# Why a unit fits, for each everyday thing a Year 2 question names (a word of the question is the key).
_SIZE_WHY = [("pencil", "A pencil is short enough to measure with a ruler, so centimetres."),
             ("potatoes", "A bag of potatoes is heavy to carry, so kilograms."),
             ("bath", "A bath holds a lot of water, so litres."),
             ("door", "A door is taller than a grown-up: about 2 metres."),
             ("sweet", "A sweet is very light, so grams."),
             ("medicine", "A spoon holds only a little, so millilitres."),
             ("playground", "A playground is many big steps long, so metres."),
             ("book", "A book is narrower than a ruler is long, so centimetres."),
             ("apple", "An apple is light: about 100 grams."),
             ("car", "A car is very heavy, so kilograms."),
             ("fish tank", "A fish tank holds a lot of water, so litres."),
             ("glass of milk", "A glass holds only a little, so millilitres."),
             ("paper clip", "A paper clip is tiny, much shorter than a ruler: about 3 centimetres."),
             ("hot summer", "95 °C is nearly as hot as boiling water. A hot summer day is about 25 °C."),
             ("cold winter", "40 °C would be a very hot day. A cold winter day is about 2 °C."),
             ("sugar", "A bag of sugar is heavy for its size: about 1 kilogram. 1 gram is as light as a paper clip."),
             ("cup holds", "200 litres would fill a bath. A cup holds about 200 millilitres."),
             ("child", "A child is much heavier than 25 grams (a few sweets): about 25 kilograms."),
             ("bucket", "10 millilitres is only two spoons. A bucket holds about 10 litres."),
             ("classroom", "8 centimetres is shorter than your hand. A classroom is about 8 metres long.")]


def _half_symbols(n, key):
    """A pictogram with half symbols: "2 whole symbols make 4, and half a symbol is 1 more: 5." """
    w, half = divmod(n, key)
    whole = "Each whole symbol is %d, so %s make%s %d" % (key, _pn(w, "whole symbol"), "s" if w == 1 else "", w * key)
    return whole + "." if not half else whole + ", and half a symbol is %d more: %d." % (half, n)


def _size_why(q):
    return next(w for k, w in _SIZE_WHY if k in q.lower())


# What each flat face looks like, for the faces of solids a Year 2 question asks about (the question is the key).
FACE_WHY = {"What 2-D shape is the flat face of a cylinder?": "A cylinder has a flat circle at each end.",
            "What 2-D shape are the faces of a cube?": "Every face of a cube is a square.",
            "What 2-D shape are the sloping faces of a pyramid?": "The sloping faces are triangles that meet at the top.",
            "What 2-D shape is the flat face of a cone?": "The flat face at the bottom of a cone is a circle.",
            "What 2-D shape are the two end faces of a triangular prism?": "A triangular prism has a triangle at each end.",
            "What 2-D shape is the bottom face of a square-based pyramid?": "Square-based means the bottom face is a square.",
            "What 2-D shape are the long side faces of a triangular prism?": "The long faces joining the two triangles are rectangles.",
            "Which 2-D shape do you see at each end of a cylinder?": "A cylinder has a flat circle at each end.",
            "Which 2-D shape is the bottom of a square-based pyramid?": "Square-based means the bottom face is a square.",
            "Which 2-D shape is at each end of a triangular prism?": "A triangular prism has a triangle at each end.",
            "Which 2-D shape is every face of a cube?": "Every face of a cube is a square."}


def _sub_steps(x, y):
    """A two-digit take-away in steps: "Take away the tens: 43 − 20 = 23. Then the ones: 23 − 9 = 14." """
    tens, ones = y // 10 * 10, y % 10
    if not tens or not ones:
        return "Take away the %s: %d − %d = %d." % ("tens" if tens else "ones", x, y, x - y)
    return "Take away the tens: %d − %d = %d. Then the ones: %d − %d = %d." % (x, tens, x - tens, x - tens, ones, x - y)


# Why one fraction of the same cake is bigger than another (Year 2: halves, thirds and quarters).
def _bigger_why(a, b):
    na, da = (int(x) for x in a.split("/"))
    nb, db = (int(x) for x in b.split("/"))
    names = {2: "halves", 3: "thirds", 4: "quarters"}
    if da == db:
        one = lambda n: "%d %s" % (n, names[da][:-1] if n == 1 else names[da])    # noqa: E731
        return "Both are %s of the same cake: %s %s more than %s." % (names[da], one(na), "is" if na == 1 else "are", one(nb))
    if na == nb == 1:
        return "Cut into %d equal parts, each part is bigger than when it is cut into %d. So %s is bigger." % (da, db, a)
    if (na, da) == (3, 4) and (nb, db) == (1, 2):
        return "1/2 is the same as 2/4, and 3 quarters is more than 2 quarters. So 3/4 is bigger."
    return "%s is bigger." % a


def _vals(d, lo, hi, k):
    """k different numbers in [lo, hi): at least 3 apart when easy, bunched together when hard."""
    if d == 0:
        for _ in range(50):
            v = random.sample(range(lo, hi), k)
            s = sorted(v)
            if all(b - a >= 3 for a, b in zip(s, s[1:])):
                return v
        return v
    if d == 2 and hi - lo > 2 * k + 3:
        base = random.randint(lo, hi - 2 * k - 3)
        return random.sample(range(base, base + 2 * k + 3), k)
    return random.sample(range(lo, hi), k)


# ================================================================== 2.0 ======
@skill("Y2.0.a", "Count in 2s, 3s, 5s and 10s", S0)
def _(d=1):
    d = _d(d)
    step = pick(_by(d, [2, 5, 10], [2, 3, 5, 10], [2, 3, 3, 5, 10]))   # 3s are the least familiar
    k = random.randint(_by(d, 1, 2, 4), _by(d, 5, 8, 9))
    kn = min(k, 100 // step - 3)                        # runs of four multiples that stay within 100

    def t_next():
        s = [step * i for i in range(kn, kn + 3)]
        return _tb("Count in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] + step, "int", {}, ["Add %d." % step])

    def t_back():
        s = [step * i for i in range(kn + 3, kn, -1)]
        return _tb("Count back in %ss:  %s, ___" % (step, ", ".join(map(str, s))), s[-1] - step, "int", {}, ["Take away %d." % step])

    def t_tens_any():
        start = random.randint(1, 9) + 10 * random.randint(0, _by(d, 1, 3, 5))
        s = [start + 10 * i for i in range(4)]
        return _tb("Count on in 10s:  %s, ___" % ", ".join(map(str, s)), s[-1] + 10, "int", {}, ["The ones digit stays the same."])

    def t_missing():
        first = min(k, 100 // step - 5) if d == 2 else 1     # stretch: start part-way along, stay within 100
        s = [step * i for i in range(first, first + 6)]
        j = random.randint(1, 4)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == j else str(v) for i, v in enumerate(s)), s[j], "int",
                   {}, ["Count in %ss." % step])

    def t_line():
        return _nl("Start at 0 and make %s of %d. Where do you land?" % (_pn(k, "jump"), step), k * step, step, 10,
                   ["%s of %d: count in %ds, %s." % (_pn(k, "jump"), step, step, ", ".join(str(step * i) for i in range(1, k + 1)))], lo=0, hi=min(100, max(30, (k * step // 10 + 1) * 10)))

    def t_back_tens():
        start = random.randint(1, 9) + 10 * random.randint(5, 9)
        s = [start - 10 * i for i in range(4)]
        return _tb("Count back in 10s:  %s, ___" % ", ".join(map(str, s)), s[-1] - 10, "int", {}, ["Take away 10; the ones digit stays the same."])

    def t_threes():
        n = random.randint(2, 8)
        return _tb("A tricycle has 3 wheels. How many wheels are on %s? Count in 3s." % _pn(n, "tricycle"), 3 * n, "int", {},
                   ["Count in %ds: %s. That makes %d." % (3, ", ".join(str(3 * i) for i in range(1, n + 1)), 3 * n)])

    def t_jumps():
        return _tb("How many jumps of %d take you from 0 to %d?" % (step, k * step), k, "int", {},
                   ["%s: %s." % (", ".join(str(step * i) for i in range(1, k + 1)), _pn(k, "jump"))])

    def t_in_count():
        n = step * random.randint(2, min(10, 98 // step)) + pick([0, 0, 1, 2 if step > 2 else 1])
        return _wq("Do you say %d when you count in %ss from 0? (yes or no)" % (n, step), "yes" if n % step == 0 else "no",
                   ["Counting in %ss: %s." % (step, ", ".join(str(step * i) for i in range(1, 11)))], "yes / no")

    def t_line_back():
        top = step * random.randint(k + 1, min(k + 4, 100 // step))
        return _nl("Start at %d and make %s back of %d. Where do you land?" % (top, _pn(k, "jump"), step), top - k * step, step, 10,
                   ["%d − %d = %d." % (top, k * step, top - k * step)], lo=0, hi=min(100, max(30, (top // 10 + 1) * 10)))

    def t_missing_tens():
        start = random.randint(1, 9) + 10 * random.randint(0, _by(d, 1, 4, 5))
        s = [start + 10 * i for i in range(5)]
        j = random.randint(1, 3)
        return _tb("Find the missing number:  %s" % ", ".join("___" if i == j else str(v) for i, v in enumerate(s)), s[j], "int", {},
                   ["The numbers go up in 10s."])

    def t_money():
        c = pick([2, 5, 10])
        return _tb("%s has %s %dp coin%s. How much money is that, in pence?" % (_kid(), _cnt(k), c, "" if k == 1 else "s"), c * k, "int", {"unit": "p"},
                   ["Count in %ss: %d." % (c, c * k)])

    if d == 0:     # counting on from small multiples; no counting back past the start of the tables
        return _pick_t([t_next, t_tens_any, t_missing, t_jumps, t_money], [t_line])
    plain = [t_next, t_back, t_tens_any, t_missing, t_back_tens, t_threes, t_jumps, t_in_count, t_missing_tens, t_money]
    if d == 2:     # stretch: more missing-number, counting-back and "do you say it?" reasoning
        plain += [t_missing, t_back, t_in_count, t_missing_tens]
    return _pick_t(plain, [t_line, t_line_back])


@skill("Y2.0.b", "Tens and ones in two-digit numbers", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 11, 11, 21), _by(d, 59, 99, 99))

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
        t, o = random.randint(1, _by(d, 5, 9, 9)), random.randint(1, _by(d, 5, 9, 9))
        return _tb("%s has %s 10p coin%s and %s 1p coin%s. How many pence is that?" % (_kid(), _cnt(t), "" if t == 1 else "s", _cnt(o), "" if o == 1 else "s"), 10 * t + o, "int",
                   {"unit": "p"}, ["%s: %dp." % (_tn(t, o), 10 * t + o)])

    def t_digit_place():
        m = random.choice([x for x in range(12, 99) if x % 10 and x // 10 != x % 10])
        which = pick(["tens", "ones"])
        return _tb("Which digit is in the %s place in %d?" % (which, m), m // 10 if which == "tens" else m % 10, "int", {},
                   ["%d: tens digit %d, ones digit %d." % (m, m // 10, m % 10)])

    def t_line():
        return _nl("Put %d on the number line." % n, n, 1, 10, ["%d is %s." % (n, _tn(n // 10, n % 10))], lo=0, hi=100)

    if d == 0:     # read tens and ones straight off; no regrouping
        return _pick_t([t_value, t_partition, t_parts, t_how_many_tens, t_ten_more, t_ten_less, t_coins, t_digit_place],
                       [t_build, t_line])
    plain = [t_value, t_partition, t_parts, t_other_way, t_ones_worth, t_how_many_tens, t_ten_more, t_ten_less, t_swap,
             t_split, t_coins, t_digit_place]
    if d == 2:     # stretch: regroup a ten, split in other ways, swap digits
        plain += [t_other_way, t_other_way, t_split, t_split, t_swap]
    return _pick_t(plain, [t_build, t_line])


@skill("Y2.0.c", "Compare and order numbers to 100 with <, > and =", S0)
def _(d=1):
    d = _d(d)
    a, b = _vals(d, 1, _by(d, 50, 100, 100), 2)     # stretch: two numbers close together

    def t_symbol():
        return _wq("Write < or > :  %d ___ %d" % (a, b), "<" if a < b else ">", ["%d is %s than %d." % (a, "less" if a < b else "more", b)],
                   "< or >")

    def t_equal():
        # = means "the same value as": a number and its tens and ones, the wrong one with the digits swapped
        # (stretch: two ways of splitting it, one of them with a ten moved into the ones)
        t, o = random.randint(2, 9), random.randint(1, 9)
        while o == t:
            o = random.randint(1, 9)
        n, right = 10 * t + o, random.random() < 0.5
        if d == 2:
            other = "%d + %d" % (10 * (t - 1), 10 + o) if right else "%d + %d" % (10 * (t - 1), o)
            return _wq("Is this true?  %d + %d = %s  (yes or no)" % (10 * t, o, other), "yes" if right else "no",
                       ["%d + %d = %d." % (10 * t, o, n),
                        "%s = %d, %s." % (other, 10 * (t - 1) + (10 + o if right else o),
                                          "so both sides are the same" if right else "so the sides are not the same")], "yes / no")
        parts = "%d + %d" % (10 * t, o) if right else "%d + %d" % (10 * o, t)
        return _wq("Is this true?  %d = %s  (yes or no)" % (n, parts), "yes" if right else "no",
                   ["%d is %d tens and %s: %d + %d." % (n, t, _pn(o, "one"), 10 * t, o)] +
                   ([] if right else ["%s = %d, so the two sides are not the same." % (parts, 10 * o + t)]), "yes / no")

    def t_order():
        vals = _vals(d, 1, _by(d, 50, 100, 100), 4)
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
        if d == 2 and 10 <= x + y - p + 1 <= 40:     # stretch: totals within 1 of each other
            q = x + y - p + pick([-1, 0, 1])
        sym = "<" if x + y < p + q else (">" if x + y > p + q else "=")
        return _wq("Write <, > or = :  %d + %d ___ %d + %d" % (x, y, p, q), sym,
                   ["%d + %d = %d and %d + %d = %d." % (x, y, x + y, p, q, p + q)], "<, > or =")

    def t_smallest():
        ds = random.sample(range(1, 10), 2)
        return _tb("Use the digits %d and %d to make the smallest two-digit number." % tuple(ds), min(ds) * 10 + max(ds), "int", {},
                   ["Put the smaller digit in the tens place."])

    def t_order_down():
        vals = _vals(d, 1, _by(d, 50, 100, 100), 4)
        k = random.randint(1, 4)
        return _tb("Put these in order, largest first. Which is number %d in the list?  %s" % (k, ", ".join(map(str, vals))),
                   sorted(vals, reverse=True)[k - 1], "int", {}, ["In order: %s." % ", ".join(map(str, sorted(vals, reverse=True)))])

    def t_tens_vs():
        t = random.randint(2, 9)
        m = 10 * t + random.choice([-3, -2, -1, 1, 2, 3])
        return _tb("Which is greater: %d tens or %d? Type the greater number." % (t, m), max(10 * t, m), "int", {},
                   ["%d tens is %d, and %d is %s than %d." % (t, 10 * t, 10 * t, "more" if 10 * t > m else "less", m)])

    def t_true():
        x, y = _vals(d, 10, _by(d, 50, 100, 100), 2)
        sym = pick(["<", ">"])
        right = (x < y) if sym == "<" else (x > y)
        return _wq("Is this true?  %d %s %d  (yes or no)" % (x, sym, y), "yes" if right else "no",
                   ["%d is %s than %d." % (x, "less" if x < y else "more", y)], "yes / no")

    if d == 0:     # compare and order plain numbers; no calculations either side
        return _pick_t([t_symbol, t_order, t_biggest, t_smallest, t_order_down, t_tens_vs, t_true], [t_line])
    plain = [t_symbol, t_equal, t_order, t_biggest, t_sym3, t_compare_sums, t_smallest, t_order_down, t_tens_vs, t_true]
    if d == 2:     # stretch: work out one or both sides before comparing
        plain += [t_sym3, t_compare_sums, t_compare_sums, t_equal]
    return _pick_t(plain, [t_line])


@skill("Y2.0.d", "Read and write numbers to 100 in numerals and words", S0)
def _(d=1):
    d = _d(d)
    if d == 0:     # teens and whole tens
        n = pick(list(range(11, 21)) + [30, 40, 50, 60, 70, 80, 90])
    elif d == 2:   # hyphenated numbers, where most spelling and digit-order slips happen
        n = pick([x for x in range(21, 100) if x % 10])
    else:
        n = random.randint(11, 100)

    def t_to_num():
        return _tb("Write in digits: %s" % n_words(n), n, "int", {}, ["%s = %d." % (n_words(n), n)])

    def t_to_word():
        return _wq("Write %d in words." % n, n_words(n), ["%d = %s." % (n, n_words(n))], "words")

    def t_parts_word():
        t, o = divmod(n, 10)
        if n == 100 or o == 0:
            return t_to_word()
        return _wq("Write the number that has %s and %s in words." % (_pn(t, "ten"), _pn(o, "one")), n_words(n),
                   ["%s and %s make %d." % (_pn(t, "ten"), _pn(o, "one"), n), "%d = %s." % (n, n_words(n))], "words")

    def t_estimate():
        # the number is given in words: reading it is the skill, the line shows it
        n2 = 10 * random.randint(1, 9) if d == 0 else random.randint(10, 90)
        q = _nl("Find where %s goes on a line from 0 to 100, and mark it." % n_words(n2), n2, 1, 10,
                ["%s = %d." % (n_words(n2), n2), "About %d." % n2], lo=0, hi=100)
        q["tolerance"] = 3          # an estimate: a mark within 3 of the number counts
        return q

    if d == 2:     # stretch: more writing in words
        return _pick_t([t_to_num, t_to_word, t_to_word, t_parts_word], [t_estimate])
    return _pick_t([t_to_num, t_to_word, t_parts_word], [t_estimate])


# ================================================================== 2.1 ======
@skill("Y2.1.a", "Addition and subtraction facts to 20 and related facts to 100", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(_by(d, 1, 3, 5), _by(d, 6, 10, 10)), random.randint(_by(d, 1, 3, 5), _by(d, 6, 10, 10))
    p = random.randint(_by(d, 1, 1, 3), _by(d, 4, 9, 8))
    q = random.randint(_by(d, 1, 1, 2), _by(d, 5, 10, 10) - p)      # tens facts stay within 100 (easy: within 50)

    def t_fact():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_sub_fact():
        return _tb("%d − %d = ___" % (a + b, b), a, "int", {}, ["%d + %d = %d." % (a, b, a + b)])

    def t_tens():
        return _tb("%d + %d = ___" % (10 * p, 10 * q), 10 * (p + q), "int", {}, ["%d + %d = %d, so %d." % (p, q, p + q, 10 * (p + q))])

    def t_bond100():
        t = random.randint(_by(d, 5, 1, 1), 9) * 10
        sol = ["%d + %d = 10, so %d + %d = 100." % (t // 10, 10 - t // 10, t, 100 - t)]
        if d == 2:                                      # hard: the missing number first, or the = sign on the left
            return _tb("___ + %d = 100" % t, 100 - t, "int", {}, sol) if random.random() < 0.5 else \
                _tb("100 = %d + ___" % t, 100 - t, "int", {}, sol)
        return _tb("%d + ___ = 100" % t, 100 - t, "int", {}, sol)

    def t_related():
        if d == 2 and random.random() < 0.5:            # hard: a related subtraction fact
            return _tb("%d − %d = %d. Use this to work out %d − %d." % (a + b, b, a, a + b + 10, b), a + 10, "int", {},
                       ["%d is 10 more than %d, so the answer is 10 more." % (a + b + 10, a + b)])
        return _tb("%d + %d = %d. Use this to work out %d + %d." % (a, b, a + b, a, b + 10), a + b + 10, "int", {},
                   ["%d is 10 more than %d, so the answer is 10 more." % (b + 10, b)])

    def t_sub_tens():
        return _tb("%d − %d = ___" % (10 * (p + q), 10 * q), 10 * p, "int", {}, ["%d − %d = %d, so %d." % (p + q, q, p, 10 * p)])

    def t_bond20():
        k = random.randint(_by(d, 10, 1, 1), 19)       # easy: from a teen number
        if d == 2:                                      # hard: take away a missing number
            return _tb("20 − ___ = %d" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])
        return _tb("%d + ___ = 20" % k, 20 - k, "int", {}, ["%d and %d make 20." % (k, 20 - k)])

    def t_from100():
        t = random.randint(_by(d, 5, 1, 1), 9) * 10
        if d == 2:
            return _tb("100 − ___ = %d" % (100 - t), t, "int", {}, ["%d + %d = 100." % (t, 100 - t)])
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
        k = random.randint(_by(d, 1, 1, 2), _by(d, 3, 5, 5))
        if d == 2:                                      # hard: the inverse, halving
            return _tb("Double ___ = %d" % (20 * k), 10 * k, "int", {}, ["Half of %d is %d, so double %d is %d." % (2 * k, k, 10 * k, 20 * k)])
        return _tb("Double %d = ___" % (10 * k), 20 * k, "int", {}, ["Double %d is %d, so double %d is %d." % (k, 2 * k, 10 * k, 20 * k)])

    def t_true():
        right = random.random() < 0.5
        shown = p + q if right else p + q + pick([-1, 1])
        return _wq("Is this true?  %d + %d = %d  (yes or no)" % (10 * p, 10 * q, 10 * shown), "yes" if right else "no",
                   ["%d + %d = %d." % (10 * p, 10 * q, 10 * (p + q))], "yes / no")

    def t_line():
        return _nl(_jump(10 * p, 10 * q), 10 * (p + q), 10, 10,
                   ["%d + %d = %d." % (10 * p, 10 * q, 10 * (p + q))], lo=0, hi=100)

    return _pick_t([t_fact, t_sub_fact, t_tens, t_bond100, t_related, t_sub_tens, t_bond20, t_from100, t_word, t_double_tens, t_true],
                   [t_bar, t_line])


@skill("Y2.1.b", "Add and subtract two-digit numbers and ones or tens", S1)
def _(d=1):
    d = _d(d)
    if d == 1:
        n = random.randint(11, 89)
    else:          # ones digit 1-8, so ones can always be added or taken without (easy) or with (stretch) crossing a ten
        n = pick([x for x in range(_by(d, 11, 11, 21), 89) if 1 <= x % 10 <= 8])

    def _ones(sub, lo=1):
        """A one-digit number to add or take: easy never crosses a ten, stretch always does."""
        o = n % 10
        if d == 0:
            return random.randint(1, o if sub else 9 - o)
        if d == 2:
            return random.randint(o + 1, 9) if sub else random.randint(10 - o, 9)
        return random.randint(lo, 9)

    def _tens():
        return random.randint(1, min(_by(d, 2, 9, 9), (99 - n) // 10)) * 10 if n < 90 else 10

    def t_add_ones():
        k = _ones(False)
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["Count on %d." % k])

    def t_sub_ones():
        k = _ones(True)
        return _tb("%d − %d = ___" % (n, k), n - k, "int", {}, ["Count back %d." % k])

    def t_add_tens():
        k = _tens()
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["The tens digit goes up; the ones stay the same."])

    def t_sub_tens():
        k = random.randint(1, n // 10) * 10
        return _tb("%d − %d = ___" % (n, k), n - k, "int", {}, ["The tens digit goes down; the ones stay the same."])

    def t_line():
        k = _ones(False, 2)
        return _nl(_jump(n, k), n + k, 1, 10, ["%d + %d = %d." % (n, k, n + k)],
                   lo=(n // 10) * 10, hi=(n // 10) * 10 + 20)

    def t_bridge():
        o = n % 10
        if d == 2:     # stretch: always goes through the next ten (n's ones digit is 1-8)
            k = random.randint(max(2, 11 - o), 9) if o >= 2 else 9
        else:
            k = random.randint(max(1, 11 - o), 9) if o >= 2 and n < 90 else random.randint(1, 9)
        return _tb("%d + %d = ___" % (n, k), n + k, "int", {}, ["%d + %d = %d, then + %d = %d." % (n, 10 - o, n + 10 - o, k - (10 - o), n + k)]
                   if o and k > 10 - o else ["Count on %d: %d." % (k, n + k)])

    def t_word_tens():
        k = _tens()
        return _tb("%s has %d stickers and gets %d more. How many stickers now?" % (_kid(), n, k), n + k, "int", {},
                   ["%d + %d = %d." % (n, k, n + k)])

    def t_word_ones():
        k = _ones(True)
        return _tb("A shop has %d apples. It sells %s. How many are left?" % (n, _pn(k, "apple")), n - k, "int", {},
                   ["%d − %d = %d." % (n, k, n - k)])

    def t_missing():
        k = _tens()
        return _tb("%d + ___ = %d" % (n, n + k), k, "int", {}, ["The tens digit went up by %d, so %d." % (k // 10, k)])

    def t_blocks():
        k = _tens()
        return {"prompt": "Work out %d + %d. Make the answer with the blocks." % (n, k), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": n + k, "answer_type": "int", "solution": ["Adding %d puts %s more: %d + %d = %d." % (k, _pn(k // 10, "ten"), n, k, n + k)]}

    def t_line_back():
        k = _ones(True, 2)
        return _nl(_jump(n, k, back=True), n - k, 1, 10, ["%d − %d = %d." % (n, k, n - k)],
                   lo=max(0, (n // 10) * 10 - 10), hi=max(0, (n // 10) * 10 - 10) + 20)

    def t_money():
        k = pick([10, 20, 30])
        m = min(n, 99 - k)
        return _tb("%s has %dp and is given %dp more. How much now, in pence?" % (_kid(), m, k), m + k, "int", {"unit": "p"},
                   ["%d + %d = %d." % (m, k, m + k)])

    plain = [t_add_ones, t_sub_ones, t_add_tens, t_sub_tens, t_bridge, t_word_tens, t_word_ones, t_missing, t_money]
    if d == 0:     # no bridging through a ten
        plain.remove(t_bridge)
    elif d == 2:   # stretch: bridging and missing numbers
        plain += [t_bridge, t_bridge, t_missing, t_sub_ones]
    return _pick_t(plain, [t_line, t_blocks, t_line_back])


@skill("Y2.1.c", "Add and subtract two two-digit numbers; add three one-digit numbers", S1)
def _(d=1):
    d = _d(d)
    a, b = random.randint(11, 60), random.randint(11, 39)
    for _ in range(200):
        # easy: no carrying when adding and no exchange when subtracting; stretch: both every time
        hi, lo = (a, b) if a >= b else (b, a)
        carry, exch = a % 10 + b % 10 >= 10, hi % 10 < lo % 10
        if d == 1 or (d == 0 and not carry and not exch) or (d == 2 and carry and exch and a != b):
            break
        a, b = random.randint(11, _by(d, 50, 60, 60)), random.randint(11, 39)
    s1, s2 = _by(d, 1, 1, 4), _by(d, 5, 9, 9)     # three one-digit numbers: small, or all bigger

    def t_add():
        return _tb("%d + %d = ___" % (a, b), a + b, "int", {}, ["Add the tens, then the ones: %d." % (a + b)])

    def t_sub():
        x, y = max(a, b), min(a, b)
        return _tb("%d − %d = ___" % (x, y), x - y, "int", {}, [_sub_steps(x, y)])

    def t_three():
        x, y, z = random.randint(s1, s2), random.randint(s1, s2), random.randint(s1, s2)
        return _tb("%d + %d + %d = ___" % (x, y, z), x + y + z, "int", {}, ["Look for a pair that makes 10."])

    def t_blocks():
        s = a + b
        if s > 99:
            return t_add()
        return {"prompt": "Work out %d + %d and make the answer with the blocks." % (a, b), "component": "base_ten",
                "spec": {"mode": "build", "max": 9}, "answer": s, "answer_type": "int", "solution": ["Add the tens, then the ones: %d + %d = %d, then %d + %d = %d." % (a, b // 10 * 10, a + b // 10 * 10, a + b // 10 * 10, b % 10, s)]}

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
        x, y, z = random.randint(s1, s2), random.randint(s1, s2), random.randint(s1, s2)
        return _tb("%s has %d red, %d blue and %d green pens. How many pens altogether?" % (_kid(), x, y, z), x + y + z, "int", {},
                   ["%d + %d + %d = %d." % (x, y, z, x + y + z)])

    def t_missing():
        return _tb("%d + ___ = %d" % (a, a + b), b, "int", {}, ["%d − %d = %d." % (a + b, a, b)])

    plain = [t_add, t_sub, t_three, t_word, t_three_word, t_missing]
    if d == 2:     # stretch: more subtraction with exchange and missing numbers
        plain += [t_sub, t_missing]
    return _pick_t(plain, [t_blocks, t_bar])


@skill("Y2.1.d", "Any order for addition; inverse and missing numbers", S1)
def _(d=1):
    d = _d(d)
    if d == 0:     # facts to 20
        a, b = random.randint(2, 10), random.randint(2, 10)
    elif d == 2:   # two two-digit numbers whose ones make more than 10
        a = pick([x for x in range(21, 60) if x % 10])
        b = 10 * random.randint(1, 3) + random.randint(10 - a % 10, 9)
    else:
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
        shown = a + b + (pick([o for o in (-1, 1, 10) if a + b + o <= 100]) if wrong else 0)    # shown sum stays within 100
        return _wq("Sam says %d + %d = %d. Check it by subtracting. Is Sam right? (yes or no)" % (a, b, shown), "no" if wrong else "yes",
                   ["%d − %d = %d%s." % (shown, b, shown - b, "" if not wrong else ", not %d" % a)], "yes / no")

    plain = [t_commute, t_not_commute, t_missing_add, t_missing_sub, t_check, t_missing_first, t_sub_gap, t_true_commute,
             t_family, t_think, t_check_answer]
    if d == 2:     # stretch: the missing number is the start or the amount taken away
        plain += [t_missing_sub, t_sub_gap, t_think, t_check_answer]
    return _pick_t(plain, [t_bar])


@skill("Y2.1.e", "Addition and subtraction problems", S1)
def _(d=1):
    d = _d(d)
    kid = _kid()

    def t_change():
        if d == 0:     # a multiple of 5 from 50p or £1
            cost, pay = 5 * random.randint(1, 9), pick([50, 100])
        else:
            cost, pay = random.randint(_by(d, 11, 11, 21), _by(d, 90, 90, 97)), _by(d, 50, pick([50, 100]), 100)
        if cost >= pay:
            pay = 100
        return _tb("%s buys a toy for %dp and pays with %s. How much change, in pence?" % (kid, cost, "£1" if pay == 100 else "50p"),
                   pay - cost, "int", {"unit": "p"},
                   ["%d − %d = %d." % (pay, cost, pay - cost)])

    def t_more():
        a, b = random.randint(10, _by(d, 30, 50, 59)), random.randint(5, _by(d, 9, 40, 39))
        return _tb("%s has %d stickers. Ben has %d more than %s. How many does Ben have?" % (kid, a, b, kid), a + b, "int", {},
                   ["%d + %d = %d." % (a, b, a + b)]) if kid != "Ben" else t_left()

    def t_left():
        a, b = random.randint(_by(d, 15, 30, 41), _by(d, 40, 90, 92)), random.randint(_by(d, 2, 5, 13), _by(d, 9, 25, 39))
        return _tb("A class had %d pencils. %d were lost. How many are left?" % (a, b), a - b, "int", {}, ["%d − %d = %d." % (a, b, a - b)])

    def t_two_step():
        a, c = random.randint(20, _by(d, 50, 50, 70)), random.randint(5, _by(d, 20, 20, 29))
        b = random.randint(5, min(_by(d, 20, 20, 29), a - 5))           # never more get off than are on the train
        return _tb("There were %d people on a train. %d got off and %d got on. How many now?" % (a, b, c), a - b + c, "int", {},
                   ["%d − %d = %d stay on; then %d + %d = %d." % (a, b, a - b, a - b, c, a - b + c)])

    def t_bar():
        whole, part = random.randint(_by(d, 20, 30, 50), _by(d, 50, 90, 99)), random.randint(10, _by(d, 15, 25, 39))
        return _strip("The bar shows %d altogether. One part is %d. What is the other part?" % (whole, part),
                      {"mode": "part_whole", "totalLabel": str(whole), "partLabel": str(part), "unknown": "part", "parts": 2},
                      whole - part, ["%d − %d = %d." % (whole, part, whole - part)])

    def t_two_change():
        x, y = random.randint(15, 45), random.randint(15, 45)
        return _tb("%s buys a pen for %dp and a ruler for %dp, and pays with £1. How much change, in pence?" % (kid, x, y),
                   100 - x - y, "int", {"unit": "p"}, ["%d + %d = %d; 100 − %d = %d." % (x, y, x + y, x + y, 100 - x - y)])

    if d == 0:     # one step only
        return _pick_t([t_change, t_more, t_left], [t_bar])
    if d == 2:     # stretch: two steps, bigger numbers
        return _pick_t([t_change, t_more, t_left, t_two_step, t_two_step, t_two_change, t_two_change], [t_bar])
    return _pick_t([t_change, t_more, t_left, t_two_step], [t_bar])


# ================================================================== 2.2 ======
@skill("Y2.2.a", "The 2, 5 and 10 times tables", S2)
def _(d=1):
    d = _d(d)
    t = pick([2, 5, 10])
    k = random.randint(_by(d, 1, 1, 6), _by(d, 6, 12, 12))     # stretch: the harder half of each table
    k = min(k, 100 // t)                                # products stay within 100 (10 × 10 at most)

    def t_mult():
        return _tb("%d × %d = ___" % (k, t), k * t, "int", {}, ["%s of %d: count in %ds to %d." % (_pn(k, "lot"), t, t, k * t)])

    def t_div():
        return _tb("%d ÷ %d = ___" % (k * t, t), k, "int", {}, ["How many %ss make %d? %d." % (t, k * t, k)])

    def t_missing():
        return _tb("___ × %d = %d" % (t, k * t), k, "int", {}, ["Count in %ds to %d: %s." % (t, k * t, ", ".join(str(t * i) for i in range(1, k + 1))),
                                                               "%d × %d = %d, so the missing number is %d." % (k, t, k * t, k)])

    def t_groups():
        g = random.randint(2, _by(d, 4, 6, 9))
        return {"prompt": "There are %d groups of %d. Write the total." % (g, t), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": t}, "answer": g * t, "answer_type": "int",
                "solution": ["%d × %d = %d." % (g, t, g * t)]}

    def t_array():
        g = random.randint(_by(d, 2, 2, 4), _by(d, 4, 6, 9))
        return {"prompt": "Build an array of %d rows of %d. How many altogether?" % (g, t), "component": "array",
                "spec": {"mode": "build", "maxRows": 10, "maxCols": 10, "targetRows": g, "targetCols": t}, "answer": g * t,
                "answer_type": "int", "solution": ["%d × %d = %d." % (g, t, g * t)]}

    def t_missing_div():
        return _tb("___ ÷ %d = %d" % (t, k), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_true():
        right = random.random() < 0.5
        shown = k * t if right else k * t + pick([o for o in (-t, t, 1) if k * t + o <= 100])
        return _wq("Is this true?  %d × %d = %d  (yes or no)" % (k, t, shown), "yes" if right else "no",
                   ["%d × %d = %d." % (k, t, k * t)], "yes / no")

    def t_word():
        what = {2: ("pair of socks", "pairs of socks", "socks"), 5: ("hand", "hands", "fingers"),
                10: ("pack of 10 pens", "packs of 10 pens", "pens")}[t]
        return _tb("How many %s are in %d %s?" % (what[2], k, what[0] if k == 1 else what[1]), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_line():
        return _nl("Count in %ds. Mark %d × %d on the number line." % (t, k, t), k * t, t, 10, ["Count in %ds: %s. So %d × %d = %d." % (t, ", ".join(str(t * i) for i in range(1, k + 1)), k, t, k * t)],
                   lo=0, hi=min(100, max(30, (k * t // 10 + 1) * 10)))

    def t_double():
        return _tb("Double %d = ___" % k, 2 * k, "int", {}, ["Double means × 2: %d × 2 = %d." % (k, 2 * k)])

    def t_which_table():
        x = pick([2, 5, 10])
        n = x * random.randint(1, min(12, 100 // x)) if random.random() < 0.5 else pick([v for v in range(3, min(12 * x, 100) + 1) if v % x])
        return _wq("Is %d in the %d times table? (yes or no)" % (n, x), "yes" if n % x == 0 else "no",
                   ["%d %s in the %d times table." % (n, "is" if n % x == 0 else "is not", x)], "yes / no")

    plain = [t_mult, t_div, t_missing, t_missing_div, t_true, t_word, t_double, t_which_table]
    if d == 0:     # mostly multiplying; no missing dividend
        plain.remove(t_missing_div)
    elif d == 2:   # stretch: division and missing numbers
        plain += [t_div, t_missing, t_missing_div, t_which_table]
    return _pick_t(plain, [t_groups, t_array, t_line])


@skill("Y2.2.b", "Odd and even numbers", S2)
def _(d=1):
    d = _d(d)

    def t_is():
        n = random.randint(_by(d, 1, 1, 21), _by(d, 20, 100, 100))
        return _wq("Is %d odd or even?" % n, "even" if n % 2 == 0 else "odd", ["Even numbers end in 0, 2, 4, 6 or 8."], "odd / even")

    def t_next_even():
        n = random.randint(_by(d, 1, 1, 21), _by(d, 18, 98, 98))
        nxt = n + 1 if n % 2 else n + 2
        return _tb("What is the next even number after %d?" % n, nxt, "int", {}, ["Even numbers end in 0, 2, 4, 6 or 8: the next one after %d is %d." % (n, nxt)])

    def t_count():
        lo = random.randint(1, _by(d, 10, 20, 60))
        hi = lo + random.randint(_by(d, 4, 5, 9), _by(d, 6, 10, 15))
        return _tb("How many odd numbers are there from %d to %d?" % (lo, hi), sum(1 for x in range(lo, hi + 1) if x % 2),
                   "int", {}, ["The odd numbers are %s: count them, %d." % (", ".join(str(x) for x in range(lo, hi + 1) if x % 2),
                                                                         sum(1 for x in range(lo, hi + 1) if x % 2))])

    def t_pairs():
        n = random.randint(4, _by(d, 12, 30, 50))
        return _wq("Can %d socks be put into pairs with none left over? (yes or no)" % n, "yes" if n % 2 == 0 else "no",
                   ["%d is %s." % (n, "even" if n % 2 == 0 else "odd")], "yes / no")

    def t_next_odd():
        n = random.randint(_by(d, 1, 1, 21), _by(d, 18, 98, 98))
        nxt = n + 1 if n % 2 == 0 else n + 2
        return _tb("What is the next odd number after %d?" % n, nxt, "int", {}, ["Odd numbers end in 1, 3, 5, 7 or 9: %d." % nxt])

    def t_prev_even():
        n = random.randint(_by(d, 3, 3, 21), _by(d, 20, 100, 100))
        prv = n - 1 if n % 2 else n - 2
        return _tb("What is the even number just before %d?" % n, prv, "int", {}, ["Even numbers end in 0, 2, 4, 6 or 8: just before %d, that is %d." % (n, prv)])

    def t_houses():
        k = random.randint(3, _by(d, 6, 12, 20))
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
        n = random.randint(2, _by(d, 6, 10, 10))
        extra = pick([0, 1])
        if extra:
            return _wq("%d counters are put into pairs. One counter is left without a partner. Is %d odd or even?" % (2 * n + 1, 2 * n + 1),
                       "odd", ["One is left without a partner, so it is odd."], "odd / even")
        return {"prompt": "Here are %d counters in pairs%s. Is %d odd or even?" % (2 * n + extra, " and one more" if extra else "",
                                                                                   2 * n + extra),
                "component": "equal_groups", "spec": {"mode": "read", "groups": n, "per": 2}, "answer": "odd" if extra else "even",
                "answer_type": "str", "solution": ["%s" % ("One is left without a partner, so it is odd." if extra else "Every counter has a partner, so it is even.")]}

    def t_teams():
        n = random.randint(6, _by(d, 20, 30, 60))
        return _wq("%d children get into pairs. Is anyone left without a partner? (yes or no)" % n, "yes" if n % 2 else "no",
                   ["%d is %s, so %s." % (n, "odd" if n % 2 else "even", "one child is left without a partner" if n % 2 else "everyone has a partner")], "yes / no")

    def t_sum_odd():
        x, y = random.randint(1, _by(d, 10, 20, 50)), random.randint(1, _by(d, 10, 20, 50))
        return _wq("Is %d + %d odd or even?" % (x, y), "even" if (x + y) % 2 == 0 else "odd", ["%d + %d = %d, which ends in %d, so it is %s." % (x, y, x + y, (x + y) % 10, "even" if (x + y) % 2 == 0 else "odd")], "odd / even")

    def t_line_even():
        n = random.randint(1, _by(d, 18, 48, 98))
        nxt = n + 1 if n % 2 else n + 2
        return _nl("Mark the first even number after %d on the number line." % n, nxt, 1, 10, ["%d ends in %d, so it is even; %d is odd." % (nxt, nxt % 10, nxt - 1)], lo=0,
                   hi=_by(d, 20, 50, 100))

    plain = [t_is, t_next_even, t_count, t_pairs, t_next_odd, t_prev_even, t_houses, t_biggest_even, t_teams, t_sum_odd]
    if d == 0:     # spot odd and even; no counting or making numbers
        plain = [t_is, t_next_even, t_pairs, t_next_odd, t_prev_even, t_teams]
    elif d == 2:   # stretch: reasoning about odd and even
        plain += [t_count, t_houses, t_biggest_even, t_sum_odd]
    return _pick_t(plain, [t_groups, t_line_even])


@skill("Y2.2.c", "Write and solve × and ÷ statements; any order for ×", S2)
def _(d=1):
    d = _d(d)
    a, b = pick([2, 5, 10]), random.randint(_by(d, 2, 2, 5), _by(d, 5, 10, 12))
    b = min(b, 100 // a)                                # products stay within 100

    def t_commute():
        bb = b if b != a else (b + 1 if a * (b + 1) <= 100 else b - 1)    # 5 × 5 swapped is the same sum
        return _tb("%d × %d = %d. What is %d × %d?" % (a, bb, a * bb, bb, a), a * bb, "int", {},
                   ["Multiplication can be done in any order.", "%d × %d = %d × %d = %d." % (bb, a, a, bb, a * bb)])

    def t_div_not():                                    # × can be swapped (yes), ÷ cannot (no)
        if random.random() < 0.5:
            return _wq("Is %d × %d the same as %d × %d? (yes or no)" % (a, b, b, a), "yes",
                       ["Multiplication can be done in any order: both are %d." % (a * b)], "yes / no")
        return _wq("Is %d ÷ %d the same as %d ÷ %d? (yes or no)" % (a * b, a, a, a * b), "no", ["Division cannot be done in any order."],
                   "yes / no")

    def t_repeated():
        return _tb("%s = ___" % " + ".join([str(a)] * b), a * b, "int", {}, ["%s of %d = %d × %d = %d." % (_pn(b, "lot"), a, b, a, a * b)])

    def t_fact_family():
        return _tb("%d × %d = %d. So %d ÷ %d = ___" % (a, b, a * b, a * b, b), a, "int", {},
                   ["%d × %d = %d, so %d groups of %d make %d: %d ÷ %d = %d. Dividing undoes multiplying." % (a, b, a * b, a, b, a * b, a * b, b, a)])

    def t_write():
        return _tb("What is %d groups of %d?" % (b, a), a * b, "int", {}, ["%d × %d = %d." % (b, a, a * b)])

    def t_missing():
        return _tb("%d × ___ = %d" % (a, a * b), b, "int", {}, ["%d × %d = %d, so the missing number is %d." % (a, b, a * b, b)])

    def t_div_write():
        return _tb("%d × %d = %d. Finish this division fact: %d ÷ %d = ___" % (b, a, a * b, a * b, a), b, "int", {},
                   ["%d ÷ %d = %d and %d ÷ %d = %d." % (a * b, b, a, a * b, a, b)])

    if d == 0:     # repeated addition and swapping the order
        return _pick_t([t_commute, t_repeated, t_fact_family, t_write])
    if d == 2:     # stretch: missing numbers and division facts, no repeated addition
        return _pick_t([t_commute, t_div_not, t_fact_family, t_write, t_missing, t_missing, t_div_write, t_div_write])
    return _pick_t([t_commute, t_div_not, t_repeated, t_fact_family, t_write])


@skill("Y2.2.d", "Multiplication and division problems", S2)
def _(d=1):
    d = _d(d)
    t = pick([2, 5, 10])
    k = random.randint(_by(d, 2, 2, 5), _by(d, 5, 10, 10))

    def t_bags():
        return _tb("There are %d bags with %d apples in each. How many apples?" % (k, t), k * t, "int", {}, ["%d × %d = %d." % (k, t, k * t)])

    def t_share():
        return _tb("%d sweets are shared equally between %d children. How many each?" % (k * t, t), k, "int", {},
                   [_share_why(k * t, t)])

    def t_coins():
        return _tb("How much are %s %dp coins worth, in pence?" % (_cnt(k), t), k * t, "int", {"unit": "p"}, ["%d × %d = %d." % (k, t, k * t)])

    def t_teams():
        return _tb("%d children make teams of %d. How many teams?" % (k * t, t), k, "int", {}, [_groups_why(k * t, t, "team")])

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
                   [_groups_why(k * t, t, "sticker")])

    def t_share_bar():
        return _strip("%d cakes are shared equally onto %d plates. How many on each plate?" % (k * t, t),
                      {"mode": "equal_parts", "parts": t, "partLabel": "?", "totalLabel": str(k * t), "unknown": "part"}, k,
                      [_share_why(k * t, t, "on each plate")]) if t <= 5 else t_share()

    def t_groups():
        return {"prompt": "%d sweets are put into bags of %d. How many bags?" % (k * t, t), "component": "equal_groups",
                "spec": {"mode": "read", "groups": k, "per": t}, "answer": k, "answer_type": "int",
                "solution": [_groups_why(k * t, t, "bag")]}

    def t_array():
        return {"prompt": "Chairs are in %d rows of %d. Build the array. How many chairs?" % (k, t), "component": "array",
                "spec": {"mode": "build", "maxRows": 10, "maxCols": 10, "targetRows": k, "targetCols": t}, "answer": k * t,
                "answer_type": "int", "solution": ["%d × %d = %d." % (k, t, k * t)]}

    def t_repeated():
        return _tb("A frog jumps %d cm each hop. How far does it go in %d hops, in cm?" % (t, k), k * t, "int", {"unit": "cm"},
                   ["%s = %d." % (" + ".join([str(t)] * k), k * t)])

    def t_two_step():
        g = random.randint(2, max(2, t))
        return _tb("There are %d boxes with %d pens in each. %d pens are taken out. How many pens are left?" % (k, t, g),
                   k * t - g, "int", {}, ["%d × %d = %d; %d − %d = %d." % (k, t, k * t, k * t, g, k * t - g)])

    plain = [t_bags, t_share, t_coins, t_teams, t_fingers, t_price, t_how_many_bought, t_repeated]
    if d == 0:     # mostly multiplying
        plain = [t_bags, t_coins, t_fingers, t_price, t_repeated, t_share]
    elif d == 2:   # stretch: grouping and sharing, and a second step
        plain += [t_share, t_teams, t_how_many_bought, t_two_step, t_two_step]
    return _pick_t(plain, [t_bar, t_share_bar, t_groups, t_array])


# ================================================================== 2.3 ======
@skill("Y2.3.a", "Find 1/3, 1/4, 2/4 and 3/4 of a shape", S3)
def _(d=1):
    d = _d(d)
    # easy: unit fractions; stretch: mostly non-unit fractions (2/4, 3/4)
    FR = _by(d, [(1, 2), (1, 4), (1, 3)], [(1, 3), (1, 4), (2, 4), (3, 4), (1, 2)], [(2, 4), (3, 4), (3, 4), (1, 3), (2, 4)])

    def t_shade():
        f = pick(FR)
        return {"prompt": "Shade %d/%d of the bar." % f, "component": "fraction_bar", "spec": {"parts": f[1], "mode": "shade"},
                "answer": "%d/%d" % f, "answer_type": "frac", "solution": ["Shade %d of the %d equal parts." % f]}

    def t_read():
        f = pick(FR)
        return _area("What fraction of the shape is shaded?", {"mode": "fraction_read", "parts": f[1], "shaded": f[0]},
                     "%d/%d" % f, ["%d out of %d equal parts." % f], atype="frac")

    def t_equiv():
        return _wq("Is 2/4 the same as 1/2? (yes or no)", "yes", ["2 quarters make a half."], "yes / no")

    def t_parts():
        n, name = pick([(3, "thirds"), (4, "quarters")])
        return _tb("How many %s make a whole?" % name, n, "int", {}, ["%d %s make 1 whole." % (n, name)])

    def t_left():
        f = pick(_by(d, [(1, 2), (3, 4)], [(1, 4), (3, 4), (2, 3)], [(1, 4), (3, 4), (2, 4)]))     # 2 of 3 eaten leaves 1/3
        return _fq("A cake is cut into %d equal pieces and %d %s eaten. What fraction is left? (like 1/4)" % (f[1], f[0],
                                                                                                              "is" if f[0] == 1 else "are"),
                   Fraction(f[1] - f[0], f[1]), ["%d out of %d pieces are left." % (f[1] - f[0], f[1])], "e.g. 1/4")   # 2/4 = 1/2 both count

    def t_grid():
        f = pick(FR)
        parts = f[1] * pick(_by(d, [1], [1, 2, 3], [2, 3]))     # stretch: more squares than parts
        return _area("Shade %d/%d of the shape." % f, {"mode": "fraction", "parts": parts}, "%d/%d" % f,
                     ["%d/%d of %d squares is %s." % (f[0], f[1], parts, _pn(parts * f[0] // f[1], "square"))], atype="frac")

    def t_bigger():
        a, b = pick(_by(d, [("1/2", "1/4"), ("3/4", "1/4")],
                        [("1/3", "1/4"), ("1/2", "1/4"), ("1/2", "1/3"), ("3/4", "1/4"), ("2/4", "1/4"), ("3/4", "1/2")],
                        [("1/3", "1/4"), ("1/2", "1/3"), ("3/4", "1/2"), ("3/4", "2/4")]))
        x, y = (a, b) if random.random() < 0.5 else (b, a)
        return _fq("Which is bigger, %s or %s of the same cake?" % (x, y), Fraction(a), [_bigger_why(a, b)])

    def t_is_third():
        sh = random.randint(1, 2)
        n = pick([3, 4])
        right = (n == 3 and sh == 1)
        return _area("A bar is cut into %d equal parts and %d %s shaded. Is one third shaded? (yes or no)"
                     % (n, sh, "is" if sh == 1 else "are"),
                     {"mode": "fraction_read", "parts": n, "rows": 1, "cols": n, "shaded": sh, "placeholder": "yes / no"},
                     "yes" if right else "no",
                     ["One third is 1 of 3 equal parts." if not right else "1 of 3 equal parts is one third."], atype="str")

    def t_name():
        f, w = pick([("1/3", "one third"), ("1/4", "one quarter"), ("3/4", "three quarters"), ("2/4", "two quarters")])
        return _fq("Write %s as a fraction (like 1/2)." % w, Fraction(f), ["%s = %s." % (w.capitalize(), f)])

    def t_unequal():
        return _wq("A pizza is cut into 4 pieces of different sizes. Is each piece a quarter? (yes or no)", "no",
                   ["Quarters must be 4 equal parts."], "yes / no")

    def t_how_many_more():
        f = pick(_by(d, [(1, 4), (2, 4)], [(1, 4), (2, 4), (1, 3)], [(1, 4), (3, 4), (1, 3)]))
        return _area("%d/%d of a bar is shaded. How many more %s must be shaded to fill it?" % (f[0], f[1], "quarters" if f[1] == 4 else "thirds"),
                     {"mode": "fraction_read", "parts": f[1], "rows": 1, "cols": f[1], "shaded": f[0], "placeholder": ""},
                     f[1] - f[0], ["%d/%d + %d/%d = 1 whole." % (f[0], f[1], f[1] - f[0], f[1])])

    def t_half_quarters():
        return _tb("How many quarters are the same as one half?", 2, "int", {}, ["2/4 = 1/2."])

    if d == 0:     # name and shade simple fractions
        return _pick_t([t_parts, t_left, t_bigger, t_name, t_unequal, t_half_quarters], [t_shade, t_read])
    plain = [t_equiv, t_parts, t_left, t_bigger, t_is_third, t_name, t_unequal, t_how_many_more, t_half_quarters]
    if d == 2:     # stretch: compare, complete the whole, judge a claim; drop the bare facts
        plain = [t_equiv, t_left, t_bigger, t_bigger, t_is_third, t_how_many_more, t_how_many_more, t_unequal]
    return _pick_t(plain, [t_shade, t_read, t_grid])


@skill("Y2.3.b", "Fractions of a set or quantity", S3)
def _(d=1):
    d = _d(d)

    def t_third():
        n = 3 * random.randint(_by(d, 1, 1, 4), _by(d, 5, 10, 12))
        return _tb("What is 1/3 of %d?" % n, n // 3, "int", {}, ["Share %d into 3 equal groups: %d." % (n, n // 3)])

    def t_quarter():
        n = 4 * random.randint(_by(d, 1, 1, 4), _by(d, 5, 10, 12))
        return _tb("What is 1/4 of %d?" % n, n // 4, "int", {}, ["Share %d into 4 equal groups: %d." % (n, n // 4)])

    def t_three_quarters():
        n = 4 * random.randint(_by(d, 1, 1, 3), _by(d, 4, 8, 10))
        return _tb("What is 3/4 of %d?" % n, 3 * n // 4, "int", {}, ["1/4 of %d is %d, so 3/4 is %d." % (n, n // 4, 3 * n // 4)])

    def t_half_of():
        n = 2 * random.randint(2, _by(d, 10, 15, 25))
        return _tb("1/2 of %d = ___" % n, n // 2, "int", {}, ["Half of %d is %d." % (n, n // 2)])

    def t_groups():
        k = random.randint(2, 6)
        g = pick([3, 4])
        return {"prompt": "Share the %d counters into %d equal groups. What is 1/%d of %d?" % (g * k, g, g, g * k), "component": "equal_groups",
                "spec": {"mode": "read", "groups": g, "per": k}, "answer": k, "answer_type": "int",
                "solution": ["One group has %d." % k]}

    def t_length():
        n = 4 * random.randint(2, _by(d, 5, 6, 10))
        return _tb("A ribbon is %d cm long. %s cuts off 1/4 of it. How long is the piece cut off, in cm?" % (n, _kid()), n // 4,
                   "int", {"unit": "cm"}, ["1/4 means 1 of 4 equal parts. " + _share_why(n, 4, "cm in each part")])

    def t_two_quarters():
        n = 4 * random.randint(_by(d, 1, 1, 3), _by(d, 5, 8, 10))
        return _tb("What is 2/4 of %d?" % n, n // 2, "int", {}, ["2/4 is the same as 1/2: half of %d is %d." % (n, n // 2)])

    def t_word_third():
        n = 3 * random.randint(2, _by(d, 5, 8, 12))
        kid = _kid()
        return _tb("%s has %d marbles and gives 1/3 of them away. How many marbles are given away?" % (kid, n), n // 3, "int", {},
                   ["1/3 means 1 of 3 equal parts. " + _share_why(n, 3, "in each part")])

    def t_left():
        n = 4 * random.randint(2, _by(d, 5, 6, 10))
        return _tb("There are %d biscuits. 1/4 of them are eaten. How many are left?" % n, n - n // 4, "int", {},
                   ["1/4 of %d is %d; %d − %d = %d." % (n, n // 4, n, n // 4, n - n // 4)])

    def t_strip():
        g = pick([3, 4])
        k = random.randint(2, _by(d, 5, 9, 9))
        return _strip("What is 1/%d of %d?" % (g, g * k), {"mode": "equal_parts", "parts": g, "partLabel": "?", "totalLabel": str(g * k),
                                                         "unknown": "part"}, k, [_share_why(g * k, g, "in each part")])

    def t_whole():
        k = random.randint(2, _by(d, 5, 10, 12))
        g = pick([2, 3, 4])
        return _tb("1/%d of a number is %d. What is the number?" % (g, k), g * k, "int", {}, ["%d × %d = %d." % (k, g, g * k)])

    def t_money():
        n = (pick([12, 20, 40, 60, 80, 100]) if random.random() < 0.5 else 4 * random.randint(2, 10)) if d else 4 * random.randint(2, 5)
        return _tb("%s has %dp and spends 1/4 of it. How much is spent, in pence?" % (_kid(), n), n // 4, "int", {"unit": "p"},
                   ["1/4 means 1 of 4 equal parts. " + _share_why(n, 4, "pence in each part")])

    plain = [t_third, t_quarter, t_three_quarters, t_half_of, t_length, t_two_quarters, t_word_third, t_left, t_whole, t_money]
    if d == 0:     # unit fractions of small numbers
        plain = [t_third, t_quarter, t_half_of, t_length, t_word_third, t_money]
    elif d == 2:   # stretch: 3/4, what is left, and the whole from a part
        plain += [t_three_quarters, t_three_quarters, t_left, t_whole, t_whole]
    return _pick_t(plain, [t_groups, t_strip])


# ================================================================== 2.4 ======
@skill("Y2.4.a", "Choose units and read scales", S4)
def _(d=1):
    d = _d(d)

    def t_unit():
        q, a = pick(_by(d, [("Would you measure the length of a pencil in cm or m?", "cm"),
                            ("Would you weigh a bag of potatoes in g or kg?", "kg"),
                            ("Would you measure a bath of water in ml or litres?", "litres")],
                        [("Would you measure the length of a pencil in cm or m?", "cm"),
                         ("Would you measure the height of a door in cm or m?", "m"),
                         ("Would you weigh a bag of potatoes in g or kg?", "kg"),
                         ("Would you weigh a sweet in g or kg?", "g"),
                         ("Would you measure a bath of water in ml or litres?", "litres"),
                         ("Would you measure a spoon of medicine in ml or litres?", "ml")],
                        [("Would you measure the length of a playground in cm or m?", "m"),
                         ("Would you measure the width of a book in cm or m?", "cm"),
                         ("Would you weigh an apple in g or kg?", "g"),
                         ("Would you weigh a car in g or kg?", "kg"),
                         ("Would you measure the water in a fish tank in ml or litres?", "litres"),
                         ("Would you measure a glass of milk in ml or litres?", "ml")]))       # hard: less obvious objects
        return _wq(q, a, [_size_why(q)], "unit")

    def t_ruler():
        mx = _by(d, 10, 20, 30)
        cm = random.randint(_by(d, 2, 3, 11), mx - 1)
        return {"prompt": "How long is it, in cm?", "component": "ruler", "spec": {"mode": "length", "value": cm, "max": mx, "unit": "cm"},
                "answer": cm, "answer_type": "num", "tolerance": 0.5, "solution": ["Start at 0: it ends at %d cm." % cm]}

    def t_scale():
        mx = _by(d, 10, pick([10, 20]), 50)
        v = 2 * random.randint(1, 24) if d == 2 else random.randint(1, mx - 1)      # hard: a 0-50 dial marked in 2s
        return {"prompt": "Read the scale. How many kg?", "component": "ruler", "spec": {"mode": "mass", "value": v, "max": mx, "unit": "kg"},
                "answer": v, "answer_type": "num", "tolerance": 0.5, "solution": ["The pointer is on %d kg." % v]}

    def t_jug():                                        # readings stay within 100
        v = random.randint(1, 19) * 5 if d == 2 else random.randint(1, _by(d, 4, 9, 9)) * 10     # hard: 5 ml lines
        return {"prompt": "How much water is in the jug, in ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": _by(d, 50, 100, 100), "unit": "ml"}, "answer": v, "answer_type": "num",
                "tolerance": _by(d, 5, 5, 2), "solution": ["The water is level with the %d ml line." % v]}

    def t_thermo():
        # reading a thermometer between its numbered lines: numbered in 10s, with marks in 2s or 5s
        # (hard: counting back down from the line above)
        step = _by(d, 2, pick([2, 5]), 2)
        line = 10 * random.randint(1, 3)
        k = random.randint(1, 10 // step - 1)
        up = d == 0 or (d == 1 and random.random() < 0.5)
        t = line + k * step if up else line - k * step
        return _tb("A thermometer is numbered in 10s, with a mark every %d degrees. The red line is %s %s the %d °C line. "
                   "What temperature does it show, in °C?" % (step, _pn(k, "mark"), "above" if up else "below", line),
                   t, "int", {"unit": "°C"},
                   ["Each mark is %d degrees, so %s %d degrees." % (step, "1 mark is" if k == 1 else "%d marks are" % k, k * step),
                    "%d %s %d = %d °C." % (line, "+" if up else "−", k * step, t)])

    def t_temp():
        if d == 2:                                      # hard: three readings, warmest or coldest
            v = random.sample(range(0, 35), 3)
            hot = random.random() < 0.5
            w = max(v) if hot else min(v)
            return _tb("Which is %s: %s? Type the number." % ("warmest" if hot else "coldest", ", ".join("%d °C" % x for x in v)), w, "int",
                       {}, ["%d is the %s." % (w, "highest" if hot else "lowest")])
        a, b = random.sample(range(0, _by(d, 20, 35, 35)), 2)
        return _tb("Which is warmer, %d °C or %d °C? Type the number." % (a, b), max(a, b), "int", {}, ["%d is higher." % max(a, b)])

    def t_estimate():
        q, a = pick(_by(d, [("A door is about 2 ___ tall. Is it m or cm?", "m"),
                            ("A paper clip is about 3 ___ long. Is it cm or m?", "cm"),
                            ("A hot summer day is about ___ °C. Is it 25 or 95?", "25")],
                        [("A door is about 2 ___ tall. Is it m or cm?", "m"),
                         ("A bag of sugar has a mass of about 1 ___. Is it kg or g?", "kg"),
                         ("A cup holds about 200 ___. Is it ml or litres?", "ml"),
                         ("A paper clip is about 3 ___ long. Is it cm or m?", "cm"),
                         ("A hot summer day is about ___ °C. Is it 25 or 95?", "25"),
                         ("A child has a mass of about 25 ___. Is it kg or g?", "kg")],
                        [("A bag of sugar has a mass of about 1 ___. Is it kg or g?", "kg"),
                         ("A cup holds about 200 ___. Is it ml or litres?", "ml"),
                         ("A child has a mass of about 25 ___. Is it kg or g?", "kg"),
                         ("An apple has a mass of about 100 ___. Is it g or kg?", "g"),
                         ("A bucket holds about 10 ___. Is it ml or litres?", "litres"),
                         ("A classroom is about 8 ___ long. Is it m or cm?", "m"),
                         ("A cold winter day is about ___ °C. Is it 2 or 40?", "2")]))
        return _wq(q, a, [_size_why(q)], "type it")

    def t_grams():
        v = random.randint(1, 19) * 5 if d == 2 else random.randint(1, _by(d, 4, 9, 9)) * 10     # hard: 5 g marks
        return {"prompt": "Read the scale. How many grams?", "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": _by(d, 50, 100, 100), "unit": "g"},
                "answer": v, "answer_type": "num", "tolerance": _by(d, 5, 5, 2), "solution": ["The pointer is on %d g." % v]}

    def t_long_ruler():
        cm = random.randint(_by(d, 5, 5, 15), _by(d, 15, 29, 29))
        return {"prompt": "Measure the pencil. How long is it, in cm?", "component": "ruler",
                "spec": {"mode": "length", "value": cm, "max": 30, "unit": "cm"}, "answer": cm, "answer_type": "num", "tolerance": 0.5,
                "solution": ["It ends at %d cm." % cm]}

    def t_colder():
        # a scale in words, numbered in 10s: the marks between the numbers are not 1s
        unit = pick(["kg", "cm", "g"])
        step = _by(d, 2, pick([2, 5]), pick([2, 5]))
        label = 10 * random.randint(0 if d == 0 else 1, _by(d, 3, 8, 8))
        k = random.randint(1, 10 // step - 1)
        v = label + k * step
        name = "The tape measure" if unit == "cm" else "The scale"
        return _tb("%s is numbered in 10s, with a mark every %d %s. The pointer is %s past %d %s. What does it show, in %s?"
                   % (name, step, unit, _pn(k, "mark"), label, unit, unit), v, "int", {"unit": unit},
                   ["Each mark is %d %s, so %s %d %s." % (step, unit, "1 mark is" if k == 1 else "%d marks are" % k, k * step, unit),
                    "%d + %d = %d %s." % (label, k * step, v, unit)])

    def t_litres():
        # a big jug marked in litres (hard: half-litre marks are not shown, so the level is between lines in 2s)
        top, step = _by(d, (5, 1), (10, 1), (20, 2))
        v = random.randint(1, top // step - 1) * step
        return {"prompt": "The jug is marked in litres. How many litres of water are in it?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": top, "unit": "litres"}, "answer": v, "answer_type": "num",
                "tolerance": _by(d, 0.5, 0.5, 1), "solution": ["The water is level with the %d litre line." % v]}

    def t_jug_more():
        top = _by(d, 50, 100, 100)                     # easy: a 50 ml jug; hard: 5 ml steps
        v = random.randint(1, 19) * 5 if d == 2 else random.randint(1, top // 10 - 1) * 10
        return {"prompt": "How much more water is needed to make %d ml?" % top, "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": top, "unit": "ml"}, "answer": top - v, "answer_type": "num",
                "tolerance": 0, "solution": ["The jug shows %d ml; %d − %d = %d." % (v, top, v, top - v)]}

    return _pick_t([t_unit, t_temp, t_thermo, t_estimate, t_colder], [t_ruler, t_scale, t_jug, t_grams, t_long_ruler, t_jug_more, t_litres])


@skill("Y2.4.b", "Compare and order lengths, mass and capacity", S4)
def _(d=1):
    d = _d(d)

    def t_symbol():
        unit = pick(["cm", "kg", "ml", "m", "g", "litres"])
        a, b = _vals(d, 2, _by(d, 30, 99, 99), 2)
        return _wq("Write < or > :  %d %s ___ %d %s" % (a, unit, b, unit), "<" if a < b else ">", ["%d %s is %s than %d %s." % (a, unit, "less" if a < b else "more", b, unit)], "< or >")

    def t_longest():
        names = ["red", "blue", "green"]
        v = _vals(d, 5, _by(d, 30, 60, 99), 3)
        return _wq("Ribbons: red %d cm, blue %d cm, green %d cm. Which is the longest?" % tuple(v), names[v.index(max(v))],
                   ["%d cm is the longest." % max(v)], "colour")

    def t_order():
        v = _vals(d, 1, _by(d, 20, 40, 60), 3)
        return _tb("Put these masses in order, lightest first. Which is in the middle?  %s" % ", ".join("%d kg" % x for x in v),
                   sorted(v)[1], "int", {"unit": "kg"}, ["Order: %s." % ", ".join("%d kg" % x for x in sorted(v))])

    def t_difference():
        a, b = [10 * x for x in random.sample(range(1, 10), 2)] if d == 0 else random.sample(range(_by(d, 10, 10, 21), 90), 2)
        return _tb("A jug holds %d ml. A cup holds %d ml. How much more does the bigger one hold, in ml?" % (max(a, b), min(a, b)),
                   abs(a - b), "int", {"unit": "ml"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_eq():
        unit = pick(["cm", "kg", "ml"])
        a = random.randint(10, _by(d, 30, 60, 90))
        b = a + pick(_by(d, [-10, 0, 10], [-5, 0, 5], [-1, 0, 1]))
        sym = "<" if a < b else (">" if a > b else "=")
        return _wq("Write <, > or = :  %d %s ___ %d %s" % (a, unit, b, unit), sym, ["%d %s is %s %d %s." % (a, unit, {"<": "less than", ">": "more than", "=": "the same as"}[sym], b, unit)], "<, > or =")

    def t_heaviest():
        names = ["red", "blue", "green"]
        v = _vals(d, 2, _by(d, 20, 30, 50), 3)
        k = pick(["heaviest", "lightest"])
        ans = names[v.index(max(v))] if k == "heaviest" else names[v.index(min(v))]
        return _dt("The table shows the mass of three parcels. Which parcel is the %s?" % k, ["Parcel", "Mass (kg)"],
                   [[names[i], v[i]] for i in range(3)], ans, ["The %s parcel is %d kg, the %s." % (ans, max(v) if k == "heaviest" else min(v), "most" if k == "heaviest" else "least")], atype="str", placeholder="colour")

    def t_order_cap():
        v = _vals(d, 1, _by(d, 10, 10, 20), 3)
        vals = [x * _by(d, 10, 10, 5) for x in v]       # within 100 ml; hard: 5 ml steps
        return _tb("Put these in order, most first. Which comes first?  %s" % ", ".join("%d ml" % x for x in vals), max(vals), "int",
                   {"unit": "ml"}, ["Order: %s." % ", ".join("%d ml" % x for x in sorted(vals, reverse=True))])

    def t_taller():
        a, b = [5 * x for x in random.sample(range(20, 27), 2)] if d == 0 else random.sample(range(90, 140), 2)
        kids = random.sample(KIDS, 2)
        return _tb("%s is %d cm tall. %s is %d cm tall. How much taller is the taller child, in cm?" % (kids[0], a, kids[1], b), abs(a - b),
                   "int", {"unit": "cm"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_bars():
        cats = ["Jug", "Cup", "Bottle", "Bowl"]
        vals = random.sample(range(1, 10), 4)
        return _bar("The chart shows how many glasses each one fills. Which holds the most?", cats, vals, cats[vals.index(max(vals))],
                    ["%s has the tallest bar." % cats[vals.index(max(vals))]], atype="str")

    plain = [t_symbol, t_longest, t_order, t_difference, t_eq, t_order_cap, t_taller]
    if d == 2:     # stretch: more ordering and finding differences
        plain += [t_order, t_difference, t_taller, t_order_cap]
    return _pick_t(plain, [t_heaviest, t_bars])


@skill("Y2.4.c", "Money: £ and p, making amounts and giving change", S4)
def _(d=1):
    d = _d(d)
    coins = _by(d, [1, 2, 5, 10], [1, 2, 5, 10, 20, 50], [1, 2, 5, 10, 20, 50])

    def _m(p):
        return "£1" if p == 100 else "%dp" % p

    def t_total():
        cs = random.sample(coins, _by(d, 2, 3, 4))
        return _tb("What is the total of %s, in pence?" % " + ".join("%dp" % c for c in cs), sum(cs), "int", {"unit": "p"},
                   ["%s = %dp." % (" + ".join(map(str, cs)), sum(cs))])

    def t_pounds():                                     # make £1 = 100p; stays within 100
        a = random.randint(5, 95) if d == 2 else _by(d, 10, 5, None) * random.randint(1, _by(d, 9, 19, None))   # hard: any pence
        return _tb("£1 = 100p. %dp + ___p = £1. How many pence are missing?" % a, 100 - a, "int", {"unit": "p"},
                   ["100 − %d = %d, so %dp." % (a, 100 - a, 100 - a)])

    def t_make():
        target = pick(_by(d, [15, 25, 30, 60, 70], [15, 25, 30, 35, 60, 70, 80], [45, 75, 80, 90, 95, 38, 67]))
        return _tb("What is the fewest coins you can use to make %dp?" % target,
                   _fewest(target), "int", {}, ["Use the biggest coins first."])

    def t_change():
        if d == 2 and random.random() < 0.5:            # hard: two things, then the change
            x, y = random.randint(10, 45), random.randint(10, 45)
            return _tb("A comic costs %dp and a sticker costs %dp. You pay with £1. How much change, in pence?" % (x, y),
                       100 - x - y, "int", {"unit": "p"}, ["%d + %d = %d." % (x, y, x + y), "100 − %d = %d." % (x + y, 100 - x - y)])
        cost = random.randint(1, 9) * 5 if d == 0 else random.randint(5, 95)     # easy: 5p steps from 50p
        pay = 50 if d == 0 else (100 if cost >= 50 else pick([50, 100]))
        return _tb("A comic costs %dp. You pay with %s. How much change, in pence?" % (cost, "£1" if pay == 100 else "50p"),
                   pay - cost, "int", {"unit": "p"}, ["%d − %d = %d." % (pay, cost, pay - cost)])

    def t_two_ways():
        cs, one = pick(_by(d, [([10, 10], 20), ([5, 5], 10), ([2, 2, 1], 5), ([10, 5], 20), ([10, 10, 10], 20)],
                           [([20, 20, 10], 50)],
                           [([20, 20, 5, 5], 50), ([20, 20, 5, 2], 50), ([50, 20, 20, 10], 100), ([50, 20, 20, 5], 100),
                            ([20, 10, 10, 5, 5], 50)]))
        same = sum(cs) == one
        return _wq("Do %s and %s make the same amount? (yes or no)" % (" + ".join("%dp" % c for c in cs), _m(one)), "yes" if same else "no",
                   ["Both make %s." % _m(one) if same else "%s = %dp, not %s." % (" + ".join("%dp" % c for c in cs), sum(cs), _m(one))],
                   "yes / no")

    def t_shop():
        if d == 2:                                      # hard: three things
            x = [random.randint(10, 30) for _ in range(3)]
            return _tb("A pencil costs %dp, a rubber costs %dp and a ruler costs %dp. How much for all three, in pence?" % tuple(x),
                       sum(x), "int", {"unit": "p"}, ["%d + %d + %d = %d." % (x[0], x[1], x[2], sum(x))])
        if d == 0:                                      # easy: the ones do not cross ten
            a = random.randint(1, 3) * 10 + random.randint(0, 5)
            b = random.randint(1, 3) * 10 + random.randint(0, 9 - a % 10)
        else:
            a, b = random.randint(10, 45), random.randint(10, 45)
        return _tb("A pencil costs %dp and a rubber costs %dp. How much for both, in pence?" % (a, b), a + b, "int", {"unit": "p"},
                   ["%d + %d = %d." % (a, b, a + b)])

    def t_how_many_coins():
        c, tot = pick(_by(d, [(2, 10), (5, 20), (10, 50), (10, 30), (5, 10)],
                          [(5, 20), (5, 30), (10, 50), (10, 70), (2, 10), (2, 16), (20, 100), (5, 50), (10, 100)],
                          [(20, 100), (5, 50), (10, 100), (2, 18), (5, 45), (2, 20), (20, 80), (5, 35)]))
        return _tb("How many %dp coins make %s?" % (c, _m(tot)), tot // c, "int", {}, [_groups_why(tot, c, "coin")])

    def t_missing_coin():
        c = pick(coins)
        if d == 2:                                      # hard: two coins known
            k = random.sample([5, 10, 20, 50], 2)
            while sum(k) + c > 100:
                k = random.sample([5, 10, 20, 50], 2)
            return _tb("%dp + %dp + ___p = %dp. Which coin is missing? Type its value in pence." % (k[0], k[1], sum(k) + c), c, "int",
                       {"unit": "p"}, ["%d + %d = %d." % (k[0], k[1], sum(k)), "%d − %d = %d." % (sum(k) + c, sum(k), c)])
        known = pick([x for x in _by(d, (10, 20), (5, 10, 20, 50), None) if x + c <= 100])
        return _tb("%dp + ___p = %dp. Which coin is missing? Type its value in pence." % (known, known + c), c, "int", {"unit": "p"},
                   ["%d − %d = %d." % (known + c, known, c)])

    def t_same():
        a = random.sample(_by(d, [1, 2, 5, 10], [1, 2, 5, 10, 20], [1, 2, 5, 10, 20, 50]), _by(d, 2, 3, 4))
        b = sum(a) + pick([0, 0, 1, 5])
        return _wq("Mia has %s. Ben has %dp. Do they have the same amount? (yes or no)" % (" + ".join("%dp" % x for x in a), b),
                   "yes" if sum(a) == b else "no", ["%s = %dp%s." % (" + ".join(map(str, a)), sum(a), "" if sum(a) == b else ", not %dp" % b)], "yes / no")

    def t_whole_pounds():                               # combine coins, then how far short of £1 (all within 100p)
        cs = random.sample(_by(d, [10, 20, 50], [5, 10, 20, 50], [1, 2, 5, 10, 20, 50]), _by(d, 2, 2, 3))
        while sum(cs) >= 100:
            cs = random.sample(_by(d, [10, 20, 50], [5, 10, 20, 50], [1, 2, 5, 10, 20, 50]), _by(d, 2, 2, 3))
        kid = _kid()
        return _tb("%s has %s. How many more pence does %s need to make £1?" % (kid, " + ".join("%dp" % c for c in cs), kid),
                   100 - sum(cs), "int", {"unit": "p"},
                   ["%s = %dp; 100 − %d = %dp." % (" + ".join(map(str, cs)), sum(cs), sum(cs), 100 - sum(cs))])

    def t_notes():
        a, b = random.sample([5, 10, 20], 2)
        n = random.randint(_by(d, 1, 1, 2), _by(d, 1, 3, 4))     # hard: more notes of one kind
        return _tb("%s has %s and a £%d note. How many pounds is that?" % (_kid(), "a £%d note" % a if n == 1 else "%s £%d notes" % (_cnt(n), a), b),
                   n * a + b, "int",
                   {"unit": "£"}, ["%d × £%d + £%d = £%d." % (n, a, b, n * a + b)])

    def t_change_pounds():
        if d == 2:                                      # hard: change from £20 or £50
            pay = pick([20, 50])
            cost = random.randint(3, pay - 1)
        else:
            cost = random.randint(2, 9)
            pay = 10 if d == 0 else (pick([10, 20]) if cost >= 5 else pick([5, 10]))
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
    if d == 0:     # quarter past and quarter to (o'clock and half past are Year 1), now and then half past
        m = pick([15, 45, 15, 45, 30])
    elif d == 2:   # five-minute times that are not on a quarter
        m = 5 * pick([1, 2, 4, 5, 7, 8, 10, 11])
    else:
        m = 5 * random.randint(0, 11)

    def t_set():
        return {"prompt": "Set the clock to %d:%02d." % (h, m), "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:%02d" % (h, m), "answer_type": "time", "solution": ["The long hand points to %d." % (m // 5 or 12)]}

    def t_quarter():
        kind = pick(["quarter past", "quarter to"])           # half past is Year 1
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
        mm = 5 * pick([7, 8, 10, 11]) if d == 2 else m       # hard: the far side of the clock, 35 to 55 minutes
        return _tb("The long hand points to %d. How many minutes past the hour is that?" % (mm // 5 or 12), mm, "int", {},
                   ["Each number is 5 minutes: %d × 5 = %d." % (mm // 5, mm)] if mm else
                   ["When the long hand points to 12 it is o'clock: 0 minutes past."])

    def t_type_time():
        mm = pick([5, 10, 20, 25])
        hh = random.randint(1, 12)
        if d == 2 and random.random() < 0.5:     # stretch: minutes *to* the hour
            ah, am = (hh - 2) % 12 + 1, 60 - mm
            return _tb("Write %d minutes to %d as a time like 4:20." % (mm, hh), "%d:%02d" % (ah, am), "time",
                       {"text": True, "placeholder": "e.g. 4:20"}, ["%d minutes to %d is %d:%02d." % (mm, hh, ah, am)])
        return _tb("Write %d minutes past %d as a time like 4:20." % (mm, hh), "%d:%02d" % (hh, mm), "time",
                   {"text": True, "placeholder": "e.g. 4:20"}, ["%d minutes past %d is %d:%02d." % (mm, hh, hh, mm)])

    def t_quarter_hand():
        kind, num = pick([("quarter past %d", 3), ("quarter to %d", 9), ("25 minutes past %d", 5), ("20 minutes to %d", 8)])
        kind = kind % random.randint(1, 12)
        return _tb("At %s, which number does the long hand point to?" % kind, num, "int", {}, ["%s: the long hand points to %d." % (kind[0].upper() + kind[1:], num)])

    def t_minutes_to():
        n = pick([7, 8]) if d == 2 else pick([9, 10, 11])      # hard: further from the hour
        return _tb("The long hand points to %d. How many minutes is it until the next o'clock?" % n, 60 - 5 * n, "int", {},
                   ["%d × 5 = %d minutes past; 60 − %d = %d." % (n, 5 * n, 5 * n, 60 - 5 * n)])

    def t_five_later():
        if d == 2:     # stretch: the new time is in the next hour
            k = pick([10, 15, 20, 25])
            mm = 5 * random.randint((60 - k) // 5, 11)
            nh, nm = h % 12 + 1, mm + k - 60
            return {"prompt": "It is %d:%02d. Set the clock to %d minutes later." % (h, mm, k), "component": "clock", "spec": {"mode": "set"},
                    "answer": "%d:%02d" % (nh, nm), "answer_type": "time",
                    "solution": ["%d:%02d + %d minutes goes past the hour: %d:%02d." % (h, mm, k, nh, nm)]}
        k = pick([5, 10, 15])
        mm = 5 * random.randint(0, (55 - k) // 5)
        return {"prompt": "It is %d:%02d. Set the clock to %d minutes later." % (h, mm, k), "component": "clock", "spec": {"mode": "set"},
                "answer": "%d:%02d" % (h, mm + k), "answer_type": "time", "solution": ["%d:%02d + %d minutes = %d:%02d." % (h, mm, k, h, mm + k)]}

    def t_digital():
        mm = pick([15, 30, 45]) if d == 0 else 5 * random.randint(1, 11)
        return {"prompt": "A digital clock shows %d:%02d. Show the same time on this clock." % (h, mm), "component": "clock",
                "spec": {"mode": "set"}, "answer": "%d:%02d" % (h, mm), "answer_type": "time",
                "solution": ["The long hand points to %d." % (mm // 5)]}

    def t_words_out():
        mm = pick([15, 30, 45])
        hh = random.randint(1, 11)
        word, ans = {15: ("quarter past", hh), 30: ("half past", hh), 45: ("quarter to", hh + 1)}[mm]
        return _tb("A clock shows %d:%02d. Is it quarter past, half past or quarter to which hour? Type the hour." % (hh, mm), ans, "int", {},
                   ["%d:%02d is %s %d." % (hh, mm, word, ans)])

    if d == 0:     # quarter and half hours only
        return _pick_t([t_long_hand, t_quarter_hand, t_words_out], [t_set, t_quarter, t_digital])
    if d == 2:     # stretch: minutes to the hour, crossing the hour
        return _pick_t([t_long_hand, t_type_time, t_type_time, t_minutes_to, t_minutes_to], [t_set, t_words, t_five_later, t_digital])
    return _pick_t([t_long_hand, t_type_time, t_quarter_hand, t_minutes_to, t_words_out], [t_set, t_quarter, t_words, t_five_later, t_digital])


@skill("Y2.5.b", "Minutes, hours and comparing times", S5)
def _(d=1):
    d = _d(d)

    def t_facts():
        q, a = pick([("How many minutes are in an hour?", 60), ("How many hours are in a day?", 24),
                     ("How many minutes are in half an hour?", 30), ("How many minutes are in a quarter of an hour?", 15)])
        return _tb(q, a, "int", {}, [{60: "The long hand goes all the way round the clock in 60 minutes.",
                                      24: "From midnight to midnight is 24 hours: 12 in the morning and 12 after midday.",
                                      30: "Half an hour is the long hand going half way round: 30 minutes.",
                                      15: "A quarter of an hour is the long hand going a quarter of the way round: 15 minutes."}[a]])

    def t_later():
        h = random.randint(_by(d, 1, 1, 9), _by(d, 8, 10, 12))
        k = random.randint(_by(d, 1, 1, 3), _by(d, 2, 3, 6))     # stretch: goes past 12 o'clock
        return _tb("It is %d o'clock. What time will it be in %d hour%s? Type the hour." % (h, k, "" if k == 1 else "s"),
                   (h + k - 1) % 12 + 1, "int", {}, ["Count on %s: %s." % (_pn(k, "hour"), ", ".join(str((h + i - 1) % 12 + 1) for i in range(1, k + 1)))])

    def t_compare():
        a, b = random.sample([10, 15, 20, 30, 45, 50], 2)
        kids = random.sample(KIDS, 2)
        if d == 2:     # stretch: one time given in words (half an hour / a quarter of an hour)
            a, wa = pick([(30, "half an hour"), (15, "a quarter of an hour")])
            b = a + pick([-10, -5, 5, 10])
            return _wq("%s read for %s. %s read for %d minutes. Who read for longer?" % (kids[0], wa, kids[1], b),
                       kids[0] if a > b else kids[1], ["%s is %d minutes; %d minutes is longer." % (wa.capitalize(), a, max(a, b))], "name")
        return _wq("%s read for %d minutes. %s read for %d minutes. Who read for longer?" % (kids[0], a, kids[1], b),
                   kids[0] if a > b else kids[1], ["%d minutes is longer." % max(a, b)], "name")

    def t_duration():
        start = random.randint(1, 10)
        k = random.randint(1, 2)
        if d == 2:     # stretch: from o'clock to quarter past, half past or quarter to, in minutes
            mins, word = pick([(15, "quarter past %d" % start), (30, "half past %d" % start), (45, "quarter to %d" % (start + 1))])
            return _tb("A TV show starts at %d o'clock and ends at %s. How many minutes long is it?" % (start, word), mins, "int", {},
                       ["From %d o'clock to %s is %d minutes." % (start, word, mins)])
        return _tb("A film starts at %d o'clock and ends at %d o'clock. How many hours long is it?" % (start, start + k), k, "int", {},
                   ["%d − %d = %d." % (start + k, start, k)])

    def t_half_hour():
        h = random.randint(1, 11)
        if d == 2:     # stretch: start from quarter past
            return _tb("It is quarter past %d. How many minutes until half past %d?" % (h, h), 15, "int", {},
                       ["Quarter past is 15 minutes past; half past is 30 minutes past: 30 − 15 = 15."])
        return _tb("It is %d o'clock. How many minutes until half past %d?" % (h, h), 30, "int", {}, ["Half an hour is 30 minutes."])

    if d == 0:     # minutes in an hour, hours in a day, an hour later
        return _pick_t([t_facts, t_facts, t_later, t_compare, t_duration])
    if d == 2:     # stretch: no bare facts
        return _pick_t([t_later, t_compare, t_duration, t_half_hour])
    return _pick_t([t_facts, t_later, t_compare, t_duration, t_half_hour])


# ================================================================== 2.6 ======
@skill("Y2.6.a", "Properties of 2-D shapes", S6)
def _(d=1):
    d = _d(d)
    SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}
    # easy: the everyday shapes; stretch: mostly the many-sided ones
    SHAPES = _by(d, ["triangle", "square", "rectangle"], ["triangle", "square", "rectangle", "pentagon", "hexagon", "octagon"],
                 ["pentagon", "hexagon", "octagon", "pentagon", "hexagon", "octagon", "rectangle"])

    def t_sides():
        name = pick(SHAPES)
        return {"prompt": "How many sides does this shape have?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": {"triangle": 3, "square": 4, "rectangle": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}[name],
                "answer_type": "int", "solution": ["Count the sides."]}

    def t_vertices():
        name = pick(_by(d, ["triangle", "square", "rectangle"], ["triangle", "square", "pentagon", "hexagon"],
                        ["pentagon", "hexagon", "octagon"]))
        return {"prompt": "How many corners (vertices) does this shape have?", "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "vertices"},
                "answer": SIDES[name], "answer_type": "int",
                "solution": ["Count the corners."]}

    def t_name():
        n, name = pick([(3, "triangle"), (5, "pentagon"), (6, "hexagon")] + ([] if d == 0 else [(8, "octagon")]))
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
        name = pick(SHAPES)
        return {"prompt": "What is the name of this shape?", "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str", "solution": ["It is %s." % _a(name)]}

    def t_total_sides():
        if d == 2:     # stretch: three shapes
            sh = random.sample([("triangle", 3), ("square", 4), ("pentagon", 5), ("hexagon", 6), ("octagon", 8)], 3)
            return _tb("How many sides do %s, %s and %s have altogether?" % tuple(_a(x[0]) for x in sh), sum(x[1] for x in sh), "int", {},
                       ["%s = %d." % (" + ".join(str(x[1]) for x in sh), sum(x[1] for x in sh))])
        a, b = random.sample([("triangle", 3), ("square", 4), ("pentagon", 5), ("hexagon", 6)], 2)
        return _tb("How many sides do a %s and a %s have altogether?" % (a[0], b[0]), a[1] + b[1], "int", {},
                   ["%d + %d = %d." % (a[1], b[1], a[1] + b[1])])

    def t_rect_vs_square():
        return _wq("A shape has 4 straight sides. Two are long and two are short. Is it a square or a rectangle?", "rectangle",
                   ["A square has 4 sides the same length."], "square / rectangle")

    def t_same_sides():
        n = random.randint(_by(d, 3, 3, 5), _by(d, 5, 8, 10))
        return _tb("A shape has %d corners. How many sides does it have?" % n, n, "int", {},
                   ["A flat shape with straight sides has as many sides as corners."])

    plain = [t_name, t_symmetry, t_count_four, t_curved, t_total_sides, t_rect_vs_square, t_same_sides]
    if d == 0:     # count and name; no sorting a list
        plain = [t_name, t_symmetry, t_curved, t_rect_vs_square]
    elif d == 2:   # stretch: counting across several shapes
        plain += [t_count_four, t_total_sides, t_same_sides]
    return _pick_t(plain, [t_sides, t_vertices, t_name_pic])


@skill("Y2.6.b", "Properties of 3-D shapes", S6)
def _(d=1):
    d = _d(d)
    SOL = {"cube": (6, 12, 8), "cuboid": (6, 12, 8), "square-based pyramid": (5, 8, 5), "triangular prism": (5, 9, 6)}

    def t_count():
        # easy: faces and corners of a cube or cuboid; stretch: mostly the pyramid and prism, often edges
        name = pick(_by(d, ["cube", "cuboid"], list(SOL), ["square-based pyramid", "triangular prism", "cuboid"]))
        what, i = pick(_by(d, [("faces", 0), ("vertices", 2)], [("faces", 0), ("edges", 1), ("vertices", 2)],
                           [("faces", 0), ("edges", 1), ("edges", 1), ("vertices", 2)]))
        return {"prompt": "How many %s does this shape have?" % what, "component": "shape",
                "spec": {"kind": "3d", "name": name, "ask": what}, "answer": SOL[name][i], "answer_type": "int",
                "solution": ["A %s has %d %s." % (name, SOL[name][i], what)]}

    def t_face_shape():
        qs = [("What 2-D shape is the flat face of a cylinder?", "circle"),
              ("What 2-D shape are the faces of a cube?", "square"),
              ("What 2-D shape are the sloping faces of a pyramid?", "triangle"),
              ("What 2-D shape is the flat face of a cone?", "circle")]
        if d == 2:     # stretch: faces that are easy to mix up
            qs = [("What 2-D shape are the two end faces of a triangular prism?", "triangle"),
                  ("What 2-D shape is the bottom face of a square-based pyramid?", "square"),
                  ("What 2-D shape are the long side faces of a triangular prism?", "rectangle"),
                  ("What 2-D shape are the sloping faces of a pyramid?", "triangle")]
        q, a = pick(qs)
        return _wq(q, a, [FACE_WHY[q]], "shape name")

    def t_roll():
        q, a = pick([("Can a sphere roll? (yes or no)", "yes"), ("Can a cube roll? (yes or no)", "no"),
                     ("Does a sphere have any flat faces? (yes or no)", "no")])
        return _wq(q, a, [{"Can a sphere roll? (yes or no)": "A sphere is curved all over, so it rolls.",
                           "Can a cube roll? (yes or no)": "A cube has only flat faces, so it slides but does not roll.",
                           "Does a sphere have any flat faces? (yes or no)": "A sphere is curved all over, so it has no flat faces."}[q]], "yes / no")

    def t_sort():
        shapes = random.sample(["cube", "sphere", "cylinder", "cone", "cuboid", "pyramid"], _by(d, 3, 4, 5))
        curved = sum(1 for s in shapes if s in ("sphere", "cylinder", "cone"))
        return _tb("How many of these have a curved surface?  %s" % ", ".join(shapes), curved, "int", {},
                   ["Sphere, cylinder and cone have curved surfaces."])

    def t_compare():
        a, b = random.sample(list(SOL), 2)
        what, i = pick([("faces", 0), ("edges", 1), ("vertices", 2)])
        if SOL[a][i] == SOL[b][i]:
            return _wq("Do a %s and a %s have the same number of %s? (yes or no)" % (a, b, what), "yes",
                       ["Both have %d %s." % (SOL[a][i], what)], "yes / no")
        if SOL[a][i] < SOL[b][i]:
            a, b = b, a
        return _tb("How many more %s does a %s have than a %s?" % (what, a, b), SOL[a][i] - SOL[b][i], "int", {},
                   ["%d − %d = %d." % (SOL[a][i], SOL[b][i], SOL[a][i] - SOL[b][i])])

    if d == 2:     # stretch: compare two solids
        return _pick_t([t_face_shape, t_sort, t_compare, t_compare], [t_count])
    return _pick_t([t_face_shape, t_roll, t_sort], [t_count])


@skill("Y2.6.c", "Patterns, turns and direction", S6)
def _(d=1):
    d = _d(d)
    DIRS = ["north", "east", "south", "west"]

    def t_pattern():
        unit = random.sample(["circle", "square", "triangle", "star"], pick(_by(d, [2], [2, 3], [3, 3, 4])))
        k = random.randint(len(unit) * 2 + 1, _by(d, 8, 12, 20))     # stretch: further along the pattern
        seq = [unit[i % len(unit)] for i in range(len(unit) * 2)]
        return _wq("The pattern goes: %s, ... What is shape number %d?" % (", ".join(seq), k), unit[(k - 1) % len(unit)],
                   ["The pattern repeats every %d shapes." % len(unit)], "shape")

    def t_turn():
        s = random.randrange(4)
        k = random.randint(1, _by(d, 2, 3, 3))
        cw = random.random() < 0.5
        if d == 2 and random.random() < 0.5:     # stretch: two turns, one each way
            k2 = random.randint(1, 2)
            name = {1: "a quarter", 2: "a half", 3: "a three-quarter"}
            return _wq("You face %s. You make %s turn clockwise, then %s turn anticlockwise. Which way do you face now?"
                       % (DIRS[s], name[k], name[k2]), DIRS[(s + k - k2) % 4],
                       ["Do one turn, then the other. A quarter turn is one right angle."], "direction")
        return _wq("You face %s and make %s turn %s. Which way do you face now?"
                   % (DIRS[s], {1: "a quarter", 2: "a half", 3: "a three-quarter"}[k], "clockwise" if cw else "anticlockwise"),
                   DIRS[(s + (k if cw else -k)) % 4], ["A quarter turn is one right angle."], "direction")

    def t_right_angles():
        k, name = pick(_by(d, [(1, "a quarter turn"), (2, "a half turn")],
                           [(1, "a quarter turn"), (2, "a half turn"), (3, "a three-quarter turn"), (4, "a whole turn")],
                           [(3, "a three-quarter turn"), (4, "a whole turn"), (2, "a half turn")]))
        return _tb("How many right angles are in %s?" % name, k, "int", {}, ["%s = %d right angle%s." % (name.capitalize(), k, "" if k == 1 else "s")])

    def t_turn_pic():
        deg, name = pick(_by(d, [(90, "quarter"), (180, "half")], [(90, "quarter"), (180, "half"), (270, "three-quarter")],
                             [(90, "quarter"), (270, "three-quarter"), (270, "three-quarter")]))
        return {"prompt": "The arrow shows an anticlockwise turn. Is it a quarter, half or three-quarter turn?", "component": "angle",
                "spec": {"mode": "turn", "degrees": deg}, "answer": name, "answer_type": "str", "solution": ["%s turn." % name.capitalize()]}

    def t_grid():
        x, y = random.randint(1, 4), random.randint(1, 4)
        r, u = random.randint(1, 4), random.randint(1, 4)
        if d == 0:     # one direction only
            r, u = pick([(r, 0), (0, u)])
            move = "%s %s" % (_pn(r or u, "square"), "right" if r else "up")
            return {"prompt": "Start at the dot. Move %s. Mark where you finish." % move,
                    "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                    "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord", "solution": ["%s." % move.capitalize()]}
        elif d == 2:   # stretch: left or down as well
            x, y = random.randint(3, 5), random.randint(3, 5)
            r, u = pick([-3, -2, -1, 1, 2, 3]), pick([-3, -2, -1, 1, 2, 3])
            return {"prompt": "Start at the dot. Move %s %s and %s %s. Mark where you finish."
                              % (_pn(abs(r), "square"), "right" if r > 0 else "left", _pn(abs(u), "square"), "up" if u > 0 else "down"),
                    "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                    "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord",
                    "solution": ["%d %s, %d %s." % (abs(r), "right" if r > 0 else "left", abs(u), "up" if u > 0 else "down")]}
        return {"prompt": "Start at the dot. Move %d square%s right and %d square%s up. Mark where you finish."
                          % (r, "" if r == 1 else "s", u, "" if u == 1 else "s"),
                "component": "coordinate_grid", "spec": {"mode": "plot", "size": 8, "points": [[x, y, "Start"]]},
                "answer": "(%d,%d)" % (x + r, y + u), "answer_type": "coord", "solution": ["%d right, %d up." % (r, u)]}

    return _pick_t([t_pattern, t_turn, t_right_angles], [t_turn_pic, t_grid])


# ================================================================== 2.7 ======
@skill("Y2.7.a", "Pictograms and tally charts", S7)
def _(d=1):
    d = _d(d)
    m = _by(d, 3, 4, 5)                                # easy: three rows; hard: five
    cats = random.sample(["Apples", "Bananas", "Grapes", "Pears", "Oranges"], m)

    def t_pictogram():
        key = pick(_by(d, [1], [1, 2, 5], [2, 5, 10]))
        vals = [key * random.randint(1, _by(d, 5, 6, 8)) for _ in cats]
        k = random.randrange(m)
        return {"prompt": "Each symbol stands for %d. How many %s?" % (key, cats[k].lower()), "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"}, "answer": vals[k], "answer_type": "int",
                "solution": ["%s × %d = %d." % (_pn(vals[k] // key, "symbol"), key, vals[k])]}

    def t_tally():
        vals = [random.randint(_by(d, 2, 2, 6), _by(d, 9, 14, 24)) for _ in cats]
        rows = [[c, _tally(v), v] for c, v in zip(cats, vals)]
        k = random.randrange(m)
        return _dt("Read the tally chart. What number goes in the empty box?", ["Fruit", "Tally", "Total"], rows, vals[k],
                   ["Count in 5s for each bundle, then the extra ones: %d." % vals[k]], missing=[k, 2])

    def t_most():
        key = _by(d, 1, 1, 2)                           # hard: a key of 2 and half symbols
        vals = random.sample(range(1, _by(d, 7, 10, 16)), m)
        return {"prompt": "Which fruit was chosen most?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"}, "answer": cats[vals.index(max(vals))],
                "answer_type": "str", "solution": ["%s has the most symbols." % cats[vals.index(max(vals))]]}

    def t_read_tally():
        v = random.randint(_by(d, 3, 3, 12), _by(d, 10, 19, 30))
        return _tb("How many does this tally show?  %s" % _tally(v), v, "int", {}, ["Each bundle is 5: %d." % v])

    def t_total():
        key = _by(d, 1, 1, pick([2, 5]))               # hard: count in 2s or 5s across five rows
        vals = [key * random.randint(1, _by(d, 5, 8, 4)) for _ in cats]
        return {"prompt": "Each symbol stands for %d. How many fruits were chosen altogether?" % key, "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"}, "answer": sum(vals), "answer_type": "int",
                "solution": ["%s = %d." % (" + ".join(map(str, vals)), sum(vals))]}

    def t_diff():
        vals = random.sample(range(1, _by(d, 7, 10, 10)), m)
        i, j = random.sample(range(m), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        key = pick(_by(d, [1], [1, 2], [2, 5]))
        vv = [v * key for v in vals]
        return {"prompt": "Each symbol stands for %d. How many more chose %s than %s?" % (key, cats[i].lower(), cats[j].lower()),
                "component": "pictogram", "spec": {"categories": cats, "values": vv, "key": key, "symbol": "circle"},
                "answer": vv[i] - vv[j], "answer_type": "int", "solution": ["%d − %d = %d." % (vv[i], vv[j], vv[i] - vv[j])]}

    def t_half_symbol():
        key = pick([2, 10]) if d == 2 else 2           # hard: a key of 10, half a symbol is 5
        vals = [key * random.randint(1, 5) - (key // 2) * pick(_by(d, [0], [0, 1], [0, 1])) for _ in cats]   # easy: whole symbols only
        k = random.randrange(m)
        return {"prompt": "Each whole symbol stands for %d. Half a symbol stands for %d. How many %s?" % (key, key // 2, cats[k].lower()),
                "component": "pictogram", "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"},
                "answer": vals[k], "answer_type": "int", "solution": [_half_symbols(vals[k], key)]}

    def t_least():
        key = _by(d, 1, 1, 2)
        vals = random.sample(range(1, _by(d, 7, 10, 16)), m)
        return {"prompt": "Which fruit was chosen the least?", "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": key, "symbol": "circle"}, "answer": cats[vals.index(min(vals))],
                "answer_type": "str", "solution": ["%s has the fewest symbols." % cats[vals.index(min(vals))]]}

    def t_tally_more():
        vals = random.sample(range(_by(d, 2, 2, 5), _by(d, 11, 15, 26)), m)
        i, j = random.sample(range(m), 2)
        rows = [[c, _tally(v)] for c, v in zip(cats, vals)]
        return _dt("The tally chart shows favourite fruit. How many more chose %s than %s?" % (cats[i].lower(), cats[j].lower())
                   if vals[i] > vals[j] else "The tally chart shows favourite fruit. How many fewer chose %s than %s?" % (cats[i].lower(), cats[j].lower()),
                   ["Fruit", "Tally"], rows, abs(vals[i] - vals[j]),
                   ["%s: %d, %s: %d; the difference is %d." % (cats[i], vals[i], cats[j], vals[j], abs(vals[i] - vals[j]))])

    def t_order():
        vals = random.sample(range(1, _by(d, 7, 10, 10)), m)
        k = random.randint(1, m)
        return {"prompt": "Put the fruits in order, most popular first. Which fruit is number %d?" % k, "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": [c for _, c in sorted(zip(vals, cats), reverse=True)][k - 1], "answer_type": "str",
                "solution": ["Order: %s." % ", ".join(c for _, c in sorted(zip(vals, cats), reverse=True))]}

    return _pick_t([t_read_tally], [t_pictogram, t_tally, t_most, t_total, t_diff, t_half_symbol, t_least, t_tally_more, t_order])


_GATE = "|\u0336" * 4            # a bundle of five: four bars crossed by the fifth


def _tally(v):
    return " ".join([_GATE] * (v // 5) + (["|" * (v % 5)] if v % 5 else []))


@skill("Y2.7.b", "Block diagrams and tables: totals and comparisons", S7)
def _(d=1):
    d = _d(d)
    cats = random.sample(["Red", "Blue", "Green", "Yellow"], 4)
    vals = [random.randint(_by(d, 1, 1, 5), _by(d, 8, 12, 20)) for _ in cats]     # stretch: bigger totals and differences

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

    def t_together():
        i, j, k = random.sample(range(4), 3)
        if vals[i] + vals[j] <= vals[k]:
            return t_more()
        return _bar("How many more chose %s and %s together than %s?" % (cats[i], cats[j], cats[k]), cats, vals,
                    vals[i] + vals[j] - vals[k], ["%d + %d = %d; %d − %d = %d." % (vals[i], vals[j], vals[i] + vals[j], vals[i] + vals[j],
                                                                                  vals[k], vals[i] + vals[j] - vals[k])])

    if d == 0:     # read one bar, find the smallest, compare two
        return _pick_t([], [t_read, t_read, t_least, t_more, t_total])
    if d == 2:     # stretch: totals and comparisons that need two steps
        return _pick_t([], [t_total, t_more, t_table, t_together, t_together])
    return _pick_t([], [t_read, t_total, t_more, t_table, t_least])


def _cnt(k):
    """A count before a coin ("four 5p coins", not "4 5p coins", which reads as 45p)."""
    return _COUNT_WORDS[k] if 0 <= k < len(_COUNT_WORDS) else str(k)


_COUNT_WORDS = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"]
