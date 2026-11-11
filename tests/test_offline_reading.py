"""A Wi-Fi blip mid-question (drill.js: the answer is kept, a note says so, it is sent again when the connection
is back and never counted twice), the "Aa" panel on top of the question card, reading settings that belong to
the child (and that a parent can set), read-aloud that does not move the question, and the words for a child on
a signed-out device."""
import re

import pytest

from conftest import BASE, DB, PASSWORD, add_child, enter_child, pending_item, signup, unlock_parent, wait_question

PHONE = {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}
TABLET = {"viewport": {"width": 820, "height": 1180}, "is_mobile": True, "has_touch": True}
NOTE = "No connection — your answer is safe. Trying again…"


def _family(browser, year=4, names=("Yusuf",), **kw):
    ctx = browser.new_context(base_url=BASE, **kw)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    email = signup(pg)
    pids = [add_child(pg, n, year) for n in names]
    enter_child(pg, names[0])
    return pg, pids, email


def _right(pg, act, doc):
    """Put the right answer on the page the way a child would, and return a function telling it is still there."""
    if act == "maths":
        pg.evaluate("v => { document.getElementById('mHost').__getValue = () => v; }", doc["answer"])
        return lambda: True
    if act == "spelling":
        pg.fill("#answer", doc["answer"])
        return lambda: pg.input_value("#answer") == doc["answer"]
    key = doc["answer"]
    if key["t"] == "mcq":
        pg.click(f"[data-testid=opt-{key['right']}]")
        return lambda: "sel" in pg.get_attribute(f"[data-testid=opt-{key['right']}]", "class")
    if key["t"] == "tap":
        for i in key["hits"]:
            pg.click(f"[data-testid=word-{i}]")
        return lambda: all("sel" in pg.get_attribute(f"[data-testid=word-{i}]", "class") for i in key["hits"])
    v = str(key["a"] if key["t"] == "num" else key["a"][0])
    pg.fill("#answer", v)
    return lambda: pg.input_value("#answer") == v


@pytest.mark.parametrize("act", ["maths", "grammar", "spelling"])
def test_a_wifi_blip_on_check_and_on_next(browser, act):
    pg, (pid,), _ = _family(browser, 5, **PHONE)
    pg.goto(f"/me/{act}")
    doc = wait_question(pg, act, pid)
    still = _right(pg, act, doc)
    pg.context.set_offline(True)
    pg.click("#check")
    pg.wait_for_selector("[data-testid=net-msg]:visible")
    assert pg.inner_text("[data-testid=net-msg]") == NOTE
    pg.wait_for_timeout(1500)                                          # a retry or two while still offline
    assert still() and pg.is_enabled("#check") and pg.is_hidden("#next")
    pg.click("#check")                                                 # tapping again does no harm
    pg.context.set_offline(False)                                      # back online: it goes by itself
    pg.wait_for_selector("#feedback.yes", timeout=10000)
    assert pg.is_hidden("[data-testid=net-msg]") and pg.is_visible("#next")
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": act}) == 1          # counted once
    # Next while offline: the answered question, its "Correct" and Next stay; the new question comes when back
    pg.context.set_offline(True)
    pg.click("#next")
    pg.wait_for_selector("[data-testid=net-msg]:visible")
    pg.wait_for_timeout(1200)
    assert "Correct" in pg.inner_text("#feedback") and pg.is_visible("#next") and pg.is_disabled("#check")
    pg.context.set_offline(False)
    doc2 = wait_question(pg, act, pid, doc["_id"])
    assert pg.is_hidden("[data-testid=net-msg]") and pg.is_hidden("#next") and pg.inner_text("#feedback") == ""
    _right(pg, act, doc2)
    pg.click("#check")
    pg.wait_for_selector("#feedback.yes")
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": act}) == 2
    pg.context.close()


def test_an_answer_that_arrived_before_the_connection_dropped_is_not_counted_twice(browser):
    pg, (pid,), _ = _family(browser, 5)
    pg.goto("/me/spelling")
    doc = wait_question(pg, "spelling", pid)
    lost = []

    def drop_reply(route):                        # the server marks it, the reply never reaches the tablet
        if not lost:
            lost.append(route.fetch().status)
            route.abort()
        else:
            route.continue_()
    pg.route("**/api/spelling/check", drop_reply)
    pg.fill("#answer", doc["answer"])
    pg.click("#check")
    pg.wait_for_function("document.body.dataset.qtoken && document.body.dataset.qtoken !== %r" % doc["_id"], timeout=10000)
    assert lost == [200]
    assert "Your answer was marked" in pg.inner_text("#feedback")
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": "spelling"}) == 1
    pg.context.close()


