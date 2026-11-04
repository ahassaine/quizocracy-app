# dev/app/logic/maths_mastery.py
"""Per-pupil, per-skill mastery + adaptive skill selection (our SmartScore equivalent).

Mastery score 0-100 per (pupil, skill):
  * correct   -> gain is LARGE early and SMALL near the top, plus a streak bonus.
  * incorrect -> penalty is small early but HEAVY in the "challenge zone" (>=85),
                 so the last stretch demands consistency (as IXL's does).
  * 100 = mastered.

Adaptive selection walks the pupil's year ladder (Yn.0 -> Yn.9, OUT_OF_YEAR skills left out):
it works the lowest level that is not yet ~mastered, preferring skills that are still moving,
spreads practice when skills plateau (PLATEAU_ATTEMPTS) or stall, finishes the skills each level
left behind once every level has passed, and periodically resurfaces a mastered skill for spaced
retention review (which IXL does not do). Years 8 and 9 also mix in earlier KS3 skills
(KS3_MIX_CHANCE).
"""
import datetime
import random
from ..db import db
from .maths_engine import skill_list

MASTERED = 100
CHALLENGE_ZONE = 85
LEVEL_PASS_RATIO = 0.8      # fraction of a level's skills mastered before moving on
REVIEW_CHANCE = 0.18        # chance of a spaced-review question
REVIEW_AFTER_DAYS = 3
STUCK_ATTEMPTS = 6        # rotate away after this many failed attempts on one skill
PLATEAU_ATTEMPTS = 20     # ... and spread practice once a skill has this many without nearing mastery


def _now():
    return datetime.datetime.utcnow()


def gain(score, streak):
    """Points for a correct answer — big early, small near 100."""
    g = max(4, int(round((MASTERED - score) * 0.22)))
    return g + min(int(streak), 4)


def penalty(score):
    """Points lost for a wrong answer — heavier in the challenge zone."""
    if score >= CHALLENGE_ZONE:
        return 12
    return max(3, int(round(score * 0.12)))


# Skills whose content the National Curriculum puts in a later year. They stay registered
# (old attempts still resolve) but are not part of their year's ladder; the later year
# teaches the same content in its own bank.
OUT_OF_YEAR = {
    "Y3.9.f",   # likelihood: probability is KS3
    "Y4.4.j",   # algebraic expressions: Year 6
    "Y4.5.f",   # simplifying fractions: Year 6
    "Y4.6.i",   # adding and subtracting decimals: Year 5
    "Y4.7.e",   # imperial units: Year 5
    "Y4.9.h",   # probability: KS3
    "Y4.9.i",   # mean: Year 6
    "Y6.9.i",   # mode and median: KS3
    "Y6.9.j",   # probability: KS3
}


# KS3 is one key stage: Years 8 and 9 keep earlier KS3 skills alive by mixing some in.
KS3_EARLIER = {8: (7,), 9: (7, 8)}
KS3_MIX_CHANCE = 0.15


def _earlier_ks3(year):
    pref = tuple("Y%d." % y for y in KS3_EARLIER.get(int(year or 0), ()))
    return [s for s in skill_list() if pref and s["key"].startswith(pref) and s["key"] not in OUT_OF_YEAR]


def _year_skills(year=None):
    """Every skill, or only those of one year (year=4 -> keys starting 'Y4.')."""
    skills = skill_list()
    if year in (None, "", 0):
        return skills
    pref = "Y%s." % year
    return [s for s in skills if s["key"].startswith(pref) and s["key"] not in OUT_OF_YEAR] or skills


async def record_attempt(pupil, skill_key, correct, value=None):
    """Log the attempt and update mastery. Returns the new mastery doc."""
    pupil = (pupil or "").lower()
    if not pupil or not skill_key:
        return None
    try:
        await db.maths_attempts.insert_one({
            "pupil": pupil, "skill": skill_key, "correct": bool(correct),
            "value": str(value)[:80] if value is not None else None, "ts": _now(),
        })
    except Exception:
        pass
    doc = await db.maths_mastery.find_one({"_id": "%s:%s" % (pupil, skill_key)}) or {}
    score = int(doc.get("score", 0))
    streak = int(doc.get("streak", 0))
    if correct:
        streak += 1
        score = min(MASTERED, score + gain(score, streak))
    else:
        streak = 0
        score = max(0, score - penalty(score))
    upd = {
        "pupil": pupil, "skill": skill_key, "score": score, "streak": streak,
        "attempts": int(doc.get("attempts", 0)) + 1,
        "correct_count": int(doc.get("correct_count", 0)) + (1 if correct else 0),
        "last": _now(),
    }
    if score >= MASTERED and not doc.get("mastered_at"):
        upd["mastered_at"] = _now()
    await db.maths_mastery.update_one({"_id": "%s:%s" % (pupil, skill_key)},
                                      {"$set": upd}, upsert=True)
    upd["mastered"] = score >= MASTERED
    return upd


async def _mastery_map(pupil):
    out = {}
    try:
        async for d in db.maths_mastery.find({"pupil": (pupil or "").lower()}):
            out[d.get("skill")] = d
    except Exception:
        pass
    return out


