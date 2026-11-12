"""Wave 5, the Year 4 check and the child's day: a check finished without signal is kept and sent (never lost on
"Marking…"), a check closed in the middle says so next time, extra time for a nervous child, "Get ready" before
question 1, a half-typed answer at time-out, a kind word on every result, a keyboard on a touch tablet, a gentle
pause after answer-bashing, "+N extra today", the Years 1-2 cap on a hard day and an honest time estimate, and the
number line's live number."""
import pathlib

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent, wait_question

TABLET = {"viewport": {"width": 820, "height": 1180}, "is_mobile": True, "has_touch": True}
PHONE = {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}
SAFE = "No connection: your answers are safe. Trying again…"


def _kid(browser, year=4, name="Arjun", targets=None, defaults=False, **kw):
    ctx = browser.new_context(base_url=BASE, **kw)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, name, year, targets=targets, year_defaults=defaults)
    enter_child(pg, name)
    return pg, pid


def _api(pg, url, body):
    return pg.evaluate("""([u, b]) => fetch(u, {method: 'POST', headers: {'Content-Type': 'application/json'},
                          body: JSON.stringify(b)}).then(async r => ({status: r.status, ...(await r.json())}))""", [url, body])


def _start(pg, pid):
    """Open the check page with a fake clock and press Start; returns the check's stored item."""
    pg.clock.install()
    pg.goto("/me/tables/year4-check")
    pg.click("[data-testid=mtc-start]")
    pg.wait_for_function("document.getElementById('count').textContent === 'Get ready…'")
    pg.clock.run_for(3100)
    pg.wait_for_function("document.body.dataset.mtcq === '0'")
    return DB.items.find_one({"pupil_id": pid, "activity": "mtc", "done": False}, sort=[("created", -1)])


def _answer(pg, item, upto, right=lambda i: True):
    """Answer questions 0 .. upto-1 (right, or one more when right(i) is False), Enter on each."""
    for i in range(upto):
        pg.wait_for_function("i => document.body.dataset.mtcq === String(i)", arg=str(i))
        pg.fill("[data-testid=mtc-answer]", str(item["answer"][i] + (0 if right(i) else 1)))
        pg.press("[data-testid=mtc-answer]", "Enter")
        if i < 24:
            pg.clock.run_for(3100)


def test_offline_for_the_last_question_the_check_is_kept_and_sent(browser):
    pg, pid = _kid(browser, 4, **TABLET)
    item = _start(pg, pid)
    _answer(pg, item, 24)
    pg.context.set_offline(True)                                        # the signal goes for question 25
    _answer_last = item["answer"][24]
    pg.wait_for_function("document.body.dataset.mtcq === '24'")
    pg.fill("[data-testid=mtc-answer]", str(_answer_last))
    pg.press("[data-testid=mtc-answer]", "Enter")
    pg.wait_for_function("t => document.getElementById('msg').textContent === t", arg=SAFE)
    assert pg.inner_text("[data-testid=mtc-count]") == "Marking…"
    kept = pg.evaluate("JSON.parse(localStorage.getItem('qz_mtc_done'))")
    assert kept["body"]["token"] == item["_id"] and len(kept["body"]["answers"]) == 25
    pg.clock.run_for(5000)                                              # still trying, still safe
    assert DB.pupils.find_one({"_id": pid}).get("mtc") is None
    pg.context.set_offline(False)                                       # back: it goes by itself
    pg.clock.run_for(2000)
    pg.wait_for_selector("[data-testid=mtc-done]:visible")
    assert pg.inner_text("[data-testid=mtc-score]").startswith("25")
    assert pg.inner_text("[data-testid=mtc-msg]") == ""
    assert pg.evaluate("localStorage.getItem('qz_mtc_done')") is None
    assert [r["score"] for r in DB.pupils.find_one({"_id": pid})["mtc"]] == [25]
    pg.context.close()


