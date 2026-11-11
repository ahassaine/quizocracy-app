"""A calm, predictable child screen (wave 6): a grown-up's "Calm screen" (on Add a child and in Settings, on by
itself with reduced motion, locked in the child's Aa panel); read-aloud on / questions only / off and slower;
times tables never move on by themselves while a button is on screen, with a calm screen or in Years 1-2;
"Practise my mistakes" waits for a press before another activity, in rounds of at most 10 mixed across subjects;
an "I don't know" button that the parent sees neutrally; a shared tablet's tiles, "Carry on" and a neutral Board."""
import datetime

import requests

from app import progress
from app.routes.child import FIX_BATCH, pick_batch
from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent, wait_question

ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")
PHONE = dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _plan(pid, acts, target=10):
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {k: {"on": k in acts, "target": target} for k in ALL}},
                                        "$unset": {"plan_log": ""}})


def _wrong(s, act):
    q = s.post(BASE + f"/api/{act}/next", json={}).json()
    r = s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": "9999" if act == "tables" else "zzqx"}).json()
    if r.get("retry"):
        r = s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": "zzqx"}).json()
    assert r["correct"] is False
    return q


def test_pick_batch_takes_subjects_in_turn():
    open_ = {"tables": [f"t{i}" for i in range(32)], "spelling": ["s1", "s2"], "grammar": ["g1", "g2", "g3"]}
    b = pick_batch(open_, ["maths", "tables", "spelling", "grammar"])
    assert sum(len(v) for v in b.values()) == FIX_BATCH == 10
    assert b["spelling"] == ["s1", "s2"] and b["grammar"] == ["g1", "g2", "g3"] and b["tables"] == [f"t{i}" for i in range(5)]
    assert pick_batch({"tables": ["a", "b"]}, ["tables"]) == {"tables": ["a", "b"]}


def test_calm_screen_from_add_a_child_is_locked_for_the_child(browser):
    for spec, width in ((PHONE, 390), ({"viewport": {"width": 1280, "height": 800}}, 1280)):
        pg = browser.new_context(base_url=BASE, **spec).new_page()
        pg.set_default_timeout(15000)
        signup(pg)
        pg.goto("/children/new")
        pg.fill("#name", "Theo")
        pg.select_option("#year", "2")
        pg.fill("#pin", "4826")
        pg.click("[data-testid=new-calm] summary")
        pg.check("[data-testid=calm]")
        pg.select_option("[data-testid=voice]", "questions")
        pg.select_option("[data-testid=voice-rate]", "slower")
        pg.click("form.card button[type=submit]")
        pg.wait_for_url("**/children/p_*?added=1*")
        pid = pg.url.split("/children/")[1].split("?")[0]
        p = DB.pupils.find_one({"_id": pid})
        assert p["calm"] is True and p["voice"] == {"mode": "questions", "rate": "slower"}
        enter_child(pg, "Theo", "4826")
        assert "a11y-calm" in pg.evaluate("document.documentElement.className")
        assert pg.evaluate("document.body.dataset.voice") == "questions"
        pg.click("[data-testid=a11y-open]")
        box = pg.locator("[data-testid=a11y-calm]")
        assert box.is_checked() and box.is_disabled()
        assert "set by a grown-up" in pg.inner_text("[data-testid=a11y-panel]")
        assert pg.evaluate("document.documentElement.scrollWidth") <= width
        pg.click("#a11yDone")
        # a right answer: the same plain "Correct.", no star, no confetti
        pg.goto("/me/tables")
        it = wait_question(pg, "tables", pid)
        pg.fill("#answer", str(it["answer"]))
        pg.click("#check")
        pg.wait_for_selector("#feedback.yes")
        assert pg.inner_text("#feedback").strip().startswith("✓ Correct.")
        assert pg.locator("#feedback.joy, .joy-star").count() == 0
        pg.evaluate("QZ.confetti(100)")
        assert pg.locator(".confetti").count() == 0
        pg.screenshot(path=f"/tmp/claude-1000/-home-ali/eec900ab-9c24-4216-8391-43f89d30a550/scratchpad/w6r/b_calm_{width}.png")
        # and nothing moves on by itself
        pg.wait_for_timeout(1500)
        assert pg.evaluate("document.body.dataset.qtoken") == it["_id"] and pg.is_visible("#next")
        pg.context.close()


