"""Parent accounts: sign up, verify email, sign in and out, reset password; the other adults of a family
(invitations), changing the account email, and the weekly summary's on/off switch."""
import datetime
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from pymongo.errors import DuplicateKeyError

from .. import config, mailer
from ..activities import new_family_plan, plan_of
from ..db import db
from ..deps import (FULL_ROLES, ROLE_TITLES, Ctx, adult_name, client_ip, create_session, device_text, end_session,
                    full_page, hit, load, local_time, log_event, note_device, over_limit, parent_page, weekly_on)
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


def _code(s: str) -> str:
    """An invitation code as compared: any case, spaces ignored."""
    return re.sub(r"\s+", "", s or "").upper()


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
                      f"Your code is {code}\n\nType it in Quizocracy within 30 minutes.\n\n"
                      f"Didn't sign up to Quizocracy? Then ignore this email.\n", secret=code)


@router.get("/signup")
async def signup_form(request: Request):
    return page(request, "signup.html", need_invite=bool(config.INVITE_CODE))


@router.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...),
                 family_name: str = Form(""), invite: str = Form(""), consent: str = Form("")):
    email = email.strip().lower()
    err = None
    if config.INVITE_CODE and _code(invite) != _code(config.INVITE_CODE):
        err = ("That invitation code is not right. Check it against your invitation (small or capital letters both work)."
               if invite.strip() else "Sign-up needs the invitation code from your invitation email.")
        err += " No code? Join the waiting list below."
    elif not EMAIL_RE.match(email):
        err = "Enter a valid email address."
    elif len(password) < 8:
        err = "Use a password of 8 characters or more."
    elif not consent:
        err = "Please confirm you are a parent or guardian aged 18 or over."
    elif await db.accounts.find_one({"email": email}):
        err = "An account already exists for this email. Sign in instead."
    if err:
        # Everything typed comes back, so one slip never means typing the code and password again.
        return page(request, "signup.html", need_invite=bool(config.INVITE_CODE), error=err, email=email,
                    password=password, family_name=family_name, invite=invite, consent=consent, status_code=400)
    fam = {"_id": new_id("fam"), "name": (family_name.strip() or "My family")[:60], "plan": new_family_plan(),
           "created": _now(), "reward": {"text": "", "threshold": 100}}
    acc = {"_id": new_id("acc"), "email": email, "pw": hash_secret(password), "family_id": fam["_id"],
           "role": "owner", "created": _now(), "verified_at": None, "report_emails": True}
    await db.families.insert_one(fam)
    await db.accounts.insert_one(acc)
    await db.waitlist.delete_one({"_id": email})   # on the waiting list before: not kept once the family is in
    await hit(f"mail:verify:{email}")              # the first code counts towards the resend limit
    await _send_code(acc)
    resp = RedirectResponse("/verify", 303)
    await create_session(resp, acc)
    await note_device(request, resp, acc, quiet=True)
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
        # which one is wrong is not said (that would tell a stranger which emails have an account); the email typed
        # is shown big, as a typo in it is the common mistake
        return page(request, "login.html", email=email, error="Email or password is not right.", check_email=True,
                    status_code=400)
    resp = RedirectResponse("/home" if acc.get("verified_at") else "/verify", 303)
    await create_session(resp, acc)
    if await note_device(request, resp, acc) and acc.get("verified_at"):
        what = device_text(request.headers.get("user-agent", ""))
        await log_event(acc["family_id"], "device", f"{adult_name(acc)} signed in on a new device ({what})")
        await mailer.send(email, "New sign-in to your Quizocracy account",
                          f"Someone signed in to your Quizocracy account ({email}) on a new device ({what}) on "
                          f"{local_time(_now()):%d %B %Y at %H:%M}.\n\n"
                          f"If it was you, there is nothing to do.\n\nIf this wasn't you, choose a new password now at "
                          f"{config.PUBLIC_URL}/forgot (this signs out every device). Then write to us at "
                          f"{config.SUPPORT_EMAIL}.\n")
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
                          f"Open this link within 1 hour to choose a new password:\n\n"
                          f"{config.PUBLIC_URL}/reset?token={tok}\n\nDidn't ask for this? Then ignore this email. "
                          f"Your password stays the same.\n",
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
        return page(request, "reset.html", token=token, error="Use 8 characters or more.", status_code=400)
    acc = await db.accounts.find_one({"email": rec["email"]})
    await db.accounts.update_one({"_id": acc["_id"]}, {"$set": {"pw": hash_secret(password),
                                                                "verified_at": acc.get("verified_at") or _now()}})
    await db.codes.delete_many({"email": rec["email"], "purpose": "reset"})
    await db.sessions.delete_many({"account_id": acc["_id"]})          # sign out everywhere
    await db.login_failures.delete_many({"email": rec["email"]})
    # Tell the account: anyone with the inbox (or a minder) can reset, and the other adults need to know.
    await mailer.send(rec["email"], "Your Quizocracy password was changed",
                      f"The password for your Quizocracy account ({rec['email']}) was changed on "
                      f"{local_time(_now()):%d %B %Y at %H:%M}. Every device was signed out. "
                      f"Sign in again with the new password.\n\n"
                      f"Didn't change it? Choose a new password now at {config.PUBLIC_URL}/forgot "
                      f"and write to us at {config.SUPPORT_EMAIL}.\n")
    return RedirectResponse("/login?reset=1", 303)


