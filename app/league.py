"""The family league and times-tables races.

League: every child earns stars each school week (Monday to Sunday, UK time) from their own plan, so a Year 1 and a
Year 9 child compete fairly: up to 10 a day for the day's plan (1 per 10% done), and 1 for every 5 right answers
past the target (at most 5 a day). Rest days and days off cost nothing. The family's children are on one table, by
name. Families can also join a friends' league with a code a parent shares: there each child shows only a
nickname picked from fixed lists (never their name, never text a family typed) and a picture, so nothing a child
writes ever reaches another family, and there is no chat of any kind.

Races: 20 times-tables questions against the clock, the same 20 for everyone on that course that week (from a
seed), so a child races the "ghost" of a brother's, sister's or friend's best run, shown moving along the track as
that run went. A wrong answer is typed again (2 seconds added). Three courses: Starter (2, 5 and 10 times tables),
Middle (adds 3, 4 and 8) and Full (2 to 12).
"""
import datetime
import hashlib
import random
import re
import secrets

from . import progress
from .activities import local_today, todays_plan
from .db import db

STAR_DAY = 10             # stars for a day's plan done
STAR_EXTRA = 5            # right answers past the target for one more star ...
STAR_EXTRA_MAX = 5        # ... and at most this many such stars a day
STAR_RACE_MAX = 3         # a finished times-tables race: 1 star, at most this many a day
RACE_N = 20
RACE_WRONG_MS = 2000      # time added for each wrong answer
RACE_MIN_MS = 350         # a question answered faster than this was not answered by a child (a script)
COURSES = {
    "starter": {"title": "Starter", "tables": [2, 5, 10], "top": 10, "about": "the 2, 5 and 10 times tables"},
    "middle": {"title": "Middle", "tables": [2, 3, 4, 5, 8, 10], "top": 12, "about": "the 2, 3, 4, 5, 8 and 10 times tables"},
    "full": {"title": "Full", "tables": list(range(2, 13)), "top": 12, "about": "every table from 2 to 12"},
}
COURSE_ORDER = ["starter", "middle", "full"]
LEAGUE_MAX_FAMILIES = 12
LEAGUES_PER_FAMILY = 3
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"      # no 0/O or 1/I
NICK_ADJ = ["Swift", "Brave", "Clever", "Happy", "Bright", "Calm", "Kind", "Lucky", "Mighty", "Quick", "Sunny",
            "Witty", "Bold", "Gentle", "Jolly", "Nimble", "Proud", "Steady", "Zesty", "Cosy"]
NICK_ANIMAL = [("Otter", "🦦"), ("Fox", "🦊"), ("Owl", "🦉"), ("Panda", "🐼"), ("Tiger", "🐯"), ("Koala", "🐨"),
               ("Penguin", "🐧"), ("Dolphin", "🐬"), ("Hedgehog", "🦔"), ("Rabbit", "🐰"), ("Badger", "🦡"),
               ("Turtle", "🐢"), ("Parrot", "🦜"), ("Whale", "🐳"), ("Lion", "🦁"), ("Frog", "🐸"), ("Bee", "🐝"),
               ("Squirrel", "🐿️"), ("Zebra", "🦓"), ("Eagle", "🦅")]
ANIMAL_PIC = dict(NICK_ANIMAL)


# ---- weeks ----
def week_start(day: str | None = None) -> str:
    d = datetime.date.fromisoformat(day or local_today())
    return (d - datetime.timedelta(days=d.weekday())).isoformat()


def week_days(start: str) -> list:
    d = datetime.date.fromisoformat(start)
    return [(d + datetime.timedelta(days=i)).isoformat() for i in range(7)]


# ---- nicknames ----
def new_nick(rng=random) -> dict:
    a, (animal, pic) = rng.choice(NICK_ADJ), rng.choice(NICK_ANIMAL)
    return {"name": f"{a} {animal}", "pic": pic}


def valid_nick(adj: str, animal: str) -> dict | None:
    if adj in NICK_ADJ and animal in ANIMAL_PIC:
        return {"name": f"{adj} {animal}", "pic": ANIMAL_PIC[animal]}
    return None


