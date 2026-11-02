"""Print sample questions with answers for hand review:  python3 scripts/maths_sample.py Y5.0 [per-skill]"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e

pref, k = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6
random.seed(int(os.getenv("SEED", "4")))
for s in e.SKILLS:
    if not s["key"].startswith(pref + "."):
        continue
    print("##", s["key"], s["title"])
    for i in range(k):
        q = e.call_generator(e.GENERATORS[s["key"]], i % 3)
        sp = e.hide_missing_cell(q.get("component"), q.get("spec") or {})
        extra = {x: sp[x] for x in ("rows", "values", "points", "min", "max") if x in sp}
        print(" d%d %s || %r [%s] %s" % (i % 3, " ".join(str(q["prompt"]).split()), q["answer"],
                                          q.get("component", "number"), str(extra)[:150] if extra else ""))
