"""Practice for the Year 1 phonics screening check (England, June of Year 1; again in Year 2 for a child who did not
reach the standard). As in the real check, the child reads words aloud to a grown-up, who marks each one: real
words and "alien" (made-up) words, an alien beside each made-up one, section 1 simpler than section 2. The app
cannot hear, so the grown-up taps right or not; nothing is marked by the app.

The full check is 40 words (20 in each section, 20 alien words in all); a short practice is 20. In past years the
expected standard has been 32 of the 40.
"""
import datetime
import random

from ..db import db
from .. import items, progress

YEARS = (1, 2)
SIZES = (20, 40)
STANDARD = 32             # of 40, in past years
KEEP = 60


def open_to(pupil: dict) -> bool:
    return int(pupil.get("year") or 0) in YEARS


def _lists():
    from ..bank import phonics_check_words as w
    return w.SECTION1_REAL, w.SECTION1_ALIEN, w.SECTION2_REAL, w.SECTION2_ALIEN


def words(size: int, rng=random) -> list:
    """[{"w": word, "alien": bool, "section": 1 or 2}]: each section half real, half alien (the real check starts
    each section with its alien words); `size` words in all."""
    r1, a1, r2, a2 = _lists()
    q = size // 4
    out = []
    for sec, real, alien in ((1, r1, a1), (2, r2, a2)):
        out += [{"w": w, "alien": True, "section": sec} for w in rng.sample(alien, q)]
        out += [{"w": w, "alien": False, "section": sec} for w in rng.sample(real, q)]
    return out


def history(pupil: dict) -> list:
    return list(pupil.get("phonics_checks") or [])


async def start(pupil: dict, size: int) -> dict | None:
    if not open_to(pupil) or size not in SIZES:
        return None
    ws = words(size)
    token = await items.issue(pupil, "phonics_check", ws, {"size": size})
    return {"token": token, "words": ws, "size": size}


async def finish(pupil: dict, token: str, marks: list) -> dict | None:
    """marks: True (read right), False (not), per word, in order. The same check sent again gets its result."""
    it = await items.claim(pupil, "phonics_check", token)
    if not it:
        old = await items.peek(pupil, "phonics_check", token)
        return old.get("result") if old and old.get("result") else None
    ws = it["answer"]
    marks = [m is True for m in (marks if isinstance(marks, list) else [])][:len(ws)]
    marks += [False] * (len(ws) - len(marks))
    score = sum(marks)
    missed = [w for w, m in zip(ws, marks) if not m]
    row = {"day": progress.today(), "at": datetime.datetime.utcnow(), "score": score, "of": len(ws),
           "real_missed": [w["w"] for w in missed if not w["alien"]], "alien_missed": [w["w"] for w in missed if w["alien"]],
           "s1": sum(m for w, m in zip(ws, marks) if w["section"] == 1), "s2": sum(m for w, m in zip(ws, marks) if w["section"] == 2)}
    before = history(pupil)
    best = max((r["score"] / r["of"] for r in before), default=None)
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$push": {"phonics_checks": {"$each": [row], "$slice": -KEEP}}})
    result = {**{k: v for k, v in row.items() if k != "at"}, "best": best is not None and score / len(ws) > best,
              "first": best is None, "standard": STANDARD if len(ws) == 40 else STANDARD // 2}
    await db.items.update_one({"_id": it["_id"]}, {"$set": {"result": result}})
    return result