async def next_skill(pupil, year=None):
    """Adaptive pick: lowest unfinished level, in-progress first; sometimes a review."""
    skills = _year_skills(year)
    if not skills:
        return None
    mm = await _mastery_map(pupil)

    # spaced retention review of an already-mastered skill
    due = [s["key"] for s in skills
           if mm.get(s["key"], {}).get("score", 0) >= MASTERED
           and (_now() - mm[s["key"]].get("last", _now())).days >= REVIEW_AFTER_DAYS]
    if due and random.random() < REVIEW_CHANCE:
        return random.choice(due), "review"

    # earlier KS3 skills, unmastered first
    earlier = _earlier_ks3(year) if year not in (None, "", 0) else []
    if earlier and random.random() < KS3_MIX_CHANCE:
        open_ = [s["key"] for s in earlier if mm.get(s["key"], {}).get("score", 0) < MASTERED]
        return random.choice(open_ or [s["key"] for s in earlier]), "review"

    # walk the ladder by strand (3.0 -> 3.9)
    strands = []
    for s in skills:
        if s["strand"] not in strands:
            strands.append(s["strand"])
    for strand in strands:
        in_strand = [s for s in skills if s["strand"] == strand]
        mastered = [s for s in in_strand if mm.get(s["key"], {}).get("score", 0) >= MASTERED]
        if len(mastered) >= max(1, int(len(in_strand) * LEVEL_PASS_RATIO)):
            continue  # this level is done enough — move up
        unfinished = [s for s in in_strand if mm.get(s["key"], {}).get("score", 0) < MASTERED]
        if not unfinished:
            continue
        started = [s for s in unfinished if mm.get(s["key"], {}).get("score", 0) > 0]
        unstarted = [s for s in unfinished if mm.get(s["key"], {}).get("score", 0) == 0]
        # anti-stuck: if the pupil keeps failing one skill (many attempts, still 0),
        # rotate to a fresh skill rather than trapping them on it forever.
        stuck = [s for s in unfinished
                 if mm.get(s["key"], {}).get("score", 0) == 0
                 and mm.get(s["key"], {}).get("attempts", 0) >= STUCK_ATTEMPTS]
        if stuck and unstarted:
            fresh = [s for s in unstarted if s not in stuck]
            if fresh:
                return fresh[0]["key"], "new"
        # plateau: long practice without reaching the challenge zone; spread practice
        # across the level instead of holding a struggling pupil on one skill
        plateau = [s for s in started if mm[s["key"]].get("attempts", 0) >= PLATEAU_ATTEMPTS
                   and mm[s["key"]]["score"] < CHALLENGE_ZONE]
        moving = [s for s in started if s not in plateau]
        if moving:
            moving.sort(key=lambda s: mm[s["key"]]["score"])
            return moving[0]["key"], "practice"
        fresh = [s for s in unstarted if s not in stuck]
        if fresh:
            return fresh[0]["key"], "new"
        # every skill here is on a plateau or stuck: rotate, least recently practised first
        unfinished.sort(key=lambda s: mm.get(s["key"], {}).get("last") or datetime.datetime.min)
        s = unfinished[0]
        return s["key"], ("practice" if mm.get(s["key"], {}).get("score", 0) > 0 else "new")

    # every level passed: finish the skills each level left behind, in ladder order
    left = [s for s in skills if mm.get(s["key"], {}).get("score", 0) < MASTERED]
    if left:
        fresh = [s for s in left if mm.get(s["key"], {}).get("attempts", 0) < STUCK_ATTEMPTS
                 or mm[s["key"]].get("score", 0) > 0]
        s = (fresh or left)[0]
        return s["key"], ("practice" if mm.get(s["key"], {}).get("score", 0) > 0 else "new")

    # everything mastered — free review
    return random.choice(skills)["key"], "review"


async def progress(pupil, year=None):
    """Summary for the practice header."""
    skills = _year_skills(year)
    mm = await _mastery_map(pupil)
    total = len(skills)
    mastered = sum(1 for s in skills if mm.get(s["key"], {}).get("score", 0) >= MASTERED)
    started = sum(1 for s in skills if 0 < mm.get(s["key"], {}).get("score", 0) < MASTERED)
    by_strand = []
    seen = []
    for s in skills:
        if s["strand"] not in seen:
            seen.append(s["strand"])
    for strand in seen:
        ins = [s for s in skills if s["strand"] == strand]
        m = sum(1 for s in ins if mm.get(s["key"], {}).get("score", 0) >= MASTERED)
        by_strand.append({"strand": strand, "mastered": m, "total": len(ins)})
    return {"total": total, "mastered": mastered, "started": started,
            "pct": int(round(100.0 * mastered / total)) if total else 0,
            "by_strand": by_strand}


async def skill_score(pupil, skill_key):
    d = await db.maths_mastery.find_one({"_id": "%s:%s" % ((pupil or "").lower(), skill_key)})
    return int((d or {}).get("score", 0))