def test_parent_turns_calm_off_and_old_less_movement_becomes_the_grown_ups(page):
    signup(page)
    pid = add_child(page, "Mia", 3)
    DB.pupils.update_one({"_id": pid}, {"$set": {"reading": {"big": False, "dys": False, "space": False, "calm": True, "contrast": False}},
                                        "$unset": {"calm": "", "voice": ""}})     # a child from before wave 6
    enter_child(page, "Mia")
    assert "a11y-calm" in page.evaluate("document.documentElement.className")
    page.click("[data-testid=a11y-open]")
    assert page.locator("[data-testid=a11y-calm]").is_disabled()       # the old "Less movement": kept as the grown-up's
    page.click("[data-testid=a11y-big]")
    page.wait_for_timeout(600)
    assert DB.pupils.find_one({"_id": pid})["calm"] is True
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    assert page.is_checked("[data-testid=calm]") and page.locator("[data-testid=read-calm]").count() == 0
    page.uncheck("[data-testid=calm]")
    page.click("form.card button[type=submit] >> text=Save")
    page.wait_for_url("**saved=1*")
    p = DB.pupils.find_one({"_id": pid})
    assert p["calm"] is False and p["reading"]["calm"] is False and p["reading"]["big"] is True
    enter_child(page, "Mia")
    assert "a11y-calm" not in page.evaluate("document.documentElement.className")
    page.click("[data-testid=a11y-open]")
    assert page.locator("[data-testid=a11y-calm]").is_enabled()          # the child's own choice again


