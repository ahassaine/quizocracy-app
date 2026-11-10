"""One rule for every count of mistakes (progress.mistake_book): "Practise my mistakes" never goes round in a
circle between subjects and ends when the mistakes due at its start are done, with a calm end screen; the star
"You put right a mistake" comes only when one really is put right; the child's button, "come back later", the
parent's "to go over" and "put right", the school words and the printed report agree; a fact and its reverse
are one fact; reporting one spelling mistake marks only that word."""
import datetime

import requests
from bson import ObjectId

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent

ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _kid(page, year, acts, name="Tia", target=10):
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


def _good(key):
    return {"mcq": key.get("right"), "tap": key.get("hits"), "num": key.get("a")}.get(key["t"], (key.get("a") or [""])[0])


def _age(pid, minutes):
    for r in DB.attempts.find({"pupil_id": pid}):
        DB.attempts.update_one({"_id": r["_id"]}, {"$set": {"ts": r["ts"] - datetime.timedelta(minutes=minutes)}})


def _miss(s, act):
    q = _next(s, act)
    assert _check(s, act, q["token"], "zzqx")["correct"] is False
    return q


def _right(s, act, token):
    doc = (DB.maths_lab_q if act == "maths" else DB.items).find_one({"_id": token})
    v = str(doc["answer"]) if act in ("maths", "tables", "spelling") else _good(doc["answer"])
    return _check(s, act, token, v)


def _loads(page, url, seconds=4):
    """Open url and count the page loads in the next few seconds (a loop between subjects makes dozens)."""
    n = {"loads": 0}
    page.on("framenavigated", lambda f: n.__setitem__("loads", n["loads"] + (f == page.main_frame)))
    page.goto(url)
    page.wait_for_timeout(seconds * 1000)
    return n["loads"]


def test_practise_my_mistakes_never_loops_between_subjects(page):
    """The wave-5 stopper: two subjects, each with a practice question left on screen in "Practise my mistakes"
    and a mistake ready in the other, sent the page back and forth about 10 times a second."""
    pid, s = _kid(page, 6, ("grammar", "maths"))
    _miss(s, "grammar")
    _miss(s, "maths")
    g, m = _next(s, "grammar", fix=1), _next(s, "maths", fix=1)      # both wait for their gap: practice questions,
    assert not g["fixing"] and not m["fixing"]                       # left unanswered on screen
    _age(pid, 40)                                                    # another sitting: both ready
    loads = _loads(page, "/me/grammar?fix=1")
    assert loads <= 2, loads
    page.wait_for_function("document.body.dataset.qtoken")
    assert "Putting a mistake right" in page.inner_text("[data-testid=fix-msg]")


def test_with_nothing_due_anywhere_the_session_ends_calmly(page):
    pid, s = _kid(page, 6, ("grammar", "spelling"))
    for act in ("grammar", "spelling"):
        _miss(s, act)
    _age(pid, 40)                                                    # a while ago, but within the hour
    for act in ("grammar", "spelling"):                              # right again in the same sitting: practised
        f = _next(s, act, fix=1)
        assert f["fixing"], f
        r = _right(s, act, f["token"])
        assert r["correct"] and r["again_later"] and not r.get("put_right"), r
    page.goto("/me")
    assert page.locator("[data-testid=fix-all]").count() == 0       # nothing due now ...
    assert "2 mistakes you practised come back later" in page.inner_text("[data-testid=fix-later]")   # ... and said so
    loads = _loads(page, "/me/grammar?fix=1", 3)                     # an old link to it: no loop, the end screen
    assert loads <= 1, loads
    end = page.inner_text("[data-testid=fix-end]")
    assert "All done for now." in end and "2 mistakes come back later" in end, end
    page.click("[data-testid=fix-end-back]")
    page.wait_for_url("**/me")


