# dev/app/logic/y3_gen_c.py — Year 3 generators: levels 3.6, 3.7, 3.8, 3.9
#
# Every generator takes a difficulty tier:  d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between 4-6 genuinely different framings (visual model,
# bare calculation, word problem, missing number, comparison, real-life context).
#
# Visual components are used wherever the maths allows:
#   fractions ....... fraction_bar / number_line
#   measurement ..... ruler (length / mass / capacity)
#   time ............ clock
#   geometry ........ shape
#   statistics ...... pictogram / bar_chart
import random
from fractions import Fraction
from .maths_engine import skill, pick, money, roman, NAMES, n_words

S6 = "3.6 Fractions"
S7 = "3.7 Measurement"
S8 = "3.8 Time & geometry"
S9 = "3.9 Statistics & reasoning"


# ---------------------------------------------------------------- helpers ----
def _tier(d):
    """Clamp the difficulty tier to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_tier(d)]


def _pick_t(weights):
    """Choose a framing index. Visual framings carry weight 2, plain typed ones 1,
    so the pupil meets a model or diagram more often than a bare sum."""
    total = float(sum(weights))
    r = random.random() * total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r < acc:
            return i
    return len(weights) - 1


# denominators per tier (used by the fraction skills)
def _dens(d, terminating=False):
    """Denominators for tier d.  terminating=True -> only denominators that give
    exact decimals, so they can be drawn on a number line."""
    if terminating:
        return _by_d(d, [2, 4], [2, 4, 5, 10], [4, 5, 8, 10])
    return _by_d(d, [2, 3, 4], [3, 4, 5, 6, 8, 10], [5, 6, 7, 8, 9, 10, 12])


def _pl(n, word, plural=None):
    """'1 part' / '3 parts'."""
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _a(word):
    """'a square' / 'an octagon'."""
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


_FRAC_WORDS = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth",
               7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth", 12: "twelfth"}


def _frac_words(n, d):
    """1/4 -> 'one quarter';  3/5 -> 'three fifths'."""
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%d/%d" % (n, d)
    if n == 1:
        return "one " + w
    return "%s %ss" % (n_words(n), w)


def _hm(h, m):
    """Normalise to a 12-hour clock string 'H:MM'."""
    h = ((int(h) - 1) % 12) + 1
    return "%d:%02d" % (h, int(m))


def _clock_minutes(d):
    return _by_d(d, [0, 30], [0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55],
                 [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 3, 7, 12, 18, 23, 37, 42, 48])


def _chart(d, n_cats=4):
    """Categories + values for a bar chart / table."""
    cats = random.sample(["Red", "Blue", "Green", "Yellow", "Purple", "Orange"], n_cats)
    lo, hi = _by_d(d, (2, 8), (2, 12), (4, 20))
    vals = [random.randint(lo, hi) for _ in cats]
    # keep all values distinct so "most / least / difference" is unambiguous
    while len(set(vals)) != len(vals):
        vals = [random.randint(lo, hi) for _ in cats]
    return cats, vals


def _tally(n):
    """7 -> '||||\\ ||'  (a bundle of five is four bars and a slash)."""
    n = int(n)
    parts = ["||||\\"] * (n // 5)
    if n % 5:
        parts.append("|" * (n % 5))
    return " ".join(parts) if parts else "(none)"


def _coin_name(p):
    """Pence value -> UK coin / note name."""
    return {100: "£1 coin", 200: "£2 coin", 500: "£5 note",
            1000: "£10 note", 2000: "£20 note"}.get(int(p), "%dp coin" % int(p))


def _coin_list(items):
    """[(count, value), ...] -> '3 20p coins and 1 £1 coin'."""
    bits = []
    for c, v in items:
        nm = _coin_name(v)
        bits.append("%d %s" % (c, nm if c == 1 else nm + "s"))
    if len(bits) == 1:
        return bits[0]
    return ", ".join(bits[:-1]) + " and " + bits[-1]


def _plot_rows(labels, counts, mark="x"):
    """Text line plot: '0 pets: x x x'."""
    return "; ".join("%s: %s" % (lab, " ".join([mark] * c) if c else "(none)")
                     for lab, c in zip(labels, counts))


def _num_q(prompt, answer, answer_type="int", unit=None, text=False,
           placeholder=None, solution=None):
    spec = {}
    if unit:
        spec["unit"] = unit
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "solution": solution or []}


# ------------------------------------------------------------------ 3.6 ------
@skill("Y3.6.a", "Show a fraction of a whole", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_dens(d))
    n = 1 if d == 0 else random.randint(1, den - 1)
    t = _pick_t([2, 2, 2, 2, 1, 1, 2, 2])

    if t == 0:                                          # visual model
        return {"prompt": "Shade %d/%d of the bar." % (n, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (n, den), "answer_type": "frac",
                "solution": ["Split the bar into %d equal parts." % den,
                             "Shade %d of them: %d/%d." % (n, n, den)]}

    if t == 1:                                          # real-life context, visual
        food = pick(["chocolate bar", "loaf of bread", "ribbon", "cake"])
        return {"prompt": "A %s is cut into %d equal pieces. Shade %s of it."
                          % (food, den, _frac_words(n, den)),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (n, den), "answer_type": "frac",
                "solution": ["%s means %d out of %d equal parts." % (_frac_words(n, den).capitalize(), n, den),
                             "Shade %s." % _pl(n, "part")]}

    if t == 2:                                          # shade the part that is LEFT
        eaten = random.randint(1, den - 1)
        left = den - eaten
        return {"prompt": "A pizza is cut into %d equal slices and %d %s eaten. "
                          "Shade the fraction that is left."
                          % (den, eaten, "is" if eaten == 1 else "are"),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (left, den), "answer_type": "frac",
                "solution": ["%d − %d = %s left." % (den, eaten, _pl(left, "slice")),
                             "That is %d/%d." % (left, den)]}

    if t == 3:                                          # equivalent shading (stretch)
        base = pick([(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)]) if d else (1, 2)
        bn, bd = base
        k = 2 if d < 2 else pick([2, 3])
        parts = bd * k
        if parts > 12:
            parts, k = bd * 2, 2
        shaded = int(Fraction(bn, bd) * parts)     # exact: bd divides parts
        return {"prompt": "The bar has %d equal parts. Shade %s of the bar."
                          % (parts, _frac_words(bn, bd)),
                "component": "fraction_bar", "spec": {"parts": parts, "mode": "shade"},
                "answer": "%d/%d" % (shaded, parts), "answer_type": "frac",
                "solution": ["%d/%d of %d parts is %s." % (bn, bd, parts, _pl(shaded, "part")),
                             "Shade %d of the %d parts." % (shaded, parts)]}

    if t == 4:                                          # bare notation -> typed
        return _num_q("A shape is split into %d equal parts. %d %s shaded. "
                      "Write the fraction that is shaded."
                      % (den, n, "part is" if n == 1 else "parts are"),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["%d shaded out of %d equal parts." % (n, den),
                                "The fraction is %d/%d." % (n, den)])

    if t == 6:                    # NEW: show fractions with an area model (grid)
        parts = pick([4, 6, 8, 9, 10, 12])
        k = random.randint(1, parts - 1)
        return {"prompt": "This area model shows one whole split into %d equal parts. "
                          "Show the fraction %d/%d by shading the area model."
                          % (parts, k, parts),
                "component": "area_grid", "spec": {"mode": "fraction", "parts": parts},
                "answer": "%d/%d" % (k, parts), "answer_type": "frac",
                "solution": ["The area model has %d equal parts." % parts,
                             "Shade %s to show %d/%d." % (_pl(k, "part"), k, parts)]}

    if t == 7:                    # NEW: understand fractions with an area model
        parts = pick([4, 6, 8, 9, 10, 12])
        k = random.randint(1, parts - 1)
        return {"prompt": "Understand the area model: it is one whole split into %d equal "
                          "parts with %s shaded. Write the fraction of the area model "
                          "that is shaded." % (parts, _pl(k, "part")),
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": parts, "shaded": k},
                "answer": "%d/%d" % (k, parts), "answer_type": "frac",
                "solution": ["%s are shaded out of %d equal parts." % (_pl(k, "part"), parts),
                             "The fraction shaded is %d/%d." % (k, parts)]}

    # missing number: how many parts of a bigger bar
    mult = 2 if den * 2 <= 12 else 1
    parts = den * mult
    return _num_q("A bar is split into %d equal parts. %s of the bar is shaded. "
                  "How many parts are shaded?" % (parts, _frac_words(n, den).capitalize()),
                  n * mult, "int", unit="parts",
                  solution=["%d parts ÷ %d = %s in each %s."
                            % (parts, den, _pl(mult, "part"), _FRAC_WORDS.get(den, "part")),
                            "%d × %d = %s shaded." % (mult, n, _pl(n * mult, "part"))])


@skill("Y3.6.b", "Write the fraction shown", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_dens(d))
    n = random.randint(1, den - 1)
    t = _pick_t([1, 1, 2, 1, 2, 2, 2])

    if t == 0:
        return _num_q("A shape is split into %d equal parts and %d are shaded. "
                      "Write the fraction shaded." % (den, n),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["%d shaded out of %d equal parts = %d/%d." % (n, den, n, den)])

    if t == 1:                                          # word problem
        who = pick(NAMES)
        return _num_q("%s cuts a cake into %d equal slices and eats %d of them. "
                      "What fraction of the cake did %s eat?" % (who, den, n, who),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["%s eaten out of %d equal slices." % (_pl(n, "slice"), den),
                                "The fraction is %d/%d." % (n, den)])

    if t == 2:                                          # visual: shade it
        return {"prompt": "Shade the bar to show the fraction with numerator %d "
                          "and denominator %d." % (n, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (n, den), "answer_type": "frac",
                "solution": ["The denominator %d is the number of equal parts." % den,
                             "The numerator %d is how many to shade." % n]}

    if t == 3:                                          # NOT shaded
        return _num_q("A strip has %d equal parts. %d %s NOT shaded. "
                      "Write the fraction that IS shaded."
                      % (den, den - n, "part is" if den - n == 1 else "parts are"),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["%d − %d = %s, so that many are shaded." % (den, den - n, _pl(n, "part")),
                                "That is %d/%d." % (n, den)])

    if t == 5:                    # NEW: match the fraction to the fraction-bar model
        return {"prompt": "Match the fraction %s to a model. The fraction bar below has "
                          "%d equal parts — shade it so that it matches %d/%d."
                          % (_frac_words(n, den), den, n, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (n, den), "answer_type": "frac",
                "solution": ["The model must show %s out of %d equal parts."
                             % (_pl(n, "part"), den),
                             "The matching model is %d/%d." % (n, den)]}

    if t == 6:                    # NEW: understand fractions from an area model
        parts = pick([4, 6, 8, 9, 10, 12])
        k = random.randint(1, parts - 1)
        return {"prompt": "Match this area model to a fraction. Write the fraction that "
                          "the shaded part of the model shows.",
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": parts, "shaded": k},
                "answer": "%d/%d" % (k, parts), "answer_type": "frac",
                "solution": ["The model has %d equal parts and %s shaded."
                             % (parts, _pl(k, "part")),
                             "It matches the fraction %d/%d." % (k, parts)]}

    # visual, real-life: shade what is left
    left = den - n
    return {"prompt": "A chocolate bar has %d equal squares. %s eats %d. "
                      "Shade the bar to show the fraction left."
                      % (den, pick(NAMES), n),
            "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
            "answer": "%d/%d" % (left, den), "answer_type": "frac",
            "solution": ["%d − %d = %s left." % (den, n, _pl(left, "square")),
                         "That is %d/%d." % (left, den)]}


@skill("Y3.6.c", "Find a fraction of a quantity", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_by_d(d, [2, 4], [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 10]))
    per = random.randint(2, _by_d(d, 5, 9, 12))
    total = den * per
    n = 1 if d == 0 else random.randint(1, den - 1)
    t = _pick_t([1, 1, 2, 1, 2, 1])

    if t == 0:                                          # bare calculation
        return _num_q("What is %d/%d of %d?" % (n, den, total), per * n, "int",
                      solution=["%d ÷ %d = %d (one part)." % (total, den, per),
                                "%d × %d = %d." % (per, n, per * n)])

    if t == 1:                                          # word problem
        who = pick(NAMES)
        thing = pick(["sweets", "marbles", "stickers", "grapes", "pencils"])
        return _num_q("%s has %d %s and gives away %s of them. How many did %s give away?"
                      % (who, total, thing, _frac_words(n, den), who),
                      per * n, "int", unit=thing,
                      solution=["%d ÷ %d = %d." % (total, den, per),
                                "%d × %d = %d %s." % (per, n, per * n, thing)])

    if t == 2:                                          # visual: build the answer
        return {"prompt": "Work out %d/%d of %d. Build your answer with the blocks."
                          % (n, den, total),
                "component": "base_ten", "spec": {"mode": "build", "max": 9},
                "answer": per * n, "answer_type": "int",
                "solution": ["%d ÷ %d = %d (one part)." % (total, den, per),
                             "%s = %d." % (_pl(n, "part"), per * n)]}

    if t == 3:                                          # missing number
        return _num_q("%s of a number is %d. What is the number?"
                      % (_frac_words(1, den).capitalize(), per),
                      total, "int",
                      solution=["One part is %d and there are %d parts." % (per, den),
                                "%d × %d = %d." % (per, den, total)])

    if t == 4:                                          # visual model
        return {"prompt": "Shade %s of this bar. Then use the bar to work out %s of %d in your head."
                          % (_frac_words(n, den), _frac_words(n, den), total),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (n, den), "answer_type": "frac",
                "solution": ["Shade %d of the %d equal parts." % (n, den),
                             "Each part of %d is %d, so %d/%d of %d = %d."
                             % (total, per, n, den, total, per * n)]}

    # comparison / two-step
    den2 = pick([2, 4, 5])
    per2 = random.randint(2, 9)
    while per2 == per * n:
        per2 = random.randint(2, 9)
    total2 = den2 * per2
    return _num_q("Which is more: %s of %d, or %s of %d? Write the larger amount."
                  % (_frac_words(n, den), total, _frac_words(1, den2), total2),
                  max(per * n, per2), "int",
                  solution=["%s of %d = %d." % (_frac_words(n, den), total, per * n),
                            "%s of %d = %d, so the larger is %d."
                            % (_frac_words(1, den2), total2, per2, max(per * n, per2))])


@skill("Y3.6.d", "Fractions on a number line", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 2, 2, 1])

    if t in (0, 1):                                     # place it on a number line
        den = pick(_dens(d, terminating=True))
        n = random.randint(1, den - 1)
        step = 1.0 / den
        return {"prompt": "Place %d/%d on the number line." % (n, den),
                "component": "number_line",
                "spec": {"min": 0, "max": 1, "step": step, "major": step},
                "answer": round(n / float(den), 6), "answer_type": "num",
                "tolerance": step / 2.0,
                "solution": ["The line from 0 to 1 is split into %d equal steps." % den,
                             "Count %s from 0." % _pl(n, "step")]}

    if t == 2:                                          # tenths beyond 1
        n = random.randint(1, _by_d(d, 9, 10, 19))
        return {"prompt": "Place %d/10 on the number line." % n,
                "component": "number_line",
                "spec": {"min": 0, "max": 2, "step": 0.1, "major": 0.5},
                "answer": round(n / 10.0, 6), "answer_type": "num",
                "tolerance": 0.05,
                "solution": ["Each small step is 1/10.", "Count %s from 0." % _pl(n, "step")]}

    if t == 3:                                          # typed: which fraction is at a mark
        den = pick(_dens(d))
        n = random.randint(1, den - 1)
        return _num_q("A number line from 0 to 1 is split into %d equal parts. "
                      "What fraction is at the %s mark after 0?" % (den, _ord(n)),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["Each part is 1/%d." % den,
                                "The %s mark after 0 is %d/%d." % (_ord(n), n, den)])

    if t == 5:                    # NEW: graph the smaller / larger fraction
        den = pick(_dens(d, terminating=True))
        while den < 3:
            den = pick([4, 5, 10])
        a, b = random.sample(range(1, den), 2)
        want_larger = random.random() < 0.5
        k = max(a, b) if want_larger else min(a, b)
        step = 1.0 / den
        return {"prompt": "Which fraction is %s, %d/%d or %d/%d? Graph the %s fraction "
                          "on the number line."
                          % ("larger" if want_larger else "smaller", a, den, b, den,
                             "larger" if want_larger else "smaller"),
                "component": "number_line",
                "spec": {"min": 0, "max": 1, "step": step, "major": step},
                "answer": round(k / float(den), 6), "answer_type": "num",
                "tolerance": step / 2.0,
                "solution": ["The denominators match, so compare the numerators.",
                             "The %s fraction is %d/%d — count %s from 0."
                             % ("larger" if want_larger else "smaller", k, den, _pl(k, "step"))]}

    if t == 6:                    # NEW: identify the fraction at a point on the line
        den = pick(_dens(d))
        n = random.randint(1, den - 1)
        return _num_q("Identify the fraction on a number line: the line from 0 to 1 is "
                      "divided into %d equal steps and a point is marked %s from 0. "
                      "Which fraction is at that point?" % (den, _pl(n, "step")),
                      "%d/%d" % (n, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["Each step on the number line is 1/%d." % den,
                                "%s from 0 is %d/%d." % (_pl(n, "step").capitalize(), n, den)])

    # equivalent fraction on a marked line
    den = pick(_by_d(d, [4], [4, 10], [8, 10]))
    base = pick([(1, 2), (1, 4), (3, 4)] if den == 4 else [(1, 2), (1, 5), (2, 5)])
    if den == 8:
        base = pick([(1, 2), (1, 4), (3, 4)])
    bn, bd = base
    step = 1.0 / den
    return {"prompt": "The line from 0 to 1 is split into %d equal steps. "
                      "Place %s on it." % (den, _frac_words(bn, bd)),
            "component": "number_line",
            "spec": {"min": 0, "max": 1, "step": step, "major": step},
            "answer": round(bn / float(bd), 6), "answer_type": "num",
            "tolerance": step / 2.0,
            "solution": ["%s = %d/%d." % (_frac_words(bn, bd).capitalize(),
                                          bn * den // bd, den),
                         "Count %s from 0." % _pl(bn * den // bd, "step")]}


@skill("Y3.6.e", "Count in tenths", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 2, 1, 1, 2, 2])

    if t == 0:                                          # count on
        n = random.randint(1, _by_d(d, 5, 8, 8))
        return _num_q("Count on in tenths: %d/10, ___ . Write the next fraction." % n,
                      "%d/10" % (n + 1), "frac", text=True, placeholder="e.g. 4/10",
                      solution=["One tenth more than %d/10 is %d/10." % (n, n + 1)])

    if t == 1:                                          # count back
        n = random.randint(2, 9)
        return _num_q("Count back in tenths: %d/10, ___ . Write the next fraction." % n,
                      "%d/10" % (n - 1), "frac", text=True, placeholder="e.g. 4/10",
                      solution=["One tenth less than %d/10 is %d/10." % (n, n - 1)])

    if t == 2:                                          # number line (visual)
        n = random.randint(1, _by_d(d, 9, 10, 19))
        return {"prompt": "Count in tenths and place %d/10 on the number line." % n,
                "component": "number_line",
                "spec": {"min": 0, "max": 2, "step": 0.1, "major": 0.5},
                "answer": round(n / 10.0, 6), "answer_type": "num",
                "tolerance": 0.05,
                "solution": ["Each step on the line is one tenth.",
                             "Count %s from 0." % _pl(n, "tenth")]}

    if t == 3:                                          # step of 2 or 3 tenths
        stepn = _by_d(d, 2, 2, 3)
        start = random.randint(1, max(1, 10 - 3 * stepn))
        seq = [start + i * stepn for i in range(3)]
        return _num_q("What comes next? %s, ___"
                      % ", ".join("%d/10" % v for v in seq),
                      "%d/10" % (seq[-1] + stepn), "frac", text=True, placeholder="e.g. 7/10",
                      solution=["The count goes up by %s each time." % _pl(stepn, "tenth"),
                                "%d/10 + %d/10 = %d/10." % (seq[-1], stepn, seq[-1] + stepn)])

    if t == 4:                                          # tenths to make a whole
        n = random.randint(1, 9)
        return _num_q("How many more tenths are needed to make %d/10 up to 1 whole?" % n,
                      10 - n, "int", unit="tenths",
                      solution=["1 whole = 10/10.", "10 − %d = %s." % (n, _pl(10 - n, "tenth"))])

    if t == 6:                    # NEW: graph decimals and fractions in tenths
        n = random.randint(1, _by_d(d, 9, 15, 19))
        as_dec = random.random() < 0.5
        label = ("the decimal %s" % ("%.1f" % (n / 10.0))) if as_dec \
                else ("the fraction %d/10" % n)
        return {"prompt": "Graph %s on the number line marked in tenths "
                          "(%d/10 = %s)." % (label, n, "%.1f" % (n / 10.0)),
                "component": "number_line",
                "spec": {"min": 0, "max": 2, "step": 0.1, "major": 0.5},
                "answer": round(n / 10.0, 6), "answer_type": "num",
                "tolerance": 0.05,
                "solution": ["Each step is one tenth, or 0.1.",
                             "%s is %s, so count %s from 0."
                             % (_pl(n, "tenth"), "%.1f" % (n / 10.0), _pl(n, "step"))]}

    # visual: shade tenths
    n = random.randint(1, 9)
    return {"prompt": "The bar is one whole split into tenths. Shade %s." % _pl(n, "tenth"),
            "component": "fraction_bar", "spec": {"parts": 10, "mode": "shade"},
            "answer": "%d/10" % n, "answer_type": "frac",
            "solution": ["Shade %d of the 10 equal parts: %d/10." % (n, n)]}


@skill("Y3.6.f", "Equivalent fractions", S6)
def _(d=1):
    d = _tier(d)
    base = pick(_by_d(d, [(1, 2), (1, 4)],
                      [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (2, 5)],
                      [(1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (5, 6)]))
    n, den = base
    k = _by_d(d, 2, random.randint(2, 4), random.randint(2, 5))
    while den * k > 12 and k > 2:          # Y3: small denominators, and every one has a word
        k -= 1
    t = _pick_t([1, 1, 2, 1, 2, 1, 2])

    if t == 0:                                          # missing numerator
        return _num_q("Complete the equivalent fraction: %d/%d = ___/%d"
                      % (n, den, den * k), n * k, "int",
                      solution=["Multiply top and bottom by %d." % k,
                                "%d/%d = %d/%d." % (n, den, n * k, den * k)])

    if t == 1:                                          # missing denominator
        return _num_q("Complete the equivalent fraction: %d/%d = %d/___"
                      % (n, den, n * k), den * k, "int",
                      solution=["%d × %d = %d, so the top was multiplied by %d." % (n, k, n * k, k),
                                "Do the same to the bottom: %d × %d = %d." % (den, k, den * k)])

    if t == 2:                                          # visual model
        parts = den * k
        if parts > 12:
            k = max(2, 12 // den)
            parts = den * k
        return {"prompt": "This bar has %d equal parts. Shade it to show %d/%d."
                          % (parts, n, den),
                "component": "fraction_bar", "spec": {"parts": parts, "mode": "shade"},
                "answer": "%d/%d" % (n * k, parts), "answer_type": "frac",
                "solution": ["%d/%d = %d/%d." % (n, den, n * k, parts),
                             "Shade %d of the %d parts." % (n * k, parts)]}

    if t == 3:                                          # 'how many ___ths'
        word = _FRAC_WORDS.get(den * k, "%dth" % (den * k)) + "s"
        return _num_q("How many %s are the same as %s?" % (word, _frac_words(n, den)),
                      n * k, "int", unit=word,
                      solution=["%d/%d = %d/%d." % (n, den, n * k, den * k),
                                "So the answer is %d." % (n * k)])

    if t == 4:                                          # equivalence on a number line
        line_den = pick([4, 8, 10])
        eq = pick([(1, 2), (1, 4), (3, 4)] if line_den in (4, 8) else [(1, 2), (1, 5), (2, 5)])
        en, ed = eq
        step = 1.0 / line_den
        return {"prompt": "The line from 0 to 1 is split into %d equal steps. "
                          "Mark %s on the line."
                          % (line_den, _frac_words(en, ed)),
                "component": "number_line",
                "spec": {"min": 0, "max": 1, "step": step, "major": step},
                "answer": round(en / float(ed), 6), "answer_type": "num",
                "tolerance": step / 2.0,
                "solution": ["%d/%d = %d/%d." % (en, ed, en * line_den // ed, line_den),
                             "Count %s from 0." % _pl(en * line_den // ed, "step")]}

    if t == 6:                    # NEW: equivalent fractions using one area model
        options = [m for m in (2, 3, 4) if den * m <= 12]
        kk = pick(options) if options else 2
        parts = den * kk
        return {"prompt": "Find the fraction equivalent to %d/%d using this one area "
                          "model. The area model has %d equal parts — shade the "
                          "equivalent fraction." % (n, den, parts),
                "component": "area_grid", "spec": {"mode": "fraction", "parts": parts},
                "answer": "%d/%d" % (n * kk, parts), "answer_type": "frac",
                "solution": ["%d/%d and %d/%d cover the same amount of the model."
                             % (n, den, n * kk, parts),
                             "Shade %d of the %d equal parts." % (n * kk, parts)]}

    # real-life context
    who = pick(NAMES)
    return _num_q("%s cuts a cake into %d equal slices and takes %s of the cake. "
                  "How many slices did %s take?" % (who, den * k, _frac_words(n, den), who),
                  n * k, "int", unit="slices",
                  solution=["%d slices ÷ %d = %d slices in one %s."
                            % (den * k, den, k, _FRAC_WORDS.get(den, "part")),
                            "%d × %d = %d slices." % (k, n, n * k)])


@skill("Y3.6.g", "Compare unit fractions", S6)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [2, 3, 4], [2, 3, 4, 5, 6, 8, 10], [3, 5, 6, 7, 8, 9, 10, 12])
    a, b = random.sample(pool, 2)
    bigger = min(a, b)          # bigger denominator = smaller piece
    smaller = max(a, b)
    t = _pick_t([1, 2, 1, 1, 2])

    if t == 0:                                          # bare comparison
        return _num_q("Which is larger: 1/%d or 1/%d? (write the fraction)" % (a, b),
                      "1/%d" % bigger, "frac", text=True, placeholder="e.g. 1/3",
                      solution=["The more equal parts you split into, the smaller each part is.",
                                "1/%d is larger than 1/%d." % (bigger, smaller)])

    if t == 1:                                          # visual model
        return {"prompt": "Shade the larger of 1/%d and 1/%d on this bar." % (a, b),
                "component": "fraction_bar", "spec": {"parts": bigger, "mode": "shade"},
                "answer": "1/%d" % bigger, "answer_type": "frac",
                "solution": ["Fewer parts means each part is bigger.",
                             "1/%d is the larger fraction." % bigger]}

    if t == 2:                                          # real-life context
        who = pick(NAMES)
        return _num_q("%s can have %s of a pizza or %s of the same pizza. "
                      "Which is more pizza? (write the fraction)"
                      % (who, _frac_words(1, a), _frac_words(1, b)),
                      "1/%d" % bigger, "frac", text=True, placeholder="e.g. 1/3",
                      solution=["Splitting into %d parts gives bigger pieces than %d parts."
                                % (bigger, smaller),
                                "So 1/%d is more." % bigger])

    if t == 3:                                          # missing number / reasoning
        return _num_q("A cake is shared equally. Which number of children gives each child "
                      "the SMALLER slice: %d children or %d children?" % (a, b),
                      smaller, "int", unit="children",
                      solution=["More children means smaller slices.",
                                "%d children gives the smaller slice." % smaller])

    # number line (visual)
    term = [x for x in (a, b) if x in (2, 4, 5, 8, 10)]
    den = min(term) if term else bigger
    if den not in (2, 4, 5, 8, 10):
        den = 4
    step = 1.0 / den
    return {"prompt": "Place 1/%d on the number line." % den,
            "component": "number_line",
            "spec": {"min": 0, "max": 1, "step": step, "major": step},
            "answer": round(1.0 / den, 6), "answer_type": "num",
            "tolerance": step / 2.0,
            "solution": ["The line is split into %d equal steps." % den,
                         "1/%d is the first step from 0." % den]}


@skill("Y3.6.h", "Compare fractions with the same denominator", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_by_d(d, [4, 5], [4, 5, 6, 8, 10], [6, 7, 8, 9, 10, 12]))
    a, b = random.sample(range(1, den), 2)
    hi, lo = max(a, b), min(a, b)
    t = _pick_t([1, 1, 2, 1, 2, 1])

    if t == 0:
        return _num_q("Which is larger: %d/%d or %d/%d? (write the fraction)" % (a, den, b, den),
                      "%d/%d" % (hi, den), "frac", text=True, placeholder="e.g. 3/5",
                      solution=["Same denominator, so compare the numerators.",
                                "%d > %d, so %d/%d is larger." % (hi, lo, hi, den)])

    if t == 1:
        return _num_q("Which is smaller: %d/%d or %d/%d? (write the fraction)" % (a, den, b, den),
                      "%d/%d" % (lo, den), "frac", text=True, placeholder="e.g. 2/5",
                      solution=["Same denominator, so compare the numerators.",
                                "%d < %d, so %d/%d is smaller." % (lo, hi, lo, den)])

    if t == 2:                                          # visual model
        return {"prompt": "Shade the larger of %d/%d and %d/%d on the bar." % (a, den, b, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (hi, den), "answer_type": "frac",
                "solution": ["Same denominator: more parts shaded means a larger fraction.",
                             "Shade %d of the %d parts." % (hi, den)]}

    if t == 3:                                          # real-life context
        p, q = pick(NAMES), None
        while q is None or q == p:
            q = pick(NAMES)
        return _num_q("%s ate %d/%d of a pie and %s ate %d/%d of an identical pie. "
                      "Who ate more? (type the name)" % (p, a, den, q, b, den),
                      p if a > b else q, "str", text=True, placeholder="a name",
                      solution=["The pies are the same size and are cut into %d equal parts." % den,
                                "%d/%d > %d/%d, so %s ate more."
                                % (hi, den, lo, den, p if a > b else q)])

    if t == 4:                                          # visual: shade the smaller
        return {"prompt": "Shade the SMALLER of %d/%d and %d/%d on the bar."
                          % (a, den, b, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (lo, den), "answer_type": "frac",
                "solution": ["Same denominator: fewer parts shaded means a smaller fraction.",
                             "Shade %d of the %d parts." % (lo, den)]}

    # ordering: how many more parts
    return _num_q("%d/%d and %d/%d are shaded on two identical bars. "
                  "How many MORE parts are shaded on the larger one?" % (a, den, b, den),
                  hi - lo, "int", unit="parts",
                  solution=["%d − %d = %s." % (hi, lo, _pl(hi - lo, "part"))])


@skill("Y3.6.i", "Add fractions with the same denominator", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_by_d(d, [4, 5], [4, 5, 6, 8, 10], [6, 7, 8, 9, 10, 12]))
    a = random.randint(1, den - 2)
    b = random.randint(1, den - a - 1)
    t = _pick_t([1, 2, 1, 1, 2, 1])

    if t == 0:                                          # bare calculation
        return _num_q("Work out %d/%d + %d/%d." % (a, den, b, den),
                      "%d/%d" % (a + b, den), "frac", text=True, placeholder="e.g. 3/5",
                      solution=["Add the numerators and keep the denominator.",
                                "%d + %d = %d, so the answer is %d/%d." % (a, b, a + b, a + b, den)])

    if t == 1:                                          # visual model
        return {"prompt": "Shade the bar to show %d/%d + %d/%d." % (a, den, b, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (a + b, den), "answer_type": "frac",
                "solution": ["Shade %s, then %d more." % (_pl(a, "part"), b),
                             "%d + %d = %d parts shaded: %d/%d." % (a, b, a + b, a + b, den)]}

    if t == 2:                                          # word problem
        who = pick(NAMES)
        return _num_q("%s drinks %d/%d of a bottle of juice in the morning and %d/%d "
                      "in the afternoon. What fraction of the bottle has %s drunk?"
                      % (who, a, den, b, den, who),
                      "%d/%d" % (a + b, den), "frac", text=True, placeholder="e.g. 3/5",
                      solution=["%d/%d + %d/%d = %d/%d." % (a, den, b, den, a + b, den)])

    if t == 3:                                          # missing number
        return _num_q("Complete: %d/%d + ___/%d = %d/%d" % (a, den, den, a + b, den),
                      b, "int",
                      solution=["%d − %d = %d." % (a + b, a, b),
                                "So the missing numerator is %d." % b])

    if t == 4:                                          # visual: complete the whole
        return {"prompt": "Imagine %d/%d of this bar is already coloured. "
                          "Shade the fraction you must ADD to make 1 whole." % (a, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (den - a, den), "answer_type": "frac",
                "solution": ["1 whole = %d/%d." % (den, den),
                             "%d − %d = %d parts, so shade %d/%d."
                             % (den, a, den - a, den - a, den)]}

    # make one whole
    return _num_q("What must be added to %d/%d to make 1 whole? (write the fraction)"
                  % (a, den),
                  "%d/%d" % (den - a, den), "frac", text=True, placeholder="e.g. 2/5",
                  solution=["1 whole = %d/%d." % (den, den),
                            "%d/%d − %d/%d = %d/%d." % (den, den, a, den, den - a, den)])


@skill("Y3.6.j", "Subtract fractions with the same denominator", S6)
def _(d=1):
    d = _tier(d)
    den = pick(_by_d(d, [4, 5], [4, 5, 6, 8, 10], [6, 7, 8, 9, 10, 12]))
    a = random.randint(2, den - 1)
    b = random.randint(1, a - 1)
    t = _pick_t([1, 2, 1, 1, 2, 1])

    if t == 0:                                          # bare calculation
        return _num_q("Work out %d/%d − %d/%d." % (a, den, b, den),
                      "%d/%d" % (a - b, den), "frac", text=True, placeholder="e.g. 2/5",
                      solution=["Subtract the numerators and keep the denominator.",
                                "%d − %d = %d, so the answer is %d/%d." % (a, b, a - b, a - b, den)])

    if t == 1:                                          # visual model
        return {"prompt": "A bar had %d/%d shaded. %d/%d is rubbed out. "
                          "Shade what is left." % (a, den, b, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (a - b, den), "answer_type": "frac",
                "solution": ["%d − %d = %s left." % (a, b, _pl(a - b, "part")),
                             "That is %d/%d." % (a - b, den)]}

    if t == 2:                                          # word problem
        who = pick(NAMES)
        return _num_q("%s had %d/%d of a cake and gave %d/%d of the cake away. "
                      "What fraction is left?" % (who, a, den, b, den),
                      "%d/%d" % (a - b, den), "frac", text=True, placeholder="e.g. 2/5",
                      solution=["%d/%d − %d/%d = %d/%d." % (a, den, b, den, a - b, den)])

    if t == 3:                                          # missing number
        return _num_q("Complete: %d/%d − ___/%d = %d/%d" % (a, den, den, a - b, den),
                      b, "int",
                      solution=["%d − %d = %d." % (a, a - b, b),
                                "So the missing numerator is %d." % b])

    if t == 4:                                          # visual: subtract from a whole
        return {"prompt": "The whole bar was shaded, then %d/%d was rubbed out. "
                          "Shade what is left." % (b, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (den - b, den), "answer_type": "frac",
                "solution": ["1 whole = %d/%d." % (den, den),
                             "%d − %d = %d parts left: %d/%d."
                             % (den, b, den - b, den - b, den)]}

    # subtract from a whole
    return _num_q("Work out 1 − %d/%d. (write the fraction)" % (b, den),
                  "%d/%d" % (den - b, den), "frac", text=True, placeholder="e.g. 2/5",
                  solution=["1 whole = %d/%d." % (den, den),
                            "%d/%d − %d/%d = %d/%d." % (den, den, b, den, den - b, den)])


# ------------------------------------------------------------------ 3.7 ------
def _ruler_len(d):
    """A sensible (value, max, unit) reading for a length ruler."""
    if d == 0:
        return random.randint(1, 10), 10, "cm"
    if d == 1:
        return random.randint(1, 20), 20, "cm"
    return random.choice([random.randint(1, 30), random.randint(1, 30)]), 30, "cm"


_UNIT_LENGTH = [
    ("the length of a pencil", "centimetres"),
    ("the width of a classroom", "metres"),
    ("the thickness of a coin", "millimetres"),
    ("the height of a door", "metres"),
    ("the length of an ant", "millimetres"),
    ("the length of a shoe", "centimetres"),
    ("the height of a tree", "metres"),
    ("the thickness of a fingernail", "millimetres"),
]

_UNIT_MASS = [
    ("a bag of sugar", "kilograms"),
    ("a paperclip", "grams"),
    ("a child", "kilograms"),
    ("a strawberry", "grams"),
    ("a car", "kilograms"),
    ("a letter in an envelope", "grams"),
]

_UNIT_VOLUME = [
    ("a spoonful of medicine", "millilitres"),
    ("a bucket of water", "litres"),
    ("a mug of tea", "millilitres"),
    ("a bath full of water", "litres"),
    ("a drop of rain", "millilitres"),
    ("a watering can", "litres"),
]


@skill("Y3.7.a", "Compare lengths (m, cm, mm)", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 1, 1, 2, 2, 1, 1])

    if t == 0:                                          # ruler reading
        v, mx, unit = _ruler_len(d)
        return {"prompt": "Read the ruler. How long is the pencil, in %s?" % unit,
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": unit},
                "answer": v, "answer_type": "int",
                "solution": ["The end of the pencil lines up with %d %s." % (v, unit)]}

    if t == 1:                                          # ruler in mm
        mx = _by_d(d, 100, 150, 200)
        v = random.randrange(10, mx + 1, 10)
        return {"prompt": "Read the ruler. How long is the line, in mm?",
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "mm"},
                "answer": v, "answer_type": "int",
                "solution": ["Each small mark is 1 mm.", "The line reaches %d mm." % v]}

    if t == 2:                                          # m + cm -> cm
        m = random.randint(1, _by_d(d, 2, 4, 9))
        cm = random.randint(10, 90)
        return _num_q("How many centimetres are there in %d m %d cm?" % (m, cm),
                      m * 100 + cm, "int", unit="cm",
                      solution=["1 m = 100 cm, so %d m = %d cm." % (m, m * 100),
                                "%d + %d = %d cm." % (m * 100, cm, m * 100 + cm)])

    if t == 3:                                          # comparison
        a_cm = random.randint(120, 480)
        b_m = random.randint(1, 4)
        b_cm = b_m * 100
        if a_cm == b_cm:
            a_cm += 5
        return _num_q("Which is longer: %d cm or %d m? Write the longer length in cm."
                      % (a_cm, b_m),
                      max(a_cm, b_cm), "int", unit="cm",
                      solution=["%d m = %d cm." % (b_m, b_cm),
                                "The longer length is %d cm." % max(a_cm, b_cm)])

    if t == 5:                    # NEW: measure using a centimetre ruler
        v, mx, unit = _ruler_len(d)
        thing = pick(["crayon", "leaf", "straw", "paintbrush", "twig"])
        return {"prompt": "Measure the %s using the centimetre ruler. "
                          "How many centimetres long is it?" % thing,
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm"},
                "answer": v, "answer_type": "int",
                "solution": ["Line the %s up with 0 on the centimetre ruler." % thing,
                             "The other end reaches %d cm." % v]}

    if t == 6:                    # NEW: which metric unit of length is appropriate?
        thing, unit_name = pick(_UNIT_LENGTH)
        return _num_q("Which metric unit of length is the most appropriate for measuring "
                      "%s: millimetres, centimetres or metres? (type the unit)" % thing,
                      unit_name, "str", text=True,
                      placeholder="millimetres / centimetres / metres",
                      solution=["%s is best measured in %s."
                                % (thing.capitalize(), unit_name)])

    if t == 7:                    # NEW: compare and convert metric units of length
        cm = random.randint(15, 95)
        mm = random.randint(100, 900)
        while mm == cm * 10:
            mm = random.randint(100, 900)
        return _num_q("Compare these metric units of length. Which is longer: %d cm or "
                      "%d mm? Convert both to millimetres and write the longer length in mm."
                      % (cm, mm),
                      max(cm * 10, mm), "int", unit="mm",
                      solution=["1 cm = 10 mm, so %d cm = %d mm." % (cm, cm * 10),
                                "The longer length is %d mm." % max(cm * 10, mm)])

    # ruler + real-life comparison
    v, mx, unit = _ruler_len(d)
    v = max(v, 3)                      # a 1 cm crayon reads as nonsense
    other = v + random.randint(1, 5)
    return {"prompt": "The ruler shows a crayon. A pen is %d %s long. "
                      "How much LONGER is the pen, in %s?" % (other, unit, unit),
            "component": "ruler",
            "spec": {"mode": "length", "value": v, "max": mx, "unit": unit},
            "answer": other - v, "answer_type": "int",
            "solution": ["The crayon measures %d %s." % (v, unit),
                         "%d − %d = %d %s." % (other, v, other - v, unit)]}


@skill("Y3.7.b", "Add and subtract lengths", S7)
def _(d=1):
    d = _tier(d)
    hi = _by_d(d, 50, 180, 500)
    t = _pick_t([1, 1, 2, 1, 2, 1, 1])

    if t == 0:                                          # addition word problem
        a = random.randint(10, hi)
        b = random.randint(10, hi)
        return _num_q("A rope is %d cm long. Another rope is %d cm long. "
                      "What is their total length?" % (a, b),
                      a + b, "int", unit="cm",
                      solution=["%d + %d = %d cm." % (a, b, a + b)])

    if t == 1:                                          # subtraction word problem
        a = random.randint(40, hi) + 30
        b = random.randint(10, a - 10)
        return _num_q("A ribbon is %d cm long. %d cm is cut off. How much is left?" % (a, b),
                      a - b, "int", unit="cm",
                      solution=["%d − %d = %d cm." % (a, b, a - b)])

    if t == 2:                                          # ruler based (visual)
        v, mx, unit = _ruler_len(d)
        extra = random.randint(2, 9)
        return {"prompt": "The ruler shows a stick. A second stick is %d %s longer. "
                          "How long are the two sticks altogether, in %s?" % (extra, unit, unit),
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": unit},
                "answer": 2 * v + extra, "answer_type": "int",
                "solution": ["The first stick is %d %s, the second is %d %s."
                             % (v, unit, v + extra, unit),
                             "%d + %d = %d %s." % (v, v + extra, 2 * v + extra, unit)]}

    if t == 3:                                          # missing number
        a = random.randint(20, hi)
        b = random.randint(20, hi)
        return _num_q("Complete: %d cm + ___ cm = %d cm" % (a, a + b),
                      b, "int", unit="cm",
                      solution=["%d − %d = %d cm." % (a + b, a, b)])

    if t == 4:                                          # ruler: cut a piece off (visual)
        v, mx, unit = _ruler_len(d)
        while v < 3:
            v, mx, unit = _ruler_len(d)
        cut = random.randint(1, v - 1)
        return {"prompt": "The ruler shows a strip of paper. %d %s is cut off. "
                          "How long is the strip now, in %s?" % (cut, unit, unit),
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": unit},
                "answer": v - cut, "answer_type": "int",
                "solution": ["The strip measures %d %s." % (v, unit),
                             "%d − %d = %d %s." % (v, cut, v - cut, unit)]}

    if t == 6:                    # NEW: metric units of length word problem (cm + mm)
        who = pick(NAMES)
        cm = random.randint(5, _by_d(d, 12, 25, 40))
        mm = random.randrange(20, _by_d(d, 90, 150, 250), 5)
        return _num_q("%s joins a pencil %d cm long and a crayon %d mm long end to end. "
                      "How long are they altogether, in millimetres?" % (who, cm, mm),
                      cm * 10 + mm, "int", unit="mm",
                      solution=["1 cm = 10 mm, so %d cm = %d mm." % (cm, cm * 10),
                                "%d + %d = %d mm." % (cm * 10, mm, cm * 10 + mm)])

    # mixed m and cm
    m = random.randint(1, _by_d(d, 2, 3, 5))
    cm = random.randint(10, 90)
    used = random.randint(20, 90)
    total = m * 100 + cm
    return _num_q("A plank is %d m %d cm long. %d cm is sawn off. "
                  "How long is the plank now, in cm?" % (m, cm, used),
                  total - used, "int", unit="cm",
                  solution=["%d m %d cm = %d cm." % (m, cm, total),
                            "%d − %d = %d cm." % (total, used, total - used)])


@skill("Y3.7.c", "Mass (kg and g)", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 2, 1, 1, 1, 1, 1])
    stepg = _by_d(d, 100, 50, 25)

    if t == 0:                                          # scale reading (visual)
        v = random.randrange(stepg, 1000 + 1, stepg)
        return {"prompt": "Read the scales. What is the mass, in grams?",
                "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v, "answer_type": "int",
                "solution": ["The pointer is at %d g." % v]}

    if t == 1:                                          # kg + g -> g
        kg = random.randint(1, _by_d(d, 2, 4, 9))
        g = random.choice([100, 200, 250, 500, 750])
        return _num_q("How many grams are there in %d kg %d g?" % (kg, g),
                      kg * 1000 + g, "int", unit="g",
                      solution=["1 kg = 1000 g, so %d kg = %d g." % (kg, kg * 1000),
                                "%d + %d = %d g." % (kg * 1000, g, kg * 1000 + g)])

    if t == 2:                                          # scale + add (visual)
        v = random.randrange(stepg, 800 + 1, stepg)
        add = random.randrange(stepg, 200 + 1, stepg)
        return {"prompt": "The scales show some flour. %d g more flour is added. "
                          "What is the new mass, in grams?" % add,
                "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v + add, "answer_type": "int",
                "solution": ["The scales read %d g." % v,
                             "%d + %d = %d g." % (v, add, v + add)]}

    if t == 3:                                          # comparison
        a = random.randrange(100, 1000, 50)
        b_kg = random.randint(1, 3)
        b = b_kg * 1000
        return _num_q("Which is heavier: %d g or %d kg? Write the heavier mass in grams."
                      % (a, b_kg),
                      max(a, b), "int", unit="g",
                      solution=["%d kg = %d g." % (b_kg, b),
                                "The heavier mass is %d g." % max(a, b)])

    if t == 5:                    # NEW: which metric unit of mass is appropriate?
        thing, unit_name = pick(_UNIT_MASS)
        return _num_q("Which metric unit of mass is the most appropriate for weighing "
                      "%s: grams or kilograms? (type the unit)" % thing,
                      unit_name, "str", text=True, placeholder="grams / kilograms",
                      solution=["The mass of %s is best measured in %s."
                                % (thing, unit_name)])

    if t == 6:                    # NEW: compare and convert metric units of mass
        kg = random.randint(1, 4)
        g = random.randrange(500, 4500, 100)
        while g == kg * 1000:
            g = random.randrange(500, 4500, 100)
        return _num_q("Compare these metric units of mass. Which is heavier: %d kg or "
                      "%d g? Convert both to grams and write the heavier mass in grams."
                      % (kg, g),
                      max(kg * 1000, g), "int", unit="g",
                      solution=["1 kg = 1000 g, so %d kg = %d g." % (kg, kg * 1000),
                                "The heavier mass is %d g." % max(kg * 1000, g)])

    if t == 7:                    # NEW: mass and volume word problem
        who = pick(NAMES)
        kg = random.randint(1, 3)
        g = random.randrange(100, 900, 50)
        poured = random.randrange(50, 600, 50)
        total = kg * 1000 + g
        return _num_q("%s has a jug of water with a mass of %d kg %d g. %s pours out water "
                      "with a mass of %d g. What is the mass of the jug of water now, "
                      "in grams?" % (who, kg, g, who, poured),
                      total - poured, "int", unit="g",
                      solution=["%d kg %d g = %d g." % (kg, g, total),
                                "%d − %d = %d g." % (total, poured, total - poured)])

    # word problem
    who = pick(NAMES)
    bags = random.randint(2, _by_d(d, 3, 5, 8))
    per = random.choice([250, 500, 200])
    return _num_q("%s buys %d bags of rice weighing %d g each. "
                  "What is the total mass, in grams?" % (who, bags, per),
                  bags * per, "int", unit="g",
                  solution=["%d × %d = %d g." % (bags, per, bags * per)])


@skill("Y3.7.d", "Capacity (l and ml)", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 1, 2, 2, 1, 2, 1, 1])
    stepml = _by_d(d, 100, 50, 50)

    if t == 0:                                          # jug reading (visual)
        v = random.randrange(stepml, 1000 + 1, stepml)
        return {"prompt": "Read the measuring jug. How much liquid is in it, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v, "answer_type": "int",
                "solution": ["The liquid reaches the %d ml mark." % v]}

    if t == 1:                                          # l + ml -> ml
        l = random.randint(1, _by_d(d, 2, 4, 9))
        ml = random.choice([100, 250, 500, 750])
        return _num_q("How many millilitres are there in %d l %d ml?" % (l, ml),
                      l * 1000 + ml, "int", unit="ml",
                      solution=["1 l = 1000 ml, so %d l = %d ml." % (l, l * 1000),
                                "%d + %d = %d ml." % (l * 1000, ml, l * 1000 + ml)])

    if t == 2:                                          # jug + pour out (visual)
        v = random.randrange(2 * stepml, 1000 + 1, stepml)
        out = random.randrange(stepml, v, stepml) if v > stepml else stepml
        return {"prompt": "The jug shows some water. %d ml is poured out. "
                          "How much water is left, in ml?" % out,
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v - out, "answer_type": "int",
                "solution": ["The jug holds %d ml." % v,
                             "%d − %d = %d ml." % (v, out, v - out)]}

    if t == 3:                                          # how much more to fill
        v = random.randrange(stepml, 1000, stepml)
        return {"prompt": "The jug shows some juice. How much MORE juice is needed "
                          "to make 1 litre, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": 1000 - v, "answer_type": "int",
                "solution": ["1 litre = 1000 ml and the jug shows %d ml." % v,
                             "1000 − %d = %d ml." % (v, 1000 - v)]}

    if t == 5:                    # NEW: measure liquid volumes in metric units
        v = random.randrange(stepml, 1000 + 1, stepml)
        return {"prompt": "Measure the liquid volume in this jug. The scale is marked in "
                          "metric units of millilitres — what is the liquid volume, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v, "answer_type": "int",
                "solution": ["Read the mark at the top of the liquid.",
                             "The liquid volume is %d ml." % v]}

    if t == 6:                    # NEW: which metric unit of volume is appropriate?
        thing, unit_name = pick(_UNIT_VOLUME)
        return _num_q("Which metric unit of volume is the most appropriate for measuring "
                      "%s: millilitres or litres? (type the unit)" % thing,
                      unit_name, "str", text=True, placeholder="millilitres / litres",
                      solution=["The volume of %s is best measured in %s."
                                % (thing, unit_name)])

    if t == 7:                    # NEW: compare and convert metric units of volume
        l = random.randint(1, 4)
        ml = random.randrange(500, 4500, 100)
        while ml == l * 1000:
            ml = random.randrange(500, 4500, 100)
        return _num_q("Compare these metric units of volume. Which holds more: %d l or "
                      "%d ml? Convert both to millilitres and write the larger volume in ml."
                      % (l, ml),
                      max(l * 1000, ml), "int", unit="ml",
                      solution=["1 l = 1000 ml, so %d l = %d ml." % (l, l * 1000),
                                "The larger volume is %d ml." % max(l * 1000, ml)])

    # word problem
    who = pick(NAMES)
    cups = random.randint(2, _by_d(d, 3, 6, 9))
    per = random.choice([150, 200, 250])
    return _num_q("%s pours %d cups of squash, each holding %d ml. "
                  "How much squash is that altogether, in ml?" % (who, cups, per),
                  cups * per, "int", unit="ml",
                  solution=["%d × %d = %d ml." % (cups, per, cups * per)])


@skill("Y3.7.e", "Convert units of measurement", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 2, 2, 1, 1, 1])

    if t == 0:                                          # forward conversion
        kind = pick(_by_d(d, ["cm_mm", "m_cm"], ["cm_mm", "m_cm", "kg_g", "l_ml"],
                          ["cm_mm", "m_cm", "kg_g", "l_ml"]))
        table = {"cm_mm": ("centimetres", "millimetres", 10, "mm", "1 cm = 10 mm"),
                 "m_cm": ("metres", "centimetres", 100, "cm", "1 m = 100 cm"),
                 "kg_g": ("kilograms", "grams", 1000, "g", "1 kg = 1000 g"),
                 "l_ml": ("litres", "millilitres", 1000, "ml", "1 l = 1000 ml")}[kind]
        v = random.randint(2, _by_d(d, 5, 9, 12))
        return _num_q("How many %s are there in %d %s?" % (table[1], v, table[0]),
                      v * table[2], "int", unit=table[3],
                      solution=["%s." % table[4],
                                "%d × %d = %d %s." % (v, table[2], v * table[2], table[3])])

    if t == 1:                                          # backward conversion
        kind = pick(["mm_cm", "cm_m", "g_kg", "ml_l"])
        table = {"mm_cm": ("millimetres", "centimetres", 10, "cm", "10 mm = 1 cm"),
                 "cm_m": ("centimetres", "metres", 100, "m", "100 cm = 1 m"),
                 "g_kg": ("grams", "kilograms", 1000, "kg", "1000 g = 1 kg"),
                 "ml_l": ("millilitres", "litres", 1000, "l", "1000 ml = 1 l")}[kind]
        v = random.randint(2, _by_d(d, 4, 9, 12))
        return _num_q("How many %s are there in %d %s?"
                      % (table[1], v * table[2], table[0]),
                      v, "int", unit=table[3],
                      solution=["%s." % table[4],
                                "%d ÷ %d = %d %s." % (v * table[2], table[2], v, table[3])])

    if t == 2:                                          # ruler reading -> convert (visual)
        v = random.randint(1, _by_d(d, 10, 20, 30))
        mx = _by_d(d, 10, 20, 30)
        return {"prompt": "Read the ruler. How long is the line, in millimetres?",
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm"},
                "answer": v * 10, "answer_type": "int",
                "solution": ["The line measures %d cm." % v,
                             "1 cm = 10 mm, so %d cm = %d mm." % (v, v * 10)]}

    if t == 3:                                          # jug reading -> convert (visual)
        half = pick(_by_d(d, [250, 500, 750], [100, 200, 250, 500, 750, 800],
                          [50, 150, 250, 350, 450, 550, 650, 750, 950]))
        return {"prompt": "The jug shows some water. How many millilitres short of "
                          "1 litre is it?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": half, "max": 1000, "unit": "ml"},
                "answer": 1000 - half, "answer_type": "int",
                "solution": ["1 litre = 1000 ml.",
                             "1000 − %d = %d ml." % (half, 1000 - half)]}

    if t == 5:                    # NEW: choose the appropriate measuring tool
        job, tool = pick([
            ("how long a pencil case is", "ruler"),
            ("how heavy a bag of apples is", "scales"),
            ("how much water a bottle holds", "measuring jug"),
            ("how tall a wall is", "tape measure"),
            ("how long a lesson lasts", "clock"),
            ("how warm the classroom is", "thermometer"),
        ])
        return _num_q("Choose the appropriate measuring tool. Which tool would you use to "
                      "measure %s — ruler, tape measure, scales, measuring jug, clock or "
                      "thermometer? (type the tool)" % job,
                      tool, "str", text=True, placeholder="type the tool",
                      solution=["To measure %s you use %s." % (job, _a(tool))])

    if t == 6:                    # NEW: compare size, weight and capacity
        prop, ask, big, small = pick([
            ("size", "longer", "bus", "pencil"),
            ("weight", "heavier", "brick", "feather"),
            ("capacity", "larger", "bucket", "teaspoon"),
            ("weight", "heavier", "apple", "paperclip"),
            ("capacity", "larger", "bath", "mug"),
            ("size", "taller", "tree", "flower"),
        ])
        first, second = ((big, small) if random.random() < 0.5 else (small, big))
        return _num_q("Compare the %s of these two things. Which is %s — %s or %s? "
                      "(type one word)" % (prop, ask, first, second),
                      big, "str", text=True, placeholder="type one word",
                      solution=["Compare their %s." % prop,
                                "The %s one is the %s." % (ask, big)])

    # missing number
    kind = pick([("cm", "m", 100), ("mm", "cm", 10), ("g", "kg", 1000), ("ml", "l", 1000)])
    small, big, factor = kind
    v = random.randint(2, 8)
    return _num_q("Complete: ___ %s = %d %s" % (small, v, big),
                  v * factor, "int", unit=small,
                  solution=["1 %s = %d %s." % (big, factor, small),
                            "%d × %d = %d %s." % (v, factor, v * factor, small)])


@skill("Y3.7.f", "Add and subtract money", S7)
def _(d=1):
    d = _tier(d)
    hi = _by_d(d, 300, 780, 1500)
    t = _pick_t([1, 1, 2, 1, 2, 2, 1, 1, 1, 1])

    if t == 0:                                          # addition
        a = random.randint(60, hi)
        b = random.randint(50, hi)
        return _num_q("Add %s and %s. Give your answer in pence." % (money(a), money(b)),
                      a + b, "int", unit="p",
                      solution=["%d + %d = %d p." % (a, b, a + b),
                                "That is %s." % money(a + b)])

    if t == 1:                                          # subtraction
        a = random.randint(150, hi) + 100
        b = random.randint(50, a - 20)
        return _num_q("%s spends %s from %s. How much is left, in pence?"
                      % (pick(NAMES), money(b), money(a)),
                      a - b, "int", unit="p",
                      solution=["%d − %d = %d p." % (a, b, a - b),
                                "That is %s." % money(a - b)])

    if t == 2:                                          # price chart, total (visual)
        names = random.sample(["Pen", "Rubber", "Ruler", "Notebook", "Sharpener"], 3)
        items = [random.randint(20, max(30, hi // 2)) for _ in names]
        return {"prompt": "The chart shows the price of each item in pence. "
                          "How much do all three cost altogether, in pence?",
                "component": "bar_chart",
                "spec": {"categories": names, "values": items, "mode": "read"},
                "answer": sum(items), "answer_type": "int",
                "solution": ["%s = %d p." % (" + ".join(str(v) for v in items), sum(items)),
                             "That is %s." % money(sum(items))]}

    if t == 3:                                          # missing number
        a = random.randint(60, hi)
        b = random.randint(50, hi)
        return _num_q("Complete: %s + ___ p = %s" % (money(a), money(a + b)),
                      b, "int", unit="p",
                      solution=["%d − %d = %d p." % (a + b, a, b)])

    if t == 5:                    # NEW: count coins and notes
        pool = _by_d(d, [5, 10, 20, 50], [10, 20, 50, 100, 200], [20, 50, 100, 200, 500, 1000])
        vals = random.sample(pool, 3)
        items = [(random.randint(1, 4), v) for v in vals]
        total = sum(c * v for c, v in items)
        return _num_q("Count the coins and notes: %s. How much money is there altogether, "
                      "in pence?" % _coin_list(items),
                      total, "int", unit="p",
                      solution=[" + ".join("%d × %d" % (c, v) for c, v in items)
                                + " = %d p." % total,
                                "That is %s." % money(total)])

    if t == 6:                    # NEW: equivalent amounts of money — up to £1
        coin = pick([2, 5, 10, 20, 50])
        count = random.randint(2, min(9, 100 // coin))
        total = coin * count
        return _num_q("Equivalent amounts of money: how many %dp coins have the same value "
                      "as %s?" % (coin, money(total)),
                      count, "int", unit="coins",
                      solution=["%d ÷ %d = %d." % (total, coin, count),
                                "%d %dp coins are equivalent to %s."
                                % (count, coin, money(total))])

    if t == 7:                    # NEW: equivalent amounts of money — up to £5
        coin = pick([20, 50, 100])
        count = random.randint(3, 500 // coin)
        total = coin * count
        return _num_q("Equivalent amounts of money: %s is made up only of %s. "
                      "How many of those coins are there?"
                      % (money(total), _coin_name(coin) + "s"),
                      count, "int", unit="coins",
                      solution=["%d ÷ %d = %d." % (total, coin, count),
                                "%s is equivalent to %d %ss."
                                % (money(total), count, _coin_name(coin))])

    if t == 8:                    # NEW: comparing groups of coins
        g1 = [(random.randint(1, 3), v) for v in random.sample([5, 10, 20, 50], 2)]
        g2 = [(random.randint(1, 3), v) for v in random.sample([5, 10, 20, 50, 100], 2)]
        s1 = sum(c * v for c, v in g1)
        s2 = sum(c * v for c, v in g2)
        while s1 == s2:
            g2 = [(random.randint(1, 4), v) for v in random.sample([5, 10, 20, 50, 100], 2)]
            s2 = sum(c * v for c, v in g2)
        return _num_q("Compare these two groups of coins. Group A: %s. Group B: %s. "
                      "Which group is worth more? Write the larger value in pence."
                      % (_coin_list(g1), _coin_list(g2)),
                      max(s1, s2), "int", unit="p",
                      solution=["Group A is worth %d p and group B is worth %d p." % (s1, s2),
                                "The larger value is %s." % money(max(s1, s2))])

    if t == 9:                    # NEW: how much more to make one pound?
        have = random.randrange(5, 100, 5)
        return _num_q("%s has %s. How much more money is needed to make one pound, "
                      "in pence?" % (pick(NAMES), money(have)),
                      100 - have, "int", unit="p",
                      solution=["One pound = 100 p.",
                                "100 − %d = %d p." % (have, 100 - have)])

    # comparison from a price chart (visual)
    names = random.sample(["Book", "Game", "Kite", "Ball"], 3)
    items = [random.randint(20, max(40, hi)) for _ in names]
    while len(set(items)) != len(items):
        items = [random.randint(20, max(40, hi)) for _ in names]
    top = items.index(max(items))
    bot = items.index(min(items))
    return {"prompt": "The chart shows prices in pence. How much MORE does the dearest "
                      "item cost than the cheapest one, in pence?",
            "component": "bar_chart",
            "spec": {"categories": names, "values": items, "mode": "read"},
            "answer": items[top] - items[bot], "answer_type": "int",
            "solution": ["The dearest is %s (%d p), the cheapest is %s (%d p)."
                         % (names[top], items[top], names[bot], items[bot]),
                         "%d − %d = %d p." % (items[top], items[bot],
                                              items[top] - items[bot])]}


@skill("Y3.7.g", "Give change", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 2, 1, 1])

    if t == 0:                                          # basic change
        paid = pick(_by_d(d, [100, 200], [500, 1000], [1000, 2000]))
        cost = random.randint(max(20, paid // 5), paid - 10)
        return _num_q("A toy costs %s. You pay with %s. How much change do you get, in pence?"
                      % (money(cost), money(paid)),
                      paid - cost, "int", unit="p",
                      solution=["%d − %d = %d p." % (paid, cost, paid - cost),
                                "That is %s." % money(paid - cost)])

    if t == 1:                                          # two items then change
        paid = pick(_by_d(d, [200, 500], [500, 1000], [1000, 2000]))
        a = random.randint(30, paid // 3)
        b = random.randint(30, paid // 3)
        return _num_q("%s buys a drink for %s and a cake for %s, and pays with %s. "
                      "How much change, in pence?" % (pick(NAMES), money(a), money(b), money(paid)),
                      paid - a - b, "int", unit="p",
                      solution=["%d + %d = %d p spent." % (a, b, a + b),
                                "%d − %d = %d p change." % (paid, a + b, paid - a - b)])

    if t == 2:                                          # missing number
        paid = pick([500, 1000])
        change = random.randint(20, paid - 50)
        return _num_q("You pay with %s and get %s change. How much did the item cost, in pence?"
                      % (money(paid), money(change)),
                      paid - change, "int", unit="p",
                      solution=["%d − %d = %d p." % (paid, change, paid - change),
                                "The item cost %s." % money(paid - change)])

    if t == 4:                    # NEW: making change — a purchase up to £1
        cost = random.randrange(5, 100, 5)
        item = pick(["rubber", "lolly", "pencil", "sticker", "badge"])
        who = pick(NAMES)
        return _num_q("A %s costs %s. %s pays with a £1 coin. Making change, how much "
                      "change should %s be given, in pence?"
                      % (item, money(cost), who, who),
                      100 - cost, "int", unit="p",
                      solution=["A £1 coin is 100 p.",
                                "100 − %d = %d p change." % (cost, 100 - cost)])

    if t == 5:                    # NEW: making change — a purchase up to £10
        cost = random.randrange(105, 1000, 5)
        item = pick(["book", "toy car", "puzzle", "board game", "kite"])
        who = pick(NAMES)
        return _num_q("A %s costs %s. %s pays with a £10 note. Making change, how much "
                      "change should %s be given, in pence?"
                      % (item, money(cost), who, who),
                      1000 - cost, "int", unit="p",
                      solution=["A £10 note is 1000 p.",
                                "1000 − %d = %d p, which is %s."
                                % (cost, 1000 - cost, money(1000 - cost))])

    # change from a price chart (visual)
    paid = pick(_by_d(d, [200, 500], [500, 1000], [1000, 2000]))
    names = random.sample(["Drink", "Cake", "Apple", "Crisps"], 3)
    items = [random.randint(20, paid // 4) for _ in names]
    i = random.randrange(3)
    j = (i + 1) % 3
    return {"prompt": "The chart shows prices in pence. %s buys the %s and the %s and "
                      "pays with %s. How much change, in pence?"
                      % (pick(NAMES), names[i].lower(), names[j].lower(), money(paid)),
            "component": "bar_chart",
            "spec": {"categories": names, "values": items, "mode": "read"},
            "answer": paid - items[i] - items[j], "answer_type": "int",
            "solution": ["%d + %d = %d p spent." % (items[i], items[j], items[i] + items[j]),
                         "%d − %d = %d p change."
                         % (paid, items[i] + items[j], paid - items[i] - items[j])]}


@skill("Y3.7.h", "Perimeter of a rectangle", S7)
def _(d=1):
    d = _tier(d)
    hi = _by_d(d, 8, 15, 25)
    t = _pick_t([1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2])

    if t == 0:                                          # rectangle
        w = random.randint(2, hi)
        h = random.randint(2, hi)
        while h == w:
            h = random.randint(2, hi)
        return _num_q("A rectangle is %d cm long and %d cm wide. What is its perimeter?" % (w, h),
                      2 * (w + h), "int", unit="cm",
                      solution=["Perimeter = %d + %d + %d + %d." % (w, h, w, h),
                                "That is %d cm." % (2 * (w + h))])

    if t == 1:                                          # square (visual shape)
        s = random.randint(2, hi)
        return {"prompt": "Each side of this square is %d cm. What is its perimeter, in cm?" % s,
                "component": "shape",
                "spec": {"kind": "2d", "name": "square", "ask": "sides", "marks": "right_angle"},
                "answer": 4 * s, "answer_type": "int",
                "solution": ["A square has 4 equal sides.",
                             "4 × %d = %d cm." % (s, 4 * s)]}

    if t == 2:                                          # missing side
        w = random.randint(2, hi)
        h = random.randint(2, hi)
        while h == w:
            h = random.randint(2, hi)
        p = 2 * (w + h)
        return _num_q("A rectangle has a perimeter of %d cm. One side is %d cm. "
                      "How long is the side next to it?" % (p, w),
                      h, "int", unit="cm",
                      solution=["%d ÷ 2 = %d is one long side plus one short side." % (p, p // 2),
                                "%d − %d = %d cm." % (p // 2, w, h)])

    if t == 3:                                          # regular polygon (visual shape)
        name, sides = pick([("pentagon", 5), ("hexagon", 6), ("octagon", 8)])
        s = random.randint(2, _by_d(d, 6, 10, 15))
        return {"prompt": "This regular %s has sides of %d cm. What is its perimeter, in cm?"
                          % (name, s),
                "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": sides * s, "answer_type": "int",
                "solution": ["%s has %d equal sides." % (_a(name).capitalize(), sides),
                             "%d × %d = %d cm." % (sides, s, sides * s)]}

    if t == 5:                    # NEW: perimeter of a figure on a grid
        rows = random.randint(2, _by_d(d, 4, 6, 8))
        cols = random.randint(2, _by_d(d, 4, 6, 8))
        return {"prompt": "Find the perimeter of this figure on the grid. Count the unit "
                          "sides all the way around the edge of the figure.",
                "component": "area_grid",
                "spec": {"mode": "read_perimeter", "rows": rows, "cols": cols},
                "answer": 2 * (rows + cols), "answer_type": "int",
                "solution": ["The figure is %d squares by %d squares." % (rows, cols),
                             "Perimeter = %d + %d + %d + %d = %d units."
                             % (rows, cols, rows, cols, 2 * (rows + cols))]}

    if t == 6:                    # NEW: area of a rectangle
        w = random.randint(2, _by_d(d, 6, 9, 12))
        h = random.randint(2, _by_d(d, 6, 9, 12))
        return _num_q("A rectangle is %d cm long and %d cm wide. What is its area, in "
                      "square centimetres?" % (w, h),
                      w * h, "int", unit="square cm",
                      solution=["Area = length × width.",
                                "%d × %d = %d square centimetres." % (w, h, w * h)])

    if t == 7:                    # NEW: area of a figure on a grid
        rows = random.randint(2, _by_d(d, 4, 6, 8))
        cols = random.randint(2, _by_d(d, 4, 6, 8))
        return {"prompt": "Find the area of this figure on the grid. Count the unit "
                          "squares that the figure covers.",
                "component": "area_grid",
                "spec": {"mode": "read_area", "rows": rows, "cols": cols},
                "answer": rows * cols, "answer_type": "int",
                "solution": ["The figure is %d rows of %d squares." % (rows, cols),
                             "%d × %d = %d square units." % (rows, cols, rows * cols)]}

    if t == 8:                    # NEW: select the figure with a given area
        dims = []
        while len(dims) < 3:
            a = random.randint(2, _by_d(d, 5, 7, 9))
            b = random.randint(2, _by_d(d, 5, 7, 9))
            if all(a * b != x * y for x, y in dims):
                dims.append((a, b))
        labels = ["A", "B", "C"]
        k = random.randrange(3)
        area = dims[k][0] * dims[k][1]
        desc = "; ".join("%s is %d squares by %d squares" % (labels[i], dims[i][0], dims[i][1])
                         for i in range(3))
        return _num_q("Select the figure with an area of %d square units. %s. "
                      "Which figure is it? (type A, B or C)" % (area, desc),
                      labels[k], "str", text=True, placeholder="A / B / C",
                      solution=["Area = rows × columns for each figure.",
                                "%s: %d × %d = %d square units."
                                % (labels[k], dims[k][0], dims[k][1], area)])

    if t == 9:                    # NEW: two figures with the same area
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        while a * b < 8 or a == b:
            a, b = random.randint(2, 6), random.randint(2, 6)
        same = a * b
        pairs = [(a, b), (b, a)]
        odd = (a, b)
        while odd[0] * odd[1] == same:
            odd = (random.randint(2, 7), random.randint(2, 7))
        order = [pairs[0], odd, pairs[1]]
        labels = ["A", "B", "C"]
        desc = "; ".join("%s is %d squares by %d squares" % (labels[i], order[i][0], order[i][1])
                         for i in range(3))
        return _num_q("Two of these figures have the same area. %s. "
                      "What is that area, in square units?" % desc,
                      same, "int", unit="square units",
                      solution=["A: %d, B: %d, C: %d square units."
                                % (order[0][0] * order[0][1], order[1][0] * order[1][1],
                                   order[2][0] * order[2][1]),
                                "Two figures share an area of %d square units." % same])

    if t == 10:                   # NEW: create a figure with a given area
        rows = random.randint(3, 6)
        cols = random.randint(3, 6)
        target = random.randint(3, rows * cols - 1)
        return {"prompt": "Create a figure with an area of %d square units by shading "
                          "squares on the grid." % target,
                "component": "area_grid",
                "spec": {"mode": "build_area", "rows": rows, "cols": cols},
                "answer": target, "answer_type": "int",
                "solution": ["Each shaded square is 1 square unit of area.",
                             "Shade exactly %d squares." % target]}

    # real-life context
    w = random.randint(3, hi)
    h = random.randint(3, hi)
    while h == w:
        h = random.randint(3, hi)
    return _num_q("A garden is %d m long and %d m wide. A fence goes all the way round. "
                  "How many metres of fence are needed?" % (w, h),
                  2 * (w + h), "int", unit="m",
                  solution=["Perimeter = 2 × (%d + %d)." % (w, h),
                            "2 × %d = %d m." % (w + h, 2 * (w + h))])


# ------------------------------------------------------------------ 3.8 ------
@skill("Y3.8.a", "Set the time on a clock", S8)
def _(d=1):
    d = _tier(d)
    h = random.randint(1, 12)
    m = pick(_clock_minutes(d))
    t = _pick_t([1, 1, 1, 1, 1])

    if t == 0:                                          # digital -> clock
        return {"prompt": "Set the clock to %s." % _hm(h, m),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m), "answer_type": "time",
                "solution": ["The hour hand goes just past %d." % h,
                             "The minute hand shows %d minutes." % m]}

    if t == 1:                                          # o'clock / half past (words)
        mm = pick(_by_d(d, [0, 30], [0, 15, 30, 45], [0, 15, 30, 45]))
        phrase = {0: "%d o'clock" % h, 15: "quarter past %d" % h,
                  30: "half past %d" % h,
                  45: "quarter to %d" % (1 if h == 12 else h + 1)}[mm]
        return {"prompt": "Set the clock to %s." % phrase,
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, mm), "answer_type": "time",
                "solution": ["%s is %s." % (phrase.capitalize(), _hm(h, mm))]}

    if t == 2:                                          # minutes past
        mm = pick(_by_d(d, [5, 10], [5, 10, 20, 25], [5, 10, 20, 25]))
        return {"prompt": "Set the clock to %d minutes past %d." % (mm, h),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, mm), "answer_type": "time",
                "solution": ["%d minutes past %d is %s." % (mm, h, _hm(h, mm))]}

    if t == 3:                                          # minutes to (stretch-friendly)
        mm = pick(_by_d(d, [15], [5, 10, 15, 20, 25], [5, 10, 20, 25]))
        nh = 1 if h == 12 else h + 1
        return {"prompt": "Set the clock to %d minutes to %d." % (mm, nh),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, 60 - mm), "answer_type": "time",
                "solution": ["%d minutes to %d means %d minutes before %d o'clock." % (mm, nh, mm, nh),
                             "That is %s." % _hm(h, 60 - mm)]}

    # real-life context
    event = pick([("registration", 9, 0), ("break time", 10, 30), ("lunch", 12, 15),
                  ("home time", 3, 30), ("swimming", 4, 45), ("bedtime", 8, 0)])
    label, eh, em = event
    return {"prompt": "%s is at %s. Set the clock to that time."
                      % (label.capitalize(), _hm(eh, em)),
            "component": "clock", "spec": {"mode": "set"},
            "answer": _hm(eh, em), "answer_type": "time",
            "solution": ["The minute hand points to %d minutes." % em,
                         ("The hour hand points to %d." % eh) if em == 0 else
                         ("The hour hand is between %d and %d." % (eh, eh % 12 + 1))]}


@skill("Y3.8.b", "Analogue to digital time", S8)
def _(d=1):
    d = _tier(d)
    h = random.randint(1, 12)
    t = _pick_t([1, 1, 1, 2, 2])

    if t == 0:                                          # quarter/half past -> digital
        m = pick(_by_d(d, [15, 30], [15, 30], [15, 30]))
        phrase = {15: "quarter past", 30: "half past"}[m]
        return _num_q("Write '%s %d' in digital form (h:mm)." % (phrase, h),
                      _hm(h, m), "time", text=True, placeholder="e.g. 3:15",
                      solution=["Quarter past means 15 minutes; half past means 30 minutes.",
                                "%s %d is %s." % (phrase, h, _hm(h, m))])

    if t == 1:                                          # quarter to -> digital
        nh = 1 if h == 12 else h + 1
        return _num_q("Write 'quarter to %d' in digital form (h:mm)." % nh,
                      _hm(h, 45), "time", text=True, placeholder="e.g. 3:45",
                      solution=["Quarter to %d is 15 minutes before %d o'clock." % (nh, nh),
                                "That is %s." % _hm(h, 45)])

    if t == 2:                                          # minutes past -> digital
        m = pick(_by_d(d, [5, 10, 20], [5, 10, 20, 25, 35, 40], [5, 10, 20, 25, 35, 40, 50, 55]))
        return _num_q("Write '%d minutes past %d' in digital form (h:mm)." % (m, h),
                      _hm(h, m), "time", text=True, placeholder="e.g. 3:20",
                      solution=["%d minutes past %d is %s." % (m, h, _hm(h, m))])

    if t == 3:                                          # words -> clock (visual)
        m = pick(_by_d(d, [0, 30], [0, 15, 30, 45], [0, 15, 20, 30, 40, 45]))
        if m == 0:
            phrase = "%d o'clock" % h
        elif m == 15:
            phrase = "quarter past %d" % h
        elif m == 30:
            phrase = "half past %d" % h
        elif m == 45:
            phrase = "quarter to %d" % (1 if h == 12 else h + 1)
        else:
            phrase = "%d minutes past %d" % (m, h)
        return {"prompt": "Set the clock to show %s." % phrase,
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m), "answer_type": "time",
                "solution": ["%s in digital form is %s." % (phrase.capitalize(), _hm(h, m))]}

    # minutes to -> clock (visual)
    m = pick(_by_d(d, [15], [5, 10, 15, 20, 25], [5, 10, 20, 25]))
    nh = 1 if h == 12 else h + 1
    return {"prompt": "Set the clock to %d minutes to %d."
                      % (m, nh),
            "component": "clock", "spec": {"mode": "set"},
            "answer": _hm(h, 60 - m), "answer_type": "time",
            "solution": ["%d minutes before %d o'clock is %s." % (m, nh, _hm(h, 60 - m))]}


@skill("Y3.8.c", "Roman numerals I–XII", S8)
def _(d=1):
    d = _tier(d)
    lo, hi = _by_d(d, (1, 6), (1, 12), (1, 12))
    n = random.randint(lo, hi)
    t = _pick_t([1, 1, 2, 1, 1])

    if t == 0:                                          # number -> numeral
        return _num_q("Write %d as a Roman numeral." % n,
                      roman(n), "str", text=True, placeholder="e.g. VII",
                      solution=["%d is written %s." % (n, roman(n))])

    if t == 1:                                          # numeral -> number
        return _num_q("What number is the Roman numeral %s?" % roman(n), n, "int",
                      solution=["%s means %d." % (roman(n), n)])

    if t == 2:                                          # roman clock face (visual)
        m = pick(_by_d(d, [0, 30], [0, 15, 30, 45], [0, 15, 30, 45]))
        phrase = ("%s o'clock" % roman(n)) if m == 0 else \
                 ("%d minutes past %s" % (m, roman(n)))
        return {"prompt": "A clock face is numbered in Roman numerals. "
                          "Set the clock to %s." % phrase,
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(n, m), "answer_type": "time",
                "solution": ["%s is %d." % (roman(n), n),
                             "So the time is %s." % _hm(n, m)]}

    if t == 3:                                          # comparison
        a, b = random.sample(range(1, hi + 1), 2)
        return _num_q("Which is the larger number: %s or %s? Write it as a normal number."
                      % (roman(a), roman(b)),
                      max(a, b), "int",
                      solution=["%s = %d and %s = %d." % (roman(a), a, roman(b), b),
                                "The larger is %d." % max(a, b)])

    # missing number in a sequence
    n = random.randint(1, 11)
    return _num_q("Counting in Roman numerals, which numeral comes straight after %s?" % roman(n),
                  roman(n + 1), "str", text=True, placeholder="e.g. VIII",
                  solution=["%s = %d, and %d comes next." % (roman(n), n, n + 1),
                            "%d is written %s." % (n + 1, roman(n + 1))])


@skill("Y3.8.d", "Time interval within the hour", S8)
def _(d=1):
    d = _tier(d)
    h = random.randint(1, 11)
    m1 = pick(_by_d(d, [0, 15, 30], [0, 5, 10, 15, 20, 25, 30], [0, 5, 10, 12, 15, 20, 23, 25, 30]))
    dur = pick(_by_d(d, [15, 30], [10, 15, 20, 25, 30], [10, 15, 18, 20, 25, 27, 30]))
    if m1 + dur > 59:
        dur = 59 - m1
        if dur < 5:
            m1, dur = 0, 30
    m2 = m1 + dur
    t = _pick_t([1, 1, 2, 2, 1])

    if t == 0:                                          # bare interval
        return _num_q("How many minutes are there from %s to %s?" % (_hm(h, m1), _hm(h, m2)),
                      dur, "int", unit="minutes",
                      solution=["%d − %d = %d minutes." % (m2, m1, dur)])

    if t == 1:                                          # word problem
        who = pick(NAMES)
        act = pick(["reads a book", "plays football", "practises the piano", "walks to the park"])
        return _num_q("%s %s from %s until %s. For how many minutes?"
                      % (who, act, _hm(h, m1), _hm(h, m2)),
                      dur, "int", unit="minutes",
                      solution=["From %s to %s is %d − %d." % (_hm(h, m1), _hm(h, m2), m2, m1),
                                "That is %d minutes." % dur])

    if t == 2:                                          # find the END time (clock, visual)
        return {"prompt": "A film starts at %s and lasts %d minutes. "
                          "Set the clock to the time it ends." % (_hm(h, m1), dur),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m2), "answer_type": "time",
                "solution": ["%d + %d = %d minutes past %d." % (m1, dur, m2, h),
                             "The film ends at %s." % _hm(h, m2)]}

    if t == 3:                                          # find the START time (clock, visual)
        return {"prompt": "A lesson lasts %d minutes and finishes at %s. "
                          "Set the clock to the time it started." % (dur, _hm(h, m2)),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m1), "answer_type": "time",
                "solution": ["%d − %d = %d minutes past %d." % (m2, dur, m1, h),
                             "It started at %s." % _hm(h, m1)]}

    # missing number
    return _num_q("A game started at %s and lasted %d minutes. "
                  "How many minutes past %d o'clock did it finish?" % (_hm(h, m1), dur, h),
                  m2, "int", unit="minutes",
                  solution=["%d + %d = %d." % (m1, dur, m2),
                            "It finished at %s." % _hm(h, m2)])


@skill("Y3.8.e", "Time interval across the hour", S8)
def _(d=1):
    d = _tier(d)
    h = random.randint(1, 11)
    m1 = pick(_by_d(d, [30, 45], [35, 40, 45, 50, 55], [32, 35, 40, 43, 45, 50, 55]))
    m2 = pick(_by_d(d, [0, 15, 30], [5, 10, 15, 20, 25, 30], [5, 10, 12, 15, 20, 25, 28, 30]))
    mins = (60 - m1) + m2
    t = _pick_t([1, 1, 2, 2, 1, 2])

    if t == 0:                                          # bare interval
        return _num_q("How many minutes are there from %s to %s?"
                      % (_hm(h, m1), _hm(h + 1, m2)),
                      mins, "int", unit="minutes",
                      solution=["%d minutes to reach %d o'clock." % (60 - m1, h + 1),
                                "Then %d minutes more: %d minutes altogether." % (m2, mins)])

    if t == 1:                                          # word problem
        who = pick(NAMES)
        return _num_q("%s starts a journey at %s and arrives at %s. "
                      "How many minutes does the journey take?"
                      % (who, _hm(h, m1), _hm(h + 1, m2)),
                      mins, "int", unit="minutes",
                      solution=["%d minutes to %d o'clock, then %d more." % (60 - m1, h + 1, m2),
                                "%d + %d = %d minutes." % (60 - m1, m2, mins)])

    if t == 2:                                          # end time (clock, visual)
        return {"prompt": "A swimming lesson starts at %s and lasts %d minutes. "
                          "Set the clock to the finish time." % (_hm(h, m1), mins),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h + 1, m2), "answer_type": "time",
                "solution": ["%d minutes takes you to %d o'clock." % (60 - m1, h + 1),
                             "%d minutes more gives %s." % (m2, _hm(h + 1, m2))]}

    if t == 3:                                          # start time (clock, visual)
        return {"prompt": "A train journey lasts %d minutes and arrives at %s. "
                          "Set the clock to the departure time." % (mins, _hm(h + 1, m2)),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m1), "answer_type": "time",
                "solution": ["Go back %d minutes to %d o'clock." % (m2, h + 1),
                             "Then back %d more minutes: %s." % (60 - m1, _hm(h, m1))]}

    if t == 5:                    # NEW: reading a bus / train schedule
        stops = ["Park", "Library", "Museum", "Market", "Station"]
        gaps = [pick([10, 15, 20, 25, 30]) for _ in range(4)]
        start = h * 60 + pick([0, 5, 10, 15, 20, 25, 30])
        times = [start]
        for g in gaps:
            times.append(times[-1] + g)
        rows = "; ".join("%s %s" % (s, _hm((tm // 60) % 12 or 12, tm % 60))
                         for s, tm in zip(stops, times))
        i, j = sorted(random.sample(range(5), 2))
        return _num_q("Read the bus schedule. %s. According to the schedule, how many "
                      "minutes does the bus take to travel from %s to %s?"
                      % (rows, stops[i], stops[j]),
                      times[j] - times[i], "int", unit="minutes",
                      solution=["The bus leaves %s at %s and reaches %s at %s."
                                % (stops[i], _hm((times[i] // 60) % 12 or 12, times[i] % 60),
                                   stops[j], _hm((times[j] // 60) % 12 or 12, times[j] % 60)),
                                "That is %d minutes." % (times[j] - times[i])])

    # comparison
    other = mins + pick([5, 10, 15])
    return _num_q("Journey A takes %d minutes. Journey B goes from %s to %s. "
                  "How many minutes LONGER is journey A?"
                  % (other, _hm(h, m1), _hm(h + 1, m2)),
                  other - mins, "int", unit="minutes",
                  solution=["Journey B takes %d + %d = %d minutes." % (60 - m1, m2, mins),
                            "%d − %d = %d minutes." % (other, mins, other - mins)])


@skill("Y3.8.f", "Units of time", S8)
def _(d=1):
    d = _tier(d)
    table = {"min_sec": ("minutes", "seconds", 60, "1 minute = 60 seconds"),
             "hr_min": ("hours", "minutes", 60, "1 hour = 60 minutes"),
             "day_hr": ("days", "hours", 24, "1 day = 24 hours"),
             "week_day": ("weeks", "days", 7, "1 week = 7 days"),
             "year_month": ("years", "months", 12, "1 year = 12 months")}
    kinds = _by_d(d, ["week_day", "year_month", "hr_min"],
                  ["min_sec", "hr_min", "day_hr", "week_day", "year_month"],
                  ["min_sec", "hr_min", "day_hr", "week_day", "year_month"])
    big, small, factor, fact = table[pick(kinds)]
    v = random.randint(2, _by_d(d, 5, 8, 12))
    t = _pick_t([1, 1, 1, 1, 2, 2])

    if t == 0:                                          # multiply
        return _num_q("How many %s are there in %d %s?" % (small, v, big),
                      v * factor, "int", unit=small,
                      solution=["%s." % fact,
                                "%d × %d = %d %s." % (v, factor, v * factor, small)])

    if t == 1:                                          # divide
        return _num_q("How many %s are there in %d %s?" % (big, v * factor, small),
                      v, "int", unit=big,
                      solution=["%s." % fact,
                                "%d ÷ %d = %d %s." % (v * factor, factor, v, big)])

    if t == 2:                                          # missing number
        return _num_q("Complete: %d %s = ___ %s" % (v, big, small),
                      v * factor, "int", unit=small,
                      solution=["%s." % fact,
                                "%d × %d = %d." % (v, factor, v * factor)])

    if t == 3:                                          # word problem
        who = pick(NAMES)
        ctx = {"minutes": "%s reads a book for %d minutes.",
               "hours": "%s's coach trip lasts %d hours.",
               "days": "%s's school trip lasts %d days.",
               "weeks": "%s's swimming course lasts %d weeks.",
               "years": "%s has lived in the same house for %d years."}[big]
        return _num_q((ctx + " How many %s is that?") % (who, v, small),
                      v * factor, "int", unit=small,
                      solution=["%s." % fact,
                                "%d × %d = %d %s." % (v, factor, v * factor, small)])

    if t == 5:                    # NEW: days, months and seasons
        seasons = ["spring", "summer", "autumn", "winter"]
        months = {"January": "winter", "February": "winter", "March": "spring",
                  "April": "spring", "May": "spring", "June": "summer",
                  "July": "summer", "August": "summer", "September": "autumn",
                  "October": "autumn", "November": "autumn", "December": "winter"}
        mode = random.randrange(3)
        if mode == 0:
            i = random.randrange(4)
            return _num_q("The four seasons of the year in order are spring, summer, "
                          "autumn and winter. Which season comes straight after %s? "
                          "(type the season)" % seasons[i],
                          seasons[(i + 1) % 4], "str", text=True,
                          placeholder="spring / summer / autumn / winter",
                          solution=["After %s comes %s." % (seasons[i], seasons[(i + 1) % 4])])
        if mode == 1:
            mth = pick(list(months.keys()))
            return _num_q("In the UK, which season is the month of %s in — spring, summer, "
                          "autumn or winter? (type the season)" % mth,
                          months[mth], "str", text=True,
                          placeholder="spring / summer / autumn / winter",
                          solution=["%s falls in %s." % (mth, months[mth])])
        season = pick(seasons)
        cnt = sum(1 for m in months if months[m] == season)
        return _num_q("There are 12 months in a year and they are shared between the four "
                      "seasons. How many months are there in %s?" % season,
                      cnt, "int", unit="months",
                      solution=["12 months ÷ 4 seasons = 3 months each.",
                                "%s has %d months." % (season.capitalize(), cnt)])

    # whole hours on a clock (visual): 1 hour = 60 minutes
    h = random.randint(1, 12)
    m = pick(_by_d(d, [0, 30], [0, 15, 30, 45], [0, 15, 30, 45]))
    hours = random.randint(1, _by_d(d, 2, 3, 5))
    eh = ((h - 1 + hours) % 12) + 1
    return {"prompt": "A film starts at %s and lasts exactly %d %s "
                      "(remember 1 hour = 60 minutes). Set the clock to the finish time."
                      % (_hm(h, m), hours, "hour" if hours == 1 else "hours"),
            "component": "clock", "spec": {"mode": "set"},
            "answer": _hm(eh, m), "answer_type": "time",
            "solution": ["%s later, the minutes stay the same." % _pl(hours, "whole hour"),
                         "%s + %s = %s." % (_hm(h, m), _pl(hours, "hour"), _hm(eh, m))]}


_SHAPES_2D = [("triangle", 3), ("square", 4), ("rectangle", 4), ("pentagon", 5),
              ("hexagon", 6), ("heptagon", 7), ("octagon", 8)]


@skill("Y3.8.g", "2-D shapes", S8)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [s for s in _SHAPES_2D if s[1] <= 5], _SHAPES_2D, _SHAPES_2D)
    name, sides = pick(pool)
    t = _pick_t([2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1])

    if t == 0:                                          # count sides (visual)
        return {"prompt": "How many sides does this shape have?",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": sides, "answer_type": "int",
                "solution": ["Count the straight sides of the %s." % name,
                             "%s has %d sides." % (_a(name).capitalize(), sides)]}

    if t == 1:                                          # count vertices (visual)
        return {"prompt": "How many vertices (corners) does this shape have?",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "vertices"},
                "answer": sides, "answer_type": "int",
                "solution": ["Count the corners of the %s." % name,
                             "%s has %d vertices." % (_a(name).capitalize(), sides)]}

    if t == 2:                                          # name the shape (visual)
        nm, sd = pick([s for s in pool if s[0] not in ("square", "rectangle")])
        return {"prompt": "What is the name of this shape?",
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["It has %d straight sides." % sd,
                             "A shape with %d sides is %s." % (sd, _a(nm))]}

    if t == 3:                                          # riddle (typed)
        nm, sd = pick([s for s in _SHAPES_2D if s[0] not in ("square", "rectangle")])
        return _num_q("A 2-D shape has %d straight sides and %d corners. What is it called?"
                      % (sd, sd),
                      nm, "str", text=True, placeholder="shape name",
                      solution=["A shape with %d sides is %s." % (sd, _a(nm))])

    if t == 5:                    # NEW: classify polygons (visual)
        nm, sd = pick([s for s in pool if s[0] not in ("square", "rectangle")])
        return {"prompt": "Classify this polygon. Count its sides — what is the polygon "
                          "called?",
                "component": "shape", "spec": {"kind": "2d", "name": nm, "ask": "name"},
                "answer": nm, "answer_type": "str",
                "solution": ["The polygon has %d straight sides." % sd,
                             "A polygon with %d sides is %s." % (sd, _a(nm))]}

    if t == 6:                    # NEW: two-dimensional shapes in the real world
        thing, nm, sd = pick([
            ("a window pane", "rectangle", 4),
            ("a chess board square", "square", 4),
            ("a road warning sign", "triangle", 3),
            ("a stop sign", "octagon", 8),
            ("a honeycomb cell", "hexagon", 6),
            ("a football's black patch", "pentagon", 5),
        ])
        return _num_q("In the real world, %s is shaped like the two-dimensional shape "
                      "called %s. How many sides does it have?" % (thing, _a(nm)),
                      sd, "int", unit="sides",
                      solution=["%s has %d straight sides." % (_a(nm).capitalize(), sd)])

    if t == 7:                    # NEW: compare sides and vertices
        (n1, s1), (n2, s2) = random.sample(_SHAPES_2D, 2)
        while s1 == s2:
            (n1, s1), (n2, s2) = random.sample(_SHAPES_2D, 2)
        big, bs, small, ss = (n1, s1, n2, s2) if s1 > s2 else (n2, s2, n1, s1)
        return _num_q("Compare the sides and vertices of these two shapes. How many MORE "
                      "vertices does %s have than %s?" % (_a(big), _a(small)),
                      bs - ss, "int", unit="vertices",
                      solution=["%s has %d vertices and %s has %d."
                                % (_a(big).capitalize(), bs, _a(small), ss),
                                "%d − %d = %d." % (bs, ss, bs - ss)])

    if t == 8:                    # NEW: attributes of polygons
        nm, sd = pick([s for s in _SHAPES_2D if s[0] not in ("square", "rectangle")])
        return _num_q("Look at the attributes of a regular polygon: it has %d equal sides "
                      "and all its angles are equal. How many vertices does this polygon "
                      "have?" % sd,
                      sd, "int", unit="vertices",
                      solution=["A polygon has as many vertices as sides.",
                                "%s has %d vertices." % (_a(nm).capitalize(), sd)])

    if t == 9:                    # NEW: sort two-dimensional shapes
        chosen = random.sample(_SHAPES_2D, 4)
        cut = pick([3, 4, 5])
        cnt = sum(1 for _, sd in chosen if sd > cut)
        return _num_q("Sort these two-dimensional shapes by their number of sides: %s. "
                      "How many of them have MORE than %d sides?"
                      % (", ".join(nm for nm, _ in chosen), cut),
                      cnt, "int", unit="shapes",
                      solution=["Sides: %s." % ", ".join("%s %d" % (nm, sd) for nm, sd in chosen),
                                "%d of them have more than %d sides." % (cnt, cut)])

    if t == 10:                   # NEW: sort shapes into a Venn diagram
        table = [("square", 4, True), ("rectangle", 4, False),
                 ("rhombus", 4, True), ("equilateral triangle", 3, True),
                 ("regular pentagon", 5, True), ("regular hexagon", 6, True),
                 ("kite", 4, False)]
        chosen = random.sample(table, 5)
        overlap = sum(1 for _, sd, eq in chosen if sd == 4 and eq)
        return _num_q("Sort these shapes into a Venn diagram. One ring is 'has 4 sides' "
                      "and the other ring is 'all sides equal'. Shapes: %s. How many "
                      "shapes belong in the overlap of the two rings?"
                      % ", ".join(nm for nm, _, _ in chosen),
                      overlap, "int", unit="shapes",
                      solution=["The overlap holds shapes with 4 sides AND all sides equal.",
                                "%s." % (", ".join(nm for nm, sd, eq in chosen
                                                   if sd == 4 and eq) or "None of them"),
                                "That is %s." % _pl(overlap, "shape")])

    # right angles (visual, real-life)
    return {"prompt": "This shape has square corners. How many sides does it have?",
            "component": "shape",
            "spec": {"kind": "2d", "name": pick(["square", "rectangle"]), "ask": "sides",
                     "marks": "right_angle"},
            "answer": 4, "answer_type": "int",
            "solution": ["A shape with 4 square (right-angled) corners has 4 sides."]}


_SOLIDS = [("cube", 6, 12, 8), ("cuboid", 6, 12, 8),
           ("square-based pyramid", 5, 8, 5), ("triangular prism", 5, 9, 6)]


@skill("Y3.8.h", "3-D shapes", S8)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [s for s in _SOLIDS if s[0] in ("cube", "cuboid")], _SOLIDS, _SOLIDS)
    name, f, e, v = pick(pool)
    t = _pick_t([2, 2, 2, 2, 1, 1, 1, 1, 1, 1])

    if t == 0:                                          # faces (visual)
        return {"prompt": "How many faces does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "faces"},
                "answer": f, "answer_type": "int",
                "solution": ["Count the flat surfaces of the %s." % name,
                             "%s has %d faces." % (_a(name).capitalize(), f)]}

    if t == 1:                                          # edges (visual)
        return {"prompt": "How many edges does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "edges"},
                "answer": e, "answer_type": "int",
                "solution": ["An edge is where two faces meet.",
                             "%s has %d edges." % (_a(name).capitalize(), e)]}

    if t == 2:                                          # vertices (visual)
        return {"prompt": "How many vertices (corners) does this solid have?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "vertices"},
                "answer": v, "answer_type": "int",
                "solution": ["A vertex is a corner where edges meet.",
                             "%s has %d vertices." % (_a(name).capitalize(), v)]}

    if t == 3:                                          # name it (visual)
        return {"prompt": "What is the name of this solid?",
                "component": "shape", "spec": {"kind": "3d", "name": name, "ask": "name"},
                "answer": name, "answer_type": "str",
                "solution": ["It has %d faces, %d edges and %d vertices." % (f, e, v),
                             "It is a %s." % name]}

    if t == 5:                    # NEW: select the three-dimensional shape
        a, b = random.sample(_SOLIDS, 2)
        while a[1] == b[1]:
            a, b = random.sample(_SOLIDS, 2)
        want = pick([a, b])
        first, second = (a, b) if random.random() < 0.5 else (b, a)
        return _num_q("Select the three-dimensional shape with %d faces: %s or %s? "
                      "(type the name of the solid)" % (want[1], first[0], second[0]),
                      want[0], "str", text=True, placeholder="solid name",
                      solution=["%s has %d faces and %s has %d."
                                % (_a(a[0]).capitalize(), a[1], _a(b[0]), b[1]),
                                "The solid with %d faces is %s." % (want[1], _a(want[0]))])

    if t == 6:                    # NEW: identify shapes traced from solids
        solid, face, traced = pick([
            ("cube", "one face", "square"),
            ("cuboid", "the flat base", "rectangle"),
            ("square-based pyramid", "the base", "square"),
            ("triangular prism", "one end face", "triangle"),
            ("cylinder", "one flat end", "circle"),
            ("cone", "the flat end", "circle"),
        ])
        return _num_q("A pencil is drawn around %s of a %s to trace it onto paper. "
                      "Which two-dimensional shape is traced? (type the shape)"
                      % (face, solid),
                      traced, "str", text=True, placeholder="shape name",
                      solution=["%s of %s is %s."
                                % (face.capitalize(), _a(solid), _a(traced)),
                                "So the traced shape is %s." % _a(traced)])

    if t == 7:                    # NEW: sort three-dimensional shapes
        chosen = random.sample(_SOLIDS, 3)
        cnt = sum(1 for s in chosen if s[1] == 6)
        return _num_q("Sort these three-dimensional shapes into two groups: solids with 6 "
                      "faces and solids without 6 faces. Solids: %s. How many of them have "
                      "6 faces?" % ", ".join(s[0] for s in chosen),
                      cnt, "int", unit="solids",
                      solution=["Faces: %s." % ", ".join("%s %d" % (s[0], s[1]) for s in chosen),
                                "%d of the solids have 6 faces." % cnt])

    if t == 8:                    # NEW: 3-D shapes in the real world I (name the solid)
        thing, solid = pick([
            ("a dice", "cube"), ("a cereal box", "cuboid"), ("a tin of beans", "cylinder"),
            ("a party hat", "cone"), ("a football", "sphere"),
            ("a tent with triangular ends", "triangular prism"),
            ("an Egyptian pyramid", "square-based pyramid"),
        ])
        return _num_q("In the real world, %s is shaped like which three-dimensional solid? "
                      "(type the name of the solid)" % thing,
                      solid, "str", text=True, placeholder="solid name",
                      solution=["%s is shaped like %s." % (thing.capitalize(), _a(solid))])

    if t == 9:                    # NEW: 3-D shapes in the real world II (count faces)
        thing, solid, ff, ee, vv = pick([
            ("a dice", "cube", 6, 12, 8),
            ("a cereal box", "cuboid", 6, 12, 8),
            ("a tent with triangular ends", "triangular prism", 5, 9, 6),
            ("an Egyptian pyramid", "square-based pyramid", 5, 8, 5),
        ])
        ask = pick(["faces", "edges", "vertices"])
        val = {"faces": ff, "edges": ee, "vertices": vv}[ask]
        return _num_q("In the real world, %s is shaped like a %s. How many %s does it have?"
                      % (thing, solid, ask),
                      val, "int", unit=ask,
                      solution=["%s has %d faces, %d edges and %d vertices."
                                % (_a(solid).capitalize(), ff, ee, vv),
                                "So it has %d %s." % (val, ask)])

    # riddle / real-life (typed)
    nm, ff, ee, vv = pick(pool)
    extra = {"cube": " All of its faces are squares of the same size.",
             "cuboid": " Its faces are rectangles, and they are not all the same size."}.get(nm, "")
    return _num_q("A solid has %d faces, %d edges and %d vertices.%s What is it called?"
                  % (ff, ee, vv, extra),
                  nm, "str", text=True, placeholder="solid name",
                  solution=["%d faces, %d edges and %d vertices describe a %s."
                            % (ff, ee, vv, nm)])


@skill("Y3.8.i", "Angles as turns / right angles", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 2, 1, 2, 1])

    if t == 0:                                          # right angles in a turn
        turns, ra = pick([("a quarter", 1), ("a half", 2), ("a three-quarter", 3),
                          ("a full", 4)])
        return _num_q("How many right angles are there in %s turn?" % turns,
                      ra, "int", unit="right angles",
                      solution=["A full turn is 4 right angles.",
                                "%s turn = %s." % (turns.capitalize(), _pl(ra, "right angle"))])

    if t == 1:                                          # clock turn (visual)
        h = random.randint(1, 12)
        quarters = pick(_by_d(d, [1, 2], [1, 2, 3], [1, 2, 3]))
        mins = 15 * quarters
        return {"prompt": "The clock shows %d o'clock. The minute hand makes %s turn "
                          "clockwise. Set the clock to the new time."
                          % (h, {1: "a quarter", 2: "a half", 3: "a three-quarter"}[quarters]),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, mins), "answer_type": "time",
                "solution": ["A quarter turn of the minute hand is 15 minutes.",
                             "%d × 15 = %d minutes, so the time is %s."
                             % (quarters, mins, _hm(h, mins))]}

    if t == 2:                                          # compass turns (real life)
        dirs = ["North", "East", "South", "West"]
        i = random.randrange(4)
        j = (i + random.randint(1, 3)) % 4
        ra = (j - i) % 4
        return _num_q("You face %s and turn clockwise to face %s. "
                      "How many right angles have you turned?" % (dirs[i], dirs[j]),
                      ra, "int", unit="right angles",
                      solution=["Each quarter turn between compass points is 1 right angle.",
                                "%s to %s clockwise is %s."
                                % (dirs[i], dirs[j], _pl(ra, "right angle"))])

    if t == 3:                                          # right angles in a shape (visual)
        name = pick(["square", "rectangle"])
        return {"prompt": "Every corner of this shape is a right angle. "
                          "How many right angles does it have?",
                "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "vertices", "marks": "right_angle"},
                "answer": 4, "answer_type": "int",
                "solution": ["%s has 4 corners and each one is a right angle." % _a(name).capitalize()]}

    # missing number
    ra = random.randint(1, 4)
    return _num_q("A turn is made of %s. How many quarter turns is that?"
                  % _pl(ra, "right angle"),
                  ra, "int", unit="quarter turns",
                  solution=["1 right angle = 1 quarter turn.",
                            "So %s = %s." % (_pl(ra, "right angle"),
                                             _pl(ra, "quarter turn"))])


@skill("Y3.8.j", "Compare an angle to a right angle", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t(_by_d(d, [2, 2, 1, 2, 1], [1, 1, 1, 2, 1], [1, 2, 2, 1, 2]))

    if t == 0:                                          # definition
        kind, ans = pick([("smaller than", "acute"), ("larger than", "obtuse")])
        return _num_q("An angle is %s a right angle. Is it acute or obtuse? (type the word)" % kind,
                      ans, "str", text=True, placeholder="acute / obtuse",
                      solution=["An angle %s a right angle is called %s." % (kind, ans)])

    if t == 1:                                          # clock hands (real life)
        cases = _by_d(d, [(1, "acute"), (3, "right"), (5, "obtuse"), (9, "right")],
                      [(1, "acute"), (2, "acute"), (3, "right"), (4, "obtuse"), (5, "obtuse"), (9, "right")],
                      [(2, "acute"), (4, "obtuse"), (7, "obtuse"), (8, "obtuse"), (10, "acute"), (11, "acute")])
        h, ans = pick(cases)
        return _num_q("At %d o'clock, the hands of a clock make an angle. "
                      "Is it acute, right or obtuse? (type the word)" % h,
                      ans, "str", text=True, placeholder="acute / right / obtuse",
                      solution=["At 3 o'clock and 9 o'clock the hands make a right angle.",
                                "At %d o'clock the angle is %s." % (h, ans)])

    if t == 2:                                          # turns
        turns, ans = pick([("less than a quarter", "acute"), ("exactly a quarter", "right"),
                           ("between a quarter and a half", "obtuse")])
        return _num_q("A turn is %s of a full turn. Is the angle acute, right or obtuse? "
                      "(type the word)" % turns,
                      ans, "str", text=True, placeholder="acute / right / obtuse",
                      solution=["A quarter turn is exactly a right angle.",
                                "%s means the angle is %s." % (turns.capitalize(), ans)])

    if t == 3:                                          # right angles in shapes (visual)
        name, ra = pick([("square", 4), ("rectangle", 4)])
        return {"prompt": "How many corners of this shape are right angles? "
                          "(count the vertices — they are all square corners)",
                "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "vertices", "marks": "right_angle"},
                "answer": ra, "answer_type": "int",
                "solution": ["%s has %d corners and all of them are right angles."
                             % (_a(name).capitalize(), ra)]}

    # counting acute/obtuse in a set
    acute = random.randint(1, 4)
    obtuse = random.randint(1, 4)
    if d == 2:                                          # stretch: right angles are in the set too
        right = random.randint(1, 3)
        big = random.random() < 0.5
        return _num_q("A set of angles has %s smaller than a right angle, %s that are exactly right angles and "
                      "%s larger than a right angle. How many of the angles are %s?"
                      % (_pl(acute, "angle"), _pl(right, "angle"), _pl(obtuse, "angle"),
                         "obtuse" if big else "not acute"),
                      obtuse if big else right + obtuse, "int", unit="angles",
                      solution=["Obtuse angles are larger than a right angle." if big else
                                "Angles that are not acute are right angles or obtuse angles.",
                                "There are %d of them." % (obtuse if big else right + obtuse)])
    return _num_q("A set of angles has %s smaller than a right angle and "
                  "%s larger than a right angle. How many acute angles are there?"
                  % (_pl(acute, "angle"), _pl(obtuse, "angle")),
                  acute, "int", unit="angles",
                  solution=["Acute angles are smaller than a right angle.",
                            "There are %d of them." % acute])


@skill("Y3.8.k", "Parallel and perpendicular lines", S8)
def _(d=1):
    d = _tier(d)
    t = _pick_t(_by_d(d, [2, 2, 2, 2, 1, 0], [1, 1, 1, 2, 1, 2], [0, 0, 2, 1, 2, 3]))

    if t == 0:                                          # definition: parallel
        return _num_q("Two straight lines never meet, no matter how far they go. "
                      "What are they called? (type the word)",
                      "parallel", "str", text=True, placeholder="type the word",
                      solution=["Lines that never meet and stay the same distance apart "
                                "are parallel."])

    if t == 1:                                          # definition: perpendicular
        return _num_q("Two straight lines meet at a right angle. "
                      "What are they called? (type the word)",
                      "perpendicular", "str", text=True, placeholder="type the word",
                      solution=["Lines that meet at a right angle are perpendicular."])

    if t == 2:                                          # real life
        cases = [("the two long rails of a ladder", "parallel"),
                 ("the two lines in the letter L", "perpendicular"),
                 ("the two edges of a straight road", "parallel"),
                 ("the two sides that meet at a corner of a picture frame", "perpendicular"),
                 ("railway tracks", "parallel")]
        if d == 2:                                      # stretch: less familiar cases
            cases = [("the clock hands at 3 o'clock", "perpendicular"),
                     ("the top edge and the bottom edge of a door", "parallel"),
                     ("the two lines that make a plus sign +", "perpendicular"),
                     ("the lines on a page of lined paper", "parallel"),
                     ("the top edge and the side edge of a book cover", "perpendicular"),
                     ("the two lines in the letter H that go up and down", "parallel")]
        case, ans = pick(cases)
        return _num_q("Are %s parallel or perpendicular? (type the word)" % case,
                      ans, "str", text=True, placeholder="parallel / perpendicular",
                      solution=["%s are %s." % (case.capitalize(), ans)])

    if t == 3:                                          # counting in a shape (visual)
        name, pairs = pick([("square", 2), ("rectangle", 2), ("hexagon", 3)])
        return {"prompt": "How many sides does this shape have? "
                          "(In this shape, opposite sides are parallel.)",
                "component": "shape", "spec": {"kind": "2d", "name": name, "ask": "sides"},
                "answer": pairs * 2, "answer_type": "int",
                "solution": ["It has %d pairs of parallel sides." % pairs,
                             "%d × 2 = %d sides." % (pairs, pairs * 2)]}

    if t == 5:                    # NEW: attributes of quadrilaterals
        mode = random.randrange(2)
        if mode == 0:
            attrs, quad = pick([
                ("4 equal sides and 4 right angles", "square"),
                ("4 right angles, with opposite sides equal but not all four sides equal",
                 "rectangle"),
                ("4 equal sides but no right angles", "rhombus"),
                ("exactly one pair of parallel sides", "trapezium"),
            ])
            return _num_q("Look at the attributes of these quadrilaterals. Which "
                          "quadrilateral has %s — square, rectangle, rhombus or "
                          "trapezium? (type the name)" % attrs,
                          quad, "str", text=True,
                          placeholder="square / rectangle / rhombus / trapezium",
                          solution=["%s has %s." % (_a(quad).capitalize(), attrs)])
        quad, pairs = pick([("square", 2), ("rectangle", 2), ("rhombus", 2),
                            ("trapezium", 1)])
        return _num_q("A %s is a quadrilateral, so it has 4 sides. How many pairs of "
                      "parallel sides does it have?" % quad,
                      pairs, "int", unit="pairs",
                      solution=["%s has %s of parallel sides."
                                % (_a(quad).capitalize(), _pl(pairs, "pair"))])

    # counting pairs
    name, pairs = pick(_by_d(d, [("square", 2), ("rectangle", 2)],
                             [("square", 2), ("rectangle", 2), ("regular hexagon", 3), ("regular octagon", 4)],
                             [("regular hexagon", 3), ("regular octagon", 4), ("rectangle", 2)]))
    return _num_q("How many pairs of parallel sides does a %s have?" % name,
                  pairs, "int", unit="pairs",
                  solution=["Opposite sides of a %s are parallel." % name,
                            "There are %d pairs." % pairs])


# names must match the shape component's 2-D vocabulary; every polygon it draws
# (other than the rectangle) is regular, so lines of symmetry = number of sides.
_SYMMETRY = [("square", 4), ("rectangle", 2), ("triangle", 3), ("pentagon", 5),
             ("hexagon", 6), ("heptagon", 7), ("octagon", 8)]
_SYM_LABEL = {"square": "square", "rectangle": "rectangle",
              "triangle": "equilateral triangle", "pentagon": "regular pentagon",
              "hexagon": "regular hexagon", "heptagon": "regular heptagon",
              "octagon": "regular octagon"}


@skill("Y3.8.l", "Lines of symmetry", S8)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [s for s in _SYMMETRY if s[1] <= 4], _SYMMETRY, _SYMMETRY)
    name, lines = pick(pool)
    t = _pick_t([2, 2, 1, 1, 1, 2])

    if t == 0:                                          # visual
        return {"prompt": "How many lines of symmetry does this shape have?",
                "component": "shape",
                "spec": {"kind": "2d", "name": name, "ask": "lines_of_symmetry"},
                "answer": lines, "answer_type": "int",
                "solution": ["Look for every fold line that makes the two halves match.",
                             "%s has %s of symmetry." % (_a(_SYM_LABEL[name]).capitalize(), _pl(lines, "line"))]}

    if t == 1:                                          # visual, different shape
        nm, ln = pick([s for s in pool if s[0] != name] or pool)
        return {"prompt": "Count the lines of symmetry of this shape.",
                "component": "shape",
                "spec": {"kind": "2d", "name": nm, "ask": "lines_of_symmetry"},
                "answer": ln, "answer_type": "int",
                "solution": ["%s has %s of symmetry." % (_a(_SYM_LABEL[nm]).capitalize(), _pl(ln, "line"))]}

    if t == 2:                                          # bare recall
        return _num_q("How many lines of symmetry does %s have?" % _a(_SYM_LABEL[name]),
                      lines, "int", unit="lines",
                      solution=["%s has %s of symmetry." % (_a(_SYM_LABEL[name]).capitalize(), _pl(lines, "line"))])

    if t == 3:                                          # riddle (regular shapes)
        sides = pick(_by_d(d, [3, 4], [3, 4, 5, 6], [3, 4, 5, 6, 8]))
        return _num_q("A regular shape has %d equal sides. How many lines of symmetry "
                      "does it have?" % sides,
                      sides, "int", unit="lines",
                      solution=["A regular shape has as many lines of symmetry as sides.",
                                "So it has %d lines of symmetry." % sides])

    if t == 5:                    # NEW: flip, turn and slide
        move, describe = pick([
            ("flip", "makes a mirror image of the shape over a mirror line"),
            ("slide", "moves the shape along without turning it or flipping it"),
            ("turn", "rotates the shape around a point"),
        ])
        return _num_q("Flip, turn and slide are three ways of moving a shape. Which move "
                      "%s — flip, turn or slide? (type the word)" % describe,
                      move, "str", text=True, placeholder="flip / turn / slide",
                      solution=["The move that %s is a %s." % (describe, move)])

    # comparison
    (n1, l1), (n2, l2) = random.sample(pool, 2) if len(pool) > 1 else (pool[0], pool[0])
    return _num_q("%s and %s. How many lines of symmetry do they have altogether?"
                  % (_a(_SYM_LABEL[n1]).capitalize(), _a(_SYM_LABEL[n2])),
                  l1 + l2, "int", unit="lines",
                  solution=["%s has %d and %s has %d."
                            % (_a(_SYM_LABEL[n1]).capitalize(), l1, _a(_SYM_LABEL[n2]), l2),
                            "%d + %d = %d." % (l1, l2, l1 + l2)])


# ------------------------------------------------------------------ 3.9 ------
@skill("Y3.9.a", "Interpret a pictogram", S9)
def _(d=1):
    d = _tier(d)
    key = pick(_by_d(d, [2], [2, 5, 10], [2, 5, 10]))
    symbol = pick(["circle", "star", "apple"])
    cats = random.sample(["Apples", "Pears", "Plums", "Oranges", "Bananas"], 4)
    vals = [key * random.randint(1, _by_d(d, 5, 7, 9)) for _ in cats]
    while len(set(vals)) != len(vals):
        vals = [key * random.randint(1, _by_d(d, 5, 7, 9)) for _ in cats]
    spec = {"categories": cats, "values": vals, "key": key, "symbol": symbol}
    i, j = random.sample(range(len(cats)), 2)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                          # read one row
        return {"prompt": "Use the pictogram. How many %s are there?" % cats[i].lower(),
                "component": "pictogram", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["Each symbol stands for %d." % key,
                             "%s has %s: %d × %d = %d."
                             % (cats[i], _pl(vals[i] // key, "symbol"), vals[i] // key, key, vals[i])]}

    if t == 1:                                          # count the symbols
        return {"prompt": "Use the pictogram. How many symbols are drawn in the %s row?"
                          % cats[i].lower(),
                "component": "pictogram", "spec": spec,
                "answer": vals[i] // key, "answer_type": "int",
                "solution": ["%s is %d and each symbol stands for %d." % (cats[i], vals[i], key),
                             "%d ÷ %d = %s." % (vals[i], key, _pl(vals[i] // key, "symbol"))]}

    if t == 2:                                          # total of two rows
        return {"prompt": "Use the pictogram. How many %s and %s are there altogether?"
                          % (cats[i].lower(), cats[j].lower()),
                "component": "pictogram", "spec": spec,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%s = %d and %s = %d." % (cats[i], vals[i], cats[j], vals[j]),
                             "%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    if t == 3:                                          # difference
        hi, lo = max(vals[i], vals[j]), min(vals[i], vals[j])
        big = cats[i] if vals[i] > vals[j] else cats[j]
        small = cats[j] if vals[i] > vals[j] else cats[i]
        return {"prompt": "Use the pictogram. How many MORE %s than %s are there?"
                          % (big.lower(), small.lower()),
                "component": "pictogram", "spec": spec,
                "answer": hi - lo, "answer_type": "int",
                "solution": ["%s = %d and %s = %d." % (big, hi, small, lo),
                             "%d − %d = %d." % (hi, lo, hi - lo)]}

    if t == 5:                    # NEW: create a pictogram (how many symbols to draw)
        k = random.randrange(len(cats))
        return _num_q("You are going to create a pictogram of this data. The key says one "
                      "symbol stands for %d. There are %d %s. How many symbols would you "
                      "draw in the %s row?"
                      % (key, vals[k], cats[k].lower(), cats[k].lower()),
                      vals[k] // key, "int", unit="symbols",
                      solution=["%d ÷ %d = %d." % (vals[k], key, vals[k] // key),
                                "Draw %s in that row of the pictogram."
                                % _pl(vals[k] // key, "symbol")])

    if t == 6:                    # NEW: create a pictogram (choose a key)
        k = random.randrange(len(cats))
        return _num_q("You are creating a pictogram with a key of one symbol = %d. "
                      "%s draws %s in the %s row. How many %s does that stand for?"
                      % (key, pick(NAMES), _pl(vals[k] // key, "symbol"),
                         cats[k].lower(), cats[k].lower()),
                      vals[k], "int", unit=cats[k].lower(),
                      solution=["%s × %d = %d." % (_pl(vals[k] // key, "symbol"), key, vals[k])])

    # total of everything
    return {"prompt": "Use the pictogram. How many pieces of fruit are there in total?",
            "component": "pictogram", "spec": spec,
            "answer": sum(vals), "answer_type": "int",
            "solution": ["%s." % " + ".join(str(v) for v in vals),
                         "The total is %d." % sum(vals)]}


@skill("Y3.9.b", "Read a bar chart", S9)
def _(d=1):
    d = _tier(d)
    cats, vals = _chart(d)
    spec = {"categories": cats, "values": vals, "mode": "read"}
    i = random.randrange(len(cats))
    t = _pick_t([1, 1, 1, 1, 1])

    if t == 0:
        return {"prompt": "Use the bar chart. How many votes did %s get?" % cats[i],
                "component": "bar_chart", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["The %s bar reaches %d." % (cats[i], vals[i])]}

    if t == 1:                                          # most popular (typed name)
        top = cats[vals.index(max(vals))]
        return {"prompt": "Use the bar chart. Which colour got the MOST votes? (type the name)",
                "component": "bar_chart", "spec": spec,
                "answer": top, "answer_type": "str",
                "solution": ["The tallest bar is %s with %d votes." % (top, max(vals))]}

    if t == 2:                                          # least popular
        bot = cats[vals.index(min(vals))]
        return {"prompt": "Use the bar chart. Which colour got the FEWEST votes? (type the name)",
                "component": "bar_chart", "spec": spec,
                "answer": bot, "answer_type": "str",
                "solution": ["The shortest bar is %s with %d votes." % (bot, min(vals))]}

    if t == 3:                                          # total
        return {"prompt": "Use the bar chart. How many votes were there altogether?",
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s." % " + ".join(str(v) for v in vals),
                             "The total is %d votes." % sum(vals)]}

    # how many more to reach a target
    target = max(vals) + random.randint(1, 5)
    return {"prompt": "Use the bar chart. How many more votes would %s need to reach %d?"
                      % (cats[i], target),
            "component": "bar_chart", "spec": spec,
            "answer": target - vals[i], "answer_type": "int",
            "solution": ["%s has %d votes." % (cats[i], vals[i]),
                         "%d − %d = %d." % (target, vals[i], target - vals[i])]}


@skill("Y3.9.c", "Interpret a table", S9)
def _(d=1):
    d = _tier(d)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    lo, hi = _by_d(d, (2, 8), (3, 15), (5, 25))
    vals = [random.randint(lo, hi) for _ in days]
    while len(set(vals)) != len(vals):
        vals = [random.randint(lo, hi) for _ in days]
    tbl = "; ".join("%s: %d" % (dy, v) for dy, v in zip(days, vals))
    t = _pick_t([1, 1, 1, 2, 2, 1, 1, 1, 1, 1])

    if t == 0:                                          # total from a table
        return _num_q("The table shows books read. %s. How many books were read in total?" % tbl,
                      sum(vals), "int", unit="books",
                      solution=["%s = %s." % (" + ".join(str(v) for v in vals), _pl(sum(vals), "book"))])

    if t == 1:                                          # difference from a table
        i, j = random.sample(range(len(days)), 2)
        return _num_q("The table shows books read. %s. How many MORE books were read on %s "
                      "than on %s?" % (tbl, days[i] if vals[i] > vals[j] else days[j],
                                       days[j] if vals[i] > vals[j] else days[i]),
                      abs(vals[i] - vals[j]), "int", unit="books",
                      solution=["%d − %d = %s."
                                % (max(vals[i], vals[j]), min(vals[i], vals[j]),
                                   _pl(abs(vals[i] - vals[j]), "book"))])

    if t == 2:                                          # missing value
        total = sum(vals)
        hide = random.randrange(len(days))
        shown = "; ".join("%s: %d" % (dy, v) for k, (dy, v) in enumerate(zip(days, vals))
                          if k != hide)
        return _num_q("The table shows books read. %s. The total for all four days is %d. "
                      "How many books were read on %s?" % (shown, total, days[hide]),
                      vals[hide], "int", unit="books",
                      solution=["%d − (%s) = %d."
                                % (total, " + ".join(str(v) for k, v in enumerate(vals) if k != hide),
                                   vals[hide])])

    if t == 3:                                          # table shown as a bar chart (visual)
        spec = {"categories": days, "values": vals, "mode": "read"}
        i = random.randrange(len(days))
        return {"prompt": "The chart shows how many books were read each day. "
                          "How many were read on %s?" % days[i],
                "component": "bar_chart", "spec": spec,
                "answer": vals[i], "answer_type": "int",
                "solution": ["The %s bar reaches %d books." % (days[i], vals[i])]}

    if t == 5:                    # NEW: interpret a tally chart
        fruits = random.sample(["Apples", "Bananas", "Pears", "Plums", "Grapes"], 4)
        counts = [random.randint(3, _by_d(d, 9, 14, 22)) for _ in fruits]
        while len(set(counts)) != len(counts):
            counts = [random.randint(3, _by_d(d, 9, 14, 22)) for _ in fruits]
        chart = "; ".join("%s %s" % (f, _tally(c)) for f, c in zip(fruits, counts))
        k = random.randrange(len(fruits))
        ask_total = random.random() < 0.4
        if ask_total:
            return _num_q("Interpret the tally chart of favourite fruits (a bundle ||||\\ "
                          "stands for 5). %s. How many children voted altogether?" % chart,
                          sum(counts), "int", unit="children",
                          solution=["%s." % " + ".join(str(c) for c in counts),
                                    "The total is %d children." % sum(counts)])
        return _num_q("Interpret the tally chart of favourite fruits (a bundle ||||\\ "
                      "stands for 5). %s. How many children chose %s?"
                      % (chart, fruits[k].lower()),
                      counts[k], "int", unit="children",
                      solution=["%s has %s of 5 and %s."
                                % (fruits[k], _pl(counts[k] // 5, "bundle"), _pl(counts[k] % 5, "extra tally mark")),
                                "That is %d children." % counts[k]])

    if t == 6:                    # NEW: which tally chart is correct?
        n = random.randint(6, _by_d(d, 12, 18, 24))
        wrong = n + pick([-2, -1, 1, 2])
        if wrong < 1:
            wrong = n + 2
        correct_first = random.random() < 0.5
        a_val, b_val = (n, wrong) if correct_first else (wrong, n)
        return _num_q("%d children chose swimming. Which tally chart is correct for %d "
                      "(a bundle ||||\\ stands for 5)? A: %s. B: %s. (type A or B)"
                      % (n, n, _tally(a_val), _tally(b_val)),
                      "A" if correct_first else "B", "str", text=True, placeholder="A / B",
                      solution=["%d = %s of 5 and %s."
                                % (n, _pl(n // 5, "bundle"), _pl(n % 5, "single mark")),
                                "The correct tally chart is %s."
                                % ("A" if correct_first else "B")])

    if t == 7:                    # NEW: interpret data in a table
        k = random.randrange(len(days))
        return _num_q("Interpret the data in this table of books read. %s. On which day "
                      "were exactly %d books read? (type the day)" % (tbl, vals[k]),
                      days[k], "str", text=True, placeholder="a day",
                      solution=["Look down the table for the value %d." % vals[k],
                                "It is on %s." % days[k]])

    if t == 8:                    # NEW: interpret a line plot
        labels = ["0 pets", "1 pet", "2 pets", "3 pets"]
        counts = [random.randint(1, _by_d(d, 4, 6, 8)) for _ in labels]
        while len(set(counts)) != len(counts):
            counts = [random.randint(1, _by_d(d, 4, 6, 8)) for _ in labels]
        plot = _plot_rows(labels, counts)
        k = random.randrange(len(labels))
        if random.random() < 0.4:
            return _num_q("Interpret this line plot. Each x stands for one child. %s. "
                          "How many children were asked altogether?" % plot,
                          sum(counts), "int", unit="children",
                          solution=["%s." % " + ".join(str(c) for c in counts),
                                    "The total is %d children." % sum(counts)])
        return _num_q("Interpret this line plot. Each x stands for one child. %s. "
                      "How many children have %s?" % (plot, labels[k]),
                      counts[k], "int", unit="children",
                      solution=["Count the x marks above '%s'." % labels[k],
                                "There are %d." % counts[k]])

    if t == 9:                    # NEW: create a line plot
        labels = ["4 cm", "5 cm", "6 cm", "7 cm"]
        counts = [random.randint(1, _by_d(d, 4, 6, 8)) for _ in labels]
        data = []
        for lab, c in zip(labels, counts):
            data += [lab.split()[0]] * c
        random.shuffle(data)
        k = random.randrange(len(labels))
        return _num_q("You are creating a line plot of these leaf lengths in centimetres: "
                      "%s. On the line plot, how many x marks go above %s?"
                      % (", ".join(data), labels[k]),
                      counts[k], "int", unit="x marks",
                      solution=["Count how many times %s appears in the data." % labels[k],
                                "It appears %s, so draw %s."
                                % (_pl(counts[k], "time"), _pl(counts[k], "x mark"))])

    # busiest day from a chart (visual)
    spec = {"categories": days, "values": vals, "mode": "read"}
    top = days[vals.index(max(vals))]
    return {"prompt": "The chart shows how many books were read each day. "
                      "On which day were the most books read? (type the day)",
            "component": "bar_chart", "spec": spec,
            "answer": top, "answer_type": "str",
            "solution": ["The tallest bar is %s with %d books." % (top, max(vals))]}


@skill("Y3.9.d", "Two-step question from data", S9)
def _(d=1):
    d = _tier(d)
    cats, vals = _chart(d)
    spec = {"categories": cats, "values": vals, "mode": "read"}
    i, j = random.sample(range(len(cats)), 2)
    t = _pick_t([1, 1, 1, 1, 1])

    if t == 0:                                          # sum of two bars
        return {"prompt": "Use the bar chart. How many votes did %s and %s get altogether?"
                          % (cats[i], cats[j]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] + vals[j], "answer_type": "int",
                "solution": ["%d + %d = %d." % (vals[i], vals[j], vals[i] + vals[j])]}

    if t == 1:                                          # total minus one
        return {"prompt": "Use the bar chart. How many votes were there altogether, "
                          "NOT counting %s?" % cats[i],
                "component": "bar_chart", "spec": spec,
                "answer": sum(vals) - vals[i], "answer_type": "int",
                "solution": ["Total = %d." % sum(vals),
                             "%d − %d = %d." % (sum(vals), vals[i], sum(vals) - vals[i])]}

    if t == 2:                                          # doubling
        return {"prompt": "Use the bar chart. If the votes for %s were doubled, "
                          "how many votes would it have?" % cats[i],
                "component": "bar_chart", "spec": spec,
                "answer": vals[i] * 2, "answer_type": "int",
                "solution": ["%s has %d votes." % (cats[i], vals[i]),
                             "%d × 2 = %d." % (vals[i], vals[i] * 2)]}

    if t == 3:                                          # sum of two then compare
        # the two largest against the smallest, so the answer is always positive
        order = sorted(range(len(cats)), key=lambda x: vals[x])
        k = order[0]
        a, b = order[-1], order[-2]
        return {"prompt": "Use the bar chart. How many more votes did %s and %s get "
                          "together than %s?" % (cats[a], cats[b], cats[k]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[a] + vals[b] - vals[k], "answer_type": "int",
                "solution": ["%d + %d = %d." % (vals[a], vals[b], vals[a] + vals[b]),
                             "%d − %d = %d." % (vals[a] + vals[b], vals[k],
                                                vals[a] + vals[b] - vals[k])]}

    # real-life two-step: extra votes arrive
    extra = random.randint(2, 9)
    return {"prompt": "Use the bar chart. %d more children vote for %s. "
                      "How many votes do %s and %s then have altogether?"
                      % (extra, cats[i], cats[i], cats[j]),
            "component": "bar_chart", "spec": spec,
            "answer": vals[i] + extra + vals[j], "answer_type": "int",
            "solution": ["%s now has %d + %d = %d votes." % (cats[i], vals[i], extra,
                                                             vals[i] + extra),
                         "%d + %d = %d." % (vals[i] + extra, vals[j],
                                            vals[i] + extra + vals[j])]}


@skill("Y3.9.e", "Comparison question from data", S9)
def _(d=1):
    d = _tier(d)
    cats, vals = _chart(d)
    spec = {"categories": cats, "values": vals, "mode": "read"}
    hi_i = vals.index(max(vals))
    lo_i = vals.index(min(vals))
    i, j = random.sample(range(len(cats)), 2)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1])

    if t == 0:                                          # most vs least
        return {"prompt": "Use the bar chart. How many MORE votes did %s get than %s?"
                          % (cats[hi_i], cats[lo_i]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[hi_i] - vals[lo_i], "answer_type": "int",
                "solution": ["%d − %d = %d." % (vals[hi_i], vals[lo_i],
                                                vals[hi_i] - vals[lo_i])]}

    if t == 1:                                          # two named bars
        big, small = (i, j) if vals[i] > vals[j] else (j, i)
        return {"prompt": "Use the bar chart. How many FEWER votes did %s get than %s?"
                          % (cats[small], cats[big]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[big] - vals[small], "answer_type": "int",
                "solution": ["%d − %d = %d." % (vals[big], vals[small],
                                                vals[big] - vals[small])]}

    if t == 2:                                          # catch up
        big, small = (i, j) if vals[i] > vals[j] else (j, i)
        return {"prompt": "Use the bar chart. How many more votes does %s need to have "
                          "the same as %s?" % (cats[small], cats[big]),
                "component": "bar_chart", "spec": spec,
                "answer": vals[big] - vals[small], "answer_type": "int",
                "solution": ["%s has %d and %s has %d." % (cats[big], vals[big],
                                                           cats[small], vals[small]),
                             "%d − %d = %d." % (vals[big], vals[small],
                                                vals[big] - vals[small])]}

    if t == 3:                                          # range
        return {"prompt": "Use the bar chart. What is the difference between the tallest "
                          "and the shortest bar?",
                "component": "bar_chart", "spec": spec,
                "answer": max(vals) - min(vals), "answer_type": "int",
                "solution": ["Tallest = %d, shortest = %d." % (max(vals), min(vals)),
                             "%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))]}

    if t == 5:                    # NEW: interpret a line graph
        hours = ["9 am", "10 am", "11 am", "12 noon", "1 pm"]
        temps = [random.randint(8, 14)]
        for _ in range(4):
            temps.append(temps[-1] + random.randint(1, _by_d(d, 3, 5, 7)))
        graph = "; ".join("%s %d°C" % (hh, tt) for hh, tt in zip(hours, temps))
        a, b = sorted(random.sample(range(5), 2))
        lg = {"points": [[hh, tt] for hh, tt in zip(hours, temps)], "yLabel": "°C", "xLabel": "Time"}
        if random.random() < 0.35:
            return dict(_num_q("The line graph shows the temperature each hour. %s. Interpret "
                          "the line graph: what was the temperature at %s, in °C?"
                          % (graph, hours[b]),
                          temps[b], "int", unit="°C",
                          solution=["Read the point on the line graph above %s." % hours[b],
                                    "The temperature was %d°C." % temps[b]]),
                        component="line_graph", spec=lg)
        return dict(_num_q("The line graph shows the temperature each hour. %s. Interpret the "
                      "line graph: by how many degrees did the temperature rise from %s "
                      "to %s?" % (graph, hours[a], hours[b]),
                      temps[b] - temps[a], "int", unit="°C",
                      solution=["%d°C at %s and %d°C at %s."
                                % (temps[a], hours[a], temps[b], hours[b]),
                                "%d − %d = %d°C." % (temps[b], temps[a],
                                                     temps[b] - temps[a])]),
                    component="line_graph", spec=lg)

    if t == 6:                    # NEW: which line graph is correct?
        start = random.randint(2, 6)
        step = random.randint(1, 4)
        weeks = [start + k * step for k in range(4)]
        rising = random.random() < 0.5
        shown = weeks if rising else weeks[::-1]
        tbl = "; ".join("week %d: %d cm" % (k + 1, v) for k, v in enumerate(shown))
        a_rises = random.random() < 0.5
        desc_a = "goes up from %d cm to %d cm" % (min(weeks), max(weeks)) if a_rises \
                 else "goes down from %d cm to %d cm" % (max(weeks), min(weeks))
        desc_b = "goes down from %d cm to %d cm" % (max(weeks), min(weeks)) if a_rises \
                 else "goes up from %d cm to %d cm" % (min(weeks), max(weeks))
        correct = "A" if (a_rises == rising) else "B"
        return _num_q("The table shows the height of a plant. %s. Which line graph is "
                      "correct for this data? Graph A %s. Graph B %s. (type A or B)"
                      % (tbl, desc_a, desc_b),
                      correct, "str", text=True, placeholder="A / B",
                      solution=["The plant height %s over the four weeks."
                                % ("rises" if rising else "falls"),
                                "So graph %s is the correct line graph." % correct])

    # half / double comparison
    return {"prompt": "Use the bar chart. How many votes would %s and %s have together "
                      "if %s doubled its votes?" % (cats[i], cats[j], cats[i]),
            "component": "bar_chart", "spec": spec,
            "answer": vals[i] * 2 + vals[j], "answer_type": "int",
            "solution": ["%d × 2 = %d." % (vals[i], vals[i] * 2),
                         "%d + %d = %d." % (vals[i] * 2, vals[j], vals[i] * 2 + vals[j])]}


@skill("Y3.9.f", "Likelihood (enrichment)", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 2, 2, 1, 2])

    if t == 0:                                          # classic
        case, ans = pick([
            ("You roll a normal dice and get a number less than 7", "certain"),
            ("You roll a normal dice and get a 7", "impossible"),
            ("It will rain tomorrow", "possible"),
            ("A coin lands on heads", "possible"),
            ("Tomorrow is a day of the week", "certain"),
            ("A cat will fly to the moon today", "impossible"),
        ])
        return _num_q("%s. Is this certain, possible or impossible? (type the word)" % case,
                      ans, "str", text=True,
                      placeholder="certain / possible / impossible",
                      solution=["This event is %s." % ans])

    if t == 1:                                          # counting outcomes on a dice
        case, ans, why = pick([
            ("an even number", 3, "2, 4 and 6 are even"),
            ("an odd number", 3, "1, 3 and 5 are odd"),
            ("a number bigger than 4", 2, "5 and 6 are bigger than 4"),
            ("a number less than 3", 2, "1 and 2 are less than 3"),
        ])
        return _num_q("A normal dice is rolled. How many of the six faces show %s?" % case,
                      ans, "int", unit="faces",
                      solution=["%s." % why, "That is %d faces." % ans])

    if t == 2:                                          # counters pictogram (visual)
        cats = ["Red", "Blue", "Green"]
        vals = [random.randint(2, _by_d(d, 6, 9, 12)) for _ in cats]
        while len(set(vals)) != len(vals):
            vals = [random.randint(2, _by_d(d, 6, 9, 12)) for _ in cats]
        return {"prompt": "The pictogram shows the counters in a bag. "
                          "How many counters are in the bag altogether?",
                "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": sum(vals), "answer_type": "int",
                "solution": ["Each symbol is 1 counter.",
                             "%s = %d counters." % (" + ".join(str(v) for v in vals),
                                                    sum(vals))]}

    if t == 3:                                          # more likely (visual, typed colour)
        cats = ["Red", "Blue", "Green"]
        vals = random.sample(range(2, _by_d(d, 8, 12, 16)), 3)
        top = cats[vals.index(max(vals))]
        return {"prompt": "The pictogram shows the counters in a bag. You take one counter "
                          "without looking. Which colour are you MOST likely to get? "
                          "(type the colour)",
                "component": "pictogram",
                "spec": {"categories": cats, "values": vals, "key": 1, "symbol": "circle"},
                "answer": top, "answer_type": "str",
                "solution": ["There are more %s counters (%d) than any other colour."
                             % (top.lower(), max(vals)),
                             "So %s is the most likely." % top.lower()]}

    if t == 5:                    # NEW: combinations
        who = pick(NAMES)
        (an, aw), (bn, bw) = random.sample([
            ("T-shirts", "T-shirt"), ("pairs of shorts", "pair of shorts"),
            ("hats", "hat"), ("scarves", "scarf"), ("pairs of socks", "pair of socks"),
        ], 2)
        a = random.randint(2, _by_d(d, 3, 5, 8))
        b = random.randint(2, _by_d(d, 3, 5, 8))
        return _num_q("%s has %d %s and %d %s. %s wears one %s with one %s. "
                      "How many different combinations can %s make?"
                      % (who, a, an, b, bn, who, aw, bw, who),
                      a * b, "int", unit="combinations",
                      solution=["Each of the %d %s can go with any of the %d %s."
                                % (a, an, b, bn),
                                "%d × %d = %d combinations." % (a, b, a * b)])

    # impossible / certain from a bag
    red = random.randint(3, 10)
    return _num_q("A bag has %d red counters and no other colours. You take one counter. "
                  "Is getting a red counter certain, possible or impossible? (type the word)"
                  % red,
                  "certain", "str", text=True, placeholder="certain / possible / impossible",
                  solution=["Every counter in the bag is red, so a red counter is certain."])


@skill("Y3.9.g", "Money and budgeting (enrichment)", S9)
def _(d=1):
    d = _tier(d)
    budget = pick(_by_d(d, [200, 500], [500, 1000], [1000, 2000]))
    t = _pick_t([2, 1, 1, 1, 2, 2, 2])

    if t == 0:                                          # budget against a price chart
        names = random.sample(["Pen", "Book", "Ruler", "Bag"], 3)
        prices = [random.randint(20, budget // 3) for _ in names]
        i, j = random.sample(range(3), 2)
        return {"prompt": "The chart shows prices in pence. You have %s and buy the %s "
                          "and the %s. How much is left, in pence?"
                          % (money(budget), names[i].lower(), names[j].lower()),
                "component": "bar_chart",
                "spec": {"categories": names, "values": prices, "mode": "read"},
                "answer": budget - prices[i] - prices[j], "answer_type": "int",
                "solution": ["%d + %d = %d p spent."
                             % (prices[i], prices[j], prices[i] + prices[j]),
                             "%d − %d = %d p left."
                             % (budget, prices[i] + prices[j],
                                budget - prices[i] - prices[j])]}

    if t == 1:                                          # how many can you buy
        price = pick([20, 25, 50, 100])
        count = budget // price
        return _num_q("Stickers cost %s each. How many can you buy with %s?"
                      % (money(price), money(budget)),
                      count, "int", unit="stickers",
                      solution=["%d ÷ %d = %d." % (budget, price, count)])

    if t == 2:                                          # saving up
        cost = budget + random.randint(50, 400)
        have = random.randint(50, budget)
        return _num_q("A book costs %s. %s has saved %s. How much more is needed, in pence?"
                      % (money(cost), pick(NAMES), money(have)),
                      cost - have, "int", unit="p",
                      solution=["%d − %d = %d p." % (cost, have, cost - have),
                                "That is %s." % money(cost - have)])

    if t == 3:                                          # weekly saving (multi-step)
        per = pick([50, 100, 150, 200])
        weeks = random.randint(3, _by_d(d, 4, 6, 9))
        who = pick(NAMES)
        return _num_q("%s saves %s every week for %d weeks. "
                      "How much has %s saved, in pence?"
                      % (who, money(per), weeks, who),
                      per * weeks, "int", unit="p",
                      solution=["%d × %d = %d p." % (per, weeks, per * weeks),
                                "That is %s." % money(per * weeks)])

    if t == 5:                    # NEW: reading financial records
        who = pick(NAMES)
        rows = [("Monday", "pocket money in", pick([100, 150, 200, 250])),
                ("Tuesday", "comic out", pick([75, 90, 120])),
                ("Thursday", "sweets out", pick([45, 60, 80])),
                ("Saturday", "job money in", pick([50, 100, 150]))]
        rec = "; ".join("%s — %s %s" % (dy, what, money(amt)) for dy, what, amt in rows)
        out = sum(a for _, w, a in rows if w.endswith("out"))
        inn = sum(a for _, w, a in rows if w.endswith("in"))
        ask_out = random.random() < 0.5
        return _num_q("Read %s's financial record for the week. %s. According to the "
                      "record, how much money did %s %s in total, in pence?"
                      % (who, rec, who, "spend" if ask_out else "receive"),
                      out if ask_out else inn, "int", unit="p",
                      solution=["Add every '%s' row." % ("out" if ask_out else "in"),
                                "The total is %s." % money(out if ask_out else inn)])

    if t == 6:                    # NEW: keeping financial records
        who = pick(NAMES)
        start = pick([200, 300, 500, 750, 1000])
        got = pick([50, 100, 150, 200])
        spent = pick([40, 60, 85, 120, 175])
        return _num_q("%s is keeping a financial record. The record starts with a balance "
                      "of %s. %s then records %s money in and %s money out. What balance "
                      "should be written at the end of the record, in pence?"
                      % (who, money(start), who, money(got), money(spent)),
                      start + got - spent, "int", unit="p",
                      solution=["%d + %d = %d p after the money in."
                                % (start, got, start + got),
                                "%d − %d = %d p, so record a balance of %s."
                                % (start + got, spent, start + got - spent,
                                   money(start + got - spent))])

    # budget check with several prices shown on a chart (visual)
    items = random.sample(["Pen", "Book", "Ruler", "Bag"], 3)
    prices = [random.randint(20, budget // 3) for _ in items]
    while len(set(prices)) != len(prices):
        prices = [random.randint(20, budget // 3) for _ in items]
    return {"prompt": "The chart shows prices in pence. How much would all three items "
                      "cost altogether, in pence?",
            "component": "bar_chart",
            "spec": {"categories": items, "values": prices, "mode": "read"},
            "answer": sum(prices), "answer_type": "int",
            "solution": ["%s = %d p." % (" + ".join(str(p) for p in prices), sum(prices)),
                         "That is %s." % money(sum(prices))]}


@skill("Y3.9.h", "Mixed multi-step reasoning", S9)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 2, 1, 2, 2])

    if t == 0:                                          # multiply then subtract
        who = pick(NAMES)
        packs = random.randint(2, _by_d(d, 4, 7, 9))
        per = random.randint(3, _by_d(d, 5, 9, 12))
        eaten = random.randint(1, min(packs * per - 1, _by_d(d, 5, 10, 20)))
        return _num_q("%s buys %d packs of %d biscuits. %s eaten. "
                      "How many are left?" % (who, packs, per,
                                              "1 biscuit is" if eaten == 1
                                              else "%d biscuits are" % eaten),
                      packs * per - eaten, "int", unit="biscuits",
                      solution=["%d × %d = %d biscuits." % (packs, per, packs * per),
                                "%d − %d = %d." % (packs * per, eaten, packs * per - eaten)])

    if t == 1:                                          # array model (visual)
        rows = random.randint(2, _by_d(d, 5, 8, 10))
        cols = random.randint(2, _by_d(d, 5, 8, 10))
        return {"prompt": "%s plants %d rows of %d seeds. Build the array and give the "
                          "total number of seeds." % (pick(NAMES), rows, cols),
                "component": "array",
                "spec": {"mode": "build", "maxRows": 10, "maxCols": 10,
                         "targetRows": rows, "targetCols": cols},
                "answer": rows * cols, "answer_type": "int",
                "solution": ["%d rows of %d." % (rows, cols),
                             "%d × %d = %d seeds." % (rows, cols, rows * cols)]}

    if t == 2:                                          # add then divide (shares exactly)
        groups = pick([2, 3, 4, 5])
        each = random.randint(2, _by_d(d, 4, 8, 12))
        total = groups * each
        a = random.randint(1, total - 1)
        b = total - a
        return _num_q("%s has %s and is given %d more. They are then shared "
                      "equally between %d friends. How many marbles does each friend get?"
                      % (pick(NAMES), _pl(a, "marble"), b, groups),
                      each, "int", unit="marbles",
                      solution=["%d + %d = %d marbles." % (a, b, total),
                                "%d ÷ %d = %d each." % (total, groups, each)])

    if t == 3:                                          # data + calculation (visual)
        _, vals = _chart(d, 3)
        cats = random.sample(NAMES, 3)
        return {"prompt": "The chart shows how many stickers three children collected. "
                          "How many stickers are there altogether?",
                "component": "bar_chart",
                "spec": {"categories": cats, "values": vals, "mode": "read"},
                "answer": sum(vals), "answer_type": "int",
                "solution": ["%s." % " + ".join(str(v) for v in vals),
                             "The total is %d stickers." % sum(vals)]}

    # measurement multi-step (visual ruler)
    v = random.randint(3, _by_d(d, 10, 20, 30))
    mx = _by_d(d, 10, 20, 30)
    copies = random.randint(2, _by_d(d, 3, 5, 8))
    return {"prompt": "The ruler shows one strip of card. %d strips are laid end to end. "
                      "How long is the line of strips, in cm?" % copies,
            "component": "ruler",
            "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm"},
            "answer": v * copies, "answer_type": "int",
            "solution": ["One strip measures %d cm." % v,
                         "%d × %d = %d cm." % (copies, v, v * copies)]}
