"""The parent pages at a glance (wave 4): reported questions in plain words and reported from the mistakes list;
right first time per activity on Home and Progress; extra answers kept out of the day's score; the day's percent
weighed by planned answers; work in an unticked activity still shown; guesses and quick days said plainly;
mistakes the app cannot ask again in their own line; an abandoned Year 4 check; a school topic in a subject
not in the plan; the focus on Add a child; the email ticks saving without a reload; and SATs papers for Year 6."""
import datetime
import re
from zoneinfo import ZoneInfo

import requests

from app import progress
from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date().isoformat()


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _value(key, right=True):
    """A right (or wrong) value for an answer key of any activity."""
    if isinstance(key, dict) and key.get("t"):
        t = key["t"]
        if t == "mcq":
            return key["right"] if right else (key["right"] + 1) % len(key["opts"])
        if t == "tap":
            return key["hits"] if right else [i for i in range(len(key["words"])) if i not in key["hits"]][:1]
        if t == "num":
            return key["a"] if right else key["a"] + 1000
        return key["a"][0] if right else "zzqx"
    return str(key) if right else str(key) + "9"


def _answer(s, act, right=True, value=None):
    q = s.post(BASE + f"/api/{act}/next", json={}).json()
    key = DB.items.find_one({"_id": q["token"]})["answer"]
    v = _value(key, right) if value is None else value
    res = s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": v}).json()
    if res.get("retry"):                                     # "Nearly": a slip gets one free retry, then it counts
        res = s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": v}).json()
    return q, key, v, res


# ---- the rules themselves, without a server ----

def test_day_percent_weighs_planned_answers_and_shows_unplanned_work():
    off = {k: {"on": False, "target": 5} for k in ("tables", "spelling", "grammar", "numbers", "verbs")}
    pupil = {"_id": "p_x", "year": 8, "activities": {**off, "maths": {"on": True, "target": 20},
                                                       "science": {"on": True, "target": 5}}}
    fam = {"plan": "family"}
    st = progress.day_status(pupil, fam, {"science": {"correct": 5, "answered": 5}}, TODAY)
    assert st["pct"] == 20                                  # 5 of 25 planned answers, not half the day
    st = progress.day_status(pupil, fam, {"maths": {"correct": 20, "answered": 30}, "science": {"correct": 5, "answered": 6}}, TODAY)
    assert st["pct"] == 100
    st = progress.day_status(pupil, fam, {"maths": {"correct": 10, "answered": 10}, "verbs": {"correct": 4, "answered": 5}}, TODAY)
    assert st["pct"] == 40 and [u["key"] for u in st["unplanned"]] == ["verbs"]   # shown, never counted


def test_guesses_are_structure_only():
    assert progress._guessed("idk", "56") and progress._guessed("I don't know", "because")
    assert progress._guessed("thick, layer, fat", "fat")                 # every word tapped
    assert progress._guessed("250 255 261 238 364", "250, 364")         # every number in the list typed
    assert not progress._guessed("I do not know. dont", "I don't know.")
    assert not progress._guessed("54", "56") and not progress._guessed("the dog, the cat", "the cat")


# ---- the pages ----

