"""The parent area stays locked when the device changes hands, wrong guesses are limited, mail cannot be flooded,
the day reaches 100% only when everything is done, and a page opened for one child never serves another."""
import re

import requests

from conftest import (BASE, DB, PASSWORD, add_child, enter_child, last_mail, new_email, signup, unlock_parent,
                      wait_question)


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _fam(email):
    return DB.accounts.find_one({"email": email})["family_id"]


def test_delete_confirm_with_apostrophe(page):
    signup(page)
    pid = add_child(page, "D'Arcy", 4)
    page.goto(f"/children/{pid}/edit")
    seen = []
    page.once("dialog", lambda d: (seen.append(d.message), d.dismiss()))
    page.click("form[action$='/delete'] button")
    page.wait_for_timeout(300)
    assert seen == ["Delete D'Arcy and all their practice data?"]
    assert DB.pupils.count_documents({"_id": pid}) == 1                 # cancelled: still there


def test_unlock_attempts_are_limited(page):
    signup(page)
    add_child(page, "Mia", 4)
    enter_child(page, "Mia")
    s = _session(page)
    codes = [s.post(BASE + "/parent-unlock", data={"password": f"wrong-{i}-pass"}, allow_redirects=False).status_code
             for i in range(8)]
    assert codes == [400] * 8
    r = s.post(BASE + "/parent-unlock", data={"password": PASSWORD}, allow_redirects=False)
    assert r.status_code == 429 and "Too many wrong passwords" in r.text
    page.goto("/parent-unlock")
    assert page.get_attribute("#password", "autocomplete") == "new-password"


def test_handover_locks_and_deleted_child_stays_locked(page, browser):
    email = signup(page)
    pid = add_child(page, "Sami", 4)
    add_child(page, "Lea", 5)
    page.goto("/home")
    page.click("text=Hand over to a child")
    page.wait_for_url("**/learn")
    assert page.locator("header a[href='/settings']").count() == 0      # no parent links once handed over
    for path in ("/home", "/settings", "/account/export", f"/children/{pid}/edit"):
        page.goto(path)
        assert page.url.endswith("/parent-unlock"), path
    # the tablet: Sami signs in; the parent deletes Sami from another device
    enter_child(page, "Sami")
    other = browser.new_context(base_url=BASE).new_page()
    other.goto("/login"); other.fill("#email", email); other.fill("#password", PASSWORD); other.click("button[type=submit]"); other.wait_for_url("**/home")
    other.request.post(f"/children/{pid}/delete")
    page.goto("/settings")
    assert page.url.endswith("/parent-unlock")
    unlock_parent(page)
    other.context.close()


def test_resend_is_throttled_and_keeps_the_guess_cap(page):
    email = new_email()
    page.goto("/signup")
    page.fill("#email", email); page.fill("#password", PASSWORD)
    if page.locator("#invite").count():
        page.fill("#invite", "BETA2026")
    page.check("#consent"); page.click("button[type=submit]"); page.wait_for_url("**/verify")
    s = _session(page)
    sent = [s.post(BASE + "/verify/resend", allow_redirects=False).status_code for _ in range(4)]
    assert sent == [303, 303, 429, 429] and DB.outbox.count_documents({"to": email}) == 3
    # 5 wrong tries kill a code, a new code does not reset the hourly cap of 10
    for _ in range(5):
        s.post(BASE + "/verify", data={"code": "000000"})
    r = s.post(BASE + "/verify", data={"code": "000000"})
    assert "no longer works" in r.text
    DB.login_failures.delete_many({"email": f"mail:verify:{email}"})   # let one more code out
    assert s.post(BASE + "/verify/resend", allow_redirects=False).status_code == 303
    for _ in range(5):
        s.post(BASE + "/verify", data={"code": "000000"})
    code = re.search(r"\b(\d{6})\b", last_mail(email, "code")["subject"]).group(1)
    r = s.post(BASE + "/verify", data={"code": code}, allow_redirects=False)
    assert r.status_code == 429 and "Too many wrong codes" in r.text


def test_forgot_is_throttled_and_replaces_old_links(page):
    email = signup(page)
    page.context.clear_cookies()
    for _ in range(5):
        requests.post(BASE + "/forgot", data={"email": email})
    assert DB.outbox.count_documents({"to": email, "subject": {"$regex": "Reset"}}) == 3
    assert DB.codes.count_documents({"email": email, "purpose": "reset"}) == 1


