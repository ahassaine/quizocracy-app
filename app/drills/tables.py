"""Times tables: multiplication and division facts, weighted towards the ones a child gets wrong or slow."""
import random
import re

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


async def next_question(pupil: dict, focus: str | None = None) -> dict:
    """focus: a fact such as "7x8" to ask again (a mistake being put right)."""
    tabs = tables_for_year(pupil.get("year", 4))
    m = re.fullmatch(r"(\d+)x(\d+)", focus or "")
    if m:
        a, b = int(m.group(1)), int(m.group(2))
    else:
        facts = {d["_id"]: d async for d in db.tables_facts.find({"pupil_id": pupil["_id"]})}
        shown = await items.just_shown(pupil, "tables")      # a missed fact comes back later, not straight away
        pool = [(a, b) for a in tabs for b in range(1, 13) if f"{a}x{b}" not in shown]
        weights = [_weight(facts.get(f"{pupil['_id']}:{a}x{b}")) for a, b in pool]
        a, b = random.choices(pool, weights=weights, k=1)[0]
    divide = pupil.get("year", 4) >= 2 and random.random() < 0.3
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
    if correct and m["fact"] in await items.just_shown(pupil, "tables"):
        # right, but straight after being shown it: counts for today, not towards the fact's streak or as put right
        await progress.record(pupil, "tables", correct, ms, "", m.get("prompt", ""), it["answer"], value)
        return {"correct": True, "expected": it["answer"], "again_later": True}
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


# Practice for the Multiplication Tables Check (England, Year 4): 25 multiplication questions from the 2 to 12
# tables, MTC_SECONDS each, nothing marked until the end. Like the real check: no 1 times table, few questions on
# the 2 and 10 tables, and more on the 6, 7, 8, 9 and 12 tables.
MTC_N, MTC_SECONDS = 25, 6
MTC_WEIGHT = {2: 0.4, 3: 1, 4: 1, 5: 1, 6: 2.4, 7: 2.4, 8: 2.4, 9: 2.4, 10: 0.4, 11: 1, 12: 2.4}
MTC_EASY_MAX = 2          # at most this many questions with a 2 or a 10 in them
MTC_KEEP = 20             # checks kept on the child's record
TIMED_OUT = "(time ran out)"


def mtc_facts(rng=random) -> list:
    """MTC_N different facts [(a, b)], both numbers drawn with MTC_WEIGHT (7 × 8 and 8 × 7 count as one)."""
    tabs = list(MTC_WEIGHT)
    w = [MTC_WEIGHT[t] for t in tabs]
    out, seen, easy = [], set(), 0
    while len(out) < MTC_N:
        a, b = rng.choices(tabs, weights=w, k=2)
        k = (min(a, b), max(a, b))
        is_easy = bool({a, b} & {2, 10})
        if k in seen or (is_easy and easy >= MTC_EASY_MAX):
            continue
        seen.add(k)
        easy += is_easy
        out.append((a, b))
    return out


async def mtc_start(pupil: dict) -> dict:
    """A new check: one token for all its questions; the answers stay on the server."""
    facts = mtc_facts()
    prompts = [f"{a} × {b} =" for a, b in facts]
    token = await items.issue(pupil, "mtc", [a * b for a, b in facts],
                              {"facts": [f"{a}x{b}" for a, b in facts], "prompts": prompts})
    return {"token": token, "questions": prompts, "seconds": MTC_SECONDS}


async def mtc_finish(pupil: dict, token: str, answers: list, counts: bool) -> dict | None:
    """Mark a whole check. Every fact goes into the times-tables record (a missed one comes up more in practice);
    when `counts` (the plan has times tables today) each answer is also a times-tables answer for the day, so the
    right ones count towards the target and the missed ones are mistakes to put right."""
    it = await items.claim(pupil, "mtc", token)
    if not it:
        return None
    m, score, missed = it["meta"], 0, []
    shown = await items.just_shown(pupil, "tables")     # answers seen in practice a moment ago: no streak, as in check()
    for i, (answer, fact, prompt) in enumerate(zip(it["answer"], m["facts"], m["prompts"])):
        given = answers[i] if i < len(answers) and isinstance(answers[i], dict) else {}
        value = str(given.get("value") or "").strip()[:6]
        ms = given.get("ms")
        ms = max(0, min(int(ms), MTC_SECONDS * 1000)) if isinstance(ms, (int, float)) else MTC_SECONDS * 1000
        correct = value.isdigit() and int(value) == answer
        a, b = (int(x) for x in fact.split("x"))
        inc = {"right": 1, "streak": 1} if correct else {"wrong": 1}
        st = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "a": a, "b": b, "last_ms": ms}
        if not correct:
            st["streak"] = 0
        copied = correct and fact in shown
        if not copied:
            await db.tables_facts.update_one({"_id": f"{pupil['_id']}:{fact}"}, {"$inc": inc, "$set": st}, upsert=True)
        if counts:
            await progress.record(pupil, "tables", correct, ms, "" if copied else fact, prompt, answer, value or TIMED_OUT)
        if correct:
            score += 1
        else:
            missed.append({"prompt": prompt, "answer": answer, "given": value})
    row = {"at": it["created"], "day": progress.today(), "score": score, "of": len(m["facts"]),
           "missed": [x["prompt"] + " " + str(x["answer"]) for x in missed]}
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$push": {"mtc": {"$each": [row], "$slice": -MTC_KEEP}}})
    last = ((pupil.get("mtc") or []) + [row])[-3:]
    return {"score": score, "of": row["of"], "missed": missed, "counted": counts, "last": [r["score"] for r in last]}
