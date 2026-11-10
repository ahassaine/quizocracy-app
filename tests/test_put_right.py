"""A mistake is put right only when THAT item is answered right later (for maths, where every question is made
fresh, a question like it), and it stays put right. "Practise my mistakes" never asks the same item twice in a
row, fills the gap a missed item waits for with practice on the same tables or skills and says when it comes
back, and after the Year 4 check practises exactly the facts missed in it. A fact missed twice gets a trick;
every check is kept with its date, a better score says "New best!", and a parent can make a check part of the
times-tables target."""
import datetime
import os
import sys

import requests

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills.tables import tip  # noqa: E402
from app.items import RECALL_ITEMS  # noqa: E402
from app.progress import alike  # noqa: E402

ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _kid(page, year, name="Rami", acts=ALL, target=10):
    signup(page)
    pid = add_child(page, name, year)
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {k: {"on": k in acts, "target": target} for k in ALL}},
                                        "$unset": {"plan_log": ""}})
    enter_child(page, name)
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return pid, s


def _next(s, act, **body):
    q = s.post(BASE + f"/api/{act}/next", json=body).json()
    assert q.get("ok"), (act, q)
    return q


def _check(s, act, token, value):
    return s.post(BASE + f"/api/{act}/check", json={"token": token, "value": value}).json()


def _age(pid, minutes=10):
    """As if every answer so far was given some minutes ago (the gap a missed item waits for is over)."""
    for r in DB.attempts.find({"pupil_id": pid}):
        DB.attempts.update_one({"_id": r["_id"]}, {"$set": {"ts": r["ts"] - datetime.timedelta(minutes=minutes)}})


def _good(key):
    return {"mcq": key.get("right"), "tap": key.get("hits"), "num": key.get("a")}.get(key["t"], (key.get("a") or [""])[0])


def test_alike_and_tips_are_structural_and_hand_written():
    assert alike("A book costs £3.70. Noah pays with a £10 note. How much change should Noah be given, in pence?",
                 "A board game costs £7.80. Sara pays with a £10 note. How much change should Sara be given, in pence?")
    assert alike("Write 'five hundred and thirty' as a numeral.", "Write 'two hundred' as a numeral.")
    assert not alike("Work out 1/4 + 1/2 × 1/2.", "Work out 3/6 + 1/6 + 1/6.")          # another order of operations
    assert not alike("Books borrowed. Use the bar chart. What is the total of all the bars?",
                     "Books borrowed. Use the bar chart. Add Mon and Wed together, then take away Fri. What is the result?")
    # a sign that belongs to a number, and an ordinal, are part of the number (they never came back before)
    assert alike("Put these in order, smallest first. Which number is 4th?   -24, 7, -3, 12, -9",
                 "Put these in order, smallest first. Which number is 2nd?   5, -18, -9, 30, -2")
    assert not alike("Work out 10 − 4.", "Work out 10 + 4.")
    assert tip(6, 9) == "9 × 6: one less than 6 is 5, and 5 + 4 = 9 → 54."
    assert "5, 6, 7, 8 → 56" in tip(8, 7) and "48" in tip(8, 7)
    for a in range(1, 13):
        for b in range(1, 13):
            t = tip(a, b)
            assert t and str(a * b) in t, (a, b, t)


def test_a_maths_mistake_is_put_right_only_by_a_question_like_it(page):
    pid, s = _kid(page, 5, acts=("maths",))
    q = _next(s, "maths")
    assert _check(s, "maths", q["token"], "zzqx")["correct"] is False
    miss = DB.attempts.find_one({"pupil_id": pid, "activity": "maths", "correct": False})
    # straight away it waits for its gap: practice meanwhile, and the child is told when it comes back
    f = _next(s, "maths", fix=1)
    assert not f["fixing"] and f["fix_later"] == 1 and "comes back in about 3 minutes" in f["fix_msg"], f
    doc = DB.maths_lab_q.find_one({"_id": f["token"]})
    assert _check(s, "maths", f["token"], str(doc["answer"]))["correct"]
    DB.attempts.update_many({"pupil_id": pid, "correct": True}, {"$unset": {"lq": ""}})   # (whatever it was)
    # right answers to other kinds of question of the same skill put nothing right
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.attempts.insert_many([{"pupil_id": pid, "family_id": fam, "activity": "maths", "correct": True,
                              "detail": miss["detail"], "lq": "Something else entirely: name the shape with %d sides." % i,
                              "day": miss["day"], "ts": datetime.datetime.utcnow()} for i in range(5)])
    _age(pid)
    f = _next(s, "maths", fix=1)
    assert f["fixing"] and f["skill"] == miss["detail"], f
    assert alike(miss["q"], f["prompt"]), (miss["q"], f["prompt"])      # the same kind of question, made fresh
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    day = page.locator("[data-testid=mistakes-day]").first.inner_text()
    assert "1 to go over" in day and "put right since" not in day, day
    enter_child(page, "Rami")
    doc = DB.maths_lab_q.find_one({"_id": f["token"]})
    assert _check(s, "maths", f["token"], str(doc["answer"]))["correct"], doc
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    day = page.locator("[data-testid=mistakes-day]").first
    assert "1 put right since" in day.inner_text(), day.inner_text()
    assert "a question like this was right later" in day.locator("[data-testid=put-right]").first.inner_text()
    # missing that kind of question again makes it one to go over again: listed once, never also as put right
    DB.attempts.insert_one({**{k: miss[k] for k in ("pupil_id", "family_id", "activity", "detail", "q", "exp", "day")},
                            "correct": False, "got": "7", "ts": datetime.datetime.utcnow()})
    page.goto(f"/children/{pid}")
    day = page.locator("[data-testid=mistakes-day]").first.inner_text()
    assert "1 to go over" in day and "put right since" not in day, day
    assert "put right before, then missed again" in page.inner_text("[data-testid=missed-again]")


