"""The parent's side: children, their plans, progress, rewards, the account and its data."""
import datetime
import json
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response

from ..activities import ACTIVITIES, ORDER, PLANS, YEARS, default_activities, plan_of, todays_plan
from ..db import FAMILY_COLLECTIONS, db
from ..deps import Ctx, family_page, hit, over_limit, own_pupil, parent_page
from ..drills import bank, maths, spelling, tables, verbs
from .. import progress
from ..tips import TIPS
from ..security import hash_secret, new_id, verify_secret
from ..web import page

router = APIRouter()
PIN_RE = re.compile(r"^\d{4}$")


async def _pupils(ctx: Ctx) -> list:
    return [p async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]


@router.get("/home")
async def home(request: Request, ctx: Ctx = Depends(parent_page)):
    pupils = await _pupils(ctx)
    board = await progress.board(ctx.family, pupils)
    hist = {p["_id"]: await progress.history(p, ctx.family, 7) for p in pupils}
    full = len(pupils) >= plan_of(ctx.family)["max_children"] and _full_reason(ctx.family) == "limit"
    return page(request, "home.html", ctx, board=board, hist=hist, plan=plan_of(ctx.family), full=full,
                welcome=request.query_params.get("welcome"))


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
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=None, years=YEARS, acts=default_activities(3))


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
        err = "The PIN must be 4 digits."
    if err:
        return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil={"name": name, "year": year}, years=YEARS,
                    acts=default_activities(year or 3), error=err, status_code=400)
    acts = _form_activities(form, year) if form.get("custom") else default_activities(year)
    p = {"_id": new_id("p"), "family_id": ctx.family["_id"], "name": name, "year": year, "pin": hash_secret(pin),
         "activities": acts, "reward": _form_reward(form, ctx.family), "created": datetime.datetime.utcnow()}
    await db.pupils.insert_one(p)
    return RedirectResponse(f"/children/{p['_id']}?added=1", 303)


@router.get("/children/{pid}")
async def child_detail(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    allowed = plan_of(ctx.family)["activities"]
    stats = {
        "maths": await maths.summary(p) if "maths" in allowed else None,
        "tables": await tables.mastered_count(p),
        "spelling": await spelling.learned_count(p),
        "verbs": await verbs.summary(p) if "verbs" in allowed and p["year"] >= ACTIVITIES["verbs"]["min_year"] else None,
        "grammar": await bank.grammar.summary(p) if "grammar" in allowed else None,
        "science": await bank.science.summary(p) if "science" in allowed else None,
    }
    return page(request, "child_detail.html", ctx, pupil=p, hist=await progress.history(p, ctx.family, 14),
                stats=stats, added=request.query_params.get("added"), maths_year=maths.engine_year(p["year"]),
                mistakes=await progress.mistakes(p, progress.day_list(7)),
                plan_items=todays_plan(p, ctx.family), TIPS=TIPS)


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
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p))


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
    upd = {"name": name or p["name"], "year": year, "activities": _form_activities(form, year),
           "reward": _form_reward(form, ctx.family)}
    pin = (form.get("pin") or "").strip()
    if pin:
        if not PIN_RE.match(pin):
            return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p),
                        error="The PIN must be 4 digits.", status_code=400)
        upd["pin"] = hash_secret(pin)
    await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    return RedirectResponse(f"/children/{p['_id']}", 303)


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
            "children": [{k: v for k, v in p.items() if k != "pin"} for p in pupils],
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
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": False,
                                                                        "parent_ok_at": datetime.datetime.utcnow()}})
    return RedirectResponse("/home", 303)


@router.get("/board")
async def board(request: Request, ctx: Ctx = Depends(family_page)):
    pupils = await _pupils(ctx)
    return page(request, "board.html", ctx, board=await progress.board(ctx.family, pupils), today=progress.today())
