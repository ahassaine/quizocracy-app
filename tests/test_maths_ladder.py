"""Simulated pupils walk every year's ladder: a strong pupil reaches every skill and masters the year,
a weak one is never trapped on one skill, and Years 8-9 keep earlier KS3 skills in the mix."""
import asyncio
import collections
import concurrent.futures
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_mastery as mm  # noqa: E402


class _Cursor:
    def __init__(self, docs):
        self.docs = list(docs)

    def __aiter__(self):
        self._it = iter(self.docs)
        return self

    async def __anext__(self):
        try:
            return next(self._it)
        except StopIteration:
            raise StopAsyncIteration


class _Coll:
    def __init__(self):
        self.docs = {}

    def find(self, q):
        return _Cursor(d for d in self.docs.values() if d.get("pupil") == q.get("pupil"))

    async def find_one(self, q):
        return self.docs.get(q["_id"])

    async def update_one(self, q, upd, upsert=False):
        self.docs.setdefault(q["_id"], {"_id": q["_id"]}).update(upd["$set"])

    async def insert_one(self, doc):
        pass


class _DB:
    def __init__(self):
        self.maths_mastery, self.maths_attempts = _Coll(), _Coll()


def _walk(monkeypatch, year, p_right, steps, seed):
    random.seed(seed)
    monkeypatch.setattr(mm, "db", _DB())
    seen, keys = collections.Counter(), []

    async def go():
        for _ in range(steps):
            key, _reason = await mm.next_skill("sim", year)
            seen[key] += 1
            keys.append(key)
            await mm.record_attempt("sim", key, random.random() < p_right)
        return await mm.progress("sim", year)
    with concurrent.futures.ThreadPoolExecutor(1) as ex:      # own thread: Playwright's loop may be running here
        return ex.submit(asyncio.run, go()).result(), seen, keys


def test_strong_pupil_masters_every_year(monkeypatch):
    for year in range(1, 10):
        own = [s["key"] for s in mm._year_skills(year)]
        prog, seen, _ = _walk(monkeypatch, year, 0.95, 40 * len(own), seed=year)
        missed = [k for k in own if not seen[k]]
        assert not missed, (year, missed[:10])
        assert prog["pct"] >= 95, (year, prog["pct"])


def test_weak_pupil_is_never_trapped(monkeypatch):
    for year in range(1, 10):
        _, seen, keys = _walk(monkeypatch, year, 0.35, 1500, seed=100 + year)
        top, n = seen.most_common(1)[0]
        assert n < 0.4 * len(keys), (year, top, n)
        first = [s["key"] for s in mm._year_skills(year) if s["strand"] == mm._year_skills(year)[0]["strand"]]
        assert all(seen[k] for k in first), (year, [k for k in first if not seen[k]])
        longest, run = 1, 1
        for a, b in zip(keys, keys[1:]):
            run = run + 1 if a == b else 1
            longest = max(longest, run)
        assert longest <= 60, (year, longest)


def test_ks3_years_mix_in_earlier_ks3(monkeypatch):
    for year, earlier in ((8, ("Y7.",)), (9, ("Y7.", "Y8."))):
        _, seen, keys = _walk(monkeypatch, year, 0.8, 1500, seed=year)
        mixed = sum(n for k, n in seen.items() if k.startswith(earlier))
        assert 0.08 * len(keys) < mixed < 0.25 * len(keys), (year, mixed)
        assert all(k.startswith(("Y%d." % year,) + earlier) for k in seen), year
    _, seen, _ = _walk(monkeypatch, 7, 0.8, 600, seed=7)
    assert all(k.startswith("Y7.") for k in seen)


def _run(monkeypatch, coro_fn):
    monkeypatch.setattr(mm, "db", _DB())
    with concurrent.futures.ThreadPoolExecutor(1) as ex:
        return ex.submit(asyncio.run, coro_fn()).result()


def test_right_first_time_secures_a_skill_in_five(monkeypatch):
    async def go():
        scores = [(await mm.record_attempt("sim", "Y6.0.a", True))["score"] for _ in range(5)]
        slip = [(await mm.record_attempt("sim", "Y6.1.a", ok))["score"] for ok in (False, True, True, True, True, True)]
        return scores, slip
    scores, slip = _run(monkeypatch, go)
    assert scores[-1] == mm.MASTERED and scores[-2] < mm.MASTERED, scores
    assert slip[-1] < mm.MASTERED, slip                     # one slip: the usual, longer road


def test_a_strong_pupil_meets_several_strands_and_skips_ahead(monkeypatch):
    for year in (4, 6, 8):
        random.seed(year)

        async def go():
            keys = []
            for _ in range(30):
                key, reason = await mm.next_skill("sim", year)
                tier = await mm.start_tier("sim", year, key, await mm.skill_score("sim", key))
                if reason == "new" and await mm.probe("sim", year, key):
                    tier = 2                               # as drills/maths does: hard questions open it
                keys.append(key)
                await mm.record_attempt("sim", key, True, tier=tier)
            return keys
        keys = _run(monkeypatch, go)
        strands = {k.rsplit(".", 1)[0] for k in keys if k.startswith("Y%d." % year)}
        assert len(strands) >= 4, (year, strands)
        # placement: 2 hard questions right in a row secure a skill (never one)
        assert len(set(keys)) >= 9, (year, len(set(keys)), keys)


def test_skills_done_elsewhere_today_wait(monkeypatch):
    async def go():
        return [await mm.next_skill("sim", 5, avoid=mm.NUMBER_WORDS) for _ in range(20)]
    picks = _run(monkeypatch, go)
    assert not {k for k, _ in picks} & mm.NUMBER_WORDS