def test_a_session_ends_with_its_queue_and_new_mistakes_wait(page):
    pid, s = _kid(page, 5, ("spelling",))
    q = _miss(s, "spelling")
    word = DB.items.find_one({"_id": q["token"]})["answer"]
    _age(pid, 90)                                                    # an older sitting: due now
    f = _next(s, "spelling", fix=1)
    since = f["fix_since"]
    assert f["fixing"] and f["fix_total"] == 1 and DB.items.find_one({"_id": f["token"]})["answer"] == word
    assert _check(s, "spelling", f["token"], "zzqx")["correct"] is False     # missed again during the session
    f = _next(s, "spelling", fix=1, since=since)
    assert f["fix_end"] and "1 mistake comes back later" in f["fix_done"], f  # it waits for the next session
    f = _next(s, "spelling", fix=1, since=since)                     # and stays ended (no open-ended run)
    assert f["fix_end"]


def test_counts_agree_everywhere_and_a_fact_and_its_reverse_are_one(page):
    pid, s = _kid(page, 4, ("tables", "spelling"))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    now, day = datetime.datetime.utcnow(), datetime.date.today().isoformat()
    row = {"pupil_id": pid, "family_id": fam, "day": day, "ms": 3000}
    old = now - datetime.timedelta(hours=3)
    DB.attempts.insert_many([
        # 7 × 12 missed, then 12 × 7 right in a later sitting: put right (one fact)
        {**row, "activity": "tables", "correct": False, "detail": "7x12", "q": "7 × 12 =", "exp": "84", "got": "72",
         "ts": old},
        {**row, "activity": "tables", "correct": True, "detail": "12x7", "ts": old + datetime.timedelta(minutes=20)},
        # 9 × 5 missed, put right, then missed again: one to go over, not also put right
        {**row, "activity": "tables", "correct": False, "detail": "9x5", "q": "9 × 5 =", "exp": "45", "got": "40", "ts": old},
        {**row, "activity": "tables", "correct": True, "detail": "9x5", "ts": old + datetime.timedelta(minutes=5)},
        {**row, "activity": "tables", "correct": False, "detail": "5x9", "q": "5 × 9 =", "exp": "45", "got": "54",
         "ts": old + datetime.timedelta(minutes=30)},
        # a word missed and right again straight after (the same sitting): practised, comes back later
        {**row, "activity": "spelling", "correct": False, "detail": "because", "q": "Spell the word you heard",
         "exp": "because", "got": "becuase", "ts": now - datetime.timedelta(minutes=20)},
        {**row, "activity": "spelling", "correct": True, "detail": "because", "ts": now - datetime.timedelta(minutes=10)},
        # a word missed in an earlier sitting: due now
        {**row, "activity": "spelling", "correct": False, "detail": "people", "q": "Spell the word you heard",
         "exp": "people", "got": "peple", "ts": old},
    ])
    page.goto("/me")
    assert page.inner_text("[data-testid=fix-all]") == "Practise my mistakes (2)"        # 9 × 5 and people
    assert "1 more mistake comes back later" in page.inner_text("[data-testid=fix-later]")  # because
    assert "1 mistake put right" in page.inner_text("[data-testid=week-wins]")             # 7 × 12
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    total = page.inner_text("[data-testid=mistakes-total]")
    assert "3 to go over" in total and "1 put right" in total and "1 of them right again today" in total, total
    day_txt = page.locator("[data-testid=mistakes-day]").first.inner_text()
    assert "3 to go over · 1 put right since" in day_txt, day_txt
    assert day_txt.count("× 5") + day_txt.count("5 ×") == 1, day_txt                     # 9 × 5 shows once
    assert "put right before, then missed again" in day_txt
    page.goto(f"/children/{pid}/report")
    rep = page.inner_text("[data-testid=report-focus]")
    assert "Times tables still to put right: 5 × 9" in rep and "7 × 12" not in rep, rep
    assert "Spelling still to put right:" in rep and "because" in rep and "people" in rep, rep


