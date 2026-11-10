"""Pages around the practice: the help page, a printable progress report, and the service worker."""
import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse

from ..activities import ACTIVITIES, ORDER, todays_plan
from ..config import BASE_DIR
from ..db import db
from ..deps import Ctx, load, own_pupil, parent_page
from ..drills import maths, spelling, tables, verbs
from .. import progress
from ..web import page
from .parent import _skill_views

router = APIRouter()

# England's year groups and the matching classes elsewhere in the UK, by age (help page and add-a-child hint).
UK_YEARS = [(1, "P2", "Year 1", "P2"), (2, "P3", "Year 2", "P3"), (3, "P4", "Year 3", "P4"), (4, "P5", "Year 4", "P5"),
            (5, "P6", "Year 5", "P6"), (6, "P7", "Year 6", "P7"), (7, "S1", "Year 7", "Year 8"),
            (8, "S2", "Year 8", "Year 9"), (9, "S3", "Year 9", "Year 10")]
RANGES = {"7": "Last 7 days", "30": "Last 30 days", "term": "This term so far"}


@router.get("/sw.js")
async def service_worker():
    # Served from the root, not /static/, so that it may look after every page (its scope is where it lives).
    return FileResponse(BASE_DIR / "static" / "sw.js", media_type="text/javascript",
                        headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"})


@router.get("/help")
async def help_page(request: Request):
    return page(request, "help.html", await load(request), uk_years=UK_YEARS)


def term_start(day: datetime.date) -> datetime.date:
    """The start of the school term `day` is in (England, roughly): autumn from 1 September, spring from
    1 January, summer from 15 April (after the Easter holidays, whose date moves)."""
    if day.month >= 9:
        return datetime.date(day.year, 9, 1)
    if day >= datetime.date(day.year, 4, 15):
        return datetime.date(day.year, 4, 15)
    return datetime.date(day.year, 1, 1)


def report_days(rng: str, first: str) -> list:
    """The local days of the report (oldest first), never before the child's first day."""
    today = datetime.date.fromisoformat(progress.today())
    n = (today - term_start(today)).days + 1 if rng == "term" else int(rng)
    return [d for d in progress.day_list(n) if d >= first]


@router.get("/children/{pid}/report")
async def report(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    rng = request.query_params.get("range") or "30"
    rng = rng if rng in RANGES else "30"
    days = report_days(rng, progress.first_day(p))
    c = (await progress.counts([p["_id"]], days)).get(p["_id"], {})
    st = (await progress.day_stats([p["_id"]], days)).get(p["_id"], {})
    tot = {k: sum(s[k] for s in st.values()) for k in ("answers", "first", "first_right", "minutes", "rushed", "copied")}
    done = sum(1 for d in days if c.get(d) and progress.day_status(p, ctx.family, c[d], d)["pct"] >= 100)
    acts = {}
    for d in c.values():
        for k, v in d.items():
            a = acts.setdefault(k, {"correct": 0, "answered": 0})
            a["correct"] += v["correct"]
            a["answered"] += v["answered"]
    on = {a["key"] for a in todays_plan(p, ctx.family)} | set(acts)
    since = datetime.datetime.fromisoformat(days[0]) if days else datetime.datetime.utcnow()
    new = {"maths": await db.maths_mastery.count_documents({"pupil": p["_id"].lower(), "mastered_at": {"$gte": since}})}
    for s in ("grammar", "science"):
        new[s] = await db.bank_mastery.count_documents({"pupil_id": p["_id"], "subject": s, "mastered_at": {"$gte": since}})
    skills = await _skill_views(p, on)
    weak = sorted(((subj, sk) for subj, groups in skills.items() for g in groups for sk in g["skills"]
                   if sk["state"] == "practising"), key=lambda x: x[1]["score"])[:8]
    open_m = await progress.open_mistakes(p, max(len(days), 1))
    words = spelling.list_for_year(p.get("year", 3))
    learned = sorted([w["word"] async for w in db.spelling_words.find(
        {"pupil_id": p["_id"], "box": {"$gte": spelling.LEARNED_BOX}, "word": {"$in": words}}, {"word": 1})],
        key=str.lower) if "spelling" in on else []
    return page(request, "progress_report.html", ctx, pupil=p, days=days, rng=rng, ranges=RANGES,
                practised=sum(1 for s in st.values() if s["answers"]), done_days=done, tot=tot,
                first_pct=(100 * tot["first_right"] // tot["first"]) if tot["first"] else None,
                acts=[(k, acts[k]) for k in ORDER if k in acts], skills=skills, new=new, weak=weak,
                to_fix={k: v for k, v in open_m.items() if k in ("tables", "spelling", "verbs", "numbers")},
                words_total=len(words), learned=learned, spelling_on="spelling" in on,
                tables=await tables.mastered_count(p) if "tables" in on else None,
                verbs=await verbs.summary(p) if "verbs" in on else None,
                maths_year=maths.engine_year(p["year"]), printed=_nice(progress.today()),
                period=f"{_nice(days[0])} to {_nice(days[-1])}" if days else "", ACTIVITIES=ACTIVITIES)


def _nice(day: str) -> str:
    d = datetime.date.fromisoformat(day)
    return f"{d.day} {d:%b %Y}"
