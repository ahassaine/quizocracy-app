"""Founding families and invitations from one family to another (the beta offer).

Founding family: every family that signs up while QZ_FOUNDING is on (the beta) is marked `founding: True`.
The offer, as the landing page and the terms state it: free during the beta, then FREE_MONTHS free months after
launch, for all its children. Nothing is charged today, so this only records who is owed what.

Invitations: each family has its own code (families.ref, made the first time it is needed) and link /join/<code>.
That code works on the sign-up form like the beta's invitation code, and the new family is stored with
`referred_by` = the inviting family's id. When the new family "stays" (at least one child answered a question in
its week 2, days 8-14, as in app/funnel.py), both families earn BONUS_MONTHS more free months. The inviting family
sees only counts, never who joined."""
import datetime
import secrets

from . import config, funnel
from .db import db

FREE_MONTHS = 12
BONUS_MONTHS = 1
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"      # no 0/O, 1/I/L: easy to read out
LENGTH = 6


def _norm(code: str) -> str:
    return "".join((code or "").split()).upper()


async def ensure_ref(family: dict) -> str:
    if family.get("ref"):
        return family["ref"]
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(LENGTH))
        if not await db.families.find_one({"ref": code}, {"_id": 1}):
            break
    await db.families.update_one({"_id": family["_id"], "ref": {"$exists": False}}, {"$set": {"ref": code}})
    family["ref"] = (await db.families.find_one({"_id": family["_id"]}, {"ref": 1}))["ref"]
    return family["ref"]


async def family_by_ref(code: str):
    code = _norm(code)
    if len(code) != LENGTH:
        return None
    return await db.families.find_one({"ref": code}, {"_id": 1, "ref": 1})


def link(code: str) -> str:
    return f"{config.PUBLIC_URL}/join/{code}"


async def stayed(family: dict) -> bool:
    """At least one child answered a question in the family's week 2 (days 8-14 from its sign-up day)."""
    d1 = funnel.local_day(family["created"])
    for d in await funnel.active_days(family):
        if 8 <= (datetime.date.fromisoformat(d) - d1).days + 1 <= 14:
            return True
    return False


async def summary(family: dict) -> dict:
    """What a family sees on Home: its link, how many families joined with it, how many stayed, and its months."""
    code = await ensure_ref(family)
    joined, kept = 0, 0
    async for f in db.families.find({"referred_by": family["_id"]}, {"created": 1, "funnel_days": 1}):
        joined += 1
        kept += await stayed(f)
    own = 0
    if family.get("referred_by") and await stayed(family):
        own = 1                                     # joined with another family's link and stayed
    return {"code": code, "link": link(code), "joined": joined, "stayed": kept,
            "founding": bool(family.get("founding")), "free_months": FREE_MONTHS,
            "bonus": (kept + own) * BONUS_MONTHS}
