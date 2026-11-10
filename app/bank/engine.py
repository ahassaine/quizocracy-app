"""Hand-written question banks (grammar and punctuation, science): loading, serving and marking.

The content lives in app/bank/content/*.py (format in SPEC.md). A question is served without its answer;
what is needed to mark it stays on the server with the item (see app/items.py).
"""
import hashlib
import importlib
import logging
import pathlib
import random
import re

from ..drills import typos
from . import excluded

log = logging.getLogger("qz.bank")
CONTENT = pathlib.Path(__file__).parent / "content"
PREFIX = {"grammar": "GP", "science": "SC"}

_BANK: dict | None = None      # {subject: {year: [skill, ...]}}
_BY_KEY: dict = {}


def _qid(skill_key: str, q: dict) -> str:
    """The id a question was served under before ids were written in the content (10 Nov 2026): a hash of its
    text, so an edit gave it a new one. scripts/bank_ids.py --legacy wrote these into the files; the engine only
    falls back to it for a question added since without an id (the lint fails on that)."""
    sig = "|".join([skill_key, q.get("t", ""), q.get("q", ""), q.get("s", ""), *map(str, q.get("opts", []))])
    return hashlib.sha1(sig.encode()).hexdigest()[:12]


def tap_parse(s: str):
    """'The dog ran [quickly] home.' -> (['The', 'dog', 'ran', 'quickly', 'home.'], [3])"""
    words, hits = [], []
    for i, tok in enumerate(s.split()):
        m = re.fullmatch(r"([^\[\]]*)\[([^\[\]]+)\]([^\[\]]*)", tok)
        if m:
            hits.append(i)
            tok = m.group(1) + m.group(2) + m.group(3)
        words.append(tok)
    return words, hits


def _usable(q: dict) -> bool:
    t = q.get("t")
    if t == "mcq":
        return isinstance(q.get("opts"), list) and 2 <= len(q["opts"]) <= 4
    if t == "tap":
        return bool(tap_parse(q.get("s", ""))[1])
    if t in ("text", "write"):
        return isinstance(q.get("a"), list) and bool(q["a"])
    if t == "num":
        return isinstance(q.get("a"), (int, float))
    return False


def load() -> dict:
    """Read every content module once. A question that cannot be marked is left out (the lint reports it)."""
    global _BANK
    if _BANK is not None:
        return _BANK
    bank: dict = {s: {} for s in PREFIX}
    for path in sorted(CONTENT.glob("*.py")):
        if path.stem == "__init__":
            continue
        try:
            mod = importlib.import_module(f"app.bank.content.{path.stem}")
        except Exception:  # noqa: BLE001 - one broken file must not take the app down
            log.exception("bank content %s does not load", path.stem)
            continue
        for sk in getattr(mod, "SKILLS", []):
            if sk.get("key") in excluded.SKILLS:
                continue
            subject = next((s for s, p in PREFIX.items() if str(sk.get("key", "")).startswith(p)), None)
            out = excluded.QUESTIONS.get(sk.get("key"), set())
            qs = [q if q.get("id") else dict(q, id=_qid(sk["key"], q))     # the id is permanent (SPEC.md)
                  for q in sk.get("qs", []) if _usable(q) and q.get("q") not in out]
            if any(not q.get("id") for q in sk.get("qs", [])):
                log.warning("bank skill %s has questions without an id: run scripts/bank_ids.py", sk.get("key"))
            if subject == "science":                 # "the axle" is as right as "axle" (not so in grammar)
                qs = [dict(q, loose=True) if q["t"] == "text" else q for q in qs]
            if not subject or not qs:
                continue
            skill = {**sk, "qs": qs, "subject": subject}
            bank[subject].setdefault(int(sk["year"]), []).append(skill)
            _BY_KEY[sk["key"]] = skill
    for years in bank.values():
        for lst in years.values():
            lst.sort(key=lambda s: s["key"])
    _BANK = bank
    return bank


