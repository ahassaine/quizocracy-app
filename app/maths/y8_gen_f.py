# Year 8 generators: more question types for skills registered in y8_gen_a … y8_gen_e.
#
# Each @_more(key, old) function is one extra framing for that skill; `old` is roughly how
# many framings the original generator already has. At import the original generator is
# wrapped so every framing, old or new, is about equally likely.
import operator
from decimal import ROUND_HALF_UP
from math import ceil, floor, gcd, isqrt

from . import maths_engine as _e
from .maths_engine import ordinal
from .y5_common import *  # noqa: F401,F403

_EXTRA = {}


def _more(key, old):
    def deco(fn):
        _EXTRA.setdefault(key, [old, []])[1].append(fn)
        return fn
    return deco


def _widen(orig, old, fns):
    def gen(d=1):
        if random.random() < len(fns) / float(len(fns) + old):
            return random.choice(fns)(_d(d))
        return _e.call_generator(orig, d)
    return gen


def _lcm(a, b):
    return a * b // gcd(a, b)


def _yn(prompt, yes, solution):
    return _wq(prompt, "yes" if yes else "no", solution, "yes or no")


def _num(prompt, ans, solution, unit=None, tol=0):
    """A decimal answer compared by value; ans is a Decimal/str/int."""
    spec = {"unit": unit} if unit else {}
    return _tb(prompt, _ds(ans), "num", spec, solution, tol)


def _int(prompt, ans, solution, unit=None):
    return _tb(prompt, int(ans), "int", {"unit": unit} if unit else {}, solution)


def _round(x, places):
    """Round a Decimal half-up to `places` decimal places (negative = tens, hundreds…)."""
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def _round_sf(x, k):
    x = Decimal(x)
    return _round(x, k - 1 - x.adjusted())


def _gbp(x):
    """Money: £5, £7.50, £12.35."""
    x = Decimal(x)
    return "£%s" % (_ds(x) if x == int(x) else "%.2f" % x)


def _an(n):
    """'a 6' / 'an 8' / 'an 11' / 'an 18': the article as the number is read aloud."""
    s = str(int(n))
    return ("an " if s[0] == "8" or s in ("11", "18") else "a ") + s


def _sym(op):
    return op.replace(">=", "≥").replace("<=", "≤")


def _cg(prompt, spec, answer, solution, atype="int", placeholder="type your answer"):
    """A coordinate grid used as a picture; the pupil types the answer."""
    sp = dict(spec)
    sp["typed"] = True
    sp["placeholder"] = placeholder
    return {"prompt": prompt, "component": "coordinate_grid", "spec": sp,
            "answer": answer, "answer_type": atype, "solution": solution}


# ================================================================== 8.0 ======
@_more("Y8.0.c", 10)
def _(d):
    k = _by(d, 1, 2, 3)
    while True:
        digits = random.randint(1000, 9999)
        x = Decimal(digits) / Decimal(10) ** (random.randint(5, 7))
        r = _round_sf(x, k)
        if digits % 10 and r.adjusted() == x.adjusted():       # no carry into a new place
            break
    return _num("Write %s correct to %d significant %s." % (_ds(x), k, "figure" if k == 1 else "figures"), r,
                ["Leading zeros are not significant: the first significant figure is the first non-zero digit.",
                 "%s to %d s.f. is %s." % (_ds(x), k, _ds(r))])


@_more("Y8.0.c", 10)
def _(d):
    v = Decimal(pick([n for n in range(_by(d, 20, 50, 100), _by(d, 99, 300, 999) + 1) if n % 10])) / 10   # always 1 d.p.
    lo = v - Decimal("0.05")
    return _num("A plank is %s m long, correct to 1 decimal place. What is the shortest length it could "
                "really be, in metres?" % _ds(v), lo,
                ["Anything from %s up to (but not including) %s rounds to %s." % (_ds(lo), _ds(v + Decimal("0.05")), _ds(v)),
                 "The shortest possible length is %s m." % _ds(lo)], "m")


@_more("Y8.0.c", 10)
def _(d):
    while True:
        a10, b10 = random.randint(*_by(d, (21, 94), (150, 940), (1500, 9400))), random.randint(21, 94)
        a, b = Decimal(a10) / 10, Decimal(b10) / _by(d, 10, 10, 100)       # stretch: b is 0.21 … 0.94
        ra, rb = _round_sf(a, 1), _round_sf(b, 1)
        if str(a10)[1] != "5" and b10 % 10 != 5 and a10 % 10 and b10 % 10 and ra < _by(d, 10, 100, 1000):
            break                                                           # no halfway cases
    est = ra * rb
    return _int("Estimate %s × %s by first rounding each number to 1 significant figure." % (_ds(a), _ds(b)), est,
                ["%s ≈ %s and %s ≈ %s." % (_ds(a), _ds(ra), _ds(b), _ds(rb)),
                 "%s × %s = %s." % (_ds(ra), _ds(rb), _ds(est))])


