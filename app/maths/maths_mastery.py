# dev/app/logic/maths_mastery.py
"""Per-pupil, per-skill mastery + adaptive skill selection (our SmartScore equivalent).

Mastery score 0-100 per (pupil, skill):
  * correct   -> gain is LARGE early and SMALL near the top, plus a streak bonus.
  * incorrect -> penalty is small early but HEAVY in the "challenge zone" (>=85),
                 so the last stretch demands consistency (as IXL's does).
  * 100 = mastered.

  * right every time FAST_STREAK in a row (or right first time on a hard placement probe) -> secure at
    once, and checked back on a later day.

Adaptive selection walks the pupil's year ladder (Yn.0 -> Yn.9, OUT_OF_YEAR skills left out):
it works the lowest unfinished level of STRAND_WINDOW strands in turn (BLOCK questions at most before
the next strand's turn), preferring skills that are still moving,
spreads practice when skills plateau (PLATEAU_ATTEMPTS) or stall, finishes the skills each level
left behind once every level has passed, and periodically resurfaces a mastered skill for spaced
retention review (which IXL does not do). Years 8 and 9 also mix in earlier KS3 skills
(KS3_MIX_CHANCE).
"""
import datetime
import random
from ..activities import FOCUS_SHARE, focus_on
from ..db import db
from .maths_engine import difficulty_for, skill_list

MASTERED = 100
CHALLENGE_ZONE = 85
LEVEL_PASS_RATIO = 0.8      # fraction of a level's skills mastered before moving on
REVIEW_CHANCE = 0.18        # chance of a spaced-review question
REVIEW_AFTER_DAYS = 3
STUCK_ATTEMPTS = 6        # rotate away after this many failed attempts on one skill
PLATEAU_ATTEMPTS = 20     # ... and spread practice once a skill has this many without nearing mastery
STRAND_WINDOW = 4         # unfinished strands worked side by side, so a child meets several in the first days
BLOCK = 6                 # questions in a row on one skill before the next strand takes a turn
YOUNG_BLOCK = 3           # ... in Years 1-3: a young child tires of one kind of question after 3 or 4
FAST_STREAK = 5           # right every time this many in a row: the skill is secure (checked back another day)
CHECK_BACK_CHANCE = 0.35  # share of questions that check back a skill secured fast, on a later day
PROBE_AFTER_FAST = 1      # skills secured fast before new skills open with one hard placement question
HARD_TIER = 2             # the hardest tier (maths_engine.difficulty_for)
HARD_RIGHT = 2            # right this many in a row at the hardest tier, with no slip, and the skill is secure
FOCUS_WINDOW = 4          # a school-topic strand: its first unfinished skills take turns ...
FOCUS_BLOCK = 3           # ... this many questions each (FAST_STREAK while every answer is right)

# Skills that are the Numbers-in-words activity under another name: on a day that activity is in the
# child's plan, maths leaves them until last.
NUMBER_WORDS = {"Y1.0.b", "Y2.0.d", "Y3.0.b", "Y3.0.c", "Y4.0.b", "Y5.0.a", "Y6.0.a", "Y6.0.b"}


def _now():
    return datetime.datetime.utcnow()


def _earlier_day(ts):
    return bool(ts) and ts.date() < _now().date()


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


_STRANDS = {}


def _strand_of(key):
    if not _STRANDS:
        _STRANDS.update({s["key"]: s["strand"] for s in skill_list()})
    return _STRANDS.get(key)


async def record_attempt(pupil, skill_key, correct, value=None, tier=None):
    """Log the attempt and update mastery. Returns the new mastery doc. tier: how hard the question was (a strong
    child who gets the hardest tier right HARD_RIGHT times in a row, with no slip, has the skill secure)."""
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
    mm = await _mastery_map(pupil)
    doc = mm.get(skill_key) or {}
    latest = max(mm.values(), key=lambda d: d.get("last") or datetime.datetime.min, default={})
    score = int(doc.get("score", 0))
    streak = int(doc.get("streak", 0))
    attempts = int(doc.get("attempts", 0)) + 1
    right = int(doc.get("correct_count", 0)) + (1 if correct else 0)
    upd = {}
    hard = int(doc.get("hard", 0)) + 1 if correct and tier is not None and int(tier) >= HARD_TIER else 0
    if correct:
        streak += 1
        score = min(MASTERED, score + gain(score, streak))
        slips = attempts - right
        if doc.get("probing") or (slips <= 1 and streak >= FAST_STREAK + 2 * slips) \
                or (slips == 0 and hard >= HARD_RIGHT) or (slips == 1 and hard >= HARD_RIGHT + 1):
            # right first time at the hardest tier (a placement probe), or right every time: secure now,
            # checked back on a later day
            score, upd["fast"] = MASTERED, True
        if doc.get("fast") and int(doc.get("score", 0)) >= MASTERED and _earlier_day(doc.get("last")):
            upd["checked"] = True
    else:
        streak = 0
        score = max(0, score - penalty(score))
        upd["fast"] = False
    if doc.get("probing"):
        upd.update({"probing": False, "probe": "right" if correct else "wrong"})
    upd.update({
        "pupil": pupil, "skill": skill_key, "score": score, "streak": streak,
        "attempts": attempts, "correct_count": right, "last": _now(), "hard": hard,
        # questions in a row on this skill: after BLOCK the next strand takes a turn
        "run": int(doc.get("run", 0)) + 1 if latest.get("skill") == skill_key else 1,
        # ... and in a row within its strand, questions from other strands not counted (a school topic's turns)
        "srun": int(doc.get("srun", 0)) + 1 if _latest_in_strand(mm, skill_key).get("skill") == skill_key else 1,
    })
    if score >= MASTERED and not doc.get("mastered_at"):
        upd["mastered_at"] = _now()
    await db.maths_mastery.update_one({"_id": "%s:%s" % (pupil, skill_key)},
                                      {"$set": upd}, upsert=True)
    upd["mastered"] = score >= MASTERED
    return upd


