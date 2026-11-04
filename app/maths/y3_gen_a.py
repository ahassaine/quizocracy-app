# dev/app/logic/y3_gen_a.py — Year 3 generators: levels 3.0 and 3.1
#
# Every generator takes a difficulty `d`:  0 = easy, 1 = core, 2 = stretch.
# Each skill offers 5-6 genuinely different framings (bare calculation, word
# problem, missing number, inverse, visual model, compare-two, odd-one-out)
# and leans on the `base_ten` / `number_line` components wherever the concept
# is about representing, ordering or rounding numbers.
import random
from .maths_engine import skill, n_words, ordinal, pick, NAMES

S0 = "3.0 Number & place value"
S1 = "3.1 Compare, order, round, patterns"


# ------------------------------------------------------------------ utils ----
def _d(d):
    """Clamp difficulty to 0/1/2."""
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _r10(n):
    """Round to the nearest 10, halves up (n >= 0)."""
    return ((int(n) + 5) // 10) * 10


def _r100(n):
    """Round to the nearest 100, halves up (n >= 0)."""
    return ((int(n) + 50) // 100) * 100


def _n(d):
    """A number of the right size for this difficulty."""
    if d == 0:
        return random.randint(11, 99)
    if d == 1:
        return random.randint(101, 999)
    # stretch: 3-digit, often with zeros / nines that trip pupils up
    if random.random() < 0.45:
        h = random.randint(1, 9)
        t = pick([0, 0, 9])
        o = pick([0, 9, random.randint(1, 9)])
        return h * 100 + t * 10 + o
    return random.randint(101, 999)


def _u(k, place):
    """'1 ten' / '3 tens', '1 one' / '0 ones' for place = 'hundreds', 'tens' or 'ones'."""
    return "%d %s" % (k, place[:-1] if k == 1 else place)


def _hto(n):
    """'3 hundreds, 4 tens and 2 ones' (drops hundreds for 2-digit numbers)."""
    n = int(n)
    h, t, o = n // 100, (n // 10) % 10, n % 10
    if h:
        return "%s, %s and %s" % (_u(h, "hundreds"), _u(t, "tens"), _u(o, "ones"))
    return "%s and %s" % (_u(t, "tens"), _u(o, "ones"))


def _places(d):
    return [(100, "hundreds"), (10, "tens"), (1, "ones")] if d >= 1 else [(10, "tens"), (1, "ones")]


def _distinct(d):
    """A number whose digits are all different (so a digit names one place)."""
    if d == 0:
        a, b = random.sample(range(1, 10), 2)
        return a * 10 + b
    a, b, c = random.sample(range(1, 10), 3)
    return a * 100 + b * 10 + c


# --- question builders -------------------------------------------------------
def _tb(prompt, ans, atype="int", spec=None, solution=None):
    """A typed-answer question (the plain `number` component)."""
    return {"prompt": prompt, "component": "number", "spec": spec or {},
            "answer": ans, "answer_type": atype, "solution": solution or []}


def _bt(prompt, ans, solution):
    """A build-it-with-place-value-blocks question."""
    ans = int(ans)
    return {"prompt": prompt, "component": "base_ten", "spec": {"mode": "build", "max": 9},
            "answer": ans, "answer_type": "int", "solution": solution}


def _nl(prompt, ans, step, major, solution):
    """A place-the-marker-on-a-number-line question.

    `ans` must be a multiple of `step`, and `major` a multiple of `step`.
    """
    ans = int(ans)
    lo = (ans // major) * major - 2 * major
    if lo < 0:
        lo = 0
    hi = lo + 5 * major
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": lo, "max": hi, "step": step, "major": major},
            "answer": ans, "answer_type": "num", "tolerance": step / 2.0,
            "solution": solution}


def _pick_t(plain, visual):
    """Choose a framing; visual framings are twice as likely as typed ones."""
    return random.choice(list(plain) + list(visual) + list(visual))()


def _lst(xs):
    return ", ".join(str(x) for x in xs)


# ------------------------------------------------------------------ 3.0 ------
@skill("Y3.0.a", "Count in multiples of 4, 8, 50, 100", S0)
def _(d=1):
    d = _d(d)
    step = pick([4, 50, 100] if d == 0 else [4, 8, 50, 100])
    kmax = {0: 6, 1: 12, 2: 18}[d]
    start = random.randint(2, kmax) * step

    def t_next():
        back = d >= 1 and random.random() < 0.4 and start - 3 * step >= 0
        sg = -step if back else step
        seq = [start + (i + 1) * sg for i in range(3)]
        return _tb("Count %s in %ds from %d. Write the next three numbers."
                   % ("back" if back else "on", step, start),
                   _lst(seq), "str",
                   {"text": True, "placeholder": "e.g. 12, 16, 20"},
                   ["%s %d each time: %s." % ("Subtract" if back else "Add", step, _lst(seq))])

    def t_forward():
        st = 1 if d == 0 else pick([1, 1, 2, 5, 10])
        s = random.randint(10, 1000 - 4 * st)
        seq = [s + (i + 1) * st for i in range(3)]
        return _tb("Count forward in %ds from %d, up to 1,000. Write the next three numbers."
                   % (st, s), _lst(seq), "str",
                   {"text": True, "placeholder": "e.g. %s" % _lst(seq[:2] + ["..."])},
                   ["Counting forward means adding %d each time." % st,
                    "The next three numbers are %s." % _lst(seq)])

    def t_missing():
        terms = [start + i * step for i in range(5)]
        idx = random.randint(1, 3)
        shown = ", ".join("___" if i == idx else str(t) for i, t in enumerate(terms))
        return _tb("These numbers are counting on in %ds. Find the missing one: %s" % (step, shown),
                   terms[idx], "int", {},
                   ["%d + %d = %d." % (terms[idx - 1], step, terms[idx])])

    def t_word():
        k = random.randint(3, 6 if d == 0 else 9)
        holder, thing = pick([("crates", "apples"), ("boxes", "pencils"),
                              ("bags", "marbles"), ("trays", "cakes")])
        who = pick(NAMES)
        return _tb("%s has %d %s. Each one holds %d %s. How many %s altogether?"
                   % (who, k, holder, step, thing, thing),
                   k * step, "int", {"unit": thing},
                   ["Count on in %ds, %d times." % (step, k),
                    "%d × %d = %d." % (k, step, k * step)])

    def t_inverse():
        k = random.randint(3, 9)
        return _tb("%s counts on in %ds from 0: %d, %d, %d, ... How many counts does it take to reach %d?"
                   % (pick(NAMES), step, step, 2 * step, 3 * step, k * step),
                   k, "int", {"unit": "counts"},
                   ["%d ÷ %d = %d." % (k * step, step, k)])

    def t_line():
        k = random.randint(2, 4)
        ans = start + k * step
        major = {4: 20, 8: 40, 50: 100, 100: 200}[step]
        return _nl("Start at %d and count on %d lots of %d. Place the number you land on."
                   % (start, k, step), ans, step, major,
                   ["%d × %d = %d." % (k, step, k * step),
                    "%d + %d = %d." % (start, k * step, ans)])

    def t_blocks():
        k = random.randint(2, 4)
        top = max(1, (999 - k * step) // step)
        s = random.randint(1, top) * step
        ans = s + k * step
        return _bt("Count on %d lots of %d from %d, then build the number you land on."
                   % (k, step, s), ans,
                   ["%d × %d = %d." % (k, step, k * step),
                    "%d + %d = %d." % (s, k * step, ans)])

    return _pick_t([t_next, t_forward, t_missing, t_word, t_inverse], [t_line, t_blocks])


@skill("Y3.0.b", "Write a number in numerals", S0)
def _(d=1):
    d = _d(d)
    n = _n(d)

    def t_words():
        return _tb("Write '%s' as a numeral." % n_words(n), n, "int", {},
                   ["'%s' is %d." % (n_words(n), n)])

    def t_words_to_digits():
        return _tb("Convert this number from words to digits:  '%s'" % n_words(n), n, "int", {},
                   ["The words '%s' mean %d." % (n_words(n), n),
                    "In digits that is %d." % n])

    def t_digits_given_words():
        return _tb("Here is a number given in words: '%s'. Write the digits for that number."
                   % n_words(n), n, "int", {},
                   ["'%s' is %d." % (n_words(n), n)])

    def t_convert_between():
        return _tb("Convert between digits and words (numbers up to 1,000): which number in "
                   "digits matches the words '%s'?" % n_words(n), n, "int", {},
                   ["'%s' is %d in digits." % (n_words(n), n)])

    def t_parts():
        return _tb("Write the number that has %s." % _hto(n), n, "int", {},
                   ["%s makes %d." % (_hto(n).capitalize(), n)])

    def t_word_problem():
        who = pick(NAMES)
        return _tb("%s writes a cheque for '%s' pounds. Write that amount in numerals."
                   % (who, n_words(n)), n, "int", {"unit": "£"},
                   ["'%s' is %d." % (n_words(n), n)])

    def t_compare():
        m = _n(d)
        while m == n:
            m = _n(d)
        big = max(n, m)
        return _tb("Which is the greater number: '%s' or '%s'? Write it in numerals."
                   % (n_words(n), n_words(m)), big, "int", {},
                   ["'%s' is %d and '%s' is %d." % (n_words(n), n, n_words(m), m),
                    "%d is greater." % big])

    def t_blocks():
        return _bt("Build '%s' with the place-value blocks." % n_words(n), n,
                   ["'%s' is %d." % (n_words(n), n),
                    "%d = %s." % (n, _hto(n))])

    def t_line():
        m = (n // 10) * 10
        if m < 10:
            m = 10
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Place '%s' on the number line." % n_words(m), m, step, major,
                   ["'%s' is %d." % (n_words(m), m)])

    return _pick_t([t_words, t_words_to_digits, t_digits_given_words, t_convert_between,
                    t_parts, t_word_problem, t_compare], [t_blocks, t_line])


@skill("Y3.0.c", "Write a number in words", S0)
def _(d=1):
    d = _d(d)
    n = _n(d)

    def t_bare():
        return _tb("Write the number %d in words." % n, n_words(n), "str",
                   {"text": True, "placeholder": "type in words"},
                   ["%d is '%s'." % (n, n_words(n))])

    def t_digits_to_words():
        return _tb("Convert this number from digits to words:  %d  (numbers up to 1,000)" % n,
                   n_words(n), "str", {"text": True, "placeholder": "type in words"},
                   ["%d is written '%s' in words." % (n, n_words(n))])

    def t_words_given_digits():
        return _tb("Here is a number given in digits: %d. Write the words for that number." % n,
                   n_words(n), "str", {"text": True, "placeholder": "type in words"},
                   ["%d in words is '%s'." % (n, n_words(n))])

    def t_parts():
        return _tb("Write in words the number that has %s." % _hto(n), n_words(n), "str",
                   {"text": True, "placeholder": "type in words"},
                   ["%s makes %d." % (_hto(n).capitalize(), n),
                    "%d is '%s'." % (n, n_words(n))])

    def t_calc():
        amt = pick([10, 100]) if d >= 1 else 10
        base = n if n + amt <= 999 else n - amt
        ans = base + amt
        return _tb("What is %d more than %d? Write your answer in words." % (amt, base),
                   n_words(ans), "str", {"text": True, "placeholder": "type in words"},
                   ["%d + %d = %d." % (base, amt, ans), "%d is '%s'." % (ans, n_words(ans))])

    def t_word_problem():
        who = pick(NAMES)
        return _tb("%s is filling in a cheque for £%d. Write the amount in words." % (who, n),
                   n_words(n), "str", {"text": True, "placeholder": "type in words"},
                   ["%d is '%s'." % (n, n_words(n))])

    def t_compare():
        m = _n(d)
        while m == n:
            m = _n(d)
        big = max(n, m)
        return _tb("Which is greater, %d or %d? Write the greater number in words." % (n, m),
                   n_words(big), "str", {"text": True, "placeholder": "type in words"},
                   ["%d is greater than %d." % (big, min(n, m)),
                    "%d is '%s'." % (big, n_words(big))])

    return _pick_t([t_bare, t_digits_to_words, t_words_given_digits, t_parts, t_calc,
                    t_word_problem, t_compare], [])


@skill("Y3.0.d", "Represent a number (blocks or number line)", S0)
def _(d=1):
    d = _d(d)
    n = _n(d)

    def t_build():
        return _bt("Build the number %d using the place-value blocks." % n, n,
                   ["%d = %s." % (n, _hto(n))])

    def t_build_words():
        return _bt("Build the number '%s' using the place-value blocks." % n_words(n), n,
                   ["'%s' is %d." % (n_words(n), n), "%d = %s." % (n, _hto(n))])

    def t_build_partition():
        h, t, o = n // 100, (n // 10) % 10, n % 10
        expr = (" + ".join(str(x) for x in (h * 100, t * 10, o) if x) or "0")
        if "+" not in expr:
            return t_build()
        return _bt("Build the number shown by %s." % expr, n,
                   ["%s = %d." % (expr, n)])

    def t_place():
        m = (n // 10) * 10
        if m < 10:
            m = 10
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Place %d on the number line." % m, m, step, major,
                   ["%d sits between %d and %d." % (m, (m // major) * major, (m // major) * major + major)])

    def t_place_shifted():
        amt = pick([10, 100]) if d >= 1 else 10
        base = (n // 10) * 10
        if base < 10:
            base = 10
        if base + amt > 990:
            base -= amt
        ans = base + amt
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Place the number that is %d more than %d on the number line." % (amt, base),
                   ans, step, major, ["%d + %d = %d." % (base, amt, ans)])

    def t_read():
        return _tb("A set of blocks shows %s. What number is it?" % _hto(n), n, "int", {},
                   ["%s = %d." % (_hto(n).capitalize(), n)])

    return _pick_t([t_read], [t_build, t_build_words, t_build_partition, t_place, t_place_shifted])


@skill("Y3.0.e", "Identify the digit in a place", S0)
def _(d=1):
    d = _d(d)

    def t_bare():
        n = _n(d)
        pos, place = pick(_places(d))
        return _tb("In the number %d, which digit is in the %s place?" % (n, place),
                   (n // pos) % 10, "int", {},
                   ["%d = %s." % (n, _hto(n)),
                    "The %s digit is %d." % (place, (n // pos) % 10)])

    def t_from_words():
        n = _n(d)
        pos, place = pick(_places(d))
        return _tb("In the number '%s', which digit is in the %s place?" % (n_words(n), place),
                   (n // pos) % 10, "int", {},
                   ["'%s' is %d." % (n_words(n), n),
                    "The %s digit is %d." % (place, (n // pos) % 10)])

    def t_which_place():
        n = _distinct(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        return _tb("In the number %d, which place is the digit %d in? (hundreds, tens or ones)"
                   % (n, dig), place, "str",
                   {"text": True, "placeholder": "hundreds / tens / ones"},
                   ["%d = %s." % (n, _hto(n)), "The %d is in the %s place." % (dig, place)])

    def t_guess():
        n = _distinct(d)
        h, t, o = n // 100, (n // 10) % 10, n % 10
        if d == 0:
            return _tb("Guess the number: it is a 2-digit number, its tens digit is %d "
                       "and its ones digit is %d. What is the number?" % (t, o),
                       n, "int", {},
                       ["%s and %s." % (_u(t, "tens"), _u(o, "ones")), "The number is %d." % n])
        return _tb("Guess the number: it is a 3-digit number between %d and %d, its tens "
                   "digit is %d and its ones digit is %d. What is the number?"
                   % (h * 100, h * 100 + 100, t, o), n, "int", {},
                   ["It has %s." % _hto(h * 100 + t * 10 + o),
                    "The number is %d." % n])

    def t_odd_one_out():
        pos, place = pick(_places(d))
        dig = random.randint(1, 9)
        def make(has):
            while True:
                m = _n(d)
                if (((m // pos) % 10) == dig) == has and m >= (100 if d >= 1 else 10):
                    return m
        target = make(True)
        opts = [target]
        while len(opts) < 4:
            m = make(False)
            if m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers has the digit %d in the %s place?   %s"
                   % (dig, place, _lst(opts)), target, "int", {},
                   ["Check the %s digit of each number." % place,
                    "%d has %d in the %s place." % (target, dig, place)])

    def t_compare():
        pos, place = pick(_places(d))
        a, b = _n(d), _n(d)
        while ((a // pos) % 10) == ((b // pos) % 10):
            b = _n(d)
        big = a if ((a // pos) % 10) > ((b // pos) % 10) else b
        return _tb("Which number has the BIGGER digit in the %s place: %d or %d? Write that number."
                   % (place, a, b), big, "int", {},
                   ["%d has %d in the %s place; %d has %d."
                    % (a, (a // pos) % 10, place, b, (b // pos) % 10),
                    "So %d has the bigger %s digit." % (big, place)])

    def t_build():
        n = _distinct(d)
        parts = [(pos, place, (n // pos) % 10) for pos, place in _places(d)]
        random.shuffle(parts)
        desc = ", ".join("%d in the %s" % (dig, place) for _pos, place, dig in parts)
        return _bt("Build the number that has %s." % desc, n, ["The number is %d." % n])

    return _pick_t([t_bare, t_from_words, t_which_place, t_guess, t_odd_one_out, t_compare],
                   [t_build])


@skill("Y3.0.f", "Value of a digit", S0)
def _(d=1):
    d = _d(d)

    def t_bare():
        n = _n(d)
        pos, place = pick(_places(d))
        for _ in range(8):                 # a value of 0 makes a poor question
            if (n // pos) % 10:
                break
            n = _n(d)
        dig = (n // pos) % 10
        return _tb("In the number %d, what is the VALUE of the digit in the %s place?" % (n, place),
                   dig * pos, "int", {},
                   ["The %s digit is %d." % (place, dig),
                    "Its value is %d × %d = %d." % (dig, pos, dig * pos)])

    def t_named_digit():
        n = _distinct(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        return _tb("What is the value of the digit %d in the number %d?" % (dig, n),
                   dig * pos, "int", {},
                   ["The %d is in the %s place." % (dig, place),
                    "It is worth %d." % (dig * pos)])

    def t_convert_places():
        big, small, factor = pick([("hundreds", "tens", 10),
                                   ("tens", "ones", 10),
                                   ("hundreds", "ones", 100)] if d >= 1
                                  else [("tens", "ones", 10)])
        k = random.randint(2, 9)
        ans = k * factor
        val = k * (100 if big == "hundreds" else 10)
        return _tb("Convert between place values (up to hundreds):  %d %s = ___ %s"
                   % (k, big, small), ans, "int", {"unit": small},
                   ["%d %s is %d." % (k, big, val),
                    "%d = %d %s." % (val, ans, small)])

    def t_correct_it():
        n = _distinct(d)
        pos, place = pick([p for p in _places(d) if p[0] != 1])
        dig = (n // pos) % 10
        who = pick(NAMES)
        return _tb("%s says the %d in %d is worth %d. %s is wrong — what is it really worth?"
                   % (who, dig, n, dig, who), dig * pos, "int", {},
                   ["The %d is in the %s place." % (dig, place),
                    "It is worth %d × %d = %d." % (dig, pos, dig * pos)])

    def t_difference():
        (p1, pl1), (p2, pl2) = random.sample(_places(d), 2)
        if p1 < p2:
            p1, pl1, p2, pl2 = p2, pl2, p1, pl1
        dig = random.randint(2, 9)
        others = [x for x in range(1, 10) if x != dig]
        a_digits = {p: pick(others) for p, _pl in _places(d)}
        b_digits = {p: pick(others) for p, _pl in _places(d)}
        a_digits[p1] = dig
        b_digits[p2] = dig
        a = sum(p * a_digits[p] for p, _pl in _places(d))
        b = sum(p * b_digits[p] for p, _pl in _places(d))
        va, vb = dig * p1, dig * p2
        return _tb("The digit %d appears in %d and in %d. How much MORE is it worth in %d?"
                   % (dig, a, b, a), va - vb, "int", {},
                   ["In %d the %d is worth %d; in %d the %d is worth %d." % (a, dig, va, b, dig, vb),
                    "%d − %d = %d." % (va, vb, va - vb)])

    def t_odd_one_out():
        pos, place = pick([p for p in _places(d) if p[0] != 1])
        dig = random.randint(1, 9)
        target = sum(p * (dig if p == pos else pick([x for x in range(0, 10) if x != dig]))
                     for p, _pl in _places(d))
        if target < (100 if d >= 1 else 10):
            target += 100 if d >= 1 else 10
        opts = [target]
        while len(opts) < 4:
            m = _n(d)
            if ((m // pos) % 10) != dig and dig in [int(c) for c in str(m)] and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("In which of these numbers is the digit %d worth %d?   %s"
                   % (dig, dig * pos, _lst(opts)), target, "int", {},
                   ["%d is worth %d only when it sits in the %s place." % (dig, dig * pos, place),
                    "That is %d." % target])

    def t_build_value():
        n = _distinct(d)
        pos, place = pick(_places(d))
        dig = (n // pos) % 10
        return _bt("Build the VALUE of the digit %d in the number %d." % (dig, n), dig * pos,
                   ["The %d is in the %s place, so it is worth %d." % (dig, place, dig * pos)])

    return _pick_t([t_bare, t_named_digit, t_convert_places, t_correct_it, t_difference,
                    t_odd_one_out], [t_build_value])


@skill("Y3.0.g", "Partition a 3-digit number", S0)
def _(d=1):
    d = _d(d)
    n = _n(d)
    h, t, o = n // 100, (n // 10) % 10, n % 10

    def t_missing_part():
        keys = ["h", "t", "o"] if d >= 1 else ["t", "o"]
        parts = {"h": h * 100, "t": t * 10, "o": o}
        miss = pick([k for k in keys if parts[k]] or keys)
        shown = " + ".join("___" if k == miss else str(parts[k]) for k in keys)
        return _tb("Complete the partition:  %d = %s" % (n, shown), parts[miss], "int", {},
                   ["%d = %s." % (n, " + ".join(str(parts[k]) for k in keys))])

    def _expr():
        keys = ["h", "t", "o"] if d >= 1 else ["t", "o"]
        parts = {"h": h * 100, "t": t * 10, "o": o}
        return " + ".join(str(parts[k]) for k in keys if parts[k]) or "0"

    def t_recombine():
        expr = _expr()
        if "+" not in expr:
            return t_missing_part()
        return _tb("Which number is this?   %s" % expr, n, "int", {},
                   ["%s = %d." % (expr, n)])

    def t_expanded():
        expr = _expr()
        if "+" not in expr:
            return t_missing_part()
        return _tb("Convert from expanded form (up to hundreds):  %s = ___" % expr, n, "int", {},
                   ["The expanded form %s is put back together." % expr,
                    "%s = %d." % (expr, n)])

    def t_flexible():
        if d == 0 or h < 2:
            return t_missing_part()
        return _tb("Complete this partition:  %d = %d + ___ + %d" % (n, (h - 1) * 100, o),
                   100 + t * 10, "int", {},
                   ["One hundred has been exchanged for ten tens.",
                    "%d + %d + %d = %d." % ((h - 1) * 100, 100 + t * 10, o, n)])

    def t_two_part():
        if d == 0:
            first = t * 10
            return _tb("Complete:  %d = %d + ___" % (n, first), n - first, "int", {},
                       ["%d − %d = %d." % (n, first, n - first)])
        if n % 100 == 0:
            return t_missing_part()
        first = h * 100
        return _tb("Complete:  %d = %d + ___" % (n, first), n - first, "int", {},
                   ["%d − %d = %d." % (n, first, n - first)])

    def t_build_expr():
        expr = _expr()
        if "+" not in expr:
            return t_build_regroup()
        return _bt("Build the number that is %s." % expr, n, ["%s = %d." % (expr, n)])

    def t_build_regroup():
        hh = random.randint(1, 7) if d >= 1 else 0
        tt = random.randint(10, 15)
        oo = random.randint(0, 9)
        val = hh * 100 + tt * 10 + oo
        who = pick(NAMES)
        desc = ("%s, %s and %s" % (_u(hh, "hundreds"), _u(tt, "tens"), _u(oo, "ones"))) if hh else \
               ("%s and %s" % (_u(tt, "tens"), _u(oo, "ones")))
        return _bt("%s has %s. Build that number with the blocks." % (who, desc), val,
                   ["%d tens is %d, so ten of them make an extra hundred." % (tt, tt * 10),
                    "%s = %d." % (desc.capitalize(), val)])

    return _pick_t([t_missing_part, t_recombine, t_expanded, t_flexible, t_two_part],
                   [t_build_expr, t_build_regroup])


@skill("Y3.0.h", "10 or 100 more or less", S0)
def _(d=1):
    d = _d(d)
    amt = 10 if d == 0 else pick([10, 100])
    n = random.randint(20, 88) if d == 0 else random.randint(120, 880)
    more = random.random() < 0.5

    def t_bare():
        ans = n + amt if more else n - amt
        return _tb("What is %d %s than %d?" % (amt, "more" if more else "less", n),
                   ans, "int", {},
                   ["%d %s %d = %d." % (n, "+" if more else "−", amt, ans)])

    def t_word():
        who = pick(NAMES)
        thing = pick(["stickers", "marbles", "beads", "stamps"])
        ans = n + amt if more else n - amt
        return _tb("%s has %d %s and then %s %d more. How many %s does %s have now?"
                   % (who, n, thing, "collects" if more else "gives away", amt, thing, who)
                   if more else
                   "%s has %d %s and then gives away %d of them. How many %s does %s have left?"
                   % (who, n, thing, amt, thing, who),
                   ans, "int", {"unit": thing},
                   ["%d %s %d = %d." % (n, "+" if more else "−", amt, ans)])

    def t_inverse():
        start = n
        result = start + amt if more else start - amt
        return _tb("%s thought of a number, %s %d and got %d. What was the number?"
                   % (pick(NAMES), "added" if more else "subtracted", amt, result),
                   start, "int", {},
                   ["Do the opposite: %d %s %d = %d." % (result, "−" if more else "+", amt, start)])

    def t_two_step():
        if d < 2:
            return t_bare()
        base = random.randint(220, 780)
        ans = base + 100 - 10
        return _tb("Start at %d. Add 100, then take away 10. What number do you reach?" % base,
                   ans, "int", {},
                   ["%d + 100 = %d." % (base, base + 100),
                    "%d − 10 = %d." % (base + 100, ans)])

    def t_line():
        base = (n // 10) * 10
        ans = base + amt if more else base - amt
        if ans < 0:
            ans = base + amt
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Place the number that is %d %s than %d on the number line."
                   % (amt, "more" if more else "less", base), ans, step, major,
                   ["%d %s %d = %d." % (base, "+" if more else "−", amt, ans)])

    def t_build():
        ans = n + amt if more else n - amt
        return _bt("Build the number that is %d %s than %d." % (amt, "more" if more else "less", n),
                   ans, ["%d %s %d = %d." % (n, "+" if more else "−", amt, ans),
                         "%d = %s." % (ans, _hto(ans))])

    return _pick_t([t_bare, t_word, t_inverse, t_two_step], [t_line, t_build])


@skill("Y3.0.i", "Ordinal numbers and position", S0)
def _(d=1):
    d = _d(d)
    top = {0: 8, 1: 14, 2: 30}[d]

    def t_race():
        pos = random.randint(2, max(3, top - 2))
        total = pos + random.randint(1, 6)
        who = pick(NAMES)
        return _tb("%s finished %s in a race of %d runners. How many runners finished AFTER %s?"
                   % (who, ordinal(pos), total, who), total - pos, "int", {"unit": "runners"},
                   ["%d runners − %d places up to %s = %d after."
                    % (total, pos, ordinal(pos), total - pos)])

    def t_figures():
        n = random.randint(3, 12) if d == 0 else random.randint(11, 99)
        return _tb("Write the ordinal number for position %d (in figures, e.g. 4th)." % n,
                   ordinal(n), "str", {"text": True, "placeholder": "e.g. 4th"},
                   ["Position %d is written %s." % (n, ordinal(n))])

    def t_who():
        k = 5 if d == 0 else 6
        names = random.sample(NAMES, k)
        pos = random.randint(2, k)
        return _tb("The finishing order was: %s. Who finished %s?" % (_lst(names), ordinal(pos)),
                   names[pos - 1], "str", {"text": True, "placeholder": "a name"},
                   ["Counting along the list, %s is %s." % (names[pos - 1], ordinal(pos))])

    def t_from_back():
        total = random.randint(6, top)
        pos = random.randint(2, total - 1)
        who = pick(NAMES)
        return _tb("There are %d children in a queue. %s is %s from the FRONT. What position is %s from the BACK?"
                   % (total, who, ordinal(pos), who), total - pos + 1, "int", {},
                   ["%d − %d = %d %s behind %s."
                    % (total, pos, total - pos, "child is" if total - pos == 1 else "children are", who),
                    "So %s is %s from the back." % (who, ordinal(total - pos + 1))])

    def t_line():
        gap = pick([5, 10])
        k = random.randint(3, 9)
        ans = gap * k
        major = 50 if gap == 5 else 100
        return _nl("Trees are planted every %d metres along a path, the 1st at %d m. "
                   "Place the %s tree on the line." % (gap, gap, ordinal(k)),
                   ans, gap, major,
                   ["%s tree = %d × %d = %d m." % (ordinal(k), k, gap, ans)])

    return _pick_t([t_race, t_figures, t_who, t_from_back], [t_line])


@skill("Y3.0.j", "Even and odd numbers", S0)
def _(d=1):
    d = _d(d)

    def t_bare():
        n = _n(d)
        ans = "even" if n % 2 == 0 else "odd"
        return _tb("Is %d even or odd? (type 'even' or 'odd')" % n, ans, "str",
                   {"text": True, "placeholder": "even / odd"},
                   ["Look at the ones digit (%d)." % (n % 10), "%d is %s." % (n, ans)])

    def t_next():
        n = _n(d)
        want = pick(["even", "odd"])
        m = n + 1
        while (m % 2 == 0) != (want == "even"):
            m += 1
        return _tb("What is the next %s number after %d?" % (want, n), m, "int", {},
                   ["Count on from %d until the ones digit is %s." % (n, want),
                    "The answer is %d." % m])

    def t_before_after():
        n = _n(d)
        want = pick(["even", "odd"])
        after = random.random() < 0.5
        m = n + 1 if after else n - 1
        while (m % 2 == 0) != (want == "even"):
            m = m + 1 if after else m - 1
        return _tb("Which %s number comes just %s %d?" % (want, "after" if after else "before", n),
                   m, "int", {},
                   ["%d is %s." % (n, "even" if n % 2 == 0 else "odd"),
                    "The %s number just %s it is %d." % (want, "after" if after else "before", m)])

    def t_odd_one_out():
        want_odd = random.random() < 0.5
        def gen(is_odd):
            while True:
                m = _n(d)
                if (m % 2 == 1) == is_odd:
                    return m
        target = gen(want_odd)
        opts = [target]
        while len(opts) < 4:
            m = gen(not want_odd)
            if m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Only ONE of these numbers is %s. Which one?   %s"
                   % ("odd" if want_odd else "even", _lst(opts)), target, "int", {},
                   ["Check the ones digit of each number.",
                    "%d is the %s one." % (target, "odd" if want_odd else "even")])

    def t_count():
        opts = []
        while len(opts) < 6:
            m = _n(d)
            if m not in opts:
                opts.append(m)
        cnt = sum(1 for x in opts if x % 2 == 0)
        return _tb("How many of these numbers are EVEN?   %s" % _lst(opts), cnt, "int", {},
                   ["The even ones are: %s." % (_lst([x for x in opts if x % 2 == 0]) or "none"),
                    "That is %d." % cnt])

    def t_share():
        n = _n(d)
        ans = "yes" if n % 2 == 0 else "no"
        return _tb("Can %d sweets be shared equally between 2 children with none left over? "
                   "(type 'yes' or 'no')" % n, ans, "str",
                   {"text": True, "placeholder": "yes / no"},
                   ["%d is %s." % (n, "even" if n % 2 == 0 else "odd"),
                    "So the answer is %s." % ans])

    def t_line():
        n = _n(d)
        if n % 2 == 0:
            n += 1
        ans = n + 1
        return _nl("Place the first EVEN number after %d on the number line." % n, ans, 2, 10,
                   ["%d is odd, so the next even number is %d." % (n, ans)])

    return _pick_t([t_bare, t_next, t_before_after, t_odd_one_out, t_count, t_share], [t_line])


# ------------------------------------------------------------------ 3.1 ------
@skill("Y3.1.a", "Compare 3-digit numbers (<, > or =)", S1)
def _(d=1):
    d = _d(d)

    def two():
        a = _n(d)
        b = a if random.random() < 0.12 else _n(d)
        return a, b

    def t_symbol():
        a, b = two()
        ans = "=" if a == b else (">" if a > b else "<")
        return _tb("Compare:  %d ___ %d   (write <, > or =)" % (a, b), ans, "str",
                   {"text": True, "placeholder": "<, > or ="},
                   ["Compare the hundreds first, then the tens, then the ones.",
                    "%d %s %d." % (a, ans, b)])

    def t_greater():
        a, b = two()
        while a == b:
            b = _n(d)
        big = max(a, b)
        return _tb("Which is greater, %d or %d? Write the greater number." % (a, b), big, "int", {},
                   ["%d is greater than %d." % (big, min(a, b))])

    def t_word():
        a, b = two()
        while a == b:
            b = _n(d)
        n1, n2 = random.sample(NAMES, 2)
        thing = pick(["stickers", "marbles", "points", "stamps"])
        who = n1 if a > b else n2
        return _tb("%s has %d %s and %s has %d %s. Who has more? (write the name)"
                   % (n1, a, thing, n2, b, thing), who, "str",
                   {"text": True, "placeholder": "a name"},
                   ["%d is greater than %d." % (max(a, b), min(a, b)),
                    "So %s has more." % who])

    def t_calc():
        if d == 0:
            a, b = random.randint(10, 40), random.randint(10, 40)
            c = random.randint(20, 80)
        else:
            a, b = random.randint(100, 500), random.randint(10, 300)
            c = random.randint(150, 800)
        left = a + b
        ans = "=" if left == c else (">" if left > c else "<")
        return _tb("Compare:  %d + %d ___ %d   (write <, > or =)" % (a, b, c), ans, "str",
                   {"text": True, "placeholder": "<, > or ="},
                   ["%d + %d = %d." % (a, b, left), "%d %s %d." % (left, ans, c)])

    def t_line():
        a = (_n(d) // 10) * 10
        b = (_n(d) // 10) * 10
        while b == a:
            b = (_n(d) // 10) * 10
        if a < 10:
            a = 10
        if b < 10:
            b = 20
        big = max(a, b)
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Which is greater, %d or %d? Place the GREATER number on the number line."
                   % (a, b), big, step, major,
                   ["%d is greater than %d." % (big, min(a, b))])

    def t_compare_line():
        a = max(10, (_n(d) // 10) * 10)
        b = max(10, (_n(d) // 10) * 10)
        while b == a:
            b = max(10, (_n(d) // 10) * 10)
        smaller = random.random() < 0.5
        ans = min(a, b) if smaller else max(a, b)
        step, major = (10, 50) if d == 0 else (10, 100)
        return _nl("Use the number line to compare these numbers up to 1,000: %d and %d. "
                   "Place the %s number on the number line."
                   % (a, b, "SMALLER" if smaller else "GREATER"), ans, step, major,
                   ["On a number line the smaller number is further to the left.",
                    "%d is greater than %d." % (max(a, b), min(a, b)),
                    "The %s number is %d." % ("smaller" if smaller else "greater", ans)])

    def t_build():
        a, b = two()
        while a == b:
            b = _n(d)
        big = max(a, b)
        return _bt("Build the SMALLER of these two numbers: %d and %d." % (a, b), min(a, b),
                   ["%d is greater than %d." % (big, min(a, b)),
                    "The smaller number is %d." % min(a, b)])

    return _pick_t([t_symbol, t_greater, t_word, t_calc], [t_line, t_compare_line, t_build])


@skill("Y3.1.b", "Order numbers to 1000", S1)
def _(d=1):
    d = _d(d)
    lo, hi = (10, 99) if d == 0 else (20, 990)
    k = 3 if d == 0 else (4 if d == 1 else 5)

    def t_order():
        ns = random.sample(range(lo, hi), k)
        asc = random.random() < 0.5
        order = sorted(ns) if asc else sorted(ns, reverse=True)
        return _tb("Write these in order, %s first:  %s"
                   % ("smallest" if asc else "largest", _lst(ns)), _lst(order), "str",
                   {"text": True, "placeholder": "e.g. 12, 34, 56"},
                   ["In order: %s." % _lst(order)])

    def t_put_in_order():
        ns = random.sample(range(lo, min(hi, 1000)), k)
        asc = random.random() < 0.5
        order = sorted(ns) if asc else sorted(ns, reverse=True)
        return _tb("Put these numbers up to 1,000 in order, from %s:  %s"
                   % ("smallest to largest" if asc else "largest to smallest", _lst(ns)),
                   _lst(order), "str", {"text": True, "placeholder": "e.g. 120, 340, 560"},
                   ["Compare the hundreds first, then the tens, then the ones.",
                    "In order: %s." % _lst(order)])

    def _greatest_least(top):
        names = random.sample(NAMES, 3)
        vals = random.sample(range(5, top), 3)
        thing = pick(["stickers", "marbles", "stamps", "conkers", "points"])
        greatest = random.random() < 0.5
        best = max(vals) if greatest else min(vals)
        who = names[vals.index(best)]
        pairs = "%s has %d %s, %s has %d and %s has %d" % (
            names[0], vals[0], thing, names[1], vals[1], names[2], vals[2])
        return _tb("%s. All the numbers are up to %s. Who has the %s number of %s? "
                   "(write the name)"
                   % (pairs, "1,000" if top > 100 else "100",
                      "greatest" if greatest else "least", thing),
                   who, "str", {"text": True, "placeholder": "a name"},
                   ["In order: %s." % _lst(sorted(vals)),
                    "The %s is %d, so %s." % ("greatest" if greatest else "least", best, who)])

    def t_gl_100():
        return _greatest_least(100)

    def t_gl_1000():
        return _greatest_least(1000)

    def t_extreme():
        ns = random.sample(range(lo, hi), k + 1)
        big = random.random() < 0.5
        ans = max(ns) if big else min(ns)
        return _tb("Which is the %s of these numbers?   %s"
                   % ("largest" if big else "smallest", _lst(ns)), ans, "int", {},
                   ["In order: %s." % _lst(sorted(ns)), "The %s is %d." % ("largest" if big else "smallest", ans)])

    def t_between():
        a = random.randint(lo, hi - 120 if d >= 1 else hi - 30)
        b = a + (random.randint(30, 90) if d >= 1 else random.randint(10, 25))
        target = random.randint(a + 1, b - 1)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(lo, hi)
            if not (a < m < b) and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers lies BETWEEN %d and %d?   %s" % (a, b, _lst(opts)),
                   target, "int", {},
                   ["%d is bigger than %d and smaller than %d." % (target, a, b)])

    def t_word():
        names = random.sample(NAMES, 3)
        scores = random.sample(range(lo, hi), 3)
        order = sorted(zip(scores, names), reverse=True)
        pos = random.randint(1, 3)
        pairs = ", ".join("%s %d" % (nm, sc) for sc, nm in zip(scores, names))
        return _tb("Points scored:  %s. Who came %s (highest points first)? (write the name)"
                   % (pairs, ordinal(pos)), order[pos - 1][1], "str",
                   {"text": True, "placeholder": "a name"},
                   ["Highest to lowest: %s." % ", ".join("%s %d" % (nm, sc) for sc, nm in order),
                    "%s came %s." % (order[pos - 1][1], ordinal(pos))])

    def t_line():
        ns = sorted(random.sample(range(lo // 10 + 1, hi // 10), k))
        ns = [x * 10 for x in ns]
        idx = 1 if k <= 3 else random.randint(1, k - 2)
        ans = ns[idx]
        step, major = (10, 50) if d == 0 else (10, 100)
        shuffled = ns[:]
        random.shuffle(shuffled)
        return _nl("Here are %d numbers: %s. Place the %s SMALLEST one on the number line."
                   % (k, _lst(shuffled), ordinal(idx + 1)), ans, step, major,
                   ["In order: %s." % _lst(ns), "The %s smallest is %d." % (ordinal(idx + 1), ans)])

    def t_order_line():
        ns = sorted(random.sample(range(lo // 10 + 1, hi // 10), k))
        ns = [x * 10 for x in ns]
        idx = 1 if k <= 3 else random.randint(1, k - 2)
        ans = ns[idx]
        step, major = (10, 50) if d == 0 else (10, 100)
        shuffled = ns[:]
        random.shuffle(shuffled)
        return _nl("Put these numbers up to 1,000 in order using the number line:  %s. "
                   "Place the %s SMALLEST number on the line." % (_lst(shuffled), ordinal(idx + 1)),
                   ans, step, major,
                   ["On a number line, numbers get bigger as you move to the right.",
                    "In order: %s." % _lst(ns),
                    "The %s smallest is %d." % (ordinal(idx + 1), ans)])

    def t_build():
        ns = random.sample(range(lo, hi), k)
        big = random.random() < 0.5
        ans = max(ns) if big else min(ns)
        return _bt("Build the %s of these numbers: %s."
                   % ("largest" if big else "smallest", _lst(ns)), ans,
                   ["In order: %s." % _lst(sorted(ns)), "The answer is %d." % ans])

    return _pick_t([t_order, t_put_in_order, t_gl_100, t_gl_1000, t_extreme, t_between, t_word],
                   [t_line, t_order_line, t_build])


@skill("Y3.1.c", "Round to the nearest 10", S1)
def _(d=1):
    d = _d(d)
    lo, hi = {0: (11, 99), 1: (101, 989), 2: (101, 989)}[d]

    def num():
        if d == 2 and random.random() < 0.4:
            return random.randint(lo // 10, hi // 10) * 10 + 5   # exact halfway
        n = random.randint(lo, hi)
        return n if n % 10 else n + random.randint(1, 9)

    def t_bare():
        n = num()
        return _tb("Round %d to the nearest 10." % n, _r10(n), "int", {},
                   ["The ones digit is %d." % (n % 10),
                    "%d rounds to %d." % (n, _r10(n))])

    def t_word():
        n = num()
        who = pick(NAMES)
        thing = pick(["beads", "stickers", "coins", "sunflower seeds"])
        return _tb("%s counted %d %s. Round that to the nearest 10." % (who, n, thing),
                   _r10(n), "int", {"unit": thing},
                   ["The ones digit is %d." % (n % 10),
                    "%d rounds to %d." % (n, _r10(n))])

    def t_inverse():
        r = random.randint(lo // 10 + 1, hi // 10) * 10
        smallest = random.random() < 0.5
        ans = r - 5 if smallest else r + 4
        return _tb("A whole number rounds to %d when rounded to the nearest 10. "
                   "What is the %s it could be?" % (r, "SMALLEST" if smallest else "LARGEST"),
                   ans, "int", {},
                   ["Numbers from %d to %d all round to %d." % (r - 5, r + 4, r),
                    "The %s is %d." % ("smallest" if smallest else "largest", ans)])

    def t_odd_one_out():
        r = random.randint(lo // 10 + 1, hi // 10 - 1) * 10
        target = random.randint(r - 5, r + 4)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(lo, hi)
            if _r10(m) != r and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers rounds to %d (nearest 10)?   %s" % (r, _lst(opts)),
                   target, "int", {},
                   ["Only %d is between %d and %d." % (target, r - 5, r + 4),
                    "%d rounds to %d." % (target, r)])

    def t_line():
        n = num()
        ans = _r10(n)
        return _nl("Round %d to the nearest 10 and place your answer on the number line." % n,
                   ans, 10, 50,
                   ["The ones digit is %d." % (n % 10), "%d rounds to %d." % (n, ans)])

    def t_build():
        n = num()
        ans = _r10(n)
        return _bt("Round %d to the nearest 10, then build your answer with the blocks." % n, ans,
                   ["The ones digit is %d." % (n % 10), "%d rounds to %d." % (n, ans)])

    return _pick_t([t_bare, t_word, t_inverse, t_odd_one_out], [t_line, t_build])


@skill("Y3.1.d", "Round to the nearest 100", S1)
def _(d=1):
    d = _d(d)
    lo, hi = {0: (110, 590), 1: (110, 979), 2: (110, 979)}[d]

    def num():
        if d == 2 and random.random() < 0.4:
            return random.randint(lo // 100, (hi - 50) // 100) * 100 + 50   # exact halfway
        n = random.randint(lo, hi)
        return n if n % 100 else n + random.randint(1, 49)

    def t_bare():
        n = num()
        return _tb("Round %d to the nearest 100." % n, _r100(n), "int", {},
                   ["The tens digit is %d." % ((n // 10) % 10),
                    "%d rounds to %d." % (n, _r100(n))])

    def t_word():
        n = num()
        who = pick(NAMES)
        return _tb("%s's school has %d books. Round that to the nearest 100." % (who, n),
                   _r100(n), "int", {"unit": "books"},
                   ["The tens digit is %d." % ((n // 10) % 10),
                    "%d rounds to %d." % (n, _r100(n))])

    def t_inverse():
        r = random.randint(2, hi // 100) * 100
        smallest = random.random() < 0.5
        ans = r - 50 if smallest else r + 49
        return _tb("A whole number rounds to %d when rounded to the nearest 100. "
                   "What is the %s it could be?" % (r, "SMALLEST" if smallest else "LARGEST"),
                   ans, "int", {},
                   ["Numbers from %d to %d all round to %d." % (r - 50, r + 49, r),
                    "The %s is %d." % ("smallest" if smallest else "largest", ans)])

    def t_odd_one_out():
        r = random.randint(2, hi // 100) * 100
        target = random.randint(r - 50, r + 49)
        opts = [target]
        while len(opts) < 4:
            m = random.randint(lo, hi)
            if _r100(m) != r and m not in opts:
                opts.append(m)
        random.shuffle(opts)
        return _tb("Which of these numbers rounds to %d (nearest 100)?   %s" % (r, _lst(opts)),
                   target, "int", {},
                   ["Only %d is between %d and %d." % (target, r - 50, r + 49),
                    "%d rounds to %d." % (target, r)])

    def t_line():
        n = num()
        ans = _r100(n)
        return _nl("Round %d to the nearest 100 and place your answer on the number line." % n,
                   ans, 100, 100,
                   ["The tens digit is %d." % ((n // 10) % 10), "%d rounds to %d." % (n, ans)])

    def t_build():
        n = num()
        while _r100(n) > 900:          # the blocks only go up to 9 hundreds
            n = num()
        ans = _r100(n)
        return _bt("Round %d to the nearest 100, then build your answer with the blocks." % n, ans,
                   ["The tens digit is %d." % ((n // 10) % 10), "%d rounds to %d." % (n, ans)])

    return _pick_t([t_bare, t_word, t_inverse, t_odd_one_out], [t_line, t_build])


@skill("Y3.1.e", "Estimate by rounding", S1)
def _(d=1):
    d = _d(d)
    to10 = (d == 0)
    rnd = _r10 if to10 else _r100
    unit = 10 if to10 else 100

    def pair():
        if to10:
            return random.randint(12, 89), random.randint(12, 89)
        return random.randint(110, 440), random.randint(110, 440)

    def t_add():
        a, b = pair()
        ra, rb = rnd(a), rnd(b)
        return _tb("Estimate %d + %d by rounding each number to the nearest %d." % (a, b, unit),
                   ra + rb, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, ra, b, rb),
                    "%d + %d = %d." % (ra, rb, ra + rb)])

    def t_sub():
        a, b = pair()
        if a < b:
            a, b = b, a
        ra, rb = rnd(a), rnd(b)
        return _tb("Estimate %d − %d by rounding each number to the nearest %d." % (a, b, unit),
                   ra - rb, "int", {},
                   ["%d ≈ %d and %d ≈ %d." % (a, ra, b, rb),
                    "%d − %d = %d." % (ra, rb, ra - rb)])

    def t_word():
        a, b = pair()
        n1, n2 = random.sample(NAMES, 2)
        thing = pick(["stickers", "beads", "stamps"])
        ra, rb = rnd(a), rnd(b)
        return _tb("%s has %d %s and %s has %d %s. Estimate the total by rounding "
                   "each number to the nearest %d." % (n1, a, thing, n2, b, thing, unit),
                   ra + rb, "int", {"unit": thing},
                   ["%d ≈ %d and %d ≈ %d." % (a, ra, b, rb),
                    "About %d altogether." % (ra + rb)])

    def t_three():
        if d < 2:
            return t_add()
        a, b, c = random.randint(110, 320), random.randint(110, 320), random.randint(110, 320)
        ra, rb, rc = rnd(a), rnd(b), rnd(c)
        return _tb("Estimate %d + %d + %d by rounding each number to the nearest 100." % (a, b, c),
                   ra + rb + rc, "int", {},
                   ["%d ≈ %d, %d ≈ %d, %d ≈ %d." % (a, ra, b, rb, c, rc),
                    "%d + %d + %d = %d." % (ra, rb, rc, ra + rb + rc)])

    def t_line():
        a, b = pair()
        ra, rb = rnd(a), rnd(b)
        ans = ra + rb
        step, major = (10, 50) if to10 else (100, 100)
        return _nl("Estimate %d + %d by rounding to the nearest %d, then place your "
                   "estimate on the number line." % (a, b, unit), ans, step, major,
                   ["%d ≈ %d and %d ≈ %d." % (a, ra, b, rb),
                    "The estimate is %d." % ans])

    def t_build():
        a, b = pair()
        ra, rb = rnd(a), rnd(b)
        ans = ra + rb
        return _bt("Estimate %d + %d by rounding to the nearest %d, then build your estimate."
                   % (a, b, unit), ans,
                   ["%d ≈ %d and %d ≈ %d." % (a, ra, b, rb),
                    "The estimate is %d." % ans])

    return _pick_t([t_add, t_sub, t_word, t_three], [t_line, t_build])


@skill("Y3.1.f", "Continue a number sequence", S1)
def _(d=1):
    d = _d(d)
    steps = {0: [2, 5, 10], 1: [3, 4, 5, 8, 10, 25], 2: [6, 7, 9, 25, 50]}[d]
    step = pick(steps)
    start = random.randint(3, 20) * step

    def terms_of(back, count=4):
        sg = -step if back else step
        return [start + i * sg for i in range(count)]

    def t_next_two():
        back = d >= 1 and random.random() < 0.35
        ts = terms_of(back)
        nxt = [ts[-1] + (i + 1) * (-step if back else step) for i in range(2)]
        if min(ts + nxt) < 0:
            back = False
            ts = terms_of(False)
            nxt = [ts[-1] + (i + 1) * step for i in range(2)]
        return _tb("Continue the sequence — write the next two numbers:  %s, ___, ___" % _lst(ts),
                   _lst(nxt), "str", {"text": True, "placeholder": "e.g. 20, 24"},
                   ["The rule is %s %d each time." % ("subtract" if back else "add", step),
                    "The next two are %s." % _lst(nxt)])

    def t_next_one():
        ts = terms_of(False)
        nxt = ts[-1] + step
        return _tb("What is the next number in this sequence?   %s, ___" % _lst(ts),
                   nxt, "int", {},
                   ["The sequence goes up in %ds." % step,
                    "%d + %d = %d." % (ts[-1], step, nxt)])

    def t_pattern_1000():
        st = pick([2, 5, 10, 25, 50, 100] if d >= 1 else [2, 5, 10])
        top = max(2, (1000 - 4 * st) // st)
        s = random.randint(2, top) * st
        ts = [s + i * st for i in range(4)]
        ans = ts[-1] + st
        return _tb("Here is a counting pattern with numbers up to 1,000:  %s, ___  "
                   "Continue the pattern — what number comes next?" % _lst(ts),
                   ans, "int", {},
                   ["The counting pattern goes up in %ds." % st,
                    "%d + %d = %d." % (ts[-1], st, ans)])

    def t_rule():
        ts = terms_of(random.random() < 0.4 and start - 3 * step >= 0)
        return _tb("These numbers follow a rule:  %s. How much does the sequence change "
                   "by each time? (write the size of the step)" % _lst(ts),
                   step, "int", {},
                   ["%d %s %d = %d." % (ts[0], "−" if ts[1] < ts[0] else "+", step, ts[1]),
                    "The step is %d." % step])

    def t_word():
        who = pick(NAMES)
        k = random.randint(4, 6)
        ts = [start + i * step for i in range(3)]
        ans = start + (k - 1) * step
        return _tb("%s builds a pattern. Row 1 has %d tiles, row 2 has %d, row 3 has %d, "
                   "and the pattern carries on in the same way. How many tiles are in row %d?"
                   % (who, ts[0], ts[1], ts[2], k), ans, "int", {"unit": "tiles"},
                   ["Each row adds %d tiles." % step,
                    "Row %d = %d + %d × %d = %d." % (k, start, k - 1, step, ans)])

    def t_back():
        big = random.randint(6, 14) * step
        ts = [big - i * step for i in range(4)]
        nxt = [ts[-1] - step, ts[-1] - 2 * step]
        return _tb("This sequence counts backwards. Write the next two numbers:  %s, ___, ___"
                   % _lst(ts), _lst(nxt), "str", {"text": True, "placeholder": "e.g. 20, 16"},
                   ["The rule is subtract %d each time." % step,
                    "The next two are %s." % _lst(nxt)])

    def t_line():
        st = pick([5, 10, 25, 50])
        major = {5: 50, 10: 100, 25: 100, 50: 200}[st]
        s = random.randint(2, 8) * st
        ts = [s + i * st for i in range(4)]
        ans = ts[-1] + st
        return _nl("Continue the sequence %s, ... and place the NEXT number on the number line."
                   % _lst(ts), ans, st, major,
                   ["The sequence goes up in %ds." % st,
                    "%d + %d = %d." % (ts[-1], st, ans)])

    return _pick_t([t_next_two, t_next_one, t_pattern_1000, t_rule, t_word, t_back], [t_line])


@skill("Y3.1.g", "Find the missing number in a sequence", S1)
def _(d=1):
    d = _d(d)
    steps = {0: [2, 5, 10], 1: [3, 4, 5, 8, 10, 50], 2: [6, 7, 9, 25, 50, 100]}[d]
    step = pick(steps)
    start = random.randint(3, 15) * step
    terms = [start + i * step for i in range(5)]

    def t_one():
        idx = random.randint(1, 3)
        shown = ", ".join("___" if i == idx else str(t) for i, t in enumerate(terms))
        return _tb("Find the missing number:  %s" % shown, terms[idx], "int", {},
                   ["The sequence goes up in %ds." % step,
                    "%d + %d = %d." % (terms[idx - 1], step, terms[idx])])

    def t_two():
        i1, i2 = sorted(random.sample([1, 2, 3], 2))
        shown = ", ".join("___" if i in (i1, i2) else str(t) for i, t in enumerate(terms))
        ans = "%d, %d" % (terms[i1], terms[i2])
        return _tb("Two numbers are missing. Write them in order, left to right:  %s" % shown,
                   ans, "str", {"text": True, "placeholder": "e.g. 12, 20"},
                   ["The sequence goes up in %ds." % step,
                    "The missing numbers are %s." % ans])

    def t_first():
        shown = ", ".join(["___"] + [str(t) for t in terms[1:]])
        return _tb("Find the missing FIRST number:  %s" % shown, terms[0], "int", {},
                   ["Count back %d from %d." % (step, terms[1]),
                    "%d − %d = %d." % (terms[1], step, terms[0])])

    def t_word():
        who = pick(NAMES)
        idx = random.randint(1, 3)
        shown = ", ".join("?" if i == idx else str(t) for i, t in enumerate(terms))
        return _tb("%s wrote a counting pattern but one number smudged:  %s. "
                   "What was the smudged number?" % (who, shown), terms[idx], "int", {},
                   ["The pattern counts on in %ds." % step,
                    "The smudged number is %d." % terms[idx]])

    def t_line():
        st = pick([5, 10, 25, 50])
        major = {5: 50, 10: 100, 25: 100, 50: 200}[st]
        s = random.randint(2, 8) * st
        ts = [s + i * st for i in range(5)]
        idx = random.randint(1, 3)
        shown = ", ".join("___" if i == idx else str(t) for i, t in enumerate(ts))
        return _nl("Find the missing number and place it on the number line:  %s" % shown,
                   ts[idx], st, major,
                   ["The sequence goes up in %ds." % st,
                    "%d + %d = %d." % (ts[idx - 1], st, ts[idx])])

    def t_build():
        st = pick([2, 5, 10] if d == 0 else [3, 4, 5, 10, 50])
        s = random.randint(3, 10) * st
        ts = [s + i * st for i in range(5)]
        if ts[-1] > 999:
            s = st * 3
            ts = [s + i * st for i in range(5)]
        idx = random.randint(1, 3)
        shown = ", ".join("___" if i == idx else str(t) for i, t in enumerate(ts))
        return _bt("Find the missing number, then build it with the blocks:  %s" % shown,
                   ts[idx],
                   ["The sequence goes up in %ds." % st,
                    "%d + %d = %d." % (ts[idx - 1], st, ts[idx])])

    return _pick_t([t_one, t_two, t_first, t_word], [t_line, t_build])