# ---- The other adults of a family: a co-parent, or a carer such as a grandparent minding the children ----

ADULTS_MAX = 6                     # adults on one family, open invitations included
INVITE_DAYS = 7
ROLE_CAN = {
    "parent": "do everything they can do: add and change children, see their progress, manage the account and invite "
              "people",
    "carer": "hand the phone or tablet to a child, unlock a child who is locked out, see Home, progress and "
             "the children's PINs, type in the school's spelling list and mark a day off. A carer cannot change "
             "the children's plans, delete children, or change the account or its data",
}


async def settings_view(ctx: Ctx) -> dict:
    """What the Settings page shows besides the family's own settings: the adults, open invitations, this adult's
    login and weekly email, and the children's PINs (for every grown-up)."""
    fid = ctx.family["_id"]
    adults = [a async for a in db.accounts.find({"family_id": fid}).sort("created", 1)]
    owner_view = ctx.full
    names = {a["_id"]: adult_name(a) for a in adults}
    return {
        "adults": [{"id": a["_id"], "email": a["email"], "name": (a.get("name") or "").strip(),
                    "role": ROLE_TITLES.get(a.get("role") or "owner", "Parent"), "role_key": a.get("role") or "owner",
                    "you": a["_id"] == ctx.account["_id"], "by": names.get(a.get("invited_by"), ""),
                    "removable": owner_view and a["_id"] != ctx.account["_id"] and (a.get("role") or "owner") != "owner"}
                   for a in adults],
        "report_emails": bool(ctx.account.get("report_emails")),
        "plan_emails": bool(ctx.account.get("plan_emails")),
        "owner_name": next((adult_name(a) for a in adults if (a.get("role") or "owner") == "owner"), ""),
        "invites": [{"id": c["_id"], "email": c["email"], "role": ROLE_TITLES.get(c.get("role"), ""),
                     "until": local_time(c["expires"]).strftime("%d %B")}
                    async for c in db.codes.find({"family_id": fid, "purpose": "invite", "expires": {"$gt": _now()}})
                    .sort("expires", 1)],
        "weekly": weekly_on(ctx.account),
        "role_title": ROLE_TITLES.get(ctx.role, "Parent"),
        # every grown-up finds the PINs in the same place (Settings), parents and carers alike; a parent can also
        # see and change one in the child's own Settings
        "pins": [{"id": p["_id"], "name": p["name"], "pin": p.get("pin_view") or ""}
                 async for p in db.pupils.find({"family_id": fid}).sort("created", 1)],
    }


async def _settings_page(request: Request, ctx: Ctx, status_code: int = 400, **kw):
    return page(request, "settings.html", ctx, plan=plan_of(ctx.family), status_code=status_code,
                **await settings_view(ctx), **kw)


def _taken(email: str, family_id: str, acc: dict | None) -> str | None:
    """Why this address cannot join this family, or None."""
    if not acc:
        return None
    if acc["family_id"] == family_id:
        return f"{email} is already on your family."
    return (f"{email} already has its own Quizocracy family, so it cannot join yours as well. "
            f"Ask them to use a different email address, or to delete that other account first.")


