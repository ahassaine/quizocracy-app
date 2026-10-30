"""End-to-end run inside the Android app: drives the app's own WebView over the DevTools protocol,
with real touch events sent through adb for the taps.

Needs: the debug APK running on an emulator, its WebView forwarded to 127.0.0.1:9333
(`adb forward tcp:9333 localabstract:webview_devtools_remote_<pid>`), and the server's database reachable.
Usage: QZ_BASE=https://quizocracy.com QZ_TEST_MONGO=... QZ_TEST_DB=qz QZ_TEST_INVITE=... python3 android_e2e.py
"""
import itertools
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

import websocket

sys.path.insert(0, os.path.dirname(__file__))
from conftest import BASE, DB, INVITE, PASSWORD, last_mail, new_email  # noqa: E402

SHOTS = os.getenv("QZ_SHOTS", "/tmp")
ADB = os.getenv("QZ_ADB", "ssh beast ~/Android/Sdk/platform-tools/adb")
CDP = os.getenv("QZ_CDP", "http://127.0.0.1:9333")


def adb(*args, out=None):
    cmd = f"{ADB} {' '.join(args)} < /dev/null"
    if out:
        with open(out, "wb") as f:
            subprocess.run(cmd, shell=True, stdout=f, check=True)
        return None
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True).stdout