def _latest_in_strand(mm, skill_key):
    strand = _strand_of(skill_key)
    return max((d for k, d in mm.items() if _strand_of(k) == strand and d.get("last")),
               key=lambda d: d["last"], default={})


def _focus_pick(in_focus, mm):
    """A school-topic strand works its first FOCUS_WINDOW unfinished skills in turn, FOCUS_BLOCK questions each
    (more while every answer is right, so a strong child secures one fast), not one skill until it is secure: with
    "The four operations" in focus, multiplication and division come up as well as column addition."""
    unfinished = [s for s in in_focus if mm.get(s["key"], {}).get("score", 0) < MASTERED]
    if not unfinished:
        return None
    fresh = [s for s in unfinished if not (mm.get(s["key"], {}).get("score", 0) == 0
                                           and mm.get(s["key"], {}).get("attempts", 0) >= STUCK_ATTEMPTS)]
    window = (fresh or unfinished)[:FOCUS_WINDOW]
    order = [s["key"] for s in in_focus]
    cur = max((mm[k] for k in order if k in mm and mm[k].get("last")), key=lambda d: d["last"], default={})

    def why(s):
        return s["key"], ("practice" if mm.get(s["key"], {}).get("score", 0) > 0 else "new")
    if cur.get("skill") in [s["key"] for s in window]:
        clean = int(cur.get("attempts", 0)) == int(cur.get("correct_count", 0))
        if int(cur.get("srun", 0)) < (FAST_STREAK if clean else FOCUS_BLOCK):
            return cur["skill"], "practice"
    at = order.index(cur["skill"]) if cur.get("skill") in order else -1
    return why(next((s for s in window if order.index(s["key"]) > at), window[0]))


async def _mastery_map(pupil):
    out = {}
    try:
        async for d in db.maths_mastery.find({"pupil": (pupil or "").lower()}):
            out[d.get("skill")] = d
    except Exception:
        pass
    return out


def _strand_pick(in_strand, mm):
    """The skill to work in one strand, or None when the strand is done enough to move up."""
    mastered = [s for s in in_strand if mm.get(s["key"], {}).get("score", 0) >= MASTERED]
    if len(mastered) >= max(1, int(len(in_strand) * LEVEL_PASS_RATIO)):
        return None  # this level is done enough — move up
    unfinished = [s for s in in_strand if mm.get(s["key"], {}).get("score", 0) < MASTERED]
    if not unfinished:
        return None
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


async def _focus_strand(pupil):
    """The maths strands the parent says the class is working on now ([] if none)."""
    try:
        p = await db.pupils.find_one({"_id": pupil}, {"focus": 1})
    except Exception:
        p = None
    return focus_on(p or {}).get("maths", [])


