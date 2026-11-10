"""A second grown-up on the family (a co-parent, or a carer with fewer rights), changing the account email, and the
weekly summary email with its one-click unsubscribe."""
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, last_mail, new_email, signup, unlock_parent

ROOT = Path(__file__).resolve().parent.parent
CARER_PW = "grandma-minds-7"


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _invite(page, email, role="carer"):
    page.goto("/settings")
    page.fill("#invite_email", email)
    page.check(f"input[name=role][value={role}]")
    page.click("[data-testid=send-invite]")
    page.wait_for_url("**/settings?invited=1*")
    return re.search(r"/invite\?token=(\S+)", last_mail(email, "invited you")["body"]).group(1)


def _accept(page, token, password=CARER_PW):
    page.goto(f"/invite?token={token}")
    page.fill("#password", password)
    page.check("#consent")
    page.click("form[action='/invite'] button")


def test_carer_joins_with_own_login_and_limited_rights(page, browser):
    owner = signup(page, family="The Bakers")
    pid = add_child(page, "Sami", 4, pin="2468")
    carer = new_email("gran")
    tok = _invite(page, carer, "carer")
    page.goto("/settings")
    assert carer in page.get_by_test_id("invite-row").inner_text()

    other = browser.new_context(base_url=BASE).new_page()
    _accept(other, tok)
    other.wait_for_url("**/home?joined=1")
    assert "The Bakers" in other.get_by_test_id("joined").inner_text()
    acc = DB.accounts.find_one({"email": carer})
    assert acc["role"] == "carer" and acc["verified_at"] and acc["family_id"] == DB.accounts.find_one({"email": owner})["family_id"]
    # a used link no longer works
    other.goto(f"/invite?token={tok}")
    assert other.get_by_test_id("invite-invalid").count() == 1

    # sees Home, progress and the PINs; no child settings, no data, no invitations
    other.goto("/home")
    assert other.locator(f"a[href='/children/{pid}/edit']").inner_text() == "Spelling list & days off"   # no plan
    assert other.locator("a[href='/children/new']").count() == 0
    other.goto(f"/children/{pid}")
    assert other.locator("h1").inner_text() == "Sami"
    other.goto("/settings")
    assert other.get_by_test_id("pin-Sami").text_content() == "2468"
    assert other.locator("form[action='/settings/invite']").count() == 0
    assert other.locator("form[action='/account/delete']").count() == 0
    assert other.get_by_test_id("my-role").inner_text() == "Carer"
    s = _session(other)
    for path in ("/children/new", f"/children/{pid}/delete", "/account/export", "/account/email"):
        r = s.get(BASE + path, allow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == "/not-allowed", path
    for path, data in ((f"/children/{pid}/delete", {}), ("/account/delete", {"confirm": "DELETE", "password": CARER_PW}),
                       ("/settings/invite", {"email": new_email(), "role": "parent"}),
                       ("/settings", {"family_name": "Hacked"})):
        r = s.post(BASE + path, data=data, allow_redirects=False)
        assert r.headers.get("location") == "/not-allowed", path
    assert DB.pupils.count_documents({"_id": pid}) == 1
    assert DB.families.find_one({"_id": acc["family_id"]})["name"] == "The Bakers"
    r = s.get(BASE + "/not-allowed")
    assert r.status_code == 403 and owner in r.text

    # the carer hands over, the child plays, the carer's own password opens the parent area again
    other.goto("/home")
    other.click("text=Hand over to a child")
    other.wait_for_url("**/learn")
    enter_child(other, "Sami", "2468")
    other.goto("/parent-unlock")
    other.fill("#password", CARER_PW)
    other.click("form[action='/parent-unlock'] button[type=submit]")
    other.wait_for_url("**/home")

    # the owner sees and removes the carer: signed out everywhere, the login stops working
    page.goto("/settings")
    rows = page.get_by_test_id("adult")
    assert rows.count() == 2 and carer in rows.nth(1).inner_text()
    page.once("dialog", lambda d: d.accept())
    rows.nth(1).get_by_test_id("remove-adult").click()
    page.wait_for_url("**/settings?removed=1*")
    assert DB.accounts.count_documents({"email": carer}) == 0
    other.goto("/home")
    assert other.url.endswith("/login")
    assert "removed you" in last_mail(carer, "removed")["body"]
    other.context.close()


def test_any_adult_unlocks_and_the_device_takes_their_rights(page, browser):
    signup(page)
    add_child(page, "Mia", 4)
    carer = new_email("nan")
    _accept(browser.new_context(base_url=BASE).new_page(), _invite(page, carer))
    # the owner's tablet, handed over: the carer's password opens it, with a carer's rights
    page.goto("/home")
    page.click("text=Hand over to a child")
    page.wait_for_url("**/learn")
    page.goto("/parent-unlock")
    page.fill("#password", CARER_PW)
    page.click("form[action='/parent-unlock'] button[type=submit]")
    page.wait_for_url("**/home")
    page.goto("/settings")
    assert page.get_by_test_id("my-role").inner_text() == "Carer"
    # handed over again, the owner's password brings full rights back
    page.goto("/home")
    page.click("text=Hand over to a child")
    unlock_parent(page)
    page.goto("/settings")
    assert page.get_by_test_id("my-role").inner_text().startswith("Parent")


def test_parent_invite_gets_full_rights(page, browser):
    signup(page)
    pid = add_child(page, "Ola", 6)
    co = new_email("co")
    other = browser.new_context(base_url=BASE).new_page()
    _accept(other, _invite(page, co, "parent"), "co-parent-pass-1")
    other.wait_for_url("**/home?joined=1")
    other.goto(f"/children/{pid}/edit")
    assert other.url.endswith(f"/children/{pid}/edit")
    other.goto("/settings")
    assert other.locator("form[action='/settings/invite']").count() == 1
    # a second parent cannot remove the owner
    assert other.get_by_test_id("remove-adult").count() == 0
    # and signs in on its own
    other.context.clear_cookies()
    other.goto("/login")
    other.fill("#email", co)
    other.fill("#password", "co-parent-pass-1")
    other.click("form[action='/login'] button")
    other.wait_for_url("**/home")
    other.context.close()


def test_email_with_its_own_family_is_refused(page, browser):
    theirs = signup(browser.new_context(base_url=BASE).new_page(), family="Elsewhere")
    signup(page)
    page.goto("/settings")
    page.fill("#invite_email", theirs)
    page.click("[data-testid=send-invite]")
    assert "already has its own Quizocracy family" in page.locator("#adults .err").inner_text()
    assert not DB.outbox.find_one({"to": theirs, "subject": {"$regex": "invited you"}})
    # invited first, then they signed up elsewhere before accepting: refused at the link, nothing created
    late = new_email("late")
    tok = _invite(page, late)
    signup(browser.new_context(base_url=BASE).new_page(), email=late, family="Their own")
    other = browser.new_context(base_url=BASE).new_page()
    other.goto(f"/invite?token={tok}")
    assert "already has its own Quizocracy family" in other.get_by_test_id("invite-error").inner_text()
    _accept(other, tok)
    assert "already has its own" in other.get_by_test_id("invite-error").inner_text()
    assert DB.accounts.count_documents({"email": late}) == 1
    other.context.close()


def test_change_email_needs_the_code_from_the_new_address(page):
    old = signup(page)
    new = new_email("moved")
    taken = new_email("taken")
    DB.accounts.insert_one({"_id": "acc_t" + taken[:8], "email": taken, "pw": "x", "family_id": "fam_none",
                            "role": "owner", "verified_at": None})
    page.goto("/settings")
    page.click("[data-testid=change-email]")
    page.fill("#new_email", taken)
    page.fill("#password", PASSWORD)
    page.click("form[action='/account/email'] button")
    assert "already has a Quizocracy account" in page.locator(".err").inner_text()
    page.fill("#new_email", new)
    page.fill("#password", "not-my-password")
    page.click("form[action='/account/email'] button")
    assert "password is not right" in page.locator(".err").inner_text()
    page.fill("#password", PASSWORD)
    page.click("form[action='/account/email'] button")
    page.wait_for_url("**/account/email?sent=1")
    code = re.search(r"\b(\d{6})\b", last_mail(new, "code")["subject"]).group(1)
    assert DB.accounts.find_one({"email": old})                     # nothing changes before the code
    page.fill("#code", "000000" if code != "000000" else "111111")
    page.click("form[action='/account/email/confirm'] button")
    assert "not right" in page.locator(".err").inner_text()
    page.fill("#code", code)
    page.click("form[action='/account/email/confirm'] button")
    page.wait_for_url("**/settings?email_changed=1")
    assert DB.accounts.find_one({"email": new}) and not DB.accounts.find_one({"email": old})
    notice = last_mail(old, "email was changed")
    assert new in notice["body"] and "If this wasn't you, reply" in notice["body"]
    page.context.clear_cookies()
    page.goto("/login")
    page.fill("#email", new)
    page.fill("#password", PASSWORD)
    page.click("form[action='/login'] button")
    page.wait_for_url("**/home")
    DB.accounts.delete_one({"email": taken})


def _script(*args):
    env = {**os.environ, "QZ_MONGO_URL": os.getenv("QZ_TEST_MONGO", "mongodb://127.0.0.1:27027"),
           "QZ_DB": DB.name, "QZ_MAIL_MODE": "capture", "QZ_PUBLIC_URL": BASE}
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "weekly_email.py"), *args], env=env,
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return r.stdout


