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
        f, pr = e._frac(a), q.get("prompt", "")
        if not (e._SIMPLEST.search(pr) or e._AS_MIXED.search(pr)):       # the form is the skill there
            ok += ["%d/%d" % (2 * f.numerator, 2 * f.denominator)]
        if f.denominator != 1 and abs(f) > 1 and f > 0 and not e._AS_IMPROPER.search(pr):
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
                at, a, tol, pr = q.get("answer_type", "num"), q["answer"], q.get("tolerance", 0), q["prompt"]
                ok, bad = variants(q)
                for v in ok:
                    if not e.check_answer(at, a, v, tol, None, pr):
                        wrong.append("%s refuses %r for %r (%s)" % (s["key"], v, a, at))
                for v in bad:
                    if _same(at, a, v):
                        continue
                    if e.check_answer(at, a, v, tol, None, pr):
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
                                      (q.get("spec") or {}).get("unit"), q["prompt"]), (key, q["answer"], shown)


def _marks(cases):
    """[(answer_type, expected, typed, prompt, right?)] -> the cases marked the other way."""
    return [c for c in cases if e.check_answer(c[0], c[1], c[2], 0, None, c[3]) != c[4]]


def test_algebra_in_another_order():
    assert _marks([
        ("str", "11a+11b", "11b+11a", "Simplify 5a + 5b + 6a + 6b", True),
        ("str", "5x+30", "30 + 5x", "Expand 5(x + 6)", True), ("str", "9n+8", "8+9n", "nth term", True),
        ("str", "C=7m+14", "C = 14 + 7m", "Write a formula for C", True),
        ("str", "x^2+22x+121", "121+22x+x²", "Expand (x+11)²", True), ("str", "5y-35", "-35+5y", "Expand", True),
        ("str", "y=-4x-2", "y=-2-4x", "Find the equation", True), ("str", "12a", "12×a", "Simplify 15a − 3a", True),
        ("str", "C=7m+14", "C=14+8m", "", False), ("str", "y=-4x-2", "x=-2-4y", "", False),
        ("str", "5x+30", "5x+6", "", False), ("str", "kite", "tike", "", False),      # a word is not a product
    ]) == []


def test_number_forms():
    assert _marks([
        ("int", -13, "x = -13", "Solve 8x = -104", True), ("int", -13, "y = -13", "Solve 8x = -104", False),
        ("num", 218.96, "$218.96", "How many dollars?", True), ("num", 5, "€5", "", True),
        ("int", 300000, "3x10^5", "How many times bigger?", True), ("int", 300000, "3 × 10⁵", "", True),
        ("int", 300000, "3x10^4", "", False),
        ("num", 0.15, "3/20", "Find the value of x.", True), ("num", 1.5, "1 1/2", "What is its gradient?", True),
        ("num", 0.15, "3/20", "Give your answer as a decimal.", False),
        ("num", 2.5, "5/2", "Round to 1 decimal place.", False), ("int", 6, "6/7", "", False),
    ]) == []


def test_word_answers_with_a_fair_extra_word_or_synonym():
    assert _marks([
        ("str", "half", "half turn", "Is it a quarter, half or three-quarter turn?", True),
        ("str", "half", "a half turn", "", True), ("str", "whole", "full turn", "", True),
        ("str", "three-quarter", "three quarters", "", True), ("str", "three-quarter", "3/4", "", True),
        ("str", "acute", "an acute angle", "", True), ("str", "equilateral", "equilateral triangle", "", True),
        ("str", "square-based pyramid", "square pyramid", "", True), ("str", "rectangle", "oblong", "", True),
        ("str", "cuboid", "rectangular prism", "", True), ("str", "Wed", "Wednesday", "", True),
        ("str", "September", "Sept", "", True), ("str", "fell", "it fell", "", True),
        ("str", "two thousand nine hundred and ninety-nine", "two thousand nine hundred and ninety-nine pounds",
         "Amina is filling in a cheque for £2,999. Write that amount in words.", True),
        ("str", "metres", "m", "", True), ("str", "cm", "centimetres", "", True), ("str", "grams", "g", "", True),
        ("str", "rectangle", "rectangles", "", True), ("str", "Cats", "Cat", "", True),
        ("str", "compasses", "a pair of compasses", "", True), ("str", "compasses", "compass", "", True),
        ("str", "ones", "ones place", "", True),
        ("str", "half", "quarter turn", "", False), ("str", "acute", "obtuse angle", "", False),
        ("str", "square-based pyramid", "triangular pyramid", "", False), ("str", "Wed", "Thursday", "", False),
        ("str", "rose", "it fell", "", False), ("str", "grams", "kg", "", False), ("str", "tens", "ten", "", False),
    ]) == []


