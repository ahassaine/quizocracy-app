#!/usr/bin/env python3
"""The Sunday-evening summary to parents: how each child's week (Monday to Sunday) went.

    python3 scripts/weekly_email.py --env-file .env              # cron, Sunday evening
    python3 scripts/weekly_email.py --env-file .env --dry-run    # print the emails, send and record nothing
    python3 scripts/weekly_email.py --env-file .env --to a@b.c   # only that adult (and so only their family)
    --week 2026-11-02   the Monday of another week (default: the week ending on the latest Sunday, today on a Sunday)

Each adult whose "Email me a weekly summary" is on gets one email per week: sends are recorded in weekly_sends
(_id "<monday>:<account>") before sending, so a second run of the same week sends nothing. Families with no
answer in the week are skipped. Every sentence here is fixed text; nothing is generated.
"""
import argparse
import asyncio
import datetime
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env(path: str) -> None:
    """KEY=value lines (as pm2's --env-file reads them); variables already set win."""
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def week_of(monday: str | None, today: datetime.date) -> list:
    """The seven local dates (ISO) of the week: the given Monday's, or the week ending on the latest Sunday."""
    if monday:
        start = datetime.date.fromisoformat(monday)
        start -= datetime.timedelta(days=start.weekday())
    else:
        start = today - datetime.timedelta(days=(today.weekday() + 1) % 7 + 6)
    return [(start + datetime.timedelta(days=i)).isoformat() for i in range(7)]


def week_label(days: list) -> str:
    a, b = datetime.date.fromisoformat(days[0]), datetime.date.fromisoformat(days[-1])
    if a.month == b.month:
        return f"the week of {a.day} to {b.day} {b:%B}"
    return f"the week of {a.day} {a:%B} to {b.day} {b:%B}"


def plural(n: int, one: str, many: str | None = None) -> str:
    return f"{n} {one if n == 1 else (many or one + 's')}"


def warm_line(name: str, done: int, days: int, answers: int) -> str:
    if not answers:
        return f"No practice this week. A short go on Monday is a good way for {name} to start again."
    if done >= days:
        return f"Every day done. That is a great habit: tell {name} well done!"
    if 2 * done >= days:
        return f"A good week: most days done. Well done, {name}."
    if done:
        return f"Some days done. A few minutes at the same time each day helps {name} most."
    return f"{name} practised, but did not finish a day's plan this week. A smaller plan can make finishing easier."


