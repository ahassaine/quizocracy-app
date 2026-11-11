"""The parent's side: children, their plans, progress, rewards, the account and its data."""
import datetime
import json
import re
from urllib.parse import quote

from bson import ObjectId
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, Response

from ..activities import (ACTIVITIES, ALL_WEEK, CAP_YEARS, CHECK_SECONDS, FOCUS_MAX, FOCUS_WEEKS, MAX_DAYS_OFF, ORDER, PLANS, SCIENCE_AREA,
                          SCIENCE_AREAS, SECONDS, WEEKDAYS, YEARS, day_label, days_text, default_activities,
                          focus_items, focus_title, minutes, plan_of, practice_days_on, rest_day, strand_label,
                          todays_plan, year_pace)
from ..bank import engine as bank_engine
from ..maths import maths_mastery
from ..db import FAMILY_COLLECTIONS, db
from ..deps import (Ctx, adult_name, clear_pin_lock, family_adult, family_events, family_page, full_page,
                    hit, local_time, log_event, over_limit, own_pupil, parent_page, pin_lock_until, pin_locks)
from ..drills import bank, maths, spelling, tables, verbs
from .. import config, funnel, levels, mailer, progress
from ..tips import TIPS
from ..security import hash_secret, new_id, verify_secret
from ..web import page, templates
from .auth import settings_view
from .child import REPORT_REASONS, _due, pick_batch, picker_page
from .team import FAMILY_SHOTS, drop_family_feedback, post_family_feedback

router = APIRouter()
PIN_RE = re.compile(r"^\d{4}$")
# What the child form's script needs to tick a year's defaults and estimate the minutes as the parent edits.
templates.env.globals["PLAN_JS"] = {"defaults": {y: default_activities(y) for y in YEARS}, "seconds": SECONDS,
                                    "pace": {y: year_pace(y) for y in YEARS}, "check_secs": CHECK_SECONDS,
                                    "cap_years": CAP_YEARS,
                                    "min_year": {k: a["min_year"] for k, a in ACTIVITIES.items()}}
templates.env.filters["daylabel"] = day_label          # "2026-11-24" -> "24 Nov"


async def _pin_taken(ctx: Ctx, pin: str, but: str | None = None) -> str | None:
    """The name of another child of this family whose PIN this is already (twins on one tablet would get into
    each other's practice), or None."""
    async for o in db.pupils.find({"family_id": ctx.family["_id"], "_id": {"$ne": but}}, {"name": 1, "pin": 1}):
        if o.get("pin") and verify_secret(pin, o["pin"]):
            return o["name"]
    return None


def _day_name(day: str) -> str:
    """When a day is, after "back to practice": "tomorrow", or "on Monday 16 Nov"."""
    d = datetime.date.fromisoformat(day)
    if d == datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=1):
        return "tomorrow"
    return f"on {d:%A} {d.day} {d:%b}"


templates.env.filters["dayname"] = _day_name


async def _pupils(ctx: Ctx) -> list:
    return [await levels.fix(p) async for p in db.pupils.find({"family_id": ctx.family["_id"]}).sort("created", 1)]


@router.get("/home")
async def home(request: Request, ctx: Ctx = Depends(parent_page)):
    pupils = await _pupils(ctx)
    board = await progress.board(ctx.family, pupils)
    hist = {p["_id"]: await progress.history(p, ctx.family, 7) for p in pupils}
    full = len(pupils) >= plan_of(ctx.family)["max_children"] and _full_reason(ctx.family) == "limit"
    return page(request, "home.html", ctx, board=board, hist=hist, plan=plan_of(ctx.family), full=full,
                accuracy={pid: accuracy(h) for pid, h in hist.items()},
                day_stats=await progress.day_stats([p["_id"] for p in pupils], [progress.today()],
                                                   progress.plan_targets(pupils, ctx.family, [progress.today()])),
                today_day=progress.today(),
                welcome=request.query_params.get("welcome"), locks=await pin_locks(pupils),
                unlocked=request.query_params.get("unlocked"), events=await family_events(ctx.family["_id"], 12),
                deleted_name=request.query_params.get("deleted_name", "")[:30],
                pending={p["_id"]: _pending(p, ctx.family) for p in pupils},
                checks={p["_id"]: _check_today(p) for p in pupils}, reward_gap=reward_gap(ctx.family, pupils),
                feedback_card=await funnel.card_for(ctx.account, ctx.family))


@router.post("/home/feedback")
async def feedback_card(request: Request, ctx: Ctx = Depends(parent_page), card: str = Form(""),
                        action: str = Form(""), mood: str = Form(""), text: str = Form("")):
    """The "How is it going?" card on Home (app/funnel.py): Send keeps the answer and posts it to the team board's
    "Family feedback" thread; "No thanks" closes it. Either way that card never shows again. Never in child mode."""
    d = await db.feedback.find_one({"_id": f"{ctx.account['_id']}:{card}"})
    if not d or d.get("status") != "shown":
        return RedirectResponse("/home", 303)
    now = datetime.datetime.utcnow()
    if action == "dismiss":
        await db.feedback.update_one({"_id": d["_id"]}, {"$set": {"status": "dismissed", "at": now}})
        return RedirectResponse("/home", 303)
    mood = mood if mood in funnel.MOODS else ""
    text = (text or "").strip()[:1000]
    if not (mood or text):
        return RedirectResponse("/home?fb=empty#feedback-card", 303)
    await db.feedback.update_one({"_id": d["_id"]}, {"$set": {"status": "sent", "mood": mood, "text": text, "at": now}})
    kids = await db.pupils.count_documents({"family_id": ctx.family["_id"]})
    days = len(await funnel.active_days(ctx.family))
    d1 = funnel.local_day(ctx.family["created"])
    mid = await post_family_feedback(
        f"{funnel.MOODS.get(mood, 'No face picked')} · {funnel.CARDS[card]} card\n"
        + (f"“{text}”\n" if text else "")
        + f"{ctx.family['name']} ({ctx.role}) · signed up {d1.day} {d1:%b} · "
        f"{kids} {'child' if kids == 1 else 'children'} · {days} active {'day' if days == 1 else 'days'}")
    await db.feedback.update_one({"_id": d["_id"]}, {"$set": {"team_msg": mid}})     # deleted with the family
    return RedirectResponse("/home?fb=thanks", 303)


FEEDBACK_PER_HOUR = 10


@router.get("/feedback")
async def feedback_form(request: Request, ctx: Ctx = Depends(parent_page)):
    """"Send us feedback": any grown-up, any time, with screenshots if they like (the link shared with the beta
    families). Never in child mode: a locked device asks for the password first."""
    return page(request, "feedback.html", ctx, sent=request.query_params.get("sent"), shots=FAMILY_SHOTS)


@router.post("/feedback")
async def feedback_send(request: Request, ctx: Ctx = Depends(parent_page), text: str = Form(""),
                        files: list[UploadFile] = File(default=[])):
    """Kept with the family's other feedback (deleted with it) and posted to the "Family feedback" thread."""
    text = (text or "").strip()[:3000]
    shots = [f for f in files if f is not None and (f.filename or "").strip()]
    key = f"feedback:{ctx.account['_id']}"
    if not (text or shots) or await over_limit(key, FEEDBACK_PER_HOUR, 60):
        err = ("You've sent a lot of messages in the last hour. Please try again a little later."
               if text or shots else "Write a few words or add a screenshot first.")
        return page(request, "feedback.html", ctx, status_code=400, error=err, text=text, shots=FAMILY_SHOTS)
    await hit(key)
    kids = [p["name"] async for p in db.pupils.find({"family_id": ctx.family["_id"]}, {"name": 1})]
    mid = await post_family_feedback(
        "✉️ Message" + (f" · {len(shots)} screenshot{'s' if len(shots) > 1 else ''}" if shots else "") + "\n"
        + (f"“{text}”\n" if text else "")
        + f"{ctx.family['name']} ({ctx.role}) · children: {', '.join(kids) or 'none yet'}", shots)
    now = datetime.datetime.utcnow()
    await db.feedback.insert_one({"_id": f"{ctx.account['_id']}:m:{mid}", "account_id": ctx.account["_id"],
                                  "family_id": ctx.family["_id"], "card": "message", "status": "sent", "text": text,
                                  "shots": len(shots), "shown_at": now, "at": now, "team_msg": mid})
    return RedirectResponse("/feedback?sent=1", 303)


def names_text(names: list) -> str:
    """"Ava", "Ava and Max", "Ava, Max and Leo"."""
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1] if names else ""


def reward_gap(family: dict, pupils: list) -> dict | None:
    """One child has a reward of their own and a brother or sister has none at all (no own reward, no family
    reward): {"without": "Ava and Max", "n", "reward": the first own reward} for "Ava and Max have no reward. Use
    the family reward?" (a one-tap family reward for the others). None otherwise, or without the rewards plan."""
    if len(pupils) < 2 or not plan_of(family)["rewards"] or (family.get("reward") or {}).get("text"):
        return None
    own = [p for p in pupils if (p.get("reward") or {}).get("text")]
    none = [p["name"] for p in pupils if not (p.get("reward") or {}).get("text")]
    if not own or not none:
        return None
    return {"without": names_text(none), "n": len(none), "reward": own[0]["reward"]}


@router.post("/settings/family-reward")
async def family_reward(request: Request, ctx: Ctx = Depends(full_page), reward_text: str = Form(""),
                        reward_threshold: int = Form(100), back: str = Form("")):
    """"Use the family reward?": the family reward set in one tap (from a child's own reward), so no child is
    left with none. Every child without a reward of their own gets it."""
    text = reward_text.strip()[:120]
    if text and plan_of(ctx.family)["rewards"]:
        r = {"text": text, "threshold": max(10, min(100, reward_threshold))}
        await db.families.update_one({"_id": ctx.family["_id"]}, {"$set": {"reward": r}})
        await log_event(ctx.family["_id"], "plan", f"{adult_name(ctx.account)} set the family reward: "
                        f"“{r['text']}” at {r['threshold']}% of the day")
    where = f"/children/{back}/edit?family_reward=1" if re.fullmatch(r"p_[0-9a-f]+", back or "") else "/home?family_reward=1"
    return RedirectResponse(where, 303)


def _pending(p: dict, family: dict) -> list | None:
    """Tomorrow's plan when it differs from today's ("From tomorrow: Maths 15"), else None."""
    now, nxt = todays_plan(p, family), todays_plan(p, family, _tomorrow())
    return nxt if [(a["key"], a["target"]) for a in nxt] != [(a["key"], a["target"]) for a in now] else None


def _check_today(p: dict) -> dict | None:
    """The Year 4 check on Home, on a day with one: {"score" (today's latest), "of", "n" (checks today), "best" (ever)}."""
    rows = [r for r in p.get("mtc") or [] if r.get("day") == progress.today()]
    if not rows:
        return None
    return {"score": rows[-1]["score"], "of": rows[-1].get("of") or 25, "n": len(rows),
            "best": max(r["score"] for r in p["mtc"])}


def _form_activities(form, year: int) -> dict:
    acts = {}
    for k in ORDER:
        try:
            target = max(1, min(200, int(form.get(f"target_{k}") or ACTIVITIES[k]["target"])))
        except ValueError:
            target = ACTIVITIES[k]["target"]
        acts[k] = {"on": bool(form.get(f"on_{k}")) and year >= ACTIVITIES[k]["min_year"], "target": target}
    if form.get("check_tables"):                   # a Year 4 check each day, as part of the times-tables target
        acts["tables"]["check"] = True
    if form.get("check_slow"):                     # "Extra time to start with": 9 seconds a question in the check
        acts["tables"]["slow"] = True
    return acts


def _full_reason(family: dict) -> str:
    """Why no more children: the plan can be upgraded ("children"), or the biggest plan is full ("limit")."""
    return "limit" if plan_of(family)["max_children"] >= max(p["max_children"] for p in PLANS.values()) else "children"


@router.get("/children/new")
async def child_new_form(request: Request, ctx: Ctx = Depends(full_page)):
    if len(await _pupils(ctx)) >= plan_of(ctx.family)["max_children"]:
        return page(request, "upgrade.html", ctx, reason=_full_reason(ctx.family), plan=plan_of(ctx.family))
    # the year list opens on Year 1, so its plan is ticked; the form's script re-ticks when the year changes
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=None, years=YEARS,
                acts=default_activities(YEARS[0]), new_focus=_new_focus(ctx.family), school_max=spelling.SCHOOL_MAX,
                school_keep=spelling.KEEP)


