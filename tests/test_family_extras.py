"""Features families expect: the app installs (manifest, icons, a service worker that keeps only the static shell
and shows an offline page), a help page, a printable progress report, and a clear statement of the curriculum."""
import re

import requests

from conftest import BASE, DB, add_child, enter_child, signup, unlock_parent


def _session(page):
    s = requests.Session()
    for c in page.context.cookies():
        s.cookies.set(c["name"], c["value"])
    return s


def _answer(s, act, right=True):
    q = s.post(BASE + f"/api/{act}/next", json={}).json()
    ans = str(DB.items.find_one({"_id": q["token"]})["answer"])
    return s.post(BASE + f"/api/{act}/check", json={"token": q["token"], "value": ans if right else ans + "zz9"}).json()


def test_manifest_icons_and_service_worker_route():
    m = requests.get(BASE + "/static/manifest.webmanifest").json()
    assert m["name"] == "Quizocracy" and m["display"] == "standalone" and m["start_url"] == "/learn"
    assert m["theme_color"] == "#4F46E5" and m["background_color"] == "#F7F8FC"
    sizes = {(i["sizes"], i["purpose"]) for i in m["icons"]}
    assert {("192x192", "any"), ("512x512", "any"), ("512x512", "maskable")} <= sizes
    for i in m["icons"]:
        r = requests.get(BASE + i["src"])
        assert r.status_code == 200 and r.headers["content-type"] == "image/png"
    home = requests.get(BASE + "/").text
    assert 'rel="apple-touch-icon" href="/static/img/apple-touch-icon.png?v=' in home     # versioned: a new icon is a new URL
    assert requests.get(BASE + "/static/img/apple-touch-icon.png").status_code == 200
    sw = requests.get(BASE + "/sw.js")
    assert sw.status_code == 200 and "javascript" in sw.headers["content-type"]
    assert sw.headers.get("service-worker-allowed") == "/" and "no-cache" in sw.headers.get("cache-control", "")
    off = requests.get(BASE + "/static/offline.html").text
    assert "You're offline" in off and "needs the internet to check answers" in off


def test_service_worker_caches_only_the_shell_and_shows_offline_page(page):
    signup(page)
    pid = add_child(page, "Ola", 3)
    page.goto(f"/children/{pid}")
    assert page.evaluate("navigator.serviceWorker.ready.then(r => !!r.active)")
    page.goto(f"/children/{pid}")                        # now under the worker: pages and static files go through it
    assert page.evaluate("!!navigator.serviceWorker.controller")
    s = _session(page)
    enter_child(page, "Ola")
    page.goto("/me/tables")
    page.wait_for_function("document.body.dataset.qtoken")
    cached = page.evaluate("""async () => { const out = [];
        for (const k of await caches.keys()) for (const r of await (await caches.open(k)).keys()) out.push(r.url);
        return out; }""")
    paths = [re.sub(r"^https?://[^/]+", "", u) for u in cached]
    assert "/static/offline.html" in paths
    assert any(p.startswith("/static/css/app.css?v=") for p in paths), paths
    assert not [p for p in paths if p.startswith("/api/") or not p.startswith("/static/")], paths   # no pages, no answers
    assert s.get(BASE + "/home").status_code == 200
    page.context.set_offline(True)
    page.goto("/home")
    assert "You're offline" in page.inner_text("body")
    page.context.set_offline(False)


def test_help_page_answers_and_search(page):
    r = requests.get(BASE + "/help")
    assert r.status_code == 200
    for anchor in ("day-plan", "mastered", "comes-back", "first-time", "pins", "changes", "rewards", "handover",
                   "siblings", "read-aloud", "curriculum", "beta", "privacy", "contact", "report", "install"):
        assert f'id="{anchor}"' in r.text and f'href="#{anchor}"' in r.text, anchor
    assert "Follows the national curriculum in England (Years 1–9)" in r.text
    assert 'href="/privacy"' in r.text
    page.goto("/help")
    row = page.get_by_test_id("uk-years").locator("tr", has_text="Year 3").first
    assert "P4" in row.inner_text()
    page.fill("[data-testid=help-search]", "locked PIN")
    assert page.is_visible("#pins") and not page.is_visible("#rewards") and not page.is_visible("#helpToc")
    page.fill("[data-testid=help-search]", "zzqqxx")
    assert page.is_visible("[data-testid=help-none]")
    page.fill("[data-testid=help-search]", "")
    assert page.is_visible("#rewards") and page.is_visible("#helpToc")
    page.goto("/")
    assert page.get_by_role("link", name="Help").count() >= 1


