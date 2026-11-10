"""Unhandled server errors (500s): the friendly page a child or parent sees, the log line, and a throttled
email to the operator (config.ALERT_EMAIL): at most one per distinct error per hour and MAX_PER_DAY a day,
each with the day's running count, plus a one-line count of the day before once a day has had any error.

The email says when, where (method and route, never the query string or a token in the path), what (exception
type, message, the last frames of the traceback, no local variables) and who (account, family and child ids,
never a cookie, a password or a form value)."""
import asyncio
import datetime
import logging
import secrets
import traceback
from zoneinfo import ZoneInfo

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from . import config, mailer
from .db import db
from .deps import COOKIE
from .security import token_key

log = logging.getLogger("qz.errors")
EVERY = datetime.timedelta(hours=1)       # one email per distinct error per hour
MAX_PER_DAY = 20
FRAMES = 8

_day = {"date": None, "errors": 0, "emailed": 0, "kinds": set()}
_last: dict = {}                          # error signature -> when it was last emailed
_tasks: set = set()                       # running email tasks (kept so they are not garbage-collected)


def _today() -> datetime.date:
    return datetime.datetime.now(ZoneInfo(config.TIMEZONE)).date()


def _roll() -> dict | None:
    """Start a new day's count when the date has changed; the finished day's count if it had any error."""
    today = _today()
    if _day["date"] == today:
        return None
    done = dict(_day) if _day["date"] and _day["errors"] else None
    _day.update(date=today, errors=0, emailed=0, kinds=set())
    return done


def _spawn(coro) -> None:
    t = asyncio.get_running_loop().create_task(coro)
    _tasks.add(t)
    t.add_done_callback(_tasks.discard)


async def _send(subject: str, body: str) -> None:
    try:
        await mailer.alert(subject, body)
    except Exception:  # noqa: BLE001 - an alert that cannot go out is logged, never raised
        log.exception("could not email the error alert")


def _summary(done: dict) -> tuple[str, str]:
    held = done["errors"] - done["emailed"]
    return (f"[quizocracy] {done['errors']} server errors on {done['date']:%a %d %b}",
            f"Server errors on {done['date']:%A %d %B %Y}: {done['errors']} ({len(done['kinds'])} different), "
            f"{done['emailed']} emailed, {held} not emailed (throttled).\n")


async def daily_count() -> None:
    """Runs for the life of the process: sends the day before's count soon after midnight, if it had errors."""
    while True:
        await asyncio.sleep(600)
        done = _roll()
        if done:
            await _send(*_summary(done))


def _where(tb) -> str:
    """The innermost frame in our own code, which names the error together with its type."""
    frames = traceback.extract_tb(tb)
    ours = [f for f in frames if str(config.BASE_DIR) in f.filename] or frames
    f = ours[-1] if ours else None
    return f"{f.filename.replace(str(config.BASE_DIR.parent) + '/', '')}:{f.lineno} in {f.name}" if f else "?"


async def _who(request: Request) -> str:
    tok = request.cookies.get(COOKIE)
    if not tok:
        return "not signed in"
    try:
        s = await asyncio.wait_for(db.sessions.find_one({"_id": token_key(tok)}), 2)
    except Exception:  # noqa: BLE001 - the database may be what failed
        return "signed in (session not readable)"
    if not s:
        return "no live session"
    return f"account {s.get('account_id')}, family {s.get('family_id')}, child {s.get('child_id') or '-'}"


def _clean(text: str, request: Request) -> str:
    for secret in (request.cookies.get(COOKIE), getattr(config, "SECRET_KEY", None), config.INVITE_CODE):
        if secret and len(secret) >= 6:
            text = text.replace(secret, "[removed]")
    return text


