# Year 7 generators: strands 7.7 and 7.8.
#
# Fractional thinking: add and subtract any fractions and mixed numbers, multiply and divide
# fractions, fraction problems.  Lines and angles: notation and labelling, measuring and estimating,
# angles at a point / on a line / vertically opposite, angles in triangles and quadrilaterals,
# properties of triangles and quadrilaterals, polygon angle sums, perpendicular and parallel lines
# and constructions, area of triangles, parallelograms and trapezia.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403

S7 = "7.7 Fractional thinking"
S8 = "7.8 Lines & angles"

def _a(x):
    """'a 7 cm', 'an 8 cm', 'an 11-sided', 'an octagon': the article read aloud, plus the text."""
    s = str(x)
    w = s.split()[0].replace(",", "").split("-")[0]
    if w[:1].isdigit():
        vowel = w.startswith("8") or w in ("11", "18") or (len(w) in (5, 8) and w[:2] in ("11", "18"))
    else:
        vowel = w[:1].lower() in "aeiou"
    return ("an " if vowel else "a ") + s



def _add_why(a, b, sign=1):
    """The steps of a/b ± c/d: the common denominator, each fraction renamed, then the sum or difference
    simplified (and as a mixed number when it is more than 1)."""
    den = a.denominator * b.denominator // _gcd(a.denominator, b.denominator)
    na, nb = a.numerator * den // a.denominator, b.numerator * den // b.denominator
    s = a + b if sign > 0 else a - b
    raw = "%d/%d" % (na + nb if sign > 0 else na - nb, den)
    out = ["Use a common denominator, %d: %s = %d/%d and %s = %d/%d." % (den, _fs(a), na, den, _fs(b), nb, den),
           "%d/%d %s %d/%d = %s." % (na, den, "+" if sign > 0 else "−", nb, den, raw)]
    if raw != _mixed(s):
        out.append("In its simplest form: %s." % _mixed(s))
    return out


def _rf(d, proper=True):
    den = pick(_by(d, [2, 3, 4, 5, 6], [3, 4, 5, 6, 8, 9, 10], [6, 7, 8, 9, 10, 12, 15]))
    num = random.randint(1, den - 1) if proper else random.randint(den + 1, 3 * den)
    return Fraction(num, den), num, den


