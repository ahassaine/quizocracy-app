"""Give every bank question a permanent id (app/bank/SPEC.md: "Question ids").

    python scripts/bank_ids.py             # add an id to every question in app/bank/content that has none
    python scripts/bank_ids.py --check     # only report questions without an id; exits 1 if there are any
    python scripts/bank_ids.py --legacy    # one-off (10 Nov 2026): the id a question was served under until then

A new question gets a fresh random id that no question has. Children's seen lists, mistakes and mastery are
stored by id, so an id is never changed or reused, even when the question's text is edited. Running the script
again changes nothing. The only change made to a file is `"id": "…", ` written after the `{` of each question
that lacks one; every other byte stays as it is.
"""
import ast
import pathlib
import re
import secrets
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
CONTENT = ROOT / "app/bank/content"
ID_RE = re.compile(r"^[0-9a-f]{12}$")


def files():
    return sorted(p for p in CONTENT.glob("*.py") if p.stem != "__init__")


def questions(src: bytes):
    """[(skill key, question Dict node)] in file order, from the module's literal SKILLS list."""
    tree = ast.parse(src)
    node = next((n.value for n in tree.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "SKILLS" for t in n.targets)), None)
    if not isinstance(node, ast.List):
        raise ValueError("no literal SKILLS list")
    out = []
    for sk in node.elts:
        fields = {k.value: v for k, v in zip(sk.keys, sk.values) if isinstance(k, ast.Constant)}
        key = ast.literal_eval(fields["key"])
        qs = fields.get("qs")
        if not isinstance(qs, ast.List) or not all(isinstance(q, ast.Dict) for q in qs.elts):
            raise ValueError(f"{key}: qs is not a literal list of dicts")
        out += [(key, q) for q in qs.elts]
    return out


def node_id(q: ast.Dict):
    for k, v in zip(q.keys, q.values):
        if isinstance(k, ast.Constant) and k.value == "id":
            return ast.literal_eval(v)
    return None


def main(argv):
    check, legacy = "--check" in argv, "--legacy" in argv
    if legacy:
        from app.bank.engine import _qid
    parsed = {p: (p.read_bytes(),) for p in files()}
    taken = set()
    for p, (src,) in parsed.items():
        qs = questions(src)
        parsed[p] = (src, qs)
        taken |= {node_id(q) for _, q in qs if node_id(q)}
    missing = 0
    for p, (src, qs) in parsed.items():
        todo = [(key, q) for key, q in qs if node_id(q) is None]
        missing += len(todo)
        if check or not todo:
            if todo:
                print(f"{p.stem}: {len(todo)} questions without an id")
            continue
        starts = [0]
        for line in src.split(b"\n"):
            starts.append(starts[-1] + len(line) + 1)
        edits = []
        for key, q in todo:
            if legacy:
                qid = _qid(key, ast.literal_eval(q))
            else:
                qid = secrets.token_hex(6)
                while qid in taken:
                    qid = secrets.token_hex(6)
            if qid in taken:
                raise SystemExit(f"{p.stem} {key}: id {qid} is already taken")
            taken.add(qid)
            off = starts[q.lineno - 1] + q.col_offset          # col_offset counts UTF-8 bytes, as src is bytes
            assert src[off:off + 1] == b"{", (p.stem, key, q.lineno)
            edits.append((off + 1, f'"id": "{qid}", '.encode()))
        for off, ins in sorted(edits, reverse=True):
            src = src[:off] + ins + src[off:]
        p.write_bytes(src)
        print(f"{p.stem}: {len(todo)} ids added")
    if check:
        print(f"{missing} questions without an id")
        return 1 if missing else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
