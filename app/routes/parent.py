"""The parent's side: children, their plans, progress, rewards, the account and its data."""
import datetime
import json
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response

from ..activities import (ACTIVITIES, ALL_WEEK, FOCUS_MAX, FOCUS_WEEKS, MAX_DAYS_OFF, ORDER, PLANS, SCIENCE_AREA,
                          SCIENCE_AREAS, SECONDS, WEEKDAYS, YEARS, day_label, days_text, default_activities,
                          focus_items, focus_title, minutes, plan_of, practice_days_on, rest_day, strand_label,
                          todays_plan, year_pace)
from ..bank import engine as bank_engine
from ..maths import maths_mastery
from ..db import FAMILY_COLLECTIONS, db
from ..deps import (Ctx, adult_name, clear_pin_lock, family_adult, family_events, family_page, full_page,
                    hit, local_time, log_event, over_limit, own_pupil, parent_page, pin_lock_until, pin_locks)
from ..drills import bank, maths, spelling, tables, verbs
from .. import config, mailer, progress
from ..tips import TIPS
from ..security import hash_secret, new_id, verify_secret
from ..web import page, templates
from .auth import settings_view
from .child import REPORT_REASONS, picker_page

router = APIRouter()
PIN_RE = re.compile(r"^\d{4}$")
# What the child form's script needs to tick a year's defaults and estimate the minutes as the parent edits.
templates.env.globals["PLAN_JS"] = {"defaults": {y: default_activities(y) for y in YEARS}, "seconds": SECONDS,
                                    "pace": {y: year_pace(y) for y in YEARS},
                                    "min_year": {k: a["min_year"] for k, a in ACTIVITIES.items()}}
templates.env.filters["daylabel"] = day_label          # "2026-11-24" -> "24 Nov"


def _day_name(day: str) -> str:
    """When a day is, after "back to practice": "tomorrow", or "on Monday 16 Nov"."""
    d = datetime.date.fromisoformat(day)
    if d == datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=1):
        return "tomorrow"
    return f"on {d:%A} {d.day} {d:%b}"


templates.env.filters["dayname"] = _day_name


async def _pupils(ctx: Ctx) -> list:
    return [p async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]


@router.get("/home")
async def home(request: Request, ctx: Ctx = Depends(parent_page)):
    pupils = await _pupils(ctx)
    board = await progress.board(ctx.family, pupils)
    hist = {p["_id"]: await progress.history(p, ctx.family, 7) for p in pupils}
    full = len(pupils) >= plan_of(ctx.family)["max_children"] and _full_reason(ctx.family) == "limit"
    return page(request, "home.html", ctx, board=board, hist=hist, plan=plan_of(ctx.family), full=full,
                day_stats=await progress.day_stats([p["_id"] for p in pupils], [progress.today()]),
                today_day=progress.today(),
                welcome=request.query_params.get("welcome"), locks=await pin_locks(pupils),
                unlocked=request.query_params.get("unlocked"), events=await family_events(ctx.family["_id"]),
                deleted_name=request.query_params.get("deleted_name", "")[:30])


def _form_activities(form, year: int) -> dict:
    acts = {}
    for k in ORDER:
        try:
            target = max(1, min(200, int(form.get(f"target_{k}") or ACTIVITIES[k]["target"])))
        except ValueError:
            target = ACTIVITIES[k]["target"]
        acts[k] = {"on": bool(form.get(f"on_{k}")) and year >= ACTIVITIES[k]["min_year"], "target": target}
    if form.get("check_tables"):                   # a Year 4 check each day, as part of the times-tables target
        acts["tables"]["check"] = True
    return acts


def _full_reason(family: dict) -> str:
    """Why no more children: the plan can be upgraded ("children"), or the biggest plan is full ("limit")."""
    return "limit" if plan_of(family)["max_children"] >= max(p["max_children"] for p in PLANS.values()) else "children"


@router.get("/children/new")
async def child_new_form(request: Request, ctx: Ctx = Depends(full_page)):
    if len(await _pupils(ctx)) >= plan_of(ctx.family)["max_children"]:
        return page(request, "upgrade.html", ctx, reason=_full_reason(ctx.family), plan=plan_of(ctx.family))
    # the year list opens on Year 1, so its plan is ticked; the form's script re-ticks when the year changes
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=None, years=YEARS,
                acts=default_activities(YEARS[0]))


@router.post("/children/new")
async def child_new(request: Request, ctx: Ctx = Depends(full_page)):
    form = await request.form()
    if len(await _pupils(ctx)) >= plan_of(ctx.family)["max_children"]:
        return page(request, "upgrade.html", ctx, reason=_full_reason(ctx.family), plan=plan_of(ctx.family),
                    status_code=403)
    name = (form.get("name") or "").strip()[:30]
    pin = (form.get("pin") or "").strip()
    try:
        year = int(form.get("year") or 0)
    except ValueError:
        year = 0
    err = None
    if not name:
        err = "Give your child's first name or a nickname."
    elif year not in YEARS:
        err = "Choose a school year."
    elif not PIN_RE.match(pin):
        err = "The PIN is 4 numbers, like 2580."
    if err:
        return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil={"name": name, "year": year}, years=YEARS,
                    acts=default_activities(year or 3), error=err, status_code=400)
    acts = _form_activities(form, year) if form.get("custom") else default_activities(year)
    p = {"_id": new_id("p"), "family_id": ctx.family["_id"], "name": name, "year": year, "pin": hash_secret(pin),
         "pin_view": pin, "activities": acts, "reward": _form_reward(form, ctx.family), "created": datetime.datetime.utcnow()}
    await db.pupils.insert_one(p)
    return RedirectResponse(f"/children/{p['_id']}?added=1", 303)


