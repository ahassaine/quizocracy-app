"""Fixes from the first QA round with real-family journeys (Nov 2026): a reward offered to a new family, the
Board saying why the child is signed out (test_calm_screen), capitals in spelling, Year 2 words first, a short
"mistakes come back" line for the young, and a place-value chart that fits a phone."""
import pytest

from conftest import BASE, DB, add_child, signup
from test_put_right import _check, _kid, _next

pytestmark = pytest.mark.skipif(BASE.startswith("https://"), reason="reads served answers from the database")


def test_a_new_family_is_offered_a_reward(page):
    signup(page)
    page.goto("/home")
    assert page.get_by_test_id("reward-choose").count() == 0              # no child yet: nothing to reward
    add_child(page, "Nia", 3)
    page.goto("/home")
    card = page.get_by_test_id("reward-choose")
    assert "Choose a reward for a finished day" in card.inner_text()
    page.get_by_test_id("reward-choose-text").fill("A story at bedtime")
    page.get_by_test_id("reward-choose-save").click()
    page.wait_for_url("**/home?family_reward=1")
    assert page.get_by_test_id("reward-choose").count() == 0
    fid = DB.pupils.find_one({"name": "Nia"}, sort=[("created", -1)])["family_id"]
    assert DB.families.find_one({"_id": fid})["reward"]["text"] == "A story at bedtime"


def _word(s, pid, word):
    """The next spelling question, made to ask `word`."""
    q = _next(s, "spelling")
    DB.items.update_one({"_id": q["token"]}, {"$set": {"answer": word}})
    return q["token"]


def test_a_capital_is_part_of_spelling_it(page):
    pid, s = _kid(page, 2, acts=("spelling",))
    t = _word(s, pid, "I")
    r = _check(s, "spelling", t, "i")                       # the letters right, not the capital: a hint, one more go
    assert r["retry"] and r["capital"] and "capital letter" in r["hint"] and not r["correct"], r
    r = _check(s, "spelling", t, "I")
    assert r["correct"], r
    t = _word(s, pid, "I")
    assert _check(s, "spelling", t, "i")["retry"]
    assert _check(s, "spelling", t, "i")["correct"] is False             # twice: a miss like any other
    t = _word(s, pid, "said")                                             # a lower-case word: any case is fine
    assert _check(s, "spelling", t, "Said")["correct"]


def test_year2_spelling_starts_with_year2_words():
    from app.drills import spelling as sp
    y2 = sp.list_for_year(2)
    assert y2[:3] == sp.LISTS["Y2"][:3] and "door" in y2[:5]
    assert set(sp.LISTS["Y1"]) <= set(y2) and len(y2) == len(set(y2))     # Year 1 words still there, as revision


def test_place_value_chart_fits_a_phone(browser):
    """Read the number in a 6-column place-value chart on a 390 px phone: short headings (HTh … O) and a key."""
    ctx = browser.new_context(base_url=BASE, viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.goto("/static/offline.html")                                       # any page of ours, for the scripts' origin
    pg.set_content("""<html><head><meta name="viewport" content="width=device-width"></head><body style="margin:0;padding:16px">
      <div id="h" style="width:100%"></div><script src="/static/maths/components/data_table.js"></script></body></html>""")
    pg.add_script_tag(url=BASE + "/static/maths/components/data_table.js")
    pg.evaluate("""() => MComp.data_table.render(document.getElementById('h'),
        {headers: ['Hundred Thousands','Ten Thousands','Thousands','Hundreds','Tens','Ones'], rows: [['6','5','7','9','3','1']]}, {submit(){}})""")
    heads = pg.eval_on_selector_all("#h th", "els => els.map(e => e.textContent)")
    assert heads == ["HTh", "TTh", "Th", "H", "T", "O"], heads
    assert "HTh hundred thousands" in pg.inner_text("[data-testid=pv-key]")
    assert pg.evaluate("document.documentElement.scrollWidth") <= 390
    ctx.close()
