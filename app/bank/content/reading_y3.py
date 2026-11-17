"""Reading comprehension, Year 3 (keys RD3.xx).

Fourteen original passages, written by hand, 150-250 words each, six questions each (mcq with four
options, find-and-tap, find-and-copy and put-in-order), mixing the KS2 reading domains (about a third
retrieval, a quarter inference, then vocabulary, sequence, summary, structure, language, comparison,
prediction and purpose). Topics link to the Year 3 curriculum where natural (Stone Age to Iron Age,
fossils, light and shadows, magnets, plants, the skeleton and muscles, food and nutrition, volcanoes and
earthquakes, rivers), alongside realistic stories, one poem, instructions, a diary and a letter:

* RD3.01 The new girl (story: a new pupil)
* RD3.02 From stone tools to iron (information: Stone Age to Iron Age)
* RD3.03 How a fossil forms (explanation)
* RD3.04 Pepper comes home (story: a lost pet found)
* RD3.05 Light and shadows (information)
* RD3.06 Make a magnet fishing game (instructions)
* RD3.07 My Bean (poem: what plants need)
* RD3.08 Bones and muscles (information)
* RD3.09 A day at Maiden Castle (diary: an Iron Age hillfort)
* RD3.10 Kenji lets go (story: learning a skill)
* RD3.11 Volcanoes and earthquakes (information)
* RD3.12 A river's journey (explanation)
* RD3.13 A letter to Grandad (letter: food and nutrition)
* RD3.14 The folded note (story: honesty)

Written for Quizocracy; to be reviewed line by line by a second reviewer (facts, one defensible answer,
no leaks) before it goes live.
"""

