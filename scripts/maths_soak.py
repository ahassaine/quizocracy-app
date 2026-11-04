"""Soak test: thousands of questions per skill per tier; reports crashes, hangs (> 0.5 s for one
question; a stuck generator is stopped after 3 s) and answers the checker refuses.   python3 scripts/maths_soak.py [Y5 ...] [--n 3000]"""
import collections, os, random, signal, sys, time, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e

N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3000
only = tuple(a + "." for a in sys.argv[1:] if a.startswith("Y"))
random.seed(int(os.getenv("SEED", "99")))
bad = collections.defaultdict(collections.Counter)


class Hang(Exception):
    pass


def _alarm(*_):
    raise Hang()


signal.signal(signal.SIGALRM, _alarm)       # a generator stuck in a loop is reported, not waited on forever
total = 0
for s in e.SKILLS:
    if only and not s["key"].startswith(only):
        continue
    for d in (0, 1, 2):
        for _ in range(N):
            t0 = time.time()
            signal.setitimer(signal.ITIMER_REAL, 3.0)
            try:
                q = e.call_generator(e.GENERATORS[s["key"]], d)
            except Hang:
                bad[s["key"]]["d%d HANG (> 3 s, stopped)" % d] += 1
                continue
            except Exception as ex:
                tb = traceback.extract_tb(ex.__traceback__)[-1]
                bad[s["key"]]["d%d crash %s: %s @ %s:%d" % (d, type(ex).__name__, ex, os.path.basename(tb.filename), tb.lineno)] += 1
                continue
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            total += 1
            if time.time() - t0 > 0.5:
                bad[s["key"]]["d%d slow %.1fs" % (d, time.time() - t0)] += 1
            if not e.check_answer(q.get("answer_type", "num"), str(q["answer"]), q["answer"], q.get("tolerance", 0)):
                bad[s["key"]]["d%d refuses own answer %r" % (d, q["answer"])] += 1
for k, c in bad.items():
    print(k)
    for m, n in c.most_common(4):
        print("   %5d× %s" % (n, m))
print("%d questions, %d skills with problems" % (total, len(bad)))
