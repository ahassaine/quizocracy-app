"""Do families stay? The team's funnel page and the parents' "How is it going?" cards (app/funnel.py)."""
import datetime
import os
import secrets
import subprocess
import sys
from zoneinfo import ZoneInfo

import pytest

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup

ROOT = os.path.dirname(os.path.dirname(__file__))
ALPH = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
pytestmark = pytest.mark.skipif(BASE.startswith("https://"), reason="writes dates straight into the database")


def _member(name="Ali", role="admin"):
    slug = "".join(secrets.choice(ALPH) for _ in range(10))
    DB.team_members.insert_one({"_id": slug, "name": name, "initials": name[:2], "role": role,
                                "telegram_chat_id": None, "active": True, "created": datetime.datetime.utcnow()})
    return slug


def _today():
    return datetime.datetime.now(ZoneInfo("Europe/London")).date()


def _fam(email):
    return DB.accounts.find_one({"email": email})["family_id"]


def _back(fid, days):
    """Move the family's sign-up `days` days into the past (noon UTC, so the London day is plain)."""
    d = _today() - datetime.timedelta(days=days)
    DB.families.update_one({"_id": fid}, {"$set": {"created": datetime.datetime(d.year, d.month, d.day, 12)}})
    return d


def _answer_on(fid, pid, day):
    """One answer by the child on that London day (day 1 = the sign-up day)."""
    DB.attempts.insert_one({"pupil_id": pid, "family_id": fid, "activity": "tables", "correct": True, "ms": 3000,
                            "detail": "3x4", "day": day.isoformat(),
                            "ts": datetime.datetime(day.year, day.month, day.day, 15)})


def test_funnel_page(page):
    ali = _member()
    email = signup(page, family="Funnel family")
    fid = _fam(email)
    pid = add_child(page, "Lina", 4)
    d1 = _back(fid, 22)                                         # signed up 22 days ago: weeks 1-3 are over
    DB.pupils.update_one({"_id": pid}, {"$set": {"created": datetime.datetime(d1.year, d1.month, d1.day, 13)}})
    for n in (1, 2, 9):                                         # active on day 1, day 2 and day 9 (week 2)
        _answer_on(fid, pid, d1 + datetime.timedelta(days=n - 1))
    # the board's front page links to it; a stranger gets nothing
    page.goto(f"/team/{ali}")
    page.click("[data-testid=funnel-link]")
    page.wait_for_url(f"**/team/{ali}/funnel")
    assert page.goto("/team/notAmember1/funnel").status == 404
    # an @example.test family is a test account: left out unless asked for
    page.goto(f"/team/{ali}/funnel?q={email}")           # q: the table lists the newest 300 otherwise
    assert page.locator(f"[data-testid=fam-{fid}]").count() == 0
    assert "Test accounts left out" in page.inner_text("[data-testid=funnel-tests]")
    page.goto(f"/team/{ali}/funnel?tests=1&q={email}")
    row = page.locator(f"[data-testid=fam-{fid}]").inner_text()
    cells = row.split("\t")
    fmt = lambda d: f"{d.day} {d:%b}"
    assert fmt(d1) in cells[1] and fmt(d1) in cells[3] and fmt(d1) in cells[4], cells           # signed up, child, answer
    assert cells[5].strip() == fmt(d1 + datetime.timedelta(days=1))                            # day 2
    assert cells[6].strip() == fmt(d1) and cells[7].strip() == fmt(d1 + datetime.timedelta(days=8))   # weeks 1, 2
    assert cells[8].strip() == "–" and cells[9].strip() == "…" and cells[10].strip() == "3", cells   # week 3 missed, 4 open
    # marking it "Not a test" brings it into the default view and into its week's numbers
    page.locator(f"[data-testid=fam-{fid}] button").click()
    page.wait_for_url(f"**/team/{ali}/funnel?tests=1#families")
    page.goto(f"/team/{ali}/funnel?q={email}")
    assert page.locator(f"[data-testid=fam-{fid}]").count() == 1
    monday = d1 - datetime.timedelta(days=d1.weekday())
    week = page.locator("[data-testid=cohort]", has_text=f"Week of {monday.day} {monday:%b %Y}")
    assert week.locator("[data-testid=cell-week2]").inner_text().startswith("1")
    assert week.locator("[data-testid=cell-week4]").inner_text() == "not yet"           # nobody's week 4 is over yet
    # deleting the child keeps the family's dates (never its answers)
    page.goto(f"/children/{pid}/delete")
    page.fill("[data-testid=delete-password]", PASSWORD)
    page.click("[data-testid=delete-confirm]")
    page.wait_for_url("**/home?deleted=1*")
    assert DB.attempts.count_documents({"family_id": fid}) == 0
    page.goto(f"/team/{ali}/funnel?q={email}")
    after = page.locator(f"[data-testid=fam-{fid}]").inner_text().split("\t")
    assert after[1:11] == cells[1:11], (after, cells)
    DB.families.update_one({"_id": fid}, {"$unset": {"test": 1}})


def _watch(since):
    env = dict(os.environ, QZ_MONGO_URL=os.getenv("QZ_TEST_MONGO", "mongodb://127.0.0.1:27027"),
               QZ_DB=DB.name, QZ_PUBLIC_URL=BASE, QZTEAM_SINCE=since)
    return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "team_watch.py")], env=env,
                          capture_output=True, text=True, check=True).stdout


