"""Wave 7, maths and grammar content: a placement probe needs 3 hard questions right in a row, of 2 kinds (pre-launch
review; it was 2), and the
page says so; one kind of question at most twice per skill in a sitting, with the tickets bar chart worded several
ways; decimal whys line up the points (0.9 = 0.90) and the classic slip gets its own line; after slips the maths
drops one tier at most, with one line saying so, and Year 8's easiest decimals are still Year 8 ones; no array to
build over 30 counters or from Year 4; Year 1-2 "rows of" problems get the rows drawn; a rewritten sentence with a
slip in a word the task did not ask to change gets "Nearly"."""
import datetime
import os
import random
import re
import sys

import requests

from conftest import BASE, DB, add_child, enter_child, signup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_maths_ladder import _run  # noqa: E402
from app.bank import engine as bank  # noqa: E402
from app.drills import maths as drill, typos  # noqa: E402
from app.maths import maths_engine as me, maths_mastery as mm  # noqa: E402


# ------------------------------------------------------------------ placement ----
def test_a_placement_probe_needs_three_hard_right_in_a_row_of_two_kinds(monkeypatch):
    async def go(answers):
        await mm.db.maths_mastery.update_one({"_id": "sim:Y6.2.a"}, {"$set": {"pupil": "sim", "skill": "Y6.2.a",
                                                                               "probing": True}}, upsert=True)
        out = []
        for ok, shape in answers:
            t = await mm.start_tier("sim", 6, "Y6.2.a", await mm.skill_score("sim", "Y6.2.a"))
            m = await mm.record_attempt("sim", "Y6.2.a", ok, tier=t, shape=shape)
            out.append((t, m["score"] >= mm.MASTERED, m.get("probing")))
        return out
    two = _run(monkeypatch, lambda: go([(True, "a"), (True, "b")]))
    assert two == [(2, False, True), (2, False, True)], two      # one or two right answers are never "secure"
    three = _run(monkeypatch, lambda: go([(True, "a"), (True, "b"), (True, "a")]))
    assert three[2] == (2, True, False), three                   # the third hard one right, 2 kinds: secure
    same = _run(monkeypatch, lambda: go([(True, "a"), (True, "a"), (True, "a")]))
    assert same[2] == (2, False, True), same                     # 3 of one kind: not yet, the probe goes on
    same = _run(monkeypatch, lambda: go([(True, "a"), (True, "a"), (True, "a"), (True, "b")]))
    assert same[3][1], same                                      # ... a fourth of another kind secures it
    slip = _run(monkeypatch, lambda: go([(True, "a"), (False, "b"), (True, "c")]))
    assert slip[1][1:] == (False, False) and not slip[2][1], slip  # a miss ends the probe: the usual road


def test_after_one_slip_four_hard_right_of_two_kinds(monkeypatch):
    async def go(answers):
        out = []
        for ok, shape in answers:
            m = await mm.record_attempt("sim", "Y6.2.b", ok, tier=2, shape=shape)
            out.append(m["score"] >= mm.MASTERED)
        return out
    got = _run(monkeypatch, lambda: go([(False, "a"), (True, "a"), (True, "b"), (True, "a"), (True, "b")]))
    assert got == [False, False, False, False, True], got


def test_the_page_says_the_real_rule():
    page = open(os.path.join(os.path.dirname(__file__), "..", "app", "templates", "child_detail.html")).read()
    rule = re.search(r'testid="mastery-rule"\) %}(.*?){% endcall %}', page, re.S).group(1)
    for words in ("5 right in a row", "7 after one wrong answer", "3 of the hardest right in a row",
                  "of at least 2 different kinds of question", "4 after one wrong answer",
                  "one or two right answers are never enough", "re-checked on a later day"):
        assert words in rule, words
    assert mm.FAST_STREAK == 5 and mm.HARD_RIGHT == 3 and mm.HARD_KINDS == 2
    helps = open(os.path.join(os.path.dirname(__file__), "..", "app", "templates", "help.html")).read()
    assert "3 of the hardest questions right in a row, of at least 2 different kinds" in helps