@router.get("/not-allowed")
async def not_allowed(request: Request, ctx: Ctx = Depends(parent_page)):
    owner = await db.accounts.find_one({"family_id": ctx.family["_id"], "role": "owner"})
    return page(request, "not_allowed.html", ctx, owner=owner["email"] if owner else "", status_code=403)


@router.post("/settings/invite")
async def invite(request: Request, ctx: Ctx = Depends(full_page), email: str = Form(""), role: str = Form("carer")):
    email = email.strip().lower()
    role = role if role in ("parent", "carer") else "carer"
    fid = ctx.family["_id"]
    err = None
    if not EMAIL_RE.match(email):
        err = "Enter the email address of the person you want to invite."
    else:
        err = _taken(email, fid, await db.accounts.find_one({"email": email}))
    if not err:
        n = await db.accounts.count_documents({"family_id": fid}) + await db.codes.count_documents(
            {"family_id": fid, "purpose": "invite", "email": {"$ne": email}, "expires": {"$gt": _now()}})
        if n >= ADULTS_MAX:
            err = f"A family can have up to {ADULTS_MAX} grown-ups, invitations included. Remove someone first."
        elif not await _mail_allowed(request, "invite", email):
            err = "We have sent several invitations to that address already. Wait a few minutes before sending another."
    if err:
        return await _settings_page(request, ctx, invite_error=err, invite_email=email, invite_role=role)
    tok = new_token()
    await db.codes.delete_many({"family_id": fid, "purpose": "invite", "email": email})    # a new one replaces it
    await db.codes.insert_one({"_id": new_id("inv"), "email": email, "purpose": "invite", "hash": token_key(tok),
                               "family_id": fid, "role": role, "by": ctx.account["_id"], "created": _now(),
                               "expires": _now() + datetime.timedelta(days=INVITE_DAYS)})
    who, fam = ctx.account["email"], ctx.family["name"]
    if (ctx.account.get("name") or "").strip():
        who = f"{ctx.account['name'].strip()} ({who})"
    await mailer.send(email, f"{who} invited you to {fam} on Quizocracy",
                      f"Hello,\n\n{who} invites you to join {fam} on Quizocracy. Their children practise maths, "
                      f"spelling and more there, a few minutes a day.\n\n"
                      f"You are invited as a {role}. You will be able to {ROLE_CAN[role]}.\n\n"
                      f"To say yes, open this link within {INVITE_DAYS} days and choose your own password:\n\n"
                      f"{config.PUBLIC_URL}/invite?token={tok}\n\n"
                      f"Not expecting this? Then ignore this email.\n", secret=tok)
    return RedirectResponse("/settings?invited=1#adults", 303)


@router.post("/settings/invites/{iid}/cancel")
async def invite_cancel(request: Request, iid: str, ctx: Ctx = Depends(full_page)):
    await db.codes.delete_one({"_id": iid, "family_id": ctx.family["_id"], "purpose": "invite"})
    return RedirectResponse("/settings#adults", 303)


@router.post("/settings/adults/{aid}/remove")
async def adult_remove(request: Request, aid: str, ctx: Ctx = Depends(full_page)):
    acc = await db.accounts.find_one({"_id": aid, "family_id": ctx.family["_id"]})
    # The account owner stays (deleting the account is the way out), and nobody removes themselves by mistake.
    if not acc or acc["_id"] == ctx.account["_id"] or (acc.get("role") or "owner") == "owner":
        return RedirectResponse("/settings#adults", 303)
    await db.accounts.delete_one({"_id": acc["_id"]})
    await db.sessions.delete_many({"account_id": acc["_id"]})        # signed out on every device
    await db.codes.delete_many({"account_id": acc["_id"]})
    await log_event(ctx.family["_id"], "adult", f"{adult_name(ctx.account)} removed {adult_name(acc)} "
                                                f"({ROLE_TITLES.get(acc.get('role'), 'Carer')})")
    await mailer.send(acc["email"], f"You were removed from {ctx.family['name']} on Quizocracy",
                      f"Hello,\n\n{ctx.account['email']} removed you from {ctx.family['name']} on Quizocracy. "
                      f"Your login there no longer works.\n\nIf you think this is a mistake, ask them to invite "
                      f"you again.\n")
    return RedirectResponse("/settings?removed=1#adults", 303)