def skills(subject: str, year: int) -> list:
    """The skills of one year, in teaching order. A year with no bank falls back to the nearest year below."""
    years = load()[subject]
    if not years:
        return []
    ys = [y for y in years if y <= int(year or 1)] or [min(years)]
    return years[max(ys)]


def bank_year(subject: str, year: int) -> int:
    years = load()[subject]
    ys = [y for y in years if y <= int(year or 1)] or [min(years or [1])]
    return max(ys)


def skill(key: str) -> dict | None:
    load()
    return _BY_KEY.get(key)


def question(key: str, qid: str) -> dict | None:
    sk = skill(key)
    return next((q for q in sk["qs"] if q["id"] == qid), None) if sk else None


def serve(q: dict) -> tuple[dict, dict]:
    """(what the child sees, what marking needs). The answer is never in the first."""
    t = q["t"]
    pub = {"kind": t, "prompt": q["q"]}
    key: dict = {"t": t}
    if t == "mcq":
        order = list(range(len(q["opts"])))
        random.shuffle(order)
        pub["opts"] = [q["opts"][i] for i in order]
        key["right"] = order.index(0)
        key["opts"] = pub["opts"]
    elif t == "tap":
        words, hits = tap_parse(q["s"])
        pub["words"] = words
        key["hits"] = hits
        key["words"] = words
    elif t == "text":
        key["a"] = q["a"]
        full = gap_sentences(q["q"], q["a"])
        if full:
            pub["gap"] = True
            key["full"] = full
        if q.get("loose"):
            key["loose"] = True
    elif t == "write":
        pub["s"] = q["s"]
        key["a"] = q["a"]
        if open_end(q["q"], q["s"]):
            key["open_end"] = True
    elif t == "num":
        pub["unit"] = q.get("unit", "")
        key["a"], key["tol"] = q["a"], q.get("tol", 0)
    return pub, key


_BLANKS = re.compile(r"[A-Za-z]*_{2,}(?:\s+_{2,})*(?:\s*\([^)]*\))?")   # "___ ___", "v_____", "___ (cry)"


def gap_sentences(prompt: str, answers: list) -> list:
    """The sentence with the gap filled in, for each accepted answer:
    "Make ... passive: 'Hands ___ ___ ___.'" + "must be washed" -> "Hands must be washed.";
    "To keep healthy, eat lots of fruit and v_____." + "vegetables" -> the whole sentence.
    A child who types the whole sentence back, not only the missing words, is right too."""
    quoted = [f for f in re.findall(r"'([^']*_{2,}[^']*)'|\"([^\"]*_{2,}[^\"]*)\"", prompt) for f in f if f]
    if quoted:
        frame = quoted[-1]
    else:
        frame = prompt.rsplit(":", 1)[-1] if "_" in prompt.rsplit(":", 1)[-1] else prompt
        frame = next((x for x in re.split(r"(?<=[.?!])\s+", frame.strip()) if "__" in x), "")
    if len(_BLANKS.findall(frame)) != 1:
        return []
    return [" ".join(_BLANKS.sub(lambda m: a, frame).split()) for a in answers]


