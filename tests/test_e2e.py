import json
import re

import pytest
import requests

from conftest import (BASE, DB, INVITE, PASSWORD, add_child, enter_child, last_mail, new_email, signup, unlock_parent,
                      wait_question)


def fam_of(email):
    return DB.accounts.find_one({"email": email})["family_id"]


def pupil(pid):
    return DB.pupils.find_one({"_id": pid})


# ---------------------------------------------------------------- public + guards ----
def test_public_pages_and_guards(page):
    for path, text in [("/", "Daily practice"), ("/privacy", "Privacy notice"), ("/terms", "Terms")]:
        r = page.goto(path)
        assert r.status == 200 and text in page.content()
    page.goto("/pricing")                       # no prices in this version
    assert page.url == BASE + "/" and "£" not in page.content()
    for path in ("/", "/signup", "/login"):
        page.goto(path)
        assert "£" not in page.content() and "four" not in page.inner_text("main").lower()
    page.goto("/home")
    assert page.url.endswith("/login")
    page.goto("/me")
    assert page.url.endswith("/login")
    assert requests.post(BASE + "/api/tables/next").status_code == 401
    # cross-site form posts are refused
    r = requests.post(BASE + "/login", data={"email": "a@example.test", "password": "x"},
                      headers={"Origin": "https://evil.example"})
    assert r.status_code == 403


# ---------------------------------------------------------------- accounts ----
def test_signup_verify_login_logout(page):
    email = new_email()
    page.goto("/signup")
    page.fill("#email", email)
    page.fill("#password", PASSWORD)
    page.fill("#invite", "WRONG")
    page.check("#consent")
    page.click("button[type=submit]")
    assert "invitation code is not valid" in page.content()
    signup(page, email)
    assert "Your email is verified" in page.content()
    # the same email cannot sign up twice
    page.context.clear_cookies()
    page.goto("/signup")
    page.fill("#email", email); page.fill("#password", PASSWORD); page.fill("#invite", INVITE); page.check("#consent")
    page.click("button[type=submit]")
    assert "already exists" in page.content()
    # sign in, wrong then right
    page.goto("/login")
    page.fill("#email", email); page.fill("#password", "nope-nope-1")
    page.click("button[type=submit]")
    assert "not right" in page.content()
    page.fill("#email", email); page.fill("#password", PASSWORD)
    page.click("button[type=submit]")
    page.wait_for_url("**/home")
    page.click("text=Sign out")
    page.wait_for_url(BASE + "/")
    page.goto("/home")
    assert page.url.endswith("/login")


def test_wrong_verification_code_and_resend(page):
    email = new_email()
    page.goto("/signup")
    page.fill("#email", email); page.fill("#password", PASSWORD); page.fill("#invite", INVITE); page.check("#consent")
    page.click("button[type=submit]")
    page.wait_for_url("**/verify")
    page.fill("#code", "000000")
    page.click("form[action='/verify'] button")
    assert "not right" in page.content()
    page.click("form[action='/verify/resend'] button")
    page.wait_for_url("**/verify?sent=1")
    assert DB.outbox.count_documents({"to": email}) == 2
    # unverified accounts cannot reach the parent area
    page.goto("/home")
    assert page.url.endswith("/verify")


def test_password_reset(page, browser):
    email = signup(page)
    other = browser.new_context(base_url=BASE).new_page()           # a second signed-in device
    other.goto("/login"); other.fill("#email", email); other.fill("#password", PASSWORD); other.click("button[type=submit]")
    other.wait_for_url("**/home")
    page.goto("/forgot")
    page.fill("#email", email)
    page.click("button[type=submit]")
    assert "reset link is on its way" in page.content()
    link = re.search(r"(/reset\?token=\S+)", last_mail(email, "Reset")["body"]).group(1)
    page.goto(link)
    page.fill("#password", "new-password-42")
    page.click("button[type=submit]")
    page.wait_for_url("**/login?reset=1")
    other.goto("/home")
    assert other.url.endswith("/login")                              # signed out everywhere
    page.goto(link)
    assert "expired or was already used" in page.content()
    page.goto("/login")
    page.fill("#email", email); page.fill("#password", "new-password-42"); page.click("button[type=submit]")
    page.wait_for_url("**/home")
    # forgot for an unknown email says the same thing and sends nothing
    page.goto("/forgot"); page.fill("#email", "nobody@example.test"); page.click("button[type=submit]")
    assert "reset link is on its way" in page.content()
    assert DB.outbox.count_documents({"to": "nobody@example.test"}) == 0