SKILLS = [
    {
        "key": "RD3.01",
        "year": 3,
        "strand": "Stories",
        "title": "The new girl",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "On Monday morning, Mrs Okafor brought a girl into Class 3. “This is Ewa,” she said. “Her family has just moved to Leeds from Poland.” Ewa held the straps of her rucksack tightly and stared at the floor.\n\n"
                "Mrs Okafor sat her next to Leo. Leo smiled, but Ewa did not look up. During maths she copied the sums carefully, but she did not say a word. At break time she stood alone by the fence and watched the others play football.\n\n"
                "Leo remembered his own first day at a new school, when he had not known anyone at all. He picked up the ball and walked over to the fence. “Do you want to play?” he asked, pointing at the goal.\n\n"
                "Ewa shook her head at first. Then she looked at the ball, and something changed in her face. She took it, dropped it onto her foot and flicked it high into the air, then caught it on her knee. Leo's mouth fell open.\n\n"
                "“You're brilliant!” he said.\n\n"
                "By the end of break, everyone wanted Ewa on their team. She did not know many English words yet, but she knew “pass” and “goal”, and she laughed when Leo tried to say “dzień dobry”, which means “good morning” in Polish. When the bell rang, she walked back to class beside him, chatting with her hands.",
        "qs": [
            {"id": "99bb732df80a", "t": "mcq", "d": "infer", "q": "How did Ewa feel when she first came into Class 3?",
             "opts": ["nervous", "angry", "excited", "bored"],
             "why": "She held her rucksack straps tightly and stared at the floor: both show she was nervous."},
            {"id": "ac016b7d1d62", "t": "text", "d": "retrieve", "q": "Where did Ewa stand at break time? Find and copy the words.",
             "a": ["by the fence", "alone by the fence", "the fence"],
             "why": "The second paragraph says she stood alone by the fence and watched the others."},
            {"id": "72b4c9461586", "t": "mcq", "d": "infer", "q": "Why did Leo go over to Ewa with the ball?",
             "opts": ["He remembered how it felt to know nobody.", "Mrs Okafor had told him to fetch her.",
                      "His team needed one more player to win.", "Ewa had asked him for a game."],
             "why": "The third paragraph says Leo remembered his own first day at a new school, when he had not known anyone."},
            {"id": "808623c1040a", "t": "mcq", "d": "language", "q": "The writer says “Leo's mouth fell open.” What does this show?",
             "opts": ["Leo was amazed.", "Leo was about to shout.", "Leo was feeling tired.", "Leo was laughing at Ewa."],
             "why": "A mouth falling open is what happens when someone is amazed: Ewa's trick surprised him."},
            {"id": "bbc1291d00e9", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Mrs Okafor brought Ewa into Class 3.", "Ewa copied the sums in maths.", "Leo asked Ewa to play.",
                       "Ewa caught the ball on her knee.", "Ewa walked back to class with Leo."],
             "why": "The story follows Ewa's first day: the classroom, maths, break time, the trick, then the bell."},
            {"id": "1c6367502cf5", "t": "mcq", "d": "summarise", "q": "What is the story mainly about?",
             "opts": ["how a friendly offer helped a new pupil settle in", "how Leo learned to speak Polish",
                      "how Class 3 won a football match", "how Ewa's family moved to Leeds"],
             "why": "Ewa starts the day alone and silent; after Leo invites her to play, she has friends by the end of break."},
        ],
    },
    {
        "key": "RD3.02",
        "year": 3,
        "strand": "Information",
        "title": "From stone tools to iron",
        "nc": "Retrieve and record information from non-fiction",
        "text": "The Stone Age was the longest period of human history. It got its name because people made their tools from stone. In Britain they often used flint, a hard stone that can be chipped to give a sharp edge. With flint axes, knives and arrowheads, they could cut wood, hunt and prepare food.\n\n"
                "For thousands of years, people in Britain were hunter-gatherers. They moved from place to place, hunting deer and wild boar and gathering nuts, berries and roots. Later, people learned to farm. They grew crops and kept animals such as sheep and cattle, so they could stay in one place. On the Orkney Islands in Scotland, you can still visit Skara Brae, a village of stone houses about 5,000 years old. Inside, there are beds and shelves made of stone, because few trees grew there to give wood.\n\n"
                "Next came the Bronze Age. People discovered that melting copper and tin together made bronze, a metal harder than copper alone.\n\n"
                "Finally, in the Iron Age, people learned to make tools from iron. Iron was harder to work, but it could be found in many more places than copper and tin. Iron Age people lived in roundhouses with thatched roofs, and many built hillforts: settlements on hilltops, protected by deep ditches and high banks of earth.",
        "qs": [
            {"id": "85a1ec45b42b", "t": "mcq", "d": "retrieve", "q": "According to the text, why was flint useful for making tools?",
             "opts": ["It could be chipped to give a sharp edge.", "It was soft and easy to bend.",
                      "It could be melted to make bronze.", "It was found only on hilltops."],
             "why": "The first paragraph says flint is a hard stone that can be chipped to give a sharp edge."},
            {"id": "139460ac5b9e", "t": "mcq", "d": "vocab", "q": "What does “hunter-gatherers” mean in the second paragraph?",
             "opts": ["people who hunted animals and collected wild food", "people who kept sheep and cattle",
                      "people who built forts on hills", "people who made tools from metal"],
             "why": "The next sentence explains it: they hunted deer and boar and gathered nuts, berries and roots."},
            {"id": "9bb03cbab7dc", "t": "mcq", "d": "infer", "q": "Why could farmers stay in one place when hunter-gatherers moved around?",
             "opts": ["Their crops and animals gave them food close by.", "They had iron tools to build houses.",
                      "All the deer and boar had gone.", "They all lived on the Orkney Islands."],
             "why": "Hunter-gatherers moved to find food; farmers grew crops and kept animals, so their food was where they lived."},
            {"id": "139d937e41bd", "t": "text", "d": "retrieve", "q": "Which two metals were melted together to make bronze?",
             "a": ["copper and tin", "tin and copper", "copper, tin", "tin, copper"],
             "why": "The third paragraph says melting copper and tin together made bronze."},
            {"id": "034620d4ce24", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what kind of roofs the roundhouses had.",
             "s": "Iron Age people lived in roundhouses with [thatched] roofs, and many built hillforts: settlements on hilltops, protected by deep ditches and high banks of earth.",
             "why": "The roundhouses had thatched roofs, made of straw or reeds."},
            {"id": "f86b661783c7", "t": "mcq", "d": "structure", "q": "How is this text organised?",
             "opts": ["in time order, from the Stone Age to the Iron Age", "as a list of questions and answers",
                      "as a story told by one Stone Age child", "from the newest times back to the oldest"],
             "why": "It begins with the Stone Age, then says “Next came the Bronze Age” and “Finally, in the Iron Age”."},
        ],
    },
    {
        "key": "RD3.03",
        "year": 3,
        "strand": "Explanations",
        "title": "How a fossil forms",
        "nc": "Read books that are structured in different ways and read for a range of purposes",
        "text": "A fossil is the remains or trace of a living thing from long ago, kept in rock. Most living things never become fossils. It only happens when the conditions are just right.\n\n"
                "Imagine an ammonite, a sea creature with a curled shell, that died millions of years ago. Its body sank to the sea bed. The soft parts rotted away or were eaten, but the hard shell was left behind.\n\n"
                "Soon, the shell was buried by sand and mud. More and more layers settled on top. Over a very long time, the weight of these layers pressed the lower ones together until they slowly turned into rock.\n\n"
                "Meanwhile, water trickled through the rock. It carried tiny bits of minerals, which slowly took the place of the shell. In the end, there was a stone copy of the ammonite, with exactly the same shape as the shell.\n\n"
                "Millions of years later, the land moved and the old sea bed was pushed up. Wind, rain and waves wore the rock away, little by little, until the fossil appeared at the surface. Then one day, someone walking along a beach spotted it.\n\n"
                "This is why fossils are often found in cliffs by the sea, and why most of them are shells, bones and teeth: the hard parts of living things.",
        "qs": [
            {"id": "0f3ce27195b4", "t": "mcq", "d": "retrieve", "q": "According to the text, what happened to the soft parts of the ammonite?",
             "opts": ["They rotted away or were eaten.", "They slowly turned into rock.",
                      "They were pushed up with the land.", "They were washed onto a beach."],
             "why": "The second paragraph says the soft parts rotted away or were eaten, but the hard shell was left."},
            {"id": "bc3e1ebb64c5", "t": "mcq", "d": "vocab", "q": "“The weight of these layers pressed the lower ones together.” Which word means the same as “pressed” here?",
             "opts": ["squashed", "lifted", "washed", "warmed"],
             "why": "The heavy layers on top pushed down hard on the ones below: they squashed them together."},
            {"id": "5c6b47393252", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the text.",
             "items": ["The ammonite died and sank to the sea bed.", "Sand and mud buried the shell.",
                       "Minerals took the place of the shell.", "The old sea bed was pushed up.",
                       "Someone spotted the fossil on a beach."],
             "why": "The text explains the steps in time order, one paragraph after another."},
            {"id": "21a588e61d2d", "t": "text", "d": "retrieve", "q": "What carried tiny bits of minerals through the rock? Find and copy one word.",
             "a": ["water", "the water"],
             "why": "The fourth paragraph says water trickled through the rock, carrying tiny bits of minerals."},
            {"id": "6ce02445aec6", "t": "mcq", "d": "infer", "q": "Why are fossils of skin very rare?",
             "opts": ["Soft parts usually rot away before they are buried.", "Skin is too light to sink to the sea bed.",
                      "Water cannot trickle through skin.", "Skin is worn away by the wind on the beach."],
             "why": "Skin is a soft part. The text says soft parts rot or are eaten, and most fossils are the hard parts."},
            {"id": "ccfd5abedb41", "t": "mcq", "d": "language", "q": "Why does the writer say “Imagine an ammonite” in the second paragraph?",
             "opts": ["to follow one example through every step", "to show that ammonites were never real",
                      "to begin a made-up story about the sea", "to ask the reader to draw an ammonite"],
             "why": "The writer picks one creature and follows it from the sea bed to the beach, so each step is easy to picture."},
        ],
    },
    {
        "key": "RD3.04",
        "year": 3,
        "strand": "Stories",
        "title": "Pepper comes home",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "Pepper, the Bangura family's grey cat, had been missing for four days. Amara had looked under every car on their street in Cardiff and called his name until her throat was sore. Each evening, she put his bowl by the back door, and each morning it was still full.\n\n"
                "On Saturday, Amara and her dad made posters. They printed a photo of Pepper with his white paws and the words LOST CAT in big red letters. Then they walked round the neighbourhood, taping the posters to lamp posts and pushing them through letterboxes.\n\n"
                "“Cats often hide when they're frightened,” Dad said. “Keep listening, not just looking.”\n\n"
                "On Sunday afternoon, the phone rang. It was Mr Price from number 42. He had just come home after a week away. When he opened his garden shed, he had heard a faint mew from behind some flowerpots.\n\n"
                "Amara ran all the way there. Pepper was curled up in an old box, thin and dusty, but his green eyes were wide open. When she knelt down, he climbed slowly into her arms and pressed his head against her chin.\n\n"
                "At home, Pepper emptied his bowl twice and fell asleep on Amara's bed. The next morning, Amara wrote a thank-you card for Mr Price, and Dad took the posters down.",
        "qs": [
            {"id": "01bb33c3d5f5", "t": "mcq", "d": "retrieve", "q": "How long had Pepper been missing when the story begins?",
             "opts": ["four days", "a week", "two days", "since Saturday"],
             "why": "The first sentence says Pepper had been missing for four days. It was Mr Price who had been away for a week."},
            {"id": "216b1c905d87", "t": "mcq", "d": "infer", "q": "Each morning, Pepper's bowl was still full. What did this tell Amara?",
             "opts": ["Pepper had not come home in the night.", "Pepper did not like his food any more.",
                      "Someone else had been feeding Pepper.", "The bowl was by the wrong door."],
             "why": "If Pepper had come back, he would have eaten. A full bowl meant he was still missing."},
            {"id": "986ddab6c202", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you the colour of Pepper's paws.",
             "s": "They printed a photo of Pepper with his [white] paws and the words LOST CAT in big red letters.",
             "why": "The poster showed Pepper with his white paws. The red was the colour of the letters."},
            {"id": "6e1572f0f871", "t": "mcq", "d": "infer", "q": "Why could Pepper not come home by himself?",
             "opts": ["He was shut inside Mr Price's shed.", "He was stuck under a car in the street.",
                      "He had lost his way in the park.", "He had hurt one of his paws."],
             "why": "Mr Price had been away and found Pepper only when he opened his shed, so Pepper had been shut in."},
            {"id": "f1258b9c769e", "t": "mcq", "d": "vocab", "q": "Mr Price heard “a faint mew”. What does “faint” mean here?",
             "opts": ["quiet and hard to hear", "loud and sharp", "angry and fierce", "sudden and scary"],
             "why": "Pepper was weak and hidden behind flowerpots, so his mew was quiet and hard to hear."},
            {"id": "b7f815ff3667", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Amara called Pepper's name in the street.", "Amara and Dad made posters.",
                       "Mr Price phoned the family.", "Amara found Pepper in an old box.", "Dad took the posters down."],
             "why": "Amara searched first, then made posters on Saturday; Mr Price rang on Sunday; the posters came down the next morning."},
        ],
    },
    {
        "key": "RD3.05",
        "year": 3,
        "strand": "Information",
        "title": "Light and shadows",
        "nc": "Retrieve and record information from non-fiction",
        "text": "We need light to see things. Light comes from a light source, such as the Sun, a torch or a candle flame. The Moon is not a light source: it only reflects light from the Sun. When there is no light at all, it is completely dark and we cannot see anything.\n\n"
                "Light travels in straight lines. When something blocks the light, a dark patch forms behind it where the light cannot reach. This dark patch is called a shadow.\n\n"
                "Not every material makes a good shadow. Opaque materials, like wood, metal and cardboard, block all the light, so they make dark shadows. Translucent materials, like tissue paper and frosted glass, let some light through, so their shadows are pale. Transparent materials, like clear glass, let almost all the light through, so they make hardly any shadow.\n\n"
                "The size of a shadow can change. If you hold a toy close to a torch, its shadow on the wall grows bigger. Move the toy away from the torch, towards the wall, and the shadow shrinks.\n\n"
                "Outside, your shadow changes during the day. In the early morning and evening, when the Sun is low in the sky, shadows are long. At midday, when the Sun is high, they are short.\n\n"
                "Never look straight at the Sun, even through sunglasses. Its light is strong enough to damage your eyes.",
        "qs": [
            {"id": "b8b3d901b3b4", "t": "mcq", "d": "retrieve", "q": "According to the text, why is the Moon not a light source?",
             "opts": ["It only reflects light from the Sun.", "It is too far away to see.",
                      "It only shines late at night.", "It is made of an opaque material."],
             "why": "The first paragraph says the Moon only reflects light from the Sun."},
            {"id": "79661f28215f", "t": "mcq", "d": "vocab", "q": "What does “opaque” mean, as it is used in the text?",
             "opts": ["lets no light through", "lets some light through", "lets almost all light through", "gives out its own light"],
             "why": "The third paragraph says opaque materials block all the light."},
            {"id": "c12504320604", "t": "mcq", "d": "compare", "q": "How is the shadow of tissue paper different from the shadow of cardboard?",
             "opts": ["It is paler.", "It is darker.", "It is bigger.", "It is a different shape."],
             "why": "Tissue paper is translucent and lets some light through, so its shadow is pale. Cardboard blocks all the light."},
            {"id": "0f7fa680b20e", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what happens to the shadow when the toy is moved towards the wall.",
             "s": "Move the toy away from the torch, towards the wall, and the shadow [shrinks].",
             "why": "Moving the toy away from the torch and towards the wall makes the shadow shrink."},
            {"id": "248e4398e249", "t": "mcq", "d": "predict", "q": "On a sunny summer day, Jake looks at his shadow at midday and again in the early evening. What will he find?",
             "opts": ["His evening shadow is longer.", "His midday shadow is longer.",
                      "Both shadows are the same length.", "He has no shadow at midday."],
             "why": "The text says shadows are long when the Sun is low, in the evening, and short at midday when it is high."},
            {"id": "55ece80e5954", "t": "mcq", "d": "purpose", "q": "Why does the writer end with the last paragraph?",
             "opts": ["to keep readers' eyes safe", "to explain how a shadow is made",
                      "to show that the Sun is a light source", "to tell readers not to play outside"],
             "why": "The last paragraph is a warning: the Sun's light is strong enough to damage your eyes."},
        ],
    },
    {
        "key": "RD3.06",
        "year": 3,
        "strand": "Instructions",
        "title": "Make a magnet fishing game",
        "nc": "Read books that are structured in different ways and read for a range of purposes",
        "text": "You can make a fishing game that works with magnets. It works because magnets attract things made of iron or steel, but not paper, plastic or wood.\n\n"
                "You will need: card, scissors, felt-tip pens, ten steel paper clips, two pencils, string, sticky tape and two small magnets.\n\n"
                "1. Draw ten fish on the card, each about the size of your hand.\n"
                "2. Colour the fish and write a number from 1 to 10 on each one.\n"
                "3. Ask an adult to help you cut the fish out.\n"
                "4. Slide a paper clip onto the nose of each fish.\n"
                "5. Tie a piece of string, about as long as your arm, to the end of each pencil. These are your fishing rods.\n"
                "6. Tape a magnet firmly to the loose end of each string.\n"
                "7. Spread the fish out on the floor, number side down.\n"
                "8. Take turns to dangle your magnet over the fish until one sticks. Turn it over and keep it.\n"
                "9. When all the fish are caught, add up the numbers on your fish. The player with the highest total wins.\n\n"
                "Tip: if a fish will not stick, check its paper clip. Some clips are coated in coloured plastic, but there should still be steel underneath. If you used kitchen foil instead, it will not work, because foil is made of aluminium, and aluminium is not magnetic.",
        "qs": [
            {"id": "bf443a5ae00e", "t": "mcq", "d": "retrieve", "q": "Why does each fish need a paper clip?",
             "opts": ["The magnet attracts the steel clip.", "The clip makes the fish sink.",
                      "The clip holds the number on.", "The clip ties the fish to the string."],
             "why": "The first paragraph says magnets attract things made of steel, and the paper clips are steel."},
            {"id": "58bb105c8c7c", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Draw ten fish on the card.", "Cut the fish out.", "Slide a paper clip onto each fish.",
                       "Tape a magnet to each string.", "Add up the numbers on your fish."],
             "why": "Follow the numbered steps: draw (1), cut (3), clip (4), magnet (6), add up (9)."},
            {"id": "02a4839dc471", "t": "text", "d": "retrieve", "q": "What do the pencils become in this game? Find and copy two words.",
             "a": ["fishing rods", "your fishing rods", "fishing rod", "a fishing rod", "the fishing rods"],
             "why": "Step 5 says the pencils with string tied on are your fishing rods."},
            {"id": "af69088f2e52", "t": "mcq", "d": "infer", "q": "Why should the fish be spread out number side down?",
             "opts": ["so players cannot pick out the high numbers", "so the paper clips stick to the floor",
                      "so the magnets pull more strongly", "so the colours do not rub off"],
             "why": "The highest total wins. If the numbers were showing, players would aim for the big ones."},
            {"id": "39318077d781", "t": "tap", "d": "vocab", "q": "Tap the word that means “let something hang down and swing”.",
             "s": "Take turns to [dangle] your magnet over the fish until one sticks.",
             "why": "To dangle the magnet is to let it hang down on its string and swing over the fish."},
            {"id": "80dcf3c9832f", "t": "mcq", "d": "structure", "q": "Why is the tip put at the end of the instructions?",
             "opts": ["to help if the game does not work", "to list what you need before you start",
                      "to explain how a player wins", "to say how many fish to draw"],
             "why": "The tip tells you what to check if a fish will not stick, so it helps fix a problem."},
        ],
    },
    {
        "key": "RD3.07",
        "year": 3,
        "strand": "Poems",
        "title": "My Bean",
        "nc": "Discuss words and phrases that capture the reader's interest and imagination",
        "text": "I pushed a bean into the soil,\n"
                "A pot of earth, a crumbly bed.\n"
                "I poured a little water in\n"
                "And whispered, “Wake up, sleepyhead.”\n\n"
                "For days the pot sat brown and bare.\n"
                "I thought my bean was fast asleep,\n"
                "But down below, where no one looked,\n"
                "A thin white root crept slow and deep.\n\n"
                "Then one bright morning, something green\n"
                "Came pushing up, bent like a hook.\n"
                "It straightened slowly in the sun,\n"
                "And Mum came running for a look.\n\n"
                "I put it on the windowsill\n"
                "Where all the morning sunshine lands.\n"
                "Each day it leaned towards the glass\n"
                "Like someone reaching out their hands.\n\n"
                "I kept the soil just damp, not soaked.\n"
                "I turned the pot to keep it straight.\n"
                "It climbed a cane up past my chin.\n"
                "It's worth it, learning how to wait.\n\n"
                "Nan says that soon it will have flowers,\n"
                "And after flowers, pods will grow.\n"
                "I'll save the fattest bean of all\n"
                "And next spring, have another go.",
        "qs": [
            {"id": "c4244755f148", "t": "mcq", "d": "retrieve", "q": "What did the poet do straight after pushing the bean into the soil?",
             "opts": ["poured in a little water", "put the pot on the windowsill", "tied the plant to a cane", "turned the pot round"],
             "why": "Verse 1 says: “I poured a little water in” straight after planting the bean."},
            {"id": "f3c50f635198", "t": "mcq", "d": "infer", "q": "In verse 2, why did the poet think the bean was “fast asleep”?",
             "opts": ["Nothing could be seen growing above the soil.", "The bean had been pushed in too deep.",
                      "The pot had been left in the dark.", "Mum had said it would never grow."],
             "why": "The pot sat “brown and bare”: the root was growing underground, where no one could see it."},
            {"id": "4c9782f46292", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you the colour of the root.",
             "s": "A thin [white] root crept slow and deep.",
             "why": "The root is described as thin and white."},
            {"id": "ea4525f37b70", "t": "mcq", "d": "language", "q": "“Like someone reaching out their hands.” What does this help you picture?",
             "opts": ["the plant leaning towards the light", "the plant falling over in the pot",
                      "the poet picking the beans", "Mum running to have a look"],
             "why": "The plant leaned towards the sunny glass, the way a person stretches out to reach something."},
            {"id": "ea90b046fd20", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the poem.",
             "items": ["A root grew down into the soil.", "A green hook pushed up.",
                       "The plant leaned towards the glass.", "The plant climbed a cane."],
             "why": "The poem follows the bean as it grows: root, shoot, leaning to the light, then climbing."},
            {"id": "da690aedbf2b", "t": "mcq", "d": "summarise", "q": "Which title would also suit this poem?",
             "opts": ["Growing Takes Care and Time", "The Bean That Never Grew", "Nan's Vegetable Garden", "A Morning in the Kitchen"],
             "why": "The poet waters, gives light, turns the pot and waits, and the bean grows tall: care and time."},
        ],
    },
    {
        "key": "RD3.08",
        "year": 3,
        "strand": "Information",
        "title": "Bones and muscles",
        "nc": "Retrieve and record information from non-fiction",
        "text": "If you had no skeleton, you would flop on the floor like a jelly. Your skeleton is the frame of bones inside your body. An adult's skeleton has 206 bones, from the long thigh bone in each leg to tiny bones deep inside each ear.\n\n"
                "Your skeleton has three important jobs. First, it supports your body and gives it its shape. Second, it protects the soft parts inside. Your skull is a hard case around your brain, and your ribs form a cage that guards your heart and lungs. Third, it helps you move.\n\n"
                "Bones cannot move on their own, though. They are moved by muscles, which are joined to the bones by strong cords called tendons. A muscle can only pull. It cannot push. So muscles often work in pairs.\n\n"
                "Try this. Bend your arm and feel the front of your upper arm. The muscle there, the biceps, has become shorter and fatter as it pulls your lower arm up. Now straighten your arm. This time the muscle at the back, the triceps, pulls your arm straight while the biceps relaxes.\n\n"
                "Not all animals have a skeleton inside them. A beetle has a hard case on the outside of its body instead, and a worm has no bones at all.\n\n"
                "To keep your bones and muscles strong, eat a healthy diet and stay active every day.",
        "qs": [
            {"id": "c65fc3d25086", "t": "mcq", "d": "language", "q": "Why does the writer begin by saying you would “flop on the floor like a jelly”?",
             "opts": ["to show in a fun way that the skeleton holds us up", "to warn that eating jelly is bad for bones",
                      "to explain how muscles pull on bones", "to describe how a worm moves"],
             "why": "A jelly has nothing firm inside it. The picture makes the reader see why we need a frame of bones."},
            {"id": "bb0305c08113", "t": "mcq", "d": "retrieve", "q": "Which part of the skeleton guards the heart and lungs?",
             "opts": ["the ribs", "the skull", "the thigh bones", "the tendons"],
             "why": "The second paragraph says the ribs form a cage that guards your heart and lungs."},
            {"id": "5783f9fce963", "t": "text", "d": "retrieve", "q": "What are the strong cords that join muscles to bones called? Find and copy one word.",
             "a": ["tendons", "tendon", "the tendons"],
             "why": "The third paragraph says muscles are joined to the bones by strong cords called tendons."},
            {"id": "23f9e949562f", "t": "tap", "d": "vocab", "q": "Tap the word that means “goes loose and stops pulling”.",
             "s": "This time the muscle at the back, the triceps, pulls your arm straight while the biceps [relaxes].",
             "why": "When the triceps pulls, the biceps relaxes: it goes loose and stops working."},
            {"id": "a176697b8264", "t": "mcq", "d": "compare", "q": "How is a beetle different from a person, according to the text?",
             "opts": ["Its hard case is on the outside.", "It has no muscles at all.",
                      "It has more bones than a person.", "It has a skull but no ribs."],
             "why": "The fifth paragraph says a beetle has a hard case on the outside of its body instead of a skeleton inside."},
            {"id": "347b0074277e", "t": "mcq", "d": "structure", "q": "Why does the writer use “First”, “Second” and “Third” in the second paragraph?",
             "opts": ["to list the skeleton's three jobs one by one", "to show the order in which bones grow",
                      "to count the bones in the arm", "to give the steps of an experiment"],
             "why": "The paragraph begins “Your skeleton has three important jobs”, then gives each job in turn."},
        ],
    },
    {
        "key": "RD3.09",
        "year": 3,
        "strand": "Letters and diaries",
        "title": "A day at Maiden Castle",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": "Tuesday 14th May\n\n"
                "Today our class went on a trip to Maiden Castle in Dorset. It isn't a castle with towers at all. It is an Iron Age hillfort, one of the biggest in Britain, and it is made of earth and grass.\n\n"
                "The coach parked at the bottom of the hill, and we could see huge green banks running all the way round the top, like giant steps. Mr Hussain told us that Iron Age people dug the ditches by hand and piled up the earth to make the banks. They had no diggers, only tools made of iron and wood. I can't even dig a hole for a tomato plant without getting tired!\n\n"
                "We climbed up through the winding entrance. Mr Hussain said it was made like that so that enemies couldn't charge straight in. At the top it was so windy that Freya's hat blew off and rolled into a ditch, and Mr Hussain had to scramble down to fetch it. Everyone cheered when he climbed back up with it.\n\n"
                "We ate our packed lunches looking out over the fields. I tried to imagine roundhouses with smoke curling out of their roofs, and children my age looking after the sheep.\n\n"
                "My legs are aching now, but it was the best trip ever. I want to go back with Dad and show him the entrance.",
        "qs": [
            {"id": "643101404de9", "t": "mcq", "d": "infer", "q": "Why does the writer say “It isn't a castle with towers at all”?",
             "opts": ["The name had made them expect a stone castle.", "The towers had all fallen down.",
                      "Mr Hussain would not let them see the towers.", "The towers were hidden by the banks."],
             "why": "“Castle” makes you think of stone towers, but Maiden Castle is made of earth and grass."},
            {"id": "4a249f292fb8", "t": "mcq", "d": "retrieve", "q": "According to Mr Hussain, why was the entrance made winding?",
             "opts": ["so enemies could not charge straight in", "so the sheep could not get out",
                      "so the wind could not blow through", "so the coach could drive to the top"],
             "why": "Mr Hussain said it was made like that so that enemies couldn't charge straight in."},
            {"id": "bc1aa3d78c1d", "t": "text", "d": "retrieve", "q": "Iron Age people had no diggers. Find and copy one material their tools were made of.",
             "a": ["iron", "wood", "the iron", "the wood"],
             "why": "The diary says their tools were made of iron and wood."},
            {"id": "445f4a2d344f", "t": "mcq", "d": "vocab", "q": "“Mr Hussain had to scramble down to fetch it.” What does “scramble” mean here?",
             "opts": ["climb quickly using hands and feet", "walk slowly along a path",
                      "slide down on his back", "jump down in one go"],
             "why": "The ditch was steep, so he had to clamber down quickly, using his hands as well as his feet."},
            {"id": "fe9cb8dad13c", "t": "mcq", "d": "infer", "q": "How did the class feel when Mr Hussain climbed back up?",
             "opts": ["pleased and amused", "worried and upset", "bored and tired", "cross and impatient"],
             "why": "Everyone cheered: they were glad he had rescued Freya's hat, and it was funny to watch."},
            {"id": "a1e7fb222787", "t": "mcq", "d": "purpose", "q": "Why has the writer written this text?",
             "opts": ["to record a day out and how it felt", "to persuade families to buy tickets",
                      "to explain how to dig a ditch", "to tell the story of an Iron Age child"],
             "why": "It is a diary: it has a date, tells what happened on the trip and says how the writer felt."},
        ],
    },
    {
        "key": "RD3.10",
        "year": 3,
        "strand": "Stories",
        "title": "Kenji lets go",
        "nc": "Predict what might happen from details stated and implied",
        "text": "Kenji was the only one in his class who still couldn't ride a bike. On Saturday, his big sister Aiko took the stabilisers off his bike and wheeled it to the long, flat path in the park.\n\n"
                "“I'll hold the back of the seat,” she said. “You just pedal and look ahead, not down at your feet.”\n\n"
                "Kenji wobbled off. The handlebars twisted left and right, and after a few metres he toppled sideways onto the grass. He sat there with green stains on his knees, and his lip trembled.\n\n"
                "“Everyone falls,” said Aiko. “I fell about fifty times when I was learning.”\n\n"
                "They tried again, and again. Each time, Kenji went a little further before he had to put his foot down. Aiko jogged beside him, puffing, holding the seat.\n\n"
                "After lunch, Kenji pushed off once more. The bike felt steadier now. He fixed his eyes on the big oak tree at the end of the path and pedalled hard towards it. “Keep holding!” he shouted.\n\n"
                "There was no answer.\n\n"
                "When he reached the tree, Kenji braked and turned round. Aiko was standing far back at the start of the path, waving both arms above her head.\n\n"
                "Kenji's mouth dropped open. Then he laughed, turned the bike round and rode all the way back to her by himself.",
        "qs": [
            {"id": "1543d26bbcc8", "t": "mcq", "d": "vocab", "q": "“Kenji wobbled off.” What does “wobbled” tell you about how he rode?",
             "opts": ["He moved unsteadily from side to side.", "He rode very fast.",
                      "He fell off straight away.", "He rode in a straight line."],
             "why": "Wobbling means rocking from side to side; the next sentence says the handlebars twisted left and right."},
            {"id": "472eed76305f", "t": "mcq", "d": "infer", "q": "After his fall, Kenji's lip trembled. How was he feeling?",
             "opts": ["upset and close to tears", "angry with Aiko", "excited to try again", "bored of the park"],
             "why": "A trembling lip is a sign that someone is about to cry. He had just fallen off."},
            {"id": "523fbab0acaa", "t": "text", "d": "retrieve", "q": "How many times did Aiko say she fell when she was learning? Type the number from the text.",
             "a": ["fifty", "about fifty", "50"],
             "why": "Aiko says, “I fell about fifty times when I was learning.”"},
            {"id": "7f3ebefa8d38", "t": "mcq", "d": "infer", "q": "Why was there no answer when Kenji shouted “Keep holding!”?",
             "opts": ["Aiko had let go and was far behind him.", "Aiko was cross that he kept falling.",
                      "Aiko had gone home for her lunch.", "Aiko was busy jogging beside him."],
             "why": "When Kenji turned round, Aiko was far back at the start of the path, so she had let go long before."},
            {"id": "d350433a8578", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Aiko took the stabilisers off.", "Kenji toppled onto the grass.", "Kenji had lunch.",
                       "Kenji pedalled towards the oak tree.", "Kenji rode back to Aiko by himself."],
             "why": "The fall came in the morning; after lunch he rode to the tree, then back on his own."},
            {"id": "8328a6199a94", "t": "mcq", "d": "predict", "q": "What is Kenji most likely to do next weekend?",
             "opts": ["ride his bike again without help", "ask for his stabilisers back",
                      "give his bike to Aiko", "stop going to the park"],
             "why": "He has just found out he can ride by himself, and he laughed with joy, so he will want to ride again."},
        ],
    },
    {
        "key": "RD3.11",
        "year": 3,
        "strand": "Information",
        "title": "Volcanoes and earthquakes",
        "nc": "Retrieve and record information from non-fiction",
        "text": "The ground under your feet feels solid, but the Earth is always on the move. Its outer layer, the crust, is cracked into huge pieces called plates. These plates fit together like a giant jigsaw, and they move very slowly, about as fast as your fingernails grow.\n\n"
                "Where two plates meet, they can push against each other, pull apart or slide past each other. Sometimes they get stuck. Pressure builds up until, suddenly, they jerk free. The ground shakes, and this is an earthquake. A strong earthquake can crack roads and knock down buildings.\n\n"
                "Deep underground, it is so hot that some rock melts. This melted rock is called magma. Where it finds a weak spot in the crust, it can rise to the surface and burst out. Once it is outside, it is called lava. Over many eruptions, layers of cooled lava and ash build up into a mountain: a volcano.\n\n"
                "Mount Etna, on the island of Sicily in Italy, is one of the most active volcanoes in Europe. Even so, farmers grow fruit on its lower slopes, because soil made from old volcanic ash is very rich.\n\n"
                "Most volcanoes and earthquakes happen near the edges of plates. Britain is far from a plate edge, so the earthquakes it has are small, and most are too weak for anyone to feel.",
        "qs": [
            {"id": "0b3d983a6374", "t": "mcq", "d": "vocab", "q": "In the first paragraph, what is the “crust”?",
             "opts": ["the Earth's outer layer", "the melted rock underground", "the edge where plates meet", "the top of a volcano"],
             "why": "The text says: “Its outer layer, the crust, is cracked into huge pieces called plates.”"},
            {"id": "d221859bed05", "t": "mcq", "d": "retrieve", "q": "According to the text, what causes an earthquake?",
             "opts": ["stuck plates suddenly jerking free", "lava bursting out of the ground",
                      "layers of ash building up", "rock melting deep underground"],
             "why": "The second paragraph says pressure builds up until the stuck plates jerk free, and the ground shakes."},
            {"id": "b6fb6bf35840", "t": "mcq", "d": "compare", "q": "What is the difference between magma and lava?",
             "opts": ["Magma is underground; lava has reached the surface.", "Magma is cold; lava is hot.",
                      "Magma is made of ash; lava is made of rock.", "Magma comes from earthquakes; lava comes from plates."],
             "why": "Both are melted rock. It is called magma underground and lava once it is outside."},
            {"id": "9b5a42985ad8", "t": "text", "d": "retrieve", "q": "Find and copy the name of the island where Mount Etna is.",
             "a": ["Sicily"],
             "why": "The fourth paragraph says Mount Etna is on the island of Sicily in Italy."},
            {"id": "ecc3c1c24774", "t": "mcq", "d": "retrieve", "q": "Why do farmers grow fruit near Mount Etna, even though it is an active volcano?",
             "opts": ["The soil there is very good for growing.", "The lava keeps the fruit warm.",
                      "There are no earthquakes in Sicily.", "The volcano never erupts any more."],
             "why": "The text says soil made from old volcanic ash is very rich, so the good harvest is worth the risk."},
            {"id": "4bf10b5fc52d", "t": "mcq", "d": "summarise", "q": "What is the last paragraph mainly about?",
             "opts": ["where volcanoes and earthquakes usually happen", "how lava cools into new rock",
                      "why Mount Etna is in Italy", "how to stay safe in an earthquake"],
             "why": "It says most happen near plate edges, and that Britain, far from one, has only small earthquakes."},
        ],
    },
    {
        "key": "RD3.12",
        "year": 3,
        "strand": "Explanations",
        "title": "A river's journey",
        "nc": "Identify main ideas drawn from more than one paragraph and summarise these",
        "text": "Every river starts somewhere, usually high in hills or mountains. This starting point is called the source. It might be a spring bubbling out of the ground, a boggy patch where rain collects, or melting snow.\n\n"
                "At first, the river is just a narrow stream. It rushes steeply downhill, tumbling over rocks. Because the water is fast, it carries stones and pebbles along, and these scrape away at the riverbed. Slowly, over thousands of years, the river cuts a deep valley shaped like a letter V.\n\n"
                "As it travels on, other streams join it. A stream that flows into a bigger river is called a tributary. With all this extra water, the river grows wider and deeper. The land becomes flatter, so the river slows down and starts to swing from side to side in big loops called meanders.\n\n"
                "Near the end of its journey, the river is wide and slow. It no longer has the strength to carry much, so it drops the fine mud it has been carrying. Finally, it reaches its mouth, where it flows into the sea or a lake.\n\n"
                "The longest river in the United Kingdom is the River Severn. Its source is in the hills of mid Wales. From there it flows through Shrewsbury, Worcester and Gloucester, before it reaches the sea at the Bristol Channel.",
        "qs": [
            {"id": "54485bbaf59a", "t": "text", "d": "retrieve", "q": "What is the starting point of a river called? Find and copy one word.",
             "a": ["source", "the source", "a source"],
             "why": "The first paragraph says: “This starting point is called the source.”"},
            {"id": "d37c19f35bee", "t": "mcq", "d": "retrieve", "q": "According to the text, what scrapes away at the riverbed near the start?",
             "opts": ["stones and pebbles carried by the fast water", "fine mud dropped by the slow water",
                      "melting snow from the mountains", "the big loops called meanders"],
             "why": "The second paragraph says the fast water carries stones and pebbles, and these scrape away at the riverbed."},
            {"id": "09036805b1fc", "t": "tap", "d": "vocab", "q": "Tap the special name for a stream that flows into a bigger river.",
             "s": "A stream that flows into a bigger river is called a [tributary].",
             "why": "A tributary is a smaller stream or river that joins a bigger one."},
            {"id": "0dc8bdc11a51", "t": "mcq", "d": "infer", "q": "Why does a river drop its mud near its mouth but not near its source?",
             "opts": ["Near the mouth it is slow, but near the source it is fast.", "There is no mud in the hills.",
                      "The sea pushes the mud back up the river.", "Tributaries take the mud away."],
             "why": "Fast water near the source can carry things along; slow water near the mouth is too weak, so the mud sinks."},
            {"id": "09e2a7dc3433", "t": "order", "d": "sequence", "q": "Put these in the order they happen on a river's journey.",
             "items": ["The river starts at its source.", "It rushes over rocks as a narrow stream.",
                       "Tributaries join it.", "It swings from side to side in meanders.", "It flows into the sea at its mouth."],
             "why": "The text follows the river from its source, downhill, through its meanders, to its mouth."},
            {"id": "45dc228eb321", "t": "mcq", "d": "structure", "q": "Why does the last paragraph describe the River Severn?",
             "opts": ["to give a real example of a river's journey", "to explain what a tributary is",
                      "to show that every river starts as snow", "to describe how a V-shaped valley forms"],
             "why": "After explaining how any river travels, the writer shows a real one, from its source in Wales to the sea."},
        ],
    },
    {
        "key": "RD3.13",
        "year": 3,
        "strand": "Letters and diaries",
        "title": "A letter to Grandad",
        "nc": "Ask questions to improve their understanding of a text",
        "text": "14 Ashgrove Road\nGlasgow\n\n"
                "Saturday\n\n"
                "Dear Grandad,\n\n"
                "Thank you for the recipe book you sent for my birthday. I have already used it! Mum let me cook dinner for the whole family last night, all by myself (well, nearly).\n\n"
                "At school we have learned that, unlike plants, humans can't make their own food, so we have to get the right nutrients from what we eat. Our teacher, Mr Byrne, showed us a plate split into sections. Carbohydrates, like rice and bread, give us energy. Protein, like fish, eggs and beans, helps our bodies grow and repair themselves. Fruit and vegetables give us vitamins and fibre. We only need a little fat and sugar.\n\n"
                "So I chose your chicken and chickpea curry, with brown rice and a big bowl of salad. I chopped the peppers very carefully, and Mum did the part with the hot oil. My brother Idris called the salad “rabbit food”, but he still had seconds!\n\n"
                "For pudding, we had sliced mango and yoghurt instead of cake. Dad said it was the best meal he'd had all week, and he didn't even have to wash up, because Idris did.\n\n"
                "Next time you visit, I will cook for you. Is there anything you don't like?\n\n"
                "Lots of love,\nZainab",
        "qs": [
            {"id": "1f9057ee2972", "t": "mcq", "d": "retrieve", "q": "What had Grandad sent Zainab for her birthday?",
             "opts": ["a recipe book", "a cooking pot", "a box of mangoes", "a plate split into sections"],
             "why": "The first line of the letter thanks Grandad for the recipe book. The plate was Mr Byrne's, at school."},
            {"id": "ba24abbf34fb", "t": "mcq", "d": "infer", "q": "Zainab says she cooked “all by myself (well, nearly)”. What do the words in brackets tell you?",
             "opts": ["She had a little help.", "The dinner was nearly burnt.",
                      "She nearly forgot to cook.", "Only some of the family ate."],
             "why": "Later she says Mum did the part with the hot oil, so she was not quite on her own."},
            {"id": "2c06f3773cb7", "t": "mcq", "d": "retrieve", "q": "According to Mr Byrne's plate, what does protein do?",
             "opts": ["helps our bodies grow and repair themselves", "gives us vitamins and fibre",
                      "gives us energy", "is needed only in small amounts"],
             "why": "The letter says protein, like fish, eggs and beans, helps our bodies grow and repair themselves."},
            {"id": "11ef78756902", "t": "tap", "d": "retrieve", "q": "Tap the food in this sentence that the letter names as a carbohydrate.",
             "s": "So I chose your chicken and chickpea curry, with brown [rice] and a big bowl of salad.",
             "why": "Rice is a carbohydrate, and the letter says carbohydrates give us energy."},
            {"id": "34754cdcaf22", "t": "mcq", "d": "infer", "q": "Idris called the salad “rabbit food”, but he still had seconds. What does this show?",
             "opts": ["He liked it more than he wanted to admit.", "He was still hungry for curry.",
                      "He wanted to feed it to a rabbit.", "He did not eat any salad at all."],
             "why": "He made fun of the salad, yet he came back for more: he must have enjoyed it."},
            {"id": "a5daac2abc49", "t": "mcq", "d": "purpose", "q": "Why did Zainab write this letter?",
             "opts": ["to thank Grandad and tell him how she used his gift", "to ask Grandad for another recipe book",
                      "to teach Grandad how to cook a curry", "to complain to Grandad about Idris"],
             "why": "She begins by thanking him for the recipe book, then tells him about the meal she cooked from it."},
        ],
    },
    {
        "key": "RD3.14",
        "year": 3,
        "strand": "Stories",
        "title": "The folded note",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "Every Saturday, Tunde helped his Aunty Bisi at her fruit stall in the busy market in Lagos. He stacked the oranges into neat pyramids, swept up fallen leaves and, best of all, was allowed to take the money.\n\n"
                "One hot morning, a tall woman in a blue headscarf bought six mangoes. She handed Tunde a folded note and hurried off into the crowd. When he unfolded it, his eyes widened. It was worth far more than six mangoes. She must have given him the wrong note by mistake.\n\n"
                "For a moment, Tunde thought about the football boots in the shop by the bus stop. Nobody had seen. Aunty Bisi was busy weighing yams for another customer.\n\n"
                "Then he remembered what she always said: “What is not yours is not yours, even when no one is looking.”\n\n"
                "“Aunty, I'll be back!” he called, and he squeezed between the stalls, past the fish sellers and the women selling cloth. At last, he spotted the blue headscarf near the spice stall.\n\n"
                "“Excuse me!” he panted. “You gave me the wrong note.”\n\n"
                "The woman stared at the note, then at him. She swapped it for the right one and pressed a small coin into his hand. “For being honest,” she said.\n\n"
                "When Tunde got back, Aunty Bisi had already heard the whole story from the cloth sellers. She didn't say a word. She just handed him the biggest, ripest mango on the stall.",
        "qs": [
            {"id": "9ea94a18f4a4", "t": "mcq", "d": "retrieve", "q": "Which job did Tunde like best at the stall?",
             "opts": ["taking the money", "stacking the oranges", "sweeping up leaves", "weighing the yams"],
             "why": "The first paragraph says “best of all, was allowed to take the money.” Aunty Bisi weighed the yams."},
            {"id": "869410c38e53", "t": "mcq", "d": "language", "q": "Why does the writer say that Tunde's “eyes widened”?",
             "opts": ["to show he was surprised", "to show he was sleepy", "to show he was cross", "to show the sun was bright"],
             "why": "Eyes open wide when someone gets a surprise: the note was worth far more than six mangoes."},
            {"id": "dbb504410431", "t": "mcq", "d": "infer", "q": "Why did Tunde think about the football boots?",
             "opts": ["He was tempted to keep the money to buy them.", "He had seen the woman near the shoe shop.",
                      "Aunty Bisi had promised to buy them.", "He needed boots to run through the market."],
             "why": "He thought of the boots just after noticing that nobody had seen: for a moment he was tempted."},
            {"id": "1a595db644b8", "t": "tap", "d": "vocab", "q": "Tap the word that means “said while breathing quickly and hard”.",
             "s": "“Excuse me!” he [panted].",
             "why": "Tunde had run through the market, so he was out of breath: he panted."},
            {"id": "3b11386409f5", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["A woman bought six mangoes.", "Tunde unfolded the note.", "Tunde remembered his aunt's words.",
                       "Tunde found the woman near the spice stall.", "Aunty Bisi gave Tunde a mango."],
             "why": "He saw the note, was tempted, remembered his aunt's saying, ran after the woman, then went back."},
            {"id": "a5947ea85f6b", "t": "mcq", "d": "infer", "q": "Why did Aunty Bisi give Tunde the biggest mango?",
             "opts": ["She was proud that he had been honest.", "It was too ripe to sell.",
                      "He had asked her for it.", "The woman had paid for it."],
             "why": "She had heard what he did, and the gift without a word shows she was proud of him."},
        ],
    },
]
