"""Pre-launch review, maths: templates that did not practise their skill (or sat below its year) are gone or fixed;
"secure" at the hardest tier needs 3 right in a row of at least 2 kinds of question, and a skill that was secure
stays secure; a fraction answer is always shown with its simplest form, an unsimplified right answer is accepted
when the question doesn't ask for the simplest form (and the feedback shows it), and gets "Nearly: simplify it"
with one retry when it does."""
import asyncio
import concurrent.futures
import os
import random
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_maths_ladder import _run  # noqa: E402
from app.maths import maths_engine as me, maths_mastery as mm  # noqa: E402

RUNS = 300


def _prompts(key, tiers=(0, 1, 2), n=RUNS):
    random.seed(11)
    return [(d, q) for d in tiers for q in (me.call_generator(me.GENERATORS[key], d) for _ in range(n))]


# ------------------------------------------------------------------ off-skill templates ----
# (skill, tiers, a pattern no prompt may match): the report's examples and the audit's main fixes
GONE = [
    ("Y6.1.f", (0, 1, 2), r"^Find the missing number:\s+___ ÷"),          # long division served as a multiplication
    ("Y6.1.f", (0, 1, 2), r"Check it: what is"),
    ("Y4.3.a", (0, 1, 2), r"2 × 2\b|\b2 equal groups with 2\b|\b2 rows with 2\b"),   # Y4 facts as Y1 work
    ("Y4.9.c", (0, 1, 2), r"TALLEST|SHORTEST"),                            # Y4 bar charts as Y2 work
    ("Y5.8.c", (2,), r"How many degrees bigger is an angle of|What is the difference in degrees"),   # a subtraction
    ("Y5.4.j", (2,), r"\b\d{3,}p\b"),                                      # "12 apples cost 1008p"
    ("Y5.4.b", (1,), r"\b\d{3,}p\b"),
    ("Y8.8.k", (1, 2), r"\(scale factor \d+\)"),                           # the method given away
    ("Y8.8.d", (0, 1, 2), r"How many (sides|vertices)"),
    ("Y8.3.h", (0, 1, 2), r"The reciprocal of \d+ is 1/\d+\. The number line"),
    ("Y6.9.e", (0, 1, 2), r"Which bar is the (TALLEST|SHORTEST)"),
    ("Y6.8.e", (0, 1, 2), r"BIGGER is the larger angle"),
    ("Y3.0.a", (1,), r"in (1|2|5|10)s from"),
    ("Y3.7.e", (0, 1, 2), r"brick|feather|bus or pencil|Compare the size"),
    ("Y3.8.f", (0, 1, 2), r"season"),
    ("Y1.2.a", (0, 1, 2), r"\bdogs\b|\bcars\b"),                            # counting in 4s is Year 3
    ("Y2.4.a", (0, 1, 2), r"degrees colder was|How much do \d+ buckets hold"),
    ("Y7.5.h", (0, 1, 2), r"Shade a shape with an area of"),
    ("Y7.9.f", (0, 1, 2), r"How many pupils are there altogether|How many more pupils|In which month were the most"),
    ("Y9.9.d", (0, 1, 2), r"How many more chose"),
]


@pytest.mark.parametrize("key,tiers,rx", GONE)
def test_off_skill_template_is_gone(key, tiers, rx):
    hits = [q["prompt"] for d, q in _prompts(key, tiers) if re.search(rx, str(q["prompt"]))]
    assert not hits, (key, hits[:3])


def test_long_division_divides_by_two_digits():
    """Y6.1.f: every bar model divides by a 2-digit number (short division by 3 was served)."""
    parts = [q["spec"].get("parts") for _, q in _prompts("Y6.1.f") if q.get("component") == "strip_model"]
    assert parts and min(parts) >= 11, parts[:10]


