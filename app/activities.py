"""The activity catalogue, plan limits and each child's daily plan."""
import datetime
import re
from zoneinfo import ZoneInfo

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
    "grammar":  {"title": "Grammar and punctuation", "icon": "✏️", "target": 5, "min_year": 1, "free": False,
                 "blurb": "Word classes, sentences and punctuation, year by year.", "img": "/static/img/grammar.png"},
    "science":  {"title": "Science", "icon": "🔬", "target": 5, "min_year": 1, "free": False,
                 "blurb": "Biology, chemistry and physics from the national curriculum.", "img": "/static/img/science.png"},
}
ORDER = ["maths", "tables", "spelling", "grammar", "science", "numbers", "verbs"]

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


# The default day for each school year: the few activities that matter most at that age, about 15 minutes
# (see minutes()). Anything else the parent can switch on.
YEAR_DEFAULTS = {
    1: {"maths": 8, "spelling": 5},       # 5 right: within reach of a child just learning to sound words out
    2: {"maths": 6, "tables": 10, "spelling": 6},     # Year 2 learns the 2, 5 and 10 tables: 10 right is plenty
    3: {"maths": 8, "tables": 20, "spelling": 8},
    4: {"maths": 8, "tables": 20, "spelling": 8},
    5: {"maths": 10, "tables": 20, "spelling": 8},
    6: {"maths": 10, "spelling": 8, "grammar": 5},
    7: {"maths": 10, "spelling": 8, "grammar": 5, "science": 5},
    8: {"maths": 10, "spelling": 8, "grammar": 5, "science": 5},
    9: {"maths": 10, "spelling": 8, "grammar": 5, "science": 5},
}
# Rough seconds a child needs per correct answer (wrong tries and reading the feedback included), and how much
# longer younger children take. Only used to tell the parent how long a day takes.
SECONDS = {"maths": 50, "tables": 8, "spelling": 25, "grammar": 40, "science": 35, "numbers": 40, "verbs": 20}


def year_pace(year: int) -> float:
    # Years 1-2: a 6- or 7-year-old reads, listens and types slowly (the wave-5 Year 2 day took about twice the
    # Year 5 time per answer)
    return 2.0 if year <= 2 else 1.2 if year <= 4 else 1.0 if year <= 6 else 0.85


CHECK_SECONDS = 240       # a Year 4 check: 25 questions of up to 6 seconds, with a 3-second "Get ready" between
# Years 1-2: an activity also ends after this many times its target in answers, right or wrong (progress.day_status),
# so a child who finds it hard is not kept going for the longest day of all
YOUNG_CAP = 2


def minutes(plan: list, year: int, check: bool = False) -> int:
    """About how long a day of this plan ([{key, target}]) takes, in minutes; check: with a Year 4 check."""
    return round(sum(SECONDS[a["key"]] * a["target"] for a in plan) * year_pace(year) / 60
                 + (CHECK_SECONDS / 60 if check else 0))


def default_activities(year: int) -> dict:
    d = YEAR_DEFAULTS.get(year) or YEAR_DEFAULTS[3]
    return {k: {"on": k in d and year >= a["min_year"], "target": d.get(k, a["target"])} for k, a in ACTIVITIES.items()}


def acts_on(pupil: dict, day: str | None) -> dict | None:
    """The activities the child's plan had on that day. A plan change is logged with the day it starts
    (plan_log, oldest first), so a change made today starts tomorrow and past days keep their own plan."""
    acts = pupil.get("activities")
    if day:
        for e in pupil.get("plan_log") or []:
            if e["from"] <= day:
                acts = e["acts"]
    return acts


def todays_plan(pupil: dict, family: dict, day: str | None = None) -> list:
    """Activities this child should do today (or on that day), respecting the family's plan."""
    allowed = plan_of(family)["activities"]
    defaults = default_activities(pupil.get("year", 3))
    if day is None:
        day = datetime.datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    acts = acts_on(pupil, day) or defaults
    out = []
    for k in ORDER:
        a = acts.get(k) or defaults[k]          # an activity added after the child was set up starts on
        if a.get("on") and k in allowed and pupil.get("year", 1) >= ACTIVITIES[k]["min_year"]:
            out.append({**ACTIVITIES[k], "key": k, "target": max(1, int(a.get("target") or ACTIVITIES[k]["target"]))})
    return out


def local_today() -> str:
    return datetime.datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()


def day_label(day: str) -> str:
    """"2026-11-24" -> "24 Nov" (a parent reads it; the year is always near)."""
    try:
        d = datetime.date.fromisoformat(day)
    except (TypeError, ValueError):
        return day or ""
    return f"{d.day} {d.strftime('%b')}"


# ---- rest days: the weekdays the child practises (logged like the plan, so a change made today starts
# tomorrow once the child has started) and single days off (sick day, holiday), which apply at once ----
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ALL_WEEK = list(range(7))
MAX_DAYS_OFF = 21              # one day off can cover up to three weeks


