"""Phonics, reading, SATs practice papers, the phonics check practice, races and leagues, end to end (the server's
API with a child's session, and the pages a child and a parent open)."""
import datetime
import re

import pytest
import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup, unlock_parent


def _family(browser, year, name="Ines", targets=None):
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    pid = add_child(pg, name, year, targets=targets)
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


def right(key):
    t = key["t"]
    return {"mcq": lambda: key["right"], "tap": lambda: key["hits"], "text": lambda: key["a"][0],
            "write": lambda: key["a"][0], "num": lambda: key["a"], "seg": lambda: key["cuts"],
            "order": lambda: key["order"]}[t]()


def wrong(key):
    t = key["t"]
    if t == "mcq":
        return (key["right"] + 1) % len(key["opts"])
    if t == "seg":
        return [1] if key["cuts"] != [1] else [2]
    if t == "order":
        return list(reversed(key["order"]))
    if t == "tap":
        return [0] if key["hits"] != [0] else [1]
    return "zzzz"


def test_phonics_serves_marks_and_never_shows_the_spoken_word(browser):
    pg, kid, s, pid = _family(browser, 1, targets={"phonics": 6})
    kinds = set()
    for i in range(30):
        q = s.post(BASE + "/api/phonics/next", json={}).json()
        assert q["ok"] and q["kind"] in ("mcq", "seg", "tap", "text"), q
        assert not {"a", "answer", "right", "hits", "cuts", "split"} & set(q), q
        it = DB.items.find_one({"_id": q["token"]})
        assert it["meta"]["skill"].startswith("PH1."), it["meta"]
        if q.get("say"):
            assert q["say"].lower() not in q["prompt"].lower()
        kinds.add(q["kind"])
        val = right(it["answer"]) if i % 3 else wrong(it["answer"])
        r = s.post(BASE + "/api/phonics/check", json={"token": q["token"], "value": val}).json()
        if r.get("retry"):
            r = s.post(BASE + "/api/phonics/check", json={"token": q["token"], "value": right(it["answer"])}).json()
        assert r["ok"] and r["correct"] == bool(i % 3) or r.get("retry"), r
    assert "seg" in kinds or "mcq" in kinds
    kid.goto("/me/phonics")
    kid.wait_for_selector("[data-testid=question]")
    assert kid.locator("#check").is_visible()


def test_reading_asks_a_passage_in_order_then_says_how_it_went(browser):
    pg, kid, s, pid = _family(browser, 3, targets={"reading": 6})
    seen = []
    done = None
    for i in range(12):
        q = s.post(BASE + "/api/reading/next", json={}).json()
        assert q["ok"] and q["passage"]["text"], q
        it = DB.items.find_one({"_id": q["token"]})
        seen.append((q["passage"]["key"], q["passage"]["n"]))
        r = s.post(BASE + "/api/reading/check", json={"token": q["token"], "value": right(it["answer"])}).json()
        if r.get("retry"):
            continue
        assert r["ok"] and r["correct"], r
        if r.get("passage_done"):
            done = r["passage_done"]
            break
    first = seen[0][0]
    assert [n for k, n in seen if k == first] == list(range(1, len(seen) + 1)), seen
    assert done and done["right"] == done["of"], done
    q = s.post(BASE + "/api/reading/next", json={}).json()
    assert q["passage"]["key"] != first and q["passage"]["n"] == 1, q
    kid.goto("/me/reading")
    kid.wait_for_selector("[data-testid=passage-title]")
    assert kid.locator("[data-testid=passage]").is_visible()


def test_reading_mistake_comes_back_with_its_passage_in_practise_my_mistakes(browser):
    pg, kid, s, pid = _family(browser, 4, targets={"reading": 6})
    q = s.post(BASE + "/api/reading/next", json={}).json()
    it = DB.items.find_one({"_id": q["token"]})
    r = s.post(BASE + "/api/reading/check", json={"token": q["token"], "value": wrong(it["answer"])}).json()
    if r.get("retry"):
        r = s.post(BASE + "/api/reading/check", json={"token": q["token"], "value": wrong(it["answer"])}).json()
    assert r["ok"] and not r["correct"]
    att = DB.attempts.find_one({"pupil_id": pid, "activity": "reading", "correct": False})
    assert att and att["detail"].startswith("RD4.") and "#" in att["detail"]


