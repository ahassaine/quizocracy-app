"""The public side before families are invited: the invitation-only beta said plainly with a waiting list, "Start now"
after adding a child, real screens and link previews on the landing page, no request to any other site (fonts are
self-hosted), robots.txt, sitemap.xml and a friendly 404, and the curriculum line that names what is left out."""
import datetime
import re
import struct
from urllib.parse import urlparse

import requests

from conftest import BASE, DB, add_child, new_email, signup

LEFT_OUT = "Evolution, puberty and human reproduction are left out on purpose, so families can cover them their own way."
PUBLIC = ("/", "/signup", "/login", "/help", "/privacy", "/terms")


def _join(page, path, email):
    page.goto(path)
    page.fill("[data-testid=waitlist-email]", email)
    page.click("[data-testid=waitlist-join]")
    page.wait_for_url(re.compile(r".*waitlist=.*"))


# ---- invitation-only, with a waiting list ----
def test_landing_says_invitation_only_and_joins_the_waiting_list(page):
    page.goto("/")
    assert "The beta is invitation-only right now." in page.inner_text("[data-testid=invite-only]")
    assert page.get_attribute("[data-testid=have-code]", "href") == "/signup"
    page.click("[data-testid=to-waitlist]")
    assert page.is_visible("[data-testid=waitlist-email]")
    email = new_email("wl")
    _join(page, "/", email.upper())                       # stored as typed, in lower case
    assert urlparse(page.url).path == "/" and "waitlist=ok" in page.url
    assert "You're on the waiting list." in page.inner_text("[data-testid=waitlist-ok]")
    row = DB.waitlist.find_one({"_id": email})
    assert row and isinstance(row["created"], datetime.datetime) and row["page"] == "/"
    assert DB.outbox.count_documents({"to": email}) == 0     # nothing is sent: no marketing, no confirmation mail
    # the same address again: still one row, with the date it first joined
    _join(page, "/signup", email)
    assert "waitlist=ok" in page.url and urlparse(page.url).path == "/signup"
    assert DB.waitlist.count_documents({"_id": email}) == 1
    assert DB.waitlist.find_one({"_id": email})["created"] == row["created"]


def test_waiting_list_refuses_a_bad_email_ignores_robots_and_is_rate_limited(page):
    _join(page, "/", "someone@home")                  # the browser lets it through; we do not
    assert "doesn't look right" in page.inner_text("[data-testid=waitlist-bad]")
    # a robot fills the hidden field: it looks done, nothing is kept
    email = new_email("bot")
    r = requests.post(BASE + "/waitlist", data={"email": email, "back": "/", "website": "http://spam.example"},
                      allow_redirects=False)
    assert r.status_code == 303 and "waitlist=ok" in r.headers["location"]
    assert DB.waitlist.count_documents({"_id": email}) == 0
    # an unknown page to come back to goes home, never elsewhere
    r = requests.post(BASE + "/waitlist", data={"email": "x", "back": "https://evil.example/"}, allow_redirects=False)
    assert r.headers["location"].startswith("/?waitlist=")
    # per connection, at most 10 tries an hour
    key = "waitlist:ip:127.0.0.1"
    now = datetime.datetime.utcnow()
    ids = DB.login_failures.insert_many([{"email": key, "ts": now} for _ in range(10)]).inserted_ids
    try:
        email = new_email("busy")
        _join(page, "/", email)
        assert "Too many tries" in page.inner_text("[data-testid=waitlist-busy]")
        assert DB.waitlist.count_documents({"_id": email}) == 0
    finally:
        DB.login_failures.delete_many({"_id": {"$in": ids}})


def test_signup_page_says_invitation_only_and_a_wrong_code_points_to_the_list(page):
    page.goto("/signup")
    assert "invitation-only right now" in page.inner_text("[data-testid=invite-only]")
    assert page.is_visible("[data-testid=waitlist]")
    page.fill("#email", new_email())
    page.fill("#password", "correct-horse-9")
    page.fill("#invite", "WRONG")
    page.check("#consent")
    page.click("form[action='/signup'] button[type=submit]")
    err = page.inner_text("[role=alert]")
    assert "invitation code is not right" in err and "Join the waiting list below" in err
    assert page.is_visible("[data-testid=waitlist-email]")      # no dead end: the list is right there


def test_signing_up_takes_the_address_off_the_waiting_list(page):
    email = new_email("wl2")
    _join(page, "/", email)
    assert DB.waitlist.count_documents({"_id": email}) == 1
    signup(page, email)
    assert DB.waitlist.count_documents({"_id": email}) == 0


