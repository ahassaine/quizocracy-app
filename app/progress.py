"""Every answer is one row in `attempts`; the day's progress and the family board are read from it."""
import datetime
import difflib
import math
import re
from fractions import Fraction
from zoneinfo import ZoneInfo

from . import config
from .activities import acts_on, back_on, next_day, plan_of, rest_day, todays_plan
from .db import db

TZ = ZoneInfo(config.TIMEZONE)


def today() -> str:
    return datetime.datetime.now(TZ).date().isoformat()


def day_list(n: int) -> list:
    d = datetime.datetime.now(TZ).date()
    return [(d - datetime.timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


async def record(pupil: dict, activity: str, correct: bool, ms: int | None = None, detail: str = "",
                 question: str = "", expected: str = "", given: str = "", copied: bool = False, like: str = "",
                 extra: dict | None = None) -> None:
    """detail: the item answered (fact, word, verb, number, skill#question; for maths the skill). copied: right,
    but straight after being shown the answer (it counts for today, never as a mistake put right). like: a
    maths question answered right, kept so it can put right an earlier maths mistake like it (alike)."""
    row = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "activity": activity,
           "correct": bool(correct), "ms": ms, "detail": detail[:80], "day": today(),
           "ts": datetime.datetime.utcnow()}
    if copied:
        row["copied"] = True
    if correct and like:
        row["lq"] = str(like)[:400]
    if not correct and question:          # a mistake keeps what was asked, so the parent can go over it later
        row.update({"q": str(question)[:400], "exp": str(expected)[:200], "got": str(given or "")[:200], **(extra or {})})
    await db.attempts.insert_one(row)


# A maths question is made fresh each time, so a maths mistake cannot come back word for word. It is put right
# by a later right answer to a question LIKE it: the same skill, the same shape (the same symbols in the same
# order once numbers are blanked) and nearly the same words (names and objects may change). Structure only.
_NUM_WORDS = (r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
              r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
              r"thousand|million)(?:-\w+)?")
LIKE_RATIO = 0.75


def _shape(prompt: str) -> tuple:
    p = re.sub(r"\d+(?:[.,]\d+)*", "#", prompt or "")
    p = re.sub(r"\b" + _NUM_WORDS + r"\b", "#", p, flags=re.I)
    # "five hundred and thirty" and "two hundred" are both one number: a run of blanks counts as one
    return re.sub(r"#+", "#", re.sub(r"[A-Za-z\s]+", "", p)), re.findall(r"[a-z]+|#", p.lower())


def alike(a: str, b: str) -> bool:
    """Two maths prompts of one skill are the same kind of question with other numbers (see above)."""
    (sa, wa), (sb, wb) = _shape(a), _shape(b)
    return sa == sb and difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio() >= LIKE_RATIO


async def _scan(pupil: dict, days: list) -> list:
    """Every mistake on these days, oldest first, each with when it was put right (None: not yet). A mistake is
    put right only by a later right answer to THAT item: the same fact, word, verb, number or bank question
    (detail), or for maths a question like it (alike). A right answer copied straight after the correction
    puts nothing right. Once put right a mistake stays put right; missing the item again is a new mistake."""
    out, waiting = [], {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": days}, "detail": {"$nin": ["", None]},
                                     "copied": {"$ne": True}},
                                    {"activity": 1, "detail": 1, "correct": 1, "ts": 1, "q": 1, "lq": 1, "nolike": 1}).sort("ts", 1):
        k = (r["activity"], r["detail"])
        if not r["correct"]:
            m = {"id": r["_id"], "activity": r["activity"], "detail": r["detail"], "ts": r["ts"], "q": r.get("q", ""),
                 "fixed": None, "nolike": bool(r.get("nolike"))}
            out.append(m)
            waiting.setdefault(k, []).append(m)
            continue
        if r["activity"] == "maths":
            if not r.get("lq"):
                continue
            hit = [m for m in waiting.get(k, []) if alike(m["q"], r["lq"])]
            waiting[k] = [m for m in waiting.get(k, []) if m not in hit]
        else:
            hit = waiting.pop(k, [])
        for m in hit:
            m["fixed"] = r["ts"]
    return out


def mistake_key(m: dict) -> str:
    """What "Practise my mistakes" asks again: the item, or for maths "skill@mistake" (a question like that one)."""
    return f"{m['detail']}@{m['id']}" if m["activity"] == "maths" else m["detail"]


async def open_mistakes(pupil: dict, days: int = 7) -> dict:
    """Mistakes not put right yet: {activity: [key, ...]} (mistake_key), the longest-waiting first, one per item
    (maths: one per kind of question). Maths mistakes no question like them could be made for stay on the
    parent's list but are not asked again (nolike)."""
    out: dict = {}
    for m in await _scan(pupil, day_list(days)):
        if m["fixed"] or m["nolike"]:
            continue
        keys = out.setdefault(m["activity"], {})
        same = next((k for k, o in keys.items() if o["detail"] == m["detail"]
                     and (m["activity"] != "maths" or alike(o["q"], m["q"]))), None)
        if same:
            del keys[same]                    # the latest miss of the item stands for it (its gap counts)
        keys[mistake_key(m)] = m
    return {a: list(ks) for a, ks in out.items() if ks}


