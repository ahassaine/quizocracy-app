"""Who is asking. A session belongs to one family; it is in parent mode or locked to one child."""
import datetime
from dataclasses import dataclass

from fastapi import HTTPException, Request

from . import config
from .db import db
from .security import new_token, token_key

COOKIE = "qz_s"


class Redirect(Exception):
    def __init__(self, url: str):
        self.url = url


@dataclass
class Ctx:
    session: dict
    account: dict
    family: dict
    child: dict | None = None


async def create_session(response, account: dict) -> None:
    tok = new_token()
    now = datetime.datetime.utcnow()
    await db.sessions.insert_one({"_id": token_key(tok), "account_id": account["_id"], "family_id": account["family_id"],
                                  "child_id": None, "created": now, "parent_ok_at": now,
                                  "expires": now + datetime.timedelta(days=config.SESSION_DAYS)})
    response.set_cookie(COOKIE, tok, max_age=config.SESSION_DAYS * 86400, httponly=True,
                        secure=config.COOKIE_SECURE, samesite="lax", path="/")


async def end_session(request: Request, response) -> None:
    tok = request.cookies.get(COOKIE)
    if tok:
        await db.sessions.delete_one({"_id": token_key(tok)})
    response.delete_cookie(COOKIE, path="/")


async def load(request: Request) -> Ctx | None:
    tok = request.cookies.get(COOKIE)
    if not tok:
        return None
    s = await db.sessions.find_one({"_id": token_key(tok), "expires": {"$gt": datetime.datetime.utcnow()}})
    if not s:
        return None
    acc = await db.accounts.find_one({"_id": s["account_id"]})
    fam = await db.families.find_one({"_id": s["family_id"]})
    if not acc or not fam:
        return None
    child = None
    if s.get("child_id"):
        child = await db.pupils.find_one({"_id": s["child_id"], "family_id": fam["_id"]})
    return Ctx(s, acc, fam, child)


async def family_page(request: Request) -> Ctx:
    ctx = await load(request)
    if not ctx:
        raise Redirect("/login")
    if not ctx.account.get("verified_at"):
        raise Redirect("/verify")
    return ctx


async def parent_page(request: Request) -> Ctx:
    ctx = await family_page(request)
    if ctx.child:
        raise Redirect("/parent-unlock")
    return ctx


async def child_page(request: Request) -> Ctx:
    ctx = await family_page(request)
    if not ctx.child:
        raise Redirect("/learn")
    return ctx


async def child_api(request: Request) -> Ctx:
    ctx = await load(request)
    if not ctx or not ctx.child or not ctx.account.get("verified_at"):
        raise HTTPException(401, "not signed in as a child")
    return ctx


async def own_pupil(ctx: Ctx, pupil_id: str) -> dict:
    """A pupil of this family, or 404. Never trust an id from the URL without this."""
    p = await db.pupils.find_one({"_id": str(pupil_id), "family_id": ctx.family["_id"]})
    if not p:
        raise HTTPException(404, "not found")
    return p