@_more("Y8.0.c", 10)
def _(d):
    whole = random.randint(0, 9)
    if d == 2:                     # stretch: 3 d.p., only the hundredths digit decides
        while True:
            h = random.randint(1, 999)
            if (h // 10) % 10 != 5 and h % 10 and 50 <= h <= 949:
                break
        x = whole + Decimal(h) / 1000
        dig = (h // 10) % 10
    else:
        while True:
            h = random.randint(1, 99)
            if h % 10 not in (0, 5) and 5 <= h <= 94:
                break
        x = whole + Decimal(h) / 100
        dig = h % 10
    r = _round(x, 1)
    return _nld("Round %s to 1 decimal place and mark the rounded number on the line." % _ds(x), r,
                whole, whole + 1, Decimal("0.1"), Decimal("0.5"),
                ["The hundredths digit is %d, so round %s." % (dig, "up" if dig >= 5 else "down"),
                 "%s ≈ %s." % (_ds(x), _ds(r))])


@_more("Y8.0.c", 10)
def _(d):
    while True:
        n = Decimal(random.randint(*_by(d, (1000, 9999), (10000, 99999), (10000, 99999)))) \
            / Decimal(10) ** random.randint(*_by(d, (0, 0), (0, 4), (5, 7)))   # stretch: 0.0… numbers
        rs = [_round_sf(n, k) for k in (1, 2, 3)]
        if len(set(_ds(r) for r in rs)) == 3:
            break
    miss = random.randrange(3)
    row = [_ds(n)] + [_ds(r) for r in rs]
    return _dt("The table rounds one number to 1, 2 and 3 significant figures. What goes in the empty cell?",
               ["Number", "1 s.f.", "2 s.f.", "3 s.f."], [row], _ds(rs[miss]),
               ["Count significant figures from the first non-zero digit.",
                "%s to %d s.f. is %s." % (_ds(n), miss + 1, _ds(rs[miss]))],
               missing=(0, miss + 1), atype="num")


@_more("Y8.0.c", 10)
def _(d):
    n = pick(_by(d, [3, 6, 9], [3, 6, 7, 9, 11, 12], [7, 11, 12, 13, 15]))
    while True:
        total = random.randint(*_by(d, (10, 60), (10, 200), (150, 999)))
        if (total * 100) % n:
            break
    each = _round(Decimal(total) / n, 2)
    return _num("£%d is shared equally between %d people. How much does each person get, to the nearest penny? "
                "Give your answer in pounds." % (total, n), each,
                ["%d ÷ %d = %s…" % (total, n, str(Decimal(total) / n)[:7]),
                 "To the nearest penny (2 decimal places): %s." % _gbp(each)], "£")


@_more("Y8.0.c", 10)
def _(d):
    unit = _by(d, 10, pick([10, 100]), pick([100, 1000]))
    shown = random.randint(2, 9) * unit + _by(d, 0, 0, random.choice([0, unit * 10]))
    ask_big = random.random() < 0.5
    ans = shown + unit // 2 - 1 if ask_big else shown - unit // 2
    return _int("A whole number rounds to %s, to the nearest %s. What is the %s whole number it could be?"
                % (_c(shown), _c(unit), "largest" if ask_big else "smallest"), ans,
                ["Numbers from %s to %s round to %s." % (_c(shown - unit // 2), _c(shown + unit // 2 - 1), _c(shown)),
                 "So the %s is %s." % ("largest" if ask_big else "smallest", _c(ans))])


# ================================================================== 8.1 ======
def _factors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def _prime(n):
    return n > 1 and all(n % k for k in range(2, isqrt(n) + 1))


@_more("Y8.1.b", 11)
def _(d):
    n = pick(_by(d, [12, 15, 18, 20, 24, 28, 30, 32, 40, 45, 50],
                 [12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 60, 64, 72, 84, 90, 96, 100],
                 [120, 144, 150, 180, 196, 200, 210, 225, 240, 252, 300, 360]))
    f = _factors(n)
    pairs = [(a, n // a) for a in f if a * a <= n]
    return _int("How many factor pairs does %d have? (3 × 4 and 4 × 3 count as the same pair.)" % n, len(pairs),
                ["The factor pairs are %s." % ", ".join("%d × %d" % p for p in pairs),
                 "That is %d pairs." % len(pairs)])


@_more("Y8.1.b", 11)
def _(d):
    while True:
        a = random.randint(_by(d, 20, 40, 80), _by(d, 60, 120, 190))
        b = a + random.randint(4, 6)
        ps = [x for x in range(a, b + 1) if _prime(x)]
        if len(ps) == 1 and a < ps[0] < b:
            break
    others = ["%d = %d × %d" % (x, min(f for f in range(2, x) if x % f == 0), x // min(f for f in range(2, x) if x % f == 0))
              for x in range(a, b + 1) if x != ps[0]]
    return _int("Exactly one number from %d to %d is prime. Which is it?" % (a, b), ps[0],
                ["The others have factors: %s." % "; ".join(others), "%d has only the factors 1 and itself." % ps[0]])


@_more("Y8.1.b", 11)
def _(d):
    m = random.randint(_by(d, 4, 6, 12), _by(d, 9, 15, 25))
    while True:
        lim = random.randint(50, _by(d, 150, 300, 1000))
        if lim % m:
            break
    ans = (lim // m + 1) * m
    return _int("What is the first multiple of %d that is greater than %d?" % (m, lim), ans,
                ["%d ÷ %d = %d remainder %d." % (lim, m, lim // m, lim % m),
                 "The next multiple is %d × %d = %d." % (lim // m + 1, m, ans)])


@_more("Y8.1.b", 11)
def _(d):
    m = random.randint(3, _by(d, 9, 15, 19))
    n = random.choice([50, 100, 150, 200, 500]) if d else random.choice([30, 50, 100])
    return _int("How many multiples of %d are there from 1 to %d?" % (m, n), n // m,
                ["%d ÷ %d = %d%s." % (n, m, n // m, " remainder %d" % (n % m) if n % m else ""),
                 "So %d multiples: %d, %d, … , %d." % (n // m, m, 2 * m, (n // m) * m)])


@_more("Y8.1.b", 11)
def _(d):
    sq = random.randint(4, _by(d, 8, 11, 14)) ** 2
    others = random.sample([x for x in range(sq - 6, sq + 7) if isqrt(x) ** 2 != x], 2)
    shown = others + [sq]
    random.shuffle(shown)
    return _int("Which of these numbers has an ODD number of factors: %s?" % ", ".join(map(str, shown)), sq,
                ["Factors come in pairs, except when a number is multiplied by itself.",
                 "%d = %d × %d is a square number, so it has %d factors." % (sq, isqrt(sq), isqrt(sq), len(_factors(sq)))])


@_more("Y8.1.b", 11)
def _(d):
    a, b = pick(_by(d, [(2, 3), (2, 5), (3, 4), (4, 5), (3, 10)],
                    [(4, 6), (6, 8), (6, 9), (4, 10), (10, 15), (8, 12), (6, 15), (12, 18)],
                    [(12, 18), (14, 21), (16, 24), (18, 24), (15, 25), (20, 30)]))
    l = _lcm(a, b)
    top = _by(d, 4, 6, 10)
    if random.random() < 0.5:
        n = l * random.randint(2, top)
    else:                          # a multiple of a that is not a multiple of b
        n = pick([x for x in range(l + 1, top * l) if x % a == 0 and x % b])
    yes = n % a == 0 and n % b == 0
    return _yn("Is %d a common multiple of %d and %d?" % (n, a, b), yes,
               ["%d ÷ %d %s and %d ÷ %d %s." % (n, a, "is exact" if n % a == 0 else "is not exact",
                                                n, b, "is exact" if n % b == 0 else "is not exact"),
                "So %s." % ("yes" if yes else "no")])


@_more("Y8.1.b", 11)
def _(d):
    while True:
        n = pick(_by(d, [12, 18, 20, 24, 30, 36], [24, 36, 48, 60, 72, 84, 90, 96, 120],
                     [144, 168, 180, 210, 240, 252, 360]))
        m = pick(_by(d, [2, 3, 5], [2, 3, 4, 5, 6], [6, 7, 8, 9, 12]))
        lo = random.randint(*_by(d, (1, 8), (5, 20), (15, 60)))
        hi = lo + random.randint(*_by(d, (4, 10), (6, 15), (10, 30)))
        hits = [f for f in _factors(n) if f % m == 0 and lo < f < hi]
        if len(hits) == 1:
            break
    return _int("I am a factor of %d and a multiple of %d. I am greater than %d and less than %d. What number am I?"
                % (n, m, lo, hi), hits[0],
                ["Factors of %d between %d and %d: %s." % (n, lo, hi, ", ".join(str(f) for f in _factors(n) if lo < f < hi)),
                 "Only %d is a multiple of %d." % (hits[0], m)])


@_more("Y8.1.f", 8)
def _(d):
    a, b = random.sample(_by(d, [4, 6, 8, 10], [6, 8, 10, 12, 20], [8, 12, 15, 18, 20, 24]), 2)
    # never one pack size a multiple of the other (easy lets an occasional one through)
    while max(a, b) % min(a, b) == 0 and (d or random.random() < 0.8):
        a, b = random.sample(_by(d, [4, 6, 8, 10], [6, 8, 10, 12, 20], [8, 12, 15, 18, 20, 24]), 2)
    l = _lcm(a, b)
    return _int("Sausages come in packs of %d and rolls in packs of %d. What is the smallest number of packs of "
                "sausages to buy so that there are exactly as many sausages as rolls?" % (a, b), l // a,
                ["The smallest equal amount is the LCM of %d and %d, which is %d." % (a, b, l),
                 "%d ÷ %d = %s of sausages." % (l, a, _pl(l // a, "pack"))])


@_more("Y8.1.f", 8)
def _(d):
    t1, t2 = pick(_by(d, [(20, 30), (30, 40), (40, 60), (30, 45)],
                      [(40, 60), (45, 60), (50, 75), (60, 80), (36, 48), (60, 90), (72, 96)],
                      [(48, 72), (54, 72), (72, 96), (84, 126), (75, 90)]))
    l = _lcm(t1, t2)
    return _int("%s runs a lap in %d seconds and %s runs a lap in %d seconds. They start together at the start line. "
                "How many laps has %s run when they are next at the start line together?"
                % ("Runner A", t1, "Runner B", t2, "Runner A"), l // t1,
                ["They meet after the LCM of %d and %d seconds, which is %d seconds." % (t1, t2, l),
                 "%d ÷ %d = %d laps." % (l, t1, l // t1)])


@_more("Y8.1.f", 8)
def _(d):
    h = random.randint(_by(d, 2, 3, 4), _by(d, 5, 8, 12))
    a, b = random.sample(range(2, 9), 2)
    while gcd(a, b) != 1:
        a, b = random.sample(range(2, 9), 2)
    L, W = a * h, b * h
    return _int("A floor %d m by %d m is covered with the largest square tiles that fit exactly (whole tiles only). "
                "How many tiles are needed?" % (L, W), a * b,
                ["The largest tile side is the HCF of %d and %d, which is %d m." % (L, W, h),
                 "%d ÷ %d = %d and %d ÷ %d = %d, so %d × %d = %d tiles." % (L, h, a, W, h, b, a, b, a * b)])


@_more("Y8.1.f", 8)
def _(d):
    a, b = random.sample(_by(d, [8, 10, 12, 16], [8, 10, 12, 15, 16, 18, 20, 24], [14, 15, 18, 21, 24, 32, 36]), 2)
    while max(a, b) % min(a, b) == 0 and (d or random.random() < 0.8):
        a, b = random.sample(_by(d, [8, 10, 12, 16], [8, 10, 12, 15, 16, 18, 20, 24], [14, 15, 18, 21, 24, 32, 36]), 2)
    l = _lcm(a, b)
    return _int("Gear A has %d teeth and gear B has %d teeth. They turn together. How many full turns does gear A "
                "make before both gears are back in their starting positions for the first time?" % (a, b), l // a,
                ["The teeth line up again after the LCM of %d and %d, which is %d teeth." % (a, b, l),
                 "%d ÷ %d = %s of gear A." % (l, a, _pl(l // a, "turn"))])


@_more("Y8.1.f", 8)
def _(d):
    h = random.randint(_by(d, 2, 4, 6), _by(d, 6, 12, 15))
    top = _by(d, 6, 8, 10)
    a, b = random.sample(range(2, top), 2)
    while gcd(a, b) != 1:
        a, b = random.sample(range(2, top), 2)
    r, bl = a * h, b * h
    return _int("A hall has %d red chairs and %d blue chairs. They are put in rows, every row has the same number "
                "of chairs, and each row has only one colour. Rows are as long as possible. How many rows are there?"
                % (r, bl), a + b,
                ["The longest possible row is the HCF of %d and %d, which is %d chairs." % (r, bl, h),
                 "%d ÷ %d = %d red rows and %d ÷ %d = %d blue rows, %d rows altogether." % (r, h, a, bl, h, b, a + b)])


@_more("Y8.1.f", 8)
def _(d):
    p, q = pick(_by(d, [(10, 15), (10, 20), (15, 20), (20, 30), (6, 10), (12, 15)],
                    [(10, 15), (12, 18), (15, 20), (20, 30), (9, 12), (6, 8), (12, 20), (18, 24)],
                    [(14, 21), (16, 24), (18, 24), (24, 36), (8, 14), (16, 20)]))
    l = _lcm(p, q)
    n = 180 // l + 1
    return _int("One bell rings every %d minutes and another every %d minutes. Both ring at 9:00. How many times do "
                "they ring together from 9:00 to 12:00, counting both 9:00 and 12:00 if they ring then?" % (p, q), n,
                ["They ring together every %d minutes (the LCM of %d and %d)." % (l, p, q),
                 "9:00 to 12:00 is 180 minutes; 180 ÷ %d = %d remainder %d." % (l, 180 // l, 180 % l),
                 "Counting 9:00 too: %d times." % n])


@_more("Y8.1.g", 11)
def _(d):
    b, n = random.randint(2, 9), random.randint(3, _by(d, 4, 6, 7))
    return _wq("Write %s in index form (like 3^4)." % " × ".join([str(b)] * n), "%d^%d" % (b, n),
               ["%d is multiplied by itself %d times." % (b, n), "%d^%d." % (b, n)], "e.g. 3^4")


@_more("Y8.1.g", 11)
def _(d):
    a, b = pick(_by(d, [(2, 3), (3, 2), (2, 5), (3, 4)],
                    [(2, 5), (3, 4), (2, 6), (2, 7), (3, 5), (5, 3), (4, 3), (2, 3)],
                    [(2, 7), (2, 8), (2, 9), (3, 5), (3, 6), (4, 5), (5, 4), (6, 3)]))
    return _int("Work out the difference between %d^%d and %d^%d." % (a, b, b, a), abs(a ** b - b ** a),
                ["%d^%d = %d and %d^%d = %d." % (a, b, a ** b, b, a, b ** a),
                 "The difference is %d." % abs(a ** b - b ** a)])


@_more("Y8.1.g", 11)
def _(d):
    n = random.randint(_by(d, 2, 3, 6), _by(d, 5, 9, 12))
    if random.random() < 0.5:
        return _int("%s = 10^?. What is the power?" % _c(10 ** n), n,
                    ["%s has %d zeros, so it is 10^%d." % (_c(10 ** n), n, n)])
    k = random.randint(2, 9) if d < 2 else random.randint(11, 99)
    return _int("Write %d × 10^%d as an ordinary number." % (k, n), k * 10 ** n,
                ["10^%d = %s." % (n, _c(10 ** n)), "%d × %s = %s." % (k, _c(10 ** n), _c(k * 10 ** n))])


@_more("Y8.1.g", 11)
def _(d):
    s, n = pick(_by(d, [10, 100], [50, 100, 200, 300, 500], [150, 250, 300, 750])), random.randint(_by(d, 2, 3, 5), _by(d, 4, 6, 8))
    return _int("A colony of %d bacteria doubles every hour. How many bacteria are there after %d hours? "
                "(Number = %d × 2^%d.)" % (s, n, s, n), s * 2 ** n,
                ["2^%d = %d." % (n, 2 ** n), "%d × %d = %s." % (s, 2 ** n, _c(s * 2 ** n))])


@_more("Y8.1.g", 11)
def _(d):
    c = random.randint(3, _by(d, 6, 9, 12))
    lo = random.randint((c - 1) ** 3 + 1, c ** 3 - 1)
    hi = random.randint(c ** 3 + 1, (c + 1) ** 3 - 1)
    return _int("Which cube number lies between %d and %d?" % (lo, hi), c ** 3,
                ["%d³ = %d and %d³ = %d." % (c - 1, (c - 1) ** 3, c + 1, (c + 1) ** 3),
                 "Only %d³ = %d is between them." % (c, c ** 3)])


@_more("Y8.1.g", 11)
def _(d):
    p = pick(_by(d, [2], [2, 3], [2, 3, 3]))
    ns = sorted(random.sample(_by(d, range(1, 11), range(1, 13 if p == 2 else 10), range(6, 21 if p == 2 else 13)), 4))
    i = random.randrange(4)
    return _io("The machine works out n^%d. What is the missing output?" % p, [(n, n ** p) for n in ns], i, ns[i] ** p,
               ["%d^%d = %d." % (ns[i], p, ns[i] ** p)], rule="n^%d" % p)


@_more("Y8.1.h", 8)
def _(d):
    a = random.randint(2, _by(d, 4, 6, 9))
    return _int("Work out (−%d)^3." % a, -a ** 3,
                ["(−%d) × (−%d) = %d, then × (−%d) = −%d." % (a, a, a * a, a, a ** 3),
                 "An odd power of a negative number is negative."])


@_more("Y8.1.h", 8)
def _(d):
    a = random.randint(_by(d, 2, 2, 6), _by(d, 5, 9, 15))
    if random.random() < 0.5:
        return _int("Work out −%d^2. (The power is worked out before the minus sign.)" % a, -a * a,
                    ["%d^2 = %d, so −%d^2 = −%d." % (a, a * a, a, a * a)])
    return _int("%s says (−%d)^2 = −%d. What is the correct value of (−%d)^2?" % (_who(), a, a * a, a), a * a,
                ["(−%d) × (−%d): negative × negative is positive." % (a, a), "(−%d)^2 = %d." % (a, a * a)])


@_more("Y8.1.h", 8)
def _(d):
    x = pick(_by(d, ["0.1", "0.2", "0.3"], ["0.1", "0.2", "0.3", "0.4", "0.5"], ["0.6", "0.7", "0.05", "1.1", "1.2"]))
    v = Decimal(x) ** 3
    return _num("Work out %s^3." % x, v, ["%s × %s × %s = %s." % (x, x, x, _ds(v))])


@_more("Y8.1.h", 8)
def _(d):
    x = pick(_by(d, ["0.2", "0.3", "0.5", "1.5", "2.5"], ["1.1", "1.2", "1.5", "2.5", "0.6", "0.9", "1.3", "3.5"],
                 ["1.4", "1.7", "2.3", "4.5", "0.35", "0.12", "6.5"]))
    v = Decimal(x) ** 2
    if random.random() < 0.5:
        return _num("A square tile has sides of %s m. What is its area, in m²?" % x, v,
                    ["Area = %s² = %s × %s = %s m²." % (x, x, x, _ds(v))], "m²")
    return _num("Work out %s^2." % x, v, ["%s × %s = %s." % (x, x, _ds(v))])


@_more("Y8.1.h", 8)
def _(d):
    n = random.randint(_by(d, 2, 11, 100), _by(d, 9, 99, 999))
    return _int("Work out (−1)^%d." % n, -1 if n % 2 else 1,
                ["(−1) × (−1) = 1, so the sign depends on whether %d is odd or even." % n,
                 "%d is %s, so (−1)^%d = %d." % (n, "odd" if n % 2 else "even", n, -1 if n % 2 else 1)])


@_more("Y8.1.h", 8)
def _(d):
    a = random.randint(2, 3)
    p, q = random.sample(_by(d, [2, 3], range(2, 6 if a == 2 else 5), [3, 4, 5] if a == 2 else [2, 3, 4, 5]), 2)
    v = (-a) ** p + (-a) ** q
    return _int("Work out (−%d)^%d + (−%d)^%d." % (a, p, a, q), v,
                ["(−%d)^%d = %d and (−%d)^%d = %d." % (a, p, (-a) ** p, a, q, (-a) ** q),
                 "%d + %s = %d." % ((-a) ** p, ("(%d)" if (-a) ** q < 0 else "%d") % (-a) ** q, v)])


@_more("Y8.1.h", 8)
def _(d):
    a = pick(_by(d, [2], [2, 3], [3, 4, 5]))
    ns = [1, 2, 3, 4, 5] if a == 2 else ([1, 2, 3, 4] if d < 2 else [1, 2, 3, 4, 5])
    i = random.randrange(1, len(ns) if d else 4)
    rows = [["(−%d)^%d" % (a, n), str((-a) ** n)] for n in ns]
    return _dt("The table shows powers of −%d. What goes in the empty cell?" % a, ["Power", "Value"], rows,
               (-a) ** ns[i], ["Each value is the one above multiplied by −%d." % a,
                               "(−%d)^%d = %d." % (a, ns[i], (-a) ** ns[i])], missing=(i, 1))


@_more("Y8.1.h", 8)
def _(d):
    x = pick(_by(d, ["0.2", "0.3", "0.4", "0.5"], ["0.7", "0.4", "0.9", "1.1", "1.2", "0.3", "0.8", "1.5"],
                 ["1.3", "1.4", "1.6", "0.06", "0.11", "2.5"]))
    v = Decimal(x) ** 2
    return _num("x^2 = %s and x is positive. What is x?" % _ds(v), x, ["%s × %s = %s, so x = %s." % (x, x, _ds(v), x)])


@_more("Y8.1.h", 8)
def _(d):
    x = pick(_by(d, ["0.1", "0.2"], ["0.2", "0.1", "0.3", "0.5"], ["0.4", "0.6", "0.7", "1.2"]))
    v = -Decimal(x) ** 3
    return _num("Work out (−%s)^3." % x, v,
                ["%s^3 = %s." % (x, _ds(-v)), "An odd power of a negative is negative: %s." % _ds(v)])


@_more("Y8.1.h", 8)
def _(d):
    a, x = random.randint(2, _by(d, 3, 5, 9)), -random.randint(_by(d, 1, 2, 4), _by(d, 4, 6, 12))
    return _int("Work out %dx² when x = %d." % (a, x), a * x * x,
                ["Square first: (%d)² = %d." % (x, x * x), "%d × %d = %d." % (a, x * x, a * x * x)])


@_more("Y8.1.h", 8)
def _(d):
    e = pick(_by(d, ["0.1", "0.2", "0.3"], ["0.1", "0.2", "0.3", "0.4", "0.5", "1.1", "1.2"], ["0.6", "0.7", "1.1", "1.2", "1.5"]))
    v = Decimal(e) ** 3
    return _num("A cube has edges of %s m. What is its volume, in m³?" % e, v, ["Volume = %s³ = %s × %s × %s = %s m³." % (e, e, e, e, _ds(v))], "m³")


@_more("Y8.1.h", 8)
def _(d):
    a = random.randint(2, _by(d, 3, 4, 4))
    ps = random.sample(_by(d, range(1, 4), range(1, 6), range(2, 7)), 3)
    vals = [(-a) ** p for p in ps]
    if len(set(vals)) < 3:
        ps = [1, 2, 3]
        vals = [(-a) ** p for p in ps]
    return _int("Which of (−%d)^%d, (−%d)^%d and (−%d)^%d is the smallest? Type its value." % (a, ps[0], a, ps[1], a, ps[2]), min(vals),
                ["The values are %s." % ", ".join(str(v) for v in vals), "The smallest is %d." % min(vals)])


@_more("Y8.1.i", 10)
def _(d):
    b = random.randint(2, 9)
    m, n = random.randint(_by(d, 2, 3, 5), _by(d, 5, 9, 12)), random.randint(2, _by(d, 4, 8, 10))
    p = random.randint(1, m + n - 1)
    return _int("Write %d^%d × %d^%d ÷ %d^%d as a single power of %d. What is the power?" % (b, m, b, n, b, p, b), m + n - p,
                ["Multiply: add the powers, %d + %d = %d." % (m, n, m + n),
                 "Divide: subtract, %d − %d = %d." % (m + n, p, m + n - p)])


@_more("Y8.1.i", 10)
def _(d):
    b, big, k = pick(_by(d, [(2, 4, 2), (3, 9, 2), (5, 25, 2), (2, 8, 3)],
                         [(2, 4, 2), (2, 8, 3), (2, 16, 4), (3, 9, 2), (3, 27, 3), (5, 25, 2), (2, 32, 5)],
                         [(2, 32, 5), (2, 64, 6), (3, 81, 4), (5, 125, 3), (3, 27, 3), (2, 16, 4)]))
    m = random.randint(2, _by(d, 4, 6, 9))
    return _int("%d^%d × %d = %d^?. What is the missing power?" % (b, m, big, b), m + k,
                ["%d = %d^%d." % (big, b, k), "%d^%d × %d^%d = %d^%d." % (b, m, b, k, b, m + k)])


@_more("Y8.1.i", 10)
def _(d):
    b = random.randint(2, 5)
    m, n = random.randint(2, _by(d, 4, 6, 9)), random.randint(2, _by(d, 4, 6, 9))
    return _int("%s says %d^%d × %d^%d = %d^%d. That is wrong. %d^%d × %d^%d = %d^?. What is the correct power?"
                % (_who(), b, m, b, n, b * b, m * n, b, m, b, n, b), m + n,
                ["Keep the base the same and add the powers.", "%d + %d = %d." % (m, n, m + n)])


@_more("Y8.1.i", 10)
def _(d):
    v = pick(["a", "y", "m", "p", "t"])
    m, n = random.randint(_by(d, 4, 5, 8), _by(d, 9, 12, 15)), random.randint(2, _by(d, 3, 4, 6))
    kind = random.randrange(3)
    if kind == 0:
        return _int("Simplify %s^%d ÷ %s^%d. What is the power of %s?" % (v, m, v, n, v), m - n, ["Subtract the powers: %d − %d = %d." % (m, n, m - n)])
    if kind == 1:
        return _int("Simplify %s^%d × %s. What is the power of %s?" % (v, m, v, v), m + 1, ["%s is %s^1, so add 1: %d + 1 = %d." % (v, v, m, m + 1)])
    return _int("Simplify (%s^%d)^%d. What is the power of %s?" % (v, n + 1, m, v), (n + 1) * m, ["Multiply the powers: %d × %d = %d." % (n + 1, m, (n + 1) * m)])


@_more("Y8.1.i", 10)
def _(d):
    b, m = random.randint(_by(d, 2, 2, 13), _by(d, 10, 12, 50)), random.randint(_by(d, 2, 2, 10), _by(d, 5, 9, 30))
    if random.random() < 0.5:
        return _int("%d^%d ÷ %d^%d = %d^?. What is the missing power?" % (b, m, b, m, b), 0,
                    ["Subtract the powers: %d − %d = 0." % (m, m), "Any number divided by itself is 1, so %d^0 = 1." % b])
    return _int("Use the laws of indices: %d^%d ÷ %d^%d = %d^0. What is the value of %d^0?" % (b, m, b, m, b, b), 1,
                ["%d^%d ÷ %d^%d is a number divided by itself, which is 1." % (b, m, b, m)])


@_more("Y8.1.i", 10)
def _(d):
    b = random.randint(2, 7)
    n, tot = random.randint(2, _by(d, 4, 6, 9)), random.randint(_by(d, 6, 8, 12), _by(d, 10, 14, 20))
    if d == 2 and random.random() < 0.5:               # stretch: the missing power is in a division
        return _int("%d^? ÷ %d^%d = %d^%d. What is the missing power?" % (b, b, n, b, tot), tot + n,
                    ["Powers subtract when dividing: ? − %d = %d." % (n, tot), "? = %d." % (tot + n)])
    return _int("%d^? × %d^%d = %d^%d. What is the missing power?" % (b, b, n, b, tot), tot - n,
                ["Powers add when multiplying: ? + %d = %d." % (n, tot), "? = %d." % (tot - n)])


@_more("Y8.1.i", 10)
def _(d):
    b, m, n = pick(_by(d, [(2, 2, 2), (3, 2, 2), (10, 2, 2), (2, 1, 3)],
                       [(2, 2, 2), (2, 3, 2), (3, 2, 2), (2, 2, 3), (10, 2, 2), (5, 1, 3), (2, 4, 2)],
                       [(2, 3, 3), (3, 2, 3), (2, 2, 4), (10, 3, 2), (5, 2, 2), (3, 3, 2)]))
    return _int("Work out (%d^%d)^%d." % (b, m, n), b ** (m * n),
                ["(%d^%d)^%d = %d^%d." % (b, m, n, b, m * n), "= %s." % _c(b ** (m * n))])


@_more("Y8.1.j", 10)
def _(d):
    a, b = random.sample(range(_by(d, 2, 2, 6), _by(d, 8, 13, 16)), 2)
    return _int("Work out √%d + √%d." % (a * a, b * b), a + b, ["√%d = %d and √%d = %d." % (a * a, a, b * b, b), "%d + %d = %d." % (a, b, a + b)])


@_more("Y8.1.j", 10)
def _(d):
    a, b, c = pick(_by(d, [(3, 4, 5), (6, 8, 10)],
                       [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)],
                       [(5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37), (9, 40, 41)]))
    return _int("Work out √(%d + %d). (Add first, then take the square root.)" % (a * a, b * b), c,
                ["%d + %d = %d." % (a * a, b * b, c * c), "√%d = %d. (Not √%d + √%d = %d.)" % (c * c, c, a * a, b * b, a + b)])


@_more("Y8.1.j", 10)
def _(d):
    a = random.randint(2, _by(d, 4, 6, 10))
    return _int("Work out the cube root of −%d." % a ** 3, -a,
                ["(−%d) × (−%d) × (−%d) = −%d." % (a, a, a, a ** 3), "So the cube root is −%d." % a])


@_more("Y8.1.j", 10)
def _(d):
    x = pick(_by(d, ["0.5", "1.1", "1.2", "1.5", "0.9"], ["1.5", "1.2", "2.5", "0.9", "0.6", "1.1", "3.5", "0.7"],
                 ["1.3", "1.4", "1.6", "2.4", "3.2", "4.5", "0.8"]))
    a = Decimal(x) ** 2
    return _num("A square garden has an area of %s m². How long is each side, in metres?" % _ds(a), x,
                ["Side = √%s." % _ds(a), "%s × %s = %s, so the side is %s m." % (x, x, _ds(a), x)], "m")


@_more("Y8.1.j", 10)
def _(d):
    n = pick([x for x in range(_by(d, 10, 10, 100), _by(d, 50, 120, 300)) if isqrt(x) ** 2 != x])
    r = _round(Decimal(n).sqrt(), 1)
    lo = isqrt(n)
    return _num("Without a calculator, √%d lies between %d and %d. Using a calculator, give √%d correct to 1 decimal place."
                % (n, lo, lo + 1, n), r, ["√%d = %s…" % (n, str(Decimal(n).sqrt())[:6]), "To 1 d.p.: %s." % _ds(r)], tol=0.05)


@_more("Y8.1.j", 10)
def _(d):
    k = random.randint(_by(d, 3, 3, 9), _by(d, 6, 11, 15))
    n = k * k + random.choice([-3, -2, -1, 1, 2, 3])
    return _yn("Is √%d greater than %d?" % (n, k), n > k * k,
               ["%d = √%d." % (k, k * k), "√%d is %s than √%d." % (n, "greater" if n > k * k else "less", k * k)])


@_more("Y8.1.j", 10)
def _(d):
    while True:
        n = random.randint(_by(d, 5, 5, 30), _by(d, 30, 95, 99))
        r = n ** 0.5
        near = round(r * 2) / 2.0
        if isqrt(n) ** 2 != n and abs(r - near) < 0.15:
            break
    return _nld("Estimate where √%d belongs and mark it on the number line." % n, near, 0, 10, Decimal("0.5"), 1,
                ["%d² = %d and %d² = %d." % (isqrt(n), isqrt(n) ** 2, isqrt(n) + 1, (isqrt(n) + 1) ** 2),
                 "√%d ≈ %.2f, so it is close to %s." % (n, r, _ds(Decimal(str(near))))])


# ================================================================== 8.2 ======
@_more("Y8.2.c", 8)
def _(d):
    q = random.randint(2, _by(d, 9, 12, 25))
    dv = Decimal(random.randint(2, 9)) / 10
    a = q * dv
    return _int("Work out %s ÷ %s." % (_ds(a), _ds(dv)), q,
                ["Multiply both numbers by 10: %s ÷ %s." % (_ds(a * 10), _ds(dv * 10)), "= %d." % q])


@_more("Y8.2.c", 8)
def _(d):
    q = random.randint(2, _by(d, 9, 12, 30))
    dv = Decimal(random.randint(2, 9)) / 100
    a = q * dv
    return _int("Work out %s ÷ %s." % (_ds(a), _ds(dv)), q,
                ["Multiply both numbers by 100: %s ÷ %s." % (_ds(a * 100), _ds(dv * 100)), "= %d." % q])


@_more("Y8.2.c", 8)
def _(d):
    q = random.randint(2, 12)
    dv = Decimal(random.randint(2, 9)) / pick([10, 100])
    a = q * dv
    k = 10 if dv * 10 == int(dv * 10) else 100
    return _int("%s ÷ %s gives the same answer as %s ÷ ?. What is the missing whole number?" % (_ds(a), _ds(dv), _ds(a * k)),
                int(dv * k), ["Multiply both numbers by %d." % k, "%s × %d = %d." % (_ds(dv), k, int(dv * k))])


@_more("Y8.2.c", 8)
def _(d):
    bag = pick(["0.25", "0.4", "0.5", "0.75", "0.2", "1.5", "0.45", "0.6"])
    n = random.randint(4, 40)
    tot = Decimal(bag) * n
    thing = pick([("rice", "kg"), ("sand", "kg"), ("juice", "litres")])
    return _int("%s %s of %s is put into bags of %s %s each. How many bags can be filled?" % (_ds(tot), thing[1], thing[0], bag, thing[1]),
                n, ["%s ÷ %s = %d." % (_ds(tot), bag, n)], "bags")


@_more("Y8.2.c", 8)
def _(d):
    a, b = pick([(7, 4), (3, 8), (9, 4), (5, 8), (13, 4), (7, 8), (11, 20), (17, 25), (9, 40), (21, 8)])
    v = Decimal(a) / b
    return _num("Work out %d ÷ %d as a decimal." % (a, b), v, ["Divide, adding zeros after the decimal point: %d ÷ %d = %s." % (a, b, _ds(v))])


@_more("Y8.2.c", 8)
def _(d):
    a = random.randint(2, 15)
    dv = pick(["0.5", "0.25", "0.2", "0.1"])
    right = Decimal(a) / Decimal(dv)
    wrong = Decimal(a) * Decimal(dv)
    return _int("%s says %d ÷ %s = %s. What is the correct answer?" % (_who(), a, dv, _ds(wrong)), right,
                ["Dividing by a number less than 1 makes the answer bigger.",
                 "%d ÷ %s = %s (there are %s lots of %s in %d)." % (a, dv, _ds(right), _ds(right), dv, a)])


@_more("Y8.2.c", 8)
def _(d):
    n = pick([4, 5, 8])
    each = Decimal(random.randint(105, 495)) / 100
    while (each * n * 100) % 1:
        each = Decimal(random.randint(105, 495)) / 100
    tot = each * n
    mean = tot / n
    return _num("%d parcels weigh %s kg altogether. What is their mean mass, in kg?" % (n, _ds(tot)), mean,
                ["Mean = total ÷ number = %s ÷ %d." % (_ds(tot), n), "= %s kg." % _ds(mean)], "kg")


@_more("Y8.2.d", 8)
def _(d):
    x = Decimal(random.randint(11, _by(d, 99, 999, 9999))) / pick(_by(d, [1], [1, 10], [10, 100]))
    if random.random() < 0.5:
        v = x * Decimal("0.1")
        return _num("Work out %s × 0.1." % _ds(x), v, ["Multiplying by 0.1 is the same as dividing by 10.", "= %s." % _ds(v)])
    v = x / Decimal("0.1")
    return _num("Work out %s ÷ 0.1." % _ds(x), v, ["Dividing by 0.1 is the same as multiplying by 10.", "= %s." % _ds(v)])


@_more("Y8.2.d", 8)
def _(d):
    x = Decimal(random.randint(11, _by(d, 99, 999, 9999))) / pick(_by(d, [1], [1, 10, 100], [10, 100, 1000]))
    if random.random() < 0.5:
        v = x / Decimal("0.01")
        return _num("Work out %s ÷ 0.01." % _ds(x), v, ["Dividing by 0.01 is the same as multiplying by 100.", "= %s." % _ds(v)])
    v = x * Decimal("0.01")
    return _num("Work out %s × 0.01." % _ds(x), v, ["Multiplying by 0.01 is the same as dividing by 100.", "= %s." % _ds(v)])


@_more("Y8.2.d", 8)
def _(d):
    big, small, k = pick([("mm", "m", 1000), ("g", "kg", 1000), ("ml", "litres", 1000), ("cm", "m", 100), ("m", "km", 1000)])
    n = _by(d, random.randint(11, 99) * (k // 10), random.randint(25, 9999), random.randint(5, 99999))
    v = Decimal(n) / k
    if random.random() < 0.5:
        return _num("Convert %s %s into %s." % (_c(n), big, small), v,
                    ["There are %s %s in 1 %s, so divide by %s." % (_c(k), big, "litre" if small == "litres" else small, _c(k)),
                     "%s ÷ %s = %s." % (_c(n), _c(k), _ds(v))], small)
    return _num("Convert %s %s into %s." % (_ds(v), small, big), n, ["Multiply by %s." % _c(k), "%s × %s = %s." % (_ds(v), _c(k), _c(n))], big)


@_more("Y8.2.d", 8)
def _(d):
    x = random.randint(11, _by(d, 99, 99, 999))
    p, q = random.sample(_by(d, [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]), 2)
    a, b = Decimal(x) / 10 ** max(p, q), Decimal(x) / 10 ** min(p, q)
    return _int("How many times bigger is %s than %s?" % (_ds(b), _ds(a)), 10 ** abs(p - q),
                ["The digits are the same; they have moved %s." % ("1 place" if abs(p - q) == 1 else "%d places" % abs(p - q)), "So it is %s times bigger." % _c(10 ** abs(p - q))])


@_more("Y8.2.d", 8)
def _(d):
    x = Decimal(random.randint(11, _by(d, 99, 999, 9999))) / _by(d, 10, 10, 100)
    pool = [("× 10", 10), ("× 100", 100), ("÷ 10", Decimal("0.1")), ("÷ 1000", Decimal("0.001")),
            ("× 1000", 1000), ("÷ 100", Decimal("0.01"))]
    while True:
        ops = random.sample(pool[:3] + pool[5:] if d == 0 else pool, 2)     # easy: no 1000s
        if ops[0][1] * ops[1][1] != 1:
            break
    v = x * ops[0][1] * ops[1][1]
    return _num("Work out %s %s %s." % (_ds(x), ops[0][0], ops[1][0]), v,
                ["%s %s = %s." % (_ds(x), ops[0][0], _ds(x * ops[0][1])), "%s %s = %s." % (_ds(x * ops[0][1]), ops[1][0], _ds(v))])


@_more("Y8.2.d", 8)
def _(d):
    ops = [("× 10", Decimal(10)), ("× 100", Decimal(100)), ("× 1000", Decimal(1000)),
           ("÷ 10", Decimal("0.1")), ("÷ 100", Decimal("0.01")), ("÷ 1000", Decimal("0.001"))]
    rows = []
    for name, k in random.sample(ops if d else ops[:2] + ops[3:5], 4):
        n = Decimal(random.randint(11, _by(d, 99, 9999, 99999))) / pick(_by(d, [10], [10, 100], [100, 1000]))
        rows.append([_ds(n), name, _ds(n * k)])
    i = random.randrange(4)
    return _dt("Each row applies the operation to the number. What goes in the empty cell?",
               ["Number", "Operation", "Answer"], rows, rows[i][2],
               ["%s %s: the digits move %s %s." % (rows[i][0], rows[i][1],
                                                 {"10": "1 place", "100": "2 places", "1000": "3 places"}[rows[i][1][2:]],
                                                       "left" if rows[i][1][0] == "×" else "right"),
                "= %s." % rows[i][2]], missing=(i, 2), atype="num")


# ================================================================== 8.3 ======
def _simp_str(f):
    f = Fraction(f)
    return "%d/%d" % (f.numerator, f.denominator)


@_more("Y8.3.a", 9)
def _(d):
    while True:
        a, b = random.randint(1, 11), random.randint(2, 12)
        if a < b and gcd(a, b) == 1:
            break
    k = random.randint(2, _by(d, 5, 9, 12))
    return _wq("Write %d/%d in its simplest form (like 3/4)." % (a * k, b * k), "%d/%d" % (a, b),
               ["The highest common factor of %d and %d is %d." % (a * k, b * k, k),
                "%d ÷ %d = %d and %d ÷ %d = %d, so %d/%d." % (a * k, k, a, b * k, k, b, a, b)], "e.g. 3/4")


@_more("Y8.3.a", 9)
def _(d):
    m = pick([5, 10, 12, 15, 20, 24, 25, 30, 35, 36, 40, 45, 48, 50])
    f = Fraction(m, 60)
    return _wq("%s spends %d minutes of an hour on homework. What fraction of the hour is that? Give it in its "
               "simplest form (like 3/4)." % (_who(), m), _simp_str(f),
               ["%d minutes out of 60 is %d/60." % (m, m), "%d/60 = %s." % (m, _simp_str(f))], "e.g. 3/4")


@_more("Y8.3.a", 9)
def _(d):
    a, b = pick([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6), (3, 8), (5, 8), (7, 10)])
    ks = random.sample(range(2, 8), 3)
    good = ["%d/%d" % (a * k, b * k) for k in ks]
    k = random.randint(2, 7)
    bad = "%d/%d" % (a * k + 1, b * k)
    shown = good + [bad]
    random.shuffle(shown)
    return _wq("Which of these is NOT equivalent to %d/%d?   %s" % (a, b, ",  ".join(shown)), bad,
               ["Simplify each one: %s all simplify to %d/%d." % (", ".join(good), a, b),
                "%s does not simplify to %d/%d." % (bad, a, b)], "type the fraction")


@_more("Y8.3.a", 9)
def _(d):
    while True:
        a, b = random.randint(1, 9), random.randint(2, 11)
        if a < b and gcd(a, b) == 1:
            break
    k = random.randint(4, _by(d, 8, 12, 16))
    return _int("What is the largest number you can divide both %d and %d by, to simplify %d/%d in one step?"
                % (a * k, b * k, a * k, b * k), k,
                ["That is the highest common factor of %d and %d." % (a * k, b * k), "HCF = %d." % k])


@_more("Y8.3.a", 9)
def _(d):
    b = pick([2, 4, 5, 10, 20, 25, 50])
    a = pick([x for x in range(1, b) if gcd(x, b) == 1])
    return _int("%d/%d = ?/100. What is the missing numerator?" % (a, b), a * 100 // b,
                ["100 ÷ %d = %d, so multiply the top and bottom by %d." % (b, 100 // b, 100 // b),
                 "%d × %d = %d." % (a, 100 // b, a * 100 // b)])


@_more("Y8.3.a", 9)
def _(d):
    a, b = pick([(1, 2), (1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (5, 6), (4, 7), (3, 8)])
    ks = [1, 2, 3, 4, 5]
    i = random.randrange(1, 5)
    row = random.randrange(2)
    rows = [["Numerator"] + [str(a * k) for k in ks], ["Denominator"] + [str(b * k) for k in ks]]
    return _dt("Every column of the table is a fraction equivalent to %d/%d. What goes in the empty cell?" % (a, b),
               ["", "×1", "×2", "×3", "×4", "×5"], rows, (a if row == 0 else b) * ks[i],
               ["That column is %d/%d multiplied top and bottom by %d." % (a, b, ks[i]),
                "%d × %d = %d." % (a if row == 0 else b, ks[i], (a if row == 0 else b) * ks[i])],
               missing=(row, i + 1))


@_more("Y8.3.c", 11)
def _(d):
    while True:
        fs = [Fraction(random.randint(1, _by(d, 7, 11, 19)), random.randint(3, _by(d, 8, 12, 20))) for _ in range(3)]
        gaps = [abs(f - Fraction(1, 2)) for f in fs]
        if len(set(fs)) == 3 and all(0 < f < 1 for f in fs) and sorted(gaps)[0] < sorted(gaps)[1] and Fraction(1, 2) not in fs:
            break
    best = fs[gaps.index(min(gaps))]
    shown = ["%d/%d" % (f.numerator, f.denominator) for f in fs]
    return _wq("Which of these fractions is closest to 1/2?   %s" % ",  ".join(shown), "%d/%d" % (best.numerator, best.denominator),
               ["Compare each with 1/2: %s." % ";  ".join("%s is %s away" % (s, _simp_str(g)) for s, g in zip(shown, gaps)),
                "%s is closest." % _simp_str(best)], "type the fraction")


@_more("Y8.3.c", 11)
def _(d):
    while True:
        b1, b2 = random.sample(_by(d, [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 9, 10, 12], [4, 6, 8, 9, 10, 12, 15]), 2)
        l = _lcm(b1, b2)
        if l <= _by(d, 24, 40, 60) and l not in (b1, b2):
            break
    a2 = pick([x for x in range(1, b2) if gcd(x, b2) == 1])
    return _int("To compare fractions with denominators %d and %d you rewrite both with denominator %d. "
                "%d/%d = ?/%d. What is the missing numerator?" % (b1, b2, l, a2, b2, l), a2 * l // b2,
                ["%d ÷ %d = %d." % (l, b2, l // b2), "%d × %d = %d." % (a2, l // b2, a2 * l // b2)])


@_more("Y8.3.c", 11)
def _(d):
    while True:
        f1 = Fraction(random.randint(1, _by(d, 4, 5, 9)), random.randint(2, _by(d, 5, 8, 12)))
        f2 = Fraction(random.randint(1, _by(d, 4, 5, 9)), random.randint(2, _by(d, 5, 8, 12)))
        if f1 != f2 and f1 < 1 and f2 < 1:
            break
    s1, s2 = "-%d/%d" % (f1.numerator, f1.denominator), "-%d/%d" % (f2.numerator, f2.denominator)
    big = s1 if -f1 > -f2 else s2
    return _wq("Which is larger: %s or %s? Type the larger one." % (s1.replace("-", "−"), s2.replace("-", "−")), big,
               ["For negative numbers, the one closer to zero is larger.",
                "%s is closer to zero, so it is larger." % big.replace("-", "−")], "e.g. -1/2")


@_more("Y8.3.c", 11)
def _(d):
    while True:
        b = random.randint(2, _by(d, 4, 6, 9))
        imp = Fraction(random.randint(b + 1, _by(d, 3, 4, 6) * b), b)
        w = random.randint(1, _by(d, 2, 3, 5))
        b2 = random.randint(2, _by(d, 5, 8, 12))
        mix = w + Fraction(random.randint(1, b2 - 1), b2)
        if imp != mix and imp.denominator == b and mix.denominator == b2:
            break
    s_imp = "%d/%d" % (imp.numerator, imp.denominator)
    s_mix = _mixed(mix)
    big = s_imp if imp > mix else s_mix
    return _wq("Which is larger: %s or %s? Type the larger one exactly as shown." % (s_imp, s_mix), big,
               ["%s = %s." % (s_imp, _mixed(imp)), "%s is larger." % big], "as shown")


@_more("Y8.3.c", 11)
def _(d):
    lo, hi, den, ans = pick(_by(d,
        [((1, 4), (1, 2), 8, 3), ((1, 5), (2, 5), 10, 3), ((1, 2), (3, 4), 8, 5), ((3, 5), (4, 5), 10, 7)],
        [((1, 3), (1, 2), 12, 5), ((1, 4), (1, 3), 24, 7), ((2, 5), (1, 2), 20, 9), ((1, 2), (2, 3), 12, 7),
         ((3, 4), (5, 6), 24, 19), ((1, 5), (1, 4), 40, 9), ((2, 3), (3, 4), 24, 17), ((3, 5), (2, 3), 30, 19)],
        [((3, 7), (1, 2), 28, 13), ((4, 9), (1, 2), 36, 17), ((5, 8), (2, 3), 48, 31), ((2, 7), (1, 3), 42, 13),
         ((5, 6), (6, 7), 84, 71), ((3, 8), (2, 5), 80, 31)]))
    return _fq("Write a fraction with denominator %d that lies between %d/%d and %d/%d." % (den, lo[0], lo[1], hi[0], hi[1]),
               Fraction(ans, den),
               ["%d/%d = %d/%d and %d/%d = %d/%d." % (lo[0], lo[1], lo[0] * den // lo[1], den, hi[0], hi[1], hi[0] * den // hi[1], den),
                "The only one in between is %d/%d." % (ans, den)], "e.g. 5/12")


@_more("Y8.3.c", 11)
def _(d):
    a, b = random.sample(NAMES, 2)
    while True:
        f1 = Fraction(random.randint(1, _by(d, 5, 7, 11)), random.randint(_by(d, 2, 3, 5), _by(d, 6, 9, 12)))
        f2 = Fraction(random.randint(1, _by(d, 5, 7, 11)), random.randint(_by(d, 2, 3, 5), _by(d, 6, 9, 12)))
        if f1 != f2 and f1 < 1 and f2 < 1 and abs(f1 - f2) < Fraction(1, _by(d, 4, 6, 12)):
            break
    win = a if f1 > f2 else b
    l = _lcm(f1.denominator, f2.denominator)
    return _wq("%s eats %s of a pizza. %s eats %s of an identical pizza. Who eats more?"
               % (a, _simp_str(f1), b, _simp_str(f2)), win,
               ["With denominator %d: %d/%d and %d/%d." % (l, f1 * l, l, f2 * l, l), "%s eats more." % win], "type a name")


@_more("Y8.3.c", 11)
def _(d):
    while True:
        fs = list({Fraction(random.randint(1, _by(d, 5, 9, 15)), random.randint(2, _by(d, 6, 10, 12))) for _ in range(4)})
        if len(fs) == 4 and all(f < 2 and f.denominator > 1 for f in fs):
            break
    order = sorted(fs, reverse=True)
    shown = ["%d/%d" % (f.numerator, f.denominator) for f in fs]
    return _wq("Put these in order from largest to smallest. Which comes second?   %s" % ",  ".join(shown),
               "%d/%d" % (order[1].numerator, order[1].denominator),
               ["As decimals: %s." % ", ".join("%s = %s" % (s, str(round(float(f), 3))) for s, f in zip(shown, fs)),
                "Largest first: %s." % ", ".join(_simp_str(f) for f in order)], "type the fraction")


@_more("Y8.3.d", 8)
def _(d):
    a, b = pick(_by(d, [(1, 3), (2, 3), (1, 6), (5, 6), (1, 9), (4, 9)],
                    [(1, 3), (2, 3), (1, 6), (5, 6), (1, 7), (2, 9), (4, 9), (1, 11), (5, 7), (7, 12)],
                    [(1, 7), (5, 7), (5, 11), (7, 12), (5, 13), (4, 15), (11, 18), (7, 22), (13, 24)]))
    v = _round(Decimal(a) / b, 3)
    return _num("Write %d/%d as a decimal, correct to 3 decimal places." % (a, b), v,
                ["%d ÷ %d = %s… (it recurs)." % (a, b, str(Decimal(a) / b)[:8]), "To 3 d.p.: %s." % _ds(v)])


@_more("Y8.3.d", 8)
def _(d):
    a, b = pick(_by(d, [(1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (3, 10), (7, 10)],
                    [(3, 8), (5, 8), (7, 8), (1, 8), (3, 20), (7, 20), (9, 25), (3, 40), (11, 40), (17, 50), (7, 25)],
                    [(3, 40), (11, 40), (17, 80), (3, 16), (9, 16), (13, 125), (7, 200), (21, 250)]))
    v = Decimal(a) / b
    return _wq("Write %s as a fraction in its simplest form (like 3/8)." % _ds(v), "%d/%d" % (a, b),
               ["%s = %d/%d." % (_ds(v), int(v * 10 ** len(_ds(v).split(".")[1])), 10 ** len(_ds(v).split(".")[1])),
                "Simplify: %d/%d." % (a, b)], "e.g. 3/8")


@_more("Y8.3.d", 8)
def _(d):
    a, b = pick(_by(d, [(1, 4), (1, 3), (2, 5), (1, 6), (3, 10), (2, 7), (1, 8), (5, 9)],
                    [(7, 20), (3, 7), (5, 16), (2, 15), (9, 40), (4, 9), (11, 25), (5, 12), (13, 50), (1, 6), (3, 80), (7, 30)],
                    [(7, 40), (3, 14), (9, 80), (5, 24), (11, 125), (7, 60), (13, 64), (4, 75), (17, 160), (9, 35)]))
    def onlytwofive(n):
        while n % 2 == 0:
            n //= 2
        while n % 5 == 0:
            n //= 5
        return n == 1
    yes = onlytwofive(b)
    return _yn("Does %d/%d make a terminating decimal (one that stops)?" % (a, b), yes,
               ["%d/%d is in its simplest form. A fraction terminates only if the denominator's prime factors are 2s and 5s." % (a, b),
                "%d %s." % (b, "has only 2s and 5s" if yes else "has another prime factor")])


@_more("Y8.3.d", 8)
def _(d):
    while True:
        fs = [Fraction(random.randint(1, 9), pick(_by(d, [2, 4, 5, 10], [4, 5, 8, 10, 20, 25], [8, 16, 20, 25, 40])))
              for _ in range(2)]
        ds = [_by(d, Decimal(random.randint(1, 9)) / 10, Decimal(random.randint(10, 99)) / 100,
                  Decimal(random.randint(101, 999)) / 1000) for _ in range(2)]
        vals = [Decimal(f.numerator) / f.denominator for f in fs] + ds
        if all(v < 1 for v in vals) and len(set(vals)) == 4:
            break
    shown = ["%d/%d" % (f.numerator, f.denominator) for f in fs] + [_ds(x) for x in ds]
    idx = list(range(4))
    random.shuffle(idx)
    shown, vals = [shown[i] for i in idx], [vals[i] for i in idx]
    ans = shown[vals.index(min(vals))]
    return _wq("Which is the smallest?   %s   (type it exactly as shown)" % ",  ".join(shown), ans,
               ["As decimals: %s." % ", ".join(_ds(v) for v in vals), "The smallest is %s." % ans], "as shown")


@_more("Y8.3.d", 8)
def _(d):
    b = pick(_by(d, [2, 4, 5, 10], [20, 25, 50, 4, 5], [8, 40, 125, 200, 250]))
    a = pick([x for x in range(1, b) if gcd(x, b) == 1])
    v = Decimal(a) / b
    t = 1000 if d == 2 else 100                       # stretch: eighths etc need 1000
    return _num("Write %d/%d as a decimal by first making the denominator %d." % (a, b, t), v,
                ["%d/%d = %d/%d." % (a, b, a * t // b, t), "= %s." % _ds(v)])


@_more("Y8.3.d", 8)
def _(d):
    w = random.randint(1, _by(d, 5, 9, 99))
    a, b = pick(_by(d, [(1, 4), (3, 4), (1, 2), (1, 5), (2, 5)],
                    [(1, 4), (3, 4), (1, 2), (1, 5), (2, 5), (3, 5), (4, 5), (1, 8), (3, 8), (7, 8), (1, 20), (9, 20)],
                    [(1, 8), (3, 8), (5, 8), (7, 8), (9, 20), (3, 25), (7, 40), (1, 16), (11, 50)]))
    v = w + Decimal(a) / b
    return _wq("Write %s as a mixed number in its simplest form (like 2 3/4)." % _ds(v), "%d %d/%d" % (w, a, b),
               ["%s = %d + %s." % (_ds(v), w, _ds(v - w)), "%s = %d/%d, so %d %d/%d." % (_ds(v - w), a, b, w, a, b)], "e.g. 2 3/4")


def _two_unlike(d):
    while True:
        b1, b2 = random.sample(_by(d, [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 10], [4, 6, 7, 8, 9, 12]), 2)
        a1, a2 = random.randint(1, b1 - 1), random.randint(1, b2 - 1)
        if gcd(a1, b1) == 1 and gcd(a2, b2) == 1:
            return Fraction(a1, b1), Fraction(a2, b2)


@_more("Y8.3.e", 7)
def _(d):
    f, g = _two_unlike(d)
    l = _lcm(f.denominator, g.denominator)
    return _fq("Work out %s + %s. Give your answer as a fraction." % (_simp_str(f), _simp_str(g)), f + g,
               ["Common denominator %d: %d/%d + %d/%d." % (l, f * l, l, g * l, l), "= %s." % _simp_str(f + g)])


@_more("Y8.3.e", 7)
def _(d):
    f, g = _two_unlike(d)
    f, g = max(f, g), min(f, g)
    l = _lcm(f.denominator, g.denominator)
    return _fq("Work out %s − %s. Give your answer as a fraction." % (_simp_str(f), _simp_str(g)), f - g,
               ["Common denominator %d: %d/%d − %d/%d." % (l, f * l, l, g * l, l), "= %s." % _simp_str(f - g)])


@_more("Y8.3.e", 7)
def _(d):
    while True:
        f, g = _two_unlike(d)
        if f + g < 1:
            break
    return _fq("%s + ? = %s. What is the missing fraction?" % (_simp_str(f), _simp_str(f + g)), g,
               ["? = %s − %s." % (_simp_str(f + g), _simp_str(f)), "= %s." % _simp_str(g)])


@_more("Y8.3.e", 7)
def _(d):
    full, used = pick([(Fraction(3, 4), Fraction(1, 3)), (Fraction(2, 3), Fraction(1, 4)), (Fraction(5, 6), Fraction(1, 4)),
                       (Fraction(7, 8), Fraction(1, 3)), (Fraction(4, 5), Fraction(1, 2)), (Fraction(9, 10), Fraction(2, 5))])
    return _fq("A water tank is %s full. Then %s of the whole tank is used. What fraction of the tank is full now?"
               % (_simp_str(full), _simp_str(used)), full - used,
               ["%s − %s." % (_simp_str(full), _simp_str(used)), "= %s." % _simp_str(full - used)])


@_more("Y8.3.e", 7)
def _(d):
    while True:
        f, g = _two_unlike(d)
        if f + g < 1:
            break
    who = _who()
    return _fq("%s spends %s of their pocket money on a book and %s on snacks. What fraction is left?"
               % (who, _simp_str(f), _simp_str(g)), 1 - f - g,
               ["Spent: %s + %s = %s." % (_simp_str(f), _simp_str(g), _simp_str(f + g)),
                "Left: 1 − %s = %s." % (_simp_str(f + g), _simp_str(1 - f - g))])


@_more("Y8.3.e", 7)
def _(d):
    while True:
        f, g = _two_unlike(d)
        w1, w2 = random.randint(3, 7), random.randint(1, 2)
        a, b = w1 + min(f, g), w2 + max(f, g)
        if a > b:
            break
    return _tb("Work out %s − %s. Give your answer as a mixed number." % (_mixed(a), _mixed(b)), _mixed(a - b), "frac",
               {"text": True, "placeholder": "e.g. 1 5/12"},
               ["Change to improper fractions or borrow 1 from the whole number.",
                "%s − %s = %s." % (_mixed(a), _mixed(b), _mixed(a - b))])


@_more("Y8.3.e", 7)
def _(d):
    f, g = _two_unlike(d)
    return _fq("%s says %s + %s = %d/%d. What is the correct answer?" % (_who(), _simp_str(f), _simp_str(g),
                                                                      f.numerator + g.numerator, f.denominator + g.denominator),
               f + g, ["You cannot add the denominators.", "Use a common denominator: %s." % _simp_str(f + g)])


@_more("Y8.3.g", 8)
def _(d):
    while True:
        b = pick(_by(d, [2, 4, 5, 10], [4, 8, 5, 10, 20], [8, 20, 25, 40]))
        a = pick([x for x in range(1, b) if gcd(x, b) == 1])
        q = random.randint(3, _by(d, 20, 60, 150))
        v = Fraction(a * q, b)
        if v.denominator > 1 and (v * 100).denominator == 1:
            break
    unit = pick(["kg", "m", "litres"])
    return _num("Work out %d/%d of %d %s." % (a, b, q, unit), _dec(v),
                ["%d ÷ %d = %s." % (q, b, _ds(Decimal(q) / b)), "× %d = %s %s." % (a, _ds(_dec(v)), unit)], unit)


@_more("Y8.3.g", 8)
def _(d):
    b = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 6, 8], [6, 7, 8, 9, 12]))
    a = pick([x for x in range(1, b) if gcd(x, b) == 1])
    tot = b * random.randint(_by(d, 2, 3, 8), _by(d, 10, 20, 40))
    left = tot - tot * a // b
    return _int("%s has £%d and spends %d/%d of it. How much is left, in pounds?" % (_who(), tot, a, b), left,
                ["Spent: %d ÷ %d × %d = £%d." % (tot, b, a, tot * a // b), "Left: %d − %d = £%d." % (tot, tot * a // b, left)], "£")


@_more("Y8.3.g", 8)
def _(d):
    b = pick(_by(d, [3, 4, 5], [3, 4, 5, 6, 7, 8], [7, 8, 9, 11, 12]))
    a = pick([x for x in range(2, b) if gcd(x, b) == 1])
    whole = b * random.randint(_by(d, 2, 2, 5), _by(d, 8, 15, 25))
    return _int("%d/%d of a number is %d. What is the number?" % (a, b, whole * a // b), whole,
                ["1/%d of the number is %d ÷ %d = %d." % (b, whole * a // b, a, whole // b),
                 "The number is %d × %d = %d." % (whole // b, b, whole)])


@_more("Y8.3.g", 8)
def _(d):
    F = Fraction
    f1, f2 = pick(_by(d, [(F(1, 2), F(1, 2)), (F(1, 2), F(1, 4)), (F(1, 4), F(1, 2)), (F(1, 3), F(1, 2))],
                      [(F(1, 2), F(1, 3)), (F(2, 3), F(1, 4)), (F(3, 4), F(1, 3)),
                       (F(1, 3), F(1, 4)), (F(2, 5), F(1, 2)), (F(3, 5), F(1, 3))],
                      [(F(3, 4), F(2, 5)), (F(5, 6), F(3, 5)), (F(2, 3), F(3, 8)), (F(4, 5), F(5, 6)), (F(3, 8), F(2, 3))]))
    n = (f1 * f2).denominator * random.randint(_by(d, 1, 2, 2), _by(d, 4, 6, 8))
    while (n * f1).denominator != 1:
        n += (f1 * f2).denominator
    first = n * f1
    return _int("A club has %d members. %s of them are juniors, and %s of the juniors play in the team. How many juniors "
                "play in the team?" % (n, _simp_str(f1), _simp_str(f2)), first * f2,
                ["Juniors: %s of %d = %d." % (_simp_str(f1), n, first), "%s of %d = %d." % (_simp_str(f2), first, first * f2)])


@_more("Y8.3.g", 8)
def _(d):
    whole, small, big = pick([(60, "minutes", "an hour"), (24, "hours", "a day"), (1000, "metres", "a kilometre"),
                              (360, "degrees", "a full turn"), (100, "pence", "a pound")])
    b = pick([x for x in _by(d, (2, 4, 5, 10), (2, 3, 4, 5, 6, 8, 10, 12), (3, 6, 8, 12, 20, 25))
              if whole % x == 0 and x < whole])
    a = pick([x for x in range(_by(d, 1, 1, 2), b) if gcd(x, b) == 1])
    return _int("How many %s are in %d/%d of %s?" % (small, a, b, big), whole * a // b,
                ["There are %d %s in %s." % (whole, small, big),
                 "%d ÷ %d × %d = %d %s." % (whole, b, a, whole * a // b, small)])


@_more("Y8.3.g", 8)
def _(d):
    while True:
        b1, b2 = random.sample(_by(d, [2, 4, 5, 10], [3, 4, 5, 6, 8], [6, 7, 8, 9, 12]), 2)
        a1, a2 = random.randint(1, b1 - 1), random.randint(1, b2 - 1)
        lo, hi = _by(d, (2, 8), (3, 15), (5, 25))
        q1, q2 = b1 * random.randint(lo, hi), b2 * random.randint(lo, hi)
        v1, v2 = q1 * a1 // b1, q2 * a2 // b2
        if v1 != v2 and gcd(a1, b1) == 1 and gcd(a2, b2) == 1:
            break
    return _int("Which is greater: %d/%d of %d or %d/%d of %d? Type the value of the greater one." % (a1, b1, q1, a2, b2, q2),
                max(v1, v2), ["%d/%d of %d = %d." % (a1, b1, q1, v1), "%d/%d of %d = %d." % (a2, b2, q2, v2),
                              "The greater value is %d." % max(v1, v2)])


@_more("Y8.3.g", 8)
def _(d):
    p1, p2 = pick(_by(d, [(2, 4), (2, 6), (4, 2), (3, 6), (4, 8)],
                      [(4, 6), (4, 10), (6, 9), (8, 12), (4, 3), (6, 4), (10, 4), (5, 8)],
                      [(6, 9), (8, 12), (6, 4), (5, 8), (12, 9), (8, 6)]))
    gs = _by(d, [100, 200, 300], [100, 150, 200, 250, 300, 400, 450, 600], [150, 250, 360, 450, 480, 600, 750])
    g = pick(gs)
    while (g * p2) % p1:
        g = pick(gs)
    f = Fraction(p2, p1)
    return _int("A recipe for %d people uses %d g of flour. How much flour is needed for %d people, in grams?" % (p1, g, p2),
                g * p2 // p1, ["Scale by %d/%d%s." % (p2, p1, "" if f.denominator == p1 else " = " + _simp_str(f)),
                               "%d × %s = %d g." % (g, _simp_str(f), g * p2 // p1)], "g")


# ================================================================== 8.4 ======
@_more("Y8.4.b", 9)
def _(d):
    r = sorted(random.sample(range(1, 8), 3))
    random.shuffle(r)
    unit = random.randint(2, _by(d, 6, 12, 25))
    tot = sum(r) * unit
    return _int("£%d is shared in the ratio %d : %d : %d. How much is the largest share, in pounds?" % (tot, r[0], r[1], r[2]),
                max(r) * unit, ["%d + %d + %d = %d parts; one part = %d ÷ %d = £%d." % (r[0], r[1], r[2], sum(r), tot, sum(r), unit),
                                "Largest share: %d × %d = £%d." % (max(r), unit, max(r) * unit)], "£")


@_more("Y8.4.b", 9)
def _(d):
    while True:
        a, b = random.sample(range(1, 10), 2)
        if gcd(a, b) == 1:
            break
    a, b = max(a, b), min(a, b)
    unit = random.randint(2, 15)
    things = pick(["stickers", "marbles", "cards", "sweets"])
    n1, n2 = random.sample(NAMES, 2)
    return _int("%s and %s share some %s in the ratio %d : %d. %s gets %d more than %s. How many %s are there altogether?"
                % (n1, n2, things, a, b, n1, (a - b) * unit, n2, things), (a + b) * unit,
                ["The difference is %d − %d = %s = %d, so one part is %d." % (a, b, _pl(a - b, "part"), (a - b) * unit, unit),
                 "Total: %d parts × %d = %d." % (a + b, unit, (a + b) * unit)])


@_more("Y8.4.b", 9)
def _(d):
    while True:
        a, b = random.sample(range(1, 10), 2)
        if gcd(a, b) == 1:
            break
    unit = random.randint(2, 15)
    thing = pick([("blue paint", "yellow paint", "litres"), ("flour", "sugar", "g"), ("sand", "cement", "kg")])
    if thing[2] == "g":
        unit *= 50
    return _int("%s and %s are mixed in the ratio %d : %d. There are %d %s of %s. How much %s is there, in %s?"
                % (thing[0].capitalize(), thing[1], a, b, a * unit, thing[2], thing[0], thing[1], thing[2]), b * unit,
                ["%s = %d %s, so one part = %d %s." % (_pl(a, "part"), a * unit, thing[2], unit, thing[2]),
                 "%s = %d %s." % (_pl(b, "part"), b * unit, thing[2])], thing[2])


@_more("Y8.4.b", 9)
def _(d):
    a, b = pick([(1, 3), (3, 1), (1, 4), (3, 5), (1, 7), (7, 13), (2, 3), (9, 11), (3, 17), (1, 19)])
    return _num("Red and blue counters are in the ratio %d : %d. What percentage of the counters are blue?" % (a, b),
                Decimal(100 * b) / (a + b), ["Blue is %d out of %d parts = %d/%d." % (b, a + b, b, a + b),
                                             "%d/%d × 100 = %s%%." % (b, a + b, _ds(Decimal(100 * b) / (a + b)))], "%")


@_more("Y8.4.b", 9)
def _(d):
    unit = random.randint(2, _by(d, 5, 10, 20))
    tot = 7 * unit
    part, k = pick([("cement", 1), ("sand", 2), ("gravel", 4)])
    return _int("Concrete is made from cement, sand and gravel in the ratio 1 : 2 : 4. How much %s is in %d kg of concrete, in kg?"
                % (part, tot), k * unit, ["1 + 2 + 4 = 7 parts; one part = %d ÷ 7 = %d kg." % (tot, unit),
                                         "%s is %d %s: %d kg." % (part.capitalize(), k, "part" if k == 1 else "parts", k * unit)], "kg")


@_more("Y8.4.b", 9)
def _(d):
    r = random.sample(range(1, 7), 3)
    unit = random.randint(2, 10) * 5
    names = ["Ana", "Bo", "Cy"]
    return _bar("Three friends share prize money in the ratio %d : %d : %d. The bar chart shows the shares of Ana and Bo, in "
                "pounds. How much does Cy get, in pounds?" % tuple(r), names[:2], [r[0] * unit, r[1] * unit], r[2] * unit,
                ["Ana's %s £%d, so one part is £%d." % ("1 part is" if r[0] == 1 else "%d parts are" % r[0], r[0] * unit, unit),
                 "Cy gets %d × %d = £%d." % (r[2], unit, r[2] * unit)])


@_more("Y8.4.e", 9)
def _(d):
    v = pick(_by(d, [10, 20, 30], [5, 10, 15, 20, 25, 30], [15, 25, 35, 45]))
    if random.random() < 0.5:
        return _int("A car travels at %d m/s. What is its speed in km/h? (1 m/s = 3.6 km/h)" % v, v * Decimal("3.6"),
                    ["%d m/s × 3600 s = %s m in an hour = %s km." % (v, _c(v * 3600), _ds(Decimal(v * 3600) / 1000)), "So %s km/h." % _ds(v * Decimal("3.6"))], "km/h")
    k = v * Decimal("3.6")
    return _int("A train travels at %s km/h. What is its speed in metres per second?" % _ds(k), v,
                ["%s km/h = %s m in 3600 seconds." % (_ds(k), _c(int(k * 1000))), "%s ÷ 3600 = %d m/s." % (_c(int(k * 1000)), v)], "m/s")


@_more("Y8.4.e", 9)
def _(d):
    while True:
        s1, s2 = random.sample(_by(d, [20, 30, 40, 60], [20, 30, 40, 45, 50, 60, 80, 90, 100, 120],
                                   [36, 40, 45, 48, 54, 60, 72, 80, 90]), 2)
        dist = _lcm(s1, s2) * random.randint(1, _by(d, 1, 2, 3))
        t = Fraction(dist, s1) + Fraction(dist, s2)
        av = Fraction(2 * dist) / t
        if av.denominator == 1 and dist <= _by(d, 240, 400, 720):
            break
    return _int("A car drives %d km at %d km/h and then another %d km at %d km/h. What is its average speed for the whole "
                "journey, in km/h?" % (dist, s1, dist, s2), av,
                ["Time: %d ÷ %d = %s h and %d ÷ %d = %s h, total %s h." % (dist, s1, _ds(_dec(Fraction(dist, s1))), dist, s2, _ds(_dec(Fraction(dist, s2))), _ds(_dec(t))),
                 "Average speed = total distance ÷ total time = %d ÷ %s = %d km/h (not the mean of the two speeds)."
                 % (2 * dist, _ds(_dec(t)), av)], "km/h")


@_more("Y8.4.e", 9)
def _(d):
    lo, hi, k = _by(d, (2, 5, 2), (2, 6, 4), (4, 9, 4))
    s1, s2 = random.randint(lo, hi) * k, random.randint(lo, hi) * k
    # ride r1 hours, stop for `st` hours, then ride r2 more hours (core/stretch vary every leg)
    r1 = pick(_by(d, [2], [1, 2, 3], [2, 3]))
    st = pick(_by(d, [1, 2], [1, 2, 3], [1, 2, 3]))
    r2 = pick(_by(d, [1], [1, 2], [2]))
    pts = [(str(h), s1 * min(h, r1) + s2 * max(0, h - r1 - st)) for h in range(r1 + st + r2 + 1)]
    ask = random.randrange(3)
    q = ["What was the cyclist's speed in the first %s, in km/h?" % _pl(r1, "hour"),
         "For how many hours did the cyclist stop?",
         "What was the cyclist's speed in the last %s, in km/h?" % _pl(r2, "hour")][ask]
    q = q.replace("first 1 hour", "first hour").replace("last 1 hour", "last hour")
    ans = [s1, st, s2][ask]
    return _lg("The distance–time graph shows a cycle ride. %s" % q, pts, ans,
               ["A flat part of the graph means no distance is covered (stopped).",
                ["%d km in %s = %d km/h." % (r1 * s1, _pl(r1, "hour"), s1),
                 "From hour %d to hour %d the line is flat: %s." % (r1, r1 + st, _pl(st, "hour")),
                 "%d − %d = %d km in %s = %d km/h." % (r1 * s1 + r2 * s2, r1 * s1, r2 * s2, _pl(r2, "hour"), s2)][ask]],
               "km", "Time (hours)")


@_more("Y8.4.e", 9)
def _(d):
    mins = pick(_by(d, [30, 60, 120], [30, 45, 90, 120, 150, 75], [45, 84, 96, 105, 135]))
    sp = _by(d, random.randint(5, 15) * 4, random.randint(10, 30) * 4, random.randint(3, 6) * 20)
    dist = sp * mins // 60
    h, m = random.randint(7, 15), pick([0, 10, 15, 20, 30, 45])
    arr = h * 60 + m + mins
    return _dt("The timetable shows a train journey of %d km. What is the train's average speed, in km/h?" % dist,
               ["Leaves", "Arrives", "Distance"], [["%02d:%02d" % (h, m), "%02d:%02d" % (arr // 60, arr % 60), "%d km" % dist]], sp,
               ["The journey takes %d minutes = %s hour%s." % (mins, _ds(Decimal(mins) / 60), "" if mins == 60 else "s"),
                "%d ÷ %s = %d km/h." % (dist, _ds(Decimal(mins) / 60), sp)])


@_more("Y8.4.e", 9)
def _(d):
    m = _by(d, random.randint(2, 8) * 25, random.randint(6, 18) * 5, random.randint(55, 150))
    v = Decimal(m) * 60 / 1000
    return _num("%s walks %d metres every minute. What is that speed in km/h?" % (_who(), m), v,
                ["In an hour: %d × 60 = %s m." % (m, _c(m * 60)), "%s m = %s km, so %s km/h." % (_c(m * 60), _ds(v), _ds(v))], "km/h")


@_more("Y8.4.e", 9)
def _(d):
    while True:
        t1, t2 = random.randint(2, _by(d, 3, 5, 9)), random.randint(2, _by(d, 3, 5, 9))
        s1, s2 = _by(d, (random.randint(3, 9) * 10, random.randint(3, 9) * 10),
                     (random.randint(30, 90), random.randint(30, 90)),
                     (random.randint(45, 130), random.randint(45, 130)))
        if s1 != s2:
            break
    return _int("Car A travels %d km in %d hours. Car B travels %d km in %d hours. How much faster is the faster car, in km/h?"
                % (s1 * t1, t1, s2 * t2, t2), abs(s1 - s2),
                ["A: %d ÷ %d = %d km/h. B: %d ÷ %d = %d km/h." % (s1 * t1, t1, s1, s2 * t2, t2, s2),
                 "Difference: %d km/h." % abs(s1 - s2)], "km/h")


@_more("Y8.4.f", 8)
def _(d):
    cur, rate = pick(_by(d, [("Australian dollars", "2"), ("euros", "1.2"), ("Swiss francs", "1.1")],
                         [("euros", "1.15"), ("euros", "1.2"), ("US dollars", "1.25"), ("US dollars", "1.3"), ("Swiss francs", "1.1")],
                         [("euros", "1.16"), ("US dollars", "1.27"), ("Swiss francs", "1.12"), ("Canadian dollars", "1.74")]))
    n = _by(d, random.randint(1, 10) * 10, random.randint(2, 40) * 10, random.randint(12, 400))
    if random.random() < 0.5:
        return _num("£1 is worth %s %s. How many %s do you get for £%d?" % (rate, cur, cur, n), Decimal(rate) * n,
                    ["%d × %s = %s." % (n, rate, _ds(Decimal(rate) * n))])
    return _num("£1 is worth %s %s. How many pounds is %s %s worth?" % (rate, cur, _ds(Decimal(rate) * n), cur), n,
                ["%s ÷ %s = %d." % (_ds(Decimal(rate) * n), rate, n)], "£")


@_more("Y8.4.f", 8)
def _(d):
    p1, p2 = pick(_by(d, [(2, 4), (2, 6), (3, 6), (4, 8), (5, 10)],
                      [(6, 10), (4, 10), (6, 15), (8, 12), (4, 14), (10, 25), (6, 9)],
                      [(6, 15), (8, 20), (12, 18), (9, 15), (8, 14), (12, 21)]))
    per = random.randint(2, 15) * 5
    g = per * p1
    while (g * p2) % p1:
        per += 5
        g = per * p1
    return _int("A recipe for %d people uses %d g of rice. How much rice is needed for %d people, in grams?" % (p1, g, p2),
                g * p2 // p1, ["One person: %d ÷ %d = %s g." % (g, p1, _ds(Decimal(g) / p1)), "%d people: %d g." % (p2, g * p2 // p1)], "g")


@_more("Y8.4.f", 8)
def _(d):
    pts = [(str(m), m * 8 // 5) for m in range(0, 51, 10)]
    if d == 2 and random.random() < 0.5:              # stretch: read between the gridlines
        m = pick([15, 25, 35, 45])
        return _lg("The conversion graph changes miles into kilometres. How many kilometres are %d miles?" % m, pts, m * 8 // 5,
                   ["%d miles is halfway between %d and %d miles." % (m, m - 5, m + 5),
                    "Halfway between %d km and %d km: %d km." % ((m - 5) * 8 // 5, (m + 5) * 8 // 5, m * 8 // 5)], "km", "Miles")
    if d == 0 or random.random() < 0.5:
        m = pick([10, 20, 30, 40, 50])
        return _lg("The conversion graph changes miles into kilometres. How many kilometres are %d miles?" % m, pts, m * 8 // 5,
                   ["Go up from %d miles to the line and across: %d km." % (m, m * 8 // 5)], "km", "Miles")
    m = pick([20, 30, 40, 50])
    return _lg("The conversion graph changes miles into kilometres. Use it to find how many kilometres are %d miles."
               % (m * 2), pts, m * 16 // 5,
               ["%d miles = %d km from the graph." % (m, m * 8 // 5), "%d miles is double: %d km." % (m * 2, m * 16 // 5)], "km", "Miles")


@_more("Y8.4.f", 8)
def _(d):
    t, s1 = pick(_by(d, [(2, 60), (4, 30), (3, 40), (6, 20), (2, 30)],
                     [(3, 40), (2, 60), (4, 30), (3, 60), (6, 20), (2, 90), (5, 36)],
                     [(5, 36), (3, 48), (4, 45), (6, 35), (7, 24)]))
    dist = t * s1
    s2 = pick([x for x in (range(20, 121, 10) if d < 2 else range(12, 121))
               if dist % x == 0 and x != s1 and dist // x >= 2])
    return _int("A journey takes %d hours at %d km/h. How many hours would it take at %d km/h?" % (t, s1, s2), dist // s2,
                ["Speed and time are in inverse proportion: the distance is %d × %d = %d km." % (t, s1, dist),
                 "%d ÷ %d = %s." % (dist, s2, _pl(dist // s2, "hour"))], "hours")


@_more("Y8.4.f", 8)
def _(d):
    while True:
        m1 = Decimal(random.randint(*_by(d, (2, 6), (3, 12), (3, 19)))) / _by(d, 1, 2, 4)
        p = Decimal(random.randint(2, 9))
        m2 = Decimal(random.randint(*_by(d, (2, 12), (2, 12), (3, 25)))) / _by(d, 1, 1, 2)
        if m1 != m2:
            break
    return _num("%s m of fabric costs %s. How much do %s m cost, in pounds?" % (_ds(m1), _gbp(m1 * p), _ds(m2)), p * m2,
                ["1 m costs %s ÷ %s = %s." % (_ds(m1 * p), _ds(m1), _gbp(p)), "%s × %s = %s." % (_ds(m2), _ds(p), _gbp(p * m2))], "£")


@_more("Y8.4.g", 9)
def _(d):
    k = pick(_by(d, ["2", "3", "5", "0.5", "1.5"], ["2.5", "1.5", "0.5", "4.5", "1.2", "0.4"],
                 ["1.25", "0.75", "2.4", "3.5", "0.6", "1.8"]))
    xs = sorted(random.sample(range(2, _by(d, 11, 13, 21)), 4))
    i = random.randrange(4)
    rows = [[str(x), _ds(Decimal(k) * x)] for x in xs]
    return _dt("y is directly proportional to x, with y = %sx. What is the missing value of y?" % k, ["x", "y"], rows,
               _ds(Decimal(k) * xs[i]), ["y = %s × %d = %s." % (k, xs[i], _ds(Decimal(k) * xs[i]))], missing=(i, 1), atype="num")


@_more("Y8.4.g", 9)
def _(d):
    k = _by(d, Decimal(random.randint(2, 9)), Decimal(random.randint(12, 60)) / 10, Decimal(random.randint(105, 999)) / 100)
    m = random.randint(2, _by(d, 5, 6, 9))
    return _num("The cost of cheese is directly proportional to its mass. %d kg costs %s. What is the constant of "
                "proportionality (the price per kg), in pounds?" % (m, _gbp(k * m)), k,
                ["k = cost ÷ mass = %s ÷ %d = %s." % (_ds(k * m), m, _ds(k))], "£")


@_more("Y8.4.g", 9)
def _(d):
    k = random.randint(_by(d, 1, 1, 2), _by(d, 2, 3, 3))
    x = random.randint(2, _by(d, 4, 5, 7))
    return _cg("The graph shows y = kx, a direct proportion. The line passes through (%d, %d). What is k?" % (x, k * x),
               {"xmin": 0, "xmax": 8, "ymin": 0, "ymax": 8 * k if k < 3 else 24,
                "lines": [{"p1": [0, 0], "p2": [8, 8 * k]}], "points": [[x, k * x, "P"]]}, k,
               ["k = y ÷ x = %d ÷ %d = %d." % (k * x, x, k)], placeholder="k")


@_more("Y8.4.g", 9)
def _(d):
    if d == 2:                                        # stretch: less familiar forms of the equation
        m, c = random.randint(2, 9), random.randint(1, 9)
        eq, yes, why = pick([("y = x/%d" % m, True, "y = (1/%d)x, so k = 1/%d and the line passes through the origin." % (m, m)),
                             ("y − %dx = 0" % m, True, "Rearranged, y = %dx: a line through the origin." % m),
                             ("y = %d + %dx" % (c, m), False, "When x = 0, y = %d, not 0, so no." % c),
                             ("y = %d(x + %d)" % (m, c), False, "y = %dx + %d: when x = 0, y = %d, so no." % (m, m * c, m * c))])
        return _yn("Does %s show y directly proportional to x?" % eq, yes,
                   ["Direct proportion means y = kx: the graph is a straight line through the origin.", why])
    m, c = random.randint(2, _by(d, 5, 9, 9)), pick([0, 0, random.randint(1, 9)])
    eq = "y = %dx" % m + (" + %d" % c if c else "")
    return _yn("Does %s show y directly proportional to x?" % eq, c == 0,
               ["Direct proportion means y = kx: the graph is a straight line through the origin.",
                "%s" % ("There is no constant added, so yes." if c == 0 else "When x = 0, y = %d, not 0, so no." % c)])


@_more("Y8.4.g", 9)
def _(d):
    k = random.randint(*_by(d, (2, 5), (2, 9), (6, 15)))
    x1, x2 = random.sample(range(2, _by(d, 11, 15, 25)), 2)
    return _int("y is directly proportional to x. When x = %d, y = %d. What is x when y = %d?" % (x1, k * x1, k * x2), x2,
                ["k = %d ÷ %d = %d." % (k * x1, x1, k), "x = %d ÷ %d = %d." % (k * x2, k, x2)])


@_more("Y8.4.g", 9)
def _(d):
    m = random.randint(2, 5)
    if d == 2:                                        # stretch: x shrinks
        k, a = random.randint(2, 9), random.randint(2, 6)
        return _int("y is directly proportional to x. When x = %d, y = %d. What is y when x is divided by %d?"
                    % (a * m, k * a * m, m), k * a,
                    ["Dividing x by %d divides y by %d." % (m, m), "%d ÷ %d = %d." % (k * a * m, m, k * a)])
    if d == 0 or random.random() < 0.5:
        return _int("y is directly proportional to x. If x is multiplied by %d, what is y multiplied by?" % m, m,
                    ["y = kx, so multiplying x by %d multiplies y by %d too." % (m, m)])
    k, a = random.randint(2, 9), random.randint(2, 6)
    return _int("y is directly proportional to x. When x = %d, y = %d. What is y when x is %d times as big?" % (a, k * a, m),
                k * a * m, ["Multiplying x by %d multiplies y by %d." % (m, m), "%d × %d = %d." % (k * a, m, k * a * m)])


@_more("Y8.4.h", 8)
def _(d):
    k = random.randint(*_by(d, (2, 5), (2, 9), (11, 25)))
    xs = sorted(random.sample(range(_by(d, 1, 1, 3), _by(d, 6, 11, 20)), 4))
    return _dt("This table shows a proportional relationship. Write its equation (like y=4x).", ["x", "y"],
               [[str(x), str(k * x)] for x in xs], "y=%dx" % k,
               ["Every y is %d times x: %d ÷ %d = %d." % (k, k * xs[0], xs[0], k), "So y = %dx." % k],
               atype="str", placeholder="e.g. y=4x")


@_more("Y8.4.h", 8)
def _(d):
    ks = random.sample(range(2, _by(d, 8, 13, 13)), 3)
    least = random.random() < 0.5
    # stretch: some equations are written as ay = bx, so k = b ÷ a must be found first
    eqs = ["y = %dx" % k if d < 2 or i == 0 else "%dy = %dx" % (a, a * k)
           for i, (k, a) in enumerate(zip(ks, [random.randint(2, 4) for _ in ks]))]
    ans = min(ks) if least else max(ks)
    return _int("Three proportional graphs are %s. Which is the %s? Type its value of k." % (", ".join(eqs), "LEAST steep" if least else "STEEPEST"),
                ans, ["Write each as y = kx: %s." % ", ".join("y = %dx" % k for k in ks),
                      "The bigger k is, the steeper the line.", "The %s has k = %d." % ("least steep" if least else "steepest", ans)])


@_more("Y8.4.h", 8)
def _(d):
    k = random.randint(_by(d, 1, 1, 2), _by(d, 2, 4, 4))
    xmax = 10 if k < 3 else 6
    x = random.randint(2, xmax - 1)
    if d == 2:                                        # stretch: read the graph backwards
        return _cg("The graph shows the proportional relationship y = %dx. Use the line to find x when y = %d." % (k, k * x),
                   {"xmin": 0, "xmax": xmax, "ymin": 0, "ymax": k * xmax, "lines": [{"p1": [0, 0], "p2": [xmax, k * xmax]}]}, x,
                   ["Go across from y = %d to the line, then down: x = %d." % (k * x, x)], placeholder="x")
    return _cg("The graph shows the proportional relationship y = %dx. Use the line to find y when x = %d." % (k, x) if k > 1 else
               "The graph shows the proportional relationship y = x. Use the line to find y when x = %d." % x,
               {"xmin": 0, "xmax": xmax, "ymin": 0, "ymax": k * xmax, "lines": [{"p1": [0, 0], "p2": [xmax, k * xmax]}]}, k * x,
               ["Go up from x = %d to the line, then across: y = %d." % (x, k * x)], placeholder="y")


@_more("Y8.4.h", 8)
def _(d):
    rate = random.randint(*_by(d, (5, 10), (7, 15), (11, 25)))
    h1, h2 = random.sample(range(2, _by(d, 6, 10, 16)), 2)
    return _int("%s's pay is proportional to the hours worked. The graph of pay against hours passes through (0, 0) and "
                "(%d, %d), with pay in pounds. How much is %s paid for %d hours?" % (_who(), h1, rate * h1, "this worker", h2),
                rate * h2, ["Pay per hour = %d ÷ %d = £%d." % (rate * h1, h1, rate), "%d × %d = £%d." % (h2, rate, rate * h2)], "£")


@_more("Y8.4.h", 8)
def _(d):
    k = random.randint(*_by(d, (2, 5), (2, 9), (6, 12)))
    x = _by(d, random.randint(2, 6), random.randint(2, 12), pick([random.randint(-12, -2), random.randint(6, 20)]))
    y = k * x if random.random() < 0.5 else k * x + pick([-2, -1, 1, 2, k])
    return _yn("Does the point (%d, %d) lie on the line y = %dx?" % (x, y, k), y == k * x,
               ["When x = %d, y = %d × %d = %d." % (x, k, x, k * x), "%s" % ("So yes." if y == k * x else "%d ≠ %d, so no." % (y, k * x))])


@_more("Y8.4.i", 6)
def _(d):
    start, drop = random.randint(_by(d, 15, 15, 22), 30), random.randint(*_by(d, (1, 3), (2, 5), (3, 5)))
    pts = [("%d:00" % (h + 1), start - drop * h) for h in range(5)]
    return _lg("A room cools at a steady rate after the heating goes off. By how many degrees does the temperature fall each hour?",
               pts, drop, ["From %d°C to %d°C in 4 hours." % (start, start - 4 * drop), "%d ÷ 4 = %d°C per hour." % (4 * drop, drop)],
               "°C", "Time")


@_more("Y8.4.i", 6)
def _(d):
    m, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 10, 20, 30))
    x0 = _by(d, 1, 1, 3)                              # stretch: the table starts further from x = 0
    xs = [x0, x0 + 1, x0 + 2, x0 + 3]
    return _dt("The values in this table change at a constant rate. What would y be when x = 0?", ["x", "y"],
               [[str(x), str(m * x + c)] for x in xs], c,
               ["y goes up by %d each time x goes up by 1." % m,
                "Go back %s from x = %d: %d − %s = %d." % ("one step" if x0 == 1 else "%d steps" % x0, x0, m * x0 + c,
                                                          str(m) if x0 == 1 else "%d × %d" % (x0, m), c)])


@_more("Y8.4.i", 6)
def _(d):
    fee = random.randint(5, 20)
    per = pick(_by(d, ["0.1", "0.2", "0.5"], ["0.05", "0.1", "0.08", "0.15", "0.2"], ["0.07", "0.12", "0.08", "0.15", "0.04"]))
    n = _by(d, random.randint(2, 10) * 10, random.randint(20, 200), random.randint(120, 500))
    tot = fee + Decimal(per) * n
    return _num("A phone plan costs £%d a month plus %s for each text. How much does a month with %d texts cost, in pounds?"
                % (fee, _gbp(per), n), tot, ["%d × %s = %s." % (n, _gbp(per), _gbp(Decimal(per) * n)), "%d + %s = %s." % (fee, _ds(Decimal(per) * n), _gbp(tot))], "£")


@_more("Y8.4.i", 6)
def _(d):
    rate = _by(d, Decimal(random.randint(1, 2)), Decimal(random.randint(1, 4)), pick([Decimal("0.5"), Decimal("1.5"), Decimal("2.5")]))
    hours = _by(d, random.randint(3, 8), random.randint(4, 12), random.randint(3, 8) * 2)   # stretch: even, so h0 is whole
    h0 = rate * hours
    return _int("A candle is %s cm tall and burns down %s cm every hour. After how many hours will it have burnt away completely?"
                % (_ds(h0), _ds(rate)), hours, ["%s ÷ %s = %d hours." % (_ds(h0), _ds(rate), hours)], "hours")


@_more("Y8.4.i", 6)
def _(d):
    m, c = random.randint(2, 9), random.randint(0, 15)
    st = _by(d, 1, 2, pick([3, 5]))
    xs = [0, st, 2 * st, 3 * st]
    return _dt("The values in this table change at a constant rate. By how much does y increase for every increase of 1 in x?",
               ["x", "y"], [[str(x), str(m * x + c)] for x in xs], m,
               ["x goes up in steps of %d and y goes up by %d each step." % (st, st * m), "%d ÷ %d = %d per 1." % (st * m, st, m)])


@_more("Y8.4.i", 6)
def _(d):
    win_a = random.random() < 0.5                     # either plan can win
    gap = _by(d, 20, 12, 8)                           # the totals are within gap% of each other
    while True:
        fa, ra = _by(d, random.randint(1, 4) * 5, random.randint(2, 20), random.randint(2, 20)), random.randint(5, 15)
        fb, rb = random.randint(10, _by(d, 40, 40, 80)), random.randint(2, ra - 1) if ra > 3 else 1
        h = random.randint(*_by(d, (2, 5), (2, 10), (6, 20)))
        ca, cb = fa + ra * h, fb + rb * h
        if ca != cb and fa < fb and (ca < cb) == win_a and abs(ca - cb) * 100 <= gap * min(ca, cb):
            break
    return _wq("Plan A charges £%d plus £%d per hour. Plan B charges £%d plus £%d per hour. Which is cheaper for %d hours? "
               "Type A or B." % (fa, ra, fb, rb, h), "A" if ca < cb else "B",
               ["A: %d + %d × %d = £%d." % (fa, ra, h, ca), "B: %d + %d × %d = £%d." % (fb, rb, h, cb),
                "Plan %s is cheaper." % ("A" if ca < cb else "B")], "A or B")


@_more("Y8.4.i", 6)
def _(d):
    m = random.randint(1, _by(d, 3, 4, 4))
    c = random.randint(0, _by(d, 0, 3, 3))
    while True:
        x1, x2 = random.sample(range(0, 6), 2)
        x1, x2 = min(x1, x2), max(x1, x2)
        if d < 2 or x2 - x1 >= 2:                     # stretch: never a single step in x
            break
    return _cg("The straight line passes through A(%d, %d) and B(%d, %d). By how much does y increase for each increase of 1 in x?"
               % (x1, m * x1 + c, x2, m * x2 + c),
               {"xmin": 0, "xmax": 6, "ymin": 0, "ymax": 6 * m + c + 1, "lines": [{"p1": [0, c], "p2": [6, 6 * m + c]}],
                "points": [[x1, m * x1 + c, "A"], [x2, m * x2 + c, "B"]]}, m,
               ["Change in y = %d − %d = %d; change in x = %d − %d = %d." % (m * x2 + c, m * x1 + c, m * (x2 - x1), x2, x1, x2 - x1),
                "%d ÷ %d = %d." % (m * (x2 - x1), x2 - x1, m)], placeholder="rate")


@_more("Y8.4.j", 10)
def _(d):
    s = pick(_by(d, [10000, 100000, 50000], [25000, 50000, 10000, 20000, 100000], [25000, 40000, 125000, 250000]))
    cm = _by(d, Decimal(random.randint(2, 10)), Decimal(random.randint(2, 15)), Decimal(random.randint(15, 150)) / 10)
    km = cm * s / 100000
    return _num("A map has a scale of 1 : %s. Two villages are %s cm apart on the map. How far apart are they in real life, in km?"
                % (_c(s), _ds(cm)), km, ["%s × %s = %s cm." % (_ds(cm), _c(s), _c(int(cm * s))),
                                         "%s cm = %s km (÷ 100,000)." % (_c(int(cm * s)), _ds(km))], "km")


@_more("Y8.4.j", 10)
def _(d):
    s = pick(_by(d, [10000, 20000, 50000], [25000, 50000, 10000, 20000], [25000, 40000, 250000]))
    km = pick(_by(d, [1, 2, 5], [1, 2, 3, 4, 5, 6, 8, 10],
                  [Decimal("1.5"), Decimal("2.5"), Decimal("3.5"), Decimal("4.2"), Decimal("7.5")]))
    cm = Decimal(km * 100000) / s
    return _num("A map has a scale of 1 : %s. A real road is %s km long. How long is it on the map, in cm?" % (_c(s), _ds(km)), cm,
                ["%s km = %s cm." % (_ds(km), _c(int(km * 100000))), "%s ÷ %s = %s cm." % (_c(int(km * 100000)), _c(s), _ds(cm))], "cm")


@_more("Y8.4.j", 10)
def _(d):
    cm = random.randint(2, _by(d, 5, 8, 12))
    s = pick(_by(d, [100, 1000], [500, 1000, 2000, 5000, 10000, 20000], [2500, 25000, 40000, 50000]))
    m = cm * s // 100
    return _int("On a map, %d cm stands for %s m in real life. The scale is 1 : n. What is n?" % (cm, _c(m)), s,
                ["%s m = %s cm." % (_c(m), _c(m * 100)), "%s ÷ %d = %s, so the scale is 1 : %s." % (_c(m * 100), cm, _c(s), _c(s))])


@_more("Y8.4.j", 10)
def _(d):
    k = pick(_by(d, [2], [2, 3, 4], [3, 4, 5]))
    a, b = random.randint(2, _by(d, 4, 5, 9)), random.randint(2, _by(d, 3, 4, 7))
    sc = "1 cm to %d m" % k if d < 2 else "1 : %d" % (k * 100)    # stretch: a ratio scale to unpick first
    return _int("A plan uses the scale %s. A room on the plan is %d cm by %d cm. What is the real area of the room, in m²?"
                % (sc, a, b), a * k * b * k, ([] if d < 2 else ["1 : %d means 1 cm stands for %d cm = %d m." % (k * 100, k * 100, k)]) +
                ["Real size: %d m by %d m." % (a * k, b * k), "%d × %d = %d m²." % (a * k, b * k, a * k * b * k)], "m²")


@_more("Y8.4.j", 10)
def _(d):
    s, m = pick(_by(d, [(10, "4"), (20, "4"), (50, "5"), (25, "4.5"), (10, "3.5")],
                    [(24, "4.32"), (18, "4.5"), (32, "4.8"), (43, "4.3"), (50, "4.25"), (76, "3.8"), (25, "3.75"), (20, "4.6")],
                    [(64, "4.48"), (72, "3.6"), (36, "4.5"), (48, "4.2"), (18, "4.05"), (43, "4.3")]))
    m = Decimal(m)
    cm = m * 100 / s
    return _num("A model car is made to a scale of 1 : %d. The real car is %s m long. How long is the model, in cm?" % (s, _ds(m)), cm,
                ["%s m = %s cm." % (_ds(m), _ds(m * 100)), "%s ÷ %d = %s cm." % (_ds(m * 100), s, _ds(cm))], "cm")


@_more("Y8.5.a", 9)
def _(d):
    p = pick(_by(d, ["50", "25", "75", "10", "5", "60", "120", "40"],
                 ["125", "150", "110", "250", "0.5", "2.5", "12.5", "300", "175"],
                 ["0.25", "0.75", "137.5", "112.5", "0.05", "350", "17.5", "2.25"]))
    v = Decimal(p) / 100
    return _num("Write %s%% as a decimal." % p, v, ["Divide by 100: %s ÷ 100 = %s." % (p, _ds(v))])


@_more("Y8.5.a", 9)
def _(d):
    a, b = pick(_by(d, [(1, 3), (2, 3), (1, 6), (5, 6), (1, 9)],
                    [(1, 3), (2, 3), (1, 6), (5, 6), (1, 7), (1, 9), (2, 7), (4, 9)],
                    [(3, 7), (5, 7), (7, 9), (5, 11), (7, 12), (11, 15), (4, 13), (8, 11)]))
    v = _round(Decimal(100 * a) / b, 1)
    return _num("Write %d/%d as a percentage, correct to 1 decimal place." % (a, b), v,
                ["%d ÷ %d × 100 = %s…" % (a, b, str(Decimal(100 * a) / b)[:7]), "To 1 d.p.: %s%%." % _ds(v)], "%", tol=0.05)


@_more("Y8.5.a", 9)
def _(d):
    rows = _by(d, [(Fraction(1, 2), "0.5", "50%"), (Fraction(1, 4), "0.25", "25%"), (Fraction(3, 4), "0.75", "75%"),
                   (Fraction(1, 10), "0.1", "10%"), (Fraction(1, 5), "0.2", "20%"), (Fraction(3, 10), "0.3", "30%"),
                   (Fraction(9, 10), "0.9", "90%")],
               [(Fraction(1, 4), "0.25", "25%"), (Fraction(1, 5), "0.2", "20%"), (Fraction(3, 8), "0.375", "37.5%"),
                (Fraction(7, 20), "0.35", "35%"), (Fraction(3, 4), "0.75", "75%"), (Fraction(1, 8), "0.125", "12.5%"),
                (Fraction(9, 10), "0.9", "90%"), (Fraction(2, 25), "0.08", "8%"), (Fraction(3, 5), "0.6", "60%")],
               [(Fraction(3, 8), "0.375", "37.5%"), (Fraction(7, 40), "0.175", "17.5%"), (Fraction(5, 16), "0.3125", "31.25%"),
                (Fraction(3, 40), "0.075", "7.5%"), (Fraction(5, 8), "0.625", "62.5%"), (Fraction(1, 80), "0.0125", "1.25%"),
                (Fraction(11, 20), "0.55", "55%"), (Fraction(9, 200), "0.045", "4.5%")])
    pickd = random.sample(rows, 4)
    i = random.randrange(4)
    col = random.randint(0, 2)
    table = [[_simp_str(f), dd, pc] for f, dd, pc in pickd]
    ans = table[i][col]
    atype = ("frac", "num", "num")[col]
    return _dt("Each row shows the same amount as a fraction, a decimal and a percentage. What goes in the empty cell?%s"
               % (" (Give the fraction in its simplest form.)" if col == 0 else " (Type the number only.)" if col == 2 else ""),
               ["Fraction", "Decimal", "Percentage"], table, ans.rstrip("%"),
               ["%s = %s = %s." % tuple(table[i])], missing=(i, col), atype=atype)


@_more("Y8.5.a", 9)
def _(d):
    cats = random.sample(["Football", "Swimming", "Tennis", "Running", "Netball", "Cycling"], 4)
    total = pick(_by(d, [20, 50], [20, 25, 40, 50], [16, 32, 40, 80]))     # hard: answers such as 12.5%
    while True:
        cuts = sorted(random.sample(range(1, total), 3))
        vals = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2]]
        if min(vals) >= 2:
            break
    i = random.randrange(4)
    pct = Decimal(100 * vals[i]) / total
    return {"prompt": "The pie chart shows the favourite sport of %d pupils. What percentage chose %s?" % (total, cats[i]),
            "component": "pie_chart", "spec": {"slices": [[c, v] for c, v in zip(cats, vals)], "highlight": i},
            "answer": _ds(pct), "answer_type": "num",
            "solution": ["%s is %d out of %d pupils." % (cats[i], vals[i], total), "%d/%d × 100 = %s%%." % (vals[i], total, _ds(pct))]}


@_more("Y8.5.a", 9)
def _(d):
    a, b = pick(_by(d, [(1, 4), (3, 4), (1, 5), (2, 5), (3, 10), (7, 10), (9, 20), (3, 25)],
                    [(7, 40), (3, 40), (1, 8), (5, 8), (9, 40), (13, 40), (7, 8), (1, 16), (3, 16)],
                    [(7, 32), (5, 16), (9, 80), (11, 40), (13, 80), (11, 16), (3, 32), (17, 80)]))
    v = Decimal(100 * a) / b
    return _num("Write %d/%d as a percentage." % (a, b), v, ["%d ÷ %d = %s." % (a, b, _ds(Decimal(a) / b)), "× 100 = %s%%." % _ds(v)], "%")


@_more("Y8.5.a", 9)
def _(d):
    x = pick(_by(d, ["0.25", "0.6", "0.07", "0.45", "0.3", "0.85", "0.09", "0.5"],
                 ["0.075", "0.005", "1.2", "0.125", "2.05", "0.035", "0.0125", "1.45"],
                 ["0.0075", "0.0005", "1.375", "2.005", "0.1625", "0.00125", "3.025", "0.0875"]))
    v = Decimal(x) * 100
    return _num("Write %s as a percentage." % x, v, ["Multiply by 100: %s × 100 = %s%%." % (x, _ds(v))], "%")


@_more("Y8.5.a", 9)
def _(d):
    p, f = pick(_by(d, [("25", "1/4"), ("20", "1/5"), ("75", "3/4"), ("40", "2/5"), ("10", "1/10"), ("60", "3/5"), ("5", "1/20"), ("30", "3/10")],
                    [("12.5", "1/8"), ("35", "7/20"), ("62.5", "5/8"), ("4", "1/25"), ("45", "9/20"), ("85", "17/20"), ("37.5", "3/8"), ("2", "1/50")],
                    [("17.5", "7/40"), ("6.25", "1/16"), ("87.5", "7/8"), ("2.5", "1/40"), ("0.5", "1/200"), ("32.5", "13/40"), ("1.25", "1/80"), ("22.5", "9/40")]))
    return _wq("Write %s%% as a fraction in its simplest form (like 3/8)." % p, f,
               ["%s%% = %s/100." % (p, p), "Simplify: %s." % f], "e.g. 3/8")


@_more("Y8.5.c", 7)
def _(d):
    out = pick(_by(d, [10, 20, 25, 50], [20, 25, 40, 50, 80], [16, 32, 40, 80, 125, 200]))
    sc = random.randint(out // 3, out)
    v = Decimal(100 * sc) / out
    return _num("%s scores %d out of %d in a test. What percentage is that?" % (_who(), sc, out), v,
                ["%d/%d × 100 = %s%%." % (sc, out, _ds(v))], "%")


@_more("Y8.5.c", 7)
def _(d):
    pounds = pick(_by(d, [1, 2, 5, 10], [2, 4, 5, 8, 10, 20], [8, 16, 25, 40]))
    q = _by(d, 1, 1, 10)                                       # stretch: answers may have 1 d.p.
    p = pick([x for x in range(5, pounds * 100, 5) if (x * q) % pounds == 0])
    v = Decimal(p * 100) / (pounds * 100)
    return _num("What percentage of £%d is %dp?" % (pounds, p), v,
                ["Use the same units: £%d = %dp." % (pounds, pounds * 100), "%d/%d × 100 = %s%%." % (p, pounds * 100, _ds(v))], "%")


@_more("Y8.5.c", 7)
def _(d):
    cats = random.sample(["Cats", "Dogs", "Fish", "Rabbits", "Birds"], 4)
    total = pick(_by(d, [20, 50], [20, 25, 40, 50], [16, 40, 80]))
    while True:
        cuts = sorted(random.sample(range(1, total), 3))
        vals = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2]]
        if min(vals) >= 1:
            break
    i = random.randrange(4)
    pct = Decimal(100 * vals[i]) / total
    return _bar("The bar chart shows the pets owned by %d pupils (each owns one pet). What percentage of them own %s?"
                % (total, cats[i].lower()), cats, vals, _ds(pct),
                ["%d out of %d pupils." % (vals[i], total), "%d/%d × 100 = %s%%." % (vals[i], total, _ds(pct))], "num")


@_more("Y8.5.c", 7)
def _(d):
    while True:
        o1, o2 = random.sample(_by(d, [10, 20, 25, 50], [20, 25, 40, 50, 60, 80], [24, 30, 35, 45, 60, 75]), 2)
        s1, s2 = random.randint(o1 // 2, o1), random.randint(o2 // 2, o2)
        if s1 * o2 != s2 * o1:
            break
    p1, p2 = Fraction(100 * s1, o1), Fraction(100 * s2, o2)
    return _wq("%s scored %d out of %d in test A and %d out of %d in test B. In which test did they do better? Type A or B."
               % (_who(), s1, o1, s2, o2), "A" if p1 > p2 else "B",
               ["A: %s%%. B: %s%%." % (_ds(_round(Decimal(100 * s1) / o1, 1)), _ds(_round(Decimal(100 * s2) / o2, 1))),
                "Test %s is the higher percentage." % ("A" if p1 > p2 else "B")], "A or B")


@_more("Y8.5.c", 7)
def _(d):
    if d == 2:                                                 # stretch: of 2 hours, so 120 minutes
        m = pick([18, 42, 54, 66, 78, 90, 102, 108])
        v = Decimal(100 * m) / 120
        return _num("What percentage of 2 hours is %d minutes?" % m, v,
                    ["2 hours = 120 minutes.", "%d/120 × 100 = %s%%." % (m, _ds(v))], "%")
    m = pick(_by(d, [6, 12, 15, 30, 45], [6, 9, 12, 15, 18, 24, 30, 36, 45, 48, 54], None))
    v = Decimal(100 * m) / 60
    return _num("What percentage of an hour is %d minutes?" % m, v, ["%d/60 × 100 = %s%%." % (m, _ds(v))], "%")


@_more("Y8.5.c", 7)
def _(d):
    a, b = pick(_by(d, [(2, 3), (5, 6), (4, 9), (7, 9), (5, 12), (7, 12)],
                    [(7, 12), (5, 9), (11, 15), (2, 7), (13, 30), (8, 21), (4, 11)],
                    [(17, 23), (19, 27), (13, 17), (23, 31), (29, 37), (31, 42), (38, 47)]))
    v = _round(Decimal(100 * a) / b, 1)
    return _num("In a club, %d of the %d members are under 16. What percentage is that, correct to 1 decimal place?" % (a, b), v,
                ["%d ÷ %d × 100 = %s…" % (a, b, str(Decimal(100 * a) / b)[:7]), "To 1 d.p.: %s%%." % _ds(v)], "%", tol=0.05)


@_more("Y8.5.c", 7)
def _(d):
    if d == 0:                                                 # easy: girls' total is 10, 20, 25 or 50
        g, b = pick([10, 20, 25, 50]), random.randint(8, 20) * 2
        gy = random.randint(1, g - 1)
    else:
        while True:
            g, b = random.randint(8, 20) * 2, random.randint(8, 20) * 2
            gy = random.randint(2, g - 2)
            if (100 * gy) % g == 0:
                break
    by = random.randint(2, b - 2)
    while d == 2 and (100 * (gy + by)) % (g + b):              # stretch: a percentage of everyone, from two rows
        b = random.randint(8, 20) * 2
        by = random.randint(2, b - 2)
    rows = [["Girls", str(gy), str(g - gy), str(g)], ["Boys", str(by), str(b - by), str(b)]]
    if d == 2:
        pct = 100 * (gy + by) // (g + b)
        return _dt("The two-way table shows who walks to school. What percentage of ALL the pupils walk?",
                   ["", "Walk", "Do not walk", "Total"], rows, pct,
                   ["%d + %d = %d walk, out of %d + %d = %d pupils." % (gy, by, gy + by, g, b, g + b),
                    "%d/%d × 100 = %d%%." % (gy + by, g + b, pct)])
    return _dt("The two-way table shows who walks to school. What percentage of the GIRLS walk?", ["", "Walk", "Do not walk", "Total"],
               rows, 100 * gy // g, ["%d of the %d girls walk." % (gy, g), "%d/%d × 100 = %d%%." % (gy, g, 100 * gy // g)])


@_more("Y8.5.d", 7)
def _(d):
    p = _by(d, Decimal(pick([10, 20, 25, 30, 50])), Decimal(random.randint(1, 60)),
            Decimal(pick(["2.5", "12.5", "7.5", "0.5", "17.5", "1.5", "4.5", "33.5"])))   # stretch: decimal percentages
    up = random.random() < 0.5
    v = (100 + p) / 100 if up else (100 - p) / 100
    return _num("What decimal do you multiply by to %s an amount by %s%%?" % ("increase" if up else "decrease", _ds(p)), v,
                ["%d%% %s %s%% = %s%%." % (100, "+" if up else "−", _ds(p), _ds(100 + p if up else 100 - p)), "As a decimal: %s." % _ds(v)])


@_more("Y8.5.d", 7)
def _(d):
    p = pick(_by(d, [10, 20, 25, 50], [3, 5, 12, 15, 35, 4, 8, 17], [3, 7, 13, 17, 23, 37, 115, 140]))
    up = random.random() < 0.5 or p > 100
    n = random.randint(*_by(d, (1, 20), (4, 60), (10, 250))) * 20
    mult = Decimal(100 + p if up else 100 - p) / 100
    return _num("Use a multiplier to %s %s by %d%%." % ("increase" if up else "decrease", _c(n), p), mult * n,
                ["The multiplier is %s." % _ds(mult), "%s × %s = %s." % (_c(n), _ds(mult), _ds(mult * n))])


@_more("Y8.5.d", 7)
def _(d):
    p = pick(_by(d, [10, 50, 20], [10, 20, 25, 30, 40], [15, 35, 45, 65, 85]))
    prices = random.sample(range(2, 30), 4)
    prices = [x * 20 for x in prices]
    i = random.randrange(4)
    rows = [[_gbp(x), _gbp(Decimal(x) * (100 - p) / 100)] for x in prices]
    return _dt("In a sale every price is cut by %d%%. What goes in the empty cell, in pounds?" % p, ["Old price", "Sale price"], rows,
               _ds(Decimal(prices[i]) * (100 - p) / 100),
               ["Multiply by %s." % _ds(Decimal(100 - p) / 100), "%d × %s = %s." % (prices[i], _ds(Decimal(100 - p) / 100), _gbp(Decimal(prices[i]) * (100 - p) / 100))],
               missing=(i, 1), atype="num")


@_more("Y8.5.d", 7)
def _(d):
    p = pick(_by(d, [10, 20, 50, 25], [10, 20, 5, 15], [3, 7, 12, 35, 4]))
    lo, hi = _by(d, (2, 60), (200, 6000), (200, 9000))
    sc = _by(d, 1, 100, 100)                                   # easy: whole pounds
    x = Decimal(random.randint(lo, hi)) / sc
    while ((x * p) % (100 if d == 0 else 1)) != 0:            # easy: the new price is whole pounds too
        x = Decimal(random.randint(lo, hi)) / sc
    v = x * (100 + p) / 100
    return _num("A train ticket costs %s. The price goes up by %d%%. What is the new price, in pounds?" % (_gbp(x), p), v,
                ["%d%% of %s = %s." % (p, _gbp(x), _gbp(x * p / 100)), "%s + %s = %s." % (_gbp(x), _gbp(x * p / 100), _gbp(v))], "£")


@_more("Y8.5.d", 7)
def _(d):
    p = pick(_by(d, [10, 50], [10, 20, 50, 25], [15, 30, 35, 40, 5]))
    n = pick(_by(d, [100, 200, 400], [40, 80, 200, 400, 120], [60, 160, 240, 500, 360]))
    v = Decimal(n) * (100 + p) / 100 * (100 - p) / 100
    return _num("%s increases %d by %d%% and then decreases the answer by %d%%, and says the result is %d again. What is the "
                "correct result?" % (_who(), n, p, p, n), v,
                ["Up %d%%: %s." % (p, _ds(Decimal(n) * (100 + p) / 100)),
                 "Down %d%% of the NEW amount: %s." % (p, _ds(v)), "It is not the same because the second %d%% is of a bigger number." % p])


@_more("Y8.5.f", 7)
def _(d):
    base = pick(_by(d, [20, 40, 50, 200], [20, 40, 50, 60, 80, 120, 200], [120, 160, 240, 360, 440, 640]))
    p = pick([x for x in _by(d, (10, 20, 25, 50, 75), (5, 10, 15, 20, 25, 30, 40, 45, 60, 75),
                             (5, 15, 35, 45, 55, 65, 85, 95)) if (base * x) % 100 == 0])
    part = base * p // 100
    return _int("What percentage of %d is %d?" % (base, part) if random.random() < 0.5 else
                "x%% of %d is %d. What is x?" % (base, part), p,
                ["%d ÷ %d × 100 = %d." % (part, base, p)], "%")


@_more("Y8.5.f", 7)
def _(d):
    a, b, c = pick(_by(d, [(10, 40, 20), (50, 60, 10), (25, 80, 10), (20, 50, 5), (10, 60, 2)],
                       [(15, 40, 6), (20, 30, 10), (25, 60, 5), (10, 90, 3), (30, 50, 6), (12, 50, 4), (40, 45, 9)],
                       [(35, 60, 7), (45, 80, 12), (18, 50, 15), (64, 25, 8), (35, 40, 28), (24, 75, 36)]))
    val = a * b // 100
    ans = val * 100 // c
    return _int("%d%% of %d = %d%% of what number?" % (a, b, c), ans,
                ["%d%% of %d = %d." % (a, b, val), "%d%% of the number is %d, so 1%% is %s and 100%% is %d." % (c, val, _ds(Decimal(val) / c), ans)])


@_more("Y8.5.f", 7)
def _(d):
    while True:
        v1 = random.randint(10, 40) * 10
        p = pick(_by(d, [10, 20, 50, -10, -50, 25], [10, 20, 25, 30, 40, 50, -10, -20, -25],
                     [15, 35, 5, 45, -15, -35, -5, -45]))
        v2 = v1 * (100 + p) // 100
        if v1 * (100 + p) % 100 == 0:
            break
    pts = [("2021", v1 - pick([20, 30, 40])), ("2022", v1), ("2023", v2)]
    return _lg("The graph shows the number of visitors to a museum (in thousands). What was the percentage %s from 2022 to 2023?"
               % ("increase" if p > 0 else "decrease"), pts, abs(p),
               ["2022: %d, 2023: %d. Change = %d." % (v1, v2, abs(v2 - v1)), "%d ÷ %d × 100 = %d%%." % (abs(v2 - v1), v1, abs(p))],
               "Visitors (1000s)", "Year")


@_more("Y8.5.f", 7)
def _(d):
    xs = _by(d, [10, 20, 30, 40, 50], [10, 20, 25, 30, 40, 50, 60, 75, 80], [12, 15, 24, 25, 35, 60, 64, 75, 80])
    a, b = random.sample(xs, 2)
    v = a * b // 100 if (a * b) % 100 == 0 else None
    while v is None:
        a, b = random.sample(xs, 2)
        v = a * b // 100 if (a * b) % 100 == 0 else None
    return _int("Work out %d%% of %d and %d%% of %d. What do you notice? Type the value they share." % (a, b, b, a), v,
                ["%d%% of %d = %d × %d ÷ 100 = %d." % (a, b, a, b, v), "%d%% of %d = %d × %d ÷ 100 = %d — the same." % (b, a, b, a, v)])


@_more("Y8.5.f", 7)
def _(d):
    lo, hi, sc = _by(d, (2, 20, 1), (4, 40, 2), (8, 80, 4))     # easy whole pounds; stretch to the 25p
    old = Decimal(random.randint(lo, hi)) / sc
    p = pick(_by(d, [10, 50, 25], [10, 20, 25, 40, 50], [15, 35, 5, 30, 45, 60]))
    new = old * (100 - p) / 100
    while new * 100 % 1:
        old = Decimal(random.randint(lo, hi)) / sc
        new = old * (100 - p) / 100
    return _int("The price of a sandwich falls from %s to %s. What is the percentage decrease?" % (_gbp(old), _gbp(new)), p,
                ["Decrease = %s." % _gbp(old - new), "%s ÷ %s × 100 = %d%%." % (_ds(old - new), _ds(old), p)], "%")


@_more("Y8.5.g", 9)
def _(d):
    if d == 0:                                                 # easy: add the VAT (forwards)
        pre = random.randint(2, 30) * 5
        return _int("A price is £%d before VAT. VAT at 20%% is added. What is the price with VAT, in pounds?" % pre, pre * 6 // 5,
                    ["20%% of £%d = £%d." % (pre, pre // 5), "%d + %d = £%d." % (pre, pre // 5, pre * 6 // 5)], "£")
    pre = random.randint(*_by(d, None, (3, 60), (60, 400))) * 5
    return _int("A price of £%d includes VAT at 20%%. What was the price before VAT, in pounds?" % (pre * 6 // 5), pre,
                ["£%d is 120%% of the price before VAT." % (pre * 6 // 5), "%d ÷ 1.2 = £%d." % (pre * 6 // 5, pre)], "£")


@_more("Y8.5.g", 9)
def _(d):
    p = pick(_by(d, [10], [10, 12.5, 15], [12.5, 15, 17.5]))
    bill = Decimal(random.randint(*_by(d, (2, 12), (10, 60), (30, 150))) * _by(d, 10, 2, 2))   # even, so 12.5% is a whole number of pence
    tip = bill * Decimal(str(p)) / 100
    tot = bill + tip
    return _num("A restaurant bill is £%d. A %s%% service charge is added. What is the total, in pounds?" % (bill, p), _round(tot, 2),
                ["%s%% of £%d = %s." % (p, bill, _gbp(_round(tip, 2))), "Total: %s." % _gbp(_round(tot, 2))], "£")


@_more("Y8.5.g", 9)
def _(d):
    if d == 2:                                                 # stretch: three items, the cheapest at half price
        xs = random.sample(range(5, 46), 3)
        xs = [2 * x for x in xs]
        lo, tot = min(xs), sum(xs) - min(xs) // 2
        return _int("A shop has an offer: buy three, get the cheapest one half price. %s buys items costing £%d, £%d and £%d. "
                    "How much do they pay, in pounds?" % ((_who(),) + tuple(xs)), tot,
                    ["The cheapest item (£%d) is half price: £%d." % (lo, lo // 2),
                     "%d + %d + %d − %d = £%d." % (xs[0], xs[1], xs[2], lo // 2, tot)], "£")
    a = random.randint(*_by(d, (2, 10), (4, 30), None)) * 2
    b = random.randint(*_by(d, (2, 10), (4, 30), None)) * 2
    hi, lo = max(a, b), min(a, b)
    if hi == lo:
        hi += 2
    tot = hi + lo // 2
    return _int("A shop has an offer: buy one, get the second (cheaper) one half price. %s buys items costing £%d and £%d. How "
                "much do they pay, in pounds?" % (_who(), hi, lo), tot, ["The cheaper item is half price: £%d." % (lo // 2), "%d + %d = £%d." % (hi, lo // 2, tot)], "£")


@_more("Y8.5.g", 9)
def _(d):
    items = random.sample([("Pens", 3), ("Folder", 5), ("Calculator", 12), ("Ruler", 2), ("Bag", 20), ("Notebook", 4)], 3)
    qty = [random.randint(1, _by(d, 2, 4, 6)) for _ in items]
    p = pick(_by(d, [10, 50], [10, 20, 25], [15, 35, 5, 30]))
    sub = sum(c * q for (n, c), q in zip(items, qty))
    tot = Decimal(sub) * (100 - p) / 100
    rows = [[n, str(q), "£%d" % c, "£%d" % (c * q)] for (n, c), q in zip(items, qty)]
    return _dt("The receipt shows a school order. A %d%% discount is taken off the total. How much is paid, in pounds?" % p,
               ["Item", "Quantity", "Price each", "Cost"], rows, _ds(tot),
               ["Total before discount: £%d." % sub, "%d%% off: %d × %s = %s." % (p, sub, _ds(Decimal(100 - p) / 100), _gbp(tot))],
               atype="num")


@_more("Y8.5.g", 9)
def _(d):
    price = random.randint(2, 15) * 4
    off = pick(_by(d, [10, 20, 50], [25, 30, 40, 20], [30, 32, 34, 35, 36]))   # stretch: close to 33⅓%
    a_cost = 2 * price
    b_cost = Decimal(3 * price) * (100 - off) / 100
    if a_cost == b_cost:
        off = 40
        b_cost = Decimal(3 * price) * (100 - off) / 100
    return _wq("A shirt costs £%d. Shop A: buy 3, pay for 2. Shop B: %d%% off every shirt. Which shop is cheaper for 3 shirts? "
               "Type A or B." % (price, off), "A" if a_cost < b_cost else "B",
               ["A: 2 × %d = £%d." % (price, a_cost), "B: 3 × %d = %d, minus %d%% = %s." % (price, 3 * price, off, _gbp(b_cost)),
                "Shop %s is cheaper." % ("A" if a_cost < b_cost else "B")], "A or B")


@_more("Y8.5.g", 9)
def _(d):
    pre = random.randint(*_by(d, (2, 20), (2, 30), (20, 150))) * 10
    p = pick(_by(d, [10, 50], [10, 20, 50], [15, 35, 45, 5]))
    after = Decimal(pre) * (100 - p) / 100
    tot = after * Decimal("1.2")
    return _num("A bike costs £%d before VAT. It is reduced by %d%%, then VAT at 20%% is added. What is the final price, in pounds?"
                % (pre, p), tot, ["Reduced: %s." % _gbp(after), "Add 20%% VAT: %s × 1.2 = %s." % (_ds(after), _gbp(tot))], "£")


@_more("Y8.5.i", 6)
def _(d):
    p = random.randint(*_by(d, (1, 10), (2, 20), (5, 60))) * 100
    r = pick(_by(d, [5, 10], [2, 3, 4, 5, 6], [3, 4, 6, 7, 8, 9]))
    y = random.randint(*_by(d, (2, 3), (2, 5), (3, 8)))
    i = p * r * y // 100
    if random.random() < 0.5:
        return _int("£%s earns £%d simple interest in %d years. What is the yearly interest rate, as a percentage?" % (_c(p), i, y), r,
                    ["Interest per year: %d ÷ %d = £%d." % (i, y, i // y), "%d ÷ %s × 100 = %d%%." % (i // y, _c(p), r)], "%")
    return _int("£%s is invested at %d%% simple interest. How many years does it take to earn £%d interest?" % (_c(p), r, i), y,
                ["Interest per year: %d%% of %s = £%d." % (r, _c(p), p * r // 100), "%d ÷ %d = %d years." % (i, p * r // 100, y)], "years")


@_more("Y8.5.i", 6)
def _(d):
    r, n = pick(_by(d, [(10, 2), (5, 2), (20, 2), (50, 2)],
                    [(10, 2), (5, 2), (4, 2), (10, 3), (2, 2), (3, 2), (20, 2)],
                    [(3, 3), (4, 3), (15, 2), (6, 2), (12, 2), (5, 3), (2, 4)]))
    m = (Decimal(100 + r) / 100) ** n
    return _num("Money grows by %d%% each year (compound interest). What single number can you multiply by to find its value after "
                "%d years?" % (r, n), m, ["Each year multiply by %s." % _ds(Decimal(100 + r) / 100),
                                         "%s^%d = %s." % (_ds(Decimal(100 + r) / 100), n, _ds(m))])


@_more("Y8.5.i", 6)
def _(d):
    p = pick(_by(d, [1000, 2000, 500], [1000, 2000, 500, 5000], [2000, 4000, 8000]))
    r = pick(_by(d, [10], [10, 20], [5, 15]))
    vals = [Decimal(p)]
    for _ in range(3):
        vals.append(vals[-1] * (100 + r) / 100)
    i = random.randint(1, 3)
    rows = [[str(y), _ds(v)] for y, v in enumerate(vals)]
    return _dt("£%s is invested at %d%% compound interest. The table shows the value at the end of each year. What goes in the "
               "empty cell, in pounds?" % (_c(p), r), ["Year", "Value (£)"], rows, _ds(vals[i]),
               ["Each year multiply by %s." % _ds(Decimal(100 + r) / 100), "%s × %s = %s." % (_ds(vals[i - 1]), _ds(Decimal(100 + r) / 100), _ds(vals[i]))],
               missing=(i, 1), atype="num")


@_more("Y8.5.i", 6)
def _(d):
    p, r, n = pick(_by(d, [(1000, 10, 2), (2000, 50, 2), (1000, 20, 2), (800, 50, 3)],
                       [(1000, 10, 3), (2000, 10, 2), (500, 20, 2), (10000, 10, 3), (8000, 50, 2), (1000, 20, 3)],
                       [(10000, 15, 3), (6400, 25, 3), (8000, 5, 3), (2000, 10, 4), (16000, 25, 4)]))
    v = Decimal(p) * (Decimal(100 - r) / 100) ** n
    return _num("A machine worth £%s loses %d%% of its value every year. What is it worth after %d years, in pounds?" % (_c(p), r, n), v,
                ["Multiply by %s each year." % _ds(Decimal(100 - r) / 100),
                 "%s × %s^%d = %s." % (_c(p), _ds(Decimal(100 - r) / 100), n, _gbp(v))], "£")


@_more("Y8.5.i", 6)
def _(d):
    p, r = pick(_by(d, [(1000, 10), (2000, 10), (1000, 20), (500, 20)],
                    [(1000, 10), (2000, 5), (500, 10), (4000, 5), (1000, 20)],
                    [(2000, 15), (5000, 6), (4000, 12), (2500, 8), (1500, 4)]))
    simple = p * r * 2 // 100
    comp = Decimal(p) * (Decimal(100 + r) / 100) ** 2 - p
    return _num("£%s is invested for 2 years at %d%% a year. How much MORE interest does compound interest earn than simple interest, "
                "in pounds?" % (_c(p), r), comp - simple,
                ["Simple: 2 × %d%% of %s = £%d." % (r, _c(p), simple), "Compound: %s × %s² − %s = %s." % (_c(p), _ds(Decimal(100 + r) / 100), _c(p), _gbp(comp)),
                 "Difference: %s." % _gbp(comp - simple)], "£")


@_more("Y8.5.i", 6)
def _(d):
    p = random.randint(*_by(d, (1, 10), (2, 10), (3, 40))) * 100
    r = pick(_by(d, [5, 10], [5, 10, 4, 2], [3, 6, 7, 8, 12]))
    pts = [(str(y), p + p * r * y // 100) for y in range(5)]
    return _lg("The graph shows the value of £%d invested at simple interest. What is the yearly interest, in pounds?" % p, pts,
               p * r // 100, ["The value goes up by the same amount every year.", "%d − %d = £%d a year." % (pts[1][1], p, p * r // 100)],
               "Value (£)", "Year")


@_more("Y8.5.j", 7)
def _(d):
    sc = _by(d, 5, 1, 1)                                       # easy: multiples of 5
    while True:
        a, b = random.randint(30 // sc, 80 // sc) * sc, random.randint(30 // sc, 80 // sc) * sc
        both = random.randint(5 // sc, (min(a, b) - 5) // sc) * sc
        if a + b - both <= 100 and both:
            break
    if d == 2:                                                 # stretch: work back from "neither" to "both"
        nei = 100 - (a + b - both)
        return _int("In a survey, %d%% of people like apples, %d%% like bananas and %d%% like neither. What percentage like both?"
                    % (a, b, nei), both,
                    ["%d%% like at least one: 100 − %d = %d%%." % (100 - nei, nei, 100 - nei),
                     "Both: %d + %d − %d = %d%%." % (a, b, 100 - nei, both)], "%")
    return _int("In a survey, %d%% of people like apples, %d%% like bananas and %d%% like both. What percentage like neither?"
                % (a, b, both), 100 - (a + b - both),
                ["Apples or bananas or both: %d + %d − %d = %d%%." % (a, b, both, a + b - both), "Neither: 100 − %d = %d%%." % (a + b - both, 100 - (a + b - both))], "%")


@_more("Y8.5.j", 7)
def _(d):
    bp = pick(_by(d, [50], [40, 50, 60, 30, 20], [35, 45, 55, 65, 24]))
    pb = pick(_by(d, [10, 20, 40], [10, 20, 30, 40, 50], [15, 25, 35, 45, 12]))
    pg = pick(_by(d, [20, 40, 60], [10, 20, 30, 40, 50, 60], [15, 25, 35, 55, 18]))
    tot = Decimal(bp * pb + (100 - bp) * pg) / 100
    return _num("In a school, %d%% of pupils are boys. %d%% of the boys and %d%% of the girls have a pet. What percentage of all the "
                "pupils have a pet?" % (bp, pb, pg), tot,
                ["Boys with pets: %d%% of %d%% = %s%%." % (pb, bp, _ds(Decimal(bp * pb) / 100)),
                 "Girls with pets: %d%% of %d%% = %s%%." % (pg, 100 - bp, _ds(Decimal((100 - bp) * pg) / 100)), "Total: %s%%." % _ds(tot)], "%")


@_more("Y8.5.j", 7)
def _(d):
    p1, p2 = pick(_by(d, [(10, 10), (50, 10), (10, 20), (50, 50), (20, 50)],
                      [(10, 20), (10, 10), (20, 25), (50, 10), (20, 50), (10, 30)],
                      [(15, 20), (12, 25), (5, 8), (30, 15), (4, 5), (25, 12)]))
    m = Decimal(100 + p1) / 100 * Decimal(100 + p2) / 100
    return _num("A town's population grows by %d%% one year and by %d%% the next year. What is the overall percentage increase?" % (p1, p2),
                (m - 1) * 100, ["Multiply: %s × %s = %s." % (_ds(Decimal(100 + p1) / 100), _ds(Decimal(100 + p2) / 100), _ds(m)),
                                "That is an increase of %s%% (not %d%%)." % (_ds((m - 1) * 100), p1 + p2)], "%")


@_more("Y8.5.j", 7)
def _(d):
    up, down = pick(_by(d, [(50, 50), (10, 10), (20, 20), (100, 50), (50, 10)],
                        [(20, 25), (25, 20), (50, 50), (10, 10), (20, 20), (25, 40)],
                        [(15, 20), (35, 20), (12, 25), (40, 30), (8, 5), (60, 35)]))
    m = Decimal(100 + up) / 100 * Decimal(100 - down) / 100
    return _num("A shop raises a price by %d%%, then later reduces the new price by %d%%. The final price is what percentage of the "
                "original price?" % (up, down), m * 100,
                ["%s × %s = %s." % (_ds(Decimal(100 + up) / 100), _ds(Decimal(100 - down) / 100), _ds(m)), "So %s%% of the original." % _ds(m * 100)], "%")


@_more("Y8.5.j", 7)
def _(d):
    while True:
        y7, y8 = random.randint(20, 60), pick([20, 25, 50]) if d == 0 else random.randint(20, 60)
        a = random.randint(5, y8 - 5)
        if (100 * a) % y8 == 0:
            break
    b = random.randint(5, y7 - 5)
    while d == 2 and (100 * (a + b)) % (y7 + y8):             # stretch: a percentage of everyone
        y7 = random.randint(20, 60)
        b = random.randint(5, y7 - 5)
    rows = [["Year 7", str(b), str(y7 - b), str(y7)], ["Year 8", str(a), str(y8 - a), str(y8)], ["Total", str(a + b), str(y7 + y8 - a - b), str(y7 + y8)]]
    if d == 2:
        rows = rows[:2]                                        # no total row: the pupil adds the two years
        pct = 100 * (a + b) // (y7 + y8)
        return _dt("The two-way table shows which pupils went on a school trip. What percentage of ALL the pupils (Years 7 and 8 "
                   "together) went on the trip?", ["", "Went", "Did not go", "Total"], rows, pct,
                   ["%d + %d = %d pupils went, out of %d + %d = %d." % (b, a, a + b, y7, y8, y7 + y8),
                    "%d/%d × 100 = %d%%." % (a + b, y7 + y8, pct)])
    return _dt("The two-way table shows which pupils went on a school trip. What percentage of Year 8 went on the trip?",
               ["", "Went", "Did not go", "Total"], rows, 100 * a // y8,
               ["%d of the %d Year 8 pupils went." % (a, y8), "%d/%d × 100 = %d%%." % (a, y8, 100 * a // y8)])


# ================================================================== 8.6 ======
def _t(c, v, first=False):
    """One algebra term with its sign: (3,'x') -> '+3x', (-1,'x') -> '-x', (5,'') -> '+5'."""
    if c == 0:
        return ""
    body = (str(abs(c)) if abs(c) != 1 or not v else "") + v
    sign = "-" if c < 0 else ("" if first else "+")
    return sign + body


def _expr(*terms):
    """_expr((2,'x^2'), (5,'x'), (-3,'')) -> '2x^2+5x-3'."""
    out = ""
    for c, v in terms:
        out += _t(c, v, first=(out == ""))
    return out or "0"


@_more("Y8.6.e", 10)
def _(d):
    while True:
        k, b, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 3, 6, 9)), random.randint(1, _by(d, 6, 9, 15))
        if gcd(b, c) == 1:
            break
    return _wq("Factorise %s fully (like 3(2x-3))." % _expr((k * b, "x"), (-k * c, "")), "%d(%s)" % (k, _expr((b, "x"), (-c, ""))),
               ["The highest common factor of %d and %d is %d." % (k * b, k * c, k),
                "%s = %d(%s)." % (_expr((k * b, "x"), (-k * c, "")), k, _expr((b, "x"), (-c, "")))], "e.g. 3(2x-3)")


@_more("Y8.6.e", 10)
def _(d):
    while True:
        k, p, q = random.randint(2, _by(d, 4, 6, 9)), random.randint(1, _by(d, 3, 5, 9)), random.randint(1, _by(d, 5, 7, 12))
        if gcd(p, q) == 1:
            break
    v1, v2 = pick([("a", "b"), ("x", "y"), ("p", "q"), ("m", "n")])
    ex = _expr((k * p, v1 + v2), (k * q, v1))
    ans = "%d%s(%s)" % (k, v1, _expr((p, v2), (q, "")))
    return _wq("Factorise %s fully (like 2a(2b+3))." % ex, ans,
               ["Both terms have the factors %d and %s." % (k, v1), "%s = %s." % (ex, ans)], "e.g. 2a(2b+3)")


@_more("Y8.6.e", 10)
def _(d):
    while True:
        hi = _by(d, 3, 5, 9)
        k, a, b, c = random.randint(2, _by(d, 4, 6, 9)), random.randint(1, hi), random.randint(1, hi), random.randint(1, _by(d, 6, 9, 15))
        if gcd(gcd(a, b), c) == 1:
            break
    ex = _expr((k * a, "x"), (k * b, "y"), (k * c, ""))
    ans = "%d(%s)" % (k, _expr((a, "x"), (b, "y"), (c, "")))
    return _wq("Factorise %s fully (like 3(2x+3y+4))." % ex, ans,
               ["All three terms divide by %d." % k, "%s = %s." % (ex, ans)], "e.g. 3(2x+3y+4)")


@_more("Y8.6.e", 10)
def _(d):
    while True:
        k, b, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 3, 6, 9)), random.randint(1, _by(d, 6, 9, 15))
        if gcd(b, c) == 1:
            break
    return _wq("A rectangle has area (%s) cm² and width %d cm. Write an expression for its length (like 2x+3)." % (_expr((k * b, "x"), (k * c, "")), k),
               _expr((b, "x"), (c, "")), ["Length = area ÷ width.", "%s = %d(%s), so the length is %s." % (_expr((k * b, "x"), (k * c, "")), k, _expr((b, "x"), (c, "")), _expr((b, "x"), (c, "")))],
               "e.g. 2x+3")


@_more("Y8.6.e", 10)
def _(d):
    while True:
        k, b, c = random.randint(2, _by(d, 5, 9, 12)), random.randint(1, _by(d, 3, 6, 9)), random.randint(2, _by(d, 6, 9, 15))
        if gcd(b, c) == 1:
            break
    return _int("%s factorised %s as %d(%s). The number at the end of the bracket is wrong. What should it be?"
                % (_who(), _expr((k * b, "x"), (k * c, "")), k, _expr((b, "x"), (k * c, ""))), c,
                ["Check by expanding: %d × %d = %d, not %d." % (k, k * c, k * k * c, k * c), "%d ÷ %d = %d." % (k * c, k, c)])


@_more("Y8.6.e", 10)
def _(d):
    while True:
        k, b, c = random.randint(2, _by(d, 4, 6, 9)), random.randint(1, _by(d, 3, 5, 9)), random.randint(1, _by(d, 5, 7, 12))
        if gcd(b, c) == 1:
            break
    ex = _expr((k * b, "x^2"), (k * c, "x"))
    ans = "%sx(%s)" % (k, _expr((b, "x"), (c, "")))
    return _wq("Factorise %s fully (like 3x(2x+3))." % ex, ans,
               ["The highest common factor is %dx." % k, "%s = %s." % (ex, ans)], "e.g. 3x(2x+3)")


def _quad(a, b, c):
    return _expr((a, "x^2"), (b, "x"), (c, ""))


@_more("Y8.6.f", 7)
def _(d):
    r = _by(d, 6, 9, 12)
    p, q = pick([x for x in range(-r, r + 1) if x]), pick([x for x in range(-r, r + 1) if x])
    if d == 0:                                                 # easy: both brackets add a positive number
        p, q = abs(p), abs(q)
    elif p > 0 and q > 0:
        p = -p
    br = lambda n: "(x%s%d)" % ("+" if n > 0 else "-", abs(n))
    return _wq("Expand and simplify %s%s (like x^2+2x-15)." % (br(p), br(q)), _quad(1, p + q, p * q),
               ["x × x = x², x × %d and %d × x give %s, %d × %d = %d." % (q, p, _expr((p + q, "x")) or "0x", p, q, p * q),
                "= %s." % _quad(1, p + q, p * q)], "e.g. x^2+2x-15")


@_more("Y8.6.f", 7)
def _(d):
    lo, hi = _by(d, (1, 6), (-9, 9), (-15, 15))                 # easy: no negatives
    p, q = pick([x for x in range(lo, hi + 1) if x]), pick([x for x in range(lo, hi + 1) if x])
    br = lambda n: "(x%s%d)" % ("+" if n > 0 else "-", abs(n))
    if random.random() < 0.5:
        return _int("Expand %s%s. What is the coefficient of x?" % (br(p), br(q)), p + q, ["%d + (%d) = %d." % (p, q, p + q)])
    return _int("Expand %s%s. What is the number term (the constant)?" % (br(p), br(q)), p * q, ["%d × (%d) = %d." % (p, q, p * q)])


@_more("Y8.6.f", 7)
def _(d):
    a = random.randint(2, _by(d, 2, 4, 6))
    p = pick([x for x in range(1, _by(d, 6, 8, 10)) if gcd(x, a) == 1])
    q = pick([x for x in range(*_by(d, (1, 6), (-6, 8), (-10, 11))) if x])
    br = "(x%s%d)" % ("+" if q > 0 else "-", abs(q))
    ans = _quad(a, a * q + p, p * q)
    qs = "(%d)" % q if q < 0 else str(q)
    return _wq("Expand and simplify (%dx+%d)%s (like 2x^2+7x+3)." % (a, p, br), ans,
               ["%dx × x = %dx², %dx × %s = %dx, %d × x = %dx, %d × %s = %d." % (a, a, a, qs, a * q, p, p, p, qs, p * q),
                "= %s." % ans], "e.g. 2x^2+7x+3")


@_more("Y8.6.f", 7)
def _(d):
    a, b = random.randint(1, _by(d, 5, 9, 15)), random.randint(1, _by(d, 5, 9, 15))
    rows = [["x", "x²", _expr((b, "x"))], ["+%d" % a, _expr((a, "x")), str(a * b)]]
    if random.random() < 0.5:
        return _dt("The grid expands (x + %d)(x + %d). What number goes in the empty cell?" % (a, b), ["×", "x", "+%d" % b], rows,
                   a * b, ["%d × %d = %d." % (a, b, a * b)], missing=(1, 2))
    return _dt("The grid expands (x + %d)(x + %d). Add up the cells: what is the coefficient of x in the answer?" % (a, b),
               ["×", "x", "+%d" % b], rows, a + b, ["%s + %s = %dx." % (_expr((b, "x")), _expr((a, "x")), a + b)])


@_more("Y8.6.f", 7)
def _(d):
    a = random.randint(1, _by(d, 5, 9, 12))
    if d == 2 and random.random() < 0.5:                       # stretch: (x − a)², a negative middle term
        a = -a
    br = "(x%s%d)" % ("+" if a > 0 else "-", abs(a))
    return _wq("Expand and simplify %s^2 − x^2 (like 6x+9)." % br, _expr((2 * a, "x"), (a * a, "")),
               ["%s² = %s." % (br, _quad(1, 2 * a, a * a)), "Subtract x²: %s." % _expr((2 * a, "x"), (a * a, ""))], "e.g. 6x+9")


@_more("Y8.6.f", 7)
def _(d):
    p, q = random.randint(1, _by(d, 5, 8, 12)), random.randint(1, _by(d, 5, 8, 12))
    x = random.randint(1, 5) if d == 0 else -random.randint(*_by(d, None, (1, 6), (3, 12)))   # easy: a positive x
    return _int("Expand (x+%d)(x+%d) and then find its value when x = %d." % (p, q, x), (x + p) * (x + q),
                ["(%d + %d)(%d + %d) = %d × %d." % (x, p, x, q, x + p, x + q), "= %d." % ((x + p) * (x + q))])


@_more("Y8.6.g", 11)
def _(d):
    k, c = random.randint(2, 6), random.randint(1, 9)
    right = random.random() < 0.5
    rhs = _expr((k, "x"), (k * c if right else c, ""))
    return _yn("Is %d(x+%d) = %s true for every value of x?" % (k, c, rhs), right,
               ["%d(x+%d) = %s." % (k, c, _expr((k, "x"), (k * c, ""))),
                "So it is %san identity." % ("" if right else "not ")])


@_more("Y8.6.g", 11)
def _(d):
    k, a, c = random.randint(2, 7), random.randint(1, 5), random.randint(1, 9)
    return _int("Fill in the gap: %d(%s − ?) = %s." % (k, _expr((a, "x")), _expr((k * a, "x"), (-k * c, ""))), c,
                ["%d × ? = %d." % (k, k * c), "? = %d." % c])


@_more("Y8.6.g", 11)
def _(d):
    a, b, c, e = random.randint(2, 9), random.randint(2, 9), random.randint(1, 8), random.randint(1, 8)
    while a <= c:
        a, c = random.randint(2, 9), random.randint(1, 8)
    ex = "%dx + %dy − %s + %s" % (a, b, "x" if c == 1 else "%dx" % c, "y" if e == 1 else "%dy" % e)
    return _wq("Simplify %s (like 3x+5y)." % ex, _expr((a - c, "x"), (b + e, "y")),
               ["x terms: %d − %d = %d." % (a, c, a - c), "y terms: %d + %d = %d." % (b, e, b + e)], "e.g. 3x+5y")


@_more("Y8.6.g", 11)
def _(d):
    k, c = random.randint(2, 9), random.randint(2, 9)
    return _int("%s writes %d(x − %d) = %dx − %d. The number term is wrong. What should it be?" % (_who(), k, c, k, c), -k * c,
                ["Multiply BOTH terms in the bracket by %d." % k, "%d × (−%d) = −%d." % (k, c, k * c)])


@_more("Y8.6.g", 11)
def _(d):
    a, b, c, e = random.randint(1, 5), random.randint(1, 9), random.randint(1, 5), random.randint(1, 9)
    return _wq("A rectangle has sides (%s) cm and (%s) cm. Write a simplified expression for its perimeter (like 6x+8)."
               % (_expr((a, "x"), (b, "")), _expr((c, "x"), (e, ""))), _expr((2 * (a + c), "x"), (2 * (b + e), "")),
               ["Perimeter = 2 × (%s + %s)." % (_expr((a, "x"), (b, "")), _expr((c, "x"), (e, ""))),
                "= %s." % _expr((2 * (a + c), "x"), (2 * (b + e), ""))], "e.g. 6x+8")


@_more("Y8.6.h", 10)
def _(d):
    m, c = random.randint(2, _by(d, 4, 7, 12)), random.randint(*_by(d, (20, 40), (30, 80), (40, 150)))
    n = random.randint(*_by(d, (2, 5), (3, 10), (8, 25)))
    return _int("The rule for a sequence is: term = %d − %d × position. What is the term in position %d?" % (c, m, n), c - m * n,
                ["%d − %d × %d = %d − %d." % (c, m, n, c, m * n), "= %d." % (c - m * n)])


@_more("Y8.6.h", 10)
def _(d):
    a, b = random.randint(2, _by(d, 5, 9, 12)), random.randint(*_by(d, (0, 9), (-5, 9), (-15, 15)))
    ns = sorted(random.sample(range(1, _by(d, 11, 13, 31)), 4))
    i = random.randrange(4)
    rule = "%sn%s" % (a, ("+%d" % b) if b > 0 else ("−%d" % -b if b < 0 else ""))
    return _io("The rule is term = %s. What is the missing term?" % rule, [(n, a * n + b) for n in ns], i, a * ns[i] + b,
               ["%d × %d %s %d = %d." % (a, ns[i], "+" if b >= 0 else "−", abs(b), a * ns[i] + b)], rule="term = " + rule)


@_more("Y8.6.h", 10)
def _(d):
    a, b = random.randint(2, _by(d, 5, 9, 12)), pick([x for x in range(*_by(d, (1, 10), (-4, 10), (-15, 16))) if x])
    n = random.randint(*_by(d, (5, 15), (10, 40), (40, 120)))
    val = a * n + b + (0 if random.random() < 0.5 else random.randint(1, a - 1))
    rule = "%dn%s" % (a, ("+%d" % b) if b > 0 else ("−%d" % -b if b < 0 else ""))
    yes = (val - b) % a == 0
    return _yn("A sequence has nth term %s. Is %d a term of the sequence?" % (rule, val), yes,
               ["Solve %s = %d: %dn = %d." % (rule, val, a, val - b),
                "n = %s, %s a whole number." % (_ds(Decimal(val - b) / a), "which is" if yes else "which is not")])


@_more("Y8.6.h", 10)
def _(d):
    a, b = random.randint(2, _by(d, 5, 9, 12)), pick([x for x in range(*_by(d, (1, 10), (-4, 10), (-15, 16))) if x])
    n = random.randint(*_by(d, (3, 12), (5, 30), (30, 120)))
    rule ="%dn%s" % (a, ("+%d" % b) if b > 0 else ("−%d" % -b if b < 0 else ""))
    return _int("A sequence has nth term %s. Which term number is %d?" % (rule, a * n + b), n,
                ["%s = %d, so %dn = %d." % (rule, a * n + b, a, a * n), "n = %d." % n])


@_more("Y8.6.h", 10)
def _(d):
    first, add = random.randint(3, _by(d, 5, 6, 9)), random.randint(2, _by(d, 3, 5, 9))
    n = random.randint(*_by(d, (4, 10), (8, 25), (30, 100)))
    return _int("Pattern 1 uses %d matchsticks. Each new pattern uses %d more matchsticks than the one before. How many matchsticks "
                "are in pattern %d?" % (first, add, n), first + add * (n - 1),
                ["The rule is %d + %d × (n − 1)." % (first, add), "%d + %d × %d = %d." % (first, add, n - 1, first + add * (n - 1))])


@_more("Y8.6.h", 10)
def _(d):
    c = random.randint(*_by(d, (0, 9), (-5, 9), (-30, 30)))
    n = random.randint(*_by(d, (2, 6), (3, 12), (9, 20)))
    rule = "n²" + (("+%d" % c) if c > 0 else ("−%d" % -c if c < 0 else ""))
    return _int("The nth term of a sequence is %s. What is the %s term?" % (rule, ordinal(n)), n * n + c,
                ["%d² = %d." % (n, n * n), "%d %s %d = %d." % (n * n, "+" if c >= 0 else "−", abs(c), n * n + c)])


@_more("Y8.6.h", 10)
def _(d):
    start, step = random.randint(*_by(d, (20, 40), (5, 20), (5, 20))), random.randint(*_by(d, (2, 3), (2, 6), (4, 9)))
    n = random.randint(*_by(d, (4, 8), (6, 12), (12, 30)))
    return _int("A sequence starts at %d and the rule is 'subtract %d'. What is the %s term?" % (start, step, ordinal(n)),
                start - step * (n - 1), ["%d − %d × %d = %d." % (start, step, n - 1, start - step * (n - 1))])


# ================================================================== 8.7 ======
@_more("Y8.7.e", 10)
def _(d):
    k = pick(_by(d, [1, 4], [1, 2, 3, 4, 7], [7, 10, 13, 16, 3]))     # 180 ÷ (k + 2) is whole
    x = 180 // (k + 2)
    return _int("In an isosceles triangle each base angle is x° and the third angle is %s°. Find x." % ("x" if k == 1 else "%dx" % k), x,
                ["x + x + %s = 180, so %dx = 180." % ("x" if k == 1 else "%dx" % k, k + 2), "x = %d." % x], "°")


@_more("Y8.7.e", 10)
def _(d):
    n = random.randint(*_by(d, (2, 2), (2, 4), (4, 6)))
    x = random.randint(*_by(d, (2, 15), (2, 30), (20, 120))) * 2
    s = sum(x + 2 * i for i in range(n))
    return _int("%d consecutive even numbers add up to %d. What is the smallest of them?" % (n, s), x,
                ["Call them %s." % ", ".join(["x"] + ["x + %d" % (2 * i) for i in range(1, n)]),
                 "%dx + %d = %d, so x = %d." % (n, n * (n - 1), s, x)])


@_more("Y8.7.e", 10)
def _(d):
    if d == 2:                                                 # stretch: a subtracted term too
        x, a = random.randint(6, 25), random.randint(2, 12)
        b = random.randint(max(1, x - a + 1), 2 * x)          # keeps 3x − b < x + (x + a): a real triangle
        p = x + (x + a) + (3 * x - b)
        return _int("A triangle has sides x cm, (x + %d) cm and (3x − %d) cm. Its perimeter is %d cm. Find x." % (a, b, p), x,
                    ["x + x + %d + 3x − %d = 5x %s %d = %d." % (a, b, "+" if a >= b else "−", abs(a - b), p),
                     "5x = %d, so x = %d." % (p - a + b, x)], "cm")
    x, a = random.randint(3, _by(d, 10, 15, None)), random.randint(1, 6)
    p = x + (x + a) + 2 * x
    return _int("A triangle has sides x cm, (x + %d) cm and 2x cm. Its perimeter is %d cm. Find x." % (a, p), x,
                ["x + x + %d + 2x = 4x + %d = %d." % (a, a, p), "4x = %d, so x = %d." % (p - a, x)], "cm")


@_more("Y8.7.e", 10)
def _(d):
    x, extra = random.randint(4, _by(d, 10, 15, 25)), random.randint(2, _by(d, 5, 8, 12))
    na, nc = random.randint(1, _by(d, 1, 3, 5)), random.randint(2, _by(d, 3, 5, 8))
    tot = na * (x + extra) + nc * x
    return _int("A child's ticket costs £x and an adult's ticket costs £%d more. %d adult%s and %d children pay £%d altogether. Find x."
                % (extra, na, "" if na == 1 else "s", nc, tot), x,
                ["%d(x + %d) + %dx = %d." % (na, extra, nc, tot), "%dx + %d = %d, so x = %d." % (na + nc, na * extra, tot, x)], "£")


@_more("Y8.7.e", 10)
def _(d):
    who = _who()
    if d == 0:                                                 # easy: one equation, ages added
        x, k = random.randint(5, 12), random.randint(2, 4)
        return _int("%s's aunt is %d times as old as %s. Their ages add up to %d. How old is %s?" % (who, k, who, (k + 1) * x, who), x,
                    ["Let %s's age be x: x + %dx = %d." % (who, k, (k + 1) * x), "%dx = %d, so x = %d." % (k + 1, (k + 1) * x, x)], "years")
    while True:
        x, k, m = random.randint(5, 14), random.randint(3, _by(d, None, 5, 7)), random.randint(2, _by(d, None, 3, 4))
        if m < k and (x * (k - m)) % (m - 1) == 0:
            t = x * (k - m) // (m - 1)
            if 2 <= t <= 40:
                break
    times = {2: "twice", 3: "three times", 4: "four times"}[m]
    return _int("%s's aunt is %d times as old as %s. In %d years' time she will be %s as old as %s. How old is %s now?"
                % (who, k, who, t, times, who, who), x,
                ["Let %s's age be x: %dx + %d = %d(x + %d)." % (who, k, t, m, t),
                 "%dx + %d = %dx + %d, so %s = %d and x = %d." % (k, t, m, m * t, "x" if k - m == 1 else "%dx" % (k - m), m * t - t, x)], "years")


@_more("Y8.7.e", 10)
def _(d):
    if d == 0:                                    # easy: x + (x + a) + (x + b) + 90 = 360
        while True:
            x, a = random.randint(40, 80), random.randint(5, 30)
            b = 270 - 3 * x - a
            if 5 <= b and x + b < 180:
                break
        return _int("A quadrilateral has a right angle. Its other angles are x°, (x + %d)° and (x + %d)°. Find x." % (a, b), x,
                    ["Angles in a quadrilateral add up to 360°.", "3x + %d + 90 = 360, so 3x = %d and x = %d." % (a + b, 270 - a - b, x)], "°")
    if d == 2:                                    # stretch: (2x + a) + 3x + (x − b) + (4x + c) = 360
        while True:
            x, a, c = random.randint(20, 34), random.randint(5, 30), random.randint(5, 30)
            b = 10 * x + a + c - 360
            if 1 <= b < x and 4 * x + c < 180:
                break
        return _int("The angles of a quadrilateral are (2x + %d)°, 3x°, (x − %d)° and (4x + %d)°. Find x." % (a, b, c), x,
                    ["Angles in a quadrilateral add up to 360°.",
                     "10x + %d − %d + %d = 360, so 10x = %d and x = %d." % (a, b, c, 360 - a + b - c, x)], "°")
    while True:                                   # x + 2x + (x + a) + (3x − b) = 360
        x, a = random.randint(20, 80), random.randint(5, 30)
        b = 7 * x + a - 360
        if 5 <= b <= 60 and all(0 < t < 180 for t in (x, 2 * x, x + a, 3 * x - b)):
            break
    return _int("The angles of a quadrilateral are x°, 2x°, (x + %d)° and (3x − %d)°. Find x." % (a, b), x,
                ["Angles in a quadrilateral add up to 360°.", "7x + %d − %d = 360, so 7x = %d and x = %d." % (a, b, 360 - a + b, x)], "°")


@_more("Y8.7.e", 10)
def _(d):
    w, x, c = random.randint(*_by(d, (2, 5), (3, 9), (6, 15))), random.randint(2, _by(d, 8, 12, 25)), random.randint(1, _by(d, 5, 8, 15))
    return _int("A rectangle is %d cm wide and (x + %d) cm long. Its area is %d cm². Find x." % (w, c, w * (x + c)), x,
                ["%d(x + %d) = %d." % (w, c, w * (x + c)), "x + %d = %d, so x = %d." % (c, x + c, x)], "cm")


@_more("Y8.7.f", 9)
def _(d):
    a = random.randint(*_by(d, (0, 5), (-6, 3), (-20, 3)))
    b = a + random.randint(*_by(d, (2, 5), (3, 8), (6, 20)))
    lo_inc, hi_inc = random.random() < 0.5, random.random() < 0.5
    ints = [n for n in range(a - 1, b + 2) if (n >= a if lo_inc else n > a) and (n <= b if hi_inc else n < b)]
    return _int("How many whole numbers satisfy %d %s x %s %d?" % (a, "≤" if lo_inc else "<", "≤" if hi_inc else "<", b), len(ints),
                ["They are %s." % ", ".join(map(str, ints)), "That is %d whole numbers." % len(ints)])


@_more("Y8.7.f", 9)
def _(d):
    n = random.randint(*_by(d, (1, 12), (-5, 12), (-30, -1)))
    words, sym = pick(_by(d, [("less than", "<"), ("more than", ">"), ("at least", ">=")],
                          [("at least", ">="), ("at most", "<="), ("less than", "<"), ("more than", ">"), ("no more than", "<="), ("no less than", ">=")],
                          [("at most", "<="), ("no more than", "<="), ("no less than", ">="), ("not more than", "<="), ("not less than", ">=")]))
    return _wq("Write 'x is %s %d' using a symbol (like x>=4)." % (words, n), "x%s%d" % (sym, n),
               ["'%s' means %s." % (words, {">=": "greater than or equal to", "<=": "less than or equal to", "<": "less than", ">": "greater than"}[sym]),
                "x%s%d." % (sym, n)], "e.g. x>=4")


@_more("Y8.7.f", 9)
def _(d):
    v, rule, sym, word = pick(_by(
        d, [("a", "be under 16 to get a child ticket", "<", 16), ("s", "score more than 50 to pass", ">", 50),
            ("h", "be at least 120 cm tall to go on a ride", ">=", 120)],
        [("h", "be at least 120 cm tall to go on a ride", ">=", 120), ("a", "be under 16 to get a child ticket", "<", 16),
         ("w", "weigh no more than 23 kg to go in the hold", "<=", 23), ("s", "score more than 50 to pass", ">", 50)],
        [("t", "run 100 m in under 12.5 seconds to qualify", "<", "12.5"), ("c", "spend at least £25 to get free delivery", ">=", 25),
         ("v", "drive at no more than 70 mph on a motorway", "<=", 70), ("n", "have more than 9 people for a group discount", ">", 9),
         ("m", "carry no more than 7.5 kg of hand luggage", "<=", "7.5"), ("T", "keep the freezer at no more than −18 °C", "<=", -18)]))
    word = str(word)
    return _wq("You must %s. Write this as an inequality using %s (like %s>=4)." % (rule, v, v), "%s%s%s" % (v, sym, word),
               ["The boundary is %s and the symbol is %s." % (word, _sym(sym)), "%s%s%s." % (v, sym, word)], "e.g. %s>=4" % v)


@_more("Y8.7.f", 9)
def _(d):
    lo, hi, sc = _by(d, (1, 60, 10), (-60, 60, 10), (-1500, -1, 100))    # easy: positive; stretch: negative, 2 d.p.
    x = Decimal(random.randint(lo, hi)) / sc
    while x == int(x):
        x = Decimal(random.randint(lo, hi)) / sc
    if random.random() < 0.5:
        return _int("What is the largest whole number x with x < %s?" % _ds(x).replace("-", "−"), floor(x),
                    ["Whole numbers less than %s: …, %d, %d." % (_ds(x), floor(x) - 1, floor(x)), "The largest is %d." % floor(x)])
    return _int("What is the smallest whole number x with x > %s?" % _ds(x).replace("-", "−"), ceil(x),
                ["Whole numbers greater than %s: %d, %d, …" % (_ds(x), ceil(x), ceil(x) + 1), "The smallest is %d." % ceil(x)])


@_more("Y8.7.f", 9)
def _(d):
    v = random.randint(*_by(d, (0, 6), (-4, 4), (-12, -2)))
    op = pick(_by(d, [">", "<"], [">", ">=", "<", "<="], [">=", "<="]))      # stretch: the boundary itself may be the answer
    test ={">": operator.gt, ">=": operator.ge, "<": operator.lt, "<=": operator.le}[op]
    while True:
        cands = random.sample(range(v - 4, v + 5), 3)
        ok = [c for c in cands if test(c, v)]
        if len(ok) == 1:
            break
    return {"prompt": "The number line shows an inequality. Which of %s satisfies it?" % ", ".join(map(str, cands)),
            "component": "inequality_line", "spec": {"op": op, "value": v, "min": v - 6, "max": v + 6},
            "answer": ok[0], "answer_type": "int",
            "solution": ["The line shows x %s %d." % (_sym(op), v), "Only %d fits." % ok[0]]}


@_more("Y8.7.g", 10)
def _(d):
    a = random.randint(2, 6)
    x = random.randint(-6, 6)
    op, flip = pick([(">", "<"), ("<", ">"), (">=", "<="), ("<=", ">=")])
    return _wq("Solve −%dx %s %d (like x<-3)." % (a, _sym(op), -a * x), "x%s%d" % (flip, x),
               ["Divide both sides by −%d." % a, "Dividing by a negative number reverses the inequality: x %s %d." % (_sym(flip), x)],
               "e.g. x<-3")


@_more("Y8.7.g", 10)
def _(d):
    while True:
        a, c = random.randint(3, 9), random.randint(1, 5)
        if a > c:
            break
    x = random.randint(-3, 9)
    b = random.randint(1, 15)
    e = (a - c) * x + b
    op = pick([">", "<", ">=", "<="])
    return _wq("Solve %s %s %s (like x>4)." % (_expr((a, "x"), (b, "")), _sym(op), _expr((c, "x"), (e, ""))), "x%s%d" % (op, x),
               ["Subtract %s from both sides: %s %s %d." % (_expr((c, "x")), _expr((a - c, "x"), (b, "")), _sym(op), e),
                "%s %s %d, so x %s %d." % (_expr((a - c, "x")), _sym(op), e - b, _sym(op), x)], "e.g. x>4")


@_more("Y8.7.g", 10)
def _(d):
    a, c = random.randint(2, 6), random.randint(1, 8)
    x = random.randint(-2, 9)
    op = pick(["<", "<=", ">", ">="])
    return _wq("Solve %d(x + %d) %s %d (like x<=5)." % (a, c, _sym(op), a * (x + c)), "x%s%d" % (op, x),
               ["Divide by %d: x + %d %s %d." % (a, c, _sym(op), x + c), "x %s %d." % (_sym(op), x)], "e.g. x<=5")


@_more("Y8.7.g", 10)
def _(d):
    a, b = random.randint(2, 5), random.randint(1, 9)
    lo = random.randint(-2, 3)
    hi = lo + random.randint(2, 5)
    return _int("How many whole numbers x satisfy %d < %dx + %d ≤ %d?" % (a * lo + b, a, b, a * hi + b), hi - lo,
                ["Subtract %d, then divide by %d: %d < x ≤ %d." % (b, a, lo, hi),
                 "x = %s." % ", ".join(str(n) for n in range(lo + 1, hi + 1))])


@_more("Y8.7.g", 10)
def _(d):
    k, c, x = random.randint(2, 5), random.randint(1, 9), random.randint(1, 8)
    op = pick([">", "<", ">=", "<="])
    return _wq("Solve x/%d + %d %s %d (like x>9)." % (k, c, _sym(op), x + c), "x%s%d" % (op, k * x),
               ["Subtract %d: x/%d %s %d." % (c, k, _sym(op), x), "Multiply by %d: x %s %d." % (k, _sym(op), k * x)], "e.g. x>9")


@_more("Y8.7.g", 10)
def _(d):
    limit = pick([500, 600, 800, 1000])
    person = random.randint(60, 95)
    box = pick([15, 20, 25, 30])
    n = (limit - person) // box
    return _int("A lift can carry at most %d kg. A worker weighing %d kg gets in with some %d kg boxes. What is the greatest number "
                "of boxes the worker can take?" % (limit, person, box), n,
                ["%d + %db ≤ %d, so %db ≤ %d." % (person, box, limit, box, limit - person),
                 "b ≤ %s, so at most %d boxes." % (_ds(_round(Decimal(limit - person) / box, 2)), n)], "boxes")


# ================================================================== 8.8 ======
def _ang(prompt, deg, answer, solution):
    """An angle drawn as a picture, with a degrees answer box."""
    return {"prompt": prompt, "component": "angle", "spec": {"mode": "classify", "degrees": int(deg), "numeric": True},
            "answer": int(answer), "answer_type": "int", "solution": solution}


def _shoelace(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return Fraction(abs(s), 2)


@_more("Y8.8.e", 9)
def _(d):
    big = random.random() < 0.5
    # easy: x, x, 2x, 2x; core: x, 2x, 3x, 4x; stretch: less friendly multipliers
    m = pick(_by(d, [(1, 1, 2, 2), (1, 1, 1, 2)], [(1, 2, 3, 4)], [(2, 3, 5, 8), (1, 3, 5, 6), (2, 4, 5, 7), (3, 4, 5, 8)]))
    x = 360 // sum(m)
    ans = x * (m[-1] if big else m[0])
    terms = ["%sx°" % ("" if k == 1 else k) for k in m]
    return _int("The angles of a quadrilateral are %s, %s, %s and %s. What is the %s angle?" % tuple(terms + ["largest" if big else "smallest"]),
                ans, ["%s = %dx = 360°, so x = %d." % (" + ".join(t[:-1] for t in terms), sum(m), x),
                      "The %s angle is %d°." % ("largest" if big else "smallest", ans)], "°")


@_more("Y8.8.e", 9)
def _(d):
    while True:
        if d == 0:                                    # easy: multiples of 10
            a, b = random.randint(4, 15) * 10, random.randint(3, 12) * 10
        else:
            a, b = random.randint(_by(d, 40, 40, 25), _by(d, 150, 150, 170)), random.randint(_by(d, 30, 30, 15), 120)
        rest = 360 - a - b
        if rest % 2 == 0 and 20 < rest // 2 < 170 and (d < 2 or rest % 20):
            break
    return _int("A kite has one pair of equal angles. The other two angles are %d° and %d°. How big is each of the equal angles?" % (a, b),
                rest // 2, ["360 − %d − %d = %d." % (a, b, rest), "%d ÷ 2 = %d°." % (rest, rest // 2)], "°")


@_more("Y8.8.e", 9)
def _(d):
    lo, hi = _by(d, (4, 14), (40, 140), (15, 165))
    a = random.randint(lo, hi) * (10 if d == 0 else 1)          # easy: multiples of 10
    while a == 90:
        a = random.randint(lo, hi) * (10 if d == 0 else 1)
    return _ang("The angle shown is %d°. It is one angle of a parallelogram. How many degrees is the angle NEXT to it (on the same side)?" % a,
                a, 180 - a, ["Next-door angles in a parallelogram add up to 180°.", "180 − %d = %d°." % (a, 180 - a)])


@_more("Y8.8.e", 9)
def _(d):
    a = _by(d, random.randint(5, 13) * 10, random.randint(50, 130), random.randint(50, 130))
    if d == 2:                                    # stretch: one more step, round the trapezium to angle BCD
        c = random.randint(40, 140)
        return _int("In a trapezium ABCD, AB is parallel to DC. Angle DAB is %d° and angle ABC is %d°. What is angle ADC + angle BCD?"
                    % (a, c), 360 - a - c,
                    ["Co-interior angles: ADC = 180 − %d = %d° and BCD = 180 − %d = %d°." % (a, 180 - a, c, 180 - c),
                     "%d + %d = %d°." % (180 - a, 180 - c, 360 - a - c)], "°")
    return _int("In a trapezium ABCD, AB is parallel to DC. Angle DAB is %d°. What is angle ADC?" % a, 180 - a,
                ["AD crosses the parallel lines, so angles DAB and ADC are co-interior and add up to 180°.", "180 − %d = %d°." % (a, 180 - a)], "°")


@_more("Y8.8.e", 9)
def _(d):
    a = _by(d, random.randint(3, 8) * 10, random.randint(30, 85), random.randint(11, 169))
    while a == 90:
        a += 1
    opp = random.random() < 0.5
    return _int("One angle of a rhombus is %d°. What is the angle %s it?" % (a, "opposite" if opp else "next to"), a if opp else 180 - a,
                ["In a rhombus opposite angles are equal and next-door angles add up to 180°.",
                 "%s" % ("The opposite angle is also %d°." % a if opp else "180 − %d = %d°." % (a, 180 - a))], "°")


@_more("Y8.8.e", 9)
def _(d):
    if d == 2:                                    # stretch: x°, 2x° and (x + a)° — the x terms differ
        while True:
            a = random.randint(5, 60)
            if (180 - a) % 4 == 0:
                x = (180 - a) // 4
                break
        big = max(2 * x, x + a)
        return _int("The angles of a triangle are x°, 2x° and (x + %d)°. What is the largest angle?" % a, big,
                    ["4x + %d = 180, so 4x = %d and x = %d." % (a, 180 - a, x),
                     "The angles are %d°, %d° and %d°; the largest is %d°." % (x, 2 * x, x + a, big)], "°")
    while True:                                   # x + (x + a) + (x + b) = 180
        a, b = random.randint(5, 40), random.randint(5, 60)
        if d == 0:                                # easy: steps of 10
            a, b = a // 10 * 10 + 10, b // 10 * 10 + 10
        if (180 - a - b) % 3 == 0 and a != b:
            x = (180 - a - b) // 3
            break
    return _int("The angles of a triangle are x°, (x + %d)° and (x + %d)°. What is the largest angle?" % (a, b), x + max(a, b),
                ["3x + %d = 180, so 3x = %d and x = %d." % (a + b, 180 - a - b, x), "Largest: %d + %d = %d°." % (x, max(a, b), x + max(a, b))], "°")


@_more("Y8.8.j", 9)
def _(d):
    while True:
        # easy: P up-and-right of C, scale factor 2; stretch: the centre can sit anywhere, factors up to 4
        cx, cy = random.randint(0, _by(d, 3, 3, 8)), random.randint(0, _by(d, 3, 3, 8))
        px, py = cx + random.randint(_by(d, 1, -2, -3), 3), cy + random.randint(_by(d, 1, -2, -3), 3)
        k = pick(_by(d, [2], [2, 3], [3, 4]))
        ix, iy = cx + k * (px - cx), cy + k * (py - cy)
        if (px, py) != (cx, cy) and 0 <= px <= 10 and 0 <= py <= 10 and 0 <= ix <= 10 and 0 <= iy <= 10:
            break
    return {"prompt": "P(%d, %d) is enlarged by scale factor %d from the centre C(%d, %d). Plot the image of P." % (px, py, k, cx, cy),
            "component": "coordinate_grid", "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[cx, cy, "C"], [px, py, "P"]]},
            "answer": "(%d,%d)" % (ix, iy), "answer_type": "coord",
            "solution": ["From C to P is (%d, %d)." % (px - cx, py - cy), "Multiply by %d: (%d, %d), so the image is (%d, %d)." % (k, k * (px - cx), k * (py - cy), ix, iy)]}


@_more("Y8.8.j", 9)
def _(d):
    n = _by(d, 2, 2, pick([3, 4]))                    # stretch: scale factor 1/3 or 1/4
    px, py = random.randint(1, 10 // n) * n, random.randint(1, 10 // n) * n
    if d == 0:                                    # easy: small even coordinates
        px, py = random.randint(1, 3) * 2, random.randint(1, 3) * 2
    return {"prompt": "P(%d, %d) is enlarged by scale factor 1/%d from the origin. Plot the image of P." % (px, py, n),
            "component": "coordinate_grid", "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[px, py, "P"]]},
            "answer": "(%d,%d)" % (px // n, py // n), "answer_type": "coord",
            "solution": ["Scale factor 1/%d divides the distance from the origin by %d." % (n, n), "(%d, %d)." % (px // n, py // n)]}


@_more("Y8.8.j", 9)
def _(d):
    k = random.randint(_by(d, 2, 2, 3), _by(d, 2, 4, 4))
    ax, ay = random.randint(1, 3), random.randint(1, 3)
    return _cg("A(%d, %d) maps to A'(%d, %d) under an enlargement with centre the origin. What is the scale factor?" % (ax, ay, k * ax, k * ay),
               {"xmin": 0, "xmax": 12, "ymin": 0, "ymax": 12, "points": [[ax, ay, "A"], [k * ax, k * ay, "A'"]]}, k,
               ["%d ÷ %d = %d and %d ÷ %d = %d." % (k * ax, ax, k, k * ay, ay, k), "Scale factor %d." % k], placeholder="scale factor")


@_more("Y8.8.j", 9)
def _(d):
    a, b, c = pick([(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 6, 8), (2, 5, 6)])
    # easy: whole-number factors; stretch: quarters and factors below 1
    k = pick(_by(d, ["2", "3"], ["1.5", "2.5", "0.5"], ["1.25", "0.75", "3.5", "0.25", "2.5"]))
    side = pick([a, b, c])
    return _num("A triangle has sides %d cm, %d cm and %d cm. It is enlarged by scale factor %s. How long does the %d cm side become, in cm?"
                % (a, b, c, k, side), Decimal(k) * side, ["%d × %s = %s cm." % (side, k, _ds(Decimal(k) * side))], "cm")


@_more("Y8.8.j", 9)
def _(d):
    img = random.randint(2, _by(d, 6, 12, 25))
    k, word = pick(_by(d, [(2, "1/2")], [(2, "1/2"), (3, "1/3"), (4, "1/4")], [(3, "1/3"), (4, "1/4"), (5, "1/5"), (10, "1/10")]))
    return _int("A shape is enlarged by scale factor %s. A side of the image is %d cm. How long was that side on the original shape, in cm?"
                % (word, img), img * k, ["Scale factor %s makes lengths %d times smaller." % (word, k), "So the original is %d × %d = %d cm." % (img, k, img * k)], "cm")


@_more("Y8.8.j", 9)
def _(d):
    b, h = random.randint(2, 4), random.randint(2, 4)
    k = pick(_by(d, [2], [2, 3], [3, 4]))
    x0, y0 = random.randint(0, 2), random.randint(0, 2)
    pts = [[x0, y0], [x0 + b, y0], [x0, y0 + h]]
    if d == 2:                                    # stretch: area grows by k² — an extra step
        while (b * h * k * k) % 2:
            b += 1
            pts = [[x0, y0], [x0 + b, y0], [x0, y0 + h]]
        area = b * h * k * k // 2
        return _cg("The right-angled triangle on the grid is enlarged by scale factor %d. What will the area of the image be, in squares?" % k,
                   {"xmin": 0, "xmax": 8, "ymin": 0, "ymax": 8, "polygon": pts}, area,
                   ["The image is %d by %d squares." % (b * k, h * k), "Area = ½ × %d × %d = %d squares." % (b * k, h * k, area)], placeholder="squares")
    return _cg("The right-angled triangle on the grid is enlarged by scale factor %d. How long will the image's horizontal side be, in squares?" % k,
               {"xmin": 0, "xmax": 8, "ymin": 0, "ymax": 8, "polygon": pts}, b * k,
               ["The horizontal side is %d squares." % b, "%d × %d = %d squares." % (b, k, b * k)], placeholder="squares")


@_more("Y8.8.k", 11)
def _(d):
    # easy: whole-number scale factors; stretch: 1.25, 3.5 … and longer sides
    a, k = random.randint(2, _by(d, 6, 8, 12)) * 2, pick(_by(d, ["2", "3", "0.5"], ["1.5", "2.5", "0.5"], ["1.5", "2.5", "1.25", "3.5", "0.5"]))
    other = random.randint(3, _by(d, 8, 12, 20)) * 2
    if k == "0.5":
        return _num("Two triangles are similar. A side of %d cm in the large triangle matches a side of %d cm in the small one. "
                    "Another side of the large triangle is %d cm. How long is the matching side in the small triangle, in cm?"
                    % (a, a // 2, other), other // 2,
                    ["Scale factor = %d ÷ %d = 0.5." % (a // 2, a), "%d × 0.5 = %d cm." % (other, other // 2)], "cm")
    return _num("Two triangles are similar. A side of %d cm in the small triangle matches a side of %s cm in the large one. Another "
                "side of the small triangle is %d cm. How long is the matching side in the large triangle, in cm?"
                % (a, _ds(Decimal(k) * a), other), Decimal(k) * other,
                ["Scale factor = %s ÷ %d = %s." % (_ds(Decimal(k) * a), a, k), "%d × %s = %s cm." % (other, k, _ds(Decimal(k) * other))], "cm")


@_more("Y8.8.k", 11)
def _(d):
    if d == 2:                                    # stretch: spot the condition from the measurements given
        p, q, r = random.sample(range(4, 13), 3)
        while 2 * max(p, q, r) >= p + q + r:          # a real triangle
            p, q, r = random.sample(range(4, 13), 3)
        x, y = random.randint(30, 80), random.randint(30, 70)
        case, ans = pick([("AB = DE = %d cm, BC = EF = %d cm and CA = FD = %d cm" % (p, q, r), "SSS"),
                          ("AB = DE = %d cm, angle B = angle E = %d° and BC = EF = %d cm" % (p, x, q), "SAS"),
                          ("angle A = angle D = %d°, AB = DE = %d cm and angle B = angle E = %d°" % (x, p, y), "ASA"),
                          ("angle C = angle F = 90°, AB = DE = %d cm and BC = EF = %d cm" % (max(p, q) + 1, min(p, q)), "RHS")])
        return _wq("Triangles ABC and DEF have %s. Which condition shows they are congruent? Type SSS, SAS, ASA or RHS." % case, ans,
                   ["S = side, A = angle, R = right angle, H = hypotenuse; an angle between two sides is 'included'.", "This is %s." % ans],
                   "SSS, SAS, ASA or RHS")
    case, ans = pick([("all three pairs of matching sides are equal", "SSS"),
                      ("two pairs of sides are equal and the angles between them are equal", "SAS"),
                      ("two pairs of angles are equal and the sides between them are equal", "ASA"),
                      ("both have a right angle, equal hypotenuses and one other pair of equal sides", "RHS")])
    return _wq("Two triangles are congruent because %s. Which condition is this? Type SSS, SAS, ASA or RHS." % case, ans,
               ["S = side, A = angle, R = right angle, H = hypotenuse.", "This is %s." % ans], "SSS, SAS, ASA or RHS")


@_more("Y8.8.k", 11)
def _(d):
    a, b = random.randint(2, 6), random.randint(3, 9)
    if a == b:
        b += 1
    # easy: small whole scale factors and an obvious mismatch; stretch: scale factors like 1.5 and a mismatch of 1
    k = Decimal(pick(_by(d, ["2", "3"], ["2", "3", "4"], ["1.5", "2.5", "3", "4"])))
    if k != int(k):
        a, b = 2 * a, 2 * b
    sim = random.random() < 0.5
    c, e = (int(a * k), int(b * k)) if sim else (int(a * k), int(b * k) + pick(_by(d, [2, 3], [-1, 1, 2], [-1, 1])))
    return _yn("Rectangle A is %d cm by %d cm. Rectangle B is %d cm by %d cm. Are they similar?" % (a, b, c, e), sim,
               ["%d ÷ %d = %s and %d ÷ %d = %s." % (c, a, _ds(k), e, b, _ds(_round(Decimal(e) / b, 2))),
                "%s" % ("Both sides are multiplied by %s, so yes." % _ds(k) if sim else "The sides are not multiplied by the same number, so no.")])


@_more("Y8.8.k", 11)
def _(d):
    stick, sh = pick(_by(d, [(2, 3), (1, 2), (2, 5), (3, 4)], [(2, 3), (1, 2), (2, 5), (3, 4), (1.5, 2)],
                         [(2, 3), (1.5, 2), (1.2, 1.6), (2, 5), (1.8, 2.4)]))
    k = Decimal(pick(_by(d, ["2", "3", "4"], ["3", "4", "5", "6", "7", "8"], ["2.5", "3.5", "4.5", "6", "7.5"])))
    tree = Decimal(str(stick)) * k
    return _num("A %s m stick casts a shadow %s m long. At the same time a tree casts a shadow %s m long. How tall is the tree, in m? "
                "(The triangles are similar.)" % (_ds(Decimal(str(stick))), _ds(Decimal(str(sh))), _ds(Decimal(str(sh)) * k)), tree,
                ["The tree's shadow is %s times as long." % _ds(k), "%s × %s = %s m." % (_ds(Decimal(str(stick))), _ds(k), _ds(tree))], "m")


@_more("Y8.8.k", 11)
def _(d):
    s = [random.randint(_by(d, 2, 3, 3), _by(d, 6, 9, 12)) for _ in range(3)]
    k = random.randint(2, _by(d, 3, 4, 6))
    i = random.randrange(3)
    rows = [["ABC"] + [str(x) for x in s], ["PQR"] + [str(x * k) for x in s]]
    if d == 2 and random.random() < 0.5:               # stretch: the missing side is in the smaller triangle
        return _dt("Triangle ABC is similar to triangle PQR (AB matches PQ, BC matches QR, CA matches RP). Lengths are in cm. What goes in "
                   "the empty cell?", ["Triangle", "AB / PQ", "BC / QR", "CA / RP"], rows, s[i],
                   ["Scale factor = %d ÷ %d = %d." % (s[(i + 1) % 3] * k, s[(i + 1) % 3], k), "%d ÷ %d = %d cm." % (s[i] * k, k, s[i])],
                   missing=(0, i + 1))
    return _dt("Triangle ABC is similar to triangle PQR (AB matches PQ, BC matches QR, CA matches RP). Lengths are in cm. What goes in "
               "the empty cell?", ["Triangle", "AB / PQ", "BC / QR", "CA / RP"], rows, s[i] * k,
               ["Scale factor = %d ÷ %d = %d." % (s[(i + 1) % 3] * k, s[(i + 1) % 3], k), "%d × %d = %d cm." % (s[i], k, s[i] * k)],
               missing=(1, i + 1))


_TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20)]


@_more("Y8.8.l", 11)
def _(d):
    h, half, side = pick(_by(d, [(4, 3, 5), (8, 6, 10), (12, 5, 13)],
                             [(12, 5, 13), (4, 3, 5), (8, 6, 10), (15, 8, 17), (12, 9, 15), (24, 7, 25)],
                             [(15, 8, 17), (12, 9, 15), (24, 7, 25), (12, 16, 20), (5, 12, 13)]))
    if d == 2:                                    # stretch: height first, then the area
        return _int("An isosceles triangle has two sides of %d cm and a base of %d cm. What is its area, in cm²?" % (side, 2 * half), h * half,
                    ["The height cuts the base in half: %d cm. h² = %d² − %d² = %d, so h = %d cm." % (half, side, half, h * h, h),
                     "Area = ½ × %d × %d = %d cm²." % (2 * half, h, h * half)], "cm²")
    return _int("An isosceles triangle has two sides of %d cm and a base of %d cm. What is its perpendicular height, in cm?" % (side, 2 * half), h,
                ["The height cuts the base in half: %d cm." % half, "h² = %d² − %d² = %d, so h = %d cm." % (side, half, h * h, h)], "cm")


@_more("Y8.8.l", 11)
def _(d):
    a = random.randint(2, _by(d, 6, 12, 20))
    if d == 2:                                    # stretch: the inverse — side from the diagonal
        v = _round((Decimal(a * a) / 2).sqrt(), 1)
        return _num("A square has a diagonal of %d cm. How long is each side, correct to 1 decimal place, in cm?" % a, v,
                    ["s² + s² = %d², so 2s² = %d and s² = %s." % (a, a * a, _ds(Decimal(a * a) / 2)),
                     "s = √%s = %s cm." % (_ds(Decimal(a * a) / 2), _ds(v))], "cm", tol=0.05)
    v = _round(Decimal(2 * a * a).sqrt(), 1)
    return _num("A square has sides of %d cm. How long is its diagonal, correct to 1 decimal place, in cm?" % a, v,
                ["d² = %d² + %d² = %d." % (a, a, 2 * a * a), "d = √%d = %s cm." % (2 * a * a, _ds(v))], "cm", tol=0.05)


@_more("Y8.8.l", 11)
def _(d):
    a, b, c = pick(_by(d, [(3, 4, 5), (4, 3, 5)], [(3, 4, 5), (6, 8, 10), (8, 6, 10), (4, 3, 5), (5, 12, 13)],
                       [(6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13)]))
    x0, y0 = 0, 0
    span = max(a, b) + 1
    return _cg("The right-angled triangle is drawn on a grid of 1 cm squares. How long is the sloping side (the hypotenuse), in cm?",
               {"xmin": 0, "xmax": span, "ymin": 0, "ymax": span, "polygon": [[x0, y0], [x0 + a, y0], [x0, y0 + b]]}, c,
               ["The two shorter sides are %d cm and %d cm." % (a, b), "%d² + %d² = %d = %d², so %d cm." % (a, b, c * c, c, c)], placeholder="cm")


@_more("Y8.8.l", 11)
def _(d):
    a, b, c = pick(_by(d, _TRIP[:2], _TRIP, _TRIP[3:]))
    return _int("A right-angled triangle has shorter sides %d cm and %d cm. What is its perimeter, in cm?" % (a, b), a + b + c,
                ["Hypotenuse: √(%d + %d) = %d cm." % (a * a, b * b, c), "%d + %d + %d = %d cm." % (a, b, c, a + b + c)], "cm")


@_more("Y8.8.l", 11)
def _(d):
    a, b, c = pick(_by(d, _TRIP[:2], _TRIP, _TRIP[2:]))
    if d == 2:                                    # stretch: the inverse — find the rise
        return _int("A ramp's sloping surface is %d m long and covers a horizontal distance of %d m. How high does the ramp rise, in m?"
                    % (c, max(a, b)), min(a, b),
                    ["rise² = %d² − %d² = %d." % (c, max(a, b), min(a, b) ** 2), "rise = %d m." % min(a, b)], "m")
    return _int("A ramp rises %d m over a horizontal distance of %d m. How long is the sloping surface of the ramp, in m?" % (min(a, b), max(a, b)), c,
                ["√(%d² + %d²) = √%d." % (min(a, b), max(a, b), c * c), "= %d m." % c], "m")


@_more("Y8.8.l", 11)
def _(d):
    k = random.randint(_by(d, 1, 2, 2), _by(d, 3, 6, 6))
    w, h = 4 * k * 4, 3 * k * 4
    if d == 2:                                    # stretch: the inverse — height from diagonal and width
        return _int("A TV screen has a %d cm diagonal and is %d cm wide. How tall is it, in cm?" % (5 * k * 4, w), h,
                    ["h² = %d² − %d² = %d." % (5 * k * 4, w, h * h), "h = √%d = %d cm." % (h * h, h)], "cm")
    return _int("A TV screen is %d cm wide and %d cm tall. How long is its diagonal, in cm?" % (w, h), 5 * k * 4,
                ["%d² + %d² = %d." % (w, h, (5 * k * 4) ** 2), "√%d = %d cm." % ((5 * k * 4) ** 2, 5 * k * 4)], "cm")


@_more("Y8.8.m", 9)
def _(d):
    while True:
        s = sorted(random.sample(range(3, 16), 3))
        if s[0] + s[1] > s[2]:
            break
    if random.random() < 0.3:
        a, b, c = pick(_TRIP)
        s = [a, b, c]
    lhs, rhs = s[0] ** 2 + s[1] ** 2, s[2] ** 2
    kind = "right" if lhs == rhs else ("acute" if lhs > rhs else "obtuse")
    return _wq("A triangle has sides %d, %d and %d. Is it acute, right-angled or obtuse? Type acute, right or obtuse." % tuple(s), kind,
               ["%d² + %d² = %d and %d² = %d." % (s[0], s[1], lhs, s[2], rhs),
                "%s" % {"right": "They are equal, so right-angled.", "acute": "a² + b² is bigger, so acute.", "obtuse": "a² + b² is smaller, so obtuse."}[kind]],
               "acute, right or obtuse")


@_more("Y8.8.m", 9)
def _(d):
    a, b, c = pick(_TRIP + [(20, 21, 29), (9, 40, 41), (12, 35, 37)])
    return _int("Two sides of a triangle are %d cm and %d cm. How long must the longest side be for the triangle to be right-angled, in cm?" % (a, b), c,
                ["Right-angled when a² + b² = c².", "%d + %d = %d = %d², so %d cm." % (a * a, b * b, c * c, c, c)], "cm")


@_more("Y8.8.m", 9)
def _(d):
    rows, n = [], 0
    for _ in range(4):
        if random.random() < 0.5:
            a, b, c = pick(_TRIP)
            n += 1
        else:
            while True:
                a, b, c = sorted(random.sample(range(3, 20), 3))
                if a + b > c and a * a + b * b != c * c:
                    break
        rows.append([str(a), str(b), str(c)])
    return _dt("The table gives the sides of four triangles. How many of them are right-angled?", ["a", "b", "c (longest)"], rows, n,
               ["Check a² + b² = c² for each row.", "%s right-angled." % ("1 is" if n == 1 else "%d are" % n)])


@_more("Y8.8.m", 9)
def _(d):
    while True:
        if random.random() < 0.5:                 # a right angle at P, legs (a, b) and (−b, a)·k
            px, py, a, b, k = random.randint(0, 6), random.randint(0, 6), random.randint(1, 3), random.randint(0, 2), random.randint(1, 2)
            pts = [[px, py], [px + a, py + b], [px - b * k, py + a * k]]
        else:
            pts = [[random.randint(0, 6), random.randint(0, 6)] for _ in range(3)]
        if all(0 <= c <= 6 for p in pts for c in p) and _shoelace(pts) > 1:
            break
    sq = sorted(((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) for p, q in ((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[0])))
    right = sq[0] + sq[1] == sq[2]
    return _cg("The triangle has vertices at (%d, %d), (%d, %d) and (%d, %d). Is it right-angled? Type yes or no." % tuple(pts[0] + pts[1] + pts[2]),
               {"xmin": 0, "xmax": 6, "ymin": 0, "ymax": 6, "polygon": pts}, "yes" if right else "no",
               ["The squared side lengths are %d, %d and %d." % tuple(sq), "%d + %d %s %d, so %s." % (sq[0], sq[1], "=" if right else "≠", sq[2], "yes" if right else "no")],
               atype="str", placeholder="yes or no")


@_more("Y8.8.n", 11)
def _(d):
    want = random.random() < 0.5
    while True:
        s = sorted(random.sample(range(2, _by(d, 12, 15, 25)), 3))
        gap = s[0] + s[1] - s[2]
        # easy: a clear yes or no; stretch: within 1 cm, or exactly equal (a flat 'triangle', so no)
        if (s[0] + s[1] > s[2]) == want and _by(d, abs(gap) >= 3, gap != 0, abs(gap) <= 1):
            break
    ok = want
    return _yn("Can you construct a triangle with sides %d cm, %d cm and %d cm?" % tuple(s), ok,
               ["The two shorter sides must add up to more than the longest.",
                "%d + %d = %d, which is %s %d." % (s[0], s[1], s[0] + s[1], "more than" if ok else ("less than" if gap else "only equal to"), s[2])])


@_more("Y8.8.n", 11)
def _(d):
    r = random.randint(2, 9)
    desc, ans = pick(_by(d, [("the same distance from two points A and B", "perpendicular bisector"),
                             ("exactly %d cm from a fixed point" % r, "circle")],
                         [("the same distance from two points A and B", "perpendicular bisector"),
                          ("the same distance from two lines that meet at a point", "angle bisector"),
                          ("exactly 3 cm from a fixed point", "circle")],
                         # stretch: the same loci, described less directly
                         [("equidistant from the two ends of a fence AB", "perpendicular bisector"),
                          ("equidistant from the two edges of a V-shaped corner", "angle bisector"),
                          ("where a goat tied to a post by a %d m rope can just reach" % r, "circle"),
                          ("equidistant from the corners P and Q of a field", "perpendicular bisector")]))
    return _wq("The locus of points %s is which shape or line? Type its name." % desc, ans,
               ["That locus is %s %s." % ("a" if ans != "angle bisector" else "an", ans)], "type the name")


@_more("Y8.8.n", 11)
def _(d):
    start, word = pick([(60, "an equilateral triangle"), (90, "a perpendicular")])
    times = pick(_by(d, [1], [1, 2], [2, 3]))
    v = start / 2 ** times
    return _num("You construct a %d° angle using %s, then bisect it%s. What angle do you end up with, in degrees?"
                % (start, word, {1: "", 2: ", then bisect one of the halves",
                                 3: ", then bisect one of the halves, then bisect one of those"}[times]), Decimal(str(v)),
                ["Each bisection halves the angle.", "%d ÷ %d = %s°." % (start, 2 ** times, _ds(Decimal(str(v))))], "°")


@_more("Y8.8.n", 11)
def _(d):
    if d == 2:                                    # stretch: use the fact — read off the shortest distance
        dists = random.sample(range(3, 15), 3)
        short = min(dists)
        return _int("Point P is joined to a straight line by three straight paths of %d m, %d m and %d m. One of them meets the line at 90°. "
                    "Which length must that one be, in m?" % tuple(dists), short,
                    ["The perpendicular is the shortest distance from a point to a line.", "So it is the shortest path: %d m." % short], "m")
    return _wq("The shortest distance from a point to a straight line is measured along a line that meets it at 90°. What is that line called? "
               "(type one word)", "perpendicular", ["It is the perpendicular from the point to the line."], "one word")


@_more("Y8.8.n", 11)
def _(d):
    while True:
        ax, ay, bx, by = [random.randint(0, 10) for _ in range(4)]
        # easy: AB is horizontal or vertical; stretch: a long slanted AB
        shape = _by(d, ax == bx or ay == by, True, ax != bx and ay != by and abs(ax - bx) + abs(ay - by) >= 8)
        if (ax + bx) % 2 == 0 and (ay + by) % 2 == 0 and (ax, ay) != (bx, by) and abs(ax - bx) + abs(ay - by) >= 4 and shape:
            break
    mx, my = (ax + bx) // 2, (ay + by) // 2
    return {"prompt": "The perpendicular bisector of AB crosses AB at its midpoint. Plot that point.",
            "component": "coordinate_grid", "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[ax, ay, "A"], [bx, by, "B"]]},
            "answer": "(%d,%d)" % (mx, my), "answer_type": "coord",
            "solution": ["Midpoint = ((%d + %d) ÷ 2, (%d + %d) ÷ 2)." % (ax, bx, ay, by), "= (%d, %d)." % (mx, my)]}


@_more("Y8.8.o", 11)
def _(d):
    dirs = {(0, 1): "000", (1, 1): "045", (1, 0): "090", (1, -1): "135", (0, -1): "180", (-1, -1): "225", (-1, 0): "270", (-1, 1): "315"}
    items = list(dirs.items())
    (ux, uy), brg = pick(items if d else items[::2])          # easy: due N, E, S or W only
    k = random.randint(2, 4)
    ax, ay = 5, 5
    bx, by = ax + k * ux, ay + k * uy
    if d == 2:                                    # stretch: the bearing of A from B (back bearing)
        back = "%03d" % ((int(brg) + 180) % 360)
        return _cg("North is straight up the grid. What is the three-figure bearing of A from B?",
                   {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[ax, ay, "A"], [bx, by, "B"]]}, back,
                   ["Stand at B, face north and turn clockwise until you face A.",
                    "B from A is %s°, so A from B is 180° different: %s°." % (brg, back)], atype="str", placeholder="e.g. 045")
    return _cg("North is straight up the grid. What is the three-figure bearing of B from A?",
               {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[ax, ay, "A"], [bx, by, "B"]]}, brg,
               ["Stand at A, face north and turn clockwise until you face B.", "That is %s°." % brg], atype="str", placeholder="e.g. 045")


@_more("Y8.8.o", 11)
def _(d):
    b = random.randint(1, 35) * 10
    t = pick([45, 90, 120, 135, 30, 60])
    if d == 0:                                    # easy: no passing through north
        t = pick([30, 60, 90])
        b = random.randint(t // 10 + 1, 35) * 10
    elif d == 2:                                  # stretch: awkward sizes that pass through north
        t = random.randint(25, 170)
        b = random.randint(5, t - 1)
    new = (b - t) % 360
    return _wq("A ship is sailing on a bearing of %03d°. It turns %d° anticlockwise. What bearing is it on now? (three figures)" % (b, t), "%03d" % new,
               ["Anticlockwise takes the bearing down: %d − %d = %d." % (b, t, b - t), "%s" % ("Add 360: %03d°." % new if b - t < 0 else "%03d°." % new)], "e.g. 045")


@_more("Y8.8.o", 11)
def _(d):
    a, b = sorted(random.sample(range(1, 36), 2))
    a, b = a * 10, b * 10
    if d == 0:                                    # easy: the gap is under 180°
        a, b = sorted(random.sample(range(1, 18), 2))
        a, b = a * 10, b * 10
    elif d == 2:                                  # stretch: any whole-degree bearings
        a, b = sorted(random.sample(range(1, 360), 2))
    ang = b - a if b - a <= 180 else 360 - (b - a)
    return _int("From a lighthouse, ship P is on a bearing of %03d° and ship Q is on a bearing of %03d°. What is the angle PLQ at the lighthouse "
                "(the smaller angle between the two directions)?" % (a, b), ang,
                ["%d − %d = %d°." % (b, a, b - a), "%s" % ("That is the smaller angle." if b - a <= 180 else "The smaller angle is 360 − %d = %d°." % (b - a, ang))], "°")


@_more("Y8.8.o", 11)
def _(d):
    t = random.randint(5, 85)
    opts = [("north", "east", t), ("north", "west", 360 - t), ("south", "east", 180 - t), ("south", "west", 180 + t)]
    # easy: measured from north only; stretch: from south or towards the west
    base, side, brg = pick(_by(d, opts[:1], opts, opts[1:]))
    return _wq("From A, the town B is %d° %s of %s (measure from %s, turning towards %s). What is the bearing of B from A? (three figures)"
               % (t, side, base, base, side), "%03d" % brg,
               ["Bearings are measured clockwise from north.", "The bearing is %03d°." % brg], "e.g. 045")


# ================================================================== 8.9 ======
@_more("Y8.9.c", 11)
def _(d):
    d1, d2 = random.randint(*_by(d, (2, 10), (3, 15), (12, 30))), random.randint(*_by(d, (2, 8), (2, 12), (9, 25)))
    while (d1 * d2) % 2:
        d2 += 1
    return _int("A kite has diagonals of %d cm and %d cm. What is its area, in cm²? (Area = ½ × d₁ × d₂.)" % (d1, d2), d1 * d2 // 2,
                ["½ × %d × %d = %d cm²." % (d1, d2, d1 * d2 // 2)], "cm²")


@_more("Y8.9.c", 11)
def _(d):
    w, h, th = (random.randint(*_by(d, (2, 6), (4, 12), (7, 15))), random.randint(*_by(d, (2, 5), (3, 8), (4, 12))),
                random.randint(*_by(d, (2, 4), (2, 6), (3, 9))))
    while (w * th) % 2:
        th += 1
    return _int("The end of a shed is a rectangle %d m wide and %d m tall, with a triangle on top that is %d m high. What is the area of "
                "the end of the shed, in m²?" % (w, h, th), w * h + w * th // 2,
                ["Rectangle: %d × %d = %d m²." % (w, h, w * h), "Triangle: ½ × %d × %d = %d m²." % (w, th, w * th // 2),
                 "Total: %d m²." % (w * h + w * th // 2)], "m²")


@_more("Y8.9.c", 11)
def _(d):
    kind = _by(d, random.randrange(2), random.randrange(3), random.randrange(1, 3))   # easy: no trapezium; hard: no triangle
    if kind == 0:
        x0, y0, b, h = random.randint(0, 2), random.randint(0, 2), random.randint(3, 6), random.randint(2, 6)
        apex = random.randint(x0, x0 + b)
        pts, name = [[x0, y0], [x0 + b, y0], [apex, y0 + h]], "triangle"
    elif kind == 1:
        x0, y0, b, h, s = random.randint(0, 2), random.randint(0, 2), random.randint(3, 5), random.randint(2, 5), random.randint(1, 3)
        pts, name = [[x0, y0], [x0 + b, y0], [x0 + b + s, y0 + h], [x0 + s, y0 + h]], "parallelogram"
    else:
        x0, y0, a, b, h = random.randint(0, 1), random.randint(0, 2), random.randint(2, 4), random.randint(5, 8), random.randint(2, 5)
        off = random.randint(0, b - a)
        pts, name = [[x0, y0], [x0 + b, y0], [x0 + off + a, y0 + h], [x0 + off, y0 + h]], "trapezium"
    area = _shoelace(pts)
    return _cg("The %s is drawn on a grid of 1 cm squares. What is its area, in cm²?" % name, {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 8, "polygon": pts},
               _ds(_dec(area)), ["Read the base and the perpendicular height from the grid.", "Area = %s cm²." % _ds(_dec(area))], atype="num", placeholder="cm²")


@_more("Y8.9.c", 11)
def _(d):
    a, b, h = (random.randint(*_by(d, (2, 6), (3, 10), (8, 20))), random.randint(*_by(d, (4, 10), (4, 14), (12, 30))),
               random.randint(*_by(d, (2, 6), (2, 10), (6, 18))))
    while ((a + b) * h) % 2:
        h += 1
    area = (a + b) * h // 2
    return _int("A trapezium has area %d cm² and parallel sides of %d cm and %d cm. What is its height, in cm?" % (area, a, b), h,
                ["½ × (%d + %d) × h = %d." % (a, b, area), "%d × h = %d, so h = %d cm." % (a + b, 2 * area, h)], "cm")


@_more("Y8.9.c", 11)
def _(d):
    a, b, h = (random.randint(*_by(d, (2, 6), (4, 12), (8, 20))), random.randint(*_by(d, (4, 10), (6, 16), (14, 30))),
               random.randint(*_by(d, (2, 6), (2, 8), (5, 15))))
    while ((a + b) * h) % 2:
        h += 1
    price = random.randint(*_by(d, (2, 5), (2, 9), (6, 15)))
    area = (a + b) * h // 2
    return _int("A lawn is a trapezium with parallel sides %d m and %d m, %d m apart. Turf costs £%d per m². How much does it cost to turf "
                "the lawn, in pounds?" % (a, b, h, price), area * price,
                ["Area = ½ × (%d + %d) × %d = %d m²." % (a, b, h, area), "%d × £%d = £%d." % (area, price, area * price)], "£")


@_more("Y8.9.d", 8)
def _(d):
    dm = _by(d, random.randint(1, 5) * 2, random.randint(2, 20) * 2, random.randint(15, 60))   # hard: odd diameters too
    v = Decimal("3.14") * dm / 2 + dm
    return _num("Take π as 3.14. A semicircle has a diameter of %d cm. What is its perimeter (curved edge plus diameter), in cm?" % dm, v,
                ["Curved edge: ½ × 3.14 × %d = %s cm." % (dm, _ds(Decimal("3.14") * dm / 2)), "Add the diameter: %s + %d = %s cm." % (_ds(Decimal("3.14") * dm / 2), dm, _ds(v))], "cm")


@_more("Y8.9.d", 8)
def _(d):
    r = random.randint(*_by(d, (2, 6), (2, 12), (11, 25)))
    return {"prompt": "A circle has an area of %dπ cm². What is its radius, in cm?" % (r * r), "component": "circle",
            "spec": {"show": "radius", "label": "r = ?"}, "answer": r, "answer_type": "int",
            "solution": ["πr² = %dπ, so r² = %d." % (r * r, r * r), "r = %d cm." % r]}


@_more("Y8.9.d", 8)
def _(d):
    dia = pick(_by(d, ["0.5"], ["0.5", "0.6", "0.7", "0.4"], ["0.45", "0.65", "0.75", "0.8", "1.2"]))
    turns = _by(d, random.randint(1, 5) * 100, random.randint(1, 10) * 100, random.randint(3, 19) * 50)
    dist = Decimal("3.14") * Decimal(dia) * turns
    return _int("Take π as 3.14. A wheel has a diameter of %s m. How many full turns does it make to travel %s m?" % (dia, _ds(dist)), turns,
                ["One turn = 3.14 × %s = %s m." % (dia, _ds(Decimal("3.14") * Decimal(dia))), "%s ÷ %s = %d turns." % (_ds(dist), _ds(Decimal("3.14") * Decimal(dia)), turns)], "turns")


@_more("Y8.9.d", 8)
def _(d):
    r = _by(d, random.randint(1, 5) * 2, random.randint(2, 10) * 2, random.randint(9, 30))   # hard: odd radii too
    arc = Decimal("3.14") * 2 * r / 4
    return _num("Take π as 3.14. A quarter circle has radius %d cm. What is its perimeter (the curved edge plus two radii), in cm?" % r, arc + 2 * r,
                ["Curved edge: ¼ × 2 × 3.14 × %d = %s cm." % (r, _ds(arc)), "%s + %d + %d = %s cm." % (_ds(arc), r, r, _ds(arc + 2 * r))], "cm")


@_more("Y8.9.d", 8)
def _(d):
    R = random.randint(*_by(d, (3, 6), (4, 12), (10, 20)))
    r = random.randint(_by(d, 1, 1, 4), R - 1)
    if d == 2:                                        # stretch: given the diameters, so halve first
        return _int("A ring is the shape between two circles with the same centre, of diameter %d cm and %d cm. Its area is kπ cm². "
                    "What is k?" % (2 * R, 2 * r), R * R - r * r,
                    ["The radii are %d cm and %d cm." % (R, r), "Big circle: %dπ. Small circle: %dπ." % (R * R, r * r),
                     "%d − %d = %d." % (R * R, r * r, R * R - r * r)])
    return _int("A ring is the shape between two circles with the same centre, of radius %d cm and %d cm. Its area is kπ cm². What is k?" % (R, r), R * R - r * r,
                ["Big circle: %dπ. Small circle: %dπ." % (R * R, r * r), "%d − %d = %d." % (R * R, r * r, R * R - r * r)])


@_more("Y8.9.d", 8)
def _(d):
    r = random.randint(*_by(d, (2, 8), (2, 15), (8, 30)))
    if d == 2:                                        # stretch: radius first, then the area
        return {"prompt": "A circle has a circumference of %dπ cm. Its area is kπ cm². What is k?" % (2 * r), "component": "circle",
                "spec": {"show": "circumference", "label": "C = %dπ cm" % (2 * r)}, "answer": r * r, "answer_type": "int",
                "solution": ["C = 2πr = %dπ, so r = %d cm." % (2 * r, r), "A = πr² = %dπ, so k = %d." % (r * r, r * r)]}
    return {"prompt": "A circle has a circumference of %dπ cm. What is its radius, in cm?" % (2 * r), "component": "circle",
            "spec": {"show": "circumference", "label": "C = %dπ cm" % (2 * r)}, "answer": r, "answer_type": "int",
            "solution": ["C = 2πr = %dπ." % (2 * r), "r = %d ÷ 2 = %d cm." % (2 * r, r)]}


@_more("Y8.9.e", 11)
def _(d):
    while True:
        W, H = random.randint(*_by(d, (3, 5), (4, 8), (7, 9))), random.randint(*_by(d, (3, 5), (4, 7), (6, 7)))
        w, h = random.randint(1, W - 2), random.randint(1, H - 2)
        x0, y0 = random.randint(0, 9 - W), random.randint(0, 7 - H)
        if 0 <= x0 and 0 <= y0:
            break
    pts = [[x0, y0], [x0 + W, y0], [x0 + W, y0 + H - h], [x0 + W - w, y0 + H - h], [x0 + W - w, y0 + H], [x0, y0 + H]]
    area = W * H - w * h
    if random.random() < _by(d, 0.75, 0.5, 0.5):
        return _cg("The L-shape is drawn on a grid of 1 cm squares. What is its area, in cm²?", {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 8, "polygon": pts},
                   area, ["Whole rectangle %d × %d = %d, minus the corner %d × %d = %d." % (W, H, W * H, w, h, w * h), "%d cm²." % area], placeholder="cm²")
    return _cg("The L-shape is drawn on a grid of 1 cm squares. What is its perimeter, in cm?", {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 8, "polygon": pts},
               2 * (W + H), ["Add up all six sides.", "%d cm (the same as the %d by %d rectangle)." % (2 * (W + H), W, H)], placeholder="cm")


@_more("Y8.9.e", 11)
def _(d):
    W, H = random.randint(*_by(d, (8, 12), (10, 20), (18, 40))), random.randint(*_by(d, (5, 9), (6, 14), (12, 30)))
    w, h = random.randint(2, W - 6), random.randint(2, H - 2)
    return _int("A U-shape is made by cutting %s cm wide, %d cm deep rectangle out of the middle of the top edge of %s cm by %d cm "
                "rectangle. What is the perimeter of the U-shape, in cm?" % (_an(w), h, _an(W), H), 2 * (W + H) + 2 * h,
                ["The outside edges still add up to 2 × (%d + %d) = %d cm." % (W, H, 2 * (W + H)),
                 "The two inside edges add 2 × %d = %d cm: %d cm in total." % (h, 2 * h, 2 * (W + H) + 2 * h)], "cm")


@_more("Y8.9.e", 11)
def _(d):
    L, W, p = random.randint(*_by(d, (4, 10), (6, 20), (15, 40))), random.randint(*_by(d, (3, 8), (4, 12), (10, 25))), random.randint(*_by(d, (1, 1), (1, 3), (2, 5)))
    return _int("A rectangular lawn %d m by %d m has a path %d m wide all the way round the outside. What is the area of the path, in m²?" % (L, W, p),
                (L + 2 * p) * (W + 2 * p) - L * W,
                ["Outer rectangle: %d × %d = %d m²." % (L + 2 * p, W + 2 * p, (L + 2 * p) * (W + 2 * p)), "Minus the lawn %d m²: %d m²." % (L * W, (L + 2 * p) * (W + 2 * p) - L * W)], "m²")


@_more("Y8.9.e", 11)
def _(d):
    W, H, w, h = (random.randint(*_by(d, (6, 12), (8, 20), (15, 40))), random.randint(*_by(d, (5, 10), (6, 15), (12, 30))),
                  random.randint(2, _by(d, 3, 5, 9)), random.randint(2, _by(d, 3, 5, 9)))
    price = random.randint(*_by(d, (2, 5), (3, 12), (11, 35)))
    per = 2 * (W + H)
    return _int("A garden is an L-shape made by removing %s m by %d m corner from %s m by %d m rectangle. Fencing costs £%d per metre. "
                "How much does it cost to fence the whole edge, in pounds?" % (_an(w), h, _an(W), H, price), per * price,
                ["The perimeter of the L-shape equals the perimeter of the rectangle: %d m." % per, "%d × £%d = £%d." % (per, price, per * price)], "£")


@_more("Y8.9.e", 11)
def _(d):
    W, H = random.randint(*_by(d, (5, 8), (6, 12), (10, 18))), random.randint(*_by(d, (5, 7), (5, 10), (8, 15)))
    w, h = random.randint(2, W - 3), random.randint(2, H - 3)
    price = random.randint(*_by(d, (5, 10), (8, 25), (18, 45)))
    area = W * H - w * h
    return _int("An L-shaped room is %s m by %d m rectangle with %s m by %d m corner missing. Carpet costs £%d per m². How much does "
                "the carpet cost, in pounds?" % (_an(W), H, _an(w), h, price), area * price,
                ["Area = %d − %d = %d m²." % (W * H, w * h, area), "%d × £%d = £%d." % (area, price, area * price)], "£")


@_more("Y8.9.e", 11)
def _(d):
    r = random.randint(*_by(d, (1, 2), (1, 4), (3, 8))) * 2
    W, H = 2 * r + random.randint(*_by(d, (2, 4), (2, 8), (5, 15))), r + random.randint(*_by(d, (2, 4), (2, 8), (5, 15)))
    semi = Decimal("3.14") * r * r / 2
    return _num("Take π as 3.14. %s cm by %d cm rectangle has a semicircle of radius %d cm cut out of the middle of its %d cm edge. "
                "What area is left, in cm²?" % (_an(W).capitalize(), H, r, W), W * H - semi,
                ["Semicircle: ½ × 3.14 × %d² = %s cm²." % (r, _ds(semi)), "%d − %s = %s cm²." % (W * H, _ds(semi), _ds(W * H - semi))], "cm²")


@_more("Y8.9.f", 10)
def _(d):
    c = random.randint(*_by(d, (1, 2), (1, 3), (2, 5)))
    l, w, h = [c * random.randint(*_by(d, (2, 4), (2, 6), (4, 10))) for _ in range(3)]
    return _int("How many cubes of edge %d cm fit exactly inside a box that measures %d cm by %d cm by %d cm?" % (c, l, w, h),
                (l // c) * (w // c) * (h // c), ["%d × %d × %d cubes along the edges." % (l // c, w // c, h // c), "= %d." % ((l // c) * (w // c) * (h // c))])


@_more("Y8.9.f", 10)
def _(d):
    l, w = pick(_by(d, [(50, 20), (40, 25), (50, 40)], [(50, 40), (40, 25), (60, 50), (30, 20), (80, 25)],
                    [(45, 32), (75, 40), (64, 25), (120, 45), (90, 35)]))
    depth = random.randint(*_by(d, (2, 10), (2, 20), (12, 45)))
    litres = Decimal(l * w * depth) / 1000
    return _int("A fish tank has a base %d cm by %d cm. %s litres of water are poured in. How deep is the water, in cm? (1 litre = 1000 cm³)"
                % (l, w, _ds(litres)), depth,
                ["%s litres = %s cm³." % (_ds(litres), _c(l * w * depth)), "%s ÷ (%d × %d) = %d cm." % (_c(l * w * depth), l, w, depth)], "cm")


@_more("Y8.9.f", 10)
def _(d):
    W, H = random.randint(*_by(d, (4, 6), (4, 8), (8, 15))), random.randint(*_by(d, (4, 6), (4, 8), (8, 15)))
    w, h, L = random.randint(1, _by(d, 2, 3, 6)), random.randint(1, _by(d, 2, 3, 6)), random.randint(*_by(d, (2, 10), (5, 15), (12, 40)))
    area = W * H - w * h
    return _int("A prism has an L-shaped cross-section: %s cm by %d cm rectangle with %s cm by %d cm corner removed. The prism is %d cm long. "
                "What is its volume, in cm³?" % (_an(W), H, _an(w), h, L), area * L,
                ["Cross-section: %d − %d = %d cm²." % (W * H, w * h, area), "%d × %d = %d cm³." % (area, L, area * L)], "cm³")


@_more("Y8.9.f", 10)
def _(d):
    v = Decimal(random.randint(*_by(d, (2, 20), (2, 60), (101, 999)))) / pick(_by(d, [1], [1, 10, 100], [100, 1000]))
    if random.random() < 0.5:
        return _num("A pond holds %s m³ of water. How many litres is that? (1 m³ = 1000 litres)" % _ds(v), v * 1000,
                    ["%s × 1000 = %s litres." % (_ds(v), _ds(v * 1000))], "litres")
    return _num("A tank holds %s litres. What is that in m³? (1 m³ = 1000 litres)" % _ds(v * 1000), v,
                ["%s ÷ 1000 = %s m³." % (_ds(v * 1000), _ds(v))], "m³")


@_more("Y8.9.f", 10)
def _(d):
    a, L = random.randint(*_by(d, (4, 12), (6, 40), (25, 150))), random.randint(*_by(d, (2, 10), (3, 15), (11, 40)))
    return _int("A prism has a cross-section of area %d cm² and a volume of %d cm³. How long is the prism, in cm?" % (a, a * L), L,
                ["Volume = area × length.", "%d ÷ %d = %d cm." % (a * L, a, L)], "cm")


@_more("Y8.9.f", 10)
def _(d):
    k = pick(_by(d, [2], [2, 3], [3, 4, 5]))
    v = random.randint(*_by(d, (1, 10), (2, 20), (10, 60))) * 5
    return _int("A cuboid has a volume of %d cm³. Every edge is made %d times as long. What is the new volume, in cm³?" % (v, k), v * k ** 3,
                ["Each of the three dimensions is multiplied by %d, so the volume is multiplied by %d × %d × %d = %d." % (k, k, k, k, k ** 3),
                 "%d × %d = %d cm³." % (v, k ** 3, v * k ** 3)], "cm³")


@_more("Y8.9.g", 9)
def _(d):
    e = pick(_by(d, [2, 3, 4, 5], [2, 3, 4, 5, 7, 8, 9, 10], [7, 8, 9, 10, 11, 12, 15, 20]))   # not 6: 6³ = 6 × 6² would give the same number back
    return _int("A cube has a volume of %d cm³. What is its total surface area, in cm²?" % (e ** 3), 6 * e * e,
                ["Edge = ∛%d = %d cm." % (e ** 3, e), "6 × %d² = %d cm²." % (e, 6 * e * e)], "cm²")


@_more("Y8.9.g", 9)
def _(d):
    l, w, h = random.randint(*_by(d, (2, 4), (2, 6), (4, 12))), random.randint(*_by(d, (2, 3), (2, 5), (3, 9))), random.randint(*_by(d, (1, 2), (1, 4), (2, 6)))
    sa = 2 * (l * w + l * h + w * h)
    cover = pick(_by(d, [5, 10], [5, 10, 4, 8], [6, 7, 12, 15]))
    tins = -(-sa // cover)
    return _int("A box is %d m by %d m by %d m. All six faces are painted. One tin of paint covers %d m². How many tins are needed?" % (l, w, h, cover), tins,
                ["Surface area = 2(%d + %d + %d) = %d m²." % (l * w, l * h, w * h, sa), "%d ÷ %d = %s, so %d tins (round up)." % (sa, cover, _ds(_round(Decimal(sa) / cover, 2)), tins)], "tins")


@_more("Y8.9.g", 9)
def _(d):
    r, h = random.randint(*_by(d, (1, 3), (1, 6), (5, 12))), random.randint(*_by(d, (2, 6), (2, 12), (9, 25)))
    return _int("A cylinder has a volume of %dπ cm³ and a radius of %d cm. How tall is it, in cm?" % (r * r * h, r), h,
                ["πr²h = %dπ, so %d × h = %d." % (r * r * h, r * r, r * r * h), "h = %d cm." % h], "cm")


@_more("Y8.9.g", 9)
def _(d):
    l, w, h = random.randint(*_by(d, (2, 6), (3, 12), (10, 30))), random.randint(*_by(d, (2, 5), (3, 10), (8, 25))), random.randint(*_by(d, (2, 4), (2, 8), (6, 20)))
    sa = l * w + 2 * l * h + 2 * w * h
    return _int("An open box (no lid) is %d cm long, %d cm wide and %d cm tall. What is its outside surface area, in cm²?" % (l, w, h), sa,
                ["Base: %d × %d = %d." % (l, w, l * w), "Sides: 2 × %d × %d + 2 × %d × %d = %d." % (l, h, w, h, 2 * l * h + 2 * w * h), "Total %d cm²." % sa], "cm²")


@_more("Y8.9.g", 9)
def _(d):
    r, h = random.randint(*_by(d, (1, 3), (2, 6), (5, 12))), random.randint(*_by(d, (2, 10), (5, 15), (12, 30)))
    v = Decimal("3.14") * 2 * r * h
    return _num("Take π as 3.14. A paper label wraps exactly once around a tin of radius %d cm and height %d cm (no overlap). What is the area of "
                "the label, in cm²?" % (r, h), v, ["The label is the curved surface: 2 × 3.14 × %d × %d." % (r, h), "= %s cm²." % _ds(v)], "cm²")


@_more("Y8.9.g", 9)
def _(d):
    e = random.randint(*_by(d, (2, 5), (2, 9), (8, 20)))
    return {"prompt": "This net folds into a cube with edges of %d cm. What is the total area of the net, in cm²?" % e, "component": "net",
            "spec": {"solid": "cube"}, "answer": 6 * e * e, "answer_type": "int",
            "solution": ["The net is 6 squares, each %d × %d = %d cm²." % (e, e, e * e), "6 × %d = %d cm²." % (e * e, 6 * e * e)]}


def _stem_rows(values):
    stems = sorted({v // 10 for v in values})
    return [[str(s), " ".join(str(v % 10) for v in sorted(values) if v // 10 == s)] for s in range(stems[0], stems[-1] + 1)]


def _stem_q(prompt, values, answer, solution, atype="int"):
    return _dt(prompt, ["Stem", "Leaves"], _stem_rows(values), answer, solution, atype=atype,
               caption="Key: %d | %d means %d" % (min(values) // 10, min(values) % 10, min(values)))


@_more("Y8.9.i", 7)
def _(d):
    while True:
        vals = [random.randint(*_by(d, (12, 39), (12, 69), (10, 99))) for _ in range(random.randint(*_by(d, (6, 9), (9, 14), (15, 22))))]
        m = max(vals, key=vals.count)
        if vals.count(m) >= 2 and sum(1 for v in set(vals) if vals.count(v) == vals.count(m)) == 1:
            break
    return _stem_q("What is the mode of the data in the stem-and-leaf diagram?", vals, m,
                   ["Look for the leaf that appears most often on one stem.", "%d appears %d times." % (m, vals.count(m))])


@_more("Y8.9.i", 7)
def _(d):
    vals = random.sample(range(*_by(d, (10, 50), (10, 80), (10, 100))), random.randint(*_by(d, (6, 9), (10, 15), (16, 24))))
    cut = random.randint(*_by(d, (20, 40), (25, 60), (30, 80)))
    n = sum(1 for v in vals if v > cut)
    return _stem_q("The stem-and-leaf diagram shows the marks in a test. How many marks are greater than %d?" % cut, vals, n,
                   ["Marks above %d: %s." % (cut, ", ".join(str(v) for v in sorted(vals) if v > cut) or "none"), "That is %d." % n])


@_more("Y8.9.i", 7)
def _(d):
    hi, k = _by(d, (40, 5), (60, 7), (90, 11))
    a = random.sample(range(10, hi), k)
    b = random.sample(range(10, hi), k)
    stems = sorted({v // 10 for v in a + b})
    rows = [[" ".join(str(v % 10) for v in sorted((x for x in a if x // 10 == s), reverse=True)), str(s),
             " ".join(str(v % 10) for v in sorted(x for x in b if x // 10 == s))] for s in range(stems[0], stems[-1] + 1)]
    grp = random.random() < 0.5
    vals = b if grp else a
    who = "girls" if grp else "boys"
    return _dt("The back-to-back stem-and-leaf diagram shows the times (in seconds) of boys (left) and girls (right). What is the range "
               "of the %s' times?" % who, ["Boys", "Stem", "Girls"], rows, max(vals) - min(vals),
               ["The %s' longest time is %d and the shortest is %d." % (who, max(vals), min(vals)), "%d − %d = %d." % (max(vals), min(vals), max(vals) - min(vals))],
               caption="Key: 3 | 2 | 5 means 23 s for a boy and 25 s for a girl")


@_more("Y8.9.i", 7)
def _(d):
    sizes = [3, 4, 5, 6, 7, 8]
    while True:
        freq = [random.randint(_by(d, 1, 0, 2), _by(d, 5, 8, 12)) for _ in sizes]
        if sum(freq) >= 10 and sorted(freq)[-1] != sorted(freq)[-2]:
            break
    kind = random.randrange(3) if d else pick([0, 2])
    if kind == 0:
        q, ans, sol = "What is the mode?", sizes[freq.index(max(freq))], ["The tallest column of dots is size %d." % sizes[freq.index(max(freq))]]
    elif kind == 1:
        k = random.choice(sizes[1:-1])
        ans = sum(f for s, f in zip(sizes, freq) if s >= k)
        q, sol = "How many pupils wear size %d or bigger?" % k, ["Add the dots for sizes %d to 8: %d." % (k, ans)]
    else:
        q, ans, sol = "How many pupils were asked?", sum(freq), ["Add up all the dots: %d." % sum(freq)]
    return _bar("The chart shows the shoe sizes of a class (each unit is one pupil). %s" % q, [str(s) for s in sizes], freq, ans, sol)


@_more("Y8.9.i", 7)
def _(d):
    while True:
        vals = random.sample(range(*_by(d, (10, 40), (10, 60), (10, 100))), random.randint(*_by(d, (4, 5), (5, 8), (8, 12))))
        if sum(vals) % len(vals) == 0:
            break
    return _stem_q("What is the mean of the data in the stem-and-leaf diagram?", vals, sum(vals) // len(vals),
                   ["Total = %d, and there are %d values." % (sum(vals), len(vals)), "%d ÷ %d = %d." % (sum(vals), len(vals), sum(vals) // len(vals))])


@_more("Y8.9.i", 7)
def _(d):
    vals = sorted(random.sample(range(*_by(d, (20, 60), (20, 90), (10, 100))), random.randint(*_by(d, (5, 7), (8, 12), (13, 18)))))
    stems = sorted({v // 10 for v in vals})
    rows = [[str(s), " ".join(str(v % 10) for v in vals if v // 10 == s)] for s in range(stems[0], stems[-1] + 1)]
    ask_big = random.random() < 0.5
    v = vals[-1] if ask_big else vals[0]
    return _dt("The stem-and-leaf diagram shows the lengths of some leaves, in cm. The stem is the units and the leaf is tenths. What is the "
               "%s length, in cm?" % ("longest" if ask_big else "shortest"), ["Stem", "Leaves"], rows, _ds(Decimal(v) / 10),
               ["%d | %d means %s cm." % (v // 10, v % 10, _ds(Decimal(v) / 10))], atype="num",
               caption="Key: %d | %d means %s cm" % (vals[0] // 10, vals[0] % 10, _ds(Decimal(vals[0]) / 10)))


@_more("Y8.9.i", 7)
def _(d):
    n = pick(_by(d, [10], [10, 20, 25], [25, 40, 50]))
    vals = random.sample(range(10, _by(d, 60, 80, 100)), n)
    cut = random.randint(*_by(d, (30, 50), (30, 60), (35, 75)))
    k = sum(1 for v in vals if v >= cut)
    return _stem_q("The stem-and-leaf diagram shows %d scores. What percentage of the scores are %d or more?" % (n, cut), vals,
                   _ds(Decimal(100 * k) / n), ["%d of the %d scores are %d or more." % (k, n, cut), "%d/%d × 100 = %s%%." % (k, n, _ds(Decimal(100 * k) / n))], atype="num")


@_more("Y8.1.a", 12)
def _(d):
    n = random.randint(*_by(d, (20, 200), (100, 900), (1000, 9999)))
    a, b = pick(_by(d, [(2, 5), (3, 4), (2, 3)], [(3, 4), (2, 9), (3, 5), (4, 5), (2, 7)],
                    [(4, 6), (6, 9), (4, 10), (3, 7), (4, 9)]))     # stretch: often NOT coprime
    m = _lcm(a, b)
    ans = (n // m + 1) * m
    return _int("What is the smallest number greater than %s that is divisible by both %d and %d?" % (_c(n), a, b), ans,
                ["Divisible by %d and %d means divisible by %d%s." % (a, b, m, "" if m == a * b else " (their LCM, not %d × %d)" % (a, b)),
                 "The next multiple of %d after %d is %d." % (m, n, ans)])


@_more("Y8.1.a", 12)
def _(d):
    p, q = _by(d, (2, 5), (3, 5), (3, 4))
    while True:
        nums = random.sample(range(*_by(d, (10, 100), (100, 1000), (1000, 10000))), 5)
        k = sum(1 for x in nums if x % (p * q) == 0)
        if k:
            break
    rows = [[str(x), "yes" if x % p == 0 else "no", "yes" if x % q == 0 else "no"] for x in nums]
    return _dt("The table shows whether each number is divisible by %d and by %d. How many of the numbers are divisible by %d?"
               % (p, q, p * q), ["Number", "÷ %d?" % p, "÷ %d?" % q], rows, k,
               ["A number is divisible by %d when it is divisible by both %d and %d." % (p * q, p, q),
                "%s." % ("1 number" if k == 1 else "%d numbers" % k)])


@_more("Y8.1.a", 12)
def _(d):
    yes = random.random() < 0.5
    if d == 0:                     # easy: the 4 rule, last two digits
        while True:
            n = random.randint(100, 9999)
            if (n % 4 == 0) == yes:
                break
        return _yn("A number is divisible by 4 if its last two digits make a multiple of 4. Is %s divisible by 4?" % _c(n),
                   yes, ["The last two digits are %02d." % (n % 100),
                         "%d ÷ 4 %s." % (n % 100, "is exact" if n % 4 == 0 else "is not exact")])
    while True:
        n = random.randint(1000, _by(d, 0, 99999, 9999999))
        if (n % 8 == 0) == yes:
            break
    last3 = n % 1000
    return _yn("A number is divisible by 8 if its last three digits make a multiple of 8. Is %s divisible by 8?" % _c(n), yes,
               ["The last three digits are %03d." % last3, "%d ÷ 8 %s." % (last3, "is exact" if last3 % 8 == 0 else "is not exact")])


@_more("Y8.3.i", 13)
def _(d):
    f, g = _two_unlike(d)
    k = random.randint(2, 4)
    return _fq("Work out (%s + %s) × %d. Give your answer as a fraction." % (_simp_str(f), _simp_str(g), k), (f + g) * k,
               ["Brackets first: %s + %s = %s." % (_simp_str(f), _simp_str(g), _simp_str(f + g)),
                "× %d = %s." % (k, _simp_str((f + g) * k))])


@_more("Y8.3.i", 13)
def _(d):
    a = Fraction(random.randint(1, 5), random.randint(6, 9))
    b = Fraction(1, random.randint(2, 4))
    c = Fraction(random.randint(1, 3), random.randint(4, 6))
    v = a + b * c
    return _fq("Work out %s + %s × %s. Give your answer as a fraction." % (_simp_str(a), _simp_str(b), _simp_str(c)), v,
               ["Multiply before adding: %s × %s = %s." % (_simp_str(b), _simp_str(c), _simp_str(b * c)),
                "%s + %s = %s." % (_simp_str(a), _simp_str(b * c), _simp_str(v))])


@_more("Y8.3.i", 13)
def _(d):
    tot = random.randint(2, 6) * 24
    f1, f2 = pick([(Fraction(1, 3), Fraction(1, 4)), (Fraction(1, 2), Fraction(1, 3)), (Fraction(1, 4), Fraction(1, 6)),
                   (Fraction(2, 3), Fraction(1, 2)), (Fraction(3, 8), Fraction(1, 3))])
    first = tot * f1
    second = (tot - first) * f2
    return _int("%s has £%d. They spend %s of it on a coat and then %s of what is left on shoes. How much do they have left, in pounds?"
                % (_who(), tot, _simp_str(f1), _simp_str(f2)), tot - first - second,
                ["Coat: %s of %d = £%d, leaving £%d." % (_simp_str(f1), tot, first, tot - first),
                 "Shoes: %s of %d = £%d, leaving £%d." % (_simp_str(f2), tot - first, second, tot - first - second)], "£")


@_more("Y8.7.b", 11)
def _(d):
    x = random.randint(-9, 12)
    a = random.randint(2, 9)
    b = random.randint(1, 20)
    return _int("Solve %d − %dx = %d." % (b, a, b - a * x), x,
                ["Subtract %d from both sides: −%dx = %d." % (b, a, -a * x), "Divide by −%d: x = %d." % (a, x)])


@_more("Y8.7.b", 11)
def _(d):
    x = random.randint(1, 12)
    a, c = random.randint(2, 6), random.randint(1, 9)
    while (x + c) % a:
        x += 1
    return _int("Solve (x + %d) / %d = %d." % (c, a, (x + c) // a), x,
                ["Multiply both sides by %d: x + %d = %d." % (a, c, x + c), "x = %d." % x])


@_more("Y8.7.b", 11)
def _(d):
    x = random.randint(2, 15)
    a, b = random.randint(2, 9), random.randint(1, 30)
    who = _who()
    return _int("%s makes a mistake solving %dx + %d = %d and gets x = %d. What is the correct value of x?"
                % (who, a, b, a * x + b, x + random.randint(1, 3)), x,
                ["%dx = %d − %d = %d." % (a, a * x + b, b, a * x), "x = %d ÷ %d = %d." % (a * x, a, x)])


# ================================================================ register ====
for _k, (_old, _fns) in _EXTRA.items():
    _e.GENERATORS[_k] = _widen(_e.GENERATORS[_k], _old, _fns)