def test_practise_my_mistakes_never_asks_the_same_question_twice_in_a_row(page):
    pid, s = _kid(page, 4, acts=("grammar",))
    q = _next(s, "grammar")
    missed = DB.items.find_one({"_id": q["token"]})["meta"]
    assert _check(s, "grammar", q["token"], "zzqx")["correct"] is False
    for _ in range(6):                         # inside the gap: never the missed question, and said honestly
        f = _next(s, "grammar", fix=1)
        it = DB.items.find_one({"_id": f["token"]})
        assert (it["meta"]["skill"], it["meta"]["qid"]) != (missed["skill"], missed["qid"])
        assert not f["fixing"] and "Your mistake comes back in" in f["fix_msg"], f
        assert _check(s, "grammar", f["token"], _good(it["answer"]))["correct"]
    _age(pid)
    f = _next(s, "grammar", fix=1)
    it = DB.items.find_one({"_id": f["token"]})
    assert f["fixing"] and (it["meta"]["skill"], it["meta"]["qid"]) == (missed["skill"], missed["qid"])
    assert _check(s, "grammar", f["token"], _good(it["answer"]))["correct"]
    r = _next(s, "grammar", fix=1)                # right again in the same sitting: the session ends calmly
    assert r["fix_end"] and "token" not in r and r["fix_total"] == 0, r
    assert r["fix_done"].startswith("All done for now. 1 mistake comes back later ("), r


def _fill(s, act, n=RECALL_ITEMS):
    """The other questions a missed one waits behind, answered right."""
    for _ in range(n):
        f = _next(s, act, fix=1)
        it = DB.items.find_one({"_id": f["token"]})
        _check(s, act, f["token"], it["answer"] if act == "spelling" else _good(it["answer"]))


def test_right_again_in_the_same_sitting_is_practice_and_put_right_only_later(page):
    pid, s = _kid(page, 4, acts=("grammar",))
    q = _next(s, "grammar")
    missed = DB.items.find_one({"_id": q["token"]})["meta"]
    assert _check(s, "grammar", q["token"], "zzqx")["correct"] is False
    _fill(s, "grammar")
    _age(pid)                                     # ten minutes on: the gap is over, but the same sitting
    f = _next(s, "grammar", fix=1)
    it = DB.items.find_one({"_id": f["token"]})
    assert f["fixing"] and (it["meta"]["skill"], it["meta"]["qid"]) == (missed["skill"], missed["qid"])
    r = _check(s, "grammar", f["token"], _good(it["answer"]))
    assert r["correct"] and r["again_later"] and not r["mastered"], r      # practice: it comes back later
    assert not r.get("put_right"), r              # no "★ You put right a mistake" for practice
    f = _next(s, "grammar", fix=1)                # nothing more to put right in this sitting: the end
    assert f["fix_end"] and f["fix_total"] == 0 and "1 mistake comes back later" in f["fix_done"], f
    page.goto("/me")
    assert page.locator("[data-testid=fix-all]").count() == 0
    assert "1 mistake you practised comes back later" in page.inner_text("[data-testid=fix-later]")
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    day = page.locator("[data-testid=mistakes-day]").first
    assert "1 to go over" in day.inner_text() and "put right since" not in day.inner_text(), day.inner_text()
    assert "right again today, checked again later" in day.locator("[data-testid=practised]").inner_text()
    assert "1 of them right again today" in page.inner_text("[data-testid=mistakes-total]")
    enter_child(page, "Rami")
    _age(pid, 60)                                 # a later sitting: it comes back, and now it counts
    f = _next(s, "grammar", fix=1)
    it = DB.items.find_one({"_id": f["token"]})
    assert f["fixing"] and f["fix_total"] == 1 and (it["meta"]["skill"], it["meta"]["qid"]) == (missed["skill"], missed["qid"])
    r = _check(s, "grammar", f["token"], _good(it["answer"]))
    assert r["correct"] and not r.get("again_later") and r["put_right"], r
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    day = page.locator("[data-testid=mistakes-day]").first.inner_text()
    assert "1 put right since" in day and "0 to go over" in day, day


