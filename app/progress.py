"""Every answer is one row in `attempts`; the day's progress and the family board are read from it."""
import contextvars
import datetime
import difflib
import math
import re
from fractions import Fraction
from zoneinfo import ZoneInfo

from . import config
from .activities import ACTIVITIES, YOUNG_CAP, acts_on, has_cap, back_on, minutes, next_day, plan_of, rest_day, todays_plan
from .db import db

TZ = ZoneInfo(config.TIMEZONE)


def today() -> str:
    return datetime.datetime.now(TZ).date().isoformat()


def pct(part: int, whole: int) -> int | None:
    """THE one rounding of every percent a parent reads: to the nearest whole number (2 of 3 is 67%, 1 of 8 is 13%),
    but never 100% short of the whole, nor 0% with something done. None when there is nothing to count."""
    if not whole:
        return None
    p = (200 * part + whole) // (2 * whole)
    return p if part >= whole else 0 if part <= 0 else max(1, min(p, 99))


# Set by routes/child.api_check while it checks the answer to a "Practise my mistakes" question: "fix", or "fixing"
# when the question was the mistake itself. record() marks the row with it, so the parent's figures count mistake
# practice on its own, never as extra practice (day_stats).
FIX_MODE: contextvars.ContextVar = contextvars.ContextVar("fix_mode", default="")


