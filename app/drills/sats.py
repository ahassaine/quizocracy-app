"""SATs practice papers (Years 5 and 6): short timed papers in the shape of the KS2 tests in May.

Five papers, each shorter than the real one but at its pace: arithmetic and reasoning (maths generators), grammar
and punctuation (the grammar bank: Year 6 skills and the earlier ones the test asks about), spelling (the Years 5
and 6 word list, read by its recorded clip, with its sentence) and reading (one Year 6 passage and all its
questions). Nothing is marked until the end, as in the real tests; then every question shows its answer and why.

A paper's questions are made when it starts and kept on the server with their answers (one item, activity
"sats"); the page shows one question at a time. Answers in a subject of today's plan count as that subject's
answers for the day (src "sats"), so a right one counts towards the target and a missed one is a mistake to put
right, as in the Year 4 check. A question left blank is not counted either way.
"""
import datetime
import json
import random
import re

from ..activities import todays_plan
from ..bank import engine as bank_engine
from ..db import db
from ..maths import maths_engine, maths_mastery
from .. import items, progress
from . import spelling

YEARS = (5, 6)
# arithmetic skills of the maths engine (as on the parent's SATs card)
ARITHMETIC = ["Y6.1.a", "Y6.1.b", "Y6.1.c", "Y6.1.d", "Y6.1.e", "Y6.1.f", "Y6.1.h", "Y6.2.f", "Y6.5.d", "Y6.5.e",
              "Y6.5.f", "Y6.5.g", "Y6.5.h", "Y6.6.f",
              # the fraction calculations the arithmetic paper has
              "Y6.3.e", "Y6.3.f", "Y6.4.a", "Y6.4.b", "Y6.4.d"]
NOT_KS2 = {"Y6.9.j"}          # probability: not in the KS2 programme of study, never on a SATs paper
PAPERS = {
    "arithmetic": {"title": "Maths: arithmetic", "n": 12, "minutes": 10, "subject": "maths",
                   "real": "The real paper: 36 calculations in 30 minutes."},
    "reasoning": {"title": "Maths: reasoning", "n": 8, "minutes": 14, "subject": "maths",
                  "real": "The real papers: about 20 problems in 40 minutes, twice."},
    "gps": {"title": "Grammar and punctuation", "n": 15, "minutes": 12, "subject": "grammar",
            "real": "The real paper: about 50 questions in 45 minutes."},
    "spelling": {"title": "Spelling", "n": 10, "minutes": 7, "subject": "spelling",
                 "real": "The real test: 20 words, each read in a sentence."},
    "reading": {"title": "Reading", "n": 7, "minutes": 15, "subject": "reading",
                "real": "The real paper: 3 texts and about 38 questions in 60 minutes."},
}
ORDER = ["arithmetic", "reasoning", "gps", "spelling", "reading"]
KEEP = 100                    # papers kept on the child's record
SHEETS = 30                   # answer sheets kept per child (the newest)
GRACE = 20                    # seconds after the time is up that a paper's answers are still taken (a slow network)


def open_to(pupil: dict) -> bool:
    return int(pupil.get("year") or 0) in YEARS


def history(pupil: dict) -> list:
    return list(pupil.get("sats_papers") or [])


def cards(pupil: dict) -> list:
    """Each paper with the child's last and best score: [{key, title, n, minutes, real, last, best, tries}]."""
    hist = history(pupil)
    out = []
    for k in ORDER:
        rows = [r for r in hist if r.get("paper") == k]
        out.append({"key": k, **PAPERS[k], "tries": len(rows), "last": rows[-1] if rows else None,
                    "best": max(rows, key=lambda r: (r["score"] / max(1, r["of"]), r["score"])) if rows else None})
    return out


def _reasoning_skills() -> list:
    return [s["key"] for s in maths_engine.skill_list()
            if s["key"].startswith("Y6.") and s["key"] not in ARITHMETIC and s["key"] not in NOT_KS2
            and s["key"] not in maths_mastery.OUT_OF_YEAR            # mode, median and range: KS3
            and s["key"] in maths_engine.GENERATORS]