@router.get("/children/{pid}")
async def child_detail(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    now, nxt = todays_plan(p, ctx.family), todays_plan(p, ctx.family, _tomorrow())
    on = {a["key"] for a in now + nxt}             # cards only for what the child does today or from tomorrow
    stats = {
        "maths": await maths.summary(p) if "maths" in on else None,
        "tables": await tables.mastered_count(p) if "tables" in on else None,
        "spelling": await spelling.learned_count(p) if "spelling" in on else None,
        "verbs": await verbs.summary(p) if "verbs" in on else None,
        "grammar": await bank.grammar.summary(p) if "grammar" in on else None,
        "science": await bank.science.summary(p) if "science" in on else None,
    }
    hist = await progress.history(p, ctx.family, 14)
    pending = [(a["key"], a["target"]) for a in nxt] != [(a["key"], a["target"]) for a in now]
    reports = await _reports(p)
    mistakes = await progress.mistakes(p, progress.day_list(7))
    _mark_reported(mistakes, reports)
    return page(request, "child_detail.html", ctx, pupil=p, hist=hist,
                hist_keys=[k for k in ORDER if any(it["key"] == k for h in hist for it in h["items"])],
                stats=stats, added=request.query_params.get("added"), maths_year=maths.engine_year(p["year"]),
                mistakes=mistakes, pending=nxt if pending else None, reports=reports,
                skills=await _skill_views(p, on), plan_items=now, TIPS=TIPS,
                school=await spelling.school_status(p) if "spelling" in on else None,
                focus=[{"title": focus_title(i["subject"], i["strand"]), "until": i["until"]}
                       for i in focus_items(p) if i["subject"] in on], rest_today=rest_day(p),
                pdays=days_text(practice_days_on(p, _tomorrow())),
                days_off=[o for o in p.get("days_off") or [] if o["to"] >= progress.today()])


def _tomorrow() -> str:
    return (datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=1)).isoformat()


REPORT_DAYS = 30
REPORT_OUTCOMES = {"open": "we're checking", "fixed": "fixed, thank you", "not_a_problem": "checked: the question is right"}


def _report_question(r: dict) -> str:
    """The question a report is about, as the family saw it (short)."""
    sv = r.get("served") or {}
    if r.get("activity") == "spelling":
        return f"spelling “{r.get('expected')}”" if r.get("expected") else "a spelling"
    if r.get("activity") == "verbs" and sv.get("base"):
        return f"past forms of “{sv['base']}”"
    q = " ".join(str(sv.get("prompt") or "").split())
    return (q[:110] + "…") if len(q) > 110 else q or ACTIVITIES.get(r.get("activity"), {}).get("title", "a question")


async def _reports(p: dict) -> list:
    """The child's "Something wrong with this question?" reports of the last REPORT_DAYS, newest first, with
    what the team found."""
    since = datetime.datetime.utcnow() - datetime.timedelta(days=REPORT_DAYS)
    out = []
    async for r in db.reports.find({"pupil_id": p["_id"], "ts": {"$gt": since}}).sort("ts", -1).limit(20):
        sv = r.get("served") or {}
        t = local_time(r["ts"])
        out.append({"activity": r.get("activity"), "question": _report_question(r), "note": r.get("note") or "",
                    "reason": REPORT_REASONS.get(r.get("reason"), ""), "status": r.get("status") or "open",
                    "outcome": REPORT_OUTCOMES.get(r.get("status") or "open", ""), "reply": r.get("reply") or "",
                    "answer": r.get("answer") or "", "expected": r.get("expected"), "day": r.get("day", ""),
                    "when": f"{t.day} {t:%b} {t:%H:%M}", "prompt": " ".join(str(sv.get("prompt") or "").split())})
    return out


def _mark_reported(mistakes: list, reports: list) -> None:
    """Mark a mistake "reported" when the child reported that question (the same question that day; for the
    activities that keep one prompt for every item, the same expected answer)."""
    keys = {(r["day"], r["activity"], r["prompt"]) for r in reports if r["prompt"]} | \
           {(r["day"], r["activity"], "=" + str(r["expected"])) for r in reports if r["expected"] is not None}
    for d in mistakes:
        for it in d.get("items", []) + d.get("fixed", []):
            same_q = (d["day"], it.get("activity"), " ".join(str(it.get("q", "")).split())) in keys
            same_a = it.get("activity") in ("spelling", "tables", "verbs", "numbers") and \
                (d["day"], it.get("activity"), "=" + str(it.get("exp", ""))) in keys
            it["reported"] = same_q or same_a


