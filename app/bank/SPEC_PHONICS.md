# Phonics bank (`phonics`, keys `PH…`): Years 1 and 2

Read `SPEC.md` first: everything there applies (ids, at least 20 questions and 3 types per skill, `why`,
British English, one defensible answer, no leaks). This file adds what is special to phonics.

Phonics is for children aged 5–7 who are learning to decode. The skill is **reading the letters**, so the app
never reads aloud a word the child is meant to decode. Questions are short; instructions are a few plain words
(a grown-up or the 🔊 button reads the instruction `q`, never the word in `w`).

## Two extra fields

* `"w"`: the word (or alien word, or short phrase) the child must **read**. Shown big, never spoken.
* `"say"`: a word the app **speaks** (🔊, and once automatically). Never shown. Use it for "listen and
  choose". `say` must be a real, common English word that a speech voice pronounces clearly and in one standard
  British way (no homographs like "read", "wind", "bow"; no names). The said word is not written in `q`.

A question has `w` or `say` (or neither, when `q` itself is the reading), never both.

## Question types

| t | Child does | Fields |
|---|---|---|
| `mcq` | picks one option | `opts`: 2–4 options, **first one right**. Options can be words, or **one emoji picture each** |
| `seg` | sound buttons: taps between the letters to split the word into its sounds | `w`: the word; `a`: the word with `|` between sounds, e.g. `"sh|i|p"`, `"t|r|ai|n"` (rules below) |
| `text` | types a short word | `a`: accepted answers. Only with `say` ("Listen, then type the word"); Year 2 mostly |
| `tap` | taps a word in a short sentence | as in SPEC.md; the sentence is shown, not read; `q` says what to find |

`seg` rules: the letters of `a` without the `|` must spell `w` exactly. Split only between graphemes
(`sh|i|p`, `ch|ai|n`, `l|igh|t`, `b|oa|t`, `f|ar|m`, `s|t|o|p`, `j|u|m|p`). **Do not use `seg` for words with a
split digraph** (cake, bike) or a silent letter. Words with double letters keep them together (`b|e|ll`,
`d|u|ck`, `f|i|zz`). Use words where the split is beyond dispute in a standard UK phonics programme.

Common question patterns (mix them; each skill needs at least 3 types):

1. **Read and pick the picture**: `{"t": "mcq", "q": "Read the word. Which picture is it?", "w": "ship",
   "opts": ["🚢", "🐑", "🐟"]}`. Distractors are pictures of words that differ by one sound (ship / sheep,
   fish) so guessing from the first letter fails. Only emoji that every phone shows clearly and that a 5-year-old
   names one way (🐟 fish, not "trout"). See the EMOJI list below; do not use others.
2. **Read and pick the word that matches a picture**: `{"t": "mcq", "q": "🐟 Which word is this?", "opts":
   ["fish", "fizz", "dish"]}` (the picture in `q`, words as options).
3. **Listen and choose the spelling**: `{"t": "mcq", "q": "Listen. Which word did you hear?", "say": "rain",
   "opts": ["rain", "ran", "rail"]}`. Options are real words, or plausible spellings of the same sounds
   (`"rain", "rane", "rayn"`) only in the alternative-spellings skills.
4. **Sound buttons**: `{"t": "seg", "q": "Tap between the sounds.", "w": "chip", "a": "ch|i|p"}`.
5. **Alien words** (the Year 1 check has them): `{"t": "mcq", "q": "This is an alien name. Which real word
   rhymes with it?", "w": "vap", "opts": ["cap", "van", "vet"]}`. Alien words follow normal phonics and are not
   real words (check!). Rhymes must rhyme in standard British English.
6. **Which word has this sound** (with `say`): `{"t": "mcq", "q": "Which word has the same sound in the
   middle as the word you hear?", "say": "boat", "opts": ["coat", "cot", "cat"]}`.
