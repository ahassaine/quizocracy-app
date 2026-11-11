"""Do families stay? The sign-up funnel and the parents' "How is it going?" cards, from our own database only.

The funnel is read from what is already stored: a family's sign-up (families.created), the owner's verification,
its children (pupils.created) and its answers (attempts: one row per answer, with the London `day`). Deleting a
child deletes its answers, so _delete_pupils first calls keep() to fold that child's dates into the family
(first_child_at, first_answer_at, funnel_days: dates only, no answers). Deleting the whole family deletes those too.

Day 1 is the sign-up day (London time), day 2 the next day; week 1 is days 1-7, week 2 days 8-14, and so on.
Active: at least one child of the family answered a question that day (or that week).
"""
import datetime
from zoneinfo import ZoneInfo

from . import config
from .db import db

TZ = ZoneInfo(config.TIMEZONE)
STEPS = [("signed_up", "Signed up"), ("verified", "Email verified"), ("child", "First child added"),
         ("answer", "First answer"), ("day2", "Active on day 2"), ("week1", "Active in week 1"),
         ("week2", "Active in week 2"), ("week3", "Active in week 3"), ("week4", "Active in week 4")]
# The last day a step can still happen on (day 1 = sign-up day); None: no deadline.
DEADLINE = {"day2": 2, "week1": 7, "week2": 14, "week3": 21, "week4": 28}
CARDS = {"d3": "3rd active day", "d14": "Day 14"}
MOODS = {"good": "😊 Good", "ok": "😐 OK", "bad": "🙁 Not great"}
CARD_DAYS = 7          # a card nobody answered retires a week after it first showed: it never nags


def local_day(utc: datetime.datetime) -> datetime.date:
    return utc.replace(tzinfo=datetime.timezone.utc).astimezone(TZ).date()


def today() -> datetime.date:
    return datetime.datetime.now(TZ).date()


def is_test(family: dict, emails: list) -> bool:
    """A beta tester's or an automated test's family: marked by hand on the funnel page, else any of its
    grown-ups' addresses is on a test domain (QZ_FUNNEL_TEST_DOMAINS)."""
    if family.get("test") is not None:
        return bool(family["test"])
    return any(e.rsplit("@", 1)[-1].lower() in config.FUNNEL_TEST_DOMAINS for e in emails)


async def keep(pupil_ids: list) -> None:
    """Before children are deleted: keep their family's funnel dates (never the answers themselves)."""
    if not pupil_ids:
        return
    async for p in db.pupils.aggregate([{"$match": {"_id": {"$in": pupil_ids}}},
                                        {"$group": {"_id": "$family_id", "c": {"$min": "$created"}}}]):
        if p.get("c"):
            await db.families.update_one({"_id": p["_id"]}, {"$min": {"first_child_at": p["c"]}})
    async for a in db.attempts.aggregate([{"$match": {"pupil_id": {"$in": pupil_ids}}},
                                          {"$group": {"_id": "$family_id", "t": {"$min": "$ts"},
                                                      "days": {"$addToSet": "$day"}}}]):
        await db.families.update_one({"_id": a["_id"]}, {"$min": {"first_answer_at": a["t"]},
                                                         "$addToSet": {"funnel_days": {"$each": a["days"]}}})


async def active_days(family: dict) -> set:
    return set(await db.attempts.distinct("day", {"family_id": family["_id"]})) | set(family.get("funnel_days") or [])


def _row(f: dict, emails: list, verified, child, answer, days: set, now: datetime.date) -> dict:
    d1 = local_day(f["created"])
    nums = sorted((datetime.date.fromisoformat(d) - d1).days + 1 for d in days)
    nums = [n for n in nums if n >= 1]
    age = (now - d1).days + 1                                   # today is day `age`
    when = {"signed_up": d1, "verified": verified and local_day(verified), "child": child and local_day(child),
            "answer": answer and local_day(answer)}
    first = lambda lo, hi: next((d1 + datetime.timedelta(days=n - 1) for n in nums if lo <= n <= hi), None)
    when["day2"] = first(2, 2)
    for w in (1, 2, 3, 4):
        when[f"week{w}"] = first(7 * w - 6, 7 * w)
    # a step is "due" once its window is over (or it happened): only those count in the percentages
    due = {k: bool(when.get(k)) or DEADLINE.get(k, 0) < age for k, _ in STEPS}
    return {"id": f["_id"], "name": f.get("name", ""), "emails": emails, "test": is_test(f, emails),
            "test_set": f.get("test"), "d1": d1, "age": age, "when": when, "due": due, "active_days": len(nums),
            "week": d1 - datetime.timedelta(days=d1.weekday())}


