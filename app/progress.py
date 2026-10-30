"""Every answer is one row in `attempts`; the day's progress and the family board are read from it."""
import datetime
from zoneinfo import ZoneInfo

from . import config
from .activities import todays_plan
from .db import db

TZ = ZoneInfo(config.TIMEZONE)


def today() -> str:
    return datetime.datetime.now(TZ).date().isoformat()


def day_list(n: int) -> list:
    d = datetime.datetime.now(TZ).date()
    return [(d - datetime.timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


async def record(pupil: dict, activity: str, correct: bool, ms: int | None = None, detail: str = "") -> None:
    await db.attempts.insert_one({
        "pupil_id": pupil["_id"], "family_id": pupil["family_id"], "activity": activity,
        "correct": bool(correct), "ms": ms, "detail": detail[:80], "day": today(),
        "ts": datetime.datetime.utcnow(),
    })


async def counts(pupil_ids: list, days: list) -> dict:
    """{pupil_id: {day: {activity: {"correct": n, "answered": m}}}}"""
    out: dict = {}
    pipe = [{"$match": {"pupil_id": {"$in": pupil_ids}, "day": {"$in": days}}},
            {"$group": {"_id": {"p": "$pupil_id", "d": "$day", "a": "$activity"},
                        "answered": {"$sum": 1}, "correct": {"$sum": {"$cond": ["$correct", 1, 0]}}}}]
    async for r in db.attempts.aggregate(pipe):
        k = r["_id"]
        out.setdefault(k["p"], {}).setdefault(k["d"], {})[k["a"]] = {"correct": r["correct"], "answered": r["answered"]}
    return out


def day_status(pupil: dict, family: dict, day_counts: dict) -> dict:
    """Progress of one child on one day: per activity and overall percent."""
    items, total = [], 0.0
    plan = todays_plan(pupil, family)
    for a in plan:
        c = day_counts.get(a["key"], {"correct": 0, "answered": 0})
        done = min(a["target"], c["correct"])
        frac = done / a["target"]
        total += frac
        items.append({**a, "done": done, "correct": c["correct"], "answered": c["answered"],
                      "pct": int(round(100 * frac)), "complete": done >= a["target"]})
    pct = int(round(100 * total / len(plan))) if plan else 0
    return {"items": items, "pct": pct}


async def board(family: dict, pupils: list, day: str | None = None) -> list:
    day = day or today()
    c = await counts([p["_id"] for p in pupils], [day])
    reward = family.get("reward") or {}
    out = []
    for p in pupils:
        st = day_status(p, family, c.get(p["_id"], {}).get(day, {}))
        earned = bool(reward.get("text")) and st["pct"] >= int(reward.get("threshold") or 100)
        out.append({"pupil": p, **st, "reward_earned": earned})
    return out


async def history(pupil: dict, family: dict, n: int = 14) -> list:
    days = day_list(n)
    c = await counts([pupil["_id"]], days)
    return [{"day": d, **day_status(pupil, family, c.get(pupil["_id"], {}).get(d, {}))} for d in days]
