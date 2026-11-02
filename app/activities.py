"""The activity catalogue, plan limits and each child's daily plan."""
from . import config

ACTIVITIES = {
    "maths":    {"title": "Maths", "icon": "🧮", "target": 10, "min_year": 1, "free": True,
                 "blurb": "Questions from the national curriculum, at your level.", "img": "/static/img/maths.png"},
    "tables":   {"title": "Times tables", "icon": "✖️", "target": 20, "min_year": 2, "free": True,
                 "blurb": "Multiplication and division facts, quick-fire.", "img": "/static/img/tables.png"},
    "spelling": {"title": "Spelling", "icon": "🔤", "target": 10, "min_year": 1, "free": True,
                 "blurb": "Listen to the word, then spell it.", "img": "/static/img/spelling.png"},
    "numbers":  {"title": "Numbers in words", "icon": "🔢", "target": 10, "min_year": 1, "free": False,
                 "blurb": "Write numbers in words, and words in numbers.", "img": "/static/img/numbers.png"},
    "verbs":    {"title": "Irregular verbs", "icon": "📝", "target": 10, "min_year": 3, "free": False,
                 "blurb": "Go, went, gone: the verbs that break the rules.", "img": "/static/img/verbs.png"},
}
ORDER = ["maths", "tables", "spelling", "numbers", "verbs"]

PLANS = {
    "free":   {"title": "Free", "max_children": 1, "activities": [k for k in ORDER if ACTIVITIES[k]["free"]],
               "rewards": False},
    "family": {"title": "Family", "max_children": 6, "activities": list(ORDER), "rewards": True},
}
YEARS = list(range(1, 10))


def plan_of(family: dict) -> dict:
    return PLANS.get((family or {}).get("plan") or "free", PLANS["free"])


def new_family_plan() -> str:
    return "family" if config.BETA_FAMILY_PLAN else "free"


def default_activities(year: int) -> dict:
    return {k: {"on": year >= a["min_year"], "target": a["target"]} for k, a in ACTIVITIES.items()}


def todays_plan(pupil: dict, family: dict) -> list:
    """Activities this child should do today, respecting the family's plan."""
    allowed = plan_of(family)["activities"]
    acts = pupil.get("activities") or default_activities(pupil.get("year", 3))
    out = []
    for k in ORDER:
        a = acts.get(k) or {}
        if a.get("on") and k in allowed and pupil.get("year", 1) >= ACTIVITIES[k]["min_year"]:
            out.append({**ACTIVITIES[k], "key": k, "target": max(1, int(a.get("target") or ACTIVITIES[k]["target"]))})
    return out
