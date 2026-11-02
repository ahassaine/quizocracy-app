"""Run every maths generator many times and flag crashes and degenerate questions.

    python3 scripts/maths_fuzz.py [Y5] [--n 300]
No database is touched: generators are called directly.
"""
import collections, re, sys, os, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e

N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 300
only = [a for a in sys.argv[1:] if a.startswith("Y")]

def choices(q):
    sp = q.get("spec") or {}
    for k in ("choices", "options"):
        if isinstance(sp.get(k), list):
            return [str(c) for c in sp[k]]
    return None

problems = collections.defaultdict(list)
for s in e.SKILLS:
    key = s["key"]
    if only and not any(key.startswith(o + ".") for o in only):
        continue
    fn = e.GENERATORS[key]
    for d in (0, 1, 2):
        prompts, answers, errs = set(), set(), 0
        for _ in range(N):
            try:
                q = e.call_generator(fn, d)
            except Exception as ex:
                errs += 1
                if errs == 1:
                    problems[key].append(f"d{d} CRASH {type(ex).__name__}: {ex} @ {traceback.extract_tb(ex.__traceback__)[-1].lineno}")
                continue
            p, a, at = q.get("prompt"), q.get("answer"), q.get("answer_type", "num")
            if not p or not str(p).strip():
                problems[key].append(f"d{d} empty prompt"); break
            if a is None or str(a).strip() == "":
                problems[key].append(f"d{d} empty answer: {p[:80]}"); break
            if not e.check_answer(at, str(a), a, q.get("tolerance", 0)):
                problems[key].append(f"d{d} own answer rejected ({at}) {a!r}: {p[:80]}"); break
            ch = choices(q)
            if ch is not None:
                if not any(e.check_answer(at, c, a, q.get("tolerance", 0)) for c in ch):
                    problems[key].append(f"d{d} answer {a!r} not among choices {ch}: {p[:80]}"); break
                if len(set(ch)) != len(ch):
                    problems[key].append(f"d{d} duplicate choices {ch}: {p[:80]}"); break
            if at in ("num", "int") and re.search(r"(?<![\d.])" + re.escape(str(a)) + r"(?![\d.])", str(p)) and len(str(a)) >= 3:
                problems[key].append(f"d{d} answer appears in prompt? {a!r}: {p[:100]}")
            prompts.add(str(p) + repr(q.get("spec"))); answers.add(str(a))
        if errs:
            problems[key].append(f"d{d} crashed {errs}/{N}")
        if len(prompts) < min(8, N // 10):
            problems[key].append(f"d{d} low variety: {len(prompts)} distinct questions in {N}")

seen = set()
for key, ps in problems.items():
    uniq = [p for p in ps if not (p in seen or seen.add(p))]
    print(key, next(x["title"] for x in e.SKILLS if x["key"] == key))
    for p in dict.fromkeys(ps):
        print("   ", p)
print(f"\n{len(problems)} of {sum(1 for s in e.SKILLS if not only or any(s['key'].startswith(o + '.') for o in only))} skills flagged")
