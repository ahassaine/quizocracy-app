"""SATs practice papers, races, the league, and the Year 1 phonics check practice: the child's pages, and the
parent's leagues page. Included before child.router, so /me/race is not taken for an activity (/me/{activity})."""
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from ..db import db
from ..deps import Ctx, child_api, child_page, full_page, own_pupil, parent_page
from ..drills import phonics_check, sats, spelling
from .. import league
from ..web import page
from .child import AUDIO_DIR, _switched

router = APIRouter()
RACE_ACT = {"title": "Times-tables race", "img": "/static/img/race.png", "target": 0}
LEAGUE_ACT = {"title": "League", "img": "/static/img/league.png", "target": 0}
CHECK_ACT = {"title": "Phonics check practice", "img": "/static/img/phonics.png", "target": 0}


async def _pupils(ctx: Ctx) -> list:
    return [p async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]


# ---- races ----
@router.get("/me/race")
async def race_home(request: Request, ctx: Ctx = Depends(child_page)):
    pupils = await _pupils(ctx)
    year = int(ctx.child.get("year") or 4)
    courses = []
    for k in league.COURSE_ORDER:
        board = await league.race_board(ctx.family, pupils, k, ctx.child)
        mine = next((r for r in board if r["me"]), None)
        courses.append({"key": k, **league.COURSES[k], "board": board[:5], "mine": mine, "n": len(board),
                        "suggested": year >= 2 and k == league.default_course(year)})
    return page(request, "race.html", ctx, act=RACE_ACT, courses=courses, fmt=league.fmt_ms,
                has_league=bool(await league.leagues_of(ctx.family["_id"])))


@router.get("/me/race/{course}")
async def race_page(request: Request, course: str, ctx: Ctx = Depends(child_page)):
    if course not in league.COURSES:
        return RedirectResponse("/me/race", 303)
    board = await league.race_board(ctx.family, await _pupils(ctx), course, ctx.child)
    mine = next((r for r in board if r["me"]), None)
    # the ghosts: the child's own best this week, and up to 3 others, the nearest faster runs first; on the course
    # for a child's own year, the children for whom it is their year's course (an older brother racing the Starter
    # course to beat his sister does not take over her races)
    others = [r for r in board if not r["me"]]
    year_of = {p["_id"]: int(p.get("year") or 4) async for p in db.pupils.find({"_id": {"$in": [r["id"] for r in others]}}, {"year": 1})}
    if course == league.default_course(int(ctx.child.get("year") or 4)):
        others = [r for r in others if league.default_course(year_of.get(r["id"], 4)) == course]
    faster = [r for r in others if not mine or r["total"] < mine["total"]][-2:]
    slower = [r for r in others if mine and r["total"] >= mine["total"]][:3 - len(faster)]
    ghosts = ([mine] if mine else []) + faster + slower
    return page(request, "race_run.html", ctx, act={**RACE_ACT, "title": f"Race: {league.COURSES[course]['title']}"},
                course={"key": course, **league.COURSES[course]}, fmt=league.fmt_ms, mine=mine,
                ghosts=[{"label": "Your best" if g["me"] else g["label"], "pic": g["pic"], "splits": g["splits"],
                         "total": g["total"], "me": g["me"]} for g in ghosts])


