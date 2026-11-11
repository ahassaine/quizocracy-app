"""The drill pages for young children: questions read aloud (speak.js), a happy "Correct" and kind words after
a run of misses, tap buttons for a few fixed words, tap-between-letters for "Put spaces between the words",
place-value blocks without a Hundreds column in Years 1-2, and table cells that type into the answer box."""
import json

from conftest import BASE, add_child, enter_child, signup, wait_question

# speechSynthesis stand-in: records what is said, and (like Chrome and Safari) refuses until the page has had a tap.
# "Had a tap" is a real (trusted) tap or key seen on this page, not navigator.userActivation: headless Chrome now and
# then reports a page it opened as already activated, with no input at all, and the test then hears speech that a
# real first visit would not allow.
STUB = """
window.__said = []; window.__tapped = false;
['pointerdown', 'mousedown', 'click', 'keydown', 'touchend'].forEach(t => window.addEventListener(t, e => {
  if (e.isTrusted) window.__tapped = true; }, true));
(function () { const s = window.speechSynthesis; if (!s) return;
  s.speak = function (u) { const ok = window.__tapped;
    setTimeout(() => { if (!ok) { u.onerror && u.onerror({ error: 'not-allowed' }); return; }
      if (u.text.trim()) window.__said.push(u.text); u.onstart && u.onstart({}); setTimeout(() => u.onend && u.onend({}), 20); }, 5); };
  s.cancel = function () {}; })();
"""
DAY = {"done": 0, "target": 5, "day_pct": 0, "reward": ""}


