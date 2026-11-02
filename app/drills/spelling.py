"""Spelling from the national-curriculum statutory lists, with spaced repetition (Leitner boxes)."""
import datetime
import json
import random
import re

from ..config import BASE_DIR
from ..db import db
from .. import items, progress

LISTS = json.load(open(BASE_DIR / "data" / "nc_spelling.json", encoding="utf-8"))["lists"]
# Years 7-9: no statutory list exists; these are hand-chosen KS3 lists (see the file's "source").
KS3 = json.load(open(BASE_DIR / "data" / "ks3_spelling.json", encoding="utf-8"))["lists"]
INTERVALS = [0, 1, 3, 7, 21]          # days until the next review, by box
LEARNED_BOX = 3                       # three correct answers on separate days

# Words that sound like other words: the child gets a sentence with a gap. Written by hand.
CUES = {
    "to": "I walk ___ school.", "here": "Come over ___.", "there": "Put it over ___.",
    "where": "___ is my coat?", "our": "This is ___ house.", "hour": "The film lasts an ___.",
    "be": "I want to ___ a vet.", "by": "Sit ___ me.", "I": "___ am happy.", "one": "I have ___ sister.",
    "son": "He is their ___.", "eye": "I closed one ___.", "great": "We had a ___ day.",
    "break": "Be careful not to ___ the glass.", "steak": "He ate a ___ for dinner.",
    "whole": "She ate the ___ cake.", "past": "We walked ___ the shop.", "would": "___ you like some tea?",
    "weight": "What is the ___ of the box?", "heard": "I ___ a noise.", "reign": "The queen's ___ was long.",
    "through": "We walked ___ the park.", "fruit": "An apple is a ___.", "eight": "Two fours make ___.",
    "eighth": "She came ___ in the race.", "forty": "Four tens make ___.", "knight": "The ___ rode a horse.",
    "minute": "Wait a ___.", "flour": "Bread is made with ___.", "great": "We had a ___ day.",
    "breath": "Take a deep ___.", "breathe": "Remember to ___ slowly.", "accept": "I ___ your offer.",
    "principal": "The ___ runs the school.", "aisle": "Walk down the ___.", "prove": "Can you ___ it?",
    "whose": "___ bag is this?", "who": "___ is at the door?", "would": "___ you like some tea?",
    "could": "___ you help me?", "should": "You ___ wear a coat.", "plant": "Water the ___.",
    "past": "We walked ___ the shop.", "dessert": "We had ice cream for ___.",
    "muscle": "Your heart is a ___.", "rhyme": "Cat and hat ___.", "queue": "Wait in the ___.",
    "programme": "We watched a TV ___.", "practise": "I ___ the piano every day.",
    # KS3 lists
    "whether": "I don't know ___ it will rain.", "advice": "Can you give me some ___?",
    "advise": "I ___ you to wear a coat.", "affect": "Will the rain ___ the match?",
    "effect": "The film had a scary ___.", "except": "Everyone came ___ Tom.",
    "stationary": "The car was ___ at the lights.", "stationery": "Pens and paper are ___.",
    "licence": "You need a driving ___.", "personnel": "Hospital ___ wear badges.",
    "wholly": "I am ___ sure.", "quiet": "Please be ___ in the library.",
}


def list_for_year(year: int) -> list:
    if year <= 1:
        return LISTS["Y1"]
    if year == 2:
        return LISTS["Y1"] + LISTS["Y2"]
    if year in (3, 4):
        return LISTS["Y3-4"]
    if year in (5, 6):
        return LISTS["Y5-6"]
    return KS3["Y%d" % min(int(year), 9)]


def audio_file(word: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", word.lower()) + ".mp3"


def _today() -> datetime.date:
    return datetime.date.fromisoformat(progress.today())


async def next_question(pupil: dict) -> dict:
    words = list_for_year(pupil.get("year", 3))
    state = {d["word"]: d async for d in db.spelling_words.find({"pupil_id": pupil["_id"]})}
    last = (pupil.get("_last_spelling") or "")
    today = _today().isoformat()
    due = [w for w in words if w in state and state[w].get("due", "") <= today and w != last]
    new = [w for w in words if w not in state]
    if due:
        due.sort(key=lambda w: (state[w].get("box", 0), state[w].get("due", "")))
        word = due[0]
    elif new:
        word = new[0]
    else:
        word = random.choice([w for w in words if w != last] or words)
    token = await items.issue(pupil, "spelling", word, {"cue": CUES.get(word, "")})
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$set": {"_last_spelling": word}})
    return {"token": token, "audio": f"/api/spelling/audio/{token}", "cue": CUES.get(word, ""),
            "letters": len(word)}


async def check(pupil: dict, token: str, value: str, ms: int | None) -> dict | None:
    it = await items.claim(pupil, "spelling", token)
    if not it:
        return None
    word = it["answer"]
    correct = str(value or "").strip().lower() == word.lower()
    st = await db.spelling_words.find_one({"_id": f"{pupil['_id']}:{word}"}) or {}
    box = int(st.get("box", 0))
    box = min(box + 1, len(INTERVALS) - 1) if correct else 0
    due = (_today() + datetime.timedelta(days=INTERVALS[box] if correct else 0)).isoformat()
    await db.spelling_words.update_one({"_id": f"{pupil['_id']}:{word}"}, {
        "$set": {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "word": word, "box": box, "due": due},
        "$inc": {"right" if correct else "wrong": 1}}, upsert=True)
    await progress.record(pupil, "spelling", correct, ms, word)
    return {"correct": correct, "expected": word}


async def learned_count(pupil: dict) -> dict:
    words = list_for_year(pupil.get("year", 3))
    n = await db.spelling_words.count_documents({"pupil_id": pupil["_id"], "box": {"$gte": LEARNED_BOX},
                                                 "word": {"$in": words}})
    return {"learned": n, "total": len(words)}
