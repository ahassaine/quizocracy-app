"""Transactional email. Every message is recorded in the outbox; it is sent unless capture applies."""
import asyncio
import base64
import datetime
import hashlib
import hmac
import smtplib
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from . import config
from .db import db


def _send_smtp(msg: EmailMessage) -> None:
    with smtplib.SMTP(config.MAIL_HOST, config.MAIL_PORT, timeout=20) as s:
        s.send_message(msg)


async def send(to: str, subject: str, body: str, secret: str | None = None, html: str | None = None,
               headers: dict | None = None) -> None:
    """`secret`: a live code or link token in the message. A captured message is kept whole (it is never sent, and
    the tests read it); a message really sent is logged without the secret, which is stored only as a hash.
    `html`: an HTML version sent alongside the plain text; `headers`: extra headers (List-Unsubscribe)."""
    to = to.strip().lower()
    captured = config.MAIL_MODE != "smtp" or to.split("@")[-1] in config.CAPTURE_DOMAINS
    log_subject, log_body = subject, body
    if secret and not captured:
        log_subject, log_body = subject.replace(secret, "[removed]"), body.replace(secret, "[removed]")
    row = {"to": to, "subject": log_subject, "body": log_body, "captured": captured,
           "created": datetime.datetime.utcnow()}
    if html and captured:
        row["html"] = html
    await db.outbox.insert_one(row)
    if captured:
        return
    msg = EmailMessage()
    msg["From"] = config.MAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="quizocracy.com")
    for k, v in (headers or {}).items():
        msg[k] = v
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")
    await asyncio.to_thread(_send_smtp, msg)


async def to_family(family_id: str, subject: str, body: str, roles: tuple = ("owner", "parent"), skip: tuple = (),
                    flag: str | None = None) -> int:
    """The same message to each adult of a family with one of `roles` (the parents, by default), leaving out the
    account ids in `skip`; with `flag`, only adults who ticked that setting. Returns how many were sent."""
    n = 0
    async for a in db.accounts.find({"family_id": family_id, "verified_at": {"$ne": None}}):
        if (a.get("role") or "owner") in roles and a["_id"] not in skip and (not flag or a.get(flag)):
            await send(a["email"], subject, body)
            n += 1
    return n


def _sig(purpose: str, account_id: str) -> str:
    mac = hmac.new(config.SECRET_KEY.encode(), f"{purpose}:{account_id}".encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac[:18]).decode()


def unsub_token(account_id: str, purpose: str = "weekly") -> str:
    """A link token that turns one email off for one adult without signing in: the account id, signed."""
    return f"{account_id}.{_sig(purpose, account_id)}"


def unsub_account(token: str, purpose: str = "weekly") -> str | None:
    """The account id in a valid unsubscribe token, or None."""
    aid, _, sig = (token or "").partition(".")
    return aid if aid and sig and hmac.compare_digest(sig, _sig(purpose, aid)) else None


async def alert(subject: str, body: str) -> bool:
    """A message to the operator (QZ_ALERT_EMAIL; nothing if unset). Unlike send(), the database is optional:
    the error being reported may be the database itself, so a failed outbox write never stops the email."""
    to = config.ALERT_EMAIL
    if not to:
        return False
    captured = config.MAIL_MODE != "smtp" or to.split("@")[-1] in config.CAPTURE_DOMAINS
    try:
        await asyncio.wait_for(db.outbox.insert_one({"to": to, "subject": subject, "body": body, "captured": captured,
                                                     "kind": "alert", "created": datetime.datetime.utcnow()}), 3)
    except Exception:  # noqa: BLE001 - the outbox is a record only
        pass
    if captured:
        return True
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = config.MAIL_FROM, to, subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="quizocracy.com")
    msg.set_content(body)
    await asyncio.to_thread(_send_smtp, msg)
    return True
