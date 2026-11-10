"""Trust between the grown-ups of one family: deleting a child, two parents editing at once, changing a role, what a
carer may change, the family activity log and its few emails, question reports the family can follow, "Change
today's plan too" and rest days told the same way everywhere, and up to three school topics."""
import datetime
import re
import secrets
from zoneinfo import ZoneInfo

import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, last_mail, new_email, signup, unlock_parent

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date()
CO_PW = "co-parent-pass-1"


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _join(page, browser, role="parent", password=CO_PW, name=None):
    """Invite a second grown-up from `page` and accept in a new browser; returns (their page, their email)."""
    email = new_email(role)
    page.goto("/settings")
    page.fill("#invite_email", email)
    page.check(f"input[name=role][value={role}]")
    page.click("[data-testid=send-invite]")
    page.wait_for_url("**/settings?invited=1*")
    tok = re.search(r"/invite\?token=(\S+)", last_mail(email, "invited you")["body"]).group(1)
    other = browser.new_context(base_url=BASE).new_page()
    other.goto(f"/invite?token={tok}")
    other.fill("#password", password)
    other.check("#consent")
    other.click("form[action='/invite'] button")
    other.wait_for_url("**/home?joined=1")
    if name:
        other.goto("/settings")
        other.fill("[data-testid=my-name]", name)
        other.click("form[action='/settings/name'] button")
    return other, email


def _save(page, pid):
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}/edit.*"))


def _right(s, activity):
    q = s.post(BASE + f"/api/{activity}/next", json={}).json()
    it = DB.items.find_one({"_id": q["token"]})
    return s.post(BASE + f"/api/{activity}/check", json={"token": q["token"], "value": it["answer"]}).json()


def test_deleting_a_child_needs_a_password_and_tells_the_other_parents(page, browser):
    owner = signup(page, family="The Hartleys")
    pid = add_child(page, "Testy", 2)
    jo, _ = _join(page, browser, "parent", name="Jo")
    jo.goto(f"/children/{pid}/edit")
    # the delete button is far from Save, and leads to its own page
    save = jo.locator("form.card button[type=submit]").bounding_box()
    link = jo.locator("[data-testid=delete-child-link]")
    assert link.bounding_box()["y"] - (save["y"] + save["height"]) >= 40
    link.click()
    jo.wait_for_url(f"**/children/{pid}/delete")
    assert "other parents" in jo.inner_text("[data-testid=delete-child]")
    jo.fill("[data-testid=delete-password]", "not-my-password")
    jo.click("[data-testid=delete-confirm]")
    assert "not right" in jo.inner_text(".err")
    assert DB.pupils.count_documents({"_id": pid}) == 1
    jo.fill("[data-testid=delete-password]", CO_PW)
    jo.click("[data-testid=delete-confirm]")
    jo.wait_for_url("**/home?deleted=1*")
    assert "Testy's profile is deleted" in jo.inner_text("[data-testid=child-deleted]")
    assert DB.pupils.count_documents({"_id": pid}) == 0
    m = last_mail(owner, "deleted")
    assert m["subject"] == "Jo deleted Testy's profile on Quizocracy" and "cannot be undone" in m["body"]
    # the owner sees it in the family activity log too
    page.goto("/home")
    assert "Jo deleted Testy's profile" in page.inner_text("[data-testid=family-log]")
    # a carer cannot delete at all
    gran, _ = _join(page, browser, "carer", password="gran-minds-77")
    pid2 = add_child(page, "Leo", 5)
    s = _session(gran)
    assert s.post(BASE + f"/children/{pid2}/delete", data={"password": "gran-minds-77"},
                  allow_redirects=False).headers["location"] == "/not-allowed"
    assert DB.pupils.count_documents({"_id": pid2}) == 1
    for p in (jo, gran):
        p.context.close()


