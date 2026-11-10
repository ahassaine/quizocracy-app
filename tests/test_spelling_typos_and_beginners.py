"""Wave 4 spelling: a parent's typing slip in the school list ("frend: did you mean friend?"), and fixing or removing
a word takes it back everywhere; Year 1 starts with words to sound out and eases off after a run of misses; tricky
words are corrected letter by letter; a different real word spelt right is not a spelling mistake; each child gets
their own order of words; and a one-letter slip in a grammar or vocabulary answer gets one "Nearly"."""
import datetime
import os
import re
import sys
from zoneinfo import ZoneInfo

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.bank import engine as bank  # noqa: E402
from app.drills import spelling, typos  # noqa: E402

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent  # noqa: E402

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date()


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _save(page, pid):
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(rf".*/children/{pid}/edit.*"))


def _answer(s, value=None):
    """Ask the next spelling word and answer it (value None: right). Returns (word, check result)."""
    q = s.post(BASE + "/api/spelling/next", json={}).json()
    word = DB.items.find_one({"_id": q["token"]})["answer"]
    res = s.post(BASE + "/api/spelling/check", json={"token": q["token"], "value": word if value is None else value(word)}).json()
    return word, res, q


# ------------------------------------------------------------------ pure ----
def test_word_list_finds_slips_and_suggests_the_word():
    assert not spelling.is_word("frend") and spelling.suggest("frend")[0] == "friend"
    assert spelling.suggest("enormus") == ["enormous"] and spelling.suggest("dont")[0] == "don't"
    assert spelling.suggest("wensday")[0] == "Wednesday" and spelling.suggest("well-knwn") == ["well-known"]
    for w in ("friend", "enormous", "don't", "well-known", "London", "zigzag", "Christmas"):
        assert spelling.is_word(w), w
    words = spelling.parse_school_words("frend, because, Zog")[0]
    assert [u["w"] for u in spelling.school_unknown(words)] == ["frend", "Zog"]
    assert [u["w"] for u in spelling.school_unknown(words, kept=["zog"])] == ["frend"]
    fixed, changed, kept = spelling.apply_fixes(words, {"frend": "friend", "zog": spelling.KEEP})
    assert [w["w"] for w in fixed] == ["friend", "because", "Zog"] and changed == {"frend": "friend"} and kept == {"zog"}


def test_tricky_words_get_letter_hints_and_letters_read_out():
    assert typos.letter_hint("sed", "said") == "sed → said: e should be ai"
    assert typos.letter_hint("ov", "of") == "ov → of: v should be f" and typos.letter_hint("du", "do").endswith("u should be o")
    assert typos.letter_hint("cat", "dog") == ""                                 # another word: no letter hint
    assert typos.spelled("said") == "said: s, a, i, d"
    assert typos.say_letters("e should be ai") == "E should be A, I"
    assert typos.say_letters("swap the i and e (e before i after c)") == "swap the I and E (E before I after C)"


def test_another_real_word_is_not_a_misspelling():
    assert spelling.other_word("nervous", "anxious") and spelling.other_word("dog", "cat")
    assert not spelling.other_word("bog", "dog")              # one letter off: a slip to correct ("b should be d")
    assert not spelling.other_word("their", "there")          # sounds alike: the hint sentence tells them apart
    assert not spelling.other_word("color", "colour") and not spelling.other_word("enormus", "enormous")


def test_hint_sentences_fit_only_their_word():
    # with the sound off, the sentence and the letter count must lead to one word (P8: nervous/anxious)
    assert "test" not in spelling.CUES["anxious"] and "system" in spelling.CUES["nervous"]
    assert spelling.CUES["said"] != "Mum ___ yes." and spelling.CUES["absolutely"] != "I am ___ sure."


def test_grammar_and_vocabulary_slips_are_nearly_but_word_endings_are_not():
    q = next(q for q in bank.skill("GP6.06")["qs"] if q.get("a") == ["approximately"])      # formal vocabulary
    assert bank.slips(bank.serve(q)[1], "aproximately", q["q"], bank.skill("GP6.06")) == [("aproximately", "approximately")]
    sk = bank.skill("GP6.03")                                                             # tenses
    q = next(q for q in sk["qs"] if q.get("a") == ["was cooking"])
    assert bank.slips(bank.serve(q)[1], "was cookng", q["q"], sk) == [("cookng", "cooking")]
    assert not bank.slips(bank.serve(q)[1], "was cookin", q["q"], sk)                  # the -ing itself is wrong
    sk = bank.skill("GP1.08")                                                             # plurals: the ending IS the skill
    q = next(q for q in sk["qs"] if q["t"] == "text")
    key = bank.serve(q)[1]
    want = key["a"][0]
    assert not bank.slips(key, want[:-1] + ("x" if want[-1] != "x" else "y"), q["q"], sk)


