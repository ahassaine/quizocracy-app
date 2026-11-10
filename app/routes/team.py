"""Team board for shaping the product (Ali, Meriem, Amine, and Claude as a bot member).

Modelled on the tanafus/tachfinia forums: one shared board, every member has a private unguessable link,
and the link decides who a message is attributed to. New threads and replies ping every other member on
Telegram with the recipient's own link.

  GET  /team/{member}                         thread list
  GET  /team/{member}/new · POST              new thread
  GET  /team/{member}/{tid}                   read a thread
  POST /team/{member}/{tid}/send              reply (reopens a resolved thread)
  POST /team/{member}/{tid}/status            open / awaiting_retest (admin) / resolved
  GET  /team/{member}/{tid}/files/{mid}/{f}   attachment
  GET  /team/{member}/maths · POST next/check  try any maths skill (testing aid; no progress recorded)
  GET  /team/{member}/reports · POST {rid}/status  children's question reports: open / fixed / not a problem
"""
import asyncio
import datetime
import json
import os
import re
import secrets
import urllib.request
from pathlib import Path

from bson import ObjectId
from fastapi import APIRouter, Body, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse

from .. import config, mailer
from ..db import db
from ..maths import maths_engine
from ..web import page
from .child import REPORT_REASONS

router = APIRouter(prefix="/team")
ALPHABET = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
UPLOADS = Path(os.getenv("QZ_DATA_DIR", str(config.BASE_DIR.parent / "data"))) / "team_uploads"
TG_FILE = Path(os.getenv("QZ_TEAM_TG_FILE", os.path.expanduser("~/.quizocracy_feedback_tg.json")))
MAX_FILES, MAX_BYTES = 10, 8 * 1024 * 1024
ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".pdf", ".txt", ".csv", ".log", ".mp4", ".mov", ".webm"}
STATUSES = {"open": "open", "awaiting_retest": "awaiting retest", "resolved": "resolved"}


def gen_slug(n: int) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(n))


def _now():
    return datetime.datetime.utcnow()


async def _member(slug: str) -> dict:
    m = await db.team_members.find_one({"_id": slug, "active": True})
    if not m:
        raise HTTPException(404, "not found")
    return m


async def _thread(tid: str) -> dict:
    t = await db.team_threads.find_one({"_id": tid})
    if not t:
        raise HTTPException(404, "not found")
    return t


def _send_tg(chat_id, text: str) -> None:
    try:
        token = json.loads(TG_FILE.read_text()).get("bot_token", "")
        if not token or not chat_id:
            return
        body = json.dumps({"chat_id": str(chat_id), "text": text[:4000], "parse_mode": "HTML",
                           "disable_web_page_preview": True}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=body,
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=8).read()
    except Exception:
        pass                      # a Telegram outage must never break the board


async def _fanout(author: dict, thread: dict, head: str, snippet: str = "") -> None:
    snippet = " ".join((snippet or "").split())[:200]
    async for m in db.team_members.find({"active": True, "_id": {"$ne": author["_id"]},
                                         "telegram_chat_id": {"$nin": [None, ""]}}):
        url = f"{config.PUBLIC_URL}/team/{m['_id']}/{thread['_id']}"
        lines = [head, f'<a href="{url}">{url}</a>'] + ([f"\n<i>{_esc(snippet)}</i>"] if snippet else [])
        asyncio.create_task(asyncio.to_thread(_send_tg, m["telegram_chat_id"], "\n".join(lines)))


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _real(files) -> list:
    return [f for f in (files or []) if f is not None and (f.filename or "").strip()]


async def _add(request: Request, thread: dict, author: dict, text: str, files: list, kind: str = "msg") -> None:
    text = (text or "").strip()
    mid = ObjectId()
    saved, dropped = [], 0
    for i, up in enumerate(files[:MAX_FILES]):
        ext = os.path.splitext(up.filename)[1].lower()
        blob = await up.read(MAX_BYTES + 1)
        if ext not in ALLOWED or not blob or len(blob) > MAX_BYTES:
            dropped += 1
            continue
        d = UPLOADS / thread["_id"] / str(mid)
        d.mkdir(parents=True, exist_ok=True)
        name = f"{i:02d}-" + (re.sub(r"[^A-Za-z0-9._-]+", "_", os.path.basename(up.filename)).strip("._-")[:80] or "file")
        (d / name).write_bytes(blob)
        saved.append(name)
    if dropped:
        text += f"\n\n[{dropped} file(s) not attached: unsupported type or over {MAX_BYTES // 2**20} MB]"
    now = _now()
    await db.team_messages.insert_one({"_id": mid, "tid": thread["_id"], "author": author["_id"], "kind": kind,
                                       "text": text[:10000], "attachments": saved, "time": now,
                                       "ip": request.headers.get("x-forwarded-for", "").split(",")[0].strip()})
    await db.team_threads.update_one({"_id": thread["_id"]}, {
        "$set": {"last_at": now, "last_author": author["_id"],
                 "last_preview": (text or f"[{len(saved)} files]")[:140]}, "$inc": {"count": 1}})


