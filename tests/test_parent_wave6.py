"""The parent pages after wave 6: "working at" per subject (maths, grammar, science), old records moved across, the
level shown only where it differs and optional on the printed report, and the suggestions both ways; one rule for
"right first time" on Home, Progress and the report, with good extra practice shown; the "quick day" line only
with rushed answers, in grey; quick wrong taps counted as rushed; adding to today's plan after the reward is
earned; saves that say what was saved; "Add it" landing on the spelling box; a nudge when only one child has a
reward; lock-outs in minutes, not a clock time; PINs in Settings for every grown-up and shown after an unlock;
joining with every error at once and a name; the PIN kept through a bounced Add a child; the child's 11th report."""
import datetime
import re
from zoneinfo import ZoneInfo

import requests

from app.bank import engine
from conftest import BASE, DB, PASSWORD, add_child, enter_child, last_mail, new_email, pin_for, signup, unlock_parent

TZ = ZoneInfo("Europe/London")
TODAY = datetime.datetime.now(TZ).date().isoformat()


def _rows(pid, rows, minutes_ago=30):
    """Answers written straight into the record, a second apart, oldest first: (activity, correct, ms, extra)."""
    fid = DB.pupils.find_one({"_id": pid})["family_id"]
    t0 = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_ago)
    DB.attempts.insert_many([{"pupil_id": pid, "family_id": fid, "activity": a, "correct": c, "ms": ms,
                              "detail": x.pop("detail", f"{a}{i}"), "day": TODAY, "ts": t0 + datetime.timedelta(seconds=i), **x}
                             for i, (a, c, ms, x) in enumerate(rows)])


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _only(pid, **targets):
    """The plan: only these activities, at these targets."""
    acts = {k: {"on": k in targets, "target": targets.get(k, 5)}
            for k in ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")}
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": acts}})


# ---- working at, subject by subject ----

def test_an_old_record_moves_across_to_levels_per_subject(page):
    signup(page)
    pid = add_child(page, "Chloe", 9, targets={"maths": 10})
    other = add_child(page, "Olly", 5, targets={"maths": 10})
    # wave 5's shapes: one level for everything (year 9) with the real school year 8; and school_year left as None
    DB.pupils.update_one({"_id": pid}, {"$set": {"year": 9, "school_year": 8}})
    DB.pupils.update_one({"_id": other}, {"$set": {"school_year": None}})
    page.goto("/home")
    assert page.get_by_test_id("kid-Chloe").get_by_test_id("home-year").inner_text() == "Year 8, working at Year 9 level"
    p = DB.pupils.find_one({"_id": pid})
    assert p["year"] == 8 and p["levels"] == {"maths": 9, "grammar": 9, "science": 9} and "school_year" not in p
    o = DB.pupils.find_one({"_id": other})
    assert o["year"] == 5 and not o.get("levels") and "school_year" not in o
    # the form shows it the new way: Year 8, each subject at Year 9
    page.goto(f"/children/{pid}/edit")
    assert page.input_value("#year") == "8" and page.input_value("[data-testid=level-maths]") == "9"


def test_maths_lower_alone_and_the_report_can_leave_it_out(page, browser):
    owner = signup(page)
    pid = add_child(page, "Noor", 8, targets={"maths": 10, "grammar": 5, "science": 5})
    page.goto(f"/children/{pid}/edit")
    page.select_option("[data-testid=level-maths]", "6")
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    p = DB.pupils.find_one({"_id": pid})
    assert p["year"] == 8 and p["levels"] == {"maths": 6}
    page.goto("/home")
    assert page.get_by_test_id("home-year").inner_text() == "Year 8 · Maths: Year 6 level"
    assert "set Noor's maths at Year 6 level (school year: Year 8)" in page.get_by_test_id("family-log").text_content()
    page.goto(f"/children/{pid}")
    assert "of 1" in page.get_by_test_id("card-maths").inner_text() or "Year 6 skills" in page.get_by_test_id("card-maths").inner_text()
    page.goto(f"/children/{pid}/report")
    assert page.get_by_test_id("report-year").inner_text() == "Year 8 · Maths: Year 6 level"
    # the parent leaves the levels off the printed report
    page.goto(f"/children/{pid}/edit")
    page.uncheck("[data-testid=level-report]")
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    page.goto(f"/children/{pid}/report")
    assert page.get_by_test_id("report-year").inner_text() == "Year 8"
    assert "left out of this report" in page.get_by_test_id("report-levels-note").inner_text()
    # the questions: maths from Year 6, grammar and science from Year 8
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login")
    kid.fill("#email", owner)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Noor")
    s = _session(kid)
    q = s.post(BASE + "/api/maths/next", json={}).json()
    assert DB.maths_lab_q.find_one({"_id": q["token"]})["skill"].startswith("Y6.")
    for sub in ("grammar", "science"):
        q = s.post(BASE + f"/api/{sub}/next", json={}).json()
        key = DB.items.find_one({"_id": q["token"]})["meta"]["skill"]
        assert int(engine.skill(key)["year"]) == engine.bank_year(sub, 8), (sub, key)
    kid.context.close()


def test_suggestions_both_ways_per_subject(page):
    signup(page)
    pid = add_child(page, "Hana", 8, targets={"maths": 20, "grammar": 40})
    _only(pid, maths=20, grammar=40)
    # maths: 12 of 42 right first time over 3 days (needs help, under 60%); grammar: 30 of 32 (85% and more over 30);
    # a week after the first day, so a lower level may be suggested (wave 8)
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime.utcnow() - datetime.timedelta(days=8)}})
    for back in (2, 1):
        _rows(pid, [("maths", i < 4, 6000, {"q": f"q{i}", "exp": "1", "got": "2", "day": (datetime.datetime.now(TZ).date()
                     - datetime.timedelta(days=back)).isoformat()}) for i in range(14)], minutes_ago=60 * 24 * back)
    _rows(pid, [("maths", i < 4, 6000, {"q": f"q{i}", "exp": "1", "got": "2"}) for i in range(14)]
          + [("grammar", i >= 2, 6000, {"q": f"g{i}", "exp": "a", "got": "b"}) for i in range(32)])
    page.goto(f"/children/{pid}")
    low = page.get_by_test_id("try-lower")
    assert "Maths is hard at the moment" in low.inner_text() and "maths at Year 7 level" in low.inner_text()
    up = page.get_by_test_id("try-ahead")
    assert "Grammar" in up.inner_text() and "Year 9" in up.inner_text()
    page.goto("/help#hard")
    assert page.locator("#hard .help-short").is_visible()


