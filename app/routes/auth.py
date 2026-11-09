"""Parent accounts: sign up, verify email, sign in and out, reset password."""
import datetime
import re

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from .. import config, mailer
from ..activities import new_family_plan
from ..db import db
from ..deps import client_ip, create_session, end_session, hit, load, over_limit
from ..security import hash_secret, new_code, new_id, new_token, token_key, verify_secret
from ..web import page

router = APIRouter()
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_FAILS = 8
CODE_TRIES = 5                     # wrong guesses for one code
CODE_FAILS_HOUR = 10               # wrong guesses per email per hour, across "Send a new code"
# Mail we send on request: (count, minutes) windows per address, and per client address for all of them.
MAIL_PER_EMAIL = ((3, 10), (5, 60))
MAIL_PER_IP = ((30, 60),)


def _now():
    return datetime.datetime.utcnow()


async def _mail_allowed(request: Request, purpose: str, email: str) -> bool:
    """Throttle mail-sending actions so nobody can flood an inbox; counts this send when it is allowed."""
    keys = ((f"mail:{purpose}:{email}", MAIL_PER_EMAIL), (f"mail:ip:{client_ip(request)}", MAIL_PER_IP))
    for key, windows in keys:
        for n, minutes in windows:
            if await over_limit(key, n, minutes):
                return False
    for key, _ in keys:
        await hit(key)
    return True


async def _send_code(account: dict) -> None:
    code = new_code()
    await db.codes.delete_many({"email": account["email"], "purpose": "verify"})
    await db.codes.insert_one({"email": account["email"], "purpose": "verify", "hash": hash_secret(code),
                               "tries": 0, "expires": _now() + datetime.timedelta(minutes=30)})
    await mailer.send(account["email"], f"Your Quizocracy code: {code}",
                      f"Your verification code is {code}\n\nIt expires in 30 minutes. "
                      f"If you did not sign up to Quizocracy, ignore this email.\n", secret=code)


@router.get("/signup")
async def signup_form(request: Request):
    return page(request, "signup.html", need_invite=bool(config.INVITE_CODE))


@router.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...),
                 family_name: str = Form(""), invite: str = Form(""), consent: str = Form("")):
    email = email.strip().lower()
    err = None
    if config.INVITE_CODE and invite.strip() != config.INVITE_CODE:
        err = "That invitation code is not valid."
    elif not EMAIL_RE.match(email):
        err = "Enter a valid email address."
    elif len(password) < 8:
        err = "Use a password of at least 8 characters."
    elif not consent:
        err = "Please confirm you are a parent or guardian aged 18 or over."
    elif await db.accounts.find_one({"email": email}):
        err = "An account already exists for this email. Sign in instead."
    if err:
        return page(request, "signup.html", need_invite=bool(config.INVITE_CODE), error=err,
                    email=email, family_name=family_name, status_code=400)
    fam = {"_id": new_id("fam"), "name": (family_name.strip() or "My family")[:60], "plan": new_family_plan(),
           "created": _now(), "reward": {"text": "", "threshold": 100}}
    acc = {"_id": new_id("acc"), "email": email, "pw": hash_secret(password), "family_id": fam["_id"],
           "role": "owner", "created": _now(), "verified_at": None}
    await db.families.insert_one(fam)
    await db.accounts.insert_one(acc)
    await hit(f"mail:verify:{email}")              # the first code counts towards the resend limit
    await _send_code(acc)
    resp = RedirectResponse("/verify", 303)
    await create_session(resp, acc)
    return resp


@router.get("/verify")
async def verify_form(request: Request):
    ctx = await load(request)
    if not ctx:
        return RedirectResponse("/login", 303)
    if ctx.account.get("verified_at"):
        return RedirectResponse("/home", 303)
    return page(request, "verify.html", ctx, email=ctx.account["email"])


@router.post("/verify")
async def verify(request: Request, code: str = Form(...)):
    ctx = await load(request)
    if not ctx:
        return RedirectResponse("/login", 303)
    email = ctx.account["email"]
    fails_key = f"verify:{email}"          # outlives each code, so "Send a new code" does not reset the cap
    if await over_limit(fails_key, CODE_FAILS_HOUR, 60):
        return page(request, "verify.html", ctx, email=email, status_code=429,
                    error="Too many wrong codes. Wait an hour, then ask for a new code.")
    rec = await db.codes.find_one({"email": email, "purpose": "verify", "expires": {"$gt": _now()}})
    if rec and rec.get("tries", 0) >= CODE_TRIES:
        return page(request, "verify.html", ctx, email=email, status_code=400,
                    error="That code has had too many wrong tries and no longer works. Ask for a new code below.")
    if not rec or not verify_secret(code.strip(), rec["hash"]):
        if rec:
            await db.codes.update_one({"_id": rec["_id"]}, {"$inc": {"tries": 1}})
        await hit(fails_key)
        return page(request, "verify.html", ctx, email=email,
                    error="That code is not right, or it has expired.", status_code=400)
    await db.codes.delete_many({"email": ctx.account["email"], "purpose": "verify"})
    await db.accounts.update_one({"_id": ctx.account["_id"]}, {"$set": {"verified_at": _now()}})
    return RedirectResponse("/home?welcome=1", 303)


