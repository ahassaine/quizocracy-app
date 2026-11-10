"""A family's ordinary day: a short default plan by school year, plan changes that start tomorrow and never take
back an earned reward, a parent view that shows how the day went, and a clear finish line for the child."""
import datetime
import re

import requests

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _right(s, act):
    q = s.post(BASE + f"/api/{act}/next", json={}).json()
    ans = DB.items.find_one({"_id": q["token"]})["answer"]
    return s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": str(ans)}).json()


def test_default_day_by_year_with_minutes(page):
    signup(page)
    page.goto("/children/new")
    page.select_option("#year", "1")
    on = lambda: {k for k in ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")   # noqa: E731
                  if page.is_checked(f"[data-testid=on-{k}]")}
    assert on() == {"maths", "spelling"}
    assert page.is_disabled("[data-testid=on-tables]") and page.is_disabled("[data-testid=on-verbs]")
    m1 = int(page.inner_text("#planMin"))
    assert 8 <= m1 <= 18, m1
    page.fill("[data-testid=target-maths]", "20")                      # the estimate follows the targets
    page.dispatch_event("[data-testid=target-maths]", "input")
    assert int(page.inner_text("#planMin")) > m1
    page.select_option("#year", "8")
    assert on() == {"maths", "spelling", "grammar", "science"}           # no times tables for Year 8
    pid = add_child(page, "Amira", 8, year_defaults=True)
    acts = DB.pupils.find_one({"_id": pid})["activities"]
    assert {k for k, a in acts.items() if a["on"]} == {"maths", "spelling", "grammar", "science"}
    y1 = add_child(page, "Maya", 1, year_defaults=True)
    acts = DB.pupils.find_one({"_id": y1})["activities"]
    assert {k for k, a in acts.items() if a["on"]} == {"maths", "spelling"}
    page.goto(f"/children/{y1}")
    for k in ("tables", "grammar", "science", "verbs"):                  # switched off: no card
        assert page.locator(f"[data-testid=card-{k}]").count() == 0, k
    assert "spelt right on 3 different days" in page.inner_text("[data-testid=card-spelling]")
    assert "statutory" not in page.content()
    assert "1.0 Counting & place value" in page.inner_text("[data-testid=skills-maths]")
    rows = page.locator("[data-testid=history] tr").count()
    assert rows == 2, rows                                               # header + today: not 14 days of 0%


def test_plan_change_starts_tomorrow_and_reward_is_kept(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "Screen time")
    page.fill("#reward_threshold", "100")
    page.click("form[action='/settings'] button[type=submit]")
    pid = add_child(page, "Leo", 4, targets={"tables": 1}, year_defaults=True)
    page.goto(f"/children/{pid}/edit")                                   # not started: changes apply now
    assert "start straight away" in page.inner_text("[data-testid=plan-now]")
    page.uncheck("[data-testid=on-maths]")
    page.uncheck("[data-testid=on-spelling]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}.*"))
    enter_child(page, "Leo")
    s = _session(page)
    assert _right(s, "tables")["day"]["reward"] == "Screen time"
    page.goto("/me")
    assert "All done for today, well done Leo!" in page.inner_text("[data-testid=all-done]")

    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    assert "Changes start tomorrow" in page.inner_text("[data-testid=plan-tomorrow]")
    page.check("[data-testid=on-spelling]")
    page.fill("[data-testid=target-tables]", "30")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}.*"))
    p = DB.pupils.find_one({"_id": pid})
    tomorrow = (datetime.date.fromisoformat(p["plan_log"][-1]["from"]))
    assert p["activities"]["spelling"]["on"] and tomorrow > datetime.date.fromisoformat(DB.attempts.find_one({"pupil_id": pid})["day"])
    page.goto("/home")
    card = page.locator("[data-testid='kid-Leo']")
    assert card.locator("[data-testid=pct]").inner_text() == "100%"
    assert "Leo earned: Screen time" in card.inner_text()
    assert "Spelling" not in card.inner_text()                           # today keeps the plan it started with
    page.goto(f"/children/{pid}")
    assert "From tomorrow" in page.inner_text("[data-testid=plan-pending]")
    assert "Times tables 1/1" in page.inner_text("[data-testid=today]")

    # asked for explicitly, today changes too: the day opens again for what was added, but the earned reward stays
    page.goto(f"/children/{pid}/edit")
    page.check("[data-testid=plan-today]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}.*"))
    page.goto("/home")
    card = page.locator("[data-testid='kid-Leo']")
    assert "Spelling 0/" in card.inner_text()
    assert card.locator("[data-testid=pct]").inner_text() == "1%"                 # 1 of 30 tables, no spelling yet
    assert "Leo earned: Screen time" in card.inner_text()
    page.goto("/board")
    assert "Times tables 1/30" in page.inner_text("[data-testid='board-Leo']")      # words, not only icons


def test_history_keeps_each_days_plan_and_parent_sees_how_the_day_went(page):
    signup(page)
    pid = add_child(page, "Zak", 5, targets={"tables": 2}, year_defaults=True)
    p = DB.pupils.find_one({"_id": pid})
    # started yesterday with a plan of 2 tables; tables did 5 right (3 extra)
    enter_child(page, "Zak")
    s = _session(page)
    for _ in range(2):
        _right(s, "tables")
    # today: a rushed wrong answer, a mashed one, and a right answer typed straight after being shown
    q = s.post(BASE + "/api/tables/next", json={}).json()
    s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": "asdf", "ms": 600})
    rows = list(DB.attempts.find({"pupil_id": pid}).sort("ts", 1))
    day = rows[0]["day"]
    ystr = (datetime.date.fromisoformat(day) - datetime.timedelta(days=1)).isoformat()
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime.fromisoformat(ystr + "T12:00")}})
    base = {"pupil_id": pid, "family_id": p["family_id"], "activity": "tables", "ms": 4000}
    t0 = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    DB.attempts.insert_many([{**base, "correct": True, "detail": f"3x{i}", "day": ystr,
                              "ts": t0 + datetime.timedelta(seconds=10 * i)} for i in range(1, 6)])
    last = rows[-1]
    DB.attempts.insert_one({**base, "correct": True, "detail": last["detail"], "day": day,
                            "ts": last["ts"] + datetime.timedelta(seconds=8)})
    # the parent raises the target today: it starts tomorrow, yesterday keeps its 2
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=target-tables]", "25")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}.*"))
    page.goto(f"/children/{pid}")
    hist = page.locator("[data-testid=history] tr")
    assert hist.count() == 3                                              # header, today, yesterday
    yrow = hist.nth(2).inner_text()
    assert ystr in yrow and "2/2" in yrow and "+3" in yrow, yrow
    today_card = page.inner_text("[data-testid=today]")
    assert "4 answers" in today_card and "right first time" in today_card, today_card
    assert "1 wrong answer looks rushed" in today_card, today_card
    assert "1 right answer was typed within a minute" in today_card, today_card
    page.goto("/home")
    assert "rushed" in page.inner_text("[data-testid='kid-Zak'] [data-testid=day-stats]")
    # the mistake was put right: it moves to "put right since"
    page.goto(f"/children/{pid}")
    m = page.inner_text("[data-testid=mistakes-day]")
    assert "0 to go over" in m and "1 put right since" in m, m
