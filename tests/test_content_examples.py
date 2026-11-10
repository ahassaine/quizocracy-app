"""Content and selection fixes from the third family wave (no server needed): a format example never gives the
answer away, Year 7 meets directed numbers only in strand 7.6, older children don't open a skill with Year-2-style
counting, and grammar and science extra practice takes the strands in turn."""
import asyncio
import concurrent.futures
import datetime
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills.bank import spread_strands  # noqa: E402
from app.maths import maths_engine as E  # noqa: E402
from app.maths import maths_mastery as mm  # noqa: E402

NUM = re.compile(r"-?\d+(?:[./:]\d+)*")


def _toks(s):
    return set(NUM.findall(str(s).replace(",", " ")))


def _questions(prefix="", tiers=(0, 1, 2), n=12):
    for s in E.SKILLS:
        if not s["key"].startswith(prefix):
            continue
        for d in tiers:
            for i in range(n):
                random.seed(hash((s["key"], d, i)))
                yield s["key"], d, E.present(E.call_generator(E.GENERATORS[s["key"]], d), s["key"])


def test_example_in_the_box_is_never_the_answer_or_part_of_it():
    bad = []
    for key, d, q in _questions():
        ph = (q.get("spec") or {}).get("placeholder")
        assert ph is None or isinstance(ph, str), (key, ph)              # never a solution list (Y8.3 slip)
        if not ph or not ph.lower().startswith("e.g."):
            continue
        ans, ex = str(q["answer"]), ph[4:]
        plain = lambda x: re.sub(r"[\s.…]+|,", "", x.lower())           # noqa: E731
        if plain(ex) == plain(ans) or (_toks(ex) & _toks(ans)) - _toks(q["prompt"]):
            bad.append((key, d, ph, ans, q["prompt"][:80]))
    assert not bad, bad[:10]


def test_neutral_examples_shapes():
    q = E.neutral_examples({"prompt": "Count forward in 10s from 655. Write the next three numbers.",
                            "answer": "665, 675, 685", "spec": {"placeholder": "e.g. 665, 675, ..."}})
    assert q["spec"]["placeholder"] == "numbers, with commas"
    q = E.neutral_examples({"prompt": "What must be added to 1/4 to make 1 whole?", "answer": "3/4",
                            "spec": {"placeholder": "e.g. 3/4"}})
    assert q["spec"]["placeholder"].startswith("e.g. ") and q["spec"]["placeholder"] != "e.g. 3/4"
    assert "/0" not in q["spec"]["placeholder"]
    q = E.neutral_examples({"prompt": "Write 8 : 12 in its simplest form. Type it like 2:3.", "answer": "2:3",
                            "spec": {"placeholder": "e.g. 2:3"}})
    assert "like 2:3" not in q["prompt"] and "like " in q["prompt"] and q["spec"]["placeholder"] != "e.g. 2:3"
    q = E.neutral_examples({"prompt": "Write it like 1/7.", "answer": "1", "spec": {}})
    assert q["prompt"] == "Write it like 1/7."                         # "like 1" is not "like 1/7"


def test_the_count_on_example_no_longer_shows_the_next_numbers():
    for _, _, q in _questions("Y3.0.a", n=60):
        if q["prompt"].startswith("Count forward in"):
            ph = q["spec"].get("placeholder", "")
            assert not (_toks(ph) & _toks(q["answer"])), (q["prompt"], ph, q["answer"])


BEFORE_76 = ("Y7.0.b", "Y7.0.c", "Y7.1.c", "Y7.1.d", "Y7.1.e", "Y7.2.a", "Y7.2.b", "Y7.2.c", "Y7.5.a", "Y7.5.g")


def test_year7_before_directed_numbers_has_no_negative_answers_or_inputs():
    for key, d, q in _questions(BEFORE_76, n=40):
        a = str(q["answer"]).strip()
        assert not a.startswith("-"), (key, d, q["prompt"], a)
        assert not re.search(r"x = -\d|C = -\d|\(−\d+\)[²³]|nth term -|multiply by -", q["prompt"]), (key, q["prompt"])


def test_year7_seven_less_than_n_and_negative_square_say_why():
    for _, _, q in _questions("Y7.1.a", n=80):
        if "less than" in q["prompt"]:
            assert "start at" in " ".join(q["solution"]) and "take" in " ".join(q["solution"]), q["solution"]
            break
    else:
        raise AssertionError("no 'less than' question met")
    for _, _, q in _questions("Y7.6.d", n=80):
        if q["prompt"].startswith("Find the value of x² when"):
            assert "a negative times a negative is positive" in " ".join(q["solution"]), q["solution"]
            break
    else:
        raise AssertionError("no negative square met")