async def nick_of(pupil: dict) -> dict:
    """The child's nickname for friends' leagues (made once, kept; a parent can change it from the fixed lists)."""
    n = pupil.get("nick")
    if not (isinstance(n, dict) and n.get("name") and n.get("pic")):
        n = new_nick()
        await db.pupils.update_one({"_id": pupil["_id"]}, {"$set": {"nick": n}})
        pupil["nick"] = n
    return n


# ---- stars ----
def day_stars(st: dict) -> int:
    """Stars for one day from its status (progress.day_status): the plan, then extra right answers."""
    if st.get("rest"):
        plan = 0
        extra = int(st.get("extra") or 0)
    else:
        plan = min(STAR_DAY, int(st.get("pct") or 0) // 10)
        extra = sum(int(i.get("extra") or 0) for i in st.get("items") or [])
    return plan + min(STAR_EXTRA_MAX, extra // STAR_EXTRA)


async def week_stars(family: dict, pupils: list, start: str | None = None) -> dict:
    """{pupil id: {"stars": n, "days": [stars per day, Monday first, None for days not come yet]}}."""
    start = start or week_start()
    days = week_days(start)
    today = local_today()
    c = await progress.counts([p["_id"] for p in pupils], [d for d in days if d <= today])
    raced: dict = {}
    async for r in db.races.find({"pupil_id": {"$in": [p["_id"] for p in pupils]}, "day": {"$in": days},
                                  "total": {"$exists": True}}, {"pupil_id": 1, "day": 1}):
        k = (r["pupil_id"], r["day"])
        raced[k] = raced.get(k, 0) + 1
    out = {}
    for p in pupils:
        first = progress.first_day(p)
        per = []
        for d in days:
            if d > today or d < first:
                per.append(None if d > today else 0)
                continue
            per.append(day_stars(progress.day_status(p, family, c.get(p["_id"], {}).get(d, {}), d))
                       + min(STAR_RACE_MAX, raced.get((p["_id"], d), 0)))
        out[p["_id"]] = {"stars": sum(x or 0 for x in per), "days": per}
    return out


# ---- leagues between families ----
def _code(rng=secrets.SystemRandom()) -> str:
    return "".join(rng.choice(CODE_ALPHABET) for _ in range(8))


def norm_code(code: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(code or "").upper())


async def leagues_of(family_id: str) -> list:
    return [lg async for lg in db.leagues.find({"families": family_id}).sort("created", 1)]


async def create_league(family: dict) -> dict | str:
    if len(await leagues_of(family["_id"])) >= LEAGUES_PER_FAMILY:
        return "full"
    for _ in range(10):
        code = _code()
        if not await db.leagues.find_one({"code": code}):
            break
    # a fixed name (never text a family typed, which other families would read): "League K7Q2"
    lg = {"_id": secrets.token_hex(8), "code": code, "owner": family["_id"], "families": [family["_id"]],
          "name": f"League {code[:4]}", "created": datetime.datetime.utcnow()}
    await db.leagues.insert_one(lg)
    return lg


async def join_league(family: dict, code: str) -> dict | str:
    """The league, or why not: "nocode", "already", "out" (the league's maker took this family out), "full" (that
    league), "many" (this family is in too many)."""
    code = norm_code(code)
    lg = await db.leagues.find_one({"code": code}) if len(code) == 8 else None
    if not lg:
        return "nocode"
    if family["_id"] in lg["families"]:
        return "already"
    if family["_id"] in (lg.get("removed") or []):
        return "out"
    if len(lg["families"]) >= LEAGUE_MAX_FAMILIES:
        return "full"
    if len(await leagues_of(family["_id"])) >= LEAGUES_PER_FAMILY:
        return "many"
    await db.leagues.update_one({"_id": lg["_id"]}, {"$addToSet": {"families": family["_id"]}})
    lg["families"].append(family["_id"])
    return lg


async def leave_league(family_id: str, league_id: str) -> None:
    """The family leaves; the league goes when its last family leaves, and passes to the next family when the
    family that made it leaves."""
    lg = await db.leagues.find_one({"_id": league_id, "families": family_id})
    if not lg:
        return
    rest = [f for f in lg["families"] if f != family_id]
    if not rest:
        await db.leagues.delete_one({"_id": league_id})
        return
    upd = {"$set": {"families": rest}}
    if lg["owner"] == family_id:
        upd["$set"]["owner"] = rest[0]
    await db.leagues.update_one({"_id": league_id}, upd)


async def remove_family(league_id: str, owner_id: str, family_id: str) -> bool:
    """The family that made the league takes another family out of it."""
    lg = await db.leagues.find_one({"_id": league_id, "owner": owner_id})
    if not lg or family_id == owner_id or family_id not in lg["families"]:
        return False
    # out for good (the code no longer lets them in), and a new code, so an old message cannot be passed on
    await db.leagues.update_one({"_id": league_id}, {"$pull": {"families": family_id}, "$addToSet": {"removed": family_id},
                                                     "$set": {"code": await _free_code()}})
    return True


async def _free_code() -> str:
    for _ in range(10):
        code = _code()
        if not await db.leagues.find_one({"code": code}):
            return code
    return _code()


async def new_code(league_id: str, owner_id: str) -> bool:
    """The league's maker gives it a new code: the old one stops working (families already in stay in)."""
    r = await db.leagues.update_one({"_id": league_id, "owner": owner_id}, {"$set": {"code": await _free_code()}})
    return bool(r.matched_count)


async def drop_family(family_id: str) -> None:
    """A deleted family leaves every league."""
    for lg in await leagues_of(family_id):
        await leave_league(family_id, lg["_id"])


def in_leagues(pupil: dict) -> bool:
    """A child takes part in friends' leagues unless a parent turned it off."""
    return pupil.get("league_on") is not False


async def table(family: dict, pupils: list, own: dict | None = None, league: dict | None = None) -> list:
    """A league table this week: [{id, label, pic, stars, days, mine, me}] by stars. Without `league`: the
    family's own children, by name. With it: every family's children who take part, by nickname (the viewer's own
    family by name too, so a parent knows who is who)."""
    start = week_start()
    rows = []
    fams = league["families"] if league else [family["_id"]]
    for fid in fams:
        fam = family if fid == family["_id"] else await db.families.find_one({"_id": fid})
        if not fam:
            continue
        kids = pupils if fid == family["_id"] else [p async for p in db.pupils.find({"family_id": fid}).sort("created", 1)]
        if league:
            kids = [p for p in kids if in_leagues(p)]
        st = await week_stars(fam, kids, start)
        for p in kids:
            mine = fid == family["_id"]
            nick = await nick_of(p) if league else None
            rows.append({"id": p["_id"], "label": (p["name"] + (f" · {nick['name']}" if league else "")) if mine
                         else nick["name"], "pic": nick["pic"] if nick else "", "stars": st[p["_id"]]["stars"],
                         "days": st[p["_id"]]["days"], "mine": mine, "me": bool(own and p["_id"] == own["_id"])})
    rows.sort(key=lambda r: (-r["stars"], r["label"]))
    place, last = 0, None
    for i, r in enumerate(rows):
        if r["stars"] != last:
            place, last = i + 1, r["stars"]
        r["place"] = place
    return rows


# ---- races ----
def default_course(year: int) -> str:
    return "starter" if year <= 2 else "middle" if year == 3 else "full"


def course_questions(course: str, week: str) -> list:
    """The week's 20 questions on a course, the same for everyone: [(a, b)], no 1 times table, no fact twice."""
    c = COURSES[course]
    rng = random.Random(int(hashlib.sha256(f"{course}:{week}".encode()).hexdigest()[:12], 16))
    out, seen = [], set()
    while len(out) < RACE_N:
        a = rng.choice(c["tables"])
        b = rng.randint(2, c["top"])
        k = (min(a, b), max(a, b))
        if k in seen and len(seen) < 40:
            continue
        seen.add(k)
        out.append((a, b) if rng.random() < 0.5 else (b, a))
    return out


async def race_start(pupil: dict, course: str) -> dict | None:
    if course not in COURSES:
        return None
    week = week_start()
    qs = course_questions(course, week)
    token = secrets.token_urlsafe(16)
    await db.races.insert_one({"_id": token, "pupil_id": pupil["_id"], "family_id": pupil["family_id"],
                               "course": course, "week": week, "started": datetime.datetime.utcnow(), "done": False})
    return {"token": token, "course": course, "week": week,
            "questions": [{"q": f"{a} × {b}", "a": a * b} for a, b in qs]}


async def race_finish(pupil: dict, token: str, splits: list, wrong: list) -> dict | None:
    """splits: ms from the start to each right answer (rising); wrong: wrong tries per question. The time is the
    last split plus RACE_WRONG_MS a wrong try. A run that could not be a child's (faster than RACE_MIN_MS a
    question, or longer than the time since it started) is not kept."""
    r = await db.races.find_one_and_update({"_id": str(token or ""), "pupil_id": pupil["_id"], "done": False},
                                           {"$set": {"done": True}})
    if not r:
        return None
    try:
        splits = [int(x) for x in splits][:RACE_N]
        wrong = [max(0, min(20, int(x))) for x in wrong][:RACE_N]
    except (TypeError, ValueError):
        return {"kept": False}
    took = (datetime.datetime.utcnow() - r["started"]).total_seconds() * 1000
    gaps = [b - a for a, b in zip([0] + splits, splits)]
    ok = len(splits) == RACE_N and all(g >= RACE_MIN_MS for g in gaps) and splits[-1] <= took + 5000
    if not ok:
        await db.races.delete_one({"_id": r["_id"]})
        return {"kept": False}
    wrong += [0] * (RACE_N - len(wrong))
    total = splits[-1] + RACE_WRONG_MS * sum(wrong)
    before = await db.races.find_one({"pupil_id": pupil["_id"], "course": r["course"], "week": r["week"],
                                      "done": True, "total": {"$exists": True}}, sort=[("total", 1)])
    await db.races.update_one({"_id": r["_id"]}, {"$set": {"splits": splits, "wrong": wrong, "total": total,
                                                          "day": progress.today(), "at": datetime.datetime.utcnow()}})
    return {"kept": True, "total": total, "wrong": sum(wrong),
            "best": before is None or total < before["total"], "was": before["total"] if before else None}


async def race_board(family: dict, pupils: list, course: str, viewer: dict | None = None) -> list:
    """The week's best run on a course of each child in the family and in the family's leagues (by nickname
    there): [{id, label, pic, total, splits, mine, me}], fastest first."""
    week = week_start()
    fams = {family["_id"]}
    for lg in await leagues_of(family["_id"]):
        fams |= set(lg["families"])
    best: dict = {}
    async for r in db.races.find({"family_id": {"$in": list(fams)}, "course": course, "week": week,
                                  "total": {"$exists": True}}).sort("total", 1):
        best.setdefault(r["pupil_id"], r)
    if not best:
        return []
    kids = {p["_id"]: p async for p in db.pupils.find({"_id": {"$in": list(best)}})}
    rows = []
    for pid, r in best.items():
        p = kids.get(pid)
        if not p:
            continue
        mine = p["family_id"] == family["_id"]
        if not mine and not in_leagues(p):
            continue
        nick = await nick_of(p)
        rows.append({"id": pid, "label": p["name"] if mine else nick["name"], "pic": nick["pic"],
                     "total": r["total"], "splits": r.get("splits") or [], "mine": mine,
                     "me": bool(viewer and pid == viewer["_id"])})
    rows.sort(key=lambda x: x["total"])
    return rows


async def race_summary(pupil: dict) -> list:
    """For the parent: this week's races per course: [{title, about, runs, best, wrong}] (wrong: wrong tries in all
    of the week's runs on that course)."""
    week = week_start()
    out = []
    for k in COURSE_ORDER:
        runs = [r async for r in db.races.find({"pupil_id": pupil["_id"], "course": k, "week": week,
                                                "total": {"$exists": True}})]
        if not runs:
            continue
        out.append({"title": COURSES[k]["title"], "about": COURSES[k]["about"], "runs": len(runs),
                    "best": fmt_ms(min(r["total"] for r in runs)), "wrong": sum(sum(r.get("wrong") or []) for r in runs)})
    return out


def fmt_ms(ms: int | None) -> str:
    if ms is None:
        return "–"
    s = ms / 1000
    return f"{int(s // 60)}:{s % 60:04.1f}" if s >= 60 else f"{s:.1f} s"
