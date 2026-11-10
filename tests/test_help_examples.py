"""Help that matches the app, the quiet discovery line on Home, the landing page's features, example questions for
a parent (read-only, nothing recorded), and grammar extra practice that takes the strands in turn."""
import re

import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup


def _search(page, words):
    page.fill("[data-testid=help-search]", words)
    return [s.get_attribute("id") for s in page.locator(".help-q").all() if s.is_visible()]


def test_help_search_finds_what_parents_type(page):
    page.goto("/help")
    for words, section in [("dyslexia", "reading"), ("font", "reading"), ("bigger", "reading"), ("text size", "reading"),
                           ("reading", "reading"), ("reading", "read-aloud"), ("sick", "days-off"),
                           ("holiday", "days-off"), ("day off", "days-off"), ("spelling list", "school-list"),
                           ("SATs", "sats"), ("test", "sats"), ("KS2", "sats"), ("test", "year4-check"),
                           ("carer", "adults"), ("grandparent", "adults"), ("partner", "adults"),
                           ("own phone", "own-phone"), ("weekly email", "weekly"), ("wrong question", "question-reports"),
                           ("homophone", "school-list")]:
        shown = _search(page, words)
        assert section in shown, (words, shown)
        assert page.locator("[data-testid=help-none]").is_hidden()
    assert "days-off" not in _search(page, "SATs")                # not "Saturday"
    assert _search(page, "zzqx") == [] and page.locator("[data-testid=help-none]").is_visible()


def test_help_says_where_a_carer_sees_pins_and_how_put_right_works(page):
    page.goto("/help")
    pins = page.text_content("#pins")                                # the details are folded under "More"
    assert "can't" not in pins.split("Showing:")[1].split("Locked:")[0], pins       # no more "a carer can't"
    assert "Children's PINs" in pins and "carer" in pins
    back = page.text_content("#comes-back")
    assert "that same question" in back and "a question like this was right later" in back
    assert "Test review" in page.text_content("#sats") and "Make carer" in page.text_content("#adults")


def test_landing_mentions_the_family_features(page):
    page.goto("/")
    body = page.inner_text("body")
    for bit in ("spelling list", "Year 4 times tables check", "carer", "dyslexia"):
        assert bit in body, bit


def test_home_line_leads_to_the_spelling_list_and_days_off(page):
    signup(page)
    pid = add_child(page, "Ella", 2, year_defaults=True)
    page.goto("/home")
    line = page.get_by_test_id("home-discover")
    assert "Got a spelling list from school?" in line.inner_text() and "Day off?" in line.inner_text()
    assert page.get_by_test_id("discover-list").get_attribute("href") == f"/children/{pid}/edit#school-list"
    page.get_by_test_id("discover-off").click()
    page.wait_for_url(f"**/children/{pid}/edit#days-off")
    assert page.locator("#days-off").is_visible()
    # once a list is running, only the day off is offered
    page.fill("[data-testid=school-words]", "said, have, like")
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(r".*saved=1.*"))
    page.goto("/home")
    assert "spelling list" not in page.get_by_test_id("home-discover").inner_text()


