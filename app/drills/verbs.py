"""Irregular verbs: type the past simple and the past participle. Levels of ~20 verbs."""
import random

from ..db import db
from .. import items, progress
from ..verbs_data import BUCKETS

LEVELS = BUCKETS[:-1]          # the last bucket in the family data is an all-verbs final check
MASTER_STREAK = 2
LEVEL_RUN = 10                 # this many right in a row on a level moves the child up to the next one


def start_level(year: int) -> int:
    """Where a child starts (0-based): the everyday verbs in Years 3-4, higher from Year 5 up."""
    return {5: 1, 6: 1, 7: 2, 8: 3, 9: 4}.get(int(year or 3), 0 if int(year or 3) < 5 else 4)


def _norm(s: str) -> str:
    return " ".join(str(s or "").strip().lower().split())


async def _state(pupil: dict) -> dict:
    st = await db.verbs_state.find_one({"_id": pupil["_id"]})
    if not st:
        st = {"_id": pupil["_id"], "pupil_id": pupil["_id"], "family_id": pupil["family_id"], "level": 0, "streaks": {}}
        await db.verbs_state.insert_one(st)
    if "start" not in st:              # once per child (also for those who began before levels started by year)
        st["start"] = start_level(pupil.get("year", 3))
        st["level"] = max(int(st.get("level", 0)), st["start"])
        await db.verbs_state.update_one({"_id": pupil["_id"]}, {"$set": {"start": st["start"], "level": st["level"]}})
    return st


def _level_done(st: dict, level: int) -> bool:
    return all(st["streaks"].get(v["base"], 0) >= MASTER_STREAK for v in LEVELS[level]["verbs"])


async def next_question(pupil: dict, focus: str | None = None) -> dict:
    """focus: a verb to ask again (a mistake being put right)."""
    st = await _state(pupil)
    level = min(st["level"], len(LEVELS) - 1)
    verbs = LEVELS[level]["verbs"]
    # never the same verb twice in a row, and a missed verb only after a gap (items.just_shown)
    away = await items.just_shown(pupil, "verbs") | {st.get("last")}
    todo = [v for v in verbs if st["streaks"].get(v["base"], 0) < MASTER_STREAK and v["base"] not in away]
    todo = todo or [v for v in verbs if v["base"] not in away] or verbs
    v = next((v for b in LEVELS for v in b["verbs"] if v["base"] == focus), None) or random.choice(todo)
    await db.verbs_state.update_one({"_id": pupil["_id"]}, {"$set": {"last": v["base"]}})
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
    copied = correct and base in await items.just_shown(pupil, "verbs")   # right straight after being shown it
    levelled = False
    if not copied:                     # a copy counts for today only: no streak, no level, not a mistake put right
        streak = st["streaks"].get(base, 0) + 1 if correct else 0
        st["streaks"][base] = streak
        run = int(st.get("run", 0)) + 1 if correct and it["meta"].get("level") == st["level"] else 0
        upd = {f"streaks.{base}": streak, "run": run}
        if correct and st["level"] < len(LEVELS) - 1 and (run >= LEVEL_RUN or _level_done(st, st["level"])):
            upd.update({"level": st["level"] + 1, "run": 0})
            levelled = True
        await db.verbs_state.update_one({"_id": pupil["_id"]}, {"$set": upd})
    await progress.record(pupil, "verbs", correct, ms, "" if copied else base, "Past forms of %s" % base,
                          "%s, %s" % (it["answer"]["past"][0], it["answer"]["pp"][0]), "%s, %s" % (past or "", pp or ""))
    return {"correct": correct, "ok_past": ok_past, "ok_pp": ok_pp,
            "expected": {"past": it["answer"]["past"][0], "pp": it["answer"]["pp"][0]}, "levelled_up": levelled}


async def summary(pupil: dict) -> dict:
    st = await _state(pupil)
    mastered = sum(1 for v in st["streaks"].values() if v >= MASTER_STREAK)
    return {"level": st["level"] + 1, "levels": len(LEVELS), "mastered": mastered,
            "total": sum(len(b["verbs"]) for b in LEVELS)}
