"""Year 4 money answers as people write them: an amount of £1 or more is asked in pounds and pence (written
like 4.75), not as "1,008p". Where changing pounds into pence is the skill itself (Y4.7.f to h) only amounts of
£10 or more move to pounds; "How many pence is £8.70?" is never changed (it does not ask "in pence")."""
import re

from .maths_engine import GENERATORS, call_generator, money

_ASK = ((re.compile(r",? in pence\?"), ", in pounds? Write it like 4.75."),
        (re.compile(r"(?:Give|Write) (?:your|the) answer in pence\."), "Give your answer in pounds, written like 4.75."),
        (re.compile(r"Write the (\w+) value in pence\."), r"Write the \1 value in pounds, written like 4.75."))


def in_pounds(q, from_p=100):
    """The question asked in pounds when its answer in pence is from_p or more; otherwise unchanged."""
    a = q.get("answer")
    if q.get("answer_type") != "int" or isinstance(a, bool) or not isinstance(a, int) or a < from_p:
        return q
    p = str(q.get("prompt", ""))
    for rx, new in _ASK:
        asked = rx.sub(new, p, count=1)
        if asked != p:
            break
    else:
        return q
    spec = {k: v for k, v in (q.get("spec") or {}).items() if k != "unit"}
    sol = list(q.get("solution") or [])
    if not any(money(a) in str(s) for s in sol):
        sol.append("In pounds and pence that is %s." % money(a))
    return {**q, "prompt": asked, "spec": spec, "answer": "%d.%02d" % divmod(a, 100), "answer_type": "num",
            "solution": sol}


def pounds_from(from_p, *keys):
    """Ask these skills' money answers of from_p pence or more in pounds."""
    for k in keys:
        fn = GENERATORS[k]

        def gen(d=1, fn=fn):
            return in_pounds(call_generator(fn, d), from_p)
        GENERATORS[k] = gen
