"""Grammar and science content after the fourth test wave (10 Nov 2026): Year 6 test review covers the GPS
favourites, wrong options say why they are wrong, strands take turns within a day, science tap questions do not
hold their own answer, calculation explanations start from the formula, and a pre-filled box says so."""
import datetime
import random
import re

import requests

from app.bank import engine
from app.drills.bank import STRAND_RUN, pick_skill

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup

ALL = [(sub, sk, q) for sub in engine.load() for y in engine.load()[sub] for sk in engine.load()[sub][y] for q in sk["qs"]]


def test_year6_test_review_has_the_gps_favourites_from_the_first_day():
    y6 = engine.skills("grammar", 6)
    review = {s["title"]: s for s in y6 if s["strand"] == "Test review"}
    for title in ("Modal verbs", "Fronted adverbials", "Relative clauses", "Adverbs of possibility"):
        sk = review[title]
        assert len(sk["qs"]) >= 20 and all(q["why"].strip() for q in sk["qs"]), title
        assert len({q["t"] for q in sk["qs"]}) >= 3, title
    order = [s["key"] for s in y6]
    assert order[:8] == ["GP6.01", "GP6.17", "GP6.02", "GP6.18", "GP6.03", "GP6.19", "GP6.04", "GP6.20"], order[:8]


def test_the_doer_is_not_called_the_subject_without_saying_active():
    for sub, sk, q in ALL:
        if sub != "grammar":
            continue
        text = " ".join(str(q.get(f, "")) for f in ("q", "why", "why2"))
        if re.search(r"(person or thing|word) that does the action", text):
            assert re.search(r"\bactive\b|usually", text), (sk["key"], text)
    q = engine.question("GP6.07", "06e8851740c9")
    assert "passive" in q["why"] and "active" in q["q"]


def test_why_not_lines_name_real_wrong_options_and_why2_differs():
    n = 0
    for sub, sk, q in ALL:
        for opt, line in (q.get("no") or {}).items():
            assert q["t"] == "mcq" and opt in q["opts"][1:] and line.strip(), (sk["key"], opt)
            n += 1
        if q.get("why2"):
            assert q["why2"] != q["why"], sk["key"]
    assert n >= 100
    for key in ("GP6.02", "GP6.17", "GP3.10", "GP7.10", "GP7.11", "GP5.05"):     # the clause and modal skills
        mcqs = [q for q in engine.skill(key)["qs"] if q["t"] == "mcq"]
        assert sum(1 for q in mcqs if q.get("no")) >= len(mcqs) - 2, key


def test_why_lines_for_a_wrong_option_and_a_second_miss():
    q = engine.question("GP6.02", "fbee2f6f83a4")
    key = {"t": "mcq", "right": 0, "opts": q["opts"]}
    no, why = engine.why_lines(q, key, q["opts"].index("We waited and the bell rang."))
    assert "coordinating" in no and why == q["why"]
    no, why = engine.why_lines(q, key, q["opts"].index("We waited and the bell rang."), again=True)
    assert why == q["why2"] != q["why"]
    no, _ = engine.why_lines(q, key, 0)
    assert no == ""


def test_options_do_not_explain_themselves():
    """'a phrase: it is only three short words' gave the answer away (P8)."""
    for sub, sk, q in ALL:
        if sub == "grammar" and q["t"] == "mcq":
            for o in q["opts"]:
                assert not re.match(r"^an? [a-z ]+: (it|they) ", o), (sk["key"], o)
                assert not re.search(r", (as in|like) '", o), (sk["key"], o)


def _run(skills, steps=60, seed=0):
    rnd = random.Random(seed)
    t0 = datetime.datetime(2026, 1, 1)
    mm, strands = {}, []
    for n in range(steps):
        run = strands[-STRAND_RUN:]
        avoid = run[0] if len(run) == STRAND_RUN and len(set(run)) == 1 else None
        sk, _ = pick_skill(skills, mm, rnd, avoid=avoid)
        d = mm.setdefault(sk["key"], {"score": 0, "attempts": 0})
        d["score"] = min(100, d["score"] + 6)
        d["attempts"] += 1
        d["last"] = t0 + datetime.timedelta(minutes=n)
        strands.append(sk["strand"])
    return strands


def test_no_strand_runs_more_than_three_in_a_row():
    for sub, year in (("science", 9), ("grammar", 6), ("science", 7), ("grammar", 1)):
        strands = _run(engine.skills(sub, year))
        longest = max(len(list(g)) for g in [list(g) for _, g in __import__("itertools").groupby(strands)])
        assert longest <= STRAND_RUN, (sub, year, strands[:20])
    first = _run(engine.skills("science", 9), steps=12)
    assert len(set(first)) >= 2 and first.count("Health") <= 8, first     # Ryan's day 1 was 12 Health questions


def test_science_tap_sentences_do_not_hold_their_answer():
    fixed = {"46b0cf1291d2": "carried in the blood", "132c796f5a32": "ovules", "42813c9bae9d": "particles",
             "7a06f32a813a": "react more slowly", "88251d01eb39": "Smoke damages", "0a03922c67ff": "divided by"}
    for qid, leak in fixed.items():
        q = next(q for sub, sk, q in ALL if q["id"] == qid)
        assert leak not in q["s"], (qid, q["s"])


def test_science_calculations_state_the_formula_first():
    for key in ("SC9.31", "SC9.36", "SC9.38", "SC9.40", "SC9.44", "SC9.46", "SC9.49", "SC8.47", "SC8.56", "SC7.43"):
        for q in engine.skill(key)["qs"]:
            if q["t"] == "num" and re.search(r"\d\s*[×x÷/]\s*\d", q["why"]):
                assert re.match(r"^[A-Za-z(]", q["why"]), (key, q["why"])          # words before the sum


def test_prefilled_sentences_are_signposted():
    for sub, sk, q in ALL:
        if q["t"] == "write":
            assert not re.match(r"^(Use the short form|Make the two words|Fix the plural word|Rewrite 'do not')", q["q"]), q["q"]


def test_a_wrong_option_shows_why_it_is_wrong(browser):
    pg = browser.new_context(base_url=BASE).new_page()
    email = signup(pg)
    pid = add_child(pg, "Dara", 6)
    ctx = browser.new_context(base_url=BASE, viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    kid = ctx.new_page()
    kid.set_default_timeout(15000)
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Dara")
    kid.goto("/me/grammar")
    kid.wait_for_selector("#area .opt, #area .word, #answer")
    it = DB.items.find_one({"pupil_id": pid, "activity": "grammar", "done": {"$ne": True}}, sort=[("_id", -1)]) \
        or DB.items.find_one({"pupil_id": pid}, sort=[("_id", -1)])
    q = engine.question("GP6.02", "fbee2f6f83a4")
    DB.items.update_one({"_id": it["_id"]}, {"$set": {"meta.skill": "GP6.02", "meta.qid": "fbee2f6f83a4", "meta.reason": "new",
                                                      "answer": {"t": "mcq", "right": 0, "opts": q["opts"]}}})
    s = requests.Session()
    for c in ctx.cookies():
        s.cookies.set(c["name"], c["value"])
    r = s.post(BASE + "/api/grammar/check", json={"token": it["_id"], "value": 1}).json()
    assert r["correct"] is False and "coordinating" in r["whynot"] and r["why"], r
    ctx.close()
    pg.context.close()
