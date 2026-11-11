"""Grammar and punctuation, and science: hand-written questions from app/bank, one year's skills at a time.

Mastery per skill uses the maths scoring (big gains early, a demanding last stretch; 100 = mastered).
The child works a window of the first WINDOW unmastered skills in teaching order, interleaved; a wrong
question comes back RETRY_GAP questions and RETRY_SECONDS later, and once more on a later day; mastered skills come back now and then for review.
Once the day's target is reached, extra practice takes the year's strands in turn, weakest first (spread_strands).
"""
import datetime
import random

from ..activities import FOCUS_SHARE, focus_on, rest_day, todays_plan
from ..bank import engine
from ..db import db
from ..levels import level
from ..maths.maths_mastery import CHALLENGE_ZONE, MASTERED, gain, penalty
from .. import items, progress
from . import typos

WINDOW = 3                 # unmastered skills practised side by side ...
STRAND_WINDOW = 2          # ... at most this many from one strand while other strands have skills open
STRAND_RUN = 3             # questions in a row from one strand before the next comes from another
SKILL_RUN = 3              # questions in a row from one skill, even in a focus, before another skill
FOCUS_MIN = 6              # a focus with fewer skills left to learn takes in the neighbouring strands too
OWN_SHARE = 0.7            # ... but most of the focus share is still the strand the grown-up chose
PLATEAU_ATTEMPTS = 25      # a skill this long without nearing mastery steps aside for the next one
RETRY_GAP = items.RECALL_ITEMS          # questions before a wrong one comes back ...
RETRY_SECONDS = items.RECALL_SECONDS    # ... and seconds, so it is remembered, not copied; then once more another day
MAX_RETRIES = 2
REVIEW_CHANCE = 0.15
REVIEW_AFTER_DAYS = 3
WEAK_SECONDS = 60          # extra practice: a strand at score 0 comes round as if met a minute earlier


def _now():
    return datetime.datetime.utcnow()


async def _mastery(pupil: dict, subject: str) -> dict:
    return {d["key"]: d async for d in db.bank_mastery.find({"pupil_id": pupil["_id"], "subject": subject})}


async def _state(pupil: dict, subject: str) -> dict:
    sid = f"{pupil['_id']}:{subject}"
    st = await db.bank_state.find_one({"_id": sid})
    if not st:
        st = {"_id": sid, "pupil_id": pupil["_id"], "family_id": pupil["family_id"], "subject": subject,
              "n": 0, "retry": []}
        await db.bank_state.insert_one(st)
    return st


def _spread(skills: list, n: int) -> list:
    """The first n skills in teaching order, but no more than STRAND_WINDOW of them from one strand while other
    strands have skills to offer: Year 9 science is not twelve Health questions before anything else."""
    out, per = [], {}
    for s in skills:
        if len(out) < n and per.get(s["strand"], 0) < STRAND_WINDOW:
            out.append(s)
            per[s["strand"]] = per.get(s["strand"], 0) + 1
    return out + [s for s in skills if s not in out][:n - len(out)]


def pick_skill(skills: list, mm: dict, rnd=random, avoid: str | None = None, width: int = WINDOW,
               avoid_skill: str | None = None) -> tuple[dict, str]:
    """Which skill comes next, and why ("new", "practice" or "review"). avoid: a strand just met STRAND_RUN times
    in a row; the next skill comes from another strand when there is one. width: how many unmastered skills are
    worked side by side (a focus works all of its skills). avoid_skill: a skill just met SKILL_RUN times in a row."""
    score = lambda s: mm.get(s["key"], {}).get("score", 0)                      # noqa: E731
    if avoid and any(s["strand"] != avoid for s in skills):
        skills = [s for s in skills if s["strand"] != avoid]
    if avoid_skill and any(s["key"] != avoid_skill for s in skills):
        skills = [s for s in skills if s["key"] != avoid_skill]
    open_ = [s for s in skills if score(s) < MASTERED]
    done = [s for s in skills if score(s) >= MASTERED]
    due = [s for s in done if (_now() - mm[s["key"]].get("last", _now())).days >= REVIEW_AFTER_DAYS]
    if not open_ or (due and rnd.random() < REVIEW_CHANCE):
        pool = due or done
        pool.sort(key=lambda s: mm[s["key"]].get("last") or datetime.datetime.min)
        return pool[0], "review"
    plateau = lambda s: (mm.get(s["key"], {}).get("attempts", 0) >= PLATEAU_ATTEMPTS        # noqa: E731
                         and score(s) < CHALLENGE_ZONE)
    window = _spread([s for s in open_ if not plateau(s)], width) or open_
    window.sort(key=lambda s: mm.get(s["key"], {}).get("last") or datetime.datetime.min)
    s = window[0]
    return s, ("practice" if s["key"] in mm else "new")


