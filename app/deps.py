"""Who is asking. A session belongs to one family; it is in parent mode or locked (child mode).
A locked session either has a child signed in or is waiting on "Who's learning?"; only the parent's
password brings it back to parent mode."""
import datetime
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from fastapi import HTTPException, Request

from . import config
from .db import db
from .security import new_token, token_key

COOKIE = "qz_s"
# Idle limits. Parent mode on a device a child has used (a PIN was typed or the parent unlocked it) locks itself;
# a parent's own sign-in, never handed over, does not. A child left signed in goes back to "Who's learning?".
PARENT_IDLE = datetime.timedelta(minutes=5)
CHILD_IDLE = datetime.timedelta(minutes=60)
SEEN_EVERY = datetime.timedelta(seconds=20)         # how stale `seen_at` may get before a request rewrites it
# Wrong PINs: this many in PIN_LOCK lock that child's tile for PIN_LOCK (a 4-digit family PIN, guessed by siblings).
PIN_FAILS, PIN_LOCK = 6, datetime.timedelta(minutes=5)


class Redirect(Exception):
    def __init__(self, url: str):
        self.url = url


@dataclass
class Ctx:
    session: dict
    account: dict
    family: dict
    child: dict | None = None
    locked: bool = False            # child mode: a child is signed in, or the device was handed over


def client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


async def over_limit(key: str, limit: int, minutes: int) -> bool:
    """True once `key` has `limit` hits in the last `minutes` (at most 60: login_failures rows expire after an hour)."""
    since = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes)
    return await db.login_failures.count_documents({"email": key, "ts": {"$gt": since}}) >= limit


async def hit(key: str) -> None:
    await db.login_failures.insert_one({"email": key, "ts": datetime.datetime.utcnow()})


async def create_session(response, account: dict) -> None:
    tok = new_token()
    now = datetime.datetime.utcnow()
    await db.sessions.insert_one({"_id": token_key(tok), "account_id": account["_id"], "family_id": account["family_id"],
                                  "child_id": None, "created": now, "parent_ok_at": now, "seen_at": now,
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
    await _idle(s)
    acc = await db.accounts.find_one({"_id": s["account_id"]})
    fam = await db.families.find_one({"_id": s["family_id"]})
    if not acc or not fam:
        return None
    child = None
    if s.get("child_id"):
        child = await db.pupils.find_one({"_id": s["child_id"], "family_id": fam["_id"]})
    # A child id whose child has gone still counts as locked: losing the child never opens the parent area.
    return Ctx(s, acc, fam, child, locked=bool(s.get("locked") or s.get("child_id")))


async def _idle(s: dict) -> None:
    """Apply the idle limits to session `s` (in place) and note this request as its last use."""
    now = datetime.datetime.utcnow()
    idle = now - (s.get("seen_at") or s.get("parent_ok_at") or s.get("created") or now)
    upd = {}
    if s.get("child_id") and idle > CHILD_IDLE:
        upd = {"child_id": None, "locked": True}
    elif s.get("handed") and not s.get("locked") and not s.get("child_id") and idle > PARENT_IDLE:
        upd = {"locked": True, "timed_out": True}
    if upd or idle > SEEN_EVERY:
        upd["seen_at"] = now
        await db.sessions.update_one({"_id": s["_id"]}, {"$set": upd})
        s.update(upd)


async def pin_lock_until(pupil_id: str) -> datetime.datetime | None:
    """When a child's tile opens again after too many wrong PINs (UTC), or None when it is open."""
    since = datetime.datetime.utcnow() - PIN_LOCK
    rows = await db.login_failures.find({"email": f"pin:{pupil_id}", "ts": {"$gt": since}}) \
        .sort("ts", -1).skip(PIN_FAILS - 1).limit(1).to_list(1)
    return rows[0]["ts"] + PIN_LOCK if rows else None


async def pin_locks(pupils: list) -> dict:
    """{pupil id: "19:42"} for each child whose tile is locked, in local time."""
    out = {}
    for p in pupils:
        until = await pin_lock_until(p["_id"])
        if until:
            out[p["_id"]] = local_hm(until)
    return out


async def clear_pin_lock(pupil_id: str) -> None:
    await db.login_failures.delete_many({"email": f"pin:{pupil_id}"})


def local_time(utc: datetime.datetime) -> datetime.datetime:
    return utc.replace(tzinfo=datetime.timezone.utc).astimezone(ZoneInfo(config.TIMEZONE))


def local_hm(utc: datetime.datetime) -> str:
    return local_time(utc).strftime("%H:%M")


async def family_page(request: Request) -> Ctx:
    ctx = await load(request)
    if not ctx:
        raise Redirect("/login")
    if not ctx.account.get("verified_at"):
        raise Redirect("/verify")
    return ctx


async def parent_page(request: Request) -> Ctx:
    ctx = await family_page(request)
    if ctx.locked:
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