def day_list(n: int) -> list:
    d = datetime.datetime.now(TZ).date()
    return [(d - datetime.timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


async def record(pupil: dict, activity: str, correct: bool, ms: int | None = None, detail: str = "",
                 question: str = "", expected: str = "", given: str = "", copied: bool = False, like: str = "",
                 extra: dict | None = None, src: str = "") -> None:
    """detail: the item answered (fact, word, verb, number, skill#question; for maths the skill). copied: right,
    but straight after being shown the answer (it counts for today, never as a mistake put right). like: a
    maths question answered right, kept so it can put right an earlier maths mistake like it (alike). src:
    "mtc" for an answer of the timed Year 4 check (its time-outs are never "rushed"; see day_stats)."""
    row = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "activity": activity,
           "correct": bool(correct), "ms": ms, "detail": detail[:80], "day": today(),
           "ts": datetime.datetime.utcnow()}
    if copied:
        row["copied"] = True
    if src:
        row["src"] = src
    if FIX_MODE.get():
        row["fix"] = True
        if FIX_MODE.get() == "fixing":
            row["fixing"] = True
    if correct and like:
        row["lq"] = str(like)[:400]
    if not correct and question:          # a mistake keeps what was asked, so the parent can go over it later
        # an answer of 0 (a number line's arrow on 0) is an answer, not a blank
        row.update({"q": str(question)[:400], "exp": str(expected)[:200], "got": "" if given is None else str(given)[:200],
                    **(extra or {})})
    await db.attempts.insert_one(row)


# A maths question is made fresh each time, so a maths mistake cannot come back word for word. It is put right
# by a later right answer to a question LIKE it: the same skill, the same shape (the same symbols in the same
# order once numbers are blanked) and nearly the same words (names and objects may change). Structure only.
_NUM_WORDS = (r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
              r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
              r"thousand|million)(?:-\w+)?")
LIKE_RATIO = 0.75


def _shape(prompt: str) -> tuple:
    # a sign that belongs to the number ("-24" in a list, not "10 − 4" or "3x − 4") and an ordinal ("4th") are
    # part of the number, so "Which number is 4th? -24, 7, -3" is like "Which is 2nd? 5, -18, -9"
    p = re.sub(r"(?<![\w)\]])[-−]?\d+(?:[.,]\d+)*(?:st|nd|rd|th)?\b|\d+(?:[.,]\d+)*", "#", prompt or "")
    p = re.sub(r"\b" + _NUM_WORDS + r"\b", "#", p, flags=re.I)
    # "five hundred and thirty" and "two hundred" are both one number: a run of blanks counts as one
    return re.sub(r"#+", "#", re.sub(r"[A-Za-z\s]+", "", p)), re.findall(r"[a-z]+|#", p.lower())


def alike(a: str, b: str) -> bool:
    """Two maths prompts of one skill are the same kind of question with other numbers (see above)."""
    (sa, wa), (sb, wb) = _shape(a), _shape(b)
    return sa == sb and difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio() >= LIKE_RATIO


# Grammar, science and spelling ask a missed question again word for word, so getting it right in the same
# sitting may only be remembering the answer just shown: that is practice (practised), and the mistake is put
# right only by a right answer at least PUT_RIGHT_AFTER after the miss (a later sitting or day).
LATER_SITTING = ("grammar", "science", "spelling")
PUT_RIGHT_AFTER = datetime.timedelta(hours=1)


async def last_miss(pupil: dict, activity: str, detail: str, days: int = 7) -> datetime.datetime | None:
    """When this child last got this item wrong (in the last few days), or None: a right answer to it then is a
    repeat of a missed question, which never makes a skill mastered."""
    r = await db.attempts.find_one({"pupil_id": pupil["_id"], "activity": activity, "detail": detail,
                                    "correct": False, "day": {"$in": day_list(days)}}, {"ts": 1}, sort=[("ts", -1)])
    return r["ts"] if r else None


def same_item(activity: str, detail: str) -> str:
    """What one mistake is about: the item, except that a times-tables fact and its reverse are one fact (7 × 12
    and 12 × 7: the same thing to learn, as the Year 4 check and tables.next_question already treat them)."""
    m = re.fullmatch(r"(\d+)x(\d+)", detail or "") if activity == "tables" else None
    return "x".join(sorted(m.groups(), key=int)) if m else detail


async def _scan(pupil: dict, days: list) -> list:
    """Every mistake on these days, oldest first, each with when it was put right (None: not yet). A mistake is
    put right only by a later right answer to THAT item: the same fact (either way round), word, verb, number or
    bank question (detail), or for maths a question like it (alike); in grammar, science and spelling only once
    the miss is PUT_RIGHT_AFTER old (sooner, it is practised: asked again in a later sitting). A right answer
    copied straight after the correction puts nothing right. Once put right a mistake stays put right; missing
    the item again is a new mistake. In "Practise my mistakes" (the row's fix): a wrong answer to a question asked
    while a mistake waits for its gap (not "fixing") is never a mistake, so a round never ends with more mistakes
    than it began with; the mistake itself missed again ("fixing") rests (rest), as one right again does."""
    out, waiting = [], {}
    async for r in db.attempts.find({"pupil_id": pupil["_id"], "day": {"$in": days}, "detail": {"$nin": ["", None]},
                                     "copied": {"$ne": True}},
                                    {"activity": 1, "detail": 1, "correct": 1, "ts": 1, "q": 1, "lq": 1, "nolike": 1,
                                     "exp": 1, "got": 1, "day": 1, "idk": 1, "fix": 1, "fixing": 1}).sort("ts", 1):
        k = (r["activity"], same_item(r["activity"], r["detail"]))
        if not r["correct"]:
            if r.get("fix") and not r.get("fixing"):
                continue                     # a filler question of "Practise my mistakes": a miss, not a mistake
            m = {"id": r["_id"], "activity": r["activity"], "detail": r["detail"], "ts": r["ts"], "q": r.get("q", ""),
                 "fixed": None, "nolike": bool(r.get("nolike")), "practised": None, "day": r.get("day", ""),
                 "exp": r.get("exp", ""), "got": r.get("got", ""), "asked": "q" in r, "rest": bool(r.get("fixing")),
                 "idk": bool(r.get("idk")) or _said_idk(r.get("got", ""))}     # "I don't know": said neutrally
            out.append(m)
            waiting.setdefault(k, []).append(m)
            continue
        if r["activity"] == "maths":
            if not r.get("lq"):
                continue
            hit = [m for m in waiting.get(k, []) if alike(m["q"], r["lq"])]
            waiting[k] = [m for m in waiting.get(k, []) if m not in hit]
        elif r["activity"] in LATER_SITTING:
            hit = [m for m in waiting.get(k, []) if r["ts"] - m["ts"] >= PUT_RIGHT_AFTER]
            waiting[k] = [m for m in waiting.get(k, []) if m not in hit]
            for m in waiting[k]:
                m["practised"] = r["ts"]
        else:
            hit = waiting.pop(k, [])
        for m in hit:
            m["fixed"] = r["ts"]
    return out


def mistake_key(m: dict) -> str:
    """What "Practise my mistakes" asks again: the item, or for maths "skill@mistake" (a question like that one)."""
    return f"{m['detail']}@{m['id']}" if m["activity"] == "maths" else m["detail"]


async def mistake_book(pupil: dict, days: list | None = None, plan: set | None = None,
                       before: datetime.datetime | None = None) -> list:
    """THE one rule behind every count of mistakes: the child's "Practise my mistakes (N)" and its countdown,
    "N come back later", "This week: N put right", the parent's "N to go over · N put right", "Still tricky" in
    the school words and the printed report all read this list, so they always agree.

    One entry per thing to learn (an item: a word, a fact either way round, a verb, a bank question; for maths a
    kind of question), from its misses in these days (the last 7 by default), oldest first. Its latest miss stands
    for it: {activity, key (mistake_key), detail, item, latest (the miss row of _scan), misses (all of them), state,
    practised, back, again, fixed}. state:
      - "fixed": put right (its latest miss was put right by a later right answer, see _scan);
      - "cannot": not put right, but the app won't ask it again (no question like it could be made, or its
        activity is not in `plan`): the parent sees it on a quieter line, the child never counts it;
      - "later": right again in the same sitting (practised), or missed again in "Practise my mistakes": it rests
        until `back` (PUT_RIGHT_AFTER after the miss), then it is due again;
      - "due": to put right now.
    again: it had been put right, then was missed again (it shows once, as to go over, never also as put right).
    before: only items whose latest miss is older than this (the queue of a "Practise my mistakes" session that
    started then: what is missed during it waits for the next one); the others are left out."""
    now = datetime.datetime.utcnow()
    out: list = []
    by_item: dict = {}
    for m in await _scan(pupil, days or day_list(7)):
        item = same_item(m["activity"], m["detail"])
        if m["activity"] == "maths":          # one entry per kind of question of the skill
            e = next((x for x in by_item.get((m["activity"], item), []) if alike(x["latest"]["q"], m["q"])), None)
        else:
            e = (by_item.get((m["activity"], item)) or [None])[0]
        if e is None:
            e = {"activity": m["activity"], "item": item, "misses": [], "again": False}
            by_item.setdefault((m["activity"], item), []).append(e)
            out.append(e)
        if e["misses"] and e["latest"]["fixed"]:
            e["again"] = True
        e["misses"].append(m)
        e["latest"] = m
    for e in out:
        m = e["latest"]
        e.update(key=mistake_key(m), detail=m["detail"], fixed=m["fixed"], practised=bool(m["practised"] and not m["fixed"]),
                 back=m["ts"] + PUT_RIGHT_AFTER if (m["practised"] or m.get("rest")) and not m["fixed"] else None)
        # practised in "Practise my mistakes" and missed again (rest): it rests too, so the child's count goes down
        # as each mistake is practised, and the round ends ("3 come back tomorrow")
        e["state"] = ("fixed" if m["fixed"] else "cannot" if m["nolike"] or (plan is not None and m["activity"] not in plan)
                      else "later" if e["back"] and now < e["back"] else "due")
    out.sort(key=lambda e: e["latest"]["ts"])
    if before is not None:
        out = [e for e in out if e["latest"]["ts"] < before]
    return out


def book_counts(book: list) -> dict:
    """The numbers every screen shows, from mistake_book: due (to put right now), later (resting until a later
    sitting), open (due + later: the parent's "to go over"), cannot, fixed (put right), and per activity
    {activity: due}."""
    n = {s: sum(1 for e in book if e["state"] == s) for s in ("due", "later", "cannot", "fixed")}
    per: dict = {}
    for e in book:
        if e["state"] == "due":
            per[e["activity"]] = per.get(e["activity"], 0) + 1
    return {**n, "open": n["due"] + n["later"], "per": per}


EVENING = 19              # from 7 pm (UK time), what comes back later comes back tomorrow, as far as a child is concerned


def back_when(backs: list) -> str:
    """When mistakes that rest come back, in a child's words: "tomorrow" in the evening; else "in about an hour"
    or "in about 20 minutes" from the latest of `backs` (when each rests until, UTC); "next time" when they
    don't rest (missed during a "Practise my mistakes" session: they wait for the next one)."""
    now = datetime.datetime.utcnow()
    if datetime.datetime.now(TZ).hour >= EVENING:
        return "tomorrow"
    backs = [b for b in backs if b and b > now]
    if not backs:
        return "next time"
    mins = math.ceil((max(backs) - now).total_seconds() / 60)
    return "in about an hour" if mins > 40 else f"in about {max(5, 5 * math.ceil(mins / 5))} minutes"


async def open_mistakes(pupil: dict, days: int = 7) -> dict:
    """Mistakes to put right now (mistake_book, state "due"): {activity: [key, ...]} (mistake_key), the
    longest-waiting first, one per item (maths: one per kind of question)."""
    out: dict = {}
    for e in await mistake_book(pupil, day_list(days)):
        if e["state"] == "due":
            out.setdefault(e["activity"], []).append(e["key"])
    return out


async def mistakes(pupil: dict, days: list) -> list:
    """For the parent, from mistake_book: newest day first, [{"day", "items": [...], "fixed": [...]}]. Each
    item shows once, on the day of its latest miss, {activity, q, exp, got, earlier, times, like, fixed,
    practised, later, again, nolike, rid, rids}: the question and answer of its latest miss, every different
    wrong answer before (earlier) and how many misses (times). like: a maths mistake is put right by a question
    like it, not by the same question; practised: right again in the same sitting (not put right yet); later:
    so it rests until a later sitting; rids: every miss of it (a report of any of them marks it)."""
    by_day: dict = {}
    for e in await mistake_book(pupil, days):
        m = e["latest"]
        earlier = []
        for x in e["misses"][:-1]:
            if x["got"] != m["got"] and x["got"] not in earlier:
                earlier.append(x["got"])
        it = {"activity": e["activity"], "q": m["q"] or m["detail"], "exp": m["exp"], "got": m["got"], "idk": m.get("idk"),
              "earlier": earlier,
              "times": len(e["misses"]), "like": e["activity"] == "maths", "fixed": bool(e["fixed"]),
              "practised": e["practised"], "later": e["state"] == "later", "again": e["again"], "nolike": m["nolike"],
              "rid": str(m["id"]), "rids": [str(x["id"]) for x in e["misses"]],
              "days": sorted({x["day"] for x in e["misses"]})}
        by_day.setdefault(m["day"], []).append(it)
    return [{"day": d, "items": [i for i in by_day[d] if not i["fixed"]], "fixed": [i for i in by_day[d] if i["fixed"]]}
            for d in sorted(by_day, reverse=True)]


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
    Percents are rounded by pct (2 of 3 is 67%), never up to 100%, so 100% and a reward "at 100%" come only when
    every activity is complete. A day that reached 100% or earned its reward keeps it (pupil.kept), whatever changes later.
    On a rest day (rest: "off" or "week", see activities.rest_day) nothing is due: every right answer is extra,
    and the day shows as rest, not as 0%; only what it had already kept stays. rest_next: tomorrow's rest ("off",
    "week" or ""), and back: the next practice day after it, so every screen can say "Tomorrow is a day off"."""
    day = day or today()
    items, done_all, target_all = [], 0, 0
    plan = todays_plan(pupil, family, day)
    rest = rest_day(pupil, day)
    for a in plan:
        c = day_counts.get(a["key"], {"correct": 0, "answered": 0})
        done = min(a["target"], c["correct"])
        # Years 1-4 (and spelling in every year): the activity also ends after YOUNG_CAP times its target in answers,
        # so a child who finds it hard is not given the longest day of all (capped: done for today, though not every
        # answer was right; activities.has_cap)
        capped = (has_cap(pupil, a["key"]) and not rest and done < a["target"]
                  and c["answered"] >= YOUNG_CAP * a["target"])
        if capped:
            done = a["target"]
        step_done, step_target = done, a["target"]
        check = check_due(pupil, day) if a["key"] == "tables" else None
        if check:                     # "and a Year 4 check": the check counts as CHECK_ANSWERS more answers
            step_done, step_target = done + CHECK_ANSWERS * check["done"], a["target"] + CHECK_ANSWERS
        frac = Fraction(step_done, step_target)
        done_all, target_all = done_all + step_done, target_all + step_target
        items.append({**a, "done": done, "correct": c["correct"], "answered": c["answered"],
                      "extra": c["correct"] if rest else max(0, c["correct"] - a["target"]),
                      "pct": pct(step_done, step_target), "complete": frac >= 1, "check": check, "capped": capped})
    # the day's percent weighs every planned answer the same: 5 science answers of 25 planned are 20%, not half
    day_pct = 0 if rest else pct(done_all, target_all) if target_all else 0
    planned = {a["key"] for a in plan}
    # work in an activity not in that day's plan (unticked since): shown, never counted towards the day
    unplanned = [{**ACTIVITIES[k], "key": k, "correct": c["correct"], "answered": c["answered"]}
                 for k, c in day_counts.items() if k in ACTIVITIES and k not in planned and c.get("answered")]
    kept = (pupil.get("kept") or {}).get(day) or {}
    exact = 0 if rest or not target_all else 100 * done_all / target_all      # unrounded: what a reward threshold is met by
    return {"items": items, "pct": max(day_pct, int(kept.get("pct") or 0)), "exact": max(exact, int(kept.get("pct") or 0)),
            "kept": kept, "rest": rest, "unplanned": unplanned,
            "extra": sum(c.get("correct", 0) for c in day_counts.values()) if rest else 0,
            "rest_next": rest_day(pupil, next_day(day)), "back": back_on(pupil, day) if rest or rest_day(pupil, next_day(day)) else ""}


CHECK_YEARS = (3, 4, 5, 6)      # the years the Year 4 multiplication check is worth practising for
CHECK_ANSWERS = 5               # a finished Year 4 check counts as this many planned answers towards the day


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
        earned = bool(reward.get("text")) and st.get("exact", st["pct"]) >= int(reward.get("threshold") or 100)
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
    st = (await day_stats([pupil["_id"]], days, plan_targets([pupil], family, days))).get(pupil["_id"], {})
    return [{"day": d, **day_status(pupil, family, c.get(pupil["_id"], {}).get(d, {}), d),
             "stats": st.get(d) or _no_stats()} for d in days]


def plan_targets(pupils: list, family: dict, days: list) -> dict:
    """What day_stats needs to keep answers after a target out of the day's headline, and to compare the time
    spent with the plan: {pupil_id: {day: {"acts": {activity: target}, "min": planned minutes, "rest": bool}}}. A
    rest day has no targets: everything on it is extra."""
    out: dict = {}
    for p in pupils:
        for d in days:
            rest = bool(rest_day(p, d))
            plan = [] if rest else todays_plan(p, family, d)
            out.setdefault(p["_id"], {})[d] = {"acts": {a["key"]: a["target"] for a in plan}, "rest": rest,
                                               "min": minutes(plan, p.get("year", 3), bool(check_due(p, d))) if plan else 0,
                                               "year": p.get("year", 3)}
    return out


QUICK_MS = 1500           # a wrong answer this fast was not really tried
# A wrong pick (an option, or a word tapped: the row has "pick") this fast from the question appearing to Check:
# a tap of about a second and the press of Check, so the question was not read
PICK_MS = 2500
COPY_MS = 60000           # a right answer this soon after being shown the answer may be a copy
ROWS = "qwertyuiop", "asdfghjkl", "zxcvbnm"
GAP_MS = 120000           # longer pauses between answers do not count as time spent


def _no_stats() -> dict:
    return {"answers": 0, "first": 0, "first_right": 0, "first_pct": None, "minutes": 0, "rushed": 0, "copied": 0,
            "guesses": 0, "extra": 0, "extra_first": 0, "extra_right": 0, "extra_pct": None, "plan_min": 0, "acts": {}, "acts_extra": {},
            "rushed_list": [], "idk": 0, "extra_at": "", "extra_after_day": False, "fixq": 0, "acts_fix": {}}


RUSHED_SHOW = 12          # rushed answers listed under "N wrong answers look rushed"


def _in_year(fact: str, year: int) -> bool:
    """A times-tables fact ("12x7") is one of the child's year: one of its numbers is a table of that year (the
    optional Year 4 check asks every table, so a Year 3 child's 12 × 7 is not judged as Year 3 work)."""
    from .drills.tables import tables_for_year           # drills.tables imports this module
    try:
        a, b = (int(x) for x in str(fact).split("x"))
    except ValueError:
        return True
    return bool({a, b} & set(tables_for_year(year)))


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


