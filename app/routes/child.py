"""The child's side: pick yourself, enter your PIN, see your day, do the activities."""
import datetime
import json
import re

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from ..activities import ACTIVITIES, todays_plan
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
    open_ = {k: v for k, v in (await progress.open_mistakes(ctx.child)).items() if k in plan}
    fix = {k: len(v) for k, v in open_.items()}
    # "Practise my mistakes" opens where a mistake is ready now, not on one still waiting for its gap
    ready = [a["key"] for a in b[0]["items"] if fix.get(a["key"])
             and set(open_[a["key"]]) - set(await items.waits(ctx.child, a["key"]))]
    tabs = next((a for a in b[0]["items"] if a["key"] == "tables"), None)
    return page(request, "me.html", ctx, status=b[0], reward=b[0]["reward"], fix=fix,
                fix_first=(ready or [a["key"] for a in b[0]["items"] if fix.get(a["key"])] or [None])[0],
                check_card=tabs if tabs and ctx.child.get("year") in progress.CHECK_YEARS else None,
                checks=tables.mtc_history(ctx.child))


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
    fx = await _fix_state(ctx, activity, bool(payload.get("check"))) if want_fix else None
    served = await _pending(ctx, activity, want_fix)
    if served:
        q, fixing = served
    else:
        # a mistake ready to put right; else (after the Year 4 check) the first look at a fact missed in it; else,
        # while mistakes wait for their gap, practice on the same tables or skills (near)
        focus = (fx["ready"] or fx["first"] or [None])[0] if fx else None
        near = fx["waiting"] if fx and not focus and activity in NEAR else None
        q = await DRILLS[activity].next_question(ctx.child, focus=focus, **({"near": near} if near else {}))
        if not q:
            return JSONResponse({"ok": False, "error": "no_question"}, status_code=500)
        fixing = bool(fx and focus in fx["ready"]) and not q.pop("no_like", False)
        await _remember(ctx, activity, q, want_fix, fixing)
    fix = {}
    if want_fix:
        fix = {"fixing": fixing, "fix_left": len(fx["todo"]), "fix_later": len(fx["waiting"]), "fix_wait": fx["wait"]}
        fix.update(await _fix_flow(ctx, activity, fx, fixing))
    return {"ok": True, **q, **fix, "day": await _day(ctx, activity)}


NEAR = ("tables", "grammar", "science")      # drills that can fill a wait with questions like the waiting ones


async def _fix_state(ctx: Ctx, activity: str, from_check: bool) -> dict:
    """Where "Practise my mistakes" stands in this activity: open (every activity's mistakes), todo (this
    activity's), ready (to put right now), waiting (shown too recently: they come back after a gap, so putting
    them right is remembering, not copying; wait: about how many seconds), and first: after the Year 4 check
    ("Practise the ones I missed", from_check), only the facts missed in it, each looked at once straight
    away, then put right after the gap."""
    open_ = await progress.open_mistakes(ctx.child)
    todo, first, check = open_.get(activity, []), [], None
    if from_check and activity == "tables" and (ctx.child.get("mtc") or [{}])[-1].get("facts") is not None:
        check = ctx.child["mtc"][-1]
        todo = [f for f in check["facts"] if f in todo]
        looked = {r["detail"] async for r in db.attempts.find(
            {"pupil_id": ctx.child["_id"], "activity": "tables", "detail": {"$in": todo},
             "ts": {"$gt": check.get("done_at") or datetime.datetime.utcnow()}}, {"detail": 1})}
        first = [f for f in todo if f not in looked]
    waits = await items.waits(ctx.child, activity) if todo else {}
    last = await items.last_detail(ctx.child, activity) if todo and activity != "maths" else None
    ready = [t for t in todo if t not in waits and t != last and t not in first]
    waiting = [t for t in todo if t not in ready and t not in first]
    return {"open": open_, "todo": todo, "ready": ready, "first": first, "waiting": waiting, "check": bool(check),
            "wait": min([waits.get(t, 0) for t in waiting], default=0)}