class Page:
    def __init__(self):
        targets = json.load(urllib.request.urlopen(CDP + "/json"))
        t = next(t for t in targets if t["type"] == "page")
        self.ws = websocket.create_connection(t["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"), timeout=60, suppress_origin=True)
        self.ids = itertools.count(1)

    def cmd(self, method, **params):
        i = next(self.ids)
        self.ws.send(json.dumps({"id": i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == i:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m.get("result", {})

    def ev(self, js, arg=None):
        expr = f"({js})({json.dumps(arg)})" if arg is not None else f"({js})()"
        r = self.cmd("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if r.get("exceptionDetails"):
            raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

    def wait(self, js, arg=None, timeout=30):
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.ev(js, arg):
                    return
            except Exception:
                pass
            time.sleep(0.25)
        raise AssertionError(f"timed out waiting for: {js} {arg or ''}")

    def goto(self, path):
        self.cmd("Page.navigate", url=BASE + path)
        time.sleep(0.5)
        self.wait("() => document.readyState === 'complete'")

    def url(self):
        return self.ev("() => location.href")

    def fill(self, sel, value):
        self.ev("""([s, v]) => { const e = document.querySelector(s); e.focus(); e.value = v;
                   e.dispatchEvent(new Event('input', {bubbles: true})); return true; }""", [sel, str(value)])

    def click(self, sel):
        self.ev("s => { document.querySelector(s).click(); return true; }", sel)

    _origin = None

    def webview_origin(self):
        """Top-left of the WebView on the screen, read once from the UI hierarchy."""
        if Page._origin is None:
            adb("shell", "uiautomator", "dump", "/sdcard/qz_ui.xml")
            xml = adb("shell", "cat", "/sdcard/qz_ui.xml")
            m = re.search(r'class="android\.webkit\.WebView"[^>]*bounds="\[(\d+),(\d+)\]', xml)
            Page._origin = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        return Page._origin

    def tap(self, sel):
        """A real finger tap: adb input tap at the element's position on the screen."""
        x, y, dpr = self.ev("""s => { const e = document.querySelector(s); e.scrollIntoView({block: 'center'});
                              const r = e.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, devicePixelRatio]; }""", sel)
        ox, oy = self.webview_origin()
        adb("shell", "input", "tap", str(int(ox + x * dpr)), str(int(oy + y * dpr)))

    def text(self, sel):
        return self.ev("s => document.querySelector(s).innerText", sel)


def shot(name):
    adb("exec-out", "screencap", "-p", out=os.path.join(SHOTS, f"android_{name}.png"))


def step(msg):
    print("✓", msg, flush=True)


def wait_item(pg, activity, pid, prev=None):
    pg.wait("""prev => document.body.dataset.qtoken && document.body.dataset.qtoken !== prev
               && !document.getElementById('check').disabled""", prev or "")
    tok = pg.ev("() => document.body.dataset.qtoken")
    return (DB.maths_lab_q if activity == "maths" else DB.items).find_one({"_id": tok})


pg = Page()
pg.goto("/")
assert pg.ev("() => !!(window.Capacitor && window.Capacitor.isNativePlatform())"), "not inside the native app"
assert pg.ev("() => window.Capacitor.getPlatform()") == "android"
assert "Daily practice" in pg.text("main")
shot("1_landing")
step("the app opens quizocracy.com inside the Android shell, with the native bridge")

email = new_email("android")
pg.goto("/signup")
pg.fill("#email", email); pg.fill("#password", PASSWORD); pg.fill("#family_name", "Android test"); pg.fill("#invite", INVITE)
pg.ev("() => { document.getElementById('consent').checked = true; return true; }")
pg.tap("form button[type=submit]")
pg.wait("() => location.pathname === '/verify'")
code = re.search(r"\b(\d{6})\b", last_mail(email, "code")["subject"]).group(1)
pg.fill("#code", code); pg.tap("form[action='/verify'] button")
pg.wait("() => location.search.includes('welcome=1')")
step("sign up and email verification, with real taps")

pg.goto("/children/new")
pg.fill("#name", "Droid"); pg.ev("() => { document.getElementById('year').value = '4'; return true; }"); pg.fill("#pin", "2468")
for k, v in {"maths": 1, "tables": 2, "spelling": 1, "numbers": 1, "verbs": 1}.items():
    pg.fill(f"[data-testid=target-{k}]", v)
pg.click("form.card button[type=submit]")
pg.wait("() => /\\/children\\/p_[0-9a-f]+/.test(location.pathname)")
pid = re.search(r"/children/(p_[0-9a-f]+)", pg.url()).group(1)
step("add a child")

pg.goto("/learn")
pg.fill("[data-testid='pin-Droid'] input[name=pin]", "2468")
pg.tap("[data-testid='pin-Droid'] button")
pg.wait("() => location.pathname === '/me'")
shot("2_child_home")
step("the child enters with a PIN")

for act in ("tables", "tables", "spelling", "numbers", "verbs", "maths"):
    pg.goto(f"/me/{act}")
    d = wait_item(pg, act, pid)
    if act == "maths":
        shot("3_maths")
        pg.ev("v => { document.getElementById('mHost').__getValue = () => v; return true; }", d["answer"])
    elif act == "verbs":
        pg.fill("#past", d["answer"]["past"][0]); pg.fill("#pp", d["answer"]["pp"][0])
    else:
        if act == "spelling":
            src = pg.ev("() => document.getElementById('audio').getAttribute('src')")
            st = pg.ev("s => fetch(s).then(r => r.status + ' ' + r.headers.get('content-type'))", src)
            assert st == "200 audio/mpeg", st
        pg.fill("#answer", d["answer"])
    pg.tap("#check")
    pg.wait("() => document.querySelector('#feedback.yes, #feedback.no')")
    assert pg.ev("() => !!document.querySelector('#feedback.yes')"), (act, pg.text("#feedback"))
    step(f"{act}: answered correctly in the app")

pg.goto("/me")
assert pg.text("[data-testid=day-pct]") == "100%", pg.text("[data-testid=day-pct]")
shot("4_day_done")
step("the child's day reaches 100%")

pg.goto("/board")
adb("shell", "input", "keyevent", "KEYCODE_BACK")
pg.wait("() => location.pathname === '/me'")
step("the Android back button goes back a page instead of closing the app")

pg.goto("/parent-unlock")
pg.fill("#password", PASSWORD); pg.tap("form[action='/parent-unlock'] button[type=submit]")
pg.wait("() => location.pathname === '/home'")
assert pg.text("[data-testid='kid-Droid'] [data-testid=pct]") == "100%"
shot("5_parent_home")
step("the parent unlocks and sees 100%")

fid = DB.accounts.find_one({"email": email})["family_id"]
pg.goto("/settings")
pg.fill("#confirm", "DELETE"); pg.fill("#delpw", PASSWORD)
pg.click("form[action='/account/delete'] button")
pg.wait("() => location.search.includes('deleted=1')")
assert DB.families.count_documents({"_id": fid}) == 0 and DB.pupils.count_documents({"family_id": fid}) == 0
step("account deleted from inside the app; its data is gone")
print("ANDROID E2E PASSED")
