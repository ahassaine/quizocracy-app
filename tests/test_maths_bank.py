"""Every maths generator: no crash, its own answer passes the checker, hidden table cells stay hidden."""
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e  # noqa: E402

RUNS = 20


def test_every_skill_generates_checkable_questions():
    random.seed(1)
    bad = []
    for s in e.SKILLS:
        for d in (0, 1, 2):
            for _ in range(RUNS):
                try:
                    q = e.call_generator(e.GENERATORS[s["key"]], d)
                except Exception as ex:          # noqa: BLE001
                    bad.append(f"{s['key']} d{d} crashed: {ex!r}")
                    break
                a = q.get("answer")
                if not str(q.get("prompt") or "").strip() or a is None or str(a).strip() == "":
                    bad.append(f"{s['key']} d{d} empty prompt or answer")
                    break
                if not e.check_answer(q.get("answer_type", "num"), str(a), a, q.get("tolerance", 0)):
                    bad.append(f"{s['key']} d{d} rejects its own answer {a!r}")
                    break
                typed = q.get("component", "number") != "number_line"          # a marker is placed, not typed
                if typed and q.get("answer_type") in ("num", "int") and "." in str(a) and len(str(a).split(".")[1]) > 9:
                    bad.append(f"{s['key']} d{d} answer {a!r} cannot be typed exactly")
                    break
                spec = e.hide_missing_cell(q.get("component"), q.get("spec") or {})
                m = spec.get("missing")
                if q.get("component") == "data_table" and isinstance(m, list) and spec["rows"][m[0]][m[1]] != "":
                    bad.append(f"{s['key']} d{d} sends the hidden table cell")
                if q.get("component") == "io_table" and isinstance(m, int) and spec["rows"][m][1] != "":
                    bad.append(f"{s['key']} d{d} sends the hidden table cell")
    assert not bad, "\n".join(bad[:30])


def _shape(p):
    p = re.sub(r"\d+(\.\d+)?", "#", p.replace("−", "-"))
    for n in e.NAMES:
        p = p.replace(n, "W")
    return p[:70]


def test_every_skill_has_real_variety():
    """At least 10 distinct question shapes per skill (scripts/maths_variety.py aims for 12+)."""
    from app.maths.maths_mastery import OUT_OF_YEAR
    random.seed(5)
    thin = []
    for s in e.SKILLS:
        if s["key"] in OUT_OF_YEAR:
            continue
        shapes = {(q.get("component"), _shape(str(q["prompt"])))
                  for d in (0, 1, 2) for q in (e.call_generator(e.GENERATORS[s["key"]], d) for _ in range(80))}
        if len(shapes) < 10:
            thin.append("%s %d" % (s["key"], len(shapes)))
    assert not thin, thin


def test_no_broken_text_or_data():
    """The lint rules that have no false positives (the full set is scripts/maths_lint.py)."""
    import json
    rx = re.compile(r"%[sdfr]|\{\}|\bNone\b(?! (of|are|is|was|were|have|has)\b)|\b(nan|NaN)\b|\ba (8|11|18)\b")
    random.seed(6)
    bad = []
    for s in e.SKILLS:
        for d in (0, 1, 2):
            for _ in range(RUNS):
                q = e.call_generator(e.GENERATORS[s["key"]], d)
                for t in [str(q["prompt"])] + [str(x) for x in q.get("solution") or []]:
                    if rx.search(t):
                        bad.append("%s: %s" % (s["key"], t[:90]))
                try:
                    json.dumps(q.get("spec") or {}, allow_nan=False)
                except (TypeError, ValueError):
                    bad.append("%s: spec is not plain JSON" % s["key"])
                if q.get("answer_type") == "int" and not re.fullmatch(r"-?\d+", str(q["answer"]).replace(",", "")):
                    bad.append("%s: int answer %r" % (s["key"], q["answer"]))
    assert not bad, "\n".join(sorted(set(bad))[:30])
