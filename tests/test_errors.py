"""Unhandled server errors (app/errors.py): the user sees the friendly page, the operator gets one email per
distinct error per hour (at most 20 a day) with no secrets in it, and /healthz reports a database that is down.
In-process (no server needed): the alert is captured by replacing mailer.alert."""
import asyncio
import concurrent.futures
import datetime

import pytest
from fastapi.testclient import TestClient

from app import config, errors, mailer
from app.main import app

SENT = []


async def _boom():
    raise ValueError("the sky fell")


async def _boom2():
    raise KeyError("missing")


for path, fn in (("/_test/boom", _boom), ("/api/_test/boom", _boom), ("/_test/boom2", _boom2)):
    if path not in {getattr(r, "path", "") for r in app.routes}:
        app.add_api_route(path, fn)


@pytest.fixture()
def client(monkeypatch):
    async def fake_alert(subject, body):
        SENT.append((subject, body))
        return True

    async def no_session(*a, **k):
        return None

    SENT.clear()
    monkeypatch.setattr(mailer, "alert", fake_alert)
    monkeypatch.setattr(config, "ALERT_EMAIL", "ops@example.test")
    monkeypatch.setattr(errors, "db", type("DB", (), {"sessions": type("C", (), {"find_one": staticmethod(no_session)})}))
    errors._last.clear()
    errors._day.update(date=errors._today(), errors=0, emailed=0, kinds=set())
    return TestClient(app, raise_server_exceptions=False)


def test_a_500_shows_the_friendly_page_and_emails_once_an_hour(client):
    r = client.get("/_test/boom?token=s3cr3t-value", cookies={"qz_s": "cookie-value-123456"})
    assert r.status_code == 500 and "Oops, something went wrong" in r.text and "Try again" in r.text
    assert r.headers["cache-control"] == "no-store"
    assert len(SENT) == 1
    subject, body = SENT[0]
    assert "ValueError" in subject and "GET /_test/boom" in subject
    for want in ("Time:", "Request:   GET /_test/boom", "ValueError: the sky fell", "Last 8 frames", "_boom",
                 "Who:       no live session", "Today so far: 1 errors"):
        assert want in body, want
    assert "s3cr3t-value" not in body and "cookie-value-123456" not in body       # no query string, no cookie
    ref = body.split("Reference: ")[1][:6]
    assert ref in r.text                                                         # the page shows the same reference
    for _ in range(3):
        assert client.get("/_test/boom").status_code == 500
    assert len(SENT) == 1                                                        # the same error: once an hour
    client.get("/_test/boom2")
    assert len(SENT) == 2 and "KeyError" in SENT[1][0]                           # a different error is emailed
    assert errors._day["errors"] == 5 and len(errors._day["kinds"]) == 2
    errors._last[next(iter(errors._last))] -= datetime.timedelta(hours=2)        # an hour later it is emailed again
    client.get("/_test/boom")
    client.get("/_test/boom2")
    assert len(SENT) == 3


def test_api_errors_are_json_and_the_day_is_capped(client):
    r = client.get("/api/_test/boom")
    assert r.status_code == 500 and r.json()["ok"] is False and r.json()["error"] == "server"
    errors._day["emailed"] = errors.MAX_PER_DAY
    errors._last.clear()
    client.get("/_test/boom2")
    assert len(SENT) == 1                                                        # 20 a day at most


def test_no_alert_email_when_unset(client, monkeypatch):
    monkeypatch.setattr(config, "ALERT_EMAIL", "")
    assert client.get("/_test/boom").status_code == 500
    assert SENT == [] and errors._day["errors"] == 1                             # still counted (and logged)


def test_the_day_before_is_counted_once():
    errors._day.update(date=errors._today() - datetime.timedelta(days=1), errors=7, emailed=3, kinds={"a", "b"})
    done = errors._roll()
    subject, body = errors._summary(done)
    assert "7 server errors" in subject and "7 (2 different), 3 emailed, 4 not emailed" in body
    assert errors._roll() is None and errors._day["errors"] == 0


def _run(coro):
    """asyncio.run in a thread of its own: the Playwright tests leave an event loop running in this one."""
    with concurrent.futures.ThreadPoolExecutor(1) as ex:
        return ex.submit(asyncio.run, coro).result()


def test_alert_helper_does_not_need_the_database(monkeypatch):
    """The error being reported may be the database: a failed outbox write still lets the alert through."""
    async def down(*a, **k):
        raise RuntimeError("db down")
    monkeypatch.setattr(config, "ALERT_EMAIL", "ops@example.test")
    monkeypatch.setattr(mailer, "db", type("DB", (), {"outbox": type("C", (), {"insert_one": staticmethod(down)})}))
    assert _run(mailer.alert("s", "b")) is True
    monkeypatch.setattr(config, "ALERT_EMAIL", "")
    assert _run(mailer.alert("s", "b")) is False


def test_healthz_is_503_when_the_database_is_down(monkeypatch):
    async def down(*a, **k):
        raise RuntimeError("no server")
    import app.main as main
    monkeypatch.setattr(main.db, "command", down, raising=False)
    r = TestClient(app, raise_server_exceptions=False).get("/healthz")
    assert r.status_code == 503 and r.json() == {"ok": False, "db": "down"}