# Typed instead of trying (a fixed list of non-answers, compared whole, never searched for inside an answer).
# Saying "I don't know" is honest, not a guess: those (IDK_WORDS, and the "I don't know" button) are counted
# apart, and the parent reads them neutrally ("said I don't know").
IDK_WORDS = {"idk", "i dk", "i dont know", "i don't know", "i do not know", "dont know", "don't know", "dunno",
             "i dunno", "no idea", "no clue", "not sure", "dk", "i'm not sure", "im not sure"}
NON_ANSWERS = {"?", "??", "???", "pass", "skip", "whatever", "nothing", "idc"}


def _said_idk(got: str) -> bool:
    return " ".join(str(got or "").lower().replace("’", "'").split()).strip(" .!") in IDK_WORDS


def _guessed(got: str, exp: str) -> bool:
    """Structure only: a non-answer ("idk", "?"), or every option ticked: three or more choices given (words
    tapped, numbers typed) where the answer has at most half as many."""
    g = " ".join(str(got or "").lower().split()).strip(" .!")
    if g in NON_ANSWERS:
        return True
    def parts(t: str) -> list:
        t = str(t or "").strip()
        if "," in t:
            return [x for x in (y.strip() for y in t.split(",")) if x]
        bits = t.split()
        return bits if bits and all(re.fullmatch(r"-?\d+(?:\.\d+)?", b) for b in bits) else [t] if t else []
    pg, pe = parts(got), parts(exp)
    return len(pg) >= 3 and all(len(x.split()) == 1 for x in pg) and len(pg) >= 2 * max(1, len(pe))


