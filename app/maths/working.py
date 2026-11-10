"""Written methods laid out in columns, for the explanation after a missed calculation: column addition with its
carries, column subtraction with its exchanges, long multiplication with its part products, and long division
step by step. Each is {"grid": plain text for a fixed-width block, every line the same width so the digits line
up, "say": one plain sentence on how to read it}."""
import re

_N = r"\d{1,3}(?:,\d{3})+|\d+"
# "£879,242 + £42,919 = £922,161", "1,326 ÷ 32 = 41 remainder 14" (a whole line, or a whole calculation in a prompt)
_CALC = re.compile(r"(?<![\d.,/^])£?(%s)\s*([+−×÷-])\s*£?(%s)(?![\d^]|[.,]\d)(?:\s*=\s*£?(%s)(?![\d]|[.,]\d)"
                   r"(?:\s*remainder\s*(%s))?)?" % (_N, _N, _N, _N))
_CHAIN = re.compile(r"(?<![\d.,/^])£?(?:%s)(?:\s*\+\s*£?(?:%s)){2,}(?![\d^]|[.,]\d)" % (_N, _N))
_OP_BEFORE = re.compile(r"[+−×÷*/=-]\s*£?$")
_OP_AFTER = re.compile(r"^\s*[+−×÷*/^(]")


def _int(s):
    return int(s.replace(",", ""))


def _cells(n, width):
    """A number as digit cells, right-aligned in width columns ("  " for an empty column)."""
    s = str(n)
    return ["  "] * (width - len(s)) + [" " + c for c in s]


def _block(rows):
    w = max(len(r) for r in rows)
    return "\n".join(r.rstrip().ljust(w) for r in rows)


def column_layout(a, op, b, *more):
    """Column addition (of two or more numbers) or subtraction, the larger number on top for a subtraction."""
    add = op == "+"
    if not add and b > a:
        a, b = b, a
    nums = [a, b] + list(more) if add else [a, b]
    res = sum(nums) if add else a - b
    w = max(len(str(n)) for n in nums + [res])
    digits = [[int(c) for c in str(n).rjust(w, "0")] for n in nums]
    marks = [" "] * w
    if add:
        carry = 0
        for i in range(w - 1, -1, -1):
            carry = (sum(d[i] for d in digits) + carry) // 10
            if carry and i > 0:
                marks[i - 1] = str(carry)
        note = ("Add each column from the right, ones first. A small number under a column is the tens carried "
                "into it.")
        label = "carried"
    else:
        borrow = 0
        for i in range(w - 1, -1, -1):
            borrow = 1 if digits[0][i] - borrow - digits[1][i] < 0 else 0
            if borrow:
                marks[i] = "1"
        note = ("Take away each column from the right, ones first. A small 1 under a column: it was too small, "
                "so it exchanged 10 from the column to its left.")
        label = "exchanged"
    line = "--" * (w + 1)
    rows = ["  " + "".join(_cells(n, w)) for n in nums[:-1]]
    rows += [("+ " if add else "- ") + "".join(_cells(nums[-1], w)), line, "  " + "".join(_cells(res, w))]
    if any(m != " " for m in marks):
        rows.append("  " + "".join(" " + m for m in marks) + "   (" + label + ")")
    return {"grid": _block(rows), "say": note}


def long_mult_layout(a, b):
    """Long multiplication: the bigger number on top, one part product for each digit of the smaller one."""
    if b > a:
        a, b = b, a
    digits = str(b)
    if b < 10:                                       # short multiplication: one row, with its carries
        w = len(str(a * b))
        marks, carry = [" "] * w, 0
        da = [int(c) for c in str(a).rjust(w, "0")]
        for i in range(w - 1, -1, -1):
            carry = (da[i] * b + carry) // 10
            if carry and i > 0:
                marks[i - 1] = str(carry)
        rows = ["  " + "".join(_cells(a, w)), "× " + "".join(_cells(b, w)), "--" * (w + 1),
                "  " + "".join(_cells(a * b, w))]
        if any(m != " " for m in marks):
            rows.append("  " + "".join(" " + m for m in marks) + "   (carried)")
        return {"grid": _block(rows), "say": "Multiply each digit by %d, ones first. A small number under a column "
                                             "is the tens carried into it, added after multiplying." % b}
    parts = [(a * int(d) * 10 ** (len(digits) - 1 - i), int(d) * 10 ** (len(digits) - 1 - i))
             for i, d in enumerate(digits)][::-1]
    parts = [(p, m) for p, m in parts if m]
    res = a * b
    w = max(len(str(res)), len(str(a)), len(digits))
    line = "--" * (w + 1)
    rows = ["  " + "".join(_cells(a, w)), "× " + "".join(_cells(b, w)), line]
    rows += ["  " + "".join(_cells(p, w)) + "   (%s × %s)" % (f"{a:,}", f"{m:,}") for p, m in parts]
    rows += [line, "  " + "".join(_cells(res, w))]
    return {"grid": _block(rows), "say": "Multiply by the ones, then by the tens (put a 0 in the ones first), then add the two rows."}


