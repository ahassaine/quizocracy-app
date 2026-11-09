# dev/app/logic/y4_gen_d.py — Year 4 generators: levels 4.6 and 4.7
#
# 4.6 Decimals (tenths & hundredths, place value, rounding, ÷10 and ÷100,
#     adding and subtracting decimals in money and measures contexts)
# 4.7 Measurement, money & time (metric conversion, scales, imperial units,
#     money, analogue/digital time, 24-hour clock, elapsed time, timetables)
#
# Every generator takes a difficulty tier d = 0 (easy) / 1 (core) / 2 (stretch)
# and chooses at random between 8+ genuinely different framings.
#
# Visual components used here:
#   area_grid (parts: 100) ... the hundredths square
#   number_line ............. decimals in steps of 0.1 and 0.01
#   ruler ................... length / mass / capacity scales
#   clock ................... analogue time
#   data_table .............. price lists, timetables, conversion tables, calendars
#   fraction_bar, bar_chart . fraction/decimal equivalence, prices
import math
import random
from fractions import Fraction
from .maths_engine import skill, pick, money, NAMES, n_words

S6 = "4.6 Decimals"
S7 = "4.7 Measurement, money & time"


# ---------------------------------------------------------------- helpers ----
def _tier(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_tier(d)]


def _pick_t(weights):
    """Choose a framing index; visual framings carry more weight."""
    total = float(sum(weights))
    r = random.random() * total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r < acc:
            return i
    return len(weights) - 1


def _pl(n, word, plural=None):
    return "%s %s" % (_n(n), word if abs(n) == 1 else (plural or word + "s"))


