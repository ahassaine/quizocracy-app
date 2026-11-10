"""The child's side: pick yourself, enter your PIN, see your day, do the activities."""
import datetime
import json
import re

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from ..activities import todays_plan
from ..config import BASE_DIR
from ..db import db
from ..deps import Ctx, child_api, child_page, family_page, local_hm, own_pupil, pin_lock_until, pin_locks
from ..drills import bank, maths, numbers, spelling, tables, verbs
from .. import items, progress
from ..security import verify_secret
from ..web import page

router = APIRouter()
DRILLS = {"maths": maths, "tables": tables, "spelling": spelling, "numbers": numbers, "verbs": verbs,
          "grammar": bank.grammar, "science": bank.science}
AUDIO_DIR = BASE_DIR / "static" / "audio" / "words"
PIN_RE = re.compile(r"^\d{4}$")


async def picker_page(request: Request, ctx: Ctx, status_code: int = 200, **kw):
    pupils = [p async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]
    return page(request, "learn.html", ctx, pupils=pupils, locks=await pin_locks(pupils), status_code=status_code,
                unlocked=request.query_params.get("unlocked"), **kw)


@router.get("/learn")
async def picker(request: Request, ctx: Ctx = Depends(family_page)):
    if ctx.session.get("child_id"):
        # "Switch" (or any visit to the picker) signs the child out: the next child needs their own PIN.
        await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": True}})
        ctx.child, ctx.locked = None, True
    return await picker_page(request, ctx)


@router.post("/learn/{pid}")
async def enter(request: Request, pid: str, ctx: Ctx = Depends(family_page), pin: str = Form("")):
    p = await own_pupil(ctx, pid)
    until = await pin_lock_until(p["_id"])
    if until:
        return await picker_page(request, ctx, pin_for=p["_id"], status_code=429,
                             error=f"Too many wrong PINs. {p['name']} is locked until {local_hm(until)}.")
    pin = pin.strip()
    if not PIN_RE.match(pin):          # not a guess: nothing is counted
        return await picker_page(request, ctx, pin_for=p["_id"], status_code=400,
                             error=f"{p['name']}'s PIN is 4 numbers. Type all 4, then press Start.")
    if not verify_secret(pin, p["pin"]):
        await db.login_failures.insert_one({"email": f"pin:{p['_id']}", "ts": datetime.datetime.utcnow()})
        until = await pin_lock_until(p["_id"])
        err = (f"Too many wrong PINs. {p['name']} is locked until {local_hm(until)}." if until else
               f"Wrong PIN. {p['name']}'s PIN is 4 numbers — ask a grown-up to check it in Parent.")
        return await picker_page(request, ctx, pin_for=p["_id"], error=err, status_code=429 if until else 400)
    await db.sessions.update_one({"_id": ctx.session["_id"]},
                                 {"$set": {"child_id": p["_id"], "locked": True, "handed": True}})
    return RedirectResponse("/me", 303)


@router.get("/me")
async def me(request: Request, ctx: Ctx = Depends(child_page)):
    b = await progress.board(ctx.family, [ctx.child])
    plan = {a["key"] for a in b[0]["items"]}
    fix = {k: len(v) for k, v in (await progress.open_mistakes(ctx.child)).items() if k in plan}
    return page(request, "me.html", ctx, status=b[0], reward=b[0]["reward"], fix=fix,
                fix_first=next((a["key"] for a in b[0]["items"] if fix.get(a["key"])), None))


def _allowed(ctx: Ctx, activity: str) -> bool:
    return any(a["key"] == activity for a in todays_plan(ctx.child, ctx.family))


@router.get("/me/{activity}")
async def activity_page(request: Request, activity: str, ctx: Ctx = Depends(child_page)):
    if activity not in DRILLS or not _allowed(ctx, activity):
        return RedirectResponse("/me", 303)
    plan = {a["key"]: a for a in todays_plan(ctx.child, ctx.family)}
    return page(request, f"act_{activity}.html", ctx, act=plan[activity])


async def _day(ctx: Ctx, activity: str) -> dict:
    st = (await progress.board(ctx.family, [ctx.child]))[0]
    it = next((i for i in st["items"] if i["key"] == activity), None)
    reward = st["reward"]
    return {"done": it["done"] if it else 0, "target": it["target"] if it else 0, "day_pct": st["pct"],
            "reward": reward.get("text", "") if st["reward_earned"] else ""}


def _switched(ctx: Ctx, payload: dict) -> JSONResponse | None:
    """The page says which child it was opened for; if another child has signed in on this device since
    (another tab, "Switch"), refuse, so one child's page never serves or credits the other."""
    pid = payload.get("pupil")
    if pid is not None and pid != ctx.child["_id"]:
        return JSONResponse({"ok": False, "error": "switched", "name": ctx.child["name"]}, status_code=409)
    return None


