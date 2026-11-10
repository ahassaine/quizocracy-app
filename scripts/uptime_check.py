#!/usr/bin/env python3
"""Uptime check for quizocracy.com, run by cron on ANOTHER machine every 5 minutes (deploy/UPTIME.md).

    python3 uptime_check.py                          # check, tell only when the state changes
    python3 uptime_check.py --verbose                # also print every run's results
    python3 uptime_check.py --base http://127.0.0.1:8344 --state /tmp/qz_up.json      # another server

Fetches /healthz (which pings the database: 503 when it is down), /, /login and one static file, each with a
timeout. The site is DOWN after --fails runs in a row with any check failing (2 by default, so one slow
moment is not an alarm) and UP again at the first run where every check passes. Only those two changes are
reported, with each check's status and time and, when it comes back, how long it was down.

Reporting: by SMTP when a host is given (--smtp-host or UPTIME_SMTP_HOST; port, user and sender likewise,
password only from UPTIME_SMTP_PASSWORD), to --to / UPTIME_TO. Without a host the report is printed, so cron
mails it to MAILTO; a run with nothing to report prints nothing. Standard library only; the state is a small
JSON file. Always exits 0 unless the arguments are wrong, so cron does not mail its own failures.
"""
import argparse
import datetime
import json
import os
import pathlib
import smtplib
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from email.message import EmailMessage
from email.utils import formatdate

PATHS = ("/healthz", "/", "/login", "/static/img/logo.png")


def check(base: str, path: str, timeout: float) -> dict:
    """One fetch: {path, ok, status, ms, error}. A check passes on HTTP 200 (and, for /healthz, "ok": true)."""
    t0 = time.monotonic()
    req = urllib.request.Request(base + path, headers={"User-Agent": "qz-uptime/1"})
    status, err = None, ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, body = r.status, r.read(65536)
        if path == "/healthz" and not json.loads(body or b"{}").get("ok"):
            err = "healthz says not ok"
    except urllib.error.HTTPError as e:
        status, err = e.code, (e.read(300).decode("utf-8", "replace").strip() or e.reason)
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ssl.SSLError, ValueError) as e:
        err = str(getattr(e, "reason", e)) or type(e).__name__
    ms = int((time.monotonic() - t0) * 1000)
    return {"path": path, "ok": status == 200 and not err, "status": status, "ms": ms, "error": str(err)[:200]}


def table(results: list) -> str:
    return "\n".join(f"  {'ok  ' if r['ok'] else 'FAIL'} {r['path']:<22} {r['status'] or '---'}  {r['ms']:>6} ms"
                     + (f"  {r['error']}" if r["error"] else "") for r in results)


def load_state(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {"state": "up", "fails": 0, "since": None}


def save_state(path: pathlib.Path, st: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(st))
    tmp.replace(path)


def report(args, subject: str, body: str) -> None:
    if not args.smtp_host:
        print(f"{subject}\n\n{body}")
        return
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = args.sender, args.to, subject
    msg["Date"] = formatdate(localtime=True)
    msg.set_content(body)
    try:
        smtp = smtplib.SMTP_SSL if args.smtp_port == 465 else smtplib.SMTP
        with smtp(args.smtp_host, args.smtp_port, timeout=20) as s:
            if args.smtp_port != 465 and args.smtp_user:          # never send a password in the clear
                s.starttls(context=ssl.create_default_context())
            if args.smtp_user:
                s.login(args.smtp_user, os.getenv("UPTIME_SMTP_PASSWORD", ""))
            s.send_message(msg)
    except (OSError, smtplib.SMTPException) as e:          # the mail could not go: let cron's MAILTO carry it
        print(f"{subject}\n\n{body}\n(SMTP failed: {e})")


def ago(since: str | None, now: datetime.datetime) -> str:
    if not since:
        return "unknown"
    mins = int((now - datetime.datetime.fromisoformat(since)).total_seconds() // 60)
    return f"{mins // 60} h {mins % 60} min" if mins >= 60 else f"{mins} min"


def main(argv=None) -> int:
    env = os.getenv
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default=env("UPTIME_BASE", "https://quizocracy.com"))
    ap.add_argument("--timeout", type=float, default=float(env("UPTIME_TIMEOUT", "10")))
    ap.add_argument("--fails", type=int, default=2, help="failed runs in a row before it counts as down")
    ap.add_argument("--state", default=env("UPTIME_STATE", str(pathlib.Path.home() / ".cache/qz_uptime.json")))
    ap.add_argument("--smtp-host", default=env("UPTIME_SMTP_HOST", ""))
    ap.add_argument("--smtp-port", type=int, default=int(env("UPTIME_SMTP_PORT", "25")))
    ap.add_argument("--smtp-user", default=env("UPTIME_SMTP_USER", ""))
    ap.add_argument("--from", dest="sender", default=env("UPTIME_FROM", "uptime@quizocracy.com"))
    ap.add_argument("--to", default=env("UPTIME_TO", ""))
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)
    if args.smtp_host and not args.to:
        ap.error("--to (or UPTIME_TO) is needed with an SMTP host")
    base = args.base.rstrip("/")
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    results = [check(base, p, args.timeout) for p in PATHS]
    ok = all(r["ok"] for r in results)
    path = pathlib.Path(args.state)
    st = load_state(path)
    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    if args.verbose:
        print(f"{base} {stamp}: {'all ok' if ok else 'failing'} (state {st['state']}, failed runs {st['fails']})\n{table(results)}")
    if ok:
        if st["state"] == "down":
            report(args, f"[UP] {base} is back",
                   f"{base} answers again at {stamp}, after about {ago(st.get('since'), now)} down.\n\n{table(results)}\n")
        st = {"state": "up", "fails": 0, "since": now.isoformat()} if st["state"] == "down" or not st.get("since") \
            else {**st, "fails": 0}
    else:
        st["fails"] = st.get("fails", 0) + 1
        if st["state"] == "up" and st["fails"] >= args.fails:
            failed = ", ".join(f"{r['path']} ({r['status'] or r['error']})" for r in results if not r["ok"])
            report(args, f"[DOWN] {base}: {failed}",
                   f"{base} has failed {st['fails']} checks in a row (every 5 minutes), the latest at {stamp}.\n\n"
                   f"{table(results)}\n\nA 503 on /healthz means the app runs but its database does not answer.\n"
                   f"You will get one more email when it is back.\n")
            st.update(state="down", since=now.isoformat())
    save_state(path, st)
    return 0


if __name__ == "__main__":
    sys.exit(main())