# ================================================================== 7.7 ======
@skill("Y7.7.a", "Add and subtract fractions with any denominators", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)
    while bd == ad:
        b, bn, bd = _rf(d)

    def t_add():
        return _fq("Work out  %d/%d + %d/%d" % (an, ad, bn, bd), a + b,
                   _add_why(a, b))

    def t_sub():
        x, y = max(a, b), min(a, b)
        if x == y:                                    # 1/2 − 2/4 would be 0
            return t_add()
        return _fq("Work out  %s − %s" % (_fs(x), _fs(y)), x - y, _add_why(x, y, -1))

    def t_simplest():
        s = a + b
        return _wq("Work out %d/%d + %d/%d. Give the answer in its simplest form (as a mixed number if it is more than 1)."
                   % (an, ad, bn, bd), _mixed(s), _add_why(Fraction(an, ad), Fraction(bn, bd)), "e.g. 1 1/6")

    def t_missing():
        s = a + b
        return _fq("%d/%d + ___ = %s. What is the missing fraction?" % (an, ad, _fs(s)), b,
                   ["%s − %d/%d = %s." % (_fs(s), an, ad, _fs(b))])

    def t_word():
        x, y = max(a, b), min(a, b)
        if x + y >= 1:
            return t_sub()
        who = _who()
        return _fq("%s spends %s of the money in a purse on a book and %s on a game. What fraction is left?" % (who, _fs(x), _fs(y)),
                   1 - x - y, ["1 − %s − %s = %s." % (_fs(x), _fs(y), _fs(1 - x - y))])

    def t_three():
        c, cn, cd = _rf(d)
        tot = a + b - c
        if tot <= 0:
            return t_add()
        return _fq("Work out  %s + %s − %s" % (_fs(a), _fs(b), _fs(c)), tot, ["Use a common denominator for all three: %s." % _fs(tot)])

    def t_more_than_one():
        return _wq("Is %s + %s more than 1? (yes or no)" % (_fs(a), _fs(b)), "yes" if a + b > 1 else "no",
                   ["%s + %s = %s." % (_fs(a), _fs(b), _fs(a + b))], "yes / no") if a + b != 1 else t_add()

    def t_error():
        return _fq("%s says %d/%d + %d/%d = %d/%d. What is the correct answer?" % (_who(), an, ad, bn, bd, an + bn, ad + bd), a + b,
                   ["You cannot add the denominators. Common denominator %d: %s." % (ad * bd // _gcd(ad, bd), _fs(a + b))])

    def t_lcd():
        if a.denominator != ad or b.denominator != bd:
            return t_add()
        return _tb("What is the lowest common denominator of %d/%d and %d/%d?" % (an, ad, bn, bd), ad * bd // _gcd(ad, bd), "int",
                   {}, ["The LCM of %d and %d is %d." % (ad, bd, ad * bd // _gcd(ad, bd))])

    def t_hours():
        x, y = pick([(Fraction(3, 4), Fraction(2, 3)), (Fraction(1, 2), Fraction(1, 3)), (Fraction(1, 4), Fraction(5, 6)),
                     (Fraction(2, 3), Fraction(1, 6)), (Fraction(3, 4), Fraction(1, 3))])
        return _fq("%s worked for %s of an hour, then %s of an hour. How many hours is that altogether?" % (_who(), _fs(x), _fs(y)),
                   x + y, ["%s + %s = %s hours (%d minutes)." % (_fs(x), _fs(y), _fs(x + y), int((x + y) * 60))])

    def t_bar():
        den = ad * bd // _gcd(ad, bd)
        if den > 12 or a == b:
            return t_add()
        res = a + b if a + b <= 1 else abs(a - b)
        txt = "%s + %s" % (_fs(a), _fs(b)) if a + b <= 1 else "%s − %s" % (_fs(max(a, b)), _fs(min(a, b)))
        return {"prompt": "Work out %s. Shade the bar to show the answer (it has %d equal parts)." % (txt, den),
                "component": "fraction_bar", "spec": {"parts": den, "mode": "shade"},
                "answer": "%d/%d" % (int(res * den), den), "answer_type": "frac",
                "solution": ["With %d equal parts: %s = %d/%d." % (den, txt, int(res * den), den)]}

    return _pick_t([t_add, t_sub, t_simplest, t_missing, t_word, t_three, t_more_than_one, t_error, t_lcd, t_hours], [t_bar])


def _gcd(x, y):
    while y:
        x, y = y, x % y
    return x


@skill("Y7.7.b", "Add and subtract mixed numbers", S7)
def _(d=1):
    d = _d(d)
    A = random.randint(1, 6) + _rf(d)[0]
    B = random.randint(1, 4) + _rf(d)[0]

    def t_add():
        return _wq("Work out %s + %s. Give a mixed number in its simplest form." % (_mixed(A), _mixed(B)), _mixed(A + B),
                   ["Add the whole numbers: %d + %d = %d." % (int(A), int(B), int(A) + int(B))]
                   + _add_why(A - int(A), B - int(B))
                   + ["Put them together: %s." % _mixed(A + B)], "e.g. 5 1/4")

    def t_sub():
        x, y = max(A, B), min(A, B)
        if x == y:
            return t_add()
        return _wq("Work out %s − %s. Give a mixed number (or whole number) in its simplest form." % (_mixed(x), _mixed(y)),
                   _mixed(x - y), ["Convert to improper fractions or subtract wholes and parts: %s." % _mixed(x - y)],
                   "e.g. 2 3/4")

    def t_whole_minus():
        w = random.randint(3, 8)
        f = _rf(d)[0]
        return _fq("Work out %d − %s." % (w, _mixed(1 + f)), w - 1 - f,
                   ["Take away the whole 1 first: %d − 1 = %d." % (w, w - 1),
                    "Then take away %s: write 1 of the %d as %d/%d, so %d − %s = %s." % (
                        _fs(f), w - 1, f.denominator, f.denominator, w - 1, _fs(f), _mixed(w - 1 - f))], "e.g. 2 1/3")

    def t_word():
        return _wq("A plank is %s m long. %s m is cut off. How much is left, in metres? (mixed number, simplest form)"
                   % (_mixed(A + B), _mixed(B)), _mixed(A), ["%s − %s = %s." % (_mixed(A + B), _mixed(B), _mixed(A))],
                   "e.g. 3 1/2")

    def t_improper():
        return _wq("Write %s as an improper fraction." % _mixed(A), _fs(A), ["%d × %d + %d = %d, so %s." % (
            A.numerator // A.denominator, A.denominator, A.numerator % A.denominator, A.numerator, _fs(A))], "e.g. 11/4")

    def t_to_whole():
        w = random.randint(B.numerator // B.denominator + 2, 9)
        return _wq("%s + ___ = %d. What is the missing number? (mixed number, simplest form)" % (_mixed(B), w), _mixed(w - B),
                   ["%d − %s = %s." % (w, _mixed(B), _mixed(w - B))], "e.g. 2 3/4")

    def t_exchange():
        den = pick([3, 4, 5, 6, 8])
        p = random.choice([v for v in range(1, den - 1) if _gcd(v, den) == 1])
        q = random.choice([v for v in range(p + 1, den) if _gcd(v, den) == 1])
        w1, w2 = random.randint(3, 8), random.randint(1, 2)
        x, y = w1 + Fraction(p, den), w2 + Fraction(q, den)
        return _wq("Work out %s − %s. (Mixed number, simplest form.)" % (_mixed(x), _mixed(y)), _mixed(x - y),
                   ["The fraction part %d/%d is smaller than %d/%d, so exchange a whole: %s = %d %d/%d."
                    % (p, den, q, den, _mixed(x), w1 - 1, den + p, den), "= %s." % _mixed(x - y)], "e.g. 2 3/4")

    def t_hours():
        x = random.randint(1, 3) + pick([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)])
        y = random.randint(1, 3) + pick([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 3)])
        return _fq("A film is %s hours long and another is %s hours. How long are they altogether, in hours? (mixed number)"
                   % (_mixed(x), _mixed(y)), x + y, ["%s + %s = %s." % (_mixed(x), _mixed(y), _mixed(x + y))], "e.g. 3 1/4")

    def t_perimeter():
        s = [random.randint(1, 4) + _rf(d)[0] for _ in range(3)]
        return _wq("A triangle has sides %s cm, %s cm and %s cm. What is its perimeter, in cm? (mixed number, simplest form)"
                   % tuple(_mixed(v) for v in s), _mixed(sum(s)), ["%s." % _mixed(sum(s))], "e.g. 9 1/2")

    def t_line():
        lo = random.randint(1, 4)
        f = pick([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 5), Fraction(3, 5)])
        v = lo + f
        step = Fraction(1, f.denominator)
        return _nld("Place %s on the number line." % _mixed(v), float(v), lo - 1, lo + 2, float(step), 1,
                    ["%s is %s of the way from %d to %d." % (_mixed(v), _fs(f), lo, lo + 1)])

    def t_bigger():
        if A == B:
            return t_add()
        return _wq("Which is bigger: %s or %s? (type it as written)" % (_mixed(A), _mixed(B)), _mixed(max(A, B)),
                   ["Compare the whole numbers first, then the fractions."], "e.g. 2 1/3")

    def t_ribbon():
        L = random.randint(5, 9)
        c1, c2 = random.randint(1, 2) + Fraction(1, 4), 1 + Fraction(pick([1, 2]), 3)
        return _wq("A ribbon is %d m long. Pieces of %s m and %s m are cut off. How much is left, in metres? (mixed number)"
                   % (L, _mixed(c1), _mixed(c2)), _mixed(L - c1 - c2), ["%d − %s − %s = %s." % (L, _mixed(c1), _mixed(c2),
                                                                                              _mixed(L - c1 - c2))], "e.g. 2 5/12")

    return _pick_t([t_add, t_sub, t_whole_minus, t_word, t_improper, t_to_whole, t_exchange, t_hours, t_perimeter, t_bigger, t_ribbon], [t_line])


@skill("Y7.7.c", "Multiply fractions", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)

    def t_ff():
        return _fq("Work out  %d/%d × %d/%d" % (an, ad, bn, bd), a * b,
                   ["Multiply tops and bottoms: %d/%d = %s." % (an * bn, ad * bd, _fs(a * b))])

    def t_of():
        return _fq("What is %d/%d of %d/%d?" % (an, ad, bn, bd), a * b, ["'Of' means ×: %s." % _fs(a * b)])

    def t_int():
        k = random.randint(2, 12)
        whole = "%d/%d" % (k * an, ad)
        return _fq("Work out  %d × %d/%d" % (k, an, ad), k * a,
                   ["Multiply the top by %d and keep the bottom: %d × %d = %d, so it is %s%s." % (
                       k, k, an, k * an, whole, "" if whole == _fs(k * a) else ", which simplifies to %s" % _fs(k * a))])

    def t_mixed():
        M = random.randint(1, 3) + a
        k = random.randint(2, 5)
        return _wq("Work out %s × %d. Give a mixed number (or whole number) in its simplest form." % (_mixed(M), k),
                   _mixed(M * k), ["Multiply the whole number and the fraction separately: %d × %d = %d and %d × %s = %s."
                                   % (k, int(M), k * int(M), k, _fs(M - int(M)), _mixed(k * (M - int(M)))),
                                   "Add them: %d + %s = %s." % (k * int(M), _mixed(k * (M - int(M))), _mixed(M * k))],
                   "e.g. 4 1/2")

    def t_area():
        return _fq("A rectangle is %d/%d m by %d/%d m. What is its area, in m²?" % (an, ad, bn, bd), a * b,
                   ["%s × %s = %s." % (_fs(a), _fs(b), _fs(a * b))])

    def t_cancel():
        p = random.randint(2, 5)
        q = random.randint(2, 7)
        r = random.randint(2, 7)
        return _fq("Work out  %d/%d × %d/%d  (cancel first if you can)" % (p, q * r, r, p * 2), Fraction(p, q * r) * Fraction(r, p * 2),
                   ["Cancel first: the %d on top and the %d underneath, and the %d on top and the %d underneath."
                    % (p, p * 2, r, q * r),
                    "That leaves 1/%d × 1/2 = %s." % (q, _fs(Fraction(p, q * r) * Fraction(r, p * 2)))])

    def t_mixed_mixed():
        M = random.randint(1, 2) + Fraction(1, pick([2, 3, 4]))
        N = random.randint(1, 3) + Fraction(pick([1, 2]), 3)
        return _wq("Work out %s × %s. Give a mixed number (or whole number) in its simplest form." % (_mixed(M), _mixed(N)),
                   _mixed(M * N), ["As improper fractions: %s × %s = %s." % (_fs(M), _fs(N), _mixed(M * N))], "e.g. 3 1/2")

    def t_of_of():
        p, q = pick([(Fraction(2, 3), Fraction(3, 4)), (Fraction(1, 2), Fraction(4, 5)), (Fraction(3, 5), Fraction(5, 6)),
                     (Fraction(3, 4), Fraction(2, 3)), (Fraction(1, 3), Fraction(3, 8))])
        x = (p * q).denominator * random.randint(2, 12)
        return _tb("Work out %s of %s of %d." % (_fs(p), _fs(q), x), int(p * q * x), "int", {},
                   ["%s × %s = %s; %s of %d = %d." % (_fs(p), _fs(q), _fs(p * q), _fs(p * q), x, int(p * q * x))])

    def t_square():
        return _fq("Work out  (%d/%d)²" % (an, ad), a * a, ["%d/%d × %d/%d = %s." % (an, ad, an, ad, _fs(a * a))])

    def t_bigger():
        return _wq("Is %d/%d × %d/%d bigger or smaller than %d/%d? (type bigger or smaller)" % (an, ad, bn, bd, an, ad), "smaller",
                   ["Multiplying by a fraction less than 1 makes it smaller."], "bigger / smaller") \
            if random.random() < 0.6 else \
            _wq("Is %d/%d × %d bigger or smaller than %d/%d? (type bigger or smaller)" % (an, ad, bn + bd, an, ad), "bigger",
                ["Multiplying by a number greater than 1 makes it bigger."], "bigger / smaller")

    def t_missing():
        return _fq("%d/%d × ___ = %s. What is the missing fraction?" % (an, ad, _fs(a * b)), b,
                   ["%s ÷ %d/%d = %s." % (_fs(a * b), an, ad, _fs(b))])

    return _pick_t([t_ff, t_of, t_int, t_mixed, t_area, t_cancel, t_mixed_mixed, t_of_of, t_square, t_bigger, t_missing])


@skill("Y7.7.d", "Divide with fractions", S7)
def _(d=1):
    d = _d(d)
    a, an, ad = _rf(d)
    b, bn, bd = _rf(d)

    def t_by_int():
        k = random.randint(2, 6)
        return _fq("Work out  %d/%d ÷ %d" % (an, ad, k), a / k, ["Dividing by %d is the same as × 1/%d: %s." % (k, k, _fs(a / k))])

    def t_int_by_unit():
        k, u = random.randint(2, 9), random.randint(2, 8)
        return _tb("How many %s are there in %d? (work out %d ÷ 1/%d)" % (_unit_word(u), k, k, u), k * u, "int", {},
                   ["%d × %d = %d." % (k, u, k * u)])

    def t_ff():
        return _fq("Work out  %d/%d ÷ %d/%d" % (an, ad, bn, bd), a / b, ["Multiply by the reciprocal %d/%d: %s." % (bd, bn, _fs(a / b))])

    def t_reciprocal():
        return _fq("What is the reciprocal of %d/%d?" % (an, ad), 1 / a, ["Flip it: %d/%d." % (ad, an)])

    def t_word():
        k = random.randint(2, 6)
        tot = Fraction(random.randint(2, 6))
        part = Fraction(1, pick([2, 3, 4]))
        return _tb("How many %s kg bags can be filled from %s kg of rice?" % (_fs(part), _fs(tot)), int(tot / part), "int",
                   {"unit": "bags"}, ["%s ÷ %s = %d." % (_fs(tot), _fs(part), int(tot / part))])

    def t_mixed_div():
        M = random.randint(1, 4) + Fraction(1, 2)
        k = pick([Fraction(1, 2), Fraction(3, 4), Fraction(1, 4)])
        return _wq("Work out %s ÷ %s. Give a mixed number (or whole number) in its simplest form." % (_mixed(M), _fs(k)),
                   _mixed(M / k), ["%s × %s = %s." % (_fs(M), _fs(1 / k), _mixed(M / k))], "e.g. 3 1/2")

    def t_portions():
        p = pick([Fraction(1, 4), Fraction(1, 3), Fraction(3, 4), Fraction(2, 3)])
        n = random.randint(3, 12)
        tot = p * n
        return _tb("A cake recipe needs %s kg of flour. How many cakes can be made from %s kg?" % (_fs(p), _mixed(tot)), n, "int",
                   {"unit": "cakes"}, ["%s ÷ %s = %d." % (_mixed(tot), _fs(p), n)])

    return _pick_t([t_by_int, t_int_by_unit, t_ff, t_reciprocal, t_word, t_mixed_div, t_portions])


def _unit_word(u):
    return {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths"}[u]


@skill("Y7.7.e", "Fraction problems", S7)
def _(d=1):
    d = _d(d)

    def t_remaining():
        x = random.randint(4, 20) * 12
        return _tb("A school has %d pupils. 1/3 walk, 1/4 come by bus and the rest come by car. How many come by car?" % x,
                   x - x // 3 - x // 4, "int", {}, ["1 − 1/3 − 1/4 = 5/12.", "5/12 of %d = %d." % (x, x - x // 3 - x // 4)])

    def t_of_remainder():
        x = random.randint(3, 15) * 20
        who = _who()
        return _tb("%s has £%d. %s spends 1/4 of it, then 2/5 of what is left. How much is left now, in pounds?"
                   % (who, x, who), x * 3 // 4 * 3 // 5, "int", {"unit": "£"},
                   ["After 1/4: £%d." % (x * 3 // 4), "2/5 of that is £%d; left £%d." % (x * 3 // 4 * 2 // 5, x * 3 // 4 * 3 // 5)])

    def t_whole_from_part():
        den = pick(_by(d, [2, 3, 4, 5], [3, 4, 5, 8], [5, 6, 7, 8, 9, 12]))
        num = 1 if d == 0 else pick([k for k in range(1, den) if Fraction(k, den).denominator == den])   # easy: a unit fraction
        part = num * random.randint(3, _by(d, 12, 20, 30))
        return _tb("%d/%d of a number is %d. What is the number?" % (num, den, part), part // num * den, "int", {},
                   ["%d ÷ %d = %d is 1/%d." % (part, num, part // num, den), "× %d = %d." % (den, part // num * den)])

    def t_compare():
        a, b = random.sample(_by(d, [Fraction(1, 2), Fraction(1, 3), Fraction(3, 4), Fraction(2, 5)],
                                 [Fraction(2, 3), Fraction(3, 5), Fraction(5, 8), Fraction(7, 12), Fraction(4, 7)],
                                 [Fraction(5, 8), Fraction(7, 12), Fraction(4, 7), Fraction(3, 5), Fraction(5, 9), Fraction(11, 20)]), 2)
        return _wq("Which is larger, %s or %s?" % (_fs(a), _fs(b)), _fs(max(a, b)),
                   ["%s ≈ %.3f, %s ≈ %.3f." % (_fs(a), float(a), _fs(b), float(b))], "e.g. 3/5")

    def t_recipe():
        m = Fraction(3, 4)
        k = pick([2, 3, 4, 6])
        return _wq("A recipe uses 3/4 cup of milk per batch. How much milk for %d batches? (mixed number or whole number)" % k,
                   _mixed(m * k), ["%d × 3/4 = %s." % (k, _mixed(m * k))], "e.g. 2 1/4")

    def t_price_rise():
        f = pick(_by(d, [Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)], [Fraction(1, 4), Fraction(1, 5), Fraction(1, 3), Fraction(2, 5)],
                     [Fraction(2, 5), Fraction(3, 8), Fraction(2, 3), Fraction(3, 4), Fraction(3, 10)]))
        x = f.denominator * random.randint(4, _by(d, 12, 30, 40))
        up = random.random() < 0.5
        new = x + f * x if up else x - f * x
        return _tb("A price of £%d %s by %s. What is the new price, in pounds?" % (x, "rises" if up else "falls", _fs(f)), int(new),
                   "int", {"unit": "£"}, ["%s of %d = %d." % (_fs(f), x, int(f * x)), "%d %s %d = %d." % (x, "+" if up else "−", int(f * x), int(new))])

    def t_ages():
        f = pick([Fraction(1, 4), Fraction(1, 5), Fraction(1, 6), Fraction(1, 8), Fraction(2, 15)])
        dad = f.denominator * random.randint(-(-56 // f.denominator), 90 // f.denominator)
        w = _who()
        return _tb("%s's age is %s of their grandad's age. Their grandad is %d. How old is %s?" % (w, _fs(f), dad, w),
                   int(f * dad), "int", {"unit": "years"}, ["%s of %d = %d." % (_fs(f), dad, int(f * dad))])

    def t_tank():
        f = pick([Fraction(2, 3), Fraction(3, 4), Fraction(2, 5), Fraction(5, 8), Fraction(3, 10)])
        full = f.denominator * random.randint(4, 20)
        return _tb("A water tank is %s full and holds %d litres. How many litres does it hold when full?" % (_fs(f), int(f * full)),
                   full, "int", {"unit": "litres"}, ["%d ÷ %d = %d is 1/%d." % (int(f * full), f.numerator, full // f.denominator,
                                                                               f.denominator), "× %d = %d." % (f.denominator, full)])

    def t_votes():
        x = random.randint(2, 15) * 8
        return _tb("In a vote, 3/8 chose pizza, 1/4 chose pasta and the rest chose curry. %d people chose curry. How many people "
                   "voted?" % (x * 3 // 8), x, "int", {"unit": "people"},
                   ["Curry: 1 − 3/8 − 1/4 = 3/8.", "3/8 is %d, so 1/8 is %d and the total is %d." % (x * 3 // 8, x // 8, x)])

    def t_journey():
        f = pick([Fraction(2, 5), Fraction(1, 3), Fraction(3, 4), Fraction(5, 8)])
        tot = f.denominator * random.randint(3, 15)
        return _tb("A family has driven %s of their journey. They have %d km left to go. How long is the whole journey, in km?"
                   % (_fs(f), int((1 - f) * tot)), tot, "int", {"unit": "km"},
                   ["%d km is %s of the journey." % (int((1 - f) * tot), _fs(1 - f)), "Whole journey = %d km." % tot])

    def t_strip():
        den = pick(_by(d, [2, 3, 4], [3, 4, 5, 6], [5, 6, 8]))
        num = random.randint(1, den - 1)
        part = random.randint(3, _by(d, 10, 15, 25))
        return _strip("%d/%d of the pupils in a club are girls. The bar shows all %d pupils split into %d equal parts. How many "
                      "girls are there?" % (num, den, den * part, den),
                      {"mode": "equal_parts", "parts": den, "partLabel": "?", "totalLabel": str(den * part), "unknown": "part"},
                      num * part, ["One part: %d ÷ %d = %d." % (den * part, den, part), "%d part%s: %d." % (num, "" if num == 1 else "s", num * part)])

    # easy: one-step problems with friendly fractions; hard: remainders, working back to the whole, several steps
    return _pick_t(_by(d, [t_whole_from_part, t_compare, t_recipe, t_price_rise, t_ages],
                       [t_remaining, t_of_remainder, t_whole_from_part, t_compare, t_recipe, t_price_rise, t_ages, t_tank,
                        t_votes, t_journey],
                       [t_remaining, t_of_remainder, t_whole_from_part, t_compare, t_price_rise, t_tank, t_votes, t_journey]),
                   [t_strip])


# ================================================================== 7.8 ======
@skill("Y7.8.a", "Angle notation and types", S8)
def _(d=1):
    d = _d(d)

    def t_type():
        if d == 2:                                   # hard: within a few degrees of 90° or 180°
            deg = pick([90, 180]) + pick([-1, 1]) * random.randint(1, 12)
        else:
            deg = random.choice([x for x in range(_by(d, 10, 5, 5), 356, _by(d, 10, 1, 1))
                                 if x not in (90, 180) and (d or not (80 <= x <= 100 or 170 <= x <= 190))])
        return _wq("Is an angle of %d° acute, obtuse or reflex?" % deg,
                   "acute" if deg < 90 else "obtuse" if deg < 180 else "reflex", ["Compare with 90° and 180°."],
                   "acute / obtuse / reflex")

    def t_vertex():
        p, q, r = random.sample("ABCDEFPQRS", 3)
        return _wq("In the angle written ∠%s%s%s, which letter is the vertex (the corner)?" % (p, q, r), q,
                   ["The middle letter is the vertex."], "one letter")

    def t_picture():
        deg = pick(_by(d, [random.randint(20, 70), random.randint(110, 160), random.randint(200, 330)],
                       [random.randint(15, 80), random.randint(100, 170), random.randint(190, 340)],
                       [random.randint(60, 80), random.randint(100, 130), random.randint(190, 220)]))
        return {"prompt": "Is this angle acute, obtuse or reflex?", "component": "angle",
                "spec": {"mode": "classify", "degrees": deg},
                "answer": "acute" if deg < 90 else "obtuse" if deg < 180 else "reflex", "answer_type": "str",
                "solution": ["It is about %d°." % deg]}

    def t_measure():
        deg = _by(d, random.randint(1, 17) * 10, random.randint(2, 34) * 5, random.randint(10, 170))
        return {"prompt": "Measure this angle. How many degrees is it?", "component": "angle",
                "spec": {"mode": "measure", "degrees": deg, "protractor": True}, "answer": deg, "answer_type": "num",
                "tolerance": 2, "solution": ["Read from 0 on the scale along the first arm: %d°." % deg]}

    def t_reflex():
        a = random.choice([v for v in range(20, 171, _by(d, 10, 1, 1)) if v != 90])
        if d == 2 and random.random() < 0.5:         # hard: work back from the reflex angle
            return _tb("The reflex angle between two arms is %d°. What is the other angle between them?" % (360 - a), a, "int",
                       {"unit": "°"}, ["360 − %d = %d." % (360 - a, a)])
        return _tb("The acute or obtuse angle between two arms is %d°. What is the reflex angle?" % a, 360 - a, "int",
                   {"unit": "°"}, ["360 − %d = %d." % (a, 360 - a)])

    def t_right_symbol():
        return _wq("On a diagram, what does a small square in a corner tell you about the angle? (one word: the angle is ...)",
                   "right", ["It marks a right angle (90°)."], "one word")

    return _pick_t(_by(d, [t_type, t_vertex, t_reflex, t_right_symbol], [t_type, t_vertex, t_reflex, t_right_symbol],
                       [t_type, t_reflex]), [t_picture, t_measure])


@skill("Y7.8.b", "Angles at a point, on a line and vertically opposite", S8)
def _(d=1):
    d = _d(d)

    def _ang(lo, hi):
        """easy: a multiple of 10 in [lo, hi]; otherwise any whole degree."""
        return random.randint(-(-lo // 10), hi // 10) * 10 if d == 0 else random.randint(lo, hi)

    def t_line():
        if d == 2:      # two angles on a line with a given difference
            diff = random.randint(5, 60) * 2
            big = (180 + diff) // 2
            return _tb("Two angles lie on a straight line. One is %d° bigger than the other. How big is the larger angle?" % diff,
                       big, "int", {"unit": "°"}, ["They add to 180 and differ by %d." % diff, "(180 + %d) ÷ 2 = %d." % (diff, big)])
        a = _ang(15, 165)
        return _tb("Two angles on a straight line: one is %d°. Find the other." % a, 180 - a, "int", {"unit": "°"},
                   ["180 − %d = %d." % (a, 180 - a)])

    def t_point():
        parts = [_ang(40, _by(d, 110, 110, 80)) for _ in range(_by(d, 2, 3, 4))]
        return _tb("Angles of %s and one more angle meet at a point. Find the missing angle." % ", ".join("%d°" % p for p in parts),
                   360 - sum(parts), "int", {"unit": "°"}, ["360 − %d = %d." % (sum(parts), 360 - sum(parts))])

    def t_vertical():
        a = _ang(20, 160)
        if d == 2:      # the other three angles at the crossing
            return _tb("Two straight lines cross. One of the four angles is %d°. What do the other three angles add up to?" % a,
                       360 - a, "int", {"unit": "°"}, ["All four angles make a full turn: 360 − %d = %d." % (a, 360 - a)])
        return _tb("Two straight lines cross. One angle is %d°. What is the angle vertically opposite it?" % a, a, "int",
                   {"unit": "°"}, ["Vertically opposite angles are equal."])

    def t_adjacent():
        if d == 2:      # one angle a multiple of its neighbour
            k = pick([2, 3, 4, 5, 8, 9])
            s = 180 // (k + 1)
            return _tb("Two straight lines cross. One angle is %d times the angle next to it. How big is the smaller angle?" % k,
                       s, "int", {"unit": "°"}, ["Neighbours add to 180: %dx = 180." % (k + 1), "x = %d." % s])
        a = _ang(20, 160)
        return _tb("Two straight lines cross. One angle is %d°. What is the angle next to it (on the same straight line)?" % a,
                   180 - a, "int", {"unit": "°"}, ["180 − %d = %d." % (a, 180 - a)])

    def t_algebra():
        if d == 0:      # x, x and a known angle
            x = random.randint(3, 8) * 10
            rest = 180 - 2 * x
            return _tb("Angles of x°, x° and %d° lie on a straight line. Find x." % rest, x, "int", {"unit": "°"},
                       ["2x + %d = 180." % rest, "x = %d." % x])
        if d == 2:      # two bracketed expressions
            x = random.randint(10, 35)
            p, q = random.randint(2, 4), random.randint(1, 3)
            c = random.randint(5, 30)
            e = 180 - (p + q) * x - c
            if e <= 0:
                return t_line()
            return _tb("Angles of (%dx + %d)° and (%sx + %d)° lie on a straight line. Find x." % (p, c, "" if q == 1 else q, e), x, "int",
                       {"unit": "°"}, ["%dx + %d = 180." % (p + q, c + e), "x = %d." % x])
        x = random.randint(10, 40)
        k = random.randint(2, 4)
        rest = 180 - (k + 1) * x
        if rest <= 0:
            return t_line()
        return _tb("Angles of x°, %dx° and %d° lie on a straight line. Find x." % (k, rest), x, "int", {"unit": "°"},
                   ["%dx + %d = 180." % (k + 1, rest), "x = %d." % x])

    def t_pic():
        if d == 2:      # the shown angle plus two equal ones make the line
            deg = random.randint(11, 79) * 2
            return {"prompt": "The angle shown is %d°. Two equal angles sit with it on a straight line. How big is each one?" % deg,
                    "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": (180 - deg) // 2,
                    "answer_type": "int", "solution": ["180 − %d = %d." % (deg, 180 - deg), "%d ÷ 2 = %d." % (180 - deg, (180 - deg) // 2)]}
        deg = random.randint(3, 15) * 10
        return {"prompt": "The angle shown is %d°. Another angle sits with it on a straight line. How big is it?" % deg,
                "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 180 - deg,
                "answer_type": "int", "solution": ["180 − %d = %d." % (deg, 180 - deg)]}

    def t_equal_point():
        if d == 2:      # equal angles plus one known angle
            n = pick([3, 4, 5, 6])
            each = random.randint(160 // n, 340 // n)
            a = 360 - n * each
            return _tb("%d equal angles and an angle of %d° meet at a point. How big is each equal angle?" % (n, a), each, "int",
                       {"unit": "°"}, ["360 − %d = %d." % (a, 360 - a), "%d ÷ %d = %d." % (360 - a, n, each)])
        n = pick(_by(d, [2, 3, 4, 6, 10], [3, 4, 5, 6, 8, 9, 10, 12], None))
        return _tb("%d equal angles meet at a point. How big is each one?" % n, 360 // n, "int", {"unit": "°"},
                   ["360 ÷ %d = %d." % (n, 360 // n)])

    def t_point_algebra():
        if d == 0:      # x, x and a known angle at a point
            x = random.randint(5, 15) * 10
            c = 360 - 2 * x
            return _tb("Angles of x°, x° and %d° meet at a point. What is x?" % c, x, "int", {"unit": "°"},
                       ["2x + %d = 360." % c, "x = %d." % x])
        if d == 2:      # expressions with constants
            for _ in range(50):
                a, b, c = random.randint(1, 4), random.randint(1, 4), random.randint(2, 5)
                x, p = random.randint(15, 60), random.randint(5, 40)
                q = (a + b + c) * x + p - 360
                if 0 < q < c * x:
                    return _tb("Angles of (%sx + %d)°, %sx° and (%dx − %d)° meet at a point. What is x?"
                               % ("" if a == 1 else a, p, "" if b == 1 else b, c, q), x, "int", {"unit": "°"},
                               ["%dx + %d − %d = 360." % (a + b + c, p, q), "%dx = %d, so x = %d." % (a + b + c, 360 - p + q, x)])
        x = pick([20, 24, 30, 36, 40, 45, 60])
        k = 360 // x
        a = random.randint(1, k - 3)
        b = random.randint(1, k - a - 1)
        c = k - a - b
        terms = ["%sx°" % ("" if t == 1 else t) for t in (a, b, c)]
        return _tb("Angles of %s, %s and %s meet at a point. What is x?" % tuple(terms), x, "int", {"unit": "°"},
                   ["%dx = 360, so x = %d." % (k, x)])

    def t_vert_algebra():
        x = random.randint(5, 30)
        c = random.randint(5, 40)
        if d == 2:      # x on both sides
            k, m = random.randint(3, 6), random.randint(1, 2)
            e = (k - m) * x + c
            if k * x + c >= 180:
                k, m, e = 3, 1, 2 * x + c
            return _tb("Two straight lines cross. Vertically opposite angles are (%dx + %d)° and (%sx + %d)°. What is x?"
                       % (k, c, "" if m == 1 else m, e), x, "int", {"unit": "°"},
                       ["They are equal: %dx + %d = %sx + %d." % (k, c, "" if m == 1 else m, e),
                        "%dx = %d, so x = %d." % (k - m, e - c, x)])
        k = _by(d, 1, random.randint(2, 4), 1)
        return _tb("Two straight lines cross. Vertically opposite angles are (%sx + %d)° and %d°. What is x?"
                   % ("" if k == 1 else k, c, k * x + c), x,
                   "int", {"unit": "°"}, ["They are equal: %sx + %d = %d." % ("" if k == 1 else k, c, k * x + c), "x = %d." % x])

    def t_three_line():
        if d == 2:      # four angles on a line
            a, b, c = random.randint(20, 50), random.randint(20, 50), random.randint(20, 50)
            return _tb("Four angles lie on a straight line. Three of them are %d°, %d° and %d°. Find the fourth." % (a, b, c),
                       180 - a - b - c, "int", {"unit": "°"}, ["180 − %d − %d − %d = %d." % (a, b, c, 180 - a - b - c)])
        a, b = _ang(20, 80), _ang(20, 70)
        return _tb("Three angles lie on a straight line. Two of them are %d° and %d°. Find the third." % (a, b), 180 - a - b, "int",
                   {"unit": "°"}, ["180 − %d − %d = %d." % (a, b, 180 - a - b)])

    def t_reflex_pic():
        if d == 2:      # the shown angle plus two equal ones make a full turn
            deg = random.randint(20, 80) * 2
            return {"prompt": "The angle shown is %d°. Two equal angles complete the full turn with it. How big is each one?" % deg,
                    "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": (360 - deg) // 2,
                    "answer_type": "int", "solution": ["360 − %d = %d." % (deg, 360 - deg), "%d ÷ 2 = %d." % (360 - deg, (360 - deg) // 2)]}
        deg = random.randint(4, 16) * 10
        return {"prompt": "The angle shown is %d°. What is the reflex angle that makes a full turn with it?" % deg,
                "component": "angle", "spec": {"mode": "classify", "degrees": deg, "numeric": True}, "answer": 360 - deg,
                "answer_type": "int", "solution": ["360 − %d = %d." % (deg, 360 - deg)]}

    def t_check_line():
        if d == 2:      # three angles, sometimes just off
            a, b = random.randint(30, 80), random.randint(30, 70)
            c = 180 - a - b + pick([0, 0, 2, -3])
            return _wq("Three angles of %d°, %d° and %d° sit next to each other. Do they make a straight line? (yes or no)" % (a, b, c),
                       "yes" if a + b + c == 180 else "no", ["%d + %d + %d = %d." % (a, b, c, a + b + c)], "yes / no")
        a = _ang(30, 150)
        b = 180 - a + pick(_by(d, [0, 0, 10, -10], [0, 0, 5, -10], None))
        return _wq("Two angles of %d° and %d° sit next to each other. Do they make a straight line? (yes or no)" % (a, b),
                   "yes" if a + b == 180 else "no", ["%d + %d = %d." % (a, b, a + b)], "yes / no")

    return _pick_t([t_line, t_point, t_vertical, t_adjacent, t_algebra, t_equal_point, t_point_algebra, t_vert_algebra,
                    t_three_line, t_check_line], [t_pic, t_reflex_pic])


@skill("Y7.8.c", "Angles in triangles", S8)
def _(d=1):
    d = _d(d)
    if d == 0:                                       # easy: multiples of 10
        a = random.randint(2, 10) * 10
        b = random.randint(2, (160 - a) // 10) * 10
    else:
        a = random.randint(20, 100)
        b = random.randint(20, 160 - a)

    def t_third():
        return _tb("Two angles of a triangle are %d° and %d°. Find the third angle." % (a, b), 180 - a - b, "int",
                   {"unit": "°"}, ["180 − %d − %d = %d." % (a, b, 180 - a - b)])

    def t_isos_base():
        apex = random.randint(20, 140) // 2 * 2
        return _tb("An isosceles triangle has an angle of %d° between its two equal sides. Find each of the other two angles."
                   % apex, (180 - apex) // 2, "int", {"unit": "°"}, ["(180 − %d) ÷ 2 = %d." % (apex, (180 - apex) // 2)])

    def t_isos_apex():
        base = random.randint(20, 85) if d else random.randint(4, 8) * 10
        return _tb("An isosceles triangle has two equal angles of %d°. Find the third angle." % base, 180 - 2 * base, "int",
                   {"unit": "°"}, ["180 − 2 × %d = %d." % (base, 180 - 2 * base)])

    def t_right():
        x = random.randint(10, 80) if d else random.randint(2, 16) * 5
        return _tb("A right-angled triangle has an angle of %d°. Find the third angle." % x, 90 - x, "int", {"unit": "°"},
                   ["180 − 90 − %d = %d." % (x, 90 - x)])

    def t_equilateral():
        return _tb("What size is each angle in an equilateral triangle?", 60, "int", {"unit": "°"}, ["180 ÷ 3 = 60."])

    def t_exterior():
        return _tb("A triangle has interior angles %d° and %d°. Find the exterior angle at the third corner (on a straight "
                   "line with the third angle)." % (a, b), a + b, "int", {"unit": "°"},
                   ["Third angle = %d°." % (180 - a - b), "180 − %d = %d." % (180 - a - b, a + b)])

    def t_possible():
        x, y, z = random.randint(20, 100), random.randint(20, 100), random.randint(20, 100)
        if random.random() < 0.5:
            z = 180 - x - y if 180 - x - y > 0 else z
        return _wq("Could a triangle have angles of %d°, %d° and %d°? (yes or no)" % (x, y, z),
                   "yes" if x + y + z == 180 else "no", ["They add up to %d°." % (x + y + z)], "yes / no")

    def t_algebra():
        x = random.randint(20, 40)
        c = random.randint(5, 30)
        rest = 180 - 3 * x - c                    # x <= 40 and c <= 30 keep this at least 30
        return _tb("The angles of a triangle are x°, (2x + %d)° and %d°. What is x?" % (c, rest), x, "int", {"unit": "°"},
                   ["3x + %d + %d = 180." % (c, rest), "3x = %d, x = %d." % (180 - c - rest, x)])

    def t_type():
        x, y = random.randint(20, 80), random.randint(20, 80)
        z = 180 - x - y
        kind = "acute" if z < 90 and x < 90 and y < 90 else "right" if 90 in (x, y, z) else "obtuse"
        return _wq("A triangle has angles of %d° and %d°. Is it an acute-angled, right-angled or obtuse-angled triangle? "
                   "(type acute, right or obtuse)" % (x, y), kind, ["The third angle is %d°." % z], "acute / right / obtuse")

    def t_right_isos():
        return _tb("A right-angled triangle is also isosceles. What size is each of its two equal angles?", 45, "int",
                   {"unit": "°"}, ["(180 − 90) ÷ 2 = 45."])

    def t_ext_interior():
        a = random.randint(25, 80)
        ext = a + random.randint(30, 90)
        return _tb("The exterior angle at one corner of a triangle is %d°. One of the two opposite interior angles is %d°. "
                   "Find the other." % (ext, a), ext - a, "int", {"unit": "°"},
                   ["The exterior angle equals the sum of the two opposite interior angles: %d − %d = %d." % (ext, a, ext - a)])

    def t_isos_from_base():
        base = random.randint(30, 80) if d else random.randint(6, 16) * 5
        return _tb("In an isosceles triangle one of the two equal angles is %d°. What is the angle between the two equal sides?"
                   % base, 180 - 2 * base, "int", {"unit": "°"}, ["180 − 2 × %d = %d." % (base, 180 - 2 * base)])

    def t_pic():
        a = random.randint(4, 9) * 10
        b = random.randint(2, 13 - a // 10) * 10
        return {"prompt": "In a triangle, the angle shown is %d° and another angle is %d°. How big is the third angle?" % (a, b),
                "component": "angle", "spec": {"mode": "classify", "degrees": a, "numeric": True}, "answer": 180 - a - b,
                "answer_type": "int", "solution": ["180 − %d − %d = %d." % (a, b, 180 - a - b)]}

    # easy: find the third angle directly; hard: isosceles from the apex, exterior angles, algebra, classifying
    return _pick_t(_by(d, [t_third, t_isos_apex, t_right, t_equilateral, t_possible, t_isos_from_base],
                       [t_third, t_isos_base, t_isos_apex, t_right, t_equilateral, t_exterior, t_possible, t_algebra, t_type,
                        t_right_isos, t_ext_interior, t_isos_from_base],
                       [t_third, t_isos_base, t_exterior, t_algebra, t_type, t_right_isos, t_ext_interior, t_isos_from_base]),
                   [t_pic])


@skill("Y7.8.d", "Angles and properties of quadrilaterals", S8)
def _(d=1):
    d = _d(d)

    def t_fourth():
        if d == 0:                                   # easy: multiples of 10
            a, b, c = random.randint(5, 13) * 10, random.randint(5, 13) * 10, random.randint(4, 12) * 10
        else:
            a, b, c = random.randint(50, 130), random.randint(50, 130), random.randint(40, 120)
        if a + b + c >= 350:
            c = 60
        return _tb("Three angles of a quadrilateral are %d°, %d° and %d°. Find the fourth." % (a, b, c), 360 - a - b - c,
                   "int", {"unit": "°"}, ["Angles in a quadrilateral add to 360°.", "360 − %d = %d." % (a + b + c, 360 - a - b - c)])

    def t_parallelogram():
        a = random.randint(40, 140) if d else random.randint(4, 14) * 10
        return _tb("A parallelogram has one angle of %d°. What size is the angle next to it?" % a, 180 - a, "int",
                   {"unit": "°"}, ["Neighbouring angles in a parallelogram add to 180°."])

    def t_kite():
        a, b = random.randint(60, 140), random.randint(40, 100)
        c = 360 - a - b - b
        if c <= 20:
            return t_fourth()
        return _tb("A kite has a pair of equal angles of %d° each and another angle of %d°. Find the last angle." % (b, a),
                   c, "int", {"unit": "°"}, ["360 − %d − %d − %d = %d." % (b, b, a, c)])

    def t_property():
        q, ans = pick([("Which quadrilateral has 4 equal sides and 4 right angles?", "square"),
                       ("Which quadrilateral has exactly one pair of parallel sides?", "trapezium"),
                       ("Which quadrilateral has 4 equal sides but its angles are not right angles?", "rhombus"),
                       ("Which quadrilateral has two pairs of equal adjacent sides and one line of symmetry?", "kite"),
                       ("Which quadrilateral has opposite sides equal and parallel, and 4 right angles, but not all sides "
                        "equal?", "rectangle")])
        return _wq(q, ans, ["That is the definition of a %s." % ans], "name")

    def t_diagonals():
        q, ans = pick([("Do the diagonals of a square cross at right angles? (yes or no)", "yes"),
                       ("Do the diagonals of a rectangle (not a square) cross at right angles? (yes or no)", "no"),
                       ("Do the diagonals of a rhombus cross at right angles? (yes or no)", "yes"),
                       ("Are the diagonals of a rectangle equal in length? (yes or no)", "yes")])
        return _wq(q, ans, ["Think of the shape's symmetry."], "yes / no")

    def t_algebra():
        x, c = random.randint(45, 60), random.randint(10, 40)
        rest = 360 - 4 * x - c                       # 80 to 170
        return _tb("The angles of a quadrilateral are x°, 2x°, (x + %d)° and %d°. What is x?" % (c, rest), x, "int", {"unit": "°"},
                   ["4x + %d + %d = 360." % (c, rest), "4x = %d, x = %d." % (4 * x, x)])

    # easy: missing angle with round numbers, names; hard: kites, diagonals and an algebraic angle sum
    return _pick_t(_by(d, [t_fourth, t_parallelogram, t_property],
                       [t_fourth, t_parallelogram, t_kite, t_property, t_diagonals],
                       [t_fourth, t_parallelogram, t_kite, t_diagonals, t_algebra]))


@skill("Y7.8.e", "Angles in polygons", S8)
def _(d=1):
    d = _d(d)
    n = pick([5, 6, 8]) if d == 0 else random.randint(5, 12)      # easy: familiar shapes, all with whole regular angles
    name = {5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 11: "hendecagon",
            12: "dodecagon"}[n]

    def t_sum():
        return _tb("What do the interior angles of %s (%d sides) add up to?" % (_a(name), n), (n - 2) * 180, "int",
                   {"unit": "°"}, ["(n − 2) × 180 = %d × 180 = %d." % (n - 2, (n - 2) * 180)])

    def t_regular():
        if 360 % n:
            return t_sum()
        return _tb("What is each interior angle of a regular %s?" % name, 180 - 360 // n, "int", {"unit": "°"},
                   ["Exterior angle = 360 ÷ %d = %d." % (n, 360 // n), "Interior = 180 − %d = %d." % (360 // n, 180 - 360 // n)])

    def t_exterior():
        if 360 % n:
            return t_sum()
        return _tb("What is each exterior angle of a regular %s?" % name, 360 // n, "int", {"unit": "°"},
                   ["Exterior angles add to 360°: 360 ÷ %d = %d." % (n, 360 // n)])

    def t_triangles():
        return _tb("How many triangles can %s-sided polygon be split into by drawing diagonals from one corner?" % _a(n), n - 2,
                   "int", {}, ["Always 2 fewer than the number of sides."])

    def t_missing():
        if d == 2:                                   # hard: a hexagon, five angles given
            k, shape, lo, hi = 6, "hexagon", 110, 130
        else:
            k, shape, lo, hi = 5, "pentagon", 95, 130
        tot = (k - 2) * 180
        angles = [random.randint(lo, hi) for _ in range(k - 1)]
        return _tb("%s angles of %s are %s. Find the %s." % (("Four", "Five")[k - 5], _a(shape), ", ".join("%d°" % a for a in angles),
                                                         ("fifth", "sixth")[k - 5]), tot - sum(angles),
                   "int", {"unit": "°"}, ["%s total = %d°." % (shape.capitalize(), tot),
                                          "%d − %d = %d." % (tot, sum(angles), tot - sum(angles))])

    def t_sides_from_ext():
        n2 = pick(_by(d, [3, 4, 5, 6, 8, 10], [3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20], [9, 12, 15, 18, 20, 24, 30, 36, 40]))
        return _tb("A regular polygon has exterior angles of %d°. How many sides does it have?" % (360 // n2), n2, "int", {},
                   ["360 ÷ %d = %d." % (360 // n2, n2)])

    def t_sides_from_int():
        n2 = pick([5, 6, 8, 9, 10, 12, 15, 18, 20])
        ext = 360 // n2
        return _tb("Each interior angle of a regular polygon is %d°. How many sides does it have?" % (180 - ext), n2, "int", {},
                   ["Exterior angle = 180 − %d = %d." % (180 - ext, ext), "360 ÷ %d = %d." % (ext, n2)])

    def t_sides_from_sum():
        return _tb("The interior angles of a polygon add up to %s°. How many sides does it have?" % _c((n - 2) * 180), n, "int", {},
                   ["%s ÷ 180 = %d triangles." % (_c((n - 2) * 180), n - 2), "Sides = %d + 2 = %d." % (n - 2, n)])

    # hard: work backwards from an angle or an angle sum to the number of sides
    return _pick_t(_by(d, [t_sum, t_regular, t_exterior, t_triangles, t_sides_from_ext],
                       [t_sum, t_regular, t_exterior, t_triangles, t_missing, t_sides_from_ext],
                       [t_sum, t_regular, t_missing, t_sides_from_ext, t_sides_from_int, t_sides_from_sum]))


@skill("Y7.8.f", "Parallel and perpendicular lines and constructions", S8)
def _(d=1):
    d = _d(d)

    def t_vocab():
        q, ans = pick([("Two lines that meet at a right angle are called what?", "perpendicular"),
                       ("Two lines that never meet and stay the same distance apart are called what?", "parallel"),
                       ("A line that cuts another line exactly in half at 90° is called the perpendicular what?", "bisector"),
                       ("Which tool, apart from a ruler, is used for standard constructions? (a pair of ...)", "compasses")])
        return _wq(q + " (one word)", ans, ["Key vocabulary."], "one word")

    def t_bisect_angle():
        a = random.randint(*_by(d, (2, 17), (10, 85), (10, 89))) * _by(d, 10, 2, 2)
        return _tb("An angle of %d° is bisected. What size are the two new angles?" % a, a // 2, "int", {"unit": "°"},
                   ["Bisect means cut in half: %d ÷ 2 = %d." % (a, a // 2)])

    def t_bisect_line():
        L = random.randint(*_by(d, (2, 10), (4, 30), (15, 60))) * 2
        return _tb("A line segment %d cm long has its perpendicular bisector drawn. How far is the crossing point from each "
                   "end, in cm?" % L, L // 2, "int", {"unit": "cm"}, ["%d ÷ 2 = %d." % (L, L // 2)])

    def t_shortest():
        return _wq("What is the shortest distance from a point to a line: along any line, or along the perpendicular? "
                   "(type any or perpendicular)", "perpendicular", ["The perpendicular distance is shortest."],
                   "any / perpendicular")

    def t_grid():
        x, y = random.randint(1, 4), random.randint(2, 6)
        k = random.randint(2, 4)
        if d == 2:                                   # hard: AB is vertical, so C goes sideways
            return {"prompt": "A line goes from A(%d,%d) to B(%d,%d). Plot point C so that AC is perpendicular to AB and %d squares "
                              "long, going right." % (x, y, x, y + 4, k), "component": "coordinate_grid",
                    "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[x, y, "A"], [x, y + 4, "B"]],
                             "lines": [{"p1": [x, y], "p2": [x, y + 4]}]},
                    "answer": "(%d,%d)" % (x + k, y), "answer_type": "coord",
                    "solution": ["AB is vertical, so AC must be horizontal: (%d,%d)." % (x + k, y)]}
        return {"prompt": "A line goes from A(%d,%d) to B(%d,%d). Plot point C so that AC is perpendicular to AB and %d squares "
                          "long, going up." % (x, y, x + 4, y, k), "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "points": [[x, y, "A"], [x + 4, y, "B"]],
                         "lines": [{"p1": [x, y], "p2": [x + 4, y]}]},
                "answer": "(%d,%d)" % (x, y + k), "answer_type": "coord",
                "solution": ["AB is horizontal, so AC must be vertical: (%d,%d)." % (x, y + k)]}

    def t_parallel_grid():
        x, y = random.randint(1, 3), random.randint(1, 3)
        dx, dy = random.randint(1, 3), random.randint(1, 3)
        if d == 2 and random.random() < 0.5:         # hard: a line sloping down
            y, dy = y + 3, -dy
        x2 = random.randint(4, 6)
        return {"prompt": "Line AB goes from (%d,%d) to (%d,%d). Starting at C(%d,%d), plot point D so that CD is parallel to AB "
                          "and the same length." % (x, y, x + dx, y + dy, x2, y), "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10,
                         "points": [[x, y, "A"], [x + dx, y + dy, "B"], [x2, y, "C"]],
                         "lines": [{"p1": [x, y], "p2": [x + dx, y + dy]}]},
                "answer": "(%d,%d)" % (x2 + dx, y + dy), "answer_type": "coord",
                "solution": ["Make the same move: %d right and %d %s." % (dx, abs(dy), "up" if dy > 0 else "down")]}

    def t_pairs():
        q, ans = pick([("How many pairs of parallel sides does a rectangle have?", 2),
                       ("How many pairs of parallel sides does a parallelogram have?", 2),
                       ("How many pairs of parallel sides does a regular hexagon have?", 3),
                       ("How many right angles does a rectangle have?", 4),
                       ("How many pairs of parallel sides does a kite have?", 0),
                       ("How many pairs of perpendicular sides does a right-angled triangle have?", 1)])
        return _tb(q, ans, "int", {}, ["Picture the shape and check each pair of sides."])

    def t_is_parallel():
        dx, dy = random.randint(1, 3), random.randint(1, 3)
        same = random.random() < 0.5
        ex, ey = (dx, dy) if same else pick([(dy, dx), (dx + 1, dy), (dx, dy + 1)])
        if not same and ex * dy == ey * dx:
            ex += 1
        x0, y0 = random.randint(0, 3), random.randint(0, 3)
        x1, y1 = random.randint(4, 6), random.randint(0, 2)
        if ex * dy == ey * dx and (x1 - x0) * dy == (y1 - y0) * dx:
            y1 = (y1 + 1) % 3
        return {"prompt": "Line AB goes from (%d,%d) to (%d,%d). Line CD goes from (%d,%d) to (%d,%d). Are the lines parallel? "
                          "(yes or no)" % (x0, y0, x0 + dx, y0 + dy, x1, y1, x1 + ex, y1 + ey), "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "typed": True, "placeholder": "yes / no",
                         "points": [[x0, y0, "A"], [x0 + dx, y0 + dy, "B"], [x1, y1, "C"], [x1 + ex, y1 + ey, "D"]],
                         "lines": [{"p1": [x0, y0], "p2": [x0 + dx, y0 + dy]}, {"p1": [x1, y1], "p2": [x1 + ex, y1 + ey]}]},
                "answer": "yes" if ex * dy == ey * dx else "no", "answer_type": "str",
                "solution": ["AB moves %d right, %d up; CD moves %d right, %d up." % (dx, dy, ex, ey)]}

    def t_perp_angle():
        return _tb("A line is drawn perpendicular to another line. What angle do they make?", 90, "int", {"unit": "°"},
                   ["Perpendicular means at right angles: 90°."]) if random.random() < 0.3 else \
            _wq("A road runs north–south. Another road crosses it running east–west. Are the roads parallel or perpendicular?",
                "perpendicular", ["North–south and east–west meet at right angles."], "parallel / perpendicular")

    def t_construct():
        a = random.randint(4, 12)
        return _tb("An equilateral triangle is constructed with compasses on a line segment %d cm long. How long is each of its "
                   "other two sides, in cm?" % a, a, "int", {"unit": "cm"}, ["All three sides of an equilateral triangle are equal."])

    # easy: vocabulary, halving and plotting a perpendicular; hard: shortest distance, counting pairs, parallel slopes
    return _pick_t(_by(d, [t_vocab, t_bisect_angle, t_bisect_line, t_perp_angle, t_construct],
                       [t_vocab, t_bisect_angle, t_bisect_line, t_shortest, t_pairs, t_perp_angle, t_construct],
                       [t_vocab, t_bisect_angle, t_bisect_line, t_shortest, t_pairs]),
                   _by(d, [t_grid], [t_grid, t_parallel_grid, t_is_parallel], [t_grid, t_parallel_grid, t_is_parallel]))


@skill("Y7.8.g", "Area of triangles, parallelograms and trapezia", S8)
def _(d=1):
    d = _d(d)

    def t_triangle():
        if d == 2:                                   # hard: a base to 1 d.p.
            b, h = Decimal(random.randint(25, 199)) / 10, random.randint(4, 30)
            return _tb("A triangle has base %s cm and perpendicular height %d cm. Find its area, in cm²." % (_ds(b), h),
                       _ds(b * h / 2), "num", {"unit": "cm²"}, ["½ × %s × %d = %s." % (_ds(b), h, _ds(b * h / 2))])
        b, h = random.randint(1, 10) * 2 if d == 0 else random.randint(2, 20), random.randint(2, _by(d, 12, 20, 20))   # easy: even base
        return _tb("A triangle has base %d cm and perpendicular height %d cm. Find its area, in cm²." % (b, h), _ds(Fraction(b * h, 2)),
                   "num", {"unit": "cm²"}, ["½ × %d × %d = %s." % (b, h, _ds(Fraction(b * h, 2)))])

    def t_parallelogram():
        b, h = random.randint(2, _by(d, 12, 20, 40)), random.randint(2, _by(d, 10, 15, 30))
        return _tb("A parallelogram has base %d m and perpendicular height %d m. Find its area, in m²." % (b, h), b * h, "int",
                   {"unit": "m²"}, ["base × height = %d." % (b * h)])

    def t_trapezium():
        a, b, h = random.randint(2, _by(d, 10, 15, 30)), random.randint(2, _by(d, 10, 15, 30)), random.randint(2, _by(d, 10, 12, 25))
        if d == 0 and (a + b) % 2:                   # easy: whole-number area
            b += 1
        return _tb("A trapezium has parallel sides %d cm and %d cm, and height %d cm. Find its area, in cm²." % (a, b, h),
                   _ds(Fraction((a + b) * h, 2)), "num", {"unit": "cm²"},
                   ["½ × (%d + %d) × %d = %s." % (a, b, h, _ds(Fraction((a + b) * h, 2)))])

    def t_reverse():
        b = random.randint(2, _by(d, 10, 16, 30))
        h = random.randint(2, _by(d, 10, 16, 30))
        return _tb("A triangle has area %s cm² and base %d cm. What is its perpendicular height, in cm?" % (_ds(Fraction(b * h, 2)), b),
                   h, "int", {"unit": "cm"}, ["Area × 2 ÷ base = %d." % h])

    def t_slant_trap():
        b, h, s = random.randint(4, 15), random.randint(3, 10), 0
        s = h + random.randint(1, 4)
        return _tb("A parallelogram has base %d cm, a sloping side of %d cm and perpendicular height %d cm. Find its area, in cm²."
                   % (b, s, h), b * h, "int", {"unit": "cm²"}, ["Use the perpendicular height, not the sloping side: %d × %d." % (b, h)])

    def t_compound():
        w, h, th = random.randint(4, 12), random.randint(3, 10), random.randint(2, 6)
        return _tb("A house shape is %s cm by %d cm rectangle with a triangle on top of base %d cm and height %d cm. Find the "
                   "total area, in cm²." % (_a(w), h, w, th), _ds(w * h + Fraction(w * th, 2)), "num", {"unit": "cm²"},
                   ["%d + %s = %s." % (w * h, _ds(Fraction(w * th, 2)), _ds(w * h + Fraction(w * th, 2)))])

    def t_grid_triangle():
        x0, y0 = random.randint(0, 2), random.randint(0, 2)
        b = _by(d, random.randint(1, 3) * 2, random.randint(2, 7), random.randint(5, 8))     # easy: even base, whole area
        h = random.randint(*_by(d, (2, 5), (2, 7), (5, 8)))
        apex = x0 + random.randint(0, b)
        return {"prompt": "Find the area of the triangle drawn on the grid. Each square is 1 cm². Give your answer in cm².",
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "typed": True, "placeholder": "cm²",
                         "polygon": [[x0, y0], [x0 + b, y0], [apex, y0 + h]]},
                "answer": _ds(Fraction(b * h, 2)), "answer_type": "num",
                "solution": ["Base %d, perpendicular height %d." % (b, h), "½ × %d × %d = %s." % (b, h, _ds(Fraction(b * h, 2)))]}

    def t_grid_parallelogram():
        x0, y0 = random.randint(0, 2), random.randint(0, 2)
        b, h, s = (random.randint(*_by(d, (2, 4), (2, 5), (4, 6))), random.randint(*_by(d, (2, 4), (2, 6), (5, 8))),
                   random.randint(1, _by(d, 2, 3, 2)))
        return {"prompt": "Find the area of the parallelogram drawn on the grid. Each square is 1 cm². Give your answer in cm².",
                "component": "coordinate_grid",
                "spec": {"xmin": 0, "xmax": 10, "ymin": 0, "ymax": 10, "typed": True, "placeholder": "cm²",
                         "polygon": [[x0, y0], [x0 + b, y0], [x0 + b + s, y0 + h], [x0 + s, y0 + h]]},
                "answer": b * h, "answer_type": "int", "solution": ["Base %d × perpendicular height %d = %d." % (b, h, b * h)]}

    def t_trap_reverse():
        a, b = random.randint(2, 10), random.randint(2, 10)
        h = random.randint(2, 10)
        if (a + b) * h % 2:
            h += 1
        return _tb("A trapezium has parallel sides %d m and %d m and an area of %d m². What is its height, in m?"
                   % (a, b, (a + b) * h // 2), h, "int", {"unit": "m"},
                   ["½ × (%d + %d) × h = %d, so %d × h = %d." % (a, b, (a + b) * h // 2, (a + b), (a + b) * h), "h = %d." % h])

    def t_cut_out():
        w, h = random.randint(6, 14), random.randint(5, 12)
        tb, th = random.randint(2, w - 2), random.randint(2, h - 1)
        return _tb("A triangle with base %d cm and height %d cm is cut out of %s cm by %d cm rectangle of card. What area of "
                   "card is left, in cm²?" % (tb, th, _a(w), h), _ds(w * h - Fraction(tb * th, 2)), "num", {"unit": "cm²"},
                   ["%d − %s = %s." % (w * h, _ds(Fraction(tb * th, 2)), _ds(w * h - Fraction(tb * th, 2)))])

    def t_mixed_units():
        b = Decimal(random.randint(5, 15)) / 10
        h = random.randint(2, 9) * 10
        return _tb("A triangle has base %s m and perpendicular height %d cm. Find its area, in cm²." % (_ds(b), h),
                   _ds(b * 100 * h / 2), "num", {"unit": "cm²"},
                   ["%s m = %d cm." % (_ds(b), int(b * 100)), "½ × %d × %d = %s." % (int(b * 100), h, _ds(b * 100 * h / 2))])

    def t_compare():
        b, h = random.randint(3, 12), random.randint(3, 12)
        return _wq("A triangle and a parallelogram both have base %d cm and perpendicular height %d cm. Which has the bigger area? "
                   "(type triangle or parallelogram)" % (b, h), "parallelogram",
                   ["Triangle %s cm², parallelogram %d cm²: the triangle is half." % (_ds(Fraction(b * h, 2)), b * h)],
                   "triangle / parallelogram")

    # easy: one formula with whole numbers; hard: working back to a length, compound shapes, mixed units
    return _pick_t(_by(d, [t_triangle, t_parallelogram, t_trapezium, t_slant_trap, t_compare],
                       [t_triangle, t_parallelogram, t_trapezium, t_reverse, t_slant_trap, t_compound, t_trap_reverse,
                        t_cut_out, t_mixed_units, t_compare],
                       [t_triangle, t_trapezium, t_reverse, t_slant_trap, t_compound, t_trap_reverse, t_cut_out, t_mixed_units]),
                   [t_grid_triangle, t_grid_parallelogram])