def test_report_is_sent_when_the_connection_is_back(browser):
    pg, (pid,), _ = _family(browser, 5)
    pg.goto("/me/grammar")
    wait_question(pg, "grammar", pid)
    pg.click("[data-testid=report-open]")
    pg.click("[data-reason=nonsense]")
    pg.context.set_offline(True)
    pg.click("[data-testid=report-send]")
    pg.wait_for_selector("[data-testid=net-msg]:visible")
    assert "report is safe" in pg.inner_text("[data-testid=net-msg]")
    pg.context.set_offline(False)
    pg.wait_for_function("document.querySelector('[data-testid=report-msg]').textContent.includes('Thanks')")
    assert DB.reports.count_documents({"pupil_id": pid}) == 1
    pg.context.close()


def _panel_on_top(pg):
    """Every checkbox of the open panel is the top element where a finger would land."""
    return pg.evaluate("""() => [...document.querySelectorAll('#a11yPanel input[data-a11y], #a11yPanel .a11y-ttl')].every(el => {
        const r = el.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
        const hit = document.elementFromPoint(x, y);
        return r.width > 0 && hit && hit.closest('#a11yPanel');
    })""")


@pytest.mark.parametrize("dev", ["phone", "tablet", "laptop"])
def test_aa_opens_on_top_of_the_question(browser, dev):
    kw = {"phone": PHONE, "tablet": TABLET, "laptop": {"viewport": {"width": 1280, "height": 800}}}[dev]
    pg, (pid,), _ = _family(browser, 4, **kw)
    for path in ("/me/maths", "/me/grammar", "/me/spelling", "/me/tables/year4-check", "/me"):
        pg.goto(path)
        if path != "/me" and "year4" not in path:
            wait_question(pg, path.rsplit("/", 1)[1], pid)
        pg.click("[data-testid=a11y-open]")                    # straight away, while the cards are still rising
        assert _panel_on_top(pg), (dev, path)
        pg.wait_for_timeout(700)
        assert _panel_on_top(pg), (dev, path)
        pg.click("[data-testid=a11y-big]")
        assert "a11y-big" in pg.evaluate("document.documentElement.className")
        assert pg.is_visible("[data-testid=a11y-panel]")           # a tap inside keeps it open
        pg.click("[data-testid=a11y-big]")
        pg.click("#a11yDone")
        assert pg.is_hidden("[data-testid=a11y-panel]")
    pg.context.close()


def test_reading_settings_belong_to_the_child(browser):
    pg, (leila, sami), email = _family(browser, 4, names=("Leila", "Sami"))
    pg.goto("/me/maths")
    pg.click("[data-testid=a11y-open]")
    assert "Leila's, on every device" in pg.inner_text("[data-testid=a11y-note]")
    pg.click("[data-testid=a11y-dys]")
    pg.click("[data-testid=a11y-space]")
    pg.wait_for_function("() => true")
    pg.wait_for_timeout(500)
    assert DB.pupils.find_one({"_id": leila})["reading"] == {"big": False, "dys": True, "space": True, "calm": False, "contrast": False}
    # a sibling on the same tablet: their own (none)
    enter_child(pg, "Sami")
    assert "a11y-" not in pg.evaluate("document.documentElement.className")
    # the parent's pages and the printable report: none of Leila's
    unlock_parent(pg)
    for path in ("/home", f"/children/{leila}"):
        pg.goto(path)
        assert "a11y-" not in pg.evaluate("document.documentElement.className"), path
    # the parent sets Sami's in his settings, and Leila's follow her to Grandma's tablet
    pg.goto(f"/children/{sami}/edit")
    assert pg.is_checked("[data-testid=read-dys]") is False
    pg.check("[data-testid=read-big]")
    pg.check("[data-testid=calm]")             # "Calm screen" (wave 6): the grown-up's, beside Reading
    pg.click("form.card button[type=submit] >> text=Save")
    pg.wait_for_url("**saved=1*")
    assert DB.pupils.find_one({"_id": sami})["reading"] == {"big": True, "dys": False, "space": False, "calm": False, "contrast": False}
    assert DB.pupils.find_one({"_id": sami})["calm"] is True
    pg.goto(f"/children/{leila}/edit")
    assert pg.is_checked("[data-testid=read-dys]") and pg.is_checked("[data-testid=read-space]")
    gran = browser.new_context(base_url=BASE, **PHONE).new_page()
    gran.set_default_timeout(15000)
    gran.goto("/login")
    gran.fill("#email", email)
    gran.fill("#password", PASSWORD)
    gran.click("button[type=submit]")
    gran.wait_for_url("**/home")
    enter_child(gran, "Leila")
    cls = gran.evaluate("document.documentElement.className")
    assert "a11y-dys" in cls and "a11y-space" in cls and "a11y-big" not in cls
    enter_child(gran, "Sami")
    cls = gran.evaluate("document.documentElement.className")
    assert "a11y-big" in cls and "a11y-calm" in cls and "a11y-dys" not in cls
    gran.context.close()
    pg.context.close()


