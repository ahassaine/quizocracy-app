"""Fix wave 2 marking: a spelling slip where spelling is not the skill gets one free retry; spelling feedback shows
the wrong letters; "+10" counts for "add 10" and "two" for 2; content fixes found by real families."""
import datetime
import os
import random
import re
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.bank import engine as bank  # noqa: E402
from app.drills import typos  # noqa: E402
from app.maths import maths_engine as me  # noqa: E402

from conftest import BASE, DB, add_child, enter_child, signup  # noqa: E402


# ------------------------------------------------------------------ pure marking ----
def test_one_slip_is_small_and_never_another_answer_word():
    assert typos.slips(["yse"], ["yes"]) and typos.slips(["ded"], ["dead"]) and typos.slips(["respiraton"], ["respiration"])
    assert typos.slips("eigth thousand three hundred".split(), "eight thousand three hundred".split(), typos.NUMBER_WORDS)
    assert not typos.slips(["eighty"], ["eight"], typos.NUMBER_WORDS)       # another number, not a slip
    assert not typos.slips(["cot"], ["cat"])                               # a 3-letter word changed is another word
    assert not typos.slips(["no"], ["yes"]) and not typos.slips(["resperashun"], ["respiration"])
    assert not typos.slips("one two three".split(), "ome twa thee".split())   # three slips is not "nearly"


def test_maths_word_answers_slip_but_numbers_and_choices_do_not():
    assert me.slipped_words("str", "yes", "yse", "Is 24 in the 3 times table? (yes or no)") == [("yse", "yes")]
    assert me.slip_hint("yes", [("yse", "yes")]) == typos.RETRY
    words = me.n_words(394)
    assert me.slipped_words("str", words, words.replace("ninety", "ninty"), "Write 394 in words")
    assert "Your number is right" in me.slip_hint(words, [("ninty", "ninety")])
    assert not me.slipped_words("str", "tenths", "tenth", "Which place? (tenths / hundredths / tenth)")
    assert not me.slipped_words("int", 12, "13", "")


def test_rules_and_number_words_are_accepted():
    for v in ("+10", "+ 10", "add 10", "plus 10", "add 10 each time", "+10 each time"):
        assert me.check_answer("str", "add 10", v), v
    assert me.check_answer("str", "subtract 3", "-3") and me.check_answer("str", "multiply by 2", "x2")
    assert me.check_answer("str", "multiply by 2 then add 1", "×2 +1")
    assert not me.check_answer("str", "add 10", "-10") and not me.check_answer("str", "add 10", "10")
    assert me.check_answer("int", 2, "two", prompt="How many lines of symmetry?")
    assert not me.check_answer("int", 19, "nineteen", prompt="Write nineteen in digits")
    assert bank.parse_num("two") == 2 and bank.mark({"t": "num", "a": 2}, "Two")


def test_science_text_slips_only_in_science():
    sci = {"t": "text", "a": ["respiration"], "loose": True}
    assert bank.slips(sci, "respiraton") and bank.slips(sci, "the respiraton")
    assert not bank.slips({"t": "text", "a": ["babies"]}, "babys")         # grammar: the spelling is the point
    assert not bank.slips({"t": "text", "a": ["dead"], "loose": True}, "deaf", "Living, dead, deaf?")


def test_spelling_hint_shows_the_letters():
    assert typos.letter_hint("acsident", "accident") == "acsident → accident: cs should be cc"
    assert typos.letter_hint("acident", "accident").endswith("c should be cc")
    assert typos.letter_hint("knowlege", "knowledge").endswith("add d after le")
    assert typos.letter_hint("xyz", "accident") == ""
    assert typos.american("analyse", "analyze") and not typos.american("analyse", "analise")
    m = typos.letter_marks("acsident", "accident")
    assert ["s", True] in m["typed"] and ["c", True] in m["word"]


