"""The child's side: pick yourself, enter your PIN, see your day, do the activities."""
import datetime

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from ..activities import todays_plan
from ..config import BASE_DIR
from ..db import db
from ..deps import Ctx, child_api, child_page, family_page, own_pupil
from ..drills import maths, numbers, spelling, tables, verbs
from .. import items, progress
from ..security import verify_secret
from ..web import page

router = APIRouter()
DRILLS = {"maths": maths, "tables": tables, "spelling": spelling, "numbers": numbers, "verbs": verbs}
AUDIO_DIR = BASE_DIR / "static" / "audio" / "words"


@router.get("/learn")
async def picker(request: Request, ctx: Ctx = Depends(family_page)):
    pupils = [p async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]
    return page(request, "learn.html", ctx, pupils=pupils)


@router.post("/learn/{pid}")
async def enter(request: Request, pid: str, ctx: Ctx = Depends(family_page), pin: str = Form(...)):
    p = await own_pupil(ctx, pid)
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    key = f"pin:{p['_id']}"
    if await db.login_failures.count_documents({"email": key, "ts": {"$gt": since}}) >= 6:
        return page(request, "learn.html", ctx, pupils=[p], pin_for=p["_id"], status_code=429,
                    error="Too many wrong PINs. Ask a parent.")
    if not verify_secret(pin.strip(), p["pin"]):
        await db.login_failures.insert_one({"email": key, "ts": datetime.datetime.utcnow()})
        pupils = [x async for x in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]
        return page(request, "learn.html", ctx, pupils=pupils, pin_for=p["_id"], error="Wrong PIN. Try again.",
                    status_code=400)
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": p["_id"]}})
    return RedirectResponse("/me", 303)


@router.get("/me")
async def me(request: Request, ctx: Ctx = Depends(child_page)):
    b = await progress.board(ctx.family, [ctx.child])
    return page(request, "me.html", ctx, status=b[0], reward=ctx.family.get("reward") or {})


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
    reward = ctx.family.get("reward") or {}
    return {"done": it["done"] if it else 0, "target": it["target"] if it else 0, "day_pct": st["pct"],
            "reward": reward.get("text", "") if st["reward_earned"] else ""}


@router.post("/api/{activity}/next")
async def api_next(activity: str, ctx: Ctx = Depends(child_api)):
    if activity not in DRILLS or not _allowed(ctx, activity):
        raise HTTPException(403, "activity not available")
    q = await DRILLS[activity].next_question(ctx.child)
    if not q:
        return JSONResponse({"ok": False, "error": "no_question"}, status_code=500)
    return {"ok": True, **q, "day": await _day(ctx, activity)}


@router.post("/api/{activity}/check")
async def api_check(activity: str, payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
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