def test_year7_sequences_never_open_with_times_table_counting():
    for _, d, q in _questions("Y7.0.a", tiers=(0, 1, 2), n=80):
        nums = [int(x) for x in re.findall(r"(?<![\d.])\d+(?![\d.])", q["prompt"])]
        run = [n for n in nums if n > 0]
        if len(run) >= 4:
            step = run[1] - run[0]
            assert not (step > 0 and all(n % step == 0 for n in run[:4]) and run[1:4] == [run[0] + step * k for k in (1, 2, 3)]), q["prompt"]


def test_hcf_tile_question_says_the_tiles_cover_the_rectangle():
    for _, _, q in _questions("Y6.2.a", n=120):
        if "tile" in q["prompt"]:
            assert "cover the whole rectangle" in q["prompt"] and "no gaps or overlaps" in q["prompt"], q["prompt"]
            return
    for _, _, q in _questions("Y6.2", n=60):
        assert "would fit into the rectangle exactly" not in q["prompt"], q["prompt"]


class _Coll:
    def __init__(self):
        self.docs = {}

    async def find_one(self, q):
        return self.docs.get(q["_id"])


class _DB:
    def __init__(self):
        self.maths_mastery = _Coll()


def _run(coro):
    with concurrent.futures.ThreadPoolExecutor(1) as ex:      # own thread: Playwright's loop may be running here
        return ex.submit(asyncio.run, coro).result()


def test_new_skills_from_year5_open_at_the_middle_tier(monkeypatch):
    db = _DB()
    monkeypatch.setattr(mm, "db", db)
    assert _run(mm.start_tier("p1", 7, "Y7.0.a", 0)) == 1           # new skill, Year 7: middle tier
    assert _run(mm.start_tier("p1", 5, "Y5.0.a", 0)) == 1
    assert _run(mm.start_tier("p1", 3, "Y3.0.a", 0)) == 0           # Year 3 keeps the easy start
    db.maths_mastery.docs["p1:Y7.0.a"] = {"attempts": 3, "correct_count": 1, "score": 10}
    assert _run(mm.start_tier("p1", 7, "Y7.0.a", 10)) == 0          # after wrong answers: easier questions
    db.maths_mastery.docs["p1:Y7.0.c"] = {"attempts": 3, "correct_count": 2, "score": 10}
    assert _run(mm.start_tier("p1", 7, "Y7.0.c", 10)) == 1          # one slip after two right: stays in the middle
    db.maths_mastery.docs["p1:Y7.0.b"] = {"attempts": 1, "correct_count": 1, "score": 23}
    assert _run(mm.start_tier("p1", 7, "Y7.0.b", 23)) == 1
    db.maths_mastery.docs["p1:Y7.0.b"] = {"attempts": 2, "correct_count": 2, "score": 35}
    assert _run(mm.start_tier("p1", 7, "Y7.0.b", 35)) == 2          # two right first time: the hardest tier
    assert _run(mm.start_tier("p1", 7, "Y7.0.b", 90)) == 2          # the score still hardens it


def test_extra_practice_takes_the_strands_in_turn_weakest_first():
    skills = [{"key": f"{st}{i}", "strand": st, "qs": [1]} for st in ("Words", "Punctuation", "Clauses") for i in range(3)]
    now = datetime.datetime.utcnow()
    mm_ = {"Words0": {"score": 60, "last": now}, "Words1": {"score": 40, "last": now - datetime.timedelta(minutes=1)}}
    first = spread_strands(skills, mm_)
    assert {s["strand"] for s in first} == {"Punctuation"} or {s["strand"] for s in first} == {"Clauses"}
    # the strand practised just now waits; of the others, the weaker goes first
    mm_.update({"Punctuation0": {"score": 70, "last": now - datetime.timedelta(minutes=5)},
                "Clauses0": {"score": 20, "last": now - datetime.timedelta(minutes=6)}})
    assert {s["strand"] for s in spread_strands(skills, mm_)} == {"Clauses"}
    seen = set()
    for _ in range(6):                     # practising the picked strand moves the turn on
        pick = spread_strands(skills, mm_)
        seen.add(pick[0]["strand"])
        now += datetime.timedelta(minutes=1)
        mm_[pick[0]["key"]] = {"score": mm_.get(pick[0]["key"], {}).get("score", 0) + 5, "last": now}
    assert seen == {"Words", "Punctuation", "Clauses"}, seen