def test_a_blip_on_the_last_tick_then_a_reload_or_another_page_sends_it(browser):
    pg, pid = _kid(browser, 4, **TABLET)
    item = _start(pg, pid)
    _answer(pg, item, 24, right=lambda i: i % 2 == 0)
    pg.context.set_offline(True)
    pg.wait_for_function("document.body.dataset.mtcq === '24'")
    pg.fill("[data-testid=mtc-answer]", str(item["answer"][24]))
    pg.click("[data-testid=mtc-keypad] .ent")                           # the blip: ✓ pressed with no signal
    pg.wait_for_function("t => document.getElementById('msg').textContent === t", arg=SAFE)
    pg.context.set_offline(False)
    pg.goto("/me")                                                     # pulled to refresh / tapped My day at once
    pg.wait_for_function("localStorage.getItem('qz_mtc_done') === null")
    pg.wait_for_load_state("load")
    rows = DB.pupils.find_one({"_id": pid})["mtc"]
    assert [r["score"] for r in rows] == [13]
    assert pg.locator("[data-testid=mtc-stopped]").count() == 0         # it counted: no "stopped" on My day
    assert not DB.pupils.find_one({"_id": pid}).get("mtc_open")
    # the same again, but the reload is the check page itself: it sends the check and shows the result
    item = _start(pg, pid)
    _answer(pg, item, 24)
    pg.context.set_offline(True)
    pg.wait_for_function("document.body.dataset.mtcq === '24'")
    pg.fill("[data-testid=mtc-answer]", "1")
    pg.press("[data-testid=mtc-answer]", "Enter")
    pg.wait_for_function("t => document.getElementById('msg').textContent === t", arg=SAFE)
    pg.context.set_offline(False)
    pg.reload()
    pg.wait_for_selector("[data-testid=mtc-done]:visible")
    assert pg.inner_text("[data-testid=mtc-score]").startswith("24")
    assert pg.locator("[data-testid=mtc-stopped]").is_hidden()
    assert [r["score"] for r in DB.pupils.find_one({"_id": pid})["mtc"]] == [13, 24]
    pg.context.close()


def test_a_check_closed_in_the_middle_says_so_next_time(browser):
    pg, pid = _kid(browser, 4, **TABLET)
    item = _start(pg, pid)
    _answer(pg, item, 8)
    pg.goto("/me")                                                     # the tab closed, the app opened again
    note = pg.locator("[data-testid=mtc-stopped]")
    assert "stopped before the end" in note.inner_text() and "Start again" in note.inner_text()
    assert pg.inner_text("[data-testid=mtc-card-go]") == "Start the check again"
    row = DB.pupils.find_one({"_id": pid})["mtc_open"]
    assert len(row) == 1 and row[0]["stopped"] is True                  # the parent sees "started, not finished"
    pg.goto("/me")
    assert len(DB.pupils.find_one({"_id": pid})["mtc_open"]) == 1        # noted once only
    pg.click("[data-testid=mtc-card-go]")
    assert "stopped before the end" in pg.inner_text("[data-testid=mtc-stopped]")
    item = _start(pg, pid)                                                  # a new check: the note goes
    pg.goto("/me")
    assert pg.locator("[data-testid=mtc-stopped]").count() == 1          # (this one was left too)
    unlock_parent(pg)
    pg.goto(f"/children/{pid}")
    assert "closed before the end" in pg.inner_text("[data-testid=mtc-unfinished]")
    pg.context.close()