def test_sets_with_thousands_commas():
    assert _marks([
        ("set", "6184930, 7518249", "6,184,930, 7,518,249", "", True),
        ("set", "6184930, 7518249", "7,518,249 and 6,184,930", "", True),
        ("set", "6184930, 7518249", "6184930; 7518249", "", True), ("set", "90, 92, 94", "90,92,94", "", True),
        ("set", "6184930, 7518249", "6,184,930", "", False), ("set", "6184930, 7518249", "6,184,931, 7,518,249", "", False),
    ]) == []
    assert e.answer_text({"answer": "6184930, 7518249", "answer_type": "set"}) == "6,184,930; 7,518,249"
    assert e.answer_text({"answer": "90, 92, 94", "answer_type": "set"}) == "90, 92, 94"


def test_fractions_in_the_asked_form():
    simplest = "Work out 4/5 − 2/5. Give your answer as a fraction in its simplest form."
    mixed = "Give your answer as a mixed number in its simplest form."
    assert _marks([
        ("frac", "2/5", "4/10", simplest, False), ("frac", "2/5", "0.4", simplest, False),
        ("frac", "2/5", "2/5", simplest, True), ("frac", "1/10", "10/100", "Write 10% as a fraction in its simplest form.", False),
        ("frac", "6 2/5", "32/5", mixed, False), ("frac", "6 2/5", "6 4/10", mixed, False),
        ("frac", "6 2/5", "6.4", mixed, False), ("frac", "6 2/5", "6 2/5", mixed, True),
        ("frac", "3/6", "3/6", "Write 2/4 in its lowest terms, then shade this area model of 6 equal parts", True),
        ("frac", "1/25", "0.04", "Write 0.04 as a fraction.", False), ("frac", "1/25", "4/100", "Write 0.04 as a fraction.", True),
        ("frac", "29/6", "4 5/6", "Write the mixed number 4 5/6 as an improper fraction.", False),
        ("frac", "29/6", "29/6", "Write the mixed number 4 5/6 as an improper fraction.", True),
        ("frac", "7/2", "3 1/2", "5 1/2 + ___ = 9. What is the missing number? (fraction or mixed number)", True),
        ("frac", "1", "1.0", "What is k? (give a fraction or decimal)", True),
        ("frac", "-6/5", "−6/5", "", True), ("frac", "1/2", "½", "", True), ("frac", "5/2", "2½ pizzas", "", True),
    ]) == []
    assert e.form_hint("frac", "2/5", "4/10", simplest) == "Right value — now simplify it."
    assert e.form_hint("frac", "2/5", "3/10", simplest) == ""            # a wrong value gets no hint


