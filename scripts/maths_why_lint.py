"""Flag maths explanations ("why", the solution lines) that only restate the answer.

    python3 scripts/maths_why_lint.py [Y8 ...] [--top 30] [--show 2]

A why is thin when, once the answer is taken out, it has no word saying what was done and nothing new: every
number and operator in it is already in the question. "It is 0.4.", "= 0.99652" for 996.52 ÷ 1000, or
"4 + 9 = 13." for the x term of (x + 4)(x + 9). Structure only: it says which skills to
read first, not what is wrong. Prints the skills with the highest share of thin whys, worst first.
"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e
from app.maths.maths_mastery import OUT_OF_YEAR

args = sys.argv[1:]
top, show = 30, 2
if "--top" in args:
    i = args.index("--top"); top = int(args[i + 1]); args = args[:i] + args[i + 2:]
if "--show" in args:
    i = args.index("--show"); show = int(args[i + 1]); args = args[:i] + args[i + 2:]
years = tuple("Y%s." % a.lstrip("Yy") for a in args)
OPS = re.compile(r"[+−×÷=/√<>%^≈]|(?<=\s)-(?=\s)| of | half | double | more | less | rounds? | between ")
STOP = {"the", "is", "it", "so", "and", "a", "an", "answer", "cm", "mm", "m", "km", "kg", "g", "ml", "litres",
        "minutes", "seconds", "hours", "p", "pence", "pounds"}


NUM = re.compile(r"\d+(?:[.,]\d+)*")
OPCH = re.compile(r"[+−×÷=/√<>%^≈²³]")


def thin(q):
    """No word that says what was done, and nothing new: its numbers and operators all come from the question
    (or are the answer)."""
    sol = " ".join(str(s) for s in (q.get("solution") or []))
    ans, prompt = str(e.answer_text(q)), str(q.get("prompt", ""))
    rest = sol.replace(ans, " ")
    words = {w.lower() for w in re.findall(r"[A-Za-z]{2,}", rest)} - STOP - {w.lower() for w in re.findall(r"[A-Za-z]+", ans + " " + prompt)}
    new_nums = set(NUM.findall(rest)) - set(NUM.findall(prompt)) - set(NUM.findall(ans))
    new_ops = set(OPCH.findall(rest)) - set(OPCH.findall(prompt)) - {"="}
    return not sol.strip() or not (words or new_nums or new_ops)


random.seed(int(os.getenv("SEED", "7")))
rows = []
for s in e.SKILLS:
    k = s["key"]
    if k in OUT_OF_YEAR or (years and not k.startswith(years)):
        continue
    bad, n, ex = 0, 0, []
    for i in range(45):
        q = e.present(e.call_generator(e.GENERATORS[k], i % 3), k)
        n += 1
        if thin(q):
            bad += 1
            if len(ex) < show:
                ex.append("%s || %s" % (" ".join(str(q["prompt"]).split())[:90], " | ".join(map(str, q.get("solution") or []))[:110]))
    if bad:
        rows.append((bad / n, k, s["title"], ex))
rows.sort(reverse=True)
print("%d skills with thin whys (of %d sampled 45 times each)" % (len(rows), sum(1 for s in e.SKILLS if s["key"] not in OUT_OF_YEAR and (not years or s["key"].startswith(years)))))
for share, k, title, ex in rows[:top]:
    print("%3d%%  %s  %s" % (round(100 * share), k, title))
    for x in ex:
        print("        ", x)