async def day_stats(pupil_ids: list, days: list, targets: dict | None = None) -> dict:
    """How each day went, beyond the target: {pupil_id: {day: {answers, first (answers that were a first try),
    first_right, first_pct, minutes, rushed, guesses, copied, extra..., plan_min, acts}}}. A first try is an answer
    not straight after a wrong answer to the same item; minutes add up the time between answers, without long
    pauses; rushed = wrong answers given in under QUICK_MS (an option or a word picked: PICK_MS) or that look like
    random keys; guesses = other wrong
    answers that are a non-answer or every option (_guessed); copied = right answers to an item within COPY_MS
    of getting it wrong (the answer was on screen). Each first try falls in ONE of three parts, the same on Home,
    Progress, the printed report and the weekly email:
      - the headline (first, first_right, first_pct, acts): the planned questions, up to each activity's target;
      - extra (extra, extra_right, extra_pct, acts_extra): THE one "extra" figure, questions after the activity's
        target (on a rest day, all of them), outside "Practise my mistakes"; the "+N" by an activity is its part;
      - fixq (acts_fix): mistakes practised in "Practise my mistakes" (the mistake itself; the row has "fixing").
    Other answers in "Practise my mistakes" (while a mistake waits for its gap) are in none of them, and neither
    are retries, copies or a real word typed for a spelling word ("other"): all of them count in answers only.
    So more effort never lowers the day's score. extra_first is extra (kept for older callers); plan_min is the
    plan's minutes. acts ({activity: [first, first_right]}) also leaves out Year 4 check facts beyond the child's
    year (_in_year), so extra practice or the optional check never turns an activity "needs help".
    rushed_list: the rushed answers ({time, activity, q, got, exp}); a time-out in the timed Year 4 check is
    never rushed. extra_at: when the extra answers were given ("19:08" or "19:08–19:20", UK time), and
    extra_after_day: they all came after the whole day's targets were met."""
    out: dict = {}
    rows = db.attempts.find({"pupil_id": {"$in": pupil_ids}, "day": {"$in": days}},
                            {"pupil_id": 1, "day": 1, "activity": 1, "detail": 1, "correct": 1, "ms": 1, "ts": 1,
                             "got": 1, "exp": 1, "copied": 1, "q": 1, "src": 1, "other": 1, "pick": 1, "idk": 1,
                             "fix": 1, "fixing": 1}).sort("ts", 1)
    wrong_at: dict = {}
    last_ts: dict = {}
    right_so_far: dict = {}
    extra_ts: dict = {}
    day_done: dict = {}
    async for r in rows:
        s = out.setdefault(r["pupil_id"], {}).setdefault(r["day"], _no_stats())
        plan = ((targets or {}).get(r["pupil_id"]) or {}).get(r["day"]) or {}
        s["plan_min"] = plan.get("min", 0)
        s["answers"] += 1
        ak = (r["pupil_id"], r["day"], r["activity"])
        lk = (r["pupil_id"], r["day"])
        target = 0 if plan.get("rest") else (plan.get("acts") or {}).get(r["activity"])
        extra = target is not None and right_so_far.get(ak, 0) >= target and not r.get("fix")
        if r["correct"]:
            right_so_far[ak] = right_so_far.get(ak, 0) + 1
        if extra:
            extra_ts.setdefault(lk, []).append(r["ts"])
        elif plan.get("acts") and lk not in day_done and all(
                right_so_far.get((r["pupil_id"], r["day"], k), 0) >= t for k, t in plan["acts"].items()):
            day_done[lk] = r["ts"]                 # the answer that met the last target
        key = (r["pupil_id"], r["activity"], "" if r.get("copied") else r.get("detail") or "")
        # maths records the skill, and every maths question is a new one, so only the other activities repeat an item
        prev_wrong = wrong_at.get(key) if key[2] and r["activity"] != "maths" else None
        ms = r.get("ms") if isinstance(r.get("ms"), (int, float)) else None
        gap = (r["ts"] - last_ts[lk]).total_seconds() * 1000 if lk in last_ts else (ms or 0)
        s["minutes"] += min(max(gap, 0), GAP_MS) / 60000
        last_ts[lk] = r["ts"]
        if r.get("other"):
            continue        # another real word, spelt right (spelling.check): its time counts, never as right or wrong
        if r.get("copied"):
            # right straight after being shown the answer (the retype after another real word, a fact just given):
            # a copy, never a right first try
            s["copied"] += 1 if r["correct"] else 0
            continue
        if r.get("fixing") and not r.get("copied") and (prev_wrong is None or
                                                         (r["ts"] - prev_wrong).total_seconds() * 1000 >= COPY_MS):
            s["fixq"] += 1                         # a mistake practised ("+ 6 mistakes practised")
            s["acts_fix"][r["activity"]] = s["acts_fix"].get(r["activity"], 0) + 1
        if prev_wrong is None:
            if r.get("fix"):
                pass                               # "Practise my mistakes": neither the headline nor extra
            elif extra:
                s["extra"] += 1
                s["extra_right"] += 1 if r["correct"] else 0
                a = s["acts_extra"].setdefault(r["activity"], [0, 0])     # "plus 25 extra answers, 80% right"
                a[0] += 1
                a[1] += 1 if r["correct"] else 0
            else:
                s["first"] += 1
                s["first_right"] += 1 if r["correct"] else 0
                if not (r.get("src") == "mtc" and not _in_year(r.get("detail"), plan.get("year", 4))):
                    a = s["acts"].setdefault(r["activity"], [0, 0])
                    a[0] += 1
                    a[1] += 1 if r["correct"] else 0
        elif r["correct"] and (r["ts"] - prev_wrong).total_seconds() * 1000 < COPY_MS:
            s["copied"] += 1
        if not r["correct"]:
            wrong_at[key] = r["ts"]
            if r.get("idk") or ("got" in r and _said_idk(r.get("got"))):
                s["idk"] += 1                      # "I don't know" (the button, or typed): honest, never rushed or a guess
            elif r.get("src") == "mtc":
                pass                               # the timed check: a time-out or a quick slip is not rushing
            elif (ms is not None and ms < (PICK_MS if r.get("pick") else QUICK_MS)) \
                    or ("got" in r and _mashed(r.get("got"), r.get("exp"))):
                s["rushed"] += 1
                quick = ms is not None and ms < (PICK_MS if r.get("pick") else QUICK_MS)
                if len(s["rushed_list"]) < RUSHED_SHOW:
                    s["rushed_list"].append({"time": f"{r['ts'].replace(tzinfo=datetime.timezone.utc).astimezone(TZ):%H:%M}",
                                             "activity": r["activity"], "q": r.get("q", ""), "got": r.get("got", ""),
                                             "exp": r.get("exp", ""), "quick": quick, "tap": quick and bool(r.get("pick"))})
            elif "got" in r and _guessed(r.get("got"), r.get("exp")):
                s["guesses"] += 1
        else:
            wrong_at.pop(key, None)
    for (pid, d), ts in extra_ts.items():
        s = out[pid][d]
        a, b = (f"{t.replace(tzinfo=datetime.timezone.utc).astimezone(TZ):%H:%M}" for t in (ts[0], ts[-1]))
        s["extra_at"] = a if a == b else f"{a}–{b}"
        s["extra_after_day"] = (pid, d) in day_done and ts[0] >= day_done[(pid, d)]
    for per in out.values():
        for s in per.values():
            s["minutes"] = round(s["minutes"])
            s["first_pct"] = pct(s["first_right"], s["first"])
            s["extra_first"] = s["extra"]
            s["extra_pct"] = pct(s["extra_right"], s["extra"])
    return out