def test_a_missed_question_right_later_never_makes_a_skill_mastered(page):
    from app.bank import engine
    pid, s = _kid(page, 4, acts=("grammar",))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    q = _next(s, "grammar")
    it = DB.items.find_one({"_id": q["token"]})
    meta, key = it["meta"], it["answer"]
    assert _check(s, "grammar", q["token"], "zzqx")["correct"] is False
    _age(pid, 120)                                # another sitting
    DB.bank_mastery.update_one({"_id": f"{pid}:{meta['skill']}"}, {"$set": {"score": 96, "streak": 4}})

    def ask(qid, k):
        tok = f"rep{qid}-{pid}"
        DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": "grammar", "answer": k,
                             "meta": {"skill": meta["skill"], "qid": qid, "reason": "retry"},
                             "created": datetime.datetime.utcnow(), "done": False})
        return _check(s, "grammar", tok, _good(k))
    r = ask(meta["qid"], key)                     # the missed question, right: put right, the score grows, not mastered
    assert r["correct"] and not r["mastered"] and r["score"] == 99 and not r.get("again_later"), r
    other = next(x for x in engine.skill(meta["skill"])["qs"] if x["id"] != meta["qid"])
    r = ask(other["id"], engine.serve(other)[1])  # a question never missed can make it mastered
    assert r["correct"] and r["mastered"], r
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert "re-checked on a later day" in page.locator("[data-testid=skills-grammar]").text_content()


def test_a_spelling_word_right_again_in_the_same_sitting_climbs_no_box(page):
    pid, s = _kid(page, 4, acts=("spelling",))
    q = _next(s, "spelling")
    word = DB.items.find_one({"_id": q["token"]})["answer"]
    assert _check(s, "spelling", q["token"], "zzqx")["correct"] is False
    _fill(s, "spelling")
    _age(pid)
    f = _next(s, "spelling", fix=1)
    assert f["fixing"] and DB.items.find_one({"_id": f["token"]})["answer"] == word, f
    r = _check(s, "spelling", f["token"], word)
    assert r["correct"] and r["again_later"], r
    st = DB.spelling_words.find_one({"_id": f"{pid}:{word}"})
    assert st["box"] == 0 and st["due"] > datetime.date.today().isoformat(), st


def _check_run(s, wrong):
    r = s.post(BASE + "/api/mtc/start", json={}).json()
    it = DB.items.find_one({"_id": r["token"]})
    ans = [{"value": "1" if i < wrong else str(a), "ms": 2000} for i, a in enumerate(it["answer"])]
    return it, s.post(BASE + "/api/mtc/finish", json={"token": r["token"], "answers": ans}).json()


def test_practise_the_ones_i_missed_after_the_check(page):
    pid, s = _kid(page, 4, acts=("tables",), target=40)
    q = _next(s, "tables")                        # an older mistake, not from the check
    old = DB.items.find_one({"_id": q["token"]})["meta"]["fact"]
    _check(s, "tables", q["token"], "9999")
    _age(pid, 40)
    it, res = _check_run(s, 3)
    facts = it["meta"]["facts"][:3]
    assert res["score"] == 22 and [m["fact"] for m in res["missed"]] == facts
    same = lambda f, g: sorted(f.split("x")) == sorted(g.split("x"))          # noqa: E731
    looked = []
    for i in range(3):                            # first, a look at each missed fact, straight away
        f = _next(s, "tables", fix=1, check=1)
        fact = DB.items.find_one({"_id": f["token"]})["meta"]["fact"]
        assert fact in facts and fact not in looked and not f["fixing"], (fact, facts, f)
        assert f["fix_msg"] == f"A first look at a fact you missed in the check · {i + 1} of 3" and f["fix_total"] == 3
        looked.append(fact)
        r = _check(s, "tables", f["token"], str(DB.items.find_one({"_id": f["token"]})["answer"]))
        assert r["correct"] and r.get("again_later"), r
    for _ in range(5):                            # then they wait for the gap: the same tables meanwhile
        f = _next(s, "tables", fix=1, check=1)
        doc = DB.items.find_one({"_id": f["token"]})
        fact, a, b = doc["meta"]["fact"], doc["meta"]["a"], doc["meta"]["b"]
        assert not any(same(fact, g) for g in facts + [old]), fact
        assert {a, b} & {int(n) for g in facts for n in g.split("x")} - {1, 10}, (fact, facts)
        assert "The 3 facts you missed come back in about" in f["fix_msg"], f["fix_msg"]
        _check(s, "tables", f["token"], str(doc["answer"]))
    _age(pid)
    done_at = DB.pupils.find_one({"_id": pid})["mtc"][0]["done_at"]              # the check, as long ago
    DB.pupils.update_one({"_id": pid}, {"$set": {"mtc.0.done_at": done_at - datetime.timedelta(minutes=10)}})
    for i in range(3):                            # after the gap: put right, one by one; the older mistake waits
        f = _next(s, "tables", fix=1, check=1)
        doc = DB.items.find_one({"_id": f["token"]})
        assert f["fixing"] and doc["meta"]["fact"] in facts and f["fix_total"] == 3 - i, f
        assert _check(s, "tables", f["token"], str(doc["answer"]))["correct"]
    f = _next(s, "tables", fix=1, check=1)
    assert f["fix_msg"] == "" and f["fix_done"].startswith("All the facts you missed in the check are put right")
    if not any(same(old, g) for g in it["meta"]["facts"][3:]):  # (unless the check asked it, right: then it is put right)
        assert old in _next(s, "tables", fix=1).get("fix_msg", "") or _next(s, "tables", fix=1)["fix_total"] == 1


