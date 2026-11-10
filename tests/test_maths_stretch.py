"""Maths that stretches: a strong child climbs the tiers fast and tests out of skills, a school topic mixes the
skills of its strand, review questions say which year they come from, and column, long multiplication and long
division mistakes show their working laid out."""
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_maths_ladder import _run  # noqa: E402
from app.maths import maths_engine, maths_mastery as mm  # noqa: E402
from app.drills import maths as drill  # noqa: E402


async def _serve(year, ok=lambda key, tier: True):
    """One question as drills/maths serves and checks it: the tier from start_tier, a probe on a new skill."""
    key, reason = await mm.next_skill("sim", year)
    tier = await mm.start_tier("sim", year, key, await mm.skill_score("sim", key))
    if reason == "new" and await mm.probe("sim", year, key):
        tier = 2
    await mm.record_attempt("sim", key, ok(key, tier), tier=tier)
    return key, tier, reason


def _focus(monkeypatch, strands):
    async def f(pupil):
        return list(strands)
    monkeypatch.setattr(mm, "_focus_strand", f)


def test_strong_year8_reaches_two_step_and_brackets_within_15(monkeypatch):
    _focus(monkeypatch, ["8.7 Equations, inequalities & linear graphs"])
    for seed in range(12):
        random.seed(seed)

        async def go():
            return [await _serve(8) for _ in range(15)]
        served = _run(monkeypatch, go)
        keys = [k for k, _, _ in served]
        assert "Y8.7.c" in keys, (seed, keys)                        # equations with brackets
        assert any(k == "Y8.7.b" and t == 2 for k, t, _ in served), (seed, served)   # two-step (hard tier)
        assert keys.count("Y8.7.a") <= 5, (seed, keys)               # not nine "plot a point" in a row


def test_hard_tier_by_the_third_question_and_secure_in_four(monkeypatch):
    async def go():
        tiers = []
        for _ in range(4):
            t = await mm.start_tier("sim", 8, "Y8.0.a", await mm.skill_score("sim", "Y8.0.a"))
            tiers.append(t)
            m = await mm.record_attempt("sim", "Y8.0.a", True, tier=t)
        return tiers, m
    tiers, m = _run(monkeypatch, go)
    assert tiers == [1, 1, 2, 2], tiers
    assert m["score"] == mm.MASTERED and m.get("fast"), m


def test_a_slip_keeps_the_middle_tier_and_the_longer_road(monkeypatch):
    async def go():
        out = []
        for ok in (True, True, False, True):
            t = await mm.start_tier("sim", 8, "Y8.0.a", await mm.skill_score("sim", "Y8.0.a"))
            m = await mm.record_attempt("sim", "Y8.0.a", ok, tier=t)
            out.append(t)
        out.append(await mm.start_tier("sim", 8, "Y8.0.a", await mm.skill_score("sim", "Y8.0.a")))
        return out, m
    tiers, m = _run(monkeypatch, go)
    assert tiers[:3] == [1, 1, 2] and tiers[3] >= 1 and tiers[4] >= 1, tiers
    assert m["score"] < mm.MASTERED, m


def test_young_years_keep_their_gentle_start(monkeypatch):
    async def go():
        tiers = []
        for _ in range(3):
            t = await mm.start_tier("sim", 2, "Y2.0.a", await mm.skill_score("sim", "Y2.0.a"))
            tiers.append(t)
            await mm.record_attempt("sim", "Y2.0.a", True, tier=t)
        return tiers
    assert _run(monkeypatch, go)[0] == 0


def test_strong_child_tests_out_with_one_hard_question(monkeypatch):
    random.seed(3)

    async def go():
        return [await _serve(8) for _ in range(30)]
    served = _run(monkeypatch, go)
    probes = [k for k, t, r in served if r == "new" and t == 2]
    assert len(probes) >= 10, served                                  # skills opened (and secured) by one hard question
    assert len({k for k, _, _ in served}) >= 15


def test_four_operations_focus_mixes_the_strand(monkeypatch):
    _focus(monkeypatch, ["6.1 The four operations"])
    for seed in range(8):
        random.seed(seed)

        async def go():
            return [await _serve(6, ok=lambda k, t: random.random() < 0.7) for _ in range(15)]
        keys = [k for k, _, _ in _run(monkeypatch, go) if k.startswith("Y6.1.")]
        first10 = keys[:10]
        assert len(set(first10)) >= 3, (seed, first10)
        assert max(first10.count(k) for k in set(first10)) <= 5, (seed, first10)
        assert set(first10) & {"Y6.1.b", "Y6.1.c", "Y6.1.d", "Y6.1.e", "Y6.1.f"}, (seed, first10)


def test_review_tag_names_the_earlier_year():
    assert drill.review_tag("Y7.4.a", 8) == "Year 7 review"
    assert drill.review_tag("Y8.3.d", 9) == "Year 8 review"
    assert drill.review_tag("Y9.0.a", 9) is None
    assert drill.review_tag("Y6.1.a", 6) is None


def _sol(key, tier, want, tries=400):
    fn = maths_engine.GENERATORS[key]
    for _ in range(tries):
        q = maths_engine.present(maths_engine.call_generator(fn, tier), key)
        if want(q):
            return q
    raise AssertionError((key, tier))