def focus_pool(skills: list, in_focus: list, mm: dict) -> list:
    """The skills the focus share ("working on this at school") is spread over: every skill of the focus strands,
    and when fewer than FOCUS_MIN of them are left to learn, the strands next to them in the year's teaching order
    (Year 9 "Punctuation" with "Grammar for style" around it), nearest first."""
    left = lambda pool: sum(1 for s in pool if mm.get(s["key"], {}).get("score", 0) < MASTERED)   # noqa: E731
    out = list(in_focus)
    order = list(dict.fromkeys(s["strand"] for s in skills))
    have = {s["strand"] for s in in_focus}
    at = [i for i, st in enumerate(order) if st in have]
    for d in range(1, len(order)):
        if left(out) >= FOCUS_MIN or not at:
            break
        for j in sorted({i + k for i in at for k in (-d, d)}):
            if 0 <= j < len(order) and order[j] not in have:
                have.add(order[j])
                out += [s for s in skills if s["strand"] == order[j]]
    return out


def spread_strands(skills: list, mm: dict) -> list:
    """Extra practice after the day's target: the skills of one strand, taking the year's strands in turn rather
    than more of the first one ("Word classes" for 17 questions). The strand met least lately goes next, a strand
    never met first of all; a weak strand counts as met up to WEAK_SECONDS earlier, so it comes round more often.
    Strands with nothing left to master wait until every strand is done."""
    by: dict = {}
    for s in skills:
        by.setdefault(s["strand"], []).append(s)
    score = lambda s: mm.get(s["key"], {}).get("score", 0)                      # noqa: E731
    mean = lambda st: sum(score(s) for s in by[st]) / len(by[st])              # noqa: E731

    def turn(st):
        last = max(mm.get(s["key"], {}).get("last") or datetime.datetime.min for s in by[st])
        if last == datetime.datetime.min:
            return (0, mean(st))
        return (1, last - datetime.timedelta(seconds=WEAK_SECONDS * (MASTERED - mean(st)) / MASTERED))
    strands = [st for st in by if any(score(s) < MASTERED for s in by[st])] or list(by)
    return by[min(strands, key=turn)]


async def past_target(pupil: dict, subject: str) -> bool:
    """Is today's practice of this subject extra: its target reached, a rest day, or not in today's plan?"""
    family = await db.families.find_one({"_id": pupil["family_id"]}) or {}
    target = next((a["target"] for a in todays_plan(pupil, family) if a["key"] == subject), None)
    if target is None or rest_day(pupil):
        return True
    day = progress.today()
    done = (await progress.counts([pupil["_id"]], [day])).get(pupil["_id"], {}).get(day, {}).get(subject, {})
    return done.get("correct", 0) >= target


def pick_question(sk: dict, seen: list, rnd=random) -> dict:
    """A question of the skill the child has not seen lately."""
    fresh = [q for q in sk["qs"] if q["id"] not in seen]
    if not fresh:                            # all seen: start again, but not with the last few
        recent = seen[-min(3, len(sk["qs"]) - 1):] if len(sk["qs"]) > 1 else []
        fresh = [q for q in sk["qs"] if q["id"] not in recent]
    return rnd.choice(fresh)


