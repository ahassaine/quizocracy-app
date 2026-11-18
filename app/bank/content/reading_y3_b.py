"""Reading comprehension, Year 3, second set (keys RD3.15-RD3.28).

Fourteen more original passages, written by hand, 150-250 words each, six questions each (mcq with four
options, find-and-tap, find-and-copy and put-in-order), mixing the KS2 reading domains as in reading_y3.py.
Topics differ from the first set: the seashore, ancient Egypt, soil (Year 3 rocks and soils), camels, giant
pandas, the weather, railways, teamwork, a market in Ghana, a seal rescue, wheelchair basketball, with
one poem, instructions, a biography, a news report, a play script and a persuasive leaflet (a toy swap):

* RD3.15 Rosa and the rock pool (story: looking after the seashore)
* RD3.16 Farming by the Nile (information: ancient Egypt)
* RD3.17 How soil is made (explanation)
* RD3.18 In charge of the stall (story: responsibility, Ghana)
* RD3.19 The Wind (poem)
* RD3.20 Make a rain gauge (instructions)
* RD3.21 Camels (information: adaptation to the desert)
* RD3.22 George Stephenson (biography: early railways)
* RD3.23 The quiz team (story: teamwork)
* RD3.24 Seal pup goes home (news report)
* RD3.25 The muddy footprints (play script)
* RD3.26 Giant pandas (information)
* RD3.27 Come to the toy swap! (persuasive writing)
* RD3.28 Leila's first match (story: wheelchair basketball, perseverance)

Written for Quizocracy; to be reviewed line by line by a second reviewer (facts, one defensible answer,
no leaks) before it goes live.
"""