def _bare(g: dict) -> bool:
    """A bare calculation, as on the arithmetic paper: typed, with at most a few words ("Work out 2,490 ÷ 6")."""
    return (g.get("component") or "number") == "number" and len([w for w in g.get("prompt", "").split() if w.isalpha()]) <= 8


def _spread(keys: list, n: int, rng=random) -> list:
    """n skills, as many different ones as there are, in a shuffled order."""
    keys = list(keys)
    rng.shuffle(keys)
    out = []
    while len(out) < n and keys:
        out += keys[:n - len(out)]
    return out[:n]


async def _maths(pupil: dict, keys: list, bare: bool | None) -> tuple[list, list]:
    """bare: True for the arithmetic paper (bare calculations only), False for reasoning (problems: words or a
    picture, never a bare sum), None for either."""
    pub, ans = [], []
    for k in keys:
        q, made = None, None
        fn = maths_engine.GENERATORS[k]
        for i in range(40):                      # a question of the paper's kind from this skill, if it makes one
            try:
                g = maths_engine.call_generator(fn, random.choice([1, 1, 2]))
            except Exception:  # noqa: BLE001 - one broken generator must not stop the paper
                continue
            if bare is None or _bare(g) == bare:
                made = g
                break
        if made is None:
            continue
        try:
            q = await maths_engine.new_question(k, made.get("difficulty", 1) if isinstance(made.get("difficulty"), int) else 1,
                                                pupil=pupil["_id"], made=made)
        except Exception:  # noqa: BLE001
            q = None
        if not q:
            continue
        pub.append({"kind": "maths", "prompt": q["prompt"], "component": q["component"], "spec": q["spec"]})
        ans.append({"t": "maths", "token": q["token"], "skill": k})
    return pub, ans


def _bank_q(sk: dict, q: dict) -> tuple[dict, dict]:
    pub, key = bank_engine.serve(q)
    return pub, {"t": "bank", "key": key, "skill": sk["key"], "qid": q["id"]}


def _gps(n: int, rng=random) -> tuple[list, list]:
    """n grammar questions: two in three from Year 6 skills, the rest from Years 3 to 5 (the test asks about them);
    one question per skill, never "put spaces between the words" (a Year 1-2 task)."""
    y6 = [s for s in bank_engine.skills("grammar", 6) if s.get("year") == 6]
    early = [s for y in (3, 4, 5) for s in bank_engine.skills("grammar", y) if s.get("year") == y]
    rng.shuffle(y6)
    rng.shuffle(early)
    picked = y6[:round(n * 2 / 3)] + early[:n - round(n * 2 / 3)]
    rng.shuffle(picked)
    pub, ans = [], []
    for sk in picked:
        qs = [q for q in sk["qs"] if not re.match(r"put spaces between", q["q"], re.I)]
        if not qs:
            continue
        p, a = _bank_q(sk, rng.choice(qs))
        pub.append({"kind": "bank", **p})
        ans.append(a)
    return pub, ans


def _spelling(pupil: dict, n: int, rng=random) -> tuple[list, list]:
    words = [w for w in spelling.list_for_year(6) if spelling.has_clip(w)]
    picked = rng.sample(words, min(n, len(words)))
    pub, ans = [], []
    for w in picked:
        cue = spelling.CUES.get(w) or spelling.CUES.get(w.lower()) or ""
        pub.append({"kind": "spelling", "prompt": "Listen, then spell the word.",
                    "sentence": cue if "___" in cue else "", "letters": len(w)})
        ans.append({"t": "spelling", "word": w})
    return pub, ans