# ---- "Start now with <name>" ----
def test_start_now_opens_the_new_childs_day(page):
    signup(page)
    pid = add_child(page, "Nadia", 3)
    assert page.is_visible("[data-testid=start-now]")
    assert page.inner_text("[data-testid=start-now]") == "Start now with Nadia"
    assert page.locator("[data-testid=added] form[action='/handover']").count() == 1     # hand-over stays
    page.click("[data-testid=start-now]")
    page.wait_for_url("**/me")
    assert page.inner_text("[data-testid=child-name]") == "Nadia"
    page.goto("/me/maths")
    page.wait_for_function("document.body.dataset.qtoken")                 # straight into a question
    page.goto("/home")
    page.wait_for_url("**/parent-unlock")                                   # the parent area is locked again
    # without a signed-in grown-up, nothing opens
    other = requests.post(BASE + f"/children/{pid}/start", allow_redirects=False)
    assert other.status_code == 303 and other.headers["location"] == "/login"


# ---- link previews, screenshots and no outside requests ----
def test_public_pages_have_link_preview_tags():
    for path in PUBLIC:
        html = requests.get(BASE + path).text
        for tag in ('name="description"', 'property="og:title"', 'property="og:description"', 'property="og:image"',
                    'name="twitter:card" content="summary_large_image"', 'name="twitter:image"'):
            assert tag in html, (path, tag)
    html = requests.get(BASE + "/").text
    img = re.search(r'property="og:image" content="([^"]+)"', html).group(1)
    assert img.endswith("/static/img/og-preview.png")
    r = requests.get(BASE + "/static/img/og-preview.png")
    assert r.status_code == 200 and r.content[:8] == b"\x89PNG\r\n\x1a\n" and len(r.content) < 400_000
    assert struct.unpack(">II", r.content[16:24]) == (1200, 630)


def test_landing_shows_real_screens_with_alt_text(page):
    page.goto("/")
    imgs = page.locator("[data-testid=landing-shots] img")
    assert imgs.count() == 2
    for i in range(2):
        img = imgs.nth(i)
        img.scroll_into_view_if_needed()
        assert len(img.get_attribute("alt")) > 40
        assert img.get_attribute("src").endswith(".webp")
        page.wait_for_function("el => el.complete && el.naturalWidth > 0", arg=img.element_handle())
        assert len(requests.get(BASE + img.get_attribute("src")).content) < 150_000


def test_no_page_requests_another_site(page):
    seen = []
    page.on("request", lambda r: seen.append(r.url))
    for path in PUBLIC:
        page.goto(path)
        page.wait_for_load_state("networkidle")
    signup(page)
    add_child(page, "Iris", 4)
    page.wait_for_load_state("networkidle")
    outside = {u for u in seen if urlparse(u).netloc not in (urlparse(BASE).netloc, "")}
    assert not outside, outside
    css = requests.get(BASE + "/static/fonts/fonts.css?v=1")
    assert css.status_code == 200 and "Plus Jakarta Sans" in css.text and "Inter" in css.text
    for f in re.findall(r"url\((/static/fonts/[^)]+\.woff2)\)", css.text):
        assert requests.get(BASE + f).status_code == 200, f
    assert "googleapis" not in requests.get(BASE + "/").text


# ---- robots.txt, sitemap.xml and the 404 page ----
def test_robots_and_sitemap():
    r = requests.get(BASE + "/robots.txt")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/plain")
    for p in ("/team/", "/api/", "/home", "/me", "/children/", "/settings", "/learn"):
        assert f"Disallow: {p}\n" in r.text, p
    assert "Allow: /help" in r.text and "Sitemap: " in r.text and "/sitemap.xml" in r.text
    s = requests.get(BASE + "/sitemap.xml")
    assert s.status_code == 200 and "xml" in s.headers["content-type"]
    locs = [urlparse(u).path for u in re.findall(r"<loc>([^<]+)</loc>", s.text)]
    assert locs == list(PUBLIC)


def test_unknown_pages_get_a_friendly_404_and_the_api_keeps_json(page):
    resp = page.goto("/no-such-page")
    assert resp.status == 404
    assert "We can't find that page" in page.inner_text("[data-testid=not-found]")
    assert page.get_attribute("[data-testid=not-found] a[href='/help']", "href") == "/help"
    assert page.locator("[data-testid=not-found] a[href='/']").count() == 1
    r = requests.get(BASE + "/api/no-such-thing")
    assert r.status_code == 404 and r.headers["content-type"].startswith("application/json")
    # signed in, the way back is Home
    signup(page)
    assert page.goto("/nothing/here").status == 404
    assert page.locator("[data-testid=not-found] a[href='/home']").count() == 1


# ---- the curriculum claim says what is left out ----
def test_curriculum_claim_names_what_is_left_out(page):
    for path in ("/", "/help", "/terms"):
        assert LEFT_OUT in requests.get(BASE + path).text, path
    page.goto("/")
    assert LEFT_OUT in page.inner_text("[data-testid=curriculum-line]")
    signup(page)
    page.goto("/children/new")
    assert LEFT_OUT in page.inner_text("[data-testid=year-hint]")
    priv = requests.get(BASE + "/privacy").text
    assert "The waiting list:" in priv and "even the fonts come from our own server" in priv
