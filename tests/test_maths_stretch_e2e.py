"""In the browser: a missed column calculation shows its written method in a fixed-width block, and a question from
an earlier year's skill carries a small "Warm-up" tag (no year number) on the child's card."""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conftest import DB, add_child, enter_child, signup, wait_question  # noqa: E402


def _focus(pid, strand):
    today = datetime.date.today()
    DB.pupils.update_one({"_id": pid}, {"$set": {"focus": [{
        "subject": "maths", "strand": strand, "weeks": 1, "from": (today - datetime.timedelta(days=1)).isoformat(),
        "until": (today + datetime.timedelta(days=7)).isoformat()}]}})


def _answer_wrong(page):
    box = page.locator("#mHost input").first
    box.fill("1")
    page.click("#check")


def test_missed_column_sum_shows_the_layout(page):
    signup(page)
    pid = add_child(page, "Aanya", year=6)
    _focus(pid, "6.1 The four operations")
    enter_child(page, "Aanya")
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto("/me/maths")
    prev, shown = None, False
    for _ in range(40):
        doc = wait_question(page, "maths", pid, prev)
        prev = doc["_id"]
        if doc.get("layout") and page.locator("#mHost input").count() == 1:
            _answer_wrong(page)
            page.wait_for_selector("pre.m-col")
            grid = page.locator("pre.m-col").inner_text()
            assert grid.strip() and grid.replace(" ", "").replace("\n", "")
            page.screenshot(path=os.environ.get("QZ_SHOTS", "/tmp") + "/stretch_layout_390.png", full_page=True)
            shown = True
            break
        page.evaluate("document.body.dataset.qtoken = ''")
        DB.maths_lab_q.update_one({"_id": doc["_id"]}, {"$set": {"done": True}})
        page.goto("/me/maths")
    assert shown, "no column calculation came up in 40 questions"


def test_earlier_year_question_is_tagged_review(page):
    signup(page)
    pid = add_child(page, "Ethan", year=9)
    enter_child(page, "Ethan")
    # Years 8 and 9 mix in earlier KS3 skills (maths_mastery.KS3_MIX_CHANCE): one comes up within a few questions
    page.goto("/me/maths")
    prev, tagged = None, None
    for _ in range(60):
        doc = wait_question(page, "maths", pid, prev)
        prev = doc["_id"]
        tag = page.locator("#reviewTag")
        if doc["skill"].startswith(("Y7.", "Y8.")):
            assert tag.is_visible() and tag.inner_text() == "Warm-up", doc["skill"]
            tagged = doc["skill"]
            page.screenshot(path=os.environ.get("QZ_SHOTS", "/tmp") + "/stretch_review_390.png")
            break
        assert not tag.is_visible(), doc["skill"]
        DB.maths_lab_q.update_one({"_id": doc["_id"]}, {"$set": {"done": True}})
        page.goto("/me/maths")
    assert tagged, "no earlier-year question in 60"