async def _names() -> dict:
    return {m["_id"]: m async for m in db.team_members.find({})}


@router.get("/{member_slug}")
async def threads(request: Request, member_slug: str, open: int = 0):
    me = await _member(member_slug)
    q = {"status": {"$ne": "resolved"}} if open else {}
    ts = [t async for t in db.team_threads.find(q).sort("last_at", -1).limit(500)]
    members = [m async for m in db.team_members.find({"active": True, "role": {"$ne": "bot"}}).sort("created", 1)]
    return page(request, "team/list.html", me=me, threads=ts, members=members, names=await _names(),
                open_only=bool(open), statuses=STATUSES,
                reports_open=await db.reports.count_documents({"status": "open"}))


@router.get("/{member_slug}/new")
async def new_form(request: Request, member_slug: str):
    return page(request, "team/new.html", me=await _member(member_slug))


@router.post("/{member_slug}/new")
async def new_thread(request: Request, member_slug: str, title: str = Form(""), text: str = Form(""),
                     files: list[UploadFile] = File(default=[])):
    me = await _member(member_slug)
    files = _real(files)
    title, text = title.strip(), text.strip()
    if not (title or text or files):
        return RedirectResponse(f"/team/{member_slug}/new", 303)
    title = (title or text.split("\n", 1)[0] or "(untitled)")[:200]
    tid = gen_slug(6)
    now = _now()
    t = {"_id": tid, "title": title, "author": me["_id"], "status": "open", "created": now, "last_at": now,
         "last_author": me["_id"], "last_preview": "", "count": 0}
    await db.team_threads.insert_one(t)
    await _add(request, t, me, text or f"({len(files)} attachments)", files)
    await _fanout(me, t, f"[quizocracy team] 🆕 «{_esc(title[:80])}» — {_esc(me['name'])}", text)
    return RedirectResponse(f"/team/{member_slug}/{tid}", 303)


@router.get("/{member_slug}/maths")
async def maths_try(request: Request, member_slug: str):
    """Testing aid: open any maths skill directly instead of waiting for the app to pick it."""
    me = await _member(member_slug)
    years = {}
    for s in maths_engine.skill_list():
        years.setdefault(s["key"].split(".")[0], []).append(s)
    return page(request, "team/maths.html", me=me, years=years)


@router.post("/{member_slug}/maths/next")
async def maths_try_next(member_slug: str, payload: dict = Body(default={})):
    me = await _member(member_slug)
    key = str(payload.get("skill") or "")
    diff = payload.get("difficulty") if payload.get("difficulty") in (0, 1, 2) else 1
    q = await maths_engine.new_question(key, diff, pupil="team:" + me["_id"])
    if not q:
        raise HTTPException(404, "no such skill")
    meta = next((s for s in maths_engine.skill_list() if s["key"] == key), {})
    return {"ok": True, **q, "skill": key, "title": meta.get("title", key), "strand": meta.get("strand", "")}


@router.post("/{member_slug}/maths/check")
async def maths_try_check(member_slug: str, payload: dict = Body(default={})):
    me = await _member(member_slug)
    res = await maths_engine.check(payload.get("token"), payload.get("value"), "team:" + me["_id"])
    res.pop("prompt", None)
    return res


REPORT_STATUSES = {"open": "open", "fixed": "fixed", "not_a_problem": "not a problem"}


@router.get("/{member_slug}/reports")
async def reports(request: Request, member_slug: str, status: str = "open"):
    """Children's "Something wrong with this question?" reports, newest first (written by routes/child.py)."""
    me = await _member(member_slug)
    q = {"status": status} if status in REPORT_STATUSES else {}
    rs = [r async for r in db.reports.find(q).sort("ts", -1).limit(300)]
    for r in rs:
        r["served_text"] = json.dumps(r.get("served"), ensure_ascii=False, indent=1, default=str)
    counts = {s: await db.reports.count_documents({"status": s}) for s in REPORT_STATUSES}
    return page(request, "team/reports.html", me=me, reports=rs, status=status if q else "all",
                statuses=REPORT_STATUSES, counts=counts, reasons=REPORT_REASONS)


REPORT_OUTCOME_MAIL = {"fixed": "We fixed it. Thank you: reports like this make the questions better.",
                       "not_a_problem": "We checked it: the question and its answer are right."}


