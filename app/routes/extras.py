"""Pages around the practice: the help page, a printable progress report, example questions for a parent, and
the service worker."""
import datetime
import random

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from ..activities import ACTIVITIES, ORDER, day_label, rest_day, strand_label, todays_plan
from ..bank import engine as bank_engine
from ..config import BASE_DIR
from ..db import db
from ..deps import Ctx, load, own_pupil, parent_page
from ..drills import maths, spelling, tables, verbs
from ..maths import maths_engine, maths_mastery
from .. import levels, progress
from ..web import page
from .parent import _skill_views, accuracy, work_on

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
    st = (await progress.day_stats([p["_id"]], days, progress.plan_targets([p], ctx.family, days))).get(p["_id"], {})
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
    weak = [(w["subject"], w) for w in await work_on(p, on, 8)]     # real weakness: wrong answers, not a low score
    # still to put right: the parent page's "to go over" (progress.mistake_book, the one rule of every count)
    open_m: dict = {}
    for e in await progress.mistake_book(p, plan={a["key"] for a in todays_plan(p, ctx.family)}):
        if e["state"] in ("due", "later"):
            open_m.setdefault(e["activity"], []).append(e["detail"])
    words = spelling.list_for_year(p.get("year", 3))
    learned = sorted([w["word"] async for w in db.spelling_words.find(
        {"pupil_id": p["_id"], "box": {"$gte": spelling.LEARNED_BOX}, "word": {"$in": words}}, {"word": 1})],
        key=str.lower) if "spelling" in on else []
    return page(request, "progress_report.html", ctx, pupil=p, days=days, rng=rng, ranges=RANGES, **_rest_days(p, days),
                practised=sum(1 for s in st.values() if s["answers"]), done_days=done, tot=tot,
                first_pct=(100 * tot["first_right"] // tot["first"]) if tot["first"] else None,
                acts=[(k, acts[k]) for k in ORDER if k in acts], skills=skills, new=new, weak=weak,
                # right first time per activity: the same rule as Home and Progress (parent.accuracy)
                acc={a["key"]: a for a in accuracy([{"stats": s} for s in st.values()])},
                to_fix={k: v for k, v in open_m.items() if k in ("tables", "spelling", "verbs", "numbers")},
                words_total=len(words), learned=learned, spelling_on="spelling" in on,
                school_lists=await spelling.school_report(p, days[0] if days else "") if "spelling" in on else [],
                tables=await tables.mastered_count(p) if "tables" in on else None,
                verbs=await verbs.summary(p) if "verbs" in on else None,
                maths_year=maths.engine_year(levels.level(p, "maths")), printed=_nice(progress.today()),
                period=f"{_nice(days[0])} to {_nice(days[-1])}" if days else "", ACTIVITIES=ACTIVITIES)


def _rest_days(p: dict, days: list) -> dict:
    """The report's days off (a sick day or a holiday, as spans: "11 Nov", "13 Nov to 15 Nov") and how many days
    were not practice days, so a gap in the record reads as planned, not missed."""
    spans, off, week = [], 0, 0
    for d in days:
        r = rest_day(p, d)
        off += r == "off"
        week += r == "week"
        if r == "off" and spans and spans[-1][1] == _prev(d):
            spans[-1][1] = d
        elif r == "off":
            spans.append([d, d])
    return {"off_spans": [day_label(a) if a == b else f"{day_label(a)} to {day_label(b)}" for a, b in spans],
            "off_count": off, "rest_count": week}


def _prev(day: str) -> str:
    return (datetime.date.fromisoformat(day) - datetime.timedelta(days=1)).isoformat()


def _nice(day: str) -> str:
    d = datetime.date.fromisoformat(day)
    return f"{d.day} {d:%b %Y}"


# ---- "See example questions": a few questions of one strand, with their answers, for a parent to look at first ----
EXAMPLES = 4                   # questions shown (3 at least, from as many of the strand's skills as there are)
# Maths framings a page can show as text and a table; any other picture is named in a line instead.
_SHOWN = ("number", "data_table", "io_table", "bar_chart", "pictogram", "pie_chart")
_PICTURE = {"number_line": "a number line", "base_ten": "place-value blocks", "array": "an array of dots",
            "fraction_bar": "a fraction bar", "clock": "a clock", "coordinate_grid": "a grid", "area_grid": "a grid of squares",
            "strip_model": "a bar model", "line_graph": "a line graph", "shape": "a shape", "angle": "an angle",
            "ruler": "a ruler or scale", "equal_groups": "groups of counters", "circle": "a circle", "net": "a net of a solid",
            "inequality_line": "a number line", "scatter_plot": "a graph"}


def _spread(skills: list, n: int) -> list:
    """n skills spread over the strand (in teaching order), each used again when the strand has fewer."""
    if len(skills) >= n:
        return sorted(random.sample(skills, n), key=skills.index)
    return [skills[i % len(skills)] for i in range(max(n - 1, len(skills), 3))]


def _maths_example(skill: dict) -> dict:
    """A question of the skill made the way the child gets it (middle tier), never stored: nothing is recorded."""
    fn = maths_engine.GENERATORS[skill["key"]]
    for _ in range(8):                         # a framing the page can show, if the skill has one
        q = maths_engine.present(maths_engine.call_generator(fn, 1), skill["key"])
        if q.get("component", "number") in _SHOWN:
            break
    spec, comp = q.get("spec") or {}, q.get("component", "number")
    table = None
    if comp == "data_table" and spec.get("rows"):
        table = {"head": spec.get("headers") or [], "rows": maths_engine.hide_missing_cell(comp, spec)["rows"]}
    elif comp == "io_table" and spec.get("rows"):
        table = {"head": ["In", "Out"], "rows": maths_engine.hide_missing_cell(comp, spec)["rows"]}
    elif comp in ("bar_chart", "pictogram") and spec.get("categories"):
        table = {"head": [], "rows": [[c, v] for c, v in zip(spec["categories"], spec.get("values") or [])]}
    elif comp == "pie_chart" and spec.get("slices"):
        table = {"head": [], "rows": [list(s[:2]) for s in spec["slices"]]}
    ans, unit = str(maths_engine.answer_text(q)), spec.get("unit") or ""
    ans = "£" + ans if unit == "£" else f"{ans} {unit}" if unit and unit not in ans else ans
    return {"skill": skill["title"], "q": q["prompt"], "table": table, "answer": ans,
            "picture": None if comp in _SHOWN else _PICTURE.get(comp, "a picture"),
            "why": [str(x) for x in q.get("solution") or []][:3]}


def _bank_example(skill: dict, used: set) -> dict:
    q = random.choice([q for q in skill["qs"] if q["id"] not in used] or skill["qs"])
    used.add(q["id"])
    pub, key = bank_engine.serve(q)
    sentence = pub.get("s") or (" ".join(pub["words"]) if pub.get("words") else "")
    ans = bank_engine.expected_text(key) + (f" {q['unit']}" if q.get("unit") else "")
    return {"skill": skill["title"], "q": q["q"], "sentence": sentence, "opts": pub.get("opts") or [],
            "answer": ans, "why": [q["why"]] if q.get("why") else []}


@router.get("/children/{pid}/examples")
async def examples(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    """A few questions of one strand, as the child of that year gets them, with the answers. Read-only and for the
    grown-ups only (parent mode): nothing is served to the child or recorded."""
    p = await own_pupil(ctx, pid)
    subject, strand = request.query_params.get("subject", ""), request.query_params.get("strand", "")
    try:
        more = max(0, min(99, int(request.query_params.get("more") or 0)))
    except ValueError:
        more = 0
    if subject == "maths":
        year = maths.engine_year(levels.level(p, "maths"))
        skills = [s for s in maths_mastery._year_skills(year) + maths_mastery._earlier_ks3(year) if s["strand"] == strand]
        qs = [_maths_example(s) for s in _spread(skills, EXAMPLES)] if skills else []
    elif subject in ("grammar", "science"):
        year = bank_engine.bank_year(subject, levels.level(p, subject))
        skills = [s for s in bank_engine.skills(subject, levels.level(p, subject)) if s["strand"] == strand and s["qs"]]
        used: set = set()
        qs = [_bank_example(s, used) for s in _spread(skills, EXAMPLES)] if skills else []
    else:
        skills = qs = []
    if not qs:
        raise HTTPException(404, "not found")
    words = bank_engine.strand_key_words(subject, skills) if subject in ("grammar", "science") else []
    return page(request, "examples.html", ctx, pupil=p, subject=subject, subject_title=ACTIVITIES[subject]["title"],
                strand=strand, strand_name=strand_label(strand), year=year, qs=qs, more=more, words=words)


@router.get("/children/{pid}/keywords")
async def key_words(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    """The key words of grammar or science for the child's level, strand by strand, each with its one-line meaning
    (app/bank/glossary.py): the list behind "Learn the key words". Grown-ups only; nothing is recorded."""
    p = await own_pupil(ctx, pid)
    subject = request.query_params.get("subject", "")
    if subject not in ("grammar", "science"):
        raise HTTPException(404, "not found")
    lvl = levels.level(p, subject)
    by: dict = {}
    for s in bank_engine.skills(subject, lvl):
        by.setdefault(s["strand"], []).append(s)
    strands = [(st, strand_label(st), bank_engine.strand_key_words(subject, sks)) for st, sks in by.items()]
    return page(request, "keywords.html", ctx, pupil=p, subject=subject, subject_title=ACTIVITIES[subject]["title"],
                year=bank_engine.bank_year(subject, lvl), strands=[s for s in strands if s[2]])
