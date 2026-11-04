"""Load: nine children (Years 1-9) practise maths at once against the running server.
Every question is served and graded right, nothing errors, and one answer token
fired eight times in parallel is counted exactly once."""
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from conftest import BASE, DB, PASSWORD, add_child, enter_child, signup

PER_CHILD = 120


def _session_for(browser, email, name):
    ctx = browser.new_context(base_url=BASE)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    pg.goto("/login")
    pg.fill("#email", email)
    pg.fill("#password", PASSWORD)
    pg.click("button[type=submit]")
    pg.wait_for_url("**/home")
    enter_child(pg, name)
    s = requests.Session()
    for c in ctx.cookies():
        s.cookies.set(c["name"], c["value"])
    ctx.close()
    return s


def _practise(s, pid, seed):
    rnd = random.Random(seed)
    lat, bad = [], []
    for _ in range(PER_CHILD):
        t0 = time.time()
        r = s.post(BASE + "/api/maths/next", json={})
        lat.append(time.time() - t0)
        if r.status_code != 200 or not r.json().get("ok"):
            bad.append("next %s %s" % (r.status_code, r.text[:120]))
            continue
        q = r.json()
        doc = DB.maths_lab_q.find_one({"_id": q["token"]})
        if not doc or doc.get("pupil") not in (pid, pid.lower()):
            bad.append("token %s not stored for %s" % (q["token"], pid))
            continue
        right = rnd.random() < 0.7
        t0 = time.time()
        r = s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": str(doc["answer"]) if right else "definitely wrong",
                                                     "ms": 3000})
        lat.append(time.time() - t0)
        if r.status_code != 200:
            bad.append("check %s %s" % (r.status_code, r.text[:120]))
        elif bool(r.json().get("correct")) != right:
            bad.append("%s graded %s for %r (%s)" % (doc.get("skill"), r.json().get("correct"), doc["answer"], doc.get("answer_type")))
    return lat, bad


def test_nine_children_at_once(browser):
    kids, sessions = {}, {}
    for fam in ((1, 2, 3), (4, 5, 6), (7, 8, 9)):           # three families of three children
        pg = browser.new_context(base_url=BASE).new_page()
        pg.set_default_timeout(15000)
        email = signup(pg)
        for y in fam:
            kids["Kid%d" % y] = add_child(pg, "Kid%d" % y, y, targets={"maths": 50})
            sessions["Kid%d" % y] = _session_for(browser, email, "Kid%d" % y)
    with ThreadPoolExecutor(9) as ex:
        res = list(ex.map(lambda n: _practise(sessions[n], kids[n], hash(n)), kids))
    lat = [x for r in res for x in r[0]]
    bad = [x for r in res for x in r[1]]
    assert not bad, "\n".join(bad[:30])
    for n, pid in kids.items():
        y = int(n[3:])
        seen = {d["skill"] for d in DB.maths_lab_q.find({"pupil": {"$in": [pid, pid.lower()]}})}
        own = {k for k in seen if k.startswith("Y%d." % y)}
        assert len(own) >= 3, (n, seen)
        assert all(k.startswith(("Y%d." % y, "Y7.", "Y8.")) for k in seen), (n, seen)
    p95 = statistics.quantiles(lat, n=20)[18]
    print("requests %d, median %.0f ms, p95 %.0f ms" % (len(lat), 1000 * statistics.median(lat), 1000 * p95))
    assert p95 < 1.0, p95

    # one token, eight parallel answers: counted once
    s = sessions["Kid5"]
    q = s.post(BASE + "/api/maths/next", json={}).json()
    ans = str(DB.maths_lab_q.find_one({"_id": q["token"]})["answer"])
    before = DB.maths_attempts.count_documents({"pupil": {"$in": [kids["Kid5"], kids["Kid5"].lower()]}})
    with ThreadPoolExecutor(8) as ex:
        codes = list(ex.map(lambda _: s.post(BASE + "/api/maths/check", json={"token": q["token"], "value": ans}).status_code, range(8)))
    assert sorted(codes) == [200] + [409] * 7, codes
    after = DB.maths_attempts.count_documents({"pupil": {"$in": [kids["Kid5"], kids["Kid5"].lower()]}})
    assert after == before + 1