def test_reading_change_made_offline_reaches_the_server(browser):
    pg, (pid,), _ = _family(browser, 4)
    pg.goto("/me")
    pg.context.set_offline(True)
    pg.click("[data-testid=a11y-open]")
    pg.click("[data-testid=a11y-big]")
    pg.wait_for_timeout(300)
    assert not DB.pupils.find_one({"_id": pid}).get("reading")
    pg.context.set_offline(False)
    pg.wait_for_function("() => true")
    for _ in range(20):
        if (DB.pupils.find_one({"_id": pid}).get("reading") or {}).get("big"):
            break
        pg.wait_for_timeout(250)
    assert DB.pupils.find_one({"_id": pid})["reading"]["big"] is True
    pg.context.close()


def test_read_aloud_does_not_move_the_question(browser):
    ctx = browser.new_context(base_url=BASE, **PHONE)          # narrow: the question wraps beside the button
    ctx.add_init_script("""(function () { const s = window.speechSynthesis; if (!s) return;
      s.speak = function (u) { const ok = navigator.userActivation ? navigator.userActivation.hasBeenActive : true;
        setTimeout(() => { if (!ok) { u.onerror && u.onerror({ error: 'not-allowed' }); return; }
          window.__said = (window.__said || []).concat([u.text]); u.onstart && u.onstart({}); setTimeout(() => u.onend && u.onend({}), 20); }, 5); };
      s.cancel = function () {}; })();""")
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    signup(pg)
    pid = add_child(pg, "Jack", 1)
    enter_child(pg, "Jack")
    pg.goto("/me/maths")
    wait_question(pg, "maths", pid)
    assert "Tap to hear" in pg.inner_text("[data-testid=speak]")
    pg.wait_for_timeout(900)                                   # the card's entrance animation is over
    before = pg.evaluate("[document.getElementById('mHost').getBoundingClientRect().top, document.querySelector('.m-prompt').getBoundingClientRect().height]")
    pg.click("[data-testid=speak]")
    pg.wait_for_function("!document.getElementById('speak').classList.contains('first')")
    after = pg.evaluate("[document.getElementById('mHost').getBoundingClientRect().top, document.querySelector('.m-prompt').getBoundingClientRect().height]")
    assert abs(after[0] - before[0]) < 2 and after[1] == before[1], (before, after)
    # a tap in the wrong place is said aloud too ("Tap the number line first.", "Type your answer first.")
    pg.evaluate("() => { document.getElementById('mHost').__getValue = () => null; }")
    pg.click("#check")
    msg = pg.inner_text("#feedback")
    assert msg
    pg.wait_for_function("m => (window.__said || []).join(' ').includes(m.replace(/\\.$/, ''))", arg=msg)
    ctx.close()


def test_child_lines_on_landing_and_sign_in_and_a_signed_out_device(browser):
    ctx = browser.new_context(base_url=BASE, **PHONE)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    line = "Children: ask your parent to sign in once on this phone or tablet, then you just use your PIN."
    pg.goto("/")
    assert line in pg.inner_text("[data-testid=kid-line]")
    pg.goto("/login")
    assert line in pg.inner_text("[data-testid=kid-line]") and pg.locator("[data-testid=kid-signed-out]").count() == 0
    email = signup(pg)
    add_child(pg, "Yusuf", 6)
    enter_child(pg, "Yusuf")
    acc = DB.accounts.find_one({"email": email})
    DB.sessions.delete_many({"account_id": acc["_id"]})       # what a password reset does on every device
    pg.goto("/me")
    pg.wait_for_url("**/login?kid=1")
    assert "This device was signed out." in pg.inner_text("[data-testid=kid-signed-out]")
    assert "Ask a grown-up to sign in again" in pg.inner_text("[data-testid=kid-signed-out]")
    assert pg.is_visible("#email")                             # the grown-up's form is still there
    # signing out on purpose is not "signed out" for a child
    pg.fill("#email", email)
    pg.fill("#password", PASSWORD)
    pg.click("button[type=submit]")
    pg.wait_for_url("**/learn")                                # signed in from a child's page: back to "Who's learning?"
    pg.goto("/home")
    pg.click("form[action='/logout'] button")
    pg.goto("/login")
    assert pg.locator("[data-testid=kid-signed-out]").count() == 0
    ctx.close()


def test_unlock_boxes_ask_for_any_grown_ups_password(browser):
    pg, (pid,), _ = _family(browser, 4)
    pg.goto("/parent-unlock")
    assert pg.inner_text("label[for=password]") == "Your password (any grown-up in this family)"
    for _ in range(8):                                           # lock the PIN with wrong guesses
        pg.goto("/learn")
        f = pg.get_by_test_id("pin-Yusuf")
        if not f.count():
            break
        f.locator("input[name=pin]").fill("9999")
        f.locator("button").click()
    pg.goto("/learn")
    pg.click("summary:has-text('Unlock Yusuf now')")
    lbl = pg.inner_text(f"label[for=upw-{pid}]")
    assert lbl == "Your password (any grown-up in this family)" and "Parent password" not in pg.content()
    pg.context.close()
