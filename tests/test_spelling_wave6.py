"""Wave 6 spelling: "thru" is a misspelling, never "spelt right"; a clearly different real word is kept for the
parent, left out of the %, and gets one real retry; each school word has one state (learned ✓✓✓, on its way, tricky,
not asked yet) on Progress and on the printed report, with last week's list; Years 3-4 start with easy words and
every year eases off after misses; an activity ends after twice its target in Years 1-4, and spelling in every year."""
import datetime
import os
import sys
from zoneinfo import ZoneInfo

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills import spelling  # noqa: E402
from app.activities import has_cap  # noqa: E402

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent  # noqa: E402

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date()
ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _kid(page, year, name, target=8, words=None):
    signup(page)
    pid = add_child(page, name, year)
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {k: {"on": k == "spelling", "target": target} for k in ALL}},
                                        "$unset": {"plan_log": ""}})
    if words:
        DB.pupils.update_one({"_id": pid}, {"$set": {"school_words": {
            "words": [{"w": w, "cue": ""} for w in words], "from": TODAY.isoformat(),
            "until": (TODAY + datetime.timedelta(days=7)).isoformat(), "before": []}}})
    enter_child(page, name)
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return pid, s


def _ask(s):
    q = s.post(BASE + "/api/spelling/next", json={}).json()
    return q, DB.items.find_one({"_id": q["token"]})["answer"]


def _check(s, token, value):
    return s.post(BASE + "/api/spelling/check", json={"token": token, "value": value}).json()


# ------------------------------------------------------------------ pure ----
def test_informal_american_and_sound_alike_words_are_never_another_real_word():
    for typed, word in (("thru", "through"), ("nite", "night"), ("tonite", "tonight"), ("lite", "light"),
                        ("cos", "because"), ("enuf", "enough"), ("tuff", "tough"), ("color", "colour"),
                        ("center", "centre"), ("realize", "realise"), ("traveled", "travelled"), ("catalog", "catalogue"),
                        ("defense", "defence"), ("threw", "through"), ("their", "there"), ("wear", "where"),
                        ("accident", "accidentally"), ("bog", "dog"), ("enormus", "enormous")):
        assert not spelling.other_word(typed, word), (typed, word)
    for typed, word in (("supervise", "accompany"), ("obvious", "apparent"), ("nervous", "anxious"), ("elephant", "busy")):
        assert spelling.other_word(typed, word), (typed, word)


def test_year34_starts_easy_and_every_year_eases_off():
    order = spelling.list_for_year(3)
    assert sorted(order) == sorted(spelling.LISTS["Y3-4"]) and len(order) == len(set(order))
    first = order[:12]
    for hard in ("actual", "address", "accidentally", "knowledge", "business", "question"):
        assert hard not in first and order.index(hard) > 40, hard
    assert order.index("accidentally") > order.index("accident") > order.index("learn")
    for year in range(1, 10):
        easy = spelling.easy_words(year)
        assert easy and all(w in spelling.CUES for w in easy), year
        w = spelling._easier({"year": year}, spelling.list_for_year(year), {}, set())
        assert w in easy, (year, w)
    # a word just missed is not "an easier one"; one spelt right before comes first
    words = spelling.list_for_year(6)
    assert spelling._easier({"year": 6}, words, {"learn": {"box": 0, "wrong": 2}}, set()) != "learn"
    assert spelling._easier({"year": 6}, words, {"queue": {"box": 1, "right": 1}}, set()) == "queue"


def test_one_state_a_school_word():
    st = spelling.word_state
    assert st(None, None)["state"] == "new"
    assert st({"box": 0, "others": 1, "other": "supervise"}, None) == {"state": "tricky", "ticks": 0, "again": False,
                                                                      "other": "supervise"}
    assert st({"box": 2, "right": 2}, None)["state"] == "way" and st({"box": 2}, None)["ticks"] == 2
    assert st({"box": 3}, None)["state"] == "learned"


def test_the_cap_covers_years_1_to_4_and_spelling_always():
    assert has_cap({"year": 3}, "tables") and has_cap({"year": 4}, "maths") and has_cap({"year": 9}, "spelling")
    assert not has_cap({"year": 5}, "maths") and not has_cap({"year": 8}, "grammar")
    assert has_cap({"year": 5, "school_year": 4}, "maths")              # by the school year, not the level worked at


