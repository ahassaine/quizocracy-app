# dev/app/logic/y6_gen_b.py — Year 6 generators: strands 6.2, 6.3 and 6.4
#
# 6.2  Factors, multiples & primes                    (Y6.2.a .. Y6.2.f)
# 6.3  Fractions: equivalence, comparing, + and -     (Y6.3.a .. Y6.3.h)
# 6.4  Fractions: x and /                             (Y6.4.a .. Y6.4.f)
#
# Every generator takes a difficulty tier: d = 0 (easy) / 1 (core) / 2 (stretch)
# and picks at random between many genuinely different framings (bare
# calculation, word problem, missing number, inverse, visual model, comparison,
# reasoning, multi-step).
#
# Visual components carry a large share of the framings:
#   fraction_bar / area_grid / number_line   -> the fraction strands
#   data_table / array / io_table            -> factors, multiples and primes
#   strip_model / bar_chart                  -> fraction-of-a-quantity problems
#
# NOTE on `frac` answers: check_answer accepts any equivalent fraction, so a
# question whose objective is "in its lowest terms" must ask for the numerator
# or the denominator as an int (or for a mixed number as a str) instead.
import random
from fractions import Fraction
from .maths_engine import skill, pick, NAMES, n_words, money

S2 = "6.2 Factors, multiples & primes"
S3 = "6.3 Fractions: equivalence, comparing, + and -"
S4 = "6.4 Fractions: x and /"

_OBJ = ["stickers", "marbles", "beads", "shells", "cards", "buttons",
        "counters", "pebbles"]
_CONT = ["boxes", "bags", "trays", "crates", "packets", "jars"]


# ---------------------------------------------------------------- helpers ----
def _t(d):
    """Clamp the difficulty tier to 0 / 1 / 2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by_d(d, easy, core, hard):
    return [easy, core, hard][_t(d)]


def _two_names():
    a = pick(NAMES)
    b = pick(NAMES)
    while b == a:
        b = pick(NAMES)
    return a, b


def _pl(n, word, plural=None):
    return "%d %s" % (n, word if abs(n) == 1 else (plural or word + "s"))


def _ord(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _hcf(a, b):
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


def _lcm(a, b):
    a, b = abs(int(a)), abs(int(b))
    if a == 0 or b == 0:
        return 0
    return a * b // _hcf(a, b)


def _factors(n):
    n = abs(int(n))
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i:
                out.append(n // i)
        i += 1
    return sorted(out)


def _factor_pairs(n):
    n = abs(int(n))
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append((i, n // i))
        i += 1
    return out


_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
           61, 67, 71, 73, 79, 83, 89, 97]
_PRIMESET = set(_PRIMES)


def _is_prime(n):
    n = int(n)
    if n < 2:
        return False
    if n <= 97:
        return n in _PRIMESET
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _prime_factors(n):
    """Prime factorisation with repeats, e.g. 60 -> [2, 2, 3, 5]."""
    n = int(n)
    out = []
    f = 2
    while f * f <= n:
        while n % f == 0:
            out.append(f)
            n //= f
        f += 1
    if n > 1:
        out.append(n)
    return out


def _pf_string(n):
    return " × ".join(str(p) for p in _prime_factors(n))


def _simp(n, d):
    g = _hcf(n, d)
    return n // g, d // g


def _mixed_str(w, n, d):
    """(2, 3, 4) -> '2 3/4';  (2, 0, 4) -> '2'."""
    w, n, d = int(w), int(n), int(d)
    if n == 0:
        return "%d" % w
    if w == 0:
        return "%d/%d" % (n, d)
    return "%d %d/%d" % (w, n, d)


def _improper_to_mixed(n, d):
    """(11, 4) -> (2, 3, 4) with the fraction part in lowest terms."""
    w = n // d
    rn, rd = n % d, d
    if rn:
        rn, rd = _simp(rn, rd)
    return w, rn, rd


_FRAC_WORDS = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth",
               7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
               11: "eleventh", 12: "twelfth", 15: "fifteenth",
               20: "twentieth", 100: "hundredth"}
_FRAC_PLURAL = {2: "halves"}


def _frac_words(n, d):
    """1/4 -> 'one quarter';  3/5 -> 'three fifths'."""
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%d/%d" % (n, d)
    if n == 1:
        return "one " + w
    return "%s %s" % (n_words(n), _FRAC_PLURAL.get(d, w + "s"))


def _plural_frac_word(d):
    w = _FRAC_WORDS.get(d)
    if not w:
        return "%dths" % d
    return _FRAC_PLURAL.get(d, w + "s")


# ------------------------------------------------------------- question ------
def _numq(prompt, answer, solution, unit=None, placeholder=None,
          answer_type="int", text=False, tolerance=0):
    spec = {}
    if text:
        spec["text"] = True
    if placeholder:
        spec["placeholder"] = placeholder
    if unit:
        spec["unit"] = unit
    return {"prompt": prompt, "component": "number", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "tolerance": tolerance, "solution": solution}


def _fracq(prompt, num, den, solution, placeholder="e.g. 3/4"):
    """A typed fraction answer (equivalent fractions are accepted)."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": "%d/%d" % (int(num), int(den)), "answer_type": "frac",
            "solution": solution}


def _wordq(prompt, answer, solution, placeholder=None):
    return _numq(prompt, answer, solution, placeholder=placeholder,
                 answer_type="str", text=True)


def _setq(prompt, values, solution, placeholder="e.g. 2, 3, 6"):
    vals = sorted(int(v) for v in values)
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": placeholder},
            "answer": ", ".join(str(v) for v in vals), "answer_type": "set",
            "solution": solution}


def _mixq(prompt, w, n, den, solution, strict=False):
    """A typed mixed-number answer, e.g. '2 3/4'. Marked by value (frac, which
    parses '2 3/4', '11/4' and unsimplified forms) unless `strict`, used only
    where writing the mixed form IS the objective."""
    return {"prompt": prompt, "component": "number",
            "spec": {"text": True, "placeholder": "e.g. 2 3/4"},
            "answer": _mixed_str(w, n, den),
            "answer_type": "str" if strict else "frac",
            "solution": solution}


def _fbq(prompt, parts, shaded, solution):
    """fraction_bar, shade mode — the answer is the shaded fraction."""
    return {"prompt": prompt, "component": "fraction_bar",
            "spec": {"parts": int(parts), "mode": "shade"},
            "answer": "%d/%d" % (int(shaded), int(parts)),
            "answer_type": "frac", "solution": solution}


def _agshade(prompt, parts, shaded, solution):
    """area_grid, fraction mode — the pupil shades the area model."""
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "fraction", "parts": int(parts)},
            "answer": "%d/%d" % (int(shaded), int(parts)),
            "answer_type": "frac", "solution": solution}


def _agread(prompt, parts, shaded, solution, answer=None, answer_type="frac",
            placeholder=None):
    """area_grid, fraction_read mode — a model with `shaded` of `parts` filled."""
    spec = {"mode": "fraction_read", "parts": int(parts), "shaded": int(shaded)}
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer if answer is not None
            else "%d/%d" % (int(shaded), int(parts)),
            "answer_type": answer_type, "solution": solution}


def _agarea(prompt, rows, cols, solution, answer=None, answer_type="int"):
    """area_grid, read_area mode — a rows × cols grid of unit squares."""
    rows, cols = int(rows), int(cols)
    return {"prompt": prompt, "component": "area_grid",
            "spec": {"mode": "read_area", "rows": rows, "cols": cols},
            "answer": rows * cols if answer is None else answer,
            "answer_type": answer_type, "solution": solution}


def _arrayq(prompt, rows, cols, solution, answer=None):
    rows, cols = int(rows), int(cols)
    return {"prompt": prompt, "component": "array",
            "spec": {"mode": "build",
                     "maxRows": min(12, max(6, rows + 2)),
                     "maxCols": min(12, max(6, cols + 2)),
                     "targetRows": rows, "targetCols": cols},
            "answer": rows * cols if answer is None else answer,
            "answer_type": "int", "solution": solution}


def _dtq(prompt, headers, rows, answer, solution, missing=None,
         answer_type="int", placeholder=None):
    spec = {"headers": [str(h) for h in headers],
            "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": answer_type,
            "solution": solution}


def _ioq(prompt, rows, missing, answer, solution, rule=None, placeholder=None):
    spec = {"rows": [[int(i), int(o)] for i, o in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": "int", "solution": solution}


def _stripq(prompt, parts, part_label, total_label, unknown, answer, solution):
    return {"prompt": prompt, "component": "strip_model",
            "spec": {"mode": "equal_parts", "parts": int(parts),
                     "partLabel": str(part_label),
                     "totalLabel": str(total_label), "unknown": unknown},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _barq(prompt, cats, vals, answer, solution):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats),
                     "values": [int(v) for v in vals], "mode": "read"},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _nlq(prompt, value, lo, hi, step, major, solution, tol=None):
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": lo, "max": hi, "step": step, "major": major},
            "answer": round(float(value), 6), "answer_type": "num",
            "tolerance": (step / 2.0) if tol is None else tol,
            "solution": solution}


def _nlfrac(prompt, num, den, hi, solution, lo=0):
    """Place num/den on a line from lo to hi ruled in 1/den steps."""
    step = 1.0 / den
    return _nlq(prompt, num / float(den), lo, hi, step, 1.0, solution,
                tol=step / 2.0)


