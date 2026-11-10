"""Year 4 check practice (the Multiplication Tables Check), "Something wrong with this question?" reports and the
team's list of them, and the per-device text and display settings ("Aa")."""
import datetime
import secrets
from collections import Counter

import pytest

from conftest import BASE, DB, add_child, enter_child, signup, wait_question

PHONE = {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}


def _kid(browser, year=4, defaults=False, phone=False, name="Sami"):
    ctx = browser.new_context(base_url=BASE, **(PHONE if phone else {}))
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, name, year, year_defaults=defaults)
    enter_child(pg, name)
    return pg, pid


def _api(pg, url, body):
    return pg.evaluate("""([u, b]) => fetch(u, {method: 'POST', headers: {'Content-Type': 'application/json'},
                          body: JSON.stringify(b)}).then(async r => ({status: r.status, ...(await r.json())}))""", [url, body])


def test_mtc_questions_are_shaped_like_the_real_check():
    from app.drills import tables
    seen = Counter()
    for _ in range(300):
        facts = tables.mtc_facts()
        assert len(facts) == 25 and len({(min(a, b), max(a, b)) for a, b in facts}) == 25
        assert all(2 <= a <= 12 and 2 <= b <= 12 for a, b in facts)              # never the 1 times table
        assert sum(1 for a, b in facts if {a, b} & {2, 10}) <= tables.MTC_EASY_MAX
        for a, b in facts:
            seen.update({a, b})
    heavy = sum(seen[t] for t in (6, 7, 8, 9, 12)) / 5
    light = sum(seen[t] for t in (3, 4, 5, 11)) / 4
    assert heavy > 1.5 * light and seen[2] < light and seen[10] < light


def test_year4_check_on_a_phone_with_its_keypad(browser):
    pg, pid = _kid(browser, 4, phone=True)
    pg.goto("/me/tables")
    wait_question(pg, "tables", pid)
    assert "Practise the Year 4 check" in pg.inner_text("[data-testid=mtc-entry]")
    pg.clock.install()
    pg.click("[data-testid=mtc-go]")
    pg.wait_for_url("**/me/tables/year4-check")
    pg.click("[data-testid=mtc-start]")
    pg.wait_for_function("document.body.dataset.mtcq === '0'")
    assert pg.locator("[data-testid=mtc-keypad]").is_visible()
    assert pg.inner_text("[data-testid=mtc-sec]") == "6"
    item = DB.items.find_one({"pupil_id": pid, "activity": "mtc", "done": False})
    answers, prompts = item["answer"], item["meta"]["prompts"]
    for i in range(25):
        pg.wait_for_function("i => document.body.dataset.mtcq === String(i)", arg=str(i))
        assert pg.inner_text("[data-testid=mtc-question]").startswith(prompts[i])
        assert pg.inner_text("[data-testid=mtc-count]") == f"Question {i + 1} of 25"
        if i == 3:                                      # nothing typed: the time runs out
            pg.clock.run_for(6300)
        elif i == 5:                                    # a wrong answer, typed on the keypad
            for d in str(answers[i] + 1):
                pg.click(f"[data-testid=mtc-keypad] button[data-k='{d}']")
            pg.click("[data-testid=mtc-keypad] .ent")
        elif i == 8:                                    # typed but not sent: the time runs out and it counts
            pg.fill("[data-testid=mtc-answer]", str(answers[i]))
            pg.clock.run_for(6300)
        else:
            pg.fill("[data-testid=mtc-answer]", str(answers[i]))
            pg.press("[data-testid=mtc-answer]", "Enter")
        assert pg.evaluate("document.body.dataset.mtcq") == ""      # no right or wrong shown in between
        assert pg.locator("[data-testid=mtc-done]").is_hidden()
        if i < 24:
            pg.clock.run_for(3100)                      # the pause before the next question
    pg.wait_for_selector("[data-testid=mtc-done]")
    assert pg.inner_text("[data-testid=mtc-score]").startswith("23")
    missed = pg.inner_text("[data-testid=mtc-missed]")
    assert prompts[3] in missed and "no answer in time" in missed and prompts[5] in missed
    assert "count towards today" in pg.inner_text("[data-testid=mtc-counted]")
    assert pg.locator("[data-testid=mtc-fix]").is_visible()
    assert pg.evaluate("document.documentElement.scrollWidth") <= 390
    # each check counts as its right answers; the misses are mistakes to put right and weigh more in practice
    day = list(DB.attempts.find({"pupil_id": pid, "activity": "tables"}))
    assert sum(a["correct"] for a in day) == 23 and len(day) == 25
    f3 = item["meta"]["facts"][3]
    assert DB.tables_facts.find_one({"_id": f"{pid}:{f3}"})["wrong"] == 1
    assert DB.pupils.find_one({"_id": pid})["mtc"][-1]["score"] == 23
    pg.goto("/me")
    assert pg.inner_text("[data-testid=tile-tables]").startswith("Times tables") and "20 of 20" in pg.inner_text("[data-testid=tile-tables]")
    assert pg.locator("[data-testid=fix-tables]").count() == 1       # the missed facts wait to be put right
    pg.goto("/me/tables")
    assert "Year 4 check practice: 23 /25" in pg.inner_text("[data-testid=mtc-last]")
    pg.context.close()


