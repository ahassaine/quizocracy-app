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


def test_natural_forms_of_an_answer():
    """Forms a child types that used to be refused: units, £ for pence, ≤/≥, ratio spaces, 24-hour times,
    remainders, am/pm spacing, a leading article, "and" in a list."""
    assert e.check_answer("num", 186, "£1.86", 0, "p") and not e.check_answer("num", 30, "£0.30")
    ok = [("num", 98, "98m²"), ("num", -5, "-5°C"), ("num", 40, "40%"),
          ("num", 3, "3 litres"), ("str", "25 r 3", "25r3"), ("str", "25 r 3", "25 remainder 3"),
          ("str", "10 am", "10am"), ("str", "x>=-1", "x ≥ -1"), ("str", "2:3", "2 : 3"),
          ("str", "09:45", "9:45"), ("str", "09:45", "9.45"), ("str", "045", "045°"),
          ("str", "elephant", "an elephant"), ("set", "2, 3, 5, 7", "2, 3, 5 and 7")]
    bad = [("num", 3, "4"), ("str", "x>=2", "x>=-2"), ("str", "13:20", "1:20"), ("num", 186, "£1.86"),
           ("str", "25 r 3", "25 r 4"), ("str", "2:3", "3:2")]
    assert [t for t in ok if not e.check_answer(*t)] == []
    assert [t for t in bad if e.check_answer(*t)] == []


def test_pie_answer_hidden_from_the_legend():
    spec = {"slices": [["A", 12], ["B", 30]], "highlight": 1}
    assert e.hide_pie_answer(spec, 30).get("hideValue") is True
    assert "hideValue" not in e.hide_pie_answer(spec, 90)            # the angle is asked, the value may show


def test_answer_shown_after_a_wrong_try():
    t = lambda a, p="Work it out.", at="num": e.answer_text({"answer": a, "prompt": p, "answer_type": at})
    assert t(26.0) == 26 and t(0.3333333333333333) == "1/3" and t(2.666667) == "2 2/3" and t(-0.5) == -0.5
    assert t(0.03156) == 0.03156 and t(0.30000000000000004) == 0.3 and t(7) == 7
    assert t(6.0, "Round 5.95 to one decimal place.") == "6.0"
    assert t(21.9, "Give your answer to 2 decimal places.") == "21.90"
    assert t(2.85, "It rounds to 2.9 to 1 decimal place. What is the smallest it could be?") == 2.85
    assert t(26.0, at="str") == 26.0          # only numbers are reformatted
    for key, fn in e.GENERATORS.items():      # the shown answer is always the stored one, re-marked
        for d in (0, 2):
            random.seed(f"{key}/{d}")
            q = e.call_generator(fn, d)
            shown = str(e.answer_text(q))
            if "/" not in shown:
                assert e.check_answer(q.get("answer_type", "num"), q["answer"], shown, q.get("tolerance", 0),
                                      (q.get("spec") or {}).get("unit")), (key, q["answer"], shown)