def test_extra_time_get_ready_after_try_again_and_kind_words(browser):
    pg, pid = _kid(browser, 4, **TABLET)
    unlock_parent(pg)
    pg.goto(f"/children/{pid}/edit")
    pg.check("[data-testid=check-slow]")
    pg.click("form.card button[type=submit]")
    pg.wait_for_url("**saved=1**")
    assert DB.pupils.find_one({"_id": pid})["activities"]["tables"]["slow"] is True
    assert pg.is_checked("[data-testid=check-slow]")
    enter_child(pg, "Arjun")
    item = _start(pg, pid)
    assert "Extra time is on: 9 seconds" in pg.inner_text("[data-testid=mtc-intro]")
    assert pg.inner_text("[data-testid=mtc-sec]") == "9"
    # Q1: a half-typed "1" of 18 when the time runs out is no answer in time
    pg.fill("[data-testid=mtc-answer]", "1")
    pg.clock.run_for(9300)
    pg.clock.run_for(3100)
    for i in range(1, 25):
        pg.wait_for_function("i => document.body.dataset.mtcq === String(i)", arg=str(i))
        pg.fill("[data-testid=mtc-answer]", str(item["answer"][i]))
        pg.press("[data-testid=mtc-answer]", "Enter")
        if i < 24:
            pg.clock.run_for(3100)
    pg.wait_for_selector("[data-testid=mtc-done]:visible")
    assert pg.inner_text("[data-testid=mtc-score]").startswith("24")
    assert "(no answer in time)" in pg.inner_text("[data-testid=mtc-missed]")
    assert "first check with extra time" in pg.inner_text("[data-testid=mtc-kind]")
    assert DB.pupils.find_one({"_id": pid})["mtc"][-1]["secs"] == 9
    # Try again: "Get ready…" before question 1 again, never straight into a running clock
    pg.click("[data-testid=mtc-again]")
    pg.wait_for_function("document.getElementById('count').textContent === 'Get ready…'")
    assert pg.evaluate("document.body.dataset.mtcq") == "" and pg.inner_text("[data-testid=mtc-question]") == ""
    pg.clock.run_for(3100)
    pg.wait_for_function("document.body.dataset.mtcq === '0'")
    item = DB.items.find_one({"activity": "mtc", "pupil_id": pid, "done": False})
    _answer(pg, item, 25, right=lambda i: i >= 7)                       # 18: not a new best, but a kind word
    pg.wait_for_selector("[data-testid=mtc-done]:visible")
    assert pg.locator("[data-testid=mtc-new-best]").is_hidden()
    assert pg.inner_text("[data-testid=mtc-kind]").startswith("Your best is still 24.")
    # the misses list starts short, with "Show all"
    assert pg.locator("[data-testid=mtc-missed] li:visible").count() == 5
    pg.click("[data-testid=mtc-show-all]")
    assert pg.locator("[data-testid=mtc-missed] li:visible").count() == 7 and pg.locator("[data-testid=mtc-show-all]").count() == 0
    pg.context.close()


def test_kind_line_from_real_data():
    from app.drills import tables
    before = [{"score": 15, "facts": ["7x8", "6x7"]}, {"score": 20, "facts": ["7x4"]}, {"score": 16, "facts": ["7x12"]}]
    res = [("7x8", True, False), ("3x7", True, False), ("4x5", False, True)]
    assert tables.mtc_kind(before, 18, res, 6) == "Your best is still 20. The 7s are coming on: you got every one right this time."
    assert tables.mtc_kind(before, 20, [("4x5", True, False)], 6).startswith("You matched your best of 20!")
    assert tables.mtc_kind(before, 18, [("4x5", True, False)], 6) == "Your best is still 20. That's 2 more than last time."
    assert tables.mtc_kind(before, 21, res, 6) == ""                    # a new best has its own big line
    assert "first check" in tables.mtc_kind([], 9, res, 6)
    assert "first check with extra time" in tables.mtc_kind(before, 9, res, 9)   # extra-time bests are kept apart


def test_enter_on_question_one_with_a_keyboard_on_a_touch_tablet(browser):
    pg, pid = _kid(browser, 4, **TABLET)
    item = _start(pg, pid)
    pg.evaluate("document.activeElement && document.activeElement.blur()")     # nothing focused, as on the tablet
    pg.keyboard.type(str(item["answer"][0]))
    pg.keyboard.press("Enter")
    assert pg.evaluate("document.body.dataset.mtcq") == ""              # taken: on to "Get ready…"
    pg.clock.run_for(3100)
    pg.wait_for_function("document.body.dataset.mtcq === '1'")
    pg.context.close()


def test_answer_bashing_gets_a_gentle_pause(browser):
    pg, pid = _kid(browser, 4, targets={"tables": 20}, **TABLET)
    pg.goto("/me/tables")
    prev = None
    for n in range(3):
        doc = wait_question(pg, "tables", pid, prev)
        prev = doc["_id"]
        pg.fill("#answer", str(int(doc["answer"]) + 1))
        pg.press("#answer", "Enter")                                    # under a second: rushed
        pg.wait_for_selector("#next:visible")
        if n < 2:
            assert pg.locator("[data-testid=slow-down]").count() == 0
            pg.click("#next")
    assert "Slow down and read it first" in pg.inner_text("[data-testid=slow-down]")
    assert pg.is_disabled("#next")
    pg.keyboard.press("Enter")                                          # Enter does not skip the pause
    assert pg.evaluate("document.body.dataset.qtoken") == prev
    pg.wait_for_function("!document.getElementById('next').disabled", timeout=8000)
    pg.click("#next")
    wait_question(pg, "tables", pid, prev)
    pg.context.close()