def _a(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _n(x):
    """Tidy number text: 3 -> '3', 3.4 -> '3.4', 3.45 -> '3.45', 0.575 -> '0.575' (575 ml)."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return "%d" % int(round(x))
    return ("%.3f" % x).rstrip("0").rstrip(".")


def _h(c):
    """Integer hundredths -> float, rounded safely."""
    return round(int(c) / 100.0, 2)


def _dec_text(c):
    """Integer hundredths -> the decimal as written, keeping a trailing zero
    only when the number really has two decimal places."""
    return _n(_h(c))


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _num_q(prompt, answer, answer_type="int", unit=None, text=False,
           placeholder=None, solution=None, tolerance=0):
    spec = {}
    if unit:
        spec["unit"] = unit
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution or []}


def _line_q(prompt, value, mn, mx, step, major, solution):
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": mn, "max": mx, "step": step, "major": major},
            "answer": round(float(value), 6), "answer_type": "num",
            "tolerance": step / 2.0, "solution": solution}


def _table_q(prompt, headers, rows, answer, answer_type, solution,
             missing=None, tolerance=0):
    spec = {"headers": list(headers),
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _hm(h, m):
    """Normalise to a 12-hour clock string 'H:MM'."""
    h = ((int(h) - 1) % 12) + 1
    return "%d:%02d" % (h, int(m))


def _hm24(h, m):
    return "%02d:%02d" % (int(h) % 24, int(m))


def _clock_minutes(d):
    return _by_d(d, [0, 15, 30, 45],
                 [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
                 [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,
                  3, 7, 12, 18, 23, 37, 42, 48])


def _round_half_up(x):
    return int(math.floor(float(x) + 0.5))


_HALF = {2: "half", 4: "quarter", 5: "fifth", 10: "tenth", 100: "hundredth",
         3: "third", 8: "eighth"}


def _small_part(d, easy, core):
    """The grams/millilitres part of a mixed measure: friendly at d=0 and d=1,
    and at d=2 often under 100 so a zero is needed as a place holder (3 kg 45 g)."""
    if d == 0:
        return random.choice(easy)
    if d == 1:
        return random.choice(core)
    return pick([random.randint(1, 9), random.randint(11, 99), random.randint(101, 999)])


def _frac_words(n, den):
    w = _HALF.get(den)
    if not w:
        return "%d/%d" % (n, den)
    if n == 1:
        return "one " + w
    return "%s %ss" % (n_words(n), w)


_SHOP = ["pen", "rubber", "ruler", "notebook", "sharpener", "pencil case",
         "sticker book", "water bottle"]
_FOOD = ["apple", "banana", "sandwich", "carton of juice", "muffin", "bread roll"]
_GIFTS = ["book", "game", "puzzle", "toy car", "jigsaw", "board game", "kite"]


def _plural(word):
    """'pen' -> 'pens'; 'sandwich' -> 'sandwiches'; 'carton of juice' -> 'cartons
    of juice'."""
    if " of " in word:
        head, rest = word.split(" of ", 1)
        return _plural(head) + " of " + rest
    if word.endswith(("ch", "sh", "s", "x")):
        return word + "es"
    return word + "s"


_UNIT_NAME = {"km": "kilometres", "m": "metres", "cm": "centimetres",
              "mm": "millimetres", "kg": "kilograms", "g": "grams",
              "l": "litres", "ml": "millilitres"}


def _uname(u):
    return _UNIT_NAME.get(u, u)


def _dec_words(c):
    """Integer hundredths -> the decimal expressed in words the fraction way:
    40 -> 'four tenths', 63 -> 'sixty-three hundredths',
    175 -> 'one and seventy-five hundredths'."""
    c = int(c)
    whole, part = divmod(c, 100)
    if part == 0:
        return n_words(whole)
    if part % 10 == 0:
        k = part // 10
        frac = "%s tenth%s" % (n_words(k), "" if k == 1 else "s")
    else:
        frac = "%s hundredth%s" % (n_words(part), "" if part == 1 else "s")
    if whole == 0:
        return frac
    return "%s and %s" % (n_words(whole), frac)


def _point_words(c):
    """Integer hundredths -> the decimal expressed in words the reading way:
    40 -> 'zero point four', 305 -> 'three point zero five'."""
    c = int(c)
    whole, part = divmod(c, 100)
    digits = "%02d" % part
    if digits[1] == "0":
        digits = digits[0]
    return "%s point %s" % (n_words(whole),
                            " ".join(n_words(int(x)) for x in digits))


_TIMELINE_EVENTS = ["the school opened", "the library was built",
                    "the swimming pool opened", "the new bridge was finished",
                    "the park was planted", "the museum opened",
                    "the village hall was built", "the railway station opened"]


# =============================================================== 4.6 =========
@skill("Y4.6.a", "Tenths and hundredths as fractions and decimals", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2])

    def hund():
        """Hundredths for this tier: whole tenths (easy), any (core), or the
        tricky ones (stretch): under a tenth, or not a whole number of tenths."""
        if d == 0:
            return random.randrange(10, 100, 10)
        if d == 1:
            return random.randint(1, 99)
        if random.random() < 0.4:
            return random.randint(1, 9)
        return random.choice([x for x in range(11, 100) if x % 10])

    if t == 10:                      # decimal expressed in words -> decimal
        if d == 0:
            c = random.randrange(10, 100, 10)
        elif d == 1:
            c = random.randint(1, 99)
        else:
            c = random.randint(1, 9) * 100 + random.randint(1, 99)
        return _num_q("Here is a decimal expressed in words: '%s'. "
                      "Write it as a decimal number." % _dec_words(c),
                      _h(c), "num",
                      solution=["'%s' means %s in all."
                                % (_dec_words(c), _pl(c, "hundredth")),
                                "As a decimal that is %s." % _dec_text(c)])

    if t == 11:                      # decimal read out in words -> decimal
        if d == 0:
            c = random.randrange(10, 100, 10)
        elif d == 1:
            c = random.randint(1, 99)
        else:
            c = random.randint(1, 9) * 100 + random.randint(1, 99)
        return _num_q("A decimal is expressed in words as '%s'. "
                      "Write that decimal in figures." % _point_words(c),
                      _h(c), "num",
                      solution=["The words after 'point' give the tenths and "
                                "hundredths digits.",
                                "'%s' in figures is %s."
                                % (_point_words(c), _dec_text(c))])

    if t == 0:                       # shade the hundredths square (decimal given)
        c = hund()
        return {"prompt": "This square is one whole split into 100 equal parts. "
                          "Shade %s of it." % _dec_text(c),
                "component": "area_grid", "spec": {"mode": "fraction", "parts": 100},
                "answer": "%d/100" % c, "answer_type": "frac",
                "solution": ["%s means %s." % (_dec_text(c), _pl(c, "hundredth")),
                             "Shade %d of the 100 small squares." % c]}

    if t == 1:                       # read the hundredths square as a fraction
        c = hund()
        return {"prompt": "The square is one whole split into 100 equal parts, "
                          "with %d small squares shaded. Write the fraction shaded." % c,
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": 100, "shaded": c},
                "answer": "%d/100" % c, "answer_type": "frac",
                "solution": ["%s out of 100 %s shaded." % ("1 part" if c == 1 else "%d parts" % c, "is" if c == 1 else "are"),
                             "The fraction is %d/100." % c]}

    if t == 2:                       # read the hundredths square as a decimal
        c = hund()
        return {"prompt": "The square is one whole split into 100 equal parts, "
                          "with %d small squares shaded. Write the shaded amount "
                          "as a decimal." % c,
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": 100, "shaded": c},
                "answer": _h(c), "answer_type": "num",
                "solution": ["%d/100 is %s." % (c, _pl(c, "hundredth")),
                             "As a decimal that is %s." % _dec_text(c)]}

    if t == 3:                       # tenths on a ten-part model
        k = random.randint(1, 9)
        shown = "%d/100" % (k * 10) if d == 2 else _dec_text(k * 10)   # stretch: given in hundredths
        return {"prompt": "The bar is one whole split into 10 equal parts. "
                          "Shade %s of it." % shown,
                "component": "fraction_bar", "spec": {"parts": 10, "mode": "shade"},
                "answer": "%d/10" % k, "answer_type": "frac",
                "solution": ["%s is %s." % (shown, _pl(k, "tenth")),
                             "Shade %d of the 10 equal parts." % k]}

    if t == 4:                       # fraction -> decimal
        den = pick([10, 100]) if d else 10
        num = random.randint(1, den - 1)
        if d == 2:                   # stretch: more than one whole, e.g. 235/100
            den = 100
            num = random.randint(1, 4) * 100 + hund()
        return _num_q("Write %d/%d as a decimal." % (num, den),
                      round(num / float(den), 2), "num",
                      solution=["%d/%d means %s." % (num, den, _pl(num, "tenth" if den == 10 else "hundredth")),
                                "As a decimal that is %s." % _n(num / float(den))])

    if t == 5:                       # decimal -> fraction
        c = hund()
        return _num_q("Write %s as a fraction with a denominator of 100."
                      % _dec_text(c),
                      "%d/100" % c, "frac", text=True, placeholder="e.g. 37/100",
                      solution=["%s is %s." % (_dec_text(c), _pl(c, "hundredth")),
                                "That is %d/100." % c])

    if t == 6:                       # how many hundredths / tenths
        if d == 2:                   # stretch: a number bigger than one
            k = random.randint(11, 49)
            if random.random() < 0.5:
                return _num_q("How many hundredths are the same as %s?" % _dec_text(k * 10),
                              k * 10, "int", unit="hundredths",
                              solution=["1 whole = 100 hundredths and 1 tenth = 10 hundredths.",
                                        "%s = %d hundredths." % (_dec_text(k * 10), k * 10)])
            return _num_q("How many tenths are the same as %s?" % _dec_text(k * 10),
                          k, "int", unit="tenths",
                          solution=["1 whole = 10 tenths.",
                                    "%s = %s." % (_dec_text(k * 10), _pl(k, "tenth"))])
        if random.random() < 0.5:
            k = random.randint(1, 9)
            return _num_q("How many hundredths are the same as %s?" % _dec_text(k * 10),
                          k * 10, "int", unit="hundredths",
                          solution=["%s is %s." % (_dec_text(k * 10), _pl(k, "tenth")),
                                    "1 tenth = 10 hundredths, so that is %d hundredths."
                                    % (k * 10)])
        k = random.randint(1, 9)
        return _num_q("How many tenths are the same as %d hundredths?" % (k * 10),
                      k, "int", unit="tenths",
                      solution=["10 hundredths = 1 tenth.",
                                "%d ÷ 10 = %s." % (k * 10, _pl(k, "tenth"))])

    if t == 7:                       # place a tenth/hundredth on a line
        c = hund() if d == 2 else random.randint(1, 99)
        if d == 0 or c % 10 == 0:
            c = random.randrange(10, 100, 10)
            return _line_q("Place %d/10 on the number line." % (c // 10),
                           _h(c), 0, 1, 0.1, 0.5,
                           ["Each step on the line is one tenth, or 0.1.",
                            "%d/10 = %s." % (c // 10, _dec_text(c))])
        return _line_q("Place %d/100 on the number line." % c, _h(c), 0, 1, 0.01, 0.1,
                       ["Each small step on the line is one hundredth, or 0.01.",
                        "%d/100 = %s." % (c, _dec_text(c))])

    if t == 8:                       # word problem
        who = pick(NAMES)
        c = random.randint(11, 89) if d == 1 else hund()
        return _num_q("%s colours %d of the 100 squares on a hundred square. "
                      "What decimal of the hundred square has %s coloured?"
                      % (who, c, who),
                      _h(c), "num",
                      solution=["%d out of 100 is %d/100." % (c, c),
                                "As a decimal that is %s." % _dec_text(c)])

    # tenths written as hundredths
    k = random.randint(1, 9)
    if d == 2:                       # stretch: the other way round
        return _num_q("Complete: ___/10 = %d/100" % (k * 10), k, "int",
                      solution=["Divide the top and bottom by 10.",
                                "%d/100 = %d/10." % (k * 10, k)])
    return _num_q("Complete: %d/10 = ___/100" % k, k * 10, "int",
                  solution=["Multiply the top and bottom by 10.",
                            "%d/10 = %d/100." % (k, k * 10)])


@skill("Y4.6.b", "Convert between fractions and decimals", S6)
def _(d=1):
    d = _tier(d)
    pairs = _by_d(d, [(1, 2, 0.5), (1, 4, 0.25), (3, 4, 0.75), (1, 10, 0.1)],
                  [(1, 2, 0.5), (1, 4, 0.25), (3, 4, 0.75), (1, 5, 0.2),
                   (2, 5, 0.4), (3, 5, 0.6), (4, 5, 0.8), (1, 10, 0.1),
                   (3, 10, 0.3), (7, 10, 0.7), (9, 10, 0.9)],
                  [(1, 4, 0.25), (3, 4, 0.75), (1, 5, 0.2), (2, 5, 0.4),
                   (3, 5, 0.6), (4, 5, 0.8), (1, 20, 0.05), (3, 20, 0.15),
                   (7, 20, 0.35), (1, 25, 0.04), (3, 25, 0.12), (7, 100, 0.07),
                   (33, 100, 0.33), (9, 100, 0.09)])
    num, den, dec = pick(pairs)
    t = _pick_t([1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1])

    if t == 0:                       # fraction -> decimal
        return _num_q("Write %d/%d as a decimal." % (num, den), dec, "num",
                      solution=["%d/%d = %d/100." % (num, den, int(round(dec * 100))),
                                "That is %s." % _n(dec)])

    if t == 1:                       # decimal -> fraction
        return _num_q("Write %s as a fraction." % _n(dec),
                      "%d/%d" % (num, den), "frac", text=True, placeholder="e.g. 3/4",
                      solution=["%s is %s." % (_n(dec), _pl(int(round(dec * 100)), "hundredth")),
                                "%d/100 = %d/%d." % (int(round(dec * 100)), num, den)])

    if t == 2:                       # shade a bar to match a decimal
        b_den = pick([2, 4, 5, 10])
        b_num = random.randint(1, b_den - 1)
        val = b_num / float(b_den)
        return {"prompt": "The bar has %d equal parts. Shade it to show %s."
                          % (b_den, _n(val)),
                "component": "fraction_bar", "spec": {"parts": b_den, "mode": "shade"},
                "answer": "%d/%d" % (b_num, b_den), "answer_type": "frac",
                "solution": ["%s = %d/%d." % (_n(val), b_num, b_den),
                             "Shade %s." % _pl(b_num, "part")]}

    if t == 3:                       # place a fraction on a decimal line
        f_num, f_den = pick([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5)])
        val = f_num / float(f_den)
        step = 0.05 if f_den == 4 else 0.1
        return _line_q("Place %s on the number line." % ("%d/%d" % (f_num, f_den)),
                       val, 0, 1, step, 0.5 if step == 0.1 else 0.25,
                       ["%d/%d = %s as a decimal." % (f_num, f_den, _n(val)),
                        "Count on from 0 to %s." % _n(val)])

    if t == 4:                       # complete the equivalence
        if random.random() < 0.5:
            return _num_q("Complete: %d/%d = ___ (write the answer as a decimal)"
                          % (num, den), dec, "num",
                          solution=["%d/%d is the same as %s." % (num, den, _n(dec))])
        return _num_q("Complete: %s = ___/100 (write the missing numerator)" % _n(dec),
                      int(round(dec * 100)), "int",
                      solution=["%s is %s." % (_n(dec), _pl(int(round(dec * 100)), "hundredth")),
                                "So %s = %d/100." % (_n(dec), int(round(dec * 100)))])

    if t == 5:                       # word problem
        who = pick(NAMES)
        return _num_q("%s ate %d/%d of a pizza. Write the amount %s ate as a decimal."
                      % (who, num, den, who), dec, "num",
                      solution=["%d/%d = %d/100." % (num, den, int(round(dec * 100))),
                                "As a decimal that is %s." % _n(dec)])

    if t == 6:                       # comparison across the two forms
        other = round(random.randrange(5, 96, 5) / 100.0, 2)
        while abs(other - dec) < 1e-9:
            other = round(random.randrange(5, 96, 5) / 100.0, 2)
        return _num_q("Which is larger, %d/%d or %s? Write the larger amount "
                      "as a decimal." % (num, den, _n(other)),
                      max(dec, other), "num",
                      solution=["%d/%d = %s." % (num, den, _n(dec)),
                                "%s is larger than %s." % (_n(max(dec, other)),
                                                           _n(min(dec, other)))])

    if t == 7:                       # hundredths square, given as a fraction
        c = int(round(dec * 100))
        return {"prompt": "Shade this hundredths square to show %d/%d." % (num, den),
                "component": "area_grid", "spec": {"mode": "fraction", "parts": 100},
                "answer": "%d/100" % c, "answer_type": "frac",
                "solution": ["%d/%d = %d/100." % (num, den, c),
                             "Shade %d of the 100 small squares." % c]}

    if t == 8:                       # mixed number -> decimal
        whole = random.randint(1, 9)
        f_num, f_den, f_dec = pick([(1, 2, 0.5), (1, 4, 0.25), (3, 4, 0.75),
                                    (1, 10, 0.1), (7, 10, 0.7), (1, 5, 0.2)])
        return _num_q("Write %d and %d/%d as a decimal." % (whole, f_num, f_den),
                      round(whole + f_dec, 2), "num",
                      solution=["%d/%d = %s." % (f_num, f_den, _n(f_dec)),
                                "%d + %s = %s." % (whole, _n(f_dec),
                                                   _n(whole + f_dec))])

    if t == 9:                       # read a shaded grid, answer as a decimal
        parts = pick([10, 100]) if d else 10
        k = random.randint(1, parts - 1)
        return {"prompt": "What fraction of the grid is shaded? Write it as a decimal.", "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": parts, "shaded": k, "placeholder": "e.g. 0.3"},
                "answer": _n(k / float(parts)), "answer_type": "num",
                "solution": ["%d of the %d equal parts %s shaded: %d/%d." % (k, parts, "is" if k == 1 else "are", k, parts),
                             "%d/%d = %s." % (k, parts, _n(k / float(parts)))]}

    if t == 10:                      # measures context
        what, unit = pick([("A jug holds", "litre"), ("A ribbon is", "metre"), ("A bag of rice weighs", "kilogram")])
        return _num_q("%s %d/%d of a %s. Write this as a decimal number of %ss." % (what, num, den, unit, unit), dec, "num",
                      solution=["%d/%d = %s." % (num, den, _n(dec)), "So it is %s %ss." % (_n(dec), unit)])

    if t == 11:                      # tenths and hundredths in words
        if random.random() < 0.5 or d == 0:
            k = random.randint(1, 9)
            return _num_q("Write %s %s as a decimal." % (n_words(k), "tenth" if k == 1 else "tenths"), _n(k / 10.0), "num",
                          solution=["%d/10 = %s." % (k, _n(k / 10.0))])
        k = random.choice([x for x in range(1, 100) if x % 10])
        return _num_q("Write %s %s as a decimal." % (n_words(k), "hundredth" if k == 1 else "hundredths"), _n(k / 100.0), "num",
                      solution=["%d/100 = %s." % (k, _n(k / 100.0))])

    # how many tenths
    tenth_dec = pick([0.2, 0.4, 0.5, 0.6, 0.8, 0.9, 0.3, 0.7])
    return _num_q("How many tenths is %s the same as?" % _n(tenth_dec),
                  int(round(tenth_dec * 10)), "int", unit="tenths",
                  solution=["1 tenth = 0.1.",
                            "%s is %s." % (_n(tenth_dec),
                                           _pl(int(round(tenth_dec * 10)), "tenth"))])


@skill("Y4.6.c", "Place value in decimals", S6)
def _(d=1):
    d = _tier(d)
    whole = random.randint(1, _by_d(d, 9, 20, 99))
    # keep every digit of the number distinct, so "the digit 3" is never ambiguous
    used = set(str(whole))
    pool = [x for x in range(1, 10) if str(x) not in used] or [1, 2, 3]
    tenths = random.choice(pool)
    pool2 = [x for x in pool if x != tenths] or [x for x in range(1, 10) if x != tenths]
    hund = random.choice(pool2) if d else 0
    val = round(whole + tenths / 10.0 + hund / 100.0, 2)
    txt = "%d.%d%d" % (whole, tenths, hund) if hund or d else "%d.%d" % (whole, tenths)
    if not hund:
        txt = "%d.%d" % (whole, tenths)
        val = round(whole + tenths / 10.0, 2)
    t = _pick_t([1, 1, 1, 1, 1, 2, 1, 1, 1, 1])

    if t == 0:                       # value of a digit, as a decimal
        if hund and random.random() < 0.5:
            return _num_q("What is the value of the digit %d in %s? "
                          "Write it as a decimal." % (hund, txt),
                          round(hund / 100.0, 2), "num",
                          solution=["The %d is in the hundredths place." % hund,
                                    "Its value is %s = %s."
                                    % (_pl(hund, "hundredth"), _n(hund / 100.0))])
        return _num_q("What is the value of the digit %d in %s? "
                      "Write it as a decimal." % (tenths, txt),
                      round(tenths / 10.0, 2), "num",
                      solution=["The %d is in the tenths place." % tenths,
                                "Its value is %s = %s."
                                % (_pl(tenths, "tenth"), _n(tenths / 10.0))])

    if t == 1:                       # which digit is in a named place
        place = pick(["tenths", "hundredths"]) if hund else "tenths"
        digit = tenths if place == "tenths" else hund
        return _num_q("Which digit is in the %s place in %s?" % (place, txt),
                      digit, "int",
                      solution=["Read the digits after the decimal point: "
                                "tenths first, then hundredths.",
                                "The %s digit is %d." % (place, digit)])

    if t == 2:                       # build from parts (single-digit ones)
        w = random.randint(1, 9)
        v2 = round(w + tenths / 10.0 + (hund / 100.0 if hund else 0), 2)
        if hund:
            return _num_q("Write the number that is %s, %s and %s."
                          % (_pl(w, "one"), _pl(tenths, "tenth"),
                             _pl(hund, "hundredth")),
                          v2, "num",
                          solution=["%s = %d, %s = %s, %s = %s."
                                    % (_pl(w, "one"), w, _pl(tenths, "tenth"), _n(tenths / 10.0),
                                       _pl(hund, "hundredth"), _n(hund / 100.0)),
                                    "Altogether that is %s." % _n(v2)])
        return _num_q("Write the number that is %s and %s."
                      % (_pl(w, "one"), _pl(tenths, "tenth")), v2, "num",
                      solution=["%s and %s is %s." % (_pl(w, "one"), _pl(tenths, "tenth"), _n(v2))])

    if t == 3:                       # partition, missing part
        if hund:
            return _num_q("Complete the partition: %s = %d + %s + ___"
                          % (txt, whole, _n(tenths / 10.0)),
                          round(hund / 100.0, 2), "num",
                          solution=["%s splits into ones, tenths and hundredths." % txt,
                                    "The missing part is %s." % _n(hund / 100.0)])
        return _num_q("Complete the partition: %s = %d + ___" % (txt, whole),
                      round(tenths / 10.0, 2), "num",
                      solution=["%s is %s and %s." % (txt, _pl(whole, "one"), _pl(tenths, "tenth")),
                                "The missing part is %s." % _n(tenths / 10.0)])

    if t == 4:                       # how many hundredths altogether
        total_h = int(round(val * 100))
        return _num_q("How many hundredths are there altogether in %s?" % txt,
                      total_h, "int", unit="hundredths",
                      solution=["1 whole = 100 hundredths.",
                                "%s = %s." % (txt, _pl(total_h, "hundredth"))])

    if t == 5:                       # hundredths square place value (visual)
        c = random.randint(11, 99)
        ask_tenths = random.random() < 0.5
        if ask_tenths:
            return {"prompt": "The hundredths square has %d of its 100 small squares "
                              "shaded. Write the value of the tenths digit of that "
                              "decimal, as a decimal." % c,
                    "component": "area_grid",
                    "spec": {"mode": "fraction_read", "parts": 100, "shaded": c},
                    "answer": round((c // 10) / 10.0, 2), "answer_type": "num",
                    "solution": ["%d/100 = %s." % (c, _dec_text(c)),
                                 "The tenths digit is %d, worth %s."
                                 % (c // 10, _n((c // 10) / 10.0))]}
        return {"prompt": "The hundredths square has %d of its 100 small squares "
                          "shaded. Write the digit in the hundredths place of that "
                          "decimal." % c,
                "component": "area_grid",
                "spec": {"mode": "fraction_read", "parts": 100, "shaded": c},
                "answer": c % 10, "answer_type": "int",
                "solution": ["%d/100 = %s." % (c, _dec_text(c)),
                             "The hundredths digit is %d." % (c % 10)]}

    if t == 6:                       # missing whole in a partition
        if hund:
            return _num_q("Complete: ___ + %s + %s = %s"
                          % (_n(tenths / 10.0), _n(hund / 100.0), txt), whole, "int",
                          solution=["%s + %s = %s."
                                    % (_n(tenths / 10.0), _n(hund / 100.0),
                                       _n(round(tenths / 10.0 + hund / 100.0, 2))),
                                    "%s − %s = %d."
                                    % (txt, _n(round(tenths / 10.0 + hund / 100.0, 2)),
                                       whole)])
        return _num_q("Complete: ___ + %s = %s" % (_n(tenths / 10.0), txt), whole, "int",
                      solution=["%s − %s = %d." % (txt, _n(tenths / 10.0), whole)])

    if t == 7:                       # money place value
        p = random.randint(1, 9)
        pence = random.randint(1, 9)
        amount = "£%d.%d%d" % (whole % 10, p, pence)
        return _num_q("In the amount %s, how many pence does the digit %d "
                      "just after the point stand for?" % (amount, p),
                      p * 10, "int", unit="p",
                      solution=["The first digit after the point counts 10p coins.",
                                "%d × 10p = %dp." % (p, p * 10)])

    if t == 8:                       # ones and hundredths only (a zero tenth)
        w = random.randint(1, 9)
        c = random.randint(1, 9)
        return _num_q("Write the number that is %s and %s."
                      % (_pl(w, "one"), _pl(c, "hundredth")),
                      round(w + c / 100.0, 2), "num",
                      solution=["There are no tenths, so the tenths digit is 0.",
                                "The number is %d.0%d." % (w, c)])

    # compare the value of the same digit in two numbers
    dig = random.randint(1, 9)
    others = [x for x in range(1, 10) if x != dig]
    a_txt = "%d.%d%d" % (random.choice(others), dig, random.choice(others))
    b_txt = "0.%d%d" % (random.choice(others), dig)
    return _num_q("The digit %d appears in %s and in %s. In which of the two numbers "
                  "is the %d worth more? Write that number."
                  % (dig, a_txt, b_txt, dig),
                  float(a_txt), "num",
                  solution=["In %s the %d is in the tenths place, worth %s."
                            % (a_txt, dig, _n(dig / 10.0)),
                            "In %s it is in the hundredths place, worth only %s, "
                            "so %s." % (b_txt, _n(dig / 100.0), a_txt)])


@skill("Y4.6.d", "One tenth or one hundredth more or less", S6)
def _(d=1):
    d = _tier(d)
    step_c = 10 if d == 0 else pick([10, 10, 1])
    word = "tenth" if step_c == 10 else "hundredth"
    lo, hi = _by_d(d, (11, 89), (105, 899), (205, 1895))
    start = random.randint(lo, hi)
    if step_c == 10 and d == 0:
        start = random.randrange(110, 900, 10)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 2])

    if t == 0:                       # one more
        return _num_q("What is one %s more than %s?" % (word, _dec_text(start)),
                      _h(start + step_c), "num",
                      solution=["One %s is %s." % (word, _dec_text(step_c)),
                                "%s + %s = %s." % (_dec_text(start), _dec_text(step_c),
                                                   _dec_text(start + step_c))])

    if t == 1:                       # one less
        s = max(start, step_c + 5)
        return _num_q("What is one %s less than %s?" % (word, _dec_text(s)),
                      _h(s - step_c), "num",
                      solution=["One %s is %s." % (word, _dec_text(step_c)),
                                "%s − %s = %s." % (_dec_text(s), _dec_text(step_c),
                                                   _dec_text(s - step_c))])

    if t == 2:                       # missing number (inverse)
        return _num_q("A number is one %s less than %s. What is that number?"
                      % (word, _dec_text(start + step_c)), _h(start), "num",
                      solution=["Take away one %s." % word,
                                "%s − %s = %s." % (_dec_text(start + step_c),
                                                   _dec_text(step_c),
                                                   _dec_text(start))])

    if t == 3:                       # inverse the other way
        who = pick(NAMES)
        return _num_q("%s thinks of a number. One %s more than that number is %s. "
                      "What number did %s think of?"
                      % (who, word, _dec_text(start + step_c), who),
                      _h(start), "num",
                      solution=["Work backwards: take one %s away." % word,
                                "%s − %s = %s." % (_dec_text(start + step_c),
                                                   _dec_text(step_c),
                                                   _dec_text(start))])

    if t == 4:                       # place the answer on a number line
        if step_c == 10:
            base = random.randrange(10, 180, 10)
            return _line_q("Place the number that is one tenth more than %s "
                           "on the number line." % _dec_text(base),
                           _h(base + 10), 0, 2, 0.1, 0.5,
                           ["One tenth more than %s is %s."
                            % (_dec_text(base), _dec_text(base + 10)),
                            "Each step on the line is 0.1."])
        base = random.randint(1, 98)
        return _line_q("Place the number that is one hundredth more than %s "
                       "on the number line." % _dec_text(base),
                       _h(base + 1), 0, 1, 0.01, 0.1,
                       ["One hundredth more than %s is %s."
                        % (_dec_text(base), _dec_text(base + 1)),
                        "Each small step on the line is 0.01."])

    if t == 5:                       # crossing a whole-number boundary
        whole = random.randint(1, 8)
        if step_c == 10:
            s = whole * 100 + 90
            return _num_q("What is one tenth more than %s?" % _dec_text(s),
                          _h(s + 10), "num",
                          solution=["%s + 0.1 crosses the next whole number."
                                    % _dec_text(s),
                                    "%s + 0.1 = %d." % (_dec_text(s), whole + 1)])
        s = whole * 100 + 99
        return _num_q("What is one hundredth more than %s?" % _dec_text(s),
                      _h(s + 1), "num",
                      solution=["%s + 0.01 makes the next whole number." % _dec_text(s),
                                "%s + 0.01 = %d." % (_dec_text(s), whole + 1)])

    if t == 6:                       # count on several steps
        k = random.randint(2, _by_d(d, 3, 4, 6))
        return _num_q("Count on %s from %s. What number do you reach?"
                      % (_pl(k, word), _dec_text(start)),
                      _h(start + k * step_c), "num",
                      solution=["%d × %s = %s." % (k, _dec_text(step_c),
                                                   _dec_text(k * step_c)),
                                "%s + %s = %s." % (_dec_text(start),
                                                   _dec_text(k * step_c),
                                                   _dec_text(start + k * step_c))])

    if t == 7:                       # measures context
        who = pick(NAMES)
        s = random.randint(105, 395)
        if step_c == 10:
            return _num_q("A sunflower is %s m tall. In a week it grows one tenth of a "
                          "metre taller. How tall is the sunflower then, in metres?"
                          % _dec_text(s),
                          _h(s + 10), "num", unit="m",
                          solution=["One tenth of a metre is 0.1 m.",
                                    "%s + 0.1 = %s m." % (_dec_text(s),
                                                          _dec_text(s + 10))])
        return _num_q("%s pours %s litres of water into a jug, then adds one hundredth "
                      "of a litre more. How much water is in the jug, in litres?"
                      % (who, _dec_text(s)),
                      _h(s + 1), "num", unit="l",
                      solution=["One hundredth of a litre is 0.01 l.",
                                "%s + 0.01 = %s l." % (_dec_text(s), _dec_text(s + 1))])

    # sequence of steps of one tenth / one hundredth
    up = random.random() < 0.5
    s = start if up else max(start, 5 * step_c)
    seq = [s + i * step_c * (1 if up else -1) for i in range(3)]
    nxt = seq[-1] + step_c * (1 if up else -1)
    return _num_q("Count %s in %ss: %s, ___. Write the next number."
                  % ("on" if up else "back", word,
                     ", ".join(_dec_text(v) for v in seq)),
                  _h(nxt), "num",
                  solution=["The count goes %s in %ss." % ("up" if up else "down", word),
                            "The next number is %s." % _dec_text(nxt)])


@skill("Y4.6.e", "Decimals on a number line and decimal sequences", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2])

    if t == 10:                      # graph a decimal on a tenths number line
        w = random.randint(0, _by_d(d, 1, 4, 8))
        c = w * 100 + random.randrange(1, 10) * 10
        return _line_q("Graph the decimal %s on the number line."
                       % _dec_text(c), _h(c), w, w + 1, 0.1, 0.5,
                       ["The number line runs from %d to %d in steps of 0.1."
                        % (w, w + 1),
                        "%s is %s past %d." % (_dec_text(c),
                                               _pl((c - w * 100) // 10, "tenth"), w)])

    if t == 11:                      # graph a decimal on a hundredths number line
        w = random.randint(0, _by_d(d, 1, 4, 8))
        c = w * 100 + random.randint(1, 99)
        return _line_q("Graph the decimal %s on the number line."
                       % _dec_text(c), _h(c), w, w + 1, 0.01, 0.1,
                       ["Each small step on the number line is one hundredth, or 0.01.",
                        "%s is %s past %d." % (_dec_text(c),
                                                 _pl(c - w * 100, "hundredth"), w)])

    if t == 0:                       # place a decimal, tenths line
        lo, hi = 0, _by_d(d, 1, 2, 2)
        c = random.randrange(1, 10 * hi) * 10
        if d == 2:                   # stretch: further along the line
            lo = random.randint(2, 7)
            hi = lo + 2
            c = lo * 100 + random.choice([x for x in range(1, 20) if x != 10]) * 10
        return _line_q("Place %s on the number line." % _dec_text(c), _h(c),
                       lo, hi, 0.1, 0.5,
                       ["Each step on the line is one tenth, or 0.1.",
                        "Count %s on from %d." % (_pl((c - lo * 100) // 10, "tenth"), lo)])

    if t == 1:                       # place a decimal, hundredths line
        base = random.randint(0, 8) * 10 if d else 0
        c = base * 10 + (random.randrange(5, 100, 5) if d == 0 else random.randint(1, 99))
        lo = round(base / 10.0, 2)
        return _line_q("Place %s on the number line." % _dec_text(c), _h(c),
                       lo, round(lo + 1, 2), 0.01, 0.5 if d == 2 else 0.1,   # stretch: fewer labels
                       ["Each small step on the line is one hundredth, or 0.01.",
                        "%s is between %s and %s." % (_dec_text(c), _n(lo),
                                                      _n(lo + 1))])

    if t == 2:                       # place a value given as a fraction
        c = random.randrange(10, 100, 10) if d == 0 else random.randint(1, 99)
        w = 1 if d == 2 else 0       # stretch: more than one whole, e.g. 135/100
        c += w * 100
        return _line_q("Place %d/100 on the number line." % c, _h(c),
                       w, w + 1, 0.01, 0.1,
                       ["%d/100 = %s." % (c, _dec_text(c)),
                        "Count %d small steps on from %d." % (c - w * 100, w)])

    if t == 3:                       # next in a sequence
        step_c = pick(_by_d(d, [10, 20], [10, 20, 25, 50], [1, 2, 5, 25, 30]))
        start = random.randint(1, 60) * 5
        seq = [start + i * step_c for i in range(3)]
        return _num_q("What comes next? %s, ___"
                      % ", ".join(_dec_text(v) for v in seq),
                      _h(seq[-1] + step_c), "num",
                      solution=["The sequence goes up in steps of %s."
                                % _dec_text(step_c),
                                "%s + %s = %s." % (_dec_text(seq[-1]),
                                                   _dec_text(step_c),
                                                   _dec_text(seq[-1] + step_c))])

    if t == 4:                       # missing middle term
        step_c = pick(_by_d(d, [10, 20], [10, 20, 5, 25], [5, 25, 2, 15]))
        start = random.randint(1, 20) * 10 if d == 0 else random.randint(10, 200)
        seq = [start + i * step_c for i in range(4)]
        k = random.choice([1, 2])
        shown = ["___" if i == k else _dec_text(v) for i, v in enumerate(seq)]
        return _num_q("Find the missing number in this sequence: %s" % ", ".join(shown),
                      _h(seq[k]), "num",
                      solution=["The sequence goes up in steps of %s."
                                % _dec_text(step_c),
                                "The missing number is %s." % _dec_text(seq[k])])

    if t == 5:                       # counting back
        step_c = pick(_by_d(d, [10], [10, 20, 5], [1, 5, 25, 30]))
        start = random.randint(max(60, 3 * step_c + 5), 300)   # never counts below zero
        seq = [start - i * step_c for i in range(3)]
        return _num_q("Count back: %s, ___. Write the next number."
                      % ", ".join(_dec_text(v) for v in seq),
                      _h(seq[-1] - step_c), "num",
                      solution=["The sequence goes down in steps of %s."
                                % _dec_text(step_c),
                                "%s − %s = %s." % (_dec_text(seq[-1]),
                                                   _dec_text(step_c),
                                                   _dec_text(seq[-1] - step_c))])

    if t == 6:                       # place a value between two whole numbers
        w = random.randint(1, 2) if d == 0 else random.randint(1, 8)
        span = 2 if d == 2 else 1    # stretch: a longer line, so read the whole number too
        c = w * 100 + random.choice([x for x in range(1, 10 * span) if x != 10]) * 10
        return _line_q("Place %s on the number line." % _dec_text(c), _h(c),
                       w, w + span, 0.1, 0.5,
                       ["The line runs from %d to %d in steps of 0.1." % (w, w + span),
                        "%s is %s past %d." % (_dec_text(c),
                                               _pl((c - w * 100) // 10, "tenth"), w)])

    if t == 7:                       # nth term of a count
        step_c = pick(_by_d(d, [10, 20], [10, 20, 25, 5], [5, 25, 15]))
        start = random.randint(1, 15) * 10 if d == 0 else random.randint(5, 150)
        k = random.randint(*_by_d(d, (3, 4), (3, 6), (5, 9)))
        return _num_q("Start at %s and count on in steps of %s. What is the %s number "
                      "you say after %s?" % (_dec_text(start), _dec_text(step_c),
                                             _ord(k), _dec_text(start)),
                      _h(start + k * step_c), "num",
                      solution=["%d steps of %s is %s." % (k, _dec_text(step_c),
                                                           _dec_text(k * step_c)),
                                "%s + %s = %s." % (_dec_text(start),
                                                   _dec_text(k * step_c),
                                                   _dec_text(start + k * step_c))])

    if t == 8:                       # halfway between
        if d == 2:                   # stretch: halfway between two decimals
            a = random.randint(1, 8) * 100 + random.randint(1, 7) * 10
            b = a + pick([10, 20, 40, 60])
            return _num_q("What number is halfway between %s and %s?"
                          % (_dec_text(a), _dec_text(b)),
                          _h((a + b) // 2), "num",
                          solution=["The gap from %s to %s is %s."
                                    % (_dec_text(a), _dec_text(b), _dec_text(b - a)),
                                    "Half of that is %s, so halfway is %s."
                                    % (_dec_text((b - a) // 2), _dec_text((a + b) // 2))])
        a = random.randint(1, 9) * 100
        b = a + 100
        return _num_q("What number is halfway between %d and %d?"
                      % (a // 100, b // 100),
                      _h((a + b) // 2), "num",
                      solution=["The gap from %d to %d is 1." % (a // 100, b // 100),
                                "Half of 1 is 0.5, so halfway is %s."
                                % _dec_text((a + b) // 2)])

    # place the answer to a small step question
    k = random.randint(1, 3) if d == 0 else random.randint(1, 5)
    base = random.randrange(0, (100 if d == 0 else 200) - k * 10 + 1, 10)
    if d == 2:                       # stretch: the count crosses a whole number
        k = random.randint(3, 9)
        base = 100 - random.randint(1, k - 1) * 10
    return _line_q("Count on %s from %s and place the number you reach on the "
                   "number line." % (_pl(k, "tenth"), _dec_text(base)),
                   _h(base + k * 10), 0, 2, 0.1, 0.5,
                   ["%s tenths on from %s is %s."
                    % (n_words(k).capitalize(), _dec_text(base),
                       _dec_text(base + k * 10)),
                    "Each step on the line is 0.1."])


@skill("Y4.6.f", "Compare and order decimals", S6)
def _(d=1):
    d = _tier(d)

    def _vals(k):
        """k distinct values in hundredths, tricky ones at higher tiers."""
        out = []
        base = random.randint(1, _by_d(d, 5, 9, 20))
        while len(out) < k:
            if d == 0:
                v = base * 100 + random.randrange(0, 100, 10)
            elif d == 1:
                v = base * 100 + random.randint(0, 99)
            else:
                v = random.choice([base, base + 1]) * 100 + random.randint(0, 99)
            if v not in out:
                out.append(v)
        return out

    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2])

    def _pair():
        """Two distinct values, both with a digit after the decimal point."""
        for _try in range(30):
            a, b = _vals(2)
            if a % 100 and b % 100:
                return a, b
        return _vals(2)

    if t == 10:                      # which decimal comparison is true?
        letters = ["A", "B", "C"]
        true_i = random.randrange(3)
        parts = []
        used = []
        for i in range(3):
            a, b = _pair()
            while frozenset((a, b)) in used:
                a, b = _pair()
            used.append(frozenset((a, b)))
            really_bigger = a > b
            if i == true_i:
                sign = ">" if really_bigger else "<"
            else:
                sign = "<" if really_bigger else ">"
            parts.append("%s %s %s %s" % (letters[i], _dec_text(a), sign,
                                          _dec_text(b)))
        return _num_q("Exactly one of these decimal comparisons is true: %s. "
                      "Type the letter of the true comparison."
                      % ", ".join(parts),
                      letters[true_i], "str", text=True, placeholder="A, B or C",
                      solution=["Line up the decimal points and compare the ones, "
                                "then the tenths, then the hundredths.",
                                "Comparison %s is the true one." % letters[true_i]])

    if t == 11:                      # is this decimal comparison true or false?
        a, b = _pair()
        sign = pick([">", "<"])
        truth = (a > b) if sign == ">" else (a < b)
        return _num_q("Is this decimal comparison true or false? %s %s %s. "
                      "Type true or false." % (_dec_text(a), sign, _dec_text(b)),
                      "true" if truth else "false", "str", text=True,
                      placeholder="true / false",
                      solution=["Compare the ones, then the tenths, then the "
                                "hundredths: %s is %s %s."
                                % (_dec_text(a), "greater than" if a > b
                                   else "less than", _dec_text(b)),
                                "So the comparison is %s."
                                % ("true" if truth else "false")])

    if t == 0:                       # which is larger
        a, b = _vals(2)
        return _num_q("Which is larger, %s or %s? Write the larger number."
                      % (_dec_text(a), _dec_text(b)), _h(max(a, b)), "num",
                      solution=["Compare the ones, then the tenths, then the hundredths.",
                                "%s is larger than %s." % (_dec_text(max(a, b)),
                                                           _dec_text(min(a, b)))])

    if t == 1:                       # which is smaller
        a, b = _vals(2)
        return _num_q("Which is smaller, %s or %s? Write the smaller number."
                      % (_dec_text(a), _dec_text(b)), _h(min(a, b)), "num",
                      solution=["Compare the ones, then the tenths, then the hundredths.",
                                "%s is smaller than %s." % (_dec_text(min(a, b)),
                                                            _dec_text(max(a, b)))])

    if t == 2:                       # largest of three
        vs = _vals(3)
        return _num_q("Write the largest of these numbers: %s"
                      % ", ".join(_dec_text(v) for v in vs), _h(max(vs)), "num",
                      solution=["Line up the decimal points and compare place by place.",
                                "The largest is %s." % _dec_text(max(vs))])

    if t == 3:                       # smallest of three
        vs = _vals(3)
        return _num_q("Write the smallest of these numbers: %s"
                      % ", ".join(_dec_text(v) for v in vs), _h(min(vs)), "num",
                      solution=["Line up the decimal points and compare place by place.",
                                "The smallest is %s." % _dec_text(min(vs))])

    if t == 4:                       # place the larger on a number line
        w = random.randint(0, 8)
        a = w * 100 + random.randrange(10, 100, 10)
        b = w * 100 + random.randrange(10, 100, 10)
        while b == a:
            b = w * 100 + random.randrange(10, 100, 10)
        return _line_q("Which is greater, %s or %s? Place the greater number on the "
                       "number line." % (_dec_text(a), _dec_text(b)),
                       _h(max(a, b)), w, w + 1, 0.1, 0.5,
                       ["Both numbers are between %d and %d." % (w, w + 1),
                        "%s is greater than %s." % (_dec_text(max(a, b)),
                                                    _dec_text(min(a, b)))])

    if t == 5:                       # word problem with names
        p, q = _two_names()
        a, b = _vals(2)
        a = a % 500 + 100
        b = b % 500 + 100
        while b == a:
            b = random.randint(100, 600)
        return _num_q("%s jumped %s and %s jumped %s. "
                      "Who jumped further? Type the name."
                      % (p, _dec_text(a) + (" metre" if a == 100 else " metres"), q,
                         _dec_text(b) + (" metre" if b == 100 else " metres")),
                      p if a > b else q, "str", text=True, placeholder="a name",
                      solution=["%s m and %s m: compare the tenths and hundredths."
                                % (_dec_text(a), _dec_text(b)),
                                "%s jumped further." % (p if a > b else q)])

    if t == 6:                       # decimal vs fraction
        f_num, f_den, f_dec = pick([(1, 2, 0.5), (1, 4, 0.25), (3, 4, 0.75),
                                    (1, 5, 0.2), (3, 5, 0.6), (7, 10, 0.7)])
        other = round(random.randrange(5, 96, 5) / 100.0, 2)
        while abs(other - f_dec) < 1e-9:
            other = round(random.randrange(5, 96, 5) / 100.0, 2)
        return _num_q("Which is greater, %s or %d/%d? Write the greater amount "
                      "as a decimal." % (_n(other), f_num, f_den),
                      max(other, f_dec), "num",
                      solution=["%d/%d = %s." % (f_num, f_den, _n(f_dec)),
                                "The greater amount is %s." % _n(max(other, f_dec))])

    if t == 7:                       # closer to a whole number
        w = random.randint(1, 8)
        a = w * 100 - random.randint(5, 45)
        b = w * 100 + random.randint(5, 45)
        while abs(w * 100 - a) == abs(b - w * 100):
            b = w * 100 + random.randint(5, 45)
        closer = a if (w * 100 - a) < (b - w * 100) else b
        return _num_q("Which number is closer to %d: %s or %s? Write that number."
                      % (w, _dec_text(a), _dec_text(b)), _h(closer), "num",
                      solution=["%s is %s away from %d and %s is %s away."
                                % (_dec_text(a), _dec_text(w * 100 - a), w,
                                   _dec_text(b), _dec_text(b - w * 100)),
                                "%s is closer." % _dec_text(closer)])

    if t == 8:                       # count how many are greater than a boundary
        vs = _vals(4)
        cut = random.randint(min(vs) + 1, max(vs))
        n_more = len([v for v in vs if v > cut])
        return _num_q("How many of these numbers are greater than %s? %s"
                      % (_dec_text(cut), ", ".join(_dec_text(v) for v in vs)),
                      n_more, "int",
                      solution=["Compare each number with %s." % _dec_text(cut),
                                "%d of them %s greater." % (n_more, "is" if n_more == 1 else "are")])

    # money comparison
    a = random.randint(105, 995)
    b = random.randint(105, 995)
    while b == a:
        b = random.randint(105, 995)
    return _num_q("Which costs more, a book at %s or a game at %s? "
                  "Write the larger price in pounds, for example 4.75."
                  % (money(a), money(b)),
                  round(max(a, b) / 100.0, 2), "num",
                  solution=["Compare the pounds first, then the pence.",
                            "The larger price is %s." % money(max(a, b))])


@skill("Y4.6.g", "Round decimals to the nearest whole number", S6)
def _(d=1):
    d = _tier(d)

    def _v():
        w = random.randint(1, _by_d(d, 9, 20, 60))
        frac = random.randrange(1, 100) if d else random.randrange(1, 10) * 10
        return w * 100 + frac

    def _m(lo, hi):
        """A measure in hundredths between lo and hi: one decimal place (easy),
        any (core), or within 0.05 of the halfway point (stretch)."""
        if d == 0:
            return random.randint(lo // 10 + 1, hi // 10) * 10
        if d == 2:
            return random.randint(lo // 100, hi // 100 - 1) * 100 + random.randint(45, 55)
        return random.randint(lo, hi)

    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                       # bare rounding
        v = _v()
        return _num_q("Round %s to the nearest whole number." % _dec_text(v),
                      _round_half_up(v / 100.0), "int",
                      solution=["Look at the tenths digit: %d." % ((v // 10) % 10),
                                "%s rounds to %d."
                                % (_dec_text(v), _round_half_up(v / 100.0))])

    if t == 1:                       # exactly a half
        w = _by_d(d, random.randint(1, 9), random.randint(1, 20),
                  random.randint(1, 9) * 10 - 1)       # stretch: 39.5 rolls over to 40
        v = w * 100 + 50
        return _num_q("Round %s to the nearest whole number." % _dec_text(v),
                      w + 1, "int",
                      solution=["%s is exactly halfway between %d and %d."
                                % (_dec_text(v), w, w + 1),
                                "A half always rounds up, so the answer is %d." % (w + 1)])

    if t == 2:                       # which of two rounds to a target
        w = random.randint(2, 15) if d < 2 else random.randint(10, 60)
        a = w * 100 - random.randint(1, 49)
        b = w * 100 - random.randint(51, 99)
        if d == 0:                   # one decimal place, well away from the half
            a = w * 100 - random.randint(1, 4) * 10
            b = w * 100 - random.randint(6, 9) * 10
        elif d == 2:                 # both close to the halfway point
            a = w * 100 - random.randint(41, 50)
            b = w * 100 - random.randint(51, 59)
        return _num_q("Which of these rounds to %d: %s or %s? Write that number."
                      % (w, _dec_text(a), _dec_text(b)), _h(a), "num",
                      solution=["%s rounds to %d." % (_dec_text(a), w),
                                "%s rounds to %d instead." % (_dec_text(b), w - 1)])

    if t == 3:                       # word problem, measures
        who = pick(NAMES)
        v = _m(105, 995)
        return _num_q("A plank is %s metres long. Rounded to the nearest metre, "
                      "how long is the plank?" % _dec_text(v),
                      _round_half_up(v / 100.0), "int", unit="m",
                      solution=["The tenths digit is %d." % ((v // 10) % 10),
                                "%s m rounds to %d m."
                                % (_dec_text(v), _round_half_up(v / 100.0))])

    if t == 4:                       # round then place on a number line
        v = _v()
        r = _round_half_up(v / 100.0)
        top = max(10, ((r // 10) + 1) * 10)
        return _line_q("Round %s to the nearest whole number, then place your answer "
                       "on the number line." % _dec_text(v), r, 0, top, 1, 5,
                       ["The tenths digit is %d." % ((v // 10) % 10),
                        "%s rounds to %d." % (_dec_text(v), r)])

    if t == 5:                       # inverse: largest / smallest that rounds to n
        w = random.randint(2, 9) if d == 0 else random.randint(2, 20)
        largest = random.random() < 0.5
        if d == 2 and largest:       # stretch: two decimal places
            return _num_q("A number with two decimal places rounds to %d. "
                          "What is the largest such number?" % w,
                          _h(w * 100 + 49), "num",
                          solution=["Anything from %s up to %s rounds to %d."
                                    % (_dec_text(w * 100 - 50),
                                       _dec_text(w * 100 + 49), w),
                                    "The largest with two decimal places is %s."
                                    % _dec_text(w * 100 + 49)])
        if largest:
            return _num_q("A number with one decimal place rounds to %d. "
                          "What is the largest such number?" % w,
                          _h(w * 100 + 40), "num",
                          solution=["Anything from %s to %s rounds to %d."
                                    % (_dec_text(w * 100 - 50),
                                       _dec_text(w * 100 + 40), w),
                                    "The largest with one decimal place is %s."
                                    % _dec_text(w * 100 + 40)])
        return _num_q("A number with one decimal place rounds to %d. "
                      "What is the smallest such number?" % w,
                      _h(w * 100 - 50), "num",
                      solution=["%s is halfway, and a half rounds up to %d."
                                % (_dec_text(w * 100 - 50), w),
                                "So the smallest is %s." % _dec_text(w * 100 - 50)])

    if t == 6:                       # money to the nearest pound
        p = _m(120, 1980)
        return _num_q("A toy costs %s. Rounded to the nearest pound, "
                      "how much is that?" % money(p),
                      _round_half_up(p / 100.0), "int", unit="£",
                      solution=["There are %d pence after the pounds." % (p % 100),
                                "%s rounds to £%d."
                                % (money(p), _round_half_up(p / 100.0))])

    if t == 7:                       # table of measurements
        who = pick(NAMES)
        rows = []
        vals = []
        for nm in random.sample(NAMES, 3):
            v = _by_d(d, random.randint(11, 19) * 10, random.randint(105, 195),
                      random.randint(140, 160))   # stretch: all near 1.5 m
            vals.append(v)
            rows.append([nm, _dec_text(v) + " m"])
        k = random.randrange(3)
        return _table_q("The table shows three heights. Round %s's height to the "
                        "nearest metre." % rows[k][0],
                        ["Name", "Height"], rows,
                        _round_half_up(vals[k] / 100.0), "int",
                        ["%s's height is %s m." % (rows[k][0], _dec_text(vals[k])),
                         "That rounds to %d m." % _round_half_up(vals[k] / 100.0)])

    if t == 8:                       # rounding down explicitly
        w = random.randint(1, 9) if d == 0 else random.randint(1, 20) if d == 1 \
            else random.randint(10, 60)
        v = w * 100 + _by_d(d, random.randint(1, 4) * 10, random.randint(1, 49),
                            random.randint(40, 49))
        return _num_q("Round %s to the nearest whole number." % _dec_text(v), w, "int",
                      solution=["The tenths digit is %d, which is less than 5."
                                % ((v // 10) % 10),
                                "So %s rounds down to %d." % (_dec_text(v), w)])

    if t == 9:                       # estimate a sum by rounding
        a, b = _v(), _v()
        ra, rb = _round_half_up(a / 100.0), _round_half_up(b / 100.0)
        return _num_q("Round each number to the nearest whole number, then add to estimate:  %s + %s"
                      % (_dec_text(a), _dec_text(b)), ra + rb, "int",
                      solution=["%s rounds to %d and %s rounds to %d." % (_dec_text(a), ra, _dec_text(b), rb),
                                "%d + %d = %d." % (ra, rb, ra + rb)])

    if t == 10:                      # closer to which whole number
        w = random.randint(1, 9) if d == 0 else random.randint(1, 19)
        f = random.choice([x for x in range(1, 10) if x != 5])
        v = w * 100 + 10 * f
        if d == 2:                   # stretch: two decimal places, right next to the half
            v = w * 100 + random.randint(41, 59)
            while v % 100 == 50:
                v = w * 100 + random.randint(41, 59)
            near = w if v % 100 < 50 else w + 1
            return _num_q("Is %s closer to %d or to %d? Write the closer whole number."
                          % (_dec_text(v), w, w + 1), near, "int",
                          solution=["%s is %s past %d, and halfway is %d.5."
                                    % (_dec_text(v), _dec_text(v % 100), w, w),
                                    "So it is closer to %d." % near])
        return _num_q("Is %s closer to %d or to %d? Write the closer whole number." % (_dec_text(v), w, w + 1),
                      w if f < 5 else w + 1, "int",
                      solution=["%s is %s tenths past %d." % (_dec_text(v), n_words(f), w),
                                "So it is closer to %d." % (w if f < 5 else w + 1)])

    if t == 11:                      # how many in a list round to a target
        w = random.randint(3, 15)
        near, far = _by_d(d, ((-4, 4, 10), (6, 9, 10)), ((-49, 49, 1), (51, 99, 1)),
                          ((-50, 49, 1), (51, 60, 1)))   # (lo, hi, step) in hundredths
        vals = []
        n_far = random.randint(1, 2)
        while len(vals) < 3 + n_far:
            if len(vals) < 3:
                v = w * 100 + random.randint(near[0], near[1]) * near[2]
            else:
                v = w * 100 + pick([-1, 1]) * random.randint(far[0], far[1]) * far[2]
            if v not in vals:
                vals.append(v)
        random.shuffle(vals)
        k = sum(1 for v in vals if _round_half_up(v / 100.0) == w)
        return _num_q("How many of these round to %d?   %s" % (w, ", ".join(_dec_text(v) for v in vals)), k, "int",
                      solution=["Numbers from %s up to (but not including) %s round to %d."
                                % (_dec_text(w * 100 - 50), _dec_text(w * 100 + 50), w),
                                "%d of them do." % k])

    if t == 12:                      # mass / time contexts
        who = pick(NAMES)
        v = _m(105, 995)
        what, unit = pick([("%s's parcel weighs %s kg.", "kg"), ("%s's rope is %s m long.", "m"),
                           ("%s's pumpkin weighs %s kg.", "kg")])
        return _num_q((what % (who, _dec_text(v))) + " Round this to the nearest whole number.",
                      _round_half_up(v / 100.0), "int", unit=unit,
                      solution=["The tenths digit is %d." % ((v // 10) % 10),
                                "%s rounds to %d." % (_dec_text(v), _round_half_up(v / 100.0))])

    # how much must be added to reach the next whole number
    v = _v()
    up = (int(math.ceil(v / 100.0))) * 100
    if up == v:
        up = v + 100
    return _num_q("How much must be added to %s to make the next whole number?"
                  % _dec_text(v), _h(up - v), "num",
                  solution=["The next whole number after %s is %d."
                            % (_dec_text(v), up // 100),
                            "%d − %s = %s." % (up // 100, _dec_text(v),
                                               _dec_text(up - v))])


@skill("Y4.6.h", "Divide by 10 and 100 to give decimals", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 2, 1, 1, 1])

    if t == 0:                       # ÷ 10
        n = random.randint(_by_d(d, 11, 12, 101), _by_d(d, 99, 199, 999))
        return _num_q("What is %d ÷ 10?" % n, round(n / 10.0, 2), "num",
                      solution=["Dividing by 10 moves every digit one place "
                                "to the right.",
                                "%d ÷ 10 = %s." % (n, _n(n / 10.0))])

    if t == 1:                       # ÷ 100
        n = random.randint(_by_d(d, 11, 12, 101), _by_d(d, 99, 299, 999))
        return _num_q("What is %d ÷ 100?" % n, round(n / 100.0, 2), "num",
                      solution=["Dividing by 100 moves every digit two places "
                                "to the right.",
                                "%d ÷ 100 = %s." % (n, _n(n / 100.0))])

    if t == 2:                       # missing dividend
        n = random.randint(12, _by_d(d, 99, 199, 899))
        by = pick([10, 100]) if d else 10
        return _num_q("Complete: ___ ÷ %d = %s" % (by, _n(n / float(by))), n, "int",
                      solution=["Multiply to go back: %s × %d = %d."
                                % (_n(n / float(by)), by, n)])

    if t == 3:                       # two steps
        n = _by_d(d, random.randint(1, 9) * 10, random.randint(12, 99), random.randint(101, 999))
        return _num_q("What is %d ÷ 10 ÷ 10?" % n, round(n / 100.0, 2), "num",
                      solution=["%d ÷ 10 = %s." % (n, _n(n / 10.0)),
                                "%s ÷ 10 = %s." % (_n(n / 10.0), _n(n / 100.0))])

    if t == 4:                       # inverse: × 10 or × 100
        c = _by_d(d, random.randint(1, 9) * 10, random.randint(1, 99), random.randint(101, 999))
        by = 10 if d == 0 else pick([10, 100])
        return _num_q("What is %s × %d?" % (_dec_text(c), by),
                      round(c * by / 100.0, 2), "num",
                      solution=["Multiplying by %d moves every digit %s place%s "
                                "to the left."
                                % (by, "one" if by == 10 else "two",
                                   "" if by == 10 else "s"),
                                "%s × %d = %s." % (_dec_text(c), by,
                                                   _n(c * by / 100.0))])

    if t == 5:                       # sharing money word problem
        who = pick(NAMES)
        by = _by_d(d, 10, pick([10, 100]), 100)
        per = _by_d(d, random.randint(2, 9), random.randint(5, 95), random.randint(11, 99))
        total = per * by
        return _num_q("%d identical %s cost %s altogether. How much does one cost, "
                      "in pence?" % (by, _plural(pick(_SHOP)), money(total)), per, "int",
                      unit="p",
                      solution=["%d ÷ %d = %d." % (total, by, per),
                                "One costs %s." % money(per)])

    if t == 6:                       # measures conversion by dividing
        kind = pick([("cm", "m", 100), ("mm", "cm", 10), ("g", "kg", 1000),
                     ("ml", "l", 1000)])
        small, big, factor = kind
        if factor == 1000:
            small, big, factor = pick([("cm", "m", 100), ("mm", "cm", 10)])
        if d == 0:
            small, big, factor = "mm", "cm", 10
        elif d == 2:                 # stretch: fewer than 100 cm, so a 0 before the digits
            small, big, factor = "cm", "m", 100
        v = random.randint(11, 99) if factor == 10 else random.randint(105, 995)
        if d == 2:
            v = pick([random.randint(1, 9), random.choice([x for x in range(11, 100) if x % 10])])
        return _num_q("Convert by dividing: how many %s are the same as %s? "
                      "Give your answer as a decimal."
                      % (_uname(big), _pl(v, _uname(small)[:-1])),
                      round(v / float(factor), 2), "num", unit=big,
                      solution=["%d %s = 1 %s, so divide by %d."
                                % (factor, small, big, factor),
                                "%d ÷ %d = %s %s." % (v, factor,
                                                      _n(v / float(factor)), big)])

    if t == 7:                       # place the result on a number line
        if d == 2:                   # stretch: ÷ 100 onto a hundredths line
            n = random.randint(1, 99)
            return _line_q("Work out %d ÷ 100 and place the answer on the number line." % n,
                           round(n / 100.0, 2), 0, 1, 0.01, 0.1,
                           ["Dividing by 100 moves the digits two places to the right.",
                            "%d ÷ 100 = %s." % (n, _n(n / 100.0))])
        n = random.randint(1, 9) * 10 + random.randint(1, 9) if d == 0 else \
            random.randint(1, 19) * 10 + random.randint(0, 9)
        return _line_q("Work out %d ÷ 10 and place the answer on the number line." % n,
                       round(n / 10.0, 2), 0, 10 if d == 0 else 20, 0.1, 1 if d == 0 else 5,
                       ["Dividing by 10 moves the digits one place to the right.",
                        "%d ÷ 10 = %s." % (n, _n(n / 10.0))])

    if t == 8:                       # what was divided by what
        n = _by_d(d, random.randint(11, 99), random.randint(2, 9) * 100 + random.randint(1, 99),
                  random.randint(1, 9))      # stretch: 7 ÷ ___ = 0.07
        by = pick([10, 100])
        return _num_q("%s ÷ ___ = %s. Write the missing number (10 or 100)."
                      % (_n(n / 1.0), _n(n / float(by))), by, "int",
                      solution=["The digits have moved %s to the right."
                                % ("one place" if by == 10 else "two places"),
                                "So the number was divided by %d." % by])

    # single digit ÷ 100
    n = random.randint(1, 9)
    if d == 0:                       # easy: single digit ÷ 10
        return _num_q("What is %d ÷ 10?" % n, round(n / 10.0, 2), "num",
                      solution=["%d ÷ 10 gives %s." % (n, _pl(n, "tenth")),
                                "That is 0.%d." % n])
    if d == 2:                       # stretch: a multiple of ten ÷ 100
        return _num_q("What is %d ÷ 100?" % (n * 10), round(n / 10.0, 2), "num",
                      solution=["%d ÷ 100 gives %s, which is %s." % (n * 10, _pl(n * 10, "hundredth"),
                                                                   _pl(n, "tenth")),
                                "That is 0.%d." % n])
    return _num_q("What is %d ÷ 100?" % n, round(n / 100.0, 2), "num",
                  solution=["%d ÷ 100 gives %s." % (n, _pl(n, "hundredth")),
                            "That is 0.0%d." % n])


@skill("Y4.6.i", "Add and subtract decimals", S6)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 2, 1, 1])
    hi = _by_d(d, 90, 900, 2000)

    if t == 0:                       # add tenths / hundredths
        step = 10 if d == 0 else 1
        a = random.randrange(step, hi, step)
        b = random.randrange(step, hi, step)
        return _num_q("Work out %s + %s." % (_dec_text(a), _dec_text(b)),
                      _h(a + b), "num",
                      solution=["Line up the decimal points.",
                                "%s + %s = %s." % (_dec_text(a), _dec_text(b),
                                                   _dec_text(a + b))])

    if t == 1:                       # subtract
        step = 10 if d == 0 else 1
        a = random.randrange(step * 3, hi, step)
        b = random.randrange(step, a, step)
        return _num_q("Work out %s − %s." % (_dec_text(a), _dec_text(b)),
                      _h(a - b), "num",
                      solution=["Line up the decimal points.",
                                "%s − %s = %s." % (_dec_text(a), _dec_text(b),
                                                   _dec_text(a - b))])

    if t == 2:                       # missing addend
        a = random.randint(10, hi)
        b = random.randint(10, hi)
        return _num_q("Complete: %s + ___ = %s" % (_dec_text(a), _dec_text(a + b)),
                      _h(b), "num",
                      solution=["%s − %s = %s." % (_dec_text(a + b), _dec_text(a),
                                                   _dec_text(b))])

    if t == 3:                       # money total (in pounds)
        a = _by_d(d, random.randint(11, 49) * 10, random.randint(105, 995), random.randint(1005, 1995))
        b = _by_d(d, random.randint(11, 49) * 10, random.randint(105, 995), random.randint(155, 995))
        who = pick(NAMES)
        return _num_q("%s buys %s for %s and %s for %s. What is the total cost, "
                      "in pounds? Write it like 4.75."
                      % (who, _a(pick(_SHOP)), money(a), _a(pick(_GIFTS)), money(b)),
                      round((a + b) / 100.0, 2), "num",
                      solution=["%s + %s = %s." % (money(a), money(b), money(a + b)),
                                "In pounds that is %s." % _n((a + b) / 100.0)])

    if t == 4:                       # money difference (in pounds)
        a = random.randint(210, 1990)
        b = random.randint(105, a - 50)
        if d == 0:                   # whole tens of pence, no exchanging
            a = random.randint(2, 9) * 100 + random.randint(1, 9) * 10
            b = random.randint(1, a // 100 - 1) * 100 + random.randint(0, (a % 100) // 10) * 10
        elif d == 2:                 # stretch: the pence must be exchanged
            a = random.randint(10, 49) * 100 + random.randint(0, 40)
            b = random.randint(1, a // 100 - 1) * 100 + random.randint(a % 100 + 1, 99)
        return _num_q("A coat costs %s and a jumper costs %s. How much more does the "
                      "coat cost, in pounds? Write it like 4.75."
                      % (money(a), money(b)),
                      round((a - b) / 100.0, 2), "num",
                      solution=["%s − %s = %s." % (money(a), money(b), money(a - b)),
                                "In pounds that is %s." % _n((a - b) / 100.0)])

    if t == 5:                       # measures: lengths in metres
        a = _by_d(d, random.randint(11, 45) * 10, random.randint(105, 950), random.randint(555, 1950))
        b = _by_d(d, random.randint(11, 45) * 10, random.randint(105, 950), random.randint(555, 1950))
        return _num_q("A rope is %s m long and another rope is %s m long. "
                      "What is their total length, in metres?"
                      % (_dec_text(a), _dec_text(b)),
                      _h(a + b), "num", unit="m",
                      solution=["%s + %s = %s m." % (_dec_text(a), _dec_text(b),
                                                     _dec_text(a + b))])

    if t == 6:                       # complements to a whole number
        v = random.randint(1, 9) * 100 + (random.randint(1, 9) * 10 if d == 0 else random.randint(1, 99))
        nxt = (v // 100 + (2 if d == 2 else 1)) * 100   # stretch: past the next whole number
        return _num_q("What must be added to %s to make %d?"
                      % (_dec_text(v), nxt // 100), _h(nxt - v), "num",
                      solution=["%d − %s = %s." % (nxt // 100, _dec_text(v),
                                                   _dec_text(nxt - v))])

    if t == 7:                       # hundredths square model
        a = random.randint(10, 60)
        b = random.randint(10, 100 - a)
        if d == 0:                   # whole tenths
            a = random.randint(1, 6) * 10
            b = random.randint(1, 10 - a // 10) * 10
        elif d == 2:                 # stretch: the hundredths make a new tenth
            a = random.randint(1, 5) * 10 + random.randint(5, 9)
            b = random.randint(1, (100 - a) // 10 - 1) * 10 + random.randint(10 - a % 10, 9)
        return {"prompt": "Work out %s + %s, then shade the hundredths square to show "
                          "your answer." % (_dec_text(a), _dec_text(b)),
                "component": "area_grid", "spec": {"mode": "fraction", "parts": 100},
                "answer": "%d/100" % (a + b), "answer_type": "frac",
                "solution": ["%s + %s = %s." % (_dec_text(a), _dec_text(b),
                                                _dec_text(a + b)),
                             "Shade %d of the 100 small squares." % (a + b)]}

    if t == 8:                       # capacity word problem
        who = pick(NAMES)
        a = random.randint(105, 490)
        b = random.randint(20, 99)
        if d == 0:
            a = random.randint(1, 4) * 100 + random.randint(1, 9) * 10
            b = random.randint(1, (a % 100) // 10) * 10     # no exchanging
        elif d == 2:                 # stretch: exchange a whole litre
            a = random.randint(1, 4) * 100 + random.randint(1, 40)
            b = random.randint(a % 100 + 1, 99)
        return _num_q("%s has %s litres of juice and drinks %s litres of it. "
                      "How much juice is left, in litres?"
                      % (who, _dec_text(a), _dec_text(b)),
                      _h(a - b), "num", unit="l",
                      solution=["%s − %s = %s l." % (_dec_text(a), _dec_text(b),
                                                     _dec_text(a - b))])

    # three-part total in a price list
    names = random.sample(_SHOP, 3)
    prices = [_by_d(d, random.randint(5, 65) * 10, random.randint(45, 650),
                    random.randint(255, 999)) for _ in names]
    rows = [[nm.capitalize(), money(p)] for nm, p in zip(names, prices)]
    return _table_q("The price list shows three items. What do all three cost "
                    "altogether, in pounds? Write it like 4.75.",
                    ["Item", "Price"], rows,
                    round(sum(prices) / 100.0, 2), "num",
                    ["%s = %s." % (" + ".join(money(p) for p in prices),
                                   money(sum(prices))),
                     "In pounds that is %s." % _n(sum(prices) / 100.0)])


# =============================================================== 4.7 =========
_LEN_UNITS = [("km", "m", 1000, "1 km = 1000 m"),
              ("m", "cm", 100, "1 m = 100 cm"),
              ("cm", "mm", 10, "1 cm = 10 mm"),
              ("m", "mm", 1000, "1 m = 1000 mm")]


@skill("Y4.7.a", "Convert units of length", S7)
def _(d=1):
    d = _tier(d)
    big, small, factor, fact = pick(_by_d(d, _LEN_UNITS[1:3], _LEN_UNITS, _LEN_UNITS))
    t = _pick_t([1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2])

    if t == 10:                      # conversion table of metric units (m and cm)
        if d == 0:
            big, small, factor, fact = _LEN_UNITS[1]      # 1 m = 100 cm
        vals = []
        rows = []
        while len(vals) < 4:
            v = random.randint(2, _by_d(d, 9, 15, 25))
            if v not in vals:
                vals.append(v)
                rows.append(["%d %s" % (v, big), "%d %s" % (v * factor, small)])
        k = random.randrange(4)
        if random.random() < 0.5:
            return _table_q("This conversion table changes between metric units. "
                            "What number belongs in the blank cell, in %s?"
                            % _uname(small),
                            ["Length in %s" % big, "Length in %s" % small], rows,
                            vals[k] * factor, "int",
                            [fact + ".",
                             "%d × %d = %d %s." % (vals[k], factor,
                                                   vals[k] * factor, small)],
                            missing=(k, 1))
        return _table_q("This conversion table changes between metric units. "
                        "What number belongs in the blank cell, in %s?"
                        % _uname(big),
                        ["Length in %s" % big, "Length in %s" % small], rows,
                        vals[k], "int",
                        [fact + ".",
                         "%d ÷ %d = %d %s." % (vals[k] * factor, factor,
                                               vals[k], big)],
                        missing=(k, 0))

    if t == 0:                       # big -> small
        v = random.randint(2, _by_d(d, 9, 20, 45))
        return _num_q("How many %s are there in %d %s?"
                      % (_uname(small), v, _uname(big)),
                      v * factor, "int", unit=small,
                      solution=[fact + ".",
                                "%d × %d = %d %s." % (v, factor, v * factor, small)])

    if t == 1:                       # small -> big
        v = random.randint(2, _by_d(d, 9, 20, 45))
        return _num_q("How many %s are there in %d %s?"
                      % (_uname(big), v * factor, _uname(small)),
                      v, "int", unit=big,
                      solution=[fact + ".",
                                "%d ÷ %d = %d %s." % (v * factor, factor, v, big)])

    if t == 2:                       # mixed units -> small
        v = random.randint(1, 9)
        extra = random.randint(1, factor - 1)
        return _num_q("Write %d %s %d %s in %s." % (v, big, extra, small, small),
                      v * factor + extra, "int", unit=small,
                      solution=[fact + ", so %d %s = %d %s."
                                % (v, big, v * factor, small),
                                "%d + %d = %d %s." % (v * factor, extra,
                                                      v * factor + extra, small)])

    if t == 3:                       # small -> mixed (ask for the leftover)
        v = random.randint(1, 9)
        extra = random.randint(1, factor - 1)
        total = v * factor + extra
        return _num_q("%d %s is the same as %d %s and how many %s?"
                      % (total, small, v, big, small),
                      extra, "int", unit=small,
                      solution=["%d %s = %d %s." % (v, big, v * factor, small),
                                "%d − %d = %d %s." % (total, v * factor, extra, small)])

    if t == 4:                       # comparison
        v = random.randint(2, 9)
        other = random.randint(v * factor - factor + 5, v * factor + factor - 5)
        while other == v * factor:
            other = random.randint(1, v * factor + factor)
        return _num_q("Which is longer, %d %s or %d %s? Write the longer length in %s."
                      % (v, big, other, small, small),
                      max(v * factor, other), "int", unit=small,
                      solution=[fact + ", so %d %s = %d %s."
                                % (v, big, v * factor, small),
                                "The longer length is %d %s."
                                % (max(v * factor, other), small)])

    if t == 5:                       # ruler reading, then convert
        mx = _by_d(d, 10, 20, 30)
        v = random.randint(1, mx)
        return {"prompt": "Read the ruler, then convert: how long is the line in "
                          "millimetres?",
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm", "answer_unit": "mm"},
                "answer": v * 10, "answer_type": "int",
                "solution": ["The line measures %d cm." % v,
                             "1 cm = 10 mm, so %d cm = %d mm." % (v, v * 10)]}

    if t == 6:                       # word problem
        v = random.randint(2, 9)
        extra = random.randint(10, max(11, factor - 10))
        thing = "path" if big == "km" else ("rope" if big == "m" else "ribbon")
        return _num_q("One %s is %d %s long and another %s is %d %s long. "
                      "What is their total length, in %s?"
                      % (thing, v, big, thing, extra, small, _uname(small)),
                      v * factor + extra, "int", unit=small,
                      solution=[fact + ", so %d %s = %d %s."
                                % (v, big, v * factor, small),
                                "%d + %d = %d %s." % (v * factor, extra,
                                                      v * factor + extra, small)])

    if t == 7:                       # conversion table with a missing cell
        rows = []
        vals = []
        for v in random.sample(range(2, 13), 3):
            vals.append(v)
            rows.append(["%d %s" % (v, big), "%d %s" % (v * factor, small)])
        k = random.randrange(3)
        return _table_q("Complete the conversion table: how many %s go in the blank "
                        "cell?" % _uname(small),
                        [big, small], rows, vals[k] * factor, "int",
                        [fact + ".",
                         "%d × %d = %d %s." % (vals[k], factor,
                                               vals[k] * factor, small)],
                        missing=(k, 1))

    if t == 8:                       # decimal conversion
        v = random.randrange(110, 1000, 10) if factor == 1000 else random.randint(105, 995)
        return _num_q("Write %d %s in %s as a decimal."
                      % (v, small, _uname(big)),
                      round(v / float(factor), 3), "num", unit=big,
                      solution=[fact + ", so divide by %d." % factor,
                                "%d ÷ %d = %s %s." % (v, factor,
                                                      _n(round(v / float(factor), 3)),
                                                      big)])

    # missing number in a conversion sentence
    v = random.randint(2, 9)
    return _num_q("Complete: ___ %s = %d %s" % (small, v, big), v * factor, "int",
                  unit=small,
                  solution=[fact + ".",
                            "%d × %d = %d %s." % (v, factor, v * factor, small)])


@skill("Y4.7.b", "Convert units of mass", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2])

    if t == 10:                      # conversion table of metric units (kg and g)
        vals = []
        rows = []
        while len(vals) < 4:
            v = random.randint(1, _by_d(d, 9, 12, 20))
            if v not in vals:
                vals.append(v)
                rows.append(["%d kg" % v, "%d g" % (v * 1000)])
        k = random.randrange(4)
        if random.random() < 0.5:
            return _table_q("This conversion table changes between metric units. "
                            "What number belongs in the blank cell, in grams?",
                            ["Mass in kg", "Mass in g"], rows,
                            vals[k] * 1000, "int",
                            ["1 kg = 1000 g.",
                             "%d × 1000 = %d g." % (vals[k], vals[k] * 1000)],
                            missing=(k, 1))
        return _table_q("This conversion table changes between metric units. "
                        "What number belongs in the blank cell, in kilograms?",
                        ["Mass in kg", "Mass in g"], rows, vals[k], "int",
                        ["1000 g = 1 kg.",
                         "%d ÷ 1000 = %d kg." % (vals[k] * 1000, vals[k])],
                        missing=(k, 0))

    if t == 0:                       # kg -> g
        v = random.randint(2, _by_d(d, 5, 12, 30))
        return _num_q("How many grams are there in %d kg?" % v, v * 1000, "int",
                      unit="g",
                      solution=["1 kg = 1000 g.",
                                "%d × 1000 = %d g." % (v, v * 1000)])

    if t == 1:                       # g -> kg
        v = random.randint(2, _by_d(d, 5, 12, 30))
        return _num_q("How many kilograms are there in %d g?" % (v * 1000), v, "int",
                      unit="kg",
                      solution=["1000 g = 1 kg.",
                                "%d ÷ 1000 = %d kg." % (v * 1000, v)])

    if t == 2:                       # mixed -> g
        kg = random.randint(1, 5 if d == 0 else 9)
        g = _small_part(d, [100, 200, 500], [100, 200, 250, 500, 750, 50, 350])
        return _num_q("Write %d kg %d g in grams." % (kg, g), kg * 1000 + g, "int",
                      unit="g",
                      solution=["%d kg = %d g." % (kg, kg * 1000),
                                "%d + %d = %d g." % (kg * 1000, g, kg * 1000 + g)])

    if t == 3:                       # g -> mixed (leftover)
        kg = random.randint(1, 5 if d == 0 else 9)
        g = _small_part(d, list(range(100, 1000, 100)), list(range(50, 1000, 50)))
        total = kg * 1000 + g
        return _num_q("%d g is the same as %d kg and how many grams?" % (total, kg),
                      g, "int", unit="g",
                      solution=["%d kg = %d g." % (kg, kg * 1000),
                                "%d − %d = %d g." % (total, kg * 1000, g)])

    if t == 4:                       # scales reading -> convert
        v = random.randrange(100, 1001, _by_d(d, 100, 50, 25))
        return {"prompt": "Read the scales. What is the mass, in grams?",
                "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v, "answer_type": "int",
                "solution": ["The pointer is at %d g." % v,
                             "That is %s of a kilogram." % ("%.3f" % (v / 1000.0)).rstrip("0").rstrip(".")]}

    if t == 5:                       # comparison
        kg = random.randint(1, 6)
        g = random.randrange(500, 6500, 100)
        while g == kg * 1000:
            g = random.randrange(500, 6500, 100)
        if d == 0:                   # far apart
            kg = random.randint(1, 4)
            g = pick([kg * 1000 - 500, kg * 1000 + random.randint(1, 4) * 500])
        elif d == 2:                 # stretch: within 100 g of each other
            kg = random.randint(2, 9)
            g = kg * 1000 + pick([-1, 1]) * random.randint(1, 9) * 10
        return _num_q("Which is heavier, %d kg or %d g? Write the heavier mass in grams."
                      % (kg, g), max(kg * 1000, g), "int", unit="g",
                      solution=["%d kg = %d g." % (kg, kg * 1000),
                                "The heavier mass is %d g." % max(kg * 1000, g)])

    if t == 6:                       # word problem
        who = pick(NAMES)
        kg = random.randint(1, 5)
        used = random.randrange(100, 900, 50)
        if d == 0:
            kg, used = random.randint(1, 3), random.randrange(100, 1000, 100)
        elif d == 2:                 # stretch: uses more than a kilogram, to the 10 g
            kg = random.randint(2, 6)
            used = random.randrange(1010, kg * 1000 - 50, 10)
        return _num_q("%s has a %d kg bag of flour and uses %d g of it. "
                      "How much flour is left, in grams?" % (who, kg, used),
                      kg * 1000 - used, "int", unit="g",
                      solution=["%d kg = %d g." % (kg, kg * 1000),
                                "%d − %d = %d g." % (kg * 1000, used,
                                                     kg * 1000 - used)])

    if t == 7:                       # decimal kilograms
        g = _by_d(d, random.randint(1, 9) * 1000 + 500, random.randrange(100, 9900, 100),
                  random.choice([x for x in range(10, 9990, 10) if x % 100]))
        return _num_q("Write %d g in kilograms as a decimal." % g,
                      round(g / 1000.0, 3), "num", unit="kg",
                      solution=["1000 g = 1 kg, so divide by 1000.",
                                "%d ÷ 1000 = %s kg." % (g, _n(round(g / 1000.0, 3)))])

    if t == 8:                       # conversion table
        rows = []
        vals = []
        for v in random.sample(range(1, _by_d(d, 6, 10, 20)), 3):
            if d == 2:               # stretch: half kilograms
                v += 0.5
            vals.append(v)
            rows.append(["%s kg" % _n(v), "%d g" % (v * 1000)])
        k = random.randrange(3)
        return _table_q("Complete the conversion table: how many grams go in the "
                        "blank cell?", ["Mass in kg", "Mass in g"], rows,
                        int(vals[k] * 1000), "int",
                        ["1 kg = 1000 g.",
                         "%s × 1000 = %d g." % (_n(vals[k]), vals[k] * 1000)],
                        missing=(k, 1))

    # half and quarter kilograms
    frac_n, frac_d, grams = pick(_by_d(d, [(1, 2, 500), (1, 4, 250), (1, 10, 100)],
                                       [(1, 2, 500), (1, 4, 250), (3, 4, 750),
                                        (1, 10, 100), (1, 5, 200)],
                                       [(3, 4, 750), (2, 5, 400), (3, 5, 600),
                                        (3, 10, 300), (7, 10, 700), (1, 100, 10)]))
    return _num_q("How many grams are there in %s of a kilogram?"
                  % _frac_words(frac_n, frac_d), grams, "int", unit="g",
                  solution=["1 kg = 1000 g.",
                            "%d/%d of 1000 = %d g." % (frac_n, frac_d, grams)])


@skill("Y4.7.c", "Convert units of capacity", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2])

    if t == 10:                      # conversion table of metric units (l and ml)
        vals = []
        rows = []
        while len(vals) < 4:
            v = random.randint(1, _by_d(d, 9, 12, 20))
            if v not in vals:
                vals.append(v)
                rows.append(["%d l" % v, "%d ml" % (v * 1000)])
        k = random.randrange(4)
        if random.random() < 0.5:
            return _table_q("This conversion table changes between metric units. "
                            "What number belongs in the blank cell, in millilitres?",
                            ["Capacity in l", "Capacity in ml"], rows,
                            vals[k] * 1000, "int",
                            ["1 l = 1000 ml.",
                             "%d × 1000 = %d ml." % (vals[k], vals[k] * 1000)],
                            missing=(k, 1))
        return _table_q("This conversion table changes between metric units. "
                        "What number belongs in the blank cell, in litres?",
                        ["Capacity in l", "Capacity in ml"], rows, vals[k], "int",
                        ["1000 ml = 1 litre.",
                         "%d ÷ 1000 = %s." % (vals[k] * 1000, _pl(vals[k], "litre"))],
                        missing=(k, 0))

    if t == 11:                      # greater or smaller volume
        l = random.randint(1, _by_d(d, 3, 5, 8))
        ml = random.randrange(_by_d(d, 500, 250, 100), (l + 1) * 1000,
                              _by_d(d, 500, 250, 50))
        while ml == l * 1000:
            ml = random.randrange(_by_d(d, 500, 250, 100), (l + 1) * 1000,
                                  _by_d(d, 500, 250, 50))
        bigger = max(l * 1000, ml)
        smaller = min(l * 1000, ml)
        if random.random() < 0.5:
            return _num_q("One bottle holds %s and one jug holds %d ml. "
                          "Which is the greater volume? Write the greater volume "
                          "in millilitres." % (_pl(l, "litre"), ml),
                          bigger, "int", unit="ml",
                          solution=["%d l = %d ml." % (l, l * 1000),
                                    "The greater volume is %d ml." % bigger])
        return _num_q("One bottle holds %s and one jug holds %d ml. "
                      "Which is the smaller volume? Write the smaller volume "
                      "in millilitres." % (_pl(l, "litre"), ml),
                      smaller, "int", unit="ml",
                      solution=["%d l = %d ml." % (l, l * 1000),
                                "The smaller volume is %d ml." % smaller])

    if t == 0:                       # l -> ml
        v = random.randint(2, _by_d(d, 5, 12, 30))
        return _num_q("How many millilitres are there in %d litres?" % v, v * 1000,
                      "int", unit="ml",
                      solution=["1 litre = 1000 ml.",
                                "%d × 1000 = %d ml." % (v, v * 1000)])

    if t == 1:                       # ml -> l
        v = random.randint(2, _by_d(d, 5, 12, 30))
        return _num_q("How many litres are there in %d ml?" % (v * 1000), v, "int",
                      unit="l",
                      solution=["1000 ml = 1 litre.",
                                "%d ÷ 1000 = %s." % (v * 1000, _pl(v, "litre"))])

    if t == 2:                       # mixed -> ml
        l = random.randint(1, 5 if d == 0 else 9)
        ml = _small_part(d, [100, 200, 500], [100, 250, 500, 750, 50, 400])
        return _num_q("Write %d l %d ml in millilitres." % (l, ml), l * 1000 + ml,
                      "int", unit="ml",
                      solution=["%d l = %d ml." % (l, l * 1000),
                                "%d + %d = %d ml." % (l * 1000, ml, l * 1000 + ml)])

    if t == 3:                       # ml -> mixed (leftover)
        l = random.randint(1, 5 if d == 0 else 9)
        ml = _small_part(d, list(range(100, 1000, 100)), list(range(50, 1000, 50)))
        total = l * 1000 + ml
        return _num_q("%d ml is the same as %s and how many millilitres?"
                      % (total, _pl(l, "litre")), ml, "int", unit="ml",
                      solution=["%d l = %d ml." % (l, l * 1000),
                                "%d − %d = %d ml." % (total, l * 1000, ml)])

    if t == 4:                       # jug reading
        v = random.randrange(_by_d(d, 100, 50, 25), 1001, _by_d(d, 100, 50, 25))
        return {"prompt": "Read the measuring jug. How much liquid is in it, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v, "answer_type": "int",
                "solution": ["The liquid reaches the %d ml mark." % v,
                             "That is %s of a litre." % _n(v / 1000.0)]}

    if t == 5:                       # how much more to fill a litre (visual)
        step = _by_d(d, 100, 50, 25)
        v = random.randrange(step, 1000, step)
        return {"prompt": "The jug shows some juice. How much more juice is needed "
                          "to make 1 litre, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": 1000 - v, "answer_type": "int",
                "solution": ["1 litre = 1000 ml and the jug shows %d ml." % v,
                             "1000 − %d = %d ml." % (v, 1000 - v)]}

    if t == 6:                       # word problem
        who = pick(NAMES)
        cups = random.randint(*_by_d(d, (2, 4), (2, 6), (4, 9)))
        per = random.choice(_by_d(d, [100, 200, 250], [150, 200, 250], [125, 175, 225, 275]))
        l = random.randint(int(math.ceil(cups * per / 1000.0)) + 1, 6)
        return _num_q("%s pours %d cups of squash from a %d litre bottle. Each cup "
                      "holds %d ml. How much squash is left in the bottle, in ml?"
                      % (who, cups, l, per),
                      l * 1000 - cups * per, "int", unit="ml",
                      solution=["%d × %d = %d ml poured out." % (cups, per, cups * per),
                                "%d − %d = %d ml left." % (l * 1000, cups * per,
                                                           l * 1000 - cups * per)])

    if t == 7:                       # decimal litres
        ml = _by_d(d, random.randint(1, 9) * 1000 + 500, random.randrange(100, 9900, 100),
                   random.choice([x for x in range(10, 9990, 10) if x % 100]))
        return _num_q("Write %d ml in litres as a decimal." % ml,
                      round(ml / 1000.0, 3), "num", unit="l",
                      solution=["1000 ml = 1 litre, so divide by 1000.",
                                "%d ÷ 1000 = %s l." % (ml, _n(round(ml / 1000.0, 3)))])

    if t == 8:                       # conversion table
        rows = []
        vals = []
        for v in random.sample(range(1, _by_d(d, 6, 10, 20)), 3):
            if d == 2:               # stretch: half litres
                v += 0.5
            vals.append(v)
            rows.append(["%s l" % _n(v), "%d ml" % (v * 1000)])
        k = random.randrange(3)
        return _table_q("Complete the conversion table: how many millilitres go in "
                        "the blank cell?", ["Capacity in l", "Capacity in ml"], rows,
                        int(vals[k] * 1000), "int",
                        ["1 l = 1000 ml.",
                         "%s × 1000 = %d ml." % (_n(vals[k]), vals[k] * 1000)],
                        missing=(k, 1))

    # fractions of a litre
    frac_n, frac_d, mls = pick(_by_d(d, [(1, 2, 500), (1, 4, 250), (1, 10, 100)],
                                     [(1, 2, 500), (1, 4, 250), (3, 4, 750),
                                      (1, 10, 100), (1, 5, 200)],
                                     [(3, 4, 750), (2, 5, 400), (3, 5, 600),
                                      (3, 10, 300), (7, 10, 700), (1, 100, 10)]))
    return _num_q("How many millilitres are there in %s of a litre?"
                  % _frac_words(frac_n, frac_d), mls, "int", unit="ml",
                  solution=["1 litre = 1000 ml.",
                            "%d/%d of 1000 = %d ml." % (frac_n, frac_d, mls)])


_UNIT_CHOICE = [
    ("the length of a pencil", "centimetres"),
    ("the thickness of a coin", "millimetres"),
    ("the height of a door", "metres"),
    ("the distance between two towns", "kilometres"),
    ("the length of a football pitch", "metres"),
    ("the width of a fingernail", "millimetres"),
    ("the mass of a strawberry", "grams"),
    ("the mass of a car", "kilograms"),
    ("the mass of a letter", "grams"),
    ("the water in a bath", "litres"),
    ("a spoonful of medicine", "millilitres"),
    ("the juice in a mug", "millilitres"),
]


@skill("Y4.7.d", "Choose units and read scales", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 1, 1, 2, 2, 1, 1, 2])

    if t == 9:                       # measure liquid volumes in metric units
        step = _by_d(d, 100, 50, 50)
        v = random.randrange(step, 1001, step)
        if d == 2 and v % 100 == 0 and v < 1000 and random.random() < 0.5:
            return {"prompt": "Measure the liquid volume in the jug, then write it "
                              "in metric units: how many litres of liquid are in "
                              "the jug? Write the volume as a decimal.",
                    "component": "ruler",
                    "spec": {"mode": "capacity", "value": v, "max": 1000,
                             "unit": "ml"},
                    "answer": round(v / 1000.0, 3), "answer_type": "num",
                    "solution": ["The liquid reaches the %d ml mark." % v,
                                 "1000 ml = 1 litre, so %d ml = %s litres."
                                 % (v, _n(round(v / 1000.0, 3)))]}
        return {"prompt": "Measure the liquid volume in the jug. How many "
                          "millilitres of liquid are in the jug?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v, "answer_type": "int",
                "solution": ["Each mark on the jug is %d ml." % step,
                             "The liquid reaches the %d ml mark." % v]}

    if t == 0:                       # read a length scale
        mx = _by_d(d, 10, 20, 30)
        v = random.randint(1, mx)
        thing = pick(["pencil", "leaf", "straw", "crayon", "twig", "ribbon"])
        return {"prompt": "Read the ruler. How long is the %s, in centimetres?" % thing,
                "component": "ruler",
                "spec": {"mode": "length", "value": v, "max": mx, "unit": "cm"},
                "answer": v, "answer_type": "int",
                "solution": ["Line the %s up with 0 on the ruler." % thing,
                             "The other end reaches %d cm." % v]}

    if t == 1:                       # read a mass scale
        step = _by_d(d, 100, 50, 25)
        v = random.randrange(step, 1001, step)
        return {"prompt": "Read the scales. What is the mass, in grams?",
                "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v, "answer_type": "int",
                "solution": ["Each mark on the scale is %d g." % step,
                             "The pointer is at %d g." % v]}

    if t == 2:                       # read a capacity scale
        step = _by_d(d, 100, 50, 50)
        v = random.randrange(step, 1001, step)
        return {"prompt": "Read the measuring jug. How much liquid is in it, in ml?",
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v, "answer_type": "int",
                "solution": ["Each mark on the jug is %d ml." % step,
                             "The liquid reaches %d ml." % v]}

    if t == 3:                       # choose the unit
        thing, unit = pick(_UNIT_CHOICE)
        return _num_q("Which unit would you use to measure %s: millimetres, "
                      "centimetres, metres, kilometres, grams, kilograms, "
                      "millilitres or litres? Type the unit name in full, as it "
                      "is written in the list." % thing,
                      unit, "str", text=True, placeholder="type the unit name",
                      solution=["%s is best measured in %s."
                                % (thing.capitalize(), unit)])

    if t == 4:                       # choose the measuring tool
        job, tool = pick([
            ("how long the school playground is", "tape measure"),
            ("how heavy a bag of apples is", "scales"),
            ("how much water a bottle holds", "measuring jug"),
            ("how long a pencil is", "ruler"),
            ("how long a lesson lasts", "clock"),
            ("how warm the room is", "thermometer"),
        ])
        return _num_q("Which tool would you use to measure %s: ruler, tape measure, "
                      "scales, measuring jug, clock or thermometer? Type the tool."
                      % job, tool, "str", text=True, placeholder="type the tool",
                      solution=["To measure %s you use %s." % (job, _a(tool))])

    if t == 5:                       # read a scale then add
        step = _by_d(d, 100, 50, 25)
        v = random.randrange(step, 801, step)
        add = random.randrange(step, 201, step)
        return {"prompt": "The scales show some flour. %d g more flour is added. "
                          "What is the new mass, in grams?" % add,
                "component": "ruler",
                "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g"},
                "answer": v + add, "answer_type": "int",
                "solution": ["The scales read %d g." % v,
                             "%d + %d = %d g." % (v, add, v + add)]}

    if t == 6:                       # read a jug then pour out
        v = random.randrange(200, 1001, 50)
        out = random.randrange(50, v, 50)
        return {"prompt": "The jug shows some water. %d ml is poured out. "
                          "How much water is left, in ml?" % out,
                "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"},
                "answer": v - out, "answer_type": "int",
                "solution": ["The jug holds %d ml." % v,
                             "%d − %d = %d ml." % (v, out, v - out)]}

    if t == 7:                       # sensible estimate
        item, val, unit = pick([("a bag of sugar", 1, "kg"),
                                ("a can of drink", 330, "ml"),
                                ("a classroom door", 2, "m"),
                                ("a new pencil", 18, "cm"),
                                ("a large bottle of water", 2, "l"),
                                ("an apple", 150, "g")])
        wrong = val * pick([10, 100])
        first, second = (val, wrong) if random.random() < 0.5 else (wrong, val)
        return _num_q("Which is the sensible measurement for %s: %d %s or %d %s? "
                      "Write the sensible number." % (item, first, unit, second, unit),
                      val, "int", unit=unit,
                      solution=["Think about the size of %s." % item,
                                "The sensible measurement is %d %s." % (val, unit)])

    # scale reading converted to a decimal
    v = random.randrange(100, 1001, 100)
    return {"prompt": "Read the scales, then write the mass in kilograms "
                      "as a decimal.",
            "component": "ruler",
            "spec": {"mode": "mass", "value": v, "max": 1000, "unit": "g", "answer_unit": "kg"},
            "answer": round(v / 1000.0, 3), "answer_type": "num",
            "solution": ["The scales read %d g." % v,
                         "1000 g = 1 kg, so %d g = %s kg."
                         % (v, _n(round(v / 1000.0, 3)))]}


@skill("Y4.7.e", "Imperial units", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    if t == 0:                       # feet -> inches
        f = random.randint(2, _by_d(d, 6, 10, 15))
        return _num_q("There are 12 inches in 1 foot. How many inches are there "
                      "in %d feet?" % f, f * 12, "int", unit="inches",
                      solution=["1 foot = 12 inches.",
                                "%d × 12 = %d inches." % (f, f * 12)])

    if t == 1:                       # inches -> feet
        f = random.randint(2, _by_d(d, 6, 10, 12))
        return _num_q("There are 12 inches in 1 foot. How many feet are there "
                      "in %d inches?" % (f * 12), f, "int", unit="feet",
                      solution=["12 inches = 1 foot.",
                                "%d ÷ 12 = %d feet." % (f * 12, f)])

    if t == 2:                       # pounds -> ounces
        lb = random.randint(2, _by_d(d, 5, 9, 12))
        return _num_q("There are 16 ounces in 1 pound. How many ounces are there "
                      "in %d pounds?" % lb, lb * 16, "int", unit="ounces",
                      solution=["1 pound = 16 ounces.",
                                "%d × 16 = %d ounces." % (lb, lb * 16)])

    if t == 3:                       # ounces -> pounds
        lb = random.randint(2, _by_d(d, 4, 8, 10))
        return _num_q("There are 16 ounces in 1 pound. How many pounds are there "
                      "in %d ounces?" % (lb * 16), lb, "int", unit="pounds",
                      solution=["16 ounces = 1 pound.",
                                "%d ÷ 16 = %d pounds." % (lb * 16, lb)])

    if t == 4:                       # gallons <-> pints
        g = random.randint(2, _by_d(d, 5, 9, 12))
        if random.random() < 0.5:
            return _num_q("There are 8 pints in 1 gallon. How many pints are there "
                          "in %d gallons?" % g, g * 8, "int", unit="pints",
                          solution=["1 gallon = 8 pints.",
                                    "%d × 8 = %d pints." % (g, g * 8)])
        return _num_q("There are 8 pints in 1 gallon. How many gallons are there "
                      "in %d pints?" % (g * 8), g, "int", unit="gallons",
                      solution=["8 pints = 1 gallon.",
                                "%d ÷ 8 = %d gallons." % (g * 8, g)])

    if t == 5:                       # rough metric conversion
        kind = pick([("inches", "centimetres", 1, 2.5, "1 inch is about 2.5 cm"),
                     ("pints", "millilitres", 1, 570, "1 pint is about 570 ml"),
                     ("pounds", "grams", 1, 450, "1 pound is about 450 g"),
                     ("gallons", "litres", 1, 4.5, "1 gallon is about 4.5 litres")])
        src, dst, _one, rate, fact = kind
        v = random.randint(2, _by_d(d, 5, 8, 12))
        ans = round(v * rate, 2)
        return _num_q("%s. About how many %s are there in %d %s?"
                      % (fact.capitalize(), dst, v, src), ans, "num", unit=dst,
                      solution=[fact + ".",
                                "%d × %s = %s %s." % (v, _n(rate), _n(ans), dst)])

    if t == 6:                       # metric -> imperial rough
        kg = random.randint(2, _by_d(d, 5, 9, 12))
        return _num_q("1 kilogram is about 2 pounds. About how many pounds is %d kg?"
                      % kg, kg * 2, "int", unit="pounds",
                      solution=["1 kg is about 2 pounds.",
                                "%d × 2 = about %d pounds." % (kg, kg * 2)])

    if t == 7:                       # comparison
        kind = pick(["length", "mass", "capacity"])
        if kind == "length":
            f = random.randint(1, 5)
            inch = random.randint(f * 12 - 8, f * 12 + 8)
            while inch == f * 12:
                inch = random.randint(1, f * 12 + 10)
            return _num_q("Which is longer, %s or %s? Write the longer "
                          "length in inches." % (_pl(f, "foot", "feet"),
                                                 _pl(inch, "inch", "inches")),
                          max(f * 12, inch), "int", unit="inches",
                          solution=["1 foot = 12 inches, so %d feet = %d inches."
                                    % (f, f * 12),
                                    "The longer length is %d inches."
                                    % max(f * 12, inch)])
        if kind == "mass":
            lb = random.randint(1, 5)
            oz = random.randint(max(1, lb * 16 - 10), lb * 16 + 10)
            while oz == lb * 16:
                oz = random.randint(1, lb * 16 + 12)
            return _num_q("Which is heavier, %s or %s? Write the "
                          "heavier mass in ounces." % (_pl(lb, "pound"),
                                                       _pl(oz, "ounce")),
                          max(lb * 16, oz), "int", unit="ounces",
                          solution=["1 pound = 16 ounces, so %s = %d ounces."
                                    % (_pl(lb, "pound"), lb * 16),
                                    "The heavier mass is %d ounces." % max(lb * 16, oz)])
        g = random.randint(1, 5)
        pt = random.randint(max(1, g * 8 - 6), g * 8 + 6)
        while pt == g * 8:
            pt = random.randint(1, g * 8 + 8)
        return _num_q("Which holds more, %s or %s? Write the larger "
                      "amount in pints." % (_pl(g, "gallon"), _pl(pt, "pint")),
                      max(g * 8, pt), "int",
                      unit="pints",
                      solution=["1 gallon = 8 pints, so %s = %d pints."
                                % (_pl(g, "gallon"), g * 8),
                                "The larger amount is %d pints." % max(g * 8, pt)])

    if t == 8:                       # word problem with a remainder
        who = pick(NAMES)
        f = random.randint(2, 6)
        extra = random.randint(1, 11)
        return _num_q("%s has a plank %s %s long. How long is the plank "
                      "in inches?" % (who, _pl(f, "foot", "feet"),
                                      _pl(extra, "inch", "inches")),
                      f * 12 + extra, "int",
                      unit="inches",
                      solution=["%d feet = %d inches." % (f, f * 12),
                                "%d + %d = %d inches." % (f * 12, extra,
                                                          f * 12 + extra)])

    # imperial conversion table
    rows = []
    vals = []
    for v in random.sample(range(1, 10), 3):
        vals.append(v)
        rows.append(["%d" % v, "%d" % (v * 12)])
    k = random.randrange(3)
    return _table_q("The table converts feet to inches. How many inches go in the "
                    "blank cell?", ["Feet", "Inches"], rows, vals[k] * 12, "int",
                    ["1 foot = 12 inches.",
                     "%d × 12 = %d inches." % (vals[k], vals[k] * 12)],
                    missing=(k, 1))


def _coin_name(p):
    return {100: "£1 coin", 200: "£2 coin", 500: "£5 note", 1000: "£10 note",
            2000: "£20 note"}.get(int(p), "%dp coin" % int(p))


def _coin_list(items):
    bits = []
    for c, v in items:
        nm = _coin_name(v)
        bits.append("%d %s" % (c, nm if c == 1 else nm + "s"))
    if len(bits) == 1:
        return bits[0]
    return ", ".join(bits[:-1]) + " and " + bits[-1]


@skill("Y4.7.f", "Count, compare and order money", S7)
def _(d=1):
    d = _tier(d)
    pool = _by_d(d, [5, 10, 20, 50], [10, 20, 50, 100, 200],
                 [5, 20, 50, 100, 200, 500, 1000])
    t = _pick_t([1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2])

    def _two_groups():
        """Two coin collections of unequal value."""
        n = _by_d(d, 2, 2, 3)
        g1 = [(random.randint(1, 3), v) for v in random.sample(pool, n)]
        g2 = [(random.randint(1, 3), v) for v in random.sample(pool, n)]
        s1 = sum(c * v for c, v in g1)
        s2 = sum(c * v for c, v in g2)
        while s1 == s2:
            g2 = [(random.randint(1, 3), v) for v in random.sample(pool, n)]
            s2 = sum(c * v for c, v in g2)
        return g1, s1, g2, s2

    if t == 10:                      # which collection shows more money?
        g1, s1, g2, s2 = _two_groups()
        return _num_q("Here are two collections of coins. Collection A has %s. "
                      "Collection B has %s. Which collection is worth more? Type A or B."
                      % (_coin_list(g1), _coin_list(g2)),
                      "A" if s1 > s2 else "B", "str", text=True,
                      placeholder="A or B",
                      solution=["Collection A is worth %s and collection B is "
                                "worth %s." % (money(s1), money(s2)),
                                "Collection %s is worth more."
                                % ("A" if s1 > s2 else "B")])

    if t == 11:                      # how much more money does one collection show?
        g1, s1, g2, s2 = _two_groups()
        return _num_q("Collection A has %s. Collection B has %s. One collection "
                      "shows more money than the other. How much more is it worth, "
                      "in pence?" % (_coin_list(g1), _coin_list(g2)),
                      abs(s1 - s2), "int", unit="p",
                      solution=["Collection A is worth %d p and collection B is "
                                "worth %d p." % (s1, s2),
                                "%d − %d = %d p." % (max(s1, s2), min(s1, s2),
                                                     abs(s1 - s2))])

    if t == 0:                       # count coins
        vals = random.sample(pool, 3)
        items = [(random.randint(1, 4), v) for v in vals]
        total = sum(c * v for c, v in items)
        return _num_q("Count the money: %s. How much is there altogether, in pence?"
                      % _coin_list(items), total, "int", unit="p",
                      solution=[" + ".join("%d × %d" % (c, v) for c, v in items)
                                + " = %d p." % total,
                                "That is %s." % money(total)])

    if t == 1:                       # count coins, answer in pounds
        vals = random.sample(_by_d(d, [10, 20, 50, 100], [20, 50, 100, 200],
                                   [5, 20, 50, 100, 200]), 3)
        items = [(random.randint(1, _by_d(d, 3, 4, 6)), v) for v in vals]
        total = sum(c * v for c, v in items)
        return _num_q("Count the money: %s. How much is there altogether, in pounds? "
                      "Write it like 4.75." % _coin_list(items),
                      round(total / 100.0, 2), "num",
                      solution=["Altogether that is %d p." % total,
                                "%d p = %s." % (total, money(total))])

    if t == 2:                       # compare two groups
        g1 = [(random.randint(1, 3), v) for v in random.sample(pool, 2)]
        g2 = [(random.randint(1, 3), v) for v in random.sample(pool, 2)]
        s1 = sum(c * v for c, v in g1)
        s2 = sum(c * v for c, v in g2)
        while s1 == s2:
            g2 = [(random.randint(1, 4), v) for v in random.sample(pool, 2)]
            s2 = sum(c * v for c, v in g2)
        return _num_q("Group A: %s. Group B: %s. Which group is worth more? "
                      "Write the larger value in pence." % (_coin_list(g1),
                                                            _coin_list(g2)),
                      max(s1, s2), "int", unit="p",
                      solution=["Group A is worth %d p; group B is worth %d p."
                                % (s1, s2),
                                "The larger value is %s." % money(max(s1, s2))])

    if t == 3:                       # equivalent coins
        coin = pick(_by_d(d, [2, 5, 10], [2, 5, 10, 20, 50], [5, 10, 20, 50]))
        count = random.randint(*_by_d(d, (2, 5), (2, min(10, 200 // coin)),
                                      (8, min(20, 1000 // coin))))
        total = coin * count
        return _num_q("How many %dp coins have the same value as %s?"
                      % (coin, money(total)), count, "int", unit="coins",
                      solution=["%d ÷ %d = %d." % (total, coin, count),
                                "%d %dp coins make %s." % (count, coin, money(total))])

    if t == 4:                       # order three amounts (largest)
        amts = []
        while len(amts) < 3:
            v = random.randint(15, _by_d(d, 200, 999, 2500))
            if v not in amts:
                amts.append(v)
        return _num_q("Write the largest of these amounts, in pence: %s"
                      % ", ".join(money(v) for v in amts), max(amts), "int", unit="p",
                      solution=["In pence the amounts are %s."
                                % ", ".join("%d" % v for v in amts),
                                "The largest is %s." % money(max(amts))])

    if t == 5:                       # order three amounts (smallest)
        amts = []
        while len(amts) < 3:
            v = random.randint(15, _by_d(d, 200, 999, 2500))
            if v not in amts:
                amts.append(v)
        return _num_q("Write the smallest of these amounts, in pence: %s"
                      % ", ".join(money(v) for v in amts), min(amts), "int", unit="p",
                      solution=["In pence the amounts are %s."
                                % ", ".join("%d" % v for v in amts),
                                "The smallest is %s." % money(min(amts))])

    if t == 6:                       # price list: dearest item
        names = random.sample(_SHOP, 4)
        prices = []
        same_pounds = random.randint(1, 9) * 100      # stretch: every price has the same pounds
        while len(prices) < 4:
            p = _by_d(d, random.randint(10, 99), random.randint(35, 950),
                      same_pounds + random.randint(1, 99))
            if p not in prices:
                prices.append(p)
        rows = [[nm.capitalize(), money(p)] for nm, p in zip(names, prices)]
        top = prices.index(max(prices))
        return _table_q("The price list shows four items. How much does the dearest "
                        "item cost, in pence?", ["Item", "Price"], rows,
                        max(prices), "int",
                        ["The dearest item is the %s at %s."
                         % (names[top], money(max(prices))),
                         "That is %d p." % max(prices)])

    if t == 7:                       # pounds and pence conversion
        v = _by_d(d, random.randint(1, 9) * 100 + random.randint(1, 9) * 10,
                  random.randint(105, 2500),
                  random.randint(1, 25) * 100 + random.randint(1, 9))   # stretch: £12.05
        if random.random() < 0.5:
            return _num_q("How many pence is %s?" % money(v), v, "int", unit="p",
                          solution=["£1 = 100 p.",
                                    "%s = %d p." % (money(v), v)])
        return _num_q("Write %d p in pounds. Write it like 4.75." % v,
                      round(v / 100.0, 2), "num",
                      solution=["100 p = £1.",
                                "%d p = %s." % (v, money(v))])

    if t == 8:                       # how much more to make a round amount
        target = pick(_by_d(d, [100], [100, 200, 500], [500, 1000, 2000]))
        have = random.randrange(10, target, 10) if d == 0 else \
            random.randrange(5, target, 5) if d == 1 else random.randint(105, target - 1)
        who = pick(NAMES)
        return _num_q("%s has %s. How much more money is needed to make %s, in pence?"
                      % (who, money(have), money(target)), target - have, "int",
                      unit="p",
                      solution=["%s is %d p." % (money(target), target),
                                "%d − %d = %d p." % (target, have, target - have)])

    # fewest coins
    amount = _by_d(d, random.randrange(10, 100, 10), random.randrange(15, 100, 5),
                   random.randint(101, 499))
    coins = [200, 100, 50, 20, 10, 5, 2, 1] if d == 2 else [50, 20, 10, 5, 2, 1]
    left, count = amount, 0
    for c in coins:
        count += left // c
        left = left % c
    return _num_q("What is the smallest number of coins needed to make %s? "
                  "You may use %s coins." % (money(amount),
                                             "1p, 2p, 5p, 10p, 20p, 50p, £1 and £2" if d == 2
                                             else "1p, 2p, 5p, 10p, 20p and 50p"),
                  count, "int", unit="coins",
                  solution=["Start with the largest coins that fit.",
                            "%s needs %s." % (money(amount), _pl(count, "coin"))])


@skill("Y4.7.g", "Add and subtract money, and give change", S7)
def _(d=1):
    d = _tier(d)
    hi = _by_d(d, 300, 999, 2500)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 2, 1])

    if t == 0:                       # add, answer in pence
        a = random.randint(45, hi)
        b = random.randint(45, hi)
        return _num_q("Add %s and %s. Give your answer in pence." % (money(a), money(b)),
                      a + b, "int", unit="p",
                      solution=["%d + %d = %d p." % (a, b, a + b),
                                "That is %s." % money(a + b)])

    if t == 1:                       # add, answer in pounds
        a = random.randint(105, hi)
        b = random.randint(105, hi)
        return _num_q("Add %s and %s. Give your answer in pounds, written like 4.75."
                      % (money(a), money(b)), round((a + b) / 100.0, 2), "num",
                      solution=["%s + %s = %s." % (money(a), money(b), money(a + b)),
                                "In pounds that is %s." % _n((a + b) / 100.0)])

    if t == 2:                       # subtract
        a = random.randint(150, hi) + 100
        b = random.randint(45, a - 20)
        who = pick(NAMES)
        return _num_q("%s has %s and spends %s. How much is left, in pence?"
                      % (who, money(a), money(b)), a - b, "int", unit="p",
                      solution=["%d − %d = %d p." % (a, b, a - b),
                                "That is %s." % money(a - b)])

    if t == 3:                       # change from a note
        paid = pick(_by_d(d, [100, 200], [500, 1000], [1000, 2000]))
        cost = random.randint(max(25, paid // 5), paid - 15)
        return _num_q("A %s costs %s. %s pays with %s. How much change, in pence?"
                      % (pick(_SHOP), money(cost), pick(NAMES), money(paid)),
                      paid - cost, "int", unit="p",
                      solution=["%d − %d = %d p." % (paid, cost, paid - cost),
                                "The change is %s." % money(paid - cost)])

    if t == 4:                       # two items, then change
        paid = pick(_by_d(d, [200, 500], [500, 1000], [1000, 2000]))
        a = random.randint(30, paid // 3)
        b = random.randint(30, paid // 3)
        who = pick(NAMES)
        return _num_q("%s buys %s for %s and %s for %s, and pays with %s. "
                      "How much change, in pence?"
                      % (who, _a(pick(_FOOD)), money(a), _a(pick(_SHOP)), money(b),
                         money(paid)),
                      paid - a - b, "int", unit="p",
                      solution=["%d + %d = %d p spent." % (a, b, a + b),
                                "%d − %d = %d p change." % (paid, a + b,
                                                            paid - a - b)])

    if t == 5:                       # missing cost from change
        paid = pick(_by_d(d, [100, 200, 500], [500, 1000, 2000], [1000, 2000, 5000]))
        change = random.randrange(10, paid - 20, 10) if d == 0 else random.randint(25, paid - 60)
        return _num_q("A shopper pays with %s and gets %s change. How much did the "
                      "item cost, in pence?" % (money(paid), money(change)),
                      paid - change, "int", unit="p",
                      solution=["%d − %d = %d p." % (paid, change, paid - change),
                                "The item cost %s." % money(paid - change)])

    if t == 6:                       # missing amount added
        a = random.randint(50, hi)
        b = random.randint(50, hi)
        return _num_q("Complete: %s + ___ p = %s" % (money(a), money(a + b)), b, "int",
                      unit="p",
                      solution=["%d − %d = %d p." % (a + b, a, b)])

    if t == 7:                       # change in pounds
        paid = pick(_by_d(d, [500], [1000, 2000], [2000, 5000]))
        cost = random.randrange(150, paid - 100, 10) if d == 0 else random.randint(150, paid - 105)
        return _num_q("A %s costs %s. %s pays with %s. How much change is that, in "
                      "pounds? Write it like 4.75."
                      % (pick(_SHOP), money(cost), pick(NAMES), money(paid)),
                      round((paid - cost) / 100.0, 2), "num",
                      solution=["%s − %s = %s." % (money(paid), money(cost),
                                                   money(paid - cost)),
                                "In pounds that is %s." % _n((paid - cost) / 100.0)])

    if t == 8:                       # price list, buy two, give change
        names = random.sample(_SHOP, 3)
        prices = [_by_d(d, random.randrange(20, 100, 5), random.randint(45, 450),
                        random.randint(145, 950)) for _ in names]
        rows = [[nm.capitalize(), money(p)] for nm, p in zip(names, prices)]
        i = random.randrange(3)
        j = (i + 1) % 3
        # the note must actually cover the two items, or "change" is negative
        paid = 500 if prices[i] + prices[j] <= 460 else 1000
        if d == 0:
            paid = 200
        elif d == 2:
            paid = 2000
        return _table_q("%s buys the %s and the %s from this price list and pays "
                        "with %s. How much change, in pence?"
                        % (pick(NAMES), names[i], names[j], money(paid)),
                        ["Item", "Price"], rows,
                        paid - prices[i] - prices[j], "int",
                        ["%s + %s = %s spent." % (money(prices[i]), money(prices[j]),
                                                  money(prices[i] + prices[j])),
                         "%s − %s = %s change."
                         % (money(paid), money(prices[i] + prices[j]),
                            money(paid - prices[i] - prices[j]))])

    # saving up: how much more is needed
    goal = _by_d(d, random.randrange(100, 500, 10), random.randint(500, 2500),
                 random.randint(2000, 5000))
    saved = random.randrange(50, goal - 40, 10) if d == 0 else random.randint(100, goal - 50)
    who = pick(NAMES)
    return _num_q("%s wants a game costing %s and has saved %s. How much more money "
                  "does %s need, in pence?" % (who, money(goal), money(saved), who),
                  goal - saved, "int", unit="p",
                  solution=["%d − %d = %d p." % (goal, saved, goal - saved),
                            "That is %s more." % money(goal - saved)])


@skill("Y4.7.h", "Money problems and price lists", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([2, 2, 2, 2, 2, 1, 1, 1, 1])

    def _list(n=4, lo=None, hi=None):
        """Price list: tidy pence at d=0, up to £3.50 at d=1, up to £12.50 at d=2."""
        lo = _by_d(d, 20, 35, 135) if lo is None else lo
        hi = _by_d(d, 150, 350, 1250) if hi is None else hi
        names = random.sample(_SHOP + _FOOD, n)
        prices = []
        while len(prices) < n:
            p = random.randrange(lo, hi + 1, 5) if d == 0 else random.randint(lo, hi)
            if p not in prices:
                prices.append(p)
        rows = [[nm.capitalize(), money(p)] for nm, p in zip(names, prices)]
        return names, prices, rows

    if t == 0:                       # total of two named items
        names, prices, rows = _list()
        i, j = random.sample(range(4), 2)
        return _table_q("Use the price list. How much do %s and %s cost "
                        "altogether, in pence?" % (_a(names[i]), _a(names[j])),
                        ["Item", "Price"], rows, prices[i] + prices[j], "int",
                        ["%s + %s = %s." % (money(prices[i]), money(prices[j]),
                                            money(prices[i] + prices[j])),
                         "That is %d p." % (prices[i] + prices[j])])

    if t == 1:                       # difference between two items
        names, prices, rows = _list()
        i, j = random.sample(range(4), 2)
        hi_i = i if prices[i] > prices[j] else j
        lo_i = j if hi_i == i else i
        return _table_q("Use the price list. How much more does %s cost than "
                        "%s, in pence?" % (_a(names[hi_i]), _a(names[lo_i])),
                        ["Item", "Price"], rows,
                        prices[hi_i] - prices[lo_i], "int",
                        ["%s − %s = %s." % (money(prices[hi_i]), money(prices[lo_i]),
                                            money(prices[hi_i] - prices[lo_i])),
                         "That is %d p." % (prices[hi_i] - prices[lo_i])])

    if t == 2:                       # multiples of one item
        names, prices, rows = _list()
        i = random.randrange(4)
        k = random.randint(2, _by_d(d, 3, 5, 8))
        return _table_q("Use the price list. How much do %d %s cost altogether, "
                        "in pence?" % (k, _plural(names[i])), ["Item", "Price"], rows,
                        k * prices[i], "int",
                        ["%d × %s = %s." % (k, money(prices[i]),
                                            money(k * prices[i])),
                         "That is %d p." % (k * prices[i])])

    if t == 3:                       # change from a note
        names, prices, rows = _list()
        i = random.randrange(4)
        paid = pick(_by_d(d, [200, 500], [500, 1000], [1000, 2000]))
        while prices[i] >= paid:
            prices[i] = random.randint(35, paid - 20)
            rows[i][1] = money(prices[i])
        return _table_q("Use the price list. %s buys %s and pays with %s. "
                        "How much change, in pence?"
                        % (pick(NAMES), _a(names[i]), money(paid)),
                        ["Item", "Price"], rows, paid - prices[i], "int",
                        ["%s − %s = %s." % (money(paid), money(prices[i]),
                                            money(paid - prices[i])),
                         "That is %d p change." % (paid - prices[i])])

    if t == 4:                       # dearest / cheapest
        names, prices, rows = _list()
        ask_dear = random.random() < 0.5
        k = prices.index(max(prices) if ask_dear else min(prices))
        return _table_q("Use the price list. Which item is the %s? Type its name."
                        % ("dearest" if ask_dear else "cheapest"),
                        ["Item", "Price"], rows, names[k], "str",
                        ["Compare the prices in the list.",
                         "The %s item is the %s at %s."
                         % ("dearest" if ask_dear else "cheapest", names[k],
                            money(prices[k]))])

    if t == 5:                       # what can be afforded
        names, prices, rows = _list(4, *_by_d(d, (20, 150), (60, 400), (150, 1250)))
        budget = random.randint(*_by_d(d, (50, 120), (150, 500), (300, 1100)))
        n_afford = len([p for p in prices if p <= budget])
        who = pick(NAMES)
        return _table_q("Use the price list. %s has %s. How many of the four items "
                        "could %s afford to buy, one at a time?"
                        % (who, money(budget), who),
                        ["Item", "Price"], rows, n_afford, "int",
                        ["Compare each price with %s." % money(budget),
                         "%d of the items cost %s or less." % (n_afford,
                                                               money(budget))])

    if t == 6:                       # bar chart of prices
        n_bars = 5 if d == 2 else 4
        names = random.sample(["Book", "Game", "Kite", "Ball", "Puzzle"], n_bars)
        prices = []
        while len(prices) < n_bars:
            p = random.randrange(20, 100, 10) if d == 0 else random.randint(20, 95)
            if p not in prices:
                prices.append(p)
        return {"prompt": "The chart shows prices in pence. How much would all %s "
                          "items cost altogether, in pence?" % n_words(n_bars),
                "component": "bar_chart",
                "spec": {"categories": names, "values": prices, "mode": "read"},
                "answer": sum(prices), "answer_type": "int",
                "solution": ["%s = %d p." % (" + ".join(str(p) for p in prices),
                                             sum(prices)),
                             "That is %s." % money(sum(prices))]}

    if t == 7:                       # two-step: buy several, then change
        names, prices, rows = _list(3, *_by_d(d, (20, 150), (45, 300), (145, 450)))
        i = random.randrange(3)
        k = random.randint(*_by_d(d, (2, 2), (2, 3), (3, 5)))
        paid = _by_d(d, 1000, 2000, 5000)
        return _table_q("Use the price list. %s buys %d %s and pays with a %s note. "
                        "How much change, in pence?"
                        % (pick(NAMES), k, _plural(names[i]), money(paid).replace(".00", "")),
                        ["Item", "Price"], rows, paid - k * prices[i], "int",
                        ["%d × %s = %s." % (k, money(prices[i]),
                                            money(k * prices[i])),
                         "%s − %s = %s change." % (money(paid), money(k * prices[i]),
                                                   money(paid - k * prices[i]))])

    # sharing a cost equally
    who = pick(NAMES)
    per = _by_d(d, random.randrange(10, 105, 5), random.randint(35, 300), random.randint(135, 999))
    k = random.randint(*_by_d(d, (2, 3), (2, 6), (3, 8)))
    return _num_q("%s and %s share the cost of a present equally. The present "
                  "costs %s in total and there are %d people paying. How much does "
                  "each person pay, in pence?" % (who, _pl(k - 1, "friend"), money(per * k), k),
                  per, "int", unit="p",
                  solution=["%d ÷ %d = %d p." % (per * k, k, per),
                            "Each person pays %s." % money(per)])


@skill("Y4.7.i", "Tell and write the time, a.m. and p.m.", S7)
def _(d=1):
    d = _tier(d)
    h = random.randint(1, 12)
    m = pick(_clock_minutes(d))
    t = _pick_t([2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1])
    # minutes said as "past"/"to": five-minute steps, and at d=2 any minute
    odd = [3, 7, 12, 18, 23, 27, 33, 37, 42, 48, 53, 57]

    if t == 9:                       # match a digital clock with an analogue clock
        if d == 2 and random.random() < 0.5:
            h24 = random.randint(13, 23)
            return {"prompt": "A digital clock shows %s. Set the analogue clock so "
                              "that it matches the digital clock."
                              % _hm24(h24, m),
                    "component": "clock", "spec": {"mode": "set"},
                    "answer": _hm(h24 - 12, m), "answer_type": "time",
                    "solution": ["%s in 12-hour time is %s."
                                 % (_hm24(h24, m), _hm(h24 - 12, m)),
                                 "Put the hour hand %s %d and the minute "
                                 "hand on %d minutes." % ("exactly on" if m == 0 else "just past", h24 - 12, m)]}
        return {"prompt": "A digital clock shows %s. Set the analogue clock so that "
                          "it matches the digital clock." % _hm(h, m),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m), "answer_type": "time",
                "solution": ["The two clocks match when they show the same time.",
                             "Put the hour hand %s %d and the minute hand "
                             "on %d minutes." % ("exactly on" if m == 0 else "just past", h, m)]}

    if t == 10:                      # analogue words -> matching digital clock
        mm = pick(_clock_minutes(d))
        if mm == 0:
            phrase = "%d o'clock" % h
        elif mm == 15:
            phrase = "quarter past %d" % h
        elif mm == 30:
            phrase = "half past %d" % h
        elif mm == 45:
            phrase = "quarter to %d" % (1 if h == 12 else h + 1)
        elif mm < 30:
            phrase = "%d minutes past %d" % (mm, h)
        else:
            phrase = "%d minutes to %d" % (60 - mm, 1 if h == 12 else h + 1)
        return _num_q("An analogue clock shows %s. Which time would the matching "
                      "digital clock show? Write it as h:mm." % phrase,
                      _hm(h, mm), "time", text=True, placeholder="e.g. 3:20",
                      solution=["%s is %s." % (phrase.capitalize(), _hm(h, mm)),
                                "The digital clock that matches shows %s."
                                % _hm(h, mm)])

    if t == 0:                       # set from digital
        return {"prompt": "Set the clock to %s." % _hm(h, m),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, m), "answer_type": "time",
                "solution": ["The hour hand goes %s %d." % ("exactly on" if m == 0 else "just past", h),
                             "The minute hand shows %d minutes." % m]}

    if t == 1:                       # set from words
        mm = pick(_by_d(d, [0, 30], [0, 15, 30, 45], [15, 45]))
        phrase = {0: "%d o'clock" % h, 15: "quarter past %d" % h,
                  30: "half past %d" % h,
                  45: "quarter to %d" % (1 if h == 12 else h + 1)}[mm]
        return {"prompt": "Set the clock to %s." % phrase,
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, mm), "answer_type": "time",
                "solution": ["%s is %s." % (phrase.capitalize(), _hm(h, mm))]}

    if t == 2:                       # set from 'minutes past / to'
        mm = pick(_by_d(d, [5, 10, 20, 25], [5, 10, 20, 25, 35, 40, 50, 55], odd))
        if mm <= 30:
            phrase = "%d minutes past %d" % (mm, h)
        else:
            phrase = "%d minutes to %d" % (60 - mm, 1 if h == 12 else h + 1)
        return {"prompt": "Set the clock to %s." % phrase,
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(h, mm), "answer_type": "time",
                "solution": ["%s is %s." % (phrase.capitalize(), _hm(h, mm))]}

    if t == 3:                       # words -> digital typed
        mm = pick(_by_d(d, [5, 10, 15, 20, 25, 30],
                        [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55], odd))
        if mm <= 30:
            phrase = "%d minutes past %d" % (mm, h)
        else:
            phrase = "%d minutes to %d" % (60 - mm, 1 if h == 12 else h + 1)
        return _num_q("Write '%s' in digital form (h:mm)." % phrase, _hm(h, mm),
                      "time", text=True, placeholder="e.g. 3:20",
                      solution=["%s is %s." % (phrase.capitalize(), _hm(h, mm))])

    if t == 4:                       # a.m. or p.m.
        easy = [("the school day starts", 8, 45, "am"),
                ("morning break begins", 10, 30, "am"),
                ("the school day ends", 3, 15, "pm"),
                ("bedtime is", 8, 0, "pm"),
                ("breakfast is eaten", 7, 15, "am")]
        tricky = [("lunch is served", 12, 30, "pm"),       # the hour number does not say
                  ("swimming club starts", 4, 45, "pm"),
                  ("the sun rises in summer", 5, 30, "am"),
                  ("the milk is delivered", 5, 15, "am"),
                  ("the owl starts hooting", 11, 30, "pm"),
                  ("the baker starts making bread", 4, 30, "am")]
        event, hh, mm, half = pick(_by_d(d, easy, easy + tricky[:3], tricky))
        return _num_q("%s at %s. Is that time am or pm? Type am or pm."
                      % (event.capitalize(), _hm(hh, mm)), half, "str", text=True,
                      placeholder="am / pm",
                      solution=["Times before midday are am; times after midday are pm.",
                                "%s at %s, which is %s." % (event.capitalize(),
                                                            _hm(hh, mm), half)])

    if t == 5:                       # before or after midday
        hh = random.randint(1, 11) if d == 0 else random.randint(1, 12)
        if d == 2:                   # stretch: the 12 o'clock hour
            hh = 12
        mm = pick([15, 30, 45]) if hh == 12 else pick([0, 30] if d == 0 else [0, 15, 30, 45])
        half = pick(["am", "pm"])
        return _num_q("Is %s %s before or after midday? Type before or after."
                      % (_hm(hh, mm), half),
                      "before" if half == "am" else "after", "str", text=True,
                      placeholder="before / after",
                      solution=["am means before midday and pm means after midday.",
                                "%s is %s midday." % (half,
                                                      "before" if half == "am"
                                                      else "after")])

    if t == 6:                       # set a real-life time
        label, eh, em = pick(_by_d(
            d, [("assembly", 9, 0), ("break", 10, 30), ("lunch", 12, 30),
                ("home time", 3, 30), ("bedtime", 8, 0)],
            [("assembly", 9, 10), ("break", 10, 45),
             ("lunch", 12, 20), ("home time", 3, 25),
             ("football club", 4, 50), ("bedtime", 8, 5)],
            [("the train", 4, 37), ("the bus", 8, 13), ("the film", 6, 48),
             ("swimming", 5, 23), ("the dentist", 11, 52)]))
        return {"prompt": "%s is at %s. Set the clock to that time."
                          % (label.capitalize(), _hm(eh, em)),
                "component": "clock", "spec": {"mode": "set"},
                "answer": _hm(eh, em), "answer_type": "time",
                "solution": ["Put the hour hand %s %d." % ("exactly on" if em == 0 else "just past", eh),
                             "Put the minute hand on %d minutes." % em]}

    if t == 7:                       # how many minutes past the hour
        mm = pick(_by_d(d, [15, 30, 45], [5, 10, 20, 25, 35, 40, 50, 55], odd))
        return _num_q("How many minutes past %d o'clock is %s?" % (h, _hm(h, mm)),
                      mm, "int", unit="minutes",
                      solution=["The minute hand has moved %d minutes past %d."
                                % (mm, h)])

    # how many minutes to the next hour
    mm = pick(_by_d(d, [30, 45], [35, 40, 45, 50, 55], [33, 38, 41, 47, 52, 56]))
    nh = 1 if h == 12 else h + 1
    return _num_q("How many minutes to %d o'clock is %s?" % (nh, _hm(h, mm)),
                  60 - mm, "int", unit="minutes",
                  solution=["From %s to %d o'clock is %d minutes."
                            % (_hm(h, mm), nh, 60 - mm)])


@skill("Y4.7.j", "12-hour and 24-hour time", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 2, 1, 1, 1, 1])
    mins = pick(_clock_minutes(d))   # o'clock/quarters, 5-minute steps, then any minute

    if t == 0:                       # afternoon 24-hour -> 12-hour
        h24 = random.randint(13, 18 if d == 0 else 23)
        if d == 2 and random.random() < 0.3:
            h24 = 12                 # stretch: the 12 o'clock hour is the trap
            return _num_q("A programme starts at %s in 24-hour time. Write that time as a "
                          "12-hour time (h:mm)." % _hm24(h24, mins),
                          _hm(12, mins), "time", text=True, placeholder="e.g. 2:30",
                          solution=["12:00 is midday, so the 12 o'clock hour is already pm.",
                                    "Do not take 12 away: %s is %s pm."
                                    % (_hm24(h24, mins), _hm(12, mins))])
        return _num_q("A programme starts at %s in 24-hour time. Write that time as a "
                      "12-hour time (h:mm)." % _hm24(h24, mins),
                      _hm(h24 - 12, mins), "time", text=True, placeholder="e.g. 2:30",
                      solution=["After midday, take 12 away from the hours.",
                                "%d − 12 = %d, so the time is %s pm."
                                % (h24, h24 - 12, _hm(h24 - 12, mins))])

    if t == 1:                       # afternoon 12-hour -> 24-hour
        h12 = random.randint(1, 6 if d == 0 else 11)
        if d == 2 and random.random() < 0.3:   # stretch: 12-something am/pm
            am = random.random() < 0.5
            ans = _hm24(0 if am else 12, mins)
            return _num_q("A train leaves at %s %s. Write that time in 24-hour form "
                          "(hh:mm)." % (_hm(12, mins), "am" if am else "pm"),
                          ans, "str", text=True, placeholder="e.g. 14:30",
                          solution=["12 o'clock at night (am) is hour 00; 12 o'clock midday "
                                    "(pm) stays hour 12.",
                                    "So %s %s is %s." % (_hm(12, mins), "am" if am else "pm", ans)])
        return _num_q("A train leaves at %s pm. Write that time in 24-hour form "
                      "(hh:mm)." % _hm(h12, mins),
                      _hm24(h12 + 12, mins), "str", text=True,
                      placeholder="e.g. 14:30",
                      solution=["For pm times, add 12 to the hours.",
                                "%d + 12 = %d, so the time is %s."
                                % (h12, h12 + 12, _hm24(h12 + 12, mins))])

    if t == 2:                       # morning: hour number only
        h12 = random.randint(8, 11)
        return _num_q("A lesson starts at %s am. In 24-hour time, what is the hour "
                      "number?" % _hm(h12, mins), h12, "int",
                      solution=["Morning hours keep the same number in 24-hour time.",
                                "The 24-hour time is %s, so the hour number is %d."
                                % (_hm24(h12, mins), h12)])

    if t == 3:                       # 24-hour morning -> 12-hour
        h24 = random.randint(8, 11) if d == 0 else random.randint(6, 11)
        if d == 2 and random.random() < 0.3:
            h24 = 0                  # stretch: 00:xx is 12-something am
            return _num_q("A night bus leaves at %s in 24-hour time. Write that as a "
                          "12-hour time (h:mm)." % _hm24(h24, mins), _hm(h24, mins), "time",
                          text=True, placeholder="e.g. 9:30",
                          solution=["Hour 00 is the hour after midnight, which is 12 on a "
                                    "12-hour clock.",
                                    "%s is %s am." % (_hm24(h24, mins), _hm(h24, mins))])
        return _num_q("A shop opens at %s in 24-hour time. Write that as a 12-hour "
                      "time (h:mm)." % _hm24(h24, mins), _hm(h24, mins), "time",
                      text=True, placeholder="e.g. 9:30",
                      solution=["Before midday the hours do not change.",
                                "%s is %s am." % (_hm24(h24, mins), _hm(h24, mins))])

    if t == 4:                       # timetable of 24-hour times
        rows = []
        times = []
        for label in ["Assembly", "Maths", "Break", "English"]:
            h24 = random.randint(9, 15)
            mm = pick(_by_d(d, [0, 30], [0, 15, 30, 45], _clock_minutes(2)))
            times.append((h24, mm))
            rows.append([label, _hm24(h24, mm)])
        k = random.randrange(4)
        h24, mm = times[k]
        ans = _hm(h24 if h24 < 13 else h24 - 12, mm)
        return _table_q("The timetable shows 24-hour times. Write the %s time as a "
                        "12-hour time (h:mm)." % rows[k][0].lower(),
                        ["Event", "Time"], rows, ans, "time",
                        ["%s is %s in 24-hour time." % (rows[k][0], _hm24(h24, mm)),
                         "As a 12-hour time that is %s." % ans])

    if t == 5:                       # is a 24-hour time morning or afternoon
        # stretch: hours either side of midday, where 12:xx is the trap
        h24 = random.randint(10, 14) if d == 2 else random.randint(6, 17)
        return _num_q("Is %s in 24-hour time in the morning or the afternoon? "
                      "Type morning or afternoon." % _hm24(h24, mins),
                      "morning" if h24 < 12 else "afternoon", "str", text=True,
                      placeholder="morning / afternoon",
                      solution=["24-hour times below 12:00 are in the morning.",
                                "%s is in the %s." % (_hm24(h24, mins),
                                                      "morning" if h24 < 12
                                                      else "afternoon")])

    if t == 6:                       # midnight and midday
        which = pick(["midnight", "midday"])
        return _num_q("What is %s in 24-hour time? Write it in the form hh:mm."
                      % which, "00:00" if which == "midnight" else "12:00", "str",
                      text=True, placeholder="e.g. 00:00",
                      solution=["The 24-hour day starts at 00:00, which is midnight.",
                                "%s is %s." % (which.capitalize(),
                                               "00:00" if which == "midnight"
                                               else "12:00")])

    if t == 7:                       # evening 12 -> 24 (double-digit hour)
        h12 = random.randint(6, 11)
        return _num_q("A film ends at %s pm. Write that time in 24-hour form (hh:mm)."
                      % _hm(h12, mins), _hm24(h12 + 12, mins), "str", text=True,
                      placeholder="e.g. 20:15",
                      solution=["Add 12 to the hours for a pm time.",
                                "%d + 12 = %d, so it is %s." % (h12, h12 + 12,
                                                                _hm24(h12 + 12, mins))])

    # match a clock face to a 24-hour time
    h24 = random.randint(13, 18 if d == 0 else 23)
    return {"prompt": "A bus leaves at %s in 24-hour time. Set the clock to show "
                      "that time." % _hm24(h24, mins),
            "component": "clock", "spec": {"mode": "set"},
            "answer": _hm(h24 - 12, mins), "answer_type": "time",
            "solution": ["%s is %s pm." % (_hm24(h24, mins), _hm(h24 - 12, mins)),
                         "Set the hour hand %s %d." % ("exactly on" if mins == 0 else "just past", h24 - 12)]}


def _hm_parts(d):
    """Hours and minutes for a mixed time: quarter hours (easy), five-minute
    steps (core), any minute (stretch)."""
    if d == 0:
        return random.randint(1, 3), pick([15, 30, 45])
    if d == 1:
        return random.randint(1, 6), random.randrange(5, 60, 5)
    return random.randint(2, 9), random.choice([x for x in range(1, 60) if x % 5])


@skill("Y4.7.k", "Convert units of time", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 1, 1, 1, 1, 1, 2, 1])

    if t == 0:                       # hours -> minutes
        h = random.randint(2, _by_d(d, 5, 9, 12))
        return _num_q("How many minutes are there in %d hours?" % h, h * 60, "int",
                      unit="minutes",
                      solution=["1 hour = 60 minutes.",
                                "%d × 60 = %d minutes." % (h, h * 60)])

    if t == 1:                       # minutes -> hours
        h = random.randint(2, _by_d(d, 5, 9, 12))
        return _num_q("How many hours are there in %d minutes?" % (h * 60), h, "int",
                      unit="hours",
                      solution=["60 minutes = 1 hour.",
                                "%d ÷ 60 = %d hours." % (h * 60, h)])

    if t == 2:                       # minutes -> seconds and back
        m = random.randint(2, _by_d(d, 5, 9, 15))
        if random.random() < 0.5:
            return _num_q("How many seconds are there in %d minutes?" % m, m * 60,
                          "int", unit="seconds",
                          solution=["1 minute = 60 seconds.",
                                    "%d × 60 = %d seconds." % (m, m * 60)])
        return _num_q("How many minutes are there in %d seconds?" % (m * 60), m,
                      "int", unit="minutes",
                      solution=["60 seconds = 1 minute.",
                                "%d ÷ 60 = %d minutes." % (m * 60, m)])

    if t == 3:                       # days -> hours and back
        days = random.randint(2, _by_d(d, 4, 8, 14))
        if random.random() < 0.5:
            return _num_q("How many hours are there in %d days?" % days, days * 24,
                          "int", unit="hours",
                          solution=["1 day = 24 hours.",
                                    "%d × 24 = %d hours." % (days, days * 24)])
        return _num_q("How many days are there in %d hours?" % (days * 24), days,
                      "int", unit="days",
                      solution=["24 hours = 1 day.",
                                "%d ÷ 24 = %d days." % (days * 24, days)])

    if t == 4:                       # fractions of an hour
        frac_n, frac_d, mins = pick(_by_d(d, [(1, 2, 30), (1, 4, 15), (3, 4, 45)],
                                          [(1, 2, 30), (1, 4, 15), (3, 4, 45),
                                           (1, 3, 20), (2, 3, 40), (1, 10, 6),
                                           (1, 5, 12)],
                                          [(2, 3, 40), (3, 10, 18), (2, 5, 24),
                                           (3, 5, 36), (7, 10, 42), (4, 5, 48)]))
        return _num_q("How many minutes are there in %s of an hour?"
                      % _frac_words(frac_n, frac_d), mins, "int", unit="minutes",
                      solution=["1 hour = 60 minutes.",
                                "%d/%d of 60 = %d minutes." % (frac_n, frac_d, mins)])

    if t == 5:                       # mixed hours and minutes -> minutes
        h, m = _hm_parts(d)
        return _num_q("How many minutes are there in %s %s?"
                      % (_pl(h, "hour"), _pl(m, "minute")),
                      h * 60 + m, "int", unit="minutes",
                      solution=["%s = %d minutes." % (_pl(h, "hour"), h * 60),
                                "%d + %d = %d minutes." % (h * 60, m, h * 60 + m)])

    if t == 6:                       # minutes -> mixed (leftover minutes)
        h, m = _hm_parts(d)
        total = h * 60 + m
        return _num_q("%d minutes is the same as %s and how many minutes?"
                      % (total, _pl(h, "hour")), m, "int", unit="minutes",
                      solution=["%s = %d minutes." % (_pl(h, "hour"), h * 60),
                                "%d − %d = %s." % (total, h * 60, _pl(m, "minute"))])

    if t == 7:                       # weeks / years / calendar facts
        if d == 2:                   # stretch: bigger multiples of the facts
            w = random.randint(6, 12)
            y = random.randint(3, 8)
            q, ans, fact = pick([
                ("How many days are there in %d weeks?" % w, 7 * w, "1 week = 7 days"),
                ("How many weeks are there in %d days?" % (7 * w), w, "7 days = 1 week"),
                ("How many months are there in %d years?" % y, 12 * y, "1 year = 12 months"),
                ("How many years are there in %d months?" % (12 * y), y, "12 months = 1 year"),
                ("How many hours are there in a week?", 168, "1 day = 24 hours, and 7 × 24 = 168"),
                ("How many days are there in a fortnight and 3 days?", 17,
                 "a fortnight is 14 days"),
            ])
            return _num_q(q, ans, "int",
                          solution=[fact[0].upper() + fact[1:] + ".", "The answer is %d." % ans])
        if d == 0:
            q, ans, fact = pick([
                ("How many days are there in 1 week?", 7, "1 week = 7 days"),
                ("How many days are there in 2 weeks?", 14, "1 week = 7 days"),
                ("How many months are there in 1 year?", 12, "1 year = 12 months"),
                ("How many days are there in December?", 31, "December has 31 days"),
            ])
            return _num_q(q, ans, "int",
                          solution=[fact.capitalize() + ".", "The answer is %d." % ans])
        q, ans, fact = pick([
            ("How many days are there in 3 weeks?", 21, "1 week = 7 days"),
            ("How many days are there in 5 weeks?", 35, "1 week = 7 days"),
            ("How many weeks are there in 28 days?", 4, "7 days = 1 week"),
            ("How many months are there in 2 years?", 24, "1 year = 12 months"),
            ("How many days are there in an ordinary year?", 365,
             "an ordinary year has 365 days"),
            ("How many days are there in a leap year?", 366,
             "a leap year has 366 days"),
            ("How many days are there in September?", 30,
             "September has 30 days"),
            ("How many days are there in December?", 31, "December has 31 days"),
        ])
        return _num_q(q, ans, "int",
                      solution=[fact.capitalize() + ".", "The answer is %d." % ans])

    if t == 8:                       # conversion table
        rows = []
        vals = []
        for v in random.sample(_by_d(d, range(1, 6), range(1, 10), range(6, 16)), 3):
            vals.append(v)
            rows.append(["%d" % v, "%d" % (v * 60)])
        k = random.randrange(3)
        return _table_q("The table converts hours to minutes. How many minutes go in "
                        "the blank cell?", ["Hours", "Minutes"], rows,
                        vals[k] * 60, "int",
                        ["1 hour = 60 minutes.",
                         "%d × 60 = %d minutes." % (vals[k], vals[k] * 60)],
                        missing=(k, 1))

    # word problem
    who = pick(NAMES)
    h, m = _hm_parts(d)
    h = min(h, 4)
    return _num_q("%s spends %s %s on a bike ride. How long is the "
                  "ride in minutes?" % (who, _pl(h, "hour"), _pl(m, "minute")),
                  h * 60 + m, "int", unit="minutes",
                  solution=["%s = %d minutes." % (_pl(h, "hour"), h * 60),
                            "%d + %d = %d minutes." % (h * 60, m, h * 60 + m)])


_MONTHS = [("January", 31), ("February", 28), ("March", 31), ("April", 30),
           ("May", 31), ("June", 30), ("July", 31), ("August", 31),
           ("September", 30), ("October", 31), ("November", 30), ("December", 31)]
_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
         "Sunday"]


@skill("Y4.7.l", "End times, elapsed time, calendars and timetables", S7)
def _(d=1):
    d = _tier(d)
    t = _pick_t([1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2])

    def _timeline():
        """Four dated events in order, as table rows plus their years."""
        events = random.sample(_TIMELINE_EVENTS, 4)
        year = random.randint(1900, 1940)
        years = []
        for _i in range(4):
            years.append(year)
            year += random.randint(_by_d(d, 5, 3, 2), _by_d(d, 20, 20, 17))
        rows = [["%d" % y, ev.capitalize()] for y, ev in zip(years, events)]
        return events, years, rows

    if t == 10:                      # timeline: years between two events
        events, years, rows = _timeline()
        i = random.randrange(3)
        j = random.randrange(i + 1, 4)
        return _table_q("The timeline shows four events and the year each one "
                        "happened. How many years are there between the year %s "
                        "and the year %s?"
                        % (events[i], events[j]),
                        ["Year", "Event"], rows, years[j] - years[i], "int",
                        ["%s in %d and %s in %d."
                         % (events[i].capitalize(), years[i], events[j], years[j]),
                         "%d − %d = %s." % (years[j], years[i],
                                             _pl(years[j] - years[i], "year"))],
                        )

    if t == 11:                      # timeline: span, or the year of an event
        events, years, rows = _timeline()
        if random.random() < 0.5:
            return _table_q("The timeline shows four events. How many years are "
                            "there from the first event to the last event?",
                            ["Year", "Event"], rows, years[3] - years[0], "int",
                            ["The first event was in %d and the last in %d."
                             % (years[0], years[3]),
                             "%d − %d = %s." % (years[3], years[0],
                                                 _pl(years[3] - years[0], "year"))])
        k = random.randrange(4)
        gap = random.randint(1, max(2, min(40, 2020 - years[k])))
        return _table_q("The timeline shows four events. How many years after %s "
                        "was the year %d?" % (events[k], years[k] + gap),
                        ["Year", "Event"], rows, gap, "int",
                        ["%s in %d." % (events[k].capitalize(), years[k]),
                         "%d − %d = %s." % (years[k] + gap, years[k], _pl(gap, "year"))])

    if t == 0:                       # end time
        h = random.randint(1, 11)
        m = pick([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        dur = random.randrange(_by_d(d, 10, 15, 20), _by_d(d, 60, 105, 150), 5)
        total = h * 60 + m + dur
        eh, em = (total // 60) % 12 or 12, total % 60
        return _num_q("A film starts at %s and lasts %d minutes. What time does it "
                      "finish? Write the time as h:mm." % (_hm(h, m), dur),
                      _hm(total // 60, em), "time", text=True, placeholder="e.g. 4:35",
                      solution=["%s plus %d minutes." % (_hm(h, m), dur),
                                "The film finishes at %s." % _hm(total // 60, em)])

    if t == 1:                       # start time (work backwards)
        h = random.randint(2, 11)
        m = pick([0, 10, 15, 20, 30, 40, 45, 50])
        dur = random.randrange(15, _by_d(d, 45, 90, 120), 5)
        total = h * 60 + m
        st = total - dur
        return _num_q("A lesson finishes at %s and lasted %d minutes. What time did "
                      "it start? Write the time as h:mm." % (_hm(h, m), dur),
                      _hm(st // 60, st % 60), "time", text=True,
                      placeholder="e.g. 2:15",
                      solution=["Count back %d minutes from %s." % (dur, _hm(h, m)),
                                "The lesson started at %s." % _hm(st // 60, st % 60)])

    if t == 2:                       # elapsed minutes
        h = random.randint(1, 10)
        m = pick([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        dur = random.randrange(_by_d(d, 10, 20, 25), _by_d(d, 60, 120, 180), 5)
        total = h * 60 + m + dur
        return _num_q("A journey starts at %s and ends at %s. How many minutes does "
                      "the journey take?" % (_hm(h, m), _hm(total // 60, total % 60)),
                      dur, "int", unit="minutes",
                      solution=["From %s to %s." % (_hm(h, m),
                                                    _hm(total // 60, total % 60)),
                                "That is %d minutes." % dur])

    if t == 3:                       # bus timetable
        rows = []
        legs = []
        base_h = random.randint(7, 15)
        for label in ["Bus A", "Bus B", "Bus C"]:
            sh = base_h + random.randint(0, 2)
            sm = pick(_by_d(d, [0, 30], [0, 10, 15, 20, 30, 40, 45, 50], _clock_minutes(2)))
            leg = random.randrange(*_by_d(d, (20, 70, 10), (20, 95, 5), (35, 140, 1)))
            end = sh * 60 + sm + leg
            legs.append(leg)
            rows.append([label, _hm24(sh, sm), _hm24(end // 60, end % 60)])
        k = random.randrange(3)
        return _table_q("The timetable shows three buses. How many minutes does the "
                        "%s journey take?" % rows[k][0],
                        ["Bus", "Leaves", "Arrives"], rows, legs[k], "int",
                        ["%s leaves at %s and arrives at %s."
                         % (rows[k][0], rows[k][1], rows[k][2]),
                         "That journey takes %d minutes." % legs[k]])

    if t == 4:                       # timetable with a missing arrival time
        rows = []
        ends = []
        base_h = random.randint(8, 14)
        for label in ["Train 1", "Train 2", "Train 3"]:
            sh = base_h + random.randint(0, 2)
            sm = pick(_by_d(d, [0, 30], [0, 10, 15, 20, 30, 45], _clock_minutes(2)))
            leg = random.randrange(*_by_d(d, (20, 70, 10), (20, 90, 5), (35, 140, 1)))
            end = sh * 60 + sm + leg
            ends.append((end, leg, sh, sm))
            rows.append([label, _hm24(sh, sm), _hm24(end // 60, end % 60),
                         "%d min" % leg])
        k = random.randrange(3)
        end, leg, sh, sm = ends[k]
        return _table_q("Complete the timetable. %s leaves at %s and the journey "
                        "takes %d minutes. What time does it arrive? Write it as a "
                        "24-hour time, like the timetable (hh:mm)." % (rows[k][0], rows[k][1], leg),
                        ["Train", "Leaves", "Arrives", "Journey"], rows,
                        _hm24(end // 60, end % 60), "time",
                        ["%s plus %d minutes." % (rows[k][1], leg),
                         "It arrives at %s." % _hm24(end // 60, end % 60)],
                        missing=(k, 2))

    if t == 5:                       # days in a month
        if d == 2:                   # stretch: two months in a row
            i = random.randrange(12)
            (n1, d1), (n2, d2) = _MONTHS[i], _MONTHS[(i + 1) % 12]
            note = " in an ordinary year" if "February" in (n1, n2) else ""
            return _num_q("How many days are there in %s and %s altogether%s?"
                          % (n1, n2, note), d1 + d2, "int", unit="days",
                          solution=["%s has %d days and %s has %d days." % (n1, d1, n2, d2),
                                    "%d + %d = %d days." % (d1, d2, d1 + d2)])
        name, days = pick(_MONTHS)
        return _num_q("How many days are there in %s%s?"
                      % (name, " in an ordinary year (not a leap year)" if name == "February" else ""),
                      days, "int", unit="days",
                      solution=["%s has %d days in an ordinary year." % (name, days)])

    if t == 6:                       # calendar: date of the next same weekday
        name, days = pick(_MONTHS)
        day = pick(_DAYS)
        k = random.randint(1, 3) if d else 1
        if d == 2:                   # stretch: the answer falls in the next month
            i = [mn for mn, _x in _MONTHS].index(name)
            nxt = _MONTHS[(i + 1) % 12][0]
            k = random.randint(2, 3)
            date = random.randint(days - 7 * k + 1, days)
            ans = date + 7 * k - days
            feb = " (it is not a leap year)" if name == "February" else ""
            return _num_q("The %s of %s is a %s%s. What is the date of the %s "
                          "%d weeks later, in %s?" % (_ord(date), name, day, feb, day, k, nxt),
                          ans, "int",
                          solution=["%d weeks is %d days, and %d + %d = %d."
                                    % (k, 7 * k, date, 7 * k, date + 7 * k),
                                    "%s has %d days, so that is %d − %d = the %s of %s."
                                    % (name, days, date + 7 * k, days, _ord(ans), nxt)])
        date = random.randint(1, days - 7 * k)
        return _num_q("The %s of %s is a %s. What is the date of the %s "
                      "%s later, in %s?" % (_ord(date), name, day, day,
                                            "1 week" if k == 1 else "%d weeks" % k,
                                            name),
                      date + 7 * k, "int",
                      solution=["The same weekday comes round every 7 days.",
                                "%d + %d = %d." % (date, 7 * k, date + 7 * k)])

    if t == 7:                       # days between two dates in a month
        name, days = pick(_MONTHS)
        if d == 2:                   # stretch: from one month into the next
            i = [mn for mn, _x in _MONTHS].index(name)
            nxt = _MONTHS[(i + 1) % 12][0]
            a = random.randint(days - 9, days - 1)
            b = random.randint(2, 15)
            ans = days - a + b
            feb = " (not a leap year)" if name == "February" else ""
            return _num_q("How many days after the %s of %s%s is the %s of %s?"
                          % (_ord(a), name, feb, _ord(b), nxt), ans, "int", unit="days",
                          solution=["%s has %d days: %d − %d = %s to the end of %s."
                                    % (name, days, days, a, _pl(days - a, "day"), name),
                                    "%d + %d = %d days." % (days - a, b, ans)])
        a = random.randint(1, days - 5)
        b = random.randint(a + 2, min(days, a + 10) if d == 0 else days)
        return _num_q("How many days after the %s of %s is the %s of %s?"
                      % (_ord(a), name, _ord(b), name), b - a, "int", unit="days",
                      solution=["%d − %d = %d days." % (b, a, b - a)])

    if t == 8:                       # elapsed time across the hour, in hours+minutes
        h = random.randint(1, 9)
        m = pick(_by_d(d, [0, 30], [10, 15, 20, 30, 40, 45], [7, 13, 22, 38, 41, 52]))
        hours = random.randint(*_by_d(d, (1, 2), (1, 3), (2, 4)))
        extra = pick([15, 30, 45]) if d == 0 else random.randrange(5, 55, 5) if d == 1 \
            else random.choice([x for x in range(1, 60) if x % 5])
        end = h * 60 + m + hours * 60 + extra
        return _num_q("A shop opens at %s and closes at %s. How many minutes is the "
                      "shop open for?" % (_hm(h, m), _hm(end // 60, end % 60)),
                      hours * 60 + extra, "int", unit="minutes",
                      solution=["From %s to %s is %s and %s."
                                % (_hm(h, m), _hm(end // 60, end % 60), _pl(hours, "hour"), _pl(extra, "minute")),
                                "That is %d minutes." % (hours * 60 + extra)])

    # club timetable: which activity is longest
    rows = []
    lens = []
    names = ["Football", "Art", "Choir", "Chess"]
    base_h = random.randint(9, 14)
    leg_range = _by_d(d, (20, 100, 10), (20, 100, 5), (25, 100, 1))
    for nm in names:
        sh = base_h + random.randint(0, 3)
        sm = pick(_by_d(d, [0, 30], [0, 15, 30, 45], _clock_minutes(2)))
        leg = random.randrange(*leg_range)
        while leg in lens:
            leg = random.randrange(*leg_range)
        lens.append(leg)
        end = sh * 60 + sm + leg
        rows.append([nm, _hm24(sh, sm), _hm24(end // 60, end % 60)])
    k = lens.index(max(lens))
    return _table_q("The timetable shows four clubs. Which club lasts the longest? "
                    "Type its name.", ["Club", "Starts", "Ends"], rows,
                    names[k], "str",
                    ["Work out how long each club lasts.",
                     "%s lasts %d minutes, which is the longest."
                     % (names[k], lens[k])])