7. **Tap the word** (Years 1–2, short sentence): `{"t": "tap", "q": "Tap the word that names an animal.",
   "s": "The [goat] is on the hill."}`.
8. **Complete the word** (mcq): `{"t": "mcq", "q": "🌧️ r _ _ n: which letters are missing?", "opts": ["ai",
   "ay", "a"]}` (Year 1 Phase 5 and Year 2 alternative spellings; the right spelling must be the only correct one).

`why` is one short line a 6-year-old's grown-up can say: "s-h-i-p: 'sh' is one sound, so ship has three
sounds." / "'ai' says /ai/ as in rain."

## EMOJI you may use (picture → the one word it means)

🐟 fish · 🚢 ship · 🐑 sheep · 🐐 goat · 🐄 cow · 🐖 pig · 🐕 dog · 🐈 cat · 🐀 rat · 🦆 duck · 🐔 hen · 🦊 fox · 🐸 frog · 🐝 bee · 🐜 ant · 🦉 owl · 🐛 bug · 🦀 crab · 🐌 snail · 🐍 snake · 🦈 shark · 🐳 whale · 🐢 turtle · 🦁 lion · 🐯 tiger · 🐻 bear · 🦓 zebra · 🐘 elephant · 🐒 monkey · 🦒 giraffe · 🐇 rabbit · 🐿️ squirrel · 🦇 bat · 🐞 ladybird · 🕷️ spider · 🐙 octopus · 🦋 butterfly · 🐦 bird · 🐣 chick · 🌧️ rain · ☀️ sun · 🌙 moon · ⭐ star · ❄️ snow · 🌳 tree · 🌸 flower · 🍂 leaf · 🌊 wave · 🔥 fire · ⛰️ hill · 🌈 rainbow · 🐚 shell · 🪨 rock · 🏠 house · 🚪 door · 🛏️ bed · 🪑 chair · 🛁 bath · 🚗 car · 🚌 bus · 🚂 train · 🚲 bike · ✈️ plane · ⛵ boat · 🛶 canoe · 🚀 rocket · 🎩 hat · 👑 crown · 👕 shirt · 🧦 sock · 👢 boot · 🧤 glove · 🎒 bag · 🧢 cap · 🍎 apple · 🍌 banana · 🍇 grapes · 🍋 lemon · 🥕 carrot · 🌽 corn · 🍞 bread · 🧀 cheese · 🥚 egg · 🍰 cake · 🍪 biscuit · 🥛 milk · ☕ cup · 🥄 spoon · 🍴 fork · 🍳 pan · 🫖 teapot · 🥣 bowl · 🔑 key · 🔒 lock · 🔔 bell · 🧸 teddy · 🪁 kite · ⚽ ball · 🥁 drum · 🎸 guitar · 📚 books · ✏️ pencil · 🖊️ pen · 📦 box · 🪣 bucket · 🧺 basket · 🕯️ candle · 💡 bulb · 🧲 magnet · ⏰ clock · 🎁 gift · 💍 ring · 👂 ear · 👁️ eye · 👃 nose · 👄 lips · 🦷 tooth · ✋ hand · 🦶 foot · 🦴 bone · 🛝 slide · 🎈 balloon · ⛺ tent · 🧹 broom · 🪥 toothbrush · 🧼 soap · 🧽 sponge · 🪜 ladder · 🔨 hammer · 🪚 saw · 🧊 ice · 🍕 pizza · 🥪 sandwich · 🍉 melon · 🍑 peach · 🍐 pear · 🍒 cherries · 🥥 coconut · 🍄 mushroom · 🥜 nuts

Use only these, each for exactly the word given. Never two pictures for the same word in one question.

## Content

Everyday words a 5–7-year-old knows. Real words in the right phase (no grapheme the child has not met yet in
that skill's phase, except in the distractors of later skills). Alien words never spell a real word, a rude
word or a name. No gods, magic, monsters, brands. British English (mum, biscuit, rubbish, sweets).
