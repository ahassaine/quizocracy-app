"""'Practise my mistakes' brings back exactly what the child got wrong until it is put right, and each child
can have their own reward instead of the family's."""
import datetime
import re

import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup, unlock_parent, wait_question


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def test_practise_my_mistakes(page):
    signup(page)
    pid = add_child(page, "Noor", 4)
    enter_child(page, "Noor")
    s = _session(page)
    q = s.post(BASE + "/api/tables/next", json={}).json()
    fact = DB.items.find_one({"_id": q["token"]})["meta"]["fact"]
    assert s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": "9999"}).json()["correct"] is False
    q = s.post(BASE + "/api/grammar/next", json={}).json()
    gq = DB.items.find_one({"_id": q["token"]})["meta"]
    assert s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": "zzqx"}).json()["correct"] is False

    # an earlier sitting: the answers are no longer fresh in mind, so the mistakes are ready to come back
    DB.attempts.update_many({"pupil_id": pid}, {"$set": {"ts": datetime.datetime.utcnow() - datetime.timedelta(hours=1)}})

    page.goto("/me")
    assert page.inner_text("[data-testid=fix-all]") == "Practise my mistakes (2)"
    assert page.inner_text("[data-testid=fix-tables]") == "1 to fix"
    page.click("[data-testid=fix-all]")
    page.wait_for_url("**/me/tables?fix=1*")
    doc = wait_question(page, "tables", pid)
    assert doc["meta"]["fact"] == fact                              # the same fact comes back
    assert "2 left" in page.inner_text("[data-testid=fix-msg]")    # the count of every subject, as on My day
    page.fill("#answer", str(doc["answer"]))
    page.click("#check")
    page.wait_for_selector("#feedback.yes")
    assert "1 left" in page.inner_text("[data-testid=fix-msg]")    # drops as soon as it is put right
    page.click("#next")

    # then straight on to the next subject's mistake: grammar, the very same question
    page.wait_for_url("**/me/grammar?fix=1&moved=1*")
    it = wait_question(page, "grammar", pid)
    assert (it["meta"]["skill"], it["meta"]["qid"]) == (gq["skill"], gq["qid"])
    assert "Now Grammar and punctuation · Putting a mistake right · 1 left" in page.inner_text("[data-testid=fix-msg]")
    q = s.post(BASE + "/api/grammar/next", json={"fix": 1}).json()          # the same question again (refresh)
    assert q["token"] == it["_id"]
    key = it["answer"]
    good = {"mcq": key.get("right"), "tap": key.get("hits"), "num": key.get("a")}.get(key["t"], (key.get("a") or [""])[0])
    assert s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": good}).json()["correct"]
    page.reload()                                 # the same session (its start is kept in the address): it ends
    assert "since=" in page.url
    assert "All your mistakes are done" in page.inner_text("[data-testid=fix-end]")
    assert page.is_visible("[data-testid=fix-end-back]")
    page.goto("/me")
    assert page.locator("[data-testid=fix-all]").count() == 0


def test_each_child_can_have_their_own_reward(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "Screen time")
    page.fill("#reward_threshold", "100")
    page.click("form[action='/settings'] button[type=submit]")
    page.wait_for_url("**/settings?saved=1")
    ones = {k: 1 for k in ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")}
    pid = add_child(page, "Adam", 4, targets=ones)
    page.goto(f"/children/{pid}/edit")
    page.fill("#reward_text", "A trip to the park")
    page.fill("#reward_threshold", "20")
    page.click("form.card button[type=submit]")
    page.wait_for_url(f"**/children/{pid}/edit?saved=1")
    add_child(page, "Lila", 4)

    enter_child(page, "Adam")
    assert "At 20%: A trip to the park" in page.inner_text("[data-testid=reward]")
    s = _session(page)
    for act in ("tables", "numbers"):                                 # 2 of 7 activities = 29%
        q = s.post(BASE + f"/api/{act}/next", json={}).json()
        ans = DB.items.find_one({"_id": q["token"]})["answer"]
        r = s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": str(ans)}).json()
    assert r["day"]["reward"] == "A trip to the park"
    page.goto("/me")
    assert "You earned: A trip to the park" in page.inner_text("[data-testid=reward]")
    unlock_parent(page)
    assert "Adam earned: A trip to the park" in page.inner_text("[data-testid='kid-Adam'] [data-testid=reward-earned]")
    page.goto("/learn")
    enter_child(page, "Lila")
    assert "At 100%: Screen time" in page.inner_text("[data-testid=reward]")   # no own reward: the family's


def test_parent_sees_how_to_help_tips(page):
    signup(page)
    pid = add_child(page, "Ravi", 1)
    page.goto(f"/children/{pid}")
    tips = page.inner_text("[data-testid=tips]")
    for title in ("Maths", "Spelling", "Grammar and punctuation", "Science"):
        assert title in tips, tips
    assert "Times tables" not in tips and "Irregular verbs" not in tips      # not in a Year 1 plan
    page.click("[data-testid=tips] details:first-child summary")
    assert "explain how they got an answer" in page.inner_text("[data-testid=tips]")