def test_curriculum_line_on_landing_and_child_form(page):
    page.goto("/")
    assert "Follows the national curriculum in England (Years 1–9)" in page.inner_text("[data-testid=curriculum-line]")
    signup(page)
    page.goto("/children/new")
    hint = page.inner_text("[data-testid=year-hint]")
    assert "national curriculum in England" in hint and "P4 in Scotland is about Year 3" in hint
    page.goto("/settings")
    assert page.get_by_test_id("settings-help").get_attribute("href") == "/help"


def test_progress_report_for_one_child(page):
    signup(page)
    pid = add_child(page, "Rania", 3, targets={"tables": 3, "spelling": 2})
    other = add_child(page, "Yusuf", 5)
    enter_child(page, "Rania")
    s = _session(page)
    for _ in range(4):
        assert _answer(s, "tables")["correct"]
    assert not _answer(s, "tables", right=False)["correct"]
    assert _answer(s, "spelling")["correct"]
    unlock_parent(page)
    page.goto(f"/children/{pid}")
    page.click("[data-testid=report-link]")
    page.wait_for_url(f"**/children/{pid}/report")
    body = page.inner_text("[data-testid=report]")
    assert "Rania · progress report" in body and "Year 3" in body and "Last 30 days" in body
    assert page.inner_text("[data-testid=days-practised]") == "1"
    assert page.inner_text("[data-testid=answers]") == "6"
    # the 3 tables and 1 spelling of the plan, all right first time: the 2 tables after the target are extra
    assert page.inner_text("[data-testid=first-pct]") == "100%"
    assert "Times tables" in page.inner_text("[data-testid=report-acts]")
    assert "words from the Year 3 word list learned" in page.inner_text("[data-testid=report-spelling]")
    assert "still to put right" in page.inner_text("[data-testid=report-focus]")
    assert page.get_attribute("[data-testid=print]", "onclick") == "window.print()"
    for rng, label in (("7", "Last 7 days"), ("term", "This term so far")):
        page.goto(f"/children/{pid}/report?range={rng}")
        assert label in page.inner_text("h1 + p")
    page.emulate_media(media="print")
    assert not page.is_visible("header.top") and not page.is_visible("[data-testid=print]")
    page.emulate_media(media="screen")
    # another family's child, and a device in child mode, never see the report
    signup(page)
    assert page.goto(f"/children/{pid}/report").status == 404
    page.context.clear_cookies()
    page.goto(f"/children/{other}/report")
    assert "/login" in page.url


def test_report_needs_parent_mode(page):
    signup(page)
    pid = add_child(page, "Nour", 4)
    enter_child(page, "Nour")
    page.goto(f"/children/{pid}/report")
    assert "/parent-unlock" in page.url


def test_install_tip_on_iphone_can_be_dismissed(browser, devices):
    ctx = browser.new_context(base_url=BASE, **devices["iPhone 13"])
    pg = ctx.new_page()
    signup(pg)
    pg.goto("/home")
    assert pg.is_visible("[data-testid=install-tip]")
    assert "Share" in pg.inner_text("[data-testid=install-ios]") and "Add to Home Screen" in pg.inner_text("[data-testid=install-ios]")
    assert not pg.is_visible("[data-testid=install-btn]")
    pg.click("[data-testid=install-dismiss]")
    assert not pg.is_visible("[data-testid=install-tip]")
    pg.reload()
    assert not pg.is_visible("[data-testid=install-tip]")                  # stays dismissed on this device
    ctx.close()


def test_install_tip_hidden_without_install_support(page):
    signup(page)
    page.goto("/home")
    assert not page.is_visible("[data-testid=install-tip]")               # headless Chromium offers no install prompt
    page.evaluate("""() => { const e = new Event('beforeinstallprompt'); e.prompt = () => {};
                     e.userChoice = Promise.resolve({outcome: 'dismissed'}); dispatchEvent(e); }""")
    assert page.is_visible("[data-testid=install-btn]")


def test_carer_can_open_the_report(page):
    email = signup(page)
    pid = add_child(page, "Lina", 2)
    DB.accounts.update_one({"email": email}, {"$set": {"role": "carer"}})     # the same session, now a carer's
    r = page.goto(f"/children/{pid}/report")
    assert r.status == 200 and "Lina · progress report" in page.inner_text("h1")