# ------------------------------------------------------------------ easier after slips ----
def test_after_a_slip_the_drop_is_one_tier_and_said(monkeypatch):
    async def go():
        await mm.record_attempt("sim", "Y8.2.a", True, tier=2)
        await mm.record_attempt("sim", "Y8.2.a", False, tier=2)
        await mm.record_attempt("sim", "Y8.2.a", False, tier=2)       # the score falls far: the tier does not
        t = await mm.start_tier("sim", 8, "Y8.2.a", 5)
        return t, await mm.eased("sim", "Y8.2.a", t)
    t, eased = _run(monkeypatch, go)
    assert t == 1 and eased, (t, eased)
    assert mm.ease_note("Add and subtract decimals") == "Let's go over decimals with an easier one."
    assert mm.ease_note("Divisibility rules") == "Let's go over dividing with an easier one."


def test_year8_easiest_decimals_are_year8_ones():
    random.seed(8)
    for _ in range(300):
        q = me.call_generator(me.GENERATORS["Y8.2.a"], 0)
        assert q.get("component") != "number_line", q["prompt"]      # no "0.5 + 0.4 on a number line" for Year 8


def test_decimal_whys_line_up_the_points():
    q = {"prompt": "A plank of wood is 3.95 m long. Tom cuts 0.9 m off the end. How long is the plank now?",
         "component": "number", "spec": {"unit": "m"}, "answer": 3.05, "answer_type": "num",
         "solution": ["3.95 − 0.9 = 3.05."]}
    q = me.present(q, "Y8.2.a")
    assert q["solution"][0] == "Line up the decimal points: 0.9 = 0.90, so work out 3.95 − 0.90."
    assert "3.86" in q["no"] and "0.9 is 0.90" in q["no"]["3.86"]
    random.seed(4)
    for key in ("Y4.6.i", "Y5.6.f", "Y6.5.d", "Y7.5.a", "Y8.2.a"):
        for d in (0, 1, 2):
            for _ in range(40):
                g = me.present(me.call_generator(me.GENERATORS[key], d), key)
                sol = " ".join(s for s in g.get("solution", []) if isinstance(s, str))
                if re.search(r"\d\.\d+ [+−] \d", sol) and "£" not in sol:
                    assert "line" in sol.lower() and "point" in sol.lower(), (key, g["prompt"], sol)


# ------------------------------------------------------------------ one kind at most twice ----
def test_the_tickets_bar_chart_has_several_wordings_and_one_kind():
    random.seed(6)
    seen = set()
    for _ in range(400):
        q = me.call_generator(me.GENERATORS["Y6.1.a"], 1)
        if q.get("component") == "bar_chart":
            seen.add(re.sub(r"[A-Z][a-z]+(?= |\?|$)", "W", re.sub(r"\d", "#", q["prompt"]))[:45])
            assert me.template_shape(q, "Y6.1.a") == "bar_chart"
            assert me.check_answer(q["answer_type"], q["answer"], str(q["answer"]))
    assert len(seen) >= 6, seen


def _kid(page, name, year):
    signup(page)
    pid = add_child(page, name, year)
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {"maths": {"on": True, "target": 10}}},
                                        "$unset": {"plan_log": "", "focus": ""}})
    enter_child(page, name)
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return pid, s


def _only_skill(pid, year, keep):
    """Every other skill of the year secure (and not due for review), so the ladder asks `keep`."""
    now = datetime.datetime.utcnow()
    for s in me.skill_list():
        if s["key"].startswith("Y%d." % year) and s["key"] != keep:
            DB.maths_mastery.update_one({"_id": "%s:%s" % (pid, s["key"])}, {"$set": {
                "pupil": pid, "skill": s["key"], "score": 100, "streak": 5, "attempts": 5, "correct_count": 5,
                "last": now, "mastered_at": now}}, upsert=True)


def test_one_kind_of_question_at_most_twice_per_skill(page):
    pid, s = _kid(page, "Omar", 6)
    _only_skill(pid, 6, "Y6.1.a")
    kinds = []
    for _ in range(18):
        q = s.post(BASE + "/api/maths/next", json={}).json()
        assert q.get("ok") and q["skill"] == "Y6.1.a", q
        kinds.append(q["component"])
        s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": "1"})      # wrong: the skill stays open
    for k in ("bar_chart", "data_table", "io_table"):
        assert kinds.count(k) <= drill.TEMPLATE_CAP, kinds


