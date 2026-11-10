"""The parent's side: children, their plans, progress, rewards, the account and its data."""
import datetime
import json
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response

from ..activities import (ACTIVITIES, ORDER, PLANS, SECONDS, YEARS, default_activities, minutes, plan_of,
                          todays_plan, year_pace)
from ..bank import engine as bank_engine
from ..maths import maths_mastery
from ..db import FAMILY_COLLECTIONS, db
from ..deps import Ctx, clear_pin_lock, family_page, hit, over_limit, own_pupil, parent_page, pin_locks
from ..drills import bank, maths, spelling, tables, verbs
from .. import progress
from ..tips import TIPS
from ..security import hash_secret, new_id, verify_secret
from ..web import page, templates
from .child import picker_page

router = APIRouter()
PIN_RE = re.compile(r"^\d{4}$")
# What the child form's script needs to tick a year's defaults and estimate the minutes as the parent edits.
templates.env.globals["PLAN_JS"] = {"defaults": {y: default_activities(y) for y in YEARS}, "seconds": SECONDS,
                                    "pace": {y: year_pace(y) for y in YEARS},
                                    "min_year": {k: a["min_year"] for k, a in ACTIVITIES.items()}}


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
                unlocked=request.query_params.get("unlocked"))


def _form_activities(form, year: int) -> dict:
    acts = {}
    for k in ORDER:
        try:
            target = max(1, min(200, int(form.get(f"target_{k}") or ACTIVITIES[k]["target"])))
        except ValueError:
            target = ACTIVITIES[k]["target"]
        acts[k] = {"on": bool(form.get(f"on_{k}")) and year >= ACTIVITIES[k]["min_year"], "target": target}
    return acts


def _full_reason(family: dict) -> str:
    """Why no more children: the plan can be upgraded ("children"), or the biggest plan is full ("limit")."""
    return "limit" if plan_of(family)["max_children"] >= max(p["max_children"] for p in PLANS.values()) else "children"


@router.get("/children/new")
async def child_new_form(request: Request, ctx: Ctx = Depends(parent_page)):
    if len(await _pupils(ctx)) >= plan_of(ctx.family)["max_children"]:
        return page(request, "upgrade.html", ctx, reason=_full_reason(ctx.family), plan=plan_of(ctx.family))
    # the year list opens on Year 1, so its plan is ticked; the form's script re-ticks when the year changes
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=None, years=YEARS,
                acts=default_activities(YEARS[0]))


@router.post("/children/new")
async def child_new(request: Request, ctx: Ctx = Depends(parent_page)):
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
    return page(request, "child_detail.html", ctx, pupil=p, hist=hist,
                hist_keys=[k for k in ORDER if any(it["key"] == k for h in hist for it in h["items"])],
                stats=stats, added=request.query_params.get("added"), maths_year=maths.engine_year(p["year"]),
                mistakes=await progress.mistakes(p, progress.day_list(7)), pending=nxt if pending else None,
                skills=await _skill_views(p, on), plan_items=now, TIPS=TIPS)


def _tomorrow() -> str:
    return (datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=1)).isoformat()


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


@router.get("/children/{pid}/edit")
async def child_edit_form(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p),
                started=await _started_today(p), today_items=todays_plan(p, ctx.family))


@router.post("/children/{pid}/edit")
async def child_edit(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    form = await request.form()
    name = (form.get("name") or p["name"]).strip()[:30]
    try:
        year = int(form.get("year") or p["year"])
    except ValueError:
        year = p["year"]
    if year not in YEARS:
        year = p["year"]
    upd = {"name": name or p["name"], "year": year, "reward": _form_reward(form, ctx.family),
           **await _new_plan(p, _form_activities(form, year), bool(form.get("plan_today")))}
    pin = (form.get("pin") or "").strip()
    if pin:
        if not PIN_RE.match(pin):
            return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p),
                        error="The PIN is 4 numbers, like 2580.", status_code=400)
        # pin_view: shown to the parent (a minder must be able to find it); a 4-digit hash would not protect it anyway.
        upd["pin"], upd["pin_view"] = hash_secret(pin), pin
    await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    if pin:
        await clear_pin_lock(p["_id"])           # a new PIN also lifts a lock from wrong guesses
    return RedirectResponse(f"/children/{p['_id']}/edit?saved=1{'&pin=1' if pin else ''}", 303)


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


async def _delete_pupils(ids: list) -> None:
    for c in ("maths_lab_q", "maths_attempts", "maths_mastery"):
        await db[c].delete_many({"pupil": {"$in": ids}})
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items"):
        await db[c].delete_many({"pupil_id": {"$in": ids}})
    # A device that child was using goes back to "Who's learning?", still locked: never to parent mode.
    await db.sessions.update_many({"child_id": {"$in": ids}}, {"$set": {"child_id": None, "locked": True}})
    await db.pupils.delete_many({"_id": {"$in": ids}})


