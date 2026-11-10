"""Grammar and punctuation, and science: hand-written questions from app/bank, one year's skills at a time.

Mastery per skill uses the maths scoring (big gains early, a demanding last stretch; 100 = mastered).
The child works a window of the first WINDOW unmastered skills in teaching order, interleaved; a wrong
question comes back RETRY_GAP questions and RETRY_SECONDS later, and once more on a later day; mastered skills come back now and then for review.
"""
import datetime
import random

from ..bank import engine
from ..db import db
from ..maths.maths_mastery import CHALLENGE_ZONE, MASTERED, gain, penalty
from .. import items, progress
from . import typos

WINDOW = 3                 # unmastered skills practised side by side
PLATEAU_ATTEMPTS = 25      # a skill this long without nearing mastery steps aside for the next one
RETRY_GAP = items.RECALL_ITEMS          # questions before a wrong one comes back ...
RETRY_SECONDS = items.RECALL_SECONDS    # ... and seconds, so it is remembered, not copied; then once more another day
MAX_RETRIES = 2
REVIEW_CHANCE = 0.15
REVIEW_AFTER_DAYS = 3


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


def pick_skill(skills: list, mm: dict, rnd=random) -> tuple[dict, str]:
    """Which skill comes next, and why ("new", "practice" or "review")."""
    score = lambda s: mm.get(s["key"], {}).get("score", 0)                      # noqa: E731
    open_ = [s for s in skills if score(s) < MASTERED]
    done = [s for s in skills if score(s) >= MASTERED]
    due = [s for s in done if (_now() - mm[s["key"]].get("last", _now())).days >= REVIEW_AFTER_DAYS]
    if not open_ or (due and rnd.random() < REVIEW_CHANCE):
        pool = due or done
        pool.sort(key=lambda s: mm[s["key"]].get("last") or datetime.datetime.min)
        return pool[0], "review"
    plateau = lambda s: (mm.get(s["key"], {}).get("attempts", 0) >= PLATEAU_ATTEMPTS        # noqa: E731
                         and score(s) < CHALLENGE_ZONE)
    window = [s for s in open_ if not plateau(s)][:WINDOW] or open_
    window.sort(key=lambda s: mm.get(s["key"], {}).get("last") or datetime.datetime.min)
    s = window[0]
    return s, ("practice" if s["key"] in mm else "new")


def pick_question(sk: dict, seen: list, rnd=random) -> dict:
    """A question of the skill the child has not seen lately."""
    fresh = [q for q in sk["qs"] if q["id"] not in seen]
    if not fresh:                            # all seen: start again, but not with the last few
        recent = seen[-min(3, len(sk["qs"]) - 1):] if len(sk["qs"]) > 1 else []
        fresh = [q for q in sk["qs"] if q["id"] not in recent]
    return rnd.choice(fresh)


def make(subject: str):
    """The drill module for one subject: next_question, check, summary."""

    async def next_question(pupil: dict, focus: str | None = None) -> dict | None:
        """focus: "skill#question" to ask again (a mistake being put right)."""
        skills = engine.skills(subject, pupil.get("year", 3))
        if not skills:
            return None
        st = await _state(pupil, subject)
        mm = await _mastery(pupil, subject)
        reason, q, sk = None, None, None
        if focus and "#" in focus:
            k, qid = focus.split("#", 1)
            sk, q = engine.skill(k), engine.question(k, qid)
            reason = "fix" if sk and q else None
        now, today = _now(), progress.today()
        for r in ([] if reason else st.get("retry", [])):
            if r["due"] <= st["n"] and r.get("after", now) <= now and r.get("day", "") < today:
                sk, q = engine.skill(r["key"]), engine.question(r["key"], r["qid"])
                if sk and q:
                    reason = "retry"
                    break
        if not reason:
            sk, reason = pick_skill(skills, mm)
            q = pick_question(sk, mm.get(sk["key"], {}).get("seen", []))
        pub, key = engine.serve(q)
        token = await items.issue(pupil, subject, key, {"skill": sk["key"], "qid": q["id"], "reason": reason})
        await db.bank_state.update_one({"_id": st["_id"]}, {"$inc": {"n": 1}})
        return {"token": token, **pub, "skill": sk["title"], "strand": sk["strand"], "reason": reason,
                "score": mm.get(sk["key"], {}).get("score", 0)}

    async def check(pupil: dict, token: str, value, ms: int | None) -> dict | None:
        it = await items.claim(pupil, subject, token)
        if not it:
            return None
        key, meta = it["answer"], it["meta"]
        correct = engine.mark(key, value)
        sk, q = engine.skill(meta["skill"]), engine.question(meta["skill"], meta["qid"])
        detail = f"{meta['skill']}#{meta['qid']}"
        slipped = [] if correct else engine.slips(key, value, (q or {}).get("q", ""))
        if slipped and not it.get("retried"):
            # a science word with a spelling slip ("respiraton"): one free retry, nothing recorded yet
            await db.items.update_one({"_id": it["_id"]}, {"$set": {"done": False, "retried": True}})
            return {"correct": False, "retry": True, "hint": typos.RETRY}
        if correct and detail in await items.just_shown(pupil, subject):
            return await _copied(pupil, subject, key, value, q, ms, detail)
        doc = await db.bank_mastery.find_one({"_id": f"{pupil['_id']}:{meta['skill']}"}) or {}
        score, streak = int(doc.get("score", 0)), int(doc.get("streak", 0))
        if correct:
            streak += 1
            score = min(MASTERED, score + gain(score, streak))
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
        elif correct and meta.get("reason") == "retry" and tries < MAX_RETRIES:
            # put right after a gap: asked once more on a later day, to see that it stayed
            retry.append({"key": meta["skill"], "qid": meta["qid"], "due": 0, "tries": MAX_RETRIES,
                          "day": progress.today()})
        await db.bank_state.update_one({"_id": st["_id"]}, {"$set": {"retry": retry[-10:]}})
        out = await _feedback(pupil, subject, key, value, q, ms, detail, correct)
        out.update({"mastered": score >= MASTERED and not doc.get("mastered_at"), "score": score})
        if slipped:                          # after the retry: which word was misspelt
            out["hint"] = typos.corrections(slipped)
        return out

    async def _feedback(pupil, subject, key, value, q, ms, detail, correct) -> dict:
        prompt = (q or {}).get("q", "")
        if q and q.get("s") and q["t"] in ("tap", "write"):
            prompt += " " + q["s"].replace("[", "").replace("]", "")
        exp = engine.expected_text(key)
        await progress.record(pupil, subject, correct, ms, detail, prompt, exp, engine.given_text(key, value))
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
        out = await _feedback(pupil, subject, key, value, q, ms, "", True)
        sc = await db.bank_mastery.find_one({"_id": f"{pupil['_id']}:{detail.split('#')[0]}"}) or {}
        out.update({"mastered": False, "score": int(sc.get("score", 0)), "again_later": True})
        return out

    async def summary(pupil: dict) -> dict:
        skills = engine.skills(subject, pupil.get("year", 3))
        mm = await _mastery(pupil, subject)
        mastered = sum(1 for s in skills if mm.get(s["key"], {}).get("score", 0) >= MASTERED)
        return {"mastered": mastered, "total": len(skills), "year": engine.bank_year(subject, pupil.get("year", 3))}

    return type(subject, (), {"next_question": staticmethod(next_question), "check": staticmethod(check),
                              "summary": staticmethod(summary)})


grammar = make("grammar")
science = make("science")
