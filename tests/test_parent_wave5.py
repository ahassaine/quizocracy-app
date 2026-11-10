"""The parent pages after wave 5: "rushed" that says which answers and never counts a Year 4 check time-out; an
answer of 0 kept as 0; "needs help" that extra practice, the optional check and a thin first day can't bring on;
the SATs card (weak only when low) and "Revise for SATs" that fills free slots from its gaps and asks before
replacing the parent's topics; a new school year that carries the topics across or says why not; "working at" a
year ahead; every plan change in Family activity, on Home ("From tomorrow") and on the child's My day; only the
owner deletes the account; a bounced save keeps every field; the Year 4 check on Home; the report email on by
default; the school list on Add a child; easy PINs; the "Hand over" menu item."""
import asyncio
import datetime
import re
import threading
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import requests

from app import progress
from app.routes.parent import easy_pin
from conftest import BASE, DB, PASSWORD, add_child, enter_child, last_mail, new_email, signup, unlock_parent

TZ = ZoneInfo("Europe/London")
TODAY = datetime.datetime.now(TZ).date().isoformat()


def _rows(pid, fid, rows):
    """Answers written straight into the record, a second apart, oldest first: (activity, correct, ms, extra)."""
    t0 = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    DB.attempts.insert_many([{"pupil_id": pid, "family_id": fid, "activity": a, "correct": c, "ms": ms,
                              "detail": x.pop("detail", f"{a}{i}"), "day": TODAY, "ts": t0 + datetime.timedelta(seconds=i), **x}
                             for i, (a, c, ms, x) in enumerate(rows)])


def _fid(pid):
    return DB.pupils.find_one({"_id": pid})["family_id"]


# ---- the rules, without a server ----

def test_easy_pins():
    for p in ("1111", "1234", "0000", "9876", "1212", "1122", "2580", "7890"):
        assert easy_pin(p), p
    for p in ("4739", "3851", "2741", "8305", "1739", "5274"):
        assert not easy_pin(p), p


def test_an_answer_of_zero_is_kept_as_zero(monkeypatch):
    rows = []

    class Attempts:
        async def insert_one(self, r):
            rows.append(r)
    monkeypatch.setattr(progress, "db", SimpleNamespace(attempts=Attempts()))
    async def both():
        await progress.record({"_id": "p_x", "family_id": "f_x"}, "maths", False, 900, "Y2.3.a",
                              "Mark 1 × 2 on the number line", "2", 0)
        await progress.record({"_id": "p_x", "family_id": "f_x"}, "maths", False, 900, "Y2.3.a", "Mark it", "2", None)
    t = threading.Thread(target=lambda: asyncio.run(both()))      # Playwright's loop may be running in this thread
    t.start()
    t.join()
    assert rows[0]["got"] == "0" and rows[1]["got"] == ""


# ---- Home and Progress ----

def test_rushed_says_which_and_never_counts_a_check_time_out(page):
    signup(page)
    pid = add_child(page, "Jay", 3, targets={"maths": 5, "tables": 5})
    fid = _fid(pid)
    _rows(pid, fid, [
        ("maths", False, 700, {"q": "What is 6 + 7?", "exp": "13", "got": "1"}),                     # quick: rushed
        ("tables", False, 6000, {"q": "12 × 7 =", "exp": "84", "got": "(time ran out)", "src": "mtc", "detail": "12x7"}),
        ("tables", False, 900, {"q": "11 × 9 =", "exp": "99", "got": "9", "src": "mtc", "detail": "11x9"}),
    ])
    page.goto("/home")
    flag = page.get_by_test_id("flag-rushed")
    assert "1 wrong answer looks rushed" in flag.inner_text()
    flag.locator("summary").click()
    items = page.get_by_test_id("rushed-list").inner_text()
    assert "What is 6 + 7?" in items and "12 × 7" not in items and "11 × 9" not in items