def _kid(browser, year, mobile=False):
    ctx = browser.new_context(base_url=BASE, **({"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}
                                                if mobile else {}))
    ctx.add_init_script(STUB)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Maya", year)
    enter_child(pg, "Maya")
    return pg, pid


def _said(pg):
    return " ".join(pg.evaluate("window.__said"))


def test_year1_hears_the_question_after_one_tap_and_is_cheered(browser):
    pg, pid = _kid(browser, 1)
    pg.goto("/me/maths")
    doc = wait_question(pg, "maths", pid)
    btn = pg.locator("[data-testid=speak]")
    assert "first" in btn.get_attribute("class") and "Tap to hear" in btn.inner_text()   # no sound before a tap
    assert pg.evaluate("window.__said") == []
    btn.click()
    pg.wait_for_function("window.__said.length > 0")
    pg.wait_for_function("!document.getElementById('speak').classList.contains('first')")
    assert pg.evaluate("s => Speak.natural(s)", doc["prompt"])[:12] in _said(pg)
    prev = doc["_id"]
    for i in range(2):                                    # two misses in a row: a kind word, and it is read out
        pg.evaluate("() => { document.getElementById('mHost').__getValue = () => 'definitely wrong'; }")
        pg.click("#check")
        pg.wait_for_selector("#feedback.no")
        assert pg.locator("[data-testid=kind]").count() == i
        pg.click("#next")
        doc = wait_question(pg, "maths", pid, prev)
        prev = doc["_id"]
    assert "Good try!" in _said(pg)
    pg.wait_for_function("p => window.__said.join(' ').includes(p)",            # the next question reads itself
                         arg=pg.evaluate("s => Speak.natural(s)", doc["prompt"]).split(".")[0])
    pg.evaluate("v => { document.getElementById('mHost').__getValue = () => v; }", doc["answer"])
    pg.click("#check")
    pg.wait_for_selector("#feedback.yes.joy .joy-star")
    assert "Correct!" in pg.inner_text("#feedback")
    assert "Skill score" not in pg.inner_text("#mastery")                        # no dropping score for a 5-year-old
    pg.context.close()


def test_year8_gets_the_button_only_and_a_quiet_correct(browser):
    pg, pid = _kid(browser, 8)
    pg.goto("/me/maths")
    doc = wait_question(pg, "maths", pid)
    btn = pg.locator("[data-testid=speak]")
    assert "first" not in btn.get_attribute("class")
    pg.click("h1")                                        # a tap on the page reads nothing by itself
    pg.wait_for_timeout(200)
    assert pg.evaluate("window.__said") == []
    btn.click()
    pg.wait_for_function("window.__said.length > 0")
    pg.evaluate("v => { document.getElementById('mHost').__getValue = () => v; }", doc["answer"])
    pg.click("#check")
    pg.wait_for_selector("#feedback.yes")
    assert pg.locator("#feedback.joy").count() == 0 and pg.locator("#feedback .tick.quiet").count() == 1
    # every year sees the skill and a small bar; scores and counts are on the parent's pages
    assert "Skill score" not in pg.inner_text("#stage") and pg.is_visible("#mastery")
    pg.context.close()


def test_speech_says_symbols_as_words(browser):
    pg, pid = _kid(browser, 3)
    pg.goto("/me/maths")
    wait_question(pg, "maths", pid)
    nat = lambda s: pg.evaluate("s => Speak.natural(s)", s)               # noqa: E731
    assert nat("7 × 8") == "7 times 8"
    assert nat("I walk ___ school.") == "I walk blank school."
    assert nat("It is i__.") == "It is i, blank."
    assert nat("Is −62 greater than -70? (type 'yes' or 'no')") == "Is minus 62 greater than minus 70? type yes or no"
    assert nat("3/4 of 12 = ___") == "3 quarters of 12 equals blank"
    assert nat("12 - 5 = 7") == "12 minus 5 equals 7"
    assert nat("Kofi's dog") == "Kofi's dog"
    pg.context.close()


def _fake(pg, act, q, res, sent):
    pg.route(f"**/api/{act}/next", lambda r: r.fulfill(json={"ok": True, "token": "t-" + act, "day": DAY, **q}))
    pg.route(f"**/api/{act}/check", lambda r: (sent.append(json.loads(r.request.post_data)),
                                               r.fulfill(json={"ok": True, "day": DAY, **res})))


def test_fixed_words_are_buttons(browser):
    sent = []
    pg, _ = _kid(browser, 2, mobile=True)
    _fake(pg, "science", {"kind": "text", "prompt": "Is a glass bottle living, dead or never alive?", "skill": "Living things",
                          "strand": "Biology", "reason": "new", "score": 0},
          {"correct": True, "expected": "never alive", "why": "", "score": 10}, sent)
    pg.goto("/me/science")
    pg.wait_for_selector("[data-testid=choices]")
    assert pg.locator("#answer").is_hidden()                                     # Year 2: no box to spell "never alive"
    assert pg.locator("[data-testid=choices] .opt").all_inner_texts() == ["Living", "Dead", "Never alive"]
    pg.click("[data-testid=choice-2]")
    pg.click("#check")
    pg.wait_for_selector("#feedback.yes")
    assert sent[-1]["value"] == "never alive"
    assert "right" in pg.get_attribute("[data-testid=choice-2]", "class")
    pg.context.close()

    sent = []
    pg, _ = _kid(browser, 6)
    _fake(pg, "maths", {"component": "number", "spec": {"text": True, "keypad": "text", "placeholder": "yes or no"},
                        "prompt": "Is 91 a prime number? Type yes or no.", "title": "Primes", "strand": "Number",
                        "reason": "new", "score": 0, "progress": {"mastered": 0, "total": 9}},
          {"correct": False, "expected": "no", "solution": [], "score": 0, "progress": {"mastered": 0, "total": 9}}, sent)
    pg.goto("/me/maths")
    pg.wait_for_selector("[data-testid=choices]")
    assert pg.locator("#mHost input.m-input").is_visible()                       # Year 6: buttons and the box
    pg.click("[data-testid=choice-0]")
    assert pg.input_value("#mHost input.m-input") == "yes"
    pg.click("#check")
    pg.wait_for_selector("#feedback.no")
    assert sent[-1]["value"] == "yes" and "right" in pg.get_attribute("[data-testid=choice-1]", "class")
    pg.context.close()


def test_put_spaces_by_tapping_between_letters(browser):
    sent = []
    pg, _ = _kid(browser, 1, mobile=True)
    _fake(pg, "grammar", {"kind": "write", "prompt": "Put spaces between the words.", "s": "Ilikecake.",
                          "skill": "Spaces", "strand": "Punctuation", "reason": "new", "score": 0},
          {"correct": True, "expected": "I like cake.", "why": "", "score": 10}, sent)
    pg.goto("/me/grammar")
    pg.wait_for_selector("[data-testid=gaps]")
    pg.tap("[data-testid=gap-1]")
    pg.tap("[data-testid=gap-5]")
    pg.tap("[data-testid=gap-3]")
    pg.tap("[data-testid=gap-3]")                                               # a second tap takes it away
    pg.tap("#check")
    pg.wait_for_selector("#feedback.yes")
    assert sent[-1]["value"] == "I like cake."
    pg.context.close()


def test_blocks_and_tables(browser):
    pg, pid = _kid(browser, 1)
    pg.goto("/me/maths")
    wait_question(pg, "maths", pid)
    render = """([n, s, a]) => { const h = document.getElementById('mHost'); h.innerHTML = '';
                 MComp[n].render(h, s, Object.assign({ submit() {} }, a)); }"""
    pg.evaluate(render, ["base_ten", {"mode": "build", "max": 9}, {"year": 1, "prompt": "Make seventeen with the blocks."}])
    assert pg.locator("#mHost [id^=bt-]").count() == 2 and pg.locator("#bt-h").count() == 0   # Tens and Ones only
    for _ in range(10):
        pg.click("#mHost button[aria-label='Add a one block']")
    assert "10 ones make a ten" in pg.inner_text("[data-testid=blocks-tip]")
    pg.evaluate(render, ["base_ten", {"mode": "build", "max": 9}, {"year": 4, "prompt": "Make 345 with the blocks."}])
    assert pg.locator("#bt-h").count() == 1

    pg.evaluate(render, ["io_table", {"rows": [[1, ""], [2, 16]], "missing": 0, "keypad": "numeric"}, {}])
    assert "Rule: ?" not in pg.inner_text("#mHost")                              # the Out number is asked, not the rule
    pg.click("[data-testid=blank-cell]")
    pg.keyboard.type("11")
    assert pg.inner_text("[data-testid=blank-cell]") == "11"
    pg.evaluate(render, ["io_table", {"rows": [[1, 11], [2, 16]], "keypad": "text"}, {}])
    assert "Rule: ?" in pg.inner_text("#mHost")                                  # the rule is what is asked
    pg.evaluate(render, ["data_table", {"headers": ["In numerals", "In words"], "rows": [["8,300", ""]], "missing": [0, 1],
                                        "keypad": "text"}, {}])
    pg.click("[data-testid=blank-cell]")
    pg.keyboard.type("eight thousand three hundred")
    assert pg.evaluate("document.querySelector('#mHost input.m-input').offsetWidth") > 300   # grew to fit
    pg.context.close()


def _slip(text):
    """One misspelt word: "eight" -> "eigth" (the last two letters swapped)."""
    ws = text.split()
    i = next(i for i, w in enumerate(ws) if len(w) >= 5 and w.isalpha() and w[-1] != w[-2])
    ws[i] = ws[i][:-2] + ws[i][-1] + ws[i][-2]
    return " ".join(ws)


def test_near_miss_spelling_gets_one_more_go(browser):
    from conftest import DB
    pg, pid = _kid(browser, 4)
    pg.goto("/me/numbers")
    prev = None
    for _ in range(25):                                  # a "write it in words" question with a long enough word
        doc = wait_question(pg, "numbers", pid, prev)
        prev = doc["_id"]
        if doc["meta"]["mode"] == "words" and any(len(w) >= 5 and w.isalpha() and w[-1] != w[-2] for w in doc["answer"].split()):
            break
        pg.fill("#answer", "1"); pg.click("#check"); pg.wait_for_selector("#feedback.yes, #feedback.no"); pg.click("#next")
    pg.fill("#answer", _slip(doc["answer"]))
    pg.click("#check")
    pg.wait_for_selector("#feedback.warn")
    assert "undefined" not in pg.inner_text("#feedback") and pg.inner_text("#feedback").strip()
    assert not pg.locator("#check").is_disabled() and DB.items.find_one({"_id": doc["_id"]})["done"] is False
    pg.click("#check")                                   # the same slip again: now marked, with the hint under the answer
    pg.wait_for_selector("#feedback.no")
    assert pg.locator("#feedback [data-testid=hint]").inner_text().strip()
    assert "undefined" not in pg.inner_text("#feedback")

    pg.goto("/me/science")
    prev = None
    for _ in range(40):                                  # a typed science word
        doc = wait_question(pg, "science", pid, prev)
        prev = doc["_id"]
        key = doc["answer"]
        if key["t"] == "text" and pg.locator("#answer").is_visible() and any(
                len(w) >= 6 and w.isalpha() and w[-1] != w[-2] for w in key["a"][0].split()):
            break
        if key["t"] == "mcq": pg.click(f"[data-testid=opt-{key['right']}]")
        elif key["t"] == "tap": pg.click("[data-testid=word-%d]" % key["hits"][0])
        elif pg.locator("#answer").is_visible(): pg.fill("#answer", str(key["a"] if key["t"] == "num" else key["a"][0]))
        else: pg.click("[data-testid=choice-0]")
        pg.click("#check"); pg.wait_for_selector("#feedback.yes, #feedback.no"); pg.click("#next")
    else:
        pg.context.close()
        return
    pg.fill("#answer", _slip(key["a"][0]))
    pg.click("#check")
    pg.wait_for_selector("#feedback.warn")
    assert "undefined" not in pg.inner_text("#feedback") and not pg.locator("#check").is_disabled()
    pg.context.close()
