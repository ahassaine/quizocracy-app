"""Siblings on one device: Switch signs the child out, a locked tile can be unlocked by a parent, parent mode
on a handed-over device times out, the parent can see a PIN, and sign-up keeps what was typed."""
import datetime
import re

import requests

from conftest import (BASE, DB, INVITE, PASSWORD, add_child, enter_child, last_mail, new_email, signup,
                      unlock_parent)


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def test_switch_signs_the_child_out(page):
    signup(page)
    add_child(page, "Maya", 1, pin="1111")
    add_child(page, "Leo", 4, pin="2222")
    enter_child(page, "Maya", "1111")
    page.click("header a:has-text('Switch')")
    page.wait_for_url("**/learn")
    assert page.locator("[data-testid=child-name]").count() == 0          # no "Maya" in the header any more
    page.goto("/me")
    assert page.url.endswith("/learn")                                    # nobody's day without a PIN
    assert _session(page).post(BASE + "/api/tables/next", json={}).status_code == 401
    enter_child(page, "Leo", "2222")
    assert "Hi Leo" in page.content()


def test_pin_lock_shows_time_and_parent_can_unlock(page):
    email = signup(page)
    mia = add_child(page, "Mia", 4, pin="4321")
    add_child(page, "Zak", 5, pin="9999")
    page.goto("/home")
    page.click("text=Hand over to a child")
    page.wait_for_url("**/learn")
    s = _session(page)
    codes = [s.post(BASE + f"/learn/{mia}", data={"pin": f"{i:04d}"}).status_code for i in range(6)]
    assert codes == [400] * 5 + [429]
    r = s.post(BASE + f"/learn/{mia}", data={"pin": "4321"})               # even the right PIN waits
    assert r.status_code == 429 and re.search(r"Mia is locked for [1-5] more minutes?", r.text)
    # on "Who's learning?": how long is left (never a clock time), and a grown-up unlock with the parent password
    page.goto("/learn")
    assert re.search(r"Mia is locked for [1-5] more minutes?", page.inner_text("[data-testid=locked-Mia]"))
    tile = page.get_by_test_id("tile-Mia")
    tile.locator("summary").click()
    tile.locator("input[name=password]").fill("wrong-password-1")
    tile.locator("button").click()
    assert "not right" in page.inner_text("[data-testid=tile-Mia]")
    page.get_by_test_id("tile-Mia").locator("input[name=password]").fill(PASSWORD)
    page.get_by_test_id("tile-Mia").locator("button").click()
    page.wait_for_url(f"**/learn?unlocked={mia}")
    enter_child(page, "Mia", "4321")
    # on Home, in parent mode
    for i in range(6):
        s.post(BASE + f"/learn/{mia}", data={"pin": f"{i:04d}"})
    unlock_parent(page)
    box = page.get_by_test_id("pin-locked")
    assert re.search(r"Mia is locked for [1-5] more minutes?", box.inner_text())
    box.locator("button").click()
    page.wait_for_url(f"**/home?unlocked={mia}")
    assert page.get_by_test_id("pin-locked").count() == 0
    assert DB.login_failures.count_documents({"email": f"pin:{mia}"}) == 0


def test_pin_messages_are_plain(page):
    signup(page)
    sophie = add_child(page, "Sophie", 2, pin="1357")
    page.goto("/learn")
    form = page.get_by_test_id("pin-Sophie")
    form.locator("input[name=pin]").fill("12")
    form.locator("button").click()
    assert "Sophie's PIN is 4 numbers" in page.content()
    assert DB.login_failures.count_documents({"email": f"pin:{sophie}"}) == 0      # a short PIN is not a guess
    page.get_by_test_id("pin-Sophie").locator("input[name=pin]").fill("1111")
    page.get_by_test_id("pin-Sophie").locator("button").click()
    assert "ask a grown-up to check it in Parent" in page.content()