def test_needs_help_not_from_extras_the_check_or_a_thin_first_day(page):
    signup(page)
    pid = add_child(page, "Kim", 3, targets={"maths": 4, "tables": 5})
    fid = _fid(pid)
    # maths: 4 right (the target), then 12 extra, mostly wrong; tables: 12 wrong, all from the optional check and
    # beyond Year 3 (the 12x, 11x, 9x and 7x tables); spelling: 3 wrong first tries only (too few to say anything)
    _rows(pid, fid, [("maths", True, 5000, {"detail": "Y3.1.a"})] * 4
          + [("maths", i % 4 == 0, 5000, {"q": f"q{i}", "exp": "1", "got": "2"}) for i in range(12)]
          + [("tables", False, 3000, {"q": "12 × 7 =", "exp": "84", "got": "80", "src": "mtc", "detail": f"{a}x{b}"})
             for a, b in [(12, 7), (11, 9), (9, 7), (7, 11), (12, 9), (11, 7), (12, 11), (9, 9), (7, 7), (11, 11), (12, 12), (9, 11)]]
          + [("spelling", False, 4000, {"q": "Spell the word you heard", "exp": "w", "got": "x"})] * 3)
    page.goto("/home")
    acc = page.get_by_test_id("home-accuracy").inner_text()
    assert "needs help" not in acc
    assert "Maths 100%" in acc                               # the extras are left out of it
    page.goto(f"/children/{pid}")
    assert page.get_by_test_id("needs-help").count() == 0
    # ten first tries under 70% (in the day's own answers) does say it
    _rows(pid, fid, [("tables", i < 3, 4000, {"q": "3 × 4 =", "exp": "12", "got": "11", "detail": f"3x{i + 1}"}) for i in range(10)])
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities.tables.target": 20}})
    page.goto("/home")
    assert "Times tables 30% needs help" in page.get_by_test_id("home-accuracy").inner_text()


def test_extras_show_their_time_and_the_check_on_home(page):
    signup(page)
    pid = add_child(page, "Ari", 4, targets={"maths": 2})
    fid = _fid(pid)
    off = {k: {"on": False, "target": 5} for k in ("tables", "spelling", "grammar", "science", "numbers", "verbs")}
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {**off, "maths": {"on": True, "target": 2}}, "mtc": [
        {"day": "2026-01-05", "score": 23, "of": 25}, {"day": TODAY, "score": 20, "of": 25}]}})
    _rows(pid, fid, [("maths", True, 3000, {})] * 4)
    page.goto("/home")
    assert re.search(r"\d\d:\d\d.*after the day was done", page.get_by_test_id("extra-at").inner_text())
    assert page.get_by_test_id("home-check").inner_text().strip() == "Check: 20/25 (best 23)"


# ---- SATs ----

def _sats_child(page):
    signup(page)
    pid = add_child(page, "Aanya", 6, targets={"maths": 10, "grammar": 5})
    # a grammar skill 8 of 9 right (score 90) is "started, not secure yet"; an arithmetic skill 1 of 5 is weak
    DB.bank_mastery.insert_one({"_id": f"{pid}:GP6.02", "pupil_id": pid, "subject": "grammar", "key": "GP6.02",
                                "score": 90, "attempts": 9, "correct": 8})
    DB.maths_mastery.insert_one({"pupil": pid.lower(), "skill": "Y6.1.a", "score": 10, "attempts": 5, "correct_count": 1})
    for k in ("Y6.7.a", "Y6.7.b", "Y6.8.a", "Y6.8.b", "Y6.0.a"):          # reasoning well under way
        DB.maths_mastery.insert_one({"pupil": pid.lower(), "skill": k, "score": 100, "attempts": 6, "correct_count": 6})
    return pid


def test_sats_weak_only_when_low_and_revise_keeps_the_parents_topics(page):
    pid = _sats_child(page)
    page.goto(f"/children/{pid}#sats")
    gps = page.get_by_test_id("sats-gps")
    assert "Main and subordinate clauses" in gps.get_by_test_id("sats-started").inner_text()
    assert gps.get_by_test_id("sats-weak").count() == 0
    assert "Column addition" in page.get_by_test_id("sats-arithmetic").get_by_test_id("sats-weak").inner_text()
    assert "off" in page.get_by_test_id("sats-off").inner_text()
    # the parent's own topic first, then "Revise for SATs": it takes the free slots, arithmetic first
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=focus-0]", "grammar:Punctuation")
    page.click("form#childForm button[type=submit]")
    page.goto(f"/children/{pid}#sats")
    page.click("[data-testid=sats-toggle]")
    page.wait_for_url("**sats=on*")
    focus = [(i["subject"], i["strand"]) for i in DB.pupils.find_one({"_id": pid})["focus"]]
    assert focus[0] == ("grammar", "Punctuation") and len(focus) == 3
    # the papers least covered: arithmetic (one topic, weak) first, then grammar (1 of 20), not geometry or ratio
    assert focus[1:] == [("maths", "6.1 The four operations"), ("grammar", "Test review")]
    assert "on until" in page.get_by_test_id("sats-on").inner_text()
    assert "Grammar: Punctuation" in page.get_by_test_id("sats-topics").inner_text()
    page.click("[data-testid=sats-toggle]")                  # Turn off: only its own topics go
    page.wait_for_url("**sats=off*")
    assert [(i["subject"], i["strand"]) for i in DB.pupils.find_one({"_id": pid})["focus"]] == [("grammar", "Punctuation")]
    # three topics of the parent's own: it asks before replacing them
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=focus-1]", "grammar:Test review")
    page.select_option("[data-testid=focus-2]", "maths:6.3 Fractions: equivalence, comparing, + and -")
    page.click("form#childForm button[type=submit]")
    page.goto(f"/children/{pid}#sats")
    page.click("[data-testid=sats-toggle]")
    page.wait_for_url("**sats=full*")
    assert len(DB.pupils.find_one({"_id": pid})["focus"]) == 3 and not DB.pupils.find_one({"_id": pid}).get("sats")
    page.click("[data-testid=sats-replace]")
    page.wait_for_url("**sats=on*")
    assert DB.pupils.find_one({"_id": pid})["sats"]["strands"]