async def mistakes(pupil: dict, days: list) -> list:
    """Wrong answers on these days, newest day first: [{"day", "items": [...], "fixed": [...]}], each
    {activity, q, exp, got, earlier, times, like}. The same question missed twice in a day shows once, with a
    count and every different wrong answer (earlier). It is "fixed" (put right) when its last miss was put right
    (see _scan); like: put right by a maths question like it, not by the same question."""
    fixed = {m["id"]: m["fixed"] for m in await _scan(pupil, days)}
    by_day: dict = {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": days}, "correct": False,
                                     "q": {"$exists": True}}).sort("ts", 1):
        items = by_day.setdefault(r["day"], {})
        k = (r["activity"], r["q"], r.get("exp", ""))
        got = r.get("got", "")
        if k in items and items[k]["fixed"]:     # missed again after it was put right: a new mistake, the old stays
            items[(k, len(items))] = items.pop(k)
        if k in items:
            it = items[k]
            it["times"] += 1
            if it["got"] != got and it["got"] not in it["earlier"]:
                it["earlier"].append(it["got"])
            it["got"] = got
        else:
            items[k] = it = {"activity": r["activity"], "q": r["q"], "exp": r.get("exp", ""), "got": got, "earlier": [],
                             "times": 1, "like": r["activity"] == "maths"}
        it["fixed"] = bool(fixed.get(r["_id"]))
    out = []
    for d in sorted(by_day, reverse=True):
        its = list(by_day[d].values())
        out.append({"day": d, "items": [i for i in its if not i["fixed"]], "fixed": [i for i in its if i["fixed"]]})
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
    is complete. A day that reached 100% or earned its reward keeps it (pupil.kept), whatever changes later.
    On a rest day (rest: "off" or "week", see activities.rest_day) nothing is due: every right answer is extra,
    and the day shows as rest, not as 0%; only what it had already kept stays. rest_next: tomorrow's rest ("off",
    "week" or ""), and back: the next practice day after it, so every screen can say "Tomorrow is a day off"."""
    day = day or today()
    items, total = [], Fraction(0)
    plan = todays_plan(pupil, family, day)
    rest = rest_day(pupil, day)
    for a in plan:
        c = day_counts.get(a["key"], {"correct": 0, "answered": 0})
        done = min(a["target"], c["correct"])
        frac = Fraction(done, a["target"])
        check = check_due(pupil, day) if a["key"] == "tables" else None
        if check:                     # "and a Year 4 check": the check is one more step of the times tables
            frac = Fraction(done + check["done"], a["target"] + 1)
        total += frac
        items.append({**a, "done": done, "correct": c["correct"], "answered": c["answered"],
                      "extra": c["correct"] if rest else max(0, c["correct"] - a["target"]),
                      "pct": math.floor(100 * frac), "complete": frac >= 1, "check": check})
    pct = 0 if rest else math.floor(100 * total / len(plan)) if plan else 0
    kept = (pupil.get("kept") or {}).get(day) or {}
    return {"items": items, "pct": max(pct, int(kept.get("pct") or 0)), "kept": kept, "rest": rest,
            "extra": sum(c.get("correct", 0) for c in day_counts.values()) if rest else 0,
            "rest_next": rest_day(pupil, next_day(day)), "back": back_on(pupil, day) if rest or rest_day(pupil, next_day(day)) else ""}


CHECK_YEARS = (3, 4, 5, 6)      # the years the Year 4 multiplication check is worth practising for


def check_due(pupil: dict, day: str) -> dict | None:
    """When the parent made a Year 4 check part of the times-tables target ("check" in the plan's tables, Years 3
    to 6): {"done": 1 if a check was finished that day, else 0}; otherwise None."""
    t = (acts_on(pupil, day) or {}).get("tables") or {}
    if not t.get("check") or pupil.get("year") not in CHECK_YEARS:
        return None
    return {"done": int(any(r.get("day") == day for r in pupil.get("mtc") or []))}


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
                             "got": 1, "exp": 1, "copied": 1}).sort("ts", 1)
    wrong_at: dict = {}
    last_ts: dict = {}
    async for r in rows:
        s = out.setdefault(r["pupil_id"], {}).setdefault(r["day"], _no_stats())
        s["answers"] += 1
        key = (r["pupil_id"], r["activity"], "" if r.get("copied") else r.get("detail") or "")
        # maths records the skill, and every maths question is a new one, so only the other activities repeat an item
        prev_wrong = wrong_at.get(key) if key[2] and r["activity"] != "maths" else None
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
