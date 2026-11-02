# Year 5 generators: strands 5.0 and 5.1 (National Curriculum, Year 5 number & place value).
#
# Numbers to 1,000,000; counting in powers of 10; negative numbers in context and through zero;
# Roman numerals to M and years; comparing, ordering, rounding to 100,000 and estimating.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S0 = "5.0 Number & place value"
S1 = "5.1 Compare, order, round & estimate"

PLACES = [(100000, "hundred thousands"), (10000, "ten thousands"), (1000, "thousands"),
          (100, "hundreds"), (10, "tens"), (1, "ones")]


def _six(d):
    """A number of the right size: 5 digits at d=0, 6 digits above (stretch adds zeros)."""
    if d == 0:
        return random.randint(10001, 99999)
    if d == 1:
        return random.randint(100001, 999999)
    digits = [random.randint(1, 9)] + [pick([0, 0, random.randint(0, 9)]) for _ in range(5)]
    return int("".join(map(str, digits)))


def _digit_at(n, place):
    return (n // place) % 10


# ================================================================== 5.0 ======
@skill("Y5.0.a", "Read and write numbers to 1,000,000", S0)
def _(d=1):
    d = _d(d)
    n = _six(d)

    def t_to_numeral():
        return _tb("Write this number in numerals: '%s'" % _words(n), n, "int", {},
                   ["'%s' is %s." % (_words(n), _c(n))])

    def t_to_words():
        return _wq("Write %s in words." % _c(n), _words(n),
                   ["%s is '%s'." % (_c(n), _words(n))], "number in words")

    def t_context():
        place, what = pick([("the stadium", "people"), ("the city library", "books"),
                            ("the charity appeal", "pounds"), ("the website", "visitors")])
        return _tb("A news report says '%s %s' came to %s. Write that number in numerals."
                   % (_words(n).capitalize(), what, place), n, "int", {},
                   ["Read each part: %s." % _c(n)])

    def t_zero_trap():
        th = random.randint(1, 9) * pick([1, 10, 100]) if d else random.randint(11, 99)
        th = min(th, 999)
        rest = pick([random.randint(1, 9), random.randint(10, 99), random.randint(1, 9) * 100])
        m = th * 1000 + rest
        return _tb("Read carefully and write in numerals: '%s'" % _words(m), m, "int", {},
                   ["Empty places are written as zeros.", "'%s' is %s." % (_words(m), _c(m))])

    def t_table():
        nums = random.sample(range(100001 if d else 10001, 999999 if d else 99999), 4)
        k = random.randrange(4)
        rows = [[_words(x), _c(x)] for x in nums]
        return _dt("This table shows numbers in words and in numerals. What numeral belongs in the "
                   "empty cell?", ["In words", "In numerals"], rows, nums[k],
                   ["'%s' is %s." % (_words(nums[k]), _c(nums[k]))], missing=[k, 1])

    def t_digits_count():
        return _tb("How many digits does the numeral for '%s' have?" % _words(n), len(str(n)), "int",
                   {}, ["%s has %d digits." % (_c(n), len(str(n)))])

    def t_million():
        k = random.randint(1, 9)
        m = 1_000_000 - k * pick([1, 10, 100, 1000])
        return _tb("Write in numerals: '%s'" % _words(m), m, "int", {},
                   ["%s is %s less than one million." % (_c(m), _c(1_000_000 - m))])

    return _pick_t([t_to_numeral, t_to_words, t_context, t_zero_trap, t_digits_count, t_million],
                   [t_table])


@skill("Y5.0.b", "Value of each digit in numbers to 1,000,000", S0)
def _(d=1):
    d = _d(d)
    n = _six(d)
    places = [p for p in PLACES if p[0] <= n]
    nz = [p for p in places if _digit_at(n, p[0])]

    def t_value():
        p, name = pick(nz)
        dg = _digit_at(n, p)
        return _tb("What is the value of the digit %d in %s?" % (dg, _c(n)), dg * p, "int", {},
                   ["The %d is in the %s place." % (dg, name), "Its value is %s." % _c(dg * p)])

    def t_which_place():
        p, name = pick(nz)
        dg = _digit_at(n, p)
        if sum(1 for q, _ in places if _digit_at(n, q) == dg) > 1:
            return t_value()
        return _wq("In %s, which place is the digit %d in? (for example: ten thousands)"
                   % (_c(n), dg), name, ["%d stands for %s." % (dg, _c(dg * p))], "place name")

    def t_partition():
        parts = [_digit_at(n, p) * p for p, _ in places if _digit_at(n, p)]
        if len(parts) < 3:
            return t_value()
        k = random.randrange(len(parts))
        shown = " + ".join("___" if i == k else _c(x) for i, x in enumerate(parts))
        return _tb("Complete:  %s = %s" % (_c(n), shown), parts[k], "int", {},
                   ["%s = %s." % (_c(n), " + ".join(_c(x) for x in parts))])

    def t_build():
        parts = [_digit_at(n, p) * p for p, _ in places if _digit_at(n, p)]
        if len(parts) < 3:
            return t_value()
        random.shuffle(parts)
        return _tb("Which number is  %s ?" % " + ".join(_c(x) for x in parts), n, "int", {},
                   ["Put each part in its place: %s." % _c(n)])

    def t_change():
        p, name = pick(nz)
        dg = _digit_at(n, p)
        new = random.choice([x for x in range(10) if x != dg])
        m = n + (new - dg) * p
        return _tb("The %s digit of %s is changed from %d to %d. By how much does the number %s?"
                   % (name, _c(n), dg, new,
                      "increase" if new > dg else "decrease"),
                   abs(new - dg) * p, "int", {},
                   ["%s → %s." % (_c(n), _c(m)), "The change is %s." % _c(abs(new - dg) * p)])

    def t_how_many():
        p, name = pick([(1000, "thousands"), (10000, "ten thousands"), (100, "hundreds")])
        return _tb("How many WHOLE %s are there in %s?" % (name, _c(n)), n // p, "int", {},
                   ["%s ÷ %s = %s remainder %s." % (_c(n), _c(p), _c(n // p), _c(n % p))])

    def t_table():
        parts = [[name, _c(_digit_at(n, p) * p)] for p, name in places]
        k = random.choice([i for i, (p, _) in enumerate(places) if _digit_at(n, p)])
        return _dt("This table splits %s into the value of each digit. What belongs in the empty "
                   "cell?" % _c(n), ["Place", "Value"], parts,
                   _digit_at(n, places[k][0]) * places[k][0],
                   ["The %s digit is %d." % (places[k][1], _digit_at(n, places[k][0]))],
                   missing=[k, 1])

    return _pick_t([t_value, t_which_place, t_partition, t_build, t_change, t_how_many], [t_table])


@skill("Y5.0.c", "Count forwards and backwards in powers of 10", S0)
def _(d=1):
    d = _d(d)
    step = pick(_by(d, [10, 100, 1000], [100, 1000, 10000], [1000, 10000, 100000]))
    base = random.randint(_by(d, 1000, 20000, 100000), _by(d, 90000, 700000, 800000))
    back = random.random() < 0.45 and base - 9 * step >= 0

    def seq(k=5):
        sg = -step if back else step
        return [base + i * sg for i in range(k)]

    def t_next():
        s = seq(4)
        nxt = s[-1] + (-step if back else step)
        return _tb("Count %s in %ss: %s, ___  What comes next?"
                   % ("back" if back else "on", _c(step), ", ".join(_c(x) for x in s)), nxt, "int",
                   {}, ["%s %s each time." % ("Subtract" if back else "Add", _c(step))])

    def t_missing():
        s = seq(5)
        k = random.randint(1, 3)
        shown = ", ".join("___" if i == k else _c(x) for i, x in enumerate(s))
        return _tb("Find the missing number: %s" % shown, s[k], "int", {},
                   ["The numbers go %s in %ss." % ("down" if back else "up", _c(step))])

    def t_jumps():
        k = random.randint(3, 8)
        ans = base + (-1 if back else 1) * k * step
        return _tb("Start at %s and count %s %d jumps of %s. Where do you land?"
                   % (_c(base), "back" if back else "on", k, _c(step)), ans, "int", {},
                   ["%d × %s = %s." % (k, _c(step), _c(k * step)),
                    "%s %s %s = %s." % (_c(base), "−" if back else "+", _c(k * step), _c(ans))])

    def t_step():
        s = seq(4)
        return _tb("What is the step in this sequence? %s" % ", ".join(_c(x) for x in s), step, "int",
                   {}, ["Each number is %s %s." % (_c(step), "less" if back else "more")])

    def t_cross():
        # crossing a boundary changes more than one digit
        b = (base // (step * 10) + 1) * step * 10 - step * random.randint(1, 2)
        ans = b + 3 * step
        return _tb("Count on 3 lots of %s from %s." % (_c(step), _c(b)), ans, "int", {},
                   ["%s + %s = %s." % (_c(b), _c(3 * step), _c(ans))])

    def t_table():
        s = seq(5)
        k = random.randint(1, 4)
        return _io("Each row counts %s by %s. What goes in the empty cell?"
                   % ("back" if back else "on", _c(step)),
                   [[i + 1, s[i]] for i in range(5)], k, s[k],
                   ["%s %s %s = %s." % (_c(s[k - 1]), "−" if back else "+", _c(step), _c(s[k]))],
                   rule=("− " if back else "+ ") + _c(step))

    return _pick_t([t_next, t_missing, t_jumps, t_step, t_cross], [t_table])


@skill("Y5.0.d", "10, 100, 1000, 10,000 or 100,000 more or less", S0)
def _(d=1):
    d = _d(d)
    n = _six(d)
    step = pick(_by(d, [10, 100, 1000], [1000, 10000, 100000], [10000, 100000, 1000, 100]))
    if n <= step:
        n += step
    more = random.random() < 0.5

    def t_plain():
        ans = n + step if more else n - step
        return _tb("What is %s %s than %s?" % (_c(step), "more" if more else "less", _c(n)), ans,
                   "int", {}, ["Only the %s digit changes (with any exchange)." % _c(step),
                               "%s %s %s = %s." % (_c(n), "+" if more else "−", _c(step), _c(ans))])

    def t_inverse():
        ans = n - step if more else n + step
        return _tb("%s is %s %s than a number. What is the number?"
                   % (_c(n), _c(step), "more" if more else "less"), ans, "int", {},
                   ["Do the opposite: %s %s %s = %s." % (_c(n), "−" if more else "+", _c(step),
                                                          _c(ans))])

    def t_how_much():
        m = n + step if more else n - step
        return _tb("How much %s is %s than %s?" % ("more" if more else "less", _c(m), _c(n)), step,
                   "int", {}, ["The difference is %s." % _c(step)])

    def t_word():
        who = _who()
        ans = n + step if more else n - step
        return _tb("A town had %s people. %s years later it had %s %s. How many people did it have "
                   "then?" % (_c(n), pick(["Ten", "Twenty", "Fifty"]), _c(step),
                              "more" if more else "fewer"), ans, "int", {},
                   ["%s %s %s = %s." % (_c(n), "+" if more else "−", _c(step), _c(ans))])

    def t_boundary():
        b = (n // (step * 10)) * step * 10 + 9 * step + random.randint(0, step - 1)
        if b >= 1_000_000 - step:
            b -= 10 * step
        return _tb("What is %s more than %s?" % (_c(step), _c(b)), b + step, "int", {},
                   ["Adding %s changes more than one digit here." % _c(step),
                    "%s + %s = %s." % (_c(b), _c(step), _c(b + step))])

    def t_table():
        nums = random.sample(range(step + 1000, 890000), 3)
        rows = [[_c(x - step), _c(x), _c(x + step)] for x in nums]
        r, c = random.randrange(3), pick([0, 2])
        ans = nums[r] - step if c == 0 else nums[r] + step
        return _dt("Complete the table. What number belongs in the empty cell?",
                   ["%s less" % _c(step), "Number", "%s more" % _c(step)], rows, ans,
                   ["%s %s %s = %s." % (_c(nums[r]), "−" if c == 0 else "+", _c(step), _c(ans))],
                   missing=[r, c])

    return _pick_t([t_plain, t_inverse, t_how_much, t_word, t_boundary], [t_table])


@skill("Y5.0.e", "Negative numbers in context", S0)
def _(d=1):
    d = _d(d)

    def t_rise():
        a = -random.randint(1, _by(d, 6, 12, 20))
        r = random.randint(2, _by(d, 10, 18, 30))
        return _tb("At 6 am the temperature was %d °C. By noon it had risen by %d degrees. What "
                   "was the temperature at noon, in °C?" % (a, r), a + r, "int", {"unit": "°C"},
                   ["%d + %d = %d." % (a, r, a + r)])

    def t_fall():
        a = random.randint(1, _by(d, 8, 12, 15))
        f = a + random.randint(1, _by(d, 6, 10, 18))
        return _tb("The temperature was %d °C and then fell by %d degrees. What is the "
                   "temperature now, in °C?" % (a, f), a - f, "int", {"unit": "°C"},
                   ["%d − %d = %d." % (a, f, a - f)])

    def t_difference():
        a = -random.randint(1, _by(d, 8, 15, 25))
        b = random.randint(1, _by(d, 8, 15, 25))
        c1, c2 = random.sample(["Oslo", "Cardiff", "Moscow", "Rome", "Belfast", "Madrid"], 2)
        return _tb("At midnight it was %d °C in %s and %d °C in %s. What is the difference "
                   "between the two temperatures, in degrees?" % (a, c1, b, c2), b - a, "int",
                   {"unit": "degrees"}, ["From %d up to 0 is %d; from 0 up to %d is %d." % (a, -a, b, b),
                                         "%d + %d = %d." % (-a, b, b - a)])

    def t_coldest():
        temps = random.sample(range(-15, 12), 4)
        towns = random.sample(["Leeds", "York", "Perth", "Dover", "Bath", "Hull"], 4)
        rows = [[t, "%d °C" % v] for t, v in zip(towns, temps)]
        k = temps.index(min(temps))
        return _dt("The table shows night temperatures. Which town was the coldest? Type its "
                   "temperature.", ["Town", "Temperature"], rows, min(temps),
                   ["The lowest number is the coldest: %d °C in %s." % (min(temps), towns[k])])

    def t_sea():
        dive = random.randint(5, _by(d, 20, 40, 80))
        up = random.randint(2, dive - 1)
        return _tb("A diver is %d m below sea level, written −%d m. The diver swims up %d m. What is the "
                   "new position? (use a minus sign for below sea level)" % (dive, dive, up),
                   up - dive, "int", {"unit": "m"}, ["−%d + %d = %d." % (dive, up, up - dive)])

    def t_lift():
        f = -random.randint(1, 3)
        up = random.randint(2, 9)
        return _tb("In a building, floor 0 is the ground floor and the basements are floors −1, "
                   "−2 and −3. A lift starts on floor %d and goes up %d floors. Which floor does it "
                   "reach?" % (f, up), f + up, "int", {}, ["%d + %d = %d." % (f, up, f + up)])

    def t_graph():
        hours = ["2 am", "4 am", "6 am", "8 am", "10 am"]
        vals = sorted(random.sample(range(-8, 7), 5))
        k = random.randrange(5)
        return _lg("Overnight temperature. Use the graph. What was the temperature at %s, in °C?"
                   % hours[k], list(zip(hours, vals)), vals[k],
                   ["Read across from the point at %s: %d °C." % (hours[k], vals[k])], "°C", "Time")

    def t_line():
        a = random.randint(-9, -1)
        r = random.randint(3, 12)
        return _nl("The temperature is %d °C and rises by %d degrees. Mark the new temperature on "
                   "the line." % (a, r), a + r, 1, 5, ["%d + %d = %d." % (a, r, a + r)],
                   lo=-10, hi=15)

    return _pick_t([t_rise, t_fall, t_difference, t_sea, t_lift], [t_coldest, t_graph, t_line])


@skill("Y5.0.f", "Count forwards and backwards through zero", S0)
def _(d=1):
    d = _d(d)
    step = pick(_by(d, [1, 2, 5], [2, 3, 5, 10], [3, 4, 6, 25, 50]))

    def t_back():
        start = step * random.randint(1, 3) + (0 if d == 0 else pick([0, 1]))
        s = [start - i * step for i in range(4)]
        return _tb("Count back in %ss: %s, ___  What comes next?" % (step, ", ".join(map(str, s))),
                   s[-1] - step, "int", {}, ["%d − %d = %d." % (s[-1], step, s[-1] - step)])

    def t_on():
        start = -step * random.randint(3, 5) - (0 if d == 0 else pick([0, 1]))
        s = [start + i * step for i in range(4)]
        return _tb("Count on in %ss: %s, ___  What comes next?" % (step, ", ".join(map(str, s))),
                   s[-1] + step, "int", {}, ["%d + %d = %d." % (s[-1], step, s[-1] + step)])

    def t_missing():
        start = -step * random.randint(2, 4)
        s = [start + i * step for i in range(6)]
        k = random.randint(1, 4)
        shown = ", ".join("___" if i == k else str(x) for i, x in enumerate(s))
        return _tb("Find the missing number: %s" % shown, s[k], "int", {},
                   ["The numbers go up in %ss." % step])

    def t_how_many():
        a = -random.randint(2, 9) * (step if d else 1)
        b = random.randint(2, 9) * (step if d else 1)
        st = step if d else 1
        return _tb("Counting in %ss from %d, how many counts does it take to reach %d?" % (st, a, b),
                   (b - a) // st, "int", {}, ["From %d to %d is %d." % (a, b, b - a),
                                              "%d ÷ %d = %d." % (b - a, st, (b - a) // st)])

    def t_line():
        a = random.randint(-8, -2)
        k = random.randint(3, 6)
        st = pick([1, 2, 3])
        ans = a + k * st
        return _nl("Start at %d and make %d jumps of %d to the right. Mark where you land."
                   % (a, k, st), ans, 1, 5, ["%d + %d = %d." % (a, k * st, ans)], lo=-10, hi=15)

    def t_line_back():
        a = random.randint(2, 6)
        k = random.randint(3, 5)
        st = pick([2, 3])
        ans = a - k * st
        return _nl("Start at %d and make %d jumps of %d to the left. Mark where you land."
                   % (a, k, st), ans, 1, 5, ["%d − %d = %d." % (a, k * st, ans)], lo=-15, hi=10)

    return _pick_t([t_back, t_on, t_missing, t_how_many], [t_line, t_line_back])


@skill("Y5.0.g", "Roman numerals to 1000 (M)", S0)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 11, 40, 100), _by(d, 100, 500, 1000))

    def t_read():
        return _tb("Write the Roman numeral %s as a number." % _rom(n), n, "int", {},
                   ["%s = %s." % (" + ".join(_split_rom(n)), n)])

    def t_write():
        return _wq("Write %d in Roman numerals." % n, _rom(n), ["%d = %s." % (n, _rom(n))],
                   "e.g. CXLII")

    def t_value():
        sym, v = pick([("C", 100), ("D", 500), ("M", 1000), ("L", 50), ("X", 10)])
        return _tb("What number does the Roman numeral %s stand for?" % sym, v, "int", {},
                   ["%s = %d." % (sym, v)])

    def t_compare():
        a, b = random.sample(range(_by(d, 11, 40, 100), _by(d, 100, 500, 1000)), 2)
        return _tb("Which is larger, %s or %s? Write it as a number." % (_rom(a), _rom(b)),
                   max(a, b), "int", {}, ["%s = %d and %s = %d." % (_rom(a), a, _rom(b), b)])

    def t_add():
        a, b = random.randint(10, 200), random.randint(10, 200)
        return _tb("Work out %s + %s. Give your answer as a number." % (_rom(a), _rom(b)), a + b,
                   "int", {}, ["%s = %d, %s = %d." % (_rom(a), a, _rom(b), b),
                               "%d + %d = %d." % (a, b, a + b)])

    def t_subtractive():
        v, s = pick([(4, "IV"), (9, "IX"), (40, "XL"), (90, "XC"), (400, "CD"), (900, "CM")])
        return _tb("In Roman numerals, a smaller symbol before a larger one is subtracted. What is "
                   "%s?" % s, v, "int", {}, ["%s = %d." % (s, v)])

    def t_table():
        nums = random.sample(range(_by(d, 11, 40, 100), _by(d, 100, 500, 1000)), 4)
        k = random.randrange(4)
        rows = [[x, _rom(x)] for x in nums]
        return _dt("Complete the table. What number belongs in the empty cell?",
                   ["Number", "Roman numeral"], rows, nums[k],
                   ["%s = %d." % (_rom(nums[k]), nums[k])], missing=[k, 0])

    return _pick_t([t_read, t_write, t_value, t_compare, t_add, t_subtractive], [t_table])


def _split_rom(n):
    out, n = [], int(n)
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out.append("%s (%d)" % (s, v))
            n -= v
    return out


@skill("Y5.0.h", "Years written in Roman numerals", S0)
def _(d=1):
    d = _d(d)
    y = random.randint(_by(d, 1900, 1066, 1000), 2030)

    def t_read():
        return _tb("A building has the year %s carved over the door. Which year is that?" % _rom(y),
                   y, "int", {}, ["%s = %s." % (_rom(y), " + ".join(_split_rom(y)))])

    def t_write():
        return _wq("Write the year %d in Roman numerals." % y, _rom(y), ["%d = %s." % (y, _rom(y))],
                   "e.g. MCMXC")

    def t_age():
        y2 = random.randint(1950, 2015)
        now = 2026
        return _tb("A film's credits end with the year %s. How many years before %d was that?"
                   % (_rom(y2), now), now - y2, "int", {"unit": "years"},
                   ["%s = %d." % (_rom(y2), y2), "%d − %d = %d." % (now, y2, now - y2)])

    def t_order():
        ys = random.sample(range(1000, 2030), 3)
        k = pick([0, 1])
        target = sorted(ys)[0] if k == 0 else sorted(ys)[-1]
        return _tb("Which of these years is the %s? %s. Write it as a number."
                   % ("earliest" if k == 0 else "latest", ", ".join(_rom(x) for x in ys)), target,
                   "int", {}, ["The years are %s." % ", ".join(map(str, ys))])

    def t_century():
        y2 = random.randint(1101, 1999)
        return _tb("The year %s: what are its first two digits when written as a number?"
                   % _rom(y2), y2 // 100, "int", {}, ["%s = %d." % (_rom(y2), y2)])

    return _pick_t([t_read, t_write, t_age, t_order, t_century])


@skill("Y5.0.i", "Number puzzles and place-value reasoning", S0)
def _(d=1):
    d = _d(d)

    def t_largest():
        ds = random.sample(range(0, 10), _by(d, 5, 6, 6))
        big = int("".join(map(str, sorted(ds, reverse=True))))
        return _tb("Use each of these digit cards once to make the LARGEST number you can: %s"
                   % ", ".join(map(str, ds)), big, "int", {},
                   ["Put the biggest digits in the biggest places: %s." % _c(big)])

    def t_smallest():
        ds = random.sample(range(0, 10), _by(d, 5, 6, 6))
        srt = sorted(ds)
        if srt[0] == 0:                                   # a number cannot start with 0
            srt[0], srt[1] = srt[1], srt[0]
        small = int("".join(map(str, srt)))
        return _tb("Use each digit card once to make the SMALLEST %d-digit number you can: %s"
                   % (len(ds), ", ".join(map(str, ds))), small, "int", {},
                   ["The first digit cannot be 0." if 0 in ds else "Smallest digits first.",
                    "The number is %s." % _c(small)])

    def t_clues():
        th = random.randint(1, 9)
        rest = [random.randint(0, 9) for _ in range(4)]
        n = int(str(th) + "".join(map(str, rest)) + str(random.randint(0, 9)))
        s = str(n)
        return _tb("I am a 6-digit number. My hundred thousands digit is %s, my ten thousands digit "
                   "is %s, my thousands digit is %s, my hundreds digit is %s, my tens digit is %s "
                   "and my ones digit is %s. What number am I?" % tuple(s), n, "int", {},
                   ["Write the digits in order: %s." % _c(n)])

    def t_between():
        lo = random.randint(10, 90) * 10000
        hi = lo + 10000
        return _tb("How many multiples of 1,000 are there strictly between %s and %s?"
                   % (_c(lo), _c(hi)), 9, "int", {},
                   ["%s, %s, ..., %s: that is 9." % (_c(lo + 1000), _c(lo + 2000), _c(hi - 1000))])

    def t_round_trip():
        n = random.randint(100000, 999999)
        p = pick([1000, 10000])
        return _tb("Replace the last %d digits of %s with zeros. What number do you get?"
                   % (len(str(p)) - 1, _c(n)), (n // p) * p, "int", {},
                   ["%s with the last digits as zeros is %s." % (_c(n), _c((n // p) * p))])

    def t_digit_sum():
        n = random.randint(100000, 999999)
        return _tb("What is the sum of the digits of %s?" % _c(n), sum(map(int, str(n))), "int", {},
                   ["%s = %d." % (" + ".join(str(n)), sum(map(int, str(n))))])

    return _pick_t([t_largest, t_smallest, t_clues, t_between, t_round_trip, t_digit_sum])


# ================================================================== 5.1 ======
@skill("Y5.1.a", "Compare numbers to 1,000,000", S1)
def _(d=1):
    d = _d(d)
    a = _six(d)
    # a close rival: same leading digits most of the time
    p = pick([10, 100, 1000, 10000])
    b = a + random.choice([-1, 1]) * random.randint(1, 9) * p
    b = abs(b) or a + p

    def t_symbol():
        sym = "<" if a < b else ">"
        return _wq("Write <, > or = to make this true:  %s ___ %s" % (_c(a), _c(b)), sym,
                   ["Compare from the left; the first different digit decides."], "<, > or =")

    def t_greater():
        return _tb("Which is greater, %s or %s?" % (_c(a), _c(b)), max(a, b), "int", {},
                   ["%s is greater." % _c(max(a, b))])

    def t_true_false():
        sym = pick(["<", ">"])
        truth = (a < b) if sym == "<" else (a > b)
        return _wq("True or false?  %s %s %s" % (_c(a), sym, _c(b)), "true" if truth else "false",
                   ["%s is %s than %s." % (_c(a), "less" if a < b else "greater", _c(b))],
                   "true / false")

    def t_context():
        c1, c2 = random.sample(["Fenton", "Oakfield", "Redhill", "Stanton", "Hartley"], 2)
        return _wq("%s has %s residents and %s has %s. Which town has more residents?"
                   % (c1, _c(a), c2, _c(b)), c1 if a > b else c2,
                   ["%s > %s." % (_c(max(a, b)), _c(min(a, b)))], "town name")

    def t_missing_digit():
        n = random.randint(100000, 999999)
        s = list(str(n))
        k = random.randint(1, 4)
        m = int("".join(s[:k] + ["0"] + s[k + 1:]))
        top = int("".join(s[:k] + ["9"] + s[k + 1:]))
        other = random.randint(m, top)
        while other == m:
            other = random.randint(m, top)
        shown = "".join(s[:k] + ["□"] + s[k + 1:])
        return _tb("%s is less than %s. Here □ is one missing digit. What is the LARGEST digit □ "
                   "could be?" % (shown, _c(other)), _largest_digit(s, k, other), "int", {},
                   ["Try the digits from 9 down until the number is less than %s." % _c(other)])

    def t_bar():
        towns = random.sample(["Fenton", "Oakfield", "Redhill", "Stanton"], 4)
        vals = [random.randint(10, 99) * 10000 for _ in range(4)]
        k = vals.index(max(vals))
        return _bar("The chart shows the population of four towns. Type the LARGEST population.",
                    towns, vals, max(vals), ["%s has the tallest bar: %s." % (towns[k], _c(max(vals)))])

    return _pick_t([t_symbol, t_greater, t_true_false, t_context, t_missing_digit], [t_bar])


def _largest_digit(s, k, other):
    for dg in range(9, -1, -1):
        if int("".join(s[:k] + [str(dg)] + s[k + 1:])) < other:
            return dg
    return 0


@skill("Y5.1.b", "Order numbers to 1,000,000", S1)
def _(d=1):
    d = _d(d)
    k = _by(d, 4, 5, 5)
    base = random.randint(1, 9) * 100000
    nums = list({base + random.randint(0, 99) * pick([1000, 100, 10]) for _ in range(k * 2)})[:k]
    while len(nums) < k:
        nums.append(base + random.randint(0, 99999))
    random.shuffle(nums)
    asc = sorted(nums)

    def t_smallest():
        return _tb("Which is the smallest of these numbers? %s" % ", ".join(_c(x) for x in nums),
                   asc[0], "int", {}, ["In order: %s." % ", ".join(_c(x) for x in asc)])

    def t_position():
        i = random.randint(2, k)
        largest = random.random() < 0.5
        order = asc[::-1] if largest else asc
        return _tb("Put these numbers in order, %s first. Which number is %s? %s"
                   % ("largest" if largest else "smallest", _ord(i), ", ".join(_c(x) for x in nums)),
                   order[i - 1], "int", {}, ["In order: %s." % ", ".join(_c(x) for x in order)])

    def t_between():
        i = random.randrange(k - 1)
        x = random.randint(asc[i] + 1, asc[i + 1] - 1) if asc[i + 1] - asc[i] > 1 else asc[i]
        more = sum(1 for v in nums if v > x)
        return _tb("How many of these numbers are greater than %s?  %s"
                   % (_c(x), ", ".join(_c(v) for v in nums)), more, "int", {},
                   ["Greater than %s: %s." % (_c(x), ", ".join(_c(v) for v in asc if v > x) or "none")])

    def t_table():
        names = random.sample(["Mount Ash", "Lake Bryn", "Cove Hill", "Fen Vale", "Glen Ard"], k)
        rows = [[n, _c(v)] for n, v in zip(names, nums)]
        i = random.randint(1, k)
        return _dt("The table shows how many visitors each park had last year. Put the numbers in "
                   "order, largest first. Which number is %s?" % _ord(i), ["Park", "Visitors"], rows,
                   asc[::-1][i - 1], ["Largest first: %s." % ", ".join(_c(x) for x in asc[::-1])])

    return _pick_t([t_smallest, t_position, t_between], [t_table])


def _ord(i):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(i, "%dth" % i)


@skill("Y5.1.c", "Round to the nearest 10, 100 or 1000", S1)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 1000, 10000, 100000), _by(d, 9999, 99999, 999999))
    u = pick([10, 100, 1000])
    # stretch: sit right on a halfway point or next to a carry
    if d == 2 and random.random() < 0.5:
        n = (n // u) * u + u // 2 + pick([-1, 0, 0, 1])

    def t_plain():
        return _tb("Round %s to the nearest %s." % (_c(n), _c(u)), _r(n, u), "int", {},
                   ["Look at the digit to the right of the %s place." % _c(u),
                    "%s rounds to %s." % (_c(n), _c(_r(n, u)))])

    def t_context():
        what = pick(["people watched the match", "tickets were sold", "cars crossed the bridge"])
        return _tb("%s %s. Round this to the nearest %s." % (_c(n), what, _c(u)), _r(n, u), "int",
                   {}, ["%s → %s." % (_c(n), _c(_r(n, u)))])

    def t_three_ways():
        return _tb("Round %s to the nearest 10, to the nearest 100 and to the nearest 1,000. Which "
                   "of the three answers is the largest?" % _c(n),
                   max(_r(n, 10), _r(n, 100), _r(n, 1000)), "int", {},
                   ["%s, %s and %s." % (_c(_r(n, 10)), _c(_r(n, 100)), _c(_r(n, 1000)))])

    def t_change():
        return _tb("%s is rounded to the nearest %s. By how much does the number change?"
                   % (_c(n), _c(u)), abs(_r(n, u) - n), "int", {},
                   ["%s rounds to %s." % (_c(n), _c(_r(n, u))),
                    "The difference is %s." % _c(abs(_r(n, u) - n))])

    def t_line():
        lo = (n // u) * u
        return _nl("Round %s to the nearest %s and mark your answer on the line." % (_c(n), _c(u)),
                   _r(n, u), u // 10 if u >= 100 else 1, u, ["%s → %s." % (_c(n), _c(_r(n, u)))],
                   lo=lo - u, hi=lo + 2 * u)

    def t_table():
        nums = random.sample(range(10000, 99999), 3)
        rows = [[_c(x), _c(_r(x, 10)), _c(_r(x, 100)), _c(_r(x, 1000))] for x in nums]
        r, c = random.randrange(3), random.randint(1, 3)
        ans = _r(nums[r], [10, 100, 1000][c - 1])
        return _dt("Complete the rounding table. What belongs in the empty cell?",
                   ["Number", "Nearest 10", "Nearest 100", "Nearest 1,000"], rows, ans,
                   ["%s to the nearest %s is %s." % (_c(nums[r]), _c([10, 100, 1000][c - 1]), _c(ans))],
                   missing=[r, c])

    return _pick_t([t_plain, t_context, t_three_ways, t_change], [t_line, t_table])


@skill("Y5.1.d", "Round to the nearest 10,000 and 100,000", S1)
def _(d=1):
    d = _d(d)
    n = random.randint(_by(d, 100000, 100000, 100000), 999999)
    u = pick(_by(d, [10000], [10000, 100000], [10000, 100000]))
    if d == 2 and random.random() < 0.5:
        n = min(999999, (n // u) * u + u // 2 + pick([-1, 0, 1]))

    def t_plain():
        return _tb("Round %s to the nearest %s." % (_c(n), _c(u)), _r(n, u), "int", {},
                   ["Look at the %s digit." % ("thousands" if u == 10000 else "ten thousands"),
                    "%s rounds to %s." % (_c(n), _c(_r(n, u)))])

    def t_headline():
        what = pick(["people visited the museum", "runners took part in the city marathons",
                     "books were borrowed"])
        return _tb("A headline rounds '%s %s' to the nearest %s. What number does the headline use?"
                   % (_c(n), what, _c(u)), _r(n, u), "int", {}, ["%s → %s." % (_c(n), _c(_r(n, u)))])

    def t_both():
        return _tb("Round %s to the nearest 10,000 and to the nearest 100,000. What is the "
                   "difference between the two answers?" % _c(n), abs(_r(n, 10000) - _r(n, 100000)),
                   "int", {}, ["%s and %s." % (_c(_r(n, 10000)), _c(_r(n, 100000)))])

    def t_line():
        lo = (n // u) * u
        return _nl("Round %s to the nearest %s and mark it on the line." % (_c(n), _c(u)),
                   _r(n, u), u // 10, u, ["%s → %s." % (_c(n), _c(_r(n, u)))],
                   lo=max(0, lo - u), hi=lo + 2 * u)

    return _pick_t([t_plain, t_headline, t_both], [t_line])


@skill("Y5.1.e", "Which numbers round to a given value", S1)
def _(d=1):
    d = _d(d)
    u = pick(_by(d, [10, 100], [100, 1000], [1000, 10000]))
    target = random.randint(2, 98) * u

    def t_smallest():
        return _tb("A whole number rounds to %s when rounded to the nearest %s. What is the "
                   "SMALLEST it could be?" % (_c(target), _c(u)), target - u // 2, "int", {},
                   ["Halfway down to the next multiple below is %s, which rounds up." % _c(target - u // 2)])

    def t_largest():
        return _tb("A whole number rounds to %s when rounded to the nearest %s. What is the "
                   "LARGEST it could be?" % (_c(target), _c(u)), target + u // 2 - 1, "int", {},
                   ["%s would round up to %s." % (_c(target + u // 2), _c(target + u))])

    def t_which():
        good = target + random.randint(-u // 2, u // 2 - 1)
        bad = [target + u // 2 + random.randint(0, u // 3), target - u // 2 - random.randint(1, u // 3),
               target + u + random.randint(-u // 3, u // 3)]
        opts = [good] + random.sample(bad, 2)
        random.shuffle(opts)
        return _tb("Which of these rounds to %s (nearest %s)?  %s" % (_c(target), _c(u),
                                                                     ", ".join(_c(x) for x in opts)),
                   good, "int", {}, ["%s rounds to %s." % (_c(good), _c(target))])

    def t_count():
        if u > 1000:
            return t_smallest()
        return _tb("How many whole numbers round to %s when rounded to the nearest %s?"
                   % (_c(target), _c(u)), u, "int", {},
                   ["From %s to %s inclusive: %s numbers." % (_c(target - u // 2), _c(target + u // 2 - 1),
                                                              _c(u))])

    return _pick_t([t_smallest, t_largest, t_which, t_count])


@skill("Y5.1.f", "Estimate and check calculations by rounding", S1)
def _(d=1):
    d = _d(d)
    u = _by(d, 100, 1000, 10000)
    a = random.randint(2, 9) * u * 10 // 10 + random.randint(-u // 3, u // 3)
    b = random.randint(2, 9) * u + random.randint(-u // 3, u // 3)
    a = abs(a) + u

    def t_sum():
        return _tb("Estimate %s + %s by rounding each number to the nearest %s." % (_c(a), _c(b), _c(u)),
                   _r(a, u) + _r(b, u), "int", {},
                   ["%s ≈ %s and %s ≈ %s." % (_c(a), _c(_r(a, u)), _c(b), _c(_r(b, u))),
                    "%s + %s = %s." % (_c(_r(a, u)), _c(_r(b, u)), _c(_r(a, u) + _r(b, u)))])

    def t_diff():
        x, y = max(a, b), min(a, b)
        if _r(x, u) == _r(y, u):
            x += 2 * u
        return _tb("Estimate %s − %s by rounding each number to the nearest %s." % (_c(x), _c(y), _c(u)),
                   _r(x, u) - _r(y, u), "int", {},
                   ["%s − %s = %s." % (_c(_r(x, u)), _c(_r(y, u)), _c(_r(x, u) - _r(y, u)))])

    def t_check():
        true = a + b
        wrong = true + pick([-1, 1]) * u * random.randint(2, 4)
        claimed = pick([true, wrong])
        ok = "yes" if claimed == true else "no"
        est = _r(a, u) + _r(b, u)
        return _wq("%s says %s + %s = %s. Estimate by rounding to the nearest %s. Is the answer "
                   "sensible? (yes or no)" % (_who(), _c(a), _c(b), _c(claimed), _c(u)), ok,
                   ["The estimate is %s." % _c(est),
                    "%s is %s the estimate." % (_c(claimed), "close to" if ok == "yes" else "far from")],
                   "yes / no")

    def t_word():
        x, y = random.randint(20000, 60000), random.randint(10000, 40000)
        return _tb("A festival sold %s tickets on Saturday and %s on Sunday. Round each to the "
                   "nearest 1,000 to estimate the total." % (_c(x), _c(y)),
                   _r(x, 1000) + _r(y, 1000), "int", {},
                   ["%s + %s = %s." % (_c(_r(x, 1000)), _c(_r(y, 1000)), _c(_r(x, 1000) + _r(y, 1000)))])

    return _pick_t([t_sum, t_diff, t_check, t_word])


@skill("Y5.1.g", "Numbers to 1,000,000 on a number line", S1)
def _(d=1):
    d = _d(d)
    major = pick(_by(d, [10000], [10000, 100000], [100000, 50000]))
    lo = random.randint(0, 5) * major
    step = major // 10

    def t_place():
        ans = lo + random.randint(1, 49) * step
        return _nl("Place %s on the number line." % _c(ans), ans, step, major,
                   ["Each small step is %s." % _c(step)], lo=lo, hi=lo + 5 * major)

    def t_halfway():
        a = lo + random.randint(0, 2) * major
        b = a + 2 * major
        return _tb("What number is exactly halfway between %s and %s?" % (_c(a), _c(b)), (a + b) // 2,
                   "int", {}, ["(%s + %s) ÷ 2 = %s." % (_c(a), _c(b), _c((a + b) // 2))])

    def t_marks():
        k = random.randint(2, 9)
        return _tb("A number line goes from %s to %s with 10 equal steps. What is the value of the "
                   "%s mark after %s?" % (_c(lo), _c(lo + major), _ord(k), _c(lo)), lo + k * step,
                   "int", {}, ["Each step is %s ÷ 10 = %s." % (_c(major), _c(step)),
                               "%s + %d × %s = %s." % (_c(lo), k, _c(step), _c(lo + k * step))])

    def t_nearest():
        ans = lo + random.randint(1, 49) * step + random.randint(1, step - 1)
        return _nl("Mark %s on the line as accurately as you can (to the nearest small step)."
                   % _c(ans), _r(ans - lo, step) + lo, step, major,
                   ["%s is nearest to %s." % (_c(ans), _c(_r(ans - lo, step) + lo))],
                   lo=lo, hi=lo + 5 * major)

    return _pick_t([t_halfway, t_marks], [t_place, t_nearest])