def test_year4_check_without_tables_in_the_plan_does_not_count(browser):
    pg, pid = _kid(browser, 7, defaults=True)          # Year 7's day has no times tables
    assert pg.locator("[data-testid=tile-tables]").count() == 0
    assert pg.goto("/me/tables/year4-check").status == 200
    r = _api(pg, "/api/mtc/start", {})
    assert r["ok"] and len(r["questions"]) == 25 and "×" in r["questions"][0] and "answer" not in r
    item = DB.items.find_one({"_id": r["token"]})
    ans = [{"value": str(v), "ms": 2000} for v in item["answer"][:20]]    # 20 right, 5 left blank
    res = _api(pg, "/api/mtc/finish", {"token": r["token"], "answers": ans})
    assert res["ok"] and res["score"] == 20 and len(res["missed"]) == 5 and res["counted"] is False and res["day"] is None
    assert DB.attempts.count_documents({"pupil_id": pid}) == 0
    assert DB.tables_facts.count_documents({"pupil_id": pid}) == 25
    assert _api(pg, "/api/mtc/finish", {"token": r["token"], "answers": ans})["status"] == 409    # marked once only
    pg.context.close()


def test_report_a_question_and_the_team_list(browser):
    DB.reports.delete_many({})
    pg, pid = _kid(browser, 4, phone=True)
    pg.goto("/me/tables")
    doc = wait_question(pg, "tables", pid)
    link = pg.locator("[data-testid=report-open]")
    assert link.inner_text() == "Something wrong with this question?"
    pg.fill("#answer", str(int(doc["answer"]) + 1))
    pg.click("#check")
    pg.wait_for_selector("#feedback.no")
    link.click()
    pg.click("[data-reason=wrong]")
    pg.fill("#reportNote", "I think my answer was right")
    pg.press("#reportNote", "Enter")                    # typing a note never answers or skips the question
    assert pg.evaluate("document.body.dataset.qtoken") == doc["_id"]
    pg.click("[data-testid=report-send]")
    pg.wait_for_function("document.getElementById('reportMsg').textContent === 'Thanks! A grown-up will check it.'")
    r = DB.reports.find_one({"pupil_id": pid})
    assert r["served"]["prompt"] == doc["meta"]["prompt"] and r["expected"] == doc["answer"]
    assert r["answer"] == str(int(doc["answer"]) + 1) and r["reason"] == "wrong" and r["year"] == 4
    assert r["activity"] == "tables" and r["skill"] == doc["meta"]["fact"] and r["device"]["w"] == 390 and r["status"] == "open"
    # the next question has its own link again
    pg.click("#next")
    wait_question(pg, "tables", pid, doc["_id"])
    assert link.is_visible() and pg.inner_text("[data-testid=report-msg]") == ""
    # another family's token gets nothing of that question
    other, _ = _kid(browser, 4, name="Lina")
    res = _api(other, "/api/report", {"activity": "tables", "token": doc["_id"], "reason": "other"})
    assert res["ok"] and DB.reports.find_one({"family_id": {"$ne": r["family_id"]}})["served"] is None
    # ten a day per child
    for _ in range(9):
        assert _api(pg, "/api/report", {"activity": "tables", "reason": "other"})["ok"]
    assert _api(pg, "/api/report", {"activity": "tables", "reason": "other"})["status"] == 429
    assert _api(pg, "/api/report", {"activity": "tables", "reason": "bogus"})["status"] == 400
    # families never see reports: not on the parent's pages
    other.goto("/me")
    assert "Something wrong" not in other.inner_text("main")
    other.context.close()
    # the team board: a count on its home, the list newest first, and a status
    slug = "".join(secrets.choice("abcdefghjkmnpqrstuvwxyz23456789") for _ in range(10))
    DB.team_members.insert_one({"_id": slug, "name": "Meriem", "initials": "Me", "role": "member", "telegram_chat_id": None,
                                "active": True, "created": datetime.datetime.utcnow()})
    pg.goto(f"/team/{slug}")
    assert pg.inner_text("[data-testid=reports-open]") == "11 open"
    pg.click("[data-testid=reports-link]")
    cards = pg.locator("[data-testid=report]")
    assert cards.count() == 11
    first = DB.reports.find_one({}, sort=[("ts", 1)])
    last = cards.nth(10)
    assert "The answer is wrong" in last.inner_text() and "I think my answer was right" in last.inner_text()
    last.locator("[data-testid=set-fixed]").click()
    pg.wait_for_url("**/reports?status=open*")
    assert pg.locator("[data-testid=report]").count() == 10
    assert DB.reports.find_one({"_id": first["_id"]})["status"] == "fixed"
    assert pg.goto("/team/notAmember1/reports").status == 404
    pg.context.close()


