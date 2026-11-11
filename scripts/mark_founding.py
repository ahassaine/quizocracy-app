"""Mark every family that signed up before founding families existed (11 Nov 2026) as a founding family.
Adds `founding: True` only where the field is missing; nothing else changes. --dry-run shows the count only.
Usage: venv/bin/python scripts/mark_founding.py [--dry-run]"""
import asyncio, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))
from app.db import db


async def main():
    q = {"founding": {"$exists": False}}
    n = await db.families.count_documents(q)
    if "--dry-run" in sys.argv:
        print(f"{n} families would be marked founding"); return
    r = await db.families.update_many(q, {"$set": {"founding": True}})
    print(f"marked {r.modified_count} of {n} families founding")

asyncio.run(main())
