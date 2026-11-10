"""Grammar and science marking and content after the fifth test wave (10 Nov 2026): a unit typed the keyboard
way is right, a name with its symbol too, and a wrong number never; a missing apostrophe is a punctuation slip
with its own retry; open rewrites say exactly what is checked; Year 6 meets apostrophes (and a parent can pick
them); typed wrong answers and formulae in word equations get their own "why not"; a Year 9 school topic from
Years 7-8 can be picked; a right answer has its "Why?"; and a question can be reported as too easy."""
import datetime
import re
from zoneinfo import ZoneInfo

import requests

from app.bank import engine
from app.routes.child import REPORT_REASONS

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup

TODAY = datetime.datetime.now(ZoneInfo("Europe/London")).date()
ALL = [(sub, sk, q) for sub in engine.load() for y in engine.load()[sub] for sk in engine.load()[sub][y] for q in sk["qs"]]


def test_a_number_with_its_unit_typed_any_usual_way_is_right_and_a_wrong_number_never():
    k = {"t": "num", "a": 4, "unit": "g/cm³"}
    for v in ["4", "4 g/cm3", "4 g/cm^3", "4g/cm³", "4 g cm-3", "4 g cm^-3", "4.0 g/cm3", "4 G/CM3",
              "4 grams per cubic centimetre", "4 g per cm3"]:
        assert engine.mark(k, v), v
    for v in ["5 g/cm3", "40 g/cm3", "4 kg/m3", "4 g/cm2", "4 kg", "4/7", "4 or 5 g/cm3", "3 g/cm3", "g/cm3"]:
        assert not engine.mark(k, v), v
    k = {"t": "num", "a": 9.8, "tol": 0.05, "unit": "m/s²"}
    for v in ["9.8 m/s2", "9.8 m s-2", "9.8 m/s/s", "9.8 ms-2", "9.8 m s^-2", "9.8 metres per second squared"]:
        assert engine.mark(k, v), v
    assert not engine.mark(k, "9.8 m/s") and not engine.mark(k, "9.9 m/s2") and not engine.mark(k, "98 m/s2")
    k = {"t": "num", "a": 1500, "unit": "W"}
    assert engine.mark(k, "1500 W") and engine.mark(k, "1,500 watts") and engine.mark(k, "1500 Watts")
    assert not engine.mark(k, "1500 kW") and not engine.mark(k, "1500 J") and not engine.mark(k, "15000 W")
    assert engine.mark({"t": "num", "a": 6, "unit": "m"}, "6 metres") and not engine.mark({"t": "num", "a": 6, "unit": "m"}, "6 m2")
    assert engine.mark({"t": "num", "a": 20, "unit": "ml"}, "20 cm3") and engine.mark({"t": "num", "a": 20, "unit": "cm³"}, "20 ml")
    assert not engine.mark({"t": "num", "a": 20, "unit": "ml"}, "20 l")
    # a question without a unit keeps its old rule: a word after the number is fine, more digits are not
    assert engine.mark({"t": "num", "a": 25}, "25kJ") and not engine.mark({"t": "num", "a": 25}, "25/30")
    # the served key carries the unit, so marking (and the parent's report) can use it
    q = engine.question("SC9.40", next(q["id"] for q in engine.skill("SC9.40")["qs"] if q["t"] == "num" and q["a"] == 4))
    pub, key = engine.serve(q)
    assert key["unit"] == "g/cm³" == pub["unit"] and engine.mark(key, "4 g/cm3")