# ------------------------------------------------------------------ through the app ----
def test_thru_is_a_mistake_and_another_real_word_is_kept_for_the_parent(page):
    pid, s = _kid(page, 3, "Olivia", words=["through", "busy", "guest"])
    seen = {}
    for _ in range(3):
        q, word = _ask(s)
        seen[word] = q
        if word == "through":
            res = _check(s, q["token"], "thru")
            assert res["correct"] is False and not res.get("other") and not res.get("retry"), res
            assert "spelt right" not in (res.get("hint") or "")
        elif word == "busy":
            res = _check(s, q["token"], "elephant")
            assert res["other"] and res["retry"] and "Listen again, then type it." in res["hint"]
            res = _check(s, q["token"], "giraffe")                       # the one retry: another real word again
            assert res["other"] and not res.get("retry") and "It comes back later" in res["hint"]
        else:
            _check(s, q["token"], word)
    assert set(seen) == {"through", "busy", "guest"}
    # neither "other" try is a mistake or in the day's %; both are kept
    assert DB.attempts.count_documents({"pupil_id": pid, "other": True, "detail": "busy"}) == 2
    assert not DB.attempts.find_one({"pupil_id": pid, "detail": "busy", "correct": False, "copied": {"$ne": True}})
    assert DB.attempts.find_one({"pupil_id": pid, "detail": "through", "correct": False, "got": "thru"})

    unlock_parent(page)
    page.goto(f"/children/{pid}")
    tricky = page.inner_text("[data-testid=school-tricky]")
    assert "through ✗" in tricky and "busy ✗" in tricky and "wrote giraffe: a real word, not the one asked" in tricky, tricky
    assert "guest ✓" in page.inner_text("[data-testid=school-way]")
    assert not page.locator("[data-testid=school-new]").count()          # every word was asked
    assert page.inner_text("[data-testid=school-learned-n]") == "1 on its way"          # not a bare "0/3"
    assert "of 3 words · 2 tricky" in page.inner_text("[data-testid=school-counts]")
    others = page.inner_text("[data-testid=other-words]")
    assert "wrote elephant for busy" in others and "wrote giraffe for busy" in others
    mistakes = page.inner_text("#mistakes ~ details") if page.locator("#mistakes ~ details").count() else ""
    assert "thru" in mistakes and "elephant" not in mistakes

    # a new week: last week's words stay until learned (guest was right once, busy has only "other" tries)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=school-words]", "guard, guide")
    page.click("form.card button[type=submit]")
    page.wait_for_url(f"**/children/{pid}/edit**")
    page.goto(f"/children/{pid}")
    last = page.inner_text("[data-testid=school-last-tricky]")
    assert last.startswith("Last week's words still to learn") and all(w in last for w in ("through", "busy", "guest")), last
    sl = DB.pupils.find_one({"_id": pid})["school_words"]
    assert sl["past"][0]["words"] == ["through", "busy", "guest"] and sl["past"][0]["from"] == TODAY.isoformat()

    # the printed report: the school lists word by word, this week's and last week's, with their dates
    page.goto(f"/children/{pid}/report?range=7")
    rep = page.inner_text("[data-testid=report-school]")
    assert "This week's list: from" in rep and "List from" in rep, rep
    rows = page.locator("[data-testid=report-school-word]").all_inner_texts()
    assert any(r.startswith("guard") and "Not asked yet" in r for r in rows), rows
    assert any(r.startswith("through") and "Tricky ✗" in r for r in rows), rows
    assert any(r.startswith("guest") and "On its way ✓" in r for r in rows), rows
    assert any(r.startswith("busy") and "wrote giraffe" in r for r in rows), rows


def test_another_real_word_does_not_lower_the_days_right_first_time(page):
    pid, s = _kid(page, 6, "Isaac", target=3, words=["accompany", "apparent", "harass"])
    for _ in range(3):
        q, word = _ask(s)
        _check(s, q["token"], "supervise" if word == "accompany" else word)
        if word == "accompany":
            _check(s, q["token"], "obvious")                             # the retry: another real word too
    unlock_parent(page)
    page.goto(f"/children/{pid}/report?range=7")
    # two right of two first tries: the two "other" tries are neither right nor wrong (progress.day_stats)
    assert page.inner_text("[data-testid=first-pct]") == "100%"


def test_spelling_ends_after_twice_its_target_in_every_year(page):
    pid, s = _kid(page, 7, "Kemi", target=2)
    day = None
    for _ in range(4):
        q, word = _ask(s)
        day = _check(s, q["token"], "zzqx")["day"]
    assert day["capped"] and day["done"] == 2, day
