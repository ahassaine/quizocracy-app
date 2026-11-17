"""Reading comprehension, Year 4 (keys RD4.xx).

Fourteen original passages, written by hand (SPEC_READING.md), 200-300 words each, six questions each,
mixing the KS2 reading domains (retrieve, infer, vocab, sequence, summarise, structure, language,
compare, predict, purpose). Topics link to the Year 4 curriculum where natural (the Romans in Britain,
the water cycle and states of water, electrical circuits, teeth and digestion, food chains,
classifying animals, sound, rainforests, mountains) alongside realistic stories, a poem, a play script,
instructions and a news report:

* RD4.01 The Romans in Britain (information)
* RD4.02 The kingfisher (story: a school trip)
* RD4.03 The water cycle (explanation)
* RD4.04 The relay (story: sports day)
* RD4.05 Make a circuit with a switch (instructions)
* RD4.06 Teeth and the journey of food (information)
* RD4.07 The red kite (play script: sharing)
* RD4.08 Food chains (information)
* RD4.09 Words in two languages (story: a grandparent's visit)
* RD4.10 Sorting animals into groups (information)
* RD4.11 Listening from the hill (poem: sound)
* RD4.12 Rainforests (information)
* RD4.13 Pupils climb the highest mountain in Wales (news report)
* RD4.14 One full length (story: a challenge overcome)

The people, schools and events in the stories, play and news report are invented. May be reviewed by
any teacher or parent reviewer of the bank.
"""