def _wait_text(n: int, secs: int, activity: str, check: bool) -> str:
    """"Your 3 mistakes come back in about 2 minutes. Until then: more of the same tables." """
    what = (("The fact you missed comes back" if n == 1 else f"The {n} facts you missed come back") if check else
            ("Your mistake comes back" if n == 1 else f"Your {n} mistakes come back"))
    mins = -(-secs // 60)
    when = (f"in about {mins} minute{'s' if mins > 1 else ''}" if secs >= 45 else
            "in less than a minute" if secs > 0 else "after a few more questions")
    fill = {"tables": "more of the same tables", "grammar": "more on the same skills",
            "science": "more on the same skills"}.get(activity, "other questions")
    it = "it" if n == 1 else "them"
    return f"{what} {when}, so you remember {it} rather than copy {it}. Until then: {fill}."


async def _fix_flow(ctx: Ctx, activity: str, fx: dict, fixing: bool) -> dict:
    """"Practise my mistakes" goes through every subject in one go: how many are left in all (fix_total, the
    count on My day), once this subject has none ready, the next subject that has (fix_next), and the line the
    child reads (fix_msg; "" when every mistake is done, then fix_done). After the Year 4 check it stays on the
    facts missed in that check."""
    plan = [a["key"] for a in todays_plan(ctx.child, ctx.family)]
    open_ = fx["open"]
    out = {"fix_total": len(fx["todo"]) if fx["check"] else sum(len(open_.get(k, [])) for k in plan),
           "fix_next": None, "fix_title": ACTIVITIES[activity]["title"],
           "fix_done": "All the facts you missed in the check are put right. Well done!" if fx["check"] else ""}
    if not fixing and activity in plan and not fx["check"]:
        i = plan.index(activity)
        others = [k for k in plan[i + 1:] + plan[:i] if open_.get(k)]
        for k in others:
            if set(open_[k]) - set(await items.waits(ctx.child, k)):
                out["fix_next"] = k
                break
        # all still waiting for a gap: go where they wait, as its own questions make the gap (never ping-pong:
        # a subject with mistakes waiting stays put)
        if not out["fix_next"] and others and not open_.get(activity):
            out["fix_next"] = others[0]
    total = out["fix_total"]
    if fixing:
        out["fix_msg"] = f"Putting a mistake right · {total} left"
    elif fx["first"] or (fx["check"] and not fx["waiting"] and fx["todo"]):
        out["fix_msg"] = f"A fact you missed in the check · {total} to put right"
    elif fx["waiting"]:
        out["fix_msg"] = _wait_text(len(fx["waiting"]), fx["wait"], activity, fx["check"])
    else:
        out["fix_msg"] = f"Your other mistakes come back a little later · {total} waiting" if total else ""
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


# Practice for the Year 4 Multiplication Tables Check (tables.mtc_*): open to every child, whatever the plan; it
# counts towards the day only when the plan has times tables.
@router.get("/me/tables/year4-check")
async def mtc_page(request: Request, ctx: Ctx = Depends(child_page)):
    hist = tables.mtc_history(ctx.child)
    return page(request, "tables_check.html", ctx, act=ACTIVITIES["tables"], practice=_allowed(ctx, "tables"),
                last=[r["score"] for r in hist[-3:]], best=max((r["score"] for r in hist), default=None))


@router.post("/api/mtc/start")
async def api_mtc_start(payload: dict = Body(default={}), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    return {"ok": True, **await tables.mtc_start(ctx.child)}


@router.post("/api/mtc/finish")
async def api_mtc_finish(payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    answers = payload.get("answers")
    res = await tables.mtc_finish(ctx.child, payload.get("token"), answers if isinstance(answers, list) else [],
                                  _allowed(ctx, "tables"))
    if res is None:
        return JSONResponse({"ok": False, "error": "expired"}, status_code=409)
    return {"ok": True, **res, "day": await _day(ctx, "tables") if res["counted"] else None}


READING = ("big", "dys", "space", "calm", "contrast")      # the "Aa" settings (_a11y.html); a parent sets them too


@router.post("/api/reading")
async def api_reading(payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    """The signed-in child's reading settings, kept with the child so they follow them to every device."""
    if (refused := _switched(ctx, payload)):
        return refused
    reading = {k: payload.get(k) is True for k in READING}
    await db.pupils.update_one({"_id": ctx.child["_id"]}, {"$set": {"reading": reading}})
    return {"ok": True, "reading": reading}


# "Something wrong with this question?": the question exactly as it was served, kept for the team board
# (/team/<member>/reports). The child's own family sees them on the progress page; no other family ever does.
REPORT_REASONS = {"wrong": "The answer is wrong", "unreadable": "I can't read or see it",
                  "nonsense": "The question doesn't make sense", "other": "Something else"}
REPORTS_PER_DAY = 10


@router.post("/api/report")
async def api_report(request: Request, payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    activity, reason = str(payload.get("activity") or ""), str(payload.get("reason") or "")
    if activity not in DRILLS or reason not in REPORT_REASONS:
        raise HTTPException(400, "bad report")
    day = progress.today()
    if await db.reports.count_documents({"pupil_id": ctx.child["_id"], "day": day}) >= REPORTS_PER_DAY:
        return JSONResponse({"ok": False, "error": "limit"}, status_code=429)
    coll, who = _served_in(activity)
    token = str(payload.get("token") or "")
    doc = await coll.find_one({"_id": token, who: ctx.child["_id"]}) if token else None
    served = expected = skill = None
    if doc:
        served = json.loads(doc["served"]["q"]) if (doc.get("served") or {}).get("q") else \
            {k: doc.get(k) for k in ("prompt", "meta") if doc.get(k) is not None}
        if activity == "maths":
            expected, skill = doc.get("display") or doc.get("answer"), doc.get("skill")
        else:
            m = doc.get("meta") or {}
            expected, skill = doc.get("answer"), m.get("skill") or m.get("fact") or m.get("base")
    dev = payload.get("device") if isinstance(payload.get("device"), dict) else {}
    answer = payload.get("answer")          # what the page last sent to Check ({value} or {past, pp}), if anything
    if isinstance(answer, dict) and set(answer) == {"value"}:
        answer = answer["value"]
    await db.reports.insert_one({
        "family_id": ctx.family["_id"], "pupil_id": ctx.child["_id"], "year": ctx.child.get("year"),
        "activity": activity, "skill": skill, "reason": reason, "note": str(payload.get("note") or "").strip()[:500],
        "token": token, "served": served, "expected": expected,
        "answer": (answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False))[:300]
                  if answer is not None else None,
        "device": {k: int(dev[k]) for k in ("w", "h") if isinstance(dev.get(k), (int, float))}
                  | {"touch": bool(dev.get("touch")), "ua": request.headers.get("user-agent", "")[:200]},
        "day": day, "ts": datetime.datetime.utcnow(), "status": "open"})
    return {"ok": True}
