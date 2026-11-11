"""Who is asking. A session belongs to one family; it is in parent mode or locked (child mode).
A locked session either has a child signed in or is waiting on "Who's learning?"; only the parent's
password brings it back to parent mode."""
import datetime
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from fastapi import HTTPException, Request

from . import config, levels
from .db import db
from .security import new_token, token_key, verify_secret

COOKIE = "qz_s"
# Idle limits. Parent mode on a device a child has used (a PIN was typed or the parent unlocked it) locks itself;
# a parent's own sign-in, never handed over, does not. A child left signed in goes back to "Who's learning?".
PARENT_IDLE = datetime.timedelta(minutes=5)
# Ten minutes for a child: on a shared tablet a sibling must not carry on in their account. (The rule is for a child
# with a PIN or with siblings; every child has a PIN, so it is every child. ui.js goes back to the picker too.)
CHILD_IDLE = datetime.timedelta(minutes=10)
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

    @property
    def role(self) -> str:
        """owner (signed the family up), parent (invited, the same rights) or carer (minds the children)."""
        return self.account.get("role") or "owner"

    @property
    def full(self) -> bool:
        """Full rights: manage children, the account, the other adults and the family's data. A carer has not."""
        return self.role in FULL_ROLES


# The adults of a family. Each has their own login; the PIN, lock and parent-mode rules are the same for all.
FULL_ROLES = ("owner", "parent")
ROLE_TITLES = {"owner": "Parent (account owner)", "parent": "Parent", "carer": "Carer"}


def weekly_on(account: dict) -> bool:
    """Does this adult get the Sunday summary? On for parents unless turned off; a carer turns it on."""
    v = account.get("weekly_email")
    return (account.get("role") or "owner") in FULL_ROLES if v is None else bool(v)


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
        child = await levels.fix(await db.pupils.find_one({"_id": s["child_id"], "family_id": fam["_id"]}))
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
    if not rows:
        return None
    # The family activity log notes each lock once, whoever sees it first (the child's next try, Home, the picker).
    key = f"pinlock:{pupil_id}:{rows[0]['ts'].isoformat()}"
    if not await db.family_log.find_one({"_id": key}, {"_id": 1}):
        p = await db.pupils.find_one({"_id": pupil_id}, {"name": 1, "family_id": 1})
        if p:
            await log_event(p["family_id"], "pin_lock", f"{p['name']} was locked out after {PIN_FAILS} wrong PINs",
                            key=key, ts=rows[0]["ts"], pupil_id=pupil_id)
    return rows[0]["ts"] + PIN_LOCK


async def pin_locks(pupils: list) -> dict:
    """{pupil id: "5 more minutes"} for each child whose tile is locked: how long is left, never a clock time (a
    device on another clock, or a grown-up in a hurry, would read a time wrongly)."""
    out = {}
    for p in pupils:
        until = await pin_lock_until(p["_id"])
        if until:
            out[p["_id"]] = minutes_left(until)
    return out


