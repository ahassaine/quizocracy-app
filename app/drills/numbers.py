"""Numbers in words (UK style) and words back to numbers."""
import random
import re

from .. import items, progress

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
    s = str(s or "").lower().replace("-", " ").replace(",", " ")
    s = re.sub(r"\band\b", " ", s)
    return " ".join(s.split())


def max_for_year(year: int) -> int:
    return {1: 20, 2: 100, 3: 1000, 4: 10000, 5: 100000}.get(year, 1_000_000)


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


async def next_question(pupil: dict) -> dict:
    n = _pick(pupil.get("year", 3))
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
    if it["meta"]["mode"] == "words":
        correct = _norm(value) == _norm(it["answer"])
    else:
        correct = re.sub(r"[\s,]", "", str(value or "")) == it["answer"]
    n, to_words = it["meta"]["n"], it["meta"]["mode"] == "words"
    await progress.record(pupil, "numbers", correct, ms, str(n),
                          ("Write %s in words" % f"{n:,}") if to_words else ("Write %s in digits" % words(n)), it["answer"], value)
    return {"correct": correct, "expected": it["answer"]}