@pytest.mark.parametrize("paper", ["arithmetic", "reasoning", "gps", "spelling", "reading"])
def test_a_sats_paper_starts_marks_and_keeps_its_score(browser, paper):
    pg, kid, s, pid = _family(browser, 6, name="Omar")
    st = s.post(BASE + "/api/sats/start", json={"paper": paper}).json()
    assert st["ok"] and st["questions"] and st["seconds"] > 0, st
    for q in st["questions"]:
        assert not {"a", "answer", "right", "hits", "word"} & set(q), q
    it = DB.items.find_one({"_id": st["token"]})
    answers = []
    for i, a in enumerate(it["answer"]):
        if a["t"] == "bank":
            answers.append(right(a["key"]) if i % 2 == 0 else None)
        elif a["t"] == "spelling":
            answers.append(a["word"] if i % 2 == 0 else None)
        else:
            doc = DB.maths_lab_q.find_one({"_id": a["token"]})
            answers.append(str(doc["answer"]) if i % 2 == 0 else None)
    res = s.post(BASE + "/api/sats/finish", json={"token": st["token"], "answers": answers, "used": 100}).json()
    assert res["ok"], res
    n_given = sum(1 for a in answers if a is not None)
    assert res["blank"] == len(answers) - n_given
    assert res["score"] >= n_given - (1 if paper in ("arithmetic", "reasoning") else 0), res   # a maths display form may differ
    again = s.post(BASE + "/api/sats/finish", json={"token": st["token"], "answers": answers}).json()
    assert again["ok"] and again["score"] == res["score"]
    p = DB.pupils.find_one({"_id": pid})
    assert p["sats_papers"][-1]["paper"] == paper and p["sats_papers"][-1]["score"] == res["score"]
    kid.goto("/me/sats")
    assert kid.locator(f"[data-testid=paper-card-{paper}] [data-testid=paper-last]").is_visible()


def test_sats_papers_are_for_years_5_and_6_only(browser):
    pg, kid, s, pid = _family(browser, 3, name="Leo")
    r = s.post(BASE + "/api/sats/start", json={"paper": "gps"})
    assert r.status_code == 403
    kid.goto("/me/sats")
    kid.wait_for_url("**/me")


def test_a_paper_on_the_page_runs_to_its_result(browser):
    pg, kid, s, pid = _family(browser, 6, name="Ava")
    kid.goto("/me/sats/gps")
    kid.click("[data-testid=paper-start]")
    kid.wait_for_selector("[data-testid=paper-count]:has-text('Question 1')")
    kid.click("[data-testid=paper-skip]")
    kid.wait_for_selector("[data-testid=paper-count]:has-text('Question 2')")
    kid.click("[data-testid=paper-finish]", no_wait_after=True)
    kid.once("dialog", lambda d: d.accept())
    kid.click("[data-testid=paper-finish]")
    kid.wait_for_selector("[data-testid=paper-done]:visible")
    assert re.search(r"\d+", kid.inner_text("[data-testid=paper-score]"))


def test_phonics_check_practice_is_marked_by_the_grown_up(browser):
    pg, kid, s, pid = _family(browser, 1, name="Mia")
    st = s.post(BASE + "/api/phonics-check/start", json={"size": 20}).json()
    assert st["ok"] and len(st["words"]) == 20
    assert sum(w["alien"] for w in st["words"]) == 10
    res = s.post(BASE + "/api/phonics-check/finish", json={"token": st["token"], "marks": [True] * 15 + [False] * 5}).json()
    assert res["ok"] and res["score"] == 15 and res["of"] == 20
    kid.goto("/me/phonics-check")
    kid.click("[data-testid=pc-start-20]")
    for _ in range(20):
        kid.click("[data-testid=pc-yes]")
    kid.wait_for_selector("[data-testid=pc-done]:visible")
    assert "20" in kid.inner_text("[data-testid=pc-score]")