def test_three_digit_addition_hard_tier_bars_are_not_round():
    """Y3.3.b hard tier: a bar chart carries 3-digit numbers to add, not 400 + 520 read off the gridlines."""
    vals = [v for _, q in _prompts("Y3.3.b", (2,)) if q.get("component") == "bar_chart" for v in q["spec"]["values"]]
    assert vals and not all(v % 10 == 0 for v in vals), vals[:10]


def test_every_answer_still_marks_itself():
    random.seed(12)
    bad = []
    for s in me.SKILLS:
        for d in (0, 1, 2):
            for _ in range(40):
                q = me.call_generator(me.GENERATORS[s["key"]], d)
                at = q.get("answer_type", "num")
                if at in ("num", "int", "frac", "str") and not me.check_answer(
                        at, q["answer"], str(q["answer"]), q.get("tolerance", 0), None, q["prompt"]):
                    bad.append("%s d%d %r" % (s["key"], d, q["answer"]))
    assert not bad, bad[:20]


# ------------------------------------------------------------------ mastery evidence ----
def _record(answers, key="Y6.2.c"):
    async def go():
        out = []
        for ok, tier, shape in answers:
            m = await mm.record_attempt("sim", key, ok, tier=tier, shape=shape)
            out.append(m["score"] >= mm.MASTERED)
        return out
    return go


def test_secure_at_the_hardest_tier_needs_three_of_two_kinds(monkeypatch):
    assert _run(monkeypatch, _record([(True, 2, "a"), (True, 2, "b")])) == [False, False]
    assert _run(monkeypatch, _record([(True, 2, "a"), (True, 2, "b"), (True, 2, "b")]))[-1]
    assert not _run(monkeypatch, _record([(True, 2, "a")] * 3))[-1]             # one kind three times: not yet
    # a middle-tier answer breaks the run: 2 hard after it are not 3
    assert not _run(monkeypatch, _record([(True, 2, "a"), (True, 1, "b"), (True, 2, "b"), (True, 2, "a")]))[-1]


def test_a_skill_that_was_secure_stays_secure(monkeypatch):
    """Progress saved under the old rule (secure after 2 hard right, no kinds stored) is not undone."""
    async def go():
        await mm.db.maths_mastery.update_one({"_id": "sim:Y6.2.d"}, {"$set": {
            "pupil": "sim", "skill": "Y6.2.d", "score": 100, "streak": 2, "attempts": 2, "correct_count": 2,
            "hard": 2, "fast": True, "mastered_at": mm._now(), "last": mm._now()}}, upsert=True)
        before = await mm.progress("sim", 6)
        m = await mm.record_attempt("sim", "Y6.2.d", True, tier=2, shape="a")
        return before, m, await mm.progress("sim", 6)
    before, m, after = _run(monkeypatch, go)
    assert m["score"] == mm.MASTERED and m["mastered"], m
    assert before["mastered"] == after["mastered"] == 1


# ------------------------------------------------------------------ fractions in their simplest form ----
@pytest.mark.parametrize("given,want", [("12/28", "3/7"), ("6/6", "1"), ("9/9", "1"), ("3 2/4", "3 1/2"),
                                        ("14/4", "7/2"), ("−4/8", "-1/2"), ("2 5/4", "3 1/4"), ("3/7", None),
                                        ("5", None), ("0.5", None), ("7/2", None)])
def test_simplest(given, want):
    assert me.simplest(given) == want


class _Q:
    """maths_lab_q in memory: the calls maths_engine.new_question and check make."""
    def __init__(self):
        self.docs = {}

    async def update_one(self, flt, upd, upsert=False):
        d = self.docs.setdefault(flt["_id"], {"_id": flt["_id"]}) if upsert else self.docs.get(flt["_id"])
        if d is not None:
            d.update(upd.get("$set", {}))

    async def find_one_and_update(self, flt, upd):
        d = self.docs.get(flt["_id"])
        if not d or d.get("pupil") != flt.get("pupil") or d.get("done"):
            return None
        out = dict(d)
        d.update(upd.get("$set", {}))
        return out