def test_reports_read_in_plain_words_and_a_parent_reports_from_the_mistakes(page):
    signup(page)
    pid = add_child(page, "Grace", 6, targets={"grammar": 5}, year_defaults=True)
    enter_child(page, "Grace")
    s = _session(page)
    q, key, v, res = _answer(s, "grammar", right=False)
    assert not res["correct"]
    assert s.post(BASE + "/api/report", json={"activity": "grammar", "token": q["token"], "reason": "wrong",
                                              "answer": {"value": v}}).json()["ok"]
    _, key2, v2, res2 = _answer(s, "grammar", right=False)    # a second mistake, to report from the parent's page
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    body = page.inner_text("body")
    assert "{'t'" not in body and "'opts'" not in body and "'right'" not in body
    rep = page.locator("[data-testid=family-report]").first
    assert "Grace reported" in rep.inner_text()
    exp = DB.reports.find_one({"pupil_id": pid})["expected"]
    from app.bank import engine
    assert rep.locator("[data-testid=report-expected]").inner_text() == engine.expected_text(exp) + (f" {exp['unit']}" if exp.get("unit") else "")
    # "Report this question" under a mistake: the grown-up's own report, in the same queue
    n = DB.reports.count_documents({"pupil_id": pid})
    item = page.locator("[data-testid=report-mistake]").first
    item.locator("summary").click()
    item.locator("input[name=note]").fill("Two words fit this one")
    item.locator("[data-testid=report-mistake-send]").click()
    page.wait_for_url(re.compile(r".*reported=1.*"))
    assert DB.reports.count_documents({"pupil_id": pid}) == n + 1
    r = DB.reports.find_one({"pupil_id": pid, "by": {"$exists": True}})
    assert r["status"] == "open" and r["note"] == "Two words fit this one" and r["day"] == TODAY
    assert "You reported" in page.inner_text("[data-testid=reports]")
    assert page.locator("[data-testid=reported-ok]").count() == 1
    assert page.locator("[data-testid=mistake-reported]").count() >= 1      # that mistake now says "reported"


def test_glance_extras_guesses_and_cards_after_one_day(page):
    signup(page)
    pid = add_child(page, "Amir", 4, targets={"tables": 3, "spelling": 2}, year_defaults=True)
    enter_child(page, "Amir")
    s = _session(page)
    for _ in range(3):
        assert _answer(s, "tables")[3]["correct"]
    for _ in range(2):                                         # after the target: extra effort
        assert not _answer(s, "tables", right=False)[3]["correct"]
    _, _, _, r = _answer(s, "spelling", value="idk")           # a believable non-answer
    assert not r["correct"]
    unlock_parent(page)
    page.goto("/home")
    card = page.locator("[data-testid='kid-Amir']")
    stats = card.locator("[data-testid=day-stats]").inner_text()
    assert "75% right first time" in stats                    # 3 of 4 planned first tries; the 2 extras left out
    assert "2 more after the targets were met" in card.inner_text()
    assert "like a guess" in card.locator("[data-testid=flag-guesses]").inner_text()
    acc = card.locator("[data-testid=home-accuracy]").inner_text()
    assert "Times tables 60%" in acc and "needs help" in acc and "Spelling 0%" in acc
    page.goto(f"/children/{pid}")
    glance = page.inner_text("[data-testid=glance]")
    assert "Times tables" in glance and "60%" in glance and "To work on next" in glance
    assert "started" in page.inner_text("[data-testid=grown-tables]")    # not a bare 0/144 after a good day
    assert "re-checked on a later day" in page.inner_text("[data-testid=mastery-rule]")
    assert "guess" in page.inner_text("[data-testid=history]")


def test_unticked_activity_keeps_its_history_and_mistakes_the_app_cannot_ask(page):
    signup(page)
    pid = add_child(page, "Tom", 8, targets={"science": 5}, year_defaults=True)
    enter_child(page, "Tom")
    s = _session(page)
    for _ in range(2):
        _answer(s, "science")
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.uncheck("[data-testid=on-science]")
    page.check("[data-testid=plan-today]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}/edit.*"))
    # a mistake in an activity not in the plan: the parent sees it in a quiet line, the child is not asked it
    DB.attempts.insert_one({"pupil_id": pid, "family_id": DB.pupils.find_one({"_id": pid})["family_id"],
                            "activity": "numbers", "correct": False, "ms": 4000, "detail": "17", "day": TODAY,
                            "ts": datetime.datetime.utcnow(), "q": "Write 17 in words", "exp": "seventeen", "got": "sevnteen"})
    page.goto(f"/children/{pid}")
    assert "(not in the plan now)" in page.inner_text("[data-testid=today]")
    assert page.locator("[data-testid=history-unplanned]").count() >= 1
    assert page.locator("[data-testid=card-science] [data-testid=offplan]").count() == 1
    assert "won't ask again" in page.inner_text("[data-testid=mistakes-cannot]")