async def _reading(pupil: dict, rng=random) -> tuple[list, list, dict | None]:
    """A Year 6 passage this child has not read yet (else the one read longest ago), with all its questions."""
    skills = [s for s in bank_engine.skills("reading", 6) if s.get("year") == 6]
    if not skills:
        return [], [], None
    seen = {d["key"]: d.get("last") or datetime.datetime.min
            async for d in db.bank_mastery.find({"pupil_id": pupil["_id"], "subject": "reading"})}
    done = {r.get("passage") for r in history(pupil) if r.get("paper") == "reading"}
    fresh = [s for s in skills if s["key"] not in seen and s["key"] not in done]
    sk = rng.choice(fresh) if fresh else min(skills, key=lambda s: seen.get(s["key"], datetime.datetime.min))
    pub, ans = [], []
    for q in sk["qs"]:
        p, a = _bank_q(sk, q)
        pub.append({"kind": "bank", **p})
        ans.append(a)
    return pub, ans, {"key": sk["key"], "title": sk["title"], "kind": sk["strand"], "text": sk["text"]}


async def start(pupil: dict, paper: str) -> dict | None:
    if paper not in PAPERS or not open_to(pupil):
        return None
    P, passage = PAPERS[paper], None
    if paper == "arithmetic":
        pub, ans = await _maths(pupil, _spread([k for k in ARITHMETIC if k in maths_engine.GENERATORS], P["n"] + 6), True)
        pub, ans = pub[:P["n"]], ans[:P["n"]]
    elif paper == "reasoning":
        pub, ans = await _maths(pupil, _spread(_reasoning_skills(), P["n"] + 6), False)
        pub, ans = pub[:P["n"]], ans[:P["n"]]
    elif paper == "gps":
        pub, ans = _gps(P["n"])
    elif paper == "spelling":
        pub, ans = _spelling(pupil, P["n"])
    else:
        pub, ans, passage = await _reading(pupil)
    if not pub:
        return None
    secs = P["minutes"] * 60
    token = await items.issue(pupil, "sats", ans, {"paper": paper, "secs": secs,
                                                   "passage": (passage or {}).get("key"),
                                                   # the pictures, kept for the answer sheet
                                                   "shows": [{"component": q.get("component"), "spec": q.get("spec")}
                                                             if q["kind"] == "maths" and q.get("component") not in (None, "number")
                                                             else None for q in pub]})
    return {"token": token, "paper": paper, "title": P["title"], "questions": pub, "seconds": secs,
            **({"passage": passage} if passage else {})}


def _same_word(typed, word: str) -> bool:
    t = re.sub(r"\s+", " ", str(typed or "")).strip().strip(".").replace("’", "'").lower()
    return bool(t) and t == word.lower()


async def bank_progress(pupil: dict, a: dict, correct: bool) -> None:
    """A paper's grammar or reading answer moves that skill's progress, as a daily answer does (the SATs card and the
    strong and weak spots then show the paper's topics as practised). Reading passages keep their first-time
    score (only a first answer is noted)."""
    from ..maths.maths_mastery import MASTERED, gain, penalty
    subject = "reading" if a["skill"].startswith("RD") else "grammar"
    _id = f"{pupil['_id']}:{a['skill']}"
    doc = await db.bank_mastery.find_one({"_id": _id}) or {}
    score, streak = int(doc.get("score", 0)), int(doc.get("streak", 0))
    upd = {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "subject": subject, "key": a["skill"],
           "attempts": int(doc.get("attempts", 0)) + 1, "correct": int(doc.get("correct", 0)) + int(correct),
           "last": datetime.datetime.utcnow()}
    if subject == "reading":
        first = dict(doc.get("first") or {})
        first.setdefault(a["qid"], correct)
        sk = bank_engine.skill(a["skill"]) or {"qs": []}
        ids = {q["id"] for q in sk["qs"]}
        upd.update(first=first, asked=list(dict.fromkeys((doc.get("asked") or []) + [a["qid"]])),
                   score=round(100 * sum(1 for k, v in first.items() if v and k in ids) / max(1, len(ids))))
    else:
        streak = streak + 1 if correct else 0
        upd.update(streak=streak, score=min(MASTERED, score + gain(score, streak)) if correct else max(0, score - penalty(score)))
    await db.bank_mastery.update_one({"_id": _id}, {"$set": upd}, upsert=True)