def test_a_unit_name_with_its_symbol_in_brackets_is_right():
    k = {"t": "text", "a": ["watt", "watts", "W"], "loose": True}
    for v in ["watt (W)", "Watts (W)", "W (watt)", "watts(w)", "watt", "W"]:
        assert engine.mark(k, v), v
    for v in ["watt (J)", "joule (W)", "(W)", "joule", "kW"]:
        assert not engine.mark(k, v), v
    k = {"t": "text", "a": ["joule", "joules"], "loose": True}          # the symbol need not be listed
    assert engine.mark(k, "joule (J)") and engine.mark(k, "J") and not engine.mark(k, "joule (N)")
    k = {"t": "text", "a": ["kg/m³"], "loose": True}
    for v in ["kg/m3", "kg m-3", "kg/m^3", "kilograms per cubic metre", "kg per m3", "KG/M3"]:
        assert engine.mark(k, v), v
    assert not engine.mark(k, "kg/m2") and not engine.mark(k, "g/cm3")
    k = {"t": "text", "a": ["carbon dioxide", "CO2"], "loose": True}
    assert engine.mark(k, "carbon dioxide (CO2)") and engine.mark(k, "CO₂") and not engine.mark(k, "carbon dioxide (O2)")
    assert engine.mark({"t": "text", "a": ["kWh"], "loose": True}, "kilowatt-hours")
    # every listed science answer is still accepted, and still marks itself only
    for sub, sk, q in ALL:
        if sub == "science" and q["t"] in ("text", "num"):
            pub, key = engine.serve(q)
            right = q["a"][0] if q["t"] == "text" else str(q["a"])
            assert engine.mark(key, right), (sk["key"], q["id"])


def test_a_missing_apostrophe_is_a_punctuation_slip_not_the_grammar():
    sk, q = engine.skill("GP6.09"), engine.question("GP6.09", "89f3ca37233c")      # "You can swim, ___?"
    pub, key = engine.serve(q)
    for v in ["cant you", "ca'nt you", "Cant you?"]:
        s = engine.apostrophe_slip(key, v, sk)
        assert s and "apostrophe" in s["retry"] and "can't" in s["after"] and "cannot" in s["after"], v
    assert engine.apostrophe_slip(key, "can you", sk) is None and engine.apostrophe_slip(key, "can't you", sk) is None
    w = {"t": "write", "a": ["The dog's bowl is empty."]}
    assert "belonging" in engine.apostrophe_slip(w, "The dogs bowl is empty.", engine.skill("GP6.02"))["after"]
    # where the apostrophe is the skill it stays a mistake, and so does a homophone in a homophone skill
    assert engine.apostrophe_slip({"t": "text", "a": ["can't"]}, "cant", engine.skill("GP6.04")) is None
    homophones = next(s for s in engine.skills("grammar", 7) if engine.spelling_matters(s))
    assert engine.apostrophe_slip({"t": "text", "a": ["we're"]}, "were", homophones) is None


def test_open_rewrites_say_exactly_what_is_checked():
    for sub, sk, q in ALL:
        if sub == "grammar" and q["t"] == "write":
            assert q["q"] not in ("Rewrite formally with no contractions.", "Rewrite in Standard English.",
                                  "Rewrite this statement as an imperative."), (sk["key"], q["q"])
    formal = [q for q in engine.skill("GP8.07")["qs"] if q["t"] == "write" and "contraction" in q["q"]]
    assert formal and all(re.search(r"[Cc]hange nothing else", q["q"]) for q in formal)


def test_year6_apostrophes_come_up_and_can_be_the_school_focus():
    y6 = [s["key"] for s in engine.skills("grammar", 6)]
    assert y6.index("GP6.04") == 1                                       # straight after word classes
    assert "Apostrophes" in engine.focus_strands("grammar", 6)
    assert [s["key"] for s in engine.focus_skills("grammar", 6, ["Apostrophes"])] == ["GP6.04"]
    assert "GP6.04" in [s["key"] for s in engine.focus_skills("grammar", 6, ["Punctuation"])]
    assert "GP6.04" in [s["key"] for s in engine.focus_skills("grammar", 6, ["Test review"])]


