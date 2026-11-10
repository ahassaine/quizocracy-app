"""A served question. The answer stays on the server; a token can be answered once, by its own child."""
import datetime
import secrets

from .db import db


async def issue(pupil: dict, activity: str, answer, meta: dict | None = None) -> str:
    token = secrets.token_urlsafe(16)
    await db.items.insert_one({"_id": token, "pupil_id": pupil["_id"], "family_id": pupil["family_id"],
                               "activity": activity, "answer": answer, "meta": meta or {},
                               "created": datetime.datetime.utcnow(), "done": False})
    return token


async def claim(pupil: dict, activity: str, token: str) -> dict | None:
    """Atomically take an unanswered item belonging to this child; None if foreign, stale or already answered."""
    return await db.items.find_one_and_update(
        {"_id": str(token or ""), "pupil_id": pupil["_id"], "activity": activity, "done": False},
        {"$set": {"done": True, "answered": datetime.datetime.utcnow()}})


async def peek(pupil: dict, activity: str, token: str) -> dict | None:
    return await db.items.find_one({"_id": str(token or ""), "pupil_id": pupil["_id"], "activity": activity})


# A missed item comes back only after a real gap, so that a right answer is remembered, not copied from the
# correction just shown: at least RECALL_ITEMS other questions AND RECALL_SECONDS. A miss older than
# RECALL_STALE (a later sitting) never counts as just shown.
RECALL_ITEMS = 5
RECALL_SECONDS = 180
RECALL_STALE = 30 * 60


async def just_shown(pupil: dict, activity: str) -> set:
    """Items (the `detail` of progress.record) whose answer this child was shown too recently to be asked again."""
    return set(await waits(pupil, activity))


async def waits(pupil: dict, activity: str) -> dict:
    """{item: seconds before it may come back (0: only questions are missing)} for each item whose answer this
    child was shown too recently: missed, or answered right straight after being shown (copied), which starts
    the gap again. For maths the item is the mistake ("skill@row id", progress.mistake_key)."""
    now = datetime.datetime.utcnow()
    rows = [r async for r in db.attempts.find(
        {"pupil_id": pupil["_id"], "activity": activity, "ts": {"$gt": now - datetime.timedelta(seconds=RECALL_STALE)}},
        {"detail": 1, "correct": 1, "ts": 1, "copied": 1}).sort("ts", 1)]
    out: dict = {}
    for i, r in enumerate(rows):
        if (not r["correct"] or r.get("copied")) and r.get("detail"):
            k = f"{r['detail']}@{r['_id']}" if activity == "maths" else r["detail"]
            secs = RECALL_SECONDS - (now - r["ts"]).total_seconds()
            if len(rows) - 1 - i < RECALL_ITEMS or secs > 0:
                out[k] = max(0, round(secs))
            else:
                out.pop(k, None)
    return out


async def last_detail(pupil: dict, activity: str) -> str | None:
    """The item (detail) of this child's last answer in this activity in this sitting, if any."""
    r = await db.attempts.find_one(
        {"pupil_id": pupil["_id"], "activity": activity,
         "ts": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(seconds=RECALL_STALE)}},
        {"detail": 1}, sort=[("ts", -1)])
    return (r or {}).get("detail") or None


async def last_answered(pupil: dict, activity: str) -> dict | None:
    """The item this child answered last in this activity (its meta, with its answer), so it is never asked
    again straight away."""
    return await db.items.find_one({"pupil_id": pupil["_id"], "activity": activity, "done": True},
                                   {"meta": 1, "answer": 1}, sort=[("answered", -1)])
