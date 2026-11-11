"""Wave 6, maths: a decimal comma is "Nearly" with a retry (thousands commas stay thousands); a chart label is
matched without case and with a word copied from the chart ("class 3a" for 3A); Years 1-2 whys explain with
counting and × (no ÷ for a missing factor, a reason for the bigger fraction, never the bare answer); after the
Year 4 check the first look is the missed fact itself, and the gap is filled with at most 5 questions from its
tables before other practice."""
import datetime
import os
import re
import sys

from conftest import BASE, DB, add_child, enter_child, signup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills.tables import NEAR_RUN  # noqa: E402
from app.maths import maths_engine as me  # noqa: E402
from test_put_right import _check, _kid, _next  # noqa: E402


# ------------------------------------------------------------------ the checker ----
def test_a_decimal_comma_is_seen_and_a_thousands_comma_is_not():
    for typed, point in (("0,00009", "0.00009"), ("3,5", "3.5"), ("0,500", "0.500"), ("-0,5", "-0.5"),
                         ("1,2345", "1.2345"), ("£2,50", "£2.50"), ("3,5 cm", "3.5 cm")):
        assert me.decimal_comma(typed) == point, typed
    for typed in ("2,750", "12,500,000", "1,000", "2, 3", "2 750", "0.5", "35"):
        assert me.decimal_comma(typed) is None, typed
    assert me.check_answer("int", 2750, "2,750") and me.check_answer("num", 6300000, "6,300,000")
    assert not me.check_answer("num", 0.00009, "0,00009")       # marked by check(): "Nearly", then a retry
    assert me.check_answer("num", 0.00009, "0.00009")
    assert me.check_answer("set", "2, 3, 5", "2, 3, 5")           # a list keeps its commas


def test_a_label_answer_ignores_case_and_a_word_copied_from_the_chart():
    bars = {"names": ["Class 3A", "Class 3B", "Class 3C"], "heads": []}
    for typed in ("3A", "3a", "class 3a", "Class 3A", "CLASS 3A"):
        assert me.check_answer("str", "3A", typed, labels=bars), typed
    for typed in ("3b", "class 3b", "3b 3a", "class"):
        assert not me.check_answer("str", "3A", typed, labels=bars), typed
    table = {"names": ["Maple", "Ash", "Elm"], "heads": ["School", "Pupils"]}
    assert me.check_answer("str", "Ash", "ash school", labels=table)
    assert me.check_answer("str", "Ash", "School Ash", labels=table)
    assert not me.check_answer("str", "Ash", "maple ash", labels=table)      # another school's name is not a copy
    parcels = {"names": ["red", "blue", "green"], "heads": ["Parcel", "Mass (kg)"]}
    assert me.check_answer("str", "red", "the red parcel", labels=parcels)
    assert not me.check_answer("str", "red", "blue red", labels=parcels)


def test_every_chart_and_table_label_answer_marks_itself_and_its_copied_form():
    seen = 0
    for s in me.SKILLS:
        fn = me.GENERATORS[s["key"]]
        for i in range(30):
            q = me.call_generator(fn, i % 3)
            labels = me.chart_labels(q)
            if not labels:
                continue
            seen += 1
            args = (q["answer_type"], q["answer"])
            kw = {"prompt": q["prompt"], "unit": (q.get("spec") or {}).get("unit"), "labels": labels}
            assert me.check_answer(*args, q["answer"], **kw), (s["key"], q["answer"])
            assert me.check_answer(*args, str(q["answer"]).upper(), **kw), (s["key"], q["answer"])
            a = " " + str(q["answer"]).lower()
            # "Class 3A" on the chart, 3A the answer: a name in words, then the answer. Not a maths expression that
            # happens to end the same way ("3^4 × 3^5" when the empty cell is 3^5): that one is rightly marked wrong.
            full = [n for n in labels["names"] if n.lower().endswith(a) and re.fullmatch(r"[a-z][a-z '’-]*", n.lower()[:-len(a)])]
            if full:
                assert me.check_answer(*args, full[0].lower(), **kw), (s["key"], full[0])
    assert seen > 100


def _whys(prefix, runs=200):
    for s in me.SKILLS:
        if not s["key"].startswith(prefix):
            continue
        for i in range(runs):
            q = me.call_generator(me.GENERATORS[s["key"]], i % 3)
            yield s["key"], q, " ".join(q.get("solution") or [])


def test_years_1_and_2_whys_explain_in_their_own_words():
    for key, q, why in _whys("Y1."):
        assert not re.search("[÷×]", why), (key, why)               # Year 1 has met neither sign
    for key, q, why in list(_whys("Y1.")) + list(_whys("Y2.")):
        a = me._sn(me.answer_text(q))
        rest = me._sn(why).replace(a, " ") if a else me._sn(why)
        # a reason: words, a sum, or the counting itself ("5, 10, 15, 20") — never the answer alone
        assert re.search(r"[a-z]{2,}|[-+=<>]|\d+ \d+", rest), (key, q["prompt"], why)
    for key, q, why in _whys("Y2.2."):
        if re.fullmatch(r"___ × \d+ = \d+|\d+ × ___ = \d+", q["prompt"]):
            assert "÷" not in why and "so the missing number is" in why, (q["prompt"], why)
    for key, q, why in _whys("Y2.3.a"):
        if q["prompt"].startswith("Which is bigger"):
            assert re.search("equal parts|Both are|the same as", why), (q["prompt"], why)
    from app.maths.y2_gen_a import _bigger_why
    assert "each part is bigger" in _bigger_why("1/2", "1/4")


