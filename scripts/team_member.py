#!/usr/bin/env python3
"""Manage team-board members. Run from the repo root (reads .env).

  venv/bin/python scripts/team_member.py add --name Meriem --initials MR --role member --telegram 1099165230
  venv/bin/python scripts/team_member.py list
"""
import argparse, datetime, os, secrets, sys
from dotenv import load_dotenv
load_dotenv(".env")
from pymongo import MongoClient

ALPHABET = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
db = MongoClient(os.getenv("QZ_MONGO_URL", "mongodb://127.0.0.1:27017"))[os.getenv("QZ_DB", "qz_dev")]
base = os.getenv("QZ_PUBLIC_URL", "http://127.0.0.1:8311").rstrip("/")

p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
a = sub.add_parser("add")
a.add_argument("--name", required=True); a.add_argument("--initials", required=True)
a.add_argument("--role", default="member", choices=["admin", "member", "bot"]); a.add_argument("--telegram", default="")
t = sub.add_parser("telegram"); t.add_argument("--name", required=True); t.add_argument("--chat", required=True)
sub.add_parser("list")
args = p.parse_args()
if args.cmd == "add":
    slug = "".join(secrets.choice(ALPHABET) for _ in range(10))
    db.team_members.insert_one({"_id": slug, "name": args.name, "initials": args.initials.upper()[:2], "role": args.role,
                                "telegram_chat_id": args.telegram or None, "active": True,
                                "created": datetime.datetime.utcnow()})
    print(f"{args.name} [{args.role}] {base}/team/{slug}")
elif args.cmd == "telegram":
    r = db.team_members.update_one({"name": args.name}, {"$set": {"telegram_chat_id": args.chat}})
    print("updated" if r.modified_count else "no change")
else:
    for m in db.team_members.find().sort("created", 1):
        print(f"{m['initials']:>3} {m['role']:<7} tg={'yes' if m.get('telegram_chat_id') else 'no ':<4} {base}/team/{m['_id']}  {m['name']}")