async def child_summary(p: dict, fam: dict, days: list, today: str, start_utc, end_utc) -> dict:
    from app import config, progress
    from app.bank import engine as bank_engine
    from app.db import db
    from app.maths import maths_mastery

    pid = p["_id"]
    first = progress.first_day(p)
    counted = [d for d in days if d >= first and d <= today]
    c = (await progress.counts([pid], days)).get(pid, {})
    st = (await progress.day_stats([pid], days)).get(pid, {})
    done = sum(1 for d in counted if progress.day_status(p, fam, c.get(d, {}), d)["pct"] >= 100)
    tot = {k: sum(int(s.get(k) or 0) for s in st.values())
           for k in ("answers", "first", "first_right", "minutes", "rushed", "copied")}
    titles = {s["key"]: s["title"] for s in maths_mastery.skill_list()}
    in_week = {"$gte": start_utc, "$lt": end_utc}

    mastered, weak = [], []
    async for d in db.maths_mastery.find({"pupil": pid, "mastered_at": in_week}):
        mastered.append(titles.get(d.get("skill"), d.get("skill")))
    async for d in db.bank_mastery.find({"pupil_id": pid, "mastered_at": in_week}):
        sk = bank_engine.skill(d["key"]) or {}
        mastered.append(sk.get("title") or d["key"])
    practised = []
    async for d in db.maths_mastery.find({"pupil": pid, "last": in_week, "score": {"$lt": maths_mastery.MASTERED}}):
        practised.append((int(d.get("score", 0)), titles.get(d.get("skill"), d.get("skill"))))
    async for d in db.bank_mastery.find({"pupil_id": pid, "last": in_week, "score": {"$lt": maths_mastery.MASTERED}}):
        sk = bank_engine.skill(d["key"]) or {}
        practised.append((int(d.get("score", 0)), f"{sk.get('title') or d['key']} ({d.get('subject', '')})"))
    weak = [t for _, t in sorted(practised)[:3]]
    # mistakes from the week (back from today to its Monday) not put right since
    opened = await progress.open_mistakes(p, (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(days[0])).days + 1)
    words = {"spelling": lambda w: f'spelling "{w}"', "tables": lambda f: f.replace("x", " × "),
             "verbs": lambda b: f'past forms of "{b}"', "numbers": lambda n: f"{n} in words"}
    shown = 0
    for act, fn in words.items():
        for det in opened.get(act, []):
            if len(weak) < 3:
                weak.append(fn(det))
                shown += 1
    more = sum(len(v) for k, v in opened.items() if k in words) - shown    # skills are already named above
    if more > 0:
        weak.append(plural(more, "more mistake") + " to put right")
    flags = []
    if tot["rushed"]:
        flags.append(plural(tot["rushed"], "wrong answer") + " given very fast or with random keys")
    if tot["copied"]:
        flags.append(plural(tot["copied"], "right answer") + " typed straight after being shown the answer")
    return {"name": p["name"], "year": p.get("year"), "days": max(1, len(counted)), "done": done,
            "answers": tot["answers"], "minutes": tot["minutes"],
            "first_pct": (100 * tot["first_right"] // tot["first"]) if tot["first"] else None,
            "mastered": mastered[:6] + ([f"and {len(mastered) - 6} more"] if len(mastered) > 6 else []),
            "weak": weak, "flags": flags, "line": warm_line(p["name"], done, max(1, len(counted)), tot["answers"]),
            "url": f"{config.PUBLIC_URL}/children/{pid}"}


async def run(args) -> int:
    from jinja2 import Environment, FileSystemLoader
    from pymongo.errors import DuplicateKeyError

    from app import config, mailer, progress
    from app.db import db
    from app.deps import weekly_on

    tz = progress.TZ
    today = datetime.datetime.now(tz).date()
    days = week_of(args.week, today)
    monday = days[0]

    def utc(d: str) -> datetime.datetime:
        local = datetime.datetime.combine(datetime.date.fromisoformat(d), datetime.time(), tz)
        return local.astimezone(datetime.timezone.utc).replace(tzinfo=None)

    start_utc = utc(monday)
    end_utc = utc((datetime.date.fromisoformat(days[-1]) + datetime.timedelta(days=1)).isoformat())
    folder = str(ROOT / "app" / "templates" / "emails")
    html_env = Environment(loader=FileSystemLoader(folder), autoescape=True)
    text_env = Environment(loader=FileSystemLoader(folder), autoescape=False, keep_trailing_newline=True)
    label = week_label(days)

    q = {"verified_at": {"$ne": None}}
    if args.to:
        q["email"] = args.to.strip().lower()
    adults = [a async for a in db.accounts.find(q)]
    by_family: dict = {}
    for a in adults:
        if weekly_on(a) or args.to:
            by_family.setdefault(a["family_id"], []).append(a)
        if args.to and not weekly_on(a):
            print(f"note: {a['email']} has the weekly summary turned off; --to sends it anyway")

    sent = quiet = already = failed = 0
    for fid, recipients in by_family.items():
        fam = await db.families.find_one({"_id": fid})
        pupils = [p async for p in db.pupils.find({"family_id": fid}).sort("created", 1)]
        if not fam or not pupils or not await db.attempts.find_one(
                {"pupil_id": {"$in": [p["_id"] for p in pupils]}, "day": {"$in": days}}, {"_id": 1}):
            quiet += 1
            continue
        children = [await child_summary(p, fam, days, today.isoformat(), start_utc, end_utc) for p in pupils]
        subject = f"{fam['name']}: your week on Quizocracy ({label.removeprefix('the week of ')})"
        for a in recipients:
            key = f"{monday}:{a['_id']}"
            if await db.weekly_sends.find_one({"_id": key}):
                already += 1
                continue
            tok = mailer.unsub_token(a["_id"])
            unsub = f"{config.PUBLIC_URL}/unsubscribe?t={tok}"
            ctx = {"week_label": label, "children": children, "unsub_url": unsub}
            text = text_env.get_template("weekly.txt").render(**ctx)
            html = html_env.get_template("weekly.html").render(**ctx)
            if args.dry_run:
                print(f"--- To: {a['email']}\nSubject: {subject}\n\n{text}")
                sent += 1
                continue
            try:
                await db.weekly_sends.insert_one({"_id": key, "family_id": fid, "account_id": a["_id"],
                                                  "week": monday, "to": a["email"],
                                                  "sent": datetime.datetime.utcnow()})
            except DuplicateKeyError:            # another run got there first
                already += 1
                continue
            try:
                await mailer.send(a["email"], subject, text, html=html,
                                  headers={"List-Unsubscribe": f"<{unsub}>",
                                           "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"})
                sent += 1
            except Exception as e:  # noqa: BLE001 - one bad address must not stop the others
                await db.weekly_sends.delete_one({"_id": key})      # not sent, so a later run may try again
                print(f"failed: {a['email']}: {e}", file=sys.stderr)
                failed += 1
    verb = "would send" if args.dry_run else "sent"
    print(f"week {days[0]}..{days[-1]}: {verb} {sent}, already sent {already}, families with no activity {quiet}, "
          f"failed {failed}")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the emails; send and record nothing")
    ap.add_argument("--to", help="only this adult's email (one family)")
    ap.add_argument("--week", help="the Monday (YYYY-MM-DD) of the week to report")
    ap.add_argument("--env-file", help="read settings from this file first (the service's .env)")
    args = ap.parse_args()
    if args.env_file:
        load_env(args.env_file)
    sys.path.insert(0, str(ROOT))
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
