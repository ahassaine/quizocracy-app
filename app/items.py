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
