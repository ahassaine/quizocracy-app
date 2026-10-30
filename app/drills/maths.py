"""Maths: the family app's generator engine (Years 3, 4, 6, 8) with per-child mastery."""
from ..maths import maths_engine, maths_mastery
from .. import progress

ENGINE_YEARS = (3, 4, 6, 8)


def engine_year(year: int) -> int:
    """The nearest year with generators at or below the child's year (Year 5 works Year 4, and so on)."""
    return max([y for y in ENGINE_YEARS if y <= max(year, 3)])


async def next_question(pupil: dict) -> dict | None:
    pid, year = pupil["_id"], engine_year(pupil.get("year", 3))
    picked = await maths_mastery.next_skill(pid, year)
    if not picked:
        return None
    skill_key, reason = picked
    score = await maths_mastery.skill_score(pid, skill_key)
    diff = maths_engine.difficulty_for(score)
    q = await maths_engine.new_question(skill_key, diff, pupil=pid)
    if not q:
        return None
    meta = next((s for s in maths_engine.skill_list() if s["key"] == skill_key), {})
    return {**q, "skill": skill_key, "title": meta.get("title", skill_key), "strand": meta.get("strand", ""),
            "reason": reason, "score": score, "progress": await maths_mastery.progress(pid, year)}


async def check(pupil: dict, token: str, value, ms: int | None) -> dict | None:
    pid = pupil["_id"]
    res = await maths_engine.check(token, value, pid)
    if not res.get("ok"):
        return None
    m = await maths_mastery.record_attempt(pid, res["skill"], res["correct"], value)
    await progress.record(pupil, "maths", res["correct"], ms, res["skill"])
    res.update({"score": m["score"], "mastered": m.get("mastered", False),
                "progress": await maths_mastery.progress(pid, engine_year(pupil.get("year", 3)))})
    return res


async def summary(pupil: dict) -> dict:
    return await maths_mastery.progress(pupil["_id"], engine_year(pupil.get("year", 3)))