# ---- one rule for right first time, with the extra practice shown ----

def test_one_rule_for_right_first_time_and_extra_practice(page):
    signup(page)
    pid = add_child(page, "Noor", 6, targets={"maths": 5})
    _only(pid, maths=5)
    # up to the target: 7 wrong then 5 right (41%); then 30 extra answers, all right
    _rows(pid, [("maths", False, 6000, {"q": f"w{i}", "exp": "1", "got": "2"}) for i in range(7)]
          + [("maths", True, 6000, {}) for _ in range(5)] + [("maths", True, 6000, {}) for _ in range(30)])
    page.goto("/home")
    acc = page.get_by_test_id("home-accuracy").inner_text()
    assert "Maths 42%" in acc and "needs help" not in acc            # 5 of 12, rounded; good extra practice lifts it out
    assert "+ 30 extra questions after the targets, 100% right first time" in page.get_by_test_id("day-extra").inner_text()
    page.goto(f"/children/{pid}")
    assert "42%" in page.get_by_test_id("glance-acts").inner_text()
    assert "plus 30 extra questions, 100% right first time" in page.get_by_test_id("glance-extra-maths").inner_text()
    page.goto(f"/children/{pid}/report?range=7")
    row = page.get_by_test_id("report-act-maths").inner_text()
    assert "42% (5 of 12)" in row and "30 questions, 100% right first time" in row
    # bad extra practice never makes it "needs help" by itself
    other = add_child(page, "Sam", 6, targets={"maths": 5})
    _only(other, maths=5)
    _rows(other, [("maths", True, 6000, {}) for _ in range(12)]
          + [("maths", False, 6000, {"q": f"x{i}", "exp": "1", "got": "2"}) for i in range(20)])
    page.goto("/home")
    assert "needs help" not in page.get_by_test_id("kid-Sam").get_by_test_id("home-accuracy").inner_text()


def test_quick_day_line_only_with_rushed_answers_and_in_grey(page):
    signup(page)
    pid = add_child(page, "Theo", 2, targets={"maths": 6})
    _only(pid, maths=6)
    _rows(pid, [("maths", True, 4000, {}) for _ in range(6)], minutes_ago=3)          # careful, and quicker than planned
    page.goto("/home")
    assert page.get_by_test_id("flag-quick").count() == 0
    other = add_child(page, "Ben", 2, targets={"maths": 6})
    _only(other, maths=6)
    _rows(other, [("maths", False, 600, {"q": "2 + 2", "exp": "4", "got": "1"})]
          + [("maths", True, 4000, {}) for _ in range(6)], minutes_ago=3)
    page.goto("/home")
    flag = page.get_by_test_id("kid-Ben").get_by_test_id("flag-quick")
    assert "worth a look together" in flag.inner_text() and "mut" in flag.get_attribute("class")