def test_focus_menu_says_the_subject_and_what_test_review_is(page):
    signup(page)
    page.goto("/children/new")
    page.select_option("#year", "6")
    page.click("[data-testid=new-focus] summary")
    page.select_option("[data-testid=new-focus-0]", "grammar:Test review")
    hint = page.get_by_test_id("focus-hint-0").inner_text()
    assert hint.startswith("Grammar and punctuation · Test review") and "apostrophes" in hint


# ---- school year, working at, and the focus ----

def test_new_year_carries_the_topic_across_or_says_why_not_and_working_at(page):
    signup(page)
    pid = add_child(page, "Chloe", 8, targets={"maths": 10, "science": 5})
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=focus-0]", "science:Energy")             # Year 9 has Energy too
    page.select_option("[data-testid=focus-1]", "maths:8.7 Equations, inequalities & linear graphs")      # not in Year 9
    page.click("form#childForm button[type=submit]")
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=level]", "9")                            # working at Year 9, school year 8
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    p = DB.pupils.find_one({"_id": pid})
    assert p["year"] == 9 and p["school_year"] == 8
    assert [i["strand"] for i in p["focus"]] == ["Energy"]
    assert "was for Year 8" in page.get_by_test_id("focus-lost").inner_text()
    page.goto("/home")
    assert page.get_by_test_id("home-year").inner_text() == "Year 8, working at Year 9 level"
    page.goto(f"/children/{pid}/report")
    assert "Year 8, working at Year 9 level" in page.get_by_test_id("report-year").inner_text()
    page.goto("/home")
    assert "moved Chloe to Year 8, working at Year 9 level" in page.get_by_test_id("family-log").text_content()


def test_a_bounced_save_keeps_every_field(page):
    signup(page)
    pid = add_child(page, "Jay", 3, targets={"tables": 10, "spelling": 5})
    page.goto(f"/children/{pid}/edit")
    page.check("[data-testid=check-tables]")
    page.fill("[data-testid=target-maths]", "12")
    page.fill("[data-testid=school-words]", "because, freind, heart")
    page.click("form#childForm button[type=submit]")
    assert page.get_by_test_id("school-unknown").is_visible()
    assert page.is_checked("[data-testid=check-tables]")
    assert page.input_value("[data-testid=target-maths]") == "12"
    page.check("[data-testid=fix-freind-0]")
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    acts = DB.pupils.find_one({"_id": pid})["activities"]
    assert acts["tables"].get("check") and acts["maths"]["target"] == 12


def test_add_a_child_with_the_school_list_and_an_easy_pin(page):
    signup(page)
    page.goto("/children/new")
    page.fill("#name", "Poppy")
    page.select_option("#year", "2")
    page.fill("#pin", "1111")
    assert page.get_by_test_id("pin-easy").is_visible()
    page.click("[data-testid=new-school] summary")
    page.fill("[data-testid=school-words]", "frend, water, money")
    page.click("form.card button[type=submit]")
    assert page.get_by_test_id("school-unknown").is_visible()
    assert page.input_value("#name") == "Poppy"
    page.fill("#pin", "1111")
    page.check("[data-testid=fix-frend-0]")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(r".*/children/p_[0-9a-f]+\?added=1.*"))
    assert "3 words" in page.get_by_test_id("added-school").inner_text()
    assert page.get_by_test_id("pin-easy-saved").is_visible()
    pid = page.url.split("/children/")[1].split("?")[0]
    assert [w["w"] for w in DB.pupils.find_one({"_id": pid})["school_words"]["words"]] == ["friend", "water", "money"]


# ---- two homes ----