def test_12_and_24_hour_times():
    to12 = "A programme starts at 13:15 in 24-hour time. Write that time as a 12-hour time (h:mm)."
    to24 = "Train 1 leaves at 15:00 and the journey takes 45 minutes. What time does it arrive? Write it as a 24-hour time (hh:mm)."
    dur = "Write 195 minutes as hours and minutes in the form h:mm (for example 2:15 means 2 hours 15 minutes)."
    assert _marks([
        ("time", "1:15", "13:15", to12, False), ("time", "1:15", "1:15am", to12, False),
        ("time", "1:15", "1:15 p.m.", to12, True), ("time", "1:15", "1.15", to12, True),
        ("time", "12:23", "00:23", "A night bus leaves at 00:23 in 24-hour time. Write that as a 12-hour time (h:mm).", False),
        ("time", "15:45", "3:45", to24, False), ("time", "15:45", "3:45 pm", to24, False), ("time", "15:45", "15.45", to24, True),
        ("time", "13:00", "1 pm", "At what time was it warmest? (type the time, like 10:00)", True),
        ("time", "08:00", "8:00", "At what time was it coldest?", True),
        ("time", "3:15", "15:15", dur, False), ("time", "3:15", "3:15", dur, True),
        ("time", "8:30", "20:30", "Ben goes to bed at half past 8 in the evening. Set the clock.", True),
    ]) == []


def test_ordinals_in_figures():
    fig = "Write the ordinal number for position 71 (in figures, e.g. 4th)."
    assert _marks([
        ("str", "71st", "71th", fig, False), ("str", "71st", "71", fig, False), ("str", "71st", "71st", fig, True),
        ("str", "13th", "13rd", "", False), ("str", "3rd", "3", "Who finished 3rd?", True),
        ("str", "3rd", "third", "Who finished?", True), ("str", "3rd", "3 rd", "", True),
    ]) == []


def test_rounding_claim_keeps_its_trailing_zero():
    """Y8.0.c "Sara says 356.03693 rounded to 1 d.p. is 356": no — to 1 d.p. it is 356.0."""
    from decimal import Decimal, ROUND_HALF_UP
    random.seed(11)
    seen = 0
    for _ in range(3000):
        q = e.call_generator(e.GENERATORS["Y8.0.c"], random.choice((0, 1, 2)))
        m = re.match(r"\w+ says ([\d.]+) rounded to (\d) d\.p\. is ([\d.]+)\.", q["prompt"])
        if not m:
            continue
        seen += 1
        x, dp, said = Decimal(m.group(1)), int(m.group(2)), m.group(3)
        right = format(x.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP), "f")
        assert q["answer"] == ("yes" if said == right else "no"), q["prompt"]
    assert seen > 20


def test_a_typed_unit_must_agree_with_the_question():
    """A unit of the same kind but another size is wrong; only money converts ("£1.86" for 186p)."""
    grams = "How many grams are there in 8 kilograms?"
    cases = [(8000, "8000 g", None, grams, True), (8000, "8000", None, grams, True), (8000, "8000 grams", None, grams, True),
             (8000, "8000 kg", None, grams, False), (8000, "8 kg", None, grams, False),
             (420, "420 m", "cm", "Add 1 m 68 cm and 2 m 52 cm. Give your answer in cm.", False),
             (40, "40 mm", "cm", "How long is the line, in millimetres?", True),
             (40, "40 m", "cm", "How long is the line, in millimetres?", False),
             (38, "£38", "p", "A rubber costs 21p and a pencil 17p. How much in pence?", False), (38, "38p", "p", "", True),
             (186, "£1.86", "p", "", True), (12, "12p", "£", "How many pounds does each person get?", False),
             (12, "£12", "£", "", True), (3, "3 ml", "litres", "", False), (3, "3 litres", "litres", "", True),
             (98, "98 cm²", "m²", "", False), (98, "98m²", "m²", "", True), (30, "30 pupils", None, "", True),
             (210, "210 hours", "minutes", "How many minutes are in 3 hours 30 minutes?", False), (-5, "-5°C", "°C", "", True)]
    assert [c for c in cases if e.check_answer("num", c[0], c[1], 0, c[2], c[3]) != c[4]] == []


def test_cafe_cakes_answer_is_a_mixed_number():
    random.seed(4)
    for _ in range(300):
        q = e.call_generator(e.GENERATORS["Y5.5.c"], 1)
        if "café" in q["prompt"]:
            f = e._frac(q["answer"])
            assert " " in q["answer"] and not e.check_answer("frac", q["answer"], "%d/%d" % (f.numerator, f.denominator),
                                                               0, None, q["prompt"])
