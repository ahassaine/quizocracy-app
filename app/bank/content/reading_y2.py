"""Reading comprehension, Year 2 (keys RD2.xx).

Fourteen original passages (80-160 words) for children aged 6-7, each with five questions in the KS1
reading domains only (vocab, retrieve, sequence, infer, predict). Questions are mcq with three options,
tap (a sentence copied exactly from the passage), order (3-4 events) and, in a few passages, text
(find and copy one word).

* Stories: RD2.01, RD2.03, RD2.07, RD2.11, RD2.14
* Information: RD2.02, RD2.04, RD2.08, RD2.10, RD2.12
* Instructions: RD2.06
* Poems: RD2.05
* Letters and diaries: RD2.09, RD2.13

Written by hand; to be reviewed line by line by a second reader (a teacher or a parent) before release.
"""

SKILLS = [
    {
        "key": "RD2.01",
        "year": 2,
        "strand": "Stories",
        "title": "Hammy comes home",
        "nc": "Make inferences on the basis of what is being said and done; answer and ask questions",
        "text": "On Friday, Miss Okafor picked Ravi to take Hammy, the class hamster, home for the weekend. "
                "Ravi was so proud that he carried the cage very carefully all the way to the car.\n\n"
                "At home, Ravi gave Hammy fresh water, seeds and a slice of carrot. "
                "Hammy stuffed the food into his cheeks until they were fat and round.\n\n"
                "On Saturday morning, the cage was empty! Ravi looked under the sofa and behind the books. "
                "At last, his sister Anya found Hammy fast asleep inside one of Dad's slippers.\n\n"
                "Dad looked at the cage. “The little door was not shut,” he said. "
                "From then on, Ravi checked the door twice every time he closed it.\n\n"
                "On Monday, Ravi took Hammy back to class. He told everyone about the slipper, and they all laughed.",
        "qs": [
            {"id": "d465f0e5d7d0", "t": "mcq", "d": "retrieve", "q": "Who picked Ravi to take Hammy home?",
             "opts": ["Miss Okafor", "Dad", "Anya"],
             "why": "The first sentence says Miss Okafor picked Ravi."},
            {"id": "7fd2506ec4ab", "t": "tap", "d": "vocab", "q": "Tap the word that shows Hammy pushed in lots of food.",
             "s": "Hammy [stuffed] the food into his cheeks until they were fat and round.",
             "why": "To stuff is to push in as much as you can. Hammy filled his cheeks until they were fat."},
            {"id": "42e862bd6984", "t": "mcq", "d": "retrieve", "q": "Where was Hammy found?",
             "opts": ["in Dad's slipper", "under the sofa", "behind the books"],
             "why": "Anya found him asleep inside one of Dad's slippers. Ravi had already looked under the sofa and behind the books.",
             "no": {"under the sofa": "Ravi looked under the sofa, but Hammy was not there."}},
            {"id": "fe02d99a28a4", "t": "mcq", "d": "infer", "q": "How did Hammy get out of his cage?",
             "opts": ["The door had been left open.", "Anya let him out to play.", "The cage broke in the car."],
             "why": "Dad saw that the little door was not shut, so Hammy walked out."},
            {"id": "da3f0ae67e54", "t": "mcq", "d": "infer", "q": "Why did Ravi check the door twice from then on?",
             "opts": ["He did not want Hammy to get out.", "Miss Okafor had told him to.", "He thought the door was broken."],
             "why": "Hammy got out because the door was not shut, and Ravi did not want that to happen again."},
        ],
    },
    {
        "key": "RD2.02",
        "year": 2,
        "strand": "Information",
        "title": "From frogspawn to frog",
        "nc": "Discuss the sequence of events in non-fiction; discuss and clarify the meanings of words",
        "text": "In spring, a mother frog lays her eggs in a pond. The eggs are inside a clear jelly "
                "that keeps them safe. A big clump of these eggs is called frogspawn.\n\n"
                "After a while, tiny tadpoles wriggle out. A tadpole has a long tail for swimming but no legs. "
                "It breathes under water and eats tiny plants.\n\n"
                "Slowly, the tadpole changes. First it grows back legs, and then front legs. "
                "Its tail gets shorter and shorter. Now it is called a froglet.\n\n"
                "At last, the young frog climbs out of the pond. It can breathe air and hop on land. "
                "It eats insects and slugs. When it is grown up, it will come back to a pond in spring.",
        "qs": [
            {"id": "ac9aa6be927c", "t": "text", "d": "vocab", "q": "Find and copy the word that means a big clump of frog eggs.",
             "a": ["frogspawn", "the frogspawn"],
             "why": "The first part says a big clump of these eggs is called frogspawn."},
            {"id": "448b6a2f1197", "t": "mcq", "d": "retrieve", "q": "What does the jelly do for the eggs?",
             "opts": ["It keeps them safe.", "It is food for the frog.", "It helps them hop."],
             "why": "The text says the eggs are inside a clear jelly that keeps them safe."},
            {"id": "ca7930effc6f", "t": "mcq", "d": "vocab", "q": "The tadpoles wriggle out. How do they move?",
             "opts": ["They twist and wiggle.", "They jump up high.", "They walk on their legs."],
             "why": "To wriggle is to twist and wiggle your body. Tadpoles have no legs yet.",
             "no": {"They walk on their legs.": "A new tadpole has no legs at all."}},
            {"id": "417329077ad3", "t": "order", "d": "sequence", "q": "Put these in the order they happen.",
             "items": ["Tiny tadpoles wriggle out of the eggs.", "The tadpole grows back legs.",
                       "The tadpole grows front legs.", "The young frog climbs out of the pond."],
             "why": "The text says first back legs, then front legs, and at last the frog climbs out."},
            {"id": "c7837c3e3e71", "t": "mcq", "d": "retrieve", "q": "What does a young frog eat?",
             "opts": ["insects and slugs", "tiny plants", "the clear jelly"],
             "why": "The last part says the young frog eats insects and slugs. Tiny plants are what a tadpole eats.",
             "no": {"tiny plants": "That is what a tadpole eats, in the second part."}},
        ],
    },
    {
        "key": "RD2.03",
        "year": 2,
        "strand": "Stories",
        "title": "Oranges at the market",
        "nc": "Discuss the sequence of events; make inferences on the basis of what is being said and done",
        "text": "Every Saturday, Amina helps her grandad at his fruit stall in the market in Marrakech. "
                "The stall is piled high with oranges, lemons and figs.\n\n"
                "Amina's job is to put the oranges into paper bags. She counts six into each bag.\n\n"
                "One day at midday, the market was busy and noisy. An old man bumped into a cart, "
                "and his bag split. Oranges rolled everywhere, under feet and between the stalls.\n\n"
                "Amina ran out from behind the stall. She picked up every orange she could find "
                "and gave them back to him in a new bag.\n\n"
                "The old man smiled. “Thank you, little one,” he said.\n\n"
                "Grandad patted Amina on the shoulder. Then he gave her the biggest, juiciest fig on the stall.",
        "qs": [
            {"id": "ab39cd9c033f", "t": "mcq", "d": "retrieve", "q": "Where is Grandad's fruit stall?",
             "opts": ["in the market in Marrakech", "in a shop by the sea", "outside Amina's school"],
             "why": "The first sentence says the stall is in the market in Marrakech."},
            {"id": "01004c136b62", "t": "text", "d": "retrieve", "q": "How many oranges does Amina put in each bag? Find and copy the word.",
             "a": ["six", "6"],
             "why": "The text says she counts six into each bag."},
            {"id": "31c5f8ef1dd0", "t": "mcq", "d": "vocab", "q": "The old man's bag split. What does split mean here?",
             "opts": ["tore open", "got very heavy", "fell over"],
             "why": "The bag tore open, so the oranges rolled out everywhere."},
            {"id": "cc1c1adf8db0", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["The old man bumped into a cart.", "Oranges rolled everywhere.",
                       "Amina picked up the oranges.", "The old man said thank you."],
             "why": "He bumped into a cart, the bag split, the oranges rolled, Amina picked them up, and he thanked her."},
            {"id": "e6f223c3f0d9", "t": "mcq", "d": "infer", "q": "How did Grandad feel about what Amina did?",
             "opts": ["pleased with her", "cross that she left the stall", "worried about the oranges"],
             "why": "He patted her on the shoulder and gave her the best fig, which shows he was pleased.",
             "no": {"cross that she left the stall": "He patted her and gave her a fig: that is not what a cross person does."}},
        ],
    },
    {
        "key": "RD2.04",
        "year": 2,
        "strand": "Information",
        "title": "What is it made of?",
        "nc": "Listen to, discuss and express views about non-fiction; retrieve information",
        "text": "Everything around you is made of a material. Wood, metal, glass and fabric are all materials.\n\n"
                "Wood comes from trees. It is strong and hard, so we use it to make tables, chairs and doors.\n\n"
                "Metal is strong too. It is shiny, and it can bend without snapping. "
                "Spoons, keys and pans are made of metal.\n\n"
                "Glass is hard and you can see through it. That is why windows are made of glass. "
                "But be careful: glass can break.\n\n"
                "Fabric is soft and it bends easily. We use it to make clothes, towels and curtains.\n\n"
                "When you make something, pick the right material for the job. A chocolate teapot would melt!",
        "qs": [
            {"id": "39d4722873ac", "t": "mcq", "d": "retrieve", "q": "Which things does the text say are made of metal?",
             "opts": ["spoons, keys and pans", "tables, chairs and doors", "clothes, towels and curtains"],
             "why": "The metal part says spoons, keys and pans are made of metal."},
            {"id": "15513168a60f", "t": "mcq", "d": "retrieve", "q": "Why are windows made of glass, as the text says?",
             "opts": ["You can see through it.", "It is soft and bends.", "It is shiny and bends."],
             "why": "The text says glass is hard and you can see through it. That is why windows are made of glass."},
            {"id": "af553d21cf8f", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what glass can do if you are not careful.",
             "s": "But be careful: glass can [break].",
             "why": "The text warns that glass can break."},
            {"id": "326bc4bc4e58", "t": "tap", "d": "vocab", "q": "Tap the word that tells you how fabric feels to touch.",
             "s": "Fabric is [soft] and it bends easily.",
             "why": "Soft tells you how fabric feels. Bends tells you what it does."},
            {"id": "d8f288dd6c61", "t": "mcq", "d": "infer", "q": "Why would a chocolate teapot be no good?",
             "opts": ["Hot tea would melt it.", "You could see through it.", "It would be too hard."],
             "why": "The text says it would melt. Hot tea would make the chocolate go soft and runny."},
        ],
    },
    {
        "key": "RD2.05",
        "year": 2,
        "strand": "Poems",
        "title": "The wind",
        "nc": "Continue to build up a repertoire of poems; discuss favourite words and phrases",
        "text": "I cannot see the wind at all,\n"
                "But I can hear it whoosh and call.\n"
                "It rattles windows, bangs the door,\n"
                "And whistles round the house once more.\n\n"
                "I see it push the clouds along,\n"
                "And bend the trees so tall and strong.\n"
                "It snatches hats and blows them high,\n"
                "And chases leaves across the sky.\n\n"
                "It flaps the washing on the line\n"
                "And dries it all in half the time.\n"
                "So though the wind is hard to find,\n"
                "It always leaves its marks behind.",
        "qs": [
            {"id": "d65be16baec1", "t": "mcq", "d": "retrieve", "q": "In the first verse, how does the poet know the wind is there?",
             "opts": ["They can hear it.", "They can see it.", "They can smell it."],
             "why": "The first verse says: I cannot see the wind at all, but I can hear it.",
             "no": {"They can see it.": "The first line says: I cannot see the wind at all."}},
            {"id": "289571d2bc50", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what the wind does to the windows.",
             "s": "It [rattles] windows, bangs the door,",
             "why": "The wind rattles the windows and bangs the door."},
            {"id": "29c507844028", "t": "mcq", "d": "vocab", "q": "The wind snatches hats. What does snatches mean?",
             "opts": ["grabs quickly", "makes wet", "folds up"],
             "why": "To snatch is to grab something quickly. The wind grabs the hats and blows them high."},
            {"id": "a360bc575be0", "t": "mcq", "d": "infer", "q": "What are the marks the wind leaves behind?",
             "opts": ["the things it has moved", "puddles of rain", "lines in the sky"],
             "why": "You cannot see the wind, but you can see the hats, leaves, trees and washing it has moved."},
            {"id": "2bf1434a78aa", "t": "mcq", "d": "infer", "q": "Which words best describe the wind in this poem?",
             "opts": ["busy and strong", "soft and quiet", "slow and sleepy"],
             "why": "It rattles, bangs, bends trees and chases leaves: it is busy and strong."},
        ],
    },
    {
        "key": "RD2.06",
        "year": 2,
        "strand": "Instructions",
        "title": "How to wash your hands",
        "nc": "Read and follow instructions; discuss the sequence of steps",
        "text": "Washing your hands gets rid of germs that can make you ill. "
                "Wash them after you use the toilet, after you play outside and before you eat.\n\n"
                "1. Wet your hands with clean water.\n"
                "2. Put on some soap.\n"
                "3. Rub your palms together.\n"
                "4. Rub the backs of your hands and in between your fingers.\n"
                "5. Keep rubbing for about 20 seconds. You could hum a short song twice while you do it.\n"
                "6. Rinse off all the soap with water.\n"
                "7. Dry your hands on a clean towel.\n\n"
                "Now your hands are clean and ready!",
        "qs": [
            {"id": "3c5c8fc4f9f9", "t": "mcq", "d": "retrieve", "q": "Which is one time the text says to wash your hands?",
             "opts": ["after you play outside", "before you go to bed", "after you read a book"],
             "why": "The first part says after the toilet, after you play outside and before you eat."},
            {"id": "99730122dd22", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Wet your hands.", "Put on some soap.", "Rinse off the soap.", "Dry your hands."],
             "why": "Steps 1, 2, 6 and 7: wet, soap, rinse, dry."},
            {"id": "383c3bacd237", "t": "text", "d": "retrieve", "q": "For how many seconds should you keep rubbing? Find and copy the number.",
             "a": ["20", "twenty", "about 20"],
             "why": "Step 5 says keep rubbing for about 20 seconds."},
            {"id": "3e620ec1532d", "t": "mcq", "d": "vocab", "q": "In step 6, what does rinse mean?",
             "opts": ["wash off with water", "rub very hard", "dry with a towel"],
             "why": "To rinse is to wash something off with water. Drying comes next, in step 7."},
            {"id": "e60124d980b1", "t": "mcq", "d": "infer", "q": "Why does the text say you could hum a short song twice?",
             "opts": ["to know how long to rub", "to make more bubbles", "to make your hands dry"],
             "why": "Humming the song twice takes about 20 seconds, so you know when to stop rubbing."},
        ],
    },
    {
        "key": "RD2.07",
        "year": 2,
        "strand": "Stories",
        "title": "Leo's wobbly bike",
        "nc": "Make inferences on the basis of what is being said and done; predict what might happen",
        "text": "Leo had a new bike, but it had no little side wheels. Every time he tried to ride it, "
                "it wobbled and he put his feet down.\n\n"
                "“I can't do it,” said Leo, and he pushed the bike away.\n\n"
                "His big sister Nia picked it up. “I fell off lots of times when I was learning,” she said. "
                "“Look straight ahead, not at your feet. I will hold the seat.”\n\n"
                "Leo pushed the pedals. Nia ran beside him, holding on. Then, without saying a word, she let go.\n\n"
                "Leo rode all the way to the big oak tree on his own. When he looked back, "
                "Nia was far behind him, clapping.\n\n"
                "“You let go!” Leo shouted. He wobbled, put his feet down and laughed.",
        "qs": [
            {"id": "95df2ea25dcf", "t": "mcq", "d": "retrieve", "q": "What did Leo do when he said he could not do it?",
             "opts": ["He pushed the bike away.", "He ran inside.", "He asked for side wheels."],
             "why": "The text says: “I can't do it,” said Leo, and he pushed the bike away."},
            {"id": "74941aeb3e2a", "t": "mcq", "d": "infer", "q": "Why did Nia tell Leo that she fell off lots of times?",
             "opts": ["to show him everyone falls when they learn", "to make him laugh at her",
                      "to tell him bikes are not safe"],
             "why": "She wanted Leo to know that falling is part of learning, so he would try again."},
            {"id": "0042c6e424ae", "t": "mcq", "d": "retrieve", "q": "Where did Nia tell Leo to look?",
             "opts": ["straight ahead", "at his feet", "back at her"],
             "why": "Nia said: look straight ahead, not at your feet.",
             "no": {"at his feet": "Nia said not to look at his feet."}},
            {"id": "df5226052992", "t": "mcq", "d": "infer", "q": "How did Leo feel when he saw Nia far behind him?",
             "opts": ["surprised and happy", "cross and sad", "scared and lost"],
             "why": "He did not know she had let go, so he was surprised, and he laughed, so he was happy."},
            {"id": "23cce7f39a26", "t": "mcq", "d": "predict", "q": "What will Leo most likely do next?",
             "opts": ["try to ride again", "give his bike away", "never ride again"],
             "why": "He has just ridden on his own and he is laughing, so he will most likely try again."},
        ],
    },
    {
        "key": "RD2.08",
        "year": 2,
        "strand": "Information",
        "title": "From cow to cup",
        "nc": "Listen to, discuss and express views about non-fiction; discuss the sequence of events",
        "text": "Milk comes from cows that live on dairy farms. In spring and summer, the cows eat fresh grass "
                "in the fields. In winter, they often stay in a barn and eat hay.\n\n"
                "Most dairy cows are milked twice a day, in the morning and in the evening. "
                "Today, farmers use milking machines. The machine gently sucks the milk from the cow's udder.\n\n"
                "The milk goes into a big cold tank to keep it fresh. A lorry collects it and takes it to a dairy. "
                "There, it is heated to kill germs and then put into bottles and cartons.\n\n"
                "Milk can also be made into butter, cheese and yoghurt. So next time you pour milk "
                "on your breakfast, think of the cows and the farmer!",
        "qs": [
            {"id": "aa3bc777aca5", "t": "mcq", "d": "retrieve", "q": "What do the cows often eat in winter?",
             "opts": ["hay", "fresh grass", "cheese"],
             "why": "The first part says in winter they often stay in a barn and eat hay.",
             "no": {"fresh grass": "They eat fresh grass in spring and summer."}},
            {"id": "0e996e2bf064", "t": "mcq", "d": "retrieve", "q": "How often are most dairy cows milked?",
             "opts": ["twice a day", "once a day", "once a week"],
             "why": "The text says most dairy cows are milked twice a day, in the morning and in the evening."},
            {"id": "6e0b849d2253", "t": "mcq", "d": "vocab", "q": "What is a cow's udder?",
             "opts": ["the part the milk comes from", "the machine that milks it", "the tank that keeps milk cold"],
             "why": "The machine sucks the milk from the udder, so the udder is the part of the cow the milk comes from."},
            {"id": "647bbdd73e6a", "t": "order", "d": "sequence", "q": "Put these in the order they happen to the milk.",
             "items": ["A machine milks the cow.", "The milk goes into a cold tank.",
                       "A lorry takes it to a dairy.", "The milk is put into bottles."],
             "why": "Milked, then the cold tank, then the lorry to the dairy, where it is heated and bottled."},
            {"id": "fa488bae5f70", "t": "mcq", "d": "retrieve", "q": "What does the text say milk can be made into?",
             "opts": ["butter, cheese and yoghurt", "bread, butter and jam", "hay, cheese and grass"],
             "why": "The last part says milk can be made into butter, cheese and yoghurt."},
        ],
    },
    {
        "key": "RD2.09",
        "year": 2,
        "strand": "Letters and diaries",
        "title": "A letter from Osaka",
        "nc": "Make inferences on the basis of what is being said and done; answer and ask questions",
        "text": "Dear Ellie,\n\n"
                "Thank you for your letter about your school in Leeds. Now I will tell you about my school in Osaka.\n\n"
                "I walk to school with my friends. When we arrive, we take off our outdoor shoes "
                "and put on indoor shoes.\n\n"
                "At lunch time, we do not go to a dining hall. We eat in our classroom! Some children wear "
                "white hats and aprons and serve the food to everyone. Today it was rice, fish and soup.\n\n"
                "After lunch, we all clean our classroom. We sweep the floor and wipe the desks. "
                "I like cleaning with my friends, because we chat and laugh.\n\n"
                "What do you do after lunch at your school? Please write back soon.\n\n"
                "Your friend,\nHana",
        "qs": [
            {"id": "4ad80f89b871", "t": "mcq", "d": "retrieve", "q": "Where is Ellie's school?",
             "opts": ["Leeds", "Osaka", "London"],
             "why": "Hana thanks Ellie for her letter about her school in Leeds. Osaka is where Hana's school is.",
             "no": {"Osaka": "Osaka is where Hana goes to school, not Ellie."}},
            {"id": "fa30a9909c94", "t": "mcq", "d": "retrieve", "q": "What do the children do when they arrive at school?",
             "opts": ["change their shoes", "eat their lunch", "sweep the floor"],
             "why": "They take off their outdoor shoes and put on indoor shoes."},
            {"id": "d27aba8ca9ef", "t": "mcq", "d": "retrieve", "q": "Where do Hana and her class eat lunch?",
             "opts": ["in their classroom", "in the dining hall", "outside in the playground"],
             "why": "Hana says they do not go to a dining hall: they eat in their classroom.",
             "no": {"in the dining hall": "Hana says they do not go to a dining hall."}},
            {"id": "2fce053b0fc5", "t": "mcq", "d": "infer", "q": "How does Hana feel about cleaning the classroom?",
             "opts": ["She enjoys it.", "She thinks it is boring.", "She does it on her own."],
             "why": "She chats and laughs with her friends while she cleans, so she enjoys it."},
            {"id": "a653283d0815", "t": "mcq", "d": "infer", "q": "Why does Hana ask Ellie a question at the end?",
             "opts": ["She wants Ellie to tell her more.", "She wants to visit Leeds.", "She forgot what Ellie said."],
             "why": "Hana asks about Ellie's school and says please write back, so she wants Ellie to tell her more."},
        ],
    },
    {
        "key": "RD2.10",
        "year": 2,
        "strand": "Information",
        "title": "Your busy heart",
        "nc": "Listen to, discuss and express views about non-fiction; discuss and clarify the meanings of words",
        "text": "Your heart is a muscle in your chest. It is about the size of your fist.\n\n"
                "Your heart works like a pump. Every time it beats, it pushes blood all around your body "
                "through tubes called blood vessels. The blood carries food and oxygen to every part of you.\n\n"
                "Put your hand on your chest and keep very still. Can you feel a beat?\n\n"
                "When you run, jump or dance, your heart beats faster. This is because your muscles need more oxygen. "
                "When you rest, it slows down again.\n\n"
                "Exercise makes your heart stronger. Try to be active every day: walk, swim, skip or play outside. "
                "Your heart never stops working, even when you are asleep!",
        "qs": [
            {"id": "6936443b20ef", "t": "mcq", "d": "retrieve", "q": "How big is your heart, as the text says?",
             "opts": ["about the size of your fist", "about the size of your head", "about the size of a pea"],
             "why": "The first part says it is about the size of your fist."},
            {"id": "c0f3545e6d63", "t": "mcq", "d": "vocab", "q": "What are blood vessels?",
             "opts": ["tubes that blood goes through", "muscles in your chest", "the beats of your heart"],
             "why": "The text says blood goes around your body through tubes called blood vessels."},
            {"id": "f9fc8b4cedb2", "t": "mcq", "d": "retrieve", "q": "What does the blood carry to every part of you?",
             "opts": ["food and oxygen", "water and air", "muscles and bones"],
             "why": "The text says the blood carries food and oxygen to every part of you."},
            {"id": "87d491f0b92d", "t": "mcq", "d": "infer", "q": "Ana has just run a race. What is her heart doing?",
             "opts": ["beating faster", "slowing down", "beating more softly"],
             "why": "The text says your heart beats faster when you run."},
            {"id": "1ade8f355d94", "t": "mcq", "d": "vocab", "q": "Try to be active every day. What does active mean?",
             "opts": ["moving about", "sitting still", "sleeping well"],
             "why": "Being active means moving about: walking, swimming, skipping or playing."},
        ],
    },
    {
        "key": "RD2.11",
        "year": 2,
        "strand": "Stories",
        "title": "Noor's cake",
        "nc": "Make inferences on the basis of what is being said and done; discuss the sequence of events",
        "text": "It was Mum's birthday, and Noor wanted to make her a cake. Dad found a recipe, "
                "and they put on their aprons.\n\n"
                "Noor cracked the eggs into a bowl. She stirred in the butter and the flour. "
                "Dad put the cake in the oven, and soon the kitchen smelled lovely.\n\n"
                "When the cake was cool, Noor cut a slice to try. She took a bite and pulled a face.\n\n"
                "Dad looked at the recipe. “Oh no,” he said. “We forgot the sugar!”\n\n"
                "Noor felt like crying. Then she took a deep breath. “There is still time,” she said. "
                "“Let's make another one.”\n\n"
                "This time, Noor ticked off each thing on the recipe as she used it. "
                "When Mum came home, there was a sweet cake waiting for her.",
        "qs": [
            {"id": "b833577977ee", "t": "mcq", "d": "retrieve", "q": "Why did Noor want to make a cake?",
             "opts": ["It was Mum's birthday.", "It was Dad's birthday.", "It was for a school sale."],
             "why": "The first sentence says it was Mum's birthday."},
            {"id": "1d54662d3961", "t": "mcq", "d": "infer", "q": "Why did Noor pull a face?",
             "opts": ["The cake did not taste nice.", "The cake was still too hot.", "The cake was burnt."],
             "why": "They had forgotten the sugar, so the cake did not taste nice. It was cool when she tried it.",
             "no": {"The cake was still too hot.": "The text says the cake was cool when Noor cut a slice."}},
            {"id": "95c43ac0f520", "t": "text", "d": "retrieve", "q": "What did they forget to put in? Find and copy the word.",
             "a": ["sugar", "the sugar"],
             "why": "Dad says: we forgot the sugar!"},
            {"id": "31650eaea322", "t": "mcq", "d": "vocab", "q": "Noor took a deep breath. What does this show?",
             "opts": ["She calmed down.", "She had been running.", "She was blowing out candles."],
             "why": "She felt like crying, then took a deep breath to calm down before she tried again."},
            {"id": "87c086f516c8", "t": "mcq", "d": "infer", "q": "Why did Noor tick off each thing on the recipe the second time?",
             "opts": ["so she would not forget anything", "because Dad could not read it", "so the cake would cook faster"],
             "why": "They forgot the sugar the first time, so she ticked things off to make sure nothing was missed."},
        ],
    },
    {
        "key": "RD2.12",
        "year": 2,
        "strand": "Information",
        "title": "Rainbows",
        "nc": "Listen to, discuss and express views about non-fiction; make inferences",
        "text": "Have you ever seen a rainbow after a shower? A rainbow is a curve of colours in the sky.\n\n"
                "You need two things to see a rainbow: sunshine and rain. Sunlight looks white, but it is "
                "really made of many colours mixed together. When sunlight shines through raindrops, "
                "the drops split the light into its colours.\n\n"
                "The colours are always in the same order: red, orange, yellow, green, blue, indigo and violet.\n\n"
                "To spot a rainbow, stand with the sun behind you and look towards the rain. "
                "The best time is often in the morning or late in the afternoon, when the sun is low in the sky.",
        "qs": [
            {"id": "339a1ccc908c", "t": "mcq", "d": "vocab", "q": "A rainbow is a curve of colours. What is a curve?",
             "opts": ["a line that bends", "a straight line", "a small dot"],
             "why": "A curve is a line that bends, like the shape of a rainbow."},
            {"id": "b547ef82faf7", "t": "mcq", "d": "retrieve", "q": "What does sunlight look like, as the text says?",
             "opts": ["white", "yellow", "orange"],
             "why": "The text says sunlight looks white, but it is really made of many colours."},
            {"id": "47bafb634b51", "t": "mcq", "d": "retrieve", "q": "What splits the sunlight into its colours?",
             "opts": ["the raindrops", "the clouds", "the wind"],
             "why": "The text says when sunlight shines through raindrops, the drops split the light into its colours."},
            {"id": "3451d0ade5cd", "t": "mcq", "d": "predict", "q": "It is raining, and the sun is low behind Ben. He looks towards the rain. What will he most likely see?",
             "opts": ["a rainbow", "a dark night sky", "the sun in front of him"],
             "why": "Sun behind you, rain in front of you and a low sun: that is just how the text says to spot a rainbow."},
            {"id": "de72edbfa666", "t": "mcq", "d": "infer", "q": "Why is the middle of the day not the best time to spot a rainbow?",
             "opts": ["The sun is high in the sky.", "It does not rain at midday.", "The sun is behind you."],
             "why": "The best time is when the sun is low. In the middle of the day the sun is high."},
        ],
    },
    {
        "key": "RD2.13",
        "year": 2,
        "strand": "Letters and diaries",
        "title": "Freya's camping diary",
        "nc": "Discuss the sequence of events; discuss and clarify the meanings of words",
        "text": "Friday\n"
                "We drove to the Lake District today. It rained all the way there! Dad and I put up the tent "
                "in the wet. The pegs kept popping out of the soggy grass, but we got it up in the end.\n\n"
                "Saturday\n"
                "The sun came out at last. We walked up a big hill called a fell. My legs ached, but from the top "
                "I could see a long, shiny lake far below. We ate our sandwiches on a rock.\n\n"
                "At night, I lay in my sleeping bag and listened. I heard an owl hooting in the trees.\n\n"
                "Sunday\n"
                "Time to go home. I am tired and muddy, but I want to come back next year!",
        "qs": [
            {"id": "cf148fbd5f65", "t": "mcq", "d": "retrieve", "q": "What was the weather like on Friday?",
             "opts": ["rainy", "sunny", "snowy"],
             "why": "Freya writes that it rained all the way there on Friday. The sun came out on Saturday.",
             "no": {"sunny": "The sun came out on Saturday, not Friday."}},
            {"id": "0986365e44c9", "t": "tap", "d": "vocab", "q": "Tap the word that means very wet.",
             "s": "The pegs kept popping out of the [soggy] grass, but we got it up in the end.",
             "why": "Soggy means very wet and soft. It had rained all day."},
            {"id": "931db6a76c1c", "t": "text", "d": "vocab", "q": "Find and copy the word that is a name for a big hill in the Lake District.",
             "a": ["fell", "a fell", "the fell", "fells"],
             "why": "Freya says they walked up a big hill called a fell."},
            {"id": "19fb1c17d4c0", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the diary.",
             "items": ["Freya and Dad put up the tent.", "They walked up a fell.",
                       "Freya heard an owl.", "It was time to go home."],
             "why": "The tent went up on Friday; the walk and the owl were on Saturday; they went home on Sunday."},
            {"id": "1233c605024c", "t": "mcq", "d": "infer", "q": "How does Freya feel about the trip?",
             "opts": ["She enjoyed it.", "She was bored.", "She never wants to go again."],
             "why": "She is tired and muddy, but she wants to come back next year, so she enjoyed it.",
             "no": {"She never wants to go again.": "She says she wants to come back next year."}},
        ],
    },
    {
        "key": "RD2.14",
        "year": 2,
        "strand": "Stories",
        "title": "The red purse",
        "nc": "Make inferences on the basis of what is being said and done; discuss word meanings",
        "text": "Mateo and his mum were walking through the park in Seville when Mateo saw something red "
                "under a bench. It was a purse! Inside were some coins, a bus ticket and a photo of a little girl.\n\n"
                "“We could buy ice creams with this,” Mateo said. Then he looked at the photo again. "
                "“But someone must be very worried.”\n\n"
                "Mum and Mateo looked around. At the other end of the park, an old woman was searching "
                "under the bushes. She looked upset.\n\n"
                "“Excuse me,” said Mateo. “Is this yours?”\n\n"
                "The woman's face lit up. “Yes! That is a photo of my granddaughter,” she said. "
                "“Thank you so much.”\n\n"
                "Mateo felt warm inside all the way home. It was better than any ice cream.",
        "qs": [
            {"id": "e4d67d5169fe", "t": "mcq", "d": "retrieve", "q": "Where did Mateo find the purse?",
             "opts": ["under a bench", "under the bushes", "on a bus"],
             "why": "The first sentence says he saw something red under a bench.",
             "no": {"under the bushes": "The old woman was searching under the bushes, but the purse was under a bench."}},
            {"id": "ca3a59688bd8", "t": "mcq", "d": "retrieve", "q": "What was inside the purse?",
             "opts": ["coins, a bus ticket and a photo", "ice creams, coins and a key", "a photo, a key and a phone"],
             "why": "The text says inside were some coins, a bus ticket and a photo of a little girl."},
            {"id": "c9f29fb18b0e", "t": "mcq", "d": "infer", "q": "Why did Mateo change his mind about the ice creams?",
             "opts": ["He thought about who had lost it.", "Mum said no to ice cream.", "The coins were not real."],
             "why": "He looked at the photo and said someone must be very worried."},
            {"id": "7241d5cd6f4e", "t": "mcq", "d": "vocab", "q": "The woman's face lit up. What does this mean?",
             "opts": ["She suddenly looked very happy.", "The sun shone on her face.", "Her face went very red."],
             "why": "When your face lights up, you suddenly look very happy."},
            {"id": "14fb8f21ba70", "t": "mcq", "d": "infer", "q": "Which word best describes Mateo?",
             "opts": ["caring", "greedy", "careless"],
             "why": "He thought about the worried owner and gave the purse back, so he is caring.",
             "no": {"greedy": "He thought about ice cream, but he gave the purse back."}},
        ],
    },
]