def test_a_fact_missed_twice_gets_a_trick(page):
    pid, s = _kid(page, 4, acts=("tables",))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    hints = []
    for i in range(2):
        tok = f"tip{i}-{pid}"
        DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": "tables", "answer": 56,
                             "meta": {"fact": "8x7", "a": 8, "b": 7, "prompt": "8 × 7 ="},
                             "created": datetime.datetime.utcnow(), "done": False})
        hints.append(_check(s, "tables", tok, "54").get("hint"))
    assert hints[0] is None and hints[1].startswith("Tip: 5, 6, 7, 8 → 56"), hints


def test_every_check_is_kept_with_its_date_and_a_new_best_is_cheered(page):
    pid, s = _kid(page, 4, acts=("tables",))
    old = [{"at": datetime.datetime.utcnow(), "day": "2026-10-01", "score": 9, "of": 25, "missed": []}] * 30
    DB.pupils.update_one({"_id": pid}, {"$set": {"mtc": old}})
    _, r = _check_run(s, 20)
    assert r["score"] == 5 and not r["new_best"] and r["best"] == 9
    _, r = _check_run(s, 2)
    assert r["score"] == 23 and r["new_best"] and r["checks"] == 32
    page.goto("/me/tables/year4-check")
    assert "your best: 23/25" in page.inner_text("[data-testid=mtc-last]")
    page.goto("/me")
    assert "Best so far: 23/25" in page.inner_text("[data-testid=mtc-card]")
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    card = page.inner_text("[data-testid=mtc-scores]")
    assert "23/25" in card and "best of 32 checks" in card, card
    page.click("[data-testid=mtc-list] summary")
    assert "1 Oct: 9/25" in page.inner_text("[data-testid=mtc-list]") and "new best" in page.inner_text("[data-testid=mtc-list]")
    page.goto(f"/children/{pid}/report")
    rep = page.inner_text("[data-testid=report-mtc]")
    assert "2 practice checks in this period" in rep and "Best: 23/25" in rep, rep


def test_a_check_a_day_can_be_part_of_the_times_tables_target(page):
    pid, s = _kid(page, 4, acts=("tables",), target=1)
    page.goto("/me")
    assert "isn't part of today's plan" in page.inner_text("[data-testid=mtc-card]")
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.check("[data-testid=check-tables]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(f"**/children/{pid}**")
    assert DB.pupils.find_one({"_id": pid})["activities"]["tables"].get("check") is True
    enter_child(page, "Rami")
    assert "Part of today's times tables" in page.inner_text("[data-testid=mtc-card]")
    q = _next(s, "tables")
    r = _check(s, "tables", q["token"], str(DB.items.find_one({"_id": q["token"]})["answer"]))
    assert r["day"]["day_pct"] == 16, r["day"]   # the target, not the check yet (it counts as 5 answers: 1 of 6)
    _, r = _check_run(s, 0)
    assert r["day"]["day_pct"] == 100, r
    page.goto("/me")
    assert "+ the check ✓" in page.inner_text("[data-testid=tile-tables]")


def test_the_parent_sees_the_weakest_tables(page):
    pid, s = _kid(page, 4, acts=("tables",))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    for f, a, b, w, r in (("7x8", 7, 8, 4, 1), ("8x6", 8, 6, 1, 3), ("3x4", 3, 4, 0, 5)):
        DB.tables_facts.insert_one({"_id": f"{pid}:{f}", "pupil_id": pid, "family_id": fam, "a": a, "b": b,
                                    "wrong": w, "right": r, "streak": 0})
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert "Weakest: the 7× and 8× tables" in page.inner_text("[data-testid=tables-weakest]")