def test_extra_right_answers_show_in_the_header(browser):
    pg, pid = _kid(browser, 4, targets={"tables": 2}, **TABLET)
    pg.goto("/me/tables")
    prev = None
    for n in range(4):
        doc = wait_question(pg, "tables", pid, prev)
        prev = doc["_id"]
        pg.fill("#answer", str(doc["answer"]))
        pg.press("#answer", "Enter")
        if n == 0:
            continue              # before the target, times tables move on by themselves, with no button showing
        pg.wait_for_selector("#next:visible")
        if n == 1:
            assert pg.locator("[data-testid=day-extra]").is_hidden()
        if n < 3:
            pg.click("#next")
    assert pg.inner_text("[data-testid=day-extra]") == "· +2 extra today ★"     # one line, one colour (wave 6)
    pg.context.close()


def test_years_1_2_cap_ends_a_hard_activity_and_the_estimate_is_honest(browser):
    pg, pid = _kid(browser, 2, targets={"tables": 3}, **PHONE)
    pg.goto("/me/tables")
    prev = None
    for n in range(6):                                                  # 6 wrong answers: twice the target
        doc = wait_question(pg, "tables", pid, prev)
        prev = doc["_id"]
        pg.fill("#answer", str(int(doc["answer"]) + 1))
        pg.wait_for_timeout(1600)                                       # tried, not rushed
        pg.press("#answer", "Enter")
        pg.wait_for_selector("#next:visible")
        if n < 5:
            pg.click("#next")
    assert "That’s plenty for today: 6 tries" in pg.inner_text("#dayMsg")
    assert pg.inner_text("#dayDone") == "0"
    pg.goto("/me")
    assert "finished for today" in pg.inner_text("[data-testid=tile-tables]")      # capped: done, with the real count
    # the form: Years 1-4 see the cap; a Year 4 check adds its minutes; from Year 5 only spelling has the cap
    unlock_parent(pg)
    pg.goto(f"/children/{pid}/edit")
    assert pg.locator("[data-testid=plan-cap]").is_visible()
    pg.select_option("#year", "4")
    m = int(pg.inner_text("#planMin"))
    pg.check("[data-testid=on-tables]")
    pg.check("[data-testid=check-tables]")
    assert int(pg.inner_text("#planMin")) == m + 4 or int(pg.inner_text("#planMin")) > m
    assert pg.locator("[data-testid=plan-cap]").is_visible()
    pg.select_option("#year", "6")
    pg.check("[data-testid=on-spelling]")
    assert pg.locator("[data-testid=plan-cap]").is_hidden() and pg.locator("[data-testid=plan-cap-spelling]").is_visible()
    pg.context.close()


def test_number_line_shows_the_arrows_number_before_check(browser):
    ctx = browser.new_context(base_url=BASE, **PHONE)
    pg = ctx.new_page()
    js = (pathlib.Path(__file__).resolve().parent.parent / "app/static/maths/components/number_line.js").read_text()
    pg.set_content('<div id="h" style="width:358px"></div>')
    pg.add_script_tag(content=js)
    pg.evaluate("MComp.number_line.render(document.getElementById('h'), {min: 0, max: 30, step: 1, major: 5}, {year: 2})")
    box = pg.locator("#h svg").first.bounding_box()
    # a tap near 2 on a 0-30 line on a phone: the arrow's number shows, and the closer look opens
    pg.mouse.click(box["x"] + 18 + (box["width"] - 36) * 2 / 30, box["y"] + 46)
    assert pg.evaluate("document.getElementById('h').__getValue()") == 2
    labels = lambda: pg.evaluate("[...document.querySelectorAll('#h svg:first-of-type text')].map(t => t.textContent)")
    assert labels()[-2] == "2"                                          # the arrow's own label, live
    assert pg.locator("#h svg").nth(1).is_visible()                     # the closer look, wide ticks
    pg.mouse.click(box["x"] + 18, box["y"] + 46)                        # on 0: it says 0, and sends 0
    assert pg.evaluate("document.getElementById('h').__getValue()") == 0
    assert labels()[-2] == "0"
    ctx.close()
