# Year 1 generators (added 2 Nov 2026 to widen the bank).
#
# Measure and begin to record lengths, mass, capacity and time (hours, minutes, seconds); sequence
# events using morning, afternoon and evening.  Short prompts for young readers.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403
from .y1_gen_a import S4, KIDS


@skill("Y1.4.e", "Measure length, mass, capacity and time", S4)
def _(d=1):
    d = _d(d)

    def t_ruler():
        cm = random.randint(2, _by(d, 10, 15, 20))
        what = pick(["crayon", "leaf", "worm", "key"])
        return {"prompt": "How long is the %s, in cm?" % what, "component": "ruler",
                "spec": {"mode": "length", "value": cm, "max": 20, "unit": "cm"}, "answer": cm, "answer_type": "num",
                "tolerance": 0.5, "solution": ["It starts at 0 and ends at %d cm." % cm]}

    def t_scale():
        kg = random.randint(1, 9)
        return {"prompt": "Read the scale. How many kilograms?", "component": "ruler",
                "spec": {"mode": "mass", "value": kg, "max": 10, "unit": "kg"}, "answer": kg, "answer_type": "num",
                "tolerance": 0.5, "solution": ["The pointer is on %d kg." % kg]}

    def t_jug():
        v = random.randint(1, 9) * 100
        return {"prompt": "How much water is in the jug, in ml?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": 1000, "unit": "ml"}, "answer": v, "answer_type": "num",
                "tolerance": 50, "solution": ["The water is level with %d ml." % v]}

    def t_cubes():
        a = random.randint(3, 12)
        what = pick(["pencil", "spoon", "shoe", "book"])
        return _tb("A %s is as long as %d cubes in a row. How many cubes long is it?" % (what, a), a, "int", {},
                   ["Count the cubes: %d." % a])

    def t_balance():
        a = random.randint(2, 9)
        what = pick(["apple", "toy car", "orange", "teddy"])
        return _tb("A %s balances %d cubes on the scales. How many cubes does it weigh?" % (what, a), a, "int", {},
                   ["The scales balance, so it weighs %d cubes." % a])

    def t_cups():
        a, b = random.sample(range(2, 10), 2)
        return _wq("A red jug fills %d cups. A blue jug fills %d cups. Which jug holds more? (red or blue)" % (a, b),
                   "red" if a > b else "blue", ["%d cups is more than %d cups." % (max(a, b), min(a, b))], "red / blue")

    def t_unit_time():
        q, a = pick([("Which takes about one second: a clap or a night's sleep? (clap or sleep)", "clap"),
                     ("Which takes longer: one minute or one hour? (minute or hour)", "hour"),
                     ("Which is shorter: one second or one minute? (second or minute)", "second"),
                     ("Would you measure a football match in seconds or hours?", "hours"),
                     ("Would you time a blink in seconds or hours?", "seconds"),
                     ("Would you time brushing your teeth in minutes or days?", "minutes")])
        return _wq(q, a, ["Seconds are short, minutes are longer, hours are longer still."], "type it")

    def t_race():
        kids = random.sample(KIDS, 3)
        t = random.sample(range(8, 30), 3)
        k = pick(["fastest", "slowest"])
        win = kids[t.index(min(t))] if k == "fastest" else kids[t.index(max(t))]
        return _dt("The table shows race times in seconds. Who was the %s?" % k, ["Name", "Seconds"],
                   [[kids[i], t[i]] for i in range(3)], win,
                   ["Fewer seconds is faster." if k == "fastest" else "More seconds is slower."], atype="str", placeholder="name")

    def t_part_day():
        q, a = pick([("Do you eat breakfast in the morning or the evening?", "morning"),
                     ("Do you go to bed in the morning or the evening?", "evening"),
                     ("Does school finish in the morning or the afternoon?", "afternoon"),
                     ("Is lunch before or after breakfast?", "after"),
                     ("Is the morning before or after the afternoon?", "before")])
        return _wq(q, a, ["Morning comes first, then afternoon, then evening."], "word")

    def t_longer_by():
        a, b = random.sample(range(2, 20), 2)
        return _tb("A blue pencil is %d cm long. A red pencil is %d cm long. How much longer is the longer pencil, in cm?" % (a, b),
                   abs(a - b), "int", {"unit": "cm"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_half_full():
        q, a = pick([("A glass holds 10 sips of juice. It has 5 sips in it. Is it full, half full or empty?", "half full"),
                     ("A glass holds 10 sips of juice. It has 10 sips in it. Is it full, half full or empty?", "full"),
                     ("A glass holds 10 sips of juice. It has no juice in it. Is it full, half full or empty?", "empty")])
        return _wq(q, a, ["Half of 10 is 5."], "full / half full / empty")

    def t_double_length():
        a = random.randint(2, 10)
        return _tb("A snake is %d cm long. Another snake is double that length. How long is it, in cm?" % a, 2 * a, "int",
                   {"unit": "cm"}, ["Double %d is %d." % (a, 2 * a)])

    return _pick_t([t_cubes, t_balance, t_cups, t_unit_time, t_part_day, t_longer_by, t_half_full, t_double_length],
                   [t_ruler, t_scale, t_jug, t_race])