def test_column_addition_shows_the_layout_and_carry():
    q = _sol("Y6.1.a", 1, lambda q: maths_engine.layout_for(q) and "+" in maths_engine.layout_for(q)["grid"])
    lay = maths_engine.layout_for(q)["grid"]
    lines = lay.splitlines()
    assert len({len(x) for x in lines}) == 1, lay                  # every line the same width: digits line up
    assert any(set(x.strip()) <= set("─-") for x in lines), lay      # the answer line


def test_long_multiplication_and_division_show_working():
    q = _sol("Y6.1.c", 1, lambda q: maths_engine.layout_for(q))
    lay = maths_engine.layout_for(q)["grid"]
    assert "×" in lay and len(lay.splitlines()) >= 5, lay          # two part-products and their sum
    q = _sol("Y6.1.f", 1, lambda q: maths_engine.layout_for(q))
    assert " ) " in maths_engine.layout_for(q)["grid"] and "÷" in maths_engine.layout_for(q)["say"]


def test_column_layout_values():
    def flat(d):
        return d["grid"].replace(" ", "")
    lay = maths_engine.column_layout(879242, "+", 42919)
    assert "879242" in flat(lay) and "922161" in flat(lay) and "111" in flat(lay)   # carries under the line
    assert "carried" in lay["say"]
    assert "3766" in flat(maths_engine.column_layout(5000, "−", 1234))
    lay = flat(maths_engine.long_mult_layout(2345, 37))
    assert "16415" in lay and "70350" in lay and "86765" in lay
    lay = flat(maths_engine.long_div_layout(7488, 24))
    assert "312" in lay and "72" in lay and "28" in lay and "48" in lay
    assert maths_engine.layout_for({"prompt": "Work out:   9,541 × 43", "answer": 410263,
                                    "solution": ["9,541 × 3 = 28,623.", "9,541 × 40 = 381,640."]})
    assert "2424" in flat(maths_engine.long_mult_layout(4738, 6))                   # short multiplication's carries
    three = maths_engine.layout_for({"prompt": "Work out:   348,402 + 276,083 + 822,646", "answer": 1447131})
    assert "348402" in flat(three) and "822646" in flat(three) and "1447131" in flat(three)
    place = {"key": "Y6.0.c", "strand": "6.0 Number & place value", "title": "Value of each digit"}
    assert maths_engine.layout_for({"prompt": "x", "answer": 1000, "solution": ["9,000 ÷ 9 = 1,000."]}, place) is None
    assert maths_engine.layout_for({"prompt": "Solve 3x + 4 = 19.", "answer": 5, "solution": ["3x = 15."]}) is None
    assert maths_engine.layout_for({"prompt": "Work out 2 + 3", "answer": 5, "solution": ["2 + 3 = 5."]}) is None
    assert maths_engine.layout_for({"prompt": "Work out:   86,830 + 14,263 − 13,257", "answer": 87836,
                                    "solution": ["86,830 + 14,263 = 101,093.", "101,093 − 13,257 = 87,836."]})


def test_negative_and_zero_powers_explain_the_reciprocal():
    fn, seen = maths_engine.GENERATORS["Y9.0.a"], 0
    for i in range(800):
        q = maths_engine.call_generator(fn, i % 3)
        m = re.search(r"(\d+)\^-(\d+)(?!\d)", q["prompt"])
        if not m or q["prompt"].startswith(("Simplify", "Work out %s^-1 +" % m.group(1))) or "×" in q["prompt"] \
                or "÷" in q["prompt"] or "?" in q["prompt"].split(".")[0]:
            continue
        b, n = int(m.group(1)), int(m.group(2))
        sol = " ".join(q["solution"])
        assert "1/%d^%d" % (b, n) in sol and "1/%d" % b ** n in sol, (q["prompt"], sol)   # 2^-3 = 1/2^3 = 1/8
        if n > 1 and b * n != b ** n:
            assert "Not 1/%d" % (b * n) in sol, sol                                          # why not 1/6
        seen += 1
    assert seen > 50
    steps, no = __import__("app.maths.y9_gen_a", fromlist=["_neg_steps"])._neg_steps(2, 3)
    assert steps[0].endswith("2^-3 = 1/2^3.") and "2 × 2 × 2 = 8" in steps[1] and "Not 1/6" in steps[2]
    assert "1/6" in no and "-8" in no


def test_a_likely_slip_gets_its_own_line_first(monkeypatch):
    stored = {}

    class Coll:
        async def update_one(self, q, upd, upsert=False):
            stored.update(upd["$set"], _id=q["_id"])

        async def find_one_and_update(self, q, upd):
            return dict(stored)

    class DB:
        maths_lab_q = Coll()
    monkeypatch.setattr(maths_engine, "db", DB())
    q = {"prompt": "Work out 2^-3 as a fraction.", "answer": "1/8", "answer_type": "frac", "spec": {"text": True},
         "solution": ["x"], "no": {"1/6": "You worked out 2 × 3 = 6."}}

    async def go():
        t = (await maths_engine.new_question("Y9.0.a", 1, pupil="sim", made=q))["token"]
        return await maths_engine.check(t, "1/6", "sim"), await maths_engine.check(t, "1 / 8", "sim")
    wrong, right = _run(monkeypatch, go)
    assert wrong["solution"][0] == "You worked out 2 × 3 = 6." and not wrong["correct"]
    assert right["correct"] and right["solution"][0] == "x"