@router.post("/api/race/start")
async def api_race_start(payload: dict = Body(default={}), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    res = await league.race_start(ctx.child, str(payload.get("course") or ""))
    if not res:
        raise HTTPException(400, "no such course")
    return {"ok": True, **res}


@router.post("/api/race/finish")
async def api_race_finish(payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    splits, wrong = payload.get("splits"), payload.get("wrong")
    res = await league.race_finish(ctx.child, payload.get("token"), splits if isinstance(splits, list) else [],
                                   wrong if isinstance(wrong, list) else [])
    if res is None:
        return JSONResponse({"ok": False, "error": "expired"}, status_code=409)
    return {"ok": True, **res, "time": league.fmt_ms(res.get("total")), "was": league.fmt_ms(res.get("was"))}


# ---- the league ----
@router.get("/me/league")
async def league_child(request: Request, ctx: Ctx = Depends(child_page)):
    pupils = await _pupils(ctx)
    family_table = await league.table(ctx.family, pupils, ctx.child) if len(pupils) > 1 else []
    tables = []
    if league.in_leagues(ctx.child):
        for lg in await league.leagues_of(ctx.family["_id"]):
            tables.append({"name": lg["name"], "rows": await league.table(ctx.family, pupils, ctx.child, lg)})
    mine = (await league.week_stars(ctx.family, [ctx.child]))[ctx.child["_id"]]
    return page(request, "league.html", ctx, act=LEAGUE_ACT, family_table=family_table, tables=tables, mine=mine,
                nick=await league.nick_of(ctx.child), days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                STAR_DAY=league.STAR_DAY, STAR_EXTRA=league.STAR_EXTRA, STAR_EXTRA_MAX=league.STAR_EXTRA_MAX)


# ---- the parent's leagues page ----
async def _leagues_view(ctx: Ctx) -> dict:
    pupils = await _pupils(ctx)
    out = []
    for lg in await league.leagues_of(ctx.family["_id"]):
        fams = []
        for fid in lg["families"]:
            if fid == ctx.family["_id"]:
                continue
            kids = [p async for p in db.pupils.find({"family_id": fid}).sort("created", 1)]
            # another family is named by its children's nicknames only (never the family's or a child's name)
            nicks = [(await league.nick_of(p))["name"] for p in kids if league.in_leagues(p)]
            fams.append({"id": fid, "label": ", ".join(nicks) or "a family with no children taking part"})
        out.append({"id": lg["_id"], "name": lg["name"], "code": lg["code"], "owner": lg["owner"] == ctx.family["_id"],
                    "families": fams, "rows": await league.table(ctx.family, pupils, None, lg)})
    for p in pupils:
        await league.nick_of(p)
    return {"leagues": out, "pupils": pupils, "family_table": await league.table(ctx.family, pupils),
            "ADJ": league.NICK_ADJ, "ANIMALS": league.NICK_ANIMAL, "MAX": league.LEAGUES_PER_FAMILY,
            "MAX_FAMILIES": league.LEAGUE_MAX_FAMILIES}


JOIN_ERRORS = {"nocode": "No league has that code. Check the 8 letters and numbers with the family who sent it.",
               "already": "Your family is already in that league.",
               "full": f"That league is full: it has {league.LEAGUE_MAX_FAMILIES} families.",
               "many": f"Your family is in {league.LEAGUES_PER_FAMILY} leagues already: leave one first.",
               "out": "The family who made that league has taken your family out of it, so it can't be joined again."}


@router.get("/leagues")
async def leagues_page(request: Request, ctx: Ctx = Depends(parent_page)):
    return page(request, "leagues.html", ctx, **await _leagues_view(ctx), done=request.query_params.get("done", ""))


@router.post("/leagues/new")
async def leagues_new(ctx: Ctx = Depends(full_page)):
    res = await league.create_league(ctx.family)
    return RedirectResponse("/leagues?done=" + ("many" if res == "full" else "made"), 303)


@router.post("/leagues/join")
async def leagues_join(request: Request, ctx: Ctx = Depends(full_page), code: str = Form("")):
    res = await league.join_league(ctx.family, code)
    if isinstance(res, str):
        return page(request, "leagues.html", ctx, **await _leagues_view(ctx), join_error=JOIN_ERRORS[res],
                    code=code[:20], status_code=400)
    return RedirectResponse("/leagues?done=joined", 303)


@router.get("/leagues/join")
async def leagues_join_get():
    return RedirectResponse("/leagues", 303)          # a refresh after a wrong code: back to the page, not an error


@router.post("/leagues/{lid}/code")
async def leagues_new_code(lid: str, ctx: Ctx = Depends(full_page)):
    await league.new_code(lid, ctx.family["_id"])
    return RedirectResponse("/leagues?done=code", 303)


@router.post("/leagues/{lid}/leave")
async def leagues_leave(lid: str, ctx: Ctx = Depends(full_page)):
    await league.leave_league(ctx.family["_id"], lid)
    return RedirectResponse("/leagues?done=left", 303)


@router.post("/leagues/{lid}/remove")
async def leagues_remove(lid: str, ctx: Ctx = Depends(full_page), family: str = Form("")):
    await league.remove_family(lid, ctx.family["_id"], family)
    return RedirectResponse("/leagues?done=removed", 303)


@router.post("/children/{pid}/league")
async def child_league(pid: str, ctx: Ctx = Depends(full_page), on: str = Form(""), adj: str = Form(""),
                       animal: str = Form("")):
    p = await own_pupil(ctx, pid)
    upd: dict = {"league_on": on == "1"}
    nick = league.valid_nick(adj, animal)
    if nick:
        upd["nick"] = nick
    await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    return RedirectResponse("/leagues?done=saved#child-" + p["_id"], 303)


# ---- the Year 1 phonics check practice (a grown-up marks) ----
@router.get("/me/phonics-check")
async def phonics_check_page(request: Request, ctx: Ctx = Depends(child_page)):
    if not phonics_check.open_to(ctx.child):
        return RedirectResponse("/me", 303)
    hist = phonics_check.history(ctx.child)
    return page(request, "phonics_check.html", ctx, act=CHECK_ACT, hist=hist[-5:], standard=phonics_check.STANDARD,
                best=max(hist, key=lambda r: r["score"] / r["of"]) if hist else None)


@router.post("/api/phonics-check/start")
async def api_phonics_check_start(payload: dict = Body(default={}), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    try:
        size = int(payload.get("size") or 20)
    except (TypeError, ValueError):
        size = 20
    res = await phonics_check.start(ctx.child, size)
    if not res:
        raise HTTPException(403, "not available")
    return {"ok": True, **res}


@router.post("/api/phonics-check/finish")
async def api_phonics_check_finish(payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    res = await phonics_check.finish(ctx.child, payload.get("token"), payload.get("marks"))
    if res is None:
        return JSONResponse({"ok": False, "error": "expired"}, status_code=409)
    return {"ok": True, **res}


# SATs practice papers (drills/sats.py): Years 5 and 6, whatever the plan; a paper's answers count for the day only
# in subjects of today's plan.
@router.get("/me/sats")
async def sats_page(request: Request, ctx: Ctx = Depends(child_page)):
    if not sats.open_to(ctx.child):
        return RedirectResponse("/me", 303)
    return page(request, "sats.html", ctx, act={"title": "SATs practice papers", "img": "/static/img/sats.png",
                                                 "target": 0}, papers=sats.cards(ctx.child), sheets=await sats.sheets(ctx.child, 8))


@router.get("/me/sats/sheet/{sid}")
async def sats_sheet_child(request: Request, sid: str, ctx: Ctx = Depends(child_page)):
    sh = await sats.sheet(ctx.child, sid)
    if not sh:
        return RedirectResponse("/me/sats", 303)
    return page(request, "sats_sheet.html", ctx, pupil=ctx.child, sheet=sh, back="/me/sats", back_label="SATs papers")


@router.get("/children/{pid}/sats/{sid}")
async def sats_sheet_parent(request: Request, pid: str, sid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    sh = await sats.sheet(p, sid)
    if not sh:
        raise HTTPException(404, "not found")
    return page(request, "sats_sheet.html", ctx, pupil=p, sheet=sh, back=f"/children/{p['_id']}#sats-papers-scores",
                back_label=f"{p['name']}'s progress")


@router.get("/me/sats/{paper}")
async def sats_paper_page(request: Request, paper: str, ctx: Ctx = Depends(child_page)):
    if not sats.open_to(ctx.child) or paper not in sats.PAPERS:
        return RedirectResponse("/me/sats", 303)
    card = next(c for c in sats.cards(ctx.child) if c["key"] == paper)
    return page(request, "sats_paper.html", ctx, act={"title": sats.PAPERS[paper]["title"], "img": "/static/img/sats.png",
                                                       "target": 0}, paper=card)


@router.post("/api/sats/start")
async def api_sats_start(payload: dict = Body(default={}), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    res = await sats.start(ctx.child, str(payload.get("paper") or ""))
    if not res:
        raise HTTPException(403, "paper not available")
    return {"ok": True, **res}


@router.post("/api/sats/finish")
async def api_sats_finish(payload: dict = Body(...), ctx: Ctx = Depends(child_api)):
    if (refused := _switched(ctx, payload)):
        return refused
    res = await sats.finish(ctx.child, payload.get("token"), payload.get("answers"), payload.get("used"), ctx.family)
    if res is None:
        return JSONResponse({"ok": False, "error": "expired"}, status_code=409)
    return {"ok": True, **res}


@router.get("/api/sats/audio/{token}/{i}")
async def api_sats_audio(token: str, i: int, ctx: Ctx = Depends(child_api)):
    w = await sats.audio_word(ctx.child, token, i)
    if not w:
        raise HTTPException(404)
    return FileResponse(AUDIO_DIR / spelling.audio_file(w), media_type="audio/mpeg", headers={"Cache-Control": "no-store"})