def test_two_parents_saving_at_once_keep_each_others_changes(page, browser):
    signup(page, family="The Hartleys")
    pid = add_child(page, "Leo", 5, targets={"spelling": 8}, year_defaults=True)
    jo, _ = _join(page, browser, "parent", name="Jo")
    page.goto(f"/children/{pid}/edit")                     # Mark opens the page first...
    jo.goto(f"/children/{pid}/edit")
    jo.fill("[data-testid=target-spelling]", "6")          # ... Jo changes spelling and saves
    _save(jo, pid)
    page.fill("#reward_text", "Pick the Friday film")      # Mark changes only the reward, on his old page
    _save(page, pid)
    p = DB.pupils.find_one({"_id": pid})
    assert p["activities"]["spelling"]["target"] == 6 and p["reward"]["text"] == "Pick the Friday film"
    note = page.inner_text("[data-testid=save-note]")
    assert note.startswith("Jo also saved Leo's settings at") and "their changes stay" in note
    assert "You both changed" not in note
    # the same field changed by both: the later save wins, and says so
    page.goto(f"/children/{pid}/edit")
    jo.goto(f"/children/{pid}/edit")
    jo.fill("[data-testid=target-maths]", "12")
    _save(jo, pid)
    page.fill("[data-testid=target-maths]", "9")
    _save(page, pid)
    assert DB.pupils.find_one({"_id": pid})["activities"]["maths"]["target"] == 9
    assert "You both changed the daily plan" in page.inner_text("[data-testid=save-note]")
    page.goto(f"/children/{pid}/edit")
    assert "Last changed by Jo" not in page.inner_text("main")    # Mark saved last
    jo.goto(f"/children/{pid}/edit")
    assert jo.inner_text("[data-testid=last-edit]").startswith("Last changed by")
    # without the page's script nothing tells what was edited: a page opened before another save is refused
    loaded = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat()
    r = _session(page).post(BASE + f"/children/{pid}/edit", data={"loaded": loaded, "name": "Leo", "year": "5",
                                                                   "reward_text": "", "custom": "1"})
    assert r.status_code == 409 and "after you opened this page" in r.text
    assert DB.pupils.find_one({"_id": pid})["reward"]["text"] == "Pick the Friday film"
    jo.context.close()


def test_change_role_keeps_the_login_and_a_carer_types_the_school_list(page, browser):
    owner = signup(page)
    pid = add_child(page, "Leo", 5, year_defaults=True)
    jo, jo_email = _join(page, browser, "parent", name="Jo")
    assert last_mail(owner, "joined")["subject"] == f"{jo_email} joined Test family on Quizocracy"
    jo.goto("/settings")
    jo.uncheck("[data-testid=weekly]")                     # Jo had turned her weekly email off (saved without a reload)
    jo.get_by_text("Weekly summary: off", exact=True).first.wait_for()
    page.goto("/settings")
    row = page.locator("[data-testid=adult]", has_text=jo_email)
    assert "invited by" in row.inner_text()
    row.locator("[data-testid=change-role]").click()
    page.wait_for_url("**/settings?role_changed=*")
    assert "Jo is now a carer" in page.inner_text("[data-testid=role-changed]")
    acc = DB.accounts.find_one({"email": jo_email})
    assert acc["role"] == "carer" and acc["weekly_email"] is False
    assert "You are now a carer" in last_mail(jo_email, "now a")["subject"]
    assert not DB.outbox.find_one({"to": jo_email, "subject": {"$regex": "removed"}})
    # still signed in, now with a carer's rights: the school list and days off, nothing else
    jo.goto("/home")
    jo.click("text=Spelling list & days off")
    jo.wait_for_url(f"**/children/{pid}/edit")
    assert jo.locator("[data-testid=target-maths]").count() == 0 and jo.locator("[data-testid=delete-child-link]").count() == 0
    jo.fill("[data-testid=school-words]", "believe, receive, ceiling")
    jo.fill("[data-testid=off-from]", (TODAY + datetime.timedelta(days=2)).isoformat())
    _save(jo, pid)
    p = DB.pupils.find_one({"_id": pid})
    assert [w["w"] for w in p["school_words"]["words"]] == ["believe", "receive", "ceiling"]
    assert p["days_off"] == [{"from": (TODAY + datetime.timedelta(days=2)).isoformat()} | {"to": (TODAY + datetime.timedelta(days=2)).isoformat()}]
    # anything else a carer posts is left alone
    r = _session(jo).post(BASE + f"/children/{pid}/edit", data={"name": "Hacked", "on_maths": "", "target_maths": "99",
                                                                 "custom": "1", "off_form": "1"}, allow_redirects=False)
    assert r.status_code == 303
    p = DB.pupils.find_one({"_id": pid})
    assert p["name"] == "Leo" and p["activities"]["maths"]["target"] != 99
    # and back to parent, same login
    page.goto("/settings")
    page.locator("[data-testid=adult]", has_text=jo_email).locator("[data-testid=change-role]").click()
    assert DB.accounts.find_one({"email": jo_email})["role"] == "parent"
    jo.goto(f"/children/{pid}/edit")
    assert jo.locator("[data-testid=target-maths]").count() == 1
    page.goto("/home")
    log = page.text_content("[data-testid=family-log]")
    assert "changed Jo from Parent to Carer" in log and "joined as parent" in log
    jo.context.close()