@router.post("/api/{activity}/next")
async def api_next(activity: str, payload: dict = Body(default={}), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    if activity not in DRILLS or not _allowed(ctx, activity):
        raise HTTPException(403, "activity not available")
    want_fix = bool(payload.get("fix"))
    open_ = await progress.open_mistakes(ctx.child) if want_fix else {}
    todo = open_.get(activity, [])
    # a mistake whose answer was just shown waits for a gap, so that putting it right is remembering, not copying
    shown = await items.just_shown(ctx.child, activity) if todo and activity != "maths" else set()
    served = await _pending(ctx, activity, want_fix)
    if served:
        q, fixing = served
    else:
        ready = [t for t in todo if t not in shown]
        q = await DRILLS[activity].next_question(ctx.child, focus=ready[0] if ready else None)
        if not q:
            return JSONResponse({"ok": False, "error": "no_question"}, status_code=500)
        fixing = bool(ready)
        await _remember(ctx, activity, q, want_fix, fixing)
    fix = {"fixing": fixing, "fix_left": len(todo), "fix_later": len([t for t in todo if t in shown])} if want_fix else {}
    if want_fix:
        fix.update(await _fix_flow(ctx, activity, open_, fixing))
    return {"ok": True, **q, **fix, "day": await _day(ctx, activity)}


async def _fix_flow(ctx: Ctx, activity: str, open_: dict, fixing: bool) -> dict:
    """"Practise my mistakes" goes through every subject in one go: how many are left in all (fix_total, the
    count on My day), and, once this subject has none ready, the next subject that has (fix_next)."""
    plan = [a["key"] for a in todays_plan(ctx.child, ctx.family)]
    out = {"fix_total": sum(len(open_.get(k, [])) for k in plan), "fix_next": None}
    if not fixing and activity in plan:
        i = plan.index(activity)
        others = [k for k in plan[i + 1:] + plan[:i] if open_.get(k)]
        for k in others:
            if k == "maths" or set(open_[k]) - await items.just_shown(ctx.child, k):
                out["fix_next"] = k
                break
        # all still waiting for a gap: go where they wait, as its own questions make the gap (never ping-pong:
        # a subject with mistakes waiting stays put)
        if not out["fix_next"] and others and not open_.get(activity):
            out["fix_next"] = others[0]
    return out


PENDING_HOURS = 12     # an unanswered question is served again (refresh, Back, Next) for this long


def _served_in(activity: str):
    return (db.maths_lab_q, "pupil") if activity == "maths" else (db.items, "pupil_id")


async def _remember(ctx: Ctx, activity: str, q: dict, want_fix: bool, fixing: bool) -> None:
    coll, _ = _served_in(activity)
    await coll.update_one({"_id": q["token"]}, {"$set": {"served": {
        "q": json.dumps(q, default=str), "fix": want_fix, "fixing": fixing, "year": ctx.child.get("year")}}})


async def _pending(ctx: Ctx, activity: str, want_fix: bool) -> tuple[dict, bool] | None:
    """The question last served to this child here and not answered yet: a refresh or Back gets it again,
    so a hard question cannot be swapped for an easier one."""
    coll, who = _served_in(activity)
    find = {who: ctx.child["_id"], "done": {"$ne": True}, "served.fix": want_fix,
            "served.year": ctx.child.get("year"),
            "created": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(hours=PENDING_HOURS)}}
    if activity != "maths":
        find["activity"] = activity
    doc = await coll.find_one(find, sort=[("created", -1)])
    return (json.loads(doc["served"]["q"]), doc["served"].get("fixing", False)) if doc else None


@router.post("/api/{activity}/check")
async def api_check(activity: str, payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    if activity not in DRILLS or not _allowed(ctx, activity):
        raise HTTPException(403, "activity not available")
    ms = payload.get("ms")
    ms = int(ms) if isinstance(ms, (int, float)) else None
    if activity == "verbs":
        res = await verbs.check(ctx.child, payload.get("token"), payload.get("past", ""), payload.get("pp", ""), ms)
    else:
        res = await DRILLS[activity].check(ctx.child, payload.get("token"), payload.get("value"), ms)
    if res is None:
        return JSONResponse({"ok": False, "error": "expired"}, status_code=409)
    return {"ok": True, **res, "day": await _day(ctx, activity)}


@router.get("/api/spelling/audio/{token}")
async def spelling_audio(token: str, ctx: Ctx = Depends(child_api)):
    it = await items.peek(ctx.child, "spelling", token)
    if not it:
        raise HTTPException(404)
    return FileResponse(AUDIO_DIR / spelling.audio_file(it["answer"]), media_type="audio/mpeg",
                        headers={"Cache-Control": "no-store"})
