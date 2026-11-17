"""Reading comprehension, Year 5 (keys RD5.01-RD5.14): 14 passages of 250-380 words, 7 questions each.

Spec: app/bank/SPEC_READING.md (and SPEC.md for the question format). Every passage and question is
original writing, written by hand. Topics link to the Year 5 curriculum where natural: Earth and space,
forces, properties and changes of materials, plant life cycles, the Anglo-Saxons and Vikings, scholars of
the Islamic Golden Age, the achievements of ancient Greece, rivers and the water supply, time zones; plus
realistic stories, a poem, a biography (Mary Anning), a persuasive article and a diary.

The questions mix the KS2 reading domains (retrieve, infer, vocab, sequence, summarise, structure,
language, compare, predict, purpose). To be checked line by line by a second reviewer (facts, one
defensible answer per question, no leaks) before scripts/bank_ids.py gives the questions their ids.
"""

SKILLS = [
    {
        "key": "RD5.01",
        "year": 5,
        "strand": "Stories",
        "title": "The last box",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "The removal van pulled away from the kerb, and Ifeoma watched it until it turned the corner at the "
            "end of Elm Road. Everything she owned was inside it except for one cardboard box, which sat on the "
            "back seat of the car beside her. On the side, in her own thick black letters, it said: DO NOT PACK. "
            "IFE ONLY.\n\n"
            "Inside were the things she could not trust to strangers: a jar of shells from Whitby, a photo of her "
            "class on sports day, and the friendship bracelet that Hannah had plaited for her the week before. "
            "Hannah had cried when they said goodbye. Ifeoma had not. She had decided that if she did not cry, it "
            "would not really be happening.\n\n"
            "The drive north to Inverness took most of the day. Her little brother, Chidi, fell asleep before they "
            "had even left Leeds, his mouth open and his cheek squashed against the window. Mum played the radio "
            "quietly. Every time a sign showed how many miles were left, Ifeoma's stomach tightened a little more.\n\n"
            "The new house was taller and narrower than the old one, with a green front door and a garden that "
            "sloped down towards a stone wall. Ifeoma carried her box upstairs to a room that smelled of fresh "
            "paint. It was bigger than her old bedroom, and from the window she could see hills, already turning "
            "purple in the evening light.\n\n"
            "She was unpacking the shells when she heard a steady tapping sound. In the garden next door, a girl "
            "about her age was throwing a tennis ball against the wall and catching it, over and over, without "
            "missing once.\n\n"
            "The girl looked up and waved. Ifeoma hesitated. Then she put the jar on the windowsill, where the "
            "shells caught the last of the sun, and went downstairs to find out the girl's name."
        ),
        "qs": [
            {"id": "dc083c24d5e6", "t": "mcq", "d": "infer", "q": "Why did Ifeoma keep one box out of the removal van?",
             "opts": ["She wanted her most precious things to stay with her.",
                      "The removal van was already too full to take it.",
                      "The box belonged to her little brother, Chidi.",
                      "She needed the things in it for the long drive."],
             "why": "The second paragraph says the box held \"the things she could not trust to strangers\": her most precious things."},
            {"id": "ac81b456d003", "t": "text", "d": "retrieve", "q": "Who plaited the friendship bracelet? Find and copy the name.",
             "a": ["Hannah"],
             "why": "The second paragraph says Hannah had plaited the bracelet for her the week before."},
            {"id": "66ac0bf86dbd", "t": "mcq", "d": "infer", "q": "Why did Ifeoma not cry when she said goodbye to Hannah?",
             "opts": ["She hoped that not crying would stop the move from feeling real.",
                      "She was not sad at all to be leaving Leeds.",
                      "She was too excited about her bigger bedroom.",
                      "Hannah had asked her to be brave and not cry."],
             "why": "She had decided that if she did not cry, it would not really be happening: she was trying not to face the move."},
            {"id": "1e6050ee88c6", "t": "tap", "d": "infer", "q": "Tap the word that shows how Ifeoma's body reacted to her nerves.",
             "s": "Every time a sign showed how many miles were left, Ifeoma's stomach [tightened] a little more.",
             "why": "Her stomach tightened: a stomach that tightens is the body's sign of worry, and it gets worse as they get closer."},
            {"id": "5e713ce488f3", "t": "mcq", "d": "vocab", "q": "\"A garden that sloped down towards a stone wall.\" What does \"sloped\" mean here?",
             "opts": ["went gradually downhill", "was covered in stones", "was long and narrow", "was full of flowers"],
             "why": "Something that slopes down goes gradually lower, like the side of a hill."},
            {"id": "8c23e1fb9ca9", "t": "mcq", "d": "predict", "q": "What is Ifeoma most likely to do next?",
             "opts": ["Introduce herself to the girl next door.",
                      "Stay in her room and finish unpacking.",
                      "Phone Hannah to say she wants to go home.",
                      "Wake Chidi up to show him the hills."],
             "why": "She goes downstairs \"to find out the girl's name\", so she is about to go and meet her."},
            {"id": "dc9399e611eb", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the story?",
             "opts": ["A worried girl arrives at a new home and starts to hope she might make a friend.",
                      "A girl refuses to move house and plans to run back to her best friend.",
                      "A family drives to Scotland for a holiday and spends the evening in the hills.",
                      "A girl and her little brother argue all the way through a long car journey."],
             "why": "Ifeoma is anxious about the move, but at the end she goes to meet the girl next door."},
        ],
    },
    {
        "key": "RD5.02",
        "year": 5,
        "strand": "Information",
        "title": "Earth, Sun and Moon",
        "nc": "Retrieve, record and present information from non-fiction",
        "text": (
            "For thousands of years, most people believed that the Sun travelled around the Earth. After all, "
            "every morning it seems to rise in the east, cross the sky and sink in the west. Today we know that "
            "the Sun is not travelling across our sky at all. It is the Earth that is moving.\n\n"
            "The Earth spins on its axis, an imaginary line running through it from the North Pole to the South "
            "Pole. It makes one complete turn every 24 hours. At any moment, half of the planet faces the Sun and "
            "has daytime, while the other half faces away into space and has night. As the Earth turns, places "
            "move from the light into the dark and back again. That is why we have day and night.\n\n"
            "At the same time, the Earth is travelling around the Sun along a huge path called an orbit. One "
            "complete orbit takes about 365 and a quarter days, which is one year. Those extra quarter days are "
            "the reason we add a day to February every fourth year, in what is called a leap year.\n\n"
            "The Sun is a star: an enormous ball of hot gas that gives out its own light. The Earth and the other "
            "planets give out no light of their own. Neither does the Moon, which orbits the Earth about once a "
            "month. When we see the Moon shining at night, we are really seeing sunlight bouncing off its rocky "
            "surface.\n\n"
            "The Moon seems to change shape during the month, from a thin crescent to a full circle and back again. "
            "In fact, its shape never changes. Half of the Moon is always lit by the Sun, but as it travels around "
            "the Earth, we see different amounts of that lit half.\n\n"
            "Scientists did not discover all this by guessing. They watched the sky carefully for many years, "
            "measured what they saw and tested their ideas against what they measured. That patient work changed "
            "the way we understand our place in space."
        ),
        "qs": [
            {"id": "5813748a3ce2", "t": "mcq", "d": "language", "q": "Why does the writer say the Sun \"seems\" to rise and cross the sky?",
             "opts": ["It only looks as if the Sun moves; really the Earth is turning.",
                      "The Sun moves too quickly for us to watch it properly.",
                      "Clouds often hide the Sun as it crosses the sky.",
                      "The Sun only rises in the east during the summer."],
             "why": "\"Seems\" means it looks that way but is not true: the first paragraph says it is the Earth that is moving."},
            {"id": "7c6909cd9990", "t": "mcq", "d": "retrieve", "q": "According to the text, what is the Earth's axis?",
             "opts": ["an imaginary line from the North Pole to the South Pole",
                      "the path the Earth follows around the Sun",
                      "the half of the Earth that faces the Sun",
                      "the line between the daytime and the night"],
             "why": "The second paragraph calls the axis \"an imaginary line running through it from the North Pole to the South Pole\"."},
            {"id": "788f03aaeb1f", "t": "mcq", "d": "retrieve", "q": "According to the text, why is it night in some places while it is day in others?",
             "opts": ["Those places are turned away from the Sun as the Earth spins.",
                      "The Sun has travelled round to the other side of the Earth.",
                      "The Moon has moved in front of the Sun and blocked its light.",
                      "Those places are much further from the Sun at that time of year."],
             "why": "The second paragraph says half the planet faces the Sun and has daytime, while the other half faces away and has night."},
            {"id": "ae0512354536", "t": "text", "d": "retrieve", "q": "How often is an extra day added to February? Find and copy the words.",
             "a": ["every fourth year", "every 4th year", "every four years", "every 4 years"],
             "why": "The third paragraph says we add a day to February every fourth year, in a leap year."},
            {"id": "361ce2541f6e", "t": "mcq", "d": "vocab", "q": "In the third paragraph, what is an \"orbit\"?",
             "opts": ["the path one object travels around another in space",
                      "the time it takes the Earth to spin once",
                      "an extra day added on to the end of February",
                      "an imaginary line through the middle of a planet"],
             "why": "The text says the Earth travels around the Sun \"along a huge path called an orbit\"."},
            {"id": "b928f41382e5", "t": "mcq", "d": "compare", "q": "What is the difference between the Sun and the Moon, according to the text?",
             "opts": ["The Sun gives out its own light; the Moon only reflects sunlight.",
                      "The Sun orbits the Earth; the Moon orbits the Sun.",
                      "The Sun is a planet; the Moon is a small star.",
                      "The Sun changes shape; the Moon always stays the same."],
             "why": "The fourth paragraph says the Sun gives out its own light, but the Moon gives out none: we see sunlight bouncing off it."},
            {"id": "baae7bdc9dd7", "t": "mcq", "d": "structure", "q": "Why did the writer include the last paragraph?",
             "opts": ["To show that these facts were found by careful watching and testing.",
                      "To explain why the Moon seems to change shape.",
                      "To tell readers to watch the sky every night.",
                      "To show that people in the past were not clever."],
             "why": "The last paragraph says scientists did not guess: they watched, measured and tested their ideas."},
        ],
    },
    {
        "key": "RD5.03",
        "year": 5,
        "strand": "Explanations",
        "title": "Why things fall and why they stop",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "Drop a pencil and it falls to the floor. Kick a football across the grass and, sooner or later, it "
            "rolls to a stop. Neither of these things happens by chance. In each case a force is at work, and a "
            "force is simply a push or a pull.\n\n"
            "The pencil falls because of gravity. Gravity is a pulling force between objects, and because the "
            "Earth has such a large mass, its pull on everything near it is strong. It pulls the pencil, the "
            "football and you towards its centre. That is why things fall downwards wherever you are on the "
            "planet, whether you live in Cardiff or in Cape Town. The weight of an object is the force of gravity "
            "pulling on it, so scientists measure weight in newtons, the unit of force, rather than in kilograms.\n\n"
            "The football stops because of friction. Friction is a force that acts when two surfaces rub or slide "
            "against each other, and it always works against the movement. Rough surfaces, such as long grass or "
            "a carpet, create more friction than smooth ones, such as ice. Friction is not always a nuisance, "
            "though. Without it, the soles of your shoes would not grip the pavement, and you would slip with "
            "every step.\n\n"
            "Air resistance is a kind of friction that acts on things moving through the air. It pushes against "
            "a falling object and slows it down. The bigger the surface pushing against the air, the greater the "
            "air resistance. A parachute works by opening out into a huge canopy that traps air beneath it, so a "
            "skydiver drifts gently to the ground instead of plunging.\n\n"
            "Water resistance acts in the same way on things moving through water. Fish, dolphins and submarines "
            "all have smooth, streamlined shapes, which let them slip through the water with less resistance.\n\n"
            "Engineers think about these forces all the time. A racing bicycle, a pair of football boots and an "
            "aeroplane are all designed with gravity, friction and air resistance in mind."
        ),
        "qs": [
            {"id": "84f1927d6b1d", "t": "mcq", "d": "retrieve", "q": "According to the text, why is the Earth's pull on everything near it so strong?",
             "opts": ["The Earth has such a large mass.",
                      "The Earth spins round so quickly.",
                      "The Earth is wrapped in a layer of air.",
                      "The Earth is very close to the Sun."],
             "why": "The second paragraph says that because the Earth has such a large mass, its pull on everything near it is strong."},
            {"id": "6cb79f39ffb8", "t": "text", "d": "retrieve", "q": "Find and copy the unit that scientists use to measure weight.",
             "a": ["newtons", "newton", "in newtons"],
             "no": {"kilograms": "The text says weight is measured in newtons \"rather than in kilograms\"."},
             "why": "Weight is a force, so the second paragraph says it is measured in newtons."},
            {"id": "f54da5cfe557", "t": "tap", "d": "retrieve", "q": "Tap the word that names a surface with very little friction.",
             "s": "Rough surfaces, such as long grass or a carpet, create more friction than smooth ones, such as [ice].",
             "why": "Ice is given as an example of a smooth surface, which creates less friction than rough ones."},
            {"id": "a9f91dc6df95", "t": "mcq", "d": "infer", "q": "Why does the writer say that friction \"is not always a nuisance\"?",
             "opts": ["Friction also does useful jobs, such as helping shoes grip.",
                      "Friction only acts on smooth surfaces, such as ice.",
                      "Friction helps footballs to roll further across grass.",
                      "Friction is really just another kind of gravity."],
             "why": "Straight after, the text says that without friction your shoes would not grip and you would slip."},
            {"id": "717f994286c4", "t": "mcq", "d": "vocab", "q": "A skydiver \"drifts gently to the ground instead of plunging\". What does \"plunging\" mean?",
             "opts": ["falling fast and steeply", "floating slowly sideways", "landing softly on grass", "spinning round and round"],
             "why": "Plunging is the opposite of drifting gently: it means dropping down fast."},
            {"id": "1a27ca3809bf", "t": "mcq", "d": "compare", "q": "How are air resistance and water resistance alike, according to the text?",
             "opts": ["Both push against moving things and slow them down.",
                      "Both pull objects towards the centre of the Earth.",
                      "Both act only on smooth, streamlined shapes.",
                      "Both are stronger when the surface is smaller."],
             "why": "Water resistance \"acts in the same way\" as air resistance, which pushes against a moving object and slows it."},
            {"id": "60263c7d958b", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to explain how some everyday forces work",
                      "to persuade readers to try skydiving",
                      "to tell the story of a football match",
                      "to give instructions for building a bicycle"],
             "why": "Each paragraph explains a force (gravity, friction, air and water resistance) using everyday examples."},
        ],
    },
    {
        "key": "RD5.04",
        "year": 5,
        "strand": "Stories",
        "title": "The turquoise pen",
        "nc": "Identify and discuss themes and conventions in a wide range of writing",
        "text": (
            "Freya's new pens were the best in the class. There were thirty of them in a flat tin, every colour "
            "from lemon to midnight blue, and Freya did not lend them to anyone. So when she slid the tin across "
            "the table and said, “You can borrow them for your poster, Zainab, as long as you bring them back "
            "tomorrow,” Zainab felt as if she had been handed a prize.\n\n"
            "That evening she spread the pens across her bedroom floor and worked until her poster about the "
            "rainforest glowed with colour. She was so pleased with it that she ran downstairs to show Dad, and "
            "then it was time for dinner, and then it was time for bed.\n\n"
            "In the morning, the turquoise pen was lying on the carpet with its cap beside it. Zainab pressed it "
            "onto the paper. Nothing came out but a dry, pale scratch.\n\n"
            "All the way to school, the tin felt heavier in her bag. Freya would never notice, she told herself. "
            "There were twenty-nine other pens. She could slip the cap back on and nobody would ever know.\n\n"
            "At the classroom door, Freya was waiting with a smile. Zainab held out the tin, opened her mouth, and "
            "closed it again. Then she took a deep breath.\n\n"
            "“I left the turquoise one open all night,” she said. “It's dried out. I'm really sorry. I'll buy you "
            "a new one with my pocket money.”\n\n"
            "Freya's smile disappeared. She took the tin without a word and sat down at the far end of the table. "
            "At lunch she played with a different group of girls. Zainab spent the afternoon staring at her maths "
            "book, wondering whether being honest had been a terrible mistake.\n\n"
            "The next morning, there was a folded note on Zainab's chair. Inside, in turquoise ink that had clearly "
            "come from a brand-new pen, it said: Thank you for telling me. Friends?"
        ),
        "qs": [
            {"id": "5e19f9e874ee", "t": "mcq", "d": "infer", "q": "Why did Zainab feel \"as if she had been handed a prize\"?",
             "opts": ["Freya never usually lent her pens to anyone.",
                      "Zainab had just won a competition for her poster.",
                      "The pens were a present for Zainab to keep.",
                      "The teacher had chosen Zainab to make a poster."],
             "why": "The first paragraph says Freya \"did not lend them to anyone\", so being allowed to borrow them felt special."},
            {"id": "619b4918d422", "t": "mcq", "d": "language", "q": "\"All the way to school, the tin felt heavier in her bag.\" Why did the writer put it this way?",
             "opts": ["To show that the secret was weighing on Zainab's mind.",
                      "To show that the pens were made of heavy metal.",
                      "To show that Zainab had packed more into her bag.",
                      "To show that Zainab was tired after a late night."],
             "why": "The tin was no heavier really: her guilt about the dried pen made it feel like a heavy load."},
            {"id": "dba2b6642026", "t": "tap", "d": "infer", "q": "Tap the word that shows Zainab nearly said nothing about the pen.",
             "s": "Zainab held out the tin, opened her mouth, and [closed] it again.",
             "why": "She opened her mouth to speak and then closed it: for a moment she was going to keep quiet."},
            {"id": "7aa254f22ef0", "t": "mcq", "d": "infer", "q": "How did Freya feel when Zainab first told her about the pen?",
             "opts": ["upset and hurt", "relieved and grateful", "amused and cheerful", "not bothered at all"],
             "why": "Her smile disappeared, she said nothing and sat far away from Zainab: all signs that she was upset."},
            {"id": "e487e9c254ef", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the story.",
             "items": ["Freya lends Zainab her pens.",
                       "Zainab shows her poster to Dad.",
                       "Zainab finds that the turquoise pen has dried out.",
                       "Zainab owns up to Freya.",
                       "Freya leaves a note on Zainab's chair."],
             "why": "The poster is made in the evening, the dry pen is found in the morning, and the note comes the day after Zainab owns up."},
            {"id": "aa668cbdb33c", "t": "mcq", "d": "infer", "q": "What does the turquoise ink in the note suggest Freya had done?",
             "opts": ["got herself a new turquoise pen",
                      "made the dried-out pen work again",
                      "borrowed Zainab's own turquoise pen",
                      "bought Zainab a whole new tin of pens"],
             "why": "The ink \"had clearly come from a brand-new pen\", so Freya had already replaced the dried one herself."},
            {"id": "d064f47989d2", "t": "mcq", "d": "summarise", "q": "What is the main message of the story?",
             "opts": ["Telling the truth can be hard, but it can make a friendship stronger.",
                      "You should never lend your favourite things to anybody.",
                      "Expensive pens are always better than cheaper pens.",
                      "It is best to keep a mistake secret if nobody will notice."],
             "why": "Zainab owns up even though it is hard, and Freya's note shows the friendship has survived."},
        ],
    },
    {
        "key": "RD5.05",
        "year": 5,
        "strand": "Information",
        "title": "Anglo-Saxons and Vikings",
        "nc": "Retrieve, record and present information from non-fiction",
        "text": (
            "After the Roman army left Britain in the early 400s, new groups of people began to cross the North "
            "Sea. They came from lands that are now parts of Germany, Denmark and the Netherlands, and today we "
            "call them the Anglo-Saxons. Some came to fight, but many came looking for good farmland. Over time "
            "they settled across much of what became England, and the name England itself comes from one of these "
            "groups, the Angles.\n\n"
            "Most Anglo-Saxons did not live in the old Roman towns, and many of those towns were left to crumble. "
            "Instead, they built villages of wooden houses with thatched roofs, surrounded by fields. Many English place names still "
            "carry Anglo-Saxon endings. A name ending in -ton often began as a farm or village, and one ending in "
            "-ford grew up beside a shallow place where people could cross a river.\n\n"
            "Near the end of the 700s, a new danger arrived. Raiders from Scandinavia, the lands we now call Norway, "
            "Denmark and Sweden, began attacking the coasts. We call them the Vikings. In AD 793 they raided the "
            "island of Lindisfarne, off the north-east coast, and the news shocked people across the country.\n\n"
            "The Vikings were famous for their longships, which were long, narrow and light. They could cross the "
            "open sea, yet they were shallow enough to row up rivers far inland. But the Vikings were not only "
            "raiders. Many were farmers, traders and skilled craftworkers, and some families came to settle for "
            "good.\n\n"
            "In the 800s, Viking armies conquered much of the north and east of England. King Alfred of Wessex "
            "fought back, and in the end an agreement split the land. The Vikings would rule the north and east, "
            "an area later called the Danelaw, while the Anglo-Saxons kept the south and west. Alfred built "
            "defended towns called burhs to protect his kingdom, and he is remembered today as Alfred the Great.\n\n"
            "The Vikings made the city of York, which they called Jorvik, into a busy trading centre. "
            "Archaeologists digging there have found the remains of their houses, workshops, shoes and even combs "
            "carved from antler."
        ),
        "qs": [
            {"id": "80f97cca781d", "t": "mcq", "d": "retrieve", "q": "Where did the Anglo-Saxons come from, according to the text?",
             "opts": ["lands that are now parts of Germany, Denmark and the Netherlands",
                      "lands that are now called Norway, Denmark and Sweden",
                      "the old Roman towns in the south of Britain",
                      "the island of Lindisfarne, off the north-east coast"],
             "why": "The first paragraph names Germany, Denmark and the Netherlands. Norway, Denmark and Sweden are where the Vikings came from."},
            {"id": "826ae24aabe3", "t": "text", "d": "retrieve", "q": "Find and copy the name of the group that the name England comes from.",
             "a": ["the Angles", "Angles"],
             "why": "The first paragraph says the name England comes from one of the groups, the Angles."},
            {"id": "382a19be0fb9", "t": "mcq", "d": "vocab", "q": "Many old Roman towns were \"left to crumble\". What does this mean?",
             "opts": ["to slowly fall to pieces", "to be rebuilt in wood", "to fill up with farmers", "to be knocked down at once"],
             "why": "Something that crumbles breaks into small pieces bit by bit: the towns were left to fall apart."},
            {"id": "9e8039ed5939", "t": "mcq", "d": "infer", "q": "Using the text, what might have been at the place where the town of Ashford first grew up?",
             "opts": ["a shallow place to cross a river", "a single farm", "an old Roman town", "a Viking trading centre"],
             "why": "The second paragraph says a name ending in -ford grew up beside a shallow place to cross a river."},
            {"id": "3b88d7fbf368", "t": "mcq", "d": "retrieve", "q": "Why were longships so useful to the Vikings?",
             "opts": ["They could cross the sea and also travel up rivers far inland.",
                      "They were heavy enough to carry whole villages of people.",
                      "They were deep enough to stay steady in any storm.",
                      "They had sails, so they never needed to be rowed."],
             "why": "The fourth paragraph says longships could cross the open sea, yet were shallow enough to row up rivers."},
            {"id": "40d72be9e7b7", "t": "mcq", "d": "structure", "q": "Why did the writer include the sentence \"But the Vikings were not only raiders.\"?",
             "opts": ["To show there was more to the Vikings than attacking.",
                      "To explain why the raid on Lindisfarne shocked people.",
                      "To describe how longships were built and rowed.",
                      "To show that no Vikings ever settled in Britain."],
             "why": "The sentence turns from the raids to the Vikings as farmers, traders, craftworkers and settlers."},
            {"id": "d6900c527e9c", "t": "mcq", "d": "summarise", "q": "Which heading would best fit the fifth paragraph?",
             "opts": ["Alfred and the Danelaw", "Life in Jorvik", "The first Viking raid", "Anglo-Saxon villages"],
             "why": "The fifth paragraph is about King Alfred fighting back and the land being split, with the Danelaw in the north and east."},
        ],
    },
    {
        "key": "RD5.06",
        "year": 5,
        "strand": "Biography",
        "title": "Mary Anning, fossil hunter",
        "nc": "Summarise the main ideas drawn from more than one paragraph, identifying key details",
        "text": (
            "Mary Anning was born in 1799 in Lyme Regis, a small town on the south coast of England. The cliffs "
            "there are made of layers of rock that slowly crumble into the sea, and after a storm, new fossils "
            "often appear on the beach.\n\n"
            "Mary's family was poor. Her father, Richard, was a carpenter who collected fossils in his spare time "
            "and sold them to visitors. He taught Mary and her brother, Joseph, how to search the shore and how "
            "to clean their finds carefully. When he died in 1810, the family was left in debt, and fossil hunting "
            "became one of the ways they earned money.\n\n"
            "In 1811, Joseph found a strange skull in the cliff. Over the following months, Mary, who was only "
            "about twelve, uncovered the rest of the skeleton. It belonged to an ichthyosaur, a sea reptile that "
            "had lived millions of years earlier. Few people had ever seen anything like it.\n\n"
            "Mary kept searching for the rest of her life. In 1823 she found the first complete skeleton of a "
            "plesiosaur, a sea reptile with a long neck and four large flippers. Some experts at first suspected "
            "that the fossil was a fake, but they soon accepted that it was real. Later she found one of the first "
            "pterosaurs discovered in Britain, a reptile that could fly.\n\n"
            "The work was hard and dangerous. Mary searched the beach in winter, when storms had loosened the "
            "rocks, and she had to watch out for falling cliffs and rising tides. In 1833 a landslide killed her "
            "dog, Tray, and only just missed Mary herself.\n\n"
            "Scientists bought her fossils and asked for her advice, yet Mary was not allowed to join the "
            "Geological Society of London, because it did not accept women at that time. Her discoveries were "
            "often written about by men who did not mention her name.\n\n"
            "Mary Anning died in 1847. Today she is remembered as one of the greatest fossil hunters who ever "
            "lived, and her finds helped scientists to understand that living things have changed over enormous "
            "stretches of time."
        ),
        "qs": [
            {"id": "f928b65d271d", "t": "mcq", "d": "retrieve", "q": "What was the job of Mary's father?",
             "opts": ["He was a carpenter.", "He was a fisherman.", "He was a scientist.", "He was a shopkeeper."],
             "why": "The second paragraph says Richard was a carpenter who collected fossils in his spare time."},
            {"id": "351651151282", "t": "mcq", "d": "infer", "q": "Why did fossil hunting become so important to the family after 1810?",
             "opts": ["They needed money to live on after Mary's father died.",
                      "Mary wanted to be allowed to join the Geological Society.",
                      "More visitors had started coming to Lyme Regis.",
                      "Joseph had just found a famous skull in the cliff."],
             "why": "Her father died in 1810 and left the family in debt, so selling fossils helped them earn money."},
            {"id": "d52e17ef1c5d", "t": "order", "d": "sequence", "q": "Put these events from Mary's life in the order they happened.",
             "items": ["Mary's father dies.",
                       "Joseph finds a strange skull in the cliff.",
                       "Mary finds a complete plesiosaur.",
                       "A landslide kills Mary's dog.",
                       "Mary Anning dies."],
             "why": "The dates in the text give the order: 1810, 1811, 1823, 1833 and 1847."},
            {"id": "15a3fabf48d6", "t": "mcq", "d": "vocab", "q": "\"Some experts at first suspected that the fossil was a fake.\" What does \"suspected\" mean?",
             "opts": ["had a feeling it might be true", "knew it for certain", "told everybody about it", "were frightened by it"],
             "why": "To suspect is to think something may be true without proof. The experts later accepted it was real."},
            {"id": "9e9512bd12d9", "t": "mcq", "d": "infer", "q": "Why did Mary search the beach in winter, even though it was dangerous?",
             "opts": ["Storms loosened the rocks, so more fossils came to light.",
                      "There were fewer visitors on the beach to get in her way.",
                      "The tides were lower and safer in the winter months.",
                      "Her father had taught her never to search in summer."],
             "why": "The text links winter to storms that had loosened the rocks; the first paragraph says new fossils appear after a storm."},
            {"id": "156caae381ea", "t": "text", "d": "retrieve", "q": "Find and copy the name of Mary's dog.",
             "a": ["Tray"],
             "why": "The fifth paragraph says a landslide killed her dog, Tray, in 1833."},
            {"id": "ffb763702af6", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to tell readers about Mary Anning's life and discoveries",
                      "to teach readers how to find and clean fossils",
                      "to persuade readers to go on holiday to Lyme Regis",
                      "to explain how the cliffs at Lyme Regis were formed"],
             "why": "A biography tells the story of a real person's life: here, Mary Anning's from birth to death and what she found."},
        ],
    },
    {
        "key": "RD5.07",
        "year": 5,
        "strand": "Information",
        "title": "Scholars of the Islamic Golden Age",
        "nc": "Retrieve, record and present information from non-fiction",
        "text": (
            "Between about the 8th and 13th centuries, cities such as Baghdad, Cairo and Córdoba were among the "
            "greatest centres of learning in the world. Historians call this period the Islamic Golden Age. "
            "Scholars there studied mathematics, medicine, astronomy, engineering and much more, and many of their "
            "ideas later spread to Europe.\n\n"
            "In Baghdad, the rulers supported a famous centre of study known as the House of Wisdom. Scholars "
            "gathered books from Greece, Persia and India and translated them into Arabic. This meant that "
            "knowledge which might otherwise have been lost was saved, studied and improved. Paper, which had been "
            "invented in China, was now being made in Baghdad, so books could be copied far more cheaply than "
            "before.\n\n"
            "One scholar who worked in Baghdad was al-Khwarizmi. He wrote a book explaining how to solve problems "
            "with unknown numbers, and the word algebra comes from part of its title. His name gives us another "
            "modern word: algorithm, a set of steps for solving a problem. His writing also helped to spread the "
            "way of writing numbers, first worked out in India, that we still use today, with the digits 0 to 9.\n\n"
            "Ibn al-Haytham, who was born in Basra and later worked in Cairo, studied light. Many earlier thinkers "
            "believed that we see because our eyes send out rays. Ibn al-Haytham showed through careful "
            "experiments that light travels from objects into our eyes. He insisted that ideas should be tested, "
            "not simply believed, which is why some people call him one of the first true scientists.\n\n"
            "Al-Jazari was an engineer who designed ingenious machines, including clocks and pumps for raising "
            "water. In his book he drew each machine in detail and explained exactly how to build it, so that "
            "others could make them too.\n\n"
            "Not all of this work was done by famous individuals. In hospitals in cities such as Baghdad and "
            "Cairo, doctors kept records of their patients and trained students on the wards. Many things we take "
            "for granted today were shaped by the patient work of these scholars."
        ),
        "qs": [
            {"id": "9befe9c6d638", "t": "mcq", "d": "retrieve", "q": "What did the scholars at the House of Wisdom do with books from Greece, Persia and India?",
             "opts": ["They translated them into Arabic.",
                      "They sent them on to China.",
                      "They locked them away unread.",
                      "They sold them in Córdoba."],
             "why": "The second paragraph says the scholars gathered the books and translated them into Arabic."},
            {"id": "d49a76d1c7d5", "t": "mcq", "d": "infer", "q": "Why did making paper in Baghdad help learning to grow?",
             "opts": ["Cheaper copies meant more people could own and read books.",
                      "Paper meant that books no longer needed translating.",
                      "Paper lasted far longer than any other material.",
                      "The paper was needed to build the House of Wisdom."],
             "why": "Books could be copied far more cheaply, so more copies could be made and shared."},
            {"id": "05e13973e619", "t": "text", "d": "retrieve", "q": "Which modern word, meaning a set of steps for solving a problem, comes from al-Khwarizmi's name? Find and copy it.",
             "a": ["algorithm"],
             "no": {"algebra": "Algebra comes from part of the title of his book, not from his name."},
             "why": "The third paragraph says his name gives us the word algorithm, a set of steps for solving a problem."},
            {"id": "19ec77a04d9a", "t": "mcq", "d": "compare", "q": "How was Ibn al-Haytham's idea about seeing different from what many earlier thinkers believed?",
             "opts": ["He showed light enters the eyes; they thought the eyes sent out rays.",
                      "He thought the eyes sent out rays; they thought light entered the eyes.",
                      "He showed light travels in curves; they thought it went straight.",
                      "He thought we see only in daylight; they thought we see in the dark."],
             "why": "Earlier thinkers believed the eyes send out rays; his experiments showed light travels from objects into the eyes."},
            {"id": "857a5e1c4c98", "t": "tap", "d": "language", "q": "Tap the word that shows how strongly Ibn al-Haytham felt that ideas must be tested.",
             "s": "He [insisted] that ideas should be tested, not simply believed, which is why some people call him one of the first true scientists.",
             "why": "To insist is to say something firmly and refuse to give way: it shows how strongly he felt."},
            {"id": "1005e3f7c731", "t": "mcq", "d": "vocab", "q": "Al-Jazari designed \"ingenious\" machines. What does \"ingenious\" mean?",
             "opts": ["cleverly thought out", "very large and heavy", "very old-fashioned", "dangerous to use"],
             "why": "Ingenious means clever and inventive: his machines were cleverly designed."},
            {"id": "4c87a4960e3a", "t": "mcq", "d": "summarise", "q": "What is the main idea of the whole text?",
             "opts": ["Scholars of the Islamic Golden Age made discoveries that still shape our world.",
                      "Baghdad was the only city in the world where people studied science.",
                      "Al-Khwarizmi was the most important person of the Islamic Golden Age.",
                      "Paper was first invented in Baghdad during the Islamic Golden Age."],
             "why": "The text describes several scholars and places, and ends by saying many things we take for granted were shaped by their work."},
        ],
    },
    {
        "key": "RD5.08",
        "year": 5,
        "strand": "Poems",
        "title": "The oak tree's story",
        "nc": "Discuss and evaluate how authors use language, including figurative language, considering the impact on the reader",
        "text": (
            "I was an acorn, smooth and brown,\n"
            "Held snug inside my cup,\n"
            "Till autumn winds came shaking down\n"
            "And no one picked me up.\n"
            "I lay among the fallen leaves\n"
            "Beneath my parent tree,\n"
            "And not one person passing by\n"
            "Looked down and noticed me.\n\n"
            "A squirrel found me, grabbed me tight\n"
            "And scampered off to hide\n"
            "His winter store. He dug a hole\n"
            "And tucked me down inside.\n"
            "He meant to come back hungry when\n"
            "The frost made food grow thin,\n"
            "But squirrels often lose their way,\n"
            "And so I stayed tucked in.\n\n"
            "I slept beneath the frozen ground\n"
            "Through weeks of ice and snow,\n"
            "Until the rain of early spring\n"
            "Came trickling down below.\n"
            "My hard shell split; a pale white root\n"
            "Went creeping down to drink;\n"
            "A green shoot climbed towards the sun,\n"
            "Much faster than you'd think.\n\n"
            "At first I was a seedling, thin\n"
            "As any blade of grass,\n"
            "And shook in fear of hungry deer\n"
            "And rabbits as they'd pass.\n"
            "But year by year I stretched my arms\n"
            "And thickened in the stem,\n"
            "Until the deer that ate young shoots\n"
            "Could shelter under them.\n\n"
            "Now I am tall, and broad, and old;\n"
            "A hundred years have passed.\n"
            "My bark is rough, my branches wide,\n"
            "My roots hold firm and fast.\n"
            "The owls and beetles, moths and jays\n"
            "All make their homes in me,\n"
            "And every autumn, from my twigs,\n"
            "I drop my acorns free.\n\n"
            "So if you find an acorn, small\n"
            "And shining in the grass,\n"
            "Remember all that it could be\n"
            "If years enough should pass.\n"
            "Then leave it lying where it fell,\n"
            "Or press it in the ground:\n"
            "The tallest oak in all the wood\n"
            "Began as something round."
        ),
        "qs": [
            {"id": "d6909a127132", "t": "mcq", "d": "structure", "q": "Who is telling the story in this poem?",
             "opts": ["the oak tree itself", "the squirrel", "the parent tree", "a person passing by"],
             "why": "The poem uses \"I\" from start to finish: \"I was an acorn\" and \"Now I am tall\". The oak tells its own life story."},
            {"id": "e592906d08fd", "t": "mcq", "d": "infer", "q": "Why did the squirrel bury the acorn?",
             "opts": ["to keep food to eat later in the winter",
                      "to help a new oak tree start to grow",
                      "to hide it away from the hungry rabbits",
                      "to keep the acorn warm through the frost"],
             "why": "It was part of \"his winter store\", and he meant to come back hungry when food grew scarce."},
            {"id": "ed69285c00d3", "t": "mcq", "d": "language", "q": "In the third verse, a root \"went creeping down to drink\". What does \"creeping\" suggest?",
             "opts": ["It grew slowly and steadily.",
                      "It grew quickly and noisily.",
                      "It grew upwards towards the light.",
                      "It grew along the top of the soil."],
             "why": "Creeping is moving slowly and quietly, which is how a root pushes its way down through the soil."},
            {"id": "4774d95f20bf", "t": "mcq", "d": "compare", "q": "How has the deer's place in the oak's life changed by the end of the fourth verse?",
             "opts": ["Deer once ate its shoots, but now shelter under its branches.",
                      "Deer once sheltered under it, but now they eat its shoots.",
                      "Deer once buried its acorns, but now they ignore the tree.",
                      "Deer once lived inside it, but now they have moved away."],
             "why": "The seedling feared hungry deer, but the grown tree's branches are big enough for deer to shelter under."},
            {"id": "a2175c6984eb", "t": "tap", "d": "retrieve", "q": "Tap the word that describes the oak's bark.",
             "s": "My bark is [rough], my branches wide,",
             "why": "The fifth verse says the bark is rough."},
            {"id": "36c356738912", "t": "order", "d": "sequence", "q": "Put these stages of the oak's life in the order the poem tells them.",
             "items": ["The acorn falls from its parent tree.",
                       "A squirrel buries the acorn.",
                       "The shell splits and a root grows down.",
                       "The thin seedling is in danger from deer.",
                       "The oak drops acorns of its own."],
             "why": "The poem follows the oak's life cycle: seed, burial, the seed beginning to grow, seedling, then a grown tree making new seeds."},
            {"id": "38bcfa754e48", "t": "mcq", "d": "summarise", "q": "What is the main message of the last verse?",
             "opts": ["Even the greatest tree begins as a small seed.",
                      "Acorns found in the grass should be thrown away.",
                      "Squirrels are the most important animals in a wood.",
                      "Oak trees grow faster than any other kind of tree."],
             "why": "The last lines say the tallest oak in the wood \"began as something round\": a tiny acorn."},
        ],
    },
    {
        "key": "RD5.09",
        "year": 5,
        "strand": "Explanations",
        "title": "From raindrop to tap",
        "nc": "Distinguish between statements of fact and opinion",
        "text": (
            "When you turn on a tap, clean water flows out almost at once. It is easy to forget that this water "
            "has made a long journey, and that a great deal of work has gone into making it safe to drink.\n\n"
            "The journey begins with rain. Some of the rain that falls on hills and mountains soaks into the "
            "ground, and some runs off the surface into streams. Streams join together to form rivers, which flow "
            "downhill towards the sea. In many places, a dam has been built across a river valley to hold the "
            "water back, making a large artificial lake called a reservoir. Other water is pumped up from deep "
            "underground, where it collects in layers of rock.\n\n"
            "River and reservoir water may look clear, but it is not yet safe to drink. It can contain mud, "
            "leaves, tiny creatures and germs that could make people ill. So it travels through large pipes to a "
            "water treatment works.\n\n"
            "At the treatment works, the water first passes through screens that catch large objects such as "
            "twigs and litter. Next, it is left to stand in big tanks so that heavy bits of dirt sink to the "
            "bottom. Then it trickles slowly through beds of sand and gravel, which filter out smaller particles. "
            "Finally, a small amount of chlorine is added to kill any germs that remain.\n\n"
            "The clean water is pumped into a network of underground pipes. Some is stored in water towers or "
            "covered tanks on high ground, so that gravity helps to push it through the pipes to homes, schools "
            "and hospitals.\n\n"
            "The story does not end at your sink. Used water from drains and toilets flows through separate pipes, "
            "called sewers, to a sewage works. There it is cleaned again before it is returned to a river, which "
            "carries it back to the sea. The sun warms the sea, water evaporates, clouds form, and the rain falls "
            "once more.\n\n"
            "Cleaning and pumping water uses a great deal of energy. Because of this, it makes sense for all of us "
            "to stop wasting it."
        ),
        "qs": [
            {"id": "66e36d19d24a", "t": "mcq", "d": "retrieve", "q": "What is a reservoir, according to the text?",
             "opts": ["a lake made by building a dam across a river valley",
                      "a layer of rock deep underground where water collects",
                      "a big tank where heavy bits of dirt sink to the bottom",
                      "a tower on high ground where clean water is stored"],
             "why": "The second paragraph says a dam across a valley holds water back, making a large lake called a reservoir."},
            {"id": "99ad2519455a", "t": "mcq", "d": "vocab", "q": "\"A large artificial lake.\" What does \"artificial\" mean here?",
             "opts": ["made by people, not by nature", "very deep and cold", "full of dirty water", "high up in the mountains"],
             "why": "The lake is there because people built a dam, so it is artificial: made by people."},
            {"id": "7da8c0dd6062", "t": "mcq", "d": "language", "q": "Why does the writer say that river water \"may look clear\"?",
             "opts": ["To warn that water can look clean but still carry germs.",
                      "To show that river water is always brown and muddy.",
                      "To explain why so many fish live in rivers.",
                      "To suggest that river water is fine to drink."],
             "why": "The sentence goes on: \"but it is not yet safe to drink\". It may look clear, yet hide mud and germs."},
            {"id": "10b54b03a277", "t": "order", "d": "sequence", "q": "Put the stages at the treatment works in the right order.",
             "items": ["Screens catch twigs and litter.",
                       "Heavy dirt sinks to the bottom of tanks.",
                       "The water trickles through sand and gravel.",
                       "Chlorine is added to kill germs."],
             "why": "The fourth paragraph gives the order with first, next, then and finally."},
            {"id": "926c4cced5d6", "t": "text", "d": "retrieve", "q": "Find and copy the name of the pipes that carry used water away from homes.",
             "a": ["sewers", "sewer", "the sewers", "the sewer"],
             "why": "The sixth paragraph says used water flows through separate pipes, called sewers, to a sewage works."},
            {"id": "9acd8643a480", "t": "mcq", "d": "infer", "q": "The sixth paragraph ends with the rain falling \"once more\". What does this show about the water's journey?",
             "opts": ["It goes round in a cycle that keeps repeating.",
                      "It ends for good once the water reaches the sea.",
                      "It stops for good at the tap in your kitchen.",
                      "It always starts again inside the sewage works."],
             "why": "The water returns to the sea, evaporates and falls as rain again, back where the text began: it is a cycle."},
            {"id": "9a62895b37eb", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion rather than a fact?",
             "opts": ["It makes sense for all of us to stop wasting water.",
                      "Streams join together to form rivers.",
                      "Chlorine is added to the water to kill germs.",
                      "Sewers carry used water to a sewage works."],
             "why": "An opinion is what someone thinks should happen. The others can be checked and proved true."},
        ],
    },
    {
        "key": "RD5.10",
        "year": 5,
        "strand": "Stories",
        "title": "Ruby's line",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions, and justify inferences with evidence",
        "text": (
            "Every Friday, Class 5 practised their assembly in the hall, and every Friday, Ruby dreaded it.\n\n"
            "Ruby had a stammer. Most days nobody noticed much, because she chose her words carefully and spoke "
            "when she was ready. But standing in front of the whole class, with a script in her hand and thirty "
            "faces watching, the words seemed to stick in her throat like toffee.\n\n"
            "This week her line was about the River Severn. “The Severn is the l-l-l…” she began, and stopped.\n\n"
            "At the back, Callum leaned towards his friends and whispered, “The l-l-l-longest river.” Two of the "
            "boys snorted with laughter. Mrs Okafor was at the far side of the hall, sorting out the music, and "
            "did not hear.\n\n"
            "Kwame heard. He felt his face go hot. Callum was his friend; they played football together every "
            "lunchtime, and Kwame did not want to be the one who spoiled things. For a moment he looked at the "
            "floor and said nothing, and he hated how easy that was.\n\n"
            "Then he saw Ruby's hands. They were shaking so much that the script rattled.\n\n"
            "“Stop it, Callum,” Kwame said, loud enough for all the boys to hear. “It isn't funny. You'd hate it "
            "if someone did that to you.”\n\n"
            "Callum stared at him. The other boys went quiet. Ruby took a breath, waited, and said, clearly, “The "
            "Severn is the longest river in Britain.”\n\n"
            "Afterwards, Callum did not speak to Kwame all through lunch, and Kwame kicked a ball against the wall "
            "on his own, wondering whether he had lost a friend.\n\n"
            "But on Monday morning, when Ruby walked into the classroom, Callum looked up. “Sorry about Friday,” "
            "he muttered, so quietly that only Ruby and Kwame heard. Ruby nodded. Kwame said nothing at all, but "
            "he smiled for the rest of the morning."
        ),
        "qs": [
            {"id": "a8b6baf836f3", "t": "mcq", "d": "vocab", "q": "\"Every Friday, Ruby dreaded it.\" What does \"dreaded\" mean?",
             "opts": ["felt very worried about it", "looked forward to it", "forgot all about it", "practised for it"],
             "why": "To dread something is to feel worried or afraid about it before it happens."},
            {"id": "cb26f4f50bb9", "t": "mcq", "d": "language", "q": "The words seemed \"to stick in her throat like toffee\". What does this comparison suggest?",
             "opts": ["The words were very hard to get out.",
                      "Ruby was eating sweets during the practice.",
                      "Ruby's throat was sore from a bad cold.",
                      "The words were sweet and pleasant to say."],
             "why": "Toffee is sticky and hard to swallow; the simile shows that the words got stuck and would not come out."},
            {"id": "bf9dfba87a66", "t": "mcq", "d": "retrieve", "q": "Why did Mrs Okafor not stop Callum?",
             "opts": ["She was busy with the music and did not hear.",
                      "She thought Callum was only joking kindly.",
                      "She had gone out of the hall for a moment.",
                      "She was helping Ruby with her script."],
             "why": "The fourth paragraph says she was at the far side of the hall, sorting out the music, and did not hear."},
            {"id": "bf521ebfd934", "t": "mcq", "d": "infer", "q": "Why did Kwame say nothing at first?",
             "opts": ["He was afraid of spoiling his friendship with Callum.",
                      "He thought that Ruby had not heard what Callum said.",
                      "He agreed that what Callum said was funny.",
                      "He expected Mrs Okafor to deal with it."],
             "why": "Callum was his friend, and Kwame \"did not want to be the one who spoiled things\"."},
            {"id": "7480385d9291", "t": "mcq", "d": "infer", "q": "What made Kwame decide to speak up?",
             "opts": ["He saw how upset Ruby was.",
                      "Mrs Okafor asked him to help.",
                      "Callum began to laugh at him too.",
                      "Ruby asked him to stop the boys."],
             "why": "He spoke straight after seeing Ruby's hands shaking so much that the script rattled."},
            {"id": "79d2f52ec8da", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how Ruby said her line the second time.",
             "s": "Ruby took a breath, waited, and said, [clearly], “The Severn is the longest river in Britain.”",
             "why": "The word clearly shows that, taking the time she needed, Ruby said her whole line the way she wanted to."},
            {"id": "7c42bea143ce", "t": "mcq", "d": "compare", "q": "How did Callum's behaviour change between Friday and Monday?",
             "opts": ["He went from mocking Ruby to saying sorry to her.",
                      "He went from ignoring Kwame to playing football with him.",
                      "He went from being kind to Ruby to teasing her.",
                      "He went from being shy to reading in the assembly."],
             "why": "On Friday he copied Ruby's stammer to make his friends laugh; on Monday he apologised to her."},
        ],
    },
    {
        "key": "RD5.11",
        "year": 5,
        "strand": "Persuasive writing",
        "title": "Leave the car at home",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "Every morning, the road outside Oakfield Primary turns into a traffic jam. Cars queue down the hill "
            "with their engines running, while parents try to squeeze into spaces that are not there. Children "
            "weave between bumpers to reach the gate. It is noisy, it is smelly and, worst of all, it is "
            "dangerous. I believe it is time for a change, and I think every family at our school should walk, "
            "scoot or cycle to school at least three days a week.\n\n"
            "First, think about our health. Doctors say that children need at least an hour of exercise every "
            "day. A fifteen-minute walk each way gives us half of that before lessons have even started. Many "
            "teachers say that pupils who arrive on foot are more awake and ready to learn. Surely that is a "
            "better start to the day than sitting in a hot car?\n\n"
            "Secondly, consider the air we breathe. When cars stand still with their engines running, they pump "
            "out fumes. Those fumes collect right outside our classrooms, at exactly the height of a child's face. "
            "Fewer cars would mean cleaner air for everyone, including the babies in pushchairs and the elderly "
            "neighbours on Mill Lane.\n\n"
            "Some people will say that they live too far away, or that the weather is too wet. But nobody has to "
            "walk the whole way. Families who live a long way off could park at the leisure centre, which is only "
            "ten minutes' walk from school, and go the rest of the way on foot. As for the rain, a good coat costs "
            "far less than a year of petrol.\n\n"
            "Finally, walking is simply more fun. You notice things from the pavement that you never see through "
            "a car window: the heron standing by the canal, the bakery opening its shutters, friends calling your "
            "name across the street.\n\n"
            "So next Monday, leave the car at home. Our school, our health and our planet will thank you.\n\n"
            "Aisha Rahman, Year 5"
        ),
        "qs": [
            {"id": "4c89407dffa3", "t": "mcq", "d": "vocab", "q": "\"Children weave between bumpers to reach the gate.\" What does \"weave\" mean here?",
             "opts": ["move in and out between things", "make cloth from threads", "run in a straight line", "wait patiently in a queue"],
             "why": "Here weave means to dodge in and out, as the children squeeze between the parked cars."},
            {"id": "743ba1a9be3e", "t": "mcq", "d": "language", "q": "\"It is noisy, it is smelly and, worst of all, it is dangerous.\" Why did the writer build the sentence this way?",
             "opts": ["To list the problems and save the most serious one until last.",
                      "To describe what the inside of the school building is like.",
                      "To show that she secretly enjoys the busy morning traffic.",
                      "To explain how all the cars came to be on the road."],
             "why": "\"Worst of all\" tells the reader that the last problem, danger, matters most, so it comes at the end."},
            {"id": "a51237af47b7", "t": "mcq", "d": "retrieve", "q": "What exactly does Aisha want families to do?",
             "opts": ["Walk, scoot or cycle to school at least three days a week.",
                      "Sell their cars and never drive anywhere again.",
                      "Park more carefully outside the school gate.",
                      "Move house so that they live nearer to the school."],
             "why": "The end of the first paragraph says every family should walk, scoot or cycle at least three days a week."},
            {"id": "ee392b3301d5", "t": "text", "d": "retrieve", "q": "How much exercise do doctors say children need every day? Find and copy the words.",
             "a": ["at least an hour", "an hour", "at least an hour of exercise", "an hour of exercise", "one hour", "1 hour"],
             "why": "The second paragraph says doctors say children need at least an hour of exercise every day."},
            {"id": "3f307011af9d", "t": "mcq", "d": "infer", "q": "Why does the writer mention \"the height of a child's face\"?",
             "opts": ["To show that children breathe in the worst of the fumes.",
                      "To show that cars are much taller than children.",
                      "To explain why children cannot see the road.",
                      "To show that the fumes rise high into the sky."],
             "why": "The fumes collect at exactly the height where children breathe, so they are the ones most affected."},
            {"id": "86da85aa8ee7", "t": "mcq", "d": "structure", "q": "What is the job of the fourth paragraph in the argument?",
             "opts": ["It answers reasons people might give for not walking.",
                      "It gives a new reason why walking keeps you healthy.",
                      "It describes the walk from the leisure centre to school.",
                      "It tells readers exactly what to wear in the rain."],
             "why": "It starts \"Some people will say…\" and then answers each objection: distance and wet weather."},
            {"id": "9764eefa043f", "t": "mcq", "d": "purpose", "q": "Who is this text mainly written for?",
             "opts": ["families at Oakfield Primary", "the neighbours on Mill Lane", "doctors and teachers", "the staff at the leisure centre"],
             "why": "Aisha asks \"every family at our school\" to change, and ends by telling them to leave the car at home."},
        ],
    },
    {
        "key": "RD5.12",
        "year": 5,
        "strand": "Letters and diaries",
        "title": "My Science Week diary",
        "nc": "Read books that are structured in different ways and read for a range of purposes",
        "text": (
            "Monday 10 March\n"
            "Mr Patel says that for Science Week we have to keep a diary of every experiment we do. I am not "
            "usually a diary person, but here goes.\n\n"
            "Today we stirred a spoonful of salt into a beaker of warm water. Within a minute the salt had "
            "completely vanished. Jamie said it had disappeared for ever, but Mr Patel just smiled and said, "
            "“Has it?” We were allowed to dip a clean finger in and taste it. It was definitely still salty. So "
            "the salt was still there: it had dissolved.\n\n"
            "Tuesday 11 March\n"
            "We poured some of yesterday's salty water into a shallow dish and left it on the sunny windowsill. "
            "Mr Patel says we have to be patient.\n\n"
            "In the afternoon we melted chocolate in a bowl over hot water, poured it into moulds and put them in "
            "the fridge. By home time it was solid again. Melting is a reversible change, which means you can get "
            "back what you started with. Personally, I would like to reverse it straight into my mouth.\n\n"
            "Wednesday 12 March\n"
            "Still waiting for the dish. Nothing exciting, except that the water level has gone down a little.\n\n"
            "We mixed sand with water and poured it through filter paper in a funnel. The water dripped through "
            "into the beaker, but the sand stayed behind in the paper. It was like a sieve, only with holes too "
            "tiny to see.\n\n"
            "Thursday 13 March\n"
            "Gran helped me bake a cake at home for my science homework. We mixed flour, eggs, sugar and butter, "
            "and the heat of the oven turned the runny mixture into a soft, spongy cake. Gran asked if I could "
            "turn the cake back into eggs and flour. I could not. That is an irreversible change: once it has "
            "happened, there is no going back.\n\n"
            "Friday 14 March\n"
            "The water in the dish has gone! In its place are tiny white crystals around the edge. The water "
            "evaporated and left the salt behind, exactly as Mr Patel said it would. Jamie had to admit that the "
            "salt had been there all along.\n\n"
            "I still do not think I am a diary person, but I might be a scientist."
        ),
        "qs": [
            {"id": "b87d188c3861", "t": "mcq", "d": "infer", "q": "When Mr Patel smiled and asked “Has it?”, what was he hinting?",
             "opts": ["The salt might still be in the water.",
                      "Jamie had not stirred the water enough.",
                      "The salt had turned into water.",
                      "The experiment had gone wrong."],
             "why": "His question doubts Jamie's idea that the salt had gone for ever, and the salty taste proves the salt was still there."},
            {"id": "0b4d8bc081dd", "t": "mcq", "d": "retrieve", "q": "Which detail in the Monday entry proves that the salt had dissolved rather than disappeared?",
             "opts": ["The water still tasted salty.",
                      "The water had turned cloudy.",
                      "The beaker had cooled down.",
                      "The salt sank to the bottom."],
             "why": "The water was \"definitely still salty\", so the salt was still in it."},
            {"id": "39562d2f23bc", "t": "mcq", "d": "vocab", "q": "In the Tuesday entry, what does \"reversible\" mean, as the diary explains it?",
             "opts": ["You can get back what you started with.",
                      "It only happens when something is heated.",
                      "It makes a brand-new material that lasts.",
                      "It happens very slowly over many days."],
             "why": "The diary says a reversible change \"means you can get back what you started with\", like chocolate setting again."},
            {"id": "5df5b0abe56c", "t": "mcq", "d": "language", "q": "\"Personally, I would like to reverse it straight into my mouth.\" Why did the writer add this sentence?",
             "opts": ["To add a joke about wanting to eat the chocolate.",
                      "To explain a new experiment the class tried.",
                      "To show that melting can never be reversed.",
                      "To complain that the chocolate tasted bad."],
             "why": "It is a joke: the writer plays on the word reverse to show they would rather eat the chocolate."},
            {"id": "5d211b5c95bf", "t": "order", "d": "sequence", "q": "Put these events from the diary in the order they happen.",
             "items": ["Salt is stirred into warm water.",
                       "Salty water is left on the windowsill.",
                       "Sand and water are poured through filter paper.",
                       "Gran and the writer bake a cake.",
                       "White crystals are found in the dish."],
             "why": "The dated entries give the order: Monday, Tuesday, Wednesday, Thursday and Friday."},
            {"id": "e38019737c24", "t": "mcq", "d": "compare", "q": "How is baking the cake different from melting the chocolate?",
             "opts": ["Baking cannot be undone, but melting can.",
                      "Melting cannot be undone, but baking can.",
                      "Both changes can be undone very easily.",
                      "Neither change needs any heat at all."],
             "why": "The chocolate set solid again (reversible), but the cake could not be turned back into eggs and flour (irreversible)."},
            {"id": "b137edb01b1d", "t": "text", "d": "retrieve", "q": "In the Friday entry, find and copy the word that tells you what happened to the water in the dish.",
             "a": ["evaporated"],
             "no": {"dissolved": "Dissolving is what the salt did on Monday. On Friday the water itself turned into a gas and left the dish."},
             "why": "The Friday entry says the water evaporated and left the salt behind."},
        ],
    },
    {
        "key": "RD5.13",
        "year": 5,
        "strand": "Stories",
        "title": "Eight hours ahead",
        "nc": "Predict what might happen from details stated and implied",
        "text": (
            "Nadia had never been on a plane before, and the airport at night was the busiest place she had ever "
            "seen. It was the February half-term, and their flight to Kuala Lumpur left London at nine o'clock in the evening. Mum said it would take "
            "about thirteen hours, and that Grandad would be waiting at the other end.\n\n"
            "For the first few hours, Nadia was far too excited to sleep. She watched the tiny plane on the "
            "screen in front of her creep across Europe. She ate a dinner of rice and chicken from a tray with "
            "little compartments. Then the cabin lights dimmed, and at last her eyes closed.\n\n"
            "When she woke, the blinds were up and sunlight was pouring in. Breakfast came round. A few hours "
            "later the plane began its descent, and Nadia pressed her nose to the window. Below her, palm trees "
            "and red rooftops stretched towards green hills.\n\n"
            "Then something strange happened. By the time they had collected their bags and walked out of the "
            "airport, the sky was turning orange and the sun was sinking. “Why is it getting dark?” Nadia asked. "
            "“We've only just had breakfast!”\n\n"
            "Grandad laughed as he lifted her bag into the boot of his car. “Welcome to Malaysia,” he said. "
            "“Here, it is evening. At home in London, it is still morning.”\n\n"
            "That night, on the veranda, he explained. The Earth spins, so the Sun rises over different parts of "
            "the world at different times, and places further east see the sunrise first. To keep clocks in step "
            "with the daylight, the world is divided into time zones. In winter, Malaysia is eight hours ahead of "
            "the United Kingdom, so when Nadia's friends at home were eating their lunch, she would be getting "
            "ready for bed.\n\n"
            "“So I've lost eight hours?” Nadia said.\n\n"
            "“You'll get them back when you fly home,” said Grandad. “But your body will need a few days to catch "
            "up.”\n\n"
            "He was right. At two o'clock that morning, Nadia was wide awake, listening to the frogs croaking in "
            "the dark garden and wishing it was time for breakfast."
        ),
        "qs": [
            {"id": "cec8032455ac", "t": "mcq", "d": "retrieve", "q": "At what time did the flight leave London?",
             "opts": ["nine o'clock in the evening", "nine o'clock in the morning", "two o'clock in the morning", "eight o'clock in the evening"],
             "why": "The first paragraph says the flight left London at nine o'clock in the evening."},
            {"id": "e518b86e8154", "t": "tap", "d": "language", "q": "Tap the verb that tells you how strongly the light was coming into the plane.",
             "s": "When she woke, the blinds were up and sunlight was [pouring] in.",
             "why": "Pouring makes the sunlight sound like a flood of water: there was plenty of it."},
            {"id": "c9fe6f02108a", "t": "mcq", "d": "vocab", "q": "\"The plane began its descent.\" What does \"descent\" mean?",
             "opts": ["the journey down towards the ground", "the long flight across Europe", "the start of the flight", "the time when breakfast is served"],
             "why": "A descent is a movement downwards: the plane was coming down to land."},
            {"id": "9696eab97a69", "t": "mcq", "d": "infer", "q": "Why was Nadia puzzled when they came out of the airport?",
             "opts": ["It felt like morning to her, but it was evening there.",
                      "She had expected the weather to be cold and wet.",
                      "Grandad was not there to meet them as promised.",
                      "She had never seen palm trees or red roofs before."],
             "why": "She had \"only just had breakfast\", yet the sun was setting: her day and Malaysia's did not match."},
            {"id": "0f3363620336", "t": "text", "d": "retrieve", "q": "In winter, how many hours ahead of the United Kingdom is Malaysia? Type the number.",
             "a": ["8", "eight", "8 hours", "eight hours"],
             "why": "Grandad explains that in winter Malaysia is eight hours ahead of the United Kingdom."},
            {"id": "d593e6f4da38", "t": "mcq", "d": "predict", "q": "What is most likely to happen to Nadia over the next few days?",
             "opts": ["Her body will slowly get used to Malaysian time.",
                      "She will decide to fly straight back to London.",
                      "She will stay awake every night of the holiday.",
                      "Grandad will change all his clocks to London time."],
             "why": "Grandad says her body \"will need a few days to catch up\", so she will gradually adjust."},
            {"id": "00d2d70fb9ff", "t": "mcq", "d": "summarise", "q": "Which of these titles would also suit the whole story?",
             "opts": ["The Upside-Down Day", "Lost at the Airport", "Dinner on a Tray", "The Frogs in the Garden"],
             "why": "The story is about the time difference that turns Nadia's day upside down. The other titles are small details."},
        ],
    },
    {
        "key": "RD5.14",
        "year": 5,
        "strand": "Information",
        "title": "What the ancient Greeks gave us",
        "nc": "Summarise the main ideas drawn from more than one paragraph, identifying key details that support the main ideas",
        "text": (
            "About two and a half thousand years ago, Greece was not one country but many separate city-states. "
            "Each city-state, such as Athens or Sparta, had its own laws, its own army and its own way of life. "
            "Although they often quarrelled and sometimes fought, the ancient Greeks shared a language and many "
            "ideas, and some of those ideas still shape the way we live today.\n\n"
            "One of the most famous is democracy, a word made from Greek words meaning “rule by the people”. In "
            "Athens, citizens met in a large open-air assembly to discuss new laws and then voted on them, often "
            "by raising their hands. This was a remarkable idea, but it had limits. Only free men from Athenian "
            "families counted as citizens. Women, enslaved people and people from other places could not vote at "
            "all.\n\n"
            "The Greeks also loved sport. Every four years, athletes from across the Greek world travelled to "
            "Olympia to compete in running, wrestling, boxing, chariot racing and other events. Winners did not "
            "receive gold medals; they were crowned with a wreath of olive leaves. The modern Olympic Games, first "
            "held in Athens in 1896, were inspired by these ancient contests.\n\n"
            "Greek thinkers asked big questions about the world and tried to answer them by reasoning and "
            "observing, rather than simply accepting old stories. Pythagoras and his followers studied numbers "
            "and shapes, and his name is still attached to a rule about right-angled triangles that pupils learn "
            "in secondary school. Hippocrates, a doctor, taught that illnesses have natural causes and that "
            "doctors should watch their patients carefully. Archimedes, who lived in the Greek city of Syracuse, "
            "worked out how objects float and invented machines for lifting heavy loads.\n\n"
            "The Greeks were also great builders and writers. They built open-air theatres into hillsides, shaped "
            "so that an actor's voice could carry to thousands of people sitting on stone seats. Plays were "
            "performed in competitions, and audiences came to watch both comedies and tragedies.\n\n"
            "So next time you watch a race, vote in a class election or sit in a theatre, remember that ideas from "
            "ancient Greece helped to make them possible."
        ),
        "qs": [
            {"id": "da7b54c2c100", "t": "mcq", "d": "retrieve", "q": "According to the first paragraph, what did the separate city-states share?",
             "opts": ["a language and many ideas", "one army and one set of laws", "the same ruler", "a single capital city"],
             "why": "The first paragraph says each city-state had its own laws and army, but they shared a language and many ideas."},
            {"id": "98e550c219c2", "t": "text", "d": "vocab", "q": "Find and copy the words that give the meaning of the word democracy.",
             "a": ["rule by the people"],
             "why": "The second paragraph says democracy is made from Greek words meaning “rule by the people”."},
            {"id": "6f7f58d0a9e1", "t": "mcq", "d": "infer", "q": "Why does the writer say that democracy in Athens \"had limits\"?",
             "opts": ["Many people who lived in Athens were not allowed to vote.",
                      "Citizens were allowed to vote only once in their lives.",
                      "The assembly met only once every four years.",
                      "Voting by raising hands was too hard to count."],
             "why": "Only free men from Athenian families could vote; women, enslaved people and outsiders could not."},
            {"id": "dec8bcd063e4", "t": "mcq", "d": "retrieve", "q": "Which difference between the ancient and the modern Olympic Games does the text mention?",
             "opts": ["Ancient winners got olive wreaths, not gold medals.",
                      "Ancient games were held every year, not every four.",
                      "Ancient games were held in Athens, not in Olympia.",
                      "Ancient games had no running races, only wrestling."],
             "why": "The third paragraph says winners \"did not receive gold medals; they were crowned with a wreath of olive leaves\"."},
            {"id": "8c790414acc8", "t": "tap", "d": "retrieve", "q": "Tap the two words that show how Greek thinkers tried to answer their questions.",
             "s": "Greek thinkers asked big questions about the world and tried to answer them by [reasoning] and [observing], rather than simply accepting old stories.",
             "why": "They answered questions by reasoning (thinking things through) and observing (watching carefully)."},
            {"id": "ce2c1e51d10b", "t": "mcq", "d": "retrieve", "q": "What did Archimedes work out, according to the text?",
             "opts": ["how objects float", "a rule about right-angled triangles", "that illnesses have natural causes", "how to build theatres into hillsides"],
             "why": "The fourth paragraph says Archimedes worked out how objects float. The triangle rule is Pythagoras; illnesses are Hippocrates."},
            {"id": "12b303b379cc", "t": "mcq", "d": "summarise", "q": "What is the main idea of the whole text?",
             "opts": ["Many ideas from ancient Greece are still part of our lives today.",
                      "Athens and Sparta were always fighting each other.",
                      "The ancient Greeks cared about sport more than anything.",
                      "Greek theatres were much bigger than modern theatres."],
             "why": "Each paragraph gives a Greek idea (democracy, the Olympics, science, theatre), and the last links them to life today."},
        ],
    },
]