def test_lockouts_unlocks_pin_changes_and_new_devices_are_logged(page, browser):
    owner = signup(page, family="The Hendersons")
    pid = add_child(page, "Ruby", 2, pin="1111")
    pat, _ = _join(page, browser, "carer", password="pat-minds-ruby", name="Pat")
    pat.goto("/home")
    pat.click("text=Hand over to a child")
    pat.wait_for_url("**/learn")
    for _ in range(6):
        form = pat.get_by_test_id("pin-Ruby")
        form.locator("input[name=pin]").fill("9999")
        form.locator("button").click()
    assert "locked for 5 more minutes" in pat.inner_text("[data-testid=locked-Ruby]")
    s = _session(pat)
    r = s.post(BASE + f"/children/{pid}/pin-unlock", data={"password": "pat-minds-ruby"}, allow_redirects=False)
    assert r.status_code == 303
    # the PIN changed by the owner
    page.goto(f"/children/{pid}/edit")
    page.fill("#pin", "2222")
    _save(page, pid)
    page.goto("/home")
    lines = page.locator("[data-testid=log-line]").all_text_contents()
    assert any("changed Ruby's PIN" in x for x in lines)
    assert any("Pat unlocked Ruby" in x for x in lines)
    assert any("Ruby was locked out after 6 wrong PINs" in x for x in lines)
    assert not DB.outbox.find_one({"to": owner, "subject": {"$regex": "unlock|PIN"}})      # routine: no email
    # a sign-in from a new browser: one line in the log, one email to that login; the same browser again: nothing
    n = DB.outbox.count_documents({"to": owner, "subject": {"$regex": "New sign-in"}})
    other = browser.new_context(base_url=BASE, user_agent="Mozilla/5.0 (Linux; Android 14) Chrome/130.0 Mobile Safari/537.36").new_page()
    for _ in range(2):
        other.goto("/login")
        other.fill("#email", owner)
        other.fill("#password", PASSWORD)
        other.click("form[action='/login'] button")
        other.wait_for_url("**/home")
    assert DB.outbox.count_documents({"to": owner, "subject": {"$regex": "New sign-in"}}) == n + 1
    m = last_mail(owner, "New sign-in")
    assert "Chrome on Android" in m["body"] and "If this wasn't you" in m["body"]
    assert "signed in on a new device (Chrome on Android)" in other.inner_text("[data-testid=family-log]")
    for p in (pat, other):
        p.context.close()


def test_question_reports_reach_the_family_with_the_outcome(page, browser):
    owner = signup(page)
    pid = add_child(page, "Rohan", 3, targets={"tables": 5}, year_defaults=True)
    enter_child(page, "Rohan")
    s = _session(page)
    q = s.post(BASE + "/api/tables/next", json={}).json()
    it = DB.items.find_one({"_id": q["token"]})
    s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": str(int(it["answer"]) - 2)})
    assert s.post(BASE + "/api/report", json={"activity": "tables", "token": q["token"], "reason": "wrong",
                                              "note": "I think it's 54", "answer": str(int(it["answer"]) - 2)}).json()["ok"]
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    rep = page.locator("[data-testid=family-report]").first
    assert "Rohan reported:" in rep.inner_text() and "I think it's 54" in rep.inner_text()
    assert rep.locator("[data-testid=report-outcome]").inner_text() == "we're checking"
    assert page.locator("[data-testid=mistake-reported]").count() == 1          # the mistake says it was reported
    # the team marks it, with a note; the email goes to a grown-up who has it ticked (on for new families since
    # wave 5; it can be unticked in Settings or on the progress page)
    page.goto("/settings")
    assert page.is_checked("[data-testid=report-emails]")
    slug = "".join(secrets.choice("abcdefghjkmnpqrstuvwxyz23456789") for _ in range(10))
    DB.team_members.insert_one({"_id": slug, "name": "Meriem", "initials": "Me", "role": "member", "telegram_chat_id": None,
                                "active": True, "created": datetime.datetime.utcnow()})
    rid = DB.reports.find_one({"pupil_id": pid})["_id"]
    team = browser.new_context(base_url=BASE).new_page()
    team.goto(f"/team/{slug}/reports")
    card = team.locator(f"#r{rid}")
    card.locator("[data-testid=report-reply-input]").fill("The answer is right: 8 × 7 = 56.")
    card.locator("[data-testid=set-not_a_problem]").click()
    team.wait_for_url("**/reports?status=open*")
    page.goto(f"/children/{pid}")
    rep = page.locator("[data-testid=family-report]").first
    assert rep.locator("[data-testid=report-outcome]").inner_text() == "checked: the question is right"
    assert "8 × 7 = 56" in rep.inner_text()
    m = last_mail(owner, "We checked the question Rohan reported")
    assert "the question and its answer are right" in m["body"] and "8 × 7 = 56" in m["body"]
    DB.team_members.delete_one({"_id": slug})
    team.context.close()


