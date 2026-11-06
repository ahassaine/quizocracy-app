# Year 9 generators: strands 9.8 and 9.9.
#
# Probability: mutually exclusive events and the sum to 1, expected frequency, relative frequency and
# fairness, probability from Venn diagrams and two-way tables, independent events from sample spaces.
# Statistics: averages and range from frequency tables, grouped data (modal class, class with the
# median, estimated mean), comparing distributions, choosing and criticising charts.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S8 = "9.8 Probability"
S9 = "9.9 Statistics"


# ================================================================== 9.8 ======
@skill("Y9.8.a", "Mutually exclusive events and probabilities summing to 1", S8)
def _(d=1):
    d = _d(d)
    ps = [Fraction(random.randint(1, 4), 20) for _ in range(3)]
    while sum(ps) >= 1:
        ps = [Fraction(random.randint(1, 4), 20) for _ in range(3)]

    def t_missing():
        cols = ["Red", "Blue", "Green", "Yellow"]
        rows = [[c, _ds(p)] for c, p in zip(cols, ps)] + [["Yellow", ""]]
        return _dt("A spinner can only land on these four colours. What is P(Yellow)?", ["Colour", "Probability"], rows, _ds(1 - sum(ps)),
                   ["1 − %s = %s." % (_ds(sum(ps)), _ds(1 - sum(ps)))], missing=[3, 1], atype="num")

    def t_or():
        return _tb("P(red) = %s and P(blue) = %s. Red and blue cannot both happen. What is P(red or blue)?" % (_ds(ps[0]), _ds(ps[1])),
                   _ds(ps[0] + ps[1]), "num", {}, ["Mutually exclusive: add them: %s." % _ds(ps[0] + ps[1])])

    def t_not():
        p = Fraction(random.randint(1, 19), 20)
        return _tb("The probability that a train is late is %s. What is the probability it is NOT late?" % _ds(p), _ds(1 - p), "num", {},
                   ["1 − %s = %s." % (_ds(p), _ds(1 - p))])

    def t_algebra():
        k = random.randint(2, 4)
        x = Fraction(1, k + 2)
        return _fq("A bag has red, blue and green counters. P(red) = x, P(blue) = %dx and P(green) = x. What is x?" % k, x,
                   ["x + %dx + x = 1, so %dx = 1." % (k, k + 2), "x = %s." % _fs(x)])

    def t_exclusive():
        q, a = pick([("Rolling a 2 and rolling a 5 on one throw of a dice", "yes"),
                     ("Rolling an even number and rolling a 4 on one throw of a dice", "no"),
                     ("Picking a heart and picking a club with one card", "yes"),
                     ("Picking a red card and picking a king with one card", "no")])
        return _wq("%s: are these mutually exclusive? (yes or no)" % q, a, ["Can both happen at once? If not, they are mutually exclusive."], "yes / no")

    def t_algebra_decimal():
        known = Fraction(random.randint(1, 4), 10)
        k = random.randint(2, 4)
        x = (1 - known) / (k + 1)
        if x.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
            known, k = Fraction(1, 10), 2
            x = (1 - known) / (k + 1)
        return _dt("These are the only outcomes of a game. Find the value of x.", ["Outcome", "Probability"],
                   [["Win", _ds(known)], ["Lose", "%dx" % k], ["Draw", "x"]], _ds(x),
                   ["%s + %dx + x = 1, so %dx = %s." % (_ds(known), k, k + 1, _ds(1 - known)), "x = %s." % _ds(x)], atype="num")

    def t_how_many():
        n = pick([20, 40, 50, 60, 80, 100])
        p = Fraction(random.randint(1, n - 1), n)
        while p.denominator not in (2, 4, 5, 10, 20, 25, 50, 100):
            p = Fraction(random.randint(1, n - 1), n)
        return _tb("A bag holds only red and blue counters, %d in total. P(red) = %s. How many blue counters are there?" % (n, _ds(p)),
                   int(n * (1 - p)), "int", {}, ["P(blue) = %s." % _ds(1 - p), "%s × %d = %d." % (_ds(1 - p), n, int(n * (1 - p)))])

    def t_three_or():
        return _tb("A spinner lands on red with probability %s, blue %s and green %s. What is P(red or blue or green)?" % (_ds(ps[0]), _ds(ps[1]), _ds(ps[2])),
                   _ds(sum(ps)), "num", {}, ["They are mutually exclusive, so add: %s." % _ds(sum(ps))])

    def t_frac_not():
        q = random.randint(3, 12)
        p = Fraction(random.randint(1, q - 1), q)
        return _fq("The probability that it snows tomorrow is %s. What is the probability that it does not snow?" % _fs(p), 1 - p,
                   ["1 − %s = %s." % (_fs(p), _fs(1 - p))])

    def t_could_be():
        pa, pb = Fraction(random.randint(2, 8), 10), Fraction(random.randint(2, 8), 10)
        return _wq("P(A) = %s and P(B) = %s. Could A and B be mutually exclusive? (yes or no)" % (_ds(pa), _ds(pb)),
                   "yes" if pa + pb <= 1 else "no", ["If they were, P(A or B) = %s, which must not be more than 1." % _ds(pa + pb)], "yes / no")

    def t_bar():
        cols = ["Red", "Blue", "Green", "Yellow"]
        cnt = [random.randint(1, 12) for _ in cols]
        k = random.randrange(4)
        return _bar("The bar chart shows the counters in a bag. One counter is taken at random. What is P(%s)? (fraction)" % cols[k].lower(),
                    cols, cnt, _fs(Fraction(cnt[k], sum(cnt))), ["%d out of %d counters." % (cnt[k], sum(cnt))], atype="frac")

    return _pick_t([t_or, t_not, t_algebra, t_exclusive, t_how_many, t_three_or, t_frac_not, t_could_be], [t_missing, t_algebra_decimal, t_bar])


