"""Reading comprehension, Year 1, second set (keys RD1.15-RD1.28).

Fourteen more short original passages (30-80 words) for children aged 5-6, on topics not used in
reading_y1.py, each with four questions in the KS1 reading domains only (vocab, retrieve, sequence, infer,
predict). Short sentences and decodable everyday words, with a few common exception words. Questions are
mcq with three options, tap (a sentence copied exactly from the passage) and order (three events); no
typed answers in Year 1.

* Stories: RD1.15, RD1.17, RD1.21, RD1.24, RD1.26
* Information: RD1.16, RD1.19, RD1.23, RD1.25, RD1.27
* Instructions: RD1.20
* Poems: RD1.18
* Letters and diaries: RD1.22, RD1.28

Written by hand; to be reviewed line by line by a second reader (a teacher or a parent) before release.
"""

SKILLS = [
    {
        "key": "RD1.15",
        "year": 1,
        "strand": "Stories",
        "title": "The wobbly tooth",
        "nc": "Discuss the sequence of events in a story; make inferences on the basis of what is being said and done",
        "text": "Ben had a wobbly tooth. It went this way and that way when he pushed it with his tongue.\n\n"
                "At lunch, Ben bit into a big green apple. Crunch! He felt a gap in his mouth. "
                "The tooth was in the apple!\n\n"
                "Ben ran to show Mum. “Look, I have a gap!” he said, with a big smile. Mum gave him a hug.",
        "qs": [
            {"id": "3fb0ab767960", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the tooth was loose.",
             "s": "Ben had a [wobbly] tooth.",
             "why": "A wobbly tooth is loose: it moves this way and that way."},
            {"id": "5b45999b8a44", "t": "mcq", "d": "retrieve", "q": "What did Ben bite into at lunch?",
             "opts": ["a green apple", "a slice of bread", "a carrot"],
             "why": "The second part says Ben bit into a big green apple."},
            {"id": "7c6a5085803f", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Ben pushed his tooth with his tongue.", "Ben bit into an apple.", "Ben ran to show Mum."],
             "why": "First Ben pushed the wobbly tooth, then he bit the apple, and then he ran to show Mum."},
            {"id": "2b6e280ce50d", "t": "mcq", "d": "infer", "q": "How did Ben feel about the gap in his mouth?",
             "opts": ["pleased", "scared", "cross"],
             "why": "He ran to show Mum and had a big smile, so he was pleased."},
        ],
    },
    {
        "key": "RD1.16",
        "year": 1,
        "strand": "Information",
        "title": "Snails",
        "nc": "Listen to and discuss non-fiction; discuss word meanings, linking new meanings to those already known",
        "text": "A snail has a soft body and a hard shell on its back. When it is scared, it hides inside its shell.\n\n"
                "A snail has no legs. It slides along on one big foot. It leaves a shiny, wet trail behind it.\n\n"
                "Snails like damp places. They come out after rain. "
                "They eat leaves, so some gardeners do not like them.",
        "qs": [
            {"id": "0aa520109d52", "t": "mcq", "d": "retrieve", "q": "What does a snail do when it is scared?",
             "opts": ["It hides inside its shell.", "It slides away on its foot.", "It leaves a shiny trail."],
             "why": "The first part says: when it is scared, it hides inside its shell."},
            {"id": "4fb5e8b1f901", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how many feet a snail has.",
             "s": "It slides along on [one] big foot.",
             "why": "The text says a snail slides along on one big foot."},
            {"id": "d8a764a4a07f", "t": "mcq", "d": "vocab", "q": "Snails like damp places. What does damp mean?",
             "opts": ["a bit wet", "very hot", "very dry"],
             "why": "Damp means a bit wet. Snails come out after rain, when things are damp."},
            {"id": "32e919461900", "t": "mcq", "d": "infer", "q": "Why do some gardeners not like snails?",
             "opts": ["Snails eat the leaves of their plants.", "Snails leave trails on the paths.",
                      "Snails hide in their shells."],
             "why": "The text says snails eat leaves. A gardener does not want the leaves of the plants eaten."},
        ],
    },
    {
        "key": "RD1.17",
        "year": 1,
        "strand": "Stories",
        "title": "Roti with Nani",
        "nc": "Discuss the sequence of events in a story; link what they read or hear to their own experiences",
        "text": "Arjun and Nani made roti for lunch. Nani mixed flour and water to make a soft dough.\n\n"
                "Arjun rolled the dough flat. It was not round. It had lumps and bumps, like a map! "
                "Nani laughed. “It will taste just as good,” she said.\n\n"
                "Nani put the roti in a hot pan. It puffed up like a ball. "
                "Arjun ate it with dal. “Yum! Can I make the next one?” he said.",
        "qs": [
            {"id": "a5d790cc8b54", "t": "mcq", "d": "retrieve", "q": "What did Nani mix to make the dough?",
             "opts": ["flour and water", "flour and milk", "eggs and water"],
             "why": "The first part says Nani mixed flour and water to make a soft dough."},
            {"id": "28fa5bd1fc36", "t": "mcq", "d": "vocab", "q": "Arjun's roti was like a map. What does this tell you?",
             "opts": ["It was a funny shape.", "It had writing on it.", "It was very big."],
             "why": "It was not round and it had lumps and bumps, so it was a funny shape, like a map."},
            {"id": "ba5d89410708", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Nani mixed the dough.", "Arjun rolled the dough flat.", "Nani put the roti in a hot pan."],
             "why": "Nani made the dough, then Arjun rolled it, and then Nani cooked it in the pan."},
            {"id": "8259e5ea83fc", "t": "mcq", "d": "infer", "q": "How do you know Arjun liked the roti?",
             "opts": ["He asked to make the next one.", "It puffed up like a ball.", "Nani laughed."],
             "why": "He said “Yum!” and asked to make the next one, so he liked it.",
             "no": {"It puffed up like a ball.": "That tells you about the roti, not what Arjun thought of it."}},
        ],
    },
    {
        "key": "RD1.18",
        "year": 1,
        "strand": "Poems",
        "title": "The train",
        "nc": "Learn to appreciate rhymes and poems; discuss word meanings",
        "text": "Clickety-clack, clickety-clack,\n"
                "The train runs fast along the track.\n\n"
                "Past the cows and past the sheep,\n"
                "Past the barn where kittens sleep.\n\n"
                "In the tunnel, dark as night,\n"
                "Then out again into the light!\n\n"
                "Slower, slower, now we stop.\n"
                "Here is the sea! Out we hop.",
        "qs": [
            {"id": "90a0d9c1d895", "t": "mcq", "d": "retrieve", "q": "In the first verse, what sound does the train make?",
             "opts": ["clickety-clack", "choo-choo", "toot-toot"],
             "why": "The first verse starts: clickety-clack, clickety-clack."},
            {"id": "d9e5ffc52d99", "t": "tap", "d": "retrieve", "q": "Tap the word for the animals that sleep in the barn.",
             "s": "Past the barn where [kittens] sleep.",
             "why": "The second verse says: past the barn where kittens sleep. The cows and sheep are outside."},
            {"id": "6b1faf9379f6", "t": "mcq", "d": "vocab", "q": "The tunnel is “dark as night”. What does this tell you?",
             "opts": ["It is very dark in the tunnel.", "The train goes in at night.", "The train stops in the tunnel."],
             "why": "Dark as night means very dark, as dark as it is at night.",
             "no": {"The train goes in at night.": "The poem says the tunnel is as dark as night, not that it is night."}},
            {"id": "ed8b1f0a4d84", "t": "mcq", "d": "infer", "q": "Where does the train stop?",
             "opts": ["by the sea", "in the tunnel", "by the barn"],
             "why": "When the train stops, the poem says: here is the sea! Out we hop."},
        ],
    },
    {
        "key": "RD1.19",
        "year": 1,
        "strand": "Information",
        "title": "The Moon",
        "nc": "Listen to and discuss non-fiction; retrieve information from a simple text",
        "text": "At night, you can often see the Moon in the sky. The Moon is a big ball of rock. "
                "It goes round and round the Earth.\n\n"
                "The Moon does not make its own light. It shines because the Sun lights it up.\n\n"
                "The Moon seems to change shape. Some nights it is a round full moon. "
                "Other nights it is a thin crescent, like a smile.",
        "qs": [
            {"id": "9d7f51f569fe", "t": "mcq", "d": "retrieve", "q": "What does the text say the Moon is?",
             "opts": ["a big ball of rock", "a big ball of ice", "a big ball of fire"],
             "why": "The first part says the Moon is a big ball of rock."},
            {"id": "11ad1eb694f7", "t": "mcq", "d": "retrieve", "q": "Why does the Moon shine?",
             "opts": ["The Sun lights it up.", "It makes its own light.", "The Earth lights it up."],
             "why": "The text says the Moon does not make its own light. It shines because the Sun lights it up.",
             "no": {"It makes its own light.": "The text says the Moon does not make its own light."}},
            {"id": "1cf2056016ed", "t": "mcq", "d": "retrieve", "q": "What is a full moon like?",
             "opts": ["round", "thin", "like a smile"],
             "why": "The last part says a full moon is round. The thin one, like a smile, is a crescent."},
            {"id": "5e2dfadb0b23", "t": "tap", "d": "vocab", "q": "Tap the word that is the name for the Moon when it is thin.",
             "s": "Other nights it is a thin [crescent], like a smile.",
             "why": "A crescent is a thin curved shape, like a smile."},
        ],
    },
    {
        "key": "RD1.20",
        "year": 1,
        "strand": "Instructions",
        "title": "Brush your teeth",
        "nc": "Listen to and discuss non-fiction; read and follow simple instructions",
        "text": "Brush your teeth in the morning and at bedtime.\n\n"
                "1. Wet your toothbrush.\n"
                "2. Put a pea-sized blob of toothpaste on it.\n"
                "3. Brush the front, the back and the top of every tooth.\n"
                "4. Keep brushing for two minutes.\n"
                "5. Spit out the toothpaste, but do not rinse with water.",
        "qs": [
            {"id": "12cbadfe68f5", "t": "mcq", "d": "retrieve", "q": "When should you brush your teeth?",
             "opts": ["in the morning and at bedtime", "after lunch and after tea", "only when they look dirty"],
             "why": "The first line says: brush your teeth in the morning and at bedtime."},
            {"id": "7ce6a7184d45", "t": "mcq", "d": "vocab", "q": "What is a pea-sized blob of toothpaste?",
             "opts": ["a small blob, as big as a pea", "a green blob", "a long line of toothpaste"],
             "why": "Pea-sized means as big as a pea, so it is a small blob."},
            {"id": "d2f4f571ddb2", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Wet your toothbrush.", "Put toothpaste on it.", "Spit out the toothpaste."],
             "why": "Wetting the brush is step 1, toothpaste is step 2 and spitting is step 5."},
            {"id": "441e71302582", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how many minutes to brush for.",
             "s": "Keep brushing for [two] minutes.",
             "why": "Step 4 says: keep brushing for two minutes."},
        ],
    },
    {
        "key": "RD1.21",
        "year": 1,
        "strand": "Stories",
        "title": "A seat on the bus",
        "nc": "Make inferences on the basis of what is being said and done",
        "text": "Hana and Mum got on the bus. Hana sat down by the window.\n\n"
                "At the next stop, an old man got on. He had a stick, and he walked slowly. "
                "There were no seats left.\n\n"
                "Hana got up. “You can have my seat,” she said. The man smiled and sat down. "
                "“Thank you, kind girl,” he said.\n\n"
                "Hana held on to the pole. Mum gave her a wink.",
        "qs": [
            {"id": "f7ef81df768f", "t": "mcq", "d": "retrieve", "q": "Where did Hana sit at first?",
             "opts": ["by the window", "next to the old man", "on Mum's lap"],
             "why": "The first part says Hana sat down by the window."},
            {"id": "97c750d5f8bf", "t": "tap", "d": "vocab", "q": "Tap the word that tells you how the old man walked.",
             "s": "He had a stick, and he walked [slowly].",
             "why": "The text says he walked slowly, with a stick."},
            {"id": "cbc7c65217a1", "t": "mcq", "d": "infer", "q": "Why did Hana give the man her seat?",
             "opts": ["He was old, and there were no seats left.", "Mum told her to get up.",
                      "She wanted to stand by the pole."],
             "why": "The man was old and walked with a stick, and there were no seats left, so Hana helped him.",
             "no": {"Mum told her to get up.": "Mum did not say anything. Hana got up all by herself."}},
            {"id": "444ca0bd61b2", "t": "mcq", "d": "infer", "q": "Mum gave Hana a wink. How did Mum feel?",
             "opts": ["proud of Hana", "cross with Hana", "worried about Hana"],
             "why": "Hana was kind to the old man. Mum's wink shows she was proud of her."},
        ],
    },
    {
        "key": "RD1.22",
        "year": 1,
        "strand": "Letters and diaries",
        "title": "A postcard from Scotland",
        "nc": "Make inferences on the basis of what is being said and done; link reading to their own experiences",
        "text": "Dear Nana,\n\n"
                "We are in Scotland. We are staying in a little hut by a lake. "
                "The hills are very big, and there is snow on the tops.\n\n"
                "Yesterday we went on a boat. I saw a big bird catch a fish!\n\n"
                "Today it is raining, so we are playing cards in the hut.\n\n"
                "Love from\nIsla",
        "qs": [
            {"id": "4ee960cddf99", "t": "mcq", "d": "retrieve", "q": "Who wrote this postcard?",
             "opts": ["Isla", "Nana", "Mum"],
             "why": "It ends with Love from Isla, so Isla wrote it. It is to Nana."},
            {"id": "addb9eef8b97", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the hut is small.",
             "s": "We are staying in a [little] hut by a lake.",
             "why": "Little means small. The hut is little."},
            {"id": "5bc2d601ea61", "t": "mcq", "d": "infer", "q": "Isla saw a big bird catch a fish! How did she feel?",
             "opts": ["excited", "sad", "sleepy"],
             "why": "She tells Nana about it and ends with “!”, so it was an exciting thing to see."},
            {"id": "8e786f6f3cd6", "t": "mcq", "d": "retrieve", "q": "Why are they in the hut today?",
             "opts": ["It is raining outside.", "The boat has gone.", "It is too dark to go out."],
             "why": "Isla says it is raining today, so they are playing cards inside the hut."},
        ],
    },
    {
        "key": "RD1.23",
        "year": 1,
        "strand": "Information",
        "title": "Bats",
        "nc": "Listen to and discuss non-fiction; discuss the sequence of events",
        "text": "A bat is an animal with fur. It has wings made of thin skin.\n\n"
                "In the day, bats sleep. They hang upside down in dark places, like caves, old barns and hollow trees.\n\n"
                "At night, bats wake up and fly out to hunt. Bats in the UK eat insects, like moths and flies. "
                "One small bat can eat lots of insects in one night.",
        "qs": [
            {"id": "0451ebca65ef", "t": "mcq", "d": "retrieve", "q": "What are a bat's wings made of?",
             "opts": ["thin skin", "feathers", "fur"],
             "why": "The first part says a bat has wings made of thin skin. Birds have feathers.",
             "no": {"fur": "A bat has fur on its body, but its wings are thin skin."}},
            {"id": "fbf29edcc035", "t": "tap", "d": "retrieve", "q": "Tap the two words that tell you how bats hang.",
             "s": "They hang [upside] [down] in dark places, like caves, old barns and hollow trees.",
             "why": "Bats hang upside down when they sleep in the day."},
            {"id": "b3d3d1c63493", "t": "mcq", "d": "vocab", "q": "Bats fly out to hunt. What does hunt mean here?",
             "opts": ["look for food to catch", "play with other bats", "find a place to sleep"],
             "why": "To hunt is to look for food and catch it. Bats catch insects to eat."},
            {"id": "b266cdfe73c9", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the text.",
             "items": ["Bats sleep upside down.", "Bats wake up.", "Bats fly out to hunt."],
             "why": "In the day bats sleep. At night they wake up and fly out to hunt."},
        ],
    },
    {
        "key": "RD1.24",
        "year": 1,
        "strand": "Stories",
        "title": "Oscar's tower",
        "nc": "Discuss the sequence of events in a story; make inferences on the basis of what is being said and done",
        "text": "Oscar made a tall tower with his blocks. It was as tall as his knee.\n\n"
                "His little sister, Rosa, crawled up. Bump! The tower fell down. "
                "Rosa giggled, but Oscar was cross.\n\n"
                "Then Oscar had an idea. He gave Rosa some blocks of her own. "
                "They made two towers side by side. Rosa's tower was little and wobbly, but she was so happy.",
        "qs": [
            {"id": "56a8ddfac07f", "t": "mcq", "d": "retrieve", "q": "How tall was Oscar's tower?",
             "opts": ["as tall as his knee", "as tall as Rosa", "as tall as the door"],
             "why": "The first part says the tower was as tall as his knee."},
            {"id": "720897a34194", "t": "mcq", "d": "infer", "q": "Why did Oscar's tower fall down?",
             "opts": ["Rosa bumped into it.", "Oscar took a block out.", "It was too wobbly."],
             "why": "Rosa crawled up, and then there was a bump, so Rosa knocked it down.",
             "no": {"It was too wobbly.": "Rosa's tower was the wobbly one, at the end of the story."}},
            {"id": "242a74c0e532", "t": "tap", "d": "vocab", "q": "Tap the word that tells you how Oscar felt when the tower fell.",
             "s": "Rosa giggled, but Oscar was [cross].",
             "why": "Cross means a bit angry. Rosa giggled, but Oscar was cross."},
            {"id": "2c7b7f79f81c", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Oscar made a tall tower.", "Rosa crawled up.", "Oscar gave Rosa some blocks."],
             "why": "Oscar made the tower, then Rosa crawled up and knocked it, and then Oscar gave her blocks."},
        ],
    },
    {
        "key": "RD1.25",
        "year": 1,
        "strand": "Information",
        "title": "Firefighters",
        "nc": "Listen to and discuss non-fiction; retrieve information from a simple text",
        "text": "Firefighters help to keep us safe. When there is a fire, they race to it in a fire engine.\n\n"
                "Firefighters wear thick coats and helmets to keep them safe from the heat. "
                "They use long hoses to spray water on the fire.\n\n"
                "Firefighters help in other ways too. They save people from floods. "
                "They can even get a cat down from a tall tree.",
        "qs": [
            {"id": "22793f9a2514", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the fire engine goes very fast.",
             "s": "When there is a fire, they [race] to it in a fire engine.",
             "why": "To race is to go very fast. Firefighters race to a fire."},
            {"id": "bdf0055e0036", "t": "mcq", "d": "retrieve", "q": "Why do firefighters wear thick coats and helmets?",
             "opts": ["to keep them safe from the heat", "to keep them dry in the rain", "to keep them warm in the snow"],
             "why": "The second part says the coats and helmets keep them safe from the heat."},
            {"id": "1fb3f66c532a", "t": "mcq", "d": "retrieve", "q": "What do firefighters use to spray water?",
             "opts": ["long hoses", "big buckets", "their helmets"],
             "why": "The text says they use long hoses to spray water on the fire."},
            {"id": "759fc807777f", "t": "mcq", "d": "infer", "q": "Which of these is a job firefighters do when there is no fire?",
             "opts": ["saving people from floods", "taking ill people to hospital", "mending broken roads"],
             "why": "The last part says firefighters help in other ways too, like saving people from floods."},
        ],
    },
    {
        "key": "RD1.26",
        "year": 1,
        "strand": "Stories",
        "title": "Sports day",
        "nc": "Make inferences on the basis of what is being said and done; discuss word meanings",
        "text": "It was sports day. Priya was in the running race. Bang! Off she went.\n\n"
                "Halfway down the track, Priya tripped and fell on the grass. Her knee hurt. "
                "The other children ran past.\n\n"
                "Priya got up. She did not stop. She ran and ran to the end. "
                "She came last, but everyone clapped and cheered for her. Priya felt as tall as a tree.",
        "qs": [
            {"id": "0d2a23a963bf", "t": "mcq", "d": "retrieve", "q": "Where did Priya fall?",
             "opts": ["halfway down the track", "at the very start", "at the end of the race"],
             "why": "The second part says she tripped halfway down the track."},
            {"id": "5e2022a9e760", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["The race began.", "Priya tripped and fell.", "Everyone clapped for Priya."],
             "why": "Bang! The race began. Then Priya fell. At the end, everyone clapped."},
            {"id": "a66ed0143262", "t": "mcq", "d": "infer", "q": "Why did everyone clap and cheer for Priya?",
             "opts": ["She got up and did not give up.", "She won the race.", "She was the fastest runner."],
             "why": "Priya fell but got up and ran to the end. She came last, so she did not win.",
             "no": {"She won the race.": "The text says she came last."}},
            {"id": "61200159de80", "t": "mcq", "d": "vocab", "q": "Priya felt as tall as a tree. This means she felt…",
             "opts": ["proud and happy", "tired and sore", "bigger than the others"],
             "why": "Feeling as tall as a tree means feeling very proud. Priya did not really grow."},
        ],
    },
    {
        "key": "RD1.27",
        "year": 1,
        "strand": "Information",
        "title": "Penguins",
        "nc": "Listen to and discuss non-fiction; discuss word meanings, linking new meanings to those already known",
        "text": "A penguin is a bird, but it cannot fly. Its wings are like flippers. "
                "It uses them to swim fast in the sea.\n\n"
                "Penguins eat fish. They dive under the water to catch them.\n\n"
                "Many penguins live where it is very cold. Thick feathers and a layer of fat keep them warm. "
                "On the ice, penguins waddle, or slide on their tummies.",
        "qs": [
            {"id": "2214fa1b00bc", "t": "mcq", "d": "retrieve", "q": "What does a penguin use its wings for?",
             "opts": ["to swim", "to fly", "to slide on the ice"],
             "why": "The first part says a penguin uses its wings to swim fast in the sea. It cannot fly.",
             "no": {"to fly": "The text says a penguin is a bird, but it cannot fly."}},
            {"id": "e2f76fad034b", "t": "mcq", "d": "vocab", "q": "Penguins dive under the water. What does dive mean?",
             "opts": ["jump in head first", "float on the top", "climb out"],
             "why": "To dive is to go into the water head first."},
            {"id": "814de79ff025", "t": "mcq", "d": "infer", "q": "Why do many penguins need thick feathers and a layer of fat?",
             "opts": ["They live where it is very cold.", "They need to fly far.", "They slide on their tummies."],
             "why": "Many penguins live where it is very cold, and the feathers and fat keep them warm."},
            {"id": "7f96362e26fd", "t": "tap", "d": "vocab", "q": "Tap the word that means walk with short steps, rocking from side to side.",
             "s": "On the ice, penguins [waddle], or slide on their tummies.",
             "why": "To waddle is to walk with short steps, rocking from side to side, like a penguin or a duck."},
        ],
    },
    {
        "key": "RD1.28",
        "year": 1,
        "strand": "Letters and diaries",
        "title": "Ada's busy week",
        "nc": "Discuss the sequence of events; make inferences on the basis of what is being said and done",
        "text": "Monday: I went to the park on my scooter. I went down the big hill!\n\n"
                "Tuesday: We went to the library. I got a book about trucks.\n\n"
                "Wednesday: I was ill, so I stayed at home in bed.\n\n"
                "Thursday: I felt better. I went back to school and read my truck book to Ms Lee.\n\n"
                "Friday: Pizza for tea!",
        "qs": [
            {"id": "cb4b70f3dabd", "t": "mcq", "d": "retrieve", "q": "What did Ada do on Monday?",
             "opts": ["went to the park on her scooter", "went to the library", "stayed at home in bed"],
             "why": "Monday says: I went to the park on my scooter."},
            {"id": "a7cd43f73f27", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the diary.",
             "items": ["Ada got a book at the library.", "Ada stayed at home in bed.", "Ada read to Ms Lee."],
             "why": "The library was on Tuesday, bed was on Wednesday and reading to Ms Lee was on Thursday."},
            {"id": "669e2d652da4", "t": "mcq", "d": "infer", "q": "What was the book Ada read to Ms Lee about?",
             "opts": ["trucks", "scooters", "pizza"],
             "why": "Ada got a book about trucks on Tuesday. On Thursday she read “my truck book”, the same book."},
            {"id": "e9f23e35a08c", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what Ada had for tea on Friday.",
             "s": "Friday: [Pizza] for tea!",
             "why": "Friday says: pizza for tea!"},
        ],
    },
]
