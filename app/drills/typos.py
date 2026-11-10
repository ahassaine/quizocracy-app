"""Near misses: a word typed with one small slip ("respiraton", "yse", "ninty") where spelling is not the skill.

Such an answer earns one free retry with "Nearly — check your spelling" before it is marked. Spelling tests never
use this. A typed word that is itself another answer word ("eighty" for "eight", "no" for "yes") is never a slip.
"""
import difflib

NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
                "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
                "thousand", "million", "and", "a"}
RETRY = "Nearly — check your spelling."


def one_slip(typed: str, want: str) -> bool:
    """One letter added, left out, changed, or two neighbours swapped. A three-letter word only by a swap
    ("yse" for "yes"): one changed letter in so short a word is usually another word."""
    if typed == want or not typed.isalpha() or not want.isalpha():
        return False
    a, b = typed, want
    if len(b) < 3 or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        if len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]]:
            return True                                        # swapped neighbours
        return len(diff) == 1 and len(b) >= 4
    if len(b) < 4:
        return False
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return any(long_[:i] + long_[i + 1:] == short for i in range(len(long_)))


def slips(typed_words: list, want_words: list, never=frozenset()) -> list:
    """[(typed, wanted), ...] when the answer is right but for one or two slipped words; [] otherwise.
    `never`: words that mean something else here, so typing one is a real mistake."""
    if len(typed_words) != len(want_words) or not want_words:
        return []
    pairs = [(t, w) for t, w in zip(typed_words, want_words) if t != w]
    if not pairs or len(pairs) > 2:
        return []
    if all(one_slip(t, w) and t not in never for t, w in pairs):
        return pairs
    return []


def number_hint(pairs: list) -> str:
    """For a number written in words whose number is right."""
    if len(pairs) == 1:
        return "Your number is right — check the spelling of '%s'." % pairs[0][0]
    return "Your number is right — check the spelling of '%s' and '%s'." % (pairs[0][0], pairs[1][0])


def corrections(pairs: list) -> str:
    """After the retry: which word was wrong. "'ninty' should be 'ninety'." """
    return " ".join("'%s' should be '%s'." % (t, w) for t, w in pairs)


# ----------------------------------------------------------------- spelling test feedback ----
# UK words of the spelling lists and their American spellings (hand-written; "practice"/"license" are left out,
# since those are also UK words, the nouns).
AMERICAN = {
    "analyse": "analyze", "behaviour": "behavior", "centre": "center", "criticise": "criticize",
    "emphasise": "emphasize", "favourite": "favorite", "fulfil": "fulfill", "jewellery": "jewelry",
    "manoeuvre": "maneuver", "marvellous": "marvelous", "neighbour": "neighbor", "programme": "program",
    "recognise": "recognize", "skilful": "skillful", "vapour": "vapor", "colour": "color",
    "organise": "organize", "realise": "realize", "apologise": "apologize", "travelled": "traveled",
}


def american(word: str, typed: str) -> bool:
    return AMERICAN.get(word.lower()) == typed.lower()


def _ops(t: str, w: str) -> list:
    return [o for o in difflib.SequenceMatcher(None, t, w, autojunk=False).get_opcodes() if o[0] != "equal"]


def swapped(t: str, w: str) -> int | None:
    """Where two neighbouring letters of the attempt are the wrong way round ("recieve", "becuase"): the index of
    the first of the two, when putting them back fixes the word or leaves at most one other change; else None.
    Without this, difflib reads a swap as one letter added and the same letter taken out. With another change as
    well, only when difflib reads it so ("tommorow" is mm → m and r → rr, not a swap)."""
    ops = _ops(t, w)
    n = len(ops)
    added = {w[j1:j2] for op, i1, i2, j1, j2 in ops if op == "insert"}
    taken = {t[i1:i2] for op, i1, i2, j1, j2 in ops if op == "delete"}
    mixed = bool(added & taken)
    best = None
    for k in range(len(t) - 1):
        if t[k] == t[k + 1]:
            continue
        t2 = t[:k] + t[k + 1] + t[k] + t[k + 2:]
        left = len(_ops(t2, w))
        if left < n and (left == 0 or (left == 1 and mixed)) and (best is None or left < best[1]):
            best = (k, left)
    return best[0] if best else None


