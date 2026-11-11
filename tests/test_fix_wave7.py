"""Wave 7, the child's side: "Practise my mistakes" ends cleanly. While a mistake waits for its gap the questions in
between are ones the child got right before, and a wrong answer to one of them is never a new mistake; a mistake
practised leaves the count, right or wrong, and rests until a later sitting; the round and My day say the same
"done for now"; moving on never shows the whole round's "N left" beside "done here". "I don't know" works in times
tables and spelling as in maths; a real word typed for a spelling word is "a different word", never "spelt
right", and its retype is kept as a copy; a new Year 2 child starts on × facts of 2, 5 and 10 up to 10 × 10."""
import datetime
import re

import requests

from conftest import BASE, DB, add_child, enter_child, signup

ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _kid(page, year, acts, name="Noor", target=10):
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


def _check(s, act, token, value, **extra):
    return s.post(BASE + f"/api/{act}/check", json={"token": token, "value": value, **extra}).json()


def _age(pid, minutes):
    for r in DB.attempts.find({"pupil_id": pid}):
        DB.attempts.update_one({"_id": r["_id"]}, {"$set": {"ts": r["ts"] - datetime.timedelta(minutes=minutes)}})


def _answer(act, token):
    doc = (DB.maths_lab_q if act == "maths" else DB.items).find_one({"_id": token})
    return doc, str(doc["answer"])


def _button(page):
    page.goto("/me")
    loc = page.locator("[data-testid=fix-all]")
    return int(re.search(r"\((\d+)\)", loc.inner_text()).group(1)) if loc.count() else 0


def test_filler_is_known_and_a_wrong_filler_answer_is_never_a_new_mistake(page):
    pid, s = _kid(page, 5, ("spelling",))
    right = []
    for _ in range(6):                                   # words spelt right in an earlier sitting: known
        q = _next(s, "spelling")
        _, w = _answer("spelling", q["token"])
        assert _check(s, "spelling", q["token"], w)["correct"]
        right.append(w)
    _age(pid, 120)
    q = _next(s, "spelling")
    _, missed = _answer("spelling", q["token"])
    assert _check(s, "spelling", q["token"], "zzqx")["correct"] is False
    assert _button(page) == 1
    f = _next(s, "spelling", fix=1)                      # straight away: the word waits for its gap
    since = f["fix_since"]
    assert not f["fixing"] and "some you already know" in f["fix_msg"], f
    for _ in range(3):
        _, w = _answer("spelling", f["token"])
        assert w in right and w != missed, (w, right)    # filler: a word spelt right before, never a new one
        r = _check(s, "spelling", f["token"], "zzqx")      # ... and a wrong answer to it
        assert r["correct"] is False
        f = _next(s, "spelling", fix=1, since=since)
        if f["fixing"]:
            break
    rows = list(DB.attempts.find({"pupil_id": pid, "fix": True, "correct": False}))
    assert rows and all(not r.get("fixing") for r in rows)
    assert _button(page) == 1                            # ... is never a new mistake: still the one word


def test_a_mistake_practised_leaves_the_count_even_when_missed_again(page):
    pid, s = _kid(page, 5, ("spelling", "tables"))
    for act in ("spelling", "spelling", "tables"):
        q = _next(s, act)
        assert _check(s, act, q["token"], "9999" if act == "tables" else "zzqx")["correct"] is False
    _age(pid, 90)                                        # an earlier sitting: all three due
    assert _button(page) == 3
    f = _next(s, "spelling", fix=1)
    since = f["fix_since"]
    assert f["fixing"] and f["fix_total"] == 3
    assert _check(s, "spelling", f["token"], "zzqx")["correct"] is False     # missed again: it rests
    assert _button(page) == 2                            # the count went down all the same
    later = page.inner_text("[data-testid=fix-later]")
    assert "1 more mistake comes back later" in later, later
    # the round goes on with the rest and ends with one "done for now", the same words My day then shows
    for _ in range(12):
        f = _next(s, "spelling", fix=1, since=since)
        if f.get("fix_end"):
            break
        if f.get("fix_next"):
            f = _next(s, f["fix_next"], fix=1, since=since)
            if f.get("fix_end"):
                break
        act = "tables" if DB.items.find_one({"_id": f["token"]})["activity"] == "tables" else "spelling"
        _check(s, act, f["token"], _answer(act, f["token"])[1])
    assert f.get("fix_end"), f
    assert f["fix_done"].startswith("All your mistakes for now are done ✓ · "), f["fix_done"]
    assert _button(page) == 0
    assert page.inner_text("[data-testid=fix-later]") == f["fix_done"]


