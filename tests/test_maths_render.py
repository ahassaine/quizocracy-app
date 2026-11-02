"""Render one real question from every maths skill (each tier) with the live components: no errors, an input."""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.maths import maths_engine as e  # noqa: E402
from conftest import BASE  # noqa: E402


def _samples():
    random.seed(5)
    out = []
    for s in e.SKILLS:
        for d in (0, 1, 2):
            q = e.call_generator(e.GENERATORS[s["key"]], d)
            comp = q.get("component", "number")
            spec = e.hide_missing_cell(comp, q.get("spec") or {})
            if comp == "angle" and q.get("answer_type", "num") in ("int", "num"):
                spec = {**spec, "numeric": True}
            out.append({"k": "%s d%d" % (s["key"], d), "c": comp, "spec": spec})
    return out


def test_every_skill_renders(page):
    samples = _samples()
    comps = sorted({x["c"] for x in samples})
    errors = []
    page.on("pageerror", lambda ex: errors.append(str(ex)))
    page.goto(BASE + "/privacy")                   # same origin as the components
    for c in comps:
        page.add_script_tag(url="/static/maths/components/%s.js" % c)
    bad = page.evaluate("""S => {
        const bad = [];
        for (const s of S) {
            const h = document.createElement('div');
            document.body.appendChild(h);
            try {
                if (!window.MComp[s.c]) { bad.push(s.k + ' no component ' + s.c); continue; }
                window.MComp[s.c].render(h, s.spec, {submit() {}});
                if (!h.children.length) bad.push(s.k + ' rendered nothing');
                if (/\\bundefined\\b|NaN/.test(h.textContent)) bad.push(s.k + ' shows undefined/NaN');
            } catch (err) { bad.push(s.k + ' ' + err); }
            h.remove();
        }
        return bad;
    }""", samples)
    assert not bad and not errors, "\n".join((bad + errors)[:40])