def _join(browser, page, role="parent", name="Steve (Dad)"):
    email = new_email("dad")
    page.goto("/settings")
    page.fill("#invite_email", email)
    page.check(f"input[name=role][value={role}]")
    page.click("[data-testid=send-invite]")
    tok = re.search(r"/invite\?token=(\S+)", last_mail(email, "invited you")["body"]).group(1)
    other = browser.new_context(base_url=BASE).new_page()
    other.goto(f"/invite?token={tok}")
    other.fill("#password", PASSWORD)
    other.check("#consent")
    other.click("form[action='/invite'] button")
    other.wait_for_url("**/home*")
    other.goto("/settings")
    other.fill("[data-testid=my-name]", name)
    other.click("form[action='/settings/name'] button")
    return other, email


def test_changes_are_seen_by_the_other_parent_and_the_child(page, browser):
    owner = signup(page)
    pid = add_child(page, "Ruby", 5, targets={"maths": 10}, year_defaults=True)
    dad, dad_email = _join(browser, page)
    page.goto("/settings")
    page.check("[data-testid=plan-emails]")                   # Mum asks for an email when Dad changes a plan
    page.wait_for_selector("[data-testid=autosaved]:has-text('Saved')")
    # Ruby starts her day, then Dad adds Science and changes today's plan too
    enter_child(dad, "Ruby")
    unlock_parent(dad)
    DB.attempts.insert_one({"pupil_id": pid, "family_id": _fid(pid), "activity": "maths", "correct": True, "ms": 3000,
                            "detail": "x", "day": TODAY, "ts": datetime.datetime.utcnow()})
    dad.goto(f"/children/{pid}/edit")
    dad.check("[data-testid=on-science]")
    dad.check("[data-testid=plan-today]")
    dad.fill("[data-testid=target-maths]", "15")
    dad.click("form#childForm button[type=submit]")
    dad.wait_for_url("**saved=1*")
    page.goto("/home")
    log = page.get_by_test_id("family-log").text_content()
    assert "Steve (Dad) changed Ruby's plan: Maths 10 → 15 a day, added Science, 5 a day, from today" in log
    assert "changed Ruby's plan" in last_mail(owner, "Ruby's plan")["body"]
    enter_child(page, "Ruby")
    assert "Steve (Dad) changed today's plan" in page.get_by_test_id("plan-note").inner_text()
    unlock_parent(page)
    # a change from tomorrow shows on Home
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=target-maths]", "20")
    page.click("form#childForm button[type=submit]")
    page.goto("/home")
    assert "Maths 20" in page.get_by_test_id("home-pending").inner_text()
    # the invited parent cannot delete the family; they may leave
    dad.goto("/settings")
    assert dad.locator("form[action='/account/delete']").count() == 0
    assert "Ask" in dad.get_by_test_id("ask-owner").inner_text()
    s = requests.Session()
    for c in dad.context.cookies():
        s.cookies.set(c["name"], c["value"])
    r = s.post(BASE + "/account/delete", data={"password": PASSWORD, "confirm": "DELETE"}, allow_redirects=False)
    assert r.status_code == 303 and DB.families.count_documents({"_id": _fid(pid)}) == 1
    # the owner deletes it: every grown-up is told
    page.goto("/settings")
    page.fill("#confirm", "DELETE")
    page.fill("#delpw", PASSWORD)
    page.click("form[action='/account/delete'] button")
    page.wait_for_url("**/?deleted=1")
    assert "Ruby" in last_mail(dad_email, "was deleted")["body"]
    assert last_mail(owner, "was deleted")


def test_report_email_on_by_default_and_ticked_on_the_progress_page(page):
    email = signup(page)
    pid = add_child(page, "Ethan", 9)
    assert DB.accounts.find_one({"email": email})["report_emails"] is True
    DB.reports.insert_one({"family_id": _fid(pid), "pupil_id": pid, "activity": "science", "reason": "other",
                           "note": "", "served": {"prompt": "Unit of power?"}, "expected": "watt", "answer": "watt (W)",
                           "day": TODAY, "ts": datetime.datetime.utcnow(), "status": "open"})
    page.goto(f"/children/{pid}")
    tick = page.get_by_test_id("report-emails-tick")
    assert tick.is_checked()
    tick.uncheck()
    page.wait_for_url("**report_emails=off*")
    assert DB.accounts.find_one({"email": email})["report_emails"] is False


def test_hand_over_in_the_menu(page):
    signup(page)
    add_child(page, "Sam", 4)
    page.goto("/home")
    page.click("[data-testid=nav-handover]")
    page.wait_for_url("**/learn")