def test_change_todays_plan_too_reopens_the_day_and_rest_days_agree(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "Minecraft")
    page.click("form[action='/settings'] button[type=submit]")
    pid = add_child(page, "Leo", 5, targets={"tables": 1}, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    for k in ("maths", "spelling"):
        page.uncheck(f"[data-testid=on-{k}]")
    _save(page, pid)
    enter_child(page, "Leo")
    _right(_session(page), "tables")
    page.goto("/me")
    assert page.locator("[data-testid=all-done]").count() == 1
    # the parent adds science for today too: the day opens again, the reward stays earned
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.check("[data-testid=on-science]")
    page.check("[data-testid=plan-today]")
    _save(page, pid)
    enter_child(page, "Leo")
    assert page.locator("[data-testid=all-done]").count() == 0
    assert "Here is your plan for today" in page.inner_text("[data-testid=day-line]")
    assert "0 of 5" in page.inner_text("[data-testid=tile-science]")
    assert "You earned: Minecraft" in page.inner_text("[data-testid=reward]")
    unlock_parent(page)
    page.goto("/home")
    assert page.inner_text("[data-testid='kid-Leo'] [data-testid=pct]") == "16%"     # 1 of 6 planned answers
    # tomorrow is a day off: Home, the Board, the child page and My day all say so
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=off-from]", (TODAY + datetime.timedelta(days=1)).isoformat())
    _save(page, pid)
    page.goto("/home")
    assert "Tomorrow is a day off" in page.inner_text("[data-testid='kid-Leo'] [data-testid=tomorrow-off]")
    page.goto("/board")
    assert "Tomorrow is a day off" in page.inner_text("[data-testid='board-Leo'] [data-testid=tomorrow-off]")
    page.goto(f"/children/{pid}")
    assert "Tomorrow is a day off" in page.inner_text("[data-testid=tomorrow-off]")
    enter_child(page, "Leo")
    assert "Tomorrow is a day off." in page.inner_text("[data-testid=day-line]")
    # and today a day off as well: the same word everywhere, never "All done ... come back tomorrow"
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=off-from]", TODAY.isoformat())
    _save(page, pid)
    page.goto("/home")
    assert page.inner_text("[data-testid='kid-Leo'] [data-testid=rest-day]") == "Day off"
    page.goto("/board")
    assert page.inner_text("[data-testid='board-Leo'] [data-testid=rest-day]") == "Day off"
    assert page.locator("[data-testid=all-done]").count() == 0
    enter_child(page, "Leo")
    assert "Today is a day off" in page.inner_text("[data-testid=rest-day]")
    assert page.locator("[data-testid=all-done]").count() == 0
    # the printed report lists the days off
    unlock_parent(page)
    page.goto(f"/children/{pid}/report?range=7")
    assert f"Days off: {TODAY.day} {TODAY:%b}" in page.inner_text("[data-testid=report-days-off]")


def test_up_to_three_topics_of_any_subjects_each_with_its_own_weeks(page):
    signup(page)
    pid = add_child(page, "Adam", 8, targets={"science": 5, "grammar": 5}, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    groups = page.locator("[data-testid=focus-0] optgroup").evaluate_all("gs => gs.map(g => g.label)")
    assert {"Science: Biology", "Science: Chemistry", "Science: Physics"} <= set(groups)
    chem = page.locator("[data-testid=focus-0] optgroup[label='Science: Chemistry'] option").all_inner_texts()
    assert "Chemical reactions" in chem and "Energy" not in chem
    page.select_option("[data-testid=focus-0]", label="Algebra: expressions, brackets & sequences")
    page.select_option("[data-testid=focus-1]", label="Equations, inequalities & linear graphs")
    page.select_option("[data-testid=focus-weeks-1]", "2")
    page.select_option("[data-testid=focus-2]", "science:Chemical reactions")
    _save(page, pid)
    f = DB.pupils.find_one({"_id": pid})["focus"]
    assert [i["subject"] for i in f] == ["maths", "maths", "science"]
    assert [i["until"] for i in f] == [(TODAY + datetime.timedelta(days=d)).isoformat() for d in (7, 14, 7)]
    page.goto(f"/children/{pid}")
    txt = page.inner_text("[data-testid=focus]")
    assert "Maths: Algebra: expressions" in txt and "Science (Chemistry): Chemical reactions" in txt
    # both maths topics get the maths focus share
    enter_child(page, "Adam")
    s = _session(page)
    strands = []
    for _ in range(30):
        q = s.post(BASE + "/api/maths/next", json={}).json()
        strands.append(q["strand"])
        s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": "-98765"})
    assert sum(st in (f[0]["strand"], f[1]["strand"]) for st in strands) >= 13, strands
    # saving again keeps each topic's own dates; a changed number of weeks counts from its first day
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=focus-weeks-0]", "2")
    page.select_option("[data-testid=focus-2]", "")
    _save(page, pid)
    f2 = DB.pupils.find_one({"_id": pid})["focus"]
    assert [(i["strand"], i["until"]) for i in f2] == [(f[0]["strand"], (TODAY + datetime.timedelta(days=14)).isoformat()),
                                                       (f[1]["strand"], f[1]["until"])]