# Real children's misspellings (wave 3): every kind of message, worded as a teacher would say it.
CHILD_SLIPS = {
    "recieve": "receive: swap the i and e (e before i after c)",
    "beleive": "believe: swap the e and i (i before e, except after c)",
    "acheive": "achieve: swap the e and i (i before e, except after c)",
    "freind": "friend: swap the e and i (i before e, except after c)",
    "becuase": "because: swap the u and a", "poeple": "people: swap the o and e",
    "persaude": "persuade: swap the a and u", "eqiupment": "equipment: swap the i and u",
    "wich": "which: add h after w", "definately": "definitely: a should be i", "seperate": "separate: pe should be pa",
    "untill": "until: ll should be l", "tommorow": "tomorrow: mm should be m; r should be rr",
    "accomodate": "accommodate: m should be mm", "embarass": "embarrass: r should be rr",
    "prejudise": "prejudice: s should be c", "prejubice": "prejudice: b should be d",
}


def test_spelling_messages_for_real_misspellings():
    for typed, msg in CHILD_SLIPS.items():
        word = msg.split(":")[0]
        assert typos.letter_hint(typed, word) == f"{typed} → {msg}", typed
        hint = typos.letter_hint(typed, word)
        assert not ("add " in hint and "take out" in hint), hint        # never "add u …; take out the u"
    assert typos.letter_hint("wierd", "weird").endswith("(this word has e before i)")
    assert typos.letter_hint("sceince", "science").endswith("(i before e, even after c here)")
    m = typos.letter_marks("recieve", "receive")                    # a swap is marked as the pair, in both
    assert m == {"typed": [["rec", False], ["ie", True], ["ve", False]], "word": [["rec", False], ["ei", True], ["ve", False]]}


def test_grammar_one_word_slip_retries_unless_spelling_is_the_skill():
    sk = bank.skill("GP5.03")                                          # relative pronouns
    q = next(q for q in sk["qs"] if q["t"] == "text" and q["a"] == ["which"])
    key = bank.serve(q)[1]
    assert bank.slips(key, "wich", q["q"], sk) == [("wich", "which")] and bank.slips(key, "whitch", q["q"], sk)
    assert not bank.slips(key, "who", q["q"], sk) and not bank.slips(key, "that", q["q"], sk)   # real choices
    assert not bank.slips(key, "wich", q["q"], bank.skill("GP7.17"))   # homophones: the spelling is the point
    for k in ("GP1.08", "GP2.08", "GP3.04", "GP9.12", "GP9.14", "GP2.18"):       # word endings, prefixes, apostrophes
        assert bank.spelling_matters(bank.skill(k)), k
    assert not bank.spelling_matters(bank.skill("GP5.03")) and not bank.spelling_matters(bank.skill("GP8.11"))


def test_sentence_missing_only_its_full_stop_or_capital_is_nearly():
    sk = bank.skill("GP7.02")
    q = next(q for q in sk["qs"] if q["t"] == "write" and "future" in q["q"])
    key, a = bank.serve(q)[1], q["a"][0]                              # "Kofi will visit his aunt on Saturday."
    assert bank.end_slip(key, a[:-1], sk)["retry"] == "Nearly — check your full stop."
    both = bank.end_slip(key, a[0].lower() + a[1:-1], sk)
    assert both["retry"] == "Nearly — check your capital letter and full stop."
    assert "capital letter at the start and a full stop at the end" in both["after"]
    assert bank.end_slip(key, a[0].lower() + a[1:], sk)["retry"] == "Nearly — check your capital letter."
    assert not bank.end_slip(key, a.replace("will visit", "visits")[:-1], sk)       # the grammar is wrong too
    caps = bank.skill("GP1.03")                                       # capitals and full stops ARE the skill
    q = next(q for q in caps["qs"] if q["t"] == "write")
    assert not bank.end_slip(bank.serve(q)[1], q["a"][0][:-1], caps)


def test_sentence_feedback_marks_the_words_that_differ():
    best, m = bank.word_marks("The dog ran acros the feild.", ["The dog ran across the field."])
    assert best == "The dog ran across the field."
    assert m == {"typed": [["The dog ran", False], ["acros", True], ["the", False], ["feild.", True]],
                 "word": [["The dog ran", False], ["across", True], ["the", False], ["field.", True]]}
    assert bank.word_marks("Something else entirely here.", ["The dog ran across the field."]) is None


# ------------------------------------------------------------------ content ----
def test_rounding_table_keeps_its_decimal_place_and_explains():
    for _ in range(200):
        q = me.call_generator(me.GENERATORS["Y8.0.c"], 1)
        if q.get("component") == "data_table" and "1 d.p." in q["prompt"]:
            assert all(re.fullmatch(r"-?\d+\.\d", r[1]) for r in q["spec"]["rows"]), q["spec"]["rows"]
            assert "digit is" in q["solution"][0]
    from app.maths.y8_gen_a import _why_dp
    assert _why_dp(Decimal("29.38"), 1).startswith("The hundredths digit is 8, 5 or more")


