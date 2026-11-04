"""Distinct prompt shapes per skill (numbers and names normalised).

    python3 scripts/maths_variety.py [Y5 ...] [--min 12]
Prints each year's average and the skills below the minimum.
"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e
from app.maths.maths_mastery import OUT_OF_YEAR
args = sys.argv[1:]
mn = 15
if "--min" in args:
    i = args.index("--min"); mn = int(args[i+1]); args = args[:i] + args[i+2:]
years = set(int(a[1:]) for a in args) or set(range(1, 10))
random.seed(3)
NM = set(e.NAMES) if hasattr(e, "NAMES") else set()
def shape(p):
    p = re.sub(r"−", "-", p)
    p = re.sub(r"\d+(\.\d+)?", "#", p)
    for n in NM: p = p.replace(n, "W")
    return p[:70]
tot = collections.Counter(); cnt = collections.Counter(); thin = collections.defaultdict(list)
for s in e.SKILLS:
    k = s["key"]
    if k in OUT_OF_YEAR: continue
    y = int(k.split(".")[0][1:])
    if y not in years: continue
    sh = set()
    for d in (0, 1, 2):
        for _ in range(60):
            q = e.call_generator(e.GENERATORS[k], d)
            sh.add((q.get("component"), shape(str(q.get("prompt")))))
    tot[y] += len(sh); cnt[y] += 1
    if len(sh) < mn: thin[y].append("%s(%d)" % (k, len(sh)))
for y in sorted(cnt):
    print("Y%d skills %d avg %.1f below %d: %d" % (y, cnt[y], tot[y] / cnt[y], mn, len(thin[y])))
    print("   ", " ".join(thin[y]))