# ------------------------------------------------------------------ the school list ----
def test_a_typo_in_the_school_list_is_asked_about_and_fixing_it_takes_it_back(page):
    signup(page)
    pid = add_child(page, "Amir", 3, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=school-words]", "frend, because, Zog")
    page.click("form.card button[type=submit]")
    box = page.inner_text("[data-testid=school-unknown]")
    assert "“frend”: did you mean “friend”?" in box and "“Zog”" in box
    assert not DB.pupils.find_one({"_id": pid}).get("school_words")                    # nothing saved yet
    page.check("[data-testid=keep-zog]")
    page.click("form.card button[type=submit]")                                        # frend still not chosen
    assert page.locator("[data-testid=school-unknown-word]").count() == 2 and page.is_checked("[data-testid=keep-zog]")
    page.check("[data-testid=keep-frend]")                                             # the parent keeps the slip
    _save(page, pid)
    sl = DB.pupils.find_one({"_id": pid})["school_words"]
    assert [w["w"] for w in sl["words"]] == ["frend", "because", "Zog"] and sl["kept"] == ["frend", "zog"]

    # the child, who spells it right, is marked wrong against the slip
    enter_child(page, "Amir")
    s = _session(page)
    seen = {}
    for _ in range(3):
        word, res, _ = _answer(s, lambda w: "friend" if w == "frend" else w)
        seen[word] = res
    assert seen["frend"]["correct"] is False
    assert DB.attempts.find_one({"pupil_id": pid, "detail": "frend", "correct": False})

    # the parent fixes it on the saved list: it is gone from the mistakes, the queue and the report
    unlock_parent(page)
    page.goto(f"/children/{pid}/edit")
    assert page.locator("[data-testid=school-unknown-word]").count() == 0                # kept: not asked again
    page.fill("[data-testid=school-words]", "friend, because, Zog")
    _save(page, pid)
    sl = DB.pupils.find_one({"_id": pid})["school_words"]
    assert [w["w"] for w in sl["words"]] == ["friend", "because", "Zog"] and "frend" not in sl["before"]
    assert not DB.attempts.find_one({"pupil_id": pid, "detail": "frend"})
    assert DB.attempts.find_one({"pupil_id": pid, "withdrawn": "frend"})["correct"] is True     # "friend" was right
    assert not DB.spelling_words.find_one({"_id": f"{pid}:frend"})
    page.goto(f"/children/{pid}")
    body = page.inner_text("body")
    assert "frend" not in body
    page.goto(f"/children/{pid}/report")
    assert "frend" not in page.inner_text("body")


def test_fixing_a_word_by_its_choice_and_removing_last_weeks_tricky_word(page):
    signup(page)
    pid = add_child(page, "Ada", 4, year_defaults=True)
    page.goto(f"/children/{pid}/edit")
    page.fill("[data-testid=school-words]", "enormus, because")
    page.click("form.card button[type=submit]")
    page.check("[data-testid=fix-enormus-0]")                                          # "Change to enormous"
    _save(page, pid)
    assert [w["w"] for w in DB.pupils.find_one({"_id": pid})["school_words"]["words"]] == ["enormous", "because"]

    # an earlier week's word still tricky can be taken out by the parent
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.pupils.update_one({"_id": pid}, {"$set": {"school_words.before": ["purpus"]}})
    DB.spelling_words.insert_one({"_id": f"{pid}:purpus", "pupil_id": pid, "family_id": fam, "word": "purpus", "box": 0,
                                  "due": TODAY.isoformat(), "wrong": 1, "right": 0})
    DB.attempts.insert_one({"pupil_id": pid, "family_id": fam, "activity": "spelling", "correct": False, "detail": "purpus",
                            "day": TODAY.isoformat(), "ts": datetime.datetime.utcnow(), "q": "Spell the word you heard",
                            "exp": "purpus", "got": "purpose"})
    page.goto(f"/children/{pid}")
    assert "purpus" in page.inner_text("[data-testid=school-last-tricky]")
    page.click("[data-testid=remove-tricky]")
    page.wait_for_url(re.compile(r".*removed=purpus.*"))
    assert "“purpus” is out" in page.inner_text("[data-testid=tricky-removed]")
    assert not page.locator("[data-testid=school-last-tricky]").count()
    assert "purpus" not in DB.pupils.find_one({"_id": pid})["school_words"]["before"]
    assert not DB.spelling_words.find_one({"_id": f"{pid}:purpus"}) and not DB.attempts.find_one({"detail": "purpus"})


