"""A child's school year, and the year each subject's questions come from ("working at", set by a parent).

`year` on a pupil is always the real school year: the plan's defaults, spelling, times tables, verbs, the Year 4
check and the SATs card follow it. Maths, grammar and science each have a level, the school year unless a parent
chose another one (`levels`: {"maths": 6}, only the subjects that differ). Maths questions come from that year of
the maths engine, grammar and science from that year of the question bank.

Before November 2026 a child had one level for every subject: `year` was that level and `school_year` the real
year when they differed. `fix` turns such a record into today's shape, once (at start-up, and again for any
record read before that ran)."""
from .db import db

SUBJECTS = ("maths", "grammar", "science")
TITLES = {"maths": "Maths", "grammar": "Grammar", "science": "Science"}


def school_year(p: dict) -> int:
    """The child's real school year (an old record keeps it in school_year)."""
    return int(p.get("school_year") or p.get("year") or 1)


def level(p: dict, subject: str) -> int:
    """The year this subject's questions come from: the parent's choice, else the school year. An old record that
    is not fixed yet: its one level (`year`) for every subject."""
    lv = (p.get("levels") or {}).get(subject)
    if lv:
        return int(lv)
    if p.get("school_year") and subject in SUBJECTS:
        return int(p.get("year") or school_year(p))
    return school_year(p)


def differs(p: dict) -> list:
    """[(subject, level)] for each subject worked at another year than the school year, in SUBJECTS order."""
    sy = school_year(p)
    return [(s, level(p, s)) for s in SUBJECTS if level(p, s) != sy]


def levels_text(p: dict) -> str:
    """"Maths: Year 6 level", "Maths: Year 6 level · Grammar: Year 9 level", or "" when every subject is at the
    school year."""
    return " · ".join(f"{TITLES[s]}: Year {lv} level" for s, lv in differs(p))


def clean(levels: dict, sy: int) -> dict | None:
    """Only the subjects that differ from the school year are kept; None when none does."""
    out = {s: int(v) for s, v in (levels or {}).items() if s in SUBJECTS and v and int(v) != sy}
    return out or None


def _update(p: dict) -> dict | None:
    if "school_year" not in p:
        return None
    sy = school_year(p)
    old = int(p.get("year") or sy)
    lv = clean({**{s: old for s in SUBJECTS}, **(p.get("levels") or {})}, sy) if p.get("school_year") else \
        clean(p.get("levels") or {}, sy)
    return {"$set": {"year": sy, "levels": lv}, "$unset": {"school_year": ""}}


async def fix(p: dict | None) -> dict | None:
    """Bring an old record (one level for all subjects) to today's shape, in the database and in `p` itself."""
    if not p:
        return p
    upd = _update(p)
    if upd:
        await db.pupils.update_one({"_id": p["_id"], "school_year": {"$exists": True}}, upd)
        p.update(upd["$set"])
        p.pop("school_year", None)
    return p


async def fix_all() -> int:
    """At start-up: every old record. Returns how many were changed."""
    n = 0
    async for p in db.pupils.find({"school_year": {"$exists": True}}):
        await fix(p)
        n += 1
    return n
