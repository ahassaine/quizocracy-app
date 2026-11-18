"""Reading comprehension, Year 5, second set (keys RD5.15-RD5.28): 14 passages of 250-380 words, 7 questions each.

Spec: app/bank/SPEC_READING.md (and SPEC.md for the question format). Every passage and question is
original writing, written by hand, on topics different from the first set (reading_y5.py). Topics link to
the Year 5 curriculum where natural: the planets of the Solar System, dissolving and separating mixtures, air
resistance, the Kingdom of Benin, the octopus; plus realistic stories set in Bristol, Kenya and Morocco, a
poem, a play script, a biography (Isaac Newton), a news report (swift nesting boxes), a persuasive article
(looking after hedgerows) and a letter from Tromsø in the Arctic polar night.

The questions mix the KS2 reading domains (retrieve, infer, vocab, sequence, summarise, structure,
language, compare, predict, purpose). To be checked line by line by a second reviewer (facts, one
defensible answer per question, no leaks) before scripts/bank_ids.py gives the questions their ids.
"""

SKILLS = [
    {
        "key": "RD5.15",
        "year": 5,
        "strand": "Stories",
        "title": "The puncture",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "On Saturday morning, Tomasz wheeled his bike out of the shed and groaned. The back tyre was completely "
            "flat. The cycle ride along the river with Jamal and Owen started at ten o'clock, and it was already "
            "half past eight.\n\n"
            "\"Dziadek!\" he called. His grandfather, who had lived with them since the summer, looked up from his "
            "newspaper at the kitchen table. \"Can you fix my tyre? Please? I'm going to be late.\"\n\n"
            "Dziadek came out, crouched beside the bike and squeezed the tyre between his finger and thumb. \"I can "
            "show you,\" he said. \"But your hands will do the work. When I was your age in Gdańsk, nobody mended "
            "my bike for me.\"\n\n"
            "Tomasz sighed, but he fetched the repair kit from the shelf. Dziadek showed him how to lever the tyre "
            "off the wheel with two plastic levers and pull out the inner tube. Then he pumped a little air into "
            "the tube and held it next to Tomasz's ear. There was a faint hiss, as quiet as a whisper.\n\n"
            "Tomasz found the tiny hole, spread glue around it and pressed the patch on straight away. When he "
            "pumped the tube up, the hiss came back.\n\n"
            "\"Too fast,\" said Dziadek. \"The glue must dry until it is no longer shiny. Patience is part of the "
            "repair.\"\n\n"
            "Tomasz wanted to throw the pump across the garden. Instead, he peeled off the patch, rubbed the "
            "rubber with the little square of sandpaper from the kit and spread fresh glue. This time he counted "
            "slowly to a hundred before pressing the patch down, and he held it there for a whole minute.\n\n"
            "The tube stayed firm. Together they fitted it back inside the tyre and pumped it up until it was "
            "hard.\n\n"
            "At five to ten, Tomasz skidded to a stop beside his friends at the bridge. Owen was kneeling by his "
            "own bike, staring miserably at a soft front tyre.\n\n"
            "Tomasz grinned and opened his bag. \"Don't worry,\" he said. \"I've brought the repair kit, and I know "
            "exactly what to do.\""
        ),
        "qs": [
            {"id": "79e4464996d5", "t": "text", "d": "retrieve", "q": "At what time did the cycle ride start? Find and copy the words.",
             "a": ["ten o'clock", "10 o'clock", "ten", "10", "10:00", "10am", "10 am"],
             "why": "The first paragraph says the ride along the river started at ten o'clock."},
            {"id": "475fd2d155c3", "t": "mcq", "d": "infer", "q": "Why did Dziadek make Tomasz do the repair himself?",
             "opts": ["He wanted Tomasz to learn how to mend a bike on his own.",
                      "He did not know how to mend a puncture himself.",
                      "He wanted to finish reading his newspaper first.",
                      "His fingers were too stiff to hold the tyre levers."],
             "no": {"He did not know how to mend a puncture himself.": "Dziadek shows Tomasz every step and knows why the first patch failed, so he does know how."},
             "why": "\"Your hands will do the work\": Dziadek knows how, but he wants Tomasz to learn, as he had to at that age."},
            {"id": "14b99892a3eb", "t": "tap", "d": "vocab", "q": "Tap the word that means \"bent down low with his knees bent\".",
             "s": "Dziadek came out, [crouched] beside the bike and squeezed the tyre between his finger and thumb.",
             "why": "To crouch is to bend your knees and lower your body, as Dziadek does to look at the tyre."},
            {"id": "3a785ceb52a2", "t": "mcq", "d": "language", "q": "Why does the writer say the hiss was \"as quiet as a whisper\"?",
             "opts": ["to show the hole was tiny and the leak was hard to hear",
                      "to show that Dziadek was speaking very softly",
                      "to show that the tube had burst with a loud bang",
                      "to show that Tomasz could not hear well"],
             "why": "A whisper is a very quiet sound: the air was escaping slowly through a tiny hole."},
            {"id": "6b2374d7de20", "t": "mcq", "d": "retrieve", "q": "Why did Tomasz's first patch not work?",
             "opts": ["He pressed it on before the glue had dried.",
                      "He put it on the wrong part of the tube.",
                      "He forgot to spread any glue at all.",
                      "He pumped the tube up far too hard."],
             "why": "He pressed the patch on \"straight away\", and Dziadek says the glue must dry until it is no longer shiny."},
            {"id": "61983868dba7", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the story.",
             "items": ["Tomasz finds that his back tyre is flat.",
                       "Dziadek says Tomasz must do the work himself.",
                       "The first patch fails and the hiss comes back.",
                       "Tomasz rubs the tube with sandpaper and uses fresh glue.",
                       "Tomasz meets his friends at the bridge."],
             "why": "The flat tyre comes first, then Dziadek's rule, the failed patch, the careful second try, and last the bridge."},
            {"id": "a2656e75211e", "t": "mcq", "d": "infer", "q": "How does Tomasz feel when he sees Owen's soft tyre at the bridge?",
             "opts": ["confident, because he now knows how to mend it",
                      "worried, because they will now be late for the ride",
                      "annoyed, because Owen did not check his bike",
                      "nervous, because he has never mended a tyre"],
             "no": {"nervous, because he has never mended a tyre": "He has just mended his own tyre that morning."},
             "why": "He grins and says, \"I know exactly what to do\": after mending his own tyre, he feels sure of himself."},
            {"id": "5268b849206a", "t": "mcq", "d": "summarise", "q": "What is the main message of the story?",
             "opts": ["Being patient and doing a job yourself means you can help others too.",
                      "It is always best to ask an adult to fix things for you.",
                      "Cycling by a river is more fun than any other sport.",
                      "Old bikes break too often and should be replaced."],
             "why": "Tomasz learns patience by mending the tyre himself, and at the end he can help Owen with his."},
        ],
    },
    {
        "key": "RD5.16",
        "year": 5,
        "strand": "Information",
        "title": "Eight planets and the Sun",
        "nc": "Retrieve, record and present information from non-fiction",
        "text": (
            "Our Sun is a star: a huge, glowing ball of hot gas. Travelling around it, each on its own path called "
            "an orbit, are eight planets. Unlike the Sun, the planets do not make any light of their own. We can "
            "see them in the night sky only because sunlight bounces off them.\n\n"
            "The four planets closest to the Sun are Mercury, Venus, Earth and Mars. They are fairly small and "
            "made of rock, with solid ground that you could stand on.\n\n"
            "Mercury is the smallest planet and the closest to the Sun. You might expect it to be the hottest, but "
            "it is not. That record belongs to Venus, the second planet. Venus is wrapped in thick clouds that "
            "trap the Sun's heat like a blanket, so its surface is hot enough to melt lead.\n\n"
            "Earth comes third. As far as we know, it is the only planet where anything lives. Next comes Mars, "
            "often called the Red Planet, because its dusty ground contains iron that has rusted.\n\n"
            "Beyond Mars lie the four giant planets: Jupiter, Saturn, Uranus and Neptune. They are made mostly of "
            "gas, or of gas and ice, and they have no solid surface to land on. Jupiter is the largest planet of "
            "all: more than a thousand Earths could fit inside it. Saturn is famous for its bright rings, which "
            "are made of countless pieces of ice and rock. Uranus and Neptune, the farthest away, are freezing "
            "cold, bluish worlds.\n\n"
            "The farther a planet is from the Sun, the longer its journey round the Sun takes. Earth takes just "
            "over 365 days, which is one year. Neptune takes about 165 Earth years, so it has been round the Sun "
            "only once since it was discovered in 1846.\n\n"
            "For many years, Pluto was called the ninth planet. Then, in 2006, scientists agreed on a new meaning "
            "of the word \"planet\". Pluto, which is very small, did not fit it, and it is now called a dwarf "
            "planet."
        ),
        "qs": [
            {"id": "ab67be5eb436", "t": "mcq", "d": "retrieve", "q": "According to the text, why can we see the planets in the night sky?",
             "opts": ["Sunlight bounces off them.",
                      "They glow with their own light.",
                      "They are made of glowing gas.",
                      "They are closer to us than the Moon."],
             "no": {"They glow with their own light.": "The first paragraph says the planets do not make any light of their own, unlike the Sun."},
             "why": "The first paragraph says we see them \"only because sunlight bounces off them\"."},
            {"id": "391b79acab23", "t": "tap", "d": "vocab", "q": "Tap the word that names the path a planet travels around the Sun.",
             "s": "Travelling around it, each on its own path called an [orbit], are eight planets.",
             "why": "The first paragraph says each planet travels on its own path \"called an orbit\"."},
            {"id": "237cbab65c9c", "t": "mcq", "d": "infer", "q": "Venus is farther from the Sun than Mercury. Why is Venus still the hotter planet?",
             "opts": ["Its thick clouds trap the Sun's heat.",
                      "It is the largest of the rocky planets.",
                      "Its rusty ground soaks up the sunlight.",
                      "Mercury is shaded from the Sun by Venus."],
             "no": {"Its rusty ground soaks up the sunlight.": "Rusty ground is how the text describes Mars, not Venus."},
             "why": "The third paragraph says Venus's clouds \"trap the Sun's heat like a blanket\", so its surface is hotter than Mercury's."},
            {"id": "f8b31a5846b4", "t": "mcq", "d": "compare", "q": "How are the four planets closest to the Sun different from the four giant planets?",
             "opts": ["They are small and rocky; the giants are mostly gas, or gas and ice.",
                      "They are cold and bluish; the giants are hot and red.",
                      "They all have rings; the giants have no rings at all.",
                      "They take longer to go round the Sun than the giants do."],
             "why": "The second paragraph says the closest four are small and made of rock; the fifth says the giants are mostly gas, or gas and ice."},
            {"id": "a3ed11a0eac9", "t": "mcq", "d": "infer", "q": "Neptune has been round the Sun only once since 1846. What explains this, according to the text?",
             "opts": ["Each of its journeys round the Sun takes about 165 years.",
                      "It travels round the Sun much faster than Earth does.",
                      "It was only discovered a few years ago.",
                      "It stopped moving for a long time after it was found."],
             "why": "The sixth paragraph says the farther a planet is, the longer its journey takes, and Neptune's takes about 165 Earth years."},
            {"id": "f8d3ec4f0013", "t": "text", "d": "retrieve", "q": "In which year did scientists agree on the new meaning of \"planet\"? Find and copy the year.",
             "a": ["2006", "in 2006"],
             "no": {"1846": "1846 is the year Neptune was discovered."},
             "why": "The last paragraph says the new meaning was agreed in 2006, and Pluto became a dwarf planet."},
            {"id": "e6a4014bd723", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the whole text?",
             "opts": ["It describes the eight planets that travel round the Sun and how they differ.",
                      "It explains why Pluto is no longer called a planet.",
                      "It tells the story of how Neptune was first discovered.",
                      "It shows why Venus is the hottest place in space."],
             "why": "Most of the text goes through the planets one group at a time; Pluto and Neptune are only small parts of it."},
        ],
    },
    {
        "key": "RD5.17",
        "year": 5,
        "strand": "Explanations",
        "title": "Where does the sugar go?",
        "nc": "Explain and discuss their understanding of what they have read; retrieve information from non-fiction",
        "text": (
            "Stir a spoonful of sugar into a glass of warm water, and after a minute or so it seems to vanish. "
            "The water looks just as clear as before. But take a sip and you will taste that the sugar is still "
            "there. So where has it gone?\n\n"
            "When sugar dissolves, it breaks up into pieces far too small to see, even with a magnifying glass. "
            "These tiny pieces spread out evenly through the water. The clear liquid you are left with is called "
            "a solution. A material that dissolves in water, like sugar or salt, is described as soluble. A "
            "material that does not dissolve, like sand or chalk, is insoluble: however long you stir it, it will "
            "stay as grains that sink to the bottom.\n\n"
            "Warm water usually dissolves sugar faster than cold water does. Stirring helps too, because it "
            "keeps moving fresh water past the sugar. But there is a limit. If you keep adding sugar to the same "
            "glass, the water will reach a point where it cannot dissolve any more, and the extra sugar will lie "
            "at the bottom however hard you stir.\n\n"
            "Can you get a dissolved material back? Yes, you can. Pour some salty water into a shallow dish and "
            "leave it in a warm, sunny place. Over a few days, the water evaporates into the air, but the salt "
            "cannot. It is left behind in the dish as small white crystals. In some hot countries, sea salt is "
            "made in just this way, in wide, shallow pools beside the sea.\n\n"
            "An insoluble material is even easier to separate. To take sand out of water, pour the mixture "
            "through filter paper. The water trickles through the tiny holes in the paper, but the grains of sand "
            "are too big to pass and stay behind.\n\n"
            "Because the salt and sand can be recovered, dissolving and mixing are called reversible changes. "
            "Baking a cake is different. Once the eggs, flour and sugar have been baked, no amount of filtering "
            "or evaporating will turn them back into what they were."
        ),
        "qs": [
            {"id": "d45fd3eb08b7", "t": "mcq", "d": "infer", "q": "In the first paragraph, how can you tell that the sugar has not really vanished?",
             "opts": ["The water still tastes sweet.",
                      "The water turns cloudy and white.",
                      "The sugar sinks to the bottom.",
                      "The water bubbles and fizzes."],
             "why": "\"Take a sip and you will taste that the sugar is still there\": the sweet taste shows it is still in the water."},
            {"id": "abb4eb3f5d25", "t": "text", "d": "retrieve", "q": "What is the clear liquid called when sugar has dissolved in water? Find and copy one word.",
             "a": ["solution", "a solution"],
             "why": "The second paragraph says the clear liquid you are left with \"is called a solution\"."},
            {"id": "e341c0b9a9d9", "t": "mcq", "d": "vocab", "q": "What does \"insoluble\" mean, as it is used in the second paragraph?",
             "opts": ["does not dissolve in water",
                      "dissolves very quickly in water",
                      "is too small to be seen",
                      "turns water a different colour"],
             "why": "The text says a material that does not dissolve, like sand, \"is insoluble\"."},
            {"id": "36f1f0a0f90b", "t": "mcq", "d": "retrieve", "q": "According to the text, why does stirring help sugar to dissolve?",
             "opts": ["It keeps moving fresh water past the sugar.",
                      "It makes the water much warmer.",
                      "It breaks the glass into smaller pieces.",
                      "It lets more air into the water."],
             "why": "The third paragraph says stirring helps \"because it keeps moving fresh water past the sugar\"."},
            {"id": "d970bffa8ff7", "t": "tap", "d": "retrieve", "q": "Tap the word that names the process that takes the water away and leaves the salt behind.",
             "s": "Over a few days, the water [evaporates] into the air, but the salt cannot.",
             "why": "The water evaporates into the air; the salt cannot, so it stays in the dish."},
            {"id": "ec20e0791a90", "t": "mcq", "d": "compare", "q": "How is getting back salt different from getting back sand, according to the text?",
             "opts": ["Salt is left when the water evaporates; sand is caught by filter paper.",
                      "Salt is caught by filter paper; sand is left when the water evaporates.",
                      "Salt can never be got back; sand can always be got back.",
                      "Salt needs cold water to separate; sand needs warm water."],
             "why": "The fourth paragraph uses evaporating to get the salt back; the fifth uses filter paper for the sand."},
            {"id": "1d56a6367278", "t": "mcq", "d": "structure", "q": "Why does the writer end with the example of baking a cake?",
             "opts": ["to show a change that cannot be reversed, unlike dissolving",
                      "to give a recipe that uses sugar and salt",
                      "to show that sugar dissolves faster in a cake",
                      "to explain how filter paper is made"],
             "why": "The last paragraph says dissolving is reversible, then gives baking as a change that cannot be undone: a contrast."},
        ],
    },
    {
        "key": "RD5.18",
        "year": 5,
        "strand": "Instructions",
        "title": "Test a parachute",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "Why does a parachute fall so slowly? In this investigation you will build two small parachutes of "
            "different sizes and find out which one takes longer to reach the ground.\n\n"
            "You will need: a plastic carrier bag, a ruler, scissors, string, two paper clips, a lump of modelling "
            "clay, a stopwatch and a partner.\n\n"
            "1. Cut a square 30 centimetres long on each side from the plastic bag. This is the canopy.\n"
            "2. Cut four pieces of string, each 30 centimetres long, and tie one to each corner of the canopy.\n"
            "3. Hold the four loose ends together, check that the strings are all the same length, and tie them in "
            "a knot.\n"
            "4. Press half of the modelling clay onto a paper clip and hook the clip through the knot. This is "
            "your load.\n"
            "5. Make a second parachute in the same way, but with a canopy only 15 centimetres on each side. Use "
            "the rest of the clay, so that both loads weigh the same.\n"
            "6. Ask an adult to stand on a safe, steady step and hold the first parachute out at arm's length. "
            "Your partner says \"Go!\", the parachute is dropped, and you time how long it takes to land.\n"
            "7. Repeat the drop three times and write down each time. Then do the same with the second "
            "parachute, dropped by the same person from the same height.\n\n"
            "What is happening? As the parachute falls, gravity pulls it down towards the Earth. At the same time, "
            "the air underneath pushes up against the canopy. This push is called air resistance. A bigger canopy "
            "meets more air, so there is more air resistance to slow it down.\n\n"
            "Why must you use the same load, the same height and the same person each time? In a fair test, you "
            "change only one thing, here the size of the canopy, and keep everything else the same. Then, if one "
            "parachute falls more slowly, you can be sure that the size of its canopy is the reason.\n\n"
            "Finally, look at your results. Were your three times for each parachute close together? If one time "
            "is very different from the others, a mistake may have been made, so test that parachute again."
        ),
        "qs": [
            {"id": "0a79f63b9be7", "t": "text", "d": "retrieve", "q": "What is the square of plastic called in these instructions? Find and copy one word.",
             "a": ["canopy", "the canopy"],
             "why": "Step 1 says of the plastic square: \"This is the canopy.\""},
            {"id": "5c36c3dd7c9f", "t": "mcq", "d": "structure", "q": "Why are the steps numbered?",
             "opts": ["so that the reader does each step in the right order",
                      "to show how many parachutes the reader must make",
                      "to show how many centimetres each piece should be",
                      "so that the reader can choose which steps to skip"],
             "why": "Instructions are numbered because the order matters: you cannot tie the knot before the strings are on."},
            {"id": "257056db79b8", "t": "mcq", "d": "infer", "q": "Why does step 5 say to use the rest of the clay for the second load?",
             "opts": ["so that both parachutes carry the same weight",
                      "so that the second parachute falls much faster",
                      "so that no modelling clay is wasted afterwards",
                      "so that the smaller canopy does not tear"],
             "why": "Step 5 says \"so that both loads weigh the same\": half the clay each keeps the test fair."},
            {"id": "af3acd87cbc0", "t": "order", "d": "sequence", "q": "Put these steps in the order the instructions give them.",
             "items": ["Cut a square from the plastic bag.",
                       "Tie a piece of string to each corner.",
                       "Hook the clip with the clay through the knot.",
                       "Make a second, smaller parachute.",
                       "Time each parachute as it is dropped."],
             "why": "The canopy is cut (step 1), then the strings tied (2), the load added (4), the second parachute made (5), and the drops timed (6 and 7)."},
            {"id": "cbc9e0317ba9", "t": "tap", "d": "vocab", "q": "Tap the two words that name the push of the air against the canopy.",
             "s": "This push is called [air] [resistance].",
             "why": "The text says the air pushing up against the canopy \"is called air resistance\"."},
            {"id": "12fb96919b56", "t": "mcq", "d": "predict", "q": "If you follow the instructions carefully, which result should you expect?",
             "opts": ["The parachute with the bigger canopy takes longer to land.",
                      "The parachute with the smaller canopy takes longer to land.",
                      "Both parachutes land at exactly the same moment.",
                      "Neither parachute opens, because the loads are too heavy."],
             "why": "A bigger canopy meets more air, so there is more air resistance to slow it down: it should fall more slowly."},
            {"id": "2220894a12ff", "t": "mcq", "d": "purpose", "q": "What is the main purpose of the paragraph that begins \"Why must you use the same load\"?",
             "opts": ["to explain what makes the test fair",
                      "to explain how to tie the strings",
                      "to tell the reader to buy a stopwatch",
                      "to describe what gravity is"],
             "why": "It explains a fair test: change only the size of the canopy and keep everything else the same."},
        ],
    },
    {
        "key": "RD5.19",
        "year": 5,
        "strand": "Biography",
        "title": "Isaac Newton",
        "nc": "Retrieve, record and present information from non-fiction; summarise the main ideas",
        "text": (
            "Isaac Newton was born in 1642 in a farmhouse at Woolsthorpe, in Lincolnshire. His father had died a "
            "few months before he was born. When Isaac was three, his mother married again and moved away, and "
            "he was brought up by his grandmother.\n\n"
            "At school in the nearby town of Grantham, Isaac was more interested in making things than in his "
            "lessons. He built model windmills, kites and sundials, and he filled his notebooks with drawings. "
            "When he was a teenager, his mother brought him home to run the family farm, but he was much happier "
            "reading than looking after the animals. In the end, his old headmaster persuaded her to send him to "
            "university instead.\n\n"
            "In 1661 Newton went to Cambridge University. Four years later, a deadly disease called the plague "
            "spread through England, and the university closed. Newton went back to Woolsthorpe, and there, "
            "working alone, he began some of his greatest discoveries.\n\n"
            "One was about light. Newton passed a beam of sunlight through a triangular piece of glass called a "
            "prism. The light spread out into a band of colours, like a rainbow. He showed that white light is "
            "really a mixture of all these colours.\n\n"
            "Another was about gravity. Newton later said that the idea came to him when he saw an apple fall "
            "from a tree. He wondered whether the same pull that brought the apple down to the ground could reach "
            "all the way up to the Moon. He worked out that it did: the force of gravity keeps the Moon in its "
            "path around the Earth, and the planets in their paths around the Sun.\n\n"
            "In 1687 Newton published a famous book that set out his laws of motion, which explain how things "
            "move when forces push or pull on them. He also built a new kind of telescope that used a curved "
            "mirror instead of lenses.\n\n"
            "Later in life, Newton moved to London, where he was put in charge of the Royal Mint, the place that "
            "made the country's coins. He died in 1727. Today, the unit that scientists use to measure force, "
            "the newton, is named after him."
        ),
        "qs": [
            {"id": "28ec592cebe0", "t": "text", "d": "retrieve", "q": "Who brought Isaac up after his mother moved away? Find and copy the words.",
             "a": ["his grandmother", "grandmother", "by his grandmother", "his gran"],
             "why": "The first paragraph says that when his mother moved away, \"he was brought up by his grandmother\"."},
            {"id": "e3e238abe8e1", "t": "mcq", "d": "infer", "q": "What do the model windmills, kites and sundials suggest about the young Isaac?",
             "opts": ["He was curious about how things worked and liked to build them.",
                      "He was the best pupil in his class at all his lessons.",
                      "He wanted to become a farmer like the rest of his family.",
                      "He was bored because his school had no books to read."],
             "no": {"He was the best pupil in his class at all his lessons.": "The text says he was more interested in making things than in his lessons."},
             "why": "Building working models and filling notebooks with drawings show a boy who wanted to know how things worked."},
            {"id": "ef300b1d7bff", "t": "mcq", "d": "retrieve", "q": "Why did Newton leave Cambridge and go back to Woolsthorpe?",
             "opts": ["The university closed because of the plague.",
                      "His mother needed him to run the family farm.",
                      "He had finished all his studies at the university.",
                      "He wanted to build windmills near his home."],
             "no": {"His mother needed him to run the family farm.": "That happened earlier, when he was a teenager, before he went to university."},
             "why": "The third paragraph says the plague spread through England \"and the university closed\"."},
            {"id": "95a6a164db8c", "t": "tap", "d": "vocab", "q": "Tap the word that names the triangular piece of glass.",
             "s": "Newton passed a beam of sunlight through a triangular piece of glass called a [prism].",
             "why": "The fourth paragraph says the triangular piece of glass is \"called a prism\"."},
            {"id": "199695af7655", "t": "mcq", "d": "retrieve", "q": "According to the text, what did Newton work out about the pull that brings an apple down?",
             "opts": ["The same pull also keeps the Moon in its path around the Earth.",
                      "It only works on things that grow on trees.",
                      "It stops working a little way above the ground.",
                      "It is the same as the light that comes from the Sun."],
             "why": "The fifth paragraph says the force of gravity reaches the Moon and \"keeps the Moon in its path around the Earth\"."},
            {"id": "1d8dc308cc0f", "t": "order", "d": "sequence", "q": "Put these events from Newton's life in the order they happened.",
             "items": ["He is brought up by his grandmother.",
                       "He builds model windmills at school in Grantham.",
                       "He goes to Cambridge University.",
                       "He goes back to Woolsthorpe when the plague spreads.",
                       "He is put in charge of the Royal Mint."],
             "why": "The text follows his life in order: childhood with his grandmother, school, Cambridge in 1661, the plague four years later, and London later in life."},
            {"id": "e87e7a261848", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the whole text?",
             "opts": ["A farm boy who loved making things grew up to make great discoveries about light, gravity and motion.",
                      "A farmer discovered gravity when an apple fell on his head while he was working.",
                      "A boy from Lincolnshire spent his whole life making coins at the Royal Mint.",
                      "A schoolboy became famous for building windmills, kites and sundials."],
             "no": {"A farmer discovered gravity when an apple fell on his head while he was working.": "The text says he saw an apple fall from a tree, and he was much happier reading than farming."},
             "why": "The text follows his life from the farm to his discoveries about light, gravity and motion, which are still used today."},
        ],
    },
    {
        "key": "RD5.20",
        "year": 5,
        "strand": "Stories",
        "title": "Save something for the hill",
        "nc": "Draw inferences and justify them with evidence; predict what might happen from details stated and implied",
        "text": (
            "The morning of the inter-school race was cool and bright. Mist still hung over the valley below "
            "Chebet's village in the Kenyan highlands, and the red dirt road was hard from the night's cold.\n\n"
            "Her cousin Kiprop walked with her to the start. He was sixteen and had run for the county, and "
            "Chebet listened to everything he said as if it were written in a book. \"Remember,\" he told her, "
            "\"the last part is all uphill. Don't spend everything at the beginning. Save something for the "
            "hill.\"\n\n"
            "Chebet nodded. But when the whistle blew, forty girls burst forward at once, elbows out, feet "
            "drumming on the road, and Chebet forgot every word. She shot to the front. For the first kilometre "
            "she led the whole race, and she could hear people cheering her name from the roadside.\n\n"
            "Then her legs began to feel like wet sand. Her breath came in short, painful gasps. One girl passed "
            "her, then another, then three together, their footsteps fading ahead. By the time the road began "
            "to climb, Chebet was ninth, and she wanted nothing more than to stop and sit down in the grass.\n\n"
            "Save something for the hill.\n\n"
            "It was too late for that, she thought. Then she noticed that the girls ahead were slowing too. "
            "Their heads were down and their arms were swinging wildly. Chebet made herself breathe slowly, in "
            "through her nose and out through her mouth. She shortened her stride, the way Kiprop did on steep "
            "ground, and fixed her eyes on the back of the runner in front.\n\n"
            "One by one, she caught them. Eighth. Sixth. Fourth. At the top of the hill, with the finish "
            "flags flapping, there were only two runners ahead of her. She passed one of them a few strides "
            "from the line.\n\n"
            "Kiprop was waiting with a bottle of water. \"Second,\" he said. \"Not bad for someone who tried to "
            "win the race in the first kilometre.\"\n\n"
            "Chebet laughed, still out of breath. \"Next time,\" she said, \"I'll listen all the way to the end.\""
        ),
        "qs": [
            {"id": "bfd4ed437072", "t": "mcq", "d": "infer", "q": "What does \"as if it were written in a book\" tell us about how Chebet felt about Kiprop's advice?",
             "opts": ["She trusted it completely.",
                      "She found it boring to listen to.",
                      "She thought it was old-fashioned.",
                      "She wanted to write it down later."],
             "why": "She \"listened to everything he said\" as if it were in a book: she treated his words as true and important."},
            {"id": "1cd12bb97d8b", "t": "mcq", "d": "retrieve", "q": "What did Kiprop warn Chebet about before the race?",
             "opts": ["The last part of the race was all uphill.",
                      "The road would be muddy after the rain.",
                      "Forty girls would try to push her over.",
                      "The race was much longer than last year."],
             "why": "He told her \"the last part is all uphill\" and to save something for the hill."},
            {"id": "7ff1f070f0d5", "t": "tap", "d": "vocab", "q": "Tap the word that shows how suddenly and fast Chebet set off.",
             "s": "She [shot] to the front.",
             "why": "\"Shot\" here means moved suddenly and very fast: she set off far too quickly."},
            {"id": "5e58d559f6af", "t": "mcq", "d": "language", "q": "\"Her legs began to feel like wet sand.\" What does this comparison suggest?",
             "opts": ["Her legs felt heavy and weak.",
                      "Her legs were covered in mud.",
                      "Her legs felt cold from the morning.",
                      "Her legs were hurt by a fall."],
             "why": "Wet sand is heavy and gives way: her tired legs felt the same after starting too fast."},
            {"id": "70f7e1cd9e18", "t": "mcq", "d": "structure", "q": "Why does the writer put \"Save something for the hill.\" on a line of its own in the middle of the race?",
             "opts": ["to show Kiprop's words coming back into Chebet's mind",
                      "to show Kiprop shouting from the side of the road",
                      "to show the words were written on a sign by the hill",
                      "to show Chebet saying the words aloud to the other girls"],
             "why": "The next line says \"It was too late for that, she thought\": she is remembering his advice, not hearing it."},
            {"id": "18709dc1b3bb", "t": "text", "d": "retrieve", "q": "In what position did Chebet finish the race? Find and copy the word Kiprop uses.",
             "a": ["second", "2nd"],
             "why": "Kiprop says \"Second,\" when he meets her at the finish."},
            {"id": "0b7cd42d260d", "t": "mcq", "d": "infer", "q": "What has Chebet learned by the end of the story?",
             "opts": ["to pace herself and keep some strength for the end",
                      "that she will never be fast enough to win a race",
                      "that running uphill is easier than running on flat ground",
                      "to ignore her cousin and run the way she likes"],
             "no": {"that she will never be fast enough to win a race": "She came second after a bad start, and she says \"Next time\": she plans to do better."},
             "why": "She says she will \"listen all the way to the end\" next time: she knows she started too fast and must save some strength."},
        ],
    },
    {
        "key": "RD5.21",
        "year": 5,
        "strand": "Poems",
        "title": "Rock pool at low tide",
        "nc": "Discuss and evaluate how authors use language, including figurative language, considering the impact on the reader",
        "text": (
            "When the tide pulls back its silver sheet\n"
            "and the bay lies bare and wide,\n"
            "I pick my way across the rocks\n"
            "to the pools it leaves behind.\n\n"
            "The weed lies flat like dripping hair,\n"
            "the limpets clamp down tight,\n"
            "and barnacles have closed their doors\n"
            "to keep the sea inside.\n\n"
            "I kneel beside the deepest pool\n"
            "and hold my shadow back,\n"
            "for crabs can feel a shadow fall\n"
            "and vanish through a crack.\n\n"
            "I wait. The ripples smooth away.\n"
            "The water clears like glass.\n"
            "A shrimp as thin as cotton thread\n"
            "goes flicking quickly past.\n\n"
            "An anemone, a blob of jam,\n"
            "unfolds its crimson crown,\n"
            "and waves its arms to catch the food\n"
            "the tide has carried down.\n\n"
            "A little fish with bulging eyes\n"
            "peers out from under a stone,\n"
            "then darts away, as if to say,\n"
            "\"This pool is mine. Go home.\"\n\n"
            "A starfish, orange as a flame,\n"
            "is pressed against the wall,\n"
            "so still it might be painted there\n"
            "and not alive at all.\n\n"
            "I lift one rock, then set it down\n"
            "exactly where it lay,\n"
            "for underneath, a dozen lives\n"
            "were sheltering from the day.\n\n"
            "The sun is warm upon my back,\n"
            "the minutes slip away,\n"
            "until a wave comes slapping in\n"
            "and showers me with spray.\n\n"
            "The tide is turning. Pool by pool,\n"
            "the sea is coming home,\n"
            "and all the tiny worlds I watched\n"
            "are joined beneath the foam.\n\n"
            "I climb back up the shingle path\n"
            "with salt upon my skin,\n"
            "and look back at the hidden town\n"
            "the tide has gathered in."
        ),
        "qs": [
            {"id": "c5584d581d7b", "t": "mcq", "d": "retrieve", "q": "Why does the speaker \"hold my shadow back\" beside the deepest pool?",
             "opts": ["Crabs can feel a shadow fall and will hide.",
                      "The sun is too hot to sit in for long.",
                      "A shadow makes the water hard to see through.",
                      "The fish only come out when it is dark."],
             "why": "The third verse says \"crabs can feel a shadow fall / and vanish through a crack\"."},
            {"id": "d513517902d6", "t": "mcq", "d": "infer", "q": "In the fourth verse, why does the speaker wait before the shrimp appears?",
             "opts": ["The ripples have to settle before the water becomes clear.",
                      "The tide has to come back in to fill the pool.",
                      "The shrimp only comes out when the sun goes in.",
                      "The speaker is too tired to keep on walking."],
             "why": "\"The ripples smooth away. / The water clears like glass.\" Only then can the speaker see the shrimp."},
            {"id": "96496aa7109a", "t": "mcq", "d": "language", "q": "Why does the poet describe the anemone as \"a blob of jam\"?",
             "opts": ["to show that it looks red, soft and round",
                      "to show that it tastes sweet to the fish",
                      "to show that it is the smallest creature in the pool",
                      "to show that it is very easy to spread"],
             "why": "Jam is red and soft, and a blob is round: the comparison helps us picture the anemone. Its \"crimson\" crown confirms the colour."},
            {"id": "1d242b58ff74", "t": "mcq", "d": "language", "q": "Why does the poet imagine the little fish saying \"This pool is mine. Go home.\"?",
             "opts": ["to make the fish seem to be guarding its own home",
                      "to show that the fish is lost and wants to go home",
                      "to show that the speaker can understand fish",
                      "to suggest that the fish is about to attack"],
             "why": "\"As if to say\" shows the fish does not really speak: darting away from under its stone, it seems to be protecting its pool."},
            {"id": "5607342e8b9e", "t": "tap", "d": "infer", "q": "Tap the word that shows how carefully the speaker puts the rock back.",
             "s": "I lift one rock, then set it down [exactly] where it lay,",
             "why": "\"Exactly where it lay\": the rock goes back in just the same place, because creatures shelter under it."},
            {"id": "9b4133e5be60", "t": "order", "d": "sequence", "q": "Put these moments in the order they happen in the poem.",
             "items": ["The speaker crosses the rocks to the pools.",
                       "A shrimp flicks past in the clear water.",
                       "A little fish darts out from under a stone.",
                       "A wave comes in and showers the speaker with spray.",
                       "The speaker climbs back up the shingle path."],
             "why": "The poem follows one visit: crossing the rocks, watching the shrimp, then the fish, the first wave of the returning tide, and the walk home."},
            {"id": "10c4e264aec9", "t": "mcq", "d": "language", "q": "In the last verse, what is \"the hidden town\"?",
             "opts": ["the rock pools and all the creatures living in them",
                      "a village that lies just behind the beach",
                      "a group of houses under the shingle path",
                      "the place where the speaker lives"],
             "why": "The tide has \"gathered in\" the pools: their many creatures are like the busy people of a town, now hidden under the sea."},
        ],
    },
    {
        "key": "RD5.22",
        "year": 5,
        "strand": "Information",
        "title": "The Kingdom of Benin",
        "nc": "Retrieve, record and present information from non-fiction; distinguish between statements of fact and opinion",
        "text": (
            "Hundreds of years ago, in the rainforests of West Africa, there was a rich and powerful kingdom "
            "called Benin. It was not in the country that is called Benin today. It lay in the south of what is "
            "now Nigeria, and its people were the Edo.\n\n"
            "The kingdom was ruled by a king called the Oba, who lived in a great palace in the capital, Benin "
            "City. The city was carefully planned. Wide, straight streets ran through it, and it was divided into "
            "areas where different groups of craftworkers lived and worked. Around the city, and across the land "
            "beyond it, the people dug long earth walls and deep ditches, a huge task that took many years.\n\n"
            "Benin is most famous for its metalwork. Skilled workers made heads, figures and flat panels called "
            "plaques from brass and bronze. Many plaques once decorated the pillars of the Oba's palace and "
            "showed scenes from life at court: the Oba with his chiefs, musicians, hunters and visitors from abroad. Other "
            "craftworkers carved beautiful objects from ivory and wood.\n\n"
            "To make a brass head, a worker first shaped a model in wax and covered it in clay. When the clay "
            "was heated, the wax melted and ran out through a small hole, leaving a hollow space the same shape "
            "as the model. Hot liquid metal was poured into that space. Once it had cooled and hardened, the "
            "clay was broken away to reveal the finished head. This method is called lost-wax casting, because "
            "the wax is lost each time.\n\n"
            "From the late 1400s, traders from Portugal arrived by sea. They exchanged brass, cloth and other "
            "goods for pepper, ivory and cloth made in Benin. The extra brass meant that even more metalwork could "
            "be made.\n\n"
            "Today, Benin brass and bronze work can be seen in museums around the world, including the British "
            "Museum in London. In Benin City, metalworkers still use lost-wax casting, a skill handed down "
            "through families for hundreds of years. In my view, these works are among the finest ever made."
        ),
        "qs": [
            {"id": "c59041411b2e", "t": "mcq", "d": "retrieve", "q": "Where was the Kingdom of Benin, according to the text?",
             "opts": ["in the south of what is now Nigeria",
                      "in the country called Benin today",
                      "on the coast of Portugal",
                      "in the north of West Africa's deserts"],
             "no": {"in the country called Benin today": "The first paragraph says it was not in the country called Benin today."},
             "why": "The first paragraph says it \"lay in the south of what is now Nigeria\"."},
            {"id": "9e3097d49e45", "t": "text", "d": "retrieve", "q": "What was the king of Benin called? Find and copy the word.",
             "a": ["Oba", "the Oba"],
             "why": "The second paragraph says the kingdom was ruled by a king called the Oba."},
            {"id": "9734781a0ee9", "t": "mcq", "d": "infer", "q": "What does the second paragraph suggest about Benin City?",
             "opts": ["It was well organised and its people worked together on big tasks.",
                      "It was small and its streets were narrow and winding.",
                      "It was built quickly by visitors from another land.",
                      "It had no walls, so it was easy for traders to enter."],
             "why": "Its streets were planned and wide, craftworkers had their own areas, and people spent years digging walls and ditches."},
            {"id": "36d96495d84c", "t": "tap", "d": "vocab", "q": "Tap the word that names the flat metal panels.",
             "s": "Skilled workers made heads, figures and flat panels called [plaques] from brass and bronze.",
             "why": "The third paragraph says the flat panels were called plaques."},
            {"id": "bd6ef98d3bbf", "t": "order", "d": "sequence", "q": "Put these steps of lost-wax casting in the right order.",
             "items": ["Shape a model in wax.",
                       "Cover the model in clay.",
                       "Heat the clay so the wax melts and runs out.",
                       "Pour hot liquid metal into the hollow space.",
                       "Break the clay away from the cooled metal."],
             "why": "The fourth paragraph gives the steps in this order: wax model, clay, heating, pouring, breaking the clay."},
            {"id": "6609debb05ed", "t": "mcq", "d": "retrieve", "q": "According to the text, what did the traders from Portugal bring to Benin?",
             "opts": ["brass, cloth and other goods",
                      "pepper, ivory and cloth",
                      "plaques, heads and figures",
                      "wax, clay and wood"],
             "no": {"pepper, ivory and cloth": "These are what Benin gave the traders in exchange."},
             "why": "The fifth paragraph says the traders exchanged brass, cloth and other goods for Benin's pepper, ivory and cloth."},
            {"id": "0afb1451fa54", "t": "mcq", "d": "purpose", "q": "Which sentence from the text is an opinion, not a fact?",
             "opts": ["In my view, these works are among the finest ever made.",
                      "The kingdom was ruled by a king called the Oba.",
                      "From the late 1400s, traders from Portugal arrived by sea.",
                      "Hot liquid metal was poured into that space."],
             "why": "\"In my view\" shows the writer's own opinion; it cannot be proved true or false."},
        ],
    },
    {
        "key": "RD5.23",
        "year": 5,
        "strand": "Play scripts",
        "title": "Finders keepers",
        "nc": "Prepare play scripts to read aloud and perform; draw inferences about characters' feelings, thoughts and motives",
        "text": (
            "(The school playground at morning break. LEO is kneeling beside a bench. SANA walks over, eating an "
            "apple.)\n"
            "SANA: What are you doing down there?\n"
            "LEO: (standing up slowly, holding something behind his back) Nothing.\n"
            "SANA: Leo. I can see it sticking out between your fingers. Is that money?\n"
            "LEO: (showing her a folded ten-pound note) It was under the bench. Finders keepers.\n"
            "SANA: That's not a rule, Leo. That's just something people say when they want to keep things.\n"
            "LEO: But nobody saw it fall. It could belong to anyone. How would we even find out whose it is?\n"
            "SANA: We could give it to Mr Okafor. Someone might be looking for it right now.\n"
            "LEO: (turning the note over in his hands) Ten pounds is a lot, though. I could get the new football "
            "I've been saving for.\n"
            "SANA: And how would you feel if it was yours, and someone else bought a football with it?\n"
            "(LEO says nothing. He looks at the note for a long moment.)\n"
            "LEO: (quietly) All right. But you come with me.\n"
            "(They cross to MR OKAFOR, who is on playground duty by the gate. A small boy, ALFIE, stands beside "
            "him. ALFIE's eyes are red, and he is rubbing his nose on his sleeve.)\n"
            "MR OKAFOR: Don't worry, Alfie. We'll check the lost property box at lunchtime. Somebody might have "
            "handed it in.\n"
            "ALFIE: (sniffing) But Mum gave it to me for the farm trip. It was in my coat pocket, and now it's "
            "gone.\n"
            "(SANA and LEO look at each other.)\n"
            "LEO: Excuse me, Mr Okafor. Was it a ten-pound note?\n"
            "ALFIE: (looking up) Yes! It was folded in half, two times.\n"
            "LEO: (holding it out to ALFIE) I found it under the bench by the climbing frame.\n"
            "(ALFIE takes the note and hugs it to his chest. A huge smile spreads across his face.)\n"
            "ALFIE: Thank you! Thank you so much!\n"
            "MR OKAFOR: Well done, Leo. That was the honest thing to do, and I know it wasn't the easy thing.\n"
            "(ALFIE runs off to tell his friends. LEO watches him go.)\n"
            "SANA: (nudging him) Still wish you'd kept it?\n"
            "LEO: (smiling) No. That felt better than any football."
        ),
        "qs": [
            {"id": "43e4aaac57e6", "t": "mcq", "d": "infer", "q": "Why does Leo hide the money behind his back when Sana arrives?",
             "opts": ["He is thinking of keeping it and does not want her to see.",
                      "He wants to give Sana a surprise present.",
                      "He thinks Sana has dropped it and wants to tease her.",
                      "He is scared that the money is not real."],
             "why": "He says \"Nothing\" and then \"Finders keepers\": he wants to keep it, so he tries to hide it."},
            {"id": "5afb6f45f9a3", "t": "mcq", "d": "retrieve", "q": "What does Sana say \"finders keepers\" really is?",
             "opts": ["something people say when they want to keep things",
                      "a school rule that Mr Okafor made up",
                      "a game that children play at break time",
                      "the law about anything found in a playground"],
             "why": "Sana says, \"That's just something people say when they want to keep things.\""},
            {"id": "05d686d77e44", "t": "mcq", "d": "infer", "q": "Why does Leo say nothing after Sana's question about how he would feel?",
             "opts": ["The question makes him think, and he realises she is right.",
                      "He is angry with Sana and has decided to ignore her.",
                      "He cannot hear her because the playground is noisy.",
                      "He is busy counting how much money he has saved."],
             "why": "He looks at the note \"for a long moment\" and then agrees to hand it in: her question has changed his mind."},
            {"id": "8266825a45ae", "t": "tap", "d": "infer", "q": "Tap the word in the stage direction that shows Alfie has been crying.",
             "s": "ALFIE: ([sniffing]) But Mum gave it to me for the farm trip.",
             "why": "Sniffing, with red eyes and a runny nose, are signs that Alfie has been crying."},
            {"id": "c9f699bb4e25", "t": "text", "d": "retrieve", "q": "What was Alfie's money for? Find and copy the words.",
             "a": ["the farm trip", "farm trip", "a farm trip", "the trip", "trip"],
             "why": "Alfie says, \"Mum gave it to me for the farm trip.\""},
            {"id": "966bf8d1756c", "t": "mcq", "d": "structure", "q": "What are the words in brackets, such as \"(quietly)\" and \"(nudging him)\", for?",
             "opts": ["to tell the actors how to speak and move",
                      "to show words the characters whisper to each other",
                      "to give the actors extra lines to learn",
                      "to show what the audience should say"],
             "why": "In a play script, stage directions in brackets tell the actors what to do and how to say their lines; they are not spoken."},
            {"id": "450f09551e83", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the play?",
             "opts": ["A boy is tempted to keep money he finds, but a friend helps him do the right thing.",
                      "A boy loses his trip money and his teacher pays for the trip instead.",
                      "Two friends argue about a football and stop speaking to each other.",
                      "A teacher finds a ten-pound note and asks the children who dropped it."],
             "why": "Leo wants to keep the note, Sana makes him think, and he gives it back to Alfie, who had lost it."},
        ],
    },
    {
        "key": "RD5.24",
        "year": 5,
        "strand": "News reports",
        "title": "Swift boxes go up at Fellside",
        "nc": "Identify how language, structure and presentation contribute to meaning; retrieve information",
        "text": (
            "Pupils at Fellside Primary School in Kendal, Cumbria, have fixed twenty nesting boxes high under the "
            "roof of their school, in the hope of welcoming back one of Britain's most remarkable birds.\n\n"
            "The boxes are for swifts: dark, fast-flying birds with long, curved wings. Swifts spend the winter "
            "in Africa and fly thousands of miles to Britain each spring to nest. They usually arrive in May and "
            "leave again in August.\n\n"
            "Swifts are made for the air. They catch insects as they fly, drink by skimming the surface of lakes "
            "and rivers, and can even sleep on the wing. They hardly ever land on the ground. Instead, they nest "
            "in narrow gaps high up in buildings, such as holes under roof tiles.\n\n"
            "That is where the trouble lies. \"When old buildings are mended or new ones are built, those gaps "
            "are often sealed up,\" explained Imran Shah, aged nine. \"So when the swifts come back from their "
            "long journey, their nesting places have gone.\" Experts say that the number of swifts in Britain has "
            "fallen sharply in recent years.\n\n"
            "The Year 5 class spent the spring term raising money for the boxes with a sponsored silence and a "
            "cake sale. The wooden boxes were fixed on the north wall of the school, out of the hot afternoon "
            "sun. A local builder lent the school a lifting platform and put them up, while the pupils watched "
            "from the playground.\n\n"
            "\"Swifts can be slow to find new nest boxes,\" said class teacher Mrs Aoife Brennan. \"So in May we "
            "are going to play recordings of swift calls next to the boxes. Swifts are drawn to places where they "
            "can hear other swifts, so we hope the calls will tell them this is a good place to stay.\"\n\n"
            "One of the boxes has a tiny camera inside, linked to a screen in the school hall, so that everyone "
            "can see if a pair moves in.\n\n"
            "\"It might take a year or two before any swifts choose our boxes,\" admitted Imran. \"But we'll be "
            "looking up every day.\""
        ),
        "qs": [
            {"id": "df2afb54edc3", "t": "text", "d": "retrieve", "q": "How many nesting boxes have the pupils fixed to their school? Find and copy the number.",
             "a": ["twenty", "20"],
             "why": "The first sentence says the pupils have fixed twenty nesting boxes under the roof."},
            {"id": "24aa3be9bb99", "t": "mcq", "d": "structure", "q": "What does the first paragraph of the report do?",
             "opts": ["It gives the main news: who did what, and where.",
                      "It explains how swifts are able to sleep while flying.",
                      "It gives the teacher's opinion of the class.",
                      "It tells readers how to build a nesting box."],
             "why": "A news report starts with the main facts (who, what, where) so readers know the story straight away."},
            {"id": "ba7d83eeb2a3", "t": "tap", "d": "vocab", "q": "Tap the word that means \"closed up so that nothing can get in\".",
             "s": "\"When old buildings are mended or new ones are built, those gaps are often [sealed] up,\" explained Imran Shah, aged nine.",
             "why": "To seal something up is to close it completely: the gaps are blocked, so swifts cannot get in to nest."},
            {"id": "8783d1783b16", "t": "mcq", "d": "retrieve", "q": "According to Imran, why do swifts find fewer places to nest?",
             "opts": ["Gaps in buildings are sealed up when buildings are mended or built.",
                      "Swifts have stopped flying back to Britain from Africa.",
                      "Roof tiles become too hot for swifts in the afternoon sun.",
                      "Other birds take the nesting places before the swifts arrive."],
             "why": "Imran says the gaps \"are often sealed up\", so the swifts' nesting places have gone when they come back."},
            {"id": "18b97a0a0af7", "t": "mcq", "d": "infer", "q": "Why were the boxes fixed on the north wall, out of the hot afternoon sun?",
             "opts": ["so that the boxes would not get too hot for the birds inside",
                      "so that the pupils could watch them from the playground",
                      "so that the swifts could find them more easily in May",
                      "so that the builder could reach them with the platform"],
             "no": {"so that the pupils could watch them from the playground": "The pupils watched the builder from the playground, but the text links the north wall to keeping out of the hot sun."},
             "why": "\"Out of the hot afternoon sun\" is the clue: a box in full sun could become too hot for swifts to nest in."},
            {"id": "00c185e3a9bc", "t": "mcq", "d": "retrieve", "q": "Why is the class going to play recordings of swift calls?",
             "opts": ["Swifts are drawn to places where they can hear other swifts.",
                      "The calls will frighten other birds away from the boxes.",
                      "The pupils want to learn how to copy the swifts' calls.",
                      "The calls will tell the swifts when to fly back to Africa."],
             "why": "Mrs Brennan says \"Swifts are drawn to places where they can hear other swifts\"."},
            {"id": "e7b36bf50381", "t": "mcq", "d": "infer", "q": "What do Imran's last words show about the pupils?",
             "opts": ["They are ready to wait patiently, even if it takes a long time.",
                      "They expect the swifts to move in on the very first day.",
                      "They have lost interest now that the boxes are up.",
                      "They think the boxes were a waste of their money."],
             "no": {"They expect the swifts to move in on the very first day.": "Imran says it might take \"a year or two\"."},
             "why": "He knows it may take \"a year or two\", but says they will be \"looking up every day\": they will keep watching."},
        ],
    },
    {
        "key": "RD5.25",
        "year": 5,
        "strand": "Stories",
        "title": "Seventy dirhams",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions, and justify inferences with evidence",
        "text": (
            "Every summer, Salma spent the mornings helping her uncle Hassan at his stall in the market in "
            "Marrakech. The stall was small, but it was piled high with dates, figs and almonds, and Uncle Hassan "
            "knew the name of nearly every customer who passed.\n\n"
            "That Thursday, he had gone to collect a delivery, and for the first time Salma was in charge on her "
            "own. \"Weigh carefully, count the change twice, and smile,\" he had said. \"That is the whole job.\"\n\n"
            "Just before noon, the lane was so crowded that Salma could hardly keep up. A woman in a wide straw "
            "hat pointed at the dates and asked for half a kilo in careful French. Salma weighed them, tipped "
            "them into a paper bag and said, \"Thirty dirhams, please.\" The woman handed over a hundred-dirham "
            "note. But as Salma turned to the tin for the change, two more customers called out at once, and by "
            "the time she looked back, the straw hat had vanished into the crowd.\n\n"
            "Salma stared at the note in her hand. Seventy dirhams of change belonged to that woman. Nobody had "
            "noticed. Uncle Hassan would never know.\n\n"
            "For a moment she did not move. Then she pulled the shutter halfway down, asked the spice seller "
            "next door to keep an eye on the stall, and ran.\n\n"
            "The lanes twisted and split, and every one was full of people. Salma squeezed past a cart of "
            "oranges and ducked under a row of hanging carpets. At last, near the lantern stalls, she spotted the "
            "straw hat.\n\n"
            "\"Madame! Your change!\" she gasped, holding out the coins and notes.\n\n"
            "The woman looked at the money, then at Salma's hot, red face, and laughed in surprise. \"You ran all "
            "this way for me? Thank you. I did not even notice I had forgotten it.\"\n\n"
            "When Uncle Hassan came back, the spice seller told him the whole story before Salma could open her "
            "mouth. Her uncle was quiet for a moment. Then he put his hand on her shoulder.\n\n"
            "\"Anyone can learn to weigh dates,\" he said. \"But that is the part of the job I cannot teach.\""
        ),
        "qs": [
            {"id": "11a0c0fac85e", "t": "mcq", "d": "retrieve", "q": "Why was Salma looking after the stall alone that Thursday?",
             "opts": ["Uncle Hassan had gone to collect a delivery.",
                      "Uncle Hassan was busy serving at a lantern stall.",
                      "Uncle Hassan had taken a customer to the spice seller.",
                      "Uncle Hassan was unwell and had stayed at home."],
             "why": "The second paragraph says he had gone to collect a delivery, and Salma was in charge on her own."},
            {"id": "f2a435d61014", "t": "mcq", "d": "retrieve", "q": "How did the woman lose her change?",
             "opts": ["She walked off while Salma was busy with other customers.",
                      "She dropped it on the ground in the crowded lane.",
                      "Salma gave it by mistake to the spice seller.",
                      "She refused to take it and told Salma to keep it."],
             "why": "Two more customers called out as Salma turned for the change, and by the time she looked back the woman had gone."},
            {"id": "3e7d4accbde1", "t": "text", "d": "retrieve", "q": "How much change did the woman need? Find and copy the words.",
             "a": ["seventy dirhams", "70 dirhams", "seventy", "70"],
             "why": "The note was a hundred dirhams and the dates cost thirty, so seventy dirhams of change belonged to the woman."},
            {"id": "bfbfaa1db819", "t": "mcq", "d": "infer", "q": "\"For a moment she did not move.\" What does this suggest about Salma?",
             "opts": ["She was deciding what to do about the money.",
                      "She was too tired to run after anyone.",
                      "She had already decided to keep the money.",
                      "She was waiting for her uncle to come back."],
             "why": "The paragraph before says nobody had noticed and her uncle would never know: for a moment she was thinking about keeping it."},
            {"id": "51ade6f16b56", "t": "tap", "d": "vocab", "q": "Tap the word that shows Salma had to push through a narrow gap.",
             "s": "Salma [squeezed] past a cart of oranges and ducked under a row of hanging carpets.",
             "why": "To squeeze past something is to push through a very narrow space: the lanes were packed with people."},
            {"id": "fcc9d4b2c8f0", "t": "mcq", "d": "infer", "q": "Why did the spice seller tell Uncle Hassan the story \"before Salma could open her mouth\"?",
             "opts": ["He was impressed and wanted her uncle to know what she had done.",
                      "He was cross that Salma had left the stall for so long.",
                      "He wanted Salma to be in trouble for closing the shutter.",
                      "He thought Uncle Hassan had already heard the story."],
             "why": "He rushed to tell the whole story, and her uncle then praised her: he was proud of her honesty."},
            {"id": "41c7bc8e531a", "t": "mcq", "d": "infer", "q": "What is \"the part of the job I cannot teach\"?",
             "opts": ["being honest when nobody would find out",
                      "weighing the dates very carefully",
                      "remembering every customer's name",
                      "running fast through crowded lanes"],
             "no": {"weighing the dates very carefully": "Uncle Hassan says \"anyone can learn to weigh dates\": that is the part that can be taught."},
             "why": "He says weighing can be learned; what he cannot teach is the honesty Salma showed by returning the money."},
        ],
    },
    {
        "key": "RD5.26",
        "year": 5,
        "strand": "Information",
        "title": "The amazing octopus",
        "nc": "Retrieve, record and present information from non-fiction; identify how structure contributes to meaning",
        "text": (
            "With eight bendy arms, no bones and skin that can change colour in a moment, the octopus is one of "
            "the most unusual animals in the sea. There are around three hundred kinds of octopus. Some are "
            "smaller than your finger, while the largest, the giant Pacific octopus, can measure several metres "
            "from the tip of one arm to the tip of another.\n\n"
            "An octopus has no skeleton at all. The only hard part of its body is its beak, a sharp mouth shaped "
            "like a parrot's, hidden in the middle of its arms. This means that an octopus can squeeze its soft "
            "body through any gap that is bigger than its beak, slipping into narrow cracks between rocks where "
            "hunters cannot follow.\n\n"
            "Each arm is lined with rows of suckers. They grip rocks and hold on to crabs and other prey, and they "
            "can also feel and taste whatever they touch. Many of the octopus's nerve cells are in its arms, not "
            "its head, so an arm can work out a lot for itself.\n\n"
            "Inside, the octopus is just as strange. Its blood is blue, not red, and it has three hearts. Two of "
            "them pump blood through the gills, where it takes in oxygen from the water. The third pumps blood "
            "round the rest of the body.\n\n"
            "An octopus is a master of disguise. Special cells in its skin can change its colour and pattern in "
            "a moment, and it can even make its skin bumpy to look like rock or seaweed. If a predator such as a "
            "seal spots it anyway, the octopus squirts a cloud of dark ink and darts away backwards. It moves "
            "fast by pushing water out through a tube in its body.\n\n"
            "Octopuses are also very clever. In aquariums, some have learned to unscrew the lid of a jar to reach "
            "the food inside, and a few have even escaped from their tanks. In the wild, one kind of octopus "
            "carries empty coconut shells across the sea floor and hides inside them when danger comes near."
        ),
        "qs": [
            {"id": "b380420c5190", "t": "text", "d": "retrieve", "q": "What is the only hard part of an octopus's body? Find and copy one word.",
             "a": ["beak", "its beak", "the beak"],
             "why": "The second paragraph says \"The only hard part of its body is its beak\"."},
            {"id": "62d6aa696b07", "t": "mcq", "d": "infer", "q": "Why can an octopus slip through such narrow gaps?",
             "opts": ["It has no bones, so its soft body can squeeze into any shape.",
                      "Its suckers pull it through the gap one arm at a time.",
                      "It squirts ink into the crack to make it wider.",
                      "Its three hearts make it strong enough to push rocks apart."],
             "why": "With no skeleton, only its beak is hard, so its soft body fits through any gap bigger than the beak."},
            {"id": "72209e1c529d", "t": "mcq", "d": "retrieve", "q": "According to the text, what can the suckers do as well as grip?",
             "opts": ["feel and taste what they touch",
                      "pump blood round the body",
                      "change colour to match the rocks",
                      "squirt out a cloud of dark ink"],
             "why": "The third paragraph says the suckers \"can also feel and taste whatever they touch\"."},
            {"id": "ac41dc7353ac", "t": "mcq", "d": "compare", "q": "How is the job of the third heart different from the job of the other two?",
             "opts": ["It pumps blood round the body; the other two pump blood through the gills.",
                      "It pumps blood through the gills; the other two pump blood round the body.",
                      "It pumps ink out of the body; the other two pump blood.",
                      "It pumps water through the tube; the other two pump blood to the arms."],
             "why": "The fourth paragraph says two hearts pump blood through the gills and \"the third pumps blood round the rest of the body\"."},
            {"id": "bb1adf4811e0", "t": "tap", "d": "vocab", "q": "Tap the word that means \"sends out liquid in a sudden, fast stream\".",
             "s": "If a predator such as a seal spots it anyway, the octopus [squirts] a cloud of dark ink and darts away backwards.",
             "why": "To squirt is to send liquid out in a quick stream, as the octopus does with its ink."},
            {"id": "909c89d0ef82", "t": "mcq", "d": "purpose", "q": "Why does the writer describe octopuses unscrewing jar lids and escaping from tanks?",
             "opts": ["to give examples that show how clever octopuses are",
                      "to warn readers never to keep an octopus at home",
                      "to explain how octopuses find food in the wild",
                      "to show that aquariums are dangerous places"],
             "no": {"to explain how octopuses find food in the wild": "The jar and tank examples happened in aquariums, not in the wild."},
             "why": "The paragraph begins \"Octopuses are also very clever\", and the jar lids and escapes are the proof."},
            {"id": "e47eba7398e7", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the whole text?",
             "opts": ["The octopus has an unusual body that helps it hide, escape and solve problems.",
                      "The giant Pacific octopus is the largest animal living in the sea.",
                      "Octopuses are dangerous hunters that attack seals and other animals.",
                      "Octopuses live inside coconut shells because they have no bones."],
             "why": "Each paragraph shows a different unusual feature: no bones, clever arms, three hearts, disguise, and problem-solving."},
        ],
    },
    {
        "key": "RD5.27",
        "year": 5,
        "strand": "Persuasive writing",
        "title": "Look after our hedgerows",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "Walk down almost any country lane in Britain and you will pass a hedgerow: a long, thick line of "
            "shrubs and small trees, such as hawthorn, blackthorn and hazel, growing along the edge of a field. "
            "Most of us hardly give them a second glance. We should. Hedgerows are some of the most precious "
            "places for wildlife in the countryside, and they need our help.\n\n"
            "First, hedgerows are homes. Their thick, thorny branches give birds a safe place to nest, out of "
            "reach of cats and foxes. Hedgehogs, dormice and countless insects shelter in them too, and the "
            "flowers in spring and the berries in autumn feed all kinds of creatures.\n\n"
            "Second, hedgerows are roads. A mouse crossing an open field is easy for a hawk to spot. A hedgerow "
            "lets it travel from one wood to the next, hidden all the way. Without hedgerows, many woods would "
            "be like islands, cut off from each other.\n\n"
            "Third, hedgerows help farmers. They shelter farm animals from wind and rain, and their roots help "
            "to stop soil from being blown or washed away.\n\n"
            "Hedgerows are part of our history, too. Some are hundreds of years old, planted to mark the edges "
            "of land in the Middle Ages or even earlier. Yet in the years after the Second World War, many "
            "thousands of miles of hedgerow were pulled up so that fields could be made bigger for tractors and "
            "other large machines.\n\n"
            "Some people say that hedges are a nuisance, because they take so much work to keep tidy. It is true "
            "that a hedgerow needs looking after. But cutting it once every two or three years, in winter, "
            "instead of every summer, means less work and leaves far more flowers and berries for wildlife.\n\n"
            "So what can you do? If you have a garden, plant a hedge of native shrubs instead of putting up a "
            "fence. Ask whether there is space for one at school. And next time you walk along a lane, stop and "
            "look closely. You will be amazed at how much is living there.\n\n"
            "Our hedgerows have stood for centuries. Let's make sure they stand for centuries more."
        ),
        "qs": [
            {"id": "d62714bf3949", "t": "mcq", "d": "vocab", "q": "“Most of us hardly give them a second glance.” What does this mean?",
             "opts": ["Most of us hardly notice hedgerows.", "Most of us look at hedgerows twice.",
                      "Most of us cannot see hedgerows from the lane.", "Most of us think hedgerows are ugly."],
             "why": "Not giving something a second glance means not paying it any attention: we walk past hedgerows without noticing them."},
            {"id": "dd537dc549d0", "t": "mcq", "d": "language", "q": "The writer says “hedgerows are roads”. What does the writer mean?",
             "opts": ["Animals use them to travel safely from place to place.", "Hedgerows grow along the sides of roads.",
                      "Tractors drive along the tops of hedgerows.", "Hedgerows were once used as roads by people."],
             "why": "The paragraph explains that a hedgerow lets a small animal travel from one wood to the next, hidden all the way, as if along a road.",
             "no": {"Hedgerows grow along the sides of roads.": "Many hedgerows do grow beside lanes, but here “roads” means routes that animals travel along."}},
            {"id": "1ff733def58d", "t": "tap", "d": "retrieve", "q": "Tap the word that names the bird that could easily spot a mouse in an open field.",
             "s": "A mouse crossing an open field is easy for a [hawk] to spot.",
             "why": "The writer says a mouse crossing an open field is easy for a hawk to spot, so a hidden route matters."},
            {"id": "0e84e259d0e3", "t": "mcq", "d": "infer", "q": "“Without hedgerows, many woods would be like islands.” Why would this be a problem for wildlife?",
             "opts": ["Animals in one wood could not safely reach another wood.",
                      "The woods would be flooded with water.",
                      "Farmers could no longer reach their fields.",
                      "There would be no berries left in the woods."],
             "why": "An island is cut off by water. A wood with no hedgerows is cut off by open fields, so small animals cannot travel safely to the next wood."},
            {"id": "7f7dc0dd2ef8", "t": "mcq", "d": "retrieve", "q": "According to the text, why were so many hedgerows pulled up after the Second World War?",
             "opts": ["to make fields bigger for large machines", "to stop soil from being blown away",
                      "to make room for new roads and houses", "to stop hedgehogs eating the crops"],
             "why": "The fifth paragraph says hedgerows were pulled up so that fields could be made bigger for tractors and other large machines.",
             "no": {"to stop soil from being blown away": "Hedgerows help to stop soil blowing away; pulling them up does the opposite."}},
            {"id": "68d4b015bf08", "t": "mcq", "d": "structure", "q": "What does the writer do in the paragraph that begins “Some people say”?",
             "opts": ["gives a reason against hedgerows, then answers it",
                      "explains how to plant a hedge in a garden",
                      "lists the animals that live in hedgerows",
                      "describes how hedgerows were first planted"],
             "why": "The writer admits that hedges take work, then argues that cutting them less often means less work and more food for wildlife."},
            {"id": "231840ea4f68", "t": "mcq", "d": "purpose", "q": "What does the writer most want readers to do?",
             "opts": ["value hedgerows and help to look after them", "cut their hedges every summer to keep them tidy",
                      "put up fences instead of planting hedges", "visit farms to find out about tractors"],
             "why": "The writer asks readers to plant hedges, ask about one at school, look closely at hedgerows and make sure they last for centuries more.",
             "no": {"cut their hedges every summer to keep them tidy": "The writer says cutting every two or three years, in winter, is better than every summer."}},
        ],
    },
    {
        "key": "RD5.28",
        "year": 5,
        "strand": "Letters and diaries",
        "title": "A letter from the polar night",
        "nc": "Identify how language, structure and presentation contribute to meaning; draw inferences and justify them with evidence",
        "text": (
            "Tromsø, Norway\n"
            "10th December\n\n"
            "Dear Kiran,\n\n"
            "Thank you for your letter. It arrived at eleven o'clock in the morning, and it was still dark. "
            "Well, nearly dark. Let me explain.\n\n"
            "As you know, we moved here in May, when Mum started her new job at the university. Tromsø is in "
            "the far north of Norway, well inside the Arctic Circle. In the summer, the sun did not set at all "
            "for weeks. It was light at midnight, and I had to sleep with a scarf over my eyes. Now it is the "
            "opposite. From the end of November until the middle of January, the sun does not rise above the "
            "horizon at all. People here call it the polar night.\n\n"
            "It is not pitch black all day, though. For a few hours around lunchtime, the sky turns a deep, "
            "glowing blue and the snow seems to shine. Then the darkness creeps back, and the street lamps stay "
            "on until the next morning.\n\n"
            "You might think everyone would be gloomy, but they are not. Little lamps glow in nearly every "
            "window, and people go skiing in the evenings on forest tracks that are lit up all the way. At "
            "school we all wear reflectors on our coats so that drivers can see us. Mine is shaped like a fox.\n\n"
            "Last Tuesday, something amazing happened. We were walking home when green light began to ripple "
            "across the sky like a curtain moving in the wind. It was the northern lights! My friend Ingrid "
            "hardly looked up. She has seen them hundreds of times. I stood in the snow with my mouth open until "
            "my toes went numb.\n\n"
            "My Norwegian is getting better, although Ingrid still laughs at my accent. I am even learning to "
            "ski, which mostly means learning to fall over in new ways.\n\n"
            "I miss you, and I miss the grey Leicester drizzle. I never thought I would say that!\n\n"
            "Write back soon,\n"
            "Hana"
        ),
        "qs": [
            {"id": "282bcf34eae6", "t": "mcq", "d": "infer", "q": "Why does Hana write “Let me explain” near the start of the letter?",
             "opts": ["Kiran may be puzzled that it was dark at eleven in the morning.",
                      "Hana is sorry that the letter took so long to arrive.",
                      "Hana needs to explain why Mum wanted a new job.",
                      "Hana wants to explain how to ski on a forest track."],
             "why": "Darkness at eleven in the morning would seem strange in Leicester, so Hana goes on to explain the polar night."},
            {"id": "d9bf1da139d9", "t": "mcq", "d": "retrieve", "q": "Why did Hana's family move to Tromsø?",
             "opts": ["Mum started a new job at the university.", "The family wanted to learn to ski.",
                      "Hana's friend Ingrid already lived there.", "They wanted to see the northern lights."],
             "why": "The second paragraph says they moved in May, when Mum started her new job at the university."},
            {"id": "7cc49f5fdadc", "t": "mcq", "d": "compare", "q": "How is summer in Tromsø different from winter, according to Hana?",
             "opts": ["In summer the sun did not set; in winter it does not rise.",
                      "In summer it rained every day; in winter it snows every night.",
                      "In summer the northern lights shone; in winter the sky is always blue.",
                      "In summer the street lamps stayed on; in winter they are switched off."],
             "why": "Hana says that in summer the sun did not set for weeks, and that now it does not rise above the horizon at all: “Now it is the opposite.”"},
            {"id": "f03747b9ed3b", "t": "text", "d": "retrieve", "q": "What do people in Tromsø call the time when the sun does not rise? Find and copy two words.",
             "a": ["polar night", "the polar night"],
             "why": "The second paragraph ends: “People here call it the polar night.”"},
            {"id": "f555391cb71f", "t": "mcq", "d": "vocab", "q": "“You might think everyone would be gloomy, but they are not.” What does “gloomy” mean here?",
             "opts": ["sad and fed up", "tired and ready for bed",
                      "cold and shivering", "lost and unable to see"],
             "why": "Gloomy here means sad. Hana goes on to show that people stay cheerful: they light lamps and go skiing."},
            {"id": "f84df32b29e4", "t": "tap", "d": "language", "q": "Hana uses a simile for the northern lights. Tap the word for the thing they are compared to.",
             "s": "We were walking home when green light began to ripple across the sky like a [curtain] moving in the wind.",
             "why": "The rippling green light is compared to a curtain moving in the wind."},
            {"id": "aea75aa3380d", "t": "mcq", "d": "infer", "q": "“I miss the grey Leicester drizzle. I never thought I would say that!” What does this suggest about Hana?",
             "opts": ["Hana used to dislike the drizzle, but now misses home.",
                      "Hana wishes it rained in Tromsø instead of snowing.",
                      "Hana is moving back to Leicester very soon.",
                      "Hana thinks Leicester has more snow than Tromsø."],
             "why": "“I never thought I would say that” shows Hana did not like the drizzle before; missing it now shows how much Hana misses home and Kiran.",
             "no": {"Hana wishes it rained in Tromsø instead of snowing.": "Hana enjoys the snow and is learning to ski; it is home that Hana misses, not the rain itself."}},
        ],
    },
]
