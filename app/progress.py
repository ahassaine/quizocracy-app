"""Every answer is one row in `attempts`; the day's progress and the family board are read from it."""
import datetime
from zoneinfo import ZoneInfo

from . import config
from .activities import plan_of, todays_plan
from .db import db

TZ = ZoneInfo(config.TIMEZONE)


def today() -> str:
    return datetime.datetime.now(TZ).date().isoformat()


def day_list(n: int) -> list:
    d = datetime.datetime.now(TZ).date()
    return [(d - datetime.timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


async def record(pupil: dict, activity: str, correct: bool, ms: int | None = None, detail: str = "",
                 question: str = "", expected: str = "", given: str = "") -> None:
    row = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "activity": activity,
           "correct": bool(correct), "ms": ms, "detail": detail[:80], "day": today(),
           "ts": datetime.datetime.utcnow()}
    if not correct and question:          # a mistake keeps what was asked, so the parent can go over it later
        row.update({"q": str(question)[:400], "exp": str(expected)[:200], "got": str(given or "")[:200]})
    await db.attempts.insert_one(row)


async def open_mistakes(pupil: dict, days: int = 7) -> dict:
    """Mistakes not put right yet: {activity: [detail, ...]}, the longest-waiting first. A mistake is put right
    when the same item (fact, word, verb, number, skill or question) is answered correctly afterwards."""
    last: dict = {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": day_list(days)}, "detail": {"$nin": ["", None]}},
                                    {"activity": 1, "detail": 1, "correct": 1, "ts": 1}).sort("ts", 1):
        last[(r["activity"], r["detail"])] = (r["correct"], r["ts"])
    out: dict = {}
    for (act, det), (ok, ts) in sorted(last.items(), key=lambda kv: kv[1][1]):
        if not ok:
            out.setdefault(act, []).append(det)
    return out


async def mistakes(pupil: dict, days: list) -> list:
    """Wrong answers on these days, newest day first: [{"day", "items": [{activity, q, exp, got, times}]}].
    The same question missed twice in a day shows once, with a count."""
    by_day: dict = {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": days}, "correct": False,
                                     "q": {"$exists": True}}).sort("ts", 1):
        items = by_day.setdefault(r["day"], {})
        k = (r["activity"], r["q"], r.get("exp", ""))
        if k in items:
            items[k]["times"] += 1
            items[k]["got"] = r.get("got", "")
        else:
            items[k] = {"activity": r["activity"], "q": r["q"], "exp": r.get("exp", ""), "got": r.get("got", ""), "times": 1}
    return [{"day": d, "items": list(by_day[d].values())} for d in sorted(by_day, reverse=True)]


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


def reward_for(pupil: dict, family: dict) -> dict:
    """The child's own reward if the parent set one, otherwise the family's; none without the rewards plan."""
    if not plan_of(family)["rewards"]:
        return {}
    own = pupil.get("reward") or {}
    return own if own.get("text") else (family.get("reward") or {})


async def board(family: dict, pupils: list, day: str | None = None) -> list:
    day = day or today()
    c = await counts([p["_id"] for p in pupils], [day])
    out = []
    for p in pupils:
        st = day_status(p, family, c.get(p["_id"], {}).get(day, {}))
        reward = reward_for(p, family)
        earned = bool(reward.get("text")) and st["pct"] >= int(reward.get("threshold") or 100)
        out.append({"pupil": p, **st, "reward": reward, "reward_earned": earned})
    return out


async def history(pupil: dict, family: dict, n: int = 14) -> list:
    days = day_list(n)
    c = await counts([pupil["_id"]], days)
    return [{"day": d, **day_status(pupil, family, c.get(pupil["_id"], {}).get(d, {}))} for d in days]
