"""Reading comprehension, Year 2, second set (keys RD2.15-RD2.28).

Fourteen more original passages (80-160 words) for children aged 6-7, on topics not used in
reading_y2.py, each with five questions in the KS1 reading domains only (vocab, retrieve, sequence,
infer, predict). Questions are mcq with three options, tap (a sentence copied exactly from the passage),
order (3-4 events) and, in some passages, text (find and copy a word or short phrase).

* Stories: RD2.15, RD2.17, RD2.21, RD2.24, RD2.28
* Information: RD2.16, RD2.19, RD2.23, RD2.25, RD2.27
* Instructions: RD2.20
* Poems: RD2.18
* Letters and diaries: RD2.22, RD2.26

Written by hand; to be reviewed line by line by a second reader (a teacher or a parent) before release.
"""

SKILLS = [
    {
        "key": "RD2.15",
        "year": 2,
        "strand": "Stories",
        "title": "The broken pot",
        "nc": "Make inferences on the basis of what is being said and done; predict what might happen",
        "text": "Kai was not allowed to play football in the house. But one rainy afternoon he was bored, "
                "so he kicked his ball gently along the hall.\n\n"
                "The ball bounced off the wall and hit Mum's plant pot. Crash! The pot broke, "
                "and soil spilled all over the floor.\n\n"
                "Kai's heart thumped. He could push the pieces under the rug and say nothing. "
                "But that would be a lie.\n\n"
                "He went to the kitchen. “Mum, I broke your pot,” he said in a small voice. "
                "“I was playing football in the hall.”\n\n"
                "Mum looked at the mess. Then she looked at Kai. “Thank you for telling me the truth,” she said. "
                "“Now let's clean it up together. And next time, the ball stays in the garden.”",
        "qs": [
            {"id": "57caf73c439b", "t": "mcq", "d": "retrieve", "q": "Why did Kai kick the ball in the hall?",
             "opts": ["He was bored on a rainy day.", "Mum said he could.", "The garden was too small."],
             "why": "The first part says it was a rainy afternoon and Kai was bored.",
             "no": {"Mum said he could.": "The first sentence says Kai was not allowed to play football in the house."}},
            {"id": "ea557ebd51ae", "t": "text", "d": "retrieve", "q": "Find and copy the word for what spilled all over the floor.",
             "a": ["soil", "the soil"],
             "why": "The second part says the pot broke, and soil spilled all over the floor."},
            {"id": "71d79a6cce9e", "t": "tap", "d": "vocab", "q": "Tap the word that shows Kai's heart was beating hard.",
             "s": "Kai's heart [thumped].",
             "why": "To thump is to beat hard and loud. Kai's heart thumped because he was worried."},
            {"id": "a2651edc0003", "t": "mcq", "d": "infer", "q": "Why did Kai speak in a small voice?",
             "opts": ["He was worried about what Mum would say.", "He had a sore throat.",
                      "He did not want Mum to hear him."],
             "why": "Kai had broken the pot and done something he was not allowed to do, so he was worried.",
             "no": {"He did not want Mum to hear him.": "He went to find Mum to tell her, so he did want her to hear."}},
            {"id": "73638d2e2c5c", "t": "mcq", "d": "predict", "q": "Where will Kai most likely play football next time?",
             "opts": ["in the garden", "in the hall", "in the kitchen"],
             "why": "Mum says: next time, the ball stays in the garden."},
        ],
    },
    {
        "key": "RD2.16",
        "year": 2,
        "strand": "Information",
        "title": "Hedgehogs",
        "nc": "Retrieve information from non-fiction; discuss and clarify the meanings of words",
        "text": "A hedgehog is a small wild animal. Its back is covered in sharp spines. "
                "When it is scared, it rolls up into a tight, prickly ball, so other animals cannot bite its soft tummy.\n\n"
                "Hedgehogs are nocturnal. This means they sleep in the day and come out at night. "
                "They snuffle through gardens and hedges, looking for beetles, worms and slugs to eat.\n\n"
                "In winter, there is not much food. So hedgehogs make a nest of leaves and go into a long, "
                "deep sleep called hibernation. They wake up again in spring.\n\n"
                "You can help hedgehogs by leaving a small gap under your garden fence, so they can move from "
                "garden to garden. Never give them milk, because it makes them ill.",
        "qs": [
            {"id": "644b869e8fbe", "t": "mcq", "d": "retrieve", "q": "Why does a hedgehog roll up into a ball?",
             "opts": ["so other animals cannot bite its soft tummy", "to keep warm in its winter nest",
                      "so it can roll along to find food"],
             "why": "The first part says it rolls up so other animals cannot bite its soft tummy."},
            {"id": "76e02b97d0ed", "t": "text", "d": "vocab", "q": "Find and copy the word that means sleeping in the day and coming out at night.",
             "a": ["nocturnal"],
             "why": "The second part says hedgehogs are nocturnal: they sleep in the day and come out at night."},
            {"id": "797b14ceb083", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the hedgehog sniffs about noisily as it looks for food.",
             "s": "They [snuffle] through gardens and hedges, looking for beetles, worms and slugs to eat.",
             "why": "To snuffle is to sniff noisily, nose down, the way a hedgehog hunts for food."},
            {"id": "2ea5e339f564", "t": "mcq", "d": "infer", "q": "Why do hedgehogs hibernate in winter?",
             "opts": ["There is not much food to find.", "Their spines fall out.", "The nights are too short."],
             "why": "The third part says there is not much food in winter, so hedgehogs sleep until spring."},
            {"id": "ed765c0e0c95", "t": "mcq", "d": "retrieve", "q": "What does the text say you can do to help hedgehogs?",
             "opts": ["Leave a gap under the fence.", "Give them a bowl of milk.", "Wake them up in winter."],
             "why": "The last part says to leave a small gap under the fence so they can move from garden to garden.",
             "no": {"Give them a bowl of milk.": "The text says never give them milk, because it makes them ill."}},
        ],
    },
    {
        "key": "RD2.17",
        "year": 2,
        "strand": "Stories",
        "title": "Mateo learns to swim",
        "nc": "Discuss the sequence of events in a story; make inferences on the basis of what is being said and done",
        "text": "Every Saturday, Mateo went to swimming lessons. The other children jumped in with a splash, "
                "but Mateo sat on the edge with his toes in the water. The deep end looked dark and scary.\n\n"
                "His teacher, Gemma, smiled at him. “Let's start in the shallow end,” she said. "
                "“You can stand up here.”\n\n"
                "The first week, Mateo just walked in the water. The next week, he put his face in and blew bubbles. "
                "After that, he kicked his legs while he held a float.\n\n"
                "Week by week, he grew braver. Then one Saturday, Gemma took the float away. "
                "Mateo kicked and pulled with his arms, and he swam five whole metres on his own!\n\n"
                "When he climbed out, he was grinning from ear to ear.",
        "qs": [
            {"id": "ec27eb76b987", "t": "mcq", "d": "infer", "q": "Why did Mateo sit on the edge at first?",
             "opts": ["He was scared of the water.", "The water was too cold.", "Gemma told him to wait."],
             "why": "The deep end looked dark and scary to him, so he did not want to jump in."},
            {"id": "fb72217e84d2", "t": "mcq", "d": "vocab", "q": "Gemma said, “Let's start in the shallow end.” What is the shallow end?",
             "opts": ["where the water is not very deep", "where the water is very cold", "where the big children swim"],
             "why": "Shallow means not deep. Gemma says: you can stand up here."},
            {"id": "be16f2f4319e", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Mateo walked in the water.", "Mateo blew bubbles.", "Mateo kicked while holding a float.",
                       "Mateo swam on his own."],
             "why": "The first week he walked, the next week he blew bubbles, after that he used a float, and then he swam alone."},
            {"id": "04154d54bfe7", "t": "text", "d": "retrieve", "q": "Find and copy how far Mateo swam on his own.",
             "a": ["five whole metres", "five metres", "5 whole metres", "5 metres", "5 m"],
             "why": "The fourth part says he swam five whole metres on his own."},
            {"id": "aade3437a759", "t": "mcq", "d": "vocab", "q": "Mateo was grinning from ear to ear. This means he was…",
             "opts": ["very happy", "very tired", "very cold"],
             "why": "A grin from ear to ear is a very big smile, so he was very happy."},
        ],
    },
    {
        "key": "RD2.18",
        "year": 2,
        "strand": "Poems",
        "title": "Autumn leaves",
        "nc": "Continue to build up a repertoire of poems; discuss and clarify the meanings of words",
        "text": "The leaves are turning red and brown,\n"
                "They twirl and swirl and flutter down.\n"
                "They dance across the garden wall,\n"
                "Then settle softly, one and all.\n\n"
                "I kick them high, I kick them wide,\n"
                "I hear them crunching as I stride.\n"
                "The squirrels scamper, quick and neat,\n"
                "And bury nuts down by my feet.\n\n"
                "The trees stand bare against the sky,\n"
                "The geese go honking, flying by.\n"
                "Then Grandma calls, “It's getting cold!”\n"
                "So in I go, with leaves of gold.",
        "qs": [
            {"id": "c62c083c98db", "t": "mcq", "d": "retrieve", "q": "In the first verse, what colours are the leaves turning?",
             "opts": ["red and brown", "green and gold", "yellow and green"],
             "why": "The first line says the leaves are turning red and brown."},
            {"id": "b9cbc0b4afb8", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the leaves make a noise when the child walks on them.",
             "s": "I hear them [crunching] as I stride.",
             "why": "Crunching is the crackly noise dry leaves make when you step on them."},
            {"id": "b1be40e70e99", "t": "mcq", "d": "retrieve", "q": "What do the squirrels do?",
             "opts": ["bury nuts", "eat the leaves", "climb the garden wall"],
             "why": "The second verse says the squirrels bury nuts down by my feet."},
            {"id": "7ed36da8caed", "t": "mcq", "d": "vocab", "q": "“The trees stand bare against the sky.” What does bare mean here?",
             "opts": ["with no leaves on", "very tall", "covered in snow"],
             "why": "The leaves have all fallen down, so the trees are bare: they have no leaves on."},
            {"id": "79ad8a98aed9", "t": "mcq", "d": "infer", "q": "How does the child feel about playing in the leaves?",
             "opts": ["They enjoy it.", "They are bored.", "They are scared of the squirrels."],
             "why": "The child kicks the leaves high and wide and only goes in when Grandma calls, so they are having fun."},
        ],
    },
    {
        "key": "RD2.19",
        "year": 2,
        "strand": "Information",
        "title": "Busy ants",
        "nc": "Retrieve information from non-fiction; discuss the sequence of events in non-fiction",
        "text": "Ants are small insects. Like all insects, an ant has six legs, and its body is made of three parts.\n\n"
                "Ants live together in big groups called colonies. Many colonies live in nests under the ground. "
                "A nest has lots of tunnels and rooms. In one room, the queen ant lays eggs. "
                "In other rooms, worker ants look after the young ants.\n\n"
                "Worker ants go out to find food. When an ant finds some, it leaves a trail of smell on its way home. "
                "Other ants follow the smell, and it leads them to the food too.\n\n"
                "Ants are very strong for their size. One ant can carry a crumb much bigger than its own head.",
        "qs": [
            {"id": "4da9ebcb56fb", "t": "text", "d": "vocab", "q": "Find and copy the word for big groups of ants that live together.",
             "a": ["colonies", "colony", "a colony"],
             "why": "The second part says ants live together in big groups called colonies."},
            {"id": "79e663bc03c4", "t": "mcq", "d": "retrieve", "q": "Who lays the eggs in the nest?",
             "opts": ["the queen ant", "the worker ants", "the young ants"],
             "why": "The second part says that in one room, the queen ant lays eggs.",
             "no": {"the worker ants": "The worker ants look after the young ants and find food."}},
            {"id": "ce475e1562ef", "t": "order", "d": "sequence", "q": "Put these in the order they happen.",
             "items": ["An ant finds some food.", "It leaves a trail of smell on its way home.",
                       "Other ants follow the smell to the food."],
             "why": "The ant finds food first, then leaves a smell trail going home, then the others follow it."},
            {"id": "0bdbe7ca15fa", "t": "mcq", "d": "infer", "q": "Why does an ant leave a trail of smell?",
             "opts": ["so other ants can find the food", "so it can find the way out of the nest",
                      "to keep other insects away"],
             "why": "Other ants follow the smell, and it leads them to the food."},
            {"id": "9ff15e1fc7da", "t": "mcq", "d": "vocab", "q": "Ants are very strong for their size. What does this mean?",
             "opts": ["They are strong for such small animals.", "They are bigger than other insects.",
                      "They are stronger than people."],
             "why": "For their size means for something so small. An ant is tiny, but it can carry a big crumb."},
        ],
    },
    {
        "key": "RD2.20",
        "year": 2,
        "strand": "Instructions",
        "title": "How to grow cress",
        "nc": "Read and follow instructions; discuss the sequence of events in non-fiction",
        "text": "Cress is a tiny plant that grows very fast. You can grow it on a windowsill and eat it in a sandwich.\n\n"
                "You will need a small pot, some cotton wool, water and a packet of cress seeds.\n\n"
                "1. Put a layer of cotton wool in the bottom of the pot.\n"
                "2. Pour on some water until the cotton wool is wet, but not swimming in water.\n"
                "3. Sprinkle the seeds thinly over the top.\n"
                "4. Put the pot on a sunny windowsill.\n"
                "5. Check the cotton wool every day. Add a little water if it feels dry.\n"
                "6. After about a week, ask a grown-up to help you snip the cress with scissors. Wash it and enjoy!",
        "qs": [
            {"id": "a1947118654d", "t": "text", "d": "retrieve", "q": "Find and copy what you put in the bottom of the pot.",
             "a": ["cotton wool", "some cotton wool", "a layer of cotton wool"],
             "why": "Step 1 says to put a layer of cotton wool in the bottom of the pot."},
            {"id": "a2fc642d5b8e", "t": "mcq", "d": "vocab", "q": "In step 3, what does “sprinkle the seeds thinly” mean?",
             "opts": ["scatter a few seeds all over the top", "push the seeds deep down",
                      "put all the seeds in one pile"],
             "why": "To sprinkle thinly is to scatter a few at a time so they spread out over the top."},
            {"id": "85f1f0f5cbe3", "t": "order", "d": "sequence", "q": "Put these steps in the right order.",
             "items": ["Put cotton wool in the pot.", "Pour on some water.", "Sprinkle the seeds.",
                       "Put the pot on a windowsill."],
             "why": "Cotton wool is step 1, water is step 2, seeds are step 3 and the windowsill is step 4."},
            {"id": "3b054f2c7285", "t": "mcq", "d": "retrieve", "q": "Where should you put the pot?",
             "opts": ["on a sunny windowsill", "in a dark cupboard", "out in the garden"],
             "why": "Step 4 says: put the pot on a sunny windowsill."},
            {"id": "c62afb5df7e9", "t": "mcq", "d": "infer", "q": "Why do you need to check the cotton wool every day?",
             "opts": ["The seeds need water to grow.", "The seeds might blow away.", "The cress might grow too tall."],
             "why": "Step 5 says to add water if it feels dry, because the seeds need water to keep growing."},
        ],
    },
    {
        "key": "RD2.21",
        "year": 2,
        "strand": "Stories",
        "title": "Biscuit in the park",
        "nc": "Make inferences on the basis of what is being said and done; discuss and clarify the meanings of words",
        "text": "On Sunday morning, Sami and his big sister Leila were walking in the park when a small brown dog "
                "trotted up to them. It had no owner with it, and its lead was dragging along the path.\n\n"
                "“It must be lost,” said Leila. The dog was shivering, so Sami knelt down and stroked its ears gently.\n\n"
                "Leila looked at the dog's collar. There was a little metal tag on it with a name, Biscuit, "
                "and a phone number.\n\n"
                "They called the number on Leila's phone. Ten minutes later, a lady came running across the grass. "
                "“Biscuit!” she cried. The dog's tail wagged so fast that it was just a blur.\n\n"
                "“He ran off after a squirrel,” the lady said. “Thank you for looking after him.”",
        "qs": [
            {"id": "c0862b20e11d", "t": "mcq", "d": "infer", "q": "How did Leila know the dog was lost?",
             "opts": ["No owner was with it, and its lead was dragging.", "It had a tag on its collar.",
                      "It came running across the grass."],
             "why": "The dog was on its own with its lead dragging, so Leila guessed it had run away from its owner.",
             "no": {"It had a tag on its collar.": "Leila only looked at the tag after she said it must be lost."}},
            {"id": "8ef42636343c", "t": "tap", "d": "vocab", "q": "Tap the word that shows the dog was shaking.",
             "s": "The dog was [shivering], so Sami knelt down and stroked its ears gently.",
             "why": "To shiver is to shake a little, when you are cold or scared."},
            {"id": "41bd796ab198", "t": "text", "d": "retrieve", "q": "Find and copy the dog's name.",
             "a": ["Biscuit"],
             "why": "The tag on the collar had the name Biscuit on it."},
            {"id": "36c3b5c804b4", "t": "mcq", "d": "infer", "q": "The dog's tail wagged so fast it was just a blur. What does this show?",
             "opts": ["The dog was very happy to see the lady.", "The dog was tired from running.",
                      "The dog was scared of the lady."],
             "why": "Dogs wag their tails when they are happy. Biscuit was glad his owner had come."},
            {"id": "61e11591ce61", "t": "mcq", "d": "retrieve", "q": "Why had Biscuit run off?",
             "opts": ["He chased a squirrel.", "He was scared of Sami.", "He wanted to find Leila."],
             "why": "The lady says: he ran off after a squirrel."},
        ],
    },
    {
        "key": "RD2.22",
        "year": 2,
        "strand": "Letters and diaries",
        "title": "Thank you, Mr Hughes",
        "nc": "Make inferences on the basis of what is being said and done; predict what might happen",
        "text": "Dear Mr Hughes,\n\n"
                "Thank you for showing Class 2 around the zoo last Tuesday. We all had a brilliant time.\n\n"
                "My favourite part was feeding the giraffes. I held up a bunch of leaves, and a giraffe wrapped "
                "its long, dark tongue round them. It felt rough and a bit slimy! "
                "I did not know that giraffes have such dark tongues.\n\n"
                "I also liked the meerkats. One stood up tall on its back legs to keep watch, "
                "while the others dug in the sand.\n\n"
                "Next term, we are going to make a class book about the animals we saw. We will send you a copy.\n\n"
                "Best wishes,\nTobi",
        "qs": [
            {"id": "7ee4259b874e", "t": "mcq", "d": "retrieve", "q": "When did Class 2 visit the zoo?",
             "opts": ["last Tuesday", "next term", "last Friday"],
             "why": "The first line says Mr Hughes showed Class 2 around the zoo last Tuesday.",
             "no": {"next term": "Next term is when they will make their class book."}},
            {"id": "52c281f4075b", "t": "mcq", "d": "retrieve", "q": "What was Tobi's favourite part?",
             "opts": ["feeding the giraffes", "watching the meerkats", "digging in the sand"],
             "why": "Tobi says: my favourite part was feeding the giraffes. Tobi also liked the meerkats.",
             "no": {"watching the meerkats": "Tobi also liked the meerkats, but feeding the giraffes was the favourite part."}},
            {"id": "d67c5665d1f8", "t": "tap", "d": "vocab", "q": "Tap the two words that tell you how the giraffe's tongue felt.",
             "s": "It felt [rough] and a bit [slimy]!",
             "why": "Tobi says the tongue felt rough and a bit slimy."},
            {"id": "69839b5270c8", "t": "mcq", "d": "infer", "q": "Why did Tobi write to Mr Hughes?",
             "opts": ["to thank him for the zoo visit", "to ask if Class 2 can come again", "to ask him about meerkats"],
             "why": "The letter starts with thank you, and it is all about the visit he showed them."},
            {"id": "7a8251bbef15", "t": "mcq", "d": "predict", "q": "What will Mr Hughes most likely get from Class 2 next term?",
             "opts": ["a copy of their class book", "some leaves for the giraffes", "a meerkat for the zoo"],
             "why": "Tobi says they will make a class book next term and send him a copy."},
        ],
    },
    {
        "key": "RD2.23",
        "year": 2,
        "strand": "Information",
        "title": "Trains, then and now",
        "nc": "Retrieve information from non-fiction; discuss the sequence of events in non-fiction",
        "text": "About two hundred years ago, some of the first railways were built in Britain. "
                "Their trains were pulled by steam engines.\n\n"
                "A steam engine burned coal to heat water. The hot water turned into steam, and the steam pushed "
                "the parts that turned the wheels. Steam trains puffed out clouds of smoke, and they were noisy and dirty.\n\n"
                "Most trains today are faster and cleaner. Many run on electricity from wires above the track.\n\n"
                "Before there were trains, many people never went far from home. A long journey by horse and cart "
                "could take days. Trains changed that. Now people could visit the seaside, and food and letters "
                "could be carried quickly across the country.",
        "qs": [
            {"id": "e92eccc8088b", "t": "mcq", "d": "retrieve", "q": "What did a steam engine burn?",
             "opts": ["coal", "wood", "oil"],
             "why": "The second part says a steam engine burned coal to heat water."},
            {"id": "eb318386ea71", "t": "order", "d": "sequence", "q": "Put these in the order they happen in a steam engine.",
             "items": ["Coal is burned.", "The water turns into steam.", "The steam pushes the parts that turn the wheels."],
             "why": "The coal heats the water, the hot water turns into steam, and the steam pushes the parts."},
            {"id": "83560adc6f2a", "t": "mcq", "d": "retrieve", "q": "Where do many trains today get their electricity from?",
             "opts": ["wires above the track", "coal in the engine", "the wheels on the track"],
             "why": "The third part says many trains run on electricity from wires above the track."},
            {"id": "56b20caef926", "t": "text", "d": "vocab", "q": "Find and copy the word in the last part that means a trip from one place to another.",
             "a": ["journey", "a journey", "a long journey", "long journey"],
             "why": "The last part says a long journey by horse and cart could take days."},
            {"id": "2fecd1a6136d", "t": "mcq", "d": "infer", "q": "Why did many people never go far from home before there were trains?",
             "opts": ["Travelling took a very long time.", "There was no seaside to visit.",
                      "Horses were not allowed on roads."],
             "why": "A long journey by horse and cart could take days, so many people stayed near home."},
        ],
    },
    {
        "key": "RD2.24",
        "year": 2,
        "strand": "Stories",
        "title": "The fox cubs",
        "nc": "Make inferences on the basis of what is being said and done; predict what might happen",
        "text": "Ellie was staying with Gran in the city for a week in May. One evening, Gran whispered, "
                "“Come to the window, quietly.”\n\n"
                "At the bottom of the garden, by the old shed, Ellie saw a fox. It had a bushy tail with a white tip. "
                "Then three small, fluffy cubs tumbled out from under the shed.\n\n"
                "The cubs played like puppies. They chased each other, pounced on leaves and rolled over and over "
                "on the grass. The mother fox sat and watched them.\n\n"
                "Ellie pressed her nose to the glass. Suddenly, a door banged next door. The mother fox gave a sharp "
                "bark, and in a flash all the cubs dashed back under the shed.\n\n"
                "“Will they come back?” asked Ellie.\n\n"
                "“Most evenings,” said Gran, smiling. “We'll watch again tomorrow.”",
        "qs": [
            {"id": "362d4bbe0614", "t": "tap", "d": "vocab", "q": "Tap the word that tells you the cubs came out rolling and falling over.",
             "s": "Then three small, fluffy cubs [tumbled] out from under the shed.",
             "why": "To tumble is to roll and fall over. The cubs tumbled out from under the shed."},
            {"id": "8ac902328f14", "t": "mcq", "d": "vocab", "q": "The cubs pounced on leaves. What did they do?",
             "opts": ["jumped on them suddenly", "ate them up", "hid under them"],
             "why": "To pounce is to jump on something suddenly, like a cat jumping on a toy."},
            {"id": "1615e4739d2b", "t": "mcq", "d": "retrieve", "q": "What did the mother fox do while the cubs played?",
             "opts": ["She sat and watched them.", "She chased the cubs.", "She hid under the shed."],
             "why": "The third part says the mother fox sat and watched them."},
            {"id": "df99d05a83b3", "t": "mcq", "d": "infer", "q": "Why did the cubs dash back under the shed?",
             "opts": ["The bang made their mother warn them.", "Ellie tapped on the glass.", "It was time to eat."],
             "why": "A door banged, and the mother fox gave a sharp bark. The cubs ran to hide.",
             "no": {"Ellie tapped on the glass.": "Ellie pressed her nose to the glass, but it was the door next door that banged."}},
            {"id": "2f7e87b814dd", "t": "mcq", "d": "predict", "q": "What will Ellie and Gran most likely do tomorrow evening?",
             "opts": ["watch for the foxes again", "go out and chase the cubs", "move the old shed"],
             "why": "Gran says the foxes come most evenings and they will watch again tomorrow."},
        ],
    },
    {
        "key": "RD2.25",
        "year": 2,
        "strand": "Information",
        "title": "Deserts",
        "nc": "Retrieve information from non-fiction; discuss and clarify the meanings of words",
        "text": "A desert is a place that gets very little rain. Some deserts are covered in sand, but others are rocky.\n\n"
                "Many deserts are very hot in the day. But at night, with no clouds to keep the warmth in, "
                "they can get very cold.\n\n"
                "Plants and animals that live in deserts have clever ways to cope. A cactus stores water in its "
                "thick stem, and it has spines instead of flat leaves.\n\n"
                "A camel can walk for days without drinking. Its wide feet help it walk on soft sand without sinking, "
                "and long eyelashes keep the sand out of its eyes. The hump on its back stores fat, not water.\n\n"
                "The Sahara, in Africa, is the biggest hot desert in the world.",
        "qs": [
            {"id": "b5fd894eff40", "t": "mcq", "d": "retrieve", "q": "What makes a place a desert, says the text?",
             "opts": ["It gets very little rain.", "It is covered in sand.", "It is hot all the time."],
             "why": "The first sentence says a desert is a place that gets very little rain.",
             "no": {"It is covered in sand.": "The text says some deserts are rocky, not sandy.",
                    "It is hot all the time.": "The text says deserts can get very cold at night."}},
            {"id": "945d165926fd", "t": "mcq", "d": "vocab", "q": "Desert plants and animals have clever ways to cope. What does cope mean?",
             "opts": ["manage in a hard place", "hide from people", "grow very big"],
             "why": "To cope is to manage when things are hard. Little rain makes a desert a hard place to live."},
            {"id": "831008efe2ed", "t": "mcq", "d": "infer", "q": "Why is a cactus good at living in a desert?",
             "opts": ["It keeps water in its stem for dry times.", "It has big flat leaves to catch rain.",
                      "It grows only where there is shade."],
             "why": "A cactus stores water in its thick stem, so it has water when there is no rain."},
            {"id": "334b712fc84b", "t": "text", "d": "retrieve", "q": "Find and copy what a camel's hump stores.",
             "a": ["fat"],
             "why": "The text says the hump stores fat, not water.",
             "no": {"water": "The text says the hump stores fat, not water."}},
            {"id": "c1ae88f16fe9", "t": "mcq", "d": "retrieve", "q": "What does the text say about the Sahara?",
             "opts": ["It is the biggest hot desert in the world.", "It is a rocky desert with no sand.",
                      "It is the coldest desert in the world."],
             "why": "The last sentence says the Sahara, in Africa, is the biggest hot desert in the world."},
        ],
    },
    {
        "key": "RD2.26",
        "year": 2,
        "strand": "Letters and diaries",
        "title": "Ibrahim's broken arm",
        "nc": "Discuss the sequence of events; make inferences on the basis of what is being said and done",
        "text": "Saturday\n"
                "I fell off the climbing frame at the park and hurt my arm. Mum took me to the hospital. "
                "I had an X-ray, which is a photo of the bones inside you. It showed that my arm was broken! "
                "The doctor put a bright blue cast on it. The cast keeps the bone still so it can mend.\n\n"
                "Sunday\n"
                "The cast is hard and heavy. My arm feels itchy inside it.\n\n"
                "Monday\n"
                "I went back to school. Everyone wanted to write their name on my cast. "
                "My best friend Jack drew a rocket on it.\n\n"
                "Tuesday\n"
                "Writing is tricky, because it is my right arm. Mr Shah let me tell my story to a partner instead.\n\n"
                "The doctor says the cast can come off in about four weeks. I can't wait!",
        "qs": [
            {"id": "0c51471766d0", "t": "mcq", "d": "retrieve", "q": "How did Ibrahim hurt his arm?",
             "opts": ["He fell off the climbing frame.", "He fell off his bike.", "He tripped at school."],
             "why": "On Saturday he wrote that he fell off the climbing frame at the park."},
            {"id": "0a3292796ece", "t": "text", "d": "vocab", "q": "Find and copy the word for a photo of the bones inside you.",
             "a": ["X-ray", "an X-ray", "xray"],
             "why": "Saturday's part says an X-ray is a photo of the bones inside you."},
            {"id": "9bff20bc9c5a", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the diary.",
             "items": ["Ibrahim fell off the climbing frame.", "Ibrahim had an X-ray.",
                       "Everyone wrote their name on the cast.", "Mr Shah let him tell his story to a partner."],
             "why": "The fall and the X-ray were on Saturday, the names on Monday and Mr Shah's help on Tuesday."},
            {"id": "85f0b59ca46b", "t": "mcq", "d": "infer", "q": "Why is writing tricky for Ibrahim?",
             "opts": ["His right arm is in a cast.", "He has forgotten how to spell.", "Jack keeps drawing on his cast."],
             "why": "His right arm is broken and in a heavy cast, and that is the hand he writes with."},
            {"id": "a7458ef10efb", "t": "mcq", "d": "infer", "q": "Ibrahim writes, “I can't wait!” How does he feel about the cast coming off?",
             "opts": ["He is looking forward to it.", "He is worried about it.", "He does not mind either way."],
             "why": "“I can't wait” means you really want something to happen soon."},
        ],
    },
    {
        "key": "RD2.27",
        "year": 2,
        "strand": "Information",
        "title": "Night and day",
        "nc": "Retrieve information from non-fiction; make inferences from the text",
        "text": "Every morning, the Sun seems to rise in the east, and every evening it seems to set in the west. "
                "But the Sun is not really moving across the sky. It is the Earth that is moving.\n\n"
                "The Earth is always spinning, like a very slow spinning top. It takes one whole day, "
                "twenty-four hours, to spin round once.\n\n"
                "As the Earth spins, one half faces the Sun. On that half, it is daytime. "
                "The other half faces away from the Sun, into dark space. On that half, it is night.\n\n"
                "So when it is lunchtime in London, it is night in New Zealand, on the other side of the world. "
                "Children there are fast asleep in bed!",
        "qs": [
            {"id": "01b00d083010", "t": "mcq", "d": "vocab", "q": "The Sun seems to rise. What does seems mean here?",
             "opts": ["looks as if it does", "really does", "does very fast"],
             "why": "Seems means it looks that way. The text says the Sun is not really moving: the Earth is.",
             "no": {"really does": "The text says the Sun is not really moving across the sky."}},
            {"id": "aa08d549490f", "t": "mcq", "d": "retrieve", "q": "What is really moving, according to the text?",
             "opts": ["the Earth", "the Sun", "the sky"],
             "why": "The first part says it is the Earth that is moving, not the Sun."},
            {"id": "ceeb2302e0d8", "t": "text", "d": "retrieve", "q": "Find and copy how many hours it takes the Earth to spin round once.",
             "a": ["twenty-four", "twenty-four hours", "twenty four", "twenty four hours", "24", "24 hours"],
             "why": "The second part says it takes one whole day, twenty-four hours, to spin round once."},
            {"id": "4bfe36cda246", "t": "mcq", "d": "retrieve", "q": "Why is it night on one half of the Earth?",
             "opts": ["That half faces away from the Sun.", "The Sun has gone out.", "Clouds cover that half."],
             "why": "The third part says the half that faces away from the Sun has night."},
            {"id": "c2749089dd81", "t": "mcq", "d": "infer", "q": "It is lunchtime in London. Why are children in New Zealand asleep?",
             "opts": ["New Zealand is facing away from the Sun.", "Children in New Zealand go to bed after lunch.",
                      "New Zealand is too cold for children."],
             "why": "New Zealand is on the other side of the world, so it is on the half facing away from the Sun."},
        ],
    },
    {
        "key": "RD2.28",
        "year": 2,
        "strand": "Stories",
        "title": "The lemonade stall",
        "nc": "Discuss the sequence of events in a story; make inferences on the basis of what is being said and done",
        "text": "The school library needed new books, so Lena decided to help. She and her brother Felix set up "
                "a stall outside their house to sell lemonade.\n\n"
                "Dad helped them squeeze the lemons. They added water and a little sugar, and stirred it all in "
                "a big jug. Felix made a sign that said: LEMONADE 50p A CUP.\n\n"
                "At first, nobody stopped. Felix sighed and kicked at the pavement. "
                "But Lena kept smiling and waving at the people walking past.\n\n"
                "Then Mrs Ahmed from next door bought a cup. She told her friends, and soon there was a queue! "
                "By the end of the afternoon, the jug was empty and the money tin was heavy.\n\n"
                "On Monday, Lena gave the money to her teacher. “Thank you,” said Miss Kerr. "
                "“This will buy lots of new books for everyone.”",
        "qs": [
            {"id": "4d07a169b3ad", "t": "mcq", "d": "retrieve", "q": "Why did Lena want to sell lemonade?",
             "opts": ["to get money for new library books", "to buy a new toy for herself", "to give Felix something to do"],
             "why": "The first sentence says the school library needed new books, so Lena decided to help."},
            {"id": "cd27c9ac842d", "t": "order", "d": "sequence", "q": "Put these in the order they happen in the story.",
             "items": ["Dad helped squeeze the lemons.", "Felix made a sign.", "Mrs Ahmed bought a cup.",
                       "Lena gave the money to Miss Kerr."],
             "why": "They squeezed the lemons, then Felix made the sign. Later Mrs Ahmed bought a cup, and on Monday Lena gave the money in."},
            {"id": "b8ede7d77847", "t": "mcq", "d": "infer", "q": "How did Felix feel when nobody stopped?",
             "opts": ["fed up", "excited", "scared"],
             "why": "Felix sighed and kicked at the pavement. Both show he was fed up."},
            {"id": "a9a87074ffa5", "t": "mcq", "d": "vocab", "q": "Soon there was a queue. What is a queue?",
             "opts": ["a line of people waiting", "a crowd of people shouting", "a big empty jug"],
             "why": "A queue is a line of people waiting their turn. Lots of people wanted lemonade."},
            {"id": "f4aaed4db9a1", "t": "mcq", "d": "infer", "q": "Why was the money tin heavy at the end of the afternoon?",
             "opts": ["Lots of people had paid for lemonade.", "Dad had put stones in it.", "Lena put her own money in it."],
             "why": "There was a queue and the jug was empty, so lots of people had paid 50p a cup."},
        ],
    },
]
