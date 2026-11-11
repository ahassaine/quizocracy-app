"""The parent's numbers agree (wave 8): ONE "extra" figure (questions after an activity's target, outside "Practise
my mistakes") on Home, Progress, the printed report and the weekly email, with mistake practice named on its own;
2 of 3 is 67% everywhere; the report's tables say what they count; "to go over" split the way the child's own
screen shows it; "needs help" and the smaller-target hint only once there is enough to go on ("early days"
before); answers in "Practise my mistakes" marked as such; and every parent page fits a 390 px phone."""
import datetime
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

import requests

from app.progress import pct
from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent

TZ = ZoneInfo("Europe/London")
ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _today(back=0):
    return (datetime.datetime.now(TZ).date() - datetime.timedelta(days=back)).isoformat()


def _only(pid, **targets):
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {k: {"on": k in targets, "target": targets.get(k, 5)}
                                                                for k in ALL}}, "$unset": {"plan_log": ""}})


def _rows(pid, rows, minutes_ago=30, back=0):
    """(activity, correct, extra fields) written straight into the record, 20 seconds apart, oldest first."""
    fid = DB.pupils.find_one({"_id": pid})["family_id"]
    t0 = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_ago, days=back)
    DB.attempts.insert_many([{"pupil_id": pid, "family_id": fid, "activity": a, "correct": c, "ms": 5000,
                              "detail": f"{a}{back}-{i}", "day": _today(back), "ts": t0 + datetime.timedelta(seconds=20 * i),
                              **({} if c else {"q": f"Q{i}", "exp": "1", "got": "2"}), **x}
                             for i, (a, c, x) in enumerate(rows)])


def test_one_rounding_for_every_percent():
    assert pct(2, 3) == 67 and pct(1, 3) == 33 and pct(1, 8) == 13 and pct(5, 12) == 42
    assert pct(199, 200) == 99 and pct(1, 300) == 1 and pct(0, 5) == 0 and pct(3, 3) == 100 and pct(1, 0) is None


def test_one_extra_figure_on_home_progress_and_the_report(page):
    email = signup(page)
    pid = add_child(page, "Mia", 5)
    _only(pid, tables=2, spelling=3)
    _rows(pid, [("tables", True, {}), ("tables", True, {}),                                   # the target
                ("tables", True, {}), ("tables", True, {}), ("tables", False, {}),            # 3 extra, 2 right
                ("tables", True, {"fix": True, "fixing": True}),                              # a mistake practised
                ("tables", True, {"fix": True}),                                              # filler while it waits
                ("spelling", True, {}), ("spelling", True, {}), ("spelling", True, {}),
                ("spelling", False, {"other": True, "exp": "fight", "got": "rite"})])          # a real word: left out
    page.goto("/home")
    card = page.get_by_test_id("kid-Mia")
    chips = card.locator(".chips").inner_text()
    assert "Times tables 2/2 +3" in chips and "Spelling 3/3" in chips and "Spelling 3/3 +" not in chips, chips
    assert "+ 3 extra questions after the targets, 67% right first time" in card.get_by_test_id("day-extra").inner_text()
    assert "+ 1 mistake practised" in card.get_by_test_id("day-fix").inner_text()
    assert card.locator("[data-testid^=home-extra-]").count() == 0           # no second, 7-day "extra" on Home
    page.goto(f"/children/{pid}")
    today = page.get_by_test_id("today").inner_text()
    assert "Times tables 2/2 +3" in today and "+ 3 extra questions" in today and "1 mistake practised" in today
    assert "plus 3 extra questions, 67% right first time" in page.get_by_test_id("glance-extra-tables").inner_text()
    assert "+ 1 mistake practised" in page.get_by_test_id("glance-fix-tables").inner_text()
    hist = page.get_by_test_id("history").inner_text()
    assert "2/2 +3" in hist and "1 mistake practised" in hist, hist
    page.goto(f"/children/{pid}/report?range=7")
    row = page.get_by_test_id("report-act-tables").inner_text()
    assert "100% (2 of 2)" in row and "3 questions, 67% right first time" in row and row.rstrip().endswith("7"), row
    sp = page.get_by_test_id("report-act-spelling").inner_text()
    assert "100% (3 of 3)" in sp and sp.rstrip().endswith("4"), sp
    rule = page.get_by_test_id("report-acts-rule").inner_text()
    assert "Practise my mistakes" in rule and "1 real word typed for the spelling word asked" in rule, rule
    assert page.get_by_test_id("report-totals-rule").is_visible()
    assert page.get_by_test_id("first-pct").inner_text() == "100%"             # the table's 5 of 5 added up
    # the weekly email: the same figure, and mistake practice on its own
    monday = (datetime.datetime.now(TZ).date() - datetime.timedelta(days=datetime.datetime.now(TZ).weekday())).isoformat()
    out = subprocess.run([sys.executable, "scripts/weekly_email.py", "--dry-run", "--to", email, "--week", monday],
                         cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))), capture_output=True, text=True,
                         env={**os.environ, "QZ_MONGO_URL": DB.client.address and f"mongodb://{DB.client.address[0]}:{DB.client.address[1]}",
                              "QZ_DB": DB.name, "QZ_MAIL_MODE": "capture"}, timeout=60).stdout
    assert "+ 3 extra questions after the targets, 67% right first time · + 1 mistake practised" in out, out


