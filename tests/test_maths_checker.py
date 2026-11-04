"""For every skill: the right answer typed in another fair way is accepted, and a near miss is refused."""
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e  # noqa: E402

RUNS = 6


def _bump_digit(s):
    """'3.2x10^-4' -> '4.2x10^-4': the same shape with one digit wrong."""
    m = re.search(r"\d", s)
    return None if not m else s[:m.start()] + str((int(m.group()) + 1) % 10) + s[m.end():]


def variants(q):
    at, a, tol = q.get("answer_type", "num"), str(q["answer"]), q.get("tolerance", 0) or 0
    ok, bad = [], []
    if at in ("num", "int"):
        v = float(a.replace(",", ""))
        ok += [" %s " % a, a.replace("-", "−")]
        if v == int(v) and abs(v) >= 1000:
            ok.append("{:,}".format(int(v)))
        dp = len(a.split(".")[1]) if "." in a else 0
        step = max(2 * tol, 10 ** -dp)
        bad += [repr(round(v + step, dp + 1)), repr(round(v - step, dp + 1))]
    elif at == "frac":
        f = e._frac(a)
        ok += ["%d/%d" % (2 * f.numerator, 2 * f.denominator)]
        if f.denominator != 1 and abs(f) > 1 and f > 0:
            w, r = divmod(f.numerator, f.denominator)
            ok.append("%d %d/%d" % (w, r, f.denominator))
        g = f + Fraction(1, f.denominator * 2)
        bad.append("%d/%d" % (g.numerator, g.denominator))
    elif at == "set":
        parts = [p for p in a.replace(",", " ").split()]
        ok.append(", ".join(reversed(parts)))
        bad.append(", ".join(parts[:-1] + [str(float(parts[-1]) + 1)]) if parts else None)
    elif at == "coord":
        ok += [a.strip("()"), a.replace(",", ", ")]
        bad.append(_bump_digit(a))
    elif at == "time":
        ok.append(a.replace(":", "."))
        bad.append(_bump_digit(a))
    else:
        ok += [a.upper(), re.sub(r"\s*([+=<>])\s*", r" \1 ", a), re.sub(r"(?<=\d)x(?=10\^)", " × ", a)]
        b = _bump_digit(a)
        sp = q.get("spec") or {}
        others = [str(c) for c in sp.get("choices") or sp.get("options") or [] if not e.check_answer(at, str(c), a)]
        bad += [b] + others[:2]
    return ok, [b for b in bad if b]


def test_fair_forms_accepted_and_near_misses_refused():
    random.seed(7)
    wrong = []
    for s in e.SKILLS:
        for d in (0, 1, 2):
            for _ in range(RUNS):
                q = e.call_generator(e.GENERATORS[s["key"]], d)
                at, a, tol = q.get("answer_type", "num"), q["answer"], q.get("tolerance", 0)
                ok, bad = variants(q)
                for v in ok:
                    if not e.check_answer(at, a, v, tol):
                        wrong.append("%s refuses %r for %r (%s)" % (s["key"], v, a, at))
                for v in bad:
                    if _same(at, a, v):
                        continue
                    if e.check_answer(at, a, v, tol):
                        wrong.append("%s accepts %r for %r (%s)" % (s["key"], v, a, at))
    assert not wrong, "\n".join(sorted(set(wrong))[:40])


def _same(at, a, v):
    """A bumped digit can land on an equal value ('-0'); that is not a near miss."""
    return at not in ("num", "int", "frac", "set", "coord", "time") and e._sn(a) == e._sn(v)