def test_an_easier_question_after_a_slip_says_so(page):
    pid, s = _kid(page, "Josh", 7)          # Year 7: no earlier KS3 skills mixed in
    _only_skill(pid, 7, "Y7.5.a")
    DB.maths_mastery.update_one({"_id": "%s:Y7.5.a" % pid}, {"$set": {
        "pupil": pid, "skill": "Y7.5.a", "score": 3, "streak": 0, "attempts": 1, "correct_count": 0, "tier": 1,
        "last": datetime.datetime.utcnow()}}, upsert=True)
    q = s.post(BASE + "/api/maths/next", json={}).json()
    assert q["skill"] == "Y7.5.a" and q.get("ease") == "Let's go over decimals with an easier one.", q
    assert DB.maths_lab_q.find_one({"_id": q["token"]})["difficulty"] == 0       # one tier below the last
    s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": "1"})   # wrong again at the same tier
    nxt = s.post(BASE + "/api/maths/next", json={}).json()
    assert nxt["skill"] == "Y7.5.a" and not nxt.get("ease"), nxt                 # said once, not after every miss


# ------------------------------------------------------------------ pictures ----
def test_no_array_to_build_when_big_or_from_year4():
    random.seed(11)
    built = drawn = 0
    for s in me.SKILLS:
        for d in (0, 1, 2):
            for _ in range(40):
                g = me.call_generator(me.GENERATORS[s["key"]], d)
                if g.get("component") != "array":
                    continue
                q = me.present(g, s["key"])
                sp = q["spec"]
                if sp.get("mode", "build") == "build":
                    built += 1
                    assert sp["targetRows"] * sp["targetCols"] <= me.BUILD_CELLS and int(s["key"][1]) <= 3, \
                        (s["key"], q["prompt"])
                else:
                    drawn += 1
                    assert not re.search(r"\bbuild\b", q["prompt"], re.I), (s["key"], q["prompt"])
                    assert me.check_answer(q["answer_type"], q["answer"], str(q["answer"]))
    assert built and drawn
    q = me.present({"prompt": "Build an array that shows 11 × 9, then type the product.", "component": "array",
                    "spec": {"mode": "build", "maxRows": 12, "maxCols": 12, "targetRows": 11, "targetCols": 9},
                    "answer": 99, "answer_type": "int", "solution": ["11 × 9 = 99."]}, "Y6.1.b")
    assert q["prompt"] == "Look at the array that shows 11 × 9, then type the product."
    assert q["spec"]["mode"] == "read" and q["answer"] == 99


def test_year1_rows_of_chairs_have_the_rows_drawn():
    random.seed(1)
    found = 0
    for _ in range(600):
        g = me.call_generator(me.GENERATORS["Y1.2.a"], 1)
        if g["prompt"].startswith("Chairs are put in"):
            q = me.present(g, "Y1.2.a")
            r, c = map(int, re.findall(r"\d+", q["prompt"])[:2])
            assert q["component"] == "array" and q["spec"]["mode"] == "read", q
            assert (q["spec"]["rows"], q["spec"]["cols"]) == (r, c) and q["answer"] == r * c
            found += 1
    assert found


# ------------------------------------------------------------------ grammar ----
def test_a_rewrite_with_a_slip_in_an_unchanged_word_is_nearly():
    sk = bank.skill("GP6.17")
    q = next(q for q in sk["qs"] if q["id"] == "0eed89d47b0d")       # Sam should tidies his room.
    key = bank.serve(q)[1]
    assert bank.slips(key, "Sam shuold tidy his room.", q["q"], sk) == [("shuold", "should")]
    assert bank.slips(key, "Sam shuold tidies his room.", q["q"], sk) == []      # the grammar is wrong too
    assert bank.slips(key, "Sam should tidi his room.", q["q"], sk) == []        # the word the task changes
    assert bank.slips(key, "Sam should tidy his rooom.", q["q"], sk) == []       # a doubled letter: not inner_slip
    assert typos.corrections([("shuold", "should")]) == "'shuold' should be 'should'."


def test_the_rewrite_slip_gets_its_retry_in_the_app(page):
    signup(page)
    pid = add_child(page, "Arjun", 6)
    enter_child(page, "Arjun")
    sk = bank.skill("GP6.17")
    q = next(q for q in sk["qs"] if q["id"] == "0eed89d47b0d")
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    tok = "w7-" + pid
    DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": "grammar",
                         "answer": bank.serve(q)[1], "meta": {"skill": sk["key"], "qid": q["id"], "reason": "new"},
                         "created": datetime.datetime.utcnow(), "done": False})
    r = page.request.post(BASE + "/api/grammar/check", data={"token": tok, "value": "Sam shuold tidy his room."}).json()
    assert r["ok"] and r["retry"] and r["hint"] == typos.RETRY
    r = page.request.post(BASE + "/api/grammar/check", data={"token": tok, "value": "Sam should tidy his room."}).json()
    assert r["ok"] and r["correct"]
