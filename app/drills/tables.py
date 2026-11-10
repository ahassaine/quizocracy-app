"""Times tables: multiplication and division facts, weighted towards the ones a child gets wrong or slow."""
import datetime
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


def _near(fact: str, a: int, b: int) -> bool:
    """A fact of the same tables as `fact` ("7x8": the 7 and 8 times tables)."""
    x, y = (int(n) for n in fact.split("x"))
    return bool({a, b} & ({x, y} - {1, 10}))


async def next_question(pupil: dict, focus: str | None = None, near: list | None = None) -> dict:
    """focus: a fact such as "7x8" to ask again (a mistake being put right). near: facts waiting to be put right;
    the question then comes from their tables (7 x 8 waits: the 7 and 8 times tables), not one of them."""
    tabs = tables_for_year(pupil.get("year", 4))
    m = re.fullmatch(r"(\d+)x(\d+)", focus or "")
    if m:
        a, b = int(m.group(1)), int(m.group(2))
    else:
        facts = {d["_id"]: d async for d in db.tables_facts.find({"pupil_id": pupil["_id"]})}
        shown = await items.just_shown(pupil, "tables")      # a missed fact comes back later, not straight away
        last = await items.last_answered(pupil, "tables")    # and no fact twice in a row
        shown |= set(near or []) | {((last or {}).get("meta") or {}).get("fact")}
        shown |= {"x".join(f.split("x")[::-1]) for f in shown if f}       # 8 x 7 is the same fact as 7 x 8
        pool = [(a, b) for a in tabs for b in range(1, 13) if f"{a}x{b}" not in shown]
        close = [(a, b) for a, b in pool if any(_near(f, a, b) for f in near or [])]
        pool = close or pool or [(a, b) for a in tabs for b in range(1, 13)]
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
    return {"mastered": n, "total": len(tabs) * 12, "weakest": weakest_text(await weakest(pupil))}


WEAK_MIN_WRONG = 3        # a table needs this many misses before it is called weak


async def weakest(pupil: dict) -> list:
    """The one or two times tables the child gets wrong most (by share of wrong answers, from WEAK_MIN_WRONG
    misses), worst first: [7, 8]. The 1 and 10 times tables are never named."""
    per: dict = {}
    async for f in db.tables_facts.find({"pupil_id": pupil["_id"]}, {"a": 1, "b": 1, "right": 1, "wrong": 1}):
        for t in {f.get("a"), f.get("b")} - {None, 1, 10}:
            s = per.setdefault(t, [0, 0])
            s[0] += int(f.get("wrong", 0))
            s[1] += int(f.get("right", 0))
    weak = [(w / (w + r), w, t) for t, (w, r) in per.items() if w >= WEAK_MIN_WRONG and w / (w + r) >= 0.2]
    return [t for _, _, t in sorted(weak, reverse=True)[:2]]


def weakest_text(tabs: list) -> str:
    """[7, 8] -> "the 7× and 8× tables"; [7] -> "the 7× table"."""
    if not tabs:
        return ""
    return "the " + " and ".join(f"{t}×" for t in tabs) + (" tables" if len(tabs) > 1 else " table")


# A trick for a fact the child keeps missing, shown with the answer from the second miss on (practice or the
# check). Hand-written ones for the facts children miss most; otherwise a way in from a fact they know (STRATEGY).
TIPS = {
    (3, 4): "1, 2, 3, 4 → 12 = 3 × 4.",
    (6, 6): "6 × 6 = 36. Both sixes: six sixes are thirty-six.",
    (6, 7): "6 × 7: 5 × 7 = 35, and one more 7 makes 42.",
    (6, 8): "6 × 8: 6 × 4 = 24, and double 24 is 48.",
    (6, 12): "6 × 12: 6 × 10 = 60, and 6 × 2 = 12, so 60 + 12 = 72.",
    (7, 7): "7 × 7 = 49: one less than 50.",
    (7, 8): "5, 6, 7, 8 → 56 = 7 × 8. Or: 8 × 6 = 48, and one more 8 makes 56.",
    (7, 12): "7 × 12: 7 × 10 = 70, and 7 × 2 = 14, so 70 + 14 = 84.",
    (8, 8): "8 × 8 = 64. Double 8 three times: 16, 32, 64.",
    (8, 12): "8 × 12: 8 × 10 = 80, and 8 × 2 = 16, so 80 + 16 = 96.",
    (9, 12): "9 × 12: 10 × 12 = 120, take away one 12: 120 − 12 = 108.",
    (11, 12): "11 × 12: 10 × 12 = 120, and one more 12 makes 132.",
    (12, 12): "12 × 12: 10 × 12 = 120, and 2 × 12 = 24, so 120 + 24 = 144.",
}


def tip(a: int, b: int) -> str:
    """The trick for a × b (either way round)."""
    x, y = min(a, b), max(a, b)
    if (x, y) in TIPS:
        return TIPS[(x, y)]
    if 9 in (a, b) and 2 <= x + y - 9 <= 10:
        n = x + y - 9                 # 9 × n, n from 2 to 10: the tens digit is one less than n, the digits make 9
        return (f"9 × {n}: one less than {n} is {n - 1}, and {n - 1} + {9 - (n - 1)} = 9 → {9 * n}."
                if n < 10 else "9 × 10 = 90.")
    for t in (1, 10, 11, 2, 5, 4, 8, 12, 6, 3, 7, 9):
        if t in (a, b):
            n = x + y - t
            return STRATEGY[t](n)
    return f"{a} × {b} = {a * b}."


