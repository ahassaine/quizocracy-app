# Year 7 generators: strand 7.9.
#
# Reasoning with number, sets and data: sets and Venn diagrams, the 0–1 probability scale and simple
# theoretical probability, sample spaces for one or two events, primes / HCF / LCM / prime
# factorisation, the mean, and reading and comparing charts.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S9 = "7.9 Sets, probability & data"


def _pf(n):
    out, k = [], 2
    while n > 1:
        while n % k == 0:
            out.append(k)
            n //= k
        k += 1
    return out


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


@skill("Y7.9.a", "Sets and Venn diagrams", S9)
def _(d=1):
    d = _d(d)
    hi = _by(d, 15, 20, 30)
    U = list(range(1, hi + 1))
    A_name, A = pick([("even numbers", {n for n in U if n % 2 == 0}), ("multiples of 3", {n for n in U if n % 3 == 0})])
    B_name, B = pick([("multiples of 5", {n for n in U if n % 5 == 0}), ("square numbers", {n for n in U if int(n ** .5) ** 2 == n}),
                      ("numbers greater than %d" % (hi // 2), {n for n in U if n > hi // 2})])

    def t_both():
        return _tb("Using the numbers 1 to %d: how many are %s AND %s?" % (hi, A_name, B_name), len(A & B), "int", {},
                   ["Both: %s." % (", ".join(map(str, sorted(A & B))) or "none")])

    def t_either():
        return _tb("Using the numbers 1 to %d: how many are %s OR %s (or both)?" % (hi, A_name, B_name), len(A | B), "int", {},
                   ["%d + %d − %d = %d." % (len(A), len(B), len(A & B), len(A | B))])

    def t_neither():
        return _tb("Using the numbers 1 to %d: how many are neither %s nor %s?" % (hi, A_name, B_name), hi - len(A | B),
                   "int", {}, ["%d − %d = %d." % (hi, len(A | B), hi - len(A | B))])

    def t_venn_table():
        a_only, both, b_only, none = random.randint(3, 15), random.randint(1, 10), random.randint(3, 15), random.randint(0, 9)
        clubs = pick([("Football", "Music"), ("Swimming", "Art"), ("Chess", "Drama")])
        rows = [["%s only" % clubs[0], a_only], ["Both", both], ["%s only" % clubs[1], b_only], ["Neither", none]]
        q = pick(["total", "club1", "club2"])
        ans = {"total": a_only + both + b_only + none, "club1": a_only + both, "club2": b_only + both}[q]
        text = {"total": "How many pupils are there altogether?", "club1": "How many pupils go to %s?" % clubs[0],
                "club2": "How many pupils go to %s?" % clubs[1]}[q]
        return _dt("The table gives the numbers in each region of a Venn diagram. %s" % text, ["Region", "Pupils"], rows, ans,
                   ["Add the regions that count."])

    def t_complement():
        return _complement()

    return _pick_t([t_both, t_either, t_neither, t_complement], [t_venn_table])


def _complement():
    tot = random.randint(20, 35)
    k = random.randint(5, tot - 3)
    return _tb("In a class of %d pupils, %d have a pet. How many do NOT have a pet?" % (tot, k), tot - k, "int", {},
               ["%d − %d = %d." % (tot, k, tot - k)])


@skill("Y7.9.b", "The probability scale and simple probability", S9)
def _(d=1):
    d = _d(d)

    def t_dice():
        q, fav = pick(_by(d, [("an even number", 3), ("a 6", 1), ("a number less than 3", 2), ("an odd number", 3)],
                          [("an even number", 3), ("a number greater than 4", 2), ("a 6", 1), ("a prime number", 3),
                           ("a number less than 3", 2), ("a multiple of 3", 2)],
                          [("a factor of 6", 4), ("a square number", 2), ("a number that is not a 3", 5), ("a prime number", 3),
                           ("a multiple of 3", 2), ("a number greater than 2", 4)]))
        return _fq("A fair six-sided dice is rolled. What is the probability of rolling %s? Simplest form." % q,
                   Fraction(fav, 6), ["%d out of 6 = %s." % (fav, _fs(Fraction(fav, 6)))])

    def t_bag():
        r, b, g = random.randint(1, _by(d, 5, 8, 15)), random.randint(1, _by(d, 5, 8, 15)), random.randint(0, _by(d, 4, 6, 10))
        col, n = pick([("red", r), ("blue", b)] + ([("green", g)] if g else []))
        if d == 2 and random.random() < 0.5:        # stretch: the complement, 'not red'
            return _fq("A bag has %d red, %d blue and %d green counters. One is taken at random. What is the probability it is "
                       "NOT %s? Simplest form." % (r, b, g, col), Fraction(r + b + g - n, r + b + g),
                       ["%d − %d = %d are not %s, out of %d." % (r + b + g, n, r + b + g - n, col, r + b + g)])
        return _fq("A bag has %d red, %d blue and %d green counters. One is taken at random. What is the probability it is "
                   "%s?" % (r, b, g, col), Fraction(n, r + b + g), ["%d out of %d." % (n, r + b + g)])

    def t_not():
        p = Fraction(random.randint(1, _by(d, 9, 9, 99)), _by(d, 10, 10, 100))
        return _tb("The probability that it rains tomorrow is %s. What is the probability that it does NOT rain? (decimal)"
                   % _ds(p), _ds(1 - p), "num", {}, ["Probabilities add to 1: 1 − %s = %s." % (_ds(p), _ds(1 - p))])

    def t_words():
        ev, ans = pick(_by(d, [("rolling a 7 on a normal dice", "impossible"), ("the sun rising tomorrow", "certain"),
                               ("getting heads when you flip a fair coin", "even chance"),
                               ("picking a blue counter from a bag of only red counters", "impossible")],
                           [("rolling a 7 on a normal dice", "impossible"), ("the sun rising tomorrow", "certain"),
                            ("getting heads when you flip a fair coin", "even chance"),
                            ("picking a red card from a bag of only red cards", "certain"),
                            ("picking a blue counter from a bag of only red counters", "impossible")],
                           [("picking a red counter from a bag of 9 red and 1 blue", "likely"),
                            ("rolling a 6 on a fair dice", "unlikely"),
                            ("getting an even number on a fair dice", "even chance"),
                            ("a fair spinner with 1 red and 4 blue sections landing on red", "unlikely"),
                            ("picking a blue counter from a bag of only red counters", "impossible"),
                            ("rolling a number less than 6 on a fair dice", "likely")]))
        return _wq("Describe the chance of %s: impossible, unlikely, even chance, likely or certain?" % ev, ans,
                   ["Use the 0–1 scale."], "word")

    def t_scale():
        ev, val = pick(_by(d, [("an impossible event", 0), ("a certain event", 1), ("an even chance", Fraction(1, 2))],
                           [("an impossible event", 0), ("a certain event", 1), ("an even chance", Fraction(1, 2))],
                           [("the chance of picking red from a bag of 3 red and 1 blue counter", Fraction(3, 4)),
                            ("the chance of picking red from a bag of 1 red and 4 blue counters", Fraction(1, 5)),
                            ("the chance of getting tails on a fair coin", Fraction(1, 2)), ("an impossible event", 0)]))
        return _tb("What number on the 0–1 probability scale shows %s?" % ev, _ds(val), "frac", {"text": True},
                   ["0 = impossible, 0.5 = even chance, 1 = certain."])

    def t_missing():
        ps = [Fraction(random.randint(_by(d, 1, 1, 5), _by(d, 2, 3, 30)), _by(d, 10, 10, 100)) for _ in range(3)]
        rest = 1 - sum(ps)
        cols = ["Red", "Blue", "Green", "Yellow"]
        rows = [[c, _ds(p)] for c, p in zip(cols, ps)] + [[cols[3], ""]]
        return _dt("A spinner lands on one of four colours. The table shows the probabilities. What is the probability of "
                   "Yellow?", ["Colour", "Probability"], rows, _ds(rest), ["1 − %s = %s." % (_ds(sum(ps)), _ds(rest))],
                   missing=[3, 1], atype="num")

    def t_spinner():
        hi = _by(d, 3, 4, 7)
        slices = [["Red", random.randint(1, hi)], ["Blue", random.randint(1, hi)], ["Green", random.randint(1, hi)]]
        tot = sum(s[1] for s in slices)
        k = random.randrange(3)
        return {"prompt": "The spinner is split into %d equal sections, shown by colour. What is the probability of %s? "
                          "Simplest form." % (tot, slices[k][0]), "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": k}, "answer": _fs(Fraction(slices[k][1], tot)),
                "answer_type": "frac", "solution": ["%d out of %d sections." % (slices[k][1], tot)]}

    return _pick_t([t_dice, t_bag, t_not, t_words, t_scale], [t_missing, t_spinner])


@skill("Y7.9.c", "Sample spaces and combined events", S9)
def _(d=1):
    d = _d(d)

    def t_count():
        a = pick(_by(d, [("a coin", 2), ("a 4-sided spinner", 4)], [("a coin", 2), ("a dice", 6), ("a 4-sided spinner", 4)],
                     [("a dice", 6), ("an 8-sided spinner", 8), ("a 5-colour spinner", 5)]))
        b = pick(_by(d, [("a coin", 2), ("a 3-colour spinner", 3)], [("a coin", 2), ("a dice", 6), ("a 3-colour spinner", 3)],
                     [("a coin", 2), ("a dice", 6), ("a 4-sided spinner", 4)]))
        who = ("Two coins" if a[0] == "a coin" else "Two dice") if a[0] == b[0] else "%s and %s" % (a[0].capitalize(), b[0])
        return _tb("%s are used together. How many possible outcomes are there?" % who, a[1] * b[1],
                   "int", {}, ["%d × %d = %d." % (a[1], b[1], a[1] * b[1])])

    def t_three():
        items = random.sample([("a coin", 2), ("a dice", 6), ("a 3-colour spinner", 3), ("a 4-sided spinner", 4)], 3)
        return _tb("%s, %s and %s are used together. How many possible outcomes are there?"
                   % (items[0][0].capitalize(), items[1][0], items[2][0]), items[0][1] * items[1][1] * items[2][1], "int", {},
                   ["%d × %d × %d = %d." % (items[0][1], items[1][1], items[2][1], items[0][1] * items[1][1] * items[2][1])])

    def t_dice_more():
        s = random.randint(7, 11)
        ways = sum(1 for x in range(1, 7) for y in range(1, 7) if x + y > s)
        return _fq("Two fair dice are rolled and the scores added. What is the probability of a total greater than %d? "
                   "Simplest form." % s, Fraction(ways, 36), ["%d of the 36 outcomes give more than %d." % (ways, s)])

    def t_two_dice_sum():
        s = random.randint(2, 12)
        ways = sum(1 for x in range(1, 7) for y in range(1, 7) if x + y == s)
        return _fq("Two fair dice are rolled and the scores added. What is the probability of a total of %d? Simplest form." % s,
                   Fraction(ways, 36), ["%d of the 36 outcomes give %d." % (ways, s)])

    def t_coins():
        if d == 2:                                  # stretch: three coins, 8 outcomes
            k = pick([0, 1, 2, 3])
            return _fq("Three fair coins are flipped. What is the probability of getting exactly %d head%s? Simplest form."
                       % (k, "" if k == 1 else "s"), Fraction({0: 1, 1: 3, 2: 3, 3: 1}[k], 8),
                       ["Outcomes: HHH, HHT, HTH, THH, HTT, THT, TTH, TTT."])
        k = pick([0, 1, 2])
        ways = {0: 1, 1: 2, 2: 1}[k]
        return _fq("Two fair coins are flipped. What is the probability of getting exactly %d head%s? Simplest form."
                   % (k, "" if k == 1 else "s"), Fraction(ways, 4), ["Outcomes: HH, HT, TH, TT."])

    def t_list():
        a, b = random.randint(2, _by(d, 3, 4, 7)), random.randint(2, _by(d, 3, 4, 8))
        if d == 2:                                  # stretch: a third course
            c = random.randint(2, 5)
            return _tb("A menu has %d starters, %d mains and %d desserts. How many different three-course meals (one of each) "
                       "are there?" % (a, b, c), a * b * c, "int", {}, ["%d × %d × %d = %d." % (a, b, c, a * b * c)])
        return _tb("A menu has %d starters and %d mains. How many different two-course meals (one of each) are there?" % (a, b),
                   a * b, "int", {}, ["%d × %d = %d." % (a, b, a * b)])

    def t_grid():
        if d == 2:                                  # stretch: 4 × 4 grid
            rows = [[str(x)] + [str(x + y) for y in range(1, 5)] for x in range(1, 5)]
            target = random.randint(3, 7)
            ways = sum(1 for x in range(1, 5) for y in range(1, 5) if x + y == target)
            return _dt("Two spinners each show 1, 2, 3 or 4. The table shows every total. What is the probability of a total of "
                       "%d? Simplest form." % target, ["+", "1", "2", "3", "4"], rows, _fs(Fraction(ways, 16)),
                       ["%d of the 16 totals are %d." % (ways, target)], atype="frac")
        rows = [[str(x)] + [str(x + y) for y in range(1, 4)] for x in range(1, 4)]
        target = random.randint(3, 5)
        ways = sum(1 for x in range(1, 4) for y in range(1, 4) if x + y == target)
        return _dt("Two spinners each show 1, 2 or 3. The table shows every total. What is the probability of a total of %d? "
                   "Simplest form." % target, ["+", "1", "2", "3"], rows, _fs(Fraction(ways, 9)),
                   ["%d of the 9 totals are %d." % (ways, target)], atype="frac")

    return _pick_t(_by(d, [t_count, t_coins, t_list], [t_count, t_two_dice_sum, t_coins, t_list],
                       [t_count, t_two_dice_sum, t_coins, t_list, t_three, t_dice_more]), [t_grid])


@skill("Y7.9.d", "Primes, HCF, LCM and prime factorisation", S9)
def _(d=1):
    d = _d(d)

    def t_pf():
        n = random.choice([x for x in range(12, _by(d, 60, 150, 400)) if len(_pf(x)) > 2])
        pf = _pf(n)
        k = random.randrange(len(pf))
        return _tb("Complete the prime factorisation:  %d = %s" % (n, " × ".join("___" if i == k else str(p) for i, p in enumerate(pf))),
                   pf[k], "int", {}, ["%d = %s." % (n, " × ".join(map(str, pf)))])

    def t_hcf():
        g = random.randint(2, 12)
        a, b = g * random.randint(2, 9), g * random.randint(2, 9)
        g = _gcd(a, b)
        return _tb("Find the HCF of %d and %d." % (a, b), g, "int", {}, ["The highest common factor is %d." % g])

    def t_lcm():
        a, b = random.randint(3, 15), random.randint(3, 15)
        if a == b:
            b += 1
        return _tb("Find the LCM of %d and %d." % (a, b), a * b // _gcd(a, b), "int", {},
                   ["The lowest common multiple is %d." % (a * b // _gcd(a, b))])

    def t_prime():
        n = random.randint(20, 120)
        p = len(_pf(n)) == 1
        return _wq("Is %d prime? (yes or no)" % n, "yes" if p else "no",
                   ["%d = %s." % (n, " × ".join(map(str, _pf(n))))], "yes / no")

    def t_product_index():
        n = pick([12, 18, 24, 36, 40, 48, 72, 80, 100])
        pf = _pf(n)
        return _tb("%d = 2^a × other primes. What is a (the power of 2)?" % n, pf.count(2), "int", {},
                   ["%d = %s." % (n, " × ".join(map(str, pf)))])

    def t_word():
        a, b = random.sample([6, 8, 9, 10, 12, 15], 2)
        return _tb("Two lighthouses flash every %d and %d seconds. They flash together now. After how many seconds will they "
                   "next flash together?" % (a, b), a * b // _gcd(a, b), "int", {"unit": "seconds"},
                   ["LCM of %d and %d = %d." % (a, b, a * b // _gcd(a, b))])

    return _pick_t([t_pf, t_hcf, t_lcm, t_prime, t_product_index, t_word])


@skill("Y7.9.e", "The mean, and comparing averages", S9)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 3, 4, 5), _by(d, 5, 7, 9))
    m = random.randint(_by(d, 5, 8, 20), _by(d, 20, 40, 99))
    sp = _by(d, 3, 6, 10)
    vals = [m + random.randint(-sp, sp) for _ in range(n - 1)]
    vals.append(m * n - sum(vals))
    if vals[-1] < 0:
        vals[-1] = m

    def t_mean():
        tot = sum(vals)
        return _tb("Find the mean of: %s" % ", ".join(map(str, vals)), _ds(Fraction(tot, len(vals))), "num", {},
                   ["%d ÷ %d = %s." % (tot, len(vals), _ds(Fraction(tot, len(vals))))]) if Fraction(tot, len(vals)).denominator in (1, 2, 4, 5) else t_missing()

    def t_missing():
        mm = random.randint(_by(d, 3, 5, 10), _by(d, 15, 30, 60))
        k = _by(d, 3, 4, 5)
        known = [random.randint(1, _by(d, mm + mm // 3, 2 * mm, mm + mm // 5)) for _ in range(k - 1)]   # keeps the last one positive
        last = mm * k - sum(known)
        if last < 0:
            known = [mm] * (k - 1)
            last = mm
        w = {3: ("three", "Two", "third"), 4: ("four", "Three", "fourth"), 5: ("five", "Four", "fifth")}[k]
        return _tb("The mean of %s numbers is %d. %s of them are %s. What is the %s?" % (w[0], mm, w[1], ", ".join(map(str, known)), w[2]),
                   last, "int", {}, ["Total = %d × %d = %d." % (mm, k, k * mm), "%d − %d = %d." % (k * mm, sum(known), last)])

    def t_which_average():
        q, ans = pick([("Which average is the most common value? (mean, median or mode)", "mode"),
                       ("Which average is the middle value when the data is in order? (mean, median or mode)", "median"),
                       ("Which average is the total divided by how many values? (mean, median or mode)", "mean")])
        return _wq(q, ans, ["Definitions of the averages."], "mean / median / mode")

    def t_mode():
        base = random.sample(range(1, _by(d, 15, 30, 60)), _by(d, 4, 5, 7))
        mode = pick(base)
        data = base + [mode, mode]
        random.shuffle(data)
        return _tb("Find the mode of: %s" % ", ".join(map(str, data)), mode, "int", {}, ["%d appears most often." % mode])

    def t_compare():
        a = [random.randint(10, _by(d, 20, 30, 99)) for _ in range(5)]
        b = [random.randint(10, _by(d, 20, 30, 99)) for _ in range(5)]
        ma, mb = Fraction(sum(a), 5), Fraction(sum(b), 5)
        if ma == mb:
            b[0] += 1
            mb = Fraction(sum(b), 5)
        return _dt("Two teams' scores are shown. Which team has the higher mean score? (A or B)", ["Team", "Scores"],
                   [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]], "A" if ma > mb else "B",
                   ["A: %s. B: %s." % (_ds(ma), _ds(mb))], atype="str")

    def t_bar_mean():
        cats = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        sp = _by(d, 2, 3, 6)
        mm = random.randint(_by(d, 13, 13, 25), _by(d, 30, 30, 60))   # the last bar is at least mm − 4·sp
        v = [mm + random.randint(-sp, sp) for _ in range(4)]
        v.append(5 * mm - sum(v))
        return _bar("The bar chart shows how many emails were received each day. What is the mean number per day?", cats, v, mm,
                    ["Total %d ÷ 5 = %d." % (sum(v), mm)])

    def t_new_value():
        k = random.randint(_by(d, 3, 4, 6), _by(d, 4, 6, 9))
        mm = random.randint(10, _by(d, 20, 30, 60))
        nv = random.randint(1, _by(d, 30, 40, 99))
        while (mm * k + nv) % (k + 1):
            nv += 1
        return _tb("The mean of %d numbers is %d. Another number, %d, is added. What is the new mean?" % (k, mm, nv),
                   (mm * k + nv) // (k + 1), "int", {}, ["Total %d + %d = %d." % (mm * k, nv, mm * k + nv),
                                                         "%d ÷ %d = %d." % (mm * k + nv, k + 1, (mm * k + nv) // (k + 1))])

    def t_best():
        q, ans = pick([("The data has one very large value (an outlier). Which average is affected most: mean, median or mode?",
                        "mean"),
                       ("Shoe sizes sold in a shop: which average tells the shop which size to order most of: mean, median or "
                        "mode?", "mode"),
                       ("Which average must be one of the values in the data: the mode or the mean?", "mode")])
        return _wq(q, ans, ["Think about what each average uses."], "mean / median / mode")

    def t_range_compare():
        a = random.sample(range(10, 60), 5)
        b = random.sample(range(10, 60), 5)
        while max(a) - min(a) == max(b) - min(b):
            b = random.sample(range(10, 60), 5)
        return _dt("Which class's test scores are more consistent (smaller range)? (A or B)", ["Class", "Scores"],
                   [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]],
                   "A" if max(a) - min(a) < max(b) - min(b) else "B",
                   ["Range A = %d, range B = %d." % (max(a) - min(a), max(b) - min(b))], atype="str")

    def t_mean_decimal():
        vals = [Decimal(random.randint(10, _by(d, 99, 99, 999))) / _by(d, 10, 10, 100) for _ in range(4)]
        while d == 2 and int(sum(vals) * 100) % 4:      # stretch: hundredths, but a mean with at most 2 decimal places
            vals[-1] += Decimal("0.01")
        return _tb("Find the mean of these times in seconds: %s" % ", ".join(_ds(v) for v in vals), _ds(sum(vals) / 4), "num",
                   {"unit": "seconds"}, ["%s ÷ 4 = %s." % (_ds(sum(vals)), _ds(sum(vals) / 4))])

    return _pick_t(_by(d, [t_mean, t_missing, t_which_average, t_mode, t_new_value],
                       [t_mean, t_missing, t_which_average, t_mode, t_new_value, t_best, t_mean_decimal],
                       [t_mean, t_missing, t_mode, t_new_value, t_best, t_mean_decimal]),
                   [t_compare, t_bar_mean, t_range_compare])


@skill("Y7.9.f", "Read, interpret and compare charts", S9)
def _(d=1):
    d = _d(d)
    cats = ["Walk", "Bus", "Car", "Cycle"]
    lo, hi = _by(d, (1, 12), (3, 30), (10, 60))

    def t_bar_total():
        v = [random.randint(lo, hi) for _ in cats]
        return _bar("The bar chart shows how pupils travel to school. How many pupils are there altogether?", cats, v, sum(v),
                    ["%s = %d." % (" + ".join(map(str, v)), sum(v))])

    def t_bar_fraction():
        v = [random.randint(_by(d, 1, 2, 5), _by(d, 6, 20, 40)) for _ in cats]
        k = random.randrange(4)
        return _bar("The bar chart shows how pupils travel to school. What fraction of the pupils %s? Simplest form."
                    % {"Walk": "walk", "Bus": "come by bus", "Car": "come by car", "Cycle": "cycle"}[cats[k]], cats, v,
                    _fs(Fraction(v[k], sum(v))), ["%d out of %d." % (v[k], sum(v))], atype="frac")

    def t_pie():
        a = pick(_by(d, [90, 180], [90, 120, 60, 180], [30, 45, 72, 135, 150]))
        rest = 360 - a
        b = rest // 2
        slices = [["Football", a], ["Tennis", b], ["Rugby", rest - b]]
        tot = pick([n for n in _by(d, (24, 36, 60), (24, 36, 60, 72, 120), (24, 40, 60, 72, 120, 180, 360)) if (n * a) % 360 == 0])
        return {"prompt": "The pie chart shows the favourite sport of %d pupils. The Football sector is %d°. How many chose "
                          "Football?" % (tot, a), "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": tot * a // 360, "answer_type": "int",
                "solution": ["%d/360 of %d = %d." % (a, tot, tot * a // 360)]}

    def t_line():
        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        v = [random.randint(_by(d, 10, 10, 20), _by(d, 40, 60, 99)) for _ in months]
        i, j = random.sample(range(5), 2)
        return _lg("The graph shows books sold each month. What is the difference between %s and %s?" % (months[i], months[j]),
                   list(zip(months, v)), abs(v[i] - v[j]), ["%d and %d." % (v[i], v[j])], "Books", "Month")

    def t_misleading():
        return _wq("A bar chart's vertical axis starts at 90 instead of 0. Does this make small differences look bigger or "
                   "smaller? (type bigger or smaller)", "bigger", ["Cutting the axis exaggerates differences."], "bigger / smaller")

    def t_bar_more():
        v = random.sample(range(lo, hi + 1), 4)
        i, j = random.sample(range(4), 2)
        if v[i] < v[j]:
            i, j = j, i
        return _bar("The bar chart shows how pupils travel to school. How many more pupils %s than %s?"
                    % ({"Walk": "walk", "Bus": "come by bus", "Car": "come by car", "Cycle": "cycle"}[cats[i]],
                       {"Walk": "walk", "Bus": "come by bus", "Car": "come by car", "Cycle": "cycle"}[cats[j]]),
                    cats, v, v[i] - v[j], ["%d − %d = %d." % (v[i], v[j], v[i] - v[j])])

    def t_bar_mode():
        v = random.sample(range(lo, hi + 1), 4)
        return _bar("The bar chart shows how pupils travel to school. Which way of travelling is the mode? (type it as on the chart)",
                    cats, v, cats[v.index(max(v))], ["The tallest bar is %s." % cats[v.index(max(v))]], atype="str")

    def t_pictogram():
        key = pick(_by(d, [2, 10], [2, 4, 10], [4, 10, 20]))
        vals = [key * random.randint(1, 8) + (key // 2 if random.random() < _by(d, 0, 0.3, 0.6) else 0) for _ in range(4)]
        names = ["Mon", "Tue", "Wed", "Thu"]
        k = random.randrange(4)
        return {"prompt": "The pictogram shows cakes sold each day. Each symbol stands for %d cakes. How many were sold on %s?"
                          % (key, names[k]), "component": "pictogram",
                "spec": {"categories": names, "values": vals, "key": key, "symbol": "circle", "unit": "cakes"},
                "answer": vals[k], "answer_type": "int", "solution": ["Count the symbols and multiply by %d: %d." % (key, vals[k])]}

    def t_line_max():
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        v = random.sample(range(_by(d, 10, 10, 20), _by(d, 40, 60, 99)), 6)
        return _lg("The graph shows books sold each month. In which month were the most books sold?", list(zip(months, v)),
                   months[v.index(max(v))], ["The highest point is %s (%d)." % (months[v.index(max(v))], max(v))], "Books", "Month",
                   atype="str")

    def t_pie_angle():
        a = pick(_by(d, [90, 120, 180, 60], [45, 60, 72, 90, 120, 135, 150], [40, 45, 72, 135, 150, 210]))
        tot = pick([n for n in (24, 40, 60, 72, 120, 180, 360) if (n * a) % 360 == 0])
        rest = 360 - a
        slices = [["Cats", a], ["Dogs", rest // 2], ["Fish", rest - rest // 2]]
        return {"prompt": "The pie chart shows the pets of %d people. The Cats sector has an angle of %d°. What fraction of the "
                          "people have cats? Simplest form." % (tot, a), "component": "pie_chart",
                "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": _fs(Fraction(a, 360)),
                "answer_type": "frac", "solution": ["%d/360 = %s." % (a, _fs(Fraction(a, 360)))]}

    def t_line_rise():
        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        v = [random.randint(_by(d, 10, 10, 20), _by(d, 40, 60, 99)) for _ in months]
        i = random.randrange(4)
        if v[i + 1] == v[i]:
            v[i + 1] += 3
        word = "increase" if v[i + 1] > v[i] else "decrease"
        return _lg("The graph shows books sold each month. By how many did sales %s from %s to %s?" % (word, months[i], months[i + 1]),
                   list(zip(months, v)), abs(v[i + 1] - v[i]), ["%d to %d." % (v[i], v[i + 1])], "Books", "Month")

    return _pick_t([t_misleading], [t_bar_total, t_bar_fraction, t_pie, t_line, t_bar_more, t_bar_mode, t_pictogram, t_line_max,
                                    t_pie_angle, t_line_rise])