@router.post("/settings/adults/{aid}/role")
async def adult_role(request: Request, aid: str, ctx: Ctx = Depends(full_page), to: str = Form("")):
    """Parent ⇄ Carer for another grown-up, keeping their login, password and weekly-email choice. The account
    owner's role never changes, and nobody changes their own."""
    acc, role = await db.accounts.find_one({"_id": aid, "family_id": ctx.family["_id"]}), to
    old = (acc or {}).get("role") or "owner"
    if not acc or acc["_id"] == ctx.account["_id"] or old == "owner" or role not in ("parent", "carer") or role == old:
        return RedirectResponse("/settings#adults", 303)
    # the weekly email defaults by role, so a choice never made is written down before the role changes
    await db.accounts.update_one({"_id": acc["_id"]}, {"$set": {"role": role, "weekly_email": weekly_on(acc)}})
    who, fam = adult_name(ctx.account), ctx.family["name"]
    await log_event(ctx.family["_id"], "role", f"{who} changed {adult_name(acc)} from {ROLE_TITLES[old]} to {ROLE_TITLES[role]}")
    await mailer.send(acc["email"], f"You are now a {role} on {fam} on Quizocracy",
                      f"Hello,\n\n{who} changed your role on {fam} from {old} to {role}. Your login and password "
                      f"stay the same.\n\nAs a {role} you can {ROLE_CAN[role].removeprefix('do everything they can do: ')}.\n")
    return RedirectResponse(f"/settings?role_changed={acc['_id']}#adults", 303)


@router.post("/settings/name")
async def my_name(request: Request, ctx: Ctx = Depends(parent_page), name: str = Form("")):
    """The name the other grown-ups see for this adult ("Jo"), in Settings and the family activity log."""
    await db.accounts.update_one({"_id": ctx.account["_id"]}, {"$set": {"name": " ".join(name.split())[:40]}})
    return RedirectResponse("/settings?name_saved=1#login", 303)


@router.post("/settings/report-emails")
async def report_emails_toggle(request: Request, ctx: Ctx = Depends(parent_page), on: str = Form(""),
                               back: str = Form("")):
    """Email me when the team has checked a question a child reported (on for families who joined since 10 Nov
    2026). Also ticked under "Questions … reported" on a child's progress page (back: that child's id)."""
    await db.accounts.update_one({"_id": ctx.account["_id"]}, {"$set": {"report_emails": bool(on)}})
    if back and re.fullmatch(r"p_[0-9a-f]+", back):
        return RedirectResponse(f"/children/{back}?report_emails={'on' if on else 'off'}#reports", 303)
    return RedirectResponse("/settings?saved=1#login", 303)


@router.post("/settings/plan-emails")
async def plan_emails_toggle(request: Request, ctx: Ctx = Depends(parent_page), on: str = Form("")):
    """Email me when another grown-up changes a child's plan, target, reward, days off, spelling list or topics
    (off unless ticked; Family activity on Home lists every change either way)."""
    await db.accounts.update_one({"_id": ctx.account["_id"]}, {"$set": {"plan_emails": bool(on)}})
    return RedirectResponse("/settings?saved=1#login", 303)


async def _open_invite(token: str) -> dict | None:
    return await db.codes.find_one({"purpose": "invite", "hash": token_key(token or ""), "expires": {"$gt": _now()}})


@router.get("/invite")
async def invite_form(request: Request, token: str = ""):
    inv = await _open_invite(token)
    fam = await db.families.find_one({"_id": inv["family_id"]}) if inv else None
    if not inv or not fam:
        return page(request, "invite.html", invalid=True, status_code=400)
    by = await db.accounts.find_one({"_id": inv.get("by")}) or {}
    return page(request, "invite.html", inv=inv, family=fam, by=by.get("email", ""), token=token,
                can=ROLE_CAN[inv["role"]], error=_taken(inv["email"], fam["_id"], await db.accounts.find_one({"email": inv["email"]})))