STRATEGY = {
    1: lambda n: f"Anything times 1 stays the same: 1 × {n} = {n}.",
    10: lambda n: f"Times 10: put a 0 on the end. {n} × 10 = {n * 10}.",
    11: lambda n: (f"Times 11 up to 9: write the number twice. 11 × {n} = {n * 11}." if n <= 9
                   else f"11 × {n}: 10 × {n} = {10 * n}, and one more {n} makes {11 * n}."),
    2: lambda n: f"Times 2 is double: double {n} is {2 * n}.",
    5: lambda n: f"Times 5 is half of times 10: 10 × {n} = {10 * n}, and half of that is {5 * n}.",
    4: lambda n: f"Times 4: double, then double again. {n}, {2 * n}, {4 * n}.",
    8: lambda n: f"Times 8: double three times. {n}, {2 * n}, {4 * n}, {8 * n}.",
    12: lambda n: f"12 × {n}: 10 × {n} = {10 * n}, and 2 × {n} = {2 * n}, so {10 * n} + {2 * n} = {12 * n}.",
    6: lambda n: f"6 × {n}: 5 × {n} = {5 * n}, and one more {n} makes {6 * n}.",
    3: lambda n: f"3 × {n}: double {n} is {2 * n}, and one more {n} makes {3 * n}.",
    7: lambda n: f"7 × {n}: 5 × {n} = {5 * n}, and 2 × {n} = {2 * n}, so {5 * n} + {2 * n} = {7 * n}.",
    9: lambda n: f"9 × {n}: 10 × {n} = {10 * n}, take away one {n}: {9 * n}.",
}


async def misses(pupil: dict, a: int, b: int) -> int:
    """How often this fact was missed, either way round (7 × 8 and 8 × 7)."""
    ids = list({f"{pupil['_id']}:{a}x{b}", f"{pupil['_id']}:{b}x{a}"})
    return sum([int(d.get("wrong", 0)) async for d in db.tables_facts.find({"_id": {"$in": ids}}, {"wrong": 1})])


TIP_AFTER = 2             # the trick shows from this miss of the same fact on


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
        await progress.record(pupil, "tables", correct, ms, m["fact"], m.get("prompt", ""), it["answer"], value,
                              copied=True)
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
    out = {"correct": correct, "expected": it["answer"]}
    if not correct and await misses(pupil, m["a"], m["b"]) >= TIP_AFTER:
        out["hint"] = "Tip: " + tip(m["a"], m["b"])
    return out


# Practice for the Multiplication Tables Check (England, Year 4): 25 multiplication questions from the 2 to 12
# tables, MTC_SECONDS each, nothing marked until the end. Like the real check: no 1 times table, few questions on
# the 2 and 10 tables, and more on the 6, 7, 8, 9 and 12 tables.
MTC_N, MTC_SECONDS = 25, 6
MTC_WEIGHT = {2: 0.4, 3: 1, 4: 1, 5: 1, 6: 2.4, 7: 2.4, 8: 2.4, 9: 2.4, 10: 0.4, 11: 1, 12: 2.4}
MTC_EASY_MAX = 2          # at most this many questions with a 2 or a 10 in them
MTC_KEEP = 100            # checks kept on the child's record (with their dates: a term of daily checks)
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
            await progress.record(pupil, "tables", correct, ms, fact, prompt, answer, value or TIMED_OUT, copied=copied)
        if correct:
            score += 1
        else:
            x = {"prompt": prompt, "answer": answer, "given": value, "fact": fact}
            if await misses(pupil, a, b) >= TIP_AFTER:         # missed before: a trick to remember it by
                x["tip"] = tip(a, b)
            missed.append(x)
    before = pupil.get("mtc") or []
    best = max((r["score"] for r in before), default=None)
    row = {"at": it["created"], "done_at": datetime.datetime.utcnow(), "day": progress.today(), "score": score,
           "of": len(m["facts"]), "missed": [x["prompt"] + " " + str(x["answer"]) for x in missed],
           "facts": [x["fact"] for x in missed]}
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$push": {"mtc": {"$each": [row], "$slice": -MTC_KEEP}}})
    pupil["mtc"] = (before + [row])[-MTC_KEEP:]           # the day's progress, read next, includes this check
    return {"score": score, "of": row["of"], "missed": missed, "counted": counts,
            "last": [r["score"] for r in pupil["mtc"][-3:]], "best": best,
            "new_best": best is not None and score > best, "checks": len(pupil["mtc"])}


def mtc_history(pupil: dict, n: int | None = None) -> list:
    """The child's checks, oldest first ([{day, score, of, best}]; best: the best so far, from the second check
    on), the last n of them."""
    out, best = [], None
    for r in pupil.get("mtc") or []:
        out.append({"day": r.get("day", ""), "score": r["score"], "of": r.get("of", MTC_N),
                    "best": best is not None and r["score"] > best})
        best = r["score"] if best is None else max(best, r["score"])
    return out[-n:] if n else out
