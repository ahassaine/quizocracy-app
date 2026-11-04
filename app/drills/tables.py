"""Times tables: multiplication and division facts, weighted towards the ones a child gets wrong or slow."""
import random

from ..db import db
from .. import items, progress

FAST_MS = 6000


def tables_for_year(year: int) -> list:
    if year <= 2:
        return [2, 5, 10]
    if year == 3:
        return [2, 3, 4, 5, 8, 10]
    return list(range(2, 13))


def _weight(f: dict | None) -> float:
    if not f:
        return 1.5
    w = (1 + 2 * f.get("wrong", 0)) / (1 + f.get("streak", 0)) ** 2
    if (f.get("last_ms") or 0) > FAST_MS:
        w *= 1.5
    return w


async def next_question(pupil: dict) -> dict:
    tabs = tables_for_year(pupil.get("year", 4))
    facts = {d["_id"]: d async for d in db.tables_facts.find({"pupil_id": pupil["_id"]})}
    pool = [(a, b) for a in tabs for b in range(1, 13)]
    weights = [_weight(facts.get(f"{pupil['_id']}:{a}x{b}")) for a, b in pool]
    a, b = random.choices(pool, weights=weights, k=1)[0]
    divide = pupil.get("year", 4) >= 3 and random.random() < 0.3
    if divide:
        prompt, answer = f"{a * b} ÷ {a} =", b
    else:
        x, y = (a, b) if random.random() < 0.5 else (b, a)
        prompt, answer = f"{x} × {y} =", a * b
    token = await items.issue(pupil, "tables", answer, {"fact": f"{a}x{b}", "a": a, "b": b, "prompt": prompt})
    return {"token": token, "prompt": prompt}


async def mastered_count(pupil: dict) -> dict:
    tabs = tables_for_year(pupil.get("year", 4))
    n = await db.tables_facts.count_documents({"pupil_id": pupil["_id"], "streak": {"$gte": 3}, "a": {"$in": tabs}})
    return {"mastered": n, "total": len(tabs) * 12}


async def check(pupil: dict, token: str, value: str, ms: int | None) -> dict | None:
    it = await items.claim(pupil, "tables", token)
    if not it:
        return None
    try:
        correct = int(str(value).strip()) == int(it["answer"])
    except ValueError:
        correct = False
    m = it["meta"]
    fid = f"{pupil['_id']}:{m['fact']}"
    if correct:
        await db.tables_facts.update_one({"_id": fid}, {"$inc": {"right": 1, "streak": 1},
                                         "$set": {"pupil_id": pupil["_id"], "family_id": pupil["family_id"],
                                                  "a": m["a"], "b": m["b"], "last_ms": ms}}, upsert=True)
    else:
        await db.tables_facts.update_one({"_id": fid}, {"$inc": {"wrong": 1}, "$set": {
            "streak": 0, "pupil_id": pupil["_id"], "family_id": pupil["family_id"], "a": m["a"], "b": m["b"],
            "last_ms": ms}}, upsert=True)
    await progress.record(pupil, "tables", correct, ms, m["fact"], m.get("prompt", ""), it["answer"], value)
    return {"correct": correct, "expected": it["answer"]}
