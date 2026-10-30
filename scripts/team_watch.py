#!/usr/bin/env python3
"""Wake poll for the team board. Prints one `QZTEAM ...` line per message newer than QZTEAM_SINCE, then
`MARKER <iso>`. Touches no state: the caller keeps the marker and advances it only after printing.
Bot members (Claude's own replies) and status lines are skipped."""
import datetime, os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
from pymongo import MongoClient

db = MongoClient(os.getenv("QZ_MONGO_URL", "mongodb://127.0.0.1:27017"))[os.getenv("QZ_DB", "qz")]
base = os.getenv("QZ_PUBLIC_URL", "https://quizocracy.com").rstrip("/")
try:
    t0 = datetime.datetime.fromisoformat(os.environ.get("QZTEAM_SINCE", "").replace("Z", "+00:00")).replace(tzinfo=None)
except Exception:
    t0 = datetime.datetime.utcnow()
members = {m["_id"]: m for m in db.team_members.find()}
bot = next((k for k, m in members.items() if m.get("role") == "bot"), "")
newest = t0
for m in db.team_messages.find({"time": {"$gt": t0}}).sort("time", 1):
    newest = max(newest, m["time"])
    if m.get("kind") == "system" or members.get(m["author"], {}).get("role") == "bot":
        continue
    t = db.team_threads.find_one({"_id": m["tid"]}) or {}
    text = " ".join((m.get("text") or "").split())[:300]
    n = len(m.get("attachments") or [])
    print(f"QZTEAM {m['time']:%Y-%m-%d %H:%M} {members.get(m['author'], {}).get('name', m['author'])} · «{t.get('title', '')}» — {text}"
          + (f" [+{n} attachment(s)]" if n else "") + f" | {base}/team/{bot}/{m['tid']}")
print("MARKER " + newest.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z")
