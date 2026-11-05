"""Maths: generator banks for Years 1 to 9 with per-child mastery."""
from ..maths import maths_engine, maths_mastery
from .. import progress

ENGINE_YEARS = (1, 2, 3, 4, 5, 6, 7, 8, 9)


def engine_year(year: int) -> int:
    """The child's own year (every year from 1 to 9 has its own bank)."""
    return max([y for y in ENGINE_YEARS if y <= max(int(year or 1), 1)])


async def next_question(pupil: dict, focus: str | None = None) -> dict | None:
    """focus: a skill to practise again (a mistake being put right)."""
    pid, year = pupil["_id"], engine_year(pupil.get("year", 3))
    picked = (focus, "fix") if focus in maths_engine.GENERATORS else await maths_mastery.next_skill(pid, year)
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
    await progress.record(pupil, "maths", res["correct"], ms, res["skill"],
                          res.pop("prompt", ""), res["expected"], value)
    res.update({"score": m["score"], "mastered": m.get("mastered", False),
                "progress": await maths_mastery.progress(pid, engine_year(pupil.get("year", 3)))})
    return res


async def summary(pupil: dict) -> dict:
    return await maths_mastery.progress(pupil["_id"], engine_year(pupil.get("year", 3)))
