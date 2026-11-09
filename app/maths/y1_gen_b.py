# Year 1 generators (added 2 Nov 2026 to widen the bank).
#
# Measure and begin to record lengths, mass, capacity and time (hours, minutes, seconds); sequence
# events using morning, afternoon and evening.  Short prompts for young readers.
from .maths_engine import skill
from .y5_common import *  # noqa: F401,F403
from .y1_gen_a import S4, KIDS, _pn


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
        top = _by(d, 5, 10, 20)                        # hard: a dial to 20 kg
        kg = random.randint(_by(d, 1, 1, 2), top - 1)
        return {"prompt": "Read the scale. How many kilograms?", "component": "ruler",
                "spec": {"mode": "mass", "value": kg, "max": top, "unit": "kg"}, "answer": kg, "answer_type": "num",
                "tolerance": 0.5, "solution": ["The pointer is on %d kg." % kg]}

    def t_jug():                                        # non-standard units: the jug is marked in cups
        top = _by(d, 5, 10, 20)
        v = 2 * random.randint(1, 9) if d == 2 else random.randint(1, top - 1)     # hard: a 20-cup jug marked in 2s
        return {"prompt": "The jug is marked in cups. How many cups of water are in it?", "component": "ruler",
                "spec": {"mode": "capacity", "value": v, "max": top, "unit": "cups"}, "answer": v, "answer_type": "num",
                "tolerance": 0, "solution": ["The water is level with %s." % _pn(v, "cup")]}

    def t_cubes():
        a = random.randint(_by(d, 3, 3, 10), _by(d, 8, 12, 20))
        what = pick(["pencil", "spoon", "shoe", "book"])
        return _tb("A %s is as long as %d cubes in a row. How many cubes long is it?" % (what, a), a, "int", {},
                   ["Count the cubes: %d." % a])

    def t_balance():
        a = random.randint(2, _by(d, 5, 9, 9))
        what = pick(["apple", "toy car", "orange", "teddy"])
        if d == 2:                                      # hard: two of them balance double
            return _tb("One %s balances %d cubes on the scales. How many cubes balance 2 of them?" % (what, a), 2 * a, "int", {},
                       ["Double %d is %d." % (a, 2 * a)])
        return _tb("A %s balances %d cubes on the scales. How many cubes does it weigh?" % (what, a), a, "int", {},
                   ["The scales balance, so it weighs %d cubes." % a])

    def t_cups():
        if d == 2:                                      # hard: three jugs, most or least
            v = random.sample(range(2, 15), 3)
            jugs = ["red", "blue", "green"]
            most = random.random() < 0.5
            w = max(v) if most else min(v)
            return _wq("A red jug fills %d cups, a blue jug fills %d cups and a green jug fills %d cups. Which jug holds the %s? "
                       "(red, blue or green)" % (v[0], v[1], v[2], "most" if most else "least"), jugs[v.index(w)],
                       ["%d cups is the %s." % (w, "most" if most else "least")], "red / blue / green")
        a, b = random.sample(range(2, _by(d, 7, 10, 10)), 2)
        return _wq("A red jug fills %d cups. A blue jug fills %d cups. Which jug holds more? (red or blue)" % (a, b),
                   "red" if a > b else "blue", ["%d cups is more than %d cups." % (max(a, b), min(a, b))], "red / blue")

    def t_unit_time():
        q, a = pick(_by(d, [("Which takes about one second: a clap or a night's sleep? (clap or sleep)", "clap"),
                            ("Would you time a blink in seconds or hours?", "seconds"),
                            ("Which takes longer: one minute or one hour? (minute or hour)", "hour")],
                        [("Which takes about one second: a clap or a night's sleep? (clap or sleep)", "clap"),
                         ("Which takes longer: one minute or one hour? (minute or hour)", "hour"),
                         ("Which is shorter: one second or one minute? (second or minute)", "second"),
                         ("Would you measure a football match in seconds or hours?", "hours"),
                         ("Would you time a blink in seconds or hours?", "seconds"),
                         ("Would you time brushing your teeth in minutes or days?", "minutes")],
                        [("Which is shorter: one second or one minute? (second or minute)", "second"),
                         ("Would you measure a football match in seconds or hours?", "hours"),
                         ("Would you time brushing your teeth in minutes or days?", "minutes"),
                         ("Would you time a sneeze in seconds or minutes?", "seconds"),
                         ("Would you measure a school day in minutes or hours?", "hours"),
                         ("Which is longer: 10 seconds or 10 minutes? (seconds or minutes)", "minutes")]))
        return _wq(q, a, ["Seconds are short, minutes are longer, hours are longer still."], "type it")

    def t_race():
        m = _by(d, 3, 3, 4)                            # hard: four runners, closer times
        kids = random.sample(KIDS, m)
        t = random.sample(range(_by(d, 8, 8, 20), _by(d, 20, 30, 40)), m)
        k = "fastest" if d == 0 else pick(["fastest", "slowest"])
        win = kids[t.index(min(t))] if k == "fastest" else kids[t.index(max(t))]
        return _dt("The table shows race times in seconds. Who was the %s?" % k, ["Name", "Seconds"],
                   [[kids[i], t[i]] for i in range(m)], win,
                   ["Fewer seconds is faster." if k == "fastest" else "More seconds is slower."], atype="str", placeholder="name")

    def t_part_day():
        q, a = pick(_by(d, [("Do you eat breakfast in the morning or the evening?", "morning"),
                            ("Do you go to bed in the morning or the evening?", "evening")],
                        [("Do you eat breakfast in the morning or the evening?", "morning"),
                         ("Do you go to bed in the morning or the evening?", "evening"),
                         ("Does school finish in the morning or the afternoon?", "afternoon"),
                         ("Is lunch before or after breakfast?", "after"),
                         ("Is the morning before or after the afternoon?", "before")],
                        [("Does school finish in the morning or the afternoon?", "afternoon"),
                         ("Is lunch before or after breakfast?", "after"),
                         ("Is the evening before or after the afternoon?", "after"),
                         ("Which comes just before the evening: the morning or the afternoon?", "afternoon"),
                         ("Is dinner before or after lunch?", "after")]))
        return _wq(q, a, ["Morning comes first, then afternoon, then evening."], "word")

    def t_longer_by():
        a, b = random.sample(range(_by(d, 2, 2, 5), _by(d, 11, 20, 21)), 2)
        if d == 2 and random.random() < 0.5:            # hard: how much shorter
            return _tb("A blue pencil is %d cm long. A red pencil is %d cm long. How much shorter is the shorter pencil, in cm?" % (a, b),
                       abs(a - b), "int", {"unit": "cm"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])
        return _tb("A blue pencil is %d cm long. A red pencil is %d cm long. How much longer is the longer pencil, in cm?" % (a, b),
                   abs(a - b), "int", {"unit": "cm"}, ["%d − %d = %d." % (max(a, b), min(a, b), abs(a - b))])

    def t_half_full():
        c = _by(d, 10, 10, pick([4, 6, 8, 12, 20]))   # hard: half of a different amount
        k = pick(_by(d, [c, 0], [c // 2, c, 0], [c // 2, c // 2, c, 0]))
        a = "full" if k == c else ("empty" if k == 0 else "half full")
        return _wq("A glass holds %d sips of juice. It has %s in it. Is it full, half full or empty?" % (c, "%d sips" % k if k else "no juice"),
                   a, ["Half of %d is %d." % (c, c // 2)], "full / half full / empty")

    def t_double_length():
        a = random.randint(_by(d, 2, 2, 6), _by(d, 5, 10, 10))
        if d == 2 and random.random() < 0.5:            # hard: half the length
            return _tb("A snake is %d cm long. Another snake is half that length. How long is it, in cm?" % (2 * a), a, "int",
                       {"unit": "cm"}, ["Half of %d is %d." % (2 * a, a)])
        return _tb("A snake is %d cm long. Another snake is double that length. How long is it, in cm?" % a, 2 * a, "int",
                   {"unit": "cm"}, ["Double %d is %d." % (a, 2 * a)])

    return _pick_t([t_cubes, t_balance, t_cups, t_unit_time, t_part_day, t_longer_by, t_half_full, t_double_length],
                   [t_ruler, t_scale, t_jug, t_race])