@skill("Y9.8.b", "Expected and relative frequency", S8)
def _(d=1):
    d = _d(d)

    def t_expected():
        p = pick([Fraction(1, 2), Fraction(1, 4), Fraction(1, 6), Fraction(1, 5), Fraction(3, 10)])
        n = p.denominator * random.randint(5, 40)
        return _tb("The probability of an event is %s. In %d trials, how many times would you expect it to happen?" % (_fs(p), n), int(p * n),
                   "int", {}, ["%s × %d = %d." % (_fs(p), n, int(p * n))])

    def t_dice():
        n = 6 * random.randint(5, 50)
        return _tb("A fair dice is rolled %d times. About how many sixes would you expect?" % n, n // 6, "int", {}, ["%d ÷ 6 = %d." % (n, n // 6)])

    def t_relative():
        n = random.choice([20, 25, 40, 50, 100, 200])
        k = random.randint(1, n - 1)
        return _tb("A drawing pin lands point up %d times in %d throws. What is the relative frequency of point up? (decimal)" % (k, n),
                   _ds(Fraction(k, n)), "num", {}, ["%d ÷ %d = %s." % (k, n, _ds(Fraction(k, n)))])

    def t_fair():
        k = pick([100, 102, 97, 250, 180])
        fair = abs(k - 100) <= 10
        return _wq("A dice is rolled 600 times and shows a six %d times. Does it seem fair? (yes or no)" % k, "yes" if fair else "no",
                   ["Expected about 100 sixes."], "yes / no")

    def t_estimate():
        n = random.choice([50, 100])
        k = random.randint(5, n - 5)
        N = pick([500, 1000, 2000])
        return _tb("In %d trials a spinner landed on blue %d times. Estimate how many times it would land on blue in %d spins." % (n, k, N),
                   k * N // n, "int", {}, ["%d/%d × %d = %d." % (k, n, N, k * N // n)])

    def t_table():
        cols = ["Red", "Blue", "Green"]
        f = [random.randint(5, 30) for _ in cols]
        k = random.randrange(3)
        return _dt("A spinner was spun %d times with these results. What is the relative frequency of %s? (fraction in simplest form)"
                   % (sum(f), cols[k]), ["Colour", "Frequency"], [[c, x] for c, x in zip(cols, f)], _fs(Fraction(f[k], sum(f))),
                   ["%d out of %d." % (f[k], sum(f))], atype="frac")

    def t_rf_count():
        n = pick([50, 100, 200, 400, 500])
        k = random.randint(1, 19) * n // 20
        return _tb("After %d trials, the relative frequency of a success is %s. How many successes were there?" % (n, _ds(Fraction(k, n))), k,
                   "int", {}, ["%s × %d = %d." % (_ds(Fraction(k, n)), n, k)])

    def t_reliable():
        small, big = pick([10, 20, 25]), pick([200, 400, 500])
        ps, pb = Fraction(random.randint(1, small - 1), small), Fraction(random.randint(1, 19), 20)
        (n1, k1), (n2, k2) = random.sample([(small, int(ps * small)), (big, int(pb * big))], 2)
        return _tb("Two pupils test the same spinner. One gets %s in %d spins; the other gets %s in %d spins. Give the more reliable "
                   "estimate of P(red) as a decimal." % (_pl(k1, "red"), n1, _pl(k2, "red"), n2), _ds(pb), "num", {},
                   ["More trials give a more reliable estimate: %d ÷ %d = %s." % (int(pb * big), big, _ds(pb))])

    def t_settle():
        p = pick([Fraction(3, 10), Fraction(2, 5), Fraction(1, 4), Fraction(3, 5), Fraction(7, 10)])
        trials = [10, 20, 50, 100, 200, 500]
        rf = [p + Fraction(random.randint(-3, 3), 20) for _ in trials[:3]] + [p + Fraction(random.randint(-1, 1), 50), p + Fraction(random.choice([-1, 1]), 100), p]
        return _lg("The graph shows the relative frequency of a coin landing on a stand after more and more trials. What is the best estimate "
                   "of the probability? (decimal)", [["%d" % t, float(v)] for t, v in zip(trials, rf)], _ds(p),
                   ["Use the value the graph settles at after the most trials: %s." % _ds(p)], "Relative frequency", "Trials", atype="num")

    def t_game():
        cost, prize = pick([(50, 2), (20, 1), (50, 3), (25, 1)])
        q = pick([5, 10, 4])
        n = q * pick([10, 20, 50])
        profit = n * cost - (n // q) * prize * 100
        return _tb("A stall charges %dp a go. The chance of winning a £%d prize is 1/%d. About how much profit should the stall make from %d "
                   "goes, in pence? (Use a minus sign for a loss.)" % (cost, prize, q, n), profit, "int", {"unit": "p"},
                   ["Takings %d × %dp = %dp." % (n, cost, n * cost), "Expected wins %d ÷ %d = %d, paying %dp." % (n, q, n // q, (n // q) * prize * 100),
                    "Profit %dp." % profit])

    def t_even():
        n = 2 * random.randint(10, 150)
        return _tb("A fair dice is rolled %d times. How many even numbers would you expect?" % n, n // 2, "int", {}, ["P(even) = 1/2; %d ÷ 2 = %d." % (n, n // 2)])

    def t_spinner_table():
        ps = pick([[Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)], [Fraction(2, 5), Fraction(3, 10), Fraction(1, 5), Fraction(1, 10)],
                   [Fraction(1, 3), Fraction(1, 3), Fraction(1, 6), Fraction(1, 6)]])
        cols = ["Red", "Blue", "Green", "White"]
        k = random.randrange(4)
        n = 120 * random.randint(1, 5)
        return _dt("A spinner has these probabilities. It is spun %d times. How many times would you expect %s?" % (n, cols[k].lower()),
                   ["Colour", "Probability"], [[c, _fs(p)] for c, p in zip(cols, ps)], int(ps[k] * n), ["%s × %d = %d." % (_fs(ps[k]), n, int(ps[k] * n))])

    return _pick_t([t_expected, t_dice, t_relative, t_fair, t_estimate, t_rf_count, t_reliable, t_game, t_even], [t_table, t_settle, t_spinner_table])


@skill("Y9.8.c", "Probability from Venn diagrams and two-way tables", S8)
def _(d=1):
    d = _d(d)
    a_only, both, b_only, none = random.randint(2, 15), random.randint(1, 10), random.randint(2, 15), random.randint(0, 10)
    tot = a_only + both + b_only + none
    A, B = pick([("play football", "play tennis"), ("have a cat", "have a dog"), ("like maths", "like art")])

    def t_both():
        rows = [["%s only" % A, a_only], ["both", both], ["%s only" % B, b_only], ["neither", none]]
        return _dt("The table gives the regions of a Venn diagram for %d pupils. A pupil is chosen at random. What is the probability they %s "
                   "AND %s? (simplest form)" % (tot, A, B), ["Region", "Pupils"], rows, _fs(Fraction(both, tot)),
                   ["%d out of %d." % (both, tot)], atype="frac")

    def t_either():
        rows = [["%s only" % A, a_only], ["both", both], ["%s only" % B, b_only], ["neither", none]]
        return _dt("The table gives the regions of a Venn diagram. A pupil is chosen at random. What is the probability they %s OR %s (or both)? "
                   "(simplest form)" % (A, B), ["Region", "Pupils"], rows, _fs(Fraction(a_only + both + b_only, tot)),
                   ["%d out of %d." % (a_only + both + b_only, tot)], atype="frac")

    def t_given():
        rows = [["%s only" % A, a_only], ["both", both], ["%s only" % B, b_only], ["neither", none]]
        return _dt("Of the pupils who %s, one is chosen at random. What is the probability they also %s? (simplest form)" % (A, B),
                   ["Region", "Pupils"], rows, _fs(Fraction(both, a_only + both)), ["%d out of %d." % (both, a_only + both)], atype="frac")

    def t_two_way():
        bl, bn, gl, gn = [random.randint(3, 20) for _ in range(4)]
        rows = [["Boys", bl, bn], ["Girls", gl, gn]]
        return _dt("A pupil is chosen at random. What is the probability it is a girl who wears glasses? (simplest form)",
                   ["", "Glasses", "No glasses"], rows, _fs(Fraction(gl, bl + bn + gl + gn)),
                   ["%d out of %d." % (gl, bl + bn + gl + gn)], atype="frac")

    def t_two_way_missing():
        bl, bn, gl, gn = [random.randint(3, 20) for _ in range(4)]
        rows = [["Boys", bl, bn, bl + bn], ["Girls", gl, gn, gl + gn], ["Total", bl + gl, bn + gn, bl + bn + gl + gn]]
        r, c = random.choice([(0, 1), (0, 2), (1, 1), (1, 2), (2, 3)])
        return _dt("Complete the two-way table.", ["", "Glasses", "No glasses", "Total"], rows, rows[r][c],
                   ["Each row and each column adds up to its total."], missing=[r, c])

    def t_two_way_given():
        bl, bn, gl, gn = [random.randint(3, 20) for _ in range(4)]
        rows = [["Boys", bl, bn], ["Girls", gl, gn]]
        who, n, k = pick([("girls", gl + gn, gl), ("boys", bl + bn, bl)])
        return _dt("One of the %s is chosen at random. What is the probability they wear glasses? (simplest form)" % who,
                   ["", "Glasses", "No glasses"], rows, _fs(Fraction(k, n)), ["%d of the %d %s." % (k, n, who)], atype="frac")

    def t_not_a():
        rows = [["%s only" % A, a_only], ["both", both], ["%s only" % B, b_only], ["neither", none]]
        return _dt("A pupil is chosen at random. What is the probability they do NOT %s? (simplest form)" % A, ["Region", "Pupils"], rows,
                   _fs(Fraction(b_only + none, tot)), ["Not in the %s circle: %d + %d = %d out of %d." % (A, b_only, none, b_only + none, tot)], atype="frac")

    def t_count_both():
        nA, nB = a_only + both, b_only + both
        return _tb("In a group of %d pupils, %d %s, %d %s and %d do neither. How many do both?" % (tot, nA, A, nB, B, none), both, "int", {},
                   ["%d + %d + %d − %d = %d (counted twice)." % (nA, nB, none, tot, both)])

    def t_only():
        rows = [["%s only" % A, a_only], ["both", both], ["%s only" % B, b_only], ["neither", none]]
        return _dt("The table gives the regions of a Venn diagram. A pupil is chosen at random. What is the probability they are in exactly "
                   "one of the two circles? (simplest form)", ["Region", "Pupils"], rows, _fs(Fraction(a_only + b_only, tot)),
                   ["%d + %d = %d out of %d." % (a_only, b_only, a_only + b_only, tot)], atype="frac")

    def t_col_given():
        bl, bn, gl, gn = [random.randint(3, 20) for _ in range(4)]
        rows = [["Boys", bl, bn], ["Girls", gl, gn]]
        return _dt("A pupil who wears glasses is chosen at random. What is the probability it is a boy? (simplest form)",
                   ["", "Glasses", "No glasses"], rows, _fs(Fraction(bl, bl + gl)), ["%d of the %d who wear glasses." % (bl, bl + gl)], atype="frac")

    return _pick_t([t_count_both], [t_both, t_either, t_given, t_two_way, t_two_way_missing, t_two_way_given, t_not_a, t_only, t_col_given])


@skill("Y9.8.d", "Independent events and sample spaces", S8)
def _(d=1):
    d = _d(d)

    def t_coin_dice():
        k = random.randint(1, 6)
        return _fq("A coin is flipped and a dice is rolled. What is P(heads and a %d)?" % k, Fraction(1, 12), ["1/2 × 1/6 = 1/12."])

    def t_two_dice():
        t = random.randint(2, 12)
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == t)
        return _fq("Two dice are rolled. What is P(total = %d)? (simplest form)" % t, Fraction(ways, 36), ["%d of 36 outcomes." % ways])

    def t_double():
        return _fq("Two dice are rolled. What is P(a double)? (simplest form)", Fraction(1, 6), ["6 doubles out of 36 = 1/6."])

    def t_product():
        p, q = pick([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)]), pick([Fraction(2, 5), Fraction(1, 5), Fraction(3, 10)])
        return _fq("P(A) = %s and P(B) = %s, and A and B are independent. What is P(A and B)?" % (_fs(p), _fs(q)), p * q,
                   ["Multiply: %s." % _fs(p * q)])

    def t_count():
        a, b, c = random.randint(2, 4), random.randint(2, 5), random.randint(2, 3)
        return _tb("A meal has %d starters, %d mains and %d desserts. How many different three-course meals are there?" % (a, b, c), a * b * c,
                   "int", {}, ["%d × %d × %d = %d." % (a, b, c, a * b * c)])

    def t_at_least():
        return _fq("Two fair coins are flipped. What is P(at least one head)?", Fraction(3, 4), ["1 − P(no heads) = 1 − 1/4."])

    def t_two_spinners():
        n1, n2 = random.randint(3, 6), random.randint(3, 8)
        r1, r2 = random.randint(1, n1 - 1), random.randint(1, n2 - 1)
        return _fq("Spinner A has %d equal sections, %d of them red. Spinner B has %d equal sections, %d of them red. Both are spun. What is "
                   "P(both red)? (simplest form)" % (n1, r1, n2, r2), Fraction(r1, n1) * Fraction(r2, n2),
                   ["%d/%d × %d/%d = %s." % (r1, n1, r2, n2, _fs(Fraction(r1, n1) * Fraction(r2, n2)))])

    def t_outcomes():
        coins, dice = random.randint(1, 3), random.randint(1, 2)
        return _tb("%d coin%s and %d dice are thrown together. How many different outcomes are there?" % (coins, "" if coins == 1 else "s", dice),
                   2 ** coins * 6 ** dice, "int", {}, ["2^%d × 6^%d = %d." % (coins, dice, 2 ** coins * 6 ** dice)])

    def t_not_both():
        p, q = pick([Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]), pick([Fraction(1, 2), Fraction(3, 5), Fraction(5, 6)])
        return _fq("A pupil takes two independent tests. P(pass the first) = %s and P(pass the second) = %s. What is the probability they do NOT "
                   "pass both?" % (_fs(p), _fs(q)), 1 - p * q, ["P(both) = %s." % _fs(p * q), "1 − %s = %s." % (_fs(p * q), _fs(1 - p * q))])

    def t_grid_event():
        kind = pick(["product even", "sum even", "difference 0", "sum more than 8", "product more than 12"])
        test = {"product even": lambda a, b: a * b % 2 == 0, "sum even": lambda a, b: (a + b) % 2 == 0, "difference 0": lambda a, b: a == b,
                "sum more than 8": lambda a, b: a + b > 8, "product more than 12": lambda a, b: a * b > 12}[kind]
        k = sum(1 for a in range(1, 7) for b in range(1, 7) if test(a, b))
        what = {"product even": "the product is even", "sum even": "the total is even", "difference 0": "the two scores are the same",
                "sum more than 8": "the total is more than 8", "product more than 12": "the product is more than 12"}[kind]
        return _fq("Two fair dice are rolled. Use a sample-space grid: what is the probability that %s? (simplest form)" % what, Fraction(k, 36),
                   ["%d of the 36 outcomes." % k])

    def t_independent():
        q, a = pick([("Rolling a dice and then flipping a coin", "yes"), ("Taking two sweets from a bag without putting the first back", "no"),
                     ("Spinning a spinner twice", "yes"), ("Picking two cards from a pack without replacing the first", "no")])
        return _wq("%s: are the two events independent? (yes or no)" % q, a,
                   ["Independent means the first result does not change the chances for the second."], "yes / no")

    def t_three_coins():
        heads = random.randint(0, 3)
        ways = [1, 3, 3, 1][heads]
        what = "no heads" if heads == 0 else "exactly %d head%s" % (heads, "" if heads == 1 else "s")
        return _fq("Three fair coins are flipped. What is P(%s)? (simplest form)" % what,
                   Fraction(ways, 8), ["%d of the 8 outcomes (HHH, HHT, …)." % ways])

    return _pick_t([t_coin_dice, t_two_dice, t_double, t_product, t_count, t_at_least, t_two_spinners, t_outcomes, t_not_both, t_grid_event,
                    t_independent, t_three_coins])



# ================================================================== 9.9 ======
_FREQ_CTX = [("Pets", "pets", "pupils", "the number of pets owned by some pupils"),
             ("Goals", "goals", "matches", "the goals a team scored in each match"),
             ("Siblings", "brothers and sisters", "pupils", "how many brothers and sisters some pupils have"),
             ("Books", "books", "pupils", "how many books some pupils read last month")]


@skill("Y9.9.a", "Averages and range from a frequency table", S9)
def _(d=1):
    d = _d(d)
    head, noun, people, desc = pick(_FREQ_CTX)
    vals = [0, 1, 2, 3, 4]
    f = [random.randint(1, 12) for _ in vals]
    n = sum(f)
    tot = sum(v * x for v, x in zip(vals, f))
    rows = [[v, x] for v, x in zip(vals, f)]
    hdr = [head, "Frequency"]

    def t_mean():
        m = Fraction(tot, n)
        if m.denominator not in (1, 2, 4, 5, 10, 20, 25, 50):
            return _dt("The table shows %s. What is the mean, to 1 decimal place?" % desc, hdr,
                       rows, round(float(m) + 1e-12, 1), ["Total %d ÷ %d %s." % (tot, n, people)], atype="num")
        return _dt("The table shows %s. What is the mean number of %s?" % (desc, noun), hdr, rows,
                   _ds(m), ["Σfx = %d; n = %d; %d ÷ %d = %s." % (tot, n, tot, n, _ds(m))], atype="num")

    def t_mode():
        if f.count(max(f)) > 1:
            return t_total()
        return _dt("The table shows %s. What is the mode?" % desc, hdr, rows, vals[f.index(max(f))],
                   ["The highest frequency is %d, for the value %d." % (max(f), vals[f.index(max(f))])])

    def t_total():
        return _dt("The table shows %s. How many %s are there altogether?" % (desc, people), hdr, rows, n,
                   ["%s = %d." % (" + ".join(map(str, f)), n)])

    def t_median():
        data = sorted(v for v, x in zip(vals, f) for _ in range(x))
        med = Fraction(data[n // 2]) if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
        return _dt("The table shows %s. What is the median?" % desc, hdr, rows, _ds(med),
                   ["There are %d values; the median is the %s value." % (n, "middle" if n % 2 else "mean of the middle two")], atype="num")

    def t_range():
        used = [v for v, x in zip(vals, f) if x]
        return _dt("The table shows %s. What is the range?" % desc, hdr, rows, max(used) - min(used),
                   ["%d − %d." % (max(used), min(used))])

    def t_sum():
        return _dt("The table shows %s. What is the total number of %s?" % (desc, noun), hdr, rows, tot,
                   ["Multiply each value by its frequency and add: %s = %d." % (" + ".join("%d×%d" % (v, x) for v, x in zip(vals, f)), tot)])

    def t_more_than():
        k = random.randint(0, 3)
        return _dt("The table shows %s. How many of the %s had more than %d?" % (desc, people, k), hdr, rows, sum(f[k + 1:]),
                   ["Add the frequencies for %s: %d." % (", ".join(str(v) for v in vals[k + 1:]), sum(f[k + 1:]))])

    def t_bar():
        if f.count(max(f)) > 1:
            return _bar("The bar chart shows %s. How many %s are there altogether?" % (desc, people), [str(v) for v in vals], f, n,
                        ["Add the bar heights: %d." % n])
        return _bar("The bar chart shows %s. What is the mode?" % desc, [str(v) for v in vals], f, vals[f.index(max(f))],
                    ["The tallest bar is at %d." % vals[f.index(max(f))]])

    def t_fx():
        fx = [[v, x, v * x] for v, x in zip(vals, f)]
        i = random.randint(1, 4)
        return _dt("Complete the f × x column for this table of %s." % noun, [head, "Frequency (f)", "f × x"], fx, fx[i][2],
                   ["%d × %d = %d." % (fx[i][1], fx[i][0], fx[i][2])], missing=[i, 2])

    def t_missing_freq():
        for _ in range(200):
            ff = [random.randint(1, 10) for _ in vals]
            j = random.randint(1, 4)
            nn, tt = sum(ff), sum(v * x for v, x in zip(vals, ff))
            m = Fraction(tt, nn)
            if m.denominator in (1, 2, 4, 5) and m != vals[j]:
                rr = [[v, x if k != j else "?"] for k, (v, x) in enumerate(zip(vals, ff))]
                return _dt("The table shows %s. The mean is %s. Find the missing frequency." % (desc, _ds(m)), hdr, rr, ff[j],
                           ["Let the missing frequency be k: (%d + %dk) ÷ (%d + k) = %s." % (tt - vals[j] * ff[j], vals[j], nn - ff[j], _ds(m)),
                            "k = %d." % ff[j]])
        return t_total()

    return _pick_t([], [t_mean, t_mode, t_total, t_median, t_range, t_sum, t_more_than, t_bar, t_fx, t_missing_freq])


_GROUP_CTX = [("Time (min)", "t", "times in minutes", 0, (5, 10)),
              ("Height (cm)", "h", "heights in cm", 140, (5, 10)),
              ("Mass (kg)", "m", "masses in kg", 40, (5, 10)),
              ("Score", "s", "test scores", 20, (10, 20))]


@skill("Y9.9.b", "Grouped data: modal class and estimated mean", S9)
def _(d=1):
    d = _d(d)
    head, v, desc, base, widths = pick(_GROUP_CTX)
    w = pick(widths)
    groups = [(base + i * w, base + (i + 1) * w) for i in range(4)]
    f = [random.randint(2, 15) for _ in groups]
    rows = [["%d < %s ≤ %d" % (g[0], v, g[1]), x] for g, x in zip(groups, f)]
    hdr = [head, "Frequency"]

    def t_modal():
        if f.count(max(f)) > 1:
            return t_total()
        g = groups[f.index(max(f))]
        return _dt("The table shows %s. Which is the modal class? Type its lower end." % desc, hdr, rows,
                   g[0], ["The modal class is %d < %s ≤ %d." % (g[0], v, g[1])])

    def t_total():
        return _dt("The table shows %s. How many values are in the table?" % desc, hdr, rows, sum(f), ["%s = %d." % (" + ".join(map(str, f)), sum(f))])

    def t_midpoint():
        k = random.randrange(4)
        return _dt("What is the midpoint of the class %d < %s ≤ %d?" % (groups[k][0], v, groups[k][1]), hdr, rows,
                   _ds(Fraction(sum(groups[k]), 2)), ["(%d + %d) ÷ 2." % groups[k]], atype="num")

    def t_est_mean():
        mids = [Fraction(a + b, 2) for a, b in groups]
        m = sum(mp * x for mp, x in zip(mids, f)) / sum(f)
        q = _dt("The table shows %s. Estimate the mean, to 1 decimal place." % desc, hdr, rows, round(float(m) + 1e-12, 1),
                ["Use midpoints: Σ(midpoint × f) ÷ Σf = %s." % format((Decimal(m.numerator) / m.denominator).quantize(Decimal("0.001"), rounding="ROUND_HALF_UP"), "f")], atype="num")
        q["tolerance"] = 0.051
        return q

    def t_median_class():
        n = sum(f)
        pos = Fraction(n + 1, 2)
        cum = 0
        for g, x in zip(groups, f):
            cum += x
            if cum >= pos:
                return _dt("The table shows %s. Which class contains the median? Type its lower end." % desc, hdr, rows, g[0],
                           ["The median is the %s value, in %d < %s ≤ %d." % (_ds(pos), g[0], v, g[1])])
        return t_total()

    def t_why_estimate():
        return _wq("Why can the mean of grouped data only be estimated? (one word: we do not know the exact ...)", "values",
                   ["The original values are lost when data is grouped."], "one word")

    def t_more_than():
        k = random.randint(1, 3)
        return _dt("The table shows %s. How many values are more than %d?" % (desc, groups[k][0]), hdr, rows, sum(f[k:]),
                   ["Add the classes above %d: %d." % (groups[k][0], sum(f[k:]))])

    def t_range_max():
        return _dt("The table shows %s. What is the greatest possible range of the data?" % desc, hdr, rows, groups[-1][1] - groups[0][0],
                   ["Largest possible value %d, smallest just above %d: about %d − %d = %d." % (groups[-1][1], groups[0][0], groups[-1][1], groups[0][0],
                                                                                              groups[-1][1] - groups[0][0])])

    def t_total_est():
        mids = [Fraction(a + b, 2) for a, b in groups]
        tot = sum(mp * x for mp, x in zip(mids, f))
        return _dt("The table shows %s. Estimate the total of all the values (Σ midpoint × frequency)." % desc, hdr, rows, _ds(tot),
                   [" + ".join("%s×%d" % (_ds(mp), x) for mp, x in zip(mids, f)) + " = %s." % _ds(tot)], atype="num")

    def t_bar():
        cats = ["%d–%d" % g for g in groups]
        if f.count(max(f)) > 1:
            return _bar("The bar chart shows grouped %s. How many values are there altogether?" % desc, cats, f, sum(f), ["Add the bars: %d." % sum(f)])
        return _bar("The bar chart shows grouped %s. Type the lower end of the modal class." % desc, cats, f, groups[f.index(max(f))][0],
                    ["The tallest bar is %s." % cats[f.index(max(f))]])

    return _pick_t([t_why_estimate], [t_modal, t_total, t_midpoint, t_est_mean, t_median_class, t_more_than, t_range_max, t_total_est, t_bar])


@skill("Y9.9.c", "Compare distributions", S9)
def _(d=1):
    d = _d(d)
    what, lo, hi = pick([("test scores", 10, 30), ("long-jump distances (in dm)", 25, 45), ("reaction times (in hundredths of a second)", 18, 40)])
    a = [random.randint(lo, hi) for _ in range(6)]
    b = [random.randint(lo, hi) for _ in range(6)]
    rows = lambda: [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]]

    def _med(xs):
        s = sorted(xs)
        return Fraction(s[2] + s[3], 2)

    def t_mean():
        ma, mb = Fraction(sum(a), 6), Fraction(sum(b), 6)
        if ma == mb:
            b[0] += 1
            mb = Fraction(sum(b), 6)
        return _dt("Two groups' %s are shown. Which group has the higher mean? (A or B)" % what, ["Group", "Values"], rows(), "A" if ma > mb else "B",
                   ["A: %.2f. B: %.2f." % (float(ma), float(mb))], atype="str", placeholder="A / B")

    def t_range():
        ra, rb = max(a) - min(a), max(b) - min(b)
        if ra == rb:
            return t_mean()
        return _dt("Two groups' %s are shown. Which group is more consistent (smaller range)? (A or B)" % what, ["Group", "Values"], rows(),
                   "A" if ra < rb else "B", ["Range A = %d, B = %d." % (ra, rb)], atype="str", placeholder="A / B")

    def t_median_diff():
        return _dt("Two groups' %s are shown. What is the difference between the two medians?" % what, ["Group", "Values"], rows(),
                   _ds(abs(_med(a) - _med(b))), ["Median A = %s, B = %s." % (_ds(_med(a)), _ds(_med(b)))], atype="num")

    def t_range_value():
        return _dt("Two groups' %s are shown. What is the range of group B?" % what, ["Group", "Values"], rows(), max(b) - min(b),
                   ["%d − %d = %d." % (max(b), min(b), max(b) - min(b))])

    def t_outlier():
        xs = [random.randint(20, 30) for _ in range(6)] + [random.randint(80, 95)]
        random.shuffle(xs)
        return _wq("Which average is LEAST affected by the outlier in  %s : mean or median?" % ", ".join(map(str, xs)), "median",
                   ["The mean is pulled towards an outlier; the median is not."], "mean / median")

    def t_statement():
        return _wq("To compare two sets of data properly, you should compare an average AND what else? (one word)", "spread",
                   ["Compare an average and a measure of spread (such as the range)."], "one word")

    def t_combined():
        n1, n2 = random.randint(2, 6) * 5, random.randint(2, 6) * 5
        m1, m2 = random.randint(20, 40), random.randint(20, 40)
        tot = n1 * m1 + n2 * m2
        mm = Fraction(tot, n1 + n2)
        if mm.denominator not in (1, 2, 4, 5, 10):
            n2 = n1
            mm = Fraction(n1 * m1 + n2 * m2, n1 + n2)
            tot = n1 * m1 + n2 * m2
        return _tb("Class A has %d pupils with a mean score of %d. Class B has %d pupils with a mean score of %d. What is the mean score of all "
                   "the pupils together?" % (n1, m1, n2, m2), _ds(mm), "num", {},
                   ["Totals: %d × %d = %d and %d × %d = %d." % (n1, m1, n1 * m1, n2, m2, n2 * m2), "%d ÷ %d = %s." % (tot, n1 + n2, _ds(mm))])

    def t_new_mean():
        n, m = random.randint(3, 9), random.randint(5, 20)
        new = m + random.randint(1, 8)
        nm = Fraction(n * m + new, n + 1)
        return _tb("The mean of %d numbers is %d. Another number, %d, is added. What is the new mean? (give a decimal if needed, to 2 d.p.)"
                   % (n, m, new), _ds(nm) if nm.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else round(float(nm) + 1e-12, 2), "num", {},
                   ["Total %d + %d = %d." % (n * m, new, n * m + new), "%d ÷ %d ≈ %.3f." % (n * m + new, n + 1, float(nm))],
                   tol=0 if nm.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100) else 0.0051)

    def t_missing_value():
        n, m = random.randint(3, 6), random.randint(8, 20)
        known = [random.randint(m - 5, m + 5) for _ in range(n - 1)]
        last = n * m - sum(known)
        while last < 1:
            known = [random.randint(m - 5, m) for _ in range(n - 1)]
            last = n * m - sum(known)
        return _tb("The mean of %d numbers is %d. %s of them are %s. What is the last number?" % (n, m, _words(n - 1).capitalize(), ", ".join(map(str, known))),
                   last, "int", {}, ["Total = %d × %d = %d." % (n, m, n * m), "%d − %d = %d." % (n * m, sum(known), last)])

    def t_compare_text():
        m1, m2 = random.randint(50, 70), random.randint(50, 70)
        r1, r2 = random.randint(8, 40), random.randint(8, 40)
        if r1 == r2:
            r2 += 5
        return _wq("Class A: mean %d, range %d. Class B: mean %d, range %d. Which class's results are more consistent? (A or B)" % (m1, r1, m2, r2),
                   "A" if r1 < r2 else "B", ["The smaller range is more consistent."], "A / B")

    return _pick_t([t_outlier, t_statement, t_combined, t_new_mean, t_missing_value, t_compare_text],
                   [t_mean, t_range, t_median_diff, t_range_value])


@skill("Y9.9.d", "Choose and criticise charts", S9)
def _(d=1):
    d = _d(d)

    def t_choose():
        q, a = pick([("You want to show how a temperature changes over a day. Which chart is best: bar chart, line graph or pie chart?", "line graph"),
                     ("You want to show the proportion of a budget spent on each item. Which chart is best: bar chart, line graph or pie chart?",
                      "pie chart"),
                     ("You want to compare the numbers of pupils choosing each sport. Which chart is best: bar chart, line graph or pie chart?",
                      "bar chart"),
                     ("You want to see if height and arm span are related. Which chart is best: scatter graph, pie chart or bar chart?",
                      "scatter graph")])
        return _wq(q, a, ["Match the chart to the question."], "chart name")

    def t_misleading():
        q, a = pick([("A bar chart's vertical axis starts at 50 instead of 0. Does that make differences look bigger or smaller?", "bigger"),
                     ("A pie chart's sectors add up to 110%. Is the chart correct? (yes or no)", "no"),
                     ("A pictogram uses bigger pictures for bigger numbers instead of more pictures. Is that fair? (yes or no)", "no"),
                     ("A line graph's time axis jumps from 2010 to 2020 and then goes up in single years. Is that fair? (yes or no)", "no"),
                     ("A survey of 10 people is used to claim what everyone in the country thinks. Is the sample big enough? (yes or no)", "no")])
        return _wq(q, a, ["Check axes, totals, scales and sample sizes."], "answer")

    def t_pie_angle():
        tot = pick([20, 30, 36, 40, 60, 90])
        k = random.randint(1, tot - 1)
        if (360 * k) % tot:
            k = tot // 4 or 1
        return _tb("In a pie chart of %d people, %d chose swimming. What angle should the swimming sector be?" % (tot, k), 360 * k // tot,
                   "int", {"unit": "°"}, ["%d/%d × 360 = %d." % (k, tot, 360 * k // tot)])

    def t_pie_read():
        slices = [["Walk", pick([90, 120, 60])], ["Bus", 0], ["Car", 0]]
        rest = 360 - slices[0][1]
        slices[1][1] = rest // 2
        slices[2][1] = rest - rest // 2
        tot = pick([24, 36, 60, 120])
        return {"prompt": "The pie chart shows how %d pupils travel. The Walk sector is %d°. How many walk?" % (tot, slices[0][1]),
                "component": "pie_chart", "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": tot * slices[0][1] // 360,
                "answer_type": "int", "solution": ["%d/360 × %d = %d." % (slices[0][1], tot, tot * slices[0][1] // 360)]}

    def t_scatter():
        kind = pick(["positive", "negative", "none"])
        xl, yl = {"positive": ("Hours revised", "Score"), "negative": ("Hours of TV", "Score"), "none": ("Shoe size", "Score")}[kind]
        xs = random.sample(range(1, 15), 8)
        if kind == "none":
            ys = [random.randint(5, 30) for _ in xs]
            r = 1
            while True:
                mx, my = sum(xs) / 8, sum(ys) / 8
                cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
                vx = sum((x - mx) ** 2 for x in xs)
                vy = sum((y - my) ** 2 for y in ys)
                r = cov / ((vx * vy) ** 0.5 or 1)
                if abs(r) < 0.2:
                    break
                ys = [random.randint(5, 30) for _ in xs]
        else:
            ys = [(2 * x if kind == "positive" else 32 - 2 * x) + random.randint(-3, 3) for x in xs]
        return {"prompt": "Describe the correlation shown. Type one word: positive, negative or none.", "component": "scatter_plot",
                "spec": {"points": sorted([[x, y] for x, y in zip(xs, ys)]), "xLabel": xl, "yLabel": yl}, "answer": kind, "answer_type": "str",
                "solution": [{"positive": "As one rises, so does the other.", "negative": "As one rises, the other falls.",
                              "none": "There is no clear pattern."}[kind]]}

    def t_bar_compare():
        cats = ["Football", "Swimming", "Tennis", "Netball"]
        vals = random.sample(range(3, 25), 4)
        i, j = random.sample(range(4), 2)
        return _bar("The bar chart shows the sports pupils chose. How many more chose %s than %s? (Use a minus sign if fewer.)"
                    % (cats[i].lower(), cats[j].lower()), cats, vals, vals[i] - vals[j], ["%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j])])

    def t_pie_fraction():
        a1 = pick([90, 120, 60, 180, 45])
        slices = [["Bus", a1], ["Walk", (360 - a1) // 2], ["Car", 360 - a1 - (360 - a1) // 2]]
        return {"prompt": "In this pie chart the Bus sector is %d°. What fraction of the pupils come by bus? (simplest form)" % a1,
                "component": "pie_chart", "spec": {"slices": slices, "mode": "read", "highlight": 0}, "answer": _fs(Fraction(a1, 360)),
                "answer_type": "frac", "solution": ["%d/360 = %s." % (a1, _fs(Fraction(a1, 360)))]}

    def t_line_change():
        years = ["2019", "2020", "2021", "2022", "2023", "2024"]
        v = [random.randint(20, 60)]
        for _ in years[1:]:
            v.append(v[-1] + random.randint(-8, 12))
        i = random.randint(1, 5)
        return _lg("The line graph shows a club's members each year. By how much did membership change from %s to %s? (Use a minus sign for a fall.)"
                   % (years[i - 1], years[i]), list(zip(years, v)), v[i] - v[i - 1], ["%d − %d = %d." % (v[i], v[i - 1], v[i] - v[i - 1])],
                   "Members", "Year")

    return _pick_t([t_choose, t_misleading, t_pie_angle], [t_pie_read, t_scatter, t_bar_compare, t_pie_fraction, t_line_change])