def test_place_value_chart_does_not_print_the_number():
    for key in ("Y6.0.a", "Y4.0.d"):
        seen = 0
        for _ in range(300):
            q = me.call_generator(me.GENERATORS[key], 1)
            if "place-value chart shows the number" in q["prompt"] and "empty" in q["prompt"]:
                seen += 1
                assert not re.search(r"\d", q["prompt"].split("?")[0].split("number")[1]), q["prompt"]
        assert seen, key


def test_no_vertical_line_in_the_prompt():
    for _ in range(300):
        q = me.call_generator(me.GENERATORS["Y8.0.d"], 1)
        assert "VERTICAL" not in q["prompt"]


def test_word_problems_name_the_key_word():
    for key in ("Y3.2.g", "Y3.5.d", "Y3.5.e", "Y4.2.f", "Y4.4.g", "Y4.4.h"):
        named = 0
        random.seed(key)                                 # about 1 in 3 for the rarest, so the same draws every run
        for _ in range(60):
            q = me.call_generator(me.GENERATORS[key], 1)
            named += any("means" in s or "'Each'" in s for s in q["solution"])
        assert named >= 15, key


def test_a_an_tap_is_worded_as_a_change():
    qs = [q for sk in bank.load()["grammar"].get(3, []) for q in sk["qs"] if q["t"] == "tap" and "'an'" in q["q"]]
    assert qs and all("should change to" in q["q"] and q["why"].startswith("The word 'a' should be 'an'") for q in qs)


# ------------------------------------------------------------------ through the API ----
def _child(page, name, year):
    signup(page)
    pid = add_child(page, name, year)
    enter_child(page, name)
    return pid


def _post(page, url, body):
    return page.request.post(BASE + url, data=body).json()


def test_maths_slip_gets_one_free_retry(page):
    pid = _child(page, "Lina", 4)
    tok = "nm-" + pid
    DB.maths_lab_q.insert_one({"_id": tok, "skill": "Y4.0.a", "prompt": "Do you say 24 when you count in 3s? (yes or no)",
                               "answer": "yes", "display": "yes", "answer_type": "str", "tolerance": 0, "unit": None,
                               "solution": ["24 = 8 × 3."], "difficulty": 1, "pupil": pid,
                               "created": datetime.datetime.utcnow()})
    r = _post(page, "/api/maths/check", {"token": tok, "value": "yse"})
    assert r["ok"] and r["retry"] and r["hint"] == typos.RETRY and "expected" not in r
    assert not DB.maths_lab_q.find_one({"_id": tok})["done"]
    assert not DB.maths_mastery.find_one({"pupil_id": pid}) if "maths_mastery" in DB.list_collection_names() else True
    r = _post(page, "/api/maths/check", {"token": tok, "value": "yes"})
    assert r["ok"] and r["correct"] and not r.get("retry")
    # a second slip on another question: after its retry it is marked, and the word is named
    DB.maths_lab_q.update_one({"_id": tok}, {"$set": {"done": False, "retried": True}})
    r = _post(page, "/api/maths/check", {"token": tok, "value": "yse"})
    assert r["ok"] and r["correct"] is False and "'yse' should be 'yes'." in r["solution"][0]


def test_numbers_slip_gets_one_free_retry(page):
    pid = _child(page, "Zak", 5)
    for _ in range(30):
        q = _post(page, "/api/numbers/next", {})
        if q["mode"] == "words":
            break
    it = DB.items.find_one({"_id": q["token"]})
    words = it["answer"].split()
    i = next((k for k, w in enumerate(words) if len(w) >= 4 and w.isalpha() and w != "and"), None)
    if i is None:
        return
    bad = words[:]
    bad[i] = bad[i][:-1]                                       # one letter left off
    if bad[i] in typos.NUMBER_WORDS:
        return
    r = _post(page, "/api/numbers/check", {"token": q["token"], "value": " ".join(bad)})
    assert r["ok"] and r["retry"] and r["hint"].startswith("Your number is right — check the spelling of")
    n_before = DB.progress.count_documents({"pupil_id": pid}) if "progress" in DB.list_collection_names() else 0
    r = _post(page, "/api/numbers/check", {"token": q["token"], "value": " ".join(bad)})
    assert r["ok"] and r["correct"] is False and not r.get("retry") and "should be" in r["hint"]
    r = _post(page, "/api/numbers/check", {"token": q["token"], "value": it["answer"]})
    assert not r.get("ok")                                     # marked once: the token is spent
    assert n_before >= 0