async def next_skill(pupil, year=None, avoid=()):
    """Adaptive pick: the lowest unfinished levels of several strands in turn, in-progress first; sometimes a
    review. avoid: skills to leave until everything else is mastered (practised elsewhere today)."""
    skills = _year_skills(year)
    if not skills:
        return None
    mm = await _mastery_map(pupil)
    rest = [s for s in skills if s["key"] not in set(avoid)]
    if any(mm.get(s["key"], {}).get("score", 0) < MASTERED for s in rest):
        skills = rest

    # "working on this at school": about two questions in three from that strand, picked as its turn would be
    focus = await _focus_strand(pupil)
    in_focus = [s for s in skills if s["strand"] in focus]
    # Years 1-3: after YOUNG_BLOCK in a row on one focus skill, the next question comes from the ladder instead
    latest = max(mm.values(), key=lambda d: d.get("last") or datetime.datetime.min, default={})
    tired = str(year or "") in ("1", "2", "3") and latest.get("run", 0) >= YOUNG_BLOCK \
        and any(s["key"] == latest.get("skill") for s in in_focus)
    if in_focus and not tired and random.random() < FOCUS_SHARE:
        pick = _focus_pick(in_focus, mm)
        if pick:
            return pick
        return min(in_focus, key=lambda s: mm.get(s["key"], {}).get("last") or datetime.datetime.min)["key"], "review"

    # a skill secured fast is checked back on a later day
    checks = [s["key"] for s in skills if mm.get(s["key"], {}).get("fast") and not mm[s["key"]].get("checked")
              and mm[s["key"]].get("score", 0) >= MASTERED and _earlier_day(mm[s["key"]].get("last"))]
    if checks and random.random() < CHECK_BACK_CHANCE:
        return checks[0], "review"

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

    # walk the ladder by strand (3.0 -> 3.9), the first STRAND_WINDOW unfinished strands side by side:
    # stay on a skill until it is mastered or has had BLOCK questions in a row, then the next strand's turn
    strands = []
    for s in skills:
        if s["strand"] not in strands:
            strands.append(s["strand"])
    window = []
    for strand in strands:
        if in_focus and strand in focus and len(strands) > len(focus):
            continue                     # the school topic has its own turns (above); the other third is the rest
        pick = _strand_pick([s for s in skills if s["strand"] == strand], mm)
        if pick:
            window.append((strand, pick))
        if len(window) >= STRAND_WINDOW:
            break
    if window:
        by_key = {s["key"]: s for s in skills}
        cur = max((d for k, d in mm.items() if k in by_key), key=lambda d: d.get("last") or datetime.datetime.min,
                  default=None)
        at = next((i for i, (strand, _) in enumerate(window) if cur and by_key[cur["skill"]]["strand"] == strand), None)
        if at is None:
            return window[0][1]
        stuck = cur.get("score", 0) == 0 and cur.get("attempts", 0) >= STUCK_ATTEMPTS
        block = YOUNG_BLOCK if str(year or "") in ("1", "2", "3") else BLOCK
        if cur.get("score", 0) < MASTERED and cur.get("run", 0) < block and not stuck:
            return cur["skill"], "practice"
        return window[(at + 1) % len(window)][1]

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


MIDDLE_FROM_YEAR = 5      # from Year 5 a new skill opens at the middle tier, not with Year-2-style counting


async def start_tier(pupil, year, skill_key, score):
    """The difficulty tier of the next question: by the score (maths_engine.difficulty_for), except that in Years
    5 to 9 a skill with no wrong answer yet is asked at the middle tier at least, and at the hardest once two are
    right (so a strong child meets the real thing by the third question, and secures it with HARD_RIGHT of
    those). One slip after two right, or a missed placement probe, keeps the middle tier. Otherwise the score
    decides again, so a child who finds the skill hard gets the easier questions."""
    tier = difficulty_for(score)
    if tier >= HARD_TIER or int(year or 0) < MIDDLE_FROM_YEAR:
        return tier
    d = await db.maths_mastery.find_one({"_id": "%s:%s" % ((pupil or "").lower(), skill_key)}) or {}
    right = int(d.get("correct_count", 0))
    wrong = int(d.get("attempts", 0)) - right
    if wrong <= 0:
        return HARD_TIER if right >= 2 else max(tier, 1)
    if wrong == 1 and (right >= 2 or d.get("probe") == "wrong"):
        return max(tier, 1)
    return tier


async def probe(pupil, year, skill_key):
    """Placement for a strong pupil: once PROBE_AFTER_FAST skills of the year were secured fast, and the last
    skill finished was one of them, a new skill opens with one question at the hardest tier. Right first time
    secures it (checked back another day); wrong, and the skill is practised as usual. True = probing now."""
    keys = {s["key"] for s in _year_skills(year)}
    mm = {k: d for k, d in (await _mastery_map(pupil)).items() if k in keys}
    if mm.get(skill_key, {}).get("attempts"):
        return False
    done = [d for d in mm.values() if d.get("mastered_at")]
    if sum(1 for d in done if d.get("fast")) < PROBE_AFTER_FAST:
        return False
    last = max(done, key=lambda d: d["mastered_at"])
    probed = max((d for d in mm.values() if d.get("probe")), key=lambda d: d.get("last") or datetime.datetime.min,
                 default={})
    if not last.get("fast") or (probed.get("probe") == "wrong" and probed.get("score", 0) < MASTERED):
        return False
    pupil = (pupil or "").lower()
    await db.maths_mastery.update_one({"_id": "%s:%s" % (pupil, skill_key)},
                                      {"$set": {"pupil": pupil, "skill": skill_key, "probing": True}}, upsert=True)
    return True