def test_an_abandoned_year4_check_counts_for_nothing(page):
    signup(page)
    pid = add_child(page, "Chidi", 4, targets={"tables": 20}, year_defaults=True)
    enter_child(page, "Chidi")
    s = _session(page)
    t = s.post(BASE + "/api/mtc/start", json={}).json()
    r = s.post(BASE + "/api/mtc/finish", json={"token": t["token"], "answers": [{"value": "", "ms": 6000}] * 25}).json()
    assert r["ok"] and r["unfinished"]
    p = DB.pupils.find_one({"_id": pid})
    assert not p.get("mtc") and len(p["mtc_open"]) == 1
    assert DB.attempts.count_documents({"pupil_id": pid}) == 0 and DB.tables_facts.count_documents({"pupil_id": pid}) == 0
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert "not finished" in page.inner_text("[data-testid=mtc-unfinished]")
    assert page.locator("[data-testid=mtc-scores]").count() == 0


def test_a_school_topic_outside_the_plan_is_flagged_with_a_fix_and_add_child_takes_a_focus(page):
    signup(page)
    page.goto("/children/new")
    page.fill("#name", "Lina")
    page.select_option("#year", "5")
    page.fill("#pin", "4826")
    page.click("[data-testid=new-focus] summary")
    opts = page.locator("[data-testid=new-focus-0] option").all_inner_texts()
    assert "Light" in opts or any("Earth and space" in o for o in opts)
    value = page.locator("[data-testid=new-focus-0] optgroup[label^='Science'] option").first.get_attribute("value")
    page.select_option("[data-testid=new-focus-0]", value)
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(r".*/children/p_[0-9a-f]+\?added=1"))
    pid = page.url.split("/children/")[1].split("?")[0]
    p = DB.pupils.find_one({"_id": pid})
    assert [(f["subject"], f["strand"]) for f in p["focus"]] == [tuple(value.split(":", 1))]
    assert not p["activities"]["science"]["on"]                      # Year 5's default day has no science
    warn = page.locator("[data-testid=focus-off]")
    assert "Science isn't in Lina's plan" in warn.inner_text()
    page.goto(f"/children/{pid}/edit")
    page.locator("[data-testid=focus-add]").click()
    page.wait_for_url(re.compile(rf".*/children/{pid}/edit\?saved=1"))
    assert DB.pupils.find_one({"_id": pid})["activities"]["science"]["on"]
    assert page.locator("[data-testid=focus-off]").count() == 0


def test_email_ticks_save_without_losing_a_typed_reward(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "30 minutes on the Switch")
    was = page.is_checked("[data-testid=weekly]")
    page.click("[data-testid=weekly]")                               # on by default: this turns it off
    page.get_by_text("Saved", exact=True).first.wait_for()
    assert DB.accounts.find_one({"email": page.inner_text("[data-testid=login-card] p").split()[0]})["weekly_email"] is (not was)
    assert page.url.endswith("/settings")                            # no reload
    assert page.input_value("#reward_text") == "30 minutes on the Switch"


def test_sats_papers_for_year6_and_the_revise_switch(page):
    signup(page)
    pid = add_child(page, "Daniel", 6, year_defaults=True)
    enter_child(page, "Daniel")
    s = _session(page)
    _answer(s, "grammar", right=False)
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    for k in ("arithmetic", "reasoning", "gps", "spelling"):
        assert page.locator(f"[data-testid=sats-{k}]").count() == 1
    assert "not a predicted mark" in page.inner_text("[data-testid=sats-honest]")
    assert "Not started yet" in page.inner_text("[data-testid=sats-reasoning]")
    page.click("[data-testid=sats-toggle]")
    page.wait_for_url(re.compile(r".*sats=on.*"))
    p = DB.pupils.find_one({"_id": pid})
    subjects = [f["subject"] for f in p["focus"]]
    assert len(subjects) == 3 and "maths" in subjects and "grammar" in subjects
    assert all(f["weeks"] == 2 for f in p["focus"])
    assert page.locator("[data-testid=sats-on]").count() == 1
    page.click("[data-testid=sats-toggle]")
    page.wait_for_url(re.compile(r".*sats=off.*"))
    assert not DB.pupils.find_one({"_id": pid}).get("focus")
    other = add_child(page, "Isla", 5, year_defaults=True)
    page.goto(f"/children/{other}")
    assert page.locator("[data-testid=sats]").count() == 0