def test_example_questions_are_read_only_and_for_grown_ups(browser):
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    pid = add_child(pg, "Nour", 7)
    before = (DB.maths_lab_q.count_documents({"pupil": pid}), DB.items.count_documents({"pupil_id": pid}),
              DB.attempts.count_documents({"pupil_id": pid}))
    pg.goto(f"/children/{pid}")
    links = pg.locator("[data-testid=skills-maths] [data-testid=examples-link]")
    assert links.count() >= 5
    pg.locator("[data-testid=skills-maths] details").first.locator("summary").click()
    links.first.click()
    pg.wait_for_url(re.compile(rf".*/children/{pid}/examples\?subject=maths&strand=.*"))
    n = pg.locator("[data-testid=example]").count()
    assert 3 <= n <= 5, n
    assert all(a.inner_text().strip() for a in pg.locator("[data-testid=example-answer]").all())
    assert "nothing here is recorded" in pg.inner_text("[data-testid=examples-note]")
    for subj in ("grammar", "science"):
        pg.goto(f"/children/{pid}")
        link = pg.locator(f"[data-testid=skills-{subj}] [data-testid=examples-link]").first
        pg.goto(BASE + link.get_attribute("href"))
        assert 3 <= pg.locator("[data-testid=example]").count() <= 5
        pg.get_by_test_id("examples-more").click()
        assert 3 <= pg.locator("[data-testid=example]").count() <= 5
    after = (DB.maths_lab_q.count_documents({"pupil": pid}), DB.items.count_documents({"pupil_id": pid}),
             DB.attempts.count_documents({"pupil_id": pid}))
    assert after == before, (before, after)                    # nothing served, nothing recorded
    assert requests.get(BASE + f"/children/{pid}/examples?subject=maths&strand=nope",
                        cookies={c["name"]: c["value"] for c in pg.context.cookies()}).status_code == 404
    # a child signed in on the device can't open it
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Nour")
    kid.goto(f"/children/{pid}/examples?subject=maths&strand=7.0%20Sequences")
    assert "/examples" not in kid.url and kid.locator("[data-testid=example]").count() == 0
    kid.context.close()
    pg.context.close()


def _right(key):
    return {"mcq": lambda: key["right"], "tap": lambda: key["hits"], "text": lambda: key["a"][0],
            "write": lambda: key["a"][0], "num": lambda: key["a"]}[key["t"]]()


def test_grammar_after_the_target_takes_the_strands_in_turn(browser):
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    add_child(pg, "Yusuf", 7, targets={"grammar": 3})
    kid = browser.new_context(base_url=BASE).new_page()
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, "Yusuf")
    s = requests.Session()
    for c in kid.context.cookies():
        s.cookies.set(c["name"], c["value"])
    strands = []
    for i in range(12):
        q = s.post(BASE + "/api/grammar/next", json={}).json()
        assert q["ok"], q
        strands.append(q["strand"])
        it = DB.items.find_one({"_id": q["token"]})
        r = s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": _right(it["answer"])}).json()
        assert r["correct"], r
    assert not any(len(set(strands[i:i + 4])) == 1 for i in range(len(strands) - 3)), strands  # never 4 in a row
    assert len(set(strands[3:])) >= 3, strands             # after it: the year's strands in turn
    kid.context.close()
    pg.context.close()


def test_help_gives_a_short_answer_first_and_search_finds_the_new_answers(page):
    page.goto("/help")
    for s in page.locator(".help-q").all():                     # one short plain sentence first, the details folded
        first = s.locator("h2 + *")
        assert "help-short" in (first.get_attribute("class") or ""), s.get_attribute("id")
        assert first.is_visible() and len(first.inner_text()) < 200, (s.get_attribute("id"), first.inner_text())
        more = s.locator("details.help-more")
        assert more.count() == 0 or more.get_attribute("open") is None, s.get_attribute("id")
    assert page.inner_text("#cost .help-short") == ("It is free during the beta. Before any paid plan starts, we will "
                                                     "email you, and you can keep or delete your account.")
    for words, section in [("price", "cost"), ("pay", "cost"), ("streak", "streak"), ("modal", "modal"),
                           ("wrong word", "wrong-word"), ("frend", "wrong-word"), ("SATs papers", "sats-papers"),
                           ("weak", "needs-help"), ("progress", "needs-help")]:
        shown = _search(page, words)
        assert shown and shown[0] == section, (words, shown)     # the best answer comes first
    # a word only in the details: the short answer stays, with the sentence the word is in
    _search(page, "asdf")
    hit = page.locator("#first-time [data-testid=help-hit]")
    assert hit.is_visible() and "asdf" in hit.inner_text() and page.locator("#first-time .help-short").is_visible()
    assert page.locator("#first-time details.help-more").get_attribute("open") is None
    page.fill("[data-testid=help-search]", "")
    ids = [s.get_attribute("id") for s in page.locator(".help-q").all()]
    assert ids[:3] == ["day-plan", "needs-help", "mastered"]     # the page order is back
    # a link to one answer opens its details
    page.goto("/help#pins")
    assert page.locator("#pins details.help-more").get_attribute("open") is not None
    assert page.locator("#pins").get_by_text("Children's PINs").is_visible()