def _new_focus(family: dict) -> dict:
    """"Working on this at school" on the Add-a-child form: the focus menu of every school year, {year: [(label,
    [[value, strand name], ...]), ...]}; the form's script shows the chosen year's."""
    return {y: [(label, [[f"{subj}:{s}", strand_label(s) + bank_engine.earlier_note(subj, y).get(s, "")] for s in strands])
                for label, subj, strands in _focus_groups(_focus_options({"year": y}, family))] for y in YEARS}


@router.post("/children/new")
async def child_new(request: Request, ctx: Ctx = Depends(full_page)):
    form = await request.form()
    if len(await _pupils(ctx)) >= plan_of(ctx.family)["max_children"]:
        return page(request, "upgrade.html", ctx, reason=_full_reason(ctx.family), plan=plan_of(ctx.family),
                    status_code=403)
    name = (form.get("name") or "").strip()[:30]
    pin = (form.get("pin") or "").strip()
    try:
        year = int(form.get("year") or 0)
    except ValueError:
        year = 0
    err = None
    if not name:
        err = "Give your child's first name or a nickname."
    elif year not in YEARS:
        err = "Choose a school year."
    elif not PIN_RE.match(pin):
        err = "The PIN is 4 numbers, like 4739."
    elif (taken := await _pin_taken(ctx, pin)):
        err = f"{taken} already uses this PIN. Pick a different one."
    acts = (_form_activities(form, year) if form.get("custom") else default_activities(year)) if year in YEARS else default_activities(3)
    p = {"_id": new_id("p"), "family_id": ctx.family["_id"], "name": name, "year": year if year in YEARS else 3,
         "pin": hash_secret(pin), "pin_view": pin, "activities": acts, "reward": _form_reward(form, ctx.family),
         "created": datetime.datetime.utcnow(), **_form_calm(form)}
    # this week's school spelling list (optional, folded on the form), with the same "did you mean" check as Settings
    school, school_err = _form_school_words(form, p) if (form.get("school_words") or "").strip() else ({}, "")
    school.pop("_withdraw", None)
    err = err or school_err
    if err:
        # nothing is saved, and everything typed comes back: the plan's ticks, the reward, the topics, the list
        return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), status_code=400, error=err,
                    pupil={"name": name, "year": year, "reward": p["reward"], "calm": p["calm"], "voice": p["voice"]},
                    years=YEARS, acts=acts,
                    new_focus=_new_focus(ctx.family), focus_picks=[form.get(f"focus_{n}") or "" for n in range(FOCUS_MAX)],
                    focus_weeks=[form.get(f"focus_weeks_{n}") or "1" for n in range(FOCUS_MAX)],
                    **{k: v for k, v in _school_week_view(p, ctx.family, {"school_words": form.get("school_words") or "",
                                                                         "school_fix": spelling.school_fixes(form)}).items()
                       if k.startswith("school_")}, new_school_open=bool((form.get("school_words") or "").strip()),
                    pin_typed=pin[:4])          # the PIN stays typed too (a bounced save never empties it)
    p.update(school)
    p.update(_form_focus(form, {**p, "year": year}, ctx.family))     # "Working on this at school" (optional)
    await db.pupils.insert_one(p)
    return RedirectResponse(f"/children/{p['_id']}?added=1{'&easy=1' if easy_pin(pin) else ''}", 303)