# ---- What grows from day to day, for the child (My day, the Board): kept simple, never compared between children ----
STREAK_LOOK = 60          # days looked back for a streak


async def streaks(family: dict, pupils: list) -> dict:
    """{pupil id: days in a row with the day's plan done (100%)}. Today counts once it is done, and an unfinished
    today does not break it; a rest day (a day off, a rest week, a day not in the practice days) neither counts
    nor breaks it."""
    days = day_list(STREAK_LOOK)
    c = await counts([p["_id"] for p in pupils], days)
    out, now = {}, today()
    for p in pupils:
        n, first = 0, first_day(p)
        for d in reversed(days):
            if d < first:
                break
            st = day_status(p, family, c.get(p["_id"], {}).get(d, {}), d)
            if st["rest"]:
                continue
            if st["pct"] >= 100:
                n += 1
            elif d != now:
                break
        out[p["_id"]] = n
    return out


async def week_wins(pupil: dict) -> dict:
    """This week (the last 7 days) for the child: mistakes put right, and skills that became secure (maths,
    grammar, science)."""
    since = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    fixed = book_counts(await mistake_book(pupil))["fixed"]      # the parent's "put right", the same rule
    secured = await db.maths_mastery.count_documents({"pupil": pupil["_id"].lower(), "mastered_at": {"$gte": since}}) \
        + await db.bank_mastery.count_documents({"pupil_id": pupil["_id"], "mastered_at": {"$gte": since}})
    return {"fixed": fixed, "secured": secured}