@router.post("/invite")
async def invite_accept(request: Request, token: str = Form(...), password: str = Form(""), consent: str = Form(""),
                        name: str = Form("")):
    inv = await _open_invite(token)
    fam = await db.families.find_one({"_id": inv["family_id"]}) if inv else None
    if not inv or not fam:
        return page(request, "invite.html", invalid=True, status_code=400)
    by = await db.accounts.find_one({"_id": inv.get("by")}) or {}
    name = " ".join(name.split())[:40]
    taken = _taken(inv["email"], fam["_id"], await db.accounts.find_one({"email": inv["email"]}))
    # every problem at once, so a nervous first try is fixed in one go (the password stays typed)
    errs = [taken] if taken else [e for e, bad in (("Use a password of 8 characters or more.", len(password) < 8),
                                                     ("Tick the box to confirm you are aged 18 or over.", not consent)) if bad]
    acc = {"_id": new_id("acc"), "email": inv["email"], "pw": hash_secret(password), "family_id": fam["_id"],
           "role": inv["role"], "invited_by": inv.get("by"), "created": _now(), "verified_at": _now(),
           "report_emails": True, **({"name": name} if name else {})}
    if not errs:
        try:
            await db.accounts.insert_one(acc)          # the link came to this inbox, so the address is verified
        except DuplicateKeyError:
            errs = [_taken(inv["email"], fam["_id"], await db.accounts.find_one({"email": inv["email"]}))]
    if errs:
        return page(request, "invite.html", inv=inv, family=fam, by=by.get("email", ""), token=token,
                    can=ROLE_CAN[inv["role"]], errors=errs, consent=consent, status_code=400,
                    typed={"name": name, "password": password if not taken else ""})
    await db.codes.delete_many({"purpose": "invite", "email": inv["email"]})      # every family's: it has joined one
    resp = RedirectResponse("/home?joined=1", 303)
    await create_session(resp, acc)
    await note_device(request, resp, acc, quiet=True)
    title = ROLE_TITLES[inv["role"]]
    await log_event(fam["_id"], "adult", f"{name + ' (' + acc['email'] + ')' if name else acc['email']} joined as {title.lower()}"
                                         + (f", invited by {adult_name(by)}" if by else ""))
    # The parents hear of every new grown-up (who can see the children's PINs), once.
    await mailer.to_family(fam["_id"], f"{acc['email']} joined {fam['name']} on Quizocracy",
                           f"Hello,\n\n{acc['email']} has joined {fam['name']} on Quizocracy as a {inv['role']}"
                           + (f", invited by {adult_name(by)}" if by else "") + ".\n\n"
                           f"In Settings you can see every grown-up, change their role or remove them: "
                           f"{config.PUBLIC_URL}/settings#adults\n\nDon't know this person? Remove them there.\n",
                           skip=(acc["_id"],))
    return resp


# ---- Changing the account email: a code goes to the new address, a notice to the old one ----

@router.get("/account/email")
async def email_form(request: Request, ctx: Ctx = Depends(full_page)):
    rec = await db.codes.find_one({"account_id": ctx.account["_id"], "purpose": "email_change", "expires": {"$gt": _now()}})
    return page(request, "email_change.html", ctx, pending=rec["email"] if rec and request.query_params.get("sent") else None)


@router.post("/account/email")
async def email_change(request: Request, ctx: Ctx = Depends(full_page), new_email: str = Form(""),
                       password: str = Form("")):
    new_email = new_email.strip().lower()
    err = None
    if not EMAIL_RE.match(new_email):
        err = "Enter a valid email address."
    elif new_email == ctx.account["email"]:
        err = "That is already your email address."
    elif not verify_secret(password, ctx.account["pw"]):
        err = "Your password is not right."
    elif await db.accounts.find_one({"email": new_email}):
        err = "That email already has a Quizocracy account. Choose another address."
    elif not await _mail_allowed(request, "email_change", new_email):
        err = "We have sent several codes already. Check that inbox and its spam folder, or wait a few minutes."
    if err:
        return page(request, "email_change.html", ctx, error=err, new_email=new_email, status_code=400)
    await _send_change_code(ctx.account, new_email)
    return RedirectResponse("/account/email?sent=1", 303)


async def _send_change_code(account: dict, new_email: str) -> None:
    code = new_code()
    await db.codes.delete_many({"account_id": account["_id"], "purpose": "email_change"})
    await db.codes.insert_one({"email": new_email, "purpose": "email_change", "account_id": account["_id"],
                               "family_id": account["family_id"], "hash": hash_secret(code), "tries": 0,
                               "expires": _now() + datetime.timedelta(minutes=30)})
    await mailer.send(new_email, f"Your Quizocracy code: {code}",
                      f"Your code is {code}\n\nType it in Quizocracy to make {new_email} the email you sign in "
                      f"with. It works for 30 minutes.\n\nDidn't ask for this? Then ignore this email. "
                      f"Nothing changes.\n", secret=code)