@router.post("/{member_slug}/reports/{rid}/status")
async def report_status(member_slug: str, rid: str, status: str = Form(...), back: str = Form("open"),
                        reply: str = Form("")):
    """Set a report's status, with an optional short note for the family. The family sees the outcome on the
    child's progress page; the grown-ups who ticked "Email me" in Settings also get it by email, once."""
    me = await _member(member_slug)
    if status not in REPORT_STATUSES or not ObjectId.is_valid(rid):
        raise HTTPException(400, "bad status")
    r = await db.reports.find_one({"_id": ObjectId(rid)})
    if not r:
        raise HTTPException(404, "not found")
    upd = {"status": status, "by": me["_id"], "status_at": _now()}
    if reply.strip() or status == "open":
        upd["reply"] = " ".join(reply.split())[:300]
    await db.reports.update_one({"_id": r["_id"]}, {"$set": upd})
    p = await db.pupils.find_one({"_id": r.get("pupil_id")}, {"name": 1})
    if status in REPORT_OUTCOME_MAIL and p and not r.get("mailed_" + status):
        await db.reports.update_one({"_id": r["_id"]}, {"$set": {"mailed_" + status: _now()}})
        note = upd.get("reply") or r.get("reply") or ""
        q = " ".join(str((r.get("served") or {}).get("prompt") or r.get("expected") or "").split())[:120]
        if r.get("activity") == "spelling" and r.get("expected"):    # every spelling question has the same prompt
            q = f"Spell the word: {r['expected']}"
        who = r.get("by_name") or p["name"]          # a grown-up's report from "Mistakes to go over", or the child's
        await mailer.to_family(r["family_id"], f"We checked the question {who} reported",
                               f"Hello,\n\n{who} reported a question"
                               + (f" from {p['name']}'s practice" if r.get("by_name") else "") + f" on {r['ts']:%d %B}"
                               + (f": “{q}”" if q else "") + (f" (“{r['note']}”)" if r.get("note") else "") + ".\n\n"
                               + REPORT_OUTCOME_MAIL[status] + (f"\n\nA note from us: {note}" if note else "")
                               + f"\n\nSee {p['name']}'s reports on the progress page: "
                               f"{config.PUBLIC_URL}/children/{r['pupil_id']}#reports\n\n"
                               f"You get this email because you ticked it in Settings: {config.PUBLIC_URL}/settings#login\n",
                               roles=("owner", "parent", "carer"), flag="report_emails")
    return RedirectResponse(f"/team/{member_slug}/reports?status={back if back in REPORT_STATUSES else 'all'}#r{rid}", 303)


@router.get("/{member_slug}/{tid}")
async def thread(request: Request, member_slug: str, tid: str):
    me = await _member(member_slug)
    t = await _thread(tid)
    msgs = [m async for m in db.team_messages.find({"tid": tid}).sort([("time", 1), ("_id", 1)]).limit(2000)]
    return page(request, "team/thread.html", me=me, t=t, msgs=msgs, names=await _names(), statuses=STATUSES,
                empty=request.query_params.get("empty"))


@router.post("/{member_slug}/{tid}/send")
async def send(request: Request, member_slug: str, tid: str, text: str = Form(""),
               files: list[UploadFile] = File(default=[])):
    me = await _member(member_slug)
    t = await _thread(tid)
    files = _real(files)
    if not text.strip() and not files:
        return RedirectResponse(f"/team/{member_slug}/{tid}?empty=1", 303)
    if t["status"] == "resolved":
        await db.team_threads.update_one({"_id": tid}, {"$set": {"status": "open"}})
    await _add(request, t, me, text, files)
    await _fanout(me, t, f"[quizocracy team] 💬 {_esc(me['name'])} on «{_esc(t['title'][:80])}»", text)
    return RedirectResponse(f"/team/{member_slug}/{tid}#end", 303)


@router.post("/{member_slug}/{tid}/status")
async def status(request: Request, member_slug: str, tid: str, status: str = Form(...)):
    me = await _member(member_slug)
    t = await _thread(tid)
    if status not in STATUSES:
        raise HTTPException(400, "bad status")
    if status == "awaiting_retest" and me["role"] not in ("admin", "bot"):
        raise HTTPException(403, "not allowed")
    await db.team_threads.update_one({"_id": tid}, {"$set": {"status": status}})
    await _add(request, t, me, f"— status changed to {STATUSES[status]} —", [], kind="system")
    await _fanout(me, t, f"[quizocracy team] {STATUSES[status]} — «{_esc(t['title'][:80])}» (by {_esc(me['name'])})")
    return RedirectResponse(f"/team/{member_slug}/{tid}", 303)


@router.get("/{member_slug}/{tid}/files/{mid}/{name}")
async def attachment(member_slug: str, tid: str, mid: str, name: str):
    await _member(member_slug)
    await _thread(tid)
    if not re.fullmatch(r"[0-9a-f]{24}", mid) or "/" in name or ".." in name:
        raise HTTPException(400)
    f = UPLOADS / tid / mid / name
    if not f.is_file():
        raise HTTPException(404)
    return FileResponse(str(f))