def test_feedback_cards(page, browser):
    ali = _member()
    email = signup(page, family="Card family")
    fid = _fam(email)
    pid = add_child(page, "Omar", 5)
    d1 = _back(fid, 4)
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").count() == 0            # no card before the 3rd active day
    for n in (1, 2):
        _answer_on(fid, pid, d1 + datetime.timedelta(days=n))
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").count() == 0
    _answer_on(fid, pid, _today())
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").is_visible()
    assert "How is it going?" in page.inner_text("[data-testid=feedback-card]")
    # children never see it: Home is parent mode only
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login"); kid.fill("#email", email); kid.fill("#password", PASSWORD); kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Omar")
    kid.goto("/home")
    assert "/home" not in kid.url and kid.locator("[data-testid=feedback-card]").count() == 0
    r = kid.request.post("/home/feedback", form={"card": "d3", "action": "send", "mood": "bad", "text": "from the child"})
    assert DB.feedback.find_one({"family_id": fid, "card": "d3"})["status"] == "shown", r.status
    kid.context.close()
    # Send with nothing picked asks again; a face and a few words are kept and posted to the team board
    page.click("[data-testid=feedback-send]")
    assert page.locator("[data-testid=feedback-empty]").is_visible()
    since = (datetime.datetime.utcnow() - datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    page.click("[data-testid=mood-good]")
    page.fill("[data-testid=feedback-text]", "Omar asks to do his tables now")
    page.click("[data-testid=feedback-send]")
    page.wait_for_url("**/home?fb=thanks")
    assert page.locator("[data-testid=feedback-thanks]").is_visible()
    assert page.locator("[data-testid=feedback-card]").count() == 0
    fb = DB.feedback.find_one({"family_id": fid, "card": "d3"})
    assert fb["status"] == "sent" and fb["mood"] == "good" and fb["text"] == "Omar asks to do his tables now"
    t = DB.team_threads.find_one({"kind": "family_feedback"})
    msg = DB.team_messages.find_one({"_id": fb["team_msg"]})
    assert t and msg["tid"] == t["_id"] and "😊 Good" in msg["text"] and "Card family" in msg["text"]
    wakes = [l for l in _watch(since).splitlines() if l.startswith("QZTEAM ")]
    assert any("Omar asks to do his tables now" in l and "Family feedback" in l for l in wakes), wakes
    # a second post of the same card changes nothing
    page.request.post("/home/feedback", form={"card": "d3", "action": "send", "mood": "bad"})
    assert DB.feedback.find_one({"_id": fb["_id"]})["mood"] == "good"
    assert DB.team_messages.count_documents({"tid": t["_id"], "text": {"$regex": "Card family"}}) == 1
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").count() == 0
    # from day 14 the second card shows; "No thanks" closes it for good, and posts nothing
    _back(fid, 13)
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").is_visible()
    page.click("[data-testid=feedback-dismiss]")
    page.wait_for_url("**/home")
    assert page.locator("[data-testid=feedback-card]").count() == 0
    assert DB.feedback.find_one({"family_id": fid, "card": "d14"})["status"] == "dismissed"
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").count() == 0
    assert DB.team_messages.count_documents({"tid": t["_id"], "text": {"$regex": "Card family"}}) == 1
    # the team sees the answers on the funnel page (test accounts included)
    page.goto(f"/team/{ali}/funnel?tests=1")
    assert "Omar asks to do his tables now" in page.inner_text("main")
    # the data download has the answers; deleting the family deletes them, the board's copy too
    exp = page.request.get("/account/export").json()
    assert {d["card"]: d["status"] for d in exp["feedback"]} == {"d3": "sent", "d14": "dismissed"}
    page.goto("/settings")
    page.fill("#confirm", "DELETE"); page.fill("#delpw", PASSWORD)
    page.click("form[action='/account/delete'] button")
    page.wait_for_url("**/?deleted=1")
    assert DB.feedback.count_documents({"family_id": fid}) == 0 and DB.team_messages.count_documents({"_id": msg["_id"]}) == 0
    t = DB.team_threads.find_one({"_id": t["_id"]})
    assert "Omar" not in t["last_preview"] and t["count"] == DB.team_messages.count_documents({"tid": t["_id"]})


def test_feedback_card_retires_unanswered(page):
    email = signup(page, family="Busy family")
    fid = _fam(email)
    pid = add_child(page, "Ines", 3)
    d1 = _back(fid, 5)
    for n in (0, 1, 2):
        _answer_on(fid, pid, d1 + datetime.timedelta(days=n))
    page.goto("/home")
    assert page.locator("[data-testid=feedback-card]").is_visible()
    page.goto("/home")                                       # still there on the next visit
    assert page.locator("[data-testid=feedback-card]").is_visible()
    DB.feedback.update_one({"family_id": fid, "card": "d3"},
                           {"$set": {"shown_at": datetime.datetime.utcnow() - datetime.timedelta(days=8)}})
    page.goto("/home")                                       # a week on, never answered: it does not nag
    assert page.locator("[data-testid=feedback-card]").count() == 0