def test_two_of_three_is_67_percent(page):
    signup(page)
    pid = add_child(page, "Ada", 3)
    _only(pid, tables=3)
    _rows(pid, [("tables", True, {}), ("tables", False, {}), ("tables", True, {})])
    page.goto("/home")
    assert page.get_by_test_id("pct").inner_text() == "67%"                   # 2 of the 3 planned right answers
    assert "67%" in page.get_by_test_id("day-stats").inner_text()             # 2 of 3 right first time
    page.goto(f"/children/{pid}")
    assert "67%" in page.get_by_test_id("glance-acts").inner_text()


def test_needs_help_and_a_smaller_target_wait_for_enough_practice(page):
    signup(page)
    early = add_child(page, "Finn", 4)
    _only(early, tables=10)
    _rows(early, [("tables", i % 4 == 0, {}) for i in range(40)])            # one day, 40 tries, 25% right
    page.goto("/home")
    acc = page.get_by_test_id("kid-Finn").get_by_test_id("home-accuracy").inner_text()
    assert "needs help" not in acc and "early days" in acc, acc
    page.goto(f"/children/{early}")
    assert page.get_by_test_id("needs-help").count() == 0 and page.get_by_test_id("early-days").count() == 1
    assert page.get_by_test_id("try-lower").count() == 0
    # 3 days and 36 first tries: "needs help", but no smaller target in the child's first week
    pid = add_child(page, "Gus", 4)
    _only(pid, tables=10)
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime.utcnow() - datetime.timedelta(days=2)}})
    for back in (2, 1, 0):
        _rows(pid, [("tables", i % 4 == 0, {}) for i in range(12)], back=back)
    page.goto(f"/children/{pid}")
    assert page.get_by_test_id("needs-help").count() == 1
    assert page.get_by_test_id("try-lower").count() == 0
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime.utcnow() - datetime.timedelta(days=8)}})
    page.goto(f"/children/{pid}")
    assert "smaller daily target" in page.get_by_test_id("try-lower").inner_text()


def test_to_go_over_is_split_like_the_childs_screen(page):
    signup(page)
    pid = add_child(page, "Leo", 6)
    _only(pid, spelling=10)
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    now = datetime.datetime.utcnow()
    old = now - datetime.timedelta(hours=3)
    row = {"pupil_id": pid, "family_id": fam, "day": _today(), "ms": 3000, "activity": "spelling",
           "q": "Spell the word you heard"}
    words = ["people", "because", "island", "minute", "special", "strange", "thought", "through", "various",
             "weight", "woman", "women"]
    DB.attempts.insert_many([{**row, "correct": False, "detail": w, "exp": w, "got": w[:-1], "ts": old} for w in words]
                            + [{**row, "correct": False, "detail": "answer", "exp": "answer", "got": "anser",
                                "ts": now - datetime.timedelta(minutes=20)},
                               {**row, "correct": True, "detail": "answer", "ts": now - datetime.timedelta(minutes=10)}])
    enter_child(page, "Leo")
    button = page.inner_text("[data-testid=fix-all]")
    n = int(re.search(r"\((\d+)\)", button).group(1))
    later = page.inner_text("[data-testid=fix-later]")
    assert n == 10 and later.startswith("1 more"), (button, later)                # a round of 10; 1 rests
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    total = page.inner_text("[data-testid=mistakes-total]")
    assert total.startswith("13 to go over: 12 ready now, 1 comes back"), total
    rule = page.inner_text("[data-testid=mistakes-rule]")
    assert "“Practise my mistakes (10)”: a round takes 10 at a time" in rule and "“1 more comes back later”" in rule, rule


def test_answers_in_practise_my_mistakes_are_marked(page):
    signup(page)
    pid = add_child(page, "Ivy", 4)
    _only(pid, spelling=5)
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.attempts.insert_one({"pupil_id": pid, "family_id": fam, "day": _today(), "ms": 3000, "activity": "spelling",
                            "correct": False, "detail": "because", "q": "Spell the word you heard", "exp": "because",
                            "got": "becuase", "ts": datetime.datetime.utcnow() - datetime.timedelta(hours=3)})
    enter_child(page, "Ivy")
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    q = s.post(BASE + "/api/spelling/next", json={"fix": 1}).json()
    assert q["ok"] and q.get("fixing"), q
    word = DB.items.find_one({"_id": q["token"]})["answer"]
    assert word == "because"
    assert s.post(BASE + "/api/spelling/check", json={"token": q["token"], "value": word}).json()["correct"]
    r = DB.attempts.find_one({"pupil_id": pid, "detail": "because", "correct": True})
    assert r.get("fix") and r.get("fixing"), r
    # an ordinary question is not marked
    q = s.post(BASE + "/api/spelling/next", json={}).json()
    s.post(BASE + "/api/spelling/check", json={"token": q["token"], "value": "zzqx"})
    r = DB.attempts.find_one({"pupil_id": pid}, sort=[("ts", -1)])
    assert "fix" not in r and "fixing" not in r, r


def test_every_parent_page_fits_a_390_phone(browser, page):
    signup(page, family="The Longname-Familyname household")
    pid = add_child(page, "Evangeline", 5)
    for back in (1, 0):
        _rows(pid, [(a, i % 3 != 0, {}) for a in ("maths", "tables", "spelling", "grammar", "science") for i in range(16)],
              back=back)
    ctx = browser.new_context(base_url=BASE, viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    ctx.add_cookies(page.context.cookies())
    pg = ctx.new_page()
    for path in ("/home", f"/children/{pid}", "/board", f"/children/{pid}/report", f"/children/{pid}/edit",
                 "/settings", "/help", f"/children/{pid}/examples?subject=maths&strand=Number+%26+place+value"):
        pg.goto(path)
        assert pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), path
        if path == f"/children/{pid}":
            assert pg.get_by_test_id("history-hint").is_visible()            # the wide table says it scrolls
    ctx.close()
