"""Maths: generator banks for Years 1 to 9 with per-child mastery."""
import datetime
import re

from bson import ObjectId

from ..activities import todays_plan
from ..db import db
from ..maths import maths_engine, maths_mastery
from .. import items, progress

ENGINE_YEARS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
REPEAT_HOURS = 6       # a question met in the last few hours is not asked again word for word ...
REPEAT_TRIES = 6       # ... as far as the skill's generator can vary it


async def _done_elsewhere(pupil: dict) -> set:
    """Maths skills another of today's activities already practises: writing numbers in words and figures is
    the Numbers-in-words activity, so on a day that is in the plan those skills wait until last."""
    family = await db.families.find_one({"_id": pupil["family_id"]}) or {}
    if any(a["key"] == "numbers" for a in todays_plan(pupil, family)):
        return maths_mastery.NUMBER_WORDS
    return set()


def engine_year(year: int) -> int:
    """The child's own year (every year from 1 to 9 has its own bank)."""
    return max([y for y in ENGINE_YEARS if y <= max(int(year or 1), 1)])


LIKE_TRIES = 800      # questions made in memory, at most, to find one like a mistake (progress.alike)


async def _mistake(focus: str | None) -> dict | None:
    """focus "skill@attempt id" (progress.mistake_key): that maths mistake, if it is one."""
    skill, _, rid = (focus or "").partition("@")
    if skill not in maths_engine.GENERATORS or not ObjectId.is_valid(rid):
        return None
    return await db.attempts.find_one({"_id": ObjectId(rid), "activity": "maths", "detail": skill, "correct": False})


def _numbers(prompt: str) -> tuple:
    """The numbers a question is made of, in any order: "Which number goes with 7 to make 10?" and "10 − ___ = 7"
    are one question in two forms."""
    return tuple(sorted(re.findall(r"\d+(?:\.\d+)?", prompt or "")))


async def _just_missed(pupil: dict, skill_key: str) -> set:
    """The numbers of this skill's questions missed too recently to come back (the gap of items.waits). A new
    question with the same numbers, even in another form (typed after a number line), would be copied from the
    correction just shown, so it is not asked until the gap is over."""
    ids = [k.split("@", 1)[1] for k in await items.waits(pupil, "maths") if k.startswith(skill_key + "@")]
    ids = [ObjectId(i) for i in ids if ObjectId.is_valid(i)]
    return {n for r in (await db.attempts.find({"_id": {"$in": ids}}, {"q": 1}).to_list(50) if ids else [])
            if (n := _numbers(r.get("q", "")))}


async def next_question(pupil: dict, focus: str | None = None) -> dict | None:
    """focus: a mistake to put right ("skill@attempt id"): a question like it, the same kind with new numbers
    (a generator never makes the same question twice). If none can be made, the mistake is marked nolike (it
    stays on the parent's list, not in "Practise my mistakes") and the question is a practice one (no_like)."""
    pid, year = pupil["_id"], engine_year(pupil.get("year", 3))
    miss = await _mistake(focus)
    picked = (miss["detail"], "fix") if miss else \
        await maths_mastery.next_skill(pid, year, avoid=await _done_elsewhere(pupil))
    if not picked:
        return None
    skill_key, reason = picked
    score = await maths_mastery.skill_score(pid, skill_key)
    diff = await maths_mastery.start_tier(pid, year, skill_key, score)     # Years 5-9 open new skills mid-tier
    if miss and miss.get("dif"):
        diff = miss["dif"]                               # as hard as the question that was missed
    if reason == "new" and await maths_mastery.probe(pid, year, skill_key):
        diff = 2                                         # placement: one hard question first
    # never the same question twice in a sitting
    recent = {d.get("prompt") async for d in db.maths_lab_q.find(
        {"pupil": pid, "created": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(hours=REPEAT_HOURS)}},
        {"prompt": 1})}
    no_like = False
    if miss:
        # made in memory until one is like the mistake (a skill with many kinds of question may need hundreds);
        # first at the missed question's tier, then at any tier, as some kinds come only at some tiers
        fn, made, tier = maths_engine.GENERATORS[skill_key], None, diff
        for i in range(LIKE_TRIES):
            tier = diff if i < LIKE_TRIES // 2 else i % 3
            g = maths_engine.call_generator(fn, tier)
            # word for word is not new, unless its picture or table carries the numbers ("What numeral belongs in
            # the empty cell?" is the same sentence over a new table)
            fresh = g.get("prompt") != miss.get("q") or (g.get("component") and g.get("spec") not in (None, "", "{}", {}))
            if fresh and progress.alike(miss.get("q", ""), g.get("prompt", "")):
                made = g
                break
        if not made:
            no_like, reason, tier = True, "practice", diff
            await db.attempts.update_one({"_id": miss["_id"]}, {"$set": {"nolike": True}})
        q = await maths_engine.new_question(skill_key, tier, pupil=pid, made=made)
    else:
        missed = await _just_missed(pupil, skill_key)
        for i in range(REPEAT_TRIES):
            q = await maths_engine.new_question(skill_key, diff, pupil=pid)
            if not q or (q["prompt"] not in recent and _numbers(q["prompt"]) not in missed) \
                    or i == REPEAT_TRIES - 1:                                 # the last try is kept, repeat or not
                break
            await db.maths_lab_q.delete_one({"_id": q["token"]})
    if not q:
        return None
    meta = next((s for s in maths_engine.skill_list() if s["key"] == skill_key), {})
    return {**q, "skill": skill_key, "title": meta.get("title", skill_key), "strand": meta.get("strand", ""),
            "reason": reason, "score": score, "progress": await maths_mastery.progress(pid, year),
            **({"no_like": True} if no_like else {})}


async def check(pupil: dict, token: str, value, ms: int | None) -> dict | None:
    pid = pupil["_id"]
    served = await db.maths_lab_q.find_one({"_id": str(token or "")}, {"difficulty": 1})
    res = await maths_engine.check(token, value, pid)
    if not res.get("ok"):
        return None
    if res.get("retry"):                 # a spelling slip: try again, nothing recorded yet
        return {"correct": False, "retry": True, "hint": res["hint"]}
    m = await maths_mastery.record_attempt(pid, res["skill"], res["correct"], value)
    prompt = res.pop("prompt", "")
    # a right answer keeps its question (like), so it can put right an earlier mistake like it;
    # a mistake keeps how hard it was (dif), so the question that puts it right is as hard
    await progress.record(pupil, "maths", res["correct"], ms, res["skill"], prompt, res["expected"], value,
                          like=prompt, extra={"dif": (served or {}).get("difficulty")})
    # mastered: only the answer that makes the skill secure for the first time (a moment, not every right answer after)
    res.update({"score": m["score"], "mastered": bool(m.get("mastered") and m.get("mastered_at")),
                "progress": await maths_mastery.progress(pid, engine_year(pupil.get("year", 3)))})
    return res


async def summary(pupil: dict) -> dict:
    return await maths_mastery.progress(pupil["_id"], engine_year(pupil.get("year", 3)))