def test_family_full_message(page):
    email = signup(page)
    for i in range(6):
        DB.pupils.insert_one({"_id": f"p_full{i}{email[:6]}", "family_id": _fam(email), "name": f"K{i}", "year": 3,
                              "pin": "x", "activities": None, "created": i})
    page.goto("/home")
    assert page.locator("a[href='/children/new']").count() == 0
    page.goto("/children/new")
    assert "room for 6 children" in page.content() and "needs the Family plan" not in page.content()


def test_day_is_100_only_when_everything_is_done(page):
    signup(page)
    pid = add_child(page, "Amy", 4, targets={"tables": 1})
    # every activity complete except times tables: 199 of 200 would round up to 100%
    p = DB.pupils.find_one({"_id": pid})
    acts = {k: {**v, "target": 200 if k == "tables" else 1} for k, v in p["activities"].items()}
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": acts, "reward": {"text": "Ice cream", "threshold": 100}}})
    from datetime import datetime
    from zoneinfo import ZoneInfo
    day = datetime.now(ZoneInfo("Europe/London")).date().isoformat()
    rows = [{"pupil_id": pid, "family_id": p["family_id"], "activity": k, "correct": True, "day": day,
             "ts": datetime.utcnow(), "detail": ""} for k, v in acts.items() if v["on"]
            for _ in range(199 if k == "tables" else 1)]
    DB.attempts.insert_many(rows)
    enter_child(page, "Amy")
    assert page.inner_text("[data-testid=day-pct]") == "99%"
    assert "You earned" not in page.inner_text("[data-testid=reward]")


def test_two_tabs_two_children(page):
    signup(page)
    ben = add_child(page, "Ben", 4)
    add_child(page, "Ava", 5)
    enter_child(page, "Ben")
    page.goto("/me/tables")
    page.wait_for_function("document.body.dataset.qtoken")
    tab2 = page.context.new_page()
    enter_child(tab2, "Ava")
    page.fill("#answer", "1"); page.click("#check")
    page.wait_for_selector("#feedback.warn")
    assert "Ava is signed in on this device now" in page.inner_text("#feedback")
    assert page.locator("#feedback a[href='/learn']").count() == 1
    assert page.is_disabled("#check")
    # the API itself refuses a page opened for Ben
    r = _session(page).post(BASE + "/api/tables/next", json={"pupil": ben})
    assert r.status_code == 409 and r.json()["error"] == "switched"


def test_export_has_every_collection(page):
    signup(page)
    pid = add_child(page, "Rami", 4)
    enter_child(page, "Rami")
    page.goto("/me/maths")
    wait_question(page, "maths", pid)
    unlock_parent(page)
    exp = page.request.get("/account/export")
    assert exp.headers.get("cache-control") == "no-store"
    data = exp.json()
    for c in ("maths_attempts", "maths_mastery", "maths_lab_q", "items", "bank_state", "emails", "devices"):
        assert c in data, c
    assert len(data["maths_lab_q"]) >= 1 and data["exported"].endswith("Z")


def test_csrf_null_origin_and_api_no_store(page):
    signup(page)
    s = _session(page)
    r = s.post(BASE + "/settings", data={"family_name": "Hacked"}, headers={"Origin": "null"}, allow_redirects=False)
    assert r.status_code == 403
    r = s.post(BASE + "/settings", data={"family_name": "Mine"}, headers={"Origin": BASE}, allow_redirects=False)
    assert r.status_code == 303
    pid = add_child(page, "Zed", 4)
    enter_child(page, "Zed")
    r = _session(page).post(BASE + "/api/tables/next", json={"pupil": pid})
    assert r.status_code == 200 and r.headers.get("cache-control") == "no-store"


def test_locked_device_lands_on_who_is_learning(page):
    signup(page)
    pid = add_child(page, "O'Neill", 4)
    banner = page.locator(".ok form[action='/handover'] button")          # the "is ready" banner's button
    assert banner.count() == 1
    banner.click()
    page.wait_for_url("**/learn")
    page.goto("/")
    assert page.url.endswith("/learn")
    enter_child(page, "O'Neill")                                            # apostrophe names work in the helper
    assert DB.sessions.count_documents({"child_id": pid}) == 1


def test_expired_question_message_stays(page):
    signup(page)
    pid = add_child(page, "Kit", 4)
    enter_child(page, "Kit")
    page.goto("/me/tables")
    doc = wait_question(page, "tables", pid)
    DB.items.delete_one({"_id": doc["_id"]})                 # the question expires while on screen
    page.fill("#answer", "1"); page.click("#check")
    wait_question(page, "tables", pid, doc["_id"])
    page.wait_for_timeout(300)
    assert "expired" in page.inner_text("#feedback")
