"""Reading comprehension, Year 4, second set (keys RD4.15-RD4.28).

Fourteen more original passages, written by hand (SPEC_READING.md), 200-300 words each, six questions each,
mixing the KS2 reading domains. The topics differ from the first set (reading_y4.py): the Vikings, how
spiders spin their webs, the Indus Valley civilisation, bats, a paper aeroplane, Shackleton's Antarctic
journey, and realistic stories, a letter, a poem, a play script, a news report and a piece of persuasive
writing:

* RD4.15 The Vikings (information)
* RD4.16 The shark book (story: honesty)
* RD4.17 How a spider spins its web (explanation)
* RD4.18 A letter from Edinburgh (letter)
* RD4.19 Make a paper aeroplane (instructions)
* RD4.20 Cities of the Indus Valley (information: an early civilisation)
* RD4.21 Frost (poem: states of water)
* RD4.22 Ernest Shackleton and the Endurance (biography)
* RD4.23 Taid's video call (play script: patience, North Wales)
* RD4.24 Pupils build a hedgehog highway (news report)
* RD4.25 Bin it! Keep our park clean (persuasive writing)
* RD4.26 Grandmother's trees (story: Kenya)
* RD4.27 Bats: hunting with sound (information)
* RD4.28 The power cut (story: a family evening)

The people, schools and events in the stories, letter, play and news report are invented. May be reviewed
by any teacher or parent reviewer of the bank.
"""

