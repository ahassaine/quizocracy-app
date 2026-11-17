"""Reading comprehension, Year 1 (keys RD1.xx).

Fourteen short original passages (30-80 words) for children aged 5-6, each with four questions in the
KS1 reading domains only (vocab, retrieve, sequence, infer, predict). Short sentences and decodable
everyday words, with a few common exception words (the, said, was, they, my, some, come). Questions are
mcq with three options, tap (a sentence copied exactly from the passage) and order (three events); no
typed answers in Year 1.

* Stories: RD1.01, RD1.03, RD1.06, RD1.10, RD1.12
* Information: RD1.02, RD1.05, RD1.09, RD1.11, RD1.13
* Instructions: RD1.07
* Poems: RD1.04
* Letters and diaries: RD1.08, RD1.14

Written by hand; to be reviewed line by line by a second reader (a teacher or a parent) before release.
"""

SKILLS = [
    {
        "key": "RD1.01",
        "year": 1,
        "strand": "Stories",
        "title": "The red kite",
        "nc": "Discuss events in a story and link what they read or hear to their own experiences",
        "text": "Sam had a red kite. It was windy, so Sam and Dad went up the hill.\n\n"
                "Dad held the kite. Sam held the string. “Let go!” said Sam. Up, up went the kite!\n\n"
                "Then the wind stopped. The kite fell into a tree. Sam was sad.\n\n"
                "Dad got a long stick. He poked the kite and it fell down. Sam grinned. "
                "“Can we go again?” he said.",
        "qs": [
            {"id": "81e7a14817b4", "t": "mcq", "d": "infer", "q": "Why did the kite fall into the tree?",
             "opts": ["The wind stopped.", "Sam let go of the string.", "Dad poked it with a stick."],
             "why": "The text says the wind stopped, and then the kite fell into a tree.",
             "no": {"Dad poked it with a stick.": "Dad poked it later, to get it out of the tree."}},
            {"id": "46a033aa90de", "t": "mcq", "d": "retrieve", "q": "Where did the kite fall?",
             "opts": ["into a tree", "into a pond", "onto a roof"],
             "why": "The third part says: the kite fell into a tree."},
            {"id": "6b76990d2779", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Dad held the kite.", "The kite fell into a tree.", "Dad got a long stick."],
             "why": "Dad held the kite first. Then the wind stopped and it fell. Then Dad got a stick to get it down."},
            {"id": "f42815ab0087", "t": "tap", "d": "vocab", "q": "Tap the word that means Sam gave a big smile.",
             "s": "Sam [grinned].",
             "why": "To grin is to give a big smile. Sam grinned when he got his kite back."},
        ],
    },
    {
        "key": "RD1.02",
        "year": 1,
        "strand": "Information",
        "title": "Hens",
        "nc": "Listen to and discuss non-fiction; retrieve information from a simple text",
        "text": "A hen is a bird. She has feathers and two legs. She has wings, but she cannot fly far.\n\n"
                "A hen pecks at the ground. She eats seeds, grass and bugs.\n\n"
                "A hen lays eggs in a nest. She sits on some of the eggs to keep them warm. "
                "After a time, chicks hatch out. A chick is small and fluffy.",
        "qs": [
            {"id": "b6793a1b753f", "t": "mcq", "d": "retrieve", "q": "What does the text say a hen cannot do?",
             "opts": ["fly far", "lay eggs", "peck at the ground"],
             "why": "The first part says: she has wings, but she cannot fly far."},
            {"id": "5023d06e04bc", "t": "mcq", "d": "vocab", "q": "A hen pecks at the ground. What does she do?",
             "opts": ["picks up food with her beak", "digs a hole with her feet", "sits down to sleep"],
             "why": "To peck is to pick at something with a beak. The hen pecks to get seeds, grass and bugs."},
            {"id": "6ea22aebaae8", "t": "mcq", "d": "retrieve", "q": "Why does a hen sit on her eggs?",
             "opts": ["to keep them warm", "to hide them from the chicks", "to crack them open"],
             "why": "The text says she sits on some of the eggs to keep them warm."},
            {"id": "320aa3ee4dd6", "t": "tap", "d": "vocab", "q": "Tap the word that tells you how a chick feels when you touch it.",
             "s": "A chick is small and [fluffy].",
             "why": "Fluffy means soft and light, like cotton wool. Small tells you its size, not how it feels."},
        ],
    },
    {
        "key": "RD1.03",
        "year": 1,
        "strand": "Stories",
        "title": "The lost sock",
        "nc": "Discuss the sequence of events in a story; make inferences on the basis of what is being said and done",
        "text": "It was time for school. Zara had one sock on. Where was the other one?\n\n"
                "She looked under the bed. No sock. She looked in the bath. No sock.\n\n"
                "Then she saw the dog, Rex. Rex was in his bed with something red in his mouth. It was the sock!\n\n"
                "Zara laughed. “Rex, you are a sock robber!” she said. "
                "She put on the sock, and it was a bit wet.",
        "qs": [
            {"id": "13d68b545a68", "t": "mcq", "d": "retrieve", "q": "Where did Zara look first?",
             "opts": ["under the bed", "in the bath", "in the dog's bed"],
             "why": "She looked under the bed first, then in the bath."},
            {"id": "719fb9766ee5", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Zara looked under the bed.", "Zara looked in the bath.", "Zara saw Rex with the sock."],
             "why": "Zara looked under the bed, then in the bath, and then she saw Rex with the sock."},
            {"id": "371f5c35f3b9", "t": "mcq", "d": "infer", "q": "Why was the sock wet?",
             "opts": ["Rex had it in his mouth.", "It fell in the bath.", "It was raining."],
             "why": "Rex had the sock in his mouth, so it got wet. The bath had no sock in it.",
             "no": {"It fell in the bath.": "Zara looked in the bath, and there was no sock there."}},
            {"id": "a81959afcd89", "t": "mcq", "d": "infer", "q": "How did Zara feel when she saw Rex with the sock?",
             "opts": ["She thought it was funny.", "She was cross with Rex.", "She was scared of Rex."],
             "why": "Zara laughed and called Rex a sock robber, so she thought it was funny."},
        ],
    },
    {
        "key": "RD1.04",
        "year": 1,
        "strand": "Poems",
        "title": "Puddles",
        "nc": "Learn to appreciate rhymes and poems; discuss word meanings",
        "text": "Drip, drop, rain on the street,\n"
                "Rain on my hat and rain on my feet.\n\n"
                "Splish, splash, I jump in a puddle,\n"
                "Mud on my coat, what a muddle!\n\n"
                "Then the sun peeps out one day,\n"
                "And dries the puddles all away.",
        "qs": [
            {"id": "e17a0377cd95", "t": "mcq", "d": "retrieve", "q": "In the first verse, where does the rain fall?",
             "opts": ["on my hat and my feet", "on the roof and the door", "on the grass and the trees"],
             "why": "The first verse says: rain on my hat and rain on my feet."},
            {"id": "6933a17d9901", "t": "tap", "d": "retrieve", "q": "Tap the word for the thing that gets mud on it.",
             "s": "Mud on my [coat], what a muddle!",
             "why": "The second verse says there is mud on my coat."},
            {"id": "402a6c33773e", "t": "mcq", "d": "vocab", "q": "What is a muddle?",
             "opts": ["a mess", "a big puddle", "a warm coat"],
             "why": "A muddle is a mess. The coat is muddy and messy after jumping in the puddle.",
             "no": {"a big puddle": "Muddle rhymes with puddle, but it means a mess."}},
            {"id": "3ad0ec66e64e", "t": "mcq", "d": "infer", "q": "What is the weather like in the last verse?",
             "opts": ["sunny", "rainy", "snowy"],
             "why": "The sun peeps out and dries the puddles, so it is sunny."},
        ],
    },
    {
        "key": "RD1.05",
        "year": 1,
        "strand": "Information",
        "title": "A bean seed grows",
        "nc": "Listen to and discuss non-fiction; discuss the sequence of events",
        "text": "A bean seed is small and hard. Plant it in soil and give it water.\n\n"
                "First, a root grows down into the soil. The root drinks up water.\n\n"
                "Next, a shoot grows up. It pushes out of the soil into the light.\n\n"
                "Then green leaves open. The plant needs light and water to grow big and strong.",
        "qs": [
            {"id": "48d5c42d7456", "t": "mcq", "d": "retrieve", "q": "What is a bean seed like?",
             "opts": ["small and hard", "big and soft", "green and flat"],
             "why": "The first sentence says a bean seed is small and hard."},
            {"id": "15a929ec7020", "t": "mcq", "d": "retrieve", "q": "Which way does the root grow?",
             "opts": ["down into the soil", "up into the light", "out of the leaves"],
             "why": "The text says the root grows down into the soil. The shoot is the part that grows up.",
             "no": {"up into the light": "That is the shoot. The root grows down."}},
            {"id": "eb8284e656d7", "t": "order", "d": "sequence", "q": "Put these in the order they happen.",
             "items": ["A root grows down.", "A shoot grows up.", "Green leaves open."],
             "why": "The text uses First, Next and Then: root, then shoot, then leaves."},
            {"id": "320500ceb335", "t": "mcq", "d": "predict", "q": "What will happen if the bean plant gets no water?",
             "opts": ["It will not grow big and strong.", "It will grow faster.", "It will grow more leaves."],
             "why": "The text says the plant needs light and water to grow big and strong."},
        ],
    },
    {
        "key": "RD1.06",
        "year": 1,
        "strand": "Stories",
        "title": "Jomo and the little goat",
        "nc": "Make inferences on the basis of what is being said and done",
        "text": "Jomo lives on a farm in Kenya. Every day, he takes the goats to eat grass.\n\n"
                "One day, the little goat ran off. Jomo looked and looked. "
                "Then he could hear “Maa, maa!” from the rocks.\n\n"
                "The little goat was stuck! Jomo went up the rocks and picked her up. "
                "He held her tight all the way home.\n\n"
                "“Well done,” said Mum. “You did not give up.”",
        "qs": [
            {"id": "c9fd7b6ada1b", "t": "mcq", "d": "retrieve", "q": "Where does Jomo live?",
             "opts": ["on a farm in Kenya", "in a town in Kenya", "on a farm in Wales"],
             "why": "The first sentence says Jomo lives on a farm in Kenya."},
            {"id": "96612b1beec7", "t": "mcq", "d": "infer", "q": "How did Jomo find the little goat?",
             "opts": ["He heard her call.", "Mum told him where she was.", "He saw her from the farm."],
             "why": "He could hear “Maa, maa!” from the rocks, so he followed the sound."},
            {"id": "86c955842925", "t": "tap", "d": "vocab", "q": "Tap the word that shows the goat could not get down.",
             "s": "The little goat was [stuck]!",
             "why": "Stuck means not able to move or get out."},
            {"id": "69126eaefc20", "t": "mcq", "d": "infer", "q": "What sort of boy is Jomo?",
             "opts": ["He keeps trying.", "He gets cross fast.", "He gives up fast."],
             "why": "He looked and looked, and Mum says he did not give up, so he keeps trying."},
        ],
    },
    {
        "key": "RD1.07",
        "year": 1,
        "strand": "Instructions",
        "title": "Make a jam sandwich",
        "nc": "Listen to and discuss non-fiction; read and follow simple instructions",
        "text": "You will need two slices of bread, butter, jam, a blunt knife and a plate. "
                "Ask a grown-up to help you.\n\n"
                "1. Put the bread on the plate.\n"
                "2. Spread butter on one side of each slice.\n"
                "3. Spread jam on top of the butter on one slice.\n"
                "4. Put the other slice on top, butter side down.\n"
                "5. Cut the sandwich in half. Now eat it!",
        "qs": [
            {"id": "107ca138a6d9", "t": "mcq", "d": "retrieve", "q": "How many slices of bread do you need?",
             "opts": ["two", "one", "three"],
             "why": "The first line says you need two slices of bread."},
            {"id": "7d54c6463f37", "t": "mcq", "d": "vocab", "q": "In step 2, what does spread mean?",
             "opts": ["put a thin layer all over", "cut into small bits", "drop in one big lump"],
             "why": "To spread butter is to make a thin layer of it all over the bread."},
            {"id": "fb4e3a202951", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Spread butter on the bread.", "Spread jam on the butter.", "Put the other slice on top."],
             "why": "Butter is step 2, jam is step 3 and the other slice goes on top in step 4."},
            {"id": "7beee1e5d112", "t": "mcq", "d": "retrieve", "q": "What do you do just before you eat the sandwich?",
             "opts": ["Cut it in half.", "Spread the jam.", "Put it on the plate."],
             "why": "Step 5 says: cut the sandwich in half. Now eat it!"},
        ],
    },
    {
        "key": "RD1.08",
        "year": 1,
        "strand": "Letters and diaries",
        "title": "Thank you, Gran",
        "nc": "Make inferences on the basis of what is being said and done; link reading to their own experiences",
        "text": "Dear Gran,\n\n"
                "Thank you for the green hat. It is soft and warm. I put it on to go to the park.\n\n"
                "It was so cold that the pond had ice on top. A duck stood on the ice! "
                "Then it slid along, and Dad and I laughed.\n\n"
                "My ears did not get cold at all, thanks to my hat.\n\n"
                "Lots of love,\nMia",
        "qs": [
            {"id": "27ee15dcb102", "t": "mcq", "d": "retrieve", "q": "What did Gran give Mia?",
             "opts": ["a green hat", "green gloves", "a red coat"],
             "why": "Mia says thank you for the green hat."},
            {"id": "4235ce6f1767", "t": "mcq", "d": "retrieve", "q": "Where did Mia go in her hat?",
             "opts": ["to the park", "to the beach", "to school"],
             "why": "Mia says she put the hat on to go to the park."},
            {"id": "702aabb07e55", "t": "mcq", "d": "infer", "q": "What made Mia and Dad laugh?",
             "opts": ["The duck slid on the ice.", "Mia's hat fell off.", "Dad fell on the ice."],
             "why": "The duck stood on the ice and slid along, and then they laughed."},
            {"id": "05008b85e5e5", "t": "mcq", "d": "infer", "q": "What does Mia think of her hat?",
             "opts": ["It is a good hat.", "It is too big.", "It is not warm."],
             "why": "She says it is soft and warm, and her ears did not get cold, so she likes it."},
        ],
    },
    {
        "key": "RD1.09",
        "year": 1,
        "strand": "Information",
        "title": "Ducks",
        "nc": "Listen to and discuss non-fiction; discuss word meanings, linking new meanings to those already known",
        "text": "A duck is a bird that can swim. Its feet are webbed. "
                "This means they have skin between the toes, so they push the water like paddles.\n\n"
                "A duck has oily feathers. The oil keeps the water off, so the duck stays dry.\n\n"
                "A mother duck lays eggs. Little ducks are called ducklings. "
                "They can swim soon after they hatch, and they follow their mum.",
        "qs": [
            {"id": "bae1b5131818", "t": "mcq", "d": "vocab", "q": "What are webbed feet?",
             "opts": ["feet with skin between the toes", "feet with long sharp claws", "feet with soft feathers"],
             "why": "The text says webbed means they have skin between the toes."},
            {"id": "c0bd1f763bb8", "t": "mcq", "d": "retrieve", "q": "What do a duck's webbed feet do?",
             "opts": ["They push the water.", "They keep the duck dry.", "They keep the eggs warm."],
             "why": "The text says the feet push the water like paddles. The oily feathers keep the duck dry.",
             "no": {"They keep the duck dry.": "That is what the oily feathers do."}},
            {"id": "10a6eb7b5568", "t": "mcq", "d": "retrieve", "q": "What keeps the water off a duck?",
             "opts": ["the oil on its feathers", "the skin on its feet", "its mum"],
             "why": "The second part says the oil keeps the water off."},
            {"id": "c84a87511bfc", "t": "tap", "d": "retrieve", "q": "Little ducks have a special name. Tap it.",
             "s": "Little ducks are called [ducklings].",
             "why": "Little ducks are called ducklings."},
        ],
    },
    {
        "key": "RD1.10",
        "year": 1,
        "strand": "Stories",
        "title": "Yusuf blows bubbles",
        "nc": "Make inferences on the basis of what is being said and done; predict what might happen",
        "text": "Yusuf was at the swimming pool with his class. "
                "He did not like to put his face in the water.\n\n"
                "“Blow bubbles,” said Miss Hall. Yusuf put his nose in. He came up fast and coughed.\n\n"
                "“Try again,” said Miss Hall. Yusuf held his breath. He put his face in and blew. "
                "Bubbles! Lots of bubbles!\n\n"
                "Yusuf came up with a big smile. “I did it!” he said.",
        "qs": [
            {"id": "f5dd82f55d21", "t": "mcq", "d": "retrieve", "q": "Where was Yusuf?",
             "opts": ["at the swimming pool", "at the beach", "in the bath"],
             "why": "The first sentence says Yusuf was at the swimming pool with his class."},
            {"id": "df8652ba52a4", "t": "mcq", "d": "infer", "q": "How did Yusuf feel at the start?",
             "opts": ["a bit scared", "very happy", "cross with Miss Hall"],
             "why": "He did not like to put his face in the water, so he felt a bit scared."},
            {"id": "805b05f08890", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Yusuf put his nose in.", "Miss Hall said, “Try again.”", "Yusuf blew lots of bubbles."],
             "why": "He put his nose in and coughed, Miss Hall said try again, and then he blew bubbles."},
            {"id": "bf7f44ff211e", "t": "mcq", "d": "predict", "q": "What will Yusuf most likely do next time?",
             "opts": ["put his face in again", "stay out of the pool", "say he will not try"],
             "why": "He did it and he was proud, so he will most likely put his face in again."},
        ],
    },
    {
        "key": "RD1.11",
        "year": 1,
        "strand": "Information",
        "title": "Winter",
        "nc": "Listen to and discuss non-fiction; discuss word meanings",
        "text": "Winter is the coldest season in the UK. The days are short and the nights are long. "
                "It gets dark before tea time.\n\n"
                "Some trees lose their leaves. Their branches look bare.\n\n"
                "Some days, it snows. People wear coats, hats and gloves to keep warm.\n\n"
                "Birds can find it hard to get food. You can help them by putting out seeds.",
        "qs": [
            {"id": "f8365c5aa0eb", "t": "mcq", "d": "retrieve", "q": "What are the days like in winter?",
             "opts": ["short", "long", "hot"],
             "why": "The text says the days are short and the nights are long.",
             "no": {"long": "It is the nights that are long in winter."}},
            {"id": "aa46a4b72fc1", "t": "mcq", "d": "infer", "q": "Why does it get dark before tea time?",
             "opts": ["The days are short.", "It snows a lot.", "The trees lose their leaves."],
             "why": "In winter the days are short, so it gets dark early."},
            {"id": "f1aa6da263d8", "t": "mcq", "d": "vocab", "q": "The branches look bare. What does bare mean here?",
             "opts": ["with no leaves", "with lots of snow", "with lots of birds"],
             "why": "The trees have lost their leaves, so the branches are bare: they have nothing on them."},
            {"id": "0b2e01c1376d", "t": "mcq", "d": "retrieve", "q": "What does the text say you can do to help birds?",
             "opts": ["put out seeds", "give them hats", "keep them inside"],
             "why": "The last part says you can help them by putting out seeds."},
        ],
    },
    {
        "key": "RD1.12",
        "year": 1,
        "strand": "Stories",
        "title": "A new friend",
        "nc": "Make inferences on the basis of what is being said and done",
        "text": "Lin was new at school. She did not know anyone. "
                "At play time, she stood by the wall on her own.\n\n"
                "Priya saw her. “Do you want to play hopscotch?” she said.\n\n"
                "Lin did not know the game. Priya showed her how to hop on one foot. "
                "Lin hopped and jumped, and she did not fall.\n\n"
                "When the bell rang, Lin and Priya went in hand in hand.",
        "qs": [
            {"id": "6952af86ce65", "t": "mcq", "d": "retrieve", "q": "Where did Lin stand at play time?",
             "opts": ["by the wall", "by the gate", "in the classroom"],
             "why": "The text says she stood by the wall on her own."},
            {"id": "19280a54abe8", "t": "mcq", "d": "infer", "q": "How did Lin feel at the start of play time?",
             "opts": ["lonely", "excited", "cross"],
             "why": "She was new, did not know anyone and stood on her own, so she felt lonely."},
            {"id": "58176c9986ea", "t": "mcq", "d": "retrieve", "q": "What game did Priya teach Lin?",
             "opts": ["hopscotch", "tag", "football"],
             "why": "Priya asked, “Do you want to play hopscotch?”"},
            {"id": "53caad796fd4", "t": "mcq", "d": "infer", "q": "How do we know the girls are friends at the end?",
             "opts": ["They go in holding hands.", "They both stand by the wall.", "Lin does not fall."],
             "why": "They went in hand in hand, which friends do."},
        ],
    },
    {
        "key": "RD1.13",
        "year": 1,
        "strand": "Information",
        "title": "Your senses",
        "nc": "Listen to and discuss non-fiction; retrieve information from a simple text",
        "text": "You have five senses. They help you find out about the world.\n\n"
                "You see with your eyes. You hear with your ears. You smell with your nose. "
                "You taste with your tongue. You feel with your skin.\n\n"
                "Your senses can keep you safe. Your nose can smell smoke. "
                "Your ears can hear a car coming, so you can wait before you cross the road.",
        "qs": [
            {"id": "1e8c2e71fa94", "t": "mcq", "d": "vocab", "q": "In this text, what are senses?",
             "opts": ["ways to find out about the world", "bones that hold you up", "foods that keep you well"],
             "why": "The first part says senses help you find out about the world."},
            {"id": "798c9c2aec2b", "t": "mcq", "d": "retrieve", "q": "What does the text say your senses can do?",
             "opts": ["keep you safe", "make you tall", "help you sleep"],
             "why": "The last part says: your senses can keep you safe."},
            {"id": "3095e3a6f943", "t": "tap", "d": "retrieve", "q": "Tap the word for what your nose can smell to keep you safe.",
             "s": "Your nose can smell [smoke].",
             "why": "The text says your nose can smell smoke, so you know there may be a fire."},
            {"id": "414503f35109", "t": "mcq", "d": "retrieve", "q": "Why is it good that you can hear a car coming?",
             "opts": ["You know to wait before you cross.", "You can see the car better.", "You can wave to the driver."],
             "why": "The text says your ears hear a car coming, so you can wait before you cross the road."},
        ],
    },
    {
        "key": "RD1.14",
        "year": 1,
        "strand": "Letters and diaries",
        "title": "Kofi's diary",
        "nc": "Discuss the sequence of events; make inferences on the basis of what is being said and done",
        "text": "Saturday\n\n"
                "Today we went to the beach in Wales. The sand was wet and cold under my feet.\n\n"
                "First, Mum and I made a big sandcastle. Then the sea came in and the waves washed it away. "
                "I was a bit sad.\n\n"
                "After that, I found a crab in a rock pool. It ran sideways under a rock.\n\n"
                "We had chips for tea. It was the best day!",
        "qs": [
            {"id": "12ee8389f8fa", "t": "mcq", "d": "retrieve", "q": "Where did Kofi go?",
             "opts": ["to the beach in Wales", "to a beach in Spain", "to a park in Wales"],
             "why": "The diary says: today we went to the beach in Wales."},
            {"id": "3bb7d29f01f8", "t": "order", "d": "sequence", "q": "Put these in the order they happen.",
             "items": ["Kofi and Mum made a sandcastle.", "The waves washed it away.", "Kofi found a crab."],
             "why": "The diary uses First, Then and After that: sandcastle, waves, then the crab."},
            {"id": "67f6f7d557a9", "t": "mcq", "d": "infer", "q": "Why was Kofi a bit sad?",
             "opts": ["The sea washed away his sandcastle.", "The sand was wet and cold.", "The crab ran away."],
             "why": "He was sad just after the waves washed the sandcastle away."},
            {"id": "5f133107d76f", "t": "tap", "d": "vocab", "q": "Tap the word that tells you which way the crab ran.",
             "s": "It ran [sideways] under a rock.",
             "why": "Sideways means to the side, not forwards. Crabs often walk sideways."},
        ],
    },
]
