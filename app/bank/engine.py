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

log = logging.getLogger("qz.bank")
CONTENT = pathlib.Path(__file__).parent / "content"
PREFIX = {"grammar": "GP", "science": "SC"}

_BANK: dict | None = None      # {subject: {year: [skill, ...]}}
_BY_KEY: dict = {}


def _qid(skill_key: str, q: dict) -> str:
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
            subject = next((s for s, p in PREFIX.items() if str(sk.get("key", "")).startswith(p)), None)
            qs = [dict(q, id=_qid(sk["key"], q)) for q in sk.get("qs", []) if _usable(q)]
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
        if q.get("loose"):
            key["loose"] = True
    elif t == "write":
        pub["s"] = q["s"]
        key["a"] = q["a"]
    elif t == "num":
        pub["unit"] = q.get("unit", "")
        key["a"], key["tol"] = q["a"], q.get("tol", 0)
    return pub, key


def _quotes(s: str) -> str:
    return (str(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
            .replace("…", "...").replace("–", "-").replace("—", "-"))


def norm_text(s: str) -> str:
    s = " ".join(_quotes(s).lower().split())
    return s.rstrip(".?!").strip()                    # a short answer's end mark does not matter


def loose(s: str) -> str:
    """Science: "the non-contact force" = "non contact force" = "noncontact force"."""
    return re.sub(r"[\s-]+", "", re.sub(r"^(a|an|the) (?=\S)", "", s))


def norm_write(s: str) -> str:
    s = " ".join(_quotes(s).split())
    return re.sub(r"\s+([,.;:!?])", r"\1", s)        # "Hello , Sam" counts as "Hello, Sam"


def parse_num(s) -> float | None:
    s = _quotes("" if s is None else str(s)).strip().replace(",", "").replace(" ", "")
    m = re.match(r"^[-+]?(\d+(\.\d*)?|\.\d+)", s.replace("−", "-"))
    return float(m.group(0)) if m else None


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
        if key.get("loose"):
            return bool(loose(v)) and loose(v) in {loose(norm_text(a)) for a in key["a"]}
        return bool(v) and v in {norm_text(a) for a in key["a"]}
    if t == "write":
        v = norm_write(value)
        return bool(v) and v in {norm_write(a) for a in key["a"]}
    if t == "num":
        v = parse_num(value)
        return v is not None and abs(v - float(key["a"])) <= float(key.get("tol") or 0) + 1e-9
    return False
