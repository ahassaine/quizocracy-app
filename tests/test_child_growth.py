"""The child's screens (wave 4): the day's finish line said and shown, the next activity as the big button, a
streak and "this week" that grow, moments when a skill becomes secure or a mistake is put right, one PIN per
child, the shared-tablet idle lock, answers kept across a lost connection, pictures for Year 1 questions, and
no run of one kind of question for the youngest."""
import datetime
import itertools

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup, wait_question
from app.activities import ACTIVITIES
from app.drills import maths as maths_drill
from app.maths import maths_engine
from app.maths import maths_mastery as mm
from app import deps
from test_maths_ladder import _walk

PHONE = dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)


def _day(n):
    return (datetime.date.today() - datetime.timedelta(days=n)).isoformat()


def _only_tables(pid, created_days_ago=4):
    acts = {k: {"on": k == "tables", "target": 1} for k in ACTIVITIES}
    DB.pupils.update_one({"_id": pid}, {"$set": {
        "activities": acts, "created": datetime.datetime.utcnow() - datetime.timedelta(days=created_days_ago)}})


def test_streak_finish_line_and_put_right_moment(page):
    signup(page)
    pid = add_child(page, "Asha", 4)
    _only_tables(pid)
    # done 3 days ago and yesterday; the day between was a day off, which does not break the streak
    DB.pupils.update_one({"_id": pid}, {"$set": {"kept": {_day(1): {"pct": 100, "reward": ""}, _day(3): {"pct": 100, "reward": ""}},
                                                 "days_off": [{"from": _day(2), "to": _day(2)}]}})
    # an old times-tables mistake, ready to put right
    DB.attempts.insert_one({"pupil_id": pid, "family_id": DB.pupils.find_one({"_id": pid})["family_id"], "activity": "tables",
                            "correct": False, "ms": 3000, "detail": "7x8", "day": _day(1),
                            "ts": datetime.datetime.utcnow() - datetime.timedelta(days=1), "q": "7 × 8 =", "exp": "56", "got": "54"})
    enter_child(page, "Asha")
    # the next unfinished activity is the big button; "Practise my mistakes" is the plain one beside it
    nxt = page.locator("[data-testid=next-activity]")
    assert "Times tables" in nxt.inner_text() and "primary" in nxt.get_attribute("class")
    assert "primary" not in page.get_attribute("[data-testid=fix-all]", "class")
    assert "2 days in a row" in page.inner_text("[data-testid=streak]")          # today does not break it yet
    page.click("[data-testid=fix-all]")
    item = wait_question(page, "tables", pid)
    page.fill("#answer", str(item["answer"]))
    page.click("#check")
    page.wait_for_selector("#feedback.yes")
    assert "put right a mistake" in page.inner_text("[data-testid=win-moment]")
    # the target is reached: "Back to My day" is the main button, "Keep going" the small one
    assert page.is_visible("[data-testid=back-day]") and page.inner_text("#next") == "Keep going"
    assert "big" not in page.get_attribute("#next", "class")
    page.click("[data-testid=back-day]")
    page.wait_for_url("**/me")
    assert "3 days in a row" in page.inner_text("[data-testid=streak]")
    assert "1 mistake put right" in page.inner_text("[data-testid=week-wins]")
    assert page.is_visible("[data-testid=switch-tip]") and page.locator("[data-testid=next-activity]").count() == 0
    page.goto("/board")
    assert "3 days in a row" in page.inner_text("[data-testid=board-Asha] [data-testid=streak]")


def test_siblings_cannot_share_a_pin(page):
    signup(page)
    add_child(page, "Amir", 3, pin="0707")
    page.goto("/children/new")
    page.fill("#name", "Lina")
    page.select_option("#year", "2")
    page.fill("#pin", "0707")
    page.click("form.card button[type=submit]")
    assert "Amir already uses this PIN. Pick a different one." in page.inner_text(".err")
    lina = add_child(page, "Lina", 2, pin="1212")
    page.goto(f"/children/{lina}/edit")
    page.fill("#pin", "0707")
    page.click("form.card button[type=submit]")
    assert "Amir already uses this PIN" in page.inner_text(".err")
    assert DB.pupils.find_one({"_id": lina})["pin_view"] == "1212"


def test_sign_in_error_shows_the_email_typed(page):
    email = signup(page)
    page.context.clear_cookies()
    page.goto("/login")
    page.fill("#email", email.replace("@", "x@"))
    page.fill("#password", PASSWORD)
    page.click("form[action='/login'] button[type=submit]")
    box = page.inner_text("[data-testid=check-email]")
    assert "Check the email address too" in box and email.replace("@", "x@") in box


def test_child_idle_lock_is_ten_minutes():
    assert deps.CHILD_IDLE == datetime.timedelta(minutes=10)


