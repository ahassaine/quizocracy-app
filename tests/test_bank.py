"""The grammar and science banks: every question can be served without its answer and marked both ways,
every year has a bank, and the skill picker behaves (no server needed)."""
import datetime
import random

import pytest

from app.bank import engine
from app.drills.bank import PLATEAU_ATTEMPTS, WINDOW, pick_question, pick_skill

SUBJECTS = ("grammar", "science")
ALL = [(sub, sk, q) for sub in SUBJECTS for yr in engine.load()[sub].values() for sk in yr for q in sk["qs"]]


def right_value(key):
    return {"mcq": lambda: key["right"], "tap": lambda: key["hits"], "text": lambda: key["a"][0],
            "write": lambda: key["a"][0], "num": lambda: key["a"]}[key["t"]]()


def wrong_value(key, q):
    t = key["t"]
    if t == "mcq":
        return (key["right"] + 1) % len(key["opts"])
    if t == "tap":
        others = [i for i in range(len(key["words"])) if i not in key["hits"]]
        return others[:1] or []
    if t == "text":
        return "zzqx"
    if t == "write":
        return q["s"]
    return key["a"] + (key.get("tol") or 0) + 1


@pytest.mark.parametrize("sub", SUBJECTS)
def test_every_year_has_a_bank(sub):
    years = engine.load()[sub]
    assert sorted(years) == list(range(1, 10)), sorted(years)
    for y, skills in years.items():
        assert len(skills) >= 8, (sub, y, len(skills))
        assert all(len(s["qs"]) >= 20 for s in skills), [(s["key"], len(s["qs"])) for s in skills if len(s["qs"]) < 20]


def test_question_ids_are_unique():
    ids = [(sk["key"], q["id"]) for _, sk, q in ALL]
    assert len(ids) == len(set(ids))


def test_every_question_marks_right_and_wrong():
    bad = []
    for sub, sk, q in ALL:
        for _ in range(2):                                   # two shuffles
            pub, key = engine.serve(q)
            leak = {"a", "right", "hits", "why"} & set(pub)
            if leak:
                bad.append((sk["key"], q["q"], "leaks " + str(leak)))
            if not engine.mark(key, right_value(key)):
                bad.append((sk["key"], q["q"], "right answer marked wrong"))
            if engine.mark(key, wrong_value(key, q)):
                bad.append((sk["key"], q["q"], "wrong answer marked right"))
            if not engine.expected_text(key).strip():
                bad.append((sk["key"], q["q"], "no answer to show"))
    assert not bad, bad[:20]


def test_marking_rules():
    k = {"t": "text", "a": ["evaporation"]}
    assert engine.mark(k, " Evaporation. ") and engine.mark(k, "evaporation?") and not engine.mark(k, "condensation") and not engine.mark(k, "")
    k = {"t": "text", "a": ["the axle", "pivot"], "loose": True}           # science: an article may be left off or added
    assert engine.mark(k, "axle") and engine.mark(k, "an axle") and engine.mark(k, "The pivot") and not engine.mark(k, "the")
    assert not engine.mark({"t": "text", "a": ["the dog"]}, "dog")             # grammar: the article counts
    k = {"t": "write", "a": ["Sam's dog can't swim."]}
    assert engine.mark(k, "Sam’s dog can’t  swim.")             # curly apostrophes, double space
    assert not engine.mark(k, "sam's dog can't swim.")                     # capitals count
    assert not engine.mark(k, "Sam's dog can't swim")                      # so does the full stop
    k = {"t": "num", "a": 12.5, "tol": 0.05}
    assert engine.mark(k, "12.5 m/s") and engine.mark(k, "12.53") and not engine.mark(k, "12.6")
    assert engine.mark({"t": "num", "a": 1000}, "1,000") and not engine.mark({"t": "num", "a": 3}, "abc")
    assert engine.mark({"t": "num", "a": 0}, 0) and engine.mark({"t": "num", "a": 0}, "0") and not engine.mark({"t": "num", "a": 0}, "")
    words, hits = engine.tap_parse("The dog ran [quickly], then [stopped].")
    assert words[3] == "quickly," and hits == [3, 5]
    k = {"t": "tap", "hits": [3, 5], "words": words}
    assert engine.mark(k, [5, 3]) and not engine.mark(k, [3]) and not engine.mark(k, [3, 5, 0])
    k = {"t": "mcq", "right": 2, "opts": ["a", "b", "c"]}
    assert engine.mark(k, 2) and engine.mark(k, "2") and not engine.mark(k, 0) and not engine.mark(k, "x")


def _sk(i, n=20):
    return {"key": "GP3.%02d" % i, "title": str(i), "strand": "s", "qs": [{"id": "%d-%d" % (i, j)} for j in range(n)]}


def test_picker_interleaves_a_window_then_moves_on():
    skills = [_sk(i) for i in range(1, 8)]
    now = datetime.datetime.utcnow()
    mm, used = {}, []
    for step in range(30):
        s, _ = pick_skill(skills, mm, random.Random(step))
        used.append(s["key"])
        mm[s["key"]] = {"score": 50, "attempts": mm.get(s["key"], {}).get("attempts", 0) + 1,
                        "last": now + datetime.timedelta(seconds=step)}
    assert set(used) == {s["key"] for s in skills[:WINDOW]}            # only the first window
    mm[skills[0]["key"]]["score"] = 100                 # first skill mastered (just now, so not due for review)
    s, _ = pick_skill(skills, mm, random.Random(0))
    assert s["key"] == skills[WINDOW]["key"]            # the window slides on to the next, never-practised skill
    assert skills[0]["key"] not in {pick_skill(skills, mm, random.Random(i))[0]["key"] for i in range(50)}


def test_picker_steps_past_a_plateau_and_reviews_when_all_mastered():
    skills = [_sk(i) for i in range(1, 6)]
    old = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    mm = {skills[0]["key"]: {"score": 30, "attempts": PLATEAU_ATTEMPTS, "last": old}}
    window = {pick_skill(skills, mm, random.Random(i))[0]["key"] for i in range(20)}
    assert window and skills[0]["key"] not in window                     # the stalled skill steps aside
    assert window <= {s["key"] for s in skills[1:WINDOW + 1]}
    mm = {s["key"]: {"score": 100, "attempts": 9, "last": old} for s in skills}
    s, why = pick_skill(skills, mm, random.Random(1))
    assert why == "review"


def test_question_picker_avoids_repeats():
    sk = _sk(1, 20)
    seen = []
    for i in range(20):
        q = pick_question(sk, seen, random.Random(i))
        assert q["id"] not in seen
        seen.append(q["id"])
    q = pick_question(sk, seen, random.Random(99))                       # all seen: not one of the last 3
    assert q["id"] not in seen[-3:]