def minutes_left(until: datetime.datetime) -> str:
    """"5 more minutes", "1 more minute": from now (UTC) to `until`, rounded up."""
    n = max(1, -(-int((until - datetime.datetime.utcnow()).total_seconds()) // 60))
    return f"{n} more minute{'' if n == 1 else 's'}"


async def clear_pin_lock(pupil_id: str) -> None:
    await db.login_failures.delete_many({"email": f"pin:{pupil_id}"})


def local_time(utc: datetime.datetime) -> datetime.datetime:
    return utc.replace(tzinfo=datetime.timezone.utc).astimezone(ZoneInfo(config.TIMEZONE))


def local_hm(utc: datetime.datetime) -> str:
    return local_time(utc).strftime("%H:%M")


# ---- The family activity log: what one grown-up did that the others should be able to see (Home) ----

def adult_name(account: dict) -> str:
    """How the other grown-ups see this adult: the name they gave in Settings, else their email."""
    return (account.get("name") or "").strip() or account.get("email", "")


async def log_event(family_id: str, kind: str, text: str, key: str | None = None, ts: datetime.datetime | None = None,
                    **extra) -> None:
    """One line in the family's activity log. `key` makes it once only (a lock seen by several pages)."""
    row = {"family_id": family_id, "kind": kind, "text": text[:200], "ts": ts or datetime.datetime.utcnow(), **extra}
    if key:
        await db.family_log.update_one({"_id": key}, {"$setOnInsert": row}, upsert=True)
    else:
        await db.family_log.insert_one(row)


async def family_events(family_id: str, n: int = 8) -> list:
    """The latest lines of the family's log, newest first: [{"text", "when"}] ("Today 13:04", "9 Nov 18:30")."""
    today = local_time(datetime.datetime.utcnow()).date()
    out = []
    async for r in db.family_log.find({"family_id": family_id}).sort("ts", -1).limit(n):
        t = local_time(r["ts"])
        day = "Today" if t.date() == today else "Yesterday" if (today - t.date()).days == 1 else f"{t.day} {t:%b}"
        out.append({"text": r["text"], "when": f"{day} {t:%H:%M}", "kind": r.get("kind", "")})
    return out


# A browser that signed in before carries this cookie; a sign-in without it is a new device (the owner of the login
# gets a one-line email). Only a hash of it is kept on the account, with the last DEVICES_KEPT.
DEVICE_COOKIE, DEVICES_KEPT = "qz_d", 20


async def note_device(request: Request, response, account: dict, quiet: bool = False) -> bool:
    """Remember this browser for this adult; True if it had never signed in to this login before. An account from
    before devices were remembered (no list yet) treats its first sign-in as known, and so does `quiet` (sign-up)."""
    tok = request.cookies.get(DEVICE_COOKIE) or new_token()
    key = token_key(tok)
    known = account.get("devices")
    new = known is not None and key not in known and not quiet
    if known is None or key not in known:
        await db.accounts.update_one({"_id": account["_id"]}, {"$push": {"devices": {"$each": [key], "$slice": -DEVICES_KEPT}}})
    response.set_cookie(DEVICE_COOKIE, tok, max_age=400 * 86400, httponly=True, secure=config.COOKIE_SECURE,
                        samesite="lax", path="/")
    return new


def device_text(ua: str) -> str:
    """"Chrome on Android" from a user agent, by its product tokens only; "a browser" when unsure."""
    ua = ua or ""
    os_ = next((n for t, n in (("iPhone", "iPhone"), ("iPad", "iPad"), ("Android", "Android"), ("Windows", "Windows"),
                                ("Mac OS X", "Mac"), ("CrOS", "Chromebook"), ("Linux", "Linux")) if t in ua), "")
    br = next((n for t, n in (("Edg/", "Edge"), ("OPR/", "Opera"), ("Firefox/", "Firefox"), ("FxiOS", "Firefox"),
                               ("CriOS", "Chrome"), ("Chrome/", "Chrome"), ("Safari/", "Safari")) if t in ua), "")
    return f"{br or 'a browser'} on {os_}" if os_ else (br or "a browser")


async def family_page(request: Request) -> Ctx:
    ctx = await load(request)
    if not ctx:
        # a child opening "Who's learning?" or My day on a device not signed in: the sign-in page says so to them,
        # and brings the family back to "Who's learning?" once a grown-up has signed in
        kid = request.url.path == "/learn" or request.url.path == "/me" or request.url.path.startswith("/me/")
        raise Redirect("/login?kid=1" if kid else "/login")
    if not ctx.account.get("verified_at"):
        raise Redirect("/verify")
    return ctx


async def parent_page(request: Request) -> Ctx:
    ctx = await family_page(request)
    if ctx.locked:
        raise Redirect("/parent-unlock")
    return ctx


async def full_page(request: Request) -> Ctx:
    """Parent mode for an adult with full rights; a carer gets a plain "ask a parent" page."""
    ctx = await parent_page(request)
    if not ctx.full:
        raise Redirect("/not-allowed")
    return ctx


async def family_adult(ctx: Ctx, password: str) -> dict | None:
    """The adult of this family whose password this is (the signed-in one tried first), or None."""
    if verify_secret(password, ctx.account["pw"]):
        return ctx.account
    async for a in db.accounts.find({"family_id": ctx.family["_id"], "_id": {"$ne": ctx.account["_id"]},
                                     "verified_at": {"$ne": None}}):
        if verify_secret(password, a["pw"]):
            return a
    return None


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
    p = await levels.fix(await db.pupils.find_one({"_id": str(pupil_id), "family_id": ctx.family["_id"]}))
    if not p:
        raise HTTPException(404, "not found")
    return p
