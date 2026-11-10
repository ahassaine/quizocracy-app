"""A question stays put until it is answered (refresh or Back cannot swap it), a missed item comes back only
after a real gap, a right answer copied straight after the correction counts for today but not as learned or
put right, verbs start at the child's level and never repeat back to back, and maths avoids exact repeats and
the skills the Numbers-in-words activity already covers."""
import datetime

import requests

from conftest import BASE, DB, add_child, enter_child, signup

ALL = ("maths", "tables", "spelling", "grammar", "science", "numbers", "verbs")


def _kid(page, year, name="Rami", acts=ALL):
    signup(page)
    pid = add_child(page, name, year)
    DB.pupils.update_one({"_id": pid}, {"$set": {"activities": {k: {"on": k in acts, "target": 10} for k in ALL}},
                                        "$unset": {"plan_log": ""}})
    enter_child(page, name)
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return pid, s


def _next(s, act, **body):
    q = s.post(BASE + f"/api/{act}/next", json=body).json()
    assert q.get("ok"), (act, q)
    return q


def _wrong(s, act, token):
    body = {"past": "zzqx", "pp": "zzqx"} if act == "verbs" else {"value": "zzqx-9999"}
    r = s.post(BASE + f"/api/{act}/check", json={"token": token, **body}).json()
    assert r["correct"] is False, (act, r)
    return r


def _age_attempts(pid, minutes=10):
    """As if the last answers were given some minutes ago (the gap a missed item waits for)."""
    for r in DB.attempts.find({"pupil_id": pid}):
        DB.attempts.update_one({"_id": r["_id"]}, {"$set": {"ts": r["ts"] - datetime.timedelta(minutes=minutes)}})


def test_refresh_serves_the_same_question_until_answered(page):
    pid, s = _kid(page, 5)
    for act in ALL:
        a = _next(s, act)
        b = _next(s, act)                      # a refresh, Back or a second tab
        assert a["token"] == b["token"], act
        _wrong(s, act, a["token"])
        assert _next(s, act)["token"] != a["token"], act


def test_a_missed_question_comes_back_after_a_gap_not_straight_away(page):
    pid, s = _kid(page, 4)
    q = _next(s, "grammar")
    missed = DB.items.find_one({"_id": q["token"]})["meta"]
    _wrong(s, "grammar", q["token"])
    for _ in range(6):                          # five other questions, well within a few minutes
        q = _next(s, "grammar")
        it = DB.items.find_one({"_id": q["token"]})["meta"]
        assert (it["skill"], it["qid"]) != (missed["skill"], missed["qid"])
        _wrong(s, "grammar", q["token"])
    st = DB.bank_state.find_one({"_id": f"{pid}:grammar"})
    DB.bank_state.update_one({"_id": st["_id"]}, {"$set": {"retry": [
        dict(r, after=r["after"] - datetime.timedelta(minutes=10)) for r in st["retry"]]}})
    q = _next(s, "grammar")
    it = DB.items.find_one({"_id": q["token"]})["meta"]
    assert (it["skill"], it["qid"], it["reason"]) == (missed["skill"], missed["qid"], "retry")


def test_a_copied_answer_counts_today_but_is_not_learned_or_put_right(page):
    pid, s = _kid(page, 4)
    q = _next(s, "spelling")
    word = DB.items.find_one({"_id": q["token"]})["answer"]
    r = _wrong(s, "spelling", q["token"])
    assert r["expected"] == word
    # "Practise my mistakes" straight away: the word waits for a gap
    f = _next(s, "spelling", fix=1)
    assert not f["fixing"] and f["fix_later"] == 1
    other = DB.items.find_one({"_id": f["token"]})["answer"]
    assert other != word
    assert s.post(BASE + "/api/spelling/check", json={"token": f["token"], "value": other}).json()["correct"]
    # the same word served within the gap (as a stray repeat would be), typed from the correction
    DB.items.insert_one({"_id": "copy-" + pid, "pupil_id": pid, "family_id": DB.pupils.find_one({"_id": pid})["family_id"],
                         "activity": "spelling", "answer": word, "meta": {}, "created": datetime.datetime.utcnow(),
                         "done": False})
    r = s.post(BASE + "/api/spelling/check", json={"token": "copy-" + pid, "value": word}).json()
    assert r["correct"] and r["again_later"], r
    assert DB.spelling_words.find_one({"_id": f"{pid}:{word}"})["box"] == 0          # not one step nearer learned
    assert DB.attempts.count_documents({"pupil_id": pid, "activity": "spelling", "correct": True}) == 2   # today
    # in a later sitting (few questions in between, but over half an hour), the word is ready to put right
    _age_attempts(pid, 40)
    f = _next(s, "spelling", fix=1)
    assert f["fixing"] and DB.items.find_one({"_id": f["token"]})["answer"] == word


def test_verbs_start_at_the_childs_level_and_never_repeat_back_to_back(page):
    pid, s = _kid(page, 8)
    prev, levels = None, []
    for _ in range(14):
        q = _next(s, "verbs")
        assert q["base"] != prev
        prev = q["base"]
        levels.append(q["level"])
        ans = DB.items.find_one({"_id": q["token"]})["answer"]
        r = s.post(BASE + "/api/verbs/check", json={"token": q["token"], "past": ans["past"][0], "pp": ans["pp"][0]}).json()
        assert r["correct"], r
    assert levels[0] == 4                       # Year 8 starts on level 4 of 8, not the everyday verbs
    assert levels[-1] == 5                      # ten right in a row moved her up


def test_maths_leaves_numbers_in_words_skills_and_never_repeats_a_question(page):
    pid, s = _kid(page, 5)
    prompts = []
    for _ in range(12):
        q = _next(s, "maths")
        assert q["skill"] != "Y5.0.a"            # read and write numbers to 1,000,000: the Numbers-in-words activity
        prompts.append(q["prompt"])
        s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": "zzqx"})
    assert len(set(prompts)) == len(prompts), prompts


def test_maths_without_numbers_in_words_starts_on_place_value(page):
    pid, s = _kid(page, 5, acts=("maths",))
    assert _next(s, "maths")["skill"] == "Y5.0.a"
