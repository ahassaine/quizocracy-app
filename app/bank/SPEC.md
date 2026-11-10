# Question banks: grammar & punctuation, and science

Hand-written question banks for two activities: **Grammar and punctuation** (`grammar`, keys `GP…`) and
**Science** (`science`, keys `SC…`), Years 1 to 9 of the national curriculum in England. No question is
produced by a program or a model at build or serve time. Everything here is written, and checked, by hand.

Each content file is a Python module in `app/bank/content/` that defines one list, `SKILLS`.
`scripts/bank_lint.py` checks every file, and a file that fails the lint is not loaded.

## A skill

```python
SKILLS = [
    {
        "key": "GP3.07",                 # GP (grammar) or SC (science) + year + "." + 2-digit order within the year
        "year": 3,
        "strand": "Punctuation",         # a short heading the parent page groups by
        "title": "Inverted commas for direct speech",   # what a parent reads: plain, short
        "nc": "Introduction to inverted commas to punctuate direct speech",  # the NC statement it covers
        "qs": [ ...questions... ],
    },
]
```

* Order within a year matters: the child meets skills in key order, so put foundations first.
* Each skill has **at least 20 questions** (aim for 22–25) and **at least 3 question types**: this is a
  production bank that a child works through for a whole school year, not a sample.
* Keys are unique across the whole bank. Do not renumber published keys later (progress is stored by key).

## Question ids

Every question carries a permanent `"id"` (12 hex characters), the first key of its dict:
`{"id": "40bb622cea67", "t": "write", ...}`. Children's seen lists, mistakes, retries and mastery are stored by
this id, so it **never changes**, even when the question's text, options or answers are edited, and it is
never reused. Write a new question without an id, then run `python scripts/bank_ids.py`: it gives each question
that lacks one a fresh id that no question has, and touches nothing else (running it again changes nothing).
Never type or copy an id by hand; the lint fails on a missing or duplicate id. Deleting a question retires its
id. (The ids written on 10 Nov 2026 are the hashes the questions were served under until then, so no record
had to move.)

## Question types

Every question has `"id"` (see above), `"t"` (type), `"q"` (the instruction or question) and `"why"` (one short sentence that
teaches the point; the child sees it after a wrong answer, under the right answer).

| t | Child does | Fields |
|---|---|---|
| `mcq` | picks one option | `opts`: 2–4 options, **the first one is the right answer** (the app shuffles them) |
| `tap` | taps word(s) in a sentence | `s`: the sentence, the right word(s) in square brackets: `"The dog ran [quickly] home."` |
| `text` | types a short answer (1–4 words) | `a`: list of accepted answers. Marking ignores capitals, spaces and a final . ? or ! |
| `write` | rewrites a sentence | `s`: the sentence to fix; `a`: list of exactly-correct versions. Marking is exact (capitals and punctuation count); only spaces and curly/straight quotes are normalised |
| `num` | types a number | `a`: the number; optional `tol` (allowed error, default 0) and `unit` (shown next to the box, e.g. `"m/s"`) |

Rules for each type:

* **mcq**: options are distinct, similar in length and form, and every wrong option is plausible: built from
  a real misconception, never a joke. Never "all of the above" / "none of the above". If the question is
  about a sentence, put the sentence in `q`.
* **tap**: one bracket pair per word; brackets wrap the word only, punctuation stays outside: `"[quickly]."`.
  Several bracketed words means the child must tap all of them (say so in `q`: "Tap the two adjectives.").
  Each target word appears once in the sentence. The sentence is shown with the brackets removed.
* **text**: list every reasonable correct form (`["evaporation", "evaporating"]`). Avoid questions where
  many different words would be correct; ask for a specific term.
* **write**: `s` must contain the error(s) to fix, and must differ from every answer. List every acceptable
  version (e.g. with and without an optional comma). Use straight quotes `'` `"` in the file.
* **num**: give the unit in `unit` and the question; use `tol` for rounding (e.g. `0.05`).

## Content rules

* Follow the national curriculum programme of study for the year (English Appendix 2 for grammar and
  punctuation; the science programmes of study). Every statutory statement for the year is covered by at
  least one skill. KS3 is one key stage; the year split is set in the brief and documented in each file.
* Right for the age: Years 1–2 use very short sentences and everyday words; KS3 uses proper terminology.
* British English spelling and usage (colour, metre, programme, mum, maths, £). SI units in science.
* One answer only. Each question must have exactly one defensible answer at that year's level. If a
  teacher could argue for a second option, rewrite it.
* No answer leaks: the right option is not the longest, the most detailed or the only grammatical fit.
  Vary the position of the idea across questions (the app shuffles, but phrasing patterns also leak).
* Questions in a skill are different questions, not the same one with a word swapped.
* Neutral, everyday content: school, home, animals, sport, food, weather, places. Varied names
  (Amir, Chloe, Kofi, Mia, Priya, Sam, Yusuf, Zara …). No gods, magic, myths, horror, violence, brands,
  or politics. Human reproduction and drugs (science) are written as in a school textbook: factual, brief.
* Text only: never refer to a picture, diagram or graph that is not given in the question.
* Science facts must be correct as taught in English schools. When the curriculum simplifies (e.g. KS2
  "light travels in straight lines"), use the curriculum's version for that year.