def practice_days_on(pupil: dict, day: str | None) -> list:
    """The weekdays (0 = Monday) the child practised in the week of that day; every day by default."""
    days = pupil.get("practice_days")
    if day:
        for e in pupil.get("days_log") or []:
            if e["from"] <= day:
                days = e["days"]
    return ALL_WEEK if days is None else list(days)


def day_off(pupil: dict, day: str) -> dict | None:
    return next((o for o in pupil.get("days_off") or [] if o["from"] <= day <= o["to"]), None)


def rest_day(pupil: dict, day: str | None = None) -> str:
    """"off" (a day off the parent marked), "week" (not one of the practice days) or "" (a practice day)."""
    day = day or local_today()
    if day_off(pupil, day):
        return "off"
    if datetime.date.fromisoformat(day).weekday() not in practice_days_on(pupil, day):
        return "week"
    return ""


def next_day(day: str) -> str:
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()


def back_on(pupil: dict, day: str) -> str:
    """The first practice day after `day` (within 6 weeks), or "" if none is in sight."""
    for _ in range(MAX_DAYS_OFF * 2):
        day = next_day(day)
        if not rest_day(pupil, day):
            return day
    return ""


def days_text(days: list) -> str:
    """[0, 1, 2, 3, 4] -> "Mon to Fri"; [5, 6] -> "Sat, Sun"; every day -> "every day"."""
    days = sorted(set(days))
    if days == ALL_WEEK:
        return "every day"
    if not days:
        return "no days"
    if len(days) > 2 and days == list(range(days[0], days[-1] + 1)):
        return f"{WEEKDAYS[days[0]]} to {WEEKDAYS[days[-1]]}"
    return ", ".join(WEEKDAYS[d] for d in days)


# ---- "working on this at school": up to three strands that get most of the questions for a week or two ----
FOCUS_SHARE = 2 / 3            # about two questions in three come from the focus strands of that subject
FOCUS_WEEKS = (1, 2)
FOCUS_MAX = 3
FOCUS_SUBJECTS = ("maths", "grammar", "science")

# The science strands by the school subject a letter home names them by (mapped by hand, after the national
# curriculum: KS3 puts the particle model under chemistry, "Matter" and "Energy" under physics).
SCIENCE_AREAS = {
    "Biology": ["Plants", "Animals, including humans", "Living things and their habitats",
                "Fossils, inheritance and adaptation", "Cells and organisation", "Skeletal and muscular systems",
                "Reproduction", "Nutrition and digestion", "Gas exchange", "Respiration", "Photosynthesis", "Health",
                "Inheritance and variation", "Ecosystems"],
    "Chemistry": ["Everyday materials", "Uses of everyday materials", "Rocks", "States of matter",
                  "Properties and changes of materials", "Particles", "Mixtures and separation", "Acids and alkalis",
                  "Atoms, elements and compounds", "The periodic table", "Atoms and the periodic table",
                  "Chemical reactions", "Materials",
                  "Earth and atmosphere"],
    "Physics": ["Seasonal changes", "Light", "Forces and magnets", "Sound", "Electricity", "Earth and space", "Forces",
                "Space physics", "Magnetism", "Energy", "Motion and forces", "Matter", "Waves"],
    "Working scientifically": ["Working scientifically"],
}
SCIENCE_AREA = {s: area for area, ss in SCIENCE_AREAS.items() for s in ss}


def focus_items(pupil: dict, day: str | None = None) -> list:
    """The focus strands running on that day: [{"subject", "strand", "weeks", "from", "until"}], each running from
    its first day up to, not including, its `until`, and then ending by itself. (A focus saved before there could
    be three was one dict for all subjects, with one pair of dates.)"""
    f = pupil.get("focus") or []
    if isinstance(f, dict):
        f = [{"subject": k, "strand": f[k], "weeks": f.get("weeks", 1), "from": f.get("from", ""),
              "until": f.get("until", "")} for k in FOCUS_SUBJECTS if f.get(k)]
    day = day or local_today()
    return [i for i in f if i.get("from", "") <= day < i.get("until", "")]


def focus_on(pupil: dict, day: str | None = None) -> dict:
    """The focus strands while they run, by subject ({"maths": ["3.6 Fractions"], "science": ["Light"]}), else {}."""
    out: dict = {}
    for i in focus_items(pupil, day):
        out.setdefault(i["subject"], []).append(i["strand"])
    return out


def focus_title(subject: str, strand: str) -> str:
    """What a parent reads for one focus: "Maths: Fractions", "Science (Physics): Light"."""
    area = SCIENCE_AREA.get(strand) if subject == "science" else None
    if area and area != "Working scientifically":
        return f"Science ({area}): {strand}"
    return f"{SUBJECT_NAMES[subject]}: {strand_label(strand)}"


SUBJECT_NAMES = {"maths": "Maths", "grammar": "Grammar", "science": "Science"}


def strand_label(strand: str) -> str:
    """"3.6 Fractions" -> "Fractions" (the maths strands carry their ladder number)."""
    return re.sub(r"^\d+\.\d+\s+", "", strand or "")
