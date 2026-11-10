"""Wave 6, grammar and science: correct rewrites in a pupil's own good English, Year 9 punctuation, more variety
when the focus has few skills, "Nearly" for grammar terms and verb forms, the key-words glossary, "no" lines that
name the real slip, and friendly numbers in Years 7-9 science."""
import importlib
import random
import re

import pytest

from app.bank import engine, glossary
from app.drills import bank as drill

GP, SC = "grammar", "science"


def _write(sk, qid):
    q = engine.question(sk, qid)
    return q, engine.serve(q)[1]


# ------------------------------------------------------------------ rewrites in the pupil's own good English ----
@pytest.mark.parametrize("skill, qid, typed", [
    ("GP9.01", "b4b688a9b788", "I suggest she go to bed early."),                       # "that" left out
    ("GP9.01", "31ed67797fa5", "The teacher insisted Sam stay behind."),
    ("GP9.01", "b4b9d31701e3", "Were he taller, he could reach the shelf."),            # inverted subjunctive
    ("GP9.02", "a208af3a0ee9", "The late arrival of the train annoyed passengers."),
    ("GP9.15", "89557fa969d9", 'The writer describes the wind as "bitter" and "sharp".'),   # double quotes
    ("GP9.15", "89557fa969d9", "The writer describes the wind as ‘bitter’ and “sharp”."),   # curly, mixed
    ("GP8.05", "e6ec569c2a9d", "Kofi said he was tired."),                              # reported, no "that"
    ("GP8.05", "e6ec569c2a9d", "Kofi said that he was tired."),
    ("GP8.04", "116237d3cd80", "If I'd known, I would have helped."),
    ("GP7.06", "b409ee48d453", "Can you pass me these books?"),
])
def test_a_correct_rewrite_in_other_good_english_is_accepted(skill, qid, typed):
    q, key = _write(skill, qid)
    assert engine.mark(key, typed), (q["q"], typed)


def test_the_normaliser_keeps_what_the_task_is_about():
    q, key = _write("GP9.15", "f738a7c5b65a")          # "Move the full stop outside the quotation marks"
    assert not engine.mark(key, "The writer calls the forest 'endless.'")
    assert engine.mark(key, 'The writer calls the forest "endless".')
    k = {"t": "write", "a": ["I know that song well."], "prompt": "Correct it."}
    assert not engine.mark(k, "I know song well.")                       # "that" before a noun stays
    k = {"t": "write", "a": ["Kofi said that he was tired."], "prompt": "Rewrite, starting 'Kofi said that'."}
    assert not engine.mark(k, "Kofi said he was tired.")                  # the task names 'that'
    k = {"t": "write", "a": ["I tidied my whole room – or most of it."], "prompt": "Add a dash."}
    assert engine.mark(k, "I tidied my whole room—or most of it.") and engine.mark(k, "I tidied my whole room - or most of it.")


def test_every_reported_speech_task_lets_that_be_left_out():
    for q in engine.skill("GP8.05")["qs"]:
        if q["t"] == "write":
            assert "said that'" not in q["q"], q["q"]


# ------------------------------------------------------------------ "no" lines that name the real slip ----
def test_should_is_named_as_good_english_but_not_the_subjunctive():
    q, key = _write("GP9.01", "31ed67797fa5")
    no, why = engine.why_lines(q, key, "The teacher insisted that Sam should stay behind.")
    assert "'should stay' is good English, but it is not the subjunctive" in no and "'stay'" in no
    q = engine.question("GP9.01", "3bb25d857c91")
    no, _ = engine.why_lines(q, engine.serve(q)[1], "should be")
    assert "not the subjunctive" in no
    assert engine.why_lines({"q": "Rewrite in the passive."}, key, "The teacher insisted that Sam should stay behind.")[0] == ""


def test_a_real_unit_of_the_same_quantity_is_named():
    q = engine.question("SC9.40", "f8cf6dd787e3")      # What is the SI unit of density?
    key = engine.serve(dict(q, loose=True))[1]
    no, _ = engine.why_lines(q, key, "g/cm3")
    assert no.startswith("g/cm3 is a real unit of density, but it is not the SI unit") and "kg/m³" in no
    q = engine.question("SC9.44", "2cda7a585a83")      # What is the unit of power?
    no, _ = engine.why_lines(q, engine.serve(dict(q, loose=True))[1], "kW")
    assert "kW is a unit of power too" in no
    no, _ = engine.why_lines({"q": "?"}, {"t": "num", "a": 3, "unit": "g/cm³"}, "3000 kg/m3")
    assert "asks for g/cm³" in no
    assert engine.why_lines(q, engine.serve(dict(q, loose=True))[1], "newton")[0] == ""     # another quantity