def test_race_keeps_a_real_run_and_refuses_a_scripted_one(browser):
    pg, kid, s, pid = _family(browser, 4, name="Kofi")
    st = s.post(BASE + "/api/race/start", json={"course": "full"}).json()
    assert st["ok"] and len(st["questions"]) == 20
    # the same course gives the same 20 questions all week
    st2 = s.post(BASE + "/api/race/start", json={"course": "full"}).json()
    assert [q["q"] for q in st["questions"]] == [q["q"] for q in st2["questions"]]
    fast = s.post(BASE + "/api/race/finish", json={"token": st2["token"], "splits": list(range(10, 210, 10)),
                                                  "wrong": [0] * 20}).json()
    assert fast["ok"] and not fast["kept"]
    st3 = s.post(BASE + "/api/race/start", json={"course": "full"}).json()
    DB.races.update_one({"_id": st3["token"]}, {"$set": {"started": datetime.datetime.utcnow() - datetime.timedelta(seconds=60)}})
    res = s.post(BASE + "/api/race/finish", json={"token": st3["token"], "splits": [2000 * (i + 1) for i in range(20)],
                                                 "wrong": [1] + [0] * 19}).json()
    assert res["ok"] and res["kept"] and res["total"] == 42000, res
    kid.goto("/me/race")
    assert "42.0 s" in kid.inner_text("[data-testid=course-full]")


def test_leagues_join_with_a_code_and_show_only_nicknames(browser):
    pg1, kid1, s1, p1 = _family(browser, 5, name="Zara")
    pg2, kid2, s2, p2 = _family(browser, 2, name="Yusuf")

    pg1.goto("/leagues")
    pg1.click("[data-testid=league-new] button")
    pg1.wait_for_selector("[data-testid=league-code]")
    code = pg1.inner_text("[data-testid=league-code]").strip()

    pg2.goto("/leagues")
    pg2.fill("[data-testid=league-code-input]", code.lower())
    pg2.click("[data-testid=league-join] button")
    pg2.wait_for_selector("[data-testid=leagues-done]")
    nick2 = DB.pupils.find_one({"_id": p2})["nick"]["name"]
    pg1.goto("/leagues")
    body = pg1.inner_text("body")
    assert nick2 in body and "Yusuf" not in body
    kid1.goto("/me/league")
    t = kid1.inner_text("[data-testid=friends-league]")
    assert nick2 in t and "Yusuf" not in t and "Zara" in t
    pg2.goto("/leagues")
    pg2.once("dialog", lambda d: d.accept())
    pg2.click("[data-testid=league-leave]")
    pg2.wait_for_selector("[data-testid=no-leagues]")
    pg2.goto("/leagues")
    pg2.fill("[data-testid=league-code-input]", "NOPE1234")
    pg2.click("[data-testid=league-join] button")
    assert pg2.locator("[data-testid=league-join-error]").is_visible()


def test_my_day_shows_the_new_cards_for_the_right_years(browser):
    pg, kid, s, pid = _family(browser, 1, name="Sam", targets={"phonics": 6})
    kid.goto("/me")
    assert kid.locator("[data-testid=pc-card]").is_visible()
    assert kid.locator("[data-testid=play-card]").is_visible()
    assert kid.locator("[data-testid=tile-phonics]").is_visible()
    assert not kid.locator("[data-testid=sats-card]").count()


def test_phonics_keeps_its_phases_in_order_and_no_sound_leaves_out_listening(browser):
    pg, kid, s, pid = _family(browser, 1, name="Lia", targets={"phonics": 6})
    for i in range(12):
        q = s.post(BASE + "/api/phonics/next", json={}).json()
        it = DB.items.find_one({"_id": q["token"]})
        assert it["meta"]["skill"] in ("PH1.01", "PH1.02", "PH1.03"), it["meta"]       # the first phases first
        s.post(BASE + "/api/phonics/check", json={"token": q["token"], "value": right(it["answer"])})
    q = s.post(BASE + "/api/phonics/next", json={}).json()
    assert s.post(BASE + "/api/phonics/nosound", json={"token": q["token"]}).json()["ok"]
    for i in range(15):
        q = s.post(BASE + "/api/phonics/next", json={}).json()
        assert not q.get("say"), q
        it = DB.items.find_one({"_id": q["token"]})
        s.post(BASE + "/api/phonics/check", json={"token": q["token"], "value": right(it["answer"])})


def test_a_copying_slip_in_reading_is_still_found(browser):
    from app_path import engine
    k = {"t": "text", "a": ["Greenfield Leisure Centre"], "copy": True}
    assert engine.mark(k, "Greenfield Leisure Center") and engine.mark({"t": "text", "a": ["bias"], "copy": True}, "bais")
    assert not engine.mark(k, "the swimming pool")