async def _mark_maths(pupil: dict, a: dict, value) -> dict:
    doc = await db.maths_lab_q.find_one_and_update({"_id": a["token"], "pupil": pupil["_id"]}, {"$set": {"done": True}})
    if not doc:
        return {"correct": False, "expected": "", "why": "", "prompt": ""}
    try:
        ok = value not in (None, "") and maths_engine.check_answer(
            doc["answer_type"], doc["answer"], value, tolerance=doc.get("tolerance", 0), unit=doc.get("unit"),
            prompt=doc.get("prompt", ""), labels=doc.get("labels"))
    except Exception:  # noqa: BLE001 - an answer in a shape the checker does not take is wrong, never a failed paper
        ok = False
    why_extra = ""
    if not ok and isinstance(value, str) and value.strip():
        # a word answer misspelt ("paralel"): the SATs credit a clear spelling of the right word
        try:
            slipped = maths_engine.slipped_words(doc["answer_type"], doc["answer"], value, doc.get("prompt", ""))
        except Exception:  # noqa: BLE001
            slipped = []
        if slipped:
            ok, why_extra = True, "Right! Check the spelling: " + ", ".join(w for _, w in slipped) + "."
    if value not in (None, ""):
        # a paper's maths answer is maths practice too: the skill's progress (and the SATs card) moves with it
        try:
            await maths_mastery.record_attempt(pupil["_id"], a["skill"], bool(ok), value, tier=doc.get("difficulty"),
                                               shape=doc.get("shape"))
        except Exception:  # noqa: BLE001 - the paper's mark matters more than the progress line
            pass
    return {"correct": bool(ok), "expected": str(doc.get("display", doc["answer"])),
            "why": why_extra or " ".join(doc.get("solution") or []), "prompt": doc.get("prompt", ""),
            "layout": doc.get("layout")}