async def report(request: Request, exc: Exception) -> str:
    """Log the error and email it if the throttle allows; returns the reference shown on the error page."""
    ref = secrets.token_hex(3)
    route = getattr(request.scope.get("route"), "path", None) or request.url.path[:80]
    log.error("500 %s %s ref=%s", request.method, route, ref, exc_info=exc)
    done = _roll()
    if done:
        _spawn(_send(*_summary(done)))
    sig = f"{type(exc).__name__} at {_where(exc.__traceback__)}"
    _day["errors"] += 1
    _day["kinds"].add(sig)
    now = datetime.datetime.utcnow()
    if not config.ALERT_EMAIL or _day["emailed"] >= MAX_PER_DAY or now - _last.get(sig, datetime.datetime.min) < EVERY:
        return ref
    _last[sig] = now
    _day["emailed"] += 1
    frames = traceback.extract_tb(exc.__traceback__)
    plumbing = ("/starlette/", "/fastapi/", "/anyio/", "/contextlib.py")      # the web framework's frames say nothing
    tb = "".join(traceback.format_list(([f for f in frames if not any(p in f.filename for p in plumbing)] or frames)[-FRAMES:]))
    local = datetime.datetime.now(ZoneInfo(config.TIMEZONE))
    body = (f"Time:      {local:%Y-%m-%d %H:%M:%S %Z} ({now:%H:%M:%S} UTC)\n"
            f"Request:   {request.method} {route}\n"
            f"Who:       {await _who(request)}\n"
            f"Error:     {type(exc).__name__}: {str(exc)[:500]}\n"
            f"Where:     {_where(exc.__traceback__)}\n"
            f"Reference: {ref} (shown to the user)\n\n"
            f"Last {FRAMES} frames:\n{tb}\n"
            f"Today so far: {_day['errors']} errors ({len(_day['kinds'])} different), this is email "
            f"{_day['emailed']} of at most {MAX_PER_DAY}. The same error is emailed at most once an hour.\n")
    _spawn(_send(f"[quizocracy] 500 {type(exc).__name__} on {request.method} {route}", _clean(body, request)))
    return ref


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#4F46E5">
<title>Something went wrong · Quizocracy</title>
<link rel="icon" href="/static/img/favicon-32.png">
<style>
  /* Self-contained, like offline.html: it must show even when the database or the templates are what failed. */
  :root { --bg:#F7F8FC; --card:#FFFFFF; --line:#E3E6EF; --ink:#111827; --mut:#5B6475; --violet:#4F46E5; color-scheme:light dark; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0B1020; --card:#141B2F; --line:#263049; --ink:#EEF1F8; --mut:#98A2B8; } }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:grid; place-items:center; padding:24px 16px; background:var(--bg); color:var(--ink);
    font:16px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  .card { max-width:420px; width:100%; background:var(--card); border:1px solid var(--line); border-radius:16px; padding:28px 22px; text-align:center; }
  img { width:72px; height:72px; }
  h1 { font-size:1.4rem; margin:.6em 0 .3em; }
  p { color:var(--mut); margin:.4em 0 1.2em; }
  .row { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
  button, a.btn { font:inherit; font-weight:700; color:#fff; background:var(--violet); border:0; border-radius:10px; padding:12px 22px;
    cursor:pointer; text-decoration:none; }
  a.btn.alt { color:var(--violet); background:transparent; border:2px solid var(--violet); padding:10px 20px; }
  small { display:block; margin-top:1.4em; color:var(--mut); }
</style>
</head>
<body>
<div class="card">
  <img src="/static/img/icon-192.png" alt="">
  <h1>Oops, something went wrong</h1>
  <p>It wasn't you: something broke on our side, and we have been told. Please try again in a moment.</p>
  <div class="row"><button type="button" onclick="location.reload()">Try again</button><a class="btn alt" href="/">Back to the start</a></div>
  <small>Reference: REF</small>
</div>
</body>
</html>
"""


async def handler(request: Request, exc: Exception):
    try:
        ref = await report(request, exc)
    except Exception:  # noqa: BLE001 - the page must show whatever happens here
        log.exception("error report failed")
        ref = "-"
    headers = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}
    if request.url.path.startswith("/api/"):
        return JSONResponse({"ok": False, "error": "server", "ref": ref}, status_code=500, headers=headers)
    return HTMLResponse(PAGE.replace("REF", ref), status_code=500, headers=headers)
