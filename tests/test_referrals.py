"""Founding families and family-to-family invitations (app/referrals.py): the link on Home, signing up with it,
and the counts the inviting family sees."""
import datetime
import re

import pytest

from conftest import BASE, DB, PASSWORD, add_child, last_mail, new_email, signup
from test_funnel_feedback import _answer_on, _back, _fam, _member

pytestmark = pytest.mark.skipif(BASE.startswith("https://"), reason="writes dates straight into the database")


def _signup_with_link(page, link, family):
    email = new_email()
    page.goto(link)
    page.wait_for_url("**/signup?ref=*")
    assert page.locator("[data-testid=invited-by-family]").is_visible()
    page.fill("#email", email); page.fill("#password", PASSWORD); page.fill("#family_name", family)
    page.check("#consent")
    page.click("button[type=submit]")
    page.wait_for_url("**/verify")
    code = re.search(r"\b(\d{6})\b", last_mail(email, "code")["subject"]).group(1)
    page.fill("#code", code); page.click("form[action='/verify'] button")
    page.wait_for_url("**/home?welcome=1")
    return email


def test_invite_a_family(browser, page):
    a = signup(page, family="Inviting family")
    fa = _fam(a)
    page.goto("/home")
    assert page.locator("[data-testid=founding]").is_visible()
    link = page.locator("[data-testid=invite-link]").inner_text().strip()
    code = DB.families.find_one({"_id": fa})["ref"]
    assert link.endswith(f"/join/{code}") and len(code) == 6
    assert "No family has joined" in page.locator("[data-testid=invite-count]").inner_text()

    # another family joins with the link: no beta code needed, and it is remembered
    other = browser.new_context(base_url=BASE).new_page()
    assert other.goto("/join/ZZZZ99").url.endswith("/signup")              # an unknown code: plain sign-up
    path = link.split("quizocracy.com")[-1] if "quizocracy.com" in link else link[link.index("/join/"):]
    b = _signup_with_link(other, path, "Joining family")
    fb = DB.families.find_one({"_id": _fam(b)})
    assert fb["referred_by"] == fa and fb["founding"] is True
    page.goto("/home")
    t = page.locator("[data-testid=invite-count]").inner_text()
    assert "1 family has joined" in t and "0 kept going" in t and "extra free month" not in t

    # it counts once a child of the new family practises in its second week
    pid = add_child(other, "Rumi", 3)
    d1 = _back(fb["_id"], 10)
    _answer_on(fb["_id"], pid, d1 + datetime.timedelta(days=8))              # day 9: week 2
    page.goto("/home")
    t = page.locator("[data-testid=invite-count]").inner_text()
    assert "1 kept going" in t and "1 extra free month" in t
    # the inviting family never sees who joined
    assert "Joining family" not in page.content() and b not in page.content()
    other.goto("/home")
    assert "1 extra free month" in other.locator("[data-testid=invite-count]").inner_text()   # both families
    # the team sees who invited whom
    ali = _member()
    page.goto(f"/team/{ali}/funnel?tests=1&q={b}")
    assert "invited by Inviting family" in page.locator("[data-testid=via]").inner_text()
    page.goto(f"/team/{ali}/funnel?tests=1")
    cells = [[c.strip() for c in r.locator("td").all_inner_texts()]
             for r in page.locator("[data-testid=inviters] tr").filter(has_text="Inviting family").all()]
    assert ["Inviting family", "1", "1", "1"] in cells
    other.context.close()


def test_wrong_code_still_refused(page):
    page.goto("/signup")
    if not page.locator("#invite").count():
        pytest.skip("sign-up is open: no code to check")
    page.fill("#email", new_email()); page.fill("#password", PASSWORD); page.fill("#invite", "NOPE42")
    page.check("#consent"); page.click("button[type=submit]")
    assert "invitation code is not right" in page.locator(".err").inner_text()