@router.get("/children/{pid}")
async def child_detail(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    now, nxt = todays_plan(p, ctx.family), todays_plan(p, ctx.family, _tomorrow())
    planned = {a["key"] for a in now + nxt}
    # cards for what the child does today or from tomorrow, and for work done lately in an activity unticked since
    # (shown "(not in the plan now)": unticking never hides what was done)
    done_lately = set(await db.attempts.distinct("activity", {"pupil_id": p["_id"], "day": {"$in": progress.day_list(30)}}))
    on = planned | (done_lately & set(ACTIVITIES))
    stats = {
        "maths": await maths.summary(p) if "maths" in on else None,
        "tables": await tables.mastered_count(p) if "tables" in on else None,
        "spelling": await spelling.learned_count(p) if "spelling" in on else None,
        "verbs": await verbs.summary(p) if "verbs" in on else None,
        "grammar": await bank.grammar.summary(p) if "grammar" in on else None,
        "science": await bank.science.summary(p) if "science" in on else None,
    }
    hist = await progress.history(p, ctx.family, 14)
    pending = [(a["key"], a["target"]) for a in nxt] != [(a["key"], a["target"]) for a in now]
    reports = await _reports(p, ctx)
    mistakes = await progress.mistakes(p, progress.day_list(7))
    _mark_reported(mistakes, reports)
    _split_mistakes(mistakes, {a["key"] for a in now})
    skills = await _skill_views(p, on)
    return page(request, "child_detail.html", ctx, pupil=p, hist=hist, fixc=await fix_counts(p, now),
                hist_keys=[k for k in ORDER if any(it["key"] == k for h in hist for it in h["items"] + h["unplanned"])],
                stats=stats, added=request.query_params.get("added"), maths_year=maths.engine_year(levels.level(p, "maths")),
                mistakes=mistakes, pending=nxt if pending else None, reports=reports,
                skills=skills, plan_items=now, TIPS=TIPS, offplan=on - planned, started=await _started(p, on),
                accuracy=accuracy(hist[-7:]), hints=level_hints(p, accuracy(hist[-7:])), work_on=await work_on(p, on), reasons=REPORT_REASONS,
                reported=request.query_params.get("reported"), sats=await sats_view(p, ctx.family),
                school=await spelling.school_status(p) if "spelling" in on else None,
                other_words=await spelling.other_tries(p, progress.day_list(7)) if "spelling" in on else [],
                focus=[{"title": focus_title(i["subject"], i["strand"]), "until": i["until"],
                        "off": i["subject"] not in {a["key"] for a in nxt}} for i in focus_items(p)],
                focus_off=_focus_off(p, ctx.family), rest_today=rest_day(p),
                pdays=days_text(practice_days_on(p, _tomorrow())),
                days_off=[o for o in p.get("days_off") or [] if o["to"] >= progress.today()])


# ---- the progress page at a glance: how each activity goes, what to work on next, what is under way ----

def _split_mistakes(mistakes: list, plan: set) -> None:
    """The same rule as the child's "Practise my mistakes" (progress.mistake_book and today's plan): a mistake the
    app can ask again stays "to go over"; one it cannot (no question like it could be made, or its activity is not
    in today's plan) moves to `cannot`, a quieter line, so the parent's count and the child's agree."""
    for d in mistakes:
        d["cannot"] = [i for i in d["items"] if i.get("nolike") or i["activity"] not in plan]
        d["items"] = [i for i in d["items"] if i not in d["cannot"]]


async def fix_counts(p: dict, plan_items: list) -> dict:
    """What the child's own My day shows (routes/child.me, the same rule: progress.mistake_book with today's plan):
    ready, the number on "Practise my mistakes (N)" (a round of at most FIX_BATCH), and later, "N more come back
    later" with when; open = due + later is "to go over", so the parent reads "8 to go over: 6 ready now, 2 come
    back tomorrow" and can see both numbers on the child's screen."""
    order = [a["key"] for a in plan_items]
    book = await progress.mistake_book(p, plan=set(order))
    due = _due(book)
    later = [e for e in book if e["state"] == "later"]
    n_due = sum(len(v) for v in due.values())
    return {"open": n_due + len(later), "due": n_due, "ready": sum(len(v) for v in pick_batch(due, order).values()),
            "later": len(later), "when": progress.back_when([e["back"] for e in later])}


def accuracy(hist: list) -> list:
    """THE one rule for "right first time" per activity, on Home, Progress and the printed report: over these days
    of progress.history, [{key, title, img, first, right, pct, extra, extra_right, extra_pct, fixq, days, weak,
    early}] in the plan's order. pct is the planned questions, up to each day's target; extra (extra_pct) is THE
    one extra figure of progress.day_stats, questions after a target outside "Practise my mistakes"; fixq the
    mistakes practised there. weak ("needs help"): below WEAK_PCT over at least WEAK_MIN first tries on at least
    WEAK_DAYS days (days), and still below it with the extras in, so extra practice never makes an activity "needs
    help" by itself, and good extra practice can lift it out. early ("early days"): below WEAK_PCT, but too soon to
    say more."""
    tot: dict = {}
    days: dict = {}
    fixq: dict = {}
    for h in hist:
        st = h.get("stats") or {}
        for i, part in enumerate(("acts", "acts_extra")):
            for k, (first, right) in (st.get(part) or {}).items():
                t = tot.setdefault(k, [0, 0, 0, 0])
                t[2 * i], t[2 * i + 1] = t[2 * i] + first, t[2 * i + 1] + right
        for k, (first, _) in (st.get("acts") or {}).items():
            days[k] = days.get(k, 0) + (1 if first else 0)
        for k, n in (st.get("acts_fix") or {}).items():
            fixq[k] = fixq.get(k, 0) + n
    out = []
    for k in ORDER:
        if k not in tot or not (tot[k][0] or tot[k][2]):
            continue
        first, right, xf, xr = tot[k]
        pct = progress.pct(right, first)
        low = pct is not None and pct < WEAK_PCT and 100 * (right + xr) < WEAK_PCT * (first + xf)
        weak = bool(low and first >= WEAK_MIN and days.get(k, 0) >= WEAK_DAYS)
        out.append({**ACTIVITIES[k], "key": k, "first": first, "right": right, "pct": pct if pct is not None else progress.pct(xr, xf),
                    "extra": xf, "extra_right": xr, "extra_pct": progress.pct(xr, xf), "only_extra": not first,
                    "fixq": fixq.get(k, 0), "days": days.get(k, 0), "weak": weak, "early": bool(low and not weak)})
    return out


# "needs help": under 70% right first time, over at least 30 first tries on at least 3 days in that activity (sooner
# it says "early days"). Extra answers after a target and Year 4 check facts beyond the year are left out (day_stats).
WEAK_PCT, WEAK_MIN, WEAK_DAYS = 70, 30, 3
HINT_DAYS = 7                     # "a smaller target" or "a year lower": only once the child has had a week of practice
AHEAD_PCT, AHEAD_MIN = 85, 30     # "Try Maths at Year 9 level": 85% right first time over 30 first tries in it
LOW_PCT = 60                      # "Maths is hard at the moment": "needs help", and under 60% right first time


def level_hints(p: dict, acc: list) -> dict:
    """What Progress suggests, subject by subject, from the last 7 days (accuracy): {"up": [...], "down": [...]},
    each {key, title, pct, first, level, to}. up: maths, grammar or science mostly right first time (AHEAD_PCT over
    AHEAD_MIN first tries), below Year 9: try that subject a year up. down: an activity that "needs help" and is
    under LOW_PCT: maths, grammar and science can work a year lower (to: that year, none at Year 1), and any
    activity can have a smaller daily target; only from HINT_DAYS after the child's first day."""
    up, down = [], []
    first = progress.first_day(p)
    week = bool(first) and (datetime.date.fromisoformat(progress.today()) - datetime.date.fromisoformat(first)).days >= HINT_DAYS
    for a in acc:
        lv = levels.level(p, a["key"]) if a["key"] in levels.SUBJECTS else None
        h = {"key": a["key"], "title": a["title"].split(" and ")[0], "pct": a["pct"], "first": a["first"], "level": lv}
        if lv and lv < YEARS[-1] and a["first"] >= AHEAD_MIN and 100 * a["right"] >= AHEAD_PCT * a["first"]:
            up.append({**h, "to": lv + 1})
        elif a["weak"] and a["pct"] < LOW_PCT and week:
            down.append({**h, "to": lv - 1 if lv and lv > YEARS[0] else None})
    return {"up": up, "down": down}


async def work_on(p: dict, on: set, n: int = 6) -> list:
    """The weakest skills, by real weakness: only skills with wrong answers, not secure yet; those with enough
    answers (WORK_MIN) and the lowest share right first, then the most wrong. A skill answered only right is never
    on it, however low its score. [{subject, key, title, strand, wrong, attempts, pct}]"""
    out = []
    if "maths" in on:
        titles = {s["key"]: s for s in maths_mastery.skill_list()}
        for d in (await maths_mastery._mastery_map(p["_id"])).values():
            if "correct_count" in d and d.get("skill") in titles:
                out.append(("maths", titles[d["skill"]], int(d.get("attempts", 0)), int(d["correct_count"]), d))
    for subject in ("grammar", "science"):
        if subject in on:
            async for d in db.bank_mastery.find({"pupil_id": p["_id"], "subject": subject}):
                sk = bank_engine.skill(d.get("key", ""))
                if sk and "correct" in d:
                    out.append((subject, sk, int(d.get("attempts", 0)), int(d["correct"]), d))
    weak = [{"subject": subj, "key": sk["key"], "title": sk["title"], "strand": sk.get("strand", ""),
             "wrong": att - right, "attempts": att, "pct": 100 * right // att}
            for subj, sk, att, right, d in out if att > right and int(d.get("score", 0)) < maths_mastery.MASTERED]
    weak.sort(key=lambda w: (w["attempts"] < WORK_MIN, w["pct"], -w["wrong"]))
    return weak[:n]


WORK_MIN = 3            # answers on a skill before its share right counts for "To work on next"


async def _started(p: dict, on: set) -> dict:
    """What is under way but not mastered yet, per activity ({"maths": 6, ...}), so a good first day never reads
    0 everywhere: maths, grammar and science skills answered; times-tables facts right at least once; spelling
    words and irregular verbs asked."""
    out = {}
    if "maths" in on:
        keys = {s["key"] for s in maths_mastery._year_skills(maths.engine_year(levels.level(p, "maths")))}
        out["maths"] = sum(1 for k, d in (await maths_mastery._mastery_map(p["_id"])).items()
                           if k in keys and d.get("attempts") and int(d.get("score", 0)) < maths_mastery.MASTERED)
    if "tables" in on:
        out["tables"] = await db.tables_facts.count_documents(
            {"pupil_id": p["_id"], "a": {"$in": tables.tables_for_year(p.get("year", 4))}, "right": {"$gte": 1},
             "streak": {"$lt": 3}})
    if "spelling" in on:
        out["spelling"] = await db.spelling_words.count_documents(
            {"pupil_id": p["_id"], "word": {"$in": spelling.list_for_year(p.get("year", 3))},
             "box": {"$lt": spelling.LEARNED_BOX}})
    for subject in ("grammar", "science"):
        if subject in on:
            keys = {s["key"] for s in bank_engine.skills(subject, levels.level(p, subject))}
            out[subject] = len([1 async for d in db.bank_mastery.find({"pupil_id": p["_id"], "subject": subject})
                                if d.get("key") in keys and int(d.get("score", 0)) < maths_mastery.MASTERED])
    if "verbs" in on:
        st = (await db.verbs_state.find_one({"pupil_id": p["_id"]})) or {}
        out["verbs"] = sum(1 for v in (st.get("streaks") or {}).values() if v < verbs.MASTER_STREAK)
    return out


def _focus_off(p: dict, family: dict) -> list:
    """The subjects of a running school focus that are not in the child's plan (from tomorrow): [{key, title}].
    Such a focus does nothing until the subject is ticked, so the parent is told, with a one-click fix."""
    nxt = {a["key"] for a in todays_plan(p, family, _tomorrow())}
    out = []
    for i in focus_items(p):
        if i["subject"] not in nxt and i["subject"] in ACTIVITIES and all(o["key"] != i["subject"] for o in out):
            out.append({"key": i["subject"], "title": ACTIVITIES[i["subject"]]["title"],
                        "can": i["subject"] in plan_of(family)["activities"]
                        and p.get("year", 1) >= ACTIVITIES[i["subject"]]["min_year"]})
    return out


@router.post("/children/{pid}/plan-add")
async def plan_add(request: Request, pid: str, ctx: Ctx = Depends(full_page), activity: str = Form(""),
                   back: str = Form("")):
    """"Science isn't in Grace's plan. Add it?": tick one activity at its default target, by the plan's rule
    (straight away before the child starts today, else from tomorrow)."""
    p = await own_pupil(ctx, pid)
    acts = {k: dict(v) for k, v in _acts(p).items()}
    if activity in ACTIVITIES and activity in plan_of(ctx.family)["activities"] \
            and p["year"] >= ACTIVITIES[activity]["min_year"] and not acts[activity].get("on"):
        acts[activity]["on"] = True
        upd = await _new_plan(p, acts, False)
        upd["edits"] = (p.get("edits") or [])[-4:] + [{"at": datetime.datetime.utcnow(), "by": ctx.account["_id"],
                                                       "who": adult_name(ctx.account), "groups": ["plan"]}]
        lines = _changes(p, upd, ctx.family)
        await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
        for line in lines:
            await _log_change(ctx, p, f"{adult_name(ctx.account)} {line}")
    where = f"/children/{p['_id']}/edit?saved=1" if back == "edit" else f"/children/{p['_id']}?plan_added={activity}"
    return RedirectResponse(where, 303)


@router.post("/children/{pid}/mistakes/report")
async def report_mistake(request: Request, pid: str, ctx: Ctx = Depends(parent_page), rid: str = Form(""),
                         reason: str = Form(""), note: str = Form("")):
    """"Report this question" from "Mistakes to go over": a grown-up reports a question from an earlier day (the
    child's screen only reports the one on it). It goes to the same checking queue, marked as the grown-up's."""
    p = await own_pupil(ctx, pid)
    r = await db.attempts.find_one({"_id": ObjectId(rid), "pupil_id": p["_id"]}) if ObjectId.is_valid(rid) else None
    if not r or reason not in REPORT_REASONS:
        return RedirectResponse(f"/children/{p['_id']}#mistakes", 303)
    # the grown-ups' own daily limit: their reports never use up the child's (child.py counts only the child's)
    since = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    if await db.reports.count_documents({"pupil_id": p["_id"], "ts": {"$gt": since}, "by": {"$exists": True}}) >= REPORTS_PER_DAY:
        return RedirectResponse(f"/children/{p['_id']}?reported=limit#mistakes", 303)
    await db.reports.insert_one({
        "family_id": ctx.family["_id"], "pupil_id": p["_id"], "activity": r["activity"],
        "year": levels.level(p, r["activity"]) if r["activity"] in levels.SUBJECTS else p.get("year"),
        "skill": str(r.get("detail") or "").split("#")[0] or None, "reason": reason, "note": note.strip()[:500],
        "token": "", "served": {"prompt": r.get("q", ""), "from": "mistakes"}, "expected": r.get("exp"),
        "answer": r.get("got"), "device": {}, "day": r["day"], "ts": datetime.datetime.utcnow(), "status": "open",
        "by": ctx.account["_id"], "by_name": adult_name(ctx.account), "attempt": str(r["_id"])})
    return RedirectResponse(f"/children/{p['_id']}?reported=1#reports", 303)


REPORTS_PER_DAY = 10            # the grown-ups' reports of one child a day; the child has their own 10 (routes/child.py)


# ---- SATs (Year 6): which topics of each paper are practised, not started yet, or weak. Coverage only. ----
# The maths skills of the arithmetic paper (written calculation), mapped by hand; every other Year 6 maths skill
# (place value, fractions, ratio, algebra, geometry, measures, statistics, problems) is on the reasoning papers.
SATS_ARITHMETIC = {"Y6.1.a", "Y6.1.b", "Y6.1.c", "Y6.1.d", "Y6.1.e", "Y6.1.f", "Y6.1.h", "Y6.2.f", "Y6.5.d", "Y6.5.e",
                   "Y6.5.f", "Y6.5.g", "Y6.5.h", "Y6.6.f"}
SATS_WEEKS = 2
SATS_SHOW = 6                   # topics named per line; the rest are counted


SATS_WEAK_PCT = 60             # "weak" in the SATs card: under 60% right over at least WORK_MIN answers, not secure


def _sats_state(doc: dict | None, right_key: str) -> str:
    """One SATs topic: "secure", "weak" (a genuinely low share right), "started" (practised, not secure yet: 8 of 9
    right is this, never weak) or "new"."""
    d = doc or {}
    att, right = int(d.get("attempts", 0)), int(d.get(right_key, 0))
    if not att:
        return "new"
    if int(d.get("score", 0)) >= maths_mastery.MASTERED:
        return "secure"
    if att >= WORK_MIN and 100 * right < SATS_WEAK_PCT * att:
        return "weak"
    return "started"


async def _sats_papers(p: dict) -> list:
    """The four SATs papers: {key, title, total, practised, secure, todo (not started yet), weak (genuinely low),
    started (practised, not secure yet), gaps: [(subject, strand, weight)] of its weak and not-started topics}."""
    mm = await maths_mastery._mastery_map(p["_id"])
    gm = {d["key"]: d async for d in db.bank_mastery.find({"pupil_id": p["_id"], "subject": "grammar"})}
    msk = maths_mastery._year_skills(6)

    def paper(key, title, skills, docs, subj, right_key):
        st = {s["key"]: _sats_state(docs.get(s["key"]), right_key) for s in skills}
        return {"key": key, "title": title, "total": len(skills), "unit": "topics",
                "practised": sum(1 for v in st.values() if v != "new"),
                "secure": sum(1 for v in st.values() if v == "secure"),
                "todo": [s["title"] for s in skills if st[s["key"]] == "new"],
                "weak": [s["title"] for s in skills if st[s["key"]] == "weak"],
                "started": [s["title"] for s in skills if st[s["key"]] == "started"],
                "gaps": [(subj, s["strand"], 2 if st[s["key"]] == "weak" else 1 if st[s["key"]] == "new" else 0.25)
                         for s in skills if st[s["key"]] != "secure"]}
    out = [paper("arithmetic", "Maths: arithmetic", [s for s in msk if s["key"] in SATS_ARITHMETIC], mm, "maths", "correct_count"),
           paper("reasoning", "Maths: reasoning", [s for s in msk if s["key"] not in SATS_ARITHMETIC], mm, "maths", "correct_count"),
           paper("gps", "Grammar and punctuation", bank_engine.skills("grammar", 6), gm, "grammar", "correct")]
    words = spelling.list_for_year(6)
    sw = {d["word"]: d async for d in db.spelling_words.find({"pupil_id": p["_id"], "word": {"$in": words}})}
    learning = {w: d for w, d in sw.items() if int(d.get("box", 0)) < spelling.LEARNED_BOX}
    # weak: missed at least as often as spelt right, and not right on a later day yet (box 0)
    weak = [w for w, d in learning.items() if int(d.get("box", 0)) == 0 and int(d.get("wrong", 0)) >= max(1, int(d.get("right", 0)))]
    out.append({"key": "spelling", "title": "Spelling", "total": len(words), "practised": len(sw), "unit": "words",
                "secure_word": "learned", "secure": len(sw) - len(learning),
                "todo": [], "todo_n": len(words) - len(sw), "weak": weak,
                "started": [w for w in learning if w not in weak], "gaps": []})
    return out


async def sats_view(p: dict, family: dict) -> dict | None:
    """For a Year 6 child (by school year): the four SATs papers (_sats_papers); and the "Revise for SATs" switch:
    on (its topics still running, and their end day), its topics, the parent's own topics, and how many free
    topic slots are left (it only ever fills those). None for other years."""
    if school_year(p) != 6:
        return None
    s = p.get("sats") or {}
    running = [(i["subject"], i["strand"]) for i in focus_items(p)]
    picks = [tuple(x) for x in s.get("strands") or [] if tuple(x) in running]
    own = [x for x in running if x not in picks]
    return {"papers": await _sats_papers(p), "on": bool(picks), "picks": [focus_title(a, b) for a, b in picks],
            "own": [focus_title(a, b) for a, b in own], "free": FOCUS_MAX - len(running),
            "until": s.get("until", ""), "grammar_on": "grammar" in {a["key"] for a in todays_plan(p, family, _tomorrow())}}


async def _sats_picks(p: dict, family: dict, n: int, skip: set) -> list:
    """Up to n strands "Revise for SATs" brings forward, from the SATs card's own gaps: the papers least covered
    first (the arithmetic paper when it is barely started), and in each the strand with the most weak and
    not-started topics (a weak topic counts double). Then the next paper, and round again. skip: strands
    already in the focus."""
    opts = _focus_options(p, family)
    # covered: practised and not weak (a weak topic is a gap still)
    papers = sorted([pp for pp in await _sats_papers(p) if pp["gaps"]],
                    key=lambda pp: (pp["practised"] - len(pp["weak"])) / pp["total"])
    ranked = []
    for pp in papers:
        w: dict = {}
        for subj, strand, weight in pp["gaps"]:
            if strand in opts.get(subj, []) and (subj, strand) not in skip:
                w[(subj, strand)] = w.get((subj, strand), 0) + weight
        ranked.append(sorted(w, key=lambda k: -w[k]))
    picks: list = []
    while len(picks) < n and any(ranked):
        for r in ranked:
            while r and r[0] in picks:
                r.pop(0)
            if r and len(picks) < n:
                picks.append(r.pop(0))
    return picks


@router.post("/children/{pid}/sats")
async def sats_switch(request: Request, pid: str, ctx: Ctx = Depends(full_page), on: str = Form(""),
                      replace: str = Form("")):
    """"Revise for SATs": for SATS_WEEKS the free topic slots of "Working on this at school" go to the SATs card's
    gaps (_sats_picks). Topics the parent picked stay: with no slot free it asks first, and only "replace" (the
    parent's answer) puts SATs topics in their place. Off: only its own topics stop."""
    p = await own_pupil(ctx, pid)
    if school_year(p) != 6:
        return RedirectResponse(f"/children/{p['_id']}", 303)
    today = progress.today()
    mine = {tuple(x) for x in (p.get("sats") or {}).get("strands") or []}
    own = [i for i in focus_items(p) if (i["subject"], i["strand"]) not in mine]
    if on:
        if len(own) >= FOCUS_MAX and not replace:
            return RedirectResponse(f"/children/{p['_id']}?sats=full#sats", 303)
        keep = [] if replace else own
        picks = await _sats_picks(p, ctx.family, FOCUS_MAX - len(keep), {(i["subject"], i["strand"]) for i in keep})
        until = _plus_days(7 * SATS_WEEKS)
        focus = keep + [{"subject": a, "strand": b, "weeks": SATS_WEEKS, "from": today, "until": until} for a, b in picks]
        upd = {"focus": focus or None, "sats": {"strands": [list(x) for x in picks], "from": today, "until": until}}
        what = (f"turned on Revise for SATs for {p['name']}: " + ", ".join(focus_title(a, b) for a, b in picks)
                + f", until {day_label(until)}") if picks else ""
        if replace and own:
            what += " (in place of " + ", ".join(focus_title(i["subject"], i["strand"]) for i in own) + ")"
    else:
        upd = {"focus": own or None, "sats": None}
        what = f"turned off Revise for SATs for {p['name']}" if mine else ""
    upd["edits"] = (p.get("edits") or [])[-4:] + [{"at": datetime.datetime.utcnow(), "by": ctx.account["_id"],
                                                   "who": adult_name(ctx.account), "groups": ["focus"]}]
    await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    if what:
        await _log_change(ctx, p, f"{adult_name(ctx.account)} {what}")
    return RedirectResponse(f"/children/{p['_id']}?sats={'on' if on else 'off'}#sats", 303)


def _tomorrow() -> str:
    return (datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=1)).isoformat()


REPORT_DAYS = 30
REPORT_OUTCOMES = {"open": "we're checking", "fixed": "fixed, thank you", "not_a_problem": "checked: the question is right"}


def _report_question(r: dict) -> str:
    """The question a report is about, as the family saw it (short)."""
    sv = r.get("served") or {}
    if r.get("activity") == "spelling":
        return f"spelling “{r.get('expected')}”" if r.get("expected") else "a spelling"
    if r.get("activity") == "verbs" and sv.get("base"):
        return f"past forms of “{sv['base']}”"
    q = " ".join(str(sv.get("prompt") or "").split())
    return (q[:110] + "…") if len(q) > 110 else q or ACTIVITIES.get(r.get("activity"), {}).get("title", "a question")


def _report_answers(r: dict) -> tuple:
    """(our answer, the child's answer, whether the child's answer was right) in plain words. A question-bank
    report keeps the answer key ({'t': 'mcq', 'right': 1, 'opts': [...]}) and the child's raw value (an option's
    number, the words tapped): both are read through the bank's own wording, never shown as they are stored."""
    exp, got = r.get("expected"), r.get("answer")
    if got is not None and not isinstance(got, str):
        got = str(got)
    right = None
    if isinstance(exp, dict) and exp.get("t"):
        value = got
        try:
            value = json.loads(got) if got not in (None, "") else None
        except ValueError:
            pass
        right = bank_engine.mark(exp, value) if got not in (None, "") else None
        got = bank_engine.given_text(exp, value) if got not in (None, "") else ""
        exp = bank_engine.expected_text(exp) + (f" {exp['unit']}" if exp.get("unit") else "")
    elif isinstance(exp, dict) and exp.get("past"):          # irregular verbs: {"past": [...], "pp": [...]}
        exp = f"{exp['past'][0]}, {(exp.get('pp') or [''])[0]}"
        try:
            g = json.loads(got or "")
            got = f"{g.get('past', '')}, {g.get('pp', '')}" if isinstance(g, dict) else got
        except ValueError:
            pass
    elif isinstance(exp, (list, dict)):
        exp = ", ".join(str(x) for x in exp) if isinstance(exp, list) else ""
    return ("" if exp is None else str(exp)), (got or ""), right


async def _reports(p: dict, ctx: Ctx | None = None) -> list:
    """The child's "Something wrong with this question?" reports of the last REPORT_DAYS, newest first, with
    what the team found. who: who sent it ("you" for the grown-up reading the page, another grown-up's name,
    or the child's name)."""
    since = datetime.datetime.utcnow() - datetime.timedelta(days=REPORT_DAYS)
    out = []
    async for r in db.reports.find({"pupil_id": p["_id"], "ts": {"$gt": since}}).sort("ts", -1).limit(20):
        sv = r.get("served") or {}
        t = local_time(r["ts"])                   # Europe/London (config.TIMEZONE), not the server's clock
        exp, got, right = _report_answers(r)
        who = ("You" if ctx and r.get("by") == ctx.account["_id"] else r.get("by_name")) if r.get("by") else p["name"]
        out.append({"activity": r.get("activity"), "question": _report_question(r), "note": r.get("note") or "",
                    "reason": REPORT_REASONS.get(r.get("reason"), ""), "status": r.get("status") or "open",
                    "outcome": REPORT_OUTCOMES.get(r.get("status") or "open", ""), "reply": r.get("reply") or "",
                    "answer": got, "answer_right": right, "expected": exp if r.get("expected") is not None else None,
                    "attempt": r.get("attempt"),
                    "day": r.get("day", ""), "who": who or "A grown-up",
                    "when": f"{t.day} {t:%b} {t:%H:%M}", "prompt": " ".join(str(sv.get("prompt") or "").split())})
    return out


def _mark_reported(mistakes: list, reports: list) -> None:
    """Mark a mistake "reported" when THAT item was reported, never others: a grown-up's report from this list
    names the miss it was sent from (attempt); a child's report is the question as served on a day the item was
    missed. A prompt that several items share ("Spell the word you heard", or any prompt seen with two different
    answers) only marks the item with the same expected answer."""
    its = [it for d in mistakes for it in d.get("items", []) + d.get("fixed", []) + d.get("cannot", [])]
    norm = lambda t: " ".join(str(t or "").split())          # noqa: E731
    answers: dict = {}
    for it in its:
        answers.setdefault((it.get("activity"), norm(it.get("q"))), set()).add(str(it.get("exp", "")))
    shared = {k for k, v in answers.items() if len(v) > 1 or k[0] == "spelling"}

    def hit(r: dict, it: dict) -> bool:
        if r.get("attempt"):
            return r["attempt"] in (it.get("rids") or [it.get("rid")])
        if r["activity"] != it.get("activity") or r["day"] not in (it.get("days") or []):
            return False
        q, exp = norm(it.get("q")), str(it.get("exp", ""))
        same_exp = r["expected"] is not None and str(r["expected"]) == exp
        if (it["activity"], q) in shared:
            return same_exp
        if it["activity"] in ("verbs", "numbers"):            # one item per answer: the expected answer names it
            return same_exp or bool(r["prompt"]) and q == r["prompt"]
        # a bank mistake keeps its question and its sentence: the question as served starts it
        return bool(r["prompt"]) and (q == r["prompt"] or it["activity"] in ("grammar", "science") and same_exp
                                      and q.startswith(r["prompt"]))
    for it in its:
        it["reported"] = any(hit(r, it) for r in reports)


def _recheck(docs) -> set:
    """Skills secured on the day they were last answered: still to be re-checked on a later day."""
    return {k for k, d in docs if isinstance(d.get("mastered_at"), datetime.datetime) and not d.get("checked")
            and isinstance(d.get("last"), datetime.datetime) and d["last"].date() == d["mastered_at"].date()}


def _by_strand(skills: list, scores: dict, recheck: set = frozenset()) -> list:
    """[{strand, secure, practising, new, skills: [{title, score, state, recheck}]}] in teaching order. Secure =
    mastered (score 100; recheck: secured lately, re-checked on a later day); practising = answered at least
    once; not started = never asked yet."""
    out: dict = {}
    for s in skills:
        sc = scores.get(s["key"])
        state = "new" if sc is None else "secure" if sc >= maths_mastery.MASTERED else "practising"
        g = out.setdefault(s["strand"], {"strand": s["strand"], "secure": 0, "practising": 0, "new": 0, "skills": []})
        g[state] += 1
        g["skills"].append({"title": s["title"], "score": sc or 0, "state": state,
                            "recheck": state == "secure" and s["key"] in recheck})
    rank = {"practising": 0, "secure": 1, "new": 2}           # the weakest started skills first
    for g in out.values():
        g["skills"].sort(key=lambda s: (rank[s["state"]], s["score"] if s["state"] == "practising" else 0))
    return list(out.values())


async def _skill_views(p: dict, on: set) -> dict:
    """Where the child is secure or still practising, strand by strand, for maths and the question banks."""
    out = {}
    if "maths" in on:
        mm = await maths_mastery._mastery_map(p["_id"])
        year = maths.engine_year(levels.level(p, "maths"))
        scores = {k: int(d.get("score", 0)) for k, d in mm.items() if d.get("attempts", 1)}
        recheck = _recheck(mm.items())
        out["maths"] = _by_strand(maths_mastery._year_skills(year), scores, recheck)
        # Years 8 and 9 also review earlier KS3 skills: those met so far show under their own year's strand
        review = _by_strand([s for s in maths_mastery._earlier_ks3(year) if s["key"] in scores], scores, recheck)
        out["maths"] += [{**g, "review": g["strand"].split(".")[0]} for g in review]
    for subject in ("grammar", "science"):
        if subject in on:
            docs = [d async for d in db.bank_mastery.find({"pupil_id": p["_id"], "subject": subject})]
            out[subject] = _by_strand(bank_engine.skills(subject, levels.level(p, subject)), {d["key"]: int(d.get("score", 0)) for d in docs},
                                      _recheck((d["key"], d) for d in docs))
    return out


def _form_reward(form, family: dict) -> dict | None:
    """The child's own reward from the form; None (use the family's) when left empty or without the plan."""
    text = (form.get("reward_text") or "").strip()[:120]
    if not text or not plan_of(family)["rewards"]:
        return None
    try:
        threshold = int(form.get("reward_threshold") or 100)
    except ValueError:
        threshold = 100
    return {"text": text, "threshold": max(10, min(100, threshold))}


def _acts(p: dict) -> dict:
    """The child's plan, with any activity added since they were set up at its default."""
    return {**default_activities(p["year"]), **(p.get("activities") or {})}


school_year = levels.school_year


def year_text(p: dict, report: bool = False) -> str:
    """"Year 8", and each subject worked at another year, only where it differs: "Year 8 · Maths: Year 6 level"
    (all three a year up: "Year 8, working at Year 9 level"), for every page a parent or a teacher reads.
    report: the printed report, where the parent may leave the levels out (levels_on_report)."""
    sy, diff = levels.school_year(p), levels.differs(p)
    if not diff or (report and p.get("levels_on_report") is False):
        return f"Year {sy}"
    if len(diff) == len(levels.SUBJECTS) and len({lv for _, lv in diff}) == 1:
        return f"Year {sy}, working at Year {diff[0][1]} level"
    return f"Year {sy} · {levels.levels_text(p)}"


templates.env.globals["year_text"] = year_text
templates.env.globals["local_today"] = progress.today
# One line under the "Working on this at school" menu for a topic whose name alone doesn't say what it covers
# (keyed by the name the menu shows).
FOCUS_HINTS = {
    "Test review": "the Year 3 to 5 grammar the SATs test asks about: word classes, clauses, tenses, apostrophes, "
                   "modal verbs, fronted adverbials, relative clauses and adverbs of possibility",
    "Terminology": "the grammar words of the year (noun phrase, subordinate clause, …) and what they mean",
    "Text": "paragraphs, headings and how sentences link up",
    "Working scientifically": "planning a fair test, measuring, tables and graphs, and reading results",
    "Matter": "density, conservation of mass, and physical and chemical changes",
}
templates.env.globals["FOCUS_HINTS"] = FOCUS_HINTS


# ---- who changed what: every change to a child's plan, targets, reward, days off, school list or topics is a line
# in Family activity (Home), so two grown-ups in two homes see the same picture; and, for those who ticked it, an email.

def _plan_changes(p: dict, acts: dict, start: str) -> list:
    """"added Science, 5 a day", "Maths 10 → 15 a day", "took Spelling out", each "from today" or "from tomorrow"."""
    old, out = _acts(p), []
    for k in ORDER:
        a, b = old.get(k) or {}, acts.get(k) or {}
        t = ACTIVITIES[k]["title"]
        if b.get("on") and not a.get("on"):
            out.append(f"added {t}, {b['target']} a day")
        elif a.get("on") and not b.get("on"):
            out.append(f"took {t} out")
        elif b.get("on") and int(a.get("target") or 0) != int(b.get("target") or 0):
            out.append(f"{t} {a.get('target')} → {b['target']} a day")
        if k == "tables" and b.get("on") and bool(a.get("check")) != bool(b.get("check")):
            out.append("added the Year 4 check" if b.get("check") else "took the Year 4 check out")
    when = "from today" if start == progress.today() else "from tomorrow" if start == _tomorrow() else f"from {day_label(start)}"
    return [f"{', '.join(out)}, {when}"] if out else []


def _changes(p: dict, upd: dict, family: dict) -> list:
    """What a save of a child's settings changed, in a parent's words, each to follow the grown-up's name: ["changed
    Ruby's plan: added Science, 5 a day, from today", "set Ruby's reward: “Film night” at 100% of the day", ...]."""
    out = []
    if "activities" in upd:
        start = (upd.get("plan_log") or [{}])[-1].get("from", progress.today())
        out += [f"changed {p['name']}'s plan: {c}" for c in _plan_changes(p, upd["activities"], start)]
    if "reward" in upd and upd["reward"] != p.get("reward"):
        r = upd["reward"]
        out.append(f"set {p['name']}'s reward: “{r['text']}” at {r['threshold']}% of the day" if r else
                   f"took off {p['name']}'s own reward (the family reward applies)")
    if "days_off" in upd:
        was = {(o["from"], o["to"]) for o in p.get("days_off") or []}
        now = {(o["from"], o["to"]) for o in upd["days_off"]}
        for a, b in sorted(now - was):
            out.append(f"marked a day off for {p['name']}: {day_label(a)}" + (f" to {day_label(b)}" if b != a else ""))
        for a, b in sorted(was - now):
            if b >= progress.today():
                out.append(f"cancelled {p['name']}'s day off {day_label(a)}" + (f" to {day_label(b)}" if b != a else ""))
    if "practice_days" in upd:
        out.append(f"set {p['name']}'s practice days: {days_text(upd['practice_days'])}")
    if "school_words" in upd or "school_words.kept" in upd:
        sl = upd.get("school_words")
        out.append(f"typed in {p['name']}'s school spelling list: {len(sl['words'])} words until {day_label(sl['until'])}"
                   if sl else f"ended {p['name']}'s school spelling list" if "school_words" in upd
                   else f"checked words in {p['name']}'s school spelling list")
    if "focus" in upd:
        f = upd["focus"] or []
        out.append(f"set {p['name']}'s school topics: " + ", ".join(f"{focus_title(i['subject'], i['strand'])} until "
                                                                f"{day_label(i['until'])}" for i in f)
                   if f else f"stopped {p['name']}'s school topics")
    if "year" in upd:
        out.append(f"moved {p['name']} to {year_text({**p, **upd})}")
    elif "levels" in upd:
        new = {**p, **upd}
        what = [f"{levels.TITLES[s].lower()} at Year {levels.level(new, s)} level" if levels.level(new, s) != new["year"]
                else f"{levels.TITLES[s].lower()} back at the school year" for s in levels.SUBJECTS
                if levels.level(new, s) != levels.level(p, s)]
        if what:
            out.append(f"set {p['name']}'s " + ", ".join(what) + f" (school year: Year {new['year']})")
    if "name" in upd and upd["name"] != p["name"]:
        out.append(f"renamed {p['name']} to {upd['name']}")
    return out


async def _log_change(ctx: Ctx, p: dict, text: str) -> None:
    """One change in Family activity, and an email to the other grown-ups who asked for one (plan_emails)."""
    await log_event(ctx.family["_id"], "plan", text, pupil_id=p["_id"])
    await mailer.to_family(ctx.family["_id"], f"{p['name']}'s plan on Quizocracy changed",
                           f"Hello,\n\n{text} ({local_time(datetime.datetime.utcnow()):%d %b at %H:%M}).\n\n"
                           f"Every change shows under Family activity on Home: {config.PUBLIC_URL}/home\n\n"
                           f"You get this email because you ticked it in Settings. Untick it there to stop.\n",
                           roles=("owner", "parent", "carer"), skip=(ctx.account["_id"],), flag="plan_emails")


# What a child's settings form holds, in groups: (key, what a parent calls it, its field names; a name ending in "_"
# stands for every field that starts with it). A save changes only the groups edited on that form (_changed_fields).
FORM_GROUPS = [("name", "the name", ("name",)), ("year", "the school year and levels", ("year", "level_")), ("pin", "the PIN", ("pin",)),
               ("reward", "the reward", ("reward_text", "reward_threshold")),
               ("plan", "the daily plan", ("on_", "target_", "check_", "plan_today")),
               ("school", "the spelling list", ("school_words", "school_ok", "school_fix_")), ("focus", "the school focus", ("focus_",)),
               ("pdays", "the practice days", ("pday",)), ("off", "the days off", ("off_",)),
               ("reading", "the reading settings", ("read_",)),
               ("calm", "the calm screen and read-aloud", ("calm", "voice", "voice_rate"))]
GROUP_LABELS = {k: label for k, label, _ in FORM_GROUPS}
CARER_GROUPS = {"school", "off"}           # a carer may type the school's spelling list and mark a day off
SAVED_AS = {"name": "name", "year": "year", "levels": "year", "levels_on_report": "year", "pin": "pin", "reward": "reward", "activities": "plan", "school_words": "school",
            "focus": "focus", "practice_days": "pdays", "days_off": "off", "reading": "reading", "calm": "calm", "voice": "calm"}
VOICE_MODES = ("on", "questions", "off")       # read-aloud: questions and feedback / questions only / nothing (speak.js)


def _form_calm(form) -> dict:
    """"Calm screen and read-aloud" (child_form.html): calm (no confetti or movement, the same plain "Correct.",
    nothing moves on until the child presses a button) and voice {mode, rate}."""
    mode, rate = form.get("voice") or "on", form.get("voice_rate") or "normal"
    return {"calm": bool(form.get("calm")), "voice": {"mode": mode if mode in VOICE_MODES else "on",
                                                       "rate": "slower" if rate == "slower" else "normal"}}


EASY_PINS = {"1234", "4321", "0000", "1212", "2580", "1122", "6969", "1004", "2000", "2468", "1357"}


def easy_pin(pin: str) -> bool:
    """A PIN a brother or sister could guess: one digit repeated (1111), a run up or down (1234, 6543, 9012),
    two pairs (1212, 1122), or a well-known one (2580 runs down the keypad). Structure only."""
    if not PIN_RE.match(pin or ""):
        return False
    d = [int(c) for c in pin]
    steps = {(b - a) % 10 for a, b in zip(d, d[1:])}
    return pin in EASY_PINS or (len(steps) == 1 and steps <= {0, 1, 9}) or pin[:2] == pin[2:] or (d[0] == d[1] and d[2] == d[3])


def _changed_fields(form) -> set | None:
    """The fields whose values differ from what the form showed when it was opened (`orig`, written by the form's
    script), or None without it (no script: everything counts as edited)."""
    try:
        pairs = json.loads(form.get("orig") or "")
    except ValueError:
        return None
    if not isinstance(pairs, list):
        return None
    orig: dict = {}
    for kv in pairs:
        if isinstance(kv, list) and len(kv) == 2:
            orig.setdefault(str(kv[0]), []).append(str(kv[1]))
    now = {k: [str(v) for v in form.getlist(k)] for k in set(form.keys()) - {"orig", "loaded"}}
    return {k for k in set(orig) | set(now) if orig.get(k, []) != now.get(k, [])}


def _groups(changed: set | None) -> set:
    if changed is None:
        return {k for k, _, _ in FORM_GROUPS}
    return {k for k, _, names in FORM_GROUPS
            if any(c == n or (n.endswith("_") and c.startswith(n)) for c in changed for n in names)}


def _edits_since(p: dict, ctx: Ctx, loaded: str | None) -> list:
    """The other grown-ups' saves of this child's settings after a form was opened (loaded: its UTC time)."""
    try:
        t = datetime.datetime.fromisoformat(loaded or "")
    except ValueError:
        return []
    return [e for e in p.get("edits") or [] if e["at"] > t and e["by"] != ctx.account["_id"]]


def _save_note(p: dict, ctx: Ctx, loaded: str | None) -> str:
    """After a save: who else saved since this form was opened, and whether both changed the same thing."""
    others = _edits_since(p, ctx, loaded)
    mine = next((e for e in reversed(p.get("edits") or []) if e["by"] == ctx.account["_id"]), None)
    if not others or not mine:
        return ""
    o = others[-1]
    note = (f"{o['who']} also saved {p['name']}'s settings at {local_time(o['at']):%H:%M}, after you opened this page. "
            f"Only what you changed here was saved, so their changes stay.")
    both = [GROUP_LABELS[g] for g, _, _ in FORM_GROUPS if g in set(mine["groups"]) & {g for e in others for g in e["groups"]}]
    if both:
        note += f" You both changed {' and '.join(both)}: yours is the one saved now."
    return note


async def _edit_page(request: Request, ctx: Ctx, p: dict, status_code: int = 200, draft: dict | None = None, **kw):
    last = (p.get("edits") or [None])[-1]           # the last save, when it was another grown-up's this week
    if not last or last["by"] == ctx.account["_id"] or last["at"] < datetime.datetime.utcnow() - datetime.timedelta(days=7):
        last = None
    started = await _started_today(p)
    return page(request, "child_form.html", ctx, plan=plan_of(ctx.family), pupil=p, years=YEARS, acts=_acts(p),
                started=started, today_items=todays_plan(p, ctx.family), limited=not ctx.full,
                earned=await _earned_today(p, ctx.family) if started else "",
                reward_gap=reward_gap(ctx.family, [{**o, **p} if o["_id"] == p["_id"] else o for o in await _pupils(ctx)]),
                loaded=datetime.datetime.utcnow().isoformat(), status_code=status_code, focus_off=_focus_off(p, ctx.family),
                last_edit={"who": last["who"], "when": local_time(last["at"]).strftime("%d %b at %H:%M"),
                           "what": [GROUP_LABELS.get(g, g) for g in last["groups"]]} if last else None,
                **_school_week_view(p, ctx.family, draft), **kw)


async def _earned_today(p: dict, family: dict) -> str:
    """The reward this child has already earned today ("30 min Roblox"), or "": a change to today's plan is then
    not needed for it (an earned reward stays earned), and the form says so before the parent picks today or not."""
    b = (await progress.board(family, [p]))[0]
    return b["reward"].get("text", "") if b["reward_earned"] else ""


@router.get("/children/{pid}/edit")
async def child_edit_form(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    p = await own_pupil(ctx, pid)
    what, _, years = request.query_params.get("lost", "").partition("|")
    old, _, new = years.partition("|")
    return await _edit_page(request, ctx, p, save_note=_save_note(p, ctx, request.query_params.get("loaded"))
                            if request.query_params.get("saved") else "",
                            lost_focus={"what": what[:200], "old": old[:1], "new": new[:1]} if what and new else None,
                            easy=bool(request.query_params.get("easy")))


def _merge_acts(p: dict, form, year: int, changed: set | None) -> dict:
    """The plan with only the activities edited on this form taken from it; the others stay as saved now."""
    acts, sent = {k: dict(v) for k, v in _acts(p).items()}, _form_activities(form, year)
    for k in ORDER:
        if changed is None or {f"on_{k}", f"target_{k}", f"check_{k}"} & changed or (k == "tables" and "check_slow" in changed):
            acts[k] = sent[k]
        if year < ACTIVITIES[k]["min_year"]:
            acts[k]["on"] = False
    return acts


@router.post("/children/{pid}/edit")
async def child_edit(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    """Save a child's settings. Two grown-ups may have the page open at once: only what was edited on this form
    changes, so one parent's save never puts back what the other changed. Without the form's script nothing can tell
    what was edited, so a form opened before someone else's save is refused instead. A carer may change only the
    school's spelling list and the days off."""
    p = await own_pupil(ctx, pid)
    form = await request.form()
    changed = _changed_fields(form)
    groups = _groups(changed)
    if form.get("plan_today"):        # "Change today's plan too" applies the saved plan and practice days to today
        groups |= {"plan", "pdays"}
    groups &= CARER_GROUPS if not ctx.full else _groups(None)
    others = _edits_since(p, ctx, form.get("loaded"))
    if changed is None and others:
        o = others[-1]
        return await _edit_page(request, ctx, p, status_code=409,
                                error=f"{o['who']} changed {p['name']}'s settings at {local_time(o['at']):%H:%M}, after "
                                      f"you opened this page. Here they are now: make your change again and save.")
    name = (form.get("name") or p["name"]).strip()[:30]
    # the school year, and per subject the level its questions come from ("working at": "" is the school year)
    year, lvs = p["year"], {s: levels.level(p, s) for s in levels.SUBJECTS}
    if "year" in groups:
        try:
            year = int(form.get("year") or p["year"])
        except ValueError:
            pass
        year = year if year in YEARS else p["year"]
        for s in levels.SUBJECTS:
            if f"level_{s}" in form:
                v = form.get(f"level_{s}") or ""
                lvs[s] = int(v) if v.isdigit() and int(v) in YEARS else year
    new_levels = levels.clean(lvs, year)
    moved = {**p, "year": year, "levels": new_levels}       # the child as saved: the focus follows each subject's level
    school, err = _form_school_words(form, p) if "school" in groups else ({}, "")
    rest, err = (await _form_rest(form, p, weekdays="pdays" in groups)) if not err else ({}, err)
    upd = {**school, **rest}
    gone = upd.pop("_withdraw", None)          # school words taken back (a typing slip fixed): see spelling.withdraw
    if "name" in groups:
        upd["name"] = name or p["name"]
    if "year" in groups and year != p["year"]:
        upd["year"] = year
    if "year" in groups and new_levels != (p.get("levels") or None):
        upd["levels"] = new_levels
    if "year" in groups and form.get("level_form") and bool(form.get("level_report")) != (p.get("levels_on_report") is not False):
        upd["levels_on_report"] = bool(form.get("level_report"))      # "Show these levels on the printed report"
    relevel = any(levels.level(moved, s) != levels.level(p, s) for s in levels.SUBJECTS)
    if "reward" in groups:
        upd["reward"] = _form_reward(form, ctx.family)
    if "plan" in groups or year != p["year"]:
        upd.update(await _new_plan(p, _merge_acts(p, form, year, changed), bool(form.get("plan_today"))))
    if "focus" in groups or relevel:
        upd.update(_form_focus(form, p, ctx.family, moved))
    lost = upd.pop("_focus_lost", None)       # topics of the old year with nothing like them in the new one
    if "focus" in upd and p.get("sats"):
        upd["sats"] = None                     # topics changed by hand are the parent's own: Revise for SATs is off
    reading = dict(p.get("reading") or {})
    if form.get("reading_form") and "reading" in groups:   # "Reading" (child_form.html): the child's "Aa" settings, on every device
        reading.update({k: bool(form.get(f"read_{k}")) for k in ("big", "dys", "space", "contrast")})
        upd["reading"] = {k: reading.get(k) is True for k in ("big", "dys", "space", "calm", "contrast")}
    if form.get("calm_form") and "calm" in groups:          # "Calm screen and read-aloud": the grown-up's, the child can't undo it
        upd.update(_form_calm(form))
        if reading.get("calm"):           # the child's own "Calm screen" (Aa) goes with the grown-up's choice
            upd["reading"] = {k: reading.get(k) is True for k in ("big", "dys", "space", "contrast")} | {"calm": False}
    pin = (form.get("pin") or "").strip() if "pin" in groups else ""
    if pin and not err:
        if not PIN_RE.match(pin):
            err = "The PIN is 4 numbers, like 4739."
        elif (taken := await _pin_taken(ctx, pin, but=p["_id"])):
            err = f"{taken} already uses this PIN. Pick a different one."
    if err:
        # nothing is saved, and every field comes back as it was typed (a tick, a target, the topics), still
        # counted as edited (dirty), so the next Save saves it
        shown = {**p, **{k: v for k, v in upd.items() if k in ("name", "year", "levels", "levels_on_report", "reward", "activities",
                                                                "plan_log", "focus", "reading", "calm", "voice")}}
        if "pdays_form" in form and "pdays" in groups:
            shown["practice_days"] = sorted({int(d) for d in form.getlist("pday") if str(d).isdigit()})
        return await _edit_page(request, ctx, shown, status_code=400, error=err,
                                draft={**{k: form.get(k) or "" for k in ("school_words", "off_from", "off_to")},
                                       "school_fix": spelling.school_fixes(form), "plan_today": bool(form.get("plan_today"))},
                                dirty=sorted(changed or []), pin_typed=(form.get("pin") or "").strip()[:4])
    today = progress.today()
    if form.get("plan_today") and "plan_log" in upd and ((p.get("kept") or {}).get(today) or {}).get("pct"):
        # "Change today's plan too" reopens a finished day when today's plan grew: the child sees what is left
        # (a reward already earned stays earned, see progress.board)
        if [(a["key"], a["target"]) for a in todays_plan({**p, **upd}, ctx.family)] != \
                [(a["key"], a["target"]) for a in todays_plan(p, ctx.family)]:
            upd[f"kept.{today}.pct"] = 0
    if pin:
        # pin_view: shown to the parent (a minder must be able to find it); a 4-digit hash would not protect it anyway.
        upd["pin"], upd["pin_view"] = hash_secret(pin), pin
    done = sorted({g for k, g in SAVED_AS.items() if k in upd and upd[k] != p.get(k)} | ({"plan"} if "plan_log" in upd else set()))
    who = adult_name(ctx.account)
    lines = _changes(p, upd, ctx.family)
    if "plan_log" in upd and upd["plan_log"][-1]["from"] == today:
        # today's plan changed: the child's My day says so in one line ("Dad added Science today")
        now = _plan_changes(p, upd["activities"], today)
        if now:
            upd["plan_note"] = {"day": today, "text": f"{who} changed today's plan: {now[0].rsplit(', from today', 1)[0]}."}
    if done:
        upd["edits"] = (p.get("edits") or [])[-4:] + [{"at": datetime.datetime.utcnow(), "by": ctx.account["_id"],
                                                       "who": who, "groups": done}]
    if upd:
        await db.pupils.update_one({"_id": p["_id"]}, {"$set": upd})
    if gone:
        await spelling.withdraw(await db.pupils.find_one({"_id": p["_id"]}), gone)
    for line in lines:
        await _log_change(ctx, p, f"{who} {line}")
    if pin:
        await clear_pin_lock(p["_id"])           # a new PIN also lifts a lock from wrong guesses
        await log_event(ctx.family["_id"], "pin", f"{who} changed {p['name']}'s PIN", pupil_id=p["_id"])
    loaded = form.get("loaded") or ""
    return RedirectResponse(f"/children/{p['_id']}/edit?saved=1{'&pin=1' if pin else ''}"
                            f"{'&easy=1' if pin and easy_pin(pin) else ''}"
                            f"{'&lost=' + quote(lost) if lost else ''}"
                            f"{'&loaded=' + loaded if others and loaded else ''}"
                            f"{'&earned=1' if 'plan_log' in upd and (await _earned_today(p, ctx.family)) else ''}", 303)


async def _started_today(p: dict) -> bool:
    return bool(await db.attempts.find_one({"pupil_id": p["_id"], "day": progress.today()}, {"_id": 1}))


async def _new_plan(p: dict, acts: dict, today_too: bool) -> dict:
    """The update for a changed plan. Once the child has started today, it starts tomorrow: today keeps the plan
    it started with, and history keeps each day's own plan (plan_log). Before the child starts, or when the
    parent asks, it starts today; a reward already earned today is kept anyway (progress.day_status)."""
    if acts == _acts(p) and not today_too:
        return {}
    start = progress.today() if today_too or not await _started_today(p) else _tomorrow()
    log = p.get("plan_log") or [{"from": "", "acts": _acts(p)}]
    log = [e for e in log if e["from"] < start]
    cutoff = progress.day_list(15)[0]               # older entries matter only for the last that started before
    keep = [e for e in log if e["from"] >= cutoff]
    log = ([e for e in log if e["from"] < cutoff][-1:] + keep)[-20:] + [{"from": start, "acts": acts}]
    return {"activities": acts, "plan_log": log}


# ---- the school's week: its spelling list, the topic the class is on, and rest days ----

def _plus_days(n: int) -> str:
    return (datetime.date.fromisoformat(progress.today()) + datetime.timedelta(days=n)).isoformat()


def _focus_options(p: dict, family: dict) -> dict:
    """The strands a parent can pick, each subject's from the year it works at (levels.level):
    {"maths": [strand, ...], "grammar": [...], ...}."""
    allowed, out = plan_of(family)["activities"], {}
    if "maths" in allowed:
        out["maths"] = list(dict.fromkeys(s["strand"] for s in maths_mastery._year_skills(maths.engine_year(levels.level(p, "maths")))))
    for subj in ("grammar", "science"):
        if subj in allowed and p["year"] >= ACTIVITIES[subj]["min_year"]:
            out[subj] = bank_engine.focus_strands(subj, levels.level(p, subj))     # + "Apostrophes", earlier KS3 topics
    return out


def _focus_groups(opts: dict) -> list:
    """The focus menu, in groups: [(label, subject, [strand, ...])]; science by Biology, Chemistry and Physics."""
    out = [("Maths", "maths", opts.get("maths", [])), ("Grammar and punctuation", "grammar", opts.get("grammar", []))]
    sci = opts.get("science", [])
    for area in SCIENCE_AREAS:
        out.append((f"Science: {area}" if area != "Working scientifically" else "Science: working scientifically",
                    "science", [x for x in sci if SCIENCE_AREA.get(x) == area]))
    out.append(("Science", "science", [x for x in sci if x not in SCIENCE_AREA]))     # a strand not mapped yet
    return [g for g in out if g[2]]


def _form_focus(form, p: dict, family: dict, new: dict | None = None) -> dict:
    """The update for "Working on this at school": up to FOCUS_MAX strands of any subjects, each for its own 1 or
    2 weeks. A strand picked again keeps its first day (a new number of weeks counts from it); a new pick runs from
    today; "Nothing" in every row ends the focus. new: the child after a change of school year or of a subject's
    level ("working at"), when there is one."""
    new = new or p
    moved = {s for s in ("maths", "grammar", "science") if levels.level(new, s) != levels.level(p, s)}
    if "focus_0" not in form and not moved:
        return {}
    cur = focus_items(p)
    if moved:
        # another year for a subject: each of its topics goes across to the same topic of that year, if it has one;
        # the others stop, and the parent is told which (_focus_lost: "Maths: Equations … was for Year 8")
        new_opts, keep, lost = _focus_options(new, family), [], []
        for i in cur:
            same = i["strand"] if i["subject"] not in moved else \
                next((s for s in new_opts.get(i["subject"], []) if strand_label(s) == strand_label(i["strand"])), None)
            if same:
                keep.append({**i, "strand": same})
            else:
                lost.append(i)
        out = {"focus": keep or None} if p.get("focus") and keep != cur else {}
        if lost:
            s = lost[0]["subject"]
            out["_focus_lost"] = (f"{' and '.join(focus_title(i['subject'], i['strand']) for i in lost)}"
                                  f"|{levels.level(p, s)}|{levels.level(new, s)}")
        return out
    opts, was = _focus_options(p, family), {(i["subject"], i["strand"]): i for i in cur}
    new = []
    for n in range(FOCUS_MAX):
        subj, _, strand = (form.get(f"focus_{n}") or "").partition(":")
        if not strand or strand not in opts.get(subj, []) or any(i["subject"] == subj and i["strand"] == strand for i in new):
            continue
        try:
            weeks = int(form.get(f"focus_weeks_{n}") or 1)
        except ValueError:
            weeks = 1
        weeks = weeks if weeks in FOCUS_WEEKS else 1
        start = was[(subj, strand)]["from"] if (subj, strand) in was else progress.today()
        until = (datetime.date.fromisoformat(start) + datetime.timedelta(weeks=weeks)).isoformat()
        if until <= progress.today():             # picked again after its weeks are over: a new run from today
            start, until = progress.today(), _plus_days(7 * weeks)
        new.append({"subject": subj, "strand": strand, "weeks": weeks, "from": start, "until": until})
    if new == cur and isinstance(p.get("focus"), list):
        return {}
    return {"focus": new or None} if (new or p.get("focus")) else {}


@router.post("/children/{pid}/school-words/remove")
async def school_word_remove(pid: str, ctx: Ctx = Depends(parent_page), word: str = Form("")):
    """✕ next to an earlier school word still tricky: take it out everywhere (spelling.withdraw), e.g. a typing
    slip the parent made last week, or a word that wasn't on the school's list. A carer may too (the list is theirs)."""
    p = await own_pupil(ctx, pid)
    w = next((x for x in spelling.carried_words(p) if x.lower() == word.strip().lower()), None)
    if w:
        await spelling.withdraw(p, {w: ""})
        await log_event(ctx.family["_id"], "school", f"{adult_name(ctx.account)} took “{w}” out of {p['name']}'s "
                        "school spelling words", pupil_id=p["_id"])
    return RedirectResponse(f"/children/{p['_id']}{'?removed=' + quote(w) if w else ''}#school-words", 303)


def _form_school_words(form, p: dict) -> tuple[dict, str]:
    """The update for the school's spelling list, and an error to show. A new list runs for SCHOOL_DAYS from today;
    the same list saved again keeps its dates; an emptied box ends it."""
    if "school_words" not in form:
        return {}, ""
    words, err = spelling.parse_school_words(form.get("school_words") or "")
    if err:
        return {}, err
    # "frend: did you mean friend?": the parent's choice for each word we did not know (fix it, or keep it)
    words, fixed, kept = spelling.apply_fixes(words, spelling.school_fixes(form))
    sl = p.get("school_words") or {}
    if words == spelling.school_words(p) and not kept - set(sl.get("kept") or []):
        return {}, ""
    if not words:
        return ({"school_words": None} if p.get("school_words") else {}), ""
    doubt = "" if form.get("school_ok") else spelling.school_doubts(form.get("school_words") or "")
    if doubt or spelling.school_unknown(words, kept | set(sl.get("kept") or [])):
        # a sentence typed without its dash, or a word we don't know: asked under the box, before saving
        return {}, "Nothing is saved yet: check the spelling list below."
    gone = spelling.withdrawn(p, words, fixed)
    if words == spelling.school_words(p):         # only words kept as they are: the list keeps its dates
        return {"school_words.kept": sorted(kept | set(sl.get("kept") or []))}, ""
    new = spelling.new_school_list(p, words, progress.today(), _plus_days(spelling.SCHOOL_DAYS), gone, kept)
    if gone and spelling.same_list(p, words):
        new["from"], new["until"] = sl["from"], sl["until"]        # the same week's list, corrected: same dates
    return {"school_words": new, **({"_withdraw": gone} if gone else {})}, ""


async def _form_rest(form, p: dict, weekdays: bool = True) -> tuple[dict, str]:
    """The update for practice days and days off, and an error to show. A change of weekdays follows the plan's
    rule (from tomorrow once the child has started today); a day off applies at once, today included. Days off
    are changes (one added, those ticked removed), so they never undo another grown-up's; weekdays=False leaves
    the weekdays alone (a carer, or a form where they were not edited)."""
    if "pdays_form" not in form and "off_form" not in form:
        return {}, ""
    upd = {}
    weekdays = weekdays and "pdays_form" in form
    days = sorted({int(d) for d in form.getlist("pday") if str(d).isdigit() and int(d) in ALL_WEEK})
    if weekdays and not days:
        return {}, "Tick at least one practice day. For a break, add days off instead."
    cur = p.get("practice_days")
    start = progress.today() if form.get("plan_today") or not await _started_today(p) else _tomorrow()
    if weekdays and (days != (ALL_WEEK if cur is None else sorted(cur)) or days != sorted(practice_days_on(p, start))):
        log = [e for e in p.get("days_log") or [{"from": "", "days": ALL_WEEK if cur is None else cur}] if e["from"] < start]
        cutoff = progress.day_list(15)[0]
        log = ([e for e in log if e["from"] < cutoff][-1:] + [e for e in log if e["from"] >= cutoff])[-20:]
        upd.update({"practice_days": days, "days_log": log + [{"from": start, "days": days}]})
    today = progress.today()
    gone = set(form.getlist("off_remove"))
    # past days off are kept for a term, as the printed report lists them
    offs = [o for o in p.get("days_off") or []
            if o["to"] >= progress.day_list(130)[0] and not (o["to"] >= today and f"{o['from']}|{o['to']}" in gone)]
    first, last = (form.get("off_from") or "").strip(), (form.get("off_to") or "").strip()
    if first or last:
        try:
            d1 = datetime.date.fromisoformat(first or last)
            d2 = datetime.date.fromisoformat(last) if last else d1
        except ValueError:
            return {}, "Pick the day off from the calendar."
        if d1.isoformat() < today:
            return {}, "A day off can start today or later."
        if d2 < d1:
            return {}, "The last day off is before the first one. Swap them round."
        if (d2 - d1).days + 1 > MAX_DAYS_OFF:
            return {}, f"Days off can cover up to {MAX_DAYS_OFF // 7} weeks at a time. Add the rest as another break."
        if d1.isoformat() > _plus_days(366):
            return {}, "Pick a day within the next year."
        offs.append({"from": d1.isoformat(), "to": d2.isoformat()})
    offs = sorted({(o["from"], o["to"]) for o in offs})[-20:]
    offs = [{"from": a, "to": b} for a, b in offs]
    if offs != (p.get("days_off") or []):
        upd["days_off"] = offs
    return upd, ""


def _school_week_view(p: dict, family: dict, draft: dict | None = None) -> dict:
    """What the child form shows for the school list, the focus and rest days (draft: what the parent typed,
    shown again with an error)."""
    today = progress.today()
    sl = spelling.school_words(p)
    return {"school_text": (draft or {}).get("school_words", spelling.school_text(sl)),
            "school_until": p["school_words"]["until"] if sl else "", "school_max": spelling.SCHOOL_MAX,
            "school_sum": spelling.school_summary(sl, p["name"]) if sl and not draft else None,
            "school_doubt": spelling.school_doubts((draft or {}).get("school_words") or ""),
            "school_unknown": spelling.school_questions(p, draft["school_words"], draft.get("school_fix"))
                              if draft and "school_words" in draft else spelling.school_questions(p),
            "school_keep": spelling.KEEP,
            "focus_groups": _focus_groups(_focus_options(p, family)), "focus_now": focus_items(p),
            "focus_max": FOCUS_MAX, "focus_title": focus_title,
            "pdays": ALL_WEEK if p.get("practice_days") is None else p["practice_days"], "WEEKDAYS": WEEKDAYS,
            "days_off": [o for o in p.get("days_off") or [] if o["to"] >= today], "today_iso": today,
            "max_off": _plus_days(366), "draft": draft or {},
            "strand_label": lambda s, _n=bank_engine.earlier_note("science", levels.level(p, "science")): strand_label(s) + _n.get(s, "")}


async def _delete_pupils(ids: list) -> None:
    await funnel.keep(ids)              # the family's funnel dates outlive the child's answers (app/funnel.py)
    for c in ("maths_lab_q", "maths_attempts", "maths_mastery"):
        await db[c].delete_many({"pupil": {"$in": ids}})
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items",
              "reports"):
        await db[c].delete_many({"pupil_id": {"$in": ids}})
    # A device that child was using goes back to "Who's learning?", still locked: never to parent mode.
    await db.sessions.update_many({"child_id": {"$in": ids}}, {"$set": {"child_id": None, "locked": True}})
    await db.pupils.delete_many({"_id": {"$in": ids}})
    if ids:
        await db.deletions.insert_many([{"kind": "pupil", "ref": i, "at": datetime.datetime.utcnow()} for i in ids])


@router.get("/children/{pid}/delete")
async def child_delete_form(request: Request, pid: str, ctx: Ctx = Depends(full_page)):
    """Deleting a child is its own page, asking for the password: never one tap next to Save."""
    p = await own_pupil(ctx, pid)
    return page(request, "child_delete.html", ctx, pupil=p, answers=await db.attempts.count_documents({"pupil_id": p["_id"]}),
                others=await db.accounts.count_documents({"family_id": ctx.family["_id"], "_id": {"$ne": ctx.account["_id"]},
                                                          "role": {"$in": ["owner", "parent"]}}))


@router.post("/children/{pid}/delete")
async def child_delete(request: Request, pid: str, ctx: Ctx = Depends(full_page), password: str = Form("")):
    """Any parent may delete a child (a carer may not), with their own password. The other parents are told."""
    p = await own_pupil(ctx, pid)
    key, err = f"delete:{ctx.account['_id']}", ""
    if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
        err = f"Too many wrong passwords. Try again in {UNLOCK_MINUTES} minutes."
    elif not verify_secret(password, ctx.account["pw"]):
        await hit(key)
        err = "That password is not right. Type your own password to delete." if password else "Type your password to delete."
    if err:
        return page(request, "child_delete.html", ctx, pupil=p, status_code=400, error=err,
                    answers=await db.attempts.count_documents({"pupil_id": p["_id"]}))
    await _delete_pupils([p["_id"]])
    who, fam = adult_name(ctx.account), ctx.family["name"]
    await log_event(ctx.family["_id"], "child", f"{who} deleted {p['name']}'s profile and practice")
    await mailer.to_family(ctx.family["_id"], f"{who} deleted {p['name']}'s profile on Quizocracy",
                           f"Hello,\n\n{who} ({ctx.account['email']}) deleted {p['name']}'s profile on {fam} on "
                           f"{local_time(datetime.datetime.utcnow()):%d %B %Y at %H:%M}. All of {p['name']}'s practice "
                           f"was deleted too. It cannot be undone.\n\nDidn't expect this? Talk to {who}. If you think "
                           f"someone else knows their password, write to us at {config.SUPPORT_EMAIL}.\n",
                           skip=(ctx.account["_id"],))
    return RedirectResponse(f"/home?deleted=1&deleted_name={p['name']}", 303)


@router.get("/settings")
async def settings_form(request: Request, ctx: Ctx = Depends(parent_page)):
    return page(request, "settings.html", ctx, plan=plan_of(ctx.family), saved=request.query_params.get("saved"),
                **await settings_view(ctx))


@router.post("/settings")
async def settings(request: Request, ctx: Ctx = Depends(full_page), family_name: str = Form(""),
                   reward_text: str = Form(""), reward_threshold: int = Form(100)):
    upd = {"name": (family_name.strip() or ctx.family["name"])[:60]}
    if plan_of(ctx.family)["rewards"]:
        upd["reward"] = {"text": reward_text.strip()[:120], "threshold": max(10, min(100, reward_threshold))}
    await db.families.update_one({"_id": ctx.family["_id"]}, {"$set": upd})
    if "reward" in upd and upd["reward"] != {k: (ctx.family.get("reward") or {}).get(k) for k in ("text", "threshold")}:
        r = upd["reward"]
        await log_event(ctx.family["_id"], "plan", f"{adult_name(ctx.account)} set the family reward: "
                        + (f"“{r['text']}” at {r['threshold']}% of the day" if r["text"] else "none"))
    return RedirectResponse("/settings?saved=1", 303)


@router.get("/account/export")
async def export(request: Request, ctx: Ctx = Depends(full_page)):
    fid = ctx.family["_id"]
    pupils = await _pupils(ctx)
    ids = [p["_id"] for p in pupils]
    accounts = [{k: v for k, v in a.items() if k != "pw"} async for a in db.accounts.find({"family_id": fid})]
    data = {"exported": datetime.datetime.utcnow(), "times": "UTC", "family": ctx.family, "accounts": accounts,
            "children": [{k: v for k, v in p.items() if k not in ("pin", "pin_view")} for p in pupils],
            "devices": [{k: s.get(k) for k in ("created", "expires", "child_id")}
                        async for s in db.sessions.find({"family_id": fid})]}
    # Every per-child collection that deleting a child removes (see _delete_pupils), so the file is complete.
    for c in ("attempts", "tables_facts", "spelling_words", "verbs_state", "bank_mastery", "bank_state", "items",
              "reports"):
        data[c] = [d async for d in db[c].find({"pupil_id": {"$in": ids}}, {"_id": 0})]
    for c in ("maths_attempts", "maths_mastery", "maths_lab_q"):
        data[c] = [d async for d in db[c].find({"pupil": {"$in": ids}}, {"_id": 0})]
    data["family_log"] = [d async for d in db.family_log.find({"family_id": fid}, {"_id": 0})]
    data["feedback"] = [d async for d in db.feedback.find({"family_id": fid}, {"_id": 0, "team_msg": 0})]
    data["emails"] = [d async for d in db.outbox.find({"to": {"$in": [a["email"] for a in accounts]}},
                                                      {"_id": 0, "to": 1, "subject": 1, "created": 1})]
    body = json.dumps(data, default=_json_default, indent=1)
    return Response(body, media_type="application/json",
                    headers={"Content-Disposition": 'attachment; filename="quizocracy-export.json"',
                             "Cache-Control": "no-store"})


def _json_default(o):
    return o.isoformat() + "Z" if isinstance(o, datetime.datetime) else str(o)


@router.post("/account/delete")
async def delete_account(request: Request, ctx: Ctx = Depends(full_page), password: str = Form(...),
                         confirm: str = Form("")):
    """Only the account owner deletes the family (a second parent in another home must never be able to wipe the
    children's record and the owner's login); every grown-up is told by email. Another grown-up may leave."""
    if ctx.role != "owner":
        return RedirectResponse("/settings#delete", 303)
    if confirm.strip().upper() != "DELETE" or not verify_secret(password, ctx.account["pw"]):
        return page(request, "settings.html", ctx, plan=plan_of(ctx.family), status_code=400,
                    delete_error="Type DELETE and your password to delete the account.", **await settings_view(ctx))
    fid = ctx.family["_id"]
    adults = [a async for a in db.accounts.find({"family_id": fid, "verified_at": {"$ne": None}})]
    kids = [p["name"] async for p in db.pupils.find({"family_id": fid}, {"name": 1})]
    await _delete_pupils([p["_id"] async for p in db.pupils.find({"family_id": fid}, {"_id": 1})])
    # every adult's address, and the ones they changed from, so the mail log about them goes too
    emails = [e async for a in db.accounts.find({"family_id": fid}) for e in [a["email"], *a.get("past_emails", [])]]
    # the team board's copy of the family's "How is it going?" answers goes too
    await drop_family_feedback([d["team_msg"] async for d in db.feedback.find(
        {"family_id": fid, "team_msg": {"$exists": True}}, {"team_msg": 1})])
    for c in FAMILY_COLLECTIONS:
        await db[c].delete_many({"family_id": fid})
    await db.codes.delete_many({"family_id": fid})             # invitations still open
    await db.weekly_sends.delete_many({"family_id": fid})
    await db.codes.delete_many({"email": {"$in": emails}})
    await db.outbox.delete_many({"to": {"$in": emails}})
    await db.families.delete_one({"_id": fid})
    await db.deletions.insert_one({"kind": "family", "ref": fid, "at": datetime.datetime.utcnow()})
    # after the mail log is cleared, so this last message is the one left (every grown-up, the owner too)
    who, when = adult_name(ctx.account), local_time(datetime.datetime.utcnow())
    for a in adults:
        await mailer.send(a["email"], f"{ctx.family['name']} was deleted from Quizocracy",
                          f"Hello,\n\n{who} ({ctx.account['email']}), the account owner, deleted the family "
                          f"“{ctx.family['name']}” on Quizocracy on {when:%d %B %Y at %H:%M}. "
                          f"{'The children (' + ', '.join(kids) + ') and all their practice were' if kids else 'Everything was'} "
                          f"deleted, and every grown-up's login there stopped working. It cannot be undone.\n\n"
                          f"Didn't expect this? Talk to {who}. If you think someone else knows their password, "
                          f"write to us at {config.SUPPORT_EMAIL}.\n")
    resp = RedirectResponse("/?deleted=1", 303)
    resp.delete_cookie("qz_s", path="/")
    return resp


@router.post("/account/leave")
async def leave_family(request: Request, ctx: Ctx = Depends(parent_page), password: str = Form(""),
                       confirm: str = Form("")):
    """A grown-up who is not the owner leaves the family: only their own login goes; the children, their
    practice and the other grown-ups stay. The parents are told."""
    if ctx.role == "owner":
        return RedirectResponse("/settings#delete", 303)
    if confirm.strip().upper() != "LEAVE" or not verify_secret(password, ctx.account["pw"]):
        return page(request, "settings.html", ctx, plan=plan_of(ctx.family), status_code=400,
                    leave_error="Type LEAVE and your password to leave the family.", **await settings_view(ctx))
    who, fam = adult_name(ctx.account), ctx.family["name"]
    await db.accounts.delete_one({"_id": ctx.account["_id"]})
    await db.sessions.delete_many({"account_id": ctx.account["_id"]})
    await db.codes.delete_many({"account_id": ctx.account["_id"]})
    await log_event(ctx.family["_id"], "adult", f"{who} left the family")
    await mailer.to_family(ctx.family["_id"], f"{who} left {fam} on Quizocracy",
                           f"Hello,\n\n{who} ({ctx.account['email']}) left {fam} on Quizocracy. Their login no longer "
                           f"works. The children and their practice are as they were.\n\nTo have them back, invite "
                           f"them again in Settings.\n")
    resp = RedirectResponse("/?left=1", 303)
    resp.delete_cookie("qz_s", path="/")
    return resp


@router.post("/handover")
async def handover(request: Request, ctx: Ctx = Depends(family_page)):
    """Lock the device before it changes hands: from here only a child's PIN or the parent's password works."""
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"locked": True}})
    return RedirectResponse("/learn", 303)