SKILLS = [
    {
        "key": "RD4.01",
        "year": 4,
        "strand": "Information",
        "title": "The Romans in Britain",
        "nc": "Retrieve and record information from non-fiction",
        "text": (
            "In AD 43, nearly two thousand years ago, a large Roman army crossed the sea and landed in Kent, in "
            "the south-east of Britain. The Romans already ruled lands all around the Mediterranean Sea, and their emperor, "
            "Claudius, wanted Britain too. Some British tribes made peace with the newcomers, but others fought hard "
            "to stay free. One of the best-known British leaders was Boudica, queen of the Iceni tribe, who led a "
            "great revolt against the Romans. In the end, though, the Roman army was too well trained and too well "
            "organised to be beaten.\n\n"
            "The Romans changed Britain in many ways. They built long, straight roads so that soldiers and traders "
            "could travel quickly from one town to another, and some modern roads still follow the same routes today. "
            "They built towns with markets, shops and public baths, where people went to wash, relax and meet their "
            "friends. Londinium, the town that grew into London, became one of the most important.\n\n"
            "The Romans never fully conquered the lands in the far north that are now Scotland. Emperor Hadrian ordered a "
            "wall to be built from coast to coast to guard the edge of Roman Britain. Hadrian's Wall was about "
            "73 miles long, with small forts along it where soldiers lived and kept watch. Long stretches of it can "
            "still be seen today.\n\n"
            "The Romans also brought a new language, Latin, which later gave English many of its words. They used "
            "coins with the emperor's head on them, and they built with stone, brick and a kind of concrete.\n\n"
            "In about AD 410, after nearly four hundred years, the last Roman soldiers left Britain to defend other "
            "parts of their empire. But many of the things they built, and many of their words, stayed behind."
        ),
        "qs": [
            {"id": "0e9f075f3c23", "t": "mcq", "d": "retrieve", "q": "In which year did the Roman army land in Britain, according to the text?",
             "opts": ["AD 43", "AD 410", "AD 73", "AD 400"],
             "why": "The first sentence says the army landed in AD 43. AD 410 is when the last soldiers left."},
            {"id": "c0b209824aaa", "t": "mcq", "d": "vocab", "q": "Boudica “led a great revolt against the Romans”. What is a revolt?",
             "opts": ["a fight against the people in charge", "a long journey across the sea",
                      "a peace agreement between tribes", "a meeting to choose a new queen"],
             "why": "Some tribes fought to stay free; Boudica led a fight against the Romans, who wanted to rule them."},
            {"id": "70996a1c32a9", "t": "text", "d": "retrieve", "q": "Find and copy the name of the Roman town that grew into London.",
             "a": ["Londinium"],
             "why": "The second paragraph says Londinium was the town that grew into London."},
            {"id": "15685ec239f9", "t": "mcq", "d": "infer", "q": "What does the text suggest about the things the Romans built?",
             "opts": ["They were made to last a very long time", "They were finished quickly and soon fell down",
                      "They were built mostly by the British tribes", "They were only found in the far north"],
             "why": "Some roads still follow Roman routes and long stretches of Hadrian's Wall can still be seen: "
                    "both show Roman building lasted."},
            {"id": "2a9eb2cc2db9", "t": "tap", "d": "retrieve", "q": "Tap the word that names the language the Romans brought.",
             "s": "The Romans also brought a new language, [Latin], which later gave English many of its words.",
             "why": "The fourth paragraph says the Romans brought Latin."},
            {"id": "a637c90ea331", "t": "mcq", "d": "summarise", "q": "What is the whole text mainly about?",
             "opts": ["how the Romans came to Britain and changed it", "why Boudica was a famous queen",
                      "how Hadrian's Wall was built", "why the Romans left Britain in AD 410"],
             "why": "Each paragraph tells part of one story: the Romans arriving, what they built and brought, and "
                    "what stayed when they left.",
             "no": {"how Hadrian's Wall was built": "The wall is only one paragraph of the text."}},
        ],
    },
    {
        "key": "RD4.02",
        "year": 4,
        "strand": "Stories",
        "title": "The kingfisher",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Class 4 had been looking forward to the trip to Marsh End Nature Reserve for weeks. Jaya had a list in "
            "her pocket of every bird she hoped to see, and right at the top, underlined twice, was the kingfisher.\n\n"
            "When the coach pulled into the car park, the warden, a tall woman called Mrs Hughes, was waiting with a "
            "box of binoculars. “The birds here are wild,” she explained. “If you want to see them, you will need to "
            "be patient and very, very quiet.”\n\n"
            "The class followed a wooden boardwalk over the reeds to a hide, a long wooden hut with narrow windows "
            "looking out over the water. Inside, everyone sat on benches and peered out. Within minutes they had "
            "spotted ducks, a heron standing as still as a statue, and a pair of swans gliding past.\n\n"
            "Jaya kept her binoculars fixed on a branch that hung low over the stream. Mrs Hughes had told her that "
            "kingfishers liked to perch there and watch for fish. Ten minutes passed. Then twenty. Ben, who was "
            "sitting next to her, began to fidget and drum his feet on the floor.\n\n"
            "“It's not coming,” he whispered. “Let's go and do the pond-dipping instead.”\n\n"
            "Jaya shook her head. She wanted to give it just a little longer.\n\n"
            "Mr Okafor was calling the class to leave when a flash of bright blue and orange shot across the water "
            "and landed on the branch. Jaya gasped. The kingfisher sat for a moment, then dived, and came up with a "
            "tiny silver fish in its beak.\n\n"
            "On the coach home, Ben asked if he could borrow Jaya's list. “Next time,” he said, “I'm going to wait "
            "too.”"
        ),
        "qs": [
            {"id": "8f7404522769", "t": "mcq", "d": "retrieve", "q": "Which bird was at the top of Jaya's list?",
             "opts": ["the kingfisher", "the heron", "the swan", "the duck"],
             "why": "The first paragraph says the kingfisher was at the top of the list, underlined twice."},
            {"id": "f2b5defbf77f", "t": "mcq", "d": "vocab", "q": "In the third paragraph, what is a “hide”?",
             "opts": ["a hut with windows for watching birds", "a path of wooden boards over the reeds",
                      "a bench where the class ate lunch", "a box for keeping binoculars in"],
             "why": "The text explains it: a long wooden hut with narrow windows looking out over the water.",
             "no": {"a path of wooden boards over the reeds": "That is the boardwalk, which led to the hide."}},
            {"id": "ddab7722a580", "t": "tap", "d": "language", "q": "Tap the word the writer compares the heron to.",
             "s": "Within minutes they had spotted ducks, a heron standing as still as a [statue], and a pair of swans gliding past.",
             "why": "“As still as a statue” compares the heron to a statue, to show it did not move at all."},
            {"id": "bda47dbd5a82", "t": "mcq", "d": "infer", "q": "How was Ben feeling after twenty minutes in the hide?",
             "opts": ["bored and impatient", "frightened of the heron", "proud of the birds he had seen",
                      "cross with Jaya for talking"],
             "why": "He fidgeted, drummed his feet and wanted to go pond-dipping instead: he was tired of waiting."},
            {"id": "d98a5abb4d92", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Mrs Hughes tells the class to be quiet", "The class spots a heron and two swans",
                       "Ben wants to go pond-dipping", "The kingfisher lands on the branch",
                       "Ben asks to borrow Jaya's list"],
             "why": "The warden speaks in the car park, the class sees birds from the hide, Ben gets restless, the "
                    "kingfisher arrives, then Ben speaks on the coach home."},
            {"id": "6d3212dab365", "t": "mcq", "d": "infer", "q": "What lesson does Ben learn by the end of the story?",
             "opts": ["Waiting patiently can be worth it", "Kingfishers only eat silver fish",
                      "Pond-dipping is more fun than birdwatching", "It is best to leave a trip early"],
             "why": "Ben gave up waiting, but Jaya waited and saw the kingfisher. Now Ben says he will wait too."},
        ],
    },
    {
        "key": "RD4.03",
        "year": 4,
        "strand": "Explanations",
        "title": "The water cycle",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": (
            "The water you drink today may once have fallen as rain on a mountain, flowed down a river or been part "
            "of an ocean far away. That is because the water on Earth is used again and again, on a never-ending "
            "journey called the water cycle.\n\n"
            "Water can be a solid, a liquid or a gas. Ice is solid water, the water in a puddle is liquid, and water "
            "vapour is a gas, which is invisible. Water changes from one state to another when it is heated or "
            "cooled.\n\n"
            "The cycle begins when the Sun warms the water in seas, lakes and rivers. Some of the liquid water turns "
            "into water vapour and rises into the air. This change is called evaporation. The warmer it is, the "
            "faster water evaporates, which is why puddles dry up more quickly on a hot day.\n\n"
            "As the water vapour rises, it cools. High in the sky, the cooled vapour turns back into tiny drops of "
            "liquid water. This is called condensation. Billions of these drops gather together to make clouds. You "
            "can see condensation at home, too, when drops of water appear on a cold window.\n\n"
            "When the drops in a cloud join up and grow too heavy to stay in the air, they fall back to the ground. "
            "This is called precipitation. It may be rain or, if the air is cold enough, snow or hail.\n\n"
            "Some of the fallen water soaks into the ground, and some runs off into streams and rivers, which carry it "
            "back to the sea. There the Sun warms it once more, and the cycle starts again."
        ),
        "qs": [
            {"id": "911b5e193b4f", "t": "tap", "d": "vocab", "q": "Tap the word that means “cannot be seen”.",
             "s": "Ice is solid water, the water in a puddle is liquid, and water vapour is a gas, which is [invisible].",
             "why": "Invisible means cannot be seen: you cannot see water vapour in the air."},
            {"id": "787397a0a5b5", "t": "mcq", "d": "infer", "q": "Kofi hangs his wet football kit on the washing line. Using the text, on which day would it dry fastest?",
             "opts": ["a hot, sunny day", "a cold, cloudy day", "a freezing winter morning", "a cool, misty evening"],
             "why": "Drying is water evaporating, and the third paragraph says the warmer it is, the faster water evaporates."},
            {"id": "3a9364b8aed3", "t": "mcq", "d": "retrieve", "q": "Which example of condensation at home does the text give?",
             "opts": ["drops of water on a cold window", "a puddle drying up on a hot day",
                      "ice melting in a glass of juice", "snow falling in the garden"],
             "why": "The fourth paragraph says you can see condensation when drops of water appear on a cold window.",
             "no": {"a puddle drying up on a hot day": "That is evaporation: liquid water turning into a gas."}},
            {"id": "80055ce993a5", "t": "text", "d": "vocab", "q": "Find and copy the word the text uses for water falling from clouds as rain, snow or hail.",
             "a": ["precipitation"],
             "why": "The fifth paragraph says falling rain, snow or hail is called precipitation."},
            {"id": "2b04fc44e934", "t": "order", "d": "sequence", "q": "Put these stages in the order the text explains them.",
             "items": ["The Sun warms water in the sea", "Water vapour rises and cools",
                       "Tiny drops gather to make clouds", "Heavy drops fall as rain",
                       "Rivers carry the water back to the sea"],
             "why": "Evaporation comes first, then condensation, then precipitation, then the water flows back to the sea."},
            {"id": "a8296a01f632", "t": "mcq", "d": "structure", "q": "Why does the writer begin by saying your drinking water may once have been part of an ocean?",
             "opts": ["To show that the same water goes round and round", "To warn readers not to drink sea water",
                      "To explain how oceans were first made", "To show that rain only falls on mountains"],
             "why": "The opening leads straight into the main idea: the water on Earth is used again and again."},
        ],
    },
    {
        "key": "RD4.04",
        "year": 4,
        "strand": "Stories",
        "title": "The relay",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "The field behind Hilltop Primary was dotted with flags and white painted lines, and the sun was already "
            "warm by ten o'clock. It was sports day, and the last race of the morning was the Year 4 relay.\n\n"
            "Rosa was running the final leg for the Green team. She had practised taking the baton from Daniel every "
            "lunchtime for two weeks. “Hand forward, eyes on the baton,” their teacher, Miss Patel, kept reminding "
            "them.\n\n"
            "The whistle blew. Priya set off first and handed over cleanly to Tom, who sprinted down the back "
            "straight and gave the Greens a clear lead. Then it was Daniel's turn. He ran well, but as he reached out "
            "to Rosa, the baton slipped from his fingers and bounced on the grass.\n\n"
            "Daniel's face went pale. By the time he had snatched it up and pressed it into Rosa's hand, the Red and "
            "Blue runners were several metres ahead.\n\n"
            "Rosa did not waste a second looking back. She pumped her arms and fixed her eyes on the finish line. Her "
            "legs burned. Slowly, step by step, she caught the Blue runner, then drew level with him, then passed him. "
            "The Red runner crossed the line first, but Rosa was only a stride behind.\n\n"
            "Second place. Daniel walked over with his head down. “Sorry,” he mumbled. “We would have won if I "
            "hadn't dropped it.”\n\n"
            "Rosa was still out of breath, but she grinned at him. “We'd never have come second if you hadn't run so "
            "well,” she said. “Anyway, it's a team race. We finished it together.”\n\n"
            "Later, when the Greens collected their silver stickers, Daniel stood at the front and clapped loudest of "
            "all."
        ),
        "qs": [
            {"id": "c44a293bd170", "t": "mcq", "d": "retrieve", "q": "Which part of the relay did Rosa run?",
             "opts": ["the last leg", "the first leg", "the second leg", "the third leg"],
             "why": "The second paragraph says Rosa was running the final leg for the Green team."},
            {"id": "cd774f44ed8e", "t": "text", "d": "retrieve", "q": "Which runner gave the Greens a clear lead? Type his name.",
             "a": ["Tom"],
             "why": "The third paragraph says Tom sprinted down the back straight and gave the Greens a clear lead."},
            {"id": "62bb3a7cd153", "t": "mcq", "d": "infer", "q": "Why did Daniel's face go pale?",
             "opts": ["He was worried he had let his team down", "He was feeling ill in the hot sun",
                      "He had hurt his fingers on the baton", "He was afraid of the Red runner"],
             "why": "He had just dropped the baton, and later he says sorry because he thinks they lost the race "
                    "because of him."},
            {"id": "eda13c565bbf", "t": "tap", "d": "vocab", "q": "Tap the word that tells you Daniel spoke quietly and not very clearly.",
             "s": "“Sorry,” he [mumbled].",
             "why": "To mumble is to speak quietly without opening your mouth much, so the words are hard to hear."},
            {"id": "6af2b75a541f", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Priya hands the baton to Tom", "Daniel drops the baton", "Rosa passes the Blue runner",
                       "The Red runner wins the race", "The Greens collect their stickers"],
             "why": "Follow the race from the first leg to the finish, then the stickers come later."},
            {"id": "ef444454195f", "t": "mcq", "d": "infer", "q": "What does the story show about Rosa?",
             "opts": ["She is kind and thinks about the whole team", "She only cares about winning races",
                      "She is angry when others make mistakes", "She likes to boast about how fast she is"],
             "why": "Instead of blaming Daniel, she praises his running and says they finished the race together.",
             "no": {"She only cares about winning races": "She grins at Daniel after coming second and says it is a team race."}},
        ],
    },
    {
        "key": "RD4.05",
        "year": 4,
        "strand": "Instructions",
        "title": "Make a circuit with a switch",
        "nc": "Retrieve and record information from non-fiction; discuss how structure and presentation contribute to meaning",
        "text": (
            "An electrical circuit is a complete loop that electricity can flow around. In this activity you will "
            "build a circuit that lights a bulb, and then add a switch so that you can turn the bulb on and off.\n\n"
            "You will need: a battery in a battery holder, a small bulb in a bulb holder, a switch and three wires "
            "with a crocodile clip at each end.\n\n"
            "1. Clip one end of the first wire to one end of the battery holder.\n"
            "2. Clip the other end of that wire to one side of the bulb holder.\n"
            "3. Take the second wire and clip it to the other side of the bulb holder.\n"
            "4. Clip the free end of the second wire to the other end of the battery holder.\n"
            "5. Look at the bulb. If every clip is tight, it should now light up, because the circuit is complete.\n"
            "6. Unclip the second wire from the battery holder. The bulb goes out, because there is now a gap in the "
            "circuit.\n"
            "7. Clip the free end of the second wire to the switch. Then use the third wire to join the other side "
            "of the switch to the battery holder.\n"
            "8. Press the switch to close it, and the bulb lights. Press it again to open it, and the bulb goes "
            "out.\n\n"
            "If the bulb does not light, check that every clip is gripping firmly and that the bulb is screwed "
            "tightly into its holder. A loose connection leaves a gap, and electricity cannot flow across it. You "
            "could also try a new battery.\n\n"
            "Only ever use batteries for experiments like this. Never play with plugs or sockets at home: mains "
            "electricity is far more powerful and can be very dangerous."
        ),
        "qs": [
            {"id": "0234ad095d46", "t": "mcq", "d": "retrieve", "q": "How many wires do you need for the whole activity?",
             "opts": ["three", "two", "four", "one"],
             "why": "The “You will need” list asks for three wires: two for the first circuit and one more for the switch."},
            {"id": "1a901c427fcc", "t": "text", "d": "retrieve", "q": "Find and copy the word that tells you what kind of clip is at each end of the wires.",
             "a": ["crocodile", "crocodile clip", "crocodile clips", "a crocodile clip", "the crocodile clips", "the crocodile clip"],
             "why": "The list says each wire has a crocodile clip at each end."},
            {"id": "1af909c0c9ce", "t": "mcq", "d": "structure", "q": "Why are steps 1 to 8 written as a numbered list?",
             "opts": ["So you do each job in the right order", "So you can count how many wires you need",
                      "To show which step is the most important", "To make the activity take less time"],
             "why": "Numbered steps show the order to work in: each step builds on the one before."},
            {"id": "37862bf91769", "t": "mcq", "d": "vocab", "q": "In step 8, what does it mean to “close” the switch?",
             "opts": ["to press it so there is no gap in the circuit", "to put a lid on top of the switch",
                      "to make a gap so the bulb goes out", "to take the switch out of the circuit"],
             "why": "When the switch is closed the bulb lights, so the loop must be complete with no gap.",
             "no": {"to make a gap so the bulb goes out": "That is opening the switch: step 8 says the bulb goes out when it is open."}},
            {"id": "5af8afeedd9f", "t": "mcq", "d": "infer", "q": "Sam's bulb stays dark. He sees that one crocodile clip has come off the battery holder. Why does the bulb not light?",
             "opts": ["There is a gap in the circuit", "The wires are too long", "The switch has been closed",
                      "The bulb is too small for the holder"],
             "why": "A clip that has come off leaves a gap, and the text says electricity cannot flow across a gap."},
            {"id": "9273f0039807", "t": "mcq", "d": "purpose", "q": "Why does the writer add the last paragraph?",
             "opts": ["To warn readers to keep away from mains electricity", "To explain how a battery is made",
                      "To tell readers where to buy a switch", "To show the activity has finished"],
             "why": "It tells readers to use only batteries and never play with plugs or sockets, because mains "
                    "electricity is dangerous."},
        ],
    },
    {
        "key": "RD4.06",
        "year": 4,
        "strand": "Information",
        "title": "Teeth and the journey of food",
        "nc": "Retrieve and record information from non-fiction",
        "text": (
            "Every time you eat a meal, your body sets to work breaking the food down into tiny pieces that it can "
            "use for energy and growth. This is called digestion, and it starts the moment food enters your mouth.\n\n"
            "Your teeth do the first job. They are not all the same shape, because each kind has a different task. "
            "The incisors at the front are flat and sharp, like little chisels, for biting and cutting. Next to them "
            "are the canines, which are pointed and good for gripping and tearing. Further back are the premolars "
            "and molars, which are wide and bumpy, for crushing and grinding food. As you chew, saliva makes the food "
            "soft and wet so that it is easy to swallow.\n\n"
            "When you swallow, the food travels down a tube called the oesophagus to your stomach. The stomach is a "
            "stretchy bag with strong muscular walls. It squeezes and churns the food and mixes it with juices that "
            "break it down further.\n\n"
            "Next, the food moves into the small intestine, a long, coiled tube. Here, the useful parts of the food "
            "pass into the blood, which carries them all around the body. What is left moves on to the large "
            "intestine, where water is taken out of it. The waste finally leaves the body when you go to the "
            "toilet.\n\n"
            "Because your teeth have such an important job, it is worth looking after them. Brush them twice a day, "
            "cut down on sugary food and drinks, and visit the dentist regularly. You only get one set of adult "
            "teeth, and they have to last you the rest of your life."
        ),
        "qs": [
            {"id": "f5258d6177a9", "t": "mcq", "d": "infer", "q": "Using the text, which teeth would do most of the work of grinding a mouthful of nuts into small pieces?",
             "opts": ["premolars and molars", "incisors", "canines", "incisors and canines"],
             "why": "The second paragraph says the wide, bumpy premolars and molars at the back are for crushing and grinding.",
             "no": {"incisors": "Incisors are for biting and cutting, not grinding.",
                    "incisors and canines": "These are for biting, cutting, gripping and tearing, not grinding.",
                    "canines": "Canines are for gripping and tearing, not grinding."}},
            {"id": "8cc6733645db", "t": "mcq", "d": "language", "q": "The writer says incisors are “like little chisels”. What does this comparison show?",
             "opts": ["They have a sharp edge for cutting", "They are made of hard metal",
                      "They are the biggest teeth in the mouth", "They are used for grinding food"],
             "why": "A chisel is a tool with a flat, sharp edge for cutting, just like an incisor.",
             "no": {"They are used for grinding food": "Grinding is the job of the wide, bumpy premolars and molars."}},
            {"id": "f8646170966a", "t": "text", "d": "retrieve", "q": "Find and copy the name of the tube that carries food from your mouth to your stomach.",
             "a": ["oesophagus", "the oesophagus"],
             "why": "The third paragraph says food travels down a tube called the oesophagus."},
            {"id": "9e36d9175662", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the small intestine is wound round and round.",
             "s": "Next, the food moves into the small intestine, a long, [coiled] tube.",
             "why": "Coiled means wound round in loops, like a rope or a hose that has been put away."},
            {"id": "8bcaf0fa8225", "t": "order", "d": "sequence", "q": "Put these in the order they happen to food.",
             "items": ["Teeth and saliva break up and soften the food", "The food travels down the oesophagus",
                       "The stomach churns the food with juices", "Useful parts pass into the blood",
                       "Water is taken out in the large intestine"],
             "why": "Food goes from the mouth down the oesophagus to the stomach, then the small intestine, then the "
                    "large intestine."},
            {"id": "bbba503e1882", "t": "mcq", "d": "purpose", "q": "Why does the writer end with advice about brushing and the dentist?",
             "opts": ["To show that teeth do an important job and need care", "To explain how saliva is made",
                      "To show that the stomach can be damaged by sugar", "To describe the shapes of different teeth"],
             "why": "The last paragraph begins “Because your teeth have such an important job”: the advice follows "
                    "from what teeth do."},
        ],
    },
    {
        "key": "RD4.07",
        "year": 4,
        "strand": "Play scripts",
        "title": "The red kite",
        "nc": "Prepare play scripts to read aloud and perform; draw inferences about characters' feelings",
        "text": (
            "(A windy beach in Northumberland. LEILA holds a new red kite. Her younger brother, OMAR, runs up beside "
            "her. MUM sits on a blanket nearby.)\n"
            "OMAR: Can I have a go? Please? Just one go!\n"
            "LEILA: Not yet. It's my kite. Auntie Samira gave it to me for my birthday.\n"
            "OMAR: But you've had it for a whole week, and I haven't even touched it.\n"
            "LEILA: That's because you'd break it. You broke my last one.\n"
            "OMAR: That was ages ago. I was only little then.\n"
            "MUM: Leila, why don't you show him how it works?\n"
            "LEILA: (sighing) Fine. But watch, don't touch. (She holds the kite above her head and runs. The kite "
            "lifts, wobbles and crashes onto the sand.)\n"
            "OMAR: (trying not to laugh) Maybe it's broken already.\n"
            "LEILA: It's not broken! The wind keeps dropping. (She tries again. The kite flips over and lands at "
            "her feet.)\n"
            "MUM: When I was your age, we always launched kites with two people. One person holds the kite up high, "
            "and the other holds the string and runs.\n"
            "LEILA: (looking at Omar) Two people?\n"
            "OMAR: I could hold it! I'd hold it really carefully, I promise.\n"
            "LEILA: (after a pause) All right. Hold it by the edges, not the middle. When I shout “now”, let go.\n"
            "(Omar lifts the kite. Leila walks backwards until the string is tight.)\n"
            "LEILA: Now!\n"
            "(Omar lets go. The kite climbs higher and higher until it is a small red dot against the clouds.)\n"
            "OMAR: We did it! We did it together!\n"
            "LEILA: (grinning) You can hold the string next. Just hold on tight."
        ),
        "qs": [
            {"id": "faf607a520e8", "t": "mcq", "d": "retrieve", "q": "Who gave Leila the kite?",
             "opts": ["Auntie Samira", "Mum", "Omar", "Grandad"],
             "why": "Leila says, “Auntie Samira gave it to me for my birthday.”"},
            {"id": "d803d413dbb4", "t": "mcq", "d": "infer", "q": "How does Omar feel when the kite crashes the first time?",
             "opts": ["He finds it a little bit funny", "He is angry with Leila",
                      "He is scared the kite will hit him", "He is upset that it is broken"],
             "why": "The stage direction says he is “trying not to laugh”, and he teases Leila that it may be broken.",
             "no": {"He is upset that it is broken": "He only jokes that it might be broken, while trying not to laugh."}},
            {"id": "18a04b4b0752", "t": "mcq", "d": "structure", "q": "What are the words in brackets, like (sighing), for?",
             "opts": ["They tell the actors how to speak or what to do", "They are words the characters whisper",
                      "They show which character speaks next", "They are the title of each scene"],
             "why": "Words in brackets are stage directions: the actors do not say them, they act them."},
            {"id": "eaf9b1466fc5", "t": "mcq", "d": "vocab", "q": "Mum says they always “launched” kites with two people. What does “launched” mean here?",
             "opts": ["got them up into the air", "bought them from a shop", "made them at home",
                      "pulled them back down"],
             "why": "Mum explains how to launch a kite: one person holds it up while the other runs, so it rises into the air."},
            {"id": "f3649e218edb", "t": "tap", "d": "language", "q": "Tap the word Omar uses to give Leila his word that he will be careful.",
             "s": "I'd hold it really carefully, I [promise].",
             "why": "Saying “I promise” tells Leila he means it and will keep his word."},
            {"id": "be49520ad4cd", "t": "mcq", "d": "summarise", "q": "What is the main message of the play?",
             "opts": ["Some jobs go better when people share and work together", "Kites break easily on windy days",
                      "Older children should always be in charge", "Beaches are the best places to fly kites"],
             "why": "Leila cannot launch the kite alone; it flies only when she lets Omar help, and then she offers "
                    "him the string too."},
        ],
    },
    {
        "key": "RD4.08",
        "year": 4,
        "strand": "Information",
        "title": "Food chains",
        "nc": "Retrieve and record information from non-fiction; draw inferences and justify them with evidence",
        "text": (
            "Every living thing needs food to give it energy. A food chain shows how that energy passes from one "
            "living thing to another when one is eaten by the next.\n\n"
            "Almost every food chain begins with a green plant. Plants do not need to eat, because they make their "
            "own food using energy from sunlight, together with air and water. For this reason, plants are called "
            "producers. Animals cannot make their own food, so they must eat plants or other animals. They are "
            "called consumers.\n\n"
            "Here is a food chain from a British woodland:\n"
            "oak leaves → caterpillar → blue tit → sparrowhawk\n\n"
            "The arrows show which way the energy travels. The caterpillar munches the oak leaves. The blue tit eats "
            "the caterpillar, and the sparrowhawk catches the blue tit.\n\n"
            "An animal that hunts and eats other animals is called a predator. The animal it hunts is its prey. In "
            "this chain, the blue tit is a predator of the caterpillar, but it is also the prey of the sparrowhawk. "
            "The sparrowhawk is at the top of the chain, because nothing in this chain eats it.\n\n"
            "Food chains can be found in every habitat. In a pond, tadpoles nibble tiny green algae, a fish eats the "
            "tadpoles, and a heron standing in the shallows catches the fish.\n\n"
            "Food chains also show why every living thing matters, even the smallest. If something harmed the "
            "caterpillars in the wood, the blue tits would have less to eat. Fewer blue tits could survive, and in "
            "time the sparrowhawks would go hungry too. A change to one link in a chain can affect every living "
            "thing above it."
        ),
        "qs": [
            {"id": "4fae7952c55c", "t": "text", "d": "vocab", "q": "Find and copy the word for a living thing that makes its own food.",
             "a": ["producer", "producers", "a producer", "the producer", "the producers"],
             "why": "The second paragraph says plants make their own food, so they are called producers.",
             "no": {"consumer": "Consumers are animals: they cannot make their own food, so they eat it."}},
            {"id": "8b8410a7d620", "t": "mcq", "d": "retrieve", "q": "What do plants use to make their own food, according to the text?",
             "opts": ["energy from sunlight, with air and water", "small insects that land on their leaves",
                      "the bodies of animals that have died", "energy from the animals that eat them"],
             "why": "The second paragraph says plants make their food using energy from sunlight, together with air and water."},
            {"id": "a452e60f6756", "t": "mcq", "d": "retrieve", "q": "In the woodland food chain, what eats the caterpillar?",
             "opts": ["the blue tit", "the sparrowhawk", "the heron", "the fish"],
             "why": "The text says the blue tit eats the caterpillar. The heron and fish are in the pond chain."},
            {"id": "ed1a5661b86b", "t": "mcq", "d": "compare", "q": "How is the sparrowhawk different from the blue tit in the woodland chain?",
             "opts": ["Nothing in the chain eats the sparrowhawk", "The sparrowhawk eats oak leaves",
                      "The sparrowhawk is a producer", "The sparrowhawk is the prey of the caterpillar"],
             "why": "The blue tit is both predator and prey, but the sparrowhawk is at the top: nothing in the chain eats it."},
            {"id": "d938fe99bac0", "t": "order", "d": "sequence", "q": "Put the pond food chain in order, starting with the living thing that is eaten first.",
             "items": ["algae", "tadpole", "fish", "heron"],
             "why": "Tadpoles nibble algae, a fish eats the tadpoles, and a heron catches the fish."},
            {"id": "413612ad0612", "t": "mcq", "d": "predict", "q": "Suppose a disease killed many of the blue tits in the wood. Using the text, what would most likely happen to the caterpillars?",
             "opts": ["More of them would survive, because fewer would be eaten", "They would all die out as well",
                      "They would start to hunt the sparrowhawks", "They would stop eating oak leaves"],
             "why": "Blue tits eat caterpillars. With fewer blue tits hunting them, more caterpillars would be left alive.",
             "no": {"They would all die out as well": "The caterpillars eat oak leaves, not blue tits, so losing blue tits "
                                                     "does not take away their food."}},
        ],
    },
    {
        "key": "RD4.09",
        "year": 4,
        "strand": "Stories",
        "title": "Words in two languages",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Mateo stood at the window of the flat in Leeds, watching every taxi that turned into the street. His "
            "grandmother, Avó Lurdes, was flying in from Portugal to stay for a whole month, and he had not seen her "
            "since he was five.\n\n"
            "There was one problem. Avó Lurdes spoke hardly any English, and Mateo's Portuguese was not much better. "
            "He knew how to say hello and thank you, and that was about it. What would they talk about for a whole "
            "month?\n\n"
            "When she finally arrived, she was smaller than he remembered, with silver hair tied back and a suitcase "
            "almost as big as she was. She hugged him so tightly that his glasses squashed against her coat, and she "
            "said something very fast that made Mum laugh.\n\n"
            "For the first two days, Mateo mostly smiled and nodded. Then, on Saturday morning, Avó Lurdes found the "
            "packet of tomato seeds he had been given at school and never planted. She held it up, raised her "
            "eyebrows and pointed to the little balcony.\n\n"
            "They spent the morning filling pots with compost. Avó showed him how to press each seed in with a "
            "fingertip, not too deep, and how to water gently so the soil did not wash away. Whenever she pointed at "
            "something, she said its name in Portuguese, and Mateo repeated it. Whenever he pointed, he told her the "
            "English word. By lunchtime she could say “pot”, “water” and “sun”.\n\n"
            "By the time she went home, the seedlings were as tall as Mateo's hand, and he had a notebook full of "
            "new words. At the airport, he hugged her and said the longest sentence he had ever said in Portuguese. "
            "Avó Lurdes's eyes filled with tears, and this time she spoke slowly, so that he understood every word."
        ),
        "qs": [
            {"id": "ac0d36ac1152", "t": "mcq", "d": "retrieve", "q": "How long was Avó Lurdes coming to stay?",
             "opts": ["a month", "a week", "two days", "a year"],
             "why": "The first paragraph says she was coming to stay for a whole month."},
            {"id": "ab211119f9b8", "t": "mcq", "d": "infer", "q": "Why was Mateo worried before his grandmother arrived?",
             "opts": ["He thought they would not be able to talk to each other", "He thought she would not like the flat",
                      "He was afraid her taxi would get lost", "He thought she would be cross about the seeds"],
             "why": "She spoke hardly any English and he knew very little Portuguese, so he wondered what they would talk about."},
            {"id": "301cba7e1097", "t": "tap", "d": "retrieve", "q": "Tap the word that names the place Avó Lurdes pointed to.",
             "s": "She held it up, raised her eyebrows and pointed to the little [balcony].",
             "why": "She pointed to the balcony, where the seeds could be planted in pots."},
            {"id": "d89eea15288b", "t": "text", "d": "retrieve", "q": "What did they fill the pots with? Find and copy one word.",
             "a": ["compost", "the compost"],
             "why": "The fifth paragraph says they spent the morning filling pots with compost."},
            {"id": "1b72bd5ddc68", "t": "mcq", "d": "compare", "q": "How had things changed between Mateo and his grandmother by the end of her visit?",
             "opts": ["At first they only smiled and nodded, but by the end they could understand each other",
                      "At first they talked all day, but by the end they had nothing left to say",
                      "At first she spoke slowly, but by the end she spoke very fast",
                      "At first they gardened together, but by the end they had stopped"],
             "why": "For the first two days Mateo mostly smiled and nodded; by the airport he spoke a long Portuguese "
                    "sentence and understood every word she said."},
            {"id": "353a9360c010", "t": "mcq", "d": "infer", "q": "Why did Avó Lurdes's eyes fill with tears at the airport?",
             "opts": ["She was moved that Mateo could now speak to her in Portuguese",
                      "She was upset that the seedlings had not grown",
                      "She was cross that Mateo had hugged her too tightly",
                      "She was worried that she would miss her flight"],
             "why": "Mateo had just said his longest Portuguese sentence ever: she was touched and happy, not sad or cross.",
             "no": {"She was upset that the seedlings had not grown": "The seedlings had grown as tall as Mateo's hand."}},
        ],
    },
    {
        "key": "RD4.10",
        "year": 4,
        "strand": "Information",
        "title": "Sorting animals into groups",
        "nc": "Retrieve and record information from non-fiction; explain and discuss their understanding of what they have read",
        "text": (
            "There are millions of different kinds of animal on Earth. To make sense of them all, scientists sort "
            "them into groups, using features that the animals share. This is called classification.\n\n"
            "The first big question is whether an animal has a backbone. Animals with a backbone are called "
            "vertebrates. Animals without one are called invertebrates. Snails, worms, spiders and insects are all "
            "invertebrates, and in fact most kinds of animal on Earth belong to this group.\n\n"
            "Vertebrates can be sorted into five smaller groups. Fish live in water and breathe using gills, and most "
            "are covered in scales. Amphibians, such as frogs and newts, begin their lives in water and later live "
            "partly on land; they have smooth, damp skin. Reptiles, such as lizards, snakes and tortoises, have dry, "
            "scaly skin, and most lay eggs on land. Birds are the only animals with feathers, and they all lay eggs "
            "with hard shells. Mammals have hair or fur, and they feed their babies on milk.\n\n"
            "Sometimes an animal surprises us. A whale lives in the sea and is shaped like a fish, but it breathes "
            "air through a blowhole and feeds its young on milk, so it is a mammal. A bat can fly, but it has fur and "
            "no feathers, so it is a mammal too.\n\n"
            "Scientists often use a classification key to identify a living thing. A key is a set of questions with "
            "yes or no answers, such as “Does it have feathers?” Each answer leads to the next question, until only "
            "one group, or one animal, is left."
        ),
        "qs": [
            {"id": "d23a2d97e0d2", "t": "text", "d": "vocab", "q": "Find and copy the word for animals that have no backbone.",
             "a": ["invertebrates", "invertebrate", "the invertebrates"],
             "why": "The second paragraph says animals without a backbone are called invertebrates.",
             "no": {"vertebrates": "Vertebrates are the animals that do have a backbone."}},
            {"id": "b1e317d93954", "t": "mcq", "d": "retrieve", "q": "According to the text, which feature do only birds have?",
             "opts": ["feathers", "eggs", "wings", "scales"],
             "why": "The text says birds are the only animals with feathers. Reptiles lay eggs too, and bats have wings.",
             "no": {"wings": "Bats can fly too, and the text says they are mammals."}},
            {"id": "3177f12f9ae5", "t": "mcq", "d": "infer", "q": "Why might someone wrongly think a whale is a fish?",
             "opts": ["It lives in the sea and is shaped like a fish", "It lays eggs with hard shells",
                      "It has smooth, damp skin like a frog", "It feeds its babies on milk"],
             "why": "The fourth paragraph says a whale lives in the sea and is shaped like a fish, which is what fools people.",
             "no": {"It feeds its babies on milk": "Feeding babies on milk is what shows a whale is a mammal, not a fish."}},
            {"id": "5ac8214d81db", "t": "tap", "d": "retrieve", "q": "Tap the word that names what a whale breathes air through.",
             "s": "A whale lives in the sea and is shaped like a fish, but it breathes air through a [blowhole] and feeds its young on milk, so it is a mammal.",
             "why": "A whale breathes air through a blowhole, not through gills like a fish."},
            {"id": "da562cfd5c44", "t": "mcq", "d": "infer", "q": "An animal has dry, scaly skin and lays its eggs on land. Using the text, which group does it most likely belong to?",
             "opts": ["reptiles", "amphibians", "fish", "birds"],
             "why": "The text says reptiles have dry, scaly skin and most lay eggs on land.",
             "no": {"fish": "Fish live in water and breathe using gills; they do not lay eggs on land.",
                    "amphibians": "Amphibians have smooth, damp skin, not dry scales."}},
            {"id": "7d83874dda7d", "t": "mcq", "d": "summarise", "q": "What is the last paragraph mainly about?",
             "opts": ["how a key helps you identify a living thing", "why whales and bats are mammals",
                      "how many kinds of animal there are", "which animals have feathers"],
             "why": "The last paragraph explains what a classification key is and how its yes or no questions work."},
        ],
    },
    {
        "key": "RD4.11",
        "year": 4,
        "strand": "Poems",
        "title": "Listening from the hill",
        "nc": "Discuss words and phrases that capture the reader's interest and imagination; recognise some different forms of poetry",
        "text": (
            "I climbed the hill above the town\n"
            "one bright October day,\n"
            "and sat upon a mossy rock\n"
            "to hear what sounds would say.\n\n"
            "Down in the street, the market stalls\n"
            "were waking one by one;\n"
            "a shutter rattled, someone laughed,\n"
            "the day had just begun.\n\n"
            "A dog was barking by the bridge,\n"
            "a bus pulled from its stop,\n"
            "a baker called out, “Bread for sale!”\n"
            "outside the corner shop.\n\n"
            "But all those noises, loud down there,\n"
            "were thin and small up here,\n"
            "as if the wind had worn them down\n"
            "before they reached my ear.\n\n"
            "My teacher says that every sound\n"
            "begins as just a shiver:\n"
            "a plucked guitar, a beaten drum,\n"
            "a bee's wings as they quiver.\n\n"
            "The shaking travels through the air,\n"
            "it spreads out far and wide,\n"
            "until it reaches someone's ear\n"
            "and shakes the drum inside.\n\n"
            "And as it goes, each sound grows weak\n"
            "and fainter on its way;\n"
            "that's why the clatter of the town\n"
            "was whispering today.\n\n"
            "Then from the grass beside my rock\n"
            "a skylark rose and sang,\n"
            "so close and clear and bright and strong\n"
            "the hillside fairly rang.\n\n"
            "So near is loud and far is soft,\n"
            "and sound is shaking air.\n"
            "I learnt it all upon a hill,\n"
            "by simply sitting there."
        ),
        "qs": [
            {"id": "305705d4d1c2", "t": "mcq", "d": "retrieve", "q": "Where did the speaker sit to listen?",
             "opts": ["on a mossy rock on a hill", "beside a market stall", "at a desk in the classroom",
                      "on a bench in the street"],
             "why": "The first verse says the speaker climbed the hill and sat upon a mossy rock."},
            {"id": "3f870b75374a", "t": "mcq", "d": "infer", "q": "Why did the market noises seem “thin and small” to the speaker?",
             "opts": ["The speaker was a long way from the market", "The market stalls were still shut",
                      "The wind was making a louder noise", "Nobody was at the market yet"],
             "why": "The noises were loud “down there” but small “up here”: sounds grow fainter the further they travel.",
             "no": {"The market stalls were still shut": "The second verse says the stalls were waking, with a shutter "
                                                         "rattling and someone laughing."}},
            {"id": "6fa37b0d59bb", "t": "mcq", "d": "vocab", "q": "In the fifth verse, what does “quiver” mean?",
             "opts": ["shaking very quickly", "flying far away", "humming a tune", "folded up and still"],
             "why": "The verse is about sounds beginning as a shiver: a bee's wings quiver, or shake fast, to make a buzz."},
            {"id": "2f2b32fc6dd0", "t": "mcq", "d": "retrieve", "q": "According to the poem, what part of the ear does the shaking air shake?",
             "opts": ["the drum inside it", "the outside of the ear", "the hair around it", "the bones of the face"],
             "why": "The sixth verse says the shaking reaches someone's ear “and shakes the drum inside”."},
            {"id": "69ca42ddf3e5", "t": "text", "d": "retrieve", "q": "Find and copy the name of the bird that sang close to the speaker.",
             "a": ["skylark", "a skylark", "the skylark"],
             "why": "The eighth verse says a skylark rose from the grass beside the rock and sang."},
            {"id": "1f8f8e4fe3f7", "t": "mcq", "d": "summarise", "q": "What does the speaker learn on the hill?",
             "opts": ["Sound is shaking air and grows fainter with distance", "Skylarks only sing in October",
                      "Markets are the noisiest places in a town", "Wind is the loudest sound of all"],
             "why": "The last verse sums it up: near is loud, far is soft, and sound is shaking air."},
        ],
    },
    {
        "key": "RD4.12",
        "year": 4,
        "strand": "Information",
        "title": "Rainforests",
        "nc": "Identify main ideas drawn from more than one paragraph and summarise these",
        "text": (
            "Tropical rainforests grow in a belt around the middle of the Earth, close to the equator. They are found "
            "in places such as South America, Central Africa, South-East Asia and the north-east of Australia. The biggest of all is "
            "the Amazon rainforest in South America.\n\n"
            "As their name suggests, rainforests are very wet. In many of them it rains on most days of the year, and "
            "because they are near the equator, they are hot all year round as well. This warm, wet weather is "
            "perfect for plants, and rainforests are home to more kinds of plants and animals than any other habitat "
            "on land.\n\n"
            "A rainforest grows in layers, a bit like the floors of a tall building. At the very top is the emergent "
            "layer, where the tallest trees poke out above the rest. Below it is the canopy, a thick roof of leaves "
            "and branches. Most rainforest animals live here, including monkeys, toucans and tree frogs, because "
            "there is plenty of fruit and sunlight. Under the canopy is the understorey, a dim, shady place where "
            "plants with large leaves catch what little light gets through. At the bottom is the forest floor. It is "
            "so dark that few plants grow there, but it is busy with insects, fungi and other living things that "
            "break down fallen leaves.\n\n"
            "Rainforests matter to everyone. Many foods we enjoy first came from rainforests, such as bananas and "
            "cocoa, which is used to make chocolate.\n\n"
            "Sadly, large areas of rainforest are cut down every year to make room for farms and roads, or for their "
            "wood. When the trees go, the animals that live in them lose their homes. Many people around the world "
            "are now working to protect the rainforests that remain."
        ),
        "qs": [
            {"id": "960a92c70de5", "t": "mcq", "d": "retrieve", "q": "Where is the biggest rainforest of all, according to the text?",
             "opts": ["South America", "Central Africa", "South-East Asia", "Australia"],
             "why": "The first paragraph says the biggest is the Amazon rainforest in South America."},
            {"id": "5a5d326830c0", "t": "mcq", "d": "language", "q": "Why does the writer say a rainforest grows in layers “a bit like the floors of a tall building”?",
             "opts": ["To help the reader picture levels one above another", "To show that people live in rainforests",
                      "To explain why rainforests are so wet", "To show that rainforest trees are made into buildings"],
             "why": "A building has floors stacked one above another; the layers of a rainforest are stacked in the same way."},
            {"id": "20803cbd7547", "t": "text", "d": "retrieve", "q": "Find and copy the name of the top layer of a rainforest.",
             "a": ["emergent", "emergent layer", "the emergent layer", "the emergent"],
             "why": "The third paragraph says the very top is the emergent layer, where the tallest trees poke out.",
             "no": {"canopy": "The canopy is the thick roof of leaves just below the emergent layer."}},
            {"id": "36f1736e1daf", "t": "mcq", "d": "infer", "q": "Why do many plants in the understorey have such large leaves?",
             "opts": ["To catch as much of the little light as they can", "To keep the rain off the forest floor",
                      "To give shade to the animals in the canopy", "To catch the fruit that falls from above"],
             "why": "The understorey is dim because little light gets through; big leaves catch more of that light."},
            {"id": "00f76e1fbce5", "t": "mcq", "d": "vocab", "q": "The understorey is “a dim, shady place”. What does “dim” mean?",
             "opts": ["with not much light", "full of noise", "very wet", "high above the ground"],
             "why": "Only a little light gets through the canopy, so the understorey is dim: not bright."},
            {"id": "fff828bd7c23", "t": "mcq", "d": "infer", "q": "What can you tell about the writer's view of rainforests from the last two paragraphs?",
             "opts": ["The writer thinks they matter and should be protected",
                      "The writer thinks more of them should become farms",
                      "The writer thinks they are too dark to be useful",
                      "The writer thinks only the Amazon is worth saving"],
             "why": "The writer says rainforests “matter to everyone” and calls their cutting down sad: both show the "
                    "writer wants them protected."},
        ],
    },
    {
        "key": "RD4.13",
        "year": 4,
        "strand": "News reports",
        "title": "Pupils climb the highest mountain in Wales",
        "nc": "Identify how language, structure and presentation contribute to meaning; distinguish fact from opinion",
        "text": (
            "Twenty-eight pupils from Riverside Primary School in Shropshire reached the summit of Yr Wyddfa, also "
            "known as Snowdon, last Friday, raising more than £2,000 for the children's ward of their local "
            "hospital.\n\n"
            "Yr Wyddfa is the highest mountain in Wales, at 1,085 metres. The group, all aged eight or nine, set off "
            "up the Llanberis Path at eight o'clock in the morning with four teachers and a trained mountain "
            "leader.\n\n"
            "The weather was kind at first, but near the top a thick cloud rolled in and the air turned cold. “We "
            "could hardly see the person in front,” said Hannah Evans, aged nine. “Everyone put on their hats and "
            "gloves, and we held on to each other's backpacks.”\n\n"
            "The class had prepared for months, walking a little further each weekend and learning about mountain "
            "safety, including how quickly the weather can change high up. Their teacher, Mrs Kaur, said: “I'm "
            "incredibly proud of them. Some of these children had never climbed a hill before this year, and today "
            "they climbed the highest mountain in Wales.”\n\n"
            "The walk to the summit and back took nearly seven hours. “My legs were like jelly at the end,” said "
            "Arjun Mehta, aged eight, “but I'd do it again tomorrow.”\n\n"
            "The money raised will buy books, games and craft kits for children who have to stay in hospital. A "
            "nurse from the ward said the gifts would “make a real difference” to young patients.\n\n"
            "Mrs Kaur says the school is already planning next year's challenge. She would not say what it is, but "
            "she told the pupils to keep their walking boots handy."
        ),
        "qs": [
            {"id": "60afefc17eea", "t": "mcq", "d": "structure", "q": "What does the first paragraph of the report do?",
             "opts": ["It gives the main facts: who, what, when and why", "It shares the pupils' opinions of the walk",
                      "It describes the weather near the top", "It explains how the pupils prepared"],
             "why": "News reports open with the key facts: 28 pupils, reached the summit, last Friday, to raise money."},
            {"id": "f7377672e8f0", "t": "mcq", "d": "retrieve", "q": "How high is Yr Wyddfa, according to the report?",
             "opts": ["1,085 metres", "2,000 metres", "1,580 metres", "805 metres"],
             "why": "The second paragraph gives its height as 1,085 metres. £2,000 is the money raised."},
            {"id": "d2f614d28a3a", "t": "mcq", "d": "infer", "q": "Why did the pupils hold on to each other's backpacks?",
             "opts": ["So that nobody got lost in the thick cloud", "Because they were too tired to walk alone",
                      "To stop their backpacks falling open", "Because the path was covered in ice"],
             "why": "Hannah says they could hardly see the person in front, so holding on kept the group together."},
            {"id": "0f4f6e03c666", "t": "tap", "d": "language", "q": "Tap the word Arjun compares his legs to.",
             "s": "“My legs were like [jelly] at the end,” said Arjun Mehta, aged eight, “but I'd do it again tomorrow.”",
             "why": "Legs “like jelly” are wobbly and weak: it shows how tired the long walk made him."},
            {"id": "5d0d3c160c00", "t": "mcq", "d": "infer", "q": "What does Mrs Kaur's advice about walking boots suggest about next year's challenge?",
             "opts": ["It will probably involve another long walk", "It will take place inside the school hall",
                      "It will be a swimming race", "It will be cancelled because of the weather"],
             "why": "Telling the pupils to keep their walking boots handy, or ready to use, hints that they will need them again."},
            {"id": "d2ccf228b93c", "t": "mcq", "d": "purpose", "q": "Which of these, from the report, is an opinion, not a fact?",
             "opts": ["The gifts will make a real difference to young patients", "The walk to the summit and back took nearly seven hours",
                      "Yr Wyddfa is the highest mountain in Wales", "The group set off at eight o'clock in the morning"],
             "why": "This is what the nurse thinks of the gifts; it cannot be checked and proved. The others can be checked and proved true.",
             "no": {"Yr Wyddfa is the highest mountain in Wales": "Mountains can be measured and compared, so this is a fact."}},
        ],
    },
    {
        "key": "RD4.14",
        "year": 4,
        "strand": "Stories",
        "title": "One full length",
        "nc": "Draw inferences such as inferring characters' feelings; identify main ideas and summarise",
        "text": (
            "Every Tuesday afternoon, Class 4 walked to the leisure centre for their swimming lesson, and every "
            "Tuesday morning, Yusuf's stomach felt tight with dread.\n\n"
            "It was not the water itself that worried him. He liked splashing in the shallow end, and he could kick "
            "along with a float as fast as anyone. The trouble was putting his face under. Whenever he tried, water "
            "rushed up his nose, and he came up spluttering and coughing.\n\n"
            "“Lots of good swimmers felt like that once,” said Mr Campbell, the swimming teacher. “Here's a trick. "
            "Blow bubbles out through your nose the whole time your face is in the water. Then the water can't get "
            "in.”\n\n"
            "That evening Yusuf practised in the bath. He hummed and blew bubbles until the water fizzed. The next "
            "Tuesday he put on his goggles and lowered his face into the pool, breathing out slowly. He counted to "
            "three, then to five, then to ten. No water went up his nose at all.\n\n"
            "Week by week, he grew braver. First he pushed off from the side and glided with his face down. Then he "
            "added his legs, and then his arms. By the end of term, he could swim a whole width without stopping.\n\n"
            "At the last lesson, Mr Campbell said that anyone who wanted to could try to swim a full length, 25 "
            "metres, for a certificate. Yusuf's stomach tightened again. But this time, as he looked down the long "
            "blue lane, he felt something else as well. He wanted to try.\n\n"
            "He pushed off. Breathe out, kick, pull, breathe. Halfway along, his arms began to ache, but he kept "
            "going. When his fingers touched the far wall, the whole class was cheering.\n\n"
            "The certificate is pinned above his bed now, right next to his goggles."
        ),
        "qs": [
            {"id": "cd06d145775e", "t": "mcq", "d": "vocab", "q": "Yusuf's stomach “felt tight with dread”. What does “dread” mean?",
             "opts": ["fear of something that is going to happen", "excitement about a treat",
                      "hunger before a meal", "tiredness after a long walk"],
             "why": "The next paragraph explains what worried him about swimming: dread is fear of something to come."},
            {"id": "3c4785f4b6e8", "t": "mcq", "d": "retrieve", "q": "What was the real trouble for Yusuf in the pool?",
             "opts": ["putting his face under the water", "kicking along with a float",
                      "splashing in the shallow end", "walking to the leisure centre"],
             "why": "The second paragraph says he liked splashing and kicking; the trouble was putting his face under."},
            {"id": "eb7643128a10", "t": "text", "d": "retrieve", "q": "Where did Yusuf practise blowing bubbles that evening? Find and copy one word.",
             "a": ["bath", "the bath"],
             "why": "The fourth paragraph says that evening Yusuf practised in the bath."},
            {"id": "88b12770b1c5", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Mr Campbell shares a trick", "Yusuf blows bubbles in the bath",
                       "He glides from the side with his face down", "He swims a whole width",
                       "He swims a full length"],
             "why": "The trick comes first, then practice at home, then small steps in the pool, ending with the full length."},
            {"id": "12ca48ed800c", "t": "mcq", "d": "infer", "q": "At the last lesson, how was Yusuf's feeling different from before?",
             "opts": ["He was still nervous, but now he also wanted to try", "He was not nervous at all any more",
                      "He was bored and wanted to go home", "He was sure he would win a race"],
             "why": "His stomach tightened again, so he was still nervous, but he “felt something else as well”: he wanted to try.",
             "no": {"He was not nervous at all any more": "His stomach tightened again, which shows he was still nervous."}},
            {"id": "656062686b76", "t": "mcq", "d": "summarise", "q": "Which is the best summary of the story?",
             "opts": ["A boy who fears putting his face in the water learns, step by step, to swim a length",
                      "A boy beats the rest of his class in a swimming race at the leisure centre",
                      "A swimming teacher shows a whole class how to dive into the deep end",
                      "A boy loses his goggles at the pool and finally finds them at home"],
             "why": "The story follows Yusuf from fearing the water, through small steps, to swimming 25 metres."},
        ],
    },
]
