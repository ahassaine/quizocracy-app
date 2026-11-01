import datetime
import os
import subprocess
import sys

from conftest import BASE, DB

ROOT = os.path.dirname(os.path.dirname(__file__))
ALPH = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _member(name, role):
    import secrets
    slug = "".join(secrets.choice(ALPH) for _ in range(10))
    DB.team_members.insert_one({"_id": slug, "name": name, "initials": name[:2], "role": role,
                                "telegram_chat_id": None, "active": True, "created": datetime.datetime.utcnow()})
    return slug


def _watch(since):
    env = dict(os.environ, QZ_MONGO_URL=os.getenv("QZ_TEST_MONGO", "mongodb://127.0.0.1:27027"),
               QZ_DB=DB.name, QZ_PUBLIC_URL=BASE, QZTEAM_SINCE=since)
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "team_watch.py")], env=env,
                         capture_output=True, text=True, check=True).stdout
    return out


import pytest


@pytest.mark.skipif(BASE.startswith("https://"), reason="never touches the real team board")
def test_team_board_end_to_end(page, tmp_path):
    DB.team_members.delete_many({}); DB.team_threads.delete_many({}); DB.team_messages.delete_many({})
    ali, meriem, bot = _member("Ali", "admin"), _member("Meriem", "member"), _member("Claude", "bot")
    since = (datetime.datetime.utcnow() - datetime.timedelta(seconds=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    assert page.goto("/team/notAmember1").status == 404
    r = page.goto(f"/team/{meriem}")
    assert r.status == 200 and r.headers.get("x-robots-tag") == "noindex, nofollow"
    # Meriem opens a thread with an image
    img = tmp_path / "shot.png"
    subprocess.run(["convert", "-size", "40x40", "xc:red", str(img)], check=True)
    page.goto(f"/team/{meriem}/new")
    page.fill("#title", "Spelling page feedback")
    page.fill("#text", "The listen button is too small on my phone")
    page.set_input_files("#files", str(img))
    page.click("button[type=submit]")
    page.wait_for_url(f"**/team/{meriem}/*")
    tid = page.url.rsplit("/", 1)[1]
    assert "too small" in page.inner_text("main")
    img_src = page.locator("main img").get_attribute("src")
    assert page.request.get(BASE + img_src).status == 200
    # Ali sees it in the list and replies; attribution follows the link
    page.goto(f"/team/{ali}")
    assert "Spelling page feedback" in page.inner_text("[data-testid=thread]")
    page.goto(f"/team/{ali}/{tid}")
    page.fill("textarea[name=text]", "Agreed — Claude, can you make it bigger? See https://quizocracy.com/learn. <marquee>x</marquee>")
    page.click("form[action$='/send'] button")
    page.wait_for_url(f"**/team/{ali}/{tid}*")
    msgs = page.locator("[data-testid=msg]").all_inner_texts()
    assert msgs[0].startswith("Meriem") and msgs[1].startswith("Ali")
    # links in messages are clickable; any other markup stays text
    link = page.locator("[data-testid=msg] a[href='https://quizocracy.com/learn']")
    assert link.count() == 1 and link.get_attribute("target") == "_blank"
    assert "<marquee>x</marquee>" in msgs[1] and page.locator("[data-testid=msg] marquee").count() == 0
    # the bot replies through its own link; that must not wake anyone
    page.goto(f"/team/{bot}/{tid}")
    page.fill("textarea[name=text]", "On it.")
    page.click("form[action$='/send'] button")
    out = _watch(since)
    wakes = [line for line in out.splitlines() if line.startswith("QZTEAM ")]
    assert len(wakes) == 2 and "Meriem" in wakes[0] and "Ali" in wakes[1], out
    assert f"/team/{bot}/{tid}" in wakes[0] and "[+1 attachment(s)]" in wakes[0]
    assert out.strip().splitlines()[-1].startswith("MARKER ")
    marker = out.strip().splitlines()[-1].split(" ", 1)[1]
    assert not [l for l in _watch(marker).splitlines() if l.startswith("QZTEAM ")]   # nothing new after the marker
    # status: members resolve, only admin/bot set awaiting retest, a reply reopens
    page.goto(f"/team/{meriem}/{tid}")
    assert page.locator("button[value=awaiting_retest]").count() == 0
    st = page.evaluate("u => fetch(u, {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:'status=awaiting_retest'}).then(r => r.status)",
                       f"/team/{meriem}/{tid}/status")
    assert st == 403
    page.click("button[value=resolved]")
    page.wait_for_url(f"**/team/{meriem}/{tid}")
    assert page.inner_text("[data-testid=status]") == "resolved"
    page.fill("textarea[name=text]", "One more thing")
    page.click("form[action$='/send'] button")
    page.wait_for_url(f"**/team/{meriem}/{tid}*")
    assert page.inner_text("[data-testid=status]") == "open"
    # empty messages are not stored; files of another thread are not reachable
    n = DB.team_messages.count_documents({"tid": tid})
    page.click("form[action$='/send'] button")
    assert "empty" in page.inner_text("main") and DB.team_messages.count_documents({"tid": tid}) == n
    assert page.request.get(BASE + img_src.replace(tid, "zzzzzz")).status == 404