def _by_strand(skills: list, scores: dict) -> list:
    """[{strand, secure, practising, new, skills: [{title, score, state}]}] in teaching order. Secure = mastered
    (score 100); practising = answered at least once; not started = never asked yet."""
    out: dict = {}
    for s in skills:
        sc = scores.get(s["key"])
        state = "new" if sc is None else "secure" if sc >= maths_mastery.MASTERED else "practising"
        g = out.setdefault(s["strand"], {"strand": s["strand"], "secure": 0, "practising": 0, "new": 0, "skills": []})
        g[state] += 1
        g["skills"].append({"title": s["title"], "score": sc or 0, "state": state})
    rank = {"practising": 0, "secure": 1, "new": 2}           # the weakest started skills first
    for g in out.values():
        g["skills"].sort(key=lambda s: (rank[s["state"]], s["score"] if s["state"] == "practising" else 0))
    return list(out.values())


async def _skill_views(p: dict, on: set) -> dict:
    """Where the child is secure or still practising, strand by strand, for maths and the question banks."""
    out = {}
    if "maths" in on:
        mm = await maths_mastery._mastery_map(p["_id"])
        year = maths.engine_year(p["year"])
        out["maths"] = _by_strand(maths_mastery._year_skills(year),
                                  {k: int(d.get("score", 0)) for k, d in mm.items() if d.get("attempts", 1)})
    for subject in ("grammar", "science"):
        if subject in on:
            mm = {d["key"]: int(d.get("score", 0)) async for d in db.bank_mastery.find({"pupil_id": p["_id"], "subject": subject})}
            out[subject] = _by_strand(bank_engine.skills(subject, p["year"]), mm)
    return out


def _form_reward(form, family: dict) -> dict | None:
    """The child's own reward from the form; None (use the family's) when left empty or without the plan."""
    text = (form.get("reward_text") or "").strip()[:120]
    if not text or not plan_of(family)["rewards"]:
        return None
    try:
        threshold = int(form.get("reward_threshold") or 100)
    except ValueError:
        threshold = 100
    return {"text": text, "threshold": max(10, min(100, threshold))}


def _acts(p: dict) -> dict:
    """The child's plan, with any activity added since they were set up at its default."""
    return {**default_activities(p["year"]), **(p.get("activities") or {})}


# What a child's settings form holds, in groups: (key, what a parent calls it, its field names; a name ending in "_"
# stands for every field that starts with it). A save changes only the groups edited on that form (_changed_fields).
FORM_GROUPS = [("name", "the name", ("name",)), ("year", "the school year", ("year",)), ("pin", "the PIN", ("pin",)),
               ("reward", "the reward", ("reward_text", "reward_threshold")),
               ("plan", "the daily plan", ("on_", "target_", "check_", "plan_today")),
               ("school", "the spelling list", ("school_words", "school_ok")), ("focus", "the school focus", ("focus_",)),
               ("pdays", "the practice days", ("pday",)), ("off", "the days off", ("off_",)),
               ("reading", "the reading settings", ("read_",))]
GROUP_LABELS = {k: label for k, label, _ in FORM_GROUPS}
CARER_GROUPS = {"school", "off"}           # a carer may type the school's spelling list and mark a day off
SAVED_AS = {"name": "name", "year": "year", "pin": "pin", "reward": "reward", "activities": "plan", "school_words": "school",
            "focus": "focus", "practice_days": "pdays", "days_off": "off", "reading": "reading"}


def _changed_fields(form) -> set | None:
    """The fields whose values differ from what the form showed when it was opened (`orig`, written by the form's
    script), or None without it (no script: everything counts as edited)."""
    try:
        pairs = json.loads(form.get("orig") or "")
    except ValueError:
        return None
    if not isinstance(pairs, list):
        return None
    orig: dict = {}
    for kv in pairs:
        if isinstance(kv, list) and len(kv) == 2:
            orig.setdefault(str(kv[0]), []).append(str(kv[1]))
    now = {k: [str(v) for v in form.getlist(k)] for k in set(form.keys()) - {"orig", "loaded"}}
    return {k for k in set(orig) | set(now) if orig.get(k, []) != now.get(k, [])}


def _groups(changed: set | None) -> set:
    if changed is None:
        return {k for k, _, _ in FORM_GROUPS}
    return {k for k, _, names in FORM_GROUPS
            if any(c == n or (n.endswith("_") and c.startswith(n)) for c in changed for n in names)}


def _edits_since(p: dict, ctx: Ctx, loaded: str | None) -> list:
    """The other grown-ups' saves of this child's settings after a form was opened (loaded: its UTC time)."""
    try:
        t = datetime.datetime.fromisoformat(loaded or "")
    except ValueError:
        return []
    return [e for e in p.get("edits") or [] if e["at"] > t and e["by"] != ctx.account["_id"]]