def long_div_layout(n, d):
    """Long division set out step by step: divide, multiply, subtract, bring down the next digit."""
    s = str(n)
    k = len(s)
    pre = len(str(d)) + 2
    pad = " " * pre

    def at(num, end):          # a number right-aligned to end under dividend digit `end`
        cells = ["  "] * k
        t = str(num)
        for j, c in enumerate(t):
            pos = end - len(t) + 1 + j
            if 0 <= pos < k:
                cells[pos] = " " + c
        return "".join(cells)
    q_digits, steps, part, started = [], [], 0, False
    for i, c in enumerate(s):
        part = part * 10 + int(c)
        qd = part // d
        if qd or started or i == k - 1:
            started = True
            steps.append((i, part, qd))
        q_digits.append(str(qd) if started else " ")
        part -= qd * d
    q = n // d
    r = n % d
    rows = [pad + "".join(" " + x for x in q_digits) + ("   r %d" % r if r else ""),
            " " * (pre - 1) + " " + "__" * k,
            str(d) + " )" + "".join(" " + c for c in s)]
    for j, (i, p, qd) in enumerate(steps):
        if j:                                         # the remainder with the next digit brought down
            rows.append(pad + at(p, i) + ("   (%d × 0)" % d if not qd else ""))
        if qd:
            rows.append(pad[:-2] + "- " + at(qd * d, i) + "   (%d × %d)" % (d, qd))
            rows.append(pad + "".join("--" if i - len(str(qd * d)) < x <= i else "  " for x in range(k)))
    rows.append(pad + at(r, k - 1) + ("   remainder" if r else ""))
    note = "%s ÷ %d = %s%s. Divide, multiply, subtract, then bring down the next digit." % (
        f"{n:,}", d, f"{q:,}", " remainder %d" % r if r else "")
    return {"grid": _block(rows), "say": note}


def _fits(op, a, b):
    if op in "+−-":
        return max(a, b) >= 100 and min(a, b) >= 10
    if op == "×":
        small, big = min(a, b), max(a, b)
        return big >= 100 and 2 <= small <= 99 and small % 10 != 0
    if op == "÷":
        return a >= 100 and 2 <= b <= 99 and b % 10 != 0 and a // b >= 10
    return False


def _layout(op, a, b):
    if op in "+−-":
        return column_layout(a, "+" if op == "+" else "−", b)
    if op == "×":
        return long_mult_layout(a, b)
    return long_div_layout(a, b)


def _value(op, a, b):
    if op == "+":
        return a + b, None
    if op in "−-":
        return a - b, None
    if op == "×":
        return a * b, None
    return a // b, a % b


# Written methods belong to the Years 3-6 arithmetic strands, not to a place-value or fraction question that
# happens to show 9,000 ÷ 9; and not to the skills that are about mental methods or facts.
_ARITH_STRAND = re.compile(r"operations|addition|subtraction|multiplication|division", re.I)
_NOT_WRITTEN = re.compile(r"mental|facts|10, 100|times table|Roman", re.I)


def written_skill(skill):
    """Does a written method suit this skill (a skill_list entry)?"""
    return bool(skill) and skill["key"][:2] in ("Y3", "Y4", "Y5", "Y6") and bool(_ARITH_STRAND.search(skill["strand"])) \
        and not _NOT_WRITTEN.search(skill["title"])


def layout_for(q, skill=None):
    """The written method for a question's calculation, or None: the calculation whose result is the answer
    first (in the prompt or the working), else the first whole calculation the working shows. skill: the
    question's skill_list entry; only arithmetic skills get one (written_skill)."""
    if skill is not None and not written_skill(skill):
        return None
    try:
        ans = int(str(q.get("answer")).replace(",", ""))
    except (TypeError, ValueError):
        ans = None
    # three or more numbers added ("Work out: 348,402 + 276,083 + 822,646"): one column sum of them all
    for m in _CHAIN.finditer(q.get("prompt", "")):
        if _OP_BEFORE.search(q["prompt"][:m.start()]) or _OP_AFTER.match(q["prompt"][m.end():]):
            continue
        nums = [_int(x) for x in re.findall(_N, m.group(0))]
        if sum(nums) == ans and max(nums) >= 100:
            return column_layout(nums[0], "+", nums[1], *nums[2:])
    found = []
    for src, text in [("p", q.get("prompt", ""))] + [("s", s) for s in (q.get("solution") or [])
                                                     if isinstance(s, str)]:
        for m in _CALC.finditer(text):
            if _OP_BEFORE.search(text[:m.start()]) or _OP_AFTER.match(text[m.end():]):
                continue                                  # part of a longer chain: 86,830 + 14,263 − 13,257
            a, op, b = _int(m.group(1)), m.group(2), _int(m.group(3))
            if op == "-" and src == "p":
                continue                                  # a hyphen in a sentence, not a minus
            if not _fits(op, a, b):
                continue
            val, rem = _value(op, a, b)
            if op in "−-" and src == "s" and val < 0:
                continue
            if m.group(4):                                # the working's own result must be the true one
                if _int(m.group(4)) != val or (m.group(5) and rem != _int(m.group(5))):
                    continue
            elif src == "s":
                continue
            found.append((val == ans or (op == "÷" and rem == ans and "remainder" in q.get("prompt", "").lower()),
                          src == "s" and bool(m.group(4)), op, a, b))
    main = [f for f in found if f[0]] or [f for f in found if f[1]]
    if not main:
        return None
    _, _, op, a, b = main[0]
    return _layout(op, a, b)