async def finish(pupil: dict, token: str, answers: list, used: int | None, family: dict) -> dict | None:
    """Mark a whole paper. The same paper sent twice (a lost reply) gets its result back, marked once only."""
    it = await items.claim(pupil, "sats", token)
    if not it:
        old = await items.peek(pupil, "sats", token)
        if old and old.get("result"):
            return {**old["result"], "again": True}
        return None
    paper, keys = it["meta"]["paper"], it["answer"]
    late = (datetime.datetime.utcnow() - it["created"]).total_seconds() > it["meta"]["secs"] + GRACE + 60 * 60
    answers = (answers if isinstance(answers, list) else [])[:len(keys)]
    answers += [None] * (len(keys) - len(answers))
    plan = {a["key"] for a in todays_plan(pupil, family)}
    rows, score, blank = [], 0, 0
    for n, (a, v) in enumerate(zip(keys, answers)):
        given = v if v not in ("", [], {}) else None
        if a["t"] == "maths":
            r = await _mark_maths(pupil, a, given)
            activity, detail = "maths", a["skill"]
            gtext = "" if given is None else (json.dumps(given) if isinstance(given, (dict, list)) else str(given))[:200]
        elif a["t"] == "spelling":
            r = {"correct": given is not None and _same_word(given, a["word"]), "expected": a["word"], "why": "",
                 "prompt": "Spell: " + a["word"]}
            activity, detail, gtext = "spelling", a["word"], "" if given is None else str(given)[:60]
            if given is not None and not r["correct"] and spelling.other_word(str(given), a["word"]):
                # a different real word, spelt right ("emergency" for "immediate"): not a spelling mistake
                r["why"] = f"“{str(given).strip()}” is a real word, spelt right, but the word read out was “{a['word']}”."
                r["other"] = True
        else:
            q = bank_engine.question(a["skill"], a["qid"]) or {}
            ok = given is not None and bank_engine.mark(a["key"], given)
            r = {"correct": bool(ok), "expected": bank_engine.expected_text(a["key"]), "why": q.get("why", ""),
                 "prompt": q.get("q", "")}
            if a["key"]["t"] == "tap":
                r["hits"] = a["key"]["hits"]
            if a["key"]["t"] == "mcq" and q.get("opts"):     # every choice, to talk through "why not this one?"
                r["opts"] = list(q["opts"])
            activity = "reading" if a["skill"].startswith("RD") else "grammar"
            detail = f"{a['skill']}#{a['qid']}"
            gtext = "" if given is None else bank_engine.given_text(a["key"], given)
            if a["key"]["t"] in ("tap", "write") and q.get("s"):
                r["prompt"] += " " + q["s"].replace("[", "").replace("]", "")
        r["given"] = gtext
        r["blank"] = given is None
        shows = it["meta"].get("shows") or []
        if n < len(shows) and shows[n]:
            r["show"] = shows[n]
        score += int(r["correct"])
        blank += int(given is None)
        rows.append(r)
        if given is not None and a["t"] == "bank":
            await bank_progress(pupil, a, bool(r["correct"]))
        if given is not None and activity in plan and not late and not r.get("other"):
            # a paper's answer counts for its subject today, like the Year 4 check's (src "sats")
            await progress.record(pupil, activity, r["correct"], None, detail, r["prompt"], r["expected"], gtext,
                                  src="sats")
    secs = it["meta"]["secs"]
    used = max(0, min(int(used), secs)) if isinstance(used, (int, float)) else None
    row = {"paper": paper, "day": progress.today(), "at": datetime.datetime.utcnow(), "score": score,
           "of": len(keys), "blank": blank, "secs": secs, "used": used, "passage": it["meta"].get("passage")}
    before = history(pupil)
    best = max((r["score"] / max(1, r["of"]) for r in before if r.get("paper") == paper), default=None)
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$push": {"sats_papers": {"$each": [row], "$slice": -KEEP}}})
    psk = bank_engine.skill(it["meta"].get("passage") or "") if it["meta"].get("passage") else None
    result = {"paper": paper, "title": PAPERS[paper]["title"], "score": score, "of": len(keys), "blank": blank,
              **({"passage": {"title": psk["title"], "text": psk["text"]}} if psk else {}),
              "used": used, "secs": secs, "rows": rows,
              "best": best is not None and score / max(1, len(keys)) > best, "first": best is None,
              "counted": any(not r["blank"] for r in rows) and PAPERS[paper]["subject"] in plan}
    await db.items.update_one({"_id": it["_id"]}, {"$set": {"result": result}})
    # the answer sheet, kept so the child and a grown-up can go through it later (SHEETS per child)
    sheet = await db.sats_sheets.insert_one({"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "at": row["at"],
                                             "day": row["day"], "result": result})
    old = [d["_id"] async for d in db.sats_sheets.find({"pupil_id": pupil["_id"]}, {"_id": 1}).sort("at", -1).skip(SHEETS)]
    if old:
        await db.sats_sheets.delete_many({"_id": {"$in": old}})
    result["sheet"] = str(sheet.inserted_id)
    return result


async def sheets(pupil: dict, n: int = SHEETS) -> list:
    """The child's answer sheets, newest first: [{id, day, paper, title, score, of}]."""
    return [{"id": str(d["_id"]), "day": d["day"], **{k: d["result"][k] for k in ("paper", "title", "score", "of")}}
            async for d in db.sats_sheets.find({"pupil_id": pupil["_id"]}).sort("at", -1).limit(n)]


async def sheet(pupil: dict, sid: str) -> dict | None:
    from bson import ObjectId
    if not ObjectId.is_valid(sid):
        return None
    d = await db.sats_sheets.find_one({"_id": ObjectId(sid), "pupil_id": pupil["_id"]})
    return {**d["result"], "day": d["day"]} if d else None


async def audio_word(pupil: dict, token: str, i: int) -> str | None:
    """The word of a spelling paper's question i (for its clip), while the paper is open."""
    it = await items.peek(pupil, "sats", token)
    if not it or it.get("done") or it["meta"].get("paper") != "spelling":
        return None
    keys = it["answer"]
    return keys[i]["word"] if 0 <= i < len(keys) else None