def test_quick_wrong_taps_count_as_rushed(page, browser):
    owner = signup(page)
    pid = add_child(page, "Kai", 5, targets={"grammar": 5})
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login")
    kid.fill("#email", owner)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Kai")
    s = _session(kid)
    for _ in range(40):                                          # a multiple-choice question, tapped wrong in 1.8 s
        q = s.post(BASE + "/api/grammar/next", json={}).json()
        key = DB.items.find_one({"_id": q["token"]})["answer"]
        if key["t"] == "mcq":
            wrong = next(i for i in range(len(q["opts"])) if i != key["right"])
            assert s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": wrong, "ms": 1800}).json()["correct"] is False
            break
        s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": "zzqx", "ms": 9000})
    else:
        raise AssertionError("no multiple-choice question")
    kid.context.close()
    page.goto("/home")
    flag = page.get_by_test_id("flag-rushed")
    flag.locator("summary").click()
    assert "(tapped very quickly)" in page.get_by_test_id("rushed-list").inner_text()


# ---- saving ----

def test_adding_to_today_after_the_reward_is_earned(page):
    signup(page)
    pid = add_child(page, "Kai", 5, targets={"maths": 2})
    _only(pid, maths=2)
    DB.pupils.update_one({"_id": pid}, {"$set": {"reward": {"text": "30 min Roblox", "threshold": 100}}})
    _rows(pid, [("maths", True, 5000, {}) for _ in range(2)])
    page.goto(f"/children/{pid}/edit")
    assert "already earned today's reward" in page.get_by_test_id("plan-earned").inner_text()
    assert page.is_checked("[data-testid=plan-start-tomorrow]")
    page.check("[data-testid=on-grammar]")
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    assert "won't be needed for it today" in page.get_by_test_id("saved-earned").inner_text()
    log = DB.pupils.find_one({"_id": pid})["plan_log"]
    assert log[-1]["from"] > TODAY                               # from tomorrow, as preselected


def test_instant_saves_say_what_was_saved(page):
    signup(page)
    page.goto("/settings")
    on = page.is_checked("[data-testid=weekly]")
    page.click("[data-testid=weekly]")
    page.wait_for_selector(f"[data-testid=autosaved]:has-text('Weekly summary: {'off' if on else 'on'}')")