# ------------------------------------------------------------------ "Nearly" for terms and verb forms ----
def test_a_slip_in_a_grammar_term_or_an_irregular_verb_form_gets_nearly():
    q = engine.question("GP7.01", "bd1c0669b83a")
    assert engine.slips(engine.serve(q)[1], "collectif noun", q["q"], engine.skill("GP7.01")) == [("collectif", "collective")]
    q = engine.question("GP7.02", "318e9b88213a")
    assert engine.slips(engine.serve(q)[1], "has writen", q["q"], engine.skill("GP7.02")) == [("writen", "written")]
    q = engine.question("GP7.10", "cf6f1cb787de")
    assert engine.slips(engine.serve(q)[1], "subordinat clause", q["q"], engine.skill("GP7.10"))


def test_where_the_spelling_is_the_skill_there_is_still_no_nearly():
    q = engine.question("GP7.03", "b99b6cd45ab8")      # comparative of 'thin': the doubling is the point
    assert engine.slips(engine.serve(q)[1], "thiner", q["q"], engine.skill("GP7.03")) == []
    q = engine.question("GP7.01", "a25c3042c680")      # abstract noun from 'brave'
    assert engine.slips(engine.serve(q)[1], "bravary", q["q"], engine.skill("GP7.01")) == []
    q = engine.question("GP7.01", "bd1c0669b83a")      # another real term is a real mistake
    assert engine.slips(engine.serve(q)[1], "abstract noun", q["q"], engine.skill("GP7.01")) == []


# ------------------------------------------------------------------ Year 9 punctuation ----
def test_year_9_punctuation_has_semicolons_colons_dashes_and_comma_splices():
    keys = [s["key"] for s in engine.skills(GP, 9) if s["strand"] == "Punctuation"]
    assert {"GP9.04", "GP9.16", "GP9.17", "GP9.18", "GP9.19"} <= set(keys)
    order = [s["key"] for s in engine.skills(GP, 9)]
    assert order.index("GP9.16") == order.index("GP9.04") + 1          # taught straight after hyphens
    for k in ("GP9.16", "GP9.17", "GP9.18", "GP9.19"):
        sk = engine.skill(k)
        assert len(sk["qs"]) >= 20 and len({q["t"] for q in sk["qs"]}) >= 3, k
        assert all(q.get("why") for q in sk["qs"]), k
        assert sum(1 for q in sk["qs"] if q.get("no")) >= 5, k
    assert "34" not in engine.question("GP9.04", "90da7ad00354")["q"]   # no "Type 34 in words" in Year 9


# ------------------------------------------------------------------ more variety in a narrow focus ----
def _mm_after(picks):
    return {k: {"score": 10, "last": i} for i, k in enumerate(picks)}


def test_the_focus_share_goes_round_every_focus_skill_and_its_neighbours():
    skills = engine.skills(GP, 9)
    in_focus = engine.focus_skills(GP, 9, ["Punctuation", "Grammar for style"])
    pool = drill.focus_pool(skills, in_focus, {})
    assert pool == in_focus and len(pool) >= 8                        # enough of their own
    one = engine.focus_skills(GP, 9, ["Sentences for effect"])
    wide = drill.focus_pool(skills, one, {})
    assert len(wide) >= drill.FOCUS_MIN and {s["strand"] for s in wide} > {"Sentences for effect"}
    import datetime
    t0, mm, seen = datetime.datetime(2026, 1, 1), {}, []
    for i in range(16):                                               # the focus share alone, 16 questions
        sk, _ = drill.pick_skill(pool, mm, rnd=random.Random(i), width=len(pool))
        seen.append(sk["key"])
        mm[sk["key"]] = {"score": 10, "last": t0 + datetime.timedelta(minutes=i)}
    assert len(set(seen)) == len(pool)                                # every focus skill came round


def test_never_more_than_three_in_a_row_from_one_skill():
    sk = engine.skills(GP, 9)[:2]
    pick, _ = drill.pick_skill(sk, {}, avoid_skill=sk[0]["key"], width=1)
    assert pick["key"] != sk[0]["key"]


# ------------------------------------------------------------------ the key-words glossary ----
def test_the_glossary_is_hand_sized_and_plain():
    terms = {**glossary.TERMS[GP], **glossary.TERMS[SC]}
    assert 150 <= len(glossary.TERMS[GP]) + len(glossary.TERMS[SC]) <= 250
    for subject in (GP, SC):
        for t, line in glossary.TERMS[subject].items():
            assert t == t.lower() and line.endswith((".", "?", "!")) and len(line.split()) <= 22, t
            assert not re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t), line.lower()), t
    for must in ("filtrate", "residue", "solute", "solvent", "control variable"):
        assert must in glossary.TERMS[SC]
    for must in ("determiner", "adverbial", "subjunctive", "comma splice"):
        assert must in glossary.TERMS[GP]
    assert terms


