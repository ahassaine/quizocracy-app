"""Grammar and punctuation, and science, end to end: each year serves its own bank, answers are marked on the
server, every question type works on the page, the parent sees progress, and deleting a child deletes it all."""
import pytest
import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup, unlock_parent, wait_question


def _kid_session(browser, year, name="Ines"):
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    pid = add_child(pg, name, year)
    ctx = browser.new_context(base_url=BASE)
    kid = ctx.new_page()
    kid.set_default_timeout(15000)
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, name)
    s = requests.Session()
    for c in ctx.cookies():
        s.cookies.set(c["name"], c["value"])
    return pg, kid, s, pid


def right_value(key):
    return {"mcq": lambda: key["right"], "tap": lambda: key["hits"], "text": lambda: key["a"][0],
            "write": lambda: key["a"][0], "num": lambda: key["a"]}[key["t"]]()


@pytest.mark.parametrize("year", range(1, 10))
def test_each_year_serves_and_marks_its_own_bank(browser, year):
    pg, kid, s, pid = _kid_session(browser, year)
    for sub, pre in (("grammar", "GP"), ("science", "SC")):
        q = s.post(BASE + f"/api/{sub}/next", json={}).json()
        assert q["ok"] and q["prompt"] and q["kind"] in ("mcq", "tap", "text", "write", "num"), q
        assert not {"a", "answer", "right", "hits", "why"} & set(q), q          # nothing gives the answer away
        it = DB.items.find_one({"_id": q["token"]})
        assert it["meta"]["skill"].startswith(f"{pre}{year}."), it["meta"]
        r = s.post(BASE + f"/api/{sub}/check", json={"token": q["token"], "value": right_value(it["answer"])}).json()
        assert r["correct"] is True, (q, r)
        assert s.post(BASE + f"/api/{sub}/check", json={"token": q["token"], "value": "x"}).status_code == 409  # once only
        q = s.post(BASE + f"/api/{sub}/next", json={}).json()
        r = s.post(BASE + f"/api/{sub}/check", json={"token": q["token"], "value": "zzqx-not-it"}).json()
        assert r["correct"] is False and r["expected"] and r["why"], r
        assert DB.bank_mastery.find_one({"pupil_id": pid, "subject": sub, "score": {"$gt": 0}})
        wrong = DB.attempts.find_one({"pupil_id": pid, "activity": sub, "correct": False})
        assert wrong and wrong.get("q") and wrong.get("exp"), wrong                 # shows under mistakes
    kid.context.close()
    pg.context.close()


def test_every_question_type_works_on_the_page(browser):
    pg, kid, s, pid = _kid_session(browser, 6)
    kinds, prev = set(), None
    for sub in ("grammar", "science"):
        kid.goto(f"/me/{sub}")
        prev = None
        for _ in range(14):
            doc = wait_question(kid, sub, pid, prev)
            prev = doc["_id"]
            key = doc["answer"]
            kinds.add(key["t"])
            if key["t"] == "mcq":
                kid.click(f"[data-testid=opt-{key['right']}]")
            elif key["t"] == "tap":
                for i in key["hits"]:
                    kid.click(f"[data-testid=word-{i}]")
            else:
                kid.fill("#answer", str(right_value(key)))
            kid.click("#check")
            kid.wait_for_selector("#feedback.yes, #feedback.no")
            assert "Correct" in kid.inner_text("#feedback"), (sub, key, kid.inner_text("#feedback"))
            kid.click("#next")
    assert {"mcq", "tap"} <= kinds and kinds & {"text", "write", "num"}, kinds
    # a wrong answer shows the right one and why
    doc = wait_question(kid, "science", pid, prev)
    key = doc["answer"]
    if key["t"] == "mcq":
        kid.click(f"[data-testid=opt-{(key['right'] + 1) % len(key['opts'])}]")
    elif key["t"] == "tap":
        kid.click("[data-testid=word-%d]" % next(i for i in range(len(key["words"])) if i not in key["hits"]))
    else:
        kid.fill("#answer", "zzqx")
    kid.click("#check")
    kid.wait_for_selector("#feedback.no")
    assert "The answer is" in kid.inner_text("#feedback")
    assert kid.locator("#feedback .why").inner_text().strip()

    unlock_parent(kid)
    kid.goto(f"/children/{pid}")
    for sub in ("grammar", "science"):
        card = kid.inner_text(f"[data-testid=card-{sub}]")
        assert "of " in card and "Year 6 skills" in card and "started" in card, card
    assert "to go over" in kid.inner_text("[data-testid=mistakes-day]")
    kid.context.close()
    pg.context.close()


def test_deleting_a_child_deletes_their_grammar_and_science(browser):
    pg, kid, s, pid = _kid_session(browser, 4)
    for sub in ("grammar", "science"):
        q = s.post(BASE + f"/api/{sub}/next", json={}).json()
        s.post(BASE + f"/api/{sub}/check", json={"token": q["token"], "value": "zzqx"})
    assert DB.bank_mastery.count_documents({"pupil_id": pid}) and DB.bank_state.count_documents({"pupil_id": pid})
    exp = pg.request.get("/account/export").json()
    assert any(d.get("subject") == "science" for d in exp["bank_mastery"])
    pg.goto(f"/children/{pid}/delete")                  # its own page, with the deleter's password
    pg.fill("[data-testid=delete-password]", PASSWORD)
    pg.click("[data-testid=delete-confirm]")
    pg.wait_for_url("**/home?deleted=1*")
    assert not DB.bank_mastery.count_documents({"pupil_id": pid}) and not DB.bank_state.count_documents({"pupil_id": pid})
    kid.context.close()
    pg.context.close()
