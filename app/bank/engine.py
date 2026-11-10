"""Hand-written question banks (grammar and punctuation, science): loading, serving and marking.

The content lives in app/bank/content/*.py (format in SPEC.md). A question is served without its answer;
what is needed to mark it stays on the server with the item (see app/items.py).
"""
import difflib
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
        for lst in years.values():      # teaching order: by key, or straight after the skill named in "after"
            lst.sort(key=lambda s: (s.get("after") or s["key"], s["key"]))
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


def why_lines(q: dict | None, key: dict, value, again: bool = False) -> tuple[str, str]:
    """(why the option picked is wrong, the explanation) for a wrong answer. An mcq option built on a common
    misconception has its own line in "no" ({option: line}); a question missed before (again) gives "why2",
    another way of putting it, when it has one."""
    q = q or {}
    why = (q.get("why2") if again else None) or q.get("why", "")
    no = (q.get("no") or {}).get(given_text(key, value)) if key.get("t") == "mcq" else None
    return no or "", why


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
# Short words that are each a real choice in grammar ("who" for "whom", "than" for "then", "where" for "were"):
# typing one is a grammar mistake, never a spelling slip.
_GRAMMAR_WORDS = frozenset(
    "a an the this that these those there their they them then than who whom whose which what when where were wear "
    "we was is it its as at of off on in into to too two and or but if so not no now how here hear our are be been "
    "being see sea by buy his he her hers me my mine your yours you ours us will would could should can may might "
    "must shall has have had do does did done went want".split())
# Grammar skills where how the word is written IS the skill (decided by the skill, not by the word): word endings
# and prefixes, verb forms and tenses, apostrophes, homophones and confused words. No spelling retry there.
_SPELLING_STRANDS = frozenset({"Words", "Word structure", "Word study"})
_SPELLING_SKILLS = frozenset({
    "GP1.07", "GP2.13", "GP2.14", "GP2.15", "GP2.16", "GP2.18", "GP2.19", "GP3.11", "GP4.03", "GP4.04", "GP4.05",
    "GP6.03", "GP6.04", "GP6.08", "GP6.09", "GP6.15", "GP7.01", "GP7.02", "GP7.03", "GP7.04", "GP7.13", "GP7.14",
    "GP7.16", "GP7.17", "GP8.01", "GP8.02", "GP8.04", "GP9.02", "GP9.04", "GP9.14"})
# Skills about capital letters, full stops and other end marks (and whole-sentence punctuation): there a missing
# capital or full stop is the mistake, not a slip.
_END_MARK_SKILLS = frozenset({
    "GP1.01", "GP1.02", "GP1.03", "GP1.04", "GP1.05", "GP1.06", "GP1.07", "GP2.01", "GP2.02", "GP2.03", "GP3.14",
    "GP4.11", "GP4.12", "GP6.14", "GP7.12", "GP7.14", "GP7.18", "GP9.05"})


# ... except where the skill is the choice of a word or a tense, not how its ending is made. Choosing a word (formal
# words, synonyms, the names of terms): a one-letter slip gets its "Nearly" as anywhere ("aproximately"). Verb
# tenses and voices: a slip inside the right word ("was cookng"), its start and ending right and no letter doubled
# or undoubled (typos.inner_slip), so "hoping" for "hopping" or "jumpd" for "jumped" stay mistakes.
_WORD_CHOICE_SKILLS = frozenset({"GP6.05", "GP6.06", "GP9.13"})
_TENSE_SKILLS = frozenset({
    "GP2.13", "GP2.14", "GP2.15", "GP2.16", "GP3.11", "GP4.05", "GP6.03", "GP6.08", "GP6.09", "GP7.02", "GP7.13",
    "GP8.01", "GP8.02", "GP8.04"})


def spelling_matters(sk: dict | None) -> bool:
    return not sk or sk.get("strand") in _SPELLING_STRANDS or sk.get("key") in _SPELLING_SKILLS


def _skill_words(sk: dict) -> set:
    """Every answer and option word of the skill: one of them typed for another is a real choice, not a slip."""
    out = set()
    for q in sk.get("qs", []):
        for a in (q.get("a") if isinstance(q.get("a"), list) else []) + list(q.get("opts") or []):
            out |= set(re.findall(r"[a-z]+", str(a).lower()))
    return out


