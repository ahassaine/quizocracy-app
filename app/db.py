"""MongoDB access. `db` is a Motor database; collections are reached as attributes (db.pupils)."""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from . import config

client = AsyncIOMotorClient(config.MONGO_URL, tz_aware=False, uuidRepresentation="standard")
db = client[config.DB_NAME]

# Every collection that holds a family's data. Deleting a family walks this list.
FAMILY_COLLECTIONS = (
    "accounts", "pupils", "sessions", "attempts", "maths_lab_q", "maths_attempts", "maths_mastery",
    "tables_facts", "spelling_words", "verbs_state", "items",
)


async def ensure_indexes():
    await db.accounts.create_index([("email", ASCENDING)], unique=True)
    await db.accounts.create_index([("family_id", ASCENDING)])
    await db.pupils.create_index([("family_id", ASCENDING)])
    await db.sessions.create_index([("expires", ASCENDING)], expireAfterSeconds=0)
    await db.sessions.create_index([("family_id", ASCENDING)])
    await db.codes.create_index([("expires", ASCENDING)], expireAfterSeconds=0)
    await db.codes.create_index([("email", ASCENDING), ("purpose", ASCENDING)])
    await db.attempts.create_index([("pupil_id", ASCENDING), ("day", ASCENDING), ("activity", ASCENDING)])
    await db.attempts.create_index([("family_id", ASCENDING), ("day", DESCENDING)])
    await db.maths_lab_q.create_index([("created", ASCENDING)], expireAfterSeconds=7 * 86400)
    await db.maths_mastery.create_index([("pupil", ASCENDING)])
    await db.maths_attempts.create_index([("pupil", ASCENDING), ("ts", DESCENDING)])
    for c in ("tables_facts", "spelling_words", "verbs_state", "items"):
        await db[c].create_index([("pupil_id", ASCENDING)])
    await db.items.create_index([("created", ASCENDING)], expireAfterSeconds=2 * 86400)
    await db.login_failures.create_index([("ts", ASCENDING)], expireAfterSeconds=3600)
    await db.outbox.create_index([("to", ASCENDING), ("created", DESCENDING)])
