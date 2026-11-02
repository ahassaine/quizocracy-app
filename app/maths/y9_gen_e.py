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

    return _pick_t([t_or, t_not, t_algebra, t_exclusive], [t_missing])


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
        n = 600
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

    return _pick_t([t_expected, t_dice, t_relative, t_fair, t_estimate], [t_table])


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

    return _pick_t([], [t_both, t_either, t_given, t_two_way])


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

    return _pick_t([t_coin_dice, t_two_dice, t_double, t_product, t_count, t_at_least])


# ================================================================== 9.9 ======
@skill("Y9.9.a", "Averages and range from a frequency table", S9)
def _(d=1):
    d = _d(d)
    vals = [0, 1, 2, 3, 4]
    f = [random.randint(1, 12) for _ in vals]
    n = sum(f)
    tot = sum(v * x for v, x in zip(vals, f))
    rows = [[v, x] for v, x in zip(vals, f)]

    def t_mean():
        m = Fraction(tot, n)
        if m.denominator not in (1, 2, 4, 5, 10, 20, 25, 50):
            return _dt("The table shows the number of pets owned by some pupils. What is the mean, to 1 decimal place?", ["Pets", "Frequency"],
                       rows, round(float(m) + 1e-12, 1), ["Total %d ÷ %d pupils." % (tot, n)], atype="num")
        return _dt("The table shows the number of pets owned by some pupils. What is the mean number of pets?", ["Pets", "Frequency"], rows,
                   _ds(m), ["Σfx = %d; n = %d; %d ÷ %d = %s." % (tot, n, tot, n, _ds(m))], atype="num")

    def t_mode():
        if f.count(max(f)) > 1:
            return t_total()
        return _dt("What is the mode number of pets?", ["Pets", "Frequency"], rows, vals[f.index(max(f))],
                   ["The highest frequency is %d, for %d pets." % (max(f), vals[f.index(max(f))])])

    def t_total():
        return _dt("How many pupils were surveyed?", ["Pets", "Frequency"], rows, n, ["%s = %d." % (" + ".join(map(str, f)), n)])

    def t_median():
        data = sorted(v for v, x in zip(vals, f) for _ in range(x))
        med = Fraction(data[n // 2]) if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
        return _dt("What is the median number of pets?", ["Pets", "Frequency"], rows, _ds(med),
                   ["There are %d values; the median is the %s value." % (n, "middle" if n % 2 else "mean of the middle two")], atype="num")

    def t_range():
        used = [v for v, x in zip(vals, f) if x]
        return _dt("What is the range of the number of pets?", ["Pets", "Frequency"], rows, max(used) - min(used),
                   ["%d − %d." % (max(used), min(used))])

    return _pick_t([], [t_mean, t_mode, t_total, t_median, t_range])


@skill("Y9.9.b", "Grouped data: modal class and estimated mean", S9)
def _(d=1):
    d = _d(d)
    w = pick([5, 10])
    groups = [(i * w, (i + 1) * w) for i in range(4)]
    f = [random.randint(2, 15) for _ in groups]
    rows = [["%d < t ≤ %d" % g, x] for g, x in zip(groups, f)]

    def t_modal():
        if f.count(max(f)) > 1:
            return t_total()
        g = groups[f.index(max(f))]
        return _dt("The table shows times in minutes. Which is the modal class? Type its lower end.", ["Time (min)", "Frequency"], rows,
                   g[0], ["The modal class is %d < t ≤ %d." % g])

    def t_total():
        return _dt("How many people are in the table?", ["Time (min)", "Frequency"], rows, sum(f), ["%d." % sum(f)])

    def t_midpoint():
        k = random.randrange(4)
        return _dt("What is the midpoint of the class %d < t ≤ %d?" % groups[k], ["Time (min)", "Frequency"], rows,
                   _ds(Fraction(sum(groups[k]), 2)), ["(%d + %d) ÷ 2." % groups[k]], atype="num")

    def t_est_mean():
        mids = [Fraction(a + b, 2) for a, b in groups]
        m = sum(mp * x for mp, x in zip(mids, f)) / sum(f)
        return _dt("Estimate the mean time, to 1 decimal place.", ["Time (min)", "Frequency"], rows, round(float(m) + 1e-12, 1),
                   ["Use midpoints: Σ(midpoint × f) ÷ Σf = %.2f." % float(m)], atype="num")

    def t_median_class():
        n = sum(f)
        pos = (n + 1) / 2
        cum = 0
        for g, x in zip(groups, f):
            cum += x
            if cum >= pos:
                return _dt("Which class contains the median? Type its lower end.", ["Time (min)", "Frequency"], rows, g[0],
                           ["The median is the %s value, in %d < t ≤ %d." % (_ds(Fraction(n + 1, 2)), g[0], g[1])])
        return t_total()

    def t_why_estimate():
        return _wq("Why can the mean of grouped data only be estimated? (one word: we do not know the exact ...)", "values",
                   ["The original values are lost when data is grouped."], "one word")

    return _pick_t([t_why_estimate], [t_modal, t_total, t_midpoint, t_est_mean, t_median_class])


@skill("Y9.9.c", "Compare distributions", S9)
def _(d=1):
    d = _d(d)
    a = [random.randint(10, 30) for _ in range(6)]
    b = [random.randint(10, 30) for _ in range(6)]

    def _med(xs):
        s = sorted(xs)
        return Fraction(s[2] + s[3], 2)

    def t_mean():
        ma, mb = Fraction(sum(a), 6), Fraction(sum(b), 6)
        if ma == mb:
            b[0] += 1
            mb = Fraction(sum(b), 6)
        return _dt("Two classes' test scores are shown. Which class has the higher mean? (A or B)", ["Class", "Scores"],
                   [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]], "A" if ma > mb else "B",
                   ["A: %.2f. B: %.2f." % (float(ma), float(mb))], atype="str")

    def t_range():
        ra, rb = max(a) - min(a), max(b) - min(b)
        if ra == rb:
            return t_mean()
        return _dt("Which class's scores are more consistent (smaller range)? (A or B)", ["Class", "Scores"],
                   [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]], "A" if ra < rb else "B",
                   ["Range A = %d, B = %d." % (ra, rb)], atype="str")

    def t_median_diff():
        return _dt("What is the difference between the two medians?", ["Class", "Scores"],
                   [["A", ", ".join(map(str, a))], ["B", ", ".join(map(str, b))]], _ds(abs(_med(a) - _med(b))),
                   ["Median A = %s, B = %s." % (_ds(_med(a)), _ds(_med(b)))], atype="num")

    def t_outlier():
        xs = [random.randint(20, 30) for _ in range(6)] + [random.randint(80, 95)]
        random.shuffle(xs)
        return _wq("Which average is LEAST affected by the outlier in  %s : mean or median?" % ", ".join(map(str, xs)), "median",
                   ["The mean is pulled towards an outlier; the median is not."], "mean / median")

    def t_statement():
        return _wq("To compare two sets of data properly, you should compare an average AND what else? (one word)", "spread",
                   ["Compare an average and a measure of spread (such as the range)."], "one word")

    return _pick_t([t_outlier, t_statement], [t_mean, t_range, t_median_diff])


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
                     ("A pictogram uses bigger pictures for bigger numbers instead of more pictures. Is that fair? (yes or no)", "no")])
        return _wq(q, a, ["Check axes, totals and scales."], "answer")

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
        pts = sorted([[x, 2 * x + random.randint(-3, 3)] for x in random.sample(range(1, 15), 8)])
        return {"prompt": "Describe the correlation shown: positive, negative or none?", "component": "scatter_plot",
                "spec": {"points": pts, "xLabel": "Hours revised", "yLabel": "Score"}, "answer": "positive", "answer_type": "str",
                "solution": ["Both values rise together."]}

    return _pick_t([t_choose, t_misleading, t_pie_angle], [t_pie_read, t_scatter])