def test_parent_sees_pin_and_saved_message(page):
    signup(page)
    pid = add_child(page, "Jack", 3, pin="2468")
    page.goto(f"/children/{pid}/edit")
    page.click("[data-testid=show-pin] summary")
    assert page.inner_text("[data-testid=pin-value]") == "2468"
    page.fill("#pin", "1739")
    page.click("form.card button[type=submit]")
    page.wait_for_url(f"**/children/{pid}/edit?saved=1&pin=1")
    assert "Saved." in page.inner_text("[data-testid=saved]") and "PIN changed" in page.inner_text("[data-testid=saved]")
    page.click("[data-testid=show-pin] summary")
    assert page.inner_text("[data-testid=pin-value]") == "1739"
    page.click("form.card button[type=submit]")                          # no PIN typed: just "Saved."
    page.wait_for_url(f"**/children/{pid}/edit?saved=1")
    assert "PIN changed" not in page.inner_text("[data-testid=saved]")
    exp = page.request.get("/account/export").json()
    assert all("pin_view" not in c and "pin" not in c for c in exp["children"])


def test_parent_mode_times_out_on_a_handed_over_device(page):
    email = signup(page)
    add_child(page, "Ife", 6)
    enter_child(page, "Ife")
    unlock_parent(page)                                                   # dad checks on the child's device
    tok = DB.sessions.find_one({"account_id": DB.accounts.find_one({"email": email})["_id"]})["_id"]
    DB.sessions.update_one({"_id": tok}, {"$set": {"seen_at": datetime.datetime.utcnow() - datetime.timedelta(minutes=6)}})
    page.goto(f"/home")
    assert page.url.endswith("/parent-unlock")
    assert "locked itself" in page.content()
    unlock_parent(page)
    assert "locked itself" not in page.content()


def test_parent_own_sign_in_does_not_time_out(page):
    email = signup(page)
    acc = DB.accounts.find_one({"email": email})["_id"]
    DB.sessions.update_many({"account_id": acc}, {"$set": {"seen_at": datetime.datetime.utcnow() - datetime.timedelta(minutes=30)}})
    page.goto("/home")
    assert page.url.endswith("/home")


def test_child_left_signed_in_goes_back_to_who_is_learning(page):
    email = signup(page)
    add_child(page, "Hana", 4)
    enter_child(page, "Hana")
    acc = DB.accounts.find_one({"email": email})["_id"]
    DB.sessions.update_many({"account_id": acc}, {"$set": {"seen_at": datetime.datetime.utcnow() - datetime.timedelta(hours=9)}})
    page.goto("/me")
    assert page.url.endswith("/learn")


def test_password_reset_emails_the_account_and_unlock_has_forgot(page):
    email = signup(page)
    add_child(page, "Tom", 4)
    enter_child(page, "Tom")
    page.goto("/parent-unlock")
    assert page.locator("a[href='/forgot']").count() == 1
    page.context.clear_cookies()
    requests.post(BASE + "/forgot", data={"email": email})
    tok = re.search(r"token=([\w-]+)", last_mail(email, "Reset")["body"]).group(1)
    page.goto(f"/reset?token={tok}")
    assert "8 characters or more" in page.inner_text("form")
    page.fill("#password", "short")
    page.click("form button[type=submit]")
    assert "8 characters or more" in page.inner_text(".err")
    page.fill("#password", "another-horse-7")
    page.click("form button[type=submit]")
    page.wait_for_url("**/login?reset=1")
    assert "was changed" in last_mail(email, "password was changed")["subject"]


def test_signup_keeps_fields_and_accepts_code_in_any_case(page):
    email = new_email()
    page.goto("/signup")
    page.fill("#email", email)
    page.fill("#password", PASSWORD)
    page.fill("#family_name", "The Okafors")
    if page.locator("#invite").count():
        page.fill("#invite", " " + " ".join(INVITE.lower()) + " ")          # "b e t a 2 0 2 6"
    page.click("button[type=submit]")                                     # forgot the tick box
    assert "parent or guardian" in page.inner_text(".err")
    assert page.input_value("#email") == email and page.input_value("#password") == PASSWORD
    assert page.input_value("#family_name") == "The Okafors"
    assert page.locator("[data-testid=consent-label] a").count() == 0    # no links inside the tappable label
    page.click("[data-testid=consent-label] span")                        # tapping the words ticks it
    assert page.is_checked("#consent")
    page.click("button[type=submit]")
    page.wait_for_url("**/verify")
    code = re.search(r"\b(\d{6})\b", last_mail(email, "code")["subject"]).group(1)
    page.fill("#code", code)
    page.click("form[action='/verify'] button")
    page.wait_for_url("**/home?welcome=1")
    assert page.inner_text("[data-testid=plan-chip]") == "Free during the beta"
    page.goto("/settings")
    assert "Free beta — every activity included" in page.inner_text("[data-testid=plan]")
    assert "£" not in page.content()