def _save_note(p: dict, ctx: Ctx, loaded: str | None) -> str:
    """After a save: who else saved since this form was opened, and whether both changed the same thing."""
    others = _edits_since(p, ctx, loaded)
    mine = next((e for e in reversed(p.get("edits") or []) if e["by"] == ctx.account["_id"]), None)
    if not others or not mine:
        return ""
    o = others[-1]
    note = (f"{o['who']} also saved {p['name']}'s settings at {local_time(o['at']):%H:%M}, after you opened this page. "
            f"Only what you changed here was saved, so their changes stay.")
    both = [GROUP_LABELS[g] for g, _, _ in FORM_GROUPS if g in set(mine["groups"]) & {g for e in others for g in e["groups"]}]
    if both:
        note += f" You both changed {' and '.join(both)}: yours is the one saved now."
    return note


async def _edit_page(request: Request, ctx: Ctx, p: dict, status_code: int = 200, draft: dict | None = None, **kw):
    last = (p.get("edits") or [None])[-1]           # the last save, when it was another grown-up's this week
    if not last or last["by"] == ctx.account["_id"] or last["at"] < datetime.datetime.utcnow() - datetime.timedelta(days=7):
        last = None
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p),
                started=await _started_today(p), today_items=todays_plan(p, ctx.family), limited=not ctx.full,
                loaded=datetime.datetime.utcnow().isoformat(), status_code=status_code,
                last_edit={"who": last["who"], "when": local_time(last["at"]).strftime("%d %b at %H:%M"),
                           "what": [GROUP_LABELS.get(g, g) for g in last["groups"]]} if last else None,
                **_school_week_view(p, ctx.family, draft), **kw)