# ------------------------------------------------------------------ the child's spelling ----
def test_year1_sounds_out_first_eases_off_and_spells_tricky_words_letter_by_letter(page):
    signup(page)
    pid = add_child(page, "Oscar", 1, year_defaults=True)
    assert DB.pupils.find_one({"_id": pid})["activities"]["spelling"]["target"] == 5
    enter_child(page, "Oscar")
    s = _session(page)
    words = []
    for _ in range(3):
        w, res, q = _answer(s, lambda w: "zz")
        words.append(w)
        assert "say" in q and res["correct"] is False                    # a sound-it-out word: the browser says it
    assert all(w in spelling.DECODABLE for w in words), words
    w, res, q = _answer(s)
    assert q.get("ease") == "Let's try an easier one." and w in spelling.EASY and res["correct"]
    w, _, q = _answer(s)
    assert not q.get("ease")                                              # a right answer ends the run

    # a tricky word: the letters one by one, on screen and read out, with the tricky part
    DB.spelling_words.delete_many({"pupil_id": pid})
    DB.pupils.update_one({"_id": pid}, {"$set": {"school_words": {"words": [{"w": "said", "cue": ""}], "from": TODAY.isoformat(),
                                                                  "until": (TODAY + datetime.timedelta(days=7)).isoformat(), "before": []}}})
    DB.attempts.delete_many({"pupil_id": pid})
    w, res, _ = _answer(s, lambda w: "sed")
    assert w == "said" and res["hint"] == "sed → said: e should be ai · said: s, a, i, d"
    assert res["spoken"] == "Not quite. said is spelt S, A, I, D. The tricky part: E should be A, I."


def test_a_right_spelling_of_another_word_is_not_a_mistake_and_twins_get_their_own_order(page):
    signup(page)
    a = add_child(page, "Adaeze", 4, year_defaults=True)
    b = add_child(page, "Chidi", 4, year_defaults=True)
    firsts = {}
    for name, pid in (("Adaeze", a), ("Chidi", b)):
        unlock_parent(page) if name == "Chidi" else None
        enter_child(page, name)
        s = _session(page)
        firsts[name] = [_answer(s)[0] for _ in range(5)]
    assert firsts["Adaeze"] != firsts["Chidi"], firsts                    # the same words, not in the same order

    s = _session(page)                                                    # Chidi, still signed in
    word, res, _ = _answer(s, lambda w: "elephant" if w.lower() != "elephant" else "giraffe")
    assert res["other"] and res["retry"] and res["hint"] == f"That is spelt right, but the word was {word}. Listen again, then type it."
    assert not DB.attempts.find_one({"pupil_id": b, "detail": word, "correct": False, "copied": {"$ne": True}})
    tok = DB.items.find_one({"pupil_id": b, "answer": word, "done": False})["_id"]          # one more go at it
    res = s.post(BASE + "/api/spelling/check", json={"token": tok, "value": word}).json()
    assert res["correct"] and res.get("again_later")                     # right straight after being shown it
    nxt = s.post(BASE + "/api/spelling/next", json={}).json()
    assert DB.items.find_one({"_id": nxt["token"]})["answer"] != word     # it comes back later, not straight away


def test_spelling_page_shows_the_other_word_message_without_not_quite(page):
    signup(page)
    pid = add_child(page, "Isla", 8, year_defaults=True)
    for size in ((390, 844), (1280, 800)):
        page.set_viewport_size({"width": size[0], "height": size[1]})
        enter_child(page, "Isla")
        page.goto("/me/spelling")
        page.wait_for_function("document.body.dataset.qtoken")
        tok = page.evaluate("document.body.dataset.qtoken")
        word = DB.items.find_one({"_id": tok})["answer"]
        page.fill("#answer", "elephant" if word.lower() != "elephant" else "giraffe")
        page.click("#check")
        page.wait_for_selector("#feedback.warn [data-testid=sound-tip]")
        fb = page.inner_text("#feedback")
        assert "Not quite" not in fb and f"the word was {word}" in fb and "Turn your sound on" in fb
        # one real retry: the box is empty, Check works and Enter sends it
        assert page.input_value("#answer") == "" and page.is_enabled("#check") and page.is_hidden("#next")
        page.fill("#answer", word)
        page.press("#answer", "Enter")
        page.wait_for_selector("#feedback.yes")
        assert DB.items.find_one({"_id": tok})["done"]
        shots = os.getenv("QZ_SHOTS")
        if shots:
            page.screenshot(path=os.path.join(shots, f"other-word-{size[0]}.png"))
        unlock_parent(page)