SKILLS = [
    {
        "key": "RD3.15",
        "year": 3,
        "strand": "Stories",
        "title": "Rosa and the rock pool",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "The tide was going out at Porthcurno, and Gran said it was the perfect time to explore. Rosa tucked her net under her arm and followed her across the wet sand to the rocks.\n\n"
                "The first pool was as clear as glass. At first, Rosa thought it was empty. Then a stone seemed to walk sideways. “A crab!” she gasped. It was a shore crab, greenish-brown and no bigger than a biscuit. It scuttled under a curtain of seaweed and vanished.\n\n"
                "Gran pointed to some dark red blobs stuck to the rock, like jelly sweets. “Beadlet anemones,” she said. “Under water, they open their tentacles to catch food. When the tide goes out, they fold them in to stay wet.”\n\n"
                "Rosa lifted a flat stone. Underneath, tiny fish darted away in every direction. She wanted to take one home in her bucket, but Gran shook her head.\n\n"
                "“This pool is their home,” Gran said. “A bucket would get warm in the sun, and they would die. We look, we learn, and we leave them where we found them.”\n\n"
                "Rosa put the stone back gently, the same way up, so that nothing underneath would be squashed. Then she noticed the sea creeping back over the sand.\n\n"
                "“Time to go,” said Gran. “The tide waits for no one.”\n\n"
                "On the way home, Rosa drew everything she had seen in her notebook, so that she would never forget it.",
        "qs": [
            {"id": "f91c17b3efa5", "t": "mcq", "d": "retrieve", "q": "Why did Gran say it was the perfect time to explore the rocks?",
             "opts": ["The tide was going out.", "The sun had just come out.", "The beach was empty.", "Rosa had a new net."],
             "why": "The first sentence says the tide was going out, and that is why Gran said it was the perfect time."},
            {"id": "5f4d655dbee1", "t": "mcq", "d": "infer", "q": "Why did Rosa think at first that the pool was empty?",
             "opts": ["The creatures were keeping still or hidden.", "The water was too muddy to see through.",
                      "The tide had washed everything away.", "Gran had already caught them all."],
             "why": "The water was clear, but the crab looked like a stone until it moved, and then it hid under the seaweed."},
            {"id": "75e0061cc2fc", "t": "tap", "d": "vocab", "q": "Tap the word that means “ran with quick, short steps”.",
             "s": "It [scuttled] under a curtain of seaweed and vanished.",
             "why": "A crab scuttles: it hurries along with quick, short steps."},
            {"id": "ae33b0ca60e1", "t": "mcq", "d": "language", "q": "The writer says the anemones looked “like jelly sweets”. What does this help you picture?",
             "opts": ["small, shiny, soft-looking blobs", "creatures that taste sweet", "creatures that move very fast", "hard, spiky shells"],
             "why": "Jelly sweets are small, soft and shiny, just like the folded-up anemones on the rock."},
            {"id": "f5c733e34eb9", "t": "text", "d": "retrieve", "q": "What do the anemones do with their tentacles when the tide goes out? Find and copy the words.",
             "a": ["fold them in", "they fold them in", "fold them"],
             "why": "Gran says that when the tide goes out, they fold them in to stay wet."},
            {"id": "f00d81f5f761", "t": "mcq", "d": "summarise", "q": "What lesson does Gran teach Rosa?",
             "opts": ["to look at sea creatures but leave them where they live", "to catch as many crabs as she can",
                      "to draw a picture of every animal she sees", "to stay away from rock pools when it is sunny"],
             "why": "Gran says, “We look, we learn, and we leave them where we found them.”"},
        ],
    },
    {
        "key": "RD3.16",
        "year": 3,
        "strand": "Information",
        "title": "Farming by the Nile",
        "nc": "Retrieve and record information from non-fiction",
        "text": "Ancient Egypt grew up along the River Nile, in the north-east of Africa. Most of the land around the river was hot, dry desert, where almost nothing could grow. So nearly everyone lived on a narrow strip of land close to the water.\n\n"
                "Every summer, heavy rain fell far away to the south, in the mountains where much of the river's water came from. The Nile rose and flooded the fields on both banks. When the water went down again a few months later, it left behind a layer of thick, black mud. This mud was full of goodness for plants, so it made the soil very rich.\n\n"
                "Farmers sowed their seeds in the damp mud. They grew wheat and barley to make bread, as well as onions, beans and lentils. They also grew flax, a plant whose stems could be spun into thread and woven into linen cloth.\n\n"
                "In the dry months, farmers had to bring water to their crops. Many used a shaduf: a long pole with a bucket on one end and a heavy weight on the other. The weight made it easy to swing the full bucket up from the river and tip it into a ditch.\n\n"
                "Reeds called papyrus grew thickly along the riverbanks. The Egyptians used them to make boats, baskets, rope and even a kind of paper. Without the Nile, there would have been no ancient Egypt.",
        "qs": [
            {"id": "3b058bcff704", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the text.",
             "items": ["Heavy rain fell in the mountains to the south.", "The Nile flooded the fields.",
                       "The water went down and left black mud.", "Farmers sowed seeds in the damp mud."],
             "why": "The second and third paragraphs explain the farming year in order: rain, flood, mud, then sowing."},
            {"id": "086dce19fbf9", "t": "mcq", "d": "vocab", "q": "“This mud was full of goodness for plants.” What does “goodness” mean here?",
             "opts": ["things that help plants to grow", "kind and helpful behaviour", "a sweet taste", "clean, fresh water"],
             "why": "The sentence goes on to say the mud made the soil very rich, so “goodness” means what plants need to grow well."},
            {"id": "9e00d8a0db46", "t": "text", "d": "retrieve", "q": "Which plant did the Egyptians spin and weave into linen? Find and copy one word.",
             "a": ["flax"],
             "why": "The third paragraph says flax stems could be spun into thread and woven into linen cloth."},
            {"id": "ad55af7c3b25", "t": "mcq", "d": "infer", "q": "Why did farmers need a shaduf in the dry months, but not straight after the flood?",
             "opts": ["After the flood, the ground was already wet.", "The shaduf only worked when it was raining.",
                      "The river disappeared after the flood.", "Farmers were busy making paper after the flood."],
             "why": "Seeds were sown in the damp mud the flood left behind. Only in the dry months did water have to be lifted from the river."},
            {"id": "e99e865b3aa9", "t": "tap", "d": "retrieve", "q": "Tap the word that names the reeds the Egyptians used to make paper.",
             "s": "Reeds called [papyrus] grew thickly along the riverbanks.",
             "why": "The reeds were called papyrus, and they were used for boats, baskets, rope and paper."},
            {"id": "cb9e0c917ad1", "t": "mcq", "d": "summarise", "q": "What is the main idea of the whole text?",
             "opts": ["The Nile made life possible in ancient Egypt.", "Farmers in Egypt built a lot of boats.",
                      "The Egyptians lived in the mountains.", "Linen cloth was made from papyrus reeds."],
             "why": "Every paragraph shows how the river gave the Egyptians food, water and materials, and the last sentence sums it up."},
        ],
    },
    {
        "key": "RD3.17",
        "year": 3,
        "strand": "Explanations",
        "title": "How soil is made",
        "nc": "Read books that are structured in different ways and read for a range of purposes",
        "text": "Soil covers much of the land, but it takes a very long time to make. Just a thin layer of it can take hundreds of years to form.\n\n"
                "Soil begins as rock. Rain, wind and ice slowly break rock into smaller and smaller pieces. When water gets into a crack in a rock and freezes, it turns into ice and takes up more space. The ice pushes the crack wider. After this happens again and again, pieces of rock break off. Rivers and waves roll these pieces against each other until some are as small as grains of sand, or even smaller.\n\n"
                "Next, living things join in. When leaves fall and plants and animals die, they rot. Tiny living things, too small to see, break them down into a dark, crumbly material called humus. Humus mixes with the rock pieces and helps plants to grow.\n\n"
                "Earthworms are important too. As they tunnel, they pull dead leaves down from the surface and mix the soil. Their tunnels let air and water reach plant roots.\n\n"
                "So soil is a mixture of tiny bits of rock, humus, air and water. Not all soil is the same. Sandy soil has large grains, so water drains through it quickly. Clay soil has very fine grains that stick together, so it holds water and feels sticky when it is wet.",
        "qs": [
            {"id": "2e997ad7e975", "t": "mcq", "d": "retrieve", "q": "According to the text, what does ice do to a crack in a rock?",
             "opts": ["It pushes the crack wider.", "It melts the rock into soil.", "It fills the crack and seals it shut.", "It makes the rock soft."],
             "why": "The second paragraph says water freezes, takes up more space, and the ice pushes the crack wider."},
            {"id": "78d72abcee6a", "t": "mcq", "d": "vocab", "q": "What is “humus”, as the word is used in this text?",
             "opts": ["dark, crumbly stuff made from rotted things", "tiny pieces of broken rock",
                      "sand that has been rolled about by waves", "the tunnels that earthworms make"],
             "why": "The third paragraph explains that rotting leaves, plants and animals are broken down into humus."},
            {"id": "d7cc656b63b0", "t": "tap", "d": "retrieve", "q": "Tap the two words that tell you what earthworms pull down from the surface.",
             "s": "As they tunnel, they pull [dead] [leaves] down from the surface and mix the soil.",
             "why": "Earthworms pull dead leaves down into the soil as they tunnel."},
            {"id": "8ea5495b872e", "t": "mcq", "d": "infer", "q": "Why might a gardener be pleased to find lots of earthworms in a flower bed?",
             "opts": ["The worms help air and water reach the roots.", "The worms turn the soil into fine sand.",
                      "The worms stop rain soaking into the soil.", "The worms break big rocks into pieces."],
             "why": "Plants need air and water at their roots, and the fourth paragraph says worms' tunnels let them in."},
            {"id": "d5f37b15a41a", "t": "mcq", "d": "compare", "q": "How is clay soil different from sandy soil?",
             "opts": ["It holds on to water for longer.", "It has larger grains of rock.",
                      "It is made without any rock.", "It lets water drain away faster."],
             "why": "The last paragraph says water drains quickly through sandy soil, but clay soil holds water."},
            {"id": "8227a0084f75", "t": "mcq", "d": "structure", "q": "Why does the writer start paragraphs with “Soil begins as rock” and “Next, living things join in”?",
             "opts": ["to show the steps in the order they happen", "to list the animals that live in soil",
                      "to tell a story about one worm", "to ask the reader questions"],
             "why": "These words take the reader through the steps one after another: first rock breaks down, next living things add humus."},
        ],
    },
    {
        "key": "RD3.18",
        "year": 3,
        "strand": "Stories",
        "title": "In charge of the stall",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "Every Saturday, Kwame helped Auntie Efua at her fruit stall in the big market in Kumasi, in Ghana. He liked stacking the mangoes into neat yellow pyramids and calling out, “Sweet pineapples! Fresh bananas!” to the people walking past.\n\n"
                "That morning, Auntie Efua needed to fetch more pineapples from the truck at the edge of the market. “You are in charge now,” she told him. “I will be back soon. Count the change carefully.”\n\n"
                "Kwame stood up very straight. He sold three oranges to a woman with a baby on her back, and he counted the coins twice before he put them in the tin.\n\n"
                "Then the sky turned dark grey. A cold wind blew dust between the stalls, and the traders all around began pulling covers over their goods. Kwame knew what that meant. He dragged the big plastic sheet from under the table and threw it over the fruit. The wind kept lifting the corners, so he weighed each one down with a heavy pineapple.\n\n"
                "A moment later, the rain came hammering down. Kwame crouched under the table with the money tin hugged to his chest.\n\n"
                "When the storm had passed, Auntie Efua hurried back, soaked to the skin. She lifted the sheet. Every mango was dry, and every coin was in the tin.\n\n"
                "She smiled and handed Kwame the biggest mango on the stall. “Next Saturday,” she said, “you can be in charge all morning.”",
        "qs": [
            {"id": "7c7225d7b85b", "t": "mcq", "d": "retrieve", "q": "Why did Auntie Efua leave the stall?",
             "opts": ["to fetch more pineapples from the truck", "to buy a big plastic sheet",
                      "to get out of the rain", "to sell oranges to a woman"],
             "why": "The second paragraph says she needed to fetch more pineapples from the truck at the edge of the market."},
            {"id": "23b55253800c", "t": "mcq", "d": "vocab", "q": "Auntie Efua says, “You are in charge now.” What does she mean?",
             "opts": ["You are the one looking after the stall.", "You must pay for all the fruit.",
                      "You must pack up the stall.", "You may eat any fruit you like."],
             "why": "Being in charge means being the person responsible. Kwame had to look after the stall while she was away."},
            {"id": "2a7dcb8a810b", "t": "mcq", "d": "infer", "q": "“Kwame knew what that meant.” What did Kwame know?",
             "opts": ["Heavy rain was about to fall.", "The market was closing early.",
                      "Auntie Efua was on her way back.", "Someone had taken some fruit."],
             "why": "The dark sky, the cold wind and the traders covering their goods all warned that a storm was coming."},
            {"id": "add01fa8a4bc", "t": "text", "d": "retrieve", "q": "What did Kwame use to weigh down the corners of the sheet? Find and copy the words.",
             "a": ["a heavy pineapple", "heavy pineapple", "pineapple", "a pineapple", "pineapples", "heavy pineapples"],
             "why": "The fourth paragraph says he weighed each corner down with a heavy pineapple."},
            {"id": "28fb7a4367be", "t": "mcq", "d": "language", "q": "The writer says the rain came “hammering down”. What does this tell you about the rain?",
             "opts": ["It was very heavy and loud.", "It was light and gentle.", "It stopped after a second.", "It was full of dust."],
             "why": "A hammer hits hard and makes a loud noise, so the rain was falling hard and noisily."},
            {"id": "4dc5f38418ba", "t": "mcq", "d": "infer", "q": "Why did Auntie Efua give Kwame the biggest mango?",
             "opts": ["to thank him for looking after the stall so well", "because it was too bruised to sell",
                      "because he had sold the most oranges", "because he was soaked from the rain"],
             "why": "She found the fruit dry and the money safe. The mango, and the offer of a whole morning in charge, show she was pleased with him."},
        ],
    },
    {
        "key": "RD3.19",
        "year": 3,
        "strand": "Poems",
        "title": "The Wind",
        "nc": "Discuss words and phrases that capture the reader's interest and imagination",
        "text": "The wind came racing down the hill\n"
                "And rattled at our door.\n"
                "It whistled through the letterbox\n"
                "And sneaked across the floor.\n\n"
                "It tugged the washing on the line\n"
                "And made the bedsheets fill\n"
                "Like sails upon a little boat\n"
                "That never could keep still.\n\n"
                "It chased the leaves around the yard\n"
                "And spun them high and low,\n"
                "Then dropped them in a crunchy heap\n"
                "And wondered where to go.\n\n"
                "It grabbed my hat and threw it up\n"
                "Into the apple tree.\n"
                "I'm sure I heard it chuckle as\n"
                "It looked back down at me.\n\n"
                "It lifted Kofi's yellow kite\n"
                "Up, up into the sky,\n"
                "And tugged the string so hard that he\n"
                "Was nearly pulled up high.\n\n"
                "At night it howled around the house\n"
                "And moaned along the lane.\n"
                "It pushed against my window glass\n"
                "And drummed with drops of rain.\n\n"
                "But in the morning, all was calm.\n"
                "The trees stood still and tall.\n"
                "The wind had slipped off somewhere else\n"
                "Without a word at all.",
        "qs": [
            {"id": "b5068949ef82", "t": "mcq", "d": "vocab", "q": "In verse 1, the wind “rattled at our door”. What does “rattled” mean?",
             "opts": ["shook it so that it knocked", "blew it wide open", "locked it tight shut", "closed it very quietly"],
             "why": "Rattling is shaking something so that it makes short, knocking sounds, as a door does in a strong wind."},
            {"id": "209fe3d48208", "t": "mcq", "d": "language", "q": "In verse 2, why does the poet compare the bedsheets to sails?",
             "opts": ["The wind filled them out, as it fills the sails of a boat.", "The bedsheets were blown into the sea.",
                      "The bedsheets were folded into the shape of a boat.", "The washing line was on a boat."],
             "why": "The wind “made the bedsheets fill”: they puffed out, just as sails do when the wind blows into them."},
            {"id": "5ef202ee8e7c", "t": "tap", "d": "retrieve", "q": "Tap the two words that name what the wind threw the poet's hat into.",
             "s": "It grabbed my hat and threw it up\nInto the [apple] [tree].",
             "why": "Verse 4 says the wind threw the hat up into the apple tree."},
            {"id": "e818a9c43c92", "t": "mcq", "d": "language", "q": "“I'm sure I heard it chuckle.” Why does the poet say the wind chuckled?",
             "opts": ["to make the wind seem like a cheeky person", "to show the hat made a noise in the tree",
                      "to show that the poet was laughing", "to tell us the wind was very cold"],
             "why": "Only people chuckle. Writing this makes the wind seem like a playful person who enjoyed the trick."},
            {"id": "e28526c1cc6d", "t": "text", "d": "retrieve", "q": "Whose kite did the wind lift? Find and copy the name.",
             "a": ["Kofi", "Kofi's"],
             "why": "Verse 5 says the wind lifted Kofi's yellow kite."},
            {"id": "ef73d9078881", "t": "mcq", "d": "compare", "q": "How is the last verse different from the rest of the poem?",
             "opts": ["The wind has gone, and everything is still.", "The wind is stronger than ever.",
                      "The wind brings snow instead of rain.", "The wind blows the trees down."],
             "why": "In the last verse “all was calm” and the trees “stood still”: the wind had gone somewhere else."},
        ],
    },
    {
        "key": "RD3.20",
        "year": 3,
        "strand": "Instructions",
        "title": "Make a rain gauge",
        "nc": "Read books that are structured in different ways and read for a range of purposes",
        "text": "A rain gauge measures how much rain falls. Weather stations all over the world use them. You can make your own and keep a record of the rain where you live.\n\n"
                "You will need: a clear plastic bottle with straight sides and a flat bottom, scissors, sticky tape, a ruler and a notebook.\n\n"
                "1. Ask an adult to cut the top third off the bottle. Keep both pieces.\n"
                "2. Turn the top piece upside down and push it into the bottom piece, so that it makes a funnel. Tape it in place.\n"
                "3. Tape the ruler to the outside of the bottle, with the zero level with the bottom.\n"
                "4. Find an open space outside, away from trees, walls and roofs.\n"
                "5. Dig a small hole and stand the bottle in it, so that the wind cannot blow it over.\n"
                "6. Check the bottle at the same time every day. Read the level of the water on the ruler in millimetres.\n"
                "7. Write the date and the reading in your notebook.\n"
                "8. Empty the bottle and put it back in its hole.\n\n"
                "Tip: the funnel guides the rain into the bottle, and its narrow neck helps stop the water drying up before you read it. After a few weeks, look back at your notebook to find your wettest day. You could make a bar chart of your results.",
        "qs": [
            {"id": "c6e94afc9faf", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how much of the bottle the adult should cut off.",
             "s": "Ask an adult to cut the top [third] off the bottle.",
             "why": "Step 1 says to cut the top third off the bottle."},
            {"id": "ae63634c2e07", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Cut the top off the bottle.", "Push the top piece in to make a funnel.", "Stand the bottle in a hole.",
                       "Write the reading in your notebook.", "Empty the bottle."],
             "why": "Follow the numbered steps: cut (1), funnel (2), hole (5), write (7), empty (8)."},
            {"id": "f1d20fef76d5", "t": "mcq", "d": "infer", "q": "Why should the rain gauge be put away from trees, walls and roofs?",
             "opts": ["They could block the rain or drip extra water in.", "The bottle must stay in the shade.",
                      "Nobody must be able to find it.", "The wind needs to reach it."],
             "why": "Trees, walls and roofs could stop rain falling in or let extra drips run in, so the reading would be wrong."},
            {"id": "d80d0fc6dd5c", "t": "text", "d": "retrieve", "q": "What unit should you use to read the level of the water? Find and copy one word.",
             "a": ["millimetres", "millimetre", "mm"],
             "why": "Step 6 says to read the level of the water on the ruler in millimetres."},
            {"id": "4c29cdd6a04d", "t": "mcq", "d": "infer", "q": "Why should you empty the bottle after each reading?",
             "opts": ["so the next reading shows only one day's rain", "so the bottle does not get too heavy",
                      "so the funnel does not fall off", "so insects can get out"],
             "why": "If the water stayed in, each reading would add up all the rain so far, not just the rain since yesterday."},
            {"id": "c57a48b4835a", "t": "mcq", "d": "structure", "q": "Why is the list of things you need put before the numbered steps?",
             "opts": ["so you can collect everything before you start", "so you know how to read the ruler",
                      "so you can find your wettest day", "so you know where to dig the hole"],
             "why": "Gathering everything first means you will not have to stop in the middle of making the rain gauge."},
        ],
    },
    {
        "key": "RD3.21",
        "year": 3,
        "strand": "Information",
        "title": "Camels",
        "nc": "Retrieve and record information from non-fiction",
        "text": "Camels live in some of the hottest, driest places on Earth. Their bodies are built for life in the desert.\n\n"
                "There are two main kinds. The dromedary has one hump and lives mostly in North Africa and the Middle East. The Bactrian camel has two humps and lives in the deserts of Central Asia, where the winters can be freezing.\n\n"
                "Many people think a camel's hump is full of water, but it is not. It is a store of fat. When food is hard to find, the camel's body uses up the fat, and the hump becomes smaller and floppy. When the camel eats well again, the hump grows firm.\n\n"
                "A camel can go for many days without drinking. When it does find water, it can drink a huge amount very quickly.\n\n"
                "Desert winds blow sand into the air, but camels are well protected. They have two rows of long eyelashes to keep sand out of their eyes, and they can close their nostrils. Their wide, padded feet spread out on soft sand, so they do not sink, a bit like snowshoes on snow.\n\n"
                "For thousands of years, people have used camels to carry heavy loads across the desert. That is why the camel is sometimes called “the ship of the desert”.",
        "qs": [
            {"id": "212dc0e19ed6", "t": "mcq", "d": "compare", "q": "How is a Bactrian camel different from a dromedary?",
             "opts": ["It has two humps.", "It has one hump.", "It lives in North Africa.", "It cannot close its nostrils."],
             "why": "The second paragraph says the dromedary has one hump and the Bactrian camel has two."},
            {"id": "3c8b8d261af7", "t": "mcq", "d": "retrieve", "q": "According to the text, what is stored in a camel's hump?",
             "opts": ["fat", "water", "milk", "air"],
             "why": "The third paragraph says many people think the hump is full of water, but it is a store of fat."},
            {"id": "1a27644f69fb", "t": "mcq", "d": "infer", "q": "A camel's hump is small and floppy. What does this probably tell you?",
             "opts": ["It has not found much food lately.", "It has just drunk a lot of water.",
                      "It is a Bactrian camel.", "It has just eaten a big meal."],
             "why": "The hump gets smaller and floppy when food is hard to find and the body uses up the fat."},
            {"id": "085bba0ce104", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what camels can close to keep sand out.",
             "s": "They have two rows of long eyelashes to keep sand out of their eyes, and they can close their [nostrils].",
             "why": "Camels can close their nostrils, so sand does not get in when they breathe."},
            {"id": "db2db7d40716", "t": "mcq", "d": "language", "q": "Why does the writer say camels' feet are “a bit like snowshoes on snow”?",
             "opts": ["to explain how wide feet stop them sinking", "to show that camels live where it snows",
                      "to say that camels' feet feel cold", "to show that camels walk slowly"],
             "why": "Snowshoes are wide so that they spread your weight and you do not sink. Camels' wide feet do the same on sand."},
            {"id": "0287443e070d", "t": "mcq", "d": "infer", "q": "Why is the camel called “the ship of the desert”?",
             "opts": ["It carries heavy loads across the sand, as ships do at sea.",
                      "It was first carried to the desert on board a ship.", "It is as big and as heavy as a small fishing boat.",
                      "It can drink as much water as a small ship can hold."],
             "why": "People have used camels to carry heavy loads across the desert, the job a ship does on the sea."},
        ],
    },
    {
        "key": "RD3.22",
        "year": 3,
        "strand": "Biography",
        "title": "George Stephenson",
        "nc": "Retrieve and record information from non-fiction",
        "text": "George Stephenson was born in 1781 in Wylam, a village near Newcastle in the north-east of England. His family was poor, so he did not go to school. As a boy, he earned money by looking after cows. Later, he worked at the coal mines, like his father.\n\n"
                "At the mines, steam engines pumped water out of the tunnels. George loved to take them apart and find out how they worked. Soon he could mend engines that nobody else could fix.\n\n"
                "George could not read or write until he was eighteen. Then he paid for lessons in the evenings, after long days at work. He wanted to be able to read about engines and new inventions.\n\n"
                "In those days, coal was pulled along tracks by horses. George built steam engines that ran on rails instead. They were called locomotives. In 1825, his engine Locomotion No. 1 pulled the first train on the Stockton and Darlington Railway, the first public railway to use steam locomotives.\n\n"
                "In 1829, a competition was held to find the best engine for a new railway between Liverpool and Manchester. George's son Robert built an engine called the Rocket, working with his father. It beat all the others.\n\n"
                "George Stephenson died in 1848. The distance he chose between the two rails is still used on most railways in Britain today, and he is often called the Father of Railways.",
        "qs": [
            {"id": "0aa0961b8565", "t": "mcq", "d": "retrieve", "q": "According to the text, why did George not go to school?",
             "opts": ["His family was poor.", "There was no school in Wylam.", "He was too busy mending engines.", "He did not like reading."],
             "why": "The first paragraph says his family was poor, so he did not go to school."},
            {"id": "aaa0e7af4b86", "t": "mcq", "d": "infer", "q": "How was George able to mend engines that nobody else could fix?",
             "opts": ["He had taken engines apart to learn how they worked.", "He had read lots of books about engines as a boy.",
                      "His father had built the engines.", "He had been to a school for engineers."],
             "why": "He took the engines apart to find out how they worked. He could not read yet, so it was not from books."},
            {"id": "a9dd9d4fc968", "t": "mcq", "d": "infer", "q": "George paid for evening lessons after long days at work. What does this show about him?",
             "opts": ["He was determined to learn.", "He did not like his job.", "He had lots of spare money.", "He found reading easy."],
             "why": "He was tired and poor, but he still paid to learn to read in his own time: he really wanted to learn."},
            {"id": "3530414ddbe8", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what pulled coal along tracks before George's engines.",
             "s": "In those days, coal was pulled along tracks by [horses].",
             "why": "The fourth paragraph says that in those days coal was pulled along tracks by horses."},
            {"id": "a8466c1cea7e", "t": "text", "d": "vocab", "q": "Find and copy the word that means “steam engines that ran on rails”.",
             "a": ["locomotives", "locomotive"],
             "why": "The fourth paragraph says George's steam engines that ran on rails were called locomotives."},
            {"id": "e67a315a5e6e", "t": "order", "d": "sequence", "q": "Put these in the order they happened in George's life.",
             "items": ["George looked after cows.", "George learned to read.", "Locomotion No. 1 pulled its first train.",
                       "The Rocket won the competition."],
             "why": "The text tells his life in time order: a boy with cows, reading at eighteen, 1825, then 1829."},
        ],
    },
    {
        "key": "RD3.23",
        "year": 3,
        "strand": "Stories",
        "title": "The quiz team",
        "nc": "Predict what might happen from details stated and implied",
        "text": "Finn, Mei and Tariq were Class 3's team for the school quiz in Belfast. Finn was sure they would win, because he knew lots of facts.\n\n"
                "In the first round, Finn grabbed the answer sheet and wrote every answer himself, as fast as he could. When the scores were read out, the team had only four points out of ten. Mei had known two of the answers he got wrong, but he had not given her a chance to speak.\n\n"
                "“Let's try something different,” said Tariq at the break. “Before anyone writes, we all say what we think.”\n\n"
                "Finn folded his arms. Then he looked at the scoreboard, and slowly he nodded.\n\n"
                "In the second round, the question was: “Which is the longest river in the United Kingdom?” Finn wanted to write “the Thames”. Mei whispered, “I think it's the Severn. We learned it in geography.” Tariq agreed with Mei. Finn took a breath and wrote “Severn”.\n\n"
                "It was right.\n\n"
                "After that, they took turns with the pen. Tariq knew about planets, Mei knew about rivers and maps, and Finn knew all his times tables. In every round after the first, they scored nine out of ten.\n\n"
                "They did not come first. They came second, just one point behind Class 4. But on the walk home, Finn said it was the best quiz he had ever done.",
        "qs": [
            {"id": "6cfe142b9e94", "t": "mcq", "d": "retrieve", "q": "Why was Finn sure the team would win?",
             "opts": ["He knew lots of facts.", "They had won the quiz before.", "Class 4 was not taking part.", "Mei had practised every night."],
             "why": "The first paragraph says Finn was sure they would win because he knew lots of facts."},
            {"id": "19ba6caf5a3a", "t": "mcq", "d": "infer", "q": "Why did the team do badly in the first round?",
             "opts": ["Finn answered alone without listening to the others.", "The questions were about rivers and maps.",
                      "Mei and Tariq did not know any answers.", "They ran out of time to write."],
             "why": "Finn wrote every answer himself. Mei knew two of the ones he got wrong, but he did not let her speak."},
            {"id": "ecf1a3dbf30c", "t": "mcq", "d": "infer", "q": "Why did Finn fold his arms when Tariq made his suggestion?",
             "opts": ["He did not like Tariq's idea at first.", "He was feeling cold in the hall.",
                      "He was waiting for the next question.", "He was pleased with their score."],
             "why": "Folding your arms often shows you are not happy with an idea. He only nodded after looking at their low score."},
            {"id": "10a55b620ca3", "t": "text", "d": "retrieve", "q": "Which river did Mei say was the longest in the United Kingdom? Find and copy the name.",
             "a": ["Severn", "the Severn", "River Severn", "the River Severn"],
             "why": "Mei whispered, “I think it's the Severn.”"},
            {"id": "b614af594254", "t": "mcq", "d": "predict", "q": "Next year the same three are in the quiz team again. What are they most likely to do?",
             "opts": ["talk about each answer together before writing", "let Finn write every answer by himself",
                      "stay at home on the day of the quiz", "only answer questions about planets"],
             "why": "Sharing ideas raised their score from four to nine, and Finn enjoyed it, so they are likely to work together again."},
            {"id": "bec0f98fbe2c", "t": "mcq", "d": "summarise", "q": "What is the main lesson of the story?",
             "opts": ["A team does better when everyone is listened to.", "You must always answer as fast as you can.",
                      "Coming second is the same as losing.", "It is best to learn every fact yourself."],
             "why": "When all three shared what they knew, they scored much higher than when Finn worked alone."},
        ],
    },
    {
        "key": "RD3.24",
        "year": 3,
        "strand": "News reports",
        "title": "Seal pup goes home",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": "A young grey seal that was found alone and underweight on a Norfolk beach has been returned to the sea after six weeks of care.\n\n"
                "The pup was spotted in December by a dog walker, Mrs Janet Hughes, after a night of strong winds and high waves. “It was lying very still near the dunes,” she said. “I kept my dog well back and phoned the rescue centre straight away.”\n\n"
                "Experts think the storm had separated the pup from its mother before it was ready to look after itself. It weighed only about half as much as a healthy pup of its age.\n\n"
                "At the rescue centre, the pup was kept warm and fed on fish, first mashed and then whole. The staff named it Pebble. By the end of January, Pebble had grown strong and could catch fish in a pool without any help.\n\n"
                "Last Tuesday, Pebble was carried down the beach in a crate. When the door opened, the seal paused, then flopped across the sand and slid into the waves.\n\n"
                "The rescue centre has a message for anyone who finds a seal pup on a beach: do not touch it, keep dogs on a lead, stay well back and call for help. Never try to push a pup into the water.",
        "qs": [
            {"id": "a4e5a5617b4f", "t": "mcq", "d": "structure", "q": "What does the first paragraph of this report do?",
             "opts": ["It gives the main news in one sentence.", "It tells you how to help a seal.",
                      "It describes the storm in detail.", "It tells you who Mrs Hughes is."],
             "why": "The first sentence tells the whole story in short: a seal was found, cared for and returned to the sea."},
            {"id": "93e5acb43366", "t": "mcq", "d": "retrieve", "q": "Who found the seal pup on the beach?",
             "opts": ["a dog walker", "a rescue worker", "a fisherman", "a lifeguard"],
             "why": "The second paragraph says the pup was spotted by a dog walker, Mrs Janet Hughes."},
            {"id": "ce35aa130a17", "t": "mcq", "d": "infer", "q": "Why did Mrs Hughes keep her dog well back?",
             "opts": ["so it would not frighten or hurt the pup", "so it would not get wet in the waves",
                      "so it would not run into the dunes", "so she could phone without dropping the lead"],
             "why": "The pup was weak and alone. A dog close by could scare it or hurt it, and the rescue centre says to keep dogs back."},
            {"id": "ad1c8fc5e543", "t": "text", "d": "retrieve", "q": "What name did the staff give the seal? Find and copy it.",
             "a": ["Pebble"],
             "why": "The fourth paragraph says the staff named it Pebble."},
            {"id": "dc84c4c60b6d", "t": "mcq", "d": "vocab", "q": "“The seal paused, then flopped across the sand.” What does “paused” mean?",
             "opts": ["stopped for a moment", "turned round", "rolled over", "cried out"],
             "why": "To pause is to stop for a short time before carrying on. Pebble waited a moment, then went into the sea."},
            {"id": "38ed38f3a806", "t": "mcq", "d": "purpose", "q": "Why does the report end with the rescue centre's message?",
             "opts": ["to tell readers what to do if they find a seal pup", "to explain how seals catch fish",
                      "to say when Pebble will come back", "to ask readers to give Pebble a new name"],
             "why": "The last paragraph gives advice for anyone who finds a pup: do not touch it, keep dogs back and call for help."},
        ],
    },
    {
        "key": "RD3.25",
        "year": 3,
        "strand": "Play scripts",
        "title": "The muddy footprints",
        "nc": "Prepare poems and play scripts to read aloud and to perform",
        "text": "MR DAVIES: Good morning, everyone. Hang up your coats, please.\n"
                "AISHA: (pointing at the floor) Mr Davies, look! There are muddy footprints all over the carpet!\n"
                "OSCAR: They go from the door right across to the reading corner.\n"
                "MR DAVIES: How strange. The room was spotless when I went home last night.\n"
                "JUN: (kneeling down) These aren't shoe prints. They're small and round, with four little toes each.\n"
                "AISHA: And there are short brown hairs on the big cushion.\n"
                "OSCAR: Maybe a fox got in!\n"
                "JUN: A fox couldn't get in. The doors were locked all night.\n"
                "MR DAVIES: Hmm. But Mrs Patel unlocks all the doors early every morning. Let's ask her.\n"
                "MRS PATEL: (rushing in, holding an empty lead) Sorry to interrupt. Has anyone seen a small brown dog? Biscuit slipped off her lead while I was opening up.\n"
                "AISHA: I think we've found her footprints!\n"
                "OSCAR: Listen. Something is snoring.\n"
                "JUN: (lifting the big cushion) Here she is, fast asleep.\n"
                "MRS PATEL: Biscuit! You naughty girl. I'm so sorry about the mess.\n"
                "MR DAVIES: Don't worry. We'll clean it up together. And Jun, well done for looking so carefully.\n"
                "OSCAR: Can Biscuit stay for the reading lesson?\n"
                "MR DAVIES: (laughing) Just this once.",
        "qs": [
            {"id": "2fe4a9ab75dc", "t": "mcq", "d": "retrieve", "q": "Where do the muddy footprints lead?",
             "opts": ["from the door to the reading corner", "from the coat pegs to the window",
                      "from the reading corner to Mr Davies's desk", "from the playground to the hall"],
             "why": "Oscar says the footprints go from the door right across to the reading corner."},
            {"id": "57b50da4eb8d", "t": "mcq", "d": "infer", "q": "Jun says the prints have “four little toes each”. What does this help the children work out?",
             "opts": ["An animal made them, not a person.", "Someone had walked in wearing wellies.",
                      "Mr Davies had left the door open.", "The mud came from the school field."],
             "why": "People's shoes do not leave small round prints with four toes, but an animal's paws do."},
            {"id": "201eddb09a3c", "t": "text", "d": "retrieve", "q": "Who unlocks all the doors early every morning? Find and copy the name.",
             "a": ["Mrs Patel", "Patel"],
             "why": "Mr Davies says that Mrs Patel unlocks all the doors early every morning."},
            {"id": "f9bcd0edf209", "t": "mcq", "d": "vocab", "q": "“Biscuit slipped off her lead.” What does this mean?",
             "opts": ["Biscuit got free from her lead.", "Biscuit fell over her lead.",
                      "Biscuit chewed through her lead.", "Biscuit carried her lead away."],
             "why": "Slipping off a lead means wriggling out of it and getting free. That is why Mrs Patel is holding an empty lead."},
            {"id": "12946992e00f", "t": "mcq", "d": "infer", "q": "Why does Mr Davies say “well done” to Jun?",
             "opts": ["Jun noticed the clues that solved the mystery.", "Jun cleaned the mud off the carpet.",
                      "Jun found Biscuit's lead in the corner.", "Jun hung up his coat straight away."],
             "why": "Jun spotted that the prints had toes, worked out a fox could not have got in at night, and lifted the cushion to find Biscuit."},
            {"id": "7e03b4f49498", "t": "mcq", "d": "structure", "q": "Why are some words in this play written in brackets?",
             "opts": ["They tell the actors what to do, not what to say.", "They are words the actors should shout.",
                      "They are words the audience says.", "They are the names of the characters."],
             "why": "Words in brackets, like “(kneeling down)”, are stage directions: actions for the actors, not lines to say."},
        ],
    },
    {
        "key": "RD3.26",
        "year": 3,
        "strand": "Information",
        "title": "Giant pandas",
        "nc": "Retrieve and record information from non-fiction",
        "text": "Giant pandas are bears with thick black and white fur. In the wild, they live only in cool, damp forests high in the mountains of China.\n\n"
                "Almost everything a panda eats is bamboo, a tall, tough kind of grass with hard, hollow stems. Bamboo is not very nourishing, so a panda has to eat a huge amount of it to stay healthy. It spends about half of every day eating, and much of the rest of the day resting, so that it does not use up too much energy.\n\n"
                "A panda's front paws are just right for holding bamboo. As well as five clawed toes, each front paw has a special bone in the wrist that works rather like a thumb. The panda uses it to grip a stem while it strips off the leaves with its strong teeth.\n\n"
                "Pandas are good climbers and can even swim, but they spend most of their time on the ground. Apart from a mother with her young cub, each panda lives on its own. Pandas rub their scent on trees to let other pandas know they are nearby.\n\n"
                "Not long ago, giant pandas were in danger of dying out, because people were cutting down the bamboo forests. Today, many of these forests are protected, and the number of wild pandas has slowly gone up.",
        "qs": [
            {"id": "b474abfbc960", "t": "mcq", "d": "retrieve", "q": "According to the text, where do giant pandas live in the wild?",
             "opts": ["in mountain forests in China", "in hot, dry deserts in China",
                      "on snowy plains in the far north", "in bamboo gardens all over the world"],
             "why": "The first paragraph says that in the wild they live only in cool, damp forests high in the mountains of China."},
            {"id": "f1a1926a83e0", "t": "mcq", "d": "vocab", "q": "“Bamboo is not very nourishing.” What does “nourishing” mean?",
             "opts": ["full of goodness that the body needs", "easy to chew and swallow",
                      "nice to taste", "quick to grow back"],
             "why": "Food that is nourishing gives the body what it needs. Bamboo has little goodness in it, so pandas must eat a huge amount."},
            {"id": "0b9d8943276c", "t": "tap", "d": "retrieve", "q": "Tap the word that names the part of the paw where the special bone is.",
             "s": "As well as five clawed toes, each front paw has a special bone in the [wrist] that works rather like a thumb.",
             "why": "The special bone is in the wrist. It is not a real thumb, but it works rather like one."},
            {"id": "ec10de64d19f", "t": "text", "d": "retrieve", "q": "What does the panda strip off the bamboo stem with its teeth? Find and copy the word.",
             "a": ["leaves", "the leaves"],
             "why": "The third paragraph says the panda grips a stem while it strips off the leaves with its strong teeth."},
            {"id": "11d77d7dc5d0", "t": "mcq", "d": "infer", "q": "Why did cutting down the bamboo forests put pandas in danger?",
             "opts": ["The pandas were losing the food they eat almost all the time.",
                      "The pandas had nowhere left to swim.",
                      "The pandas could not mark trees with their scent.",
                      "The pandas had to live together in big groups."],
             "why": "Almost everything a panda eats is bamboo, so losing the bamboo forests meant losing its food."},
            {"id": "40501af95246", "t": "mcq", "d": "summarise", "q": "What is the last paragraph mostly about?",
             "opts": ["how pandas nearly died out and are now doing a little better", "how pandas find enough bamboo to eat",
                      "how pandas use their scent to stay apart", "how a mother panda looks after her cub"],
             "why": "It says pandas were in danger of dying out, but now the forests are protected and their numbers have slowly gone up."},
        ],
    },
    {
        "key": "RD3.27",
        "year": 3,
        "strand": "Persuasive writing",
        "title": "Come to the toy swap!",
        "nc": "Identify how language, structure and presentation contribute to meaning",
        "text": "Have you got toys at home that you never play with any more? A jigsaw you have finished ten times? A game you have grown out of? Don't throw them away. Bring them to the Year 3 Toy Swap!\n\n"
                "Here is how it works. On Thursday morning, bring up to three toys, books or games to the school hall. They must be clean and in good condition, with no pieces missing. For each one, you will get a ticket. On Friday after school, the hall will be full of tables of toys, and you can swap each ticket for any toy you like.\n\n"
                "Why should you come? It is fair, because everyone who brings a toy gets to choose one. It is free, because you do not need any money at all. And it is kind to our planet. Many toys are made of plastic, which takes hundreds of years to break down. A toy that finds a new owner does not end up in a bin.\n\n"
                "Best of all, a toy that bores you could make someone else very happy. And their old toy might be just right for you!\n\n"
                "Any toys left over will go to the charity shop on Mill Street.\n\n"
                "So look under your bed tonight. Then come along, bring a friend, and swap!\n\n"
                "From Mrs Okafor and the Year 3 Green Team",
        "qs": [
            {"id": "4cfefd90dc5e", "t": "mcq", "d": "language", "q": "The text begins with three questions. Why?",
             "opts": ["to make readers think of their own unused toys", "to test how much readers know about toys",
                      "to find out who has the most toys", "to explain how the swap works"],
             "why": "Questions like “A game you have grown out of?” make each reader think about the toys at home they no longer play with."},
            {"id": "649e4f76cec7", "t": "mcq", "d": "vocab", "q": "“A game you have grown out of?” What does “grown out of” mean here?",
             "opts": ["become too old to enjoy", "become too big to fit inside",
                      "lost some of the pieces of", "played with too many times"],
             "why": "You grow out of a game when you get older and it no longer interests you."},
            {"id": "179e9799d075", "t": "mcq", "d": "retrieve", "q": "How many toys can each child bring?",
             "opts": ["up to three", "only one", "up to ten", "as many as they like"],
             "why": "The second paragraph says to bring up to three toys, books or games."},
            {"id": "f5b4b32dd2b4", "t": "tap", "d": "retrieve", "q": "Tap the word that names what you get for each toy you bring.",
             "s": "For each one, you will get a [ticket].",
             "why": "You get a ticket for each toy, and on Friday you swap each ticket for a toy."},
            {"id": "a0c6d015b041", "t": "mcq", "d": "infer", "q": "Why must the toys be clean and have no pieces missing?",
             "opts": ["so that another child will be glad to have them", "so that they fit on the tables in the hall",
                      "so that they can be sold for a lot of money", "so that they can go straight into a bin"],
             "why": "Each toy is going to a new owner, who will only be happy with a toy that is clean and complete."},
            {"id": "3ee0cf727d71", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to persuade children to bring toys to the swap", "to explain how plastic toys are made",
                      "to ask families to give money to a charity shop", "to tell a story about a lost toy"],
             "why": "It gives reasons to come, such as fair, free and kind to the planet, and ends by telling readers to come along and swap."},
        ],
    },
    {
        "key": "RD3.28",
        "year": 3,
        "strand": "Stories",
        "title": "Leila's first match",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": "Leila had used a wheelchair since she was a baby, and she could spin it round faster than anyone in her class. But when her cousin Sami asked her to try his wheelchair basketball club, her stomach did a somersault.\n\n"
                "“What if I can't even reach the hoop?” she asked.\n\n"
                "“Nobody can at first,” said Sami. “Just come and see.”\n\n"
                "The sports hall in Birmingham was loud with squeaking wheels and bouncing balls. The players used special chairs with slanted wheels, which made them easier to turn quickly. The coach, Mr Mensah, lent Leila one and explained the rules. You could push your wheels twice, and then you had to bounce or pass the ball.\n\n"
                "For the first half hour, nothing went in. Leila's arms ached, and her shots fell short again and again. She thought about going home.\n\n"
                "Then Mr Mensah crouched beside her. “Use your whole body, not just your arms,” he said. “Lean forward and push up from your shoulders.”\n\n"
                "Leila took a deep breath. She leaned forward and pushed, and the ball rose in a high curve. It hit the rim, wobbled for a moment and dropped through the net.\n\n"
                "Sami cheered so loudly that everyone turned round. Leila grinned. Her arms still ached, but she did not care.\n\n"
                "At the end of the session, she asked Mr Mensah just one question: “What time do you start next week?”",
        "qs": [
            {"id": "9ccd395b1b01", "t": "mcq", "d": "language", "q": "“Her stomach did a somersault.” What does this tell you about Leila?",
             "opts": ["She felt nervous.", "She felt hungry.", "She felt bored.", "She felt sleepy."],
             "why": "A somersault feeling in your tummy is a way of describing nerves. She was worried she could not reach the hoop."},
            {"id": "c7a23be8f972", "t": "mcq", "d": "retrieve", "q": "According to the text, why were the special chairs easier to turn quickly?",
             "opts": ["They had slanted wheels.", "They had a small motor.",
                      "They had brakes on the wheels.", "They had handles for pushing."],
             "why": "The fourth paragraph says the chairs had slanted wheels, which made them easier to turn quickly."},
            {"id": "382314f718f1", "t": "text", "d": "retrieve", "q": "How many times could a player push their wheels before bouncing or passing the ball? Find and copy one word.",
             "a": ["twice"],
             "why": "Mr Mensah explained that you could push your wheels twice, then you had to bounce or pass."},
            {"id": "929ec277e29e", "t": "mcq", "d": "infer", "q": "Why did Leila think about going home?",
             "opts": ["None of her shots had gone in.", "Sami had gone home without her.",
                      "The hall was too loud for her.", "Mr Mensah had told her off."],
             "why": "For half an hour nothing went in and her arms ached, so she felt like giving up."},
            {"id": "d10227bed85b", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Sami asked Leila to try his club.", "Mr Mensah lent Leila a chair.", "Leila's shots fell short.",
                       "Mr Mensah gave Leila some advice.", "The ball dropped through the net."],
             "why": "The story follows Leila's first visit: the invitation, the chair, the missed shots, the advice, then the basket."},
            {"id": "4bdd2e894039", "t": "mcq", "d": "infer", "q": "What does Leila's question at the end show?",
             "opts": ["She wants to come back next week.", "She wants to stop playing basketball.",
                      "She is worried about getting home.", "She wants to watch another team."],
             "why": "Asking what time they start next week shows she enjoyed it and means to return."},
        ],
    },
]