def glossed(pupil: dict) -> bool:
    """Key words are underlined with their meaning from Year 3 (glossary.py); Years 1-2 hear the question read."""
    return int(pupil.get("year") or 0) >= 3


def make(subject: str):
    """The drill module for one subject: next_question, check, summary."""

    async def next_question(pupil: dict, focus: str | None = None, near: list | None = None,
                            known: bool = False) -> dict | None:
        """focus: "skill#question" to ask again (a mistake being put right). near: questions ("skill#question")
        waiting to be put right; the question then comes from their skills, not one of them. known: focus is a
        question this child got right before, asked while a mistake waits for its gap (not a mistake)."""
        skills = engine.skills(subject, level(pupil, subject))      # "working at" for this subject, else the school year
        if not skills:
            return None
        st = await _state(pupil, subject)
        mm = await _mastery(pupil, subject)
        reason, q, sk = None, None, None
        if focus and "#" in focus:
            k, qid = focus.split("#", 1)
            sk, q = engine.skill(k), engine.question(k, qid)
            reason = ("known" if known else "fix") if sk and q else None
        # never a question whose answer was just shown (it waits for its gap), nor the one just answered
        last = ((await items.last_answered(pupil, subject)) or {}).get("meta") or {}
        away = await items.just_shown(pupil, subject) | set(near or []) | {f"{last.get('skill')}#{last.get('qid')}"}
        now, today = _now(), progress.today()
        for r in ([] if reason else st.get("retry", [])):
            if r["due"] <= st["n"] and r.get("after", now) <= now and r.get("day", "") < today \
                    and f"{r['key']}#{r['qid']}" not in away:
                sk, q = engine.skill(r["key"]), engine.question(r["key"], r["qid"])
                if sk and q:
                    reason = "retry"
                    break
        if not reason:
            # "working on this at school": about two questions in three from that strand, still by mastery
            strands = focus_on(pupil).get(subject, [])
            in_focus = engine.focus_skills(subject, level(pupil, subject), strands)   # an earlier year's topic too
            close = [s for s in skills if len(s["qs"]) > 3 and any(n.split("#")[0] == s["key"] for n in near or [])]
            focused = focus_pool(skills, in_focus, mm) if in_focus else []
            pool = close or (focused if focused and random.random() < FOCUS_SHARE else None)
            if pool is focused and len(focused) > len(in_focus) and random.random() < OWN_SHARE:
                pool = focused = list(in_focus)                  # the chosen strand stays most of it; neighbours fill in
            width = len(pool) if pool is focused else WINDOW     # the focus share goes round all its skills
            if not pool:            # in teaching order up to the day's target; after it, the strands in turn
                pool = spread_strands(skills, mm) if await past_target(pupil, subject) else skills
                pool = [s for s in pool if s not in focused] or pool    # the other third: not the focus again
            run = st.get("strands", [])[-STRAND_RUN:]       # one strand three times running: another one next,
            avoid = run[0] if len(run) == STRAND_RUN and len(set(run)) == 1 and run[0] not in strands else None
            runs = st.get("skills", [])[-SKILL_RUN:]        # never more than SKILL_RUN in a row from one skill
            avoid_skill = runs[0] if len(runs) == SKILL_RUN and len(set(runs)) == 1 else None
            sk, reason = pick_skill(pool, mm, avoid=avoid, width=width,   # unless the grown-up chose that
                                    avoid_skill=avoid_skill)              # strand as the focus
            q = pick_question(sk, mm.get(sk["key"], {}).get("seen", [])
                              + [a.split("#", 1)[1] for a in away if a.startswith(sk["key"] + "#")])
        pub, key = engine.serve(q)
        token = await items.issue(pupil, subject, key, {"skill": sk["key"], "qid": q["id"], "reason": reason})
        await db.bank_state.update_one({"_id": st["_id"]}, {"$inc": {"n": 1},
                                                           "$push": {"strands": {"$each": [sk["strand"]], "$slice": -5},
                                                                     "skills": {"$each": [sk["key"]], "$slice": -5}}})
        out = {"token": token, **pub, "skill": sk["title"], "strand": sk["strand"], "reason": reason,
               "score": mm.get(sk["key"], {}).get("score", 0)}
        if glossed(pupil):                  # key words in the question, tap for the meaning (none that give it away)
            out["terms"] = engine.key_words(subject, [q["q"]], q)
        return out

    async def check(pupil: dict, token: str, value, ms: int | None, idk: bool = False) -> dict | None:
        """idk: "I don't know" was pressed: a miss marked idk (not a guess, not rushed), with the answer and why."""
        it = await items.claim(pupil, subject, token)
        if not it:
            return None
        key, meta = it["answer"], it["meta"]
        correct = False if idk else engine.mark(key, value)
        sk, q = engine.skill(meta["skill"]), engine.question(meta["skill"], meta["qid"])
        detail = f"{meta['skill']}#{meta['qid']}"
        apos = None if correct or idk else engine.apostrophe_slip(key, value, sk)    # "cant you": a punctuation slip
        slipped = [] if correct or apos or idk else engine.slips(key, value, (q or {}).get("q", ""), sk)
        ends = None if correct or slipped or idk else (apos or engine.end_slip(key, value, sk))
        if (slipped or ends) and not it.get("retried"):
            # a word with a spelling slip ("respiraton", "wich"), or a sentence missing only its capital or full
            # stop, where that is not the skill: one free retry, nothing recorded yet
            await db.items.update_one({"_id": it["_id"]}, {"$set": {"done": False, "retried": True}})
            return {"correct": False, "retry": True, "hint": ends["retry"] if ends else typos.RETRY}
        if correct and detail in await items.just_shown(pupil, subject):
            return await _copied(pupil, subject, key, value, q, ms, detail)
        doc = await db.bank_mastery.find_one({"_id": f"{pupil['_id']}:{meta['skill']}"}) or {}
        score, streak = int(doc.get("score", 0)), int(doc.get("streak", 0))
        missed = await progress.last_miss(pupil, subject, detail) if correct else None
        practice = bool(missed and _now() - missed < progress.PUT_RIGHT_AFTER)
        if practice:
            pass        # a question missed in this sitting, right again: practice, the score and streak stay
        elif correct:
            streak += 1
            score = min(MASTERED, score + gain(score, streak))
            if missed:  # a question missed before, right later: the score grows, but only a question never
                score = min(score, max(int(doc.get("score", 0)), MASTERED - 1))     # missed makes it mastered
        else:
            streak = 0
            score = max(0, score - penalty(score))
        seen = [s for s in doc.get("seen", []) if s != meta["qid"]] + [meta["qid"]]
        upd = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "subject": subject, "key": meta["skill"],
               "score": score, "streak": streak, "attempts": int(doc.get("attempts", 0)) + 1,
               "correct": int(doc.get("correct", 0)) + (1 if correct else 0), "last": _now(), "seen": seen[-40:]}
        if score >= MASTERED and not doc.get("mastered_at"):
            upd["mastered_at"] = _now()
        await db.bank_mastery.update_one({"_id": f"{pupil['_id']}:{meta['skill']}"}, {"$set": upd}, upsert=True)

        st = await _state(pupil, subject)
        retry = [r for r in st.get("retry", []) if not (r["key"] == meta["skill"] and r["qid"] == meta["qid"])]
        tries = next((r.get("tries", 0) for r in st.get("retry", [])
                      if r["key"] == meta["skill"] and r["qid"] == meta["qid"]), 0)
        if not correct and tries < MAX_RETRIES:
            retry.append({"key": meta["skill"], "qid": meta["qid"], "due": st["n"] + RETRY_GAP, "tries": tries + 1,
                          "after": _now() + datetime.timedelta(seconds=RETRY_SECONDS)})
        elif correct and meta.get("reason") in ("retry", "fix") and tries < MAX_RETRIES:
            # put right after a gap: asked once more on a later day, to see that it stayed
            retry.append({"key": meta["skill"], "qid": meta["qid"], "due": 0, "tries": MAX_RETRIES,
                          "day": progress.today()})
        await db.bank_state.update_one({"_id": st["_id"]}, {"$set": {"retry": retry[-10:]}})
        out = await _feedback(pupil, subject, key, value, q, ms, detail, correct, idk=idk)
        if idk:             # nothing was picked: the answer and why, no "why that one is wrong"
            out["whynot"], out["idk"] = "", True
        elif not correct:   # why the option picked is wrong; a question missed before is explained another way
            out["whynot"], out["why"] = engine.why_lines(q, key, value, meta.get("reason") in ("retry", "fix"))
        out.update({"mastered": score >= MASTERED and not doc.get("mastered_at"), "score": score})
        if practice:                         # not put right yet: asked again in a later sitting
            out["again_later"] = True
        if slipped:                         # after the retry: which word was misspelt
            out["hint"] = typos.corrections(slipped)
        if ends:                             # the grammar was right: say what was missing, not why the grammar is so
            out["hint"], out["why"] = ends["after"], ""
        if not correct and not idk and key["t"] == "write":
            wm = engine.word_marks(value, key["a"])     # the words that differ, marked in both sentences
            if wm:
                out["expected"], out["marks"] = wm
        if glossed(pupil):                   # after the answer: the key words of the question and its explanation
            out["terms"] = engine.key_words(subject, [(q or {}).get("q", ""), out.get("why", ""), out.get("whynot", "")])
        return out

    async def _feedback(pupil, subject, key, value, q, ms, detail, correct, copied=False, idk=False) -> dict:
        prompt = (q or {}).get("q", "")
        if q and q.get("s") and q["t"] in ("tap", "write"):
            prompt += " " + q["s"].replace("[", "").replace("]", "")
        exp = engine.expected_text(key)
        # pick: an option or words tapped, so a wrong one this quick was not read (progress.PICK_MS)
        # idk: "I don't know" pressed (nothing given, never rushed or a guess: progress.day_stats)
        await progress.record(pupil, subject, correct, ms, detail, prompt, exp,
                              "" if idk else engine.given_text(key, value), copied=copied,
                              extra={"idk": True} if idk else {"pick": True} if key["t"] in ("mcq", "tap") else None)
        out = {"correct": correct, "expected": exp, "why": (q or {}).get("why", "")}
        if key["t"] == "mcq":
            out["right"] = key["right"]
        if key["t"] == "tap":
            out["hits"] = key["hits"]
        if key["t"] == "num" and q and q.get("unit"):
            out["expected"] = f"{exp} {q['unit']}"
        return out

    async def _copied(pupil, subject, key, value, q, ms, detail) -> dict:
        """Right, but straight after being shown it: counts for today; no mastery, and the mistake stays to put right."""
        out = await _feedback(pupil, subject, key, value, q, ms, detail, True, copied=True)
        sc = await db.bank_mastery.find_one({"_id": f"{pupil['_id']}:{detail.split('#')[0]}"}) or {}
        out.update({"mastered": False, "score": int(sc.get("score", 0)), "again_later": True})
        return out

    async def summary(pupil: dict) -> dict:
        skills = engine.skills(subject, level(pupil, subject))
        mm = await _mastery(pupil, subject)
        mastered = sum(1 for s in skills if mm.get(s["key"], {}).get("score", 0) >= MASTERED)
        return {"mastered": mastered, "total": len(skills), "year": engine.bank_year(subject, level(pupil, subject))}

    return type(subject, (), {"next_question": staticmethod(next_question), "check": staticmethod(check),
                              "summary": staticmethod(summary)})


grammar = make("grammar")
science = make("science")