def test_school_words_say_right_last_time_only_when_it_was(page):
    pid, s = _kid(page, 3, ("spelling",))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    today = datetime.date.today()
    DB.pupils.update_one({"_id": pid}, {"$set": {"school_words": {
        "words": [{"w": w} for w in ("water", "money", "again", "half")], "from": today.isoformat(),
        "until": (today + datetime.timedelta(days=7)).isoformat()}}})
    now, day = datetime.datetime.utcnow(), today.isoformat()
    row = {"pupil_id": pid, "family_id": fam, "day": day, "ms": 3000, "activity": "spelling"}
    for w, box in (("water", 1), ("money", 0), ("again", 0), ("half", 0)):
        DB.spelling_words.insert_one({"_id": f"{pid}:{w}", "pupil_id": pid, "family_id": fam, "word": w, "box": box,
                                      "right": 1 if w != "half" else 0, "wrong": 0 if w == "water" else 1, "due": day})
    DB.attempts.insert_many([
        {**row, "correct": False, "detail": "money", "q": "Spell the word you heard", "exp": "money", "got": "muny",
         "ts": now - datetime.timedelta(minutes=30)},
        {**row, "correct": True, "detail": "money", "ts": now - datetime.timedelta(minutes=25)},   # same sitting
        {**row, "correct": False, "detail": "half", "q": "Spell the word you heard", "exp": "half", "got": "harf",
         "ts": now - datetime.timedelta(minutes=30)},
        {**row, "correct": False, "detail": "again", "q": "Spell the word you heard", "exp": "again", "got": "agen",
         "ts": now - datetime.timedelta(hours=3)},
        {**row, "correct": True, "detail": "again", "ts": now - datetime.timedelta(hours=1)},      # a later sitting
    ])
    DB.spelling_words.update_one({"_id": f"{pid}:again"}, {"$set": {"box": 1}})
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    right = page.inner_text("[data-testid=school-right]")
    assert "water" in right and "again" in right and "money" not in right, right
    assert "money" in page.inner_text("[data-testid=school-again]")
    assert "half" in page.inner_text("[data-testid=school-tricky]") and "money" not in page.inner_text("[data-testid=school-tricky]")
    page.goto(f"/children/{pid}/report")
    rep = page.inner_text("[data-testid=report-focus]")
    assert "Spelling still to put right:" in rep and "money" in rep and "half" in rep and "again" not in rep, rep


def test_reporting_one_spelling_mistake_marks_only_that_word(page):
    pid, s = _kid(page, 5, ("spelling",))
    words = []
    for _ in range(3):
        q = _miss(s, "spelling")
        words.append(DB.items.find_one({"_id": q["token"]})["answer"])
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    first = page.locator("[data-testid=report-mistake]").first
    first.locator("summary").click()
    first.locator("button[data-testid=report-mistake-send]").click()
    page.wait_for_url("**reported=1**")
    assert page.locator("[data-testid=mistake-reported]").count() == 1
    assert page.locator("[data-testid=report-mistake]").count() == 2         # the other two can still be reported
    rep = DB.reports.find_one({"pupil_id": pid})
    att = DB.attempts.find_one({"_id": ObjectId(rep["attempt"])})
    assert rep["expected"] == att["exp"] and att["exp"] in words and rep["answer"] == "zzqx", rep
    # a new mistake on another word is not born "reported"
    enter_child(page, "Tia")
    q = _miss(s, "spelling")
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert page.locator("[data-testid=mistake-reported]").count() == 1
    # a child's own report from the drill marks only the word it was about
    enter_child(page, "Tia")
    q = _next(s, "spelling")
    w = DB.items.find_one({"_id": q["token"]})["answer"]
    assert s.post(BASE + "/api/report", json={"activity": "spelling", "token": q["token"], "reason": "wrong"}).json()["ok"]
    _check(s, "spelling", q["token"], "zzqx")
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert page.locator("[data-testid=mistake-reported]").count() == 2, w