@router.post("/account/email/resend")
async def email_resend(request: Request, ctx: Ctx = Depends(full_page)):
    rec = await db.codes.find_one({"account_id": ctx.account["_id"], "purpose": "email_change"})
    if not rec:
        return RedirectResponse("/account/email", 303)
    if not await _mail_allowed(request, "email_change", rec["email"]):
        return page(request, "email_change.html", ctx, pending=rec["email"], status_code=429,
                    error="We have sent several codes already. Check that inbox and its spam folder, "
                          "or wait a few minutes before asking for another.")
    await _send_change_code(ctx.account, rec["email"])
    return RedirectResponse("/account/email?sent=1", 303)


@router.post("/account/email/confirm")
async def email_confirm(request: Request, ctx: Ctx = Depends(full_page), code: str = Form("")):
    aid = ctx.account["_id"]
    rec = await db.codes.find_one({"account_id": aid, "purpose": "email_change", "expires": {"$gt": _now()}})
    if not rec:
        return page(request, "email_change.html", ctx, status_code=400,
                    error="That code has expired. Enter the new address again to get a new code.")
    fails_key = f"verify:{rec['email']}"         # the same hourly cap as the sign-up code
    err = None
    if await over_limit(fails_key, CODE_FAILS_HOUR, 60):
        err = "Too many wrong codes. Wait an hour, then ask for a new code."
    elif rec.get("tries", 0) >= CODE_TRIES:
        err = "That code has had too many wrong tries and no longer works. Ask for a new code below."
    elif not verify_secret(code.strip(), rec["hash"]):
        await db.codes.update_one({"_id": rec["_id"]}, {"$inc": {"tries": 1}})
        await hit(fails_key)
        err = "That code is not right, or it has expired."
    if err:
        return page(request, "email_change.html", ctx, pending=rec["email"], error=err, status_code=400)
    old, new = ctx.account["email"], rec["email"]
    try:
        await db.accounts.update_one({"_id": aid}, {"$set": {"email": new}, "$addToSet": {"past_emails": old}})
    except DuplicateKeyError:
        await db.codes.delete_many({"account_id": aid, "purpose": "email_change"})
        return page(request, "email_change.html", ctx, status_code=400,
                    error="That email has just been used for another Quizocracy account. Choose another address.")
    await db.codes.delete_many({"account_id": aid, "purpose": "email_change"})
    await mailer.send(old, "Your Quizocracy email was changed",
                      f"The email you sign in to Quizocracy with was changed from {old} to {new} on "
                      f"{local_time(_now()):%d %B %Y at %H:%M}. From now on, sign in with {new}.\n\n"
                      f"If this wasn't you, reply to this email now (or write to {config.SUPPORT_EMAIL}) "
                      f"and we will put it right.\n", headers={"Reply-To": config.SUPPORT_EMAIL})
    return RedirectResponse("/settings?email_changed=1", 303)


# ---- The weekly summary: on/off in Settings, and a signed one-click link in each email ----

@router.post("/settings/weekly")
async def weekly_toggle(request: Request, ctx: Ctx = Depends(parent_page), weekly: str = Form("")):
    await db.accounts.update_one({"_id": ctx.account["_id"]}, {"$set": {"weekly_email": bool(weekly)}})
    return RedirectResponse("/settings?saved=1#login", 303)


@router.get("/unsubscribe")
async def unsubscribe_form(request: Request, t: str = ""):
    # A link opened is not yet a "yes": mail scanners open links too. One press of the button turns it off.
    acc = await db.accounts.find_one({"_id": mailer.unsub_account(t)}) if mailer.unsub_account(t) else None
    return page(request, "unsubscribe.html", acc=acc, t=t, status_code=200 if acc else 400)


@router.post("/unsubscribe")
async def unsubscribe(request: Request):
    form = await request.form()
    t = request.query_params.get("t") or form.get("t") or ""      # mail apps' one-click POST puts it in the URL
    aid = mailer.unsub_account(t)
    acc = await db.accounts.find_one({"_id": aid}) if aid else None
    if acc:
        await db.accounts.update_one({"_id": aid}, {"$set": {"weekly_email": False}})
    return page(request, "unsubscribe.html", acc=acc, t=t, done=bool(acc), status_code=200 if acc else 400)
