#!/usr/bin/env python3
"""After restoring a backup: delete again every family and child that was deleted after that backup was taken.

Run it with the live `deletions` list saved BEFORE the restore (mongoexport it first), or against the same database
when only some collections were restored:
    PYTHONPATH=. venv/bin/python scripts/reapply_deletions.py [--from deletions.json] [--dry-run]
"""
import asyncio, json, sys

from app.db import FAMILY_COLLECTIONS, db
from app.routes.parent import _delete_pupils


async def main(args):
    if "--from" in args:
        rows = [json.loads(l) for l in open(args[args.index("--from") + 1]) if l.strip()]
    else:
        rows = [d async for d in db.deletions.find({}, {"_id": 0})]
    dry = "--dry-run" in args
    pupils = [r["ref"] for r in rows if r["kind"] == "pupil"]
    families = [r["ref"] for r in rows if r["kind"] == "family"]
    pupils += [p["_id"] async for p in db.pupils.find({"family_id": {"$in": families}}, {"_id": 1})]
    print(f"{len(families)} families, {len(set(pupils))} children to delete again" + (" (dry run)" if dry else ""))
    if dry:
        return
    await _delete_pupils(sorted(set(pupils)))
    for c in FAMILY_COLLECTIONS:
        await db[c].delete_many({"family_id": {"$in": families}})
    for c in ("codes", "weekly_sends"):
        await db[c].delete_many({"family_id": {"$in": families}})
    await db.families.delete_many({"_id": {"$in": families}})
    print("done")


asyncio.run(main(sys.argv[1:]))
