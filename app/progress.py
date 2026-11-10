"""Every answer is one row in `attempts`; the day's progress and the family board are read from it."""
import datetime
import math
from fractions import Fraction
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
    """Wrong answers on these days, newest day first: [{"day", "items": [...], "fixed": [...]}], each
    {activity, q, exp, got, earlier, times}. The same question missed twice in a day shows once, with a count
    and every different wrong answer (earlier). A mistake is "fixed" by the same rule as open_mistakes: the
    same item was answered right afterwards."""
    still = {(a, d) for a, ds in (await open_mistakes(pupil, len(days) if days else 7)).items() for d in ds}
    by_day: dict = {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": days}, "correct": False,
                                     "q": {"$exists": True}}).sort("ts", 1):
        items = by_day.setdefault(r["day"], {})
        k = (r["activity"], r["q"], r.get("exp", ""))
        got = r.get("got", "")
        if k in items:
            it = items[k]
            it["times"] += 1
            if it["got"] != got and it["got"] not in it["earlier"]:
                it["earlier"].append(it["got"])
            it["got"] = got
        else:
            items[k] = {"activity": r["activity"], "q": r["q"], "exp": r.get("exp", ""), "got": got, "earlier": [],
                        "times": 1, "detail": r.get("detail") or ""}
    out = []
    for d in sorted(by_day, reverse=True):
        its = list(by_day[d].values())
        out.append({"day": d, "items": [i for i in its if not i["detail"] or (i["activity"], i["detail"]) in still],
                    "fixed": [i for i in its if i["detail"] and (i["activity"], i["detail"]) not in still]})
    return out


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


def day_status(pupil: dict, family: dict, day_counts: dict, day: str | None = None) -> dict:
    """Progress of one child on one day, against the plan of that day: per activity and overall percent.
    Percents are rounded down (exact fractions), so 100% and a reward "at 100%" come only when every activity
    is complete. A day that reached 100% or earned its reward keeps it (pupil.kept), whatever changes later."""
    day = day or today()
    items, total = [], Fraction(0)
    plan = todays_plan(pupil, family, day)
    for a in plan:
        c = day_counts.get(a["key"], {"correct": 0, "answered": 0})
        done = min(a["target"], c["correct"])
        frac = Fraction(done, a["target"])
        total += frac
        items.append({**a, "done": done, "correct": c["correct"], "answered": c["answered"],
                      "extra": max(0, c["correct"] - a["target"]), "pct": math.floor(100 * frac),
                      "complete": done >= a["target"]})
    pct = math.floor(100 * total / len(plan)) if plan else 0
    kept = (pupil.get("kept") or {}).get(day) or {}
    return {"items": items, "pct": max(pct, int(kept.get("pct") or 0)), "kept": kept}


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
        st = day_status(p, family, c.get(p["_id"], {}).get(day, {}), day)
        reward, kept = reward_for(p, family), st["kept"]
        earned = bool(reward.get("text")) and st["pct"] >= int(reward.get("threshold") or 100)
        if kept.get("reward"):                    # earned earlier today: never taken back, and the same reward
            reward, earned = {**reward, "text": kept["reward"]}, True
        if (earned or st["pct"] >= 100) and day == today() and (st["pct"] > int(kept.get("pct") or 0)
                                                              or (earned and not kept.get("reward"))):
            await _keep(p, day, st["pct"], reward.get("text", "") if earned else "")
        out.append({"pupil": p, **st, "reward": reward, "reward_earned": earned})
    return out


async def _keep(pupil: dict, day: str, pct: int, reward: str) -> None:
    """Remember that this day reached pct (and earned reward), so a later change of plan or reward cannot
    take it back. Days older than a month are dropped."""
    old = sorted(d for d in (pupil.get("kept") or {}) if d < day_list(31)[0])
    upd = {"$set": {f"kept.{day}": {"pct": pct, "reward": reward or (pupil.get("kept") or {}).get(day, {}).get("reward", "")}}}
    if old:
        upd["$unset"] = {f"kept.{d}": "" for d in old}
    await db.pupils.update_one({"_id": pupil["_id"]}, upd)
    pupil.setdefault("kept", {})[day] = upd["$set"][f"kept.{day}"]