def _quotes(s: str) -> str:
    return (str(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
            .replace("…", "...").replace("–", "-").replace("—", "-"))


def norm_text(s: str) -> str:
    s = " ".join(_quotes(s).lower().split())
    return s.rstrip(".?!").strip() or s               # a short answer's end mark does not matter (unless it IS the answer: "?")


def loose(s: str) -> str:
    """Science: "the non-contact force" = "non contact force" = "noncontact force"."""
    return re.sub(r"[\s-]+", "", re.sub(r"^(a|an|the) (?=\S)", "", s))


def norm_write(s: str) -> str:
    s = " ".join(_quotes(s).split())
    return re.sub(r"\s+([,.;:!?])", r"\1", s)        # "Hello , Sam" counts as "Hello, Sam"


_END_MARKS = re.compile(r"full stop|punctuat|end mark|question mark|exclamation|capital letter", re.I)


def open_end(prompt: str, s: str) -> bool:
    """A "write" sentence given without an end mark, in a task that is not about end marks ("Add a colon",
    "Add a clause starting with 'because'"): the full stop it never asked for may be left out."""
    return not _quotes(s).rstrip().rstrip("'\"").endswith((".", "?", "!")) and not _END_MARKS.search(prompt)


_WORD_NUM = {w: float(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}


def parse_num(s) -> float | None:
    """One number, with digit-group commas or spaces and a unit if the child likes ("10 000 kJ", "6 m").
    A hedge or a range is not one number: "25 or 30", "6-9", "6/7", "1.4.9" give None."""
    s = _quotes("" if s is None else str(s)).strip().replace("−", "-")
    if s.lower() in _WORD_NUM:                       # "two" for 2: the number is the answer, not how it is written
        return _WORD_NUM[s.lower()]
    m = re.match(r"^[-+]?(?:\d{1,3}(?:[, ]\d{3})+(?!\d)|\d+)(?:\.\d+)?|^[-+]?\.\d+", s)
    if not m or re.search(r"\d", s[m.end():]):
        return None
    return float(re.sub(r"[, ]", "", m.group(0)))


def fmt_num(x) -> str:
    return ("%g" % x) if isinstance(x, float) else str(x)


def expected_text(key: dict) -> str:
    t = key["t"]
    if t == "mcq":
        return key["opts"][key["right"]]
    if t == "tap":
        return ", ".join(re.sub(r"^\W+|\W+$", "", key["words"][i]) for i in key["hits"])
    if t in ("text", "write"):
        return key["a"][0]
    return fmt_num(key["a"])


def given_text(key: dict, value) -> str:
    t = key["t"]
    try:
        if t == "mcq":
            return key["opts"][int(value)]
        if t == "tap":
            return ", ".join(re.sub(r"^\W+|\W+$", "", key["words"][int(i)]) for i in sorted(set(value or [])))
    except (TypeError, ValueError, IndexError):
        return ""
    return str(value or "")[:200]


def mark(key: dict, value) -> bool:
    t = key["t"]
    if t == "mcq":
        try:
            return int(value) == key["right"]
        except (TypeError, ValueError):
            return False
    if t == "tap":
        try:
            return sorted({int(i) for i in (value or [])}) == sorted(key["hits"])
        except (TypeError, ValueError):
            return False
    if t == "text":
        v = norm_text(value)
        ok = key["a"] + key.get("full", [])
        if key.get("loose"):
            return bool(loose(v)) and loose(v) in {loose(norm_text(a)) for a in ok}
        return bool(v) and v in {norm_text(a) for a in ok}
    if t == "write":
        v = norm_write(value)
        ok = {norm_write(a) for a in key["a"]}
        if key.get("open_end"):
            v, ok = v.rstrip(". "), {a.rstrip(". ") for a in ok}
        return bool(v) and v in ok
    if t == "num":
        v = parse_num(value)
        return v is not None and abs(v - float(key["a"])) <= float(key.get("tol") or 0) + 1e-9
    return False


_NEVER = frozenset({"yes", "no"})


def slips(key: dict, value, prompt: str = "") -> list:
    """Science words typed with one slip ("respiraton", "ded"): [(typed, wanted)] against the nearest accepted
    answer, for a free retry. Never in grammar, where how a word is written is often the point, and never a word
    the question itself offers ("living, dead or never alive?")."""
    if key.get("t") != "text" or not key.get("loose"):
        return []
    words = lambda s: re.findall(r"[a-z]+", re.sub(r"^(a|an|the) (?=\S)", "", norm_text(s)))   # noqa: E731
    tv = words(value)
    for a in key["a"]:
        pairs = typos.slips(tv, words(a), _NEVER | set(re.findall(r"[a-z]+", prompt.lower())))
        if pairs:
            return pairs
    return []