@router.post("/children/{pid}/start")
async def start_now(request: Request, pid: str, ctx: Ctx = Depends(parent_page)):
    """"Start now with Maya" (just after adding a child): the grown-up is here, so the child's day opens on this
    device without the picker and the PIN. The parent area locks as on a hand-over: the password brings it back."""
    p = await own_pupil(ctx, pid)
    await db.sessions.update_one({"_id": ctx.session["_id"]},
                                 {"$set": {"child_id": p["_id"], "locked": True, "handed": True},
                                  "$unset": {"pin_show": ""}})
    return RedirectResponse("/me", 303)


@router.get("/parent-unlock")
async def unlock_form(request: Request, ctx: Ctx = Depends(family_page)):
    if not ctx.locked:
        return RedirectResponse("/home", 303)
    return page(request, "unlock.html", ctx)


UNLOCK_FAILS, UNLOCK_MINUTES = 8, 15
PIN_SHOW = datetime.timedelta(minutes=3)        # "Show Isaac's PIN" on the picker, after a grown-up's unlock


@router.post("/parent-unlock")
async def unlock(request: Request, ctx: Ctx = Depends(family_page), password: str = Form(...)):
    key = f"unlock:{ctx.family['_id']}"          # per family, so every device of the family shares the count
    if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
        return page(request, "unlock.html", ctx, status_code=429,
                    error=f"Too many wrong passwords. The parent area is locked for {UNLOCK_MINUTES} minutes.")
    adult = await family_adult(ctx, password)
    if not adult:
        await hit(key)
        return page(request, "unlock.html", ctx, error="That password is not right.", status_code=400)
    await db.login_failures.delete_many({"email": key})
    now = datetime.datetime.utcnow()
    # handed: this device has been in a child's hands, so parent mode here locks itself when left idle (deps).
    # Any adult of the family can open it, and the device is then theirs, with their own rights (a carer's or a parent's).
    await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": False,
                                                                        "parent_ok_at": now, "seen_at": now,
                                                                        "handed": True, "timed_out": False,
                                                                        "account_id": adult["_id"]}})
    return RedirectResponse("/home", 303)


