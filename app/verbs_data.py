# dev/app/logic/irregular_verbs_data.py
"""British English irregular verbs, bucketed ~20 per level.

Difficulty RAMPS across levels (common everyday verbs first, rare/literary
last) while each level deliberately MIXES transformation patterns (invariant,
-ought, i-a-u, -en participle, British -t, base=participle, ...) so a pupil
can't guess a level's answers from a single rule. Each verb = (base, [accepted
past forms], [accepted past participle forms]); the first form is canonical.
British spellings are canonical (got, learnt, dreamt...); common alternates
(learned, gotten...) are also accepted.
"""
from typing import List, Dict, Any

_RAW: List[Dict[str, Any]] = [
    {"label": "Level 1 · everyday & short", "verbs": [
        ('break', ['broke'], ['broken']),
        ('build', ['built'], ['built']),
        ('find', ['found'], ['found']),
        ('cut', ['cut'], ['cut']),
        ('begin', ['began'], ['begun']),
        ('do', ['did'], ['done']),
        ('drive', ['drove'], ['driven']),
        ('feel', ['felt'], ['felt']),
        ('have', ['had'], ['had']),
        ('bring', ['brought'], ['brought']),
        ('hang', ['hung'], ['hung']),
        ('let', ['let'], ['let']),
        ('eat', ['ate'], ['eaten']),
        ('get', ['got'], ['got', 'gotten']),
        ('make', ['made'], ['made']),
        ('grow', ['grew'], ['grown']),
        ('hold', ['held'], ['held']),
        ('fall', ['fell'], ['fallen']),
        ('keep', ['kept'], ['kept']),
        ('become', ['became'], ['become']),
    ]},
    {"label": "Level 2 · common mix", "verbs": [
        ('put', ['put'], ['put']),
        ('go', ['went'], ['gone']),
        ('give', ['gave'], ['given']),
        ('leave', ['left'], ['left']),
        ('pay', ['paid'], ['paid']),
        ('know', ['knew'], ['known']),
        ('lose', ['lost'], ['lost']),
        ('see', ['saw'], ['seen']),
        ('read', ['read'], ['read']),
        ('say', ['said'], ['said']),
        ('meet', ['met'], ['met']),
        ('speak', ['spoke'], ['spoken']),
        ('show', ['showed'], ['shown', 'showed']),
        ('buy', ['bought'], ['bought']),
        ('cling', ['clung'], ['clung']),
        ('set', ['set'], ['set']),
        ('ring', ['rang'], ['rung']),
        ('stand', ['stood'], ['stood']),
        ('send', ['sent'], ['sent']),
        ('take', ['took'], ['taken']),
    ]},
    {"label": "Level 3 · building up", "verbs": [
        ('win', ['won'], ['won']),
        ('blow', ['blew'], ['blown']),
        ('sit', ['sat'], ['sat']),
        ('write', ['wrote'], ['written']),
        ('tell', ['told'], ['told']),
        ('cast', ['cast'], ['cast']),
        ('spend', ['spent'], ['spent']),
        ('bite', ['bit'], ['bitten']),
        ('feed', ['fed'], ['fed']),
        ('sing', ['sang'], ['sung']),
        ('draw', ['drew'], ['drawn']),
        ('cost', ['cost'], ['cost']),
        ('bend', ['bent'], ['bent']),
        ('choose', ['chose'], ['chosen']),
        ('lead', ['led'], ['led']),
        ('think', ['thought'], ['thought']),
        ('fling', ['flung'], ['flung']),
        ('burn', ['burnt', 'burned'], ['burnt', 'burned']),
        ('forget', ['forgot'], ['forgotten']),
        ('come', ['came'], ['come']),
    ]},
    {"label": "Level 4 · stretching", "verbs": [
        ('hit', ['hit'], ['hit']),
        ('fly', ['flew'], ['flown']),
        ('deal', ['dealt'], ['dealt']),
        ('forgive', ['forgave'], ['forgiven']),
        ('sell', ['sold'], ['sold']),
        ('swim', ['swam'], ['swum']),
        ('dig', ['dug'], ['dug']),
        ('dream', ['dreamt', 'dreamed'], ['dreamt', 'dreamed']),
        ('freeze', ['froze'], ['frozen']),
        ('hurt', ['hurt'], ['hurt']),
        ('slide', ['slid'], ['slid']),
        ('throw', ['threw'], ['thrown']),
        ('hide', ['hid'], ['hidden']),
        ('learn', ['learnt', 'learned'], ['learnt', 'learned']),
        ('shut', ['shut'], ['shut']),
        ('understand', ['understood'], ['understood']),
        ('lend', ['lent'], ['lent']),
        ('ride', ['rode'], ['ridden']),
        ('catch', ['caught'], ['caught']),
        ('wear', ['wore'], ['worn']),
    ]},
    {"label": "Level 5 · tougher forms", "verbs": [
        ('bear', ['bore'], ['borne']),
        ('spin', ['spun'], ['spun']),
        ('mean', ['meant'], ['meant']),
        ('rise', ['rose'], ['risen']),
        ('bleed', ['bled'], ['bled']),
        ('split', ['split'], ['split']),
        ('shake', ['shook'], ['shaken']),
        ('shoot', ['shot'], ['shot']),
        ('lie', ['lay'], ['lain']),
        ('breed', ['bred'], ['bred']),
        ('spread', ['spread'], ['spread']),
        ('sleep', ['slept'], ['slept']),
        ('steal', ['stole'], ['stolen']),
        ('shine', ['shone'], ['shone']),
        ('drink', ['drank'], ['drunk']),
        ('flee', ['fled'], ['fled']),
        ('smell', ['smelt', 'smelled'], ['smelt', 'smelled']),
        ('wake', ['woke'], ['woken']),
        ('swear', ['swore'], ['sworn']),
        ('run', ['ran'], ['run']),
    ]},
    {"label": "Level 6 · less common", "verbs": [
        ('bet', ['bet'], ['bet']),
        ('spell', ['spelt', 'spelled'], ['spelt', 'spelled']),
        ('forbid', ['forbade', 'forbad'], ['forbidden']),
        ('fight', ['fought'], ['fought']),
        ('sting', ['stung'], ['stung']),
        ('lay', ['laid'], ['laid']),
        ('sweep', ['swept'], ['swept']),
        ('foresee', ['foresaw'], ['foreseen']),
        ('quit', ['quit'], ['quit']),
        ('tear', ['tore'], ['torn']),
        ('sink', ['sank'], ['sunk']),
        ('bind', ['bound'], ['bound']),
        ('creep', ['crept'], ['crept']),
        ('mistake', ['mistook'], ['mistaken']),
        ('rid', ['rid'], ['rid']),
        ('grind', ['ground'], ['ground']),
        ('kneel', ['knelt', 'kneeled'], ['knelt', 'kneeled']),
        ('oversee', ['oversaw'], ['overseen']),
        ('mow', ['mowed'], ['mown', 'mowed']),
        ('stick', ['stuck'], ['stuck']),
    ]},
    {"label": "Level 7 · tricky mix", "verbs": [
        ('lean', ['leant', 'leaned'], ['leant', 'leaned']),
        ('overtake', ['overtook'], ['overtaken']),
        ('mislead', ['misled'], ['misled']),
        ('spring', ['sprang'], ['sprung']),
        ('sweat', ['sweat', 'sweated'], ['sweat', 'sweated']),
        ('teach', ['taught'], ['taught']),
        ('swing', ['swung'], ['swung']),
        ('sew', ['sewed'], ['sewn', 'sewed']),
        ('leap', ['leapt', 'leaped'], ['leapt', 'leaped']),
        ('prove', ['proved'], ['proven', 'proved']),
        ('plead', ['pleaded', 'pled'], ['pleaded', 'pled']),
        ('burst', ['burst'], ['burst']),
        ('light', ['lit', 'lighted'], ['lit', 'lighted']),
        ('strive', ['strove'], ['striven']),
        ('sow', ['sowed'], ['sown', 'sowed']),
        ('uphold', ['upheld'], ['upheld']),
        ('spill', ['spilt', 'spilled'], ['spilt', 'spilled']),
        ('swell', ['swelled'], ['swollen', 'swelled']),
        ('stink', ['stank', 'stunk'], ['stunk']),
        ('forecast', ['forecast'], ['forecast']),
    ]},
    {"label": "Level 8 · rare & literary", "verbs": [
        ('overcome', ['overcame'], ['overcome']),
        ('spoil', ['spoilt', 'spoiled'], ['spoilt', 'spoiled']),
        ('tread', ['trod'], ['trodden']),
        ('wind', ['wound'], ['wound']),
        ('withdraw', ['withdrew'], ['withdrawn']),
        ('strike', ['struck'], ['struck']),
        ('weep', ['wept'], ['wept']),
        ('weave', ['wove'], ['woven']),
        ('shed', ['shed'], ['shed']),
        ('seek', ['sought'], ['sought']),
        ('wring', ['wrung'], ['wrung']),
        ('withhold', ['withheld'], ['withheld']),
        ('dwell', ['dwelt', 'dwelled'], ['dwelt', 'dwelled']),
        ('bid', ['bade', 'bid'], ['bidden', 'bid']),
        ('undergo', ['underwent'], ['undergone']),
        ('slay', ['slew'], ['slain']),
        ('thrust', ['thrust'], ['thrust']),
        ('thrive', ['thrived', 'throve'], ['thrived', 'thriven']),
        ('rebuild', ['rebuilt'], ['rebuilt']),
        ('forsake', ['forsook'], ['forsaken']),
    ]},
]