@router.get("/children/{pid}/edit")
async def child_edit_form(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    return await _edit_page(request, ctx, p, save_note=_save_note(p, ctx, request.query_params.get("loaded"))
                            if request.query_params.get("saved") else "")


def _merge_acts(p: dict, form, year: int, changed: set | None) -> dict:
    """The plan with only the activities edited on this form taken from it; the others stay as saved now."""
    acts, sent = {k: dict(v) for k, v in _acts(p).items()}, _form_activities(form, year)
    for k in ORDER:
        if changed is None or {f"on_{k}", f"target_{k}", f"check_{k}"} & changed:
            acts[k] = sent[k]
        if year < ACTIVITIES[k]["min_year"]:
            acts[k]["on"] = False
    return acts


@router.post("/children/{pid}/edit")
async def child_edit(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    """Save a child's settings. Two grown-ups may have the page open at once: only what was edited on this form
    changes, so one parent's save never puts back what the other changed. Without the form's script nothing can tell
    what was edited, so a form opened before someone else's save is refused instead. A carer may change only the
    school's spelling list and the days off."""
    p = await own_pupil(ctx, pid)
    form = await request.form()
    changed = _changed_fields(form)
    groups = _groups(changed)
    if form.get("plan_today"):        # "Change today's plan too" applies the saved plan and practice days to today
        groups |= {"plan", "pdays"}
    groups &= CARER_GROUPS if not ctx.full else _groups(None)
    others = _edits_since(p, ctx, form.get("loaded"))
    if changed is None and others:
        o = others[-1]
        return await _edit_page(request, ctx, p, status_code=409,
                                error=f"{o['who']} changed {p['name']}'s settings at {local_time(o['at']):%H:%M}, after "
                                      f"you opened this page. Here they are now: make your change again and save.")
    name = (form.get("name") or p["name"]).strip()[:30]
    try:
        year = int(form.get("year") or p["year"])
    except ValueError:
        year = p["year"]
    if year not in YEARS or "year" not in groups:
        year = p["year"]
    school, err = _form_school_words(form, p) if "school" in groups else ({}, "")
    rest, err = (await _form_rest(form, p, weekdays="pdays" in groups)) if not err else ({}, err)
    if err:
        return await _edit_page(request, ctx, p, status_code=400, error=err,
                                draft={k: form.get(k) or "" for k in ("school_words", "off_from", "off_to")})
    upd = {**school, **rest}
    if "name" in groups:
        upd["name"] = name or p["name"]
    if "year" in groups and year != p["year"]:
        upd["year"] = year
    if "reward" in groups:
        upd["reward"] = _form_reward(form, ctx.family)
    if "plan" in groups or year != p["year"]:
        upd.update(await _new_plan(p, _merge_acts(p, form, year, changed), bool(form.get("plan_today"))))
    if "focus" in groups or year != p["year"]:
        upd.update(_form_focus(form, p, ctx.family, year))
    if form.get("reading_form") and "reading" in groups:   # "Reading" (child_form.html): the child's "Aa" settings, on every device
        upd["reading"] = {k: bool(form.get(f"read_{k}")) for k in ("big", "dys", "space", "calm", "contrast")}
    today = progress.today()
    if form.get("plan_today") and "plan_log" in upd and ((p.get("kept") or {}).get(today) or {}).get("pct"):
        # "Change today's plan too" reopens a finished day when today's plan grew: the child sees what is left
        # (a reward already earned stays earned, see progress.board)
        if [(a["key"], a["target"]) for a in todays_plan({**p, **upd}, ctx.family)] != \
                [(a["key"], a["target"]) for a in todays_plan(p, ctx.family)]:
            upd[f"kept.{today}.pct"] = 0
    pin = (form.get("pin") or "").strip() if "pin" in groups else ""
    if pin:
        if not PIN_RE.match(pin):
            return await _edit_page(request, ctx, p, status_code=400, error="The PIN is 4 numbers, like 2580.")
        # pin_view: shown to the parent (a minder must be able to find it); a 4-digit hash would not protect it anyway.
        upd["pin"], upd["pin_view"] = hash_secret(pin), pin
    done = sorted({g for k, g in SAVED_AS.items() if k in upd and upd[k] != p.get(k)} | ({"plan"} if "plan_log" in upd else set()))
    if done:
        upd["edits"] = (p.get("edits") or [])[-4:] + [{"at": datetime.datetime.utcnow(), "by": ctx.account["_id"],
                                                       "who": adult_name(ctx.account), "groups": done}]
    if upd:
        await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    if pin:
        await clear_pin_lock(p["_id"])           # a new PIN also lifts a lock from wrong guesses
        await log_event(ctx.family["_id"], "pin", f"{adult_name(ctx.account)} changed {p['name']}'s PIN", pupil_id=p["_id"])
    loaded = form.get("loaded") or ""
    return RedirectResponse(f"/children/{p['_id']}/edit?saved=1{'&pin=1' if pin else ''}"
                            f"{'&loaded=' + loaded if others and loaded else ''}", 303)


async def _started_today(p: dict) -> bool:
    return bool(await db.attempts.find_one({"pupil_id": p["_id"], "day": progress.today()}, {"_id": 1}))


async def _new_plan(p: dict, acts: dict, today_too: bool) -> dict:
    """The update for a changed plan. Once the child has started today, it starts tomorrow: today keeps the plan
    it started with, and history keeps each day's own plan (plan_log). Before the child starts, or when the
    parent asks, it starts today; a reward already earned today is kept anyway (progress.day_status)."""
    if acts == _acts(p) and not today_too:
        return {}
    start = progress.today() if today_too or not await _started_today(p) else _tomorrow()
    log = p.get("plan_log") or [{"from": "", "acts": _acts(p)}]
    log = [e for e in log if e["from"] < start]
    cutoff = progress.day_list(15)[0]               # older entries matter only for the last that started before
    keep = [e for e in log if e["from"] >= cutoff]
    log = ([e for e in log if e["from"] < cutoff][-1:] + keep)[-20:] + [{"from": start, "acts": acts}]
    return {"activities": acts, "plan_log": log}


# ---- the school's week: its spelling list, the topic the class is on, and rest days ----

def _plus_days(n: int) -> str:
    return (datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=n)).isoformat()


def _focus_options(p: dict, family: dict) -> dict:
    """The strands of the child's year a parent can pick: {"maths": [strand, ...], "grammar": [...], ...}."""
    allowed, out = plan_of(family)["activities"], {}
    if "maths" in allowed:
        out["maths"] = list(dict.fromkeys(s["strand"] for s in maths_mastery._year_skills(maths.engine_year(p["year"]))))
    for subj in ("grammar", "science"):
        if subj in allowed and p["year"] >= ACTIVITIES[subj]["min_year"]:
            out[subj] = list(dict.fromkeys(s["strand"] for s in bank_engine.skills(subj, p["year"])))
    return out


def _focus_groups(opts: dict) -> list:
    """The focus menu, in groups: [(label, subject, [strand, ...])]; science by Biology, Chemistry and Physics."""
    out = [("Maths", "maths", opts.get("maths", [])), ("Grammar and punctuation", "grammar", opts.get("grammar", []))]
    sci = opts.get("science", [])
    for area in SCIENCE_AREAS:
        out.append((f"Science: {area}" if area != "Working scientifically" else "Science: working scientifically",
                    "science", [x for x in sci if SCIENCE_AREA.get(x) == area]))
    out.append(("Science", "science", [x for x in sci if x not in SCIENCE_AREA]))     # a strand not mapped yet
    return [g for g in out if g[2]]


def _form_focus(form, p: dict, family: dict, year: int) -> dict:
    """The update for "Working on this at school": up to FOCUS_MAX strands of any subjects, each for its own 1 or
    2 weeks. A strand picked again keeps its first day (a new number of weeks counts from it); a new pick runs from
    today; "Nothing" in every row (or a new school year) ends the focus."""
    if "focus_0" not in form and year == p["year"]:
        return {}
    cur = focus_items(p)
    if year != p["year"]:
        return {"focus": None} if p.get("focus") else {}
    opts, was = _focus_options(p, family), {(i["subject"], i["strand"]): i for i in cur}
    new = []
    for n in range(FOCUS_MAX):
        subj, _, strand = (form.get(f"focus_{n}") or "").partition(":")
        if not strand or strand not in opts.get(subj, []) or any(i["subject"] == subj and i["strand"] == strand for i in new):
            continue
        try:
            weeks = int(form.get(f"focus_weeks_{n}") or 1)
        except ValueError:
            weeks = 1
        weeks = weeks if weeks in FOCUS_WEEKS else 1
        start = was[(subj, strand)]["from"] if (subj, strand) in was else progress.today()
        until = (datetime.date.fromisoformat(start) + datetime.timedelta(weeks=weeks)).isoformat()
        if until <= progress.today():             # picked again after its weeks are over: a new run from today
            start, until = progress.today(), _plus_days(7 * weeks)
        new.append({"subject": subj, "strand": strand, "weeks": weeks, "from": start, "until": until})
    if new == cur and isinstance(p.get("focus"), list):
        return {}
    return {"focus": new or None} if (new or p.get("focus")) else {}


def _form_school_words(form, p: dict) -> tuple[dict, str]:
    """The update for the school's spelling list, and an error to show. A new list runs for SCHOOL_DAYS from today;
    the same list saved again keeps its dates; an emptied box ends it."""
    if "school_words" not in form:
        return {}, ""
    words, err = spelling.parse_school_words(form.get("school_words") or "")
    if err:
        return {}, err
    if words == spelling.school_words(p):
        return {}, ""
    if not words:
        return ({"school_words": None} if p.get("school_words") else {}), ""
    doubt = "" if form.get("school_ok") else spelling.school_doubts(form.get("school_words") or "")
    if doubt:                                    # a sentence typed without its dash: asked under the box, before saving
        return {}, "Nothing is saved yet: check the spelling list below."
    return {"school_words": spelling.new_school_list(p, words, progress.today(), _plus_days(spelling.SCHOOL_DAYS))}, ""


async def _form_rest(form, p: dict, weekdays: bool = True) -> tuple[dict, str]:
    """The update for practice days and days off, and an error to show. A change of weekdays follows the plan's
    rule (from tomorrow once the child has started today); a day off applies at once, today included. Days off
    are changes (one added, those ticked removed), so they never undo another grown-up's; weekdays=False leaves
    the weekdays alone (a carer, or a form where they were not edited)."""
    if "pdays_form" not in form and "off_form" not in form:
        return {}, ""
    upd = {}
    weekdays = weekdays and "pdays_form" in form
    days = sorted({int(d) for d in form.getlist("pday") if str(d).isdigit() and int(d) in ALL_WEEK})
    if weekdays and not days:
        return {}, "Tick at least one practice day. For a break, add days off instead."
    cur = p.get("practice_days")
    start = progress.today() if form.get("plan_today") or not await _started_today(p) else _tomorrow()
    if weekdays and (days != (ALL_WEEK if cur is None else sorted(cur)) or days != sorted(practice_days_on(p, start))):
        log = [e for e in p.get("days_log") or [{"from": "", "days": ALL_WEEK if cur is None else cur}] if e["from"] < start]
        cutoff = progress.day_list(15)[0]
        log = ([e for e in log if e["from"] < cutoff][-1:] + [e for e in log if e["from"] >= cutoff])[-20:]
        upd.update({"practice_days": days, "days_log": log + [{"from": start, "days": days}]})
    today = progress.today()
    gone = set(form.getlist("off_remove"))
    # past days off are kept for a term, as the printed report lists them
    offs = [o for o in p.get("days_off") or []
            if o["to"] >= progress.day_list(130)[0] and not (o["to"] >= today and f"{o['from']}|{o['to']}" in gone)]
    first, last = (form.get("off_from") or "").strip(), (form.get("off_to") or "").strip()
    if first or last:
        try:
            d1 = datetime.date.fromisoformat(first or last)
            d2 = datetime.date.fromisoformat(last) if last else d1
        except ValueError:
            return {}, "Pick the day off from the calendar."
        if d1.isoformat() < today:
            return {}, "A day off can start today or later."
        if d2 < d1:
            return {}, "The last day off is before the first one. Swap them round."
        if (d2 - d1).days + 1 > MAX_DAYS_OFF:
            return {}, f"Days off can cover up to {MAX_DAYS_OFF // 7} weeks at a time. Add the rest as another break."
        if d1.isoformat() > _plus_days(366):
            return {}, "Pick a day within the next year."
        offs.append({"from": d1.isoformat(), "to": d2.isoformat()})
    offs = sorted({(o["from"], o["to"]) for o in offs})[-20:]
    offs = [{"from": a, "to": b} for a, b in offs]
    if offs != (p.get("days_off") or []):
        upd["days_off"] = offs
    return upd, ""


def _school_week_view(p: dict, family: dict, draft: dict | None = None) -> dict:
    """What the child form shows for the school list, the focus and rest days (draft: what the parent typed,
    shown again with an error)."""
    today = progress.today()
    sl = spelling.school_words(p)
    return {"school_text": (draft or {}).get("school_words", spelling.school_text(sl)),
            "school_until": p["school_words"]["until"] if sl else "", "school_max": spelling.SCHOOL_MAX,
            "school_sum": spelling.school_summary(sl, p["name"]) if sl and not draft else None,
            "school_doubt": spelling.school_doubts((draft or {}).get("school_words") or ""),
            "focus_groups": _focus_groups(_focus_options(p, family)), "focus_now": focus_items(p),
            "focus_max": FOCUS_MAX, "focus_title": focus_title,
            "pdays": ALL_WEEK if p.get("practice_days") is None else p["practice_days"], "WEEKDAYS": WEEKDAYS,
            "days_off": [o for o in p.get("days_off") or [] if o["to"] >= today], "today_iso": today,
            "max_off": _plus_days(366), "draft": draft or {}, "strand_label": strand_label}


async def _delete_pupils(ids: list) -> None:
    for c in ("maths_lab_q", "maths_attempts", "maths_mastery"):
        await db[c].delete_many({"pupil": {"$in": ids}})
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items",
              "reports"):
        await db[c].delete_many({"pupil_id": {"$in": ids}})
    # A device that child was using goes back to "Who's learning?", still locked: never to parent mode.
    await db.sessions.update_many({"child_id": {"$in": ids}}, {"$set": {"child_id": None, "locked": True}})
    await db.pupils.delete_many({"_id": {"$in": ids}})


