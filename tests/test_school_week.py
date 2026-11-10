"""The school's week at home: the weekly spelling list from school, "working on this at school" (a strand that gets
most of the questions for a week or two), and rest days (practice weekdays and days off)."""
import base64
import datetime
import re
from zoneinfo import ZoneInfo

import requests

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date()


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _save(page, pid):
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}/edit.*"))


def _label(d: datetime.date) -> str:
    return f"{d.day} {d.strftime('%b')}"


def test_school_spelling_list_comes_first_then_the_year_list(page):
    signup(page)
    pid = add_child(page, "Ada", 3, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    assert "We'll say each word" in page.text_content("#school-list ~ [data-testid=explain]")
    page.fill("[data-testid=school-words]", "because, friend\nzigzagged - The path zigzagged up the hill.\nth3re")
    page.click("form.card button[type=submit]")
    assert "can't be a spelling word" in page.inner_text(".err")
    assert "zigzagged" in page.input_value("[data-testid=school-words]")          # what was typed stays
    assert not DB.pupils.find_one({"_id": pid}).get("school_words")
    page.fill("[data-testid=school-words]", ", ".join(f"word{chr(97 + i // 26)}{chr(97 + i % 26)}" for i in range(31)))
    page.click("form.card button[type=submit]")
    assert "Up to 30" in page.inner_text(".err")
    page.fill("[data-testid=school-words]", "because, friend\nzigzagged - The path zigzagged up the hill.")
    _save(page, pid)
    sl = DB.pupils.find_one({"_id": pid})["school_words"]
    assert [w["w"] for w in sl["words"]] == ["because", "friend", "zigzagged"]
    assert sl["words"][2]["cue"] == "The path ___ up the hill."
    assert sl["until"] == (TODAY + datetime.timedelta(days=7)).isoformat()
    assert "Running until" in page.inner_text("[data-testid=school-running]")

    enter_child(page, "Ada")
    s = _session(page)
    seen = []
    for _ in range(3):
        q = s.post(BASE + "/api/spelling/next", json={}).json()
        word = DB.items.find_one({"_id": q["token"]})["answer"]
        seen.append(word)
        if word == "zigzagged":                       # no recorded clip: the browser's voice says it
            assert q["audio"] == "" and base64.b64decode(q["say"]).decode()[::-1] == "zigzagged"
            assert q["cue"] == "The path ___ up the hill."
        else:
            assert q["audio"].startswith("/api/spelling/audio/") and "say" not in q
        r = s.post(BASE + "/api/spelling/check", json={"token": q["token"], "value": word}).json()
        assert r["correct"]
    assert sorted(seen) == ["because", "friend", "zigzagged"]
    q = s.post(BASE + "/api/spelling/next", json={}).json()            # all done for today: back to the year list
    assert DB.items.find_one({"_id": q["token"]})["answer"] not in seen
    st = DB.spelling_words.find_one({"_id": f"{pid}:zigzagged"})
    assert st["due"] == (TODAY + datetime.timedelta(days=1)).isoformat()   # back tomorrow, every day until learned

    # the word is read aloud in the real page too (a school word with no clip uses speech synthesis)
    page.goto("/me/spelling")
    page.wait_for_function("document.body.dataset.qtoken")

    unlock_parent(page)
    page.goto(f"/children/{pid}")
    card = page.inner_text("[data-testid=card-school-words]")
    # day 1: "3 right so far", not a discouraging "0/3 learned" (wave 5)
    assert "3 right so far" in card and "because, friend, zigzagged" in card
    assert _label(TODAY + datetime.timedelta(days=7)) in card

    # saved again unchanged, the week keeps its dates; emptied, the list stops
    DB.pupils.update_one({"_id": pid}, {"$set": {"school_words.from": (TODAY - datetime.timedelta(days=2)).isoformat()}})
    page.goto(f"/children/{pid}/edit")
    _save(page, pid)
    assert DB.pupils.find_one({"_id": pid})["school_words"]["from"] == (TODAY - datetime.timedelta(days=2)).isoformat()
    page.fill("[data-testid=school-words]", "")
    _save(page, pid)
    assert not DB.pupils.find_one({"_id": pid}).get("school_words")


def test_focus_strand_gets_most_questions_and_shows_on_the_child_page(page):
    signup(page)
    pid = add_child(page, "Ben", 4, targets={"grammar": 5}, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    opts = page.locator("[data-testid=focus-0] option").all_inner_texts()
    assert "Fractions" in opts and not any(re.match(r"\d", o) for o in opts)     # plain names, no ladder numbers
    groups = page.locator("[data-testid=focus-0] optgroup").evaluate_all("gs => gs.map(g => g.label)")
    assert groups[:2] == ["Maths", "Grammar and punctuation"] and "Science: Physics" in groups   # Year 4: sound, electricity
    page.select_option("[data-testid=focus-0]", label="Fractions")
    page.select_option("[data-testid=focus-weeks-0]", "2")
    page.select_option("[data-testid=focus-1]", label="Punctuation")          # each topic has its own weeks
    _save(page, pid)
    f = DB.pupils.find_one({"_id": pid})["focus"]
    until, until1 = TODAY + datetime.timedelta(days=14), TODAY + datetime.timedelta(days=7)
    assert [(i["subject"], i["until"]) for i in f] == [("maths", until.isoformat()), ("grammar", until1.isoformat())]
    assert f[0]["strand"].endswith("Fractions") and f[1]["strand"] == "Punctuation"
    page.goto(f"/children/{pid}")
    assert page.inner_text("[data-testid=focus]").startswith(
        f"Focus: Maths: Fractions until {_label(until)} · Grammar: Punctuation until {_label(until1)}")

    enter_child(page, "Ben")
    s = _session(page)
    strands = []
    for _ in range(30):
        q = s.post(BASE + "/api/maths/next", json={}).json()
        strands.append(q["strand"])
        s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": "-98765"})
    assert sum(st == f[0]["strand"] for st in strands) >= 13, strands   # about two in three
    assert len(set(strands)) > 1                                         # the rest of the plan carries on
    gs = []
    for _ in range(18):
        q = s.post(BASE + "/api/grammar/next", json={}).json()
        gs.append(q["strand"])
        s.post(BASE + "/api/grammar/check", json={"token": q["token"], "value": "zzzz"})
    assert sum(st == "Punctuation" for st in gs) >= 7, gs

    # it ends by itself
    DB.pupils.update_one({"_id": pid}, {"$set": {"focus.0.until": TODAY.isoformat(), "focus.1.until": TODAY.isoformat()}})
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    assert not page.locator("[data-testid=focus]").count()


def test_rest_days_show_as_rest_and_never_take_back_a_reward(page):
    signup(page)
    page.goto("/settings")
    page.fill("#reward_text", "Park trip")
    page.fill("#reward_threshold", "100")
    page.click("form[action='/settings'] button[type=submit]")
    pid = add_child(page, "Cara", 3, targets={"tables": 1}, year_defaults=True)
    wd = TODAY.weekday()

    # today is not a practice day (the child hasn't started, so it applies today)
    page.goto(f"/children/{pid}/edit")
    page.uncheck("[data-testid=on-maths]")
    page.uncheck("[data-testid=on-spelling]")
    page.uncheck(f"[data-testid=pday-{wd}]")
    _save(page, pid)
    p = DB.pupils.find_one({"_id": pid})
    assert wd not in p["practice_days"] and p["days_log"][-1]["from"] == TODAY.isoformat()
    page.goto("/home")
    card = page.locator("[data-testid='kid-Cara']")
    assert card.locator("[data-testid=rest-day]").inner_text() == "Rest day"
    page.goto(f"/children/{pid}")
    assert "Rest day" in page.inner_text("[data-testid=today-rest]")
    assert page.locator("[data-testid=history-rest]").count() == 1

    enter_child(page, "Cara")
    assert "Today is a rest day — enjoy it!" in page.inner_text("[data-testid=rest-day]")
    s = _session(page)
    q = s.post(BASE + "/api/tables/next", json={}).json()                # practice is still allowed
    r = s.post(BASE + "/api/tables/check", json={"token": q["token"], "value": DB.items.find_one({"_id": q["token"]})["answer"]}).json()
    assert r["correct"] and r["day"]["reward"] == ""                     # extra: no reward on a rest day
    unlock_parent(page)
    page.goto("/home")
    assert "1 extra right answer anyway" in page.inner_text("[data-testid='kid-Cara']")
    page.goto("/board")
    assert page.locator("[data-testid=rest-day]").count() == 1

    # practice day again: the child has started, so the change waits until tomorrow
    page.goto(f"/children/{pid}/edit")
    page.check(f"[data-testid=pday-{wd}]")
    _save(page, pid)
    p = DB.pupils.find_one({"_id": pid})
    assert p["days_log"][-1]["from"] == (TODAY + datetime.timedelta(days=1)).isoformat()
    page.goto("/home")
    assert page.locator("[data-testid='kid-Cara'] [data-testid=rest-day]").count() == 1
    page.goto(f"/children/{pid}/edit")
    page.check(f"[data-testid=pday-{wd}]")
    page.check("[data-testid=plan-today]")                               # ... unless asked for today too
    _save(page, pid)
    page.goto("/home")
    assert page.locator("[data-testid='kid-Cara'] [data-testid=pct]").inner_text() == "100%"
    assert "Cara earned: Park trip" in page.inner_text("[data-testid='kid-Cara']")

    # plain errors for days off
    page.goto(f"/children/{pid}/edit")
    for first, last, msg in [((TODAY - datetime.timedelta(days=1)), None, "today or later"),
                             (TODAY + datetime.timedelta(days=3), TODAY + datetime.timedelta(days=1), "before the first"),
                             (TODAY, TODAY + datetime.timedelta(days=21), "up to 3 weeks")]:
        page.evaluate("document.querySelectorAll('input[type=date]').forEach(i => { i.removeAttribute('min'); })")
        page.fill("[data-testid=off-from]", first.isoformat())
        page.fill("[data-testid=off-to]", last.isoformat() if last else "")
        page.click("form.card button[type=submit]")
        assert msg in page.inner_text(".err"), msg
    for i in range(7):
        page.uncheck(f"[data-testid=pday-{i}]")
    page.fill("[data-testid=off-from]", "")
    page.fill("[data-testid=off-to]", "")
    page.click("form.card button[type=submit]")
    assert "at least one practice day" in page.inner_text(".err")

    # a day off for today (a sick day) applies at once, and the reward earned today stays earned
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=off-from]", TODAY.isoformat())
    _save(page, pid)
    assert DB.pupils.find_one({"_id": pid})["days_off"] == [{"from": TODAY.isoformat(), "to": TODAY.isoformat()}]
    page.goto("/home")
    card = page.locator("[data-testid='kid-Cara']")
    assert "Cara earned: Park trip" in card.inner_text() and card.locator("[data-testid=rest-day]").inner_text() == "Day off"
    assert "had already done 100% of the plan" in card.inner_text()
    page.goto(f"/children/{pid}")
    assert "Day off" in page.inner_text("[data-testid=history-rest]")
    page.goto(f"/children/{pid}/edit")
    assert "(now)" in page.inner_text("[data-testid=days-off]")
    page.check("[data-testid=days-off] input[name=off_remove]")          # cancelled: a practice day again
    _save(page, pid)
    assert DB.pupils.find_one({"_id": pid})["days_off"] == []


def test_school_list_sentences_in_a_comma_list_and_homophones():
    from app.drills import spelling
    words, err = spelling.parse_school_words("because, people, thought, through, should, their - it is their dog, should, could")
    assert not err and [(w["w"], w["cue"]) for w in words] == [
        ("because", ""), ("people", ""), ("thought", ""), ("through", ""), ("should", ""), ("their", "it is ___ dog"),
        ("could", "")]
    words, _ = spelling.parse_school_words("went, want - I want a dog, what\nwhen - When I got home, I had tea, said")
    assert [(w["w"], w["cue"]) for w in words] == [("went", ""), ("want", "I ___ a dog"), ("what", ""),
                                                   ("when", "___ I got home, I had tea"), ("said", "")]
    assert not spelling.school_doubts("went, want - I want a dog, what")
    doubt = spelling.school_doubts("went, want I want a dog, what")
    assert doubt.startswith("“I”, “a” and “dog” look like part of a sentence: did you mean “want - I want a dog”?")
    assert spelling.school_doubts("their it is their dog should could")
    assert not spelling.school_doubts("the a do to today of said says are were\nI you your they")   # a Year 1 list
    # a homophone with no sentence: our sentence if we have one, else ask, else a short meaning
    assert spelling.cue_for("their") == ("The children put on ___ coats.", "ours")
    assert spelling.cue_for("maid")[1] == "meaning" and spelling.cue_for("zigzag") == ("", "")
    s = spelling.school_summary(spelling.parse_school_words("their, witch, said - Mum said yes")[0], "Sam")
    assert (s["n"], s["yours"], s["ours"]) == (3, 1, 1)
    assert s["ask"] == ["‘witch’ sounds like ‘which’: add a sentence after a dash so Sam knows which one, like “witch - …”."]


def test_school_list_is_checked_shown_back_and_last_weeks_tricky_words_stay(page):
    signup(page)
    pid = add_child(page, "Sam", 4, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=school-words]", "went, want I want a dog, what")
    page.click("form.card button[type=submit]")
    assert "“I”, “a” and “dog” look like part of a sentence" in page.inner_text("[data-testid=school-doubt]")
    assert not DB.pupils.find_one({"_id": pid}).get("school_words")             # nothing saved yet
    page.fill("[data-testid=school-words]", "because, people, thought, should, their - it is their dog, could, witch")
    _save(page, pid)
    summary = page.inner_text("[data-testid=school-summary]")
    assert "Saved: 7 words: because, people, thought, should, their, could, witch · 1 with your sentence" in summary
    assert "‘witch’ sounds like ‘which’" in page.inner_text("[data-testid=school-ask]")
    # the same doubt can be overruled: "Save the list as it is"
    page.fill("[data-testid=school-words]", "ice cream, jelly")
    page.click("form.card button[type=submit]")
    page.check("[data-testid=school-ok]")
    _save(page, pid)
    assert [w["w"] for w in DB.pupils.find_one({"_id": pid})["school_words"]["words"]] == ["ice", "cream", "jelly"]

    # last week's words: still tricky ones are named on the card, and come back in practice when due
    DB.pupils.update_one({"_id": pid}, {"$set": {"school_words.words": [{"w": "because", "cue": ""}, {"w": "people", "cue": ""}]}})
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    for w, box, wrong in (("because", 0, 2), ("people", 3, 1)):
        DB.spelling_words.insert_one({"_id": f"{pid}:{w}", "pupil_id": pid, "family_id": fam, "word": w, "box": box,
                                      "due": TODAY.isoformat(), "wrong": wrong, "right": box})
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=school-words]", "zigzag")
    _save(page, pid)
    assert DB.pupils.find_one({"_id": pid})["school_words"]["before"][:2] == ["because", "people"]
    page.goto(f"/children/{pid}")
    assert page.inner_text("[data-testid=school-last-tricky]").startswith("Last week's words still tricky: because")
    assert [t.strip("✕ \n") for t in page.locator("[data-testid=tricky-word]").all_inner_texts()] == ["because"]  # people is learned
    enter_child(page, "Sam")
    s = _session(page)
    got = []
    for _ in range(2):
        q = s.post(BASE + "/api/spelling/next", json={}).json()
        word = DB.items.find_one({"_id": q["token"]})["answer"]
        got.append(word)
        s.post(BASE + "/api/spelling/check", json={"token": q["token"], "value": word})
    assert got[0] == "zigzag" and "because" in got + [DB.items.find_one(
        {"_id": s.post(BASE + "/api/spelling/next", json={}).json()["token"]})["answer"]]