def _norm(s: str) -> str:
    return (s or "").strip().lower()


BUCKETS: List[Dict[str, Any]] = []
for _b in _RAW:
    BUCKETS.append({
        "label": _b["label"],
        "verbs": [
            {"base": _norm(base), "past": [_norm(x) for x in past], "pp": [_norm(x) for x in pp]}
            for (base, past, pp) in _b["verbs"]
        ],
    })

# Level 9 is the final check: every verb from every level in one pool. It is a
# bucket like any other so the rest of the engine can index it, but it is passed
# on different terms (irregular_verbs_logic.FINAL_*).
ALL_VERBS: List[Dict[str, Any]] = [v for _b in BUCKETS for v in _b["verbs"]]
BUCKETS.append({
    "label": f"Level {len(BUCKETS) + 1} · final check — all {len(ALL_VERBS)} verbs",
    "verbs": ALL_VERBS,
})

NUM_BUCKETS = len(BUCKETS)
FINAL_INDEX = NUM_BUCKETS - 1


def bucket_label(index: int) -> str:
    if 0 <= index < NUM_BUCKETS:
        return BUCKETS[index]["label"]
    return BUCKETS[-1]["label"] if BUCKETS else ""


def bucket_verbs(index: int) -> List[Dict[str, Any]]:
    if 0 <= index < NUM_BUCKETS:
        return BUCKETS[index]["verbs"]
    return BUCKETS[-1]["verbs"] if BUCKETS else []