@router.get("/children/{pid}/delete")
async def child_delete_form(request: Request, pid: str, ctx: Ctx = Depends(full_page)):
    """Deleting a child is its own page, asking for the password: never one tap next to Save."""
    p = await own_pupil(ctx, pid)
    return page(request, "child_delete.html", ctx, pupil=p, answers=await db.attempts.count_documents({"pupil_id": p["_id"]}),
                others=await db.accounts.count_documents({"family_id": ctx.family["_id"], "_id": {"$ne": ctx.account["_id"]},
                                                          "role": {"$in": ["owner", "parent"]}}))


@router.post("/children/{pid}/delete")
async def child_delete(request: Request, pid: str, ctx: Ctx = Depends(full_page), password: str = Form("")):
    """Any parent may delete a child (a carer may not), with their own password. The other parents are told."""
    p = await own_pupil(ctx, pid)
    key, err = f"delete:{ctx.account['_id']}", ""
    if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
        err = f"Too many wrong passwords. Try again in {UNLOCK_MINUTES} minutes."
    elif not verify_secret(password, ctx.account["pw"]):
        await hit(key)
        err = "That password is not right. Type your own password to delete." if password else "Type your password to delete."
    if err:
        return page(request, "child_delete.html", ctx, pupil=p, status_code=400, error=err,
                    answers=await db.attempts.count_documents({"pupil_id": p["_id"]}))
    await _delete_pupils([p["_id"]])
    who, fam = adult_name(ctx.account), ctx.family["name"]
    await log_event(ctx.family["_id"], "child", f"{who} deleted {p['name']}'s profile and practice")
    await mailer.to_family(ctx.family["_id"], f"{who} deleted {p['name']}'s profile on Quizocracy",
                           f"Hello,\n\n{who} ({ctx.account['email']}) deleted {p['name']}'s profile on {fam}, with all of "
                           f"{p['name']}'s practice, on {local_time(datetime.datetime.utcnow()):%d %B %Y at %H:%M}. "
                           f"It cannot be undone.\n\nIf you did not expect this, talk to {who}. If you think someone "
                           f"else has their password, write to us at {config.SUPPORT_EMAIL}.\n",
                           skip=(ctx.account["_id"],))
    return RedirectResponse(f"/home?deleted=1&deleted_name={p['name']}", 303)