@router.post("/children/{pid}/pin-unlock")
async def pin_unlock(request: Request, pid: str, ctx: Ctx = Depends(family_page), password: str = Form(""),
                     back: str = Form("")):
    """Lift a child's lock after wrong PINs: from Home in parent mode, or on "Who's learning?" with the password."""
    p = await own_pupil(ctx, pid)
    adult = ctx.account
    if ctx.locked:
        key = f"unlock:{ctx.family['_id']}"      # the same count as the parent-area password
        err = None
        if await over_limit(key, UNLOCK_FAILS, UNLOCK_MINUTES):
            err = f"Too many wrong passwords. Try again in {UNLOCK_MINUTES} minutes."
        elif not (adult := await family_adult(ctx, password)):
            await hit(key)
            err = "That password is not right. Use your own password (any grown-up on this family)."
        if err:
            return await picker_page(request, ctx, pin_for=p["_id"], unlock_error=err, status_code=400)
        # the child is locked out because the PIN was forgotten: the grown-up who just typed a password may see it
        # on "Who's learning?" for a few minutes (picker_page), without a trip to the parent area
        await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"pin_show": {
            "pid": p["_id"], "until": datetime.datetime.utcnow() + PIN_SHOW}}})
    if await pin_lock_until(p["_id"]):
        await log_event(ctx.family["_id"], "pin_unlock", f"{adult_name(adult)} unlocked {p['name']}", pupil_id=p["_id"])
    await clear_pin_lock(p["_id"])
    return RedirectResponse(f"/{'home' if back == 'home' and not ctx.locked else 'learn'}?unlocked={p['_id']}", 303)


@router.get("/board")
async def board(request: Request, ctx: Ctx = Depends(family_page)):
    if ctx.session.get("child_id"):
        # the Board is the family's, neutral: opening it signs the child out (as Switch does), so a brother or
        # sister who picks the tablet up next needs their own PIN, never carries on in this child's account
        await db.sessions.update_one({"_id": ctx.session["_id"]}, {"$set": {"child_id": None, "locked": True}})
        ctx.child, ctx.locked = None, True
    pupils = await _pupils(ctx)
    return page(request, "board.html", ctx, board=await progress.board(ctx.family, pupils), today=progress.today(),
                today_label=_nice_day(progress.today()), streaks=await progress.streaks(ctx.family, pupils))


def _nice_day(day: str) -> str:
    """"2026-11-10" -> "Tuesday 10 November"."""
    d = datetime.date.fromisoformat(day)
    return f"{d:%A} {d.day} {d:%B}"
