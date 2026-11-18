"""Reading comprehension, Year 8 (KS3), second set (RD8.13-RD8.24).

Twelve more original passages, written by hand for this bank (none copied or paraphrased from a published
text), each 350-550 words with seven questions, at the same Year 8 depth as reading_y8.py: implicit meaning
and inference from evidence, the writer's methods (language, structure, tone), viewpoint, fact and opinion,
and comparing ideas and attitudes within one text. Topics differ from the first set.

Passages: a boy who interprets for his mother at parents' evening; how the Channel Tunnel was dug; a poem
about a bakery at dawn and the city's early workers; what causes the tides; John Harrison and the sea clock; an
opinion article in praise of boredom; a diary from a bird observatory on Fair Isle; a local
news report on otters returning to a river; a play scene about a group project; a boy twisting his first cord
for a grass rope bridge in the Andes; William Roy, triangulation and the Ordnance Survey; a girl's first repair
at a repair café.

Non-fiction facts are limited to well-established ones taught in English schools; the news report, diary,
article and stories are fiction with invented people and places. Written for review line by line by a second
reviewer (a teacher of KS3 English) before use.
"""

SKILLS = [
    # ------------------------------------------------------------------ RD8.13
    {
        "key": "RD8.13",
        "year": 8,
        "strand": "Stories",
        "title": "The Interpreter",
        "nc": "Read critically: study setting, plot and characterisation, and the effects of these",
        "text": "Every parents' evening, Daniyar became two people. In English he was a Year 8 pupil with an untucked shirt and a planner he had forgotten to get signed. In Kazakh he was his mother's voice.\n\n"
                "They sat at the small table outside the science lab, his mother upright in her good grey coat, her handbag held on her knees like something that might be taken away. Mrs Hollis smiled at them both and opened her laptop.\n\n"
                "“Daniyar is a lovely member of the class,” she began. Daniyar translated this at once, and his mother's shoulders came down a little.\n\n"
                "“He's clearly very able. His test results are some of the best in the year.” He translated that too, more slowly, so that it would last.\n\n"
                "Then Mrs Hollis turned the laptop round. “But I'm worried about homework. He's handed in two pieces out of the last seven. When I ask him, he tells me he forgot.”\n\n"
                "There was a pause. In the pause, Daniyar could hear the hum of the drinks machine at the end of the corridor and a younger child somewhere complaining about the wait. His mother was looking at him with the patient, trusting face she wore at the bank and the post office and the doctor's, all the places where the words belonged to him.\n\n"
                "It would be so easy. He could say that Mrs Hollis wanted him to keep working hard. He could say anything at all.\n\n"
                "“She says,” he began in Kazakh, and stopped. His mouth was dry. “She says I have only handed in two homeworks out of seven. She says I tell her I forget.”\n\n"
                "He did not look at his mother. He looked at the laptop, at the row of red boxes that had been waiting there all term.\n\n"
                "His mother said nothing for a moment. Then she spoke quietly, and Daniyar turned to Mrs Hollis.\n\n"
                "“My mother asks,” he said, “why I didn't tell her.”\n\n"
                "He realised, as he said it, that the question was not really for the teacher.\n\n"
                "That night, at the kitchen table, his mother put his science book in front of him and sat down opposite with her own notebook, the one in which she copied English words she meant to learn. For an hour they worked side by side without speaking much. Sometimes she pointed at a word in his book and he told her what it meant; sometimes he asked her to test him, and she read out the questions in her careful accent, and he answered.\n\n"
                "At ten o'clock she closed her notebook. “Tomorrow,” she said in English, “you tell me the homework. I check.”\n\n"
                "It was the first time she had said a whole sentence to him in English. Daniyar found, to his surprise, that he did not mind at all.",
        "qs": [
            {"id": "78b9186616bd", "t": "text", "d": "retrieve", "q": "Find and copy the name of the language Daniyar speaks with his mother.",
             "a": ["Kazakh"],
             "why": "The first paragraph says: “In Kazakh he was his mother's voice.”"},
            {"id": "ef505d6cbe8f", "t": "mcq", "d": "language", "q": "His mother holds her handbag on her knees “like something that might be taken away”. What does this simile suggest about her?",
             "opts": ["She feels uneasy and out of place in the school",
                      "She has seen a thief waiting in the corridor",
                      "She is in a hurry to leave and go back home",
                      "She has brought a present to give the teacher"],
             "no": {"She has seen a thief waiting in the corridor": "Nobody in the story steals anything. The simile describes how she holds the bag, which shows how she feels."},
             "why": "Gripping a bag as if someone might take it shows tension: she is not relaxed in a place where she cannot understand what is said."},
            {"id": "55b38206a680", "t": "mcq", "d": "infer", "q": "Why does Daniyar translate the praise about his test results slowly?",
             "opts": ["He wants his mother to enjoy the good news for longer",
                      "He cannot remember the Kazakh words for test results",
                      "His mother has asked him to speak more slowly to her",
                      "He wants Mrs Hollis to notice how carefully he works"],
             "why": "The writer says he spoke slowly “so that it would last”: he is stretching out the good moment, perhaps because he knows the bad news is coming."},
            {"id": "83b14437b7e6", "t": "mcq", "d": "language", "q": "The writer describes the bank, the post office and the doctor's as “all the places where the words belonged to him”. What does this suggest?",
             "opts": ["In those places his mother relies on him to speak for her",
                      "He keeps a list of useful English words for those places",
                      "Those places are where he first learned to speak English",
                      "He is the only person in those places who speaks Kazakh"],
             "why": "His mother cannot speak English there, so the English words are his: he does the talking, and she has to trust what he says."},
            {"id": "488e9d940bba", "t": "tap", "d": "infer", "q": "Tap the word that shows Daniyar was nervous as he began to tell the truth.",
             "s": "His mouth was [dry].",
             "why": "A dry mouth is a sign of nerves: he is frightened of what his mother will think when she hears the truth."},
            {"id": "6229a143b50b", "t": "mcq", "d": "compare", "q": "How is the mother's part in Daniyar's schoolwork different at the end of the story from the start?",
             "opts": ["She now plans to check his homework herself, not just rely on his words",
                      "She no longer trusts him, so she refuses to speak to him at all",
                      "She now asks the teacher to send all his homework to her in Kazakh",
                      "She has decided to stop learning English so he can help her instead"],
             "no": {"She no longer trusts him, so she refuses to speak to him at all": "She does not refuse to speak to him: she sits with him for an hour and speaks to him in English."},
             "why": "At the start she depends on Daniyar to tell her what is said. At the end she takes charge: “Tomorrow, you tell me the homework. I check.”"},
            {"id": "4d84f208ae35", "t": "mcq", "d": "summarise", "q": "Which best describes the choice at the centre of the story?",
             "opts": ["Whether to translate the teacher's bad news honestly",
                      "Whether to tell the teacher that his mother is unwell",
                      "Whether to leave parents' evening before it is his turn",
                      "Whether to ask the teacher for more time to do his work"],
             "why": "Daniyar could “say anything at all”, because only he understands both languages. He chooses to tell his mother exactly what Mrs Hollis said."},
        ],
    },
    # ------------------------------------------------------------------ RD8.14
    {
        "key": "RD8.14",
        "year": 8,
        "strand": "Information",
        "title": "Under the Channel",
        "nc": "Understand increasingly challenging texts: make inferences and refer to evidence in the text",
        "text": "For as long as people have crossed the English Channel, some have dreamed of going under it instead. In 1802 a French engineer drew up plans for a tunnel to carry horse-drawn coaches, lit by oil lamps, with an artificial island halfway across where the horses could be changed. It was never begun.\n\n"
                "The first real digging came in the 1880s, when boring machines cut more than a kilometre of tunnel out from each coast. Then the work stopped. Many people in Britain feared that an enemy army might one day march through the tunnel, and for nearly a century the idea was set aside. Another attempt in the 1970s was abandoned after a short time, largely because of its cost. In 1986 Britain and France signed an agreement, and two years later the digging began again, this time for good.\n\n"
                "The engineers' first problem was the rock. Under the Channel lie layers of chalk, but not all chalk is alike. The tunnellers looked for one particular layer called chalk marl, which is soft enough to cut easily but contains enough clay to keep most of the seawater out. Because this layer dips and rises beneath the seabed, the tunnels were steered to follow it, which is why they are not perfectly straight.\n\n"
                "The digging was done by huge tunnel boring machines. At the front of each, a rotating cutting head ground away the rock; behind it, the machine lined the new tunnel with curved concrete segments, ring after ring. Teams worked from England and from France at the same time, guided by lasers and careful calculation. On 1 December 1990 the British and French teams met beneath the sea. The two ends were less than a metre out of line: after many kilometres of digging in the dark, it was a remarkable piece of accuracy.\n\n"
                "There are in fact three tunnels, not one. Two carry trains, one in each direction. Between them runs a smaller service tunnel, used by maintenance teams and as a safe place for passengers to escape to in an emergency. Altogether the tunnel is about 50 kilometres long, and more of it lies under the sea than of any other tunnel in the world.\n\n"
                "Digging on this scale produced millions of tonnes of crushed chalk. On the British side, much of it was used to build new land at the foot of the white cliffs near Dover. Today that land is a nature reserve called Samphire Hoe, where wild flowers grow on rock that once lay deep beneath the seabed.\n\n"
                "The tunnel opened in 1994. A crossing that had always depended on ships, tides and the weather can now be made by train, in any season, in the dry.",
        "qs": [
            {"id": "edde8bbcc179", "t": "mcq", "d": "retrieve", "q": "In the plan of 1802, what was the artificial island halfway across for?",
             "opts": ["changing the horses", "refilling the oil lamps",
                      "letting ships pass by", "storing the dug-out rock"],
             "why": "The first paragraph says the island was “where the horses could be changed”."},
            {"id": "fae5af43a2bd", "t": "mcq", "d": "retrieve", "q": "According to the text, why did the digging of the 1880s stop?",
             "opts": ["People feared an enemy army could use the tunnel",
                      "The boring machines could not cut through chalk",
                      "Seawater flooded the tunnel from the French side",
                      "Britain and France could not agree on the cost"],
             "no": {"Britain and France could not agree on the cost": "Cost is the reason the text gives for the attempt in the 1970s, not the one in the 1880s."},
             "why": "The second paragraph says many people in Britain “feared that an enemy army might one day march through the tunnel”."},
            {"id": "f304a90dfd86", "t": "mcq", "d": "vocab", "q": "“Another attempt in the 1970s was abandoned after a short time.” What does abandoned mean here?",
             "opts": ["given up before it was finished", "left empty and falling into ruin",
                      "kept secret from the public", "handed over to another country"],
             "no": {"left empty and falling into ruin": "An abandoned building is left empty, but here it is an attempt: the work was given up."},
             "why": "An attempt that is abandoned is stopped and given up; the digging only began again “for good” in 1988."},
            {"id": "06bae6ad5c10", "t": "text", "d": "retrieve", "q": "Find and copy the name of the layer of rock that the tunnellers followed.",
             "a": ["chalk marl", "the chalk marl", "chalk marls"],
             "why": "The third paragraph says they looked for “one particular layer called chalk marl”."},
            {"id": "492199d5eeca", "t": "mcq", "d": "infer", "q": "What does the third paragraph suggest would have happened if the tunnels had been dug through other layers of chalk?",
             "opts": ["More seawater would have leaked into the tunnels",
                      "The tunnels would have come out far from Dover",
                      "The boring machines would have cut much faster",
                      "The tunnels would have needed no concrete lining"],
             "why": "Chalk marl was chosen because its clay keeps “most of the seawater out”, which suggests the other chalk would let more water in."},
            {"id": "2065506e43a6", "t": "tap", "d": "language", "q": "Tap the word that shows the writer's admiration for how closely the two ends met.",
             "s": "The two ends were less than a metre out of line: after many kilometres of digging in the dark, it was a [remarkable] piece of accuracy.",
             "why": "“Remarkable” means worth noticing because it is so impressive: the writer is praising the engineers' accuracy."},
            {"id": "317a3d384803", "t": "order", "d": "sequence", "q": "Put these in the order they happened, according to the text.",
             "items": ["A French engineer plans a tunnel for coaches", "Boring machines dig out from each coast, then stop",
                      "An attempt is given up, largely because of its cost", "The British and French teams meet under the sea",
                      "The tunnel opens"],
             "why": "The plan was in 1802, the first digging in the 1880s, the abandoned attempt in the 1970s, the meeting in 1990 and the opening in 1994."},
        ],
    },
    # ------------------------------------------------------------------ RD8.15
    {
        "key": "RD8.15",
        "year": 8,
        "strand": "Poems",
        "title": "Saturday Shift",
        "nc": "Read critically: recognise a range of poetic conventions and understand how these have been used",
        "text": "At four the alarm is a small rude bird\nand Mum is already dressed, already\na shape in the hall with the keys in her hand.\nI go with her on Saturdays. I tell my friends\nit's for the money. It isn't\nfor the money.\n\n"
                "Outside, the street is a photograph of a street:\ncars parked in their sleep, every curtain shut,\na fox that stops in the middle of the road\nand stares at us as if we were the strangers,\nwhich, at this hour, I suppose we are.\nThen it trots off to finish its rounds.\n\n"
                "The night bus passes, lit up like a fish tank,\nthree passengers inside, each one alone\nwith a window and a face reflected in it.\nA man in an orange jacket sweeps the gutter\nin long, slow strokes, the way you'd stroke a cat,\nand nods to Mum as if they're old colleagues.\n\n"
                "They are, in a way. They are the people\nwho put the city back together every night\nwhile the rest of it is sleeping:\nthe sweeper and the driver and the cleaner,\nthe nurse who's walking home across the car park,\nand my mum, with flour already on her sleeve.\n\n"
                "The bakery is warm before we've switched a thing on,\nas if the ovens still remember yesterday.\nMum ties her apron with one quick tug.\nShe does not talk much at this hour. Her hands\ndo the talking: they fold and press and turn\nthe dough a hundred times, never hurried, never late.\n\n"
                "I am allowed the rolls. I weigh each one,\na soft white ball of dough on the silver scale,\nand if it's wrong I pinch a little off\nor add a little on, until the needle settles.\nMum says that's the whole secret of baking.\nI think she means the whole secret of everything.\n\n"
                "By six the windows are grey, then pale, then gold.\nThe first van comes. The first old man,\nhis folded paper tucked beneath his arm,\ntaps on the glass before we've turned the sign,\nand Mum lets him in anyway, because\nshe always does, because he's always first.\n\n"
                "Later my friends will wake and eat their toast\nand never think about the hands that made it,\nthe sweeper's broom, the driver's yawn, the fox.\nThat's fine. That's how it works. The city sleeps\nand we keep watch. But I know now, every Saturday,\nwhose morning it really is.",
        "qs": [
            {"id": "51b616a393e0", "t": "mcq", "d": "infer", "q": "In the first verse the speaker says, “It isn't / for the money.” What does this suggest?",
             "opts": ["The speaker has a real reason that the friends are not told",
                      "The speaker is not paid anything at all for the work",
                      "The speaker's friends have dared the speaker to go",
                      "The speaker is saving up to buy a bakery one day"],
             "no": {"The speaker is not paid anything at all for the work": "The speaker does not say there is no pay; the point is that money is not the real reason for going."},
             "why": "The speaker gives the friends an easy reason, money, then admits it is not the real one. The rest of the poem shows the real reasons: time with Mum and the early city."},
            {"id": "a6dfb9ea9a6e", "t": "mcq", "d": "language", "q": "“Outside, the street is a photograph of a street”. What does this metaphor suggest about the street?",
             "opts": ["It is so still that nothing in it seems to move",
                      "It is brightly coloured, like a holiday picture",
                      "It is a street the speaker has never seen before",
                      "It is so dark that the speaker cannot see it"],
             "why": "A photograph is frozen: nothing moves in it. The parked cars “in their sleep” and the shut curtains show the same stillness."},
            {"id": "8cb8297db785", "t": "text", "d": "retrieve", "q": "Find and copy the name of the animal that stops in the middle of the road.",
             "a": ["fox", "a fox", "the fox", "foxes"],
             "why": "The second verse describes “a fox that stops in the middle of the road”."},
            {"id": "72746dab95ad", "t": "tap", "d": "language", "q": "Tap the two words that tell you what the lit-up night bus is compared to.",
             "s": "The night bus passes, lit up like a [fish] [tank], three passengers inside, each one alone with a window and a face reflected in it.",
             "why": "The simile “like a fish tank” pictures a bright glass box in the dark, with a few silent figures inside, each one separate."},
            {"id": "b4406737b10a", "t": "mcq", "d": "vocab", "q": "The sweeper nods to Mum “as if they're old colleagues”. What are colleagues?",
             "opts": ["people who work alongside each other", "people who live in the same street",
                      "people who were at school together", "people who belong to the same family"],
             "why": "Colleagues are people who work together. The next verse explains why the word fits: they are all part of the city's night workforce."},
            {"id": "f3256e977ca0", "t": "mcq", "d": "infer", "q": "Mum says weighing the rolls is “the whole secret of baking”. What does the speaker think she really means?",
             "opts": ["Small, careful adjustments until things are right matter in all of life",
                      "Baking is the most important job that anyone in a city can do",
                      "Mum has a secret recipe that she will not share with anyone",
                      "The speaker should only be trusted with the easiest jobs"],
             "why": "Pinching a little off or adding a little on “until the needle settles” is patient care. The speaker thinks this is “the whole secret of everything”, not just of baking."},
            {"id": "140d95158cdf", "t": "mcq", "d": "summarise", "q": "Which best sums up the main idea of the poem?",
             "opts": ["The city depends on early workers most people never notice, and the speaker now values them",
                      "Working early in a bakery is tiring, and the speaker would rather stay in bed like friends",
                      "The city before dawn is a lonely place that is best avoided by anyone who can sleep",
                      "The speaker's friends are lazy for sleeping late and should help in the bakery too"],
             "no": {"The speaker's friends are lazy for sleeping late and should help in the bakery too": "The speaker does not blame the friends: “That's fine. That's how it works.”"},
             "why": "The poem lists the people who “put the city back together every night” and ends with the speaker's pride: “whose morning it really is”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.16
    {
        "key": "RD8.16",
        "year": 8,
        "strand": "Explanations",
        "title": "What Makes the Tides",
        "nc": "Read a wide range of non-fiction: follow an explanation and the evidence and reasoning in it",
        "text": "Stand on almost any beach in Britain for a day and you will watch the sea creep up the sand and slide back again, not once but twice. A high tide comes roughly every twelve hours and twenty-five minutes, so each day the high tides arrive about fifty minutes later than the day before. Fishing crews, sailors and anyone exploring rock pools need to know when they will come. But what makes them happen at all?\n\n"
                "The main cause is the Moon. Every object pulls on every other object through the force of gravity, and the Moon's pull on the Earth is strong enough to move whole oceans. Water on the side of the Earth nearest the Moon is pulled towards it most strongly, so it heaps up into a bulge.\n\n"
                "The puzzling part is that there is a second bulge, on the side of the Earth facing away from the Moon. The reason is that the Moon's pull weakens with distance. It pulls the solid Earth more strongly than it pulls the water on the far side, so the Earth is drawn very slightly away from that water, which is left behind as a second heap.\n\n"
                "As the Earth spins once a day, each coast is carried through both bulges in turn, giving two high tides and, between them, two low tides. Meanwhile the Moon is moving along its orbit in the same direction as the Earth spins, so each day the Earth has to turn a little further to catch up with it. That is why the tides are later each day.\n\n"
                "The Sun pulls on the oceans too, but because it is so much further away, its effect on the tides is less than half that of the Moon. When the Sun, the Moon and the Earth are lined up, at new moon and full moon, their pulls add together. The result is spring tides: the highest high tides and the lowest low tides. The name has nothing to do with the season; it comes from the idea of the water springing up. When the Sun and the Moon pull at right angles to each other, at half moon, their pulls partly cancel out. These are called neap tides, and the difference between high and low water is much smaller.\n\n"
                "The shape of the land matters as well. In the open ocean the rise and fall is gentle, often less than a metre, and enclosed seas such as the Mediterranean have very small tides. But where a wide bay narrows into a funnel, the incoming water is squeezed and forced higher. The Severn Estuary, between England and Wales, has one of the largest tidal ranges in the world: at spring tides the water can rise and fall by more than twelve metres.",
        "qs": [
            {"id": "8a42e322331b", "t": "mcq", "d": "retrieve", "q": "According to the text, roughly how long is it from one high tide to the next?",
             "opts": ["twelve hours and twenty-five minutes", "twenty-four hours and fifty minutes",
                      "six hours and twenty-five minutes", "twelve hours and fifty minutes"],
             "no": {"twelve hours and fifty minutes": "Fifty minutes is how much later the tides come each day; the gap between two high tides is twelve hours and twenty-five minutes."},
             "why": "The first paragraph says “a high tide comes roughly every twelve hours and twenty-five minutes”."},
            {"id": "8db20116bb72", "t": "mcq", "d": "retrieve", "q": "According to the text, why is there a bulge of water on the side of the Earth facing away from the Moon?",
             "opts": ["The Moon pulls the solid Earth more strongly than that water",
                      "The Sun pulls that water towards it at the same time",
                      "The spinning Earth flings that water outwards into a heap",
                      "The Moon pulls that water more strongly than the near side"],
             "no": {"The spinning Earth flings that water outwards into a heap": "The text does not give the Earth's spin as the cause. It says the Earth is drawn away from the far-side water because the Moon pulls the Earth more strongly."},
             "why": "The third paragraph explains that the Moon's pull weakens with distance, so the Earth is drawn slightly away from the far-side water, which is “left behind as a second heap”."},
            {"id": "a84a29ae7c21", "t": "mcq", "d": "structure", "q": "The third paragraph begins, “The puzzling part is that there is a second bulge”. Why does the writer open it like this?",
             "opts": ["To admit that the next idea is surprising before explaining it",
                      "To show that scientists still do not know why tides happen",
                      "To change the subject from the Moon to the Sun's effect",
                      "To warn the reader that the rest of the text is less reliable"],
             "why": "Calling it “puzzling” prepares the reader for an idea that seems strange, then the paragraph explains it step by step."},
            {"id": "864dc1f8e1e0", "t": "mcq", "d": "compare", "q": "How does the Sun's effect on the tides compare with the Moon's, according to the text?",
             "opts": ["It is less than half as strong, because the Sun is much further away",
                      "It is twice as strong, because the Sun is so much bigger than the Moon",
                      "It is about the same, so the two together cause the second bulge",
                      "It is only felt at half moon, when the Sun and Moon pull together"],
             "no": {"It is twice as strong, because the Sun is so much bigger than the Moon": "The Sun is bigger, but the text says that because it is so far away its effect on the tides is “less than half that of the Moon”."},
             "why": "The fifth paragraph says that because the Sun is so much further away, “its effect on the tides is less than half that of the Moon”."},
            {"id": "6ed3a84a2add", "t": "tap", "d": "retrieve", "q": "Tap the word that names the small tides that come when the Sun and the Moon pull at right angles.",
             "s": "These are called [neap] tides, and the difference between high and low water is much smaller.",
             "why": "At half moon the pulls “partly cancel out”, giving neap tides, with a small difference between high and low water."},
            {"id": "cef3efd4d5ff", "t": "mcq", "d": "infer", "q": "A family plans a trip to the Severn Estuary on the night of a full moon. What should they expect, according to the text?",
             "opts": ["A very large rise and fall of the water", "Almost no tide at all that night",
                      "Only one high tide instead of two", "A smaller tide than at half moon"],
             "why": "A full moon brings spring tides, the biggest of the month, and the funnel shape of the Severn Estuary makes its tides among the largest in the world."},
            {"id": "41f5423e1add", "t": "mcq", "d": "vocab", "q": "“Enclosed seas such as the Mediterranean have very small tides.” What does enclosed mean here?",
             "opts": ["almost surrounded by land", "kept calm by walls and gates",
                      "closed to ships for part of the year", "very deep and far from any coast"],
             "why": "An enclosed sea is shut in by land on almost every side, so the tidal bulges cannot build up in it as they do in the open ocean."},
        ],
    },
    # ------------------------------------------------------------------ RD8.17
    {
        "key": "RD8.17",
        "year": 8,
        "strand": "Biography",
        "title": "John Harrison and the Problem of Longitude",
        "nc": "Read a wide range of non-fiction: biography; how the writer presents a person and judges events",
        "text": "In the early 1700s, a ship's captain far out at sea could find his latitude, how far north or south he was, by measuring the height of the sun at noon. Finding his longitude, how far east or west he was, was another matter. Ships ran aground on coasts they believed were many miles away, and over the years thousands of sailors died. In 1714 Parliament offered a prize of up to £20,000, a fortune at the time, to anyone who could solve the problem.\n\n"
                "In theory, the answer was time. The Earth turns through 360 degrees every 24 hours, which is 15 degrees every hour. If a navigator knew the exact time at his home port, he could compare it with noon where the ship was, and the difference would give his longitude. But that needed a clock that kept almost perfect time on a rolling, damp ship, through heat and cold, for months on end. Pendulum clocks were useless at sea, and many learned men believed that such a clock could never be built.\n\n"
                "John Harrison was not a learned man, or at least not the kind that learned men recognised. Born in Yorkshire in 1693, he grew up in a village in Lincolnshire and trained as a carpenter, like his father. He taught himself clockmaking, and his first clocks were made almost entirely of wood, even the toothed wheels. For some parts he chose a tropical wood so naturally oily that it needed no oil at all, at a time when oil that thickened in the cold was one of the main reasons clocks went wrong.\n\n"
                "Harrison's first sea clock, now called H1, was finished in 1735. It was a large, heavy machine of brass, and on a trial voyage to Lisbon it performed well. Harrison, however, was not satisfied. He spent more than twenty years building two more sea clocks, each better than the last, and then took a completely different direction. His fourth timekeeper, H4, finished in 1759, looked like an oversized pocket watch, about thirteen centimetres across.\n\n"
                "In 1761 his son William sailed with H4 to Jamaica. After more than two months at sea, it was out by only about five seconds. A second trial, to Barbados, was just as successful. Yet the Board of Longitude, the committee in charge of the prize, would not pay in full. Some of its members suspected luck; others preferred a rival method that used the positions of the Moon and stars. They demanded his drawings, his clocks and proof that other craftsmen could make copies.\n\n"
                "A copy was made, and Captain James Cook took it on his second great voyage in the 1770s and praised it highly. By then Harrison was an old man. In 1773, after King George III took his side, Parliament granted him a large sum of money, although he was never officially awarded the prize. He died three years later.\n\n"
                "Today his sea clocks are kept at the Royal Observatory in Greenwich. The carpenter whom the experts doubted had solved one of the great problems of his age.",
        "qs": [
            {"id": "31c4fceccb7c", "t": "mcq", "d": "retrieve", "q": "According to the text, how could a captain in the early 1700s find his latitude?",
             "opts": ["by measuring the height of the sun at noon",
                      "by comparing the time at home with noon on the ship",
                      "by using a pendulum clock kept on board",
                      "by counting the days since leaving port"],
             "no": {"by comparing the time at home with noon on the ship": "That is the method for finding longitude, how far east or west a ship is, and it needed a clock nobody had yet built."},
             "why": "The first paragraph says he could find his latitude “by measuring the height of the sun at noon”. Longitude was the hard part."},
            {"id": "1e8ce67c85b6", "t": "mcq", "d": "infer", "q": "Why did Harrison choose a naturally oily wood for some parts of his clocks?",
             "opts": ["So that no oil was needed, because oil that thickened in the cold made clocks go wrong",
                      "Because it was cheaper and easier to find in Lincolnshire than brass",
                      "So that the clock would float if it fell from a ship into the sea",
                      "Because his father had told him that oily wood was the best for carpentry"],
             "why": "The third paragraph says the wood “needed no oil at all”, at a time when oil that thickened in the cold “was one of the main reasons clocks went wrong”."},
            {"id": "f94e3cda83eb", "t": "tap", "d": "infer", "q": "Tap the word that shows Harrison wanted to do even better after his first sea clock worked well.",
             "s": "Harrison, however, was not [satisfied].",
             "why": "H1 “performed well”, but Harrison was “not satisfied”: he spent more than twenty years improving on it."},
            {"id": "b1ea33ca2922", "t": "mcq", "d": "compare", "q": "How was H4 different from H1, according to the text?",
             "opts": ["H1 was a large, heavy machine; H4 was about the size of a big pocket watch",
                      "H1 was made of wood; H4 was the first of his clocks made of brass",
                      "H1 failed its trial at sea; H4 was the first to pass a trial",
                      "H1 was tested on a voyage to Jamaica; H4 on a voyage to Lisbon"],
             "no": {"H1 failed its trial at sea; H4 was the first to pass a trial": "The text says that on its trial voyage to Lisbon, H1 “performed well”."},
             "why": "The fourth paragraph calls H1 “a large, heavy machine of brass” and says H4 “looked like an oversized pocket watch, about thirteen centimetres across”."},
            {"id": "57ccd5a4a98a", "t": "mcq", "d": "retrieve", "q": "According to the text, why would the Board of Longitude not pay Harrison in full after the trials?",
             "opts": ["Some members suspected luck, and others preferred a method using the Moon and stars",
                      "H4 was several minutes out when it reached Jamaica after two months at sea",
                      "Harrison had sent his son on the voyage instead of sailing himself",
                      "King George III had ordered the Board to keep the prize money"],
             "no": {"King George III had ordered the Board to keep the prize money": "The King did the opposite: he “took his side”, and Parliament then granted Harrison money."},
             "why": "The fifth paragraph says: “Some of its members suspected luck; others preferred a rival method that used the positions of the Moon and stars.”"},
            {"id": "6cde34c99bb3", "t": "order", "d": "sequence", "q": "Put these in the order they happened, according to the text.",
             "items": ["Parliament offers a prize for solving the problem", "Harrison finishes his first sea clock",
                       "William sails with H4 to Jamaica", "Parliament grants Harrison a large sum of money",
                       "Harrison dies"],
             "why": "The prize was offered in 1714, H1 was finished in 1735, the voyage to Jamaica was in 1761, the money was granted in 1773, and Harrison died three years later."},
            {"id": "8a6287c3013b", "t": "mcq", "d": "summarise", "q": "Which best describes how the writer presents Harrison?",
             "opts": ["As a self-taught craftsman who kept going until he solved a problem experts thought impossible",
                      "As a famous scientist who won the longitude prize quickly and easily",
                      "As a stubborn man whose clocks never worked well once they were at sea",
                      "As an explorer who sailed round the world with Captain James Cook"],
             "no": {"As a famous scientist who won the longitude prize quickly and easily": "He was a carpenter who taught himself, he worked for decades, and he “was never officially awarded the prize”."},
             "why": "The writer stresses that he trained as a carpenter, “taught himself clockmaking”, and worked for decades; the last sentence calls him “the carpenter whom the experts doubted”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.18
    {
        "key": "RD8.18",
        "year": 8,
        "strand": "Persuasive writing",
        "title": "In Praise of Boredom",
        "nc": "Know how language, including figurative language, vocabulary choice and rhetoric, presents meaning",
        "text": "When did you last do absolutely nothing? I do not mean scrolling, or watching, or listening to something with one ear while you message a friend. I mean nothing: sitting on a wall, or lying on your bed, staring at a crack in the ceiling while the minutes crawl past.\n\n"
                "If you are like most people, the honest answer is probably “I can't remember.” Every gap in our day, the bus stop, the queue in the canteen, the five minutes before a lesson begins, is filled before it has a chance to open. And we think this is a good thing. Boredom, we are told, is the enemy: something to be cured as quickly as possible.\n\n"
                "I want to argue the opposite. Boredom is not a problem to be solved. It is a door, and we keep slamming it shut.\n\n"
                "Two summers ago, I spent three weeks at my grandmother's house in a village in the hills of northern Portugal. There was no internet signal, the television showed one channel, and my grandmother went to bed at nine. For the first four days I was so bored I could have screamed. I followed her round the kitchen. I counted the tiles on the floor. I complained, loudly and often.\n\n"
                "On the fifth day, something changed. With nothing else to do, I took an old notebook down to the stream at the bottom of the village and began, for no reason at all, to draw the stones. The next day I drew the lizards that sunbathed on the wall. By the end of the holiday I had filled the notebook, and I had found something I still love doing. Nobody suggested it. Nothing beeped to remind me. It grew, slowly, out of the empty time.\n\n"
                "That is the point. When the mind has nothing to hold on to, it begins to wander, and a wandering mind is where ideas are born. Plenty of people say that their best thoughts arrive on a long walk or in the shower, exactly the moments when nothing is demanding their attention. If every empty minute is filled with things other people have made, when do our own ideas get their turn?\n\n"
                "Some will say that this is easy to write and hard to live. They are right. A phone is made to be picked up, putting it down takes effort, and nobody enjoys feeling restless. I am not suggesting that anyone throws their phone into a river. I am suggesting something much smaller: that now and then, when a gap opens in your day, you leave it open.\n\n"
                "Wait at the bus stop with nothing in your hands. Look out of the window on the way home. Lie on your bed and stare at the ceiling. It will feel uncomfortable at first. It is supposed to. Boredom is the itch that comes before an idea.\n\n"
                "So the next time you hear yourself say “I'm bored”, do not reach for a screen. Wait. Something may be about to begin.",
        "qs": [
            {"id": "a6a9887b242b", "t": "mcq", "d": "structure", "q": "Why does the writer open the article with a question?",
             "opts": ["To make readers think about their own habits before the argument begins",
                      "To collect answers about how readers spend their free time",
                      "To show that the writer does not know the answer either",
                      "To suggest that doing nothing is impossible for anyone"],
             "why": "“When did you last do absolutely nothing?” makes each reader check their own day, so they are already involved when the argument starts."},
            {"id": "6ce8a9ad25cc", "t": "mcq", "d": "infer", "q": "“Every gap in our day … is filled before it has a chance to open.” What is the writer suggesting?",
             "opts": ["We fill spare moments so fast that we never experience them as empty",
                      "School timetables now have too many lessons and too few breaks",
                      "Bus stops and canteens are more crowded than they used to be",
                      "People are always late, so they never have any spare time"],
             "why": "The “gaps” are the spare minutes at the bus stop or in the queue; the writer means we reach for something to do before we ever feel that time as empty."},
            {"id": "1fe9cd6fa83b", "t": "mcq", "d": "language", "q": "“It is a door, and we keep slamming it shut.” What does this metaphor suggest about boredom?",
             "opts": ["It could lead us somewhere new, but we refuse to let it",
                      "It traps us inside, like a locked room with no way out",
                      "It is something we must keep out of our lives",
                      "It makes people angry enough to slam doors"],
             "why": "A door leads somewhere. By filling every gap, we shut that door before boredom can lead us to anything, such as a new idea.",
             "no": {"It is something we must keep out of our lives": "That is the view the writer argues against (“Boredom, we are told, is the enemy”)."}},
            {"id": "0efae26385be", "t": "tap", "d": "retrieve", "q": "Tap the word that names what the writer drew on the day after drawing the stones.",
             "s": "The next day I drew the [lizards] that sunbathed on the wall.",
             "why": "The writer drew the stones first, and the next day drew the lizards on the wall."},
            {"id": "704a89a9eeb3", "t": "mcq", "d": "infer", "q": "Why does the writer include the short sentences “Nobody suggested it. Nothing beeped to remind me.”?",
             "opts": ["To stress that the new interest came from the writer alone",
                      "To complain that the grandmother ignored the writer all summer",
                      "To show that the writer's phone had been broken on the journey",
                      "To prove that drawing is better for everyone than using a screen"],
             "why": "No person and no device prompted the drawing: the point is that the idea grew by itself out of empty time, which is the writer's whole argument."},
            {"id": "d574ae5ed094", "t": "mcq", "d": "structure", "q": "What is the purpose of the paragraph that begins “Some will say”?",
             "opts": ["It admits a fair objection, then makes the writer's request smaller so it seems reasonable",
                      "It changes the argument to say that phones should be banned for young people",
                      "It gives scientific evidence about how phones are designed to be addictive",
                      "It tells a second story about the holiday in Portugal to support the argument"],
             "why": "The writer agrees that putting a phone down is hard, then says the suggestion is “much smaller”: just leaving the odd gap open. Answering an objection makes the argument harder to dismiss.",
             "no": {"It changes the argument to say that phones should be banned for young people": "The writer says the opposite: “I am not suggesting that anyone throws their phone into a river.”"}},
            {"id": "89f1085bd3fa", "t": "mcq", "d": "summarise", "q": "Which statement best sums up the writer's viewpoint?",
             "opts": ["Boredom is uncomfortable but valuable, because it gives our own ideas room to grow",
                      "Young people should give up their phones and spend every summer offline",
                      "Boredom is harmful, so we should always find something to fill a gap",
                      "Drawing is the best cure for boredom, and everyone should try it"],
             "why": "The writer admits boredom feels uncomfortable (“It is supposed to”) but argues it is “the itch that comes before an idea”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.19
    {
        "key": "RD8.19",
        "year": 8,
        "strand": "Letters and diaries",
        "title": "A Week on Fair Isle",
        "nc": "Read a wide range of writing: diaries; how a writer's viewpoint and feelings develop",
        "text": "Monday\n\n"
                "Arrived. The plane had eight seats and every one of them rattled. Aunt Priti met me on the airstrip in a waterproof so huge it looked as if it were wearing her. “Ishaan! You made it!” she shouted over the wind. Fair Isle is about five kilometres long and lies on its own in the sea between Orkney and Shetland. There are no shops like ours, no cinema, and the wind never stops, not even for a second. I have been here four hours and I have already counted the days until I go home. There are six.\n\n"
                "Wednesday\n\n"
                "Today I helped with the ringing. Aunt Priti works at the bird observatory, and each morning she checks the nets and traps for small birds that have landed on the island overnight. Every bird is weighed, measured and given a tiny metal ring on its leg with its own number, and then it is let go. If anyone, anywhere, finds that bird again, the number tells them where it has been. One warbler that Aunt Priti ringed here was found a few weeks later in Portugal.\n\n"
                "She showed me how to hold a bird with its head between my first two fingers, firmly but gently. I held a robin. It weighed about the same as a pound coin and a few sweets, and its heart was going so fast I could feel it in my fingertips. When I opened my hand it sat there for a second, as if it had not noticed it was free, and then it was gone.\n\n"
                "Less good: on the cliffs this afternoon a fulmar chick spat a stream of orange oil at me. Aunt Priti says that is how they defend themselves. She also says the smell will come out of my coat eventually. I was sceptical, and I still am.\n\n"
                "Friday\n\n"
                "The plane could not come because of the wind. I was furious for about an hour. Then the radio in the kitchen crackled, someone shouted a name I had never heard, and suddenly everyone in the observatory was pulling on boots. A bird that normally lives thousands of kilometres away had been blown here by the storm, and it was sitting on a wall above the harbour.\n\n"
                "We stood in a line in the rain, nine adults and me, not speaking. It was small and brown and not very exciting, if I am honest. But I looked at their faces, and I understood that the exciting thing was not really the bird. It was that it had come all that way, across all that sea, and of all the places it could have landed, it had found us.\n\n"
                "The plane might come tomorrow. I have stopped counting the days. I have started counting the birds.",
        "qs": [
            {"id": "297b4e237134", "t": "mcq", "d": "infer", "q": "What does the Monday entry suggest about how Ishaan feels when he arrives?",
             "opts": ["He is unhappy and already wishes he could go home",
                      "He is excited to start work at the bird observatory",
                      "He is frightened that the plane will crash on the way back",
                      "He is angry with Aunt Priti for meeting him so late"],
             "why": "He has “already counted the days” until he goes home after only four hours, and he lists everything the island does not have."},
            {"id": "24ee334850d8", "t": "mcq", "d": "retrieve", "q": "According to the diary, what does the number on a bird's ring tell anyone who finds it again?",
             "opts": ["where the bird has been", "how old the bird is now",
                      "what the bird likes to eat", "how much the bird weighs"],
             "no": {"how much the bird weighs": "The bird is weighed when it is ringed, but the diary says the number “tells them where it has been”."},
             "why": "The Wednesday entry says: “If anyone, anywhere, finds that bird again, the number tells them where it has been.”"},
            {"id": "a920481c7b40", "t": "mcq", "d": "language", "q": "When Ishaan lets the robin go, “it sat there for a second, as if it had not noticed it was free”. What does this detail add?",
             "opts": ["It captures a small, surprising moment that clearly stayed with him",
                      "It shows that the robin was hurt and could not fly away at all",
                      "It explains how ringers check that a bird is healthy before release",
                      "It shows that Ishaan had held the robin too tightly in his hand"],
             "no": {"It shows that the robin was hurt and could not fly away at all": "The robin is not hurt: “and then it was gone”."},
             "why": "The pause before the robin flies is a tiny, vivid detail; recording it shows how much the moment of holding a wild bird meant to him."},
            {"id": "cde36e9a4ef4", "t": "text", "d": "retrieve", "q": "Find and copy the name of the bird that spat oil at Ishaan.",
             "a": ["fulmar", "a fulmar", "the fulmar", "fulmar chick", "a fulmar chick", "the fulmar chick", "fulmars"],
             "why": "The Wednesday entry says “a fulmar chick spat a stream of orange oil at me”."},
            {"id": "78f6ad633021", "t": "mcq", "d": "vocab", "q": "Aunt Priti says the smell will come out of his coat. Ishaan writes, “I was sceptical, and I still am.” What does sceptical mean?",
             "opts": ["doubtful that something is true", "sure that something will happen",
                      "upset about something unfair", "pleased with a piece of good news"],
             "why": "Being sceptical means doubting a claim. Ishaan does not believe the smell will really come out."},
            {"id": "bc3df68215de", "t": "tap", "d": "retrieve", "q": "Tap the word that shows how Ishaan first felt when the plane could not come.",
             "s": "I was [furious] for about an hour.",
             "why": "He was “furious”, very angry, at first; then the news of the rare bird changed his mood."},
            {"id": "35f84d84d618", "t": "mcq", "d": "compare", "q": "How do Ishaan's last two sentences show a change since Monday?",
             "opts": ["On Monday he counted days until leaving; now he cares about the island's birds",
                      "On Monday he loved the birds; now he only wants the plane to come",
                      "On Monday he was busy at the observatory; now he has nothing to do",
                      "On Monday he could count well; now he keeps losing count of things"],
             "why": "On Monday he “counted the days until I go home”; now he has “stopped counting the days” and “started counting the birds”: the island has won him over."},
        ],
    },
    # ------------------------------------------------------------------ RD8.20
    {
        "key": "RD8.20",
        "year": 8,
        "strand": "News reports",
        "title": "Pupils Find Otters Back on the River Lenn",
        "nc": "Read a wide range of non-fiction: news reports; distinguish fact from opinion and weigh viewpoints",
        "text": "Otters have returned to the River Lenn in Kettleford for the first time in more than fifty years, after a team of Year 8 pupils spotted the signs on a school river survey.\n\n"
                "The pupils, from the science club at Kettleford Academy, were checking the river last month when they found webbed footprints in the mud beneath the old railway bridge. Close by, on a flat stone at the water's edge, they found a small pile of droppings. Otter droppings, known as spraint, have a sweet smell that some people compare to jasmine tea, and they often contain tiny fish bones.\n\n"
                "“At first we thought it was a dog,” said Amara Osei, 13. “But Mr Rahman got down and sniffed it, which was disgusting, and then he went completely quiet.”\n\n"
                "The club set up a motion-sensitive camera on the bank. Four nights later it recorded a female otter and two cubs swimming upstream just after midnight.\n\n"
                "Dr Helen Pryce, an ecologist with the county wildlife trust, said the discovery was “wonderful news”. “Otters are at the top of the river food chain,” she explained. “They can only survive where there are plenty of fish, and fish need clean water. When otters come back, it tells us that the whole river is recovering.”\n\n"
                "Otters disappeared from many English rivers between the 1950s and the 1970s. Harmful farm chemicals washed into the water, built up in the fish and then in the otters that ate them. Since those chemicals were banned, otters have gradually spread back along rivers across the country. The Lenn itself was badly polluted by factories upstream until the 1980s, and volunteers have spent years clearing rubbish and planting trees along its banks.\n\n"
                "Not everyone is celebrating without reservation. Gareth Lloyd, secretary of Kettleford Angling Club, said his members were pleased that the river was healthier but worried about the fish. “An otter can eat a lot in a night,” he said. “We have spent a great deal of money putting fish back into this river, and we would like some of them to stay there.”\n\n"
                "Dr Pryce said she understood the concern. “Otters do eat mainly fish,” she said, “but a healthy river can support both. We are happy to work with the anglers and keep an eye on fish numbers.”\n\n"
                "For the pupils, the hardest part is keeping the exact spot a secret, to stop the family from being disturbed. The club has now been asked to share its survey method with other schools along the river.\n\n"
                "“It's the best thing I've ever found,” said Amara. “Even if Mr Rahman did have to sniff it.”",
        "qs": [
            {"id": "a133dcf25fc8", "t": "mcq", "d": "structure", "q": "What is the main job of the first paragraph of the report?",
             "opts": ["To sum up who found what, and where, in one sentence",
                      "To describe exactly how the pupils set up the camera",
                      "To give the anglers' view before anyone else's",
                      "To explain why otters left English rivers"],
             "why": "Like most news reports, it opens with the key facts: otters are back on the River Lenn, found by Year 8 pupils on a river survey. The details come later."},
            {"id": "770194c3974a", "t": "text", "d": "retrieve", "q": "Find and copy the word used for otter droppings.",
             "a": ["spraint", "the spraint", "spraints"],
             "why": "The second paragraph says: “Otter droppings, known as spraint”."},
            {"id": "dff5c45403b9", "t": "mcq", "d": "retrieve", "q": "What did the camera record?",
             "opts": ["a female otter and two cubs swimming upstream", "a dog digging beneath the old railway bridge",
                      "two adult otters catching fish at midnight", "an otter leaving footprints on a flat stone"],
             "no": {"a dog digging beneath the old railway bridge": "The pupils first thought the footprints were a dog's, but the camera recorded otters."},
             "why": "The fourth paragraph says it “recorded a female otter and two cubs swimming upstream just after midnight”."},
            {"id": "7ce6d160fb94", "t": "mcq", "d": "infer", "q": "Why did Mr Rahman most likely go “completely quiet” after sniffing the droppings?",
             "opts": ["He realised from the smell that they were not a dog's, but an otter's",
                      "He was too disgusted by the smell to say anything to the pupils",
                      "He was angry that the pupils had touched something so dirty",
                      "He was listening for a dog that might be close by on the bank"],
             "no": {"He was too disgusted by the smell to say anything to the pupils": "It was Amara who found the sniffing disgusting. Spraint has a sweet smell, which is how he could tell it was not a dog's."},
             "why": "The report says spraint has a sweet smell, unlike a dog's. Sniffing it told him it was an otter's, and the discovery left him lost for words."},
            {"id": "9c719ef98450", "t": "mcq", "d": "vocab", "q": "“Not everyone is celebrating without reservation.” What does without reservation mean here?",
             "opts": ["completely, with no doubts at all", "without booking a place in advance",
                      "without permission from the school", "quietly, without telling anyone"],
             "no": {"without booking a place in advance": "A reservation can be a booking, but here it means a doubt: some people are not completely happy."},
             "why": "A reservation here is a doubt. The next paragraph shows the anglers' doubt: they are pleased, but worried about the fish."},
            {"id": "059e4965f868", "t": "mcq", "d": "compare", "q": "How does Gareth Lloyd's view of the otters differ from Dr Pryce's?",
             "opts": ["He worries they will eat too many fish; she thinks the river can support both",
                      "He wants the otters removed; she wants the anglers to leave the river",
                      "He thinks the river is still polluted; she thinks it is completely clean",
                      "He doubts the pupils saw otters; she is sure the camera showed them"],
             "no": {"He wants the otters removed; she wants the anglers to leave the river": "Neither says this. He is pleased the river is healthier, and she offers to work with the anglers."},
             "why": "Mr Lloyd says “An otter can eat a lot in a night”; Dr Pryce replies that “a healthy river can support both” and offers to watch fish numbers."},
            {"id": "a96b154a1145", "t": "mcq", "d": "summarise", "q": "Which would be the best alternative headline for this report?",
             "opts": ["School survey reveals river's return to health", "Anglers demand action over hungry otters",
                      "Teacher sniffs mystery droppings by bridge", "Farm chemicals banned after otters vanish"],
             "no": {"Anglers demand action over hungry otters": "The anglers are only one part of the report, and they do not demand action: they are “pleased that the river was healthier”."},
             "why": "The report is mainly about the pupils' discovery and what it shows: otters are back because the river is recovering."},
        ],
    },
    # ------------------------------------------------------------------ RD8.21
    {
        "key": "RD8.21",
        "year": 8,
        "strand": "Play scripts",
        "title": "The Group Project",
        "nc": "Read critically: study plot, characterisation and dialogue in drama, and the effects of these",
        "text": "(A geography classroom after school on a Thursday. Rain against the windows. AISHA sits at a table covered in printouts, glue sticks and a half-finished poster about volcanoes. CALLUM is balancing a ruler on one finger. JUN comes in with his coat already on.)\n"
                "AISHA: Oh, look who it is. You do know the presentation is on Monday?\n"
                "JUN: I know. I can only stay ten minutes.\n"
                "AISHA: Ten minutes. Of course. That's ten more than last week.\n"
                "CALLUM: (still balancing the ruler) Look, the important thing is that we're all here now, and the poster is, er, nearly a poster.\n"
                "AISHA: Callum, please don't. (She slams the folder on the desk.) Jun, we've had three meetings. You've missed every one. I've done the poster, Callum's done the slides, and you've done... what, exactly?\n"
                "JUN: Some of it.\n"
                "AISHA: Some of what? We're all getting the same mark, you know. If this goes badly, it goes badly for all three of us.\n"
                "CALLUM: (quietly) Aisha.\n"
                "AISHA: What? Someone has to say it.\n"
                "(Pause. JUN looks at the clock above the door. Then, reluctantly, he takes a battered notebook out of his bag and puts it on the table.)\n"
                "JUN: I've done the bit on why they erupt. And the three case studies. I did them at night.\n"
                "(CALLUM picks up the notebook and turns the pages slowly.)\n"
                "CALLUM: Jun, this is... There are diagrams. You've labelled the magma chamber. In colour.\n"
                "AISHA: (taking it from him) Why didn't you bring this to the meetings?\n"
                "JUN: Because the meetings are at half past three, and my sister comes out of primary at a quarter to four. Mum works late at the hospital on weekdays now. There's nobody else to get her.\n"
                "(Silence. AISHA puts the notebook down very carefully, as if it might break.)\n"
                "AISHA: You could have told us.\n"
                "JUN: I didn't want it to be a whole thing. People get weird about it.\n"
                "CALLUM: We wouldn't have got weird. (Beat.) Well. Aisha might have organised a rota.\n"
                "AISHA: (almost smiling) I would have organised a very good rota. (She pauses.) I'm sorry, Jun. I thought you just didn't care.\n"
                "JUN: It's fine. I'd have thought the same.\n"
                "AISHA: Could we meet at lunchtime instead? Tomorrow, and Monday morning before registration?\n"
                "JUN: Lunchtime's good. (He looks at the clock again and stands.) I have to go.\n"
                "AISHA: Jun. Next time, tell us.\n"
                "JUN: (at the door, turning back) Next time, ask.\n"
                "(He goes. AISHA and CALLUM look at the notebook, then at each other.)\n"
                "CALLUM: So. Shall I take the volcano bit off my slides, then?\n"
                "AISHA: Callum. Every single one.",
        "qs": [
            {"id": "ffcda585be67", "t": "mcq", "d": "retrieve", "q": "Why is Aisha angry with Jun at the start of the scene?",
             "opts": ["He has missed all three of the group's meetings", "He has spoiled the poster she made about volcanoes",
                      "He has told the teacher that she is too bossy", "He has lost the slides that Callum made for them"],
             "why": "Aisha says: “Jun, we've had three meetings. You've missed every one.”"},
            {"id": "b325cb7c0ff0", "t": "mcq", "d": "infer", "q": "What do Callum's first words and actions suggest about him?",
             "opts": ["He wants to keep things light and avoid an argument", "He is furious with Jun and wants him out of the group",
                      "He has not noticed that Jun has come into the room", "He is secretly pleased that Aisha is losing her temper"],
             "why": "He jokes that the poster is “nearly a poster” and says “the important thing is that we're all here now”, trying to calm things before Aisha's anger boils over."},
            {"id": "a3bb0a01f7aa", "t": "tap", "d": "language", "q": "Tap the word in this stage direction that shows how angry Aisha is.",
             "s": "(She [slams] the folder on the desk.)",
             "why": "To slam something is to put it down hard and loudly, which shows her frustration has boiled over."},
            {"id": "6611e25dc184", "t": "mcq", "d": "vocab", "q": "“Then, reluctantly, he takes a battered notebook out of his bag.” What does reluctantly mean?",
             "opts": ["without really wanting to", "very quickly and eagerly",
                      "in a proud, showing-off way", "by mistake, without meaning to"],
             "why": "Doing something reluctantly means doing it unwillingly. Jun did not want to explain himself, as he says later: “I didn't want it to be a whole thing.”"},
            {"id": "63b1b624b263", "t": "mcq", "d": "infer", "q": "Why does Aisha put the notebook down “very carefully, as if it might break”?",
             "opts": ["She now sees how much effort it stands for and feels ashamed",
                      "The notebook is old and its pages are falling out",
                      "She is worried that Callum will try to take it from her",
                      "She wants to copy Jun's diagrams onto the poster neatly"],
             "why": "The stage direction comes straight after Jun explains about his sister. Handling the notebook gently shows her new respect, and her apology soon follows."},
            {"id": "cb97aaa33187", "t": "mcq", "d": "compare", "q": "How does Aisha's view of Jun change during the scene?",
             "opts": ["She first thinks he does not care, then realises he has worked hard in difficult circumstances",
                      "She first admires his diagrams, then decides he should leave the group altogether",
                      "She first feels sorry for him, then becomes angry when she sees his notebook",
                      "She first ignores him completely, then asks him to do all of the presentation"],
             "why": "She tells him, “I thought you just didn't care”: she had judged him before she knew about his sister, and she apologises."},
            {"id": "a245587bde6c", "t": "mcq", "d": "structure", "q": "Aisha says, “Next time, tell us.” Jun replies, “Next time, ask.” What is the effect of this exchange near the end?",
             "opts": ["The echo shows each of them has a lesson: speak up, and do not assume",
                      "It shows that Jun is still angry and will not come to any more meetings",
                      "It shows that Aisha has not forgiven Jun for missing the meetings",
                      "It repeats the plan to meet at lunchtime so that the audience remembers it"],
             "why": "The two lines match in shape but point in opposite directions: Jun should have explained, and Aisha should have asked before she judged."},
        ],
    },
    # ------------------------------------------------------------------ RD8.22
    {
        "key": "RD8.22",
        "year": 8,
        "strand": "Stories",
        "title": "Mateo's Cord",
        "nc": "Read critically: study setting, plot and characterisation, and the effects of these",
        "text": "Every June, when the dry season had turned the grass on the hillsides to the colour of straw, the four villages above the river rebuilt their bridge.\n\n"
                "Mateo had crossed the old one a hundred times. It hung across the gorge like a hammock, swaying with every step, and the river roared so far below that he had learned not to look at it. By June the old bridge was grey and sagging. Its ropes had stiffened in the sun and softened in the rain, and his grandfather said that a bridge, like a person, could only carry so much for so long.\n\n"
                "This year, for the first time, Mateo was old enough to make a cord.\n\n"
                "His grandmother showed him how. She took a bundle of the long, tough grass, wetted it, and rolled it against her thigh with the flat of her hand, twisting as she went, feeding in new stems before the old ones ran out. A cord grew out of her hands as if it had always been there, smooth and even, as thick as his little finger.\n\n"
                "Mateo's cord was not like that. It was thick in some places and thin in others, and twice it came apart altogether. By the evening his palm was raw and his cord was ten arm-lengths of lumps. When the family laid out their cords to be counted, he pushed his underneath his grandmother's, where it could not be seen.\n\n"
                "She noticed. She pulled it out, wrapped one end round her wrist, gave the other to him, and leaned back with all her weight. Mateo braced his feet. The cord creaked, and stretched a little, and held.\n\n"
                "“Ugly,” she said. “But strong.” And she laid it on top.\n\n"
                "The next morning the cords from all four villages were gathered on the slope. Hundreds of them were plaited together into thicker ropes, and the thicker ropes were plaited again, until each of the great main ropes was as thick as a man's leg. Then, with dozens of people pulling at once, the main ropes were carried across and fastened to the stone ends of the bridge on either side of the gorge. Only when the new bridge was in place was the old one cut free. It fell slowly, folding in on itself, and the river took it away.\n\n"
                "On the third day the bridge was finished, and Mateo walked across it behind his grandmother. It swayed exactly as the old one had. He looked down at the ropes beneath his hands and tried to find his own cord, the lumpy one, the one that had come apart twice.\n\n"
                "He could not. It was in there somewhere, plaited in with a thousand others, holding.\n\n"
                "Halfway across, for the first time in his life, he looked down at the river.",
        "qs": [
            {"id": "71fe4c705eec", "t": "mcq", "d": "language", "q": "The old bridge “hung across the gorge like a hammock”. What does this simile suggest about the bridge?",
             "opts": ["It dips in the middle and swings as people cross",
                      "It is comfortable enough to lie down and rest on",
                      "It is woven so tightly that nothing can fall through",
                      "It is folded away and stored when it is not in use"],
             "why": "A hammock hangs low in the middle and swings: the next words, “swaying with every step”, confirm the picture."},
            {"id": "f39b281307a6", "t": "mcq", "d": "vocab", "q": "What is a gorge, as the word is used in this story?",
             "opts": ["a deep, narrow valley with steep sides", "a fast stream that runs between two villages",
                      "a wide, flat field of long dry grass", "a stone tower at each end of a bridge"],
             "why": "The river roars “so far below” the bridge: a gorge is a deep, narrow valley that a river has cut between steep sides."},
            {"id": "86d295aec94c", "t": "mcq", "d": "infer", "q": "Why does Mateo push his cord underneath his grandmother's?",
             "opts": ["He is ashamed that it is lumpy and uneven", "He wants to keep it as a souvenir of the day",
                      "He thinks it will dry out faster underneath", "He has been told that new cords go at the bottom"],
             "why": "His cord is “ten arm-lengths of lumps” beside her smooth one, and he hides it “where it could not be seen”."},
            {"id": "81feb0d3f05c", "t": "tap", "d": "infer", "q": "Tap the word in the grandmother's speech that shows what she cares about most in a cord.",
             "s": "“Ugly,” she said. “But [strong].”",
             "why": "She admits the cord is ugly, but “strong” is what matters for a bridge, and she has just tested it with all her weight."},
            {"id": "d217cdd5399f", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Mateo's grandmother tests his cord", "The cords are plaited into thicker ropes",
                       "The main ropes are fastened on either side of the gorge", "The old bridge is cut free and falls",
                       "Mateo walks across the new bridge"],
             "why": "The testing is the evening before; the next morning the cords are plaited and the main ropes fixed; only then is the old bridge cut free; on the third day Mateo crosses."},
            {"id": "354b05ff6a8c", "t": "mcq", "d": "infer", "q": "At the end, Mateo looks down at the river “for the first time in his life”. What does this suggest?",
             "opts": ["He now feels safe, trusting a bridge he helped to build",
                      "He has dropped something and wants to see where it fell",
                      "He is trying to see where the old bridge has gone",
                      "He has become dizzy and is about to lose his balance"],
             "no": {"He is trying to see where the old bridge has gone": "The old bridge was carried away days earlier. The point is that he has always been too afraid to look down before."},
             "why": "He had “learned not to look” at the river. Knowing his own strong cord is in the bridge, he is no longer afraid."},
            {"id": "400b822e4e85", "t": "mcq", "d": "summarise", "q": "Which best sums up the main idea of the story?",
             "opts": ["Many small efforts, even imperfect ones, together make something strong",
                      "Young people should leave hard work to those with more experience",
                      "Old things should be thrown away as soon as new ones are made",
                      "A bridge must look perfect before anyone is allowed to cross it"],
             "why": "Mateo's lumpy cord cannot be found among a thousand others, but it is “in there somewhere ... holding”: everyone's work together carries the bridge."},
        ],
    },
    # ------------------------------------------------------------------ RD8.23
    {
        "key": "RD8.23",
        "year": 8,
        "strand": "Information",
        "title": "Measuring Britain",
        "nc": "Understand increasingly challenging texts: follow the development of ideas and refer to evidence in the text",
        "text": "After an uprising in 1745, the British army discovered that it had almost no reliable maps of the Scottish Highlands. Roads, rivers and even mountains were missing or drawn in the wrong place. A young Scot called William Roy was given the job of helping to survey the Highlands, and for several years his teams walked, measured and drew the land. The finished map was handsome, but Roy knew that it was not truly accurate. He spent much of the rest of his life arguing that Britain needed something better: a map built on careful measurement from the very first line.\n\n"
                "The method he wanted was triangulation. It rests on a simple fact of geometry: if you know the length of one side of a triangle and the sizes of the two angles at its ends, you can calculate the lengths of the other two sides without ever walking along them. A surveyor stands at each end of a measured line in turn and uses an instrument called a theodolite to measure the angle to a distant point, such as a hilltop. Each side that has been calculated can then become the base of a new triangle, and so a chain of triangles can be stretched across a whole country.\n\n"
                "Everything depends on the first line, the baseline. In 1784 Roy measured one across Hounslow Heath, west of London, on flat open ground close to where Heathrow Airport stands today. It was about eight kilometres long, and measuring it took most of a summer. His team began with long wooden rods laid end to end, but found that the wood grew and shrank with the damp. They replaced the rods with glass tubes, which did not, and checked every length again and again. It was painstaking work, and it had to be: any error in the baseline would be copied into every triangle built on it.\n\n"
                "Roy died in 1790. A year later the Board of Ordnance, which supplied the army, began the national survey he had argued for, and the organisation that grew from it is still called the Ordnance Survey. Its first map, of the county of Kent, was published in 1801.\n\n"
                "Over the following decades, surveyors hauled their instruments up hill after hill in all weathers, sometimes waiting days for the cloud to lift so that they could see the next point. In the 1930s a new and even more accurate survey began, and thousands of concrete pillars, known as trig points, were built on hilltops to hold the instruments perfectly steady.\n\n"
                "Today satellites can fix a position in seconds, and the trig points are no longer needed for map-making. Most of them still stand, though, and walkers who reach a summit often walk over and touch one, perhaps without knowing that it marks a corner of a triangle in a pattern that once covered the whole of Britain.",
        "qs": [
            {"id": "7942ebf91e33", "t": "mcq", "d": "retrieve", "q": "According to the text, what was wrong with the early maps of the Scottish Highlands?",
             "opts": ["Roads, rivers and mountains were missing or in the wrong place",
                      "They showed only the roads and none of the mountains",
                      "They were drawn so small that the army could not read them",
                      "They had been made from satellite pictures that were blurred"],
             "why": "The first paragraph says “Roads, rivers and even mountains were missing or drawn in the wrong place.”"},
            {"id": "3c2669053db9", "t": "mcq", "d": "retrieve", "q": "According to the text, what does a surveyor need to know to calculate the other two sides of a triangle?",
             "opts": ["the length of one side and the two angles at its ends",
                      "the length of one side and nothing more",
                      "the height of the hill at each corner of the triangle",
                      "the three angles of the triangle and nothing else"],
             "why": "The second paragraph says you need “the length of one side of a triangle and the sizes of the two angles at its ends”."},
            {"id": "5010eadebc51", "t": "tap", "d": "retrieve", "q": "Tap the word that names the instrument used to measure angles.",
             "s": "A surveyor stands at each end of a measured line in turn and uses an instrument called a [theodolite] to measure the angle to a distant point, such as a hilltop.",
             "why": "The surveyor “uses an instrument called a theodolite to measure the angle”."},
            {"id": "ff3b1d179ce1", "t": "mcq", "d": "retrieve", "q": "Why did Roy's team replace the wooden rods with glass tubes?",
             "opts": ["Glass kept the same length in damp weather, unlike wood",
                      "Glass tubes were cheaper and lighter to carry across the heath",
                      "Wooden rods snapped when they were laid end to end",
                      "Glass let the team see through the tubes to the next hill"],
             "why": "The wood “grew and shrank with the damp”, so the same rod gave different lengths; the glass tubes “did not”, which mattered because any error would spread through every triangle."},
            {"id": "de8d20735f64", "t": "mcq", "d": "vocab", "q": "“It was painstaking work.” What does painstaking mean here?",
             "opts": ["done with great care and attention to detail", "so tiring that it caused the workers pain",
                      "done quickly to finish before the winter", "dangerous, because of the risk of injury"],
             "no": {"so tiring that it caused the workers pain": "The word contains “pain”, but painstaking means taking great care, like checking “every length again and again”."},
             "why": "Painstaking means very careful and thorough: the team “checked every length again and again”."},
            {"id": "6a5bd4922eca", "t": "order", "d": "sequence", "q": "Put these in the order they happened, according to the text.",
             "items": ["Roy helps to survey the Scottish Highlands", "Roy measures a baseline on Hounslow Heath",
                       "The Board of Ordnance begins the national survey", "The first map, of Kent, is published",
                       "Concrete trig points are built on hilltops"],
             "why": "The Highlands survey followed 1745; the baseline was 1784; the national survey began in 1791; the Kent map came out in 1801; trig points were built from the 1930s."},
            {"id": "e79eb323fa81", "t": "mcq", "d": "structure", "q": "Why does the writer end with walkers touching a trig point on a summit?",
             "opts": ["To link a familiar sight today to the history the text has explained",
                      "To warn walkers that trig points are dangerous and should be avoided",
                      "To suggest that trig points are still the best way to make maps",
                      "To introduce a new topic about walking routes in the mountains"],
             "no": {"To suggest that trig points are still the best way to make maps": "The last paragraph says the opposite: satellites have taken over, and trig points “are no longer needed for map-making”."},
             "why": "The ending brings the history up to date: an ordinary walker's habit turns out to connect with the great triangle pattern that “once covered the whole of Britain”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.24
    {
        "key": "RD8.24",
        "year": 8,
        "strand": "Stories",
        "title": "The Repair Café",
        "nc": "Read critically: study setting, plot and characterisation, and the effects of these",
        "text": "The repair café opened at ten on the first Saturday of every month, in the community centre behind the swimming baths. By five past ten there was already a queue: a woman with a lamp, a boy with a scooter that squeaked, a man holding a sewing machine as carefully as a sleeping baby.\n\n"
                "Hana had been helping her uncle Tariq at his table since September. Mostly she passed him screwdrivers and wrote labels. Today, for the first time, he slid a radio across the table towards her and said, “Your turn.”\n\n"
                "The radio belonged to Mr Jenkins, who was eighty-one and wore a tie. It was the size of a shoebox, with a cream plastic case and a dial that glowed orange, or used to. “It stopped in August,” he said. “The shop said it wasn't worth mending. They said I should buy a new one.” He looked at the radio, not at Hana. “I'd rather not.”\n\n"
                "Hana wanted to start unscrewing things at once. Uncle Tariq put his hand flat on the table. “First rule,” he said. “Don't guess. Ask questions.”\n\n"
                "So she asked. Did it make any sound at all? No. Did the dial light up? No. Did it run on batteries or from the wall? Batteries, always.\n\n"
                "“Then where would you look first?” said her uncle.\n\n"
                "Hana turned the radio over and opened the little door at the back. The batteries inside were old, and round the metal springs that touched them was a crust of something green and powdery, like mould on forgotten bread.\n\n"
                "“The batteries have leaked,” said Uncle Tariq, “and the springs are corroded. The electricity can't get through.”\n\n"
                "He did not take over. He handed her a cotton bud, a little dish of vinegar and an old toothbrush, and went to help the woman with the lamp. Hana scrubbed. It was slow, fiddly work, and twice she thought she had finished and found more green hiding underneath. Mr Jenkins sat opposite and did not hurry her. He told her about the cricket matches he had listened to on this radio, summer after summer, with the window open and the garden going gold in the evening.\n\n"
                "When the springs were bright silver again, she dried them, fitted four new batteries and turned the dial.\n\n"
                "Nothing. Her stomach dropped.\n\n"
                "Then came a crackle, a hiss, and a man's voice, very calm, reading out the weather. The dial glowed orange.\n\n"
                "Mr Jenkins said nothing for a moment. Then he took out a folded handkerchief, blew his nose, and said that it must be the dust.\n\n"
                "On the form, under “Repaired by”, Uncle Tariq let Hana write her own name. Under “Cost” there was nothing to write. The repair café never charged; there was only a jar for donations by the door.\n\n"
                "At half past twelve, as they were packing up, Mr Jenkins came back with a carrier bag. Inside was a small clock that no longer ticked.\n\n"
                "“My neighbour's,” he said. “I told her I knew someone.”\n\n"
                "Hana looked at her uncle. Uncle Tariq looked at the clock, and then at her. “First rule?” he said.\n\n"
                "“Don't guess,” said Hana, and pulled the clock towards her.",
        "qs": [
            {"id": "000a09a7b637", "t": "mcq", "d": "language", "q": "A man holds his sewing machine “as carefully as a sleeping baby”. What does this simile suggest?",
             "opts": ["He treasures the machine and is afraid of damaging it",
                      "He has brought his baby with him to the repair café",
                      "The sewing machine is very light and easy to carry",
                      "He is trying not to wake the people in the queue"],
             "why": "People hold a sleeping baby gently, because it is precious and they do not want to disturb it: the man treats his machine the same way."},
            {"id": "1705904884bb", "t": "mcq", "d": "retrieve", "q": "What had the shop told Mr Jenkins about his radio?",
             "opts": ["It was not worth mending, and he should buy a new one",
                      "Its batteries had leaked, and its springs needed cleaning",
                      "It could be mended, but only if he paid a great deal",
                      "It was too old for any shop to find the right parts"],
             "no": {"Its batteries had leaked, and its springs needed cleaning": "That is what Hana and her uncle found at the repair café, not what the shop said."},
             "why": "Mr Jenkins says: “The shop said it wasn't worth mending. They said I should buy a new one.”"},
            {"id": "d3fe74f37f2d", "t": "text", "d": "retrieve", "q": "Find and copy the two words of Uncle Tariq's first rule that tell Hana what not to do.",
             "a": ["Don't guess", "don't guess", "Don't guess.", "do not guess"],
             "why": "Uncle Tariq says: “First rule. Don't guess. Ask questions.”"},
            {"id": "70dc84a7462c", "t": "mcq", "d": "vocab", "q": "“The springs are corroded.” What does corroded mean here?",
             "opts": ["slowly damaged by a chemical, so the metal is eaten away",
                      "bent out of shape by being pressed too hard",
                      "painted green to show which way round the batteries go",
                      "pulled loose from the place where they were fixed"],
             "no": {"painted green to show which way round the batteries go": "The green is not paint: it is a powdery crust left by the leaking batteries."},
             "why": "Corroded metal has been worn away by a chemical, here the liquid that leaked from the old batteries; that is why “the electricity can't get through”."},
            {"id": "cae988f045dd", "t": "mcq", "d": "infer", "q": "Why does Uncle Tariq go to help the woman with the lamp instead of cleaning the springs himself?",
             "opts": ["He wants Hana to finish the repair on her own",
                      "He thinks the radio is not worth mending after all",
                      "The woman has complained about waiting in the queue",
                      "He does not know how to clean corroded springs"],
             "no": {"He does not know how to clean corroded springs": "He knows exactly what is wrong and hands Hana the right things to clean them with."},
             "why": "He “did not take over”: he gave Hana the tools and left her to it, because today was her turn to do the repair."},
            {"id": "6e13b16a978e", "t": "mcq", "d": "infer", "q": "Why does Mr Jenkins say “it must be the dust” when the radio works again?",
             "opts": ["He is moved almost to tears and does not want to show it",
                      "The radio has been left in a dusty cupboard since August",
                      "He is warning Hana to clean the inside of the radio too",
                      "The community centre is dusty and is making him sneeze"],
             "why": "He goes quiet, then takes out a handkerchief and blows his nose: the radio and its memories mean a great deal to him, and blaming the dust hides how emotional he is."},
            {"id": "b8d759fd98e7", "t": "mcq", "d": "structure", "q": "Why does the story end with Hana saying “Don't guess” and pulling the clock towards her?",
             "opts": ["It shows she has learned her uncle's lesson and now feels ready to take on a repair herself",
                      "It shows she is tired of the radio and wants to try a more interesting job",
                      "It shows that her uncle has stopped helping at the repair café for good",
                      "It shows she is worried the clock will be too difficult for her to mend"],
             "why": "She repeats the first rule without being told it, and reaches for the clock at once: after mending the radio she is confident enough to start the next job on her own."},
        ],
    },
]
