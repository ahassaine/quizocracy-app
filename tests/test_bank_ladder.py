"""Simulated pupils on every year of the grammar and science banks: a strong pupil masters the whole year,
a weak pupil is never held on one skill, and questions do not repeat while unseen ones remain."""
import datetime
import random

import pytest

from app.bank import engine
from app.drills.bank import pick_question, pick_skill
from app.maths.maths_mastery import MASTERED, gain, penalty

YEARS = [(sub, y) for sub in ("grammar", "science") for y in range(1, 10)]


def simulate(skills, p_right, steps, seed=0, hard=()):
    rnd = random.Random(seed)
    t0 = datetime.datetime(2026, 1, 1)
    mm, picks = {}, []
    for n in range(steps):
        sk, _ = pick_skill(skills, mm, rnd)
        d = mm.setdefault(sk["key"], {"score": 0, "streak": 0, "attempts": 0, "seen": []})
        q = pick_question(sk, d["seen"], rnd)
        p = 0.25 if sk["key"] in hard else p_right
        if rnd.random() < p:
            d["streak"] += 1
            d["score"] = min(MASTERED, d["score"] + gain(d["score"], d["streak"]))
        else:
            d["streak"] = 0
            d["score"] = max(0, d["score"] - penalty(d["score"]))
        d["attempts"] += 1
        d["last"] = t0 + datetime.timedelta(minutes=n)
        d["seen"] = (d["seen"] + [q["id"]])[-40:]
        picks.append((sk["key"], q["id"]))
    return mm, picks


@pytest.mark.parametrize("sub,year", YEARS)
def test_strong_pupil_masters_the_year(sub, year):
    skills = engine.skills(sub, year)
    mm, picks = simulate(skills, 0.95, steps=len(skills) * 14)
    done = sum(1 for s in skills if mm.get(s["key"], {}).get("score", 0) >= MASTERED)
    assert done == len(skills), (sub, year, done, len(skills))
    # no question twice in a row within a skill while it still had unseen ones
    for k in {s["key"] for s in skills}:
        ids = [q for key, q in picks if key == k]
        n = len(engine.skill(k)["qs"])
        assert len(set(ids[:n])) == min(len(ids), n), (k, ids[:n])


@pytest.mark.parametrize("sub,year", YEARS)
def test_weak_pupil_is_never_trapped(sub, year):
    skills = engine.skills(sub, year)
    hard = {skills[0]["key"], skills[1]["key"]}               # two skills the pupil keeps getting wrong
    dones = []
    for seed in (3, 4, 5):        # the median of three runs: one unlucky run of a random pupil is not a trap
        mm, picks = simulate(skills, 0.8, steps=len(skills) * 25, seed=seed, hard=hard)
        touched = {k for k, _ in picks}
        assert touched == {s["key"] for s in skills}, (sub, year, len(touched), len(skills))
        dones.append(sum(1 for s in skills if mm.get(s["key"], {}).get("score", 0) >= MASTERED))
    assert sorted(dones)[1] >= len(skills) - len(hard) - 2, (sub, year, dones, len(skills))