# ================================================================== 6.2 ======
@skill("Y6.2.a", "Common factors and the HCF", S2)
def _(d=1):
    d = _t(d)
    if d == 0:
        g = pick([2, 3, 4, 5, 6])
        p, q = random.sample([1, 2, 3, 5, 7], 2)
    elif d == 1:
        g = pick([3, 4, 6, 8, 9, 12])
        p, q = random.sample([1, 2, 3, 4, 5, 7], 2)
    else:
        g = pick([6, 8, 9, 12, 14, 15, 16, 18])
        p, q = random.sample([2, 3, 4, 5, 7, 9], 2)
    while _hcf(p, q) != 1:
        p, q = random.sample([1, 2, 3, 5, 7, 9], 2)
    a, b = g * p, g * q

    def hcf_pair():
        return _numq("What is the highest common factor (HCF) of %d and %d?"
                     % (a, b), g,
                     ["The factors of %d are %s."
                      % (a, ", ".join(str(x) for x in _factors(a))),
                      "The factors of %d are %s."
                      % (b, ", ".join(str(x) for x in _factors(b))),
                      "The largest factor in both lists is %d." % g])

    def common_factors():
        common = [x for x in _factors(a) if b % x == 0]
        return _setq("List all the common factors of %d and %d. Separate them "
                     "with commas." % (a, b), common,
                     ["The common factors are the numbers that divide into "
                      "both %d and %d." % (a, b),
                      "They are %s." % ", ".join(str(x) for x in common)])

    def how_many_common():
        common = [x for x in _factors(a) if b % x == 0]
        return _numq("How many common factors do %d and %d have?" % (a, b),
                     len(common),
                     ["The common factors are %s."
                      % ", ".join(str(x) for x in common),
                      "That is %s." % _pl(len(common), "common factor")])

    def is_common_factor():
        if random.random() < 0.5:
            f = pick([x for x in _factors(g) if x > 1] or [1])
            return _wordq("Is %d a common factor of %d and %d? Type yes or no."
                          % (f, a, b), "yes",
                          ["%d ÷ %d = %d and %d ÷ %d = %d."
                           % (a, f, a // f, b, f, b // f),
                           "%d divides into both, so it is a common factor."
                           % f],
                          placeholder="yes or no")
        bad = g + 1
        while a % bad == 0 and b % bad == 0:
            bad += 1
        return _wordq("Is %d a common factor of %d and %d? Type yes or no."
                      % (bad, a, b), "no",
                      ["%d does not divide exactly into both %d and %d."
                       % (bad, a, b),
                       "So %d is not a common factor." % bad])

    def table_factors():
        rows = [[str(a), ", ".join(str(x) for x in _factors(a))],
                [str(b), ", ".join(str(x) for x in _factors(b))]]
        return _dtq("The table lists all the factors of each number. What is "
                    "the highest common factor of %d and %d?" % (a, b),
                    ["Number", "Factors"], rows, g,
                    ["Look for the numbers that appear in both rows.",
                     "The largest one is %d." % g])

    def word_bags():
        who = pick(NAMES)
        t1, t2 = pick(_OBJ), pick(_OBJ)
        while t2 == t1:
            t2 = pick(_OBJ)
        return _numq("%s has %d %s and %d %s. %s makes identical party bags "
                     "using every item, with the same number of %s in each bag "
                     "and the same number of %s in each bag. What is the "
                     "greatest number of party bags %s can make?"
                     % (who, a, t1, b, t2, who, t1, t2, who), g,
                     ["The number of bags must be a common factor of %d and "
                      "%d." % (a, b),
                      "The greatest common factor is %d, so %s bags."
                      % (g, g)], unit="bags")

    def word_tiles():
        rows, cols = pick([(4, 6), (6, 9), (8, 12), (9, 12), (10, 12),
                           (6, 8), (8, 10), (4, 10), (6, 10), (9, 6),
                           (12, 8), (10, 4)])
        gg = _hcf(rows, cols)
        return _agarea("This rectangle is %d squares wide and %d squares "
                       "tall. What is the side length of the largest square "
                       "tile that would fit into the rectangle exactly, with "
                       "no gaps?" % (cols, rows), rows, cols,
                       ["The tile's side must be a common factor of %d and %d."
                        % (rows, cols),
                        "The highest common factor of %d and %d is %d."
                        % (rows, cols, gg)], answer=gg)

    def hcf_three():
        c = g * pick([x for x in (2, 3, 5, 7, 11) if x not in (p, q)] or [11])
        return _numq("What is the highest common factor of %d, %d and %d?"
                     % (a, b, c), _hcf(_hcf(a, b), c),
                     ["%d divides into %d, %d and %d." % (g, a, b, c),
                      "No larger number divides into all three, so the HCF is "
                      "%d." % _hcf(_hcf(a, b), c)])

    def hcf_to_simplify():
        gg = _hcf(a, b)
        sn, sd = _simp(a, b)
        if a == b:
            return hcf_pair()
        big, small = (a, b) if a > b else (b, a)
        sn2, sd2 = _simp(small, big)
        return _numq("The fraction %d/%d is written in its lowest terms by "
                     "dividing both parts by their HCF. Type the numerator of "
                     "the fraction in its lowest terms." % (small, big), sn2,
                     ["The HCF of %d and %d is %d." % (small, big, gg),
                      "%d ÷ %d = %d, so the numerator is %d."
                      % (small, gg, sn2, sn2)])

    def missing_number():
        return _numq("The highest common factor of %d and a second number is "
                     "%d. The second number is a multiple of %d between %d and "
                     "%d. What is the second number?"
                     % (a, g, g, b - g + 1, b + g - 1), b,
                     ["The only multiple of %d between %d and %d is %d."
                      % (g, b - g + 1, b + g - 1, b),
                      "The HCF of %d and %d is %d." % (a, b, g)])

    def coprime_check():
        x, y = random.sample([9, 10, 11, 13, 14, 15, 16, 21, 25], 2)
        gg = _hcf(x, y)
        return _numq("What is the highest common factor of %d and %d?"
                     % (x, y), gg,
                     ["The common factors of %d and %d are %s."
                      % (x, y, ", ".join(str(z) for z in _factors(x)
                                         if y % z == 0)),
                      "The highest is %d." % gg])

    opts = [hcf_pair, hcf_pair, common_factors, how_many_common,
            is_common_factor, table_factors, word_bags, word_tiles,
            coprime_check]
    if d == 0:
        opts = [hcf_pair, common_factors, is_common_factor, table_factors,
                word_bags, word_tiles, how_many_common]
    elif d == 2:
        opts = [hcf_pair, common_factors, hcf_three, hcf_to_simplify,
                missing_number, word_bags, word_tiles, table_factors,
                coprime_check]
    opts = opts + [table_factors, word_tiles, table_factors]
    return pick(opts)()


@skill("Y6.2.b", "Common multiples and the LCM", S2)
def _(d=1):
    d = _t(d)
    if d == 0:
        a, b = random.sample([2, 3, 4, 5, 6], 2)
    elif d == 1:
        a, b = random.sample([3, 4, 5, 6, 8, 9, 10, 12], 2)
    else:
        a, b = random.sample([6, 8, 9, 10, 12, 14, 15, 16, 18], 2)
    L = _lcm(a, b)

    def lcm_pair():
        return _numq("What is the lowest common multiple (LCM) of %d and %d?"
                     % (a, b), L,
                     ["Multiples of %d: %s ..."
                      % (a, ", ".join(str(a * i) for i in range(1, 6))),
                      "Multiples of %d: %s ..."
                      % (b, ", ".join(str(b * i) for i in range(1, 6))),
                      "The smallest number in both lists is %d." % L])

    def first_common_multiples():
        vals = [L * i for i in (1, 2, 3)]
        return _setq("Write the first three common multiples of %d and %d. "
                     "Separate them with commas." % (a, b), vals,
                     ["The lowest common multiple is %d." % L,
                      "The next common multiples are multiples of %d: %s."
                      % (L, ", ".join(str(v) for v in vals))])

    def is_common_multiple():
        if random.random() < 0.5:
            m = L * random.randint(1, 3)
            return _wordq("Is %d a common multiple of %d and %d? Type yes or "
                          "no." % (m, a, b), "yes",
                          ["%d ÷ %d = %d and %d ÷ %d = %d."
                           % (m, a, m // a, m, b, m // b),
                           "%d divides exactly by both, so yes." % m],
                          placeholder="yes or no")
        cands = [a * i for i in range(2, 13) if (a * i) % b != 0]
        if not cands:
            cands = [b * i for i in range(1, 13) if (b * i) % a != 0]
        if not cands:
            return lcm_pair()
        m = pick(cands)
        miss = a if m % a else b
        return _wordq("Is %d a common multiple of %d and %d? Type yes or no."
                      % (m, a, b), "no",
                      ["%d ÷ %d = %d remainder %d, so it is not exact."
                       % (m, miss, m // miss, m % miss),
                       "So %d is not a common multiple of %d and %d."
                       % (m, a, b)], placeholder="yes or no")

    def table_multiples():
        rows = [[str(a), ", ".join(str(a * i) for i in range(1, 9))],
                [str(b), ", ".join(str(b * i) for i in range(1, 9))]]
        return _dtq("The table lists the first eight multiples of each number. "
                    "What is the lowest common multiple of %d and %d?"
                    % (a, b), ["Number", "Multiples"], rows, L,
                    ["Find the smallest number that appears in both rows.",
                     "It is %d." % L])

    def word_buses():
        who = pick(NAMES)
        return _numq("At a bus stop, one bus leaves every %d minutes and "
                     "another leaves every %d minutes. Both leave together at "
                     "9:00 am. How many minutes later do the two buses next "
                     "leave together?" % (a, b), L,
                     ["The buses leave together after a common multiple of %d "
                      "and %d minutes." % (a, b),
                      "The lowest common multiple is %d minutes." % L],
                     unit="minutes")

    def word_packs():
        return _numq("Bread rolls come in packs of %d and burgers come in "
                     "packs of %d. Whole packs are bought so that there are "
                     "exactly as many rolls as burgers. What is the smallest "
                     "number of rolls that can be bought?" % (a, b), L,
                     ["The total must be a multiple of both %d and %d."
                      % (a, b),
                      "The lowest common multiple is %d." % L])

    def packs_needed():
        return _numq("Rolls come in packs of %d and burgers come in packs of "
                     "%d. To have exactly the same number of each, how many "
                     "packs of rolls are needed?" % (a, b), L // a,
                     ["The lowest common multiple of %d and %d is %d."
                      % (a, b, L),
                      "%d ÷ %d = %s of rolls." % (L, a, _pl(L // a, "pack"))],
                     unit="packs")

    def on_line():
        st = min(a, b)
        other = max(a, b)
        top = st * ((L // st) + 1)
        return _nlq("This number line counts in steps of %d. Mark the lowest "
                    "common multiple of %d and %d." % (st, a, b), L, 0, top,
                    st, st * 2,
                    ["Every mark on the line is a multiple of %d." % st,
                     "The first one that is also a multiple of %d is %d."
                     % (other, L)])

    def io_multiples():
        rows = [[i, a * i] for i in range(1, 5)]
        k = random.randrange(4)
        return _ioq("This table lists the multiples of %d in order. Type the "
                    "missing Out number." % a, rows, k, rows[k][1],
                    ["The rule is × %d." % a,
                     "%d × %d = %d." % (rows[k][0], a, rows[k][1])],
                    rule="× %d" % a)

    def lcm_three():
        c = pick([x for x in (2, 3, 4, 5, 6) if x != a and x != b] or [7])
        return _numq("What is the lowest common multiple of %d, %d and %d?"
                     % (a, b, c), _lcm(L, c),
                     ["The LCM of %d and %d is %d." % (a, b, L),
                      "The LCM of %d and %d is %d." % (L, c, _lcm(L, c))])

    def lcm_as_denominator():
        return _numq("To add 1/%d and 1/%d, both fractions are rewritten with "
                     "the same denominator. What is the lowest common "
                     "denominator?" % (a, b), L,
                     ["The lowest common denominator is the LCM of %d and %d."
                      % (a, b),
                      "The LCM of %d and %d is %d." % (a, b, L)])

    def next_after():
        start = random.randint(1, 3) * L
        return _numq("The lowest common multiple of %d and %d is %d. What is "
                     "the next common multiple after %d?" % (a, b, L, start),
                     start + L,
                     ["Every common multiple of %d and %d is a multiple of %d."
                      % (a, b, L),
                      "%d + %d = %d." % (start, L, start + L)])

    opts = [lcm_pair, lcm_pair, first_common_multiples, is_common_multiple,
            table_multiples, word_buses, word_packs, on_line, io_multiples,
            lcm_as_denominator]
    if d == 0:
        opts = [lcm_pair, first_common_multiples, is_common_multiple,
                table_multiples, word_buses, on_line, io_multiples]
    elif d == 2:
        opts = [lcm_pair, first_common_multiples, lcm_three, packs_needed,
                word_buses, word_packs, next_after, lcm_as_denominator,
                table_multiples, on_line]
    opts = opts + [table_multiples, on_line, io_multiples]
    return pick(opts)()


@skill("Y6.2.c", "Prime and composite numbers to 100", S2)
def _(d=1):
    d = _t(d)
    lo, hi = _by_d(d, (2, 30), (2, 60), (30, 100))
    prime_pool = [p for p in _PRIMES if lo <= p <= hi]
    comp_pool = [n for n in range(max(4, lo), hi + 1) if not _is_prime(n)]

    def is_prime_q():
        if random.random() < 0.5:
            n = pick(prime_pool)
            return _wordq("Is %d a prime number? Type yes or no." % n, "yes",
                          ["%d has exactly two factors: 1 and %d." % (n, n),
                           "A number with exactly two factors is prime."],
                          placeholder="yes or no")
        n = pick(comp_pool)
        f = _prime_factors(n)[0]
        return _wordq("Is %d a prime number? Type yes or no." % n, "no",
                      ["%d ÷ %d = %d, so %d has more than two factors."
                       % (n, f, n // f, n),
                       "%d is a composite number." % n])

    def classify():
        n = pick(prime_pool + comp_pool)
        ans = "prime" if _is_prime(n) else "composite"
        if _is_prime(n):
            sol = ["The only factors of %d are 1 and %d." % (n, n),
                   "A number with exactly two factors is prime."]
        else:
            f = _prime_factors(n)[0]
            sol = ["%d is a factor of %d, as well as 1 and %d."
                   % (f, n, n),
                   "%d has more than two factors, so it is composite." % n]
        return _wordq("Is %d prime or composite? Type the word." % n, ans, sol,
                      placeholder="prime or composite")

    def table_classify():
        nums = random.sample(range(max(4, lo), hi + 1), 4)
        k = random.randrange(4)
        rows = [[str(x), "prime" if _is_prime(x) else "composite"]
                for x in nums]
        ans = rows[k][1]
        rows[k][1] = ""
        n = nums[k]
        if ans == "prime":
            sol = ["%d has exactly two factors, 1 and %d." % (n, n),
                   "So %d is prime." % n]
        else:
            f = _prime_factors(n)[0]
            sol = ["%d divides exactly by %d." % (n, f),
                   "So %d has more than two factors and is composite." % n]
        return _dtq("Complete the table. Type the missing word for %d — prime "
                    "or composite." % n, ["Number", "Prime or composite"],
                    rows, ans, sol, missing=(k, 1), answer_type="str",
                    placeholder="prime or composite")

    def next_prime():
        n = random.randint(lo, hi - 4)
        p = n + 1
        while not _is_prime(p):
            p += 1
        return _numq("What is the next prime number after %d?" % n, p,
                     ["Test each number after %d in turn." % n,
                      "%d is the first one with exactly two factors." % p])

    def previous_prime():
        n = random.randint(max(lo + 4, 6), hi)
        p = n - 1
        while p > 1 and not _is_prime(p):
            p -= 1
        return _numq("What is the largest prime number smaller than %d?" % n, p,
                     ["Work back from %d, testing each number." % n,
                      "%d is the first prime found, at %d." % (p, p)])

    def primes_between():
        a = random.randint(lo, max(lo, hi - 15))
        b = a + random.randint(8, 14)
        while _is_prime(a):
            a += 1
        while _is_prime(b):
            b += 1
        vals = [p for p in _PRIMES if a < p < b]
        if not vals:
            return next_prime()
        return _setq("List all the prime numbers between %d and %d. Separate "
                     "them with commas." % (a, b), vals,
                     ["Check each number from %d to %d for exactly two "
                      "factors." % (a + 1, b - 1),
                      "The primes are %s." % ", ".join(str(v) for v in vals)])

    def count_primes():
        a = random.randint(lo, max(lo, hi - 15))
        b = a + random.randint(9, 15)
        while _is_prime(a):
            a += 1
        while _is_prime(b):
            b += 1
        vals = [p for p in _PRIMES if a < p < b]
        return _numq("How many prime numbers are there between %d and %d?"
                     % (a, b), len(vals),
                     ["The primes between %d and %d are %s."
                      % (a, b, ", ".join(str(v) for v in vals) or "none"),
                      "That is %d." % len(vals)])

    def smallest_prime_factor():
        n = pick([x for x in comp_pool if not _is_prime(x)])
        f = _prime_factors(n)[0]
        return _numq("%d is a composite number. What is its smallest prime "
                     "factor?" % n, f,
                     ["%d ÷ %d = %d." % (n, f, n // f),
                      "%d is prime and is the smallest prime that divides %d."
                      % (f, n)])

    def which_is_prime():
        p = pick(prime_pool)
        others = random.sample([x for x in comp_pool if x != p], 3)
        nums = others + [p]
        random.shuffle(nums)
        rows = [[str(x), ", ".join(str(y) for y in _factors(x))]
                for x in nums]
        return _dtq("The table shows the factors of four numbers. Exactly one "
                    "of them is prime. Type that number.",
                    ["Number", "Factors"], rows, p,
                    ["A prime number has exactly two factors.",
                     "%d has only 1 and %d, so %d is the prime."
                     % (p, p, p)])

    def array_reason():
        n = pick([x for x in comp_pool if len(_factor_pairs(x)) > 1
                  and x <= 60])
        pairs = [(r, c) for r, c in _factor_pairs(n)
                 if 1 < r <= 10 and c <= 12]
        if not pairs:
            return is_prime_q()
        r, c = pick(pairs)
        return _arrayq("Build an array with %d rows of %d counters and type "
                       "how many counters it holds. The array shows that this "
                       "number has a factor other than 1 and itself, so it is "
                       "composite." % (r, c), r, c,
                       ["%d × %d = %d." % (r, c, n),
                        "%d is a factor of %d, so %d is not prime."
                        % (r, n, n)])

    def only_even_prime():
        return _numq("Exactly one even number is prime. What is it?", 2,
                     ["Every other even number divides by 2 as well as by 1 "
                      "and itself.",
                      "So 2 is the only even prime number."])

    def word_prime():
        who = pick(NAMES)
        n = pick(comp_pool)
        f = _prime_factors(n)[0]
        return _numq("%s has %d counters and wants to arrange them in equal "
                     "rows of more than one, using more than one row. What is "
                     "the smallest number of rows %s can use?"
                     % (who, n, who), f,
                     ["The number of rows must be a factor of %d that is more "
                      "than 1." % n,
                      "The smallest such factor is %d." % f], unit="rows")

    opts = [is_prime_q, classify, table_classify, next_prime, primes_between,
            smallest_prime_factor, which_is_prime, array_reason, count_primes]
    if d == 0:
        opts = [is_prime_q, classify, table_classify, next_prime,
                only_even_prime, which_is_prime, array_reason, primes_between]
    elif d == 2:
        opts = [is_prime_q, classify, next_prime, previous_prime,
                primes_between, count_primes, smallest_prime_factor,
                which_is_prime, table_classify, word_prime]
    opts = opts + [table_classify, which_is_prime, array_reason]
    return pick(opts)()


@skill("Y6.2.d", "Factor pairs and prime factorisation", S2)
def _(d=1):
    d = _t(d)
    if d == 0:
        n = pick([12, 16, 18, 20, 24, 28, 30])
    elif d == 1:
        n = pick([24, 30, 36, 40, 42, 45, 48, 54, 56, 60])
    else:
        n = pick([60, 64, 72, 75, 80, 84, 90, 96, 100])
    pf = _prime_factors(n)
    pairs = _factor_pairs(n)

    def all_factors():
        return _setq("List all the factors of %d. Separate them with commas."
                     % n, _factors(n),
                     ["Work through the factor pairs: %s."
                      % ", ".join("%d × %d" % (r, c) for r, c in pairs),
                      "The factors are %s."
                      % ", ".join(str(x) for x in _factors(n))])

    def count_factors():
        return _numq("How many factors does %d have altogether?" % n,
                     len(_factors(n)),
                     ["The factor pairs of %d are %s."
                      % (n, ", ".join("%d × %d" % (r, c) for r, c in pairs)),
                      "That gives %s in total."
                      % _pl(len(_factors(n)), "factor")])

    def count_pairs():
        return _numq("How many different factor pairs does %d have?" % n,
                     len(pairs),
                     ["The factor pairs are %s."
                      % ", ".join("%d × %d" % (r, c) for r, c in pairs),
                      "That is %s." % _pl(len(pairs), "pair")])

    def complete_pair():
        r, c = pick(pairs)
        return _numq("Complete the factor pair:  %d × ___ = %d" % (r, n), c,
                     ["%d ÷ %d = %d." % (n, r, c),
                      "So the factor pair is %d × %d." % (r, c)])

    def table_pairs():
        rows = [[str(r), str(c)] for r, c in pairs]
        k = random.randrange(len(rows))
        ans = int(rows[k][1])
        rows[k][1] = ""
        return _dtq("This table lists every factor pair of %d. Type the "
                    "missing number." % n, ["First factor", "Second factor"],
                    rows, ans,
                    ["%d ÷ %d = %d." % (n, pairs[k][0], ans),
                     "The pair is %d × %d = %d." % (pairs[k][0], ans, n)],
                    missing=(k, 1))

    def prime_factorisation_count():
        return _numq("%d written as a product of prime factors is %s. How many "
                     "prime factors are multiplied together?"
                     % (n, _pf_string(n)), len(pf),
                     ["%s has %s written down."
                      % (_pf_string(n), _pl(len(pf), "number")),
                      "So %d prime factors are multiplied together." % len(pf)])

    def missing_prime():
        idx = random.randrange(len(pf))
        shown = list(str(p) for p in pf)
        ans = pf[idx]
        shown[idx] = "___"
        return _numq("Complete the prime factorisation of %d:  %s"
                     % (n, " × ".join(shown)), ans,
                     ["The prime factorisation of %d is %s."
                      % (n, _pf_string(n)),
                      "The missing prime factor is %d." % ans])

    def largest_prime_factor():
        return _numq("What is the largest prime factor of %d?" % n, max(pf),
                     ["%d = %s." % (n, _pf_string(n)),
                      "The largest prime factor is %d." % max(pf)])

    def smallest_prime_factor():
        return _numq("What is the smallest prime factor of %d?" % n, min(pf),
                     ["%d = %s." % (n, _pf_string(n)),
                      "The smallest prime factor is %d." % min(pf)])

    def how_many_twos():
        target = min(set(pf))
        c = pf.count(target)
        return _numq("In the prime factorisation of %d, how many times does "
                     "the prime number %d appear?" % (n, target), c,
                     ["%d = %s." % (n, _pf_string(n)),
                      "%d appears %s." % (target, _pl(c, "time"))])

    def product_check():
        r, c = pick([pr for pr in pairs if pr[0] > 1] or pairs)
        return _numq("%d × %d = ___ . Both numbers are factors of the answer."
                     % (r, c), r * c,
                     ["%d × %d = %d." % (r, c, r * c)])

    def array_pair():
        cands = [(r, c) for r, c in pairs if 1 < r <= 10 and c <= 12]
        if not cands:
            return complete_pair()
        r, c = pick(cands)
        return _arrayq("Build an array of %d rows with %d counters in each row, "
                       "then type the total number of counters. %d and %d are "
                       "a factor pair of that total." % (r, c, r, c), r, c,
                       ["%d × %d = %d." % (r, c, n),
                        "%d and %d are a factor pair of %d." % (r, c, n)])

    def area_pair():
        cands = [(r, c) for r, c in pairs if 1 < r <= 10 and c <= 12]
        if not cands:
            return complete_pair()
        r, c = pick(cands)
        return _agarea("A rectangle is made from %d unit squares in %d rows. "
                       "How many squares are in each row?" % (n, r), r, c,
                       ["%d ÷ %d = %d." % (n, r, c),
                        "Each row holds %d squares." % c], answer=c)

    def word_rectangles():
        cands = [pr for pr in pairs]
        return _numq("%d square tiles are arranged into a rectangle. Every "
                     "tile must be used and every row must hold the same "
                     "number of tiles. How many different rectangles are "
                     "possible, counting a rectangle and its turn as the same "
                     "one? A single row of tiles counts as a rectangle."
                     % n, len(cands),
                     ["Each rectangle matches a factor pair: %s."
                      % ", ".join("%d × %d" % (r, c) for r, c in cands),
                      "That is %s." % _pl(len(cands), "rectangle")],
                     unit="rectangles")

    opts = [all_factors, count_factors, complete_pair, table_pairs,
            prime_factorisation_count, missing_prime, largest_prime_factor,
            array_pair, area_pair, count_pairs]
    if d == 0:
        opts = [all_factors, count_factors, complete_pair, table_pairs,
                array_pair, area_pair, product_check, count_pairs]
    elif d == 2:
        opts = [all_factors, count_factors, table_pairs, missing_prime,
                prime_factorisation_count, largest_prime_factor,
                smallest_prime_factor, how_many_twos, word_rectangles,
                area_pair]
    opts = opts + [table_pairs, array_pair, area_pair]
    return pick(opts)()


@skill("Y6.2.e", "Divisibility rules", S2)
def _(d=1):
    d = _t(d)
    divisors = _by_d(d, [2, 5, 10, 3], [2, 3, 4, 5, 6, 9, 10],
                     [3, 4, 6, 8, 9, 11, 25])
    lo, hi = _by_d(d, (20, 200), (100, 999), (500, 9999))

    def _rule(k):
        return {2: "a number is divisible by 2 if its last digit is even",
                3: "a number is divisible by 3 if its digit sum is divisible "
                   "by 3",
                4: "a number is divisible by 4 if its last two digits make a "
                   "number divisible by 4",
                5: "a number is divisible by 5 if it ends in 0 or 5",
                6: "a number is divisible by 6 if it is divisible by both 2 "
                   "and 3",
                8: "a number is divisible by 8 if halving it three times "
                   "still gives a whole number",
                9: "a number is divisible by 9 if its digit sum is divisible "
                   "by 9",
                10: "a number is divisible by 10 if it ends in 0",
                11: "a number is divisible by 11 if the alternating sum of "
                    "its digits is 0 or a multiple of 11",
                25: "a number is divisible by 25 if it ends in 00, 25, 50 or "
                    "75"}[k]

    def _digsum(x):
        return sum(int(c) for c in str(x))

    def yes_no():
        k = pick(divisors)
        if random.random() < 0.5:
            n = random.randint(lo // k, hi // k) * k
            return _wordq("Is %d divisible by %d? Type yes or no." % (n, k),
                          "yes",
                          ["Remember: %s." % _rule(k),
                           "%d ÷ %d = %d exactly." % (n, k, n // k)],
                          placeholder="yes or no")
        n = random.randint(lo, hi)
        while n % k == 0:
            n += 1
        return _wordq("Is %d divisible by %d? Type yes or no." % (n, k), "no",
                      ["Remember: %s." % _rule(k),
                       "%d ÷ %d = %d remainder %d, so it is not exact."
                       % (n, k, n // k, n % k)])

    def digit_sum():
        n = random.randint(lo, hi)
        return _numq("The divisibility rule for 3 and for 9 uses the digit "
                     "sum. What is the digit sum of %d?" % n, _digsum(n),
                     ["Add the digits: %s."
                      % " + ".join(str(c) for c in str(n)),
                      "The digit sum is %d." % _digsum(n)])

    def digit_sum_then():
        n = random.randint(lo // 3, hi // 3) * 3
        return _wordq("The digit sum of %d is %d. Is %d divisible by 3? Type "
                      "yes or no." % (n, _digsum(n), n), "yes",
                      ["%d ÷ 3 = %d, so the digit sum is a multiple of 3."
                       % (_digsum(n), _digsum(n) // 3),
                       "So %d is divisible by 3." % n], placeholder="yes or no")

    def remainder():
        k = pick([3, 4, 6, 7, 8, 9])
        n = random.randint(lo, hi)
        return _numq("What is the remainder when %d is divided by %d?" % (n, k),
                     n % k,
                     ["%d × %d = %d." % (k, n // k, k * (n // k)),
                      "%d − %d = %d." % (n, k * (n // k), n % k)],
                     placeholder="the remainder")

    def missing_digit():
        k = pick([3, 9])
        head = random.randint(1, 9)
        tail = random.randint(0, 9)
        cands = [x for x in range(10) if (head * 100 + x * 10 + tail) % k == 0]
        if not cands:
            return yes_no()
        ans = cands[0]
        return _numq("A digit is missing from this number:  %d__%d . What is "
                     "the smallest digit that makes the whole number divisible "
                     "by %d?" % (head, tail, k), ans,
                     ["Use the digit-sum rule: %s." % _rule(k),
                      "%d + %d + %d = %d, which is divisible by %d."
                      % (head, ans, tail, head + ans + tail, k)],
                     placeholder="a digit 0-9")

    def which_divisible():
        k = pick(divisors)
        good = random.randint(lo // k, hi // k) * k
        bads = []
        while len(bads) < 3:
            x = random.randint(lo, hi)
            if x % k != 0 and x not in bads and x != good:
                bads.append(x)
        nums = bads + [good]
        random.shuffle(nums)
        rows = [[str(x), str(_digsum(x))] for x in nums]
        return _dtq("The table shows four numbers and their digit sums. "
                    "Exactly one of them is divisible by %d. Type that number."
                    % k, ["Number", "Digit sum"], rows, good,
                    ["Remember: %s." % _rule(k),
                     "%d ÷ %d = %d exactly." % (good, k, good // k)])

    def list_divisible():
        k = pick([2, 3, 4, 5])
        nums = random.sample(range(lo, hi), 6)
        good = [x for x in nums if x % k == 0]
        if not good:
            good = [random.randint(lo // k, hi // k) * k]
            nums = nums[:5] + good
            random.shuffle(nums)
        return _setq("Which of these numbers are divisible by %d?  %s.  Type "
                     "them, separated by commas."
                     % (k, ", ".join(str(x) for x in nums)), good,
                     ["Remember: %s." % _rule(k),
                      "The numbers divisible by %d are %s."
                      % (k, ", ".join(str(x) for x in sorted(good)))])

    def which_divisor():
        n = pick([120, 180, 240, 300, 360, 420, 480, 540, 600])
        divs = [k for k in (3, 4, 6, 8, 9) if n % k == 0]
        return _setq("Which of 3, 4, 6, 8 and 9 divide exactly into %d? Type "
                     "them, separated by commas." % n, divs,
                     ["Test each one in turn.",
                      "%d divides exactly by %s."
                      % (n, ", ".join(str(x) for x in divs))])

    def word_share():
        k = pick([3, 4, 6, 8])
        n = random.randint(lo, hi)
        while n % k == 0:
            n += 1
        return _wordq("%d sweets are to be shared equally between %d children "
                      "with none left over. Is that possible? Type yes or no."
                      % (n, k), "no",
                      ["%d ÷ %d = %d remainder %d." % (n, k, n // k, n % k),
                       "There would be %s left over, so it is not possible."
                       % _pl(n % k, "sweet")], placeholder="yes or no")

    def word_boxes():
        k = pick([4, 6, 8, 9])
        n = random.randint(max(2, lo // k), hi // k) * k
        return _numq("%d pencils are packed into boxes of %d with none left "
                     "over. How many boxes are filled?" % (n, k), n // k,
                     ["%d is divisible by %d." % (n, k),
                      "%d ÷ %d = %d boxes." % (n, k, n // k)], unit="boxes")

    def rule_naming():
        k = pick([2, 5, 10])
        n = random.randint(lo // k, hi // k) * k
        return _numq("%d is divisible by %d. What is the last digit of %d?"
                     % (n, k, n), n % 10,
                     ["Remember: %s." % _rule(k),
                      "The last digit of %d is %d." % (n, n % 10)],
                     placeholder="a digit")

    def next_multiple():
        k = pick([3, 4, 6, 9])
        n = random.randint(lo, hi)
        nxt = ((n // k) + 1) * k
        return _numq("What is the next number after %d that is divisible by "
                     "%d?" % (n, k), nxt,
                     ["%d ÷ %d = %d remainder %d." % (n, k, n // k, n % k),
                      "%d × %d = %d." % (k, nxt // k, nxt)])

    opts = [yes_no, yes_no, digit_sum, remainder, which_divisible,
            list_divisible, word_boxes, next_multiple, digit_sum_then]
    if d == 0:
        opts = [yes_no, digit_sum, digit_sum_then, which_divisible,
                list_divisible, word_boxes, rule_naming]
    elif d == 2:
        opts = [yes_no, remainder, missing_digit, which_divisible,
                which_divisor, list_divisible, word_share, next_multiple,
                word_boxes]
    opts = opts + [which_divisible, which_divisible]
    return pick(opts)()


@skill("Y6.2.f", "Square and cube numbers", S2)
def _(d=1):
    d = _t(d)
    sq_range = _by_d(d, (2, 8), (2, 12), (5, 15))
    cu_range = _by_d(d, (2, 4), (2, 6), (3, 10))

    def square_bare():
        n = random.randint(*sq_range)
        return _numq("Work out %d². (%d² means %d × %d.)" % (n, n, n, n),
                     n * n, ["%d² = %d × %d = %d." % (n, n, n, n * n)])

    def cube_bare():
        n = random.randint(*cu_range)
        return _numq("Work out %d³. (%d³ means %d × %d × %d.)"
                     % (n, n, n, n, n), n ** 3,
                     ["%d × %d = %d." % (n, n, n * n),
                      "%d × %d = %d." % (n * n, n, n ** 3)])

    def square_root():
        n = random.randint(*sq_range)
        return _numq("Which number multiplied by itself gives %d?" % (n * n), n,
                     ["%d × %d = %d." % (n, n, n * n),
                      "So the number is %d." % n])

    def cube_root():
        n = random.randint(*cu_range)
        return _numq("A cube number is %d. Which number was multiplied by "
                     "itself three times to make it?" % (n ** 3), n,
                     ["%d × %d × %d = %d." % (n, n, n, n ** 3),
                      "So the number is %d." % n])

    def is_square():
        if random.random() < 0.5:
            n = random.randint(*sq_range)
            v = n * n
            return _wordq("Is %d a square number? Type yes or no." % v, "yes",
                          ["%d × %d = %d." % (n, n, v),
                           "%d is a square number." % v],
                          placeholder="yes or no")
        v = random.randint(sq_range[0] ** 2 + 1, sq_range[1] ** 2)
        while int(round(v ** 0.5)) ** 2 == v:
            v += 1
        r = int(v ** 0.5)
        return _wordq("Is %d a square number? Type yes or no." % v, "no",
                      ["%d² = %d and %d² = %d." % (r, r * r, r + 1,
                                                   (r + 1) ** 2),
                       "%d is between them, so it is not a square number."
                       % v])

    def square_area():
        n = random.randint(3, min(10, sq_range[1]))
        return _agarea("This square is %d squares long on each side. What is "
                       "its area, in square units?" % n, n, n,
                       ["The area of a square is side × side.",
                        "%d² = %d × %d = %d square units."
                        % (n, n, n, n * n)])

    def area_to_side():
        n = random.randint(3, min(10, sq_range[1]))
        return _agarea("This square has an area of %d square units. How long "
                       "is each side, in units?" % (n * n), n, n,
                       ["A square has equal sides, so side × side = %d."
                        % (n * n),
                        "%d × %d = %d, so each side is %d units."
                        % (n, n, n * n, n)], answer=n)

    def cube_volume():
        n = random.randint(*cu_range)
        return _numq("A cube has edges %d cm long. What is its volume, in cm³?"
                     % n, n ** 3,
                     ["Volume of a cube = edge × edge × edge.",
                      "%d³ = %d cm³." % (n, n ** 3)], unit="cm³")

    def list_squares():
        a = random.randint(1, 6)
        b = a + random.randint(3, 5)
        vals = [x * x for x in range(a, b + 1)]
        return _setq("List the square numbers from %d² to %d². Separate them "
                     "with commas." % (a, b), vals,
                     ["%s." % ", ".join("%d² = %d" % (x, x * x)
                                        for x in range(a, b + 1)),
                      "The square numbers are %s."
                      % ", ".join(str(v) for v in vals)])

    def sum_of_squares():
        a = random.randint(2, min(9, sq_range[1]))
        b = random.randint(2, min(9, sq_range[1]))
        return _numq("Work out %d² + %d²." % (a, b), a * a + b * b,
                     ["%d² = %d and %d² = %d." % (a, a * a, b, b * b),
                      "%d + %d = %d." % (a * a, b * b, a * a + b * b)])

    def difference_of_squares():
        a = random.randint(4, min(12, sq_range[1]))
        b = random.randint(2, a - 1)
        return _numq("Work out %d² − %d²." % (a, b), a * a - b * b,
                     ["%d² = %d and %d² = %d." % (a, a * a, b, b * b),
                      "%d − %d = %d." % (a * a, b * b, a * a - b * b)])

    def compare_powers():
        a = random.randint(2, 6)
        b = random.randint(2, 9)
        while a ** 3 == b * b:
            b += 1
        big = max(a ** 3, b * b)
        return _numq("Which is greater, %d³ or %d²? Type the greater value."
                     % (a, b), big,
                     ["%d³ = %d and %d² = %d." % (a, a ** 3, b, b * b),
                      "The greater value is %d." % big])

    def on_line():
        n = random.randint(3, 9)
        v = n * n
        lo = (v // 10) * 10
        return _nlq("Work out %d² and mark the answer on the number line, "
                    "which runs from %d to %d in steps of 1."
                    % (n, lo, lo + 10), v, lo, lo + 10, 1, 5,
                    ["%d² = %d × %d = %d." % (n, n, n, v),
                     "Mark %d on the line." % v])

    def table_squares():
        ins = sorted(random.sample(range(2, 13), 4))
        rows = [[i, i * i] for i in ins]
        k = random.randrange(4)
        return _ioq("Every Out number in this table is the square of the In "
                    "number. Type the missing Out number.", rows, k,
                    rows[k][1],
                    ["The rule is: multiply the number by itself.",
                     "%d × %d = %d." % (rows[k][0], rows[k][0], rows[k][1])],
                    rule="square it")

    def word_tiles():
        n = random.randint(4, min(12, sq_range[1]))
        return _numq("A square patio is made from square tiles, with %d tiles "
                     "along each side. How many tiles are used altogether?"
                     % n, n * n,
                     ["%d² = %d × %d = %d tiles." % (n, n, n, n * n)],
                     unit="tiles")

    def word_cubes():
        n = random.randint(*cu_range)
        return _numq("A large cube is built from small cubes, with %d small "
                     "cubes along each edge. How many small cubes are used "
                     "altogether?" % n, n ** 3,
                     ["%d³ = %d × %d × %d." % (n, n, n, n),
                      "That is %d small cubes." % (n ** 3)], unit="cubes")

    opts = [square_bare, cube_bare, square_root, square_area, cube_volume,
            list_squares, table_squares, word_tiles, on_line, is_square]
    if d == 0:
        opts = [square_bare, cube_bare, square_root, square_area,
                area_to_side, table_squares, on_line, word_tiles]
    elif d == 2:
        opts = [square_bare, cube_bare, cube_root, is_square, sum_of_squares,
                difference_of_squares, compare_powers, cube_volume,
                word_cubes, table_squares, area_to_side]
    opts = opts + [square_area, table_squares, on_line, area_to_side]
    return pick(opts)()


# ================================================================== 6.3 ======
@skill("Y6.3.a", "Equivalent fractions", S3)
def _(d=1):
    d = _t(d)
    base = pick(_by_d(d, [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)],
                      [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5),
                       (5, 6), (3, 8)],
                      [(2, 3), (3, 4), (2, 5), (4, 5), (5, 6), (3, 8), (5, 8),
                       (7, 10), (5, 12), (7, 12)]))
    n, den = base
    k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
              random.randint(3, 9))

    def missing_numerator():
        return _numq("Complete the equivalent fraction:  %d/%d = ___/%d"
                     % (n, den, den * k), n * k,
                     ["The denominator was multiplied by %d: %d × %d = %d."
                      % (k, den, k, den * k),
                      "Do the same to the numerator: %d × %d = %d."
                      % (n, k, n * k)])

    def missing_denominator():
        return _numq("Complete the equivalent fraction:  %d/%d = %d/___"
                     % (n, den, n * k), den * k,
                     ["The numerator was multiplied by %d: %d × %d = %d."
                      % (k, n, k, n * k),
                      "Do the same to the denominator: %d × %d = %d."
                      % (den, k, den * k)])

    def missing_down():
        return _numq("Complete the equivalent fraction:  %d/%d = ___/%d"
                     % (n * k, den * k, den), n,
                     ["The denominator was divided by %d: %d ÷ %d = %d."
                      % (k, den * k, k, den),
                      "Do the same to the numerator: %d ÷ %d = %d."
                      % (n * k, k, n)])

    def multiplier():
        return _numq("%d/%d = %d/%d. What number were the numerator and the "
                     "denominator both multiplied by?"
                     % (n, den, n * k, den * k), k,
                     ["%d ÷ %d = %d." % (den * k, den, k),
                      "Both parts were multiplied by %d." % k])

    def shade_bar():
        options = [m for m in (2, 3, 4, 5, 6) if den * m <= 12]
        if not options:
            return read_area()
        kk = pick(options)
        parts = den * kk
        return _fbq("This bar has %d equal parts. Shade it to show a fraction "
                    "equivalent to %d/%d." % (parts, n, den), parts, n * kk,
                    ["%d/%d = %d/%d." % (n, den, n * kk, parts),
                     "Shade %d of the %d parts." % (n * kk, parts)])

    def shade_area():
        options = [m for m in (2, 3, 4) if den * m <= 12]
        if not options:
            return read_area()
        kk = pick(options)
        parts = den * kk
        return _agshade("This area model has %d equal parts. Shade it to show "
                        "a fraction equivalent to %d/%d." % (parts, n, den),
                        parts, n * kk,
                        ["%d/%d and %d/%d cover the same amount."
                         % (n, den, n * kk, parts),
                         "Shade %d of the %d equal parts." % (n * kk, parts)])

    def read_area():
        parts = pick([6, 8, 10, 12])
        num = random.randint(1, parts - 1)
        sn, sd = _simp(num, parts)
        return _agread("Write the fraction of this area model that is shaded, "
                       "using the number of equal parts you can see.",
                       parts, num,
                       ["The model has %d equal parts with %s shaded."
                        % (parts, _pl(num, "part")),
                        "That is %d/%d." % (num, parts)],
                       placeholder="e.g. 3/4")

    def on_line():
        line_den = pick([6, 8, 10, 12])
        cands = [(a, b) for a, b in [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4),
                                     (1, 5), (2, 5), (3, 5), (1, 6), (5, 6)]
                 if (a * line_den) % b == 0 and a < b]
        if not cands:
            return shade_bar()
        en, ed = pick(cands)
        return _nlfrac("This number line from 0 to 1 is divided into %d equal "
                       "steps. Mark the point equivalent to %d/%d."
                       % (line_den, en, ed), en * line_den // ed, line_den, 1,
                       ["%d/%d = %d/%d." % (en, ed, en * line_den // ed,
                                            line_den),
                        "Count %d steps from 0." % (en * line_den // ed)])

    def how_many():
        word = _plural_frac_word(den * k)
        return _numq("How many %s are the same as %s?"
                     % (word, _frac_words(n, den)), n * k,
                     ["%d/%d = %d/%d." % (n, den, n * k, den * k),
                      "So the answer is %d." % (n * k)], unit=word)

    def hundredths():
        m = random.randint(1, 9)
        if random.random() < 0.5:
            return _numq("Complete:  %d/10 = ___/100" % m, m * 10,
                         ["Multiply the numerator and the denominator by 10.",
                          "%d/10 = %d/100." % (m, m * 10)])
        return _numq("Complete:  %d/100 = ___/10" % (m * 10), m,
                     ["Divide the numerator and the denominator by 10.",
                      "%d/100 = %d/10." % (m * 10, m)])

    def common_denominator():
        d1, d2 = random.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
        L = _lcm(d1, d2)
        a = random.randint(1, d1 - 1)
        return _numq("%d/%d is rewritten with a denominator of %d. What is the "
                     "new numerator?" % (a, d1, L), a * (L // d1),
                     ["%d ÷ %d = %d, so both parts are multiplied by %d."
                      % (L, d1, L // d1, L // d1),
                      "%d × %d = %d." % (a, L // d1, a * (L // d1))])

    def word_cake():
        who = pick(NAMES)
        parts = den * k
        return _numq("%s cuts a cake into %d equal slices and takes %s of the "
                     "whole cake. How many slices does %s take?"
                     % (who, parts, _frac_words(n, den), who), n * k,
                     ["%d slices ÷ %d = %d slices in one %s."
                      % (parts, den, k, _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %d slices." % (k, n, n * k)], unit="slices")

    def which_equivalent():
        good = "%d/%d" % (n * k, den * k)
        bad = "%d/%d" % (n * k + 1, den * k)
        if random.random() < 0.5:
            labels, ans = [good, bad], "A"
        else:
            labels, ans = [bad, good], "B"
        return _wordq("Which fraction is equivalent to %d/%d?  A: %s   B: %s.  "
                      "Type A or B." % (n, den, labels[0], labels[1]), ans,
                      ["Multiply the numerator and the denominator of %d/%d by "
                       "%d." % (n, den, k),
                       "%d/%d = %d/%d, so the answer is %s."
                       % (n, den, n * k, den * k, ans)], placeholder="A or B")

    def arithmetic_sequence():
        """An arithmetic sequence of fractions: a constant fraction difference."""
        sden = pick(_by_d(d, [4, 5, 8, 10], [5, 6, 8, 10, 12],
                          [6, 8, 9, 10, 12, 16]))
        step = random.randint(1, max(1, sden // 3))
        start = random.randint(1, max(1, sden // 2))
        terms = [start + i * step for i in range(4)]
        nxt = start + 4 * step
        shown = ", ".join("%d/%d" % (v, sden) for v in terms)
        return _fracq("Here is an arithmetic sequence of fractions:  %s, ___ ."
                      "  What is the next term in the sequence? Write it as a "
                      "fraction." % shown, nxt, sden,
                      ["The constant difference between the terms is %d/%d."
                       % (step, sden),
                       "%d/%d + %d/%d = %d/%d."
                       % (terms[3], sden, step, sden, nxt, sden)])

    def geometric_sequence():
        """A geometric sequence of fractions: a constant ratio."""
        r = pick([2, 2, 3])
        if r == 2:
            gn, g0 = pick([(1, 2), (1, 3), (1, 4), (1, 8), (3, 4), (3, 8)])
        else:
            gn, g0 = pick([(1, 2), (1, 3), (1, 9)])
        dens = [g0 * (r ** i) for i in range(4)]
        nxt_den = g0 * (r ** 4)
        shown = ", ".join("%d/%d" % (gn, x) for x in dens)
        return _fracq("Here is a geometric sequence of fractions:  %s, ___ ."
                      "  What is the next term in the sequence? Write it as a "
                      "fraction." % shown, gn, nxt_den,
                      ["Each term is one %s of the term before, because the "
                       "denominator is multiplied by %d each time."
                       % (_FRAC_WORDS.get(r, "%dth" % r), r),
                       "%d × %d = %d, so the next term is %d/%d."
                       % (dens[3], r, nxt_den, gn, nxt_den)])

    def table_equivalents():
        rows = [["%d/%d" % (n * i, den * i), str(den * i)] for i in
                range(1, 5)]
        j = random.randrange(4)
        ans = int(rows[j][1])
        rows[j][1] = ""
        rows[j][0] = "%d/?" % (n * (j + 1))
        return _dtq("Every fraction in this table is equivalent to %d/%d. Type "
                    "the missing denominator." % (n, den),
                    ["Fraction", "Denominator"], rows, ans,
                    ["%d/%d = %d/%d." % (n, den, n * (j + 1), den * (j + 1)),
                     "The missing denominator is %d." % ans], missing=(j, 1))

    opts = [missing_numerator, missing_denominator, multiplier, shade_bar,
            shade_area, read_area, on_line, how_many, hundredths, word_cake,
            table_equivalents, arithmetic_sequence, geometric_sequence]
    if d == 0:
        opts = [missing_numerator, missing_denominator, shade_bar, shade_area,
                read_area, on_line, hundredths, table_equivalents,
                arithmetic_sequence]
    elif d == 2:
        opts = [missing_numerator, missing_denominator, missing_down,
                multiplier, how_many, which_equivalent, common_denominator,
                word_cake, shade_area, on_line, table_equivalents,
                arithmetic_sequence, geometric_sequence]
    opts = opts + [shade_area, on_line, shade_bar, read_area]
    return pick(opts)()


@skill("Y6.3.b", "Simplify fractions to lowest terms", S3)
def _(d=1):
    d = _t(d)
    simple = pick(_by_d(d, [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)],
                        [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5),
                         (3, 5), (4, 5), (5, 6), (3, 8)],
                        [(2, 3), (3, 4), (2, 5), (4, 5), (5, 6), (3, 8),
                         (5, 8), (7, 10), (5, 12), (7, 12), (4, 9)]))
    sn, sd = simple
    k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
              random.randint(3, 9))
    bn, bd = sn * k, sd * k

    def numerator_of_lowest():
        return _numq("Write %d/%d in its lowest terms. Type the numerator of "
                     "the answer." % (bn, bd), sn,
                     ["The HCF of %d and %d is %d." % (bn, bd, k),
                      "%d ÷ %d = %d, so the numerator is %d."
                      % (bn, k, sn, sn)])

    def denominator_of_lowest():
        return _numq("Write %d/%d in its lowest terms. Type the denominator of "
                     "the answer." % (bn, bd), sd,
                     ["The HCF of %d and %d is %d." % (bn, bd, k),
                      "%d ÷ %d = %d, so the denominator is %d."
                      % (bd, k, sd, sd)])

    def divide_by_what():
        return _numq("To write %d/%d in its lowest terms, the numerator and "
                     "the denominator are both divided by the same number. "
                     "What is that number?" % (bn, bd), k,
                     ["The highest common factor of %d and %d is %d."
                      % (bn, bd, k),
                      "%d ÷ %d = %d and %d ÷ %d = %d."
                      % (bn, k, sn, bd, k, sd)])

    def already_lowest():
        if random.random() < 0.5:
            return _wordq("Is %d/%d already in its lowest terms? Type yes or "
                          "no." % (sn, sd), "yes",
                          ["The only number that divides both %d and %d is 1."
                           % (sn, sd),
                           "So %d/%d is already in its lowest terms."
                           % (sn, sd)], placeholder="yes or no")
        return _wordq("Is %d/%d already in its lowest terms? Type yes or no."
                      % (bn, bd), "no",
                      ["Both %d and %d can be divided by %d." % (bn, bd, k),
                       "%d/%d = %d/%d, so it was not in its lowest terms."
                       % (bn, bd, sn, sd)], placeholder="yes or no")

    def shade_lowest():
        return _fbq("This bar has %d equal parts. Write %d/%d in its lowest "
                    "terms, then shade the bar to show it." % (sd, bn, bd),
                    sd, sn,
                    ["%d/%d = %d/%d in its lowest terms." % (bn, bd, sn, sd),
                     "Shade %d of the %d parts." % (sn, sd)])

    def area_lowest():
        cands = [m for m in (sd, sd * 2, sd * 3) if 3 <= m <= 12 and m != bd]
        if not cands:
            return shade_lowest()
        parts = cands[0]
        shaded = sn * (parts // sd)
        return _agshade("Write %d/%d in its lowest terms, then shade this area "
                        "model of %d equal parts to show the same amount."
                        % (bn, bd, parts), parts, shaded,
                        ["%d/%d in its lowest terms is %d/%d."
                         % (bn, bd, sn, sd),
                         "On a model of %d equal parts that is %s shaded."
                         % (parts, _pl(shaded, "part"))])

    def read_area_lowest():
        parts = pick([6, 8, 10, 12])
        num = random.choice([x for x in range(1, parts)
                             if _hcf(x, parts) > 1] or [2])
        rn, rd = _simp(num, parts)
        return _agread("This area model has %d equal parts. Write the shaded "
                       "fraction in its lowest terms and type its denominator."
                       % parts, parts, num,
                       ["The shaded fraction is %d/%d." % (num, parts),
                        "Dividing both parts by %d gives %d/%d."
                        % (_hcf(num, parts), rn, rd)],
                       answer=rd, answer_type="int",
                       placeholder="the denominator")

    def which_is_lowest():
        if random.random() < 0.5:
            labels, ans = ["%d/%d" % (bn, bd), "%d/%d" % (sn, sd)], "B"
        else:
            labels, ans = ["%d/%d" % (sn, sd), "%d/%d" % (bn, bd)], "A"
        return _wordq("These two fractions are equivalent. Which one is "
                      "written in its lowest terms?  A: %s   B: %s.  Type A or "
                      "B." % (labels[0], labels[1]), ans,
                      ["%d/%d can still be divided by %d." % (bn, bd, k),
                       "%d/%d cannot be simplified further, so the answer is "
                       "%s." % (sn, sd, ans)], placeholder="A or B")

    def word_counters():
        tot, red = bd, bn
        return _numq("A bag holds %d counters and %d of them are red. Written "
                     "in its lowest terms, the fraction of counters that are "
                     "red is %d/___ . Type the missing denominator."
                     % (tot, red, sn), sd,
                     ["%d/%d of the counters are red." % (red, tot),
                      "Divide both parts by %d: %d/%d." % (k, sn, sd)])

    def word_slices():
        who = pick(NAMES)
        return _numq("A cake is cut into %d equal slices and %s eats %d of "
                     "them. In its lowest terms the fraction %s eats is "
                     "___/%d of the cake. Type the missing numerator."
                     % (bd, who, bn, who, sd), sn,
                     ["%s eats %d/%d of the cake." % (who, bn, bd),
                      "%d/%d = %d/%d in its lowest terms."
                      % (bn, bd, sn, sd)])

    def hundredths_lowest():
        hk = pick([10, 15, 20, 24, 25, 30, 35, 40, 45, 50, 60, 64, 70, 75,
                   80, 90, 96])
        rn, rd = _simp(hk, 100)
        return _numq("Write %d/100 in its lowest terms. Type the denominator "
                     "of the answer." % hk, rd,
                     ["The HCF of %d and 100 is %d." % (hk, _hcf(hk, 100)),
                      "%d/100 = %d/%d." % (hk, rn, rd)])

    def table_lowest():
        pairs = []
        while len(pairs) < 3:
            a, b = random.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
            if a < b and _hcf(a, b) > 1 and [a, b] not in pairs:
                pairs.append([a, b])
        rows = [["%d/%d" % (a, b), "%d/%d" % _simp(a, b)] for a, b in pairs]
        j = random.randrange(3)
        a, b = pairs[j]
        rn, rd = _simp(a, b)
        rows[j][1] = ""
        return _dtq("Complete the table. Type the denominator of %d/%d written "
                    "in its lowest terms." % (a, b),
                    ["Fraction", "Lowest terms"], rows, rd,
                    ["The HCF of %d and %d is %d." % (a, b, _hcf(a, b)),
                     "%d/%d = %d/%d." % (a, b, rn, rd)], missing=(j, 1),
                    placeholder="the denominator")

    def hcf_first():
        return _numq("What is the highest common factor of %d and %d? You "
                     "would divide by it to write %d/%d in its lowest terms."
                     % (bn, bd, bn, bd), k,
                     ["The common factors of %d and %d include %d."
                      % (bn, bd, k),
                      "The highest common factor is %d." % k])

    opts = [numerator_of_lowest, denominator_of_lowest, divide_by_what,
            already_lowest, shade_lowest, area_lowest, read_area_lowest,
            word_counters, word_slices, table_lowest, hcf_first]
    if d == 0:
        opts = [numerator_of_lowest, denominator_of_lowest, divide_by_what,
                already_lowest, shade_lowest, area_lowest, read_area_lowest,
                table_lowest]
    elif d == 2:
        opts = [numerator_of_lowest, denominator_of_lowest, divide_by_what,
                already_lowest, which_is_lowest, word_counters, word_slices,
                hundredths_lowest, read_area_lowest, area_lowest, hcf_first,
                table_lowest]
    opts = opts + [shade_lowest, area_lowest, read_area_lowest]
    return pick(opts)()


@skill("Y6.3.c", "Improper fractions and mixed numbers", S3)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [2, 3, 4], [3, 4, 5, 6, 8], [5, 6, 7, 8, 9, 10, 12]))
    whole = _by_d(d, random.randint(1, 2), random.randint(1, 4),
                  random.randint(2, 6))
    part = pick([x for x in range(1, den) if _hcf(x, den) == 1])
    imp = whole * den + part

    def improper_to_mixed_whole():
        return _numq("Write %d/%d as a mixed number. Type the whole-number "
                     "part." % (imp, den), whole,
                     ["%d ÷ %d = %d remainder %d." % (imp, den, whole, part),
                      "The whole-number part is %d." % whole])

    def improper_to_mixed_num():
        return _numq("Write %d/%d as a mixed number. Type the numerator of the "
                     "fraction part." % (imp, den), part,
                     ["%d ÷ %d = %d remainder %d." % (imp, den, whole, part),
                      "The mixed number is %s, so the numerator is %d."
                      % (_mixed_str(whole, part, den), part)])

    def improper_to_mixed_full():
        return _mixq("Write %d/%d as a mixed number. Type it like  2 3/4 ."
                     % (imp, den), whole, part, den,
                     ["%d ÷ %d = %d remainder %d." % (imp, den, whole, part),
                      "So %d/%d = %s." % (imp, den,
                                          _mixed_str(whole, part, den))],
                     strict=True)

    def mixed_to_improper():
        return _numq("Write the mixed number %s as an improper fraction. The "
                     "denominator stays %d — type the numerator."
                     % (_mixed_str(whole, part, den), den), imp,
                     ["%d whole = %d × %d = %d %s."
                      % (whole, whole, den, whole * den,
                         _plural_frac_word(den)),
                      "%d + %d = %d, so the fraction is %d/%d."
                      % (whole * den, part, imp, imp, den)])

    def mixed_to_improper_frac():
        return _fracq("Write the mixed number %s as an improper fraction."
                      % _mixed_str(whole, part, den), imp, den,
                      ["%d whole = %d/%d." % (whole, whole * den, den),
                       "%d/%d + %d/%d = %d/%d."
                       % (whole * den, den, part, den, imp, den)])

    def how_many_wholes():
        return _numq("How many whole ones are there in %d/%d?" % (imp, den),
                     whole,
                     ["%d/%d makes one whole." % (den, den),
                      "%d ÷ %d = %d remainder %d, so there are %s."
                      % (imp, den, whole, part, _pl(whole, "whole"))],
                     unit="wholes")

    def parts_left_over():
        return _numq("%d/%d is made of %s and a fraction left over. How many "
                     "%s are left over?"
                     % (imp, den, _pl(whole, "whole"), _plural_frac_word(den)),
                     part,
                     ["%d × %d = %d." % (whole, den, whole * den),
                      "%d − %d = %d, so %s are left over."
                      % (imp, whole * den, part,
                         _pl(part, _FRAC_WORDS.get(den, "part")))])

    def whole_as_improper():
        w = random.randint(2, 5)
        return _numq("How many %s are there in %d whole ones? In other words, "
                     "%d = ___/%d." % (_plural_frac_word(den), w, w, den),
                     w * den,
                     ["One whole is %d/%d." % (den, den),
                      "%d × %d = %d." % (w, den, w * den)])

    def on_line():
        hi = whole + 1
        if hi * den > 30:
            return improper_to_mixed_whole()
        return _nlfrac("Mark %d/%d on the number line. Each small step is "
                       "1/%d." % (imp, den, den), imp, den, hi,
                       ["%d/%d = %s." % (imp, den,
                                         _mixed_str(whole, part, den)),
                        "Count %d steps of 1/%d from 0." % (imp, den)])

    def on_line_mixed():
        hi = whole + 1
        if hi * den > 30:
            return mixed_to_improper()
        return _nlfrac("Mark the mixed number %s on the number line."
                       % _mixed_str(whole, part, den), imp, den, hi,
                       ["%s means %d whole and %d/%d."
                        % (_mixed_str(whole, part, den), whole, part, den),
                        "That is %d/%d, or %d steps of 1/%d from 0."
                        % (imp, den, imp, den)])

    def shade_part():
        if den > 12:
            return improper_to_mixed_num()
        return _fbq("%d/%d is written as the mixed number %s. This bar shows "
                    "one whole in %d equal parts — shade it to show just the "
                    "fraction part of the mixed number."
                    % (imp, den, _mixed_str(whole, part, den), den),
                    den, part,
                    ["%d ÷ %d = %d remainder %d." % (imp, den, whole, part),
                     "The fraction part is %d/%d, so shade %s."
                     % (part, den, _pl(part, "part"))])

    def area_part():
        if den > 12:
            return improper_to_mixed_num()
        return _agshade("A recipe needs %s cups of flour. This area model "
                        "shows one whole cup split into %d equal parts. Shade "
                        "it to show the fraction part of %s."
                        % (_mixed_str(whole, part, den), den,
                           _mixed_str(whole, part, den)), den, part,
                        ["The fraction part of %s is %d/%d."
                         % (_mixed_str(whole, part, den), part, den),
                         "Shade %d of the %d equal parts." % (part, den)])

    def word_pizzas():
        who = pick(NAMES)
        return _numq("%s has %d/%d of a pizza, where every pizza is cut into "
                     "%d equal slices. How many whole pizzas can %s make from "
                     "those slices?" % (who, imp, den, den, who), whole,
                     ["%d slices ÷ %d slices per pizza = %d remainder %d."
                      % (imp, den, whole, part),
                      "%s can make %s." % (who, _pl(whole, "whole pizza"))],
                     unit="pizzas")

    def word_jugs():
        who = pick(NAMES)
        return _numq("%s pours %s litres of juice into glasses that each hold "
                     "1/%d of a litre. How many glasses does %s fill?"
                     % (who, _mixed_str(whole, part, den), den, who), imp,
                     ["%s litres = %d/%d litres."
                      % (_mixed_str(whole, part, den), imp, den),
                      "Each glass is 1/%d of a litre, so %d glasses are "
                      "filled." % (den, imp)], unit="glasses")

    def table_convert():
        rows = []
        for i in range(3):
            w = random.randint(1, 4)
            p = random.randint(1, den - 1)
            rows.append([_mixed_str(w, p, den), "%d/%d" % (w * den + p, den),
                         w * den + p])
        j = random.randrange(3)
        ans = rows[j][2]
        table = [[r[0], r[1]] for r in rows]
        table[j][1] = ""
        w = int(rows[j][0].split()[0])
        p = int(rows[j][0].split()[1].split("/")[0])
        return _dtq("Complete the table. Type the numerator of %s written as "
                    "an improper fraction." % rows[j][0],
                    ["Mixed number", "Improper fraction"], table, ans,
                    ["%d × %d = %d." % (w, den, w * den),
                     "%d + %d = %d, so %s = %d/%d."
                     % (w * den, p, ans, rows[j][0], ans, den)],
                    missing=(j, 1), placeholder="the numerator")

    opts = [improper_to_mixed_whole, improper_to_mixed_num,
            improper_to_mixed_full, mixed_to_improper, mixed_to_improper_frac,
            how_many_wholes, on_line, on_line_mixed, shade_part, area_part,
            word_pizzas, table_convert]
    if d == 0:
        opts = [improper_to_mixed_whole, improper_to_mixed_num,
                mixed_to_improper, how_many_wholes, whole_as_improper,
                on_line, shade_part, area_part, table_convert]
    elif d == 2:
        opts = [improper_to_mixed_full, improper_to_mixed_num,
                mixed_to_improper, mixed_to_improper_frac, parts_left_over,
                word_pizzas, word_jugs, on_line_mixed, table_convert,
                area_part]
    opts = opts + [on_line, shade_part, area_part, on_line_mixed]
    return pick(opts)()


@skill("Y6.3.d", "Compare and order fractions", S3)
def _(d=1):
    d = _t(d)
    dens = _by_d(d, [2, 3, 4, 6], [2, 3, 4, 5, 6, 8, 10, 12],
                 [3, 4, 5, 6, 7, 8, 9, 10, 12])

    def _pair():
        """Two different fractions with different values."""
        for _ in range(40):
            d1, d2 = pick(dens), pick(dens)
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            if Fraction(n1, d1) != Fraction(n2, d2):
                return (n1, d1), (n2, d2)
        return (1, 2), (1, 3)

    def larger_of_two():
        (n1, d1), (n2, d2) = _pair()
        L = _lcm(d1, d2)
        big = (n1, d1) if Fraction(n1, d1) > Fraction(n2, d2) else (n2, d2)
        return _fracq("Which is larger, %d/%d or %d/%d? Write the fraction."
                      % (n1, d1, n2, d2), big[0], big[1],
                      ["Rewrite both with denominator %d: %d/%d = %d/%d and "
                       "%d/%d = %d/%d."
                       % (L, n1, d1, n1 * (L // d1), L, n2, d2,
                          n2 * (L // d2), L),
                       "%d/%d is larger." % (big[0], big[1])])

    def smaller_of_two():
        (n1, d1), (n2, d2) = _pair()
        L = _lcm(d1, d2)
        small = (n1, d1) if Fraction(n1, d1) < Fraction(n2, d2) else (n2, d2)
        return _fracq("Which is smaller, %d/%d or %d/%d? Write the fraction."
                      % (n1, d1, n2, d2), small[0], small[1],
                      ["With denominator %d they are %d/%d and %d/%d."
                       % (L, n1 * (L // d1), L, n2 * (L // d2), L),
                       "%d/%d is smaller." % (small[0], small[1])])

    def sign_between():
        (n1, d1), (n2, d2) = _pair()
        sign = "<" if Fraction(n1, d1) < Fraction(n2, d2) else ">"
        L = _lcm(d1, d2)
        return _wordq("Type < or > to make this true:  %d/%d ___ %d/%d"
                      % (n1, d1, n2, d2), sign,
                      ["Use the common denominator %d: %d/%d and %d/%d."
                       % (L, n1 * (L // d1), L, n2 * (L // d2), L),
                       "So %d/%d %s %d/%d." % (n1, d1, sign, n2, d2)],
                      placeholder="< or >")

    def common_denominator():
        d1, d2 = random.sample(dens, 2)
        L = _lcm(d1, d2)
        return _numq("To compare fractions with denominators %d and %d, both "
                     "are rewritten with the same denominator. What is the "
                     "lowest common denominator?" % (d1, d2), L,
                     ["The lowest common denominator is the LCM of %d and %d."
                      % (d1, d2),
                      "The LCM of %d and %d is %d." % (d1, d2, L)])

    def converted_numerator():
        d1, d2 = random.sample(dens, 2)
        L = _lcm(d1, d2)
        a = random.randint(1, d1 - 1)
        return _numq("%d/%d is being compared with a fraction in %s, so it "
                     "is rewritten with denominator %d. What is its new "
                     "numerator?" % (a, d1, _plural_frac_word(d2), L),
                     a * (L // d1),
                     ["%d ÷ %d = %d." % (L, d1, L // d1),
                      "%d × %d = %d." % (a, L // d1, a * (L // d1))])

    def largest_of_three():
        fr = []
        while len(fr) < 3:
            dd = pick(dens)
            nn = random.randint(1, dd - 1)
            if all(Fraction(nn, dd) != Fraction(x, y) for x, y in fr):
                fr.append((nn, dd))
        best = max(fr, key=lambda p: Fraction(p[0], p[1]))
        return _fracq("Which of these is the largest?  %s.  Write the fraction."
                      % ", ".join("%d/%d" % f for f in fr), best[0], best[1],
                      ["Compare them using a common denominator.",
                       "The largest is %d/%d." % best])

    def smallest_of_three():
        fr = []
        while len(fr) < 3:
            dd = pick(dens)
            nn = random.randint(1, dd - 1)
            if all(Fraction(nn, dd) != Fraction(x, y) for x, y in fr):
                fr.append((nn, dd))
        best = min(fr, key=lambda p: Fraction(p[0], p[1]))
        return _fracq("Which of these is the smallest?  %s.  Write the "
                      "fraction." % ", ".join("%d/%d" % f for f in fr),
                      best[0], best[1],
                      ["Compare them using a common denominator.",
                       "The smallest is %d/%d." % best])

    def compare_to_half():
        dd = pick([5, 6, 7, 8, 9, 10, 12])
        nn = random.randint(1, dd - 1)
        while Fraction(nn, dd) == Fraction(1, 2):
            nn = random.randint(1, dd - 1)
        ans = "larger" if Fraction(nn, dd) > Fraction(1, 2) else "smaller"
        return _wordq("Is %d/%d larger or smaller than 1/2? Type larger or "
                      "smaller." % (nn, dd), ans,
                      ["Half of %d is %g." % (dd, dd / 2.0),
                       "%d is %s than half of %d, so %d/%d is %s than 1/2."
                       % (nn, "more" if ans == "larger" else "less", dd, nn,
                          dd, ans)], placeholder="larger or smaller")

    def improper_vs_mixed():
        dd = pick([3, 4, 5, 6, 8])
        w = random.randint(1, 3)
        p = random.randint(1, dd - 1)
        mixed = Fraction(w * dd + p, dd)
        imp_n = random.randint(dd + 1, 4 * dd)
        while Fraction(imp_n, dd) == mixed:
            imp_n += 1
        bigger_is_mixed = mixed > Fraction(imp_n, dd)
        ans = "A" if bigger_is_mixed else "B"
        return _wordq("Which is larger?  A: %s   B: %d/%d.  Type A or B."
                      % (_mixed_str(w, p, dd), imp_n, dd), ans,
                      ["%s = %d/%d." % (_mixed_str(w, p, dd), w * dd + p, dd),
                       "%d/%d is larger, so the answer is %s."
                       % (max(w * dd + p, imp_n), dd, ans)],
                      placeholder="A or B")

    def order_line():
        dd = pick([4, 5, 6, 8, 10])
        a, b = random.sample(range(1, dd), 2)
        want_larger = random.random() < 0.5
        k = max(a, b) if want_larger else min(a, b)
        word = "larger" if want_larger else "smaller"
        return _nlfrac("Compare %d/%d and %d/%d, then mark the %s fraction on "
                       "the number line." % (a, dd, b, dd, word), k, dd, 1,
                       ["The denominators match, so compare the numerators %d "
                        "and %d." % (a, b),
                        "The %s fraction is %d/%d." % (word, k, dd)])

    def order_line_greater_than_one():
        dd = pick([3, 4, 5, 6])
        n1 = random.randint(dd + 1, 2 * dd - 1)
        n2 = random.randint(dd + 1, 2 * dd - 1)
        while n2 == n1:
            n2 = random.randint(dd + 1, 2 * dd - 1)
        k = max(n1, n2)
        return _nlfrac("Both of these fractions are greater than 1. Mark the "
                       "larger of %d/%d and %d/%d on the number line."
                       % (n1, dd, n2, dd), k, dd, 2,
                       ["The denominators match, so compare the numerators.",
                        "%d/%d is larger, which is %s."
                        % (k, dd, _mixed_str(*_improper_to_mixed(k, dd)))])

    def shade_larger():
        dd = pick([4, 5, 6, 8, 10, 12])
        a, b = random.sample(range(1, dd), 2)
        which = "larger" if random.random() < 0.5 else "smaller"
        k = max(a, b) if which == "larger" else min(a, b)
        return _fbq("Shade this bar of %d equal parts to show the %s of %d/%d "
                    "and %d/%d." % (dd, which, a, dd, b, dd), dd, k,
                    ["Same denominator: compare the numerators %d and %d."
                     % (a, b),
                     "The %s fraction is %d/%d, so shade %s."
                     % (which, k, dd, _pl(k, "part"))])

    def word_who():
        p, q = _two_names()
        (n1, d1), (n2, d2) = _pair()
        winner = p if Fraction(n1, d1) > Fraction(n2, d2) else q
        return _wordq("%s read %d/%d of a book and %s read %d/%d of an "
                      "identical book. Who read more? Type the name."
                      % (p, n1, d1, q, n2, d2), winner,
                      ["Rewrite both fractions with the common denominator %d."
                       % _lcm(d1, d2),
                       "%s read the larger fraction." % winner],
                      placeholder="a name")

    def table_order():
        dd = pick([8, 10, 12])
        nums = random.sample(range(1, dd), 3)
        rows = [[pick(["Monday", "Tuesday", "Wednesday", "Thursday"]),
                 "%d/%d" % (x, dd)] for x in nums]
        seen = set()
        days = ["Monday", "Tuesday", "Wednesday"]
        rows = [[days[i], "%d/%d" % (nums[i], dd)] for i in range(3)]
        best = max(range(3), key=lambda i: nums[i])
        return _dtq("The table shows the fraction of a jigsaw finished on each "
                    "day. On which day was the largest fraction finished? Type "
                    "the day.", ["Day", "Fraction finished"], rows,
                    days[best],
                    ["All the fractions are %s, so compare the numerators %s."
                     % (_plural_frac_word(dd),
                        ", ".join(str(x) for x in nums)),
                     "The largest is %d/%d, on %s."
                     % (nums[best], dd, days[best])], answer_type="str",
                    placeholder="a day")

    opts = [larger_of_two, smaller_of_two, sign_between, largest_of_three,
            smallest_of_three, compare_to_half, order_line, shade_larger,
            word_who, table_order, common_denominator]
    if d == 0:
        opts = [larger_of_two, smaller_of_two, sign_between, order_line,
                shade_larger, table_order, compare_to_half]
    elif d == 2:
        opts = [larger_of_two, sign_between, largest_of_three,
                smallest_of_three, compare_to_half, improper_vs_mixed,
                order_line_greater_than_one, word_who, common_denominator,
                table_order, shade_larger]
    opts = opts + [order_line, shade_larger, order_line]
    return pick(opts)()


@skill("Y6.3.e", "Add and subtract fractions with the same denominator", S3)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [4, 5, 6, 8], [5, 6, 8, 9, 10, 12],
                     [7, 8, 9, 10, 12, 15, 20]))
    a = random.randint(1, den - 1)
    b = random.randint(1, den - 1)

    def add_bare():
        return _fracq("Work out %d/%d + %d/%d. Write the answer as a fraction."
                      % (a, den, b, den), a + b, den,
                      ["The denominators are the same, so add the numerators.",
                       "%d + %d = %d, so the answer is %d/%d."
                       % (a, b, a + b, a + b, den)])

    def sub_bare():
        hi, lo = max(a, b), min(a, b)
        if hi == lo:
            if hi < den - 1:
                hi += 1
            else:
                lo -= 1
        return _fracq("Work out %d/%d − %d/%d. Write the answer as a fraction."
                      % (hi, den, lo, den), hi - lo, den,
                      ["The denominators are the same, so subtract the "
                       "numerators.",
                       "%d − %d = %d, so the answer is %d/%d."
                       % (hi, lo, hi - lo, hi - lo, den)])

    def add_to_mixed():
        x = random.randint(den // 2 + 1, den - 1)
        y = random.randint(den - x + 1, den - 1) if den - x + 1 <= den - 1 \
            else den - 1
        tot = x + y
        w, rn, rd = _improper_to_mixed(tot, den)
        return _mixq("Work out %d/%d + %d/%d. The answer is greater than 1 — "
                     "write it as a mixed number, like  1 1/4 ."
                     % (x, den, y, den), w, rn, rd,
                     ["%d + %d = %d, so the total is %d/%d."
                      % (x, y, tot, tot, den),
                      "%d/%d = %s." % (tot, den, _mixed_str(w, rn, rd))])

    def missing_addend():
        tot = random.randint(2, den)
        x = random.randint(1, tot - 1)
        return _numq("Complete:  %d/%d + ___/%d = %d/%d" % (x, den, den, tot,
                                                            den), tot - x,
                     ["%d − %d = %d." % (tot, x, tot - x),
                      "%d/%d + %d/%d = %d/%d."
                      % (x, den, tot - x, den, tot, den)])

    def missing_subtrahend():
        tot = random.randint(2, den)
        x = random.randint(1, tot - 1)
        return _numq("Complete:  %d/%d − ___/%d = %d/%d" % (tot, den, den, x,
                                                            den), tot - x,
                     ["%d − %d = %d." % (tot, x, tot - x),
                      "%d/%d − %d/%d = %d/%d."
                      % (tot, den, tot - x, den, x, den)])

    def complete_the_whole():
        x = random.randint(1, den - 1)
        return _numq("What must be added to %d/%d to make 1 whole? Type the "
                     "numerator of the answer, which is ___/%d."
                     % (x, den, den), den - x,
                     ["One whole is %d/%d." % (den, den),
                      "%d − %d = %d, so %d/%d is needed."
                      % (den, x, den - x, den - x, den)])

    def three_fractions():
        x = random.randint(1, max(1, den - 3))
        y = random.randint(1, max(1, den - 2))
        z = random.randint(1, max(1, den - 2))
        return _fracq("Work out %d/%d + %d/%d + %d/%d. Write the answer as a "
                      "fraction." % (x, den, y, den, z, den), x + y + z, den,
                      ["Add the numerators: %d + %d + %d = %d."
                       % (x, y, z, x + y + z),
                       "The answer is %d/%d." % (x + y + z, den)])

    def shade_total():
        dd = min(den, 12)
        x = random.randint(1, dd - 2)
        y = random.randint(1, dd - x - 1)
        return _fbq("Shade this bar of %d equal parts to show %d/%d + %d/%d."
                    % (dd, x, dd, y, dd), dd, x + y,
                    ["%d + %d = %d parts." % (x, y, x + y),
                     "%d/%d + %d/%d = %d/%d." % (x, dd, y, dd, x + y, dd)])

    def shade_difference():
        dd = min(den, 12)
        x = random.randint(2, dd)
        y = random.randint(1, x - 1)
        return _agshade("This area model has %d equal parts. Shade it to show "
                        "%d/%d − %d/%d." % (dd, x, dd, y, dd), dd, x - y,
                        ["%d − %d = %s left." % (x, y, _pl(x - y, "part")),
                         "%d/%d − %d/%d = %d/%d."
                         % (x, dd, y, dd, x - y, dd)])

    def on_line_add():
        dd = min(den, 10)
        x = random.randint(1, dd - 2)
        y = random.randint(1, dd - x - 1)
        return _nlfrac("Start at %d/%d and count on %d/%d. Mark where you land "
                       "on the number line." % (x, dd, y, dd), x + y, dd, 1,
                       ["Counting on %d/%d means %s of 1/%d."
                        % (y, dd, _pl(y, "step"), dd),
                        "%d/%d + %d/%d = %d/%d."
                        % (x, dd, y, dd, x + y, dd)])

    def on_line_sub():
        dd = min(den, 10)
        x = random.randint(2, dd)
        y = random.randint(1, x - 1)
        return _nlfrac("Start at %d/%d and count back %d/%d. Mark where you "
                       "land on the number line." % (x, dd, y, dd), x - y, dd,
                       1,
                       ["Counting back %d/%d means %s of 1/%d."
                        % (y, dd, _pl(y, "step"), dd),
                        "%d/%d − %d/%d = %d/%d."
                        % (x, dd, y, dd, x - y, dd)])

    def word_pizza():
        who = pick(NAMES)
        x = random.randint(1, den - 2)
        y = random.randint(1, den - x - 1)
        return _fracq("%s eats %d/%d of a pizza for lunch and %d/%d of the "
                      "same pizza for tea. What fraction of the pizza has %s "
                      "eaten altogether?" % (who, x, den, y, den, who),
                      x + y, den,
                      ["%d/%d + %d/%d = %d/%d."
                       % (x, den, y, den, x + y, den)])

    def word_left():
        who = pick(NAMES)
        x = random.randint(2, den)
        y = random.randint(1, x - 1)
        return _fracq("%s has %d/%d of a bag of flour and uses %d/%d of a bag. "
                      "What fraction of a bag does %s have left?"
                      % (who, x, den, y, den, who), x - y, den,
                      ["%d/%d − %d/%d = %d/%d."
                       % (x, den, y, den, x - y, den)])

    def word_remaining_whole():
        who = pick(NAMES)
        x = random.randint(1, den - 2)
        y = random.randint(1, den - x - 1)
        left = den - x - y
        return _fracq("A wall is painted in one day. %s paints %d/%d of it in "
                      "the morning and %d/%d of it in the afternoon. What "
                      "fraction of the wall is still unpainted?"
                      % (who, x, den, y, den), left, den,
                      ["%d/%d + %d/%d = %d/%d painted."
                       % (x, den, y, den, x + y, den),
                       "%d/%d − %d/%d = %d/%d unpainted."
                       % (den, den, x + y, den, left, den)])

    opts = [add_bare, sub_bare, missing_addend, complete_the_whole,
            shade_total, shade_difference, on_line_add, on_line_sub,
            word_pizza, word_left]
    if d == 0:
        opts = [add_bare, sub_bare, missing_addend, complete_the_whole,
                shade_total, shade_difference, on_line_add, word_pizza]
    elif d == 2:
        opts = [add_bare, sub_bare, add_to_mixed, three_fractions,
                missing_addend, missing_subtrahend, word_left,
                word_remaining_whole, on_line_sub, shade_difference]
    opts = opts + [shade_total, on_line_add, shade_difference, on_line_sub]
    return pick(opts)()


@skill("Y6.3.f", "Add and subtract fractions with different denominators", S3)
def _(d=1):
    d = _t(d)

    def _dens():
        if d == 0:
            d1 = pick([2, 3, 4, 5])
            d2 = d1 * pick([2, 3])
            return d1, d2
        if d == 1:
            pairs = [(2, 4), (2, 6), (3, 6), (2, 8), (4, 8), (3, 9), (5, 10),
                     (2, 10), (3, 12), (4, 12), (6, 12), (2, 3), (3, 4),
                     (4, 5)]
            return pick(pairs)
        pairs = [(3, 4), (4, 5), (3, 5), (5, 6), (2, 7), (3, 8), (5, 8),
                 (4, 9), (6, 8), (5, 12), (7, 10), (6, 9)]
        return pick(pairs)

    def add_bare():
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        tot = n1 * (L // d1) + n2 * (L // d2)
        return _fracq("Work out %d/%d + %d/%d. Write the answer as a fraction."
                      % (n1, d1, n2, d2), tot, L,
                      ["The lowest common denominator is %d." % L,
                       "%d/%d = %d/%d and %d/%d = %d/%d."
                       % (n1, d1, n1 * (L // d1), L, n2, d2, n2 * (L // d2),
                          L),
                       "%d/%d + %d/%d = %d/%d."
                       % (n1 * (L // d1), L, n2 * (L // d2), L, tot, L)])

    def sub_bare():
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        for _ in range(30):
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            if Fraction(n1, d1) > Fraction(n2, d2):
                break
        else:
            n1, n2 = d1 - 1, 1
        diff = n1 * (L // d1) - n2 * (L // d2)
        if diff <= 0:
            return add_bare()
        return _fracq("Work out %d/%d − %d/%d. Write the answer as a fraction."
                      % (n1, d1, n2, d2), diff, L,
                      ["The lowest common denominator is %d." % L,
                       "%d/%d = %d/%d and %d/%d = %d/%d."
                       % (n1, d1, n1 * (L // d1), L, n2, d2, n2 * (L // d2),
                          L),
                       "%d/%d − %d/%d = %d/%d."
                       % (n1 * (L // d1), L, n2 * (L // d2), L, diff, L)])

    def common_denominator():
        d1, d2 = _dens()
        return _numq("To work out %d/%d + %d/%d, both fractions are rewritten "
                     "with the same denominator. What is the lowest common "
                     "denominator?" % (random.randint(1, d1 - 1), d1,
                                       random.randint(1, d2 - 1), d2),
                     _lcm(d1, d2),
                     ["The lowest common denominator is the LCM of %d and %d."
                      % (d1, d2),
                      "The LCM of %d and %d is %d." % (d1, d2, _lcm(d1, d2))])

    def convert_numerator():
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        return _numq("Rewriting %d/%d with a denominator of %d gives ___/%d. "
                     "Type the missing numerator." % (n1, d1, L, L),
                     n1 * (L // d1),
                     ["%d ÷ %d = %d." % (L, d1, L // d1),
                      "%d × %d = %d." % (n1, L // d1, n1 * (L // d1))])

    def missing_addend():
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        tot = n1 * (L // d1) + n2 * (L // d2)
        return _fracq("Complete:  %d/%d + ___ = %d/%d. Write the missing "
                      "fraction." % (n1, d1, tot, L), n2 * (L // d2), L,
                      ["%d/%d = %d/%d." % (n1, d1, n1 * (L // d1), L),
                       "%d/%d − %d/%d = %d/%d."
                       % (tot, L, n1 * (L // d1), L, n2 * (L // d2), L)])

    def from_one_whole():
        d1 = pick([3, 4, 5, 6, 8, 10, 12])
        d2 = pick([x for x in [2, 3, 4, 5, 6] if x != d1] or [2])
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        used = n1 * (L // d1) + n2 * (L // d2)
        if used >= L:
            return add_bare()
        return _fracq("%d/%d and %d/%d of a cake are eaten. What fraction of "
                      "the cake is left?" % (n1, d1, n2, d2), L - used, L,
                      ["%d/%d + %d/%d = %d/%d eaten."
                       % (n1, d1, n2, d2, used, L),
                       "1 − %d/%d = %d/%d left." % (used, L, L - used, L)])

    def shade_sum():
        d1, d2 = pick([(2, 4), (2, 6), (3, 6), (2, 8), (4, 8), (3, 12),
                       (4, 12), (6, 12), (2, 10), (5, 10)])
        L = _lcm(d1, d2)
        n1, n2 = 1, random.randint(1, max(1, d2 // 2))
        tot = n1 * (L // d1) + n2 * (L // d2)
        if tot >= L:
            n2 = 1
            tot = n1 * (L // d1) + n2 * (L // d2)
        return _fbq("This bar has %d equal parts. Shade it to show %d/%d + "
                    "%d/%d." % (L, n1, d1, n2, d2), L, tot,
                    ["%d/%d = %d/%d and %d/%d = %d/%d."
                     % (n1, d1, n1 * (L // d1), L, n2, d2, n2 * (L // d2), L),
                     "Shade %d of the %d parts." % (tot, L)])

    def shade_area_sum():
        d1, d2 = pick([(2, 6), (3, 6), (2, 8), (4, 8), (3, 12), (4, 12),
                       (6, 12), (2, 4), (5, 10)])
        L = _lcm(d1, d2)
        n1, n2 = 1, 1
        tot = L // d1 + L // d2
        return _agshade("This area model has %d equal parts. Shade it to show "
                        "1/%d + 1/%d." % (L, d1, d2), L, tot,
                        ["1/%d = %d/%d and 1/%d = %d/%d."
                         % (d1, L // d1, L, d2, L // d2, L),
                         "%d + %d = %d parts to shade."
                         % (L // d1, L // d2, tot)])

    def on_line_sum():
        d1, d2 = pick([(2, 4), (2, 6), (3, 6), (2, 8), (4, 8), (5, 10),
                       (2, 10), (3, 12), (4, 12), (6, 12)])
        L = _lcm(d1, d2)
        n1 = 1
        n2 = random.randint(1, max(1, d2 - L // d1 - 1)) if d2 > 2 else 1
        tot = L // d1 + n2 * (L // d2)
        if tot > L:
            return shade_sum()
        return _nlfrac("This number line is ruled in %s. Work out 1/%d + "
                       "%d/%d and mark the answer."
                       % (_plural_frac_word(L), d1, n2, d2), tot, L,
                       1,
                       ["1/%d = %d/%d and %d/%d = %d/%d."
                        % (d1, L // d1, L, n2, d2, n2 * (L // d2), L),
                        "The total is %d/%d." % (tot, L)])

    def word_two_jobs():
        who = pick(NAMES)
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        tot = n1 * (L // d1) + n2 * (L // d2)
        return _fracq("%s spends %d/%d of an hour reading and %d/%d of an hour "
                      "drawing. What fraction of an hour does %s spend on the "
                      "two activities altogether?"
                      % (who, n1, d1, n2, d2, who), tot, L,
                      ["The lowest common denominator is %d." % L,
                       "%d/%d + %d/%d = %d/%d."
                       % (n1 * (L // d1), L, n2 * (L // d2), L, tot, L)])

    def word_difference():
        p, q = _two_names()
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        for _ in range(30):
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            if Fraction(n1, d1) > Fraction(n2, d2):
                break
        else:
            n1, n2 = d1 - 1, 1
        diff = n1 * (L // d1) - n2 * (L // d2)
        if diff <= 0:
            return word_two_jobs()
        return _fracq("%s walks %d/%d of a mile and %s walks %d/%d of a mile. "
                      "How much further does %s walk than %s? Write the answer "
                      "as a fraction of a mile."
                      % (p, n1, d1, q, n2, d2, p, q), diff, L,
                      ["Both fractions become %s: %d/%d and %d/%d."
                       % (_plural_frac_word(L), n1 * (L // d1), L,
                          n2 * (L // d2), L),
                       "%d/%d − %d/%d = %d/%d."
                       % (n1 * (L // d1), L, n2 * (L // d2), L, diff, L)])

    def answer_denominator():
        d1, d2 = _dens()
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        tot = n1 * (L // d1) + n2 * (L // d2)
        while tot % L == 0:
            n2 = random.randint(1, d2 - 1)
            tot = n1 * (L // d1) + n2 * (L // d2)
        rn, rd = _simp(tot, L)
        return _numq("Work out %d/%d + %d/%d and write the answer in its "
                     "lowest terms. Type the denominator of that answer."
                     % (n1, d1, n2, d2), rd,
                     ["%d/%d + %d/%d = %d/%d." % (n1, d1, n2, d2, tot, L),
                      "In lowest terms that is %d/%d." % (rn, rd)])

    opts = [add_bare, add_bare, sub_bare, common_denominator,
            convert_numerator, shade_sum, shade_area_sum, on_line_sum,
            word_two_jobs, from_one_whole]
    if d == 0:
        opts = [add_bare, sub_bare, common_denominator, convert_numerator,
                shade_sum, shade_area_sum, on_line_sum]
    elif d == 2:
        opts = [add_bare, sub_bare, missing_addend, from_one_whole,
                word_two_jobs, word_difference, answer_denominator,
                common_denominator, shade_area_sum, on_line_sum]
    opts = opts + [shade_sum, shade_area_sum, on_line_sum]
    return pick(opts)()


@skill("Y6.3.g", "Add and subtract mixed numbers", S3)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [3, 4, 5], [4, 5, 6, 8], [5, 6, 8, 9, 10, 12]))
    w1 = random.randint(1, _by_d(d, 3, 5, 8))
    w2 = random.randint(1, _by_d(d, 3, 5, 8))
    p1 = random.randint(1, den - 1)
    p2 = random.randint(1, den - 1)
    for _ in range(30):
        if (p1 + p2) % den:
            break
        p1 = random.randint(1, den - 1)
        p2 = random.randint(1, den - 1)

    def add_whole_part():
        tot = (w1 * den + p1) + (w2 * den + p2)
        W, N, D = _improper_to_mixed(tot, den)
        return _numq("Work out %s + %s. Type the whole-number part of the "
                     "answer." % (_mixed_str(w1, p1, den),
                                  _mixed_str(w2, p2, den)), W,
                     ["Add the wholes: %d + %d = %d." % (w1, w2, w1 + w2),
                      "Add the fractions: %d/%d + %d/%d = %d/%d."
                      % (p1, den, p2, den, p1 + p2, den),
                      "The answer is %s, so the whole-number part is %d."
                      % (_mixed_str(W, N, D), W)])

    def add_full():
        tot = (w1 * den + p1) + (w2 * den + p2)
        W, N, D = _improper_to_mixed(tot, den)
        return _mixq("Work out %s + %s. Write the answer as a mixed number, "
                     "like  3 1/4 ." % (_mixed_str(w1, p1, den),
                                        _mixed_str(w2, p2, den)), W, N, D,
                     ["%d + %d = %d wholes." % (w1, w2, w1 + w2),
                      "%d/%d + %d/%d = %d/%d."
                      % (p1, den, p2, den, p1 + p2, den),
                      "Altogether that is %s." % _mixed_str(W, N, D)])

    def add_improper():
        tot = (w1 * den + p1) + (w2 * den + p2)
        return _fracq("Work out %s + %s. Write the answer as an improper "
                      "fraction." % (_mixed_str(w1, p1, den),
                                     _mixed_str(w2, p2, den)), tot, den,
                      ["%s = %d/%d and %s = %d/%d."
                       % (_mixed_str(w1, p1, den), w1 * den + p1, den,
                          _mixed_str(w2, p2, den), w2 * den + p2, den),
                       "%d/%d + %d/%d = %d/%d."
                       % (w1 * den + p1, den, w2 * den + p2, den, tot, den)])

    def sub_full():
        A = max(w1 * den + p1, w2 * den + p2)
        B = min(w1 * den + p1, w2 * den + p2)
        if A - B < den or (A - B) % den == 0:
            A = B + den * random.randint(1, 2) + random.randint(1, den - 1)
        diff = A - B
        W, N, D = _improper_to_mixed(diff, den)
        aw, an, ad = _improper_to_mixed(A, den)
        bw, bn, bd = _improper_to_mixed(B, den)
        return _mixq("Work out %s − %s. Write the answer as a mixed number, "
                     "like  1 1/4 ." % (_mixed_str(aw, an, ad),
                                        _mixed_str(bw, bn, bd)), W, N, D,
                     ["%s = %d/%d and %s = %d/%d."
                      % (_mixed_str(aw, an, ad), A, den,
                         _mixed_str(bw, bn, bd), B, den),
                      "%d/%d − %d/%d = %d/%d, which is %s."
                      % (A, den, B, den, diff, den, _mixed_str(W, N, D))])

    def sub_whole_part():
        A = max(w1 * den + p1, w2 * den + p2)
        B = min(w1 * den + p1, w2 * den + p2)
        if A - B < den:
            A = B + den + random.randint(1, den - 1)
        diff = A - B
        W, N, D = _improper_to_mixed(diff, den)
        aw, an, ad = _improper_to_mixed(A, den)
        bw, bn, bd = _improper_to_mixed(B, den)
        return _numq("Work out %s − %s. Type the whole-number part of the "
                     "answer." % (_mixed_str(aw, an, ad),
                                  _mixed_str(bw, bn, bd)), W,
                     ["%d/%d − %d/%d = %d/%d." % (A, den, B, den, diff, den),
                      "%d/%d = %s, so the whole-number part is %d."
                      % (diff, den, _mixed_str(W, N, D), W)])

    def sub_fraction_part():
        A = max(w1 * den + p1, w2 * den + p2)
        B = min(w1 * den + p1, w2 * den + p2)
        if A - B <= 1 or (A - B) % den == 0:
            A = B + den + 1
        diff = A - B
        W, N, D = _improper_to_mixed(diff, den)
        aw, an, ad = _improper_to_mixed(A, den)
        bw, bn, bd = _improper_to_mixed(B, den)
        return _numq("Work out %s − %s. Type the numerator of the fraction "
                     "part of the answer, which has denominator %d."
                     % (_mixed_str(aw, an, ad), _mixed_str(bw, bn, bd), D),
                     N,
                     ["%d/%d − %d/%d = %d/%d." % (A, den, B, den, diff, den),
                      "That is %s, so the numerator is %d."
                      % (_mixed_str(W, N, D), N)])

    def add_whole_to_mixed():
        k = random.randint(2, 9)
        return _mixq("Work out %s + %d. Write the answer as a mixed number."
                     % (_mixed_str(w1, p1, den), k), w1 + k, p1, den,
                     ["Only the whole-number part changes: %d + %d = %d."
                      % (w1, k, w1 + k),
                      "The answer is %s." % _mixed_str(w1 + k, p1, den)])

    def missing_part():
        A = w1 * den + p1
        B = A + random.randint(1, 3) * den + random.randint(1, den - 1)
        diff = B - A
        aw, an, ad = _improper_to_mixed(A, den)
        bw, bn, bd = _improper_to_mixed(B, den)
        W, N, D = _improper_to_mixed(diff, den)
        return _mixq("Complete:  %s + ___ = %s. Write the missing amount as a "
                     "mixed number or a fraction."
                     % (_mixed_str(aw, an, ad), _mixed_str(bw, bn, bd)),
                     W, N, D,
                     ["%d/%d − %d/%d = %d/%d." % (B, den, A, den, diff, den),
                      "That is %s." % _mixed_str(W, N, D)])

    def on_line():
        dd = min(den, 8)
        ww = random.randint(0, 2)
        pp = random.randint(1, dd - 1)
        add = random.randint(1, dd - 1)
        tot = ww * dd + pp + add
        hi = 3
        if tot > hi * dd:
            return add_full()
        W, N, D = _improper_to_mixed(tot, dd)
        return _nlfrac("Start at %s on the number line and count on %d/%d. "
                       "Mark where you land."
                       % (_mixed_str(ww, pp, dd), add, dd), tot, dd, hi,
                       ["%s = %d/%d." % (_mixed_str(ww, pp, dd),
                                         ww * dd + pp, dd),
                        "%d/%d + %d/%d = %d/%d, which is %s."
                        % (ww * dd + pp, dd, add, dd, tot, dd,
                           _mixed_str(W, N, D))])

    def word_ribbon():
        who = pick(NAMES)
        tot = (w1 * den + p1) + (w2 * den + p2)
        W, N, D = _improper_to_mixed(tot, den)
        return _mixq("%s joins a ribbon %s metres long to a ribbon %s metres "
                     "long. How long is the joined ribbon, in metres? Write "
                     "the answer as a mixed number."
                     % (who, _mixed_str(w1, p1, den),
                        _mixed_str(w2, p2, den)), W, N, D,
                     ["%d/%d + %d/%d = %d/%d."
                      % (w1 * den + p1, den, w2 * den + p2, den, tot, den),
                      "That is %s metres." % _mixed_str(W, N, D)])

    def word_juice():
        who = pick(NAMES)
        A = max(w1 * den + p1, w2 * den + p2)
        B = min(w1 * den + p1, w2 * den + p2)
        if A == B or (A - B) % den == 0:
            A = B + 1
        diff = A - B
        W, N, D = _improper_to_mixed(diff, den)
        aw, an, ad = _improper_to_mixed(A, den)
        bw, bn, bd = _improper_to_mixed(B, den)
        return _mixq("A jug holds %s litres of juice. %s pours out %s litres. "
                     "How many litres are left in the jug? Write the answer as "
                     "a mixed number or a fraction."
                     % (_mixed_str(aw, an, ad), who,
                        _mixed_str(bw, bn, bd)), W, N, D,
                     ["%d/%d − %d/%d = %d/%d." % (A, den, B, den, diff, den),
                      "That is %s litres." % _mixed_str(W, N, D)])

    def word_total_whole():
        who = pick(NAMES)
        tot = (w1 * den + p1) + (w2 * den + p2)
        W, N, D = _improper_to_mixed(tot, den)
        return _numq("%s bakes for %s hours on Saturday and %s hours on "
                     "Sunday. How many complete hours does %s bake over the "
                     "two days?" % (who, _mixed_str(w1, p1, den),
                                    _mixed_str(w2, p2, den), who), W,
                     ["The total is %d/%d hours." % (tot, den),
                      "%d/%d = %s hours, so %d complete hours."
                      % (tot, den, _mixed_str(W, N, D), W)], unit="hours")

    opts = [add_full, add_whole_part, add_improper, sub_full, sub_whole_part,
            add_whole_to_mixed, on_line, word_ribbon, word_juice]
    if d == 0:
        opts = [add_whole_part, add_full, add_whole_to_mixed, on_line,
                word_ribbon, add_improper, sub_whole_part]
    elif d == 2:
        opts = [add_full, add_improper, sub_full, sub_fraction_part,
                missing_part, word_juice, word_ribbon, word_total_whole,
                on_line]
    opts = opts + [on_line, on_line]
    return pick(opts)()


@skill("Y6.3.h", "Fraction addition and subtraction problems", S3)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [4, 5, 6, 8], [5, 6, 8, 10, 12], [6, 8, 9, 10, 12]))

    def two_step_same():
        who = pick(NAMES)
        a = random.randint(1, den - 3)
        b = random.randint(1, den - a - 2)
        c = random.randint(1, den - a - b - 1)
        left = den - a - b - c
        return _fracq("A jar of jam is used over three days. %s uses %d/%d of "
                      "it on Monday, %d/%d on Tuesday and %d/%d on Wednesday. "
                      "What fraction of the jar is left?"
                      % (who, a, den, b, den, c, den), left, den,
                      ["%d/%d + %d/%d + %d/%d = %d/%d used."
                       % (a, den, b, den, c, den, a + b + c, den),
                       "%d/%d − %d/%d = %d/%d left."
                       % (den, den, a + b + c, den, left, den)])

    def two_step_different():
        d1, d2 = pick([(2, 4), (2, 6), (3, 6), (4, 8), (2, 8), (3, 12),
                       (4, 12), (5, 10), (2, 3), (3, 4)])
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        used = n1 * (L // d1) + n2 * (L // d2)
        if used >= L:
            return two_step_same()
        return _fracq("A tank of water is emptied in two goes: %d/%d of the "
                      "tank, then %d/%d of the tank. What fraction of the tank "
                      "is still full?" % (n1, d1, n2, d2), L - used, L,
                      ["%d/%d + %d/%d = %d/%d used."
                       % (n1, d1, n2, d2, used, L),
                       "1 − %d/%d = %d/%d still full."
                       % (used, L, L - used, L)])

    def strip_problem():
        who = pick(NAMES)
        parts = min(den, 8)
        each = random.randint(4, 30)
        total = parts * each
        return _stripq("Use the strip model. A ribbon %d cm long is cut into "
                       "%d equal parts. %s uses one part. How many centimetres "
                       "does %s use?" % (total, parts, who, who), parts, "?",
                       "%d cm" % total, "part", each,
                       ["Each part is 1/%d of %d cm." % (parts, total),
                        "%d ÷ %d = %d cm." % (total, parts, each)])

    def bar_chart_problem():
        cats = ["Reading", "Sport", "Music"]
        vals = random.sample(range(3, 10), 3)
        i = pick([x for x in range(3) if vals[x] != max(vals)])
        return _barq("The chart shows how many hours a class spent on each "
                     "activity last week. How many more hours were spent on "
                     "the largest activity than on %s?" % cats[i].lower(),
                     cats, vals, max(vals) - vals[i],
                     ["The largest bar is %d hours." % max(vals),
                      "%d − %d = %s." % (max(vals), vals[i],
                                          _pl(max(vals) - vals[i], "hour"))])

    def data_table_problem():
        rows = []
        names = random.sample(NAMES, 3)
        nums = random.sample(range(1, den), 3)
        for i in range(3):
            rows.append([names[i], "%d/%d" % (nums[i], den)])
        i, j = random.sample(range(3), 2)
        hi, lo = max(nums[i], nums[j]), min(nums[i], nums[j])
        who_hi = names[nums.index(hi)]
        who_lo = names[nums.index(lo)]
        return _dtq("The table shows the fraction of a book each person has "
                    "read. How much more of the book has %s read than %s? Type "
                    "the numerator of the answer, which is a number of %s."
                    % (who_hi, who_lo, _plural_frac_word(den)),
                    ["Name", "Fraction read"], rows, hi - lo,
                    ["%d/%d − %d/%d = %d/%d."
                     % (hi, den, lo, den, hi - lo, den),
                     "So the numerator is %d." % (hi - lo)],
                    placeholder="the numerator")

    def missing_start():
        who = pick(NAMES)
        d1, d2 = pick([(2, 4), (3, 6), (4, 8), (2, 6), (5, 10), (3, 12),
                       (2, 3), (3, 4)])
        L = _lcm(d1, d2)
        used = random.randint(1, d1 - 1) * (L // d1)
        left = random.randint(1, d2 - 1) * (L // d2)
        if used + left > L:
            return two_step_same()
        return _fracq("%s used %d/%d of a bag of rice and has %d/%d of the bag "
                      "left. What fraction of the bag did %s start with?"
                      % (who, used, L, left, L, who), used + left, L,
                      ["%d/%d + %d/%d = %d/%d."
                       % (used, L, left, L, used + left, L)])

    def compare_then_add():
        d1, d2 = pick([(3, 4), (2, 5), (4, 5), (3, 8), (5, 6), (2, 3)])
        L = _lcm(d1, d2)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        tot = n1 * (L // d1) + n2 * (L // d2)
        while tot >= L:
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            tot = n1 * (L // d1) + n2 * (L // d2)
        return _numq("%d/%d of a class walk to school and %d/%d cycle. "
                     "Together these fractions are written over the same "
                     "denominator %d. What is the numerator of the total?"
                     % (n1, d1, n2, d2, L), tot,
                     ["%d/%d = %d/%d and %d/%d = %d/%d."
                      % (n1, d1, n1 * (L // d1), L, n2, d2, n2 * (L // d2),
                         L),
                      "%d + %d = %d." % (n1 * (L // d1), n2 * (L // d2),
                                         tot)])

    def shade_problem():
        parts = max(6, min(den, 12))
        a = random.randint(2, parts - 4)
        b = random.randint(2, parts - a - 1)
        return _agshade("A garden is split into %d equal beds. %s hold "
                        "carrots and %s hold beans. Shade the area model "
                        "to show the fraction of the garden used for carrots "
                        "and beans altogether."
                        % (parts, _pl(a, "bed"), _pl(b, "bed")), parts, a + b,
                        ["%d/%d + %d/%d = %d/%d."
                         % (a, parts, b, parts, a + b, parts),
                         "Shade %d of the %d parts." % (a + b, parts)])

    def line_problem():
        dd = min(den, 10)
        a = random.randint(1, dd - 2)
        b = random.randint(1, dd - a - 1)
        who = pick(NAMES)
        return _nlfrac("%s walks %d/%d of a mile, rests, then walks another "
                       "%d/%d of a mile. Mark the total distance on the number "
                       "line, where 1 stands for one mile."
                       % (who, a, dd, b, dd), a + b, dd, 1,
                       ["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, a + b, dd),
                        "Mark %d steps of 1/%d from 0." % (a + b, dd)])

    def mixed_number_problem():
        dd = pick([4, 5, 6, 8])
        w1 = random.randint(1, 4)
        p1 = random.randint(1, dd - 1)
        w2 = random.randint(1, 4)
        p2 = random.randint(1, dd - 1)
        while (p1 + p2) % dd == 0:
            p2 = random.randint(1, dd - 1)
        tot = (w1 * dd + p1) + (w2 * dd + p2)
        W, N, D = _improper_to_mixed(tot, dd)
        who = pick(NAMES)
        return _mixq("%s runs %s km on Saturday and %s km on Sunday. How far "
                     "does %s run in total, in km? Write the answer as a mixed "
                     "number." % (who, _mixed_str(w1, p1, dd),
                                  _mixed_str(w2, p2, dd), who), W, N, D,
                     ["%d/%d + %d/%d = %d/%d."
                      % (w1 * dd + p1, dd, w2 * dd + p2, dd, tot, dd),
                      "That is %s km." % _mixed_str(W, N, D)])

    def money_fraction():
        d1 = pick([2, 4, 5, 10])
        tot = random.randint(2, 12) * d1 * 10
        n1 = random.randint(1, d1 - 1)
        spent = tot * n1 // d1
        return _numq("%s of a savings pot is spent, which is %d/%d of the "
                     "money. The pot held %s. How much is spent, in pence?"
                     % (_frac_words(n1, d1).capitalize(), n1, d1, money(tot)),
                     spent,
                     ["%dp ÷ %d = %dp is one %s."
                      % (tot, d1, tot // d1, _FRAC_WORDS.get(d1, "part")),
                      "%d × %d = %dp." % (tot // d1, n1, spent)], unit="p")

    opts = [two_step_same, two_step_different, strip_problem,
            data_table_problem, shade_problem, line_problem, missing_start,
            bar_chart_problem, mixed_number_problem]
    if d == 0:
        opts = [two_step_same, strip_problem, shade_problem, line_problem,
                bar_chart_problem, data_table_problem]
    elif d == 2:
        opts = [two_step_different, missing_start, compare_then_add,
                mixed_number_problem, money_fraction, data_table_problem,
                strip_problem, shade_problem, line_problem]
    opts = opts + [shade_problem, line_problem, strip_problem]
    return pick(opts)()


# ================================================================== 6.4 ======
@skill("Y6.4.a", "Multiply a fraction by a whole number", S4)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [3, 4, 5, 6], [4, 5, 6, 8, 10], [5, 6, 7, 8, 9, 12]))
    num = random.randint(1, den - 1)
    k = _by_d(d, random.randint(2, 3), random.randint(2, 6),
              random.randint(3, 9))

    def bare():
        return _fracq("Work out %d/%d × %d. Write the answer as a fraction."
                      % (num, den, k), num * k, den,
                      ["Multiply the numerator by %d and keep the denominator."
                       % k,
                       "%d × %d = %d, so the answer is %d/%d."
                       % (num, k, num * k, num * k, den)])

    def bare_reversed():
        return _fracq("Work out %d × %d/%d. Write the answer as a fraction."
                      % (k, num, den), num * k, den,
                      ["%d × %d/%d means %d lots of %d/%d."
                       % (k, num, den, k, num, den),
                       "%d × %d = %d, so the answer is %d/%d."
                       % (k, num, num * k, num * k, den)])

    def as_mixed():
        tot = num * k
        W, N, D = _improper_to_mixed(tot, den)
        if tot < den or tot % den == 0:
            return bare()
        return _mixq("Work out %d/%d × %d. Write the answer as a mixed number, "
                     "like  2 1/4 ." % (num, den, k), W, N, D,
                     ["%d × %d = %d, so the answer is %d/%d."
                      % (num, k, tot, tot, den),
                      "%d/%d = %s." % (tot, den, _mixed_str(W, N, D))])

    def repeated_addition():
        m = min(k, 4)
        chain = " + ".join(["%d/%d" % (num, den)] * m)
        return _fracq("Work out %s. Write the answer as a fraction." % chain,
                      num * m, den,
                      ["This is %d/%d × %d." % (num, den, m),
                       "%d × %d = %d, so the answer is %d/%d."
                       % (num, m, num * m, num * m, den)])

    def numerator_only():
        return _numq("%d/%d × %d = ___/%d . Type the missing numerator."
                     % (num, den, k, den), num * k,
                     ["Multiplying by %d multiplies the numerator by %d." % (k,
                                                                             k),
                      "%d × %d = %d." % (num, k, num * k)])

    def missing_multiplier():
        return _numq("Complete:  %d/%d × ___ = %d/%d" % (num, den, num * k,
                                                         den), k,
                     ["%d ÷ %d = %d." % (num * k, num, k),
                      "%d/%d × %d = %d/%d." % (num, den, k, num * k, den)])

    def whole_number_answer():
        dd = pick([2, 3, 4, 5, 6])
        nn = random.randint(1, dd - 1)
        m = dd * random.randint(1, 4)
        return _numq("Work out %d/%d × %d. The answer is a whole number — type "
                     "it." % (nn, dd, m), nn * m // dd,
                     ["%d/%d × %d = %d/%d." % (nn, dd, m, nn * m, dd),
                      "%d ÷ %d = %d." % (nn * m, dd, nn * m // dd)])

    def shade_bar():
        dd = min(den, 12)
        nn = 1
        m = random.randint(2, max(2, dd - 1))
        return _fbq("This bar has %d equal parts. Shade it to show 1/%d × %d."
                    % (dd, dd, m), dd, m,
                    ["1/%d × %d means %d lots of 1/%d." % (dd, m, m, dd),
                     "That is %d/%d, so shade %s." % (m, dd, _pl(m, "part"))])

    def shade_area():
        dd = min(den, 12)
        nn = random.randint(1, max(1, dd // 3))
        m = random.randint(2, max(2, dd // max(1, nn)))
        if nn * m > dd:
            m = max(2, dd // nn)
        return _agshade("This area model has %d equal parts. Shade it to show "
                        "%d/%d × %d." % (dd, nn, dd, m), dd, min(nn * m, dd),
                        ["%d/%d × %d = %d/%d." % (nn, dd, m, nn * m, dd),
                         "Shade %d of the %d parts." % (min(nn * m, dd), dd)])

    def on_line():
        dd = pick([4, 5, 6, 8, 10])
        m = random.randint(2, 4)
        nn = 1
        tot = m
        hi = 1 if tot <= dd else 2
        if tot > hi * dd:
            return bare()
        return _nlfrac("Work out 1/%d × %d and mark the answer on the number "
                       "line." % (dd, m), tot, dd, hi,
                       ["1/%d × %d = %d/%d." % (dd, m, m, dd),
                        "Count %d steps of 1/%d from 0." % (m, dd)])

    def word_glasses():
        who = pick(NAMES)
        dd = pick([2, 3, 4, 5])
        m = random.randint(3, 9)
        while m % dd == 0:
            m = random.randint(3, 9)
        tot = m
        W, N, D = _improper_to_mixed(tot, dd)
        return _mixq("%s fills %d glasses, each holding 1/%d of a litre. How "
                     "many litres does %s pour altogether? Write the answer as "
                     "a mixed number or a fraction." % (who, m, dd, who),
                     W, N, D,
                     ["1/%d × %d = %d/%d litres." % (dd, m, m, dd),
                      "%d/%d = %s litres." % (m, dd, _mixed_str(W, N, D))])

    def word_recipe():
        who = pick(NAMES)
        m = random.randint(2, 6)
        return _fracq("One cake needs %d/%d of a bag of sugar. %s bakes %d "
                      "cakes. What fraction of a bag of sugar does %s need "
                      "altogether? Write the answer as a fraction."
                      % (num, den, who, m, who), num * m, den,
                      ["%d/%d × %d = %d/%d." % (num, den, m, num * m, den)])

    def table_scaling():
        rows = [[str(i), "%d/%d" % (num * i, den)] for i in range(1, 5)]
        j = random.randrange(4)
        ans = num * (j + 1)
        rows[j][1] = ""
        return _dtq("Each portion of a recipe uses %d/%d of a litre of milk. "
                    "Complete the table: type the numerator of the amount "
                    "needed for %s, over the denominator %d."
                    % (num, den, _pl(j + 1, "portion"), den), ["Portions", "Litres of milk"],
                    rows, ans,
                    ["%d/%d × %d = %d/%d." % (num, den, j + 1, ans, den),
                     "The numerator is %d." % ans], missing=(j, 1),
                    placeholder="the numerator")

    def word_length():
        m = random.randint(3, 8)
        dd = pick([2, 4, 5, 10])
        nn = random.randint(1, dd - 1)
        while (nn * m) % dd == 0:
            nn = random.randint(1, dd - 1)
            m = random.randint(3, 8)
        tot = nn * m
        W, N, D = _improper_to_mixed(tot, dd)
        return _mixq("A plank is %d/%d of a metre long. How long are %d of "
                     "these planks laid end to end, in metres? Write the "
                     "answer as a mixed number or a fraction."
                     % (nn, dd, m), W, N, D,
                     ["%d/%d × %d = %d/%d metres." % (nn, dd, m, tot, dd),
                      "%d/%d = %s metres." % (tot, dd, _mixed_str(W, N, D))])

    opts = [bare, bare_reversed, repeated_addition, numerator_only, as_mixed,
            shade_bar, shade_area, on_line, word_recipe, table_scaling]
    if d == 0:
        opts = [bare, bare_reversed, repeated_addition, numerator_only,
                shade_bar, shade_area, on_line, table_scaling]
    elif d == 2:
        opts = [bare, as_mixed, missing_multiplier, whole_number_answer,
                word_glasses, word_length, word_recipe, table_scaling,
                shade_area, on_line]
    opts = opts + [shade_bar, shade_area, on_line, table_scaling]
    return pick(opts)()


@skill("Y6.4.b", "Multiply pairs of fractions", S4)
def _(d=1):
    d = _t(d)
    if d == 0:
        d1, d2 = pick([(2, 2), (2, 3), (3, 2), (2, 4), (3, 3), (4, 2)])
    elif d == 1:
        d1, d2 = pick([(2, 3), (3, 4), (2, 5), (3, 5), (4, 3), (5, 2),
                       (4, 4), (2, 6), (6, 2)])
    else:
        d1, d2 = pick([(3, 5), (4, 5), (5, 6), (3, 8), (4, 7), (5, 8),
                       (6, 5), (7, 3), (8, 3), (9, 2)])
    n1 = random.randint(1, d1 - 1) if d1 > 1 else 1
    n2 = random.randint(1, d2 - 1) if d2 > 1 else 1
    pn, pd = n1 * n2, d1 * d2

    def bare():
        return _fracq("Work out %d/%d × %d/%d. Write the answer as a fraction."
                      % (n1, d1, n2, d2), pn, pd,
                      ["Multiply the numerators: %d × %d = %d."
                       % (n1, n2, pn),
                       "Multiply the denominators: %d × %d = %d."
                       % (d1, d2, pd),
                       "The answer is %d/%d." % (pn, pd)])

    def of_language():
        return _fracq("What is %d/%d of %d/%d? Write the answer as a fraction."
                      % (n1, d1, n2, d2), pn, pd,
                      ["'of' means multiply: %d/%d × %d/%d."
                       % (n1, d1, n2, d2),
                       "%d × %d = %d and %d × %d = %d, so the answer is %d/%d."
                       % (n1, n2, pn, d1, d2, pd, pn, pd)])

    def numerator_only():
        return _numq("%d/%d × %d/%d = ___/%d . Type the missing numerator."
                     % (n1, d1, n2, d2, pd), pn,
                     ["Multiply the numerators together.",
                      "%d × %d = %d." % (n1, n2, pn)])

    def denominator_only():
        return _numq("%d/%d × %d/%d = %d/___ . Type the missing denominator."
                     % (n1, d1, n2, d2, pn), pd,
                     ["Multiply the denominators together.",
                      "%d × %d = %d." % (d1, d2, pd)])

    def lowest_terms_denominator():
        rn, rd = _simp(pn, pd)
        return _numq("Work out %d/%d × %d/%d and write the answer in its "
                     "lowest terms. Type the denominator of that answer."
                     % (n1, d1, n2, d2), rd,
                     ["%d/%d × %d/%d = %d/%d." % (n1, d1, n2, d2, pn, pd),
                      "In its lowest terms that is %d/%d." % (rn, rd)])

    def area_model():
        if pd > 12:
            return bare()
        return _agshade("This area model has %d equal parts, made by splitting "
                        "a whole into %d parts one way and %d parts the other. "
                        "Shade it to show %d/%d × %d/%d."
                        % (pd, d1, d2, n1, d1, n2, d2), pd, pn,
                        ["%d/%d × %d/%d = %d/%d."
                         % (n1, d1, n2, d2, pn, pd),
                         "Shade %d of the %d equal parts." % (pn, pd)])

    def bar_model():
        if pd > 12:
            return bare()
        return _fbq("This bar has %d equal parts, which is %d × %d. Shade it "
                    "to show %d/%d of %d/%d." % (pd, d1, d2, n1, d1, n2, d2),
                    pd, pn,
                    ["%d/%d of %d/%d = %d/%d." % (n1, d1, n2, d2, pn, pd),
                     "Shade %s." % _pl(pn, "part")])

    def read_area():
        if pd > 12:
            return bare()
        return _agread("This area model has %d equal parts. The shading was "
                       "made by taking %d/%d of %d/%d. Write the shaded "
                       "fraction." % (pd, n1, d1, n2, d2), pd, pn,
                       ["%d/%d × %d/%d = %d/%d." % (n1, d1, n2, d2, pn, pd),
                        "The shaded fraction is %d/%d." % (pn, pd)],
                       placeholder="e.g. 3/8")

    def word_cake():
        who = pick(NAMES)
        return _fracq("%s has %d/%d of a cake left and gives %d/%d of what is "
                      "left to a friend. What fraction of the whole cake does "
                      "%s give away?" % (who, n2, d2, n1, d1, who), pn, pd,
                      ["%d/%d of %d/%d = %d/%d × %d/%d."
                       % (n1, d1, n2, d2, n1, d1, n2, d2),
                       "That is %d/%d of the whole cake." % (pn, pd)])

    def word_garden():
        return _fracq("%d/%d of a garden is lawn. %d/%d of the lawn is in the "
                      "shade. What fraction of the whole garden is shaded "
                      "lawn?" % (n2, d2, n1, d1), pn, pd,
                      ["%d/%d × %d/%d = %d/%d."
                       % (n1, d1, n2, d2, pn, pd)])

    def three_fractions():
        d3 = pick([2, 3, 4])
        n3 = random.randint(1, d3 - 1) if d3 > 1 else 1
        return _fracq("Work out %d/%d × %d/%d × %d/%d. Write the answer as a "
                      "fraction." % (n1, d1, n2, d2, n3, d3), pn * n3,
                      pd * d3,
                      ["Multiply all the numerators: %d × %d × %d = %d."
                       % (n1, n2, n3, pn * n3),
                       "Multiply all the denominators: %d × %d × %d = %d."
                       % (d1, d2, d3, pd * d3)])

    def square_of_fraction():
        dd = pick([2, 3, 4, 5, 6])
        nn = random.randint(1, dd - 1)
        return _fracq("Work out %d/%d × %d/%d. Write the answer as a fraction."
                      % (nn, dd, nn, dd), nn * nn, dd * dd,
                      ["%d × %d = %d and %d × %d = %d."
                       % (nn, nn, nn * nn, dd, dd, dd * dd),
                       "The answer is %d/%d." % (nn * nn, dd * dd)])

    def mixed_times_fraction():
        dd = pick([2, 3, 4])
        w = random.randint(1, 3)
        p = random.randint(1, dd - 1)
        imp = w * dd + p
        d3 = pick([2, 3, 4, 5])
        n3 = random.randint(1, d3 - 1)
        return _fracq("Work out %s × %d/%d. Change the mixed number to an "
                      "improper fraction first. Write the answer as a "
                      "fraction." % (_mixed_str(w, p, dd), n3, d3),
                      imp * n3, dd * d3,
                      ["%s = %d/%d." % (_mixed_str(w, p, dd), imp, dd),
                       "%d/%d × %d/%d = %d/%d."
                       % (imp, dd, n3, d3, imp * n3, dd * d3)])

    def missing_fraction():
        return _fracq("Complete:  %d/%d × ___ = %d/%d. Write the missing "
                      "fraction." % (n1, d1, pn, pd), n2, d2,
                      ["%d ÷ %d = %d and %d ÷ %d = %d."
                       % (pn, n1, n2, pd, d1, d2),
                       "The missing fraction is %d/%d." % (n2, d2)])

    opts = [bare, bare, of_language, numerator_only, denominator_only,
            area_model, bar_model, read_area, word_cake, word_garden]
    if d == 0:
        opts = [bare, of_language, numerator_only, denominator_only,
                area_model, bar_model, read_area, square_of_fraction]
    elif d == 2:
        opts = [bare, of_language, lowest_terms_denominator, three_fractions,
                mixed_times_fraction, missing_fraction, word_cake,
                word_garden, area_model, read_area]
    opts = opts + [area_model, bar_model, read_area]
    return pick(opts)()


@skill("Y6.4.c", "Find a fraction of a quantity", S4)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [2, 3, 4, 5], [3, 4, 5, 6, 8, 10],
                     [5, 6, 7, 8, 9, 10, 12]))
    num = random.randint(1, den - 1)
    per = _by_d(d, random.randint(2, 9), random.randint(3, 20),
                random.randint(6, 40))
    total = den * per

    def bare():
        return _numq("What is %d/%d of %d?" % (num, den, total), num * per,
                     ["%d ÷ %d = %d, which is one %s."
                      % (total, den, per, _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %d." % (per, num, num * per)])

    def unit_fraction():
        return _numq("What is 1/%d of %d?" % (den, total), per,
                     ["Dividing by %d gives one %s."
                      % (den, _FRAC_WORDS.get(den, "part")),
                      "%d ÷ %d = %d." % (total, den, per)])

    def money_of():
        pence = den * random.randint(3, 40) * 5
        return _numq("What is %d/%d of %s? Give your answer in pence."
                     % (num, den, money(pence)), pence // den * num,
                     ["%dp ÷ %d = %dp." % (pence, den, pence // den),
                      "%dp × %d = %dp." % (pence // den, num,
                                           pence // den * num)], unit="p")

    def mass_of():
        grams = den * random.randint(5, 60) * 5
        return _numq("What is %d/%d of %d g?" % (num, den, grams),
                     grams // den * num,
                     ["%d ÷ %d = %d g." % (grams, den, grams // den),
                      "%d × %d = %d g." % (grams // den, num,
                                           grams // den * num)], unit="g")

    def time_of():
        dd = pick([2, 3, 4, 5, 6, 10, 12])
        nn = random.randint(1, dd - 1)
        return _numq("What is %d/%d of an hour, in minutes?" % (nn, dd),
                     60 // dd * nn,
                     ["60 ÷ %d = %d minutes." % (dd, 60 // dd),
                      "%d × %d = %d minutes." % (60 // dd, nn,
                                                 60 // dd * nn)],
                     unit="minutes")

    def word_class():
        who = pick(NAMES)
        return _numq("A school has %d pupils. %d/%d of the pupils walk to "
                     "school. How many pupils walk to school?"
                     % (total, num, den), num * per,
                     ["%d ÷ %d = %d pupils in one %s."
                      % (total, den, per, _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %d pupils." % (per, num, num * per)],
                     unit="pupils")

    def word_remaining():
        return _numq("A box holds %d counters. %d/%d of them are red and the "
                     "rest are blue. How many counters are blue?"
                     % (total, num, den), total - num * per,
                     ["%d/%d of %d = %d red counters."
                      % (num, den, total, num * per),
                      "%d − %d = %d blue counters."
                      % (total, num * per, total - num * per)],
                     unit="counters")

    def inverse_whole():
        return _numq("%d/%d of a number is %d. What is the number?"
                     % (num, den, num * per), total,
                     ["%d ÷ %d = %d, which is one %s."
                      % (num * per, num, per, _FRAC_WORDS.get(den, "part")),
                      "%d × %d = %d." % (per, den, total)])

    def inverse_unit():
        return _numq("1/%d of a number is %d. What is the number?"
                     % (den, per), total,
                     ["One %s is %d." % (_FRAC_WORDS.get(den, "part"), per),
                      "%d × %d = %d." % (per, den, total)])

    def strip_model():
        parts = min(den, 8)
        each = per
        return _stripq("Use the strip model. A strip worth %d is split into %d "
                       "equal parts. What is one part worth?"
                       % (parts * each, parts), parts, "?",
                       str(parts * each), "part", each,
                       ["%d ÷ %d = %d." % (parts * each, parts, each)])

    def strip_model_multi():
        parts = min(den, 8)
        want = random.randint(1, parts - 1)
        return _stripq("Use the strip model. A strip worth %d is split into %d "
                       "equal parts. What %s %s worth altogether?"
                       % (parts * per, parts, "is" if want == 1 else "are",
                          _pl(want, "part")), parts, "?",
                       str(parts * per), "part", want * per,
                       ["%d ÷ %d = %d for one part." % (parts * per, parts,
                                                        per),
                        "%d × %d = %d." % (per, want, want * per)])

    def bar_chart_of():
        cats = ["Red", "Blue", "Green"]
        vals = [den * random.randint(2, 8) for _ in cats]
        i = random.randrange(3)
        return _barq("The chart shows how many beads of each colour are in a "
                     "jar. %d/%d of the %s beads are chipped. How many %s "
                     "beads are chipped?"
                     % (num, den, cats[i].lower(), cats[i].lower()),
                     cats, vals, vals[i] // den * num,
                     ["There are %d %s beads." % (vals[i], cats[i].lower()),
                      "%d ÷ %d = %d, and %d × %d = %d."
                      % (vals[i], den, vals[i] // den, vals[i] // den, num,
                         vals[i] // den * num)])

    def table_of():
        dd = pick([2, 4, 5, 10])
        amounts = [dd * random.randint(4, 20) for _ in range(3)]
        items = ["Book", "Game", "Puzzle"]
        rows = [[items[i], money(amounts[i])] for i in range(3)]
        i = random.randrange(3)
        nn = random.randint(1, dd - 1)
        return _dtq("The table shows the full price of each item. In a sale, "
                    "%d/%d of the price is taken off the %s. How many pence "
                    "are taken off?" % (nn, dd, items[i].lower()),
                    ["Item", "Full price"], rows, amounts[i] // dd * nn,
                    ["The %s costs %dp." % (items[i].lower(), amounts[i]),
                     "%d ÷ %d = %d, and %d × %d = %dp."
                     % (amounts[i], dd, amounts[i] // dd, amounts[i] // dd,
                        nn, amounts[i] // dd * nn)])

    def area_of_quantity():
        parts = pick([4, 6, 8, 10, 12])
        shaded = random.randint(1, parts - 1)
        each = random.randint(2, 12)
        return _agread("This area model shows a bag of %d sweets split into %d "
                       "equal parts, with %s shaded. How many sweets "
                       "does the shaded part represent?"
                       % (parts * each, parts, _pl(shaded, "part")), parts, shaded,
                       ["%d ÷ %d = %d sweets in each part."
                        % (parts * each, parts, each),
                        "%d × %d = %d sweets." % (each, shaded,
                                                  shaded * each)],
                       answer=shaded * each, answer_type="int",
                       placeholder="number of sweets")

    def compare_two():
        dd1 = pick([2, 3, 4, 5])
        dd2 = pick([x for x in [2, 3, 4, 5, 6] if x != dd1])
        L = _lcm(dd1, dd2) * random.randint(2, 8)
        n_1 = random.randint(1, dd1 - 1)
        n_2 = random.randint(1, dd2 - 1)
        v1, v2 = L // dd1 * n_1, L // dd2 * n_2
        for _ in range(30):
            if v1 != v2:
                break
            n_1 = random.randint(1, dd1 - 1)
            n_2 = random.randint(1, dd2 - 1)
            v1, v2 = L // dd1 * n_1, L // dd2 * n_2
        if v1 == v2:
            return bare()
        return _numq("Which is greater, %d/%d of %d or %d/%d of %d? Type the "
                     "greater amount." % (n_1, dd1, L, n_2, dd2, L),
                     max(v1, v2),
                     ["%d/%d of %d = %d." % (n_1, dd1, L, v1),
                      "%d/%d of %d = %d." % (n_2, dd2, L, v2),
                      "The greater amount is %d." % max(v1, v2)])

    opts = [bare, unit_fraction, money_of, mass_of, word_class,
            word_remaining, strip_model, strip_model_multi, bar_chart_of,
            table_of, area_of_quantity]
    if d == 0:
        opts = [unit_fraction, bare, money_of, word_class, strip_model,
                bar_chart_of, area_of_quantity, table_of]
    elif d == 2:
        opts = [bare, money_of, mass_of, time_of, word_remaining,
                inverse_whole, inverse_unit, compare_two, strip_model_multi,
                table_of, area_of_quantity, bar_chart_of]
    opts = opts + [strip_model_multi, area_of_quantity, bar_chart_of]
    return pick(opts)()


@skill("Y6.4.d", "Divide a fraction by a whole number", S4)
def _(d=1):
    d = _t(d)
    den = pick(_by_d(d, [2, 3, 4], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7, 8]))
    num = random.randint(1, den - 1)
    k = _by_d(d, random.randint(2, 3), random.randint(2, 5),
              random.randint(3, 8))

    def bare():
        return _fracq("Work out %d/%d ÷ %d. Write the answer as a fraction."
                      % (num, den, k), num, den * k,
                      ["Dividing by %d makes each part %d times smaller."
                       % (k, k),
                       "Multiply the denominator by %d: %d × %d = %d."
                       % (k, den, k, den * k),
                       "The answer is %d/%d." % (num, den * k)])

    def unit_bare():
        return _fracq("Work out 1/%d ÷ %d. Write the answer as a fraction."
                      % (den, k), 1, den * k,
                      ["1/%d split into %d equal pieces gives %s."
                       % (den, k, _plural_frac_word(den * k)),
                       "The answer is 1/%d." % (den * k)])

    def denominator_only():
        return _numq("%d/%d ÷ %d = %d/___ . Type the missing denominator."
                     % (num, den, k, num), den * k,
                     ["Dividing by %d multiplies the denominator by %d."
                      % (k, k),
                      "%d × %d = %d." % (den, k, den * k)])

    def exact_division():
        m = random.randint(2, 5)
        nn = m * random.randint(1, 3)
        dd = nn + random.randint(1, 6)
        return _fracq("Work out %d/%d ÷ %d. The numerator divides exactly, so "
                      "the denominator stays the same. Write the answer as a "
                      "fraction." % (nn, dd, m), nn // m, dd,
                      ["%d ÷ %d = %d." % (nn, m, nn // m),
                       "The answer is %d/%d." % (nn // m, dd)])

    def missing_divisor():
        return _numq("Complete:  %d/%d ÷ ___ = %d/%d" % (num, den, num,
                                                         den * k), k,
                     ["%d ÷ %d = %d." % (den * k, den, k),
                      "So the missing number is %d." % k])

    def shade_result():
        dd = den * k
        if dd > 12:
            return bare()
        return _fbq("This bar has %d equal parts. Shade it to show 1/%d ÷ %d."
                    % (dd, den, k), dd, 1,
                    ["Splitting each %s into %d gives %s."
                     % (_FRAC_WORDS.get(den, "part"), k,
                        _plural_frac_word(dd)),
                     "1/%d ÷ %d = 1/%d, so shade 1 part." % (den, k, dd)])

    def shade_area_result():
        dd = den * k
        if dd > 12:
            return bare()
        return _agshade("This area model has %d equal parts, because each "
                        "%s has been split into %d. Shade it to show "
                        "%d/%d ÷ %d."
                        % (dd, _FRAC_WORDS.get(den, "part"), k, num, den, k),
                        dd, num,
                        ["%d/%d ÷ %d = %d/%d." % (num, den, k, num, dd),
                         "Shade %s." % _pl(num, "part")])

    def on_line():
        dd = den * k
        if dd > 12:
            return bare()
        return _nlfrac("This number line is divided into %d equal steps. Work "
                       "out %d/%d ÷ %d and mark the answer."
                       % (dd, num, den, k), num, dd, 1,
                       ["%d/%d ÷ %d = %d/%d." % (num, den, k, num, dd),
                        "Mark %d steps of 1/%d from 0." % (num, dd)])

    def word_share_pizza():
        who = pick(NAMES)
        return _fracq("%s has %d/%d of a pizza and shares it equally between "
                      "%d people. What fraction of a whole pizza does each "
                      "person get?" % (who, num, den, k), num, den * k,
                      ["%d/%d ÷ %d = %d/%d."
                       % (num, den, k, num, den * k)])

    def word_ribbon():
        return _fracq("A piece of ribbon is %d/%d of a metre long. It is cut "
                      "into %d equal pieces. What fraction of a metre is each "
                      "piece?" % (num, den, k), num, den * k,
                      ["%d/%d ÷ %d = %d/%d."
                       % (num, den, k, num, den * k)])

    def word_paint():
        who = pick(NAMES)
        return _fracq("%s has 1/%d of a tin of paint and uses the same amount "
                      "on each of %d doors, using all of it. What fraction of "
                      "a tin is used on each door?" % (who, den, k),
                      1, den * k,
                      ["1/%d ÷ %d = 1/%d." % (den, k, den * k)])

    def inverse_check():
        return _numq("%d/%d ÷ %d = %d/%d. Check by multiplying: %d/%d × %d = "
                     "___/%d . Type the missing numerator."
                     % (num, den, k, num, den * k, num, den * k, k, den * k),
                     num * k,
                     ["%d/%d × %d = %d/%d." % (num, den * k, k, num * k,
                                               den * k),
                      "%d/%d = %d/%d, which is where we started."
                      % (num * k, den * k, num, den)])

    def table_divide():
        rows = [[str(i), "%d/%d" % (num, den * i)] for i in range(2, 6)]
        j = random.randrange(4)
        ans = den * (j + 2)
        rows[j][1] = ""
        return _dtq("%d/%d is shared equally between different numbers of "
                    "children. Type the denominator of the fraction each child "
                    "gets when it is shared between %d children."
                    % (num, den, j + 2),
                    ["Number of children", "Fraction each"], rows, ans,
                    ["%d/%d ÷ %d = %d/%d." % (num, den, j + 2, num, ans),
                     "The denominator is %d." % ans], missing=(j, 1),
                    placeholder="the denominator")

    opts = [bare, unit_bare, denominator_only, shade_result,
            shade_area_result, on_line, word_share_pizza, word_ribbon,
            table_divide]
    if d == 0:
        opts = [unit_bare, bare, denominator_only, shade_result,
                shade_area_result, on_line, word_paint, table_divide]
    elif d == 2:
        opts = [bare, exact_division, missing_divisor, inverse_check,
                word_share_pizza, word_ribbon, word_paint, table_divide,
                shade_area_result, on_line]
    opts = opts + [shade_area_result, on_line, shade_result]
    return pick(opts)()


@skill("Y6.4.e", "Relate fractions to division", S4)
def _(d=1):
    d = _t(d)
    a = _by_d(d, random.randint(1, 4), random.randint(2, 7),
              random.randint(3, 11))
    b = _by_d(d, random.randint(2, 5), random.randint(3, 8),
              random.randint(4, 12))
    while b == a:
        b = random.randint(2, 9)

    def division_as_fraction():
        return _fracq("Write %d ÷ %d as a fraction." % (a, b), a, b,
                      ["A division can be written as a fraction: %d ÷ %d = "
                       "%d/%d." % (a, b, a, b)])

    def fraction_as_division_num():
        return _numq("%d/%d can be written as a division. Complete:  %d/%d = "
                     "___ ÷ %d" % (a, b, a, b, b), a,
                     ["The numerator becomes the number being divided.",
                      "%d/%d = %d ÷ %d." % (a, b, a, b)])

    def fraction_as_division_den():
        return _numq("%d/%d can be written as a division. Complete:  %d/%d = "
                     "%d ÷ ___" % (a, b, a, b, a), b,
                     ["The denominator becomes the number you divide by.",
                      "%d/%d = %d ÷ %d." % (a, b, a, b)])

    def share_cakes():
        who = pick(NAMES)
        small, big = min(a, b), max(a, b)
        if small == big:
            small = max(1, big - 1)
        return _fracq("%s %s shared equally between %d children. What "
                      "fraction of a cake does each child get?"
                      % (_pl(small, "cake"), "is" if small == 1 else "are", big), small, big,
                      ["%d ÷ %d = %d/%d." % (small, big, small, big),
                       "Each child gets %d/%d of a cake." % (small, big)])

    def share_as_mixed():
        big = random.randint(5, 17)
        small = random.randint(2, 4)
        while big % small == 0:
            big += 1
        W, N, D = _improper_to_mixed(big, small)
        return _mixq("%d pizzas are shared equally between %d people. How much "
                     "pizza does each person get? Write the answer as a mixed "
                     "number, like  2 1/3 ." % (big, small), W, N, D,
                     ["%d ÷ %d = %d/%d." % (big, small, big, small),
                      "%d/%d = %s." % (big, small, _mixed_str(W, N, D))])

    def exact_division():
        q = random.randint(2, 9)
        n = q * b
        return _numq("Work out %d ÷ %d. The answer is a whole number — type "
                     "it." % (n, b), q,
                     ["%d ÷ %d = %d/%d." % (n, b, n, b),
                      "%d/%d = %d." % (n, b, q)])

    def strip_share():
        parts = min(max(b, 2), 8)
        each = random.randint(3, 20)
        return _stripq("Use the strip model. %d cakes weigh %d g altogether "
                       "and are shared equally between %d people. How many "
                       "grams of cake does each person get?"
                       % (parts, parts * each, parts), parts, "?",
                       "%d g" % (parts * each), "part", each,
                       ["%d ÷ %d = %d g." % (parts * each, parts, each)])

    def line_share():
        dd = pick([3, 4, 5, 6, 8])
        nn = random.randint(1, dd - 1)
        return _nlfrac("%d ÷ %d gives a fraction. Mark the answer on this "
                       "number line, which is ruled in steps of 1/%d."
                       % (nn, dd, dd), nn, dd, 1,
                       ["%d ÷ %d = %d/%d." % (nn, dd, nn, dd),
                        "Mark %d steps of 1/%d from 0." % (nn, dd)])

    def shade_share():
        dd = pick([3, 4, 5, 6, 8, 10, 12])
        nn = random.randint(1, dd - 1)
        return _fbq("%s %s shared equally between %d people. This bar "
                    "shows one whole cake in %d equal parts — shade the amount "
                    "one person gets." % (_pl(nn, "cake"), "is" if nn == 1 else "are", dd, dd), dd, nn,
                    ["%d ÷ %d = %d/%d of a cake each." % (nn, dd, nn, dd),
                     "Shade %s." % _pl(nn, "part")])

    def area_share():
        parts = pick([4, 6, 8, 10, 12])
        nn = random.randint(1, parts - 1)
        return _agshade("%s of bread %s shared equally between %d "
                        "families. This area model shows one whole loaf in %d "
                        "equal parts. Shade the amount one family gets."
                        % (_pl(nn, "loaf", "loaves"), "is" if nn == 1 else "are", parts, parts), parts, nn,
                        ["%d ÷ %d = %d/%d of a loaf each."
                         % (nn, parts, nn, parts),
                         "Shade %d of the %d parts." % (nn, parts)])

    def reciprocal_fraction():
        rn, rd = pick(_by_d(d,
                            [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4)],
                            [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6),
                             (3, 8), (5, 8), (7, 10)],
                            [(3, 7), (4, 9), (5, 8), (7, 8), (7, 12), (9, 10),
                             (5, 12), (11, 12)]))
        return _fracq("What is the reciprocal of %d/%d? Write your answer as a "
                      "fraction." % (rn, rd), rd, rn,
                      ["To find the reciprocal of a fraction, swap the "
                       "numerator and the denominator.",
                       "The reciprocal of %d/%d is %d/%d." % (rn, rd, rd, rn)])

    def reciprocal_whole():
        w = random.randint(*_by_d(d, (2, 6), (2, 12), (3, 20)))
        return _fracq("What is the reciprocal of %d? Write your answer as a "
                      "fraction." % w, 1, w,
                      ["%d is the same as %d/1." % (w, w),
                       "Swapping the numerator and the denominator gives 1/%d."
                       % w])

    def reciprocal_numerator():
        rn, rd = pick([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6),
                       (3, 8), (5, 8), (7, 10), (3, 7), (4, 9), (5, 12)])
        if random.random() < 0.5:
            return _numq("The reciprocal of %d/%d is a fraction in its lowest "
                         "terms. Type the numerator of that reciprocal."
                         % (rn, rd), rd,
                         ["The reciprocal of %d/%d is %d/%d." % (rn, rd, rd, rn),
                          "Its numerator is %d." % rd],
                         placeholder="the numerator")
        return _numq("The reciprocal of %d/%d is a fraction in its lowest "
                     "terms. Type the denominator of that reciprocal."
                     % (rn, rd), rn,
                     ["The reciprocal of %d/%d is %d/%d." % (rn, rd, rd, rn),
                      "Its denominator is %d." % rn],
                     placeholder="the denominator")

    def table_divisions():
        rows = [["%d ÷ %d" % (i, b), "%d/%d" % (i, b)] for i in range(1, 5)]
        j = random.randrange(4)
        ans = j + 1
        rows[j][1] = ""
        return _dtq("Every division in this table is written as a fraction "
                    "with denominator %d. Type the numerator that belongs in "
                    "the empty cell." % b, ["Division", "Fraction"], rows, ans,
                    ["%d ÷ %d = %d/%d." % (j + 1, b, j + 1, b),
                     "The numerator is %d." % ans], missing=(j, 1),
                    placeholder="the numerator")

    def which_is_more():
        p, q = _two_names()
        a1, b1 = random.randint(1, 5), random.randint(2, 6)
        a2, b2 = random.randint(1, 5), random.randint(2, 6)
        while Fraction(a1, b1) == Fraction(a2, b2):
            a2 = random.randint(1, 5)
        winner = p if Fraction(a1, b1) > Fraction(a2, b2) else q
        return _wordq("%s %s shared between %d children in %s's group, "
                      "and %s %s shared between %d children in %s's "
                      "group. In which group does each child get more? Type "
                      "the name of the person whose group it is."
                      % (_pl(a1, "cake"), "is" if a1 == 1 else "are", b1, p,
                         _pl(a2, "cake"), "is" if a2 == 1 else "are", b2, q), winner,
                      ["%d ÷ %d = %d/%d and %d ÷ %d = %d/%d."
                       % (a1, b1, a1, b1, a2, b2, a2, b2),
                       "%s's group gets more each." % winner],
                      placeholder="a name")

    def remainder_as_fraction():
        dd = random.randint(2, 6)
        q = random.randint(2, 9)
        r = random.randint(1, dd - 1)
        n = q * dd + r
        return _numq("%d ÷ %d = %d and a fraction. The fraction has "
                     "denominator %d — type its numerator." % (n, dd, q, dd),
                     r,
                     ["%d × %d = %d." % (dd, q, q * dd),
                      "%d − %d = %d, so the fraction is %d/%d."
                      % (n, q * dd, r, r, dd)])

    opts = [division_as_fraction, fraction_as_division_num, share_cakes,
            shade_share, area_share, line_share, table_divisions, strip_share,
            exact_division, reciprocal_fraction, reciprocal_whole,
            reciprocal_numerator]
    if d == 0:
        opts = [division_as_fraction, fraction_as_division_num, share_cakes,
                shade_share, area_share, line_share, table_divisions,
                strip_share]
    elif d == 2:
        opts = [division_as_fraction, fraction_as_division_den, share_as_mixed,
                remainder_as_fraction, which_is_more, table_divisions,
                strip_share, area_share, line_share, exact_division,
                reciprocal_fraction, reciprocal_numerator]
    opts = opts + [shade_share, area_share, line_share, table_divisions]
    return pick(opts)()


@skill("Y6.4.f", "Multi-step fraction problems", S4)
def _(d=1):
    d = _t(d)

    def fraction_then_remainder():
        dd = pick([2, 3, 4, 5])
        per = random.randint(4, _by_d(d, 10, 20, 40))
        total = dd * per
        nn = random.randint(1, dd - 1)
        used = nn * per
        dd2 = pick([2, 3, 4])
        left = total - used
        if left % dd2 != 0:
            dd2 = 2
            if left % 2 != 0:
                return _numq("A jar holds %d sweets. %d/%d of the sweets are "
                             "eaten. How many sweets are left?"
                             % (total, nn, dd), left,
                             ["%d/%d of %d = %d eaten."
                              % (nn, dd, total, used),
                              "%d − %d = %d left." % (total, used, left)],
                             unit="sweets")
        second = left // dd2
        return _numq("A jar holds %d sweets. %d/%d of them are eaten on "
                     "Monday. On Tuesday 1/%d of the sweets that are left are "
                     "eaten. How many sweets are eaten on Tuesday?"
                     % (total, nn, dd, dd2), second,
                     ["%d/%d of %d = %d eaten on Monday."
                      % (nn, dd, total, used),
                      "%d − %d = %d left." % (total, used, left),
                      "%d ÷ %d = %d eaten on Tuesday."
                      % (left, dd2, second)], unit="sweets")

    def add_then_of():
        dd = pick([4, 6, 8, 10, 12])
        a = random.randint(1, dd - 2)
        b = random.randint(1, dd - a - 1)
        per = random.randint(3, 15)
        total = dd * per
        return _numq("A bag holds %d marbles. %d/%d of them are red and %d/%d "
                     "are blue. How many marbles are red or blue altogether?"
                     % (total, a, dd, b, dd), (a + b) * per,
                     ["%d/%d + %d/%d = %d/%d." % (a, dd, b, dd, a + b, dd),
                      "%d ÷ %d = %d, and %d × %d = %d marbles."
                      % (total, dd, per, per, a + b, (a + b) * per)],
                     unit="marbles")

    def money_two_steps():
        dd = pick([2, 4, 5])
        start = dd * random.randint(4, 30) * 10
        nn = random.randint(1, dd - 1)
        spent = start // dd * nn
        left = start - spent
        who = pick(NAMES)
        return _numq("%s starts with %s and spends %d/%d of it. How much money "
                     "does %s have left, in pence?"
                     % (who, money(start), nn, dd, who), left,
                     ["%d/%d of %dp = %dp spent." % (nn, dd, start, spent),
                      "%d − %d = %dp left." % (start, spent, left)],
                     unit="p")

    def fraction_of_fraction():
        d1 = pick([2, 3, 4])
        d2 = pick([2, 3, 4, 5])
        per = random.randint(2, 10)
        total = d1 * d2 * per
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        first = total // d1 * n1
        second = first // d2 * n2
        return _numq("A school has %d pupils. %d/%d of the pupils are in Key "
                     "Stage 2, and %d/%d of those pupils walk to school. How "
                     "many pupils walk to school?"
                     % (total, n1, d1, n2, d2), second,
                     ["%d/%d of %d = %d pupils in Key Stage 2."
                      % (n1, d1, total, first),
                      "%d/%d of %d = %d pupils walk."
                      % (n2, d2, first, second)], unit="pupils")

    def strip_two_step():
        parts = pick([4, 5, 6, 8])
        per = random.randint(5, 25)
        total = parts * per
        want = random.randint(1, parts - 1)
        return _stripq("Use the strip model. A rope %d cm long is cut into %d "
                       "equal pieces. How long is one piece, in cm?"
                       % (total, parts), parts, "?", "%d cm" % total, "part",
                       per,
                       ["%d ÷ %d = %d cm." % (total, parts, per)])

    def bar_two_step():
        cats = ["Year 4", "Year 5", "Year 6"]
        dd = pick([2, 3, 4])
        vals = [dd * random.randint(4, 15) for _ in cats]
        i = random.randrange(3)
        nn = random.randint(1, dd - 1)
        got = vals[i] // dd * nn
        return _barq("The chart shows how many books each year group borrowed. "
                     "%d/%d of the %s books were novels. How many %s books "
                     "were novels?" % (nn, dd, cats[i], cats[i]), cats, vals,
                     got,
                     ["%s borrowed %d books." % (cats[i], vals[i]),
                      "%d ÷ %d = %d, and %d × %d = %d novels."
                      % (vals[i], dd, vals[i] // dd, vals[i] // dd, nn, got)])

    def recipe_table():
        dd = pick([2, 4])
        base = [dd * random.randint(2, 10) for _ in range(3)]
        items = ["Flour (g)", "Sugar (g)", "Butter (g)"]
        rows = [[items[i], str(base[i])] for i in range(3)]
        i = random.randrange(3)
        nn = random.randint(1, dd - 1)
        return _dtq("The table shows the ingredients for one cake. A smaller "
                    "cake uses %d/%d of every amount. How many grams of the "
                    "ingredient on row %d — %s — does the smaller cake need?"
                    % (nn, dd, i + 1, items[i].split(" ")[0].lower()),
                    ["Ingredient", "Amount"], rows, base[i] // dd * nn,
                    ["The full recipe uses %d g." % base[i],
                     "%d ÷ %d = %d, and %d × %d = %d g."
                     % (base[i], dd, base[i] // dd, base[i] // dd, nn,
                        base[i] // dd * nn)])

    def area_two_step():
        parts = pick([8, 10, 12])
        a = random.randint(2, parts - 4)
        b = random.randint(2, parts - a - 1)
        left = parts - a - b
        return _agshade("A field is split into %d equal strips. %s grow "
                        "wheat and %s grow barley. Shade the area model "
                        "to show the fraction of the field that is left over."
                        % (parts, _pl(a, "strip"), _pl(b, "strip")), parts,
                        left,
                        ["%d + %d = %d strips are used." % (a, b, a + b),
                         "%d − %d = %s left, which is %d/%d."
                         % (parts, a + b, _pl(left, "strip"), left, parts)])

    def line_two_step():
        dd = pick([6, 8, 10, 12])
        a = random.randint(1, dd - 3)
        b = random.randint(1, dd - a - 2)
        c = random.randint(1, dd - a - b - 1)
        return _nlfrac("A walk has three parts: %d/%d of a mile, %d/%d of a "
                       "mile and %d/%d of a mile. Mark the total distance on "
                       "the number line, where 1 stands for one mile."
                       % (a, dd, b, dd, c, dd), a + b + c, dd, 1,
                       ["%d + %d + %d = %d." % (a, b, c, a + b + c),
                        "The total is %d/%d of a mile." % (a + b + c, dd)])

    def mixed_multi():
        dd = pick([4, 5, 6, 8])
        w = random.randint(1, 4)
        p = random.randint(1, dd - 1)
        k = random.randint(2, 4)
        while (p * k) % dd == 0:
            k = random.randint(2, 4)
            p = random.randint(1, dd - 1)
        tot = (w * dd + p) * k
        W, N, D = _improper_to_mixed(tot, dd)
        return _mixq("One bottle holds %s litres of water. How much water is "
                     "in %d identical bottles, in litres? Write the answer as "
                     "a mixed number." % (_mixed_str(w, p, dd), k), W, N, D,
                     ["%s = %d/%d litres." % (_mixed_str(w, p, dd),
                                              w * dd + p, dd),
                      "%d/%d × %d = %d/%d, which is %s litres."
                      % (w * dd + p, dd, k, tot, dd, _mixed_str(W, N, D))])

    def divide_then_multiply():
        dd = pick([2, 3, 4])
        k = random.randint(2, 4)
        return _fracq("A cake is cut so that each person gets 1/%d of it. Each "
                      "of those pieces is then split equally between %d "
                      "children. What fraction of the whole cake does each "
                      "child get?" % (dd, k), 1, dd * k,
                      ["1/%d ÷ %d = 1/%d." % (dd, k, dd * k)])

    def difference_of_fractions_of():
        dd = pick([4, 5, 6, 8, 10])
        per = random.randint(3, 20)
        total = dd * per
        n1 = random.randint(2, dd - 1)
        n2 = random.randint(1, n1 - 1)
        return _numq("%d/%d of %d and %d/%d of %d are worked out. What is the "
                     "difference between the two answers?"
                     % (n1, dd, total, n2, dd, total), (n1 - n2) * per,
                     ["%d/%d of %d = %d." % (n1, dd, total, n1 * per),
                      "%d/%d of %d = %d." % (n2, dd, total, n2 * per),
                      "%d − %d = %d." % (n1 * per, n2 * per,
                                         (n1 - n2) * per)])

    def reverse_left():
        dd = pick([3, 4, 5, 8])
        nn = random.randint(1, dd - 1)
        per = random.randint(2, _by_d(d, 6, 12, 25))
        start = dd * per
        who = pick(NAMES)
        return _numq("%s spends %d/%d of their savings and has £%d left. How much did %s have to start with, in pounds?"
                     % (who, nn, dd, (dd - nn) * per, who), start,
                     ["%d/%d is left, and that is £%d." % (dd - nn, dd, (dd - nn) * per),
                      "So 1/%d is £%d ÷ %d = £%d." % (dd, (dd - nn) * per, dd - nn, per),
                      "The whole is %d × £%d = £%d." % (dd, per, start)], unit="£")

    def what_fraction_left():
        d1, d2 = random.sample([2, 3, 4, 5, 6, 8], 2)
        f = Fraction(1, d1) + Fraction(1, d2)
        left = 1 - f
        thing, a, b = pick([("garden", "grass", "flowers"), ("class", "walk to school", "come by bus"),
                            ("bookshelf", "stories", "atlases")])
        return _fracq("In a %s, 1/%d is %s and 1/%d is %s. What fraction is left for everything else?"
                      % (thing, d1, a, d2, b) if thing != "class" else
                      "In a class, 1/%d of the children %s and 1/%d %s. What fraction of the class travel some other way?"
                      % (d1, a, d2, b), left.numerator, left.denominator,
                      ["1/%d + 1/%d = %d/%d." % (d1, d2, f.numerator, f.denominator),
                       "1 − %d/%d = %d/%d." % (f.numerator, f.denominator, left.numerator, left.denominator)])

    def how_much_more():
        a, b = random.sample([Fraction(2, 5), Fraction(3, 8), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(1, 3)], 2)
        big, small = max(a, b), min(a, b)
        diff = big - small
        who1, who2 = random.sample(NAMES, 2)
        return _fracq("%s eats %d/%d of a pizza. %s eats %d/%d of an identical pizza. How much more pizza does %s eat? "
                      "Give the answer as a fraction." % (who1, big.numerator, big.denominator, who2, small.numerator,
                                                          small.denominator, who1), diff.numerator, diff.denominator,
                      ["Use a common denominator: %d/%d − %d/%d." % (big.numerator, big.denominator, small.numerator,
                                                                     small.denominator),
                       "The difference is %d/%d." % (diff.numerator, diff.denominator)])

    opts = [fraction_then_remainder, add_then_of, fraction_of_fraction,
            strip_two_step, bar_two_step, recipe_table, area_two_step,
            line_two_step, mixed_multi, money_two_steps, reverse_left, what_fraction_left, how_much_more]
    if d == 0:
        opts = [add_then_of, strip_two_step, bar_two_step, area_two_step,
                line_two_step, recipe_table, money_two_steps, reverse_left]
    elif d == 2:
        opts = [fraction_then_remainder, fraction_of_fraction, mixed_multi,
                divide_then_multiply, difference_of_fractions_of,
                recipe_table, bar_two_step, area_two_step, line_two_step, reverse_left, what_fraction_left,
                how_much_more]
    opts = opts + [area_two_step, line_two_step, strip_two_step]
    return pick(opts)()