@router.get("/settings")
async def settings_form(request: Request, ctx: Ctx = Depends(parent_page)):
    return page(request, "settings.html", ctx, plan=plan_of(ctx.family), saved=request.query_params.get("saved"),
                **await settings_view(ctx))


@router.post("/settings")
async def settings(request: Request, ctx: Ctx = Depends(full_page), family_name: str = Form(""),
                   reward_text: str = Form(""), reward_threshold: int = Form(100)):
    upd = {"name": (family_name.strip() or ctx.family["name"])[:60]}
    if plan_of(ctx.family)["rewards"]:
        upd["reward"] = {"text": reward_text.strip()[:120], "threshold": max(10, min(100, reward_threshold))}
    await db.families.update_one({"_id": ctx.family["_id"]}, {"$set": upd})
    return RedirectResponse("/settings?saved=1", 303)


@router.get("/account/export")
async def export(request: Request, ctx: Ctx = Depends(full_page)):
    fid = ctx.family["_id"]
    pupils = await _pupils(ctx)
    ids = [p["_id"] for p in pupils]
    accounts = [{k: v for k, v in a.items() if k != "pw"} async for a in db.accounts.find({"family_id": fid})]
    data = {"exported": datetime.datetime.utcnow(), "times": "UTC", "family": ctx.family, "accounts": accounts,
            "children": [{k: v for k, v in p.items() if k not in ("pin", "pin_view")} for p in pupils],
            "devices": [{k: s.get(k) for k in ("created", "expires", "child_id")}
                        async for s in db.sessions.find({"family_id": fid})]}
    # Every per-child collection that deleting a child removes (see _delete_pupils), so the file is complete.
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items",
              "reports"):
        data[c] = [d async for d in db[c].find({"pupil_id": {"$in": ids}}, {"_id": 0})]
    for c in ("maths_attempts", "maths_mastery", "maths_lab_q"):
        data[c] = [d async for d in db[c].find({"pupil": {"$in": ids}}, {"_id": 0})]
    data["family_log"] = [d async for d in db.family_log.find({"family_id": fid}, {"_id": 0})]
    data["emails"] = [d async for d in db.outbox.find({"to": {"$in": [a["email"] for a in accounts]}},
                                                      {"_id": 0, "to": 1, "subject": 1, "created": 1})]
    body = json.dumps(data, default=_json_default, indent=1)
    return Response(body, media_type="application/json",
                    headers={"Content-Disposition": 'attachment; filename="quizocracy-export.json"',
                             "Cache-Control": "no-store"})


