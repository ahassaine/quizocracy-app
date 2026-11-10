"""Changing a child's year moves the progress cards to the new year's bank, and hides activities the
new year does not have."""
from conftest import add_child, signup


def test_progress_follows_new_year(page):
    signup(page)
    pid = add_child(page, "Lina", 6)
    page.goto("/children/%s" % pid)
    txt = page.inner_text("main")
    assert "Year 6 skills mastered" in txt and "/132" in txt and "Irregular verbs" in txt, txt

    page.goto("/children/%s/edit" % pid)
    page.select_option("#year", "2")
    page.click("form.card button[type=submit]")
    page.wait_for_url("**/children/%s/edit?saved=1" % pid)
    page.goto("/children/%s" % pid)
    txt = page.inner_text("main")
    assert "Year 2 skills mastered" in txt and "/36" in txt, txt
    assert "Irregular verbs" not in txt, txt