def slips(key: dict, value, prompt: str = "", sk: dict | None = None) -> list:
    """A word typed with one slip ("respiraton", "ded", "wich" for "which"): [(typed, wanted)] against the nearest
    accepted answer, for a free retry. In science always; in grammar unless the skill is about how words are
    written (spelling_matters). Never a word the question itself offers ("living, dead or never alive?"), and in
    grammar never a short grammar word or another answer of the skill ("who" for "whom")."""
    if key.get("t") != "text":
        return []
    never = _NEVER | set(re.findall(r"[a-z]+", prompt.lower()))
    inner = False                    # only a slip inside the word (_TENSE_SKILLS)
    if not key.get("loose"):
        if not sk or sk.get("subject") != "grammar":
            return []
        if spelling_matters(sk) and sk.get("key") not in _WORD_CHOICE_SKILLS:
            if sk.get("key") not in _TENSE_SKILLS:
                return []
            inner = True
        never |= _GRAMMAR_WORDS | _skill_words(sk)
    words = lambda s: re.findall(r"[a-z]+", re.sub(r"^(a|an|the) (?=\S)", "", norm_text(s)))   # noqa: E731
    tv = words(value)
    if not tv or re.sub(r"[a-z\s'-]", "", norm_text(value)):        # digits or signs typed: not a word slip
        return []
    for a in key["a"] + key.get("full", []):
        pairs = typos.slips(tv, words(a), never)
        if pairs and (not inner or all(typos.inner_slip(t, w) for t, w in pairs)):
            return pairs
    return []


_END = {".": "full stop", "?": "question mark", "!": "exclamation mark"}


def end_slip(key: dict, value, sk: dict | None = None) -> dict | None:
    """A rewritten sentence right but for a missing capital letter at the start and/or a missing end mark
    ("Kofi will visit his aunt on Saturday" for "... Saturday."): {"retry": ..., "after": ...} for one free retry,
    then a correction that says what was missing. Not in a skill about capitals and end marks."""
    if key.get("t") != "write" or not sk or sk.get("key") in _END_MARK_SKILLS:
        return None
    v = norm_write(value).strip()
    if not v:
        return None
    for a in (norm_write(x).strip() for x in key["a"]):
        cap = v[:1].islower() and a[:1].isupper() and v[1:2] == a[1:2]
        v2 = (a[:1] + v[1:]) if cap else v
        end = a[-1:] if a[-1:] in _END and v2 + a[-1] == a else ""
        if not (cap or end) or (v2 + end) != a:
            continue
        what = " and ".join(x for x in ("capital letter" if cap else "", _END[end] if end else "") if x)
        start = "a capital letter at the start" if cap else ""
        stop = ("a %s at the end" % _END[end]) if end else ""
        return {"retry": "Nearly — check your %s." % what,
                "after": "Your words were right: the sentence needs %s." % " and ".join(x for x in (start, stop) if x)}
    return None


def word_marks(value, answers: list) -> tuple[str, dict] | None:
    """For a sentence answer: (the accepted answer nearest to what was typed, the words that differ in each),
    as {"typed": [[text, wrong]], "word": [[text, changed]]} like spelling's letter marks. None when there is
    nothing to compare or the two have little in common."""
    tv = norm_write(value).split()
    if not tv:
        return None
    best = max(answers, key=lambda a: difflib.SequenceMatcher(None, tv, norm_write(a).split(), autojunk=False).ratio())
    av = norm_write(best).split()
    sm = difflib.SequenceMatcher(None, tv, av, autojunk=False)
    if sm.ratio() < 0.5:
        return None
    t_out, a_out = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if i2 > i1:
            t_out.append([" ".join(tv[i1:i2]), op != "equal"])
        if j2 > j1:
            a_out.append([" ".join(av[j1:j2]), op != "equal"])
    if not any(c for _, c in a_out) and not any(c for _, c in t_out):
        return None
    return best, {"typed": t_out, "word": a_out}