def test_key_words_are_found_but_never_give_the_answer_away():
    kw = engine.key_words(SC, ["Evaporate the filtrates; keep the residue."])
    assert set(kw) == {"filtrate", "residue"}
    assert set(engine.key_words(GP, ["Add a semi-colon, not a colon."])) == {"semi-colon", "colon"}
    q = {"t": "mcq", "q": "What is a control variable?", "opts": ["A variable kept the same", "The one you change"]}
    assert "control variable" not in engine.key_words(SC, [q["q"]], q)
    q = {"t": "tap", "q": "Tap the determiner.", "s": "We go swimming [every] Friday."}
    assert "determiner" not in engine.key_words(GP, [q["q"]], q)   # its line lists 'every'
    q = {"t": "text", "q": "What do we call a noun that names a group?", "a": ["collective noun"]}
    assert "noun" in engine.key_words(GP, [q["q"]], q)
    # every question of Years 3-9: a term shown before the answer never has the answer in its line
    for subject in (GP, SC):
        for y in range(3, 10):
            for sk in engine.skills(subject, y):
                for q in sk["qs"]:
                    if q["t"] not in ("text", "mcq"):
                        continue
                    answers = [q["opts"][0]] if q["t"] == "mcq" else [str(a) for a in q["a"]]
                    for t, line in engine.key_words(subject, [q["q"]], q).items():
                        for a in answers:
                            a = engine.norm_text(a)
                            assert len(a) < 4 or not re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(a), line.lower()), (sk["key"], q["q"], t)


def test_each_strand_has_its_key_words_for_the_parent():
    by = {}
    for s in engine.skills(SC, 7):
        by.setdefault(s["strand"], []).append(s)
    lists = {st: engine.strand_key_words(SC, sks) for st, sks in by.items()}
    assert sum(1 for v in lists.values() if v) >= len(lists) * 0.8
    mixtures = next(v for st, v in lists.items() if "ixture" in st or "eparat" in st)
    assert "filtrate" in dict(mixtures) or "solute" in dict(mixtures)


# ------------------------------------------------------------------ friendly numbers in Years 7-9 science ----
def test_years_7_to_9_science_sums_have_whole_or_one_decimal_answers():
    for y in (7, 8, 9):
        for sk in importlib.import_module(f"app.bank.content.science_y{y}").SKILLS:
            for q in sk["qs"]:
                if q["t"] == "num":
                    assert round(q["a"], 1) == q["a"], (sk["key"], q["q"], q["a"])


# ------------------------------------------------------------------ on the page ----
def test_a_key_word_is_underlined_and_tapping_it_shows_its_meaning(browser):
    from conftest import BASE, DB, add_child, enter_child, signup
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Camille", 7)
    add_child(pg, "Ada", 2)
    enter_child(pg, "Camille")
    for _ in range(25):                         # science questions until one has a key word
        pg.goto("/me/science")
        pg.wait_for_function("document.body.dataset.qtoken && !document.getElementById('check').disabled")
        if pg.locator("#q [data-testid=kw]").count():
            break
        DB.items.delete_many({"pupil_id": pid, "done": False})
    kw = pg.locator("#q [data-testid=kw]").first
    assert kw.count(), "no key word in 25 Year 7 science questions"
    kw.click()
    pop = pg.get_by_test_id("kw-pop")
    assert pop.is_visible() and ":" in pop.inner_text() and len(pop.inner_text()) > 12
    pg.keyboard.press("Escape")
    assert pg.get_by_test_id("kw-pop").count() == 0
    # a Year 2 child gets no underlines (read-aloud instead)
    enter_child(pg, "Ada")
    import requests
    s = requests.Session()
    for c in pg.context.cookies():
        s.cookies.set(c["name"], c["value"])
    q = s.post(BASE + "/api/science/next", json={}).json()
    assert "terms" not in q
    pg.context.close()


def test_the_parent_sees_key_words_per_strand(browser):
    from conftest import BASE, add_child, signup
    pg = browser.new_context(base_url=BASE).new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Camille", 7)
    pg.goto(f"/children/{pid}")
    link = pg.get_by_test_id("keywords-link")
    assert link.count() >= 1
    pg.goto(f"/children/{pid}/keywords?subject=science")
    assert pg.get_by_test_id("keywords-strand").count() >= 5
    assert "filtrate" in pg.content()
    pg.goto(f"/children/{pid}/examples?subject=science&strand=" + __import__("urllib.parse").parse.quote(
        next(s["strand"] for s in engine.skills(SC, 7) if s["key"] == "SC7.31")))
    assert pg.get_by_test_id("strand-key-words").count() == 1
    pg.context.close()