def _swap_note(t2: str, k: int) -> str:
    """For ie/ei, the rule that goes with the swap (t2: the attempt with the swap put right)."""
    pair = t2[k:k + 2]
    if pair not in ("ie", "ei"):
        return ""
    after_c = k > 0 and t2[k - 1] == "c"
    if pair == "ei":
        return " (e before i after c)" if after_c else " (this word has e before i)"
    return " (i before e, even after c here)" if after_c else " (i before e, except after c)"


def letter_marks(typed: str, word: str) -> dict:
    """The child's attempt against the word, in pieces: {"typed": [[text, wrong]], "word": [[text, changed]]}.
    "acsident" / "accident": typed ac|s|ident with s wrong, word ac|c|ident with c changed. Two letters the wrong
    way round are marked as a pair in both ("rec|ie|ve", "rec|ei|ve")."""
    k = swapped(typed.lower(), word.lower()) if len(typed) == len(word) else None
    if k is not None and typed[:k] + typed[k + 1] + typed[k] + typed[k + 2:] == word:
        return {"typed": [p for p in ([typed[:k], False], [typed[k:k + 2], True], [typed[k + 2:], False]) if p[0]],
                "word": [p for p in ([word[:k], False], [word[k:k + 2], True], [word[k + 2:], False]) if p[0]]}
    sm = difflib.SequenceMatcher(None, typed, word, autojunk=False)
    t_out, w_out = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if i2 > i1:
            t_out.append([typed[i1:i2], op != "equal"])
        if j2 > j1:
            w_out.append([word[j1:j2], op != "equal"])
    return {"typed": t_out, "word": w_out}


def letter_hint(typed: str, word: str) -> str:
    """'acsident → accident: cs should be cc'; 'knowlege → knowledge: add d after le'; 'becuase → because: swap
    the u and a'; 'recieve → receive: swap the i and e (e before i after c)'; at most two changes."""
    typed, word = typed.strip(), word.strip()
    if not typed or typed.lower() == word.lower() or len(typed) > 2 * len(word) + 3:
        return ""
    t, w = typed.lower(), word.lower()
    sm = difflib.SequenceMatcher(None, t, w, autojunk=False)
    if sm.ratio() < 0.6:                                        # a different word altogether: no letter hint
        return ""
    bits = []
    k = swapped(t, w)
    if k is not None:
        t = t[:k] + t[k + 1] + t[k] + t[k + 2:]
        bits.append("swap the %s and %s%s" % (typed.lower()[k], typed.lower()[k + 1], _swap_note(t, k)))
    ops = _ops(t, w)
    if (not ops and not bits) or len(ops) + len(bits) > 2:
        return ""
    for op, i1, i2, j1, j2 in ops:
        if op == "replace" and i2 - i1 == 1 and j2 - j1 == 1 and i1 > 0 and w[j1] in (w[j1 - 1], w[j1 + 1:j1 + 2]):
            bits.append("%s should be %s" % (t[i1 - 1:i2], w[j1 - 1:j2]))         # cs should be cc
        elif op == "replace" and i2 - i1 == 1 and j2 - j1 == 1:
            # one letter: "s should be c" (prejudise); with the letter before it when the letter comes twice
            ctx = 1 if i1 > 0 and t.count(t[i1]) > 1 else 0
            bits.append("%s should be %s" % (t[i1 - ctx:i2], w[j1 - ctx:j2]))      # pe should be pa (seperate)
        elif op == "replace":
            bits.append("%s should be %s" % (t[i1:i2], w[j1:j2]))
        elif op == "insert":
            add = w[j1:j2]
            if len(add) == 1 and add in (w[j1 - 1:j1], w[j2:j2 + 1]):
                bits.append("%s should be %s" % (add, add * 2))                    # c should be cc
            elif j1 > 0:
                bits.append("add %s after %s" % (add, w[:j1] if j1 <= 3 else w[j1 - 2:j1]))
            else:
                bits.append("it starts with %s" % w[:j2 + 1])
        else:                                                                      # letters to take out
            gone = t[i1:i2]
            if len(gone) == 1 and gone in (t[i1 - 1:i1], t[i2:i2 + 1]):
                bits.append("%s should be %s" % (gone * 2, gone))                  # ss should be s
            else:
                bits.append("take out the %s" % gone)
    return "%s → %s: %s" % (typed, word, "; ".join(bits))
