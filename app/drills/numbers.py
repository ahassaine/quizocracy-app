"""Numbers in words (UK style) and words back to numbers."""
import random
import re

from .. import items, progress
from ..db import db
from . import typos

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
        "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _under_1000(n: int, and_needed: bool) -> str:
    parts = []
    h, r = divmod(n, 100)
    if h:
        parts.append(ONES[h] + " hundred")
    if r:
        if h or and_needed:
            parts.append("and")
        parts.append(ONES[r] if r < 20 else TENS[r // 10] + ("-" + ONES[r % 10] if r % 10 else ""))
    return " ".join(parts)


def words(n: int) -> str:
    """UK English: 2,045 -> 'two thousand and forty-five'."""
    if n == 0:
        return "zero"
    out = []
    millions, rest = divmod(n, 1_000_000)
    thousands, units = divmod(rest, 1000)
    if millions:
        out.append(_under_1000(millions, False) + " million")
    if thousands:
        out.append(_under_1000(thousands, False) + " thousand")
    if units:
        out.append(_under_1000(units, bool(millions or thousands) and units < 100))
    return " ".join(out)


def _norm(s: str) -> str:
    s = str(s or "").lower()
    for ch in "-\u2010\u2011\u2012\u2013\u2014,.!":
        s = s.replace(ch, " ")
    s = re.sub(r"\band\b", " ", s)
    s = re.sub(r"\bnought\b", "zero", s)
    s = re.sub(r"^\s*a\s+(?=hundred\b|thousand\b|million\b)", "one ", s)
    return " ".join(s.split())


def max_for_year(year: int) -> int:
    return {1: 20, 2: 100, 3: 1000, 4: 10000, 5: 1_000_000}.get(year, 10_000_000)


def _pick(year: int) -> int:
    hi = max_for_year(year)
    lo = max(0, hi // 100)
    n = random.randint(lo, hi)
    if hi >= 1000 and random.random() < 0.4:      # tricky zeros: 3,005  40,070
        digits = list(str(n))
        for i in range(1, len(digits)):
            if random.random() < 0.35:
                digits[i] = "0"
        n = int("".join(digits))
    return n


async def next_question(pupil: dict, focus: str | None = None) -> dict:
    """focus: a number to write again (a mistake being put right)."""
    n = int(focus) if str(focus or "").isdigit() else _pick(pupil.get("year", 3))
    to_words = random.random() < 0.65
    if to_words:
        token = await items.issue(pupil, "numbers", words(n), {"mode": "words", "n": n})
        return {"token": token, "mode": "words", "prompt": f"{n:,}", "ask": "Write this number in words"}
    token = await items.issue(pupil, "numbers", str(n), {"mode": "digits", "n": n})
    return {"token": token, "mode": "digits", "prompt": words(n), "ask": "Write this number in digits"}


async def check(pupil: dict, token: str, value: str, ms: int | None) -> dict | None:
    it = await items.claim(pupil, "numbers", token)
    if not it:
        return None
    slipped = []
    if it["meta"]["mode"] == "words":
        correct = _norm(value) == _norm(it["answer"])
        if not correct:                  # the number is right but a word is misspelt: "eigth", "ninty"
            slipped = typos.slips(_norm(value).split(), _norm(it["answer"]).split(), typos.NUMBER_WORDS)
    else:
        correct = re.sub(r"[\s,]", "", str(value or "")) == it["answer"]
    if slipped and not it.get("retried"):
        # one free retry, nothing recorded: the same question stays open
        await db.items.update_one({"_id": it["_id"]}, {"$set": {"done": False, "retried": True}})
        return {"correct": False, "retry": True, "hint": typos.number_hint(slipped)}
    n, to_words = it["meta"]["n"], it["meta"]["mode"] == "words"
    copied = correct and str(n) in await items.just_shown(pupil, "numbers")   # right straight after being shown it
    await progress.record(pupil, "numbers", correct, ms, "" if copied else str(n),
                          ("Write %s in words" % f"{n:,}") if to_words else ("Write %s in digits" % words(n)), it["answer"], value)
    return {"correct": correct, "expected": it["answer"], **({"again_later": True} if copied else {}),
            **({"hint": "Your number was right. " + typos.corrections(slipped)} if slipped else {})}