def test_typed_wrong_answers_and_formulae_get_their_own_why_not():
    q = next(q for q in engine.skill("GP9.06")["qs"] if q["t"] == "text" and q["a"] == ["inversion"])
    pub, key = engine.serve(q)
    no, why = engine.why_lines(q, key, "Fronting")
    assert "swap" in no and "Fronting" in why
    q = next(q for q in engine.skill("SC9.16")["qs"] if "magnesium + oxygen" in q["q"])
    pub, key = engine.serve(q)
    assert "names, not formulae" in engine.why_lines(q, key, "MgO")[0]
    q = next(q for q in engine.skill("SC9.16")["qs"] if "iron + oxygen" in q["q"])     # no line of its own
    pub, key = engine.serve(q)
    assert "word equation uses the names" in engine.why_lines(q, key, "Fe2O3")[0]
    assert engine.why_lines(q, key, "iron sulfide")[0] == ""
    q = engine.question("GP8.01", "2ee3ad187384")
    no, _ = engine.why_lines(q, {"t": "mcq", "right": 0, "opts": q["opts"]}, q["opts"].index("The road has been busy this week."))
    assert "adjective" in no and "past participle" in no


def test_health_explanations_put_each_effect_with_its_cause():
    q = engine.question("SC9.02", "9f3eea623dab")
    assert "come from smoking" not in q["why"] and "brain damage" in q["why"].lower()
    assert "long-term" in q["no"]["Brain damage and memory loss"]
    for sub, sk, q in ALL:
        if sk["strand"] == "Health":
            assert not re.search(r"the others (come|are) from smoking", q["why"]), (sk["key"], q["id"])


def test_year9_can_pick_atoms_and_the_periodic_table():
    sk = engine.skill("SC9.50")
    assert sk["year"] == 9 and len(sk["qs"]) >= 20 and len({q["t"] for q in sk["qs"]}) >= 3
    strands = engine.focus_strands("science", 9)
    assert {"Atoms and the periodic table", "Atoms, elements and compounds", "The periodic table"} <= set(strands)
    note = engine.earlier_note("science", 9)
    assert note["Atoms, elements and compounds"] == " (Year 7–8 topic)" and "Atoms and the periodic table" not in note
    keys = [s["key"] for s in engine.focus_skills("science", 9, ["The periodic table"])]
    assert "SC9.50" in keys and "SC8.22" in keys
    assert not any(s["key"] in ("SC7.16", "SC7.17", "SC9.09") for s in engine.focus_skills("science", 9, strands))
    assert engine.focus_strands("science", 7) == list(dict.fromkeys(s["strand"] for s in engine.skills("science", 7)))
    assert "easy" in REPORT_REASONS and REPORT_REASONS["easy"] == "Too easy for this year"


