"""Every maths generator: no crash, its own answer passes the checker, hidden table cells stay hidden."""
import os
import random
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
