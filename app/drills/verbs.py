"""Irregular verbs: type the past simple and the past participle. Levels of ~20 verbs."""
import random

from ..db import db
from .. import items, progress
from ..verbs_data import BUCKETS

LEVELS = BUCKETS[:-1]          # the last bucket in the family data is an all-verbs final check
MASTER_STREAK = 2


def _norm(s: str) -> str:
    return " ".join(str(s or "").strip().lower().split())


async def _state(pupil: dict) -> dict:
    st = await db.verbs_state.find_one({"_id": pupil["_id"]})
    if not st:
        st = {"_id": pupil["_id"], "pupil_id": pupil["_id"], "family_id": pupil["family_id"], "level": 0, "streaks": {}}
        await db.verbs_state.insert_one(st)
    return st


def _level_done(st: dict, level: int) -> bool:
    return all(st["streaks"].get(v["base"], 0) >= MASTER_STREAK for v in LEVELS[level]["verbs"])


async def next_question(pupil: dict) -> dict:
    st = await _state(pupil)
    level = min(st["level"], len(LEVELS) - 1)
    verbs = LEVELS[level]["verbs"]
    todo = [v for v in verbs if st["streaks"].get(v["base"], 0) < MASTER_STREAK] or verbs
    v = random.choice(todo)
    token = await items.issue(pupil, "verbs", {"past": v["past"], "pp": v["pp"]}, {"base": v["base"], "level": level})
    return {"token": token, "base": v["base"], "level": level + 1, "levels": len(LEVELS),
            "level_label": LEVELS[level]["label"]}


async def check(pupil: dict, token: str, past: str, pp: str, ms: int | None) -> dict | None:
    it = await items.claim(pupil, "verbs", token)
    if not it:
        return None
    ok_past = _norm(past) in it["answer"]["past"]
    ok_pp = _norm(pp) in it["answer"]["pp"]
    correct = ok_past and ok_pp
    base = it["meta"]["base"]
    st = await _state(pupil)
    streak = st["streaks"].get(base, 0) + 1 if correct else 0
    st["streaks"][base] = streak
    upd = {f"streaks.{base}": streak}
    levelled = False
    if correct and st["level"] < len(LEVELS) - 1 and _level_done(st, st["level"]):
        upd["level"] = st["level"] + 1
        levelled = True
    await db.verbs_state.update_one({"_id": pupil["_id"]}, {"$set": upd})
    await progress.record(pupil, "verbs", correct, ms, base, "Past forms of %s" % base,
                          "%s, %s" % (it["answer"]["past"][0], it["answer"]["pp"][0]), "%s, %s" % (past or "", pp or ""))
    return {"correct": correct, "ok_past": ok_past, "ok_pp": ok_pp,
            "expected": {"past": it["answer"]["past"][0], "pp": it["answer"]["pp"][0]}, "levelled_up": levelled}


async def summary(pupil: dict) -> dict:
    st = await _state(pupil)
    mastered = sum(1 for v in st["streaks"].values() if v >= MASTER_STREAK)
    return {"level": st["level"] + 1, "levels": len(LEVELS), "mastered": mastered,
            "total": sum(len(b["verbs"]) for b in LEVELS)}