SKILLS = [
    {
        "key": "RD4.15",
        "year": 4,
        "strand": "Information",
        "title": "The Vikings",
        "nc": "Retrieve and record information from non-fiction",
        "text": (
            "The Vikings came from Scandinavia, the part of northern Europe that is now Norway, Sweden and "
            "Denmark. Most Vikings were farmers and fishermen. They kept cattle, sheep and pigs, grew oats and "
            "barley, and lived in long wooden houses with a fire burning in the middle. There were no chimneys, "
            "so the smoke drifted out through a hole in the roof.\n\n"
            "In the late 700s, groups of Vikings began to sail across the North Sea to Britain. At first they "
            "came to raid: they attacked places on the coast, took what they could carry and sailed home again. "
            "Later, many came to stay. They settled in large parts of northern and eastern England and farmed "
            "the land, just as they had done at home.\n\n"
            "The Vikings were expert shipbuilders. Their longships were narrow and light, with a sail and rows "
            "of oars, so they could cross the open sea and also travel far up shallow rivers.\n\n"
            "One of the most important Viking towns in England was Jorvik, which we now call York. "
            "Archaeologists digging there have found the remains of wooden houses and workshops, combs made of "
            "bone and even shoes made of leather. These finds tell us that Jorvik was a busy place, full of "
            "craftspeople and traders.\n\n"
            "Viking traders travelled to many far-off lands. They swapped furs, wool and walrus ivory for "
            "silver, silk and spices.\n\n"
            "Viking words are still part of English today. “Sky”, “egg” and “window” all came from the "
            "language the Vikings spoke, and many places with names ending in “-by”, such as Whitby and "
            "Grimsby, were once Viking villages."
        ),
        "qs": [
            {"id": "5ddcaf1ea5ea", "t": "mcq", "d": "retrieve", "q": "How did the smoke from the fire get out of a Viking house?",
             "opts": ["through a hole in the roof", "up a tall stone chimney", "out of the open door",
                      "through the narrow windows"],
             "why": "The first paragraph says there were no chimneys, so the smoke drifted out through a hole in the roof."},
            {"id": "5f531b5d6892", "t": "mcq", "d": "vocab", "q": "“At first they came to raid.” What does “raid” mean here?",
             "opts": ["make a quick attack and take things", "stay and farm the land",
                      "swap goods with other people", "build new towns and villages"],
             "why": "The text explains it straight after: they attacked places, took what they could carry and sailed home.",
             "no": {"stay and farm the land": "That is what many Vikings did later, when they “came to stay”."}},
            {"id": "15aa4e628a62", "t": "tap", "d": "retrieve",
             "q": "Tap the two words that describe the longships and explain how they could travel up shallow rivers.",
             "s": "Their longships were [narrow] and [light], with a sail and rows of oars, so they could cross the open sea and also travel far up shallow rivers.",
             "why": "The longships were narrow and light, so they could travel far up shallow rivers."},
            {"id": "1544cd342f15", "t": "mcq", "d": "infer", "q": "What was the inside of a Viking house probably like?",
             "opts": ["smoky, with a fire in the middle", "cold, because there was no fire",
                      "bright, with large glass windows", "quiet, because no one cooked there"],
             "why": "A fire burned in the middle and the smoke had only a hole in the roof to escape through, so the "
                    "house would have been smoky."},
            {"id": "91a966863250", "t": "text", "d": "retrieve", "q": "Find and copy the Viking name for the town we now call York.",
             "a": ["Jorvik"],
             "why": "The fourth paragraph says Jorvik is the town we now call York."},
            {"id": "5a8b3477248a", "t": "mcq", "d": "summarise", "q": "Which would be the best other title for this text?",
             "opts": ["Who the Vikings were and what they left behind", "How to build a Viking longship",
                      "The day the Vikings found York", "Why the Vikings stopped farming"],
             "why": "The text covers Viking homes, journeys, ships, towns, trade and the words they left in English.",
             "no": {"How to build a Viking longship": "Longships take up only one short paragraph, and the text "
                                                       "does not tell you how to build one."}},
        ],
    },
    {
        "key": "RD4.16",
        "year": 4,
        "strand": "Stories",
        "title": "The shark book",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Tomasz had borrowed the book about sharks from the school library three weeks ago, and now it was "
            "gone. He had searched under his bed, behind the sofa and inside every bag in the house. His little "
            "sister, Ola, had even checked the fridge, just in case.\n\n"
            "On Friday morning, Mrs Adeyemi, the librarian, was stamping books at the front desk when Tomasz came "
            "in. His hands felt sticky and his heart was thumping.\n\n"
            "“I've lost the shark book,” he said quietly. “I'm really sorry. I've looked everywhere.”\n\n"
            "Mrs Adeyemi put down her stamp. “Thank you for telling me,” she said. “Most people just hope I won't "
            "notice.”\n\n"
            "“Will I have to pay for it?” asked Tomasz. He had four pounds and twenty pence in his money box, and "
            "he had been saving it for a new football.\n\n"
            "“Let's not worry about that yet,” said Mrs Adeyemi. “Books have a way of turning up. Keep looking, "
            "and come back on Monday.”\n\n"
            "All weekend, Tomasz thought about the book. On Sunday afternoon, he went with Dad to fetch the "
            "camping chairs from the shed. When Dad unfolded the second chair, something slid out of the cloth "
            "pocket on its back and landed with a thud on the grass. It was the shark book, a little dusty but "
            "not torn.\n\n"
            "Tomasz remembered at once. He had been reading in the garden one sunny evening, and when it started "
            "to rain he had pushed the book into the pocket of his chair.\n\n"
            "On Monday, he was waiting at the library door before it opened. Mrs Adeyemi smiled as he held up "
            "the book.\n\n"
            "“You see?” she said. “Telling the truth is never wasted. Now, would you like to borrow the one about "
            "whales?”"
        ),
        "qs": [
            {"id": "6eab508cdde6", "t": "mcq", "d": "retrieve", "q": "Who checked the fridge for the missing book?",
             "opts": ["Ola", "Dad", "Tomasz", "Mrs Adeyemi"],
             "why": "The first paragraph says his little sister, Ola, even checked the fridge, just in case."},
            {"id": "1b4eb69b1f04", "t": "mcq", "d": "infer", "q": "How was Tomasz feeling when he came into the library on Friday?",
             "opts": ["nervous", "excited", "bored", "cross"],
             "why": "His hands were sticky and his heart was thumping because he had to own up to losing the book.",
             "no": {"excited": "A thumping heart can mean excitement, but Tomasz was about to say he had lost the "
                               "book, and he spoke quietly and said sorry."}},
            {"id": "b46f6f17ae46", "t": "mcq", "d": "infer", "q": "Why was Tomasz worried about having to pay for the book?",
             "opts": ["He was saving his money for a football", "He had no money at all",
                      "His dad had told him not to pay", "The book cost more than ten pounds"],
             "why": "He had four pounds twenty in his money box, and he had been saving it for a new football."},
            {"id": "58325507d8ef", "t": "mcq", "d": "vocab", "q": "“Books have a way of turning up.” What does “turning up” mean here?",
             "opts": ["being found again", "being returned late", "getting torn", "going round in circles"],
             "why": "Mrs Adeyemi means lost books are often found again, and the shark book was."},
            {"id": "bb9a6639d3cc", "t": "mcq", "d": "retrieve", "q": "Where was the book found?",
             "opts": ["in the pocket of a camping chair", "on a shelf in the shed", "under Tomasz's bed",
                      "inside a bag in the house"],
             "why": "It slid out of the cloth pocket on the back of a camping chair when Dad unfolded it.",
             "no": {"on a shelf in the shed": "The chairs were kept in the shed, but the book was inside a chair's pocket."}},
            {"id": "d8f277fc5ea5", "t": "mcq", "d": "summarise", "q": "What is the main message of the story?",
             "opts": ["Owning up is the right thing to do, even when it is hard", "Library books should never be taken home",
                      "You should always pay for something you lose", "Sharks are more interesting than whales"],
             "why": "Tomasz was nervous but told the truth, and Mrs Adeyemi says “Telling the truth is never wasted.”"},
        ],
    },
    {
        "key": "RD4.17",
        "year": 4,
        "strand": "Explanations",
        "title": "How a spider spins its web",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "Spiders make silk inside their bodies. At first the silk is a liquid, but as the spider pulls it out "
            "through tiny tubes called spinnerets, near the end of its body, it hardens into a thread. For its "
            "thickness, spider silk is amazingly strong, and it can stretch a long way without snapping.\n\n"
            "Not every spider builds a web. The garden spider, which is common in Britain in late summer and "
            "autumn, builds a round one called an orb web. Here is how it does it.\n\n"
            "First, the spider lets out a long, fine thread from a high place and waits for the breeze to carry "
            "it. When the loose end catches on a twig or a fence, the spider has a bridge. It walks along this "
            "thread to make it stronger, then adds more threads to build a frame.\n\n"
            "Next, the spider runs threads from the edge of the frame to the middle, like the spokes of a bicycle "
            "wheel. These spokes are not sticky. After that, it lays a spiral of sticky silk round and round, "
            "starting near the edge and working in towards the centre. As it moves about, the spider steps mostly "
            "on the dry spokes, which helps it not to get caught in its own trap.\n\n"
            "When the web is finished, the spider waits, either in the centre or hidden close by with one leg "
            "resting on a signal thread. If an insect flies into the sticky spiral, the web shakes. The spider "
            "rushes out and wraps its prey in silk.\n\n"
            "A web is soon damaged by wind, rain and struggling insects, so many garden spiders build a new one "
            "almost every day. Some even eat the old silk and use it again."
        ),
        "qs": [
            {"id": "cf1c7753a2ef", "t": "text", "d": "retrieve", "q": "Find and copy the word for the tiny tubes that the silk comes out of.",
             "a": ["spinnerets", "spinneret"],
             "why": "The first paragraph says the silk is pulled out through tiny tubes called spinnerets."},
            {"id": "aefd56d18675", "t": "mcq", "d": "structure", "q": "Why does the second paragraph end with “Here is how it does it.”?",
             "opts": ["to tell the reader that the steps for building a web come next",
                      "to show that the spider is speaking to the reader",
                      "to show that the explanation is now finished",
                      "to ask the reader to try building a web"],
             "why": "This sentence leads into the paragraphs that follow, which explain the building of the web step by step."},
            {"id": "8f716768bff7", "t": "order", "d": "sequence", "q": "Put these in the order the garden spider does them.",
             "items": ["The breeze carries a long thread to a twig", "The spider builds a frame",
                       "The spider adds the spokes", "The spider lays the sticky spiral"],
             "why": "First comes the bridge thread, then the frame, then the spokes from the edge to the middle, and last the sticky spiral."},
            {"id": "31d3f18e420c", "t": "mcq", "d": "language", "q": "Why does the writer say the threads are “like the spokes of a bicycle wheel”?",
             "opts": ["to help the reader picture lines spreading out from the middle",
                      "to show that the web turns round like a wheel",
                      "to explain why these threads are sticky",
                      "to show how fast the spider can move"],
             "why": "A bicycle wheel's spokes run straight out from the centre to the rim, just as these threads run from the middle of the web to its frame."},
            {"id": "a7bba3db1019", "t": "mcq", "d": "infer", "q": "Why does a hidden spider keep one leg on a signal thread?",
             "opts": ["so it can feel the web shake when an insect is caught",
                      "so the web does not blow away in the wind",
                      "so it can make more silk while it waits",
                      "so it does not get stuck on the sticky spiral"],
             "why": "An insect hitting the web makes it shake. With a leg on the signal thread, the hidden spider can feel this and rush out.",
             "no": {"so it does not get stuck on the sticky spiral": "The spider avoids getting stuck by stepping on the dry spokes; the signal thread is for feeling the web shake."}},
            {"id": "ced406743cb7", "t": "mcq", "d": "vocab", "q": "“The spider rushes out and wraps its prey in silk.” What is “prey”?",
             "opts": ["an animal that is caught to be eaten", "a thread that holds the web up",
                      "a hiding place close to the web", "a spider that shares the web"],
             "why": "Prey is an animal hunted or caught by another animal for food. Here it is the insect caught in the web."},
        ],
    },
    {
        "key": "RD4.18",
        "year": 4,
        "strand": "Letters and diaries",
        "title": "A letter from Edinburgh",
        "nc": "Retrieve and record information; identify how language, structure and presentation contribute to meaning",
        "text": (
            "Dear Grandpa,\n\n"
            "Thank you for the birthday money. I spent some of it on a postcard of Edinburgh Castle, which I have "
            "put inside this letter, and I am saving the rest for a new sketchbook.\n\n"
            "We have been here for three days now, and Edinburgh is nothing like Leeds. The old part of the city "
            "is built on a steep hill, and the streets are made of cobbles that make your ankles wobble. Mum says "
            "the castle stands on rock that was once part of a volcano, millions of years ago. I could hardly "
            "believe it, but our guide said the same thing, so it must be true.\n\n"
            "Yesterday we climbed Arthur's Seat, which is a big hill right next to the city centre. It was so "
            "windy at the top that Amara's hat blew off and rolled all the way down the slope. Dad chased after it "
            "for ages, and she laughed so much she had to sit down. From the top we could see the whole city, the "
            "sea, and even some hills far away on the other side of the water.\n\n"
            "Today it rained all morning, so we spent it in a museum. My favourite room was full of old clocks and "
            "machines with cogs that still turned. I sat on a bench and drew three of them in my notebook.\n\n"
            "Tomorrow we are catching the train home. I will show you all my drawings when you come for lunch on "
            "Sunday.\n\n"
            "Lots of love,\n"
            "Kemi"
        ),
        "qs": [
            {"id": "84d5be666291", "t": "mcq", "d": "retrieve", "q": "What has Kemi put inside the letter?",
             "opts": ["a postcard of Edinburgh Castle", "some of her birthday money", "a new sketchbook",
                      "a drawing of a clock"],
             "why": "The first paragraph says she bought a postcard of the castle and put it inside the letter."},
            {"id": "ce3e83dd074a", "t": "mcq", "d": "vocab", "q": "The streets “are made of cobbles that make your ankles wobble”. What are cobbles?",
             "opts": ["rounded stones set into the road", "steep steps cut into a hill",
                      "smooth, flat paving slabs", "puddles left behind by the rain"],
             "why": "Cobbles are rounded stones set close together; their bumpy tops are what make ankles wobble.",
             "no": {"smooth, flat paving slabs": "Smooth, flat slabs would not make your ankles wobble."}},
            {"id": "87362d487fcd", "t": "mcq", "d": "infer", "q": "“I could hardly believe it, but our guide said the same thing, so it must be true.” What does this show?",
             "opts": ["Kemi was surprised by the fact at first", "Kemi already knew all about volcanoes",
                      "Kemi thinks her mum often makes things up", "Kemi did not enjoy the guided tour"],
             "why": "“I could hardly believe it” shows the fact surprised her, until a second person said the same thing."},
            {"id": "3a97321ee0de", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you whose hat blew off.",
             "s": "It was so windy at the top that [Amara's] hat blew off and rolled all the way down the slope.",
             "why": "It was Amara's hat that blew off at the top of Arthur's Seat."},
            {"id": "cbfad04e3c63", "t": "order", "d": "sequence", "q": "Put these in the order they happen, from what the letter says.",
             "items": ["The family arrives in Edinburgh", "They climb Arthur's Seat", "Kemi draws machines in a museum",
                       "They catch the train home"],
             "why": "They arrived three days ago, climbed Arthur's Seat yesterday, went to the museum today and go "
                    "home tomorrow."},
            {"id": "1e18355ab192", "t": "mcq", "d": "purpose", "q": "Why did Kemi write this letter?",
             "opts": ["to thank Grandpa and tell him about her trip", "to ask Grandpa for more birthday money",
                      "to invite Grandpa to visit Edinburgh", "to explain how volcanoes are made"],
             "why": "She begins by thanking him for the money, then tells him what she has done in Edinburgh."},
        ],
    },
    {
        "key": "RD4.19",
        "year": 4,
        "strand": "Instructions",
        "title": "Make a paper aeroplane",
        "nc": "Retrieve and record information from non-fiction; discuss how structure and presentation contribute to meaning",
        "text": (
            "A paper aeroplane takes only a few minutes to make. All you need is one sheet of A4 paper and a flat "
            "table to fold it on. Read all the steps before you begin.\n\n"
            "1. Lay the paper on the table with its short edges at the top and the bottom.\n"
            "2. Fold the paper in half lengthways, so that the two long edges meet. Run your thumbnail along the "
            "fold to make a sharp crease, then open the paper out flat again.\n"
            "3. Fold the two top corners in so that their edges meet along the centre crease. The top of the "
            "paper now looks like the roof of a house.\n"
            "4. Fold the two new slanting edges in to the centre crease again. This makes the nose of the plane "
            "long and pointed.\n"
            "5. Fold the whole plane in half along the centre crease, with all your folds on the outside.\n"
            "6. Fold one side down to make a wing, so that its slanting edge lines up with the bottom edge of the "
            "plane. Turn the plane over and do the same on the other side.\n"
            "7. Lift both wings up so that they stick out level. From the front, the plane should look like a "
            "letter T.\n\n"
            "To fly your plane, hold it underneath, near the front, and throw it gently forwards and a little "
            "upwards. Never aim it at a person or an animal.\n\n"
            "Now see if you can make it fly better. If it dives straight into the ground, bend the back edges of "
            "both wings up a tiny amount. If it keeps turning to one side, check that the two wings are the same "
            "shape. Change only one thing at a time, then throw the plane again and watch what happens."
        ),
        "qs": [
            {"id": "901e239f56e4", "t": "text", "d": "retrieve", "q": "Find and copy the size of paper you need.",
             "a": ["A4", "A4 paper", "a sheet of A4", "one sheet of A4 paper", "a sheet of A4 paper"],
             "why": "The first paragraph says all you need is one sheet of A4 paper and a flat table."},
            {"id": "371894960aa4", "t": "mcq", "d": "vocab", "q": "In step 2, you “make a sharp crease”. What is a crease?",
             "opts": ["a line pressed into paper by folding it", "a cut made in paper with scissors",
                      "a corner of a sheet of paper", "a line drawn on paper with a ruler"],
             "why": "You make the crease by running your thumbnail along the fold: it is the line the fold leaves."},
            {"id": "f73203f05c75", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Fold the paper in half and open it out", "Fold the top corners in to the centre crease",
                       "Fold the slanting edges in to the centre again", "Fold the whole plane in half",
                       "Fold down a wing on each side"],
             "why": "Steps 2 to 6 give the folds in this order: the centre crease, the corners, the slanting edges, "
                    "the whole plane in half, then the wings."},
            {"id": "543cbb686bd5", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how hard to throw the plane.",
             "s": "To fly your plane, hold it underneath, near the front, and throw it [gently] forwards and a little upwards.",
             "why": "The text says to throw it gently: a hard throw would not help it glide."},
            {"id": "972db8309090", "t": "mcq", "d": "infer", "q": "Why should you change only one thing at a time when you test your plane?",
             "opts": ["so you can tell which change made the difference", "so the paper does not tear",
                      "so the plane is ready to fly more quickly", "so you do not need a second sheet of paper"],
             "why": "If you changed two things at once and the plane flew better, you would not know which change "
                    "had helped."},
            {"id": "ea73a987f261", "t": "mcq", "d": "summarise", "q": "What are the last two paragraphs mostly about?",
             "opts": ["flying the plane and making it fly better", "folding the wings into the right shape",
                      "the things you need before you start", "why some planes turn to one side"],
             "why": "After the numbered steps, the text tells you how to throw the plane and how to fix it if it "
                    "dives or turns.",
             "no": {"why some planes turn to one side": "The text tells you what to check if it turns, but that "
                                                         "is only one part of the last paragraph."}},
        ],
    },
    {
        "key": "RD4.20",
        "year": 4,
        "strand": "Information",
        "title": "Cities of the Indus Valley",
        "nc": "Retrieve and record information from non-fiction; identify main ideas drawn from more than one paragraph",
        "text": (
            "About four and a half thousand years ago, one of the world's earliest civilisations grew up beside "
            "the River Indus, in what is now Pakistan and north-west India. Every year the river flooded and left "
            "behind rich soil, where farmers grew wheat, barley and cotton.\n\n"
            "The Indus people built large cities. The two best known today are Mohenjo-daro and Harappa. What "
            "makes them special is how carefully they were planned. The main streets were straight and crossed "
            "each other at right angles, making a pattern like a grid. Houses were built of baked mud bricks, and "
            "in many different towns the bricks were made to the same shape and proportions.\n\n"
            "The cities were also very clean for their time. Many houses had their own washing area and a toilet. "
            "Waste water from the houses flowed into drains that ran under the streets, covered with bricks. In "
            "Mohenjo-daro there was a large pool, now called the Great Bath, which had a layer of natural tar behind "
            "its brick walls to keep the water in. Nobody knows for certain what it was used for.\n\n"
            "The Indus people were traders. They used sets of stone weights, all carefully measured, so that goods "
            "could be weighed fairly. They also carved small, square seals out of stone. Many seals show an animal, "
            "such as a bull or an elephant, along with a few signs of writing. Experts have studied these signs "
            "for many years, but nobody has yet worked out how to read them.\n\n"
            "After hundreds of years, the great cities slowly emptied, and they lay buried until archaeologists "
            "began to dig them up in the 1920s."
        ),
        "qs": [
            {"id": "20ab53de5bb3", "t": "text", "d": "retrieve", "q": "What did the river leave behind when it flooded? Find and copy two words.",
             "a": ["rich soil"],
             "why": "The first paragraph says the river flooded every year and left behind rich soil."},
            {"id": "c9425400215f", "t": "mcq", "d": "vocab", "q": "The main streets made “a pattern like a grid”. What does this tell you about them?",
             "opts": ["They ran in straight lines that crossed to make squares", "They wound round and round in circles",
                      "They were built on top of one another", "They all led down to the river"],
             "why": "A grid is a pattern of straight lines crossing at right angles, like the squares on squared paper."},
            {"id": "5f91ebb30849", "t": "mcq", "d": "infer", "q": "Which detail best shows that the Indus cities were carefully planned?",
             "opts": ["The main streets were straight and crossed at right angles.",
                      "The river flooded the fields every year.",
                      "Farmers grew wheat, barley and cotton.",
                      "Many seals showed a bull or an elephant."],
             "why": "Straight streets meeting at right angles do not happen by chance: someone must have planned where they would go."},
            {"id": "df1307425d25", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what the drains were covered with.",
             "s": "Waste water from the houses flowed into drains that ran under the streets, covered with [bricks].",
             "why": "The drains ran under the streets and were covered with bricks."},
            {"id": "08c439c47c78", "t": "mcq", "d": "retrieve", "q": "Why did the Indus people use carefully measured stone weights?",
             "opts": ["so that goods could be weighed fairly", "to hold down the roofs of their houses",
                      "to carve the small square seals", "to line the Great Bath"],
             "why": "The fourth paragraph says the weights were carefully measured so that goods could be weighed fairly.",
             "no": {"to line the Great Bath": "The Great Bath was kept watertight with tar and bricks, not with weights."}},
            {"id": "40b4f604ae88", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the whole text?",
             "opts": ["The Indus people built well-planned, clean cities and were skilled traders.",
                      "The Indus people lived in small villages with no streets or drains.",
                      "Experts can now read all of the writing on the Indus seals.",
                      "The River Indus flooded so often that nobody could farm there."],
             "why": "The text describes the planned streets, the drains and the Great Bath, and the weights and seals used for trade."},
        ],
    },
    {
        "key": "RD4.21",
        "year": 4,
        "strand": "Poems",
        "title": "Frost",
        "nc": "Discuss words and phrases that capture the reader's interest and imagination; recognise some different forms of poetry",
        "text": (
            "Last night, while all the town was still\n"
            "and every light was out,\n"
            "the cold came creeping down the hill\n"
            "and wandered all about.\n\n"
            "It breathed on every garden gate,\n"
            "on every car and wall;\n"
            "it found the window by my bed\n"
            "and did not knock at all.\n\n"
            "The air was full of water, thin\n"
            "as breath and out of sight;\n"
            "it touched the icy glass, and froze\n"
            "in patterns, sharp and white.\n\n"
            "At seven, when I raised the blind,\n"
            "I gasped at what I found:\n"
            "a forest made of silver ferns\n"
            "that grew without a sound,\n\n"
            "with feathers, stars and spiky lace\n"
            "and rivers branching wide,\n"
            "as if some artist, small and neat,\n"
            "had drawn them from outside.\n\n"
            "I pressed my warm thumb on the frost\n"
            "and counted up to ten;\n"
            "a tiny, see-through circle cleared,\n"
            "then slowly froze again.\n\n"
            "By nine, the sun had climbed the roofs\n"
            "and found my window pane;\n"
            "the ferns went soft, the forest wept,\n"
            "and trickled down like rain.\n\n"
            "The drops rolled down and dried away,\n"
            "back into air once more,\n"
            "to wait for one more freezing night,\n"
            "as they have done before.\n\n"
            "So if you wake one winter day\n"
            "and find your window white,\n"
            "remember what the cold has drawn\n"
            "while you slept through the night."
        ),
        "qs": [
            {"id": "67ded32dca28", "t": "mcq", "d": "language", "q": "Why does the poet say the cold came “creeping” down the hill?",
             "opts": ["to show it arrived slowly and quietly", "to show it arrived with a loud crash",
                      "to show it rushed past very fast", "to show it stayed for only a moment"],
             "why": "Creeping is moving slowly and quietly, so nobody notices: the town was still and asleep."},
            {"id": "37d9b4e3a59c", "t": "text", "d": "retrieve", "q": "At what time did the poet raise the blind?",
             "a": ["seven", "at seven", "7", "seven o'clock"],
             "why": "The fourth verse begins “At seven, when I raised the blind”."},
            {"id": "05c7908cb81d", "t": "mcq", "d": "infer", "q": "“I gasped at what I found.” How did the poet feel on seeing the frost?",
             "opts": ["amazed", "frightened", "bored", "disappointed"],
             "why": "The poet goes on to describe a silver forest, feathers, stars and lace: the gasp is wonder at "
                    "something beautiful.",
             "no": {"frightened": "People can gasp in fright, but the poet describes the frost as beautiful and "
                                  "even touches it."}},
            {"id": "c42a28eafffd", "t": "tap", "d": "language", "q": "Tap the word that makes the melting frost sound like someone crying.",
             "s": "the ferns went soft, the forest [wept],",
             "why": "To weep is to cry: the drops of melting frost are like tears running down."},
            {"id": "f8e7934bc0ec", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the poem.",
             "items": ["The cold comes down the hill", "Frost patterns form on the glass",
                       "The poet presses a thumb on the frost", "The sun melts the frost",
                       "The drops dry away into the air"],
             "why": "The poem follows one night and morning: the cold arrives, frost forms, the poet touches it, the "
                    "sun melts it and the drops dry away."},
            {"id": "13cb7fdec094", "t": "mcq", "d": "summarise", "q": "What is the poem mainly about?",
             "opts": ["frost forming on a window and then disappearing", "a child who is afraid of the cold",
                      "an artist drawing patterns on glass", "a winter walk down a frosty hill"],
             "why": "Each verse follows the frost: the cold arrives, the patterns form, then the sun melts them and "
                    "the water dries away.",
             "no": {"an artist drawing patterns on glass": "The poet only says it looks “as if” an artist had drawn "
                                                            "them: the cold made the patterns."}},
        ],
    },
    {
        "key": "RD4.22",
        "year": 4,
        "strand": "Biography",
        "title": "Ernest Shackleton and the Endurance",
        "nc": "Retrieve and record information from non-fiction; draw inferences and justify them with evidence",
        "text": (
            "Ernest Shackleton was an explorer who was born in Ireland in 1874. As a young man he went to sea, and "
            "he soon dreamed of exploring Antarctica, the frozen continent around the South Pole.\n\n"
            "In 1914, Shackleton set out with a team of sailors and scientists on a ship called the Endurance. His "
            "plan was to cross the whole of Antarctica on foot, from one side to the other. No one had ever done "
            "it before.\n\n"
            "The plan went wrong before it had even begun. In early 1915, the Endurance became stuck in the thick "
            "sea ice of the Weddell Sea. For months the ship drifted, trapped, while the ice squeezed it tighter "
            "and tighter. At last, the ice crushed the ship and it sank. The men camped on the floating ice, with "
            "three small lifeboats they had saved.\n\n"
            "In April 1916, when the ice began to break up, they rowed to a rocky, empty place called Elephant "
            "Island. They were on land again, but no one in the world knew where they were. Shackleton decided to "
            "go for help. With five of the men, he sailed one of the small boats about 800 miles across some of the "
            "stormiest seas on Earth to the island of South Georgia. Then Shackleton and two of the men crossed its "
            "icy mountains on foot to reach a station on the other side, where people lived and worked.\n\n"
            "Shackleton would not rest until he had rescued the men left behind. His first attempts were stopped by "
            "the ice, but in August 1916 he reached Elephant Island at last. Every one of the men there was still "
            "alive.\n\n"
            "In 2022, explorers found the wreck of the Endurance, deep at the bottom of the Weddell Sea."
        ),
        "qs": [
            {"id": "d7cb085e7521", "t": "mcq", "d": "retrieve", "q": "What was Shackleton's plan when he set out in 1914?",
             "opts": ["to cross the whole of Antarctica on foot", "to sail all the way round Antarctica",
                      "to find a ship lost in the ice", "to build a station on South Georgia"],
             "why": "The second paragraph says his plan was to cross the whole of Antarctica on foot."},
            {"id": "ecd7a2e7898a", "t": "mcq", "d": "vocab", "q": "“For months the ship drifted, trapped.” What does “drifted” mean here?",
             "opts": ["moved slowly, carried along by the ice", "sailed fast towards land",
                      "stayed completely still", "sank to the bottom of the sea"],
             "why": "The ship was stuck in floating sea ice, so it was carried slowly along wherever the ice went.",
             "no": {"sank to the bottom of the sea": "The ship only sank later, when the ice crushed it."}},
            {"id": "3406b5db65ac", "t": "order", "d": "sequence", "q": "Put these in the order they happen.",
             "items": ["The Endurance gets stuck in the ice", "The ice crushes the ship",
                       "The men reach Elephant Island", "Shackleton sails to South Georgia",
                       "The men on Elephant Island are rescued"],
             "why": "The text tells the events in order, from the ship getting stuck in 1915 to the rescue in August 1916."},
            {"id": "73083a4981e8", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how many men sailed with Shackleton to South Georgia.",
             "s": "With [five] of the men, he sailed one of the small boats about 800 miles across some of the stormiest seas on Earth to the island of South Georgia.",
             "why": "Five men went with him, so six sailed in the small boat."},
            {"id": "b2efee77a3a4", "t": "mcq", "d": "infer", "q": "What does the text suggest about Shackleton?",
             "opts": ["He was determined and cared about his men", "He was careless with his ship",
                      "He gave up as soon as things went wrong", "He wanted to be famous more than anything"],
             "why": "He made a dangerous journey for help and kept trying until every man was rescued.",
             "no": {"He wanted to be famous more than anything": "The text never mentions fame; it shows him "
                                                                  "risking his life to save the others."}},
            {"id": "369df77834f5", "t": "mcq", "d": "structure", "q": "Why does the writer end with the wreck being found in 2022?",
             "opts": ["to link the old story to our own time", "to explain why the ship sank",
                      "to show how the men were rescued", "to describe life on Elephant Island"],
             "why": "The rest of the text happened over a hundred years ago; the last line shows the story still "
                    "matters today."},
        ],
    },
    {
        "key": "RD4.23",
        "year": 4,
        "strand": "Play scripts",
        "title": "Taid's video call",
        "nc": "Prepare play scripts to read aloud and perform; draw inferences about characters' feelings",
        "text": (
            "(Taid's kitchen in Bangor, North Wales. TAID sits at the table, holding a tablet very close to his "
            "face. ELIN and RHYS stand behind him.)\n"
            "TAID: Your Auntie Mari is in Canada, and this thing is supposed to let me see her. "
            "All I can see is my own nose.\n"
            "ELIN: That's the camera, Taid. Hold it further away, and a bit lower.\n"
            "(TAID lowers the tablet so far that it points at the ceiling.)\n"
            "RHYS: (giggling) Now Auntie Mari will only see the lampshade.\n"
            "ELIN: Here, let me do it. It'll be quicker.\n"
            "(ELIN reaches for the tablet. TAID holds on to it.)\n"
            "TAID: (firmly) Quicker for you, cariad. But you won't be here next Sunday, when I want to call her "
            "again.\n"
            "(ELIN stops, then lets go.)\n"
            "ELIN: Sorry, Taid. I'll tell you what to press, and you press it.\n"
            "RHYS: And I'll write the steps on a card, so you can keep it by the kettle.\n"
            "TAID: Now you're talking.\n"
            "(ELIN points. TAID taps the screen slowly. A ringing sound.)\n"
            "TAID: It's ringing! Now what?\n"
            "ELIN: Just wait. Hold it steady.\n"
            "AUNTIE MARI: (from the tablet) Dad? I can see you! But I can't hear a word you're saying.\n"
            "RHYS: (whispering) The microphone button, Taid. The one with a line through it.\n"
            "(TAID taps it.)\n"
            "TAID: Mari? Can you hear me now?\n"
            "AUNTIE MARI: Loud and clear! Oh, it's so good to see you.\n"
            "TAID: (beaming at the children) And I did it myself. Well, nearly.\n"
            "(The next Sunday. TAID is alone in the kitchen. RHYS's card is propped against the kettle. TAID reads "
            "it, taps the screen and holds the tablet steady.)\n"
            "AUNTIE MARI: (from the tablet) Dad! You called me all by yourself!\n"
            "TAID: (proudly) Step four, cariad. Never forget the microphone."
        ),
        "qs": [
            {"id": "39c902c5af93", "t": "mcq", "d": "infer", "q": "Who is Taid?",
             "opts": ["Elin and Rhys's grandfather", "Elin and Rhys's father",
                      "Auntie Mari's brother", "a neighbour who lives next door"],
             "why": "Auntie Mari calls him “Dad”. She is Elin and Rhys's aunt, so her dad is their grandfather. (Taid is a Welsh word for grandad.)",
             "no": {"Auntie Mari's brother": "Auntie Mari calls him “Dad”, so he is her father, not her brother."}},
            {"id": "854a605ffe1e", "t": "text", "d": "retrieve", "q": "When Taid lowers the tablet too far, what does Rhys say Auntie Mari will see? Find and copy the word.",
             "a": ["lampshade", "the lampshade"],
             "why": "Rhys giggles and says Auntie Mari will only see the lampshade, because the camera points at the ceiling."},
            {"id": "f8f73c2568b9", "t": "mcq", "d": "infer", "q": "Why does Taid hold on to the tablet when Elin reaches for it?",
             "opts": ["He wants to learn to make the call himself", "He is afraid Elin will drop it",
                      "He is cross that Rhys laughed at him", "He wants Elin to write the steps down"],
             "why": "He says Elin won't be there next Sunday when he wants to call again, so he needs to learn to do it on his own.",
             "no": {"He wants Elin to write the steps down": "Writing the steps on a card is Rhys's idea, and it comes after Taid holds on to the tablet."}},
            {"id": "f88675407308", "t": "mcq", "d": "vocab", "q": "When Rhys offers to write the steps on a card, Taid says, “Now you're talking.” What does he mean?",
             "opts": ["That's a good idea.", "Please speak more loudly.",
                      "You can talk to Mari now.", "Stop talking and listen."],
             "why": "“Now you're talking” is a way of saying someone has had a good idea. Taid is pleased with Rhys's plan."},
            {"id": "ea493bf7ab39", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you where Taid can keep Rhys's card.",
             "s": "RHYS: And I'll write the steps on a card, so you can keep it by the [kettle].",
             "why": "Rhys says Taid can keep the card by the kettle, and in the last scene it is propped against the kettle."},
            {"id": "8f83b1b6b665", "t": "mcq", "d": "structure", "q": "Why does the play end with a scene from the next Sunday?",
             "opts": ["to show that Taid can now make the call on his own",
                      "to show that Elin and Rhys have moved to Canada",
                      "to show that Auntie Mari has come home to visit",
                      "to show that the tablet has stopped working"],
             "why": "In the last scene Taid is alone, follows the card, and Auntie Mari says he called her all by himself."},
        ],
    },
    {
        "key": "RD4.24",
        "year": 4,
        "strand": "News reports",
        "title": "Pupils build a hedgehog highway",
        "nc": "Identify how language, structure and presentation contribute to meaning; distinguish fact from opinion",
        "text": (
            "Children at Little Ashby Primary School in Norfolk have helped to link up more than forty gardens in "
            "their village, so that hedgehogs can move safely from one to another.\n\n"
            "The project began last spring, when Class 4 learned that the number of hedgehogs in Britain has fallen "
            "sharply in recent years. “We found out that hedgehogs walk a long way every night looking for food,” "
            "said Freya, aged nine. “But fences and walls get in the way, so they end up on the roads instead.”\n\n"
            "The class wrote a letter to every house in the village, asking families to make a small gap at the "
            "bottom of their garden fence. The gap only needs to be about 13 centimetres wide and 13 centimetres "
            "high. “That is big enough for a hedgehog, but too small for most pets,” explained their teacher, "
            "Mr Bashir.\n\n"
            "Forty-three families said yes. Some cut holes in their fences, while others dug a small tunnel under "
            "a wall. The pupils painted a sign for each gap so that nobody would block it up by mistake.\n\n"
            "Now a camera in the school garden has caught something special. Last Tuesday night, it filmed two "
            "hedgehogs passing through the gap in the school fence.\n\n"
            "“It was the best thing I've ever seen,” said Ibrahim, aged eight. “I think every village should do "
            "this.”\n\n"
            "The school plans to visit two nearby villages next term to help them start highways of their own.\n\n"
            "Hedgehogs are nocturnal, which means they are mostly active at night. In a single night, a hedgehog "
            "can travel about a mile."
        ),
        "qs": [
            {"id": "f0ad090bc7c6", "t": "mcq", "d": "retrieve", "q": "How many families agreed to make a gap?",
             "opts": ["forty-three", "forty", "thirteen", "two"],
             "why": "The fourth paragraph says forty-three families said yes.",
             "no": {"thirteen": "13 centimetres is the size of the gap, not the number of families."}},
            {"id": "b28af0a1730d", "t": "mcq", "d": "vocab", "q": "The number of hedgehogs “has fallen sharply”. What does this mean?",
             "opts": ["has gone down by a lot", "has gone up a little", "has stayed the same",
                      "has gone down very slowly"],
             "why": "“Fallen sharply” means dropped quickly and by a lot: that is why the class wanted to help."},
            {"id": "4549d7c66d7a", "t": "mcq", "d": "infer", "q": "Why should the gap be too small for most pets?",
             "opts": ["so that dogs and cats cannot get into other people's gardens",
                      "so that hedgehogs do not get stuck in it", "so that the fence does not fall down",
                      "so that the gap cannot be seen from the road"],
             "why": "A gap pets could squeeze through would let them wander into the next garden; a small gap lets "
                    "only hedgehogs through."},
            {"id": "8bf1883eb321", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you on which day the camera filmed the hedgehogs.",
             "s": "Last [Tuesday] night, it filmed two hedgehogs passing through the gap in the school fence.",
             "why": "The report says the camera filmed them last Tuesday night."},
            {"id": "18158d242ea5", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion, not a fact?",
             "opts": ["“I think every village should do this.”", "Forty-three families said yes.",
                      "Hedgehogs are mostly active at night.", "The camera filmed two hedgehogs."],
             "why": "“I think … should” shows what Ibrahim believes; the others can be checked and shown to be true."},
            {"id": "8272e620975a", "t": "mcq", "d": "structure", "q": "Why does the reporter include the words of Freya, Ibrahim and Mr Bashir?",
             "opts": ["to let the people who took part explain it in their own words",
                      "to show that the pupils disagreed about the project",
                      "to give the instructions for cutting a hole in a fence",
                      "to list every family who made a gap"],
             "why": "News reports quote the people involved: Freya explains the problem, Mr Bashir the gap size, and "
                    "Ibrahim how it felt."},
        ],
    },
    {
        "key": "RD4.25",
        "year": 4,
        "strand": "Persuasive writing",
        "title": "Bin it! Keep our park clean",
        "nc": "Identify how language, structure and presentation contribute to meaning; distinguish fact from opinion",
        "text": (
            "Hollybank Park is right next to our school. We play football there, we race each other round the "
            "pond, and at weekends it is full of families. But look a little closer and you will see crisp "
            "packets under the benches, cans in the bushes and plastic bottles floating on the pond. It is time "
            "for all of us to say: bin it!\n\n"
            "First of all, litter harms wildlife. Hedgehogs can get their heads stuck in empty cans and yoghurt "
            "pots, and birds can get tangled up in plastic. Ducks may swallow small pieces of plastic because "
            "they think it is food. An animal cannot read a sign saying “Keep away”, so it is up to us to keep "
            "it safe.\n\n"
            "Litter also lasts much longer than most people think. Plastic does not rot away like fallen leaves "
            "do. A bottle dropped in the park today could still be lying there when we are grown up.\n\n"
            "Some people say that picking up litter is the council's job. It is true that the park keepers empty "
            "the bins. However, they cannot be everywhere at once, and if nobody dropped litter in the first "
            "place, there would be nothing for anyone to pick up.\n\n"
            "Best of all, keeping the park clean is easy. There are eight bins in Hollybank Park, so there is "
            "always one close by. If a bin is full, take your rubbish home with you.\n\n"
            "I think a clean park is a happier park for everyone. So come and join Class 4 for our big litter "
            "pick this Saturday at ten o'clock. We will bring gloves and bags; you just need to bring a "
            "grown-up. Together, we can make Hollybank shine!\n\n"
            "Priya Nair, Class 4"
        ),
        "qs": [
            {"id": "faa006dab5a6", "t": "mcq", "d": "retrieve", "q": "Where in the park has the writer seen plastic bottles?",
             "opts": ["floating on the pond", "under the benches", "in the bushes", "next to the bins"],
             "why": "The first paragraph says crisp packets are under the benches, cans are in the bushes and "
                    "plastic bottles are floating on the pond.",
             "no": {"under the benches": "That is where the crisp packets are.",
                    "in the bushes": "That is where the cans are."}},
            {"id": "9a641bdb0df8", "t": "mcq", "d": "infer", "q": "“An animal cannot read a sign saying ‘Keep away’.” What does the writer mean?",
             "opts": ["Animals cannot keep themselves safe from litter, so people must",
                      "The park needs more signs that animals can understand",
                      "Animals should be kept out of the park altogether",
                      "Litter is only dangerous for the people in the park"],
             "why": "She has just said litter traps and harms animals; they cannot know the danger, so she says it "
                    "is up to us to keep them safe."},
            {"id": "aacffb0ffc48", "t": "mcq", "d": "vocab", "q": "“Plastic does not rot away like fallen leaves do.” What does “rot away” mean?",
             "opts": ["slowly break down until it is gone", "blow away in the wind",
                      "float away on the water", "fade in the sunshine"],
             "why": "Fallen leaves slowly break down into the soil; plastic does not, so it stays for many years."},
            {"id": "23a770698ef8", "t": "mcq", "d": "structure", "q": "Why does the writer begin one paragraph with “Some people say that picking up litter is the council's job”?",
             "opts": ["to answer an argument against her own view", "to agree that children should not pick up litter",
                      "to explain how often the bins are emptied", "to tell a story about the park keepers"],
             "why": "She gives what someone might say against her, then uses “However” to show why it does not stop "
                    "us helping."},
            {"id": "7ca5779c7aed", "t": "tap", "d": "retrieve", "q": "Tap the two words that tell you what time the litter pick starts.",
             "s": "So come and join Class 4 for our big litter pick this Saturday at [ten] [o'clock].",
             "why": "The litter pick starts at ten o'clock on Saturday."},
            {"id": "7a1c357afbe4", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to persuade readers to keep the park free of litter", "to explain how park keepers do their job",
                      "to describe the wildlife that lives in the park", "to tell the story of a day in the park"],
             "why": "Priya gives reasons, answers an argument against her and asks everyone to join the litter pick: "
                    "she wants to persuade."},
        ],
    },
    {
        "key": "RD4.26",
        "year": 4,
        "strand": "Stories",
        "title": "Grandmother's trees",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Wanjiru's grandmother lived on a small farm in the hills of Kenya, where the red earth turned to dust "
            "in the dry season. Behind her house was a bare slope, and every year the rain washed a little more of "
            "its soil away.\n\n"
            "“When I was a girl,” said Grandmother, “that hill was covered in trees. Their roots held the soil "
            "together. Now look at it.”\n\n"
            "The next morning, she gave Wanjiru and her cousin Kamau ten tiny seedlings in plastic pots. “We are "
            "going to bring the trees back,” she said.\n\n"
            "The children dug ten holes in a neat row, planted the seedlings and pressed the soil down firmly "
            "around each one. Every evening, they carried water up from the stream in yellow cans. The cans were "
            "heavy, and the path was steep. By the end of the first week, Kamau was grumbling.\n\n"
            "“They're not even growing,” he said, kicking a stone. “This is a waste of time.”\n\n"
            "Grandmother laughed. “Trees are never in a hurry,” she said. “But they remember who looks after "
            "them.”\n\n"
            "In the second week, a goat got loose and ate three of the seedlings right down to their stalks. "
            "Wanjiru wanted to cry. Instead, she and Kamau built a little fence of thorny branches around each of "
            "the trees that were left.\n\n"
            "When the rains came at last, the seedlings shot up. By the time the children went home at the end "
            "of the holidays, the smallest one reached Wanjiru's knee, and Kamau was counting the new leaves "
            "every morning.\n\n"
            "Two years later, Wanjiru stood in the shade of a tree taller than herself. Beside it, Kamau was "
            "planting the next row."
        ),
        "qs": [
            {"id": "2160dedf7bc2", "t": "mcq", "d": "infer", "q": "Why did Grandmother want to plant trees on the bare slope?",
             "opts": ["so the rain would stop washing the soil away", "so she could sell the wood",
                      "so the goats would have food to eat", "so the farm would have a fence"],
             "why": "She says the trees' roots used to hold the soil together; since they went, the rain has been "
                    "washing it away."},
            {"id": "10fdf9db3a3e", "t": "text", "d": "retrieve", "q": "Find and copy the word that names what the children carried water in.",
             "a": ["cans", "yellow cans", "can", "the cans", "the yellow cans"],
             "why": "The fourth paragraph says they carried water up from the stream in yellow cans."},
            {"id": "707da285b517", "t": "mcq", "d": "infer", "q": "How was Kamau feeling by the end of the first week?",
             "opts": ["fed up and impatient", "proud and excited", "frightened and worried", "calm and happy"],
             "why": "He was grumbling, kicking a stone and saying it was a waste of time: he was tired of waiting "
                    "for the seedlings to grow."},
            {"id": "42b9c6cc0c86", "t": "mcq", "d": "language", "q": "Grandmother says, “Trees are never in a hurry.” What does she mean?",
             "opts": ["Trees take a long time to grow", "Trees should be planted quickly",
                      "Trees grow best in the dry season", "Trees need very little water"],
             "why": "She is answering Kamau's complaint that the seedlings are not growing: she means growing takes time."},
            {"id": "74de182e3bce", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["The children plant ten seedlings", "Kamau says it is a waste of time",
                       "A goat eats three of the seedlings", "The rains come and the seedlings shoot up",
                       "Kamau plants the next row"],
             "why": "The story follows the trees from planting, through the first and second weeks and the rains, to "
                    "two years later."},
            {"id": "af17758be54e", "t": "mcq", "d": "infer", "q": "How has Kamau changed by the end of the story?",
             "opts": ["He has gone from grumbling to caring about the trees", "He has become afraid of the goats",
                      "He has stopped helping his grandmother", "He has decided trees are a waste of time"],
             "why": "At first he called it a waste of time; later he counts the new leaves every morning and plants "
                    "a new row himself.",
             "no": {"He has decided trees are a waste of time": "He said that in the first week, but by the end he "
                                                                "is planting more trees."}},
        ],
    },
    {
        "key": "RD4.27",
        "year": 4,
        "strand": "Information",
        "title": "Bats: hunting with sound",
        "nc": "Retrieve and record information from non-fiction; explain and discuss their understanding of what they have read",
        "text": (
            "As the sun sets on a summer evening, you might see a small, dark shape flitting over a garden or along "
            "a river. It moves too quickly and too unevenly to be a bird. It is probably a bat.\n\n"
            "Bats are the only mammals that can truly fly. Like other mammals, they have fur and feed their young "
            "on milk. Their wings are made of thin, stretchy skin, spread between very long finger bones. More than "
            "a dozen kinds of bat live in Britain. The smallest, the pipistrelle, is lighter than a pound coin.\n\n"
            "British bats eat insects, such as moths, beetles and midges. A single pipistrelle can catch hundreds "
            "of tiny insects in one night. But how do bats find such small prey in the dark?\n\n"
            "The answer is sound. As it flies, a bat gives out a stream of very high-pitched calls, most of them "
            "too high for humans to hear. When a call hits an object, such as a tree or a moth, it bounces back as "
            "an echo. By listening to the echoes, the bat can work out where things are, how big they are and even "
            "which way they are moving. This is called echolocation.\n\n"
            "Bats are not blind, though. They can see, but in the dark their ears tell them far more than their "
            "eyes do.\n\n"
            "In winter, when there are few insects about, British bats hibernate. They find a cool, quiet place, "
            "such as a cave, an old building or a hollow tree, and their bodies slow right down until spring.\n\n"
            "All bats in Britain are protected by law, so it is against the law to harm them or disturb the "
            "places where they rest."
        ),
        "qs": [
            {"id": "61054a27d808", "t": "mcq", "d": "vocab", "q": "“A small, dark shape flitting over a garden.” What does “flitting” mean?",
             "opts": ["moving quickly and lightly", "hanging upside down", "gliding slowly in circles",
                      "calling out loudly"],
             "why": "The next sentence says it moves too quickly and unevenly to be a bird: flitting is darting about lightly."},
            {"id": "7f63166797ad", "t": "mcq", "d": "retrieve", "q": "What are a bat's wings made of?",
             "opts": ["thin, stretchy skin between long finger bones", "feathers on long arm bones",
                      "fur stretched over a hard shell", "thick skin between its legs and tail"],
             "why": "The second paragraph says the wings are thin, stretchy skin spread between very long finger bones."},
            {"id": "7abcd924c332", "t": "tap", "d": "retrieve", "q": "Tap the word that names the smallest kind of bat in Britain.",
             "s": "The smallest, the [pipistrelle], is lighter than a pound coin.",
             "why": "The text says the smallest is the pipistrelle, which is lighter than a pound coin."},
            {"id": "53df75f4e69f", "t": "order", "d": "sequence", "q": "Put these steps of echolocation in order.",
             "items": ["The bat gives out a high-pitched call", "The call hits an object",
                       "An echo bounces back to the bat", "The bat works out where the object is"],
             "why": "The fourth paragraph explains it: call, hit, echo, then the bat uses the echo to find the object."},
            {"id": "61251e0355f2", "t": "mcq", "d": "infer", "q": "Why do British bats hibernate in winter?",
             "opts": ["There are not enough insects for them to eat", "They cannot see on dark winter nights",
                      "Their calls do not work in cold air", "They are protected by law in winter"],
             "why": "Bats eat insects, and the text says there are few insects about in winter, so resting until spring "
                    "saves them from going hungry."},
            {"id": "32fbe1f155c4", "t": "mcq", "d": "compare", "q": "According to the text, how do a bat's eyes and ears compare in the dark?",
             "opts": ["Its ears tell it far more than its eyes", "Its eyes tell it far more than its ears",
                      "Its eyes do not work at all", "Its eyes and ears are equally useful"],
             "why": "The fifth paragraph says bats can see, but in the dark their ears tell them far more than their eyes do.",
             "no": {"Its eyes do not work at all": "The text says bats are not blind: they can see."}},
        ],
    },
    {
        "key": "RD4.28",
        "year": 4,
        "strand": "Stories",
        "title": "The power cut",
        "nc": "Draw inferences such as inferring characters' feelings; identify main ideas and summarise",
        "text": (
            "The storm had been growling over Cardiff all afternoon. Just as Seren sat down to finish her game on "
            "the tablet, the lights flickered once, twice, and went out. The fridge stopped humming. The "
            "television went dark. Outside, the whole street was black.\n\n"
            "“Power cut,” said Mam calmly. “Nobody open the freezer.”\n\n"
            "Seren's little brother, Gethin, grabbed her arm. “I don't like it,” he whispered.\n\n"
            "Dad found the torch in the kitchen drawer and three candles in a box under the sink. Soon the living "
            "room was full of soft, wobbling light and long shadows that stretched up the walls.\n\n"
            "“My tablet's nearly flat,” Seren groaned. “What are we supposed to do now?”\n\n"
            "“When I was your age,” said Mam, “we had power cuts all the time. We used to make shadow puppets.” "
            "She held her hands in front of the torch, hooked her thumbs together and fluttered her fingers. A "
            "bird flew across the ceiling.\n\n"
            "Gethin forgot to be frightened. Before long he was making a dog that barked (Dad did the barking), "
            "and Seren had worked out how to make a rabbit with floppy ears. Then Dad told them about the day he "
            "got lost on a school trip to the seaside, and they laughed so much that Gethin got hiccups.\n\n"
            "At half past nine, the lights snapped back on. The fridge started humming again, and the television "
            "blared into life.\n\n"
            "Everyone blinked. For a moment, nobody moved.\n\n"
            "“Can we turn it all off again?” asked Gethin.\n\n"
            "Seren was surprised to find that she had been thinking exactly the same thing."
        ),
        "qs": [
            {"id": "fc18096ab185", "t": "mcq", "d": "language", "q": "Why does the writer say the storm had been “growling”?",
             "opts": ["to make the thunder sound like an angry animal", "to show the storm was very quiet",
                      "to show the storm had only just started", "to make the storm sound friendly"],
             "why": "Growling is the low, angry sound an animal makes: it makes the storm's rumbling sound fierce.",
             "no": {"to show the storm had only just started": "It had been growling “all afternoon”."}},
            {"id": "6b03113f1e9a", "t": "mcq", "d": "infer", "q": "Why did Mam tell everyone not to open the freezer?",
             "opts": ["to keep the cold in while the power was off", "because the freezer was already empty",
                      "because Gethin wanted an ice lolly", "because the freezer door was broken"],
             "why": "With no electricity the freezer cannot make cold, so opening it would let the cold out and the "
                    "food could start to melt."},
            {"id": "a090a4e20a1f", "t": "mcq", "d": "retrieve", "q": "Where did Dad find the candles?",
             "opts": ["in a box under the sink", "in the kitchen drawer", "on a shelf in the living room",
                      "next to the fridge"],
             "why": "The torch was in the kitchen drawer; the three candles were in a box under the sink.",
             "no": {"in the kitchen drawer": "That is where Dad found the torch, not the candles."}},
            {"id": "6fb87482902f", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how Gethin had felt in the dark before the puppets.",
             "s": "Gethin forgot to be [frightened].",
             "why": "He forgot to be frightened once the shadow puppets began; earlier he grabbed Seren's arm and "
                    "whispered that he did not like it."},
            {"id": "f67c2669c1d3", "t": "mcq", "d": "vocab", "q": "“The television blared into life.” What does “blared” mean?",
             "opts": ["made a sudden loud noise", "slowly went quiet", "flickered softly", "broke down"],
             "why": "When the power came back the television came on suddenly and loudly, after the quiet evening."},
            {"id": "c8a74cb4c089", "t": "mcq", "d": "infer", "q": "How do Seren's feelings change during the story?",
             "opts": ["She goes from fed up to enjoying the evening", "She goes from happy to bored",
                      "She goes from frightened to angry", "She stays cross the whole time"],
             "why": "She groans about her tablet at first, but by the end she, like Gethin, wishes the lights were "
                    "off again.",
             "no": {"She goes from frightened to angry": "It was Gethin who was frightened; Seren was fed up "
                                                        "about her tablet."}},
        ],
    },
]