@router.post("/children/{pid}/delete")
async def child_delete(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    await _delete_pupils([p["_id"]])
    return RedirectResponse("/home?deleted=1", 303)


@router.get("/settings")
async def settings_form(request: Request, ctx: Ctx = Depends(parent_page)):
    return page(request, "settings.html", ctx, plan=plan_of(ctx.family), saved=request.query_params.get("saved"))


@router.post("/settings")
async def settings(request: Request, ctx: Ctx = Depends(parent_page), family_name: str = Form(""),
                   reward_text: str = Form(""), reward_threshold: int = Form(100)):
    upd = {"name": (family_name.strip() or ctx.family["name"])[:60]}
    if plan_of(ctx.family)["rewards"]:
        upd["reward"] = {"text": reward_text.strip()[:120], "threshold": max(10, min(100, reward_threshold))}
    await db.families.update_one({"_id": ctx.family["_id"]}, {"$set": upd})
    return RedirectResponse("/settings?saved=1", 303)


@router.get("/account/export")
async def export(request: Request, ctx: Ctx = Depends(parent_page)):
    fid = ctx.family["_id"]
    pupils = await _pupils(ctx)
    ids = [p["_id"] for p in pupils]
    accounts = [{k: v for k, v in a.items() if k != "pw"} async for a in db.accounts.find({"family_id": fid})]
    data = {"exported": datetime.datetime.utcnow(), "times": "UTC", "family": ctx.family, "accounts": accounts,
            "children": [{k: v for k, v in p.items() if k not in ("pin", "pin_view")} for p in pupils],
            "devices": [{k: s.get(k) for k in ("created", "expires", "child_id")}
                        async for s in db.sessions.find({"family_id": fid})]}
    # Every per-child collection that deleting a child removes (see _delete_pupils), so the file is complete.
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items"):
        data[c] = [d async for d in db[c].find({"pupil_id": {"$in": ids}}, {"_id": 0})]
    for c in ("maths_attempts", "maths_mastery", "maths_lab_q"):
        data[c] = [d async for d in db[c].find({"pupil": {"$in": ids}}, {"_id": 0})]
    data["emails"] = [d async for d in db.outbox.find({"to": {"$in": [a["email"] for a in accounts]}},
                                                      {"_id": 0, "to": 1, "subject": 1, "created": 1})]
    body = json.dumps(data, default=_json_default, indent=1)
    return Response(body, media_type="application/json",
                    headers={"Content-Disposition": 'attachment; filename="quizocracy-export.json"',
                             "Cache-Control": "no-store"})


def _json_default(o):
    return o.isoformat() + "Z" if isinstance(o, datetime.datetime) else str(o)


@router.post("/account/delete")
async def delete_account(request: Request, ctx: Ctx = Depends(parent_page), password: str = Form(...),
                         confirm: str = Form("")):
    if confirm.strip().upper() != "DELETE" or not verify_secret(password, ctx.account["pw"]):
        return page(request, "settings.html", ctx, plan=plan_of(ctx.family), status_code=400,
                    delete_error="Type DELETE and your password to delete the account.")
    fid = ctx.family["_id"]
    await _delete_pupils([p["_id"] async for p in db.pupils.find({"family_id": fid}, {"_id": 1})])
    emails = [a["email"] async for a in db.accounts.find({"family_id": fid})]
    for c in FAMILY_COLLECTIONS:
        await db[c].delete_many({"family_id": fid})
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
    if not verify_secret(password, ctx.account["pw"]):
        await hit(key)
        return page(request, "unlock.html", ctx, error="That password is not right.", status_code=400)
    await db.login_failures.delete_many({"email": key})
    now = datetime.datetime.utcnow()
    # handed: this device has been in a child's hands, so parent mode here locks itself when left idle (deps).
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": False,
                                                                        "parent_ok_at": now, "seen_at": now,
                                                                        "handed": True, "timed_out": False}})
    return RedirectResponse("/home", 303)


@router.post("/children/{pid}/pin-unlock")
async def pin_unlock(request: Request, pid: str, ctx: Ctx = Depends(family_page), password: str = Form(""),
                     back: str = Form("")):
    """Lift a child's lock after wrong PINs: from Home in parent mode, or on "Who's learning?" with the password."""
    p = await own_pupil(ctx, pid)
    if ctx.locked:
        key = f"unlock:{ctx.family['_id']}"      # the same count as the parent-area password
        err = None
        if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
            err = f"Too many wrong passwords. Try again in {UNLOCK_MINUTES} minutes."
        elif not verify_secret(password, ctx.account["pw"]):
            await hit(key)
            err = "That parent password is not right."
        if err:
            return await picker_page(request, ctx, pin_for=p["_id"], unlock_error=err, status_code=400)
    await clear_pin_lock(p["_id"])
    return RedirectResponse(f"/{'home' if back == 'home' and not ctx.locked else 'learn'}?unlocked={p['_id']}", 303)


@router.get("/board")
async def board(request: Request, ctx: Ctx = Depends(family_page)):
    pupils = await _pupils(ctx)
    return page(request, "board.html", ctx, board=await progress.board(ctx.family, pupils), today=progress.today())