@router.post("/verify/resend")
async def verify_resend(request: Request):
    ctx = await load(request)
    if ctx and not ctx.account.get("verified_at"):
        if not await _mail_allowed(request, "verify", ctx.account["email"]):
            return page(request, "verify.html", ctx, email=ctx.account["email"], status_code=429,
                        error="We have sent several codes already. Check your inbox and spam folder, "
                              "or wait a few minutes before asking for another.")
        await _send_code(ctx.account)
    return RedirectResponse("/verify?sent=1", 303)


@router.get("/login")
async def login_form(request: Request):
    return page(request, "login.html")


@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    email = email.strip().lower()
    since = _now() - datetime.timedelta(minutes=15)
    if await db.login_failures.count_documents({"email": email, "ts": {"$gt": since}}) >= MAX_FAILS:
        return page(request, "login.html", email=email, status_code=429,
                    error="Too many attempts. Wait 15 minutes, or reset your password.")
    acc = await db.accounts.find_one({"email": email})
    if not acc or not verify_secret(password, acc["pw"]):
        await db.login_failures.insert_one({"email": email, "ts": _now()})
        return page(request, "login.html", email=email, error="Email or password is not right.", status_code=400)
    resp = RedirectResponse("/home" if acc.get("verified_at") else "/verify", 303)
    await create_session(resp, acc)
    return resp


@router.post("/logout")
async def logout(request: Request):
    ctx = await load(request)
    if ctx and ctx.locked:
        return RedirectResponse("/parent-unlock", 303)     # a child cannot sign the parent out
    resp = RedirectResponse("/", 303)
    await end_session(request, resp)
    return resp


@router.get("/forgot")
async def forgot_form(request: Request):
    return page(request, "forgot.html")


@router.post("/forgot")
async def forgot(request: Request, email: str = Form(...)):
    email = email.strip().lower()
    acc = await db.accounts.find_one({"email": email})
    # Over the limit, nothing is sent but the page says the same: it must not tell which emails have accounts,
    # and the link sent earlier still works.
    if acc and await _mail_allowed(request, "reset", email):
        tok = new_token()
        await db.codes.delete_many({"email": email, "purpose": "reset"})      # a new link replaces older ones
        await db.codes.insert_one({"email": email, "purpose": "reset", "hash": token_key(tok),
                                   "expires": _now() + datetime.timedelta(hours=1)})
        await mailer.send(email, "Reset your Quizocracy password",
                          f"Use this link within an hour to choose a new password:\n\n"
                          f"{config.PUBLIC_URL}/reset?token={tok}\n\nIf you did not ask for this, ignore this email.\n",
                          secret=tok)
    return page(request, "forgot.html", sent=True)


@router.get("/reset")
async def reset_form(request: Request, token: str = ""):
    rec = await db.codes.find_one({"purpose": "reset", "hash": token_key(token), "expires": {"$gt": _now()}})
    return page(request, "reset.html", token=token, invalid=not rec)


@router.post("/reset")
async def reset(request: Request, token: str = Form(...), password: str = Form(...)):
    rec = await db.codes.find_one({"purpose": "reset", "hash": token_key(token), "expires": {"$gt": _now()}})
    if not rec:
        return page(request, "reset.html", token=token, invalid=True, status_code=400)
    if len(password) < 8:
        return page(request, "reset.html", token=token, error="Use at least 8 characters.", status_code=400)
    acc = await db.accounts.find_one({"email": rec["email"]})
    await db.accounts.update_one({"_id": acc["_id"]}, {"$set": {"pw": hash_secret(password),
                                                                "verified_at": acc.get("verified_at") or _now()}})
    await db.codes.delete_many({"email": rec["email"], "purpose": "reset"})
    await db.sessions.delete_many({"account_id": acc["_id"]})          # sign out everywhere
    await db.login_failures.delete_many({"email": rec["email"]})
    return RedirectResponse("/login?reset=1", 303)
