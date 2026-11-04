"""A wrong answer in any activity shows on the parent's child page with the question, what the child wrote
and the right answer; right answers do not."""
import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup, unlock_parent


def test_parent_sees_mistakes(browser):
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    pid = add_child(pg, "Mina", 6)

    ctx = browser.new_context(base_url=BASE)
    kid = ctx.new_page()
    kid.set_default_timeout(15000)
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Mina")
    s = requests.Session()
    for c in ctx.cookies():
        s.cookies.set(c["name"], c["value"])

    wrong = {"maths": {"value": "zzz"}, "tables": {"value": "9999"}, "spelling": {"value": "qqqq"},
             "numbers": {"value": "nope"}, "verbs": {"past": "goed", "pp": "goned"}}
    for act, body in wrong.items():
        q = s.post(BASE + "/api/%s/next" % act, json={}).json()
        assert q.get("ok"), (act, q)
        r = s.post(BASE + "/api/%s/check" % act, json={"token": q["token"], **body}).json()
        assert r.get("correct") is False, (act, r)
    # one right answer must not appear
    q = s.post(BASE + "/api/tables/next", json={}).json()
    ans = DB.items.find_one({"_id": q["token"]})["answer"]
    assert s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": str(ans)}).json()["correct"]

    rows = list(DB.attempts.find({"pupil_id": pid, "correct": False}))
    assert {r["activity"] for r in rows} == set(wrong) and all(r.get("q") and r.get("exp") for r in rows), rows
    assert not DB.attempts.find_one({"pupil_id": pid, "correct": True, "q": {"$exists": True}})

    unlock_parent(kid)
    kid.goto("/children/%s" % pid)
    day = kid.locator("[data-testid=mistakes-day]").first
    txt = day.inner_text()
    assert "5 to go over" in txt, txt
    for shown in ("zzz", "9999", "qqqq", "nope", "goed, goned", "Spell the word you heard", "Past forms of"):
        assert shown in txt, (shown, txt)
    ctx.close()