def test_review_skills_are_a_warm_up_for_the_child():
    from app.drills import maths as drill
    assert drill.review_tag("Y7.4.a", 8) == "Warm-up" and drill.review_tag("Y8.4.a", 8) is None


# ------------------------------------------------------------------ through the API ----
def _child(page, name, year):
    signup(page)
    pid = add_child(page, name, year)
    enter_child(page, name)
    return pid


def _post(page, url, body):
    return page.request.post(BASE + url, data=body).json()


def _served(pid, tok, answer, prompt, atype="num", labels=None):
    DB.maths_lab_q.insert_one({"_id": tok, "skill": "Y7.0.a", "prompt": prompt, "answer": answer, "display": str(answer),
                               "answer_type": atype, "tolerance": 0, "unit": None, "solution": ["Look at the place."],
                               "difficulty": 1, "pupil": pid, "labels": labels, "created": datetime.datetime.utcnow()})


def test_a_decimal_comma_gets_nearly_and_one_retry(page):
    pid = _child(page, "Camille", 7)
    tok = "dc-" + pid
    _served(pid, tok, 0.00009, "What is the value of the digit 9 in 0.15089?")
    r = _post(page, "/api/maths/check", {"token": tok, "value": "0,00009"})
    assert r["ok"] and r["retry"] and r["hint"] == "Nearly: in England we write a decimal point, 0.00009", r
    assert not DB.maths_lab_q.find_one({"_id": tok})["done"]
    assert not DB.attempts.find_one({"pupil_id": pid, "activity": "maths"})              # nothing recorded yet
    r = _post(page, "/api/maths/check", {"token": tok, "value": "0.00009"})
    assert r["ok"] and r["correct"], r
    # a wrong number with a comma is wrong, and says how England writes it
    tok2 = tok + "b"
    _served(pid, tok2, 3.5, "Write 7/2 as a decimal.")
    r = _post(page, "/api/maths/check", {"token": tok2, "value": "4,5"})
    assert r["ok"] and r["correct"] is False and not r.get("retry")
    assert r["solution"][0] == "In England we write a decimal point: 4.5, not 4,5.", r
    # a thousands comma is still a thousands comma
    tok3 = tok + "c"
    _served(pid, tok3, 2750, "Write two thousand, seven hundred and fifty in digits.", atype="int")
    r = _post(page, "/api/maths/check", {"token": tok3, "value": "2,750"})
    assert r["ok"] and r["correct"], r


def test_a_bar_label_copied_from_the_chart_is_right(page):
    pid = _child(page, "Ava", 3)
    q = me.call_generator(me.GENERATORS["Y3.1.a"], 1)
    for _ in range(300):                               # the bar chart of classes ("Class 3A")
        if q.get("component") == "bar_chart" and q["answer_type"] == "str":
            break
        q = me.call_generator(me.GENERATORS["Y3.1.a"], 1)
    tok = "lb-" + pid
    _served(pid, tok, q["answer"], q["prompt"], atype="str", labels=me.chart_labels(q))
    r = _post(page, "/api/maths/check", {"token": tok, "value": "class " + q["answer"].lower()})
    assert r["ok"] and r["correct"], (q["answer"], r)


def test_the_first_look_is_the_missed_fact_and_the_wait_mixes_tables(page):
    pid, s = _kid(page, 5, acts=("tables",), target=60)
    q = _next(s, "tables")                             # an earlier mistake ...
    _check(s, "tables", q["token"], "9999")
    left = _next(s, "tables", fix=1)                    # ... and a practice question left on screen in its session
    assert not left["fixing"]
    r = s.post(BASE + "/api/mtc/start", json={}).json()
    facts = DB.items.find_one({"_id": r["token"]})["meta"]["facts"]
    i = next(k for k, f in enumerate(facts) if {int(n) for n in f.split("x")} - {1, 10})
    s.post(BASE + "/api/mtc/finish", json={"token": r["token"], "answers": [
        {"value": "1" if k == i else str(a), "ms": 2000} for k, a in enumerate(DB.items.find_one({"_id": r["token"]})["answer"])]})
    missed = facts[i]
    tabs = {int(n) for n in missed.split("x")} - {1, 10}
    f = _next(s, "tables", fix=1, check=1)
    doc = DB.items.find_one({"_id": f["token"]})
    assert f["token"] != left["token"] and sorted(doc["meta"]["fact"].split("x")) == sorted(missed.split("x")), (doc, missed)
    assert f["fix_msg"] == "A first look at a fact you missed in the check · 1 of 1", f["fix_msg"]
    _check(s, "tables", f["token"], str(doc["answer"]))
    near = []
    for _ in range(NEAR_RUN + 4):                      # while it waits: its tables for 5 questions, then the others
        f = _next(s, "tables", fix=1, check=1)
        doc = DB.items.find_one({"_id": f["token"]})
        assert not f["fixing"], f
        near.append(bool({doc["meta"]["a"], doc["meta"]["b"]} & tabs))
        _check(s, "tables", f["token"], str(doc["answer"]))
    assert near[:NEAR_RUN] == [True] * NEAR_RUN and not any(near[NEAR_RUN:]), (missed, near)
