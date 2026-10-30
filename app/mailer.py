"""Transactional email. Every message is recorded in the outbox; it is sent unless capture applies."""
import asyncio
import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from . import config
from .db import db


def _send_smtp(msg: EmailMessage) -> None:
    with smtplib.SMTP(config.MAIL_HOST, config.MAIL_PORT, timeout=20) as s:
        s.send_message(msg)


async def send(to: str, subject: str, body: str) -> None:
    to = to.strip().lower()
    captured = config.MAIL_MODE != "smtp" or to.split("@")[-1] in config.CAPTURE_DOMAINS
    await db.outbox.insert_one({"to": to, "subject": subject, "body": body, "captured": captured,
                                "created": datetime.datetime.utcnow()})
    if captured:
        return
    msg = EmailMessage()
    msg["From"] = config.MAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="quizocracy.com")
    msg.set_content(body)
    await asyncio.to_thread(_send_smtp, msg)
