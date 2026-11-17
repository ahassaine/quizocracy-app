# Reading comprehension bank (`reading`, keys `RD…`)

Read `SPEC.md` first: everything there applies (ids, question types, `why`, `no`, `why2`, British English,
one defensible answer, no leaks, content rules). This file adds what is special to reading.

The content is **written by hand**. Every passage is original writing: never copy or closely paraphrase a
published text, and never use a real living person's private life. Non-fiction must be **true**: only facts
that are well established and taught in English schools; when unsure of a number or date, leave it out.

## A passage is a "skill"

Each file `app/bank/content/reading_yN.py` defines `SKILLS`, one entry per passage:

```python
SKILLS = [
    {
        "key": "RD3.01",               # RD + year + "." + 2-digit order within the year
        "year": 3,
        "strand": "Information",       # one of the KINDS below: the parent page groups by it
        "title": "How bees make honey",  # the passage's title, shown above it
        "nc": "Retrieve and record information from non-fiction",   # the NC reading statement it practises most
        "text": "Bees live together in a hive...\n\nA worker bee ...",   # the passage (see below)
        "qs": [ ...questions, in the order the child answers them... ],
    },
]
```

* `text`: paragraphs separated by a blank line (`\n\n`). A poem keeps its line breaks (`\n`) and puts a
  blank line between verses. A play script writes each line as `NAME: words` on its own line. A list of
  steps (instructions, a recipe) writes each step on its own line starting `1. `, `2. ` … No markdown, no
  headings inside the text (the title is shown above it), no pictures.
* Strands (`KINDS`): `Stories`, `Information`, `Instructions`, `Poems`, `Letters and diaries`,
  `Biography`, `News reports`, `Persuasive writing`, `Play scripts`, `Explanations`. Each year mixes them;
  stories and information texts are about half; every year has at least one poem.
* The child reads the passage once and answers its questions in the order written, with the passage on screen
  the whole time. So order the questions roughly as the text goes, the overall question (summary, main idea,
  purpose, title choice) last.

## Lengths and numbers per year

| Year | Passages | Words per passage | Questions per passage | Notes |
|---|---|---|---|---|
| 1 | 14 | 30–80 | 4 | short sentences, decodable everyday words; mostly mcq with 3 options; 1 `order` of 3 in about half |
| 2 | 14 | 80–160 | 5 | |
| 3 | 14 | 150–250 | 6 | |
| 4 | 14 | 200–300 | 6 | |
| 5 | 14 | 250–380 | 7 | |
| 6 | 16 | 300–450 | 7 | KS2 SATs style and spread of domains |
| 7, 8, 9 | 12 each | 350–550 | 7 | KS3: viewpoint, language and structure, comparison within the text |

## Questions

Every question has `"d"`: the reading skill it tests, one of

| d | Meaning (KS1 / KS2 test framework) |
|---|---|
| `vocab` | the meaning of a word or phrase in context (1a, 2a) |
| `retrieve` | find a fact or detail in the text (1b, 2b) |
| `sequence` | the order of events (1c) |
| `summarise` | the main idea of a paragraph or of the whole text (2c) |
| `infer` | feelings, reasons, motives, from clues; answer not stated in so many words (1d, 2d) |
| `predict` | what is likely to happen next, from the text (1e, 2e) |
| `structure` | how the text is organised; why a section or heading is there (2f) |
| `language` | why the writer chose a word or phrase; its effect (2g) |
| `compare` | compare two things, characters or ideas within the text (2h) |
| `purpose` | why the text was written; fact or opinion; who it is for |

Mix the domains in each passage. Over a year: about a third `retrieve`, a quarter `infer`, then `vocab`,
then the rest. Year 1–2: `retrieve`, `vocab`, `sequence`, `infer`, `predict` only.

Question types (see SPEC.md for mcq, tap, text):

* **mcq** (most questions): 3 options in Years 1–2, 4 in Years 3–9. Wrong options must be things a child who
  read carelessly could believe (a detail from the wrong paragraph, a too-literal reading), never silly.
  Inference options: the right one is supported by the text; each wrong one is contradicted or unsupported.
* **tap** "Find and tap": `s` is **one sentence copied exactly from the passage** (character for character,
  same punctuation), with the word(s) to tap in brackets. `q` says what to find: "Tap the word that shows the
  fox was hungry." The lint checks that the sentence is in the passage.
* **text** "Find and copy" / one-word answers: `a` lists every acceptable answer (a word or short phrase
  copied from the text, with and without "the" where both are fine). Only where the answer is clear-cut.
  Not in Year 1.
* **order**: put events in order. `items`: 3–5 short events, **in the right order**; the app shuffles them
  and the child taps them in order. `q`: "Put these in the order they happen in the story." Only for
  sequences the text makes certain.

Do not use `write` or `num` in reading. No question may be answerable without reading the passage
(general knowledge must not give the answer away: "What do bees make?" is out; "What does the hive keep warm
in winter, according to the text?" is in). Do not quote the answer sentence word for word in the question
when the domain is `infer`.

`why` (shown after a wrong answer): point to where the answer is: "The second paragraph says the hive is kept
at the same warmth all year." or explain the clue for an inference: "She hid her face and would not speak:
both show she was embarrassed."

## Content

Useful and true (science, nature, the body, history, geography, how things work, sport, health, everyday life,
good character). Stories are realistic (school, family, friends, animals behaving as animals, journeys,
challenges, kindness, honesty, perseverance); fables with talking animals are fine but no magic. No gods,
religion, festivals, magic, myths, legends with supernatural beings, fairies, dragons, ghosts, monsters,
horror, violence, romance, alcohol, gambling, brands, celebrities or politics. Varied names from many
backgrounds. Settings in the UK and around the world.

Make a passage worth reading: something a child learns from or enjoys. Vary topics across the year; no two
passages on the same subject.