@pytest.mark.parametrize("phone", [True, False])
def test_text_and_display_settings(browser, phone):
    pg, pid = _kid(browser, 2, phone=phone)
    width = 390 if phone else 1280
    pg.click("[data-testid=a11y-open]")
    for k in ("big", "dys", "space", "calm", "contrast"):
        pg.check(f"[data-testid=a11y-{k}]")
        assert pg.evaluate("k => document.documentElement.classList.contains('a11y-' + k)", k)
    pg.click("#a11yDone")
    for path in ("/me", "/me/maths", "/me/spelling", "/me/tables", "/me/tables/year4-check"):
        pg.goto(path)
        assert pg.evaluate("document.documentElement.className").count("a11y-") == 5      # kept on this device
        assert pg.evaluate("document.documentElement.scrollWidth") <= width, path
    font = pg.evaluate("getComputedStyle(document.body).fontFamily")
    assert font.startswith("Verdana") and not pg.evaluate("[...document.styleSheets].some(s => s.href && /font.*(dyslex|open)/i.test(s.href))")
    pg.goto("/me/maths")
    wait_question(pg, "maths", pid)
    assert pg.evaluate("getComputedStyle(document.querySelector('.rise')).animationName") == "none"
    # read-aloud stays for Years 1-2
    assert pg.locator("[data-testid=speak]").count() == 1
    pg.click("[data-testid=a11y-open]")
    pg.uncheck("[data-testid=a11y-big]")
    pg.reload()
    assert "a11y-big" not in pg.evaluate("document.documentElement.className")
    pg.context.close()


def test_settings_page_works_without_storage_and_honours_reduced_motion(browser):
    ctx = browser.new_context(base_url=BASE, reduced_motion="reduce", **PHONE)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    add_child(pg, "Ada", 3)
    enter_child(pg, "Ada")
    pg.add_init_script("Object.defineProperty(window, 'localStorage', {get() { throw new Error('blocked'); }});")
    pg.goto("/me")
    pg.click("[data-testid=a11y-open]")
    calm = pg.locator("[data-testid=a11y-calm]")
    assert calm.is_checked() and calm.is_disabled()
    pg.check("[data-testid=a11y-big]")
    assert "a11y-big" in pg.evaluate("document.documentElement.className")
    assert pg.evaluate("document.documentElement.scrollWidth") <= 390
    ctx.close()