def test_birthday_suggests_the_school_year(page):
    signup(page)
    page.goto("/children/new")
    page.click("[data-testid=born-helper] summary")
    today = datetime.date.today()
    start = today.year if today.month >= 9 else today.year - 1
    page.select_option("[data-testid=born-month]", "10")                    # October: the youngest is born in August
    page.select_option("[data-testid=born-year]", str(start - 7))           # 6 on 1 September: Year 2
    assert "Year 2" in page.inner_text("[data-testid=born-says]") and page.input_value("#year") == "2"


def test_an_answer_survives_leaving_the_page_offline(browser):
    ctx = browser.new_context(base_url=BASE, **PHONE)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Ryan", 9, targets={"spelling": 3})
    enter_child(pg, "Ryan")
    pg.goto("/me/spelling")
    doc = wait_question(pg, "spelling", pid)
    pg.fill("#answer", doc["answer"])
    ctx.set_offline(True)
    pg.click("#check")
    pg.wait_for_selector("[data-testid=net-msg]:visible")
    pg.close()                                                       # the child gives up and closes the page
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": "spelling"}) == 0
    ctx.set_offline(False)
    pg2 = ctx.new_page()
    pg2.goto("/me")                                                  # any page sends the kept answer
    for _ in range(50):
        if DB.attempts.count_documents({"pupil_id": pid, "activity": "spelling"}):
            break
        pg2.wait_for_timeout(100)
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": "spelling", "correct": True}) == 1
    pg2.wait_for_function("localStorage.getItem('qz_pending') === null")        # dropped once the server has it
    ctx.close()


def test_read_aloud_says_every_sign_before_a_blank(page):
    signup(page)
    add_child(page, "Oscar", 1, year_defaults=True)
    enter_child(page, "Oscar")
    page.goto("/me/maths")
    page.wait_for_function("!!(window.Speak && window.Speak.natural)")
    said = page.evaluate("""() => ['10 − ___ = 6', '___ − 4 = 6', '3 × ___ = 12', '12 ÷ ___ = 3', '___ + 3 = 10',
                                    '___ < 5', '7 > ___', '10 - ___ = 2'].map(Speak.natural)""")
    assert said == ["10 minus blank equals 6", "blank minus 4 equals 6", "3 times blank equals 12",
                    "12 divided by blank equals 3", "blank plus 3 equals 10", "blank is less than 5",
                    "7 is greater than blank", "10 minus blank equals 2"]
    # the child sees the skill and a small bar, no scores or counts
    page.wait_for_function("document.body.dataset.qtoken")
    head = page.inner_text("#stage")
    assert "Skill score" not in head and "skills mastered" not in head and page.is_visible("#mastery")


def _gen(key, want, d=1, tries=400):
    fn = maths_engine.GENERATORS[key]
    for _ in range(tries):
        q = maths_engine.call_generator(fn, d)
        if want in q["prompt"]:
            return q
    raise AssertionError(f"no {want!r} in {key}")


def test_ten_frame_and_shaded_parts_have_a_picture():
    q = _gen("Y1.1.a", "ten frame", 0)
    assert q["component"] == "area_grid" and q["spec"]["dots"] and q["spec"]["rows"] * q["spec"]["cols"] == 10
    assert q["answer"] == 10 - q["spec"]["shaded"]
    q = _gen("Y1.3.a", "Is half shaded", 1)
    assert q["component"] == "area_grid" and q["spec"]["mode"] == "fraction_read"
    assert maths_engine.check_answer(q["answer_type"], q["answer"], q["answer"])
    q = _gen("Y1.3.b", "Is that one quarter", 1)
    assert q["component"] == "area_grid" and q["spec"]["parts"] == 4
    q = _gen("Y2.3.a", "Is one third shaded", 1, 2000)
    assert q["component"] == "area_grid" and q["spec"]["cols"] == q["spec"]["parts"]
    q = _gen("Y2.3.a", "must be shaded to fill it", 1, 2000)
    assert q["component"] == "area_grid" and q["answer"] == q["spec"]["parts"] - q["spec"]["shaded"]


def test_the_same_numbers_in_another_form_are_one_question():
    assert maths_drill._numbers("Which number goes with 7 to make 10? Mark it on the number line.") == \
        maths_drill._numbers("Which number goes with 7 to make 10?") == maths_drill._numbers("10 − ___ = 7")
    assert maths_drill._numbers("How many halves make a whole?") == ()


def test_years_1_to_3_get_at_most_3_of_one_skill_in_a_row(monkeypatch):
    for year in (1, 2, 3):
        _, _, keys = _walk(monkeypatch, year, 0.6, 300, seed=7 + year)
        runs = [len(list(g)) for _, g in itertools.groupby(keys)]
        # a review or a check-back can land on the skill just practised now and then; a block of 4+ never
        assert sum(1 for r in runs if r > 3) <= 2 and max(runs) <= 5, (year, max(runs))
    _, _, keys = _walk(monkeypatch, 4, 0.6, 300, seed=11)
    assert max(len(list(g)) for _, g in itertools.groupby(keys)) >= 4           # older years keep their blocks