def _last_monday():
    t = datetime.date.today()
    return t - datetime.timedelta(days=t.weekday() + 7)


def test_weekly_email_once_per_week_with_unsubscribe(page):
    email = signup(page, family="The Weeklies")
    pid = add_child(page, "Noor", 4)
    fid = DB.accounts.find_one({"email": email})["family_id"]
    monday = _last_monday()
    rows = []
    for i in range(3):                        # three days of practice last week, some wrong and a fast miss
        day = (monday + datetime.timedelta(days=i)).isoformat()
        ts = datetime.datetime.combine(monday + datetime.timedelta(days=i), datetime.time(17))
        for j in range(6):
            rows.append({"pupil_id": pid, "family_id": fid, "activity": "tables", "correct": j % 3 != 0,
                         "ms": 900 if j == 0 else 4000, "detail": f"{j + 2}x7", "day": day,
                         "ts": ts + datetime.timedelta(seconds=20 * j), "q": "", "exp": "1", "got": "2"})
    DB.attempts.insert_many(rows)
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime.combine(monday, datetime.time(8))}})

    out = _script("--dry-run", "--to", email, "--week", monday.isoformat())
    assert "NOOR (Year 4)" in out and "18 answers" in out and "would send 1" in out
    assert not DB.weekly_sends.find_one({"family_id": fid})
    out = _script("--to", email, "--week", monday.isoformat())
    assert "sent 1" in out
    m = last_mail(email, "your week on Quizocracy")
    assert f"/children/{pid}" in m["body"] and "of 7 days" in m["body"] and "right first time" in m["body"]
    assert "given very fast" in m["body"] and "<html" in m["html"]
    out = _script("--to", email, "--week", monday.isoformat())
    assert "sent 0, already sent 1" in out
    # a family with no practice that week gets nothing
    assert "families with no activity 1" in _script("--to", email, "--week",
                                                    (monday - datetime.timedelta(days=14)).isoformat())

    # one-click unsubscribe from the email, no sign-in
    link = re.search(r"(/unsubscribe\?t=\S+)", m["body"]).group(1)
    page.context.clear_cookies()
    page.goto(link)
    page.get_by_test_id("unsubscribe").click()
    assert page.get_by_test_id("unsubscribed").count() == 1
    assert DB.accounts.find_one({"email": email})["weekly_email"] is False
    assert requests.post(BASE + "/unsubscribe?t=" + link.split("t=")[1][:-3] + "xyz").status_code == 400
    # and the switch in Settings turns it back on
    page.goto("/login")
    page.fill("#email", email)
    page.fill("#password", PASSWORD)
    page.click("form[action='/login'] button")
    page.wait_for_url("**/home")
    page.goto("/settings")
    assert not page.get_by_test_id("weekly").is_checked()
    page.get_by_test_id("weekly").check()
    page.get_by_text("Weekly summary: on", exact=True).first.wait_for()               # saved without a reload
    assert DB.accounts.find_one({"email": email})["weekly_email"] is True