class _EDB:
    def __init__(self):
        self.maths_lab_q = _Q()


def _serve_and_check(monkeypatch, q, values):
    monkeypatch.setattr(me, "db", _EDB())
    monkeypatch.setitem(me.GENERATORS, "Ztest", lambda d=1: dict(q))

    async def go():
        served = await me.new_question("Ztest", 1, pupil="sim")
        doc = me.db.maths_lab_q.docs[served["token"]]
        return doc, [await me.check(served["token"], v, "sim") for v in values]
    with concurrent.futures.ThreadPoolExecutor(1) as ex:
        return ex.submit(asyncio.run, go()).result()


def test_unsimplified_answer_is_shown_with_its_simplest_form(monkeypatch):
    q = {"prompt": "A box holds 28 counters and 12 of them are green. What fraction of the counters are green?",
         "answer": "12/28", "answer_type": "frac", "solution": ["12 of the 28 counters are green: 12/28."]}
    doc, (res,) = _serve_and_check(monkeypatch, q, ["5/28"])
    assert doc["display"] == "12/28 = 3/7"
    assert res["correct"] is False and res["expected"] == "12/28 = 3/7"
    assert res["solution"][-1] == "12/28 = 3/7 in its simplest form."


def test_the_why_is_not_told_twice(monkeypatch):
    q = {"prompt": "Shade 3 of the 6 parts. What fraction is shaded?", "answer": "3/6", "answer_type": "frac",
         "solution": ["3 of 6 parts are shaded: 3/6 = 1/2."]}
    doc, _ = _serve_and_check(monkeypatch, q, [])
    assert doc["solution"] == q["solution"]


def test_unsimplified_right_answer_accepted_when_not_asked(monkeypatch):
    q = {"prompt": "What is 2/7 + 4/14? Write the answer as a fraction.", "answer": "4/7", "answer_type": "frac",
         "solution": ["4/14 = 2/7, so 2/7 + 2/7 = 4/7."]}
    _, (res,) = _serve_and_check(monkeypatch, q, ["8/14"])
    assert res["correct"] is True
    assert res["hint"] == "8/14 = 4/7 in its simplest form."
    _, (res,) = _serve_and_check(monkeypatch, q, ["4/7"])
    assert res["correct"] is True and "hint" not in res


def test_simplest_form_asked_gets_nearly_and_one_retry(monkeypatch):
    q = {"prompt": "Write 12/28 in its simplest form.", "answer": "3/7", "answer_type": "frac",
         "solution": ["12 and 28 can both be divided by 4: 12/28 = 3/7."]}
    _, (first, second) = _serve_and_check(monkeypatch, q, ["6/14", "3/7"])
    assert first["retry"] and first["hint"] == "Nearly: simplify it." and not first["correct"]
    assert second["correct"] is True
    _, (first, second) = _serve_and_check(monkeypatch, q, ["6/14", "6/14"])
    assert second["correct"] is False and second["solution"][0] == me.SIMPLIFY_HINT
    _, (res,) = _serve_and_check(monkeypatch, q, ["2/7"])                         # a wrong value: no retry
    assert res["correct"] is False and not res.get("retry")


def test_simplest_form_questions_store_the_simplest_answer():
    """A typed question that asks for the simplest form has its answer in the simplest form."""
    random.seed(13)
    bad = []
    for s in me.SKILLS:
        if s["key"] in mm.OUT_OF_YEAR:
            continue
        for d in (0, 1, 2):
            for _ in range(60):
                q = me.call_generator(me.GENERATORS[s["key"]], d)
                if (q.get("component") or "number") == "number" and me._SIMPLEST.search(str(q["prompt"])) \
                        and me.simplest(str(q["answer"])):
                    bad.append("%s %r %s" % (s["key"], q["answer"], q["prompt"][:80]))
    assert not bad, bad[:10]