def test_login_rate_limit(page):
    email = signup(page)
    page.context.clear_cookies()
    for _ in range(8):
        page.goto("/login"); page.fill("#email", email); page.fill("#password", "wrong-pass-1"); page.click("button[type=submit]")
    page.goto("/login"); page.fill("#email", email); page.fill("#password", PASSWORD); page.click("button[type=submit]")
    assert "Too many attempts" in page.content()


# ---------------------------------------------------------------- children + plans ----
def test_children_validation_edit_and_plan_limits(page):
    email = signup(page)
    page.goto("/children/new")
    page.fill("#name", "Lina"); page.select_option("#year", "3"); page.fill("#pin", "12")
    page.eval_on_selector("form.card", "f => f.noValidate = true")      # test the server's own check
    page.click("form.card button[type=submit]")
    assert "PIN must be 4 digits" in page.content()
    pid = add_child(page, "Lina", 3)
    assert "Lina is ready" in page.content()
    p = pupil(pid)
    assert p["pin"] != "1234" and p["pin"].startswith("scrypt$") and p["year"] == 3
    assert p["activities"]["verbs"]["on"] and not p["activities"]["tables"]["on"] is False
    # edit: change year and a target, switch numbers off
    page.goto(f"/children/{pid}/edit")
    page.select_option("#year", "5")
    page.fill("[data-testid=target-maths]", "7")
    page.uncheck("[data-testid=on-numbers]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(f"**/children/{pid}")
    p = pupil(pid)
    assert p["year"] == 5 and p["activities"]["maths"]["target"] == 7 and not p["activities"]["numbers"]["on"]
    # free plan: one child, three activities
    DB.families.update_one({"_id": fam_of(email)}, {"$set": {"plan": "free"}})
    page.goto("/children/new")
    assert "needs the Family plan" in page.content() and "£" not in page.content()
    page.goto("/home")
    chips = page.locator("[data-testid='kid-Lina'] .chip").all_inner_texts()
    assert not any("Irregular" in c or "Numbers" in c for c in chips)
    DB.families.update_one({"_id": fam_of(email)}, {"$set": {"plan": "family"}})
    add_child(page, "Adam", 6)
    page.goto("/home")
    assert page.locator("[data-testid='kid-Adam']").count() == 1
    # delete a child removes their data
    page.goto(f"/children/{pid}/edit")
    page.once("dialog", lambda d: d.accept())
    page.click("form[action$='/delete'] button")
    page.wait_for_url("**/home?deleted=1")
    assert DB.pupils.count_documents({"_id": pid}) == 0


def test_child_mode_pin_and_parent_lock(page):
    signup(page)
    add_child(page, "Mia", 4, pin="4321")
    page.goto("/learn")
    form = page.locator("[data-testid='pin-Mia']")
    form.locator("input[name=pin]").fill("1111"); form.locator("button").click()
    assert "Wrong PIN" in page.content()
    enter_child(page, "Mia", "4321")
    assert "Hi Mia" in page.content()
    assert "can see your answers" in page.content()
    for path in ("/home", "/settings", "/children/new", "/account/export"):
        page.goto(path)
        assert page.url.endswith("/parent-unlock"), path
    page.goto("/parent-unlock")
    page.fill("#password", "not-it-123"); page.click("form[action='/parent-unlock'] button[type=submit]")
    assert "not right" in page.content()
    unlock_parent(page)
    assert "Hand over to a child" in page.content()


# ---------------------------------------------------------------- the drills ----
def _answer_simple(page, value):
    page.fill("#answer", str(value))
    page.click("#check")
    page.wait_for_selector("#feedback.yes, #feedback.no")


def test_tables_drill_to_target(page):
    signup(page)
    pid = add_child(page, "Tom", 4, targets={"tables": 4})
    enter_child(page, "Tom")
    page.click("[data-testid=tile-tables]")
    page.wait_for_url("**/me/tables")
    prev = None
    it = wait_question(page, "tables", pid, prev)
    prompt = page.inner_text("[data-testid=question]")
    a, op, b = re.match(r"(\d+) ([×÷]) (\d+)", prompt).groups()
    assert int(it["answer"]) == (int(a) * int(b) if op == "×" else int(a) // int(b))
    _answer_simple(page, int(it["answer"]) + 1)                       # a wrong answer first
    assert "Not quite" in page.inner_text("#feedback")
    for _ in range(4):
        page.click("#next") if page.is_visible("#next") else None
        prev = it["_id"]
        it = wait_question(page, "tables", pid, prev)
        _answer_simple(page, it["answer"])
        assert "Correct" in page.inner_text("#feedback")
    assert page.inner_text("#dayDone") == "4"
    page.goto("/me")
    assert "done" in page.inner_text("[data-testid=tile-tables]")


def test_spelling_drill_audio_and_answers(page):
    signup(page)
    pid = add_child(page, "Nour", 2, targets={"spelling": 2})
    enter_child(page, "Nour")
    page.goto("/me/spelling")
    it = wait_question(page, "spelling", pid)
    src = page.eval_on_selector("#audio", "a => a.getAttribute('src')")
    assert it["answer"] not in src                                       # the URL does not give the word away
    r = page.request.get(BASE + src)
    assert r.status == 200 and r.headers["content-type"] == "audio/mpeg" and len(r.body()) > 1000
    _answer_simple(page, it["answer"] + "x")
    assert it["answer"] in page.inner_text("#feedback")
    for _ in range(2):
        page.click("#next")
        it = wait_question(page, "spelling", pid, it["_id"])
        _answer_simple(page, it["answer"].upper())                        # capitals do not matter
        assert "Correct" in page.inner_text("#feedback")
    st = DB.spelling_words.find_one({"pupil_id": pid, "word": it["answer"]})
    assert st["box"] == 1


def test_numbers_drill(page):
    signup(page)
    pid = add_child(page, "Ilyas", 5, targets={"numbers": 3})
    enter_child(page, "Ilyas")
    page.goto("/me/numbers")
    it = None
    for _ in range(3):
        it = wait_question(page, "numbers", pid, it["_id"] if it else None)
        ans = it["answer"]
        if it["meta"]["mode"] == "words":
            ans = ans.replace("-", " ").upper()                            # hyphens and case are forgiven
        _answer_simple(page, ans)
        assert "Correct" in page.inner_text("#feedback"), it
        page.click("#next")
    it = wait_question(page, "numbers", pid, it["_id"])
    _answer_simple(page, "zero zero")
    assert "Not quite" in page.inner_text("#feedback")


def test_verbs_drill(page):
    signup(page)
    pid = add_child(page, "Yara", 6, targets={"verbs": 2})
    enter_child(page, "Yara")
    page.goto("/me/verbs")
    it = wait_question(page, "verbs", pid)
    page.fill("#past", it["answer"]["past"][0]); page.fill("#pp", "wrongform"); page.click("#check")
    page.wait_for_selector("#feedback.no")
    for _ in range(2):
        page.click("#next")
        it = wait_question(page, "verbs", pid, it["_id"])
        page.fill("#past", it["answer"]["past"][-1]); page.fill("#pp", it["answer"]["pp"][-1]); page.click("#check")
        page.wait_for_selector("#feedback.yes")
    assert page.inner_text("#dayDone") == "2"


def _answer_maths(page, doc, value):
    page.evaluate("v => { const h = document.getElementById('mHost'); h.__getValue = () => v; }", value)
    page.click("#check")
    page.wait_for_selector("#feedback.yes, #feedback.no")


@pytest.mark.parametrize("year", [1, 2, 3, 4, 5, 6, 7, 8])
def test_maths_drill_each_year(page, year):
    signup(page)
    pid = add_child(page, "Zak", year, targets={"maths": 3})
    enter_child(page, "Zak")
    page.goto("/me/maths")
    doc = wait_question(page, "maths", pid)
    assert doc["skill"].startswith(f"Y{year}.")
    assert page.locator("#mHost").count() == 1 and page.locator("#mHost >> *").count() > 0   # a component rendered
    _answer_maths(page, doc, "definitely wrong")
    assert "Answer:" in page.inner_text("#feedback")
    for _ in range(3):
        page.click("#next")
        doc = wait_question(page, "maths", pid, doc["_id"])
        if page.locator("#mHost input.m-input").count() and doc["answer_type"] in ("num", "int", "str", "frac"):
            page.fill("#mHost input.m-input", str(doc["answer"]))                       # type it like a child
            page.click("#check"); page.wait_for_selector("#feedback.yes, #feedback.no")
        else:
            _answer_maths(page, doc, doc["answer"])
        assert "Correct" in page.inner_text("#feedback"), doc
    m = DB.maths_mastery.find_one({"pupil": pid})
    assert m and m["score"] > 0
    assert page.inner_text("#dayDone") == "3"


def test_answer_cannot_be_replayed_or_used_by_another_child(page):
    signup(page)
    a = add_child(page, "Ana", 4)
    b = add_child(page, "Ben", 4)
    enter_child(page, "Ana")
    page.goto("/me/tables")
    it = wait_question(page, "tables", a)
    ok = page.evaluate("t => fetch('/api/tables/check', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({token:t, value:'1'})}).then(r => r.status)", it["_id"])
    assert ok == 200
    again = page.evaluate("t => fetch('/api/tables/check', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({token:t, value:'1'})}).then(r => r.status)", it["_id"])
    assert again == 409
    enter_child(page, "Ben")
    page.goto("/me/tables")
    wait_question(page, "tables", b)
    page.goto("/me/tables")                 # Ana's next token, served to Ben's session, must fail
    ana_token = DB.items.insert_one({"_id": "manual-ana-" + a, "pupil_id": a, "family_id": pupil(a)["family_id"], "activity": "tables",
                                     "answer": 4, "meta": {"fact": "2x2", "a": 2, "b": 2}, "done": False}).inserted_id
    st = page.evaluate("t => fetch('/api/tables/check', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({token:t, value:'4'})}).then(r => r.status)", ana_token)
    assert st == 409


def test_activity_not_in_plan_is_refused(page):
    email = signup(page)
    add_child(page, "Ola", 4)
    DB.families.update_one({"_id": fam_of(email)}, {"$set": {"plan": "free"}})
    enter_child(page, "Ola")
    page.goto("/me/verbs")
    assert page.url.endswith("/me")
    st = page.evaluate("() => fetch('/api/verbs/next', {method:'POST'}).then(r => r.status)")
    assert st == 403


# ---------------------------------------------------------------- board + rewards ----
def test_reward_board_and_parent_view(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "30 minutes of screen time")
    page.fill("#reward_threshold", "100")
    page.click("form[action='/settings'] button[type=submit]")
    page.wait_for_url("**/settings?saved=1")
    pid = add_child(page, "Sara", 4, targets={"maths": 1, "tables": 1, "spelling": 1, "numbers": 1, "verbs": 1})
    add_child(page, "Omar", 4)
    enter_child(page, "Sara")
    assert "At 100%: 30 minutes of screen time" in page.inner_text("[data-testid=reward]")
    for act in ("tables", "spelling", "numbers", "verbs", "maths"):
        page.goto(f"/me/{act}")
        doc = wait_question(page, act, pid)
        if act == "maths":
            _answer_maths(page, doc, doc["answer"])
        elif act == "verbs":
            page.fill("#past", doc["answer"]["past"][0]); page.fill("#pp", doc["answer"]["pp"][0]); page.click("#check")
            page.wait_for_selector("#feedback.yes")
        else:
            _answer_simple(page, doc["answer"])
        assert "Correct" in page.inner_text("#feedback"), act
    page.goto("/me")
    assert page.inner_text("[data-testid=day-pct]") == "100%"
    assert "You earned: 30 minutes of screen time" in page.inner_text("[data-testid=reward]")
    page.goto("/board")
    assert "30 minutes" in page.inner_text("[data-testid='board-Sara']")
    assert "0%" in page.inner_text("[data-testid='board-Omar']")
    unlock_parent(page)
    assert page.inner_text("[data-testid='kid-Sara'] [data-testid=pct]") == "100%"
    page.goto(f"/children/{pid}")
    assert "100%" in page.inner_text("[data-testid=history]")


# ---------------------------------------------------------------- isolation ----
def test_families_are_isolated(browser):
    pa = browser.new_context(base_url=BASE).new_page()
    pb = browser.new_context(base_url=BASE).new_page()
    signup(pa, family="Family A")
    a_child = add_child(pa, "Adam", 4)
    enter_child(pa, "Adam")
    pa.goto("/me/tables")
    a_item = wait_question(pa, "tables", a_child)
    signup(pb, family="Family B")
    b_child = add_child(pb, "Adam", 4)           # same first name in another family
    assert a_child != b_child
    for path in (f"/children/{a_child}", f"/children/{a_child}/edit"):
        assert pb.goto(path).status == 404
    st = pb.evaluate("pid => fetch('/learn/' + pid, {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:'pin=1234'}).then(r => r.status)", a_child)
    assert st == 404
    pb.goto("/board")
    assert pb.locator("[data-testid^=board-]").count() == 1
    enter_child(pb, "Adam")
    st = pb.evaluate("t => fetch('/api/tables/check', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({token:t, value:'1'})}).then(r => r.status)", a_item["_id"])
    assert st == 409
    assert DB.items.find_one({"_id": a_item["_id"]})["done"] is False      # A's question is untouched
    pa.context.close(); pb.context.close()


# ---------------------------------------------------------------- data rights ----
def test_export_and_delete_account(page):
    email = signup(page)
    pid = add_child(page, "Rami", 4, targets={"tables": 1})
    enter_child(page, "Rami")
    page.goto("/me/tables")
    it = wait_question(page, "tables", pid)
    _answer_simple(page, it["answer"])
    unlock_parent(page)
    with page.expect_download() as dl:
        page.evaluate("() => { const a = document.createElement('a'); a.href = '/account/export'; a.download = ''; document.body.appendChild(a); a.click(); }")
    data = json.loads(open(dl.value.path()).read())
    assert data["children"][0]["name"] == "Rami" and "pin" not in data["children"][0]
    assert "pw" not in data["accounts"][0] and len(data["attempts"]) == 1
    fid = fam_of(email)
    page.goto("/settings")
    page.fill("#confirm", "nope"); page.fill("#delpw", PASSWORD)
    page.click("form[action='/account/delete'] button")
    assert "Type DELETE" in page.content()
    page.fill("#confirm", "DELETE"); page.fill("#delpw", PASSWORD)
    page.click("form[action='/account/delete'] button")
    page.wait_for_url("**/?deleted=1")
    for c in ("accounts", "pupils", "sessions", "attempts", "tables_facts", "items"):
        assert DB[c].count_documents({"family_id": fid}) == 0, c
    assert DB.families.count_documents({"_id": fid}) == 0
    assert DB.outbox.count_documents({"to": email}) == 0
    page.goto("/login"); page.fill("#email", email); page.fill("#password", PASSWORD); page.click("button[type=submit]")
    assert "not right" in page.content()


# ---------------------------------------------------------------- phones ----
@pytest.mark.parametrize("device", ["iPhone 13", "Pixel 7"])
def test_phone_layout(browser, devices, device):
    spec = {k: v for k, v in devices[device].items() if k != "default_browser_type"}
    ctx = browser.new_context(base_url=BASE, **spec)
    page = ctx.new_page()
    signup(page)
    pid = add_child(page, "Lea", 4, targets={"tables": 1})
    for path in ("/", "/home", f"/children/{pid}", "/settings", "/learn"):
        page.goto(path)
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), path
    enter_child(page, "Lea")
    for path in ("/me", "/me/maths", "/me/tables", "/me/spelling", "/me/numbers", "/me/verbs", "/board"):
        page.goto(path)
        page.wait_for_timeout(400)
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), path
    before = DB.items.find_one({"pupil_id": pid, "activity": "tables"}, sort=[("created", -1)])
    page.goto("/me/tables")
    it = wait_question(page, "tables", pid, before["_id"] if before else None)
    page.tap("#answer"); page.fill("#answer", str(it["answer"])); page.tap("#check")
    page.wait_for_selector("#feedback.yes")
    ctx.close()