def test_reduced_motion_is_a_calm_screen(browser):
    ctx = browser.new_context(base_url=BASE, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Ada", 5, targets={"tables": 10})
    enter_child(pg, "Ada")
    assert "a11y-calm" in pg.evaluate("document.documentElement.className")
    pg.goto("/me/tables")
    it = wait_question(pg, "tables", pid)
    pg.fill("#answer", str(it["answer"]))
    pg.click("#check")
    pg.wait_for_selector("#feedback.yes")
    pg.wait_for_timeout(1500)
    assert pg.evaluate("document.body.dataset.qtoken") == it["_id"]      # waits for the press
    ctx.close()


def test_times_tables_quick_flow_never_under_a_button(page):
    signup(page)
    pid = add_child(page, "Kai", 5, targets={"tables": 2})
    enter_child(page, "Kai")
    page.goto("/me/tables")
    it = wait_question(page, "tables", pid)
    page.fill("#answer", str(it["answer"]))
    page.click("#check")
    page.wait_for_selector("#feedback.yes")
    assert page.is_hidden("#next")                                      # no button to reach for while it moves on
    it2 = wait_question(page, "tables", pid, it["_id"])                 # the quick flow, Year 3 up
    page.fill("#answer", str(it2["answer"]))
    page.click("#check")
    page.wait_for_selector("#feedback.yes")
    page.wait_for_timeout(1500)                                         # target reached: Back to My day / Keep going
    assert page.evaluate("document.body.dataset.qtoken") == it2["_id"] and page.is_visible("[data-testid=back-day]")


def test_years_1_2_tables_wait_for_the_press(page):
    signup(page)
    pid = add_child(page, "Ivy", 2, targets={"tables": 5})
    enter_child(page, "Ivy")
    page.goto("/me/tables")
    it = wait_question(page, "tables", pid)
    page.fill("#answer", str(it["answer"]))
    page.click("#check")
    page.wait_for_selector("#feedback.yes")
    page.wait_for_timeout(1500)
    assert page.evaluate("document.body.dataset.qtoken") == it["_id"] and page.is_visible("#next")


def test_practise_my_mistakes_is_a_short_mixed_round(page):
    signup(page)
    pid = add_child(page, "Liv", 4)
    _plan(pid, ("tables", "grammar"))
    enter_child(page, "Liv")
    s = _session(page)
    for _ in range(12):
        _wrong(s, "tables")
    for _ in range(3):
        _wrong(s, "grammar")
    DB.attempts.update_many({"pupil_id": pid}, {"$set": {"ts": datetime.datetime.utcnow() - datetime.timedelta(hours=1)}})
    page.goto("/me")
    assert page.inner_text("[data-testid=fix-all]") == f"Practise my mistakes ({FIX_BATCH})"      # never 15
    assert page.inner_text("[data-testid=fix-grammar]") == "3 to fix"
    f = s.post(BASE + "/api/tables/next", json={"fix": 1}).json()
    assert f["fix_total"] == FIX_BATCH and f["fixing"]
    since = f["fix_since"]
    assert DB.pupils.find_one({"_id": pid})["fix_batch"]["since"] == since
    keys = DB.pupils.find_one({"_id": pid})["fix_batch"]["keys"]
    assert sum(1 for k, _ in keys if k == "grammar") == 3 and len(keys) == FIX_BATCH


def test_i_dont_know_is_a_neutral_miss(page):
    signup(page)
    pid = add_child(page, "Noor", 8)
    _plan(pid, ("maths", "science"), target=5)
    enter_child(page, "Noor")
    page.goto("/me/maths")
    it = wait_question(page, "maths", pid)
    assert page.is_visible("[data-testid=idk]")
    page.click("[data-testid=idk]")
    page.wait_for_selector("[data-testid=idk-said]")
    assert "Not quite" not in page.inner_text("#feedback") and "Answer:" in page.inner_text("#feedback")
    assert page.is_hidden("[data-testid=idk]") and page.is_visible("#next")
    row = DB.attempts.find_one({"pupil_id": pid, "activity": "maths"})
    assert row["correct"] is False and row["idk"] is True and row["got"] == ""
    s = _session(page)
    q = s.post(BASE + "/api/science/next", json={}).json()
    r = s.post(BASE + "/api/science/check", json={"token": q["token"], "idk": True, "ms": 300}).json()
    assert r["ok"] and r["idk"] and not r["correct"] and r["expected"]
    unlock_parent(page)
    page.goto("/home")
    card = page.locator("[data-testid='kid-Noor']")
    assert "I don't know" in card.locator("[data-testid=flag-idk]").inner_text()
    assert card.locator("[data-testid=flag-guesses]").count() == 0 and card.locator("[data-testid=flag-rushed]").count() == 0
    page.goto(f"/children/{pid}")
    assert page.locator("[data-testid=mistake-idk]").count() >= 2
    assert "I don't know" in page.inner_text("[data-testid=history]")
    assert it["_id"]


def test_shared_tablet_tiles_carry_on_and_a_neutral_board(page):
    signup(page)
    ben = add_child(page, "Ben", 4)
    _plan(ben, ("maths", "tables"), target=4)
    add_child(page, "Ava", 3)
    enter_child(page, "Ben")
    s = _session(page)
    q = s.post(BASE + "/api/tables/next", json={}).json()
    s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": DB.items.find_one({"_id": q["token"]})["answer"]})
    page.goto("/me")
    assert page.inner_text("[data-testid=next-activity]").strip() == "Carry on: Times tables →"
    page.goto("/board")                                                  # the family's screen: Ben is signed out
    assert page.locator("[data-testid=child-name]").count() == 0
    assert page.goto("/me").url.endswith("/learn")
    assert page.inner_text("[data-testid=tile-pct-Ben]") == "13%"        # 1 of 8 planned answers (12.5, to the nearest)
    assert page.inner_text("[data-testid=tile-pct-Ava]") == "0%"


def test_read_aloud_setting_and_help(page):
    signup(page)
    pid = add_child(page, "Sam", 2)
    for mode, button, talks in (("off", 0, False), ("questions", 1, False), ("on", 1, True)):
        DB.pupils.update_one({"_id": pid}, {"$set": {"voice": {"mode": mode, "rate": "slower"}}})
        enter_child(page, "Sam")
        page.goto("/me/maths")
        wait_question(page, "maths", pid)
        assert page.locator("[data-testid=speak]").count() == button, mode
        assert page.evaluate("window.Speak.talks") is talks, mode
    page.goto("/help")
    for word in ("confetti", "autism", "calm", "sensory", "animation", "motion"):
        page.fill("[data-testid=help-search]", word)
        page.wait_for_timeout(150)
        assert page.is_visible("#calm"), word
    page.fill("[data-testid=help-search]", "mute")
    page.wait_for_timeout(150)
    assert page.is_visible("#read-aloud")
