"""End-to-end tests: a real browser against a running server, reading emails and answers from its database.

QZ_BASE   server URL           (default http://127.0.0.1:8311)
QZ_TEST_MONGO / QZ_TEST_DB     the server's database (for the outbox and served answers)
QZ_TEST_INVITE                 the server's invitation code
"""
import os
import re
import uuid

import pytest
from playwright.sync_api import sync_playwright
from pymongo import MongoClient

BASE = os.getenv("QZ_BASE", "http://127.0.0.1:8311").rstrip("/")
DB = MongoClient(os.getenv("QZ_TEST_MONGO", "mongodb://127.0.0.1:27027"))[os.getenv("QZ_TEST_DB", "qz_test")]
INVITE = os.getenv("QZ_TEST_INVITE", "BETA2026")
PASSWORD = "correct-horse-9"


_PW = {}


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        _PW["devices"] = p.devices
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture()
def devices(browser):
    return _PW["devices"]


@pytest.fixture()
def page(browser):
    ctx = browser.new_context(base_url=BASE)
    pg = ctx.new_page()
    pg.set_default_timeout(15000)
    yield pg
    ctx.close()


def new_email(tag="p"):
    return f"{tag}-{uuid.uuid4().hex[:10]}@example.test"


def last_mail(to, subject_contains=""):
    m = DB.outbox.find_one({"to": to, "subject": {"$regex": re.escape(subject_contains)}}, sort=[("created", -1)])
    assert m, f"no email to {to}"
    return m


def signup(page, email=None, family="Test family"):
    email = email or new_email()
    page.goto("/signup")
    page.fill("#email", email)
    page.fill("#password", PASSWORD)
    page.fill("#family_name", family)
    if page.locator("#invite").count():
        page.fill("#invite", INVITE)
    page.check("#consent")
    page.click("button[type=submit]")
    page.wait_for_url("**/verify")
    code = re.search(r"\b(\d{6})\b", last_mail(email, "code")["subject"]).group(1)
    page.fill("#code", code)
    page.click("form[action='/verify'] button")
    page.wait_for_url("**/home?welcome=1")
    return email


def add_child(page, name="Sami", year=4, pin="1234", targets=None):
    page.goto("/children/new")
    page.fill("#name", name)
    page.select_option("#year", str(year))
    page.fill("#pin", pin)
    for k, v in (targets or {}).items():
        page.fill(f"[data-testid=target-{k}]", str(v))
    page.click("form.card button[type=submit]")
    page.wait_for_url(re.compile(r".*/children/p_[0-9a-f]+\?added=1"))
    return page.url.split("/children/")[1].split("?")[0]


def enter_child(page, name, pin="1234"):
    page.goto("/learn")
    form = page.locator(f"[data-testid='pin-{name}']")
    form.locator("input[name=pin]").fill(pin)
    form.locator("button").click()
    page.wait_for_url("**/me")


def unlock_parent(page):
    page.goto("/parent-unlock")
    page.fill("#password", PASSWORD)
    page.click("form[action='/parent-unlock'] button[type=submit]")
    page.wait_for_url("**/home")


def pending_item(pupil_id, activity):
    it = DB.items.find_one({"pupil_id": pupil_id, "activity": activity, "done": False}, sort=[("created", -1)])
    assert it, f"no pending {activity} item"
    return it


def wait_question(page, activity, pupil_id, previous=None):
    """Wait until the page shows a new question, and return its stored item."""
    for _ in range(100):
        if activity == "maths":
            doc = DB.maths_lab_q.find_one({"pupil": pupil_id, "done": {"$ne": True}}, sort=[("created", -1)])
        else:
            doc = DB.items.find_one({"pupil_id": pupil_id, "activity": activity, "done": False}, sort=[("created", -1)])
        if doc and doc["_id"] != previous:
            page.wait_for_function("() => document.getElementById('check') && !document.getElementById('check').disabled")
            return doc
        page.wait_for_timeout(100)
    raise AssertionError("no new question appeared")