async def families(include_test: bool = False) -> list:
    """Every family's funnel dates, newest sign-up first."""
    emails, verified = {}, {}
    async for a in db.accounts.find({}, {"family_id": 1, "email": 1, "role": 1, "verified_at": 1}):
        emails.setdefault(a["family_id"], []).append(a["email"])
        if (a.get("role") or "owner") == "owner" and a.get("verified_at"):
            verified[a["family_id"]] = a["verified_at"]
    child = {r["_id"]: r["c"] async for r in db.pupils.aggregate(
        [{"$group": {"_id": "$family_id", "c": {"$min": "$created"}}}])}
    answers = {r["_id"]: r async for r in db.attempts.aggregate(
        [{"$group": {"_id": "$family_id", "t": {"$min": "$ts"}, "days": {"$addToSet": "$day"}}}])}
    now, rows = today(), []
    names = {f["_id"]: f.get("name", "") async for f in db.families.find({}, {"name": 1})}
    async for f in db.families.find({}).sort("created", -1):
        if not f.get("created"):
            continue
        a = answers.get(f["_id"]) or {}
        firsts = lambda *xs: min((x for x in xs if x), default=None)
        r = _row(f, emails.get(f["_id"], []), verified.get(f["_id"]),
                 firsts(child.get(f["_id"]), f.get("first_child_at")), firsts(a.get("t"), f.get("first_answer_at")),
                 set(a.get("days") or []) | set(f.get("funnel_days") or []), now)
        r["via"] = names.get(f.get("referred_by"), "a deleted family") if f.get("referred_by") else ""
        r["via_id"] = f.get("referred_by") or ""
        r["founding"] = bool(f.get("founding"))
        if include_test or not r["test"]:
            rows.append(r)
    return rows


def cohorts(rows: list) -> list:
    """Per week of sign-up (Monday), newest first, then "All weeks": for each step the families that reached it,
    of those whose window for it is over ("due"), and the percentage of those."""
    groups = {}
    for r in rows:
        groups.setdefault(r["week"], []).append(r)
    out = []
    for label, rs in [(f"Week of {w.day} {w:%b %Y}", groups[w]) for w in sorted(groups, reverse=True)] + [("All weeks", rows)]:
        cells = {}
        for k, _ in STEPS:
            due = [r for r in rs if r["due"][k]]
            n = sum(1 for r in due if r["when"].get(k))
            cells[k] = {"n": n, "due": len(due), "pct": round(100 * n / len(due)) if due else None}
        out.append({"label": label, "size": len(rs), "cells": cells})
    return out if rows else []


# ---------------------------------------------------------------- "How is it going?" cards on Home ----

async def card_for(account: dict, family: dict) -> str | None:
    """The card this grown-up should see on Home now: "d14" from the family's 14th day, else "d3" from its 3rd
    active day. Each shows until it is sent or dismissed, or for CARD_DAYS after it first showed; then never
    again. A card that came due while a later one is showing is skipped."""
    if not family.get("created"):
        return None
    done = {d["card"]: d async for d in db.feedback.find({"account_id": account["_id"]})}
    age = (today() - local_day(family["created"])).days + 1
    card = "d14" if age >= 14 else "d3" if len(await active_days(family)) >= 3 else None
    if card is None or (card == "d3" and "d14" in done):
        return None
    d = done.get(card)
    now = datetime.datetime.utcnow()
    if d is None:
        await db.feedback.update_one({"_id": f"{account['_id']}:{card}"}, {"$setOnInsert": {
            "account_id": account["_id"], "family_id": family["_id"], "card": card, "shown_at": now,
            "status": "shown"}}, upsert=True)
        return card
    if d.get("status") != "shown" or now - d["shown_at"] > datetime.timedelta(days=CARD_DAYS):
        return None
    return card


def invitations(rows: list) -> dict:
    """Who invited whom (app/referrals.py), from the funnel rows: per inviting family, the families that joined with
    its link, how many kept going into week 2, and the extra free months both sides have earned so far."""
    by = {}
    for r in rows:
        if r["via_id"]:
            e = by.setdefault(r["via_id"], {"name": r["via"], "joined": 0, "stayed": 0})
            e["joined"] += 1
            e["stayed"] += bool(r["when"].get("week2"))
    stayed_new = sum(bool(r["via_id"] and r["when"].get("week2")) for r in rows)
    return {"inviters": sorted(by.values(), key=lambda e: (-e["stayed"], -e["joined"], e["name"])),
            "founding": sum(r["founding"] for r in rows), "joined": sum(bool(r["via_id"]) for r in rows),
            "stayed": stayed_new}