def _json_default(o):
    return o.isoformat() + "Z" if isinstance(o, datetime.datetime) else str(o)


@router.post("/account/delete")
async def delete_account(request: Request, ctx: Ctx = Depends(full_page), password: str = Form(...),
                         confirm: str = Form("")):
    if confirm.strip().upper() != "DELETE" or not verify_secret(password, ctx.account["pw"]):
        return page(request, "settings.html", ctx, plan=plan_of(ctx.family), status_code=400,
                    delete_error="Type DELETE and your password to delete the account.", **await settings_view(ctx))
    fid = ctx.family["_id"]
    await _delete_pupils([p["_id"] async for p in db.pupils.find({"family_id": fid}, {"_id": 1})])
    # every adult's address, and the ones they changed from, so the mail log about them goes too
    emails = [e async for a in db.accounts.find({"family_id": fid}) for e in [a["email"], *a.get("past_emails", [])]]
    for c in FAMILY_COLLECTIONS:
        await db[c].delete_many({"family_id": fid})
    await db.codes.delete_many({"family_id": fid})             # invitations still open
    await db.weekly_sends.delete_many({"family_id": fid})
    await db.codes.delete_many({"email": {"$in": emails}})
    await db.outbox.delete_many({"to": {"$in": emails}})
    await db.families.delete_one({"_id": fid})
    resp = RedirectResponse("/?deleted=1", 303)
    resp.delete_cookie("qz_s", path="/")
    return resp


@router.post("/handover")
async def handover(request: Request, ctx: Ctx = Depends(family_page)):
    """Lock the device before it changes hands: from here only a child's PIN or the parent's password works."""
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"locked": True}})
    return RedirectResponse("/learn", 303)


@router.get("/parent-unlock")
async def unlock_form(request: Request, ctx: Ctx = Depends(family_page)):
    if not ctx.locked:
        return RedirectResponse("/home", 303)
    return page(request, "unlock.html", ctx)


UNLOCK_FAILS, UNLOCK_MINUTES = 8, 15


@router.post("/parent-unlock")
async def unlock(request: Request, ctx: Ctx = Depends(family_page), password: str = Form(...)):
    key = f"unlock:{ctx.family['_id']}"          # per family, so every device of the family shares the count
    if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
        return page(request, "unlock.html", ctx, status_code=429,
                    error=f"Too many wrong passwords. The parent area is locked for {UNLOCK_MINUTES} minutes.")
    adult = await family_adult(ctx, password)
    if not adult:
        await hit(key)
        return page(request, "unlock.html", ctx, error="That password is not right.", status_code=400)
    await db.login_failures.delete_many({"email": key})
    now = datetime.datetime.utcnow()
    # handed: this device has been in a child's hands, so parent mode here locks itself when left idle (deps).
    # Any adult of the family can open it, and the device is then theirs, with their own rights (a carer's or a parent's).
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": False,
                                                                        "parent_ok_at": now, "seen_at": now,
                                                                        "handed": True, "timed_out": False,
                                                                        "account_id": adult["_id"]}})
    return RedirectResponse("/home", 303)


@router.post("/children/{pid}/pin-unlock")
async def pin_unlock(request: Request, pid: str, ctx: Ctx = Depends(family_page), password: str = Form(""),
                     back: str = Form("")):
    """Lift a child's lock after wrong PINs: from Home in parent mode, or on "Who's learning?" with the password."""
    p = await own_pupil(ctx, pid)
    adult = ctx.account
    if ctx.locked:
        key = f"unlock:{ctx.family['_id']}"      # the same count as the parent-area password
        err = None
        if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
            err = f"Too many wrong passwords. Try again in {UNLOCK_MINUTES} minutes."
        elif not (adult := await family_adult(ctx, password)):
            await hit(key)
            err = "That password is not right. Use your own password (any grown-up on this family)."
        if err:
            return await picker_page(request, ctx, pin_for=p["_id"], unlock_error=err, status_code=400)
    if await pin_lock_until(p["_id"]):
        await log_event(ctx.family["_id"], "pin_unlock", f"{adult_name(adult)} unlocked {p['name']}", pupil_id=p["_id"])
    await clear_pin_lock(p["_id"])
    return RedirectResponse(f"/{'home' if back == 'home' and not ctx.locked else 'learn'}?unlocked={p['_id']}", 303)


@router.get("/board")
async def board(request: Request, ctx: Ctx = Depends(family_page)):
    pupils = await _pupils(ctx)
    return page(request, "board.html", ctx, board=await progress.board(ctx.family, pupils), today=progress.today(),
                today_label=_nice_day(progress.today()))


def _nice_day(day: str) -> str:
    """"2026-11-10" -> "Tuesday 10 November"."""
    d = datetime.date.fromisoformat(day)
    return f"{d:%A} {d.day} {d:%B}"