def _session(ctx):
    s = requests.Session()
    for c in ctx.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _child(browser, name, year, targets=None):
    pg = browser.new_context(base_url=BASE).new_page()
    email = signup(pg)
    pid = add_child(pg, name, year, targets=targets)
    ctx = browser.new_context(base_url=BASE, viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    kid = ctx.new_page()
    kid.set_default_timeout(15000)
    kid.goto("/login")
    kid.fill("#email", email)
    kid.fill("#password", PASSWORD)
    kid.click("button[type=submit]")
    kid.wait_for_url("**/home")
    enter_child(kid, name)
    return pg, ctx, kid, pid


def _set_item(pid, activity, skill, qid):
    """The child's next question, made the one the test needs."""
    q = engine.question(skill, qid)
    pub, key = engine.serve(q)
    it = DB.items.find_one({"pupil_id": pid, "activity": activity, "done": {"$ne": True}}, sort=[("_id", -1)])
    DB.items.update_one({"_id": it["_id"]}, {"$set": {"meta.skill": skill, "meta.qid": qid, "meta.reason": "new",
                                                      "answer": key}})
    return it["_id"], q


def test_apostrophe_retry_and_unit_marking_through_the_api(browser):
    pg, ctx, kid, pid = _child(browser, "Aanya", 6)
    s = _session(ctx)
    s.post(BASE + "/api/grammar/next", json={})
    tok, _ = _set_item(pid, "grammar", "GP6.09", "89f3ca37233c")
    r = s.post(BASE + "/api/grammar/check", json={"token": tok, "value": "cant you"}).json()
    assert r["retry"] and "apostrophe" in r["hint"], r
    r = s.post(BASE + "/api/grammar/check", json={"token": tok, "value": "cant you"}).json()
    assert r["correct"] is False and "can't" in r["hint"] and "apostrophe" in r["hint"] and r["why"] == "", r
    ctx.close()
    pg.context.close()

    pg, ctx, kid, pid = _child(browser, "Ethan", 9)
    s = _session(ctx)
    s.post(BASE + "/api/science/next", json={})
    qid = next(q["id"] for q in engine.skill("SC9.40")["qs"] if q["t"] == "num" and q["a"] == 4)
    tok, _ = _set_item(pid, "science", "SC9.40", qid)
    r = s.post(BASE + "/api/science/check", json={"token": tok, "value": "4 g/cm3"}).json()
    assert r["correct"] is True and r["why"], r
    ctx.close()
    pg.context.close()


def test_a_year9_focus_on_a_year8_topic_serves_its_questions(browser):
    pg, ctx, kid, pid = _child(browser, "Ravi", 9, targets={"science": 5})
    pg.goto(f"/children/{pid}/edit")
    opts = pg.locator("[data-testid=focus-0] option").all_inner_texts()
    assert "Atoms, elements and compounds (Year 7–8 topic)" in opts and "Atoms and the periodic table" in opts, opts
    DB.pupils.update_one({"_id": pid}, {"$set": {"focus": [{"subject": "science", "strand": "Atoms, elements and compounds",
                                                            "weeks": 1, "from": TODAY.isoformat(),
                                                            "until": (TODAY + datetime.timedelta(days=7)).isoformat()}]}})
    s = _session(ctx)
    skills = []
    for _ in range(18):
        q = s.post(BASE + "/api/science/next", json={}).json()
        skills.append(q["strand"])
        s.post(BASE + "/api/science/check", json={"token": q["token"], "value": "zzzz" if q["kind"] != "mcq" else 0})
    assert sum(st in ("Atoms, elements and compounds", "Atoms and the periodic table") for st in skills) >= 7, skills
    ctx.close()
    pg.context.close()


def test_a_right_answer_has_a_why_toggle(browser):
    pg, ctx, kid, pid = _child(browser, "Mia", 9)
    kid.goto("/me/science")
    kid.wait_for_selector("#area .opt, #area .word, #answer")
    tok = kid.evaluate("document.body.dataset.qtoken")
    it = DB.items.find_one({"_id": tok})
    why = engine.question(it["meta"]["skill"], it["meta"]["qid"])["why"]
    # whatever is on screen, the first choice (or "zzz") is made the right answer
    if kid.locator("#area .opt").count():
        DB.items.update_one({"_id": tok}, {"$set": {"answer.right": 0}})
        kid.locator("#area .opt").first.click()
    elif kid.locator("#area .word").count():
        DB.items.update_one({"_id": tok}, {"$set": {"answer.hits": [0]}})
        kid.locator("#area .word").first.click()
    else:
        DB.items.update_one({"_id": tok}, {"$set": {"answer": {"t": "text", "a": ["zzz"]}}})
        kid.fill("#answer", "zzz")
    kid.click("#check")
    kid.wait_for_selector("[data-testid=why-right]")
    assert not kid.locator("[data-testid=why-right] .why").is_visible()
    kid.click("[data-testid=why-right] summary")
    assert kid.locator("[data-testid=why-right] .why").is_visible()
    assert kid.inner_text("[data-testid=why-right] .why").strip() == why.strip()
    ctx.close()
    pg.context.close()
