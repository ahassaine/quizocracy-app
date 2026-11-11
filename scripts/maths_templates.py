"""Print samples of every template of every maths skill, for reading against the skill's title and year.

    python3 scripts/maths_templates.py [Y5 | Y5.3 | Y5.3.a ...] [--n 120] [--k 1]

A template is the framing function inside a skill's generator that made the question (found by watching which
nested function returned it), or, for a generator that branches inline, the question's wording with numbers and
names left out. For each template: how often each tier serves it, then k samples per tier with the answer and
the first line of the "why".
"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e
from app.maths.maths_mastery import OUT_OF_YEAR

args = sys.argv[1:]
N = int(args[args.index("--n") + 1]) if "--n" in args else 120
K = int(args[args.index("--k") + 1]) if "--k" in args else 1
only = [a for a in args if a.startswith("Y")]
random.seed(int(os.getenv("SEED", "7")))


def _shape(p):
    p = re.sub(r"\d[\d,.]*", "#", p.replace("−", "-"))
    for n in e.NAMES:
        p = p.replace(n, "W")
    return p[:48]


def made_by(fn, d):
    """(question, template key)."""
    seen = []

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is not fn.__code__ and "<locals>" in frame.f_code.co_qualname \
                and not frame.f_code.co_qualname.startswith("pounds_from"):
            seen.append((frame.f_code.co_qualname, arg))
    sys.setprofile(prof)
    try:
        q = e.call_generator(fn, d)
    finally:
        sys.setprofile(None)
    names = [n for n, r in seen if r is q]
    if names:
        return q, names[-1].split("<locals>.")[-1]
    return q, "~" + (q.get("component") or "number") + ":" + _shape(str(q.get("prompt")))


def one(q):
    sol = (q.get("solution") or [""])
    sol = " / ".join(str(s) for s in sol[:2])
    comp = q.get("component") or "number"
    sp = q.get("spec") or {}
    extra = {x: sp[x] for x in ("values", "categories", "choices", "options", "min", "max", "step") if x in sp}
    return "%s || ans %r [%s%s] || %s" % (" ".join(str(q.get("prompt")).split())[:260], q.get("answer"), comp,
                                          (" " + str(extra)[:110]) if extra else "", sol[:200])


for s in e.SKILLS:
    k = s["key"]
    if only and not k.startswith(tuple(o.rstrip(".") + "." if o.count(".") < 2 else o for o in only)) \
            and k not in only:
        continue
    fn = e.GENERATORS[k]
    tmpl = collections.defaultdict(lambda: {0: [], 1: [], 2: []})
    for d in (0, 1, 2):
        for _ in range(N):
            q, t = made_by(fn, d)
            tmpl[t][d].append(q)
    print("\n## %s %s%s  (%d templates)" % (k, s["title"], "  [OUT_OF_YEAR]" if k in OUT_OF_YEAR else "",
                                            len(tmpl)))
    for t, by in sorted(tmpl.items()):
        print("  - %s  [d0 %d, d1 %d, d2 %d]" % (t, len(by[0]), len(by[1]), len(by[2])))
        for d in (0, 1, 2):
            for q in by[d][:K]:
                print("      d%d %s" % (d, one(q)))