def test_add_it_lands_on_the_spelling_box(browser, devices):
    ctx = browser.new_context(base_url=BASE, viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.set_default_timeout(15000)
    signup(page)
    add_child(page, "Kai", 5, year_defaults=True)
    page.goto("/home")
    page.click("[data-testid=discover-list]")
    page.wait_for_load_state("load")
    page.wait_for_timeout(500)
    box = page.get_by_test_id("school-words").bounding_box()
    head = page.evaluate("document.querySelector('header.top').getBoundingClientRect().bottom")
    assert head <= box["y"] and box["y"] + box["height"] <= 844
    ctx.close()


def test_one_child_with_a_reward_nudges_for_the_others(page):
    signup(page)
    ben = add_child(page, "Ben", 4, targets={"maths": 5})
    add_child(page, "Ava", 3, targets={"maths": 5})
    add_child(page, "Max", 2, targets={"maths": 5})
    page.goto(f"/children/{ben}/edit")
    page.fill("#reward_text", "Sticker on the chart")
    page.click("form#childForm button[type=submit]")
    page.wait_for_url("**saved=1*")
    assert "Ava and Max have no reward" in page.get_by_test_id("reward-gap").inner_text()
    page.goto("/home")
    page.click("[data-testid=reward-gap-use]")
    page.wait_for_url("**/home?family_reward=1")
    fam = DB.families.find_one({"_id": DB.pupils.find_one({"_id": ben})["family_id"]})
    assert fam["reward"]["text"] == "Sticker on the chart"
    assert page.get_by_test_id("reward-gap").count() == 0


# ---- PINs, lock-outs and carers ----

def test_lock_in_minutes_and_the_pin_after_an_unlock(page, browser):
    owner = signup(page)
    add_child(page, "Isaac", 4)
    page.goto("/settings")                                     # a parent finds the PINs in Settings too
    page.get_by_test_id("pins").locator("summary").first.click()
    assert page.get_by_test_id("pin-Isaac").inner_text() == pin_for("Isaac")
    page.click("text=Hand over")
    page.goto("/learn")
    for _ in range(6):
        form = page.get_by_test_id("pin-Isaac")
        form.locator("input[name=pin]").fill("0000" if pin_for("Isaac") != "0000" else "1111")
        form.locator("button").click()
    locked = page.get_by_test_id("locked-Isaac").inner_text()
    assert "locked for 5 more minutes" in locked and not re.search(r"\d\d:\d\d", locked)
    tile = page.get_by_test_id("tile-Isaac")
    tile.locator("summary").click()
    tile.locator("input[name=password]").fill(PASSWORD)
    tile.locator("button").first.click()
    page.wait_for_url("**/learn?unlocked=*")
    page.get_by_test_id("show-pin-Isaac").locator("summary").click()
    assert page.get_by_test_id("shown-pin-Isaac").inner_text() == pin_for("Isaac")
    enter_child(page, "Isaac")                                 # once the child is in, it is hidden again
    page.goto("/learn")
    assert page.get_by_test_id("show-pin-Isaac").count() == 0


def test_joining_shows_every_error_at_once_and_asks_a_name(page, browser):
    signup(page)
    add_child(page, "Isaac", 4)
    email = new_email("gran")
    page.goto("/settings")
    page.fill("#invite_email", email)
    page.check("input[name=role][value=carer]")
    page.click("[data-testid=send-invite]")
    tok = re.search(r"/invite\?token=(\S+)", last_mail(email, "invited you")["body"]).group(1)
    gran = browser.new_context(base_url=BASE).new_page()
    gran.goto(f"/invite?token={tok}")
    gran.fill("[data-testid=join-name]", "Gran")
    gran.fill("#password", "short")
    gran.click("form[action='/invite'] button")
    err = gran.get_by_test_id("invite-error").inner_text()
    assert "8 characters" in err and "18 or over" in err
    assert gran.input_value("#password") == "short" and gran.input_value("[data-testid=join-name]") == "Gran"
    gran.fill("#password", PASSWORD)
    gran.check("#consent")
    gran.click("form[action='/invite'] button")
    gran.wait_for_url("**/home*")
    assert DB.accounts.find_one({"email": email})["name"] == "Gran"
    assert "Gran (" in gran.get_by_test_id("family-log").text_content()
    gran.goto("/settings")                                     # the carer's PINs, in the same place as a parent's
    assert gran.get_by_test_id("pins").is_visible()
    gran.context.close()


def test_add_a_child_keeps_the_pin_after_the_spelling_check(page):
    signup(page)
    page.goto("/children/new")
    page.fill("#name", "Olivia")
    page.select_option("#year", "3")
    page.fill("#pin", "4739")
    page.click("[data-testid=new-school] summary")
    page.fill("[data-testid=school-words]", "thogh, laugh")
    page.click("form.card button[type=submit]")
    assert page.get_by_test_id("school-unknown").is_visible()
    assert page.input_value("#pin") == "4739"
    page.locator("[data-testid=school-unknown-word] input[type=radio]").first.check()
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(r".*/children/p_[0-9a-f]+\?added=1.*"))


# ---- reports ----

def test_the_childs_eleventh_report_is_not_sent_and_says_so(page, browser):
    owner = signup(page)
    pid = add_child(page, "Zara", 9, targets={"maths": 10})
    fid = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.reports.insert_many([{"family_id": fid, "pupil_id": pid, "activity": "maths", "reason": "wrong", "day": TODAY,
                             "ts": datetime.datetime.utcnow(), "status": "open"} for _ in range(10)])
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login")
    kid.fill("#email", owner)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Zara")
    kid.goto("/me/maths")
    kid.wait_for_function("document.body.dataset.qtoken")
    kid.click("[data-testid=report-open]")
    kid.click("[data-reason=wrong]")
    kid.fill("#reportNote", "I think the answer is 46")
    kid.click("[data-testid=report-send]")
    kid.wait_for_selector("[data-testid=report-msg]:has-text('Report it again tomorrow')")
    assert "not sent" in kid.get_by_test_id("report-msg").inner_text()
    assert kid.input_value("#reportNote") == "I think the answer is 46"
    kid.context.close()
    assert DB.reports.count_documents({"pupil_id": pid}) == 10
    # the parent's own report still goes: the grown-ups have their own limit
    _rows(pid, [("maths", False, 6000, {"q": "What is 6 + 7?", "exp": "13", "got": "12", "detail": "Y9.1.a"})])
    page.goto(f"/children/{pid}#mistakes")
    rep = page.get_by_test_id("report-mistake").first
    rep.locator("summary").click()
    rep.get_by_test_id("report-mistake-send").click()
    page.wait_for_url("**reported=1*")
    assert DB.reports.count_documents({"pupil_id": pid}) == 11
