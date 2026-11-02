# Year 5 shared helpers: number formatting, words to a million, Roman numerals to MMM,
# exact fractions/decimals, and the question builders every Y5 module uses.
#
# Every generator takes a difficulty d: 0 = easy, 1 = core, 2 = stretch.
import random
from decimal import Decimal
from fractions import Fraction

from .maths_engine import n_words, pick, NAMES

__all__ = ["random", "Fraction", "Decimal", "pick", "NAMES", "_d", "_by", "_c", "_words", "_rom",
           "_fs", "_mixed", "_ds", "_dec", "_tb", "_wq", "_fq", "_nl", "_nld", "_io", "_dt", "_lg",
           "_bar", "_strip", "_area", "_pick_t", "_who", "_pl", "_r", "_distinct"]


def _d(d):
    try:
        d = int(d)
    except Exception:
        d = 1
    return 0 if d < 0 else (2 if d > 2 else d)


def _by(d, a, b, c):
    """Pick a value by difficulty."""
    return (a, b, c)[_d(d)]


def _c(n):
    """3482 -> '3,482'; keeps negatives."""
    n = int(n)
    return ("-" if n < 0 else "") + "{:,}".format(abs(n))


def _words(n):
    """UK words for 0..9,999,999: 305021 -> 'three hundred and five thousand and twenty-one'."""
    n = int(n)
    if n < 1000:
        return n_words(n)
    if n < 1_000_000:
        th, r = divmod(n, 1000)
        s = n_words(th) + " thousand"
        if r == 0:
            return s
        return s + (" and " if r < 100 else " ") + n_words(r)
    m, r = divmod(n, 1_000_000)
    s = n_words(m) + " million"
    if r == 0:
        return s
    return s + (" and " if r < 100 else " ") + _words(r)


_RV = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
       (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _rom(n):
    n, out = int(n), ""
    for v, s in _RV:
        while n >= v:
            out += s
            n -= v
    return out


def _fs(f):
    """Fraction -> 'a/b' (not simplified further; integers stay 'n')."""
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)


def _mixed(f):
    """Fraction -> '2 1/3' (whole numbers stay whole, proper fractions stay 'a/b')."""
    f = Fraction(f)
    w, r = divmod(f.numerator, f.denominator)
    if r == 0:
        return str(w)
    if w == 0:
        return "%d/%d" % (r, f.denominator)
    return "%d %d/%d" % (w, r, f.denominator)


def _dec(x):
    """Exact Decimal from int/str/Fraction-with-terminating-decimal."""
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def _ds(x):
    """Exact decimal string without trailing zeros: 3.450 -> '3.45', 4.0 -> '4'."""
    v = _dec(x).normalize()
    s = format(v, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _tb(prompt, ans, atype="int", spec=None, solution=None, tol=0):
    q = {"prompt": prompt, "component": "number", "spec": spec or {},
         "answer": ans, "answer_type": atype, "solution": solution or []}
    if tol:
        q["tolerance"] = tol
    return q


def _wq(prompt, ans, solution, placeholder="type your answer"):
    return _tb(prompt, ans, "str", {"text": True, "placeholder": placeholder}, solution)


def _fq(prompt, ans, solution, placeholder="e.g. 3/4"):
    """A fraction answer compared by value (2/4 = 1/2 = 0.5)."""
    return _tb(prompt, _fs(ans), "frac", {"text": True, "placeholder": placeholder}, solution)


def _nl(prompt, ans, step, major, solution, lo=None, hi=None):
    """Place a whole number on a number line."""
    ans = int(ans)
    if lo is None:
        lo = (ans // major) * major - 2 * major
        if lo < 0 <= ans:
            lo = 0
    if hi is None:
        hi = lo + 5 * major
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": lo, "max": hi, "step": step, "major": major},
            "answer": ans, "answer_type": "num", "tolerance": step / 2.0, "solution": solution}


def _nld(prompt, ans, lo, hi, step, major, solution):
    """Place a decimal on a number line from lo to hi."""
    return {"prompt": prompt, "component": "number_line",
            "spec": {"min": float(lo), "max": float(hi), "step": float(step), "major": float(major)},
            "answer": float(ans), "answer_type": "num", "tolerance": float(step) / 2.0,
            "solution": solution}


def _io(prompt, rows, missing, answer, solution, rule=None, atype="int"):
    spec = {"rows": [[a, b] for a, b in rows]}
    if missing is not None:
        spec["missing"] = int(missing)
    if rule:
        spec["ruleLabel"] = rule
    return {"prompt": prompt, "component": "io_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _dt(prompt, headers, rows, answer, solution, missing=None, atype="int", caption=None, placeholder=None):
    spec = {"headers": [str(h) for h in headers], "rows": [[str(c) for c in r] for r in rows]}
    if missing is not None:
        spec["missing"] = [int(missing[0]), int(missing[1])]
    if caption:
        spec["caption"] = caption
    if placeholder:
        spec["placeholder"] = placeholder
    return {"prompt": prompt, "component": "data_table", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _lg(prompt, points, answer, solution, ylabel, xlabel, atype="int", tol=0):
    q = {"prompt": prompt, "component": "line_graph",
         "spec": {"points": [[str(a), b] for a, b in points], "yLabel": ylabel, "xLabel": xlabel},
         "answer": answer, "answer_type": atype, "solution": solution}
    if tol:
        q["tolerance"] = tol
    return q


def _bar(prompt, cats, vals, answer, solution, atype="int"):
    return {"prompt": prompt, "component": "bar_chart",
            "spec": {"categories": list(cats), "values": list(vals), "mode": "read"},
            "answer": answer, "answer_type": atype, "solution": solution}


def _strip(prompt, spec, answer, solution, atype="int"):
    return {"prompt": prompt, "component": "strip_model", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _area(prompt, spec, answer, solution, atype="int"):
    return {"prompt": prompt, "component": "area_grid", "spec": spec,
            "answer": answer, "answer_type": atype, "solution": solution}


def _pick_t(plain, visual=()):
    """Choose a framing; visual framings count twice."""
    return random.choice(list(plain) + list(visual) + list(visual))()


def _who():
    return pick(NAMES)


def _pl(n, word, plural=None):
    return "%s %s" % (_c(n) if isinstance(n, int) else n, word if n == 1 else (plural or word + "s"))


def _r(n, unit):
    """Round a non-negative integer to the nearest unit, halves up."""
    return ((int(n) + unit // 2) // unit) * unit


def _distinct(k, lo, hi):
    return random.sample(range(lo, hi + 1), k)