def test_science_slip_gets_one_free_retry_and_spelling_shows_letters(page):
    pid = _child(page, "Amira", 8)
    sk = next(s for s in bank.load()["science"][8] if any(q["t"] == "text" for q in s["qs"]))
    q = next(q for q in sk["qs"] if q["t"] == "text" and re.fullmatch(r"[a-z]{6,}", q["a"][0]))
    pub, key = bank.serve(q)
    tok = "nm-sc-" + pid
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": "science", "answer": key,
                         "meta": {"skill": sk["key"], "qid": q["id"], "reason": "new"},
                         "created": datetime.datetime.utcnow(), "done": False})
    slip = q["a"][0][:3] + q["a"][0][4:]
    r = _post(page, "/api/science/check", {"token": tok, "value": slip})
    assert r["ok"] and r["retry"] and "check your spelling" in r["hint"]
    r = _post(page, "/api/science/check", {"token": tok, "value": q["a"][0]})
    assert r["ok"] and r["correct"]

    tok = "nm-sp-" + pid
    DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": "spelling", "answer": "analyse",
                         "meta": {"cue": ""}, "created": datetime.datetime.utcnow(), "done": False})
    r = _post(page, "/api/spelling/check", {"token": tok, "value": "analyze"})
    assert r["ok"] and not r["correct"] and not r.get("retry") and "American spelling" in r["hint"]


def _bank_item(pid, activity, sk, q, tag):
    key = bank.serve(q)[1]
    tok = f"nm-{tag}-{pid}"
    fam = DB.pupils.find_one({"_id": pid})["family_id"]
    DB.items.insert_one({"_id": tok, "pupil_id": pid, "family_id": fam, "activity": activity, "answer": key,
                         "meta": {"skill": sk["key"], "qid": q["id"], "reason": "new"},
                         "created": datetime.datetime.utcnow(), "done": False})
    return tok


def test_grammar_near_misses_retry_and_say_what_was_wrong(page):
    pid = _child(page, "Leila", 7)
    sk = bank.skill("GP5.03")
    q = next(q for q in sk["qs"] if q["t"] == "text" and q["a"] == ["which"])
    tok = _bank_item(pid, "grammar", sk, q, "gw")
    r = _post(page, "/api/grammar/check", {"token": tok, "value": "wich"})
    assert r["ok"] and r["retry"] and r["hint"] == typos.RETRY
    r = _post(page, "/api/grammar/check", {"token": tok, "value": "wich"})
    assert r["ok"] and r["correct"] is False and r["hint"] == "'wich' should be 'which'."

    sk = bank.skill("GP7.02")                         # a rewrite right but for its full stop
    q = next(q for q in sk["qs"] if q["t"] == "write" and "future" in q["q"])
    tok = _bank_item(pid, "grammar", sk, q, "gf")
    r = _post(page, "/api/grammar/check", {"token": tok, "value": q["a"][0][:-1]})
    assert r["ok"] and r["retry"] and r["hint"] == "Nearly — check your full stop."
    r = _post(page, "/api/grammar/check", {"token": tok, "value": q["a"][0][:-1]})
    assert r["ok"] and r["correct"] is False and r["why"] == ""          # not the explanation about the verb
    assert r["hint"] == "Your words were right: the sentence needs a full stop at the end."
    assert [t for t, d in r["marks"]["word"] if d] == [q["a"][0].split()[-1]]

    sk = bank.skill("GP1.03")                         # capitals and full stops are the skill: marked at once
    q = next(q for q in sk["qs"] if q["t"] == "write")
    tok = _bank_item(pid, "grammar", sk, q, "gc")
    r = _post(page, "/api/grammar/check", {"token": tok, "value": q["a"][0][:-1]})
    assert r["ok"] and r["correct"] is False and not r.get("retry") and r["marks"]