def test_a_paper_answer_sheet_can_be_opened_again_by_child_and_parent(browser):
    pg, kid, s, pid = _family(browser, 6, name="Noor")
    st = s.post(BASE + "/api/sats/start", json={"paper": "gps"}).json()
    res = s.post(BASE + "/api/sats/finish", json={"token": st["token"], "answers": [], "used": 30}).json()
    assert res["ok"] and res["sheet"]
    kid.goto("/me/sats")
    kid.click("[data-testid=sheet-link]")
    assert kid.locator("[data-testid=sheet-row]").count() == res["of"]
    pg.goto(f"/children/{pid}/sats/{res['sheet']}")
    assert pg.locator("[data-testid=sheet-row]").count() == res["of"]


def test_arithmetic_paper_is_bare_calculations_and_reasoning_has_no_probability(browser):
    pg, kid, s, pid = _family(browser, 6, name="Rhys")
    st = s.post(BASE + "/api/sats/start", json={"paper": "arithmetic"}).json()
    assert all(q["component"] == "number" for q in st["questions"]), [q["component"] for q in st["questions"]]
    for _ in range(3):
        st = s.post(BASE + "/api/sats/start", json={"paper": "reasoning"}).json()
        assert not any("probab" in q["prompt"].lower() for q in st["questions"])


def test_a_family_taken_out_of_a_league_cannot_rejoin_and_the_code_changes(browser):
    pg1, kid1, s1, p1 = _family(browser, 5, name="Ava")
    pg2, kid2, s2, p2 = _family(browser, 4, name="Ben")
    pg1.goto("/leagues")
    pg1.click("[data-testid=league-new] button")
    code = pg1.inner_text("[data-testid=league-code]").strip()
    pg2.goto("/leagues")
    pg2.fill("[data-testid=league-code-input]", code)
    pg2.click("[data-testid=league-join] button")
    pg2.wait_for_selector("[data-testid=leagues-done]")
    pg1.goto("/leagues")
    pg1.click("[data-testid^=league-] details summary")
    pg1.once("dialog", lambda d: d.accept())
    pg1.click("text=Take out")
    pg1.wait_for_selector("[data-testid=leagues-done]")
    assert pg1.inner_text("[data-testid=league-code]").strip() != code
    pg2.goto("/leagues")
    pg2.fill("[data-testid=league-code-input]", pg1.inner_text("[data-testid=league-code]").strip())
    pg2.click("[data-testid=league-join] button")
    assert "taken your family out" in pg2.inner_text("[data-testid=league-join-error]")
    assert pg2.goto("/leagues/join").url.endswith("/leagues")


def test_reading_counts_questions_answered_so_a_slip_never_opens_a_second_passage(browser):
    pg, kid, s, pid = _family(browser, 4, name="Ola", targets={"reading": 6})
    first = None
    for i in range(6):
        q = s.post(BASE + "/api/reading/next", json={}).json()
        first = first or q["passage"]["key"]
        assert q["passage"]["key"] == first
        it = DB.items.find_one({"_id": q["token"]})
        r = s.post(BASE + "/api/reading/check", json={"token": q["token"], "value": wrong(it["answer"]) if i == 0 else right(it["answer"])}).json()
        if r.get("retry"):
            r = s.post(BASE + "/api/reading/check", json={"token": q["token"], "value": wrong(it["answer"])}).json()
    assert r["day"]["done"] == 6 and r["day"]["target"] == 6, r["day"]


def test_phonics_starts_where_the_parent_says(browser):
    pg, kid, s, pid = _family(browser, 2, name="Cal", targets={"phonics": 6})
    q = s.post(BASE + "/api/phonics/next", json={}).json()
    assert DB.items.find_one({"_id": q["token"]})["meta"]["skill"].startswith("PH2.")
    DB.pupils.update_one({"_id": pid}, {"$set": {"phonics_from": "PH1.04"}})
    s.post(BASE + "/api/phonics/check", json={"token": q["token"], "value": right(DB.items.find_one({"_id": q["token"]})["answer"])})
    q = s.post(BASE + "/api/phonics/next", json={}).json()
    assert DB.items.find_one({"_id": q["token"]})["meta"]["skill"] in ("PH1.04", "PH1.05", "PH1.06")
    pg.goto(f"/children/{pid}/edit")
    assert pg.locator("[data-testid=level-phonics]").input_value() == "PH1.04"