def first_day(pupil: dict) -> str:
    """The child's first day in the app (local date), or "" if unknown."""
    c = pupil.get("created")
    if not isinstance(c, datetime.datetime):
        return ""
    return c.replace(tzinfo=datetime.timezone.utc).astimezone(TZ).date().isoformat()


async def history(pupil: dict, family: dict, n: int = 14) -> list:
    """The last n days, from the child's first day on, each against the plan it had that day."""
    days = [d for d in day_list(n) if d >= first_day(pupil)]
    c = await counts([pupil["_id"]], days)
    st = (await day_stats([pupil["_id"]], days)).get(pupil["_id"], {})
    return [{"day": d, **day_status(pupil, family, c.get(pupil["_id"], {}).get(d, {}), d),
             "stats": st.get(d) or _no_stats()} for d in days]


QUICK_MS = 1500           # a wrong answer this fast was not really tried
COPY_MS = 60000           # a right answer this soon after being shown the answer may be a copy
ROWS = "qwertyuiop", "asdfghjkl", "zxcvbnm"
GAP_MS = 120000           # longer pauses between answers do not count as time spent


def _no_stats() -> dict:
    return {"answers": 0, "first": 0, "first_right": 0, "first_pct": None, "minutes": 0, "rushed": 0, "copied": 0}


def _mashed(got: str, exp: str) -> bool:
    """Structure only, never meaning: blank; one key held or a straight run along one keyboard row (aaaa, asdf,
    qwertyuio); or a single character where the answer is much longer."""
    g = (got or "").strip().lower()
    if not g:
        return True
    row = next((r for r in ROWS if len(g) >= 4 and set(g) <= set(r)), None)
    if row and g not in str(exp or "").lower():
        steps = {row.index(b) - row.index(a) for a, b in zip(g, g[1:])}
        if steps in ({0}, {1}, {-1}) or (len(g) >= 6 and steps <= {-1, 0, 1}):
            return True
    return len(g) == 1 and len(str(exp or "").strip()) >= 6


async def day_stats(pupil_ids: list, days: list) -> dict:
    """How each day went, beyond the target: {pupil_id: {day: {answers, first (answers that were a first try),
    first_right, first_pct, minutes, rushed, copied}}}. A first try is an answer not straight after a wrong
    answer to the same item; minutes add up the time between answers, without long pauses; rushed = wrong answers given in under QUICK_MS or that look like random keys;
    copied = right answers to an item within COPY_MS of getting it wrong (the answer was on screen)."""
    out: dict = {}
    rows = db.attempts.find({"pupil_id": {"$in": pupil_ids}, "day": {"$in": days}},
                            {"pupil_id": 1, "day": 1, "activity": 1, "detail": 1, "correct": 1, "ms": 1, "ts": 1,
                             "got": 1, "exp": 1}).sort("ts", 1)
    wrong_at: dict = {}
    last_ts: dict = {}
    async for r in rows:
        s = out.setdefault(r["pupil_id"], {}).setdefault(r["day"], _no_stats())
        s["answers"] += 1
        key = (r["pupil_id"], r["activity"], r.get("detail") or "")
        # maths records the skill, and every maths question is a new one, so only the other activities repeat an item
        prev_wrong = wrong_at.get(key) if r.get("detail") and r["activity"] != "maths" else None
        ms = r.get("ms") if isinstance(r.get("ms"), (int, float)) else None
        lk = (r["pupil_id"], r["day"])
        gap = (r["ts"] - last_ts[lk]).total_seconds() * 1000 if lk in last_ts else (ms or 0)
        s["minutes"] += min(max(gap, 0), GAP_MS) / 60000
        last_ts[lk] = r["ts"]
        if prev_wrong is None:
            s["first"] += 1
            s["first_right"] += 1 if r["correct"] else 0
        elif r["correct"] and (r["ts"] - prev_wrong).total_seconds() * 1000 < COPY_MS:
            s["copied"] += 1
        if not r["correct"]:
            wrong_at[key] = r["ts"]
            if (ms is not None and ms < QUICK_MS) or ("got" in r and _mashed(r.get("got"), r.get("exp"))):
                s["rushed"] += 1
        else:
            wrong_at.pop(key, None)
    for per in out.values():
        for s in per.values():
            s["minutes"] = round(s["minutes"])
            s["first_pct"] = math.floor(100 * s["first_right"] / s["first"]) if s["first"] else None
    return out