def test_moving_on_says_done_here_without_the_rounds_count(page):
    pid, s = _kid(page, 5, ("spelling", "tables"))
    for act in ("spelling", "tables"):
        q = _next(s, act)
        assert _check(s, act, q["token"], "9999" if act == "tables" else "zzqx")["correct"] is False
    _age(pid, 90)
    for vp in ({"width": 390, "height": 844}, {"width": 1280, "height": 800}):
        page.set_viewport_size(vp)
        page.goto("/me")
        page.click("[data-testid=fix-all]")
        page.wait_for_function("document.body.dataset.qtoken")
        act = page.url.split("/me/")[1].split("?")[0]
        tok = page.evaluate("document.body.dataset.qtoken")
        page.fill("#answer", _answer(act, tok)[1])
        page.click("#check")
        page.wait_for_selector("#next:visible")
        page.click("#next")
        card = page.wait_for_selector("[data-testid=fix-move]")
        line = page.inner_text("[data-testid=fix-move-line]")
        title = "Spelling" if act == "spelling" else "Times tables"
        assert line == f"{title}: all done for now ✓", line
        assert page.inner_text("[data-testid=fix-msg]").strip() == ""          # no "1 left" beside it
        assert "(1) →" in page.inner_text("[data-testid=fix-move-go]")
        assert card.is_visible()
        page.click("[data-testid=fix-move-go]")
        page.wait_for_function("document.body.dataset.qtoken")
        nact = page.url.split("/me/")[1].split("?")[0]
        assert nact != act
        if vp["width"] == 390:                           # the first round is done: make both due again
            DB.attempts.delete_many({"pupil_id": pid, "correct": True})
            DB.attempts.update_many({"pupil_id": pid}, {"$unset": {"fix": "", "fixing": ""}})
            DB.pupils.update_one({"_id": pid}, {"$unset": {"fix_batch": ""}})
            DB.items.update_many({"pupil_id": pid}, {"$set": {"done": True}})
            _age(pid, 90)


def test_i_dont_know_in_times_tables_and_spelling(page):
    pid, s = _kid(page, 4, ("tables", "spelling"))
    q = _next(s, "tables")
    r = _check(s, "tables", q["token"], "", idk=True)
    _, ans = _answer("tables", q["token"])
    assert r["idk"] and r["correct"] is False and str(r["expected"]) == ans and r["hint"].startswith("Tip: "), r
    q = _next(s, "spelling")
    _, word = _answer("spelling", q["token"])
    r = _check(s, "spelling", q["token"], "", idk=True)
    assert r["idk"] and r["correct"] is False and r["expected"] == word and r["hint"] == f"{word}: " + ", ".join(word), r
    rows = list(DB.attempts.find({"pupil_id": pid, "idk": True}))
    assert {x["activity"] for x in rows} == {"tables", "spelling"}
    # the button is on both pages, beside Check, and says "That's OK"
    for act in ("tables", "spelling"):
        page.goto(f"/me/{act}")
        page.wait_for_function("document.body.dataset.qtoken")
        assert page.is_visible("[data-testid=idk]")
        page.click("[data-testid=idk]")
        page.wait_for_selector("[data-testid=idk-said]")
        assert page.is_visible("[data-testid=hint]")


def test_another_real_word_is_a_different_word_and_its_retype_a_copy(page):
    pid, s = _kid(page, 2, ("spelling",))
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.items.insert_one({"_id": "fight-" + pid, "pupil_id": pid, "family_id": fam, "activity": "spelling",
                         "answer": "fight", "meta": {}, "created": datetime.datetime.utcnow(), "done": False})
    r = _check(s, "spelling", "fight-" + pid, "rite")
    assert r["retry"] and r["other"], r
    assert r["hint"] == "'rite' is a different word. The word was fight. Listen again.", r
    assert "spelt right" not in r["hint"] + r["spoken"]
    r = _check(s, "spelling", "fight-" + pid, "fight")             # the retype, straight after being given the word
    assert r["correct"] and r["again_later"], r
    row = DB.attempts.find_one({"pupil_id": pid, "correct": True})
    assert row["copied"] and row["detail"] == "fight", row          # a copy, not a plain right first try


def test_a_new_year_2_child_starts_on_times_facts_up_to_10x10(page):
    pid, s = _kid(page, 2, ("tables",))
    for _ in range(40):
        q = _next(s, "tables")
        assert "÷" not in q["prompt"], q["prompt"]
        a, b = (int(n) for n in re.findall(r"\d+", q["prompt"]))
        assert ({a, b} & {2, 5, 10}) and a <= 10 and b <= 10, q["prompt"]
        DB.items.update_one({"_id": q["token"]}, {"$set": {"done": True}})
    # once a fact is known (right twice in a row), it may come as division too
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.tables_facts.insert_many([{"_id": f"{pid}:{t}x{n}", "pupil_id": pid, "family_id": fam, "a": t, "b": n,
                                  "right": 2, "wrong": 0, "streak": 2} for t in (2, 5, 10) for n in range(1, 11)])
    seen = set()
    for _ in range(40):
        q = _next(s, "tables")
        seen.add("÷" in q["prompt"])
        DB.items.update_one({"_id": q["token"]}, {"$set": {"done": True}})
    assert seen == {True, False}
